#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Wuqiao County (吴桥县), Cangzhou, Hebei.

Data compiled from:
 - 吴桥县人民政府官网 机构设置/领导分工 (as of 2026-07)
 - 中共吴桥县委 巡视整改进展情况通报 (2026-06-16)
 - 网易新闻 2024-09-17 吴桥县委主要负责同志调整
 - 沧州市既有数据集 (新华区 前区长 陈国帮)
Confidence labels: confirmed / plausible / unverified. Gaps preserved, not fabricated.
"""

import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _parent in REPO_ROOT.parents:
    if (_parent / "gov_relation").is_dir():
        REPO_ROOT = _parent
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "吴桥县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "吴桥县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "吴桥县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "吴桥县_network.db"
    GEXF_PATH = GRAPH_DIR / "吴桥县_network.gexf"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── 现任县委书记 / 县长 ──
    {"id": 1, "name": "陈国帮", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴桥县委书记、吴桥经济开发区党工委书记(兼)、一级调研员",
     "current_org": "中共吴桥县委员会",
     "source": "网易新闻2024-09-17; 沧州市新华区档案"},
    {"id": 2, "name": "崔雪刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-05", "birthplace": "待查", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、县政府县长、县经济开发区管委会主任",
     "current_org": "吴桥县人民政府",
     "source": "吴桥县人民政府官网 领导简介 (2023-05)"},
    # ── 前任领导 ──
    {"id": 3, "name": "崔炳甫", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原吴桥县委书记(另有任用)、一级调研员",
     "current_org": "中共吴桥县委员会(前任)",
     "source": "网易新闻 2024-09-17"},
    {"id": 4, "name": "张长瑞", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "更早前任吴桥县委书记(涉调查传闻,未证实)",
     "current_org": "中共吴桥县委员会(更早前任)",
     "source": "搜索引擎联想词(unverified)"},
    # ── 县政府班子 ──
    {"id": 5, "name": "张宇", "gender": "男", "ethnicity": "回族",
     "birth": "1981-02", "birthplace": "", "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县政府常务副县长",
     "current_org": "吴桥县人民政府",
     "source": "吴桥县人民政府官网 领导分工 (2026-07)"},
    {"id": 6, "name": "王新军", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-07", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长",
     "current_org": "吴桥县人民政府",
     "source": "吴桥县人民政府官网 领导分工 (2026-07)"},
    {"id": 7, "name": "王涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-07", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长",
     "current_org": "吴桥县人民政府",
     "source": "吴桥县人民政府官网 领导分工 (2026-07)"},
    {"id": 8, "name": "赵广宇", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-06", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长、公安局党委书记、局长、四级高级警长",
     "current_org": "吴桥县公安局",
     "source": "吴桥县人民政府官网 领导分工 (2026-07)"},
    {"id": 9, "name": "孙亚英", "gender": "女", "ethnicity": "汉族",
     "birth": "1980-10", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长",
     "current_org": "吴桥县人民政府",
     "source": "吴桥县人民政府官网 领导分工 (2026-07)"},
    {"id": 10, "name": "李树立", "gender": "男", "ethnicity": "汉族",
     "birth": "1992-12", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长",
     "current_org": "吴桥县人民政府",
     "source": "吴桥县人民政府官网 领导分工 (2026-07)"},
]

organizations = [
    {"id": 1, "name": "中共吴桥县委员会", "type": "党委", "level": "县处级",
     "parent": "中共沧州市委员会", "location": "河北省沧州市吴桥县"},
    {"id": 2, "name": "吴桥县人民政府", "type": "政府", "level": "县处级",
     "parent": "沧州市人民政府", "location": "河北省沧州市吴桥县"},
    {"id": 3, "name": "吴桥经济开发区管委会", "type": "开发区", "level": "县处级(省级)",
     "parent": "吴桥县人民政府", "location": "河北省沧州市吴桥县"},
    {"id": 4, "name": "吴桥县公安局", "type": "政府", "level": "乡科级",
     "parent": "吴桥县人民政府/沧州市公安局", "location": "河北省沧州市吴桥县"},
    {"id": 5, "name": "中共吴桥县纪律检查委员会/监察委员会", "type": "党委", "level": "县处级",
     "parent": "中共吴桥县委员会/沧州市纪委监委", "location": "河北省沧州市吴桥县"},
    {"id": 6, "name": "吴桥县人大常委会", "type": "人大", "level": "县处级",
     "parent": "沧州市人大常委会", "location": "河北省沧州市吴桥县"},
    {"id": 7, "name": "中国人民政治协商会议吴桥县委员会", "type": "政协", "level": "县处级",
     "parent": "沧州市政协", "location": "河北省沧州市吴桥县"},
    {"id": 8, "name": "中共沧州市新华区委员会", "type": "党委", "level": "县处级",
     "parent": "中共沧州市委员会", "location": "河北省沧州市新华区"},
    {"id": 9, "name": "沧州市新华区人民政府", "type": "政府", "level": "县处级",
     "parent": "沧州市人民政府", "location": "河北省沧州市新华区"},
    {"id": 10, "name": "中共南皮县委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共南皮县委员会", "location": "河北省沧州市南皮县"},
    {"id": 11, "name": "中共盐山县委办公室", "type": "党委", "level": "乡科级",
     "parent": "中共盐山县委员会", "location": "河北省沧州市盐山县"},
    {"id": 12, "name": "沧州市人民政府", "type": "政府", "level": "地厅级",
     "parent": "河北省人民政府", "location": "河北省沧州市"},
    {"id": 13, "name": "中共沧州市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共河北省委", "location": "河北省沧州市"},
]

positions = [
    # ── 陈国帮 (县委书记) ──
    {"person_id": 1, "org_id": 11, "title": "盐山县委常委、县委办公室主任",
     "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "南皮县委常委、组织部部长",
     "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "沧州市人民政府常务副秘书长",
     "start": "", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "沧州市新华区委副书记(兼)",
     "start": "约2021", "end": "约2024", "rank": "正县级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "沧州市新华区委副书记、区政府区长",
     "start": "约2021", "end": "约2024/2025", "rank": "正县级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "吴桥县委书记(一级调研员)",
     "start": "2024-09-15", "end": "present", "rank": "副厅级(一级调研员)", "note": "2024-09-15领导干部大会宣布;2026-05-09主持县委十二届十二次全会"},
    {"person_id": 1, "org_id": 3, "title": "吴桥经济开发区党工委书记(兼)",
     "start": "2024-09-15", "end": "present", "rank": "", "note": ""},

    # ── 崔雪刚 (县长) ──
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县政府代县长",
     "start": "约2022", "end": "约2023", "rank": "正县级", "note": "公开履历前段待查"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长",
     "start": "约2023", "end": "present", "rank": "正县级", "note": "2023-05官方在任;2026-07分工仍获县领导协助"},
    {"person_id": 2, "org_id": 3, "title": "县经济开发区管委会主任",
     "start": "", "end": "present", "rank": "", "note": "县委副书记、县长兼任"},

    # ── 崔炳甫 (前任书记) ──
    {"person_id": 3, "org_id": 1, "title": "吴桥县委书记、吴桥经济开发区党工委书记(兼)、一级调研员",
     "start": "", "end": "2024-09-15", "rank": "一级调研员", "note": "2024-09-15免职,另有任用"},

    # ── 张长瑞 (更早前任) ──
    {"person_id": 4, "org_id": 1, "title": "更早前任吴桥县委书记",
     "start": "", "end": "", "rank": "", "note": "涉'被调查'传闻,unverified"},

    # ── 张宇 (常务副县长) ──
    {"person_id": 5, "org_id": 1, "title": "吴桥县委、县政府常务副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "因2026-07分工,协助县长崔雪刚分管审计"},
    {"person_id": 5, "org_id": 2, "title": "吴桥县政府常务副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "发改、财税、人社、应急、政务公开、京津冀协同"},

    # ── 王新军 ──
    {"person_id": 6, "org_id": 2, "title": "县政府副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "负责住建、交通运输、城管、市政"},

    # ── 王涛 ──
    {"person_id": 7, "org_id": 2, "title": "县政府副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "负责自然资源、农业农村、乡村振兴、民政、水务"},

    # ── 赵广宇 ──
    {"person_id": 8, "org_id": 4, "title": "副县长、公安局党委书记、局长、四级高级警长",
     "start": "", "end": "present", "rank": "副县级", "note": "负责公安、司法、退役军人事务、社会稳定"},

    # ── 孙亚英 ──
    {"person_id": 9, "org_id": 2, "title": "县政府副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "负责教育、卫健、医保、文旅、杂技、大运河文化带"},

    # ── 李树立 ──
    {"person_id": 10, "org_id": 3, "title": "县政府副县长(兼，协助开发区)",
     "start": "", "end": "present", "rank": "副县级", "note": "负责商务、工信、招商引资、金融、环保、开发区"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "陈国帮任县委书记、崔雪刚任县长，党政一把手搭档，共同领导县委、县政府",
     "overlap_org": "中共吴桥县委员会/吴桥县人民政府",
     "overlap_period": "2024-09至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "strength": "strong",
     "context": "陈国帮接替崔炳甫任吴桥县委书记、吴桥经济开发区党工委书记(兼)",
     "overlap_org": "中共吴桥县委员会",
     "overlap_period": "2024-09-15", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor", "strength": "weak",
     "context": "张长瑞为更早前任吴桥县委书记(时间线仅部分可考)",
     "overlap_org": "中共吴桥县委员会",
     "overlap_period": "更早", "confidence": "unverified"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "陈国帮与张宇同县委/政府班子共事，张宇任县委、县政府常务副县长",
     "overlap_org": "中共吴桥县委员会/吴桥县人民政府",
     "overlap_period": "2024-09至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "strength": "strong",
     "context": "陈国帮与王新军在县政府班子共事",
     "overlap_org": "吴桥县人民政府",
     "overlap_period": "2024-09至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "strength": "strong",
     "context": "陈国帮与王涛在县政府班子共事",
     "overlap_org": "吴桥县人民政府",
     "overlap_period": "2024-09至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "strength": "strong",
     "context": "陈国帮与赵广宇(副县长兼公安局长)在工作中直接对接(公安、维稳)",
     "overlap_org": "吴桥县人民政府",
     "overlap_period": "2024-09至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "strength": "strong",
     "context": "陈国帮与孙亚英(主管文旅/杂技/大运河)共事",
     "overlap_org": "吴桥县人民政府",
     "overlap_period": "2024-09至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "strength": "strong",
     "context": "陈国帮与李树立共事，李树立协助开发区工作",
     "overlap_org": "吴桥经济开发区管委会",
     "overlap_period": "2024-09至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "崔雪刚(县长)与张宇(常务副县长)直接搭班，张宇协助崔雪刚分管审计",
     "overlap_org": "吴桥县人民政府",
     "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "strength": "strong",
     "context": "崔雪刚(县长)与王新军在县政府共事",
     "overlap_org": "吴桥县人民政府",
     "overlap_period": "约2023-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "strength": "strong",
     "context": "崔雪刚(县长)与王涛在县政府共事",
     "overlap_org": "吴桥县人民政府",
     "overlap_period": "约2023-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "strength": "strong",
     "context": "崔雪刚(县长)与赵广宇在县政府共事",
     "overlap_org": "吴桥县人民政府",
     "overlap_period": "约2023-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "strength": "strong",
     "context": "崔雪刚(县长)与孙亚英在县政府共事",
     "overlap_org": "吴桥县人民政府",
     "overlap_period": "约2023-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "strength": "medium",
     "context": "崔雪刚(县长)与李树立在县政府共事，李树立协助开发区及项目建设",
     "overlap_org": "吴桥县人民政府",
     "overlap_period": "约2024-至今", "confidence": "confirmed"},
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p["current_post"]
    if "县委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif ("县长" in role and "副书记" in role) or ("县长" in role):
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    else:
        return "100,100,100"


def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")


def is_top_leader(p):
    role = p["current_post"]
    return ("县委书记" in role and "副书记" not in role) or ("县长" in role and "副书记" in role)


def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"


# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>吴桥县领导班子工作关系网络 - 河北省沧州市吴桥县</description>')
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
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append('          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()