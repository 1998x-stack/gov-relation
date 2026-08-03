#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 范县 leadership network.

调查日期: 2026-08-03
信息来源: 范县人民政府网站 (fanxian.gov.cn), 濮阳市人民政府网站 (puyang.gov.cn)
调查级别: 县
"""

import json
import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "范县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "范县_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-03"
SLUG = "河南省濮阳市范县"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 县委领导 (Party Committee)
    # ═══════════════════════════════

    # 县委书记 — 待查
    {
        "id": 1,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共范县县委书记",
        "current_org": "中共范县委员会",
        "source": "",
    },
    # 王鹏 — 县委副书记、县长
    {
        "id": 2,
        "name": "王鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "范县县委副书记、县长",
        "current_org": "范县人民政府",
        "source": "http://www.fanxian.gov.cn/xxgk/ldls.thtml?cid=16141",
    },
    # 毕孟川 — 县委常委、常务副县长
    {
        "id": 3,
        "name": "毕孟川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "范县县委常委、常务副县长",
        "current_org": "范县人民政府",
        "source": "http://www.fanxian.gov.cn/xxgk/ldls.thtml?cid=16141",
    },
    # 牟艳 — 县委常委、副县长
    {
        "id": 4,
        "name": "牟艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "范县县委常委、副县长",
        "current_org": "范县人民政府",
        "source": "http://www.fanxian.gov.cn/xxgk/ldls.thtml?cid=16141",
    },
    # 周瑞敏 — 县委常委、副县长
    {
        "id": 5,
        "name": "周瑞敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "范县县委常委、副县长",
        "current_org": "范县人民政府",
        "source": "http://www.fanxian.gov.cn/xxgk/ldls.thtml?cid=16141",
    },
    # 党广毅 — 副县长、公安局局长
    {
        "id": 6,
        "name": "党广毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "范县副县长、县公安局局长",
        "current_org": "范县人民政府",
        "source": "http://www.fanxian.gov.cn/xxgk/ldls.thtml?cid=16141",
    },
    # 辛国胜 — 县政府党组成员、副县长
    {
        "id": 7,
        "name": "辛国胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "范县副县长",
        "current_org": "范县人民政府",
        "source": "http://www.fanxian.gov.cn/xxgk/ldls.thtml?cid=16141",
    },
    # 裴中江 — 县政府党组成员、副县长
    {
        "id": 8,
        "name": "裴中江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "范县副县长",
        "current_org": "范县人民政府",
        "source": "http://www.fanxian.gov.cn/xxgk/ldls.thtml?cid=16141",
    },
    # 刘继立 — 县政府党组成员、副县长
    {
        "id": 9,
        "name": "刘继立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "范县副县长",
        "current_org": "范县人民政府",
        "source": "http://www.fanxian.gov.cn/xxgk/ldls.thtml?cid=16141",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共范县委员会", "type": "党委", "level": "县级", "parent": "中共濮阳市委员会", "location": "河南省濮阳市范县"},
    {"id": 2, "name": "范县人民政府", "type": "政府", "level": "县级", "parent": "濮阳市人民政府", "location": "河南省濮阳市范县"},
    {"id": 3, "name": "范县公安局", "type": "政府", "level": "县级", "parent": "范县人民政府", "location": "河南省濮阳市范县"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 县委书记（待查）
    {"person_id": 1, "org_id": 1, "title": "中共范县县委书记",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "范县县委书记信息未从公开渠道获取"},
    # 王鹏
    {"person_id": 2, "org_id": 1, "title": "范县县委副书记",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "同时任县政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "范县县长（代理县长）",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "主持县政府全面工作，负责审计方面工作；2026年7月前任命为代理县长"},
    # 毕孟川
    {"person_id": 3, "org_id": 1, "title": "范县县委常委",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "范县常务副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "负责县政府常务工作，分管发展改革、财政税务、开发区建设、人社、统计、营商环境等"},
    # 牟艳
    {"person_id": 4, "org_id": 1, "title": "范县县委常委",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "范县副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "分管民政、供销、残疾人事业、烟草、金融、保险等"},
    # 周瑞敏
    {"person_id": 5, "org_id": 1, "title": "范县县委常委",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "范县副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "分管农业农村、水利、生态环境、脱贫攻坚成果巩固等"},
    # 党广毅
    {"person_id": 6, "org_id": 2, "title": "范县副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "兼任县公安局局长"},
    {"person_id": 6, "org_id": 3, "title": "范县公安局局长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "分管公安、司法、信访维稳等"},
    # 辛国胜
    {"person_id": 7, "org_id": 2, "title": "范县副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "分管住房和城乡建设、自然资源、城市管理等"},
    # 裴中江
    {"person_id": 8, "org_id": 2, "title": "范县副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "分管工业和信息化、交通运输、商务、招商引资、退役军人事务等"},
    # 刘继立
    {"person_id": 9, "org_id": 2, "title": "范县副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "分管文化广电体育旅游、科技创新、教育、卫生健康、医疗保障、市场监管等"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 县长 ↔ 常务副县长
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "县长与常务副县长党政工作搭档关系，毕孟川协助王鹏分管县政府日常工作",
     "overlap_org": "范县人民政府", "overlap_period": ""},
    # 县长 ↔ 县委常委/副县长 牟艳
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "县长与牟艳——县委常委会共事",
     "overlap_org": "中共范县委员会", "overlap_period": ""},
    # 县长 ↔ 县委常委/副县长 周瑞敏
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "县长与周瑞敏——县委常委会共事",
     "overlap_org": "中共范县委员会", "overlap_period": ""},
    # 常务副县长 ↔ 牟艳
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "常务副县长与牟艳——县政府领导班子成员",
     "overlap_org": "范县人民政府", "overlap_period": ""},
    # 常务副县长 ↔ 周瑞敏
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "常务副县长与周瑞敏——县政府领导班子成员",
     "overlap_org": "范县人民政府", "overlap_period": ""},
    # 常务副县长 ↔ 党广毅
    {"person_a": 3, "person_b": 6, "type": "overlap",
     "context": "常务副县长与党广毅——县政府领导班子成员，毕孟川协助县长分管应急管理",
     "overlap_org": "范县人民政府", "overlap_period": ""},
    # 党广毅 ↔ 王鹏
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "县长与公安局长——王鹏主持县政府全面工作，党广毅为副县长",
     "overlap_org": "范县人民政府", "overlap_period": ""},
    # 其他副县长间的同事关系
    {"person_a": 7, "person_b": 8, "type": "overlap",
     "context": "辛国胜与裴中江——同为县政府党组成员",
     "overlap_org": "范县人民政府", "overlap_period": ""},
    {"person_a": 8, "person_b": 9, "type": "overlap",
     "context": "裴中江与刘继立——同为县政府党组成员",
     "overlap_org": "范县人民政府", "overlap_period": ""},
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
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 范县人民政府网站 (fanxian.gov.cn)")
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
        if "书记" in post and "县委" in post and "副" not in post:
            return ("255,50,50", 20.0)  # Red, top leader
        elif "县长" in post and "副" not in post:
            return ("50,100,255", 20.0)  # Blue
        elif "常务" in post:
            return ("50,100,255", 15.0)
        elif "副书记" in post:
            return ("100,100,255", 15.0)  # Deputy secretary
        elif "县委常委" in post:
            return ("50,100,255", 12.0)
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
        f'    <description>{SLUG} 领导班子关系网络 — 截至{AS_OF}</description>',
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
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    # person → org edges
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o_{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
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
        {"id": "S001", "title": "范县人民政府领导之窗",
         "url": "http://www.fanxian.gov.cn/xxgk/ldls.thtml?cid=16141",
         "publisher": "范县人民政府", "published_at": "2026-07-04",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认王鹏为县委副书记、县长（代理县长）；确认毕孟川、牟艳、周瑞敏为县委常委、副县长"},
        {"id": "S002", "title": "范县人民政府门户网站首页",
         "url": "http://www.fanxian.gov.cn/",
         "publisher": "范县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "首页显示王鹏为县长，照片更新于2026-07-04"},
        {"id": "S003", "title": "濮阳市人民政府网站",
         "url": "https://www.puyang.gov.cn/",
         "publisher": "濮阳市人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "搜索'范县'获得近半年新闻确认当前领导班子"},
        {"id": "S004", "title": "范县公安局",
         "url": "http://www.fanxian.gov.cn/xxgk/ldls.thtml?cid=16141",
         "publisher": "范县人民政府", "published_at": "2026-07-04",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认党广毅为副县长、县公安局局长"},
    ]


def make_person_json(person, timeline, rels, source_reg):
    """Build a person graph JSON following the V1 schema."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "濮阳市",
            "region": "范县",
            "job": person["current_post"],
            "task_id": "henan_范县",
            "time_focus": "截至2026年7-8月"
        },
        "identity": {
            "person_id": f"fanxian_{person['name']}",
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
            "administrative_rank": "正处级" if "书记" in person["current_post"] or ("县长" in person["current_post"] and "副" not in person["current_post"]) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至{AS_OF}，公开渠道未发现{person['name']}的负面信号",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": source_reg,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{person['name']}的出生年份、籍贯、教育背景和任现职前的全部履历均缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}任{person['current_post']}前的完整履历是什么？",
                "why_it_matters": "无法评估其职业路径、来源系统和晋升模式",
                "suggested_queries": [f"{person['name']} 简历 范县", f"{person['name']} 任前公示", f"{person['name']} Baidu Baike"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年份、籍贯、教育背景是什么？",
                "why_it_matters": "缺少基础身份信息，无法进行去重和人口统计分析",
                "suggested_queries": [f"{person['name']} 出生", f"{person['name']} 濮阳"],
                "last_attempted": AS_OF,
            },
        ],
    }


if __name__ == "__main__":
    run_build()

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 王鹏 (县长)
    wangp_timeline = [
        {"start": "2026年", "end": "至今", "org": "范县人民政府",
         "title": "范县县委副书记、县长（代理县长）",
         "notes": "主持县政府全面工作，负责审计方面工作。分管县审计局。",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    wangp_rels = [
        {"person": "毕孟川", "person_id": "fanxian_毕孟川",
         "relationship_type": "superior_subordinate", "strength": "strong",
         "evidence": "县长与常务副县长——毕孟川协助王鹏负责县政府常务工作",
         "overlap_org": "范县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "牟艳", "person_id": "fanxian_牟艳",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "县长与县委常委、副县长牟艳——在县委常委会和县政府领导班子共事",
         "overlap_org": "中共范县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "周瑞敏", "person_id": "fanxian_周瑞敏",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "县长与县委常委、副县长周瑞敏——在县委常委会和县政府领导班子共事",
         "overlap_org": "中共范县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    wangp_json = make_person_json(persons[1], wangp_timeline, wangp_rels, source_register)
    wangp_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-濮阳市-县长-王鹏.json")
    with open(wangp_path, "w", encoding="utf-8") as f:
        json.dump(wangp_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(wangp_path)}")

    # 毕孟川 (常务副县长)
    bimc_timeline = [
        {"start": "", "end": "至今", "org": "范县人民政府",
         "title": "范县县委常委、常务副县长",
         "notes": "负责县政府常务工作，分管经济运行、发展改革、财政税务、开发区建设、人力资源社会保障、统计、营商环境等",
         "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    bimc_rels = [
        {"person": "王鹏", "person_id": "fanxian_王鹏",
         "relationship_type": "superior_subordinate", "strength": "strong",
         "evidence": "常务副县长协助县长王鹏工作",
         "overlap_org": "范县人民政府", "overlap_period": "",
         "direction": "other_to_person", "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "牟艳", "person_id": "fanxian_牟艳",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "常务副县长与牟艳——县政府领导班子成员",
         "overlap_org": "范县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    bimc_json = make_person_json(persons[2], bimc_timeline, bimc_rels, source_register)
    bimc_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-濮阳市-常务副县长-毕孟川.json")
    with open(bimc_path, "w", encoding="utf-8") as f:
        json.dump(bimc_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(bimc_path)}")

    # 党广毅 (副县长、公安局长)
    dang_timeline = [
        {"start": "", "end": "至今", "org": "范县人民政府",
         "title": "范县副县长、县公安局局长",
         "notes": "分管公安、司法、信访维稳等工作",
         "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    dang_rels = [
        {"person": "王鹏", "person_id": "fanxian_王鹏",
         "relationship_type": "superior_subordinate", "strength": "medium",
         "evidence": "党广毅为副县长，在县政府领导班子中受县长领导",
         "overlap_org": "范县人民政府", "overlap_period": "",
         "direction": "other_to_person", "confidence": "confirmed",
         "source_ids": ["S001", "S004"]},
    ]
    dang_json = make_person_json(persons[5], dang_timeline, dang_rels, source_register)
    dang_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-濮阳市-公安局局长-党广毅.json")
    with open(dang_path, "w", encoding="utf-8") as f:
        json.dump(dang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(dang_path)}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")