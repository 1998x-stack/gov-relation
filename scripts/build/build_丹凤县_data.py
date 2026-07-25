#!/usr/bin/env python3
"""丹凤县领导班子工作关系网络 - Build Script.

Sources:
  - https://www.danfeng.gov.cn/zfxxgk1/fdzdgk/ldzc.htm (政府领导页)
  - https://www.danfeng.gov.cn/info/4431/459371.htm (张杰简历)
  - https://www.danfeng.gov.cn/info/4431/459381.htm (索涛简历)
  - https://www.danfeng.gov.cn/info/4431/460581.htm (冯烽简历)
  - https://www.danfeng.gov.cn/info/4431/459391.htm (许军简历)
  - https://www.danfeng.gov.cn/info/4431/459401.htm (马苑元简历)
  - https://www.danfeng.gov.cn/info/4431/459411.htm (龚富杰简历)
  - https://www.danfeng.gov.cn/info/4431/459421.htm (赵雅萍简历)
  - https://www.danfeng.gov.cn/info/4431/459431.htm (郝浩简历)
  - https://www.danfeng.gov.cn/info/1731/468261.htm (郭安贵以县委书记身份出席人大会议)
"""

import sqlite3
import json
import os
from datetime import datetime

AS_OF = "2026-07-25"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "丹凤县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "丹凤县_network.gexf")
PERSONS_DIR = STAGING_DIR

# ── Data ──────────────────────────────────────────────────────────────────

persons = [
    {
        "id": "p1",
        "name": "郭安贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "丹凤县委书记",
        "current_org": "中共丹凤县委员会",
        "source": "https://www.danfeng.gov.cn/info/1731/468261.htm",
        "notes": "2026年5月以县委书记身份主持县人大会议并发表讲话"
    },
    {
        "id": "p2",
        "name": "张杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年3月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "2008年7月",
        "work_start": "2003年7月",
        "current_post": "丹凤县县长",
        "current_org": "丹凤县人民政府",
        "source": "https://www.danfeng.gov.cn/info/4431/459371.htm",
        "notes": "现任中共丹凤县委副书记、县政府党组书记、县长，2026年5月当选"
    },
    {
        "id": "p3",
        "name": "索涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年11月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "1995年8月",
        "work_start": "1992年12月",
        "current_post": "丹凤县委常委、常务副县长",
        "current_org": "丹凤县人民政府",
        "source": "https://www.danfeng.gov.cn/info/4431/459381.htm",
        "notes": "县政府党组副书记"
    },
    {
        "id": "p4",
        "name": "冯烽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年9月",
        "birthplace": "",
        "education": "研究生学历，博士学位",
        "party_join": "2002年4月",
        "work_start": "2002年7月",
        "current_post": "丹凤县委常委、副县长",
        "current_org": "丹凤县人民政府",
        "source": "https://www.danfeng.gov.cn/info/4431/460581.htm",
        "notes": "分管数字经济、商贸流通等"
    },
    {
        "id": "p5",
        "name": "许军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年8月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "1997年10月",
        "work_start": "1993年8月",
        "current_post": "丹凤县副县长、县公安局局长",
        "current_org": "丹凤县人民政府",
        "source": "https://www.danfeng.gov.cn/info/4431/459391.htm",
        "notes": "县公安局党委书记、局长"
    },
    {
        "id": "p6",
        "name": "马苑元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年5月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "2013年12月",
        "work_start": "2010年3月",
        "current_post": "丹凤县副县长",
        "current_org": "丹凤县人民政府",
        "source": "https://www.danfeng.gov.cn/info/4431/459401.htm",
        "notes": "分管工业、经贸、招商引资等"
    },
    {
        "id": "p7",
        "name": "龚富杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年1月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "2000年7月",
        "current_post": "丹凤县副县长",
        "current_org": "丹凤县人民政府",
        "source": "https://www.danfeng.gov.cn/info/4431/459411.htm",
        "notes": "中共党员，分管农业农村、乡村振兴、水利、林业等"
    },
    {
        "id": "p8",
        "name": "赵雅萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "",
        "education": "全日制大学学历，本科双学位",
        "party_join": "",
        "work_start": "2005年8月",
        "current_post": "丹凤县副县长",
        "current_org": "丹凤县人民政府",
        "source": "https://www.danfeng.gov.cn/info/4431/459421.htm",
        "notes": "分管文化旅游、市场监管、妇女儿童等"
    },
    {
        "id": "p9",
        "name": "郝浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年4月9日",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "1991年12月",
        "work_start": "1990年12月",
        "current_post": "丹凤县副县长",
        "current_org": "丹凤县人民政府",
        "source": "https://www.danfeng.gov.cn/info/4431/459431.htm",
        "notes": "分管教育、科技、民政、卫健、医保等"
    },
    {
        "id": "p10",
        "name": "吴宏涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "丹凤县人大常委会主任",
        "current_org": "丹凤县人民代表大会常务委员会",
        "source": "https://www.danfeng.gov.cn/info/1731/468261.htm",
        "notes": "2026年5月人大会议上担任大会主席团成员并发表讲话"
    },
]

organizations = [
    {"id": 1, "name": "中共丹凤县委员会", "type": "党委", "level": "县", "parent": "中共商洛市委员会", "location": "陕西省商洛市丹凤县"},
    {"id": 2, "name": "丹凤县人民政府", "type": "政府", "level": "县", "parent": "商洛市人民政府", "location": "陕西省商洛市丹凤县"},
    {"id": 3, "name": "丹凤县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "丹凤县", "location": "陕西省商洛市丹凤县"},
    {"id": 4, "name": "丹凤县公安局", "type": "政府", "level": "县", "parent": "丹凤县人民政府", "location": "陕西省商洛市丹凤县"},
]

positions = [
    # 郭安贵
    {"person_id": "p1", "org_id": 1, "title": "丹凤县委书记", "start": "", "end": "present", "rank": "正处级", "note": "2026年5月仍在任"},
    # 张杰
    {"person_id": "p2", "org_id": 2, "title": "丹凤县县长", "start": "2026-05", "end": "present", "rank": "正处级", "note": "2026年5月28日当选"},
    {"person_id": "p2", "org_id": 1, "title": "丹凤县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 索涛
    {"person_id": "p3", "org_id": 2, "title": "丹凤县常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组副书记"},
    {"person_id": "p3", "org_id": 1, "title": "丹凤县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 冯烽
    {"person_id": "p4", "org_id": 2, "title": "丹凤县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p4", "org_id": 1, "title": "丹凤县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 许军
    {"person_id": "p5", "org_id": 2, "title": "丹凤县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p5", "org_id": 4, "title": "丹凤县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": "县公安局党委书记"},
    # 马苑元
    {"person_id": "p6", "org_id": 2, "title": "丹凤县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 龚富杰
    {"person_id": "p7", "org_id": 2, "title": "丹凤县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 赵雅萍
    {"person_id": "p8", "org_id": 2, "title": "丹凤县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 郝浩
    {"person_id": "p9", "org_id": 2, "title": "丹凤县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 吴宏涛
    {"person_id": "p10", "org_id": 3, "title": "丹凤县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

relationships = [
    # 郭安贵 <-> 张杰 (党政一把手)
    {"person_a": "p1", "person_b": "p2", "type": "overlap", "context": "党政正职搭档", "overlap_org": "丹凤县", "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 索涛 <-> 张杰 (常务副职协助县长)
    {"person_a": "p2", "person_b": "p3", "type": "superior_subordinate", "context": "正副县长工作关系", "overlap_org": "丹凤县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 郭安贵 <-> 索涛 (县委常委关系)
    {"person_a": "p1", "person_b": "p3", "type": "superior_subordinate", "context": "县委班子上下级", "overlap_org": "中共丹凤县委员会", "overlap_period": "至今", "confidence": "confirmed"},
    # 郭安贵 <-> 冯烽 (县委常委关系)
    {"person_a": "p1", "person_b": "p4", "type": "superior_subordinate", "context": "县委班子上下级", "overlap_org": "中共丹凤县委员会", "overlap_period": "至今", "confidence": "confirmed"},
    # 张杰 <-> 冯烽 (正副县长关系)
    {"person_a": "p2", "person_b": "p4", "type": "superior_subordinate", "context": "正副县长工作关系", "overlap_org": "丹凤县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 张杰 <-> 许军 (正副县长关系)
    {"person_a": "p2", "person_b": "p5", "type": "superior_subordinate", "context": "正副县长工作关系", "overlap_org": "丹凤县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 张杰 <-> 马苑元 (正副县长关系)
    {"person_a": "p2", "person_b": "p6", "type": "superior_subordinate", "context": "正副县长工作关系", "overlap_org": "丹凤县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 张杰 <-> 龚富杰 (正副县长关系)
    {"person_a": "p2", "person_b": "p7", "type": "superior_subordinate", "context": "正副县长工作关系", "overlap_org": "丹凤县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 张杰 <-> 赵雅萍 (正副县长关系)
    {"person_a": "p2", "person_b": "p8", "type": "superior_subordinate", "context": "正副县长工作关系", "overlap_org": "丹凤县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 张杰 <-> 郝浩 (正副县长关系)
    {"person_a": "p2", "person_b": "p9", "type": "superior_subordinate", "context": "正副县长工作关系", "overlap_org": "丹凤县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 郭安贵 <-> 吴宏涛 (县委与人大关系)
    {"person_a": "p1", "person_b": "p10", "type": "overlap", "context": "县委与县人大主要领导", "overlap_org": "丹凤县", "overlap_period": "至今", "confidence": "confirmed"},
]


# ── Build: Database ──────────────────────────────────────────────────────

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for t in ("relationships", "positions", "organizations", "persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")

    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT, notes TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT,
        rank TEXT, note TEXT
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT, confidence TEXT
    )""")

    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute("INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (pid(p["id"]), p["name"], p["gender"], p["ethnicity"], p["birth"],
                     p.get("birthplace", ""), p["education"], p["party_join"], p["work_start"],
                     p["current_post"], p["current_org"], p["source"], p.get("notes", "")))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                    (pid(pos["person_id"]), pos["org_id"], pos["title"],
                     pos.get("start", ""), pos.get("end", ""),
                     pos.get("rank", ""), pos.get("note", "")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?,?,?,?,?,?,?)",
                    (pid(r["person_a"]), pid(r["person_b"]), r["type"], r["context"],
                     r["overlap_org"], r["overlap_period"], r.get("confidence", "unverified")))

    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")


# ── Build: GEXF ──────────────────────────────────────────────────────────

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;") if s is not None else ""

def person_color(post):
    if "县委书记" in post and "副" not in post:
        return ("255,50,50", 20.0)
    elif "县长" in post and "副" not in post:
        return ("50,100,255", 20.0)
    elif "县委副书记" in post:
        return ("50,100,255", 15.0)
    elif "常委" in post:
        return ("100,150,255", 12.0)
    elif "副县长" in post:
        return ("100,150,255", 12.0)
    elif "人大" in post:
        return ("200,255,255", 12.0)
    elif "政协" in post:
        return ("255,240,200", 12.0)
    else:
        return ("100,100,100", 12.0)

def org_color(org_type):
    colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
    }
    return colors.get(org_type, ("200,200,200", 8.0))

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>丹凤县领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c, sz = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid_val = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        a = int(r["person_a"][1:])
        b = int(r["person_b"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


# ── Person JSON ──────────────────────────────────────────────────────────

def make_person_json(person, timeline, rels_list, src_register):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "陕西省",
            "city": "商洛市",
            "region": "丹凤县",
            "job": person["current_post"],
            "task_id": "shaanxi_丹凤县",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": f"danfeng_{''.join(c for c in person['name'] if c != ' ')}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person["education"], "study_type": "unknown", "source_ids": []}],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}" if person["birth"] else person["name"],
                "name_birthplace": "",
                "official_profile_url": person["source"]
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "县委书记" in person["current_post"] or "县长" in person["current_post"] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
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
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": src_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（早期职业经历、教育背景缺失）"
        },
        "open_questions": [
            {"priority": "critical", "question": "郭安贵完整履历未知", "why_it_matters": "县委书记是核心人物，完整履历对分析其关系网络至关重要", "suggested_queries": ["郭安贵 简历", "郭安贵 任前公示", "郭安贵 商洛"], "last_attempted": AS_OF},
            {"priority": "high", "question": "张杰在丹凤之前的职业生涯", "why_it_matters": "县长履历有助于溯源其与上级或同级的关系", "suggested_queries": ["张杰 商洛 简历", "张杰 任前公示 丹凤县长"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "副县长们更完整的职业履历", "why_it_matters": "了解每位副县长的背景有助于识别跨县关系网络", "suggested_queries": ["索涛 简历 商洛", "冯烽 简历", "许军 商洛"], "last_attempted": AS_OF}
        ]
    }

def write_person_jsons():
    """Create person graph JSON files for the two core leaders."""
    source_register = [
        {"id": "S001", "title": "丹凤县政府网站—领导之窗", "url": "https://www.danfeng.gov.cn/zfxxgk1/fdzdgk/ldzc.htm", "publisher": "丹凤县人民政府", "published_at": "2026", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "政府领导列表"},
        {"id": "S002", "title": "张杰简历页", "url": "https://www.danfeng.gov.cn/info/4431/459371.htm", "publisher": "丹凤县人民政府", "published_at": "2026", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张杰：1981年3月生，研究生学历"},
        {"id": "S003", "title": "丹凤县第十九届人民代表大会第六次会议闭幕", "url": "https://www.danfeng.gov.cn/info/1731/468261.htm", "publisher": "丹凤县人民政府", "published_at": "2026-05-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认郭安贵为县委书记，张杰当选县长"},
    ]

    def person_timeline(person):
        """Build timeline from positions data for this person."""
        tl = []
        for pos in positions:
            if pos["person_id"] == person["id"]:
                tl.append({
                    "start": pos.get("start", "unknown"),
                    "end": pos.get("end", "present"),
                    "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
                    "title": pos["title"],
                    "level": pos.get("rank", ""),
                    "location": "陕西省商洛市丹凤县",
                    "system": "party" if pos["org_id"] == 1 else "government",
                    "rank": pos.get("rank", ""),
                    "is_key_promotion": "县委书记" in pos["title"] or ("县长" in pos["title"] and "副" not in pos["title"]),
                    "notes": pos.get("note", ""),
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"]
                })
        return tl

    def person_relationships(person):
        """Build relationships list for this person."""
        rels = []
        for r in relationships:
            target_id = None
            direction = "person_to_other"
            if r["person_a"] == person["id"]:
                target_id = r["person_b"]
                direction = "person_to_other"
            elif r["person_b"] == person["id"]:
                target_id = r["person_a"]
                direction = "other_to_person"
            if target_id:
                target_person = next((p for p in persons if p["id"] == target_id), None)
                if target_person:
                    rels.append({
                        "person": target_person["name"],
                        "person_id": f"danfeng_{''.join(c for c in target_person['name'] if c != ' ')}",
                        "relationship_type": r["type"],
                        "strength": "strong" if r.get("confidence") == "confirmed" else "medium",
                        "evidence": r.get("context", ""),
                        "overlap_org": r.get("overlap_org", ""),
                        "overlap_period": r.get("overlap_period", ""),
                        "direction": direction,
                        "confidence": r.get("confidence", "unverified"),
                        "source_ids": ["S001", "S003"]
                    })
        return rels

    core_people = ["p1", "p2"]
    for pid in core_people:
        person = next(p for p in persons if p["id"] == pid)
        filename = f"{AS_OF}-陕西省-商洛市-{person['current_post']}-{person['name']}.json"
        filepath = os.path.join(PERSONS_DIR, filename)
        data = make_person_json(person, person_timeline(person), person_relationships(person), source_register)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filepath}")


# ── Main ─────────────────────────────────────────────────────────────────

def build():
    print(f"\n{'='*60}")
    print(f"丹凤县 Network Build - {AS_OF}")
    print(f"{'='*60}")
    build_db()
    build_gexf()
    write_person_jsons()
    print(f"\n{'='*60}")
    print(f"Build Complete: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
    print(f"{'='*60}")

if __name__ == "__main__":
    build()
