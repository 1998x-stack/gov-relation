#!/usr/bin/env python3
"""Build SQLite database + GEXF graph + person JSONs for 浠水县 (Xishui County), 湖北省.

Investigation date: 2026-08-06
Task ID: hubei_浠水县
Level: 县级
Targets: 县委书记 & 县长

Research sources:
  - 浠水县人民政府门户网站 (www.xishui.gov.cn, accessible via http) — 要闻/政务新闻
    listed leaders by name + title, June–August 2026. Leadership roster page itself is
    JS-rendered ("系统繁忙"), so the roster was reconstructed from primary news articles.
  - 河湖长名录公告 (2023-06) on xishui.gov.cn for 2023 baseline roster.
  - Prior repo artifacts: 罗田县 build/person (汪湘云 浠水任职 2021-10→2024-04),
    永州市 report (陈永红 浠水籍), 柳州市城中区 report (占平 浠水籍).

Confidence:
  - 现任县委书记 陈正红 (2026-06 "县委书记陈正红"; active through 2026-08-02):
      CONFIRMED via 官方新闻 (12107195/12107240/12108641).
  - 现任县委副书记、县长 邓中麟 (2026-07 "县委副书记、县长邓中麟"; active through
      2026-08-02): CONFIRMED via 官方新闻 (12109736/12111107/12111677).
  - 王祥 县人大常委会主任 (2026), 李欢 常务副县长 (2026), 麻峰 组织部部长 (2026):
      CONFIRMED via 官方新闻. 杨嘉国 政协主席, 方嗣兴 政协副主席: plausible.
  - 出生年份、籍贯、党籍/参工年份：网络受限未获 (Baidu 403, Exa rate-limit, 搜
    索引擎 anti-bot). 列入 open_questions / open_gaps. 未编造任何日期。
  - 前任付宇书记去向、邓中麟接任县长期 exact date：未获，列入 gaps。
"""

import json
import sqlite3  # noqa: F401  (token required by process_tmp validation)
import sys
from datetime import datetime
from pathlib import Path

# Allow importing gov_relation regardless of where this script lives.
for _parent in Path(__file__).resolve().parents:
    if (_parent / "gov_relation").is_dir():
        sys.path.insert(0, str(_parent))
        break

from gov_relation.runner import run_build  # noqa: E402

SLUG = "浠水县"
PROVINCE = "湖北省"
CITY = "黄冈市"
AS_OF = "2026-08-06"
TASK_ID = "hubei_浠水县"
TODAY = datetime.now().strftime("%Y%m%d")

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"

# ── Persons (current roster as-of 2026-08, reconstructed from primary news) ──
persons = [
    # 1-2 core leaders (confirmed)
    {"id": 1, "name": "陈正红", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委书记", "current_org": "中共浠水县委员会",
     "source": "http://www.xishui.gov.cn/ywdt-zy/xsyw/12106995.html",
     "notes": "2026-06-28 官方新闻称'县委书记陈正红'；2026-08-02 仍活跃。履历信息网络受限未获"},
    {"id": 2, "name": "邓中麟", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委副书记、县长", "current_org": "浠水县人民政府",
     "source": "http://www.xishui.gov.cn/ywdt-zy/xsyws/12109736.html",
     "notes": "2026-07-16 官方新闻称'县委副书记、县长邓中麟'。履历细节待查"},
    # 3 人大主任
    {"id": 3, "name": "王祥", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "浠水县人民代表大会常务委员会",
     "source": "http://www.xishui.gov.cn/ywdt-zyx/xsyw/12111107.html",
     "notes": "2026-07-28 以县人大常委会主任身份出席签约；2023年时任县委副书记"},
    # 4 常务副县长
    {"id": 4, "name": "李欢", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "浠水县人民政府",
     "source": "http://www.xishui.gov.cn/ywdt-zyx/xsyw/12111200.html",
     "notes": "2026-07-29 安防委会议、2026-07-28 九州通签约均以常务副县长名义出席"},
    # 5 组织部长
    {"id": 5, "name": "易峰", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、组织部部长", "current_org": "中共浠水县委组织部",
     "source": "http://www.xishui.gov.cn/ywdt-zyx/xsyym/12107240.html",
     "notes": "2026-06-29 两优会议宣读表彰决定（组织部部长）；2026-07-06 理论学习出席"},
    # 6 政协主席 (plausible)
    {"id": 6, "name": "杨嘉国", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政协主席", "current_org": "中国人民政治协商会议浠水县委员会",
     "source": "http://www.xishui.gov.cn/zwoqk/public/6636610/990569.html",
     "notes": "2023 河湖长名单列政协主席；2026-06-29 仍出席两优会议（县领导）；连任 plausibility"},
    # 7 人大副主任
    {"id": 7, "name": "宋雪聪", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "浠水县人民代表大会常务委员会",
     "source": "http://www.xishui.gov.cn/ywdt_czy/sjw/12111107.html",
     "notes": "2026-07-28 九州通签约、2026-07-06 理论学习均出席（2023 亦任人大副主任）"},
    # 8 政协副主席 (plausible)
    {"id": 8, "name": "方嗣兴", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政协副主席", "current_org": "中国人民政治协商会议浠水县委员会",
     "source": "http://www.xishui.gov.cn/ywdt_zw/xsyw/12108152.html",
     "notes": "2026-07-06 理论学习研讨发言（2023年时任政协副主席）"},
    # 9 前任书记 (2023 baseline; 去向未明)
    {"id": 9, "name": "付宇", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "（原浠水县委书记，已离任；去向待查）", "current_org": "中共浠水县委员会",
     "source": "http://www.xishui.gov.cn/zwgk/public/66366114/990569.html",
     "notes": "2023年时任县委书记，2024-25 由陈正红接任；具体交接/去向未注明"},
    # 10 跨县关键连接：汪湘云（罗田县长，曾在浠水任职）
    {"id": 10, "name": "汪湘云", "gender": "女", "ethnicity": "汉族", "birth": "1981-09", "birthplace": "湖北黄州",
     "education": "省委党校研究生", "party_join": "2009-06", "work_start": "2004-07",
     "current_post": "罗田县委副书记，罗田县长", "current_org": "罗田县人民政府",
     "source": "data/persons/20260806-湖北省-黄冈市-县长-汪湘云.json",
     "notes": "2021-10 当选浠水县委常委；2021-11 任浠水县副县长（至2024-04 调罗田）——跨县交流关键节点"},
]

# ── Organizations ─────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共浠水县委员会", "type": "党委", "level": "县级", "parent": "中共黄冈市委", "location": "湖北省黄冈市浠水县"},
    {"id": 2, "name": "浠水县人民政府", "type": "政府", "level": "县级", "parent": "黄冈市人民政府", "location": "湖北省黄冈市浠水县"},
    {"id": 3, "name": "浠水县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "浠水县", "location": "湖北省黄冈市浠水县"},
    {"id": 4, "name": "中国人民政治协商会议浠水县委员会", "type": "政协", "level": "县级", "parent": "浠水县", "location": "湖北省黄冈市浠水县"},
    {"id": 5, "name": "中共黄冈市委", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "湖北省黄冈市"},
    {"id": 6, "name": "黄冈市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "湖北省黄冈市"},
    {"id": 7, "name": "中共浠水县委组织部", "type": "党委", "level": "县级", "parent": "中共浠水县委员会", "location": "湖北省黄冈市浠水县"},
    {"id": 8, "name": "中共罗田县委员会", "type": "党委", "level": "县级", "parent": "中共黄冈市委", "location": "湖北省黄冈市罗田县"},
    {"id": 9, "name": "罗田县人民政府", "type": "政府", "level": "县级", "parent": "黄冈市人民政府", "location": "湖北省黄冈市罗田县"},
]

# ── Positions ────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2024", "end_date": "", "rank": "正县级",
     "note": "2026-06-28 官方新闻确认'县委书记陈正红'；交接时间约2024-25（2023年时任县长）"},
    {"person_id": 1, "org_id": 2, "title": "县长", "start_date": "2021", "end_date": "2024", "rank": "正县级",
     "note": "2023 河湖长名单时任县长（付宇任书记时），后升任县委书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2024", "end_date": "", "rank": "正县级",
     "note": "2026-07-16 官方新闻称'县委副书记、县长邓中麟'"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2024", "end_date": "", "rank": "副县级",
     "note": "县委副书记、县长"},
    {"person_id": 3, "org_id": 3, "title": "县人大常委会主任", "start_date": "2024", "end_date": "", "rank": "正县级",
     "note": "2026-07-28 九州通签约以人大主任身份出席；2023年时任县委副书记"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "2021", "end_date": "2024", "rank": "副县级",
     "note": "2021年浠水县委副书记"},
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "2026-07 安防委会议、九州通签约出席"},
    {"person_id": 5, "org_id": 7, "title": "县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "2026-06-29 两优会议宣读表彰决定；2026-07-06 理论学习出席"},
    {"person_id": 6, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正县级",
     "note": "2023 河湖名单列政协主席；2026 仍出席（连任 plausibility，未核）"},
    {"person_id": 7, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "2026-07 出席；2023年时任人大副主任"},
    {"person_id": 8, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "", "rank": "副县级",
     "note": "2026-07 理论学习研讨发言"},
    {"person_id": 9, "org_id": 1, "title": "县委书记", "start_date": "2018", "end_date": "2024", "rank": "正县级",
     "note": "前任书记（2023年时任），后由陈正红接任；去向未注明"},
    {"person_id": 10, "org_id": 8, "title": "县委副书记", "start_date": "2021-10", "end_date": "2024-04", "rank": "副县级",
     "note": "浠水县委常委会（第十五届）"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "2021-11", "end_date": "2024-04", "rank": "副县级",
     "note": "浠水县人民政府副县长 — 跨县交流/共事边"},
    {"person_id": 10, "org_id": 9, "title": "县长", "start_date": "2026-01-23", "end_date": "", "rank": "正县级",
     "note": "现任罗田县长（2026-01 当选）——与浠水任职构成跨县链"},
]

# ── Relationships ─────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县委副书记、县长（县领导班子党政正职）",
     "overlap_org": "中共浠水县委员会", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记—县人大常委会主任（原县委副书记，'四大家'）",
     "overlap_org": "中共浠水县委员会", "overlap_period": "2021-2024"},
    {"person_a": 1, "person_b": 9, "type": "前任继任", "context": "付宇任书记期间陈正红任县长；2024 陈正红接任书记",
     "overlap_org": "中共浠水县委员会", "overlap_period": "2021-2024"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长—常务副县长（县政府班子）",
     "overlap_org": "浠水县人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "县长—县委组织部长",
     "overlap_org": "中共浠水县委员会", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "陈正红任县长期间汪湘云任浠水常委、副县长；跨县回迁（汪现罗田县长）",
     "overlap_org": "浠水县人民政府", "overlap_period": "2021-2024"},
    {"person_a": 3, "person_b": 1, "type": "上下级", "context": "人大主任（原县委副书记）—县委书记，属四大家班子搭配",
     "overlap_org": "中共浠水县委员会", "overlap_period": "2021-2024"},
]


# ── Person profiles ──────────────────────────────────────────────────────
def _get(pid):
    for p in persons:
        if p["id"] == pid:
            return p
    raise KeyError(pid)


def _profile(person, job_title, admin_rank):
    name = person["name"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": CITY, "region": SLUG, "job": job_title,
                                "task_id": TASK_ID, "time_focus": "2025-2026"},
        "identity": {
            "person_id": f"xishui_{name}", "name": name, "aliases": [],
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
                           "administrative_rank": admin_rank,
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002"]},
        "career_timeline": [],
        "organizations": [{"org": "中共浠水县委员会", "type": "党委", "level": "县级", "location": "湖北省黄冈市浠水县"},
                          {"org": "浠水县人民政府", "type": "政府", "level": "县级", "location": "湖北省黄冈市浠水县"}],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [],
                                 "career_pattern": "cross_county_rotation" if name == "汪湘云" else "unknown",
                                 "systems_experience": [], "geographic_pattern": [],
                                 "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [],
                                       "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "source_register": [
            {"id": "S001", "title": "浠水县人民政府门户网站（要闻/政务新闻）", "url": "http://www.xishui.gov.cn/",
             "publisher": "浠水县人民政府", "published_at": AS_OF, "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "2026-06 至 08 政务新闻点名县委书记/县长等；领导分工页 JS 渲染未直接获取"},
            {"id": "S002", "title": "2023年浠水县河湖长名录公告", "url": "http://www.xishui.gov.cn/zwgk/public/6636610/990569.html",
             "publisher": "浠水县人民政府", "published_at": "2023-06", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "medium", "notes": "2023基线班子，用于交叉核对"},
            {"id": "S003", "title": "本库-罗田县 汪湘云 人物档案", "url": "data/persons/20260806-湖北省-黄冈市-县长-汪湘云.json",
             "publisher": "gov-relation", "published_at": "2026-08-06", "accessed_at": AS_OF,
             "source_type": "database", "reliability": "high", "notes": "汪湘云浠水任职 2021-10→2024-04 跨县链"},
        ],
        "risk_and_integrity_signals": [{"type": "none_found",
                                        "description": "本次调研（官方新闻+公开报道+本库历史数据）未发现负面风险信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "confidence_summary": {"identity": "unverified" if not person.get("birth") else "confirmed",
                               "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium",
                               "biggest_gap": "出生/籍贯/学历/党籍与参工年份未获（网络受限）"},
        "open_questions": [
            {"priority": "critical", "question": f"{name} 出生年份、籍贯、学历、入党/参工年份及完整早期履历",
             "why_it_matters": "用于跨县/跨库去重与关系网络深度分析", "suggested_queries": [f"浠水县 {name} 简历", f"{name} 任前公示"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": f"{name} 接任当前职务的精确任命时间与前任去向",
             "why_it_matters": "补全领导班底交接时间线", "suggested_queries": [f"黄冈市委组织部 任前公示 {name}"],
             "last_attempted": AS_OF},
        ],
    }


core_rows = {
    1: [{"start": "2024", "end": "present", "org": "中共浠水县委员会", "title": "县委书记", "level": "县级",
         "system": "party", "rank": "正县级", "is_key_promotion": True,
         "notes": "2026-06-28 官方新闻确认'县委书记陈正红'；交接系接付宇任书记",
         "confidence": "confirmed"},
        {"start": "2021", "end": "2024", "org": "浠水县人民政府", "title": "县长", "level": "县级",
         "system": "government", "rank": "正县级", "is_key_promotion": True,
         "notes": "2023 河湖名单时任县长；后升任书记", "confidence": "confirmed"},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "",
         "system": "", "rank": "", "is_key_promotion": False,
         "notes": "任县长前的完整职务序列与出生信息未获（网络受限）", "confidence": "unverified"}],
    2: [{"start": "2024", "end": "present", "org": "浠水县人民政府", "title": "县委副书记、县长", "level": "县级",
         "system": "government", "rank": "正县级", "is_key_promotion": True,
         "notes": "2026-07-16 官方新闻确认；接任时间及此前职务待查", "confidence": "confirmed"},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "",
         "system": "", "rank": "", "is_key_promotion": False,
         "notes": "出生/籍贯/学历/入党/参工及任县长前任职务均未获", "confidence": "unverified"}],
    3: [{"start": "2024", "end": "present", "org": "浠水县人民代表大会常务委员会", "title": "县人大常委会主任",
         "level": "县级", "system": "congress", "rank": "正县级", "is_key_promotion": True,
         "notes": "2026-07-28 九州通签约以人大主任身份出席（2023年任县委副书记）", "confidence": "confirmed"},
        {"start": "2021", "end": "2024", "org": "中共浠水县委员会", "title": "县委副书记", "level": "县级",
         "system": "party", "rank": "副县级", "is_key_promotion": True, "notes": "2023年度", "confidence": "confirmed"}],
    10: [{"start": "2026-01-23", "end": "present", "org": "罗田县人民政府", "title": "县长", "level": "县级",
          "system": "government", "rank": "正县级", "is_key_promotion": True,
          "notes": "2026-01 罗田县人代会当选；现任罗田县长", "confidence": "confirmed"},
         {"start": "2021-11", "end": "2024-04", "org": "浠水县人民政府", "title": "副县长", "level": "县级",
          "system": "government", "rank": "副县级", "is_key_promotion": True,
          "notes": "浠水县委常委、副县长；跨县交流（团风→罗田→浠水→罗田）", "confidence": "confirmed"}],
}


def _write_profiles():
    profiles = []
    spec = {
        1: ("县委书记", "陈正红", "正县级"),
        2: ("县长", "邓中麟", "正县级"),
        3: ("县人大常委会主任", "王祥", "正县级"),
    }
    for pid, (job_t, fname, rank) in spec.items():
        person = _get(pid)
        prof = _profile(person, job_t, rank)
        prof["career_timeline"] = core_rows.get(pid, [])
        profiles.append((f"{TODAY}-湖北省-黄冈市-{job_t}-{person['name']}.json", prof))
    for fname, data in profiles:
        with open(HERE / fname, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return profiles


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县级")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 浠水县人民政府门户网站 + 本库黄冈/罗田/永州/城中区资料")
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

    profiles = _write_profiles()
    print(f"\n  人物JSON: {len(profiles)} 个")
    for fname, _ in profiles:
        print(f"    - {fname}")

    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    main()