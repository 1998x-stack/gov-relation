#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 施秉县 (Shibing County, Qiandongnan, Guizhou) leadership network.

施秉县 — 贵州省黔东南苗族侗族自治州辖县, 位于贵州省东部, 㵲阳河畔.
Research date: 2026-08-03. Sources: qdnsb.gov.cn official news pages.
"""

import json
import os
import sqlite3
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/guizhou_施秉县")
DB_PATH = os.path.join(STAGING, "施秉县_network.db")
GEXF_PATH = os.path.join(STAGING, "施秉县_network.gexf")
PERSONS_DIR = os.path.join(STAGING, "persons")

AS_OF = "2026-08-03"
TODAY = AS_OF.replace("-", "")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

# ── Persons ──
persons = [
    # ── Core Leaders (Targets) ──
    # 潘丽章 — 施秉县委书记
    {"id": 1, "name": "潘丽章", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "施秉县委书记",
     "current_org": "中共施秉县委员会",
     "source": "www.qdnsb.gov.cn 官方新闻（2026年7月多篇报道确认姓名和职务）"},

    # 石家彬 — 施秉县委副书记、县长
    {"id": 2, "name": "石家彬", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "施秉县委副书记、县人民政府县长",
     "current_org": "施秉县人民政府",
     "source": "www.qdnsb.gov.cn 官方新闻（2026年7月多篇报道确认姓名和职务）"},

    # ── 县委领导班子 ──
    # 张炜 — 县委副书记
    {"id": 3, "name": "张炜", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "施秉县委副书记",
     "current_org": "中共施秉县委员会",
     "source": "www.qdnsb.gov.cn 县委常委会新闻（2026-07-22, 2026-07-15）"},

    # 周武权 — 县委副书记
    {"id": 4, "name": "周武权", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "施秉县委副书记",
     "current_org": "中共施秉县委员会",
     "source": "www.qdnsb.gov.cn 县委常委会第218次会议（2026-07-15）"},

    # ── 县政协 ──
    # 邰文福 — 县政协主席
    {"id": 5, "name": "邰文福", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "施秉县政协主席",
     "current_org": "政协施秉县委员会",
     "source": "www.qdnsb.gov.cn 县委常委会第219次（扩大）会议（2026-07-22）"},

    # ── 县领导（副县长级，职务待确认）──
    {"id": 6, "name": "龙燚", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "施秉县领导",
     "current_org": "施秉县人民政府",
     "source": "www.qdnsb.gov.cn 石家彬调研报道（2026-07-18）"},

    {"id": 7, "name": "郝稳", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "施秉县领导",
     "current_org": "施秉县人民政府",
     "source": "www.qdnsb.gov.cn 石家彬调研报道（2026-07-18）"},

    {"id": 8, "name": "姜文大", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "施秉县领导",
     "current_org": "施秉县人民政府",
     "source": "www.qdnsb.gov.cn 潘丽章调研报道（2026-07-18）"},

    {"id": 9, "name": "金延楷", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "施秉县领导",
     "current_org": "施秉县人民政府",
     "source": "www.qdnsb.gov.cn 潘丽章调研报道（2026-07-18）"},
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共施秉县委员会", "type": "党委", "level": "县处级", "parent": "中共黔东南苗族侗族自治州委员会", "location": "贵州省黔东南州施秉县"},
    {"id": 2, "name": "施秉县人民政府", "type": "政府", "level": "县处级", "parent": "黔东南苗族侗族自治州人民政府", "location": "贵州省黔东南州施秉县"},
    {"id": 3, "name": "施秉县人大常委会", "type": "人大", "level": "县处级", "parent": "黔东南州人大常委会", "location": "贵州省黔东南州施秉县"},
    {"id": 4, "name": "政协施秉县委员会", "type": "政协", "level": "县处级", "parent": "政协黔东南州委员会", "location": "贵州省黔东南州施秉县"},
    {"id": 5, "name": "中共施秉县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共施秉县委员会", "location": "贵州省黔东南州施秉县"},
]

# ── Positions ──
positions = [
    # 潘丽章 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "施秉县委书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "女，姓名通过官方新闻确认（2026年7月多篇报道：常委会主持会议、调研乡村）"},

    # 石家彬 — 县长
    {"person_id": 2, "org_id": 1, "title": "施秉县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "施秉县人民政府县长", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "官方新闻多次报道。调研景区安全、学校建设、自然资源工作等"},

    # 张炜 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "施秉县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "出席县委常委会第218次、第219次会议"},

    # 周武权 — 县委副书记
    {"person_id": 4, "org_id": 1, "title": "施秉县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "出现在县委常委会第218次会议名单"},

    # 邰文福 — 政协主席
    {"person_id": 5, "org_id": 4, "title": "施秉县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "出席县委常委会第219次会议"},

    # 龙燚 — 县领导（推测为副县长）
    {"person_id": 6, "org_id": 2, "title": "施秉县副县长（推测）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "陪同县长调研，职务待确认"},

    # 郝稳 — 县领导
    {"person_id": 7, "org_id": 2, "title": "施秉县领导（推测为副县长）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "陪同县长调研，职务待确认"},

    # 姜文大 — 县领导
    {"person_id": 8, "org_id": 2, "title": "施秉县领导（推测为副县长）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "陪同县委书记潘丽章调研，职务待确认"},

    # 金延楷 — 县领导
    {"person_id": 9, "org_id": 2, "title": "施秉县领导（推测为副县长）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "陪同县委书记潘丽章调研，职务待确认"},
]

# ── Relationships ──
relationships = [
    # 书记 ↔ 县长（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "潘丽章（县委书记）与石家彬（县长）构成县委书记-县长搭档",
     "overlap_org": "中共施秉县委员会/施秉县人民政府", "overlap_period": "2026年至今"},

    # 书记 ↔ 县委副书记
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "潘丽章与张炜（县委副书记）在县委常委会共事",
     "overlap_org": "中共施秉县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "潘丽章与周武权（县委副书记）在县委常委会共事",
     "overlap_org": "中共施秉县委员会", "overlap_period": "2026年至今"},

    # 书记 ↔ 政协主席
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "潘丽章与邰文福（政协主席）在县委常委会会议同席",
     "overlap_org": "中共施秉县委员会", "overlap_period": "2026年至今"},

    # 县长 ↔ 县领导
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "石家彬与龙燚共同调研防溺水、旅游服务保障等工作",
     "overlap_org": "施秉县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "石家彬与郝稳共同调研",
     "overlap_org": "施秉县人民政府", "overlap_period": "2026年至今"},

    # 书记 ↔ 县领导
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "潘丽章与姜文大共同调研防溺水、防汛抗旱等工作",
     "overlap_org": "施秉县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "潘丽章与金延楷共同调研",
     "overlap_org": "施秉县人民政府", "overlap_period": "2026年至今"},
]

# ═══════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build():
    os.makedirs(STAGING, exist_ok=True)
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
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
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"施秉县_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "255,50,50"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "50,100,255"
        if "纪委书记" in post or "纪委" in post:
            return "255,165,0"
        if "副书记" in post or "副" in post:
            return "100,150,220"
        if "主任" in post and "副" not in post:
            return "60,180,60"
        if "政协" in post:
            return "180,160,80"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post) or \
               ("县长" in post and "副" not in post and "人大" not in post and "政协" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "square"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "circle"
        if "纪委书记" in post or "纪委" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "纪委": "255,200,150",
            "开发区": "200,255,200",
            "事业单位": "220,220,220",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>施秉县领导班子关系网络（基于www.qdnsb.gov.cn官方新闻、领导活动报道）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization
    for pos in positions:
        if pos["org_id"] == 99:
            continue
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person
    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person JSONs ──
    source_register = [
        {"id": "S001", "title": "施秉县委常委会第219次（扩大）会议召开", "url": "https://www.qdnsb.gov.cn/xwzx/zwyw/202607/t20260722_90649134.html",
         "publisher": "施秉县人民政府", "published_at": "2026-07-22", "accessed_at": "2026-08-03", "source_type": "official", "reliability": "high",
         "notes": "报道潘丽章（书记）、石家彬（县长）、邰文福（政协主席）、张炜（县委副书记）"},
        {"id": "S002", "title": "十四届县委常委会第218次会议召开", "url": "https://www.qdnsb.gov.cn/xwzx/zwyw/202607/t20260715_90623365.html",
         "publisher": "施秉县人民政府", "published_at": "2026-07-15", "accessed_at": "2026-08-03", "source_type": "official", "reliability": "high",
         "notes": "报道潘丽章、石家彬、邰文福、周武权、张炜"},
        {"id": "S003", "title": "石家彬调研督导未成年人防溺水、旅游服务保障等相关工作", "url": "https://www.qdnsb.gov.cn/xwzx/ldhd_5889777/202607/t20260720_90637840.html",
         "publisher": "施秉县人民政府", "published_at": "2026-07-18", "accessed_at": "2026-08-03", "source_type": "official", "reliability": "high",
         "notes": "报道石家彬（县长）活动，提及龙燚、郝稳"},
        {"id": "S004", "title": "潘丽章调研督导未成年人防溺水、防汛抗旱等相关工作", "url": "https://www.qdnsb.gov.cn/xwzx/ldhd_5889777/202607/t20260720_90637753.html",
         "publisher": "施秉县人民政府", "published_at": "2026-07-18", "accessed_at": "2026-08-03", "source_type": "official", "reliability": "high",
         "notes": "报道潘丽章（书记）活动，提及姜文大、金延楷"},
        {"id": "S005", "title": "潘丽章到马溪乡调研", "url": "https://www.qdnsb.gov.cn/xwzx/ldhd_5889777/202607/t20260720_90637732.html",
         "publisher": "施秉县人民政府", "published_at": "2026-07-16", "accessed_at": "2026-08-03", "source_type": "official", "reliability": "high",
         "notes": "报道潘丽章到马溪乡调研"},
        {"id": "S006", "title": "石家彬到城区小学调研", "url": "https://www.qdnsb.gov.cn/xwzx/ldhd_5889777/202607/t20260714_90619475.html",
         "publisher": "施秉县人民政府", "published_at": "2026-07-14", "accessed_at": "2026-08-03", "source_type": "official", "reliability": "high",
         "notes": "报道石家彬调研教育"},
        {"id": "S007", "title": "石家彬为施秉县自然资源系统讲授专题党课", "url": "https://www.qdnsb.gov.cn/xwzx/ldhd_5889777/202607/t20260713_90612517.html",
         "publisher": "施秉县人民政府", "published_at": "2026-07-10", "accessed_at": "2026-08-03", "source_type": "official", "reliability": "high",
         "notes": "报道石家彬讲授党课"},
    ]

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "贵州省",
                "city": "黔东南苗族侗族自治州",
                "region": "施秉县",
                "job": p.get("current_post", ""),
                "task_id": "guizhou_施秉县",
                "time_focus": "2026年8月"
            },
            "identity": {
                "person_id": f"施秉县_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
                ] if p.get("education") else [],
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
                "administrative_rank": "县处级正职" if ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "纪委" not in p.get("current_post", "")) or ("县长" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "人大" not in p.get("current_post", "")) else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": []
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
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历信息缺失（出生年份、籍贯、教育背景均未知）"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 施秉"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 潘丽章 Person JSON ──
    plz_timeline = [
        {"start": "", "end": "", "org": "中共施秉县委员会", "title": "施秉县委书记",
         "notes": "现任（2026年7月官方新闻确认），履历待查",
         "confidence": "confirmed", "source_ids": ["S001", "S002", "S004"]},
    ]
    plz_relationships = [
        {"person": "石家彬", "person_id": "施秉县_石家彬", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "潘丽章（县委书记）与石家彬（县长）构成县委书记-县长搭档",
         "overlap_org": "中共施秉县委员会", "overlap_period": "2026年至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "张炜", "person_id": "施秉县_张炜", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "在县委常委会共事",
         "overlap_org": "中共施秉县委员会", "overlap_period": "2026年至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "周武权", "person_id": "施秉县_周武权", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "在县委常委会共事",
         "overlap_org": "中共施秉县委员会", "overlap_period": "2026年至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]

    plz_json = make_person_json(persons[0], plz_timeline, plz_relationships)
    plz_path = os.path.join(PERSONS_DIR, f"{TODAY}-贵州省-黔东南苗族侗族自治州-县委书记-潘丽章.json")
    with open(plz_path, "w", encoding="utf-8") as f:
        json.dump(plz_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {plz_path}")

    # ── 石家彬 Person JSON ──
    sjb_timeline = [
        {"start": "", "end": "", "org": "施秉县人民政府", "title": "施秉县委副书记、县长",
         "notes": "现任（2026年7月官方新闻确认），履历待查",
         "confidence": "confirmed", "source_ids": ["S001", "S003", "S006", "S007"]},
    ]
    sjb_relationships = [
        {"person": "潘丽章", "person_id": "施秉县_潘丽章", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "石家彬（县长）与潘丽章（县委书记）构成县委书记-县长搭档",
         "overlap_org": "中共施秉县委员会", "overlap_period": "2026年至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "龙燚", "person_id": "施秉县_龙燚", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "共同调研防溺水、旅游服务保障等工作",
         "overlap_org": "施秉县人民政府", "overlap_period": "2026-07",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "郝稳", "person_id": "施秉县_郝稳", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "共同调研",
         "overlap_org": "施秉县人民政府", "overlap_period": "2026-07",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    ]

    sjb_json = make_person_json(persons[1], sjb_timeline, sjb_relationships)
    sjb_path = os.path.join(PERSONS_DIR, f"{TODAY}-贵州省-黔东南苗族侗族自治州-县长-石家彬.json")
    with open(sjb_path, "w", encoding="utf-8") as f:
        json.dump(sjb_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {sjb_path}")

    print(f"\nBuild complete. All artifacts in {STAGING}")


if __name__ == "__main__":
    build()