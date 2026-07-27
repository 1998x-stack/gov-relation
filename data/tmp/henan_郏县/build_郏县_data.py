#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 郏县 (Jia County), 平顶山市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_郏县
Level: 县
Targets: 县委书记 & 县长

Research constraints:
  - Exa search: rate-limited (free tier exhausted)
  - Baidu: 403/blocked
  - Jina Reader: timed out
  - Google: blocked by captcha

Evidence approach:
  - 县政府领导信息来自郏县人民政府官方网站 (www.jiaxian.gov.cn)
  - 县长王铮: confirmed from official profile page
  - 常务副县长杨兆华、副县长王芳/李政杰/杨继朝/张怡/赵萌: confirmed from official profile pages
  - 县委书记: information from training data knowledge; not listed on government site
  - 县委常委名单: partially confirmed from government page (杨兆华、王芳 as 县委常委)
  - This is a partial-evidence artifact following the source_fallbacks playbook:
    create valid artifacts with explicit uncertainty markers

Confidence notes:
  - 王铮 (县长): confirmed — 县政府官方网站公布简历
  - 杨兆华 (常务副县长): confirmed — 县政府官方网站公布简历
  - 王芳 (宣传部长/副县长): confirmed — 县政府官方网站公布简历
  - 其他副县长: confirmed — 县政府官方网站公布简历
  - 县委书记及其他县委常委: plausible — 训练数据知识，未经官方网站核实
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
os.chdir(str(BASE_DIR))
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "郏县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

CANONICAL_DB = DATABASE_DIR / f"{SLUG}_network.db"
CANONICAL_GEXF = GRAPH_DIR / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE_DIR / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE_DIR / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "王景育",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共郏县委员会",
        "source": "训练数据知识——王景育约2021年起任郏县县委书记；此前曾任郏县县长（确切信息待官方确认）"
    },
    {
        "id": 2,
        "name": "王铮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年1月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "郏县人民政府",
        "source": "https://www.jiaxian.gov.cn/contents/31712/255245.html — 郏县人民政府官方网站领导简历页（confirmed）"
    },
    # ═══════ Previous Leadership ═══════
    {
        "id": 3,
        "name": "李红民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县长",
        "current_org": "",
        "source": "训练数据知识——李红民此前曾任郏县县长，约2021年被王铮接替"
    },
    # ═══════ County Party Standing Committee ═══════
    {
        "id": 4,
        "name": "杨兆华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年4月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "郏县人民政府",
        "source": "https://www.jiaxian.gov.cn/contents/31712/255244.html — confirmed"
    },
    {
        "id": 5,
        "name": "王芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、副县长",
        "current_org": "中共郏县县委宣传部",
        "source": "https://www.jiaxian.gov.cn/contents/31712/466560.html — confirmed"
    },
    # ═══════ County Government Deputies ═══════
    {
        "id": 6,
        "name": "李政杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年7月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "郏县人民政府",
        "source": "https://www.jiaxian.gov.cn/contents/31712/255237.html — confirmed"
    },
    {
        "id": 7,
        "name": "杨继朝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "郏县人民政府",
        "source": "https://www.jiaxian.gov.cn/contents/31712/297761.html — confirmed"
    },
    {
        "id": 8,
        "name": "张怡",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "郏县人民政府",
        "source": "https://www.jiaxian.gov.cn/contents/31712/297763.html — confirmed"
    },
    {
        "id": 9,
        "name": "赵萌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年12月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中国民主同盟盟员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "郏县人民政府",
        "source": "https://www.jiaxian.gov.cn/contents/31712/391372.html — confirmed"
    },
    {
        "id": 10,
        "name": "黄运宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年11月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三级调研员",
        "current_org": "郏县人民政府",
        "source": "https://www.jiaxian.gov.cn/contents/31712/255236.html — confirmed"
    },
    {
        "id": 11,
        "name": "王应钦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年4月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、办公室主任",
        "current_org": "郏县人民政府办公室",
        "source": "https://www.jiaxian.gov.cn/contents/31712/300510.html — confirmed"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共郏县委员会", "type": "党委", "level": "县", "parent": "中共平顶山市委", "location": "郏县"},
    {"id": 2, "name": "郏县人民政府", "type": "政府", "level": "县", "parent": "平顶山市人民政府", "location": "郏县"},
    {"id": 3, "name": "中共郏县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共郏县委员会", "location": "郏县"},
    {"id": 4, "name": "郏县监察委员会", "type": "党委", "level": "县", "parent": "中共郏县委员会", "location": "郏县"},
    {"id": 5, "name": "中共郏县县委宣传部", "type": "党委", "level": "县", "parent": "中共郏县委员会", "location": "郏县"},
    {"id": 6, "name": "郏县公安局", "type": "政府", "level": "县", "parent": "郏县人民政府", "location": "郏县"},
    {"id": 7, "name": "郏县人民政府办公室", "type": "政府", "level": "县", "parent": "郏县人民政府", "location": "郏县"},
    {"id": 8, "name": "郏县人大常委会", "type": "人大", "level": "县", "parent": "平顶山市人大常委会", "location": "郏县"},
    {"id": 9, "name": "政协郏县委员会", "type": "政协", "level": "县", "parent": "政协平顶山市委员会", "location": "郏县"},
    {"id": 10, "name": "中共平顶山市委", "type": "党委", "level": "地级市", "parent": "中共河南省委", "location": "平顶山市"},
    {"id": 11, "name": "平顶山市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "平顶山市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 王景育 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "约2021", "end_date": "至今", "rank": "正县级", "note": "推测从县长升任"},
    {"person_id": 1, "org_id": 2, "title": "县长", "start_date": "约2019", "end_date": "约2021", "rank": "正县级", "note": "此前担任郏县县长（待核实）"},
    # 王铮 — 县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "约2022", "end_date": "至今", "rank": "正县级", "note": "1981年1月生，本科"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "约2022", "end_date": "至今", "rank": "副县级", "note": "县委副书记、县长"},
    # 李红民 — 前任县长
    {"person_id": 3, "org_id": 2, "title": "县长", "start_date": "约2019", "end_date": "约2021", "rank": "正县级", "note": "前任县长"},
    # 杨兆华
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": "1978年4月生，研究生"},
    # 王芳
    {"person_id": 5, "org_id": 5, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": "1976年10月生，研究生"},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": "兼任副县长"},
    # 李政杰
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": "1971年7月生，本科"},
    # 杨继朝
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": "1973年12月生，研究生"},
    {"person_id": 7, "org_id": 6, "title": "县公安局局长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": "兼任县公安局局长"},
    # 张怡
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": "1982年9月生，研究生"},
    # 赵萌
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": "1980年12月生，本科，民盟"},
    # 黄运宏
    {"person_id": 10, "org_id": 2, "title": "三级调研员", "start_date": "", "end_date": "至今", "rank": "三级调研员", "note": "1970年11月生，本科"},
    # 王应钦
    {"person_id": 11, "org_id": 7, "title": "县政府党组成员、办公室主任", "start_date": "", "end_date": "至今", "rank": "正科级", "note": "1980年4月生，研究生"},
]

# ── Relationships ─────────────────────────────────────────────────────────
relationships = [
    # 王景育 — 王铮（县委书记与县长）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长工作搭档", "overlap_org": "郏县", "overlap_period": "约2022至今"},
    # 王景育 — 李红民（前后任县长关系）
    {"person_a": 1, "person_b": 3, "type": "前后任", "context": "王景育接替李红民任县长（王此前为县长）", "overlap_org": "郏县人民政府", "overlap_period": ""},
    # 王景育 — 杨兆华（上下级）
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记与常务副县长", "overlap_org": "中共郏县委员会", "overlap_period": ""},
    # 王铮 — 杨兆华（党政搭档）
    {"person_a": 2, "person_b": 4, "type": "党政搭档", "context": "县长与常务副县长工作搭档", "overlap_org": "郏县人民政府", "overlap_period": ""},
    # 王铮 — 其他副县长（领导关系）
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长与副县长", "overlap_org": "郏县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长与副县长、公安局长", "overlap_org": "郏县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长与副县长", "overlap_org": "郏县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长与副县长", "overlap_org": "郏县人民政府", "overlap_period": ""},
    # 县委常委关系
    {"person_a": 4, "person_b": 5, "type": "共事", "context": "同为县委常委", "overlap_org": "中共郏县委员会", "overlap_period": ""},
    # 王芳 — 李政杰等（同为副县长）
    {"person_a": 5, "person_b": 6, "type": "共事", "context": "同为副县长", "overlap_org": "郏县人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "共事", "context": "同为副县长", "overlap_org": "郏县人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "共事", "context": "同为副县长", "overlap_org": "郏县人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "共事", "context": "同为副县长", "overlap_org": "郏县人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "共事", "context": "同为副县长", "overlap_org": "郏县人民政府", "overlap_period": ""},
    {"person_a": 8, "person_b": 9, "type": "共事", "context": "同为副县长", "overlap_org": "郏县人民政府", "overlap_period": ""},
]


# ── Person JSON Writer ────────────────────────────────────────────────────
def make_source_register():
    return [
        {"id": "S001", "title": "郏县人民政府—县政府领导", "url": "https://www.jiaxian.gov.cn/channels/31712.html", "publisher": "郏县人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "郏县人民政府官方网站，县政府领导信息公开"},
        {"id": "S002", "title": "县长王铮官方简历", "url": "https://www.jiaxian.gov.cn/contents/31712/255245.html", "publisher": "郏县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县长王铮出生年月、学历等信息"},
        {"id": "S003", "title": "常务副县长杨兆华官方简历", "url": "https://www.jiaxian.gov.cn/contents/31712/255244.html", "publisher": "郏县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S004", "title": "副县长王芳官方简历", "url": "https://www.jiaxian.gov.cn/contents/31712/466560.html", "publisher": "郏县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S005", "title": "副县长李政杰官方简历", "url": "https://www.jiaxian.gov.cn/contents/31712/255237.html", "publisher": "郏县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S006", "title": "副县长、公安局长杨继朝官方简历", "url": "https://www.jiaxian.gov.cn/contents/31712/297761.html", "publisher": "郏县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S007", "title": "副县长张怡官方简历", "url": "https://www.jiaxian.gov.cn/contents/31712/297763.html", "publisher": "郏县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S008", "title": "副县长赵萌官方简历", "url": "https://www.jiaxian.gov.cn/contents/31712/391372.html", "publisher": "郏县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S009", "title": "三级调研员黄运宏官方简历", "url": "https://www.jiaxian.gov.cn/contents/31712/255236.html", "publisher": "郏县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S010", "title": "县政府办公室主任王应钦简历", "url": "https://www.jiaxian.gov.cn/contents/31712/300510.html", "publisher": "郏县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S011", "title": "郏县人民政府门户网站首页", "url": "https://www.jiaxian.gov.cn", "publisher": "郏县人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "获取了网站架构和栏目信息"},
    ]


def write_person_jsons():
    sr = make_source_register()

    person_relationships = {p["id"]: [] for p in persons}
    for r in relationships:
        person_relationships.setdefault(r["person_a"], []).append(r)
        person_relationships.setdefault(r["person_b"], []).append(r)

    # Person JSON configs: person_id, job_title in filename, name
    configs = [
        (1, "县委书记", "王景育"),
        (2, "县长", "王铮"),
        (4, "常务副县长", "杨兆华"),
        (5, "宣传部长", "王芳"),
    ]

    for pid, job, name in configs:
        p = next(x for x in persons if x["id"] == pid)
        p_positions = [pos for pos in positions if pos["person_id"] == pid]
        timeline = []
        for pos in p_positions:
            timeline.append({
                "start": pos.get("start_date", ""),
                "end": pos.get("end_date", ""),
                "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
                "title": pos["title"],
                "level": pos.get("rank", ""),
                "location": "平顶山市郏县",
                "system": "party" if "县委" in pos["title"] or "书记" in pos["title"] else "government",
                "rank": pos.get("rank", ""),
                "is_key_promotion": "县委书记" in pos["title"] or "县长" == pos["title"],
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if pid != 1 else "plausible",
                "source_ids": ["S001", "S002"] if pid == 2 else (["S001"] if pid != 1 else [])
            })

        # Relationships for this person
        rels = []
        for r in person_relationships.get(pid, []):
            other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
            other = next((x for x in persons if x["id"] == other_id), None)
            if other:
                rels.append({
                    "person": other["name"],
                    "person_id": f"jiaxian_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] in ("党政搭档", "上下级") else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed" if pid != 1 and other_id != 1 else "plausible",
                    "source_ids": []
                })

        # Education
        education_list = []
        if p.get("education"):
            education_list.append({
                "period": "",
                "institution": "",
                "major": "",
                "degree": p["education"],
                "study_type": "unknown",
                "source_ids": []
            })

        # Risk signals
        risk_signals = [{"type": "none_found", "description": "本次调研未发现王景育的纪律处分、审计问题或负面报道", "date": "", "confidence": "unverified", "source_ids": [] if pid != 1 else []}]

        is_party_secretary = "县委书记" in p["current_post"]
        is_county_mayor = "县长" == p["current_post"]

        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "平顶山市",
                "region": "郏县",
                "job": p["current_post"],
                "task_id": "henan_郏县",
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"jiaxian_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": education_list,
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p["current_post"],
                "current_org": p["current_org"],
                "administrative_rank": "正县级" if (is_party_secretary or is_county_mayor) else "副县级",
                "as_of": AS_OF,
                "is_current_confirmed": True if pid != 1 else False,
                "source_ids": ["S001", "S002"] if pid == 2 else (["S001"] if pid == 4 or pid == 5 else [])
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": rels,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": risk_signals,
            "source_register": sr,
            "confidence_summary": {
                "identity": "confirmed" if pid != 1 else "plausible",
                "current_role": "confirmed" if pid != 1 else "plausible",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "公开资料受限，无法获取完整履历、出生地和籍贯等详细信息"
            },
            "open_questions": [
                {"priority": "critical", "question": f"{p['name']}的完整履历", "why_it_matters": "核心领导人履历是关系网络的基础", "suggested_queries": [f"{p['name']} 简历 郏县", f"{p['name']} 任前公示 平顶山", f"{p['name']} 百度百科"], "last_attempted": AS_OF},
                {"priority": "high", "question": f"{p['name']}的出生地和籍贯", "why_it_matters": "用于身份识别和去重", "suggested_queries": [f"{p['name']} 出生 郏县", f"{p['name']} 籍贯"], "last_attempted": AS_OF},
            ]
        }
        if pid == 1:
            result["open_questions"].insert(1, {
                "priority": "critical",
                "question": "王景育是否仍为郏县县委书记",
                "why_it_matters": "县委书记是核心目标人物，但其身份未经官方网站确认",
                "suggested_queries": ["郏县县委书记 2026", "王景育 郏县 2026", "郏县县委领导分工"],
                "last_attempted": AS_OF
            })

        filename = f"{TODAY}-河南省-平顶山市-{job}-{p['name']}.json"
        filepath = STAGING_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filepath}")


# ── Build ──────────────────────────────────────────────────────────────────
def main():
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

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

    write_person_jsons()

    print(f"\n=== Build Summary ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Staging: {STAGING_DIR}")
    print("Done.")


if __name__ == "__main__":
    main()
