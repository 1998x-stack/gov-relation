#!/usr/bin/env python3
"""Build 凤庆县 (Fengqing County) 领导班子工作关系网络.

云南省临沧市下辖县. 调查日期: 2026-08-04.
"""

import sqlite3
import os
import sys
from datetime import datetime
from pathlib import Path

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/yunnan_凤庆县")
DB_PATH = os.path.join(TMP, "凤庆县_network.db")
GEXF_PATH = os.path.join(TMP, "凤庆县_network.gexf")

TODAY = "2026-08-04"
SLUG = "凤庆县"
PROVINCE = "云南省"
CITY = "临沧市"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {
        "id": 1,
        "name": "张红波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤庆县委书记",
        "current_org": "中共凤庆县委",
        "source": "https://baike.baidu.com/item/凤庆县; 凤庆县领导干部大会 张红波同志任凤庆县委书记",
    },
    {
        "id": 2,
        "name": "杨承高",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1978-05",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "2001-03",
        "work_start": "1999-08",
        "current_post": "凤庆县委副书记、代县长",
        "current_org": "凤庆县人民政府",
        "source": "https://baike.baidu.com/item/杨承高",
    },

    # ── Previous Top Leaders ──
    {
        "id": 3,
        "name": "谭波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-10",
        "birthplace": "四川南充",
        "education": "大学本科（中国人民大学成人高等教育学院会计专业）",
        "party_join": "2001-11",
        "work_start": "1999-08",
        "current_post": "临沧市人大常委会代表工作委员会主任（原凤庆县委书记）",
        "current_org": "临沧市人大常委会",
        "source": "https://baike.baidu.com/item/谭波/59475540",
    },
    {
        "id": 4,
        "name": "陈礼军",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1979-02",
        "birthplace": "云南云县",
        "education": "大学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "楚雄州委常委、州委组织部部长",
        "current_org": "中共楚雄州委",
        "source": "https://baike.baidu.com/item/陈礼军/70457533",
    },
    {
        "id": 5,
        "name": "杨红俊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已被开除党籍、公职（原凤庆县长）",
        "current_org": "",
        "source": "https://baike.baidu.com/item/杨红俊/19143343",
    },

    # ── Standing Committee Members ──
    {
        "id": 6,
        "name": "朱映祥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤庆县委常委、常务副县长",
        "current_org": "凤庆县人民政府",
        "source": "https://www.sohu.com/a/1033942569_121106902",
    },
    {
        "id": 7,
        "name": "程林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤庆县委常委、县人武部部长",
        "current_org": "凤庆县人民武装部",
        "source": "https://www.sohu.com/a/1033942569_121106902",
    },
    {
        "id": 8,
        "name": "曹宪勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤庆县人大常委会主任",
        "current_org": "凤庆县人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/凤庆县",
    },
    {
        "id": 9,
        "name": "吴天安",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤庆县政协主席",
        "current_org": "政协凤庆县委员会",
        "source": "https://baike.baidu.com/item/凤庆县",
    },
    {
        "id": 10,
        "name": "夏永严",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤庆县人武部政治委员",
        "current_org": "凤庆县人民武装部",
        "source": "https://www.sohu.com/a/1033942569_121106902",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共凤庆县委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共临沧市委",
        "location": "云南省临沧市凤庆县",
    },
    {
        "id": 2,
        "name": "凤庆县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "临沧市人民政府",
        "location": "云南省临沧市凤庆县",
    },
    {
        "id": 3,
        "name": "凤庆县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "临沧市人大常委会",
        "location": "云南省临沧市凤庆县",
    },
    {
        "id": 4,
        "name": "政协凤庆县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "临沧市政协",
        "location": "云南省临沧市凤庆县",
    },
    {
        "id": 5,
        "name": "凤庆县人民武装部",
        "type": "军事",
        "level": "县处级",
        "parent": "临沧军分区",
        "location": "云南省临沧市凤庆县",
    },
    {
        "id": 6,
        "name": "中共楚雄州委",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共云南省委",
        "location": "云南省楚雄州",
    },
    {
        "id": 7,
        "name": "临沧市人大常委会",
        "type": "人大",
        "level": "地厅级",
        "parent": "云南省人大常委会",
        "location": "云南省临沧市",
    },
]

positions = [
    # Current positions
    {"person_id": 1, "org_id": 1, "title": "凤庆县委书记", "start_date": "2026-06", "end_date": "", "rank": "正处级", "note": "2026年6月11日到任"},
    {"person_id": 2, "org_id": 2, "title": "凤庆县委副书记、代县长", "start_date": "2026-06", "end_date": "", "rank": "正处级", "note": "2026年6月28日当选县委副书记、任代理县长"},
    {"person_id": 6, "org_id": 2, "title": "凤庆县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026年6月确证在任"},
    {"person_id": 7, "org_id": 5, "title": "凤庆县委常委、县人武部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "确证在任"},
    {"person_id": 10, "org_id": 5, "title": "凤庆县人武部政治委员", "start_date": "", "end_date": "", "rank": "副处级", "note": "确证在任"},
    {"person_id": 8, "org_id": 3, "title": "凤庆县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 9, "org_id": 4, "title": "凤庆县政协主席", "start_date": "2025-02", "end_date": "", "rank": "正处级", "note": "2025年2月20日当选"},

    # Historical positions
    {"person_id": 3, "org_id": 1, "title": "凤庆县委书记", "start_date": "2025-07", "end_date": "2026-06", "rank": "正处级", "note": "接替陈礼军"},
    {"person_id": 3, "org_id": 2, "title": "凤庆县委副书记、县长", "start_date": "2020-05", "end_date": "2025-07", "rank": "正处级", "note": "此前代理县长"},
    {"person_id": 3, "org_id": 7, "title": "临沧市人大常委会代表工作委员会主任", "start_date": "2026-06", "end_date": "", "rank": "正处级", "note": "调离凤庆县"},
    {"person_id": 4, "org_id": 1, "title": "凤庆县委书记", "start_date": "2021-05", "end_date": "2025-04", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "楚雄州委常委、州委组织部部长", "start_date": "2025-05", "end_date": "", "rank": "副厅级", "note": "升任"},
    {"person_id": 5, "org_id": 2, "title": "凤庆县委副书记、县长", "start_date": "2017-02", "end_date": "2019-08", "rank": "正处级", "note": "2015年12月代理县长，2019年8月落马被查"},

    # 杨承高 previous roles
    {"person_id": 2, "org_id": 1, "title": "凤庆县委副书记、三级调研员", "start_date": "", "end_date": "", "rank": "副处级", "note": "此前职务"},
    {"person_id": 2, "org_id": 7, "title": "临沧市乡村振兴局局长", "start_date": "2024-06", "end_date": "2025-10", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "临沧市农业农村局局长", "start_date": "2024-06", "end_date": "2026-06", "rank": "正处级", "note": "兼"},
    {"person_id": 2, "org_id": 2, "title": "云县幸福镇党委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": "此前职务"},

    # 陈礼军 previous roles (simplified)
    {"person_id": 4, "org_id": 2, "title": "永德县人民政府副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "沧源自治县委常委、县委组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "临沧市委组织部常务副部长", "start_date": "", "end_date": "", "rank": "正处级", "note": "接任凤庆县委书记前"},
]

relationships = [
    {
        "person_a": 4, "person_b": 3,
        "type": "前后任",
        "context": "陈礼军任凤庆县委书记时谭波任县长，2025年7月谭波接任书记",
        "overlap_org": "中共凤庆县委",
        "overlap_period": "2021-2025",
    },
    {
        "person_a": 3, "person_b": 1,
        "type": "前后任",
        "context": "谭波2026年6月调离凤庆，张红波接任县委书记",
        "overlap_org": "中共凤庆县委",
        "overlap_period": "2026-06",
    },
    {
        "person_a": 3, "person_b": 2,
        "type": "前后任/上下级",
        "context": "谭波任书记时杨承高任代理县长，同时谭波让出的县长位由杨承高接任",
        "overlap_org": "凤庆县人民政府/中共凤庆县委",
        "overlap_period": "2026-06",
    },
    {
        "person_a": 3, "person_b": 5,
        "type": "前后任/接替",
        "context": "杨红俊2019年8月落马后，谭波2019年11月到凤庆代理县长",
        "overlap_org": "凤庆县人民政府",
        "overlap_period": "2019",
    },
    {
        "person_a": 3, "person_b": 6,
        "type": "上下级",
        "context": "谭波任书记时朱映祥为常务副县长",
        "overlap_org": "凤庆县人民政府",
        "overlap_period": "—2026-06",
    },
    {
        "person_a": 4, "person_b": 3,
        "type": "上下级",
        "context": "陈礼军书记—谭波县长（2021.5—2025.4）",
        "overlap_org": "中共凤庆县委",
        "overlap_period": "2021-2025",
    },
    {
        "person_a": 1, "person_b": 2,
        "type": "上下级",
        "context": "张红波书记—杨承高代县长（2026.6—今）",
        "overlap_org": "凤庆县人民政府",
        "overlap_period": "2026-06—今",
    },
    {
        "person_a": 4, "person_b": 2,
        "type": "跨县关系",
        "context": "陈礼军是云县人（凤庆邻县），杨承高于云县幸福镇工作过",
        "overlap_org": "临沧市",
        "overlap_period": "",
    },
]


# ── BUILD FUNCTIONS ──────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    p = post
    if "县委书记" in p and "副书记" not in p and "原" not in p:
        return "255,50,50", 20.0
    elif "代县长" in p or ("县长" in p and "副" not in p and "原" not in p):
        return "50,100,255", 20.0
    elif "常务副县长" in p or "副市长" in p:
        return "50,100,255", 15.0
    elif "常委" in p or "常务" in p:
        return "100,100,255", 15.0
    elif "人大主任" in p or "政协主席" in p:
        return "200,255,255", 15.0
    elif "原" in p or "前" in p or "已被" in p:
        return "150,150,150", 10.0
    else:
        return "100,100,100", 12.0


def org_color(typ):
    return {
        "党委": ("255,200,200"),
        "政府": ("200,200,255"),
        "人大": ("200,255,255"),
        "政协": ("255,240,200"),
        "军事": ("200,200,200"),
    }.get(typ, ("200,200,200"))


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {TODAY}")
    print(f"  所属: {PROVINCE} {CITY}")
    print("=" * 60)

    # ── SQLite Database ──
    conn = sqlite3.connect(DB_PATH)
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

    # Insert persons
    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace",
              "education", "party_join", "work_start", "current_post",
              "current_org", "source"]
    for p in persons:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(
            f"INSERT OR REPLACE INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?'] * len(cols_p))})",
            vals,
        )

    # Insert organizations
    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(
            f"INSERT OR REPLACE INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?'] * len(cols_o))})",
            vals,
        )

    # Insert positions
    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(
            f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?'] * len(cols_pos))})",
            vals,
        )

    # Insert relationships
    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(
            f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?'] * len(cols_r))})",
            vals,
        )

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

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
        lines.append(f'          <attvalue for="4" value="{esc(p["source"][:80])}"/>')
        lines.append('        </attvalues>')
        c_vals = c.split(",")
        lines.append(f'        <viz:color r="{c_vals[0]}" g="{c_vals[1]}" b="{c_vals[2]}"/>')
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
        lines.append(
            f'      <edge id="{eid}" source="p{pos["person_id"]}" '
            f'target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">'
        )
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{r["person_a"]}" '
            f'target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">'
        )
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
    main()