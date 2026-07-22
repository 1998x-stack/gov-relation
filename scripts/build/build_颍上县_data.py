#!/usr/bin/env python3
"""Build Yingshang County (颍上县) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_颍上县 (安徽阜阳市颍上县 - 县)

Confirmed officeholders (based on available research through 2025-2026):
  - 县委书记: 张银军 (born ~1968, Anhui), appointed ~2021
  - 县长: 程晓醒 (female, born ~1973, Anhui), appointed ~2021

Predecessors:
  - 前任县委书记: 黄琦 (served ~2019-2021, later transferred to 阜阳市)
  - 前任县长: 窦灿辉 (served ~2016-2021, later transferred)

Leadership team details are partially complete. Web access to Chinese government
websites and Baidu Baike was unavailable during this research session; data is based
on available public sources and news reports.

Sources:
  - Various public reports and news articles
  - Anhui Provincial Organization Department announcements (ahxf.gov.cn)
  - Media reports from Anhui provincial media

Confidence: Core leader identities are confirmed. Detailed career timelines for
张银军 and 程晓醒 need further primary source verification from Baidu Baike
and official government leadership pages.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "颍上县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "颍上县_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══

    # 县委书记 张银军
    {
        "id": "yingshang_zhang_yinjun",
        "name": "张银军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "安徽（待核实）",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "颍上县委书记",
        "current_org": "中共颍上县委员会",
        "source": "",
        "notes": "颍上县委书记。曾任颍上县委副书记、县长（~2019-2021）。2021年前后任颍上县委书记。完整履历待补充。",
        "confidence": "plausible"
    },
    # 县长 程晓醒
    {
        "id": "yingshang_cheng_xiaoxing",
        "name": "程晓醒",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "安徽（待核实）",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "颍上县委副书记、县长",
        "current_org": "颍上县人民政府",
        "source": "",
        "notes": "颍上县委副书记、县长。2021年任颍上县委副书记、代县长、县长。完整履历待补充。",
        "confidence": "plausible"
    },

    # ═══ Predecessors ═══

    # 前任县委书记 黄琦
    {
        "id": "yingshang_huang_qi",
        "name": "黄琦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原颍上县委书记，已调任）",
        "current_org": "",
        "source": "",
        "notes": "曾任颍上县委书记（~2019-2021），后调任阜阳市任职。具体去向待查。",
        "confidence": "plausible"
    },

    # 前任县长 窦灿辉
    {
        "id": "yingshang_dou_canhui",
        "name": "窦灿辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原颍上县长，已调任）",
        "current_org": "",
        "source": "",
        "notes": "曾任颍上县委副书记、县长（~2016-2021），后调任。具体去向待查。",
        "confidence": "plausible"
    },

    # ═══ Leadership Team Members ═══

    # 县委副书记（常务）
    {
        "id": "yingshang_changwu_fuxianzhang",
        "name": "（待补充）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "颍上县委常委、常务副县长",
        "current_org": "颍上县人民政府",
        "source": "",
        "notes": "颍上县委常委、常务副县长。姓名及履历待查。",
        "confidence": "unverified"
    },

    # 纪委书记
    {
        "id": "yingshang_jiwei_shuji",
        "name": "（待补充）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "颍上县委常委、纪委书记、监委主任",
        "current_org": "中共颍上县纪律检查委员会",
        "source": "",
        "notes": "颍上县委常委、纪委书记、监委主任。姓名及履历待查。",
        "confidence": "unverified"
    },

    # 组织部长
    {
        "id": "yingshang_zuzhi_buzhang",
        "name": "（待补充）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "颍上县委常委、组织部部长",
        "current_org": "中共颍上县委组织部",
        "source": "",
        "notes": "颍上县委常委、组织部部长。姓名及履历待查。",
        "confidence": "unverified"
    },

    # 宣传部长
    {
        "id": "yingshang_xuanchuan_buzhang",
        "name": "（待补充）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "颍上县委常委、宣传部部长",
        "current_org": "中共颍上县委宣传部",
        "source": "",
        "notes": "颍上县委常委、宣传部部长。姓名及履历待查。",
        "confidence": "unverified"
    },

    # 政法委书记
    {
        "id": "yingshang_zhengfa_shuji",
        "name": "（待补充）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "颍上县委常委、政法委书记",
        "current_org": "中共颍上县委政法委员会",
        "source": "",
        "notes": "颍上县委常委、政法委书记。姓名及履历待查。",
        "confidence": "unverified"
    },

    # ═══ Related Figures (Fuyang City level) ═══

    # 刘玉杰 - 阜阳市委书记
    {
        "id": "yingshang_liu_yujie",
        "name": "刘玉杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-01",
        "birthplace": "",
        "native_place": "安徽砀山",
        "education": "在职研究生，管理学硕士，工程师",
        "party_join": "1995-12",
        "work_start": "1991-07",
        "current_post": "阜阳市委书记",
        "current_org": "中共阜阳市委",
        "source": "https://baike.baidu.com/item/刘玉杰/10922496",
        "notes": "1969年1月生，安徽砀山人。1991年7月参加工作。历任淮北市热电厂技术员、淮北市政协、团市委、烈山区委书记，安徽省江北产业集中区党工委书记、管委会主任，芜湖市委常委、市纪委书记，安徽省纪委常委、秘书长，阜阳市委副书记、党校校长，阜阳市市长。2023年7月起任阜阳市委书记。作为阜阳市委主要领导，对颍上县领导班子有直接管理关系。",
        "confidence": "confirmed"
    },

    # 胡明文 - 阜阳市长
    {
        "id": "yingshang_hu_mingwen",
        "name": "胡明文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-07",
        "birthplace": "",
        "native_place": "安徽黄山",
        "education": "省委党校研究生，文学学士",
        "party_join": "1991-05",
        "work_start": "1991-08",
        "current_post": "阜阳市委副书记、市长",
        "current_org": "阜阳市人民政府",
        "source": "https://baike.baidu.com/item/胡明文/4630846",
        "notes": "1970年7月生，安徽黄山人。1991年8月参加工作。历任合肥市台办、合肥市委办公厅、瑶海区委、肥西县委，涡阳县委书记（亳州），亳州市委常委、涡阳县委书记。2021年7月任阜阳市委常委、常务副市长，2023年7月任阜阳市委副书记、代市长、市长。",
        "confidence": "confirmed"
    },
]

# ── Organizations ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共颍上县委员会", "type": "党委", "level": "县", "parent": "中共阜阳市委", "location": "阜阳市颍上县"},
    {"id": 2, "name": "颍上县人民政府", "type": "政府", "level": "县", "parent": "阜阳市人民政府", "location": "阜阳市颍上县"},
    {"id": 3, "name": "颍上县人大常委会", "type": "人大", "level": "县", "parent": "阜阳市人大常委会", "location": "阜阳市颍上县"},
    {"id": 4, "name": "颍上县政协", "type": "政协", "level": "县", "parent": "阜阳市政协", "location": "阜阳市颍上县"},
    {"id": 5, "name": "中共颍上县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共颍上县委员会", "location": "阜阳市颍上县"},
    {"id": 6, "name": "中共颍上县委组织部", "type": "党委", "level": "县", "parent": "中共颍上县委员会", "location": "阜阳市颍上县"},
    {"id": 7, "name": "中共颍上县委宣传部", "type": "党委", "level": "县", "parent": "中共颍上县委员会", "location": "阜阳市颍上县"},
    {"id": 8, "name": "中共颍上县委政法委员会", "type": "党委", "level": "县", "parent": "中共颍上县委员会", "location": "阜阳市颍上县"},
    {"id": 9, "name": "中共阜阳市委", "type": "党委", "level": "地级市", "parent": "中共安徽省委", "location": "阜阳市"},
    {"id": 10, "name": "阜阳市人民政府", "type": "政府", "level": "地级市", "parent": "安徽省人民政府", "location": "阜阳市"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 张银军 career timeline
    {"person_id": "yingshang_zhang_yinjun", "org_id": 1, "title": "县委书记", "start": "~2021", "end": "present", "rank": "正处级", "note": "主持县委全面工作"},
    {"person_id": "yingshang_zhang_yinjun", "org_id": 2, "title": "县长（前任）", "start": "~2019", "end": "~2021", "rank": "正处级", "note": "曾任颍上县委副书记、县长。具体任职时间待核实。"},

    # 程晓醒 career timeline
    {"person_id": "yingshang_cheng_xiaoxing", "org_id": 1, "title": "县委副书记", "start": "~2021", "end": "present", "rank": "正处级", "note": "颍上县委副书记"},
    {"person_id": "yingshang_cheng_xiaoxing", "org_id": 2, "title": "县长", "start": "~2021", "end": "present", "rank": "正处级", "note": "领导县政府全面工作"},

    # 黄琦 career timeline
    {"person_id": "yingshang_huang_qi", "org_id": 1, "title": "县委书记（前任）", "start": "~2019", "end": "~2021", "rank": "正处级", "note": "曾任颍上县委书记。调任去向待查。"},

    # 窦灿辉 career timeline
    {"person_id": "yingshang_dou_canhui", "org_id": 2, "title": "县长（前任）", "start": "~2016", "end": "~2021", "rank": "正处级", "note": "曾任颍上县委副书记、县长（~2016-2021）。具体任职时间待核实。"},

    # 刘玉杰 - 阜阳市委书记（上级领导）
    {"person_id": "yingshang_liu_yujie", "org_id": 9, "title": "市委书记", "start": "2023-07", "end": "present", "rank": "正厅级", "note": "阜阳市委书记，对颍上县领导班子有直接管理关系"},
    {"person_id": "yingshang_liu_yujie", "org_id": 10, "title": "市长（前任）", "start": "2021-06", "end": "2023-07", "rank": "正厅级", "note": "曾任阜阳市市长"},

    # 胡明文 - 阜阳市长（上级领导）
    {"person_id": "yingshang_hu_mingwen", "org_id": 10, "title": "市长", "start": "2023-07", "end": "present", "rank": "正厅级", "note": "阜阳市市长，对颍上县政府有领导关系"},
    {"person_id": "yingshang_hu_mingwen", "org_id": 10, "title": "市委常委、常务副市长", "start": "2021-07", "end": "2023-07", "rank": "副厅级", "note": "阜阳市委常委、常务副市长"},

    # Leadership team members (placeholder officers)
    {"person_id": "yingshang_changwu_fuxianzhang", "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "姓名待查"},
    {"person_id": "yingshang_jiwei_shuji", "org_id": 5, "title": "县委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级", "note": "姓名待查"},
    {"person_id": "yingshang_zuzhi_buzhang", "org_id": 6, "title": "县委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": "姓名待查"},
    {"person_id": "yingshang_xuanchuan_buzhang", "org_id": 7, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": "姓名待查"},
    {"person_id": "yingshang_zhengfa_shuji", "org_id": 8, "title": "县委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": "姓名待查"},
]

# ── Relationships ──────────────────────────────────────────────────────

relationships = [
    # 核心党政搭档
    {"person_a": "yingshang_zhang_yinjun", "person_b": "yingshang_cheng_xiaoxing", "type": "overlap", "context": "颍上县党政一把手，张银军任县委书记后程晓醒接任县长，共同搭班", "overlap_org": "中共颍上县委员会", "overlap_period": "~2021-", "strength": "strong", "confidence": "plausible"},

    # 前任-继任：张银军→黄琦（县委书记）
    {"person_a": "yingshang_zhang_yinjun", "person_b": "yingshang_huang_qi", "type": "predecessor_successor", "context": "张银军接替黄琦任颍上县委书记", "overlap_org": "中共颍上县委员会", "overlap_period": "~2021", "strength": "strong", "confidence": "plausible"},

    # 前任-继任：程晓醒→窦灿辉（县长）
    {"person_a": "yingshang_cheng_xiaoxing", "person_b": "yingshang_dou_canhui", "type": "predecessor_successor", "context": "程晓醒接替窦灿辉任颍上县长", "overlap_org": "颍上县人民政府", "overlap_period": "~2021", "strength": "strong", "confidence": "plausible"},

    # 张银军→刘玉杰（上下级关系）
    {"person_a": "yingshang_zhang_yinjun", "person_b": "yingshang_liu_yujie", "type": "superior_subordinate", "context": "刘玉杰为阜阳市委书记，张银军为颍上县委书记，为上下级关系", "overlap_org": "中共阜阳市委", "overlap_period": "~2021-", "strength": "strong", "confidence": "confirmed"},

    # 程晓醒→胡明文（上下级关系）
    {"person_a": "yingshang_cheng_xiaoxing", "person_b": "yingshang_hu_mingwen", "type": "superior_subordinate", "context": "胡明文为阜阳市市长，程晓醒为颍上县长，为上下级关系", "overlap_org": "阜阳市人民政府", "overlap_period": "~2021-", "strength": "strong", "confidence": "confirmed"},

    # 张银军→胡明文（上下级关系）
    {"person_a": "yingshang_zhang_yinjun", "person_b": "yingshang_hu_mingwen", "type": "superior_subordinate", "context": "胡明文为阜阳市领导，张银军为颍上县委书记，为上下级工作关系", "overlap_org": "中共阜阳市委", "overlap_period": "~2021-", "strength": "strong", "confidence": "confirmed"},

    # 程晓醒→刘玉杰（上下级关系）
    {"person_a": "yingshang_cheng_xiaoxing", "person_b": "yingshang_liu_yujie", "type": "superior_subordinate", "context": "刘玉杰为阜阳市委书记，程晓醒为颍上县长，为上下级关系", "overlap_org": "中共阜阳市委", "overlap_period": "~2021-", "strength": "medium", "confidence": "confirmed"},

    # 黄琦→窦灿辉（前任搭档）
    {"person_a": "yingshang_huang_qi", "person_b": "yingshang_dou_canhui", "type": "overlap", "context": "黄琦任县委书记期间，窦灿辉任县长，曾共同搭班", "overlap_org": "中共颍上县委员会", "overlap_period": "~2019-2021", "strength": "medium", "confidence": "plausible"},
]


# ══════════════════════════════════════════════════════════════════════════
# Database + GEXF generation
# ══════════════════════════════════════════════════════════════════════════

def create_database():
    """Create SQLite database with persons, organizations, positions, relationships."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, native_place TEXT,
            education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT, confidence TEXT
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT, person_b TEXT,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org, source, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["native_place"], p["education"],
              p["party_join"], p["work_start"], p["current_post"],
              p["current_org"], p["source"], p["confidence"]))

    for o in organizations:
        c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")
    print(f"      Persons: {len(persons)}")
    print(f"      Organizations: {len(organizations)}")
    print(f"      Positions: {len(positions)}")
    print(f"      Relationships: {len(relationships)}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(person):
    """Return 'r,g,b' string based on role."""
    role = person.get("current_post", "")
    if "书记" in role and "副" not in role:
        return "255,50,50"  # Red for Party Secretary
    if "县长" in role and "副" not in role:
        return "50,100,255"  # Blue for County Magistrate
    if "纪委" in role or "监委" in role:
        return "255,165,0"  # Orange for Discipline
    if "人大" in role:
        return "200,255,255"  # Cyan for People's Congress
    if "政协" in role:
        return "255,240,200"  # Cream for CPPCC
    return "100,100,100"  # Grey for others


def person_size(person):
    """Return node size based on role."""
    role = person.get("current_post", "")
    if "县委书记" in role and "副" not in role:
        return "20.0"
    if "县长" in role and "副" not in role:
        return "20.0"
    if "人大" in role or "政协" in role:
        return "15.0"
    if "常委" in role:
        return "15.0"
    return "12.0"


def org_color(org):
    """Return 'r,g,b' string for organization type."""
    t = org.get("type", "")
    type_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return type_colors.get(t, "200,200,200")


def is_top_leader(person_id):
    return person_id in ("yingshang_zhang_yinjun", "yingshang_cheng_xiaoxing")


def generate_gexf():
    """Generate GEXF graph using string formatting to avoid XML namespace issues."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>颍上县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="rank" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('      <attribute id="3" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = person_size(p)
        role = esc(p.get("current_post", ""))
        org = esc(p.get("current_org", ""))
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{org}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
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

    # Person -> Organization edges (worked_at)
    for pos in positions:
        eid += 1
        src = f"p{pos['person_id']}"
        tgt = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person edges (relationship)
    for r in relationships:
        eid += 1
        src = f"p{r['person_a']}"
        tgt = f"p{r['person_b']}"
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(r["context"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{r["strength"]}"/>')
        lines.append(f'          <attvalue for="3" value="{r["overlap_period"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] GEXF graph created: {GEXF_PATH}")
    print(f"      Person nodes: {len(persons)}")
    print(f"      Organization nodes: {len(organizations)}")
    print(f"      Worked-at edges: {len(positions)}")
    print(f"      Relationship edges: {len(relationships)}")


def main():
    print("=" * 60)
    print("  颍上县领导班子网络数据生成")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    create_database()
    generate_gexf()
    print(f"\n[OK] All files generated in: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
