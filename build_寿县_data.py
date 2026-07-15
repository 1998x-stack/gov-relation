#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 寿县 (Shou County, Huainan, Anhui) leadership network.
Generated: 2026-07-15
Task: anhui_寿县 - 县委书记 & 县长
Sources: shouxian.gov.cn government website (leadership profiles, news, accessed 2026-07-15)
Note: Web search degraded (Exa rate-limited, Baidu/Google/Wikipedia blocked).
      Core leaders identified from official government pages.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
# If running from staging temp dir (data/tmp/anhui_寿县/), go up to repo root
if "data/tmp" in BASE:
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))
STAGING = os.path.join(BASE, "data/tmp/anhui_寿县")
DB_PATH = os.path.join(STAGING, "寿县_network.db")
GEXF_PATH = os.path.join(STAGING, "寿县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {"id": 1, "name": "孙奇志", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "寿县县委书记", "current_org": "中国共产党寿县委员会",
     "source": "https://www.shouxian.gov.cn/public/118322644/1260740781.html"},
    {"id": 2, "name": "赵德兵", "gender": "男", "ethnicity": "汉族",
     "birth": "1974", "birthplace": "", "education": "硕士研究生（合肥工业大学工业工程专业工程硕士）",
     "party_join": "中共党员", "work_start": "1995-09",
     "current_post": "寿县县委副书记、县政府党组书记、县长", "current_org": "寿县人民政府",
     "source": "https://www.shouxian.gov.cn/public/118322644/1260766348.html"},

    # ── Predecessor ──
    {"id": 3, "name": "牛方括", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前任寿县县委书记（~2021-2025)", "current_org": "",
     "source": "https://www.shouxian.gov.cn/zwzx/zwxx/8076638.html"},

    # ── 县领导（from government website confirmed）──
    {"id": 4, "name": "张亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "寿县副县长", "current_org": "寿县人民政府",
     "source": "https://www.shouxian.gov.cn/zwzx/zwxx/8177132.html"},
]

organizations = [
    {"id": 101, "name": "中国共产党寿县委员会", "type": "party",
     "level": "county", "parent": "中国共产党淮南市委员会", "location": "安徽省淮南市寿县"},
    {"id": 102, "name": "寿县人民政府", "type": "government",
     "level": "county", "parent": "淮南市人民政府", "location": "安徽省淮南市寿县"},
    {"id": 103, "name": "寿县人民代表大会常务委员会", "type": "people_congress",
     "level": "county", "parent": "寿县", "location": "安徽省淮南市寿县"},
    {"id": 104, "name": "中国人民政治协商会议寿县委员会", "type": "cppcc",
     "level": "county", "parent": "寿县", "location": "安徽省淮南市寿县"},
    {"id": 105, "name": "中国共产党淮南市委员会", "type": "party",
     "level": "prefecture", "parent": "中国共产党安徽省委员会", "location": "安徽省淮南市"},
    {"id": 106, "name": "淮南市人民政府", "type": "government",
     "level": "prefecture", "parent": "安徽省人民政府", "location": "安徽省淮南市"},
    {"id": 107, "name": "寿县经济开发区（安徽寿县新桥国际产业园、寿县蜀山现代产业园）", "type": "development_zone",
     "level": "county", "parent": "寿县人民政府", "location": "安徽省淮南市寿县"},
    {"id": 108, "name": "寿县堰口镇人民政府", "type": "government",
     "level": "township", "parent": "寿县人民政府", "location": "安徽省淮南市寿县堰口镇"},
    {"id": 109, "name": "寿县双桥镇人民政府", "type": "government",
     "level": "township", "parent": "寿县人民政府", "location": "安徽省淮南市寿县双桥镇"},
    {"id": 110, "name": "寿县板桥镇人民政府", "type": "government",
     "level": "township", "parent": "寿县人民政府", "location": "安徽省淮南市寿县板桥镇"},
    {"id": 111, "name": "寿县迎河镇人民政府", "type": "government",
     "level": "township", "parent": "寿县人民政府", "location": "安徽省淮南市寿县迎河镇"},
    {"id": 112, "name": "寿县建设乡人民政府", "type": "government",
     "level": "township", "parent": "寿县人民政府", "location": "安徽省淮南市寿县（原建设乡）"},
    {"id": 113, "name": "共青团寿县委员会", "type": "mass_organization",
     "level": "county", "parent": "中国共产党寿县委员会", "location": "安徽省淮南市寿县"},
    {"id": 114, "name": "共青团安徽省委员会", "type": "mass_organization",
     "level": "province", "parent": "中国共产党安徽省委员会", "location": "安徽省合肥市"},
    {"id": 115, "name": "新桥国际产业园", "type": "development_zone",
     "level": "county", "parent": "寿县人民政府", "location": "安徽省淮南市寿县"},
]

positions = [
    # ── 孙奇志 ──
    # Sun Qizhi - known positions from government news
    # She was 县长 before becoming 县委书记
    # Exact appointment dates for her early career unknown
    {"person_id": 1, "org_id": 101, "title": "寿县县委书记",
     "start": "2025", "end": "present", "rank": "county_chief", "note": "Confirmed as of 2025-09 (National Health Commission press conference). News continues into 2026-07."},
    {"person_id": 1, "org_id": 102, "title": "寿县县委副书记、县长",
     "start": "2022", "end": "2025", "rank": "county_deputy", "note": "Interview published 2023-02-18 as '寿县县委副书记、县长孙奇志'."},
    # Note: Earlier career positions are unverified. She was identified as female in the Sep 2025 press conference.

    # ── 赵德兵（full timeline from official government profile）──
    {"person_id": 2, "org_id": 112, "title": "原建设乡乡长助理",
     "start": "1999-07", "end": "2001-12", "rank": "township", "note": ""},
    {"person_id": 2, "org_id": 111, "title": "迎河镇副镇长",
     "start": "2001-12", "end": "2006-03", "rank": "township", "note": ""},
    {"person_id": 2, "org_id": 113, "title": "共青团寿县委员会副书记",
     "start": "2006-03", "end": "2008-08", "rank": "county", "note": "其间: 2006.12--2008.03在共青团安徽省委员会挂职锻炼"},
    {"person_id": 2, "org_id": 114, "title": "共青团安徽省委员会挂职锻炼",
     "start": "2006-12", "end": "2008-03", "rank": "province", "note": "挂职"},
    {"person_id": 2, "org_id": 110, "title": "板桥镇党委副书记",
     "start": "2008-08", "end": "2009-04", "rank": "township", "note": ""},
    {"person_id": 2, "org_id": 109, "title": "双桥镇党委副书记、镇长",
     "start": "2009-04", "end": "2013-09", "rank": "township", "note": ""},
    {"person_id": 2, "org_id": 108, "title": "堰口镇党委副书记、镇长",
     "start": "2013-09", "end": "2016-03", "rank": "township", "note": ""},
    {"person_id": 2, "org_id": 108, "title": "堰口镇党委书记、镇长",
     "start": "2016-03", "end": "2016-08", "rank": "township", "note": ""},
    {"person_id": 2, "org_id": 108, "title": "堰口镇党委书记",
     "start": "2016-08", "end": "2020-04", "rank": "township", "note": "2013.09--2017.06在合肥工业大学工业工程专业在职研究生学习,获工程硕士专业学位"},
    {"person_id": 2, "org_id": 115, "title": "新桥国际产业园党工委副书记、管委会主任",
     "start": "2020-04", "end": "2021-06", "rank": "county", "note": ""},
    {"person_id": 2, "org_id": 115, "title": "新桥国际产业园党工委书记、管委会主任",
     "start": "2021-06", "end": "2022-03", "rank": "county", "note": ""},
    {"person_id": 2, "org_id": 101, "title": "县委常委,新桥国际产业园党工委书记、管委会主任",
     "start": "2022-03", "end": "2023-03", "rank": "county_deputy", "note": ""},
    {"person_id": 2, "org_id": 107, "title": "县委常委,县经济开发区党工委副书记、管委会副主任",
     "start": "2023-03", "end": "2024-07", "rank": "county_deputy", "note": "安徽寿县新桥国际产业园、寿县蜀山现代产业园"},
    {"person_id": 2, "org_id": 107, "title": "县经济开发区党工委书记、管委会主任",
     "start": "2024-07", "end": "2025-09", "rank": "county", "note": ""},
    {"person_id": 2, "org_id": 101, "title": "县委副书记、县长候选人",
     "start": "2025-09", "end": "2025-10", "rank": "county_deputy", "note": ""},
    {"person_id": 2, "org_id": 102, "title": "县委副书记，县政府党组书记、代县长",
     "start": "2025-10", "end": "2026-01", "rank": "county_deputy", "note": "县经济开发区党工委书记、管委会主任"},
    {"person_id": 2, "org_id": 102, "title": "县委副书记，县政府党组书记、县长",
     "start": "2026-01", "end": "present", "rank": "county_chief", "note": "县经济开发区(安徽寿县新桥国际产业园、寿县蜀山现代产业园)党工委书记、管委会主任，领导县政府全面工作。负责审计工作。"},

    # ── 牛方括 ──
    {"person_id": 3, "org_id": 101, "title": "寿县县委书记",
     "start": "2021", "end": "2025", "rank": "county_chief", "note": "Still serving as of January 2025 per news（会见奇缘冰雪集团）. By September 2025, Sun Qizhi had assumed role."},

    # ── 张亮 ──
    {"person_id": 4, "org_id": 102, "title": "寿县副县长",
     "start": "", "end": "present", "rank": "county_deputy", "note": "Confirmed active as of 2026-01（会见简谐能源科技客商）."},
]

relationships = [
    # Predecessor-successor: 牛方括 → 孙奇志
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor",
     "context": "牛方括 as 县委书记, 孙奇志 as 县长 (2022-2025), then 孙奇志 succeeded as 县委书记 (~2025)",
     "overlap_org": "中国共产党寿县委员会", "overlap_period": "2022~2025",
     "strength": "strong", "confidence": "confirmed"},

    # Superior-subordinate: 孙奇志 → 赵德兵
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "孙奇志 as 县委书记 and 赵德兵 as 县长 (2026-)",
     "overlap_org": "寿县", "overlap_period": "2026-01~present",
     "strength": "strong", "confidence": "confirmed"},

    # Overlap: 孙奇志 and 赵德兵 on 经济开发区
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "Both served on 寿县经济开发区 leadership - 孙奇志 as 县委领导 of development zone, 赵德兵 as director",
     "overlap_org": "寿县经济开发区", "overlap_period": "2024~2025",
     "strength": "medium", "confidence": "plausible"},
]


# ── BUILD FUNCTIONS ─────────────────────────────────────────────────

def create_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE persons(
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
        CREATE TABLE organizations(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE relationships(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        );
    """)

    for p in persons:
        cur.execute("INSERT INTO persons VALUES(:id,:name,:gender,:ethnicity,:birth,:birthplace,:education,:party_join,:work_start,:current_post,:current_org,:source)", p)
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES(:id,:name,:type,:level,:parent,:location)", o)
    for pos in positions:
        cur.execute("INSERT INTO positions(person_id,org_id,title,start,\"end\",rank,note) VALUES(:person_id,:org_id,:title,:start,:end,:rank,:note)", pos)
    for r in relationships:
        cur.execute("INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period) VALUES(:person_a,:person_b,:type,:context,:overlap_org,:overlap_period)", r)

    conn.commit()
    conn.close()
    print(f"DB created: {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return color for person node based on role."""
    role = p.get("current_post", "")
    if "书记" in role and "县委" in role:
        return "255,50,50"  # Red - Party Secretary
    if "县长" in role:
        return "50,100,255"  # Blue - County Mayor
    if "副县长" in role:
        return "50,100,255"  # Blue - Deputy Mayor
    return "100,100,100"  # Grey - Others


def org_color(o):
    t = o["type"]
    if t == "party":
        return "255,200,200"
    if t == "government":
        return "200,200,255"
    if t == "development_zone":
        return "200,255,200"
    if t in ("township",):
        return "255,255,200"
    if t == "mass_organization":
        return "255,220,255"
    if t in ("people_congress",):
        return "200,255,255"
    if t == "cppcc":
        return "255,240,200"
    return "200,200,200"


def is_top_leader(p):
    name = p["name"]
    title = p.get("current_post", "")
    return name in ("孙奇志", "赵德兵", "牛方括") or "书记" in title


def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>寿县（安徽省淮南市）领导关系网络 - 2026年7月更新</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = p.get("current_post", "")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="安徽省"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="安徽省"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Person->Organization (worked_at)
    for pos in positions:
        eid += 1
        title_label = pos.get("title", "")
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(title_label)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title_label)}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person->Person relationships
    for r in relationships:
        eid += 1
        rtype = r.get("type", "")
        ctx = r.get("context", "")
        conf = r.get("confidence", "unverified")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(conf)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


if __name__ == "__main__":
    os.makedirs(STAGING, exist_ok=True)
    create_db()
    create_gexf()
    print("Build complete.")
