#!/usr/bin/env python3
"""Build Suzhou (宿州市) leadership network database and GEXF graph.

Targets: 市委书记王庆武, 市长任东
Research date: 2026-07-15
Sources:
  - www.ahsz.gov.cn (official government website, accessed 2026-07-15)
  - 宿州市人民政府 市长之窗 page (current leadership roster)
  - Official news articles (市委常委会 2026-07-14, 市政府第94次常务会议 2026-07-15)
  - 拂晓新闻网 (official local media)

Confidence: Current roles (市委书记王庆武, 市长任东) confirmed from official
  government news (书记专题会议 Jul 6, 台风防范 Jul 6-13, 人大代表座谈会 Jul 13,
  市政府常务会议 Jul 15). 市长任东 biography from official 市长之窗 page.
  Biographical details beyond basic info are limited due to restricted web search
  access (Baidu/external search tools unavailable).
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "宿州市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "宿州市_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "王庆武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共宿州市委员会",
        "source": "https://www.ahsz.gov.cn/zwzx/zwyw/196452021.html (听取人大代表意见建议, 2026-07-14); https://www.ahsz.gov.cn/zwzx/zwyw/196452011.html (督导台风防范, 2026-07-14)",
        "notes": "2026年7月任宿州市委书记。积极推动项目建设、防汛防台风、营商环境优化等工作。频繁出席调研活动(2026年7月)。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "任东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-10",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "宿州市人民政府",
        "source": "https://www.ahsz.gov.cn/content/column/167473061?liId=161973231&leaderTypeId=90385511 (市长之窗, accessed 2026-07-15)",
        "notes": "任东，男，汉族，1972年10月出生，省委党校研究生，中共党员。现任宿州市委副书记、市政府党组书记、市长。分管审计局。主持市政府全面工作。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 3,
        "name": "刘天卓",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共宿州市委员会",
        "source": "https://www.ahsz.gov.cn/zwzx/zwyw/196443231.html (书记专题会议, 2026-07-07)",
        "notes": "2026年7月任宿州市委副书记。出席书记专题会议(2026-07-06)。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "欧冬林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-01",
        "birthplace": "",
        "native_place": "",
        "education": "研究生、工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "宿州市人民政府",
        "source": "https://www.ahsz.gov.cn/content/column/167473061?liId=161973381&leaderTypeId=90385511 (市长之窗, accessed 2026-07-15)",
        "notes": "欧冬林，男，汉族，1979年1月出生，研究生、工程硕士，中共党员。市委常委、市政府党组副书记、常务副市长。负责市政府常务工作。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "张琼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共宿州市纪律检查委员会",
        "source": "https://www.ahsz.gov.cn/zwzx/zwyw/196443231.html (书记专题会议, 2026-07-07)",
        "notes": "2026年7月任宿州市委常委、市纪委书记、市监委主任。出席书记专题会议(2026-07-06)。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "霍绍斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共宿州市委组织部",
        "source": "https://www.ahsz.gov.cn/zwzx/zwyw/196443231.html (书记专题会议, 2026-07-07)",
        "notes": "2026年7月任宿州市委常委、组织部部长。出席书记专题会议(2026-07-06)。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "杨永春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "宿州市人民政府",
        "source": "https://www.ahsz.gov.cn/content/column/167473061?liId=161973211&leaderTypeId=90385511 (市长之窗, accessed 2026-07-15)",
        "notes": "市政府党组成员、副市长，市公安局党委书记、局长、督察长。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "杨泽胜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "宿州市人民政府",
        "source": "https://www.ahsz.gov.cn/content/column/167473061?liId=161973351&leaderTypeId=90385511 (市长之窗, accessed 2026-07-15)",
        "notes": "副市长，民进宿州市委会主委。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "吴绪峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "宿州市人民政府",
        "source": "https://www.ahsz.gov.cn/content/column/167473061?liId=161973361&leaderTypeId=90385511 (市长之窗, accessed 2026-07-15)",
        "notes": "市政府党组成员、副市长。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "李莉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "宿州市人民政府",
        "source": "https://www.ahsz.gov.cn/content/column/167473061?liId=161973411&leaderTypeId=90385511 (市长之窗, accessed 2026-07-15)",
        "notes": "市政府党组成员、副市长。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "汪峻",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "宿州市人民政府",
        "source": "https://www.ahsz.gov.cn/content/column/167473061?liId=161973441&leaderTypeId=90385511 (市长之窗, accessed 2026-07-15)",
        "notes": "市政府党组成员、副市长。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 12,
        "name": "岳峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席、市委秘书长",
        "current_org": "中国人民政治协商会议宿州市委员会",
        "source": "https://www.ahsz.gov.cn/zwzx/zwyw/196447361.html (调研项目建设, 2026-07-09); https://www.ahsz.gov.cn/zwzx/zwyw/196452021.html (人大代表座谈会, 2026-07-14)",
        "notes": "市政协副主席、市委秘书长。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "李荣权",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "宿州市人民政府",
        "source": "https://www.ahsz.gov.cn/content/column/167473061?liId=161973371&leaderTypeId=90385511 (市长之窗, accessed 2026-07-15)",
        "notes": "市政府党组成员、秘书长。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "赵琳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "宿州市人民代表大会常务委员会",
        "source": "https://www.ahsz.gov.cn/zwzx/zwyw/196452021.html (人大代表座谈会, 2026-07-14)",
        "notes": "市人大常委会党组书记、主任。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "祖钧公",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "宿州市人民代表大会常务委员会",
        "source": "https://www.ahsz.gov.cn/zwzx/zwyw/196452021.html (人大代表座谈会, 2026-07-14)",
        "notes": "市人大常委会党组副书记、副主任。完整履历待补充。",
        "confidence": "confirmed"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共宿州市委员会",
        "type": "党委",
        "level": "地市",
        "parent": "中共安徽省委",
        "location": "安徽省宿州市"
    },
    {
        "id": 2,
        "name": "宿州市人民政府",
        "type": "政府",
        "level": "地市",
        "parent": "安徽省人民政府",
        "location": "安徽省宿州市"
    },
    {
        "id": 3,
        "name": "中共宿州市纪律检查委员会",
        "type": "党委",
        "level": "地市",
        "parent": "中共宿州市委/中共安徽省纪委",
        "location": "安徽省宿州市"
    },
    {
        "id": 4,
        "name": "中共宿州市委组织部",
        "type": "党委",
        "level": "地市",
        "parent": "中共宿州市委",
        "location": "安徽省宿州市"
    },
    {
        "id": 5,
        "name": "宿州市人民代表大会常务委员会",
        "type": "人大",
        "level": "地市",
        "parent": "安徽省人大常委会",
        "location": "安徽省宿州市"
    },
    {
        "id": 6,
        "name": "中国人民政治协商会议宿州市委员会",
        "type": "政协",
        "level": "地市",
        "parent": "安徽省政协",
        "location": "安徽省宿州市"
    },
    {
        "id": 7,
        "name": "宿州市公安局",
        "type": "政府",
        "level": "地市",
        "parent": "宿州市人民政府",
        "location": "安徽省宿州市"
    },
]

positions = [
    # 王庆武 positions
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正厅级", "note": "现任。积极调研项目建设和防汛防台风工作。2026年7月持续在任。"},

    # 任东 positions
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": "现任市委副书记、市政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "", "end": "present", "rank": "正厅级", "note": "现任。主持市政府全面工作。分管审计局。"},

    # 刘天卓
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": "现任。"},

    # 欧冬林
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "现任市委常委、市政府党组副书记"},
    {"person_id": 4, "org_id": 2, "title": "常务副市长", "start": "", "end": "present", "rank": "副厅级", "note": "现任。负责市政府常务工作。"},

    # 张琼
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "现任。"},
    {"person_id": 5, "org_id": 3, "title": "市纪委书记、市监委主任", "start": "", "end": "present", "rank": "副厅级", "note": "现任。"},

    # 霍绍斌
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "现任。"},
    {"person_id": 6, "org_id": 4, "title": "组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": "现任。"},

    # 杨永春
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市政府党组成员、副市长"},
    {"person_id": 7, "org_id": 7, "title": "市公安局局长", "start": "", "end": "present", "rank": "副厅级", "note": "市公安局党委书记、局长、督察长"},

    # 杨泽胜
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "民进宿州市委会主委"},

    # 吴绪峰
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市政府党组成员、副市长"},

    # 李莉
    {"person_id": 10, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市政府党组成员、副市长"},

    # 汪峻
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市政府党组成员、副市长"},

    # 岳峰
    {"person_id": 12, "org_id": 6, "title": "市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "市委秘书长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # 李荣权
    {"person_id": 13, "org_id": 2, "title": "市政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": "市政府党组成员、秘书长"},

    # 赵琳
    {"person_id": 14, "org_id": 5, "title": "市人大常委会主任", "start": "", "end": "present", "rank": "正厅级", "note": "市人大常委会党组书记、主任"},

    # 祖钧公
    {"person_id": 15, "org_id": 5, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副厅级", "note": "市人大常委会党组副书记、副主任"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长党政搭档", "overlap_org": "中共宿州市委员会/宿州市人民政府", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与市委副书记搭档", "overlap_org": "中共宿州市委员会", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "市长与常务副市长工作搭档", "overlap_org": "宿州市人民政府", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委书记与纪委书记监督关系", "overlap_org": "中共宿州市委员会", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "市委书记与组织部部长工作关系", "overlap_org": "中共宿州市委员会", "overlap_period": "2026-至今"},
    {"person_a": 4, "person_b": 7, "type": "colleague", "context": "常务副市长与副市长工作关系", "overlap_org": "宿州市人民政府", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "市委书记与市委秘书长工作关系", "overlap_org": "中共宿州市委员会", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 14, "type": "colleague", "context": "市委书记与市人大常委会主任工作关系", "overlap_org": "宿州市四套班子", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长与市政府秘书长工作关系", "overlap_org": "宿州市人民政府", "overlap_period": "2026-至今"},
]


# ── database ─────────────────────────────────────────────────────────────
def create_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons(
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
        );
        CREATE TABLE IF NOT EXISTS organizations(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, "end", rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"DB: {DB_PATH}")


# ── GEXF ─────────────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_node_color(p):
    """Red for party sec, blue for gov leader, orange for discipline, grey for others."""
    post = p["current_post"]
    if "书记" in post and "市纪委" not in post:
        return "255,50,50"
    if "市长" in post:
        return "50,100,255"
    if "纪委书记" in post:
        return "255,165,0"
    if "组织部部长" in post:
        return "100,150,200"
    return "100,100,100"

def org_node_color(o):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(o["type"], "200,200,200")

def is_top_leader(p):
    return p["id"] in (1, 2)

def create_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>宿州市领导关系网络 — 市委书记王庆武、市长任东</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="level" type="string"/>')
    lines.append('      <attribute id="2" title="current_post" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_node_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('          <attvalue for="1" value="地厅级"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_node_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["level"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person -> organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person <-> person (relationship), weight="2.0"
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="working_relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF: {GEXF_PATH}")


# ── main ─────────────────────────────────────────────────────────────────
def main():
    create_database()
    create_gexf()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ("persons", "organizations", "positions", "relationships"):
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
    conn.close()
    print("Done.")

if __name__ == "__main__":
    main()
