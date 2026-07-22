#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 武山县 (Wushan County), 天水市, 甘肃省.

武山县 — 甘肃省天水市下辖县, 位于天水市西北部, 渭河上游.
Covers current County Party Secretary (王龙强), County Magistrate (赵百祥),
their predecessors, and leadership team.

Current leadership as of 2026-07:
  - 王龙强 (县委书记, appointed ~September 2025)
  - 赵百祥 (县长, elected January 2025)

Reference sources:
  - 武山县人民政府官网领导之窗: https://www.wushan.gov.cn/ldzc1/ldjj.htm
  - 天水市人民政府: https://www.tianshui.gov.cn
  - 网易/澎湃新闻: 人事任免报道
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/gansu_武山县")
os.makedirs(TMP, exist_ok=True)

DB_PATH = os.path.join(TMP, "武山县_network.db")
GEXF_PATH = os.path.join(TMP, "武山县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════
    # CURRENT TOP LEADERS
    # ═══════════════════════════════════════════════════════════

    # 王龙强 — 武山县委书记 (as of 2025.09)
    {"id": 1, "name": "王龙强", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-07", "birthplace": "甘肃永昌",
     "education": "博士研究生学历（甘肃农业大学，农学博士）",
     "party_join": "中共党员", "work_start": "2005",
     "current_post": "武山县委书记",
     "current_org": "中共武山县委员会",
     "source": "https://www.wushan.gov.cn/; 网易新闻2025-09-11; 澎湃新闻2021-07-20任前公示"},

    # 赵百祥 — 武山县委副书记、县长 (as of 2025.01)
    {"id": 2, "name": "赵百祥", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-07", "birthplace": "甘肃秦州",
     "education": "省委党校本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武山县委副书记、县长",
     "current_org": "武山县人民政府",
     "source": "https://www.wushan.gov.cn/ldzc1/; 天水在线2024-12-06; 百度百科"},

    # ═══════════════════════════════════════════════════════════
    # FOUR MAJOR LEADERSHIP (四大班子)
    # ═══════════════════════════════════════════════════════════

    # 李海巴 — 县委副书记（专职）
    {"id": 3, "name": "李海巴", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武山县委副书记（专职）",
     "current_org": "中共武山县委员会",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # 孙德银 — 县人大常委会主任
    {"id": 4, "name": "孙德银", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武山县人大常委会主任",
     "current_org": "武山县人民代表大会常务委员会",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # 秦福才 — 县政协主席
    {"id": 5, "name": "秦福才", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武山县政协主席",
     "current_org": "中国人民政治协商会议武山县委员会",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # ═══════════════════════════════════════════════════════════
    # STANDING COMMITTEE MEMBERS (县委常委)
    # ═══════════════════════════════════════════════════════════

    # 胡小云 — 县委常委
    {"id": 6, "name": "胡小云", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武山县委常委",
     "current_org": "中共武山县委员会",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # 刘忠锋 — 县委常委、副县长
    {"id": 7, "name": "刘忠锋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武山县委常委、副县长",
     "current_org": "中共武山县委员会/武山县人民政府",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # 赵强 — 县委常委、副县长
    {"id": 8, "name": "赵强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武山县委常委、副县长",
     "current_org": "中共武山县委员会/武山县人民政府",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # 王宏 — 县委常委
    {"id": 9, "name": "王宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武山县委常委",
     "current_org": "中共武山县委员会",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # 王想成 — 县委常委、城关镇党委书记
    {"id": 10, "name": "王想成", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武山县委常委、城关镇党委书记",
     "current_org": "中共武山县委员会/武山县城关镇",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # 张淑香 — 县委常委、副县长
    {"id": 11, "name": "张淑香", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武山县委常委、副县长",
     "current_org": "中共武山县委员会/武山县人民政府",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # 李玉兰 — 县委常委、宣传部部长
    {"id": 12, "name": "李玉兰", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武山县委常委、宣传部部长",
     "current_org": "中共武山县委员会",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # 郗智聪 — 县委常委
    {"id": 13, "name": "郗智聪", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武山县委常委",
     "current_org": "中共武山县委员会",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # ═══════════════════════════════════════════════════════════
    # OTHER DEPUTY MAYORS (副县长)
    # ═══════════════════════════════════════════════════════════

    # 谢怀东 — 副县长
    {"id": 14, "name": "谢怀东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武山县副县长",
     "current_org": "武山县人民政府",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # 麦国泉 — 副县长
    {"id": 15, "name": "麦国泉", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "武山县副县长",
     "current_org": "武山县人民政府",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # 王根红 — 副县长
    {"id": 16, "name": "王根红", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武山县副县长",
     "current_org": "武山县人民政府",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # 王岩 — 副县长
    {"id": 17, "name": "王岩", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "武山县副县长",
     "current_org": "武山县人民政府",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # 刘耀青 — 副县长
    {"id": 18, "name": "刘耀青", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "武山县副县长",
     "current_org": "武山县人民政府",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # 高峰 — 副县长
    {"id": 19, "name": "高峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "武山县副县长",
     "current_org": "武山县人民政府",
     "source": "https://www.wushan.gov.cn/ldzc1/"},

    # ═══════════════════════════════════════════════════════════
    # PREDECESSORS
    # ═══════════════════════════════════════════════════════════

    # 王新强 — 前任武山县委书记 (~2021.07-2025.09)
    {"id": 20, "name": "王新强", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-09", "birthplace": "甘肃天水",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原武山县委书记",
     "current_org": "原中共武山县委员会",
     "source": "百度百科; 甘肃党建2021-11-27; 澎湃新闻2021-07-20任前公示"},

    # 王志成 — 前任武山县县长 (~2023.09-2024.12)
    {"id": 21, "name": "王志成", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-06", "birthplace": "甘肃华池",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市秦州区委副书记、区长（原武山县长）",
     "current_org": "天水市秦州区人民政府",
     "source": "百度百科; 武山新闻2024-12"},
]

organizations = [
    {"id": 1, "name": "中共武山县委员会", "type": "党委", "level": "县处级",
     "parent": "中共天水市委员会", "location": "甘肃省天水市武山县"},
    {"id": 2, "name": "武山县人民政府", "type": "政府", "level": "县处级",
     "parent": "天水市人民政府", "location": "甘肃省天水市武山县"},
    {"id": 3, "name": "武山县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "天水市人大常委会", "location": "甘肃省天水市武山县"},
    {"id": 4, "name": "中国人民政治协商会议武山县委员会", "type": "政协", "level": "县处级",
     "parent": "天水市政协", "location": "甘肃省天水市武山县"},
    {"id": 5, "name": "武山县城关镇", "type": "乡镇/街道", "level": "乡科级",
     "parent": "武山县人民政府", "location": "甘肃省天水市武山县城关镇"},
    {"id": 6, "name": "中共天水市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共甘肃省委员会", "location": "甘肃省天水市"},
    {"id": 7, "name": "天水市人民政府", "type": "政府", "level": "地厅级",
     "parent": "甘肃省人民政府", "location": "甘肃省天水市"},
    {"id": 8, "name": "甘谷县人民政府", "type": "政府", "level": "县处级",
     "parent": "天水市人民政府", "location": "甘肃省天水市甘谷县"},
    {"id": 9, "name": "秦安县人民政府", "type": "政府", "level": "县处级",
     "parent": "天水市人民政府", "location": "甘肃省天水市秦安县"},
    {"id": 10, "name": "天水市秦州区人民政府", "type": "政府", "level": "县处级",
     "parent": "天水市人民政府", "location": "甘肃省天水市秦州区"},
    {"id": 11, "name": "共青团天水市委员会", "type": "群团", "level": "县处级",
     "parent": "中共天水市委员会", "location": "甘肃省天水市"},
    {"id": 12, "name": "甘肃农业大学", "type": "事业单位", "level": "厅局级",
     "parent": "甘肃省人民政府", "location": "甘肃省兰州市"},
]

positions = [
    # ── 王龙强 (id=1) ──
    {"person_id": 1, "org_id": 1, "title": "武山县委书记", "start": "2025-09", "end": "present", "rank": "副厅级",
     "note": "2025年9月任武山县委书记，此前任秦安县委副书记、县长"},
    {"person_id": 1, "org_id": 9, "title": "秦安县委副书记、县长", "start": "2021-07", "end": "2025-09", "rank": "正处级",
     "note": "2021年7月任秦安县委副书记、代县长，后当选县长"},
    {"person_id": 1, "org_id": 9, "title": "秦安县委副书记（正县级）", "start": "~2020", "end": "2021-07", "rank": "正处级",
     "note": ""},
    {"person_id": 1, "org_id": 11, "title": "共青团天水市委书记、党组书记", "start": "~2015", "end": "~2020", "rank": "正处级",
     "note": ""},
    {"person_id": 1, "org_id": 8, "title": "甘谷县副县长", "start": "~2012", "end": "~2015", "rank": "副处级",
     "note": "从天水市调任至甘谷县"},
    {"person_id": 1, "org_id": 12, "title": "甘肃农业大学科技处科技服务与协作科科长", "start": "~2005", "end": "2012", "rank": "正科级",
     "note": "2005年甘肃农业大学硕士毕业后留校任教，后任科技处科长"},

    # ── 赵百祥 (id=2) ──
    {"person_id": 2, "org_id": 2, "title": "武山县委副书记、县长", "start": "2025-01", "end": "present", "rank": "正处级",
     "note": "2025年1月9日当选武山县县长"},
    {"person_id": 2, "org_id": 2, "title": "武山县副县长（常务）", "start": "~2022", "end": "2025-01", "rank": "副处级",
     "note": "任县委常委、常务副县长"},
    {"person_id": 2, "org_id": 1, "title": "武山县委常委", "start": "~2021", "end": "2025-01", "rank": "副处级",
     "note": ""},

    # ── 李海巴 (id=3) ──
    {"person_id": 3, "org_id": 1, "title": "武山县委副书记（专职）", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 孙德银 (id=4) ──
    {"person_id": 4, "org_id": 3, "title": "武山县人大常委会主任", "start": "", "end": "present", "rank": "正处级",
     "note": ""},

    # ── 秦福才 (id=5) ──
    {"person_id": 5, "org_id": 4, "title": "武山县政协主席", "start": "", "end": "present", "rank": "正处级",
     "note": ""},

    # ── 胡小云 (id=6) ──
    {"person_id": 6, "org_id": 1, "title": "武山县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 刘忠锋 (id=7) ──
    {"person_id": 7, "org_id": 1, "title": "武山县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 7, "org_id": 2, "title": "武山县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 赵强 (id=8) ──
    {"person_id": 8, "org_id": 1, "title": "武山县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 8, "org_id": 2, "title": "武山县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 王宏 (id=9) ──
    {"person_id": 9, "org_id": 1, "title": "武山县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 王想成 (id=10) ──
    {"person_id": 10, "org_id": 1, "title": "武山县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 10, "org_id": 5, "title": "武山县城关镇党委书记", "start": "", "end": "present", "rank": "正科级",
     "note": ""},

    # ── 张淑香 (id=11) ──
    {"person_id": 11, "org_id": 1, "title": "武山县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 11, "org_id": 2, "title": "武山县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 李玉兰 (id=12) ──
    {"person_id": 12, "org_id": 1, "title": "武山县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 郗智聪 (id=13) ──
    {"person_id": 13, "org_id": 1, "title": "武山县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 谢怀东 (id=14) ──
    {"person_id": 14, "org_id": 2, "title": "武山县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 麦国泉 (id=15) ──
    {"person_id": 15, "org_id": 2, "title": "武山县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 王根红 (id=16) ──
    {"person_id": 16, "org_id": 2, "title": "武山县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 王岩 (id=17) ──
    {"person_id": 17, "org_id": 2, "title": "武山县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 刘耀青 (id=18) ──
    {"person_id": 18, "org_id": 2, "title": "武山县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 高峰 (id=19) ──
    {"person_id": 19, "org_id": 2, "title": "武山县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 王新强 (id=20) ──
    {"person_id": 20, "org_id": 1, "title": "武山县委书记", "start": "2021-07", "end": "2025-09", "rank": "副厅级",
     "note": "前任县委书记，2025年9月由王龙强接任"},
    {"person_id": 20, "org_id": 6, "title": "天水市畜牧兽医局党组书记、局长", "start": "", "end": "2021-07", "rank": "正处级",
     "note": "任武山县委书记前职务"},

    # ── 王志成 (id=21) ──
    {"person_id": 21, "org_id": 2, "title": "武山县委副书记、县长", "start": "2023-09", "end": "2024-12", "rank": "正处级",
     "note": "前任县长，2024年12月调任秦州区"},
    {"person_id": 21, "org_id": 10, "title": "天水市秦州区委副书记、区长", "start": "2024-12", "end": "present", "rank": "正处级",
     "note": "现任秦州区区长"},
]

relationships = [
    # ── Current top leaders ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "王龙强作为县委书记, 赵百祥作为县长, 是党政一把手搭档关系",
     "overlap_org": "中共武山县委员会/武山县人民政府",
     "overlap_period": "2025-09~present", "confidence": "confirmed"},

    # ── 书记+副书记 ──
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "strength": "strong",
     "context": "王龙强作为县委书记, 李海巴作为专职副书记, 是县委班子搭档",
     "overlap_org": "中共武山县委员会",
     "overlap_period": "2025-09~present", "confidence": "confirmed"},

    # ── Succession chain: 县委书记 ──
    {"person_a": 1, "person_b": 20, "type": "predecessor_successor", "strength": "strong",
     "context": "王龙强接替王新强任武山县委书记",
     "overlap_org": "中共武山县委员会",
     "overlap_period": "2025-09", "confidence": "confirmed"},

    # ── Succession chain: 县长 ──
    {"person_a": 2, "person_b": 21, "type": "predecessor_successor", "strength": "strong",
     "context": "赵百祥接替王志成任武山县县长（赵原为常务副县长升任）",
     "overlap_org": "武山县人民政府",
     "overlap_period": "2025-01", "confidence": "confirmed"},

    # ── 前任搭档关系 ──
    {"person_a": 20, "person_b": 21, "type": "superior_subordinate", "strength": "strong",
     "context": "王新强与王志成为前任党政一把手搭档（2023-2024）",
     "overlap_org": "中共武山县委员会/武山县人民政府",
     "overlap_period": "2023-09~2024-12", "confidence": "confirmed"},

    # ── 王龙强+王志成 (前任县长与现任书记曾在秦安共事？) ──
    {"person_a": 1, "person_b": 21, "type": "same_system", "strength": "medium",
     "context": "王龙强曾任秦安县长，王志成曾任武山县长后调任秦州区长，同在县级政府主官序列",
     "overlap_org": "天水辖区县政府",
     "overlap_period": "", "confidence": "plausible"},

    # ── 赵百祥从副县长升任县长（与前任县长工作交集） ──
    {"person_a": 2, "person_b": 21, "type": "superior_subordinate", "strength": "strong",
     "context": "赵百祥在王志成任县长期间任常务副县长，是直接下属",
     "overlap_org": "武山县人民政府",
     "overlap_period": "~2023-09~2024-12", "confidence": "confirmed"},

    # ── Top leaders + 四大班子 ──
    {"person_a": 1, "person_b": 4, "type": "overlap", "strength": "medium",
     "context": "王龙强与孙德银在武山县党政班子共事",
     "overlap_org": "中共武山县委员会/武山县人大常委会",
     "overlap_period": "2025-09~present", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 5, "type": "overlap", "strength": "medium",
     "context": "王龙强与秦福才在武山县党政班子共事",
     "overlap_org": "中共武山县委员会/武山县政协",
     "overlap_period": "2025-09~present", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 4, "type": "overlap", "strength": "medium",
     "context": "赵百祥与孙德银在武山县党政班子共事",
     "overlap_org": "武山县人民政府/武山县人大常委会",
     "overlap_period": "2025-01~present", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 5, "type": "overlap", "strength": "medium",
     "context": "赵百祥与秦福才在武山县党政班子共事",
     "overlap_org": "武山县人民政府/武山县政协",
     "overlap_period": "2025-01~present", "confidence": "confirmed"},

    # ── 王龙强与赵百祥的前任工作交接 ──
    {"person_a": 1, "person_b": 20, "type": "predecessor_successor", "strength": "strong",
     "context": "王龙强接替王新强任武山县委书记",
     "overlap_org": "中共武山县委员会",
     "overlap_period": "2025-09", "confidence": "confirmed"},

    # ── 县委班子内部关系 ──
    {"person_a": 1, "person_b": 6, "type": "overlap", "strength": "medium",
     "context": "县委常委班子共事",
     "overlap_org": "中共武山县委员会",
     "overlap_period": "2025-09~present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "strength": "medium",
     "context": "县委常委班子共事",
     "overlap_org": "中共武山县委员会",
     "overlap_period": "2025-09~present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "strength": "medium",
     "context": "县委常委班子共事",
     "overlap_org": "中共武山县委员会",
     "overlap_period": "2025-09~present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "strength": "medium",
     "context": "县委常委班子共事",
     "overlap_org": "中共武山县委员会",
     "overlap_period": "2025-09~present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "strength": "medium",
     "context": "县委常委班子共事",
     "overlap_org": "中共武山县委员会",
     "overlap_period": "2025-09~present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "strength": "medium",
     "context": "县委常委班子共事",
     "overlap_org": "中共武山县委员会",
     "overlap_period": "2025-09~present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "strength": "medium",
     "context": "县委常委班子共事",
     "overlap_org": "中共武山县委员会",
     "overlap_period": "2025-09~present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "strength": "medium",
     "context": "县委常委班子共事",
     "overlap_org": "中共武山县委员会",
     "overlap_period": "2025-09~present", "confidence": "confirmed"},

    # ── 县长与政府班子成员 ──
    {"person_a": 2, "person_b": 7, "type": "overlap", "strength": "medium",
     "context": "县政府班子共事",
     "overlap_org": "武山县人民政府",
     "overlap_period": "2025-01~present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "strength": "medium",
     "context": "县政府班子共事",
     "overlap_org": "武山县人民政府",
     "overlap_period": "2025-01~present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "strength": "medium",
     "context": "县政府班子共事",
     "overlap_org": "武山县人民政府",
     "overlap_period": "2025-01~present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "strength": "medium",
     "context": "县政府班子共事",
     "overlap_org": "武山县人民政府",
     "overlap_period": "2025-01~present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "strength": "medium",
     "context": "县政府班子共事",
     "overlap_org": "武山县人民政府",
     "overlap_period": "2025-01~present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "strength": "medium",
     "context": "县政府班子共事",
     "overlap_org": "武山县人民政府",
     "overlap_period": "2025-01~present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 17, "type": "overlap", "strength": "medium",
     "context": "县政府班子共事",
     "overlap_org": "武山县人民政府",
     "overlap_period": "2025-01~present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 18, "type": "overlap", "strength": "medium",
     "context": "县政府班子共事",
     "overlap_org": "武山县人民政府",
     "overlap_period": "2025-01~present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 19, "type": "overlap", "strength": "medium",
     "context": "县政府班子共事",
     "overlap_org": "武山县人民政府",
     "overlap_period": "2025-01~present", "confidence": "confirmed"},
]


# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p["current_post"]
    if "县委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "县长" in role and "副书记" in role:
        return "50,100,255"
    elif "县长" in role:
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    elif "原" in role:
        return "160,160,160"
    else:
        return "100,100,100"


def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")


def is_top_leader(p):
    role = p["current_post"]
    return "县委书记" in role or ("县长" in role and "副书记" in role)


def person_size(p):
    return "20.0" if is_top_leader(p) else ("14.0" if "原" not in p["current_post"] else "10.0")


# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
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
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>武山县领导班子工作关系网络 - 甘肃省天水市武山县</description>')
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
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
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

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
