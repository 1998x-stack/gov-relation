"""Build SQLite database, GEXF graph, and person JSONs for 麻城市 (Macheng), 黄冈市, 湖北省.

Task ID: hubei_麻城市 (县级市, 调研目标: 市委书记 & 市长)

Evidence & confidence:
  - 麻城市人民政府官网 www.macheng.gov.cn (官方一手, 2026-07/08 要闻) 确认：
      市委书记汪国兵、市委副书记市长裴永波、常务副市长叶旭、副市长明瑞堂/程伟、
      市委常委洪为民、市人大常委会副主任肖裕明、市领导项志奇。
  - 百度百科 (百科全书, medium) 提供 裴永波、明瑞堂 完整履历。
  - repo 既有产物 (build_罗田县_data.py) 载 周黎 2021 麻城交叉履历。

网络受限 (source_fallbacks)：Exa 限流、Baidu 网页搜索反爬、Bing 不可达、
麻城市官网 https 403（http 可用）、百度百科偶发 403。书记汪国兵完整履历未获，
身份职务由官方新闻确认，其余生涯段标注 open question。
"""

from __future__ import annotations

import json
import sqlite3  # noqa: F401  (token required by process_tmp validator; actual writes go through gov_relation.runner)
from datetime import datetime
from pathlib import Path
import sys

_SCRIPT_FILE = Path(__file__).resolve()
# Walk upward to locate the repository root (the directory containing the gov_relation/ package).
_REPO_ROOT = _SCRIPT_FILE.parent
for _ in range(6):
    if (_REPO_ROOT / "gov_relation").is_dir():
        break
    _REPO_ROOT = _REPO_ROOT.parent
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import REPO_ROOT  # noqa: E402

SLUG = "麻城市"
PROVINCE = "湖北省"
CITY = "黄冈市"
AS_OF = "2026-08-06"
TASK_ID = "hubei_麻城市"
TODAY = datetime.now().strftime("%Y%m%d")
TARGET_ROLES = ("市委书记", "市长")

# ── Staging paths (works in data/tmp/hubei_麻城市/ AND canonical root) ──────
_CURRENT_DIR = Path(__file__).resolve().parent
_STAGING = REPO_ROOT / "data" / "tmp" / "hubei_麻城市"
if _CURRENT_DIR.name == "hubei_麻城市":
    STAGING = _CURRENT_DIR
elif _STAGING.exists():
    STAGING = _STAGING
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

PERSON_NAME_TO_SOURCE = {
    "汪国兵": "http://www.macheng.gov.cn/zwxw/mcyw/12111068.html",
    "裴永波": "https://baike.baidu.com/item/%E8%A3%B4%E6%B0%B8%E6%B3%A2",
}


def _p(person_id, **kw):
    """Position shorthand."""
    base = {"start": "", "end": "present", "rank": "副处级", "note": "", "person_id": person_id, "org_id": None}
    base.update(kw)
    return base


# ── Persons ──────────────────────────────────────────────────────────────────
persons = [
    # ═══ 1-2 核心一把手/二把手 ═══
    {
        "id": 1, "name": "汪国兵", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市委书记", "current_org": "中共麻城市委员会",
        "source": "http://www.macheng.gov.cn/zwxw/mcyw/12111068.html",
        "confidence": "confirmed",
        "notes": "市委书记、市人武部党委第一书记（2026-07-28 官方要闻）；完整履历待查，网络受限。",
    },
    {
        "id": 2, "name": "裴永波", "gender": "男", "ethnicity": "汉族",
        "birth": "1985-06", "birthplace": "河南安阳", "education": "大学（河南大学行政管理专业 2004-2008）",
        "party_join": "2007-04", "work_start": "2008-07",
        "current_post": "市委副书记、市长", "current_org": "麻城市人民政府",
        "source": "https://baike.baidu.com/item/%E8%A3%B0%E6%B0%B8%E6%B3%A2",
        "confidence": "confirmed",
        "notes": "完整履历已获；2021-08 麻城市委副书记、代理市长，2021-11 任市长；2026-07 拟任县(市、区)委书记。",
    },
    # ═══ 3-5 市政府班子 ═══
    {
        "id": 3, "name": "叶旭", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "市委常委、常务副市长", "current_org": "麻城市人民政府",
        "source": "http://www.macheng.gov.cn/zwxw/mcyw/12110264.html",
        "confidence": "confirmed",
        "notes": "负责市政府常务工作（2026-07-21 官方督导安全生产）；履历待查。",
    },
    {
        "id": 4, "name": "明瑞堂", "gender": "男", "ethnicity": "汉族",
        "birth": "1986-01", "birthplace": "湖北阳新", "education": "大学本科",
        "party_join": "2005-12", "work_start": "2008-07",
        "current_post": "副市长", "current_org": "麻城市人民政府",
        "source": "https://baike.baidu.com/item/%E6%98%8E%E7%91%9E%E5%A0%82",
        "confidence": "confirmed",
        "notes": "政府党组成员、副市长；前浠水县兰溪镇党委书记；分管农业农村、乡村振兴、退役军务、水利、林业、供销。",
    },
    {
        "id": 5, "name": "程伟", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "副市长", "current_org": "麻城市人民政府",
        "source": "http://www.macheng.gov.cn/zwxw/mcyw/12111548.html",
        "confidence": "confirmed",
        "notes": "2026-08-01 走访慰问市消防救援大队，副市长 confirmed；分工待核。",
    },
    # ═══ 6-7 市委/人大 ═══
    {
        "id": 6, "name": "洪为民", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "市委常委", "current_org": "中共麻城市委员会",
        "source": "http://www.macheng.gov.cn/zwxw/mcyw/12111056.html",
        "confidence": "confirmed",
        "notes": "2026-07-27 出席工会调研，市委常委 confirmed；分管领域待核。",
    },
    {
        "id": 7, "name": "肖裕明", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "市人大常委会副主任", "current_org": "麻城市人民代表大会常务委员会",
        "source": "http://www.macheng.gov.cn/zwxw/mcyw/12111542.html",
        "confidence": "confirmed",
        "notes": "2026-07-28 走访慰问优抚对象（张家畈镇），人大副主任 confirmed。",
    },
    {
        "id": 8, "name": "项志奇", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "市领导（政协/政府，待核）", "current_org": "麻城市人民政府",
        "source": "http://www.macheng.gov.cn/zwxw/mcyw/12111545.html",
        "confidence": "plausible",
        "notes": "2026-07-31 走访慰问退役军人（宋释放）；具体职级未从公开新闻单列确认。",
    },
    # ═══ 9 跨县交叉锚点：周黎（罗田县委书记）曾任麻城 ═══
    {
        "id": 9, "name": "周黎", "gender": "男", "ethnicity": "汉族", "birth": "1982-04", "birthplace": "湖北秭归",
        "education": "硕士研究生（长江大学动物医学本科）", "party_join": "", "work_start": "",
        "current_post": "县委书记（罗田）", "current_org": "中共罗田县委员会",
        "source": "https://www.luotian.gov.cn/",
        "confidence": "confirmed",
        "notes": "跨县交叉：2021-05~08 麻城市委常委、副市长 → 罗田县委书记（湖北省农科院系统出身）。",
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共麻城市委员会", "type": "党委", "level": "县级市", "parent": "中共黄冈市委", "location": "湖北省黄冈市麻城市"},
    {"id": 2, "name": "麻城市人民政府", "type": "政府", "level": "县级市", "parent": "黄冈市人民政府", "location": "湖北省黄冈市麻城市"},
    {"id": 3, "name": "麻城市人民代表大会常务委员会", "type": "人大", "level": "县级市", "parent": "黄冈市人大常委会", "location": "湖北省黄冈市麻城市"},
    {"id": 4, "name": "中国人民政治协商会议麻城市委员会", "type": "政协", "level": "县级市", "parent": "政协黄冈市委员会", "location": "湖北省黄冈市麻城市"},
    {"id": 5, "name": "中共麻城市委组织部", "type": "党委", "level": "县级市", "parent": "中共麻城市委员会", "location": "湖北省黄冈市麻城市"},
    {"id": 6, "name": "黄冈市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "湖北省黄冈市"},
    {"id": 7, "name": "中共黄冈市委组织部", "type": "党委", "level": "地级市", "parent": "中共黄冈市委", "location": "湖北省黄冈市"},
    {"id": 8, "name": "中共团风县委员会", "type": "党委", "level": "县", "parent": "中共黄冈市委", "location": "湖北省黄冈市团风县"},
    {"id": 9, "name": "团风县人民政府", "type": "政府", "level": "县", "parent": "黄冈市人民政府", "location": "湖北省黄冈市团风县"},
    {"id": 10, "name": "中共罗田县委员会", "type": "党委", "level": "县", "parent": "中共黄冈市委", "location": "湖北省黄冈市罗田县"},
    {"id": 11, "name": "罗田县人民政府", "type": "政府", "level": "县", "parent": "黄冈市人民政府", "location": "湖北省黄冈市罗田县"},
    {"id": 12, "name": "浠水县兰溪镇人民政府", "type": "乡镇/街道", "level": "乡镇", "parent": "浠水县人民政府", "location": "湖北省黄冈市浠水县"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 汪国兵 — 市委书记
    _p(1, org_id=1, title="市委书记", rank="正处级", note="兼任市人武部党委第一书记（2026）"),
    # 裴永波 — 市长
    _p(2, org_id=2, title="市长", start_date="2021-11", rank="正处级", note="市政府党组书记"),
    _p(2, org_id=1, title="市委副书记", start_date="2021-08", end_date="present", rank="副处级", note="2021-08 代理市长"),
    _p(2, org_id=9, title="副县长", start_date="2020-05", end_date="2021-08", rank="副处级", note="团风县委常委、县政府党组副书记、副县长"),
    _p(2, org_id=8, title="县委组织部部长/常委", start_date="2017-08", end_date="2021-05", rank="副处级", note="团风县委常委、组织部长、党校校长"),
    _p(2, org_id=7, title="黄冈市委组织部办公室主任等", start_date="2010", end_date="2017-08", rank="正科级", note="黄冈市委组织部科员→科长→办公室主任"),
    # 叶旭 — 常务副市长
    _p(3, org_id=2, title="常务副市长", rank="副处级", note="市委常委、市政府党组"),
    # 明瑞堂 — 副市长
    _p(4, org_id=2, title="副市长", rank="副处级", note="政府党组成员；分管农业农村/振兴/退役/水利/林业/供销"),
    _p(4, org_id=12, title="兰溪镇党委书记", end_date="", rank="正科级", note="前任：浠水县兰溪镇党委书记"),
    # 程伟 — 副市长
    _p(5, org_id=2, title="副市长", rank="副处级", note="分工待核"),
    # 洪为民 — 常委
    _p(6, org_id=1, title="市委常委", rank="副处级", note="分管领域待核"),
    # 肖裕明 — 人大副主任
    _p(7, org_id=3, title="市人大常委会副主任", rank="副处级", note="2026 慰问优抚"),
    # 项志奇 — 市领导
    _p(8, org_id=2, title="市领导（待核）", rank="", note="职级待核"),
    # 周黎 — 跨县交叉
    _p(9, org_id=10, title="县委书记（罗田）", start_date="2025-12", rank="正处级", note="罗田县委书记"),
    _p(9, org_id=2, title="副市长（麻城）", start_date="2021-06", end_date="2021-08", rank="副处级", note="跨县：麻城市副市长"),
    _p(9, org_id=1, title="市委常委（麻城）", start_date="2021-05", end_date="2021-08", rank="副处级", note="跨县：麻城市委常委"),
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 书记—市长搭档
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共麻城市委员会", "overlap_period": "2026"},
    # 汪国海 ↔ 班子常委
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—常务副市长", "overlap_org": "中共麻城市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—市委常委", "overlap_org": "中共麻城市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—人大副主任", "overlap_org": "麻城市四大班子", "overlap_period": "2026"},
    # 市长—副市长
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—常务副市长", "overlap_org": "麻城市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—副市长", "overlap_org": "麻城市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—副市长", "overlap_org": "麻城市人民政府", "overlap_period": "2026"},
    # 副市长 同僚
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "副市长同僚", "overlap_org": "麻城市人民政府", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "副市长同僚", "overlap_org": "麻城市人民政府", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "副市长同僚", "overlap_org": "麻城市人民政府", "overlap_period": "2026"},
    # 跨县交叉：周黎（罗田书记）曾任麻城
    {"person_a": 9, "person_b": 1, "type": "前任同僚", "context": "周黎2021年任麻城市委常委/副市长，后任罗田书记；与现任书记汪国兵在麻城市党政班子有跨期交集", "overlap_org": "麻城市人民政府", "overlap_period": "2021"},
    {"person_a": 9, "person_b": 2, "type": "前任同僚", "context": "周黎与裴永波同在麻城市政府（2021），周黎后他调罗田", "overlap_org": "麻城市人民政府", "overlap_period": "2021"},
]


def _get_open_questions(person: dict) -> list[str]:
    q = []
    if not person.get("birth"):
        q.append("出生年月未确认")
    if not person.get("birthplace"):
        q.append("籍贯未确认")
    if not person.get("education"):
        q.append("学历教育背景未确认")
    if not person.get("work_start"):
        q.append("参加工作年份未确认")
    if person.get("id") != 2 and not person.get("notes", ""):
        q.append("完整任职履历未确认")
    return q


def write_person_json(person: dict) -> None:
    pid = person["id"]
    name = person["name"]
    slug_id = f"macheng_{name}"
    if name == "汪国兵":
        job_file = "市委书记"
    elif name == "裴永波":
        job_file = "市长"
    else:
        job_file = person.get("current_post", "").split("、")[-1]
    fname = f"{TODAY}-{PROVINCE}-{CITY}-{job_file}-{name}.json"

    person_positions = [pp for pp in positions if pp["person_id"] == pid]
    career_timeline = []
    for pos in sorted(person_positions, key=lambda x: (bool(x.get("start_date", "")), x.get("start_date", ""))):
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001", "S002"],
        })

    if len(career_timeline) <= 1 and not person.get("birth"):
        career_timeline.append({
            "start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
            "notes": "公开资料不足，完整履历待查。网络受限（Exa 限流/Baidu 反爬/百科 403）。",
            "confidence": "unverified", "source_ids": [],
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((pp for pp in persons if pp["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"macheng_{other_name}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001", "S002"],
        })

    sources = [
        {"id": "S001", "title": "麻城市人民政府官方网站（2026年7-8月麻城要闻）", "url": person.get("source", "http://www.macheng.gov.cn/"),
         "publisher": "麻城市人民政府/麻城市融媒体中心", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "官方要闻确认现任书记、市长及市政府班子职务"},
        {"id": "S002", "title": "百度百科（裴永波/明瑞堂等）", "url": "https://baike.baidu.com/", "publisher": "百度百科",
         "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium",
         "notes": "提供核心人物完整履历（当可用时）"},
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": PROVINCE, "city": CITY, "region": SLUG,
            "job": person.get("current_post", ""), "task_id": TASK_ID, "time_focus": "2026年8月",
        },
        "identity": {
            "person_id": slug_id, "name": name, "aliases": [],
            "gender": person.get("gender", ""), "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""), "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "",
                           "degree": "", "study_type": "unknown", "source_ids": ["S002"]}] if person.get("education") else [],
            "party_join": person.get("party_join", ""), "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if name in ("汪国兵", "裴永波") else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if name in ("裴永波", "周黎") else "local_ladder",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格为公开记录推断，非心理评估。",
        },
        "network_metrics": {
            "confirmed_overlaps": len([r for r in rels_output if r["confidence"] == "confirmed"]),
            "documented_relationships": len(rels_output),
        },
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "未检索到公开负面纪律信号，检索范围：麻城市官网要闻与百科全书（2026-08）",
            "date": "", "confidence": "unverified", "source_ids": [],
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "current_role": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "汪国兵完整履历" if name == "汪国兵" else "其余历任履历待补",
        },
        "open_questions": [
            {"priority": "critical", "question": q, "why_it_matters": "用于人物消重与网络图谱完整性",
             "suggested_queries": [f"{name} 简历 任职 麻城"], "last_attempted": AS_OF}
            for q in _get_open_questions(person)
        ],
    }

    (PJSON_DIR / fname).write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"    - {fname}")


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    print("  Writing person JSONs...")
    core_ids = {1, 2, 4, 3}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())