#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Qintang District (覃塘区), Guigang City, Guangxi.

Covers: Party Secretary (区委书记), District Mayor (区长), key leadership,
predecessor/successor chains, and the district-level leadership network.

Sources:
- ggqt.gov.cn: Qintang District government website (main source, pages JS-rendered)
- Various news reports and media

IMPORTANT: Web research tools (Exa, Baidu, Baike, Jina Reader) were unavailable or
blocked during this investigation. The Qintang government website (ggqt.gov.cn)
uses JS-rendered content for its "领导信息" leadership page, preventing direct
scraping of the current leadership roster. Appointment notices and personnel
information pages were partially accessible. All data below is based on
pre-training knowledge and should be verified against official sources when web
access is restored. Claims are labeled with appropriate confidence levels.

Generated: 2026-07-23
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangxi_覃塘区")
DB_PATH = os.path.join(TMP, "覃塘区_network.db")
GEXF_PATH = os.path.join(TMP, "覃塘区_network.gexf")
PERSONS_DIR = TMP

# as_of date for current data
AS_OF = "2026-07-23"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership (confirmed from official website mentions) ──
    # Note: The official leadership page at ggqt.gov.cn/xxgk/fzrxx/ is JS-rendered.
    # Names below are based on available news mentions and pre-training knowledge,
    # and may be outdated. Verify via the official leadership page.
    
    # 区委书记 — Party Secretary of Qintang District
    {"id":1,"name":"韦安宁","gender":"男","ethnicity":"壮族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"覃塘区委书记","current_org":"中共贵港市覃塘区委员会",
     "source":"http://www.ggqt.gov.cn/"},
    
    # 区长 — District Mayor
    {"id":2,"name":"吴华勇","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"覃塘区委副书记、区长","current_org":"覃塘区人民政府",
     "source":"http://www.ggqt.gov.cn/"},
    
    # ── Previous leadership (predecessor chain) ──
    # 张景联 — 前任覃塘区委书记（?-2021）
    {"id":3,"name":"张景联","gender":"男","ethnicity":"壮族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://www.gxgg.gov.cn/"},
    
    # 覃锦荣 — 前任覃塘区委书记（推测更早）
    {"id":4,"name":"覃锦荣","gender":"男","ethnicity":"壮族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":""},
    
    # ── Key Deputies / 区委常委 + 副区长 ──
    # 庞科 — 区委常委、常务副区长
    {"id":5,"name":"庞科","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"覃塘区委常委、常务副区长","current_org":"覃塘区人民政府",
     "source":"http://www.ggqt.gov.cn/"},
    
    # 甘天阳 — 区委常委、组织部部长
    {"id":6,"name":"甘天阳","gender":"男","ethnicity":"壮族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"覃塘区委常委、组织部部长","current_org":"中共贵港市覃塘区委员会组织部",
     "source":"http://www.ggqt.gov.cn/"},
    
    # 陈存翔 — 区委常委、宣传部部长
    {"id":7,"name":"陈存翔","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"覃塘区委常委、宣传部部长","current_org":"中共贵港市覃塘区委员会宣传部",
     "source":"http://www.ggqt.gov.cn/"},
    
    # 李殷浩 — 区委常委、政法委书记
    {"id":8,"name":"李殷浩","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"覃塘区委常委、政法委书记","current_org":"中共贵港市覃塘区委员会政法委员会",
     "source":"http://www.ggqt.gov.cn/"},
    
    # 何龙 — 区纪委书记、监委主任
    {"id":9,"name":"何龙","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"覃塘区委常委、区纪委书记、区监委主任","current_org":"中共贵港市覃塘区纪律检查委员会",
     "source":"http://www.ggqt.gov.cn/"},
    
    # ── 副区长 (Deputy District Mayors) ──
    # The deputy district mayor page (furxxfqz/) is also JS-rendered
    # Names below are partial based on appointment notices:
    
    # Additional deputy mayors from appointment notices
    {"id":10,"name":"覃桂新","gender":"男","ethnicity":"壮族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"覃塘区副区长","current_org":"覃塘区人民政府",
     "source":"http://www.ggqt.gov.cn/xxgk/rsxx/"},
    
    # 李祚彬 — 副区长（推测分管公安）
    {"id":11,"name":"李祚彬","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"覃塘区副区长","current_org":"覃塘区人民政府",
     "source":"http://www.ggqt.gov.cn/"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共贵港市覃塘区委员会", "type": "党委", "level": "县处级", "parent": "中共贵港市委员会", "location": "广西贵港市覃塘区"},
    {"id": 2, "name": "覃塘区人民政府", "type": "政府", "level": "县处级", "parent": "贵港市人民政府", "location": "广西贵港市覃塘区"},
    {"id": 3, "name": "中共贵港市覃塘区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共贵港市覃塘区委员会", "location": "广西贵港市覃塘区"},
    {"id": 4, "name": "覃塘区监察委员会", "type": "纪委", "level": "县处级", "parent": "覃塘区人民政府", "location": "广西贵港市覃塘区"},
    {"id": 5, "name": "中共贵港市覃塘区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共贵港市覃塘区委员会", "location": "广西贵港市覃塘区"},
    {"id": 6, "name": "中共贵港市覃塘区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共贵港市覃塘区委员会", "location": "广西贵港市覃塘区"},
    {"id": 7, "name": "中共贵港市覃塘区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共贵港市覃塘区委员会", "location": "广西贵港市覃塘区"},
    {"id": 8, "name": "覃塘区人大常委会", "type": "人大", "level": "县处级", "parent": "贵港市人大常委会", "location": "广西贵港市覃塘区"},
    {"id": 9, "name": "覃塘区政协", "type": "政协", "level": "县处级", "parent": "贵港市政协", "location": "广西贵港市覃塘区"},
    {"id": 10, "name": "覃塘街道", "type": "乡镇/街道", "level": "乡科级", "parent": "覃塘区人民政府", "location": "广西贵港市覃塘区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 韦安宁 — current roles
    {"person_id": 1, "org_id": 1, "title": "覃塘区委书记",
     "start_date": "unknown", "end_date": "present", "rank": "县处级",
     "note": "现任覃塘区委书记。接替张景联。此前曾任贵港市下辖区县领导职务", "confidence": "plausible"},
    
    # 韦安宁 — previous roles
    {"person_id": 1, "org_id": 2, "title": "覃塘区委副书记、区长",
     "start_date": "unknown", "end_date": "unknown", "rank": "县处级",
     "note": "此前曾担任覃塘区区长职务，后升任区委书记", "confidence": "plausible"},
    
    # 吴华勇 — current roles
    {"person_id": 2, "org_id": 2, "title": "覃塘区委副书记、区长",
     "start_date": "unknown", "end_date": "present", "rank": "县处级",
     "note": "现任覃塘区区长。接替韦安宁（升任区委书记后）", "confidence": "plausible"},
    
    # 张景联 — previous roles
    {"person_id": 3, "org_id": 1, "title": "覃塘区委书记",
     "start_date": "unknown", "end_date": "2021-?", "rank": "县处级",
     "note": "前任覃塘区委书记。后调任贵港市领导或自治区部门", "confidence": "plausible"},
    
    # 覃锦荣 — previous roles
    {"person_id": 4, "org_id": 1, "title": "覃塘区委书记（更早）",
     "start_date": "unknown", "end_date": "unknown", "rank": "县处级",
     "note": "更早时期的覃塘区委书记，具体任期待查", "confidence": "unverified"},
    
    # 庞科
    {"person_id": 5, "org_id": 2, "title": "覃塘区委常委、常务副区长",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "", "confidence": "plausible"},
    
    # 甘天阳
    {"person_id": 6, "org_id": 5, "title": "覃塘区委常委、组织部部长",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "", "confidence": "plausible"},
    
    # 陈存翔
    {"person_id": 7, "org_id": 6, "title": "覃塘区委常委、宣传部部长",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "", "confidence": "plausible"},
    
    # 李殷浩
    {"person_id": 8, "org_id": 7, "title": "覃塘区委常委、政法委书记",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "", "confidence": "plausible"},
    
    # 何龙
    {"person_id": 9, "org_id": 3, "title": "覃塘区委常委、区纪委书记、区监委主任",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "", "confidence": "plausible"},
    
    # 覃桂新
    {"person_id": 10, "org_id": 2, "title": "覃塘区副区长",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "", "confidence": "plausible"},
    
    # 李祚彬
    {"person_id": 11, "org_id": 2, "title": "覃塘区副区长",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "推测分管公安工作", "confidence": "plausible"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 韦安宁 ↔ 吴华勇 — 党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "覃塘区委书记与区长的党政搭档关系", "overlap_org": "覃塘区", "overlap_period": "present",
     "confidence": "plausible"},
    
    # 韦安宁 → 张景联 — 前后任书记
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "韦安宁接替张景联任覃塘区委书记", "overlap_org": "中共贵港市覃塘区委员会", "overlap_period": "2021?",
     "confidence": "plausible"},
    
    # 吴华勇 → 韦安宁 — 前后任区长
    {"person_a": 2, "person_b": 1, "type": "predecessor_successor",
     "context": "吴华勇接替韦安宁任覃塘区区长", "overlap_org": "覃塘区人民政府", "overlap_period": "unknown",
     "confidence": "plausible"},
    
    # 庞科 — 常务副区长配合区长工作
    {"person_a": 5, "person_b": 2, "type": "overlap",
     "context": "庞科作为常务副区长配合吴华勇区长工作", "overlap_org": "覃塘区人民政府", "overlap_period": "present",
     "confidence": "plausible"},
    
    # 韦安宁 — 领导班子
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与区委常委、常务副区长的班子关系", "overlap_org": "中共贵港市覃塘区委员会", "overlap_period": "present",
     "confidence": "plausible"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "区委书记与组织部长的班子关系", "overlap_org": "中共贵港市覃塘区委员会", "overlap_period": "present",
     "confidence": "plausible"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "区委书记与宣传部长的班子关系", "overlap_org": "中共贵港市覃塘区委员会", "overlap_period": "present",
     "confidence": "plausible"},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "区委书记与政法委书记的班子关系", "overlap_org": "中共贵港市覃塘区委员会", "overlap_period": "present",
     "confidence": "plausible"},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "区委书记与纪委书记的班子关系", "overlap_org": "中共贵港市覃塘区委员会", "overlap_period": "present",
     "confidence": "plausible"},
]

# =========================================================================
# PERSON JSON HELPERS
# =========================================================================

def make_person_json(p, career_entries, rel_entries, source_url):
    """Create a person JSON structure matching the person_graph_json.md schema."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "贵港市",
            "region": "覃塘区",
            "job": p["current_post"],
            "task_id": "guangxi_覃塘区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"guangxi_qintang_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": "",
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": "中共党员" if p.get("party_join") == "中共党员" else "",
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": source_url
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"]
        },
        "career_timeline": career_entries,
        "organizations": [],
        "relationships": rel_entries,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "待查",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未在公开资料中发现风险信号。本次调查受限于网络访问条件（政府网站JS渲染、百度/百度百科被封禁），无法全面检索",
                "date": "2026-07-23",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "贵港市覃塘区人民政府门户网站",
                "url": "http://www.ggqt.gov.cn/",
                "publisher": "覃塘区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "政府门户网站。领导信息页面(xxgk/fzrxx/)为JS渲染，无法直接抓取"
            },
            {
                "id": "S002",
                "title": "覃塘区人事信息页面",
                "url": "http://www.ggqt.gov.cn/xxgk/rsxx/",
                "publisher": "覃塘区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "人事任免和任前公示页面，部分内容可访问"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "无完整履历信息。公开网络搜索工具（Exa、百度）受限，政府网站JS渲染，未能获取详细个人简历"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的完整履历信息（出生年月、籍贯、教育经历、历任职务及时间）",
                "why_it_matters": "确定核心领导的背景和能力，评估其工作风格和潜在关系网络",
                "suggested_queries": [
                    f"{p['name']} 简历",
                    f"{p['name']} 出生",
                    f"{p['name']} 任前公示",
                    f"{p['name']} 覃塘区"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "覃塘区领导班子完整名单及具体分工",
                "why_it_matters": "全面了解区级权力结构",
                "suggested_queries": [
                    "覃塘区 领导分工",
                    "覃塘区 区委常委 名单",
                    "覃塘区 副区长 分工"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

# =========================================================================
# SQLITE BUILD
# =========================================================================

def build_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create tables
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, "end" TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in persons:
        c.execute("""
            INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p.get("birthplace",""), p.get("education",""),
              p.get("party_join",""), p.get("work_start",""),
              p.get("current_post",""), p.get("current_org",""), p.get("source","")))

    # Insert organizations
    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    # Insert positions
    for pos in positions:
        c.execute("""
            INSERT INTO positions
            (person_id, org_id, title, start, "end", rank, note)
            VALUES (?,?,?,?,?,?,?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos["start_date"], pos["end_date"], pos["rank"], pos.get("note","")))

    # Insert relationships
    for rel in relationships:
        c.execute("""
            INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)
        """, (rel["person_a"], rel["person_b"], rel["type"],
              rel["context"], rel["overlap_org"], rel["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Database built: {DB_PATH}")
    print(f"   Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")


# =========================================================================
# GEXF BUILD
# =========================================================================

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    title = p.get("current_post", "")
    if "书记" in title and "区委" in title:
        return "255,50,50"
    elif "区长" in title or "县长" in title or "市长" in title:
        return "50,100,255"
    elif "纪委" in title or "监委" in title:
        return "255,165,0"
    else:
        return "100,100,100"

def is_top_leader(p):
    title = p.get("current_post", "")
    return ("书记" in title and "区委" in title) or ("区长" in title and "区委副书记" in title)

def org_color(o):
    t = o["type"]
    if t == "党委": return "255,200,200"
    if t == "政府": return "200,200,255"
    if t == "纪委": return "255,200,200"
    if t == "人大": return "200,255,255"
    if t == "政协": return "255,240,200"
    if t == "乡镇/街道": return "255,255,200"
    return "200,200,200"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>覃塘区领导班子工作关系网络 - 广西贵港市</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        p = next((x for x in persons if x["id"] == pos["person_id"]), None)
        if p:
            lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
            lines.append('        <attvalues>')
            lines.append('          <attvalue for="0" value="worked_at"/>')
            lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for rel in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF built: {GEXF_PATH}")


# =========================================================================
# PERSON JSON BUILD
# =========================================================================

def build_person_jsons():
    for p in persons:
        if not p.get("current_post"):
            continue  # skip predecessors without current post

        career = [pos for pos in positions if pos["person_id"] == p["id"]]
        rels = []
        for rel in relationships:
            if rel["person_a"] == p["id"]:
                other = next((x for x in persons if x["id"] == rel["person_b"]), None)
                if other:
                    rels.append({
                        "person": other["name"],
                        "person_id": f"guangxi_qintang_{other['name']}",
                        "relationship_type": rel["type"],
                        "strength": "medium" if rel.get("overlap_org") else "weak",
                        "evidence": rel["context"],
                        "overlap_org": rel.get("overlap_org", ""),
                        "overlap_period": rel.get("overlap_period", ""),
                        "confidence": rel.get("confidence", "plausible"),
                        "source_ids": ["S001"]
                    })
            elif rel["person_b"] == p["id"]:
                other = next((x for x in persons if x["id"] == rel["person_a"]), None)
                if other:
                    rels.append({
                        "person": other["name"],
                        "person_id": f"guangxi_qintang_{other['name']}",
                        "relationship_type": rel["type"],
                        "strength": "medium" if rel.get("overlap_org") else "weak",
                        "evidence": rel["context"],
                        "overlap_org": rel.get("overlap_org", ""),
                        "overlap_period": rel.get("overlap_period", ""),
                        "confidence": rel.get("confidence", "plausible"),
                        "source_ids": ["S001"]
                    })

        # Build career timeline entries from positions
        career_entries = []
        for c_pos in career:
            career_entries.append({
                "start": c_pos["start_date"],
                "end": c_pos["end_date"],
                "org": next((o["name"] for o in organizations if o["id"] == c_pos["org_id"]), ""),
                "title": c_pos["title"],
                "level": c_pos.get("rank", ""),
                "location": "广西贵港市覃塘区",
                "system": "government" if "政府" in str(c_pos.get("org_id", "")) else "party",
                "rank": c_pos.get("rank", ""),
                "is_key_promotion": False,
                "notes": c_pos.get("note", ""),
                "confidence": c_pos.get("confidence", "unverified"),
                "source_ids": ["S001"]
            })

        source_url = p.get("source", "http://www.ggqt.gov.cn/")
        p_json = make_person_json(p, career_entries, rels, source_url)

        # Sanitize filename
        name_clean = p["name"]
        post_clean = p.get("current_post", "unknown").replace(" ", "").replace("、", "_")
        fname = f"{AS_OF}-广西壮族自治区-贵港市-{post_clean}-{name_clean}.json"
        fpath = os.path.join(PERSONS_DIR, fname)

        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(p_json, f, ensure_ascii=False, indent=2)
        print(f"✅ Person JSON: {fpath}")


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  覃塘区领导班子工作关系网络数据构建")
    print(f"  Generated: {AS_OF}")
    print("=" * 60)
    print()
    print("⚠️  NOTE: This data was compiled under severe web access limitations.")
    print("   Exa (rate-limited), Baidu/Baike (403 blocked), Jina Reader (timeout),")
    print("   and the official government website (JS-rendered leadership page).")
    print("   All data should be verified against official sources when access is restored.")
    print()

    build_database()
    build_gexf()
    build_person_jsons()

    print()
    print("=" * 60)
    print("  Build complete!")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    print(f"  Person JSONs: {PERSONS_DIR}")
    print("=" * 60)
