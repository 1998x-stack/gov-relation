#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 黄岛区, 青岛市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_黄岛区
Level: 市辖区 (副省级城市辖区, 地厅级)
Targets: 区委书记 & 区长

Key findings:
- 原区委书记 孙永红 于 2025年9月14日 被山东省纪委监委调查
- 现任区委书记 刘昌松 于 2025年11月到任 (原聊城市委常委、常务副市长)
- 区长 王清源 于 2022年1月至今在任 (兼西海岸新区管委主任)

Research sources:
- 青岛西海岸新区(黄岛区)政务网 xihaian.gov.cn — confirmed government leadership list
- 网易新闻 — 刘昌松任命报道、王清源简介
- 青岛日报/青报网 — 刘昌松到任报道
- 凤凰网青岛 — 刘昌松调任报道
- 新京报 — 刘昌松拟任正厅级公示
- 360百科 — 黄岛区词条、王清源简介
- 青岛政务网 qingdao.gov.cn — 区政协、人大会议新闻

Confidence notes:
- 刘昌松和王清源的当前职务已通过多方新闻源确认
- 刘昌松的早期履历仅来自任前公示，具体时间节点待补
- 王清源的早期履历(2021年前)完全待查
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

SLUG = "黄岛区"
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
    # Party Committee (区委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 刘昌松 — 青岛市委常委、西海岸新区工委书记、黄岛区委书记 (现任)
    {
        "id": 1,
        "name": "刘昌松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年2月",
        "birthplace": "山东文登",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青岛市委常委、西海岸新区工委书记、黄岛区委书记",
        "current_org": "中共青岛西海岸新区工作委员会",
        "source": "网易新闻、青岛日报、凤凰网青岛、新京报多方确认"
    },
    # 王清源 — 工委副书记、管委主任、区长
    {
        "id": 2,
        "name": "王清源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "山东青岛",
        "education": "省委党校研究生，管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西海岸新区管委主任、区委副书记、区长",
        "current_org": "青岛西海岸新区管理委员会",
        "source": "青岛西海岸新区政务网 xihaian.gov.cn 领导信息页"
    },
    # 李金国 — 区委副书记
    {
        "id": 3,
        "name": "李金国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "山东胶州",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共黄岛区委员会",
        "source": "搜狐新闻、青岛政务网"
    },
    # 臧浩宇 — 工委区委常委、常务副区长
    {
        "id": 4,
        "name": "臧浩宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "研究生，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "工委区委常委、副区长（常务）",
        "current_org": "青岛西海岸新区管理委员会",
        "source": "青岛西海岸新区政务网领导信息页"
    },
    # 赵英民 — 区委常委、副区长
    {
        "id": 5,
        "name": "赵英民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "工委区委常委、副区长",
        "current_org": "青岛西海岸新区管理委员会",
        "source": "青岛西海岸新区政务网"
    },
    # 薛文谦 — 副区长
    {
        "id": 6,
        "name": "薛文谦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "青岛西海岸新区管理委员会",
        "source": "青岛西海岸新区政务网，2024年9月任副区长"
    },
    # 薛山 — 副区长
    {
        "id": 7,
        "name": "薛山",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "青岛西海岸新区管理委员会",
        "source": "青岛西海岸新区政务网"
    },
    # 傅强 — 副区长
    {
        "id": 8,
        "name": "傅强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "青岛西海岸新区管理委员会",
        "source": "青岛西海岸新区政务网，2026年初到任"
    },
    # 洪金鑫 — 副区长
    {
        "id": 9,
        "name": "洪金鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "青岛西海岸新区管理委员会",
        "source": "网易新闻，2024年9月任副区长"
    },
    # 孙永红 — 原区委书记（被查）
    {
        "id": 10,
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
        "source": "山东省纪委监委通报、北青政知新媒体、中国山东网"
    },
    # 王孝芝 — 区人大常委会主任
    {
        "id": 11,
        "name": "王孝芝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年2月",
        "birthplace": "",
        "education": "省委党校研究生，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "黄岛区人民代表大会常务委员会",
        "source": "青岛政务网、腾讯网、青岛新闻网，2026年1月补选"
    },
    # 薛仁龙 — 区人大常委会副主任
    {
        "id": 12,
        "name": "薛仁龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会党组副书记、副主任",
        "current_org": "黄岛区人民代表大会常务委员会",
        "source": "黄岛区人大官网"
    },
    # 逯鹰 — 区政协主席
    {
        "id": 13,
        "name": "逯鹰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议青岛市黄岛区委员会",
        "source": "黄岛区政务网、青岛政协"
    },
    # 赵楠 — 副区长
    {
        "id": 14,
        "name": "赵楠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "青岛西海岸新区管理委员会",
        "source": "青岛西海岸新区政务网常务会议记录"
    },
    # 王本剑 — 副区长
    {
        "id": 15,
        "name": "王本剑",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "青岛西海岸新区管理委员会",
        "source": "青岛西海岸新区政务网"
    },
    # 王凯 — 副区长
    {
        "id": 16,
        "name": "王凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "青岛西海岸新区管理委员会",
        "source": "青岛西海岸新区政务网"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共青岛西海岸新区工作委员会 / 中共黄岛区委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共青岛市委员会",
        "location": "青岛市黄岛区"
    },
    {
        "id": 2,
        "name": "青岛西海岸新区管理委员会 / 黄岛区人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "青岛市人民政府",
        "location": "青岛市黄岛区"
    },
    {
        "id": 3,
        "name": "中共黄岛区纪律检查委员会 / 黄岛区监察委员会",
        "type": "纪委",
        "level": "地厅级",
        "parent": "中共青岛市纪律检查委员会",
        "location": "青岛市黄岛区"
    },
    {
        "id": 4,
        "name": "黄岛区人民代表大会常务委员会",
        "type": "人大",
        "level": "地厅级",
        "parent": "青岛市人民代表大会常务委员会",
        "location": "青岛市黄岛区"
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议青岛市黄岛区委员会",
        "type": "政协",
        "level": "地厅级",
        "parent": "政协青岛市委员会",
        "location": "青岛市黄岛区"
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
]

positions_data = [
    # 刘昌松
    {"person_id": 1, "org_id": 1, "title": "青岛市委常委、西海岸新区工委书记、黄岛区委书记", "start_date": "2025-11", "end_date": "present", "rank": "正厅级", "note": "confirmed via multiple news sources"},
    # 王清源
    {"person_id": 2, "org_id": 2, "title": "西海岸新区管委主任、区长", "start_date": "2022-01", "end_date": "present", "rank": "正厅级", "note": "confirmed from official leadership page"},
    {"person_id": 2, "org_id": 1, "title": "工委副书记、区委副书记", "start_date": "2022-01", "end_date": "present", "rank": "正厅级", "note": "confirmed"},
    # 李金国
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "2025", "end_date": "present", "rank": "正处级", "note": "promoted from 政法委书记"},
    # 臧浩宇
    {"person_id": 4, "org_id": 2, "title": "工委区委常委、副区长（常务）", "start_date": "2024-09", "end_date": "present", "rank": "正处级", "note": "confirmed"},
    # 赵英民
    {"person_id": 5, "org_id": 2, "title": "工委区委常委、副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    # 薛文谦
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "2024-09", "end_date": "present", "rank": "副处级", "note": ""},
    # 薛山
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": "2026年初到任"},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "2024-09", "end_date": "present", "rank": "副处级", "note": ""},
    # 孙永红（前区委书记）
    {"person_id": 10, "org_id": 1, "title": "青岛市委常委、西海岸新区工委书记、黄岛区委书记", "start_date": "2020-01", "end_date": "2025-09", "rank": "正厅级", "note": "2025年9月14日被山东省纪委监委调查"},
    # 王孝芝
    {"person_id": 11, "org_id": 4, "title": "区人大常委会主任", "start_date": "2026-01", "end_date": "present", "rank": "正厅级", "note": "2026年1月补选"},
    {"person_id": 12, "org_id": 4, "title": "区人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": "党组副书记"},
    # 逯鹰
    {"person_id": 13, "org_id": 5, "title": "区政协主席", "start_date": "unknown", "end_date": "present", "rank": "正厅级", "note": ""},
    # 其他副区长
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
]

relationships_data = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "刘昌松（书记）与王清源（区长/管委主任）为当前黄岛区/西海岸新区党政主要领导搭档", "overlap_org": "中共黄岛区委员会 / 西海岸新区管委", "overlap_period": "2025-11-present"},
    # 前任继任关系
    {"person_a": 1, "person_b": 10, "type": "前任继任", "context": "刘昌松接替孙永红任黄岛区委书记/西海岸新区工委书记", "overlap_org": "中共黄岛区委员会", "overlap_period": "2025-11"},
    # 区长与常务副区长
    {"person_a": 2, "person_b": 4, "type": "工作关系", "context": "区长—常务副区长工作搭档", "overlap_org": "黄岛区人民政府", "overlap_period": "2024-09-present"},
    # 区长与其他副区长
    {"person_a": 2, "person_b": 5, "type": "工作关系", "context": "区长—副区长工作关系", "overlap_org": "黄岛区人民政府", "overlap_period": "unknown-present"},
    {"person_a": 2, "person_b": 6, "type": "工作关系", "context": "区长—副区长工作关系", "overlap_org": "黄岛区人民政府", "overlap_period": "2024-09-present"},
    {"person_a": 2, "person_b": 7, "type": "工作关系", "context": "区长—副区长工作关系", "overlap_org": "黄岛区人民政府", "overlap_period": "unknown-present"},
    # 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "工作关系", "context": "书记—专职副书记工作关系", "overlap_org": "中共黄岛区委员会", "overlap_period": "2025-present"},
    # 副书记与区长
    {"person_a": 3, "person_b": 2, "type": "工作关系", "context": "区委副书记与区委副书记（区长）工作关系", "overlap_org": "中共黄岛区委员会", "overlap_period": "2025-present"},
    # 人大主任与书记
    {"person_a": 11, "person_b": 1, "type": "工作关系", "context": "区人大常委会主任与区委书记工作关系", "overlap_org": "黄岛区", "overlap_period": "2026-01-present"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "刘昌松": {
        "filename": f"{TODAY}-山东省-青岛市-黄岛区委书记-刘昌松.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "山东省",
                "city": "青岛市",
                "region": "黄岛区",
                "job": "区委书记",
                "task_id": "shandong_黄岛区",
                "time_focus": "2025-2026"
            },
            "identity": {
                "person_id": "huangdao_liu_changsong",
                "name": "刘昌松",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1972年2月",
                "birthplace": "山东文登",
                "native_place": "山东文登",
                "education": ["大学"],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "刘昌松_1972年2月",
                    "name_birthplace": "刘昌松_山东文登",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "青岛市委常委、西海岸新区工委书记、黄岛区委书记",
                "current_org": "中共青岛西海岸新区工作委员会",
                "administrative_rank": "正厅级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002", "S003"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "", "org": "山东省内（聊城市）", "title": "历任职务", "level": "", "location": "山东省", "system": "government", "rank": "", "is_key_promotion": False, "notes": "早期履历待查", "confidence": "unverified", "source_ids": []},
                {"start": "unknown", "end": "2025-11", "org": "中共聊城市委员会", "title": "聊城市委常委、常务副市长", "level": "地厅级", "location": "山东聊城", "system": "government", "rank": "副厅级", "is_key_promotion": True, "notes": "此前在聊城任职", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
                {"start": "2025-11", "end": "present", "org": "中共青岛西海岸新区工作委员会", "title": "青岛市委常委、西海岸新区工委书记、黄岛区委书记", "level": "地厅级", "location": "山东青岛", "system": "party", "rank": "正厅级", "is_key_promotion": True, "notes": "拟任正厅级，接替被查的孙永红", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
            ],
            "organizations": [],
            "relationships": [
                {"person": "王清源", "person_id": "huangdao_wang_qingyuan", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记—区长党政搭档", "overlap_org": "中共黄岛区委员会", "overlap_period": "2025-11-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "孙永红", "person_id": "huangdao_sun_yonghong", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "刘昌松接替被调查的孙永红任黄岛区委书记", "overlap_org": "中共黄岛区委员会", "overlap_period": "2025-11", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S003"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["地方治理", "经济管理"],
                "secondary_specializations": [],
                "career_pattern": "从聊城调任青岛，跨市调任",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["山东文登→聊城→青岛"],
                "promotion_velocity": {"summary": "2025年11月从聊城市委常委调任青岛市委常委（副省级城市），同时任西海岸新区工委书记为正厅级岗位，属于重用", "notable_fast_promotions": ["从聊城调任青岛属于跨市重要晋升"]}
            },
            "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": ""},
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面信息", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "网易新闻 — 刘昌松任青岛西海岸新区工委书记", "url": "https://www.163.com", "publisher": "网易", "published_at": "2025-11", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium"},
                {"id": "S002", "title": "青岛日报 — 刘昌松到任报道", "url": "https://www.qingdaonews.com", "publisher": "青岛日报", "published_at": "2025-11", "accessed_at": AS_OF, "source_type": "media", "reliability": "high"},
                {"id": "S003", "title": "凤凰网青岛 / 新京报 — 刘昌松拟任正厅级公示", "url": "https://www.ifeng.com", "publisher": "凤凰网", "published_at": "2025-11", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium"},
            ],
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "2025年11月前在聊城市的完整职业生涯"},
            "open_questions": [{"priority": "critical", "question": "刘昌松在聊城市的具体职务变迁时间线", "why_it_matters": "核心人物早期履历完全空白", "suggested_queries": ["刘昌松 聊城 任职 简历", "刘昌松 聊城市常务副市长 任职时间"], "last_attempted": AS_OF}]
        }
    },
    "王清源": {
        "filename": f"{TODAY}-山东省-青岛市-黄岛区区长-王清源.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "山东省",
                "city": "青岛市",
                "region": "黄岛区",
                "job": "区长",
                "task_id": "shandong_黄岛区",
                "time_focus": "2022-2026"
            },
            "identity": {
                "person_id": "huangdao_wang_qingyuan",
                "name": "王清源",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1974年9月",
                "birthplace": "山东青岛",
                "native_place": "山东青岛",
                "education": ["省委党校研究生", "管理学学士"],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "王清源_1974年9月",
                    "name_birthplace": "王清源_山东青岛",
                    "official_profile_url": "https://www.xihaian.gov.cn/zwgk/gknr/jgzn/ldxx/wqy/"
                }
            },
            "current_status": {
                "current_post": "西海岸新区管委主任、黄岛区委副书记、区长",
                "current_org": "青岛西海岸新区管理委员会",
                "administrative_rank": "正厅级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "", "org": "青岛市", "title": "早期职务（含援藏经历）", "level": "", "location": "山东青岛/西藏", "system": "government", "rank": "", "is_key_promotion": False, "notes": "2022年前约20年履历待查，有援藏经历", "confidence": "unverified", "source_ids": []},
                {"start": "unknown", "end": "2022-01", "org": "莱西市人民政府", "title": "莱西市市长", "level": "县处级", "location": "山东青岛莱西", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "莱西为青岛代管县级市", "confidence": "plausible", "source_ids": ["S002"]},
                {"start": "2022-01", "end": "present", "org": "青岛西海岸新区管理委员会", "title": "西海岸新区管委主任、黄岛区委副书记、区长", "level": "地厅级", "location": "山东青岛", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "confirmed from official site and multiple news sources", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            ],
            "organizations": [],
            "relationships": [
                {"person": "刘昌松", "person_id": "huangdao_liu_changsong", "relationship_type": "overlap", "strength": "strong", "evidence": "区长—区委书记党政搭档", "overlap_org": "黄岛区/西海岸新区", "overlap_period": "2025-11-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "臧浩宇", "person_id": "huangdao_zang_haoyu", "relationship_type": "overlap", "strength": "strong", "evidence": "区长—常务副区长工作搭档", "overlap_org": "黄岛区人民政府", "overlap_period": "2024-09-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["地方行政管理", "开发区管理"],
                "secondary_specializations": ["援藏工作"],
                "career_pattern": "青岛本地成长型干部，从莱西市长调任黄岛区长",
                "systems_experience": ["government"],
                "geographic_pattern": ["山东青岛→莱西→黄岛（西海岸新区）"],
                "promotion_velocity": {"summary": "从莱西市长（县级市正处）调任黄岛区长/西海岸新区管委主任（副省级城市辖区正厅/副厅），属于重用", "notable_fast_promotions": ["从莱西市长直接调任西海岸新区管委主任，跨越幅度较大"]}
            },
            "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": ""},
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面信息", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "青岛西海岸新区政务网 — 领导信息", "url": "https://www.xihaian.gov.cn/zwgk/gknr/jgzn/ldxx/", "publisher": "黄岛区人民政府", "published_at": "2026", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
                {"id": "S002", "title": "360百科 — 黄岛区", "url": "https://baike.so.com", "publisher": "360百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium"},
            ],
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "high", "biggest_gap": "2022年前完整职业生涯（约20年）"},
            "open_questions": [{"priority": "critical", "question": "王清源2022年1月前约20年的完整职业履历", "why_it_matters": "核心人物之一，履历完全空白", "suggested_queries": ["王清源 简历 莱西市长", "王清源 援藏 任职"], "last_attempted": AS_OF}]
        }
    },
    "孙永红": {
        "filename": f"{TODAY}-山东省-青岛市-原黄岛区委书记-孙永红.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "山东省",
                "city": "青岛市",
                "region": "黄岛区",
                "job": "原区委书记",
                "task_id": "shandong_黄岛区",
                "time_focus": "2020-2025"
            },
            "identity": {
                "person_id": "huangdao_sun_yonghong",
                "name": "孙永红",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1968年6月",
                "birthplace": "山东即墨",
                "native_place": "山东即墨",
                "education": ["在职研究生"],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "孙永红_1968年6月",
                    "name_birthplace": "孙永红_山东即墨",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "原黄岛区委书记（2025年9月被调查）",
                "current_org": "中共黄岛区委员会",
                "administrative_rank": "正厅级（被调查）",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "unknown", "org": "青岛市", "title": "早期职务（待查）", "level": "", "location": "山东青岛", "system": "other", "rank": "", "is_key_promotion": False, "notes": "孙永红早期履历（约2010年前）完全待查", "confidence": "unverified", "source_ids": []},
                {"start": "unknown", "end": "2015", "org": "胶州市人民政府", "title": "胶州市市长", "level": "县处级", "location": "山东青岛胶州", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "confirmed from multiple sources", "confidence": "plausible", "source_ids": ["S002"]},
                {"start": "2015", "end": "2020-01", "org": "中共胶州市委员会", "title": "胶州市委书记", "level": "县处级", "location": "山东青岛胶州", "system": "party", "rank": "正处级（高配副厅）", "is_key_promotion": True, "notes": "", "confidence": "plausible", "source_ids": ["S002"]},
                {"start": "2020-01", "end": "2025-09-14", "org": "中共黄岛区委员会", "title": "青岛市委常委、西海岸新区工委书记、黄岛区委书记", "level": "地厅级", "location": "山东青岛", "system": "party", "rank": "正厅级", "is_key_promotion": True, "notes": "2025年9月14日被山东省纪委监委调查", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            ],
            "organizations": [],
            "relationships": [
                {"person": "刘昌松", "person_id": "huangdao_liu_changsong", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "孙永红被调查后，刘昌松接任黄岛区委书记", "overlap_org": "中共黄岛区委员会", "overlap_period": "2025-11", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["县域治理", "开发区管理"],
                "secondary_specializations": [],
                "career_pattern": "青岛本地成长型干部，从胶州起步升至青岛市委常委",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["山东即墨→胶州→黄岛"],
                "promotion_velocity": {"summary": "从胶州市委书记（县级市）升任青岛市委常委、黄岛区委书记，为重要晋升", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": ""},
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "disciplinary_action", "description": "2025年9月14日被山东省纪委监委通报涉嫌严重违纪违法，接受纪律审查和监察调查", "date": "2025-09-14", "confidence": "confirmed", "source_ids": ["S001", "S002"]}
            ],
            "source_register": [
                {"id": "S001", "title": "山东省纪委监委 — 孙永红接受纪律审查和监察调查", "url": "https://www.sdjc.gov.cn", "publisher": "山东省纪委监委", "published_at": "2025-09-14", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
                {"id": "S002", "title": "北青政知新媒体 — 孙永红被查报道", "url": "https://www.sohu.com", "publisher": "北京青年报", "published_at": "2025-09-14", "accessed_at": AS_OF, "source_type": "media", "reliability": "high"},
            ],
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed（被查）", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "早期履历（2015年前约25年）"},
            "open_questions": [{"priority": "critical", "question": "孙永红的早期履历（2010年前的完整职业经历）", "why_it_matters": "了解其晋升基础和关系网络", "suggested_queries": ["孙永红 简历 早期", "孙永红 胶州 市长 任职时间"], "last_attempted": AS_OF}]
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
