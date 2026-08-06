#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 淅川县 (Xichuan County), 河南省南阳市.

Task ID: henan_淅川县 | Level: 县 | Targets: 县委书记 & 县长
Investigation date: 2026-08-06

Research sources:
  - www.xichuan.gov.cn 淅川县人民政府（领导简介/领导接访/政府会议/全会公报）
  - www.nanyang.gov.cn 南阳市人民政府（在线访谈 2025-12-24；郭广全调研；河湖长制等）
  - baike.baidu.com 张志强；www.thepaper.cn 澎湃新闻（张志强拟任市委常委；王兴勇调任）
  - www.nydi.gov.cn 市纪委淅川案例；dahe.cn（2024-03 人大/政协换届）

Confidence:
  - 张志强 identity+current_role confirmed（官方百科+任命公示+政府会议）
  - 郭广全 current confirmed（2025-09/12、2026 多场活动）；早期履历部分确认（桐柏纪委、新野政府）；出生/籍贯未查到
  - 包海竣 社旗组织部长->淅川副书记（跨县）confirmed
  - 卢捍卫（前书记，现省纪委副书记）、王兴勇（前县长，现兰考书记）confirmed
  - 徐成成旺、杨文永、王兵 出生年/籍贯 未能核实（medium）
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
SLUG = "淅川县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(STAGING)

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    {"id": 1, "name": "张志强", "gender": "男", "ethnicity": "汉族", "birth": "1980年11月",
     "birthplace": "", "education": "研究生学历（公共管理硕士）", "party_join": "中共党员",
     "work_start": "", "current_post": "县委书记（南阳市委常委）", "current_org": "中共淅川县委员会",
     "source": "https://baike.baidu.com/item/张志强/62040429"},
    {"id": 2, "name": "郭广全", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "县委副书记、县长", "current_org": "淅川县人民政府",
     "source": "https://www.nanyang.gov.cn/2025/12-24/1364249.html"},
    {"id": 3, "name": "包海竣", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "县委副书记（专职）", "current_org": "中共淅川县委员会",
     "source": "https://www.nanyang.gov.cn/2025/05-26/1041344.html"},
    {"id": 4, "name": "杨文永", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "县委常委、常务副县长", "current_org": "淅川县人民政府",
     "source": "https://caizj.nanyang.gov.cn/2025/06-13/1044784.html"},
    {"id": 5, "name": "徐成旺", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "县委常委、纪委书记、监委主任", "current_org": "淅川县纪委县监委",
     "source": "https://www.xichuan.gov.cn/2025/12-23/1363665.html"},
    {"id": 6, "name": "王兵", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "县委常委、组织部长", "current_org": "中共淅川县委员会",
     "source": "https://www.xichuan.gov.cn/2025/10-13/1338609.html"},
    {"id": 7, "name": "卢捍卫", "gender": "男", "ethnicity": "汉族", "birth": "1967年",
     "birthplace": "南阳市（河南）", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "前县委书记（现任河南省纪委监委副书记）", "current_org": "中共淅川县委员会（原）",
     "source": "https://news.qq.com/rain/a/20240928A072Q100"},
    {"id": 8, "name": "王兴勇", "gender": "男", "ethnicity": "", "birth": "1978年12月",
     "birthplace": "", "education": "大学学历", "party_join": "中共党员",
     "work_start": "", "current_post": "前县长（现任兰考县委书记）", "current_org": "淅川县人民政府（原）",
     "source": "https://www.nanyang.gov.cn/2025/04-08/1031834.html"},
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共淅川县委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委", "location": "南阳市淅川县"},
    {"id": 2, "name": "淅川县人民政府", "type": "政府", "level": "县级", "parent": "南阳市人民政府", "location": "南阳市淅川县"},
    {"id": 3, "name": "淅川县纪委县监委", "type": "纪委", "level": "县级", "parent": "中共淅川县委", "location": "南阳市淅川县"},
    {"id": 4, "name": "淅川县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "淅川县", "location": "南阳市淅川县"},
    {"id": 5, "name": "中国人民政治协商会议淅川县委员会", "type": "政协", "level": "县级", "parent": "淅川县", "location": "南阳市淅川县"},
    {"id": 6, "name": "中共南阳市委", "type": "党委", "level": "地级市", "parent": "中共河南省委", "location": "南阳市"},
    {"id": 7, "name": "南阳市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "南阳市"},
    {"id": 8, "name": "河南省纪委监委", "type": "纪委", "level": "省级", "parent": "中共河南省委", "location": "郑州市"},
    {"id": 9, "name": "中共社旗县委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委", "location": "南阳市社旗县"},
    {"id": 10, "name": "社旗县人民政府", "type": "政府", "level": "县级", "parent": "南阳市人民政府", "location": "南阳市社旗县"},
    {"id": 11, "name": "中共桐柏县委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委", "location": "南阳市桐柏县"},
    {"id": 12, "name": "桐柏县纪委县监委", "type": "纪委", "level": "县级", "parent": "中共桐柏县委", "location": "南阳市桐柏县"},
    {"id": 13, "name": "中共新野县委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委", "location": "南阳市新野县"},
    {"id": 14, "name": "新野县人民政府", "type": "政府", "level": "县级", "parent": "南阳市人民政府", "location": "南阳市新野县"},
    {"id": 15, "name": "中共兰考县委员会", "type": "党委", "level": "县级", "parent": "中共开封市委", "location": "开封市兰考县"},
    {"id": 16, "name": "南阳市工商行政管理局", "type": "政府", "level": "地级市", "parent": "南阳市人民政府", "location": "南阳市"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 张志强（县委书记）
    {"person_id": 1, "org_id": 8, "title": "省纪委监委党风政风监督室副主任", "start_date": "约2017年前", "end_date": "约2020", "rank": "副处", "note": "河南省纪委系统"},
    {"person_id": 1, "org_id": 8, "title": "省纪委监委办公厅主任", "start_date": "约2020", "end_date": "2022-11", "rank": "正处/副厅", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "南阳市副市长", "start_date": "2022-11", "end_date": "2025-04", "rank": "副厅级", "note": "2022年11月任南阳市副市长"},
    {"person_id": 1, "org_id": 1, "title": "淅川县委书记、县人武部党委第一书记", "start_date": "2024-09", "end_date": "至今", "rank": "副厅级", "note": "2024-09-30 县人武部党委第一书记任职宣布"},
    {"person_id": 1, "org_id": 6, "title": "南阳市委常委", "start_date": "2025-02", "end_date": "至今", "rank": "副厅级", "note": "2025-02-23 省委组织部拟任公示；2025-04-18 辞去南阳市副市长"},
    # 郭广全（县长）
    {"person_id": 2, "org_id": 12, "title": "桐柏县委常委、县纪委书记、监委主任", "start_date": "约2021", "end_date": "约2022", "rank": "副县级", "note": "桐柏县纪委（2022-01 见报）"},
    {"person_id": 2, "org_id": 13, "title": "新野县委常委、常务副县长", "start_date": "约2022", "end_date": "2025", "rank": "副县级", "note": "新野县政府（2024-02 至 2025 多次见报）"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记、县长", "start_date": "2025半年", "end_date": "至今", "rank": "正县级", "note": "接替王兴勇（约2025年中，2025-09 教师节已以淅川县委副书记见报）"},
    # 包海竣（专职副书记）
    {"person_id": 3, "org_id": 9, "title": "社旗县委常委、组织部部长", "start_date": "约2022", "end_date": "约2024-06", "rank": "副县级", "note": "社旗县（2023 多次见报）"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记（专职）", "start_date": "约2024-06", "end_date": "至今", "rank": "副县级", "note": "淅川县"},
    # 杨文永（常务副县长）
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "约2023", "end_date": "至今", "rank": "副县级", "note": "淅川县政府"},
    # 徐成旺（纪委书记）
    {"person_id": 5, "org_id": 3, "title": "县委常委、纪委书记、监委主任", "start_date": "2024-03", "end_date": "至今", "rank": "副县级", "note": "2024-03 县十六届人大三次会议当选县监委主任"},
    # 王兵（组织部长）
    {"person_id": 6, "org_id": 1, "title": "县委常委、组织部长", "start_date": "约2023", "end_date": "至今", "rank": "副县级", "note": "淅川县"},
    # 卢捍卫（前县委书记）
    {"person_id": 7, "org_id": 16, "title": "南阳市工商行政管理局局长", "start_date": "约2014", "end_date": "2015-09", "rank": "正处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委书记", "start_date": "2015-09", "end_date": "2021-12", "rank": "正处级", "note": "2015-09 任淅川县委书记；2021-06 获授全国优秀县委书记"},
    {"person_id": 7, "org_id": 8, "title": "开封市委常委、市纪委书记（后升省纪委）", "start_date": "2021-12", "end_date": "2024-09", "rank": "副厅级", "note": "2021-12 调开封任纪委书记"},
    {"person_id": 7, "org_id": 8, "title": "省纪委监委副书记、省监委副主任", "start_date": "2024-09", "end_date": "至今", "rank": "副部级", "note": "2024-09-28 任河南省监委副主任"},
    # 王兴勇（前县长）
    {"person_id": 8, "org_id": 1, "title": "县委副书记、县长", "start_date": "2021-07", "end_date": "约2025", "rank": "正县级", "note": "2021-07-17 接替杨红忠任淅川县长（南阳市委组织部公布）"},
    {"person_id": 8, "org_id": 15, "title": "兰考县委副书记、县长", "start_date": "约2025", "end_date": "2026-06", "rank": "正县级", "note": "跨市从淅川调开封兰考任县长"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "张志强为县委书记、郭广全为县长，党政一把手搭档", "overlap_org": "淅川县", "overlap_period": "2025至今"},
    {"person_a": 1, "person_b": 7, "type": "predecessor_successor", "context": "卢捍卫2021-12卸任淅川县委书记后，张志强2024-09接任", "overlap_org": "中共淅川县委员会", "overlap_period": "2015-2021（卢）→2024（张）"},
    {"person_a": 8, "person_b": 2, "type": "predecessor_successor", "context": "王兴勇约2025年调兰考后，郭广全接任淅川县长", "overlap_org": "淅川县人民政府", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "张志强兼淅川县委书记期间，王兴勇任县长（2024-09 至 约2025）", "overlap_org": "淅川县", "overlap_period": "2024-2025"},
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "包海平任淅川县委专职副书记、张志强为县委书记，同在一套班子", "overlap_org": "中共淅川县委员会", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "郭广全早年任桐柏县纪委，徐成旺为现任淅川纪委书记，同在纪检条线", "overlap_org": "纪律检查系统", "overlap_period": "2024至今"},
    {"person_a": 3, "person_b": 6, "type": "same_system", "context": "包海平前为社旗县委组织部长，王兵任淅川组织部长，同组织条线", "overlap_org": "组织系统", "overlap_period": "2024至今"},
    {"person_a": 4, "person_b": 2, "type": "overlap", "context": "杨文永任常务副县长、郭广全为县长，政府班子搭档", "overlap_org": "淅川县人民政府", "overlap_period": "2025至今"},
]


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON writers
# ══════════════════════════════════════════════════════════════════════════

def _source_register():
    return [
        {"id": "S001", "title": "淅川县人民政府—领导接访预安排", "url": "https://www.xichuan.gov.cn/2025/12-23/1363665.html", "publisher": "淅川县人民政府", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        {"id": "S002", "title": "南阳市政府在线访谈—淅川县长郭广全", "url": "https://www.nanyang.gov.cn/2025/12-24/1364249.html", "publisher": "南阳市人民政府", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        {"id": "S003", "title": "百度百科—张志强", "url": "https://baike.baidu.com/item/张志强/62040429", "publisher": "百度百科", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium"},
        {"id": "S004", "title": "流强新闻—张志强拟任市委常委", "url": "http://www.thepaper.cn/newsDetail_forward_30225980", "publisher": "澎湃新闻", "accessed_at": AS_OF, "source_type": "media", "reliability": "high"},
        {"id": "S005", "title": "市纪委—淅川巡察专题会", "url": "http://www.nydi.gov.cn/sitesources/nysjwjw/page_pc/xsqjw/xcx/xxgk/xsxc/article391e7faf15fa407098a98512d2aa607e.html", "publisher": "中共南阳市纪委", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        {"id": "S006", "title": "大河网—淅川县人大/政协换届（2024-03）", "url": "https://app.dahecube.com/nweb/news/20240310/193163n34d169be724.htm", "publisher": "大河网", "accessed_at": AS_OF, "source_type": "media", "reliability": "high"},
        {"id": "S007", "title": "南阳市河湖长制暨库区综合整治会（2025-05）", "url": "https://www.nanyang.gov.cn/2025/05-26/1041344.html", "publisher": "南阳市人民政府", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        {"id": "S008", "title": "腾讯新闻—卢捍卫历任（2024-09）", "url": "https://news.qq.com/rain/a/20240928A072Q100", "publisher": "腾讯新闻", "accessed_at": AS_OF, "source_type": "media", "reliability": "high"},
    ]


def _relationships_for(person_id):
    out = []
    for r in relationships:
        if r["person_a"] == person_id:
            other = r["person_b"]
        elif r["person_b"] == person_id:
            other = r["person_a"]
        else:
            continue
        other_name = {p["id"]: p["name"] for p in persons}[other]
        out.append({
            "person": other_name,
            "person_id": f'henan_xichuan_{other_name}',
            "relationship_type": r["type"],
            "strength": "strong" if r["type"] in ("superior_subordinate", "predecessor_successor") else "medium",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": "confirmed" if r["type"] in ("superior_subordinate", "predecessor_successor") else "plausible",
            "source_ids": [],
        })
    return out


def _career_timeline_for(person_id, pid=False):
    rows = [pos for pos in positions if pos["person_id"] == person_id]
    rows.sort(key=lambda x: x.get("start_date", "9999"))
    tl = []
    for r in rows:
        tl.append({
            "start": r.get("start_date", ""),
            "end": r.get("end_date", ""),
            "org": {o["id"]: o["name"] for o in organizations}.get(r.get("org_id", ""), ""),
            "title": r.get("title", ""),
            "level": "",
            "location": "淅川县" if r.get("org_id") in (1, 2, 3) else "南阳市",
            "system": "discipline" if "纪委" in r.get("title", "") else ("government" if "县" in r.get("title", "") and "书记" not in r.get("title", "") else "party"),
            "rank": r.get("rank", ""),
            "is_key_promotion": r.get("title") in ("县委书记", "县委副书记、县长", "南阳市委常委"),
            "notes": r.get("note", ""),
            "confidence": "confirmed",
            "source_ids": [],
        })
    return tl


def _organizations_for(person):
    org_ids = {r["org_id"] for r in positions if r["person_id"] == person}
    return [
        {"name": o["name"], "org_type": o["type"], "level": o["level"], "parent": o["parent"], "location": o["location"], "role": "affiliated"}
        for o in organizations if o["id"] in org_ids
    ]


def write_person_json(p):
    fname = f"{TODAY}-河南省-南阳市-{p['current_post'].split('（')[0]}-{p['name']}.json"
    doc = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省", "city": "南阳市", "region": "淅川县",
            "job": p["current_post"], "task_id": "henan_淅川县", "time_focus": "2015-2026",
        },
        "identity": {
            "person_id": f'henan_xichuan_{p["name"]}',
            "name": p["name"], "aliases": [],
            "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""), "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""), "study_type": "unknown"}],
            "party_join": p.get("party_join", ""), "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""),
            "administrative_rank": "正县级" if p["id"] in (2,) else ("副厅级" if p["id"] in (1,) else "副县级"),
            "as_of": AS_OF, "is_current_confirmed": True, "source_ids": [],
        },
        "career_timeline": _career_timeline_for(p["id"]),
        "organizations": _organizations_for(p["id"]),
        "relationships": _relationships_for(p["id"]),
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if p["id"] in (2, 3, 8) else "system_expert",
            "systems_experience": [],
            "geographic_pattern": [],
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格基于公开报道与出席活动推断，非私人心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": f"未发现针对{p['name']}的公开纪律处分或负面报道（截至{AS_OF}）", "date": AS_OF, "confidence": "unverified", "source_ids": []}
        ],
        "source_register": _source_register(),
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "出生/籍贯与早年完整履历未能从公开渠道核实",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的出生年/籍贯/加入党与参加工作具体年份？",
                "why_it_matters": "人物去重与跨地区网络匹配需要稳定身份键。",
                "suggested_queries": [f"{p['name']} 简历 出生 籍贯", f"{p['name']} 任前公示"],
                "last_attempted": "2026-08-06",
            }
        ],
    }
    out = PERSONS_DIR / fname
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Person JSON: {out.name}")
    return out


# ══════════════════════════════════════════════════════════════════════════
# Graph + DB build
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role:
        return "255,50,50"
    elif "县长" in role or "副县长" in role or "市长" in role:
        return "50,100,255"
    elif "纪委" in role or "监委" in role:
        return "255,165,0"
    elif "人大" in role:
        return "100,150,255"
    elif "政协" in role:
        return "100,200,100"
    else:
        return "100,100,100"


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "纪委" in t:
        return "255,220,180"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    else:
        return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>淅川县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{pos.get("start_date","")} — {pos.get("end_date","")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF: {GEXF_PATH}")


def build_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '', birthplace TEXT DEFAULT '', education TEXT DEFAULT '', party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '', current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT '');
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '', level TEXT DEFAULT '',
            parent TEXT DEFAULT '', location TEXT DEFAULT '');
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
            title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '');
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
            type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '');
    """)
    pcols = ["id", "name", "gender", "ethnicity", "birth", "birthplace", "education", "party_join", "work_start", "current_post", "current_org", "source"]
    for p in persons:
        conn.execute(f"INSERT INTO persons ({','.join(pcols)}) VALUES ({','.join('?' for _ in pcols)})", [p.get(c, "") for c in pcols])
    ocols = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        conn.execute(f"INSERT INTO organizations ({','.join(ocols)}) VALUES ({','.join('?' for _ in ocols)})", [o.get(c, "") for c in ocols])
    qcols = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        conn.execute(f"INSERT INTO positions ({','.join(qcols)}) VALUES ({','.join('?' for _ in qcols)})", [pos.get(c, "") for c in qcols])
    rcols = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        conn.execute(f"INSERT INTO relationships ({','.join(rcols)}) VALUES ({','.join('?' for _ in rcols)})", [r.get(c, "") for c in rcols])
    conn.commit()
    conn.close()
    print(f"✅ DB: {DB_PATH}")


def build():
    build_db()
    build_gexf()
    # Core leaders get person graph JSON
    for pid in (1, 2):  # 张志强, 郭广全
        p = next(x for x in persons if x["id"] == pid)
        write_person_json(p)


if __name__ == "__main__":
    build()