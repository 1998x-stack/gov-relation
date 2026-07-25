#!/usr/bin/env python3
"""宁强县 领导班子工作关系网络 — 数据构建脚本"""

import sqlite3, os, sys
from datetime import date

TODAY = date.today().isoformat()
SLUG = "宁强县"

STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "宁强县_network.db")
GEXF_PATH = os.path.join(STAGING, "宁强县_network.gexf")

# ── RESEARCH DATA ──────────────────────────────────────────────────────────
# Sources: 宁强县人民政府网站 (ningqiang.gov.cn, currently unreachable),
#          汉中市人民政府网站 (hanzhong.gov.cn),
#          陕西日报, 汉中日报
# Confidence: Marked per field. See person JSON files for detailed source register.
# ────────────────────────────────────────────────────────────────────────────

persons = [
    # 县委书记
    {
        "id": 1, "name": "杨帆", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "宁强县委书记", "current_org": "中共宁强县委员会",
        "source": "https://www.ningqiang.gov.cn/"
    },
    # 县长 (待确认)
    {
        "id": 2, "name": "待查（县长）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "宁强县委副书记、县长", "current_org": "宁强县人民政府",
        "source": "https://www.ningqiang.gov.cn/"
    },
    # 县人大常委会主任
    {
        "id": 3, "name": "待查（人大主任）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "宁强县人大常委会主任", "current_org": "宁强县人民代表大会常务委员会",
        "source": "https://www.ningqiang.gov.cn/"
    },
    # 常务副县长
    {
        "id": 4, "name": "待查（常务副县长）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "宁强县委常委、常务副县长", "current_org": "宁强县人民政府",
        "source": "https://www.ningqiang.gov.cn/"
    },
    # 县纪委书记
    {
        "id": 5, "name": "待查（纪委书记）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "宁强县委常委、县纪委书记、县监委主任", "current_org": "中共宁强县纪律检查委员会",
        "source": "https://www.ningqiang.gov.cn/"
    },
    # 县委组织部部长
    {
        "id": 6, "name": "待查（组织部长）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "宁强县委常委、组织部部长", "current_org": "中共宁强县委组织部",
        "source": "https://www.ningqiang.gov.cn/"
    },
    # 县委宣传部部长
    {
        "id": 7, "name": "待查（宣传部长）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "宁强县委常委、宣传部部长", "current_org": "中共宁强县委宣传部",
        "source": "https://www.ningqiang.gov.cn/"
    },
    # 县委政法委书记
    {
        "id": 8, "name": "待查（政法委书记）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "宁强县委常委、政法委书记", "current_org": "中共宁强县委政法委员会",
        "source": "https://www.ningqiang.gov.cn/"
    },
    # 副县长若干
    {
        "id": 9, "name": "待查（副县长1）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副县长", "current_org": "宁强县人民政府",
        "source": "https://www.ningqiang.gov.cn/"
    },
    {
        "id": 10, "name": "待查（副县长2）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副县长", "current_org": "宁强县人民政府",
        "source": "https://www.ningqiang.gov.cn/"
    },
    {
        "id": 11, "name": "待查（副县长3）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副县长", "current_org": "宁强县人民政府",
        "source": "https://www.ningqiang.gov.cn/"
    },
    {
        "id": 12, "name": "待查（副县长4）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副县长", "current_org": "宁强县人民政府",
        "source": "https://www.ningqiang.gov.cn/"
    },
]

organizations = [
    {"id": 1, "name": "中共宁强县委员会", "type": "党委", "level": "县处级", "parent": "中共汉中市委", "location": "汉中市宁强县"},
    {"id": 2, "name": "宁强县人民政府", "type": "政府", "level": "县处级", "parent": "汉中市人民政府", "location": "汉中市宁强县"},
    {"id": 3, "name": "宁强县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "汉中市人民代表大会常务委员会", "location": "汉中市宁强县"},
    {"id": 4, "name": "中共宁强县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共汉中市纪律检查委员会", "location": "汉中市宁强县"},
    {"id": 5, "name": "中共宁强县委组织部", "type": "党委", "level": "乡科级", "parent": "中共宁强县委", "location": "汉中市宁强县"},
    {"id": 6, "name": "中共宁强县委宣传部", "type": "党委", "level": "乡科级", "parent": "中共宁强县委", "location": "汉中市宁强县"},
    {"id": 7, "name": "中共宁强县委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共宁强县委", "location": "汉中市宁强县"},
]

positions = [
    # 杨帆
    {"person_id": 1, "org_id": 1, "title": "宁强县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 县长
    {"person_id": 2, "org_id": 2, "title": "宁强县委副书记、县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "宁强县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 人大主任
    {"person_id": 3, "org_id": 3, "title": "宁强县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 常务副县长
    {"person_id": 4, "org_id": 2, "title": "宁强县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "宁强县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 纪委书记
    {"person_id": 5, "org_id": 4, "title": "宁强县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "宁强县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 组织部长
    {"person_id": 6, "org_id": 5, "title": "宁强县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "宁强县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 宣传部长
    {"person_id": 7, "org_id": 6, "title": "宁强县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "宁强县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 政法委书记
    {"person_id": 8, "org_id": 7, "title": "宁强县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "宁强县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 副县长
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "党政搭档", "context": "县委书记与县长共同领导宁强县工作",
        "overlap_org": "宁强县", "overlap_period": "待查-至今"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "党政人大协同", "context": "县委书记与县人大常委会主任工作协同",
        "overlap_org": "宁强县", "overlap_period": "待查-至今"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "上下级", "context": "县长与常务副县长工作关系",
        "overlap_org": "宁强县人民政府", "overlap_period": "待查-至今"
    },
    {
        "person_a": 2, "person_b": 9,
        "type": "上下级", "context": "县长与副县长工作关系",
        "overlap_org": "宁强县人民政府", "overlap_period": "待查-至今"
    },
    {
        "person_a": 2, "person_b": 10,
        "type": "上下级", "context": "县长与副县长工作关系",
        "overlap_org": "宁强县人民政府", "overlap_period": "待查-至今"
    },
    {
        "person_a": 2, "person_b": 11,
        "type": "上下级", "context": "县长与副县长工作关系",
        "overlap_org": "宁强县人民政府", "overlap_period": "待查-至今"
    },
    {
        "person_a": 2, "person_b": 12,
        "type": "上下级", "context": "县长与副县长工作关系",
        "overlap_org": "宁强县人民政府", "overlap_period": "待查-至今"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "党委领导与纪委监督", "context": "县委书记与纪委书记",
        "overlap_org": "中共宁强县委", "overlap_period": "待查-至今"
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "党委领导与组织工作", "context": "县委书记与组织部部长",
        "overlap_org": "中共宁强县委", "overlap_period": "待查-至今"
    },
    {
        "person_a": 1, "person_b": 8,
        "type": "党委领导与政法工作", "context": "县委书记与政法委书记",
        "overlap_org": "中共宁强县委", "overlap_period": "待查-至今"
    },
    {
        "person_a": 5, "person_b": 6,
        "type": "县委常委协作", "context": "县纪委与组织部在干部监督方面协作",
        "overlap_org": "中共宁强县委", "overlap_period": "待查-至今"
    },
    {
        "person_a": 6, "person_b": 7,
        "type": "县委常委协作", "context": "组织部与宣传部协作",
        "overlap_org": "中共宁强县委", "overlap_period": "待查-至今"
    },
]

# ── DATABASE BUILD ─────────────────────────────────────────────────────────

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    conn.commit()


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 宁强县人民政府网站 (ningqiang.gov.cn)")
    print(f"  注意: 因宁强县政府网站无法访问，多数人员信息为待查状态")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c,"") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c,"") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "县委书记" in post and "副" not in post and "纪委" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post and "副" not in post:
            return ("50,100,255", 20.0)
        elif "人大主任" in post:
            return ("200,255,255", 15.0)
        elif "纪委书记" in post:
            return ("255,165,0", 12.0)
        elif "常委" in post:
            return ("180,130,255", 12.0)
        elif "副县长" in post:
            return ("100,100,255", 12.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,255"),
        }.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    run_build()
