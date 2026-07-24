#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 阳新县 (Yangxin County, 黄石市, 湖北省) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/阳新县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/阳新县_network.gexf")

# ── DATA ────────────────────────────────────────────────────────────────────

persons = [
    # ── County Party Committee Leaders ──
    {"id": 1, "name": "杨波", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳新县委书记", "current_org": "中共阳新县委员会",
     "source": "https://www.yx.gov.cn/xwdt/yxyw/202607/t20260724_1345711.html"},
    {"id": 2, "name": "卢川", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-02", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳新县委副书记、县长", "current_org": "阳新县人民政府",
     "source": "https://www.yx.gov.cn/zfxxgk/fdzdgknr/xzfld_11079/202605/t20260514_1327523.html"},
    {"id": 3, "name": "韩顺东", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳新县委常委、组织部部长", "current_org": "中共阳新县委员会",
     "source": "https://www.yx.gov.cn/xwdt/yxyw/202607/t20260715_1343262.html"},
    {"id": 4, "name": "马辉商", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳新县委常委", "current_org": "中共阳新县委员会",
     "source": "https://www.yx.gov.cn/xwdt/yxyw/202607/t20260724_1345714.html"},
    {"id": 5, "name": "倪学军", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-09", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳新县委常委、常务副县长", "current_org": "阳新县人民政府",
     "source": "https://www.yx.gov.cn/zfxxgk/fdzdgknr/xzfld_11079/202605/t20260514_1327517.html"},
    {"id": 6, "name": "郑鹏鲲", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳新县委常委、县纪委书记、监委主任", "current_org": "中共阳新县纪律检查委员会",
     "source": "https://www.yx.gov.cn/xwdt/yxyw/202607/t20260724_1345714.html"},
    {"id": 7, "name": "杨前友", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-10", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳新县委常委、副县长", "current_org": "阳新县人民政府",
     "source": "https://www.yx.gov.cn/zfxxgk/fdzdgknr/xzfld_11079/202605/t20260514_1327514.html"},
    {"id": 8, "name": "朱玉良", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳新县领导", "current_org": "中共阳新县委员会",
     "source": "https://www.yx.gov.cn/xwdt/yxyw/202607/t20260724_1345714.html"},

    # ── County Government Leaders ──
    {"id": 9, "name": "兰山", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-08", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳新县副县长、党组成员，县委政法委副书记、县公安局局长", "current_org": "阳新县人民政府",
     "source": "https://www.yx.gov.cn/zfxxgk/fdzdgknr/xzfld_11079/202605/t20260514_1327512.html"},
    {"id": 10, "name": "虞润卿", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳新县副县长", "current_org": "阳新县人民政府",
     "source": "https://www.yx.gov.cn/xwdt/yxyw/202607/t20260715_1343238.html"},
    {"id": 11, "name": "石顺发", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳新县副县长", "current_org": "阳新县人民政府",
     "source": "https://www.yx.gov.cn/xwdt/yxyw/202607/t20260723_1345417.html"},
    {"id": 12, "name": "林子荣", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳新县副县长", "current_org": "阳新县人民政府",
     "source": "https://www.yx.gov.cn/xwdt/yxyw/202607/t20260715_1343238.html"},

    # ── Former Leaders (Moved/Resigned) ──
    {"id": 13, "name": "李冠男", "gender": "男", "ethnicity": "汉族",
     "birth": "1987-01", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原阳新县委副书记（已调任黄石港区代理区长）", "current_org": "",
     "source": "https://www.huangshigang.gov.cn/zwpd/fdzdgknr/ldzc/202108/t20210820_827346.html"},
]

organizations = [
    {"id": 1, "name": "中共阳新县委员会", "type": "党委", "level": "县级", "parent": "中共黄石市委员会", "location": "阳新县"},
    {"id": 2, "name": "阳新县人民政府", "type": "政府", "level": "县级", "parent": "黄石市人民政府", "location": "阳新县"},
    {"id": 3, "name": "中共阳新县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共黄石市纪律检查委员会", "location": "阳新县"},
    {"id": 4, "name": "阳新县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "黄石市人民代表大会常务委员会", "location": "阳新县"},
    {"id": 5, "name": "中国人民政治协商会议阳新县委员会", "type": "政协", "level": "县级", "parent": "中国人民政治协商会议黄石市委员会", "location": "阳新县"},
    {"id": 6, "name": "阳新县公安局", "type": "政府", "level": "县级", "parent": "黄石市公安局", "location": "阳新县"},
    {"id": 7, "name": "中共黄石港区委员会", "type": "党委", "level": "县级", "parent": "中共黄石市委员会", "location": "黄石港区"},
    {"id": 8, "name": "黄石港区人民政府", "type": "政府", "level": "县级", "parent": "黄石市人民政府", "location": "黄石港区"},
]

positions = [
    # 杨波
    {"person_id": 1, "org_id": 1, "title": "阳新县委书记",
     "start": "", "end": "present", "rank": "正县级", "note": "2026年7月已确认在任"},

    # 卢川
    {"person_id": 2, "org_id": 2, "title": "阳新县长",
     "start": "", "end": "present", "rank": "正县级", "note": "主持县政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "阳新县委副书记",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 韩顺东
    {"person_id": 3, "org_id": 1, "title": "阳新县委常委、组织部部长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 马辉商
    {"person_id": 4, "org_id": 1, "title": "阳新县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "具体职务待确认"},

    # 倪学军
    {"person_id": 5, "org_id": 1, "title": "阳新县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "阳新县常务副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "负责县政府常务工作"},

    # 郑鹏鲲
    {"person_id": 6, "org_id": 1, "title": "阳新县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "阳新县纪委书记、监委主任",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 杨前友
    {"person_id": 7, "org_id": 1, "title": "阳新县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "阳新县副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "负责自然资源、住建、城管等工作"},

    # 朱玉良
    {"person_id": 8, "org_id": 1, "title": "阳新县领导",
     "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},

    # 兰山
    {"person_id": 9, "org_id": 2, "title": "阳新县副县长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "阳新县公安局局长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 虞润卿
    {"person_id": 10, "org_id": 2, "title": "阳新县副县长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 石顺发
    {"person_id": 11, "org_id": 2, "title": "阳新县副县长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 林子荣
    {"person_id": 12, "org_id": 2, "title": "阳新县副县长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 李冠男（原阳新县委副书记，已调离）
    {"person_id": 13, "org_id": 1, "title": "阳新县委副书记",
     "start": "", "end": "2026-05", "rank": "副县级", "note": "调任黄石港区代理区长"},
    {"person_id": 13, "org_id": 7, "title": "黄石港区委副书记",
     "start": "2026-06", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 8, "title": "黄石港区代理区长",
     "start": "2026-06", "end": "present", "rank": "正县级", "note": "2026年6月12日区人大常委会任命"},
]

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "杨波为县委书记，卢川为县委副书记、县长，党政一把手搭档关系",
     "overlap_org": "中共阳新县委员会", "overlap_period": "在任期间"},

    # 常委会班子成员间
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "杨波为县委书记，韩顺东为县委常委、组织部部长",
     "overlap_org": "中共阳新县委员会", "overlap_period": "在任期间"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "杨波（县委书记）与倪学军（县委常委、常务副县长）",
     "overlap_org": "中共阳新县委员会", "overlap_period": "在任期间"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "杨波为县委书记，郑鹏鲲为县委常委、纪委书记",
     "overlap_org": "中共阳新县委员会", "overlap_period": "在任期间"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "杨波（县委书记）与杨前友（县委常委、副县长）",
     "overlap_org": "中共阳新县委员会", "overlap_period": "在任期间"},

    # 县政府上下级
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "卢川（县长）与倪学军（常务副县长）政府上下级",
     "overlap_org": "阳新县人民政府", "overlap_period": "在任期间"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "卢川（县长）与杨前友（副县长）政府上下级",
     "overlap_org": "阳新县人民政府", "overlap_period": "在任期间"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "卢川（县长）与兰山（副县长、公安局长）政府上下级",
     "overlap_org": "阳新县人民政府", "overlap_period": "在任期间"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "卢川（县长）与虞润卿（副县长）政府上下级",
     "overlap_org": "阳新县人民政府", "overlap_period": "在任期间"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "卢川（县长）与石顺发（副县长）政府上下级",
     "overlap_org": "阳新县人民政府", "overlap_period": "在任期间"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "卢川（县长）与林子荣（副县长）政府上下级",
     "overlap_org": "阳新县人民政府", "overlap_period": "在任期间"},

    # 同级常委间关系
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "同为县委常委班子成员",
     "overlap_org": "中共阳新县委员会", "overlap_period": "在任期间"},
    {"person_a": 3, "person_b": 6, "type": "overlap",
     "context": "同为县委常委班子成员",
     "overlap_org": "中共阳新县委员会", "overlap_period": "在任期间"},
    {"person_a": 3, "person_b": 7, "type": "overlap",
     "context": "同为县委常委班子成员",
     "overlap_org": "中共阳新县委员会", "overlap_period": "在任期间"},
    {"person_a": 5, "person_b": 6, "type": "overlap",
     "context": "同为县委常委班子成员",
     "overlap_org": "中共阳新县委员会", "overlap_period": "在任期间"},
    {"person_a": 5, "person_b": 7, "type": "overlap",
     "context": "同为县委常委班子成员",
     "overlap_org": "中共阳新县委员会", "overlap_period": "在任期间"},
    {"person_a": 6, "person_b": 7, "type": "overlap",
     "context": "同为县委常委班子成员",
     "overlap_org": "中共阳新县委员会", "overlap_period": "在任期间"},

    # 跨县区调任关系
    {"person_a": 13, "person_b": 1, "type": "overlap",
     "context": "李冠男曾任阳新县委副书记，与杨波在阳新县委班子共事",
     "overlap_org": "中共阳新县委员会", "overlap_period": "至2026年5月"},
    {"person_a": 13, "person_b": 2, "type": "overlap",
     "context": "李冠男曾任阳新县委副书记，与卢川在阳新县委班子共事",
     "overlap_org": "中共阳新县委员会", "overlap_period": "至2026年5月"},
]

# ── BUILD FUNCTIONS ─────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
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
        CREATE TABLE IF NOT EXISTS relationships (
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
    conn.commit()

def person_color(p):
    """Return GEXF color string based on person's role."""
    post = p.get("current_post", "")
    if "县委" in post and ("书记" in post and "副" not in post[:post.find("书记")+2]):
        return "255,50,50"
    elif "县长" in post:
        return "50,100,255"
    elif "纪委" in post:
        return "255,165,0"
    elif "常委" in post and ("副县长" in post or "常务" in post):
        return "50,100,255"
    elif "副县长" in post:
        return "50,100,255"
    elif "常委" in post:
        return "100,100,100"
    elif "原" in post:
        return "150,150,150"
    else:
        return "100,100,100"

def is_top_leader(p):
    post = p.get("current_post", "")
    # 县委书记（非副书记）
    if "县委书记" in post and "副书记" not in post:
        return True
    # 县长（非副县长）
    if "县长" in post and "副县长" not in post:
        return True
    return False

def build_gexf(persons_list, orgs_list, positions_list, relationships_list):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>阳新县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="post" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - Persons
    lines.append('    <nodes>')
    for p in persons_list:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        if p.get("id", 0) == 13:  # former leaders
            sz = "10.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - Organizations
    for o in orgs_list:
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="200" g="200" b="200"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person -> organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions_list:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start", ""))} - {esc(pos.get("end", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person <-> person
    for r in relationships_list:
        eid += 1
        w = "2.0" if r["type"] in ("superior_subordinate",) else "1.5"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    return "\n".join(lines)

# ── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print(f"Building database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    for p in persons:
        conn.execute(
            "INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p.get("current_post", ""), p.get("current_org", ""), p.get("source", ""))
        )

    # Insert organizations
    for o in organizations:
        conn.execute(
            "INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    # Insert positions
    for pos in positions:
        conn.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", ""),
             pos.get("rank", ""), pos.get("note", ""))
        )

    # Insert relationships
    for r in relationships:
        conn.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""))
        )

    conn.commit()
    conn.close()

    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    # Build GEXF
    print(f"\nBuilding GEXF: {GEXF_PATH}")
    gexf_content = build_gexf(persons, organizations, positions, relationships)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write(gexf_content)
    print("  Done.")

    # Summary table
    print("\n── Key Personnel ──")
    for p in persons:
        if is_top_leader(p):
            print(f"  {p['name']} — {p['current_post']} ({p.get('birth', '?')})")
    print("\n── Standing Committee (confirmed) ──")
    for p in persons:
        if 1 <= p["id"] <= 8 and p["id"] != 2:
            print(f"  {p['name']} — {p['current_post']}")
    print("\n── Government Leaders ──")
    for p in persons:
        if 9 <= p["id"] <= 12:
            print(f"  {p['name']} — {p['current_post']}")
    print("\n── Cross-Region Transfer ──")
    for p in persons:
        if p["id"] == 13:
            print(f"  {p['name']} — {p['current_post']}")


if __name__ == "__main__":
    main()
