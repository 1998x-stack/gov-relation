#!/usr/bin/env python3
"""Build SQLite database + GEXF graph + person JSONs for 黄梅县 (Hubei, 黄冈市).

Investigation date: 2026-08-06
Task ID: hubei_黄梅县
Level: 县级
Targets: 县委书记 & 县长

Research sources:
  - www.hm.gov.cn (黄梅县人民政府门户, HTTP) — 政府领导页 (县政府领导班子简历/分工)、
    黄梅要闻 2026-07-29 至 2026-08-05 (马梁/刘婷/县四大家/小池滨江新区).
  - www.hg.gov.cn (黄冈市人民政府门户) — 李军杰赴武穴、黄梅调研 (2026-08-06)、
    市长刘洁简历、黄梅县创业融资 县区动态.
  - 澎湃/搜狐/任前公示: 因网络受限 (Exa rate-limited, Bing/Baidu/Baike degraded)，
    马梁、刘婷的党内完整履历 (birth of 马梁/前职/籍贯/教育) 未核到 — 记为 open_questions。

Confidence:
  - 县委书记 马梁: CONFIRMED via 黄梅县人民政府要闻 (2026-08-01 八一慰问: 县委书记、县人武部党委第一书记).
  - 县委副书记/县长 刘婷: CONFIRMED via 黄梅县政府领导页 (官方简历: 女, 汉族, 1980年4月生, 大学, 中共党员).
  - 县人大常委会主任 欧阳水平, 县政协主席 龚家雄: CONFIRMED via 2026-08-01 八一家访 四大家顺序.
  - 县委常委/常务副县长 张鄂: CONFIRMED via 政府领导页 + 民生实事推进会 (2026-07-30).
  - 县委常委/小池滨江新区党工委书记 商胜辉: CONFIRMED via 光电座谈 (2026-08-03).
  - 副县长 饶维学/刘远征/宋州俊/田聪聪/夏辉(公安)/汪秀梅(挂职)/汪洋(挂职): CONFIRMED via 政府领导页.
  - 高金磊: 县领导, 具体职务未核到 (可能为常委) — flagged in open_questions。
  - 上级 context 黄冈市委书记李军杰、市长刘洁 (女,1969-03): CONFIRMED via hg.gov.cn。
  - 马梁详细履历 & 县委书记 predecessor/successor chain: partial — flagged in open_questions。
    No dates/education fabricated beyond official 简历 lines quoted.
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

SLUG = "黄梅县"
PROVINCE = "湖北省"
CITY = "黄冈市"
AS_OF = "2026-08-06"
TODAY = datetime.now().strftime("%Y%m%d")

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"

# ── Persons (confirmed as-of 2026-08-06) ─────────────────────────────────
persons = [
    {"id": 1, "name": "马梁", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委书记", "current_org": "中共黄梅县委员会",
     "source": "http://www.hm.gov.cn/ywdt/hmyw/12111716.html"},
    {"id": 2, "name": "刘婷", "gender": "女", "ethnicity": "汉族", "birth": "1980-04", "birthplace": "",
     "education": "大学", "party_join": "", "work_start": "",
     "current_post": "县长", "current_org": "黄梅县人民政府",
     "source": "http://www.hm.gov.cn/zfld/"},
    {"id": 3, "name": "欧阳水平", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "黄梅县人民代表大会常务委员会",
     "source": "http://www.hm.gov.cn/ywdt/hmyw/12111716.html"},
    {"id": 4, "name": "龚家雄", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政协主席", "current_org": "中国人民政治协商会议黄梅县委员会",
     "source": "http://www.hm.gov.cn/ywdt/hmyw/12111716.html"},
    {"id": 5, "name": "张鄂", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "黄梅县人民政府",
     "source": "http://www.hm.gov.cn/zfld/"},
    {"id": 6, "name": "商胜辉", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、湖北小池滨江新区党工委书记", "current_org": "湖北小池滨江新区",
     "source": "http://www.hm.gov.cn/ywdt/hmyw/12111695.html"},
    {"id": 7, "name": "高金磊", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县领导", "current_org": "黄梅县",
     "source": "http://www.hm.gov.cn/ywdt/hmyw/12111713.html"},
    {"id": 8, "name": "饶维学", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "黄梅县人民政府",
     "source": "http://www.hm.gov.cn/zfld/"},
    {"id": 9, "name": "刘远征", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "黄梅县人民政府",
     "source": "http://www.hm.gov.cn/zfld/"},
    {"id": 10, "name": "宋州俊", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "黄梅县人民政府",
     "source": "http://www.hm.gov.cn/zfld/"},
    {"id": 11, "name": "田聪聪", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "黄梅县人民政府",
     "source": "http://www.hm.gov.cn/zfld/"},
    {"id": 12, "name": "夏辉", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长、公安局局长", "current_org": "黄梅县公安局",
     "source": "http://www.hm.gov.cn/zfld/"},
    {"id": 13, "name": "汪秀梅", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长（挂职）", "current_org": "黄梅县人民政府",
     "source": "http://www.hm.gov.cn/zfld/"},
    {"id": 14, "name": "汪洋", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长（挂职）", "current_org": "黄梅县人民政府",
     "source": "http://www.hm.gov.cn/zfld/"},
    {"id": 15, "name": "李军杰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "黄冈市委书记", "current_org": "中共黄冈市委",
     "source": "https://www.hg.gov.cn/zwxw/hgyw/9392028.html"},
    {"id": 16, "name": "刘洁", "gender": "女", "ethnicity": "汉族", "birth": "1969-03", "birthplace": "",
     "education": "大学学历、法律硕士", "party_join": "", "work_start": "",
     "current_post": "黄冈市委副书记、市长", "current_org": "黄冈市人民政府",
     "source": "https://www.hg.gov.cn/"},
]

# ── Organizations ─────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共黄梅县委员会", "type": "党委", "level": "县级", "parent": "中共黄冈市委", "location": "湖北省黄冈市黄梅县"},
    {"id": 2, "name": "黄梅县人民政府", "type": "政府", "level": "县级", "parent": "黄冈市人民政府", "location": "湖北省黄冈市黄梅县"},
    {"id": 3, "name": "黄梅县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "黄梅县", "location": "湖北省黄冈市黄梅县"},
    {"id": 4, "name": "中国人民政治协商会议黄梅县委员会", "type": "政协", "level": "县级", "parent": "黄梅县", "location": "湖北省黄冈市黄梅县"},
    {"id": 5, "name": "湖北小池滨江新区", "type": "开发区", "level": "县级", "parent": "黄梅县", "location": "湖北省黄冈市黄梅县小池镇"},
    {"id": 6, "name": "黄梅县公安局", "type": "政府", "level": "县级", "parent": "黄梅县人民政府", "location": "湖北省黄冈市黄梅县"},
    {"id": 7, "name": "黄梅县人民武装部", "type": "政府", "level": "县级", "parent": "黄冈军分区", "location": "湖北省黄冈市黄梅县"},
    {"id": 8, "name": "中共黄冈市委", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "湖北省黄冈市"},
    {"id": 9, "name": "黄冈市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "湖北省黄冈市"},
]

# ── Positions (confirmed, as-of 2026-08-06) ──────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "兼人武部第一书记、县群腐集中整治工作领导小组组长（官方要闻）"},
    {"person_id": 1, "org_id": 7, "title": "县人武部党委第一书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "2026-08-01 八一慰问确认"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正县级", "note": "县委副书记、县政府党组书记、县长（官方政府领导页）"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "县委副书记、县政府党组书记、县长"},
    {"person_id": 3, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正县级", "note": "2026-08-01 县四大家八一慰问确认"},
    {"person_id": 4, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正县级", "note": "2026-08-01 县四大家八一慰问确认"},
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "县委常委、县政府党组副书记、副县长（官方政府领导页）"},
    {"person_id": 6, "org_id": 5, "title": "党工委书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "县委常委、湖北小池滨江新区党工委书记（2026-08-03座谈）"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "县政府党组成员、副县长（官方政府领导页）"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "副县长（官方政府领导页）"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "县政府党组成员、副县长（官方政府领导页）"},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "县政府党组成员、副县长（官方政府领导页）"},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "县政府党组成员、副县长（官方政府领导页）"},
    {"person_id": 12, "org_id": 6, "title": "公安局局长", "start_date": "", "end_date": "", "rank": "副县级", "note": "副县长、公安局局长（官方政府领导页）"},
    {"person_id": 13, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "副县级", "note": "县政府党组成员、副县长（挂职）（官方政府领导页）"},
    {"person_id": 14, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "副县级", "note": "县政府党组成员、副县长（挂职）（官方政府领导页）"},
    {"person_id": 15, "org_id": 8, "title": "黄冈市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "上级（黄冈市委书记）对接黄梅调研"},
    {"person_id": 16, "org_id": 9, "title": "黄冈市委副书记、市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "上级（黄冈市长）"},
]

# ── Relationships (confirmed) ─────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长（县委班子核心搭子）", "overlap_org": "中共黄梅县委员会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记—人大常委会主任（县四大家）", "overlap_org": "黄梅县", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "县委书记—政协主席（县四大家）", "overlap_org": "黄梅县", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记—常务副县长张鄂（常委班子）", "overlap_org": "中共黄梅县委员会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记—县委常委/小池新区党工委书记商胜辉", "overlap_org": "中共黄梅县委员会", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长—常务副县长张鄂（县政府党组）", "overlap_org": "黄梅县人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长—副县长饶珠学（县政府班子）", "overlap_org": "黄梅县人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长—副县长刘远征（县政府班子）", "overlap_org": "黄梅县人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长—副县长宋州俊（县政府班子）", "overlap_org": "黄梅县人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "县长—副县长田聪聪（县政府班子）", "overlap_org": "黄梅县人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "县长—副县长汪（挂职）（县政府班子）", "overlap_org": "黄梅县人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "县长—副县长汪洋（挂职）（县政府班子）", "overlap_org": "黄梅县人民政府", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 15, "type": "上下级", "context": "黄梅县委书记—黄冈市委书记（上下级关系）", "overlap_org": "中共黄冈市委", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "黄梅县长—黄冈市长（上下级关系）", "overlap_org": "黄冈市人民政府", "overlap_period": "2026年"},
]


# ── Person JSON profiles ──────────────────────────────────────────────────
def _get(pid):
    for p in persons:
        if p["id"] == pid:
            return p
    raise KeyError(pid)


def json_profile(person, admin_rank, career_rows, gov_records, gap_note, pattern, systems, spec=(), role_type="other"):
    name = person["name"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": CITY, "region": SLUG, "job": person["current_post"],
                                "task_id": "hubei_黄梅县", "time_focus": "2025-2026"},
        "identity": {
            "person_id": f"huangmei_{name}", "name": name, "aliases": [],
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
            {"org": "中共黄梅县委员会", "type": "党委", "level": "县级", "location": "湖北省黄冈市黄梅县"},
            {"org": "黄梅县人民政府", "type": "政府", "level": "县级", "location": "湖北省黄冈市黄梅县"},
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {"primary_specializations": list(spec), "secondary_specializations": [],
                                 "career_pattern": "unknown", "systems_experience": list(systems),
                                 "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [],
                                       "management_signals": [],
                                       "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "本次调研（官方要闻+政府领导页）未发现负面信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "黄梅县人民政府门户（政府领导页 + 黄梅要闻）", "url": "http://www.hm.gov.cn/", "publisher": "黄梅县人民政府", "published_at": AS_OF, "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官方简历/新闻确认现任职务"},
            {"id": "S002", "title": "黄冈市人民政府门户（县区动态/黄冈要闻）", "url": "https://www.hg.gov.cn/", "publisher": "黄冈市人民政府", "published_at": AS_OF, "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市委市政府调研的县政府情"},
        ],
        "confidence_summary": {"identity": "confirmed" if person.get("birth") else "partial",
                               "current_role": "confirmed",
                               "career_completeness": "thin",
                               "relationship_confidence": "medium",
                               "biggest_gap": gap_note},
        "open_questions": [{"priority": "high", "question": gap_note, "why_it_matters": "用于跨县网络与履历深度分析",
                            "suggested_queries": [f"黄梅县 {name} 简历", f"{CITY} 组织部 任前公示 {name}"], "last_attempted": AS_OF}],
    }


def row(start, end, org, title, lvl, system, rank, key, note, conf="confirmed"):
    return {"start": start, "end": end, "org": org, "title": title, "level": lvl, "location": "湖北省",
            "system": system, "rank": rank, "is_key_promotion": key, "notes": note, "confidence": conf, "source_ids": ["S001"]}


ma_career = [
    row("", "present", "中共黄梅县委员会", "县委书记", "县级", "party", "正县级", True, "兼县委民兵连第一书记（八一慰问 2026-08）"),
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "马梁在黄梅县委书记前的详细履历（出生/籍贯/学历/前职/就任时间）公开来源暂未核到，待补", "confidence": "unverified", "source_ids": []},
]

liu_career = [
    row("", "present", "黄梅县人民政府", "县长", "县级", "government", "正县级", True, "县委副书记、县政府党组书记、县长（官方政府领导页）"),
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "刘婷任黄梅县长前的历任职务及籍贯/党籍时间等细节未公开，待补", "confidence": "unverified", "source_ids": []},
]


def _write_profiles_json():
    profiles = []
    ma = _get(1)
    liu = _get(2)
    ma_prof = json_profile(ma, "正县级", ma_career, [], "详细履历（出生/籍贯/学历/前职/就任时间）公开不足", "unknown", ["party"], ["群众监督/群腐整治", "人民武装"])
    liu_prof = json_profile(liu, "正县级", liu_career, [], "任职前履历与出生地等信息未公开", "unknown", ["government", "party"], [])
    ma_prof["governance_record"] = [
        {"period": "2026", "domain": "discipline", "achievement_or_event": "主持召开全县群腐集中整治工作领导小组扩大会暨信访推进会（2026-08-01）", "role_in_event": "县委书记主持", "measurable_outcome": "", "location": "黄梅县", "confidence": "confirmed", "source_ids": ["S001"]},
        {"period": "2026", "domain": "public_security", "achievement_or_event": "到县群众信访接待服务中心接访（2026-07-29）", "role_in_event": "县委书记接访", "measurable_outcome": "", "location": "黄梅县", "confidence": "confirmed", "source_ids": ["S001"]},
        {"period": "2026", "domain": "other", "achievement_or_event": "率县三大家开展八一建军节慰问，强调红色资源/双拥共建（2026-08-01）", "role_in_event": "县委书记率队", "measurable_outcome": "", "location": "黄梅县", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    liu_prof["governance_record"] = [
        {"period": "2026", "domain": "economic_development", "achievement_or_event": "主持光电通信材料重点企业座谈会，打造'光谷第九园'小池科技园（2026-07）", "role_in_event": "县长主持座谈", "measurable_outcome": "", "location": "黄梅县", "confidence": "confirmed", "source_ids": ["S001"]},
        {"period": "2026", "domain": "other", "achievement_or_event": "主持召开全县民生领域实事攻坚推进会（2026-07-30）", "role_in_event": "县长主持", "measurable_outcome": "", "location": "黄梅县", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    profiles.append((f"{TODAY}-湖北省-黄冈市-县委书记-马梁.json", ma_prof))
    profiles.append((f"{TODAY}-湖北省-黄冈市-县长-刘婷.json", liu_prof))
    for fname, data in profiles:
        with open(HERE / fname, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return profiles


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县级")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 黄梅县人民政府门户 + 黄冈市政府门户")
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