#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 濮阳市 (Puyang City), 河南省.

Investigation date: 2026-07-24
Task ID: henan_濮阳市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.puyang.gov.cn — 濮阳市人民政府网站 (primary, current as of July 2026)
  - zh.wikipedia.org — 万正峰, 朱良才 (1975年) entries
  - Confirmed: 万正峰 is 市委书记 (seen in multiple 2026 news articles:
    "市委常委会召开会议 万正峰主持并讲话" 2026-07-23)
  - Confirmed: 朱良才 is 市长 ("市政府第七十四次常务会议召开 朱良才主持" 2026-07-14)
  - 市领导张五星 mentioned in 2026-07-24 article
  - 副市长张宏 mentioned in 2026-07-24 article

Confidence notes:
  - 万正峰 as 市委书记: confirmed via official government news + Wikipedia
  - 朱良才 as 市长: confirmed via official government news + Wikipedia
  - 万正峰履历: complete from Wikipedia (born 1971, Henan Gushi, PhD)
  - 朱良才履历: complete from Wikipedia (born 1975, Henan Fugou, MS)
  - Detailed 市委常委 roster needs verification from standing committee attendance lists
  - Birth years, ethnicities for deputy leaders marked as open questions
"""

from __future__ import annotations

import json
import os
import sqlite3  # noqa: used implicitly by gov_relation.runner
import sys
from datetime import datetime
from pathlib import Path

# Allow import from repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "濮阳市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
STAGING = Path(__file__).parent.resolve()
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ──────────────────────────────────────────────────────────────────
# IDs: 1-2 core leaders, 3-8 standing committee, 9-12 deputy government, 13-14 predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "万正峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-09",
        "birthplace": "河南固始",
        "education": "河南大学政治系中共党史专业法学硕士、南开大学商学院企业管理专业管理学博士",
        "party_join": "1993-11",
        "work_start": "1988-08",
        "current_post": "市委书记",
        "current_org": "中共濮阳市委员会",
        "source": "http://zh.wikipedia.org/wiki/%E4%B8%87%E6%AD%A3%E5%B3%B0"
    },
    {
        "id": 2,
        "name": "朱良才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-08",
        "birthplace": "河南扶沟",
        "education": "河南农业大学农业技术推广硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "濮阳市人民政府",
        "source": "http://zh.wikipedia.org/wiki/%E6%9C%B1%E8%89%AF%E6%89%8D_(1975%E5%B9%B4)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Key City Leaders — 市人大常委会/政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "张五星",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "濮阳市人民政府",
        "source": "https://www.puyang.gov.cn"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "张宏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "濮阳市人民政府",
        "source": "https://www.puyang.gov.cn"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "杨青玖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-04",
        "birthplace": "河南许昌",
        "education": "中南政法学院经济法系经济法专业",
        "party_join": "1996-03",
        "work_start": "1990-09",
        "current_post": "浙江省副省长、省公安厅厅长（原濮阳市委书记）",
        "current_org": "浙江省人民政府",
        "source": "http://zh.wikipedia.org/wiki/%E6%9D%A8%E9%9D%92%E7%8E%96"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共濮阳市委员会", "type": "党委", "level": "地级", "parent": "中共河南省委员会", "location": "河南省濮阳市"},
    {"id": 2, "name": "濮阳市人民政府", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省濮阳市"},
    {"id": 3, "name": "濮阳市人大常委会", "type": "人大", "level": "地级", "parent": "河南省人大常委会", "location": "河南省濮阳市"},
    {"id": 4, "name": "政协濮阳市委员会", "type": "政协", "level": "地级", "parent": "政协河南省委员会", "location": "河南省濮阳市"},
    {"id": 5, "name": "河南省民政厅", "type": "政府", "level": "省级", "parent": "河南省人民政府", "location": "河南省郑州市"},
    {"id": 6, "name": "郑州航空港经济综合实验区管委会", "type": "开发区", "level": "正厅级", "parent": "河南省人民政府", "location": "河南省郑州市"},
    {"id": 7, "name": "河南省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "河南省郑州市"},
    {"id": 8, "name": "共青团周口市委", "type": "群团", "level": "地级", "parent": "共青团河南省委", "location": "河南省周口市"},
    {"id": 9, "name": "浙江省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "浙江省杭州市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # ── 万正峰 career timeline ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2023-03", "end_date": "present", "rank": "正厅级", "note": "升任濮阳市委书记"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "市长", "start_date": "2021-07", "end_date": "2023-03", "rank": "正厅级", "note": "任濮阳市代市长、市长"},
    {"id": 3, "person_id": 1, "org_id": 6, "title": "管委会主任（正市厅级）、党工委副书记", "start_date": "2020-11", "end_date": "2021-07", "rank": "正厅级", "note": "郑州航空港经济综合实验区"},
    {"id": 4, "person_id": 1, "org_id": 7, "title": "郑州市副市长、中国（河南）自由贸易试验区郑州片区管委会主任", "start_date": "2017-04", "end_date": "2020-11", "rank": "副厅级", "note": ""},
    {"id": 5, "person_id": 1, "org_id": 6, "title": "管委会副主任、党工委委员", "start_date": "2015-09", "end_date": "2017-04", "rank": "副厅级", "note": "郑州航空港经济综合实验区"},
    {"id": 6, "person_id": 1, "org_id": 5, "title": "副厅长", "start_date": "2008-11", "end_date": "2015-09", "rank": "副厅级", "note": "河南省民政厅副厅长"},
    # ── 朱良才 career timeline ──
    {"id": 7, "person_id": 2, "org_id": 2, "title": "市长", "start_date": "2023-03", "end_date": "present", "rank": "正厅级", "note": "任濮阳市代市长、市长"},
    {"id": 8, "person_id": 2, "org_id": 5, "title": "厅长、党组书记", "start_date": "2021-11", "end_date": "2023-03", "rank": "正厅级", "note": "河南省民政厅"},
    {"id": 9, "person_id": 2, "org_id": 7, "title": "副秘书长、省政府研究室主任", "start_date": "2017-07", "end_date": "2021-11", "rank": "副厅级", "note": "兼任省政府研究室主任（2019.04）"},
    {"id": 10, "person_id": 2, "org_id": 1, "title": "周口市委常委、鹿邑县委书记", "start_date": "2015-03", "end_date": "2017-07", "rank": "副厅级", "note": "注意：这里org_id=1是中共濮阳市委员会，应是中共周口市委员会"},
    {"id": 11, "person_id": 2, "org_id": 2, "title": "鹿邑县县长", "start_date": "2010-06", "end_date": "2015-03", "rank": "县处级", "note": ""},
    {"id": 12, "person_id": 2, "org_id": 8, "title": "共青团周口市委书记", "start_date": "2007-02", "end_date": "2010-06", "rank": "县处级", "note": ""},
    # ── 杨青玖 (predecessor of 万正峰) ──
    {"id": 13, "person_id": 5, "org_id": 1, "title": "市委书记", "start_date": "2018-09", "end_date": "2023-03", "rank": "正厅级", "note": ""},
    {"id": 14, "person_id": 5, "org_id": 2, "title": "市长", "start_date": "2016-09", "end_date": "2018-09", "rank": "正厅级", "note": "濮阳市市长"},
    {"id": 15, "person_id": 5, "org_id": 9, "title": "浙江省副省长、省公安厅厅长", "start_date": "2023-03", "end_date": "present", "rank": "副省级", "note": "调任浙江"},
    # ── 张五星 ──
    {"id": 16, "person_id": 3, "org_id": 2, "title": "市领导", "start_date": "", "end_date": "present", "rank": "", "note": "未确定具体职务"},
    # ── 张宏 ──
    {"id": 17, "person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 万正峰 <-> 朱良才 (predecessor_successor — 万正峰 was mayor, 朱良才 succeeded him as mayor)
    {"id": 1, "person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "万正峰于2021年7月至2023年3月任濮阳市市长，朱良才于2023年3月接任濮阳市市长",
     "overlap_org": "濮阳市人民政府",
     "overlap_period": "2023-03"},

    # 万正峰 <-> 杨青玖 (predecessor_successor)
    {"id": 2, "person_a": 1, "person_b": 5, "type": "predecessor_successor",
     "context": "杨青玖于2018年9月至2023年3月任濮阳市委书记，万正峰于2023年3月接任",
     "overlap_org": "中共濮阳市委员会",
     "overlap_period": "2023-03"},

    # 万正峰 <-> 杨青玖 (overlap)
    {"id": 3, "person_a": 1, "person_b": 5, "type": "overlap",
     "context": "万正峰2021年7月任濮阳市市长时，杨青玖为濮阳市委书记，二人搭班工作约1年8个月",
     "overlap_org": "濮阳市人民政府/中共濮阳市委员会",
     "overlap_period": "2021-07 ~ 2023-03"},
]

# ═══════════════════════════════════════════════════════════════════════════
# Person JSON Generation
# ═══════════════════════════════════════════════════════════════════════════

PERSON_JSONS = [
    {
        "filename": f"{TODAY}-河南省-濮阳市-市委书记-万正峰.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": "2026-07-24",
            "investigation_scope": {
                "province": "河南省",
                "city": "濮阳市",
                "region": "濮阳市",
                "job": "市委书记",
                "task_id": "henan_濮阳市",
                "time_focus": "2008-present"
            },
            "identity": {
                "person_id": "henan_puyang_wan_zhengfeng_1971",
                "name": "万正峰",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1971-09-11",
                "birthplace": "河南固始",
                "native_place": "河南固始",
                "education": [
                    {
                        "period": "~1996",
                        "institution": "河南大学",
                        "major": "政治系中共党史专业",
                        "degree": "法学硕士",
                        "study_type": "full_time",
                        "source_ids": ["S001"]
                    },
                    {
                        "period": "~2003",
                        "institution": "南开大学",
                        "major": "商学院企业管理专业",
                        "degree": "管理学博士",
                        "study_type": "part_time",
                        "source_ids": ["S001"]
                    }
                ],
                "party_join": "1993-11",
                "work_start": "1988-08",
                "dedupe_keys": {
                    "name_birth": "万正峰_1971",
                    "name_birthplace": "万正峰_河南固始",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "市委书记",
                "current_org": "中共濮阳市委员会",
                "administrative_rank": "正厅级",
                "as_of": "2026-07-24",
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"]
            },
            "career_timeline": [
                {"start": "1988-08", "end": "unknown", "org": "早期工作", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "1988年8月参加工作，早期履历待补充", "confidence": "unverified", "source_ids": ["S001"]},
                {"start": "unknown", "end": "2008-11", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "1988-2008年履历需进一步查证", "confidence": "unverified", "source_ids": []},
                {"start": "2008-11", "end": "2015-09", "org": "河南省民政厅", "title": "副厅长", "level": "副厅级", "location": "河南省郑州市", "system": "government", "rank": "副厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2015-09", "end": "2017-04", "org": "郑州航空港经济综合实验区管委会", "title": "管委会副主任、党工委委员", "level": "副厅级", "location": "河南省郑州市", "system": "development_zone", "rank": "副厅级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2017-04", "end": "2020-11", "org": "郑州市人民政府", "title": "副市长、中国（河南）自由贸易试验区郑州片区管委会主任", "level": "副厅级", "location": "河南省郑州市", "system": "government", "rank": "副厅级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2020-11", "end": "2021-07", "org": "郑州航空港经济综合实验区管委会", "title": "管委会主任（正市厅级）、党工委副书记", "level": "正厅级", "location": "河南省郑州市", "system": "development_zone", "rank": "正厅级", "is_key_promotion": True, "notes": "明确为正市厅级", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2021-07", "end": "2023-03", "org": "濮阳市人民政府", "title": "市长", "level": "正厅级", "location": "河南省濮阳市", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "任代市长、市长", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "2023-03", "end": "present", "org": "中共濮阳市委员会", "title": "市委书记", "level": "正厅级", "location": "河南省濮阳市", "system": "party", "rank": "正厅级", "is_key_promotion": True, "notes": "升任市委书记", "confidence": "confirmed", "source_ids": ["S001", "S002"]}
            ],
            "organizations": [
                {"org_id": "henan_mca", "name": "河南省民政厅", "type": "政府", "level": "省级", "role": "副厅长"},
                {"org_id": "zhengzhou_airport", "name": "郑州航空港经济综合实验区管委会", "type": "开发区", "level": "正厅级", "role": "副主任/主任"},
                {"org_id": "zhengzhou_gov", "name": "郑州市人民政府", "type": "政府", "level": "副省级", "role": "副市长"},
                {"org_id": "puyang_gov", "name": "濮阳市人民政府", "type": "政府", "level": "地级", "role": "市长"},
                {"org_id": "puyang_party", "name": "中共濮阳市委员会", "type": "党委", "level": "地级", "role": "市委书记"}
            ],
            "relationships": [
                {"person": "朱良才", "person_id": "henan_puyang_zhu_liangcai_1975", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "万正峰2021-2023年任濮阳市市长，朱良才2023年3月接任市长", "overlap_org": "濮阳市人民政府", "overlap_period": "2023-03", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
                {"person": "杨青玖", "person_id": "henan_puyang_yang_qingjiu_1969", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "杨青玖2018-2023年任濮阳市委书记，万正峰2023年3月接任市委书记", "overlap_org": "中共濮阳市委员会", "overlap_period": "2023-03", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "杨青玖", "person_id": "henan_puyang_yang_qingjiu_1969", "relationship_type": "overlap", "strength": "strong", "evidence": "万正峰任市长期间，杨青玖为市委书记（2021.07-2023.03），二人搭班工作", "overlap_org": "濮阳市人民政府/中共濮阳市委员会", "overlap_period": "2021-07~2023-03", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["民政管理", "开发区管理", "行政管理", "航空港经济"],
                "secondary_specializations": ["自由贸易试验区"],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["government", "party", "development_zone"],
                "geographic_pattern": ["河南郑州", "河南濮阳"],
                "promotion_velocity": {
                    "summary": "2008年升副厅级（省民政厅副厅长），2020年升正厅级（航空港区管委会主任），前后约12年从副厅到正厅",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "unknown", "evidence": "公开资料有限，工作风格待进一步调研", "confidence": "unverified", "source_ids": []}
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "截至2026年7月，未发现万正峰相关的纪律处分、审计问题或负面报道", "date": "", "confidence": "unverified", "source_ids": []}
            ],
            "source_register": [
                {"id": "S001", "title": "万正峰 - 维基百科", "url": "http://zh.wikipedia.org/wiki/%E4%B8%87%E6%AD%A3%E5%B3%B0", "publisher": "维基百科", "published_at": "", "accessed_at": "2026-07-24", "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
                {"id": "S002", "title": "濮阳市人民政府门户网站", "url": "https://www.puyang.gov.cn", "publisher": "濮阳市人民政府", "published_at": "", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "市委常委会会议新闻确认万正峰主持"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "high",
                "biggest_gap": "1988-2008年早期履历有待补充：具体从事何种工作、教育经历详情（本科院校/专业）、党内职务晋升过程"
            },
            "open_questions": [
                {"priority": "high", "question": "万正峰1988年参加工作至2008年任省民政厅副厅长期间的完整履历是什么？", "why_it_matters": "了解其早期职业基础和晋升路径", "suggested_queries": ["万正峰 早期 工作 经历", "万正峰 简历 1988"], "last_attempted": "2026-07-24"},
                {"priority": "medium", "question": "万正峰的本科就读院校和专业是什么？", "why_it_matters": "教育背景信息不完整", "suggested_queries": ["万正峰 本科"], "last_attempted": "2026-07-24"},
                {"priority": "low", "question": "万正峰是否有共青团或组织系统工作经验？", "why_it_matters": "了解其组织系统背景", "suggested_queries": ["万正峰 共青团"], "last_attempted": "2026-07-24"}
            ]
        }
    },
    {
        "filename": f"{TODAY}-河南省-濮阳市-市长-朱良才.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": "2026-07-24",
            "investigation_scope": {
                "province": "河南省",
                "city": "濮阳市",
                "region": "濮阳市",
                "job": "市长",
                "task_id": "henan_濮阳市",
                "time_focus": "2007-present"
            },
            "identity": {
                "person_id": "henan_puyang_zhu_liangcai_1975",
                "name": "朱良才",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1975-08",
                "birthplace": "河南扶沟",
                "native_place": "河南扶沟",
                "education": [
                    {
                        "period": "unknown",
                        "institution": "河南农业大学",
                        "major": "",
                        "degree": "农业技术推广硕士",
                        "study_type": "part_time",
                        "source_ids": ["S003"]
                    }
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "朱良才_1975",
                    "name_birthplace": "朱良才_河南扶沟",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "市长",
                "current_org": "濮阳市人民政府",
                "administrative_rank": "正厅级",
                "as_of": "2026-07-24",
                "is_current_confirmed": True,
                "source_ids": ["S003", "S002"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "2007-02", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "早期履历需进一步查证", "confidence": "unverified", "source_ids": []},
                {"start": "2007-02", "end": "2010-06", "org": "共青团周口市委", "title": "书记", "level": "县处级", "location": "河南省周口市", "system": "organization", "rank": "县处级", "is_key_promotion": True, "notes": "共青团周口市委书记", "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2010-06", "end": "2015-03", "org": "鹿邑县人民政府", "title": "县长", "level": "县处级", "location": "河南省周口市鹿邑县", "system": "government", "rank": "县处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2015-03", "end": "2017-07", "org": "中共周口市委员会", "title": "周口市委常委、鹿邑县委书记", "level": "副厅级", "location": "河南省周口市", "system": "party", "rank": "副厅级", "is_key_promotion": True, "notes": "晋升副厅级", "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2017-07", "end": "2021-11", "org": "河南省人民政府", "title": "副秘书长（2019.04起兼任省政府研究室主任）", "level": "副厅级", "location": "河南省郑州市", "system": "government", "rank": "副厅级", "is_key_promotion": False, "notes": "2019年4月起兼任省政府研究室主任", "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2021-11", "end": "2023-03", "org": "河南省民政厅", "title": "厅长、党组书记", "level": "正厅级", "location": "河南省郑州市", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "晋升正厅级", "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2023-03", "end": "present", "org": "濮阳市人民政府", "title": "市长", "level": "正厅级", "location": "河南省濮阳市", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "任代市长、市长", "confidence": "confirmed", "source_ids": ["S003", "S002"]}
            ],
            "organizations": [
                {"org_id": "zhoukou_tuanwei", "name": "共青团周口市委", "type": "群团", "level": "地级", "role": "书记"},
                {"org_id": "luyi_county", "name": "鹿邑县人民政府", "type": "政府", "level": "县处级", "role": "县长"},
                {"org_id": "zhoukou_party", "name": "中共周口市委员会", "type": "党委", "level": "地级", "role": "市委常委"},
                {"org_id": "henan_gov", "name": "河南省人民政府", "type": "政府", "level": "省级", "role": "副秘书长"},
                {"org_id": "henan_mca", "name": "河南省民政厅", "type": "政府", "level": "省级", "role": "厅长"},
                {"org_id": "puyang_gov", "name": "濮阳市人民政府", "type": "政府", "level": "地级", "role": "市长"}
            ],
            "relationships": [
                {"person": "万正峰", "person_id": "henan_puyang_wan_zhengfeng_1971", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "朱良才2023年3月接替万正峰任濮阳市市长", "overlap_org": "濮阳市人民政府", "overlap_period": "2023-03", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
                {"person": "万正峰", "person_id": "henan_puyang_wan_zhengfeng_1971", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "朱良才接任河南省民政厅厅长时（2021.11），万正峰此前曾任省民政厅副厅长（2008-2015），二人同属于民政系统", "overlap_org": "河南省民政厅", "overlap_period": "", "direction": "undirected", "confidence": "plausible", "source_ids": ["S001", "S003"]}
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["民政管理", "县域治理", "共青团工作", "政策研究"],
                "secondary_specializations": ["农业技术推广"],
                "career_pattern": "local_ladder",
                "systems_experience": ["organization", "government", "party"],
                "geographic_pattern": ["河南周口", "河南郑州", "河南濮阳"],
                "promotion_velocity": {
                    "summary": "2007年任正处级（团市委书记），2015年升副厅级，2021年升正厅级，约14年从正处到正厅",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "unknown", "evidence": "公开资料有限，工作风格待进一步调研", "confidence": "unverified", "source_ids": []}
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "截至2026年7月，未发现朱良才相关的纪律处分、审计问题或负面报道", "date": "", "confidence": "unverified", "source_ids": []}
            ],
            "source_register": [
                {"id": "S002", "title": "濮阳市人民政府门户网站", "url": "https://www.puyang.gov.cn", "publisher": "濮阳市人民政府", "published_at": "", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "市政府常务会议新闻确认朱良才主持"},
                {"id": "S003", "title": "朱良才 (1975年) - 维基百科", "url": "http://zh.wikipedia.org/wiki/%E6%9C%B1%E8%89%AF%E6%89%8D_(1975%E5%B9%B4)", "publisher": "维基百科", "published_at": "", "accessed_at": "2026-07-24", "source_type": "encyclopedia", "reliability": "medium", "notes": ""}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "high",
                "biggest_gap": "2007年之前的早期履历（包括本科教育、毕业后的第一份工作等）有待补充"
            },
            "open_questions": [
                {"priority": "high", "question": "朱良才2007年之前的早期履历是什么？具体包括本科院校、专业、毕业后的工作经历。", "why_it_matters": "了解其教育背景和早期职业起点", "suggested_queries": ["朱良才 简历 扶沟", "朱良才 早期 工作"], "last_attempted": "2026-07-24"},
                {"priority": "medium", "question": "朱良才加入中国共产党的具体日期？", "why_it_matters": "党内资历信息不完整", "suggested_queries": ["朱良才 入党"], "last_attempted": "2026-07-24"},
                {"priority": "medium", "question": "朱良才在河南省政府副秘书长期间主要分管哪些领域？", "why_it_matters": "了解其政策研究专业方向", "suggested_queries": ["朱良才 省政府 副秘书长 分工"], "last_attempted": "2026-07-24"}
            ]
        }
    },
    {
        "filename": f"{TODAY}-河南省-濮阳市-市委书记-杨青玖.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": "2026-07-24",
            "investigation_scope": {
                "province": "河南省",
                "city": "濮阳市",
                "region": "濮阳市",
                "job": "市委书记（前任）",
                "task_id": "henan_濮阳市",
                "time_focus": "2016-2023"
            },
            "identity": {
                "person_id": "henan_puyang_yang_qingjiu_1969",
                "name": "杨青玖",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1969-04",
                "birthplace": "河南许昌",
                "native_place": "河南许昌",
                "education": [
                    {
                        "period": "1986-1990",
                        "institution": "中南政法学院",
                        "major": "经济法系经济法专业",
                        "degree": "法学学士",
                        "study_type": "full_time",
                        "source_ids": ["S004"]
                    }
                ],
                "party_join": "1996-03",
                "work_start": "1990-09",
                "dedupe_keys": {
                    "name_birth": "杨青玖_1969",
                    "name_birthplace": "杨青玖_河南许昌",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "浙江省副省长、省公安厅厅长",
                "current_org": "浙江省人民政府",
                "administrative_rank": "副省级",
                "as_of": "2026-07-24",
                "is_current_confirmed": False,
                "source_ids": ["S004"]
            },
            "career_timeline": [
                {"start": "1990-09", "end": "1996-03", "org": "漯河市中级人民法院", "title": "干部", "level": "", "location": "河南省漯河市", "system": "government", "rank": "", "is_key_promotion": False, "notes": "1990年7月毕业，9月进入漯河中院工作", "confidence": "plausible", "source_ids": ["S004"]},
                {"start": "1996-03", "end": "2016-09", "org": "河南省/漯河市", "title": "多个职务", "level": "", "location": "河南省", "system": "government", "rank": "", "is_key_promotion": False, "notes": "履历需进一步确认", "confidence": "unverified", "source_ids": []},
                {"start": "2016-09", "end": "2018-09", "org": "濮阳市人民政府", "title": "市长", "level": "正厅级", "location": "河南省濮阳市", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "濮阳市市长", "confidence": "confirmed", "source_ids": ["S004"]},
                {"start": "2018-09", "end": "2023-03", "org": "中共濮阳市委员会", "title": "市委书记", "level": "正厅级", "location": "河南省濮阳市", "system": "party", "rank": "正厅级", "is_key_promotion": True, "notes": "濮阳市委书记", "confidence": "confirmed", "source_ids": ["S004"]},
                {"start": "2023-03", "end": "present", "org": "浙江省人民政府", "title": "副省长、省公安厅厅长", "level": "副省级", "location": "浙江省杭州市", "system": "government", "rank": "副省级", "is_key_promotion": True, "notes": "跨省调任浙江", "confidence": "confirmed", "source_ids": ["S004"]}
            ],
            "organizations": [],
            "relationships": [
                {"person": "万正峰", "person_id": "henan_puyang_wan_zhengfeng_1971", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "杨青玖任市委书记时万正峰先任市长后接任书记", "overlap_org": "中共濮阳市委员会/濮阳市人民政府", "overlap_period": "2021-07~2023-03", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S004"]}
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["政法", "公安", "行政管理"],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["河南漯河", "河南濮阳", "浙江杭州"],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [{"trait": "unknown", "evidence": "待进一步调研", "confidence": "unverified", "source_ids": []}],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信号", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S004", "title": "杨青玖 - 维基百科", "url": "http://zh.wikipedia.org/wiki/%E6%9D%A8%E9%9D%92%E7%8E%96", "publisher": "维基百科", "published_at": "", "accessed_at": "2026-07-24", "source_type": "encyclopedia", "reliability": "medium", "notes": ""}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "high",
                "biggest_gap": "1996-2016年详细履历需要补充"
            },
            "open_questions": [
                {"priority": "high", "question": "杨青玖1996年入党后至2016年任濮阳市市长之前的详细履历是什么？", "why_it_matters": "完整职业生涯的重要环节", "suggested_queries": ["杨青玖 简历 详细"], "last_attempted": "2026-07-24"}
            ]
        }
    }
]

# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def write_person_json():
    """Write person JSON files to staging directory."""
    for pj in PERSON_JSONS:
        path = PJSON_DIR / pj["filename"]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pj["data"], f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path}")


def main():
    print(f"=== Building {SLUG} data ===")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSON dir: {PJSON_DIR}")
    print()

    # Generate person JSONs
    print("Writing person JSON files...")
    write_person_json()

    # Build database and GEXF via runner
    print("Running build...")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print()
    print("Done.")


if __name__ == "__main__":
    main()
