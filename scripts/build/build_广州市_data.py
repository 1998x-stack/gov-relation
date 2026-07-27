#!/usr/bin/env python3
"""
广州市领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Guangzhou City leadership network.

Level: 地级市 (副省级城市)
Province: 广东省
Region: 广州市
Targets: 市委书记 & 市长

Research Sources:
- Wikipedia (zh.wikipedia.org) — 广州市市长列表, 冯忠华, 孙志洋, 郭永航
- 人民网 — 地方领导资料
- 南方日报 / 南方+ — 任免公告
- 中国经济网 — 人事报道

Research Date: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "广州市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "广州市_network.gexf")

# ── DATA ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════
    {
        "id": "p01",
        "name": "冯忠华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年5月",
        "birthplace": "辽宁丹东",
        "native_place": "辽宁丹东",
        "education": "大学(合肥工业大学资源与环境科学系环境工程专业)/工程硕士(清华大学建筑学院建筑与土木工程)",
        "party_join": "中共党员(1992年加入)",
        "work_start": "1993年7月",
        "current_post": "广东省委常委、广州市委书记",
        "current_org": "中共广州市委员会",
        "source": "Wikipedia: 冯忠华; 人民网: 冯忠华简历; 南方日报: 任广州市委书记报道",
        "person_id": "guangzhou_feng_zhonghua"
    },
    {
        "id": "p02",
        "name": "孙志洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年5月",
        "birthplace": "吉林扶余",
        "native_place": "吉林扶余",
        "education": "大学(吉林工业大学汽车拖拉机专业)/工商管理硕士(吉林大学)",
        "party_join": "中共党员(1992年10月加入)",
        "work_start": "1997年7月",
        "current_post": "广州市委副书记、市长",
        "current_org": "广州市人民政府",
        "source": "Wikipedia: 孙志洋; 新华社; 南方日报",
        "person_id": "guangzhou_sun_zhiyang"
    },
    # ════════════════════════════════════════
    # Previous Leadership (for context)
    # ════════════════════════════════════════
    {
        "id": "p03",
        "name": "郭永航",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年10月",
        "birthplace": "山东济阳",
        "native_place": "山东济阳",
        "education": "大学(武汉大学历史系)/管理学博士(武汉大学行政管理在职)",
        "party_join": "中共党员(1986年6月加入)",
        "work_start": "1989年7月",
        "current_post": "广东省政协副主席(被调查)",
        "current_org": "广东省政协",
        "source": "Wikipedia: 郭永航; 中央纪委国家监委网站",
        "person_id": "guangzhou_guo_yonghang"
    },
    {
        "id": "p04",
        "name": "林克庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年10月",
        "birthplace": "湖北仙桃",
        "native_place": "湖北仙桃",
        "education": "大学(中国人民大学哲学)/在职研究生",
        "party_join": "中共党员",
        "work_start": "1988年8月",
        "current_post": "广东省政协主席",
        "current_org": "广东省政协",
        "source": "Wikipedia: 林克庆; 中国经济网",
        "person_id": "guangzhou_lin_keqing"
    },
    # ════════════════════════════════════════
    # Key Deputy Leaders
    # ════════════════════════════════════════
    {
        "id": "p05",
        "name": "陈国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广州市委副书记",
        "current_org": "中共广州市委员会",
        "source": "广州日报",
        "person_id": "guangzhou_chen_guo"
    },
    {
        "id": "p06",
        "name": "杨飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广州市委常委、市纪委书记",
        "current_org": "中共广州市纪律检查委员会",
        "source": "广州日报",
        "person_id": "guangzhou_yang_fei"
    },
    # ════════════════════════════════════════
    # Previous Mayors / Secretaries for Relationship Context
    # ════════════════════════════════════════
    {
        "id": "p07",
        "name": "温国辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年10月",
        "birthplace": "广东揭西",
        "native_place": "广东揭西",
        "education": "大学(华南理工大学)/在职研究生",
        "party_join": "中共党员",
        "work_start": "1984年7月",
        "current_post": "广东省政协副主席",
        "current_org": "广东省政协",
        "source": "Wikipedia: 温国辉",
        "person_id": "guangzhou_wen_guohui"
    },
]

# 2. Organizations
organizations = [
    {"id": "o01", "name": "中共广州市委员会", "type": "党委", "level": "副省级", "location": "广州市"},
    {"id": "o02", "name": "广州市人民政府", "type": "政府", "level": "副省级", "location": "广州市"},
    {"id": "o03", "name": "中共广东省委员会", "type": "党委", "level": "省级", "location": "广州市"},
    {"id": "o04", "name": "广东省人民政府", "type": "政府", "level": "省级", "location": "广州市"},
    {"id": "o05", "name": "广东省政协", "type": "政协", "level": "省级", "location": "广州市"},
    {"id": "o06", "name": "中共广州市纪律检查委员会", "type": "党委", "level": "副省级", "location": "广州市"},
    {"id": "o07", "name": "中央纪委国家监委", "type": "党委", "level": "国家级", "location": "北京"},
    {"id": "o08", "name": "中国共产党海南省委员会", "type": "党委", "level": "省级", "location": "海口"},
    {"id": "o09", "name": "海南省人民政府", "type": "政府", "level": "省级", "location": "海口"},
    {"id": "o10", "name": "中华人民共和国住房和城乡建设部", "type": "政府", "level": "国家级", "location": "北京"},
    {"id": "o11", "name": "中共珠海市委员会", "type": "党委", "level": "地厅级", "location": "珠海"},
    {"id": "o12", "name": "珠海市人民政府", "type": "政府", "level": "地厅级", "location": "珠海"},
    {"id": "o13", "name": "中共深圳市委员会", "type": "党委", "level": "副省级", "location": "深圳"},
    {"id": "o14", "name": "深圳市人民政府", "type": "政府", "level": "副省级", "location": "深圳"},
    {"id": "o15", "name": "中国第一汽车集团有限公司", "type": "政府", "level": "国家级", "location": "长春"},
    {"id": "o16", "name": "全国人大常委会", "type": "人大", "level": "国家级", "location": "北京"},
    {"id": "o17", "name": "广州市人大常委会", "type": "人大", "level": "副省级", "location": "广州市"},
    {"id": "o18", "name": "政协广州市委员会", "type": "政协", "level": "副省级", "location": "广州市"},
]

# 3. Positions (Person→Organization)
positions = [
    # 冯忠华
    {"id": "z01", "person_id": "p01", "org_id": "o10", "title": "建设部/住建部干部(综合与法规处处长、城乡规划司副司长等)", "start": "1993", "end": "2015", "rank": ""},
    {"id": "z02", "person_id": "p01", "org_id": "o10", "title": "住建部科技与产业化发展中心主任(正司长级)", "start": "2015", "end": "2016", "rank": "正司级"},
    {"id": "z03", "person_id": "p01", "org_id": "o10", "title": "住建部城乡规划司司长", "start": "2016", "end": "2018", "rank": "正司级"},
    {"id": "z04", "person_id": "p01", "org_id": "o16", "title": "十三届全国人大常委会专职委员、全国人大农业与农村委员会委员", "start": "2018-03", "end": "2019-06", "rank": "正司级"},
    {"id": "z05", "person_id": "p01", "org_id": "o09", "title": "海南省人民政府副省长", "start": "2019-06", "end": "2022-04", "rank": "副省级"},
    {"id": "z06", "person_id": "p01", "org_id": "o08", "title": "海南省委常委、组织部部长", "start": "2022-04", "end": "2024-06", "rank": "副省级"},
    {"id": "z07", "person_id": "p01", "org_id": "o03", "title": "广东省委常委、组织部部长", "start": "2024-06", "end": "2026-06", "rank": "副省级"},
    {"id": "z08", "person_id": "p01", "org_id": "o01", "title": "广东省委常委、广州市委书记", "start": "2025-12-24", "end": "present", "rank": "副省级"},

    # 孙志洋
    {"id": "z09", "person_id": "p02", "org_id": "o15", "title": "中国第一汽车集团干部(长春汽车研究所→一汽规划部、办公厅、发展部)", "start": "1997-07", "end": "2018", "rank": ""},
    {"id": "z10", "person_id": "p02", "org_id": "o15", "title": "中国第一汽车集团副总经理、党委常委", "start": "2018", "end": "2021-03", "rank": "副部级(央企)"},
    {"id": "z11", "person_id": "p02", "org_id": "o04", "title": "广东省人民政府副省长", "start": "2021-03", "end": "2023-11", "rank": "副省级"},
    {"id": "z12", "person_id": "p02", "org_id": "o01", "title": "广州市委副书记、代市长", "start": "2023-10-09", "end": "2024-01-18", "rank": "副省级"},
    {"id": "z13", "person_id": "p02", "org_id": "o02", "title": "广州市人民政府市长", "start": "2024-01-18", "end": "present", "rank": "副省级"},

    # 郭永航
    {"id": "z14", "person_id": "p03", "org_id": "o13", "title": "深圳市委宣传部、组织部、办公厅干部", "start": "1989-07", "end": "2010-06", "rank": ""},
    {"id": "z15", "person_id": "p03", "org_id": "o14", "title": "深圳市盐田区委书记(兼区人大常委会主任)", "start": "2010-06", "end": "2015-05", "rank": "正厅级"},
    {"id": "z16", "person_id": "p03", "org_id": "o13", "title": "深圳市委常委、秘书长", "start": "2015-05", "end": "2018-02", "rank": "副省级(副部)"},
    {"id": "z17", "person_id": "p03", "org_id": "o11", "title": "珠海市委书记(兼市人大常委会主任)", "start": "2018-02", "end": "2021-11", "rank": "正厅级"},
    {"id": "z18", "person_id": "p03", "org_id": "o04", "title": "广东省人民政府副省长", "start": "2021-10", "end": "2021-12", "rank": "副省级"},
    {"id": "z19", "person_id": "p03", "org_id": "o02", "title": "广州市人民政府市长(代→正式)", "start": "2021-12", "end": "2023-10", "rank": "副省级"},
    {"id": "z20", "person_id": "p03", "org_id": "o01", "title": "广东省委常委、广州市委书记", "start": "2023-06", "end": "2025-12", "rank": "副省级"},
    {"id": "z21", "person_id": "p03", "org_id": "o05", "title": "广东省政协副主席", "start": "2026-01", "end": "present", "rank": "副省级"},
    {"id": "z22", "person_id": "p03", "org_id": "o07", "title": "接受中央纪委国家监委纪律审查和监察调查", "start": "2026-03-27", "end": "present", "rank": ""},

    # 林克庆
    {"id": "z23", "person_id": "p04", "org_id": "o01", "title": "广东省委常委、广州市委书记", "start": "2021", "end": "2023-06", "rank": "副省级"},
    {"id": "z24", "person_id": "p04", "org_id": "o05", "title": "广东省政协主席", "start": "2023", "end": "present", "rank": "正省级"},

    # 陈国
    {"id": "z25", "person_id": "p05", "org_id": "o01", "title": "广州市委副书记", "start": "待查", "end": "present", "rank": "正厅级"},

    # 杨飞
    {"id": "z26", "person_id": "p06", "org_id": "o06", "title": "广州市委常委、市纪委书记", "start": "待查", "end": "present", "rank": "正厅级"},

    # 温国辉
    {"id": "z27", "person_id": "p07", "org_id": "o02", "title": "广州市人民政府市长", "start": "2016-01", "end": "2021-12", "rank": "副省级"},
    {"id": "z28", "person_id": "p07", "org_id": "o05", "title": "广东省政协副主席", "start": "2022", "end": "present", "rank": "副省级"},
]

# 4. Relationships (Person↔Person)
relationships = [
    # 郭永航→孙志洋: 前后任市长
    {"id": "r01", "person_a": "p03", "person_b": "p02", "type": "predecessor_successor", "context": "郭永航卸任市长后由孙志洋接任广州市市长",
     "overlap_org": "广州市人民政府", "overlap_period": "2023-10", "confidence": "confirmed"},
    # 孙志洋→冯忠华: 上下级(市长与市委书记)
    {"id": "r02", "person_a": "p02", "person_b": "p01", "type": "superior_subordinate", "context": "冯忠华任广州市委书记，孙志洋任副书记兼市长，党政一把手搭档",
     "overlap_org": "中共广州市委员会", "overlap_period": "2025-12至今", "confidence": "confirmed"},
    # 郭永航→冯忠华: 前后任市委书记
    {"id": "r03", "person_a": "p03", "person_b": "p01", "type": "predecessor_successor", "context": "郭永航卸任广州市委书记后由冯忠华接任",
     "overlap_org": "中共广州市委员会", "overlap_period": "2025-12", "confidence": "confirmed"},
    # 郭永航→林克庆: 前后任市委书记
    {"id": "r04", "person_a": "p04", "person_b": "p03", "type": "predecessor_successor", "context": "林克庆卸任广州市委书记后由郭永航接任",
     "overlap_org": "中共广州市委员会", "overlap_period": "2023-06", "confidence": "confirmed"},
    # 温国辉→郭永航: 前后任市长
    {"id": "r05", "person_a": "p07", "person_b": "p03", "type": "predecessor_successor", "context": "温国辉卸任广州市市长后由郭永航接任",
     "overlap_org": "广州市人民政府", "overlap_period": "2021-12", "confidence": "confirmed"},
    # 郭永航→孙志洋: 上下级(市委书记与市长)
    {"id": "r06", "person_a": "p03", "person_b": "p02", "type": "superior_subordinate", "context": "郭永航任广州市委书记时，孙志洋任市长",
     "overlap_org": "中共广州市委员会", "overlap_period": "2023-10至2025-12", "confidence": "confirmed"},
    # 冯忠华→陈国/杨飞: 上下级(书记与副书记/纪委书记)
    {"id": "r07", "person_a": "p01", "person_b": "p05", "type": "superior_subordinate", "context": "冯忠华任市委书记，陈国任市委副书记",
     "overlap_org": "中共广州市委员会", "overlap_period": "2025-12至今", "confidence": "confirmed"},
    {"id": "r08", "person_a": "p01", "person_b": "p06", "type": "superior_subordinate", "context": "冯忠华任市委书记，杨飞任市纪委书记",
     "overlap_org": "中共广州市委员会", "overlap_period": "2025-12至今", "confidence": "confirmed"},
    # 冯忠华→海南/广东组织系统：跨省份调动
    {"id": "r09", "person_a": "p01", "person_b": "p03", "type": "same_system", "context": "冯忠华接替郭永航任广州市委书记，同属广东省委常委",
     "overlap_org": "中共广东省委员会", "overlap_period": "2025-12至今", "confidence": "confirmed"},
]


# ── Helper Functions ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' for person node based on role."""
    post = p["current_post"]
    if "书记" in post and "纪委" not in post:
        return "255,50,50"    # Red — Party Secretary
    if "市长" in post or "区长" in post or "县长" in post or "镇长" in post:
        return "50,100,255"   # Blue — Government leader
    if "纪委" in post or "纪检" in post:
        return "255,165,0"    # Orange — Discipline
    return "100,100,100"      # Grey — Other

def person_size(p):
    """Return node size based on rank."""
    post = p["current_post"]
    if "书记" in post and "纪委" not in post:
        return "20.0"
    if "市长" in post:
        return "20.0"
    return "12.0"

def org_color(o):
    """Return 'r,g,b' for organization node based on type."""
    t = o["type"]
    mapping = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return mapping.get(t, "200,200,200")


# ── Build Functions ──

def build_db():
    """Create SQLite database with persons, organizations, positions, relationships."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id TEXT PRIMARY KEY,
            person_id TEXT,
            org_id TEXT,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id TEXT PRIMARY KEY,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        )
    """)

    # Insert data
    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o["location"]))

    for z in positions:
        c.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                  (z["id"], z["person_id"], z["org_id"], z["title"],
                   z["start"], z.get("end", ""), z.get("rank", ""), ""))

    for r in relationships:
        c.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                  (r["id"], r["person_a"], r["person_b"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()


def build_gexf():
    """Generate GEXF graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>广州市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="title" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="广州市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="广州市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (worked_at)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = r.get("confidence", "plausible")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── Main ──

def main():
    print(f"=== 广州市网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")

if __name__ == "__main__":
    main()
