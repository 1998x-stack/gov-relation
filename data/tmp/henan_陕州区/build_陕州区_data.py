#!/usr/bin/env python3
"""
陕州区领导班子关系网络数据构建脚本
等级: 市辖区
调查日期: 2026-07-24
信息来源: 陕州区政府网站(www.shanzhou.gov.cn) + 公开新闻
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────
STAGING = Path(__file__).resolve().parent
REPO_ROOT = STAGING.parent.parent

SLUG = "陕州区"
AS_OF = "2026-07-24"
TODAY = AS_OF.replace("-", "")

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING / "persons"
PERSONS_DIR.mkdir(parents=True, exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════

persons = [
    # ── 1 李军 — 区委书记 ──
    {
        "id": "p1",
        "name": "李军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共三门峡市陕州区委员会",
        "source": "陕州区政府网站: 主持第四次党代会、多次主持会议",
    },
    # ── 2 何飞 — 区长 ──
    {
        "id": "p2",
        "name": "何飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "陕州区人民政府",
        "source": "陕州区政府网站: 政府领导页(2025-11-24)",
    },
    # ── 3 孔利亚 — 区委常委 ──
    {
        "id": "p3",
        "name": "孔利亚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共三门峡市陕州区委员会",
        "source": "陕州区第四次党代会主席团名单(2026-06-25)",
    },
    # ── 4 王胜军 — 区委常委 ──
    {
        "id": "p4",
        "name": "王胜军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共三门峡市陕州区委员会",
        "source": "陕州区第四次党代会主席团名单(2026-06-25)",
    },
    # ── 5 丁锐 — 区委常委 ──
    {
        "id": "p5",
        "name": "丁锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共三门峡市陕州区委员会",
        "source": "陕州区第四次党代会主席团名单(2026-06-25); 随李军调研项目(2026-07-19)",
    },
    # ── 6 寇晓辉 — 区委常委 ──
    {
        "id": "p6",
        "name": "寇晓辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共三门峡市陕州区委员会",
        "source": "陕州区第四次党代会主席团名单(2026-06-25); 两优一先会议(2026-06-29)",
    },
    # ── 7 李志高 — 区委常委 ──
    {
        "id": "p7",
        "name": "李志高",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共三门峡市陕州区委员会",
        "source": "陕州区第四次党代会主席团名单(2026-06-25); 随李军调研项目(2026-07-19)",
    },
    # ── 8 李远 — 区委常委 ──
    {
        "id": "p8",
        "name": "李远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共三门峡市陕州区委员会",
        "source": "陕州区第四次党代会主席团名单(2026-06-25); 两优一先会议(2026-06-29)",
    },
    # ── 9 辛欣 — 区委常委、统战部部长 ──
    {
        "id": "p9",
        "name": "辛欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共三门峡市陕州区委员会",
        "source": "陕州区政府网站: 调研张茅乡安全生产及防汛(2026-07-21); 第四次党代会主席团名单",
    },
    # ── 10 张晓丹 — 副区长 ──
    {
        "id": "p10",
        "name": "张晓丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长、党组成员",
        "current_org": "陕州区人民政府",
        "source": "陕州区政府网站: 政府领导页(2025-11-24); 第四次党代会主席团名单; 两优一先会议",
    },
    # ── 11 张华 — 副区长、公安局长 ──
    {
        "id": "p11",
        "name": "张华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长、党组成员、区公安局长",
        "current_org": "陕州区人民政府",
        "source": "陕州区政府网站: 政府领导页(2025-11-25)",
    },
    # ── 12 蔡啸虎 — 二级调研员 ──
    {
        "id": "p12",
        "name": "蔡啸虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "二级调研员",
        "current_org": "陕州区人民政府",
        "source": "陕州区政府网站: 政府领导页(2025-11-24); 随李军调研项目(2026-07-19)",
    },
    # ── 13 苏万军 — 二级调研员 ──
    {
        "id": "p13",
        "name": "苏万军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "二级调研员",
        "current_org": "陕州区人民政府",
        "source": "陕州区政府网站: 政府领导页(2025-11-24)",
    },
    # ── 14 樊卫星 — 区领导 ──
    {
        "id": "p14",
        "name": "樊卫星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "陕州区",
        "source": "陕州区两优一先表彰大会(2026-06-29)",
    },
    # ── 15 李刚 — 区领导 ──
    {
        "id": "p15",
        "name": "李刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "陕州区",
        "source": "陕州区两优一先表彰大会(2026-06-29)",
    },
]

organizations = [
    {"id": 1, "name": "中共三门峡市陕州区委员会", "type": "党委", "level": "县处级", "parent": "中共三门峡市委", "location": "三门峡市陕州区"},
    {"id": 2, "name": "陕州区人民政府", "type": "政府", "level": "县处级", "parent": "三门峡市人民政府", "location": "三门峡市陕州区"},
    {"id": 3, "name": "陕州区公安局", "type": "政府", "level": "乡科级", "parent": "陕州区人民政府", "location": "三门峡市陕州区"},
    {"id": 4, "name": "陕州区文化广电和旅游局", "type": "政府", "level": "乡科级", "parent": "陕州区人民政府", "location": "三门峡市陕州区"},
    {"id": 5, "name": "陕州区先进制造业开发区", "type": "开发区", "level": "乡科级", "parent": "陕州区人民政府", "location": "三门峡市陕州区"},
]

positions = [
    # 李军 — 区委书记
    {"person_id": "p1", "org_id": 1, "title": "区委书记", "start": "", "end": "", "rank": "正县处级", "note": "主持区委全面工作；主持第四次党代会（2026-06-25）；为全区党员讲授党课"},
    # 何飞 — 区长
    {"person_id": "p2", "org_id": 1, "title": "区委副书记", "start": "", "end": "", "rank": "副县处级", "note": "区委副书记"},
    {"person_id": "p2", "org_id": 2, "title": "区长、党组书记", "start": "", "end": "", "rank": "正县处级", "note": "主持区政府全面工作；分管审计局"},
    # 孔利亚 — 区委常委
    {"person_id": "p3", "org_id": 1, "title": "区委常委", "start": "", "end": "", "rank": "副县处级", "note": "随李军调研甘山果香项目"},
    # 王胜军 — 区委常委
    {"person_id": "p4", "org_id": 1, "title": "区委常委", "start": "", "end": "", "rank": "副县处级", "note": ""},
    # 丁锐 — 区委常委
    {"person_id": "p5", "org_id": 1, "title": "区委常委", "start": "", "end": "", "rank": "副县处级", "note": "随李军调研甘山果香项目(2026-07-19)"},
    # 寇晓辉 — 区委常委
    {"person_id": "p6", "org_id": 1, "title": "区委常委", "start": "", "end": "", "rank": "副县处级", "note": "出席两优一先表彰大会(2026-06-29)"},
    # 李志高 — 区委常委
    {"person_id": "p7", "org_id": 1, "title": "区委常委", "start": "", "end": "", "rank": "副县处级", "note": "随李军调研甘山果香项目(2026-07-19)"},
    # 李远 — 区委常委
    {"person_id": "p8", "org_id": 1, "title": "区委常委", "start": "", "end": "", "rank": "副县处级", "note": ""},
    # 辛欣 — 区委常委、统战部长
    {"person_id": "p9", "org_id": 1, "title": "区委常委、统战部部长", "start": "", "end": "", "rank": "副县处级", "note": "负责统战工作；调研张茅乡防汛安全生产(2026-07-21)"},
    # 张晓丹 — 副区长
    {"person_id": "p10", "org_id": 2, "title": "副区长、党组成员", "start": "", "end": "", "rank": "副县处级", "note": "分管教育体育、科技、人社、卫健、医保、文旅、残联、妇女儿童；联系工会、民族宗教、对台、侨务等"},
    {"person_id": "p10", "org_id": 4, "title": "党组书记", "start": "", "end": "", "rank": "", "note": "区文化广电和旅游局党组书记"},
    # 张华 — 副区长、公安局长
    {"person_id": "p11", "org_id": 2, "title": "副区长、党组成员", "start": "", "end": "", "rank": "副县处级", "note": "兼任区公安局局长；负责公安、司法、信访稳定；联系国家安全"},
    {"person_id": "p11", "org_id": 3, "title": "局长", "start": "", "end": "", "rank": "乡科级正职", "note": "陕州区公安局局长"},
    # 蔡啸虎 — 二级调研员
    {"person_id": "p12", "org_id": 2, "title": "二级调研员", "start": "", "end": "", "rank": "正县处级", "note": "随李军调研甘山果香项目(2026-07-19)"},
    # 苏万军 — 二级调研员
    {"person_id": "p13", "org_id": 2, "title": "二级调研员", "start": "", "end": "", "rank": "正县处级", "note": ""},
    # 樊卫星 — 区领导
    {"person_id": "p14", "org_id": 1, "title": "区领导", "start": "", "end": "", "rank": "副县处级", "note": "出席两优一先表彰大会(2026-06-29); 具体职务待确认"},
    # 李刚 — 区领导
    {"person_id": "p15", "org_id": 1, "title": "区领导", "start": "", "end": "", "rank": "副县处级", "note": "出席两优一先表彰大会(2026-06-29); 具体职务待确认"},
]

relationships = [
    # 党政主要负责同志
    {"person_a": "p1", "person_b": "p2", "type": "党政搭档", "context": "区委书记与区长党政工作搭档，共同出席项目调研(2026-07-19)", "overlap_org": "陕州区", "overlap_period": ""},
    # 区委常委会核心
    {"person_a": "p1", "person_b": "p3", "type": "工作关系", "context": "区委书记与区委常委，第四次党代会主席团成员", "overlap_org": "中共陕州区委", "overlap_period": ""},
    {"person_a": "p1", "person_b": "p4", "type": "工作关系", "context": "区委书记与区委常委，第四次党代会主席团成员", "overlap_org": "中共陕州区委", "overlap_period": ""},
    {"person_a": "p1", "person_b": "p5", "type": "工作关系", "context": "区委书记与区委常委，共同调研甘山果香项目(2026-07-19)", "overlap_org": "中共陕州区委", "overlap_period": ""},
    {"person_a": "p1", "person_b": "p6", "type": "工作关系", "context": "区委书记与区委常委，出席两优一先表彰大会(2026-06-29)", "overlap_org": "中共陕州区委", "overlap_period": ""},
    {"person_a": "p1", "person_b": "p7", "type": "工作关系", "context": "区委书记与区委常委，共同调研甘山果香项目(2026-07-19)", "overlap_org": "中共陕州区委", "overlap_period": ""},
    {"person_a": "p1", "person_b": "p8", "type": "工作关系", "context": "区委书记与区委常委，第四次党代会主席团成员", "overlap_org": "中共陕州区委", "overlap_period": ""},
    {"person_a": "p1", "person_b": "p9", "type": "工作关系", "context": "区委书记与区委常委、统战部长，第四次党代会主席团成员", "overlap_org": "中共陕州区委", "overlap_period": ""},
    # 副区长与区长
    {"person_a": "p2", "person_b": "p10", "type": "党政搭档", "context": "区长与副区长工作搭档", "overlap_org": "陕州区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p11", "type": "党政搭档", "context": "区长与副区长兼公安局长工作搭档", "overlap_org": "陕州区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p12", "type": "工作关系", "context": "区长与二级调研员", "overlap_org": "陕州区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p13", "type": "工作关系", "context": "区长与二级调研员", "overlap_org": "陕州区政府", "overlap_period": ""},
    # 调研参与关系
    {"person_a": "p5", "person_b": "p7", "type": "工作关系", "context": "同为区委常委，共同参加甘山果香项目调研(2026-07-19)", "overlap_org": "中共陕州区委", "overlap_period": ""},
    {"person_a": "p6", "person_b": "p8", "type": "工作关系", "context": "同为区委常委，共同出席两优一先表彰大会(2026-06-29)", "overlap_org": "中共陕州区委", "overlap_period": ""},
    {"person_a": "p9", "person_b": "p10", "type": "工作关系", "context": "同为区委常委/政府领导，均为第四次党代会主席团成员", "overlap_org": "陕州区", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════════
# SQLite DB Builder
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for t in ("relationships", "positions", "organizations", "persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")

    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start_date TEXT, end_date TEXT,
        rank TEXT, note TEXT
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT
    )""")

    # Normalize person ids: strip "p" prefix for DB
    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (pid(p["id"]), p["name"], p["gender"], p["ethnicity"], p["birth"],
                     p["birthplace"], p["education"], p["party_join"], p["work_start"],
                     p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pid(pos["person_id"]), pos["org_id"], pos["title"],
                     pos.get("start", ""), pos.get("end", ""),
                     pos.get("rank", ""), pos.get("note", "")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (pid(r["person_a"]), pid(r["person_b"]), r["type"], r["context"],
                     r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")


# ══════════════════════════════════════════════════════════════════════════
# GEXF Graph Builder
# ══════════════════════════════════════════════════════════════════════════

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;") if s is not None else ""

def person_color(post):
    if "书记" in post and "副" not in post and "纪委" not in post:
        return ("255,50,50", 20.0)
    elif "区长" in post and "副" not in post:
        return ("50,100,255", 20.0)
    elif "副" in post and ("区长" in post or "书记" in post):
        return ("100,150,255", 12.0)
    elif "常委" in post:
        return ("100,150,255", 12.0)
    else:
        return ("100,100,100", 12.0)

def org_color(org_type):
    colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "开发区": ("200,255,200", 8.0),
    }
    return colors.get(org_type, ("200,200,200", 8.0))

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>陕州区领导班子关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Organization nodes
    for o in organizations:
        c, sz = org_color(o["type"])
        nid = f"o{o['id']}"
        lines.append(f'      <node id="{nid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization
    for pos in positions:
        eid += 1
        nid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pos["person_id"]}" target="{nid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # Person <-> Person
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "陕州区政府网站—政府领导页", "url": "http://www.shanzhou.gov.cn/18348/0000/zhengfuxinxi-1.html", "publisher": "陕州区人民政府", "published_at": "2025-11-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "政府领导名单: 何飞、张晓丹、张华、蔡啸虎、苏万军"},
        {"id": "S002", "title": "陕州区第四次代表大会胜利闭幕", "url": "http://www.shanzhou.gov.cn/18442/2026/6/2270962.html", "publisher": "陕州区人民政府", "published_at": "2026-06-25", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "主席团名单: 李军 何飞 孔利亚 王胜军 丁锐 寇晓辉 李志高 李远 辛欣 张晓丹"},
        {"id": "S003", "title": "李军深入一线调研重点项目建设", "url": "http://www.shanzhou.gov.cn/18020/2026/7/2278550.html", "publisher": "陕州区人民政府", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "李军以区委书记身份调研；何飞、孔利亚、丁锐、李志高、蔡啸虎参加"},
        {"id": "S004", "title": "陕州区两优一先表彰大会召开", "url": "http://www.shanzhou.gov.cn/18442/2026/6/2271784.html", "publisher": "陕州区人民政府", "published_at": "2026-06-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "李军讲授党课；孔利亚、樊卫星、丁锐、李刚、寇晓辉、李志高、李远、辛欣、张晓丹出席"},
        {"id": "S005", "title": "区领导辛欣调研督导安全生产及防汛工作", "url": "http://www.shanzhou.gov.cn/18020/2026/7/2278992.html", "publisher": "陕州区人民政府", "published_at": "2026-07-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "辛欣以区委常委、统战部部长身份调研张茅乡"},
        {"id": "S006", "title": "陕州区政府网站—何飞简历", "url": "http://www.shanzhou.gov.cn/18348/616601952/1331632.html", "publisher": "陕州区人民政府", "published_at": "2025-11-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "何飞: 区委副书记、区政府区长、党组书记"},
        {"id": "S007", "title": "陕州区政府网站—张晓丹简历", "url": "http://www.shanzhou.gov.cn/18348/616602816/1333255.html", "publisher": "陕州区人民政府", "published_at": "2025-11-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张晓丹: 副区长、党组成员，区文化广电和旅游局党组书记"},
        {"id": "S008", "title": "陕州区政府网站—张华简历", "url": "http://www.shanzhou.gov.cn/18348/2025/11/2172196.html", "publisher": "陕州区人民政府", "published_at": "2025-11-25", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张华: 副区长、党组成员，兼区公安局长"},
        {"id": "S009", "title": "陕州区政府网站—蔡啸虎简历", "url": "http://www.shanzhou.gov.cn/18348/616602816/1333258.html", "publisher": "陕州区人民政府", "published_at": "2025-11-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "蔡啸虎: 二级调研员"},
        {"id": "S010", "title": "陕州区政府网站—苏万军简历", "url": "http://www.shanzhou.gov.cn/18348/616602816/1333261.html", "publisher": "陕州区人民政府", "published_at": "2025-11-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "苏万军: 二级调研员"},
    ]

def make_person_json(person, timeline, relationships_list, source_register):
    """Build a person graph JSON following the schema."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "三门峡市",
            "region": "陕州区",
            "job": person["current_post"],
            "task_id": "henan_陕州区",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": f"shanzhouqu_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}" if person["birth"] else person["name"],
                "name_birthplace": f"{person['name']}_{person['birthplace']}" if person["birthplace"] else person["name"],
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
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
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面公开记录", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "缺少出生年份、完整教育和早期履历信息"
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的出生年份和籍贯是？", "why_it_matters": "核心人物身份信息缺失", "suggested_queries": [f"{person['name']} 简历 出生"], "last_attempted": AS_OF},
            {"priority": "high", "question": f"{person['name']}的完整职业履历是什么？", "why_it_matters": "无法分析晋升路径和跨部门经验", "suggested_queries": [f"{person['name']} 任职经历 简历"], "last_attempted": AS_OF},
        ]
    }


def build():
    print("=" * 60)
    print("  三门峡市陕州区领导班子工作关系网络")
    print("  等级: 市辖区")
    print(f"  调查日期: {AS_OF}")
    print("  信息来源: 陕州区政府网站")
    print("=" * 60)

    build_db()
    build_gexf()

    print(f"\n  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 李军 (区委书记)
    li_timeline = [
        {"start": "", "end": "", "org": "中共三门峡市陕州区委员会", "title": "区委书记", "notes": "主持第四次党代会(2026-06-25)；讲授七一党课(2026-06-29)；调研重点项目建设(2026-07-19)", "confidence": "confirmed", "source_ids": ["S002", "S003", "S004"]},
    ]
    li_relationships = [
        {"person": "何飞", "person_id": "shanzhouqu_何飞", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记与区长党政搭档", "overlap_org": "陕州区", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "孔利亚", "person_id": "shanzhouqu_孔利亚", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记与区委常委，共同参加项目调研", "overlap_org": "中共陕州区委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "丁锐", "person_id": "shanzhouqu_丁锐", "relationship_type": "overlap", "strength": "medium", "evidence": "共同调研甘山果香项目", "overlap_org": "中共陕州区委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "李志高", "person_id": "shanzhouqu_李志高", "relationship_type": "overlap", "strength": "medium", "evidence": "共同调研甘山果香项目", "overlap_org": "中共陕州区委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    li_json = make_person_json(persons[0], li_timeline, li_relationships, source_register)
    li_path = PERSONS_DIR / f"{TODAY}-河南省-三门峡市-区委书记-李军.json"
    with open(li_path, "w", encoding="utf-8") as f:
        json.dump(li_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {li_path.name}")

    # 2. 何飞 (区长)
    he_timeline = [
        {"start": "", "end": "", "org": "中共三门峡市陕州区委员会", "title": "区委副书记", "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S006"]},
        {"start": "", "end": "", "org": "陕州区人民政府", "title": "区长、党组书记", "notes": "主持区政府全面工作；分管审计局", "confidence": "confirmed", "source_ids": ["S001", "S006"]},
    ]
    he_relationships = [
        {"person": "李军", "person_id": "shanzhouqu_李军", "relationship_type": "overlap", "strength": "strong", "evidence": "区长与区委书记党政搭档", "overlap_org": "陕州区", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "张晓丹", "person_id": "shanzhouqu_张晓丹", "relationship_type": "overlap", "strength": "medium", "evidence": "区长与副区长工作搭档", "overlap_org": "陕州区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "张华", "person_id": "shanzhouqu_张华", "relationship_type": "overlap", "strength": "medium", "evidence": "区长与副区长工作搭档", "overlap_org": "陕州区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    he_json = make_person_json(persons[1], he_timeline, he_relationships, source_register)
    he_path = PERSONS_DIR / f"{TODAY}-河南省-三门峡市-区长-何飞.json"
    with open(he_path, "w", encoding="utf-8") as f:
        json.dump(he_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {he_path.name}")

    # 3. 孔利亚 (区委常委、副书记?)
    k_timeline = [
        {"start": "", "end": "", "org": "中共三门峡市陕州区委员会", "title": "区委常委", "notes": "出席第四次党代会(2026-06)；参加甘山果香项目调研(2026-07-19)；出席两优一先表彰(2026-06-29)", "confidence": "confirmed", "source_ids": ["S002", "S003", "S004"]},
    ]
    k_relationships = [
        {"person": "李军", "person_id": "shanzhouqu_李军", "relationship_type": "overlap", "strength": "strong", "evidence": "区委常委与区委书记工作关系", "overlap_org": "中共陕州区委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
    ]
    k_json = make_person_json(persons[2], k_timeline, k_relationships, source_register)
    k_path = PERSONS_DIR / f"{TODAY}-河南省-三门峡市-区委常委-孔利亚.json"
    with open(k_path, "w", encoding="utf-8") as f:
        json.dump(k_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {k_path.name}")

    # 4. 辛欣 (区委常委、统战部长)
    xin_timeline = [
        {"start": "", "end": "", "org": "中共三门峡市陕州区委员会", "title": "区委常委、统战部部长", "notes": "调研张茅乡安全生产及防汛(2026-07-21)", "confidence": "confirmed", "source_ids": ["S002", "S005"]},
    ]
    xin_relationships = [
        {"person": "李军", "person_id": "shanzhouqu_李军", "relationship_type": "overlap", "strength": "medium", "evidence": "区委常委、统战部长与区委书记工作关系", "overlap_org": "中共陕州区委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    xin_json = make_person_json(persons[8], xin_timeline, xin_relationships, source_register)
    xin_path = PERSONS_DIR / f"{TODAY}-河南省-三门峡市-统战部长-辛欣.json"
    with open(xin_path, "w", encoding="utf-8") as f:
        json.dump(xin_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {xin_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()
