---
name: china-gov-network
description: >
  Research government official career histories, leadership teams, political personnel
  networks, cadre transfers, and relationship graphs for any jurisdiction. Use when Codex
  is asked to investigate officials' resumes, current leadership rosters, predecessor or
  successor paths, who-knows-who networks, Chinese cadre exchange networks, US/state/local
  government personnel networks, or to build SQLite, GEXF, Markdown/HTML reports, and
  per-person graph JSON files such as data/persons/YYYYMMDD-{province}-{city}-{job}-{name}.json.
---

# Government Personnel Network Investigator

Build evidence-backed government personnel intelligence: current officeholders, career
timelines, leadership teams, relationship networks, SQLite/GEXF data, reports, open gaps,
per-person graph JSON, and queue-driven investigation dispatch.

## Core Principles

- Start from repository state before web research. Avoid duplicating existing scripts,
  databases, graphs, reports, or open gaps.
- Treat official government pages and appointment notices as primary sources. Treat Baidu
  Baike and media as secondary unless corroborated.
- Attach sources, source type, and confidence to every important claim.
- Distinguish `confirmed`, `plausible`, and `unverified`. Never fill timeline gaps by inference.
- Prefer incremental maintenance: update existing artifacts when present; create new ones
  only when the task is genuinely new.
- Use the current repo utilities when available: `gov_relation.todo`, `gov_relation.slugs`,
  `gov_relation.paths`, and `scripts/inventory.py`.
- For detailed workflows, read only the relevant reference:
  - `references/investigation_stages.md`: phase/stage gates and evidence standards.
  - `references/subagent_dispatch.md`: subagent roles, prompts, and Opencode dispatch.
  - `references/person_graph_json.md`: per-person graph JSON schema.
  - `references/gexf_pattern.md`: GEXF generation pattern.
  - `references/app_architecture.md`: local backend, static frontend, GitHub Pages.
  - `references/tmp_staging.md`: `data/tmp` staging and promotion workflow.
  - `references/source_fallbacks.md`: search/source fallback playbook for Exa limits,
    Baidu 403, and government-site timeouts.

## Phase 0: Repository Preflight

Before launching research agents, inspect local state:

1. Read `report/open_gaps.md` if present.
2. Run or inspect `python3 run_todo_loop.py --status` when the task maps to `data/TODO.json`.
3. Use `python3 generate_build_template.py <task_id>` when a task id is known.
4. Run `python3 scripts/inventory.py` for artifact coverage when useful.
5. Check for existing:
   - `build_<slug>_data.py`
   - `data/database/<slug>_network.db`
   - `data/graph/<slug>_network.gexf`
   - `report/YYYYMMDD-...md`
   - `data/persons/YYYYMMDD-{province}-{city}-{job}-{name}.json`
6. For new artifacts, stage them under `data/tmp/<task_id>/` and promote only with
   `scripts/process_tmp.py` after validation.

Classify the job:

| Job type | Default action |
| --- | --- |
| New region/person | Full research + new artifacts |
| Existing region with gaps | Read existing artifacts, target missing fields |
| Data repair | Fix script/schema/output only, do not relitigate all research |
| Report/index update | Reuse existing DB/GEXF/person JSON |
| Single-person profile | Produce person JSON first, then optional network artifacts |

## Phase 1: Right-Sized Research

For complex or queue-driven investigations, read `references/investigation_stages.md`
and `references/subagent_dispatch.md`.

Scale research to task size:

| Scope | Suggested agents/search tracks |
| --- | --- |
| Single official | 1-2 tracks: full resume, public record/media corroboration |
| County/district leadership | 3-5 tracks: current roster, top 2 leaders, key deputies, predecessors, exchanges |
| Province/cross-region network | 5 tracks + targeted deep dives |
| Repair/update | No broad agents unless source freshness is uncertain |

For subagents, use cost-efficient models when available. Ask each track to return:

- specific answer to assigned question
- structured people/org/position/relationship facts
- dates and source URLs
- source type: `official`, `appointment_notice`, `media`, `encyclopedia`, `database`, `inferred`
- confidence: `confirmed`, `plausible`, `unverified`
- gaps and suggested follow-up queries

Chinese search priorities:

1. official leadership pages: `领导之窗`, `领导分工`, `ldzc.shtml`
2. organization department appointment notices: `任前公示`, `干部任免`
3. government meeting/news pages
4. mainstream media such as The Paper
5. encyclopedia pages only as secondary leads

When Exa is rate-limited, Baidu returns 403/captcha, or government sites time out, read
`references/source_fallbacks.md`. Do not repeatedly hammer failing source families. After
two failures per source family, switch to alternate official URL patterns, local artifacts,
Jina Reader/cache-style fetches, general web queries, and partial-evidence artifact mode.

US/non-Chinese priorities:

1. official `.gov` biographies and directories
2. legislative/executive records
3. Ballotpedia, campaign finance databases, reputable newspapers
4. LinkedIn only for staff-level career hints, with lower confidence

## Phase 2: Quality Gate and Deep Dive

Before building artifacts, audit research outputs:

| Check | Required action if weak |
| --- | --- |
| Correct person/office/current roster? | rerun with explicit names and current/现任 terms |
| Dates and offices sourced? | search appointment notices and official pages |
| Key top-leader timeline complete? | deep dive on missing periods |
| Relationships supported by overlapping org/time? | downgrade to plausible/unverified or remove |
| Existing open gaps addressed? | update `report/open_gaps.md` after resolution |

Deep dive only on high-value gaps:

- missing early career of top leaders
- predecessor/successor movement
- shared organizations and overlapping tenures
- mentor/protege or same-system evidence
- cross-county/province exchange patterns
- public achievements, governance style, controversies, disciplinary signals

## Phase 3: Structured Data Artifacts

For backend/frontend integration, read `references/app_architecture.md`.

### SQLite and GEXF

Create or update `build_<slug>_data.py`. Keep research data as explicit Python dict/list
records near the top, but reuse repo utilities where practical. Output:

- `data/database/<slug>_network.db`
- `data/graph/<slug>_network.gexf`

For new queue-driven work, write these files first to `data/tmp/<task_id>/`, then run
`python3 scripts/process_tmp.py data/tmp/<task_id>` as a dry run and promote with `--apply`
only after validation. Read `references/tmp_staging.md` for the staging contract.

SQLite tables:

```sql
persons(id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
organizations(id, name, type, level, parent, location)
positions(id, person_id, org_id, title, start, "end", rank, note)
relationships(id, person_a, person_b, type, context, overlap_org, overlap_period)
```

For GEXF generation, read `references/gexf_pattern.md` when writing or repairing graph output.
Use string formatting rather than ElementTree for `viz` namespace safety.

### Per-Person Graph JSON

For each core figure, write:

```text
data/persons/YYYYMMDD-{province}-{city}-{job}-{name}.json
```

Examples:

- `data/persons/20260715-江西省-鹰潭市-区长-张三.json`
- `data/persons/20260715-广东省-省长-王某.json`

Read `references/person_graph_json.md` before creating this file. The person JSON is the
canonical deep profile for a person and should include resume table, relationship evidence,
governance record, professional specialization, personality/work-style indicators, sources,
confidence, and open questions.

## Phase 4: Reports and Pages

Markdown report path:

```text
report/YYYYMMDD-[地区]-[主题].md
```

Recommended report sections:

1. investigation scope and evidence standard
2. current leadership roster
3. top figures' career paths
4. predecessor/successor movements
5. confirmed relationship network
6. plausible/unverified leads
7. cross-region cadre exchange
8. governance style, achievements, professional background
9. data artifacts
10. source list and open gaps

HTML briefing is optional unless requested. If a frontend-design skill is available, use it.
If unavailable, create a concise single-file HTML or skip HTML without blocking SQLite/GEXF/person JSON.

For `report/graph.html`, deduplicate people before adding nodes:

- primary: name + birth year/month
- secondary: name + birthplace + career overlap
- tertiary: same source URL or official profile

## Phase 5: Validation and Closeout

Run relevant checks:

- `python3 -m py_compile build_<slug>_data.py`
- `python3 build_<slug>_data.py`
- inspect that `.db` and `.gexf` exist
- `python3 scripts/inventory.py`
- validate person JSON with `python3 -m json.tool <file>`

Update `report/open_gaps.md` after every investigation:

- add unresolved gaps with priority
- move resolved gaps to a resolved section with date and source
- keep old unresolved entries for at least 6 months

Final response to user:

1. top findings
2. files created/updated
3. validation run
4. remaining gaps and suggested next deep dive

## File Organization

```text
build_<slug>_data.py                         # data builder
data/tmp/<task_id>/                          # temporary staged outputs before promotion
data/database/<slug>_network.db              # SQLite output
data/graph/<slug>_network.gexf               # GEXF output
data/persons/YYYYMMDD-{province}-{city}-{job}-{name}.json
report/YYYYMMDD-[地区]-[主题].md
report/YYYYMMDD-[地区]-[主题].html            # optional
report/open_gaps.md
report/graph.html
```
