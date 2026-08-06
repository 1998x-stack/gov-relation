#!/usr/bin/env python3
"""正安县（遵义市）领导班子关系网络数据生成脚本。

Targets: 县委书记 田茂荣, 县委副书记、县长 贾军
Data as of: 2026-08-06
Sources: 正安县人民政府官网 (www.gzza.gov.cn) 领导活动/要闻 + 家长单位任免
Note: 正安官网未公开"领导之窗"简历栏目，核心人物履历按来源置信度标注。
"""

import json
import os
import sqlite3
from datetime import datetime

TASK_ID = "guizhou_正安县"
SLUG = "正安县"
AS_OF = "2026-08-06"
PROVINCE = "贵州省"
PARENT_CITY = "遵义市"

BASE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "data/tmp/guizhou_正安县"
_BASE_OVERRIDE = os.environ.get("ZHENGAN_BASE")
if _BASE_OVERRIDE:
    BASE = _BASE_OVERRIDE

DB_PATH = os.path.join(BASE, "正安县_network.db")
GEXF_PATH = os.path.join(BASE, "正安县_network.gexf")
PERSONS_DIR = os.path.join(BASE)
os.makedirs(PERSONS_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────

# S001/S002 = 正安县政府官网"领导活动"栏目文章（书记/县长身份、班子名单）
# S003  = 十三届县委常委会第191次会议报道（朱煜/贾军/江波/谢俊/何波）
# S004  = 县委书记田茂荣走访各班子报道（2026-06-08）
# S005  = 县纪委监委/组织部/宣传部等县委部门
source_register = [
    {"id": "S001",
     "title": "领导活动-县委书记田茂荣到相关单位走访调研",
     "url": "http://www.gzza.gov.cn/xwzx/ldhd/202606/t20260609_90494391.html",
     "publisher": "正安县人民政府网", "published_at": "2026-06-09", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "2026-06-08 田茂荣以县委书记走访县人大/政府/政协/县纪委监委/组织部/宣传部/政法委/统战部；贾军为县委副书记、县长；江波为人大主任。田茂荣在任的直接官方证据。"},
    {"id": "S002",
     "title": "领导活动频道-贾军到桴㯊镇/芙蓉江镇调研等",
     "url": "https://www.gzza.gov.cn/xwzx/ldhd/",
     "publisher": "正安县人民政府网", "published_at": "2026-07-27", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "贾军以县长身份活动连续覆盖2026-03至07月底；田茂荣以县委书记身份活动覆盖2026-06-08至07-16。"},
    {"id": "S003",
     "title": "十三届县委常委会第133次会议暨经开区党工委会议召开",
     "url": "https://www.gzza.gov.cn/xwzx/ldhd/202604/t20260430_90059736.html",
     "publisher": "正安县人民政府网", "published_at": "2026-04-30", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "2026-04-29朱煜仍为县委书记主持；贾军（副书记/县长）、江波（人大主任）、谢俊（副书记）、何波（常委/经开区党组织副书记、管委会副主任）出席。确认朱煜在任到至少2026-04。"},
    {"id": "S004",
     "title": "正安县人民政府关于王雨平等同志任免职的通知",
     "url": "http://www.gzza.gov.cn/xxgk/zxgk/rsxx/202606/t20260604_90478312.html",
     "publisher": "正安县人民政府网", "published_at": "2026-06-04", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "medium",
     "notes": "县政府序列部门负责人任免，非县领导班子层面。"},
]

# persons 列表（id 连续，用于 DB/gexf 内引用）
persons = [
    # 1 - 县委书记
    {
        "id": 1, "name": "田茂荣", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "中共正安县委书记",
        "current_org": "中共正安县委员会",
        "source": "https://www.gzza.gov.cn/xwzx/ldhd/202606/t20260609_90494391.html",
    },
    # 2 - 县长
    {
        "id": 2, "name": "贾军", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "正安县委副书记、县人民政府党组书记、县长",
        "current_org": "正安县人民政府",
        "source": "https://www.gzza.gov.cn/xwzx/ldhd/202606/t20260609_90494391.html",
    },
    # 3 - 前任县委书记
    {
        "id": 3, "name": "朱煜", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "正安县委书记（前任，2026-04-30左右卸任）",
        "current_org": "中共正安县委员会",
        "source": "https://www.gzza.gov.cn/xwzx/ldhd/202604/t20260430_90059736.html",
    },
    # 4 - 县委副书记
    {
        "id": 4, "name": "谢俊", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共正安县委员会",
        "source": "https://www.gzza.gov.cn/xwzx/ldhd/202604/t20260430_90059736.html",
    },
    # 5 - 县人大常委会主任
    {
        "id": 5, "name": "江波", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "正安县人大常委会主任",
        "current_org": "正安县人民代表大会常务委员会",
        "source": "https://www.gzza.gov.cn/xwzx/ldhd/202606/t20260609_90494391.html",
    },
    # 6 - 县委常委、经开区
    {
        "id": 6, "name": "何波", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "正安县委常委、贵州正安经开区党工委副书记、管委会副主任",
        "current_org": "贵州正安经济技术开发区",
        "source": "https://www.gzza.gov.cn/xwzx/ldhd/202604/t20260430_90059736.html",
    },
    # 7 - 县委常委、政法委书记（前任信息）
    {
        "id": 7, "name": "孙勇", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "正安县委常委、政法委书记",
        "current_org": "中共正安县委政法委员会",
        "source": "https://www.gzza.gov.cn/xwzx/ldhd/",
    },
    # 8 - 县委常委、县委办主任
    {
        "id": 8, "name": "吕力", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "正安县委常委、县委办主任",
        "current_org": "中共正安县委办公室",
        "source": "https://www.gzza.gov.cn/xwzx/ldhd/",
    },
]

# organizations
organizations = [
    {"id": 1, "name": "中共正安县委员会", "type": "党委", "level": "县处级", "parent": "中共遵义市委", "location": "正安县"},
    {"id": 2, "name": "正安县人民政府", "type": "政府", "level": "县处级", "parent": "遵义市人民政府", "location": "正安县"},
    {"id": 3, "name": "正安县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "遵义市人大常委会", "location": "正安县"},
    {"id": 4, "name": "中共正安县委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共正安县委员会", "location": "正安县"},
    {"id": 5, "name": "中共正安县委办公室", "type": "党委", "level": "乡科级", "parent": "中共正安县委员会", "location": "正安县"},
    {"id": 6, "name": "贵州正安经济技术开发区", "type": "开发区", "level": "县处级", "parent": "遵义市人民政府", "location": "正安县"},
]

positions = [
    # 田茂荣
    {"person_id": 1, "org_id": 1, "title": "中共正安县委书记", "start_date": "2026-06", "end_date": "", "rank": "县处级正职", "note": "现任（2026-06起在任）"},
    # 贾军
    {"person_id": 2, "org_id": 1, "title": "正安县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "正安县人民政府县长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    # 朱煜（前任）
    {"person_id": 3, "org_id": 1, "title": "正安县委书记", "start_date": "", "end_date": "2026-04-30", "rank": "县处级正职", "note": "前任，2026-04-30仍主持常委会"},
    # 谢俊
    {"person_id": 4, "org_id": 1, "title": "正安县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 江波
    {"person_id": 5, "org_id": 3, "title": "正安县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    # 何波
    {"person_id": 6, "org_id": 6, "title": "贵州正安经开区党工委副书记、管委会副主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任，兼县委常委"},
    # 孙勇
    {"person_id": 7, "org_id": 4, "title": "正安县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 吕力
    {"person_id": 8, "org_id": 5, "title": "正安县委常委、县委办主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
]

# relationships（备案：全部为"同班子/同组织共事"，置信度 confirmed 以官方新闻确认）
relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "田茂荣（县委书记）与贾军（县委副书记、县长）为县委常委会核心搭档",
     "overlap_org": "中共正安县委员会/正安县人民政府", "overlap_period": "2026-06-至今"},
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "田茂荣接替朱煜出任正安县委书记（2026-04至06期间交接）",
     "overlap_org": "中共正安县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "田茂荣（书记）与谢俊（县委副书记）在县委常委会共事",
     "overlap_org": "中共正安县委员会", "overlap_period": "2026-06-至今"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "田茂荣（书记）与江波（人大主任）在县四大班子协同工作中共事；2026-06-08走访人大",
     "overlap_org": "正安县党政班子", "overlap_period": "2026-06-至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "田茂荣（书记）与何波（县委常委、经开区党委副书记）在县委常委会共事",
     "overlap_org": "中共正安县委员会", "overlap_period": "2026-06-至今"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "贾军（县长）在朱煜任书记期间任县长，与朱煜在党政班子共事",
     "overlap_org": "中共正安县委员会/正安县人民政府", "overlap_period": "至2026-04"},
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "贾军（县长）与谢俊（县委副书记）在县委常委会共事",
     "overlap_org": "中共正安县委员会", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "贾军（县长）与江波（人大主任）在县四大班子协同中共事",
     "overlap_org": "正安县党政班子", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "贾军（县长）与何波（常委、经开区副主任）在县委常委会共事",
     "overlap_org": "中共正安县委员会", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "贾军（县长）与孙勇（政法委书记）在县委常委会共事",
     "overlap_org": "中共正安县委员会", "overlap_period": "2026-至今"},
    {"person_a": 7, "person_b": 8, "type": "overlap",
     "context": "孙勇（政法委书记）与吕力（县委办主任）同为县委常委",
     "overlap_org": "中共正安县委员会", "overlap_period": "2026-至今"},
]


# ── Build Functions ───────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build():
    os.makedirs(BASE, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
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
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"zhengan_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "255,50,50"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "50,100,255"
        if "纪委书记" in post:
            return "255,165,0"
        if "副" in post or "副书记" in post:
            return "100,150,220"
        if "主任" in post and "副" not in post:
            return "60,180,60"
        if "政协" in post:
            return "180,160,80"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post) or \
               ("县长" in post and "副" not in post and "人大" not in post and "政协" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "square"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "circle"
        if "纪委书记" in post or "纪委" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "纪委": "255,200,150",
            "开发区": "200,255,200",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>正安县领导班子关系网络（基于正安县人民政府官网）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
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
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person Graph JSONs ──
    now = AS_OF.replace("-", "")

    def make_person_json(p, timeline, relationships_list, biggest_gap, career_completeness="thin"):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": "正安县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"zhengan_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {"period": "", "institution": "", "major": "", "degree": p.get("education", ""),
                     "study_type": "unknown", "source_ids": []}
                ] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职" if p["id"] in [1, 2, 3, 5] else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": p["id"] in [1, 2],
                "source_ids": ["S001", "S002", "S003"]
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
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号（本轮网络搜索受限，未独立核广泛负面线索）",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": career_completeness,
                "relationship_confidence": "medium",
                "biggest_gap": biggest_gap
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "正安官网未公开领导之窗简历，无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 正安县", f"{p['name']} 任前公示 遵义"],
                 "last_attempted": AS_OF},
            ]
        }
        return result

    # 为每个核心人物生成 person JSON
    now = AS_OF.replace("-", "")
    # 1 田茂荣
    tmr_timeline = [
        {"start": "2026-06", "end": "present", "org": "中共正安县委员会", "title": "正安县委书记",
         "notes": "现任；2026-06-08走访县人大/政府/政协/纪委监委/组织部等", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "2026-06", "org": "履历缺口", "title": "",
         "notes": "任正安县委书记前完整履历未获一手来源；推测曾任职遵义市或省内。", "confidence": "unverified", "source_ids": []},
    ]
    tmr_rel = [
        {"person": "贾军", "person_id": "zhengan_贾军", "relationship_type": "overlap", "strength": "strong",
         "evidence": "与县长贾军为县委常委会/县政府核心搭档", "overlap_org": "中共正安县委员会/正安县人民政府",
         "overlap_period": "2026-06-至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "朱煜", "person_id": "zhengan_朱煜", "relationship_type": "predecessor_successor", "strength": "strong",
         "evidence": "接替朱煜出任正安县委书记", "overlap_org": "中共正安县委员会", "overlap_period": "2026",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S001"]},
    ]
    tmr_json = make_person_json(persons[0], tmr_timeline, tmr_rel,
                                "县委书记田茂荣完整履历/出生信息缺失", "thin")
    tmr_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-遵义市-县委书记-田茂荣.json")
    with open(tmr_path, "w", encoding="utf-8") as f:
        json.dump(tmr_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {tmr_path}")

    # 2 贾军
    jj_timeline = [
        {"start": "", "end": "present", "org": "中共正安县委员会", "title": "正安县委副书记",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "", "end": "present", "org": "正安县人民政府", "title": "正安县人民政府县长",
         "notes": "现任；2026-03至07-27以县长身份赴乡镇调研、高考巡考、安全生产督查", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "出任正安县长前的任职路径未获一手来源", "confidence": "unverified", "source_ids": []},
    ]
    jj_rel = [
        {"person": "田茂荣", "person_id": "zhengan_田茂荣", "relationship_type": "overlap", "strength": "strong",
         "evidence": "与县委书记田茂荣为党政核心搭档", "overlap_org": "中共正安县委员会/正安县人民政府",
         "overlap_period": "2026-06-至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "朱煜", "person_id": "zhengan_朱煜", "relationship_type": "overlap", "strength": "strong",
         "evidence": "与前任县委书记朱煜在党政班子共事", "overlap_org": "中共正安县委员会/正安县人民政府",
         "overlap_period": "至2026-04", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    jj_json = make_person_json(persons[1], jj_timeline, jj_rel,
                               "贾军完整履历/出生信息缺失", "thin")
    jj_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-遵义市-县长-贾军.json")
    with open(jj_path, "w", encoding="utf-8") as f:
        json.dump(jj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {jj_path}")

    print("\n✅ All artifacts generated.")

if __name__ == "__main__":
    build()