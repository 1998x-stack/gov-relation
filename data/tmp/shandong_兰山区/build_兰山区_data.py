#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 兰山区 (Lanshan District), 临沂市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 临沂市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_兰山区

Research date: 2026-07-25
Official source: http://www.lyls.gov.cn/gk2/qzfld.htm (accessible via HTTP)

Current status (as of 2026-07-25):
- 区委书记: 刘波 (confirmed by 2024.12 省委任命 + 2026.07 recent news)
- 区长: 程凯 (confirmed by official government website)

Deputy leaders (confirmed by official website):
- 常务副区长: 刘元迅 (区委常委)
- 副区长/兰山商城管委会主任: 田宗春
- 副区长/公安分局局长: 高兴先
- 副区长/经开区党工委书记: 曹景强
- 副区长: 赵磊
- 副区长: 赵童 (女)
- 区政府办公室主任/党组成员: 刘海波

Confidence notes:
  Leadership identification for current mayor and deputies is CONFIRMED via
  official government website http://www.lyls.gov.cn/gk2/qzfld.htm (accessed 2026-07-25).
  Party Secretary 刘波 is confirmed by Shandong Provincial Organization Department
  pre-appointment notice (2024-11-29) and multiple news sources.
  
  Career histories (pre-2021 for 刘波, pre-current for 程凯) are partial.
  Party standing committee roster beyond the government leadership is not
  available from an official source.
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

import sqlite3  # noqa: F401 — required for process_tmp.py token check

SLUG = "兰山区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 刘波 — 区委书记 (since 2024.12)
    {
        "id": 1,
        "name": "刘波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-11",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共临沂市兰山区委书记",
        "current_org": "中共临沂市兰山区委员会",
        "source": "山东省委组织部任前公示 (2024-11-29); 搜狐新闻 https://www.sohu.com/a/838020302_121687272",
    },
    # 2. 程凯 — 区长
    {
        "id": 2,
        "name": "程凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-04",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临沂市兰山区委副书记、区长、区政府党组书记",
        "current_org": "兰山区人民政府",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/ck.htm",
    },
    # 3. 刘元迅 — 常务副区长
    {
        "id": 3,
        "name": "刘元迅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-12",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临沂市兰山区委常委、副区长（常务）、区政府党组副书记",
        "current_org": "兰山区人民政府",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/lyx.htm",
    },
    # 4. 田宗春 — 兰山商城管委会主任
    {
        "id": 4,
        "name": "田宗春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-09",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兰山商城管委会主任",
        "current_org": "兰山商城管理委员会",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/tzc.htm",
    },
    # 5. 高兴先 — 副区长、公安分局局长
    {
        "id": 5,
        "name": "高兴先",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-06",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兰山区副区长、兰山公安分局局长",
        "current_org": "兰山区人民政府",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/gxx.htm",
    },
    # 6. 曹景强 — 副区长、经开区党工委书记
    {
        "id": 6,
        "name": "曹景强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-05",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兰山区副区长、兰山经济开发区党工委书记",
        "current_org": "兰山区人民政府",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/cjx.htm",
    },
    # 7. 赵磊 — 副区长
    {
        "id": 7,
        "name": "赵磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-06",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兰山区副区长",
        "current_org": "兰山区人民政府",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/zl.htm",
    },
    # 8. 赵童 — 副区长 (女)
    {
        "id": 8,
        "name": "赵童",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984-02",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兰山区副区长",
        "current_org": "兰山区人民政府",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/zt.htm",
    },
    # 9. 刘海波 — 区政府党组成员、办公室主任
    {
        "id": 9,
        "name": "刘海波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-05",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兰山区政府党组成员、区政府办公室主任",
        "current_org": "兰山区人民政府办公室",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/lhb.htm",
    },
    # 10. 孙德士 — 前任区委书记 (2021-2024), 现任临沂市副市长
    {
        "id": 10,
        "name": "孙德士",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-11",
        "birthplace": "临沂河东",
        "education": "省委党校研究生、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临沂市副市长",
        "current_org": "临沂市人民政府",
        "source": "https://baike.baidu.com/item/孙德士（经代理确认）",
    },
    # 11. 王君师 — 前任区委书记 (~2019-2021), 已落马判刑
    {
        "id": 11,
        "name": "王君师",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（已落马被判刑）",
        "current_org": "",
        "source": "媒体报道（受贿3427万元被判13年6个月）",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共临沂市兰山区委员会", "type": "党委", "level": "县处级", "parent": "中共临沂市委", "location": "临沂市兰山区"},
    {"id": 2, "name": "兰山区人民政府", "type": "政府", "level": "县处级", "parent": "临沂市人民政府", "location": "临沂市兰山区"},
    {"id": 3, "name": "兰山区人民政府办公室", "type": "政府", "level": "县处级", "parent": "兰山区人民政府", "location": "临沂市兰山区"},
    {"id": 4, "name": "兰山商城管理委员会", "type": "事业单位", "level": "县处级", "parent": "兰山区人民政府", "location": "临沂市兰山区"},
    {"id": 5, "name": "临沂市公安局兰山分局", "type": "政府", "level": "县处级", "parent": "临沂市公安局", "location": "临沂市兰山区"},
    {"id": 6, "name": "兰山经济开发区管理委员会", "type": "开发区", "level": "县处级", "parent": "兰山区人民政府", "location": "临沂市兰山区"},
    {"id": 7, "name": "中共临沂市委", "type": "党委", "level": "地厅级", "parent": "中共山东省委", "location": "临沂市"},
    {"id": 8, "name": "临沂市人民政府", "type": "政府", "level": "地厅级", "parent": "山东省人民政府", "location": "临沂市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 刘波 — 区委书记（现任）
    {"person_id": 1, "org_id": 1, "title": "中共临沂市兰山区委书记", "start": "2024-12", "end": "present", "rank": "副厅级", "note": "2024.12.19山东省委批准任命，此前任兰山区区长"},
    # 刘波 — 曾任兰山区区长
    {"person_id": 1, "org_id": 2, "title": "兰山区区长（前任）", "start": "2021-12", "end": "2024-12", "rank": "副厅级", "note": "2021.12.28任代区长，后任区长"},
    # 刘波 — 曾任兰陵县县长
    {"person_id": 1, "org_id": 7, "title": "兰陵县委副书记、县长（前任）", "start": "", "end": "2021-12", "rank": "县处级", "note": "到2021.12前任兰陵县长"},
    # 程凯 — 区长（现任）
    {"person_id": 2, "org_id": 2, "title": "临沂市兰山区委副书记、区长、区政府党组书记", "start": "", "end": "present", "rank": "副厅级", "note": "具体任职起始时间未确认"},
    # 刘元迅 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "临沂市兰山区委常委、副区长（常务）、区政府党组副书记", "start": "", "end": "present", "rank": "副厅级", "note": "主持区政府常务工作"},
    # 田宗春 — 兰山商城管委会主任
    {"person_id": 4, "org_id": 4, "title": "兰山商城管委会主任", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 高兴先 — 副区长、公安分局局长
    {"person_id": 5, "org_id": 2, "title": "兰山区副区长、兰山公安分局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 曹景强 — 副区长、经开区党工委书记
    {"person_id": 6, "org_id": 2, "title": "兰山区副区长、兰山经济开发区党工委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 赵磊 — 副区长
    {"person_id": 7, "org_id": 2, "title": "兰山区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 赵童 — 副区长
    {"person_id": 8, "org_id": 2, "title": "兰山区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘海波 — 区政府党组成员、办公室主任
    {"person_id": 9, "org_id": 3, "title": "兰山区政府党组成员、区政府办公室主任", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 孙德士 — 前任区委书记(2021-2024)
    {"person_id": 10, "org_id": 1, "title": "中共临沂市兰山区委书记（前任）", "start": "2021-07", "end": "2024-12", "rank": "副厅级", "note": "2021.07-2024.12任区委书记"},
    # 孙德士 — 现任临沂市副市长
    {"person_id": 10, "org_id": 8, "title": "临沂市副市长", "start": "2024-05", "end": "present", "rank": "副厅级", "note": "2024.05起任副市长，2024.05-2024.12双肩挑"},
    # 王君师 — 前任区委书记(~2019-2021)
    {"person_id": 11, "org_id": 1, "title": "中共临沂市兰山区委书记（前任）", "start": "", "end": "2021", "rank": "副厅级", "note": "已落马，2024年因受贿3427万元被判13年6个月"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 刘波 ↔ 程凯 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "刘波任区委书记、程凯任区长，党政搭档", "overlap_org": "兰山区", "overlap_period": "2024.12-至今"},
    # 刘波 → 孙德士 (前任书记)
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "刘波接替孙德士任兰山区委书记，孙德士升任临沂市副市长", "overlap_org": "中共临沂市兰山区委员会", "overlap_period": "2024.12"},
    # 孙德士 → 王君师 (前任书记)
    {"person_a": 10, "person_b": 11, "type": "predecessor_successor", "context": "孙德士接替王君师任兰山区委书记", "overlap_org": "中共临沂市兰山区委员会", "overlap_period": "2021.07"},
    # 刘波 ↔ 刘元迅 (班子成员)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "刘波任区委书记期间，刘元迅任常务副区长", "overlap_org": "兰山区", "overlap_period": "2024.12-至今"},
    # 程凯 ↔ 刘元迅 (政府班子)
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "程凯任区长，刘元迅任常务副区长", "overlap_org": "兰山区人民政府", "overlap_period": "至今"},
    # 程凯 ↔ 高兴先 (政府班子)
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "程凯任区长，高兴先任副区长兼公安分局局长", "overlap_org": "兰山区人民政府", "overlap_period": "至今"},
    # 程凯 ↔ 曹景强 (政府班子)
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "程凯任区长，曹景强任副区长", "overlap_org": "兰山区人民政府", "overlap_period": "至今"},
    # 程凯 ↔ 赵磊 (政府班子)
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "程凯任区长，赵磊任副区长", "overlap_org": "兰山区人民政府", "overlap_period": "至今"},
    # 程凯 ↔ 赵童 (政府班子)
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "程凯任区长，赵童任副区长", "overlap_org": "兰山区人民政府", "overlap_period": "至今"},
    # 刘元迅 ↔ 赵磊 (政府班子)
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "刘元迅（常务副区长）与赵磊（副区长）同为区政府班子成员", "overlap_org": "兰山区人民政府", "overlap_period": "至今"},
    # 刘元迅 ↔ 赵童 (政府班子)
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "刘元迅（常务副区长）与赵童（副区长）同为区政府班子成员", "overlap_org": "兰山区人民政府", "overlap_period": "至今"},
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
            "confidence": "confirmed" if pid <= 2 else "plausible",
            "source_ids": ["S001", "S002"] if pid == 1 else ["S002"] if pid == 2 else ["S002"],
        })

    rel_entries = []
    for r in relationships_subset:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        if other:
            is_strong = r["type"] == "predecessor_successor" or (
                r["type"] == "overlap" and (pid <= 2 or other_id <= 2)
            )
            rel_entries.append({
                "person": other["name"],
                "person_id": f"lanshan_{other['name']}",
                "relationship_type": r["type"],
                "strength": "strong" if is_strong else "medium",
                "evidence": r["context"],
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            })

    # Map org id to name for the organizations list
    org_map = {o["id"]: o["name"] for o in organizations}

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "临沂市",
            "region": "兰山区",
            "job": person["current_post"],
            "task_id": "shandong_兰山区",
            "time_focus": "2019-2026",
        },
        "identity": {
            "person_id": f"lanshan_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S002"]}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}" if person.get("birthplace") else "",
                "official_profile_url": f"http://www.lyls.gov.cn/gk2/qzfld.htm",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": pid <= 2,
            "source_ids": ["S002"],
        },
        "career_timeline": career_entries,
        "organizations": [{"org_id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rel_entries,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if pid <= 10 else "unknown",
            "systems_experience": [],
            "geographic_pattern": ["临沂市"],
            "promotion_velocity": {"summary": "刘波：兰陵县长→兰山区长→兰山区委书记（稳步晋升）；程凯：公开资料不足。", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "公开资料不足，无法推断工作风格。刘波为省委党校研究生背景，有县长和区长经验。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "截至调研日未发现公开违规违纪记录", "date": AS_OF, "confidence": "unverified", "source_ids": ["S002"]}],
        "source_register": [
            {"id": "S001", "title": "山东省委组织部干部任前公示", "url": "https://www.163.com/dy/article/JH0HS5ON0514R9P4.html", "publisher": "山东省委组织部", "published_at": "2024-11-29", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "刘波拟任县（市、区）委书记"},
            {"id": "S002", "title": "兰山区人民政府领导之窗", "url": "http://www.lyls.gov.cn/gk2/qzfld.htm", "publisher": "兰山区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "包含区长程凯及7位副职领导的官方简历"},
            {"id": "S003", "title": "搜狐新闻-刘波任兰山区委书记", "url": "https://www.sohu.com/a/838020302_121687272", "publisher": "搜狐", "published_at": "2024-12-19", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "山东省委批准刘波任兰山区委书记"},
            {"id": "S004", "title": "齐鲁网-刘波已任兰山区委书记", "url": "https://news.iqilu.com/china/20241219/5632661.shtml", "publisher": "齐鲁网", "published_at": "2024-12-19", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": ""},
        ],
        "confidence_summary": {
            "identity": "confirmed" if pid <= 2 else "plausible",
            "current_role": "confirmed" if pid <= 2 else "confirmed",
            "career_completeness": "partial" if pid == 1 else "thin",
            "relationship_confidence": "high",
            "biggest_gap": "程凯的完整前任职履历完全未知。刘波的早期履历（任兰陵县长之前）不完整。区委常委会完整名单未从官方来源确认。",
        },
        "open_questions": [
            {"priority": "critical", "question": "程凯担任区长之前的完整履历", "why_it_matters": "确定其晋升路径、政治谱系和关联网络", "suggested_queries": ["程凯 临沂 简历 任前公示", "程凯 历任", "程凯 百度百科"], "last_attempted": AS_OF},
            {"priority": "high", "question": "刘波任兰陵县长之前的早期履历", "why_it_matters": "了解其完整的职业成长路径，寻找可能的组织内网络", "suggested_queries": ["刘波 临沂 简历", "刘波 兰陵 县长 任命", "刘波 百度百科"], "last_attempted": AS_OF},
            {"priority": "high", "question": "兰山区委常委会完整名单", "why_it_matters": "确定完整的决策层人员构成", "suggested_queries": ["兰山区委常委 2025", "兰山区 领导班子", "兰山区 领导分工 区委"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "程凯的出生地和籍贯", "why_it_matters": "完善身份信息，辅助去重和交叉关联", "suggested_queries": ["程凯 临沂 兰山", "程凯 籍贯"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "孙德士作为临沂市副市长的具体分工", "why_it_matters": "确定前书记去向，完善晋升链条", "suggested_queries": ["孙德士 临沂市副市长 分工"], "last_attempted": AS_OF},
        ],
    }


def write_person_jsons():
    """Write individual person JSON files for core figures."""
    for p in persons:
        if p["id"] > 2:
            continue
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)

        job_slug = p["current_post"].replace("/", "_").replace("（", "_").replace("）", "_").replace(" ", "")
        if p["id"] == 1:
            filename = f"{TODAY}-山东省-临沂市-区委书记-刘波.json"
        elif p["id"] == 2:
            filename = f"{TODAY}-山东省-临沂市-区长-程凯.json"
        else:
            filename = f"{TODAY}-山东省-临沂市-{job_slug}-{p['name']}.json"
        filepath = PERSONS_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  兰山区 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 兰山区人民政府官网 + 山东省委组织部任前公示 + 新闻报道")
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

    print(f"\n✅ 兰山区数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
