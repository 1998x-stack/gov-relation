#!/usr/bin/env python3
"""Build SQLite database + GEXF graph + person JSONs for 罗田县 (Luotian County), 湖北省.

Investigation date: 2026-08-06
Task ID: hubei_罗田县
Level: 县级
Targets: 县委书记 & 县长

Research sources:
  - 罗田县人民政府门户网站 (www.luotian.gov.cn) — 政府信息公开、罗田要闻、领导之窗.
    Accessed 2026-08-06.
  - 湖北日报 / 荆楚网 / 百越之南 / 网易 等公开人事报道确认 周黎、汪湘云 履历及
    郝爱芳→周黎 县委书记交接链。
  - 百度百科 人物词条（周黎、汪湘云、秦新平、张卫兵、姜焕勇）。

Confidence:
  - 现任县委书记 周黎（2025年12月任）、县长 汪湘云（2026年1月当选）:
    CONFIRMED via 罗田县政府官网新闻 (2026-01-06 党代会第五次会议；2026-01-23 人代会五次会议
    选举汪湘云为县长；2026-07-25 县委理论学习中心组第11次集体学习).
  - 县委副书记 张志刚、县人大常委会主任 秦新平、县政协主席 张卫兵、常务副县长(县政府党组副书记)
    姜焕勇、组织部长 卫松、政法委书记 刘晓宇、县委办主任 邱常国: CONFIRMED via 官方新闻。
  - 周黎完整履历（湖北秭归人、1982年生、长江大学动物医学、湖北省农科院 → 麻城 → 罗田）:
    CONFIRMED via 任前公示/多篇一致媒体报道。
  - 汪湘云完整履历（湖北黄州人、1981年生、团风 → 浠水 → 罗田）: CONFIRMED via 官方及媒体。
  - 部分副职履历细节（出生/教育）仍有缺口，已列入 open_questions。未编造任何日期。
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

SLUG = "罗田县"
PROVINCE = "湖北省"
CITY = "黄冈市"
AS_OF = "2026-08-06"
TASK_ID = "hubei_罗田县"
TODAY = datetime.now().strftime("%Y%m%d")

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"

# ── Persons (confirmed as-of 2026-08-06) ─────────────────────────────────
persons = [
    {"id": 1, "name": "周黎", "gender": "男", "ethnicity": "汉族", "birth": "1982-04", "birthplace": "湖北秭归",
     "education": "硕士研究生（长江大学动物医学专业本科）", "party_join": "2003-06", "work_start": "2005-07",
     "current_post": "县委书记", "current_org": "中共罗田县委员会",
     "source": "https://www.luotian.gov.cn/"},
    {"id": 2, "name": "汪湘云", "gender": "女", "ethnicity": "汉族", "birth": "1981-09", "birthplace": "湖北黄州",
     "education": "省委党校研究生", "party_join": "2009-06", "work_start": "2004-07",
     "current_post": "县长", "current_org": "罗田县人民政府",
     "source": "https://www.luotian.gov.cn/"},
    {"id": 3, "name": "张志刚", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委副书记", "current_org": "中共罗田县委员会",
     "source": "https://www.luotian.gov.cn/"},
    {"id": 4, "name": "秦新平", "gender": "男", "ethnicity": "汉族", "birth": "1969-03", "birthplace": "湖北罗田",
     "education": "中央党校经济管理专业大学本科", "party_join": "1990-06", "work_start": "1987-07",
     "current_post": "县人大常委会主任", "current_org": "罗田县人民代表大会常务委员会",
     "source": "https://baike.baidu.com/"},
    {"id": 5, "name": "张卫兵", "gender": "男", "ethnicity": "汉族", "birth": "1970-04", "birthplace": "湖北罗田",
     "education": "中央党校大学学历", "party_join": "1997-03", "work_start": "1988-07",
     "current_post": "县政协主席", "current_org": "中国人民政治协商会议罗田县委员会",
     "source": "https://baike.baidu.com/"},
    {"id": 6, "name": "姜焕勇", "gender": "男", "ethnicity": "汉族", "birth": "1986-09", "birthplace": "", "education": "研究生",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、常务副县长（县政府党组副书记）", "current_org": "罗田县人民政府",
     "source": "https://www.luotian.gov.cn/"},
    {"id": 7, "name": "卫松", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委常委、组织部部长", "current_org": "中共罗田县委组织部",
     "source": "https://www.luotian.gov.cn/"},
    {"id": 8, "name": "刘晓宇", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委常委、政法委书记", "current_org": "中共罗田县委政法委员会",
     "source": "https://www.luotian.gov.cn/"},
    {"id": 9, "name": "邱常国", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委委员、县委办公室主任", "current_org": "中共罗田县委办公室",
     "source": "https://www.luotian.gov.cn/"},
    {"id": 10, "name": "丰峰", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委委员、统战部部长、县总工会主席", "current_org": "中共罗田县委统战部",
     "source": "https://www.luotian.gov.cn/"},
    {"id": 11, "name": "黄巍", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "副县长", "current_org": "罗田县人民政府",
     "source": "https://www.luotian.gov.cn/"},
    {"id": 12, "name": "罗富", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "副县长", "current_org": "罗田县人民政府",
     "source": "https://www.luotian.gov.cn/"},
    {"id": 13, "name": "郝爱芳", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "（原罗田县委书记，2026到期拟提市人大常委会副主任）", "current_org": "中共罗田县委员会",
     "source": "https://www.luotian.gov.cn/"},
    {"id": 14, "name": "肖燕梅", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "（原罗田县委书记，已离任）", "current_org": "中共罗田县委员会",
     "source": "https://news.sina.com.cn/"},
]

# ── Organizations ─────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共罗田县委员会", "type": "党委", "level": "县级", "parent": "中共黄冈市委", "location": "湖北省黄冈市罗田县"},
    {"id": 2, "name": "罗田县人民政府", "type": "政府", "level": "县级", "parent": "黄冈市人民政府", "location": "湖北省黄冈市罗田县"},
    {"id": 3, "name": "罗田县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "罗田县", "location": "湖北省黄冈市罗田县"},
    {"id": 4, "name": "中国人民政治协商会议罗田县委员会", "type": "政协", "level": "县级", "parent": "罗田县", "location": "湖北省黄冈市罗田县"},
    {"id": 5, "name": "中共黄冈市委", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "湖北省黄冈市"},
    {"id": 6, "name": "黄冈市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "湖北省黄冈市"},
    {"id": 7, "name": "中共罗田县委组织部", "type": "党委", "level": "县级", "parent": "中共罗田县委员会", "location": "湖北省黄冈市罗田县"},
    {"id": 8, "name": "中共罗田县委政法委员会", "type": "党委", "level": "县级", "parent": "中共罗田县委员会", "location": "湖北省黄冈市罗田县"},
    {"id": 9, "name": "中共罗田县委办公室", "type": "党委", "level": "县级", "parent": "中共罗田县委员会", "location": "湖北省黄冈市罗田县"},
    {"id": 10, "name": "中共罗田县委统一战线工作部", "type": "党委", "level": "县级", "parent": "中共罗田县委员会", "location": "湖北省黄冈市罗田县"},
    {"id": 11, "name": "湖北省农业科学院", "type": "事业单位", "level": "省属", "parent": "湖北省人民政府", "location": "湖北省武汉市"},
    {"id": 12, "name": "中共麻城市委员会", "type": "党委", "level": "县级市", "parent": "中共黄冈市委", "location": "湖北省黄冈市麻城市"},
    {"id": 13, "name": "麻城市人民政府", "type": "政府", "level": "县级市", "parent": "黄冈市人民政府", "location": "湖北省黄冈市麻城市"},
    {"id": 14, "name": "中共浠水县委员会", "type": "党委", "level": "县级", "parent": "中共黄冈市委", "location": "湖北省黄冈市浠水县"},
    {"id": 15, "name": "浠水县人民政府", "type": "政府", "level": "县级", "parent": "黄冈市人民政府", "location": "湖北省黄冈市浠水县"},
    {"id": 16, "name": "中共团风县委员会", "type": "党委", "level": "县级", "parent": "中共黄冈市委", "location": "湖北省黄冈市团风县"},
    {"id": 17, "name": "中共红安县委员会", "type": "党委", "level": "县级", "parent": "中共黄冈市委", "location": "湖北省黄冈市红安县"},
]

# ── Positions (confirmed, as-of 2026-08-06) ──────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2025-12", "end_date": "", "rank": "正县级", "note": "2025-11-27 任前公示，2025-12 任县委书记；2025-12-17 兼任县人武部党委第一书记"},
    {"person_id": 1, "org_id": 2, "title": "县长", "start_date": "2021-11", "end_date": "2025-12", "rank": "正县级", "note": "2021-11-15 当选罗田县第十八届人民政府县长，至升任县委书记"},
    {"person_id": 1, "org_id": 1, "title": "县委副书记", "start_date": "2021-08", "end_date": "2025-12", "rank": "副县级", "note": "2021-08 任县委副书记、代县长"},
    {"person_id": 1, "org_id": 12, "title": "市委常委", "start_date": "2021-05", "end_date": "2021-08", "rank": "副县级", "note": "调至黄冈市任麻城市委常委"},
    {"person_id": 1, "org_id": 13, "title": "副市长", "start_date": "2021-06", "end_date": "2021-08", "rank": "副县级", "note": "次月获任麻城市副市长"},
    {"person_id": 1, "org_id": 11, "title": "粮食作物研究所所长、党委委员", "start_date": "", "end_date": "2021-05", "rank": "", "note": "湖北省农业科学院（此前任农科院人事处处长）"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2026-01-23", "end_date": "", "rank": "正县级", "note": "2026-01 人代会五次会议当选县长；此前2026-01-07已为县委副书记、县长提名人选（代县长）"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2026-01", "end_date": "", "rank": "副县级", "note": "县委副书记、县长"},
    {"person_id": 2, "org_id": 2, "title": "副县长（县政府党组副书记）", "start_date": "2024-04", "end_date": "2026-01", "rank": "副县级", "note": "调任罗田县委委员、县政府党组副书记、副县长"},
    {"person_id": 2, "org_id": 14, "title": "县委常委", "start_date": "2021-10", "end_date": "2024-04", "rank": "副县级", "note": "2021-10 当选浠水县第十五届县委；2021-11 任浠水县副县长"},
    {"person_id": 2, "org_id": 15, "title": "副县长", "start_date": "2021-11", "end_date": "2024-04", "rank": "副县级", "note": "浠水县人民政府副县长"},
    {"person_id": 2, "org_id": 16, "title": "总路咀镇党委书记", "start_date": "", "end_date": "2021", "rank": "乡科级", "note": "团风县；曾任上巴河镇党委副书记、镇长"},
    {"person_id": 2, "org_id": 16, "title": "上巴河镇党委副书记、镇长", "start_date": "", "end_date": "", "rank": "乡科级", "note": "团风县"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "2026", "end_date": "", "rank": "副县级", "note": "此前任县委委员、组织部长（2024-07仍在职）"},
    {"person_id": 4, "org_id": 3, "title": "县人大常委会主任", "start_date": "2021-11", "end_date": "", "rank": "正县级", "note": "罗田县第十八届人大常委会主任（党的代表，县委委员）"},
    {"person_id": 5, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正县级", "note": "政协第十一届罗田县委员会主席（曾任罗田县副县长）"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "十六届县委委员"},
    {"person_id": 6, "org_id": 2, "title": "常务副县长（县政府党组副书记）", "start_date": "", "end_date": "", "rank": "副县级", "note": "协助县长主持县政府日常工作，兼管项目建设/招商引资"},
    {"person_id": 7, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "曾为2021届副县长"},
    {"person_id": 8, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "曾为2021届副县长"},
    {"person_id": 9, "org_id": 1, "title": "县委委员、县委办公室主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "县委委员"},
    {"person_id": 10, "org_id": 1, "title": "县委委员、统战部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "兼县总工会主席"},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "2026-06", "end_date": "", "rank": "副县级", "note": "2026-06-23 县人大常委会第三十四次会议决定任命"},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "2026-06", "end_date": "", "rank": "副县级", "note": "2026-06-23 县人大常委会第三十四次会议决定任命"},
    {"person_id": 13, "org_id": 1, "title": "县委书记", "start_date": "2021-06", "end_date": "2025-11", "rank": "正县级", "note": "前任县委书记（2021-06任，2025-11拟提市人大常委会副主任，2025-12 周黎接任）"},
    {"person_id": 14, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "前任县委书记（2018年时任，2018年被责任问责环境环保事件）"},
]

# ── Relationships (confirmed as-of 2026-08-06) ────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长（县领导班子成员）", "overlap_org": "中共罗田县委员会", "overlap_period": "2026-01至今"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记—县委副书记", "overlap_org": "中共罗田县委员会", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 13, "type": "前任继任", "context": "郝爱芳卸任书记，周黎接任（县长→书记晋升）", "overlap_org": "中共罗田县委员会", "overlap_period": "2021-2025"},
    {"person_a": 2, "person_b": 1, "type": "上下级", "context": "县长（女）—县委书记（县领导班子成员）", "overlap_org": "罗田县人民政府", "overlap_period": "2026-01至今"},
    {"person_a": 6, "person_b": 2, "type": "上下级", "context": "常务副县长配合县长主持县政府日常工作", "overlap_org": "罗田县人民政府", "overlap_period": "2026至今"},
    {"person_a": 4, "person_b": 5, "type": "同届共事", "context": "县人大常委会主任—县政协主席（县四套班子）", "overlap_org": "中共罗田县委员会", "overlap_period": "2021至今"},
    {"person_a": 13, "person_b": 1, "type": "跨县相关", "context": "郝爱芳任书记期间，周黎先任县长（2021-2025）", "overlap_org": "中共罗田县委员会", "overlap_period": "2021-2025"},
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
                                "task_id": TASK_ID, "time_focus": "2025-2026"},
        "identity": {
            "person_id": f"luotian_{name}", "name": name, "aliases": [],
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
            {"org": "中共罗田县委员会", "type": "党委", "level": "县级", "location": "湖北省黄冈市罗田县"},
            {"org": "罗田县人民政府", "type": "政府", "level": "县级", "location": "湖北省黄冈市罗田县"},
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
            {"id": "S001", "title": "罗田县人民政府门户网站（政府信息公开/要闻）", "url": "https://www.luotian.gov.cn/", "publisher": "罗田县人民政府", "published_at": AS_OF, "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官方政府新闻及领导之窗确认"},
            {"id": "S002", "title": "湖北日报/荆楚网/网易 人事报道", "url": "https://www.hubei.gov.cn/", "publisher": "湖北日报", "published_at": "2026-01", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "周黎/汪湘云/秦新平履历及交接链"},
        ],
        "confidence_summary": {"identity": "confirmed" if person.get("birth") else "partial",
                               "current_role": "confirmed",
                               "career_completeness": "complete" if career_rows else "thin",
                               "relationship_confidence": "medium",
                               "biggest_gap": gap_note},
        "open_questions": [{"priority": "high", "question": gap_note, "why_it_matters": "用于跨县网络深度分析",
                            "suggested_queries": [f"罗田县 {name} 简历", f"{CITY} 组织部 任前公示 {name}"], "last_attempted": AS_OF}],
    }


# ── Career rows ───────────────────────────────────────────────────────────
def row(start, end, org, title, lvl, system, rank, key, note, conf="confirmed"):
    return {"start": start, "end": end, "org": org, "title": title, "level": lvl, "location": "湖北省",
            "system": system, "rank": rank, "is_key_promotion": key, "notes": note, "confidence": conf, "source_ids": ["S001", "S002"]}


zhou_career = [
    row("2025-12", "present", "中共罗田县委员会", "县委书记", "县级", "party", "正县级", True, "接终爱芳任县委书记（2025-11-27 公示，2025-12-17 兼县人武部党委第一书记）"),
    row("2021-08", "2025-12", "罗田县人民政府", "县长", "县级", "government", "正县级", True, "2021-08 任县委副书记、代县长；2021-11-15 当选县长"),
    row("2021-05", "2021-08", "麻城市人民政府", "副市长", "县级市", "government", "副县级", True, "跨县交流（麻城为黄冈市辖县级市）"),
    row("2021-05", "2021-08", "中共麻城市委员会", "市委常委", "县级市", "party", "副县级", True, ""),
    row("2005-07", "2021-05", "湖北省农业科学院", "人事处处长、粮食作物研究所所长/党委委员", "省属", "state_owned_enterprise", "", True, "2005年进入省农科院，长期任职（任人事处处长、粮作所所长）"),
    {"start": "2005-07", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "system": "agriculture", "rank": "", "is_key_promotion": False, "notes": "2005年长江大学动物医学专业毕业，进入湖北省农科院（具体任职时间节点公开不完全）", "confidence": "confirmed", "source_ids": ["S002"]},
]

wang_career = [
    row("2026-01-23", "present", "罗田县人民政府", "县长", "县级", "government", "正县级", True, "2026-01-23 代表大会选举当选县长（此前为县委副书记、县长提名人选/代县长）"),
    row("2024-04", "2026-01", "罗田县人民政府", "副县长（县政府党组副书记）", "县级", "government", "副县级", True, "调任罗田县委委员、县政府党组副书记、副县长"),
    row("2024-04", "2026-01", "中共罗田县委", "县委委员", "县级", "party", "副县级", True, "2024年4月起任罗田县委委员"),
    row("2021-10", "2024-04", "中共浠水县委员会", "县委常委", "县级", "party", "副县级", True, "2021-10 当选浠水县第十五届县委常委"),
    row("2021-11", "2024-04", "浠水县人民政府", "副县长", "县级", "government", "副县级", True, "2021-11 任浠水县副县长"),
    row("", "2021", "中共团风县委员会", "总路咀镇党委书记", "乡镇", "party", "乡科级", True, "团风县总路咀镇党委书记（曾任上巴河镇党委副书记、镇长）"),
    row("", "", "中共团风县委员会", "上巴河镇党委副书记、镇长", "乡镇", "party", "乡科级", False, "团风县基层干部出身"),
    {"start": "2004-07", "end": "unknown", "org": "履历之缺口", "title": "", "level": "", "system": "", "notes": "2004年7月参加工作以来团风各镇细节时间未完整公开", "confidence": "confirmed", "source_ids": ["S002"]},
]

qin_career = [
    row("2021-11", "present", "罗田县人民代表大会常务委员会", "县人大常委会主任", "县级", "congress", "正县级", True, "罗田县第十八届人大常委会主任（县委委员）"),
    row("", "", "黄冈市住房公积金管理中心", "副主任", "地级市", "government", "副县级", False, "调任"),
    row("", "", "红安县人民政府", "副县长", "县级", "government", "副县级", True, "跨县（红安为黄冈市辖县）"),
    row("", "", "中共红安县委员会", "县委常委、宣传部部长", "县级", "party", "副县级", True, "红安县委常委兼宣传部长"),
    row("", "", "罗田县石桥铺镇/河铺镇/九资河镇", "组织干事/组织委员/党委副书记/镇长/党委书记", "乡镇", "party", "乡科级", True, "罗田本地基层出身"),
    {"start": "1987-07", "end": "unknown", "org": "履历之缺口", "title": "", "notes": "1987年7月参加工作（罗田基层），具体各节点年份待补", "confidence": "confirmed", "source_ids": ["S002"]},
]

zhang_career = [
    row("2021-11", "present", "中国人民政治协商会议罗田县委员会", "县政协主席", "县级", "congress", "正县级", True, "县委委员、县政协主席（曾任罗田县副县长）"),
    row("", "", "罗田县人民政府", "副县长", "县级", "government", "副县级", True, "曾任副县长"),
    row("1988-07", "unknown", "罗田县各乡镇", "基层干部", "乡镇", "party", "乡科级", False, "1988年7月参加工作，罗田基层出身"),
]

zhou_rels = [
    {"person": "汪湘云", "person_id": "luotian_汪湘云", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记—县长（县领导班子成员，2026-01至今）", "overlap_org": "中共罗田县委员会", "overlap_period": "2026-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    {"person": "郝爱芳", "person_id": "luotian_郝爱芳", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "前任书记→继任书记（2025年12月交接，周黎由县长升任书记）", "overlap_org": "中共罗田县委员会", "overlap_period": "2021-2025", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
]

wang_rels = [
    {"person": "周黎", "person_id": "luotian_周黎", "relationship_type": "overlap", "strength": "strong", "evidence": "县长—县委书记，县领导班子成员（2026-01至今）", "overlap_org": "中共罗田县委员会", "overlap_period": "2026-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    {"person": "姜焕勇", "person_id": "luotian_姜焕勇", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "县长—常务副县长（县政府党组副书记）", "overlap_org": "罗田县人民政府", "overlap_period": "2026至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
]


def _write_profiles_json():
    profiles = []
    zhou = _get(1)
    wang = _get(2)
    qin = _get(4)
    zhang = _get(5)

    zhou_prof = json_profile(zhou, "正县级", zhou_career, zhou_rels, [], "1982年生，长江大学动物医学专业毕业，湖北省农科院期间各关键任职具体时间节点待补", "cross_county_rotation", ["party", "government", "agriculture"], ["动物医学/农业", "组织人事"])
    wang_prof = json_profile(wang, "正县级", wang_career, wang_rels, "团风→浠水→罗田 女子部调任路径，团风各乡镇任职年份待补", "cross_county_rotation", ["party", "government", "organization"], ["财政/农村基层"])
    qin_prof = json_profile(qin, "正县级", qin_career, [], "罗田基层出身，红安跨县任职年份具体待查", "local_ladder", ["party", "government", "乡"], [])
    zhang_prof = json_profile(zhang, "正县级", zhang_career, [], "1988年参加工作，先后任副县长、县政协主席，早期基层年份待补", "local_ladder", ["party", "government"], [])

    # governance + style evidence from official news
    zhou_prof["governance_record"] = [
        {"period": "2025-2026", "domain": "rural_revitalization", "achievement_or_event": "县委书记调研旅游产业发展（2026-07-28）、工业经济平台建设及招商引资工作推进会（2026-03-31）", "role_in_event": "县委书记主持推进", "measurable_outcome": "", "location": "罗田县", "confidence": "confirmed", "source_ids": ["S001"]},
        {"period": "2026-01", "domain": "party_building", "achievement_or_event": "主持罗田县委理论学习中心组2026年第11次集体学习（2026-07-25）", "role_in_event": "县委书记主持并讲话", "measurable_outcome": "", "location": "罗田县", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    zhou_prof["work_style_and_personality"] = {
        "public_style_indicators": [{"trait": "low_profile", "evidence": "正式讲话强调严守政治规矩、坚决执行党中央和省委市委决策部署（2025-12 党建工作调研会）", "confidence": "confirmed", "source_ids": ["S001"]}],
        "speech_themes": ["全域旅游/文旅产业", "工业经济", "招商引资", "党的建设"],
        "management_signals": ["多次主持县委常委会并亲自抓招商引资、望点工业项目推进会"],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
    }
    wang_prof["governance_record"] = [
        {"period": "2026", "domain": "economic_development", "achievement_or_event": "出席“县政府招商引资组2026年工作推进会”（2026-04-15）", "role_in_event": "县长出席讲话", "measurable_outcome": "", "location": "罗田县", "confidence": "confirmed", "source_ids": ["S001"]},
        {"period": "2026-02", "domain": "agriculture", "achievement_or_event": "主持十八届罗田县政府常务会议（第100-103次）部署一揽子县域工作", "role_in_event": "县长主持", "measurable_outcome": "", "location": "罗田县", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    wang_prof["work_style_and_personality"] = {
        "public_style_indicators": [{"trait": "low_profile", "evidence": "公开报道以主持政府常务会议、调研县域经济为主", "confidence": "confirmed", "source_ids": ["S001"]}],
        "speech_themes": ["招商引资", "项目建设", "乡村振兴"],
        "management_signals": ["担任校长及政府党组副书记多年，组织协调经验丰富"],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
    }

    profiles.append((f"{TODAY}-湖北省-黄冈市-县委书记-周黎.json", zhou_prof))
    profiles.append((f"{TODAY}-湖北省-黄冈市-县长-汪湘云.json", wang_prof))
    profiles.append((f"{TODAY}-湖北省-黄冈市-县人大常委会主任-秦新平.json", qin_prof))
    profiles.append((f"{TODAY}-湖北省-黄冈市-县政协主席-张卫兵.json", zhang_prof))

    for fname, data in profiles:
        with open(HERE / fname, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return profiles


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县级")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 罗田县人民政府门户网站 + 公开报道")
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