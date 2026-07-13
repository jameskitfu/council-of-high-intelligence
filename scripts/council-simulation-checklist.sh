#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_DIR}"

echo "== Council Simulation Checklist =="

pass() { echo "[PASS] $1"; }
fail() { echo "[FAIL] $1"; exit 1; }
warn() { echo "[WARN] $1"; }

# --- File existence checks ---

[[ -f "SKILL.md" ]] || fail "SKILL.md is missing"
pass "SKILL.md exists"
[[ -f "SKILL.codex.md" ]] || fail "SKILL.codex.md is missing"
pass "SKILL.codex.md exists"

if compgen -G "agents/council-*.md" >/dev/null; then
  agent_count=$(python3 -c "import glob; print(len(glob.glob('agents/council-*.md')))" 2>/dev/null || echo "unknown")
  pass "Agent definitions found (count=${agent_count})"
  [[ "${agent_count}" -eq 22 ]] || fail "Expected 22 council agents, found ${agent_count}"
  pass "Exactly 22 council agent definitions found"
else
  fail "No agent definitions found under agents/council-*.md"
fi

[[ -f "configs/provider-model-slots.example.yaml" ]] || fail "configs/provider-model-slots.example.yaml is missing"
pass "Provider/model slot template exists"

[[ -f "CLAUDE.md" ]] || warn "CLAUDE.md is missing (recommended for project conventions)"

# --- SKILL.md content checks ---

grep -q "exploration-orthogonal" SKILL.md || fail "exploration-orthogonal profile missing in SKILL.md"
pass "exploration-orthogonal profile documented in SKILL.md"

grep -q "execution-lean" SKILL.md || fail "execution-lean profile missing in SKILL.md"
pass "execution-lean profile documented in SKILL.md"

grep -q -- "--models" SKILL.md || fail "--models flag missing in SKILL.md"
pass "--models flag documented in SKILL.md"

grep -q -- "--quick" SKILL.md || fail "--quick flag missing in SKILL.md"
pass "--quick mode documented in SKILL.md"

grep -q -- "--duo" SKILL.md || fail "--duo flag missing in SKILL.md"
pass "--duo mode documented in SKILL.md"

grep -q "CHECKPOINT" SKILL.md || fail "Execution checkpoints missing in SKILL.md"
pass "Execution checkpoints present in SKILL.md"

grep -q "VERIFY" SKILL.md || fail "Verification steps missing in SKILL.md"
pass "Verification steps present in SKILL.md"

# Round 2 anonymization (issue #17) — protect against silent regression
grep -q "ANONYMIZED" SKILL.md || fail "Round 2 anonymization missing in SKILL.md (issue #17)"
grep -q "Member A" SKILL.md || fail "Member-label vocabulary missing in SKILL.md (issue #17)"
pass "Round 2 anonymization wired in SKILL.md"

grep -q "anonymiz" SKILL.codex.md || fail "Round 2 anonymization missing in SKILL.codex.md (issue #17)"
pass "Round 2 anonymization wired in SKILL.codex.md"

# Anti-conformity directive (issue #19) — must be in every Round 2 prompt
ac_count_skill=$(grep -c "Anti-conformity directive" SKILL.md || true)
if [[ "$ac_count_skill" -lt 3 ]]; then
  fail "Anti-conformity directive missing from one or more Round 2 prompts in SKILL.md (issue #19; expected ≥3 occurrences, found ${ac_count_skill})"
fi
pass "Anti-conformity directive present in all 3 Round 2 prompts in SKILL.md"

grep -q "Anti-conformity directive" SKILL.codex.md || fail "Anti-conformity directive missing in SKILL.codex.md (issue #19)"
pass "Anti-conformity directive present in SKILL.codex.md"

# Chairman role (issue #18) — must be wired into STEP 1.7, STEP 7, flags, and Codex
grep -q "STEP 1.7" SKILL.md || fail "Chairman selection step missing in SKILL.md (issue #18)"
grep -q -- "--chairman" SKILL.md || fail "--chairman flag missing in SKILL.md (issue #18)"
grep -q "CHAIRMAN" SKILL.md || fail "Chairman synthesis step missing in SKILL.md (issue #18)"
pass "Chairman role wired in SKILL.md (STEP 1.7 + --chairman flag + synthesis step)"

grep -q -i "chairman" SKILL.codex.md || fail "Chairman role missing in SKILL.codex.md (issue #18)"
pass "Chairman role wired in SKILL.codex.md"

grep -q "chairman_defaults" configs/auto-route-defaults.yaml || fail "chairman_defaults block missing in auto-route-defaults.yaml (issue #18)"
pass "Chairman defaults configured in auto-route-defaults.yaml"

# Verdict actionability sections (issue #21)
grep -q "Acceptable Compromises" SKILL.md || fail "Acceptable Compromises section missing in SKILL.md (issue #21)"
grep -q "Kill Criteria" SKILL.md || fail "Kill Criteria section missing in SKILL.md (issue #21)"
grep -q "Concrete Next Step" SKILL.md || fail "Concrete Next Step section missing in SKILL.md (issue #21)"
pass "Verdict actionability sections present in SKILL.md (Acceptable Compromises / Kill Criteria / Concrete Next Step)"

grep -q "Acceptable Compromises" SKILL.codex.md || fail "Acceptable Compromises missing in SKILL.codex.md (issue #21)"
grep -q "Kill Criteria" SKILL.codex.md || fail "Kill Criteria missing in SKILL.codex.md (issue #21)"
grep -q "Concrete Next Step" SKILL.codex.md || fail "Concrete Next Step missing in SKILL.codex.md (issue #21)"
pass "Verdict actionability sections present in SKILL.codex.md"

# OpenAI-compatible API archetype (issue #16) — must be wired in dispatch + routing
grep -q "openai_compatible_api" SKILL.md || fail "openai_compatible_api archetype missing in SKILL.md (issue #16)"
grep -q "base_url" SKILL.md || fail "base_url handling missing in SKILL.md (issue #16)"
grep -q "api_key_env" SKILL.md || fail "api_key_env handling missing in SKILL.md (issue #16)"
pass "openai_compatible_api archetype wired in SKILL.md (dispatch + base_url + api_key_env)"

grep -q "openai_compatible_api\|openai-compatible\|OpenAI-Compatible" SKILL.codex.md || fail "openai_compatible_api archetype missing in SKILL.codex.md (issue #16)"
pass "openai_compatible_api archetype wired in SKILL.codex.md"

# Session Metadata schema (issue #7 Phase 1)
grep -q "Session Metadata" SKILL.md || fail "Session Metadata block missing in SKILL.md (issue #7)"
grep -q "schema_version: 1" SKILL.md || fail "schema_version: 1 marker missing in SKILL.md Session Metadata (issue #7)"
pass "Session Metadata schema wired in SKILL.md"

grep -q "Session Metadata\|session metadata\|session_metadata" SKILL.codex.md || fail "Session Metadata missing in SKILL.codex.md (issue #7)"
pass "Session Metadata referenced in SKILL.codex.md"

# --- Exact council graph and schema validation ---

if ! python3 - <<'PY'
from pathlib import Path
import ast
import re

EXPECTED_IDS = {
    "ada", "aristotle", "aurelius", "feynman", "jobs", "kahneman",
    "karpathy", "krashen", "lao-tzu", "leonardo", "machiavelli",
    "meadows", "munger", "musashi", "rams", "rubin", "socrates",
    "sun-tzu", "sutskever", "taleb", "torvalds", "watts",
}
EXPECTED_NEW_TRIADS = {
    "creative": {"rubin", "leonardo", "rams"},
    "creator": {"rubin", "jobs", "watts"},
    "editing": {"rubin", "rams", "feynman"},
    "product-vision": {"jobs", "rams", "torvalds"},
    "launch": {"jobs", "musashi", "machiavelli"},
    "creator-product": {"jobs", "rubin", "karpathy"},
    "invention": {"leonardo", "ada", "feynman"},
    "prototype": {"leonardo", "torvalds", "karpathy"},
    "language-learning": {"krashen", "kahneman", "feynman"},
    "learn-in-public": {"krashen", "leonardo", "rubin"},
    "english-content": {"krashen", "jobs", "rams"},
}
EXPECTED_PROFILES = {
    "classic": EXPECTED_IDS,
    "exploration-orthogonal": {
        "socrates", "feynman", "sun-tzu", "machiavelli", "ada",
        "lao-tzu", "aurelius", "torvalds", "karpathy", "sutskever",
        "kahneman", "meadows",
    },
    "execution-lean": {"torvalds", "feynman", "sun-tzu", "aurelius", "ada"},
    "ai-creator-learner": {
        "karpathy", "torvalds", "feynman", "rubin", "jobs", "leonardo",
        "krashen", "rams",
    },
}
REQUIRED_HEADINGS = (
    "Identity",
    "Analytical Method",
    "What You See That Others Miss",
    "What You Tend to Miss",
    "When Deliberating in Council",
    "Output Format (Council Round 2)",
    "Output Format (Standalone)",
)

errors = []


def describe(values):
    return ", ".join(sorted(values)) or "<none>"


def compare_sets(label, actual, expected):
    if actual != expected:
        errors.append(
            f"{label}: missing [{describe(expected - actual)}]; "
            f"unexpected [{describe(actual - expected)}]"
        )


def markdown_section(text, heading):
    lines = text.splitlines()
    marker = f"## {heading}"
    try:
        start = lines.index(marker) + 1
    except ValueError:
        errors.append(f"missing section {marker!r}")
        return []
    end = next((index for index in range(start, len(lines)) if lines[index].startswith("## ")), len(lines))
    return lines[start:end]


def markdown_subsection(text, heading):
    lines = text.splitlines()
    pattern = re.compile(rf"^### `{re.escape(heading)}`(?:\s|$)")
    matches = [index for index, line in enumerate(lines) if pattern.match(line)]
    if len(matches) != 1:
        errors.append(f"expected one profile subsection for {heading!r}, found {len(matches)}")
        return []
    start = matches[0] + 1
    end = next((index for index in range(start, len(lines)) if lines[index].startswith("### ")), len(lines))
    return lines[start:end]


def table_rows(lines):
    rows = []
    for line in lines:
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(r"`[^`]+`", cells[0]):
            rows.append(cells)
    return rows


def parse_frontmatter(path):
    text = path.read_text()
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        errors.append(f"{path}: malformed YAML frontmatter delimiters")
        return text, {}

    council = {}
    in_council = False
    for line in parts[1].splitlines():
        if line == "council:":
            in_council = True
            continue
        if in_council and not line.startswith("  "):
            in_council = False
        if not in_council:
            continue
        match = re.match(r"^  ([a-z_]+):\s*(.*)$", line)
        if not match:
            continue
        key, raw_value = match.groups()
        if key in {"polarity_pairs", "triads", "profiles", "provider_affinity"}:
            try:
                value = ast.literal_eval(raw_value)
            except (SyntaxError, ValueError):
                errors.append(f"{path}: council.{key} is not a valid inline string array")
                continue
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                errors.append(f"{path}: council.{key} must be an inline string array")
                continue
            if len(value) != len(set(value)):
                errors.append(f"{path}: council.{key} contains duplicate entries")
            council[key] = value
        else:
            council[key] = raw_value
    return text, council


agent_paths = sorted(Path("agents").glob("council-*.md"))
actual_ids = {path.stem[len("council-"):] for path in agent_paths}
compare_sets("agent ID set", actual_ids, EXPECTED_IDS)

agent_metadata = {}
for path in agent_paths:
    agent_id = path.stem[len("council-"):]
    text, council = parse_frontmatter(path)
    agent_metadata[agent_id] = council

    headings = [line[3:] for line in text.splitlines() if line.startswith("## ")]
    for required in REQUIRED_HEADINGS:
        count = headings.count(required)
        if count != 1:
            errors.append(f"{path}: expected exact heading '## {required}' once, found {count}")
    grounding = [heading for heading in headings if heading == "Grounding Protocol" or heading.startswith("Grounding Protocol — ")]
    if len(grounding) != 1:
        errors.append(f"{path}: expected one exact Grounding Protocol heading, found {len(grounding)}")
    if headings.count("Identity") == 1 and len(grounding) == 1 and headings.count("Analytical Method") == 1:
        if not headings.index("Identity") < headings.index(grounding[0]) < headings.index("Analytical Method"):
            errors.append(f"{path}: Grounding Protocol must appear after Identity and before Analytical Method")

    affinity = council.get("provider_affinity")
    if not isinstance(affinity, list) or not affinity:
        errors.append(f"{path}: council.provider_affinity is missing from YAML frontmatter or empty")

skill_text = Path("SKILL.md").read_text()
skill_roster_rows = table_rows(markdown_section(skill_text, "The 22 Council Members"))
figure_to_id = {}
skill_roster = set()
for row in skill_roster_rows:
    if len(row) < 2:
        continue
    match = re.fullmatch(r"`council-([^`]+)`", row[0])
    if not match:
        continue
    agent_id = match.group(1)
    skill_roster.add(agent_id)
    figure_to_id[row[1].casefold()] = agent_id
compare_sets("SKILL.md roster", skill_roster, EXPECTED_IDS)

aliases = {agent_id.casefold(): agent_id for agent_id in EXPECTED_IDS}
aliases.update(figure_to_id)
for figure, agent_id in list(figure_to_id.items()):
    last_name = figure.split()[-1]
    if last_name not in aliases:
        aliases[last_name] = agent_id


def resolve_member(raw, label):
    token = raw.strip().strip("`")
    agent_id = aliases.get(token.casefold())
    if agent_id is None:
        errors.append(f"{label}: unknown member {token!r}")
    return agent_id


canonical_triads = {}
for row in table_rows(markdown_section(skill_text, "Pre-defined Triads")):
    if len(row) < 2:
        continue
    triad = row[0].strip("`")
    members = {
        member_id
        for member in row[1].split("+")
        if (member_id := resolve_member(member, f"SKILL.md triad {triad}")) is not None
    }
    if triad in canonical_triads:
        errors.append(f"SKILL.md triad {triad!r} is duplicated")
    canonical_triads[triad] = members

for triad, expected_members in EXPECTED_NEW_TRIADS.items():
    compare_sets(f"SKILL.md new triad {triad}", canonical_triads.get(triad, set()), expected_members)

expected_triads_by_member = {agent_id: set() for agent_id in EXPECTED_IDS}
for triad, members in canonical_triads.items():
    for member in members:
        expected_triads_by_member[member].add(triad)

expected_profiles_by_member = {agent_id: set() for agent_id in EXPECTED_IDS}
for profile, members in EXPECTED_PROFILES.items():
    for member in members:
        expected_profiles_by_member[member].add(profile)

for agent_id in sorted(EXPECTED_IDS & actual_ids):
    council = agent_metadata[agent_id]
    actual_triads = set(council.get("triads", []))
    actual_profiles = set(council.get("profiles", []))
    compare_sets(f"{agent_id} frontmatter triads", actual_triads, expected_triads_by_member[agent_id])
    compare_sets(f"{agent_id} frontmatter profiles", actual_profiles, expected_profiles_by_member[agent_id])

for agent_id in sorted(EXPECTED_IDS & actual_ids):
    pairs = agent_metadata[agent_id].get("polarity_pairs", [])
    if not isinstance(pairs, list):
        errors.append(f"{agent_id}: council.polarity_pairs is missing")
        continue
    for peer in pairs:
        if peer not in EXPECTED_IDS:
            errors.append(f"{agent_id}: polarity pair points to unknown agent {peer!r}")
        elif peer == agent_id:
            errors.append(f"{agent_id}: polarity pair cannot point to itself")
        elif agent_id not in agent_metadata.get(peer, {}).get("polarity_pairs", []):
            errors.append(f"one-way polarity pair: {agent_id} -> {peer}, but {peer} does not point to {agent_id}")


def parse_compact_roster(text, platform):
    section = markdown_section(text, "Member Roster")
    spans = [re.fullmatch(r"`([^`]+)`", line.strip()) for line in section]
    values = [match.group(1) for match in spans if match]
    if len(values) != 1:
        errors.append(f"{platform}: expected one Member Roster code span, found {len(values)}")
        return set()
    return {token.strip() for token in values[0].split(",") if token.strip()}


def parse_compact_triads(text, platform):
    triads = {}
    for row in table_rows(markdown_section(text, "Triads")):
        if len(row) < 2:
            continue
        triad = row[0].strip("`")
        members = {token.strip().strip("`") for token in row[1].split(",") if token.strip()}
        if triad in triads:
            errors.append(f"{platform}: triad {triad!r} is duplicated")
        triads[triad] = members
    return triads


def parse_skill_profiles(text):
    profiles = {}
    for profile in EXPECTED_PROFILES:
        block = markdown_subsection(text, profile)
        joined = "\n".join(block)
        if profile == "classic":
            count_match = re.search(r"\bAll (\d+) members\b", joined)
            if not count_match or int(count_match.group(1)) != len(EXPECTED_IDS):
                errors.append("SKILL.md classic profile must state All 22 members")
            profiles[profile] = EXPECTED_IDS if count_match else set()
            continue
        members_match = re.search(r"^\*\*Members\*\*:\s*(.+)$", joined, re.MULTILINE)
        if not members_match:
            errors.append(f"SKILL.md profile {profile!r} is missing its Members line")
            profiles[profile] = set()
            continue
        profiles[profile] = {
            member_id
            for member in members_match.group(1).split(",")
            if (member_id := resolve_member(member, f"SKILL.md profile {profile}")) is not None
        }
    return profiles


def parse_compact_profiles(text, platform):
    profiles = {}
    for line in markdown_section(text, "Profiles"):
        match = re.match(r"^- `([^`]+)`: (.+)$", line)
        if not match:
            continue
        profile, raw_members = match.groups()
        if raw_members == "all 22 members":
            members = EXPECTED_IDS
        else:
            members = {token.strip().strip("`") for token in raw_members.split(",") if token.strip()}
        profiles[profile] = members
    compare_sets(f"{platform} profile ID set", set(profiles), set(EXPECTED_PROFILES))
    return profiles


coordinator_texts = {
    "SKILL.md": skill_text,
    "SKILL.codex.md": Path("SKILL.codex.md").read_text(),
    "SKILL.gemini.md": Path("SKILL.gemini.md").read_text(),
}
coordinator_rosters = {
    "SKILL.md": skill_roster,
    "SKILL.codex.md": parse_compact_roster(coordinator_texts["SKILL.codex.md"], "SKILL.codex.md"),
    "SKILL.gemini.md": parse_compact_roster(coordinator_texts["SKILL.gemini.md"], "SKILL.gemini.md"),
}
for platform, roster in coordinator_rosters.items():
    compare_sets(f"{platform} roster", roster, EXPECTED_IDS)

coordinator_triads = {
    "SKILL.md": canonical_triads,
    "SKILL.codex.md": parse_compact_triads(coordinator_texts["SKILL.codex.md"], "SKILL.codex.md"),
    "SKILL.gemini.md": parse_compact_triads(coordinator_texts["SKILL.gemini.md"], "SKILL.gemini.md"),
}
for platform, triads in coordinator_triads.items():
    compare_sets(f"{platform} triad ID set", set(triads), set(canonical_triads))
    for triad, canonical_members in canonical_triads.items():
        compare_sets(f"{platform} triad {triad}", triads.get(triad, set()), canonical_members)

coordinator_profiles = {
    "SKILL.md": parse_skill_profiles(skill_text),
    "SKILL.codex.md": parse_compact_profiles(coordinator_texts["SKILL.codex.md"], "SKILL.codex.md"),
    "SKILL.gemini.md": parse_compact_profiles(coordinator_texts["SKILL.gemini.md"], "SKILL.gemini.md"),
}
for platform, profiles in coordinator_profiles.items():
    compare_sets(f"{platform} profile ID set", set(profiles), set(EXPECTED_PROFILES))
    for profile, expected_members in EXPECTED_PROFILES.items():
        compare_sets(f"{platform} profile {profile}", profiles.get(profile, set()), expected_members)

readme_count_markers = {
    "README.md": ("22 AI personas", "members-22", "## The 22 Council Members", "Installs 22 council agents"),
    "README.zh-CN.md": ("22 位 AI 人格", "members-22", "## 22 位议会成员", "安装 22 位议会成员"),
}
for readme_name, count_markers in readme_count_markers.items():
    readme = Path(readme_name).read_text()
    for marker in count_markers:
        if marker not in readme:
            errors.append(f"{readme_name}: current 22-member marker {marker!r} is missing")
    for agent_id in ("jobs", "rubin", "leonardo", "krashen"):
        if f"`council-{agent_id}`" not in readme:
            errors.append(f"{readme_name}: council-{agent_id} is missing")
    if "ai-creator-learner" not in readme:
        errors.append(f"{readme_name}: ai-creator-learner is missing")

if "22 member personas" not in Path("CLAUDE.md").read_text():
    errors.append("CLAUDE.md must state 22 member personas")

if errors:
    for error in errors:
        print(f"[FAIL] {error}")
    raise SystemExit(1)
PY
then
  fail "Exact council graph validation failed"
fi
pass "Exact 22-member council graph, schemas, coordinators, profiles, and docs validated"

# --- Verdict template dedup check ---

if grep -q "^{" demos/verdict-template.md 2>/dev/null; then
  warn "demos/verdict-template.md still contains template placeholders (should point to SKILL.md)"
fi
pass "Verdict template dedup check done"

# --- Auto-routing checks ---

[[ -f "scripts/detect-providers.sh" ]] || fail "scripts/detect-providers.sh is missing"
[[ -x "scripts/detect-providers.sh" ]] || fail "scripts/detect-providers.sh is not executable"
pass "detect-providers.sh exists and is executable"

if detect_output="$(bash scripts/detect-providers.sh 2>/dev/null)"; then
  if echo "$detect_output" | grep -q '"provider_count"'; then
    pass "detect-providers.sh produces valid JSON"
  else
    fail "detect-providers.sh output missing provider_count field"
  fi
else
  fail "detect-providers.sh exited with error"
fi

[[ -f "configs/auto-route-defaults.yaml" ]] || fail "configs/auto-route-defaults.yaml is missing"
pass "Auto-route defaults config exists"

grep -q -- "--no-auto-route" SKILL.md || fail "--no-auto-route flag missing in SKILL.md"
pass "--no-auto-route flag documented in SKILL.md"

grep -q -- "--dry-route" SKILL.md || fail "--dry-route flag missing in SKILL.md"
pass "--dry-route flag documented in SKILL.md"

# --- Install script checks ---

if command -v shellcheck >/dev/null 2>&1; then
  shellcheck install.sh
  pass "shellcheck passed for install.sh"
else
  warn "shellcheck not installed; skipped"
fi

./install.sh --dry-run >/tmp/council-install-dry-run.log
pass "install.sh --dry-run completed"

grep -q "Installed .* council agents" /tmp/council-install-dry-run.log || fail "install dry-run output missing agent install summary"
pass "install summary output present"

./install.sh --dry-run --copy-configs >/tmp/council-install-dry-run-configs.log
pass "install.sh --dry-run --copy-configs completed"

grep -q "Installed .* config files" /tmp/council-install-dry-run-configs.log || fail "copy-configs dry-run output missing config install summary"
pass "config summary output present"

./install.sh --dry-run --codex >/tmp/council-install-dry-run-codex.log
pass "install.sh --dry-run --codex completed"

grep -q "Installed Codex skill to" /tmp/council-install-dry-run-codex.log || fail "codex dry-run output missing Codex skill summary"
pass "Codex install summary output present"

echo
echo "Checklist complete."
