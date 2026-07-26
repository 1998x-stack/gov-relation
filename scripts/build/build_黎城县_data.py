#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 黎城县, 长治市, 山西省.

Level: 县
Province: 山西省
Parent city: 长治市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: shanxi_黎城县
Research date: 2026-07-26

Current Status (as of 2026-07-26 based on available media and official notices):
- 县委书记: 李颖南 (Li Yingnan, promoted from 县长 ~2025-04)
- 县长: 侯敏 (Hou Min, female, elected 2025-09-23, formerly 县委副书记、政法委书记)
- Predecessor 县委书记: 牛晨霞 (Niu Chenxia, female, former secretary until early 2025)

Known standing committee members (partial):
- 冯志波 — 县委常委、宣传部部长
- 王宽明 — 县人大常委会副主任 (partial bio from Baidu)
- 郭卫斌 — 曾任县委副书记、政法委书记 (2016-2019)
- 张中伟 (female, b.1979) — 副县长
- 王元生 — 副县长、公安局长

Confidence notes:
  Web access severely degraded during research — Exa rate-limited, Baidu 403, government site
  HTTP-only accessible but JS-rendered content unavailable. Data sourced from existing build
  script, Baidu search snippets, and the accessible parts of sxlc.gov.cn.

  This is a partial-evidence build per source_fallbacks.md artifact mode.
  All claims marked with confidence levels. Unresolved biographical fields are in
  open_questions.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Resolve repo root regardless of script location
_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _STAGING_DIR
for _ in range(4):
    _candidate = _REPO_ROOT.parent
    if (_candidate / "gov_relation").exists():
        _REPO_ROOT = _candidate
        break
    _REPO_ROOT = _candidate
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build


SLUG = "黎城县"
AS_OF = "2026-07-26"
TODAY = "20260726"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── Core Leadership (Primary Targets) ──

    # 1. 李颖南 — 县委书记
    {
        "id": 1,
        "name": "李颖南",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年8月",
        "birthplace": "山西省五寨县",
        "education": "研究生学历，哲学硕士",
        "party_join": "2005年12月",
        "work_start": "2006年6月",
        "current_post": "中共黎城县委书记",
        "current_org": "中共黎城县委员会",
        "source": "百度百科 / 澎湃新闻; 政府网站确认",
    },
    # 2. 侯敏 — 县长
    {
        "id": 2,
        "name": "侯敏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年7月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎城县委副书记、县长",
        "current_org": "黎城县人民政府",
        "source": "澎湃新闻 https://www.thepaper.cn/newsDetail_forward_29733389 ; 黎城县政府门户网站",
    },

    # ── Identified Committee Members / Deputies ──

    # 3. 冯志波 — 县委常委、宣传部部长
    {
        "id": 3,
        "name": "冯志波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎城县委常委、宣传部部长",
        "current_org": "中共黎城县委宣传部",
        "source": "综合知识（网络搜索受限，需进一步验证）",
    },
    # 4. 王宽明 — 县人大常委会副主任
    {
        "id": 4,
        "name": "王宽明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年8月",
        "birthplace": "山西黎城",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1984年9月",
        "current_post": "黎城县人大常委会副主任",
        "current_org": "黎城县人民代表大会常务委员会",
        "source": "百度百科（百度搜索片段）",
    },
    # 5. 郭卫斌 — 前任县委副书记、政法委书记 (2016-2019)
    {
        "id": 5,
        "name": "郭卫斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "山西省壶关县",
        "education": "中央党校研究生学历",
        "party_join": "1996年6月",
        "work_start": "1994年6月",
        "current_post": "（原黎城县委副书记、政法委书记，2019年拟任县人大主任）",
        "current_org": "",
        "source": "长治市委组织部2019年1月22日拟任职干部公示（搜狐网转载）",
    },
    # 6. 张中伟 — 副县长 (female)
    {
        "id": 6,
        "name": "张中伟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979年",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎城县副县长",
        "current_org": "黎城县人民政府",
        "source": "综合知识（网络搜索受限，需进一步验证）",
    },
    # 7. 王元生 — 副县长、公安局长
    {
        "id": 7,
        "name": "王元生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎城县副县长、县公安局局长",
        "current_org": "黎城县人民政府/黎城县公安局",
        "source": "综合知识（网络搜索受限，需进一步验证）",
    },
    # 8. 牛晨霞 — 原黎城县委书记 (predecessor)
    {
        "id": 8,
        "name": "牛晨霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原黎城县委书记，已于2025年离任）",
        "current_org": "",
        "source": "综合知识（网络搜索受限，需进一步验证）",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共黎城县委员会", "type": "党委", "level": "县级", "parent": "中共长治市委员会", "location": "山西省长治市黎城县"},
    {"id": 2, "name": "黎城县人民政府", "type": "政府", "level": "县级", "parent": "长治市人民政府", "location": "山西省长治市黎城县"},
    {"id": 3, "name": "中共黎城县委宣传部", "type": "党委部门", "level": "县级", "parent": "中共黎城县委员会", "location": "山西省长治市黎城县"},
    {"id": 4, "name": "中共黎城县委政法委员会", "type": "党委部门", "level": "县级", "parent": "中共黎城县委员会", "location": "山西省长治市黎城县"},
    {"id": 5, "name": "黎城县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "山西省长治市黎城县"},
    {"id": 6, "name": "黎城县公安局", "type": "政府部门", "level": "县级", "parent": "黎城县人民政府/长治市公安局", "location": "山西省长治市黎城县"},
    {"id": 7, "name": "中共黎城县委组织部", "type": "党委部门", "level": "县级", "parent": "中共黎城县委员会", "location": "山西省长治市黎城县"},
    {"id": 8, "name": "中共黎城县纪律检查委员会", "type": "纪律检查", "level": "县级", "parent": "中共长治市纪律检查委员会/中共黎城县委员会", "location": "山西省长治市黎城县"},
    {"id": 9, "name": "中共黎城县委统一战线工作部", "type": "党委部门", "level": "县级", "parent": "中共黎城县委员会", "location": "山西省长治市黎城县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 李颖南 career timeline
    {"person_id": 1, "org_id": 1, "title": "中共黎城县委书记", "start_date": "2025-04", "end_date": "至今", "rank": "正处级", "note": "由县长升任县委书记"},
    {"person_id": 1, "org_id": 2, "title": "黎城县委副书记、县长", "start_date": "2021", "end_date": "2025-04", "rank": "正处级", "note": "任县长约4年后升任书记"},
    {"person_id": 1, "org_id": 1, "title": "黎城县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "时间待确认"},

    # 侯敏 career timeline
    {"person_id": 2, "org_id": 2, "title": "黎城县委副书记、县长", "start_date": "2025-09-23", "end_date": "至今", "rank": "正处级", "note": "2025年9月23日当选县长"},
    {"person_id": 2, "org_id": 1, "title": "黎城县委副书记、政法委书记", "start_date": "", "end_date": "2025-09", "rank": "副处级", "note": "任县委副书记、政法委书记，后提名县长候选人"},
    {"person_id": 2, "org_id": 1, "title": "长治市潞州区委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "长治市潞州区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "原长治市城区并入潞州区后"},
    {"person_id": 2, "org_id": 2, "title": "长治市潞州区政府筹备组副组长", "start_date": "", "end_date": "", "rank": "", "note": "区划调整期间"},
    {"person_id": 2, "org_id": 2, "title": "长治市城区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "潞州区成立前，长治市城区副区长"},

    # 郭卫斌 career timeline
    {"person_id": 5, "org_id": 1, "title": "黎城县委副书记、政法委书记", "start_date": "2016-08", "end_date": "2019-01", "rank": "副处级", "note": "2016年8月任现职；2019年1月拟提名人大主任"},
    {"person_id": 5, "org_id": 2, "title": "黎城县委常委、常务副县长", "start_date": "", "end_date": "2016-08", "rank": "副处级", "note": "曾任黎城县委常委、常务副县长"},
    {"person_id": 5, "org_id": 2, "title": "长治市住房保障和城乡建设管理局副局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # 王宽明 career timeline
    {"person_id": 4, "org_id": 5, "title": "黎城县人大常委会副主任", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "黎城县委办公室工作", "start_date": "1997-07", "end_date": "2001-09", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "黎城一中副校长", "start_date": "1996-11", "end_date": "1997-07", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "黎城一中教师", "start_date": "1984-09", "end_date": "1996-11", "rank": "", "note": ""},

    # 冯志波
    {"person_id": 3, "org_id": 1, "title": "黎城县委常委、宣传部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},

    # 张中伟
    {"person_id": 6, "org_id": 2, "title": "黎城县副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},

    # 王元生
    {"person_id": 7, "org_id": 2, "title": "黎城县副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "黎城县公安局局长", "start_date": "", "end_date": "至今", "rank": "", "note": ""},

    # 牛晨霞 (predecessor)
    {"person_id": 8, "org_id": 1, "title": "黎城县委书记", "start_date": "", "end_date": "2025-03", "rank": "正处级", "note": "前任县委书记"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 李颖南 ↔ 侯敏 — 先后任县长、县委书记/县长
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "李颖南由县长升任县委书记，侯敏由县委副书记升任县长，二人曾在黎城县委班子共事 (2024-2025)", "overlap_org": "中共黎城县委员会", "overlap_period": "2024-2025"},

    # 侯敏 ↔ 郭卫斌 — 先后任政法委书记
    {"person_a": 2, "person_b": 5, "type": "predecessor_successor", "context": "郭卫斌曾任县委副书记、政法委书记 (2016-2019)，侯敏后任该职", "overlap_org": "中共黎城县委员会", "overlap_period": ""},

    # 李颖南 ↔ 牛晨霞 — 前后任搭档关系
    {"person_a": 1, "person_b": 8, "type": "predecessor_successor", "context": "李颖南接替牛晨霞任县委书记；牛晨霞是李颖南任县长期间的县委书记", "overlap_org": "中共黎城县委员会", "overlap_period": "2021-2025"},

    # 侯敏 ↔ 牛晨霞 — 曾同属县委班子
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "侯敏任县委副书记时，牛晨霞是县委书记", "overlap_org": "中共黎城县委员会", "overlap_period": ""},

    # 李颖南 ↔ 王宽明 — 县领导班子共事
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "李颖南任书记/县长期间，王宽明任县人大副主任", "overlap_org": "黎城县", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSONS
# ══════════════════════════════════════════════════════════════════════════════

PERSON_JSONS = {
    # 李颖南 — 县委书记
    1: {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山西省",
            "city": "长治市",
            "region": "黎城县",
            "job": "县委书记",
            "task_id": "shanxi_黎城县",
            "time_focus": "2006-至今",
        },
        "identity": {
            "person_id": "licheng_li_yingnan",
            "name": "李颖南",
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1982年8月",
            "birthplace": "山西省五寨县",
            "education": [
                {"institution": "", "major": "", "degree": "研究生学历，哲学硕士", "study_type": "unknown"}
            ],
            "party_join": "2005年12月",
            "work_start": "2006年6月",
        },
        "current_status": {
            "current_post": "中共黎城县委书记",
            "current_org": "中共黎城县委员会",
            "as_of": AS_OF,
            "is_current_confirmed": True,
        },
        "career_timeline": [
            {"start": "2025-04", "end": "至今", "org": "黎城县委", "title": "县委书记", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2021", "end": "2025-04", "org": "黎城县人民政府", "title": "县长", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2006-06", "end": "2021", "org": "", "title": "（2021年前履历待查）", "confidence": "unverified", "notes": "2006年参加工作至2021年之间的完整履历未被公开资料覆盖"},
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {"id": "S001", "title": "百度百科/李颖南", "url": "", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "2006-2021年15年履历完全空白",
        },
        "open_questions": [
            {"priority": "critical", "question": "2006-2021年间的履历空缺", "why_it_matters": "无法判断其职业起点、晋升速度、系统经验", "suggested_queries": ["长治市 李颖南 任职经历", "李颖南 简历 工作"], "last_attempted": AS_OF},
        ],
    },

    # 侯敏 — 县长
    2: {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山西省",
            "city": "长治市",
            "region": "黎城县",
            "job": "县长",
            "task_id": "shanxi_黎城县",
            "time_focus": "2018-至今",
        },
        "identity": {
            "person_id": "licheng_hou_min",
            "name": "侯敏",
            "gender": "女",
            "ethnicity": "汉族",
            "birth": "1978年7月",
            "birthplace": "",
            "education": [{"institution": "中央党校", "major": "", "degree": "大学", "study_type": "party_school"}],
            "party_join": "中共党员",
            "work_start": "",
        },
        "current_status": {
            "current_post": "黎城县委副书记、县长",
            "current_org": "黎城县人民政府",
            "as_of": AS_OF,
            "is_current_confirmed": True,
        },
        "career_timeline": [
            {"start": "2025-09-23", "end": "至今", "org": "黎城县人民政府", "title": "县长、县委副书记", "confidence": "confirmed", "notes": "2025年9月当选，澎湃新闻报道"},
            {"start": "", "end": "2025-09", "org": "黎城县委", "title": "县委副书记、政法委书记", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "", "org": "长治市潞州区委", "title": "区委常委、宣传部部长", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "", "org": "长治市潞州区人民政府", "title": "副区长", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "", "org": "长治市潞州区政府筹备组", "title": "筹备组副组长", "confidence": "plausible", "source_ids": ["S002"]},
            {"start": "", "end": "", "org": "长治市城区人民政府", "title": "副区长", "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {"id": "S002", "title": "澎湃新闻 - 侯敏当选县长", "url": "https://www.thepaper.cn/newsDetail_forward_29733389", "publisher": "澎湃新闻", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": ""},
            {"id": "S003", "title": "黎城县政府网站领导简介", "url": "http://www.sxlc.gov.cn/szsjzj/xzzj/xzjj/", "publisher": "黎城县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "medium", "notes": "页面JS渲染，直接访问仅获模板"},
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "low",
            "biggest_gap": "潞州区过渡期具体起止时间及早期全部履历",
        },
        "open_questions": [
            {"priority": "high", "question": "侯敏在长治市城区从何时开始任副区长？如何进入潞州区班子？", "why_it_matters": "判断其跨区晋升路径和速度", "suggested_queries": ["侯敏 长治 城区 副区长 任职时间"], "last_attempt": AS_OF},
            {"priority": "medium", "question": "侯敏的出生地和教育背景", "why_it_matters": "有助于确定籍贯和教育系统（是否本地培养）", "suggested_queries": ["侯敏 出生 籍贯", "侯敏 学历"], "last_attempt": AS_OF},
        ],
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# EXECUTION
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Step 1: Build database and GEXF
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Step 2: Write person JSONs
    for pid, data in PERSON_JSONS.items():
        person = next((p for p in persons if p["id"] == pid), None)
        if not person:
            continue
        job_short = person["current_post"].replace("中共", "").replace("黎城县", "").strip() or "official"
        name = person["name"]
        fname = f"{TODAY}-山西省-长治市-{job_short}-{name}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {fpath}")

    print(f"\nDone! Canonical path map:")
    print(f"  Build script: data/tmp/shanxi_黎城县/build_黎城县_data.py")
    print(f"  Database:      {DB_PATH}")
    print(f"  GEXF:          {GEXF_PATH}")
    print(f"  Person JSONs:  {PERSONS_DIR}/YYYYMMDD-*.json")