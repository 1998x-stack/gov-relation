#!/usr/bin/env python3
"""
大埔县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
City: 梅州市
County: 大埔县
Targets: 县委书记 & 县长

Research Date: 2026-07-22

Research Notes:
- 凌晓文（县长）的身份已通过大埔县人民政府官网领导之窗页面确认：
  https://www.dabu.gov.cn/zwgk/ldzc/index.html
  官方简历：凌晓文，男，汉族，1976年8月生，大学学历，公共管理硕士，中共党员。
- 黄增国（县委书记）的身份已通过大埔县纪委官网新闻确认：
  https://www.dbjw.gov.cn/xwxc/zhyw/t20250710_4593.htm  (2025-07-10)
  https://www.dbjw.gov.cn/xwxc/gzdt/t20260629_5054.htm (2026-06-29)
- 叶慧玲（县委常委、县纪委书记、县监委主任）的身份已通过大埔县纪委全会新闻确认：
  https://www.dbjw.gov.cn/xwxc/gzdt/t20260126_4860.htm (2026-01-26)
- 朱汉东、林健雄（前任县委书记）和刘彩波（前任县长）的信息仍基于训练数据，标注[P]。
- 其他领导班子成员（县委副书记、常务副县长、组织部部长、宣传部部长）具体姓名在
  现有可访问的官方来源中未找到，标注为[G]信息缺失。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

try:
    from gov_relation.runner import run_build
    USE_RUNNER = True
except ImportError:
    USE_RUNNER = False

# ── Slug & Paths ──
SLUG = "大埔县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
CANONICAL_DB = os.path.join(DATABASE_DIR, f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(GRAPH_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ══════════════════════════════════════════════════════════════════════════════
# RESEARCH DATA
# ══════════════════════════════════════════════════════════════════════════════
#
# CONFIDENCE KEY:
#   [C] = Confirmed — official government website / reliable multiple sources
#   [P] = Plausible — likely correct based on training data
#   [U] = Unverified — needs confirmation
#   [G] = Gap — information not available
# ══════════════════════════════════════════════════════════════════════════════

# ── Persons ──

persons = [
    # ════════════════════════════════════════════
    # CURRENT 县委书记 (Party Secretary)
    # ════════════════════════════════════════════

    # [C] Current 县委书记 — 黄增国
    # Confirmed by dbjw.gov.cn news: 2025-07-10 and 2026-06-29 articles
    {
        "id": 1,
        "name": "黄增国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共大埔县委书记",
        "current_org": "中共大埔县委员会",
        "source": "[C] Confirmed by official news articles on dbjw.gov.cn (2025-07-10, 2026-01-26, 2026-06-29). Name and role confirmed as 县委书记黄增国 presiding over county-level party meetings. Detailed career history requires further research."
    },

    # ════════════════════════════════════════════
    # CURRENT 县长 (County Mayor)
    # ════════════════════════════════════════════

    # [C] Current 县长 — 凌晓文
    # Confirmed by dabu.gov.cn leadership page
    {
        "id": 2,
        "name": "凌晓文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-08",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大埔县委副书记、县政府党组书记、县长",
        "current_org": "大埔县人民政府",
        "source": "[C] Confirmed by dabu.gov.cn leadership page (https://www.dabu.gov.cn/zwgk/ldzc/index.html). Official bio: 男，汉族，1976年8月生，大学学历，公共管理硕士，中共党员。Also confirmed by dbjw.gov.cn news articles."
    },

    # ════════════════════════════════════════════
    # CURRENT 县委常委、县纪委书记
    # ════════════════════════════════════════════

    # [C] Current 县纪委书记 — 叶慧玲
    # Confirmed by dbjw.gov.cn 纪委全会 news
    {
        "id": 3,
        "name": "叶慧玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大埔县委常委、县纪委书记、县监委主任",
        "current_org": "中共大埔县纪律检查委员会",
        "source": "[C] Confirmed by dbjw.gov.cn (2026-01-26 十三届县纪委六次全会 news): 县委常委、县纪委书记、县监委主任叶慧玲主持会议."
    },

    # ════════════════════════════════════════════
    # PREDECESSORS — 县委书记
    # ════════════════════════════════════════════

    # [P] Predecessor 县委书记 — 朱汉东
    {
        "id": 4,
        "name": "朱汉东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年（约）",
        "birthplace": "待查（似为广东梅州人）",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任中共大埔县委书记（~2016-2021）",
        "current_org": "中共大埔县委员会（原）",
        "source": "[P] Training data knowledge. Served as 大埔县委书记 after previously being 大埔县长. 黄增国的直接前任可能不是朱汉东，需要确认黄增国的到任时间和前任."
    },

    # [P] Earlier 县委书记 — 林健雄
    {
        "id": 5,
        "name": "林健雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任中共大埔县委书记（~2013-2016）",
        "current_org": "中共大埔县委员会（原）",
        "source": "[P] Training data knowledge. Earlier 大埔县委书记."
    },

    # ════════════════════════════════════════════
    # PREDECESSORS — 县长
    # ════════════════════════════════════════════

    # [P] Predecessor 县长 — 刘彩波
    {
        "id": 6,
        "name": "刘彩波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任大埔县人民政府县长（~2016-2021）",
        "current_org": "大埔县人民政府（原）",
        "source": "[P] Training data knowledge. Served as 大埔县长, potentially during 朱汉东's tenure as 县委书记."
    },

    # ════════════════════════════════════════════
    # NOTABLE DEPUTIES / 领导班子成员 (信息缺失)
    # ════════════════════════════════════════════

    # [G] 县委副书记 (专职)
    {
        "id": 7,
        "name": "县委副书记（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共大埔县委副书记（专职）",
        "current_org": "中共大埔县委员会",
        "source": "Information gap — name not available from accessible sources."
    },

    # [G] 常务副县长
    {
        "id": 8,
        "name": "常务副县长（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大埔县委常委、常务副县长",
        "current_org": "大埔县人民政府",
        "source": "Information gap — name not available from accessible sources."
    },

    # [G] 县委组织部部长
    {
        "id": 9,
        "name": "组织部部长（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大埔县委常委、组织部部长",
        "current_org": "中共大埔县委组织部",
        "source": "Information gap — name not available from accessible sources."
    },

    # [G] 县委宣传部部长
    {
        "id": 10,
        "name": "宣传部部长（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大埔县委常委、宣传部部长",
        "current_org": "中共大埔县委宣传部",
        "source": "Information gap — name not available from accessible sources."
    },

    # ════════════════════════════════════════════
    # NOTABLE NATIVES — 大埔籍在外地担任要职的干部
    # ════════════════════════════════════════════

    # [C] 陈通汕 — 大埔人, 现任厦门思明区委书记
    {
        "id": 11,
        "name": "陈通汕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-11",
        "birthplace": "广东省梅州市大埔县",
        "native_place": "广东省梅州市大埔县",
        "education": "在职研究生，管理学硕士",
        "party_join": "中共党员",
        "work_start": "1992-08",
        "current_post": "厦门市思明区委书记",
        "current_org": "中共思明区委",
        "source": "[C] data/persons/20260716-福建省-厦门市-思明区委书记-陈通汕.json已确认."
    },

    # [P] 郭文海 — 大埔人
    {
        "id": 12,
        "name": "郭文海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广东省梅州市大埔县",
        "native_place": "广东省梅州市大埔县",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广东省重要职务（待确认具体职位）",
        "current_org": "待确认",
        "source": "[P] Training data knowledge. 广东大埔人, previously served in Foshan/Shunde leadership. Current role requires verification."
    },
]

# ── Organizations ──

organizations = [
    {
        "id": 1,
        "name": "中共大埔县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共梅州市委",
        "location": "广东省梅州市大埔县湖寮镇"
    },
    {
        "id": 2,
        "name": "大埔县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "梅州市人民政府",
        "location": "广东省梅州市大埔县湖寮镇"
    },
    {
        "id": 3,
        "name": "中共大埔县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共梅州市纪委",
        "location": "广东省梅州市大埔县湖寮镇"
    },
    {
        "id": 4,
        "name": "中共大埔县委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共大埔县委员会",
        "location": "广东省梅州市大埔县湖寮镇"
    },
    {
        "id": 5,
        "name": "中共大埔县委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共大埔县委员会",
        "location": "广东省梅州市大埔县湖寮镇"
    },
    {
        "id": 6,
        "name": "大埔县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "梅州市人民代表大会常务委员会",
        "location": "广东省梅州市大埔县湖寮镇"
    },
    {
        "id": 7,
        "name": "政协大埔县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协梅州市委员会",
        "location": "广东省梅州市大埔县湖寮镇"
    },
    {
        "id": 8,
        "name": "大埔县监察委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "梅州市监察委员会",
        "location": "广东省梅州市大埔县湖寮镇"
    },
]

# ── Positions ──

positions = [
    # 黄增国 — 县委书记（当前）
    {"person_id": 1, "org_id": 1, "title": "大埔县委书记", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": "[C] 确认现任县委书记（dbjw.gov.cn 2025-2026新闻确认）。"},

    # 凌晓文 — 县长（当前）
    {"person_id": 2, "org_id": 2, "title": "大埔县人民政府县长", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": "[C] Official from dabu.gov.cn leadership page. 男，1976年8月生。"},
    {"person_id": 2, "org_id": 1, "title": "大埔县委副书记", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[C] 县长同时任县委副书记（dabu.gov.cn确认）。"},

    # 叶慧玲 — 县纪委书记
    {"person_id": 3, "org_id": 3, "title": "大埔县委常委、县纪委书记、县监委主任", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[C] 确认现任县纪委书记（dbjw.gov.cn 2026-01-26纪委全会新闻确认）。"},
    {"person_id": 3, "org_id": 8, "title": "大埔县监委主任", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[C] 县纪委书记同时任县监委主任。"},
    {"person_id": 3, "org_id": 1, "title": "大埔县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[C] 县委常委。"},

    # 朱汉东 — 前任县委书记
    {"person_id": 4, "org_id": 1, "title": "大埔县委书记（原）", "start_date": "~2016", "end_date": "~2021", "rank": "正处级", "note": "[P] 前任县委书记。可能与黄增国之间还有其他人。"},

    # 林健雄 — 更早的县委书记
    {"person_id": 5, "org_id": 1, "title": "大埔县委书记（原）", "start_date": "~2013", "end_date": "~2016", "rank": "正处级", "note": "[P] 朱汉东的前任。"},

    # 刘彩波 — 前任县长
    {"person_id": 6, "org_id": 2, "title": "大埔县人民政府县长（原）", "start_date": "~2016", "end_date": "~2021", "rank": "正处级", "note": "[P] 与朱汉东搭档的县长。"},

    # 县委副书记（专职）
    {"person_id": 7, "org_id": 1, "title": "大埔县委副书记（专职）", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[G] 姓名待查。"},

    # 常务副县长
    {"person_id": 8, "org_id": 2, "title": "大埔县委常委、常务副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[G] 姓名待查。"},
    {"person_id": 8, "org_id": 1, "title": "大埔县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},

    # 组织部部长
    {"person_id": 9, "org_id": 4, "title": "大埔县委常委、组织部部长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[G] 姓名待查。"},
    {"person_id": 9, "org_id": 1, "title": "大埔县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},

    # 宣传部部长
    {"person_id": 10, "org_id": 5, "title": "大埔县委常委、宣传部部长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[G] 姓名待查。"},
    {"person_id": 10, "org_id": 1, "title": "大埔县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},

    # 陈通汕 — 大埔籍在外干部
    {"person_id": 11, "org_id": 1, "title": "厦门市思明区委书记", "start_date": "待查", "end_date": "现在", "rank": "正厅级", "note": "大埔籍在厦门任职，非大埔县干部。"},

    # 郭文海 — 大埔籍在外干部
    {"person_id": 12, "org_id": 1, "title": "广东省重要职务（待确认）", "start_date": "待查", "end_date": "现在", "rank": "待查", "note": "大埔籍在外任职代表。"},
]

# ── Relationships ──

relationships = [
    # 黄增国与凌晓文 — 现任党政搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "黄增国（县委书记）与凌晓文（县长）现任党政搭档",
        "overlap_org": "中共大埔县委员会/大埔县人民政府",
        "overlap_period": "当前"
    },
    # 黄增国与叶慧玲 — 县委领导与纪委书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "黄增国（县委书记）与叶慧玲（纪委书记）县委领导与纪委负责人关系",
        "overlap_org": "中共大埔县委员会",
        "overlap_period": "当前"
    },
    # 凌晓文与叶慧玲 — 县委常委同僚
    {
        "person_a": 2,
        "person_b": 3,
        "type": "colleague",
        "context": "凌晓文（县委副书记、县长）与叶慧玲（县委常委、纪委书记）同为县委常委班子成员",
        "overlap_org": "中共大埔县委员会",
        "overlap_period": "当前"
    },
    # 朱汉东 → 黄增国（推测）
    {
        "person_a": 4,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "朱汉东卸任大埔县委书记，黄增国接任（推测，需确认中间是否有其他书记）",
        "overlap_org": "中共大埔县委员会",
        "overlap_period": "~2021-2022（推测）"
    },
    # 林健雄 → 朱汉东
    {
        "person_a": 5,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "林健雄卸任大埔县委书记，朱汉东接任",
        "overlap_org": "中共大埔县委员会",
        "overlap_period": "~2016"
    },
    # 刘彩波 → 凌晓文（推测）
    {
        "person_a": 6,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "刘彩波卸任大埔县长，凌晓文接任（推测）",
        "overlap_org": "大埔县人民政府",
        "overlap_period": "待确认"
    },
    # 朱汉东与刘彩波 — 党政搭档（推测）
    {
        "person_a": 4,
        "person_b": 6,
        "type": "colleague",
        "context": "朱汉东（县委书记）与刘彩波（县长）前任党政搭档（推测）",
        "overlap_org": "中共大埔县委员会/大埔县人民政府",
        "overlap_period": "~2016-2021"
    },
]

# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # ── Determine output paths (staging mode) ──
    db = DB_PATH
    gexf = GEXF_PATH

    if USE_RUNNER:
        run_build(
            slug=SLUG,
            persons=persons,
            organizations=organizations,
            positions=positions,
            relationships=relationships,
            db_path=db,
            gexf_path=gexf,
            overwrite=True,
        )
    else:
        # Fallback: manual SQLite + GEXF
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY,
                name TEXT,
                gender TEXT,
                ethnicity TEXT,
                birth TEXT,
                birthplace TEXT,
                native_place TEXT,
                education TEXT,
                party_join TEXT,
                work_start TEXT,
                current_post TEXT,
                current_org TEXT,
                source TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS organizations (
                id INTEGER PRIMARY KEY,
                name TEXT,
                type TEXT,
                level TEXT,
                parent TEXT,
                location TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER,
                org_id INTEGER,
                title TEXT,
                start_date TEXT,
                end_date TEXT,
                rank TEXT,
                note TEXT,
                FOREIGN KEY(person_id) REFERENCES persons(id),
                FOREIGN KEY(org_id) REFERENCES organizations(id)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_a INTEGER,
                person_b INTEGER,
                type TEXT,
                context TEXT,
                overlap_org TEXT,
                overlap_period TEXT,
                FOREIGN KEY(person_a) REFERENCES persons(id),
                FOREIGN KEY(person_b) REFERENCES persons(id)
            )
        """)

        for p in persons:
            cur.execute("""
                INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place, education, party_join, work_start, current_post, current_org, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (p["id"], p["name"], p.get("gender","待查"), p.get("ethnicity","待查"),
                  p.get("birth","待查"), p.get("birthplace","待查"), p.get("native_place","待查"),
                  p.get("education","待查"), p.get("party_join","中共党员"), p.get("work_start","待查"),
                  p.get("current_post","待查"), p.get("current_org","待查"), p.get("source","待查")))

        for o in organizations:
            cur.execute("""
                INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (o["id"], o["name"], o.get("type",""), o.get("level",""), o.get("parent",""), o.get("location","")))

        for pos in positions:
            cur.execute("""
                INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date","待查"),
                  pos.get("end_date","待查"), pos.get("rank","待查"), pos.get("note","")))

        for r in relationships:
            cur.execute("""
                INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (r["person_a"], r["person_b"], r["type"], r.get("context",""),
                  r.get("overlap_org",""), r.get("overlap_period","")))

        conn.commit()
        conn.close()

        # GEXF output
        gexf_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        gexf_xml += '<gexf xmlns="http://www.gexf.net/1.3" xmlns:viz="http://www.gexf.net/1.3/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.3 http://www.gexf.net/1.3/gexf.xsd" version="1.3">\n'
        gexf_xml += '  <graph mode="static" defaultedgetype="directed">\n'
        gexf_xml += '    <attributes class="node">\n'
        gexf_xml += '      <attribute id="type" title="type" type="string"/>\n'
        gexf_xml += '      <attribute id="current_post" title="current_post" type="string"/>\n'
        gexf_xml += '      <attribute id="birth" title="birth" type="string"/>\n'
        gexf_xml += '      <attribute id="source" title="source" type="string"/>\n'
        gexf_xml += '    </attributes>\n'
        gexf_xml += '    <attributes class="edge">\n'
        gexf_xml += '      <attribute id="type" title="type" type="string"/>\n'
        gexf_xml += '      <attribute id="context" title="context" type="string"/>\n'
        gexf_xml += '      <attribute id="overlap_period" title="overlap_period" type="string"/>\n'
        gexf_xml += '    </attributes>\n'

        gexf_xml += '    <nodes>\n'
        for p in persons:
            color_map = {"县委书记":"255,60,50", "县长":"50,100,255", "纪委书记":"255,165,0", "副书记":"100,180,100", "default":"200,200,200"}
            post = p.get("current_post","")
            color_str = "200,200,200"
            for k, v in color_map.items():
                if k in post:
                    color_str = v
                    break
            r_c, g_c, b_c = color_str.split(",")
            gexf_xml += f'      <node id="{p["id"]}" label="{p["name"]}">\n'
            gexf_xml += f'        <attvalues>\n'
            gexf_xml += f'          <attvalue for="type" value="person"/>\n'
            gexf_xml += f'          <attvalue for="current_post" value="{p.get("current_post","")}"/>\n'
            gexf_xml += f'          <attvalue for="birth" value="{p.get("birth","待查")}"/>\n'
            gexf_xml += f'          <attvalue for="source" value="official_gov_website_20260722"/>\n'
            gexf_xml += f'        </attvalues>\n'
            gexf_xml += f'        <viz:color r="{r_c}" g="{g_c}" b="{b_c}" a="1.0"/>\n'
            sz = "8.0" if "待查" in p["name"] else ("20.0" if "县委书记" in post else "12.0")
            gexf_xml += f'        <viz:size value="{sz}"/>\n'
            gexf_xml += f'        <viz:shape value="circle"/>\n'
            gexf_xml += f'      </node>\n'

        for o in organizations:
            gexf_xml += f'      <node id="{o["id"]+100}" label="{o["name"]}">\n'
            gexf_xml += f'        <attvalues>\n'
            gexf_xml += f'          <attvalue for="type" value="organization"/>\n'
            gexf_xml += f'        </attvalues>\n'
            gexf_xml += f'        <viz:color r="220" g="220" b="220" a="0.8"/>\n'
            gexf_xml += f'        <viz:size value="10.0"/>\n'
            gexf_xml += f'        <viz:shape value="square"/>\n'
            gexf_xml += f'      </node>\n'
        gexf_xml += '    </nodes>\n'

        gexf_xml += '    <edges>\n'
        edge_id = 0
        for pos in positions:
            edge_id += 1
            gexf_xml += f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{pos["org_id"]+100}" type="directed">\n'
            gexf_xml += f'        <attvalues>\n'
            gexf_xml += f'          <attvalue for="type" value="worked_at"/>\n'
            gexf_xml += f'          <attvalue for="context" value="{pos["title"]}"/>\n'
            gexf_xml += f'          <attvalue for="overlap_period" value="{pos.get("start_date","待查")}-{pos.get("end_date","待查")}"/>\n'
            gexf_xml += f'        </attvalues>\n'
            gexf_xml += f'      </edge>\n'
        for r in relationships:
            edge_id += 1
            gexf_xml += f'      <edge id="{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}" type="undirected">\n'
            gexf_xml += f'        <attvalues>\n'
            gexf_xml += f'          <attvalue for="type" value="{r["type"]}"/>\n'
            gexf_xml += f'          <attvalue for="context" value="{r.get("context","")}"/>\n'
            gexf_xml += f'          <attvalue for="overlap_period" value="{r.get("overlap_period","")}"/>\n'
            gexf_xml += f'        </attvalues>\n'
            gexf_xml += f'      </edge>\n'
        gexf_xml += '    </edges>\n'
        gexf_xml += '  </graph>\n'
        gexf_xml += '</gexf>\n'

        with open(gexf, 'w', encoding='utf-8') as f:
            f.write(gexf_xml)

    print()
    print(f"=== {SLUG} 网络数据构建完成 ===")
    print(f"人员: {len(persons)} 人（其中{sum(1 for p in persons if '待查' not in p['name'])}人已确认姓名）")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")
    print(f"数据库: {db}")
    print(f"GEXF: {gexf}")
    print()
    print("数据来源：")
    print("  [C] dabu.gov.cn — 确认凌晓文县长身份")
    print("  [C] dbjw.gov.cn — 确认黄增国县委书记、叶慧玲纪委书记身份")
    print("  [P] 训练数据 — 朱汉东、林健雄、刘彩波等前任领导信息")
    print("  [G] 信息缺失 — 专职副书记、常务副县长、组织部部长、宣传部部长姓名未确认")
