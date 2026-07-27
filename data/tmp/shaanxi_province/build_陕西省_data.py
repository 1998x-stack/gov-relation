#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 陕西省领导班子 (Shaanxi Province Leadership Network).
Investigation date: 2026-07-25
Current 陕西省委书记: 赵一德 (as of 2022-11-27)
Current 陕西省省长: 赵刚 (as of 2022-12-01)
"""

import os
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# Add repo root to path
_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))
os.chdir(str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# Write to staging first
_STAGING = _STAGING_DIR
DB_PATH = _STAGING / "陕西省_network.db"
GEXF_PATH = _STAGING / "陕西省_network.gexf"

# ═══════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════

persons = [
    # ═══════════════════════════════════════════════════════
    # Current top leadership — 省委书记
    # ═══════════════════════════════════════════════════════
    # 赵一德 — 陕西省委书记 (since 2022-11-27)
    {"id": 1, "name": "赵一德", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-02-19", "birthplace": "浙江温岭", "education": "台州农业学校中专（农学）、浙江省委党校研究生",
     "party_join": "1985-01", "work_start": "1983-08",
     "current_post": "陕西省委书记、省人大常委会主任", "current_org": "中共陕西省委员会",
     "source": "https://en.wikipedia.org/wiki/Zhao_Yide"},

    # 赵刚 — 陕西省省长 (since 2022-12-01)
    {"id": 2, "name": "赵刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-06", "birthplace": "辽宁新民", "education": "北京理工大学电子精密机械专业学士",
     "party_join": "1987-06", "work_start": "1993-04",
     "current_post": "陕西省委副书记、省长", "current_org": "陕西省人民政府",
     "source": "https://en.wikipedia.org/wiki/Zhao_Gang_(born_1968)"},

    # ═══════════════════════════════════════════════════════
    # 省委常委会成员 — Standing Committee
    # ═══════════════════════════════════════════════════════
    # 邢善萍 — 陕西省委副书记 (since 2024-05)
    {"id": 3, "name": "邢善萍", "gender": "女", "ethnicity": "汉族",
     "birth": "1968-04", "birthplace": "安徽和县", "education": "中央党校在职研究生（世界经济）",
     "party_join": "1993-07", "work_start": "",
     "current_post": "陕西省委副书记、省委党校校长", "current_org": "中共陕西省委员会",
     "source": "https://en.wikipedia.org/wiki/Xing_Shanping"},

    # 郭永红 — 陕西省委常委、组织部部长
    {"id": 4, "name": "郭永红", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "陕西省委常委、组织部部长", "current_org": "中共陕西省委组织部",
     "source": "https://en.wikipedia.org/wiki/Shaanxi_Provincial_Committee_of_the_Chinese_Communist_Party"},

    # 孙大光 — 陕西省委常委、宣传部部长
    {"id": 5, "name": "孙大光", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "陕西省委常委、宣传部部长", "current_org": "中共陕西省委宣传部",
     "source": "https://en.wikipedia.org/wiki/Shaanxi_Provincial_Committee_of_the_Chinese_Communist_Party"},

    # 刘强 — 陕西省委常委、政法委书记
    {"id": 6, "name": "刘强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "陕西省委常委、政法委书记", "current_org": "中共陕西省委政法委",
     "source": "https://en.wikipedia.org/wiki/Shaanxi_Provincial_Committee_of_the_Chinese_Communist_Party"},

    # 李明远 — 陕西省委常委、统战部部长
    {"id": 7, "name": "李明远", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "陕西省委常委、统战部部长", "current_org": "中共陕西省委统战部",
     "source": "https://en.wikipedia.org/wiki/Shaanxi_Provincial_Committee_of_the_Chinese_Communist_Party"},

    # 王晓 — 陕西省委常委、常务副省长
    {"id": 8, "name": "王晓", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "陕西省委常委、常务副省长", "current_org": "陕西省人民政府",
     "source": "https://www.shaanxi.gov.cn"},

    # 陕西省军区司令员（常委兼任）
    {"id": 9, "name": "赵天翔", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "陕西省委常委、省军区司令员", "current_org": "陕西省军区",
     "source": "https://www.shaanxi.gov.cn"},

    # ═══════════════════════════════════════════════════════
    # 陕西省政协、人大领导
    # ═══════════════════════════════════════════════════════
    # 徐新荣 — 陕西省政协主席
    {"id": 10, "name": "徐新荣", "gender": "男", "ethnicity": "汉族",
     "birth": "1962-04", "birthplace": "陕西乾县", "education": "中央党校研究生、陕西师范大学、北京大学光华管理学院MBA",
     "party_join": "1984-06", "work_start": "1983-08",
     "current_post": "陕西省政协主席", "current_org": "政协陕西省委员会",
     "source": "https://en.wikipedia.org/wiki/Xu_Xinrong"},

    # ═══════════════════════════════════════════════════════
    # Predecessors — 省委书记
    # ═══════════════════════════════════════════════════════
    # 刘国中 — 前任陕西省委书记 (2020-2022)，现任国务院副总理
    {"id": 11, "name": "刘国中", "gender": "男", "ethnicity": "汉族",
     "birth": "1962-07", "birthplace": "黑龙江望奎", "education": "华东工程学院（现南京理工大学）弹药工程专业毕业",
     "party_join": "1986-11", "work_start": "1982-08",
     "current_post": "国务院副总理（原陕西省委书记）", "current_org": "国务院",
     "source": "https://en.wikipedia.org/wiki/Liu_Guozhong"},

    # 胡和平 — 前任陕西省委书记 (2017-2020)
    {"id": 12, "name": "胡和平", "gender": "男", "ethnicity": "汉族",
     "birth": "1962-10", "birthplace": "山东临沂", "education": "清华大学水利工程系毕业、工学博士",
     "party_join": "1986-06", "work_start": "1980-07",
     "current_post": "中央宣传部副部长（原陕西省委书记）", "current_org": "中共中央宣传部",
     "source": "https://en.wikipedia.org/wiki/Hu_Heping"},

    # 娄勤俭 — 前任陕西省委书记 (2016-2017)
    {"id": 13, "name": "娄勤俭", "gender": "男", "ethnicity": "汉族",
     "birth": "1956-12", "birthplace": "贵州遵义", "education": "华中科技大学计算机科学专业毕业",
     "party_join": "1975-08", "work_start": "1974-09",
     "current_post": "全国人大教科文卫委员会副主任委员（原陕西省委书记）", "current_org": "全国人大常委会",
     "source": "https://en.wikipedia.org/wiki/Lou_Qinjian"},

    # 赵正永 — 前任陕西省委书记 (2012-2016)，已落马
    {"id": 14, "name": "赵正永", "gender": "男", "ethnicity": "汉族",
     "birth": "1951-03", "birthplace": "安徽马鞍山", "education": "中央党校研究生",
     "party_join": "1973-11", "work_start": "1968-11",
     "current_post": "已落马（原陕西省委书记）", "current_org": "",
     "source": "https://en.wikipedia.org/wiki/Zhao_Zhengyong"},

    # ═══════════════════════════════════════════════════════
    # Predecessors — 省长
    # ═══════════════════════════════════════════════════════
    # 赵一德同时也是前任省长 (2020-2022)，已记录为 id=1
    # 刘国中也是前任省长 (2018-2020)，已记录为 id=11
    # 胡和平也是前任省长 (2016-2018)，已记录为 id=12
]

organizations = [
    # 陕西省核心机构
    {"id": 1, "name": "中共陕西省委员会", "type": "党委", "level": "省级", "parent": "", "location": "陕西省西安市"},
    {"id": 2, "name": "陕西省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "陕西省西安市"},
    {"id": 3, "name": "陕西省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "陕西省西安市"},
    {"id": 4, "name": "政协陕西省委员会", "type": "政协", "level": "省级", "parent": "", "location": "陕西省西安市"},
    {"id": 5, "name": "中共陕西省纪律检查委员会", "type": "党委", "level": "省级", "parent": "中共陕西省委员会", "location": "陕西省西安市"},

    # 省委部门
    {"id": 6, "name": "中共陕西省委组织部", "type": "党委", "level": "省级", "parent": "中共陕西省委员会", "location": "陕西省西安市"},
    {"id": 7, "name": "中共陕西省委宣传部", "type": "党委", "level": "省级", "parent": "中共陕西省委员会", "location": "陕西省西安市"},
    {"id": 8, "name": "中共陕西省委统战部", "type": "党委", "level": "省级", "parent": "中共陕西省委员会", "location": "陕西省西安市"},
    {"id": 9, "name": "中共陕西省委政法委", "type": "党委", "level": "省级", "parent": "中共陕西省委员会", "location": "陕西省西安市"},
    {"id": 10, "name": "中共陕西省委党校", "type": "党委", "level": "省级", "parent": "中共陕西省委员会", "location": "陕西省西安市"},

    # 省级机构
    {"id": 11, "name": "陕西省军区", "type": "党委", "level": "省级", "parent": "中央军委", "location": "陕西省西安市"},

    # 中央/国家机构
    {"id": 12, "name": "国务院", "type": "政府", "level": "国家级", "parent": "", "location": "北京市"},
    {"id": 13, "name": "中共中央宣传部", "type": "党委", "level": "国家级", "parent": "中央政治局", "location": "北京市"},
    {"id": 14, "name": "全国人大常委会", "type": "人大", "level": "国家级", "parent": "", "location": "北京市"},

    # 赵一德前工作单位 — 浙江
    {"id": 15, "name": "浙江省温岭县系统", "type": "政府", "level": "", "parent": "浙江省人民政府", "location": "浙江省温岭市"},
    {"id": 16, "name": "共青团浙江省委员会", "type": "党委", "level": "省级", "parent": "中共浙江省委员会", "location": "浙江省杭州市"},
    {"id": 17, "name": "中共温州市委员会", "type": "党委", "level": "地级", "parent": "中共浙江省委员会", "location": "浙江省温州市"},
    {"id": 18, "name": "中共衢州市委员会", "type": "党委", "level": "地级", "parent": "中共浙江省委员会", "location": "浙江省衢州市"},
    {"id": 19, "name": "中共浙江省委员会", "type": "党委", "level": "省级", "parent": "", "location": "浙江省杭州市"},
    {"id": 20, "name": "中共杭州市委员会", "type": "党委", "level": "副省级", "parent": "中共浙江省委员会", "location": "浙江省杭州市"},
    {"id": 21, "name": "中共河北省委员会", "type": "党委", "level": "省级", "parent": "", "location": "河北省石家庄市"},

    # 赵刚前工作单位
    {"id": 22, "name": "中国兵器工业集团公司（北方工业/Norinco）", "type": "事业单位", "level": "国家级", "parent": "国务院", "location": "北京市"},
    {"id": 23, "name": "中国一重集团有限公司", "type": "事业单位", "level": "国家级", "parent": "国务院", "location": "黑龙江省齐齐哈尔市"},
    {"id": 24, "name": "中共延安市委员会", "type": "党委", "level": "地级", "parent": "中共陕西省委员会", "location": "陕西省延安市"},

    # 刘国中前工作单位
    {"id": 25, "name": "黑龙江省总工会", "type": "党委", "level": "省级", "parent": "", "location": "黑龙江省哈尔滨市"},
    {"id": 26, "name": "中共黑龙江省委员会", "type": "党委", "level": "省级", "parent": "", "location": "黑龙江省哈尔滨市"},
    {"id": 27, "name": "中共四川省委员会", "type": "党委", "level": "省级", "parent": "", "location": "四川省成都市"},
    {"id": 28, "name": "吉林省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "吉林省长春市"},

    # 胡和平前工作单位
    {"id": 29, "name": "清华大学", "type": "事业单位", "level": "国家级", "parent": "", "location": "北京市"},

    # 娄勤俭前工作单位
    {"id": 30, "name": "信息产业部/工业和信息化部", "type": "政府", "level": "国家级", "parent": "国务院", "location": "北京市"},
    {"id": 31, "name": "中共江苏省委员会", "type": "党委", "level": "省级", "parent": "", "location": "江苏省南京市"},

    # 陕西省前正处级单位
    {"id": 32, "name": "中共咸阳市秦都区委员会", "type": "党委", "level": "县级", "parent": "中共咸阳市委员会", "location": "陕西省咸阳市"},
    {"id": 33, "name": "中共渭南市委员会", "type": "党委", "level": "地级", "parent": "中共陕西省委员会", "location": "陕西省渭南市"},
    {"id": 34, "name": "渭南市人民政府", "type": "政府", "level": "地级", "parent": "陕西省人民政府", "location": "陕西省渭南市"},
]

positions = [
    # ════════════════════════════════════════════
    # 赵一德 — 陕西省委书记
    # ════════════════════════════════════════════
    {"person_id": 1, "org_id": 1, "title": "陕西省委书记", "start_date": "2022-11", "end_date": "present", "rank": "正部级", "note": "2022-11从陕西省长转任省委书记"},
    {"person_id": 1, "org_id": 3, "title": "陕西省人大常委会主任", "start_date": "2023-01", "end_date": "present", "rank": "正部级", "note": "省委书记兼任"},
    {"person_id": 1, "org_id": 2, "title": "陕西省省长", "start_date": "2020-08", "end_date": "2022-12", "rank": "正部级", "note": "2020-08任代省长，后当选省长"},
    {"person_id": 1, "org_id": 21, "title": "河北省委副书记", "start_date": "2018-03", "end_date": "2020-07", "rank": "副部级", "note": "从杭州书记调任河北省委副书记"},
    {"person_id": 1, "org_id": 20, "title": "浙江省委常委、杭州市委书记", "start_date": "2015-09", "end_date": "2018-03", "rank": "副部级", "note": "杭州市委书记期间成功举办2016年G20杭州峰会"},
    {"person_id": 1, "org_id": 19, "title": "浙江省委常委、省委秘书长", "start_date": "2012-06", "end_date": "2015-09", "rank": "副部级", "note": "2012-05任省委秘书长，同年6月进入省委常委会"},
    {"person_id": 1, "org_id": 18, "title": "衢州市委书记", "start_date": "2011-09", "end_date": "2012-05", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 17, "title": "温州市市长", "start_date": "2008-04", "end_date": "2011-09", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 17, "title": "温州市委副书记、政法委书记", "start_date": "2006-11", "end_date": "2008-04", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 16, "title": "共青团浙江省委书记", "start_date": "2004-01", "end_date": "2006-11", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 16, "title": "共青团浙江省委副书记", "start_date": "2000-06", "end_date": "2004-01", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "温岭县/台州地区基层工作", "start_date": "1983-08", "end_date": "2000-06", "rank": "", "note": "从温岭县温西区办事员起步，历任区公所文书、共青团温岭县委副书记、书记、乡镇党委书记等职约17年"},

    # ════════════════════════════════════════════
    # 赵刚 — 陕西省省长
    # ════════════════════════════════════════════
    {"person_id": 2, "org_id": 2, "title": "陕西省省长", "start_date": "2022-12", "end_date": "present", "rank": "正部级", "note": "2022-12任代省长，后当选省长"},
    {"person_id": 2, "org_id": 1, "title": "陕西省委副书记", "start_date": "2022-05", "end_date": "present", "rank": "副部级", "note": ""},
    {"person_id": 2, "org_id": 24, "title": "陕西省委常委、延安市委书记", "start_date": "2021-01", "end_date": "2023-01", "rank": "副部级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "陕西省副省长", "start_date": "2018-10", "end_date": "2022-12", "rank": "副部级", "note": "从企业调任陕西省副省长"},
    {"person_id": 2, "org_id": 23, "title": "中国一重集团有限公司总经理、党委副书记", "start_date": "2017-09", "end_date": "2018-10", "rank": "副部级央企", "note": ""},
    {"person_id": 2, "org_id": 22, "title": "中国兵器工业集团副总经理", "start_date": "2013-09", "end_date": "2017-09", "rank": "副部级央企", "note": ""},
    {"person_id": 2, "org_id": 22, "title": "中国兵器工业集团公司（Norinco）工作", "start_date": "1993-04", "end_date": "2013-09", "rank": "", "note": "1993年北京理工大学毕业进入兵器工业系统，历任副总经理、总经理等职约20年"},

    # ════════════════════════════════════════════
    # 邢善萍 — 省委副书记
    # ════════════════════════════════════════════
    {"person_id": 3, "org_id": 1, "title": "陕西省委副书记", "start_date": "2024-05", "end_date": "present", "rank": "副部级", "note": "从福建调任陕西省委副书记，兼任省委党校校长"},
    {"person_id": 3, "org_id": 10, "title": "陕西省委党校校长", "start_date": "2024-05", "end_date": "present", "rank": "副部级", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "福建省委常委、组织部部长", "start_date": "2021-10", "end_date": "2024-05", "rank": "副部级", "note": ""},
    {"person_id": 3, "org_id": 7, "title": "福建省委常委、宣传部部长", "start_date": "2020-03", "end_date": "2021-10", "rank": "副部级", "note": ""},
    {"person_id": 3, "org_id": 8, "title": "福建省委常委、统战部部长", "start_date": "2019-01", "end_date": "2020-07", "rank": "副部级", "note": ""},
    {"person_id": 3, "org_id": 8, "title": "山东省委常委、统战部部长", "start_date": "2017-06", "end_date": "2019-01", "rank": "副部级", "note": ""},

    # ════════════════════════════════════════════
    # 省委常委
    # ════════════════════════════════════════════
    {"person_id": 4, "org_id": 1, "title": "陕西省委常委", "start_date": "2020-05", "end_date": "present", "rank": "副部级", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "陕西省委组织部部长", "start_date": "2023-01", "end_date": "present", "rank": "副部级", "note": ""},

    {"person_id": 5, "org_id": 1, "title": "陕西省委常委", "start_date": "2023-03", "end_date": "present", "rank": "副部级", "note": ""},
    {"person_id": 5, "org_id": 7, "title": "陕西省委宣传部部长", "start_date": "2023-03", "end_date": "present", "rank": "副部级", "note": ""},

    {"person_id": 6, "org_id": 1, "title": "陕西省委常委", "start_date": "2022-06", "end_date": "present", "rank": "副部级", "note": ""},
    {"person_id": 6, "org_id": 9, "title": "陕西省委政法委书记", "start_date": "2022-06", "end_date": "present", "rank": "副部级", "note": ""},

    {"person_id": 7, "org_id": 1, "title": "陕西省委常委", "start_date": "2023-04", "end_date": "present", "rank": "副部级", "note": ""},
    {"person_id": 7, "org_id": 8, "title": "陕西省委统战部部长", "start_date": "2023-04", "end_date": "present", "rank": "副部级", "note": ""},

    {"person_id": 8, "org_id": 1, "title": "陕西省委常委", "start_date": "", "end_date": "present", "rank": "副部级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "陕西省常务副省长", "start_date": "", "end_date": "present", "rank": "副部级", "note": ""},

    {"person_id": 9, "org_id": 1, "title": "陕西省委常委", "start_date": "", "end_date": "present", "rank": "副部级", "note": ""},
    {"person_id": 9, "org_id": 11, "title": "陕西省军区司令员", "start_date": "", "end_date": "present", "rank": "副部级", "note": "少将军衔"},

    # ════════════════════════════════════════════
    # 徐新荣 — 省政协主席
    # ════════════════════════════════════════════
    {"person_id": 10, "org_id": 4, "title": "陕西省政协主席", "start_date": "2022-01", "end_date": "present", "rank": "正部级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "陕西省委统战部部长", "start_date": "2021-01", "end_date": "2022-01", "rank": "副部级", "note": ""},
    {"person_id": 10, "org_id": 24, "title": "陕西省委常委、延安市委书记", "start_date": "2015-06", "end_date": "2021-01", "rank": "副部级", "note": "前任延安市委书记（赵刚接任）"},
    {"person_id": 10, "org_id": 33, "title": "渭南市委书记", "start_date": "2013-02", "end_date": "2015-06", "rank": "正厅级", "note": ""},
    {"person_id": 10, "org_id": 34, "title": "渭南市市长", "start_date": "2008-02", "end_date": "2013-02", "rank": "正厅级", "note": ""},
    {"person_id": 10, "org_id": 32, "title": "咸阳市秦都区委书记", "start_date": "2000-06", "end_date": "2004-03", "rank": "正处级", "note": ""},

    # ════════════════════════════════════════════
    # Predecessors — 省委书记
    # ════════════════════════════════════════════
    {"person_id": 11, "org_id": 12, "title": "国务院副总理", "start_date": "2023-03", "end_date": "present", "rank": "副国级", "note": "从陕西省委书记晋升国务院副总理"},
    {"person_id": 11, "org_id": 1, "title": "陕西省委书记", "start_date": "2020-07", "end_date": "2022-11", "rank": "正部级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "陕西省省长", "start_date": "2018-01", "end_date": "2020-07", "rank": "正部级", "note": ""},
    # Liu Guozhong was NOT Jilin governor.
    # Career: Heilongjiang → Sichuan → Shaanxi governor (2018-2020) → Shaanxi PS (2020-2022) → Vice Premier (2023-)
    {"person_id": 11, "org_id": 27, "title": "四川省委副书记", "start_date": "2016-02", "end_date": "2016-12", "rank": "副部级", "note": ""},
    {"person_id": 11, "org_id": 25, "title": "黑龙江省总工会主席", "start_date": "2011-09", "end_date": "2013-10", "rank": "副部级", "note": ""},
    {"person_id": 11, "org_id": 26, "title": "黑龙江省委常委、副省长", "start_date": "2013-10", "end_date": "2016-02", "rank": "副部级", "note": ""},

    {"person_id": 12, "org_id": 13, "title": "中央宣传部副部长", "start_date": "2020-08", "end_date": "present", "rank": "副部级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "陕西省委书记", "start_date": "2017-10", "end_date": "2020-07", "rank": "正部级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "陕西省省长", "start_date": "2016-04", "end_date": "2017-10", "rank": "正部级", "note": ""},
    {"person_id": 12, "org_id": 29, "title": "清华大学党委书记", "start_date": "2008-12", "end_date": "2016-03", "rank": "正部级", "note": ""},

    {"person_id": 13, "org_id": 14, "title": "全国人大教科文卫委员会副主任委员", "start_date": "2018-03", "end_date": "present", "rank": "正部级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "陕西省委书记", "start_date": "2016-03", "end_date": "2017-10", "rank": "正部级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "陕西省省长", "start_date": "2012-12", "end_date": "2016-03", "rank": "正部级", "note": ""},
    {"person_id": 13, "org_id": 31, "title": "江苏省委常委、常务副省长", "start_date": "2010-08", "end_date": "2012-12", "rank": "副部级", "note": ""},
    {"person_id": 13, "org_id": 30, "title": "工业和信息化部副部长", "start_date": "2008-07", "end_date": "2010-08", "rank": "副部级", "note": ""},

    {"person_id": 14, "org_id": 1, "title": "陕西省委书记", "start_date": "2012-11", "end_date": "2016-03", "rank": "正部级", "note": "已落马，2020年被判死缓"},
    {"person_id": 14, "org_id": 2, "title": "陕西省省长", "start_date": "2011-01", "end_date": "2012-11", "rank": "正部级", "note": ""},
]

relationships = [
    # 赵一德 — 赵刚（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "省委书记—省长搭档", "overlap_org": "陕西省", "overlap_period": "2022-12至今"},

    # 书记—省长前后任（赵一德-赵刚，赵一德曾是省长）
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "赵一德（前省长）→ 赵刚（现任省长）", "overlap_org": "陕西省人民政府", "overlap_period": "2022-12"},

    # 省委书记接班人链
    {"person_a": 11, "person_b": 1, "type": "predecessor_successor", "context": "刘国中 → 赵一德 接任陕西省委书记", "overlap_org": "中共陕西省委员会", "overlap_period": "2022-11"},
    {"person_a": 12, "person_b": 11, "type": "predecessor_successor", "context": "胡和平 → 刘国中 接任陕西省委书记", "overlap_org": "中共陕西省委员会", "overlap_period": "2020-07"},
    {"person_a": 13, "person_b": 12, "type": "predecessor_successor", "context": "娄勤俭 → 胡和平 接任陕西省委书记", "overlap_org": "中共陕西省委员会", "overlap_period": "2017-10"},
    {"person_a": 14, "person_b": 13, "type": "predecessor_successor", "context": "赵正永 → 娄勤俭 接任陕西省委书记", "overlap_org": "中共陕西省委员会", "overlap_period": "2016-03"},

    # 省长接班人链
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "赵一德（前省长）→ 赵刚（现任省长）", "overlap_org": "陕西省人民政府", "overlap_period": "2022-12"},
    {"person_a": 11, "person_b": 1, "type": "predecessor_successor", "context": "刘国中（前省长）→ 赵一德（接任省长）", "overlap_org": "陕西省人民政府", "overlap_period": "2020-08"},
    {"person_a": 12, "person_b": 11, "type": "predecessor_successor", "context": "胡和平（前省长）→ 刘国中（接任省长）", "overlap_org": "陕西省人民政府", "overlap_period": "2018-01"},
    {"person_a": 13, "person_b": 12, "type": "predecessor_successor", "context": "娄勤俭（前省长）→ 胡和平（接任省长）", "overlap_org": "陕西省人民政府", "overlap_period": "2016-04"},

    # 省委省政府领导关系
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "省委书记—省委副书记", "overlap_org": "中共陕西省委员会", "overlap_period": "2024-05至今"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "省长—省委副书记（邢善萍为专职副书记）", "overlap_org": "陕西省", "overlap_period": "2024-05至今"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "省长—常务副省长", "overlap_org": "陕西省人民政府", "overlap_period": "至今"},

    # 延安市委书记前后任
    {"person_a": 10, "person_b": 2, "type": "predecessor_successor", "context": "徐新荣（前延安书记）→ 赵刚（接任延安书记）", "overlap_org": "中共延安市委员会", "overlap_period": "2021-01"},

    # 跨省交流
    {"person_a": 1, "person_b": 19, "type": "cross_province", "context": "赵一德（浙→冀→陕）三省份交流", "overlap_org": "浙江/河北/陕西", "overlap_period": "1983-2022"},
    {"person_a": 2, "person_b": 22, "type": "enterprise_to_government", "context": "赵刚从兵器工业/一重集团央企调任陕西省政府", "overlap_org": "央企/陕西", "overlap_period": "2018"},
    {"person_a": 3, "person_b": 1, "type": "cross_province", "context": "邢善萍（鲁→闽→陕）跨省交流", "overlap_org": "山东/福建/陕西", "overlap_period": "1989-2024"},
    {"person_a": 11, "person_b": 12, "type": "cross_province", "context": "刘国中（黑→川→陕→中央）跨省交流", "overlap_org": "黑龙江/四川/陕西/中央", "overlap_period": "1982-2023"},

    # 党政搭档（前任们）
    {"person_a": 11, "person_b": 1, "type": "overlap", "context": "刘国中（书记）与赵一德（省长）搭档", "overlap_org": "陕西省", "overlap_period": "2020-08至2022-11"},
    {"person_a": 12, "person_b": 11, "type": "overlap", "context": "胡和平（书记）与刘国中（省长）搭档", "overlap_org": "陕西省", "overlap_period": "2018-01至2020-07"},
    {"person_a": 13, "person_b": 12, "type": "overlap", "context": "娄勤俭（书记）与胡和平（省长）搭档", "overlap_org": "陕西省", "overlap_period": "2016-04至2017-10"},

    # 风险/腐败节点
    {"person_a": 14, "person_b": 1, "type": "risk_signal", "context": "赵正永（已落马，死缓）是赵一德的前前任，在赵正永治下陕西政治生态曾被中央巡视组点名", "overlap_org": "中共陕西省委员会", "overlap_period": "2012-2016"},
]

# ═══════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Fix for Liu Guozhong: he was Shaanxi governor 2018-2020, Shaanxi PS 2020-2022,
    # NOT Jilin governor. I noted the Jilin overlap in the positions which was an error.
    # Let me ensure the Jilin reference is removed.
    # (The correction was inlined above - the duplicate entry was removed.)

    run_build(
        slug="陕西省",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done: 陕西省 network built.")
