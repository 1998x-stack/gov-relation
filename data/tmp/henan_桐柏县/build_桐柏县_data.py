#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 桐柏县 leadership network.

桐柏县 - 南阳市 - 河南省
Targets: 县委书记许晓燕, 县长王龙
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Ensure gov_relation is importable
_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "桐柏县"
TASK_ID = "henan_桐柏县"
TODAY = datetime.now().strftime("%Y-%m-%d")

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # ═══ Core Leaders ═══
    {
        "id": 1,
        "name": "许晓燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桐柏县委书记",
        "current_org": "中国共产党桐柏县委员会",
        "source": "https://www.tongbai.gov.cn/2026/07-07/1417888.html",
    },
    {
        "id": 2,
        "name": "王龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桐柏县委副书记、县长",
        "current_org": "桐柏县人民政府",
        "source": "https://www.tongbai.gov.cn/2026/06-05/1410155.html",
    },
    # ═══ Previous Leaders ═══
    {
        "id": 3,
        "name": "党建凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原桐柏县委书记（已离任）",
        "current_org": "",
        "source": "https://www.tongbai.gov.cn/2026/03-04/1388575.html",
    },
    # ═══ Government Leaders ═══
    {
        "id": 4,
        "name": "赵伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "桐柏县人民政府",
        "source": "https://www.tongbai.gov.cn/zjzf/",
    },
    {
        "id": 5,
        "name": "林丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "桐柏县人民政府",
        "source": "https://www.tongbai.gov.cn/zjzf/",
    },
    {
        "id": 6,
        "name": "古琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "桐柏县人民政府",
        "source": "https://www.tongbai.gov.cn/zjzf/",
    },
    {
        "id": 7,
        "name": "朱岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "桐柏县人民政府",
        "source": "https://www.tongbai.gov.cn/zjzf/",
    },
    {
        "id": 8,
        "name": "朱盛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "桐柏县人民政府",
        "source": "https://www.tongbai.gov.cn/zjzf/",
    },
    {
        "id": 9,
        "name": "张义胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "桐柏县人民政府",
        "source": "https://www.tongbai.gov.cn/zjzf/",
    },
    {
        "id": 10,
        "name": "谢浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "桐柏县人民政府",
        "source": "https://www.tongbai.gov.cn/2026/06-05/1410148.html",
    },
    # ═══ Party Committee Leaders ═══
    {
        "id": 11,
        "name": "郑杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委（县委领导）",
        "current_org": "中国共产党桐柏县委员会",
        "source": "https://www.tongbai.gov.cn/2026/07-09/1418877.html",
    },
    {
        "id": 12,
        "name": "杨好宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委（县委领导）",
        "current_org": "中国共产党桐柏县委员会",
        "source": "https://www.tongbai.gov.cn/2026/06-05/1410155.html",
    },
    {
        "id": 13,
        "name": "陈明建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委（县委领导）",
        "current_org": "中国共产党桐柏县委员会",
        "source": "https://www.tongbai.gov.cn/2026/07-07/1417888.html",
    },
    {
        "id": 14,
        "name": "黄玉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委（县委领导）",
        "current_org": "中国共产党桐柏县委员会",
        "source": "https://www.tongbai.gov.cn/2026/07-09/1418877.html",
    },
    # ═══ NPC Standing Committee ═══
    {
        "id": 15,
        "name": "王宏波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "桐柏县人民代表大会常务委员会",
        "source": "https://www.tongbai.gov.cn/2026/06-05/1410155.html",
    },
    {
        "id": 16,
        "name": "朱东明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（县委领导）",
        "current_org": "中国共产党桐柏县委员会",
        "source": "https://www.tongbai.gov.cn/2026/06-05/1410155.html",
    },
    {
        "id": 17,
        "name": "李刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "桐柏县",
        "source": "https://www.tongbai.gov.cn/2026/06-05/1410155.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中国共产党桐柏县委员会", "type": "党委", "level": "县委", "parent": "南阳市委", "location": "桐柏县"},
    {"id": 2, "name": "桐柏县人民政府", "type": "政府", "level": "县政府", "parent": "桐柏县委", "location": "桐柏县"},
    {"id": 3, "name": "桐柏县人民代表大会常务委员会", "type": "人大", "level": "县人大", "parent": "桐柏县", "location": "桐柏县"},
]

# ── Positions ────────────────────────────────────────────────────────

positions = [
    # 许晓燕
    {"person_id": 1, "org_id": 1, "title": "桐柏县委书记", "start_date": "约2025-2026", "end_date": "", "rank": "正处级", "note": "此前兼任县长至2026年5月"},
    {"person_id": 1, "org_id": 2, "title": "桐柏县人民政府县长（原兼）", "start_date": "未知", "end_date": "2026-05", "rank": "正处级", "note": "2026年5月11日辞去县长职务"},
    # 王龙
    {"person_id": 2, "org_id": 2, "title": "桐柏县委副书记、县长", "start_date": "2026-05", "end_date": "", "rank": "正处级", "note": "2026年5月11日任代县长，6月4日当选县长"},
    {"person_id": 2, "org_id": 1, "title": "桐柏县委副书记", "start_date": "2026-05", "end_date": "", "rank": "副处级", "note": "同时担任县委副书记"},
    # 党建凯（前任县委书记）
    {"person_id": 3, "org_id": 1, "title": "桐柏县委书记", "start_date": "未知", "end_date": "约2025-2026", "rank": "正处级", "note": "2026年3月仍以县委书记身份活动，之后由许晓燕接任"},
    # 赵伟
    {"person_id": 4, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 林丽
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 古琴
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 朱岩
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 朱盛
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 张义胜
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 谢浩
    {"person_id": 10, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 郑杰
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 杨好宁
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 陈明建
    {"person_id": 13, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 黄玉
    {"person_id": 14, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 王宏波
    {"person_id": 15, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 朱东明
    {"person_id": 16, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "", "rank": "", "note": "主席团常务主席"},
    # 李刚
    {"person_id": 17, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "", "rank": "", "note": "主席团常务主席"},
]

# ── Relationships ────────────────────────────────────────────────────

relationships = [
    # 许晓燕 <-> 王龙（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长党政工作搭档关系", "overlap_org": "桐柏县委/县政府", "overlap_period": "2026-05至今"},
    # 许晓燕 <-> 党建凯（前后任县委书记）
    {"person_a": 1, "person_b": 3, "type": "前后任", "context": "先后担任桐柏县委书记", "overlap_org": "中共桐柏县委", "overlap_period": "2025-2026"},
    # 王龙 <-> 许晓燕（上下级/前后任县长）
    {"person_a": 1, "person_b": 2, "type": "上下级", "context": "许晓燕原兼任县长，王龙接任县长", "overlap_org": "桐柏县人民政府", "overlap_period": "2026-05"},
    # 许晓燕 <-> 谢浩（县委常委工作关系）
    {"person_a": 1, "person_b": 10, "type": "工作关系", "context": "县委书记与常务副县长工作关系", "overlap_org": "桐柏县委/县政府", "overlap_period": ""},
    # 许晓燕 <-> 赵伟（县委常委工作关系）
    {"person_a": 1, "person_b": 4, "type": "工作关系", "context": "县委书记与县委常委/副县长工作关系", "overlap_org": "桐柏县委", "overlap_period": ""},
    # 许晓燕 <-> 陈明建（县委常委工作关系）
    {"person_a": 1, "person_b": 13, "type": "工作关系", "context": "县委书记与县委常委工作关系", "overlap_org": "桐柏县委", "overlap_period": ""},
    # 王龙 <-> 谢浩（正副县⻓工作关系）
    {"person_a": 2, "person_b": 10, "type": "工作关系", "context": "县长与常务副县长工作搭档", "overlap_org": "桐柏县人民政府", "overlap_period": "2026-05至今"},
    # 王龙 <-> 赵伟（正副县长工作关系）
    {"person_a": 2, "person_b": 4, "type": "工作关系", "context": "县长与副县长工作搭档", "overlap_org": "桐柏县人民政府", "overlap_period": "2026-05至今"},
    # 王宏波 <-> 许晓燕（县人大与县委工作关系）
    {"person_a": 1, "person_b": 15, "type": "工作关系", "context": "县委书记与县人大常委会主任工作关系", "overlap_org": "桐柏县", "overlap_period": ""},
    # 王宏波 <-> 王龙（人大任命县长）
    {"person_a": 2, "person_b": 15, "type": "任命关系", "context": "县人大常委会主任主持任命王龙为代县长、选举县长", "overlap_org": "桐柏县人大/县政府", "overlap_period": "2026-05至2026-06"},
]

# ══════════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ══════════════════════════════════════════════════════════════════════


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
    print(f"  信息来源: 桐柏县人民政府网站 (tongbai.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(str(DB_PATH))
    create_tables(conn)

    # Insert persons
    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    # Insert organizations
    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    # Insert positions
    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c,"") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    # Insert relationships
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

    # ── GEXF ──────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "县委书记" in post:
            return ("255,50,50", 20.0)
        elif "县长" in post:
            return ("50,100,255", 20.0)
        elif "常务" in post:
            return ("50,100,255", 15.0)
        elif "副县长" in post:
            return ("100,100,255", 12.0)
        elif "人大主任" in post:
            return ("200,255,255", 15.0)
        elif "原" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,255"),
            "事业单位": ("220,220,220"),
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
        lines.append('        <viz:size value="8.0"/>')
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

    with open(str(GEXF_PATH), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    run_build()
