#!/usr/bin/env python3
"""Build SQLite database + GEXF graph + person JSONs for 监利市 (Jianli City), 湖北省.

Investigation date: 2026-08-06
Task ID: hubei_监利市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - 监利市人民政府门户网站 www.jianli.gov.cn — 监利要闻/领导信息/两会、市二届人大常委会第三十次会议、政府工作报告
  - 监利发布 / 湖北日报 / 中华网湖北 / 凤凰网湖北 / 腾讯新闻 / 荆州新闻网 / 鲁中晨报等公开人事报道
  - 百度百科 (聂良平/瞿俊森/韩旭) 及官方任前公示

Confidence:
  - 现任市委书记 聂良平、市委副书记/市长 瞿俊森: CONFIRMED (2025-12-27 市二届人大常委会第三十次会议决定;
    2025-12-31 二届人大五次会议第三次全体会议 瞿俊森当选市长; 百度百科/官方领导之窗、2026-02/05 市委常委会新闻持续确认)
  - 市人大常委会主任 项红、市政协主席 廖和平: CONFIRMED (2025-12-28 两会主席台就座)
  - 市委常委会: 王焱群(常务副市长/市委副书记?按官方=市委常委、党组副书记、常务副市长/行政学校校长)、李炜(组织/宣传部长)、徐岭(纪委书记/监委主任): CONFIRMED via 官方会议报道
  - 市政府: 李萌/李真顺/曾唯 副市长: CONFIRMED via 官方领导信息
  - 前任市委书记 韩旭、前任市长 聂良平→书记: CONFIRMED via 多源报道 (韩旭 2025-11 拟任新职 (卸任监利市委书记)卸任)
  - 部分履历中段节点 (聂良平 2001-2020、韩旭 2009-2020 濮阳时期) 公开细节有限, 在 open_questions/报告标注, 不虚造日期。
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

SLUG = "监利市"
PROVINCE = "湖北省"
CITY = "荆州市"
AS_OF = "2026-08-06"
TODAY = datetime.now().strftime("%Y%m%d")

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"

# ── Persons (confirmed as-of 2026-08-06) ─────────────────────────────────
persons = [
    {"id": 1, "name": "聂良平", "gender": "男", "ethnicity": "汉族", "birth": "1977-09", "birthplace": "湖北潜江",
     "education": "大学本科（中国地质大学 贸易经济专业）", "party_join": "1998-12", "work_start": "1999-07",
     "current_post": "市委书记", "current_org": "中共监利市委员会",
     "source": "http://www.jianli.gov.cn/"},
    {"id": 2, "name": "瞿俊森", "gender": "男", "ethnicity": "土家族", "birth": "1985-01", "birthplace": "湖北恩施",
     "education": "硕士研究生（清华大学法学院 刑法学专业）", "party_join": "", "work_start": "",
     "current_post": "市长", "current_org": "监利市人民政府",
     "source": "http://www.jianli.gov.cn/"},
    {"id": 3, "name": "项红", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "市人大常委会主任", "current_org": "监利市人民代表大会常务委员会",
     "source": "http://www.jianli.gov.cn/"},
    {"id": 4, "name": "廖和平", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "市政协主席", "current_org": "中国人民政治协商会议监利市委员会",
     "source": "http://www.jianli.gov.cn/"},
    {"id": 5, "name": "王焱群", "gender": "男", "ethnicity": "汉族", "birth": "1983-07", "birthplace": "", "education": "本科学历",
     "party_join": "", "work_start": "", "current_post": "市委常委、常务副市长", "current_org": "监利市人民政府",
     "source": "http://www.jianli.gov.cn/"},
    {"id": 6, "name": "李炜", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "市委常委、市委组织部部长、市委宣传部部长、市总工会主席",
     "current_org": "中共监利市委组织部", "source": "http://www.jianli.gov.cn/"},
    {"id": 7, "name": "徐岭", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "市委常委、市纪委书记、市监委主任", "current_org": "中共监利市纪律检查委员会",
     "source": "http://www.jianli.gov.cn/"},
    {"id": 8, "name": "李萌", "gender": "男", "ethnicity": "汉族", "birth": "1970-06", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "", "current_post": "副市长", "current_org": "监利市人民政府",
     "source": "http://www.jianli.gov.cn/"},
    {"id": 9, "name": "李真顺", "gender": "女", "ethnicity": "朝鲜族", "birth": "1978-04", "birthplace": "", "education": "博士研究生",
     "party_join": "", "work_start": "", "current_post": "副市长", "current_org": "监利市人民政府",
     "source": "http://www.jianli.gov.cn/"},
    {"id": 10, "name": "曾唯", "gender": "女", "ethnicity": "汉族", "birth": "1987-01", "birthplace": "", "education": "研究生学历",
     "party_join": "", "work_start": "", "current_post": "副市长", "current_org": "监利市人民政府",
     "source": "http://www.jianli.gov.cn/"},
    {"id": 11, "name": "韩旭", "gender": "男", "ethnicity": "汉族", "birth": "1982-01", "birthplace": "河南邓州",
     "education": "博士研究生、理学博士（中国科学技术大学硕博连读）", "party_join": "2006-06", "work_start": "2008-07",
     "current_post": "荆州市委常委（前任监利市委书记）", "current_org": "中共荆州市委",
     "source": "https://baike.baidu.com/"},
    {"id": 12, "name": "刘俊军", "gender": "男", "ethnicity": "汉族", "birth": "1981-07", "birthplace": "",
     "education": "省委党校研究生", "party_join": "", "work_start": "",
     "current_post": "仙桃市委常委、组织部部长（原监利副市长）", "current_org": "中共仙桃市委委员会",
     "source": "https://baike.baidu.com/"},
]

# ── Organizations ─────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共监利市委员会", "type": "党委", "level": "县级市", "parent": "中共荆州市委", "location": "湖北省荆州市监利市"},
    {"id": 2, "name": "监利市人民政府", "type": "政府", "level": "县级市", "parent": "荆州市人民政府", "location": "湖北省荆州市监利市"},
    {"id": 3, "name": "监利市人民代表大会常务委员会", "type": "人大", "level": "县级市", "parent": "监利市", "location": "湖北省荆州市监利市"},
    {"id": 4, "name": "中国人民政治协商会议监利市委员会", "type": "政协", "level": "县级市", "parent": "监利市", "location": "湖北省荆州市监利市"},
    {"id": 5, "name": "中共荆州市委", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "湖北省荆州市"},
    {"id": 6, "name": "荆州市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "湖北省荆州市"},
    {"id": 7, "name": "中共监利市委组织部", "type": "党委", "level": "县级市", "parent": "中共监利市委员会", "location": "湖北省荆州市监利市"},
    {"id": 8, "name": "中共监利市纪律检查委员会", "type": "党委", "level": "县级市", "parent": "中共监利市委员会", "location": "湖北省荆州市监利市"},
    {"id": 9, "name": "中共沙市区委", "type": "党委", "level": "区级", "parent": "中共荆州市委", "location": "湖北省荆州市沙市区"},
    {"id": 10, "name": "沙市区人民政府", "type": "政府", "level": "区级", "parent": "荆州市人民政府", "location": "湖北省荆州市沙市区"},
]

# ── Positions (confirmed, as-of 2026-08-06) ──────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2025-12", "end_date": "", "rank": "正县级", "note": "接韩旭任监利市委书记；2025-12 兼任市长至 2025-12-31 辞去市长"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start_date": "2020-10", "end_date": "2025-12", "rank": "正县级", "note": "2020-10 任副市长、代理市长；2021-01-08 当选监利市长；2025-12-31 辞去市长"},
    {"person_id": 1, "org_id": 1, "title": "市委副书记", "start_date": "2020-10", "end_date": "2025-12", "rank": "副县级", "note": "任市长期间兼任市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2025-12-31", "end_date": "", "rank": "正县级", "note": "2025-12-27 任副市长、代理市长；2025-12-31 当选市长"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2023-10", "end_date": "", "rank": "副县级", "note": "2025-12-31 前为市委副书记、政法委书记，其后转任市长"},
    {"person_id": 3, "org_id": 3, "title": "市人大常委会党组书记、主任", "start_date": "", "end_date": "", "rank": "正县级", "note": "2025-12-28 两会主席团前排就座"},
    {"person_id": 4, "org_id": 4, "title": "市政协党组书记、主席", "start_date": "", "end_date": "", "rank": "正县级", "note": "2025-12-28 两会主席团前排就座"},
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "市委常委"},
    {"person_id": 5, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "市政府党组副书记、常务副市长、市行政学校校长"},
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "市委组织部部长，兼任宣传部部长、市总工会主席（2024-10 起兼任组织部长）"},
    {"person_id": 6, "org_id": 7, "title": "市委组织部部长、宣传部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "2024-10 官证实任组织部长并兼宣传部长"},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "2024-10 市委巡察工作领导小组组长"},
    {"person_id": 7, "org_id": 8, "title": "市纪委书记、市监委主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任监利市委常委、市纪委书记、市监委主任"},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "市政府党组成员"},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "市政府党组成员"},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "市政府党组成员"},
    {"person_id": 11, "org_id": 1, "title": "市委书记", "start_date": "2020-06-19", "end_date": "2025-11", "rank": "正县级", "note": "前任监利县委书记/监利市委书记"},
    {"person_id": 11, "org_id": 6, "title": "荆州市副市长", "start_date": "2022-01", "end_date": "2025-03", "rank": "副厅级", "note": "市委常委副职务"},
    {"person_id": 11, "org_id": 5, "title": "荆州市委常委", "start_date": "2025-03", "end_date": "", "rank": "副厅级", "note": "2025-03 任荆州市委常委；2025-11 拟任新职"},  # sourced note
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副县级", "note": "原监利市政府党组成员、副市长（前任）"},
    {"person_id": 12, "org_id": 9, "title": "洪湖市委常委、组织部部长", "start_date": "2025", "end_date": "2026", "rank": "副县级", "note": "监利调洪湖"},
    {"person_id": 12, "org_id": 10, "title": "仙桃市委常委、组织部部长", "start_date": "2026-07", "end_date": "", "rank": "副县级", "note": "2026-06 省委组织部任前公示(2026年第112号)，跨市履新"},
]

# ── Relationships (confirmed) ─────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长（市委班子 & 市政府班子共事）", "overlap_org": "中共监利市委员会", "overlap_period": "2025-12至今"},
    {"person_a": 1, "person_b": 2, "type": "前任继任", "context": "聂良平卸任市长，瞿俊森接任市长（2025-12 交接）", "overlap_org": "监利市人民政府", "overlap_period": "2025-12"},
    {"person_a": 11, "person_b": 1, "type": "前任继任", "context": "韩旭卸任书记，聂良平接任书记（长期书记/市长搭档 2020-2025）", "overlap_org": "中共监利市委员会", "overlap_period": "2020-2025"},
    {"person_a": 11, "person_b": 1, "type": "上下级", "context": "韩旭为市委书记、聂良平为市长（2020-2025）", "overlap_org": "监利市人民政府", "overlap_period": "2020-10-2025"},
    {"person_a": 5, "person_b": 2, "type": "上下级", "context": "常务副市长配合市长主持市政府日常工作", "overlap_org": "监利市人民政府", "overlap_period": "2025至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "市委书记—组织部长（市委班子）", "overlap_org": "中共监利市委员会", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 7, "type": "同系统", "context": "市长—纪委书记（市政府/监利体系）", "overlap_org": "监利市人民政府", "overlap_period": "2025至今"},
    {"person_a": 12, "person_b": 1, "type": "上下级", "context": "刘俊军任监利副市长时 聂良平为书记/市长（2025 同僚）", "overlap_org": "监利市人民政府", "overlap_period": "2025"},
]

# ── Person JSON profile builder ───────────────────────────────────────────
def _get(pid):
    for p in persons:
        if p["id"] == pid:
            return p
    raise KeyError(pid)


def build_profile(person, admin_rank, career_rowsrows, rel_list, gov_records, spec, systems, pattern, gap):
    name = person["name"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": CITY, "region": SLUG, "job": person["current_post"],
                                "task_id": "hubei_监利市", "time_focus": "2020-2026"},
        "identity": {
            "person_id": f"jianli_{name}", "name": name, "aliases": [],
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
        "career_timeline": career_rowsrows,
        "organizations": [
            {"org": "中共监利市委员会", "type": "党委", "level": "县级市", "location": "湖北省荆州市监利市"},
            {"org": "监利市人民政府", "type": "政府", "level": "县级市", "location": "湖北省荆州市监利市"},
        ],
        "relationships": rel_list,
        "governance_record": gov_records,
        "professional_profile": {"primary_specializations": spec, "secondary_specializations": [],
                                 "career_rowspattern": pattern, "systems_experience": systems,
                                 "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [],
                                       "management_signals": [],
                                       "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "本次调研（官方新闻+公开报道）未发现该核心人物负面信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "监利市人民政府门户网站（监利要闻/领导信息/市人大常委会会议）", "url": "http://www.jianli.gov.cn/", "publisher": "监利市人民政府", "published_at": AS_OF, "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市委/人大任命、两会、领导信息确认"},
            {"id": "S002", "title": "湖北日报/腾讯/凤凰网湖北/中华网/荆州新闻网 + 百度百科", "url": "https://news.hubeidaily.net/", "publisher": "湖北日报等", "published_at": "2025-12", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "聂良平、瞿俊森、韩旭履历及人事调整"},
        ],
        "confidence_summary": {"identity": "confirmed" if person.get("birth") else "partial",
                               "current_role": "confirmed",
                               "career_rowscompleteness": "complete" if career_rowsrows else "thin",
                               "relationship_confidence": "medium",
                               "biggest_gap": gap},
        "open_questions": [{"priority": "high" if gap else "low", "question": gap, "why_it_matters": "用于跨县网络与晋升路径深度分析",
                            "suggested_queries": [f"监利市 {name} 简历", f"{CITY} 组织部 任前公示 {name}"], "last_attempted": AS_OF}],
    }


# ── Career rows ───────────────────────────────────────────────────────────
def row(start, end, org, title, lvl, system, key, note, conf="confirmed"):
    return {"start": start, "end": end, "org": org, "title": title, "level": lvl, "location": "湖北省",
            "system": system, "rank": "", "is_key_promotion": key, "notes": note, "confidence": conf, "source_ids": ["S001", "S002"]}


# ── 聂良平 career ─────────────────────────────────────────────────────────
nie_career = [
    row("2025-12", "present", "中共监利市委员会", "市委书记", "县级市", "party", True, "原监利市长，2025-12 任市委书记，并短期兼任市长"),
    row("2020-10", "2025-12", "监利市人民政府", "市长", "县级市", "government", True, "2020-10 任副市长、代理市长；2021-01 当选；2025-12-31 辞去市长"),
    row("1995-09", "1999-06", "中国地质大学", "贸易经济专业学生", "本科", "education", False, "大学本科"),
    row("1999-07", "1999-08", "荆州区川店镇", "见习", "乡镇", "government", False, ""),
    row("1999-08", "2000-01", "荆州区川店镇藤店管理区", "副主任", "乡镇", "government", False, ""),
    row("2000-01", "2000-11", "荆州区川店镇藤店管理区", "党总支副书记", "乡镇", "government", False, ""),
    {"start": "2000-11", "end": "2020-10", "org": "履历待查（荆州体系内部职务）", "title": "", "notes": "2000.11 至任监利代理市长前之间约 20 年的中段职务（含外来市委组织部等）公开细节有限", "confidence": "unverified", "source_ids": []},
]

# ── 瞿俊森 career ─────────────────────────────────────────────────────────
qu_career = [
    row("2025-12-31", "present", "监利市人民政府", "市长", "县级市", "government", True, "2025-12-31 当选监利市长"),
    row("2025-12-27", "2025-12-31", "监利市人民政府", "副市长、代理市长", "县级市", "government", True, "2025-12-27 市二届人大常委会第三十次会议任命"),
    row("2023-10", "2025-12", "中共监利市委员会", "市委副书记、政法委书记", "县级市", "party", True, "2023-10 由荆州共青团调任监利"),
    row("2021-12", "2023-10", "共青团荆州市委", "团委书记", "地级市", "organization", True, "2021-12 任团委书记"),
    row("2021-09", "2021-12", "共青团荆州市委", "团委副书记（主持全面工作）", "地级市", "organization", True, ""),
    row("", "", "荆州市沙市区", "副区长、沙市经济开发区管委会主任", "区级", "government", True, "沙市区副区长"),
    row("", "", "沙市区锣场镇", "党委书记", "乡镇", "party", True, ""),
    row("", "", "沙市区立新乡", "党委副书记、乡长", "乡镇", "government", False, ""),
    {"start": "", "end": "", "org": "学历", "title": "清华大学法学院 刑法学专业 硕士", "notes": "土家族，湖北恩施人", "confidence": "confirmed", "source_ids": ["S002"]},
]

# ── 韩旭 career (predecessor) ─────────────────────────────────────────────
han_career = [
    row("2025-03", "present", "中共荆州市委", "市委常委", "地级市", "party", True, "2025-03 任荆州市委常委，卸任副市长"),
    row("2022-01", "2025-03", "荆州市人民政府", "荆州市副市长", "地级市", "government", True, "2022-01 任，并兼监利市委书记"),
    row("2020-06-19", "2025-11", "中共监利市委员会", "市委书记（原监利县委）", "县级市", "party", True, "2020-06-19 任监利县委书记，监利撤县设市后任监利市委书记；2025-11 卸任"),
    row("", "", "河南省濮阳市（台前县等）", "县长等", "县", "government", True, "34 岁任濮阳县长"),
    row("2009-06", "", "河南省濮阳工业园区管委会", "主任助理", "副县级", "development_zone", True, "27 岁副县级；跨省调河南濮阳"),
    row("2008-07", "2009-06", "湖北孝感市科技局", "干部", "市直", "government", False, ""),
    row("2003", "2008", "中国科学技术大学", "硕博连读", "高等教育", "education", True, ""),
]

# ── relationship lists for person JSON ─────────────────────────────────────
nie_rels = [
    {"person": "瞿俊森", "person_id": "jianli_瞿俊森", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "书记—市长，且 2025-12 市长交接（聂良平→瞿俊森）", "overlap_org": "监利市人民政府", "overlap_period": "2025-12至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    {"person": "韩旭", "person_id": "jianli_韩旭", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "韩旭卸任书记，聂良平 2025-12 接任", "overlap_org": "中共监利市委员会", "overlap_period": "2020-2025", "confidence": "confirmed", "source_ids": ["S002"]},
]
qu_rels = [
    {"person": "聂良平", "person_id": "jianli_聂良平", "relationship_type": "overlap", "strength": "strong", "evidence": "市长—市委书记（2025-12至今市班子共事）", "overlap_org": "中共监利市委员会", "overlap_period": "2025-12至今", "confidence": "confirmed", "source_ids": ["S001"]},
    {"person": "王焱群", "person_id": "jianli_王焱群", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "市长—常务副市长", "overlap_org": "监利市人民政府", "overlap_period": "2025至今", "confidence": "confirmed", "source_ids": ["S001"]},
]

def _write_profiles_json():
    profiles = []
    nie_prof = build_profile(_get(1), "正县级", nie_career, nie_rels,
                             [{"period": "2025-2026", "domain": "governance", "achievement_or_event": "主持市二届人大常委会三十次会议, 辞去市长任书记", "role_in_event": "市委书记", "measurable_outcome": "", "location": "监利市", "confidence": "confirmed", "source_ids": ["S001"]}],
                             ["贸易经济"], ["party", "government"], "本地梯子+市长接任书记",
                             "2000.11-2020.10 中段履历公开有限（含外来市委组织部、荆州体系内职务）")
    qu_prof = build_profile(_get(2), "正县级", qu_career, qu_rels,
                            [{"period": "2025-12", "domain": "governance", "achievement_or_event": "2025-12 市二届人大常委会第三十次会议任命、当选监利市长；2026 主持欠薪治理调度等", "role_in_event": "市长", "measurable_outcome": "", "location": "监利市", "confidence": "confirmed", "source_ids": ["S001", "S002"]}],
                             ["法学"], ["party", "government", "organization"], "跨区交流",
                             "沙市区履历前更早节点（出生年份后至立新乡前）待查")
    profiles = [
        ("20260806-湖北省-荆州市-市委书记-聂良平.json", nie_prof),
        ("20260806-湖北省-荆州市-市长-瞿俊森.json", qu_prof),
    ]
    for fname, data in profiles:
        with open(HERE / fname, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return profiles


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县级市")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 监利市人民政府门户网站 + 公开报道")
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