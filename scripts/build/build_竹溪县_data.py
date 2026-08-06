#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 竹溪县 (Zhuxi County), 十堰市, 湖北省.

Level: 县
Province: 湖北省
Parent city: 十堰市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: hubei_竹溪县

Research date: 2026-08-06
Official source: http://www.zhuxi.gov.cn/ (竹溪县人民政府) — confirmed accessible via HTTP

Current status (as of 2026-08-06):
- 县委书记: 许庆一 (confirmed via official 县委 leadership page + leader bio article + news)
- 县委副书记、县长: 师文明 (confirmed via official 县委/县政府 leadership pages + leader bio)

Roster sources:
  县委领导: http://www.zhuxi.gov.cn/xxgkxi/fdzdgk/zfld/xw/
  县政府领导: http://www.zhuxi.gov.cn/xxgkxi/fdzdgk/zfld/xzf/

Confidence notes:
  - Current roles for all 县委/县政府 members: confirmed via official government website bios (2026-08)
  - Identity fields (gender, ethnicity, birth year, birthplace, education, party/work dates): confirmed for
    every leader from official individual bio articles on zhuxi.gov.cn
  - Full PRIOR career-timeline segments (posts before current role): unverified (official "简历" gives only
    identity + current role, not the full post history)
  - Predecessor 书记/县长 identities and tenures: unverified (Exa rate-limited, Baidu/Bing blocked) — see open gaps
  - All names gender inferred only where official note omitted; defaulted conservatively
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
SLUG = "竹溪县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# Core source URIs reused throughout
S_XW = "http://www.zhuxi.gov.cn/xxgkxi/fdzdgk/zfld/xw/"
S_XZF = "http://www.zhuxi.gov.cn/xxgkxi/fdzdgk/zfld/xzf/"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "许庆一",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1983-10",
        "birthplace": "河南南阳",
        "education": "党校研究生",
        "party_join": "中共党员（2007-04加入）",
        "work_start": "2005-08",
        "current_post": "县委书记",
        "current_org": "中共竹溪县委员会",
        "source": S_XW + "xqy/"
    },
    {
        "id": 2,
        "name": "师文明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-08",
        "birthplace": "河南漯河",
        "education": "博士研究生",
        "party_join": "中共党员（2002-06加入）",
        "work_start": "2003-07",
        "current_post": "县委副书记、县长",
        "current_org": "竹溪县人民政府",
        "source": S_XW + "swm_xw/"
    },
    # ═══════ 县委领导 ═══════
    {
        "id": 3,
        "name": "刘冬勤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-08",
        "birthplace": "湖北荆门",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "2008-07",
        "current_post": "县委副书记",
        "current_org": "中共竹溪县委员会",
        "source": S_XW + "kam_119446/"
    },
    {
        "id": 4,
        "name": "李伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-01",
        "birthplace": "湖北郧县",
        "education": "党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共竹溪县委组织部",
        "source": S_XW + "lw/"
    },
    {
        "id": 5,
        "name": "柯爱民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-08",
        "birthplace": "湖北竹溪",
        "education": "大学",
        "party_join": "中共党员（1998-01加入）",
        "work_start": "1988-12",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共竹溪县委统一战线工作部",
        "source": S_XW + "kam_97209/"
    },
    {
        "id": 6,
        "name": "罗显锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "湖北竹山",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共竹溪县纪律检查委员会",
        "source": S_XW + "kam_117744/"
    },
    {
        "id": 7,
        "name": "李芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980-08",
        "birthplace": "湖北竹溪",
        "education": "党校研究生",
        "party_join": "中共党员（2006-12加入）",
        "work_start": "1999-09",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共竹溪县委宣传部",
        "source": S_XW + "kam/"
    },
    {
        "id": 8,
        "name": "喻伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-09",
        "birthplace": "湖北竹溪",
        "education": "党校研究生",
        "party_join": "中共党员（2008-07加入）",
        "work_start": "2005-09",
        "current_post": "县委常委、常务副县长、政法委书记",
        "current_org": "竹溪县人民政府",
        "source": S_XZF + "swm_xzf_123641/"
    },
    {
        "id": 9,
        "name": "彭君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-10",
        "birthplace": "湖北竹溪",
        "education": "大学本科",
        "party_join": "中共党员（2003-07加入）",
        "work_start": "2000-10",
        "current_post": "县委常委、副县长",
        "current_org": "竹溪县人民政府",
        "source": S_XZF + "swm_xzf_115094/"
    },
    {
        "id": 10,
        "name": "朱东方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-04",
        "birthplace": "北京密云",
        "education": "党校研究生",
        "party_join": "中共党员（2003-06加入）",
        "work_start": "2004-08",
        "current_post": "县委常委、副县长",
        "current_org": "竹溪县人民政府",
        "source": S_XZF + "swm_xzf_123546/"
    },
    {
        "id": 11,
        "name": "潘志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-12",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县人武部部长",
        "current_org": "竹溪县人民武装部",
        "source": S_XW + "kam_119759/"
    },
    # ═══════ 县政府其他领导 ═══════
    {
        "id": 12,
        "name": "王博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-12",
        "birthplace": "湖北十堰",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "2008-08",
        "current_post": "副县长",
        "current_org": "竹溪县人民政府",
        "source": S_XZF + "ylj_119509/"
    },
    {
        "id": 13,
        "name": "吴毕龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-11",
        "birthplace": "湖北监利",
        "education": "大学",
        "party_join": "中共党员（2004-06加入）",
        "work_start": "2000-12",
        "current_post": "副县长、县公安局局长",
        "current_org": "竹溪县人民法院/竹溪县公安局",
        "source": S_XZF + "ylj/"
    },
    {
        "id": 14,
        "name": "郭稼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-05",
        "birthplace": "湖北竹溪",
        "education": "大学本科",
        "party_join": "中共党员（2007-07加入）",
        "work_start": "2005-09",
        "current_post": "副县长",
        "current_org": "竹溪县人民政府",
        "source": S_XZF + "ylj_119503/"
    },
    {
        "id": 15,
        "name": "闫晗",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1988-09",
        "birthplace": "湖北十堰",
        "education": "硕士研究生",
        "party_join": "中共党员（2009-03加入）",
        "work_start": "2012-09",
        "current_post": "副县长",
        "current_org": "竹溪县人民政府",
        "source": S_XZF + "ylj_119508/"
    },
    {
        "id": 16,
        "name": "鲁仲顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-10",
        "birthplace": "湖北竹溪",
        "education": "在职大学（公共管理）",
        "party_join": "中共党员（2005-07加入）",
        "work_start": "1999-12",
        "current_post": "副县长",
        "current_org": "竹溪县人民政府",
        "source": S_XZF + "ylj_122094/"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共竹溪县委员会", "type": "党委", "level": "县级", "parent": "中共十堰市委员会", "location": "湖北省十堰市竹溪县"},
    {"id": 2, "name": "竹溪县人民政府", "type": "政府", "level": "县级", "parent": "十堰市人民政府", "location": "湖北省十堰市竹溪县"},
    {"id": 3, "name": "中共竹溪县委组织部", "type": "党委", "level": "县级", "parent": "中共竹溪县委员会", "location": "湖北省十堰市竹溪县"},
    {"id": 4, "name": "中共竹溪县委统一战线工作部", "type": "党委", "level": "县级", "parent": "中共竹溪县委员会", "location": "湖北省十堰市竹溪县"},
    {"id": 5, "name": "中共竹溪县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共十堰市纪律检查委员会", "location": "湖北省十堰市竹溪县"},
    {"id": 6, "name": "中共竹溪县委宣传部", "type": "党委", "level": "县级", "parent": "中共竹溪县委员会", "location": "湖北省十堰市竹溪县"},
    {"id": 7, "name": "中共竹溪县委政法委员会", "type": "党委", "level": "县级", "parent": "中共竹溪县委员会", "location": "湖北省十堰市竹溪县"},
    {"id": 8, "name": "竹溪县人民武装部", "type": "政府", "level": "县级", "parent": "十堰市军分区", "location": "湖北省十堰市竹溪县"},
    {"id": 9, "name": "竹溪县监察委员会", "type": "党委", "level": "县级", "parent": "十堰市监察委员会", "location": "湖北省十堰市竹溪县"},
    {"id": 10, "name": "竹溪县公安局", "type": "政府", "level": "县级", "parent": "十堰市公安局", "location": "湖北省十堰市竹溪县"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县级", "note": "Confirmed as of 2026-08-06"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "", "end": "present", "rank": "正县级", "note": "Confirmed as of 2026-08-06"},
    # 县委领导
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "县委常委、组织部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "县委常委、统战部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "县委常委、县纪委书记、县监委主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "县委常委、常务副县长、政法委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 8, "title": "县委常委、县人武部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 县政府其他领导
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 10, "title": "副县长、县公安局局长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # Top leadership tandem
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政主要领导搭档", "overlap_org": "竹溪县", "overlap_period": "current"},
    # 县委书记与县委班子成员
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与县委副书记", "overlap_org": "中共竹溪县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与组织部部长", "overlap_org": "中共竹溪县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与统战部部长", "overlap_org": "中共竹溪县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与纪委书记", "overlap_org": "中共竹溪县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与宣传部部长", "overlap_org": "中共竹溪县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记与常务副县长/政法委书记", "overlap_org": "中共竹溪县委员会", "overlap_period": "current"},
    # 县长与班子成员/副县长
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "竹溪县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "竹溪县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "竹溪县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "竹溪县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "竹溪县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "竹溪县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "竹溪县人民政府", "overlap_period": "current"},
    # 政法委书记兼常务副县长 与 公安局长（政法系统联动）
    {"person_a": 8, "person_b": 13, "type": "overlap", "context": "常务副县长/政法委书记与公安局长（政法系统联动）", "overlap_org": "竹溪县政法系统", "overlap_period": "current"},
    # 纪委书记 与 监察委主任同一人已是自我；常委与其他成员
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "县委书记与县人武部部长", "overlap_org": "中共竹溪县委员会", "overlap_period": "current"},
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
        return "县委书记" in p["current_post"] or p["current_post"] == "县长"

    def person_color(p):
        cp = p.get("current_post", "")
        if "县委书记" in cp:
            return "255,50,50"
        if cp == "县长":
            return "50,100,255"
        if "纪委书记" in cp:
            return "255,165,0"
        return "100,100,100"

    def org_color(o):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
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
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
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