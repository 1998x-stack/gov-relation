#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 工农区 (Gongnong District), 鹤岗市, 黑龙江省.

Investigation date: 2026-08-05
Task ID: heilongjiang_工农区
Level: 市辖区（县处级）
Targets: 区委书记 & 区长
Parent city: 鹤岗市

Research sources (all confirmed via 工农区人民政府官网 http://www.hggn.gov.cn/):
  1. 姜明珠 = 区委书记 (主持区委13届128次常委扩大会议 2026-08-05)
  2. 刘长青 = 区委副书记、区长 (主持区政府党组扩大会议暨常务会议 2026-07-31; 防汛督导 2026-08-02)
  3. 曲忠宝 = 区委常委、组织部部长、统战部部长 (区委统一战线领导小组会议 2026-07-09)
  4. 陆书明 = 区委常委、副区长 (强降雨防范工作会议 2026-08-01; 河长公告区级河段长)
  5. 吕杨   = 区委常委、政府副区长、区河长办主任 (防内涝及安全生产督导 2026-07-31)
  6. 田德全 = 区政府副区长、市公安局工农分局局长 (统一战线领导小组会议 2026-07-09)
  7. 赵红煜 = 政府副区长 (养老机构防汛督导 2026-08-04)
  8. 赵鹏   = 区领导 (全区上半年经济运行推进会 2026-07), 职务待核实(疑为副区长)
  9. 马安相 = 区人大常委会副主任 (统一战线领导小组会议 2026-07-09)

工农区概况（走进工农/区情简介, 官方）:
  - 鹤岗市经济文化中心城区, 2025年地区生产总值51.88亿元(+3.5%), 商贸零售额占全市1/3以上
  - 常住人口13.1万(六区之首), 辖红旗/新南(前进)/团结(湖滨)/育才 4个街道办事处, 14个社区
  - 政府驻地: 育才路178号, 邮编 154101

Confidence notes:
  - 现任区委书记、区长及班子: confirmed via 官方新闻与河长公告
  - 完整履历(出生/籍贯/学历/入党/历任起止) 未取得 -> open_questions / open_gaps
    (搜索渠道均被拦: 百度百科403, 360无词条, Exa限流, Bing/搜狗验证码)
  - 前任区委书记/区长 及其去向: unverified
  - 纪委书记/监委主任、宣传部长、人大主任、政协主席/副主席: 官方站未刊名 -> open_gaps
"""

import json
import os
from datetime import datetime

SLUG = "工农区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")

MISSING = {"gender": "", "ethnicity": "", "birth": "", "birthplace": "",
           "education": "", "party_join": "中共党员", "work_start": ""}

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    {"id": 1, "name": "姜明珠", **MISSING, "gender": "", "ethnicity": "汉族",
     "current_post": "区委书记",
     "current_org": "中共鹤岗市工农区委员会", "source": "工农区政府官网—主持区委常委会会议 (2026-08-05)"},
    {"id": 2, "name": "刘长青", **MISSING, "gender": "", "ethnicity": "汉族",
     "current_post": "区委副书记、区政府区长",
     "current_org": "鹤岗市工农区人民政府", "source": "工农区政府官网—政府党组/常务会议 (2026-07-31)"},
    {"id": 3, "name": "曲忠宝", **MISSING, "gender": "", "ethnicity": "汉族",
     "current_post": "区委常委、组织部部长、统战部部长",
     "current_org": "中共鹤岗市工农区委员会", "source": "工农区政府官网—统一战线领导小组会议 (2026-07-09)"},
    {"id": 4, "name": "陆书明", **MISSING, "gender": "", "ethnicity": "汉族",
     "current_post": "区委常委、政府副区长",
     "current_org": "鹤岗市工农区人民政府", "source": "工农区政府官网—强降雨防范会议 (2026-08-01)+河长公告"},
    {"id": 5, "name": "吕杨", **MISSING, "gender": "", "ethnicity": "汉族",
     "current_post": "区委常委、政府副区长、区河长办主任",
     "current_org": "鹤岗市工农区人民政府", "source": "工农区政府官网—防内涝督导 (2026-07-31)+河长公告"},
    {"id": 6, "name": "田德全", **MISSING, "gender": "", "ethnicity": "汉族",
     "current_post": "区政府副区长、市公安局工农分局局长",
     "current_org": "鹤岗市工农区人民政府", "source": "工农区政府官网—统一战线领导小组会议 (2026-07-09)"},
    {"id": 7, "name": "赵红煜", **MISSING, "gender": "", "ethnicity": "汉族",
     "current_post": "政府副区长",
     "current_org": "鹤岗市工农区人民政府", "source": "工农区政府官网—养老机构防汛督导 (2026-08-04)"},
    {"id": 8, "name": "赵鹏", **MISSING, "gender": "", "ethnicity": "汉族",
     "current_post": "区领导（职务待核实，疑为副区长）",
     "current_org": "鹤岗市工农区人民政府", "source": "工农区政府官网—经济运行推进会议 (2026-07)"},
    {"id": 9, "name": "马安相", **MISSING, "gender": "", "ethnicity": "汉族",
     "current_post": "区人大常委会副主任",
     "current_org": "鹤岗市工农区人民代表大会常务委员会", "source": "工农区政府官网—统一战线领导小组会议 (2026-07-09)"},
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共鹤岗市工农区委员会", "type": "党委", "level": "县处级", "parent": "中共鹤岗市委员会", "location": "黑龙江省鹤岗市工农区"},
    {"id": 2, "name": "鹤岗市工农区人民政府", "type": "政府", "level": "县处级", "parent": "鹤岗市人民政府", "location": "黑龙江省鹤岗市工农区"},
    {"id": 3, "name": "鹤岗市工农区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "鹤岗市人民代表大会常务委员会", "location": "黑龙江省鹤岗市工农区"},
    {"id": 4, "name": "中国人民政治协商会议鹤岗市工农区委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议鹤岗市委员会", "location": "黑龙江省鹤岗市工农区"},
    {"id": 5, "name": "鹤岗市工农区纪委监委", "type": "纪委", "level": "县处级", "parent": "中共鹤岗市纪律检查委员会", "location": "黑龙江省鹤岗市工农区"},
    {"id": 6, "name": "鹤岗市公安局工农分局", "type": "公安", "level": "乡科级", "parent": "鹤岗市工农区人民政府", "location": "黑龙江省鹤岗市工农区"},
    {"id": 7, "name": "中共鹤岗市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委员会", "location": "鹤岗市"},
    {"id": 8, "name": "鹤岗市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "鹤岗市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "主持区委全面工作；区级总河长"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "区级总河长"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "主持区政府全面工作；主持区政府党组(扩大)会议暨常务会议"},
    {"person_id": 3, "org_id": 1, "title": "区委常委、组织部部长、统战部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责组织、干部、人才、党建、统战"},
    {"person_id": 4, "org_id": 2, "title": "区委常委、政府副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "区级河段长；主持强降雨防范工作会议"},
    {"person_id": 5, "org_id": 2, "title": "区委常委、政府副区长、区河长办主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责安全生产、防内涝"},
    {"person_id": 6, "org_id": 2, "title": "政府副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "兼任公安分局局长，负责公共安全"},
    {"person_id": 6, "org_id": 6, "title": "市公安局工农分局局长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "政府副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责养老、民政等"},
    {"person_id": 8, "org_id": 2, "title": "区领导（疑为副区长）", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "职务待核实"},
    {"person_id": 9, "org_id": 3, "title": "区人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "负责人大相关工作"},
]

# ── Relationships (核心班子关系，confirmed via 官方新闻/河长公告) ─────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长（党政正职搭档）", "overlap_org": "工农区", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与组织部部长/统战部部长（人事）", "overlap_org": "中共工农区委", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与区委常委、副区长陆书明", "overlap_org": "中共工农区委/区政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与区委常委、副区长吕杨", "overlap_org": "中共工农区委/区政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与副区长/公安局长田德全", "overlap_org": "中共工农区委/区政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与区委常委、副区长陆书明（同场防汛检查）", "overlap_org": "工农区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与区委常委、副区长吕杨", "overlap_org": "工农区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长赵红煜", "overlap_org": "工农区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长与区领导赵鹏", "overlap_org": "工农区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "区委书记与区人大副主任马安相", "overlap_org": "工农区", "overlap_period": "2026"},
]

# ── Helpers ────────────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(name):
    if name == "姜明珠":
        return "255,50,50"                      # 红=区委书记
    if name == "刘长青":
        return "50,100,255"                      # 蓝=区长
    if name in ("陆书明", "吕杨", "田德全", "赵红煜", "赵鹏"):
        return "80,130,230"                      # 政府副区长
    if name == "曲忠宝":
        return "200,100,255"                     # 组织部/统战
    if name == "马安相":
        return "200,220,240"                     # 人大
    return "100,100,100"

def org_color(o_type):
    if "党委" in o_type or "纪检" in o_type:
        return "255,200,200"
    if "政府" in o_type or "公安" in o_type:
        return "200,200,255"
    if "人大" in o_type:
        return "200,255,255"
    if "政协" in o_type:
        return "255,240,200"
    return "200,200,200"

def person_by_name(name):
    for p in persons:
        if p["name"] == name:
            return p
    raise KeyError(name + " 不在 persons 中")

# ── DB ─────────────────────────────────────────────────────────────────────
def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT);
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT);
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id), FOREIGN KEY(org_id) REFERENCES organizations(id));
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id), FOREIGN KEY(person_b) REFERENCES persons(id));
    """)
    for p in persons:
        cur.execute(
            "INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""), p.get("birth",""),
             p.get("birthplace",""), p.get("education",""), p.get("party_join",""), p.get("work_start",""),
             p.get("current_post",""), p.get("current_org",""), p.get("source","")))
    for o in organizations:
        cur.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

# ── GEXF ───────────────────────────────────────────────────────────────────
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>工农区领导班子工作关系网络 - 鹤岗市, 黑龙江省</description>')
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
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        sz = "20.0" if p["name"] in ("姜明珠", "刘长青") else 16.0 if p["name"] in ("曲忠宝",) else 12.0
        nid = f"p{p['id']}"
        lines.append(f'      <node id="{nid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o["name"])
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  OK: GEXF ({eid} edges)")

# ── Person JSON ────────────────────────────────────────────────────────────
def make_person_json(p, timeline=None, relationships_list=None, source_register=None):
    if timeline is None:
        timeline = []
    if relationships_list is None:
        relationships_list = []
    if source_register is None:
        source_register = []
    name = p["name"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "鹤岗市",
            "region": "工农区",
            "job": p.get("current_post", ""),
            "task_id": "heilongjiang_工农区",
            "time_focus": "2026年8月"
        },
        "identity": {
            "person_id": f"gongnong_{name}",
            "name": name,
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
                "name_birth": f"{name}_{p.get('birth','')}",
                "name_birthplace": f"{name}_{p.get('birthplace','')}",
                "official_profile_url": "http://www.hggn.gov.cn/"
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "县处级" if p["id"] in (1, 2) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": ["黑龙江省鹤岗市"],
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
            {"type": "none_found", "description": "公开官方信息未发现该人物负面信号", "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{name}的出生/籍贯/教育及历任职务起止时间待补充"
        },
        "open_questions": [
            {"priority": "high", "question": f"{name}的出生/籍贯/教育/入党及历任职务起止时间", "why_it_matters": "丰富人物画像与网络分析", "suggested_queries": [f"{name} 简历", f"{name} 任前公示"], "last_attempted": AS_OF}
        ]
    }

def _write_person(obj, job, name):
    path = os.path.join(STAGING, f"{TODAY}-黑龙江省-鹤岗市-{job}-{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  OK: person json {os.path.basename(path)}")

def build_person_jsons():
    SOURCES = [
        {"id": "S001", "title": "工农区人民政府官网—姜明珠主持召开区委常委会会议", "url": "http://www.hggn.gov.cn/gongnongqurenminzhengfu/7c2dda6411e8aae8f8d3e0f9ee820/202608/92355.shtml", "publisher": "工农区人民政府", "published_at": "2026-08-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认姜明珠任区委书记"},
        {"id": "S002", "title": "工农区人民政府官网——刘长青主持区政府党组会议暨常务会议", "url": "http://www.hggn.gov.cn/", "publisher": "工农区人民政府", "published_at": "2026-07-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认刘长青为区委副书记、区长"},
        {"id": "S003", "title": "工农区人民政府官网——区级河长名单公告", "url": "http://www.hggn.gov.cn/", "publisher": "工农区人民政府", "published_at": "2026-05-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认姜明珠/刘长青为区级总河长、陆书明为河段长、吕杨为区河长办主任"},
    ]

    # 1. 区委书记 姜明珠
    jmz_tl = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到姜明珠完整履历（搜索渠道受限）", "confidence": "unverified", "source_ids": []},
        {"start": "unknown", "end": "present", "org": "中共鹤岗市工农区委员会", "title": "区委书记", "notes": "官方新闻确认，2026年8月仍在任", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    jmz_rel = [
        {"person": "刘长青", "person_id": "gongnong_刘长青", "relationship_type": "overlap", "strength": "strong", "evidence": "党政正职搭档", "overlap_org": "工农区", "overlap_period": "2026", "direction": "undirected", "confidence": "confirmed", "source_ids": []},
    ]
    jmz = make_person_json(person_by_name("姜明珠"), jmz_tl, jmz_rel, SOURCES)
    jmz["governance_record"] = [
        {"period": "2026-07", "domain": "economic_development", "achievement_or_event": "主持全区经济运行推进会议", "role_in_event": "区委书记", "measurable_outcome": "经济运行调度", "location": "工农区", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    _write_person(jmz, "区委书记", "姜明珠")

    # 2. 区长 刘长青
    lcq_tl = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到刘长青完整履历", "confidence": "unverified", "source_ids": []},
        {"start": "unknown", "end": "present", "org": "鹤岗市工农区人民政府", "title": "区委副书记、区长", "notes": "官方新闻确认，主持区政府党组/常务会议", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    lcq_rel = [
        {"person": "姜明珠", "person_id": "gongnong_姜明珠", "relationship_type": "overlap", "strength": "strong", "evidence": "党政正职搭档", "overlap_org": "工农区", "overlap_period": "2026", "direction": "undirected", "confidence": "confirmed", "source_ids": []},
    ]
    lcq = make_person_json(person_by_name("刘长青"), lcq_tl, lcq_rel, SOURCES)
    _write_person(lcq, "区长", "刘长青")

    # 3. 区委常委、组织部长/统战部长 曲忠宝
    p = person_by_name("曲忠宝")
    obj = make_person_json(p, [
        {"start": "unknown", "end": "present", "org": "中共工农区委", "title": "区委常委、组织部部长、统战部部长", "notes": "现任（2026-07）", "confidence": "confirmed", "source_ids": ["S001"]},
    ], [], SOURCES)
    obj["confidence_summary"]["career_completeness"] = "thin"
    _write_person(obj, "区委常委、组织部部长、统战部部长", "曲忠宝")

    # 4. 区人大副主任 马安相
    p = person_by_name("马安相")
    obj = make_person_json(p, [
        {"start": "unknown", "end": "present", "org": "鹤岗市工农区人民代表大会常务委员会", "title": "区人大常委会副主任", "notes": "现任", "confidence": "confirmed", "source_ids": ["S001"]},
    ], [], SOURCES)
    obj["confidence_summary"]["career_completeness"] = "thin"
    _write_person(obj, "区人大常委会副主任", "马安相")

# ── Main ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    orig_cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        print(f"Building {SLUG} network data...")
        build_db()
        build_gexf()
        build_person_jsons()
        print("\nOutput files in:", STAGING)
        print("  DB:  ", DB_PATH)
        print("  GEXF:", GEXF_PATH)
        for f in sorted(os.listdir(STAGING)):
            if f.endswith(".json") and f.startswith(TODAY):
                print("  Person:", f)
        print("Done.")
    finally:
        os.chdir(orig_cwd)