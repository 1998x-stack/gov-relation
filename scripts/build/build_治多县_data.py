#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 治多县 leadership network.

治多县隶属青海省玉树藏族自治州，位于青海省南部、三江源核心区，是长江发源地、
全国平均海拔最高、主体民族（藏族）比例最高的县城之一，素有"万里长江第一县"、
"可可西里门户"之称。县域面积 8.06 万平方公里，辖五乡一镇，平均海拔 4500 米以上。

Current leadership as of 2026-08 (sources: 治多县人民政府网站 www.zhiduo.gov.cn、
治多党建网 www.zhiduodj.gov.cn、县十六届人大五次会议公报):
- 县委书记: 池永杰（兼玉树州人大常委会副主任，2022 年起；2025-07 仍以"治多县委书记"名义履职）
- 县委副书记、代县长: 马小鹏（2026-07 起以"代县长"身份履职，汛期/经济运行/养老等多次现场）
- 县长(前任): 普措格来（县委副书记、县长，2022-10 至 2025/26）

县委书记职级无人事公示（县以下任命多不公开任前公示），生平/历任日期等以来源标注置信度。
县委书记/县长更亲前任链条、马小鹏任代县长前职务、人民政协主席等为公开资料未见/未确认项。

Confidence: confirmed = 官方官网/两会公报；plausible = 党媒/地方报道；unverified = 内部线索。
Biography 单体不完整者置于 person JSON 的 open_questions 与 report/open_gaps.md。
"""

import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _parent in REPO_ROOT.parents:
    if (_parent / "gov_relation").is_dir():
        REPO_ROOT = _parent
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "治多县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "治多县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "治多县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "治多县_network.db"
    GEXF_PATH = GRAPH_DIR / "治多县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共治多县委员会", "type": "党委", "level": "县处级", "parent": "中共玉树州委", "location": "青海省玉树藏族自治州治多县"},
    {"id": 2, "name": "治多县人民政府", "type": "政府", "level": "县处级", "parent": "玉树州人民政府", "location": "青海省玉树藏族自治州治多县"},
    {"id": 3, "name": "治多县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "玉树州人大常委会", "location": "青海省玉树藏族自治州治多县"},
    {"id": 4, "name": "中国人民政治协商会议治多县委员会", "type": "政协", "level": "县处级", "parent": "政协玉树州委员会", "location": "青海省玉树藏族自治州治多县"},
    {"id": 5, "name": "中共治多县纪律检查委员会/治多县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共玉树州纪委", "location": "青海省玉树藏族自治州治多县"},
    {"id": 6, "name": "治多县人民法院", "type": "法院", "level": "县处级", "parent": "玉树州中级人民法院", "location": "青海省玉树藏族自治州治多县"},
    {"id": 7, "name": "治多县人民检察院", "type": "检察院", "level": "县处级", "parent": "玉树州人民检察院", "location": "青海省玉树藏族自治州治多县"},
    {"id": 8, "name": "中共玉树州委员会", "type": "党委", "level": "地厅级", "parent": "中共青海省委", "location": "青海省玉树藏族自治州玉树市"},
    {"id": 9, "name": "玉树藏族自治州人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "青海省人大常委会", "location": "青海省玉树藏族自治州玉树市"},
    {"id": 10, "name": "中共北京市丰台区委员会", "type": "党委", "level": "地厅级", "parent": "中共北京市委", "location": "北京市丰台区"},
    {"id": 11, "name": "北京市丰台区人民政府", "type": "政府", "level": "地厅级", "parent": "北京市人民政府", "location": "北京市丰台区"},
    {"id": 12, "name": "中共北京市丰台区玉泉营街道工作委员会", "type": "党委部门", "level": "正处级", "parent": "中共北京市丰台区委", "location": "北京市丰台区玉泉营街道"},
    {"id": 13, "name": "北京理工大学", "type": "事业单位", "level": "正厅级", "parent": "", "location": "北京市海淀区"},
    {"id": 14, "name": "北京航空航天大学", "type": "事业单位", "level": "正厅级", "parent": "", "location": "北京市海淀区"},
    {"id": 15, "name": "教育部职业教育与成人教育司", "type": "政府部门", "level": "司局级", "parent": "中华人民共和国教育部", "location": "北京市"},
    {"id": 16, "name": "治多县总工会", "type": "群团", "level": "县处级", "parent": "玉树州总工会", "location": "青海省玉树藏族自治州治多县"},
    {"id": 17, "name": "治多县人民法院(法警队)/县委政法委", "type": "政法", "level": "县处级", "parent": "中共治多县委", "location": "青海省玉树藏族自治州治多县"},
    {"id": 18, "name": "治多县索加乡党委", "type": "乡镇", "level": "乡科级", "parent": "中共治多县委", "location": "青海省玉树藏族自治州治多县索加乡"},
    {"id": 19, "name": "治多县政法委", "type": "政法", "level": "县处级", "parent": "中共治多县委", "location": "青海省玉树藏族自治州治多县"},
    {"id": 20, "name": "中共治多县委组织部", "type": "党委部门", "level": "县处级", "parent": "中共治多县委", "location": "青海省玉树藏族自治州治多县"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 池永杰 — 县委书记（现任）
    {"id": 1, "name": "池永杰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共治多县委书记（兼玉树州人大常委会副主任）", "current_org": "中共治多县委员会",
     "source": "https://www.zhiduodj.gov.cn/Index/Read/10260.html"},
    # 2 — 马小鹏 — 县委副书记、代县长（现任）
    {"id": 2, "name": "马小鹏", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县委副书记、县人民政府代县长", "current_org": "治多县人民政府",
     "source": "http://www.zhiduo.gov.cn/html/745/634785.html"},
    # 3 — 普措格来 — 县长（前任，2022-2026）
    {"id": 3, "name": "普措格来", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县原县委副书记、县长（2026年离任）", "current_org": "治多县人民政府",
     "source": "http://www.zhiduo.gov.cn/html/738/634271.html"},
    # 4 — 段斌 — 县委副书记、副县长（挂职，北京对口支援）
    {"id": 4, "name": "段斌", "gender": "男", "ethnicity": "",
     "birth": "1988年", "birthplace": "陕西咸阳",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "2014年6月",
     "current_post": "治多县委副书记、副县长（援青干部，2025-08起）", "current_org": "治多县人民政府",
     "source": "http://www.zhiduo.gov.cn/html/840/634191.html"},
    # 5 — 刘俊 — 县委副书记、副县长（挂职，教育部）
    {"id": 5, "name": "刘俊", "gender": "男", "ethnicity": "",
     "birth": "1982年3月", "birthplace": "",
     "education": "博士研究生学历", "party_join": "中共党员", "work_start": "2004年",
     "current_post": "治多县委副书记、副县长（援疆，2025-08起）", "current_org": "治多县人民政府",
     "source": "http://www.zhiduo.gov.cn/html/840/634190.html"},
    # 6 — 任喜春 — 县委副书记
    {"id": 6, "name": "任喜春", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县委副书记", "current_org": "中共治多县委员会",
     "source": "https://www.zhiduodj.gov.cn/Index/Read/10258.html"},
    # 7 — 公却才旺 — 县委常委、政法委书记
    {"id": 7, "name": "公却才旺", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县委常委、政法委书记", "current_org": "治多县政法委",
     "source": "http://www.zhiduo.gov.cn/html/738/634202.html"},
    # 8 — 刘挺 — 县委常委、组织部部长
    {"id": 8, "name": "刘挺", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县委常委、组织部部长", "current_org": "中共治多县委组织部",
     "source": "https://www.zhiduodj.gov.cn/List/Read/10206.html"},
    # 9 — 赫发春 — 县委常委、副县长人选
    {"id": 9, "name": "赫发春", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县委常委、副县长人选（2026-07）", "current_org": "治多县人民政府",
     "source": "http://www.zhiduo.gov.cn/html/738/634804.html"},
    # 10 — 五一 — 副县长
    {"id": 10, "name": "五一", "gender": "男", "ethnicity": "藏族",
     "birth": "1979年5月", "birthplace": "青海治多",
     "education": "青海民族学院法学专业本科学历", "party_join": "2001年7月入党", "work_start": "1996年4月",
     "current_post": "治多县人民政府副县长", "current_org": "治多县人民政府",
     "source": "http://www.zhiduo.gov.cn/html/840/619318.html"},
    # 11 — 昂文扎西 — 副县长（原政协副主席）
    {"id": 11, "name": "昂文扎西", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县人民政府副县长（原县政协副主席）", "current_org": "治多县人民政府",
     "source": "http://www.zhiduo.gov.cn/html/840/634276.html"},
    # 12 — 陈鸿雁 — 副县长
    {"id": 12, "name": "陈鸿雁", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县人民政府副县长", "current_org": "治多县人民政府",
     "source": "http://www.zhiduo.gov.cn/html/738/634202.html"},
    # 13 — 才仁旺加 — 副县长
    {"id": 13, "name": "才仁旺加", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县人民政府副县长", "current_org": "治多县人民政府",
     "source": "http://www.zhiduo.gov.cn/html/738/634202.html"},
    # 14 — 吴海勇 — 副县长
    {"id": 14, "name": "吴海勇", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县人民政府副县长", "current_org": "治多县人民政府",
     "source": "http://www.zhiduo.gov.cn/html/738/634202.html"},
    # 15 — 张华 — 副县长
    {"id": 15, "name": "张华", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县人民政府副县长", "current_org": "治多县人民政府",
     "source": "http://www.zhiduo.gov.cn/html/738/634000.html"},
    # 16 — 白项欠 — 副县长（2022时段）
    {"id": 16, "name": "白项欠", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县人民政府原副县长", "current_org": "治多县人民政府",
     "source": "http://www.zhiduo.gov.cn/html/738/List-16.html"},
    # 17 — 荣伟 — 县委常委、常务副县长（2023时段）
    {"id": 17, "name": "荣伟", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县委原常委、常务副县长", "current_org": "治多县人民政府",
     "source": "http://www.zhiduo.gov.cn/html/738/List-11.html"},
    # 18 — 文雅 — 县人大常委会主任
    {"id": 18, "name": "文雅", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县人大常委会主任", "current_org": "治多县人民代表大会常务委员会",
     "source": "http://www.zhiduo.gov.cn/html/738/632440.html"},
    # 19 — 刘洪祥 — 县人大常委会副主任
    {"id": 19, "name": "刘洪祥", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县人大常委会副主任", "current_org": "治多县人民代表大会常务委员会",
     "source": "http://www.zhiduo.gov.cn/html/738/632440.html"},
    # 20 — 刘文骥 — 县人民法院代理院长
    {"id": 20, "name": "刘文骥", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县人民法院代理院长", "current_org": "治多县人民法院",
     "source": "http://www.zhiduo.gov.cn/html/738/632440.html"},
    # 21 — 梅杭秀 — 县人民检察院检察长
    {"id": 21, "name": "梅杭秀", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县人民检察院检察长", "current_org": "治多县人民检察院",
     "source": "http://www.zhiduo.gov.cn/html/738/632440.html"},
    # 22 — 索昂尼保 — 县纪委副书记、监委副主任
    {"id": 22, "name": "索昂尼保", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县纪委副书记、监委副主任", "current_org": "中共治多县纪律检查委员会",
     "source": "http://www.zhiduo.gov.cn/html/738/634805.html"},
    # 23 — 马兰 — 县委组织部部长（前任，退休慰问报道线索）
    {"id": 23, "name": "马兰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县原县委组织部部长", "current_org": "中共治多县委员会",
     "source": "https://www.zhiduodj.gov.cn/News/Read/10238.html"},
    # 24 — 伊拉 — 县委常委、常务副县长（2022时段）
    {"id": 24, "name": "伊拉", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "治多县原县委常委、常务副县长", "current_org": "治多县人民政府",
     "source": "http://www.zhiduo.gov.cn/html/738/List-16.html"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 1 — 池永杰
    {"person_id": 1, "org_id": 1, "title": "治多县委书记", "start_date": "2022", "end_date": "present", "rank": "正处级", "note": "官方报道2022年已任；2025-07仍以书记名义履职（兼职州人大副主任）"},
    {"person_id": 1, "org_id": 9, "title": "玉树州人大常委会副主任（兼）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "州人大常委会副主任兼职"},
    # 2 马小鹏
    {"person_id": 2, "org_id": 2, "title": "治多县委副书记、代县长", "start_date": "2026", "end_date": "present", "rank": "正处级", "note": "2026-07汛期/经济运行/养老等多次履职"},
    # 3 普措格来
    {"person_id": 3, "org_id": 2, "title": "治多县委副书记、县长", "start_date": "2022", "end_date": "2025", "rank": "正处级", "note": "2022-10确认任县长；2025-11仍任；2026转由马小鹏代"},
    # 4 段斌
    {"person_id": 4, "org_id": 2, "title": "治多县委副书记、副县长（援青）", "start_date": "2023", "end_date": "present", "rank": "副处级", "note": "2021-09起在北京丰台区工作，2025-08调任治多挂职"},
    {"person_id": 4, "org_id": 12, "title": "丰台区玉泉营街道党工委委员、办事处副主任", "start_date": "2021-09", "end_date": "2025", "rank": "正处级", "note": "北京丰台区玉泉营街道"},
    {"person_id": 4, "org_id": 14, "title": "北京航空航天大学交通科学与工程学院团委书记", "start_date": "2014", "end_date": "2021", "rank": "", "note": ""},
    # 5 刘俊
    {"person_id": 5, "org_id": 2, "title": "治多县委副书记、副县长（援青）", "start_date": "2023", "end_date": "present", "rank": "副处级", "note": "2025-08起"},
    {"person_id": 5, "org_id": 15, "title": "教育部职成司职业院校德育工作处（副处长/处长）", "start_date": "", "end_date": "2023", "rank": "副司局级", "note": "历任教育部职业教育与成人教育司职业院校德育工作处副处长、处长"},
    {"person_id": 5, "org_id": 13, "title": "北京理工大学工会干部", "start_date": "2004", "end_date": "", "rank": "", "note": ""},
    # 6 任喜春
    {"person_id": 6, "org_id": 1, "title": "治多县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 7 公却才旺
    {"person_id": 7, "org_id": 19, "title": "治多县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 8 刘挺
    {"person_id": 8, "org_id": 20, "title": "治多县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 9 赫发春
    {"person_id": 9, "org_id": 2, "title": "治多县委常委、副县长人选", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": "2026-07任前公示拟任"},
    # 10 五一
    {"person_id": 10, "org_id": 2, "title": "治多县人民政府副县长", "start_date": "2023-05", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 18, "title": "治多县索加乡党委书记", "start_date": "2021-04", "end_date": "2023", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 16, "title": "治多县总工会常务副主席", "start_date": "", "end_date": "2021", "rank": "", "note": ""},
    {"person_id": 10, "org_id": 17, "title": "治多县法院法警队队长/县委政法委综治办主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 11 昂文扎西
    {"person_id": 11, "org_id": 2, "title": "治多县人民政府副县长（原县政协副主席）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 12 陈鸿雁
    {"person_id": 12, "org_id": 2, "title": "治多县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 13 才仁旺加
    {"person_id": 13, "org_id": 2, "title": "治多县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 14 吴海勇
    {"person_id": 14, "org_id": 2, "title": "治多县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 15 张华
    {"person_id": 15, "org_id": 2, "title": "治多县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 16 白项欠
    {"person_id": 16, "org_id": 2, "title": "治多县人民政府副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2022年度见诸报端"},
    # 17 荣伟
    {"person_id": 17, "org_id": 2, "title": "治多县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2023年度报道"},
    # 18 文雅
    {"person_id": 18, "org_id": 3, "title": "治多县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2025-02作人大工作报告"},
    # 19 刘洪祥
    {"person_id": 19, "org_id": 3, "title": "治多县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 20 刘文骥
    {"person_id": 20, "org_id": 6, "title": "治多县人民法院代理院长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2025-02代理院长"},
    # 21 梅杭秀
    {"person_id": 21, "org_id": 7, "title": "治多县人民检察院检察长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2025-02作检院工作报告"},
    # 22 索昂尼保
    {"person_id": 22, "org_id": 5, "title": "治多县纪委副书记、监委副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 23 马兰
    {"person_id": 23, "org_id": 20, "title": "治多县委组织部部长（前任）", "start_date": "", "end_date": "", "rank": "副处级", "note": "退休干部工作报道线索"},
    # 24 伊拉
    {"person_id": 24, "org_id": 2, "title": "治多县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2022年度报道"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "池永杰（县委书记）与马小鹏（代县长）为治多县现任党政主要领导，同一班子共事", "overlap_org": "治多县", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "普措格来为池永杰任内的县长搭档，后离任由马小鹏接任县长", "overlap_org": "治多县", "overlap_period": "2022-2026"},
    {"person_a": 3, "person_b": 1, "type": "上下级", "context": "普措格来任县长期间向上对县委书记池永杰", "overlap_org": "治多县", "overlap_period": "2022-2025"},
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor", "context": "普措格来卸任县长由马小鹏接任（代）", "overlap_org": "治多县", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "县委书记与县委常委、政法委书记公却才旺同为县委班子", "overlap_org": "治多县", "overlap_period": "2022至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "县委书记与县委常委、组织部部长刘挺（组织部归口县委）", "overlap_org": "治多县", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "代县长马小鹏与县委常委、副县长人选赫发春（县政府班子）", "overlap_org": "治多县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "代县长与副县长陈鸿雁同属县政府班子", "overlap_org": "治多县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "代县长与副县长才仁旺加同属县政府班子", "overlap_org": "治多县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "代县长与副县长吴海勇同属县政府班子", "overlap_org": "治多县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "代县长与副县长五一（养老调研同行）", "overlap_org": "治多县人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 22, "type": "上下级", "context": "县委书记与县纪委书记/监委副主任索昂尼保（纪委监察）", "overlap_org": "治多县纪委", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "援青梯子", "context": "段斌、刘俊同属北京对口支援/挂职副县，同期抵治多（2025-08）", "overlap_org": "治多县人民政府", "overlap_period": "2025至今"},
    {"person_a": 4, "person_b": 1, "type": "上下级", "context": "挂职副书记、副县长同驻县委书记", "overlap_org": "治多县", "overlap_period": "2025至今"},
    {"person_a": 5, "person_b": 1, "type": "上下级", "context": "挂职副书记、副县长同驻县委书记", "overlap_org": "治多县", "overlap_period": "2025至今"},
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor", "context": "普措格来任县长时段段斌同时挂职副县长（共事）", "overlap_org": "治多县人民政府", "overlap_period": "2023-2025"},
    {"person_a": 18, "person_b": 1, "type": "上下级", "context": "人大常委会主任与县委书记（党政分工）", "overlap_org": "治多县人大", "overlap_period": ""},
    {"person_a": 20, "person_b": 21, "type": "政法体制内同源", "context": "法检两院为首长（刘文骥、梅杭秀）同属治多政法体制", "overlap_org": "治多县", "overlap_period": ""},
    {"person_a": 24, "person_b": 17, "type": "predecessor_successor", "context": "常务副县长由伊拉（2022）转荣伟（2023），任职更迭", "overlap_org": "治多县人民政府", "overlap_period": "2022-2023"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "代县长马小鹏与挂职县委副书记、副县长段斌（县政府班子）", "overlap_org": "治多县人民政府", "overlap_period": "2026"},
]

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Wrote DB: {DB_PATH}")
    print(f"Wrote GEXF: {GEXF_PATH}")
    print(f"Stats: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")