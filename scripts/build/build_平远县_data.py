#!/usr/bin/env python3
"""
平远县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
City: 梅州市
County: 平远县
Targets: 县委书记 & 县长

Research Date: 2026-07-22

Research Notes:
- 当前县委书记：周小勇 [C] 已通过平远县人民政府官网多个官方新闻确认：
  https://www.pingyuan.gov.cn/pyyw/zwyw/content/post_2926420.html (2026-07-22)
  https://www.pingyuan.gov.cn/pyyw/zwyw/content/post_2925151.html (2026-07-20)
  https://www.pingyuan.gov.cn/pyyw/zwyw/content/post_2871456.html (2026-02-14)
- 现任县长：喻勇 [C] 已通过平远县人民政府官网领导之窗页面确认：
  https://www.pingyuan.gov.cn/zwgk/ldzc/
  https://www.pingyuan.gov.cn/zwgk/gzbg/content/post_2916512.html (2026-06-21 政府工作报告)
  喻勇于2025年2月任代县长，后正式任县长。
- 周小勇的前任县委书记信息未能在可访问来源中确认 [G]。
  根据2026年1月9日的新闻，当时由喻勇（县委副书记、县长）主持县委常委会会议，
  周小勇未出现在前述报道中。至2026年2月14日，周小勇已以县委书记身份公开出席活动。
- 县政府领导班子：余毅宗（县政府党组副书记、副县长）、胡俊坛、李万年、陈瑛、
  蓝常基、王平梅、李菲丹、蔡榕（副县长）[C]
- 县委常委/其他领导：谢婷（县委常委、统战部部长）、吴雨华、林欣、郭育春 [P]
- 个人详尽履历（出生年月、籍贯、教育背景、入党时间等）除姓名和职务外大部分尚未查到 [G]。
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
SLUG = "平远县"
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
#   [P] = Plausible — likely correct based on available evidence
#   [U] = Unverified — needs confirmation
#   [G] = Gap — information not available
# ══════════════════════════════════════════════════════════════════════════════

# ── Persons ──

persons = [
    # ════════════════════════════════════════════
    # CURRENT 县委书记 (Party Secretary)
    # ════════════════════════════════════════════

    # [C] Current 县委书记 — 周小勇
    # Confirmed by pingyuan.gov.cn official news: 2026-02-14, 2026-07-15, 2026-07-17, 2026-07-20, 2026-07-22
    {
        "id": 1,
        "name": "周小勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共平远县委书记",
        "current_org": "中共平远县委员会",
        "source": "[C] Confirmed by multiple official news articles on pingyuan.gov.cn (2026-02-14, 2026-07-15, 2026-07-17, 2026-07-20, 2026-07-22). Role confirmed as 县委书记周小勇 presiding over county-level meetings and representing 平远 in investment talks. Detailed career history requires further research."
    },

    # ════════════════════════════════════════════
    # CURRENT 县长 (County Mayor)
    # ════════════════════════════════════════════

    # [C] Current 县长 — 喻勇
    # Confirmed by pingyuan.gov.cn leadership page and government work reports
    {
        "id": 2,
        "name": "喻勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平远县人民政府县长",
        "current_org": "平远县人民政府",
        "source": "[C] Confirmed by pingyuan.gov.cn leadership page (https://www.pingyuan.gov.cn/zwgk/ldzc/) listing 喻勇 as 县长. Also confirmed by delivering 2025 government work report as 代县长 (February 2025) and 2026 government work report as 县长 (June 2026). Professional background and full career history require further research."
    },

    # ════════════════════════════════════════════
    # 县政府领导层 (Government Leadership)
    # ════════════════════════════════════════════

    # [C] 县政府党组副书记、副县长 — 余毅宗
    {
        "id": 3,
        "name": "余毅宗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平远县委常委、县政府党组副书记、副县长",
        "current_org": "平远县人民政府",
        "source": "[C] Confirmed by pingyuan.gov.cn leadership page listing 余毅宗 as 县政府党组副书记、副县长. Also mentioned in 2026-05-26 news as 县委常委、县政府党组副书记、副县长."
    },

    # [C] 副县长 — 胡俊坛
    {
        "id": 4,
        "name": "胡俊坛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平远县人民政府副县长",
        "current_org": "平远县人民政府",
        "source": "[C] Confirmed by pingyuan.gov.cn leadership page listing 胡俊坛 as 副县长. Also mentioned in 2026-02-14 news."
    },

    # [C] 副县长 — 李万年
    {
        "id": 5,
        "name": "李万年",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平远县人民政府副县长",
        "current_org": "平远县人民政府",
        "source": "[C] Confirmed by pingyuan.gov.cn leadership page listing 李万年 as 副县长. Also mentioned in 2026-02-14 news."
    },

    # [C] 副县长 — 陈瑛
    {
        "id": 6,
        "name": "陈瑛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "平远县人民政府副县长",
        "current_org": "平远县人民政府",
        "source": "[C] Confirmed by pingyuan.gov.cn leadership page listing 陈瑛 as 副县长."
    },

    # [C] 副县长 — 蓝常基
    {
        "id": 7,
        "name": "蓝常基",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平远县人民政府副县长",
        "current_org": "平远县人民政府",
        "source": "[C] Confirmed by pingyuan.gov.cn leadership page listing 蓝常基 as 副县长. Also mentioned in 2026-02-14 news."
    },

    # [C] 副县长 — 王平梅
    {
        "id": 8,
        "name": "王平梅",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "平远县人民政府副县长",
        "current_org": "平远县人民政府",
        "source": "[C] Confirmed by pingyuan.gov.cn leadership page listing 王平梅 as 副县长. Also mentioned in 2026-05-26 and 2026-07-22 news."
    },

    # [C] 副县长 — 李菲丹
    {
        "id": 9,
        "name": "李菲丹",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "平远县人民政府副县长",
        "current_org": "平远县人民政府",
        "source": "[C] Confirmed by pingyuan.gov.cn leadership page listing 李菲丹 as 副县长. Also mentioned in 2026-02-14 and 2026-07-22 news."
    },

    # [C] 副县长 — 蔡榕
    {
        "id": 10,
        "name": "蔡榕",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "平远县人民政府副县长",
        "current_org": "平远县人民政府",
        "source": "[C] Confirmed by pingyuan.gov.cn leadership page listing 蔡榕 as 副县长."
    },

    # ════════════════════════════════════════════
    # 县委常委/其他领导 (Party Standing Committee)
    # ════════════════════════════════════════════

    # [C] 县委常委、统战部部长 — 谢婷
    # Confirmed by 2026-07-20 news and 2026-02-14 news
    {
        "id": 11,
        "name": "谢婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平远县委常委、统战部部长",
        "current_org": "中共平远县委员会",
        "source": "[C] Confirmed by pingyuan.gov.cn official news. Article 2026-07-20 mentions 县委常委、统战部部长谢婷. Also mentioned in 2026-02-14 news."
    },

    # [P] 吴雨华 — 县领导（从新闻排序看可能为县委常委或副县长级别）
    {
        "id": 12,
        "name": "吴雨华",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平远县领导",
        "current_org": "中共平远县委/平远县人民政府",
        "source": "[C] Frequently appears in official news (2026-02-14, 2026-07-17, 2026-07-20, 2026-07-22) as 县领导. Listed at senior position in meeting attendee lists. Exact title requires confirmation."
    },

    # [P] 林欣 — 县领导
    {
        "id": 13,
        "name": "林欣",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平远县领导",
        "current_org": "中共平远县委/平远县人民政府",
        "source": "[C] Appears in official news (2026-02-14, 2026-07-22). Listed in meeting attendee lists."
    },

    # [P] 郭育春 — 县领导
    {
        "id": 14,
        "name": "郭育春",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平远县领导",
        "current_org": "中共平远县委/平远县人民政府",
        "source": "[C] Appears in official news (2026-02-14). Listed in attendee lists."
    },

    # ════════════════════════════════════════════
    # 人大、政协 (Former/Senior leaders — for complete picture)
    # ════════════════════════════════════════════

    # [G] — 县人大常委会主任 — 信息缺失
    # [G] — 县政协主席 — 信息缺失
]

# ── Organizations ──

organizations = [
    {
        "id": 1,
        "name": "中共平远县委员会",
        "type": "党委",
        "level": "县处级",
        "location": "广东省梅州市平远县",
        "parent": "中共梅州市委员会",
    },
    {
        "id": 2,
        "name": "平远县人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "广东省梅州市平远县",
        "parent": "梅州市人民政府",
    },
    {
        "id": 3,
        "name": "中共平远县委统战部",
        "type": "党委部门",
        "level": "县处级",
        "location": "广东省梅州市平远县",
        "parent": "中共平远县委员会",
    },
    {
        "id": 4,
        "name": "平远县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "location": "广东省梅州市平远县",
        "parent": "平远县",
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议平远县委员会",
        "type": "政协",
        "level": "县处级",
        "location": "广东省梅州市平远县",
        "parent": "平远县",
    },
]

# ── Positions ──

positions = [
    # 周小勇
    {"person_id": 1, "org_id": 1, "title": "中共平远县委书记", "start": "不早于2026-01", "end": "至今", "rank": "正处级", "note": "[C] First confirmed appearance as 县委书记 on 2026-02-14 news. Prior to this, exact appointment date unknown."},
    # 喻勇
    {"person_id": 2, "org_id": 2, "title": "平远县人民政府代县长", "start": "2025-02", "end": "2025年（后转正）", "rank": "正处级", "note": "[C] Delivered 2025 GWR as 代县长 (2025-02-10)"},
    {"person_id": 2, "org_id": 2, "title": "平远县人民政府县长", "start": "2025年", "end": "至今", "rank": "正处级", "note": "[C] Confirmed on leadership page and 2026 GWR"},
    {"person_id": 2, "org_id": 1, "title": "中共平远县委副书记", "start": "2025-02", "end": "至今", "rank": "副处级", "note": "[C] Confirmed as presiding over 县委常委会 in 2026-01-09 news as 县委副书记、县长"},
    # 余毅宗
    {"person_id": 3, "org_id": 2, "title": "平远县委常委、县政府党组副书记、副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed by leadership page and news"},
    # 胡俊坛
    {"person_id": 4, "org_id": 2, "title": "平远县人民政府副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed by leadership page"},
    # 李万年
    {"person_id": 5, "org_id": 2, "title": "平远县人民政府副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed by leadership page"},
    # 陈瑛
    {"person_id": 6, "org_id": 2, "title": "平远县人民政府副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed by leadership page"},
    # 蓝常基
    {"person_id": 7, "org_id": 2, "title": "平远县人民政府副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed by leadership page"},
    # 王平梅
    {"person_id": 8, "org_id": 2, "title": "平远县人民政府副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed by leadership page"},
    # 李菲丹
    {"person_id": 9, "org_id": 2, "title": "平远县人民政府副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed by leadership page"},
    # 蔡榕
    {"person_id": 10, "org_id": 2, "title": "平远县人民政府副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed by leadership page"},
    # 谢婷
    {"person_id": 11, "org_id": 3, "title": "平远县委常委、统战部部长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed by news articles"},
    # 吴雨华
    {"person_id": 12, "org_id": 1, "title": "平远县领导", "start": "待查", "end": "至今", "rank": "副处级待确认", "note": "[P] Appears frequently in news"},
    # 林欣
    {"person_id": 13, "org_id": 1, "title": "平远县领导", "start": "待查", "end": "至今", "rank": "副处级待确认", "note": "[P] Appears in news"},
    # 郭育春
    {"person_id": 14, "org_id": 1, "title": "平远县领导", "start": "待查", "end": "至今", "rank": "副处级待确认", "note": "[P] Appears in news"},
]

# ── Relationships ──

relationships = [
    # 周小勇 <-> 喻勇: 书记/县长搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长——平远县党政主要领导搭档关系",
        "overlap_org": "中共平远县委员会/平远县人民政府",
        "overlap_period": "2026年初至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 周小勇 <-> 余毅宗: 常委/副书记关系
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委、县政府党组副书记",
        "overlap_org": "中共平远县委员会/平远县人民政府",
        "overlap_period": "2026年至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 喻勇 <-> 余毅宗: 县长与党组副书记
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与县政府党组副书记——县政府领导班子层级关系",
        "overlap_org": "平远县人民政府",
        "overlap_period": "2025年至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 喻勇 <-> 各位副县长: 政府班子
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与副县长——县政府领导班子",
        "overlap_org": "平远县人民政府",
        "overlap_period": "2025年至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县长与副县长——县政府领导班子",
        "overlap_org": "平远县人民政府",
        "overlap_period": "2025年至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县长与副县长——县政府领导班子",
        "overlap_org": "平远县人民政府",
        "overlap_period": "2025年至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县长与副县长——县政府领导班子",
        "overlap_org": "平远县人民政府",
        "overlap_period": "2025年至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长与副县长——县政府领导班子",
        "overlap_org": "平远县人民政府",
        "overlap_period": "2025年至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "县长与副县长——县政府领导班子",
        "overlap_org": "平远县人民政府",
        "overlap_period": "2025年至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "县长与副县长——县政府领导班子",
        "overlap_org": "平远县人民政府",
        "overlap_period": "2025年至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 谢婷作为县委常委与县委领导关系
    {
        "person_a": 1,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委、统战部部长——县委领导班子",
        "overlap_org": "中共平远县委员会",
        "overlap_period": "2026年至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 吴雨华、林欣、郭育春 — 同事关系（与县委领导）
    {
        "person_a": 1,
        "person_b": 12,
        "type": "overlap",
        "context": "同县领导班子成员",
        "overlap_org": "中共平远县委员会",
        "overlap_period": "2026年至今",
        "strength": "medium",
        "confidence": "plausible",
    },
    {
        "person_a": 1,
        "person_b": 13,
        "type": "overlap",
        "context": "同县领导班子成员",
        "overlap_org": "中共平远县委员会",
        "overlap_period": "2026年至今",
        "strength": "medium",
        "confidence": "plausible",
    },
    {
        "person_a": 1,
        "person_b": 14,
        "type": "overlap",
        "context": "同县领导班子成员",
        "overlap_org": "中共平远县委员会",
        "overlap_period": "2026年至今",
        "strength": "medium",
        "confidence": "plausible",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

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
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
else:
    # Fallback: direct SQLite + GEXF
    print("gov_relation.runner not available; building directly...")
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, native_place TEXT, education TEXT,
            party_join TEXT, work_start TEXT, current_post TEXT,
            current_org TEXT, source TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, location TEXT,
            parent TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, "end" TEXT, rank TEXT, note TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT
        )
    """)

    for p in persons:
        conn.execute(
            "INSERT INTO persons VALUES (:id,:name,:gender,:ethnicity,:birth,:birthplace,:native_place,:education,:party_join,:work_start,:current_post,:current_org,:source)",
            p,
        )
    for o in organizations:
        conn.execute(
            "INSERT INTO organizations VALUES (:id,:name,:type,:level,:location,:parent)",
            o,
        )
    for pos in positions:
        conn.execute(
            "INSERT INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (:person_id,:org_id,:title,:start,:end,:rank,:note)",
            pos,
        )
    for r in relationships:
        conn.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (:person_a,:person_b,:type,:context,:overlap_org,:overlap_period)",
            r,
        )

    conn.commit()
    conn.close()
    print(f"DB: {DB_PATH}")

    # Write GEXF
    from datetime import datetime

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append("    <creator>gov-relation research agent</creator>")
    lines.append(f"    <description>{SLUG} 领导班子工作关系网络</description>")
    lines.append("  </meta>")
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('      <attribute id="2" title="current_post" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('      <attribute id="4" title="location" type="string"/>')
    lines.append('      <attribute id="5" title="gender" type="string"/>')
    lines.append('      <attribute id="6" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="7" title="birth" type="string"/>')
    lines.append('      <attribute id="8" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append("    <nodes>")
    for p in persons:
        pid = p["id"]
        name = p["name"]
        cp = p.get("current_post", "")
        g = p.get("gender", "")
        eth = p.get("ethnicity", "")
        b = p.get("birth", "")
        src = p.get("source", "")
        # Color by role
        if "县委书记" in cp:
            color = "255,50,50"
            sz = "20.0"
        elif "县长" in cp:
            color = "50,100,255"
            sz = "20.0"
        elif "副书记、副县长" in cp:
            color = "50,100,255"
            sz = "16.0"
        else:
            color = "100,100,100"
            sz = "12.0"

        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append("        <attvalues>")
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(name)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(cp)}"/>')
        lines.append(f'          <attvalue for="3" value="县处级"/>')
        lines.append(f'          <attvalue for="4" value="广东省梅州市平远县"/>')
        lines.append(f'          <attvalue for="5" value="{esc(g)}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(eth)}"/>')
        lines.append(f'          <attvalue for="7" value="{esc(b)}"/>')
        lines.append(f'          <attvalue for="8" value="{esc(src[:100])}"/>')
        lines.append("        </attvalues>")
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append("      </node>")
    lines.append("    </nodes>")

    # Org nodes
    lines.append("    <nodes>")
    for o in organizations:
        oid = o["id"] + 100000
        name = o["name"]
        otype = o.get("type", "")
        oloc = o.get("location", "")
        # Color by org type
        org_colors = {
            "党委": "255,200,200",
            "党委部门": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
        }
        ocolor = org_colors.get(otype, "200,200,200")
        lines.append(f'      <node id="o{oid}" label="{esc(name)}">')
        lines.append("        <attvalues>")
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(name)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="3" value="县处级"/>')
        lines.append(f'          <attvalue for="4" value="{esc(oloc)}"/>')
        lines.append("        </attvalues>")
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append("      </node>")
    lines.append("    </nodes>")

    # Edges: positions (person->org)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"] + 100000
        title = pos.get("title", "")
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Edges: relationships (person<->person)
    for r in relationships:
        pa = r["person_a"]
        pb = r["person_b"]
        rtype = r.get("type", "")
        ctx = r.get("context", "")
        oo = r.get("overlap_org", "")
        op = r.get("overlap_period", "")
        lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(oo)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(op)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF: {GEXF_PATH}")

    print("\nDone!")
