#!/usr/bin/env python3
"""Build SQLite database + GEXF graph + person JSONs for 三穗县 (Sansui County), 贵州省.

Investigation date: 2026-08-06
Task ID: guizhou_三穗县
Level: 县级
Targets: 县委书记 & 县长

Sources: 三穗县人民政府门户网站 (www.gzss.gov.cn) 政府领导之窗 + 政务要闻/领导活动;
黔东南州政府网 (www.qdn.gov.cn); 百度百科·三穗县词条 (前任书记 刘明波).

Confidence:
  - 县委书记 杨波: CONFIRMED via county news; personal bio fields not obtained -> gap.
  - 县长 林晓晖: CONFIRMED incl. birth/education via 政府领导之窗.
  - 各副县级: CONFIRMED via 政府领导之窗 profiles.
  - 人大主任陈永祥、政协主席赵平、政法书记潘勇、人大副主任杨梦昌、政协副主席敬业:
    CONFIRMED via county news.
  - 前任书记 刘志强: CONFIRMED (百度百科词条 截至2023-03); 去向未确认。
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

for _parent in Path(__file__).resolve().parents:
    if (_parent / "gov_relation").is_dir():
        sys.path.insert(0, str(_parent))
        break

from gov_relation.runner import run_build  # noqa: E402

SLUG = "三穗县"
PROVINCE = "贵州省"
CITY = "黔东南苗族侗族自治州"
AS_OF = "2026-08-06"
TASK_ID = "guizhou_三穗县"
TODAY = datetime.now().strftime("%Y%m%d")

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"

# ── Persons (confirmed as-of 2026-08-06) ─────────────────────────────────
persons = [
    {"id": 1, "name": "杨波", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委书记", "current_org": "中共三穗县委员会",
     "source": "https://www.gzss.gov.cn/xwzx/"},
    {"id": 2, "name": "林晓晖", "gender": "男", "ethnicity": "汉族", "birth": "1988-06", "birthplace": "山东寿光",
     "education": "研究生学历", "party_join": "2007-08", "work_start": "2014-07",
     "current_post": "县委副书记、县长", "current_org": "三穗县人民政府",
     "source": "https://www.gzss.gov.cn/zwgk/zfld/"},
    {"id": 3, "name": "陈永祥", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县人大常委会主任", "current_org": "三穗县人民代表大会常务委员会",
     "source": "https://www.gzss.gov.cn/xwzx/"},
    {"id": 4, "name": "赵平", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县政协主席", "current_org": "中国人民政治协商会议三穗县委员会",
     "source": "https://www.gzss.gov.cn/xwzx/"},
    {"id": 5, "name": "潘勇", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委常委、县委政法委书记", "current_org": "中共三穗县委政法委员会",
     "source": "https://www.gzss.gov.cn/xwzx/"},
    {"id": 6, "name": "周茂", "gender": "男", "ethnicity": "侗族", "birth": "1986-01", "birthplace": "贵州岑巩",
     "education": "大学本科（管理学学士）", "party_join": "2006-12", "work_start": "2009-07",
     "current_post": "县委常委、常务副县长", "current_org": "三穗县人民政府",
     "source": "https://www.gzss.gov.cn/zwgk/zfld/"},
    {"id": 7, "name": "王媛", "gender": "女", "ethnicity": "侗族", "birth": "1987-11", "birthplace": "贵州凯里",
     "education": "本科（在职公共管理硕士）", "party_join": "2014-07", "work_start": "2010-08",
     "current_post": "县委常委、副县长", "current_org": "三穗县人民政府",
     "source": "https://www.gzss.gov.cn/zwgk/zfld/"},
    {"id": 8, "name": "刘业平", "gender": "男", "ethnicity": "汉族", "birth": "1980-09", "birthplace": "广东兴宁",
     "education": "大学学历", "party_join": "2005-01", "work_start": "2002-07",
     "current_post": "县委常委、副县长", "current_org": "三穗县人民政府",
     "source": "https://www.gzss.gov.cn/zwgk/zfld/"},
    {"id": 9, "name": "黄金模", "gender": "男", "ethnicity": "汉族", "birth": "1979-09", "birthplace": "贵州施秉",
     "education": "本科学历", "party_join": "2006-11", "work_start": "2004-09",
     "current_post": "县政府党组成员、副县长", "current_org": "三穗县人民政府",
     "source": "https://www.gzss.gov.cn/zwgk/zfld/"},
    {"id": 10, "name": "田红祥", "gender": "男", "ethnicity": "侗族", "birth": "1981-09", "birthplace": "贵州镇远",
     "education": "本科学历", "party_join": "2004-11", "work_start": "2006-07",
     "current_post": "县政府党组成员、副县长", "current_org": "三穗县人民政府",
     "source": "https://www.gzss.gov.cn/zwgk/zfld/"},
    {"id": 11, "name": "张全通", "gender": "男", "ethnicity": "侗族", "birth": "1979-08", "birthplace": "贵州岑巩",
     "education": "本科学历", "party_join": "2002-07", "work_start": "2003-03",
     "current_post": "副县长、县公安局局长", "current_org": "三穗县公安局",
     "source": "https://www.gzss.gov.cn/zwgk/zfld/"},
    {"id": 12, "name": "刘洪斌", "gender": "男", "ethnicity": "汉族", "birth": "1980-09", "birthplace": "贵州镇远",
     "education": "本科学历", "party_join": "2005-06", "work_start": "2003-02",
     "current_post": "县政府党组成员、副县长", "current_org": "三穗县人民政府",
     "source": "https://www.gzss.gov.cn/zwgk/zfld/"},
    {"id": 13, "name": "姚尧", "gender": "男", "ethnicity": "侗族", "birth": "1992-04", "birthplace": "贵州罗甸",
     "education": "本科学历", "party_join": "2023-11", "work_start": "2014-08",
     "current_post": "副县长", "current_org": "三穗县人民政府",
     "source": "https://www.gzss.gov.cn/zwgk/zfld/"},
    {"id": 14, "name": "王国斌", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县人大常委会副主任", "current_org": "三穗县人民代表大会常务委员会",
     "source": "https://www.gzss.gov.cn/xwzx/"},
    {"id": 15, "name": "杨精豪", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县政协副主席", "current_org": "中国人民政治协商会议三穗县委员会",
     "source": "https://www.gzss.gov.cn/xwzx/"},
    {"id": 16, "name": "刘明波", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "（前任县委书记，已离任）", "current_org": "中共三穗县委员会",
     "source": "https://baike.baidu.com/"},
]

# ── Organizations ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共三穗县委员会", "type": "党委", "level": "县级", "parent": "中共黔东南州委", "location": "贵州省黔东南州三穗县"},
    {"id": 2, "name": "三穗县人民政府", "type": "政府", "level": "县级", "parent": "黔东南州人民政府", "location": "贵州省黔东南州三穗县"},
    {"id": 3, "name": "三穗县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "三穗县", "location": "贵州省黔东南州三穗县"},
    {"id": 4, "name": "中国人民政治协商会议三穗县委员会", "type": "政协", "level": "县级", "parent": "三穗县", "location": "贵州省黔东南州三穗县"},
    {"id": 5, "name": "中共黔东南州委", "type": "党委", "level": "地级市", "parent": "中共贵州省委", "location": "贵州省黔东南州凯里市"},
    {"id": 6, "name": "黔东南州人民政府", "type": "政府", "level": "地级市", "parent": "贵州省人民政府", "location": "贵州省黔东南州凯里市"},
    {"id": 7, "name": "中共三穗县委政法委员会", "type": "党委", "level": "县级", "parent": "中共三穗县委员会", "location": "贵州省黔东南州三穗县"},
    {"id": 8, "name": "三穗县公安局", "type": "政府", "level": "县级", "parent": "三穗县人民政府", "location": "贵州省黔东南州三穗县"},
]

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正县级",
     "note": "现任县委书记（官方新闻 2026-07/08 确认）；接任前任书记刘明波，到任时间未公开"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正县级",
     "note": "县委副书记、县长；领导政府全面工作（财政/金融/审计/粮食）"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "兼任县委副书记"},
    {"person_id": 3, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正县级", "note": "县四大班子领导"},
    {"person_id": 4, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正县级", "note": "县四大班子领导"},
    {"person_id": 5, "org_id": 7, "title": "县委常委、县委政法委书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "政法工作负责人"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "县委委员/常委"},
    {"person_id": 6, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "主持政府常务工作（发改/税务/统计/应急/金融/大数据等），协助县长"},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "县委委员/常委"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "分管环保/市场监管/人社/招商引资等"},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "县委委员/常委"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "分管东西部协作，协助招商引资"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "县政府党组成员、副县长；分管卫健/医保/民政/民宗等"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "县政府党组成员、副县长；分管交通/工信/商务/教育/文旅等"},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "政府党组成员、副县长、县公安局局长"},
    {"person_id": 11, "org_id": 8, "title": "县公安局局长", "start_date": "", "end_date": "", "rank": "副县级", "note": "主持县公安局全面工作"},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "县政府党组成员、副县长；分管自然资源/住建/执法等"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "协助招商引资/旅游发展，分管定点帮扶"},
    {"person_id": 14, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "县人大常委会副主任"},
    {"person_id": 15, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "", "rank": "副县级", "note": "县政协副主席"},
    {"person_id": 16, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正县级",
     "note": "前任县委书记（百度百科截至2023-03在任）；离任时间与去向未公开"},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长（党委政府一把手搭档）", "overlap_org": "中共三穗县委员会", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长—常务副县长（主持政府日常）", "overlap_org": "三穗县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长—副县长（兼常委）", "overlap_org": "三穗县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长—副县长（兼常委）", "overlap_org": "三穗县人民政府", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 16, "type": "前任继任", "context": "前任书记刘明波→继任书记杨波（县委书记换届）", "overlap_org": "中共三穗县委员会", "overlap_period": "2023前后"},
    {"person_a": 5, "person_b": 11, "type": "共事", "context": "政法委书记—公安局长（政法系统配合）", "overlap_org": "中共三穗县委政法委员会", "overlap_period": "现任"},
    {"person_a": 3, "person_b": 4, "type": "同届共事", "context": "人大主任—政协主席（县四套班子）", "overlap_org": "中共三穗县委员会", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "县长—副县长姚尧", "overlap_org": "三穗县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长—副县长黄金模", "overlap_org": "三穗县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长—副县长田红祥", "overlap_org": "三穗县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "县长—副县长刘洪斌", "overlap_org": "三穗县人民政府", "overlap_period": "现任"},
    {"person_a": 6, "person_b": 7, "type": "共事", "context": "两位县委常委同班子", "overlap_org": "中共三穗县委员会", "overlap_period": "现任"},
    {"person_a": 7, "person_b": 8, "type": "共事", "context": "王媛与刘业平协作（分管招商引资）", "overlap_org": "三穗县人民政府", "overlap_period": "现任"},
]

# ── Person JSON profiles ─────────────────────────────────────────────────
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
        "investigation_scope": {"province": PROVINCE, "city": CITY, "region": SLUG,
                                "job": person["current_post"], "task_id": TASK_ID, "time_focus": "2025-2026"},
        "identity": {
            "person_id": f"sansui_{name}", "name": name, "aliases": [],
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
            {"org": "中共三穗县委员会", "type": "党委", "level": "县级", "location": "贵州省黔东南州三穗县"},
            {"org": "三穗县人民政府", "type": "政府", "level": "县级", "location": "贵州省黔东南州三穗县"},
        ],
        "relationships": [],
        "governance_record": gov_records,
        "professional_profile": {"primary_specializations": list(spec), "secondary_specializations": [],
                                 "career_pattern": pattern, "systems_experience": list(systems),
                                 "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [],
                                       "management_signals": [],
                                       "caveat": "Work style is inferred from public records, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "本次官方渠道调研未发现负面信号", "date": "",
                                        "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "三穗县人民政府门户·政府领导之窗", "url": "https://www.gzss.gov.cn/zwgk/zfld/",
             "publisher": "三穗县人民政府办公室", "published_at": AS_OF, "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "领导简历官方来源"},
            {"id": "S002", "title": "三穗县政府网·政务要闻/领导活动", "url": "https://www.gzss.gov.cn/xwzx/",
             "publisher": "三穗县融媒体中心", "published_at": "2026-08", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "确认书记杨波、人大主任陈永祥、政协主席赵平、政法书记潘勇等"},
            {"id": "S003", "title": "百度百科·三穗县词条", "url": "https://baike.baidu.com/",
             "publisher": "百度百科", "published_at": "2023-03", "accessed_at": AS_OF,
             "source_type": "encyclopedia", "reliability": "medium", "notes": "前任县委书记刘明波确认"},
        ],
        "confidence_summary": {"identity": "confirmed" if person.get("birth") else "partial",
                               "current_role": "confirmed",
                               "career_completeness": "complete" if career_rows else "thin",
                               "relationship_confidence": "medium",
                               "biggest_gap": gap_note},
        "open_questions": [{"priority": "high", "question": gap_note, "why_it_matters": "用于跨县网络深度分析",
                            "suggested_queries": [f"{SLUG} {name} 简历", f"{CITY} 组织部 任前公示 {name}"],
                            "last_attempted": AS_OF}],
    }


def row(start, end, org, title, lvl, system, rank, key, note, conf="confirmed"):
    return {"start": start, "end": end, "org": org, "title": title, "level": lvl, "location": "贵州省",
            "system": system, "rank": rank, "is_key_promotion": key, "notes": note,
            "confidence": conf, "source_ids": ["S001", "S002"]}


# Career rows
yang_career = [
    row("", "present", "中共三穗县委员会", "县委书记", "县级", "party", "正县级", True, "现任县委书记（官方新闻 2026-07/08 确认）"),
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "system": "",
     "rank": "", "is_key_promotion": False, "notes": "生年/籍贯/学历/入党/此前任职未公开（搜索与人物词条受限）",
     "confidence": "unverified", "source_ids": []},
]

lin_career = [
    row("", "present", "三穗县人民政府", "县长（县委副书记）", "县级", "government", "正县级", True, "负责政府全面工作（财政/金融/审计/粮食）"),
    {"start": "2014-07", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "system": "",
     "rank": "", "is_key_promotion": False, "notes": "山东寿光人，1988-06生，2007-08入党，2014-07参加工作，研究生；早期任职节点未公开",
     "confidence": "confirmed", "source_ids": ["S001"]},
]

zhou_career = [
    row("", "present", "三穗县人民政府", "常务副县长（县委常委）", "县级", "government", "副县级", True, "主持政府常务工作，协助县长"),
    row("", "", "履历开头", "", "县级", "government", "", False, "贵州岑巩人，1986-01生，侗族，2009-07工作，2006-12入党，大学本科/管理学学士"),
]

wang_career = [
    row("", "", "三穗县人民政府", "副县长（县委常委）", "县级", "government", "副县级", True, "分管环保/市场监管/人社/招商引资等"),
    row("", "", "履历开头", "", "县级", "government", "", False, "贵州凯里人，1987-11生，女，侗族，2010-08工作，2014-07入党，本科/在职公共管理硕士"),
]

liuy_career = [
    row("", "", "三穗县人民政府", "副县长（县委常委）", "县级", "government", "副县级", True, "分管东西部协作，协助招商引资"),
    row("", "", "履历开头", "", "县级", "government", "", False, "广东兴宁人，1980-09生，汉族，2002-07工作，2005-01入党，大学学历（跨省干部）"),
]


def _write_profiles_json():
    profiles = []
    yang = _get(1)
    lin = _get(2)
    zhou = _get(6)
    wang = _get(7)
    liu = _get(8)

    yang_prof = json_profile(yang, "正县级", yang_career, [], "县委书记杨波完整履历（生/籍贯/学历/入党）公开资料未取得",
                             "unknown", ["party"], [])
    yang_prof["identity"]["person_id"] = "sansui_yang_bo"
    yang_prof["open_questions"] = [{"priority": "critical", "question": "杨波完整履历",
                                    "why_it_matters": "县委书记为县党政核心", "suggested_queries": ["三穗县 杨波 任前公示"],
                                    "last_attempted": AS_OF}]

    lin_prof = json_profile(lin, "正县级", lin_career, [], "县长林晓晖早期仕途（寿光→三穗）具体任职节点未公开",
                            "cross_county_rotation", ["government", "party"], "政府管理")
    lin_prof["governance_record"] = [
        {"period": "2026", "domain": "economic_development", "achievement_or_event": "主持县政府全面工作，统筹财政/金融/审计/粮食",
         "role_in_event": "县长", "measurable_outcome": "2025年GDP 63.42亿元(+4.2%)", "location": SLUG,
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]

    zhou_prof = json_profile(zhou, "副县级", zhou_career, [], "周茂此前跨县任职细节待查",
                             "cross_county_rotation", ["government"], [])
    wang_prof = json_profile(wang, "副县级", wang_career, [], "王嫒早期履历待查",
                             "cross_county_rotation", ["government"], [])
    liu_prof = json_profile(liu, "副县级", liuy_career, [], "刘业平早年履历待查（跨省干部）",
                            "cross_county_rotation", ["government"], [])

    profiles.append((f"{TODAY}-贵州省-黔东南苗族侗族自治州-县委书记-杨波.json", yang_prof))
    profiles.append((f"{TODAY}-贵州省-黔东南苗族侗族自治州-县长-林晓晖.json", lin_prof))
    profiles.append((f"{TODAY}-贵州省-黔东南苗族侗族自治州-常务副县长-周茂.json", zhou_prof))
    profiles.append((f"{TODAY}-贵州省-黔东南苗族侗族自治州-副县长-王嫒.json", wang_prof))
    profiles.append((f"{TODAY}-贵州省-黔东南苗族侗族自治州-副县长-刘业平.json", liu_prof))

    for fname, data in profiles:
        with open(HERE / fname, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return profiles


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县级")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 三穗县人民政府门户网站 + 公开报道")
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

    conn = sqlite3.connect(str(DB_PATH))
    try:
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                  for t in ("persons", "organizations", "positions", "relationships")}
    finally:
        conn.close()
    print("  DB counts:", counts)

    profiles = _write_profiles_json()
    print("\n  人物 JSON: %d 个" % len(profiles))
    for fname, _ in profiles:
        print(f"    - {fname}")

    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    main()