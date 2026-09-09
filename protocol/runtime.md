# Runtime Adapter Contract

`skill_root` is the resolved directory of the invoked SKILL, never an assumed home-directory path. Python 3.9+ is required for the installed helpers. They use only the standard library and perform no inference.

## Routing Input and Output

Serialize selected members from persona frontmatter and provider entries from detection. `manual` fixes only the specified members; automatic allocation fills the others. Model choices remain in the coordinator's routing table because the helper assigns provider IDs, not model families.

```json
{
  "members": [
    {"id": "jobs", "polarity_pairs": ["rubin", "torvalds"], "provider_affinity": ["anthropic"]},
    {"id": "rubin", "polarity_pairs": ["jobs", "torvalds"]},
    {"id": "torvalds", "polarity_pairs": ["jobs", "rubin"]}
  ],
  "providers": [
    {"name": "openai", "available": true},
    {"name": "google", "available": true}
  ],
  "manual": {},
  "max_nodes": 20000
}
```

```bash
python3 "${skill_root}/scripts/council_runtime.py" route --input route-input.json
```

Output contains `assignments`, `conflicts` (collocated pairs), `provider_counts`, `manual_members`, search `nodes`, `reason` and `status`. `satisfied` proves separation for supplied provider IDs; `relaxed` means exhaustive search proved zero conflicts impossible under the fixed constraints and returns a minimum-conflict assignment. `search_limit` returns the best complete assignment found without claiming optimality or impossibility. Provider balance and affinity are soft, not globally optimized. `analysis_only` means no candidates. Invalid input returns JSON `error` with exit code 2. Unknown graph peers outside the selected panel are ignored.

## Voting Input and Output

An `execution_id` identifies an observed independent call, not a persona label created after simulation. Different seats may use the same model but require separate calls. A replacement call uses a new identity; only its authoritative final response is included.

```json
{
  "mode": "quick",
  "panel": ["jobs", "rubin", "torvalds"],
  "domain_weight": "jobs",
  "options": ["ship", "wait"],
  "responses": [
    {"member": "jobs", "status": "degraded", "text": "[Simulated] ship"},
    {"member": "rubin", "status": "live", "execution_id": "tool-call-12/rubin/r2", "text": "STANCE: ship | CONFIDENCE: high | DEALBREAKER: no"},
    {"member": "torvalds", "status": "live", "execution_id": "tool-call-13/torvalds/r2", "text": "STANCE: ship | CONFIDENCE: med | DEALBREAKER: no"}
  ]
}
```

```bash
python3 "${skill_root}/scripts/council_runtime.py" tally --input tally-input.json
```

This example produces `split`, `ship: 2.0`, original weight `3.5`, threshold `7/3`, two valid live seats, and excluded Jobs. The simulated vote never becomes 1.5 extra support. Output also provides `accepted`, `excluded`, `required_live`, `live_count`, `minority_dealbreakers`, `status` and `winner`. Missing/malformed responses are reported in exclusions; repair them only within the shared attempt budget. For duo, use two panel members and their final texts; options may be empty and votes are always empty.

## Dispatch Boundary

Native seats use the current platform's exposed tools and schema. Fresh contexts receive the member's persona and allowed transcript; neither native nor external seats receive secret environment values. Read the whole persona for every provider so routing does not discard the analytical method or blind spots.

External invocations must use argument arrays and serialized JSON/stdin rather than expanding user text into a shell command. For example, execute with Python `subprocess.run(argv, input=prompt, text=True, timeout=...)` where stdin is supported. Do not interpolate a prompt containing quotes, backticks or `$()` into shell source. Capture exit status and stderr (redact credentials), then apply the shared fallback policy on failure or empty output. Bound calls and terminate their process groups on timeout before retrying.

| exec_method | Invocation contract |
|-------------|---------------------|
| `subagent` | Native host adapter; actual exposed tools and supported model settings |
| `claude_cli` | `claude -p --model MODEL --tools "" PROMPT`; check local help before use |
| `codex_exec` | `codex exec --sandbox read-only --model MODEL -`, prompt through stdin; check local help |
| `gemini_cli` | `gemini -m MODEL -p PROMPT` in a supported read-only/tool-disabled configuration; if unavailable, use host fallback |
| `ollama_run` | `ollama run MODEL PROMPT`; model must be in local inventory |
| `cursor_cli` | `cursor-agent -p --mode ask --model MODEL --output-format text PROMPT` |
| `openai_compatible_api` | POST serialized system/user messages to `base_url + /chat/completions`; key resolved from `api_key_env` only inside the process |

CLI examples describe argument vectors, not shell interpolation templates. Verify installed CLI help where flags differ. Do not use automatic-approval bypasses. Member deliberation does not authorize edits, installations or third-party messages; any optional read/search tools stay within the request's existing scope. If a provider cannot enforce the allowed action scope, mark it unavailable and use the authorized host path.

For HTTP, use system/user messages, `temperature: 0.7`, `max_tokens: 1200`, a 90-second attempt timeout, and require a successful HTTP status plus nonempty `.choices[0].message.content`. Record request identity when available; otherwise record the local invocation identity. An error, timeout, unsupported model or empty response consumes one attempt. A detected key or successful `/models` response is not proof that inference works. Never put the key itself in model context, argv, metadata or error output.

## Host Fallback

Fallback always means a new authorized invocation on the **current host**, using its supported model settings. In Codex that is an OpenAI/native invocation; in Gemini it is Google/native; in Claude it is Anthropic/native. If the native dispatch tool is absent, simulation is `degraded`, never `live`. The final report includes actual provider/family changes and the helper's unchanged quorum result. Model family overlap is a limitation even when native calls are independent.
