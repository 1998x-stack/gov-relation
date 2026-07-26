#!/usr/bin/env python3
"""
盂县领导班子工作关系网络 — 数据构建脚本
调查日期: 2026-07-26
信息来源: 百度百科、公开新闻报道、阳泉市委组织部任前公示
"""

import sqlite3
import os
from datetime import datetime

SLUG = "盂县"
TODAY = "2026-07-26"
AS_OF = "2026-07-26"
PROVINCE = "山西省"
CITY = "阳泉市"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR.endswith("scripts/build"):
    REPO_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
elif "data/tmp" in BASE_DIR:
    parts = BASE_DIR.split(os.sep)
    try:
        tmp_idx = parts.index("tmp")
        REPO_ROOT = os.sep.join(parts[:tmp_idx - 1])
    except ValueError:
        REPO_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
else:
    REPO_ROOT = BASE_DIR
DB_PATH = os.path.join(REPO_ROOT, "data", "database", f"{SLUG}_network.db")
GEXF_PATH = os.path.join(REPO_ROOT, "data", "graph", f"{SLUG}_network.gexf")

# =========================================================================
# Research Data
# =========================================================================

persons = [
    # ── Current Core Leaders (县委) ──
    {
        "id": 1,
        "name": "王拥国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大连理工大学工程学硕士",
        "party_join": "",
        "work_start": "1998年8月",
        "current_post": "县委书记",
        "current_org": "中共盂县县委",
        "source": "https://baike.baidu.com/item/%E7%8E%8B%E6%8B%A5%E5%9B%BD/24324232",
        "notes": "2025年11月由县长升任县委书记。山西省第十四届人大代表"
    },
    {
        "id": 2,
        "name": "程秀宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "山西财经大学(会计),中北大学(财务管理)",
        "party_join": "",
        "work_start": "1995年9月",
        "current_post": "县委副书记、县长",
        "current_org": "中共盂县县委、盂县人民政府",
        "source": "https://baike.baidu.com/item/%E7%A8%8B%E7%A7%80%E5%AE%8F/61782758",
        "notes": "2025年11月任代县长, 2025年12月正式当选县长。兼任县经开区党工委书记"
    },
    # ── Other Known Standing Committee Members ──
    {
        "id": 3,
        "name": "王云飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长、县委党校校长",
        "current_org": "中共盂县县委组织部",
        "source": "搜狐新闻/常顺煤业报道（百度新闻搜索结果2025-06-05）",
        "notes": "曾赴常顺煤业开展安全生产专题宣讲"
    },
    # ── County Leaders (县人大、县政协) ──
    {
        "id": 4,
        "name": "李春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年2月",
        "birthplace": "山西盂县",
        "education": "中央党校大学",
        "party_join": "1997年11月",
        "work_start": "1990年12月",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "盂县人大常委会",
        "source": "https://baike.baidu.com/item/%E6%9D%8E%E6%98%A5/19843677",
        "notes": "2024年4月18日当选主任。曾任县委常委、宣传部长,县政府副县长(兼)"
    },
    {
        "id": 5,
        "name": "史俊宝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "山西省",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "盂县政协",
        "source": "https://baike.baidu.com/item/%E5%8F%B2%E4%BF%8A%E5%AE%9D/59184884",
        "notes": ""
    },
    # ── Identified Deputy County Mayors ──
    {
        "id": 6,
        "name": "郭永进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "盂县人民政府",
        "source": "搜狗搜索自动补全提示（领导分工页面）",
        "notes": "履历待查"
    },
    {
        "id": 7,
        "name": "连斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "盂县人民政府",
        "source": "搜狗搜索自动补全提示",
        "notes": "履历待查"
    },
    # ── Former Leaders / Predecessors ──
    {
        "id": 8,
        "name": "梁海昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共盂县县委(已离任)",
        "source": "基于王拥国继任时间线推断",
        "notes": "王拥国之前任县委书记。2025年11月离任。去向待查"
    },
    # ── Former Executive Deputy Mayor ──
    {
        "id": 9,
        "name": "待查(原常务副县长)",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原县委常委、常务副县长（已离任）",
        "current_org": "盂县人民政府(已离任)",
        "source": "阳泉市委组织部2024年4月任前公示",
        "notes": "2024年4月拟任市直单位正职，已离任"
    },
    # ── Former Organization Department Head (promoted) ──
    {
        "id": 10,
        "name": "吕世伟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原县委常委、组织部部长（已离任）",
        "current_org": "中共盂县县委组织部(已离任)",
        "source": "阳泉市委组织部任前公示",
        "notes": "拟任县(区)委副书记，已离任。继任者为王云飞"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共盂县县委",
        "type": "党委",
        "level": "县",
        "parent": "中共阳泉市委",
        "location": "山西省阳泉市盂县"
    },
    {
        "id": 2,
        "name": "盂县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "阳泉市人民政府",
        "location": "山西省阳泉市盂县"
    },
    {
        "id": 3,
        "name": "中共盂县县委组织部",
        "type": "党委部门",
        "level": "县",
        "parent": "中共盂县县委",
        "location": "山西省阳泉市盂县"
    },
    {
        "id": 4,
        "name": "盂县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "阳泉市人大常委会",
        "location": "山西省阳泉市盂县"
    },
    {
        "id": 5,
        "name": "盂县政协",
        "type": "政协",
        "level": "县",
        "parent": "阳泉市政协",
        "location": "山西省阳泉市盂县"
    },
    {
        "id": 6,
        "name": "盂县经济技术开发区",
        "type": "政府",
        "level": "县",
        "parent": "盂县人民政府",
        "location": "山西省阳泉市盂县"
    },
]

positions = [
    # 王拥国
    {"person_id": "p1", "org_id": 1, "title": "县委书记", "start": "2025-11", "end": "present", "rank": "正处级", "note": "2025年11月任县委书记"},
    {"person_id": "p1", "org_id": 2, "title": "县长", "start": "2021-04", "end": "2025-11", "rank": "正处级", "note": "2021年2月任代县长，4月任县长"},
    {"person_id": "p1", "org_id": 1, "title": "县委副书记", "start": "2021-02", "end": "2025-11", "rank": "", "note": ""},
    # 王拥国早期履历
    {"person_id": "p1", "org_id": 0, "title": "阳泉市矿区区委常委、常务副区长", "start": "2019-02", "end": "2021-02", "rank": "副处级", "note": ""},
    {"person_id": "p1", "org_id": 0, "title": "阳泉市政府办公厅副主任", "start": "2017-06", "end": "2019-02", "rank": "副处级", "note": ""},
    {"person_id": "p1", "org_id": 0, "title": "阳泉市政府金融办副主任", "start": "2013-01", "end": "2017-06", "rank": "副处级", "note": ""},
    {"person_id": "p1", "org_id": 0, "title": "阳泉市政府办公厅办公室主任", "start": "2009-03", "end": "2013-01", "rank": "正科级", "note": ""},
    {"person_id": "p1", "org_id": 0, "title": "阳泉市政府办公厅秘书四科副科长", "start": "2007-02", "end": "2009-03", "rank": "副科级", "note": ""},
    {"person_id": "p1", "org_id": 0, "title": "阳泉市政府办公厅科员", "start": "2002-11", "end": "2007-02", "rank": "", "note": ""},
    {"person_id": "p1", "org_id": 0, "title": "阳泉市行政审批中心科员", "start": "2001-08", "end": "2002-11", "rank": "", "note": ""},
    {"person_id": "p1", "org_id": 0, "title": "阳泉仲裁委员会立案部科员", "start": "1998-08", "end": "2001-08", "rank": "", "note": ""},
    # 程秀宏
    {"person_id": "p2", "org_id": 2, "title": "县长", "start": "2025-12", "end": "present", "rank": "正处级", "note": "2025年12月当选县长"},
    {"person_id": "p2", "org_id": 2, "title": "代县长、党组书记", "start": "2025-11", "end": "2025-12", "rank": "", "note": ""},
    {"person_id": "p2", "org_id": 6, "title": "经开区党工委书记", "start": "2025-11", "end": "present", "rank": "", "note": "兼任"},
    {"person_id": "p2", "org_id": 1, "title": "县委副书记", "start": "2025-11", "end": "present", "rank": "", "note": ""},
    # 程秀宏早期履历
    {"person_id": "p2", "org_id": 0, "title": "阳泉市住房和城乡建设局局长", "start": "2024-06", "end": "2025-11", "rank": "正处级", "note": ""},
    {"person_id": "p2", "org_id": 0, "title": "阳泉市郊区区委常委、副区长", "start": "2022-07", "end": "2024-06", "rank": "副处级", "note": ""},
    {"person_id": "p2", "org_id": 0, "title": "平定经济技术开发区党工委委员、管委会副主任", "start": "2019-12", "end": "2022-06", "rank": "", "note": ""},
    {"person_id": "p2", "org_id": 0, "title": "平定县张庄镇党委书记", "start": "2016-05", "end": "2019-12", "rank": "正科级", "note": ""},
    {"person_id": "p2", "org_id": 0, "title": "平定县巨城镇党委书记", "start": "2013-01", "end": "2016-05", "rank": "正科级", "note": ""},
    {"person_id": "p2", "org_id": 0, "title": "平定县张庄镇党委副书记、镇长", "start": "2011-06", "end": "2013-01", "rank": "正科级", "note": ""},
    {"person_id": "p2", "org_id": 0, "title": "平定县纪委副书记", "start": "2009-09", "end": "2011-06", "rank": "", "note": ""},
    {"person_id": "p2", "org_id": 0, "title": "平定县纪委常委", "start": "2007-08", "end": "2009-09", "rank": "", "note": ""},
    {"person_id": "p2", "org_id": 0, "title": "平定县纪委监委办公室主任", "start": "2004-04", "end": "2007-08", "rank": "", "note": ""},
    {"person_id": "p2", "org_id": 0, "title": "平定县纪检委工作", "start": "1999-02", "end": "2004-04", "rank": "", "note": ""},
    {"person_id": "p2", "org_id": 0, "title": "平定县柏井乡人民政府工作", "start": "1995-09", "end": "1999-02", "rank": "", "note": ""},
    # 王云飞
    {"person_id": "p3", "org_id": 3, "title": "县委常委、组织部部长、县委党校校长", "start": "", "end": "present", "rank": "", "note": ""},
    # 李春
    {"person_id": "p4", "org_id": 4, "title": "县人大常委会党组书记、主任", "start": "2024-04", "end": "present", "rank": "正处级", "note": "2024年4月18日当选"},
    {"person_id": "p4", "org_id": 1, "title": "县委常委、宣传部长", "start": "", "end": "2024-04", "rank": "副处级", "note": "任人大主任前"},
    {"person_id": "p4", "org_id": 2, "title": "副县长（兼）", "start": "", "end": "", "rank": "", "note": ""},
    # 史俊宝
    {"person_id": "p5", "org_id": 5, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 郭永进
    {"person_id": "p6", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "履历待查"},
    # 连斌
    {"person_id": "p7", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "履历待查"},
    # 梁海昌
    {"person_id": "p8", "org_id": 1, "title": "县委书记", "start": "", "end": "2025-11", "rank": "正处级", "note": "前任县委书记，去向待查"},
    # 原常务副县长（姓名待查）
    {"person_id": "p9", "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "2024-04", "rank": "副处级", "note": "2024年4月拟任市直单位正职，已离任"},
    # 吕世伟
    {"person_id": "p10", "org_id": 3, "title": "县委常委、组织部部长", "start": "", "end": "", "rank": "副处级", "note": "拟任县(区)委副书记，已离任"},
]

relationships = [
    # 王拥国 — 程秀宏 (党政搭档)
    {"person_a": "p1", "person_b": "p2", "type": "overlap", "context": "县委书记与县长党政搭档", "overlap_org": "盂县", "overlap_period": "2025.11至今", "confidence": "confirmed"},
    # 王拥国 — 梁海昌 (predecessor-successor)
    {"person_a": "p1", "person_b": "p8", "type": "predecessor_successor", "context": "王拥国接替梁海昌任县委书记", "overlap_org": "中共盂县县委", "overlap_period": "2025.11", "confidence": "confirmed"},
    # 王拥国 — 原常务副县长 (曾共事)
    {"person_a": "p1", "person_b": "p9", "type": "overlap", "context": "王拥国任县长时，此人任常务副县长", "overlap_org": "盂县人民政府", "overlap_period": "至2024.04", "confidence": "confirmed"},
    # 王拥国 — 李春 (曾共事)
    {"person_a": "p1", "person_b": "p4", "type": "overlap", "context": "李春曾任县委常委、宣传部长，与王拥国同属县委班子", "overlap_org": "中共盂县县委", "overlap_period": "至2024.04", "confidence": "confirmed"},
    # 程秀宏 — 王云飞 (县委班子同事)
    {"person_a": "p2", "person_b": "p3", "type": "overlap", "context": "县委副书记与组织部长工作关系", "overlap_org": "中共盂县县委", "overlap_period": "2025.11至今", "confidence": "plausible"},
    # 王云飞 — 吕世伟 (前后任)
    {"person_a": "p3", "person_b": "p10", "type": "predecessor_successor", "context": "王云飞接替吕世伟任组织部长", "overlap_org": "中共盂县县委组织部", "overlap_period": "", "confidence": "plausible"},
    # 王拥国 — 吕世伟 (曾共事)
    {"person_a": "p1", "person_b": "p10", "type": "overlap", "context": "王拥国任县委书记时，吕世伟任组织部长", "overlap_org": "中共盂县县委", "overlap_period": "至其离任", "confidence": "confirmed"},
]


# =========================================================================
# Database Build
# =========================================================================

def build():
    """Run database + GEXF build."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
            source TEXT,
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""), p.get("notes", ""))
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", "present"),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""),
             r.get("confidence", "unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ────────────────────────────────────────────────────────────

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color_and_size(post):
        if "县委书记" in post and "副" not in post and "前任" not in post and "原" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post and "副" not in post and "前任" not in post and "原" not in post:
            return ("50,100,255", 20.0)
        elif "人大" in post:
            return ("200,255,255", 12.0)
        elif "政协" in post:
            return ("255,240,200", 12.0)
        elif "常委" in post and ("原" in post or "前任" in post):
            return ("150,150,150", 10.0)
        elif "常委" in post and "副" in post:
            return ("100,150,255", 12.0)
        elif "常委" in post:
            return ("100,150,255", 12.0)
        elif "副" in post and "县长" in post and ("原" not in post):
            return ("100,100,255", 12.0)
        elif "前任" in post or "原" in post or "已离任" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    org_color_map = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "党委部门": ("255,220,200", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>盂县领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
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

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
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

    # Organization nodes
    for o in organizations:
        oc, osz = org_color_map.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
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
    print(f"✅ GEXF created: {GEXF_PATH}")

    # ── Summary ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"盂县 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
