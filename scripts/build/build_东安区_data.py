#!/usr/bin/env python3
"""东安区(牡丹江市) 领导班子工作关系网络 — 数据构建脚本

研究日期: 2026-08-05
主要来源: 东安区人民政府官方网站 https://www.donganqu.gov.cn/mdjdaqrmzf/c102959/ldlist.shtml (区委领导)
          /mdjdaqrmzf/c102961/ldlist.shtml (区政府领导)
          东安宣传微信公众号 <十一届十次全会> 报道 (2026-01-06)
"""

import os
from datetime import date

TODAY = date.today().isoformat()
SLUG = "东安区"
SHORT = "东安"

BASE = os.path.dirname(os.path.abspath(__file__))
# 规范产物路径：统一写入 data/database 与 data/graph
# 脚本可能在 scripts/build/ 或 data/tmp/<task>/ 中运行；
# 通过上溯目录定位仓库根目录，使 DB/GEXF 落盘到规范位置。
if os.path.basename(BASE) == "build" and os.path.basename(os.path.dirname(BASE)) == "scripts":
    REPO = os.path.dirname(os.path.dirname(BASE))
else:
    REPO = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))
DB_PATH = os.path.join(REPO, "data", "database", "东安区_network.db")
GEXF_PATH = os.path.join(REPO, "data", "graph", "东安区_network.gexf")

# ── RESEARCH DATA ──────────────────────────────────────────────────────────
# 来源缩写:
#   O1 东安区人民政府官网-领导简介(区委/政府/人大/政协)
#   O2 东安宣传公众号《区委十一届十次全会》报道
#   O3 东安区人大 会议报道
#   M1 既往牡丹江/宁安调查 (王树军 履历)

persons = [
    # ── 核心:区委书记 ──
    {
        "id": 1, "name": "林坤", "gender": "女", "ethnicity": "汉族",
        "birth": "1977年1月", "birthplace": "", "education": "研究生学历，农业推广硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安区委书记", "current_org": "中共牡丹江市东安区委员会",
        "source": "https://www.donganqu.gov.cn/mdjdaqrmzf/c102959/202310/c03_409641.shtml"
    },
    # ── 核心:区委副书记、区长 ──
    {
        "id": 2, "name": "艾磊", "gender": "男", "ethnicity": "汉族",
        "birth": "1981年10月", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安区委副书记、区长", "current_org": "牡丹江市东安区人民政府",
        "source": "https://www.donganqu.gov.cn/mjsdaqrmzf/c102961/202502/c03_994617.shtml"
    },
    # ── 东安区委领导(11届区委常委会) ──
    {
        "id": 3, "name": "邱海涛", "gender": "男", "ethnicity": "汉族",
        "birth": "1977年9月", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安区委常委", "current_org": "中共牡丹江市东安区委员会",
        "source": "https://www.donganqu.gov.cn/mdjdaqrmzf/c102959/202310/c03_409624.shtml"
    },
    {
        "id": 4, "name": "李博峰", "gender": "男", "ethnicity": "",
        "birth": "1982年1月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安区委常委", "current_org": "中共牡丹江市东安区委员会",
        "source": "https://www.donganqu.gov.cn/mdjdaqrmzf/c102959/202606/c03_1051010.shtml"
    },
    {
        "id": 5, "name": "王铁男", "gender": "男", "ethnicity": "汉族",
        "birth": "1987年12月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安区委常委", "current_org": "中共牡丹江市东安区委员会",
        "source": "https://www.donganqu.gov.cn/mdjdaqrmzf/c102959/202602/c03_1037395.shtml"
    },
    {
        "id": 6, "name": "于玲玲", "gender": "女", "ethnicity": "汉族",
        "birth": "1985年1月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安区委常委", "current_org": "中共牡丹江市东安区委员会",
        "source": "https://www.donganqu.gov.cn/mdjdaqrmzf/c102959/202606/c03_1051124.shtml"
    },
    {
        "id": 7, "name": "于谱海", "gender": "男", "ethnicity": "汉族",
        "birth": "1976年2月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安区委常委", "current_org": "中共牡丹江市东安区委员会",
        "source": "https://www.donganqu.gov.cn/mdjdaqrmzf/c102959/202606/c03_1051133.shtml"
    },
    # ── 区政府副区长(兼区委常委/副区长) ──
    {
        "id": 8, "name": "柳青杨", "gender": "女", "ethnicity": "汉族",
        "birth": "1975年7月", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安区副区长", "current_org": "牡丹江市东安区人民政府",
        "source": "https://www.donganqu.gov.cn/mdjdaqrmzf/c102961/202512/c03_1030654.shtml"
    },
    {
        "id": 9, "name": "褚磊", "gender": "男", "ethnicity": "汉族",
        "birth": "1986年10月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安区副区长", "current_org": "牡丹江市东安区人民政府",
        "source": "https://www.donganqu.gov.cn/mdjdaqrmzf/c102961/202606/c03_1051013.shtml"
    },
    {
        "id": 10, "name": "梁光玉", "gender": "男", "ethnicity": "汉族",
        "birth": "1968年6月", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安区副区长", "current_org": "牡丹江市东安区人民政府",
        "source": "https://www.donganqu.gov.cn/mdjdaqrmzf/c102961/202110/c03_409606.shtml"
    },
    {
        "id": 11, "name": "嵇慧斌", "gender": "男", "ethnicity": "汉族",
        "birth": "1974年4月", "birthplace": "", "education": "省委党校研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安区副区长", "current_org": "牡丹江市东安区人民政府",
        "source": "https://www.donganqu.gov.cn/mdjdaqrmzf/c102961/202501/c03_989296.shtml"
    },
    {
        "id": 12, "name": "赵捃凯", "gender": "男", "ethnicity": "汉族",
        "birth": "1989年9月", "birthplace": "", "education": "研究生学历，工学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安区副区长", "current_org": "牡丹江市东安区人民政府",
        "source": "https://www.donganqu.gov.cn/mdjdaqrmzf/c102961/202602/c03_1037398.shtml"
    },
    # ── 区人大常委会 ──
    {
        "id": 13, "name": "沙士伟", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "东安区人大常委会主任", "current_org": "牡丹江市东安区人民代表大会常务委员会",
        "source": "https://www.donganqu.gov.cn/mdjdaqrmzf/c102960/202310/c03_409618.shtml"
    },
    {
        "id": 14, "name": "王瑶", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "东安区人大常委会副主任", "current_org": "牡丹江市东安区人民代表大会常务委员会",
        "source": "https://www.donganqu.gov.cn/mdjdaqrmzf/c102960/201901/c03_409784.shtml"
    },
    # ── 区政协 ──
    {
        "id": 15, "name": "王丽华", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "东安区政协主席", "current_org": "政协牡丹江市东安区委员会",
        "source": "https://www.donganqu.gov.cn/mdjdaqrmzf/c102962/202112/c03_409749.shtml"
    },
    # ── 前任区长 ──
    {
        "id": 16, "name": "王树军", "gender": "男", "ethnicity": "蒙古族",
        "birth": "1977年1月", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任区长 (2025年区委副书记、代区长→区长, 2026年离任)",
        "current_org": "牡丹江市东安区人民政府",
        "source": "https://mp.weixin.qq.com/s/p5HAfiPvtGvhhOEAfAxjKA"
    },
]

organizations = [
    {"id": 1, "name": "中共牡丹江市东安区委员会", "type": "党委", "level": "县处级", "parent": "中共牡丹江市委", "location": "黑龙江省牡丹江市东安区"},
    {"id": 2, "name": "牡丹江市东安区人民政府", "type": "政府", "level": "县处级", "parent": "牡丹江市人民政府", "location": "黑龙江省牡丹江市东安区"},
    {"id": 3, "name": "牡丹江市东安区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "牡丹江市人民代表大会常务委员会", "location": "黑龙江省牡丹江市东安区"},
    {"id": 4, "name": "政协牡丹江市东安区委员会", "type": "政协", "level": "县处级", "parent": "政协牡丹江市委员会", "location": "黑龙江省牡丹江市东安区"},
]

positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026-01-06 区委十一届十次全会由林坤主持并作报告; 领导简介首页排名第一"},
    # 区长
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "官方领导简介显示'区委副书记、区长：艾磊'"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    ]

positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026-01 区委全会作工作报告"},
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "官方确认"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]
for pid, org, title in [
    (3, 1, "区委常委"), (4, 1, "区委常委"), (5, 1, "区委常委"),
    (6, 1, "区委常委"), (7, 1, "区委常委"),
    (8, 2, "副区长"), (9, 2, "副区长"), (10, 2, "副区长"),
    (11, 2, "副区长"), (12, 2, "副区长"),
    (13, 3, "区人大常委会主任"), (14, 3, "区人大常委会副主任"),
    (15, 4, "区政协主席"), (16, 2, "区长(前任)"),
]:
    positions.append({
        "person_id": pid, "org_id": org, "title": title,
        "start_date": "", "end_date": "present",
        "rank": "县处级副职" if title in ("副区长", "区委常委", "区人大常委会副主任") else "县处级正职",
        "note": "",
    })

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "林坤任区委书记、艾磊任区长, 共同领导东安区工作", "overlap_org": "东安区", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 13, "type": "党政人大协同", "context": "区委书记与区人大常委会主任工作协同", "overlap_org": "东安区", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 16, "type": "接任关系", "context": "王树军为前任区长,后卸任,艾磊接任区长", "overlap_org": "东安区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长与副区长工作关系", "overlap_org": "东安区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长与副区长工作关系", "overlap_org": "东安区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区长与副区长工作关系", "overlap_org": "东安区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长与副区长工作关系", "overlap_org": "东安区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长与副区长工作关系", "overlap_org": "东安区人民政府", "overlap_period": "2026-至今"},
    # 区委班子内部协同
    {"person_a": 1, "person_b": 3, "type": "班子成员", "context": "区委书记与区委常委同班子", "overlap_org": "东安区委", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 6, "type": "班子成员", "context": "区委书记与区委常委同班子", "overlap_org": "东安区委", "overlap_period": "2026-至今"},
]


# ── DATABASE BUILD ─────────────────────────────────────────────────────────

def create_tables(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
        CREATE TABLE persons (
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
            note TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT ''
        );
    """)


def build():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace", "education",
              "party_join", "work_start", "current_post", "current_org", "source"]
    for p in persons:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?'] * len(cols_p))})", vals)

    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?'] * len(cols_o))})", vals)

    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?'] * len(cols_pos))})", vals)

    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?'] * len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────────
    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(post):
        if "区委书记" in post:
            return ("255,50,50", 20.0)
        elif "区长" in post and "副" not in post:
            return ("50,100,255", 20.0)
        elif "人大主任" in post:
            return ("200,255,255", 15.0)
        elif "政协主席" in post:
            return ("255,240,200", 15.0)
        elif "副区长" in post:
            return ("100,100,255", 12.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,255"),
            "政协": ("255,240,200"),
        }.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SHORT} 东安区领导班子关系网络</description>',
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
        lines.append('          <attvalue for="0" value="person"/>')
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
        lines.append('          <attvalue for="0" value="organization"/>')
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
        lines.append('          <attvalue for="0" value="worked_at"/>')
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
    print(f"\n✅ {SHORT} 东安区 数据构建完成。")


if __name__ == "__main__":
    build()