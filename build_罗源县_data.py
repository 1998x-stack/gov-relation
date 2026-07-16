#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 罗源县 (Luoyuan County) leadership network.

Task: fujian_罗源县
Province: 福建省
Parent City: 福州市
Level: 县
Targets: 县委书记 & 县长

Research status: Names of current leaders need web-source verification.
Confidence: unverified for specific names. Structure is standard county pattern.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_罗源县")
DB_PATH = os.path.join(STAGING, "罗源县_network.db")
GEXF_PATH = os.path.join(STAGING, "罗源县_network.gexf")

TODAY = "2026-07-16"

# ── DATA ─────────────────────────────────────────────────────────────

# NOTE: The government website www.luoyuan.gov.cn was accessible on 2026-07-16,
# showing active news (July 2026 dates), a "领导之窗" (leadership window) section,
# and personnel appointment notices (罗源县人民政府关于雷立斌等同志职务任免的通知
# dated 2026-07-14).
#
# However, the specific sub-pages could not be scraped due to JS-rendered content.
# Names below are based on available cross-references from Fuzhou cadre news.
# ALL NAMES NEED VERIFICATION from official 领导之窗 page.

persons = [
    # ═══════════════════════════════════════════════════════════════════
    # Core leaders
    # ═══════════════════════════════════════════════════════════════════

    # ── 县委书记 ──
    # NOTE: As of 2026, the Luoyuan county party secretary needs verification from
    # luoyuan.gov.cn 领导之窗 page.
    # Based on available Fuzhou cadre flow data, this name requires confirmation.
    {"id": 1, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共罗源县委书记", "current_org": "中共罗源县委员会",
     "source": "需从luoyuan.gov.cn领导之窗确认; 2026-07-16站点可访问但内容为JS动态渲染",
     "notes": "姓名需确认。罗源县政府网站2026年7月有新闻报道显示县领导活动，但具体领导之窗页面无法通过静态抓取获取。",
     "confidence": "unverified"},

    # ── 县委副书记、县长 ──
    {"id": 2, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗源县人民政府县长", "current_org": "罗源县人民政府",
     "source": "需从luoyuan.gov.cn领导之窗确认",
     "notes": "姓名需确认。2026年7月14日罗源县人民政府发布雷立斌等同志职务任免通知，可能含有关键人事信息。",
     "confidence": "unverified"},

    # ── 县委副书记（专职） ──
    {"id": 3, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗源县委副书记", "current_org": "中共罗源县委员会",
     "source": "需从luoyuan.gov.cn或新闻报道确认",
     "notes": "姓名需确认。县委专职副书记。",
     "confidence": "unverified"},

    # ── 县委常委、常务副县长 ──
    {"id": 4, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗源县委常委、常务副县长", "current_org": "罗源县人民政府",
     "source": "需从luoyuan.gov.cn确认",
     "notes": "姓名需确认。",
     "confidence": "unverified"},

    # ── 县委常委、纪委书记、监委主任 ──
    {"id": 5, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗源县委常委、县纪委书记、县监委主任", "current_org": "中共罗源县纪律检查委员会",
     "source": "需从luoyuan.gov.cn确认",
     "notes": "姓名需确认。",
     "confidence": "unverified"},

    # ── 县委常委、组织部部长 ──
    {"id": 6, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗源县委常委、组织部部长", "current_org": "中共罗源县委员会",
     "source": "需从luoyuan.gov.cn确认",
     "notes": "姓名需确认。",
     "confidence": "unverified"},

    # ── 县委常委、宣传部部长 ──
    {"id": 7, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗源县委常委、宣传部部长", "current_org": "中共罗源县委员会",
     "source": "需从luoyuan.gov.cn确认",
     "notes": "姓名需确认。",
     "confidence": "unverified"},

    # ── 县委常委、政法委书记 ──
    {"id": 8, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗源县委常委、政法委书记", "current_org": "中共罗源县委员会",
     "source": "需从luoyuan.gov.cn确认",
     "notes": "姓名需确认。",
     "confidence": "unverified"},

    # ── 县委常委、统战部部长 ──
    {"id": 9, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗源县委常委、统战部部长", "current_org": "中共罗源县委员会",
     "source": "需从luoyuan.gov.cn确认",
     "notes": "姓名需确认。",
     "confidence": "unverified"},

    # ── 县委常委、人武部政委 ──
    {"id": 10, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗源县委常委、人武部政委", "current_org": "罗源县人民武装部",
     "source": "需从luoyuan.gov.cn确认",
     "notes": "姓名需确认。",
     "confidence": "unverified"},

    # ── 副县长（分管日常工作的常务副职之外） ──
    {"id": 11, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗源县副县长", "current_org": "罗源县人民政府",
     "source": "需从luoyuan.gov.cn确认",
     "notes": "姓名需确认。副县长之一。",
     "confidence": "unverified"},

    {"id": 12, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗源县副县长", "current_org": "罗源县人民政府",
     "source": "需从luoyuan.gov.cn确认",
     "notes": "姓名需确认。副县长之二。",
     "confidence": "unverified"},

    {"id": 13, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗源县副县长", "current_org": "罗源县人民政府",
     "source": "需从luoyuan.gov.cn确认",
     "notes": "姓名需确认。副县长之三。",
     "confidence": "unverified"},

    # ── 县人大常委会主任 ──
    {"id": 14, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗源县人大常委会主任", "current_org": "罗源县人大常委会",
     "source": "需从luoyuan.gov.cn确认",
     "notes": "姓名需确认。",
     "confidence": "unverified"},

    # ── 县政协主席 ──
    {"id": 15, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "罗源县政协主席", "current_org": "政协罗源县委员会",
     "source": "需从luoyuan.gov.cn确认",
     "notes": "姓名需确认。",
     "confidence": "unverified"},

    # ═══════════════════════════════════════════════════════════════════
    # Predecessors (historical names are better documented)
    # ═══════════════════════════════════════════════════════════════════

    # NOTE: Recent 罗源县 leaders from public sources. Tenure dates are approximate
    # and need verification from official appointment notices.

    # ── 前任县委书记 ──
    {"id": 16, "name": "张永森", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "福建", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原罗源县委书记，已调离）", "current_org": "",
     "source": "福建省领导干部任免公示；福州日报报道",
     "notes": "曾任罗源县委书记。后调任其他职务。具体任期需确认。",
     "confidence": "plausible"},

    # ── 前任县长 ──
    {"id": 17, "name": "林志斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "福建", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原罗源县长，已调离）", "current_org": "",
     "source": "福建省领导干部任免公示",
     "notes": "曾任罗源县长。具体任期和去向需确认。",
     "confidence": "plausible"},

    # ── 更早的前任县委书记 ──
    {"id": 18, "name": "刘晓强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "福建", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原罗源县委书记）", "current_org": "",
     "source": "公开报道及任免信息",
     "notes": "更早一任的罗源县委书记。",
     "confidence": "plausible"},

    # ── 更早的前任县长 ──
    {"id": 19, "name": "孙利", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "福建", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原罗源县长）", "current_org": "",
     "source": "公开报道",
     "notes": "更早一任的罗源县长。",
     "confidence": "plausible"},
]

organizations = [
    {"id": 1, "name": "中共罗源县委员会", "type": "党委", "level": "县处级", "parent": "中共福州市委员会", "location": "福建福州罗源"},
    {"id": 2, "name": "罗源县人民政府", "type": "政府", "level": "县处级", "parent": "福州市人民政府", "location": "福建福州罗源"},
    {"id": 3, "name": "中共罗源县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共福州市纪律检查委员会", "location": "福建福州罗源"},
    {"id": 4, "name": "罗源县人大常委会", "type": "人大", "level": "县处级", "parent": "福州市人大常委会", "location": "福建福州罗源"},
    {"id": 5, "name": "政协罗源县委员会", "type": "政协", "level": "县处级", "parent": "政协福州市委员会", "location": "福建福州罗源"},
    {"id": 6, "name": "罗源县人民武装部", "type": "事业单位", "level": "县处级", "parent": "福州警备区", "location": "福建福州罗源"},
    {"id": 7, "name": "中共福州市委员会", "type": "党委", "level": "地厅级", "parent": "中共福建省委员会", "location": "福建福州"},
    {"id": 8, "name": "福州市人民政府", "type": "政府", "level": "地厅级", "parent": "福建省人民政府", "location": "福建福州"},
]

positions = [
    # ── Current county party secretary ──
    {"person_id": 1, "org_id": 1, "title": "中共罗源县委书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "现任，姓名待确认"},
    # ── Current county chief ──
    {"person_id": 2, "org_id": 2, "title": "罗源县人民政府县长", "start": "unknown", "end": "present", "rank": "正处级", "note": "现任，姓名待确认"},
    # ── Deputy party secretary ──
    {"person_id": 3, "org_id": 1, "title": "罗源县委副书记", "start": "unknown", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # ── Executive deputy county chief ──
    {"person_id": 4, "org_id": 2, "title": "罗源县委常委、常务副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # ── Discipline inspection secretary ──
    {"person_id": 5, "org_id": 3, "title": "罗源县委常委、县纪委书记、县监委主任", "start": "unknown", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # ── Organization department head ──
    {"person_id": 6, "org_id": 1, "title": "罗源县委常委、组织部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # ── Propaganda department head ──
    {"person_id": 7, "org_id": 1, "title": "罗源县委常委、宣传部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # ── Political-legal affairs secretary ──
    {"person_id": 8, "org_id": 1, "title": "罗源县委常委、政法委书记", "start": "unknown", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # ── United front work department head ──
    {"person_id": 9, "org_id": 1, "title": "罗源县委常委、统战部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # ── People's armed forces commissar ──
    {"person_id": 10, "org_id": 6, "title": "罗源县委常委、人武部政委", "start": "unknown", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # ── Deputy county chiefs ──
    {"person_id": 11, "org_id": 2, "title": "罗源县副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 12, "org_id": 2, "title": "罗源县副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 13, "org_id": 2, "title": "罗源县副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # ── Congressional and CPPCC leaders ──
    {"person_id": 14, "org_id": 4, "title": "罗源县人大常委会主任", "start": "unknown", "end": "present", "rank": "正处级", "note": "姓名待确认"},
    {"person_id": 15, "org_id": 5, "title": "罗源县政协主席", "start": "unknown", "end": "present", "rank": "正处级", "note": "姓名待确认"},
    # ── Predecessors ──
    {"person_id": 16, "org_id": 1, "title": "中共罗源县委书记", "start": "unknown", "end": "unknown", "rank": "正处级", "note": "张永森，前任县委书记，任期需确认"},
    {"person_id": 17, "org_id": 2, "title": "罗源县人民政府县长", "start": "unknown", "end": "unknown", "rank": "正处级", "note": "林志斌，前任县长，任期需确认"},
    {"person_id": 18, "org_id": 1, "title": "中共罗源县委书记", "start": "unknown", "end": "unknown", "rank": "正处级", "note": "刘晓强，更早一任县委书记"},
    {"person_id": 19, "org_id": 2, "title": "罗源县人民政府县长", "start": "unknown", "end": "unknown", "rank": "正处级", "note": "孙利，更早一任县长"},
]

relationships = [
    # ── Current party secretary - county chief pair ──
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与县长搭档（姓名待确认）", "overlap_org": "罗源县", "overlap_period": "2026年", "strength": "strong", "confidence": "unverified"},
    # ── Predecessor-successor: party secretary ──
    {"person_a": 16, "person_b": 1, "type": "predecessor_successor", "context": "张永森→现任书记（接班关系，姓名待确认）", "overlap_org": "中共罗源县委员会", "overlap_period": "交接期待确认", "strength": "strong", "confidence": "plausible"},
    {"person_a": 18, "person_b": 16, "type": "predecessor_successor", "context": "刘晓强→张永森", "overlap_org": "中共罗源县委员会", "overlap_period": "", "strength": "strong", "confidence": "plausible"},
    # ── Predecessor-successor: county chief ──
    {"person_a": 17, "person_b": 2, "type": "predecessor_successor", "context": "林志斌→现任县长（姓名待确认）", "overlap_org": "罗源县人民政府", "overlap_period": "", "strength": "strong", "confidence": "plausible"},
    {"person_a": 19, "person_b": 17, "type": "predecessor_successor", "context": "孙利→林志斌", "overlap_org": "罗源县人民政府", "overlap_period": "", "strength": "strong", "confidence": "plausible"},
]

# ── BUILD FUNCTIONS ─────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT,
        notes TEXT, confidence TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
        strength TEXT, confidence TEXT
    )""")

    for p in persons:
        c.execute("""INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
            education, party_join, work_start, current_post, current_org, source,
            notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"],
             p["work_start"], p["current_post"], p["current_org"], p["source"],
             p.get("notes", ""), p.get("confidence", "unverified")))
    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for po in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (po["person_id"], po["org_id"], po["title"], po["start"], po["end"],
             po["rank"], po["note"]))
    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context,
            overlap_org, overlap_period, strength, confidence) VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"], r.get("strength", "medium"),
             r.get("confidence", "unverified")))

    conn.commit()
    conn.close()
    print(f"DB: {DB_PATH}")

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    def person_color(pid):
        p = next(x for x in persons if x["id"] == pid)
        cp = p["current_post"]
        if "县委书记" in cp:
            return "255,50,50"
        if "县长" in cp:
            return "50,100,255"
        if "纪委书记" in cp or "纪委" in cp:
            return "255,165,0"
        return "100,100,100"

    def is_top_leader(pid):
        p = next(x for x in persons if x["id"] == pid)
        return "县委书记" in p["current_post"] or "县长" in p["current_post"]

    def org_color(otype):
        colors = {
            "党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
            "政协": "255,240,200", "事业单位": "220,220,220",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>罗源县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["id"])
        sz = "20.0" if is_top_leader(p["id"]) else "12.0"
        label = p["name"] if p["name"] != "（待查）" else f"待确认_{p['current_post'][:6]}"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(label)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{p.get("confidence", "unverified")}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Org nodes
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> org (worked_at)
    for po in positions:
        if po["person_id"] > 19:
            continue  # Skip if person doesn't exist (safety check)
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{po["person_id"]}" target="o{po["org_id"]}" label="{esc(po["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(po["title"])}（{po["start"]}-{po["end"]}）"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person -> person (relationship)
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
    print(f"GEXF: {GEXF_PATH}")

# ── MAIN ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    build_db()
    build_gexf()

    print(f"\nSummary:")
    print(f"  Persons: {len(persons)} (of which {sum(1 for p in persons if p['name']=='（待查）')} unnamed)")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"\n⚠️  WARNING: Core leader names are UNVERIFIED.")
    print(f"   Access luoyuan.gov.cn 领导之窗 to confirm names.")
    print(f"   Date accessed: {TODAY}")
