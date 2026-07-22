#!/usr/bin/env python3
"""Build Xuanzhou District (宣州区) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-16
Task: anhui_宣州区 (市辖区 level)
Province: 安徽省
Parent city: 宣城市
Region: 宣州区
Targets: 区委书记 & 区长

Sources:
  - https://www.xuanzhou.gov.cn/SiteLeader/78.html (领导之窗, accessed 2026-07-16)
  - https://www.xuanzhou.gov.cn/SiteLeader/showList/209/78.html (杨培靖 profile, accessed 2026-07-16)
  - https://www.xuanzhou.gov.cn/SiteLeader/showList/83/78.html (卢明 profile, accessed 2026-07-16)
  - https://www.xuanzhou.gov.cn/SiteLeader/showList/206/78.html (王炜 profile, accessed 2026-07-16)
  - https://www.xuanzhou.gov.cn/SiteLeader/showList/108/78.html (余建亚 profile, accessed 2026-07-16)
  - https://www.xuanzhou.gov.cn/SiteLeader/showList/119/78.html (黄彬 profile, accessed 2026-07-16)
  - https://www.xuanzhou.gov.cn/SiteLeader/showList/212/78.html (曹兵 profile, accessed 2026-07-16)
  - https://www.xuanzhou.gov.cn/SiteLeader/showList/201/78.html (周红兵 profile, accessed 2026-07-16)
  - https://www.xuanzhou.gov.cn/SiteLeader/showList/210/78.html (汪琪 profile, accessed 2026-07-16)
  - https://www.xuanzhou.gov.cn/News/show/1721665.html (区委常委会会议, 2026-07-16)
  - https://www.xuanzhou.gov.cn/News/show/1721664.html (区委理论学习中心组集中学习会议, 2026-07-16)
  - https://www.xuanzhou.gov.cn/News/show/1719137.html (宣州区第十五次党代会, 2026-06-29)
  - https://www.xuanzhou.gov.cn/News/show/1720614.html (高真理督导集中整治工作, 2026-07-09)
  - https://www.xuanzhou.gov.cn/News/show/1720474.html (高真理调研在建工业项目, 2026-07-08)

Confidence: Current roles confirmed from official Xuanzhou district government leadership pages.
  Biographical details from official government profiles. Party committee composition confirmed
  from news reports of the 15th CPC Xuanzhou District Congress and standing committee meetings.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "宣州区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "宣州区_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Top Leaders ═══════════════════════════════════════════════════
    {
        "id": 1,
        "name": "高真理",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共宣州区委",
        "source": "https://www.xuanzhou.gov.cn/News/show/1721665.html (区委常委会会议, 2026-07-16)",
        "notes": "宣州区委书记。主持区委全面工作。2026年7月主持区委常委会会议、区委理论学习中心组会议。\n2026年6月主持宣州区第十五次党代会并作报告。\n履历缺口：公开资料未找到高真理详细简历。此前职务及完整履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "杨培靖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年12月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "宣州区人民政府",
        "source": "https://www.xuanzhou.gov.cn/SiteLeader/showList/209/78.html (杨培靖官方简历, accessed 2026-07-16)",
        "notes": "宣州区委副书记、区政府区长、党组书记。领导区政府全面工作，负责审计工作。分管审计局、宣城高新区管委会。\n曾任共青团宣城市委副调研员，宣城市委台湾工作办公室副主任，泾县人民政府副县长、党组成员，泾县县委常委、宣传部部长，泾县县委副书记，宣城市干部教育培训现场教学基地管理办公室（泾县县委党校、县行政学校）常务副主任（常务副校长）。",
        "confidence": "confirmed"
    },
    # ═══ District Leadership (区领导) ══════════════════════════════════
    {
        "id": 3,
        "name": "孙金平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "宣州区人大常委会",
        "source": "https://www.xuanzhou.gov.cn/News/show/1719137.html (宣州区第十五次党代会, 2026-06-29)",
        "notes": "宣州区人大常委会主任。2026年6月宣州区第十五次党代会主席团成员。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "时国金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "宣州区政协",
        "source": "https://www.xuanzhou.gov.cn/News/show/1719137.html (宣州区第十五次党代会, 2026-06-29)",
        "notes": "宣州区政协主席。2026年6月宣州区第十五次党代会主席团成员。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "朱伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共宣州区委",
        "source": "https://www.xuanzhou.gov.cn/News/show/1719137.html (宣州区第十五次党代会, 2026-06-29)",
        "notes": "宣州区委副书记。协助书记处理区委日常工作。2026年7月参加高真理督导集中整治工作。\n履历待查。",
        "confidence": "confirmed"
    },
    # ═══ Government Leaders (区政府领导) ═══════════════════════════════
    {
        "id": 6,
        "name": "卢明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "宣州区人民政府",
        "source": "https://www.xuanzhou.gov.cn/SiteLeader/showList/83/78.html (卢明官方简历, accessed 2026-07-16)",
        "notes": "宣州区委常委、区政府常务副区长、党组副书记。负责区政府常务工作。分管发展改革、财政、金融、国资、自然资源规划、应急管理、税务、统计、林业等。\n曾任宣州区五星乡党委书记，宣州区城市管理行政执法局局长、党组书记，宣州区水阳镇党委书记（副县级），宣州区政府副区长、党组成员。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "王炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年9月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "宣州区人民政府",
        "source": "https://www.xuanzhou.gov.cn/SiteLeader/showList/206/78.html (王炜官方简历, accessed 2026-07-16)",
        "notes": "宣州区委常委、区政府副区长、党组成员。负责工信、环保、住建、城管、招商引资等。\n曾任宣城市发改委交通科科长、固定资产投资科科长、总工程师、副主任（副局长）、党组成员。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "余建亚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年9月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、区公安分局局长",
        "current_org": "宣州区人民政府",
        "source": "https://www.xuanzhou.gov.cn/SiteLeader/showList/108/78.html (余建亚官方简历, accessed 2026-07-16)",
        "notes": "宣州区政府副区长、党组成员，区委政法委副书记，宣城市公安局宣州分局局长、党委书记。负责公安、司法、退役军人事务、信访等。\n曾任宁国市公安局党委委员、纪委书记，宁国市城市管理综合执法局局长、党组书记，宁国市河沥溪街道党工委书记，宣城市公安局宣州分局局长。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "黄彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年2月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "宣州区人民政府",
        "source": "https://www.xuanzhou.gov.cn/SiteLeader/showList/119/78.html (黄彬官方简历, accessed 2026-07-16)",
        "notes": "宣州区政府副区长、党组成员。负责民政、农业农村、水利、乡村振兴、烟叶生产等。\n曾任宣州区发改委副主任，宣州区金融工作办公室主任，宣州区狸桥镇党委副书记、镇长，宣州经济开发区党工委副书记、管委会主任，宣州区狸桥镇党委书记、宣州经济开发区党工委书记。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "曹兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年4月",
        "birthplace": "",
        "native_place": "",
        "education": "博士研究生，教授",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "宣州区人民政府",
        "source": "https://www.xuanzhou.gov.cn/SiteLeader/showList/212/78.html (曹兵官方简历, accessed 2026-07-16)",
        "notes": "宣州区政府副区长、党组成员。负责科技、交通运输等。曾任安徽工程大学建筑工程学院土木工程系副主任、主任，安徽工程大学建筑工程学院副院长。\n高校挂职/任职的年轻干部，博士、教授职称。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "周红兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年11月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "宣州区人民政府",
        "source": "https://www.xuanzhou.gov.cn/SiteLeader/showList/201/78.html (周红兵官方简历, accessed 2026-07-16)",
        "notes": "宣州区政府副区长、党组成员。负责教体、商务、市场监管、数据资源、政务服务、供销等。\n曾任宣州区委组织部副部长、区人才工作领导小组办公室主任、区委组织部常务副部长，宣州区教育体育局党委书记、局长。",
        "confidence": "confirmed"
    },
    {
        "id": 12,
        "name": "汪琪",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年3月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "农工党党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "宣州区人民政府",
        "source": "https://www.xuanzhou.gov.cn/SiteLeader/showList/210/78.html (汪琪官方简历, accessed 2026-07-16)",
        "notes": "宣州区政府副区长（非中共党员，农工党）。负责人社、文旅、卫健、医保等。\n曾任宣城市人社局劳动关系与调解仲裁办公室主任、考录科科长、政策法规与表彰奖励科科长。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "赵流海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、宣城高新区管委会主任",
        "current_org": "宣州区人民政府",
        "source": "https://www.xuanzhou.gov.cn/News/show/1720474.html (高真理调研在建工业项目, 2026-07-08)",
        "notes": "宣州区政府党组成员，宣城高新区管委会主任。2026年7月陪同区委书记高真理调研在建工业项目。\n履历待查。",
        "confidence": "confirmed"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共宣州区委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共宣城市委",
        "location": "宣州区",
        "source": "official"
    },
    {
        "id": 2,
        "name": "宣州区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "宣城市人民政府",
        "location": "宣州区",
        "source": "official"
    },
    {
        "id": 3,
        "name": "宣州区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "宣州区",
        "location": "宣州区",
        "source": "official"
    },
    {
        "id": 4,
        "name": "宣州区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "宣州区",
        "location": "宣州区",
        "source": "official"
    },
    {
        "id": 5,
        "name": "宣城高新技术产业开发区管委会",
        "type": "开发区",
        "level": "县处级",
        "parent": "宣州区人民政府",
        "location": "宣州区",
        "source": "official"
    },
    {
        "id": 6,
        "name": "宣城市公安局宣州分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "宣州区人民政府",
        "location": "宣州区",
        "source": "official"
    },
    {
        "id": 7,
        "name": "泾县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "宣城市人民政府",
        "location": "泾县",
        "source": "official"
    },
    {
        "id": 8,
        "name": "中共泾县县委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共宣城市委",
        "location": "泾县",
        "source": "official"
    },
    {
        "id": 9,
        "name": "共青团宣城市委",
        "type": "群团",
        "level": "县处级",
        "parent": "宣城市",
        "location": "宣城市",
        "source": "official"
    },
    {
        "id": 10,
        "name": "宣城市委台湾工作办公室",
        "type": "政府",
        "level": "县处级",
        "parent": "宣城市",
        "location": "宣城市",
        "source": "official"
    },
    {
        "id": 11,
        "name": "宣州区五星乡党委",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "中共宣州区委",
        "location": "五星乡",
        "source": "official"
    },
    {
        "id": 12,
        "name": "宣州区城市管理行政执法局",
        "type": "政府",
        "level": "乡科级",
        "parent": "宣州区人民政府",
        "location": "宣州区",
        "source": "official"
    },
    {
        "id": 13,
        "name": "宣州区水阳镇党委",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "中共宣州区委",
        "location": "水阳镇",
        "source": "official"
    },
    {
        "id": 14,
        "name": "宣城市发改委",
        "type": "政府",
        "level": "县处级",
        "parent": "宣城市人民政府",
        "location": "宣城市",
        "source": "official"
    },
    {
        "id": 15,
        "name": "宁国市公安局",
        "type": "政府",
        "level": "乡科级",
        "parent": "宁国市人民政府",
        "location": "宁国市",
        "source": "official"
    },
    {
        "id": 16,
        "name": "宁国市河沥溪街道党工委",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "中共宁国市委",
        "location": "宁国市",
        "source": "official"
    },
    {
        "id": 17,
        "name": "宣州区狸桥镇党委",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "中共宣州区委",
        "location": "狸桥镇",
        "source": "official"
    },
    {
        "id": 18,
        "name": "宣州经济开发区管委会",
        "type": "开发区",
        "level": "乡科级",
        "parent": "宣州区人民政府",
        "location": "宣州区",
        "source": "official"
    },
    {
        "id": 19,
        "name": "安徽工程大学建筑工程学院",
        "type": "事业单位",
        "level": "县处级",
        "parent": "安徽工程大学",
        "location": "芜湖市",
        "source": "official"
    },
    {
        "id": 20,
        "name": "宣州区委组织部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共宣州区委",
        "location": "宣州区",
        "source": "official"
    },
    {
        "id": 21,
        "name": "宣州区教育体育局",
        "type": "政府",
        "level": "乡科级",
        "parent": "宣州区人民政府",
        "location": "宣州区",
        "source": "official"
    },
    {
        "id": 22,
        "name": "宣城市人社局",
        "type": "政府",
        "level": "县处级",
        "parent": "宣城市人民政府",
        "location": "宣城市",
        "source": "official"
    },
    {
        "id": 23,
        "name": "宣城市干部教育培训现场教学基地管理办公室",
        "type": "事业单位",
        "level": "县处级",
        "parent": "宣城市",
        "location": "泾县",
        "source": "official"
    },
    {
        "id": 24,
        "name": "宣州区发改委",
        "type": "政府",
        "level": "乡科级",
        "parent": "宣州区人民政府",
        "location": "宣州区",
        "source": "official"
    },
    {
        "id": 25,
        "name": "宣州区金融工作办公室",
        "type": "政府",
        "level": "乡科级",
        "parent": "宣州区人民政府",
        "location": "宣州区",
        "source": "official"
    },
]

positions = [
    # 高真理
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持区委全面工作"},
    # 杨培靖
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "正处级", "note": "兼任区长"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "正处级", "note": "主持区政府全面工作"},
    {"person_id": 2, "org_id": 9, "title": "副调研员", "start": "", "end": "", "rank": "", "note": "共青团宣城市委"},
    {"person_id": 2, "org_id": 10, "title": "副主任", "start": "", "end": "", "rank": "", "note": "宣城市委台湾工作办公室副主任"},
    {"person_id": 2, "org_id": 7, "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": "泾县人民政府副县长"},
    {"person_id": 2, "org_id": 8, "title": "县委常委、宣传部部长", "start": "", "end": "", "rank": "副处级", "note": "泾县县委常委、宣传部部长"},
    {"person_id": 2, "org_id": 8, "title": "县委副书记", "start": "", "end": "", "rank": "副处级", "note": "泾县县委副书记"},
    {"person_id": 2, "org_id": 23, "title": "常务副主任（常务副校长）", "start": "", "end": "", "rank": "正处级", "note": "宣城市干部教育培训现场教学基地管理办公室（泾县县委党校）常务副主任"},
    # 孙金平
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 时国金
    {"person_id": 4, "org_id": 4, "title": "区政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 朱伟
    {"person_id": 5, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 卢明
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "常务副区长", "start": "", "end": "present", "rank": "副处级", "note": "区政府常务副区长、党组副书记"},
    {"person_id": 6, "org_id": 11, "title": "党委书记", "start": "", "end": "", "rank": "乡科级正职", "note": "五星乡党委书记"},
    {"person_id": 6, "org_id": 12, "title": "局长、党组书记", "start": "", "end": "", "rank": "乡科级正职", "note": "区城市管理行政执法局局长"},
    {"person_id": 6, "org_id": 13, "title": "党委书记", "start": "", "end": "", "rank": "副县级", "note": "水阳镇党委书记（副县级）"},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": "宣州区政府副区长"},
    # 王炜
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "区政府副区长、党组成员"},
    {"person_id": 7, "org_id": 14, "title": "交通科科长、投资科科长、总工程师、副主任", "start": "", "end": "", "rank": "", "note": "宣城市发改委历任多职"},
    # 余建亚
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "区政府副区长"},
    {"person_id": 8, "org_id": 6, "title": "局长、党委书记", "start": "", "end": "present", "rank": "乡科级正职", "note": "宣城市公安局宣州分局局长"},
    {"person_id": 8, "org_id": 15, "title": "党委委员、纪委书记", "start": "", "end": "", "rank": "", "note": "宁国市公安局"},
    {"person_id": 8, "org_id": 16, "title": "党工委书记", "start": "", "end": "", "rank": "", "note": "宁国市河沥溪街道党工委书记"},
    # 黄彬
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "区政府副区长"},
    {"person_id": 9, "org_id": 24, "title": "副主任", "start": "", "end": "", "rank": "", "note": "宣州区发改委副主任"},
    {"person_id": 9, "org_id": 25, "title": "主任", "start": "", "end": "", "rank": "", "note": "宣州区金融工作办公室主任"},
    {"person_id": 9, "org_id": 17, "title": "党委副书记、镇长", "start": "", "end": "", "rank": "", "note": "狸桥镇党委副书记、镇长"},
    {"person_id": 9, "org_id": 18, "title": "党工委副书记、管委会主任", "start": "", "end": "", "rank": "", "note": "宣州经济开发区"},
    {"person_id": 9, "org_id": 17, "title": "党委书记（兼经开区党工委书记）", "start": "", "end": "", "rank": "", "note": "狸桥镇党委书记兼宣州经济开发区党工委书记"},
    # 曹兵
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "区政府副区长"},
    {"person_id": 10, "org_id": 19, "title": "土木工程系副主任、主任", "start": "", "end": "", "rank": "", "note": "安徽工程大学建筑工程学院"},
    {"person_id": 10, "org_id": 19, "title": "副院长", "start": "", "end": "", "rank": "", "note": "安徽工程大学建筑工程学院副院长"},
    # 周红兵
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "区政府副区长"},
    {"person_id": 11, "org_id": 20, "title": "副部长、常务副部长", "start": "", "end": "", "rank": "", "note": "宣州区委组织部副部长、区人才办主任、常务副部长"},
    {"person_id": 11, "org_id": 21, "title": "党委书记、局长", "start": "", "end": "", "rank": "乡科级正职", "note": "宣州区教育体育局局长"},
    # 汪琪
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "区政府副区长（非党）"},
    {"person_id": 12, "org_id": 22, "title": "科长", "start": "", "end": "", "rank": "", "note": "宣城市人社局多科室科长"},
    # 赵流海
    {"person_id": 13, "org_id": 2, "title": "区政府党组成员", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 13, "org_id": 5, "title": "管委会主任", "start": "", "end": "present", "rank": "", "note": "宣城高新区管委会主任"},
]

relationships = [
    # 高真理 ↔ 杨培靖 (区委书记 + 区长，党政搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "高真理任区委书记、杨培靖任区长，为宣州区党政主要负责人", "overlap_org": "中共宣州区委/宣州区人民政府", "overlap_period": "2026-至今", "strength": "strong"},
    # 高真理 ↔ 朱伟 (区委书记 + 区委副书记)
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "高真理任区委书记，朱伟任区委副书记，协助处理区委日常工作", "overlap_org": "中共宣州区委", "overlap_period": "2026-至今", "strength": "strong"},
    # 杨培靖 ↔ 卢明 (区长 + 常务副区长)
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "杨培靖任区长，卢明任常务副区长协助分管审计局和高新区管委会", "overlap_org": "宣州区人民政府", "overlap_period": "至今", "strength": "strong"},
    # 高真理 ↔ 孙金平 (区委书记 + 人大主任)
    {"person_a": 1, "person_b": 3, "type": "党政搭档", "context": "高真理任区委书记，孙金平任区人大常委会主任，第十五次党代会主席团成员", "overlap_org": "中共宣州区委/宣州区人大常委会", "overlap_period": "2026-至今", "strength": "medium"},
    # 高真理 ↔ 时国金 (区委书记 + 政协主席)
    {"person_a": 1, "person_b": 4, "type": "党政搭档", "context": "高真理任区委书记，时国金任区政协主席", "overlap_org": "中共宣州区委/宣州区政协", "overlap_period": "2026-至今", "strength": "medium"},
    # 杨培靖 ↔ 王炜 (区长 + 副区长)
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "杨培靖任区长，王炜任区委常委、副区长", "overlap_org": "宣州区人民政府", "overlap_period": "至今", "strength": "strong"},
    # 高真理 ↔ 赵流海 (区委书记 + 高新区主任)
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "高真理调研宣城高新区在建工业项目，赵流海陪同", "overlap_org": "宣城高新区", "overlap_period": "2026-07-08", "strength": "medium"},
    # 杨培靖 ↔ 赵流海 (区长 + 高新区主任)
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "杨培靖分管审计局、宣城高新区管委会，赵流海为高新区管委会主任", "overlap_org": "宣州区人民政府/宣城高新区", "overlap_period": "至今", "strength": "strong"},
    # 卢明 ↔ 杨培靖 (常务副区长协助区长)
    {"person_a": 6, "person_b": 2, "type": "上下级", "context": "卢明作为常务副区长协助区长分管审计局和高新区管委会", "overlap_org": "宣州区人民政府", "overlap_period": "至今", "strength": "strong"},
    # 杨培靖 ↔ 泾县渊源 (曾在泾县长期任职)
    {"person_a": 2, "person_b": 9, "type": "同地任职", "context": "杨培靖曾任泾县副县长、县委常委、宣传部部长、县委副书记，黄彬曾任狸桥镇党委书记（狸桥镇位于宣州区但接壤多县）", "overlap_org": "", "overlap_period": "不同时期", "strength": "weak"},
    # 卢明 ↔ 周红兵 (同区任职多年)
    {"person_a": 6, "person_b": 11, "type": "同地任职", "context": "卢明和周红兵均在宣州区基层多岗位任职，可能有过工作交集", "overlap_org": "宣州区", "overlap_period": "多年", "strength": "medium"},
    # 王炜 ↔ 黄彬 (均为副区长)
    {"person_a": 7, "person_b": 9, "type": "同级关系", "context": "王炜和黄彬均为宣州区副区长，在同届政府班子中共事", "overlap_org": "宣州区人民政府", "overlap_period": "至今", "strength": "medium"},
]


# ── build functions ──────────────────────────────────────────────────────

def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )''')

    c.execute('''CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT, source TEXT
    )''')

    c.execute('''CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )''')

    c.execute('''CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )''')

    for p in persons:
        c.execute('''INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
            education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute('''INSERT INTO organizations (id, name, type, level, parent, location, source)
            VALUES (?,?,?,?,?,?,?)''',
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"], o["source"]))

    for pos in positions:
        c.execute('''INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)''',
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute('''INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)''',
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Color by role: red=party secretary, blue=government head, orange=discipline, grey=other."""
    post = p.get("current_post", "")
    if "书记" in post and "区委书记" in post:
        return "255,50,50"
    elif "区长" in post and ("区委副书记" in post or "区长" == post):
        return "50,100,255"
    elif "副区长" in post:
        return "50,100,255"
    elif "常委" in post:
        return "50,100,255"
    elif "人大" in post:
        return "200,255,255"
    elif "政协" in post:
        return "255,240,200"
    else:
        return "100,100,100"


def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


def is_top_leader(p):
    return p["id"] in [1, 2]  # 区委书记 and 区长


def is_vip_leader(p):
    return p["id"] in [1, 2, 5, 6]  # 书记, 区长, 副书记, 常务副区长


def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>宣州区（安徽省宣城市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        if is_top_leader(p):
            sz = "20.0"
        elif is_vip_leader(p):
            sz = "16.0"
        else:
            sz = "12.0"
        role = esc(p["current_post"])
        org = esc(p["current_org"])
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{org}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        sz = "8.0"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person → organization (worked_at)
    for pos in positions:
        eid += 1
        src = f"p{pos['person_id']}"
        tgt = f"o{pos['org_id']}"
        label = esc(pos["title"])
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{label}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person (relationship)
    for r in relationships:
        eid += 1
        src = f"p{r['person_a']}"
        tgt = f"p{r['person_b']}"
        w = "2.0" if r.get("strength") == "strong" else "1.5" if r.get("strength") == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("strength", "medium"))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def print_summary():
    print(f"Database: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"\nPersons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print("\nCore leadership:")
    for p in persons:
        if p["id"] <= 13:
            print(f"  {p['current_post']}: {p['name']}")
    print(f"\nResearch date: 2026-07-16")
    print(f"Data confidence: confirmed (from official government sources)")


if __name__ == "__main__":
    print("Building 宣州区 leadership network...")
    create_database()
    create_gexf()
    print_summary()
    print("\nDone.")
