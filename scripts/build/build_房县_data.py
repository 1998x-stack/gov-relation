#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 房县 (Fang County), 十堰市, 湖北省.

Level: 县
Province: 湖北省
Parent city: 十堰市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: hubei_房县

Research date: 2026-07-24
Official source: https://www.fangxian.gov.cn/ (房县人民政府) — confirmed accessible

Current status (as of 2026-07-24):
- 县委书记: 谢晓鸣 (confirmed via official government website leadership window)
- 县委副书记、县长: 杨丹华 (confirmed via official government website leadership window)

Roster sources:
  县政府领导之窗: https://www.fangxian.gov.cn/xzf/
  县委新闻报导确认: https://www.fangxian.gov.cn/ (谢晓鸣主持召开县委常委会, 杨丹华主持县政府常务会议)

Confidence notes:
  - Current roles for 县委书记 and 县长: confirmed via official government website
  - Full县委常委会/县政府/县人大 roster: unverified — article URLs on the CMS-based government site
    could not be directly fetched; 竹山县 roster used as structural template
  - Career histories for all leaders: unverified — only current positions confirmed from official sources
  - Birth details, education, party join dates: unverified
  - Exa search was rate-limited; Baidu returned 403; Google/Bing/DuckDuckGo timed out;
    Jina Reader timed out; Baidu Baike blocked
  - Some personal details (gender, ethnicity) may be inferred from official context where reasonable
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "房县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "谢晓鸣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共房县委员会",
        "source": "https://www.fangxian.gov.cn/xzf/ (领导之窗)"
    },
    {
        "id": 2,
        "name": "杨丹华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "房县人民政府",
        "source": "https://www.fangxian.gov.cn/xzf/ (领导之窗)"
    },
    # ═══════ 县委领导 (roster unverified — placeholder structure) ═══════
    {
        "id": 3,
        "name": "待确认-县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记（协助书记抓党建工作）",
        "current_org": "中共房县委员会",
        "source": "待确认 — 参考竹山县组织架构推定"
    },
    {
        "id": 4,
        "name": "待确认-纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共房县纪律检查委员会",
        "source": "待确认"
    },
    {
        "id": 5,
        "name": "待确认-常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "房县人民政府",
        "source": "待确认"
    },
    {
        "id": 6,
        "name": "待确认-组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共房县县委组织部",
        "source": "待确认"
    },
    {
        "id": 7,
        "name": "待确认-宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共房县县委宣传部",
        "source": "待确认"
    },
    {
        "id": 8,
        "name": "待确认-县委政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共房县县委政法委员会",
        "source": "待确认"
    },
    {
        "id": 9,
        "name": "待确认-县委办主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办主任",
        "current_org": "中共房县委员会办公室",
        "source": "待确认"
    },
    {
        "id": 10,
        "name": "待确认-统战部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共房县县委统战部",
        "source": "待确认"
    },
    {
        "id": 11,
        "name": "待确认-人武部政委",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县人武部政委",
        "current_org": "房县人民武装部",
        "source": "待确认"
    },
    # ═══════ 县政府其他领导 ═══════
    {
        "id": 12,
        "name": "待确认-副县长1",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "房县人民政府",
        "source": "待确认"
    },
    {
        "id": 13,
        "name": "待确认-副县长2",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "房县人民政府",
        "source": "待确认"
    },
    {
        "id": 14,
        "name": "待确认-副县长3",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "房县人民政府",
        "source": "待确认"
    },
    # ═══════ 县人大领导 ═══════
    {
        "id": 15,
        "name": "待确认-人大主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "房县人大常委会",
        "source": "待确认"
    },
    {
        "id": 16,
        "name": "待确认-人大副主任1",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "房县人大常委会",
        "source": "待确认"
    },
    # ═══════ 县政协领导 ═══════
    {
        "id": 17,
        "name": "待确认-政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组书记、主席",
        "current_org": "房县政协",
        "source": "待确认"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共房县委员会", "type": "党委", "level": "县级", "parent": "中共十堰市委员会", "location": "湖北省十堰市房县"},
    {"id": 2, "name": "房县人民政府", "type": "政府", "level": "县级", "parent": "十堰市人民政府", "location": "湖北省十堰市房县"},
    {"id": 3, "name": "中共房县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共十堰市纪律检查委员会", "location": "湖北省十堰市房县"},
    {"id": 4, "name": "房县监察委员会", "type": "党委", "level": "县级", "parent": "十堰市监察委员会", "location": "湖北省十堰市房县"},
    {"id": 5, "name": "中共房县县委组织部", "type": "党委", "level": "县级", "parent": "中共房县委员会", "location": "湖北省十堰市房县"},
    {"id": 6, "name": "中共房县县委宣传部", "type": "党委", "level": "县级", "parent": "中共房县委员会", "location": "湖北省十堰市房县"},
    {"id": 7, "name": "中共房县县委政法委员会", "type": "党委", "level": "县级", "parent": "中共房县委员会", "location": "湖北省十堰市房县"},
    {"id": 8, "name": "中共房县委员会办公室", "type": "党委", "level": "县级", "parent": "中共房县委员会", "location": "湖北省十堰市房县"},
    {"id": 9, "name": "中共房县县委统战部", "type": "党委", "level": "县级", "parent": "中共房县委员会", "location": "湖北省十堰市房县"},
    {"id": 10, "name": "房县人民武装部", "type": "政府", "level": "县级", "parent": "十堰市军分区", "location": "湖北省十堰市房县"},
    {"id": 11, "name": "房县人大常委会", "type": "人大", "level": "县级", "parent": "十堰市人大常委会", "location": "湖北省十堰市房县"},
    {"id": 12, "name": "房县政协", "type": "政协", "level": "县级", "parent": "政协十堰市委员会", "location": "湖北省十堰市房县"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县级", "note": "Confirmed as of 2026-07-24 via official website"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "", "end": "present", "rank": "正县级", "note": "Confirmed as of 2026-07-24 via official website"},
    # 县委领导 (placeholder)
    {"person_id": 3, "org_id": 1, "title": "县委副书记（协助书记抓党建工作）", "start": "", "end": "present", "rank": "副县级", "note": "待确认 — 推定存在此岗位"},
    {"person_id": 4, "org_id": 3, "title": "县委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副县级", "note": "待确认"},
    {"person_id": 5, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "present", "rank": "副县级", "note": "待确认"},
    {"person_id": 6, "org_id": 5, "title": "县委常委、组织部部长", "start": "", "end": "present", "rank": "副县级", "note": "待确认"},
    {"person_id": 7, "org_id": 6, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": "待确认"},
    {"person_id": 8, "org_id": 7, "title": "县委常委、政法委书记", "start": "", "end": "present", "rank": "副县级", "note": "待确认"},
    {"person_id": 9, "org_id": 8, "title": "县委常委、县委办主任", "start": "", "end": "present", "rank": "副县级", "note": "待确认"},
    {"person_id": 10, "org_id": 9, "title": "县委常委、统战部部长", "start": "", "end": "present", "rank": "副县级", "note": "待确认"},
    {"person_id": 11, "org_id": 10, "title": "县委常委、县人武部政委", "start": "", "end": "present", "rank": "副县级", "note": "待确认"},
    # 县政府其他领导
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "待确认"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "待确认"},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "待确认"},
    # 县人大
    {"person_id": 15, "org_id": 11, "title": "县人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正县级", "note": "待确认"},
    {"person_id": 16, "org_id": 11, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": "待确认"},
    # 县政协
    {"person_id": 17, "org_id": 12, "title": "县政协党组书记、主席", "start": "", "end": "present", "rank": "正县级", "note": "待确认"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # Top leadership tandem
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政主要领导搭档", "overlap_org": "房县", "overlap_period": "current"},
]

try:
    import sqlite3  # noqa: F811

    # ── Inject repo path ────────────────────────────────────────────────────
    sys.path.insert(0, str(BASE))

    from gov_relation.runner import run_build

    print(f"=== Building {SLUG} network ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\nDB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("=== Done ===")

except ImportError as e:
    print(f"ERROR importing gov_relation modules: {e}")
    print("Falling back to standalone mode...")
    # ── Standalone fallback ──────────────────────────────────────────────
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        conn.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["education"], p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        conn.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        conn.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
              pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        conn.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"Standalone DB written: {DB_PATH}")

    # ── Build GEXF ──────────────────────────────────────────────────────
    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">',
        '    <creator>Research Agent</creator>',
        f'    <description>{SLUG} leadership network</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="role" type="string"/>',
        '      <attribute id="2" title="org" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '    </attributes>',
    ]

    def is_top_leader(p):
        return "县委书记" in p["current_post"] or p["current_post"] == "县长" or "县委副书记、县长" in p["current_post"]

    def person_color(p):
        if "县委书记" in p.get("current_post", ""):
            return "255,50,50"
        if "县长" in p.get("current_post", ""):
            return "50,100,255"
        if "纪委书记" in p.get("current_post", ""):
            return "255,165,0"
        return "100,100,100"

    def org_color(o):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
        }
        return colors.get(o.get("type", ""), "200,200,200")

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p).split(",")
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o).split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        context = r.get("context", r.get("type", ""))
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(context)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Standalone GEXF written: {GEXF_PATH}")
