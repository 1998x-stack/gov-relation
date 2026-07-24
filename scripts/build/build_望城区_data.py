#!/usr/bin/env python3
"""
望城区领导班子工作关系网络
等级: 市辖区 | 上级: 长沙市
调查日期: 2026-07-24
信息来源: 望城区政府网站 (www.wangcheng.gov.cn)
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
AS_OF = "2026-07-24"
TODAY = "20260724"

# Staging: this file lives at data/tmp/hunan_望城区/
STAGING = Path(__file__).resolve().parent
# Canonical destinations (promoted later by process_tmp.py)
DB_PATH = STAGING / "望城区_network.db"
GEXF_PATH = STAGING / "望城区_network.gexf"
PERSONS_DIR = STAGING

# ══════════════════════════════════════════════════════════════════════════
# RESEARCH DATA
# ══════════════════════════════════════════════════════════════════════════

persons = [
    # ── Core Leaders ──
    {
        "id": "p1",
        "name": "许凡",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "望城区委书记",
        "current_org": "中共长沙市望城区委员会",
        "source": "望城区政府网站—新闻",
    },
    {
        "id": "p2",
        "name": "蒋砺",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "望城区委副书记、代区长",
        "current_org": "望城区人民政府",
        "source": "望城区政府网站—领导信息",
    },
    # ── Government Leadership (from wangcheng.gov.cn/qzf/) ──
    {
        "id": "p3",
        "name": "张璐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "望城区人民政府",
        "source": "望城区政府网站—领导信息",
    },
    {
        "id": "p4",
        "name": "丁旭明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "望城区人民政府",
        "source": "望城区政府网站—领导信息",
    },
    {
        "id": "p5",
        "name": "贺茂云",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "望城区人民政府",
        "source": "望城区政府网站—领导信息",
    },
    {
        "id": "p6",
        "name": "毛斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "望城区人民政府",
        "source": "望城区政府网站—领导信息",
    },
    {
        "id": "p7",
        "name": "旦增平措",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "望城区人民政府",
        "source": "望城区政府网站—领导信息",
    },
    {
        "id": "p8",
        "name": "杨海军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "望城区人民政府",
        "source": "望城区政府网站—领导信息",
    },
    {
        "id": "p9",
        "name": "周志国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "望城区人民政府",
        "source": "望城区政府网站—领导信息",
    },
    {
        "id": "p10",
        "name": "吴益彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "望城区人民政府",
        "source": "望城区政府网站—领导信息",
    },
    # ── Other Leaders Mentioned in News ──
    {
        "id": "p11",
        "name": "王辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "望城区",
        "source": "望城区政府网站—新闻（2026-07-23）",
    },
    {
        "id": "p12",
        "name": "苏春光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "望城区人民代表大会常务委员会",
        "source": "望城区政府网站—新闻（2026-07-23 许凡走访区人大）",
    },
    {
        "id": "p13",
        "name": "王湘云",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协望城区委员会",
        "source": "望城区政府网站—新闻（2026-07-23 许凡走访区政协）",
    },
    {
        "id": "p14",
        "name": "李雪龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "望城区",
        "source": "望城区政府网站—新闻（2026-07-23）",
    },
    {
        "id": "p15",
        "name": "陈旷",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "望城区",
        "source": "望城区政府网站—新闻（2026-07-22 许凡调研雷锋精神）",
    },
    # ── Predecessors ──
    {
        "id": "p16",
        "name": "蔡锋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任区长",
        "current_org": "",
        "source": "望城区政府网站—政府常务会议（2026年3-5月蔡锋主持）",
    },
]

organizations = [
    {"id": 1, "name": "中共长沙市望城区委员会", "type": "党委", "level": "区级", "parent": "中共长沙市委", "location": "长沙市望城区"},
    {"id": 2, "name": "望城区人民政府", "type": "政府", "level": "区级", "parent": "长沙市人民政府", "location": "长沙市望城区"},
    {"id": 3, "name": "望城区人民代表大会常务委员会", "type": "人大", "level": "区级", "parent": "长沙市人大", "location": "长沙市望城区"},
    {"id": 4, "name": "政协望城区委员会", "type": "政协", "level": "区级", "parent": "长沙市政协", "location": "长沙市望城区"},
    {"id": 5, "name": "望城区纪委监委", "type": "党委", "level": "区级", "parent": "中共望城区委", "location": "长沙市望城区"},
    {"id": 6, "name": "望城区委组织部", "type": "党委", "level": "区级", "parent": "中共望城区委", "location": "长沙市望城区"},
    {"id": 7, "name": "望城区委宣传部", "type": "党委", "level": "区级", "parent": "中共望城区委", "location": "长沙市望城区"},
    {"id": 8, "name": "望城区委统战部", "type": "党委", "level": "区级", "parent": "中共望城区委", "location": "长沙市望城区"},
    {"id": 9, "name": "望城区委政法委", "type": "党委", "level": "区级", "parent": "中共望城区委", "location": "长沙市望城区"},
    {"id": 10, "name": "望城区公安分局", "type": "政府", "level": "区级", "parent": "望城区政府", "location": "长沙市望城区"},
    {"id": 11, "name": "湖南望城经济开发区", "type": "开发区", "level": "区级", "parent": "望城区政府", "location": "长沙市望城区"},
]

positions = [
    # 许凡 — 区委书记
    {"person_id": "p1", "org_id": 1, "title": "望城区委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持区委全面工作"},
    # 蒋砺 — 代区长
    {"person_id": "p2", "org_id": 1, "title": "望城区委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p2", "org_id": 2, "title": "代理区长", "start": "", "end": "present", "rank": "正处级", "note": "领导区人民政府全面工作，分管审计局"},
    # 张璐 — 常务副区长
    {"person_id": "p3", "org_id": 2, "title": "常务副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 副区长们
    {"person_id": "p4", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p5", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p6", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p7", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p8", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p9", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p10", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 苏春光
    {"person_id": "p12", "org_id": 3, "title": "主任", "start": "", "end": "present", "rank": "正处级", "note": "区人大常委会主任"},
    # 王湘云
    {"person_id": "p13", "org_id": 4, "title": "主席", "start": "", "end": "present", "rank": "正处级", "note": "区政协主席"},
    # 蔡锋（前任区长）
    {"person_id": "p16", "org_id": 2, "title": "前任区长", "start": "", "end": "2026-05", "rank": "正处级", "note": "截至2026年5月仍以区长身份活动"},
]

relationships = [
    # ── 党政一把手 ──
    {"person_a": "p1", "person_b": "p2", "type": "党政搭档", "context": "区委书记与代区长党政一把手", "overlap_org": "望城区", "overlap_period": "2026—"},
    # ── 区委书记与班子成员 ──
    {"person_a": "p1", "person_b": "p3", "type": "上下级", "context": "区委书记与常务副区长", "overlap_org": "望城区", "overlap_period": ""},
    {"person_a": "p1", "person_b": "p12", "type": "工作关系", "context": "走访区人大机关并征求党代会意见", "overlap_org": "望城区", "overlap_period": ""},
    {"person_a": "p1", "person_b": "p13", "type": "工作关系", "context": "走访区政协机关并征求党代会意见", "overlap_org": "望城区", "overlap_period": ""},
    # ── 代区长与副区长们 ──
    {"person_a": "p2", "person_b": "p3", "type": "上下级", "context": "代区长与常务副区长", "overlap_org": "望城区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p4", "type": "上下级", "context": "代区长与副区长", "overlap_org": "望城区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p5", "type": "上下级", "context": "代区长与副区长", "overlap_org": "望城区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p6", "type": "上下级", "context": "代区长与副区长", "overlap_org": "望城区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p7", "type": "上下级", "context": "代区长与副区长", "overlap_org": "望城区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p8", "type": "上下级", "context": "代区长与副区长", "overlap_org": "望城区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p9", "type": "上下级", "context": "代区长与副区长", "overlap_org": "望城区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p10", "type": "上下级", "context": "代区长与副区长", "overlap_org": "望城区政府", "overlap_period": ""},
    # ── 前任-继任关系 ──
    {"person_a": "p16", "person_b": "p2", "type": "前任继任", "context": "蔡锋前任区长，蒋砺现任代区长", "overlap_org": "望城区政府", "overlap_period": "2025-2026"},
]

# ══════════════════════════════════════════════════════════════════════════
# SQLite DB Builder
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(str(DB_PATH))
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
    elif "前任" in post:
        return ("180,180,180", 12.0)
    elif "主任" in post:
        return ("200,255,255", 12.0)
    elif "主席" in post:
        return ("255,240,200", 12.0)
    else:
        return ("100,100,100", 12.0)


def org_color(org_type):
    colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "开发区": ("200,255,200", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }
    return colors.get(org_type, ("200,200,200", 8.0))


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>望城区领导班子关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

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

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        nid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pos["person_id"]}" target="{nid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
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
        {"id": "S001", "title": "望城区政府网站—区政府领导信息页", "url": "http://www.wangcheng.gov.cn/qzf/", "publisher": "望城区人民政府", "published_at": "2026-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区政府领导名单: 蒋砺（代区长）、张璐（常务副区长）、丁旭明、贺茂云、毛斌、旦增平措、杨海军、周志国、吴益彬"},
        {"id": "S002", "title": "全区推进常态化帮扶持续巩固拓展脱贫攻坚成果工作推进会召开", "url": "http://www.wangcheng.gov.cn/xxgk_343/qzfxxgkml/qtzfxxgk_131516/gkmlgzdt/gkmuwcyw/202607/t20260723_12508720.html", "publisher": "望城区融媒体中心", "published_at": "2026-07-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "许凡以望城区委书记身份讲话，蒋砺以区委副书记、代区长身份主持"},
        {"id": "S003", "title": "许凡走访区人大、区政协机关并征求区第四次党代会报告意见建议", "url": "http://www.wangcheng.gov.cn/xxgk_343/qzfxxgkml/qtzfxxgk_131516/gkmlgzdt/gkmuwcyw/202607/t20260723_12508717.html", "publisher": "望城区融媒体中心", "published_at": "2026-07-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "许凡以望城区委书记身份走访人大政协"},
        {"id": "S004", "title": "许凡调研学习弘扬雷锋精神工作", "url": "http://www.wangcheng.gov.cn/xxgk_343/qzfxxgkml/qtzfxxgk_131516/gkmlgzdt/gkmuwcyw/202607/t20260722_12507220.html", "publisher": "望城区融媒体中心", "published_at": "2026-07-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "许凡以望城区委书记身份调研，陈旷、毛斌参加"},
        {"id": "S005", "title": "蒋砺调研全区文旅产业发展工作", "url": "http://www.wangcheng.gov.cn/xxgk_343/qzfxxgkml/qtzfxxgk_131516/gkmlgzdt/gkmuwcyw/202607/t20260722_12507210.html", "publisher": "望城区融媒体中心", "published_at": "2026-07-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "蒋砺以区委副书记、代区长身份调研，丁旭明参加"},
        {"id": "S006", "title": "蒋砺调研重点项目建设", "url": "http://www.wangcheng.gov.cn/xxgk_343/qzfxxgkml/qtzfxxgk_131516/gkmlgzdt/gkmuwcyw/202607/t20260723_12508714.html", "publisher": "望城区融媒体中心", "published_at": "2026-07-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "蒋砺以区委副书记、代区长身份调研，张璐参加"},
        {"id": "S007", "title": "望城区政府常务会议（蔡锋主持，2026-03-14）", "url": "http://www.wangcheng.gov.cn/qzf/", "publisher": "望城区人民政府", "published_at": "2026-03-14", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "蔡锋在2026年3-5月以区长身份主持政府常务会议"},
    ]


def make_person_json(person, timeline, relationships_list, src_reg):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖南省",
            "city": "长沙市",
            "region": "望城区",
            "job": person["current_post"],
            "task_id": "hunan_望城区",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": f"wangcheng_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person["education"], "study_type": "unknown", "source_ids": []}] if person["education"] else [],
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
        "source_register": src_reg,
        "confidence_summary": {
            "identity": "confirmed" if person["birth"] else "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"缺少{person['name']}的出生年份{'、籍贯' if not person['birthplace'] else ''}和早期履历信息"
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的出生年份和籍贯是？", "why_it_matters": "核心人物身份信息缺失", "suggested_queries": [f"{person['name']} 简历 出生"], "last_attempted": AS_OF},
            {"priority": "high", "question": f"{person['name']}的完整职业履历是什么？", "why_it_matters": "无法分析晋升路径和跨部门经验", "suggested_queries": [f"{person['name']} 任职经历 简历"], "last_attempted": AS_OF},
        ] if not person["birth"] else [
            {"priority": "high", "question": f"{person['name']}的早期职业履历是什么？", "why_it_matters": "当前仅通过官方领导页面获得基本信息", "suggested_queries": [f"{person['name']} 工作经历 简历"], "last_attempted": AS_OF},
        ]
    }


def build():
    print("=" * 60)
    print("  长沙市望城区领导班子工作关系网络")
    print("  等级: 市辖区")
    print(f"  调查日期: {AS_OF}")
    print("  信息来源: 望城区政府网站")
    print("=" * 60)

    build_db()
    build_gexf()

    print(f"\n  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    src_reg = make_source_register()

    # 1. 许凡 (区委书记)
    xufan_timeline = [
        {"start": "", "end": "present", "org": "中共长沙市望城区委员会", "title": "望城区委书记", "notes": "主持区委全面工作；2026年7月密集出席调研活动", "confidence": "confirmed", "source_ids": ["S002", "S003", "S004"]},
    ]
    xufan_relationships = [
        {"person": "蒋砺", "person_id": "wangcheng_蒋砺", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记与代区长党政搭档", "overlap_org": "望城区", "overlap_period": "2026—", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "苏春光", "person_id": "wangcheng_苏春光", "relationship_type": "overlap", "strength": "medium", "evidence": "走访区人大机关", "overlap_org": "望城区", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "王湘云", "person_id": "wangcheng_王湘云", "relationship_type": "overlap", "strength": "medium", "evidence": "走访区政协机关", "overlap_org": "望城区", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    xufan_json = make_person_json(persons[0], xufan_timeline, xufan_relationships, src_reg)
    xufan_path = PERSONS_DIR / f"{TODAY}-湖南省-长沙市-区委书记-许凡.json"
    with open(xufan_path, "w", encoding="utf-8") as f:
        json.dump(xufan_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {xufan_path.name}")

    # 2. 蒋砺 (代区长)
    jiangli_timeline = [
        {"start": "", "end": "present", "org": "中共长沙市望城区委员会", "title": "区委副书记", "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "", "end": "present", "org": "望城区人民政府", "title": "代理区长", "notes": "领导区政府全面工作，分管审计工作", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    jiangli_relationships = [
        {"person": "许凡", "person_id": "wangcheng_许凡", "relationship_type": "overlap", "strength": "strong", "evidence": "代区长与区委书记党政搭档", "overlap_org": "望城区", "overlap_period": "2026—", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "张璐", "person_id": "wangcheng_张璐", "relationship_type": "overlap", "strength": "strong", "evidence": "代区长与常务副区长工作搭档", "overlap_org": "望城区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
        {"person": "丁旭明", "person_id": "wangcheng_丁旭明", "relationship_type": "overlap", "strength": "medium", "evidence": "代区长与副区长工作关系", "overlap_org": "望城区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
        {"person": "蔡锋", "person_id": "wangcheng_蔡锋", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "蔡锋前任区长，蒋砺现任代区长", "overlap_org": "望城区政府", "overlap_period": "2025-2026", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S007"]},
    ]
    jiangli_json = make_person_json(persons[1], jiangli_timeline, jiangli_relationships, src_reg)
    jiangli_path = PERSONS_DIR / f"{TODAY}-湖南省-长沙市-代区长-蒋砺.json"
    with open(jiangli_path, "w", encoding="utf-8") as f:
        json.dump(jiangli_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {jiangli_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()
