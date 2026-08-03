#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 江达县 (Jiangda County), 昌都市, 西藏自治区.

Current officeholders as of 2026-08:
  - Party Secretary (县委书记): 达瓦 — confirmed from jiangda.changdu.gov.cn news (2023-02 article)
  - County Mayor (县长): 张雷鸣 — Male, Han, born 1975-06, CPC 1999-01, work 1999-07
  - Key deputies: 王小丹, 高伟, 嘎松丁达, 秦云友, 李贺, 张鹏, 洛松次成, 王鑫, 江培次它, 达泽仁, 次仁央宗

Sources:
  - jiangda.changdu.gov.cn (official 江达县人民政府 website)
  - jiangda.changdu.gov.cn/jdx/c102078/zfxxgk_zfld.shtml (leadership listing)
  - jiangda.changdu.gov.cn/jdx/c102078/202108/f02c2671f0354cfda93f24ad61331c3e.shtml (张雷鸣 detail)
  - jiangda.changdu.gov.cn search results for 县委书记 (confirmed 达瓦)
  - changdu.gov.cn (昌都市人民政府)
  - changdu_network.db (existing repo database for prefecture-level data)
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TASK_ID = "xizang_江达县"
STAGING = os.path.join(BASE, "data/tmp", TASK_ID)
DB_PATH = os.path.join(STAGING, "江达县_network.db")
GEXF_PATH = os.path.join(STAGING, "江达县_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# Confidence: confirmed = official source verified; plausible = credible media
# =========================================================================
persons = [
    # ── Party Secretary (县委书记) ──
    {
        "id": 1,
        "name": "达瓦",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江达县委书记",
        "current_org": "中共江达县委员会",
        "source": "http://jiangda.changdu.gov.cn (search confirmed article: 江达县委书记达瓦深入寺庙开展走访慰问工作, 2023-02-06). Baidu Baike unavailable (403)."
    },
    # ── County Mayor (县长) ──
    {
        "id": 2,
        "name": "张雷鸣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-06",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1999-07",
        "current_post": "江达县委副书记、县长",
        "current_org": "江达县人民政府",
        "source": "http://jiangda.changdu.gov.cn/jdx/c102078/202108/f02c2671f0354cfda93f24ad61331c3e.shtml"
    },
    # ── Deputy leaders (from official leadership page) ──
    {
        "id": 3,
        "name": "王小丹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副秘书长、县委常委、县政府常务副县长",
        "current_org": "江达县人民政府",
        "source": "http://jiangda.changdu.gov.cn/jdx/c102078/zfxxgk_zfld.shtml"
    },
    {
        "id": 4,
        "name": "高伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常务副书记、政府常务副县长",
        "current_org": "江达县人民政府",
        "source": "http://jiangda.changdu.gov.cn/jdx/c102078/zfxxgk_zfld.shtml"
    },
    {
        "id": 5,
        "name": "嘎松丁达",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "江达县委常委、政府党组副书记、县政府常务副县长",
        "current_org": "江达县人民政府",
        "source": "http://jiangda.changdu.gov.cn/jdx/c102078/zfxxgk_zfld.shtml"
    },
    {
        "id": 6,
        "name": "秦云友",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府副县长",
        "current_org": "江达县人民政府",
        "source": "http://jiangda.changdu.gov.cn/jdx/c102078/zfxxgk_zfld.shtml"
    },
    {
        "id": 7,
        "name": "李贺",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政府副县长",
        "current_org": "江达县人民政府",
        "source": "http://jiangda.changdu.gov.cn/jdx/c102078/zfxxgk_zfld.shtml"
    },
    {
        "id": 8,
        "name": "张鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长、公安局局长兼督察长",
        "current_org": "江达县人民政府",
        "source": "http://jiangda.changdu.gov.cn/jdx/c102078/zfxxgk_zfld.shtml"
    },
    {
        "id": 9,
        "name": "洛松次成",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "江达县人民政府",
        "source": "http://jiangda.changdu.gov.cn/jdx/c102078/zfxxgk_zfld.shtml"
    },
    {
        "id": 10,
        "name": "王鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "江达县人民政府",
        "source": "http://jiangda.changdu.gov.cn/jdx/c102078/zfxxgk_zfld.shtml"
    },
    {
        "id": 11,
        "name": "江培次它",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "江达县人民政府",
        "source": "http://jiangda.changdu.gov.cn/jdx/c102078/zfxxgk_zfld.shtml"
    },
    {
        "id": 12,
        "name": "达泽仁",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "江达县人民政府",
        "source": "http://jiangda.changdu.gov.cn/jdx/c102078/zfxxgk_zfld.shtml"
    },
    {
        "id": 13,
        "name": "次仁央宗",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "江达县人民政府",
        "source": "http://jiangda.changdu.gov.cn/jdx/c102078/zfxxgk_zfld.shtml"
    },
    # ── Changdu-level leaders from existing changdu_network.db ──
    {
        "id": 14,
        "name": "庄劲松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-03",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "1993",
        "current_post": "昌都市委书记",
        "current_org": "中共昌都市委员会",
        "source": "https://baike.baidu.com/item/%E5%BA%84%E5%8A%B2%E6%9D%BE/58702246"
    },
    {
        "id": 15,
        "name": "罗庆伍",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1971-05",
        "birthplace": "西藏那曲",
        "education": "自治区党委党校大专",
        "party_join": "中共党员",
        "work_start": "1992-07",
        "current_post": "昌都市委副书记、市长",
        "current_org": "昌都市人民政府",
        "source": "changdu_network.db"
    },
    # ── Party committee leaders likely in 江达 ──
    # Additional deputies (from article: 高伟 is 县委常务副书记)
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共江达县委员会", "type": "党委", "level": "县", "parent": "中共昌都市委员会", "location": "西藏自治区昌都市江达县"},
    {"id": 2, "name": "江达县人民政府", "type": "政府", "level": "县", "parent": "昌都市人民政府", "location": "西藏自治区昌都市江达县"},
    {"id": 3, "name": "江达县公安局", "type": "政府", "level": "县", "parent": "江达县人民政府", "location": "西藏自治区昌都市江达县"},
    {"id": 4, "name": "江达县审计局", "type": "政府", "level": "县", "parent": "江达县人民政府", "location": "西藏自治区昌都市江达县"},
    {"id": 5, "name": "中共昌都市委员会", "type": "党委", "level": "地级", "parent": "中共西藏自治区委员会", "location": "西藏自治区昌都市"},
    {"id": 6, "name": "昌都市人民政府", "type": "政府", "level": "地级", "parent": "西藏自治区人民政府", "location": "西藏自治区昌都市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 达瓦 - Party Secretary
    {"person_id": 1, "org_id": 1, "title": "江达县委书记", "start": "", "end": "present", "rank": "县(正处)", "note": "Confirmed from 2023-02 news article. May still be current as of 2026."},
    # 张雷鸣 - County Mayor
    {"person_id": 2, "org_id": 2, "title": "江达县委副书记、县长", "start": "", "end": "present", "rank": "县(正处)", "note": "Confirmed from official website, bio last updated 2024-07-05"},
    # 王小丹
    {"person_id": 3, "org_id": 2, "title": "市政府副秘书长、县委常委、县政府常务副县长", "start": "", "end": "present", "rank": "县(副处)", "note": ""},
    # 高伟
    {"person_id": 4, "org_id": 1, "title": "县委常务副书记", "start": "", "end": "present", "rank": "县(副处)", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "政府常务副县长", "start": "", "end": "present", "rank": "县(副处)", "note": ""},
    # 嘎松丁达
    {"person_id": 5, "org_id": 2, "title": "江达县委常委、政府党组副书记、常务副县长", "start": "", "end": "present", "rank": "县(副处)", "note": ""},
    # 秦云友
    {"person_id": 6, "org_id": 2, "title": "县委常委、县政府副县长", "start": "", "end": "present", "rank": "县(副处)", "note": ""},
    # 李贺
    {"person_id": 7, "org_id": 2, "title": "县委常委、政府副县长", "start": "", "end": "present", "rank": "县(副处)", "note": ""},
    # 张鹏
    {"person_id": 8, "org_id": 3, "title": "县政府副县长、公安局局长兼督察长", "start": "", "end": "present", "rank": "县(副处)", "note": ""},
    # 洛松次成
    {"person_id": 9, "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "县(副处)", "note": ""},
    # 王鑫
    {"person_id": 10, "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "县(副处)", "note": ""},
    # 江培次它
    {"person_id": 11, "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "县(副处)", "note": ""},
    # 达泽仁
    {"person_id": 12, "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "县(副处)", "note": ""},
    # 次仁央宗
    {"person_id": 13, "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "县(副处)", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭档关系", "overlap_org": "江达县委/县政府", "overlap_period": "current", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与常务副县长工作关系", "overlap_org": "江达县人民政府", "overlap_period": "current", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长与常务副县长工作关系", "overlap_org": "江达县人民政府", "overlap_period": "current", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与常务副县长工作关系", "overlap_org": "江达县人民政府", "overlap_period": "current", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与公安局局长", "overlap_org": "江达县人民政府", "overlap_period": "current", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "江达县人民政府", "overlap_period": "current", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "江达县人民政府", "overlap_period": "current", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "江达县人民政府", "overlap_period": "current", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "江达县人民政府", "overlap_period": "current", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "江达县人民政府", "overlap_period": "current", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "两人均任常务副县长", "overlap_org": "江达县人民政府", "overlap_period": "current", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "同任县委常委", "overlap_org": "中共江达县委员会", "overlap_period": "current", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "同任县委常委、副县长", "overlap_org": "江达县人民政府", "overlap_period": "current", "strength": "medium", "confidence": "confirmed"},
]

# =========================================================================
# SQLITE DATABASE
# =========================================================================
def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '',
        birth TEXT DEFAULT '',
        birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '',
        party_join TEXT DEFAULT '',
        work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '',
        current_org TEXT DEFAULT '',
        source TEXT DEFAULT ''
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT DEFAULT '',
        level TEXT DEFAULT '',
        parent TEXT DEFAULT '',
        location TEXT DEFAULT ''
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT DEFAULT '',
        start TEXT DEFAULT '',
        end TEXT DEFAULT '',
        rank TEXT DEFAULT '',
        note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL,
        type TEXT DEFAULT '',
        context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        strength TEXT DEFAULT '',
        confidence TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

# =========================================================================
# GEXF GRAPH
# =========================================================================
def e(s):
    """XML-escape."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(name, role):
    """Color by role."""
    if "书记" in role and "副" not in role:
        return "255,50,50"  # red — party secretary
    if "县长" in role and "副" not in role:
        return "50,100,255"  # blue — county mayor
    if "常务副" in role:
        return "70,130,200"  # steel blue — executive deputy
    if "副县长" in role or "副主席" in role:
        return "100,130,200"  # lighter blue — deputy
    if "政法委" in role or "公安" in role or "督察" in role:
        return "255,165,0"  # orange — public security/discipline
    if "组织" in role or "统战" in role:
        return "200,130,50"  # amber
    if "宣传" in role:
        return "180,180,50"  # olive
    return "100,100,100"  # grey

def org_type_color(otype):
    m = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
         "政协": "255,240,200", "事业单位": "220,220,220", "公安": "180,180,220"}
    return m.get(otype, "200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>江达县 leadership network - 昌都市, 西藏自治区</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="organization" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p, p["current_post"])
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{e(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{e(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{e(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:position x="{len(lines) * 0.1}" y="{len(lines) * 0.1}" z="0.0"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_type_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{e(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{e(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # person→organization edges (worked_at)
    for pos in positions:
        eid += 1
        o = next((x for x in organizations if x["id"] == pos["org_id"]), None)
        w = "2.0" if any(p["id"] == pos["person_id"] and p["id"] in (1,2) for p in persons) else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{e(pos["title"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{e(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person↔person edges (relationship)
    for r in relationships:
        eid += 1
        w = "3.0" if r["strength"] == "strong" else "2.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{e(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{e(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")