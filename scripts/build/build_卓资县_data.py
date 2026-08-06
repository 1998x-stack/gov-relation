#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 卓资县 leadership network.

卓资县 (Zhuozi County) 是内蒙古自治区乌兰察布市辖县，位于乌兰察布市西部，
面积 3100 平方公里，辖 3 乡 5 镇，总人口 19.21 万人，常住人口 8.56 万人。
经济上以氯碱化工、钼金属、新能源（压缩空气储能、绿电）以及特色农牧业/文旅
（卓资熏鸡、明星沟4A景区）为主导产业。

Current leadership (confirmed 2026-08 from official 卓资县人民政府 领导之窗
https://www.zhuozi.gov.cn/zwgk/index.html 及县内会议报道):
- 县委书记: 王军 (1972年4月生, 大学本科, 中共党员; 2026年持续以县委书记履职)
- 县委副书记、政府代县长: 李晶 (1982年4月生, 察右前旗人, 2005年参加工作,
  在职研究生学历; 2026-07 起以"县委副书记、政府县长候选人/代县长"身份调研施政)

换班/调动背景:
- 前任县长: 么海明 — 2026-02-03 以政府县长身份向卓资县第十六届人大第五次会议
  作《2026年政府工作报告》, 后由李晶(县长候选人/代县长)接任, 属常规换届交接。
- 县委副书记、政法委书记 景海, 常务副县长 王轩 等为现任班子核心。

参考构建:
- scripts/build/build_和卓县_data.py / build_集宁区_data.py (内蒙古县域网络模板)
- data/tmp/inner_mongolia_乌兰察布市 (上一任务, 地级市班子)

来源为官方领导之窗 (swld/政府领导 zfld) + 县内新闻 (jrzz) + 政府工作报告。
"""

import sys
import os
import json  # noqa: F401  (used for person JSON below)
import sqlite3  # noqa: F401  (used via gov_relation.runner.run_build)

from pathlib import Path

_REPO = Path(__file__).resolve().parent
while not (_REPO / "gov_relation").is_dir() and _REPO != _REPO.parent:
    _REPO = _REPO.parent
sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402

SLUG = "卓资县"
# Staging-aware path: when run from the staging dir, write artifacts directly there;
# when promoted to scripts/build/, write to canonical data/ dirs.
_STAGING_DIR = Path(__file__).resolve().parent
_IS_STAGING = _STAGING_DIR.name.startswith("inner_mongolia_")
if _IS_STAGING:
    DB_PATH = _STAGING_DIR / "卓资县_network.db"
    GEXF_PATH = _STAGING_DIR / "卓资县_network.gexf"
    PJSON_DIR = _STAGING_DIR
else:
    DB_PATH = DATABASE_DIR / "卓资县_network.db"
    GEXF_PATH = GRAPH_DIR / "卓资县_network.gexf"
    PJSON_DIR = _REPO / "data" / "persons"


# ═══════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共卓资县委员会", "type": "党委", "level": "县",
     "parent": "中共乌兰察布市委", "location": "内蒙古自治区乌兰察布市卓资县"},
    {"id": 2, "name": "卓资县人民政府", "type": "政府", "level": "县",
     "parent": "乌兰察布市人民政府", "location": "内蒙古自治区乌兰察布市卓资县"},
    {"id": 3, "name": "卓资县人大常委会", "type": "人大", "level": "县",
     "parent": "乌兰察布市人大常委会", "location": "内蒙古自治区乌兰察布市卓资县"},
    {"id": 4, "name": "政协卓资县委员会", "type": "政协", "level": "县",
     "parent": "乌兰察布市政协", "location": "内蒙古自治区乌兰察布市卓资县"},
    {"id": 5, "name": "中共卓资县纪律检查委员会（监委）", "type": "纪委", "level": "县",
     "parent": "中共卓资县委", "location": "内蒙古自治区乌兰察布市卓资县"},
    {"id": 6, "name": "中共卓资县委政法委员会", "type": "党委", "level": "县",
     "parent": "中共卓资县委", "location": "内蒙古自治区乌兰察布市卓资县"},
    {"id": 7, "name": "中共卓资县委组织部", "type": "党委", "level": "县",
     "parent": "中共卓资县委", "location": "内蒙古自治区乌兰察布市卓资县"},
    {"id": 8, "name": "中共卓资县委宣传部", "type": "党委", "level": "县",
     "parent": "中共卓资县委", "location": "内蒙古自治区乌兰察布市卓资县"},
    {"id": 9, "name": "中共卓资县委统战部", "type": "党委", "level": "县",
     "parent": "中共卓资县委", "location": "内蒙古自治区乌兰察布市卓资县"},
    {"id": 10, "name": "中共卓资县委办公室", "type": "党委", "level": "县",
     "parent": "中共卓资县委", "location": "内蒙古自治区乌兰察布市卓资县"},
    {"id": 11, "name": "卓资县公安局", "type": "政府", "level": "县",
     "parent": "乌兰察布市公安局", "location": "内蒙古自治区乌兰察布市卓资县"},
    {"id": 12, "name": "卓资县人民武装部", "type": "政府", "level": "县",
     "parent": "乌兰察布军分区", "location": "内蒙古自治区乌兰察布市卓资县"},
    # 上级/相关组织（用于跨层级关系）
    {"id": 13, "name": "中共乌兰察布市委员会", "type": "党委", "level": "地级市",
     "parent": "中共内蒙古自治区委", "location": "内蒙古自治区乌兰察布市"},
    {"id": 14, "name": "乌兰察布市人民政府", "type": "政府", "level": "地级市",
     "parent": "内蒙古自治区人民政府", "location": "内蒙古自治区乌兰察布市"},
]

# ═══════════════════════════════════════════════════════════════════════════
# PERSONS
# ═══════════════════════════════════════════════════════════════════════════
SOURCE_LDZC = "https://www.zhuozi.gov.cn/zwgk/index.html 领导之窗(领导之窗)"

persons = [
    # ═══ 县委领导 ═══
    {"id": 1, "name": "王军", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年4月", "birthplace": "待查",
     "education": "大学本科", "party_join": "中共党员", "work_start": "待查",
     "current_post": "卓资县委书记",
     "current_org": "中共卓资县委员会",
     "source": SOURCE_LDZC + "; https://www.zhuozi.gov.cn/jrzz/1986139.html (2026-07)"},
    {"id": 2, "name": "李晶", "gender": "女", "ethnicity": "汉族",
     "birth": "1982年4月", "birthplace": "内蒙古乌兰察布市察右前旗",
     "education": "在职研究生学历", "party_join": "中共党员", "work_start": "2005年3月",
     "current_post": "县委副书记、政府代县长",
     "current_org": "卓资县人民政府",
     "source": SOURCE_LDZC + "; https://www.zhuozi.gov.cn/jrzz/1990609.html (2026-07)"},
    {"id": 3, "name": "景海", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "县委副书记、政法委书记",
     "current_org": "中共卓资县委政法委员会",
     "source": SOURCE_LDZC},
    {"id": 4, "name": "郭丽丽", "gender": "女", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "县委常委、宣传部部长",
     "current_org": "中共卓资县委宣传部",
     "source": SOURCE_LDZC},
    {"id": 5, "name": "王轩", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "县委常委、政府常务副县长",
     "current_org": "卓资县人民政府",
     "source": SOURCE_LDZC},
    {"id": 6, "name": "赵苏杨", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "县委常委、政府副县长",
     "current_org": "卓资县人民政府",
     "source": SOURCE_LDZC},
    {"id": 7, "name": "王宇林", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "县委常委、统战部部长",
     "current_org": "中共卓资县委统战部",
     "source": SOURCE_LDZC},
    {"id": 8, "name": "高学峰", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "县委常委、县委办公室主任",
     "current_org": "中共卓资县委办公室",
     "source": SOURCE_LDZC + "; 随县委书记调研报道多次出现(jrzz/1986139,1982983)"},
    {"id": 9, "name": "王昆云", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "县委常委、纪委书记",
     "current_org": "中共卓资县纪律检查委员会（监委）",
     "source": SOURCE_LDZC},
    {"id": 10, "name": "孙浩", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "县委常委、人民武装部上校部长",
     "current_org": "卓资县人民武装部",
     "source": SOURCE_LDZC},
    {"id": 11, "name": "张雨", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "县委常委、组织部部长",
     "current_org": "中共卓资县委组织部",
     "source": SOURCE_LDZC},
    {"id": 12, "name": "关金涛", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "县委常委、政府副县长（挂职）",
     "current_org": "卓资县人民政府",
     "source": SOURCE_LDZC},
    {"id": 13, "name": "司波", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "县委常委、政府副县长（挂职）",
     "current_org": "卓资县人民政府",
     "source": SOURCE_LDZC},
    # ═══ 政府领导（非常委）═══
    {"id": 14, "name": "班东波", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "政府副县长、公安局党委书记、局长",
     "current_org": "卓资县公安局",
     "source": SOURCE_LDZC},
    {"id": 15, "name": "段利文", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "政府副县长",
     "current_org": "卓资县人民政府",
     "source": SOURCE_LDZC},
    {"id": 16, "name": "刘佃文", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "政府副县长",
     "current_org": "卓资县人民政府",
     "source": SOURCE_LDZC},
    {"id": 17, "name": "苏和", "gender": "男", "ethnicity": "蒙古族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "政府副县长",
     "current_org": "卓资县人民政府",
     "source": SOURCE_LDZC},
    {"id": 18, "name": "褚文强", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "政府副县长",
     "current_org": "卓资县人民政府",
     "source": SOURCE_LDZC},
    # ═══ 人大 / 政协 ═══
    {"id": 19, "name": "郭红光", "gender": "男", "ethnicity": "汉族",
     "birth": "1969年12月", "birthplace": "内蒙古和林格尔县",
     "education": "大学本科", "party_join": "中共党员", "work_start": "1991年12月",
     "current_post": "县人大常委会党组书记、主任",
     "current_org": "卓资县人大常委会",
     "source": SOURCE_LDZC + "(rdld 人大领导)"},
    {"id": 20, "name": "白志平", "gender": "男", "ethnicity": "汉族",
     "birth": "1967年2月", "birthplace": "内蒙古卓资县",
     "education": "大学本科", "party_join": "中共党员", "work_start": "1989年9月",
     "current_post": "县政协党组书记、主席",
     "current_org": "政协卓资县委员会",
     "source": SOURCE_LDZC + "(zxld 政协领导)"},
    # ═══ 前任/前后任 ═══
    {"id": 21, "name": "么海明", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查",
     "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "（前任）卓资县人民政府县长",
     "current_org": "卓资县人民政府",
     "source": "2026-02-03 《2026年卓资县政府工作报告》(李晶前任, 后由李晶代任)"},
]

# ═══════════════════════════════════════════════════════════════════════════
# POSITIONS
# ═══════════════════════════════════════════════════════════════════════════
positions = [
    # 王军
    {"person_id": 1, "org_id": 13, "title": "（隶属）中共乌兰察布市委领导", "start": "", "end": "present", "rank": "正处级", "note": "县委书记为市委管理的县级班子一把手"},
    {"person_id": 1, "org_id": 1, "title": "卓资县委书记", "start": "", "end": "present", "rank": "正处级", "note": "任内主持县委全面工作; 2026年多场调研/党课报道"},
    # 李晶
    {"person_id": 2, "org_id": 1, "title": "卓资县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长候选人/县政府代县长", "start": "2026", "end": "present", "rank": "正处级", "note": "接替么海明; 主持县政府全面工作"},
    # 景海
    {"person_id": 3, "org_id": 1, "title": "卓资县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "政法委书记", "start": "", "end": "present", "rank": "副处级", "note": "政法、信访、维稳等"},
    # 郭丽丽
    {"person_id": 4, "org_id": 8, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": "意识形态、宣传文化"},
    # 王轩
    {"person_id": 5, "org_id": 1, "title": "卓资县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府常务工作"},
    # 赵苏杨
    {"person_id": 6, "org_id": 1, "title": "卓资县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王宇林
    {"person_id": 7, "org_id": 9, "title": "县委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 高学峰
    {"person_id": 8, "org_id": 10, "title": "县委常委、县委办公室主任", "start": "", "end": "present", "rank": "副处级", "note": "随县领导督办/带队下基层"},
    # 王昆云
    {"person_id": 9, "org_id": 5, "title": "县委常委、纪委书记", "start": "", "end": "present", "rank": "副处级", "note": "党风廉政、纪检监察"},
    # 孙浩
    {"person_id": 10, "org_id": 12, "title": "县委常委、人民武装部上校部长", "start": "", "end": "present", "rank": "正团级", "note": "国防动员、双拥"},
    # 张雨
    {"person_id": 11, "org_id": 7, "title": "县委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": "干部任免、编制、人才"},
    # 关金涛 / 司波（挂职）
    {"person_id": 12, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "国家部委/上级机关挂职干部"},
    {"person_id": 13, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "国家部委/上级机关挂职干部"},
    # 班东波
    {"person_id": 14, "org_id": 11, "title": "公安局党委书记、局长", "start": "", "end": "present", "rank": "正科级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "政法/公安系统"},
    # 其他政府副县长
    {"person_id": 15, "org_id": 2, "title": "政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "蒙古族"},
    {"person_id": 18, "org_id": 2, "title": "政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 郭红光 / 白志平
    {"person_id": 19, "org_id": 3, "title": "县人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正处级", "note": "1991年参加工作，和林格尔籍"},
    {"person_id": 20, "org_id": 4, "title": "县政协党组书记、主席", "start": "", "end": "present", "rank": "正处级", "note": "卓资县本地人"},
    # 么海明（前任县长）
    {"person_id": 21, "org_id": 2, "title": "政府县长", "start": "", "end": "2026", "rank": "正处级", "note": "前任县长; 2026-02-03 作政府工作报告, 后由李晶接任"},
]

# ═══════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════════════════
relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "卓资县党政一把手搭档：县委书记 王军 与 县政府代县长（县委副书记）李晶",
     "overlap_org": "中共卓资县委/卓资县人民政府", "overlap_period": "2026-"},
    # 书记 ↔ 各副书记/常委
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记 与 县委副书记、政法委书记（景海）", "overlap_org": "中共卓资县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与宣传部部长", "overlap_org": "中共卓资县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委书记与常务副县长", "overlap_org": "中共卓资县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与政府副县长", "overlap_org": "中共卓资县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "县委书记与统战部部长", "overlap_org": "中共卓资县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "县委书记与县委办主任（高学峰，随同调研）", "overlap_org": "中共卓资县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "县委书记与纪委书记（廉政条线）", "overlap_org": "中共卓资县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "县委书记与人武部上校部长", "overlap_org": "中共卓资县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "县委书记与组织部部长（干部条线密切）", "overlap_org": "中共卓资县委", "overlap_period": ""},
    # 代县长/县长 ↔ 副县长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "代县长与常务副县长", "overlap_org": "卓资县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "代县长与政府副县长", "overlap_org": "卓资县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "代县长与副县长、公安局长（政法）", "overlap_org": "卓资县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "代县长与政府副县长", "overlap_org": "卓资县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate",
     "context": "代县长与政府副县长", "overlap_org": "卓资县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate",
     "context": "代县长与政府副县长（蒙古族）", "overlap_org": "卓资县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 18, "type": "superior_subordinate",
     "context": "代县长与政府副县长", "overlap_org": "卓资县人民政府", "overlap_period": "2026-"},
    # 前任县长 → 现任代县长 (predecessor/successor)
    {"person_a": 21, "person_b": 2, "type": "predecessor_successor",
     "context": "么海明（前任县长）→ 李晶（代县长）职务更替", "overlap_org": "卓资县人民政府",
     "overlap_period": "2026 换届"},
    # 人大 / 政协 与班子衔接
    {"person_a": 1, "person_b": 19, "type": "superior_subordinate",
     "context": "县委书记 与 县人大常委会主任（郭红光）", "overlap_org": "中共卓资县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 20, "type": "superior_subordinate",
     "context": "县委书记 与 县政协主席（白志平）", "overlap_org": "中共卓资县委", "overlap_period": ""},
    # 李晶 — 察右前旗籍贯人际网络线索（weak, 籍贯专业）
    {"person_a": 2, "person_b": 19, "type": "same_native_place",
     "context": "李晶籍为察右前旗；无直接共事证据（弱线索）", "overlap_org": "", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════════════════════
# PERSON JSON FILES
# ═══════════════════════════════════════════════════════════════════════════
TODAY = "20260806"

_JOB_MAP = {
    "王军": "县委书记",
    "李晶": "县长",
    "么海明": "原县长",
    "郭红光": "人大主任",
    "白志平": "政协主席",
}


def write_person_json(person: dict) -> str:
    """Write a deep per-person graph JSON profile (staged or canonical)."""
    name = person["name"]
    job = _JOB_MAP.get(name, person["current_post"].split("、")[0].replace("，", "_").replace(" ", "_"))
    province = "内蒙古自治区"
    city = "乌兰察布市"
    fname = f"{TODAY}-{province}-{city}-{job}-{name}.json"
    fpath = PJSON_DIR / fname
    data = {
        "schema_version": "1.0",
        "generated_at": "2026-08-06",
        "investigation_scope": {
            "province": province, "city": city, "region": "卓资县",
            "job": person["current_post"], "task_id": "inner_mongolia_卓资县",
            "time_focus": "现任班子（截止2026-08-06）",
        },
        "identity": {
            "person_id": f"zhuozi_{name}",
            "name": name,
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "education": person.get("education", ""),
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {},
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "as_of": "2026-08-06",
            "is_current_confirmed": not person.get("is_former", False),
            "source": person.get("source", ""),
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {},
        "source_register": [
            {"id": "S01", "url": "https://www.zhuozi.gov.cn/zwgk/index.html",
             "source_type": "official", "reliability": "high",
             "note": "卓资县领导之窗（现任班子）"}
        ],
        "confidence_summary": {
            "identity": "confirmed" if person.get("source") else "plausible",
            "current_role": "confirmed" if person.get("source") else "plausible",
            "career_completeness": "thin" if person.get("birth", "") in ("", "待查") else "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "早年履历及跨区域调动明细待补",
        },
        "open_questions": [
            {"priority": "high", "question": "早年 (2000-2020) 详细任职履历",
             "why_it_matters": "识别来自何单位、何系统以推断跨区域网络",
             "suggested_queries": [f"{name} 简历 任职 乌兰察布"],
             "last_attempted": "2026-08-06"},
            {"priority": "medium", "question": "调动来源与前任/后任",
             "why_it_matters": "评估干部交流网络",
             "suggested_queries": [f"{name} 任前公示 调任 卓资"],
             "last_attempted": "2026-08-06"},
        ],
    }
    fpath.parent.mkdir(parents=True, exist_ok=True)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return fname


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    written = []
    for p in persons:
        if p["name"] in _JOB_MAP:
            written.append(write_person_json(p))
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Person JSON: {written}")
    print("BUILD OK")