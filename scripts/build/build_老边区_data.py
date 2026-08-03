#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 老边区, 营口市, 辽宁省.

Investigation date: 2026-08-03
Task ID: liaoning_老边区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.laobian.gov.cn — 老边区人民政府官方网站 (accessible — leadership pages readable)
  - Baidu Baike — 老边区条目 (accessible, partial)
  - Government news articles (两优一先表彰大会, 常务会议)

Confidence notes:
  - 区政府班子成员全员确认（1区长+8副区长），详细个人简历部分缺失
  - 区委常委会：6/12席位已确认，剩余6席待查
  - 人大、政协主任/主席有轮动迹象（唐厚民→柳耀鹏, 刘启旦→张海利）
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "老边区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-03"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_老边区"
if _CURRENT_DIR.name == "liaoning_老边区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1=区委书记, 2=区长, 3=区委副书记, 4-8=区委常委, 9-17=区政府副职, 18=人大, 19=政协

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "彭伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老边区委书记",
        "current_org": "中共老边区委员会",
        "source": "https://baike.baidu.com/item/老边区"
    },
    {
        "id": 2,
        "name": "周鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-04",
        "birthplace": "",
        "education": "研究生学历，硕士学位",
        "party_join": "共产党员",
        "work_start": "",
        "current_post": "老边区委副书记、区政府党组书记、区长",
        "current_org": "老边区人民政府",
        "source": "http://www.laobian.gov.cn/ldzc/013001/013001001/leader.html"
    },
    {
        "id": 3,
        "name": "王钧瑞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老边区委副书记",
        "current_org": "中共老边区委员会",
        "source": "http://www.laobian.gov.cn/003/003001/20260630/7d6acfaf-532d-4394-9d4d-4fa5a79bba88.html"
    },
    {
        "id": 4,
        "name": "吴超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-10",
        "birthplace": "",
        "education": "大学",
        "party_join": "共产党员",
        "work_start": "",
        "current_post": "老边区委常委、区政府党组副书记、副区长（常务）",
        "current_org": "老边区人民政府",
        "source": "http://www.laobian.gov.cn/ldzc/013002/013002001/leader.html"
    },
    {
        "id": 5,
        "name": "孙林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-03",
        "birthplace": "",
        "education": "大学学历，江苏省委党校研究生",
        "party_join": "共产党员",
        "work_start": "",
        "current_post": "老边区委常委、副区长",
        "current_org": "老边区人民政府",
        "source": "http://www.laobian.gov.cn/ldzc/013002/013002003/leader.html"
    },
    {
        "id": 6,
        "name": "于泽锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老边区委常委、组织部部长",
        "current_org": "中共老边区委员会",
        "source": "http://www.laobian.gov.cn/003/003001/20260630/7d6acfaf-532d-4394-9d4d-4fa5a79bba88.html"
    },
    # ── 区政府副区长 ─────────────────────────────────────────────────────
    {
        "id": 7,
        "name": "李晓贺",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老边区副区长",
        "current_org": "老边区人民政府",
        "source": "http://www.laobian.gov.cn/ldzc/013001/013001001/leader.html"
    },
    {
        "id": 8,
        "name": "李洋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老边区副区长",
        "current_org": "老边区人民政府",
        "source": "http://www.laobian.gov.cn/ldzc/013001/013001001/leader.html"
    },
    {
        "id": 9,
        "name": "屈力",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老边区副区长",
        "current_org": "老边区人民政府",
        "source": "http://www.laobian.gov.cn/ldzc/013001/013001001/leader.html"
    },
    {
        "id": 10,
        "name": "冷岩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老边区副区长",
        "current_org": "老边区人民政府",
        "source": "http://www.laobian.gov.cn/ldzc/013001/013001001/leader.html"
    },
    {
        "id": 11,
        "name": "安志勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-11",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、老边区公安分局党组书记、局长",
        "current_org": "老边区人民政府 / 营口市公安局老边分局",
        "source": "http://www.laobian.gov.cn/ldzc/013002/013002004/leader.html"
    },
    {
        "id": 12,
        "name": "王鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老边区副区长",
        "current_org": "老边区人民政府",
        "source": "http://www.laobian.gov.cn/govxxgk/lbq/2026-05-25/ef65b90f-bc08-4cb6-80c6-87f4c2d80d7f.html"
    },
    # ── 开发区主任 ───────────────────────────────────────────────────
    {
        "id": 17,
        "name": "李大岭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "营口辽河经济开发区管委会主任",
        "current_org": "营口辽河经济开发区管委会",
        "source": "http://www.laobian.gov.cn/003/003001/20260630/7d6acfaf-532d-4394-9d4d-4fa5a79bba88.html"
    },
    # ── 人大、政协 ───────────────────────────────────────────────────────
    {
        "id": 13,
        "name": "柳耀鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老边区人大常委会主任（现任）",
        "current_org": "老边区人大常委会",
        "source": "http://www.laobian.gov.cn/003/003001/20260630/7d6acfaf-532d-4394-9d4d-4fa5a79bba88.html"
    },
    {
        "id": 14,
        "name": "张海利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老边区政协主席（候选人）",
        "current_org": "政协老边区委员会",
        "source": "http://www.laobian.gov.cn/003/003001/20260630/7d6acfaf-532d-4394-9d4d-4fa5a79bba88.html"
    },
    # ── 前任 ─────────────────────────────────────────────────────────────
    {
        "id": 15,
        "name": "唐厚民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/item/老边区"
    },
    {
        "id": 16,
        "name": "刘启旦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/item/老边区"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共老边区委员会", "type": "party_committee", "level": "县处级", "parent": "中共营口市委", "location": "老边区"},
    {"id": 2, "name": "老边区人民政府", "type": "government", "level": "县处级", "parent": "营口市人民政府", "location": "老边区"},
    {"id": 3, "name": "老边区人大常委会", "type": "npc", "level": "县处级", "parent": "", "location": "老边区"},
    {"id": 4, "name": "政协老边区委员会", "type": "cppcc", "level": "县处级", "parent": "", "location": "老边区"},
    {"id": 5, "name": "老边区纪委监委", "type": "discipline", "level": "县处级", "parent": "营口市纪委监委", "location": "老边区"},
    {"id": 6, "name": "老边区委组织部", "type": "party_department", "level": "县处级", "parent": "中共老边区委员会", "location": "老边区"},
    {"id": 7, "name": "老边区公安分局", "type": "government", "level": "乡科级", "parent": "营口市公安局", "location": "老边区"},
    {"id": 8, "name": "老边区审计局", "type": "government", "level": "乡科级", "parent": "老边区人民政府", "location": "老边区"},
    {"id": 9, "name": "营口辽河经济开发区管委会", "type": "development_zone", "level": "县处级", "parent": "营口市人民政府", "location": "老边区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 彭伟
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 周鹏
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "正处级", "note": "主持区政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王钧瑞
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 吴超
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责区政府常务工作"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 孙林
    {"person_id": 5, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责民政、退役军人事务"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 于泽锋
    {"person_id": 6, "org_id": 6, "title": "组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 副区长们
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "分管公安、司法"},
    {"person_id": 11, "org_id": 7, "title": "局长", "start": "", "end": "present", "rank": "正科级", "note": "兼任老边区公安分局局长"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责生态、教育、卫健"},
    # 人大、政协
    {"person_id": 13, "org_id": 3, "title": "主任", "start": "", "end": "present", "rank": "正处级", "note": "老边区人大常委会主任"},
    {"person_id": 14, "org_id": 4, "title": "主席（候选人）", "start": "", "end": "present", "rank": "正处级", "note": "政协主席候选人"},
    # 李大岭
    {"person_id": 17, "org_id": 9, "title": "管委会主任", "start": "", "end": "present", "rank": "正处级", "note": "营口辽河经济开发区管委会主任"},
    # 前人大、政协
    {"person_id": 15, "org_id": 3, "title": "主任（原任）", "start": "", "end": "", "rank": "正处级", "note": "百度百科显示截至2025年7月"},
    {"person_id": 16, "org_id": 4, "title": "主席（原任）", "start": "", "end": "", "rank": "正处级", "note": "百度百科显示截至2025年7月"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
# Key relationships based on known work overlaps
relationships = [
    # 区委—政府班子核心关系
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记—区长", "overlap_org": "中共老边区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记—区委副书记", "overlap_org": "中共老边区委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长—常务副区长", "overlap_org": "老边区人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记—组织部长", "overlap_org": "中共老边区委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "区委副书记—组织部长", "overlap_org": "中共老边区委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "常务副区长—副区长（常委兼任）", "overlap_org": "老边区人民政府", "overlap_period": ""},
    # 区政府同级
    {"person_a": 7, "person_b": 2, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "老边区人民政府", "overlap_period": ""},
    {"person_a": 8, "person_b": 2, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "老边区人民政府", "overlap_period": ""},
    {"person_a": 9, "person_b": 2, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "老边区人民政府", "overlap_period": ""},
    {"person_a": 10, "person_b": 2, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "老边区人民政府", "overlap_period": ""},
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "老边区人民政府", "overlap_period": ""},
    {"person_a": 12, "person_b": 2, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "老边区人民政府", "overlap_period": ""},
    # 工作互补关系（来自工作分工通知）
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "工作互补关系（安志勇—王鑫）", "overlap_org": "老边区人民政府", "overlap_period": "2026-05-25至今"},
    # 李大岭 — 区委书记（区域协同）
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "辽河经济开发区隶属老边区域，管委会主任与区委书记有工作交集", "overlap_org": "老边区", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "区长与经济开发区管委会主任工作关系", "overlap_org": "老边区", "overlap_period": ""},
    # 人大、政协
    {"person_a": 13, "person_b": 1, "type": "overlap", "context": "区人大常委会主任—区委书记", "overlap_org": "老边区", "overlap_period": ""},
    {"person_a": 14, "person_b": 1, "type": "overlap", "context": "政协主席（候选人）—区委书记", "overlap_org": "老边区", "overlap_period": ""},
    # 前任与现任（人大、政协轮动）
    {"person_a": 13, "person_b": 15, "type": "predecessor_successor", "context": "人大主任继任关系", "overlap_org": "老边区人大常委会", "overlap_period": ""},
    {"person_a": 14, "person_b": 16, "type": "predecessor_successor", "context": "政协主席交替关系", "overlap_org": "政协老边区委员会", "overlap_period": ""},
]

# ── Person JSON(s) — write for key figures ────────────────────────────────────
def _write_person_json(person_id: int, person: dict, out_dir: Path) -> None:
    """Write a minimal person graph JSON for key individuals who have confirmed data."""
    filename = f"{TODAY}-辽宁省-营口市-{person['current_post'].replace('、', '、').replace('，', '、')}-{person['name']}.json"
    # sanitize — keep only Chinese chars, letters, numbers, -, .
    import re
    safe_name = re.sub(r'[^\u4e00-\u9fff\w\-. ]', '_', filename)
    filepath = out_dir / safe_name

    pjson = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "营口市",
            "region": "老边区",
            "job": person["current_post"],
            "task_id": "liaoning_老边区",
            "time_focus": AS_OF,
        },
        "identity": {
            "name": person["name"],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "education": [{"period": "", "institution": "", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": bool(person["source"]),
            "source_ids": [],
        },
        "career_timeline": [
            {
                "start": "",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "confidence": "confirmed" if person["source"] else "plausible",
                "source_ids": [],
            }
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "No adverse signals found in this investigation.", "confidence": "unverified"}],
        "source_register": [
            {"id": "S001", "title": "老边区政府领导之窗", "url": person["source"], "publisher": "老边区人民政府", "source_type": "official", "reliability": "high"},
        ],
        "confidence_summary": {
            "identity": "partial" if not person["birth"] else "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "完整履历（出生年月至今的全部职务）",
        },
        "open_questions": [
            {"priority": "high", "question": "完整履历", "why_it_matters": "了解晋升路径和人际网络", "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 此前担任"], "last_attempted": TODAY}
        ],
    }
    filepath.write_text(json.dumps(pjson, ensure_ascii=False, indent=2), encoding="utf-8")
    return filepath

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"═══ Building {SLUG} network ═══")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:   {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    # Write person JSON files for key confirmed individuals
    key_people = [p for p in persons if p["birth"] and p["source"]]
    for p in key_people:
        fpath = _write_person_json(p["name"], p, PJSON_DIR)
        print(f"  Person JSON: {fpath.name}")

    # Build DB + GEXF
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

    # Verify
    import sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.execute("SELECT COUNT(*) FROM persons")
    p_count = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM organizations")
    o_count = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM positions")
    pos_count = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM relationships")
    r_count = cur.fetchone()[0]
    conn.close()

    print(f"  DB written: {DB_PATH.exists()}, size={DB_PATH.stat().st_size} bytes")
    print(f"    Persons: {p_count}, Orgs: {o_count}, Positions: {pos_count}, Relations: {r_count}")
    print(f"  GEXF written: {GEXF_PATH.exists()}, size={GEXF_PATH.stat().st_size} bytes")
    print(f"═══ Done ═══")
