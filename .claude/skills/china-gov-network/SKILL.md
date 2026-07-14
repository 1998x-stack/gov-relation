---
name: china-gov-network
description: >
  Research government official career histories, leadership teams, and build personnel
  relationship networks — for ANY jurisdiction (Chinese counties, US federal/state agencies,
  city governments, etc.). Use this skill whenever the user asks about officials' resumes,
  career paths, leadership rosters, political personnel networks, government cadre
  relationships, or wants to map out who-knows-who in any government organization.
  Triggers on phrases like "调查XX的履历", "XX领导班子", "工作关系大网", "人事关系图谱",
  "干部交流网络", "investigate XX official", "government personnel network", "map
  connections between", or any request to investigate government officials' backgrounds
  and connections. Also triggers when the user wants to build a SQLite database, GEXF
  graph, or HTML briefing about government personnel. Jurisdiction-agnostic — works for
  中国官场, US Congress, state agencies, city councils, or any political entity.
---

# Government Personnel Network Investigator

Investigate government officials in ANY jurisdiction — their career histories, leadership
teams, and inter-personnel relationship networks. Works for Chinese counties, US federal/state
agencies, city governments, or any political entity. The output is a structured dataset
(SQLite + GEXF) plus a comprehensive Markdown report and an interactive HTML briefing page.

> **Model for ALL subagents**: `haiku` (cost-efficient, fast search).
> Phase 1 (5 agents) and Phase 2 (3 agents) all use this model. Phase 3 (code generation,
> report writing, HTML design) uses the session's default model.

## Workflow Overview

```
Phase 1: Broad Research      Phase 2: Deep Dive         Phase 3: Build & Deliver
┌──────────────────┐       ┌──────────────────┐       ┌─────────────────────────┐
│ 5 subagents       │  ──→  │ 3 subagents       │  ──→  │ SQLite DB + GEXF        │
│ different angles  │       │ targeted gaps     │       │ Markdown report         │
│ haiku │       │ haiku │       │ + frontend-design skill │
└──────────────────┘       └──────────────────┘       └─────────────────────────┘
```

## Phase 1: Broad Research (5 Subagents)

Deploy 5 subagents simultaneously, each from a different research angle. Use the
general-purpose agent type with `model: "haiku"` for cost efficiency.
All 5 run in parallel (`run_in_background: true`).

The 5 angles are:

| # | Angle | Search Focus | Sample Queries |
|---|-------|-------------|----------------|
| 1 | **Current Leader ID & Resume** | Who holds the target position? Full career timeline, birth info, education. | `"XXX 简历 任职经历"`, `"XXX 任前公示"`, Baidu Baike |
| 2 | **Leadership Team Roster** | All members of the 领导班子 (county committee + government), their current posts, birth years, native places. | Official government website leadership pages, `"XXX县委 领导班子"`, `"XXX县政府 领导分工"` |
| 3 | **Key Deputies' Careers** | Career histories of the 2-3 most important deputy positions (e.g., 常务副县长, 县委副书记, 组织部长). | Each deputy's Baidu Baike, `"XXX 简历 任职"`, `"XXX 此前 担任"` |
| 4 | **Predecessor & Successors** | Who held the position before? Where did they go? Recent promotions/transfers out of the county. | `"前任XXX书记"`, `"XXX 卸任 去向"`, 市委组织部任前公示 |
| 5 | **Cross-County Exchange Network** | Personnel flows between this county and neighboring counties/districts. Patterns of cadre exchange. | `"XX县 XX县 干部交流"`, `"XX市 县级干部 调任"`, cross-county transfers |

### Agent Prompt Template

For each agent, provide a detailed prompt with:
- Specific search queries to run (3-5 queries)
- What information to extract (dates, positions, locations, sources)
- The expected return format (structured text with source URLs)
- Reminder to use WebSearch for each query and WebFetch for key pages

### Phase 1 Output

Each agent returns structured findings. From these, identify:
1. **Information gaps** — key people with missing career histories
2. **Connection leads** — potential work overlaps between people
3. **Anomalies** — unusual career moves, rapid promotions, scandal traces

### ⚠ Phase 1 Quality Gate (MANDATORY)

Before proceeding to Phase 2, run this checklist against each of the 5 agent outputs.
Subagents (especially haiku) can drift — producing historical lists when you asked for
current people, or returning general trivia instead of targeted career data.

**For each agent, ask:**

| Check | If NO, action |
|-------|---------------|
| Did it answer the SPECIFIC question assigned? | Respawn that agent with a tighter prompt |
| Did it return CURRENT information (not just historical)? | Add "current" / "现任" keywords to the respawn prompt |
| Did it provide DATES and SOURCE URLs for each claim? | Ask the agent to supplement with sources |
| For Agent 3 (key deputies): did it cover the NAMED individuals, not a generic history of the position? | Most common failure — respawn with explicit "查 XXX（姓名）的履历，不是这个职位的历史" |

**If 2+ agents failed the check**: fix and respawn before moving to Phase 2. This quality
gate prevents the most common failure mode — where a bad Phase 1 output silently propagates
into Phase 2, and critical connections are missed.

After the gate passes, compile a **Phase 1 Gap Summary** — a bullet list of names with
missing career segments, ranked by their importance to the investigation. This directly
informs Phase 2 agent assignments.

---

## Phase 2: Deep Dive (3 Subagents)

Based on Phase 1 findings, identify the 3 most important gaps or leads, then deploy
3 subagents in parallel to investigate them. Use the same agent config as Phase 1.

Typical deep-dive topics:

| # | Topic | When to Use |
|---|-------|------------|
| 1 | **Primary Leader's Full Career** | If Phase 1 couldn't find the complete career history of the top leader (most common gap) |
| 2 | **Deputies' Career Intersections** | Find whether deputies ever worked with the top leader before (same org, same time) |
| 3 | **Predecessor's Whereabouts & Network** | Where did the predecessor go? Who did they take/promote? County-to-county exchange patterns |

### Deep Dive Agent Prompting

These agents should:
- Search for specific names + locations + time periods
- Cross-reference multiple sources to confirm dates
- Look for 任前公示 (pre-appointment public notices) which often contain full resumes
- Check Baidu Baike for each person (may need multiple search attempts)

---

## Phase 3: Build Deliverables

### 3a. Python Script: Database + Graph

Write a Python script `build_data.py` that creates both the SQLite database and the
GEXF graph file. Do NOT use pre-built templates — generate the script fresh based on
the actual research data collected.

**SQLite Schema** (4 tables):

```sql
persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
organizations (id, name, type, level, parent, location)
positions (id, person_id, org_id, title, start, end, rank, note)  -- FOREIGN KEY person_id, org_id
relationships (id, person_a, person_b, type, context, overlap_org, overlap_period)  -- FOREIGN KEY person_a, person_b
```

**GEXF Structure**:
- Nodes: persons (colored by role: red=party secretary, blue=government leader, orange=discipline, grey=other) + organizations (colored by type)
- Edges: person→organization (`worked_at`) + person↔person (`relationship`)
- Edge attributes: type, start date, end date, context description
- Viz attributes: color, size (20.0 for top leaders, 12.0 for others, 8.0 for orgs)
- Use `xmlns:viz="http://gexf.net/1.3/viz"` namespace for visual attributes

Build the GEXF using string formatting to avoid XML namespace issues with ElementTree.
See the pattern in `references/gexf_pattern.md`.

**Script Requirements**:
- Hard-code all research data as Python dicts/lists at the top of the script
- Use `sqlite3` standard library (no pip install needed)
- Generate GEXF 1.3 format with viz namespace
- Print summary statistics on completion
- Exit cleanly — check output files after running

### 3b. Markdown Report

Write a comprehensive Chinese-language report following this structure:

```
# [地区]领导班子工作关系网络调查报告
## 1. 现任[职位]：[姓名] (完整履历、晋升路径)
## 2. 现任[搭档职位]：[姓名] (履历)
## 3. 前任[职位]：[姓名] (去向)
## 4. 领导班子成员 (每人基本信息 + 履历)
## 5. 近期人事变动 (时间线)
## 6. 工作关系网络分析 (确认的交集、强弱关系分类)
## 7. 周边县区人事交流网络 (跨县调动模式)
## 8. 关键洞察与突破线索 (优先级排序)
## 9. 数据文件说明
## 10. 信息来源汇总 (所有URL)
```

Save as `report/YYYYMMDD-[地区]-[职位].md`.

### 3c. HTML Briefing Page — Delegate to `frontend-design` Skill

**CRITICAL**: Do NOT write the HTML yourself. Invoke the `frontend-design` skill via
`Skill({skill: "frontend-design", args: "<design brief>"})`. The frontend-design skill
is a specialized design agent that will produce a distinctive, non-templated result.

**Design brief to pass** (adapt the bracketed parts to the current investigation):

```
design html based on the following research. Single-file HTML page.

Subject: [地区]领导班子工作关系网络 — an intelligence briefing for researchers
analyzing Chinese political personnel networks.

Content to include:
- Header with title, date, and 4 key stats (人物/机构/任职/关系 count)
- Person card grid: all key figures with name, role, birthplace, connection badges
- Career timelines for the top 3-4 figures (vertical timeline)
- Relationship matrix table showing who connected to whom/when/where
- Cross-county exchange network flow diagram
- Key insights panel with breakthrough leads and power assessment

Design direction: Dark-mode "intelligence dossier" aesthetic. Deep near-black
surface, warm off-white text, cinnabar red (#E03C31) as the sole accent (used
sparingly like a seal stamp), gold (#C9A94E) for confirmed connections, hairline
1px borders, no rounded corners over 4px. Chinese-first typography with Noto
Serif SC for display. Think classified briefing document, not dashboard.

The real research data is below: [paste Phase 1+2 findings here]
```

**After the HTML is generated**:
- Save it as `report/YYYYMMDD-[地区]-[主题].html`
- Verify it opens correctly and all text renders

**Escalation**: If the frontend-design skill is unavailable or fails, fall back to
building the HTML inline using the design system documented in this skill. But
always try the skill first — it produces more distinctive results.

### 3d. Interactive Graph Page

Build a `graph.html` that visualizes ALL persons and relationships using **vis.js**
(CDN-loaded, no build step). This is the master graph for the entire project — accumulate
data from each investigation into it.

**Person ID Convention — CRITICAL for dedup across investigations**:

Use the format `{county}_{surname_givenname}` for person IDs, e.g.:
- `jinxian_xiong_zhenqiang` for 熊振强（进贤县委书记）
- `nanchang_jia_yuchao` for 贾彧超（南昌县委书记）

This prevents duplicates when the same person appears in multiple investigations
(e.g., 熊振强 appears in both 进贤县 research as secretary AND 南昌县 research via
徐志勇's Anyi connection). Before adding a new person, check by name + birth year
against existing nodes. If a match is found, ADD new positions/relationships to the
existing node rather than creating a duplicate.

**Requirements**:
- Load `vis-network` from CDN (https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/vis-network.min.js)
- Persons as colored circles (red=party secretary, blue=government, orange=discipline, grey=other)
- Organizations as small colored boxes
- Two edge types: `worked_at` (thin grey, person→org) and `relationship` (thick gold for strong, thin blue for weak, person↔person)
- forceAtlas2Based physics for natural layout
- Click a person node → show tooltip with name, title, birthplace, career summary
- Legend for node colors and edge types
- Auto-fit after stabilization
- Link back to `index.html`

**After each investigation**, check for duplicates (by name+birth), then append new
persons, organizations, and edges to graph.html so it grows into a comprehensive
network map over time.

---

## Critical Rules

### Model Selection
- Phase 1 & 2 subagents: ALWAYS `model: "haiku"` for cost efficiency
- Phase 3 code generation: use the session's default model (the one you're running on)

### Data Integrity
- Every claim must cite a source URL
- Distinguish "confirmed" vs "plausible" vs "unverified" in the report
- When a person's career history is incomplete, explicitly flag the gap — don't fabricate
- 百度百科 is secondary quality; government websites are primary

### File Organization
```
data/database/[network].db     — SQLite
data/graph/[network].gexf      — GEXF graph
report/YYYYMMDD-[地区]-[主题].md   — Markdown report
report/YYYYMMDD-[地区]-[主题].html — HTML briefing
report/index.html              — Master index linking all reports + data files
report/graph.html              — Interactive vis.js network graph (accumulate over time)
```
For GitHub Pages deployment, rename `report/` → `docs/` (Pages only supports `/` or `/docs`).

### Search Strategy (adapt to jurisdiction)

**For Chinese government entities**:
- Use WebSearch for each query (not WebFetch for initial searches)
- Government leadership pages (`ldzc.shtml`) are the most reliable source for current rosters
- 任前公示 (pre-appointment notices) from 市委组织部 are gold for career histories
- 澎湃新闻 (thepaper.cn) often has detailed official appointment articles
- 百度百科 is secondary quality; government websites are primary

**For US government entities**:
- Wikipedia is a strong starting point for federal/state officials
- Official .gov bio pages (congress.gov, agency sites)
- Ballotpedia for election history and prior offices
- OpenSecrets / FollowTheMoney for campaign finance connections
- LinkedIn for staff-level career paths
- News archives (NYT, WaPo, Politico) for appointment coverage

**Universal**: Always cite source URLs. Distinguish "confirmed from official source" vs "reported by media" vs "inferred from timeline overlap".

### Edge Cases
- If the target position is vacant or recently changed, note this prominently
- If Baidu Baike entries are incomplete (common for county-level officials), try 360百科, 搜狐百科
- If no career history can be found for a key figure, mark them as "履历待查" with priority level
- If the official website is inaccessible, try cached versions or news reports

---

## After Completion

Present to the user:
1. A summary of key findings (top 3-5 insights)
2. The file paths of all deliverables
3. The top 3 unanswered questions that could drive further investigation
4. An offer to deep-dive into any specific person or connection

### Open Gaps Registry

After EVERY investigation, write an **Open Gaps Registry** to `report/open_gaps.md`.
This file persists across investigations and tracks unresolved information holes with
priority levels. When starting a NEW investigation in the same region, read this file
first and prioritize filling the highest-ranked gaps.

**Format**:

```markdown
# Open Gaps Registry
> Last updated: YYYY-MM-DD

## ⭐⭐⭐⭐⭐ Critical (core figures with major career gaps)
| Person | Current Role | What's Missing | Last Attempted | Notes |
|--------|-------------|----------------|----------------|-------|
| 雷桥亮 | 进贤代县长 | 2022年前20年职业生涯 | 2026-07-14 | 1980年生，42岁前履历完全未知 |

## ⭐⭐⭐⭐ High (important deputies or key connections)
| Person/Gap | What's Missing | Last Attempted | Notes |
|-----------|----------------|----------------|-------|
| 帅志 | 1996-2008 12年早期履历 | 2026-07-14 | 南昌县长 |

## ⭐⭐⭐ Medium (would enrich the network picture)
| Gap | Last Attempted | Notes |
|-----|----------------|-------|

## ⭐⭐ Low (nice to have)
| Gap | Last Attempted | Notes |
|-----|----------------|-------|
```

**Rules**:
- Update this file after every investigation — add new gaps, remove filled ones, adjust priorities
- Never delete entries older than 6 months — they may still be useful context
- When a gap is filled, move it to a "Resolved" section at the bottom with the date resolved
- Read this file at the START of each new investigation to guide Phase 2 deep-dive topics
