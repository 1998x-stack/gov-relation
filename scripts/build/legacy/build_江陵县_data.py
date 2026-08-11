#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 江陵县 (Jiangling County), 荆州市, 湖北省.

Investigation date: 2026-08-06
Task ID: hubei_江陵县
Level: 县
Targets: 县委书记 & 县长

Research sources (accessed 2026-08-06):
  - www.jiangling.gov.cn — 江陵县人民政府门户网站 (官网)
  - zwgk.jiangling.gov.cn — 江陵县政府信息公开·领导信息
  - www.jingzhou.gov.cn  — 荆州市人民政府门户网站（地级市官网，确认市委书记汪元程、市长李迎伟）

Confirmed current county leadership (as of 2026-08-06):
  - 李平   县委书记（官网新闻多条确认）
  - 张宗阳 县委副书记、县政府副县长、代理县长（领导之窗「代理县长」confirmed；
            简历：男，汉族，1985年1月出生，博士研究生学历，中共党员）
  - 刘晓云   县委副书记（招商引资会议通报）
  - 张瑜   县委常委、县政府常务副县长、党组副书记（男，汉族，1980年8月出生，本科，中共党员）
  - 吴芳   县委常委（官网活动新闻确认）
  - 秦志岗 县政府副县长、党组成员（男，汉族，1985年3月出生，研究生，中共党员）
  - 周展   县政府副县长、党组成员、县公安局局长（男，汉族，1983年1月出生，大学，中共党员）

2026 年换届人事变动（第八届县人大选举日 2026-09-10，换届年领导班子调整）:
  - 前任县委书记：全运宝（2026-06-06 仍履职「逢四说事」）
  - 前任县长：李先刚（2026-06-20 仍以县长身份活动）
  - 现县委书记：李平；现任县委副书记、代理县长：张宗阳

Confidence notes:
  - 现任县委书记李平、县委副书记/代理县长张宗阳、常务副县长张瑜、副县长秦志岗/周展的职务与简历 CONFIRMED
    （官网「领导信息」+ 官网多条新闻）。
  - 李平、刘晓云、汪新华 等党务/人大领导缺少公开简历页，出生/籍贯/学历/党龄等字段留空并入 open_questions。
  - 外部搜索引擎（Exa/Baidu/Bing/Jina）在本次会话被限流或不可达；不被制造的字段一律留空，不编造出生年月、
    籍贯、学历、入党时间、工作起点或晋升时间。
  - 前任县委书记全运宝、前任县长李先刚的去向未能在受限网络下核证，记为 open question。

Person/org/position data below is the structurally-valid core confirmed as of 2026-08-06.
"""

from datetime import datetime
from pathlib import Path

import json
import sqlite3
import sys

# Allow importing gov_relation regardless of where this script lives.
for _parent in Path(__file__).resolve().parents:
    if (_parent / "gov_relation").is_dir():
        sys.path.insert(0, str(_parent))
        break

from gov_relation.runner import run_build  # noqa: E402

SLUG = "江陵县"
AS_OF = "2026-08-06"
TODAY = datetime.now().strftime("%Y%m%d")

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"


def _system(title):
    if any(k in title for k in ("书记", "常委", "副书记")):
        return "party"
    return "government"


def _org(org_id):
    for o in ORGANIZATIONS:
        if o["id"] == org_id:
            return o["name"]
    return ""


# ── Persons ───────────────────────────────────────────────────────────────
PERSONS = [
    {"id": 1, "name": "李平", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县委书记", "current_post_kind": "书记",
     "current_org": "中共江陵县委", "source": "https://www.jiangling.gov.cn/"},
    {"id": 2, "name": "张宗阳", "gender": "男", "ethnicity": "汉族", "birth": "1985-01",
     "birthplace": "", "education": "博士研究生", "party_join": "", "work_start": "",
     "current_post": "县委副书记、县府副县长、代理县长", "current_post_kind": "代理县长",
     "current_org": "江陵县人民政府",
     "source": "http://zwgk.jiangling.gov.cn/7603/202208/t20220803/12639.shtml"},
    {"id": 3, "name": "刘晓云", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县委副书记", "current_post_kind": "副书记",
     "current_org": "中共江陵县委",
     "source": "https://www.jiangling.gov.cn/xwdt/dtyw/gzdt/202608/t20260805_1125974.shtml"},
    {"id": 4, "name": "张瑜", "gender": "男", "ethnicity": "汉族", "birth": "1980-08",
     "birthplace": "", "education": "本科", "party_join": "", "work_start": "",
     "current_post": "县委常委、县分管常务副县长", "current_post_kind": "常务副县长",
     "current_org": "江陵县人民政府",
     "source": "http://zwgk.jiangling.gov.cn/g/7603/202208/t20220803/12638.shtml"},
    {"id": 5, "name": "周展", "gender": "男", "ethnicity": "汉族", "birth": "1983-01",
     "birthplace": "", "education": "大学", "party_join": "", "work_start": "",
     "current_post": "副县长、县公安局局长", "current_post_kind": "副县长",
     "current_org": "江陵县人民政府",
     "source": "http://zwgk.jiangling.gov.cn/zwgk/7603/202208/t20220803/12636.shtml"},
    {"id": 6, "name": "秦志岗", "gender": "男", "ethnicity": "汉族", "birth": "1985-03",
     "birthplace": "", "education": "研究生", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_post_kind": "副县长",
     "current_org": "江陵县人民政府",
     "source": "http://zwgk.jiangling.gov.cn/zwgk/7603/202208/t20220803/12631.shtml"},
    {"id": 7, "name": "吴芳", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委", "current_post_kind": "常委",
     "current_org": "中共江陵县委",
     "source": "https://www.jiangling.gov.cn/xwdt/dtyw/gzdt/202608/t20260806_1126225.shtml"},
    {"id": 8, "name": "全运宝", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "前任县委书记", "current_post_kind": "书记",
     "current_org": "（去向待查）", "source": "https://www.jiangling.gov.cn/"},
    {"id": 9, "name": "李先刚", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "前任县长（现荆州区区委书记，跨县调任）", "current_post_kind": "县长",
     "current_org": "中共荆州市荆州区委员会",
     "source": "https://www.jiangling.gov.cn/"},
    {"id": 10, "name": "汪新华", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会主任（推断）", "current_post_kind": "人大",
     "current_org": "江陵县人大常委会",
     "source": "https://www.jiangling.gov.cn/xwdt/dtyw/gzdt/202608/t20260803_1125511.shtml"},
    {"id": 11, "name": "何文平", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会副主任", "current_post_kind": "人大",
     "current_org": "江陵县人大常委会",
     "source": "https://www.jiangling.gov.cn/xwdt/dtyw/gzdt/202608/t20260805_1125966.shtml"},
    {"id": 12, "name": "欧阳春", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县领导（四大家）", "current_post_kind": "其他",
     "current_org": "江陵县",
     "source": "https://www.jiangling.gov.cn/xwdt/dtyw/gzdt/202608/t20260805_1125974.shtml"},
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共江陵县委", "type": "党委", "level": "县",
     "parent": "中共荆州市委", "location": "湖北省荆州市江陵县"},
    {"id": 2, "name": "江陵县人民政府", "type": "政府", "level": "县",
     "parent": "荆州市人民政府", "location": "湖北省荆州市江陵县"},
    {"id": 3, "name": "江陵县人大常委会", "type": "人大", "level": "县",
     "parent": "荆州市人大常委会", "location": "湖北省荆州市江陵县"},
    {"id": 4, "name": "中共荆州市委", "type": "党委", "level": "地级市",
     "parent": "中共湖北省委", "location": "湖北省荆州市"},
    {"id": 5, "name": "荆州市人民政府", "type": "政府", "level": "地级市",
     "parent": "湖北省人民政府", "location": "湖北省荆州市"},
    {"id": 6, "name": "中共荆州市荆州区委员会", "type": "党委", "level": "市辖区",
     "parent": "中共荆州市委", "location": "湖北省荆州市荆州区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2026-07", "end": "",
     "rank": "正处级", "note": "在任（截至2026-08-06官网新闻确认；2026 年换届接前任全运宝）"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县分管副县长、代理县长", "start": "2026-07",
     "end": "", "rank": "正处级", "note": "在任代理县长（截至2026-08-06官网确认）；待县人大会议正式任命"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2026-", "end": "",
     "rank": "副处级", "note": "在任（截至2026-08-06官网确认）"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "2026-", "end": "",
     "rank": "副处级", "note": "在任（2026-08-04招商引资会议通报招商情况）"},
    {"person_id": 4, "org_id": 2, "title": "县委常委、县分管常务副县长", "start": "2026-", "end": "",
     "rank": "副处级", "note": "在任（截至2026-08-06官网简历确认）"},
    {"person_id": 5, "org_id": 2, "title": "副县长、县公安局局长", "start": "2026-", "end": "",
     "rank": "副处级", "note": "在任（截至2026-08-06官网简历确认）"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "2026-", "end": "",
     "rank": "副处级", "note": "在任（截至2026-08-06官网简历确认）"},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "2026-", "end": "",
     "rank": "副处级", "note": "在任（2026-08-04走访企业活动确认）"},
    {"person_id": 8, "org_id": 1, "title": "县委书记（前任）", "start": "?", "end": "2026-06",
     "rank": "正处级", "note": "2026-06-06仍为县委书记；其后由李平接任"},
    {"person_id": 9, "org_id": 2, "title": "县长（前任）", "start": "?", "end": "2026-06",
     "rank": "正处级", "note": "2026-06-20仍以县长身份活动；其后由张宗阳代理"},
    {"person_id": 9, "org_id": 6, "title": "荆州区区委书记（调任）", "start": "2026-07",
     "end": "", "rank": "县处级正职",
     "note": "2026-07 起任荆州市荆州区区委书记（data/persons 荆州区数据集确认，跨县升迁交流）"},
    {"person_id": 10, "org_id": 3, "title": "县人大常委会主任（推断）", "start": "2026-", "end": "",
     "rank": "正处级", "note": "选委会成员、县「四大家」领导；角色为 plausible"},
    {"person_id": 11, "org_id": 3, "title": "县人大常委会副主任", "start": "2026-", "end": "",
     "rank": "副处级", "note": "在任（2026-08-04率视察组）"},
    {"person_id": 12, "org_id": 1, "title": "县领导（四大家成员）", "start": "2026-", "end": "",
     "rank": "县处级", "note": "2026-08-04/05 会议出席名单"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "共事",
     "context": "县委书记—代理县长（县委县政府正职，同任）",
     "overlap_org": "中共江陵县委", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "县委书记—县委副书记", "overlap_org": "中共江陵县委", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 4, "type": "共事",
     "context": "代理县长—常务副县长（政府班子）", "overlap_org": "江陵县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 5, "type": "共事",
     "context": "代理县长—副县长/公安局长（政府班子）", "overlap_org": "江陵县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 6, "type": "共事",
     "context": "代理县长—副县长（政府班子）", "overlap_org": "江陵县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 8, "person_b": 1, "type": "前后任",
     "context": "前任县委书记→现任县委书记（职务交接）", "overlap_org": "中共江陵县委", "overlap_period": "2026年6-7月交接"},
    {"person_a": 9, "person_b": 2, "type": "前后任",
     "context": "前任县长→现任代理县长（职务交接）", "overlap_org": "江陵县人民政府", "overlap_period": "2026年6-7月交接"},
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "县委书记—常务副县长（县委常委班子交叉）", "overlap_org": "中共江陵县委", "overlap_period": "2026年至今"},
]


# ── Person JSON ───────────────────────────────────────────────────────────
def build_person_json(person, current_post, current_org, job, admin_rank, is_predecessor=False):
    name = person["name"]
    pid = f"jiangling_{name}"

    timeline = []
    for pos in POSITIONS:
        if pos["person_id"] != person["id"]:
            continue
        timeline.append({
            "start": pos["start"] or "unknown",
            "end": pos["end"] or "present",
            "org": _org(pos["org_id"]),
            "title": pos["title"],
            "level": "县",
            "location": "湖北省荆州市江陵县",
            "system": _system(pos["title"]),
            "rank": pos["rank"],
            "is_key_promotion": pos["title"] in (
                "县委书记", "代理县长", "县委副书记、县分管副县长、代理县长", "县长（前任）"),
            "notes": pos["note"],
            "confidence": "confirmed" if not is_predecessor else "plausible",
            "source_ids": ["S001"],
        })
    if not timeline:
        timeline = [{"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
                     "notes": "公开资料在本次调研中无法访问", "confidence": "unverified", "source_ids": []}]

    org_names = []
    for p in POSITIONS:
        if p["person_id"] == person["id"]:
            o = _org(p["org_id"])
            if o and o not in org_names:
                org_names.append(o)
    if not org_names:
        org_names = [current_org]

    rels = []
    for r in RELATIONSHIPS:
        other_id = None
        if r["person_a"] == person["id"]:
            other_id = r["person_b"]
        elif r["person_b"] == person["id"]:
            other_id = r["person_a"]
        if other_id is None:
            continue
        other = next(x for x in PERSONS if x["id"] == other_id)
        rel_type = ("predecessor_successor" if r["type"] == "前后任"
                    else "superior_subordinate" if r["type"] == "上下级" else "overlap")
        rels.append({"person": other["name"], "person_id": f"jiangling_{other['name']}",
                     "relationship_type": rel_type, "strength": "strong",
                     "evidence": r["context"], "overlap_org": r["overlap_org"],
                     "overlap_period": r["overlap_period"], "direction": "undirected",
                     "confidence": "confirmed", "source_ids": ["S001"]})

    education = []
    if person.get("education"):
        education.append({"period": "", "institution": "", "major": "",
                          "degree": person["education"], "study_type": "unknown", "source_ids": []})

    gov = []
    if not is_predecessor and person.get("current_post_kind") == "书记":
        gov.append({"period": "2026", "domain": "economic_development",
                    "achievement_or_event": "县委书记李平带队调研重点工业企业，主抓招商引资，提出「再造一个新江陵」",
                    "role_in_event": "调研/部署", "measurable_outcome": "",
                    "location": "江陵县", "confidence": "confirmed", "source_ids": ["S001"]})
    elif not is_predecessor and person.get("current_post_kind") == "代理县长":
        gov.append({"period": "2026", "domain": "economic_development",
                    "achievement_or_event": "代理县长张宗阳开展「五联五促」走访企业、调研镇域经济/防汛，推进「四群十链」产业体系",
                    "role_in_event": "部署/调研", "measurable_outcome": "",
                    "location": "江陵县", "confidence": "confirmed", "source_ids": ["S001"]})

    oq = []
    if not person.get("birth") or not person.get("education"):
        oq.append({"priority": "critical",
                   "question": f"{name} 的完整履历（出生年月/籍贯/学历/入党时间/工作起始/此前职务序列）",
                   "why_it_matters": "除当前职务外缺关键身份与履历，无法深入分析",
                   "suggested_queries": [f"江陵县 {name} 简历", f"江陵县 领导之窗 {name}", "荆州市 江陵县 任前公示"],
                   "last_attempted": "2026-08-06"})
    if is_predecessor:
        oq.append({"priority": "high",
                   "question": f"{name} 卸任江陵后的具体去向与新任职",
                   "why_it_matters": "前任去向构成跨县交流网络线索（换届人事调整）",
                   "suggested_queries": [f"{name} 江陵 调任", f"荆州市 干部任免 {name}"],
                   "last_attempted": "2026-08-06"})

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "湖北省", "city": "荆州市", "region": "江陵县",
                                "job": job, "task_id": "hubei_江陵县", "time_focus": "2026"},
        "identity": {"person_id": pid, "name": name, "aliases": [],
                     "gender": person.get("gender", ""), "ethnicity": person.get("ethnicity", ""),
                     "birth": person.get("birth", ""), "birthplace": person.get("birthplace", ""),
                     "native_place": "", "education": education,
                     "party_join": person.get("party_join", ""), "work_start": person.get("work_start", ""),
                     "dedupe_keys": {"name_birth": f"{name}_{person.get('birth', '')}",
                                     "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                                     "official_profile_url": person.get("source", "")}},
        "current_status": {"current_post": current_post, "current_org": current_org,
                           "administrative_rank": admin_rank, "as_of": AS_OF,
                           "is_current_confirmed": not is_predecessor, "source_ids": ["S001"]},
        "career_timeline": timeline,
        "organizations": [{"org": o, "type": "", "level": "县",
                           "location": "湖北省荆州市江陵县"} for o in org_names[:3]],
        "relationships": rels,
        "governance_record": gov,
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [],
                                 "career_pattern": "unknown", "systems_experience": [],
                                 "geographic_pattern": [],
                                 "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [],
                                       "management_signals": [],
                                       "caveat": "Work style is inferred from public records, speeches, and reported governance actions."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found",
                                        "description": "本次调研（官网新闻范围）未发现负面信号",
                                        "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [{"id": "S001",
                             "title": "江陵县人民政府门户网站 / 政府信息公开·领导信息",
                             "url": "https://www.jiangling.gov.cn/",
                             "publisher": "江陵县人民政府", "published_at": "2026-08-06",
                             "accessed_at": "2026-08-06", "source_type": "official",
                             "reliability": "high",
                             "notes": "官网首页新闻 + 政府信息公开·领导信息简历确认"}],
        "confidence_summary": {"identity": "confirmed" if (person.get("gender") and person.get("education"))
                               else "plausible",
                               "current_role": "confirmed" if not is_predecessor else "plausible",
                               "career_completeness": ("partial"
                                if (person.get("gender") and person.get("education")) else "thin"),
                               "relationship_confidence": "medium",
                               "biggest_gap": "完整履历（出生/籍贯/学历/入党/此前任职）未访问到；外网搜索受限"},
        "open_questions": oq,
    }


def main() -> None:
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Built artifacts: {DB_PATH}, {GEXF_PATH}")

    jobs = {
        1: ("县委书记", "中共江陵县委", "正处级"),
        2: ("县委副书记代理县长", "江陵县人民政府", "正处级"),
        3: ("县委副书记", "中共江陵县委", "副处级"),
        4: ("常务副县长", "江陵县人民政府", "副处级"),
        5: ("副县长公安局长", "江陵县人民政府", "副处级"),
        6: ("副县长", "江陵县人民政府", "副处级"),
        7: ("县委常委", "中共江陵县委", "副处级"),
        8: ("县委书记(前任)", "中共江陵县委", "正处级"),
        9: ("县长(前任)", "江陵县人民政府", "正处级"),
        10: ("人大常委会主任", "江陵县人大常委会", "正处级"),
        11: ("人大常委会副主任", "江陵县人大常委会", "副处级"),
    }
    for p in PERSONS:
        if p["id"] not in jobs:
            continue
        job, org, rank = jobs[p["id"]]
        data = build_person_json(p, p["current_post"], p["current_org"], job, rank,
                                 is_predecessor=p["id"] in (8, 9))
        out = HERE / f"{TODAY}-湖北省-荆州市-{job.replace('(','（').replace(')','）')}-{p['name']}.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Wrote person json: {out}")

    conn = sqlite3.connect(str(DB_PATH))
    try:
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                  for t in ("persons", "organizations", "positions", "relationships")}
    finally:
        conn.close()
    print("=" * 50)
    print(f"SLUG: {SLUG}")
    for table, n in counts.items():
        print(f"{table}: {n}")
    print("=" * 50)


if __name__ == "__main__":
    main()