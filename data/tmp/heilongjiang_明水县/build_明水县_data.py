#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 明水县 (Mingshui County), 黑龙江省.

Investigation date: 2026-08-05
Task ID: heilongjiang_明水县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.mingshui.gov.cn (明水县人民政府官网) — primary, confirmed as-of 2026-08-05
    * 本地要闻/时政要闻 (2026-01~08): 马福(县委书记)、邓吉喆(县委副书记/县长) 及县委/政府班子
    * 政府领导简历页 (2026-02-26): 现任县领导出生年份、学历、分工
  - repository 既往调研: build_绥化市_data.py / report(20260805 绥化市), build_甘南县_data.py(刘正伟=明水籍)
  - 前任链: 县委书记 刘宝邱 → 马福; 县长 邹晓宁 → 邓吉喆; 人大主任 王振坤 → 杨春玲

Confidence:
  - 现任党政正职/县政府班子/县委常委: confirmed (官方)
  - 邓吉喆 1987-04, 研究生; 王玉林 1973-01 在职研究生 1997.7工作 1996.11入党: confirmed (官方简历)
  - 徐建 1982.5, 张鹏 1972.11, 刘春香 1975.9, 单云韬 1983.8: confirmed (官方简历)
  - 马福、邓吉喆 早年完整履历: unverified
  - 关海涛(绥化副市长)曾否任明水县长: plausible lead (旧河长公告)
"""
import json
import shutil
import sqlite3
import sys
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "明水县"
AS_OF = "2026-08-05"
TODAY = "20260805"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / "scripts" / "build" / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    {"id": 1, "name": "马福", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委书记", "current_org": "中共明水县委员会",
     "source": "明水县政府官网本地要闻(2026-01~08)"},
    {"id": 2, "name": "邓吉喆", "gender": "男", "ethnicity": "汉族", "birth": "1987-04", "birthplace": "", "education": "研究生",
     "party_join": "党员", "work_start": "", "current_post": "县委副书记、县长", "current_org": "明水县人民政府",
     "source": "明水县政府领导简历页(2026-02-26)"},
    {"id": 3, "name": "韩超", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委副书记", "current_org": "中共明水县委员会",
     "source": "明水县政府官网本地要闻"},
    {"id": 4, "name": "王玉林", "gender": "男", "ethnicity": "汉族", "birth": "1973-01", "birthplace": "", "education": "在职研究生",
     "party_join": "1996-11", "work_start": "1997-07", "current_post": "县委常委、常务副县长", "current_org": "明水县人民政府",
     "source": "明水县政府领导简历页(2026-02-26)"},
    {"id": 5, "name": "徐建", "gender": "男", "ethnicity": "汉族", "birth": "1982-05", "birthplace": "", "education": "大学",
     "party_join": "党员", "work_start": "", "current_post": "县委常委、副县长", "current_org": "明水县人民政府",
     "source": "明水县政府领导简历页(2026-02-26)"},
    {"id": 6, "name": "李朝阳", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委常委（曾任组织部长）", "current_org": "中共明水县委员会",
     "source": "明水县政府官网本地要闻"},
    {"id": 7, "name": "王雷", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委常委、宣传部长", "current_org": "中共明水县委员会",
     "source": "明水县政府官网本地要闻"},
    {"id": 8, "name": "宋国柏", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委常委、统战部长", "current_org": "中共明水县委员会",
     "source": "明水县政府官网本地要闻"},
    {"id": 9, "name": "王英进", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委常委、政法委书记", "current_org": "中共明水县委员会",
     "source": "明水县政府官网本地要闻"},
    {"id": 10, "name": "高秀成", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委常委、县纪委书记、县监委代主任", "current_org": "中共明水县纪律检查委员会",
     "source": "明水县政府官网本地要闻"},
    {"id": 11, "name": "张鹏", "gender": "男", "ethnicity": "汉族", "birth": "1972-11", "birthplace": "", "education": "大学",
     "party_join": "党员", "work_start": "", "current_post": "副县长、县公安局局长", "current_org": "明水县公安局",
     "source": "明水县政府领导简历页(2026-02-26)"},
    {"id": 12, "name": "刘春香", "gender": "女", "ethnicity": "汉族", "birth": "1975-09", "birthplace": "", "education": "大学",
     "party_join": "党员", "work_start": "", "current_post": "副县长", "current_org": "明水县人民政府",
     "source": "明水县政府领导简历页(2026-02-26)"},
    {"id": 13, "name": "单云韬", "gender": "男", "ethnicity": "汉族", "birth": "1983-08", "birthplace": "", "education": "大学",
     "party_join": "党员", "work_start": "", "current_post": "副县长", "current_org": "明水县人民政府",
     "source": "明水县政府领导简历页(2026-02-26)"},
    {"id": 14, "name": "杨春玲", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县人大常委会主任", "current_org": "明水县人民代表大会常务委员会",
     "source": "明水县政府官网本地要闻(2026-06-05)"},
    {"id": 15, "name": "李永吉", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县政协主席", "current_org": "中国人民政治协商会议明水县委员会",
     "source": "明水县政府官网本地要闻"},
    {"id": 16, "name": "刘宝邱", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "绥化市政协副主席（原明水县委书记）", "current_org": "政协绥化市委员会",
     "source": "明水县政府官网旧新闻(2023-2025)"},
    {"id": 17, "name": "邹晓宁", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "前任明水县委副书记、县长", "current_org": "明水县人民政府",
     "source": "明水县政府官网旧新闻(2023-2025)"},
    {"id": 18, "name": "王振坤", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "前任明水县人大常委会主任", "current_org": "明水县人民代表大会常务委员会",
     "source": "明水县政府官网旧新闻(2023-2024)"},
    {"id": 19, "name": "谢俊杰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "", "current_post": "县委常委、组织部部长", "current_org": "中共明水县委员会",
     "source": "明水县政府官网 2026-07 人大换届/常委会新闻"},
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共明水县委员会", "type": "党委", "level": "县级", "parent": "中共绥化市委员会", "location": "明水县"},
    {"id": 2, "name": "明水县人民政府", "type": "政府", "level": "县级", "parent": "绥化市人民政府", "location": "明水县"},
    {"id": 3, "name": "中共明水县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共绥化市纪律检查委员会", "location": "明水县"},
    {"id": 4, "name": "明水县公安局", "type": "政府", "level": "县级", "parent": "明水县人民政府", "location": "明水县"},
    {"id": 5, "name": "明水县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "绥化市人民代表大会常务委员会", "location": "明水县"},
    {"id": 6, "name": "中国人民政治协商会议明水县委员会", "type": "政协", "level": "县级", "parent": "绥化市政协", "location": "明水县"},
    {"id": 7, "name": "政协绥化市委员会", "type": "政协", "level": "地市级", "parent": "绥化市", "location": "绥化市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "约2025末", "end_date": "", "rank": "正处级", "note": "接任刘宝邱"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start_date": "约2026初", "end_date": "", "rank": "正处级", "note": "主持县政府全面工作，分管县财政局、县审计局"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责常务、发改、信访、安全生产等"},
    {"person_id": 5, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责住建、自然资源、林草和社区"},
    {"person_id": 6, "org_id": 1, "title": "县委常委（曾任组织部长）", "start_date": "", "end_date": "约2026年中", "rank": "副处级", "note": "2026年中组织部长交接给谢俊杰"},
    {"person_id": 19, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "约2026年中", "end_date": "", "rank": "副处级", "note": "接任李朝阳"},
    {"person_id": 7, "org_id": 1, "title": "县委常委、宣传部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委、统战部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 3, "title": "县委常委、县纪委书记、县监委代主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 4, "title": "副县长、县公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责公安、司法、退役军人"},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责民政、市场监管、生态环境"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责教育、医保、卫生、文体、旅游"},
    {"person_id": 14, "org_id": 5, "title": "县人大常委会主任", "start_date": "约2025", "end_date": "", "rank": "正处级", "note": "前任县委副书记"},
    {"person_id": 15, "org_id": 6, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 16, "org_id": 7, "title": "市政协副主席（曾任县委书记）", "start_date": "", "end_date": "2025", "rank": "副厅级", "note": "前任明水县委书记"},
    {"person_id": 17, "org_id": 2, "title": "县委副书记、县长（前任）", "start_date": "约2023", "end_date": "2025", "rank": "正处级", "note": "2025-07仍任县长"},
    {"person_id": 18, "org_id": 5, "title": "县人大常委会主任（前任）", "start_date": "", "end_date": "约2025", "rank": "正处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "马福任县委书记、邓吉喆任县长，为明水县现阶段党政正职搭档", "overlap_org": "明水县", "overlap_period": "2026"},
    {"person_a": 16, "person_b": 1, "type": "前任-后继", "context": "刘宝邱前任县委书记（兼市政协副主席）→ 马福接任县委书记", "overlap_org": "中共明水县委员会", "overlap_period": "~2025交接"},
    {"person_a": 17, "person_b": 2, "type": "前任-后继", "context": "邹晓宁前任县长 → 邓吉喆接任县长", "overlap_org": "明水县人民政府", "overlap_period": "~2025-2026"},
    {"person_a": 1, "person_b": 3, "type": "县委班子", "context": "马福(书记)、韩超(副书记)共事", "overlap_org": "中共明水县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "县委班子", "context": "马福(书记)、李朝阳(曾任组织部长)共事", "overlap_org": "中共明水县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 19, "type": "县委班子", "context": "马福(书记)、谢俊杰(组织部长)共事", "overlap_org": "中共明水县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 7, "type": "县委班子", "context": "马福(书记)、王雷(宣传部长)共事", "overlap_org": "中共明水县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 8, "type": "县委班子", "context": "马福(书记)、宋国柏(统战部长)共事", "overlap_org": "中共明水县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 9, "type": "县委班子", "context": "马福(书记)、王英进(政法委书记)共事", "overlap_org": "中共明水县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 10, "type": "县委班子", "context": "马福(书记)、高秀成(纪委书记)共事", "overlap_org": "中共明水县委员会", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "政府班子", "context": "邓吉喆(县长)、王玉林(常务副县长)协理县政府工作", "overlap_org": "明水县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "政府班子", "context": "邓吉喆(县长)、徐健(副县长)共事", "overlap_org": "明水县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 11, "type": "政府班子", "context": "邓吉喆(县长)、张鹏(副县长/公安局长)共事", "overlap_org": "明水县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 12, "type": "政府班子", "context": "邓吉喆(县长)、刘晓香(副县长)共事", "overlap_org": "明水县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 13, "type": "政府班子", "context": "邓吉喆(县长)、单云韬(副县长)共事", "overlap_org": "明水县人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 14, "type": "班子共事", "context": "马福(书记)、杨春玲(人大主任，前任县委副书记)同在领导班子", "overlap_org": "明水县", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "班子共事", "context": "县政府与县政协在县两会等场合共同推进政务", "overlap_org": "明水县", "overlap_period": ""},
    {"person_a": 18, "person_b": 14, "type": "前任-后继", "context": "王振坤前任人大主任 → 杨春玲接任县人大主任", "overlap_org": "明水县人民代表大会常务委员会", "overlap_period": "~2025"},
]

# ── GEXF ───────────────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    if post.startswith("县委书记"):
        return "255,50,50"
    if "县长" in post or "副县长" in post:
        return "50,100,255"
    if "纪委" in post or "监委" in post:
        return "255,165,0"
    return "100,100,100"


def person_size(post):
    if post.startswith("县委书记") or (post.startswith("县委副书记") and "县长" in post):
        return "20.0"
    return "12.0"


def org_color(t):
    return {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
            "政协": "255,240,200", "纪委": "255,230,180"}.get(t, "200,200,200")


def build_gexf(path: Path) -> None:
    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
         f'  <meta lastmodifieddate="{AS_OF}">',
         '    <creator>Gov-Relation Research Agent</creator>',
         f'    <description>{esc(SLUG)} 领导班子工作关系网络 — {AS_OF}</description>',
         '  </meta>', '  <graph mode="static" defaultedgetype="undirected">',
         '    <attributes class="node">',
         '      <attribute id="0" title="type" type="string"/>',
         '      <attribute id="1" title="label" type="string"/>',
         '      <attribute id="2" title="role" type="string"/>',
         '    </attributes>',
         '    <attributes class="edge">',
         '      <attribute id="0" title="type" type="string"/>',
         '      <attribute id="1" title="context" type="string"/>',
         '    </attributes>',
         '    <nodes>']
    for p in persons:
        post = p["current_post"]
        c = person_color(post).split(",")
        L.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        L.append('        <attvalues>')
        L.append('          <attvalue for="0" value="person"/>')
        L.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        L.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        L.append('        </attvalues>')
        L.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        L.append(f'        <viz:size value="{person_size(post)}"/>')
        L.append('      </node>')
    for o in organizations:
        c = org_color(o["type"]).split(",")
        L.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        L.append('        <attvalues>')
        L.append('          <attvalue for="0" value="organization"/>')
        L.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        L.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        L.append('        </attvalues>')
        L.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        L.append('        <viz:size value="8.0"/>')
        L.append('      </node>')
    L.append('    </nodes>')
    L.append('    <edges>')
    eid = 0
    for pos in positions:
        L.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        L.append('        <attvalues>')
        L.append('          <attvalue for="0" value="worked_at"/>')
        L.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        L.append('        </attvalues>')
        L.append('      </edge>')
        eid += 1
    for r in relationships:
        L.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        L.append('        <attvalues>')
        L.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        L.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        L.append('        </attvalues>')
        L.append('      </edge>')
        eid += 1
    L.append('    </edges>')
    L.append('  </graph>')
    L.append('</gexf>')
    path.write_text("\n".join(L), encoding="utf-8")
    print(f"  ✅ GEXF: {path}")


# ── SQLite ──────────────────────────────────────────────────────────────────
def build_db(path: Path) -> None:
    if path.exists():
        path.unlink()
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("CREATE TABLE persons (id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT, birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT, current_post TEXT, current_org TEXT, source TEXT)")
    c.execute("CREATE TABLE organizations (id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT)")
    c.execute("CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER, title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT)")
    c.execute("CREATE TABLE relationships (id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER, type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT)")
    for p in persons:
        c.execute("INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"  ✅ DB: {path}")


# ── Person JSON ─────────────────────────────────────────────────────────────
SOURCES = [
    {"id": "S1", "title": "明水县人民政府官网 本地要闻/时政要闻", "url": "https://www.mingshui.gov.cn/", "publisher": "明水县人民政府",
     "published_at": "2026-01~08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
     "notes": "多次新闻确认 现任县委书记马福、县委副书记县长邓吉喆 等班子"},
    {"id": "S2", "title": "明水县政府 政府领导 简历页", "url": "https://www.mingshui.gov.cn/", "publisher": "明水县人民政府",
     "published_at": "2026-02-26", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
     "notes": "邓吉喆(1987.4/研究生)、王玉林(1973.1)、徐建(1982.5)、张鹏(1972.11)、刘春香(1975.9)、单云韬(1983.8)"},
    {"id": "S3", "title": "明水县政府 县人大主任杨春玲调研", "url": "https://www.mingshui.gov.cn/", "publisher": "明水县人民政府",
     "published_at": "2026-06-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "现任县人大主任 杨春玲"},
    {"id": "S4", "title": "明水县政府 旧新闻(2023-2025)", "url": "https://www.mingshui.gov.cn/", "publisher": "明水县人民政府",
     "published_at": "2023-2025", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
     "notes": "前任县委书记 刘宝邱(兼市政协副主席)、前任县长 邹晓宁"},
    {"id": "S5", "title": "甘南县政府调研报告(build_甘南县_data.py)", "url": "repo:scripts/build/build_甘南县_data.py", "publisher": "gov-relation",
     "published_at": "2026-08", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium",
     "notes": "甘南县委书记 刘正伟, 男汉 1985-01, 明水人; 明水籍跨县线索"},
]


def _gap(priority, q, why, queries):
    return {"priority": priority, "question": q, "why_it_matters": why, "suggested_queries": queries, "last_attempted": AS_OF}


def _rel(person, pid, rtype, strength, evidence, overlap_org="明水县", period="", confidence="confirmed"):
    return {"person": person, "person_id": pid, "relationship_type": rtype, "strength": strength,
            "evidence": evidence, "overlap_org": overlap_org, "overlap_period": period,
            "confidence": confidence, "source_ids": ["S1", "S2"]}


def write_person_jsons() -> None:
    mafu = {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {"province": "黑龙江省", "city": "绥化市", "region": "明水县",
                                "job": "县委书记", "task_id": "heilongjiang_明水县", "time_focus": "2026"},
        "identity": {"person_id": "mingshui_mafu", "name": "马福", "gender": "男", "ethnicity": "汉族",
                     "birth": "", "birthplace": "", "native_place": "", "education": [],
                     "party_join": "", "work_start": "", "dedupe_keys": {}},
        "current_status": {"current_post": "县委书记", "current_org": "中共明水县委员会",
                           "administrative_rank": "正处级", "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S1"]},
        "career_timeline": [
            {"start": "约2025末", "end": "present", "org": "中共明水县委员会", "title": "县委书记",
             "level": "县处", "location": "明水县", "system": "party", "rank": "正处级", "is_key_promotion": True,
             "notes": "接任刘宝邱，为明水县党政一把手", "confidence": "confirmed", "source_ids": ["S1"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "location": "",
             "system": "other", "rank": "", "notes": "公开资料未查到 任书记前的完整履历", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"org": "中共明水县委员会", "type": "党委", "role": "县委书记", "period": "约2025末至今"}],
        "relationships": [
            _rel("邓吉喆", "mingshui_dengjizhe", "overlap", "strong", "与邓吉喆(县长)为明水县党政正职搭档", "明水县", "2026"),
            _rel("刘宝邱", "mingshui_liubaoqiu", "predecessor_successor", "strong", "刘宝邱前任县委书记→马福接任", "中共明水县委员会", "~2025", "plausible"),
            _rel("王玉林", "mingshui_wangyulin", "overlap", "medium", "与常务副县长王玉林共事", "明水县", "2026"),
            _rel("杨春玲", "mingshui_yangchunling", "overlap", "medium", "县人大主任杨春玲（前任县委副书记）", "明水县", "", "plausible"),
        ],
        "governance_record": [
            {"period": "2026-08", "domain": "public_security", "achievement_or_event": "主持防汛形势分析会、深入一线督导防雨, 部署防大汛", "role_in_event": "主持/带队", "location": "明水县", "confidence": "confirmed", "source_ids": ["S1"]},
            {"period": "2026-07", "domain": "livelihood", "achievement_or_event": "深入民政领域专项调研，强调养老服务民生保障", "role_in_event": "调研带队", "location": "明水县", "confidence": "confirmed", "source_ids": ["S1"]},
            {"period": "2026", "domain": "economy", "achievement_or_event": "会见客商洽谈算力/风电项目合作、推进县域招商", "role_in_event": "洽谈牵头", "location": "明水县", "confidence": "confirmed", "source_ids": ["S1"]},
        ],
        "professional_profile": {"primary_specializations": ["党建工作", "应急防汛", "经济项目招商"],
                                 "secondary_specializations": [], "career_pattern": "unknown",
                                 "systems_experience": ["party", "government"], "geographic_pattern": [],
                                 "promotion_velocity": {"summary": "履历不全", "notable_fast_promotions": []}},
        "work_style_and_personality": {
            "public_style_indicators": [{"trait": "grassroots_oriented", "evidence": "首选直插一线方式督导防汛/安全生产/党建", "confidence": "plausible", "source_ids": ["S1"]}],
            "speech_themes": ["以人民为中心", "防汛救民生至上", "营商环境", "乡村振兴", "干部队伍"],
            "management_signals": ["强调部门协同", "一线指挥", "对标省市部署"],
            "caveat": "Work style inferred from public records, not private assessment."},
        "network_metrics": {"degree_centrality": "high", "clusters": ["县委书记-县政府-县委班子"]},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}],
        "source_register": SOURCES,
        "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "马福 完整履历（出生年份、籍贯、教育）未查到"},
        "open_questions": [
            _gap("critical", "马福完整履历？出生年份、籍贯、教育背景、历任职务？", "现任一把手，政治网络关键", ["马福 简历 明水", "马福 任前公示 绥化"]),
            _gap("high", "马福何时从何职调任县委书记？前任交接时间？", "了解交接迹与网络", ["明水县 前任 县委书记", "马福 任职"]),
        ],
    }
    write_json("20260805-黑龙江省-绥化市-县委书记-马福.json", mafu)

    dengjizhe = {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {"province": "黑龙江省", "city": "绥化市", "region": "明水县",
                                "job": "县长", "task_id": "heilongjiang_明水县", "time_focus": "2026"},
        "identity": {"person_id": "mingshui_dengjizhe", "name": "邓吉喆", "gender": "男", "ethnicity": "汉族",
                     "birth": "1987年4月", "birthplace": "", "native_place": "", "education": [
                         {"period": "", "institution": "", "major": "", "degree": "研究生", "study_type": "unknown", "source_ids": ["S2"]}],
                     "party_join": "党员", "work_start": "", "dedupe_keys": {}},
        "current_status": {"current_post": "县委副书记、县长", "current_org": "明水县人民政府",
                           "administrative_rank": "正处级", "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S2"]},
        "career_timeline": [
            {"start": "约2026初", "end": "present", "org": "明水县人民政府", "title": "县长",
             "level": "县处", "location": "明水县", "system": "government", "rank": "正处级", "is_key_promotion": True,
             "notes": "主持县政府全面工作, 分管县财政局(国资办)、审计局", "confidence": "confirmed", "source_ids": ["S2"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "location": "",
             "system": "other", "rank": "", "notes": "公开资料未查到任县长前的职务", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"org": "明水县人民政府", "type": "政府", "role": "县长"}],
        "relationships": [
            _rel("马福", "mingshui_mafu", "overlap", "strong", "与马福(县委书记)为党政搭档", "明水县", "2026"),
            _rel("邹晓宁", "mingshui_zouxiaoning", "predecessor_successor", "strong", "邹晓宁前任县长→邓吉喆接任", "明水县人民政府", "~2025-2026", "plausible"),
            _rel("王玉林", "mingshui_wangyulin", "overlap", "medium", "与常务副县长王玉林共理县政府", "明水县人民政府", "2026"),
            _rel("张冲", "mingshui_zhangpeng", "overlap", "medium", "副县长张冲（公安局长）与县长共事", "明水县人民政府", "2026"),
        ],
        "governance_record": [
            {"period": "2026-08", "domain": "public_security", "achievement_or_event": "主持防汛调度会、实地督导强降雨防范", "role_in_event": "主持", "location": "明水县", "confidence": "confirmed", "source_ids": ["S1"]},
            {"period": "2026-07", "domain": "economy", "achievement_or_event": "主持全县经济运行分析会、部署下半年稳增长", "role_in_event": "主持", "location": "明水县", "confidence": "confirmed", "source_ids": ["S1"]},
            {"period": "2026-06", "domain": "urban", "achievement_or_event": "调研重点项目建设、巡河", "role_in_event": "调研带队", "location": "明水县", "confidence": "confirmed", "source_ids": ["S1"]},
        ],
        "professional_profile": {"primary_specializations": ["经济管理", "政府工作", "项目调度"],
                                 "secondary_specializations": [], "career_pattern": "unknown",
                                 "systems_experience": ["government"], "geographic_pattern": [],
                                 "promotion_velocity": {"summary": "1987年生任县长, 晋升较快, 历不详", "notable_fast_promotions": []}},
        "work_style_and_personality": {
            "public_style_indicators": [{"trait": "pragmatic", "evidence": "主抓经济、项目、防汛", "confidence": "plausible", "source_ids": ["S1"]}],
            "speech_themes": ["稳增长", "重点项目", "防汛", "招商"],
            "management_signals": ["进度督导", "部门协同", "数据会商"],
            "caveat": "Style inferred from public records, not private assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}],
        "source_register": SOURCES,
        "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "邓吉喆 任职前履历/籍贯"},
        "open_questions": [
            _gap("critical", "邓吉喆在任县长前的职务与完整履历？", "评估新兴干部政治网络", ["邓吉喆 简历 明水", "邓吉喆 任前公示"]),
            _gap("medium", "邓吉喆籍贯/出生地？", "同乡分析", ["邓吉喆 籍贯"]),
        ],
    }
    write_json("20260805-黑龙江省-绥化市-县长-邓吉喆.json", dengjizhe)


def write_json(fname: str, data: dict) -> None:
    path = PERSONS_DIR / fname
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Person JSON: {path}")



# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.path.insert(0, str(BASE))
    build_db(DB_PATH)
    build_gexf(GEXF_PATH)
    write_person_jsons()

    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_BUILD.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_PERSONS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
    shutil.copy2(__file__, CANONICAL_BUILD)
    print(f"  ✅ Canonical DB: {CANONICAL_DB}")
    print(f"  ✅ Canonical GEXF: {CANONICAL_GEXF}")
    print(f"  ✅ Canonical build: {CANONICAL_BUILD}")
    print(f"\n✅ Done — {SLUG} data build complete.")


if __name__ == "__main__":
    main()