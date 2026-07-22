#!/usr/bin/env python3
"""
阳山县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
City: 清远市
County: 阳山县
Targets: 县委书记 & 县长

Research Date: 2026-07-22

Research Notes:
- 邓耀雄（县委书记）的身份已通过阳山县人民政府官网多篇2026年政务动态文章确认：
  http://www.yangshan.gov.cn/zxzx/zwyw/content/post_2167313.html (2026-07-17 高质量党建和发展工作会议)
  http://www.yangshan.gov.cn/zxzx/zwyw/content/post_2116778.html (2026-02-24 到黄坌镇调研百千万工程)
  http://www.yangshan.gov.cn/zxzx/zwyw/content/post_2159659.html (2026-06-24 到秤架瑶族乡调研)
  http://www.yangshan.gov.cn/zxzx/zwyw/content/post_2153672.html (2026-06-04 招商引资项目快调快处专题会议)
- 罗振宇（县长）的身份已通过阳山县人民政府官网领导之窗页面确认：
  http://www.yangshan.gov.cn/xxgk/ldzc/content/post_1473061.html
  简历：罗振宇，男，汉族，1979年1月生，研究生，中共党员。现任县委副书记、县长。
  2026年政务动态：http://www.yangshan.gov.cn/zxzx/zwyw/content/post_2120409.html (2026-03-05 调研督导重点工作)
  http://www.yangshan.gov.cn/zxzx/zwyw/content/post_2165357.html (2026-07-13 陪同顺德北滘商会考察)
- 曹贝宁（县委常委、副县长、党组副书记）身份确认：
  http://www.yangshan.gov.cn/xxgk/ldzc/content/post_2167907.html
  简历：曹贝宁，男，汉族，1976年10月生，本科，中共党员。
- 钟志华（县委常委、副县长）身份确认：
  http://www.yangshan.gov.cn/xxgk/ldzc/content/post_1473166.html
  简历：钟志华，女，汉族，1979年5月生，大学，中共党员。
- 黄泽鹏（副县长，挂职）身份确认：
  http://www.yangshan.gov.cn/xxgk/ldzc/content/post_1788711.html
  简历：黄泽鹏，男，汉族，1989年9月生，研究生，中共党员。（挂职，负责广清对口帮扶）
- 潘伟军（副县长、公安局局长）身份确认：
  http://www.yangshan.gov.cn/xxgk/ldzc/content/post_2093050.html
  简历：潘伟军，男，汉族，1977年10月生，大学，中共党员。
- 黄玉简（副县长）身份确认：
  http://www.yangshan.gov.cn/xxgk/ldzc/content/post_2092946.html
  简历：黄玉简，男，苗族，1984年3月生，大学，工学学士，中共党员。
- 邹华鹏（副县长）身份确认：
  http://www.yangshan.gov.cn/xxgk/ldzc/content/post_2167892.html
  简历：邹华鹏，男，汉族，1980年4月生，省委党校大学，中共党员。
- 欧金华（县政府党组成员、办公室主任）身份确认：
  http://www.yangshan.gov.cn/xxgk/ldzc/content/post_1707473.html
  简历：欧金华，男，汉族，1978年2月生，大学，中共党员。
- Baidu Baike and other encyclopedia sources (403/gov.cn timeouts): detailed career histories
  for most figures unavailable beyond the brief official bios.
- 邓耀雄's background (birth year, birthplace, education, prior positions) needs further research.
  His first appearance on yangshan.gov.cn as 县委书记 appears in early 2026 news.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

try:
    from gov_relation.runner import run_build
    USE_RUNNER = True
except ImportError:
    USE_RUNNER = False

# ── Slug & Paths ──
SLUG = "阳山县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
CANONICAL_DB = os.path.join(DATABASE_DIR, f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(GRAPH_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ══════════════════════════════════════════════════════════════════════════════
# RESEARCH DATA
# ══════════════════════════════════════════════════════════════════════════════
#
# CONFIDENCE KEY:
#   [C] = Confirmed — official government website / reliable multiple sources
#   [P] = Plausible — likely correct based on training data
#   [U] = Unverified — needs confirmation
#   [G] = Gap — information not available
# ══════════════════════════════════════════════════════════════════════════════

# ── Persons ──

persons = [
    # ════════════════════════════════════════════
    # CURRENT 县委书记 (Party Secretary)
    # ════════════════════════════════════════════

    # [C] 县委书记 — 邓耀雄
    # Confirmed by yangshan.gov.cn news: 2026-07-17, 2026-06-24, 2026-06-04, 2026-02-24
    {
        "id": 1,
        "name": "邓耀雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共阳山县委书记",
        "current_org": "中共阳山县委员会",
        "source": "[C] Confirmed by multiple official news articles on yangshan.gov.cn (2026-07-17, 2026-06-24, 2026-06-04, 2026-02-24). Current as of July 2026. Detailed career history requires further research."
    },

    # ════════════════════════════════════════════
    # CURRENT 县长 (County Mayor)
    # ════════════════════════════════════════════

    # [C] 县长 — 罗振宇
    # Confirmed by yangshan.gov.cn leadership page and multiple news articles
    {
        "id": 2,
        "name": "罗振宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳山县委副书记、县政府县长",
        "current_org": "阳山县人民政府",
        "source": "[C] Confirmed by yangshan.gov.cn leadership page (http://www.yangshan.gov.cn/xxgk/ldzc/content/post_1473061.html). Birth: 1979年1月，研究生. Multiple 2026 news articles confirm current role."
    },

    # ════════════════════════════════════════════
    # 县委常委、常务副县长
    # ════════════════════════════════════════════

    # [C] 县委常委、副县长（常务） — 曹贝宁
    {
        "id": 3,
        "name": "曹贝宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳山县委常委、县政府党组副书记、副县长",
        "current_org": "阳山县人民政府",
        "source": "[C] Confirmed by yangshan.gov.cn leadership page (http://www.yangshan.gov.cn/xxgk/ldzc/content/post_2167907.html). Birth: 1976年10月，本科. Also confirmed accompanying 邓耀雄 in 2026-02-24 news."
    },

    # ════════════════════════════════════════════
    # 县委常委、副县长
    # ════════════════════════════════════════════

    # [C] 县委常委、副县长 — 钟志华（女）
    {
        "id": 4,
        "name": "钟志华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳山县委常委、县政府党组成员、副县长",
        "current_org": "阳山县人民政府",
        "source": "[C] Confirmed by yangshan.gov.cn leadership page (http://www.yangshan.gov.cn/xxgk/ldzc/content/post_1473166.html). Birth: 1979年5月，大学. Also mentioned in 2026-07-13 news."
    },

    # ════════════════════════════════════════════
    # 副县长（挂职）
    # ════════════════════════════════════════════

    # [C] 副县长（挂职） — 黄泽鹏
    {
        "id": 5,
        "name": "黄泽鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳山县副县长（挂职）",
        "current_org": "阳山县人民政府",
        "source": "[C] Confirmed by yangshan.gov.cn leadership page (http://www.yangshan.gov.cn/xxgk/ldzc/content/post_1788711.html). Birth: 1989年9月，研究生. Specializes in 广州对口帮扶清远(阳山) work."
    },

    # ════════════════════════════════════════════
    # 副县长、公安局局长
    # ════════════════════════════════════════════

    # [C] 副县长、公安局局长 — 潘伟军
    {
        "id": 6,
        "name": "潘伟军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳山县政府党组成员、副县长、县公安局局长",
        "current_org": "阳山县人民政府",
        "source": "[C] Confirmed by yangshan.gov.cn leadership page (http://www.yangshan.gov.cn/xxgk/ldzc/content/post_2093050.html). Birth: 1977年10月，大学."
    },

    # ════════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════════

    # [C] 副县长 — 黄玉简
    {
        "id": 7,
        "name": "黄玉简",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1984年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学，工学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳山县政府党组成员、副县长",
        "current_org": "阳山县人民政府",
        "source": "[C] Confirmed by yangshan.gov.cn leadership page (http://www.yangshan.gov.cn/xxgk/ldzc/content/post_2092946.html). Birth: 1984年3月，大学，工学学士."
    },

    # ════════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════════

    # [C] 副县长 — 邹华鹏
    {
        "id": 8,
        "name": "邹华鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳山县政府党组成员、副县长",
        "current_org": "阳山县人民政府",
        "source": "[C] Confirmed by yangshan.gov.cn leadership page (http://www.yangshan.gov.cn/xxgk/ldzc/content/post_2167892.html). Birth: 1980年4月，省委党校大学."
    },

    # ════════════════════════════════════════════
    # 县政府党组成员、办公室主任
    # ════════════════════════════════════════════

    # [C] 县政府党组成员 — 欧金华
    {
        "id": 9,
        "name": "欧金华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳山县政府党组成员，县人民政府办公室党组书记、主任",
        "current_org": "阳山县人民政府办公室",
        "source": "[C] Confirmed by yangshan.gov.cn leadership page (http://www.yangshan.gov.cn/xxgk/ldzc/content/post_1707473.html). Birth: 1978年2月，大学."
    },
]

# ── Organizations ──

organizations = [
    {
        "id": 1,
        "name": "中共阳山县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共清远市委员会",
        "location": "广东省清远市阳山县"
    },
    {
        "id": 2,
        "name": "阳山县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "清远市人民政府",
        "location": "广东省清远市阳山县"
    },
    {
        "id": 3,
        "name": "阳山县人民政府办公室",
        "type": "政府",
        "level": "县级",
        "parent": "阳山县人民政府",
        "location": "广东省清远市阳山县"
    },
    {
        "id": 4,
        "name": "阳山县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "阳山县人民政府",
        "location": "广东省清远市阳山县"
    },
]

# ── Positions ──

positions = [
    # 邓耀雄 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共阳山县委书记", "start": "待查", "end": "至今", "rank": "正处级", "note": "[C] Confirmed by yangshan.gov.cn (2026-02-24 onward)"},

    # 罗振宇 — 县长
    {"person_id": 2, "org_id": 2, "title": "阳山县委副书记、县政府县长", "start": "待查", "end": "至今", "rank": "正处级", "note": "[C] Confirmed by yangshan.gov.cn leadership page"},
    {"person_id": 2, "org_id": 1, "title": "阳山县委副书记", "start": "待查", "end": "至今", "rank": "正处级", "note": "[C] Title confirmed on official bio"},

    # 曹贝宁 — 县委常委、常务副县长
    {"person_id": 3, "org_id": 1, "title": "阳山县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed"},
    {"person_id": 3, "org_id": 2, "title": "阳山县政府党组副书记、副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed by official bio"},

    # 钟志华 — 县委常委、副县长
    {"person_id": 4, "org_id": 1, "title": "阳山县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed"},
    {"person_id": 4, "org_id": 2, "title": "阳山县政府党组成员、副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed by official bio"},

    # 黄泽鹏 — 副县长（挂职）
    {"person_id": 5, "org_id": 2, "title": "阳山县副县长（挂职）", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed. 广州对口帮扶清远（阳山）挂职."},

    # 潘伟军 — 副县长、公安局局长
    {"person_id": 6, "org_id": 2, "title": "阳山县政府党组成员、副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed"},
    {"person_id": 6, "org_id": 4, "title": "阳山县公安局局长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed by official bio"},

    # 黄玉简 — 副县长
    {"person_id": 7, "org_id": 2, "title": "阳山县政府党组成员、副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed by official bio"},

    # 邹华鹏 — 副县长
    {"person_id": 8, "org_id": 2, "title": "阳山县政府党组成员、副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "[C] Confirmed by official bio"},

    # 欧金华 — 县政府党组成员、办公室主任
    {"person_id": 9, "org_id": 2, "title": "阳山县政府党组成员", "start": "待查", "end": "至今", "rank": "正科级", "note": "[C] Confirmed by official bio"},
    {"person_id": 9, "org_id": 3, "title": "阳山县人民政府办公室党组书记、主任", "start": "待查", "end": "至今", "rank": "正科级", "note": "[C] Confirmed by official bio"},
]

# ── Relationships ──
# Based on official sources: same-organization overlaps confirmed for current team.
# Deeper relationship evidence (prior co-work, same-school, predecessor-successor)
# requires additional research not available through current web access.

relationships = [
    # 邓耀雄 <-> 罗振宇: 书记-县长 搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政搭档", "overlap_org": "中共阳山县委员会/阳山县人民政府", "overlap_period": "2026至今", "strength": "strong", "confidence": "confirmed"},

    # 邓耀雄 <-> 曹贝宁: 县委班子
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委常委班子共事", "overlap_org": "中共阳山县委员会", "overlap_period": "2026至今", "strength": "strong", "confidence": "confirmed"},

    # 邓耀雄 <-> 钟志华: 县委班子
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委常委班子共事", "overlap_org": "中共阳山县委员会", "overlap_period": "2026至今", "strength": "strong", "confidence": "confirmed"},

    # 罗振宇 <-> 曹贝宁: 县长-常务副县长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县政府领导搭档（县长-常务副县长）", "overlap_org": "阳山县人民政府", "overlap_period": "2026至今", "strength": "strong", "confidence": "confirmed"},

    # 罗振宇 <-> 钟志华: 县长-副县长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县政府领导搭档", "overlap_org": "阳山县人民政府", "overlap_period": "2026至今", "strength": "strong", "confidence": "confirmed"},

    # 曹贝宁陪同邓耀雄调研（confirmed by 2026-02-24 news）
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "曹贝宁陪同邓耀雄到黄坌镇调研督导百千万工程", "overlap_org": "阳山县", "overlap_period": "2026-02-24", "strength": "strong", "confidence": "confirmed"},
]


# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

def build_with_runner():
    """Build using the gov_relation.runner if available."""
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )


def build_standalone():
    """Fallback build using raw sqlite3 + string-based GEXF generation."""
    # ── SQLite DB ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
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
            start TEXT DEFAULT '',
            end TEXT DEFAULT '',
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
            strength TEXT DEFAULT 'medium',
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"✅ SQLite DB written: {DB_PATH}")

    # ── GEXF Graph ──
    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    from datetime import datetime

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>阳山县领导班子工作关系网络 — 清远市阳山县</description>')
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
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        pid = p["id"]
        role_color = {
            1: "255,50,50",    # 县委书记 — red
            2: "50,100,255",    # 县长 — blue
        }.get(pid, "100,100,100")  # others — grey

        role = p["current_post"]
        org = p["current_org"]
        sz = "20.0" if pid in (1, 2) else "12.0"

        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{role_color.split(",")[0]}" g="{role_color.split(",")[1]}" b="{role_color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
    }
    for o in organizations:
        oid = o["id"]
        color = org_colors.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization edges (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person edges (relationships)
    for r in relationships:
        eid += 1
        weight = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["confidence"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph written: {GEXF_PATH}")

    # ── Summary ──
    print(f"\n📊 Summary:")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")


if __name__ == "__main__":
    import sys

    # Check if we should use canonical paths (--canonical flag)
    use_canonical = "--canonical" in sys.argv
    if use_canonical:
        import shutil
        os.makedirs(DATABASE_DIR, exist_ok=True)
        os.makedirs(GRAPH_DIR, exist_ok=True)

    if USE_RUNNER:
        build_with_runner()
    else:
        build_standalone()

    # If --canonical, also copy to canonical locations
    if use_canonical:
        import shutil
        if os.path.exists(DB_PATH):
            shutil.copy2(DB_PATH, CANONICAL_DB)
            print(f"✅ Copied DB to canonical: {CANONICAL_DB}")
        if os.path.exists(GEXF_PATH):
            shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
            print(f"✅ Copied GEXF to canonical: {CANONICAL_GEXF}")
