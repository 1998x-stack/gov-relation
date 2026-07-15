# Subagent Dispatch Reference

Use this when spawning subagents or generating Opencode/iagent prompts from `data/TODO.json`.

## OpenCode Agent and Models

OpenCode separates execution agent and model:

- `--agent`: permission/persona, default `build`.
- `--model`: provider/model string, e.g. `agent-loop/standard` or `iagent/standard`.

Use the strongest available model for synthesis and artifact generation:

- `iagent/standard`: default for all queue workers; high-detail research, source comparison, difficult biographies.
- `agent-loop/standard`: optional lower-cost fallback for routine roster collection.

Default to `iagent/standard` for this project unless the user explicitly requests a lower-cost fallback.

## Role Matrix

| Role | Model intent | Suggested OpenCode model | Input | Output |
| --- | --- | --- | --- |
| intake | iagent | iagent/standard | task id + repo paths | existing artifact summary |
| roster | iagent | iagent/standard | region + targets | current roster with official URLs |
| biography | iagent | iagent/standard | core person names | full career timeline |
| predecessor | iagent | iagent/standard | office + region | predecessor/successor movement |
| network | iagent | iagent/standard | people + timeline | relationship edge candidates |
| governance | iagent | iagent/standard | person + public reports | achievements, domains, style evidence |
| verifier | iagent | iagent/standard | all findings | conflicts, missing dates, confidence downgrades |
| builder | iagent | iagent/standard | verified facts | DB/GEXF/person JSON/report updates |

## Prompt Contract

Every subagent prompt should include:

- task id, province, city/region, level, target roles
- specific role assignment
- output schema required
- source requirements
- explicit instruction to mark unknowns as unknown
- repository artifacts to read first, when applicable

Return format:

```markdown
## Findings
| Claim | Date/Period | Source | Source Type | Confidence |

## People
...

## Organizations
...

## Relationships
...

## Gaps
...

## Suggested Follow-Up Queries
...
```

## Queue Dispatch Pattern

Use `data/TODO.json` as the source of truth.

Recommended loop:

1. `python3 run_todo_loop.py` to get next item.
2. `python3 scripts/todo_queue.py claim --worker-id worker-1 --model-intent iagent --opencode-agent build --opencode-model iagent/standard`
3. Run Opencode with the generated prompt file.
4. Validate and promote staged artifacts with `scripts/process_tmp.py`.
5. Mark done with `python3 scripts/todo_queue.py done --task-id <task_id> --worker-id <worker-id>` only after DB/GEXF/person JSON/report exist and validation passes.

Never mark done before validation. Failed or blocked work should use `todo_queue.py fail` or `todo_queue.py release`, not manual edits to `TODO.json`.

## Four-Worker Pattern

Start four independent OpenCode sessions. In each session, claim one task:

```bash
python3 scripts/todo_queue.py claim --worker-id worker-1 --model-intent iagent --opencode-agent build --opencode-model iagent/standard
python3 scripts/todo_queue.py claim --worker-id worker-2 --model-intent iagent --opencode-agent build --opencode-model iagent/standard
python3 scripts/todo_queue.py claim --worker-id worker-3 --model-intent iagent --opencode-agent build --opencode-model iagent/standard
python3 scripts/todo_queue.py claim --worker-id worker-4 --model-intent iagent --opencode-agent build --opencode-model iagent/standard
```

Each worker reads its generated prompt under `logs/dispatch/`, completes the task, promotes
from `data/tmp/<task_id>/`, and then marks done.

Queue state lives in `data/dispatch_state.json`; concurrent claims are protected by
`data/dispatch_state.lock/`.

## Opencode Prompt Template

```text
Use the china-gov-network skill at .agents/skills/china-gov-network.

Task:
- task_id: {task_id}
- province: {province}
- parent_city: {parent_city}
- region: {region}
- level: {level}
- targets: {targets}

Model intent: {model}

Required workflow:
1. Phase 0 repository preflight.
2. Read relevant references:
   - investigation_stages.md
   - subagent_dispatch.md
   - person_graph_json.md
   - gexf_pattern.md when writing graph output
3. Complete research with source URLs and confidence labels.
4. Create/update build script, SQLite, GEXF, report, open gaps.
5. Create data/persons/YYYYMMDD-{province}-{city}-{job}-{name}.json for each core figure.
6. Run validation and report files changed.
```

## Batching Policy

- Default: one TODO item per Opencode run.
- Use batches only for homogeneous low-risk subtasks under the same city.
- Stop a batch on the first failed validation.
- Persist logs under `logs/dispatch/`.
