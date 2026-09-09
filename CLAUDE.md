# Council of High Intelligence

## Architecture

- `SKILL.md`, `SKILL.codex.md`, `SKILL.gemini.md` — host adapters and catalog discovery
- `protocol/core.md` — shared execution sequence, modes, quorum and verdict contract
- `protocol/runtime.md` — route/tally JSON interfaces and provider dispatch contract
- `protocol/panels.md` — shared full catalog, including profile triads and duo mappings
- `agents/council-*.md` — 22 member personas with YAML frontmatter
- `install.sh` — installs to `~/.claude/` and optionally `~/.codex/skills/council/`
- `configs/` — provider/model routing templates
- `demos/` — example prompts and scoring rubric
- `scripts/` — provider detection, deterministic route/tally helpers and validation checklist
- `tests/` — offline runtime, detection and isolated installation scenarios

## Conventions

### Agent files
- Section order: Identity → Grounding Protocol → Analytical Method → What You See → What You Miss → When Deliberating → Output Format (Council Round 2) → Output Format (Standalone)
- Grounding Protocol appears **immediately after Identity** (LLMs weight earlier instructions more heavily)
- "What You See" and "What You Miss" sections: ≤3 sentences each
- Every agent gets a Council Round 2 output format with structured headers (Disagree, Strengthened by, Position Update, Evidence Label)
- New agents must be wired into the shared catalog (`protocol/panels.md`), all three platform catalogs and both READMEs (`README.md`, `README.zh-CN.md`)

### Shared protocol
- Coordinator instructions live once in `protocol/core.md`, as an **execution sequence** with numbered STEPs and `[CHECKPOINT]`/`[VERIFY]` markers
- Three modes: full (3-round), quick (2-round), duo (dialectic)
- Reference tables (triads, profiles, polarity pairs) live in `protocol/panels.md`, separate from execution

### Testing
- Always run `./scripts/council-simulation-checklist.sh` after changes
- Always run `./install.sh --dry-run` to verify installation
- When changing Codex installation, also run `./install.sh --dry-run --codex`
- Test at least one mode (full/quick/duo) after protocol changes

### Style
- Keep agent prompts tight — no filler sentences
- Grounding protocols use specific constraints ("maximum 2 analogies", "3-level depth limit"), not vague guidance
- Each agent's Council Round 2 "Disagree" prompt is tailored to their epistemic lens
