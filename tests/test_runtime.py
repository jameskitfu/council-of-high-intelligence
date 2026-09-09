"""Mechanical decisions that must not depend on a coordinator's prose tally."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RuntimeTests(unittest.TestCase):
    def call(self, command, payload, ok=True):
        helper = ROOT / 'scripts/council_runtime.py'
        self.assertTrue(helper.exists(), 'Missing executable route/tally contract')
        result = subprocess.run([sys.executable, str(helper), command],
                                input=json.dumps(payload), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0 if ok else 2, result.stderr)
        return json.loads(result.stdout)

    def route_input(self, count=2):
        return {'members': [
            {'id': 'jobs', 'polarity_pairs': ['rubin', 'torvalds']},
            {'id': 'rubin', 'polarity_pairs': ['jobs', 'torvalds']},
            {'id': 'torvalds', 'polarity_pairs': ['jobs', 'rubin']}],
            'providers': [{'name': name, 'available': True}
                          for name in ['openai', 'google', 'anthropic'][:count]]}

    def ballot(self):
        return {'mode': 'full', 'panel': ['jobs', 'rubin', 'torvalds'],
                'domain_weight': 'jobs', 'options': ['ship', 'wait'],
                'responses': [self.response('jobs'), self.response('rubin'),
                              self.response('torvalds', 'wait')]}

    @staticmethod
    def response(member, option='ship', status='live', execution_id=None):
        return {'member': member, 'status': status,
                'execution_id': execution_id or member + '/round3',
                'text': f'STANCE: {option} | CONFIDENCE: high | DEALBREAKER: no'}

    def test_two_providers_report_impossible_triangle(self):
        result = self.call('route', self.route_input())
        self.assertEqual(result['status'], 'relaxed')
        self.assertEqual(len(result['assignments']), 3)
        self.assertEqual(len(result['conflicts']), 1)
        for a, b in result['conflicts']:
            self.assertEqual(result['assignments'][a], result['assignments'][b])

    def test_three_providers_separate_triangle(self):
        result = self.call('route', self.route_input(3))
        self.assertEqual(result['status'], 'satisfied')
        self.assertEqual(len(set(result['assignments'].values())), 3)
        self.assertEqual(result['conflicts'], [])

    def test_manual_route_is_preserved_and_conflicts_reported(self):
        payload = self.route_input()
        payload['manual'] = dict.fromkeys(['jobs', 'rubin', 'torvalds'], 'openai')
        result = self.call('route', payload)
        self.assertEqual(result['assignments'], payload['manual'])
        self.assertEqual(len(result['conflicts']), 3)

    def test_unavailable_provider_is_never_assigned(self):
        payload = self.route_input()
        payload['providers'][0]['available'] = False
        result = self.call('route', payload)
        self.assertEqual(set(result['assignments'].values()), {'google'})

    def test_unavailable_manual_route_rejected_without_silent_override(self):
        payload = self.route_input()
        payload['manual'] = {'jobs': 'missing'}
        self.assertIn('error', self.call('route', payload, ok=False))

    def test_no_provider_returns_analysis_only(self):
        payload = self.route_input(0)
        result = self.call('route', payload)
        self.assertEqual(result['status'], 'analysis_only')
        self.assertEqual(result['assignments'], {})

    def test_search_budget_is_reported_not_called_unsatisfiable(self):
        payload = self.route_input()
        payload['max_nodes'] = 1
        result = self.call('route', payload)
        self.assertEqual(result['status'], 'search_limit')
        self.assertEqual(len(result['assignments']), 3)

    def test_weighted_majority_and_minority(self):
        payload = self.ballot()
        payload['responses'][2]['text'] = 'STANCE: wait | CONFIDENCE: low | DEALBREAKER: yes'
        result = self.call('tally', payload)
        self.assertEqual(result['status'], 'consensus')
        self.assertEqual(result['winner'], 'ship')
        self.assertEqual(result['votes'], {'ship': 2.5, 'wait': 1.0})
        self.assertEqual(result['minority_dealbreakers'], ['torvalds'])

    def test_ordinary_pair_cannot_override_domain_seat(self):
        payload = self.ballot()
        payload['responses'] = [self.response('jobs', 'wait'), self.response('rubin'),
                                self.response('torvalds')]
        result = self.call('tally', payload)
        self.assertEqual(result['status'], 'split')
        self.assertIsNone(result['winner'])

    def test_simulated_domain_vote_excluded_without_shrinking_denominator(self):
        payload = self.ballot()
        payload['responses'] = [self.response('jobs', status='degraded'),
                                self.response('rubin'), self.response('torvalds')]
        result = self.call('tally', payload)
        self.assertEqual(result['votes'], {'ship': 2.0, 'wait': 0.0})
        self.assertEqual(result['total_weight'], 3.5)
        self.assertEqual(result['status'], 'split')
        self.assertIn('jobs', result['excluded'])

    def test_all_simulated_is_analysis_only(self):
        payload = self.ballot()
        for response in payload['responses']:
            response['status'] = 'degraded'
        result = self.call('tally', payload)
        self.assertEqual(result['status'], 'analysis_only')
        self.assertEqual(sum(result['votes'].values()), 0)

    def test_quorum_requires_two_thirds_of_original_panel(self):
        payload = self.ballot()
        payload['panel'] += ['ada', 'feynman']
        result = self.call('tally', payload)
        self.assertEqual(result['required_live'], 4)
        self.assertEqual(result['status'], 'quorum_unavailable')

    def test_abstention_counts_for_quorum_but_not_support(self):
        payload = self.ballot()
        payload['responses'][0] = self.response('jobs', 'abstain')
        result = self.call('tally', payload)
        self.assertEqual(result['live_count'], 3)
        self.assertEqual(result['total_weight'], 3.5)
        self.assertEqual(result['votes'], {'ship': 1.0, 'wait': 1.0})

    def test_invalid_stance_cannot_be_inferred_from_prose(self):
        for text in ['I strongly recommend ship.',
                     'STANCE: go | CONFIDENCE: high | DEALBREAKER: no',
                     'STANCE: ship | CONFIDENCE: certain | DEALBREAKER: no',
                     'STANCE: ship | CONFIDENCE: high | DEALBREAKER: no\n'
                     'STANCE: wait | CONFIDENCE: low | DEALBREAKER: yes']:
            with self.subTest(text=text):
                payload = self.ballot()
                payload['responses'][0]['text'] = text
                result = self.call('tally', payload)
                self.assertIn('jobs', result['excluded'])
                self.assertIsNone(result['winner'])

    def test_route_rejects_malformed_affinity_as_json_error(self):
        payload = self.route_input()
        payload['members'][0]['provider_affinity'] = {'openai': 1}
        result = self.call('route', payload, ok=False)
        self.assertIn('error', result)

    def test_tally_rejects_fewer_than_two_or_more_than_four_options(self):
        for options in [['ship'], ['a', 'b', 'c', 'd', 'e']]:
            with self.subTest(options=options):
                payload = self.ballot()
                payload['options'] = options
                result = self.call('tally', payload, ok=False)
                self.assertIn('error', result)

    def test_duplicate_execution_cannot_supply_two_votes(self):
        payload = self.ballot()
        payload['responses'][1]['execution_id'] = payload['responses'][0]['execution_id']
        result = self.call('tally', payload)
        self.assertEqual(result['status'], 'quorum_unavailable')
        self.assertEqual(result['live_count'], 1)

    def test_duplicate_member_records_rejected(self):
        payload = self.ballot()
        payload['responses'].append(copy.deepcopy(payload['responses'][0]))
        self.assertIn('error', self.call('tally', payload, ok=False))

    def test_duo_never_issues_decision_tally(self):
        payload = self.ballot()
        payload['mode'] = 'duo'
        payload['panel'] = payload['panel'][:2]
        payload['responses'] = payload['responses'][:2]
        result = self.call('tally', payload)
        self.assertEqual(result['status'], 'dialectic')
        self.assertEqual(result['votes'], {})
        self.assertIsNone(result['winner'])


if __name__ == '__main__':
    unittest.main()
