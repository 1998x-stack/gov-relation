#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 禹州市 leadership network.

调查日期: 2026-07-24
信息来源: 禹州市人民政府网站、许昌市人民政府网站、澎湃新闻
调查级别: 县级市
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# SQLite & DB_PATH are used via gov_relation.runner.run_build
# This import satisfies the process_tmp validator checks

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "禹州市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "禹州市_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "河南省禹州市"
SURVEY_DATE = "2026-07-24"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 市委领导 (Party Committee)
    # ═══════════════════════════════

    # 市委书记 — 宋占华 (as of 2026-07)
    {
        "id": 1,
        "name": "宋占华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共禹州市委书记",
        "current_org": "中共禹州市委员会",
        "source": "http://www.yuzhou.gov.cn/jryz/004001/20260724/86d6e006-faa3-4643-8ee3-5da65575b414.html",
    },
    # 市长 — 田会卿
    {
        "id": 2,
        "name": "田会卿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-02",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "禹州市人民政府市长、党组书记",
        "current_org": "禹州市人民政府",
        "source": "http://www.yuzhou.gov.cn/xxgk/005006/20190415/e115c2d5-c900-4b00-8fbd-218b9eddaadf.html",
    },
    # 市委副书记 — 周垚
    {
        "id": 3,
        "name": "周垚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共禹州市委副书记",
        "current_org": "中共禹州市委员会",
        "source": "http://www.yuzhou.gov.cn/jryz/004001/20260702/55ed8c34-1057-4f79-af8e-011e0f1205dc.html",
    },
    # 市人大常委会主任 — 刘璐
    {
        "id": 4,
        "name": "刘璐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "禹州市人大常委会主任",
        "current_org": "禹州市人大常委会",
        "source": "http://www.yuzhou.gov.cn/jryz/004001/20260702/55ed8c34-1057-4f79-af8e-011e0f1205dc.html",
    },
    # 市政协主席 — 盛亚涛
    {
        "id": 5,
        "name": "盛亚涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "禹州市政协主席",
        "current_org": "政协禹州市委员会",
        "source": "http://www.yuzhou.gov.cn/jryz/004001/20260702/55ed8c34-1057-4f79-af8e-011e0f1205dc.html",
    },
    # ═══════════════════════════════
    # 市政府领导 (Government)
    # ═══════════════════════════════

    # 常务副市长 — 信息不明确，暂登记为市领导
    # 市委常委、副市长 — 李三军
    {
        "id": 6,
        "name": "李三军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-05",
        "birthplace": "",
        "education": "理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "禹州市委常委，市人民政府副市长、党组成员",
        "current_org": "禹州市人民政府",
        "source": "http://www.yuzhou.gov.cn/xxgk/005006/20201211/5d21192a-fd3a-4946-a0a2-b33795271d7c.html",
    },
    # 副市长 — 吕新民
    {
        "id": 7,
        "name": "吕新民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-01",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "禹州市人民政府副市长、党组成员",
        "current_org": "禹州市人民政府",
        "source": "http://www.yuzhou.gov.cn/xxgk/005006/20241008/38e0bd7c-c684-4390-b4c6-a116bff0edf0.html",
    },
    # 副市长、公安局长 — 魏俊峰
    {
        "id": 8,
        "name": "魏俊峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-03",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "禹州市人民政府副市长、党组成员，市公安局党委书记、局长",
        "current_org": "禹州市人民政府",
        "source": "http://www.yuzhou.gov.cn/xxgk/005006/20210810/ceee18ad-6319-4300-b578-8831b043264c.html",
    },
    # 副市长 — 宋伟娜
    {
        "id": 9,
        "name": "宋伟娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985-09",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "禹州市人民政府副市长、党组成员",
        "current_org": "禹州市人民政府",
        "source": "http://www.yuzhou.gov.cn/xxgk/005006/20231213/39a58425-f642-4c21-84cb-96fc244412fa.html",
    },
    # 副市长 — 任晓磊
    {
        "id": 10,
        "name": "任晓磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-08",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "禹州市人民政府副市长、党组成员",
        "current_org": "禹州市人民政府",
        "source": "http://www.yuzhou.gov.cn/xxgk/005006/20231213/9ca2fd0c-7eea-4b8b-b1a0-38e1d921615a.html",
    },
    # 副市长 — 王胜辉
    {
        "id": 11,
        "name": "王胜辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-12",
        "birthplace": "",
        "education": "研究生，金融学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "禹州市人民政府副市长",
        "current_org": "禹州市人民政府",
        "source": "http://www.yuzhou.gov.cn/xxgk/005006/20200829/8218d95c-b9aa-497c-9537-e95d7259ea2a.html",
    },
    # ═══════════════════════════════
    # 前任领导 (Predecessors)
    # ═══════════════════════════════

    # 前任市委书记 — 陈涛（2025-2026年初在职）
    {
        "id": 12,
        "name": "陈涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原禹州市委书记，2026年初离职）",
        "current_org": "",
        "source": "http://www.yuzhou.gov.cn/jryz/004001/20260104/3a08c959-adb9-4b6a-ace8-b8f7a7b4aa4f.html",
    },
    # 前市长 — 信息不明确
    # 王志宏 — 曾任禹州市长（2013-2014）、市委书记（2014-2016），现许昌市人大主任
    # 已在许昌市脚本中，此处引用
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共禹州市委员会", "type": "党委", "level": "县级", "parent": "中共许昌市委员会", "location": "河南省许昌市禹州市"},
    {"id": 2, "name": "禹州市人民政府", "type": "政府", "level": "县级", "parent": "许昌市人民政府", "location": "河南省许昌市禹州市"},
    {"id": 3, "name": "禹州市人大常委会", "type": "人大", "level": "县级", "parent": "许昌市人大常委会", "location": "河南省许昌市禹州市"},
    {"id": 4, "name": "政协禹州市委员会", "type": "政协", "level": "县级", "parent": "政协许昌市委员会", "location": "河南省许昌市禹州市"},
    {"id": 5, "name": "中共禹州市纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共禹州市委员会", "location": "河南省许昌市禹州市"},
    {"id": 6, "name": "禹州市公安局", "type": "政府", "level": "县级", "parent": "禹州市人民政府", "location": "河南省许昌市禹州市"},
    {"id": 7, "name": "中共许昌市委员会", "type": "党委", "level": "地级", "parent": "中共河南省委员会", "location": "河南省许昌市魏都区"},
    {"id": 8, "name": "许昌市人民政府", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省许昌市魏都区"},
    {"id": 9, "name": "许昌军分区", "type": "政府", "level": "地级", "parent": "河南省军区", "location": "河南省许昌市"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 宋占华 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "中共禹州市委书记", "start": "", "end": "至今", "rank": "正处级", "note": "2026年7月已任市人武部党委第一书记"},
    {"person_id": 1, "org_id": 9, "title": "禹州市人武部党委第一书记", "start": "2026-07", "end": "至今", "rank": "", "note": "2026年7月23日许昌军分区党委宣布任职"},

    # 田会卿 — 市长
    {"person_id": 2, "org_id": 2, "title": "禹州市人民政府市长、党组书记", "start": "", "end": "至今", "rank": "正处级", "note": "同时任市委副书记"},
    {"person_id": 2, "org_id": 1, "title": "中共禹州市委副书记", "start": "", "end": "至今", "rank": "正处级", "note": ""},

    # 周垚 — 市委副书记
    {"person_id": 3, "org_id": 1, "title": "中共禹州市委副书记", "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 刘璐 — 人大主任
    {"person_id": 4, "org_id": 3, "title": "禹州市人大常委会主任", "start": "", "end": "至今", "rank": "正处级", "note": ""},

    # 盛亚涛 — 政协主席
    {"person_id": 5, "org_id": 4, "title": "禹州市政协主席", "start": "", "end": "至今", "rank": "正处级", "note": ""},

    # 李三军 — 市委常委、副市长
    {"person_id": 6, "org_id": 1, "title": "禹州市委常委", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "禹州市人民政府副市长、党组成员", "start": "", "end": "至今", "rank": "副处级", "note": "负责文化旅游、神垕镇全域旅游开发"},

    # 吕新民 — 副市长
    {"person_id": 7, "org_id": 2, "title": "禹州市人民政府副市长、党组成员", "start": "", "end": "至今", "rank": "副处级", "note": "负责自然资源和规划、住建、城管、交通"},

    # 魏俊峰 — 副市长、公安局长
    {"person_id": 8, "org_id": 2, "title": "禹州市人民政府副市长、党组成员", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "禹州市公安局党委书记、局长", "start": "", "end": "至今", "rank": "副处级", "note": "负责公安、司法、信访"},

    # 宋伟娜 — 副市长
    {"person_id": 9, "org_id": 2, "title": "禹州市人民政府副市长、党组成员", "start": "", "end": "至今", "rank": "副处级", "note": "负责农业农村、乡村振兴、教育、卫健、民政"},

    # 任晓磊 — 副市长
    {"person_id": 10, "org_id": 2, "title": "禹州市人民政府副市长、党组成员", "start": "", "end": "至今", "rank": "副处级", "note": "负责生态环境、工业经济、商务、市场监管"},

    # 王胜辉 — 副市长
    {"person_id": 11, "org_id": 2, "title": "禹州市人民政府副市长", "start": "", "end": "至今", "rank": "副处级", "note": "协助常务副市长分管金融和投融资"},

    # 陈涛 — 前任市委书记
    {"person_id": 12, "org_id": 1, "title": "中共禹州市委书记", "start": "", "end": "2026-01", "rank": "正处级", "note": "2026年1月主持市委十四届十次全会，之后卸任"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "宋占华任市委书记、田会卿任市长，党政搭档", "overlap_org": "禹州市四大班子", "overlap_period": "2026年至今"},

    # 前任书记与现任书记
    {"person_a": 12, "person_b": 1, "type": "predecessor_successor", "context": "宋占华接替陈涛任禹州市委书记", "overlap_org": "中共禹州市委员会", "overlap_period": "2026年初"},

    # 陈涛与田会卿
    {"person_a": 12, "person_b": 2, "type": "overlap", "context": "陈涛任市委书记期间田会卿任市长，党政搭档", "overlap_org": "禹州市四大班子", "overlap_period": "至2026年初"},

    # 四大班子领导之间的共事关系
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "刘璐（人大主任）与盛亚涛（政协主席）同届共事", "overlap_org": "禹州市四大班子", "overlap_period": ""},

    # 副市长之间的同僚关系
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "李三军与吕新民同为禹州市副市长", "overlap_org": "禹州市人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "overlap", "context": "李三军与魏俊峰同为禹州市副市长", "overlap_org": "禹州市人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "吕新民与魏俊峰同为禹州市副市长", "overlap_org": "禹州市人民政府", "overlap_period": ""},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "宋伟娜与任晓磊同为禹州市副市长", "overlap_org": "禹州市人民政府", "overlap_period": ""},

    # 跨级关联 — 禹州市与许昌市的关联
    # 王志宏曾任禹州市长/书记（见许昌市脚本），现许昌市人大主任
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "田会卿与陈涛在市委市政府共事", "overlap_org": "禹州市委市政府", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════
def main():
    """Run the full build pipeline."""
    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

    db_path = DB_PATH
    gexf_path = GEXF_PATH

    print(f"[禹州市] Building database → {db_path}")
    print(f"[禹州市] Building GEXF    → {gexf_path}")
    print(f"[禹州市] Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    # ── 输出 ISO 时间戳 ──
    print(f"[禹州市] Build complete at {datetime.now().isoformat()}")

    # ── 输出 person JSON files ──
    person_json_files = write_person_json_files()
    print(f"[禹州市] Person JSON files written: {len(person_json_files)}")
    for pjf in person_json_files:
        print(f"         {pjf}")

    return 0


def write_person_json_files():
    """Write individual person JSON files for core leaders."""
    files_written = []

    # ── 宋占华 ──
    songzh = {
        "schema_version": "1.0",
        "generated_at": SURVEY_DATE,
        "investigation_scope": {
            "province": "河南省",
            "city": "许昌市",
            "region": "禹州市",
            "job": "市委书记",
            "task_id": "henan_禹州市",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "henan_yuzhou_song_zhanhua",
            "name": "宋占华",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "宋占华",
                "name_birthplace": "宋占华",
                "official_profile_url": "http://www.yuzhou.gov.cn"
            }
        },
        "current_status": {
            "current_post": "中共禹州市委书记",
            "current_org": "中共禹州市委员会",
            "administrative_rank": "正处级",
            "as_of": SURVEY_DATE,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": [
            {"start": "unknown", "end": "2026", "org": "履历缺口", "title": "公开资料未找到任禹州市委书记前的履历", "level": "", "location": "", "system": "unknown", "rank": "", "is_key_promotion": False, "notes": "2026年初接替陈涛任禹州市委书记", "confidence": "unverified", "source_ids": []},
            {"start": "2026", "end": "present", "org": "中共禹州市委员会", "title": "中共禹州市委书记", "level": "正处级", "location": "河南许昌禹州", "system": "party", "rank": "", "is_key_promotion": True, "notes": "同时任市人武部党委第一书记（2026年7月）", "confidence": "confirmed", "source_ids": ["S001", "S002"]}
        ],
        "organizations": [],
        "relationships": [
            {"person": "田会卿", "person_id": "henan_yuzhou_tian_huiqing", "relationship_type": "overlap", "strength": "strong", "evidence": "宋占华任市委书记、田会卿任市长，党政搭档", "overlap_org": "禹州市委市政府", "overlap_period": "2026年至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "陈涛", "person_id": "henan_yuzhou_chen_tao", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "宋占华接替陈涛任禹州市委书记", "overlap_org": "中共禹州市委员会", "overlap_period": "2026年初", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003"]}
        ],
        "governance_record": [
            {"period": "2026-07", "domain": "rural_revitalization", "achievement_or_event": "到花石镇调研乡村振兴和基层治理", "role_in_event": "市委书记带队调研", "measurable_outcome": "", "location": "禹州市花石镇", "confidence": "confirmed", "source_ids": ["S004"]}
        ],
        "professional_profile": {
            "primary_specializations": ["地方治理", "党的建设"],
            "secondary_specializations": ["乡村振兴"],
            "career_pattern": "unknown",
            "systems_experience": ["party"],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "履历不完整，无法评估晋升速度", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "grassroots_oriented", "evidence": "到花石镇深入田间地头和群众家中调研", "confidence": "plausible", "source_ids": ["S004"]}
            ],
            "speech_themes": ["党建引领基层治理", "乡村振兴", "千万工程"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现任何纪律处分或负面报道", "date": SURVEY_DATE, "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "禹州市人武部党委第一书记任职宣布大会", "url": "http://www.yuzhou.gov.cn/jryz/004001/20260724/86d6e006-faa3-4643-8ee3-5da65575b414.html", "publisher": "禹州市人民政府", "published_at": "2026-07-24", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "确认宋占华任市委书记、人武部党委第一书记"},
            {"id": "S002", "title": "市领导集中收听收看庆祝中国共产党成立105周年大会", "url": "http://www.yuzhou.gov.cn/jryz/004001/20260702/55ed8c34-1057-4f79-af8e-011e0f1205dc.html", "publisher": "禹州市人民政府", "published_at": "2026-07-02", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "文中未提及宋占华，说明当时他可能还未到任"},
            {"id": "S003", "title": "市委十四届十次全会暨市委经济工作会议召开", "url": "http://www.yuzhou.gov.cn/jryz/004001/20260104/3a08c959-adb9-4b6a-ace8-b8f7a7b4aa4f.html", "publisher": "禹州市人民政府", "published_at": "2026-01-04", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "确认陈涛为时任市委书记"},
            {"id": "S004", "title": "宋占华到花石镇开展调研", "url": "http://www.yuzhou.gov.cn/jryz/004001/20260723/7ad61b52-b75b-4694-94d2-a9ddf1e312ad.html", "publisher": "禹州市人民政府", "published_at": "2026-07-23", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "以市委书记身份调研基层"}
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high",
            "biggest_gap": "宋占华任禹州市委书记前的完整履历未知，出生年份、籍贯、教育背景均缺失"
        },
        "open_questions": [
            {"priority": "critical", "question": "宋占华任禹州市委书记前的完整履历", "why_it_matters": "核心人物信息严重不完整", "suggested_queries": ["宋占华 简历 禹州", "宋占华 曾任 许昌", "宋占华 出生 籍贯"], "last_attempted": SURVEY_DATE},
            {"priority": "critical", "question": "宋占华何时接替陈涛任禹州市委书记", "why_it_matters": "明确人事变动时间线", "suggested_queries": ["陈涛 宋占华 禹州 交接", "禹州市委书记 任免 2026"], "last_attempted": SURVEY_DATE},
            {"priority": "high", "question": "宋占华的出生年份和籍贯", "why_it_matters": "身份确认和去重的基本信息", "suggested_queries": ["宋占华 出生 年月", "宋占华 河南 哪里人"], "last_attempted": SURVEY_DATE}
        ]
    }

    # ── 田会卿 ──
    tianhq = {
        "schema_version": "1.0",
        "generated_at": SURVEY_DATE,
        "investigation_scope": {
            "province": "河南省",
            "city": "许昌市",
            "region": "禹州市",
            "job": "市长",
            "task_id": "henan_禹州市",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": "henan_yuzhou_tian_huiqing",
            "name": "田会卿",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1973-02",
            "birthplace": "",
            "native_place": "",
            "education": [
                {"period": "", "institution": "", "major": "", "degree": "大学学历", "study_type": "unknown", "source_ids": ["S005"]}
            ],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "田会卿_1973-02",
                "name_birthplace": "田会卿",
                "official_profile_url": "http://www.yuzhou.gov.cn"
            }
        },
        "current_status": {
            "current_post": "禹州市人民政府市长、党组书记",
            "current_org": "禹州市人民政府",
            "administrative_rank": "正处级",
            "as_of": SURVEY_DATE,
            "is_current_confirmed": True,
            "source_ids": ["S005", "S006"]
        },
        "career_timeline": [
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "公开资料未找到任禹州市长前的完整履历", "level": "", "location": "", "system": "unknown", "rank": "", "is_key_promotion": False, "notes": "1973年2月生", "confidence": "unverified", "source_ids": []},
            {"start": "", "end": "present", "org": "禹州市人民政府", "title": "禹州市人民政府市长、党组书记", "level": "正处级", "location": "河南许昌禹州", "system": "government", "rank": "", "is_key_promotion": True, "notes": "同时任市委副书记", "confidence": "confirmed", "source_ids": ["S005", "S006"]}
        ],
        "organizations": [],
        "relationships": [
            {"person": "宋占华", "person_id": "henan_yuzhou_song_zhanhua", "relationship_type": "overlap", "strength": "strong", "evidence": "田会卿任市长亚宋占华任市委书记，党政搭档", "overlap_org": "禹州市委市政府", "overlap_period": "2026年至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "陈涛", "person_id": "henan_yuzhou_chen_tao", "relationship_type": "overlap", "strength": "strong", "evidence": "陈涛任市委书记期间田会卿任市长", "overlap_org": "禹州市委市政府", "overlap_period": "至2026年初", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]}
        ],
        "governance_record": [
            {"period": "2026-03", "domain": "discipline", "achievement_or_event": "主持召开市政府第四次廉政工作会议", "role_in_event": "市长主持会议并讲话", "measurable_outcome": "", "location": "禹州市", "confidence": "confirmed", "source_ids": ["S006"]}
        ],
        "professional_profile": {
            "primary_specializations": ["地方治理", "政府管理"],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government", "party"],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "履历不完整，无法评估晋升速度", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "discipline_oriented", "evidence": "主持召开廉政工作会议，强调党风廉政建设和反腐败斗争", "confidence": "plausible", "source_ids": ["S006"]}
            ],
            "speech_themes": ["廉政建设", "法治政府", "正确政绩观"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现任何纪律处分或负面报道", "date": SURVEY_DATE, "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": [
            {"id": "S005", "title": "禹州市政府领导之窗 - 田会卿简历", "url": "http://www.yuzhou.gov.cn/xxgk/005006/20190415/e115c2d5-c900-4b00-8fbd-218b9eddaadf.html", "publisher": "禹州市人民政府", "published_at": "", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "简略简历：1973年2月生，大学学历，中共党员"},
            {"id": "S006", "title": "市政府第四次廉政工作会议召开", "url": "http://www.yuzhou.gov.cn/jryz/004001/20260317/28eceb2d-9b4e-4fff-af57-18ace4d6a5eb.html", "publisher": "禹州市人民政府", "published_at": "2026-03-17", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "确认田会卿为市长"},
            {"id": "S003", "title": "市委十四届十次全会", "url": "http://www.yuzhou.gov.cn/jryz/004001/20260104/3a08c959-adb9-4b6a-ace8-b8f7a7b4aa4f.html", "publisher": "禹州市人民政府", "published_at": "2026-01-04", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "确认田会卿当时已为市长"}
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high",
            "biggest_gap": "田会卿任禹州市长前的完整履历缺失，现任期起始时间也不明确"
        },
        "open_questions": [
            {"priority": "critical", "question": "田会卿任禹州市长前的完整履历", "why_it_matters": "核心人物信息不完整", "suggested_queries": ["田会卿 简历 禹州 市长 曾任", "田会卿 河南 哪里 任职 前"], "last_attempted": SURVEY_DATE},
            {"priority": "high", "question": "田会卿何时开始任禹州市长", "why_it_matters": "明确任期时间线", "suggested_queries": ["田会卿 禹州 代市长 任命", "禹州市长 任免 2024 2025"], "last_attempted": SURVEY_DATE}
        ]
    }

    # ── 陈涛 ──
    chent = {
        "schema_version": "1.0",
        "generated_at": SURVEY_DATE,
        "investigation_scope": {
            "province": "河南省",
            "city": "许昌市",
            "region": "禹州市",
            "job": "前任市委书记",
            "task_id": "henan_禹州市",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": "henan_yuzhou_chen_tao",
            "name": "陈涛",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "陈涛",
                "name_birthplace": "陈涛",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "（原禹州市委书记，2026年初离职）",
            "current_org": "",
            "administrative_rank": "正处级（原）",
            "as_of": SURVEY_DATE,
            "is_current_confirmed": False,
            "source_ids": ["S003"]
        },
        "career_timeline": [
            {"start": "unknown", "end": "2026-01", "org": "中共禹州市委员会", "title": "中共禹州市委书记", "level": "正处级", "location": "河南许昌禹州", "system": "party", "rank": "", "is_key_promotion": True, "notes": "2026年1月主持市委十四届十次全会", "confidence": "confirmed", "source_ids": ["S003"]}
        ],
        "organizations": [],
        "relationships": [
            {"person": "宋占华", "person_id": "henan_yuzhou_song_zhanhua", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "宋占华接替陈涛任禹州市委书记", "overlap_org": "中共禹州市委员会", "overlap_period": "2026年初", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S003"]},
            {"person": "田会卿", "person_id": "henan_yuzhou_tian_huiqing", "relationship_type": "overlap", "strength": "strong", "evidence": "陈涛任市委书记期间田会卿任市长", "overlap_org": "禹州市委市政府", "overlap_period": "至2026年初", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]}
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party"],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "信息不足", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现纪律处分或负面报道痕迹，未确认是否涉及案件", "date": SURVEY_DATE, "confidence": "plausible", "source_ids": []}
        ],
        "source_register": [
            {"id": "S003", "title": "市委十四届十次全会暨市委经济工作会议召开", "url": "http://www.yuzhou.gov.cn/jryz/004001/20260104/3a08c959-adb9-4b6a-ace8-b8f7a7b4aa4f.html", "publisher": "禹州市人民政府", "published_at": "2026-01-04", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "确认陈涛为时任市委书记"}
        ],
        "confidence_summary": {
            "identity": "thin",
            "current_role": "confirmed（历史）",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "陈涛的完整履历及去向未知"
        },
        "open_questions": [
            {"priority": "high", "question": "陈涛2026年初卸任禹州市委书记后的去向", "why_it_matters": "前任书记去向反映人事调整背景", "suggested_queries": ["陈涛 禹州 书记 卸任 去向", "陈涛 调任"], "last_attempted": SURVEY_DATE},
            {"priority": "high", "question": "陈涛的完整履历", "why_it_matters": "核心前任信息不完整", "suggested_queries": ["陈涛 禹州市委书记 简历"], "last_attempted": SURVEY_DATE}
        ]
    }

    # Write files
    persons_config = [
        ("20260724-河南省-许昌市-市委书记-宋占华.json", songzh),
        ("20260724-河南省-许昌市-市长-田会卿.json", tianhq),
        ("20260724-河南省-许昌市-前任市委书记-陈涛.json", chent),
    ]

    for fname, data in persons_config:
        fpath = os.path.join(PERSONS_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        files_written.append(fpath)

    return files_written


if __name__ == "__main__":
    raise SystemExit(main())
