#!/usr/bin/env python3
"""
五华县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
City: 梅州市
County: 五华县
Targets: 县委书记 & 县长

Research Date: 2026-07-22

Research Notes:
- 钟秀堂（县长）的身份已通过梅江区调查（guangdong_梅江区 task）交叉确认。
  钟秀堂，女，汉族，1974年4月生，广东大埔人，省委党校大学学历，中共党员，1995年参加工作。
  曾任梅江区区长（~2021-~2023），后调任五华县县长（~2023-现在）。
- 吴晖（前任县委书记）的信息基于训练数据知识，标注[P]。
- 朱少辉（前任县委书记/县长）的信息基于训练数据知识，标注[P]。
- 其他领导班子成员的信息基于训练数据知识和常见班子配置，所有未经验证的信息均标注[U]。
- 所有信息需在恢复网络访问后通过 wuhua.gov.cn 官方领导之窗页面核实。

CONFIDENCE KEY:
  [C] = Confirmed — official government website / reliable multiple sources
  [P] = Plausible — likely correct based on training data
  [U] = Unverified — needs confirmation
  [G] = Gap — information not available
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
SLUG = "五华县"
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

    # [P] 五华县委书记 — 朱少辉（推测为现任或近期任职）
    # 朱少辉曾任五华县县长，后接任县委书记。目前是否仍在任需确认。
    {
        "id": 1,
        "name": "朱少辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共五华县委书记（推测）",
        "current_org": "中共五华县委员会",
        "source": "[P] 朱少辉曾任五华县县长，后接任县委书记。具体任职时间和当前是否仍在任需通过 wuhua.gov.cn 确认。"
    },

    # ════════════════════════════════════════════
    # CURRENT 县长 (County Mayor)
    # ════════════════════════════════════════════

    # [P] 五华县县长 — 钟秀堂
    # 已通过梅江区调查报告交叉确认
    {
        "id": 2,
        "name": "钟秀堂",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年4月",
        "birthplace": "广东省梅州市大埔县",
        "native_place": "广东省梅州市大埔县",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "1995年",
        "current_post": "五华县委副书记、县人民政府县长",
        "current_org": "五华县人民政府",
        "source": "[P] 梅江区调查报告（guangdong_梅江区 task）确认钟秀堂从梅江区区长调任五华县县长。" +
                 "data/persons/20260722-广东省-梅州市-区长-钟秀堂.json 存档。" +
                 "五华县是梅州市面积最大、人口最多的县。待通过 wuhua.gov.cn 官方页面核实。"
    },

    # ════════════════════════════════════════════
    # PREDECESSORS — 县委书记
    # ════════════════════════════════════════════

    # [P] 前任县委书记 — 吴晖
    {
        "id": 3,
        "name": "吴晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任中共五华县委书记（~2019-~2021）",
        "current_org": "中共五华县委员会（原）",
        "source": "[P] 训练数据知识。吴晖曾任五华县委书记，后调往梅州市直部门。具体去向待查。"
    },

    # ════════════════════════════════════════════
    # PREDECESSORS — 县长
    # ════════════════════════════════════════════

    # [P] 前任县长 — 朱少辉（曾任职，后升县委书记）
    {
        "id": 4,
        "name": "朱少辉（前任县长职务）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任五华县人民政府县长",
        "current_org": "五华县人民政府（原）",
        "source": "[P] 训练数据知识。朱少辉曾任五华县县长，后升任五华县委书记。需确认具体时间线和是否存在其他人选。"
    },

    # ════════════════════════════════════════════
    # KEY DEPUTIES / 领导班子关键成员
    # ════════════════════════════════════════════

    # [U] 县委副书记（专职）
    {
        "id": 5,
        "name": "县委副书记（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共五华县委副书记（专职）",
        "current_org": "中共五华县委员会",
        "source": "Information gap — 五华县委专职副书记的姓名未通过现有网络渠道确认。"
    },

    # [U] 常务副县长
    {
        "id": 6,
        "name": "常务副县长（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "五华县委常委、常务副县长",
        "current_org": "五华县人民政府",
        "source": "Information gap — 五华县常务副县长的姓名未通过现有网络渠道确认。"
    },

    # [U] 县纪委书记
    {
        "id": 7,
        "name": "县纪委书记（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "五华县委常委、县纪委书记、县监委主任",
        "current_org": "中共五华县纪律检查委员会",
        "source": "Information gap — 五华县纪委书记的姓名未通过现有网络渠道确认。"
    },

    # [U] 县委组织部部长
    {
        "id": 8,
        "name": "组织部部长（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "五华县委常委、组织部部长",
        "current_org": "中共五华县委组织部",
        "source": "Information gap — 五华县委组织部部长的姓名未通过现有网络渠道确认。"
    },

    # [U] 县委宣传部部长
    {
        "id": 9,
        "name": "宣传部部长（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "五华县委常委、宣传部部长",
        "current_org": "中共五华县委宣传部",
        "source": "Information gap — 五华县委宣传部部长的姓名未通过现有网络渠道确认。"
    },

    # [U] 县委政法委书记
    {
        "id": 10,
        "name": "政法委书记（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "五华县委常委、政法委书记",
        "current_org": "中共五华县委政法委员会",
        "source": "Information gap — 五华县委政法委书记的姓名未通过现有网络渠道确认。"
    },

    # ════════════════════════════════════════════
    # CONNECTED FIGURES — 跨地区关联人物
    # ════════════════════════════════════════════

    # [P] 朱国城 — 五华人，现任梅州市人大常委会副主任
    {
        "id": 11,
        "name": "朱国城",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年10月",
        "birthplace": "广东省梅州市五华县",
        "native_place": "广东省梅州市五华县",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1987年",
        "current_post": "梅州市人大常委会副主任（副厅级）",
        "current_org": "梅州市人民代表大会常务委员会",
        "source": "[P] data/persons/20260722-广东省-梅州市-区委书记-朱国城.json 确认。" +
                 "五华人，曾任梅江区委书记、梅江区区长、梅州市政府副秘书长等职。"
    },
]

# ── Organizations ──

organizations = [
    {
        "id": 1,
        "name": "中共五华县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共梅州市委",
        "location": "广东省梅州市五华县水寨镇"
    },
    {
        "id": 2,
        "name": "五华县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "梅州市人民政府",
        "location": "广东省梅州市五华县水寨镇"
    },
    {
        "id": 3,
        "name": "中共五华县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共梅州市纪委",
        "location": "广东省梅州市五华县水寨镇"
    },
    {
        "id": 4,
        "name": "中共五华县委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共五华县委员会",
        "location": "广东省梅州市五华县水寨镇"
    },
    {
        "id": 5,
        "name": "中共五华县委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共五华县委员会",
        "location": "广东省梅州市五华县水寨镇"
    },
    {
        "id": 6,
        "name": "中共五华县委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共五华县委员会",
        "location": "广东省梅州市五华县水寨镇"
    },
    {
        "id": 7,
        "name": "五华县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "梅州市人民代表大会常务委员会",
        "location": "广东省梅州市五华县水寨镇"
    },
    {
        "id": 8,
        "name": "政协五华县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协梅州市委员会",
        "location": "广东省梅州市五华县水寨镇"
    },
    {
        "id": 9,
        "name": "五华县监察委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "梅州市监察委员会",
        "location": "广东省梅州市五华县水寨镇"
    },
    {
        "id": 10,
        "name": "梅州市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "广东省梅州市梅江区"
    },
]

# ── Positions ──

positions = [
    # 朱少辉 — 县委书记（推测当前）
    {"person_id": 1, "org_id": 1, "title": "五华县委书记", "start_date": "待查（推测~2021）", "end_date": "现在（待确认）", "rank": "正处级", "note": "[P] 朱少辉从县长升任县委书记。当前是否仍在任需核实。"},

    # 钟秀堂 — 县长（当前）
    {"person_id": 2, "org_id": 2, "title": "五华县人民政府县长", "start_date": "~2023", "end_date": "现在", "rank": "正处级", "note": "[P] 从梅江区区长平调/微调至五华县县长。"},
    {"person_id": 2, "org_id": 1, "title": "五华县委副书记", "start_date": "~2023", "end_date": "现在", "rank": "副处级", "note": "[P] 县长同时任县委副书记。"},

    # 吴晖 — 前任县委书记
    {"person_id": 3, "org_id": 1, "title": "五华县委书记", "start_date": "~2019", "end_date": "~2021", "rank": "正处级", "note": "[P] 前任县委书记。具体任期和去向待查。"},

    # 朱少辉 — 前任县长时间
    {"person_id": 4, "org_id": 2, "title": "五华县人民政府县长", "start_date": "待查", "end_date": "~2021", "rank": "正处级", "note": "[P] 朱少辉在升任县委书记前曾任五华县县长。"},

    # 朱国城 — 关联人物
    {"person_id": 11, "org_id": 10, "title": "梅州市人大常委会副主任", "start_date": "~2022", "end_date": "现在", "rank": "副厅级", "note": "[P] 五华人，从梅江区委书记升任。"},
    {"person_id": 11, "org_id": 1, "title": "曾关联（五华籍领导）", "start_date": "", "end_date": "", "rank": "", "note": "朱国城是五华县人，但职业生涯主要在梅州市和梅江区。此条仅标注地缘关联。"},

    # 领导班子其他成员（待查）
    {"person_id": 5, "org_id": 1, "title": "五华县委专职副书记", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[G] 姓名待查。"},
    {"person_id": 6, "org_id": 2, "title": "五华县委常委、常务副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[G] 姓名待查。"},
    {"person_id": 7, "org_id": 3, "title": "五华县委常委、县纪委书记、县监委主任", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[G] 姓名待查。"},
    {"person_id": 8, "org_id": 4, "title": "五华县委常委、组织部部长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[G] 姓名待查。"},
    {"person_id": 9, "org_id": 5, "title": "五华县委常委、宣传部部长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[G] 姓名待查。"},
    {"person_id": 10, "org_id": 6, "title": "五华县委常委、政法委书记", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "[G] 姓名待查。"},
]

# ── Relationships ──

relationships = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "县委书记与县长党政搭档",
     "overlap_org": "中共五华县委员会/五华县人民政府",
     "overlap_period": "~2023-现在（推测）"},

    # 前任-继任（县委书记）
    {"person_a": 3, "person_b": 1, "type": "前任_继任",
     "context": "吴晖→朱少辉，县委书记交接",
     "overlap_org": "中共五华县委员会",
     "overlap_period": "~2021"},

    # 前任-继任（县长）
    {"person_a": 4, "person_b": 2, "type": "前任_继任",
     "context": "朱少辉（县长任上）→钟秀堂，县长交接",
     "overlap_org": "五华县人民政府",
     "overlap_period": "~2023"},

    # 县长与前任书记的县长-书记关系
    {"person_a": 1, "person_b": 4, "type": "同一人不同职级",
     "context": "朱少辉先后担任五华县县长和县委书记",
     "overlap_org": "中共五华县委员会/五华县人民政府",
     "overlap_period": ""},

    # 地缘关联：朱国城（五华人）与五华县的关联
    {"person_a": 11, "person_b": 2, "type": "地缘关联",
     "context": "朱国城（五华人）与五华县领导的地缘关联",
     "overlap_org": "",
     "overlap_period": ""},

    # 跨县交流：钟秀堂从梅江区调任五华县
    {"person_a": 2, "person_b": 11, "type": "跨县交流",
     "context": "钟秀堂从梅江区调任五华县，朱国城曾任梅江区委书记。两人在梅江区可能有过工作交集。",
     "overlap_org": "梅江区",
     "overlap_period": "~2021-~2023"},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if USE_RUNNER:
    # ── Use gov_relation runner for DB, custom GEXF below ──
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH + ".tmp",  # Write runner GEXF to tmp, we'll overwrite
        overwrite=True,
    )
else:
    # ── Fallback: manual SQLite + GEXF ──

    conn = sqlite3.connect(DB_PATH)

    # Create tables
    conn.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
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

        CREATE TABLE relationships (
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

    # Insert persons
    for p in persons:
        conn.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p.get("current_post", ""), p.get("current_org", ""),
             p.get("source", ""))
        )

    # Insert organizations
    for o in organizations:
        conn.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    # Insert positions
    for pos in positions:
        conn.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos.get("title", ""),
             pos.get("start_date", ""), pos.get("end_date", ""),
             pos.get("rank", ""), pos.get("note", ""))
        )

    # Insert relationships
    for r in relationships:
        conn.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r.get("type", ""),
             r.get("context", ""), r.get("overlap_org", ""),
             r.get("overlap_period", ""))
        )

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# ── GEXF generation (string formatting to avoid namespace issues) ──
def _build_gexf():
    from datetime import datetime

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(current_post):
        if "书记" in current_post and "纪委" not in current_post:
            return "255,50,50"
        if "县长" in current_post or "区长" in current_post:
            return "50,100,255"
        if "纪委" in current_post or "监委" in current_post:
            return "255,165,0"
        return "100,100,100"

    def is_top_leader(p):
        return p["id"] in (1, 2, 3)

    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "200,255,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>{esc(SLUG)}领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('      <attribute id="5" title="org_type" type="string"/>')
    lines.append('      <attribute id="6" title="level" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p.get("current_post", ""))
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="training_data"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc = org_colors.get(o.get("type", ""), "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="5" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos.get("title", ""))}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("type", ""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r.get("type", ""))}"/>')
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
    print(f"GEXF created: {GEXF_PATH}")

_build_gexf()

# ── Summary ──
print(f"\n=== {SLUG} Data Build Summary ===")
print(f"Persons: {len(persons)}")
print(f"Organizations: {len(organizations)}")
print(f"Positions: {len(positions)}")
print(f"Relationships: {len(relationships)}")
print(f"DB: {DB_PATH}")
print(f"GEXF: {GEXF_PATH}")
print("Note: Most data is [P] plausible or [U] unverified. Verify through wuhua.gov.cn when web access is restored.")
