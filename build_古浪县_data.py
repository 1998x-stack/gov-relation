#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 古浪县 (Gulang County), Wuwei, Gansu.

古浪县 — 甘肃省武威市下辖县，位于河西走廊东端，是全国荒漠化重点监测县。
Covers current Party Secretary (杨琦玮), County Mayor (马亚同), their predecessors,
key leadership (县委常委13人+县政府班子), and relationship network.

Data sourced from official 古浪县人民政府 website (www.gulang.gov.cn) as of July 2026.
县委领导: https://www.gulang.gov.cn/col/col11580/index.html
县政府领导: https://www.gulang.gov.cn/col/col11582/index.html
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/gansu_古浪县")
os.makedirs(TMP, exist_ok=True)

DB_PATH = os.path.join(TMP, "古浪县_network.db")
GEXF_PATH = os.path.join(TMP, "古浪县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── A. Current Top Two Leaders ──

    # 杨琦玮 — 古浪县委书记 (female, as of 2026.07)
    {"id": 1, "name": "杨琦玮", "gender": "女", "ethnicity": "汉族",
     "birth": "1983-03", "birthplace": "",
     "education": "研究生学历，经济学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县委书记",
     "current_org": "中共古浪县委员会",
     "source": "https://www.gulang.gov.cn/col/col18003/index.html"},

    # 马亚同 — 古浪县委副书记、县长 (as of 2026.07)
    {"id": 2, "name": "马亚同", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-06", "birthplace": "",
     "education": "大学学历，经济学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县委副书记、县人民政府县长",
     "current_org": "古浪县人民政府",
     "source": "https://www.gulang.gov.cn/col/col30613/index.html"},

    # ── B. 县委领导班子（县委常委共13人，含书记、县长）──
    # Source: 县委领导 page https://www.gulang.gov.cn/col/col11580/index.html

    # 徐立峰 — 县委副书记 (third in command)
    {"id": 3, "name": "徐立峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-10", "birthplace": "",
     "education": "大学学历，文学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县委副书记",
     "current_org": "中共古浪县委员会",
     "source": "https://www.gulang.gov.cn/col/col11580/index.html"},

    # 姚得军 — 县委常委、政法委书记
    {"id": 4, "name": "姚得军", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-07", "birthplace": "",
     "education": "省委党校大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县委常委、政法委书记",
     "current_org": "中共古浪县委员会",
     "source": "https://www.gulang.gov.cn/col/col11580/index.html"},

    # 王吉庆 — 县委常委、组织部部长
    {"id": 5, "name": "王吉庆", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-04", "birthplace": "",
     "education": "省委党校研究生学历，工学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县委常委、组织部部长",
     "current_org": "中共古浪县委员会",
     "source": "https://www.gulang.gov.cn/col/col11580/index.html"},

    # 秦宗山 — 县委常委、县纪委书记、县监委主任
    {"id": 6, "name": "秦宗山", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-09", "birthplace": "",
     "education": "大学学历，文学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县委常委、县纪委书记、县监委主任",
     "current_org": "中共古浪县纪律检查委员会",
     "source": "https://www.gulang.gov.cn/col/col11580/index.html"},

    # 赵生煌 — 县委常委、统战部部长
    {"id": 7, "name": "赵生煌", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-08", "birthplace": "",
     "education": "省委党校研究生学历，文学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县委常委、统战部部长",
     "current_org": "中共古浪县委员会",
     "source": "https://www.gulang.gov.cn/col/col11580/index.html"},

    # 卢继发 — 县委常委、常务副县长
    {"id": 8, "name": "卢继发", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-01", "birthplace": "",
     "education": "大学学历，教育学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县委常委、常务副县长",
     "current_org": "古浪县人民政府",
     "source": "https://www.gulang.gov.cn/col/col11580/index.html"},

    # 刘大伟 — 县委常委、副县长（挂职）
    {"id": 9, "name": "刘大伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-04", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县委常委、副县长（挂职）",
     "current_org": "古浪县人民政府",
     "source": "https://www.gulang.gov.cn/col/col11580/index.html"},

    # 李涛 — 县委常委、副县长
    {"id": 10, "name": "李涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-11", "birthplace": "",
     "education": "在职大学学历，农业推广硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县委常委、副县长",
     "current_org": "古浪县人民政府",
     "source": "https://www.gulang.gov.cn/col/col11580/index.html"},

    # 王衡 — 县委常委、副县长（挂职）
    {"id": 11, "name": "王衡", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县委常委、副县长（挂职）",
     "current_org": "古浪县人民政府",
     "source": "https://www.gulang.gov.cn/col/col11580/index.html"},

    # 董钰山 — 县委常委、宣传部部长
    {"id": 12, "name": "董钰山", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-02", "birthplace": "",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县委常委、宣传部部长",
     "current_org": "中共古浪县委员会",
     "source": "https://www.gulang.gov.cn/col/col11580/index.html"},

    # 陈文超 — 县委常委、县人武部上校部长
    {"id": 13, "name": "陈文超", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-08", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县委常委、县人武部上校部长",
     "current_org": "古浪县人民武装部",
     "source": "https://www.gulang.gov.cn/col/col11580/index.html"},

    # ── C. 县政府班子成员（副县长，非县委常委）──
    # Source: 县政府领导 page https://www.gulang.gov.cn/col/col11582/index.html

    # 周涛元 — 副县长、县公安局局长
    {"id": 14, "name": "周涛元", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-04", "birthplace": "",
     "education": "在职大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县人民政府副县长、县公安局局长",
     "current_org": "古浪县人民政府",
     "source": "https://www.gulang.gov.cn/col/col11582/index.html"},

    # 臧伯平 — 副县长
    {"id": 15, "name": "臧伯平", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-10", "birthplace": "",
     "education": "大学学历，教育学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县人民政府副县长",
     "current_org": "古浪县人民政府",
     "source": "https://www.gulang.gov.cn/col/col11582/index.html"},

    # 宋学军 — 副县长
    {"id": 16, "name": "宋学军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县人民政府副县长",
     "current_org": "古浪县人民政府",
     "source": "https://www.gulang.gov.cn/col/col11582/index.html"},

    # 赵庆朋 — 副县长（挂职）
    {"id": 17, "name": "赵庆朋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县人民政府副县长（挂职）",
     "current_org": "古浪县人民政府",
     "source": "https://www.gulang.gov.cn/col/col11582/index.html"},

    # 贾喜奎 — 副县长、县河长办主任（兼）
    {"id": 18, "name": "贾喜奎", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县人民政府副县长、县河长办主任（兼）",
     "current_org": "古浪县人民政府",
     "source": "https://www.gulang.gov.cn/col/col11582/index.html"},

    # ── D. 县人大常委会领导 ──

    # 张浩晓 — 县人大常委会主任
    {"id": 19, "name": "张浩晓", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-09", "birthplace": "",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县人大常委会主任",
     "current_org": "古浪县人大常委会",
     "source": "https://www.gulang.gov.cn/col/col11580/index.html"},

    # ── E. 县政协领导 ──

    # 单俊阳 — 县政协主席
    {"id": 20, "name": "单俊阳", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-05", "birthplace": "",
     "education": "省委党校大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古浪县政协主席",
     "current_org": "政协古浪县委员会",
     "source": "https://www.gulang.gov.cn/col/col11580/index.html"},

    # ── F. Predecessors ──

    # 李万岳 — 前任古浪县委书记 (Wikipedia info, pre-2025)
    {"id": 21, "name": "李万岳", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前任古浪县委书记（已离任）",
     "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/%E5%8F%A4%E6%B5%AA%E5%8E%BF"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共古浪县委员会", "type": "党委", "level": "县处级",
     "parent": "中共武威市委员会", "location": "甘肃省武威市古浪县"},
    {"id": 2, "name": "古浪县人民政府", "type": "政府", "level": "县处级",
     "parent": "武威市人民政府", "location": "甘肃省武威市古浪县"},
    {"id": 3, "name": "中共古浪县纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共古浪县委", "location": "甘肃省武威市古浪县"},
    {"id": 4, "name": "古浪县监察委员会", "type": "政府", "level": "县处级",
     "parent": "古浪县人民政府", "location": "甘肃省武威市古浪县"},
    {"id": 5, "name": "古浪县人大常委会", "type": "人大", "level": "县处级",
     "parent": "武威市人大常委会", "location": "甘肃省武威市古浪县"},
    {"id": 6, "name": "政协古浪县委员会", "type": "政协", "level": "县处级",
     "parent": "政协武威市委员会", "location": "甘肃省武威市古浪县"},
    {"id": 7, "name": "古浪县人民武装部", "type": "其他", "level": "县处级",
     "parent": "武威军分区", "location": "甘肃省武威市古浪县"},
    {"id": 8, "name": "古浪县公安局", "type": "政府", "level": "乡科级",
     "parent": "古浪县人民政府", "location": "甘肃省武威市古浪县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ──县委班子──
    {"person_id": 1, "org_id": 1, "title": "古浪县委书记",
     "start": "", "end": "present", "rank": "正县级", "note": "1983年3月生，研究生/经济学博士"},
    {"person_id": 2, "org_id": 1, "title": "古浪县委副书记",
     "start": "", "end": "present", "rank": "副县级", "note": "1985年6月生，大学/经济学学士"},
    {"person_id": 2, "org_id": 2, "title": "古浪县人民政府县长",
     "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "古浪县委副书记",
     "start": "", "end": "present", "rank": "副县级", "note": "1980年10月生，大学/文学学士"},
    {"person_id": 4, "org_id": 1, "title": "古浪县委常委、政法委书记",
     "start": "", "end": "present", "rank": "副县级", "note": "1981年7月生，省委党校大学"},
    {"person_id": 5, "org_id": 1, "title": "古浪县委常委、组织部部长",
     "start": "", "end": "present", "rank": "副县级", "note": "1981年4月生，省委党校研究生/工学学士"},
    {"person_id": 6, "org_id": 3, "title": "古浪县委常委、县纪委书记、县监委主任",
     "start": "", "end": "present", "rank": "副县级", "note": "1985年9月生，大学/文学学士"},
    {"person_id": 6, "org_id": 4, "title": "古浪县监察委员会主任",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "古浪县委常委、统战部部长",
     "start": "", "end": "present", "rank": "副县级", "note": "1982年8月生，省委党校研究生/文学学士"},
    {"person_id": 8, "org_id": 2, "title": "古浪县委常委、常务副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "1982年1月生，大学/教育学学士"},
    {"person_id": 9, "org_id": 2, "title": "古浪县委常委、副县长（挂职）",
     "start": "", "end": "present", "rank": "副县级", "note": "1980年4月生，大学"},
    {"person_id": 10, "org_id": 2, "title": "古浪县委常委、副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "1983年11月生，在职大学/农业推广硕士"},
    {"person_id": 11, "org_id": 2, "title": "古浪县委常委、副县长（挂职）",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "古浪县委常委、宣传部部长",
     "start": "", "end": "present", "rank": "副县级", "note": "1986年2月生，省委党校研究生"},
    {"person_id": 13, "org_id": 7, "title": "古浪县委常委、县人武部上校部长",
     "start": "", "end": "present", "rank": "副县级", "note": "1981年8月生，大学"},

    # ──县政府班子（非县委常委的副县长）──
    {"person_id": 14, "org_id": 2, "title": "古浪县人民政府副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "兼县公安局局长，1984年4月生，在职大学"},
    {"person_id": 14, "org_id": 8, "title": "古浪县公安局局长",
     "start": "", "end": "present", "rank": "乡科级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "古浪县人民政府副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "1986年10月生，大学/教育学学士"},
    {"person_id": 16, "org_id": 2, "title": "古浪县人民政府副县长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "古浪县人民政府副县长（挂职）",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "古浪县人民政府副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "兼县河长办主任"},

    # ──人大、政协──
    {"person_id": 19, "org_id": 5, "title": "古浪县人大常委会主任",
     "start": "", "end": "present", "rank": "正县级", "note": "1968年9月生，省委党校研究生"},
    {"person_id": 20, "org_id": 6, "title": "古浪县政协主席",
     "start": "", "end": "present", "rank": "正县级", "note": "1975年5月生，省委党校大学"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Core leadership pair
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "杨琦玮（县委书记）与马亚同（县长）为古浪县党政正职搭档",
     "overlap_org": "中共古浪县委/古浪县政府", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},

    # 县委主要领导与副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与专职副书记",
     "overlap_org": "中共古浪县委", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},

    # 县委书记与各县委常委
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与政法委书记", "overlap_org": "中共古浪县委", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委书记与组织部部长", "overlap_org": "中共古浪县委", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与纪委书记", "overlap_org": "中共古浪县委", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "县委书记与统战部部长", "overlap_org": "中共古浪县委", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "县委书记与常务副县长", "overlap_org": "中共古浪县委", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "县委书记与（挂职）副县长", "overlap_org": "中共古浪县委", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "县委书记与副县长", "overlap_org": "中共古浪县委", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "县委书记与（挂职）副县长", "overlap_org": "中共古浪县委", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "县委书记与宣传部部长", "overlap_org": "中共古浪县委", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate",
     "context": "县委书记与人武部上校部长", "overlap_org": "中共古浪县委", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 19, "type": "superior_subordinate",
     "context": "县委书记与县人大常委会主任（党委领导人大）", "overlap_org": "古浪县", "overlap_period": "2026-至今",
     "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 20, "type": "superior_subordinate",
     "context": "县委书记与县政协主席（党委领导政协）", "overlap_org": "古浪县", "overlap_period": "2026-至今",
     "strength": "medium", "confidence": "confirmed"},

    # 县长与政府班子成员
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "县长与常务副县长（政府工作搭档）", "overlap_org": "古浪县人民政府", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "县长与（挂职）副县长", "overlap_org": "古浪县人民政府", "overlap_period": "2026-至今",
     "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "古浪县人民政府", "overlap_period": "2026-至今",
     "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "县长与公安局长", "overlap_org": "古浪县人民政府", "overlap_period": "2026-至今",
     "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "古浪县人民政府", "overlap_period": "2026-至今",
     "strength": "medium", "confidence": "confirmed"},
]


# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def build_database():
    """Create SQLite database with all tables and data."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
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
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert data
    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace,
                education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["education"], p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
              pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org,
                overlap_period, strength, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"  ✓ Database created: {DB_PATH}")


def build_gexf():
    """Create GEXF graph file using string formatting."""
    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>古浪县领导班子工作关系网络 — 甘肃省武威市古浪县</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org_type" type="string"/>')
    lines.append('      <attribute id="2" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        # Color by role
        if p["id"] == 1:
            c = "255,50,50"   # Red — party secretary
        elif p["id"] == 2:
            c = "50,100,255"  # Blue — county mayor
        elif "纪委" in (p["current_post"] or "") or "监委" in (p["current_post"] or ""):
            c = "255,165,0"   # Orange — discipline
        elif "人大" in (p["current_post"] or ""):
            c = "200,255,255" # Cyan — congress
        elif "政协" in (p["current_post"] or ""):
            c = "255,240,200" # Cream — consultative
        elif "人武部" in (p["current_post"] or ""):
            c = "180,180,100" # Olive — military
        elif "政法委" in (p["current_post"] or ""):
            c = "180,120,200" # Purple — political/legal
        else:
            c = "100,100,100" # Grey — other

        sz = "20.0" if p["id"] in (1, 2) else ("16.0" if p["id"] in (19, 20) else "12.0")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,150",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "default": "200,200,200",
    }
    for o in organizations:
        c = org_colors.get(o["type"], org_colors["default"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Person -> organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["strength"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["confidence"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ GEXF graph created: {GEXF_PATH}")


def print_summary():
    """Print summary statistics."""
    print(f"\n=== 古浪县 Network Data Summary ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Top leaders: 杨琦玮（县委书记）、马亚同（县长）")
    print(f"  Data as of: July 2026")
    print(f"  Primary source: gulang.gov.cn")
    print()


if __name__ == "__main__":
    print("Building 古浪县 network data...")
    build_database()
    build_gexf()
    print_summary()
