#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贺兰县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 宁夏回族自治区
Parent City: 银川市
Region: 贺兰县
Targets: 县委书记 & 县长

Research Sources:
- 贺兰县人民政府网站 县委领导页 (www.nxhl.gov.cn/xxgk_7799/ldzc_73864/xwld_73865/)
- 贺兰县人民政府 常委会会议纪要 / 政府工作报告
- 澎湃新闻 任前公示 / 腾讯新闻 彭小沛履历
- 百度百科 杨爱军词条
- 银川市政协 贺兰县政协常委会会议

Research Date: 2026-08-07
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build  # noqa: E402

SLUG = "贺兰县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401, E402

# ── Data ──

# 1. Persons
persons = [
    # ── Current Top Leaders ──
    {
        "id": 1,
        "name": "杨爱军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年2月",
        "birthplace": "宁夏灵武",
        "native_place": "宁夏灵武",
        "education": "西北政法大学法律专业，大学学历（在职）",
        "party_join": "2000年6月",
        "work_start": "1997年7月",
        "current_post": "贺兰县委书记",
        "current_org": "中共贺兰县委员会",
        "source": "杨爱军，男，汉族，1974年2月出生，宁夏灵武人，2000年6月加入中国共产党，1997年7月参加工作，西北政法大学法律专业毕业，大学学历。现任贺兰县委书记、县人民武装部党委第一书记。2025年8月11日任贺兰县委书记，2025年9月任县人武部党委第一书记。来源：贺兰县人民政府县委领导页、百度百科。confidence=confirmed",
    },
    {
        "id": 2,
        "name": "彭小沛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "北京大学外国语学院英语系，学士+硕士",
        "party_join": "中共党员",
        "work_start": "约2012年",
        "current_post": "贺兰县委副书记、县长",
        "current_org": "贺兰县人民政府",
        "source": "彭小沛，男，汉族，1988年5月出生，硕士研究生学历，中共党员。2007年进入北京大学外国语学院英语系学习，获学士、硕士学位。毕业后赴宁夏工作。2025年3月14日被宣布提名贺兰县人民政府县长候选人（时任中卫市政府副秘书长、办公室主任）。来源：贺兰县人民政府、腾讯新闻、自治区党委组织部任前公示。confidence=confirmed",
    },
    {
        "id": 3,
        "name": "马小平",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1985年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "2010年9月",
        "current_post": "贺兰县委副书记、立岗镇党委书记",
        "current_org": "中共贺兰县委员会",
        "source": "马小平，男，回族，1985年11月出生，中共党员，研究生学历，2010年9月参加工作。现任贺兰县委常委、副书记，立岗镇党委书记，县委国家安全委员会办公室主任（兼）。协助县委书记分管党的建设工作。来源：贺兰县人民政府县委领导页。confidence=confirmed",
    },
    # ── 县委其他常委（现任班子）──
    {
        "id": 4,
        "name": "葸小明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺兰县委常委（挂职）、贺兰工业园区党工委副书记、管委会主任",
        "current_org": "宁夏贺兰工业园区",
        "source": "葸小明，现任贺兰县委常委（挂职）、宁夏贺兰工业园区党工委副书记、管委会主任。来源：贺兰县人民政府县委领导页。confidence=confirmed（身份）",
    },
    {
        "id": 5,
        "name": "唐健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺兰县委常委、政法委书记",
        "current_org": "中共贺兰县委员会",
        "source": "唐健，现任贺兰县委常委、政法委书记。来源：贺兰县人民政府县委领导名单。confidence=confirmed（身份）",
    },
    {
        "id": 6,
        "name": "王君",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1978年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "宁夏党校研究生",
        "party_join": "中共党员",
        "work_start": "1999年7月",
        "current_post": "贺兰县委常委、纪委书记、监察委员会主任",
        "current_org": "中共贺兰县纪律检查委员会",
        "source": "王君，男，回族，1978年5月出生，中共党员，宁夏党校研究生，1999年7月参加工作。现任贺兰县委常委、纪委书记，监察委员会主任。主持县纪检监察、党风廉政建设和反腐败、巡察工作。来源：贺兰县人民政府县委领导页。confidence=confirmed",
    },
    {
        "id": 7,
        "name": "王鉴之",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "宁夏党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺兰县委常委、宣传部部长",
        "current_org": "中共贺兰县委员会",
        "source": "王鉴之，女，汉族，1980年4月生，中共党员，宁夏党校研究生学历。现任贺兰县委常委、宣传部部长。来源：贺兰县人民政府县委领导页。confidence=confirmed",
    },
    {
        "id": 8,
        "name": "张楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2010年9月",
        "current_post": "贺兰县委常委、组织部部长",
        "current_org": "中共贺兰县委员会",
        "source": "张楠，男，汉族，1986年8月出生，中共党员，大学学历，2010年9月参加工作。现任贺兰县委常委、组织部部长，县直机关工委委员、书记，县委党校（行政学校）校长。来源：贺兰县人民政府县委领导页。confidence=confirmed",
    },
    {
        "id": 9,
        "name": "蒋伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺兰县委常委、常务副县长",
        "current_org": "贺兰县人民政府",
        "source": "蒋伟，男，汉族，1978年12月出生，中共党员，在职大学学历。现任贺兰县委常委、县人民政府常务副县长。来源：贺兰县人民政府县委领导页。confidence=confirmed",
    },
    {
        "id": 10,
        "name": "丁尧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺兰县委常委、统战部部长",
        "current_org": "中共贺兰县委员会",
        "source": "丁尧，现任贺兰县委常委、统战部部长。来源：贺兰县人民政府县委领导名单。confidence=confirmed（身份）",
    },
    {
        "id": 11,
        "name": "陆成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺兰县委常委、副县长",
        "current_org": "贺兰县人民政府",
        "source": "陆成，男，汉族，1983年11月出生，中共党员，大学学历。现任贺兰县委常委、县人民政府副县长。来源：贺兰县人民政府县委领导页。confidence=confirmed",
    },
    {
        "id": 12,
        "name": "杨振苗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺兰县委常委、副县长（挂职）",
        "current_org": "贺兰县人民政府",
        "source": "杨振苗，现任贺兰县委常委、副县长（挂职）。来源：贺兰县人民政府县委领导名单。confidence=confirmed（身份）",
    },
    # ── 人大 / 政协 ──
    {
        "id": 13,
        "name": "田晓波",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺兰县人大常委会主任",
        "current_org": "贺兰县人大常委会",
        "source": "田晓波，现任贺兰县人大常委会主任，多次列席县委常委会并出席春节走访慰问。来源：贺兰县人民政府新闻、常委会纪要。confidence=confirmed",
    },
    {
        "id": 14,
        "name": "陆斌",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺兰县政协主席",
        "current_org": "贺兰县政协",
        "source": "陆斌，现任贺兰县政协主席（县政协党组书记）。2026年3月26日主持政协第十一届贺兰县委员会第二十七次常委会会议。来源：银川市政协网站、贺兰县人民政府新闻。confidence=confirmed",
    },
    # ── 前任领导 ──
    {
        "id": 20,
        "name": "丁炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "银川市人大常委会副主任（原贺兰县委书记）",
        "current_org": "银川市人大常委会",
        "source": "丁炜，曾任银川市人大常委会副主任、贺兰县委书记。2025年8月11日不再担任贺兰县委书记，由杨爱军接替。来源：县人民政府新闻、澎湃新闻。confidence=confirmed（前职）",
    },
    {
        "id": 21,
        "name": "刘炳炳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原贺兰县委副书记、县长）",
        "current_org": "",
        "source": "刘炳炳，曾任贺兰县委副书记、县长（2023年8月时在任）。2025年初由彭小沛接替。2024年2月县政府领导分工通知显示刘炳炳为主持政府全面工作的县长。来源：贺兰县人民政府政府领导分工通知。confidence=confirmed",
    },
    # ── 曾担任县政府副职（工作分工证据）──
    {
        "id": 30,
        "name": "段建宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原贺兰县委常委、常务副县长）",
        "current_org": "",
        "source": "段建宏，曾任贺兰县委常委、县政府常务副县长（2022年12月县级河长分工、2024年县政府领导分工）。后由蒋伟接替常务副县长。来源：贺兰县人民政府河湖长、政府领导分工通知。confidence=confirmed",
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共贺兰县委员会", "type": "党委", "level": "县级", "parent": "中共银川市委", "location": "宁夏回族自治区银川市贺兰县"},
    {"id": 2, "name": "贺兰县人民政府", "type": "政府", "level": "县级", "parent": "银川市人民政府", "location": "宁夏回族自治区银川市贺兰县"},
    {"id": 3, "name": "贺兰县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "宁夏回族自治区银川市贺兰县"},
    {"id": 4, "name": "贺兰县政协", "type": "政协", "level": "县级", "parent": "", "location": "宁夏回族自治区银川市贺兰县"},
    {"id": 5, "name": "中共贺兰县纪律检查委员会", "type": "党委", "level": "县级", "parent": "银川市纪委监委", "location": "宁夏回族自治区银川市贺兰县"},
    {"id": 6, "name": "宁夏贺兰工业园区", "type": "开发区", "level": "县级", "parent": "", "location": "宁夏回族自治区银川市贺兰县"},
    {"id": 7, "name": "立岗镇", "type": "乡镇/街道", "level": "乡镇", "parent": "贺兰县人民政府", "location": "宁夏回族自治区银川市贺兰县"},
    {"id": 8, "name": "银川市人大常委会", "type": "人大", "level": "地级市", "parent": "宁夏回族自治区人大常委会", "location": "宁夏回族自治区银川市"},
    {"id": 9, "name": "银川市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共银川市委", "location": "宁夏回族自治区银川市"},
    {"id": 10, "name": "中卫市人民政府", "type": "政府", "level": "地级市", "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区中卫市"},
    {"id": 11, "name": "中宁县人民政府", "type": "政府", "level": "县级", "parent": "中卫市人民政府", "location": "宁夏回族自治区中卫市中宁县"},
    {"id": 12, "name": "中共中宁县委员会", "type": "党委", "level": "县级", "parent": "中共中卫市委", "location": "宁夏回族自治区中卫市中宁县"},
    {"id": 13, "name": "中共沙坡头区委员会", "type": "党委", "level": "县级", "parent": "中共中卫市委", "location": "宁夏回族自治区中卫市沙坡头区"},
    {"id": 14, "name": "银川市人民政府", "type": "政府", "level": "地级市", "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区银川市"},
]

# 3. Positions
positions = [
    # ── 现任领导 ──
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2025年8月", "end_date": "至今", "rank": "正处级", "note": "2025年8月11日宣布任贺兰县委书记，接替丁炜"},
    {"person_id": 1, "org_id": 9, "title": "银川市监察委员会副主任", "start_date": "2021年9月", "end_date": "2022年12月", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "银川市纪委监委纪检监察办公室主任", "start_date": "待查", "end_date": "待查", "rank": "", "note": "历任银川市纪委办公室主任"},
    {"person_id": 1, "org_id": 14, "title": "银川市司法局局长", "start_date": "2022年12月", "end_date": "2024年4月", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "银川市审批服务管理局局长", "start_date": "2024年4月", "end_date": "2025年8月", "rank": "正处级", "note": "2025年8月25日银川市人大常委会免去该职"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2025年", "end_date": "至今", "rank": "正处级", "note": "2025年3月提名县长候选人，后任代县长、县长"},
    {"person_id": 2, "org_id": 10, "title": "中卫市政府副秘书长、办公室主任", "start_date": "2024年6月", "end_date": "2025年3月", "rank": "正处级", "note": "机关党组书记"},
    {"person_id": 2, "org_id": 12, "title": "中宁县委副书记", "start_date": "2023年", "end_date": "2024年6月", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "中宁县常委、常务副县长", "start_date": "2022年1月", "end_date": "2023年", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 13, "title": "沙坡头区常委、组织部部长", "start_date": "2021年", "end_date": "2022年1月", "rank": "副处级", "note": "2021年4月区/县党委常委、组织部部长任前公示"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "2025年多次以县委副书记身份出席常委会"},
    {"person_id": 3, "org_id": 7, "title": "立岗镇党委书记", "start_date": "待查", "end_date": "至今", "rank": "正科级", "note": "兼任"},
    {"person_id": 4, "org_id": 6, "title": "贺兰工业园区党工委副书记、管委会主任", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "县委常委（挂职）"},
    {"person_id": 5, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "县委常委、纪委书记、监委主任", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "接替段建宏"},
    {"person_id": 10, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "县委常委、副县长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "县委常委、副县长（挂职）", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "县人大常委会主任", "start_date": "待查", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 4, "title": "县政协主席", "start_date": "2024年", "end_date": "至今", "rank": "正处级", "note": "接替张魁"},
    # ── 前任领导 ──
    {"person_id": 20, "org_id": 1, "title": "县委书记", "start_date": "待查", "end_date": "2025年8月", "rank": "正处级", "note": "兼任银川市人大常委会副主任，2025年8月不再担任"},
    {"person_id": 21, "org_id": 2, "title": "县长", "start_date": "待查", "end_date": "2025年", "rank": "正处级", "note": "2025年由彭小沛接替"},
    {"person_id": 30, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "待查", "end_date": "待查", "rank": "副处级", "note": "2022-2024年在任，后由蒋伟接替"},
]

# 4. Relationships
relationships = [
    # 现任班子核心
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长，党政主要领导工作搭档", "overlap_org": "贺兰县委/县政府", "overlap_period": "2025年3月至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与县委副书记（分管党建）", "overlap_org": "中共贺兰县委员会", "overlap_period": "2025年至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "贺兰县人民政府", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委常委会班子成员（书记与纪委书记）", "overlap_org": "中共贺兰县委员会", "overlap_period": "2025年至今"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委常委会班子成员（书记与组织部长）", "overlap_org": "中共贺兰县委员会", "overlap_period": "2025年至今"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "县委书记与县人大常委会主任", "overlap_org": "贺兰县", "overlap_period": "2025年至今"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "县委书记与县政协主席", "overlap_org": "贺兰县", "overlap_period": "2025年至今"},
    # 前任-现任 交接
    {"person_a": 20, "person_b": 1, "type": "predecessor_successor", "context": "丁炜前任县委书记，杨爱军接替", "overlap_org": "中共贺兰县委员会", "overlap_period": "2025年8月交接"},
    {"person_a": 21, "person_b": 2, "type": "predecessor_successor", "context": "刘炳炳前任县长，彭小沛接替", "overlap_org": "贺兰县人民政府", "overlap_period": "2025年交接"},
    {"person_a": 30, "person_b": 9, "type": "predecessor_successor", "context": "段建宏前任常务副县长，蒋伟接替", "overlap_org": "贺兰县人民政府", "overlap_period": "待查"},
    # 前任搭档关系
    {"person_a": 20, "person_b": 21, "type": "overlap", "context": "丁炜任县委书记期间，刘炳炳任县长搭档", "overlap_org": "贺兰县委/县政府", "overlap_period": "2023-2024年"},
]

# ── Build ──
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

import sqlite3
conn = sqlite3.connect(DB_PATH)
cur = conn.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur = conn.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur = conn.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur = conn.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]
conn.close()

print(f"\n✅ {SLUG} build complete!")
print(f"   Persons:       {person_count}")
print(f"   Organizations: {org_count}")
print(f"   Positions:     {pos_count}")
print(f"   Relationships: {rel_count}")
print(f"   DB: {DB_PATH}")
print(f"   GEXF: {GEXF_PATH}")