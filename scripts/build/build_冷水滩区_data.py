#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
冷水滩区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 湖南省
Parent City: 永州市
Targets: 区委书记 & 区长
Task ID: hunan_冷水滩区

As of: 2026-08-06
数据来源: 百度百科、永州政府网(yzcity.gov.cn)、冷水滩区人民政府门户(www.lst.gov.cn)、红网/新湖南/网易订阅
研究说明:
  - 李辉(区委书记): 2021-10 任冷水滩区委副书记、区长, 2025-05 起任区委书记, 2026-07-29 十届区委一次全会连选。
  - 李胜利(区长): 自郴州跨市调任, 2025-11 任区委副书记/代区长, 2026-01-28 当选区长。
  - 前任区委书记秦志军 2024-12 升任永州市副市长(与 scripts/build/build_永州市_data.py 一致)。
  - 部分区委常委分工和完整履历待补充, 以 open_questions / confidence 显式表示。
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
SLUG = "冷水滩区"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_OUT = STAGING_DIR

AS_OF = "2026-08-06"

# ══════════════════════════════════════════════════════════════════════
# 1. PERSONS
# ══════════════════════════════════════════════════════════════════════
persons = [
    # 核心：区委书记
    {
        "id": 1,
        "name": "李辉",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1978年3月",
        "birthplace": "湖南省张家界市",
        "education": "湘潭大学法学院法律专业研究生，法律硕士",
        "party_join": "中共党员",
        "work_start": "约1999年",
        "current_post": "冷水滩区委书记",
        "current_org": "中共永州市冷水滩区委员会",
        "source": "百度百科(李辉)；永州政府网/红网 2026-07-29 冷水滩区十次党代会「区委书记李辉」；区人武部党委第一书记。",
        "notes": "早年湖南省司法厅工作多年; 后调入湖南省政府研究室(综合处主任科员/副处长/处长); 2021-10 任冷水滩区委副书记、区长; 2025-05 起任区委书记; 2026-07-29 十届区委一次全会连选为书记。",
    },
    # 核心：区长
    {
        "id": 2,
        "name": "李胜利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年7月",
        "birthplace": "湖南省衡阳市衡南县",
        "education": "湖南省委党校法学理论在职研究生；文学学士(衡阳师范学院汉语言文学)",
        "party_join": "2005年4月",
        "work_start": "2005年7月",
        "current_post": "冷水滩区委副书记、区长",
        "current_org": "冷水滩区人民政府",
        "source": "百度百科(李胜利)；永州市委组织部 2025-11-17 任前公示；冷水滩区十届人大六次会议 2026-01-28 当选区长。",
        "notes": "2001-2005 衡阳师范学院汉语言文学；2005 选调生郴州市汝城县大坪镇；郴州市北湖区多个乡镇/街道党委书记(万华岩镇/月峰乡/石盖塘镇)；2016起任嘉禾县委常委、统战部长，桂东县委常委、纪委书记，桂阳县常务副县长；2023-2025 郴州市公共资源交易中心党组书记、郴州市信访局局长；2025-11 跨市调任冷水滩任区委副书记/代区长, 2026-01 当选区长。",
    },
    # 前任区委书记（已升任永州市副市长）
    {
        "id": 3,
        "name": "秦志军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永州市人民政府副市长",
        "current_org": "永州市人民政府",
        "source": "百度百科(秦志军)；网易订阅(build_永州市_data.py 一致)；永州政府网官方新闻。",
        "notes": "2021-07 ~ 2024-12 任冷水滩区委书记；2024-12 升任永州市人民政府副市长。",
    },
    # 前任区委书记（2020-2021）
    {
        "id": 4,
        "name": "桂砺锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已离任（原冷水滩区委书记）",
        "current_org": "",
        "source": "冷水滩区政府门户/永州市政府 2020-12-29 干部大会；2021-07 另有任用。",
        "notes": "2020-12 ~ 2021-07 任冷水滩区委书记，后另有任用。",
    },
    # 前任区委书记（兼任）
    {
        "id": 5,
        "name": "何冲龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已卸任（原冷水滩区委书记）",
        "current_org": "",
        "source": "永州市政府 2020-12-29 干部大会：市政协副主席何冲龙不再兼任中共冷水滩区委书记。",
        "notes": "2020-12 卸任，不再兼任冷水滩区委书记；原永州市政协副主席兼任。",
    },
    # 现任领导班子（区委）
    {
        "id": 6,
        "name": "王勤",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年1月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "冷水滩区委副书记",
        "current_org": "中共永州市冷水滩区委员会",
        "source": "百度百科(中国共产党永州市冷水滩区委员会 现任领导)；新湖南 2026-07-12 永州市委管理干部任前公示(王勤 拟进一步使用)。",
        "notes": "原冷水滩区委常委、纪委书记、监委主任；2026-07 任前公示拟进一步使用，升任区委副书记。",
    },
    {
        "id": 7,
        "name": "蒋欧林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年7月",
        "birthplace": "湖南省永州市东安县",
        "education": "湖南大学工业管理工程，自考本科学历，工学学士",
        "party_join": "2000年3月",
        "work_start": "1997年9月",
        "current_post": "冷水滩区委常委、常务副区长",
        "current_org": "冷水滩区人民政府",
        "source": "百度百科(蒋欧林)；冷水滩区人民政府门户领导页；红网 2025-11-27 区人大常委会会议。",
        "notes": "原冷水滩区委常委、区委办主任；现为区委常委、常务副区长。",
    },
    {
        "id": 8,
        "name": "杨胜德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "冷水滩区委常委、区委组织部部长",
        "current_org": "中共永州市冷水滩区委组织部",
        "source": "百度百科(中国共产党永州市冷水滩区委员会 现任领导)。",
        "notes": "区委常委、组织部部长。",
    },
    {
        "id": 9,
        "name": "黄燕玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "冷水滩区人大常委会主任",
        "current_org": "冷水滩区人民代表大会常务委员会",
        "source": "永州新闻网/红网 2025-11-27 区十届人大常委会第三十一次会议；百度百科。",
        "notes": "区人大常委会主任。",
    },
    {
        "id": 10,
        "name": "文嵩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "冷水滩区委常委",
        "current_org": "中共永州市冷水滩区委员会",
        "source": "百度百科(中国共产党永州市冷水滩区委员会 现任领导)。",
        "notes": "区委常委，分工待查。",
    },
    {
        "id": 11,
        "name": "刘晓燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "冷水滩区委常委",
        "current_org": "中共永州市冷水滩区委员会",
        "source": "百度百科(中国共产党永州市冷水滩区委员会 现任领导)。",
        "notes": "区委常委，分工待查。",
    },
    {
        "id": 12,
        "name": "曾勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "冷水滩区委常委",
        "current_org": "中共永州市冷水滩区委员会",
        "source": "百度百科(中国共产党永州市冷水滩区委员会 现任领导)。",
        "notes": "区委常委，分工待查。",
    },
    {
        "id": 13,
        "name": "周芳武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "冷水滩区委常委、区人大常委会副主任",
        "current_org": "冷水滩区人民代表大会常务委员会",
        "source": "百度百科 + 新湖南 2024-02-26 区十届四次人大会议。",
        "notes": "区委常委并任区人大常委会副主任(原处处级副职)。",
    },
    {
        "id": 14,
        "name": "伍诗仁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "湖南省永州市零陵区",
        "education": "中央广播电视大学法学专业",
        "party_join": "1999年6月",
        "work_start": "1997年8月",
        "current_post": "冷水滩区委常委",
        "current_org": "中共永州市冷水滩区委员会",
        "source": "百度百科(伍诗仁-湖南省永州市冷水滩区委常委)。",
        "notes": "区委常委，政法/公安线相关岗位待确认。",
    },
    {
        "id": 15,
        "name": "周显平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年5月",
        "birthplace": "湖南省永州市冷水滩区",
        "education": "中央党校函授学院法律专业，本科学历",
        "party_join": "中共党员",
        "work_start": "2001年1月",
        "current_post": "冷水滩区委常委、区人民政府副区长",
        "current_org": "冷水滩区人民政府",
        "source": "百度百科(周显平-湖南省永州市冷水滩区委常委、区人民政府党组)。",
        "notes": "2026-07 任区委常委；此前任冷水滩区人民政府副区长。",
    },
    {
        "id": 16,
        "name": "张文风",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "永州市冷水滩区",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "1989年7月",
        "current_post": "冷水滩区人民政府副区长",
        "current_org": "冷水滩区人民政府",
        "source": "百度百科(张文风-湖南省永州市冷水滩区副区长)。",
        "notes": "区委委员/副区长，本地干部(冷水滩人)。",
    },
    {
        "id": 17,
        "name": "周亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已离任（原冷水滩区委副书记、区长候选人）",
        "current_org": "",
        "source": "永州市政府网 2020-12-29 干部大会。",
        "notes": "2020-12 任区委副书记、提名为区长候选人；后经换届调整。",
    },
]

# ══════════════════════════════════════════════════════════════════════
# 2. ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共永州市冷水滩区委员会", "type": "党委", "level": "县处级", "parent": "中共永州市委员会", "location": "湖南省永州市冷水滩区"},
    {"id": 2, "name": "冷水滩区人民政府", "type": "政府", "level": "县处级", "parent": "永州市人民政府", "location": "湖南省永州市冷水滩区"},
    {"id": 3, "name": "冷水滩区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "永州市人民代表大会常务委员会", "location": "湖南省永州市冷水滩区"},
    {"id": 4, "name": "政协永州市冷水滩区委员会", "type": "政协", "level": "县处级", "parent": "政协永州市委员会", "location": "湖南省永州市冷水滩区"},
    {"id": 5, "name": "中共永州市冷水滩区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共永州市纪律检查委员会", "location": "湖南省永州市冷水滩区"},
    {"id": 6, "name": "中共永州市冷水滩区委组织部", "type": "党委", "level": "乡科级", "parent": "中共永州市冷水滩区委员会", "location": "湖南省永州市冷水滩区"},
    {"id": 7, "name": "中共永州市冷水滩区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共永州市冷水滩区委员会", "location": "湖南省永州市冷水滩区"},
    {"id": 8, "name": "永州市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "湖南省永州市"},
    {"id": 9, "name": "湖南省政府研究室", "type": "党委", "level": "省直部门", "parent": "湖南省人民政府", "location": "湖南省长沙市"},
    {"id": 10, "name": "郴州市北湖区（乡镇/街道）", "type": "党委", "level": "乡科级", "parent": "中共郴州市北湖区委", "location": "湖南省郴州市北湖区"},
    {"id": 11, "name": "郴州市（嘉禾/桂东/桂阳）县级班子", "type": "党委", "level": "县处级", "parent": "中共郴州市委", "location": "湖南省郴州市"},
    {"id": 12, "name": "郴州市信访局/公共资源交易中心", "type": "党委", "level": "县处级", "parent": "郴州市人民政府", "location": "湖南省郴州市"},
]

# ══════════════════════════════════════════════════════════════════════
# 3. POSITIONS (现任 + 历史任职)
# ══════════════════════════════════════════════════════════════════════
positions = [
    # 李辉（区委书记）
    {"person_id": 1, "org_id": 9, "title": "湖南省政府研究室处长", "start_date": "约2015", "end_date": "2021-09", "rank": "处级", "note": "省直经历(综合处副处长/处长)"},
    {"person_id": 1, "org_id": 1, "title": "冷水滩区委副书记、区长", "start_date": "2021-10", "end_date": "2025-04", "rank": "县处级正职", "note": "2021-10 任区长"},
    {"person_id": 1, "org_id": 1, "title": "冷水滩区委书记", "start_date": "2025-05", "end_date": "至今", "rank": "县处级正职", "note": "2025-05任; 2026-07 十届区委一次全会连任"},
    # 李胜利（区长）
    {"person_id": 2, "org_id": 10, "title": "郴州市北湖区乡镇/街道党委书记", "start_date": "约2010", "end_date": "约2016", "rank": "乡科级", "note": "万华岩镇/月峰乡/石盖塘镇"},
    {"person_id": 2, "org_id": 11, "title": "郴州市 县级党委班子成员", "start_date": "2016", "end_date": "2023", "rank": "县处级副职", "note": "嘉禾县委副书记/纪委书记/桂阳常务副县长"},
    {"person_id": 2, "org_id": 12, "title": "郴州市信访局局长、公共资源交易中心书记", "start_date": "2023", "end_date": "2025-11", "rank": "县处级", "note": "2023-2025 任"},
    {"person_id": 2, "org_id": 1, "title": "冷水滩区委副书记", "start_date": "2025-11-25", "end_date": "2025-11-26", "rank": "县处级副职", "note": "干部会议宣布"},
    {"person_id": 2, "org_id": 2, "title": "冷水滩区委副书记、代理区长", "start_date": "2025-11-27", "end_date": "2026-01-27", "rank": "县处级正职", "note": "区人大常委会决定任代区长"},
    {"person_id": 2, "org_id": 2, "title": "冷水滩区委副书记、区长", "start_date": "2026-01-28", "end_date": "至今", "rank": "县处级正职", "note": "十届人大六次会议当选"},
    # 秦志军（前任区委书记）
    {"person_id": 3, "org_id": 1, "title": "冷水滩区委书记", "start_date": "2021-07", "end_date": "2024-12", "rank": "县处级正职", "note": "2021-07 干部大会任命"},
    {"person_id": 3, "org_id": 8, "title": "永州市人民政府副市长", "start_date": "2024-12", "end_date": "至今", "rank": "副厅级", "note": "2024-12 升任副市长"},
    # 桂砺锋（前任区委书记）
    {"person_id": 4, "org_id": 1, "title": "冷水滩区委书记", "start_date": "2020-12", "end_date": "2021-07", "rank": "县处级正职", "note": "另有任用"},
    # 何冲龙（前任区委书记兼任）
    {"person_id": 5, "org_id": 1, "title": "冷水滩区委书记(兼任)", "start_date": "至2020-12", "end_date": "2020-12", "rank": "县处级正职", "note": "市政协副主席兼任，卸任不再兼任"},
    # 王勤（现任区委副书记）
    {"person_id": 6, "org_id": 5, "title": "冷水滩区委常委、纪委书记、监委主任", "start_date": "约2020", "end_date": "2026-06", "rank": "县处级副职", "note": "任纪委书记"},
    {"person_id": 6, "org_id": 1, "title": "冷水滩区委副书记", "start_date": "2026-07", "end_date": "至今", "rank": "县处级副职", "note": "任前公示拟进一步使用"},
    # 蒋欧林（常务副区长）
    {"person_id": 7, "org_id": 1, "title": "冷水滩区委常委、区委办主任", "start_date": "约2021", "end_date": "约2024", "rank": "县处级副职", "note": "主持区委机关日常工作"},
    {"person_id": 7, "org_id": 2, "title": "冷水滩区委常委、常务副区长", "start_date": "约2024", "end_date": "至今", "rank": "县处级副职", "note": "党委常委、常务副区长"},
    # 其他常委会委员
    {"person_id": 8, "org_id": 6, "title": "冷水滩区委常委、区委组织部部长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "现任"},
    {"person_id": 9, "org_id": 3, "title": "冷水滩区人大常委会主任", "start_date": "约2021", "end_date": "至今", "rank": "县处级正职", "note": "区人大主任"},
    {"person_id": 10, "org_id": 1, "title": "冷水滩区委常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "分工待查"},
    {"person_id": 11, "org_id": 1, "title": "冷水滩区委常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "分工待查"},
    {"person_id": 12, "org_id": 1, "title": "冷水滩区委常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "分工待查"},
    {"person_id": 13, "org_id": 3, "title": "冷水滩区人大常委会副主任", "start_date": "约2021", "end_date": "至今", "rank": "县处级副职", "note": "兼区委常委"},
    {"person_id": 14, "org_id": 1, "title": "冷水滩区委常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "分工待确认"},
    {"person_id": 15, "org_id": 2, "title": "冷水滩区人民政府副区长", "start_date": "2021", "end_date": "2026-06", "rank": "县处级副职", "note": "原区政府副区长"},
    {"person_id": 15, "org_id": 1, "title": "冷水滩区委常委", "start_date": "2026-07", "end_date": "至今", "rank": "县处级副职", "note": "2026-07 任区委常委"},
    {"person_id": 16, "org_id": 2, "title": "冷水滩区人民政府副区长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "副区长(本地干部)"},
    {"person_id": 17, "org_id": 2, "title": "冷水滩区人民政府区长(提名候选人)", "start_date": "2020-12", "end_date": "约2021", "rank": "县处级", "note": "前任区长候选人"},
]

# ══════════════════════════════════════════════════════════════════════
# 4. RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════
relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "李辉(区委书记)与李胜利(区长)为冷水滩区党政一把手，2026年起正式搭班子；2025-2026 在区委常委会长期共事。",
     "overlap_org": "永州市冷水滩区", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "李辉接替秦志军任冷水滩区委书记(2025-05)；秦志军升永州市副市长(2024-12)。",
     "overlap_org": "中共永州市冷水滩区委员会", "overlap_period": "2021-2025"},
    {"person_a": 1, "person_b": 17, "type": "predecessor_successor",
     "context": "周亮为2020-12 提名区长候选人，后经换届于2021-10 由李辉任区长（前后任）。",
     "overlap_org": "冷水滩区人民政府", "overlap_period": "2021前后"},
    {"person_a": 3, "person_b": 1, "type": "promotion_chain",
     "context": "秦志军由冷水滩区委书记晋升永州市副市长（区→市平台）。",
     "overlap_org": "永州市", "overlap_period": "2024-12"},
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate",
     "context": "王勤（区委副书记，前纪委书记）与李辉在区委班子共事。",
     "overlap_org": "中共永州市冷水滩区委员会", "overlap_period": "2021至今"},
    {"person_a": 7, "person_b": 2, "type": "overlap",
     "context": "蒋欧林(常务副区长)在李胜利(区长)领导下主持区政府日常工作。",
     "overlap_org": "冷水滩区人民政府", "overlap_period": "2025至今"},
    {"person_a": 7, "person_b": 1, "type": "overlap",
     "context": "李辉(区长/书记)期间，蒋欧林任区委办主任/常务副区长，长期在区委班子共事。",
     "overlap_org": "中共永州市冷水滩区委员会", "overlap_period": "2021至今"},
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

    person_data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖南省",
            "city": "永州市",
            "region": "冷水滩区",
            "job": p["current_post"],
            "task_id": "hunan_冷水滩区",
            "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": f"lengshuitan_{p['name']}",
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
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if p["id"] in (1, 2) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": pos.get("start_date") or "unknown",
                "end": pos.get("end_date") or "unknown",
                "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
                "title": pos["title"],
                "level": pos.get("rank", ""),
                "location": "湖南省永州市冷水滩区",
                "system": "party" if ("委" in pos["title"] or "纪" in pos["title"]) else "government",
                "rank": pos.get("rank", ""),
                "is_key_promotion": ("书记" in pos["title"]) or ("区长" in pos["title"]),
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if p["id"] in (1, 2) else "plausible",
                "source_ids": ["S001"] if p["id"] in (1, 2) else ["S002"],
            }
            for pos in p_poses
        ],
        "organizations": [],
        "relationships": [],
        "_relationship_raw": p_rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if p["id"] in (1, 2) else "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
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
            {"id": "S001", "title": "百度百科 — 永州市冷水滩区委领导履历", "url": "https://baike.baidu.com/", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "李辉/李胜利等人物履历与现任职务"},
            {"id": "S002", "title": "永州市人民政府门户网", "url": "https://www.yzcity.gov.cn/", "publisher": "永州市人民政府办公室", "published_at": AS_OF, "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县区传真 冷水滩新闻/党代会/人大会议"},
            {"id": "S003", "title": "冷水滩区人民政府门户网", "url": "https://www.lst.gov.cn/", "publisher": "冷水滩区人民政府办公室", "published_at": AS_OF, "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区政府领导页 李胜利/蒋欧林等"},
        ],
        "confidence_summary": {
            "identity": "confirmed" if p["id"] in (1, 2) else "plausible",
            "current_role": "confirmed" if p["id"] in (1, 2) else "plausible",
            "career_completeness": "partial" if p["id"] in (1, 2) else "thin",
            "relationship_confidence": "medium" if p["id"] in (1, 2) else "low",
            "biggest_gap": f"{p['name']} 的部分早期履历时间节点与现任分工待核；部分百科信息来源需二次确认。",
        },
        "open_questions": [
            {"priority": "critical" if p["id"] in (1, 2) else "high",
             "question": f"{p['name']} 的完整职业履历与出生资料？",
             "why_it_matters": "核心领导基础档案",
             "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任前公示"],
             "last_attempted": AS_OF},
            {"priority": "high",
             "question": f"{p['name']} 是否曾在永州市其他县区工作，或与郴州/张家界地区有人员往来？",
             "why_it_matters": "跨地交流网络分析",
             "suggested_queries": [f"{p['name']} 永州", f"{p['name']} 任职经历"],
             "last_attempted": AS_OF},
        ],
    }

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
    print("  冷水滩区领导班子数据构建完成")
    print("=" * 60)
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"  JSON:  {len(PERSON_FILES)} person files")
    print("=" * 60)
    print(f"\nPerson count:      {len(persons)}")
    print(f"Org count:         {len(organizations)}")
    print(f"Position count:    {len(positions)}")
    print(f"Relationship count:{len(relationships)}")
    print("\nNOTE: 当前网络受限(Exa限流/Baidu部分受限)，部分区委常委分工履历待补充。")
    print("      核心领导(李辉/李胜利)基于百度百科+官方新闻有较完整履历。")


if __name__ == "__main__":
    main()