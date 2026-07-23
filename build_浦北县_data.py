#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浦北县领导班子工作关系网络 — 数据构建脚本
Build SQLite database + GEXF graph + person JSON for Pubei County.

Level: 县
Province: 广西壮族自治区
Parent city: 钦州市
Targets: 县委书记 & 县长
Task: guangxi_浦北县

Research date: 2026-07-23

Current leadership (as of July 2026):
- 县委书记: 刘超荣 (promoted from 县长 in June/July 2026)
- 县长: 沈海涛 (拟提名为县长候选人 as of 2026-06-17 pre-appointment notice)
- 前任县委书记: 杨永冲 (left office in 2026)

Sources:
- 浦北县人民政府官网: https://www.gxpb.gov.cn/
- 钦州市人民政府官网: https://www.qinzhou.gov.cn/
- Baidu search results for 浦北县 leadership
- 搜狗搜索 for 刘超荣 resume details
- 领导干部任职前公示 (2026年6月17日, 钦州市委组织部)
- 网易订阅 / 浦北发布 WeChat articles

Confidence:
- Current roles: confirmed (multiple sources including official appointment notice)
- Biographical details: partial - some public resume data available
- Career timelines: partial for 刘超荣 (detailed), limited for 沈海涛
"""

from pathlib import Path
import sqlite3
import sys
import json
from datetime import datetime

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Staging paths ──
STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "浦北县_network.db"
GEXF_PATH = STAGING_DIR / "浦北县_network.gexf"
PERSONS_OUT_DIR = STAGING_DIR

TODAY = "2026-07-23"
GENERATED_AT = TODAY

# ════════════════════════════════════════════════════════════════
# RESEARCH NOTES
# ════════════════════════════════════════════════════════════════
#
# Current leadership (as of July 2026):
# 1. 刘超荣 (Liu Chaorong) — 县委书记 (promoted from 县长, ~June 2026)
#    - Male, Han ethnicity, born 1982-03, 广西平南人士
#    - 2006.07: Graduated from 武汉体育学院, 社会体育专业
#    - 2006.07-2007.04: 钦州市钦南区东场镇政府干部
#    - 2007.04-2007.07: 钦南区康熙岭镇政府负责人
#    - 2007.07-2009.03: 钦南区康熙岭镇副镇长
#    - 2009.03-2011.04: 钦南区犀牛脚镇副镇长
#    - 2011.04-2011.07: 钦南区尖山镇委副书记、综治办主任
#    - → (various positions in 钦南区, 钦北区)
#    - → 钦北区委常委、副区长
#    - → 钦州市水利局局长
#    - 2023.10: 浦北县委副书记、代县长
#    - 2023.11: 浦北县长
#    - 2026.06~07: 浦北县委书记
#
# 2. 沈海涛 (Shen Haitao) — 县长 (拟提名为县长候选人, as of 2026-06-17)
#    - Male, Yao ethnicity, born 1987-11
#    - University degree, 在职管理学硕士
#    - From enterprise background: 广西北港资源发展有限公司
#    - → 财务部部长 → 副总经理 → 董事、副董事长、总经理
#    - 2025.12: 浦北县委常委、县政府党组副书记、常务副县长
#    - 2026.06: 拟提名为县(市、区)长候选人
#
# 3. 杨永冲 (Yang Yongchong) — 前任县委书记
#    - Male, Miao ethnicity, born 1985-01, 贵州印江人士
#    - PhD, 清华大学化学系有机化学专业 (博士研究生)
#    - 2002.09-2006.09: 北京化工大学应用化学专业
#    - 2006.09-2011.07: 清华大学化学系有机化学专业 (直博)
#    - 2011.07: 参加工作 (广西选调生)
#    - → 钦州市石化局局长
#    - → 浦北县长
#    - → 浦北县委书记 (至2026年)
#    - 2026.06: 拟任县(市、区)党委书记 (公示: 刘超荣接任, 杨永冲去向待查)
#
# 4. 陈柏 — 浦北县委常委、政法委书记
#    - 1979年7月生, 汉族, 广西浦北人士
#
# 5. 李遥 — 前浦北县委副书记
#    - mentioned in 2020 news articles
#
# ════════════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════════════
# PERSONS
# ════════════════════════════════════════════════════════════════

persons = [
    # ── 1: 刘超荣 — 浦北县委书记 (2026-) ──
    {
        "id": 1,
        "name": "刘超荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年3月",
        "birthplace": "广西平南",
        "education": "在职研究生学历，公共行政与管理硕士",
        "party_join": "2009年6月",
        "work_start": "2006年7月",
        "current_post": "浦北县委书记",
        "current_org": "中共浦北县委员会",
        "source": "搜狗搜索/百度搜索结果, 2026年7月"
    },
    # ── 2: 沈海涛 — 浦北县长 (拟任, 2026-) ──
    {
        "id": 2,
        "name": "沈海涛",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth": "1987年11月",
        "birthplace": "",
        "education": "大学，在职管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦北县委副书记、县人民政府副县长、党组副书记（拟提名为县长候选人）",
        "current_org": "浦北县人民政府",
        "source": "领导干部任职前公示(2026年6月17日), 搜狗搜索"
    },
    # ── 3: 杨永冲 — 前任浦北县委书记 ──
    {
        "id": 3,
        "name": "杨永冲",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1985年1月",
        "birthplace": "贵州印江",
        "education": "研究生学历，博士（清华大学化学系有机化学专业）",
        "party_join": "2009年6月",
        "work_start": "2011年7月",
        "current_post": "前任浦北县委书记",
        "current_org": "",
        "source": "网易订阅/搜狗搜索, 2026年7月"
    },
    # ── 4: 陈柏 — 浦北县委常委、政法委书记 ──
    {
        "id": 4,
        "name": "陈柏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年7月",
        "birthplace": "广西浦北",
        "education": "广西区党校研究生学历，工学学士",
        "party_join": "2002年12月",
        "work_start": "",
        "current_post": "浦北县委常委、政法委书记",
        "current_org": "中共浦北县委员会",
        "source": "百度搜索结果, 2026年7月"
    },
    # ── 5: 班博文 — 浦北县人大常委会主任 ──
    {
        "id": 5,
        "name": "班博文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦北县人大常委会主任",
        "current_org": "浦北县人大常委会",
        "source": "浦北县新闻报道"
    },
    # ── 6: 陈建军 — 浦北县政协主席 ──
    {
        "id": 6,
        "name": "陈建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦北县政协主席",
        "current_org": "浦北县政协",
        "source": "浦北县新闻报道"
    },
]

# ════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共浦北县委员会", "type": "党委", "level": "县处级", "parent": "中共钦州市委员会", "location": "广西钦州市浦北县"},
    {"id": 2, "name": "浦北县人民政府", "type": "政府", "level": "县处级", "parent": "钦州市人民政府", "location": "广西钦州市浦北县"},
    {"id": 3, "name": "中共浦北县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共浦北县委员会", "location": "广西钦州市浦北县"},
    {"id": 4, "name": "浦北县人大常委会", "type": "人大", "level": "县处级", "parent": "浦北县", "location": "广西钦州市浦北县"},
    {"id": 5, "name": "浦北县政协", "type": "政协", "level": "县处级", "parent": "浦北县", "location": "广西钦州市浦北县"},
    {"id": 6, "name": "钦州市钦南区人民政府", "type": "政府", "level": "县处级", "parent": "钦州市人民政府", "location": "广西钦州市钦南区"},
    {"id": 7, "name": "钦州市水利局", "type": "政府", "level": "正处级", "parent": "钦州市人民政府", "location": "广西钦州市"},
    {"id": 8, "name": "广西北港资源发展有限公司", "type": "事业单位", "level": "", "parent": "", "location": "广西"},
    {"id": 9, "name": "钦州市钦北区人民政府", "type": "政府", "level": "县处级", "parent": "钦州市人民政府", "location": "广西钦州市钦北区"},
    {"id": 10, "name": "钦州市石化局", "type": "政府", "level": "正处级", "parent": "钦州市人民政府", "location": "广西钦州市"},
    {"id": 11, "name": "清华大学化学系", "type": "事业单位", "level": "", "parent": "清华大学", "location": "北京市"},
]

# ════════════════════════════════════════════════════════════════
# POSITIONS (person → org relationships)
# ════════════════════════════════════════════════════════════════

positions = [
    # 刘超荣 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "浦北县委书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "主持县委全面工作"},
    # 刘超荣 — 浦北县长（前任职务）
    {"person_id": 1, "org_id": 2, "title": "浦北县长", "start_date": "2023-10", "end_date": "2026-06", "rank": "正处级", "note": "此前曾任浦北县长"},
    # 刘超荣 — 钦州市水利局局长
    {"person_id": 1, "org_id": 7, "title": "钦州市水利局局长", "start_date": "", "end_date": "2023-10", "rank": "正处级", "note": "任浦北县长前的职务"},
    # 刘超荣 — 钦北区委常委、副区长
    {"person_id": 1, "org_id": 9, "title": "钦北区委常委、副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "曾任"},
    # 刘超荣 — 钦南区基层职务
    {"person_id": 1, "org_id": 6, "title": "钦州市钦南区东场镇政府干部等", "start_date": "2006-07", "end_date": "", "rank": "", "note": "曾任东场镇干部、康熙岭镇副镇长、犀牛脚镇副镇长、尖山镇委副书记等"},
    # 沈海涛 — 浦北常务副县长（拟任县长）
    {"person_id": 2, "org_id": 2, "title": "浦北县委常委、常务副县长", "start_date": "2025-12", "end_date": "present", "rank": "正处级", "note": "拟提名为县长候选人"},
    # 沈海涛 — 广西北港资源
    {"person_id": 2, "org_id": 8, "title": "广西北港资源发展有限公司总经理", "start_date": "", "end_date": "2025-12", "rank": "", "note": "曾任财务部部长、副总经理、董事、副董事长、总经理"},
    # 杨永冲 — 前任县委书记
    {"person_id": 3, "org_id": 1, "title": "浦北县委书记（前任）", "start_date": "", "end_date": "2026-06", "rank": "正处级", "note": "前任县委书记，去向待查"},
    # 杨永冲 — 浦北县长（前任）
    {"person_id": 3, "org_id": 2, "title": "浦北县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "此前曾任浦北县长"},
    # 杨永冲 — 钦州市石化局
    {"person_id": 3, "org_id": 10, "title": "钦州市石化局局长", "start_date": "", "end_date": "", "rank": "正处级", "note": "曾任"},
    # 陈柏 — 政法委书记
    {"person_id": 4, "org_id": 1, "title": "浦北县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "县委常委"},
    # 班博文 — 人大主任
    {"person_id": 5, "org_id": 4, "title": "浦北县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持人大工作"},
    # 陈建军 — 政协主席
    {"person_id": 6, "org_id": 5, "title": "浦北县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持政协工作"},
]

# ════════════════════════════════════════════════════════════════
# RELATIONSHIPS (person ↔ person)
# ════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政关系",
        "context": "刘超荣（县委书记）与沈海涛（拟任县长）为浦北县党政一把手搭档",
        "overlap_org": "浦北县",
        "overlap_period": "2025-至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "前后任",
        "context": "杨永冲为前任浦北县委书记，刘超荣接任；此前刘超荣接替杨永冲的浦北县长职务",
        "overlap_org": "浦北县",
        "overlap_period": "2023-2026",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "上下级",
        "context": "沈海涛2025年12月任浦北县委常委、常务副县长时，杨永冲为浦北县委书记",
        "overlap_org": "浦北县",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "同僚",
        "context": "刘超荣与陈柏同属浦北县委常委班子",
        "overlap_org": "中共浦北县委员会",
        "overlap_period": "2023-至今",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "党政同责",
        "context": "刘超荣（县委书记）与班博文（人大主任）同为县主要领导",
        "overlap_org": "浦北县",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "党政同责",
        "context": "刘超荣（县委书记）与陈建军（政协主席）同为县主要领导",
        "overlap_org": "浦北县",
        "overlap_period": "",
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "上下级",
        "context": "陈柏在杨永冲任县委书记期间任县委常委",
        "overlap_org": "中共浦北县委员会",
        "overlap_period": "",
    },
]

# ════════════════════════════════════════════════════════════════
# PERSON JSON TEMPLATES
# ════════════════════════════════════════════════════════════════

def make_person_json(person, extra):
    """Create a person graph JSON following the reference schema."""
    return {
        "schema_version": "1.0",
        "generated_at": GENERATED_AT,
        "investigation_scope": extra["scope"],
        "identity": {
            "person_id": extra.get("person_id", ""),
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": extra.get("birth", person["birth"]),
            "birthplace": extra.get("birthplace", person["birthplace"]),
            "native_place": extra.get("native_place", ""),
            "education": extra.get("education", []),
            "party_join": extra.get("party_join_date", person.get("party_join", "")),
            "work_start": extra.get("work_start_date", person.get("work_start", "")),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{extra.get('birth', person.get('birth', 'unknown'))}",
                "name_birthplace": f"{person['name']}_{extra.get('birthplace', person.get('birthplace', 'unknown'))}",
                "official_profile_url": extra.get("profile_url", ""),
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": extra.get("rank", ""),
            "as_of": TODAY,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": extra.get("career_timeline", []),
        "organizations": extra.get("organizations", []),
        "relationships": extra.get("relationships", []),
        "governance_record": extra.get("governance_record", []),
        "professional_profile": extra.get("professional_profile", {}),
        "work_style_and_personality": extra.get("work_style", {}),
        "network_metrics": {},
        "risk_and_integrity_signals": extra.get("risk_signals", []),
        "source_register": [
            {
                "id": "S001",
                "title": "浦北县人民政府门户网站",
                "url": "https://www.gxpb.gov.cn/",
                "publisher": "浦北县人民政府",
                "published_at": "",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "县政府官网; 包含领导活动动态",
            },
            *extra.get("extra_sources", []),
        ],
        "confidence_summary": {
            "identity": extra.get("confidence_identity", "unverified"),
            "current_role": extra.get("confidence_role", "confirmed"),
            "career_completeness": extra.get("career_completeness", "thin"),
            "relationship_confidence": extra.get("relationship_confidence", "medium"),
            "biggest_gap": extra.get("biggest_gap", ""),
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": q,
                "why_it_matters": w,
                "suggested_queries": sq,
                "last_attempted": TODAY,
            }
            for q, w, sq in extra.get("open_questions", [])
        ],
    }


# ── 刘超荣 person JSON ──
liuchaorong_json = make_person_json(persons[0], {
    "person_id": "guangxi_pubei_liuchaorong",
    "scope": {
        "province": "广西壮族自治区",
        "city": "钦州市",
        "region": "浦北县",
        "job": "县委书记",
        "task_id": "guangxi_浦北县",
        "time_focus": "2006-2026",
    },
    "birth": "1982年3月",
    "birthplace": "广西平南",
    "native_place": "广西平南",
    "education": [
        {
            "period": "2002年9月—2006年7月",
            "institution": "武汉体育学院",
            "major": "社会体育",
            "degree": "本科",
            "study_type": "full_time",
            "source_ids": ["S002"],
        },
        {
            "period": "",
            "institution": "公共行政与管理",
            "major": "",
            "degree": "硕士",
            "study_type": "part_time",
            "source_ids": ["S002"],
        },
    ],
    "party_join_date": "2009年6月",
    "work_start_date": "2006年7月",
    "rank": "正处级",
    "profile_url": "",
    "career_timeline": [
        {
            "start": "2006年7月",
            "end": "2007年4月",
            "org": "钦州市钦南区东场镇",
            "title": "钦南区东场镇政府干部",
            "level": "科员",
            "location": "广西钦州市钦南区",
            "system": "government",
            "rank": "",
            "is_key_promotion": False,
            "notes": "参加工作",
            "confidence": "confirmed",
            "source_ids": ["S002"],
        },
        {
            "start": "2007年4月",
            "end": "2007年7月",
            "org": "钦州市钦南区康熙岭镇",
            "title": "钦南区康熙岭镇政府负责人",
            "level": "乡科级",
            "location": "广西钦州市钦南区",
            "system": "government",
            "rank": "",
            "is_key_promotion": False,
            "notes": "",
            "confidence": "confirmed",
            "source_ids": ["S002"],
        },
        {
            "start": "2007年7月",
            "end": "2009年3月",
            "org": "钦州市钦南区康熙岭镇",
            "title": "钦南区康熙岭镇副镇长",
            "level": "乡科级副职",
            "location": "广西钦州市钦南区",
            "system": "government",
            "rank": "副科级",
            "is_key_promotion": False,
            "notes": "",
            "confidence": "confirmed",
            "source_ids": ["S002"],
        },
        {
            "start": "2009年3月",
            "end": "2011年4月",
            "org": "钦州市钦南区犀牛脚镇",
            "title": "钦南区犀牛脚镇副镇长",
            "level": "乡科级副职",
            "location": "广西钦州市钦南区",
            "system": "government",
            "rank": "副科级",
            "is_key_promotion": False,
            "notes": "",
            "confidence": "confirmed",
            "source_ids": ["S002"],
        },
        {
            "start": "2011年4月",
            "end": "2011年7月",
            "org": "钦州市钦南区尖山镇",
            "title": "钦南区尖山镇委副书记、综治办主任",
            "level": "乡科级正职",
            "location": "广西钦州市钦南区",
            "system": "party",
            "rank": "正科级",
            "is_key_promotion": False,
            "notes": "",
            "confidence": "confirmed",
            "source_ids": ["S002"],
        },
        {
            "start": "未知",
            "end": "未知",
            "org": "钦州市钦北区",
            "title": "钦北区委常委、副区长",
            "level": "县处级副职",
            "location": "广西钦州市钦北区",
            "system": "government",
            "rank": "副处级",
            "is_key_promotion": True,
            "notes": "2011-2023年间经历了钦南区多个岗位和钦北区领导职务",
            "confidence": "plausible",
            "source_ids": ["S002"],
        },
        {
            "start": "未知",
            "end": "2023年10月",
            "org": "钦州市水利局",
            "title": "钦州市水利局局长",
            "level": "正处级",
            "location": "广西钦州市",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "拟任市直正处级单位正职公示 (2022年4月)",
            "confidence": "confirmed",
            "source_ids": ["S002", "S003"],
        },
        {
            "start": "2023年10月",
            "end": "2023年11月",
            "org": "浦北县人民政府",
            "title": "浦北县委副书记、代理县长",
            "level": "县处级正职",
            "location": "广西钦州市浦北县",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "2023年9月公示后任浦北县委副书记、县政府党组书记",
            "confidence": "confirmed",
            "source_ids": ["S002", "S003"],
        },
        {
            "start": "2023年11月",
            "end": "2026年6月",
            "org": "浦北县人民政府",
            "title": "浦北县长",
            "level": "县处级正职",
            "location": "广西钦州市浦北县",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "2023年11月当选浦北县长",
            "confidence": "confirmed",
            "source_ids": ["S002", "S003"],
        },
        {
            "start": "2026年6月",
            "end": "present",
            "org": "中共浦北县委员会",
            "title": "浦北县委书记",
            "level": "县处级正职",
            "location": "广西钦州市浦北县",
            "system": "party",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "2026年6月公示拟任县(市、区)党委书记，7月已主持县委常委会会议",
            "confidence": "confirmed",
            "source_ids": ["S003"],
        },
    ],
    "organizations": [],
    "relationships": [
        {
            "person": "沈海涛",
            "person_id": "guangxi_pubei_shenhaitao",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "刘超荣（县委书记）与沈海涛（拟任县长）为浦北县党政一把手搭档",
            "overlap_org": "浦北县",
            "overlap_period": "2025-至今",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S003"],
        },
        {
            "person": "杨永冲",
            "person_id": "guangxi_pubei_yangyongchong",
            "relationship_type": "predecessor_successor",
            "strength": "strong",
            "evidence": "杨永冲为前任浦北县委书记，刘超荣接任；刘超荣此前也接替杨永冲任浦北县长",
            "overlap_org": "浦北县",
            "overlap_period": "2023-2026",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S003"],
        },
        {
            "person": "陈柏",
            "person_id": "guangxi_pubei_chenbai",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "同属浦北县委常委班子",
            "overlap_org": "中共浦北县委员会",
            "overlap_period": "2023-至今",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
    ],
    "governance_record": [],
    "professional_profile": {
        "primary_specializations": ["基层治理", "水利管理"],
        "secondary_specializations": ["县域经济发展"],
        "career_pattern": "local_ladder",
        "systems_experience": ["government", "party"],
        "geographic_pattern": ["广西钦州"],
        "promotion_velocity": {
            "summary": "2006年参加工作，2023年升正处级（浦北县长），约17年由科员晋升正处",
            "notable_fast_promotions": [
                "2006-2011: 5年从镇政府干部升至正科级",
                "2022-2023: 从水利局长转任浦北县长（重要县域正职）",
            ]
        },
    },
    "work_style": {
        "public_style_indicators": [
            {"trait": "grassroots_oriented", "evidence": "长期在钦南区乡镇基层工作，从镇政府干部逐渐晋升", "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
    },
    "risk_signals": [
        {"type": "none_found", "description": "截至2026年7月，未在公开渠道发现刘超荣的纪律处分、审计问题或负面媒体报道", "date": TODAY, "confidence": "plausible", "source_ids": ["S001", "S002"]},
    ],
    "extra_sources": [
        {
            "id": "S002",
            "title": "搜狗搜索 - 浦北县委书记刘超荣简历",
            "url": "https://www.sogou.com/web?query=刘超荣+浦北+简历",
            "publisher": "搜狗搜索",
            "published_at": "2026-07-23",
            "accessed_at": TODAY,
            "source_type": "media",
            "reliability": "medium",
            "notes": "搜索结果汇总（包含广西县域经济网、钦州领导干部任职前公示等来源）",
        },
        {
            "id": "S003",
            "title": "领导干部任职前公示（2026年6月17日）",
            "url": "",
            "publisher": "中共钦州市委组织部",
            "published_at": "2026-06-17",
            "accessed_at": TODAY,
            "source_type": "appointment_notice",
            "reliability": "high",
            "notes": "刘超荣拟任县(市、区)党委书记；沈海涛拟提名为县(市、区)长候选人",
        },
        {
            "id": "S004",
            "title": "钦州市人民政府门户网站",
            "url": "https://www.qinzhou.gov.cn/",
            "publisher": "钦州市人民政府",
            "published_at": "",
            "accessed_at": TODAY,
            "source_type": "official",
            "reliability": "high",
            "notes": "市级官网",
        },
    ],
    "confidence_identity": "confirmed",
    "confidence_role": "confirmed",
    "career_completeness": "partial",
    "relationship_confidence": "medium",
    "biggest_gap": "刘超荣2011年至任钦北区委常委/副区长之间的详细履历（约10年）需要进一步核实",
    "open_questions": [
        ("刘超荣2011年至2019年间在钦南区和钦北区的详细任职经历是什么？", "约10年的职业履历存在较大缺口", ["刘超荣 钦南区 任职", "刘超荣 钦北区 任职时间"]),
        ("刘超荣的婚姻和家庭背景？", "补充完整个人图谱", ["刘超荣 家庭"]),
        ("刘超荣在钦州市水利局期间的主要政绩？", "评估其专业治理能力", ["刘超荣 水利局 政绩"]),
    ],
})

# ── 沈海涛 person JSON ──
shenhaitao_json = make_person_json(persons[1], {
    "person_id": "guangxi_pubei_shenhaitao",
    "scope": {
        "province": "广西壮族自治区",
        "city": "钦州市",
        "region": "浦北县",
        "job": "县长",
        "task_id": "guangxi_浦北县",
        "time_focus": "2025-2026",
    },
    "birth": "1987年11月",
    "birthplace": "待查",
    "native_place": "待查",
    "education": [
        {
            "period": "",
            "institution": "",
            "major": "管理学",
            "degree": "硕士",
            "study_type": "part_time",
            "source_ids": ["S003"],
        },
    ],
    "party_join_date": "待查",
    "work_start_date": "待查",
    "rank": "正处级",
    "profile_url": "",
    "career_timeline": [
        {
            "start": "未知",
            "end": "2025年12月",
            "org": "广西北港资源发展有限公司",
            "title": "财务部部长→副总经理→董事、副董事长、总经理",
            "level": "",
            "location": "广西",
            "system": "state_owned_enterprise",
            "rank": "",
            "is_key_promotion": False,
            "notes": "企业任职经历，具体任职时间待查",
            "confidence": "plausible",
            "source_ids": ["S003"],
        },
        {
            "start": "2025年12月",
            "end": "present",
            "org": "浦北县人民政府",
            "title": "浦北县委常委、常务副县长（党组副书记）",
            "level": "县处级",
            "location": "广西钦州市浦北县",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "从企业调任政府，2025年12月任浦北县委常委、常务副县长",
            "confidence": "confirmed",
            "source_ids": ["S003"],
        },
        {
            "start": "2026年6月",
            "end": "present",
            "org": "浦北县人民政府",
            "title": "拟提名为浦北县长候选人",
            "level": "县处级正职",
            "location": "广西钦州市浦北县",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "2026年6月17日公示拟提名为县(市、区)长候选人",
            "confidence": "confirmed",
            "source_ids": ["S003"],
        },
    ],
    "organizations": [],
    "relationships": [
        {
            "person": "刘超荣",
            "person_id": "guangxi_pubei_liuchaorong",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "沈海涛（常务副县长/拟任县长）与刘超荣（县委书记）为浦北县党政搭档",
            "overlap_org": "浦北县",
            "overlap_period": "2025-至今",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S003"],
        },
        {
            "person": "杨永冲",
            "person_id": "guangxi_pubei_yangyongchong",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "沈海涛2025年12月任浦北县委常委、常务副县长时，杨永冲为县委书记",
            "overlap_org": "浦北县",
            "overlap_period": "2025-2026",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S003"],
        },
    ],
    "governance_record": [],
    "professional_profile": {
        "primary_specializations": ["企业管理", "财务管理"],
        "secondary_specializations": [],
        "career_pattern": "cross_county_rotation",
        "systems_experience": ["state_owned_enterprise", "government"],
        "geographic_pattern": ["广西"],
        "promotion_velocity": {
            "summary": "从企业高管转任地方政府要职，属于较罕见的【国企→政府】转换路径",
            "notable_fast_promotions": [],
        },
    },
    "work_style": {
        "public_style_indicators": [
            {"trait": "unknown", "evidence": "公开信息有限", "confidence": "unverified", "source_ids": []},
        ],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
    },
    "risk_signals": [
        {"type": "none_found", "description": "截至2026年7月，未在公开渠道发现沈海涛的纪律处分、审计问题或负面媒体报道", "date": TODAY, "confidence": "plausible", "source_ids": ["S001"]},
    ],
    "extra_sources": [
        {
            "id": "S003",
            "title": "领导干部任职前公示（2026年6月17日）",
            "url": "",
            "publisher": "中共钦州市委组织部",
            "published_at": "2026-06-17",
            "accessed_at": TODAY,
            "source_type": "appointment_notice",
            "reliability": "high",
            "notes": "沈海涛拟提名为县(市、区)长候选人",
        },
        {
            "id": "S005",
            "title": "浦北发布 - 浦北县委常委、常务副县长沈海涛参加活动报道",
            "url": "",
            "publisher": "浦北发布（微信公众平台）",
            "published_at": "2025-12-30",
            "accessed_at": TODAY,
            "source_type": "media",
            "reliability": "medium",
            "notes": "确认沈海涛2025年12月已任浦北县委常委、常务副县长",
        },
    ],
    "confidence_identity": "plausible",
    "confidence_role": "confirmed",
    "career_completeness": "thin",
    "relationship_confidence": "medium",
    "biggest_gap": "沈海涛的完整职业生涯履历（包括毕业院校、早期工作经历）需要进一步核实",
    "open_questions": [
        ("沈海涛的毕业院校和专业背景？", "作为县长的教育基础信息", ["沈海涛 毕业 院校", "沈海涛 学历"]),
        ("沈海涛在广西北港资源发展有限公司的详细任职时间？", "完善其企业履职时间线", ["沈海涛 北港资源 任职"]),
        ("沈海涛的籍贯和出生地？", "作为县长的基础身份信息，对人物溯源和去重至关重要", ["沈海涛 籍贯"]),
        ("沈海涛何时加入中国共产党？", "作为政治身份的基础信息", ["沈海涛 中共党员"]),
    ],
})

# ── 杨永冲 person JSON ──
yangyongchong_json = make_person_json(persons[2], {
    "person_id": "guangxi_pubei_yangyongchong",
    "scope": {
        "province": "广西壮族自治区",
        "city": "钦州市",
        "region": "浦北县",
        "job": "前任县委书记",
        "task_id": "guangxi_浦北县",
        "time_focus": "2011-2026",
    },
    "birth": "1985年1月",
    "birthplace": "贵州印江",
    "native_place": "贵州印江",
    "education": [
        {
            "period": "2002年9月—2006年9月",
            "institution": "北京化工大学",
            "major": "应用化学",
            "degree": "本科",
            "study_type": "full_time",
            "source_ids": ["S006"],
        },
        {
            "period": "2006年9月—2011年7月",
            "institution": "清华大学化学系",
            "major": "有机化学",
            "degree": "博士",
            "study_type": "full_time",
            "source_ids": ["S006"],
        },
    ],
    "party_join_date": "2009年6月",
    "work_start_date": "2011年7月",
    "rank": "正处级",
    "profile_url": "",
    "career_timeline": [
        {
            "start": "2011年7月",
            "end": "未知",
            "org": "钦州市",
            "title": "广西选调生（清华大学博士）",
            "level": "",
            "location": "广西钦州市",
            "system": "government",
            "rank": "",
            "is_key_promotion": True,
            "notes": "清华大学博士毕业后通过广西选调生项目到钦州工作",
            "confidence": "confirmed",
            "source_ids": ["S006"],
        },
        {
            "start": "未知",
            "end": "未知",
            "org": "钦州市石化局",
            "title": "钦州市石化局局长",
            "level": "正处级",
            "location": "广西钦州市",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "曾任钦州市石化局局长",
            "confidence": "plausible",
            "source_ids": ["S006"],
        },
        {
            "start": "未知",
            "end": "2023年8月",
            "org": "浦北县人民政府",
            "title": "浦北县长",
            "level": "县处级正职",
            "location": "广西钦州市浦北县",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "2023年8月公示拟任县(区)党委书记",
            "confidence": "confirmed",
            "source_ids": ["S006"],
        },
        {
            "start": "2023年8月",
            "end": "2026年6月",
            "org": "中共浦北县委员会",
            "title": "浦北县委书记",
            "level": "县处级正职",
            "location": "广西钦州市浦北县",
            "system": "party",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "2023年8月公示拟任县委书记，后正式任职",
            "confidence": "confirmed",
            "source_ids": ["S006"],
        },
        {
            "start": "2026年6月",
            "end": "present",
            "org": "去向待查",
            "title": "卸任浦北县委书记",
            "level": "",
            "location": "",
            "system": "other",
            "rank": "",
            "is_key_promotion": False,
            "notes": "2026年6月刘超荣拟任县委书记公示后，杨永冲去向尚未在公开渠道披露",
            "confidence": "unverified",
            "source_ids": [],
        },
    ],
    "organizations": [],
    "relationships": [
        {
            "person": "刘超荣",
            "person_id": "guangxi_pubei_liuchaorong",
            "relationship_type": "predecessor_successor",
            "strength": "strong",
            "evidence": "杨永冲为前任浦北县委书记，刘超荣接任；两人先后担任浦北县长职务",
            "overlap_org": "浦北县",
            "overlap_period": "2023-2026",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S003", "S006"],
        },
        {
            "person": "沈海涛",
            "person_id": "guangxi_pubei_shenhaitao",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "沈海涛2025年12月任浦北县委常委、常务副县长期间，在杨永冲领导下工作",
            "overlap_org": "浦北县",
            "overlap_period": "2025-2026",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S003", "S005"],
        },
        {
            "person": "陈柏",
            "person_id": "guangxi_pubei_chenbai",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "陈柏在杨永冲任县委书记期间任县委常委",
            "overlap_org": "中共浦北县委员会",
            "overlap_period": "",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
    ],
    "governance_record": [],
    "professional_profile": {
        "primary_specializations": ["化学工程", "石化产业管理"],
        "secondary_specializations": ["县域治理"],
        "career_pattern": "technical_specialist",
        "systems_experience": ["government"],
        "geographic_pattern": ["贵州印江→北京（清华）→广西钦州"],
        "promotion_velocity": {
            "summary": "清华大学博士（2011年毕业），选调至广西，约12年升正处级县委书记",
            "notable_fast_promotions": [
                "清华博士学历起点高，选调生身份",
                "约12年从选调生到县委书记",
            ]
        },
    },
    "work_style": {
        "public_style_indicators": [
            {"trait": "technocratic", "evidence": "清华大学化学系博士背景，技术型官员", "confidence": "confirmed", "source_ids": ["S006"]},
        ],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
    },
    "risk_signals": [
        {"type": "none_found", "description": "截至2026年7月，未在公开渠道发现杨永冲的纪律处分、审计问题或负面媒体报道", "date": TODAY, "confidence": "plausible", "source_ids": ["S006"]},
    ],
    "extra_sources": [
        {
            "id": "S006",
            "title": "网易订阅 - 浦北县委书记杨永冲简历",
            "url": "",
            "publisher": "网易订阅/新京报",
            "published_at": "",
            "accessed_at": TODAY,
            "source_type": "media",
            "reliability": "medium",
            "notes": "包含杨永冲的教育背景和主要任职信息",
        },
    ],
    "confidence_identity": "confirmed",
    "confidence_role": "confirmed",
    "career_completeness": "partial",
    "relationship_confidence": "medium",
    "biggest_gap": "杨永冲2011年选调后至任钦州市石化局局长期间的详细履历需要核实；2026年6月卸任县委书记后的去向未公开",
    "open_questions": [
        ("杨永冲2011年选调后在钦州市的具体早期任职经历？", "约10年的早期职业经历存在缺口", ["杨永冲 选调生 任职", "杨永冲 早期 履历"]),
        ("杨永冲卸任浦北县委书记后的去向？", "追踪干部调动路径", ["杨永冲 最新 任命", "杨永冲 去向"]),
    ],
})

# ════════════════════════════════════════════════════════════════
# WRITE PERSON JSONs
# ════════════════════════════════════════════════════════════════

def write_person_json(data, filename):
    path = PERSONS_OUT_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")

write_person_json(liuchaorong_json, f"{TODAY}-广西壮族自治区-钦州市-县委书记-刘超荣.json")
write_person_json(shenhaitao_json, f"{TODAY}-广西壮族自治区-钦州市-县长-沈海涛.json")
write_person_json(yangyongchong_json, f"{TODAY}-广西壮族自治区-钦州市-前任县委书记-杨永冲.json")

# ════════════════════════════════════════════════════════════════
# BUILD DATABASE & GEXF
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Building 浦北县 leadership network...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons dir: {PERSONS_OUT_DIR}")

    run_build(
        slug="浦北县领导班子关系图",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print("Done.")
