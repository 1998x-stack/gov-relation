# Source Fallback Playbook

Use this when web search is degraded: Exa rate limits, Baidu 403/captcha, government-site
timeouts, or intermittent transport errors.

## Operating Rules

- Prefer local repository artifacts before external search.
- Do not retry the same failing source family more than twice in one task.
- Do not block artifact creation on missing perfect biographies. Preserve uncertainty in
  `confidence`, `open_questions`, and report gaps.
- Treat Baidu Baike/search as secondary leads only. Never depend on Baidu as the sole source.
- If search tools are rate-limited, use direct URL probes and existing repo patterns.

## Local-First Checks

Before any web call, inspect:

```bash
python3 scripts/inventory.py
ls build_*{region}* data/database/*{region}* data/graph/*{region}* report/*{region}* 2>/dev/null
python3 - <<'PY'
import sqlite3, glob
for db in glob.glob('data/database/*network.db'):
    pass
PY
```

Also search existing reports and build scripts for the county/city and target names:

```bash
rg -n "{region}|{parent_city}|{possible_name}" build_*.py report data/persons docs/assets/data
```

## Government Site Fallbacks

Try URL families in this order, stopping after useful evidence appears:

1. Official host root and common leadership paths:
   - `https://www.{pinyin}.gov.cn/`
   - `https://www.{pinyin}.gov.cn/{short}/ldzc/`
   - `https://www.{pinyin}.gov.cn/{short}/ldzc/ldzc.shtml`
   - `https://www.{pinyin}.gov.cn/{short}/zfxxgk/`
2. HTTP fallback when HTTPS times out:
   - `http://www.{pinyin}.gov.cn/...`
3. Article/search patterns:
   - `site:{host} 领导 分工`
   - `site:{host} 区委书记 OR 县委书记 OR 市委书记`
   - `site:{host} 区长 OR 县长 OR 市长`
4. Parent-city and organization-department sites:
   - `{parent_city} 组织部 任前公示 {region}`
   - `{parent_city} 人大 任命 {region} 区长`

For timed-out pages, try text extraction mirrors:

```text
https://r.jina.ai/http://r.jina.ai/http://{url}
https://r.jina.ai/http://{url}
https://r.jina.ai/http://https://{host}/...
```

## Search Engine Fallbacks

If Exa returns rate-limit errors, stop using Exa for that task. Use:

- direct `WebFetch` to official pages and likely article URLs
- Google/Bing result pages only as a last-resort lead source
- `r.jina.ai/http://r.jina.ai/http://www.google.com/search?q=...` when direct result pages are blocked
- local repo `rg` against previous province/city build scripts

Recommended query set:

```text
{region} 现任 {target_role}
{region} 领导之窗 {target_role}
{region} 领导分工 {target_role}
{name} 简历 {region}
{name} 任前公示
{name} {parent_city} 组织部
{region} 人大 任命 区长 县长 市长
```

## Artifact Mode Under Partial Evidence

When only partial evidence is available:

- Create the build script, SQLite DB, GEXF, report, and person JSON anyway.
- Label claims as `confirmed`, `plausible`, or `unverified`.
- Use `source_type: "official"` only for official pages/notices.
- Put unresolved biographical fields in `open_questions`.
- Add a high-priority gap to `report/open_gaps.md`.
- Do not invent dates, education, birthplace, party dates, or work-start dates.

This mode is preferable to failing with no artifacts. The quality gate can still pass if
canonical artifacts exist and uncertainty is explicit.
