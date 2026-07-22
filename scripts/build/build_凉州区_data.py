#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 凉州区 (Liangzhou District), Wuwei, Gansu.

凉州区 — 甘肃省武威市市辖区, 河西走廊东大门, 武威市政治经济文化中心.
Covers current Party Secretary (王强), District Mayor (邓涛), their predecessors,
key leadership, and relationship network.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/gansu_凉州区")
os.makedirs(TMP, exist_ok=True)

DB_PATH = os.path.join(TMP, "凉州区_network.db")
GEXF_PATH = os.path.join(TMP, "凉州区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── A. Current Top Leaders ──

    # 王强 — 武威市委常委、凉州区委书记, also 甘肃武威工业园区党工委书记兼管委会主任
    {"id": 1, "name": "王强", "gender": "男", "ethnicity": "藏族",
     "birth": "1973-08", "birthplace": "",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武威市委常委、凉州区委书记、甘肃武威工业园区党工委书记兼管委会主任",
     "current_org": "中共武威市凉州区委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col3133/index.html"},

    # 邓涛 — 凉州区委副书记、区政府区长
    {"id": 2, "name": "邓涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-03", "birthplace": "",
     "education": "大学学历，公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区委副书记、区政府党组书记、区长",
     "current_org": "凉州区人民政府",
     "source": "https://www.gsliangzhou.gov.cn/col/col31784/index.html"},

    # ── B. District Party Committee ──

    # 刘兴武 — 区委副书记
    {"id": 3, "name": "刘兴武", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-09", "birthplace": "",
     "education": "大学学历，法学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区委副书记",
     "current_org": "中共武威市凉州区委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col29423/index.html"},

    # 许娜 — 区委常委、组织部部长
    {"id": 4, "name": "许娜", "gender": "女", "ethnicity": "汉族",
     "birth": "1983-12", "birthplace": "",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区委常委、组织部部长",
     "current_org": "中共武威市凉州区委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col31077/index.html"},

    # 何立宏 — 区委常委
    {"id": 5, "name": "何立宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区委常委",
     "current_org": "中共武威市凉州区委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 刘永龙 — 区委常委、宣传部部长
    {"id": 6, "name": "刘永龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-08", "birthplace": "",
     "education": "在职大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区委常委、宣传部部长、区新时代文明实践中心办公室主任（兼）",
     "current_org": "中共武威市凉州区委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col30915/index.html"},

    # 吴万攀 — 区委常委
    {"id": 7, "name": "吴万攀", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区委常委",
     "current_org": "中共武威市凉州区委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 陈华 — 区委常委、区政府副区长
    {"id": 8, "name": "陈华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区委常委、区政府副区长",
     "current_org": "中共武威市凉州区委员会/凉州区人民政府",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 徐振雄 — 区委常委
    {"id": 9, "name": "徐振雄", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区委常委",
     "current_org": "中共武威市凉州区委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 郭干干 — 区委常委
    {"id": 10, "name": "郭干干", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区委常委",
     "current_org": "中共武威市凉州区委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # ── C. District Government Deputy Mayors ──

    # 王多龙 — 副区长、市公安局凉州分局局长
    {"id": 11, "name": "王多龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-08", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区政府党组成员、副区长、武威市公安局副局长、市公安局凉州分局党委书记、局长、督察长（兼）",
     "current_org": "凉州区人民政府",
     "source": "https://www.gsliangzhou.gov.cn/col/col3168/index.html"},

    # 张永宏 — 副区长
    {"id": 12, "name": "张永宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区政府副区长",
     "current_org": "凉州区人民政府",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 赵玉生 — 副区长
    {"id": 13, "name": "赵玉生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区政府副区长",
     "current_org": "凉州区人民政府",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 董西泉 — 副区长
    {"id": 14, "name": "董西泉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区政府副区长",
     "current_org": "凉州区人民政府",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 薛扬 — 副区长
    {"id": 15, "name": "薛扬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区政府副区长",
     "current_org": "凉州区人民政府",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 徐祥宗 — 副区长
    {"id": 16, "name": "徐祥宗", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区政府副区长",
     "current_org": "凉州区人民政府",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # ── D. District People's Congress ──

    # 俞天平 — 区人大常委会主任
    {"id": 17, "name": "俞天平", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-06", "birthplace": "",
     "education": "党校大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区人大常委会党组书记、主任",
     "current_org": "凉州区人民代表大会常务委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col3074/index.html"},

    # 张多文 — 区人大常委会副主任
    {"id": 18, "name": "张多文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区人大常委会副主任",
     "current_org": "凉州区人民代表大会常务委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 张宝生 — 区人大常委会副主任
    {"id": 19, "name": "张宝生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区人大常委会副主任",
     "current_org": "凉州区人民代表大会常务委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 张万栋 — 区人大常委会副主任
    {"id": 20, "name": "张万栋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区人大常委会副主任",
     "current_org": "凉州区人民代表大会常务委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 刘春年 — 区人大常委会副主任
    {"id": 21, "name": "刘春年", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区人大常委会副主任",
     "current_org": "凉州区人民代表大会常务委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 吴天亮 — 区人大常委会副主任
    {"id": 22, "name": "吴天亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区人大常委会副主任",
     "current_org": "凉州区人民代表大会常务委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 刘成 — 区人大常委会副主任
    {"id": 23, "name": "刘成", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凉州区人大常委会副主任",
     "current_org": "凉州区人民代表大会常务委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # ── E. District CPPCC ──

    # 徐兴平 — 区政协主席
    {"id": 24, "name": "徐兴平", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-11", "birthplace": "",
     "education": "党校研究生学历，工学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政协凉州区委员会党组书记、主席",
     "current_org": "政协凉州区委员会",
     "source": "https://www.gsliangzhou.gov.cn/col/col2747/index.html"},

    # ── F. Predecessors (known from public records) ──

    # 李世英 — 前任区委书记（Wikipedia lists him, but appears to be outdated or possibly erroneous）
    # Listed with unverified confidence as the official source shows 王强 as current
    # Keeping this record for reference
    {"id": 25, "name": "李世英", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原凉州区委书记（信息待确认）",
     "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/%E5%87%89%E5%B7%9E%E5%8C%BA"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共武威市凉州区委员会", "type": "党委", "level": "县处级",
     "parent": "中共武威市委员会", "location": "甘肃省武威市凉州区"},
    {"id": 2, "name": "凉州区人民政府", "type": "政府", "level": "县处级",
     "parent": "武威市人民政府", "location": "甘肃省武威市凉州区"},
    {"id": 3, "name": "凉州区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "武威市人大常委会", "location": "甘肃省武威市凉州区"},
    {"id": 4, "name": "政协凉州区委员会", "type": "政协", "level": "县处级",
     "parent": "政协武威市委员会", "location": "甘肃省武威市凉州区"},
    {"id": 5, "name": "中共武威市凉州区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共武威市凉州区委员会", "location": "甘肃省武威市凉州区"},
    {"id": 6, "name": "武威市公安局凉州分局", "type": "政府", "level": "乡科级",
     "parent": "武威市公安局", "location": "甘肃省武威市凉州区"},
    {"id": 7, "name": "甘肃武威工业园区党工委", "type": "党委", "level": "县处级",
     "parent": "中共武威市委", "location": "甘肃省武威市凉州区"},
    {"id": 8, "name": "甘肃武威工业园区管委会", "type": "政府", "level": "县处级",
     "parent": "武威市人民政府", "location": "甘肃省武威市凉州区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 王强
    {"person_id": 1, "org_id": 1, "title": "武威市委常委、凉州区委书记",
     "start": "", "end": "present", "rank": "副厅级", "note": "主持区委全面工作"},
    {"person_id": 1, "org_id": 7, "title": "甘肃武威工业园区党工委书记兼管委会主任",
     "start": "", "end": "present", "rank": "", "note": ""},

    # 邓涛
    {"person_id": 2, "org_id": 2, "title": "凉州区委副书记、区政府党组书记、区长",
     "start": "", "end": "present", "rank": "县处级", "note": "主持区政府全面工作。负责审计方面工作"},

    # 刘兴武
    {"person_id": 3, "org_id": 1, "title": "凉州区委副书记",
     "start": "", "end": "present", "rank": "县处级", "note": "负责区委日常工作"},

    # 许娜
    {"person_id": 4, "org_id": 1, "title": "凉州区委常委、组织部部长",
     "start": "", "end": "present", "rank": "县处级", "note": "负责组织、干部、人才工作"},

    # 何立宏
    {"person_id": 5, "org_id": 1, "title": "凉州区委常委",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 刘永龙
    {"person_id": 6, "org_id": 1, "title": "凉州区委常委、宣传部部长",
     "start": "", "end": "present", "rank": "县处级",
     "note": "负责宣传思想、意识形态、精神文明工作"},

    # 吴万攀
    {"person_id": 7, "org_id": 1, "title": "凉州区委常委",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 陈华
    {"person_id": 8, "org_id": 1, "title": "凉州区委常委、区政府副区长",
     "start": "", "end": "present", "rank": "县处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "凉州区政府副区长",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 徐振雄
    {"person_id": 9, "org_id": 1, "title": "凉州区委常委",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 郭干干
    {"person_id": 10, "org_id": 1, "title": "凉州区委常委",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 王多龙
    {"person_id": 11, "org_id": 2, "title": "凉州区政府党组成员、副区长",
     "start": "", "end": "present", "rank": "县处级", "note": "负责公安、信访等工作"},
    {"person_id": 11, "org_id": 6, "title": "武威市公安局凉州分局党委书记、局长、督察长（兼）",
     "start": "", "end": "present", "rank": "", "note": ""},

    # 张永宏
    {"person_id": 12, "org_id": 2, "title": "凉州区政府副区长",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 赵玉生
    {"person_id": 13, "org_id": 2, "title": "凉州区政府副区长",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 董西泉
    {"person_id": 14, "org_id": 2, "title": "凉州区政府副区长",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 薛扬
    {"person_id": 15, "org_id": 2, "title": "凉州区政府副区长",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 徐祥宗
    {"person_id": 16, "org_id": 2, "title": "凉州区政府副区长",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 俞天平
    {"person_id": 17, "org_id": 3, "title": "凉州区人大常委会党组书记、主任",
     "start": "", "end": "present", "rank": "县处级", "note": "主持区人大常委会全面工作"},

    # 张多文
    {"person_id": 18, "org_id": 3, "title": "凉州区人大常委会副主任",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 张宝生
    {"person_id": 19, "org_id": 3, "title": "凉州区人大常委会副主任",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 张万栋
    {"person_id": 20, "org_id": 3, "title": "凉州区人大常委会副主任",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 刘春年
    {"person_id": 21, "org_id": 3, "title": "凉州区人大常委会副主任",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 吴天亮
    {"person_id": 22, "org_id": 3, "title": "凉州区人大常委会副主任",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 刘成
    {"person_id": 23, "org_id": 3, "title": "凉州区人大常委会副主任",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 徐兴平
    {"person_id": 24, "org_id": 4, "title": "政协凉州区委员会党组书记、主席",
     "start": "", "end": "present", "rank": "县处级", "note": "主持区政协全面工作"},

    # 李世英 (前区委书记, unverified)
    {"person_id": 25, "org_id": 1, "title": "凉州区委书记（前任）",
     "start": "", "end": "", "rank": "", "note": "信息来源为维基百科，待官方确认"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 王强 — 邓涛 (党政正职搭档, as of 2026)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记与区长党政正职搭档",
     "overlap_org": "中共武威市凉州区委员会/凉州区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 王强 — 刘兴武 (书记与副书记)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区委副书记",
     "overlap_org": "中共武威市凉州区委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 邓涛 — 刘兴武 (区长与副书记)
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "区政府区长与区委副书记为区委常委会班子成员",
     "overlap_org": "中共武威市凉州区委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 王强 — 各区委常委 (领导关系)
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记与区委常委、组织部部长",
     "overlap_org": "中共武威市凉州区委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与区委常委",
     "overlap_org": "中共武威市凉州区委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "区委书记与区委常委、宣传部部长",
     "overlap_org": "中共武威市凉州区委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "区委书记与区委常委",
     "overlap_org": "中共武威市凉州区委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "区委书记与区委常委、副区长",
     "overlap_org": "中共武威市凉州区委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "区委书记与区委常委",
     "overlap_org": "中共武威市凉州区委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "区委书记与区委常委",
     "overlap_org": "中共武威市凉州区委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    # 区长 — 副区长们
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "区长与副区长（公安）",
     "overlap_org": "凉州区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "凉州区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "凉州区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "凉州区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "凉州区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},

    {"person_a": 2, "person_b": 16, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "凉州区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.gsliangzhou.gov.cn/col/col2957/index.html"},
]

# =========================================================================
# SQLITE BUILD
# =========================================================================
def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons(
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
        CREATE TABLE organizations(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions(
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE relationships(
            id INTEGER PRIMARY KEY,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            source TEXT
        );
    """)

    for p in persons:
        c.execute("""INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p.get("birthplace", ""), p.get("education", ""),
                   p.get("party_join", ""), p.get("work_start", ""),
                   p.get("current_post", ""), p.get("current_org", ""),
                   p.get("source", "")))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES(?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"],
                   o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""INSERT INTO positions(person_id,org_id,title,start,"end",rank,note)
                     VALUES(?,?,?,?,?,?,?)""",
                  (pos["person_id"], pos["org_id"], pos["title"],
                   pos.get("start", ""), pos.get("end", ""),
                   pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        c.execute("""INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period,strength,confidence,source)
                     VALUES(?,?,?,?,?,?,?,?,?)""",
                  (r["person_a"], r["person_b"], r["type"], r["context"],
                   r.get("overlap_org", ""), r.get("overlap_period", ""),
                   r.get("strength", ""), r.get("confidence", ""),
                   r.get("source", "")))

    conn.commit()
    conn.close()
    print(f"SQLite DB created: {DB_PATH}")


# =========================================================================
# GEXF BUILD
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    pid = p["id"]
    # 区委书记
    if pid == 1:
        return "255,50,50"
    # 区长
    if pid == 2:
        return "50,100,255"
    # 区委副书记
    if pid == 3:
        return "50,100,255"
    # 区委常委、组织部部长
    if pid == 4:
        return "255,165,0"
    # 区委常委、宣传部部长
    if pid == 6:
        return "255,165,0"
    # 人大主任
    if pid == 17:
        return "200,200,200"
    # 政协主席
    if pid == 24:
        return "200,200,200"
    return "100,100,100"


def is_top_leader(p):
    return p["id"] in (1, 2)


def org_color(o):
    otype = o.get("type", "")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(otype, "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Research Agent</creator>')
    lines.append('    <description>凉州区（武威市）领导关系网络 - 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="job" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        if pid == 25:
            sz = "8.0"
        elif is_top_leader(p):
            sz = "20.0"
        else:
            sz = "12.0"
        c = person_color(p)
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        c = org_color(o)
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person relationships
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")
