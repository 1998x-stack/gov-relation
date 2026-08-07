#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 吴起县, 延安市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_吴起县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - 吴起县人民政府官网 (www.wqx.gov.cn) — 本地要闻/公示公告/政府信息公开 多篇官方新闻
    确认现任县委书记张宏江、县委副书记·代县长闫晓妮、县委常委会班子（组织/宣传/统战/纪委/政法/人武部）、
    县政府领导班子（常务副职/8名副县）、县人大主任、县政协主席，及前任县委书记贺毅
  - www.wqx.gov.cn/zfxxgk/fdzdgknr/zfld/ 政府领导栏目 — 每名政府领导的个人简历页（官方、含出生/籍贯/学历/完整任职时间线）
  - 官方新闻时间线重建：贺毅(书记)→张宏江(县长→书记) 2026年交接；闫晓妮 2026-06-11 任代县长

Confidence notes:
  - 县委、政府、人大、政协主体均为官方新闻/官方简历确认（high）
  - 张宏江（现任县委书记）完整履历：县人大第二十六次会议（2026-06-11）确认其辞去县长并接任书记，
    但任吴起县长之前（2024年前）的公开履历未能在本轮获取，以 open_questions 记录，不臆造
  - 闫晓妮（代县长）：官方简历完整（延安市委组织部→团市委副书记→市直机关工委书记→安塞区委副书记、砖窑湾镇党委书记→吴起代县长）
  - 县委副书记乔栋、及部分乡镇/部门干部履历待查
  - 网络访问受限：Exa 限流、百度和360/Bing/Sogou 需验证码；全部结论基于吴起县政府官网页
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.abspath(os.path.join(BASE, "..", "..", "..")))

from gov_relation.runner import run_build

SLUG = "吴起县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ─── 县委主要领导 ───
    {
        "id": 1,
        "name": "张宏江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共吴起县委员会",
        "source": "吴起县政府官网新闻确认。2026-07 多篇'县委书记张宏江主持召开县委常委会/防汛会议'；2026-06-11县十八届人大常委会第二十六次会议接受其辞去县长职务接任县委书记；2026-05-20任县人武部党委第一书记；此前(至2026-04)任县委副书记、县长"
    },
    {
        "id": 2,
        "name": "闫晓妮",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980-12",
        "birthplace": "陕西蓝田",
        "education": "在职研究生、管理学学士",
        "party_join": "中共党员",
        "work_start": "2003-07",
        "current_post": "县委副书记、代县长",
        "current_org": "吴起县人民政府",
        "source": "吴起县政府官网政府领导页(官方简历)。2026-06-11县人大常委会第二十六次会议决定任命为副县长、代理县长；政府党组书记、代县长。简历：延安市委组织部→团市委副书记→市直机关工委书记→安塞区委副书记、砖窑湾镇党委书记"
    },
    {
        "id": 3,
        "name": "乔栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、党校校长",
        "current_org": "中共吴起县委员会",
        "source": "2026-04-15科级干部培训班'县委副书记、县委党校校长乔栋出席开班'；2026-04-01县委理论中心组'县委副书记乔栋'；履历待查"
    },
    # ─── 县委常委会 ───
    {
        "id": 4,
        "name": "张史奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-02",
        "birthplace": "陕西省洛川县",
        "education": "工商管理硕士研究生",
        "party_join": "中共党员",
        "work_year": "2000-07",
        "current_post": "县委常委、常务副县长",
        "current_org": "吴起县人民政府",
        "source": "吴起县政府官网政府领导页(官方简历)。洛川教师→洛川县委办→子长县委统战/宣传→延长县委组织→2024-01吴起县委常委、常务副县长"
    },
    {
        "id": 5,
        "name": "王崛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-11",
        "birthplace": "陕西绥德",
        "education": "本科(延安大学工商管理)",
        "party_join": "中共党员",
        "work_year": "2003-07",
        "current_post": "县委常委、副县长",
        "current_org": "吴起县人民政府",
        "source": "吴起县政府官网政府领导页(官方简历)。志丹县政府办→志丹县金融办主任→延安市委办副总值班室等→2024-01吴起县委常委、副县长"
    },
    {
        "id": 6,
        "name": "野根利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共吴起县委员会",
        "source": "2026-07-11防汛调度会'县委常委、宣传部部长野根利'；2026-07-10'两优一先'表彰大会列席常委；履历待查"
    },
    {
        "id": 7,
        "name": "赵晓杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共吴起县委员会",
        "source": "2026-07-10'两优一先'表彰大会'县委常委、组织部部长赵晓杰宣读表彰决定'；2026-06-16目标责任考核'县委组织部部长'；履历待查"
    },
    {
        "id": 8,
        "name": "何重达",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共吴起县纪律检查委员会",
        "source": "2026-06-16任前廉政法规考试'县委常委、纪委书记、监委主任何重达到场巡考'；履历待查"
    },
    {
        "id": 9,
        "name": "刘政",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共吴起县委政法委员会",
        "source": "2026-03-12县公安局2026年公安工作会议'县委常委、政法委书记刘政出席会议并讲话'；履历待查"
    },
    {
        "id": 10,
        "name": "王海博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共吴起县委员会",
        "source": "2026-07-28县人大常委会第二十八次会议'县委常委、统战部部长王海博'；履历待查"
    },
    {
        "id": 11,
        "name": "邢卫平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、人武部上校政治委员",
        "current_org": "吴起县人民武装部",
        "source": "2026-05-20县人武部党委第一书记任职大会'县委常委、人武部上校政治委员邢卫平主持会议'；军事干部交流"
    },
    # ─── 县政府班子 ───
    {
        "id": 12,
        "name": "杜晓莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974-09",
        "birthplace": "河南新乡",
        "education": "全日制中专、在职省委党校研究生",
        "party_join": "无党派",
        "work_year": "1993-07",
        "current_post": "副县长",
        "current_org": "吴起县人民政府",
        "source": "吴起县政府官网政府领导页(官方简历)。吴起县幼儿园教师→副园长→工商联副会长/主席→2019-07吴起副县长"
    },
    {
        "id": 13,
        "name": "荆永恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-02",
        "birthplace": "陕西省洛川县",
        "education": "大学本科、法学学士",
        "party_join": "中共党员",
        "work_year": "1993-07",
        "current_post": "副县长、公安局局长",
        "current_org": "吴起县人民政府",
        "source": "吴起县政府官网政府领导页(官方简历)。洛川公安系统→子长公安政委→宜川副县长/公安局长→2024-04吴起副县长、公安局长"
    },
    {
        "id": 14,
        "name": "齐敏仝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-08",
        "birthplace": "陕西吴起",
        "education": "全日制大学学历、文学学士、在职省委党校研究生",
        "party_join": "中共党员",
        "work_year": "2005-10",
        "current_post": "副县长",
        "current_org": "吴起县人民政府",
        "source": "吴起县政府官网政府领导页(官方简历)。延安市委通讯组→市委宣传部→2021-10吴起副县长"
    },
    {
        "id": 15,
        "name": "王文文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-10",
        "birthplace": "陕西子长",
        "education": "全日制大学、工学学士(环境工程)",
        "party_join": "中共党员",
        "work_year": "2003-07",
        "current_post": "副县长",
        "current_org": "吴起县人民政府",
        "source": "吴起县政府官网政府领导页(官方简历)。志丹县乡镇→延安市委组织部考核→2025-12吴起副县长"
    },
    {
        "id": 16,
        "name": "曹殿东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-12",
        "birthplace": "陕西志丹",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_year": "1998-08",
        "current_post": "副县长",
        "current_org": "吴起县人民政府",
        "source": "吴起县政府官网政府领导页(官方简历)。洛川师范→志丹乡镇教学→县委办→乡镇长/镇党委书记→志丹县政办/县政府办主任→2025-12吴起副县长"
    },
    {
        "id": 17,
        "name": "王智阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "吴起县人民政府",
        "source": "2026-07-28县人大常委会第二十八次会议'决定任命王智阳同志为吴起县人民政府副县长'（列席）"
    },
    {
        "id": 18,
        "name": "蔡德勤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-08",
        "birthplace": "陕西吴起",
        "education": "",
        "party_join": "中共党员",
        "work_year": "1989-10",
        "current_post": "政府党组成员、二级调研员",
        "current_org": "吴起县人民政府",
        "source": "吴起县政府官网政府领导页(官方简历)。吴起本土干部：乡镇文书→副乡长→乡镇书记→国资中心主任→住建规划局长……→政府党组成员、二级调研员"
    },
    # ─── 人大/政协 ───
    {
        "id": 19,
        "name": "王晓春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "吴起县人民代表大会常务委员会",
        "source": "2026-07-29县四套班子慰问'县人大常委会主任王晓春'；多次主持县人大常委会会议"
    },
    {
        "id": 20,
        "name": "梁丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议吴起县委员会",
        "source": "2026-07-28慰问'县政协主席梁丰'；2006-03政协十届五次会议主持；2026-07-17县委常委会(扩大)列席"
    },
    {
        "id": 21,
        "name": "齐乃珂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议吴起县委员会",
        "source": "2026-03政协十届五次会议主席台前排就座"
    },
    {
        "id": 22,
        "name": "蔡凤梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议吴起县委员会",
        "source": "2026-07-29县四套班子慰问名单；2026-03政协会议主席台"
    },
    {
        "id": 23,
        "name": "雷晓虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议吴起县委员会",
        "source": "2026-03政协十届五次会议'县政协副主席雷晓虎'"
    },
    # ─── 前任 ───
    {
        "id": 24,
        "name": "贺毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原县委书记、延安市政协副主席",
        "current_org": "中共吴起县委员会",
        "source": "2026-03/04官方新闻'市政协副主席、县委书记贺毅'；其县委书记职务由张宏江接任(2026-06人大确认张辞县长任书记)，去向为延安市政协副主席"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共吴起县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共延安市委员会",
        "location": "延安市吴起县"
    },
    {
        "id": 2,
        "name": "吴起县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "延安市人民政府",
        "location": "延安市吴起县"
    },
    {
        "id": 3,
        "name": "吴起县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "延安市人民代表大会常务委员会",
        "location": "延安市吴起县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议吴起县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协延安市委员会",
        "location": "延安市吴起县"
    },
    {
        "id": 5,
        "name": "中共吴起县纪律检查委员会/县监委",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共延安市纪律检查委员会",
        "location": "延安市吴起县"
    },
    {
        "id": 6,
        "name": "中共吴起县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共吴起县委员会",
        "location": "延安市吴起县"
    },
    {
        "id": 7,
        "name": "吴起县公安局",
        "type": "政府",
        "level": "正科级",
        "parent": "延安市公安局 / 吴起县人民政府",
        "location": "延安市吴起县"
    },
    {
        "id": 8,
        "name": "吴起县人民武装部",
        "type": "其他",
        "level": "县处级",
        "parent": "延安军分区",
        "location": "延安市吴起县"
    },
]

positions_data = [
    # 县委
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2026", "end_date": "present", "rank": "县处级", "note": "2026-06-11辞去县长后接任书记；2026-05-20任县人武部党委第一书记"},
    {"person_id": 24, "org_id": 1, "title": "县委书记(离任)", "start_date": "unknown", "end_date": "2026", "rank": "县处级", "note": "贺毅：市政协副主席兼吴起县委书记；后张宏江接任"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记、党校校长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2026", "end_date": "present", "rank": "县处级", "note": "兼代县长"},
    {"person_id": 6, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 11, "org_id": 8, "title": "人民武装部政委", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": "上校政治委员"},
    {"person_id": 9, "org_id": 6, "title": "县委常委、政法委书记", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    # 政府
    {"person_id": 1, "org_id": 2, "title": "县长(前任)", "start_date": "unknown", "end_date": "2026-06", "rank": "县处级", "note": "2026-04仍任县委副书记、县长；2026-06-11辞去"},
    {"person_id": 2, "org_id": 2, "title": "代县长", "start_date": "2026-06", "end_date": "present", "rank": "县处级", "note": "政府党组书记；2026-06-11县人大常委会任命"},
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start_date": "2024-01", "end_date": "present", "rank": "副县处级", "note": "县委常委"},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "2024-01", "end_date": "present", "rank": "副县处级", "note": "县委常委"},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "2019-07", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长、公安局长", "start_date": "2024-04", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 13, "org_id": 7, "title": "公安局局长", "start_date": "2024-04", "end_date": "present", "rank": "副县处级", "note": "副县长兼公安局长"},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "2024-10", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "2025-12", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副县长", "start_date": "2025-12", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "2026-07", "end_date": "present", "rank": "副县处级", "note": "2026-07-28任命"},
    {"person_id": 18, "org_id": 2, "title": "政府党组成员、二级调研员", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    # 纪委
    {"person_id": 8, "org_id": 5, "title": "县委常委、纪委书记、监委主任", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    # 人大/政协
    {"person_id": 19, "org_id": 3, "title": "县人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "县政协主席", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "县政协副主席", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 22, "org_id": 4, "title": "县政协副主席", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 23, "org_id": 4, "title": "县政协副主席", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
]

relationships_data = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记张宏江——县委副书记、代县长闫晓妮，党政主要领导搭档，同场主持/出席县委常委会、县四套班子会议等", "overlap_org": "中共吴起县委/县政府", "overlap_period": "2026-present"},
    {"person_a": 1, "person_b": 24, "type": "前任/继任", "context": "贺毅离任县委书记，张宏江接任县委书记（张宏江原任县长）；两人先后任吴起县长/书记", "overlap_org": "中共吴起县委/县政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 1, "type": "继任(前任县长→继任书记)", "context": "张宏江由县长转任县委书记后辞去县长，闫晓妮接任代县长", "overlap_org": "吴起县人民政府", "overlap_period": "2026-06"},
    # 书记与班子成员
    {"person_a": 1, "person_b": 3, "type": "班子", "context": "书记张宏江——副书记乔栋同场主持/列席县委常委会与理论研读会", "overlap_org": "中共吴起县委", "overlap_period": "2026-present"},
    {"person_a": 1, "person_b": 7, "type": "班子", "context": "县委组织部赵晓杰在表彰会宣读县委决定并要求落实书记部署（组织系统汇报）", "overlap_org": "中共吴起县委", "overlap_period": "2026-present"},
    {"person_a": 1, "person_b": 8, "type": "班子", "context": "县委书记——纪委书记何重达（党风廉政、廉政考试）", "overlap_org": "中共吴起县委", "overlap_period": "2026-present"},
    {"person_a": 1, "person_b": 9, "type": "班子", "context": "县委书记——政法委书记刘政（政法稳定、安全生产）", "overlap_org": "中共吴起县委", "overlap_period": "2026-present"},
    {"person_a": 1, "person_b": 4, "type": "班子", "context": "县委常委会（扩大）会议同场，书记与常务副县长同席", "overlap_org": "中共吴起县委", "overlap_period": "2026-present"},
    {"person_a": 1, "person_b": 19, "type": "工作关系", "context": "县四套班子领导共同走访慰问；人大常委会", "overlap_org": "吴起县", "overlap_period": "2026-present"},
    {"person_a": 1, "person_b": 20, "type": "工作关系", "context": "县政协主席梁丰出席,与县委常委会同场", "overlap_org": "吴起县政协/县委", "overlap_period": "2026-present"},
    # 县长与政府班子
    {"person_a": 2, "person_b": 4, "type": "工作搭档", "context": "代县长闫晓妮——常务副县长张史奇（县政府常务工作、经济调度）", "overlap_org": "吴起县人民政府", "overlap_period": "2026-present"},
    {"person_a": 2, "person_b": 5, "type": "工作搭档", "context": "代县长——副县长王崛（农业农村、乡村振兴）同场政府会议", "overlap_org": "吴起县人民政府", "overlap_period": "2026-present"},
    {"person_a": 2, "person_b": 13, "type": "工作搭档", "context": "代县长——副县长、公安局长荆永恒（治安、防汛安保）", "overlap_org": "吴起县人民政府", "overlap_period": "2026-present"},
    # 政府班子内部（跨县/同单位履历交集）
    {"person_a": 5, "person_b": 15, "type": "同系统(延安市委办/组织部)", "context": "王崛曾在延安市委办、王文文曾在延安市委组织部工作，均市级系统出身、现任吴起副县长", "overlap_org": "延安市级机关", "overlap_period": "2010s"},
    {"person_a": 16, "person_b": 18, "type": "同乡代码(志丹人)", "context": "曹殿东为陕西志丹人，曾在志丹县政府办任；蔡德勤为陕西吴起本土干部", "overlap_org": "志丹县/吴起县", "overlap_period": "unknown"},
    {"person_a": 13, "person_b": 24, "type": "前同单位", "context": "荆永恒曾在宜川县政府任副县长、公安局长（离开后再报道吴起）", "overlap_org": "宜川县政府", "overlap_period": "2019-2024"},
    # 前任班子与历史衔接
    {"person_a": 24, "person_b": 3, "type": "前任班子", "context": "贺毅(书记)——乔栋(副书记) 曾同任县委班子（贺毅任职期间）", "overlap_org": "中共吴起县委", "overlap_period": "unknown-2026"},
]

# ════════════════════════════════════════════════════════════════════════════════════
# Person JSON generation (schema_version 1.0, evidence-backed)
# ════════════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "张宏江": {
        "filename": f"{TODAY}-陕西省-延安市-县委书记-张宏江.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "陕西省", "city": "延安市", "region": "吴起县", "job": "县委书记", "task_id": "shaanxi_吴起县", "time_focus": "2026"},
            "identity": {
                "person_id": "wuqi_zhang_hongjiang",
                "name": "张宏江",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {"name_birth": "张宏江_未知", "name_birthplace": "张宏江_未知", "official_source": "https://www.wqx.gov.cn/"}
            },
            "current_status": {"current_post": "县委书记", "current_org": "中共吴起县委员会", "administrative_rank": "县处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002", "S003"]},
            "career_timeline": [
                {"start": "2026", "end": "present", "org": "中共吴起县委员会", "title": "县委书记", "level": "县处级", "location": "陕西延安吴起", "system": "party", "rank": "县处级", "is_key_promotion": True, "notes": "2026年6月左右由县委副书记、县长升任县委'书记；县人大常委会第二十六至二十八次会议相关新闻确认；人民武力部党委第一书记(2026-05-20)", "confidence": "confirmed", "source_ids": ["S001", "S002", "S009"]},
                {"start": "unknown", "end": "2026-06", "org": "吴起县人民政府", "title": "县委副书记、县长", "level": "县处级", "location": "陕西延安吴起", "system": "government", "rank": "县处级", "is_key_promotion": False, "notes": "2026-03-04县人大会议前全县两会期间任县委副书记、县长；2026-06-11县人大常委会接受辞去县长职务；多次主持经济运行、重点项目调度与防汛会议", "confidence": "confirmed", "source_ids": ["S006", "S008", "S007"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开渠道未获取张宏江任吴起县长、县委书记之前履历（出生、籍贯、学历、任吴起县长前任职单位与时间、任吴起县长的具体任命年份）。已是主要缺口。", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [
                {"org": "中共吴起县委员会", "role": "县委书记", "period": "2026-present", "source_ids": ["S001"]},
                {"org": "吴起县人民政府", "role": "县委副书记、县长", "period": "unknown-2026-06", "source_ids": ["S008"]},
            ],
            "relationships": [
                {"person": "闫晓妮", "person_id": "wuqi_yan_xiaoni", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记——县委副书记、代县长党政搭档；张宏江由县长任书记后闫晓妮继任代县长", "overlap_org": "中共吴起县委/县政府", "overlap_period": "2026-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "贺毅", "person_id": "wuqi_he_yi", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "贺毅(原书记)离任，张宏江接任；两人均曾任吴起县长", "overlap_org": "中共吴起县委/县政府", "overlap_period": "2026", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
                {"person": "赵晓杰", "person_id": "wuqi_zhao_xiaojie", "relationship_type": "overlap", "strength": "medium", "evidence": "书记——组织部长同管委会/县委部署", "overlap_org": "中共吴起县委", "overlap_period": "2026-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S010"]},
            ],
            "governance_record": [
                {"period": "2026-08", "domain": "public_security", "achievement_or_event": "主持召开全县防汛抗旱、防汛调度会,部署北洛河防洪、地质灾害排查、安全生产大检查", "role_in_event": "主持", "measurable_outcome": "", "location": "延安吴起", "confidence": "confirmed", "source_ids": ["S002"]},
                {"period": "2026-07", "domain": "economic_development", "achievement_or_event": "主持县委常委会(扩大)会议部署改革、产业", "role_in_event": "主持", "measurable_outcome": "", "location": "延安吴起", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "professional_profile": {
                "primary_specializations": ["党的建设", "县域治理", "经济调度", "应急防汛"],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["延安市"],
                "promotion_velocity": {"summary": "由吴起县长升任吴起县委书记（2026）；晋升路径清晰、幅度在县域内", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "stability_oriented", "evidence": "多次强调防汛、安全生产、风险隐患排查督导", "confidence": "plausible", "source_ids": ["S002"]},
                    {"trait": "grassroots_oriented", "evidence": "到吴仓堡镇、吴起街道、白豹镇、香菇产业等一线调研", "confidence": "plausible", "source_ids": ["S011"]},
                ],
                "speech_themes": ["五个深入学习贯彻", "防汛", "正确政绩观", "四个十", "一园五区"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "公开搜索未发现张宏江相关纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "张宏江主持召开县委常委会（扩大）会议", "url": "https://www.wqx.gov.cn/xwzx/bdyw/2079371020751343617.html", "publisher": "吴起县融媒体中心", "published_at": "2026-07-17", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认'县委书记张宏江'"},
                {"id": "S002", "title": "县委书记张宏江主持召开全县防汛抗旱工作视频调度会", "url": "https://www.wqx.gov.cn/xwzx/bdyw/2077216293917876225.html", "publisher": "吴起县融媒体中心", "published_at": "2026-07-11", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县委书记在任"},
                {"id": "S006", "title": "政协吴起县第十届委员会第五次会议", "url": "https://www.wqx.gov.cn/xwzx/bdyw/2034565029983952897.html", "publisher": "吴起县融媒体中心", "published_at": "2026-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "2026-03仍任县委副书记、县长"},
                {"id": "S008", "title": "县第十八届人大常委会第二十六次会议", "url": "https://www.wqx.gov.cn/xwzx/bdyw/2068856703933292546.html", "publisher": "吴起县融媒体中心", "published_at": "2026-06-11", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "接受张宏江辞职、任闫妮代县长"},
            ],
            "confidence_summary": {"identity": "partial", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "medium", "biggest_gap": "任吴起县长的先工作经历及个人基本信息（出生、籍贯、学历、任县长时间）"},
            "open_questions": [
                {"priority": "critical", "question": "张宏江完整履历(出生、籍贯、学历、任吴起县长前任职单位、任吴起县长具体年份)", "why_it_matters": "县委书记关键人物履历不完整", "suggested_queries": ["张宏江 吴起 简历", "张宏江 延安 任前公示", "吴起县 县委书记 任命"], "last_attempted": AS_OF},
                {"priority": "high", "question": "张宏江是何处交流到吴起任长/县长(是否此前在洛川/延安市直)", "why_it_matters": "跨县域人事网络分析", "suggested_queries": ["张宏江 洛川", "张宏江 县长 任命"], "last_attempted": AS_OF},
            ]
        }
    },
    "闫晓妮": {
        "filename": f"{TODAY}-陕西省-延安市-代县长-闫晓妮.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "陕西省", "city": "延安市", "region": "吴起县", "job": "代县长", "task_id": "shaanxi_吴起县", "time_focus": "2026"},
            "identity": {
                "person_id": "wuqi_yan_xiaoni",
                "name": "闫晓妮",
                "aliases": [],
                "gender": "女",
                "ethnicity": "汉族",
                "birth": "1980-12",
                "birthplace": "陕西蓝田",
                "native_place": "陕西蓝田",
                "education": [
                    {"period": "higher", "institution": "延安院校（学历）", "major": "", "degree": "管理学学士、在职研究生", "study_type": "unknown", "source_ids": ["S012"]}
                ],
                "party_join": "2002-06",
                "work_start": "2003-07",
                "dedupe_keys": {"name_birth": "闫晓妮_198012", "name_birthplace": "闫晓妮_陕西蓝田", "official_source": "https://www.wqx.gov.cn/zfxxgk/fdzdgknr/zfld/xc/yxn/1.html"}
            },
            "current_status": {"current_post": "县委副书记、代县长", "current_org": "吴起县人民政府", "administrative_rank": "县处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S012", "S008"]},
            "career_timeline": [
                {"start": "2026-06", "end": "present", "org": "吴起县人民政府", "title": "县委副书记、代县长", "level": "县处级", "location": "陕西延安吴起", "system": "party|government", "rank": "县处级", "is_key_promotion": True, "notes": "2026-06-11县人大常委会任命为副县长、代理县长(接任张宏江辞去县长职)", "confidence": "confirmed", "source_ids": ["S008"]},
                {"start": "2024-10", "end": "2026-05", "org": "中共安塞区委", "title": "安塞区委副书记、砖窑湾镇党委书记", "level": "县处级", "location": "陕西延安安塞", "system": "party", "rank": "县处级", "is_key_promotion": False, "notes": "官方简历确认；涉及安塞区(跨县交流指标，2025-01曾以该身份出现)", "confidence": "confirmed", "source_ids": ["S012"]},
                {"start": "2022-03", "end": "2024-10", "org": "延安市委直属机关工作委员会", "title": "工委书记", "level": "县处级", "location": "陕西延安", "system": "other", "rank": "县处级", "is_key_promotion": False, "notes": "市级直属工委", "confidence": "confirmed", "source_ids": ["S012"]},
                {"start": "2012-08", "end": "2022-03", "org": "共青团延安市委", "title": "副书记", "level": "副县处级", "location": "陕西延安", "system": "other", "rank": "副县处级", "is_key_promotion": False, "notes": "共青团延安市委副书记", "confidence": "confirmed", "source_ids": ["S012"]},
                {"start": "2003-07", "end": "2012-08", "org": "中共延安市委组织部", "title": "干部监督科副主任科员→组织科副科长", "level": "乡科级", "location": "陕西延安", "system": "organization", "rank": "乡科级", "is_key_promotion": False, "notes": "市委组织部科级干部", "confidence": "confirmed", "source_ids": ["S012"]},
            ],
            "organizations": [
                {"org": "吴起县人民政府", "role": "县委副书记、代县长", "period": "2026-06-present", "source_ids": ["S008"]},
                {"org": "中共安塞区委", "role": "区委副书记、砖窑湾镇党委书记", "period": "2024-10-2026-05", "source_ids": ["S012"]},
                {"org": "延安市委直属机关工委", "role": "书记", "period": "2022-03-2024-10", "source_ids": ["S012"]},
                {"org": "共青团延安市委", "role": "副书记", "period": "2012-08-2022-03", "source_ids": ["S012"]},
                {"org": "延安市委组织部", "role": "干部监督科/组织科", "period": "2003-07-2012-08", "source_ids": ["S012"]},
            ],
            "relationships": [
                {"person": "张宏江", "person_id": "wuqi_zhang_hongjiang", "relationship_type": "overlap", "strength": "strong", "evidence": "代县长闫晓妮——县委书记张宏江党政搭档；闫晓妮接任张宏江辞任的县长职", "overlap_org": "中共吴起县委/县政府", "overlap_period": "2026-06-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S008"]},
                {"person": "贺毅", "person_id": "wuqi_he_yi", "relationship_type": "other", "strength": "weak", "evidence": "贺毅任书记期间、闫晓妮未同班子（其到达为2026）；关系存疑", "overlap_org": "中共吴起县委", "overlap_period": "unknown", "direction": "undirected", "confidence": "unverified", "source_ids": []},
                {"person": "张史奇", "person_id": "wuqi_zhang_shiqi", "relationship_type": "overlap", "strength": "medium", "evidence": "代县长——常务副县长张史奇（分管县政府常务/经济）同场政府会议", "overlap_org": "吴起县人民政府", "overlap_period": "2026-present", "direction": "undirected", "confidence": "confirmed", "source_ids": []},
            ],
            "governance_record": [
                {"period": "2026-08", "domain": "public_security", "achievement_or_event": "主持县政府党组(扩大)会议传达防汛、教育、党建指示", "role_in_event": "主持", "measurable_outcome": "", "location": "延安吴起", "confidence": "confirmed", "source_ids": ["S013"]},
                {"period": "2026-07", "domain": "rural_revitalization", "achievement_or_event": "到五谷城镇调研农业农村工作", "role_in_event": "带队调研", "measurable_outcome": "", "location": "延安吴起", "confidence": "confirmed", "source_ids": []},
            ],
            "professional_profile": {
                "primary_specializations": ["党的建设", "组织人才", "群团工作"],
                "secondary_specializations": ["县域治理", "农业农村"],
                "career_pattern": "provincial_department(市级机关→县区)",
                "systems_experience": ["organization", "party", "government"],
                "geographic_pattern": ["延安市", "安塞区", "吴起县"],
                "promotion_velocity": {"summary": "市委组织部→团市委副书记→市直机关工委书记→安塞区委副书记→吴起代县长，晋升路径清晰", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "grassroots_oriented", "evidence": "调研乡镇农业农村；强调应急、民生、教育", "confidence": "plausible", "source_ids": ["S013"]},
                ],
                "speech_themes": ["防汛安全", "基础教育", "民生实事", "党建引领"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "公开搜索未发现闫晓妮的纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S012", "title": "吴起县代县长闫晓妮(个人简历)", "url": "https://www.wqx.gov.cn/zfxxgk/fdzdgknr/zfld/xc/yxn/1.html", "publisher": "吴起县人民政府", "published_at": "2026-06-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官方简历：含出生、籍贯、学历与完整任职时间线"},
                {"id": "S008", "title": "县第十八届人大常委会第二十六次会议", "url": "https://www.wqx.gov.cn/xwzx/bdyw/2068856703933292546.html", "publisher": "吴起县融媒体中心", "published_at": "2026-06-11", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "决定任命闫晓妮为副县长、代理县长"},
                {"id": "S013", "title": "闫晓妮主持召开县政府党组（扩大）会议", "url": "https://www.wqx.gov.cn/xwzx/bdyw/2084826023890837506.html", "publisher": "吴起县融媒体中心", "published_at": "2026-07-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "政府党组书记、代县长在任"},
            ],
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "complete", "relationship_confidence": "medium", "biggest_gap": "任安塞区委副书记前后学习经历与学历具体院校；吴起代县长的正式当选时间"},
            "open_questions": [
                {"priority": "low", "question": "闫晓妮的学历具体院校/专业", "why_it_matters": "简历中'管理学学士、在职研究生'未具体化", "suggested_queries": ["闫晓妮 蓝田 学历"], "last_attempted": AS_OF}
            ]
        }
    },
}


def write_person_json(data: dict, filename: str) -> Path:
    path = STAGING_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")
    return path


def main():
    print(f"Building network for {SLUG}...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print()

    print("Writing person JSON files...")
    for key, entry in PERSON_JSON_TEMPLATE.items():
        write_person_json(entry["data"], entry["filename"])

    print()
    print("=" * 60)
    print(f"Build complete for {SLUG}")
    print(f"  {len(persons_data)} persons")
    print(f"  {len(organizations_data)} organizations")
    print(f"  {len(positions_data)} positions")
    print(f"  {len(relationships_data)} relationships")
    print(f"  {len(PERSON_JSON_TEMPLATE)} person JSONs")
    print("=" * 60)


if __name__ == "__main__":
    main()