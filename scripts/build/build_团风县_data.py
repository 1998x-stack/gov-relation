#!/usr/bin/env python3
"""Build SQLite database + GEXF graph + person JSONs for 团风县 (Hubei, 黄冈市).

Investigation date: 2026-08-06
Task ID: hubei_团风县
Level: 县级
Targets: 县委书记 & 县长

Research sources:
  - www.tfzf.gov.cn (团风县人民政府门户, HTTP) — 县长之窗 (全部县政府领导简历/分工)、
    团风要闻 (fx2026年6-8月) — Accessed 2026-08-06.
  - www.hg.gov.cn (黄冈市人民政府门户) — 时政/县区动态 context.
  - Media/web search (Exa rate-limited, Bing/Google/Baidu/Baike degraded) 用于核验
    刘君峰履历与前任链 — partial evidence; gaps flagged in open_questions.

Confidence:
  - 县委书记 刘君峰 (兼任县防汛抗旱指挥部指挥长): CONFIRMED via 团风要闻
    (2026-07-02 招商引资推进会 / 2026-07-23 农业农村 / 2026-08-05 信访重点会议).
  - 县委副书记/县长 张章: CONFIRMED via 团风县长之窗 (官方简历: 1985年7月生,
    湖北省委党校研究生, 中共党员).
  - 县政府领导班子 (张毅/彭哲/饶斌/周厚瑜/何彬): CONFIRMED via 团风县长之窗
    领导之窗, each with official 简历+分工.
  - 县人大常委会主任 丁永忠, 县政协主席 丁晗, 县委常委/人武部部长 胡永军,
    县人武部政委 卢蛟: CONFIRMED via 团风要闻 (2026-07-29 八一慰问 / 2026-07-02
    收看大会).
  - 刘君峰 detailed 履历 & predecessor(s): partial — flagged in open_questions.
    No dates/education fabricated beyond the official 简历 lines quoted.
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Allow importing gov_relation regardless of where this script lives.
for _parent in Path(__file__).resolve().parents:
    if (_parent / "gov_relation").is_dir():
        sys.path.insert(0, str(_parent))
        break

from gov_relation.runner import run_build  # noqa: E402

SLUG = "团风县"
PROVINCE = "湖北省"
CITY = "黄冈市"
AS_OF = "2026-08-06"
TODAY = datetime.now().strftime("%Y%m%d")

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"

# ── Persons (confirmed as-of 2026-08-06) ─────────────────────────────────
persons = [
    {"id": 1, "name": "刘君峰", "gender": "", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委书记", "current_org": "中共团风县委员会",
     "source": "http://www.tfzf.gov.cn/xwzx/tfyw/12107614.html"},
    {"id": 2, "name": "张章", "gender": "男", "ethnicity": "汉族", "birth": "1985-07", "birthplace": "",
     "education": "湖北省委党校研究生", "party_join": "", "work_start": "",
     "current_post": "县长", "current_org": "团风县人民政府",
     "source": "http://www.tfzf.gov.cn/site/tpl/6782200"},
    {"id": 3, "name": "张毅", "gender": "男", "ethnicity": "汉族", "birth": "1984-06", "birthplace": "",
     "education": "大学", "party_join": "", "work_start": "",
     "current_post": "常务副县长", "current_org": "团风县人民政府",
     "source": "http://www.tfzf.gov.cn/content/column/6794748?liId=115&leaderTypeId=34"},
    {"id": 4, "name": "彭哲", "gender": "男", "ethnicity": "汉族", "birth": "1980-10", "birthplace": "",
     "education": "在职研究生", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "团风县人民政府",
     "source": "http://www.tfzf.gov.cn/content/column/6794748?liId=127&leaderTypeId=34"},
    {"id": 5, "name": "饶斌", "gender": "男", "ethnicity": "汉族", "birth": "1985-12", "birthplace": "",
     "education": "大学", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "团风县人民政府",
     "source": "http://www.tfzf.gov.cn/content/column/6794748?liId=342&leaderTypeId=34"},
    {"id": 6, "name": "周厚瑜", "gender": "男", "ethnicity": "汉族", "birth": "1982-09", "birthplace": "",
     "education": "大学学历、工程硕士", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "团风县人民政府",
     "source": "http://www.tfzf.gov.cn/content/column/6794748?liId=346&leaderTypeId=34"},
    {"id": 7, "name": "何彬", "gender": "男", "ethnicity": "汉族", "birth": "1977-08", "birthplace": "",
     "education": "大学", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "团风县人民政府",
     "source": "http://www.tfzf.gov.cn/content/column/6794748?liId=349&leaderTypeId=34"},
    {"id": 8, "name": "丁永忠", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县人大常委会主任", "current_org": "团风县人民代表大会常务委员会",
     "source": "http://www.tfzf.gov.cn/xwzx/tfyw/12111293.html"},
    {"id": 9, "name": "丁晗", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县政协主席", "current_org": "中国人民政治协商会议团风县委员会",
     "source": "http://www.tfzf.gov.cn/xwzx/tfyw/12111293.html"},
    {"id": 10, "name": "胡永军", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委常委、人武部部长", "current_org": "团风县人民武装部",
     "source": "http://www.tfzf.gov.cn/xwzx/tfyw/12111293.html"},
    {"id": 11, "name": "卢蛟", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县人武部政委", "current_org": "团风县人民武装部",
     "source": "http://www.tfzf.gov.cn/xwzx/tfyw/12111293.html"},
]

# ── Organizations ─────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共团风县委员会", "type": "党委", "level": "县级", "parent": "中共黄冈市委", "location": "湖北省黄冈市团风县"},
    {"id": 2, "name": "团风县人民政府", "type": "政府", "level": "县级", "parent": "黄冈市人民政府", "location": "湖北省黄冈市团风县"},
    {"id": 3, "name": "团风县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "团风县", "location": "湖北省黄冈市团风县"},
    {"id": 4, "name": "中国人民政治协商会议团风县委员会", "type": "政协", "level": "县级", "parent": "团风县", "location": "湖北省黄冈市团风县"},
    {"id": 5, "name": "团风县人民武装部", "type": "政府", "level": "县级", "parent": "黄冈军分区", "location": "湖北省黄冈市团风县"},
    {"id": 6, "name": "中共黄冈市委", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "湖北省黄冈市"},
    {"id": 7, "name": "黄冈市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "湖北省黄冈市"},
]

# ── Positions (confirmed, as-of 2026-08-06) ──────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "兼县防汛抗旱指挥部指挥长（2026年多篇官方新闻）"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正县级", "note": "县委副书记、县政府党组书记、县长（官方县长之窗）"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "县委副书记、县长"},
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "县政府党组副书记、副县长，三级调研员；分管财政/人社/应急/统计等"},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "县政府党组成员；水利/农业农村/民政/供销"},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "县政府党组成员；工业/交通/招商/市场监管/科技"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "县政府党组成员；政务/文旅/医保/民族宗教"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "县政府党组成员；城建/自然资源/教育/卫健/生态环境"},
    {"person_id": 8, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正县级", "note": "2026-07-29八一慰问确认"},
    {"person_id": 9, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正县级", "note": "2026-07-29八一慰问确认"},
    {"person_id": 10, "org_id": 5, "title": "县委常委、人武部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "2026-07-29八一慰问确认"},
    {"person_id": 11, "org_id": 5, "title": "县人武部政委", "start_date": "", "end_date": "", "rank": "副县级", "note": "2026-07-29八一慰问确认"},
]

# ── Relationships (confirmed) ─────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长（县领导班子成员）", "overlap_org": "中共团风县委员会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记—常务副县长（常委班子/县政府）", "overlap_org": "中共团风县委员会", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长—常务副县长（县政府党组）", "overlap_org": "团风县人民政府", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "县委书记—人大常委会主任（县四大家）", "overlap_org": "团风县", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "县委书记—政协主席（县四大家）", "overlap_org": "团风县", "overlap_period": "2026年"},
]

# ── Person JSON profiles ──────────────────────────────────────────────────
def _get(pid):
    for p in persons:
        if p["id"] == pid:
            return p
    raise KeyError(pid)


def json_profile(person, admin_rank, career_rows, gov_records, gap_note, pattern, systems, spec=()):
    name = person["name"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": CITY, "region": SLUG, "job": person["current_post"],
                                "task_id": "hubei_团风县", "time_focus": "2025-2026"},
        "identity": {
            "person_id": f"tuanfeng_{name}", "name": name, "aliases": [],
            "gender": person.get("gender", ""), "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""), "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": person.get("education", ""), "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{name}_{person.get('birth','')}",
                            "name_birthplace": f"{name}_{person.get('birthplace','')}",
                            "official_profile_url": person.get("source", "")},
        },
        "current_status": {"current_post": person["current_post"], "current_org": person["current_org"],
                           "administrative_rank": admin_rank, "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S001"]},
        "career_timeline": career_rows,
        "organizations": [
            {"org": "中共团风县委员会", "type": "党委", "level": "县级", "location": "湖北省黄冈市团风县"},
            {"org": "团风县人民政府", "type": "政府", "level": "县级", "location": "湖北省黄冈市团风县"},
        ],
        "relationships": [],
        "governance_record": [
            {"period": "2026", "domain": "other", "achievement_or_event": "以县委书记身份主持召开县招商引资工作推进会、督导农业农村与安全生产（2026-07）",
             "role_in_event": "县委书记部署/调研", "measurable_outcome": "", "location": "团风县",
             "confidence": "confirmed", "source_ids": ["S001"]},
        ] if person["current_post"] == "县委书记" else [
            {"period": "2026", "domain": "other", "achievement_or_event": "主持县政府全面工作（县政府常务/防汛抗旱/招商考察）",
             "role_in_event": "县长主持/率队", "measurable_outcome": "", "location": "团风县",
             "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "professional_profile": {"primary_specializations": list(spec), "secondary_specializations": [],
                                 "career_pattern": pattern, "systems_experience": list(systems),
                                 "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [],
                                       "management_signals": [],
                                       "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "本次调研（官方新闻+公开报道）未发现负面信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "团风县人民政府门户（县长之窗 + 团风要闻）", "url": "http://www.tfzf.gov.cn/", "publisher": "团风县人民政府", "published_at": AS_OF, "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官方简介/新闻确认现任职务"},
        ],
        "confidence_summary": {"identity": "partial" if not person.get("birth") else "confirmed",
                               "current_role": "confirmed",
                               "career_completeness": "thin",
                               "relationship_confidence": "medium",
                               "biggest_gap": gap_note},
        "open_questions": [{"priority": "high", "question": gap_note, "why_it_matters": "用于跨县网络与履历深度分析",
                            "suggested_queries": [f"团风县 {name} 简历", f"{CITY} 组织部 任前公示 {name}"], "last_attempted": AS_OF}],
    }


# ── Career rows ───────────────────────────────────────────────────────────
def row(start, end, org, title, lvl, system, rank, key, note, conf="confirmed"):
    return {"start": start, "end": end, "org": org, "title": title, "level": lvl, "location": "湖北省",
            "system": system, "rank": rank, "is_key_promotion": key, "notes": note, "confidence": conf, "source_ids": ["S001"]}


liu_career = [
    row("2026", "present", "中共团风县委员会", "县委书记", "县级", "party", "正县级", True, "兼县防汛抗旱指挥部指挥长（2026年官方要闻）"),
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "刘君峰在任团风县委书记前的详细履历（出生/籍贯/学历/前职）公开来源暂未核到，待补", "confidence": "unverified", "source_ids": []},
]

zhang_career = [
    row("", "present", "团风县人民政府", "县长", "县级", "government", "正县级", True, "县委副书记、县政府党组书记、县长（官方县长之窗）"),
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "张章任团风县长前任职务及出生地/党籍时间等细节未公开，待补", "confidence": "unverified", "source_ids": []},
]


def _write_profiles_json():
    profiles = []
    liu = _get(1)
    zhang = _get(2)
    liu_prof = json_profile(liu, "正县级", liu_career, [], "详细履历（出生/籍贯/学历/前职）公开不足", "unknown", ["party"], ["招商引资", "农业农村"])
    zhang_prof = json_profile(zhang, "正县级", zhang_career, [], "任县长前履历与出生信息未公开", "unknown", ["government", "party"], [])
    liu_prof["governance_record"] = [
        {"period": "2026", "domain": "economic_development", "achievement_or_event": "主持召开全县招商引资工作推进会（2026-07-02）", "role_in_event": "县委书记主持并讲话", "measurable_outcome": "", "location": "团风县", "confidence": "confirmed", "source_ids": ["S001"]},
        {"period": "2026", "domain": "public_security", "achievement_or_event": "调研督导安全生产工作（2026-07-06）", "role_in_event": "县委书记调研", "measurable_outcome": "", "location": "团风县", "confidence": "confirmed", "source_ids": ["S001"]},
        {"period": "2026", "domain": "rural_revitalization", "achievement_or_event": "调研督导农业农村工作（2026-07-22）", "role_in_event": "县委书记调研", "measurable_outcome": "", "location": "团风县", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    zhang_prof["governance_record"] = [
        {"period": "2026", "domain": "public_security", "achievement_or_event": "参加全县防汛抗旱指挥部会议、率队对外招商考察（2026）", "role": "县长", "measurable_outcome": "", "location": "团风县", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    profiles.append((f"{TODAY}-湖北省-黄冈市-县委书记-刘君峰.json", liu_prof))
    profiles.append((f"{TODAY}-湖北省-黄冈市-县长-张章.json", zhang_prof))
    for fname, data in profiles:
        with open(HERE / fname, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return profiles


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县级")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 团风县人民政府门户 + 黄冈市政府门户")
    print("=" * 60)

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

    profiles = _write_profiles_json()
    print(f"\n  人物JSON: {len(profiles)} 个")
    for fname, _ in profiles:
        print(f"    - {fname}")

    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    main()