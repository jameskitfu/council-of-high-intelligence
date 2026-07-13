# Creator-Learner Council Members Design

## Goal

Expand the council from 18 to 22 members with four orthogonal lenses tailored to AI engineering, YouTube creation, and English learning:

- Rick Rubin — creative direction and artistic truth
- Steve Jobs — product taste and integrated experience
- Leonardo da Vinci — observational synthesis and visual invention
- Stephen Krashen — language acquisition and comprehensible input

Naval Ravikant remains out of scope because his leverage, wealth, and life-philosophy lenses overlap substantially with Munger, Taleb, Lao Tzu, Aurelius, and Machiavelli.

## Member boundaries

### Rick Rubin

- Domain: `Creative direction & artistic truth`
- Polarity: `Listen to what the work wants to become`
- Unique job: identify the living core of a work, remove performative or fear-driven additions, and distinguish productive refinement from avoidance.
- Must not become a generic minimalist; Rams owns user clarity and Lao Tzu owns non-intervention.
- Polarity pairs: Jobs and Torvalds.

### Steve Jobs

- Domain: `Product taste & integrated experience`
- Polarity: `Shape the whole experience around one clear promise`
- Unique job: integrate technology, story, packaging, launch, and end-to-end experience into a coherent product.
- Must not duplicate Rams's user-centered simplicity or Torvalds's maintainability lens.
- Polarity pairs: Rubin, Rams, and Torvalds.

### Leonardo da Vinci

- Domain: `Observational synthesis & visual invention`
- Polarity: `See it, sketch it, then understand it`
- Unique job: reason through direct observation, visual models, cross-domain analogy, and prototypes before formalization.
- Must not become a generic polymath; Munger owns mental-model breadth, Feynman owns first-principles explanation, and Ada owns formal abstraction.
- Polarity pairs: Aristotle and Ada.

### Stephen Krashen

- Domain: `Language acquisition & comprehensible input`
- Polarity: `Acquire through meaningful input before forcing output`
- Unique job: assess input comprehensibility, affective filters, acquisition versus explicit study, and sustainable exposure to authentic language.
- Must not provide generic study motivation or claim that output and correction never matter.
- Polarity pair: Feynman, contrasting natural acquisition with explicit explanation and testing.

## Panels and routing

The following domain triads will be added:

| Domain | Members | Purpose |
|---|---|---|
| `creative` | Rubin + Leonardo + Rams | artistic truth + invention + user clarity |
| `creator` | Rubin + Jobs + Watts | authentic work + product direction + reframing |
| `editing` | Rubin + Rams + Feynman | essence + clarity + comprehension test |
| `product-vision` | Jobs + Rams + Torvalds | integrated experience + user need + feasibility |
| `launch` | Jobs + Musashi + Machiavelli | story + timing + incentives |
| `creator-product` | Jobs + Rubin + Karpathy | packaging + authenticity + AI capability |
| `invention` | Leonardo + Ada + Feynman | observation + formalization + empirical testing |
| `prototype` | Leonardo + Torvalds + Karpathy | sketch + build + empirical iteration |
| `language-learning` | Krashen + Kahneman + Feynman | acquisition + learning bias + reality check |
| `learn-in-public` | Krashen + Leonardo + Rubin | input + visible learning + authentic expression |
| `english-content` | Krashen + Jobs + Rams | acquisition value + content promise + viewer clarity |

Add an `ai-creator-learner` profile with eight members:

`karpathy, torvalds, feynman, rubin, jobs, leonardo, krashen, rams`

The profile follows a content-production loop: comprehensible English input → observation and visual synthesis → AI understanding → working artifact → authentic story → packaging → audience clarity.

The existing `exploration-orthogonal` and `execution-lean` profiles remain unchanged. `classic` and `--full` include all 22 members. Manual selection becomes `2-12`; default auto-selection remains a three-member triad so normal usage does not become more expensive.

Each new member receives explicit `provider_affinity` metadata. The existing provider-spread and polarity-separation algorithm handles the new seats without changes to provider detection.

## Files and platform parity

Create four agent files under `agents/`, following the repository's exact section order and structured Round 2 / standalone output contracts.

Keep these surfaces synchronized:

- `SKILL.md`
- `SKILL.codex.md`
- `SKILL.gemini.md`
- `README.md`
- `README.zh-CN.md`
- `CHANGELOG.md`
- `CLAUDE.md`
- `scripts/council-simulation-checklist.sh`

The installer requires no behavioral change because it discovers `agents/council-*.md` dynamically.

## Validation design

Extend the simulation checklist before adding members so the first run fails for the missing feature. The checks will require:

- exactly 22 agent files
- all four new agent files
- consistent required sections and early Grounding Protocol placement
- frontmatter provider affinity for all 22 agents
- all four names and the `ai-creator-learner` profile in Claude, Codex, and Gemini coordinator files
- all 11 new triad identifiers in the platform coordinator files
- current member counts in both READMEs and project documentation

After implementation, run:

- `./scripts/council-simulation-checklist.sh`
- `./install.sh --dry-run`
- `./install.sh --dry-run --codex`
- `./install.sh --dry-run --gemini`
- Markdown structure and local-link validation for both READMEs
- `git diff --check`

## Out of scope

- Adding Naval Ravikant
- Changing provider detection or model defaults
- Changing deliberation round structure, weighted voting, Chairman selection, or fallback behavior
- Adding all four members to `exploration-orthogonal` or `execution-lean`
- Running all 22 members by default when no explicit panel is selected
