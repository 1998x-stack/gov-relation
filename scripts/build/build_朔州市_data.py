#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 朔州市 (Shuozhou City), 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_朔州市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - zh.wikipedia.org/wiki/朔州市 — leadership table, historical list
  - zh.wikipedia.org/wiki/吴秀玲 — mayor biography
  - zh.wikipedia.org/wiki/姜四清 — predecessor biography
  - zh.wikipedia.org/wiki/熊燕斌 — predecessor biography (corrupt, removed)
  - district.ce.cn/newarea/sddy/202412/12/t20241212_39232983.shtml — 王帅红 appointment notice

Confidence notes:
  - 王帅红: confirmed via official appointment notice (中国经济网, 2024-12-12)
  - 吴秀玲: confirmed via Wikipedia and in office since 2021-02
  - 张立新: Wikipedia as 政协主席
  - 人大主任: marked as 空缺 (vacant) per Wikipedia
  - Detailed career timelines for 王帅红 (pre-2024) are incomplete — he previously served as 山西省纪委副书记、省监委副主任, 省生态环境厅党组书记厅长
  - 吴秀玲's early career details are not publicly available on Wikipedia
  - Web search (Exa) rate-limited during this investigation; direct Wikipedia/WebFetch used instead
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
SLUG = "朔州市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# Staging paths
DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")

# Canonical destinations (relative to repo root)
REPO_ROOT = Path(STAGING).parent.parent.parent
CANONICAL_DB = str(REPO_ROOT / "data" / "database" / f"{SLUG}_network.db")
CANONICAL_GEXF = str(REPO_ROOT / "data" / "graph" / f"{SLUG}_network.gexf")
CANONICAL_BUILD = str(REPO_ROOT / f"build_{SLUG}_data.py")
CANONICAL_PERSONS = REPO_ROOT / "data" / "persons"

# ── Persons ────────────────────────────────────────────────────────────────────

persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ═════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "王帅红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年8月",
        "birthplace": "山西省稷山县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共朔州市委员会",
        "source": "https://zh.wikipedia.org/wiki/朔州市 | http://district.ce.cn/newarea/sddy/202412/12/t20241212_39232983.shtml"
    },
    {
        "id": 2,
        "name": "吴秀玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年1月",
        "birthplace": "山西省文水县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "朔州市人民政府",
        "source": "https://zh.wikipedia.org/wiki/吴秀玲"
    },
    {
        "id": 3,
        "name": "张立新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年9月",
        "birthplace": "山西省定襄县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政协主席",
        "current_org": "朔州市政协",
        "source": "https://zh.wikipedia.org/wiki/朔州市"
    },

    # ═════════════════════════════════════════════════════════════════════
    # Recent Predecessors (Key Figures)
    # ═════════════════════════════════════════════════════════════════════

    {
        "id": 4,
        "name": "姜四清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年2月",
        "birthplace": "湖北省天门市",
        "education": "中南财经大学/中国人民大学/东北师范大学",
        "party_join": "1998年",
        "work_start": "",
        "current_post": "前任市委书记（调离）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/姜四清"
    },
    {
        "id": 5,
        "name": "熊燕斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年9月",
        "birthplace": "江西省丰城市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原市委书记（被查）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/熊燕斌"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中国共产党朔州市委员会", "type": "党委", "level": "地级", "location": "山西省朔州市"},
    {"id": 2, "name": "朔州市人民政府", "type": "政府", "level": "地级", "location": "山西省朔州市"},
    {"id": 3, "name": "朔州市人民代表大会常务委员会", "type": "人大", "level": "地级", "location": "山西省朔州市"},
    {"id": 4, "name": "中国人民政治协商会议朔州市委员会", "type": "政协", "level": "地级", "location": "山西省朔州市"},
    {"id": 5, "name": "山西省生态环境厅", "type": "政府", "level": "省级", "location": "山西省太原市"},
    {"id": 6, "name": "中共山西省纪律检查委员会", "type": "党委", "level": "省级", "location": "山西省太原市"},
    {"id": 7, "name": "山西省发展和改革委员会", "type": "政府", "level": "省级", "location": "山西省太原市"},
    {"id": 8, "name": "中共阳泉市委员会", "type": "党委", "level": "地级", "location": "山西省阳泉市"},
    {"id": 9, "name": "山西省地质勘查局", "type": "事业单位", "level": "省级", "location": "山西省太原市"},
]

# ── Positions ──────────────────────────────────────────────────────────────────

positions = [
    # 王帅红
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2024-12", "end": "至今", "rank": "正厅级", "note": "2024年12月任"},
    {"person_id": 1, "org_id": 6, "title": "副书记、省监委副主任", "start": "", "end": "2024-12", "rank": "", "note": "此前担任"},
    {"person_id": 1, "org_id": 5, "title": "党组书记、厅长", "start": "", "end": "2024-12", "rank": "正厅级", "note": "履新前任"},

    # 吴秀玲
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "2021-02", "end": "至今", "rank": "正厅级", "note": "第十四届全国人大代表"},

    # 张立新
    {"person_id": 3, "org_id": 4, "title": "政协主席", "start": "2021-02", "end": "至今", "rank": "正厅级"},

    # 姜四清
    {"person_id": 4, "org_id": 1, "title": "市委书记", "start": "2021-08", "end": "2024-12", "rank": "正厅级"},
    {"person_id": 4, "org_id": 8, "title": "市委书记", "start": "2020-03", "end": "2021-08", "rank": "正厅级"},
    {"person_id": 4, "org_id": 7, "title": "主任", "start": "2017-05", "end": "2020-03", "rank": "正厅级"},

    # 熊燕斌
    {"person_id": 5, "org_id": 1, "title": "市委书记", "start": "2021-02", "end": "2021-08", "rank": "正厅级", "note": "2022年被双开"},
    {"person_id": 5, "org_id": 2, "title": "市长", "start": "2019-12", "end": "2021-02", "rank": "正厅级"},
    {"person_id": 5, "org_id": 9, "title": "副局长", "start": "2021-09", "end": "2022-02", "rank": "正厅级", "note": "调任后不久被查"},
]

# ── Relationships ──────────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "市委书记与市长搭班关系",
        "overlap_org": "中共朔州市委员会/朔州市人民政府",
        "overlap_period": "2024-12至今",
    },
    {
        "person_a": 4, "person_b": 2,
        "type": "superior_subordinate",
        "context": "前任市委书记与现任市长搭班关系",
        "overlap_org": "中共朔州市委/朔州市人民政府",
        "overlap_period": "2021-08至2024-12",
    },
    {
        "person_a": 5, "person_b": 2,
        "type": "predecessor_successor",
        "context": "熊燕斌在离开市长职位后，吴秀玲接任市长",
        "overlap_org": "朔州市人民政府",
        "overlap_period": "2021-02",
    },
    {
        "person_a": 5, "person_b": 4,
        "type": "predecessor_successor",
        "context": "熊燕斌为市委书记，姜四清接任",
        "overlap_org": "中共朔州市委",
        "overlap_period": "2021-08",
    },
    {
        "person_a": 4, "person_b": 1,
        "type": "predecessor_successor",
        "context": "姜四清离职后王帅红接任市委书记",
        "overlap_org": "中共朔州市委",
        "overlap_period": "2024-12",
    },
]

# ── GEXF Builder ───────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_gexf(persons, orgs, positions, rels, output_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent (China-Gov-Network skill)</creator>')
    lines.append('    <description>朔州市（山西省地级市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="current_post" type="string"/>')
    lines.append('      <attribute id="3" title="province" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        name = p["name"]
        post = p.get("current_post", "")
        corg = p.get("current_org", "")

        # Color by role
        if "书记" in post and "市委" in corg:
            c = "255,50,50"   # red — party secretary
            sz = "20.0"
        elif "市长" in post or "区长" in post or "县长" in post:
            c = "50,100,255"  # blue — government head
            sz = "15.0"
        elif "政协" in post:
            c = "200,200,255"  # light blue for legislative
            sz = "12.0"
        else:
            c = "100,100,100"
            sz = "12.0"

        lines.append(f'      <node id="p{p["id"]}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(post)}"/>')
        lines.append('          <attvalue for="3" value="山西省"/>')
        lines.append('        </attvalues>')
        r, g, b = c.split(",")
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
    }
    for o in orgs:
        oc = org_colors.get(o["type"], "200,200,200")
        sz = "8.0"
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="山西省"/>')
        lines.append('        </attvalues>')
        r, g, b = oc.split(",")
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        title = pos.get("title", "")
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person <-> Person (relationship)
    for r in rels:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── Database Builder ───────────────────────────────────────────────────────────

def build_db(persons, orgs, positions, rels, output_path):
    import sqlite3
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    conn = sqlite3.connect(output_path)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE if not exists persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE if not exists organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE if not exists positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE if not exists relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p.get("education", ""), p["party_join"],
                   p.get("work_start", ""), p["current_post"], p["current_org"],
                   p["source"]))
    for o in orgs:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o.get("org", ""),
                   o.get("parent", ""), o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"],
                   pos.get("start", ""), pos.get("end", ""),
                   pos.get("rank", ""), pos.get("note", "")))
    for r in rels:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"],
                   r.get("context", ""), r.get("overlap_org", ""),
                   r.get("overlap_period", "")))

    conn.commit()
    conn.close()


# ── Person JSON Writers ────────────────────────────────────────────────────────

def write_person_json_wang_shuaihong(persons_dir):
    import json
    data = {
        "schema_version": "1.0",
        "generated_at": "2026-07-26",
        "investigation_scope": {
            "province": "山西省",
            "city": "朔州市",
            "region": "朔州市",
            "job": "市委书记",
            "task_id": "shanxi_朔州市",
            "time_focus": "2024-至今"
        },
        "identity": {
            "person_id": "shuozhou-wang_shuaihong",
            "name": "王帅红",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1973年8月",
            "birthplace": "山西省稷山县",
            "native_place": "山西省稷山县",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "王帅红_1973-08",
                "name_birthplace": "王帅红_稷山县",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "中共朔州市委书记",
            "current_org": "中共朔州市委员会",
            "administrative_rank": "正厅级",
            "as_of": "2026-07-26",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": [
            {
                "start": "2024-12",
                "end": "至今",
                "org": "中共朔州市委",
                "title": "市委书记",
                "level": "正厅级",
                "location": "山西省朔州市",
                "system": "party",
                "rank": "正厅级",
                "is_key_promotion": True,
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "start": "",
                "end": "2024-12",
                "org": "山西省生态环境厅",
                "title": "党组书记、厅长",
                "level": "正厅级",
                "location": "山西省太原市",
                "system": "government",
                "rank": "正厅级",
                "is_key_promotion": False,
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "start": "",
                "end": "2024-12",
                "org": "中共山西省纪律检查委员会",
                "title": "副书记、省监委副主任",
                "level": "副厅级",
                "location": "山西省太原市",
                "system": "discipline",
                "rank": "副厅级",
                "is_key_promotion": False,
                "confidence": "plausible",
                "source_ids": ["S001"]
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "（2020年前完整履历待查）",
                "confidence": "unverified",
                "notes": "王帅红公开履历仅有近5年记录，早期经历（教育、基层任职、纪检系统成长路径）未找到"
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "吴秀玲",
                "person_id": "shuozhou-wu_xiuling",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "现任朔州市委书记和市长，直接搭班合作",
                "overlap_org": "朔州市",
                "overlap_period": "2024-12至今",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "姜四清",
                "person_id": "shuozhou-jiang_siqing",
                "relationship_type": "predecessor_successor",
                "strength": "strong",
                "evidence": "姜四清卸任朔州市委书记后，王A帅红接任",
                "overlap_org": "中共朔州市委",
                "overlap_period": "2024-12",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "governance_record": [
            {
                "period": "生态环保厅长任期",
                "domain": "environment",
                "achievement_or_event": "担任山西省生态环境厅党组书记",
                "role_in_event": "厅长",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "professional_profile": {
            "primary_specializations": ["纪检监察", "生态环境"],
            "secondary_specializations": [],
            "career_pattern": "provincial_department",
            "systems_experience": ["party", "government", "discipline"],
            "geographic_pattern": ["山西省->太原->朔州"],
            "promotion_velocity": {
                "summary": "从省纪委副书记到市委书记为平级调整",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "尚无足够的公开言行资料判断工作风格"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现新违纪举报或负面记录",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "王帅红任朔州市委书记 — 中国经济网",
                "url": "http://district.ce.cn/newarea/sddy/202412/12/t20241212_39232983.shtml",
                "publisher": "中国经济网",
                "published_at": "2024-12-12",
                "accessed_at": "2026-07-26",
                "source_type": "media",
                "reliability": "high",
                "notes": "官方任命报道，包含经济履历概述"
            },
            {
                "id": "S002",
                "title": "朔州市 Wikipedia 页面",
                "url": "https://zh.wikipedia.org/wiki/朔州市",
                "publisher": "Wikipedia",
                "published_at": "",
                "accessed_at": "2026-07-26",
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "确认市委书记现任为王帅红"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "2020年前逾20年履历完全空白"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "2020年前王帅红的完整履历",
                "why_it_matters": "无法判断其职业起点、晋升路径、系统经验和政绩表现",
                "suggested_queries": [
                    "王帅红 简历 工作经历",
                    "王帅红 朔州",
                    "山西省纪委 王帅红"
                ],
                "last_attempted": "2026-07-26"
            }
        ]
    }
    fname = f"{TODAY}-山西省-朔州市-市委书记-王帅红.json"
    with open(persons_dir / fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return fname


def write_person_json_wu_xiuling(persons_dir):
    import json
    data = {
        "schema_version": "1.0",
        "generated_at": "2026-07-26",
        "investigation_scope": {
            "province": "山西省",
            "city": "朔州市",
            "region": "朔州市",
            "job": "市长",
            "task_id": "shanxi_朔州市",
            "time_focus": "2021-至今"
        },
        "identity": {
            "person_id": "shuozhou-wu_xiuling",
            "name": "吴秀玲",
            "aliases": [],
            "gender": "女",
            "ethnicity": "汉族",
            "birth": "1971年1月",
            "birthplace": "山西省文水县",
            "native_place": "山西省文水县",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "吴秀玲_1971-01",
                "name_birthplace": "吴秀玲_文水县",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "朔州市人民政府市长",
            "current_org": "朔州市人民政府",
            "administrative_rank": "正厅级",
            "as_of": "2026-07-26",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": [
            {
                "start": "2021-02",
                "end": "至今",
                "org": "朔州市人民政府",
                "title": "市长",
                "level": "正厅级",
                "location": "山西省朔州市",
                "system": "government",
                "rank": "正厅级",
                "is_key_promotion": True,
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "（2021年前履历待查）",
                "confidence": "unverified",
                "notes": "公开资料未找到吴秀玲在2021年接任市长前的完整履历"
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "王帅红",
                "person_id": "shuozhou_wang_shuaihong",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "现任市长，与市委书记直接搭班",
                "overlap_org": "朔州市",
                "overlap_period": "2024-12至今",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "姜四清",
                "person_id": "shuozhou_jiang_siqing",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "姜四清任市委书记同期间，吴秀玲为市长",
                "overlap_org": "朔州市",
                "overlap_period": "2021-08至2024-12",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "熊燕斌",
                "person_id": "shuozhou_xiong_yanbin",
                "relationship_type": "predecessor_successor",
                "strength": "medium",
                "evidence": "熊燕斌市长离任后，吴秀玲接任市长",
                "overlap_org": "朔州市人民政府",
                "overlap_period": "2021-02",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": ["山西省->朔州市"],
            "promotion_velocity": {
                "summary": "2021年2月任朔州市市长（正厅级），晋升路径待查",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "公开履历缺乏足够信息评估",
                    "confidence": "unverified"
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "缺乏资料，无法评估"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现任何负面记录或违纪信号",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "吴秀玲 Wikipedia 页面",
                "url": "https://zh.wikipedia.org/wiki/吴秀玲",
                "publisher": "Wikipedia",
                "published_at": "",
                "accessed_at": "2026-07-26",
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "确认基本信息、现任市长、前任关系"
            },
            {
                "id": "S002",
                "title": "朔州市 Wikipedia 页面",
                "url": "https://zh.wikipedia.org/wiki/朔州市",
                "publisher": "Wikipedia",
                "published_at": "",
                "accessed_at": "2026-07-26",
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "确认市长身份"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "2021年前大段履历完全空白"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "吴秀玲在2021年之前的职业履历",
                "why_it_matters": "无法判断其职业经验、成长路径和晋升背景",
                "suggested_queries": [
                    "吴秀玲 简历 朔州",
                    "吴秀玲 任职经历",
                    "吴秀玲 文水县 工作"
                ],
                "last_attempted": "2026-07-26"
            }
        ]
    }
    fname = f"{TODAY}-山西省-朔州市-市长-吴秀玲.json"
    with open(persons_dir / fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return fname


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from datetime import datetime

    print("=" * 60)
    print(f" 朔州市 (Shuozhou) leadership network build")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f" Date: {now_str}")
    print("=" * 60)

    build_db(persons, organizations, positions, relationships, DB_PATH)
    build_gexf(persons, organizations, positions, relationships, GEXF_PATH)

    persons_dir = Path(STAGING)
    wang_file = write_person_json_wang_shuaihong(persons_dir)
    wu_file = write_person_json_wu_xiuling(persons_dir)

    print(f"\nStaging results in {STAGING}:")
    print(f"  Database:   {DB_PATH}")
    print(f"  GEXF:       {GEXF_PATH}")
    print(f"  Person JS 1: {wang_file}")
    print(f"  Person JS 2: {wu_file}")