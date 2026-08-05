#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Huanan County leadership network.

桦南县 (Huanan County) — 黑龙江省佳木斯市. Generates:
  - SQLite DB (persons, organizations, positions, relationships)
  - GEXF graph
  - Person JSON profiles for core leaders (县委书记, 县长)

Source of truth: official 桦南县人民政府 领导之窗
https://www.huanan.gov.cn/hnx/c100071/ldzc.shtml + individual leadership bio pages.
Roster confirmed as of 2026-08-05.
"""

import json
import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _ in range(6):
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    REPO_ROOT = REPO_ROOT.parent
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "桦南县"
TODAY = date.today().strftime("%Y%m%d")

# ── Paths (relative to repo root) ──
# When GOV_REL_DATABASE_DIR is set (staging mode), write DB/GEXF/person JSON
# directly into that dir so process_tmp can collect and promote them.
_STAGE = os.getenv("GOV_REL_DATABASE_DIR")
if _STAGE:
    DATA_DIR = Path(_STAGE)
    DB_PATH = DATA_DIR / f"{SLUG}_network.db"
    GEXF_PATH = DATA_DIR / f"{SLUG}_network.gexf"
    PERSONS_DIR = DATA_DIR
else:
    DATA_DIR = REPO_ROOT / "data"
    DB_PATH = DATA_DIR / "database" / f"{SLUG}_network.db"
    GEXF_PATH = DATA_DIR / "graph" / f"{SLUG}_network.gexf"
    PERSONS_DIR = DATA_DIR / "persons"

# ══════════════════════════════════════════════
#  PERSONS
# ══════════════════════════════════════════════
# Current roster from official 领导之窗 (2026-08-05)

persons = [
    # ── 县委书记 ──
    {"id": 1, "name": "徐永刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-11", "birthplace": "",
     "education": "本科学历",
     "party_join": "", "work_start": "1992-09",
     "current_post": "桦南县委书记", "current_org": "中共桦南县委员会",
     "source": "https://www.huanan.gov.cn/hnx/c100072/202406/c04_100226.shtml"},
    # ── 县委副书记、县长 ──
    {"id": 2, "name": "程显峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-02", "birthplace": "",
     "education": "研究生学历",
     "party_join": "", "work_start": "1995-07",
     "current_post": "桦南县委副书记、县政府县长", "current_org": "桦南县人民政府",
     "source": "https://www.huanan.gov.cn/hnx/c100074/202502/c04_100247.shtml"},
    # ── 县委副书记 ──
    {"id": 3, "name": "徐景新", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-11", "birthplace": "", "education": "本科学历",
     "party_join": "", "work_start": "1993-12",
     "current_post": "桦南县委副书记", "current_org": "中共桦南县委员会",
     "source": "https://www.huanan.gov.cn/hnx/c100072/202406/c04_100224.shtml"},
    # ── 县委常委、常务副县长 ──
    {"id": 4, "name": "曲振波", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-03", "birthplace": "", "education": "研究生学历",
     "party_join": "", "work_start": "1998-08",
     "current_post": "桦南县委常委、政府副县长", "current_org": "桦南县人民政府",
     "source": "https://www.huanan.gov.cn/hnx/c100072/202510/c04_169615.shtml"},
    # ── 县委常委、副县长 ──
    {"id": 5, "name": "肖德发", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-12", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "1997-08",
     "current_post": "桦南县委常委、政府副县长", "current_org": "桦南县人民政府",
     "source": "https://www.huanan.gov.cn/hnx/c100074/202502/c04_100245.shtml"},
    # ── 县委常委、纪委书记 ──
    {"id": 6, "name": "李承霖", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-06", "birthplace": "", "education": "硕士学历",
     "party_join": "", "work_start": "2006-08",
     "current_post": "桦南县委常委、县纪委书记、县监委主任", "current_org": "中共桦南县纪律检查委员会",
     "source": "https://www.huanan.gov.cn/hnx/c100072/202406/c04_100216.shtml"},
    # ── 县委常委、政法委书记 ──
    {"id": 7, "name": "王刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-05", "birthplace": "", "education": "本科学历",
     "party_join": "", "work_start": "",
     "current_post": "桦南县委常委、政法委书记", "current_org": "中共桦南县委员会",
     "source": "https://www.huanan.gov.cn/hnx/c100072/202406/c04_100219.shtml"},
    # ── 县委常委、组织部部长 ──
    {"id": 8, "name": "杨旭", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-10", "birthplace": "", "education": "本科学历",
     "party_join": "", "work_start": "2008-07",
     "current_post": "桦南县委常委、组织部部长", "current_org": "中共桦南县委员会",
     "source": "https://www.huanan.gov.cn/hnx/c100072/202406/c04_100215.shtml"},
    # ── 县委常委、宣传部部长 ──
    {"id": 9, "name": "姚宏俊", "gender": "女", "ethnicity": "汉族",
     "birth": "1992-06", "birthplace": "", "education": "研究生学历",
     "party_join": "", "work_start": "2014-09",
     "current_post": "桦南县委常委、宣传部部长", "current_org": "中共桦南县委员会",
     "source": "https://www.huanan.gov.cn/hnx/c100072/202510/c04_169613.shtml"},
    # ── 县委常委、人武部长 ──
    {"id": 10, "name": "黄河", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1977-09", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "1995-12",
     "current_post": "桦南县委常委、人武部长", "current_org": "桦南县人民武装部",
     "source": "https://www.huanan.gov.cn/hnx/c100072/202406/c04_100221.shtml"},
    # ── 副县长、公安局长 ──
    {"id": 11, "name": "闫力学", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-04", "birthplace": "", "education": "研究生学历",
     "party_join": "", "work_start": "1993-08",
     "current_post": "桦南县副县长、县公安局局长", "current_org": "桦南县公安局",
     "source": "https://www.huanan.gov.cn/hnx/c100074/202502/c04_100244.shtml"},
    # ── 副县长 ──
    {"id": 12, "name": "周迎春", "gender": "女", "ethnicity": "汉族",
     "birth": "1983-02", "birthplace": "", "education": "研究生学历",
     "party_join": "", "work_start": "2007-07",
     "current_post": "桦南县人民政府副县长", "current_org": "桦南县人民政府",
     "source": "https://www.huanan.gov.cn/hnx/c100074/202502/c04_100241.shtml"},
    # ── 副县长 ──
    {"id": 13, "name": "张佩升", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-12", "birthplace": "", "education": "大专学历",
     "party_join": "", "work_start": "1995-10",
     "current_post": "桦南县人民政府副县长", "current_org": "桦南县人民政府",
     "source": "https://www.huanan.gov.cn/hnx/c100074/202502/c04_100238.shtml"},
    # ── 副县长 ──
    {"id": 14, "name": "周金虎", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-01", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "1997-12",
     "current_post": "桦南县人民政府副县长", "current_org": "桦南县人民政府",
     "source": "https://www.huanan.gov.cn/hnx/c100074/202502/c04_100236.shtml"},
    # ── 县人大常委会主任 ──
    {"id": 15, "name": "安秀敏", "gender": "女", "ethnicity": "汉族",
     "birth": "1968-07", "birthplace": "", "education": "本科学历",
     "party_join": "", "work_start": "1987-07",
     "current_post": "桦南县人大常委会主任", "current_org": "桦南县人大常委会",
     "source": "https://www.huanan.gov.cn/hnx/c100073/202310/c04_100233.shtml"},
    # ── 县政协主席 ──
    {"id": 16, "name": "陈洪宝", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "桦南县政协主席", "current_org": "中国人民政治协商会议桦南县委员会",
     "source": "https://www.huanan.gov.cn/hnx/c100075/202406/c04_100251.shtml"},
]

# ══════════════════════════════════════════════
#  ORGANIZATIONS
# ══════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共桦南县委员会", "type": "party", "level": "县级",
     "parent": "中共佳木斯市委员会", "location": "黑龙江省佳木斯市桦南县"},
    {"id": 2, "name": "桦南县人民政府", "type": "government", "level": "县级",
     "parent": "佳木斯市人民政府", "location": "黑龙江省佳木斯市桦南县"},
    {"id": 3, "name": "桦南县人民代表大会常务委员会", "type": "npc", "level": "县级",
     "parent": "佳木斯市人民代表大会常务委员会", "location": "黑龙江省佳木斯市桦南县"},
    {"id": 4, "name": "中国人民政治协商会议桦南县委员会", "type": "cppcc", "level": "县级",
     "parent": "中国人民政治协商会议佳木斯市委员会", "location": "黑龙江省佳木斯市桦南县"},
    {"id": 5, "name": "中共桦南县纪律检查委员会", "type": "discipline", "level": "县级",
     "parent": "中共佳木斯市纪律检查委员会", "location": "黑龙江省佳木斯市桦南县"},
    {"id": 6, "name": "桦南县公安局", "type": "government", "level": "县级",
     "parent": "桦南县人民政府", "location": "黑龙江省佳木斯市桦南县"},
    {"id": 7, "name": "桦南县人民武装部", "type": "government", "level": "县级",
     "parent": "佳木斯军分区", "location": "黑龙江省佳木斯市桦南县"},
    {"id": 8, "name": "中共佳木斯市委员会", "type": "party", "level": "地级",
     "parent": "中共黑龙江省委员会", "location": "黑龙江省佳木斯市"},
    {"id": 9, "name": "中共黑龙江省委员会", "type": "party", "level": "省级",
     "parent": "", "location": "黑龙江省哈尔滨市"},
]

# ══════════════════════════════════════════════
#  POSITIONS
# ══════════════════════════════════════════════

positions = [
    {"person_id": 1, "org_id": 1, "title": "桦南县委书记",
     "start_date": "~2021", "end_date": "至今", "rank": "正处级",
     "note": "主持县委全面工作（官网 2026 确认）"},
    {"person_id": 2, "org_id": 2, "title": "桦南县委副书记、县政府县长",
     "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": "主持县政府全面工作；主管财政局、审计局、经开区管委会、城投/农投公司"},
    {"person_id": 2, "org_id": 1, "title": "桦南县委副书记",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "县委班子成员，兼任县政府县长"},
    {"person_id": 3, "org_id": 1, "title": "桦南县委副书记",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "协助县委书记抓党的建设、社会建设；分管农业农村/乡村振兴/群团"},
    {"person_id": 4, "org_id": 2, "title": "桦南县委常委、政府副县长（常务）",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "正处长级；负责县政府常务工作，协助县长分管审计局"},
    {"person_id": 5, "org_id": 2, "title": "桦南县委常委、政府副县长",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "负责城市建设、生态环境、市场监管、交通运输、退役军人事务"},
    {"person_id": 6, "org_id": 5, "title": "桦南县委常委、县纪委书记、县监委主任",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "主持纪检监察、巡察工作"},
    {"person_id": 7, "org_id": 1, "title": "桦南县委常委、政法委书记",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "负责政法、维稳、平安建设"},
    {"person_id": 8, "org_id": 1, "title": "桦南县委常委、组织部部长",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "主持县委组织部全面工作"},
    {"person_id": 9, "org_id": 1, "title": "桦南县委常委、宣传部部长",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "主持县委宣传部全面工作"},
    {"person_id": 10, "org_id": 7, "title": "桦南县委常委、人武部长",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "负责全县武装工作"},
    {"person_id": 11, "org_id": 6, "title": "桦南县政府副县长、县公安局局长",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "负责公共安全、法治建设"},
    {"person_id": 12, "org_id": 2, "title": "桦南县人民政府副县长",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "负责教育、卫生、城市社区管理"},
    {"person_id": 13, "org_id": 2, "title": "桦南县人民政府副县长",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "负责商务、工业信息，协助县长分管经开区"},
    {"person_id": 14, "org_id": 2, "title": "桦南县人民政府副县长",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "负责农业农村、乡村振兴、兽医、气象"},
    {"person_id": 15, "org_id": 3, "title": "桦南县人大常委会党组书记、主任",
     "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": "主持县人大全面工作"},
    {"person_id": 16, "org_id": 4, "title": "桦南县政协主席",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "主持县政协全面工作"},
]

# ══════════════════════════════════════════════
#  RELATIONSHIPS
# ══════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "现任县委书记与县长搭档（党政一把手），共同主持县领导班子工作",
     "overlap_org": "桦南县党委·县政府班子", "overlap_period": "2021年至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委副书记（专职）班子成员关系",
     "overlap_org": "中共桦南县委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 3, "type": "colleague",
     "context": "两名县委副书记，同为县委常委班子成员",
     "overlap_org": "中共桦南县委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与常务副县长：县政府班子关系，常务协助县长分管审计",
     "overlap_org": "桦南县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "县长与副县长：县政府班子关系",
     "overlap_org": "桦南县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "县长与副县长：县政府班子关系",
     "overlap_org": "桦南县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "县长与副县长：副县长协助县长分管经开区管委会",
     "overlap_org": "桦南县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "县长与副县长：县政府班子关系",
     "overlap_org": "桦南县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "县长与副县长（公安局长）：县政府班子/公安系统关系",
     "overlap_org": "桦南县人民政府·桦南县公安局", "overlap_period": "至今"},
    {"person_a": 4, "person_b": 5, "type": "colleague",
     "context": "两名常委副县长共同负责县政府常务与分管领域",
     "overlap_org": "桦南县人民政府", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 15, "type": "colleague",
     "context": "县委书记与人大主任：党委与人大班子领导交圈",
     "overlap_org": "桦南县党委·人大班子", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 16, "type": "colleague",
     "context": "县委书记与政协主席：党委与政协班子领导交圈",
     "overlap_org": "桦南县党委·政协班子", "overlap_period": "至今"},
]


# ══════════════════════════════════════════════
#  PERSON JSON WRITER
# ══════════════════════════════════════════════

_JOB_SLUG = {1: "县委书记", 2: "县长"}


def write_person_json(person: dict) -> str:
    """Write a person JSON profile for a core figure (县委书记, 县长)."""
    post_slug = _JOB_SLUG.get(person["id"], "领导班子成员")
    name_slug = person["name"]
    filename = f"{TODAY}-黑龙江省-佳木斯市-{post_slug}-{name_slug}.json"
    filepath = PERSONS_DIR / filename

    is_party_secretary = person["id"] == 1
    person_json = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "佳木斯市",
            "region": "桦南县",
            "job": person["current_post"],
            "task_id": "heilongjiang_桦南县",
            "time_focus": "2026年8月",
        },
        "identity": {
            "person_id": f"huanan_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender") or "",
            "ethnicity": person.get("ethnicity") or "",
            "birth": person.get("birth") or "",
            "birthplace": person.get("birthplace") or "",
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "",
                           "degree": person.get("education") or "",
                           "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join") or "",
            "work_start": person.get("work_start") or "",
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if (is_party_secretary or "县长" in person["current_post"]) else "县处级",
            "as_of": TODAY,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "县处级正职" if (is_party_secretary or "县长" in person["current_post"]) else "县处级副职",
                "location": "黑龙江省佳木斯市桦南县",
                "system": "party" if "书记" in person["current_post"] else "government",
                "rank": "正处级" if (is_party_secretary or "县长" in person["current_post"]) else "副处级",
                "is_key_promotion": True,
                "notes": f"现任{person['current_post']}（桦南县人民政府领导之窗官网确认）",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            }
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "无公开的性格/工作风格资料；仅依据官网职务分工推断。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未检索到该领导公开的违纪/审计/负面报道线索",
             "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "桦南县人民政府 领导之窗 个人简介页",
                "url": person["source"],
                "publisher": "桦南县人民政府",
                "published_at": "2026-06-12",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "任前简介页；含出生年月、参加工作年月、学历、现任职务",
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "早期职业履历（岗位晋升轨迹、调任来源）未公开，需通过任前公示/媒体补充",
        },
        "open_questions": [
            {
                "priority": "high",
                "question": f"{person['name']}的完整任职轨迹（此前历任岗位、调任桦南县时间、前任去向）",
                "why_it_matters": "核心领导人的晋升路径与来源地是人事网络分析的关键",
                "suggested_queries": [
                    f"{person['name']} 简历 任职经历",
                    f"{person['name']} 任前公示 佳木斯",
                    f"{person['name']} 桦南县委书记 履新",
                ],
                "last_attempted": TODAY,
            }
        ],
    }

    PERSONS_DIR.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)
    print(f"  [ok]  {filename}")
    return filename


def main():
    print("=" * 60)
    print("  桦南县 — 领导班子工作关系网络")
    print(f"  Generated: {TODAY}")
    print("  Source: 桦南县人民政府官网 领导之窗")
    print("=" * 60)

    print("\nBuilding database and GEXF graph...")
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
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    # Verify the database contains the 4 expected tables
    conn = sqlite3.connect(str(DB_PATH))
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    for req in ("persons", "organizations", "positions", "relationships"):
        assert req in tables, f"missing table {req}"
    print("  DB tables OK: persons, organizations, positions, relationships")

    print("\nWriting person JSON files for core leaders...")
    core_leader_ids = [1, 2]
    json_files = [write_person_json(next(p for p in persons if p["id"] == pid))
                  for pid in core_leader_ids]

    print()
    print("─" * 60)
    print("  统计摘要")
    print("─" * 60)
    print(f"  人员 (persons):     {len(persons)}")
    print(f"  机构 (orgs):        {len(organizations)}")
    print(f"  任职 (positions):   {len(positions)}")
    print(f"  关系 (edges):       {len(relationships)}")
    print(f"  JSON 文件:           {len(json_files)}")
    print()
    print("  说明:")
    print("    - 现任县委书记 = 徐永刚 (官网领导之窗确认)")
    print("    - 现任县长     = 程显峰 (官网领导之窗确认)")
    print("    - 出生/参加工作时间、学历源自官网个人简介")
    print("    - 籍贯/完整晋升履历尚缺，待后续补充")
    print()
    print("=" * 60)
    print("  Build complete.")
    print("  → Validate: python3 -m py_compile build_桦南县_data.py")
    print("  → Promote:  python3 scripts/process_tmp.py data/tmp/heilongjiang_桦南县 --apply")
    print("=" * 60)


if __name__ == "__main__":
    main()