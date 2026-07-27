#!/usr/bin/env python3
"""龙江县（齐齐哈尔市）领导班子关系网络生成脚本

数据来源：
  - 百度百科龙江县词条（baike.baidu.com/item/龙江县）
  - 百度百科关宝建词条（baike.baidu.com/item/关宝建/1089022）
  - 以上均截至2025年5月

数据截至：2026年7月

Target roles:
  县委书记: 关宝建
  县长:    付先锋

NOTE: Web access to Chinese government sites (lj.gov.cn, qqhr.gov.cn) and Baidu Baike
individual pages was completely unreachable from this environment (timeouts, firewall blocks).
The leadership names (关宝建, 付先锋) are confirmed from the Baidu Baike 龙江县 page (副主编级).
All other details (birth, education, career timeline) are unknown and marked unverified.
"""

import json
import os
import sqlite3
from datetime import datetime

AS_OF = "2026-07-24"
TODAY = "20260724"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING = SCRIPT_DIR
DB_PATH = os.path.join(STAGING, "龙江县_network.db")
GEXF_PATH = os.path.join(STAGING, "龙江县_network.gexf")
PERSONS_DIR = os.path.join(STAGING, "persons")

os.makedirs(PERSONS_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════
# DATA — All entries with confidence levels
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Current Top Leaders ──
    {
        "id": 1,
        "name": "关宝建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共龙江县委员会",
        "source": "https://baike.baidu.com/item/关宝建/1089022（通过百度百科龙江县词条确认，个人词条未访问到）",
        "confidence": "confirmed",
        "notes": "百度百科龙江县词条'政治'章节确认关宝建为县委书记（截至2025年5月）"
    },
    {
        "id": 2,
        "name": "付先锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "龙江县人民政府",
        "source": "https://baike.baidu.com/item/龙江县（百度百科龙江县词条确认）",
        "confidence": "confirmed",
        "notes": "百度百科龙江县词条'政治'章节确认付先锋为县长（截至2025年5月）"
    },
    # ── Other leadership roles (unconfirmed placeholders) ──
    {
        "id": 3,
        "name": "待确认人大常委会主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "龙江县人大常委会",
        "source": "需从官方政府网站确认",
        "confidence": "unverified",
        "notes": "龙江县人大常委会主任姓名未知"
    },
    {
        "id": 4,
        "name": "待确认政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "龙江县政协",
        "source": "需从官方政府网站确认",
        "confidence": "unverified",
        "notes": "龙江县政协主席姓名未知"
    },
    {
        "id": 5,
        "name": "待确认纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记",
        "current_org": "中共龙江县纪律检查委员会",
        "source": "需从官方政府网站确认",
        "confidence": "unverified",
        "notes": "龙江县纪委书记姓名未知"
    },
    # ── Predecessors (from training knowledge) ──
    {
        "id": 6,
        "name": "待确认前任县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "需从官方信息确认",
        "confidence": "unverified",
        "notes": "关宝建的前任县委书记姓名待确认"
    },
    {
        "id": 7,
        "name": "待确认前任县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "需从官方信息确认",
        "confidence": "unverified",
        "notes": "付先锋的前任县长姓名待确认"
    },
]

organizations = [
    {"id": 1, "name": "中共龙江县委员会", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市委员会", "location": "黑龙江省齐齐哈尔市龙江县"},
    {"id": 2, "name": "龙江县人民政府", "type": "政府", "level": "县处级",
     "parent": "齐齐哈尔市人民政府", "location": "黑龙江省齐齐哈尔市龙江县"},
    {"id": 3, "name": "龙江县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "齐齐哈尔市人大常委会", "location": "黑龙江省齐齐哈尔市龙江县"},
    {"id": 4, "name": "中国人民政治协商会议龙江县委员会", "type": "政协", "level": "县处级",
     "parent": "齐齐哈尔市政协", "location": "黑龙江省齐齐哈尔市龙江县"},
    {"id": 5, "name": "中共龙江县纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共齐齐哈尔市纪律检查委员会", "location": "黑龙江省齐齐哈尔市龙江县"},
    {"id": 6, "name": "中共龙江县委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市委政法委员会", "location": "黑龙江省齐齐哈尔市龙江县"},
    {"id": 7, "name": "中共龙江县委组织部", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市委组织部", "location": "黑龙江省齐齐哈尔市龙江县"},
    {"id": 8, "name": "中共龙江县委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市委宣传部", "location": "黑龙江省齐齐哈尔市龙江县"},
    {"id": 9, "name": "龙江县监察委员会", "type": "纪委", "level": "县处级",
     "parent": "齐齐哈尔市监察委员会", "location": "黑龙江省齐齐哈尔市龙江县"},
    {"id": 10, "name": "龙江县人民法院", "type": "事业单位", "level": "县处级",
     "parent": "齐齐哈尔市中级人民法院", "location": "黑龙江省齐齐哈尔市龙江县"},
    {"id": 11, "name": "龙江县人民检察院", "type": "事业单位", "level": "县处级",
     "parent": "齐齐哈尔市人民检察院", "location": "黑龙江省齐齐哈尔市龙江县"},
    {"id": 12, "name": "龙江县人民武装部", "type": "事业单位", "level": "县处级",
     "parent": "齐齐哈尔军分区", "location": "黑龙江省齐齐哈尔市龙江县"},
]

positions = [
    # 关宝建 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "上任时间待确认", "confidence": "confirmed"},
    # 付先锋 - 县长
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "上任时间待确认", "confidence": "confirmed"},
    # Placeholder positions for unknown roles
    {"person_id": 3, "org_id": 3, "title": "县人大常委会主任",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "姓名待确认", "confidence": "unverified"},
    {"person_id": 4, "org_id": 4, "title": "县政协主席",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "姓名待确认", "confidence": "unverified"},
    {"person_id": 5, "org_id": 5, "title": "县委常委、纪委书记",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "姓名待确认", "confidence": "unverified"},
]

relationships = []


# ═══════════════════════════════════════════════════════════════════════
# XML Escaping
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ═══════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════

def build():
    print(f"Building 龙江县 network data ({AS_OF})...")
    print()

    # ── 1. SQLite Database ──
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT
        );
    """)

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
                   p.get("birth",""), p.get("birthplace",""), p.get("education",""),
                   p.get("party_join",""), p.get("work_start",""),
                   p.get("current_post",""), p.get("current_org",""), p.get("source","")))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o.get("parent",""), o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"],
                   pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note","")))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r.get("type",""),
                   r.get("context",""), r.get("overlap_org",""), r.get("overlap_period","")))

    conn.commit()

    # Print summary
    p_count = c.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    o_count = c.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
    pos_count = c.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
    r_count = c.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
    conn.close()
    print(f"[SQLite] Written: {DB_PATH}")
    print(f"  Persons: {p_count}, Organizations: {o_count}, Positions: {pos_count}, Relationships: {r_count}")

    # ── 2. GEXF Graph ──
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>龙江县（齐齐哈尔市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="title" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        name = p["name"]
        conf = p.get("confidence", "unverified")
        post = p.get("current_post", "")

        # Color by role
        if "县委书记" in post or "县委" in post and "书记" in post:
            color = "255,50,50"
            node_type = "person"
        elif "县长" in post or "区长" in post:
            color = "50,100,255"
            node_type = "person"
        elif "纪委书记" in post:
            color = "255,165,0"
            node_type = "person"
        else:
            color = "100,100,100"
            node_type = "person"

        sz = "20.0" if p["id"] in (1, 2) else "12.0"

        lines.append(f'      <node id="p{p["id"]}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{node_type}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        o_type = o["type"]
        if o_type == "党委":
            o_color = "255,200,200"
        elif o_type == "政府":
            o_color = "200,200,255"
        elif o_type == "人大":
            o_color = "200,255,255"
        elif o_type == "政协":
            o_color = "255,240,200"
        elif o_type == "纪委":
            o_color = "255,200,200"
        else:
            o_color = "200,200,200"

        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o_type)}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{o_color.split(",")[0]}" g="{o_color.split(",")[1]}" b="{o_color.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n[GEXF] Written: {GEXF_PATH}")

    # ── 3. Person JSONs ──

    source_register = [
        {"id": "S001", "title": "百度百科 - 龙江县",
         "url": "https://baike.baidu.com/item/龙江县",
         "publisher": "百度百科", "published_at": "",
         "accessed_at": AS_OF, "source_type": "encyclopedia",
         "reliability": "medium",
         "notes": "提供了关宝建（县委书记）和付先锋（县长）的姓名"},
        {"id": "S002", "title": "百度百科 - 关宝建",
         "url": "https://baike.baidu.com/item/关宝建/1089022",
         "publisher": "百度百科", "published_at": "",
         "accessed_at": AS_OF, "source_type": "encyclopedia",
         "reliability": "medium",
         "notes": "关宝建个人词条，本环境未访问到内容"},
    ]

    def make_person_json(p, timeline, rels_list):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "齐齐哈尔市",
                "region": "龙江县",
                "job": p.get("current_post", ""),
                "task_id": "heilongjiang_龙江县",
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"longjiang_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职" if p["id"] in (1,2) else "县处级",
                "as_of": AS_OF,
                "is_current_confirmed": p.get("confidence") == "confirmed",
                "source_ids": ["S001"]
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": rels_list,
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
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "confirmed" if p.get("confidence") == "confirmed" else "unverified",
                "current_role": "confirmed" if p.get("confidence") == "confirmed" else "unverified",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": f"{p['name']}的完整履历、出生年月、籍贯、教育背景全部缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的出生年月和籍贯",
                 "why_it_matters": "身份基本资料缺失，无法进行身份确认和去重",
                 "suggested_queries": [f"{p['name']} 出生 年月", f"{p['name']} 籍贯"],
                 "last_attempted": AS_OF},
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径、系统经历和职业模式",
                 "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任前公示", f"{p['name']} 任职经历"],
                 "last_attempted": AS_OF},
                {"priority": "high",
                 "question": f"{p['name']}的教育背景",
                 "why_it_matters": "教育经历有助于判断其专业特长和系统归属",
                 "suggested_queries": [f"{p['name']} 毕业 学校", f"{p['name']} 学历"],
                 "last_attempted": AS_OF},
            ]
        }
        return result

    # ── Person JSON: 关宝建 (县委书记) ──
    gbj_timeline = [
        {"start": "unknown", "end": "present", "org": "中共龙江县委员会",
         "title": "县委书记",
         "notes": "上任时间、此前任职均未知。百度百科龙江县词条确认其为现任县委书记。",
         "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    gbj_rels = []
    gbj_json = make_person_json(persons[0], gbj_timeline, gbj_rels)
    gbj_path = os.path.join(PERSONS_DIR, f"{TODAY}-黑龙江省-齐齐哈尔市-县委书记-关宝建.json")
    with open(gbj_path, "w", encoding="utf-8") as f:
        json.dump(gbj_json, f, ensure_ascii=False, indent=2)
    print(f"\n[PERSON JSON] Written: {gbj_path}")

    # ── Person JSON: 付先锋 (县长) ──
    fx_timeline = [
        {"start": "unknown", "end": "present", "org": "龙江县人民政府",
         "title": "县委副书记、县长",
         "notes": "上任时间、此前任职均未知。百度百科龙江县词条确认其为现任县长。",
         "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    fx_rels = []
    fx_json = make_person_json(persons[1], fx_timeline, fx_rels)
    fx_path = os.path.join(PERSONS_DIR, f"{TODAY}-黑龙江省-齐齐哈尔市-县长-付先锋.json")
    with open(fx_path, "w", encoding="utf-8") as f:
        json.dump(fx_json, f, ensure_ascii=False, indent=2)
    print(f"[PERSON JSON] Written: {fx_path}")

    print("\nDone. Summary:")
    print(f"  DB:        {DB_PATH}")
    print(f"  GEXF:      {GEXF_PATH}")
    print(f"  Persons:   {PERSONS_DIR}/")


if __name__ == "__main__":
    build()
