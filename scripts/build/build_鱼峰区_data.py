#!/usr/bin/env python3
"""Build 鱼峰区 (Yufeng District, Liuzhou, Guangxi) leadership network.

Generated: 2026-07-22
Sources: yfq.gov.cn leadership pages and news articles (Feb-Jul 2026)
"""

import json
import os
import sqlite3
from datetime import datetime

# =========================================================================
# Constants
# =========================================================================
AS_OF = "2026-07-22"
STAGING = os.path.dirname(os.path.abspath(__file__))
PERSONS_DIR = os.path.join(STAGING, "persons")
DB_PATH = os.path.join(STAGING, "鱼峰区_network.db")
GEXF_PATH = os.path.join(STAGING, "鱼峰区_network.gexf")

NOW = AS_OF.replace("-", "")

# =========================================================================
# Source Register
# =========================================================================
source_register = [
    {
        "id": "S001",
        "title": "鱼峰区主要领导聚焦民生热点，一线推进工作落实",
        "url": "http://www.yfq.gov.cn/zwgk/qzfld/qz/zyjhhhd/202605/t20260513_3750832.shtml",
        "publisher": "魅力鱼峰（鱼峰区政府）",
        "published_at": "2026-05-13",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirms 钟云 as 区委书记, 毛国勇 as 副区长"
    },
    {
        "id": "S002",
        "title": "锚定'双过半' 聚力抓落实——鱼峰区召开2026年二季度经济发展调度会",
        "url": "http://www.yfq.gov.cn/zwgk/qzfld/qz/zyjhhhd/202605/t20260507_3748426.shtml",
        "publisher": "魅力鱼峰（鱼峰区政府）",
        "published_at": "2026-05-07",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirms 钟云 (区委书记), 毛国勇 (区委副书记、区长), 梁太福 (区人大常委会主任), 覃汉棠 (区政协主席)"
    },
    {
        "id": "S003",
        "title": "鱼峰区与北师大携手推进科学幼小衔接全域改革",
        "url": "http://www.yfq.gov.cn/zwgk/qzfld/qz/zyjhhhd/202604/t20260428_3745874.shtml",
        "publisher": "柳州市鱼峰区人民政府",
        "published_at": "2026-04-28",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirms 毛国勇 (区长), 梁融静 (副区长)"
    },
    {
        "id": "S004",
        "title": "心系基层 情暖新春——鱼峰区开展春节前走访慰问活动",
        "url": "http://www.yfq.gov.cn/zwgk/qzfld/qz/zyjhhhd/202602/t20260217_3724854.shtml",
        "publisher": "魅力鱼峰（鱼峰区政府）",
        "published_at": "2026-02-15",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirms 钟云 (区委书记), 毛国勇 (区长), 王海涛 (区委常委、区委办主任), 陈刚 (副区长、公安鱼峰分局局长)"
    },
    {
        "id": "S005",
        "title": "鱼峰区召开'四大攻坚'行动工作调度会",
        "url": "http://www.yfq.gov.cn/zwgk/qzfld/qz/zyjhhhd/202604/t20260409_3740135.shtml",
        "publisher": "魅力鱼峰（鱼峰区政府）",
        "published_at": "2026-04-09",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirms 钟云, 毛国勇, 梁太福, 覃汉棠 as 四家班子领导"
    },
    {
        "id": "S006",
        "title": "鱼峰区集中整治群众身边不正之风和腐败问题暨化解历史矛盾工作调度会召开",
        "url": "http://www.yfq.gov.cn/zwgk/qzfld/qz/zyjhhhd/202605/t20260508_3749011.shtml",
        "publisher": "魅力鱼峰（鱼峰区政府）",
        "published_at": "2026-05-08",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirms 钟云, 毛国勇"
    },
    {
        "id": "S007",
        "title": "鱼峰区：走访服务重点企业，为复工复产注入强心剂",
        "url": "http://www.yfq.gov.cn/zwgk/qzfld/qz/zyjhhhd/202602/t20260227_3726143.shtml",
        "publisher": "魅力鱼峰（鱼峰区政府）",
        "published_at": "2026-02-27",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirms 钟云, 毛国勇"
    },
    {
        "id": "S008",
        "title": "陈震到鱼峰公安分局、白沙镇调研督导基层社会治理工作",
        "url": "http://www.yfq.gov.cn/xwzx/tpxw/202607/t20260722_3775837.shtml",
        "publisher": "鱼峰区政府",
        "published_at": "2026-07-22",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "Mentions 陈震 as active leader"
    },
    {
        "id": "S009",
        "title": "罗长青到白沙镇督导水库安全度汛工作",
        "url": "http://www.yfq.gov.cn/xwzx/tpxw/202607/t20260722_3775835.shtml",
        "publisher": "鱼峰区政府",
        "published_at": "2026-07-22",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirms 罗长青 as 区政协党组书记、主席提名人选"
    },
    {
        "id": "S010",
        "title": "鱼峰区政府领导之窗（区政府领导页面）",
        "url": "http://www.yfq.gov.cn/zwgk/qzfld/qz/",
        "publisher": "鱼峰区政府",
        "published_at": "2026",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "区政府领导名录页"
    },
]

# =========================================================================
# Person Data
# =========================================================================
persons = [
    {
        "id": 1,
        "name": "钟云",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鱼峰区委书记",
        "current_org": "中共柳州市鱼峰区委员会",
        "source": "http://www.yfq.gov.cn/zwgk/qzfld/qz/zyjhhhd/202605/t20260513_3750832.shtml"
    },
    {
        "id": 2,
        "name": "毛国勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鱼峰区委副书记、区长",
        "current_org": "鱼峰区人民政府",
        "source": "http://www.yfq.gov.cn/zwgk/qzfld/qz/zyjhhhd/202605/t20260507_3748426.shtml"
    },
    {
        "id": 3,
        "name": "梁太福",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鱼峰区人大常委会主任",
        "current_org": "鱼峰区人大常委会",
        "source": "http://www.yfq.gov.cn/zwgk/qzfld/qz/zyjhhhd/202605/t20260507_3748426.shtml"
    },
    {
        "id": 4,
        "name": "覃汉棠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鱼峰区政协主席",
        "current_org": "鱼峰区政协",
        "source": "http://www.yfq.gov.cn/zwgk/qzfld/qz/zyjhhhd/202605/t20260507_3748426.shtml"
    },
    {
        "id": 5,
        "name": "王海涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鱼峰区委常委、区委办主任",
        "current_org": "中共柳州市鱼峰区委员会",
        "source": "http://www.yfq.gov.cn/zwgk/qzfld/qz/zyjhhhd/202602/t20260217_3724854.shtml"
    },
    {
        "id": 6,
        "name": "梁融静",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鱼峰区副区长",
        "current_org": "鱼峰区人民政府",
        "source": "http://www.yfq.gov.cn/zwgk/qzfld/qz/zyjhhhd/202604/t20260428_3745874.shtml"
    },
    {
        "id": 7,
        "name": "陈刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鱼峰区副区长、公安鱼峰分局局长",
        "current_org": "鱼峰区人民政府",
        "source": "http://www.yfq.gov.cn/zwgk/qzfld/qz/zyjhhhd/202602/t20260217_3724854.shtml"
    },
    {
        "id": 8,
        "name": "陈震",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鱼峰区领导（调研基层治理）",
        "current_org": "鱼峰区人民政府",
        "source": "http://www.yfq.gov.cn/xwzx/tpxw/202607/t20260722_3775837.shtml"
    },
    {
        "id": 9,
        "name": "罗长青",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鱼峰区政协党组书记、主席提名人选",
        "current_org": "鱼峰区政协",
        "source": "http://www.yfq.gov.cn/xwzx/tpxw/202607/t20260722_3775835.shtml"
    },
]

# =========================================================================
# Organization Data
# =========================================================================
organizations = [
    {"id": 1, "name": "中共柳州市鱼峰区委员会", "type": "党委", "level": "县处级", "parent": "中共柳州市委员会", "location": "柳州市鱼峰区"},
    {"id": 2, "name": "鱼峰区人民政府", "type": "政府", "level": "县处级", "parent": "柳州市人民政府", "location": "柳州市鱼峰区"},
    {"id": 3, "name": "鱼峰区人大常委会", "type": "人大", "level": "县处级", "parent": "柳州市人大常委会", "location": "柳州市鱼峰区"},
    {"id": 4, "name": "鱼峰区政协", "type": "政协", "level": "县处级", "parent": "柳州市政协", "location": "柳州市鱼峰区"},
    {"id": 5, "name": "公安鱼峰分局", "type": "政府", "level": "乡科级", "parent": "柳州市公安局", "location": "柳州市鱼峰区"},
]

# =========================================================================
# Position Data
# =========================================================================
positions = [
    # 钟云 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "鱼峰区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "Confirmed as of Feb-Jul 2026"},
    # 毛国勇 - 区委副书记、区长
    {"person_id": 2, "org_id": 1, "title": "鱼峰区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "鱼峰区区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 梁太福 - 区人大常委会主任
    {"person_id": 3, "org_id": 3, "title": "鱼峰区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 覃汉棠 - 区政协主席
    {"person_id": 4, "org_id": 4, "title": "鱼峰区政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 王海涛 - 区委常委、区委办主任
    {"person_id": 5, "org_id": 1, "title": "鱼峰区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "区委办主任", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    # 梁融静 - 副区长
    {"person_id": 6, "org_id": 2, "title": "鱼峰区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管教育"},
    # 陈刚 - 副区长兼公安分局局长
    {"person_id": 7, "org_id": 2, "title": "鱼峰区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "公安鱼峰分局局长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    # 陈震 - 区领导
    {"person_id": 8, "org_id": 2, "title": "鱼峰区领导", "start_date": "", "end_date": "present", "rank": "", "note": "2026年7月调研基层社会治理"},
    # 罗长青 - 政协党组书记
    {"person_id": 9, "org_id": 4, "title": "鱼峰区政协党组书记、主席提名人选", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026年7月督导水库安全度汛"},
]

# =========================================================================
# Relationship Data
# =========================================================================
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "钟云为区委书记、毛国勇为区长，组成鱼峰区党政正职搭档", "overlap_org": "鱼峰区党政班子", "overlap_period": "至2026年"},
    {"person_a": 1, "person_b": 3, "type": "同届领导", "context": "钟云（区委书记）和梁太福（区人大常委会主任）共同出席区经济发展调度会", "overlap_org": "鱼峰区四家班子", "overlap_period": "至2026年"},
    {"person_a": 1, "person_b": 4, "type": "同届领导", "context": "钟云和覃汉棠（区政协主席）共同出席区经济发展调度会", "overlap_org": "鱼峰区四家班子", "overlap_period": "至2026年"},
    {"person_a": 2, "person_b": 3, "type": "选举关系", "context": "毛国勇与梁太福在区经济发展调度会上同台", "overlap_org": "鱼峰区四家班子", "overlap_period": "至2026年"},
    {"person_a": 2, "person_b": 4, "type": "同届领导", "context": "毛国勇与覃汉棠共同出席区经济发展调度会", "overlap_org": "鱼峰区四家班子", "overlap_period": "至2026年"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "王海涛作为区委常委、区委办主任，直接服务区委书记钟云", "overlap_org": "中共鱼峰区委", "overlap_period": "至2026年"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "梁融静作为副区长在区长毛国勇领导下工作", "overlap_org": "鱼峰区人民政府", "overlap_period": "至2026年"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "陈刚作为副区长在区长毛国勇领导下工作", "overlap_org": "鱼峰区人民政府", "overlap_period": "至2026年"},
    {"person_a": 6, "person_b": 7, "type": "同事", "context": "梁融静与陈刚同为鱼峰区副区长", "overlap_org": "鱼峰区人民政府", "overlap_period": "至2026年"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "罗长青作为政协党组书记在区委书记钟云领导下工作", "overlap_org": "鱼峰区四家班子", "overlap_period": "2026年"},
]


# =========================================================================
# Helper: xml escape
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# =========================================================================
# Person JSON Generator
# =========================================================================
def make_person_json(person, timeline, relationships_list):
    """Generate a person graph JSON."""
    # Build source IDs used
    source_ids = set()
    for entry in timeline:
        for sid in entry.get("source_ids", []):
            source_ids.add(sid)
    for rel in relationships_list:
        for sid in rel.get("source_ids", []):
            source_ids.add(sid)

    filtered_sources = [s for s in source_register if s["id"] in source_ids]

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "柳州市",
            "region": "鱼峰区",
            "job": person["current_post"],
            "task_id": "guangxi_鱼峰区",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": f"yufeng_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级正职" if "书记" in person["current_post"] and "副" not in person["current_post"] or "区长" in person["current_post"] else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S002"]
        },
        "career_timeline": timeline,
        "organizations": [{"org_id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "plausible", "source_ids": []}
        ],
        "source_register": filtered_sources,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "缺少出生年月、籍贯、教育背景和完整履历信息"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年月、籍贯、教育背景",
                "why_it_matters": "核心身份信息，用于人员去重和履历分析",
                "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任前公示", f"{person['name']} 百度百科"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['name']}的完整履历（此前任职经历）",
                "why_it_matters": "了解晋升路径和工作交集",
                "suggested_queries": [f"{person['name']} 曾任", f"{person['name']} 任职经历"],
                "last_attempted": AS_OF
            }
        ]
    }


# =========================================================================
# Main Build
# =========================================================================
def build():
    os.makedirs(PERSONS_DIR, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""),
                     r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    gexf_lines = []
    gexf_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    gexf_lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    gexf_lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    gexf_lines.append('    <creator>Gov-Relation Research Agent</creator>')
    gexf_lines.append('    <description>鱼峰区领导班子关系网络</description>')
    gexf_lines.append('  </meta>')
    gexf_lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    gexf_lines.append('    <attributes class="node">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="current_post" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="current_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="birth" type="string"/>')
    gexf_lines.append('      <attribute id="4" title="source" type="string"/>')
    gexf_lines.append('    </attributes>')

    # Edge attributes
    gexf_lines.append('    <attributes class="edge">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="context" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    gexf_lines.append('    </attributes>')

    # Nodes — persons
    gexf_lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        post = p.get("current_post", "")
        is_secretary = "书记" in post and "副" not in post.split("、")[0] if "、" not in post else "书记" in post and not post.startswith("副")
        is_mayor = "区长" in post and "副" not in post
        is_discipline = "纪委" in post

        if is_secretary:
            color = "200,30,30"
        elif is_mayor:
            color = "30,100,200"
        elif is_discipline:
            color = "255,165,0"
        else:
            color = "100,100,100"

        size = "20.0" if (is_secretary or is_mayor) else "12.0"
        shape = "square" if is_secretary else ("circle" if is_mayor else "triangle")

        gexf_lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="person"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        gexf_lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        gexf_lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        gexf_lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        gexf_lines.append(f'        <viz:size value="{size}"/>')
        gexf_lines.append(f'        <viz:shape value="{shape}"/>')
        gexf_lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        otype = o["type"]
        if otype == "党委":
            ocolor = "255,200,200"
        elif otype == "政府":
            ocolor = "200,200,255"
        elif otype == "人大":
            ocolor = "200,255,255"
        elif otype == "政协":
            ocolor = "255,240,200"
        elif otype == "纪委":
            ocolor = "255,200,150"
        elif otype == "开发区":
            ocolor = "200,255,200"
        elif otype == "乡镇/街道":
            ocolor = "255,255,200"
        else:
            ocolor = "200,200,200"

        gexf_lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="organization"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        gexf_lines.append(f'        <viz:size value="8.0"/>')
        gexf_lines.append(f'        <viz:shape value="hexagon"/>')
        gexf_lines.append('      </node>')

    gexf_lines.append('    </nodes>')

    # Edges
    gexf_lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        gexf_lines.append(
            f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"] + 100000}" label="{esc(pos["title"])}" weight="1.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append('          <attvalue for="0" value="worked_at"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        gexf_lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="relationship"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        gexf_lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        gexf_lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')

    gexf_lines.append('    </edges>')
    gexf_lines.append('  </graph>')
    gexf_lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(gexf_lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person graph JSONs ──
    # 钟云 timeline
    zhongyun_timeline = [
        {"start": "2026年以前", "end": "present", "org": "中共柳州市鱼峰区委员会", "title": "鱼峰区委书记",
         "level": "县处级正职", "location": "广西柳州", "system": "party", "rank": "县处级正职",
         "is_key_promotion": True, "notes": "已知自2026年2月起以区委书记身份公开活动",
         "confidence": "confirmed", "source_ids": ["S001", "S002", "S004"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到钟云任鱼峰区委书记前的完整履历",
         "confidence": "unverified", "source_ids": []},
    ]
    zhongyun_relationships = [
        {"person": "毛国勇", "person_id": "yufeng_毛国勇", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "钟云为区委书记、毛国勇为区长，党政搭档",
         "overlap_org": "鱼峰区党政班子",
         "overlap_period": "至2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "梁太福", "person_id": "yufeng_梁太福", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "同时任职于鱼峰区四家班子",
         "overlap_org": "鱼峰区四家班子",
         "overlap_period": "至2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "覃汉棠", "person_id": "yufeng_覃汉棠", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "同时任职于鱼峰区四家班子",
         "overlap_org": "鱼峰区四家班子",
         "overlap_period": "至2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    zhongyun_json = make_person_json(persons[0], zhongyun_timeline, zhongyun_relationships)
    zhongyun_path = os.path.join(PERSONS_DIR, f"{NOW}-广西壮族自治区-柳州市-区委书记-钟云.json")
    with open(zhongyun_path, "w", encoding="utf-8") as f:
        json.dump(zhongyun_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {zhongyun_path}")

    # 毛国勇 timeline
    maoguoyong_timeline = [
        {"start": "2026年以前", "end": "present", "org": "鱼峰区人民政府", "title": "鱼峰区区长",
         "level": "县处级正职", "location": "广西柳州", "system": "government", "rank": "县处级正职",
         "is_key_promotion": True, "notes": "同时担任区委副书记. Known自2026年2月起以区长身份公开活动",
         "confidence": "confirmed", "source_ids": ["S002", "S003", "S004"]},
        {"start": "unknown", "end": "2026", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到毛国勇任鱼峰区区长前的完整履历",
         "confidence": "unverified", "source_ids": []},
    ]
    maoguoyong_relationships = [
        {"person": "钟云", "person_id": "yufeng_钟云", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "毛国勇为区委副书记、区长，与区委书记钟云党政搭档",
         "overlap_org": "鱼峰区党政班子",
         "overlap_period": "至2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "梁融静", "person_id": "yufeng_梁融静", "relationship_type": "superior_subordinate",
         "strength": "medium",
         "evidence": "梁融静作为副区长在区长毛国勇领导下工作",
         "overlap_org": "鱼峰区人民政府",
         "overlap_period": "至2026年",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "陈刚", "person_id": "yufeng_陈刚", "relationship_type": "superior_subordinate",
         "strength": "medium",
         "evidence": "陈刚作为副区长在区长毛国勇领导下工作",
         "overlap_org": "鱼峰区人民政府",
         "overlap_period": "至2026年",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    maoguoyong_json = make_person_json(persons[1], maoguoyong_timeline, maoguoyong_relationships)
    maoguoyong_path = os.path.join(PERSONS_DIR, f"{NOW}-广西壮族自治区-柳州市-区长-毛国勇.json")
    with open(maoguoyong_path, "w", encoding="utf-8") as f:
        json.dump(maoguoyong_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {maoguoyong_path}")

    print("\nBuild complete.")


if __name__ == "__main__":
    build()
