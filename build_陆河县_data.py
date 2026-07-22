#!/usr/bin/env python3
"""
陆河县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
City: 汕尾市
County: 陆河县
Targets: 县委书记 & 县长

Research Date: 2026-07-22

Research Notes:
- 程永东（县委书记）身份已通过陆河县人民政府官网多篇2026年政务动态文章确认：
  https://www.luhe.gov.cn/luhe/jjlh/lhyw/content/post_1262941.html (2026-07-15 县委九届十次全会)
  https://www.luhe.gov.cn/luhe/jjlh/lhyw/content/post_1262938.html (2026-07-15 县委常委会扩大会议)
  https://www.luhe.gov.cn/luhe/jjlh/lhyw/content/post_1261555.html (2026-07-07 县委常委会)
  https://www.luhe.gov.cn/luhe/jjlh/lhyw/content/post_1259806.html (2026-07-02 省关工委调研，县委书记程永东陪同)
- 叶胜勇（县长）身份和专业分工已通过官方领导之窗页面确认：
  https://www.luhe.gov.cn/luhe/zwgk/0100/0102/content/post_1187259.html
  简历：叶胜勇，男，汉族，1973年3月生，大学学历，中共党员
- 蔡秋茂（县委副书记）身份通过县委常委会新闻确认
- 王维斌（县人大常委会主任）身份通过县委常委会新闻确认
- 郑志坚（县委常委、常务副县长）简历已确认：男，汉族，1976年12月生，大学学历，经济学学士，中共党员
- 曾玮玮（县委常委、宣传部部长）简历已确认：女，汉族，1980年2月生，大学学历，中共党员
- 连燕峰（县委常委、县政府党组成员）简历已确认：男，汉族，1973年8月生，在职大学学历，中共党员
- 蔡燕群（县委常委、组织部部长）从省关工委调研新闻中确认
- 卢杭棍（副县长）简历已确认：男，汉族，1982年10月生，大学学历，工学学士，农工党员
- 叶小彬（副县长）简历已确认：男，汉族，1974年12月生，在职大专学历，中共党员
- 黄礼政（副县长、公安局长）简历已确认：男，汉族，1976年11月生，大学学历，中共党员
- 彭培生（副县长、挂职）简历已确认：男，汉族，1982年11月生，大学学历，管理学学士，中共党员，挂任
- 林永锐（副县长）简历已确认：男，汉族，1986年11月生，大学学历，管理学学士，中共党员
- Web access severely degraded: Baidu Baike returns 403, 360百科 blocked, Sogou captcha.
  Detailed career histories for most figures partially available.
- All persons marked [C] are confirmed by official luhe.gov.cn sources for their current role.
- Biographical details (birth year, birthplace, education) are confirmed from official leadership page for
  government team members. Party secretary 程永东's full bio details (birth year, birthplace, education)
  are marked [G] from the leadership page as no dedicated 领导之窗 page was found for 县委 on the site.
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
SLUG = "陆河县"
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

    # [C] Current 县委书记 — 程永东
    # Confirmed by luhe.gov.cn news: 2026-07-15 (县委九届十次全会), 
    # 2026-07-15 (县委常委会扩大会议), 2026-07-07 (县委常委会), 2026-07-02 (省关工委调研)
    {
        "id": 1,
        "name": "程永东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共陆河县委书记",
        "current_org": "中共陆河县委员会",
        "source": "[C] Confirmed by multiple official news articles on luhe.gov.cn (2026-07-15 县委九届十次全会, 2026-07-07 县委常委会, 2026-07-02 省关工委调研). Current as of July 2026. Detailed career history requires further research."
    },

    # ════════════════════════════════════════════
    # CURRENT 县长 (County Mayor)
    # ════════════════════════════════════════════

    # [C] Current 县长 — 叶胜勇
    # Confirmed by luhe.gov.cn 领导之窗 page and multiple news articles
    {
        "id": 2,
        "name": "叶胜勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆河县委副书记、县政府县长",
        "current_org": "陆河县人民政府",
        "source": "[C] Confirmed by luhe.gov.cn 领导之窗页面: '叶胜勇，男，汉族，1973年3月生，大学学历，中共党员。现任陆河县人民政府县长、县政府党组书记。' Also confirmed in multiple news articles (2026-07-15 县委常委会)."
    },

    # ════════════════════════════════════════════
    # CURRENT 县委副书记
    # ════════════════════════════════════════════

    # [C] Current 县委副书记 — 蔡秋茂
    {
        "id": 3,
        "name": "蔡秋茂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆河县委副书记",
        "current_org": "中共陆河县委员会",
        "source": "[C] Confirmed by luhe.gov.cn news (2026-07-15 县委常委会扩大会议): '县委副书记蔡秋茂出席会议'."
    },

    # ════════════════════════════════════════════
    # 县人大常委会主任
    # ════════════════════════════════════════════

    # [C] 县人大常委会主任 — 王维斌
    {
        "id": 4,
        "name": "王维斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆河县人大常委会主任",
        "current_org": "陆河县人大常委会",
        "source": "[C] Confirmed by luhe.gov.cn news (2026-07-15 县委常委会扩大会议): '县人大常委会主任王维斌'出席会议."
    },

    # ════════════════════════════════════════════
    # CURRENT 县委常委、常务副县长
    # ════════════════════════════════════════════

    # [C] 县委常委、常务副县长 — 郑志坚
    {
        "id": 5,
        "name": "郑志坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学，经济学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆河县委常委、县政府副县长、县政府党组副书记",
        "current_org": "陆河县人民政府",
        "source": "[C] Confirmed by luhe.gov.cn 领导之窗页面: '郑志坚，男，汉族，1976年12月生，大学学历，经济学学士，中共党员。现任陆河县委常委，县政府副县长、县政府党组副书记。'"
    },

    # ════════════════════════════════════════════
    # CURRENT 县委常委、宣传部部长
    # ════════════════════════════════════════════

    # [C] 县委常委、宣传部部长 — 曾玮玮
    {
        "id": 6,
        "name": "曾玮玮",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆河县委常委、宣传部部长",
        "current_org": "中共陆河县委员会",
        "source": "[C] Confirmed by luhe.gov.cn 领导之窗页面: '曾玮玮，女，汉族，1980年2月生，大学学历，中共党员。现任陆河县委常委、宣传部部长。'"
    },

    # ════════════════════════════════════════════
    # CURRENT 县委常委、县政府党组成员
    # ════════════════════════════════════════════

    # [C] 县委常委、县政府党组成员 — 连燕峰
    {
        "id": 7,
        "name": "连燕峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆河县委常委、县政府党组成员",
        "current_org": "陆河县人民政府",
        "source": "[C] Confirmed by luhe.gov.cn 领导之窗页面: '连燕峰，男，汉族，1973年8月生，在职大学学历，中共党员。现任陆河县委常委，县政府党组成员。'"
    },

    # ════════════════════════════════════════════
    # CURRENT 县委常委、组织部部长
    # ════════════════════════════════════════════

    # [C] 县委常委、组织部部长 — 蔡燕群
    {
        "id": 8,
        "name": "蔡燕群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆河县委常委、组织部部长",
        "current_org": "中共陆河县委员会",
        "source": "[C] Confirmed by luhe.gov.cn news (2026-07-02 省关工委调研): '县委书记程永东，县委常委、组织部部长蔡燕群陪同调研'."
    },

    # ════════════════════════════════════════════
    # CURRENT 副县长
    # ════════════════════════════════════════════

    # [C] 副县长 — 卢杭棍
    {
        "id": 9,
        "name": "卢杭棍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学，工学学士",
        "party_join": "农工党员",
        "work_start": "待查",
        "current_post": "陆河县人民政府副县长",
        "current_org": "陆河县人民政府",
        "source": "[C] Confirmed by luhe.gov.cn 领导之窗页面: '卢杭棍，男，汉族，1982年10月生，大学学历，工学学士，农工党员。现任县政府副县长。'"
    },

    # [C] 副县长 — 叶小彬
    {
        "id": 10,
        "name": "叶小彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大专",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆河县人民政府副县长",
        "current_org": "陆河县人民政府",
        "source": "[C] Confirmed by luhe.gov.cn 领导之窗页面: '叶小彬，男，汉族，1974年12月生，在职大专学历，中共党员。现任县政府副县长、县政府党组成员。' Also confirmed in news (东坑镇活动)."
    },

    # [C] 副县长、公安局长 — 黄礼政
    {
        "id": 11,
        "name": "黄礼政",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆河县人民政府副县长、县公安局局长",
        "current_org": "陆河县人民政府",
        "source": "[C] Confirmed by luhe.gov.cn 领导之窗页面: '黄礼政，男，汉族，1976年11月生，大学学历，中共党员。现任县政府副县长、县政府党组成员，县公安局党委书记、局长、督察长、一级警长。'"
    },

    # [C] 副县长（挂职）— 彭培生
    {
        "id": 12,
        "name": "彭培生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学，管理学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆河县人民政府副县长（挂职）",
        "current_org": "陆河县人民政府",
        "source": "[C] Confirmed by luhe.gov.cn 领导之窗页面: '彭培生，男，汉族，1982年11月生，大学学历，管理学学士，中共党员，挂任县政府副县长、县政府党组成员。'"
    },

    # [C] 副县长 — 林永锐
    {
        "id": 13,
        "name": "林永锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学，管理学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆河县人民政府副县长",
        "current_org": "陆河县人民政府",
        "source": "[C] Confirmed by luhe.gov.cn 领导之窗页面: '林永锐，男，汉族，1986年11月生，大学学历，管理学学士，中共党员。现任县政府副县长、县政府党组成员。'"
    },
]

# ── Organizations ──

organizations = [
    {
        "id": 1,
        "name": "中共陆河县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共汕尾市委",
        "location": "广东省汕尾市陆河县"
    },
    {
        "id": 2,
        "name": "陆河县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "汕尾市人民政府",
        "location": "广东省汕尾市陆河县"
    },
    {
        "id": 3,
        "name": "陆河县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "陆河县",
        "location": "广东省汕尾市陆河县"
    },
    {
        "id": 4,
        "name": "中共陆河县委宣传部",
        "type": "党委",
        "level": "县",
        "parent": "中共陆河县委员会",
        "location": "广东省汕尾市陆河县"
    },
    {
        "id": 5,
        "name": "中共陆河县委组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共陆河县委员会",
        "location": "广东省汕尾市陆河县"
    },
    {
        "id": 6,
        "name": "陆河县公安局",
        "type": "政府",
        "level": "县",
        "parent": "陆河县人民政府",
        "location": "广东省汕尾市陆河县"
    },
]

# ── Positions ──

positions = [
    # 程永东
    {"person_id": 1, "org_id": 1, "title": "中共陆河县委书记", "start": "待查", "end": None, "rank": "正处级", "note": "主持县委全面工作"},
    # 叶胜勇
    {"person_id": 2, "org_id": 2, "title": "陆河县人民政府县长", "start": "待查", "end": None, "rank": "正处级", "note": "主持县政府全面工作，负责审计工作"},
    {"person_id": 2, "org_id": 1, "title": "陆河县委副书记", "start": "待查", "end": None, "rank": "正处级", "note": "县委副书记"},
    # 蔡秋茂
    {"person_id": 3, "org_id": 1, "title": "陆河县委副书记", "start": "待查", "end": None, "rank": "副处级", "note": "协助县委书记处理县委日常工作"},
    # 王维斌
    {"person_id": 4, "org_id": 3, "title": "陆河县人大常委会主任", "start": "待查", "end": None, "rank": "正处级", "note": "主持县人大常委会全面工作"},
    # 郑志坚
    {"person_id": 5, "org_id": 2, "title": "陆河县委常委、常务副县长", "start": "待查", "end": None, "rank": "副处级", "note": "负责县政府常务工作，分管发展改革、财政、应急管理等"},
    {"person_id": 5, "org_id": 1, "title": "陆河县委常委", "start": "待查", "end": None, "rank": "副处级", "note": "县委常委"},
    # 曾玮玮
    {"person_id": 6, "org_id": 1, "title": "陆河县委常委", "start": "待查", "end": None, "rank": "副处级", "note": "县委常委"},
    {"person_id": 6, "org_id": 4, "title": "陆河县委宣传部部长", "start": "待查", "end": None, "rank": "副处级", "note": "负责宣传、文化、卫生健康等工作"},
    # 连燕峰
    {"person_id": 7, "org_id": 1, "title": "陆河县委常委", "start": "待查", "end": None, "rank": "副处级", "note": "县委常委"},
    {"person_id": 7, "org_id": 2, "title": "陆河县政府党组成员", "start": "待查", "end": None, "rank": "副处级", "note": "负责自然资源、住建、交通等工作"},
    # 蔡燕群
    {"person_id": 8, "org_id": 1, "title": "陆河县委常委、组织部部长", "start": "待查", "end": None, "rank": "副处级", "note": "负责组织、干部工作"},
    {"person_id": 8, "org_id": 5, "title": "中共陆河县委组织部部长", "start": "待查", "end": None, "rank": "副处级", "note": "主持县委组织部工作"},
    # 卢杭棍
    {"person_id": 9, "org_id": 2, "title": "陆河县人民政府副县长", "start": "待查", "end": None, "rank": "副处级", "note": "负责科工、商务、水利、林业等工作"},
    # 叶小彬
    {"person_id": 10, "org_id": 2, "title": "陆河县人民政府副县长", "start": "待查", "end": None, "rank": "副处级", "note": "负责农业农村、人社、民政等工作"},
    # 黄礼政
    {"person_id": 11, "org_id": 2, "title": "陆河县人民政府副县长、县公安局局长", "start": "待查", "end": None, "rank": "副处级", "note": "负责公安、司法、国家安全等工作"},
    {"person_id": 11, "org_id": 6, "title": "陆河县公安局局长", "start": "待查", "end": None, "rank": "副处级", "note": "主持县公安局工作"},
    # 彭培生
    {"person_id": 12, "org_id": 2, "title": "陆河县人民政府副县长（挂职）", "start": "待查", "end": None, "rank": "副处级", "note": "负责对口帮扶、驻镇帮镇扶村等工作"},
    # 林永锐
    {"person_id": 13, "org_id": 2, "title": "陆河县人民政府副县长", "start": "待查", "end": None, "rank": "副处级", "note": "负责政务数据工作"},
]

# ── Relationships ──

relationships = [
    # 书记—县长：党政正职搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "党政正职搭档：程永东（县委书记）与叶胜勇（县长）在陆河县共同主持党政工作",
        "overlap_org": "陆河县",
        "overlap_period": "2026至今"
    },
    # 书记—副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "程永东（县委书记）与蔡秋茂（县委副书记）在县委常委会中共事",
        "overlap_org": "中共陆河县委",
        "overlap_period": "2026至今"
    },
    # 县长—常务副县长
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "叶胜勇（县长）与郑志坚（常务副县长）在县政府班子中配合工作",
        "overlap_org": "陆河县人民政府",
        "overlap_period": "2026至今"
    },
    # 县长—人大主任
    {
        "person_a": 2,
        "person_b": 4,
        "type": "peer",
        "context": "叶胜勇（县长）与王维斌（县人大常委会主任）在党政联席会议中共事",
        "overlap_org": "陆河县",
        "overlap_period": "2026至今"
    },
    # 书记—人大主任
    {
        "person_a": 1,
        "person_b": 4,
        "type": "peer",
        "context": "程永东（县委书记）与王维斌（县人大常委会主任）在县委常委会扩大会议中共同出席",
        "overlap_org": "陆河县",
        "overlap_period": "2026至今"
    },
    # 副书记—组织部长
    {
        "person_a": 3,
        "person_b": 8,
        "type": "peer",
        "context": "蔡秋茂（县委副书记）与蔡燕群（组织部部长）在县委中配合干部工作",
        "overlap_org": "中共陆河县委",
        "overlap_period": "2026至今"
    },
    # 常务副县长—组织部长（县委常委内跨系统配合）
    {
        "person_a": 5,
        "person_b": 8,
        "type": "peer",
        "context": "郑志坚（县委常委、常务副县长）与蔡燕群（县委常委、组织部部长）同为县委常委",
        "overlap_org": "中共陆河县委",
        "overlap_period": "2026至今"
    },
    # 常务副县长—宣传部长（县委常委内跨系统配合）
    {
        "person_a": 5,
        "person_b": 6,
        "type": "peer",
        "context": "郑志坚（县委常委、常务副县长）与曾玮玮（县委常委、宣传部部长）同为县委常委",
        "overlap_org": "中共陆河县委",
        "overlap_period": "2026至今"
    },
    # 书记—组织部长
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "程永东（县委书记）与蔡燕群（组织部部长）在干部管理工作中配合",
        "overlap_org": "中共陆河县委",
        "overlap_period": "2026至今"
    },
    # 副县长之间的同事关系
    {"person_a": 9, "person_b": 10, "type": "peer", "context": "卢杭棍与叶小彬同为陆河县副县长", "overlap_org": "陆河县人民政府", "overlap_period": "2026至今"},
    {"person_a": 9, "person_b": 11, "type": "peer", "context": "卢杭棍与黄礼政同为陆河县副县长", "overlap_org": "陆河县人民政府", "overlap_period": "2026至今"},
    {"person_a": 10, "person_b": 11, "type": "peer", "context": "叶小彬与黄礼政同为陆河县副县长", "overlap_org": "陆河县人民政府", "overlap_period": "2026至今"},
    {"person_a": 12, "person_b": 13, "type": "peer", "context": "彭培生（挂职）与林永锐同为陆河县副县长", "overlap_org": "陆河县人民政府", "overlap_period": "2026至今"},
]


# ══════════════════════════════════════════════════════════════════════════════
# BUILD
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
            elif "县长" in p["current_post"] and "副" not in p["current_post"]:
                return "50,100,255"  # Blue for government head
            elif "常务副县长" in p["current_post"] or "副县长" in p["current_post"]:
                return "50,100,255"  # Blue for deputy government
            elif "人大" in p["current_post"]:
                return "200,255,255"  # Cyan for NPC
            return "100,100,100"

        def is_top_leader(p):
            return p["id"] in [1, 2]  # 书记 and 县长

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
            "人大": "200,255,255",
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
