#!/usr/bin/env python3
"""Deterministic Council routing and voting. No network or model calls."""
import argparse
from collections import Counter
import json
import re
import sys


def unique_ids(values, label):
    if not isinstance(values, list) or any(not isinstance(v, str) or not v for v in values):
        raise ValueError(f'{label} must be a list of nonempty strings')
    if len(values) != len(set(values)):
        raise ValueError(f'{label} contains duplicates')
    return values


def route(data):
    members = data['members']
    ids = unique_ids([m['id'] for m in members], 'members')
    if not 1 <= len(ids) <= 22:
        raise ValueError('route needs 1–22 members')
    providers = data['providers']
    unique_ids([p['name'] for p in providers], 'providers')
    names = [p['name'] for p in providers if p.get('available') is True]
    manual = data.get('manual', {})
    if not isinstance(manual, dict) or any(k not in ids or v not in names for k, v in manual.items()):
        raise ValueError('manual assignments must reference panel members and available providers')
    edges, affinities = set(), {}
    for member in members:
        peers = unique_ids(member.get('polarity_pairs', []), 'polarity_pairs')
        affinity = member.get('provider_affinity', [])
        if not isinstance(affinity, list) or any(not isinstance(p, str) for p in affinity):
            raise ValueError('provider_affinity must be a list of strings')
        if member['id'] in peers:
            raise ValueError('a polarity pair cannot reference itself')
        edges.update(tuple(sorted((member['id'], peer))) for peer in peers if peer in ids)
        affinities[member['id']] = affinity
    edges = sorted(edges)
    if not names:
        return {'status': 'analysis_only', 'assignments': {}, 'conflicts': [],
                'unassigned': ids, 'nodes': 0, 'reason': 'no available provider candidates'}
    limit = data.get('max_nodes', 20000)
    if type(limit) is not int or not 1 <= limit <= 200000:
        raise ValueError('max_nodes must be an integer in 1..200000')
    neighbors = {member: set() for member in ids}
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)

    def conflicts(assignment):
        return [[a, b] for a, b in edges if a in assignment and b in assignment
                and assignment[a] == assignment[b]]

    def next_member(assignment):
        # Saturation first exposes hard triangles before unrelated seats.
        return min((m for m in ids if m not in assignment), key=lambda m: (
            -len({assignment[n] for n in neighbors[m] if n in assignment}),
            -len(neighbors[m]), ids.index(m)))

    def choices(member, assignment):
        counts, affinity = Counter(assignment.values()), affinities[member]
        return sorted(names, key=lambda p: (
            sum(assignment.get(n) == p for n in neighbors[member]), counts[p],
            affinity.index(p) if p in affinity else len(affinity), names.index(p)))

    # Retain a complete assignment even when the bounded search is exhausted.
    best = dict(manual)
    while len(best) < len(ids):
        member = next_member(best)
        best[member] = choices(member, best)[0]
    best_count = len(conflicts(best))
    nodes, exhausted = 0, False

    def search(assignment):
        nonlocal best, best_count, nodes, exhausted
        if best_count == 0:
            return
        if nodes >= limit:
            exhausted = True
            return
        nodes += 1
        current = len(conflicts(assignment))
        if current >= best_count:
            return
        if len(assignment) == len(ids):
            best, best_count = dict(assignment), current
            return
        member = next_member(assignment)
        for provider in choices(member, assignment):
            assignment[member] = provider
            search(assignment)
            del assignment[member]
            if best_count == 0 or exhausted:
                break

    search(dict(manual))
    status = 'satisfied' if best_count == 0 else 'search_limit' if exhausted else 'relaxed'
    return {'status': status, 'assignments': {m: best[m] for m in ids},
            'conflicts': conflicts(best), 'nodes': nodes,
            'provider_counts': dict(Counter(best.values())), 'manual_members': sorted(manual),
            'reason': {'satisfied': 'all polarity pairs separated',
                       'relaxed': 'zero-conflict assignment impossible under supplied constraints',
                       'search_limit': 'search budget exhausted; impossibility not proven'}[status]}


STANCE = re.compile(r'STANCE: ([A-Za-z0-9_-]+) \| CONFIDENCE: (high|med|low) \| DEALBREAKER: (yes|no)')


def tally(data):
    panel = unique_ids(data['panel'], 'panel')
    if not 2 <= len(panel) <= 22:
        raise ValueError('tally needs 2–22 locked panel members')
    mode = data.get('mode', 'full')
    if mode not in ('full', 'quick', 'duo') or (mode == 'duo' and len(panel) != 2):
        raise ValueError('invalid mode or duo panel size')
    domain = data.get('domain_weight')
    if domain is not None and domain not in panel:
        raise ValueError('domain_weight must be a locked panel member or null')
    options = unique_ids(data.get('options', []), 'options')
    if mode != 'duo' and (not 2 <= len(options) <= 4 or 'abstain' in options or
                             any(not re.fullmatch(r'[A-Za-z0-9_-]+', o) for o in options)):
        raise ValueError('provide 2–4 canonical option IDs; abstain is reserved')
    responses = data.get('responses', [])
    response_ids = unique_ids([r['member'] for r in responses], 'responses')
    if any(m not in panel for m in response_ids):
        raise ValueError('response from a member outside the locked panel')
    by_member = {r['member']: r for r in responses}
    executions = Counter(r.get('execution_id') for r in responses if r.get('status') == 'live')
    excluded, accepted = {}, {}
    # Integer half-votes avoid floating-point errors at exactly 2/3.
    weights = {m: 3 if m == domain else 2 for m in panel}
    total, votes = sum(weights.values()), dict.fromkeys(options, 0)
    for member in panel:
        response = by_member.get(member)
        if response is None:
            excluded[member] = 'missing response'
            continue
        if response.get('status') not in ('live', 'degraded', 'offline'):
            raise ValueError('response status must be live, degraded or offline')
        if response['status'] != 'live':
            excluded[member] = response['status']
            continue
        execution = response.get('execution_id')
        if not isinstance(execution, str) or not execution or executions[execution] > 1:
            excluded[member] = 'missing or shared execution_id'
            continue
        text = response.get('text', '')
        if not isinstance(text, str):
            raise ValueError('response text must be a string')
        if mode == 'duo':
            if not text.strip():
                excluded[member] = 'empty response'
                continue
            accepted[member] = {'stance': None, 'dealbreaker': False}
            continue
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        stance_lines = [line for line in lines if line.startswith('STANCE:')]
        match = STANCE.fullmatch(stance_lines[0]) if len(stance_lines) == 1 else None
        if not match or lines[-1] != stance_lines[0]:
            excluded[member] = 'missing or malformed final STANCE line'
            continue
        option, confidence, dealbreaker = match.groups()
        if option not in options and option != 'abstain':
            excluded[member] = 'unknown option ID'
            continue
        accepted[member] = {'stance': option, 'confidence': confidence, 'dealbreaker': dealbreaker == 'yes'}
        if option != 'abstain':
            votes[option] += weights[member]
    required = max(2, (2 * len(panel) + 2) // 3)
    winner = None
    if not accepted:
        status = 'analysis_only'
    elif len(accepted) < required:
        status = 'quorum_unavailable'
    elif mode == 'duo':
        status = 'dialectic'
    else:
        winner = next((o for o, weight in votes.items() if 3 * weight >= 2 * total), None)
        status = 'consensus' if winner else 'split'
    return {'status': status, 'winner': winner,
            'votes': {} if mode == 'duo' else {o: w / 2 for o, w in votes.items()},
            'total_weight': total / 2, 'threshold': total / 3,
            'required_live': required, 'live_count': len(accepted),
            'accepted': accepted, 'excluded': excluded,
            'minority_dealbreakers': [m for m, r in accepted.items()
                                     if r['dealbreaker'] and r['stance'] != winner]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['route', 'tally'])
    parser.add_argument('--input', help='JSON file; defaults to stdin')
    args = parser.parse_args()
    try:
        if args.input:
            with open(args.input, encoding='utf-8') as source:
                data = json.load(source)
        else:
            data = json.load(sys.stdin)
        if not isinstance(data, dict):
            raise ValueError('input must be a JSON object')
        result = route(data) if args.command == 'route' else tally(data)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
