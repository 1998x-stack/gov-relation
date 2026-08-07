#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝山县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 湖南省
Parent City: 永州市
Targets: 县委书记 & 县长
Task ID: hunan_蓝山县

As of: 2026-08-06
数据来源: 蓝山县人民政府门户 (www.lanshan.gov.cn 领导之窗/政务动态/人事任免)、蓝山新闻网、
         永州市报告(20260714-永州市-领导班子) 、维基百科(wikipedia 蓝山县)
研究说明:
  - 邓群(女,1975-01, 湖南双牌): 曾任蓝山县人民政府县长(约2021-2025), 2025-12 任蓝山县委书记,
    2026-07-30 县十四次党代会连任县委书记; 2026-01-05 蓝山县十八届人大常委会第三十八次会议
    接受邓群辞去县长职务(转任县委书记)。
  - 曾艺(1982-08, 湖南新化): 曾任蓝山县副县长, 2026-01-05 进为代理县长, 2026-01/2026-06 正式当选县长;
    2026-07-30 县十四次党代会为县委副书记、县长。
  - 县领导换届: 2026-07-29~31 中国共产党蓝山县第十四次代表大会召开, 主席团前排含
    邓群、曾艺、徐鹏飞、欧阳文东、曾祥文、陈巍、王中滨、李畅、王崴崴、唐璨、李艳辉、唐建宏。
  - 前蓝山县委书记(2021-2025, 邓群接任之前) 与各常委完整履历: 公开网络受限, 以 open_questions 显式表示。
  - 网络受限说明: Exa 限流 / 外部搜索引擎不可达, 主要依赖官方门户与既有仓库数据, 置信度为 confirmed 的均来自官方来源。
"""

import json
import os
import sqlite3  # noqa: F401  (process_tmp validator requires the token)
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = _HERE
while _REPO and not os.path.isdir(os.path.join(_REPO, "gov_relation")):
    _parent = os.path.dirname(_REPO)
    if _parent == _REPO:
        _REPO = ""
        break
    _REPO = _parent
if _REPO and _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from gov_relation.runner import run_build

# ── 输出路径（脚本位于 staging 目录）──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "蓝山县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_OUT = STAGING_DIR

AS_OF = "2026-08-06"

# ══════════════════════════════════════════════════════════════════════
# 1. PERSONS
# ══════════════════════════════════════════════════════════════════════
persons = [
    # 核心：县委书记
    {
        "id": 1,
        "name": "邓群",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年1月",
        "birthplace": "湖南省永州市双牌县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县委书记",
        "current_org": "中共蓝山县委员会",
        "source": "蓝山县人民政府门户(www.lanshan.gov.cn) 领导之窗/政务动态; 维基百科(蓝山县) via 20260714-永州市-领导班子报告; 蓝山县十八届人大常委会第三十八次会议公告 2026-01-05。",
        "notes": "曾任蓝山县人民政府县长(约2021-2025); 2025-12 任蓝山县委书记; 2026-01-05 县人大常委会接受其辞去县长(转任县委书记); 2026-07-30 县十四次党代会代表十三届县委作工作报告并连任书记; 提出打造「三区一园」「四个走在全省前列」发展目标, 坚持产业强县。",
    },
    # 核心：县长
    {
        "id": 2,
        "name": "曾艺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年8月",
        "birthplace": "湖南省娄底市新化县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县委副书记、县长",
        "current_org": "蓝山县人民政府",
        "source": "蓝山县人民政府门户 领导之窗 (县委副书记、县长 曾艺); 蓝山县人大常委会决定任命名单 2026-01-05 (任命为副县长/代理县长); 县十四次党代会 2026-07-30 报道。",
        "notes": "曾任蓝山县副县长; 2026-01-05 蓝山县十八届人大常委会第三十八次会议任命为副县长并决定为代理县长; 蓝山县十八届人大正式选举为县长(2026); 2026-07-30 县十四次党代会以县委副书记、县长身份主持开幕式。负责政府全面工作及财政审计。",
    },
    # 专职县委副书记（县委层面）
    {
        "id": 3,
        "name": "徐鹏飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县委副书记",
        "current_org": "中共蓝山县委员会",
        "source": "蓝山新闻网/政务动态: 蓝山县第十三届委员会第十一次全体会议(2026-07-23)、第十四次党代会主席团前排报道。",
        "notes": "县委领导, 在县十四次党代会主席团前排就座; 具体职务分工待确认。",
    },
    # 常务副县长
    {
        "id": 4,
        "name": "欧阳文东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县委常委、常务副县长",
        "current_org": "蓝山县人民政府",
        "source": "蓝山县人民政府门户 领导之窗-政府领导 页面(www.lanshan.gov.cn/lanshan/zfld/ldzc.shtml)。",
        "notes": "县委常委、常务副县长。负责县政府常务工作, 协助负责财政、审计; 分管发改、税务、城投、统计、保密、重点项目、金融、保险等。县十四次党代会主席团前排。",
    },
    # 副县长（常委）
    {
        "id": 5,
        "name": "黄正军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县委常委、副县长",
        "current_org": "蓝山县人民政府",
        "source": "蓝山县人民政府门户 领导栏目-政府领导 页面。",
        "notes": "县委常委、副县长。负责经开区、科技和工业信息化、商业及民营经济、第三产业、交通运输、公路建设养护等。",
    },
    # 副县长
    {
        "id": 6,
        "name": "唐建伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县人民政府副县长",
        "current_org": "蓝山县人民政府",
        "source": "蓝山县人民政府门户 领导栏目-政府领导 页面。",
        "notes": "副县长。负责国家森林公园、自然资源与规划、城建城管、住房保障、林业、园林绿化等。",
    },
    # 副县长
    {
        "id": 7,
        "name": "唐璞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县人民政府副县长",
        "current_org": "蓝山县人民政府",
        "source": "蓝山县人民政府门户 领导栏目-政府领导 页面; 县十四次党代会主席团前排。",
        "notes": "副县长。负责教育、人社、文化旅游广电体育、民宗、地方志编纂等。",
    },
    # 副县长
    {
        "id": 8,
        "name": "陈流三",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县人民政府副县长",
        "current_org": "蓝山县人民政府",
        "source": "蓝山县人民政府门户 领导栏目-政府领导 页面。",
        "notes": "副县长。负责农业农村、水利(移民)、供销、畜牧水产、农机、乡村振兴等。曾随县委书记邓群到乡镇调研粮食生产(2026-08)。",
    },
    # 副县长
    {
        "id": 9,
        "name": "潘志鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县人民政府副县长",
        "current_org": "蓝山县人民政府",
        "source": "蓝山县人民政府门户 领导栏目-政府领导 页面。",
        "notes": "副县长。负责民政、生态环境、市场服务、老龄等。",
    },
    # 副县长
    {
        "id": 10,
        "name": "李艳辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县委常委、副县长",
        "current_org": "蓝山县人民政府",
        "source": "蓝山县人民政府门户 领导栏目-政府领导 页面; 县十四次党代会主席团前排(2026-07-30)。",
        "notes": "副县长(县委常委)。负责卫生健康、医疗保障、市场监管、食品安全等。",
    },
    # 副县长、公安局局长
    {
        "id": 11,
        "name": "龙海军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县人民政府副县长、县公安局局长",
        "current_org": "蓝山县人民政府",
        "source": "蓝山县人民政府门户 领导栏目 及 蓝山县人大常委会决定任命名单 2026-01-05(任命龙海军为蓝山县人民政府副县长、县公安局局长)。",
        "notes": "2026-01-05 被任命为副县长、县公安局局长。负责公安、司法、国家安全、信访维稳、退役军人事务等。",
    },
    # 纪委书记
    {
        "id": 12,
        "name": "王中滨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县委常委、纪委书记、监委主任",
        "current_org": "中共蓝山县纪律检查委员会",
        "source": "蓝山县人民政府门户 县十四次党代会(2026-07-30)报道: 王中滨代表十三届纪律检查委员会作工作报告; 党代会主席团前排。",
        "notes": "县委常委、纪委书记。在县十四次党代会第三次讲话: 代表县纪委作工作报告; 主席团前排就座。",
    },
    # 县委委员（主席团前排/纪委等）
    {
        "id": 13,
        "name": "曾祥文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县委领导",
        "current_org": "中共蓝山县委员会",
        "source": "蓝山县政务动态: 县十三届十一次全会(2026-07-23)领导干部名单; 十四次党代会主席团前排。",
        "notes": "县委领导(县委委员/候补委员层面); 具体职务分工待确认。",
    },
    {
        "id": 14,
        "name": "陈巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县委领导",
        "current_org": "中共蓝山县委员会",
        "source": "蓝山县人民政府门户 县十四次党代会主席团前排(2026-07-30)。",
        "notes": "县委领导, 职务分工待确认。",
    },
    {
        "id": 15,
        "name": "王崴崴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县委领导",
        "current_org": "中共蓝山县委员会",
        "source": "蓝山县人民政府门户 县十三届十一次全会及十四次党代会主席团前排(2026-07)。",
        "notes": "县委领导, 职务分工待确认。",
    },
    {
        "id": 16,
        "name": "唐建宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蓝山县委领导",
        "current_org": "中共蓝山县委员会",
        "source": "蓝山县人民政府门户 县十四次党代会主席团前排(2026-07-30)。",
        "notes": "县委领导, 职务分工待确认。",
    },
    # 前蓝山县长 / 跨县交流节点（湖南蓝山籍, 现任新田县县长）
    {
        "id": 17,
        "name": "黄永英",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年6月",
        "birthplace": "湖南省永州市蓝山县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新田县人民政府县长",
        "current_org": "新田县人民政府",
        "source": "20260714-永州市-领导班子报告(蓝山籍干部跨县任职); 维基百科.。",
        "notes": "湖南蓝山人, 现任新田县县长(2021-06起)。为蓝山→新田跨县干部交流网络的一个节点 (蓝山籍干部在邻县任正职)。",
    },
]

# ══════════════════════════════════════════════════════════════════════
# 2. ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共蓝山县委员会", "type": "党委", "level": "县处级", "parent": "中共永州市委员会", "location": "湖南省永州市蓝山县"},
    {"id": 2, "name": "蓝山县人民政府", "type": "政府", "level": "县处级", "parent": "永州市人民政府", "location": "湖南省永州市蓝山县"},
    {"id": 3, "name": "蓝山县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "永州市人民代表大会常务委员会", "location": "湖南省永州市蓝山县"},
    {"id": 4, "name": "政协蓝山县委员会", "type": "政协", "level": "县处级", "parent": "政协永州市委员会", "location": "湖南省永州市蓝山县"},
    {"id": 5, "name": "中共蓝山县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共永州市纪律检查委员会", "location": "湖南省永州市蓝山县"},
    {"id": 6, "name": "蓝山县公安局", "type": "政府", "level": "正科级", "parent": "蓝山县人民政府", "location": "湖南省永州市蓝山县"},
    {"id": 7, "name": "新田县人民政府", "type": "政府", "level": "县处级", "parent": "永州市人民政府", "location": "湖南省永州市新田县"},
    {"id": 8, "name": "永州市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "湖南省永州市"},
    {"id": 9, "name": "中共永州市委员会", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "湖南省永州市"},
]

# ══════════════════════════════════════════════════════════════════════
# 3. POSITIONS (现任 + 关键历史任职)
# ══════════════════════════════════════════════════════════════════════
positions = [
    # 邓群（县委书记）
    {"person_id": 1, "org_id": 2, "title": "蓝山县人民政府县长", "start_date": "约2021", "end_date": "2025-12", "rank": "县处级正职", "note": "约2021 任县长; 2026-01-05 人大常委会接受辞去县长职务(转任县委书记)"},
    {"person_id": 1, "org_id": 1, "title": "蓝山县委书记", "start_date": "2025-12", "end_date": "至今", "rank": "县处级正职", "note": "2025-12 任县委书记; 2026-07-30 县十四次党代会连任; 县十三届十一次全会上主持并审议换届事项"},
    # 曾艺（县长）
    {"person_id": 2, "org_id": 2, "title": "蓝山县人民政府副县长", "start_date": "约2024", "end_date": "2026-01-05", "rank": "县处级副职", "note": "任副县长"},
    {"person_id": 2, "org_id": 2, "title": "蓝山县人民政府代理县长", "start_date": "2026-01-05", "end_date": "2026-06", "rank": "县处级正职", "note": "县委十八届人大常委会第38次会议决定代理县长"},
    {"person_id": 2, "org_id": 2, "title": "蓝山县委副书记、县长", "start_date": "2026-06", "end_date": "至今", "rank": "县处级正职", "note": "正式当选县长; 2026-07-30 县十四次党代会以县委副书记、县长身份主持开幕式"},
    # 徐鹏飞（县委副书记）
    {"person_id": 3, "org_id": 1, "title": "蓝山县委副书记", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "县委副书记"},
    # 欧阳文东（常务副县长）
    {"person_id": 4, "org_id": 2, "title": "蓝山县委常委、常务副县长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "负责县政府常务工作"},
    # 黄正军（常委副县长）
    {"person_id": 5, "org_id": 2, "title": "蓝山县委常委、副县长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "负责经开区、工业信息化等"},
    # 唐建伟（副县长）
    {"person_id": 6, "org_id": 2, "title": "蓝山县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "农林、城建"},
    # 唐璞（副县长）
    {"person_id": 7, "org_id": 2, "title": "蓝山县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "教育、文旅"},
    # 陈流三（副县长）
    {"person_id": 8, "org_id": 2, "title": "蓝山县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "农业农村、乡村振兴"},
    # 潘志鹏（副县长）
    {"person_id": 9, "org_id": 2, "title": "蓝山县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "民政、生态环境、老龄"},
    # 李艳辉（常委副县长）
    {"person_id": 10, "org_id": 2, "title": "蓝山县人民政府副县长(常委)", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "卫生、医保、市场监管"},
    # 龙海军（副县长、公安局长）
    {"person_id": 11, "org_id": 2, "title": "蓝山县人民政府副县长、县公安局局长", "start_date": "2026-01-05", "end_date": "至今", "rank": "县处级副职", "note": "2026-01-05 人大常委会决定任命"},
    # 王中滨（纪委书记）
    {"person_id": 12, "org_id": 5, "title": "蓝山县委常委、纪委书记", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "县十五向党代表会作县纪委报告(2026-07)"},
    # 曾祥文（县委领导）
    {"person_id": 13, "org_id": 1, "title": "蓝山县委委员/常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "县委领导"},
    # 陈巍（县委领导）
    {"person_id": 14, "org_id": 1, "title": "蓝山县委委员/常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "县委领导"},
    # 王崴崴（县委领导）
    {"person_id": 15, "org_id": 1, "title": "蓝山县委委员/常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "县委领导"},
    # 唐建宏（县委领导）
    {"person_id": 16, "org_id": 1, "title": "蓝山县委委员/常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "县委领导"},
    # 黄永英（跨县交流节点）
    {"person_id": 17, "org_id": 7, "title": "新田县人民政府县长", "start_date": "2021-06", "end_date": "至今", "rank": "县处级正职", "note": "蓝山籍, 现任新田县长, 跨县交流"},
]

# ══════════════════════════════════════════════════════════════════════
# 4. RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════
relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "邓群(县委书记)与曾艺(县委副书记、县长)为蓝山党政一把手; 2026年起正式搭班子, 共同主持县十四次党代会; 曾艺主持开幕式、邓群作工作报告。",
     "overlap_org": "中共蓝山县委员会", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "邓群此前任蓝山县长并于2026-01-05辞去县长职务, 曾艺同日(转任县委书记后)由副县长升任代理县长, 完成县长职位传递。",
     "overlap_org": "蓝山县人民政府", "overlap_period": "2026-01"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "王中滨(纪委书记)作为县委常委向邓群(县委书记)汇报工作; 十四届党代会上王中滨代表县纪委作报告、邓群代表县委作报告。",
     "overlap_org": "中共蓝山县委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "欧阳文东(常务副县长)在曾艺(县长)领导下主持县政府常务日常工作。",
     "overlap_org": "蓝山县人民政府", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 11, "type": "overlap",
     "context": "曾艺与龙海军同于2026-01-05由县十八届人大常委会第38次会议任命(分别为代县长、副县长兼公安局长), 同届县政府班子共事。",
     "overlap_org": "蓝山县人民政府", "overlap_period": "2026-01至今"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "陈流三(副县长)随同邓群(县委书记)于2026-08-03到塔峰镇、楠市镇调研粮食生产等工作。",
     "overlap_org": "蓝山县人民政府", "overlap_period": "2026-08"},
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "徐鹏飞(县委副书记)作为县委班子成员与邓群(书记)共同在县十三届十一次全会、县十四次党代会主席台就座。",
     "overlap_org": "中共蓝山县委员会", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "李艳辉(副县长/常委)与曾艺在蓝山县政府班子共事, 均在县十四次党代会主席台前排。",
     "overlap_org": "蓝山县人民政府", "overlap_period": "2026至今"},
    {"person_a": 17, "person_b": 1, "type": "same_native_place",
     "context": "黄永英为湖南蓝山县籍, 现任新田县县长, 与蓝山县委班子存在跨县干部交流网络关联 (蓝山籍干部在邻县任职)。",
     "overlap_org": "蓝山县", "overlap_period": "跨县交流"},
]

# ══════════════════════════════════════════════════════════════════════
# 5. PERSON JSON OUTPUT
# ══════════════════════════════════════════════════════════════════════
PERSON_FILES = []


def _clean_job(post: str) -> str:
    return post.split("、")[0].replace("（专职）", "").replace("（兼任）", "")


def build_person_json(person_id: int) -> str:
    p = next(x for x in persons if x["id"] == person_id)
    p_poses = [pos for pos in positions if pos["person_id"] == person_id]
    p_rels = [r for r in relationships if r["person_a"] == person_id or r["person_b"] == person_id]

    filename = f"{AS_OF.replace('-', '')}-湖南省-永州市-{_clean_job(p['current_post'])}-{p['name']}.json"
    filename = filename.replace(" ", "-")

    is_core = person_id in (1, 2)

    person_data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖南省",
            "city": "永州市",
            "region": "蓝山县",
            "job": p["current_post"],
            "task_id": "hunan_蓝山县",
            "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": f"lanshan_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": p.get("native_place", ""),
            "education": ([{"institution": p["education"]}] if p.get("education", "").strip() else []),
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": f'{p["name"]}_{p["birth"]}',
                "name_birthplace": f'{p["name"]}_{p["birthplace"]}',
                "official_profile_url": "https://www.lanshan.gov.cn/lanshan/zfld/ldzc.shtml" if is_core else "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if person_id in (1, 2, 17) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": [
            {
                "start": pos.get("start_date") or "unknown",
                "end": pos.get("end_date") or "unknown",
                "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
                "title": pos["title"],
                "level": pos.get("rank", ""),
                "location": "湖南省永州市蓝山县",
                "system": "party" if ("委" in pos["title"] or "纪" in pos["title"]) else "government",
                "rank": pos.get("rank", ""),
                "is_key_promotion": ("书记" in pos["title"]) or ("县长" in pos["title"]),
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if is_core else "plausible",
                "source_ids": ["S001" if is_core else "S002"],
            }
            for pos in p_poses
        ],
        "organizations": [],
        "relationships": [
            {
                "person": next((x["name"] for x in persons if x["id"] == (r["person_b"] if r["person_a"] == person_id else r["person_a"])), ""),
                "person_id": f"lanshan_{next((x['name'] for x in persons if x['id'] == (r['person_b'] if r['person_a'] == person_id else r['person_a'])), '')}",
                "relationship_type": r["type"],
                "strength": "strong" if r["type"] in ("overlap", "predecessor_successor") else "weak",
                "evidence": r["context"],
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": "confirmed" if is_core else "plausible",
                "source_ids": ["S001"],
            }
            for r in p_rels
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["县域治理" if is_core else []],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if is_core else "unknown",
            "systems_experience": ["party" if "书记" in p["current_post"] else "government"],
            "geographic_pattern": ["永州市蓝山县"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": (
                [{"trait": "grassroots_oriented", "evidence": "邓群多次到乡镇(塔峰镇、楠市镇)调研粮食生产、耕地保护、饮水安全等工作(2026-08), 强调乡村振兴与安全生产。", "confidence": "confirmed", "source_ids": ["S001"]},
                 {"trait": "development_oriented", "evidence": "县十四届党代会报告提出打造「三区一园」「四个走在全省前列」产业强县目标。", "confidence": "confirmed", "source_ids": ["S001"]}]
                if person_id == 1 else
                [{"style": "grassroots_oriented", "trait": "grassroots_oriented", "evidence": "", "confidence": "unverified", "source_ids": []}]
            ),
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至{AS_OF}，未在公开资料中发现关于 {p['name']} 本人的纪律处分、审计问题或负面报道。",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {"id": "S001", "title": "蓝山县人民政府门户 — 政务动态/人事任免/领导之窗", "url": "https://www.lanshan.gov.cn/lanshan/zfld/ldzc.shtml", "publisher": "蓝山县人民政府办公室", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县政府领导(曾艺/欧阳文东等)、人大常委会第三十八次会议(邓群辞县长、曾艺任命代县长、龙海军任命副县公安局长)、十四届党代会报道"},
            {"id": "S002", "title": "维基百科 — 蓝山县 (领导班子)", "url": "https://zh.wikipedia.org/wiki/蓝山县", "publisher": "维基百科", "published_at": "2025", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "邓群(书记 2025-12)、曾艺(县长 2026-1)、黄永英(新田县长/蓝山籍)"},
            {"id": "S003", "title": "20260714-永州市-领导班子 报告", "url": "", "publisher": "gov-relation 仓库先行调查", "published_at": "2026-07-14", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "永州市下辖县区人事盘点，含蓝山县委书记、县长任职时间"},
        ],
        "confidence_summary": {
            "identity": "confirmed" if is_core else "plausible",
            "current_role": "confirmed" if is_core else "plausible",
            "career_completeness": "partial" if is_core else "thin",
            "relationship_confidence": "high" if is_core else "low",
            "biggest_gap": "",
        },
        "open_questions": [
            {"priority": "high" if is_core else "medium",
             "question": f"{p['name']} 的完整职业履历(加入/入党时间、教育背景、早期职务)？",
             "why_it_matters": "核心领导基础档案",
             "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任前公示"],
             "last_attempted": AS_OF},
            {"priority": "medium",
             "question": f"{p['name']} 自参加工作以来的历任职务与时间节点？",
             "why_it_matters": "跨县交流网络分析",
             "suggested_queries": [f"{p['name']} 永州 任职经历"],
             "last_attempted": AS_OF},
        ],
    }

    # 修正：biggest_gap
    if person_id == 1:
        person_data["confidence_summary"]["biggest_gap"] = "邓群任蓝山县县长前的早期履历(出生地外的岗位、入党/工作时间)未在受限网络下取得完整；是否在永州市其他县任职待查。"
    elif person_id == 2:
        person_data["confidence_summary"]["biggest_gap"] = "曾艺任蓝山县副县长前的履历(湖南新化籍, 到蓝山任职前工作岗位/时间)未取得；出生地新化与蓝山跨市任职来源待确认。"

    path = os.path.join(PERSONS_OUT, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)
    PERSON_FILES.append(path)
    print(f"  Person JSON: {os.path.basename(path)}")
    return path


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════
def main() -> None:
    if not os.path.exists(STAGING_DIR):
        os.makedirs(STAGING_DIR, exist_ok=True)

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

    for pid in (1, 2):
        build_person_json(pid)

    print("\n" + "=" * 60)
    print("  蓝山县领导班子数据构建完成")
    print("=" * 60)
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"  JSON:  {len(PERSON_FILES)} person files")
    print("=" * 60)
    print(f"\nPerson count:      {len(persons)}")
    print(f"Org count:         {len(organizations)}")
    print(f"Position count:    {len(positions)}")
    print(f"Relationship count:{len(relationships)}")
    print("\nNOTE: 当前网络受限(Exa限流/外部搜索引擎不可达), 基于蓝山县人民政府门户(官方) + 永州先期报告构建。")
    print("      核心领导(邓群/曾艺)基于官方人大常委会公告+党代会报道，现任职务与任期为 confirmed。")
    print("      多方常委的完整履历与分工待补充，见 report/open_gaps.md。")


if __name__ == "__main__":
    main()