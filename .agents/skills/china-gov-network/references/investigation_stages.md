# Investigation Stages Reference

Use this when a task needs detailed investigation, multiple agents, or queue-driven work.

## Stage Map

| Stage | Goal | Output | Gate |
| --- | --- | --- | --- |
| S0 Intake | Map user request to TODO/task/artifacts | task id, region, targets, existing files | no duplicate work |
| S1 Current Facts | Verify current officeholders and roster | current leaders + official URLs | current as of date |
| S2 Career Timelines | Build full resumes for core figures | dated career rows | no unsourced promotions |
| S3 Network Edges | Identify relationship evidence | edge candidates with strength/confidence | overlap proof or downgrade |
| S4 Governance Profile | Extract achievements, specialties, style | governance/professional/personality fields | public evidence only |
| S5 Data Build | Create/update DB, GEXF, person JSON | generated artifacts | validation passes |
| S6 Report & Gaps | Write report and open gaps | report + updated gaps | gaps explicit |
| S7 Publish | Refresh app data and pages | docs data, index, graph | static assets valid |

## Evidence Standards

Use these confidence levels consistently:

- `confirmed`: official source, appointment notice, or two independent reliable sources.
- `plausible`: credible media/encyclopedia with partial corroboration.
- `unverified`: lead without enough evidence; keep out of strong graph edges.

Use these source types:

- `official`
- `appointment_notice`
- `media`
- `encyclopedia`
- `database`
- `inferred`

## Detailed Research Angles

For a county/district standard task, cover:

1. current top two leaders
2. full leadership roster
3. predecessor and successor path
4. key deputies: 常务副职, 组织, 纪委, 政法, 宣传
5. cross-region rotations
6. same organization and same-period overlaps
7. governance domains: industry, urban construction, rural revitalization, public security, discipline, education, health, environment
8. professional background: finance, law, engineering, party school, development zone, SOE, discipline, organization system
9. work-style indicators from speeches, meeting reports, campaign language, inspection feedback
10. risk signals: disciplinary inspection, audit, negative media, unusual removals

## Quality Gates

Before artifact generation:

- Every current role has an as-of date.
- Every core figure has at least one source-backed identity record.
- Timeline gaps are explicit, not silently skipped.
- Strong edges have overlap organization and overlap period.
- Weak/personality/style conclusions cite public evidence and include caveats.
- Person JSON exists for each core figure requested by the task.

## Open Gaps Policy

Read `report/open_gaps.md` at the start. At closeout:

- Add unresolved gaps with priority.
- Move resolved gaps to a resolved section with date and source.
- Keep old unresolved entries for at least 6 months.

