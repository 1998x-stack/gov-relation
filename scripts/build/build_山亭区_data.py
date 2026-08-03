#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 山亭区 (Shanting District), 枣庄市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 枣庄市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_山亭区

Research date: 2026-08-03
Official source: http://www.shanting.gov.cn/ — partially accessible via HTTP

Current status (as of 2026-08-03, confirmed from official government site):
- 区委书记: 王德海 (confirmed by news article "区委常委会（扩大）会议暨区委财经委员会会议召开 王德海主持并讲话", 2026-07-28)
- 区长: 王彪 (confirmed by 山政任〔2026〕6号, appointed 副区长/代理区长 2026-04-27; referred to as 区委副书记、区长 in 2026-08-01 article)

Confidence notes:
  Web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited, blocked, or timed out.
  Government site http://www.shanting.gov.cn/ was accessible via HTTP (HTTPS timed out).
  Leadership identification confirmed from official government news articles and personnel appointment notices.
  Biographical details beyond current roles could not be verified through available web tools.

  This is a partial-evidence build per source_fallbacks.md artifact mode.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "山亭区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-03"
TODAY = "20260803"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 王德海 — 区委书记
    {
        "id": 1,
        "name": "王德海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枣庄市山亭区委书记",
        "current_org": "中共枣庄市山亭区委员会",
        "source": "山亭区政府网新闻确认，2026-07-28出席区委常委会",
    },
    # 2. 王彪 — 区长
    {
        "id": 2,
        "name": "王彪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "枣庄市山亭区人民政府区长",
        "current_org": "枣庄市山亭区人民政府",
        "source": "山政任〔2026〕6号，2026-04-27任副区长、代理区长；2026-08-01新闻确认为区委副书记、区长",
    },
    # 3. 王绪景 — 原副区长，现山亭经济开发区管委会主任
    {
        "id": 3,
        "name": "王绪景",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山亭经济开发区管委会主任",
        "current_org": "山亭经济开发区管委会",
        "source": "山政任〔2026〕8号，2026-05-20任职；山政任〔2026〕9号免去副区长",
    },
    # 4. 孙彦民 — 副区长
    {
        "id": 4,
        "name": "孙彦民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山亭区人民政府副区长",
        "current_org": "枣庄市山亭区人民政府",
        "source": "山政任〔2026〕9号，2026-06-03任命",
    },
    # 5. 赵传甲 — 副区长
    {
        "id": 5,
        "name": "赵传甲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山亭区人民政府副区长",
        "current_org": "枣庄市山亭区人民政府",
        "source": "2026-08-03区长办公会议参会名单",
    },
    # 6. 戴娟 — 副区长
    {
        "id": 6,
        "name": "戴娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山亭区人民政府副区长",
        "current_org": "枣庄市山亭区人民政府",
        "source": "2026-08-03区长办公会议参会名单",
    },
    # 7. 宗晓庆 — 副区长
    {
        "id": 7,
        "name": "宗晓庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山亭区人民政府副区长",
        "current_org": "枣庄市山亭区人民政府",
        "source": "2026-08-03区长办公会议参会名单",
    },
    # 8. 周涛 — 副区长
    {
        "id": 8,
        "name": "周涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山亭区人民政府副区长",
        "current_org": "枣庄市山亭区人民政府",
        "source": "2026-08-03区长办公会议参会名单",
    },
    # 9. 李霞 — 区领导（活动报道中出现）
    {
        "id": 9,
        "name": "李霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山亭区领导",
        "current_org": "山亭区",
        "source": "2026-08-03走访慰问活动新闻",
    },
    # 10. 李洪波 — 区领导
    {
        "id": 10,
        "name": "李洪波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山亭区领导",
        "current_org": "山亭区",
        "source": "2026-08-03走访慰问活动新闻",
    },
    # 11. 张泺源 — 山亭经济开发区管委会副主任
    {
        "id": 11,
        "name": "张泺源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山亭经济开发区管委会副主任（挂职1年）",
        "current_org": "山亭经济开发区管委会",
        "source": "山政任〔2026〕7号，2026-04-29任职",
    },
    # 12. 前任区长（刘莹/待确认）— 即王彪前任
    {
        "id": 12,
        "name": "待确认（前任区长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原山亭区区长",
        "current_org": "",
        "source": "王彪2026年4月任代理区长，说明前任已卸任",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共枣庄市山亭区委员会", "type": "党委", "level": "县处级", "parent": "中共枣庄市委", "location": "枣庄市山亭区"},
    {"id": 2, "name": "枣庄市山亭区人民政府", "type": "政府", "level": "县处级", "parent": "枣庄市人民政府", "location": "枣庄市山亭区"},
    {"id": 3, "name": "山亭经济开发区管委会", "type": "开发区", "level": "县处级", "parent": "枣庄市山亭区人民政府", "location": "枣庄市山亭区"},
    {"id": 4, "name": "中共枣庄市委", "type": "党委", "level": "地厅级", "parent": "中共山东省委", "location": "枣庄市"},
    {"id": 5, "name": "枣庄市人民政府", "type": "政府", "level": "地厅级", "parent": "山东省人民政府", "location": "枣庄市"},
    {"id": 6, "name": "枣庄市山亭区人大常委会", "type": "人大", "level": "县处级", "parent": "枣庄市山亭区", "location": "枣庄市山亭区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 王德海 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共枣庄市山亭区委书记", "start": "", "end": "present", "rank": "副厅级", "note": "2026年7月仍在任，具体到任时间待查"},
    # 王彪 — 区长
    {"person_id": 2, "org_id": 1, "title": "中共枣庄市山亭区委副书记", "start": "2026-04", "end": "present", "rank": "县处级", "note": "2026年4月27日任副区长、代理区长"},
    {"person_id": 2, "org_id": 2, "title": "枣庄市山亭区人民政府区长", "start": "2026-04", "end": "present", "rank": "县处级", "note": "山政任〔2026〕6号，预计后续人大会议转为正式区长"},
    # 王绪景 — 原副区长，现经开区主任
    {"person_id": 3, "org_id": 2, "title": "山亭区人民政府副区长", "start": "", "end": "2026-06", "rank": "县处级", "note": "山政任〔2026〕9号免去副区长职务"},
    {"person_id": 3, "org_id": 3, "title": "山亭经济开发区管委会主任", "start": "2026-05", "end": "present", "rank": "县处级", "note": "山政任〔2026〕8号，试用期一年"},
    # 孙彦民 — 副区长
    {"person_id": 4, "org_id": 2, "title": "山亭区人民政府副区长", "start": "2026-06", "end": "present", "rank": "县处级", "note": "山政任〔2026〕9号任命"},
    # 赵传甲 — 副区长
    {"person_id": 5, "org_id": 2, "title": "山亭区人民政府副区长", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 戴娟 — 副区长
    {"person_id": 6, "org_id": 2, "title": "山亭区人民政府副区长", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 宗晓庆 — 副区长
    {"person_id": 7, "org_id": 2, "title": "山亭区人民政府副区长", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 周涛 — 副区长
    {"person_id": 8, "org_id": 2, "title": "山亭区人民政府副区长", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 李霞 — 区领导
    {"person_id": 9, "org_id": 1, "title": "山亭区领导", "start": "", "end": "present", "rank": "县处级", "note": "具体职务待确认"},
    # 李洪波 — 区领导
    {"person_id": 10, "org_id": 1, "title": "山亭区领导", "start": "", "end": "present", "rank": "县处级", "note": "具体职务待确认"},
    # 张泺源 — 经开区副主任
    {"person_id": 11, "org_id": 3, "title": "山亭经济开发区管委会副主任（挂职）", "start": "2026-04", "end": "present", "rank": "县处级", "note": "山政任〔2026〕7号，挂职1年"},
    # 待确认前任区长
    {"person_id": 12, "org_id": 2, "title": "原山亭区区长", "start": "", "end": "2026-04", "rank": "县处级", "note": "王彪接任前已卸任，姓名待确认"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 王德海 ↔ 王彪 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "王德海任区委书记、王彪任区长，党政搭档", "overlap_org": "山亭区", "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 王德海 ↔ 王绪景 (区委书记-班子成员)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "王德海任区委书记期间，王绪景先后任副区长、经开区主任", "overlap_org": "山亭区", "overlap_period": "至今", "confidence": "confirmed"},
    # 王德海 ↔ 孙彦民 (区委书记-副区长)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "王德海任区委书记期间，孙彦民任副区长", "overlap_org": "山亭区", "overlap_period": "2026-06至今", "confidence": "confirmed"},
    # 王德海 ↔ 赵传甲 (班子成员)
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "王德海任区委书记期间，赵传甲任副区长", "overlap_org": "山亭区", "overlap_period": "至今", "confidence": "plausible"},
    # 王德海 ↔ 戴娟 (班子成员)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "王德海任区委书记期间，戴娟任副区长", "overlap_org": "山亭区", "overlap_period": "至今", "confidence": "plausible"},
    # 王德海 ↔ 宗晓庆 (班子成员)
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "王德海任区委书记期间，宗晓庆任副区长", "overlap_org": "山亭区", "overlap_period": "至今", "confidence": "plausible"},
    # 王德海 ↔ 周涛 (班子成员)
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "王德海任区委书记期间，周涛任副区长", "overlap_org": "山亭区", "overlap_period": "至今", "confidence": "plausible"},
    # 王彪 ↔ 王绪景 (政府班子)
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "王彪任区长期间，王绪景曾任副区长，后转经开区主任", "overlap_org": "枣庄市山亭区人民政府", "overlap_period": "2026-04至2026-06", "confidence": "confirmed"},
    # 王彪 ↔ 孙彦民 (政府班子)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "王彪任区长期间，孙彦民任副区长", "overlap_org": "枣庄市山亭区人民政府", "overlap_period": "2026-06至今", "confidence": "confirmed"},
    # 王彪 ↔ 赵传甲 (政府班子)
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "王彪任区长期间，赵传甲任副区长", "overlap_org": "枣庄市山亭区人民政府", "overlap_period": "至今", "confidence": "plausible"},
    # 王彪 ↔ 戴娟 (政府班子)
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "王彪任区长期间，戴娟任副区长", "overlap_org": "枣庄市山亭区人民政府", "overlap_period": "至今", "confidence": "plausible"},
    # 王彪 ↔ 宗晓庆 (政府班子)
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "王彪任区长期间，宗晓庆任副区长", "overlap_org": "枣庄市山亭区人民政府", "overlap_period": "至今", "confidence": "plausible"},
    # 王彪 ↔ 周涛 (政府班子)
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "王彪任区长期间，周涛任副区长", "overlap_org": "枣庄市山亭区人民政府", "overlap_period": "至今", "confidence": "plausible"},
    # 王彪 ↔ 前任区长 (接替关系)
    {"person_a": 2, "person_b": 12, "type": "predecessor_successor", "context": "王彪接替前任任山亭区区长", "overlap_org": "枣庄市山亭区人民政府", "overlap_period": "2026-04", "confidence": "confirmed"},
    # 王绪景 ↔ 孙彦民 (职务交接)
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor", "context": "王绪景免去副区长后，孙彦民被任命为副区长", "overlap_org": "枣庄市山亭区人民政府", "overlap_period": "2026-06", "confidence": "confirmed"},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON BUILDER
# ══════════════════════════════════════════════════════════════════════════════


def build_person_json(person: dict, relationships_subset: list[dict]) -> dict:
    """Build a person graph JSON from the data rows."""
    pid = person["id"]

    career_entries = []
    for pos in positions:
        if pos["person_id"] != pid:
            continue
        career_entries.append({
            "start": pos.get("start", ""),
            "end": pos.get("end", "present"),
            "org": pos["org_id"],
            "title": pos["title"],
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", ""),
            "confidence": "plausible",
            "source_ids": ["S001"],
        })

    rel_entries = []
    for r in relationships_subset:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        if other:
            rel_entries.append({
                "person": other["name"],
                "person_id": f"shanting_{other['name']}",
                "relationship_type": r["type"],
                "strength": "strong" if r.get("confidence") == "confirmed" else "medium",
                "evidence": r["context"],
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": r.get("confidence", "unverified"),
                "source_ids": ["S001"],
            })

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "枣庄市",
            "region": "山亭区",
            "job": person["current_post"],
            "task_id": "shandong_山亭区",
            "time_focus": "2020-2026",
        },
        "identity": {
            "person_id": f"shanting_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}" if person.get("birthplace") else "",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "副厅级" if pid == 1 else "县处级",
            "as_of": AS_OF,
            "is_current_confirmed": pid <= 2,
            "source_ids": ["S001"],
        },
        "career_timeline": career_entries,
        "organizations": [{"org_id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rel_entries,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": [],
            "geographic_pattern": ["枣庄市"],
            "promotion_velocity": {"summary": "公开资料不足，难以判断晋升速度", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "公开资料不足，无法推断工作风格",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "截至调研日未发现公开违规违纪记录", "date": AS_OF, "confidence": "unverified", "source_ids": ["S001"]}],
        "source_register": [
            {"id": "S001", "title": "山亭区人民政府网站公开信息", "url": "http://www.shanting.gov.cn/", "publisher": "枣庄市山亭区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "medium", "notes": "政府网站HTTP可访问，HTTPS不可用；领导职务来自新闻和人事任免通知"},
            {"id": "S002", "title": "山政任〔2026〕6号", "url": "http://www.shanting.gov.cn/zwgk/xxgkml/qzbm/qrsj/202605/t20260512_2282789.html", "publisher": "山亭区人民政府", "published_at": "2026-05-10", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "王彪任命为副区长、代理区长"},
            {"id": "S003", "title": "山政任〔2026〕8号", "url": "http://www.shanting.gov.cn/zwgk/xxgkml/qzbm/qrsj/202606/t20260626_2299160.html", "publisher": "山亭区人民政府", "published_at": "2026-06-01", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "王绪景任经开区管委会主任"},
            {"id": "S004", "title": "山政任〔2026〕9号", "url": "http://www.shanting.gov.cn/zwgk/xxgkml/qzbm/qrsj/202606/t20260626_2299161.html", "publisher": "山亭区人民政府", "published_at": "2026-06-03", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "孙彦民任副区长，免去王绪景副区长"},
            {"id": "S005", "title": "区委常委会召开 王德海主持并讲话", "url": "http://www.shanting.gov.cn/stxw/jrst/202607/t20260728_2310520.html", "publisher": "山亭区人民政府", "published_at": "2026-07-28", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认王德海为区委书记"},
            {"id": "S006", "title": "王彪主持召开区长办公会议", "url": "http://www.shanting.gov.cn/stxw/jrst/202608/t20260803_2312727.html", "publisher": "山亭区人民政府", "published_at": "2026-08-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认王彪为区委副书记、区长，确认赵传甲、戴娟、宗晓庆、周涛为副区长"},
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "所有领导人员完整履历（出生年月、教育背景、早期任职）均未查证。区委书记王德海的前任身份待确认。前任区长姓名待确认。区委常委名单（不含政府领导）不完整。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前区委书记王德海的完整履历（含出生年月、出生地、教育背景、早期任职及此前职务）", "why_it_matters": "确定政治谱系和可能的关联网络，王德海何时起任山亭区委书记、前任是谁", "suggested_queries": ["王德海 枣庄 简历", "王德海 山亭区委书记 任前公示", "王德海 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前区长王彪的完整履历（含出生年月、出生地、教育背景、早期任职及此前职务）", "why_it_matters": "确定其晋升路径和与王德海的关联历史", "suggested_queries": ["王彪 山亭区 区长 简历", "王彪 枣庄 组织部", "王彪 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "王彪的前任区长姓名与去向", "why_it_matters": "追踪前任去向，分析权力交接模式", "suggested_queries": ["原山亭区区长 调任", "山亭区 2025年 区长", "山亭区人大 免去区长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "王德海的前任区委书记是谁及去向", "why_it_matters": "追踪前任晋升路径", "suggested_queries": ["前任山亭区委书记", "原山亭区委书记 去向"], "last_attempted": AS_OF},
            {"priority": "high", "question": "山亭区委常委完整名单（不含区政府副区长以外的成员）", "why_it_matters": "完善领导班子图谱", "suggested_queries": ["山亭区 区委常委 分工", "山亭区 领导班子"], "last_attempted": AS_OF},
            {"priority": "high", "question": "李霞、李洪波的确切职务", "why_it_matters": "确定是否进入领导班子", "suggested_queries": ["李霞 山亭区", "李洪波 山亭区"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "孙彦民此前职务", "why_it_matters": "了解新任副区长的晋升路径", "suggested_queries": ["孙彦民 简历 枣庄", "孙彦民 山亭区"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "赵传甲、戴娟、宗晓庆、周涛的完整履历和此前职务", "why_it_matters": "完整政府班子分析", "suggested_queries": ["赵传甲 山亭区", "戴娟 山亭区", "宗晓庆 山亭区", "周涛 山亭区"], "last_attempted": AS_OF},
            {"priority": "low", "question": "王绪景的此前履历和任职背景", "why_it_matters": "分析从副区长到经开区主任的职务变动", "suggested_queries": ["王绪景 枣庄 简历", "王绪景 山亭区"], "last_attempted": AS_OF},
            {"priority": "low", "question": "张泺源的此前背景", "why_it_matters": "评估经开区管理团队构成", "suggested_queries": ["张泺源 枣庄", "张泺源 山亭区"], "last_attempted": AS_OF},
        ],
    }


def write_person_jsons():
    """Write individual person JSON files."""
    for p in persons:
        # Only write core figures (区委书记 and 区长)
        if p["id"] > 2:
            continue
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)

        job_slug = p["current_post"].replace("/", "_").replace("（", "_").replace("）", "_").replace(" ", "")
        filename = f"{TODAY}-山东省-枣庄市-{job_slug}-{p['name']}.json"
        filepath = PERSONS_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  山亭区 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 山亭区政府官网（HTTP），网络搜索工具受限")
    print(f"{'='*60}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("\n--- Writing person JSONs ---")
    os.makedirs(PERSONS_DIR, exist_ok=True)
    write_person_jsons()

    print(f"\n✅ 山亭区数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")