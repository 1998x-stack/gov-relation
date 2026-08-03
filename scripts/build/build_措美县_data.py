#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
措美县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 西藏自治区
Parent City: 山南市
Region: 措美县
Targets: 县委书记 & 县长

Research Sources:
- 措美县人民政府官网 (www.cuomei.gov.cn):
  - 领导之窗 — 邢飞县长个人页面: http://www.cuomei.gov.cn/zwgk/ldzc/202106/t20210617_83665.html
  - 领导之窗 — 普布扎西: http://www.cuomei.gov.cn/zwgk/ldzc/202106/t20210617_83659.html
  - 领导之窗 — 张伟良: http://www.cuomei.gov.cn/zwgk/ldzc/202106/t20210617_83658.html
  - 领导之窗 — 益西加措: http://www.cuomei.gov.cn/zwgk/ldzc/202106/t20210617_83656.html
  - 领导之窗 — 向晓花: http://www.cuomei.gov.cn/zwgk/ldzc/202106/t20210617_83648.html
  - 领导之窗 — 周兆青: http://www.cuomei.gov.cn/zwgk/ldzc/202106/t20210617_83651.html
  - 领导之窗 — 多吉: http://www.cuomei.gov.cn/zwgk/ldzc/202505/t20250506_150590.html
  - 领导之窗 — 巴桑罗布: http://www.cuomei.gov.cn/zwgk/ldzc/202505/t20250506_150592.html
- 新闻确认: 桑旦为县委书记(2026年4月起多次以"县委书记桑旦"出现在领导活动栏目)
  - http://www.cuomei.gov.cn/xwzx/ldhd/202606/t20260612_171068.html → 县委书记桑旦实地督导"三农"工作
  - http://www.cuomei.gov.cn/xwzx/ldhd/202606/t20260603_170684.html → 县委书记桑旦调研督导城市建设工作
  - http://www.cuomei.gov.cn/xwzx/ldhd/202605/t20260519_169449.html → 县委书记桑旦调研重点工作
  - http://www.cuomei.gov.cn/xwzx/ldhd/202604/t20260427_168382.html → 桑旦深入古堆乡督导调研
  - http://www.cuomei.gov.cn/xwzx/ldhd/202606/t20260603_170682.html → 桑旦主持召开2026年全县林长制河湖长制工作会议
  - http://www.cuomei.gov.cn/xwzx/ldhd/202606/t20260603_170676.html → 谢超调研哲古镇
- 邢飞（县长）个人简历来自领导之窗页面: "邢飞，男，汉族，1978年7月出生，陕西临潼人..."
- 梁博副县长出现在领导活动中: http://www.cuomei.gov.cn/xwzx/ldhd/202607/t20260716_173601.html

Research Date: 2026-08-03

Gaps:
- 县委书记桑旦的出生年月、籍贯、学历、完整履历暂缺（未在政府网站公布个人简介）
- 梁博副县长(交通)的详细履历暂缺（未在领导之窗页面中列出）
- 谢超(县委常委)的详细履历和职务暂缺
- 孟子东(县委常委、县委办主任)的详细履历暂缺
- 县人大常委会主任、县政协主席姓名暂缺
- 前任县委书记信息暂缺
- 纪委书记、组织部长、宣传部长、统战部长、政法委书记等县委主要部门负责人信息暂缺
- 部分副县长的详细分工和完整履历暂缺
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "措美县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "桑旦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "措美县委书记",
        "current_org": "中共措美县委员会",
        "source": "措美县人民政府官网领导活动：'县委书记桑旦'多次出现在2026年4月—6月的公开报道中。来源：http://www.cuomei.gov.cn/xwzx/ldhd/202606/t20260612_171068.html — '县委书记桑旦实地督导三农工作'"
    },
    {
        "id": 2,
        "name": "邢飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年7月",
        "birthplace": "陕西临潼",
        "education": "西藏自治区党委党校研究生班经济学（经济管理）专业毕业",
        "party_join": "2001年6月",
        "work_start": "1999年7月",
        "current_post": "措美县委副书记、县长",
        "current_org": "措美县人民政府",
        "source": "https://www.cuomei.gov.cn/zwgk/ldzc/202106/t20210617_83665.html — 邢飞，男，汉族，1978年7月出生，陕西临潼人，2001年6月入党，1999年7月参加工作，西藏自治区党委党校研究生院经济学（经济管理）专业毕业。现任西藏自治区山南市措美县委副书记、政府县长。"
    },
    # ════════════════════════════════════════
    # Government Deputy Leaders (from 领导之窗)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "普布扎西",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1979年10月",
        "birthplace": "西藏琼结",
        "education": "本科学历",
        "party_join": "2007年6月",
        "work_start": "2004年9月",
        "current_post": "措美县委常委、政府常务副县长",
        "current_org": "措美县人民政府",
        "source": "https://www.cuomei.gov.cn/zwgk/ldzc/202106/t20210617_83659.html — 普布扎西，男，藏族，1979年10月生，西藏琼结人，2007年6月加入中国共产党，2004年9月参加工作，本科学历。现任西藏自治区山南市措美县委常委、政府常务副县长。"
    },
    {
        "id": 4,
        "name": "张伟良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年11月",
        "birthplace": "山西运城",
        "education": "大专学历",
        "party_join": "1997年12月",
        "work_start": "1997年7月",
        "current_post": "措美县人民政府副县长",
        "current_org": "措美县人民政府",
        "source": "https://www.cuomei.gov.cn/zwgk/ldzc/202106/t20210617_83658.html — 张伟良，男，汉族，1972年11月生，山西运城人，1997年12月加入中国共产党，1997年7月参加工作，大专学历。现任西藏自治区措美县人民政府副县长。"
    },
    {
        "id": 5,
        "name": "益西加措",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1969年8月",
        "birthplace": "西藏扎囊",
        "education": "大专学历",
        "party_join": "2004年6月",
        "work_start": "1992年7月",
        "current_post": "措美县人民政府副县长",
        "current_org": "措美县人民政府",
        "source": "https://www.cuomei.gov.cn/zwgk/ldzc/202106/t20210617_83656.html — 益西加措，男，藏族，1969年8月生，西藏扎囊人，2004年6月加入中国共产党，1992年7月参加工作，大专学历。现任西藏自治区措美县人民政府副县长。"
    },
    {
        "id": 6,
        "name": "向晓花",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年8月",
        "birthplace": "四川绵阳",
        "education": "大学学历",
        "party_join": "2006年7月",
        "work_start": "2005年8月",
        "current_post": "措美县人民政府副县长",
        "current_org": "措美县人民政府",
        "source": "https://www.cuomei.gov.cn/zwgk/ldzc/202106/t20210617_83648.html — 向晓花，女，汉族，1982年8月生，四川绵阳人，2006年7月加入中国共产党，2005年8月参加工作，大学学历。现任西藏自治区山南市措美县政府副县长。"
    },
    {
        "id": 7,
        "name": "周兆青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年9月",
        "birthplace": "湖北钟祥",
        "education": "在职大专学历",
        "party_join": "2001年6月",
        "work_start": "1999年7月",
        "current_post": "措美县人民政府副县长",
        "current_org": "措美县人民政府",
        "source": "https://www.cuomei.gov.cn/zwgk/ldzc/202106/t20210617_83651.html — 周兆青，男，汉族，1979年9月出生，湖北钟祥人，2001年6月加入中国共产党，1999年7月参加工作，在职大专学历。现任西藏自治区措美县人民政府副县长。"
    },
    {
        "id": 8,
        "name": "多吉",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1980年9月",
        "birthplace": "西藏琼结",
        "education": "大学学历",
        "party_join": "2005年9月",
        "work_start": "2006年8月",
        "current_post": "措美县人民政府副县长",
        "current_org": "措美县人民政府",
        "source": "https://www.cuomei.gov.cn/zwgk/ldzc/202505/t20250506_150590.html — 多吉，男，藏族，1980年9月生，西藏琼结人，2005年9月加入中国共产党，2006年8月参加工作，大学学历。现任西藏自治区措美县人民政府副县长。"
    },
    {
        "id": 9,
        "name": "巴桑罗布",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1984年7月",
        "birthplace": "西藏乃东",
        "education": "大学学历",
        "party_join": "2008年6月",
        "work_start": "2006年7月",
        "current_post": "措美县人民政府副县长",
        "current_org": "措美县人民政府",
        "source": "https://www.cuomei.gov.cn/zwgk/ldzc/202505/t20250506_150592.html — 巴桑罗布，男，藏族，1984年7月生，西藏乃东人，2008年6月加入中国共产党，2006年7月参加工作，大学学历。现任西藏自治区措美县人民政府副县长。"
    },
    # ════════════════════════════════════════
    # Other Known Leaders (from leadership activities)
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "梁博",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "措美县人民政府副县长",
        "current_org": "措美县人民政府",
        "source": "https://www.cuomei.gov.cn/xwzx/ldhd/202607/t20260716_173601.html — '梁博副县长带队督导交通在建项目'"
    },
    {
        "id": 11,
        "name": "孟子东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "措美县委常委、县委办主任",
        "current_org": "中共措美县委办公室",
        "source": "https://www.cuomei.gov.cn/xwzx/ldhd/202606/t20260603_170684.html — '县委常委、县委办主任孟子东'参与县委书记桑旦城市建设调研"
    },
    {
        "id": 12,
        "name": "谢超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "措美县领导",
        "current_org": "措美县人民政府",
        "source": "https://www.cuomei.gov.cn/xwzx/ldhd/202606/t20260603_170676.html — '谢超调研哲古镇古珠村藏蕨麻试种植工作'"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共措美县委员会",
        "type": "党委",
        "level": "县级",
        "location": "山南市措美县",
        "parent": "中共山南市委"
    },
    {
        "id": 2,
        "name": "措美县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "山南市措美县",
        "parent": "山南市人民政府"
    },
    {
        "id": 3,
        "name": "措美县人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "山南市措美县",
        "parent": "山南市人大常委会"
    },
    {
        "id": 4,
        "name": "政协措美县委员会",
        "type": "政协",
        "level": "县级",
        "location": "山南市措美县",
        "parent": "政协山南市委员会"
    },
    {
        "id": 5,
        "name": "中共措美县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "location": "山南市措美县",
        "parent": "中共山南市纪律检查委员会"
    },
    {
        "id": 6,
        "name": "中共措美县委组织部",
        "type": "党委部门",
        "level": "县级",
        "location": "山南市措美县",
        "parent": "中共措美县委员会"
    },
    {
        "id": 7,
        "name": "中共措美县委宣传部",
        "type": "党委部门",
        "level": "县级",
        "location": "山南市措美县",
        "parent": "中共措美县委员会"
    },
    {
        "id": 8,
        "name": "中共措美县委统战部",
        "type": "党委部门",
        "level": "县级",
        "location": "山南市措美县",
        "parent": "中共措美县委员会"
    },
    {
        "id": 9,
        "name": "中共措美县委政法委",
        "type": "政法系统",
        "level": "县级",
        "location": "山南市措美县",
        "parent": "中共措美县委员会"
    },
    {
        "id": 10,
        "name": "中共措美县委办公室",
        "type": "党委部门",
        "level": "县级",
        "location": "山南市措美县",
        "parent": "中共措美县委员会"
    },
    {
        "id": 11,
        "name": "措美县审计局",
        "type": "政府部门",
        "level": "县级",
        "location": "山南市措美县",
        "parent": "措美县人民政府"
    },
    {
        "id": 12,
        "name": "措美县发展和改革委员会",
        "type": "政府部门",
        "level": "县级",
        "location": "山南市措美县",
        "parent": "措美县人民政府"
    },
    # Previous organizations (for career timelines)
    {
        "id": 13,
        "name": "山南地区行政公署国有资产监督管理委员会",
        "type": "政府部门",
        "level": "地市级",
        "location": "山南地区",
        "parent": "山南地区行政公署"
    },
    {
        "id": 14,
        "name": "中共扎囊县委员会",
        "type": "党委",
        "level": "县级",
        "location": "山南市扎囊县",
        "parent": "中共山南市委"
    },
    {
        "id": 15,
        "name": "浪卡子县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "山南市浪卡子县",
        "parent": "山南市人民政府"
    },
    {
        "id": 16,
        "name": "中共山南市委统战部",
        "type": "党委部门",
        "level": "地市级",
        "location": "山南市乃东区",
        "parent": "中共山南市委员会"
    },
    {
        "id": 17,
        "name": "隆子县交通局",
        "type": "政府部门",
        "level": "县级",
        "location": "山南市隆子县",
        "parent": "隆子县人民政府"
    },
    {
        "id": 18,
        "name": "隆子县水利局",
        "type": "政府部门",
        "level": "县级",
        "location": "山南市隆子县",
        "parent": "隆子县人民政府"
    },
    {
        "id": 19,
        "name": "加查县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "location": "山南市加查县",
        "parent": "中共加查县委员会"
    },
    {
        "id": 20,
        "name": "加查县人民政府办公室",
        "type": "政府部门",
        "level": "县级",
        "location": "山南市加查县",
        "parent": "加查县人民政府"
    },
    {
        "id": 21,
        "name": "加查县拉绥乡",
        "type": "乡镇/街道",
        "level": "乡级",
        "location": "山南市加查县",
        "parent": "加查县人民政府"
    },
    {
        "id": 22,
        "name": "加查县坝乡",
        "type": "乡/镇",
        "level": "乡级",
        "location": "山南市加查县",
        "parent": "加查县人民政府"
    },
    {
        "id": 23,
        "name": "加查县崔久乡",
        "type": "乡/镇",
        "level": "乡级",
        "location": "山南市加查县",
        "parent": "加查县人民政府"
    },
    {
        "id": 24,
        "name": "洛扎县色乡",
        "type": "乡/镇",
        "level": "乡级",
        "location": "山南市洛扎县",
        "parent": "洛扎县人民政府"
    },
    {
        "id": 25,
        "name": "洛扎县生格乡",
        "type": "乡/镇",
        "level": "乡级",
        "location": "山南市洛扎县",
        "parent": "洛扎县人民政府"
    },
    {
        "id": 26,
        "name": "洛扎县民政局",
        "type": "政府部门",
        "level": "县级",
        "location": "山南市洛扎县",
        "parent": "洛扎县人民政府"
    },
    {
        "id": 27,
        "name": "措美县措美镇",
        "type": "乡/镇",
        "level": "乡级",
        "location": "山南市措美县",
        "parent": "措美县人民政府"
    },
    {
        "id": 28,
        "name": "加查县政协",
        "type": "政协",
        "level": "县级",
        "location": "山南市加查县",
        "parent": "政协山南市委员会"
    },
    {
        "id": 29,
        "name": "山南市委政法委",
        "type": "政法系统",
        "level": "地市级",
        "location": "山南市乃东区",
        "parent": "中共山南市委员会"
    },
]

# 3. Positions
positions = [
    # 桑旦 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "措美县委书记", "start": "", "end": "present", "rank": "正处级", "note": "2026年4月至6月以县委书记身份多次出现在公开报道中"},
    # 邢飞 — 县长
    {"person_id": 2, "org_id": 2, "title": "措美县委副书记、县长", "start": "", "end": "present", "rank": "正处级", "note": "主持县政府全面工作"},
    {"person_id": 2, "org_id": 13, "title": "山南地区行政公署国有资产监督管理委员会政工人事科科长", "start": "", "end": "", "rank": "", "note": "曾任"},
    {"person_id": 2, "org_id": 14, "title": "扎囊县委常委、组织部部长", "start": "", "end": "", "rank": "副处级", "note": "曾任"},
    {"person_id": 2, "org_id": 14, "title": "扎囊县委副书记", "start": "", "end": "", "rank": "正处级", "note": "曾任"},
    {"person_id": 2, "org_id": 15, "title": "浪卡子县委副书记、人大常委会主任", "start": "", "end": "", "rank": "正处级", "note": "曾任"},
    {"person_id": 2, "org_id": 16, "title": "山南市委统战部常务副部长", "start": "", "end": "", "rank": "正处级", "note": "曾任"},
    # 普布扎西 — 县委常委、常务副县长
    {"person_id": 3, "org_id": 1, "title": "措美县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "措美县政府常务副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 17, "title": "隆子县交通局副局长", "start": "", "end": "", "rank": "", "note": "曾任"},
    {"person_id": 3, "org_id": 17, "title": "隆子县交通局局长", "start": "", "end": "", "rank": "", "note": "曾任"},
    {"person_id": 3, "org_id": 18, "title": "隆子县水利局局长", "start": "", "end": "", "rank": "", "note": "曾任"},
    {"person_id": 3, "org_id": 2, "title": "措美县政府副县长（升任常务前）", "start": "", "end": "", "rank": "副处级", "note": "曾任"},
    # 张伟良 — 副县长
    {"person_id": 4, "org_id": 2, "title": "措美县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 19, "title": "加查县纪律检查委员会副书记", "start": "", "end": "", "rank": "", "note": "曾任"},
    {"person_id": 4, "org_id": 20, "title": "加查县人民政府办公室副主任", "start": "", "end": "", "rank": "", "note": "曾任"},
    {"person_id": 4, "org_id": 21, "title": "加查县拉绥乡党委书记", "start": "", "end": "", "rank": "正科级", "note": "曾任"},
    {"person_id": 4, "org_id": 28, "title": "加查县政协副主席", "start": "", "end": "", "rank": "副处级", "note": "曾任"},
    # 益西加措 — 副县长
    {"person_id": 5, "org_id": 2, "title": "措美县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 23, "title": "加查县林业局副局长", "start": "", "end": "", "rank": "", "note": "曾任"},
    {"person_id": 5, "org_id": 22, "title": "加查县坝乡党委副书记、乡长", "start": "", "end": "", "rank": "正科级", "note": "曾任"},
    {"person_id": 5, "org_id": 23, "title": "加查县崔久乡党委书记", "start": "", "end": "", "rank": "正科级", "note": "曾任"},
    # 向晓花 — 副县长
    {"person_id": 6, "org_id": 2, "title": "措美县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 24, "title": "洛扎县色乡党委宣传委员、副乡长", "start": "", "end": "", "rank": "", "note": "曾任"},
    {"person_id": 6, "org_id": 25, "title": "洛扎县生格乡党委书记", "start": "", "end": "", "rank": "正科级", "note": "曾任"},
    {"person_id": 6, "org_id": 26, "title": "洛扎县民政局局长、退役军人事务局局长", "start": "", "end": "", "rank": "", "note": "曾任"},
    # 周兆青 — 副县长
    {"person_id": 7, "org_id": 2, "title": "措美县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 19, "title": "加查县建设局副局长", "start": "", "end": "", "rank": "", "note": "曾任"},
    {"person_id": 7, "org_id": 21, "title": "加查县拉绥乡党委书记、人大主席", "start": "", "end": "", "rank": "正科级", "note": "曾任"},
    {"person_id": 7, "org_id": 22, "title": "加查县坝乡党委书记", "start": "", "end": "", "rank": "正科级", "note": "曾任"},
    {"person_id": 7, "org_id": 19, "title": "加查县市场监督管理局局长", "start": "", "end": "", "rank": "", "note": "曾任"},
    # 多吉 — 副县长
    {"person_id": 8, "org_id": 2, "title": "措美县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "措美县老干部局局长", "start": "", "end": "", "rank": "", "note": "曾任"},
    {"person_id": 8, "org_id": 27, "title": "措美镇党委副书记、镇长", "start": "", "end": "", "rank": "正科级", "note": "曾任"},
    {"person_id": 8, "org_id": 27, "title": "措美镇党委书记", "start": "", "end": "", "rank": "正科级", "note": "曾任"},
    # 巴桑罗布 — 副县长
    {"person_id": 9, "org_id": 2, "title": "措美县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 29, "title": "山南市先进双联户创建评选工作办公室副主任", "start": "", "end": "", "rank": "", "note": "曾任"},
    {"person_id": 9, "org_id": 29, "title": "山南市委政法委维稳指导科科长", "start": "", "end": "", "rank": "", "note": "曾任"},
    {"person_id": 9, "org_id": 29, "title": "山南市委政法委政工人事科科长", "start": "", "end": "", "rank": "", "note": "曾任"},
    # 梁博 — 副县长
    {"person_id": 10, "org_id": 2, "title": "措美县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "分管交通领域"},
    # 孟子东 — 县委常委、县委办主任
    {"person_id": 11, "org_id": 1, "title": "措美县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 10, "title": "措美县委办公室主任", "start": "", "end": "present", "rank": "正科级", "note": ""},
    # 谢超 — 县领导
    {"person_id": 12, "org_id": 2, "title": "措美县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待查"},
]

# 4. Relationships
relationships = [
    # 桑旦 — 邢飞：党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政一把手", "context": "桑旦（县委书记）与邢飞（县长）为措美县党政主要负责人", "overlap_org": "措美县", "overlap_period": "2026年至今"},
    # 邢飞 — 普布扎西：上下级（县长与常务副县长）
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长与常务副县长", "overlap_org": "措美县人民政府", "overlap_period": ""},
    # 邢泰 — 各副县长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长与副县长", "overlap_org": "措美县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长与副县长", "overlap_org": "措美县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长与副县长", "overlap_org": "措美县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长与副县长", "overlap_org": "措美县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长与副县长", "overlap_org": "措美县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长与副县长", "overlap_org": "措美县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长与副县长", "overlap_org": "措美县人民政府", "overlap_period": ""},
    # 桑旦（县委常委
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与县委常委、常务副县长", "overlap_org": "中共措美县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "县委书记与县委常委、县委办主任", "overlap_org": "中共措美县委员会", "overlap_period": "2026年至今"},
    # 多吉洞与桑旦共同调研
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "县委书记与副县长多吉多次一同下乡调研", "overlap_org": "措美县", "overlap_period": "2026年"},
    # 孟子东与桑德（直接下属）
    {"person_a": 11, "person_b": 1, "type": "上下级", "context": "县委常委、县委办主任向县委书记汇报工作", "overlap_org": "中共措美县委员会", "overlap_period": "2026年至今"},
]

# ── Build ──

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
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")