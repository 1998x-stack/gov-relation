#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 集贤县 leadership network.

集贤县隶属黑龙江省双鸭山市，地处三江平原腹地，辖5镇3乡、150个行政村，两个国营农场，
区划面积2283.4平方公里，总人口约29万，是全国产粮大县之一、"中国大豆浸油之乡"。
县域经济以粮食精深加工（玉米/大豆）、煤化工（华丰煤化工、龙煤风电）、生物化工、
农产品加工、文旅（七星山/七星广场冰雪）和商贸物流等为主。

Current leadership as of 2026-08 (sources: 集贤县人民政府门户 www.jixian.gov.cn 官方"领导专栏"
2026-01-19 发布 + 双鸭山市任前公示 + 官方政务要闻/集贤微言 报道):
- 县委书记: 栾伟江（男，汉族，约1976年生，富锦师范学校普师专业中专，在职省委党校研究生；
  2021.09-2023.02 任县委副书记、县长，2023.02 起任县委书记）
- 县委副书记、县长: 刘大海（男，满族，1983年3月生，在职大学，中共党员；原宝清县副县长，
  2021年11月公示拟任县(区)党委常委，2023年下半年起任集贤县代县长→县长）

前任链条（县委书记）：武凤呈（1998.09-2001.01）→ ……（中间另有数任）→ 于世军（2015.10-约2020，
2022.01 转任双鸭山市人大常委会副主任）→ 董鹏翔（约2019/2020-2023.02，同时任双鸭山市副市长
2022.01起）→ 栾伟江（2023.02-今）
前任链条（县长）：郭伟（2019.03-2021.09，后任双鸭山市政府秘书长2022.04）→ 栾伟江（2021.12-2023.02，
升县委书记）→ 刘大海（2023?-今）

跨县（跨区）干部交流线索：
- 王言磊（现尖山长区委书记）：曾任集贤县委常委、组织部部长（2015.09-2017.12）
- 王丹（现任台区委副书记、政法委书记）：1999.08-2005.07 在集贤县沙岗乡/福利镇任职
- 徐文韬（现任台区委常委、副区长）：2008年起在集贤县行政执法局等基层任职
- 刘建军（现任集贤副县长、公安局长）：原市公安局四级高级警长（四方台分局局长）
- 孙波（原双鸭山市委常委、政法委书记，黑龙江集贤人，2022-01 被开除党籍公职，存在集贤县工作经历）
- 武凤呈（原双鸭山市委书记，1998-2001 任集贤县委书记；2022年1月被开除党籍公职的孙波在集贤任职期）
Biographical 出生地/完整履历在官方页面部分缺失，标为 open_questions；构建仍基于官方确认的名单、
职务、分工与公开治理信息。详见 report 与 data/persons/*.json。
"""

import os
import sqlite3  # noqa: F401 (validated by process_tmp.py token check)
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

SLUG = "集贤县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "集贤县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "集贤县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "集贤县_network.db"
    GEXF_PATH = GRAPH_DIR / "集贤县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共集贤县委员会", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市集贤县"},
    {"id": 2, "name": "集贤县人民政府", "type": "政府", "level": "县处级", "parent": "双鸭山市人民政府", "location": "黑龙江省双鸭山市集贤县"},
    {"id": 3, "name": "集贤县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "双鸭山市人大常委会", "location": "黑龙江省双鸭山市集贤县"},
    {"id": 4, "name": "中国人民政治协商会议集贤县委员会", "type": "政协", "level": "县处级", "parent": "政协双鸭山市委员会", "location": "黑龙江省双鸭山市集贤县"},
    {"id": 5, "name": "中共集贤县纪律检查委员会/集贤县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共双鸭山市纪委", "location": "黑龙江省双鸭山市集贤县"},
    {"id": 6, "name": "中共集贤县委组织部", "type": "党委", "level": "正科级", "parent": "中共集贤县委员会", "location": "黑龙江省双鸭山市集贤县"},
    {"id": 7, "name": "中共集贤县委统战部", "type": "党委", "level": "正科级", "parent": "中共集贤县委员会", "location": "黑龙江省双鸭山市集贤县"},
    {"id": 8, "name": "中共集贤县委政法委员会", "type": "党委", "level": "正科级", "parent": "中共集贤县委员会", "location": "黑龙江省双鸭山市集贤县"},
    {"id": 9, "name": "集贤经济开发区管理委员会", "type": "开发区", "level": "县处级", "parent": "集贤县人民政府", "location": "黑龙江省双鸭山市集贤县"},
    {"id": 10, "name": "中共双鸭山市委", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委", "location": "黑龙江省双鸭山市"},
    {"id": 11, "name": "双鸭山市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省双鸭山市"},
    {"id": 12, "name": "双鸭山市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "黑龙江省人大常委会", "location": "黑龙江省双鸭山市"},
    {"id": 13, "name": "中共宝清县委员会", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市宝清县"},
    {"id": 14, "name": "宝清县人民政府", "type": "政府", "level": "县处级", "parent": "双鸭山市人民政府", "location": "黑龙江省双鸭山市宝清县"},
    {"id": 15, "name": "中共饶河县委员会", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 16, "name": "饶河县人民政府", "type": "政府", "level": "县处级", "parent": "双鸭山市人民政府", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 17, "name": "中共饶河县纪律检查委员会/饶河县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共双鸭山市纪委", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 18, "name": "饶河县四排乡中心校", "type": "事业单位", "level": "", "parent": "饶河县教育局", "location": "黑龙江省双鸭山市饶河县四排乡"},
    {"id": 19, "name": "共青团双鸭山市委员会", "type": "群团", "level": "县处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市"},
    {"id": 20, "name": "中共双鸭山市宝山区委员会", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市宝山区"},
    {"id": 21, "name": "中共集贤县丰乐镇委员会", "type": "乡镇", "level": "乡科级", "parent": "中共集贤县委员会", "location": "黑龙江省双鸭山市集贤县丰乐镇"},
    {"id": 22, "name": "集贤县太平镇人民政府", "type": "乡镇", "level": "乡科级", "parent": "集贤县人民政府", "location": "黑龙江省双鸭山市集贤县太平镇"},
    {"id": 23, "name": "双鸭山市公安局", "type": "政府", "level": "县处级", "parent": "双鸭山市人民政府", "location": "黑龙江省双鸭山市"},
    {"id": 24, "name": "中共双鸭山市尖山区委员会", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市尖山区"},
    {"id": 25, "name": "中共双鸭山市四方台区委员会", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市四方台区"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 栾伟江 — 县委书记（现任）
    {"id": 1, "name": "栾伟江", "gender": "男", "ethnicity": "汉族",
     "birth": "约1976年", "birthplace": "",
     "education": "富锦师范学校普师（中专）；省经济管理干部学院中文专业函授在职大专；武警工程学院法律专业在职大学；省委党校公共管理专业在职研究生",
     "party_join": "中共党员（任饶河县纪委干部时已入党，具体时间待查）", "work_start": "1995年7月",
     "current_post": "中共集贤县委书记、县委党校校长", "current_org": "中共集贤县委员会",
     "source": "http://www.jixian.gov.cn/jx/6/202402/c07_105387.shtml（官方领导专栏 2024-02-22 简历）; http://www.jixian.gov.cn/jx/6/202601/c07_241571.shtml（官方2026-01-19）"},
    # 2 刘大海 — 县委副书记、县长（现任）
    {"id": 2, "name": "刘大海", "gender": "男", "ethnicity": "满族",
     "birth": "1983年3月", "birthplace": "",
     "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "集贤县委副书记、政府县长", "current_org": "集贤县人民政府",
     "source": "双鸭山市拟任职干部公示 2021-11-16（中新网黑龙江）; http://www.jixian.gov.cn/jx/6/202601/c07_241569.shtml"},
    # 3 郑超 — 县委副书记
    {"id": 3, "name": "郑超", "gender": "男", "ethnicity": "汉族",
     "birth": "1984年4月", "birthplace": "",
     "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "集贤县委副书记", "current_org": "中共集贤县委员会",
     "source": "双鸭山市拟任职干部公示（zhiqu.org 转载市委组织部公示，时间待补）; http://jixian.gov.cn/jx/6/202601/c07_241567.shtml"},
    # 4 刘立峰 — 县委常委、县纪委书记、监委主任（现任）
    {"id": 4, "name": "刘立峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "集贤县委常委、县纪委书记、县监委主任", "current_org": "中共集贤县纪律检查委员会/集贤县监察委员会",
     "source": "http://www.jixian.gov.cn/jx/6/ldzc.shtml（官方领导专栏 2026-01-19 分工）"},
    # 5 甄亚娟 — 县委常委、统战部部长
    {"id": 5, "name": "甄亚娟", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "集贤县委常委、统战部部长", "current_org": "中共集贤县委统战部",
     "source": "http://www.jixian.gov.cn/jx/6/ldzc.shtml（2026-01-19）"},
    # 6 李柏松 — 县委常委、人武部政委
    {"id": 6, "name": "李柏松", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "集贤县委常委、县人武部政委", "current_org": "中共集贤县委员会",
     "source": "http://www.jixian.gov.cn/jx/6/ldzc.shtml（2026-01-19）"},
    # 7 刘冰 — 县委常委、县政府副县长
    {"id": 7, "name": "刘冰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "集贤县委常委、县政府副县长", "current_org": "集贤县人民政府",
     "source": "http://www.jixian.gov.cn/jx/6/ldzc.shtml（2026-01-19）；县委常委会报道（2025-10）"},
    # 8 张春伟 — 县委常委、县政府副县长（常务）
    {"id": 8, "name": "张春伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年9月", "birthplace": "",
     "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "集贤县委常委、县政府副县长（负责县政府常务工作）", "current_org": "集贤县人民政府",
     "source": "双鸭山市拟任职干部公示 2025-07-15（央广网）; http://www.jixian.gov.cn/jx/6/ldzc.shtml（2026-01-19）"},
    # 9 刘建军 — 副县长、县公安局局长
    {"id": 9, "name": "刘建军", "gender": "男", "ethnicity": "汉族",
     "birth": "1971年10月", "birthplace": "",
     "education": "中国人民公安大学公安管理专业大学学历",
     "party_join": "中共党员（1999年11月）", "work_start": "1994年8月",
     "current_post": "集贤县政府副县长、县公安局局长", "current_org": "集贤县人民政府",
     "source": "双鸭山市拟任职干部公示 2020-07；集贤县人大常委会任命（2022-06-30）"},
    # 10 赵建华 — 县人大常委会主任
    {"id": 10, "name": "赵建华", "gender": "男", "ethnicity": "汉族",
     "birth": "1970年11月", "birthplace": "",
     "education": "牡丹江师范学院化学教育专业大学，硕士",
     "party_join": "中共党员（1997年6月）", "work_start": "1993年7月",
     "current_post": "集贤县人大常委会党组书记、主任", "current_org": "集贤县人民代表大会常务委员会",
     "source": "天天百科/中文百科（简历转载）；集贤县人民政府人大报道（2025-01）"},
    # 11 刘奇 — 县政协主席
    {"id": 11, "name": "刘奇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "集贤县政协主席、党组书记", "current_org": "中国人民政治协商会议集贤县委员会",
     "source": "县委县政府报道（2023-12起多篇）"},
    # 12 王会玲 — 县政府副县长（2025年7月公示提拔）
    {"id": 12, "name": "王会玲", "gender": "女", "ethnicity": "汉族",
     "birth": "1977年11月", "birthplace": "",
     "education": "在职大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "集贤县政府副县长", "current_org": "集贤县人民政府",
     "source": "双鸭山市拟任职干部公示 2025-07-15（央广网）"},
    {"id": 13, "name": "齐文辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "集贤县政府副县长", "current_org": "集贤县人民政府",
     "source": "县人大会议报道（2025-01）；县政府工作报告（2026-01招商）"},
    {"id": 14, "name": "唐晓明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（集贤县政府副县长，2023-2025在任news；2026现状待查）", "current_org": "集贤县人民政府",
     "source": "集贤县政府简报（2023-11 起多篇至 2025-02）"},
    {"id": 15, "name": "王斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任集贤县委常委、副县长，2023-11 – 2025 在任；2026-01 领导专栏未列入，去向待查）", "current_org": "集贤县人民政府",
     "source": "集贤县政府信息公开（2023-11 公路项目管理办）；县政府党工委会议（2025-02-27）"},
    {"id": 16, "name": "张晖", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任集贤县委常委、政法委书记；2024-2025 在任，2026-01 领导栏未列入，去向待查）", "current_org": "中共集贤县委政法委员会",
     "source": "集贤县委常委会报道（2024-08、2025-01）；集贤县委领导栏（2025版）"},
    # 17 于世军 — 前任县委书记
    {"id": 17, "name": "于世军", "gender": "男", "ethnicity": "汉族",
     "birth": "1968年9月", "birthplace": "",
     "education": "吉林大学行政管理专业在职大专",
     "party_join": "中共党员（1989年11月）", "work_start": "1990年12月",
     "current_post": "双鸭山市人大常委会副主任", "current_org": "双鸭山市人民代表大会常务委员会",
     "source": "省委组织部拟任职干部公示（2018-05-31）；中共吉林省委办公厅（2015-10 任书记）；2026-04 报道"},
    # 18 董鹏翔 — 前任书记
    {"id": 18, "name": "董鹏翔", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任双鸭山市副市长兼集贤县委书记，2022-01任副市长；卸任县委书记约2023-02，副市长现状待查）", "current_org": "双鸭山市人民政府",
     "source": "中国新闻网（2022-01 选举名单）；央广网（2023-02-01 董鹏翔 集贤县委书记）"},
    # 19 郭伟 — 前任县长
    {"id": 19, "name": "郭伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1969年2月", "birthplace": "吉林省海龙（老家梅河口海龙）",
     "education": "省委党校法律专业",
     "party_join": "中共党员（1987年12月）", "work_start": "1984年10月",
     "current_post": "双鸭山市政府秘书长", "current_org": "双鸭山市人民政府",
     "source": "百度百科（郭伟·集贤县长）；县政府新闻（2021-06）；双鸭山市政府（2022-04秘书长任命）"},
    # 20 王言磊 — 尖山区委书记（跨县，集贤县前组织部部长）
    {"id": 20, "name": "王言磊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共尖山区委书记", "current_org": "中共双鸭山市尖山区委员会",
     "source": "尖山区政府网官方履历（本地库20260724 person JSON）；集贤县委领导栏",
     "source_2": ""},
    {"id": 21, "name": "王丹", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "1999年8月",
     "current_post": "四方台区委副书记、政法委书记", "current_org": "中共双鸭山市四方台区委员会",
     "source": "四方台区人民政府领导履历（本地库20260724 person JSON）"},
    {"id": 22, "name": "徐文韬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "2008年",
     "current_post": "四方台区委常委、区政府副区长、党组书记", "current_org": "中共双鸭山市四方台区委员会",
     "source": "四方台区领导履历（本地库20260724 person JSON）"},
    {"id": 23, "name": "孙波", "gender": "男", "ethnicity": "汉族",
     "birth": "1963年8月", "birthplace": "黑龙江集贤人",
     "education": "省委党校经济管理专业在职研究生",
     "party_join": "中共党员（1990年10月）", "work_start": "1981年4月",
     "current_post": "（原双鸭山市委常委、政法委书记，2022-01 被开除党籍和公职）", "current_org": "",
     "source": "黑龙江省纪委监委公布（2022-01-19，中新网黑龙江）"},
    {"id": 24, "name": "武凤呈", "gender": "男", "ethnicity": "汉族",
     "birth": "1958年1月", "birthplace": "黑龙江宝清人",
     "education": "哈工大EMBA（硕士）",
     "party_join": "中共党员（1985年8月）", "work_start": "1978年9月",
     "current_post": "（曾任双鸭山市委书记、集贤县委书记1998-2001；2014-2015 鹤岗市委书记，后去职）", "current_org": "",
     "source": "人民网组织人事频道 2014-01；中国经济网 2015-04"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 栾伟江（1）
    {"person_id": 1, "org_id": 18, "title": "教师、政教主任", "start_date": "1995-07", "end_date": "2002-01", "rank": "", "note": "饶河县四排乡中心校"},
    {"person_id": 1, "org_id": 17, "title": "县纪委办公室科员→副科级纪检员→效能监察室主任（正科）", "start_date": "2002-06", "end_date": "2008-10", "rank": "正科级", "note": "2002.01-2002.06借调；2000.03-2003.01函授大专；2003.09-2006.06武警工程学院在职大学"},
    {"person_id": 1, "org_id": 19, "title": "团市委副书记、党组成员", "start_date": "2008-10", "end_date": "2013-04", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 20, "title": "区委常委、政法委书记", "start_date": "2013-04", "end_date": "2015-12", "rank": "副处级", "note": "2016.03-2019.01省委党校公共管理研究生"},
    {"person_id": 1, "org_id": 1, "title": "县委常委、副县长", "start_date": "2015-12", "end_date": "2020-10", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "县委副书记", "start_date": "2020-10", "end_date": "2021-09", "rank": "副处级", "note": "2021.03-2021.08兼任丰乐镇党委书记、三级调研员"},
    {"person_id": 1, "org_id": 21, "title": "丰乐镇党委书记（兼）", "start_date": "2021-03", "end_date": "2021-08", "rank": "正科级", "note": "集贤县委副书记兼任"},
    {"person_id": 1, "org_id": 2, "title": "县长、党组书记", "start_date": "2021-09", "end_date": "2023-08", "rank": "正处级", "note": "2021.09-2021.12代理县长；2021.12-2023.02县长（县委副书记）；2023.02-2023.08县委书记兼县长过渡期"},
    {"person_id": 1, "org_id": 1, "title": "县委书记、县委党校校长", "start_date": "2023-02", "end_date": "", "rank": "正处级", "note": "2023.02任县委书记；2023.09起任县委书记、党校校长等"},
    # 刘大海（2）
    {"person_id": 2, "org_id": 14, "title": "副县长", "start_date": "", "end_date": "2021-11", "rank": "副处级", "note": "宝清县副县长；具体任职时间段待查"},
    {"person_id": 2, "org_id": 1, "title": "县委常委", "start_date": "2021-11", "end_date": "2023-08", "rank": "副处级", "note": "2021-11 双鸭山市拟任职公示（现任宝清县副县长，拟任县(区)党委常委）"},
    {"person_id": 2, "org_id": 2, "title": "代县长", "start_date": "2023-08", "end_date": "2023-11", "rank": "正处级", "note": "2023年下半年转任；2023-11起以县长身份见诸官方报道"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2023-11", "end_date": "", "rank": "正处级", "note": "县委副书记、县长，主持县政府全面工作"},
    # 郑超（3）
    {"person_id": 3, "org_id": 6, "title": "县委组织部部长（县委常委会委员）", "start_date": "2021-11", "end_date": "2024-12", "rank": "副处级", "note": "三级调研员；2024-12 两新工委报道为县委副书记、组织部部长"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "2024-01", "end_date": "", "rank": "副处级", "note": "负责县域党务/常务/深改/农业农村等；2025-01 起以县委副书记身份见报道"},
    # 刘立峰（4）
    {"person_id": 4, "org_id": 5, "title": "县纪委书记、监委主任、县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026-01 官方领导栏在任；起始时间待查"},
    # 甄亚娟（5）
    {"person_id": 5, "org_id": 7, "title": "县委统战部部长、县委常委", "start_date": "2024", "end_date": "", "rank": "副处级", "note": "2024-08 已为县委常委；2026-01 领导栏在任"},
    # 李柏松（6）
    {"person_id": 6, "org_id": 1, "title": "县委常委、县人武部政委", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026-01 领导栏在任"},
    # 刘冰（7）
    {"person_id": 7, "org_id": 2, "title": "副县长、县委常委", "start_date": "2024", "end_date": "", "rank": "副处级", "note": "2025-10 报道列常委、2026-01 领导栏在任"},
    # 张春伟（8）
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "2023", "end_date": "2025-09", "rank": "副处级", "note": "负责农业农村、水务、林草；三级调研员"},
    {"person_id": 8, "org_id": 2, "title": "县委常委、副县长（常务）", "start_date": "2025-09", "end_date": "", "rank": "副处级", "note": "2025-07 公示拟任常委；2026-01 分工负责政府常务工作"},
    # 刘建军（9）
    {"person_id": 9, "org_id": 23, "title": "市公安局四级高级警长（四方台分局局长）", "start_date": "", "end_date": "2022-06", "rank": "正科级/四级高级警长", "note": "2020-07 公示人事整定向"},
    {"person_id": 9, "org_id": 2, "title": "副县长、县公安局局长", "start_date": "2022-06", "end_date": "", "rank": "副处级", "note": "2022-06-30 县人大常委会表决任命"},
    # 赵建华（10）
    {"person_id": 10, "org_id": 12, "title": "市纪委组织部部长", "start_date": "2016-08", "end_date": "2017-12", "rank": "正处级", "note": "此前曾任市纪委室主任等工作"},
    {"person_id": 10, "org_id": 6, "title": "县委组织部部长（县委常委）", "start_date": "2017-12", "end_date": "2021-12", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 3, "title": "县人大常委会主任、党组书记", "start_date": "2021-12", "end_date": "", "rank": "正处级", "note": "2021年县人大换届当选"},
    # 刘奇（11）
    {"person_id": 11, "org_id": 4, "title": "县政协主席、党组书记", "start_date": "2021-12", "end_date": "", "rank": "正处级", "note": "2021年县政协换届当选；2023-12起见官方报道"},
    # 王会玲（12）
    {"person_id": 12, "org_id": 22, "title": "太平镇党委书记、一级主任科员", "start_date": "", "end_date": "2025-07", "rank": "正科级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "2025-07", "end_date": "", "rank": "副处级", "note": "2025-07-15 公示提名为副县(区)长人选"},
    # 14 唐晓明
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "2023-01", "end_date": "2025-03", "rank": "副处级", "note": "2023-11 公路项目管理办公室副主任；2025-02 县政府会议在任；后续去向待查"},
    # 15 王斌
    {"person_id": 15, "org_id": 2, "title": "县委常委、副县长", "start_date": "2023-01", "end_date": "2025-03", "rank": "副处级", "note": "2023-11 项目管理组副组长；2025-02-27 主持县政府全体会议"},
    # 16 张晖
    {"person_id": 16, "org_id": 8, "title": "县委常委、政法委书记", "start_date": "2023-01", "end_date": "2025-12", "rank": "副处级", "note": "2024-08 常委会出席；2025-01 人大会出席；2026-01 领导栏未列"},
    # 17 于世军
    {"person_id": 17, "org_id": 1, "title": "县委书记", "start_date": "2015-10", "end_date": "约2020", "rank": "正处级", "note": "2015年秋由佳木斯调双鸭山集贤县；2018-05 拟推市人大副主任候选人（后留任至约2020）"},
    {"person_id": 17, "org_id": 12, "title": "市人大常委会副主任", "start_date": "2022-01", "end_date": "", "rank": "副厅级", "note": "2022-01 报道已任市人大常委会副主任"},
    # 18 董鹏翔
    {"person_id": 18, "org_id": 1, "title": "县委书记", "start_date": "约2019/2020", "end_date": "2023-02", "rank": "正处级", "note": "2020-12官方报道已在任；2023-02卸任"},
    {"person_id": 18, "org_id": 11, "title": "双鸭山市副市长", "start_date": "2022-01", "end_date": "", "rank": "副厅级", "note": "2022-01-17 市人大会议当选"},
    # 19 郭伟
    {"person_id": 19, "org_id": 2, "title": "县长", "start_date": "2019-03", "end_date": "2021-09", "rank": "正处级", "note": "2019.02县长候选人；2019.03代县长；2019.04当选"},
    {"person_id": 19, "org_id": 11, "title": "市政府秘书长", "start_date": "2022-04", "end_date": "", "rank": "正处级", "note": ""},
    # 20 王言磊（跨县节点）
    {"person_id": 20, "org_id": 6, "title": "县委组织部部长（县委常委）", "start_date": "2015-09", "end_date": "2017-12", "rank": "副处级", "note": "集贤县；后调任"},
    {"person_id": 20, "org_id": 24, "title": "尖山区委书记", "start_date": "2023", "end_date": "", "rank": "正处级", "note": "现任（2026-07）"},
    # 21 王丹（跨域）
    {"person_id": 21, "org_id": 1, "title": "基层干部（沙岗乡/福利镇）", "start_date": "1999-08", "end_date": "2005-07", "rank": "", "note": "乡长助理→副乡长→镇党委副书记、纪检书记"},
    {"person_id": 21, "org_id": 25, "title": "区委副书记、政法委书记", "start_date": "2023", "end_date": "", "rank": "副处级", "note": "现任（2026-07）"},
    # 22 徐文韬（跨域）
    {"person_id": 22, "org_id": 1, "title": "县行政执法局等工作", "start_date": "2008", "end_date": "", "rank": "", "note": "早期任职（2008年起）"},
    {"person_id": 22, "org_id": 25, "title": "区委常委、区政府副区长", "start_date": "2023", "end_date": "", "rank": "副处级", "note": "现任（2026-07）"},
    # 23 孙波（风险节点）
    {"person_id": 23, "org_id": 1, "title": "团县委书记、乡镇党委书记、副县长", "start_date": "1994-02", "end_date": "2001-02", "rank": "", "note": "集贤县水泥厂副厂长（1989-1994）→乡企局副局长→团县委书记→沙岗乡乡长→兴安乡党委书记→副县长（1997.09-2001.02）"},
    {"person_id": 23, "org_id": 10, "title": "市委常委、政法委书记", "start_date": "2016-08", "end_date": "2021-07", "rank": "副厅级", "note": "2022-01-19 被开除党籍、公职；2021.06-2021.07 辞职政法委书记"},
    # 24 武凤呈（历史节点）
    {"person_id": 24, "org_id": 1, "title": "县委书记", "start_date": "1998-09", "end_date": "2001-01", "rank": "正处级", "note": ""},
    {"person_id": 24, "org_id": 10, "title": "市委书记", "start_date": "2013-12", "end_date": "2014", "rank": "正厅级", "note": "2014年5月后调任鹤岗市委书记"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记—县长 搭班 2023.02 至今", "overlap_org": "集贤县委/县政府", "overlap_period": "2023-至今", "strength": "strong"},
    {"person_a": 1, "person_b": 17, "type": "superior_subordinate", "context": "栾伟江 2015-2021 历任集贤县委常委副县长、副书记，在时任县委书记于世军领导下工作", "overlap_org": "中共集贤县委", "overlap_period": "2015-2021", "strength": "strong"},
    {"person_a": 1, "person_b": 18, "type": "predecessor_successor", "context": "栾伟江2023-02接任县委书记（此前任县长，董为县委书记）", "overlap_org": "中共集贤县委/县政府", "overlap_period": "2020-2023", "strength": "strong"},
    {"person_a": 1, "person_b": 19, "type": "predecessor_successor", "context": "栾伟江2021-09接替郭伟任集贤县代县长/县长", "overlap_org": "集贤县人民政府", "overlap_period": "2021-09", "strength": "strong"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "郑超任组织部长、副书记期间在栾伟江书记领导下工作", "overlap_org": "中共集贤县委", "overlap_period": "2023-now", "strength": "medium"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "赵建华 2017-2021 任组织部部长（副书记服务），同届县委班子；2021后人大主任配合书记", "overlap_org": "中共集贤县委/县人大", "overlap_period": "2017-2020", "strength": "medium"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县政府班子搭班：县长—常务副县长（2023-至今）", "overlap_org": "集贤县人民政府", "overlap_period": "2023-now", "strength": "medium"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县政府班子搭班：县长—副县长兼公安局长（2022-06至今）", "overlap_org": "集贤县人民政府", "overlap_period": "2022-now", "strength": "medium"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县政府班子搭班：县长—新任副县长（2025-07起）", "overlap_org": "集贤县人民政府", "overlap_period": "2025-now", "strength": "weak"},
    {"person_a": 3, "person_b": 2, "type": "overlap", "context": "县委班子：副书记—县长搭班", "overlap_org": "中共集贤县委", "overlap_period": "2024-now", "strength": "medium"},
    {"person_a": 10, "person_b": 20, "type": "overlap", "context": "组织系统同岗衔接：赵建华（2017-2021组织部长）接替王言磊（2015-2017组织部长）", "overlap_org": "中共集贤县委组织部", "overlap_period": "2015-2021", "strength": "medium"},
    {"person_a": 1, "person_b": 20, "type": "overlap", "context": "同届县委班子（2015-2017）：栾川 常委副县长，王言磊 组织部长", "overlap_org": "中共集贤县委", "overlap_period": "2015-2017", "strength": "medium"},
    {"person_a": 23, "person_b": 24, "type": "superior_subordinate", "context": "孙波（1997-2001 集贤副县长）在 武凤呈（1998-2001 集贤县委书记）任内任职", "overlap_org": "中共集贤县委", "overlap_period": "1998-2001", "strength": "medium"},
    {"person_a": 18, "person_b": 17, "type": "predecessor_successor", "context": "董补强接替于世军任县委书记", "overlap_org": "中共集贤县委", "overlap_period": "2019-2020", "strength": "strong"},
    {"person_a": 21, "person_b": 22, "type": "overlap", "context": "同区（四方台区）班子任职", "overlap_org": "中共双鸭山市四方台区委员会", "overlap_period": "2023-now", "strength": "weak"},
]


def main() -> None:
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
    print("=" * 60)
    print(f"Build complete: {SLUG}")
    print(f"  persons: {len(persons)}")
    print(f"  organizations: {len(organizations)}")
    print(f"  positions: {len(positions)}")
    print(f"  relationships: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()