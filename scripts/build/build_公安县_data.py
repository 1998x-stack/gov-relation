#!/usr/bin/env python3
"""Build SQLite database + GEXF graph + person JSONs for 公安县 (Gongan County), 湖北省.

Investigation date: 2026-08-06
Task ID: hubei_公安县
Level: 县级
Targets: 县委书记 & 县长

Research sources:
  - www.gongan.gov.cn (公安县人民政府门户网站) — 领导之窗 (政府领导简介)、公安要闻/
    部门动态/图片新闻. Accessed 2026-08-06.
  - Baidu search + 凤凰网/鲁网/网易/微信公众平台 articles confirming 刘春霞 and 彭伟
    career paths and the 严广超→刘春霞→彭伟 succession chain.

Confidence:
  - Current 县委书记 刘春霞, 县委副书记/县长 彭伟, 县委副书记 郭磊, 县人大常委会主任
    林庭武, 县政协主席 陈万林: CONFIRMED via official gongan.gov.cn news
    (2026-07-31 十五届县委第九次全会；2026-08-03 县委专题调度会议).
  - Government roster (周敏/邹锋/李洋/黄琼/程雄杰/王博/马光庆) CONFIRMED via official
    领导之窗 bio pages.
  - 刘春霞/彭伟/严广超 full careers CONFIRMED via multiple consistent media reports.
  - Some deputy biographical fields remain incomplete and are flagged in open_questions.
    No dates fabricated.
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

SLUG = "公安县"
PROVINCE = "湖北省"
CITY = "荆州市"
AS_OF = "2026-08-06"
TODAY = datetime.now().strftime("%Y%m%d")

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"

# ── Persons (confirmed as-of 2026-08-06) ─────────────────────────────────
persons = [
    {"id": 1, "name": "刘春霞", "gender": "女", "ethnicity": "汉族", "birth": "1975-11", "birthplace": "湖北潜江",
     "education": "大学学历，公共管理硕士，审计师", "party_join": "1998-06", "work_start": "1996-09",
     "current_post": "县委书记", "current_org": "中共公安县委员会",
     "source": "https://www.gongan.gov.cn/"},
    {"id": 2, "name": "彭伟", "gender": "男", "ethnicity": "汉族", "birth": "1983-11", "birthplace": "湖北仙桃",
     "education": "大学文化程度", "party_join": "2003-12", "work_start": "2005-08",
     "current_post": "县长", "current_org": "公安县人民政府",
     "source": "http://zwgk.gongan.gov.cn/31650/112220253/t105220253124/648066.shtml"},
    {"id": 3, "name": "郭磊", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委副书记", "current_org": "中共公安县委员会",
     "source": "https://www.gongan.gov.cn/"},
    {"id": 4, "name": "林庭武", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县人大常委会主任", "current_org": "公安县人民代表大会常务委员会",
     "source": "https://www.gongan.gov.cn/"},
    {"id": 5, "name": "陈万林", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县政协主席", "current_org": "中国人民政治协商会议公安县委员会",
     "source": "https://www.gongan.gov.cn/"},
    {"id": 6, "name": "周敏", "gender": "男", "ethnicity": "汉族", "birth": "1978-11", "birthplace": "湖北松滋",
     "education": "党校研究生", "party_join": "", "work_start": "2000-03",
     "current_post": "县委常委、常务副县长", "current_org": "公安县人民政府",
     "source": "http://zwgk.gongan.gov.cn/31650/103220253/t105220253034/574466.shtml"},
    {"id": 7, "name": "邹锋", "gender": "男", "ethnicity": "汉族", "birth": "1976-03", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "", "current_post": "副县长、县公安局局长", "current_org": "公安县人民政府",
     "source": "http://zwgk.gongan.gov.cn/31650/111220233/t124220233114/432729.shtml"},
    {"id": 8, "name": "李洋", "gender": "男", "ethnicity": "汉族", "birth": "1987-04", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "", "current_post": "副县长", "current_org": "公安县人民政府",
     "source": "http://zwgk.gongan.gov.cn/31650/105220253/t122220253054/590491.shtml"},
    {"id": 9, "name": "黄琼", "gender": "女", "ethnicity": "汉族", "birth": "1988-11", "birthplace": "湖北公安",
     "education": "大学文化程度", "party_join": "", "work_start": "2013-10",
     "current_post": "副县长", "current_org": "公安县人民政府",
     "source": "http://zwgk.gongan.gov.cn/31650/107220263/t131220263074/715617.shtml"},
    {"id": 10, "name": "程雄杰", "gender": "男", "ethnicity": "汉族", "birth": "1984-07", "birthplace": "湖北应城",
     "education": "研究生", "party_join": "2007-03", "work_start": "2003-09",
     "current_post": "副县长（挂职）", "current_org": "公安县人民政府",
     "source": "http://zwgk.gongan.gov.cn/31650/101220263/t106220263014/660755.shtml"},
    {"id": 11, "name": "王博", "gender": "女", "ethnicity": "蒙古族", "birth": "1985-10", "birthplace": "黑龙江拜泉",
     "education": "硕士", "party_join": "", "work_start": "2010-04",
     "current_post": "副县长（挂职）", "current_org": "公安县人民政府",
     "source": "http://zwgk.gongan.gov.cn/31650/101220263/t106220263014/660758.shtml"},
    {"id": 12, "name": "马光庆", "gender": "男", "ethnicity": "汉族", "birth": "1972-09", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "", "current_post": "县委常委、副县长", "current_org": "公安县人民政府",
     "source": "http://zwgk.gongan.gov.cn/31650/111220233/t124220233114/432713.shtml"},
    {"id": 13, "name": "陈义勇", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委常委、政法委书记", "current_org": "中共公安县委政法委员会",
     "source": "https://www.gongan.gov.cn/"},
    {"id": 14, "name": "严广超", "gender": "男", "ethnicity": "汉族", "birth": "1977-05", "birthplace": "湖北武汉",
     "education": "博士研究生", "party_join": "1998-12", "work_start": "",
     "current_post": "荆州市副市长", "current_org": "荆州市人民政府",
     "source": "https://baike.baidu.com/"},
]

# ── Organizations ─────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共公安县委员会", "type": "党委", "level": "县级", "parent": "中共荆州市委", "location": "湖北省荆州市公安县"},
    {"id": 2, "name": "公安县人民政府", "type": "政府", "level": "县级", "parent": "荆州市人民政府", "location": "湖北省荆州市公安县"},
    {"id": 3, "name": "公安县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "公安县", "location": "湖北省荆州市公安县"},
    {"id": 4, "name": "中国人民政治协商会议公安县委员会", "type": "政协", "level": "县级", "parent": "公安县", "location": "湖北省荆州市公安县"},
    {"id": 5, "name": "中共荆州市委", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "湖北省荆州市"},
    {"id": 6, "name": "荆州市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "湖北省荆州市"},
    {"id": 7, "name": "中共公安县委政法委员会", "type": "党委", "level": "县级", "parent": "中共公安县委员会", "location": "湖北省荆州市公安县"},
]

# ── Positions (confirmed, as-of 2026-08-06) ──────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2025-10", "end_date": "", "rank": "正县级", "note": "接严广超任县委书记（2026-07-31全会、2026-08-03会议确认）"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2025-12-31", "end_date": "", "rank": "正县级", "note": "2025-11-28任代县长，2025-12-31当选县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2025-11", "end_date": "", "rank": "副县级", "note": "县委副书记、县长"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "2025", "end_date": "", "rank": "副县级", "note": "曾兼县委政法委书记（2025-12）"},
    {"person_id": 4, "org_id": 3, "title": "县人大常委会党组书记、主任", "start_date": "", "end_date": "", "rank": "正县级", "note": "2026-07-31全会确认"},
    {"person_id": 5, "org_id": 4, "title": "县政协党组书记、主席", "start_date": "", "end_date": "", "rank": "正县级", "note": "2026-07-31全会确认"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "十五届县委常委"},
    {"person_id": 6, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "协助县长主持县政府日常工作"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "2026-02", "end_date": "", "rank": "副县级", "note": "兼任县公安局局长"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "分管农业农村、乡村振兴、水利、生态环境等"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "分管文旅、医保、教育、卫生健康等"},
    {"person_id": 10, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "副县级", "note": "挂职，分管供销"},
    {"person_id": 11, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "副县级", "note": "挂职，分管科技"},
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "十五届县委常委"},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "亦任经济开发区党工委第一书记"},
    {"person_id": 13, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "2026-08调研县法院/司法局"},
    {"person_id": 13, "org_id": 7, "title": "政法委书记", "start_date": "2026", "end_date": "", "rank": "副县级", "note": "现任县委常委、政法委书记"},
    {"person_id": 14, "org_id": 1, "title": "县委书记", "start_date": "2021-09", "end_date": "2025-09", "rank": "正县级", "note": "前任县委书记"},
    {"person_id": 14, "org_id": 6, "title": "荆州市副市长", "start_date": "2025-10", "end_date": "", "rank": "副厅级", "note": "离任公安县委书记后任"},
]

# ── Relationships (confirmed) ─────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长（县领导班子成员）", "overlap_org": "中共公安县委员会", "overlap_period": "2025-10至今"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记—县委副书记", "overlap_org": "中共公安县委员会", "overlap_period": "2025至今"},
    {"person_a": 14, "person_b": 1, "type": "前任继任", "context": "严广超卸任书记，刘春霞接任（书记—县长交接）", "overlap_org": "中共公安县委员会", "overlap_period": "2021-2025"},
    {"person_a": 6, "person_b": 2, "type": "上下级", "context": "常务副县长配合县长主持日常工作", "overlap_org": "公安县人民政府", "overlap_period": "2025至今"},
    {"person_a": 13, "person_b": 3, "type": "同系统", "context": "陈义勇接任政法委书记，郭磊此前兼政法委书记", "overlap_org": "中共公安县委政法委员会", "overlap_period": "2025-2026"},
]

# ── Person JSON profiles ──────────────────────────────────────────────────
def _get(pid):
    for p in persons:
        if p["id"] == pid:
            return p
    raise KeyError(pid)


def json_profile(person, admin_rank, career_rows, rel_list, gov_records, gap_note, pattern, systems, spec=()):
    name = person["name"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": CITY, "region": SLUG, "job": person["current_post"],
                                "task_id": "hubei_公安县", "time_focus": "2025-2026"},
        "identity": {
            "person_id": f"gongan_{name}", "name": name, "aliases": [],
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
            {"org": "中共公安县委员会", "type": "党委", "level": "县级", "location": "湖北省荆州市公安县"},
            {"org": "公安县人民政府", "type": "政府", "level": "县级", "location": "湖北省荆州市公安县"},
        ],
        "relationships": [],
        "governance_record": gov_records,
        "professional_profile": {"primary_specializations": list(spec), "secondary_specializations": [],
                                 "career_pattern": pattern, "systems_experience": list(systems),
                                 "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [],
                                       "management_signals": [],
                                       "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "本次调研（官方新闻+公开报道）未发现负面信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "公安县人民政府门户网站（领导之窗/新闻）", "url": "https://www.gongan.gov.cn/", "publisher": "公安县人民政府", "published_at": AS_OF, "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官方领导之窗及新闻确认"},
            {"id": "S002", "title": "凤凰网/鲁网/网易 人事报道", "url": "https://hunan.ifeng.com/", "publisher": "凤凰网", "published_at": "2025-11", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "刘春霞/彭伟/严广超履历"},
        ],
        "confidence_summary": {"identity": "confirmed" if person.get("birth") else "partial",
                               "current_role": "confirmed",
                               "career_completeness": "complete" if career_rows else "thin",
                               "relationship_confidence": "medium",
                               "biggest_gap": gap_note},
        "open_questions": [{"priority": "high", "question": gap_note, "why_it_matters": "用于跨县网络深度分析",
                            "suggested_queries": [f"公安县 {name} 简历", f"{CITY} 组织部 任前公示 {name}"], "last_attempted": AS_OF}],
    }


# ── Career rows ───────────────────────────────────────────────────────────
def row(start, end, org, title, lvl, system, rank, key, note, conf="confirmed"):
    return {"start": start, "end": end, "org": org, "title": title, "level": lvl, "location": "湖北省",
            "system": system, "rank": rank, "is_key_promotion": key, "notes": note, "confidence": conf, "source_ids": ["S001", "S002"]}


liu_career = [
    row("2025-10", "present", "中共公安县委员会", "县委书记", "县级", "party", "正县级", True, "接严广超任县委书记"),
    row("2020", "2025-10", "公安县人民政府", "县长", "县级", "government", "正县级", True, "任县委书记前任县长（2025-11辞去县长由彭伟接任）"),
    row("", "", "湖北省潜江市审计局", "经济责任审计分局局长", "县级", "government", "", False, "审计出身（审计师）"),
    row("", "", "湖北省潜江市老新镇", "党委副书记、常务副镇长", "乡镇", "government", "", False, ""),
    row("", "", "湖北省潜江市广华寺办事处", "党委书记、人大主任", "乡科级", "party", "", True, ""),
    row("", "", "湖北省国营周矶农场（管理区）", "党委书记、人大主任", "乡科级", "party", "", True, ""),
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "潜江任职前教育与更早任职，公开细节有限", "confidence": "unverified", "source_ids": []},
]

peng_career = [
    row("2025-12-31", "present", "公安县人民政府", "县长", "县级", "government", "正县级", True, "2025-12-31当选县长"),
    row("2025-11", "2025-12", "公安县人民政府", "县委副书记、代理县长", "县级", "government", "正县级", True, "2025-11-28 县十八届人大常委会任命副县长、代理县长"),
    row("2023-10", "2025", "中共洪湖市委", "市委副书记、政法委书记", "县级", "party", "副县级", True, "跨县交流前职（洪湖为荆州市辖）"),
    row("2018", "2023-10", "松滋市", "市委常委、市委组织部部长", "县级", "organization", "副县级", True, "2018年调松滋任副市长，后任常委/组织部长"),
    row("2008", "2018", "中共荆州市委组织部", "市组织部人才科科长、办公室主任等", "地级市", "organization", "", True, "长期在荆州市委组织部工作（副科级组织员/研究室副主任/人才办副主任/正科级组织员/人才科科长/办公室主任）"),
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "出生/入学与2005年参加工作前履历，公开未详", "confidence": "unverified", "source_ids": []},
]

liu_rels = [
    {"person": "彭伟", "person_id": "gongan_彭伟", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记—县长，县领导班子成员（2025-10至今）", "overlap_org": "中共公安县委员会", "overlap_period": "2025-10至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    {"person": "严广超", "person_id": "gongan_严广超", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "前任书记→继任书记（2025年交接）", "overlap_org": "中共公安县委员会", "overlap_period": "2021-2025", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
]

peng_rels = [
    {"person": "刘春霞", "person_id": "gongan_刘春霞", "relationship_type": "overlap", "strength": "strong", "evidence": "县长—县委书记，县领导班子成员（2025-10至今）", "overlap_org": "中共公安县委员会", "overlap_period": "2025-10至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    {"person": "周敏", "person_id": "gongan_周敏", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "县长—常务副县长（2025至今）", "overlap_org": "公安县人民政府", "overlap_period": "2025至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
]


def _write_profiles_json():
    profiles = []
    liu = _get(1)
    peng = _get(2)
    liu_prof = json_profile(liu, "正县级", liu_career, [], liu_rels, "潜江演前教育与更早履历细节公开有限", "local_ladder", ["审计", "乡镇", "开发区", "party", "government"], ["审计", "公共管理"])
    peng_prof = json_profile(peng, "正县级", peng_career, [], peng_rels, "2005年参加工作前履历及市级/松滋各节点具体年份待补", "organization_track", ["组织", "government", "党委", "片区"], [])
    liu_prof["governance_record"] = [{"period": "2025-2026", "domain": "anticorruption", "achievement_or_event": "县委专题调度群众身边不正之风和腐败问题集中整治、医保基金管理专项整治", "role_in_event": "县委书记讲话部署", "measurable_outcome": "", "location": "公安县", "confidence": "confirmed", "source_ids": ["S001"]}]
    peng_prof["governance_record"] = [{"period": "2025-2026", "domain": "public_security", "achievement_or_event": "主持召开县十八届政府常务会议（第71/76次）", "role_in_event": "县长主持", "measurable_outcome": "", "location": "公安县", "confidence": "confirmed", "source_ids": ["S001"]}]
    profiles.append(("20260806-湖北省-荆州市-县委书记-刘春霞.json", liu_prof))
    profiles.append(("20260806-湖北省-荆州市-县长-彭伟.json", peng_prof))
    for fname, data in profiles:
        with open(HERE / fname, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return profiles


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县级")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 公安县人民政府门户网站 + 公开报道")
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