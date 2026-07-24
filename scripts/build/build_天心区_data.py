#!/usr/bin/env python3
"""
天心区领导班子工作关系网络
等级: 市辖区 | 上级: 长沙市
调查日期: 2026-07-24
信息来源: 天心区政府网站 (www.tianxin.gov.cn)
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
AS_OF = "2026-07-24"
TODAY = "20260724"
BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "天心区_network.db"
GEXF_PATH = BASE / "天心区_network.gexf"
PERSONS_DIR = BASE

# ── Data ───────────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": "p1",
        "name": "周志军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "天心区委书记",
        "current_org": "中共长沙市天心区委员会",
        "source": "天心区委宣传部新闻",
    },
    {
        "id": "p2",
        "name": "梁天琛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年10月",
        "birthplace": "",
        "education": "会计硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "天心区委副书记、区长",
        "current_org": "天心区人民政府",
        "source": "天心区政府网站领导信息",
    },
    # ── Government Leadership ──
    {
        "id": "p3",
        "name": "张浩平",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1976年11月",
        "birthplace": "",
        "education": "本科",
        "party_join": "",
        "work_start": "1999年7月",
        "current_post": "区委常委、常务副区长",
        "current_org": "天心区人民政府",
        "source": "天心区政府网站领导信息",
    },
    {
        "id": "p4",
        "name": "郑州",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年10月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "",
        "work_start": "1999年12月",
        "current_post": "区委常委、副区长",
        "current_org": "天心区人民政府",
        "source": "天心区政府网站领导信息",
    },
    {
        "id": "p5",
        "name": "王钰莹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "1997年7月",
        "current_post": "副区长",
        "current_org": "天心区人民政府",
        "source": "天心区政府网站领导信息",
    },
    {
        "id": "p6",
        "name": "贺国鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1991年6月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长提名人选",
        "current_org": "天心区人民政府",
        "source": "天心区政府网站领导信息",
    },
    {
        "id": "p7",
        "name": "李勇军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年9月",
        "birthplace": "",
        "education": "在职研究生、工商管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "天心区人民政府",
        "source": "天心区政府网站领导信息",
    },
    {
        "id": "p8",
        "name": "汤波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年10月",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "天心区人民政府",
        "source": "天心区政府网站领导信息",
    },
    {
        "id": "p9",
        "name": "刘海平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年10月",
        "birthplace": "",
        "education": "本科",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长、区公安分局局长",
        "current_org": "天心区人民政府",
        "source": "天心区政府网站领导信息",
    },
    {
        "id": "p10",
        "name": "周缇",
        "gender": "女",
        "ethnicity": "",
        "birth": "1985年9月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "天心区人民政府",
        "source": "天心区政府网站领导信息",
    },
    {
        "id": "p11",
        "name": "孙泉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "天心区人民政府",
        "source": "天心区政府网站新闻",
    },
    # ── Park/Zone Leadership ──
    {
        "id": "p12",
        "name": "陈宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "园区领导",
        "current_org": "天心经开区",
        "source": "天心区政府网站新闻",
    },
    {
        "id": "p13",
        "name": "许伟斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "园区领导",
        "current_org": "天心经开区",
        "source": "天心区政府网站新闻",
    },
    # ── Predecessors ──
    {
        "id": "p14",
        "name": "吴新伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "",
        "source": "已知公开信息",
    },
]

organizations = [
    {"id": 1, "name": "中共长沙市天心区委员会", "type": "党委", "level": "区级", "parent": "中共长沙市委", "location": "长沙市天心区"},
    {"id": 2, "name": "天心区人民政府", "type": "政府", "level": "区级", "parent": "长沙市人民政府", "location": "长沙市天心区"},
    {"id": 3, "name": "天心区人民代表大会常务委员会", "type": "人大", "level": "区级", "parent": "长沙市人大", "location": "长沙市天心区"},
    {"id": 4, "name": "中国人民政治协商会议天心区委员会", "type": "政协", "level": "区级", "parent": "长沙市政协", "location": "长沙市天心区"},
    {"id": 5, "name": "天心区纪委监委", "type": "党委", "level": "区级", "parent": "中共天心区委", "location": "长沙市天心区"},
    {"id": 6, "name": "天心区委组织部", "type": "党委", "level": "区级", "parent": "中共天心区委", "location": "长沙市天心区"},
    {"id": 7, "name": "天心区委宣传部", "type": "党委", "level": "区级", "parent": "中共天心区委", "location": "长沙市天心区"},
    {"id": 8, "name": "天心区委统战部", "type": "党委", "level": "区级", "parent": "中共天心区委", "location": "长沙市天心区"},
    {"id": 9, "name": "天心区委政法委", "type": "党委", "level": "区级", "parent": "中共天心区委", "location": "长沙市天心区"},
    {"id": 10, "name": "天心区公安分局", "type": "政府", "level": "区级", "parent": "天心区政府", "location": "长沙市天心区"},
    {"id": 11, "name": "天心经开区", "type": "开发区", "level": "区级", "parent": "天心区政府", "location": "长沙市天心区"},
]

positions = [
    # 周志军
    {"person_id": "p1", "org_id": 1, "title": "天心区委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持区委全面工作"},
    # 梁天琛
    {"person_id": "p2", "org_id": 1, "title": "天心区委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p2", "org_id": 2, "title": "天心区区长、党组书记", "start": "", "end": "present", "rank": "正处级", "note": "领导区政府全面工作"},
    # 张浩平
    {"person_id": "p3", "org_id": 1, "title": "天心区委常委", "start": "2021年10月", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p3", "org_id": 2, "title": "常务副区长", "start": "2021年10月", "end": "present", "rank": "副处级", "note": "负责区政府常务工作"},
    # 郑州
    {"person_id": "p4", "org_id": 1, "title": "天心区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p4", "org_id": 2, "title": "副区长", "start": "2021年10月", "end": "present", "rank": "副处级", "note": "负责市场监管、城管等工作"},
    # 王钰莹
    {"person_id": "p5", "org_id": 2, "title": "副区长", "start": "2021年10月", "end": "present", "rank": "副处级", "note": "负责教育、科技、文化、卫生等工作"},
    # 贺国鹏
    {"person_id": "p6", "org_id": 2, "title": "副区长提名人选", "start": "", "end": "present", "rank": "副处级", "note": "负责民政、农业农村、退役军人等工作"},
    # 李勇军
    {"person_id": "p7", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责住建、自然资源、城投等工作"},
    # 汤波
    {"person_id": "p8", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责人社、商务、交通等工作"},
    # 刘海平
    {"person_id": "p9", "org_id": 2, "title": "副区长、公安分局局长", "start": "", "end": "present", "rank": "副处级", "note": "负责公安、司法、信访等工作"},
    {"person_id": "p9", "org_id": 10, "title": "党委书记、局长", "start": "", "end": "present", "rank": "副处级", "note": "主持公安分局全面工作"},
    # 周缇
    {"person_id": "p10", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责工信、数据管理、行政审批等工作"},
    # 孙泉
    {"person_id": "p11", "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 陈宇
    {"person_id": "p12", "org_id": 11, "title": "园区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 许伟斌
    {"person_id": "p13", "org_id": 11, "title": "园区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 吴新伟（前任区委书记）
    {"person_id": "p14", "org_id": 1, "title": "前任区委书记", "start": "", "end": "", "rank": "正处级", "note": "周志军的前任"},
]

relationships = [
    # ── 周志军与班子成员 ──
    {"person_a": "p1", "person_b": "p2", "type": "党政搭档", "context": "区委书记与区长党政一把手", "overlap_org": "天心区", "overlap_period": ""},
    {"person_a": "p1", "person_b": "p3", "type": "上下级", "context": "区委书记与分管常务工作的常委", "overlap_org": "天心区委", "overlap_period": ""},
    {"person_a": "p1", "person_b": "p4", "type": "上下级", "context": "区委书记与区委常委、副区长", "overlap_org": "天心区委", "overlap_period": ""},
    # ── 区长与副区长们 ──
    {"person_a": "p2", "person_b": "p3", "type": "上下级", "context": "区长与常务副区长", "overlap_org": "天心区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p4", "type": "上下级", "context": "区长与副区长（区委常委）", "overlap_org": "天心区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p5", "type": "上下级", "context": "区长与副区长", "overlap_org": "天心区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p6", "type": "上下级", "context": "区长与副区长提名人选", "overlap_org": "天心区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p7", "type": "上下级", "context": "区长与副区长", "overlap_org": "天心区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p8", "type": "上下级", "context": "区长与副区长", "overlap_org": "天心区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p9", "type": "上下级", "context": "区长与副区长兼公安局长", "overlap_org": "天心区政府", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p10", "type": "上下级", "context": "区长与副区长", "overlap_org": "天心区政府", "overlap_period": ""},
    # ── 张浩平与副区长（同为政府班子） ──
    {"person_a": "p3", "person_b": "p5", "type": "同僚", "context": "常务副区长与副区长，同属政府班子", "overlap_org": "天心区政府", "overlap_period": ""},
    {"person_a": "p3", "person_b": "p7", "type": "同僚", "context": "常务副区长与副区长，同属政府班子", "overlap_org": "天心区政府", "overlap_period": ""},
    {"person_a": "p3", "person_b": "p4", "type": "同僚", "context": "同为区委常委，共事于区委常委会", "overlap_org": "天心区委", "overlap_period": ""},
    # ── 前任-继任关系 ──
    {"person_a": "p14", "person_b": "p1", "type": "前任继任", "context": "吴新伟前任区委书记，周志军现任区委书记", "overlap_org": "中共天心区委", "overlap_period": ""},
    # ── 园区领导与区政府 ──
    {"person_a": "p2", "person_b": "p12", "type": "工作关系", "context": "区长与天心经开区园区领导", "overlap_org": "天心区", "overlap_period": ""},
    {"person_a": "p2", "person_b": "p13", "type": "工作关系", "context": "区长与天心经开区园区领导", "overlap_org": "天心区", "overlap_period": ""},
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
    lines.append(f'    <description>天心区领导班子关系网络 - {AS_OF}</description>')
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
        {"id": "S001", "title": "天心区政府网站—政府领导页", "url": "http://www.tianxin.gov.cn/qzf/", "publisher": "天心区人民政府", "published_at": "2026-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区政府领导名单: 梁天琛、张浩平、郑州、王钰莹、贺国鹏、李勇军、汤波、刘海平、周缇"},
        {"id": "S002", "title": "天心区委常委会召开会议（2026-07-13）", "url": "http://www.tianxin.gov.cn/zwgk8/xxgkml9/qtfdxx/yaowendongtai/zwdt/202607/t20260713_12490256.html", "publisher": "天心区委宣传部", "published_at": "2026-07-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "受天心区委书记周志军委托，区委副书记、区长梁天琛主持会议"},
        {"id": "S003", "title": "天心区委常委会召开会议（2026-07-10）", "url": "http://www.tianxin.gov.cn/zwgk8/xxgkml9/qtfdxx/yaowendongtai/zwdt/202607/t20260710_12485495.html", "publisher": "天心区委宣传部", "published_at": "2026-07-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "受天心区委书记周志军委托，区委副书记、区长梁天琛主持会议；传达副省长、市委书记陈竞调研指示精神"},
        {"id": "S004", "title": "梁天琛主持召开区长办公会", "url": "http://www.tianxin.gov.cn/zwgk8/xxgkml9/qtfdxx/yaowendongtai/zwdt/202607/t20260714_12491610.html", "publisher": "天心区政府", "published_at": "2026-07-14", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "梁天琛主持，张浩平、郑州、王钰莹、贺国鹏、李勇军、汤波、陈宇、许伟斌参加"},
        {"id": "S005", "title": "天心区民生领域信访问题集中治理工作调度会议", "url": "http://www.tianxin.gov.cn/zwgk8/xxgkml9/qtfdxx/yaowendongtai/zwdt/202607/t20260717_12494774.html", "publisher": "天心区政府", "published_at": "2026-07-17", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "梁天琛主持；区领导孙泉、黄先辉参加"},
        {"id": "S006", "title": "梁天琛领导信息页", "url": "http://www.tianxin.gov.cn/qzf/zfld/ldzc11/202603/t20260327_12346875.html", "publisher": "天心区人民政府", "published_at": "2026-03-27", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "梁天琛，男，汉族，1984年10月生，会计硕士，天心区委副书记、区长"},
        {"id": "S007", "title": "张浩平领导信息页", "url": "http://www.tianxin.gov.cn/qzf/zfld/ldzc11/202111/t20211124_10361351.html", "publisher": "天心区人民政府", "published_at": "2023-02-27", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张浩平，男，土家族，1976年11月生，区委常委、常务副区长；完整工作经历"},
        {"id": "S008", "title": "郑州领导信息页", "url": "http://www.tianxin.gov.cn/qzf/zfld/ldzc11/202111/t20211124_10361255.html", "publisher": "天心区人民政府", "published_at": "2021-11-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "郑州，男，汉族，1980年10月生，硕士，区委常委、副区长；完整工作经历"},
        {"id": "S009", "title": "王钰莹领导信息页", "url": "http://www.tianxin.gov.cn/qzf/zfld/ldzc11/202111/t20211124_10361235.html", "publisher": "天心区人民政府", "published_at": "2021-11-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王钰莹，女，汉族，1974年9月生，研究生，副区长；完整工作经历"},
        {"id": "S010", "title": "贺国鹏领导信息页", "url": "http://www.tianxin.gov.cn/qzf/zfld/ldzc11/202605/t20260519_12386336.html", "publisher": "天心区人民政府", "published_at": "2026-05-19", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "贺国鹏，男，汉族，1991年6月生，省委党校研究生，副区长提名人选"},
        {"id": "S011", "title": "李勇军领导信息页", "url": "http://www.tianxin.gov.cn/qzf/zfld/ldzc11/202305/t20230515_11095742.html", "publisher": "天心区人民政府", "published_at": "2023-05-15", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "李勇军，男，汉族，1979年9月生，在职研究生/工商管理硕士，副区长"},
        {"id": "S012", "title": "汤波领导信息页", "url": "http://www.tianxin.gov.cn/qzf/zfld/ldzc11/202512/t20251210_12107858.html", "publisher": "天心区人民政府", "published_at": "2025-12-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "汤波，男，汉族，1984年10月生，博士研究生，副区长"},
        {"id": "S013", "title": "刘海平领导信息页", "url": "http://www.tianxin.gov.cn/qzf/zfld/ldzc11/202401/t20240129_11359997.html", "publisher": "天心区人民政府", "published_at": "2024-01-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "刘海平，男，汉族，1971年10月生，本科，副区长、公安分局局长"},
        {"id": "S014", "title": "周缇领导信息页", "url": "http://www.tianxin.gov.cn/qzf/zfld/ldzc11/202508/t20250821_11961590.html", "publisher": "天心区人民政府", "published_at": "2025-08-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "周缇，女，1985年9月生，研究生，副区长"},
    ]


def make_person_json(person, timeline, relationships_list, src_reg):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖南省",
            "city": "长沙市",
            "region": "天心区",
            "job": person["current_post"],
            "task_id": "hunan_天心区",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": f"tianxin_{person['name']}",
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
            "biggest_gap": f"缺少{person['name']}的出生年份{'、籍贯' if not person['birthplace'] else ''}和早期履历信息" if not person["birth"] else "缺少完整早期履历"
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
    print("  长沙市天心区领导班子工作关系网络")
    print("  等级: 市辖区")
    print(f"  调查日期: {AS_OF}")
    print("  信息来源: 天心区政府网站")
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

    # 1. 周志军 (区委书记)
    zhou_timeline = [
        {"start": "", "end": "", "org": "中共长沙市天心区委员会", "title": "天心区委书记", "notes": "主持区委全面工作；2026年7月分别委托梁天琛主持区委常委会", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
    ]
    zhou_relationships = [
        {"person": "梁天琛", "person_id": "tianxin_梁天琛", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记与区长党政搭档，为重振地方发展的核心搭档", "overlap_org": "天心区", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "吴新伟", "person_id": "tianxin_吴新伟", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "前任区委书记", "overlap_org": "中共天心区委", "overlap_period": "", "direction": "other_to_person", "confidence": "plausible", "source_ids": []},
    ]
    zhou_json = make_person_json(persons[0], zhou_timeline, zhou_relationships, src_reg)
    zhou_path = PERSONS_DIR / f"{TODAY}-湖南省-长沙市-区委书记-周志军.json"
    with open(zhou_path, "w", encoding="utf-8") as f:
        json.dump(zhou_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zhou_path.name}")

    # 2. 梁天琛 (区长)
    liang_timeline = [
        {"start": "", "end": "present", "org": "中共长沙市天心区委员会", "title": "区委副书记", "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S006"]},
        {"start": "", "end": "present", "org": "天心区人民政府", "title": "区长、党组书记", "notes": "领导区政府全面工作，负责审计工作", "confidence": "confirmed", "source_ids": ["S001", "S006"]},
    ]
    liang_relationships = [
        {"person": "周志军", "person_id": "tianxin_周志军", "relationship_type": "overlap", "strength": "strong", "evidence": "区长与区委书记党政搭档", "overlap_org": "天心区", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "张浩平", "person_id": "tianxin_张浩平", "relationship_type": "overlap", "strength": "strong", "evidence": "区长与常务副区长工作搭档", "overlap_org": "天心区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "郑州", "person_id": "tianxin_郑州", "relationship_type": "overlap", "strength": "medium", "evidence": "区长与副区长工作搭档", "overlap_org": "天心区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "王钰莹", "person_id": "tianxin_王钰莹", "relationship_type": "overlap", "strength": "medium", "evidence": "区长与副区长工作搭档", "overlap_org": "天心区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "贺国鹏", "person_id": "tianxin_贺国鹏", "relationship_type": "overlap", "strength": "medium", "evidence": "区长与副区长提名人选工作关系", "overlap_org": "天心区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "李勇军", "person_id": "tianxin_李勇军", "relationship_type": "overlap", "strength": "medium", "evidence": "区长与副区长工作搭档", "overlap_org": "天心区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "汤波", "person_id": "tianxin_汤波", "relationship_type": "overlap", "strength": "medium", "evidence": "区长与副区长工作搭档", "overlap_org": "天心区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    liang_json = make_person_json(persons[1], liang_timeline, liang_relationships, src_reg)
    liang_path = PERSONS_DIR / f"{TODAY}-湖南省-长沙市-区长-梁天琛.json"
    with open(liang_path, "w", encoding="utf-8") as f:
        json.dump(liang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {liang_path.name}")

    # 3. 张浩平 (常务副区长) - has detailed career
    zhang_timeline = [
        {"start": "1999年7月", "end": "2007年3月", "org": "湖南省交通规划勘察设计院", "title": "工作", "notes": "", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "2007年3月", "end": "2009年10月", "org": "湖南省交通规划勘察设计院公路勘察设计二处", "title": "副主任工程师", "notes": "", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "2009年10月", "end": "2010年5月", "org": "湖南省交通规划勘察设计院公路勘察设计二处", "title": "副处长", "notes": "", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "2010年5月", "end": "2011年12月", "org": "长沙市发展和改革委员会代建制指导协调处", "title": "副处长", "notes": "", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "2011年12月", "end": "2012年11月", "org": "长沙市发展和改革委员会投资管理局", "title": "项目评审室主任", "notes": "", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "2012年11月", "end": "2016年4月", "org": "长沙市发展和改革委员会", "title": "主任科员", "notes": "", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "2016年4月", "end": "2019年7月", "org": "长沙市发展和改革委员会", "title": "投资管理处处长", "notes": "", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "2019年7月", "end": "2020年4月", "org": "长沙市发展和改革委员会", "title": "固定资产投资处处长", "notes": "", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "2020年7月", "end": "2021年7月", "org": "浏阳经开区", "title": "党工委委员、管委会副主任", "notes": "", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "2021年7月", "end": "2021年10月", "org": "天心区人民政府", "title": "区委常委、副区长提名候选人", "notes": "", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "2021年10月", "end": "present", "org": "天心区人民政府", "title": "区委常委、常务副区长", "notes": "负责区政府常务工作", "confidence": "confirmed", "source_ids": ["S001", "S007"]},
    ]
    zhang_relationships = [
        {"person": "梁天琛", "person_id": "tianxin_梁天琛", "relationship_type": "overlap", "strength": "strong", "evidence": "常务副区长与区长工作搭档", "overlap_org": "天心区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "郑州", "person_id": "tianxin_郑州", "relationship_type": "overlap", "strength": "medium", "evidence": "同为区委常委和政府班子成员", "overlap_org": "天心区委、天心区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S007", "S008"]},
    ]
    zhang_json = make_person_json(persons[2], zhang_timeline, zhang_relationships, src_reg)
    zhang_path = PERSONS_DIR / f"{TODAY}-湖南省-长沙市-常务副区长-张浩平.json"
    with open(zhang_path, "w", encoding="utf-8") as f:
        json.dump(zhang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zhang_path.name}")

    # 4. 郑州 - has detailed career
    zheng_timeline = [
        {"start": "1999年12月", "end": "2005年7月", "org": "长沙市天心区旧城建设开发公司", "title": "工作", "notes": "", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2005年7月", "end": "2008年2月", "org": "长沙市天心城市建设投资有限责任公司", "title": "副总经理", "notes": "", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2008年2月", "end": "2010年5月", "org": "天心区桂花坪街道", "title": "工委委员、副书记、纪委书记", "notes": "", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2010年5月", "end": "2012年7月", "org": "天心区桂花坪街道", "title": "工委副书记、政协联络处主任", "notes": "", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2012年7月", "end": "2014年11月", "org": "天心区黑石铺街道", "title": "工委副书记、办事处主任", "notes": "", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2014年11月", "end": "2016年3月", "org": "天心区先锋街道", "title": "工委副书记、办事处主任", "notes": "", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2016年3月", "end": "2016年8月", "org": "天心区先锋街道", "title": "工委书记", "notes": "", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2016年8月", "end": "2021年7月", "org": "天心区坡子街街道", "title": "工委书记", "notes": "2021年3月晋升四级调研员", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2021年7月", "end": "2021年10月", "org": "天心区人民政府", "title": "党组成员、副区长提名候选人", "notes": "", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2021年10月", "end": "present", "org": "天心区人民政府", "title": "副区长", "notes": "后任区委常委、副区长", "confidence": "confirmed", "source_ids": ["S001", "S008"]},
    ]
    zheng_json = make_person_json(persons[3], zheng_timeline, [], src_reg)
    zheng_path = PERSONS_DIR / f"{TODAY}-湖南省-长沙市-副区长-郑州.json"
    with open(zheng_path, "w", encoding="utf-8") as f:
        json.dump(zheng_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zheng_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()
