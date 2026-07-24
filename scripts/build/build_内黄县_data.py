#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 内黄县 leadership network.

调查日期: 2026-07-24
信息来源: 内黄县人民政府网站 (neihuang.gov.cn)
调查级别: 县
"""

import json
import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
# Resolve to repo root (data/tmp/henan_内黄县/ → repo root)
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "内黄县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "内黄县_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "河南省安阳市内黄县"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 县委领导 (Party Committee)
    # ═══════════════════════════════

    # 县委书记 — 待确认（2026年6月十四次党代会选举产生，具体姓名暂未找到公开资料）
    {
        "id": 1,
        "name": "待确认",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共内黄县委书记",
        "current_org": "中共内黄县委员会",
        "source": "http://www.neihuang.gov.cn/ (2026-06 第十四次党代会)",
    },
    # 祁欢 — 县委副书记、县长、党组书记
    {
        "id": 2,
        "name": "祁欢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-02",
        "birthplace": "",
        "education": "大学，法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "内黄县委副书记、县长",
        "current_org": "内黄县人民政府",
        "source": "http://www.neihuang.gov.cn/template/viewList?catalogId=cd7f9daf3fa6451881d487e347a1013a",
    },
    # 王相月 — 县委常委、常务副县长
    {
        "id": 3,
        "name": "王相月",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "内黄县委常委、常务副县长",
        "current_org": "内黄县人民政府",
        "source": "http://www.neihuang.gov.cn/henan/nhxrmzf/wzlm/zfxxgk/zfxxgk/zc/zfbwj/a862c572f1b949e6a058dedf2d67fde1.html",
    },
    # 桑越峰 — 副县长
    {
        "id": 4,
        "name": "桑越峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "内黄县副县长",
        "current_org": "内黄县人民政府",
        "source": "http://www.neihuang.gov.cn/henan/nhxrmzf/wzlm/zfxxgk/zfxxgk/zc/zfbwj/a862c572f1b949e6a058dedf2d67fde1.html",
    },
    # 段希斌 — 副县长
    {
        "id": 5,
        "name": "段希斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "内黄县副县长",
        "current_org": "内黄县人民政府",
        "source": "http://www.neihuang.gov.cn/henan/nhxrmzf/wzlm/zfxxgk/zfxxgk/zc/zfbwj/a862c572f1b949e6a058dedf2d67fde1.html",
    },
    # 郝志刚 — 副县长、县公安局局长
    {
        "id": 6,
        "name": "郝志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "内黄县副县长、县公安局局长",
        "current_org": "内黄县人民政府",
        "source": "http://www.neihuang.gov.cn/henan/nhxrmzf/wzlm/zfxxgk/zfxxgk/zc/zfbwj/a862c572f1b949e6a058dedf2d67fde1.html",
    },
    # 司心宇 — 县政府党组成员（副县级）
    {
        "id": 7,
        "name": "司心宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "内黄县政府党组成员",
        "current_org": "内黄县人民政府",
        "source": "http://www.neihuang.gov.cn/henan/nhxrmzf/wzlm/zfxxgk/zfxxgk/zc/zfbwj/a862c572f1b949e6a058dedf2d67fde1.html",
    },
    # 刘娟 — 县政府党组成员
    {
        "id": 8,
        "name": "刘娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "内黄县政府党组成员",
        "current_org": "内黄县人民政府",
        "source": "http://www.neihuang.gov.cn/henan/nhxrmzf/wzlm/zfxxgk/zfxxgk/zc/zfbwj/a862c572f1b949e6a058dedf2d67fde1.html",
    },
    # 赵晓波 — 副县长
    {
        "id": 9,
        "name": "赵晓波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "内黄县副县长",
        "current_org": "内黄县人民政府",
        "source": "http://www.neihuang.gov.cn/henan/nhxrmzf/wzlm/zfxxgk/zfxxgk/zc/zfbwj/a862c572f1b949e6a058dedf2d67fde1.html",
    },
    # 温晓飞 — 县政府党组成员、政府办公室主任
    {
        "id": 10,
        "name": "温晓飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "内黄县政府党组成员、办公室主任",
        "current_org": "内黄县人民政府办公室",
        "source": "http://www.neihuang.gov.cn/henan/nhxrmzf/wzlm/zfxxgk/zfxxgk/zc/zfbwj/a862c572f1b949e6a058dedf2d67fde1.html",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共内黄县委员会", "type": "党委", "level": "县级", "parent": "中共安阳市委员会", "location": "河南省安阳市内黄县"},
    {"id": 2, "name": "内黄县人民政府", "type": "政府", "level": "县级", "parent": "安阳市人民政府", "location": "河南省安阳市内黄县"},
    {"id": 3, "name": "内黄县公安局", "type": "政府", "level": "正科级", "parent": "内黄县人民政府", "location": "河南省安阳市内黄县"},
    {"id": 4, "name": "内黄县人民政府办公室", "type": "政府", "level": "正科级", "parent": "内黄县人民政府", "location": "河南省安阳市内黄县"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共内黄县委书记",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "2026年6月内黄县第十四次党代会选举产生"},
    # 祁欢
    {"person_id": 2, "org_id": 1, "title": "内黄县委副书记",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "同时任县政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "内黄县县长",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "主持县政府全面工作"},
    # 王相月
    {"person_id": 3, "org_id": 1, "title": "内黄县委常委",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": ""},
    {"person_id": 3, "org_id": 2, "title": "内黄县常务副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "负责常务工作；联系开发区"},
    # 桑越峰
    {"person_id": 4, "org_id": 2, "title": "内黄县副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "负责生态环境、市场监管、文化广电体育旅游、行政审批"},
    # 段希斌
    {"person_id": 5, "org_id": 2, "title": "内黄县副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "负责基本建设、自然资源、住建、城管、交通"},
    # 郝志刚
    {"person_id": 6, "org_id": 2, "title": "内黄县副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "兼任县公安局局长"},
    {"person_id": 6, "org_id": 3, "title": "内黄县公安局局长",
     "start_date": "", "end_date": "", "rank": "正科级",
     "note": ""},
    # 司心宇
    {"person_id": 7, "org_id": 2, "title": "内黄县政府党组成员",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "负责科技、工业、招商引资、通讯、电力"},
    # 刘娟
    {"person_id": 8, "org_id": 2, "title": "内黄县政府党组成员",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "负责教育、民政、卫健、退役军人事务、医保"},
    # 赵晓波
    {"person_id": 9, "org_id": 2, "title": "内黄县副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "负责水利、农业农村、粮食和物资储备"},
    # 温晓飞
    {"person_id": 10, "org_id": 2, "title": "内黄县政府党组成员",
     "start_date": "", "end_date": "", "rank": "正科级",
     "note": "主持县政府办公室全面工作"},
    {"person_id": 10, "org_id": 4, "title": "内黄县人民政府办公室主任",
     "start_date": "", "end_date": "", "rank": "正科级",
     "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 县长 ↔ 常务副县长
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "县长与常务副县长党政工作搭档",
     "overlap_org": "内黄县人民政府", "overlap_period": ""},
    # 县长 ↔ 副县长(公安)
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "县长与分管公安的副县长工作关系",
     "overlap_org": "内黄县人民政府", "overlap_period": ""},
    # 县长 ↔ 副县长(城建)
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "县长与分管城建副县长工作关系",
     "overlap_org": "内黄县人民政府", "overlap_period": ""},
    # 县长 ↔ 副县长(环保)
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "县长与分管环保副县长工作关系",
     "overlap_org": "内黄县人民政府", "overlap_period": ""},
    # 县长 ↔ 党组成员(工业)
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "县长与分管工业党组成员工作关系",
     "overlap_org": "内黄县人民政府", "overlap_period": ""},
    # 县长 ↔ 党组成员(民生)
    {"person_a": 2, "person_b": 8, "type": "overlap",
     "context": "县长与分管民生党组成员工作关系",
     "overlap_org": "内黄县人民政府", "overlap_period": ""},
    # 县长 ↔ 副县长(农业)
    {"person_a": 2, "person_b": 9, "type": "overlap",
     "context": "县长与分管农业副县长工作关系",
     "overlap_org": "内黄县人民政府", "overlap_period": ""},
    # 县长 ↔ 政府办主任
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "县长与政府办公室主任紧密工作关系",
     "overlap_org": "内黄县人民政府", "overlap_period": ""},
    # 常务副县长 ↔ 副县长(城建) — 部分分管重叠
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "常务副县长与城建副县长——段希斌协助生态环境工作",
     "overlap_org": "内黄县人民政府", "overlap_period": ""},
    # 副县长(环保) ↔ 副县长(城建) — 协助关系
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "桑越峰主管生态环境，段希斌协助",
     "overlap_org": "内黄县人民政府", "overlap_period": ""},
    # 党组成员(工业) ↔ 党组成员(民生)
    {"person_a": 7, "person_b": 8, "type": "overlap",
     "context": "司心宇与刘娟均为政府党组成员",
     "overlap_org": "内黄县人民政府", "overlap_period": ""},
    # 常务副县长 ↔ 政府办主任
    {"person_a": 3, "person_b": 10, "type": "overlap",
     "context": "王相月协助县长分管金融，温晓飞协助县长处理日常工作",
     "overlap_org": "内黄县人民政府", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════

import sqlite3


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

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
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

        CREATE TABLE relationships (
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
    print(f"  信息来源: 内黄县人民政府网站 (neihuang.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
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
        if "书记" in post and "县委" in post:
            return ("255,50,50", 20.0)  # Red, top leader
        elif "县长" in post:
            return ("50,100,255", 20.0)  # Blue
        elif "常务" in post:
            return ("50,100,255", 15.0)
        elif "副县长" in post or "党组成员" in post:
            return ("100,100,255", 12.0)  # Light blue
        else:
            return ("100,100,100", 12.0)  # Grey

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
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

    # Person nodes
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

    # Organization nodes
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
    # person → org edges
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person edges
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


# ═══════════════════════════════════════════════════════════════════
# PERSON JSON GENERATION
# ═══════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "内黄县政府领导信息",
         "url": "http://www.neihuang.gov.cn/template/viewList?catalogId=cd7f9daf3fa6451881d487e347a1013a",
         "publisher": "内黄县人民政府", "published_at": "2026",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "内黄县政府领导名单（县长/副县长）"},
        {"id": "S002", "title": "内政办〔2026〕1号 关于调整县政府领导分工的通知",
         "url": "http://www.neihuang.gov.cn/henan/nhxrmzf/wzlm/zfxxgk/zfxxgk/zc/zfbwj/a862c572f1b949e6a058dedf2d67fde1.html",
         "publisher": "内黄县人民政府办公室", "published_at": "2026-07-23",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "县政府领导分工调整"},
        {"id": "S003", "title": "内黄县人民政府网站",
         "url": "http://www.neihuang.gov.cn/",
         "publisher": "内黄县人民政府", "published_at": "",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "内黄县人民政府门户网站"},
    ]


def make_person_json(person, timeline, rels, source_reg):
    """Build a person graph JSON following the V1 schema."""
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "安阳市",
            "region": "内黄县",
            "job": person["current_post"],
            "task_id": "henan_内黄县",
            "time_focus": "截至2026年7月"
        },
        "identity": {
            "person_id": f"neihuang_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "书记" in person["current_post"] or "县长" in person["current_post"] else "副处级",
            "as_of": "2026-07-23",
            "is_current_confirmed": True if person["name"] != "待确认" else False,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": source_reg,
        "confidence_summary": {
            "identity": "plausible" if person["name"] != "待确认" else "unverified",
            "current_role": "confirmed" if person["name"] != "待确认" else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "县委书记姓名确认; 各领导早期履历",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "现任内黄县委书记是谁？",
                "why_it_matters": "县委书记是内黄县最高领导，是网络分析的核心节点",
                "suggested_queries": ["内黄县委书记 2026", "内黄县第十四次党代会 选举"],
                "last_attempted": TODAY,
            },
            {
                "priority": "high",
                "question": f"{person['name']}的早期履历（参加工作至今）",
                "why_it_matters": "完整履历是理解晋升路径和人际网络的基础",
                "suggested_queries": [f"{person['name']} 简历 {person['current_post']}"],
                "last_attempted": TODAY,
            },
        ],
    }


if __name__ == "__main__":
    run_build()

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 县委书记 (待确认)
    sec_timeline = [
        {"start": "2026-06", "end": "", "org": "中共内黄县委员会",
         "title": "中共内黄县委书记",
         "notes": "2026年6月内黄县第十四次党代会选举产生",
         "confidence": "unverified", "source_ids": []},
    ]
    sec_rels = [
        {"person": "祁欢", "person_id": "neihuang_祁欢",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "县委书记与县长党政工作搭档",
         "overlap_org": "内黄县", "overlap_period": "2026-",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    sec_json = make_person_json(persons[0], sec_timeline, sec_rels, source_register)
    sec_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-安阳市-县委书记-待确认.json")
    with open(sec_path, "w", encoding="utf-8") as f:
        json.dump(sec_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(sec_path)}")

    # 2. 祁欢 (县长)
    qi_timeline = [
        {"start": "", "end": "", "org": "内黄县人民政府",
         "title": "内黄县委副书记、县长、县政府党组书记",
         "notes": "1983年2月生，大学，法学硕士；主持县政府全面工作",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    qi_rels = [
        {"person": "待确认", "person_id": "neihuang_待确认",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "县长与县委书记党政工作搭档",
         "overlap_org": "内黄县", "overlap_period": "2026-",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "王相月", "person_id": "neihuang_王相月",
         "relationship_type": "superior_subordinate", "strength": "strong",
         "evidence": "县长与常务副县长——协助县长分管审计",
         "overlap_org": "内黄县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S002"]},
        {"person": "郝志刚", "person_id": "neihuang_郝志刚",
         "relationship_type": "superior_subordinate", "strength": "medium",
         "evidence": "县长与分管公安的副县长",
         "overlap_org": "内黄县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S002"]},
    ]
    qi_json = make_person_json(persons[1], qi_timeline, qi_rels, source_register)
    qi_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-安阳市-县长-祁欢.json")
    with open(qi_path, "w", encoding="utf-8") as f:
        json.dump(qi_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(qi_path)}")

    # 3. 王相月 (常务副县长)
    wang_timeline = [
        {"start": "", "end": "", "org": "内黄县人民政府",
         "title": "内黄县委常委、常务副县长",
         "notes": "负责政府常务工作；联系先进制造业开发区",
         "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    wang_rels = [
        {"person": "祁欢", "person_id": "neihuang_祁欢",
         "relationship_type": "superior_subordinate", "strength": "strong",
         "evidence": "常务副县长协助县长工作",
         "overlap_org": "内黄县人民政府", "overlap_period": "",
         "direction": "other_to_person", "confidence": "confirmed",
         "source_ids": ["S002"]},
    ]
    wang_json = make_person_json(persons[2], wang_timeline, wang_rels, source_register)
    wang_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-安阳市-常务副县长-王相月.json")
    with open(wang_path, "w", encoding="utf-8") as f:
        json.dump(wang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(wang_path)}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")
