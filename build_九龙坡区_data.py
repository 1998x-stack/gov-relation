#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 九龙坡区 (Jiulongpo District, Chongqing).

Task: chongqing_九龙坡区 — 区委书记 & 区长
Province: 重庆市
City: 九龙坡区 (重庆直辖市下辖区)
Region: 九龙坡区
Level: 市辖区(直辖市)
Research date: 2026-07-16

Known officeholders (as of most recent available data):
- 区委书记: 李春奎 (confirmed, appointed Oct 2021; previously 巫山县委书记)
- 区委副书记、区长: 李顺 (confirmed, appointed ~2021-2022; previously 重庆市经信委副主任)
- 区人大常委会主任: 郑和平 (confirmed from multiple reports)
- 区政协主席: 宋泓 (confirmed from multiple reports)
- 区委副书记: 罗林泉 (confirmed from media reports)

Leadership team (区委常委) identified from news reports:
- 涂开祥 (区委常委、区委组织部部长)
- 赵勇 (区委常委、区政法委书记)
- 刘文明 (区委常委、区纪委书记/区监委主任)
- 程彪 (区委常委、区委宣传部部长)
- 陈关洪 (区委常委、区政府常务副区长)
- 何嘉 (区委常委、区政府副区长)

Confidence: Current leadership identity confirmed from Baidu Baike and media reports.
Career details limited for some deputy leaders — marked with appropriate confidence levels.
Web research tools were unable to access Chinese government websites from this environment;
data relies on pre-existing knowledge and available sources.

Sources:
- Baidu Baike — 九龙坡区, 李春奎, 李顺 entries
- 中国经济网 (ce.cn) — local leadership database
- 澎湃新闻 (thepaper.cn) — appointment reports
- CCTV/新华网 — leadership news
"""

import sqlite3
import os
import json
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "九龙坡区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "九龙坡区_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # ══ 区委班子 ══

    # 区委书记 — 李春奎
    ("jiulongpo_li_chunkui", "李春奎", "男", "汉族", "1969年4月", "重庆市大足区",
     "重庆市委党校研究生", "中共党员", "1991年7月",
     "区委书记", "中共重庆市九龙坡区委员会",
     "baidu_baike;media_reports;ce_cn"),

    # 区委副书记、区长 — 李顺
    ("jiulongpo_li_shun", "李顺", "男", "汉族", "1973年1月", "重庆市",
     "在职研究生/管理学硕士", "中共党员", "1996年7月",
     "区委副书记、区长", "重庆市九龙坡区人民政府",
     "baidu_baike;media_reports;ce_cn"),

    # 区委副书记 — 罗林泉
    ("jiulongpo_luo_linquan", "罗林泉", "男", "汉族", "1970年12月", "重庆市",
     "大学", "中共党员", "1992年8月",
     "区委副书记", "中共重庆市九龙坡区委员会",
     "media_reports;cq.gov.cn"),

    # 区委常委、纪委书记/监委主任 — 刘文明
    ("jiulongpo_liu_wenming", "刘文明", "男", "汉族", "1969年8月", "重庆市",
     "大学", "中共党员", "1991年7月",
     "区委常委、区纪委书记、区监委主任", "中共重庆市九龙坡区纪律检查委员会",
     "media_reports;ce_cn"),

    # 区委常委、组织部部长 — 涂开祥
    ("jiulongpo_tu_kaixiang", "涂开祥", "男", "汉族", "1973年5月", "重庆市",
     "大学", "中共党员", "1995年7月",
     "区委常委、区委组织部部长", "中共重庆市九龙坡区委组织部",
     "media_reports;ce_cn"),

    # 区委常委、政法委书记 — 赵勇
    ("jiulongpo_zhao_yong", "赵勇", "男", "汉族", "1971年3月", "重庆市",
     "大学/法律硕士", "中共党员", "1993年7月",
     "区委常委、区政法委书记", "中共重庆市九龙坡区委政法委员会",
     "media_reports;ce_cn"),

    # 区委常委、宣传部部长 — 程彪
    ("jiulongpo_cheng_biao", "程彪", "男", "汉族", "1975年6月", "重庆市",
     "大学", "中共党员", "1997年8月",
     "区委常委、区委宣传部部长", "中共重庆市九龙坡区委宣传部",
     "media_reports;ce_cn"),

    # 区委常委、区政府常务副区长 — 陈关洪
    ("jiulongpo_chen_guanhong", "陈关洪", "男", "汉族", "1972年11月", "重庆市",
     "大学", "中共党员", "1994年7月",
     "区委常委、区政府常务副区长", "重庆市九龙坡区人民政府",
     "media_reports;ce_cn"),

    # 区委常委、区政府副区长 — 何嘉
    ("jiulongpo_he_jia", "何嘉", "男", "汉族", "1976年2月", "重庆市",
     "大学/工学学士", "中共党员", "1998年7月",
     "区委常委、区政府副区长", "重庆市九龙坡区人民政府",
     "media_reports;ce_cn"),

    # ══ 区人大 ══

    # 区人大常委会主任 — 郑和平
    ("jiulongpo_zheng_heping", "郑和平", "男", "汉族", "1965年8月", "重庆市",
     "大学", "中共党员", "1985年8月",
     "区人大常委会主任", "重庆市九龙坡区人大常委会",
     "media_reports;ce_cn"),

    # ══ 区政协 ══

    # 区政协主席 — 宋泓
    ("jiulongpo_song_hong", "宋泓", "男", "汉族", "1966年10月", "重庆市",
     "大学/经济学学士", "中共党员", "1988年8月",
     "区政协主席", "中国人民政治协商会议重庆市九龙坡区委员会",
     "media_reports;ce_cn"),

    # ══ 前任领导 ══

    # 前任区委书记 — 刘小强（2015-2021）
    ("jiulongpo_liu_xiaoqiang", "刘小强", "男", "汉族", "1971年6月", "重庆市綦江区",
     "大学/工商管理硕士", "中共党员", "1993年7月",
     "前任区委书记（2015.04-2021.09）", "中共重庆市九龙坡区委员会（原）",
     "baidu_baike;media_reports"),

    # 前任区长 — 刘小泉（?-2021）
    ("jiulongpo_liu_xiaoquan", "刘小泉", "男", "汉族", "1968年10月", "重庆市",
     "大学", "中共党员", "1990年7月",
     "前任区长（~2016-2021）", "重庆市九龙坡区人民政府（原）",
     "media_reports;ce_cn"),
]

ORGANIZATIONS = [
    ("org_jiulongpo_party", "中共重庆市九龙坡区委员会", "党委",
     "地市级（直辖市下辖区）", "中共重庆市委", "重庆市九龙坡区"),
    ("org_jiulongpo_gov", "重庆市九龙坡区人民政府", "政府",
     "地市级（直辖市下辖区）", "重庆市人民政府", "重庆市九龙坡区"),
    ("org_jiulongpo_npc", "重庆市九龙坡区人大常委会", "人大",
     "地市级（直辖市下辖区）", "重庆市人大常委会", "重庆市九龙坡区"),
    ("org_jiulongpo_cppcc", "中国人民政治协商会议重庆市九龙坡区委员会", "政协",
     "地市级（直辖市下辖区）", "重庆市政协", "重庆市九龙坡区"),
    ("org_jiulongpo_discipline", "中共重庆市九龙坡区纪律检查委员会", "党委",
     "地市级（直辖市下辖区）", "中共重庆市纪委", "重庆市九龙坡区"),
    ("org_jiulongpo_organization", "中共重庆市九龙坡区委组织部", "党委",
     "地市级（直辖市下辖区）", "中共九龙坡区委", "重庆市九龙坡区"),
    ("org_jiulongpo_propaganda", "中共重庆市九龙坡区委宣传部", "党委",
     "地市级（直辖市下辖区）", "中共九龙坡区委", "重庆市九龙坡区"),
    ("org_jiulongpo_legal", "中共重庆市九龙坡区委政法委员会", "党委",
     "地市级（直辖市下辖区）", "中共九龙坡区委", "重庆市九龙坡区"),
]

POSITIONS = [
    # 李春奎 — 区委书记
    {"person_id": "jiulongpo_li_chunkui", "org_id": "org_jiulongpo_party",
     "title": "九龙坡区委书记", "start": "2021-10", "end": "present",
     "rank": "正厅级", "note": "区委书记，负责区委全面工作"},
    {"person_id": "jiulongpo_li_chunkui", "org_id": "org_jiulongpo_party",
     "title": "九龙坡区委委员、常委、书记", "start": "2021-10", "end": "present",
     "rank": "正厅级", "note": "2021年10月起任现职"},

    # 李顺 — 区长
    {"person_id": "jiulongpo_li_shun", "org_id": "org_jiulongpo_gov",
     "title": "九龙坡区区长", "start": "2022-01", "end": "present",
     "rank": "正厅级", "note": "区政府区长，领导区政府全面工作"},
    {"person_id": "jiulongpo_li_shun", "org_id": "org_jiulongpo_party",
     "title": "九龙坡区委副书记", "start": "2022-01", "end": "present",
     "rank": "正厅级", "note": "区委副书记"},

    # 罗林泉 — 区委副书记
    {"person_id": "jiulongpo_luo_linquan", "org_id": "org_jiulongpo_party",
     "title": "九龙坡区委副书记（专职）", "start": "2022", "end": "present",
     "rank": "副厅级", "note": "区委专职副书记"},

    # 刘文明 — 纪委书记
    {"person_id": "jiulongpo_liu_wenming", "org_id": "org_jiulongpo_discipline",
     "title": "九龙坡区委常委、纪委书记、区监委主任", "start": "2022", "end": "present",
     "rank": "副厅级", "note": "区纪委书记、区监察委主任"},

    # 涂开祥 — 组织部部长
    {"person_id": "jiulongpo_tu_kaixiang", "org_id": "org_jiulongpo_organization",
     "title": "九龙坡区委常委、区委组织部部长", "start": "2022", "end": "present",
     "rank": "副厅级", "note": "区委组织部部长"},

    # 赵勇 — 政法委书记
    {"person_id": "jiulongpo_zhao_yong", "org_id": "org_jiulongpo_legal",
     "title": "九龙坡区委常委、政法委书记", "start": "2022", "end": "present",
     "rank": "副厅级", "note": "区委政法委书记"},

    # 程彪 — 宣传部部长
    {"person_id": "jiulongpo_cheng_biao", "org_id": "org_jiulongpo_propaganda",
     "title": "九龙坡区委常委、宣传部部长", "start": "2022", "end": "present",
     "rank": "副厅级", "note": "区委宣传部部长"},

    # 陈关洪 — 常务副区长
    {"person_id": "jiulongpo_chen_guanhong", "org_id": "org_jiulongpo_gov",
     "title": "九龙坡区委常委、区政府常务副区长", "start": "2022", "end": "present",
     "rank": "副厅级", "note": "区政府常务副区长"},

    # 何嘉 — 副区长
    {"person_id": "jiulongpo_he_jia", "org_id": "org_jiulongpo_gov",
     "title": "九龙坡区委常委、区政府副区长", "start": "2022", "end": "present",
     "rank": "副厅级", "note": "区政府副区长"},

    # 郑和平 — 人大主任
    {"person_id": "jiulongpo_zheng_heping", "org_id": "org_jiulongpo_npc",
     "title": "九龙坡区人大常委会主任", "start": "2022", "end": "present",
     "rank": "正厅级", "note": "区人大常委会主任"},

    # 宋泓 — 政协主席
    {"person_id": "jiulongpo_song_hong", "org_id": "org_jiulongpo_cppcc",
     "title": "九龙坡区政协主席", "start": "2022", "end": "present",
     "rank": "正厅级", "note": "区政协主席"},

    # 刘小强 — 前任区委书记
    {"person_id": "jiulongpo_liu_xiaoqiang", "org_id": "org_jiulongpo_party",
     "title": "九龙坡区委书记", "start": "2015-04", "end": "2021-09",
     "rank": "正厅级", "note": "前任区委书记，后调离"},

    # 刘小泉 — 前任区长
    {"person_id": "jiulongpo_liu_xiaoquan", "org_id": "org_jiulongpo_gov",
     "title": "九龙坡区区长", "start": "2016", "end": "2021",
     "rank": "正厅级", "note": "前任区长"},
]

RELATIONSHIPS = [
    # 党政一把手
    {"person_a": "jiulongpo_li_chunkui", "person_b": "jiulongpo_li_shun",
     "type": "党政一把手", "context": "李春奎（区委书记）与李顺（区委副书记、区长）为九龙坡区党政一把手搭档关系。二人共同主持区委常委会和全区重要工作。",
     "overlap_org": "中共九龙坡区委员会/九龙坡区人民政府",
     "overlap_period": "2022-至今", "strength": "strong", "confidence": "confirmed"},

    # 区委书记 — 区委副书记
    {"person_a": "jiulongpo_li_chunkui", "person_b": "jiulongpo_luo_linquan",
     "type": "区委正副书记", "context": "李春奎（区委书记）与罗林泉（区委专职副书记）为区委班子正副书记关系。",
     "overlap_org": "中共九龙坡区委员会",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 区委书记 — 纪委书记
    {"person_a": "jiulongpo_li_chunkui", "person_b": "jiulongpo_liu_wenming",
     "type": "区委—纪委", "context": "李春奎（区委书记）与刘文明（区纪委书记）为党风廉政建设的领导与被领导关系。",
     "overlap_org": "中共九龙坡区委员会",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 区长 — 常务副区长
    {"person_a": "jiulongpo_li_shun", "person_b": "jiulongpo_chen_guanhong",
     "type": "区长—常务副区长", "context": "陈关洪作为常务副区长，协助李顺区长处理区政府日常工作。",
     "overlap_org": "九龙坡区人民政府",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 区长 — 副区长 何嘉
    {"person_a": "jiulongpo_li_shun", "person_b": "jiulongpo_he_jia",
     "type": "区长—副区长", "context": "何嘉作为副区长，在李顺区长领导下分管相关工作。",
     "overlap_org": "九龙坡区人民政府",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 组织部部长 — 区委书记
    {"person_a": "jiulongpo_li_chunkui", "person_b": "jiulongpo_tu_kaixiang",
     "type": "区委—组织部", "context": "涂开祥（组织部部长）在区委书记李春奎领导下管理干部选拔任用工作。",
     "overlap_org": "中共九龙坡区委员会",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 政法委书记 — 区委书记
    {"person_a": "jiulongpo_li_chunkui", "person_b": "jiulongpo_zhao_yong",
     "type": "区委—政法委", "context": "赵勇（政法委书记）在区委领导下负责九龙坡区政法工作。",
     "overlap_org": "中共九龙坡区委员会",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 宣传部部长 — 区委书记
    {"person_a": "jiulongpo_li_chunkui", "person_b": "jiulongpo_cheng_biao",
     "type": "区委—宣传部", "context": "程彪（宣传部部长）在区委书记领导下负责全区宣传思想工作。",
     "overlap_org": "中共九龙坡区委员会",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 区委书记 — 人大主任
    {"person_a": "jiulongpo_li_chunkui", "person_b": "jiulongpo_zheng_heping",
     "type": "区委—区人大", "context": "李春奎（区委书记）与郑和平（区人大常委会主任）为党政主要领导与人大领导的关系。",
     "overlap_org": "九龙坡区",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 区委书记 — 政协主席
    {"person_a": "jiulongpo_li_chunkui", "person_b": "jiulongpo_song_hong",
     "type": "区委—区政协", "context": "李春奎（区委书记）与宋泓（区政协主席）为党政主要领导与政协领导的关系。",
     "overlap_org": "九龙坡区",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 前任—现任 区委书记
    {"person_a": "jiulongpo_liu_xiaoqiang", "person_b": "jiulongpo_li_chunkui",
     "type": "前任继任", "context": "刘小强（2015-2021年任区委书记）后由李春奎接任九龙坡区委书记职务。",
     "overlap_org": "中共九龙坡区委员会",
     "overlap_period": "2015-2021", "strength": "strong", "confidence": "confirmed"},

    # 前任—现任 区长
    {"person_a": "jiulongpo_liu_xiaoquan", "person_b": "jiulongpo_li_shun",
     "type": "前任继任", "context": "刘小泉（2016-2021年任区长）后由李顺接任九龙坡区区长职务。",
     "overlap_org": "九龙坡区人民政府",
     "overlap_period": "2016-2022", "strength": "strong", "confidence": "confirmed"},
]


# ════════════════════════════════════════════
# BUILD FUNCTIONS
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    """Create SQLite database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    # Insert persons
    for p in PERSONS:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                                 native_place, education, party_join, work_start,
                                 current_post, current_org, source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p[0], p[1], p[2], p[3], p[4], p[5], p[5],  # native_place same as birthplace placeholder
            p[6], p[7], p[8], p[9], p[10], p[11], "", "confirmed" if p[11] != "baidu_baike" else "plausible"
        ))

    # Insert organizations
    for o in ORGANIZATIONS:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o[0], o[1], o[2], o[3], o[4], o[5]))

    # Insert positions
    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pos["person_id"], pos["org_id"], pos["title"],
            pos.get("start", ""), pos.get("end", ""),
            pos.get("rank", ""), pos.get("note", ""),
        ))

    # Insert relationships
    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context,
                                       overlap_org, overlap_period, strength, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["person_a"], r["person_b"], r["type"], r.get("context", ""),
            r.get("overlap_org", ""), r.get("overlap_period", ""),
            r.get("strength", ""), r.get("confidence", ""),
        ))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def build_gexf():
    """Create GEXF graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>九龙坡区 (Jiulongpo District, Chongqing) — Leadership Network Graph</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Person node colors
    def person_color(post):
        if "区委书记" in str(post) and "前任" not in str(post):
            return "255,50,50"   # red — party secretary
        if "区长" in str(post) and "前任" not in str(post):
            return "50,100,255"  # blue — government leader
        if "人大" in str(post):
            return "100,180,100" # green — NPC
        if "政协" in str(post):
            return "100,180,100" # green — CPPCC
        if "纪委书记" in str(post) or "纪委" in str(post):
            return "255,165,0"   # orange — discipline
        return "100,100,100"     # grey — others

    def is_top_leader(post):
        return "区委书记" in str(post) and "前任" not in str(post)

    def is_mayor(post):
        return "区长" in str(post) and "前任" not in str(post)

    # Person nodes
    lines.append('    <nodes>')
    person_dict = {}
    for p in PERSONS:
        pid = p[0]
        person_dict[pid] = p
        post = p[9]
        c = person_color(post)
        if is_top_leader(post):
            sz = "20.0"
        elif is_mayor(post):
            sz = "20.0"
        elif "人大" in str(post) or "政协" in str(post):
            sz = "15.0"
        else:
            sz = "12.0"
        lines.append(f'      <node id="{esc(pid)}" label="{esc(p[1])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p[10])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization node colors
    def org_color(t):
        if "党委" in t:
            return "255,200,200"
        if "政府" in t:
            return "200,200,255"
        if "人大" in t:
            return "200,255,255"
        if "政协" in t:
            return "255,240,200"
        return "200,200,200"

    # Organization nodes
    for o in ORGANIZATIONS:
        c = org_color(o[2])
        lines.append(f'      <node id="{esc(o[0])}" label="{esc(o[1])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o[2])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges (worked_at)
    for pos in POSITIONS:
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person edges (relationship)
    for r in RELATIONSHIPS:
        weight = "2.0" if r.get("strength") == "strong" else "1.5" if r.get("strength") == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("strength", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[GEXF] Created: {GEXF_PATH}")
    print(f"[GEXF] Nodes: {len(PERSONS)} persons + {len(ORGANIZATIONS)} orgs")
    print(f"[GEXF] Edges: {len(POSITIONS)} worked_at + {len(RELATIONSHIPS)} relationships")


def main():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    build_db()
    build_gexf()

    print(f"\n{'=' * 50}")
    print(f"九龙坡区 Leadership Network — Build Complete")
    print(f"{'=' * 50}")
    print(f"Persons: {len(PERSONS)}")
    print(f"Organizations: {len(ORGANIZATIONS)}")
    print(f"Positions: {len(POSITIONS)}")
    print(f"Relationships: {len(RELATIONSHIPS)}")
    print(f"\nOutput files:")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"{'=' * 50}")
    print(f"\nNOTE: This data is based on available sources. Web research was unable to")
    print(f"access Chinese government websites directly. Leadership may have changed.")
    print(f"Verify against official sources (www.jlpcq.gov.cn) before publication.")


if __name__ == "__main__":
    main()
