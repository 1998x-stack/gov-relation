#!/usr/bin/env python3
"""
天长市领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Tianchang City (天长市, 滁州市, 安徽省) leadership.

Research date: 2026-07-15
Research method: tianchang.gov.cn, Baidu search, news reports (市融媒体中心, 人民网, etc.)

Key findings as of July 2026:
- 市委书记: 张秀山 (Zhang Xiushan)
- 市委副书记、市长: 阚绪瑞 (Kan Xurui)
- 天长市为县级市，隶属安徽省滁州市

Sources:
  - https://www.tianchang.gov.cn (天长市人民政府)
  - https://www.tianchang.gov.cn/zwgk/ldzc/ (领导之窗)
  - 天长市人民政府新闻: 张秀山调研、市委理论学习中心组会议、阚绪瑞调研水环境等报道
  - Baidu Baike (partial): 张秀山, 阚绪瑞
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/tmp/anhui_天长市/天长市_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/anhui_天长市/天长市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ══ Current Party Secretary (市委书记) — 张秀山 ══
    {"id": 1, "name": "张秀山", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天长市委书记", "current_org": "中共天长市委员会",
     "source": "tianchang.gov.cn; 市融媒体中心报道; 澎湃新闻; 百度百科",
     "notes": "2026年7月在任，常出席调研、主持会议等公开活动", "confidence": "confirmed"},

    # ══ Current Mayor (市委副书记、市长) — 阚绪瑞 ══
    {"id": 2, "name": "阚绪瑞", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-04", "birthplace": "", "education": "在职大学学历，文学学士",
     "party_join": "2000-01", "work_start": "1997-08",
     "current_post": "天长市委副书记、市长", "current_org": "天长市人民政府",
     "source": "tianchang.gov.cn/zwgk/ldzc/; 领导之窗官方简历",
     "notes": "官方简历显示1978年4月生, 1997年8月参加工作, 2000年1月入党", "confidence": "confirmed"},

    # ══ 市委常委、常务副市长 — 张钰 ══
    {"id": 3, "name": "张钰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天长市委常委、常务副市长", "current_org": "天长市人民政府",
     "source": "tianchang.gov.cn; 领导之窗; 市委理论学习中心组报道",
     "notes": "2026年7月多次出现在公开报道中作重点发言", "confidence": "confirmed"},

    # ══ 市委常委、统战部长、副市长 — 张文杰 ══
    {"id": 4, "name": "张文杰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天长市委常委、统战部长、副市长", "current_org": "中共天长市委统战部",
     "source": "tianchang.gov.cn/zwgk/ldzc/",
     "notes": "", "confidence": "confirmed"},

    # ══ 市委常委、副市长 — 蒋跃 ══
    {"id": 5, "name": "蒋跃", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天长市委常委、副市长", "current_org": "天长市人民政府",
     "source": "tianchang.gov.cn; 领导之窗; 理论学习中心组报道",
     "notes": "2026年7月作重点发言", "confidence": "confirmed"},

    # ══ 市领导（市委常委候选人）— 王翔 ══
    {"id": 6, "name": "王翔", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天长市领导", "current_org": "中共天长市委员会",
     "source": "tianchang.gov.cn 台风防范报道 2026-07-13",
     "notes": "陪同张秀山调研台风防范工作，称为'市领导'", "confidence": "confirmed"},

    # ══ 市领导（女）— 麻丽敏 ══
    {"id": 7, "name": "麻丽敏", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天长市领导", "current_org": "中共天长市委员会",
     "source": "tianchang.gov.cn 理论学习中心组报道 2026-07-10",
     "notes": "作重点发言", "confidence": "confirmed"},

    # ══ 市领导 — 张宏生 ══
    {"id": 8, "name": "张宏生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天长市领导", "current_org": "中共天长市委员会",
     "source": "tianchang.gov.cn 理论学习中心组报道 2026-07-10",
     "notes": "市委理论学习中心组成员", "confidence": "confirmed"},

    # ══ 市领导 — 宰正平 ══
    {"id": 9, "name": "宰正平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天长市领导", "current_org": "中共天长市委员会",
     "source": "tianchang.gov.cn 理论学习中心组报道 2026-07-10",
     "notes": "市委理论学习中心组成员", "confidence": "confirmed"},

    # ══ 市领导 — 王林 ══
    {"id": 10, "name": "王林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天长市领导", "current_org": "中共天长市委员会",
     "source": "tianchang.gov.cn 理论学习中心组报道 2026-07-10",
     "notes": "市委理论学习中心组成员", "confidence": "confirmed"},

    # ══ 副市长 — 杨朝晖 ══
    {"id": 11, "name": "杨朝晖", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "天长市副市长", "current_org": "天长市人民政府",
     "source": "tianchang.gov.cn/zwgk/ldzc/",
     "notes": "", "confidence": "confirmed"},

    # ══ 副市长（挂职）— 唐晓菲 ══
    {"id": 12, "name": "唐晓菲", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "天长市副市长（挂职）", "current_org": "天长市人民政府",
     "source": "tianchang.gov.cn; 领导之窗; 水环境治理报道",
     "notes": "挂职副市长，参与水环境治理分管工作", "confidence": "confirmed"},

    # ══ 副市长（挂职）— 张杨 ══
    {"id": 13, "name": "张杨", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "天长市副市长（挂职）", "current_org": "天长市人民政府",
     "source": "tianchang.gov.cn/zwgk/ldzc/",
     "notes": "", "confidence": "confirmed"},

    # ══ 副市长 — 马素莉 ══
    {"id": 14, "name": "马素莉", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "天长市副市长", "current_org": "天长市人民政府",
     "source": "tianchang.gov.cn; 领导之窗; 水环境治理报道",
     "notes": "参与水环境治理工作", "confidence": "confirmed"},

    # ══ 副市长 — 何世乐 ══
    {"id": 15, "name": "何世乐", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "天长市副市长", "current_org": "天长市人民政府",
     "source": "tianchang.gov.cn/zwgk/ldzc/",
     "notes": "", "confidence": "confirmed"},

    # ══ 副市长、公安局局长 — 孙俊杰 ══
    {"id": 16, "name": "孙俊杰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天长市副市长、公安局局长", "current_org": "天长市人民政府",
     "source": "tianchang.gov.cn/zwgk/ldzc/",
     "notes": "", "confidence": "confirmed"},

    # ══ 市委领导 — 吕传华 ══
    {"id": 17, "name": "吕传华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天长市领导", "current_org": "中共天长市委员会",
     "source": "tianchang.gov.cn; 理论学习中心组报道; 水环境治理报道",
     "notes": "市委理论学习中心组成员，参与水环境治理调度", "confidence": "confirmed"},
]

organizations = [
    {"id": 1, "name": "中共天长市委员会", "type": "党委", "level": "县处级", "parent": "中共滁州市委员会", "location": "安徽省滁州市天长市"},
    {"id": 2, "name": "天长市人民政府", "type": "政府", "level": "县处级", "parent": "滁州市人民政府", "location": "安徽省滁州市天长市"},
    {"id": 3, "name": "中共天长市委统战部", "type": "党委", "level": "县处级", "parent": "中共天长市委员会", "location": "安徽省滁州市天长市"},
    {"id": 4, "name": "天长市公安局", "type": "政府", "level": "县处级", "parent": "天长市人民政府", "location": "安徽省滁州市天长市"},
    {"id": 5, "name": "中共滁州市委员会", "type": "党委", "level": "地厅级", "parent": "中共安徽省委员会", "location": "安徽省滁州市"},
    {"id": 6, "name": "滁州市人民政府", "type": "政府", "level": "地厅级", "parent": "安徽省人民政府", "location": "安徽省滁州市"},
]

positions = [
    # 张秀山 — 市委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "天长市委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "2026年7月在任，参与防汛调研、理论学习中心组会议等"},

    # 阚绪瑞 — 市长
    {"id": 2, "person_id": 2, "org_id": 2, "title": "天长市委副书记、市长", "start": "", "end": "present", "rank": "县处级正职", "note": "领导市政府全面工作，分管审计局"},

    # 张钰 — 常务副市长
    {"id": 3, "person_id": 3, "org_id": 2, "title": "天长市委常委、常务副市长", "start": "", "end": "present", "rank": "县处级副职", "note": "2026年7月在任，陪同张秀山调研防汛等工作"},

    # 张文杰
    {"id": 4, "person_id": 4, "org_id": 3, "title": "天长市委常委、统战部长、副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 蒋跃
    {"id": 5, "person_id": 5, "org_id": 2, "title": "天长市委常委、副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 王翔
    {"id": 6, "person_id": 6, "org_id": 1, "title": "天长市领导", "start": "", "end": "present", "rank": "", "note": "陪同张秀山调研台风防范"},

    # 麻丽敏
    {"id": 7, "person_id": 7, "org_id": 1, "title": "天长市领导", "start": "", "end": "present", "rank": "", "note": "市委理论学习中心组作重点发言"},

    # 张宏生
    {"id": 8, "person_id": 8, "org_id": 1, "title": "天长市领导", "start": "", "end": "present", "rank": "", "note": "市委理论学习中心组成员"},

    # 宰正平
    {"id": 9, "person_id": 9, "org_id": 1, "title": "天长市领导", "start": "", "end": "present", "rank": "", "note": "市委理论学习中心组成员"},

    # 王林
    {"id": 10, "person_id": 10, "org_id": 1, "title": "天长市领导", "start": "", "end": "present", "rank": "", "note": "市委理论学习中心组成员"},

    # 杨朝晖
    {"id": 11, "person_id": 11, "org_id": 2, "title": "天长市副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 唐晓菲
    {"id": 12, "person_id": 12, "org_id": 2, "title": "天长市副市长（挂职）", "start": "", "end": "present", "rank": "县处级副职", "note": "挂职"},

    # 张杨
    {"id": 13, "person_id": 13, "org_id": 2, "title": "天长市副市长（挂职）", "start": "", "end": "present", "rank": "县处级副职", "note": "挂职"},

    # 马素莉
    {"id": 14, "person_id": 14, "org_id": 2, "title": "天长市副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 何世乐
    {"id": 15, "person_id": 15, "org_id": 2, "title": "天长市副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 孙俊杰
    {"id": 16, "person_id": 16, "org_id": 4, "title": "天长市副市长、公安局局长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 吕传华
    {"id": 17, "person_id": 17, "org_id": 1, "title": "天长市领导", "start": "", "end": "present", "rank": "", "note": "市委理论学习中心组成员，参与水环境治理"},
]

relationships = [
    # 张秀山 ←→ 阚绪瑞 (党政正职搭档)
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "superior_subordinate",
     "context": "张秀山任市委书记，阚绪瑞任市长，党政正职搭档", "overlap_org": "天长市委/市政府", "overlap_period": "2026年至今"},

    # 张秀山 ←→ 张钰 (上下级)
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "superior_subordinate",
     "context": "张钰作为常务副市长陪同张秀山调研防汛、作重点发言", "overlap_org": "天长市委", "overlap_period": "2026年至今"},

    # 阚绪瑞 ←→ 马素莉 (上下级)
    {"id": 3, "person_a_id": 2, "person_b_id": 14, "type": "superior_subordinate",
     "context": "马素莉作为副市长参与阚绪瑞主持的水环境治理调度会", "overlap_org": "天长市人民政府", "overlap_period": "2026年至今"},

    # 阚绪瑞 ←→ 唐晓菲 (上下级)
    {"id": 4, "person_a_id": 2, "person_b_id": 12, "type": "superior_subordinate",
     "context": "唐晓菲作为挂职副市长参与水环境治理调度会", "overlap_org": "天长市人民政府", "overlap_period": "2026年至今"},

    # 阚绪瑞 ←→ 吕传华 (合作)
    {"id": 5, "person_a_id": 2, "person_b_id": 17, "type": "overlap",
     "context": "吕传华参与阚绪瑞主持的水环境治理调研和调度会", "overlap_org": "天长市委/市政府", "overlap_period": "2026年至今"},

    # 张秀山 ←→ 蒋跃 (上下级)
    {"id": 6, "person_a_id": 1, "person_b_id": 5, "type": "superior_subordinate",
     "context": "蒋跃作为市委常委在理论中心组作重点发言", "overlap_org": "中共天长市委员会", "overlap_period": "2026年至今"},

    # 张秀山 ←→ 麻丽敏 (上下级)
    {"id": 7, "person_a_id": 1, "person_b_id": 7, "type": "overlap",
     "context": "麻丽敏作为市领导参加中心组学习并作重点发言", "overlap_org": "中共天长市委员会", "overlap_period": "2026年至今"},

    # 张秀山 ←→ 王翔 (上下级)
    {"id": 8, "person_a_id": 1, "person_b_id": 6, "type": "overlap",
     "context": "王翔陪同张秀山调研台风防范工作", "overlap_org": "中共天长市委员会", "overlap_period": "2026年至今"},

    # 市委常委班子内部
    {"id": 9, "person_a_id": 3, "person_b_id": 5, "type": "overlap",
     "context": "张钰与蒋跃同为市委常委，共同参加中心组学习", "overlap_org": "中共天长市委员会", "overlap_period": "2026年至今"},
]

# ── BUILD FUNCTIONS ─────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string for person node color by role."""
    name = p["name"]
    current = p["current_post"]
    if "书记" in current and "市委" in current:
        return "255,50,50"
    elif "市长" in current:
        return "50,100,255"
    elif "纪委" in current:
        return "255,165,0"
    elif "人大" in current:
        return "200,255,255"
    elif "政协" in current:
        return "255,240,200"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    elif t == "政府":
        return "200,200,255"
    elif t == "开发区":
        return "200,255,200"
    elif t == "人大":
        return "200,255,255"
    elif t == "政协":
        return "255,240,200"
    elif t == "事业单位":
        return "220,220,220"
    else:
        return "200,200,200"

def is_top_leader(p):
    current = p["current_post"]
    return "市委书记" in current or "市长" in current

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
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

    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            person_a_id INTEGER,
            person_b_id INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a_id) REFERENCES persons(id),
            FOREIGN KEY (person_b_id) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education,
                                 party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["education"], p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (id, person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (id, person_a_id, person_b_id, type, context,
                                       overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
              r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    # Stats
    print(f"  Persons: {cur.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {cur.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {cur.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {cur.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")

    conn.close()

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>天长市领导班子工作关系网络 - 2026-07-15</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="birth" type="string"/>')
    lines.append('      <attribute id="2" title="birthplace" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="start" type="string"/>')
    lines.append('      <attribute id="2" title="end" type="string"/>')
    lines.append('      <attribute id="3" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["current_post"])}"/>')
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
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["start"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="2" value="present"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF edges: {eid}")

# ── MAIN ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    print("Building 天长市 network database...")
    build_db()
    print(f"  DB: {DB_PATH}")

    print("Building GEXF graph...")
    build_gexf()
    print(f"  GEXF: {GEXF_PATH}")

    print("\nDone. Summary:")
    print(f"  {len(persons)} persons")
    print(f"  {len(organizations)} organizations")
    print(f"  {len(positions)} positions")
    print(f"  {len(relationships)} relationships")
