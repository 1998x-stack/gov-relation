#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 永泰县 (Yongtai County, Fuzhou, Fujian).

Task: fujian_永泰县 — 县委书记 & 县长
Province: 福建省
City: 福州市
Region: 永泰县
Level: 县
Research date: 2026-07-16

Confirmed officeholders (as of 2026-07-16):
- 县委书记: 刘广辉 (appointed 2026-07-02, succeeded 陈金友)
- 代县长: 林吓清 (appointed 2026-07-08, succeeded 苏冰)

Sources:
- 大美永泰 (永泰县融媒体中心) — 2026-07-02
- 百度百科 — 刘广辉词条, 林吓清词条
- 福州新闻网 — 永泰县领导干部大会报道
- 福建省委组织部任前公示 — 2023-12
- 永泰县人民政府官网
- 网易新闻 — 福建4位代县长上任
- 鲁网 (福建省委组织部公示)
- 鲁中晨报 — 陈建新任职

Confidence: Current leadership confirmed from multiple official/news sources.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING = SCRIPT_DIR
DB_PATH = os.path.join(STAGING, "永泰县_network.db")
GEXF_PATH = os.path.join(STAGING, "永泰县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 县委书记 — 刘广辉
    {
        "id": "yongtai_liu_guanghui",
        "name": "刘广辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年10月",
        "birthplace": "福建闽清",
        "native_place": "福建闽清",
        "education": "大学",
        "party_join": "2001年11月",
        "work_start": "1991年12月",
        "current_post": "永泰县委书记",
        "current_org": "中共永泰县委员会",
        "source": "百度百科（刘广辉词条）; 大美永泰（永泰县融媒体中心, 2026-07-02）",
        "notes": "2026年7月2日起任永泰县委书记、县人武部党委第一书记。前任：福州市台江区委副书记、区长（2021年12月—2026年6月）。早期在福州市政府外事办公室工作。",
        "confidence": "confirmed",
    },

    # 代县长 — 林吓清
    {
        "id": "yongtai_lin_xiaqing",
        "name": "林吓清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年7月",
        "birthplace": "福建平潭",
        "native_place": "福建平潭",
        "education": "在职研究生，公共管理硕士",
        "party_join": "2003年10月",
        "work_start": "2005年7月",
        "current_post": "永泰县委副书记、代县长",
        "current_org": "永泰县人民政府",
        "source": "百度百科（林吓清词条）; 永泰县融媒体中心（2026-07-08）; 网易新闻（福建4位代县长上任）",
        "notes": "2026年7月8日起任永泰县委副书记、代县长。前任职务：连江县委副书记、福州市委办公厅综合处处长、福州市委深改办副主任。",
        "confidence": "confirmed",
    },

    # 前县委书记 — 陈金友
    {
        "id": "yongtai_chen_jinyou",
        "name": "陈金友",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "福建莆田",
        "native_place": "福建莆田",
        "education": "研究生学历，法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任永泰县委书记（已调离）",
        "current_org": "（调离，去向待确认）",
        "source": "福州新闻网（永泰县领导干部大会报道, 2023-12-29）; 福建省委组织部任前公示（2020年12月）; 汲古新知",
        "notes": "2023年12月29日任永泰县委书记，接替雷连鸣（二者职务对调）。此前任永泰县长（约2016年—2023年12月）。更早：福州市信访局党组书记、局长兼市政府副秘书长，福清市委常委，福州市政府办公厅系统，福建省公安厅刑警总队副科长。2026年6月/7月卸任县委书记，去向待确认。",
        "confidence": "confirmed",
    },

    # 前县长 — 苏冰
    {
        "id": "yongtai_su_bing",
        "name": "苏冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年7月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任永泰县长（已调离）",
        "current_org": "（调离，去向待确认）",
        "source": "永泰县人民政府官网; 福州新闻网（2023-12-29）; 永泰县人大会议报道（2023-12-31）",
        "notes": "2023年12月29日提名为永泰县长候选人，2023年12月31日当选县长。此前任永泰县委副书记（正处长级）、洑口乡党委书记。2026年7月卸任县长，去向待确认。",
        "confidence": "confirmed",
    },

    # 前县委书记 — 雷连鸣
    {
        "id": "yongtai_lei_lianming",
        "name": "雷连鸣",
        "gender": "男",
        "ethnicity": "畲族",
        "birth": "1983年8月",
        "birthplace": "福建福安",
        "native_place": "福建福安",
        "education": "研究生学历，法学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任永泰县委书记（已调任设区市副职）",
        "current_org": "（调任设区市党政副职）",
        "source": "鲁网（福建省委组织部公示, 2023-12-11）; 福建省委组织部任前公示",
        "notes": "先后毕业于厦门大学、清华大学。曾任二十四届全国学联副主席、清华大学研究生团委副书记（正科级）。约2016年前后任永泰县长，约2019/2020年任永泰县委书记。2023年12月省委组织部公示拟任设区市党政副职。'80后'少数民族（畲族）干部。",
        "confidence": "confirmed",
    },

    # ══════════════ Leadership Team ══════════════

    # 县委副书记 — 潘福全
    {
        "id": "yongtai_pan_fuquan",
        "name": "潘福全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县委副书记",
        "current_org": "中共永泰县委员会",
        "source": "永泰县人民政府官网（2025年2月会议）",
        "notes": "在2025年2月永泰县会议中出现。",
        "confidence": "confirmed",
    },

    # 县委常委、县人武部上校部长 — 颜建伟
    {
        "id": "yongtai_yan_jianwei",
        "name": "颜建伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县委常委、县人武部上校部长",
        "current_org": "永泰县人武部",
        "source": "百度百科（中国共产党永泰县委员会词条）",
        "notes": "",
        "confidence": "confirmed",
    },

    # 县委常委、纪委书记 — 肖小英
    {
        "id": "yongtai_xiao_xiaoying",
        "name": "肖小英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县委常委、县纪委书记、县监委主任",
        "current_org": "永泰县纪委监委",
        "source": "百度百科（中国共产党永泰县委员会词条）",
        "notes": "",
        "confidence": "confirmed",
    },

    # 县委常委、组织部部长 — 林文峰
    {
        "id": "yongtai_lin_wenfeng",
        "name": "林文峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县委常委、组织部部长",
        "current_org": "永泰县委组织部",
        "source": "永泰县人民政府官网",
        "notes": "兼县委党校校长。",
        "confidence": "confirmed",
    },

    # 县委常委 — 柯永华
    {
        "id": "yongtai_ke_yonghua",
        "name": "柯永华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县委常委",
        "current_org": "中共永泰县委员会",
        "source": "永泰县人民政府官网（2025年2月会议）",
        "notes": "",
        "confidence": "confirmed",
    },

    # 县委常委 — 张国淼
    {
        "id": "yongtai_zhang_guomiao",
        "name": "张国淼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县委常委",
        "current_org": "中共永泰县委员会",
        "source": "永泰县人民政府官网",
        "notes": "",
        "confidence": "confirmed",
    },

    # 县委常委 — 李志专
    {
        "id": "yongtai_li_zhizhuan",
        "name": "李志专",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县委常委",
        "current_org": "中共永泰县委员会",
        "source": "永泰县政府官网（2026年7月会议）",
        "notes": "",
        "confidence": "confirmed",
    },

    # 县委常委 — 郑晓红
    {
        "id": "yongtai_zheng_xiaohong",
        "name": "郑晓红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县委常委",
        "current_org": "中共永泰县委员会",
        "source": "永泰县人民政府官网",
        "notes": "",
        "confidence": "confirmed",
    },

    # 县委常委 — 陈祥富
    {
        "id": "yongtai_chen_xiangfu",
        "name": "陈祥富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县委常委",
        "current_org": "中共永泰县委员会",
        "source": "永泰县人民政府官网",
        "notes": "",
        "confidence": "confirmed",
    },

    # 县委常委、副县长（常务）— 游海涛
    {
        "id": "yongtai_you_haitao",
        "name": "游海涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县委常委、副县长（常务）",
        "current_org": "永泰县人民政府",
        "source": "永泰县人民政府官网",
        "notes": "负责县政府常务工作。",
        "confidence": "confirmed",
    },

    # 县委常委、政法委书记 — 陈建新
    {
        "id": "yongtai_chen_jianxin",
        "name": "陈建新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年6月",
        "birthplace": "福建平潭",
        "native_place": "福建平潭",
        "education": "大学，法律硕士",
        "party_join": "2003年12月",
        "work_start": "1999年12月",
        "current_post": "永泰县委常委、政法委书记",
        "current_org": "永泰县委政法委",
        "source": "鲁中晨报",
        "notes": "2025年5月到任。此前任福州市司法局副局长。与林吓清同为福建平潭人。",
        "confidence": "confirmed",
    },

    # ══════════════ County Government Members ══════════════

    # 副县长 — 张卫忠
    {
        "id": "yongtai_zhang_weizhong",
        "name": "张卫忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县副县长",
        "current_org": "永泰县人民政府",
        "source": "永泰县人民政府官网（2026年7月会议）",
        "notes": "",
        "confidence": "confirmed",
    },

    # 副县长 — 刘漪
    {
        "id": "yongtai_liu_yi",
        "name": "刘漪",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县副县长",
        "current_org": "永泰县人民政府",
        "source": "永泰县人民政府官网（2026年7月会议）",
        "notes": "",
        "confidence": "confirmed",
    },

    # 副县长 — 方惠忠
    {
        "id": "yongtai_fang_huizhong",
        "name": "方惠忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县副县长",
        "current_org": "永泰县人民政府",
        "source": "永泰县人民政府官网（2026年7月会议）",
        "notes": "",
        "confidence": "confirmed",
    },

    # 副县长 — 陈军
    {
        "id": "yongtai_chen_jun",
        "name": "陈军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县副县长",
        "current_org": "永泰县人民政府",
        "source": "永泰县人民政府官网（2026年7月会议）",
        "notes": "",
        "confidence": "confirmed",
    },

    # 副县长 — 叶俊忠
    {
        "id": "yongtai_ye_junzhong",
        "name": "叶俊忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永泰县副县长",
        "current_org": "永泰县人民政府",
        "source": "永泰县人民政府官网（2026年7月会议）",
        "notes": "",
        "confidence": "confirmed",
    },
]

organizations = [
    {
        "id": "org_yongtai_cpc",
        "name": "中国共产党永泰县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "福州市委",
        "location": "福州市永泰县",
    },
    {
        "id": "org_yongtai_gov",
        "name": "永泰县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "福州市政府",
        "location": "福州市永泰县",
    },
    {
        "id": "org_yongtai_cdc",
        "name": "永泰县纪委监委",
        "type": "纪委",
        "level": "县级",
        "parent": "福州市纪委监委",
        "location": "福州市永泰县",
    },
    {
        "id": "org_yongtai_odb",
        "name": "永泰县人武部",
        "type": "军事",
        "level": "县级",
        "parent": "福州警备区",
        "location": "福州市永泰县",
    },
    {
        "id": "org_yongtai_org",
        "name": "永泰县委组织部",
        "type": "党委部门",
        "level": "县级",
        "parent": "永泰县委",
        "location": "福州市永泰县",
    },
    {
        "id": "org_yongtai_police",
        "name": "永泰县委政法委",
        "type": "党委部门",
        "level": "县级",
        "parent": "永泰县委",
        "location": "福州市永泰县",
    },
    {
        "id": "org_taijiang_gov",
        "name": "福州市台江区人民政府",
        "type": "政府",
        "level": "区级",
        "parent": "福州市政府",
        "location": "福州市台江区",
    },
    {
        "id": "org_lianjiang_cpc",
        "name": "中国共产党连江县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "福州市委",
        "location": "福州市连江县",
    },
    {
        "id": "org_fuzhou_cpc",
        "name": "中国共产党福州市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "福建省委",
        "location": "福州市",
    },
    {
        "id": "org_fuzhou_gov",
        "name": "福州市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "福建省",
        "location": "福州市",
    },
    {
        "id": "org_fujian_gat",
        "name": "福建省公安厅",
        "type": "政府",
        "level": "省级",
        "parent": "福建省",
        "location": "福州市",
    },
    {
        "id": "org_fuzhou_bgt",
        "name": "福州市委办公厅",
        "type": "党委部门",
        "level": "地市级",
        "parent": "福州市委",
        "location": "福州市",
    },
]

positions = [
    # 刘广辉
    {
        "person_id": "yongtai_liu_guanghui",
        "org_id": "org_yongtai_cpc",
        "title": "永泰县委书记",
        "start": "2026年7月",
        "end": "至今",
        "rank": "正处级",
        "note": "2026年7月2日起任职。兼县人武部党委第一书记。",
    },
    {
        "person_id": "yongtai_liu_guanghui",
        "org_id": "org_taijiang_gov",
        "title": "福州市台江区委副书记、区长",
        "start": "2021年12月",
        "end": "2026年6月",
        "rank": "正处级",
        "note": "上任前职务。",
    },
    # 林吓清
    {
        "person_id": "yongtai_lin_xiaqing",
        "org_id": "org_yongtai_gov",
        "title": "永泰县委副书记、代县长",
        "start": "2026年7月",
        "end": "至今",
        "rank": "正处级",
        "note": "2026年7月8日起以代县长身份公开亮相。",
    },
    {
        "person_id": "yongtai_lin_xiaqing",
        "org_id": "org_lianjiang_cpc",
        "title": "连江县委副书记",
        "start": "",
        "end": "2026年7月",
        "rank": "副处级",
        "note": "前任职务。",
    },
    {
        "person_id": "yongtai_lin_xiaqing",
        "org_id": "org_fuzhou_bgt",
        "title": "福州市委办公厅综合处处长",
        "start": "",
        "end": "",
        "rank": "正科级",
        "note": "早期职务。",
    },
    # 陈金友
    {
        "person_id": "yongtai_chen_jinyou",
        "org_id": "org_yongtai_cpc",
        "title": "永泰县委书记",
        "start": "2023年12月",
        "end": "2026年6月",
        "rank": "正处级",
        "note": "接替雷连鸣。",
    },
    {
        "person_id": "yongtai_chen_jinyou",
        "org_id": "org_yongtai_gov",
        "title": "永泰县长",
        "start": "约2016年",
        "end": "2023年12月",
        "rank": "正处级",
        "note": "后升任县委书记。",
    },
    {
        "person_id": "yongtai_chen_jinyou",
        "org_id": "org_fujian_gat",
        "title": "福建省公安厅刑警总队副科长",
        "start": "",
        "end": "",
        "rank": "",
        "note": "早期职务。",
    },
    # 苏冰
    {
        "person_id": "yongtai_su_bing",
        "org_id": "org_yongtai_gov",
        "title": "永泰县委副书记、县长",
        "start": "2023年12月",
        "end": "2026年7月",
        "rank": "正处级",
        "note": "",
    },
    # 雷连鸣
    {
        "person_id": "yongtai_lei_lianming",
        "org_id": "org_yongtai_cpc",
        "title": "永泰县委书记",
        "start": "约2019年",
        "end": "2023年12月",
        "rank": "正处级",
        "note": "",
    },
    {
        "person_id": "yongtai_lei_lianming",
        "org_id": "org_yongtai_gov",
        "title": "永泰县长",
        "start": "约2016年",
        "end": "约2019年",
        "rank": "正处级",
        "note": "",
    },
    # 潘福全
    {
        "person_id": "yongtai_pan_fuquan",
        "org_id": "org_yongtai_cpc",
        "title": "永泰县委副书记",
        "start": "",
        "end": "至今",
        "rank": "副处级",
        "note": "",
    },
    # 颜建伟
    {
        "person_id": "yongtai_yan_jianwei",
        "org_id": "org_yongtai_odb",
        "title": "永泰县委常委、县人武部上校部长",
        "start": "",
        "end": "至今",
        "rank": "正团级",
        "note": "",
    },
    # 肖小英
    {
        "person_id": "yongtai_xiao_xiaoying",
        "org_id": "org_yongtai_cdc",
        "title": "永泰县委常委、县纪委书记、县监委主任",
        "start": "",
        "end": "至今",
        "rank": "副处级",
        "note": "",
    },
    # 林文峰
    {
        "person_id": "yongtai_lin_wenfeng",
        "org_id": "org_yongtai_org",
        "title": "永泰县委常委、组织部部长",
        "start": "",
        "end": "至今",
        "rank": "副处级",
        "note": "兼县委党校校长。",
    },
    # 陈建新
    {
        "person_id": "yongtai_chen_jianxin",
        "org_id": "org_yongtai_police",
        "title": "永泰县委常委、政法委书记",
        "start": "2025年5月",
        "end": "至今",
        "rank": "副处级",
        "note": "此前任福州市司法局副局长。",
    },
    # 游海涛
    {
        "person_id": "yongtai_you_haitao",
        "org_id": "org_yongtai_gov",
        "title": "永泰县委常委、副县长（常务）",
        "start": "",
        "end": "至今",
        "rank": "副处级",
        "note": "",
    },
]

relationships = [
    # Current leadership duo
    {
        "person_a": "yongtai_liu_guanghui",
        "person_b": "yongtai_lin_xiaqing",
        "type": "direct_coworker",
        "context": "新县委书记与新代县长搭档",
        "overlap_org": "永泰县委/永泰县政府",
        "overlap_period": "2026年7月至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # Previous leadership duo
    {
        "person_a": "yongtai_chen_jinyou",
        "person_b": "yongtai_su_bing",
        "type": "direct_coworker",
        "context": "前县委书记与前县长搭档",
        "overlap_org": "永泰县委/永泰县政府",
        "overlap_period": "2023年12月—2026年6月",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # Role swap: 陈金友 ↔ 雷连鸣
    {
        "person_a": "yongtai_lei_lianming",
        "person_b": "yongtai_chen_jinyou",
        "type": "succession",
        "context": "雷连鸣曾为永泰县委书记（约2019-2023），陈金友为其县长（2016-2023），后职务对调，陈金友接任书记",
        "overlap_org": "永泰县",
        "overlap_period": "约2016年—2023年12月",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 林吓清 ↔ 陈建新 (townsman)
    {
        "person_a": "yongtai_lin_xiaqing",
        "person_b": "yongtai_chen_jianxin",
        "type": "townsman",
        "context": "同为福建平潭人",
        "overlap_org": "平潭乡缘",
        "overlap_period": "长期",
        "strength": "weak",
        "confidence": "confirmed",
    },
    # 刘广辉 ↔ 陈金友 (Fuzhou system)
    {
        "person_a": "yongtai_liu_guanghui",
        "person_b": "yongtai_chen_jinyou",
        "type": "fuzhou_system",
        "context": "均曾在福州市政府系统工作",
        "overlap_org": "福州市",
        "overlap_period": "不同时期",
        "strength": "weak",
        "confidence": "plausible",
    },
    # 雷连鸣 ↔ 苏冰 (previous coworkers)
    {
        "person_a": "yongtai_lei_lianming",
        "person_b": "yongtai_su_bing",
        "type": "direct_coworker",
        "context": "雷连鸣任县委书记期间，苏冰曾任永泰县委副书记",
        "overlap_org": "永泰县委",
        "overlap_period": "约2019年—2023年12月",
        "strength": "medium",
        "confidence": "plausible",
    },
    # 陈金友 → 刘广辉 (succession as party secretary)
    {
        "person_a": "yongtai_chen_jinyou",
        "person_b": "yongtai_liu_guanghui",
        "type": "succession",
        "context": "陈金友卸任县委书记后由刘广辉接任",
        "overlap_org": "永泰县委",
        "overlap_period": "2026年7月",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 苏冰 → 林吓清 (succession as county mayor)
    {
        "person_a": "yongtai_su_bing",
        "person_b": "yongtai_lin_xiaqing",
        "type": "succession",
        "context": "苏冰卸任县长后由林吓清接任",
        "overlap_org": "永泰县人民政府",
        "overlap_period": "2026年7月",
        "strength": "strong",
        "confidence": "confirmed",
    },
]


# ── HELPERS ────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p.get("current_post", "")
    if "县委书记" in post:
        return "255,50,50"      # red — party secretary
    if "县长" in post or "代县长" in post:
        return "50,100,255"     # blue — government leader
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"      # orange — discipline
    if "人大" in post or "政协" in post:
        return "100,180,100"    # green — congress/CPPCC
    if "政法委" in post:
        return "180,100,0"      # brown — political/legal
    return "100,100,100"        # grey — others


def is_top_leader(p):
    return "县委书记" in p.get("current_post", "") or "县长" in p.get("current_post", "") or "代县长" in p.get("current_post", "")


def org_color(o):
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "纪委" in t:
        return "255,220,180"
    if "军事" in t:
        return "220,220,220"
    if "党委部门" in t:
        return "230,210,210"
    return "200,200,200"


# ── BUILD DB ───────────────────────────────────────────────────────────

def build_db():
    """Create SQLite database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                                 native_place, education, party_join, work_start,
                                 current_post, current_org, source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
            p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
            p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
            p.get("current_post", ""), p.get("current_org", ""),
            p.get("source", ""), p.get("notes", ""), p.get("confidence", ""),
        ))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pos["person_id"], pos["org_id"], pos["title"],
            pos.get("start", ""), pos.get("end", ""),
            pos.get("rank", ""), pos.get("note", ""),
        ))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context,
                                       overlap_org, overlap_period, strength, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["person_a"], r["person_b"], r["type"], r.get("context", ""),
            r.get("overlap_org", ""), r.get("overlap_period", ""),
            r.get("strength", ""), r.get("confidence", ""),
        ))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


# ── BUILD GEXF ─────────────────────────────────────────────────────────

def build_gexf():
    """Create GEXF graph file using string formatting (avoids namespace issues)."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>永泰县 (Yongtai County, Fuzhou, Fujian) — Leadership Network Graph</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges (worked_at)
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person edges (relationships)
    for r in relationships:
        weight = "2.0" if r.get("strength") == "strong" else "1.5" if r.get("strength") == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("strength", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[GEXF] Created: {GEXF_PATH}")
    print(f"[GEXF] Nodes: {len(persons)} persons + {len(organizations)} orgs")
    print(f"[GEXF] Edges: {len(positions)} worked_at + {len(relationships)} relationships")


# ── MAIN ───────────────────────────────────────────────────────────────

def main():
    os.makedirs(STAGING, exist_ok=True)
    build_db()
    build_gexf()

    # Print summary
    print(f"\n{'=' * 50}")
    print(f"永泰县 Leadership Network — Build Complete")
    print(f"{'=' * 50}")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"\nOutput files:")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
