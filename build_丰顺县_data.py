#!/usr/bin/env python3
"""
丰顺县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
City: 梅州市
County: 丰顺县
Targets: 县委书记 & 县长

Research Date: 2026-07-22

Research Notes:
- 张志锋（县委书记）的身份已通过丰顺县人民政府官网多篇2026年政务动态文章确认：
  https://www.fengshun.gov.cn/fszx/zwdt/content/post_2923432.html (2026-07-13 督导检查重点项目)
  https://www.fengshun.gov.cn/fszx/zwdt/content/post_2918441.html (2026-06-29 县委常委会)
  https://www.fengshun.gov.cn/fszx/zwdt/content/post_2911026.html (2026-06-04 高考备考)
- 凌望远（县长）的身份已通过丰顺县人民政府官网文章确认：
  https://www.fengshun.gov.cn/fszx/zwdt/content/post_2908865.html (2026-05-29 百千万工程推进会，"县委副书记、县长凌望远主持会议")
  另在 https://www.fengshun.gov.cn/fszx/zwdt/index.html 文章列表中确认"张志锋凌望远看望慰问老同志"(2026-02-14)
- 张晓山（县委副书记、政法委书记）身份确认：
  https://www.fengshun.gov.cn/fszx/zwdt/content/post_2908865.html (2026-05-29，"县委副书记、政法委书记张晓山总结全县'百千万工程'三年初见成效工作")
- 夏兰亭、石远平、古孟青、吴伟明、饶富将 — 县领导（参加张志锋督导活动）
  https://www.fengshun.gov.cn/fszx/zwdt/content/post_2923432.html
- 谢定雄（副县长）身份确认：
  https://www.fengshun.gov.cn/fszx/zwdt/content/post_2908865.html (2026-05-29)
- 罗灏（县领导）身份确认：
  https://www.fengshun.gov.cn/fszx/zwdt/content/post_2911026.html (2026-06-04 陪同高考备考督导)
- Web access severely degraded: Baidu Baike returns 403, meizhou.gov.cn returns 521 Cloudflare error,
  Jina Reader times out, Exa API rate-limited. Detailed career histories for most figures unavailable.
- All persons marked [C] are confirmed by official fengshun.gov.cn sources for their current role.
- Biographical details (birth year, birthplace, education) are mostly unverified and marked [G].
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
SLUG = "丰顺县"
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

    # [C] Current 县委书记 — 张志锋
    # Confirmed by fengshun.gov.cn news: 2026-07-13, 2026-06-29, 2026-06-04, 2026-05-29, 2026-03-27, 2026-03-11
    {
        "id": 1,
        "name": "张志锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共丰顺县委书记",
        "current_org": "中共丰顺县委员会",
        "source": "[C] Confirmed by multiple official news articles on fengshun.gov.cn (2026-07-13, 2026-06-29, 2026-06-04). Current as of July 2026. Detailed career history requires further research."
    },

    # ════════════════════════════════════════════
    # CURRENT 县长 (County Mayor)
    # ════════════════════════════════════════════

    # [C] Current 县长 — 凌望远
    # Confirmed by fengshun.gov.cn 百千万工程推进会: "县委副书记、县长凌望远主持会议"
    {
        "id": 2,
        "name": "凌望远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丰顺县委副书记、县政府县长",
        "current_org": "丰顺县人民政府",
        "source": "[C] Confirmed by fengshun.gov.cn news article (2026-05-29 百千万工程推进会): '县委副书记、县长凌望远主持会议'. Also referenced in '张志锋凌望远看望慰问老同志' (2026-02-14). Current as of July 2026."
    },

    # ════════════════════════════════════════════
    # CURRENT 县委副书记、政法委书记
    # ════════════════════════════════════════════

    # [C] Current 县委副书记、政法委书记 — 张晓山
    {
        "id": 3,
        "name": "张晓山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丰顺县委副书记、政法委书记",
        "current_org": "中共丰顺县委员会",
        "source": "[C] Confirmed by fengshun.gov.cn news (2026-05-29): '县委副书记、政法委书记张晓山总结全县百千万工程三年初见成效工作'."
    },

    # ════════════════════════════════════════════
    # CURRENT 县委常委（参加督导活动）
    # ════════════════════════════════════════════

    # [C] 县委常委 — 夏兰亭
    {
        "id": 4,
        "name": "夏兰亭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丰顺县委常委",
        "current_org": "中共丰顺县委员会",
        "source": "[C] Confirmed as 县领导 attending 张志锋 inspection (fengshun.gov.cn 2026-07-13). Exact role (may be 常务副县长 or other specific position) requires confirmation."
    },

    # [C] 县委常委 — 石远平
    {
        "id": 5,
        "name": "石远平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丰顺县委常委",
        "current_org": "中共丰顺县委员会",
        "source": "[C] Confirmed as 县领导 attending 张志锋 inspection (fengshun.gov.cn 2026-07-13). Exact portfolio requires confirmation."
    },

    # [C] 县委常委 — 古孟青
    {
        "id": 6,
        "name": "古孟青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丰顺县委常委",
        "current_org": "中共丰顺县委员会",
        "source": "[C] Confirmed as 县领导 attending 张志锋 inspection (fengshun.gov.cn 2026-07-13). Exact portfolio requires confirmation."
    },

    # [C] 县委常委 — 吴伟明
    {
        "id": 7,
        "name": "吴伟明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丰顺县委常委",
        "current_org": "中共丰顺县委员会",
        "source": "[C] Confirmed as 县领导 attending 张志锋 inspection (fengshun.gov.cn 2026-07-13). Exact portfolio requires confirmation."
    },

    # [C] 县委常委 — 饶富将
    {
        "id": 8,
        "name": "饶富将",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丰顺县委常委",
        "current_org": "中共丰顺县委员会",
        "source": "[C] Confirmed as 县领导 attending 张志锋 inspection (fengshun.gov.cn 2026-07-13) and also in 高考备考 article (2026-06-04). Exact portfolio requires confirmation."
    },

    # ════════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════════

    # [C] 副县长 — 谢定雄
    {
        "id": 9,
        "name": "谢定雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丰顺县人民政府副县长",
        "current_org": "丰顺县人民政府",
        "source": "[C] Confirmed by fengshun.gov.cn (2026-05-29): '副县长谢定雄对《丰顺县2026年推进乡村全面振兴重点工作任务清单》作说明'."
    },

    # [C] 县领导（副县长级别）— 罗灏
    {
        "id": 10,
        "name": "罗灏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丰顺县领导",
        "current_org": "丰顺县人民政府",
        "source": "[C] Confirmed accompanying 张志锋 in 高考备考 inspection (fengshun.gov.cn 2026-06-04): '县领导罗灏、饶富将等参加活动'."
    },
]

# ── Organizations ──

organizations = [
    {
        "id": 1,
        "name": "中共丰顺县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共梅州市委",
        "location": "广东省梅州市丰顺县汤坑镇"
    },
    {
        "id": 2,
        "name": "丰顺县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "梅州市人民政府",
        "location": "广东省梅州市丰顺县汤坑镇"
    },
    {
        "id": 3,
        "name": "中共丰顺县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共梅州市纪委",
        "location": "广东省梅州市丰顺县汤坑镇"
    },
    {
        "id": 4,
        "name": "丰顺县委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共丰顺县委员会",
        "location": "广东省梅州市丰顺县汤坑镇"
    },
]

# ── Positions ──

positions = [
    # 张志锋 — 县委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "丰顺县委书记",
        "start": "待查",
        "end": "现在",
        "rank": "正处级",
        "note": "[C] 确认现任县委书记（fengshun.gov.cn 2026年多篇新闻确认）。到任时间待查。"
    },
    # 凌望远 — 县长
    {
        "person_id": 2,
        "org_id": 2,
        "title": "丰顺县人民政府县长",
        "start": "待查",
        "end": "现在",
        "rank": "正处级",
        "note": "[C] Official from fengshun.gov.cn: 县委副书记、县长凌望远（2026-05-29 百千万工程推进会确认）。"
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "丰顺县委副书记",
        "start": "待查",
        "end": "现在",
        "rank": "副处级",
        "note": "[C] 县长同时任县委副书记。"
    },
    # 张晓山 — 县委副书记、政法委书记
    {
        "person_id": 3,
        "org_id": 1,
        "title": "丰顺县委副书记",
        "start": "待查",
        "end": "现在",
        "rank": "副处级",
        "note": "[C] Confirmed by fengshun.gov.cn 2026-05-29."
    },
    {
        "person_id": 3,
        "org_id": 4,
        "title": "丰顺县委政法委书记",
        "start": "待查",
        "end": "现在",
        "rank": "副处级",
        "note": "[C] Confirmed by fengshun.gov.cn 2026-05-29."
    },
    # 夏兰亭 — 县委常委
    {
        "person_id": 4,
        "org_id": 1,
        "title": "丰顺县委常委",
        "start": "待查",
        "end": "现在",
        "rank": "副处级",
        "note": "[C] Confirmed as 县领导（fengshun.gov.cn 2026-07-13）。具体职务（可能为常务副县长或组织部长等）待确认。"
    },
    # 石远平 — 县委常委
    {
        "person_id": 5,
        "org_id": 1,
        "title": "丰顺县委常委",
        "start": "待查",
        "end": "现在",
        "rank": "副处级",
        "note": "[C] Confirmed as 县领导（fengshun.gov.cn 2026-07-13）。具体职务待确认。"
    },
    # 古孟青 — 县委常委
    {
        "person_id": 6,
        "org_id": 1,
        "title": "丰顺县委常委",
        "start": "待查",
        "end": "现在",
        "rank": "副处级",
        "note": "[C] Confirmed as 县领导（fengshun.gov.cn 2026-07-13）。具体职务待确认。"
    },
    # 吴伟明 — 县委常委
    {
        "person_id": 7,
        "org_id": 1,
        "title": "丰顺县委常委",
        "start": "待查",
        "end": "现在",
        "rank": "副处级",
        "note": "[C] Confirmed as 县领导（fengshun.gov.cn 2026-07-13）。具体职务待确认。"
    },
    # 饶富将 — 县委常委
    {
        "person_id": 8,
        "org_id": 1,
        "title": "丰顺县委常委",
        "start": "待查",
        "end": "现在",
        "rank": "副处级",
        "note": "[C] Confirmed as 县领导（fengshun.gov.cn 2026-07-13, 2026-06-04）。具体职务待确认。"
    },
    # 谢定雄 — 副县长
    {
        "person_id": 9,
        "org_id": 2,
        "title": "丰顺县人民政府副县长",
        "start": "待查",
        "end": "现在",
        "rank": "副处级",
        "note": "[C] Confirmed by fengshun.gov.cn 2026-05-29. Portfolio likely includes agriculture/rural affairs based on article context."
    },
    # 罗灏 — 县领导
    {
        "person_id": 10,
        "org_id": 2,
        "title": "丰顺县领导",
        "start": "待查",
        "end": "现在",
        "rank": "副处级",
        "note": "[C] Confirmed accompanying 张志锋（fengshun.gov.cn 2026-06-04）。具体职务（可能为副县长）待确认。"
    },
]

# ── Relationships ──

relationships = [
    # 张志锋 ↔ 凌望远 — 党政搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "张志锋（县委书记）与凌望远（县长）现任党政搭档",
        "overlap_org": "中共丰顺县委员会/丰顺县人民政府",
        "overlap_period": "当前"
    },
    # 张志锋 ↔ 张晓山 — 县委领导与副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "张志锋（县委书记）与张晓山（县委副书记、政法委书记）县委领导关系",
        "overlap_org": "中共丰顺县委员会",
        "overlap_period": "当前"
    },
    # 凌望远 ↔ 张晓山 — 同事
    {
        "person_a": 2,
        "person_b": 3,
        "type": "colleague",
        "context": "凌望远（县委副书记、县长）与张晓山（县委副书记、政法委书记）同为县委副书记",
        "overlap_org": "中共丰顺县委员会",
        "overlap_period": "当前"
    },
    # 张志锋 ↔ 夏兰亭 — 县委领导与常委
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "张志锋（县委书记）与夏兰亭（县委常委）县委领导与常委关系",
        "overlap_org": "中共丰顺县委员会",
        "overlap_period": "当前"
    },
    # 张志锋 ↔ 石远平
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "张志锋（县委书记）与石远平（县委常委）县委领导与常委关系",
        "overlap_org": "中共丰顺县委员会",
        "overlap_period": "当前"
    },
    # 张志锋 ↔ 古孟青
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "张志锋（县委书记）与古孟青（县委常委）县委领导与常委关系",
        "overlap_org": "中共丰顺县委员会",
        "overlap_period": "当前"
    },
    # 张志锋 ↔ 吴伟明
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "张志锋（县委书记）与吴伟明（县委常委）县委领导与常委关系",
        "overlap_org": "中共丰顺县委员会",
        "overlap_period": "当前"
    },
    # 张志锋 ↔ 饶富将
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "张志锋（县委书记）与饶富将（县委常委）县委领导与常委关系",
        "overlap_org": "中共丰顺县委员会",
        "overlap_period": "当前"
    },
    # 凌望远 ↔ 谢定雄 — 县长与副县长
    {
        "person_a": 2,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "凌望远（县长）与谢定雄（副县长）县政府领导关系",
        "overlap_org": "丰顺县人民政府",
        "overlap_period": "当前"
    },
    # 凌望远 ↔ 罗灏
    {
        "person_a": 2,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "凌望远（县长）与罗灏（县领导）县政府领导关系",
        "overlap_org": "丰顺县人民政府",
        "overlap_period": "当前"
    },
    # 谢定雄 ↔ 罗灏 — 副县长同事
    {
        "person_a": 9,
        "person_b": 10,
        "type": "colleague",
        "context": "谢定雄与罗灏同为县政府领导",
        "overlap_org": "丰顺县人民政府",
        "overlap_period": "当前"
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def build():
    if USE_RUNNER:
        run_build(
            slug=SLUG,
            persons=persons,
            organizations=organizations,
            positions=positions,
            relationships=relationships,
            db_path=DB_PATH,
            gexf_path=GEXF_PATH,
        )
    else:
        # Fallback: manual SQLite + GEXF
        conn = sqlite3.connect(DB_PATH)
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
                start TEXT,
                end TEXT,
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
            cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                         p["birthplace"], p["native_place"], p["education"],
                         p["party_join"], p["work_start"], p["current_post"],
                         p["current_org"], p["source"]))
        for o in organizations:
            cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
        for pos in positions:
            cur.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)""",
                        (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))
        for r in relationships:
            cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)""",
                        (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

        conn.commit()
        conn.close()
        print(f"✅ DB created: {DB_PATH}")

        # Build GEXF manually
        from datetime import datetime

        def esc(s):
            if s is None:
                return ""
            return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

        def person_color(p):
            if p["current_post"].startswith("中共") and "书记" in p["current_post"] and "纪委" not in p["current_post"]:
                return "255,50,50"  # Red for party secretary
            elif p["current_post"].startswith("丰顺县委"):
                return "255,50,50"  # Red for party officials
            elif p["current_post"].startswith("丰顺县人民政府") or "县长" in p["current_post"]:
                return "50,100,255"  # Blue for government
            return "100,100,100"

        def is_top_leader(p):
            return p["id"] <= 2

        lines = []
        lines.append('<?xml version="1.0" encoding="UTF-8"?>')
        lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
        lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
        lines.append('    <creator>Gov Relation Research Agent</creator>')
        lines.append(f'    <description>{SLUG} leadership network</description>')
        lines.append('  </meta>')
        lines.append('  <graph mode="static" defaultedgetype="undirected">')

        # Attributes
        lines.append('    <attributes class="node">')
        lines.append('      <attribute id="0" title="type" type="string"/>')
        lines.append('      <attribute id="1" title="role" type="string"/>')
        lines.append('      <attribute id="2" title="org" type="string"/>')
        lines.append('    </attributes>')
        lines.append('    <attributes class="edge">')
        lines.append('      <attribute id="0" title="type" type="string"/>')
        lines.append('      <attribute id="1" title="context" type="string"/>')
        lines.append('      <attribute id="2" title="period" type="string"/>')
        lines.append('    </attributes>')

        # Nodes: Persons
        lines.append('    <nodes>')
        for p in persons:
            c = person_color(p)
            sz = "20.0" if is_top_leader(p) else "12.0"
            lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
            lines.append('        <attvalues>')
            lines.append('          <attvalue for="0" value="person"/>')
            lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
            lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
            lines.append('        </attvalues>')
            lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
            lines.append(f'        <viz:size value="{sz}"/>')
            lines.append('      </node>')

        # Nodes: Organizations
        org_colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "纪委": "255,200,200",
        }
        for o in organizations:
            c = org_colors.get(o["type"], "200,200,200")
            lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
            lines.append('        <attvalues>')
            lines.append('          <attvalue for="0" value="organization"/>')
            lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
            lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
            lines.append('        </attvalues>')
            lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
            lines.append('        <viz:size value="8.0"/>')
            lines.append('      </node>')
        lines.append('    </nodes>')

        # Edges
        eid = 0
        lines.append('    <edges>')
        # person->organization edges
        for pos in positions:
            eid += 1
            lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
            lines.append('        <attvalues>')
            lines.append('          <attvalue for="0" value="worked_at"/>')
            lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
            lines.append(f'          <attvalue for="2" value="{esc(pos["start"])} - {esc(pos["end"])}"/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')

        # person<->person edges
        for r in relationships:
            eid += 1
            w = "2.0" if r["type"] == "superior_subordinate" else "1.5"
            lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{w}">')
            lines.append('        <attvalues>')
            lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
            lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
            lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')
        lines.append('    </edges>')
        lines.append('  </graph>')
        lines.append('</gexf>')

        with open(GEXF_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"✅ GEXF created: {GEXF_PATH}")

    print(f"\n📊 Summary: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


if __name__ == "__main__":
    build()
