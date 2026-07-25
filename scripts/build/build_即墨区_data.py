#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 即墨区, 青岛市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_即墨区
Level: 市辖区 (副省级城市辖区)
Targets: 区委书记 & 区长

Key findings:
- 区委书记 孙杰 于 2026年1月由即墨区长转任区委书记 (接替韩世军)
- 区长 张宏业 于 2026年2月由平度市长调任即墨区长
- 前任区委书记 韩世军 调任青岛市政府党组成员、崂山实验室主任助理

Research sources:
- 百度百科 — 即墨区词条 (confirming current leadership as of 2026年2月)
- 百度百科 — 孙杰 (即墨区委书记, lemmaId 60043891)
- 百度百科/Baidu search — 张宏业 (即墨区长, baike item)
- Baidu search — 韩世军去向

Confidence notes:
- 孙杰当前职务已确认 (即墨区委书记, 2026.1-)
- 张宏业当前职务已确认 (即墨区长, 2026.2.13-)
- 孙杰的早期履历 (青岛市发改委综合处处长、副主任) 来自百度百科，日期节点待精确
- 张宏业的早期履历 (胶州工作多年→平度市委副书记、市长) 来自百度搜索结果，精确时间待查
- 韩世军新职 (青岛市政府党组成员) 已确认
- 区委常委班子多数成员信息不完整
"""

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build

SLUG = "即墨区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (区委) Leadership — Core
    # ══════════════════════════════════════════════════════════════════════════

    # 孙杰 — 即墨区委书记 (现任)
    {
        "id": 1,
        "name": "孙杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年4月",
        "birthplace": "山东临沂费县",
        "education": "研究生，管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "即墨区委书记、区人武部党委第一书记",
        "current_org": "中共青岛市即墨区委员会",
        "source": "百度百科 (lemmaId 60043891), 即墨政务网, 青岛日报"
    },
    # 张宏业 — 即墨区委副书记、区长 (现任)
    {
        "id": 2,
        "name": "张宏业",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年11月",
        "birthplace": "",
        "education": "省委党校研究生，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "即墨区委副书记、区政府党组书记、区长兼青岛蓝谷管理局党委副书记、局长",
        "current_org": "即墨区人民政府",
        "source": "即墨政务网 (jimo.gov.cn), 百度百科"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Standing Committee (区委常委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 滕安正 — 区委常委、组织部部长
    {
        "id": 3,
        "name": "滕安正",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共青岛市即墨区委员会组织部",
        "source": "即墨区组织工作会议新闻报道, Baidu search"
    },
    # 郭树升 — 区委常委、政法委书记
    {
        "id": 4,
        "name": "郭树升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共青岛市即墨区委员会政法委员会",
        "source": "即墨区政法工作会议新闻报道, Baidu search"
    },
    # 马明强 — 区委常委、副区长
    {
        "id": 5,
        "name": "马明强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "即墨区人民政府",
        "source": "即墨新闻报道 (2026年7月消息), Baidu search"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Government (区政府) — Deputy Mayors
    # ══════════════════════════════════════════════════════════════════════════

    # 丁明启 — 副区长
    {
        "id": 6,
        "name": "丁明启",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "即墨区人民政府",
        "source": "即墨区人民政府领导信息 (Baidu search)"
    },
    # 周兆奇 — 副区长
    {
        "id": 7,
        "name": "周兆奇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "即墨区人民政府",
        "source": "即墨区人民政府领导信息 (Baidu search)"
    },
    # 盛鹏 — 副区长
    {
        "id": 8,
        "name": "盛鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "即墨区人民政府",
        "source": "即墨区人民政府领导信息 (Baidu search)"
    },
    # 于鑫 — 副区长
    {
        "id": 9,
        "name": "于鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "即墨区人民政府",
        "source": "即墨区人民政府领导信息 (Baidu search)"
    },
    # 宋千秀 — 副区长 (2026年4月任命)
    {
        "id": 10,
        "name": "宋千秀",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "即墨区人民政府",
        "source": "即墨区人大常委会公告 (2026年4月30日)"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════════

    # 韩世军 — 原即墨区委书记
    {
        "id": 20,
        "name": "韩世军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年10月",
        "birthplace": "山东蓬莱",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青岛市政府党组成员、崂山实验室主任助理、青岛科创大走廊工作推进领导小组执行副组长",
        "current_org": "青岛市人民政府",
        "source": "Baidu search, 即墨政务网, 青岛日报"
    },
    # 孙永红 — 原即墨市委书记/前黄岛区委书记 (即墨人, for cross-reference)
    {
        "id": 21,
        "name": "孙永红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年6月",
        "birthplace": "山东即墨",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原黄岛区委书记（2025年9月被调查）",
        "current_org": "中共黄岛区委员会",
        "source": "山东省纪委监委通报 (即墨籍重要人物, 用于交叉引用)"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共青岛市即墨区委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共青岛市委员会",
        "location": "青岛市即墨区"
    },
    {
        "id": 2,
        "name": "即墨区人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "青岛市人民政府",
        "location": "青岛市即墨区"
    },
    {
        "id": 3,
        "name": "中共青岛市即墨区纪律检查委员会 / 即墨区监察委员会",
        "type": "纪委",
        "level": "地厅级",
        "parent": "中共青岛市纪律检查委员会",
        "location": "青岛市即墨区"
    },
    {
        "id": 4,
        "name": "即墨区人民代表大会常务委员会",
        "type": "人大",
        "level": "地厅级",
        "parent": "青岛市人民代表大会常务委员会",
        "location": "青岛市即墨区"
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议青岛市即墨区委员会",
        "type": "政协",
        "level": "地厅级",
        "parent": "政协青岛市委员会",
        "location": "青岛市即墨区"
    },
    {
        "id": 6,
        "name": "中共青岛市委员会",
        "type": "党委",
        "level": "副省级",
        "parent": "中共山东省委员会",
        "location": "青岛市"
    },
    {
        "id": 7,
        "name": "青岛市人民政府",
        "type": "政府",
        "level": "副省级",
        "parent": "山东省人民政府",
        "location": "青岛市"
    },
    {
        "id": 8,
        "name": "青岛蓝谷管理局",
        "type": "事业单位",
        "level": "地厅级",
        "parent": "青岛市人民政府",
        "location": "青岛市即墨区"
    },
    {
        "id": 9,
        "name": "青岛市发展和改革委员会",
        "type": "政府",
        "level": "地厅级",
        "parent": "青岛市人民政府",
        "location": "青岛市"
    },
    {
        "id": 10,
        "name": "中共胶州市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共青岛市委员会",
        "location": "青岛市胶州市"
    },
    {
        "id": 11,
        "name": "胶州市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "青岛市人民政府",
        "location": "青岛市胶州市"
    },
    {
        "id": 12,
        "name": "中共平度市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共青岛市委员会",
        "location": "青岛市平度市"
    },
    {
        "id": 13,
        "name": "平度市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "青岛市人民政府",
        "location": "青岛市平度市"
    },
    {
        "id": 14,
        "name": "中共龙口市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共烟台市委员会",
        "location": "烟台市龙口市"
    },
    {
        "id": 15,
        "name": "龙口市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "烟台市人民政府",
        "location": "烟台市龙口市"
    },
    {
        "id": 16,
        "name": "崂山实验室",
        "type": "事业单位",
        "level": "国家级",
        "parent": "",
        "location": "青岛市崂山区"
    },
]

positions_data = [
    # 孙杰 (id=1)
    {"person_id": 1, "org_id": 9, "title": "青岛市发改委综合处处长", "start_date": "unknown", "end_date": "unknown", "rank": "正处级", "note": "confirmed from Baidu百科; exact date unknown"},
    {"person_id": 1, "org_id": 9, "title": "青岛市发展和改革委员会党组成员、副主任", "start_date": "unknown", "end_date": "unknown", "rank": "副厅级", "note": "confirmed from Baidu百科; exact date unknown"},
    {"person_id": 1, "org_id": 1, "title": "即墨区委副书记、区长", "start_date": "unknown", "end_date": "2026-01-12", "rank": "正厅级", "note": "2026年1月12日辞去区长职务"},
    {"person_id": 1, "org_id": 8, "title": "青岛蓝谷管理局局长", "start_date": "unknown", "end_date": "2026-01", "rank": "正厅级", "note": "兼任，转任书记后卸任"},
    {"person_id": 1, "org_id": 1, "title": "即墨区委书记、区人武部党委第一书记", "start_date": "2026-01-08", "end_date": "present", "rank": "正厅级", "note": "2026年1月8日被任命为区人武部党委第一书记，同时任区委书记"},

    # 张宏业 (id=2)
    {"person_id": 2, "org_id": 11, "title": "胶州市副市长等职", "start_date": "unknown", "end_date": "unknown", "rank": "副处级", "note": "在胶州市工作多年，历任多职"},
    {"person_id": 2, "org_id": 12, "title": "平度市委副书记", "start_date": "2023-03", "end_date": "2026-02", "rank": "副厅级", "note": "confirmed"},
    {"person_id": 2, "org_id": 13, "title": "平度市市长", "start_date": "2023-03", "end_date": "2026-02", "rank": "正处级(高配)", "note": "2023年3月-2026年2月任平度市长"},
    {"person_id": 2, "org_id": 2, "title": "即墨区委副书记、区政府党组书记、区长", "start_date": "2026-02-13", "end_date": "present", "rank": "正厅级", "note": "2026年2月13日正式当选即墨区长"},
    {"person_id": 2, "org_id": 8, "title": "青岛蓝谷管理局党委副书记、局长", "start_date": "2026-02", "end_date": "present", "rank": "正厅级", "note": "兼任"},

    # 滕安正 (id=3)
    {"person_id": 3, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": ""},

    # 郭树升 (id=4)
    {"person_id": 4, "org_id": 1, "title": "区委常委、政法委书记", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": ""},

    # 马明强 (id=5)
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "2026-07", "end_date": "present", "rank": "副厅级", "note": "2026年7月拟进一步使用，已任即墨区委常委"},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": "担任区委常委、副区长"},

    # 丁明启 (id=6)
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},

    # 周兆奇 (id=7)
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},

    # 盛鹏 (id=8)
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},

    # 于鑫 (id=9)
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},

    # 宋千秀 (id=10)
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "2026-04-30", "end_date": "present", "rank": "副处级", "note": "2026年4月30日区人大常委会通过任命"},

    # 韩世军 (id=20) — 前即墨区委书记
    {"person_id": 20, "org_id": 15, "title": "龙口市委副书记、市长", "start_date": "unknown", "end_date": "unknown", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 14, "title": "海阳市委副书记", "start_date": "unknown", "end_date": "unknown", "rank": "副厅级", "note": ""},
    {"person_id": 20, "org_id": 14, "title": "龙口市委书记", "start_date": "unknown", "end_date": "2021-01", "rank": "正处级(高配副厅)", "note": ""},
    {"person_id": 20, "org_id": 1, "title": "即墨区委书记", "start_date": "2021-01-23", "end_date": "2025-12", "rank": "正厅级", "note": "2021年1月23日就任"},
    {"person_id": 20, "org_id": 7, "title": "青岛市政府党组成员", "start_date": "2025-12", "end_date": "present", "rank": "副省级?不确定", "note": "韩世军新职"},
    {"person_id": 20, "org_id": 16, "title": "崂山实验室主任助理", "start_date": "2025-12", "end_date": "present", "rank": "", "note": "兼任"},

    # 孙永红 (id=21) — 即墨籍, 前黄岛书记, for reference
    {"person_id": 21, "org_id": 11, "title": "胶州市市长", "start_date": "unknown", "end_date": "2015", "rank": "正处级", "note": ""},
    {"person_id": 21, "org_id": 10, "title": "胶州市委书记", "start_date": "2015", "end_date": "2020-01", "rank": "正处级", "note": "高配副厅"},
]

relationships_data = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "孙杰（区委书记）与张宏业（区长）为当前即墨区党政主要领导搭档", "overlap_org": "中共即墨区委员会 / 即墨区人民政府", "overlap_period": "2026-02-present"},
    # 前任继任关系 (孙杰接替韩世军)
    {"person_a": 1, "person_b": 20, "type": "前任继任", "context": "孙杰接替韩世军任即墨区委书记", "overlap_org": "中共即墨区委员会", "overlap_period": "2026-01"},
    # 前任继任关系 (张宏业接替孙杰的区长职务)
    {"person_a": 2, "person_b": 1, "type": "前任继任", "context": "张宏业接替孙杰任即墨区长（孙杰转任区委书记）", "overlap_org": "即墨区人民政府", "overlap_period": "2026-02"},
    # 书记与蓝谷管理局 (孙杰曾任局长)
    {"person_a": 1, "person_b": 2, "type": "职务交接", "context": "孙杰原兼任青岛蓝谷管理局局长，转任书记后张宏业兼任局长", "overlap_org": "青岛蓝谷管理局", "overlap_period": "2026-02"},
    # 书记与组织部长
    {"person_a": 1, "person_b": 3, "type": "工作关系", "context": "区委书记—组织部部长工作关系", "overlap_org": "中共即墨区委员会", "overlap_period": "2026-01-present"},
    # 书记与政法委书记
    {"person_a": 1, "person_b": 4, "type": "工作关系", "context": "区委书记—政法委书记工作关系", "overlap_org": "中共即墨区委员会", "overlap_period": "2026-01-present"},
    # 区长与常委副区长
    {"person_a": 2, "person_b": 5, "type": "工作关系", "context": "区长—常委副区长工作搭档", "overlap_org": "即墨区人民政府", "overlap_period": "2026-02-present"},
    # 区长与副区长们
    {"person_a": 2, "person_b": 6, "type": "工作关系", "context": "区长—副区长工作关系", "overlap_org": "即墨区人民政府", "overlap_period": "2026-02-present"},
    {"person_a": 2, "person_b": 7, "type": "工作关系", "context": "区长—副区长工作关系", "overlap_org": "即墨区人民政府", "overlap_period": "2026-02-present"},
    {"person_a": 2, "person_b": 8, "type": "工作关系", "context": "区长—副区长工作关系", "overlap_org": "即墨区人民政府", "overlap_period": "2026-02-present"},
    {"person_a": 2, "person_b": 9, "type": "工作关系", "context": "区长—副区长工作关系", "overlap_org": "即墨区人民政府", "overlap_period": "2026-02-present"},
    {"person_a": 2, "person_b": 10, "type": "工作关系", "context": "区长—副区长工作关系", "overlap_org": "即墨区人民政府", "overlap_period": "2026-04-present"},
    # 韩世军与孙杰 — 前任继任
    {"person_a": 20, "person_b": 1, "type": "前任继任", "context": "韩世军→孙杰即墨区委书记交接", "overlap_org": "中共即墨区委员会", "overlap_period": "2026-01"},
    # 韩世军与孙永红 — 同为青岛区市委书记
    {"person_a": 20, "person_b": 21, "type": "同系统任职", "context": "韩世军（即墨书记）与孙永红（黄岛书记）同时期任青岛市区（市）委书记", "overlap_org": "青岛市各区市", "overlap_period": "2021-2025"},
    # 孙杰与孙永红 — 同姓+同青岛系统
    {"person_a": 1, "person_b": 21, "type": "同系统任职", "context": "孙杰（即墨书记）与孙永红（黄岛前书记）同为青岛市区级领导", "overlap_org": "青岛市", "overlap_period": "2021-2025"},
    # 张宏业与韩世军 — 平度→即墨 跨区调动
    {"person_a": 2, "person_b": 20, "type": "跨区调动", "context": "张宏业从平度市长调任即墨区长，韩世军此前亦从龙口/海阳调任即墨", "overlap_org": "青岛市", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "孙杰": {
        "filename": f"{TODAY}-山东省-青岛市-区委书记-孙杰.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "山东省",
                "city": "青岛市",
                "region": "即墨区",
                "job": "区委书记",
                "task_id": "shandong_即墨区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "jimo_sun_jie",
                "name": "孙杰",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1981年4月",
                "birthplace": "山东临沂费县",
                "native_place": "临沂费县",
                "education": [
                    {"period": "unknown", "institution": "山东大学", "major": "企业管理", "degree": "研究生，管理学硕士", "study_type": "full_time", "source_ids": ["S001"]}
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "孙杰_1981年4月",
                    "name_birthplace": "孙杰_临沂费县",
                    "official_profile_url": "https://baike.baidu.com/item/%E5%AD%99%E6%9D%B0/60043891"
                }
            },
            "current_status": {
                "current_post": "即墨区委书记、区人武部党委第一书记",
                "current_org": "中共青岛市即墨区委员会",
                "administrative_rank": "正厅级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "unknown", "org": "青岛市发展和改革委员会", "title": "综合处处长", "level": "县处级", "location": "山东青岛", "system": "government", "rank": "正处级", "is_key_promotion": False, "notes": "在青岛市发改委工作，历任综合处处长", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "青岛市发展和改革委员会", "title": "党组成员、副主任", "level": "地厅级", "location": "山东青岛", "system": "government", "rank": "副厅级", "is_key_promotion": True, "notes": "升任青岛市发改委副主任", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "2026-01-12", "org": "中共青岛市即墨区委员会/即墨区人民政府", "title": "即墨区委副书记、区长", "level": "地厅级", "location": "山东青岛即墨", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "调任即墨区，兼任青岛蓝谷管理局局长", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "2026-01", "org": "青岛蓝谷管理局", "title": "局长", "level": "地厅级", "location": "山东青岛即墨", "system": "other", "rank": "正厅级", "is_key_promotion": False, "notes": "兼任", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2026-01-08", "end": "present", "org": "中共青岛市即墨区委员会", "title": "即墨区委书记、区人武部党委第一书记", "level": "地厅级", "location": "山东青岛即墨", "system": "party", "rank": "正厅级", "is_key_promotion": True, "notes": "由区长转任区委书记，2026年1月8日被任命为区人武部党委第一书记", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "organizations": [],
            "relationships": [
                {"person": "张宏业", "person_id": "jimo_zhang_hongye", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记—区长党政搭档", "overlap_org": "中共即墨区委员会/即墨区人民政府", "overlap_period": "2026-02-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"person": "韩世军", "person_id": "jimo_han_shijun", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "孙杰接替韩世军任即墨区委书记", "overlap_org": "中共即墨区委员会", "overlap_period": "2026-01", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["发展改革", "经济管理", "地方治理"],
                "secondary_specializations": [],
                "career_pattern": "青岛市发改委系统出身，调任即墨区党政主官",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["山东费县→青岛→即墨"],
                "promotion_velocity": {"summary": "从青岛市发改委副主任调任即墨区长（正厅），后转任即墨区委书记，是青岛市首位80后区委书记（1981年生）", "notable_fast_promotions": ["青岛市首位80后区委书记"]}
            },
            "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "工作风格基于有限的公开报道推测"},
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面信息", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "百度百科 — 孙杰 (即墨区委书记)", "url": "https://baike.baidu.com/item/%E5%AD%99%E6%9D%B0/60043891", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium"},
                {"id": "S002", "title": "即墨政务网 — 领导信息", "url": "http://www.jimo.gov.cn/zwgk/fdzwgk/ldxx/", "publisher": "即墨区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
            ],
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "青岛市发改委任职的具体时间和各任职节点"},
            "open_questions": [{"priority": "critical", "question": "孙杰在青岛市发改委各职务的具体任职时间", "why_it_matters": "核心人物履历需精确化", "suggested_queries": ["孙杰 青岛市发改委 任职时间", "孙杰 即墨区长 任命时间"], "last_attempted": AS_OF},
                             {"priority": "medium", "question": "孙杰的早期生涯和家庭背景", "why_it_matters": "网络分析需要", "suggested_queries": ["孙杰 即墨 简历 费县", "孙杰 山东大学 企业管理"], "last_attempted": AS_OF}]
        }
    },
    "张宏业": {
        "filename": f"{TODAY}-山东省-青岛市-区长-张宏业.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "山东省",
                "city": "青岛市",
                "region": "即墨区",
                "job": "区长",
                "task_id": "shandong_即墨区",
                "time_focus": "2023-2026"
            },
            "identity": {
                "person_id": "jimo_zhang_hongye",
                "name": "张宏业",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1978年11月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {"period": "unknown", "institution": "省委党校", "major": "", "degree": "研究生", "study_type": "party_school", "source_ids": ["S002"]},
                    {"period": "unknown", "institution": "unknown", "major": "", "degree": "工学学士", "study_type": "unknown", "source_ids": ["S002"]}
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "张宏业_1978年11月",
                    "name_birthplace": "张宏业_unknown",
                    "official_profile_url": "http://www.jimo.gov.cn/zwgk/fdzwgk/ldxx/202202/t20220207_4315601.shtml"
                }
            },
            "current_status": {
                "current_post": "即墨区委副书记、区政府党组书记、区长兼青岛蓝谷管理局党委副书记、局长",
                "current_org": "即墨区人民政府",
                "administrative_rank": "正厅级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S002", "S003"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "unknown", "org": "胶州市", "title": "历任职务（含副市长等）", "level": "", "location": "山东青岛胶州", "system": "government", "rank": "", "is_key_promotion": False, "notes": "在胶州市工作多年，具体职务和时间待查", "confidence": "plausible", "source_ids": ["S003"]},
                {"start": "2023-03", "end": "2026-02", "org": "中共平度市委员会/平度市人民政府", "title": "平度市委副书记、市长", "level": "县处级", "location": "山东青岛平度", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2023年3月至2026年2月任职", "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2026-02-13", "end": "present", "org": "即墨区人民政府", "title": "即墨区委副书记、区长", "level": "地厅级", "location": "山东青岛即墨", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "2026年2月13日正式当选即墨区长", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
                {"start": "2026-02", "end": "present", "org": "青岛蓝谷管理局", "title": "党委副书记、局长", "level": "地厅级", "location": "山东青岛即墨", "system": "other", "rank": "正厅级", "is_key_promotion": False, "notes": "兼任", "confidence": "confirmed", "source_ids": ["S002"]},
            ],
            "organizations": [],
            "relationships": [
                {"person": "孙杰", "person_id": "jimo_sun_jie", "relationship_type": "overlap", "strength": "strong", "evidence": "区长—区委书记党政搭档", "overlap_org": "即墨区", "overlap_period": "2026-02-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
                {"person": "孙杰", "person_id": "jimo_sun_jie", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "张宏业接替转任区委书记的孙杰任即墨区长", "overlap_org": "即墨区人民政府", "overlap_period": "2026-02", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["地方治理", "县域经济管理"],
                "secondary_specializations": [],
                "career_pattern": "跨区调任型，从胶州起步→平度→即墨",
                "systems_experience": ["government"],
                "geographic_pattern": ["胶州→平度→即墨"],
                "promotion_velocity": {"summary": "从平度市长（县级市）调任即墨区长（副省级城市辖区），属于重用", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "grassroots_oriented", "evidence": "近期多次深入一线调研回迁安置、企业创新和农业生产", "confidence": "plausible", "source_ids": ["S003"]}
                ],
                "speech_themes": ["重点项目建设", "企业创新", "回迁安置", "农业生产"],
                "management_signals": [],
                "caveat": "工作风格基于有限的公开报道推测"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面信息", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S002", "title": "即墨政务网 — 区政府领导", "url": "http://www.jimo.gov.cn/zwgk/fdzwgk/ldxx/202202/t20220207_4315601.shtml", "publisher": "即墨区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
                {"id": "S003", "title": "百度百科/Baidu搜索 — 张宏业 (即墨区长)", "url": "https://www.baidu.com/s?wd=张宏业+即墨+区长", "publisher": "百度", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium"},
            ],
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "在胶州市的完整职业履历（全市）和出生地/籍贯"},
            "open_questions": [{"priority": "critical", "question": "张宏业在胶州市的具体任职经历（历任哪些职务，时间节点）", "why_it_matters": "核心人物早期履历空白", "suggested_queries": ["张宏业 胶州 任职", "张宏业 胶州副市长"], "last_attempted": AS_OF},
                             {"priority": "medium", "question": "张宏业的出生地和籍贯", "why_it_matters": "身份信息缺失", "suggested_queries": ["张宏业 籍贯 1978"], "last_attempted": AS_OF}]
        }
    },
    "韩世军": {
        "filename": f"{TODAY}-山东省-青岛市-前任区委书记-韩世军.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "山东省",
                "city": "青岛市",
                "region": "即墨区",
                "job": "前任区委书记",
                "task_id": "shandong_即墨区",
                "time_focus": "2021-2025"
            },
            "identity": {
                "person_id": "jimo_han_shijun",
                "name": "韩世军",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1968年10月",
                "birthplace": "山东蓬莱",
                "native_place": "山东蓬莱",
                "education": [
                    {"period": "unknown", "institution": "省委党校", "major": "", "degree": "研究生", "study_type": "party_school", "source_ids": ["S001"]}
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "韩世军_1968年10月",
                    "name_birthplace": "韩世军_蓬莱",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "青岛市政府党组成员、崂山实验室主任助理、青岛科创大走廊工作推进领导小组执行副组长",
                "current_org": "青岛市人民政府",
                "administrative_rank": "正厅级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "unknown", "org": "龙口市人民政府", "title": "龙口市委副书记、市长", "level": "县处级", "location": "山东烟台龙口", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "plausible", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "中共海阳市委员会", "title": "海阳市委副书记", "level": "县处级", "location": "山东烟台海阳", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "plausible", "source_ids": ["S001"]},
                {"start": "unknown", "end": "2021-01", "org": "中共龙口市委员会", "title": "龙口市委书记", "level": "县处级", "location": "山东烟台龙口", "system": "party", "rank": "正处级(高配)", "is_key_promotion": True, "notes": "", "confidence": "plausible", "source_ids": ["S001"]},
                {"start": "2021-01-23", "end": "2025-12", "org": "中共青岛市即墨区委员会", "title": "即墨区委书记", "level": "地厅级", "location": "山东青岛即墨", "system": "party", "rank": "正厅级", "is_key_promotion": True, "notes": "2021年1月23日就任即墨区委书记", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2025-12", "end": "present", "org": "青岛市人民政府", "title": "青岛市政府党组成员", "level": "副省级", "location": "山东青岛", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "调任青岛市政府", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2025-12", "end": "present", "org": "崂山实验室", "title": "主任助理", "level": "国家级", "location": "山东青岛", "system": "other", "rank": "", "is_key_promotion": False, "notes": "兼任", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "organizations": [],
            "relationships": [
                {"person": "孙杰", "person_id": "jimo_sun_jie", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "韩世军→孙杰即墨区委书记交接", "overlap_org": "中共即墨区委员会", "overlap_period": "2026-01", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "孙永红", "person_id": "jimo_sun_yonghong", "relationship_type": "same_system", "strength": "medium", "evidence": "同时期任青岛市区（市）委书记", "overlap_org": "青岛市", "overlap_period": "2021-2025", "direction": "undirected", "confidence": "plausible", "source_ids": []},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["县域治理", "地方党政领导"],
                "secondary_specializations": ["科技创新管理"],
                "career_pattern": "烟台-青岛跨市调任型，从龙口→海阳→龙口→即墨→青岛市政府",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["山东蓬莱→龙口→海阳→即墨→青岛"],
                "promotion_velocity": {"summary": "从龙口市委书记（县级市）调任即墨区委书记（副省级城市辖区正厅），属于重要跨市调任", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": ""},
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面信息", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "百度搜索 — 韩世军 (前任即墨区委书记)", "url": "https://www.baidu.com/s?wd=韩世军+即墨+前任区委书记", "publisher": "百度", "published_at": "", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium"},
            ],
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "medium", "biggest_gap": "龙口市长/海阳副书记/龙口市委书记等职位的精确时间节点"},
            "open_questions": [{"priority": "high", "question": "韩世军在龙口市长、海阳副书记、龙口市委书记各职位的精确时间", "why_it_matters": "前任核心人物履历精确化", "suggested_queries": ["韩世军 龙口 市长 任职时间", "韩世军 海阳 副书记", "韩世军 简历"], "last_attempted": AS_OF}]
        }
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

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
