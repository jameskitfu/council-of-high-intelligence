# Shared Council Execution Protocol

This is the single execution protocol for Claude, Codex and Gemini. Read it in full before dispatch. The platform SKILL supplies only the host adapter and catalog. Resolve all relative paths from the directory containing that SKILL (`skill_root`), including custom installation roots. Read [runtime.md](runtime.md) before using the helper commands.

The host orchestrates model calls; the Python helpers perform routing and vote arithmetic. Never replace a failed helper call with an invented result. Correct invalid input within the request's scope; if execution is unavailable, provide labeled multi-perspective analysis without claiming a verified route or council consensus.

## STEP 0: Parse Mode and Lock Panel

1. `--quick` selects two rounds; `--duo` selects three rounds with exactly two members; default full mode uses three rounds. Reject conflicting mode flags.
2. Select the panel: `--full` means all 22; `--members` means 2–12 unique valid IDs; `--triad` resolves from the catalog (including the selected profile's triads); a profile alone means its panel. Without a panel flag, choose the best matching triad. Reject incompatible selectors instead of silently discarding one. In duo mode choose a catalog polarity pair if no explicit selection was supplied; any resulting panel must have exactly two members.
3. Use [panels.md](panels.md) as the complete shared catalog, including profile-specific triads and duo keyword mappings. The client tables are a discovery aid.
4. Lock the original panel before analysis. Designate at most one unambiguously on-domain member with weight **1.5×**; all others carry **1.0×**. An ambiguous match means no domain-weight seat. Do not change this after seeing positions or failures. In a weighted triad, the two ordinary seats alone cannot clear the threshold; disclose this property rather than calling the weight a neutral tie-breaker.

`[CHECKPOINT]` State mode, panel and domain-weight seat. Preserve the user's existing authorization: discovering a CLI, model, credential or config is not permission for additional costs, data sharing, installations or writes.

## STEP 1: Detect Capabilities and Route

1. Read the host adapter. Record host, actual native dispatch/continuation tools, concurrency limit and default model. Resolve tool names and arguments from the current runtime schema; do not pass Claude model aliases to another host. If native subagents are unavailable, mark the native provider unavailable even if detection calls it a candidate.
2. Run `bash {skill_root}/scripts/detect-providers.sh --host {host}`. Parse JSON. `available` means a dispatch **candidate**, not verified login or inference. `installed`, `authenticated`, `inference_ready` and `probe_status` are separate. Probe only versions/local model inventory; authentication and inference remain unknown until an authorized call supplies evidence.
3. Filter candidates against the actual tools and the user's allowed providers. `--no-auto-route` restricts candidates to the current host and uses its actual default model. `--models [path]` preserves explicit seat/provider/model choices from the supplied YAML; validate names and resolve supported `exec_method` values. Reject an unavailable or unsupported explicit mapping with its reason before dispatch; do not silently reroute it. A manual mapping and `--no-auto-route` conflict. Unknown custom endpoints require explicit `base_url` and `api_key_env` plus existing authorization.
4. Serialize selected member IDs, `polarity_pairs`, `provider_affinity`, filtered detection entries, and any fixed manual provider assignments as route JSON. Run `python3 {skill_root}/scripts/council_runtime.py route --input {route_input}`. Use its assignments. This helper first seeks polarity separation, then uses provider spread and affinity as **soft** preferences. Manual assignments remain fixed. When separation is impossible it returns `relaxed` plus collocated pairs; a bounded search ending early returns `search_limit`, never a proof of impossibility. With no candidates it returns `analysis_only`.
5. Choose models only after assigning providers: preserve explicit choices; for native seats use the actual host model unless a valid override is authorized; for external seats consult installed `configs/auto-route-defaults.yaml` and detection suggestions. Model IDs are suggestions, not proof of availability. Record actual provider **and model family**; a Cursor GPT seat and a native OpenAI seat may share a family despite distinct provider IDs. Report such overlaps and any separation lost after fallback; do not count provider IDs as proof of independent reasoning.
6. For `openai_compatible_api`, resolve endpoint and credential **environment variable name** from the config/detection entry. Keep secret values inside the dispatch process, out of prompts, files, routing JSON and transcripts.

`[CHECKPOINT]` Show member → provider → model → exec_method, candidate readiness, `relaxed`/`search_limit` reasons and exact collocated pairs. `--dry-route` stops here in **every mode**, even with a single provider or manual mapping. It starts no member, Chairman, restatement or inference call.

## STEP 1.5: Restatement Gate and Seat State

Before full-mode analysis, each member returns its own one-sentence restatement and one alternative framing (50 words total). Quick and duo combine these with their opening round. Keep restatements private until all first-round analyses are complete so the initial pass remains blind. Flag meaningful framing divergence in the verdict; ask only for indispensable missing information.

Create one isolated context per member. Supply the problem, persona and allowed evidence, without the coordinator's prior conclusions, sibling identities or routing table. Use the host's exposed fresh-context option, not a hardcoded parameter. Preserve a seat's own context between rounds; if concurrency requires releasing it, resume from its **own** transcript plus the peer material allowed for that round. Schedule bounded batches within actual capacity; lack of 22 simultaneous slots does not make 22 seats fail.

States and provenance:

- `live`: an actual member invocation returned a usable response. A successful fresh invocation on the authorized host fallback can be live; it must have its own execution record.
- `degraded`: the coordinator supplied `[Simulated]` text. Useful as supplementary analysis, never as an independent vote.
- `offline`: no usable response. Exclude from support, retain in the original panel denominator.
- Track member, round, attempt, actual provider/model, tool/request identity, status and reason. Use a real tool/request identity plus the seat/round call record as `execution_id`; do not fabricate multiple IDs for one combined multi-persona response.

Timeouts: native calls 90 seconds per attempt, external CLI 60 seconds (Cursor 90), HTTP 90, Ollama 120. These are **per-seat attempt deadlines**, not a shorter overlapping round cutoff. Polling/wait limits are observation windows, not failures. Respect host tool limits and give progress updates while waiting.

At most **3 total attempts per seat per round**, including spawn, continuation, malformed-output repair and provider fallback together. Backoff between completed failed attempts is 2 then 5 seconds. Do not create concurrent duplicate attempts: stop/confirm the old attempt ended before retrying; ignore late output from superseded attempts. An external failure uses the next remaining attempt on the **current host** if authorized native dispatch exists, with an isolated copy of that seat's persona and permitted context. Mark the failed provider unavailable for later attempts in this session. Otherwise use labeled simulation or offline; do not assume Anthropic exists. Preserve successful live seats even when too few remain for quorum.

## STEP 1.7: Select the Chairman

Select before Round 1 in every mode: explicit `--chairman`, then a configured `chairman` override, then an available capable model, preferring a family absent from the panel. Treat unknown or ambiguous overrides as invalid rather than guessing. Use only currently supported model settings; across providers there is no assumed global ranking. Break an otherwise equal choice in stable detection order. With one host, use its supported default/high tier and disclose overlap.

If no authorized dispatch capability exists, record `Chairman: unavailable — coordinator synthesis` and make no attempt; do not label an unattempted call as failed. This branch is required for `analysis_only` sessions.

The Chairman is a **separate invocation/context**, never an existing deliberating seat. The model may overlap if necessary; disclose it. It audits the full transcript only after final positions. If its single attempt fails, the coordinator can synthesize with `Chairman: failed — coordinator fallback`; this never changes the computed tally or quorum.

## STEP 2: Round 1 — Independent Analysis

Run members independently with their own complete persona, the problem, permitted evidence and the relevant word limit. Do not circulate other members' restatements or analyses yet.

| Mode | Round 1 | Round 2 | Round 3 |
|------|---------|---------|---------|
| full | Standalone analysis, ≤400 words | Cross-examination, ≤300 words | Final position, ≤100 words |
| quick | Restate + analysis, ≤200 words | Final position, ≤75 words | None |
| duo | Restate + opening, ≤300 words | Direct response, ≤200 words | Final statement, ≤50 words |

`[CHECKPOINT]` Collect actual outputs and provenance; apply the same attempt budget to missing or unusable responses.

## STEP 3: Round 2 — ANONYMIZED Review

For full and quick, create a private stable mapping `Member A`, `Member B`, etc. Replace name headers and self-attribution with these labels; do not include the mapping or panel list in peer prompts. Keep both anonymized and original transcripts. Persona output placeholders `{member name}` mean the anonymous label in this round. Duo is exempt.

Include the following **Anti-conformity directive** in Round 2 of all modes:

> If your Round 1 position was correct, defend it. Do not update merely because peers disagree, because consensus is forming, or because a position is repeated by multiple members. Update only when presented with sound reasoning that exposes a specific flaw in your earlier argument. Name that flaw when you update; if you cannot name it, do not claim an evidence-based update.

Full: use each persona's Council Round 2 format (`Disagree`, `Strengthened by`, `Position Update`, `Evidence Label`) and engage at least two peers if available. With only two seats, engage the one peer. Preserve the existing sequence: panels ≤4 review sequentially using earlier anonymized Round 2 responses; larger panels review Round 1 in parallel/batches. Quick: issue final positions from anonymized Round 1 outputs. Duo: each responds directly to the counterpart in parallel. Keep simulated peer material explicitly labeled as such.

## STEP 4: Full-Mode Enforcement

Perform one bounded pass after full Round 2. Check dissent coverage (two non-overlapping objections), novelty (new claim/test/risk/reframing), evidence labels (`empirical`, `mechanistic`, `strategic`, `ethical`, `heuristic`) and >70% agreement. Request missing coverage or ask two suitable members to examine the strongest alternative when agreement is high. An assigned counterfactual is labeled as an exercise, not silently counted as a member's final stance. This scan cannot invent votes.

Use at most one supplemental request per member, combining applicable checks; its failures use only the remaining Round 2 attempt budget. Cap Socratic recursion at a 50-word position after an answered question is re-asked, and cut exchanges beyond two messages per pair. No additional deliberation round.

## STEP 5: Final Positions and Structured Stance

Restore names for full/duo Round 3. Quick ends at Round 2. Before the final round, lock 2–4 canonical option IDs (`ship`, `wait`, etc.) with neutral definitions derived from the problem and earlier proposals; supply **the same** options to every seat. Include materially distinct live options, do not merge opposing positions to manufacture agreement. `abstain` is reserved for backing none.

In full/quick require this final nonempty line, exactly once:

```text
STANCE: <option_id or abstain> | CONFIDENCE: high|med|low | DEALBREAKER: yes|no
```

Do not infer a missing stance from prose or translate labels after voting. Repair invalid output only within the seat's remaining attempt budget. If exhausted, keep the raw output but exclude it as invalid. Duo has no stance requirement and no decision vote.

## STEP 6: Mechanical Tally and Quorum

Run `python3 {skill_root}/scripts/council_runtime.py tally --input {tally_input}` on the locked original panel, domain-weight seat, canonical options and observed final responses. Use JSON serialization, not string interpolation. The helper enforces:

1. Only valid `live` responses from distinct execution records count. Simulated, offline, missing, duplicate-execution and malformed responses contribute **zero** support. Duplicate member records are input errors: resolve which attempt is authoritative from logs, never sum attempts.
2. Minimum valid live responses: `max(2, ceil(2 × original_panel_size / 3))`. Valid abstentions count for quorum, not option support. Never shrink the panel to manufacture quorum.
3. The total weight remains the **original** panel weight, including abstainers and failed/simulated seats. Consensus requires quorum **and** an option with at least `2/3 × original_total_weight`. Integer arithmetic handles exact boundaries. Keep the original 1.5×/1× weights.
4. `consensus` has a winning option; `split` has quorum but no winner; `quorum_unavailable` has insufficient live responses; `analysis_only` has none. Duo with both real responses is `dialectic`, with no Vote Tally or decision winner. No status licenses another round.
5. Preserve `DEALBREAKER: yes` minority positions. Shared model/family use is disclosed even when separate real invocations legitimately count as separate seats; vote percentages are not probabilities of correctness.

`[VERIFY]` Save the raw input and result with the session evidence when local artifacts are authorized. Do not upgrade `split`, `quorum_unavailable` or `analysis_only` into a council verdict by fluent synthesis. Fully simulated output is titled **Multi-perspective analysis — simulated**, not independent council consensus.

## STEP 7: Chairman Synthesis and Output

Send the Chairman the problem, original panel/weights, actual routing/fallback records, all rounds (Round 2 with names restored), options and the **unaltered computed tally**. It can explain tradeoffs, dissent and uncertainty but cannot change support, quorum, weights or result status. If it contradicts the computed result, the coordinator corrects those mechanical fields explicitly and annotates the correction; it must not pass through a false consensus.

Full verdict fields, in order:

1. Problem; Council Composition; Chairman; Provider Routing (include actual family overlaps and readiness).
2. Acceptable Compromises; Kill Criteria (`If X by date, invalidated → Y`); Concrete Next Step (one named action with owner/date).
3. Unresolved Questions; Recommended Next Steps.
4. Result Status; Consensus & Agreement; Vote Tally (option → weight, original denominator, threshold, required/valid live seats, exclusions, marked domain seat).
5. Key Insights by Member; Points of Disagreement; Minority Report; Epistemic Diversity Scorecard (reasoning labels, not a numerical accuracy claim).
6. Follow-Up: what outcome to check, when, and what evidence changes the decision. Do not schedule an automation unless the user requests one.

Quick retains Problem, Panel, Chairman, Result Status, Recommended Action (conditional if no consensus), Kill Criteria, Concrete Next Step, Positions, Vote Tally, Key Disagreement and Follow-Up; compromises optional. Duo retains Problem, Chairman, Result Status, each position, agreement, core tension, implications, one Concrete Next Step and Follow-Up; kill criteria encouraged. Duo and fully simulated reports present analysis without a winning council decision.

Append one **Session Metadata** JSON block with `schema_version: 2`, host, mode, panel_size, rounds_run, tools_used, planned/actual provider_count and model families, fallbacks_triggered, live/degraded/offline counts, route status/conflicts, tally status, Chairman outcome, and best-effort token/duration estimates (`null` if unavailable). No credentials or fabricated token counts.

`[VERIFY]` Check the final report against the helper result and raw tool provenance before delivery. Successful local validation does not authorize installation, external writes, publication or fees.
