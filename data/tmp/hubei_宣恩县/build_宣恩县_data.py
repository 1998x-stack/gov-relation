#!/usr/bin/env python3
"""宣恩县领导班子工作关系网络 — 数据构建脚本。

调查时间: 2026-07-24
数据来源: 宣恩县人民政府门户网站 (xe.gov.cn) 时政要闻报道
核心人物: 县委书记王闯、县长安生永
"""

import json
import os
import sqlite3
from datetime import datetime

AS_OF = "2026-07-24"

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "宣恩县_network.db")
GEXF_PATH = os.path.join(STAGING, "宣恩县_network.gexf")
PERSON_DIR = STAGING

# ── Data ───────────────────────────────────────────────────────────────────

persons = [
    {
        "id": "p1",
        "name": "王闯",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1977年5月",
        "birthplace": "湖北来凤",
        "education": "省委党校研究生（待确认）",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共宣恩县委员会",
        "source": "xe.gov.cn; 搜狗微信搜索结果",
        "notes": "赴恩施州各县市区调研也多次见到他。2023年9月前任习覃调离后接任。"
    },
    {
        "id": "p2",
        "name": "安生永",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "宣恩县人民政府",
        "source": "xe.gov.cn 多篇报道",
        "notes": "出生年月、籍贯、教育背景待补充。公开报道中以县长身份主持全县优化营商环境大会、县委全面依法治县工作会议等。"
    },
    {
        "id": "p3",
        "name": "覃正彪",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共宣恩县委员会办公室",
        "source": "http://www.xe.gov.cn/xwdt/xeyw/202607/t20260720_1820779.shtml",
        "notes": "几乎所有王闯调研活动均有陪同，系书记核心幕僚。"
    },
    {
        "id": "p4",
        "name": "卢军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "宣恩县人民政府、宣恩县公安局",
        "source": "http://www.xe.gov.cn/xwdt/xeyw/202605/t20260506_1802098.shtml",
        "notes": ""
    },
    {
        "id": "p5",
        "name": "陈久奎",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宣恩县",
        "source": "xe.gov.cn 多篇报道",
        "notes": "在多次重要会议中担任主持角色，推测为县人大常委会主任或县委专职副书记。具体职务待确认。"
    },
    {
        "id": "p6",
        "name": "周志斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宣恩县",
        "source": "xe.gov.cn 多篇报道",
        "notes": "具体职务待确认。出席县规划委员会会议、灾后重建会议等。"
    },
    {
        "id": "p7",
        "name": "张通军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共宣恩县委员会",
        "source": "xe.gov.cn 多篇报道",
        "notes": "在两优一先表彰大会上宣读表彰决定，在县委理论学习中心组发言。推测为县委组织部部长或县委副书记。具体职务待确认。"
    },
    {
        "id": "p8",
        "name": "向重臣",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宣恩县",
        "source": "xe.gov.cn 报道",
        "notes": "具体职务待确认。出席两优一先表彰大会、中心组学习等。"
    },
    {
        "id": "p9",
        "name": "冉俊杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宣恩县",
        "source": "xe.gov.cn 报道",
        "notes": "在中心组学习作发言，出席灾后重建会议。具体职务待确认。"
    },
    {
        "id": "p10",
        "name": "朱朝春",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宣恩县",
        "source": "xe.gov.cn 报道",
        "notes": "具体职务待确认。出席依法治县会议、灾后重建会议等。"
    },
    {
        "id": "p11",
        "name": "陈勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宣恩县",
        "source": "xe.gov.cn 报道",
        "notes": "具体职务待确认。出席依法治县会议、两优一先表彰大会等。"
    },
    {
        "id": "p12",
        "name": "李俊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宣恩县",
        "source": "xe.gov.cn 报道",
        "notes": "具体职务待确认。出席两优一先表彰大会、中心组学习等。"
    },
    {
        "id": "p13",
        "name": "陶华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宣恩县",
        "source": "xe.gov.cn 报道",
        "notes": "出席县规划委员会会议。具体职务待确认。"
    },
    {
        "id": "p14",
        "name": "唐刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宣恩县",
        "source": "xe.gov.cn 报道",
        "notes": "出席防汛督查、灾后重建会议、规划委员会会议。具体职务待确认。"
    },
    {
        "id": "p15",
        "name": "袁永灿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宣恩县",
        "source": "xe.gov.cn 报道",
        "notes": "出席灾后重建会议、规划委员会会议。具体职务待确认。"
    },
    {
        "id": "p16",
        "name": "舒蓉",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宣恩县",
        "source": "xe.gov.cn 报道",
        "notes": "出席县规划委员会会议。推测为女性。具体职务待确认。"
    },
    {
        "id": "p17",
        "name": "龚家邦",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宣恩县",
        "source": "xe.gov.cn 报道",
        "notes": "出席白水河村灾后重建会议。具体职务待确认。"
    },
    {
        "id": "p18",
        "name": "张亚丹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宣恩工业园区管委会主任",
        "current_org": "宣恩工业园区管委会",
        "source": "http://www.xe.gov.cn/xwdt/xeyw/202606/t20260602_1809358.shtml",
        "notes": ""
    },
]

# ── Predecessor data ──────────────────────────────────────────────────────

predecessors = [
    {
        "id": "p19",
        "name": "习覃",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "湖北广播电视台党委委员、纪委书记",
        "current_org": "湖北广播电视台",
        "source": "搜狗微信搜索结果",
        "notes": "前任宣恩县委书记，2023年9月调任湖北广播电视台党委委员、纪委书记。"
    },
]

all_persons = persons + predecessors

organizations = [
    {"id": 1, "name": "中共宣恩县委员会", "type": "党委", "level": "县级", "parent": "中共恩施州委", "location": "宣恩县"},
    {"id": 2, "name": "宣恩县人民政府", "type": "政府", "level": "县级", "parent": "恩施州人民政府", "location": "宣恩县"},
    {"id": 3, "name": "中共宣恩县委办公室", "type": "党委", "level": "县级", "parent": "中共宣恩县委员会", "location": "宣恩县"},
    {"id": 4, "name": "宣恩县公安局", "type": "政府", "level": "县级", "parent": "宣恩县人民政府", "location": "宣恩县"},
    {"id": 5, "name": "宣恩县人大常委会", "type": "人大", "level": "县级", "parent": "宣恩县", "location": "宣恩县"},
    {"id": 6, "name": "宣恩县政协", "type": "政协", "level": "县级", "parent": "宣恩县", "location": "宣恩县"},
    {"id": 7, "name": "宣恩工业园区管委会", "type": "开发区", "level": "县级", "parent": "宣恩县人民政府", "location": "宣恩县"},
    {"id": 8, "name": "湖北广播电视台", "type": "事业单位", "level": "省级", "parent": "湖北省", "location": "武汉市"},
]

positions = [
    # 王闯
    {"person_id": "p1", "org_id": 1, "title": "县委书记", "start": "2023年", "end": "present", "rank": "正处级", "note": ""},
    # 安生永
    {"person_id": "p2", "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "同时担任县委副书记"},
    # 覃正彪
    {"person_id": "p3", "org_id": 3, "title": "县委常委、县委办公室主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 卢军
    {"person_id": "p4", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p4", "org_id": 4, "title": "县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": "兼任"},
    # 陈久奎
    {"person_id": "p5", "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "推测为县人大常委会主任或县委专职副书记"},
    # 周志斌
    {"person_id": "p6", "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "推测为县委常委或县政府领导"},
    # 张通军
    {"person_id": "p7", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "推测为县委组织部部长或县委副书记"},
    # 向重臣
    {"person_id": "p8", "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 冉俊杰
    {"person_id": "p9", "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 朱朝春
    {"person_id": "p10", "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 陈勇
    {"person_id": "p11", "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 李俊
    {"person_id": "p12", "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 陶华
    {"person_id": "p13", "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 唐刚
    {"person_id": "p14", "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 袁永灿
    {"person_id": "p15", "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 舒蓉
    {"person_id": "p16", "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 龚家邦
    {"person_id": "p17", "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 张亚丹
    {"person_id": "p18", "org_id": 7, "title": "管委会主任", "start": "", "end": "present", "rank": "", "note": ""},
    # 习覃 (predecessor)
    {"person_id": "p19", "org_id": 1, "title": "县委书记", "start": "", "end": "2023年9月", "rank": "正处级", "note": "前任县委书记"},
    {"person_id": "p19", "org_id": 8, "title": "党委委员、纪委书记", "start": "2023年9月", "end": "present", "rank": "副厅级", "note": "调任湖北广播电视台"},
]

relationships = [
    # 王闯 <-> 安生永 (党政正职搭档)
    {"person_a": "p1", "person_b": "p2", "type": "党政搭档", "context": "县委书记与县长，在县规划委员会会议、优化营商环境大会等多项工作中密切配合", "overlap_org": "宣恩县", "overlap_period": "2023至今", "confidence": "confirmed"},
    # 王闯 <-> 覃正彪 (书记与办公室主任)
    {"person_a": "p1", "person_b": "p3", "type": "上下级", "context": "覃正彪作为县委办主任，在王闯的调研活动中几乎全程陪同", "overlap_org": "中共宣恩县委员会", "overlap_period": "2024至今", "confidence": "confirmed"},
    # 王闯 <-> 卢军 (书记与公安局长)
    {"person_a": "p1", "person_b": "p4", "type": "上下级", "context": "县委书记与分管公安工作的副县长", "overlap_org": "宣恩县", "overlap_period": "", "confidence": "confirmed"},
    # 陈久奎 (推测为主持会议的县领导)
    {"person_a": "p1", "person_b": "p5", "type": "上下级", "context": "陈久奎在多个重要会议中担任主持（两优一先表彰大会、依法治县会议等）", "overlap_org": "宣恩县", "overlap_period": "", "confidence": "confirmed"},
    # 张通军
    {"person_a": "p1", "person_b": "p7", "type": "上下级", "context": "张通军作为县委常委，在表彰大会宣读决定，参与中心组学习研讨", "overlap_org": "中共宣恩县委员会", "overlap_period": "", "confidence": "confirmed"},
    # 安生永 <-> 卢军
    {"person_a": "p2", "person_b": "p4", "type": "上下级", "context": "县长与分管副县长", "overlap_org": "宣恩县人民政府", "overlap_period": "", "confidence": "confirmed"},
    # 习覃 -> 王闯 (前后任)
    {"person_a": "p19", "person_b": "p1", "type": "前后任", "context": "习覃离任宣恩县委书记后，王闯接任", "overlap_org": "中共宣恩县委员会", "overlap_period": "2023年", "confidence": "confirmed"},
    # 共同出席重要会议 - 基于报道的多位领导交集
    {"person_a": "p5", "person_b": "p7", "type": "同场合", "context": "陈久奎与张通军共同参加两优一先表彰大会、依法治县工作会议等", "overlap_org": "宣恩县", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": "p5", "person_b": "p6", "type": "同场合", "context": "共同出席县规划委员会会议", "overlap_org": "宣恩县", "overlap_period": "2026年7月", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p6", "type": "同场合", "context": "王闯与周志斌共同出席多个会议及调研活动", "overlap_org": "宣恩县", "overlap_period": "2026年", "confidence": "confirmed"},
]


# ── Build ──────────────────────────────────────────────────────────────────

def build():
    """Run database + GEXF build."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # ── SQLite ──────────────────────────────────────────────────────────
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for t in ("relationships", "positions", "organizations", "persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")

    cur.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT, notes TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT, confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    def pid(s):
        return int(s[1:])

    for p in all_persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pid(p["id"]), p["name"], p.get("gender", ""), p.get("ethnicity", ""),
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
    print(f"   {len(all_persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ────────────────────────────────────────────────────────────────

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color_and_size(post):
        if "县委书记" in post and "副" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post and "副" not in post and "委" not in post:
            return ("50,100,255", 20.0)
        elif "县委常委" in post:
            return ("100,150,255", 15.0)
        elif "副" in post and ("县长" in post or "县" in post):
            return ("100,150,255", 12.0)
        elif "副县长" in post:
            return ("100,150,255", 12.0)
        elif "县领导" in post:
            return ("100,100,100", 12.0)
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
        "开发区": ("200,255,200", 8.0),
        "事业单位": ("220,220,220", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>宣恩县领导班子工作关系网络 - 2026年7月</description>')
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
    for p in all_persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
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
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization
    for pos in positions:
        eid += 1
        pid_val = pos["person_id"]
        lines.append(f'      <edge id="e{eid}" source="{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")

    print(f"\n{'='*60}")
    print(f"宣恩县 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(all_persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
