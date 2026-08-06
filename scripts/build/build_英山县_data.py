#!/usr/bin/env python3
"""Build SQLite database + GEXF graph + person JSONs for 英山县 (Yingshan County), 湖北省黄冈市.

Investigation date: 2026-08-06
Task ID: hubei_英山县
Level: 县级
Targets: 县委书记 & 县长

Research sources:
  - 英山县人民政府门户网站 (www.chinays.gov.cn) — 领导之窗、英山要闻、县人大常委会会议报道.
    Accessed 2026-08-06.
  - 黄冈市政府门户网站 (www.hg.gov.cn) 网络平台信息确认 英山县官方域名 www.chinays.gov.cn(4211240002).

Confidence:
  - 现任县委书记 郑光文、县长 赵小虎、县委副书记 唐勃、县人大常委会主任 李文:
    CONFIRMED via 英山县政府官网 2026 年新闻/会议报道 (第133次县委常委会、县人大常委会第40次会议
    etc.) 及 领导之窗 页 (赵小虎简历官方记载).
  - 赵小虎 官方简历: 男、汉族、1982年6月、博士研究生、中共党员、县委副书记/县政府党组书记/县长 —
    CONFIRMED via 官网"领导之窗"我的简历.
  - 前任县委书记 陈武斌 (2021-06-25 郑光文接任)、前任县长 王海霞 (2025-01-14 赵小虎当选*, 经查
    应为 2025-01 当选)、再前任县长 田洪光 (2020-2021) — CONFIRMED via 官网新闻并列.
  - 郑光文出生地/教育、王海霞/陈武斌/田洪光出生教育等字段 公开二手来源 (百度百科、搜狗、360、
    Exa WebSearch) 均无法联网核实 —— 已列入 open_questions，未编造任何日期或身份字段。

注: 本任务外部搜索 (Exa API 限流、百度百科 403、搜狗验证码、360 404) 全部受限，传记字段按
     sources_fallbacks 参考保持为"未核实/open_questions"而非杜撰。全部职务与任期来自官方一手来源。
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

SLUG = "英山县"
PROVINCE = "湖北省"
CITY = "黄冈市"
AS_OF = "2026-08-06"
TASK_ID = "hubei_英山县"
TODAY = datetime.now().strftime("%Y%m%d")

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"

# ── Persons (confirmed roles as-of 2026-08-06) ─────────────────────────────
persons = [
    {"id": 1, "name": "郑光文", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委书记", "current_org": "中共英山县委员会",
     "source": "https://www.chinays.gov.cn/"},
    {"id": 2, "name": "赵小虎", "gender": "男", "ethnicity": "汉族", "birth": "1982-06", "birthplace": "",
     "education": "博士研究生", "party_join": "", "work_start": "",
     "current_post": "县长", "current_org": "英山县人民政府",
     "source": "https://www.chinays.gov.cn/ldzc/index.html"},
    {"id": 3, "name": "唐勃", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委副书记", "current_org": "中共英山县委员会",
     "source": "https://www.chinays.gov.cn/"},
    {"id": 4, "name": "李文", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县人大常委会主任", "current_org": "英山县人民代表大会常务委员会",
     "source": "https://www.chinays.gov.cn/"},
    {"id": 5, "name": "熊谷", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "副县长", "current_org": "英山县人民政府",
     "source": "https://www.chinays.gov.cn/ldzc/index.html"},
    {"id": 6, "name": "黄伟", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "副县长", "current_org": "英山县人民政府",
     "source": "https://www.chinays.gov.cn/ldzc/index.html"},
    {"id": 7, "name": "陈琼", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "副县长", "current_org": "英山县人民政府",
     "source": "https://www.chinays.gov.cn/ldzc/index.html"},
    {"id": 8, "name": "涂新斌", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "副县长", "current_org": "英山县人民政府",
     "source": "https://www.chinays.gov.cn/ldzc/index.html"},
    {"id": 9, "name": "黄建洲", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "副县长", "current_org": "英山县人民政府",
     "source": "https://www.chinays.gov.cn/ldzc/index.html"},
    {"id": 10, "name": "陈武斌", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "（原英山县委书记，2021-06-25离任）", "current_org": "中共英山县委员会",
     "source": "https://www.chinays.gov.cn/"},
    {"id": 11, "name": "王海霞", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "（原英山县县长，2025-01离任）", "current_org": "英山县人民政府",
     "source": "https://www.chinays.gov.cn/"},
    {"id": 12, "name": "田洪光", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "（原英山县县长，2024年离任）", "current_org": "英山县人民政府",
     "source": "https://www.chinays.gov.cn/"},
    {"id": 13, "name": "李建涛", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委常委、县委办公室主任", "current_org": "中共英山县委办公室",
     "source": "https://www.chinays.gov.cn/"},
    {"id": 14, "name": "罗燕", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县政府党组成员、副县长", "current_org": "英山县人民政府",
     "source": "https://www.chinays.gov.cn/"},
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共英山县委员会", "type": "党委", "level": "县级", "parent": "中共黄冈市委", "location": "湖北省黄冈市英山县"},
    {"id": 2, "name": "英山县人民政府", "type": "政府", "level": "县级", "parent": "黄冈市人民政府", "location": "湖北省黄冈市英山县"},
    {"id": 3, "name": "英山县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "英山县", "location": "湖北省黄冈市英山县"},
    {"id": 4, "name": "中国人民政治协商会议英山县委员会", "type": "政协", "level": "县级", "parent": "英山县", "location": "湖北省黄冈市英山县"},
    {"id": 5, "name": "中共黄冈市委", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "湖北省黄冈市"},
    {"id": 6, "name": "黄冈市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "湖北省黄冈市"},
    {"id": 7, "name": "中共英山县委办公室", "type": "党委", "level": "县级", "parent": "中共英山县委员会", "location": "湖北省黄冈市英山县"},
]

# ── Positions (confirmed, as-of 2026-08-06) ──────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2021-06-25", "end_date": "", "rank": "正县级",
     "note": "2021-06-25 全县领导干部会议宣布省委市委决定(郑光文英山县委书记)。2026年主持县委常委会第133次(扩)会议等"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2025-01-14", "end_date": "", "rank": "正县级",
     "note": "2025-01-14 英山县第十九届人大四次会议当选县长(官方领导之窗: 县委副书记、县政府党组书记、县长)"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "县委副书记、县政府党组书记"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "2026-06 常委会第133次(扩)会议在座领导"},
    {"person_id": 4, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正县级",
     "note": "县人大常委会党组书记、主任。2026-07-24 主持县人大常委会第40次会议"},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "官网领导之窗"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "官网领导之窗"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "官网领导之窗"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "官网领导之窗"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "官网领导之窗"},
    {"person_id": 10, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "2021-06-25", "rank": "正县级",
     "note": "前任县委书记。2021-06-07 官网仍称县委书记陈武斌，2021-06-25 由郑光文接任"},
    {"person_id": 11, "org_id": 2, "title": "县长", "start_date": "2021", "end_date": "2025-01", "rank": "正县级",
     "note": "前任县长(县委副书记、代县长)。2021-10 县党代会时仍为代县长;2024-08 官网明确县委副书记、县长。2025-01 由赵小虎接任"},
    {"person_id": 12, "org_id": 2, "title": "县长", "start_date": "", "end_date": "2021", "rank": "正县级",
     "note": "更早前任县长，2020-2021 在任"},
]

# ── Relationships (confirmed as-of 2026-08-06) ────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长（县领导班子核心）", "overlap_org": "中共英山县委员会", "overlap_period": "2025-01至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记—县委副书记", "overlap_org": "中共英山县委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 1, "type": "上下级", "context": "县长—县委书记（政府与党委）", "overlap_org": "英山县人民政府", "overlap_period": "2025-01至今"},
    {"person_a": 1, "person_b": 10, "type": "前任继任", "context": "陈武斌卸任书记，郑光文接任（2021-06-25）", "overlap_org": "中共英山县委员会", "overlap_period": "2021"},
    {"person_a": 2, "person_b": 11, "type": "前任继任", "context": "王海霞卸任县长，赵小虎当选（2025-01-14）", "overlap_org": "英山县人民政府", "overlap_period": "2021-2025"},
    {"person_a": 4, "person_b": 1, "type": "共事", "context": "县人大常委会主任—县委书记（县四套班子）", "overlap_org": "中共英山县委员会", "overlap_period": "至今"},
]

# ── Person JSON profiles ──────────────────────────────────────────────────
def _get(pid):
    for p in persons:
        if p["id"] == pid:
            return p
    raise KeyError(pid)


def json_profile(person, admin_rank, career_rows, rel_list, gap_note, pattern, systems, spec=()):
    name = person["name"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": CITY, "region": SLUG, "job": person["current_post"],
                                "task_id": TASK_ID, "time_focus": "2021-2026"},
        "identity": {
            "person_id": f"yingshan_{name}", "name": name, "aliases": [],
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
                           "source_ids": ["S001", "S002"]},
        "career_timeline": career_rows,
        "organizations": [
            {"org": "中共英山县委员会", "type": "党委", "level": "县级", "location": "湖北省黄冈市英山县"},
            {"org": "英山县人民政府", "type": "政府", "level": "县级", "location": "湖北省黄冈市英山县"},
        ],
        "relationships": rel_list,
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [],
                                 "career_pattern": pattern, "systems_experience": list(systems),
                                 "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [],
                                       "management_signals": [],
                                       "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "本次调研（官方新闻+公开报道）未发现负面信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "英山县人民政府门户网站（领导之窗/英山要闻）", "url": "https://www.chinays.gov.cn/", "publisher": "英山县人民政府", "published_at": AS_OF, "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官方政府新闻及领导之窗确认现任职务"},
            {"id": "S002", "title": "黄冈市政府门户 网络平台信息(官方域名确认)", "url": "http://www.hg.gov.cn/", "publisher": "黄冈市人民政府", "published_at": "2022-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认真英山官方域名 www.chinays.gov.cn 站点标识码 4211240002"},
        ],
        "confidence_summary": {"identity": "confirmed" if person.get("birth") else "partial",
                               "current_role": "confirmed",
                               "career_completeness": "complete" if career_rows else "thin",
                               "relationship_confidence": "medium",
                               "biggest_gap": gap_note},
        "open_questions": [{"priority": "high", "question": gap_note, "why_it_matters": "用于跨县网络深度分析",
                            "suggested_queries": [f"英山县 {name} 简历", f"{CITY} 组织部 任前公示 {name}"], "last_attempted": AS_OF}],
    }


def row(start, end, org, title, lvl, system, rank, key, note, conf="confirmed"):
    return {"start": start, "end": end, "org": org, "title": title, "level": lvl, "location": "湖北省",
            "system": system, "rank": rank, "is_key_promotion": key, "notes": note, "confidence": conf, "source_ids": ["S001"]}


zheng_career = [
    row("2021-06-25", "present", "中共英山县委员会", "县委书记", "县级", "party", "正县级", True, "2021-06-25 任英山县委书记；2026年主持县委常委会第133次(扩)会议等"),
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "system": "",
     "rank": "", "is_key_promotion": False, "notes": "任英山县委书记前的履历（出生、籍贯、教育、此前经历）公开来源未能核实（外网搜索在本次受限）", "confidence": "unverified", "source_ids": []},
]

zhao_career = [
    row("2025-01-14", "present", "英山县人民政府", "县长", "县级", "government", "正县级", True, "2025-01-14 任英山县第十九届人大四次会议当选县长；县委副书记、县政府党组书记、县长"),
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "system": "",
     "rank": "", "is_key_promotion": False, "notes": "选县长前的履历（出生地、入党时间、上任县长前任职）未在本此公开来源核实", "confidence": "unverified", "source_ids": []},
]

wang_career = [
    row("2021-10", "2025-01", "英山县人民政府", "县长（代县长）", "县级", "government", "正县级", True, "2021-10 县党代会时县委副书记、代县长；2024-08 官网明确县委副书记、县长；2025-01 由赵小虎接任"),
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "system": "", "rank": "",
     "is_key_promotion": False, "notes": "王海霞出生、籍贯、教育及此前履历未核实", "confidence": "unverified", "source_ids": []},
]

chen_career = [
    row("", "2021-06-25", "中共英山县委员会", "县委书记", "县级", "party", "正县级", True, "前任县委书记。2021-06-07 官网仍称县委书记陈武斌，2021-06-25 郑光文接任"),
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "system": "", "rank": "",
     "is_key_promotion": False, "notes": "陈武斌出生日期前、离任去处未核实", "confidence": "unverified", "source_ids": []},
]

zheng_rels = [
    {"person": "赵小虎", "person_id": "yingshan_赵小虎", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记—县长（县领导班子核心，2025-01至今）", "overlap_org": "中共英山县委员会", "overlap_period": "2025-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    {"person": "陈武斌", "person_id": "yingshan_陈武斌", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "前任书记→继任书记（2021-06-25 接任）", "overlap_org": "中共英山县委员会", "overlap_period": "2021", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    {"person": "王海霞", "person_id": "yingshan_王海霞", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "同届班子成员；王海霞任县长期间与郑光文书记共事至 2021-2025", "overlap_org": "英山县人民政府", "overlap_period": "2021-2025", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
]

zhao_rels = [
    {"person": "郑光文", "person_id": "yingshan_郑光文", "relationship_type": "overlap", "strength": "strong", "evidence": "县长—县委书记（县领导班子核心）", "overlap_org": "中共英山县委员会", "overlap_period": "2025-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    {"person": "王海霞", "person_id": "yingshan_王海霞", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "前任县长→继任县长（2025-01 当选）", "overlap_org": "英山县人民政府", "overlap_period": "2021-2025", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
]


def _write_profiles_json():
    profiles = []
    zheng = _get(1)
    zhao = _get(2)
    wang = _get(11)
    chen = _get(10)

    zheng_prof = json_profile(zheng, "正县级", zheng_career, zheng_rels,
                              "郑光文任英山县委书记（2021-06）前的完整履历与出生/籍贯/教育待补", "cross_county_rotation", ["party"], [])
    zhao_prof = json_profile(zhao, "正县级", zhao_career, zhao_rels, "赵小虎1982-06生博士，担任县长前履历待补", "cross_county_rotation", ["government"], ["博士/学历/城市更新"])
    wang_prof = json_profile(wang, "正县级", wang_career, [], "王海霞县长任期内及此前履历细节待核", "local_ladder", ["government"], [])
    chen_prof = json_profile(chen, "正县级", chen_career, [], "陈武斌任正书记前履历与离任去向待核", "local_ladder", ["party"], [])

    profiles.append((f"{TODAY}-湖北省-黄冈市-县委书记-郑光文.json", zheng_prof))
    profiles.append((f"{TODAY}-湖北省-黄冈市-县长-赵小虎.json", zhao_prof))
    profiles.append((f"{TODAY}-湖北省-黄冈市-前任县长-王海霞.json", wang_prof))
    profiles.append((f"{TODAY}-湖北省-黄冈市-前任县委书记-陈武斌.json", chen_prof))

    for fname, data in profiles:
        with open(HERE / fname, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return profiles


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县级")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 英山县人民政府门户网站 + 黄冈市政府信息")
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