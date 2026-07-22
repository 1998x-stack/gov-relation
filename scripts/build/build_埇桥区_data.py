#!/usr/bin/env python3
"""Build Yongqiao District (埇桥区) leadership network database and GEXF graph.

Targets: 区委书记王汝娜, 区长张擎
Research date: 2026-07-15
Sources:
  - www.szyq.gov.cn (official district government website, accessed 2026-07-15)
  - 区长之窗 page: https://www.szyq.gov.cn/xxgk/ldzc/index.html (leadership roster)
  - 埇桥区第十一届委员会第一次全体会议 (2026-06-23, elected区委常委/书记/副书记)
  - 埇桥区第十一届人民代表大会第六次会议公告 (2026-07-12, elected 区长张擎, 监委主任吴贞远)
  - News articles from 区融媒体中心 (various dates June-July 2026)

Confidence: Current roles confirmed from official government news and election notices.
  District Committee elected 2026-06-23, District Mayor elected 2026-07-12.
  Biographical details for 张擎 from official 区长之窗 page.
  Biographical details for 王汝娜 limited due to restricted web search (Exa rate-limited).
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "埇桥区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "埇桥区_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "王汝娜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共宿州市埇桥区委员会",
        "source": "https://www.szyq.gov.cn/zx/yqyw/163879011.html (区委十一届一次全会 2026-06-23, 当选区委书记); https://www.szyq.gov.cn/zx/yqyw/163936111.html (调研生态环境整改 2026-07-15)",
        "notes": "王汝娜，2026年6月23日当选中共宿州市埇桥区第十一届委员会书记。主持区委全面工作。频繁调研生态环保、乡村振兴、文旅产业、防汛防台风等工作。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "张擎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-02",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历、经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "埇桥区人民政府",
        "source": "https://www.szyq.gov.cn/xxgk/ldzc/index.html (区长之窗, accessed 2026-07-15); https://www.szyq.gov.cn/zx/gsgg/163924961.html (区十一届人大六次会议 2026-07-12, 补选为区长)",
        "notes": "张擎，男，汉族，1986年2月出生，大学学历，经济学学士，中共党员。2026年7月12日当选埇桥区人民政府区长。区委副书记、区政府党组书记、区长。调研高端装备制造产业发展(2026-07-15)。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 3,
        "name": "杨健",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共宿州市埇桥区委员会",
        "source": "https://www.szyq.gov.cn/zx/yqyw/163879011.html (区委十一届一次全会 2026-06-23, 当选区委副书记)",
        "notes": "2026年6月23日当选中共宿州市埇桥区第十一届委员会副书记。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "蒋雪梅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区政府党组副书记、副区长",
        "current_org": "埇桥区人民政府",
        "source": "https://www.szyq.gov.cn/zx/yqyw/163879011.html (区委十一届一次全会 2026-06-23); https://www.szyq.gov.cn/xxgk/ldzc/index.html (区长之窗)",
        "notes": "区委常委，区政府党组副书记、副区长。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "舒彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共宿州市埇桥区委员会",
        "source": "https://www.szyq.gov.cn/zx/yqyw/163879011.html (区委十一届一次全会 2026-06-23)",
        "notes": "2026年6月23日当选区委常委。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "任鸿志",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共宿州市埇桥区委员会",
        "source": "https://www.szyq.gov.cn/zx/yqyw/163879011.html (区委十一届一次全会 2026-06-23)",
        "notes": "2026年6月23日当选区委常委。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "李杨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区政府党组成员、副区长",
        "current_org": "埇桥区人民政府",
        "source": "https://www.szyq.gov.cn/zx/yqyw/163879011.html (区委十一届一次全会 2026-06-23); https://www.szyq.gov.cn/xxgk/ldzc/index.html (区长之窗)",
        "notes": "区委常委，区政府党组成员、副区长。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "谢浩然",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共宿州市埇桥区委员会",
        "source": "https://www.szyq.gov.cn/zx/yqyw/163879011.html (区委十一届一次全会 2026-06-23); https://www.szyq.gov.cn/zx/yqyw/163929011.html (陪同调研乡村文旅 2026-07-14)",
        "notes": "2026年6月23日当选区委常委。陪同王汝娜调研乡村文旅项目(2026-07-14)。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "万苗苗",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共宿州市埇桥区委员会",
        "source": "https://www.szyq.gov.cn/zx/yqyw/163879011.html (区委十一届一次全会 2026-06-23); https://www.szyq.gov.cn/zx/yqyw/163936111.html (陪同调研生态环境 2026-07-15)",
        "notes": "2026年6月23日当选区委常委。陪同王汝娜调研突出生态环境问题整改(2026-07-15)。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "吴贞远",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共宿州市埇桥区纪律检查委员会",
        "source": "https://www.szyq.gov.cn/zx/yqyw/163879011.html (区委十一届一次全会 2026-06-23, 当选区委常委); https://www.szyq.gov.cn/zx/gsgg/163924961.html (区十一届人大六次会议 2026-07-12, 补选为区监委主任)",
        "notes": "2026年6月23日当选区委常委。2026年7月12日补选为埇桥区监察委员会主任。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "陆雪峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共宿州市埇桥区委员会",
        "source": "https://www.szyq.gov.cn/zx/yqyw/163879011.html (区委十一届一次全会 2026-06-23); https://www.szyq.gov.cn/zx/yqyw/163927401.html (陪同调研防汛 2026-07-13)",
        "notes": "2026年6月23日当选区委常委。陪同王汝娜调研防汛防台风工作(2026-07-13)。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 12,
        "name": "赵振华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长（挂）",
        "current_org": "埇桥区人民政府",
        "source": "https://www.szyq.gov.cn/xxgk/ldzc/index.html (区长之窗, accessed 2026-07-15)",
        "notes": "副区长（挂职）。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "张少付",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府党组成员、副区长，市公安局埇桥分局党委书记、局长",
        "current_org": "埇桥区人民政府/宿州市公安局埇桥分局",
        "source": "https://www.szyq.gov.cn/xxgk/ldzc/index.html (区长之窗, accessed 2026-07-15)",
        "notes": "区政府党组成员、副区长，市公安局埇桥分局党委书记、局长、二级高级警长。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "王伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "埇桥区人民政府",
        "source": "https://www.szyq.gov.cn/xxgk/ldzc/index.html (区长之窗, accessed 2026-07-15)",
        "notes": "区政府党组成员、副区长。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "李国盛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "埇桥区人民政府",
        "source": "https://www.szyq.gov.cn/xxgk/ldzc/index.html (区长之窗, accessed 2026-07-15)",
        "notes": "副区长。完整履历待补充。",
        "confidence": "confirmed"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共宿州市埇桥区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共宿州市委",
        "location": "安徽省宿州市埇桥区"
    },
    {
        "id": 2,
        "name": "埇桥区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "宿州市人民政府",
        "location": "安徽省宿州市埇桥区"
    },
    {
        "id": 3,
        "name": "中共宿州市埇桥区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共埇桥区委/中共宿州市纪委",
        "location": "安徽省宿州市埇桥区"
    },
    {
        "id": 4,
        "name": "宿州市公安局埇桥分局",
        "type": "政府",
        "level": "县处级",
        "parent": "埇桥区人民政府/宿州市公安局",
        "location": "安徽省宿州市埇桥区"
    },
]

positions = [
    # 王汝娜
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2026-06", "end": "present", "rank": "正处级", "note": "2026年6月23日当选区委书记。主持区委全面工作。"},

    # 张擎
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "正处级", "note": "2026年6月23日当选区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "2026-07", "end": "present", "rank": "正处级", "note": "2026年7月12日补选为区长。区政府党组书记。主持区政府全面工作。"},

    # 杨健
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "2026-06", "end": "present", "rank": "正处级", "note": "2026年6月23日当选区委副书记。"},

    # 蒋雪梅
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026年6月23日当选区委常委"},
    {"person_id": 4, "org_id": 2, "title": "副区长（常务）", "start": "", "end": "present", "rank": "副处级", "note": "区政府党组副书记、常务副区长"},

    # 舒彬
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026年6月23日当选区委常委"},

    # 任鸿志
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026年6月23日当选区委常委"},

    # 李杨
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026年6月23日当选区委常委"},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "区政府党组成员、副区长"},

    # 谢浩然
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026年6月23日当选区委常委"},

    # 万苗苗
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026年6月23日当选区委常委"},

    # 吴贞远
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026年6月23日当选区委常委"},
    {"person_id": 10, "org_id": 3, "title": "区纪委书记、区监委主任", "start": "2026-07", "end": "present", "rank": "副处级", "note": "2026年7月12日补选为区监察委员会主任"},

    # 陆雪峰
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026年6月23日当选区委常委"},

    # 赵振华
    {"person_id": 12, "org_id": 2, "title": "副区长（挂）", "start": "", "end": "present", "rank": "副处级", "note": "挂职副区长"},

    # 张少付
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "区政府党组成员、副区长"},
    {"person_id": 13, "org_id": 4, "title": "局长", "start": "", "end": "present", "rank": "副处级", "note": "市公安局埇桥分局党委书记、局长、二级高级警长"},

    # 王伟
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "区政府党组成员、副区长"},

    # 李国盛
    {"person_id": 15, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "副区长"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长党政搭档", "overlap_org": "中共埇桥区委/埇桥区政府", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与区委副书记搭档", "overlap_org": "中共埇桥区委", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 3, "type": "colleague", "context": "区委副书记同僚", "overlap_org": "中共埇桥区委", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与常务副区长工作关系", "overlap_org": "中共埇桥区委/埇桥区政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与常务副区长工作搭档", "overlap_org": "埇桥区政府", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "区委书记与纪委书记监督关系", "overlap_org": "中共埇桥区委", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区委书记与区委常委工作关系", "overlap_org": "中共埇桥区委", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "区委书记与区委常委工作关系", "overlap_org": "中共埇桥区委", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "区委书记与区委常委工作关系", "overlap_org": "中共埇桥区委", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长工作关系", "overlap_org": "埇桥区政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "区长与副区长（公安）工作关系", "overlap_org": "埇桥区政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "区长与副区长工作关系", "overlap_org": "埇桥区政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "区长与副区长工作关系", "overlap_org": "埇桥区政府", "overlap_period": "2026-至今"},
    {"person_a": 4, "person_b": 7, "type": "colleague", "context": "常务副区长与副区长工作关系", "overlap_org": "埇桥区政府", "overlap_period": "2026-至今"},
    {"person_a": 5, "person_b": 6, "type": "colleague", "context": "区委常委同僚", "overlap_org": "中共埇桥区委", "overlap_period": "2026-至今"},
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
    if "区委书记" in post and "纪委" not in post:
        return "255,50,50"
    if "区长" in post:
        return "50,100,255"
    if "纪委书记" in post or "监委" in post:
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
    lines.append('    <description>埇桥区领导关系网络 — 区委书记王汝娜、区长张擎</description>')
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
        lines.append('          <attvalue for="1" value="县处级"/>')
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
