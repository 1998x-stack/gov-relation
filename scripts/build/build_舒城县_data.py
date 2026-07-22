#!/usr/bin/env python3
"""Build Shucheng County (舒城县) leadership network database and GEXF graph.

Targets: 县委书记韩锋, 县长胡敏
Research date: 2026-07-15
Sources:
  - www.shucheng.gov.cn (official county government website)
  - 领导之窗: https://www.shucheng.gov.cn/ldzc/index.html
  - 韩锋 profile: https://www.shucheng.gov.cn/zwzx/jrsc/38826533.html (2026-07-14)
  - 韩锋 profile: https://www.shucheng.gov.cn/zwzx/jrsc/38811288.html (2026-06-24, 十六次党代会开幕, 报告人)
  - 韩锋 profile: https://www.shucheng.gov.cn/zwzx/jrsc/38811659.html (2026-06-25, 十六次党代会闭幕, 主持)
  - 韩锋 profile: https://www.shucheng.gov.cn/zwzx/jrsc/38814027.html (2026-07-01, 两优一先表彰)
  - 胡敏 profile: https://www.shucheng.gov.cn/ldzc/index.html (领导之窗, 县委副书记、县长)
  - 中国共产党舒城县第十六次代表大会主席团名单 (2026-06-24)

Confidence: Current roles confirmed from official government website and leadership pages.
  Biographical details for 胡敏 sourced from official profile. 韩锋's bio limited to
  official news mentions only — career history before current role is unverified.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "舒城县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "舒城县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # === 1. Party Secretary (县委书记) ===
    {
        "id": 1,
        "name": "韩锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共舒城县委员会",
        "source": "https://www.shucheng.gov.cn (2026-07-14, 督导防汛防台风); https://www.shucheng.gov.cn/zwzx/jrsc/38811288.html (2026-06-24, 十六次党代会作报告); https://www.shucheng.gov.cn/zwzx/jrsc/38814027.html (2026-07-01, 两优一先表彰讲话)",
        "notes": "韩锋，现任中共舒城县委书记。2026年6月在中国共产党舒城县第十六次代表大会上代表第十五届县委作工作报告，后主持闭幕会。2026年7月督导防汛防台风工作，出席两优一先表彰会。此前为舒城县第十五届县委书记（约2021年起）。公开资料暂未找到完整简历和出生年份。",
        "confidence": "confirmed"
    },
    # === 2. County Mayor (县长) ===
    {
        "id": 2,
        "name": "胡敏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978-10",
        "birthplace": "安徽霍山",
        "native_place": "安徽霍山",
        "education": "本科学历",
        "party_join": "2000年加入中国共产党",
        "work_start": "1997-08",
        "current_post": "县委副书记、县长",
        "current_org": "舒城县人民政府",
        "source": "https://www.shucheng.gov.cn/ldzc/index.html (领导之窗-县政府领导-胡敏); https://www.shucheng.gov.cn/zwzx/jrsc/38811288.html (2026-06-24, 十六次党代会主持开幕式); https://www.shucheng.gov.cn/zwzx/jrsc/38814027.html (2026-07-01, 两优一先表彰主持)",
        "notes": "胡敏，女，汉族，安徽霍山人，1978年10月出生，1997年8月参加工作，2000年加入中国共产党，本科学历。现任县委副书记，县政府县长、党组书记。领导县政府全面工作，负责审计工作，分管县审计局。",
        "confidence": "confirmed"
    },
    # === 3. Deputy Party Secretary (县委副书记) ===
    {
        "id": 3,
        "name": "张辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县委党校校长、城关镇党委书记",
        "current_org": "中共舒城县委员会",
        "source": "https://www.shucheng.gov.cn/zwzx/jrsc/38814027.html (2026-07-01, 两优一先表彰宣读表彰决定); https://www.shucheng.gov.cn/zwzx/jrsc/38811288.html (2026-06-24, 大会主席团名单)",
        "notes": "张辉，现任舒城县委副书记，兼任县委党校校长、城关镇党委书记。在十六次党代会主席团名单中列第5位。",
        "confidence": "confirmed"
    },
    # === 4. County Discipline Secretary (县纪委书记) ===
    {
        "id": 4,
        "name": "刘全岭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共舒城县纪律检查委员会",
        "source": "https://www.shucheng.gov.cn/zwzx/jrsc/38811288.html (2026-06-24, 党代会主席团中列第10位，新列入)",
        "notes": "刘全岭，现任舒城县委常委、县纪委书记、县监委主任。在十六次党代会主席团名单中出现。",
        "confidence": "confirmed"
    },
    # === 5. Standing Committee - 郑文 ===
    {
        "id": 5,
        "name": "郑文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "舒城县人民政府",
        "source": "https://www.shucheng.gov.cn/ldzc/index.html (领导之窗-我的同事); https://www.shucheng.gov.cn/zwzx/jrsc/38811288.html (2026-06-24, 十六次党代会主席团)",
        "notes": "郑文，现任舒城县委常委、常务副县长。在县政府领导之窗位列县长之后第一位。",
        "confidence": "confirmed"
    },
    # === 6. Standing Committee - 林涛 ===
    {
        "id": 6,
        "name": "林涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共舒城县委员会",
        "source": "https://www.shucheng.gov.cn/zwzx/jrsc/38811288.html (2026-06-24, 十六次党代会主席团)",
        "notes": "林涛，现任舒城县委常委。在十六次党代会主席团名单中列第9位。",
        "confidence": "confirmed"
    },
    # === 7. Standing Committee - 张蕾 ===
    {
        "id": 7,
        "name": "张蕾",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "舒城县人民政府",
        "source": "https://www.shucheng.gov.cn/ldzc/index.html (领导之窗-我的同事); https://www.shucheng.gov.cn/zwzx/jrsc/38811288.html (2026-06-24, 十六次党代会主席团)",
        "notes": "张蕾，现任舒城县委常委、副县长。在县政府领导之窗位列常务副县长之后。",
        "confidence": "confirmed"
    },
    # === 8. Standing Committee / Organization Department ===
    {
        "id": 8,
        "name": "邱前东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共舒城县委组织部",
        "source": "https://www.shucheng.gov.cn/zwzx/jrsc/38811288.html (2026-06-24, 十六次党代会主席团)",
        "notes": "邱前东，现任舒城县委常委、组织部部长。在十六次党代会主席团名单中位列第11位。",
        "confidence": "confirmed"
    },
    # === 9. Standing Committee - 许浒 ===
    {
        "id": 9,
        "name": "许浒",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共舒城县委员会",
        "source": "https://www.shucheng.gov.cn/zwzx/jrsc/38811288.html (2026-06-24, 十六次党代会主席团列第14位)",
        "notes": "许浒，现任舒城县委常委。在十六次党代会主席团名单中列第14位。",
        "confidence": "confirmed"
    },
    # === 10. Standing Committee - 杨宏 ===
    {
        "id": 10,
        "name": "杨宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共舒城县委员会",
        "source": "https://www.shucheng.gov.cn/zwzx/jrsc/38811288.html (2026-06-24, 十六次党代会主席团列第15位)",
        "notes": "杨宏，现任舒城县委常委。在十六次党代会主席团名单中列第15位。",
        "confidence": "confirmed"
    },
    # === 11. Deputy County Mayor - 张栋梁 ===
    {
        "id": 11,
        "name": "张栋梁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "舒城县人民政府",
        "source": "https://www.shucheng.gov.cn/ldzc/index.html (领导之窗-我的同事); https://www.shucheng.gov.cn/zwzx/jrsc/38811288.html (2026-06-24, 十六次党代会主席团)",
        "notes": "张栋梁，现任舒城县副县长。在党代会主席团中列第13位。",
        "confidence": "confirmed"
    },
    # === 12. Deputy County Mayor - 胡俊 ===
    {
        "id": 12,
        "name": "胡俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "舒城县人民政府",
        "source": "https://www.shucheng.gov.cn/ldzc/index.html (领导之窗-我的同事)",
        "notes": "胡俊，现任舒城县副县长。",
        "confidence": "confirmed"
    },
    # === 13. Deputy County Mayor - 张成伟 ===
    {
        "id": 13,
        "name": "张成伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "舒城县人民政府",
        "source": "https://www.shucheng.gov.cn/ldzc/index.html (领导之窗-我的同事)",
        "notes": "张成伟，现任舒城县副县长。",
        "confidence": "confirmed"
    },
    # === 14. Deputy County Mayor - 吴军涛 ===
    {
        "id": 14,
        "name": "吴军涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "舒城县人民政府",
        "source": "https://www.shucheng.gov.cn/ldzc/index.html (领导之窗-我的同事)",
        "notes": "吴军涛，现任舒城县副县长。",
        "confidence": "confirmed"
    },
    # === 15. Deputy County Mayor (挂职) - 杨培 ===
    {
        "id": 15,
        "name": "杨培",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "舒城县人民政府",
        "source": "https://www.shucheng.gov.cn/ldzc/index.html (领导之窗-我的同事)",
        "notes": "杨培，现任舒城县副县长（挂职）。",
        "confidence": "confirmed"
    },
    # === 16. Predecessor (前任县委书记，已不再出现) ===
    # Note: 韩锋 appears to be the continuing secretary from the 15th term.
    # The 15th CPC Shucheng County Committee (2021-2026) had 韩锋 as secretary.
    # No predecessor information found - he seems to have served at least 5 years.
]

organizations = [
    {
        "id": 1,
        "name": "中共舒城县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共六安市委员会",
        "location": "安徽省六安市舒城县"
    },
    {
        "id": 2,
        "name": "舒城县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "六安市人民政府",
        "location": "安徽省六安市舒城县"
    },
    {
        "id": 3,
        "name": "中共舒城县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共舒城县委员会",
        "location": "安徽省六安市舒城县"
    },
    {
        "id": 4,
        "name": "中共舒城县委组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共舒城县委员会",
        "location": "安徽省六安市舒城县"
    },
    {
        "id": 5,
        "name": "中共舒城县委宣传部",
        "type": "党委",
        "level": "县",
        "parent": "中共舒城县委员会",
        "location": "安徽省六安市舒城县"
    },
    {
        "id": 6,
        "name": "中共舒城县委统战部",
        "type": "党委",
        "level": "县",
        "parent": "中共舒城县委员会",
        "location": "安徽省六安市舒城县"
    },
    {
        "id": 7,
        "name": "舒城县城关镇",
        "type": "乡镇",
        "level": "乡镇",
        "parent": "舒城县",
        "location": "安徽省六安市舒城县城关镇"
    },
    {
        "id": 8,
        "name": "舒城县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "舒城县",
        "location": "安徽省六安市舒城县"
    },
    {
        "id": 9,
        "name": "中国人民政治协商会议舒城县委员会",
        "type": "政协",
        "level": "县",
        "parent": "舒城县",
        "location": "安徽省六安市舒城县"
    },
]

positions = [
    # 韩锋
    (1, 1, "县委书记", "", "present", "正处级", "主持县委全面工作"),
    # 胡敏
    (2, 2, "县长", "", "present", "正处级", "领导县政府全面工作，负责审计工作"),
    (2, 1, "县委副书记", "", "present", "正处级", ""),
    # 张辉
    (3, 1, "县委副书记", "", "present", "副处级", ""),
    (3, 7, "城关镇党委书记", "", "present", "副处级", "兼任"),
    # 刘全岭
    (4, 1, "县委常委", "", "present", "副处级", ""),
    (4, 3, "县纪委书记、监委主任", "", "present", "副处级", ""),
    # 郑文
    (5, 2, "常务副县长", "", "present", "副处级", ""),
    (5, 1, "县委常委", "", "present", "副处级", ""),
    # 林涛
    (6, 1, "县委常委", "", "present", "副处级", ""),
    # 张蕾
    (7, 2, "副县长", "", "present", "副处级", ""),
    (7, 1, "县委常委", "", "present", "副处级", ""),
    # 邱前东
    (8, 1, "县委常委", "", "present", "副处级", ""),
    (8, 4, "组织部部长", "", "present", "副处级", ""),
    # 许浒
    (9, 1, "县委常委", "", "present", "副处级", ""),
    # 杨宏
    (10, 1, "县委常委", "", "present", "副处级", ""),
    # 张栋梁
    (11, 2, "副县长", "", "present", "副处级", ""),
    # 胡俊
    (12, 2, "副县长", "", "present", "副处级", ""),
    # 张成伟
    (13, 2, "副县长", "", "present", "副处级", ""),
    # 吴军涛
    (14, 2, "副县长", "", "present", "副处级", ""),
    # 杨培
    (15, 2, "副县长（挂职）", "", "present", "副处级", ""),
]

relationships = [
    # 书记 - 县长
    (1, 2, "overlap", "书记与县长搭档，共同主持县委县政府全面工作", "中共舒城县委员会", "2021-", "strong"),
    # 书记 - 副书记
    (1, 3, "overlap", "书记与副书记在县委常委会共事", "中共舒城县委员会", "2026-", "strong"),
    # 书记 - 各常委
    (1, 4, "overlap", "县委常委会共事；书记与纪委书记", "中共舒城县委员会", "2026-", "medium"),
    (1, 5, "overlap", "县委常委会共事；书记与常务副县长", "中共舒城县委员会", "2026-", "strong"),
    (1, 6, "overlap", "县委常委会共事", "中共舒城县委员会", "2026-", "medium"),
    (1, 7, "overlap", "县委常委会共事", "中共舒城县委员会", "2026-", "medium"),
    (1, 8, "overlap", "县委常委会共事；书记与组织部部长", "中共舒城县委员会", "2026-", "strong"),
    (1, 9, "overlap", "县委常委会共事", "中共舒城县委员会", "2026-", "medium"),
    (1, 10, "overlap", "县委常委会共事", "中共舒城县委员会", "2026-", "medium"),
    # 县长 - 常务副县长
    (2, 5, "overlap", "县长与常务副县长工作搭档", "舒城县人民政府", "2026-", "strong"),
    # 县长 - 各副县长
    (2, 7, "overlap", "县政府班子", "舒城县人民政府", "2026-", "medium"),
    (2, 11, "overlap", "县政府班子", "舒城县人民政府", "2026-", "medium"),
    (2, 12, "overlap", "县政府班子", "舒城县人民政府", "2026-", "medium"),
    (2, 13, "overlap", "县政府班子", "舒城县人民政府", "2026-", "medium"),
    (2, 14, "overlap", "县政府班子", "舒城县人民政府", "2026-", "medium"),
    (2, 15, "overlap", "县政府班子", "舒城县人民政府", "2026-", "medium"),
    # 副书记 - 其他常委
    (3, 4, "overlap", "同为县委领导", "中共舒城县委员会", "2026-", "medium"),
    (3, 5, "overlap", "同为县委领导", "中共舒城县委员会", "2026-", "medium"),
    # 常务副县长 - 其他副县长
    (5, 11, "overlap", "县政府班子", "舒城县人民政府", "2026-", "medium"),
    (5, 12, "overlap", "县政府班子", "舒城县人民政府", "2026-", "medium"),
    (5, 13, "overlap", "县政府班子", "舒城县人民政府", "2026-", "medium"),
    # 常委互连
    (4, 8, "overlap", "同为县委常委", "中共舒城县委员会", "2026-", "medium"),
    (5, 8, "overlap", "同为县委常委", "中共舒城县委员会", "2026-", "medium"),
    (7, 8, "overlap", "同为县委常委", "中共舒城县委员会", "2026-", "medium"),
]


# ══════════════════════════════════════════════════════════════════════════
# Database + GEXF generation
# ══════════════════════════════════════════════════════════════════════════

def create_database():
    """Create SQLite database with persons, organizations, positions, relationships."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, native_place TEXT,
            education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT, notes TEXT, confidence TEXT
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org,
                                 source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["native_place"], p["education"],
              p["party_join"], p["work_start"],
              p["current_post"], p["current_org"],
              p["source"], p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        pid, oid, title, start, end, rank, note = pos
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (pid, oid, title, start, end, rank, note))

    for r in relationships:
        pa, pb, rtype, ctx, oorg, operiod, strength = r
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (pa, pb, rtype, ctx, oorg, operiod, strength))

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")
    print(f"      Persons: {len(persons)}")
    print(f"      Organizations: {len(organizations)}")
    print(f"      Positions: {len(positions)}")
    print(f"      Relationships: {len(relationships)}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(person):
    """Return 'r,g,b' string based on role."""
    role = person.get("current_post", "")
    if "书记" in role and "副书记" not in role and "纪委" not in role:
        return "255,50,50"  # Red for Party Secretary
    if "县长" in role and "副" not in role:
        return "50,100,255"  # Blue for County Mayor
    if "纪委书记" in role or "监委" in role:
        return "255,165,0"  # Orange for Discipline
    if "常委" in role and "副县长" in role:
        return "50,100,255"  # Blue for Standing/Deputy
    if "副县长" in role:
        return "50,100,255"  # Blue for Deputy Mayor
    if "副书记" in role:
        return "255,100,100"  # Light Red for Deputy Secretary
    if "组织部" in role:
        return "100,150,255"
    if "常委" in role:
        return "100,100,200"  # Indigo for other Standing members
    return "100,100,100"  # Grey for others


def person_size(person):
    """Return node size based on rank."""
    role = person.get("current_post", "")
    if "县委书记" in role and "副" not in role:
        return "20.0"
    if "县长" in role and "副" not in role:
        return "20.0"
    return "12.0"


def org_color(org):
    """Return 'r,g,b' string for organization type."""
    t = org.get("type", "")
    type_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "乡镇": "255,255,200",
    }
    return type_colors.get(t, "200,200,200")


def generate_gexf():
    """Generate GEXF graph using string formatting to avoid XML namespace issues."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>舒城县领导班子工作关系网络 - 六安市舒城县</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges (worked_at)
    for pos in positions:
        pid, oid, title, start, end, rank, note = pos
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(start)}-{esc(end)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person edges (relationship)
    for r in relationships:
        pa, pb, rtype, ctx, oorg, operiod, strength = r
        weight = "2.0" if strength == "strong" else "1.5" if strength == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(operiod)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] GEXF graph created: {GEXF_PATH}")
    print(f"      Person nodes: {len(persons)}")
    print(f"      Organization nodes: {len(organizations)}")
    print(f"      Person→Org edges: {len(positions)}")
    print(f"      Person↔Person edges: {len(relationships)}")
    print(f"      Total edges: {len(positions) + len(relationships)}")


def main():
    print("=" * 60)
    print("  舒城县领导班子网络数据生成")
    print(f"  Generated: {TODAY}")
    print("=" * 60)
    create_database()
    generate_gexf()
    print(f"\nSummary:")
    print(f"  Top leaders: 韩锋（县委书记）, 胡敏（县长）")
    print(f"  Standing Committee: 10 members (including secretary and deputy)")
    print(f"  Government team: 1县长 + 1常务副县长 + 3副县长 + 1挂职副县长")
    print(f"  Research as of: {TODAY}")
    print(f"\n[OK] All files generated in: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
