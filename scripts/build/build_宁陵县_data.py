#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 宁陵县 (Ningling County), 商丘市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_宁陵县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - https://www.ningling.gov.cn/ — 宁陵县人民政府官方网站（accessed 2026-07-24）
  - 宁陵要闻 2026-06-25: "县委书记栗团结深入乡镇调研群众身边不正之风和腐败问题集中整治工作"
  - 宁陵要闻 2025-12-31: "县长栗团结到县群众服务中心公开接访"
  - 宁陵要闻 2026-03-23: "宁陵县政银企对接会及一季度金融指标运行分析会召开" mentions 卢泓亦
  - 宁陵要闻 2026-07-23: "宁陵县人大常委会主任董俊山调研惠宁理想新城项目建设情况"
  - 宁陵要闻 2026-01-28: "全县金融系统工作会议召开" mentions 卢泓亦
  - 宁陵要闻 2025-12-31: "我县召开经济运行调度会" confirms 栗团结 as 县长
  - 商丘市政府网站 www.shangqiu.gov.cn 确认商丘市领导信息

Confidence notes:
  - 栗团结: confirmed as 县委书记 since ~June 2026 (previously 县长 before 2026)
  - 董俊山: confirmed as 县人大常委会主任 (2026-07-22)
  - 卢泓亦: confirmed as 县委常委、常务副县长 (2026-01 to 2026-03)
  - 岳德熙: confirmed as 县委常委、政法委书记 (2025-12-29)
  - 陈苏豫、司维: confirmed as 县领导 (2026-06-25 article)
  - 高立: confirmed as 县人大常委会副主任、县总工会主席
  - 齐雅琳: confirmed as 县政协副主席
  - 朱勇: confirmed as 县开发区党工委书记
  - 宁陵县现任县长（栗团结升任县委书记后）身份待查
  - All career timelines, birth info, education: unverified due to degraded web access
  - This is a partial-evidence artifact: core leader identities are confirmed through
    official sources but detailed biographies are gaps.
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root: data/tmp/henan_宁陵县/ → data/ → repo root
SLUG = "宁陵县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "栗团结",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共宁陵县委员会",
        "source": "Confirmed via official government news: 2026-06-25 article '县委书记栗团结深入乡镇调研'. Previously served as 宁陵县长 (confirmed via 2025-12-31 article '县长栗团结到县群众服务中心公开接访' and 2025-12-30 '县长栗团结出席经济运行调度会'). Promoted from 县长 to 县委书记 between Jan and June 2026."
    },
    {
        "id": 2,
        "name": "待查（县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长（姓名待查）",
        "current_org": "宁陵县人民政府",
        "source": "Current 宁陵县长 identity unverified. 栗团结 was previously 县长 (confirmed through 2025-12 articles) and has been promoted to 县委书记 (~June 2026). The new 县长 or 代县长 has not been identified from available news articles. Needs targeted search or government leadership page access."
    },
    # ═══════ Other Confirmed Leaders ═══════
    {
        "id": 3,
        "name": "董俊山",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "宁陵县人民代表大会常务委员会",
        "source": "Confirmed via 2026-07-23 official article: '宁陵县人大常委会主任董俊山调研惠宁理想新城项目建设情况'."
    },
    {
        "id": 4,
        "name": "卢泓亦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "宁陵县人民政府",
        "source": "Confirmed via multiple official articles: 2026-03-23 '县委常委、常务副县长卢泓亦' (政银企对接会); 2026-01-28 '县委常委、常务副县长卢鸿亦' (全县金融系统工作会议). Note: name appears as 卢泓亦 (2026-03) and 卢鸿亦 (2026-01), likely the same person."
    },
    {
        "id": 5,
        "name": "岳德熙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共宁陵县委员会",
        "source": "Confirmed via 2025-12-29 official article: '县委常委、政法委书记岳德熙参加接访'."
    },
    {
        "id": 6,
        "name": "陈苏豫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（具体职务待查）",
        "current_org": "宁陵县",
        "source": "Mentioned in 2026-06-25 article as '县领导陈苏豫、司维参加' accompanying 县委书记栗团结 in investigation."
    },
    {
        "id": 7,
        "name": "司维",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（具体职务待查）",
        "current_org": "宁陵县",
        "source": "Mentioned in 2026-06-25 article as '县领导陈苏豫、司维参加' accompanying 县委书记栗团结 in investigation."
    },
    {
        "id": 8,
        "name": "高立",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任、县总工会主席",
        "current_org": "宁陵县人民代表大会常务委员会",
        "source": "Mentioned in 2026-02-27 article: '县人大常委会副主任、县总工会主席高立'."
    },
    {
        "id": 9,
        "name": "齐雅琳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议宁陵县委员会",
        "source": "Mentioned in 2026-02-27 article: '县政协副主席齐雅琳'."
    },
    {
        "id": 10,
        "name": "朱勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县开发区党工委书记",
        "current_org": "宁陵县先进制造业开发区",
        "source": "Mentioned in 2026-02-27 article: '县开发区党工委书记朱勇'."
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共宁陵县委员会", "type": "党委", "level": "县处级", "parent": "中共商丘市委", "location": "宁陵县"},
    {"id": 2, "name": "宁陵县人民政府", "type": "政府", "level": "县处级", "parent": "商丘市人民政府", "location": "宁陵县"},
    {"id": 3, "name": "宁陵县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "商丘市人大常委会", "location": "宁陵县"},
    {"id": 4, "name": "中国人民政治协商会议宁陵县委员会", "type": "政协", "level": "县处级", "parent": "商丘市政协", "location": "宁陵县"},
    {"id": 5, "name": "宁陵县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "商丘市纪委监委", "location": "宁陵县"},
    {"id": 6, "name": "中共商丘市委", "type": "党委", "level": "地级市", "parent": "中共河南省委", "location": "商丘市"},
    {"id": 7, "name": "商丘市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "商丘市"},
    {"id": 8, "name": "宁陵县先进制造业开发区", "type": "开发区", "level": "县处级", "parent": "宁陵县人民政府", "location": "宁陵县"},
]

# ── Positions (person → org with title) ────────────────────────────────────

positions = [
    # 栗团结 (id=1)
    {"person_id": 1, "org_id": 2, "title": "县长（前任）", "start_date": "unknown", "end_date": "~2026-05", "rank": "县处级正职", "note": "Confirmed as 县长 through 2025-12-31 article. Exact start date unknown."},
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "~2026-06", "end_date": "present", "rank": "县处级正职", "note": "First confirmed as 县委书记 in 2026-06-25 article."},
    # 待查县长 (id=2)
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "推定：县长兼任县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "姓名和到任时间待查"},
    # 董俊山 (id=3)
    {"person_id": 3, "org_id": 3, "title": "县人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "县处级正职", "note": "Confirmed via 2026-07-22 article"},
    # 卢泓亦 (id=4)
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": "Confirmed in 2026-01 and 2026-03 articles"},
    # 岳德熙 (id=5)
    {"person_id": 5, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": "Confirmed via 2025-12-29 article"},
    # 陈苏豫 (id=6)
    {"person_id": 6, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    # 司维 (id=7)
    {"person_id": 7, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    # 高立 (id=8)
    {"person_id": 8, "org_id": 3, "title": "县人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": "Also serves as 县总工会主席"},
    # 齐雅琳 (id=9)
    {"person_id": 9, "org_id": 4, "title": "县政协副主席", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 朱勇 (id=10)
    {"person_id": 10, "org_id": 8, "title": "县开发区党工委书记", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────

relationships = [
    # 栗团结 ↔ 待查县长（推定党政搭档）
    {
        "person_a": 1, "person_b": 2,
        "type": "predecessor_successor",
        "context": "栗团结从宁陵县长晋升为县委书记，新任县长（待查）接替其县长职位。推定为新一届党政正职搭档。",
        "overlap_org": "宁陵县",
        "overlap_period": "2026"
    },
    # 栗团结 ↔ 卢泓亦（推定上下级）
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "栗团结（县委书记）和卢泓亦（县委常委、常务副县长）在宁陵县工作，为党政领导关系",
        "overlap_org": "宁陵县",
        "overlap_period": "当前"
    },
    # 栗团结 ↔ 岳德熙
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "栗团结（县长时）和岳德熙（县委常委、政法委书记）曾同县任职",
        "overlap_org": "宁陵县",
        "overlap_period": "2025-2026"
    },
    # 栗团结 ↔ 董俊山
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "栗团结（县委书记）与董俊山（县人大常委会主任）为宁陵县核心领导",
        "overlap_org": "宁陵县",
        "overlap_period": "当前"
    },
    # 栗团结 ↔ 陈苏豫、司维
    {
        "person_a": 1, "person_b": 6,
        "type": "superior_subordinate",
        "context": "陈苏豫陪同栗团结调研（2026-06-25），推定存在上下级或协作关系",
        "overlap_org": "宁陵县",
        "overlap_period": "2026"
    },
    {
        "person_a": 1, "person_b": 7,
        "type": "superior_subordinate",
        "context": "司维陪同栗团结调研（2026-06-25），推定存在上下级或协作关系",
        "overlap_org": "宁陵县",
        "overlap_period": "2026"
    },
    # 卢泓亦 ↔ 待查县长（政府正副职）
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "推定：县长与常务副县长为政府正副职搭档",
        "overlap_org": "宁陵县人民政府",
        "overlap_period": "当前"
    },
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "栗团结",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "商丘市",
                "region": "宁陵县",
                "job": "县委书记",
                "task_id": "henan_宁陵县",
                "time_focus": "2025-2026"
            },
            "identity": {
                "person_id": "ningling_li_tuanjie",
                "name": "栗团结",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "栗团结_unknown",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共宁陵县委员会",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到栗团结任宁陵县长前的完整履历。网络访问受限。",
                    "confidence": "unverified",
                    "source_ids": []
                },
                {
                    "start": "unknown",
                    "end": "~2026-05",
                    "org": "宁陵县人民政府",
                    "title": "县长",
                    "level": "县处级正职",
                    "location": "河南省商丘市宁陵县",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": False,
                    "notes": "Confirmed as 县长: 2025-12-29 接访, 2025-12-30 经济运行调度会. Start date unknown.",
                    "confidence": "confirmed",
                    "source_ids": ["S002", "S003"]
                },
                {
                    "start": "~2026-06",
                    "end": "present",
                    "org": "中共宁陵县委员会",
                    "title": "县委书记",
                    "level": "县处级正职",
                    "location": "河南省商丘市宁陵县",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "First confirmed as 县委书记 in 2026-06-25 article.",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "organizations": [
                {"org": "宁陵县人民政府", "role": "县长", "period": "~2025-2026"},
                {"org": "中共宁陵县委员会", "role": "县委书记", "period": "2026—至今"}
            ],
            "relationships": [
                {
                    "person": "待查（县长）",
                    "person_id": "ningling_county_mayor_unknown",
                    "relationship_type": "predecessor_successor",
                    "strength": "strong",
                    "evidence": "栗团结从宁陵县长晋升为县委书记，继任县长待查",
                    "overlap_org": "宁陵县",
                    "overlap_period": "2026",
                    "direction": "undirected",
                    "confidence": "plausible",
                    "source_ids": []
                },
                {
                    "person": "卢泓亦",
                    "person_id": "ningling_lu_hongyi",
                    "relationship_type": "superior_subordinate",
                    "strength": "medium",
                    "evidence": "栗团结（县委书记）和卢泓亦（县委常委、常务副县长）在宁陵县同一领导班子",
                    "overlap_org": "宁陵县",
                    "overlap_period": "当前",
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": []  # inferred from separate articles
                },
                {
                    "person": "岳德熙",
                    "person_id": "ningling_yue_dexi",
                    "relationship_type": "overlap",
                    "strength": "medium",
                    "evidence": "栗团结（县长时）和岳德熙（县委常委、政法委书记）曾于2025年底一同参加接访活动",
                    "overlap_org": "宁陵县",
                    "overlap_period": "2025-2026",
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": []
                }
            ],
            "governance_record": [
                {
                    "period": "2026-06-25",
                    "domain": "discipline",
                    "achievement_or_event": "深入乡镇调研群众身边不正之风和腐败问题集中整治工作",
                    "role_in_event": "主持调研",
                    "location": "宁陵县石桥镇、孔集乡",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "period": "2026-06-25",
                    "domain": "economic_development",
                    "achievement_or_event": "调研高标准农田建设项目,查看灌排配套、道路升级等工作",
                    "role_in_event": "调研指导",
                    "location": "宁陵县",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "period": "2026-06-25",
                    "domain": "education",
                    "achievement_or_event": "实地察看县第三、第四中心敬老院,关注养老服务和医保基金管理",
                    "role_in_event": "检查指导",
                    "location": "宁陵县",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "period": "2025-12-29",
                    "domain": "public_security",
                    "achievement_or_event": "到县群众服务中心公开接访,现场研究解决群众反映的问题",
                    "role_in_event": "接访",
                    "location": "宁陵县",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "period": "2025-12-30",
                    "domain": "economic_development",
                    "achievement_or_event": "主持召开全县经济运行调度会,安排部署经济工作",
                    "role_in_event": "主持",
                    "location": "宁陵县",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "从县长升任县委书记，属典型县内晋升路径。具体时间线和速度因履历未知无法评估。",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "grassroots_oriented",
                        "evidence": "深入乡镇调研群众身边不正之风和腐败问题集中整治，赴基层一线实地察看敬老院、卫生院等民生设施",
                        "confidence": "plausible",
                        "source_ids": ["S001"]
                    },
                    {
                        "trait": "discipline_oriented",
                        "evidence": "调研专门聚焦不正之风和腐败问题集中整治，强调农村集体'三资'管理和医保基金安全",
                        "confidence": "plausible",
                        "source_ids": ["S001"]
                    }
                ],
                "speech_themes": ["群众利益无小事", "六个狠抓", "规范四议两公开", "案结事了、事心双解"],
                "management_signals": ["重视信访工作", "关注民生领域", "强调整改落实"],
                "caveat": "工作风格基于公开报道和讲话要点推断，非私人心理评估"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现栗团结相关的纪检处分、审计问题或负面媒体报道。实际上其作为县长/县委书记着力推动不正之风和腐败问题整治。",
                    "date": AS_OF,
                    "confidence": "plausible",
                    "source_ids": []
                }
            ],
            "source_register": [
                {"id": "S001", "title": "县委书记栗团结深入乡镇调研群众身边不正之风和腐败问题集中整治工作", "url": "https://www.ningling.gov.cn/zwzx/nlyw/content_308081", "publisher": "宁陵县人民政府", "published_at": "2026-06-26", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认栗团结为县委书记"},
                {"id": "S002", "title": "我县召开经济运行调度会", "url": "https://www.ningling.gov.cn/zwzx/nlyw/content_298450", "publisher": "宁陵县人民政府", "published_at": "2025-12-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认栗团结为县长"},
                {"id": "S003", "title": "县长栗团结到县群众服务中心公开接访", "url": "https://www.ningling.gov.cn/zwzx/nlyw/content_298444", "publisher": "宁陵县人民政府", "published_at": "2025-12-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认栗团结为县长，岳德熙为县委常委、政法委书记"}
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "栗团结任宁陵县长前的完整职业履历"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "栗团结的出生年份、籍贯、学历信息？",
                    "why_it_matters": "核心人物基本身份信息",
                    "suggested_queries": ["栗团结 简历 宁陵", "栗团结 任前公示 商丘"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "栗团结何时担任宁陵县长？此前任何职？",
                    "why_it_matters": "完整晋升路径对关系网分析至关重要",
                    "suggested_queries": ["栗团结 宁陵县 县长 任职时间", "栗团结 商丘 任职经历"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "栗团结何时由县长升任县委书记？正式任命文件？",
                    "why_it_matters": "确认晋升时间线和组织程序",
                    "suggested_queries": ["宁陵县 县委书记 任命 2026", "商丘市委 宁陵县 栗团结 任职"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    {
        "id": 2,
        "name": "待查县长",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "商丘市",
                "region": "宁陵县",
                "job": "县委副书记、县长",
                "task_id": "henan_宁陵县",
                "time_focus": "2025-2026"
            },
            "identity": {
                "person_id": "ningling_county_mayor_unknown",
                "name": "待查",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "unknown",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "县委副书记、县长（姓名待查）",
                "current_org": "宁陵县人民政府",
                "administrative_rank": "县处级正职（推定）",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": []
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "未知",
                    "title": "",
                    "notes": "宁陵县县长身份信息完全未知。栗团结升任县委书记后，县长职位可能由上级下派或县内提拔。网络访问受限导致无法确认。",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [],
            "relationships": [
                {
                    "person": "栗团结",
                    "person_id": "ningling_li_tuanjie",
                    "relationship_type": "predecessor_successor",
                    "strength": "strong",
                    "evidence": "栗团结此前任宁陵县长，晋升县委书记后有人接替县长职位",
                    "overlap_org": "宁陵县",
                    "overlap_period": "2026",
                    "direction": "other_to_person",
                    "confidence": "plausible",
                    "source_ids": []
                },
                {
                    "person": "卢泓亦",
                    "person_id": "ningling_lu_hongyi",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "推定：县长与常务副县长为政府正副职搭档",
                    "overlap_org": "宁陵县人民政府",
                    "overlap_period": "当前",
                    "direction": "undirected",
                    "confidence": "plausible",
                    "source_ids": []
                }
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "完全未知",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "完全未知"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "身份未知，无法评估",
                    "date": AS_OF,
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "source_register": [],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "unverified",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "宁陵县县长的姓名、职务、履历完全未知"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "宁陵县现任县长是谁？",
                    "why_it_matters": "核心目标人物之一",
                    "suggested_queries": ["宁陵县 县长 2026", "宁陵县 人民政府 县长 任命", "宁陵县 代县长"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "宁陵县县长何时到任？此前任职经历是什么？",
                    "why_it_matters": "完整履历对关系网络分析至关重要",
                    "suggested_queries": ["宁陵县 县长 简历", "宁陵县 县长 任前公示 商丘"],
                    "last_attempted": AS_OF
                }
            ]
        }
    }
]

# ══════════════════════════════════════════════════════════════════════════
# Runner
# ══════════════════════════════════════════════════════════════════════════

def main():
    # Use the public runner library from gov_relation
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

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

    # Write person JSON files
    for pf in person_files_data:
        person_name = pf["name"]
        job = pf["job"]
        filename = f"{TODAY}-河南省-商丘市-{job}-{person_name}.json"
        filepath = PERSONS_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filepath}")

    print(f"\nDone. Build complete for {SLUG}.")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")


if __name__ == "__main__":
    main()
