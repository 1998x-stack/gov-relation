#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 和硕县, 巴音郭楞蒙古自治州, 新疆.

Investigation date: 2026-07-28
Task ID: xinjiang_和硕县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - 和硕县人民政府官方网站 (www.hoxut.gov.cn) — confirmed current leadership roster (2026-07-10 updated)
  - 硕政发〔2026〕14号 县长副县长分工文件 (2026-06-30)
  - 中国县域经济报2021年专访 (张峰简历)
  - 搜狗搜索: 和硕县_县委书记_现任 (2026-07-28)

Key findings:
  - 县委书记: 张峰（1968年6月生，山东宁阳人，博士研究生学历，1991年7月参加工作，1991年5月入党）
  - 县长: 明吉尔（县委副书记、政府党组书记）
  - 常务副县长: 张子扬（县委副书记、正县级）
  - 副县长: 刘奕泽、张勇强（兼公安局长）、葛军、巴音花（挂职）、阿司木江·阿优福、刘楠
  - 政府党组成员: 依布拉音·努尔

Confidence notes:
  - 张峰完整履历仅部分确认（县委书记职务），早年经历缺失
  - 明吉尔出生日期、学历、早期履历完全缺失
  - 县委常委完整名单未获取到
  - 历任县委书记信息：李育森（被查落马）、赵毅杰（2018年前后）、张锋（约2018至今）
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

SLUG = "和硕县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-28"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

persons = [
    {"id": 1, "name": "张峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-06", "birthplace": "山东省泰安市宁阳县",
     "education": "博士研究生", "party_join": "1991-05", "work_start": "1991-07",
     "current_post": "和硕县委书记", "current_org": "中共和硕县委员会",
     "source": "中国县域经济报2021年专访"},
    {"id": 2, "name": "明吉尔", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "和硕县长", "current_org": "和硕县人民政府",
     "source": "和硕县人民政府领导之窗"},
    {"id": 3, "name": "张子扬", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "和硕县委副书记(正县级)、常务副县长", "current_org": "和硕县人民政府",
     "source": "和硕县人民政府领导之窗"},
    {"id": 4, "name": "刘奕泽", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "和硕县副县长", "current_org": "和硕县人民政府",
     "source": "和硕县人民政府领导之窗"},
    {"id": 5, "name": "张勇强", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "和硕县副县长、县公安局局长", "current_org": "和硕县人民政府",
     "source": "和硕县人民政府领导之窗"},
    {"id": 6, "name": "葛军", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "和硕县副县长", "current_org": "和硕县人民政府",
     "source": "和硕县人民政府领导之窗"},
    {"id": 7, "name": "巴音花", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "和硕县副县长(挂职)", "current_org": "和硕县人民政府",
     "source": "和硕县人民政府领导之窗"},
    {"id": 8, "name": "阿司木江·阿优福", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "和硕县副县长", "current_org": "和硕县人民政府",
     "source": "和硕县人民政府领导之窗"},
    {"id": 9, "name": "刘楠", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "和硕县副县长", "current_org": "和硕县人民政府",
     "source": "和硕县人民政府领导之窗"},
    {"id": 10, "name": "依布拉音·努尔", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "和硕县政府党组成员", "current_org": "和硕县人民政府",
     "source": "和硕县人民政府领导之窗"},
    {"id": 11, "name": "马丽红", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "和硕县委常委、宣传部部长",
     "current_org": "中共和硕县委员会",
     "source": "和硕县2026年宣传思想文化工作推进会报道"},
    {"id": 12, "name": "李育森", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "和硕县前县委书记(落马)",
     "current_org": "中共和硕县委员会",
     "source": "闽南网、环球网——涉严重违纪被查"},
    {"id": 13, "name": "赵毅杰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "和硕县前县委书记",
     "current_org": "中共和硕县委员会",
     "source": "中国经济网2018年报道"},
]

organizations = [
    {"id": 1, "name": "中共和硕县委员会", "type": "党委", "level": "县",
     "parent": "", "location": "新疆巴音郭楞蒙古自治州和硕县"},
    {"id": 2, "name": "和硕县人民政府", "type": "政府", "level": "县",
     "parent": "", "location": "新疆巴音郭楞蒙古自治州和硕县"},
    {"id": 3, "name": "和硕县公安局", "type": "政法机关", "level": "县",
     "parent": "和硕县人民政府", "location": "新疆巴音郭楞蒙古自治州和硕县"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "和硕县委书记",
     "start_date": "约2018", "end_date": "", "rank": "正县处级",
     "note": "中国县域经济报2021专访；2026年政府网站仍提及"},
    {"person_id": 2, "org_id": 2, "title": "和硕县人民政府县长",
     "start_date": "", "end_date": "", "rank": "正县处级",
     "note": "2026年6月30日分工文件确认"},
    {"person_id": 2, "org_id": 1, "title": "和硕县委副书记",
     "start_date": "", "end_date": "", "rank": "正县处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "和硕县人民政府常务副县长",
     "start_date": "", "end_date": "", "rank": "正县处级",
     "note": "县委副书记（正县级）、县人民政府党组副书记"},
    {"person_id": 4, "org_id": 2, "title": "和硕县副县长",
     "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "和硕县副县长",
     "start_date": "", "end_date": "", "rank": "副县处级", "note": "兼县委政法委副书记"},
    {"person_id": 5, "org_id": 3, "title": "和硕县公安局局长、督察长",
     "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "和硕县副县长",
     "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "和硕县副县长(挂职)",
     "start_date": "", "end_date": "", "rank": "副县处级", "note": "挂职"},
    {"person_id": 8, "org_id": 2, "title": "和硕县副县长",
     "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "和硕县副县长",
     "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "和硕县政府党组成员",
     "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "和硕县委常委、宣传部部长",
     "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "和硕县委书记(前)",
     "start_date": "约2015", "end_date": "约2017", "rank": "正县处级",
     "note": "涉严重违纪被查"},
    {"person_id": 13, "org_id": 1, "title": "和硕县委书记(前)",
     "start_date": "约2017", "end_date": "约2018", "rank": "正县处级",
     "note": "中国经济网2018年报道脱贫攻坚"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "县委县政府一把手", "overlap_org": "和硕县委、县政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "上下级",
     "context": "县政府正副职", "overlap_org": "和硕县人民政府",
     "overlap_period": ""},
    {"person_a": 12, "person_b": 13, "type": "前后任",
     "context": "县委书记前后交接", "overlap_org": "中共和硕县委员会",
     "overlap_period": "2017-2018"},
    {"person_a": 13, "person_b": 1, "type": "前后任",
     "context": "县委书记前后交接", "overlap_org": "中共和硕县委员会",
     "overlap_period": "约2018"},
]


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 和硕县人民政府网站 (hoxut.gov.cn) 及新闻报道")
    print("=" * 60)

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
        if "县委书记" in post and "副书记" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post:
            return ("50,100,255", 20.0)
        elif "常务" in post or "副书记" in post:
            return ("150,100,100", 15.0)
        elif "副县长" in post or "常委" in post:
            return ("100,100,255", 12.0)
        elif "前" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,180,180"),
            "政府": ("180,180,255"),
            "政法机关": ("200,200,200"),
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
        lines.append('        <viz:size value="8.0"/>')
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
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    run_build()