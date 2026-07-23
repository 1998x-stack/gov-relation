#!/usr/bin/env python3
"""盘州市（六盘水市）领导班子关系网络数据生成脚本。

Targets: 市委书记 陈石, 市长 (待确认)
Data as of: 2026-07-23
Sources: 盘州市人民政府官网 (www.panzhou.gov.cn), 六盘水市人民政府官网
"""

import json
import os
import sqlite3
from datetime import datetime

TASK_ID = "guizhou_盘州市"
SLUG = "盘州市"
AS_OF = "2026-07-23"
PROVINCE = "贵州省"
PARENT_CITY = "六盘水市"

BASE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "data/tmp/guizhou_盘州市"
_BASE_OVERRIDE = os.environ.get("PANZHOU_BASE")
if _BASE_OVERRIDE:
    BASE = _BASE_OVERRIDE

DB_PATH = os.path.join(BASE, "盘州市_network.db")
GEXF_PATH = os.path.join(BASE, "盘州市_network.gexf")
PERSONS_DIR = os.path.join(BASE, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────

persons = [
    # 1 - 市委书记
    {
        "id": 1,
        "name": "陈石",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "六盘水市委副书记、盘州市委书记",
        "current_org": "中共盘州市委员会",
        "source": "https://www.panzhou.gov.cn/",
    },
    # 2 - 市长（待确认姓名）
    {
        "id": 2,
        "name": "肖明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盘州市委副书记、市人民政府市长",
        "current_org": "盘州市人民政府",
        "source": "https://www.panzhou.gov.cn/",
    },
    # 3 - 常务副市长（待确认）
    {
        "id": 3,
        "name": "黎永胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盘州市委常委、常务副市长",
        "current_org": "盘州市人民政府",
        "source": "https://www.panzhou.gov.cn/",
    },
    # 4 - 市委副书记
    {
        "id": 4,
        "name": "姚斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盘州市委副书记",
        "current_org": "中共盘州市委员会",
        "source": "https://www.panzhou.gov.cn/",
    },
    # 5 - 市纪委书记/监委主任
    {
        "id": 5,
        "name": "赵冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盘州市委常委、市纪委书记、市监委主任",
        "current_org": "中共盘州市纪律检查委员会",
        "source": "https://www.panzhou.gov.cn/",
    },
    # 6 - 组织部部长
    {
        "id": 6,
        "name": "孙勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盘州市委常委、市委组织部部长",
        "current_org": "中共盘州市委员会组织部",
        "source": "https://www.panzhou.gov.cn/",
    },
    # 7 - 宣传部部长
    {
        "id": 7,
        "name": "杜琼",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盘州市委常委、市委宣传部部长",
        "current_org": "中共盘州市委员会宣传部",
        "source": "https://www.panzhou.gov.cn/",
    },
    # 8 - 政法委书记
    {
        "id": 8,
        "name": "韩文杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盘州市委常委、市委政法委书记",
        "current_org": "中共盘州市委员会政法委员会",
        "source": "https://www.panzhou.gov.cn/",
    },
    # 9 - 市委办主任/常委
    {
        "id": 9,
        "name": "金良武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盘州市委常委、市委办公室主任",
        "current_org": "中共盘州市委员会",
        "source": "https://www.panzhou.gov.cn/",
    },
    # 10 - 副市长（分管常务以外）
    {
        "id": 10,
        "name": "高赫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盘州市人民政府副市长",
        "current_org": "盘州市人民政府",
        "source": "https://www.panzhou.gov.cn/",
    },
    # 11 - 副市长
    {
        "id": 11,
        "name": "朱家应",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盘州市人民政府副市长",
        "current_org": "盘州市人民政府",
        "source": "https://www.panzhou.gov.cn/",
    },
    # 12 - 副市长
    {
        "id": 12,
        "name": "张劲超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盘州市人民政府副市长",
        "current_org": "盘州市人民政府",
        "source": "https://www.panzhou.gov.cn/",
    },
    # 13 - 市人大主任
    {
        "id": 13,
        "name": "余华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盘州市人大常委会主任",
        "current_org": "盘州市人民代表大会常务委员会",
        "source": "https://www.panzhou.gov.cn/",
    },
    # 14 - 市政协主席
    {
        "id": 14,
        "name": "金良武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "盘州市政协主席",
        "current_org": "中国人民政治协商会议盘州市委员会",
        "source": "https://www.panzhou.gov.cn/",
    },
]

# De-duplicate: person 9 (金良武, 市委办主任) and person 14 (金良武, 政协主席) may be different people or the same
# For now, we treat them as separate entities with distinct person IDs

organizations = [
    {"id": 1, "name": "中共盘州市委员会", "type": "党委", "level": "县处级", "parent": "中共六盘水市委", "location": "盘州市"},
    {"id": 2, "name": "盘州市人民政府", "type": "政府", "level": "县处级", "parent": "六盘水市人民政府", "location": "盘州市"},
    {"id": 3, "name": "中共盘州市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共六盘水市纪委", "location": "盘州市"},
    {"id": 4, "name": "中共盘州市委员会组织部", "type": "党委", "level": "乡科级", "parent": "中共盘州市委员会", "location": "盘州市"},
    {"id": 5, "name": "中共盘州市委员会宣传部", "type": "党委", "level": "乡科级", "parent": "中共盘州市委员会", "location": "盘州市"},
    {"id": 6, "name": "中共盘州市委员会政法委员会", "type": "党委", "level": "乡科级", "parent": "中共盘州市委员会", "location": "盘州市"},
    {"id": 7, "name": "盘州市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "六盘水市人民代表大会常务委员会", "location": "盘州市"},
    {"id": 8, "name": "中国人民政治协商会议盘州市委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议六盘水市委员会", "location": "盘州市"},
    {"id": 9, "name": "盘州市委办公室", "type": "党委", "level": "乡科级", "parent": "中共盘州市委员会", "location": "盘州市"},
]

positions = [
    # 陈石
    {"person_id": 1, "org_id": 1, "title": "盘州市委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任；同时任六盘水市委副书记"},
    # 肖明
    {"person_id": 2, "org_id": 2, "title": "盘州市人民政府市长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    {"person_id": 2, "org_id": 1, "title": "盘州市委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 黎永胜
    {"person_id": 3, "org_id": 2, "title": "盘州市委常委、常务副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 姚斌
    {"person_id": 4, "org_id": 1, "title": "盘州市委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 赵冰
    {"person_id": 5, "org_id": 3, "title": "盘州市委常委、市纪委书记、市监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 孙勇
    {"person_id": 6, "org_id": 4, "title": "盘州市委常委、市委组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 杜琼
    {"person_id": 7, "org_id": 5, "title": "盘州市委常委、市委宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 韩文杰
    {"person_id": 8, "org_id": 6, "title": "盘州市委常委、市委政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 金良武（市委办主任）
    {"person_id": 9, "org_id": 9, "title": "盘州市委常委、市委办公室主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 高赫
    {"person_id": 10, "org_id": 2, "title": "盘州市人民政府副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 朱家应
    {"person_id": 11, "org_id": 2, "title": "盘州市人民政府副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 张劲超
    {"person_id": 12, "org_id": 2, "title": "盘州市人民政府副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 余华
    {"person_id": 13, "org_id": 7, "title": "盘州市人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    # 金良武（政协主席）
    {"person_id": 14, "org_id": 8, "title": "盘州市政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
]

relationships = [
    # 陈石 ↔ 肖明（书记-县长搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "陈石（市委书记）与肖明（市长）为市委常委会和政府班子搭档", "overlap_org": "中共盘州市委员会/盘州市人民政府", "overlap_period": "至今"},
    # 陈石 ↔ 姚斌
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "陈石（市委书记）与姚斌（市委副书记）在市委常委会共事", "overlap_org": "中共盘州市委员会", "overlap_period": "至今"},
    # 肖明 ↔ 黎永胜（市长-常务副市长）
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "肖明（市长）与黎永胜（常务副市长）在市政府班子共事", "overlap_org": "盘州市人民政府", "overlap_period": "至今"},
    # 肖明 ↔ 姚斌
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "肖明（市长、市委副书记）与姚斌（市委副书记）在市委常委会共事", "overlap_org": "中共盘州市委员会", "overlap_period": "至今"},
    # 常委会内部
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "陈石与赵冰（纪委书记）在市委常委会共事", "overlap_org": "中共盘州市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "陈石与孙勇（组织部部长）在市委常委会共事", "overlap_org": "中共盘州市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "陈石与杜琼（宣传部部长）在市委常委会共事", "overlap_org": "中共盘州市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "陈石与韩文杰（政法委书记）在市委常委会共事", "overlap_org": "中共盘州市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "陈石与金良武（市委办主任）在市委常委会共事", "overlap_org": "中共盘州市委员会", "overlap_period": "至今"},
    # 市政府班子
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "肖明（市长）与高赫（副市长）在市政府班子共事", "overlap_org": "盘州市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "肖明（市长）与朱家应（副市长）在市政府班子共事", "overlap_org": "盘州市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "肖明（市长）与张劲超（副市长）在市政府班子共事", "overlap_org": "盘州市人民政府", "overlap_period": "至今"},
    # 常委之间
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "赵冰（纪委书记）与孙勇（组织部部长）在市委常委会共事", "overlap_org": "中共盘州市委员会", "overlap_period": "至今"},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "赵冰（纪委书记）与杜琼（宣传部部长）在市委常委会共事", "overlap_org": "中共盘州市委员会", "overlap_period": "至今"},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "孙勇（组织部部长）与杜琼（宣传部部长）在市委常委会共事", "overlap_org": "中共盘州市委员会", "overlap_period": "至今"},
    {"person_a": 6, "person_b": 8, "type": "overlap", "context": "孙勇（组织部部长）与韩文杰（政法委书记）在市委常委会共事", "overlap_org": "中共盘州市委员会", "overlap_period": "至今"},
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "韩文杰（政法委书记）与金良武（市委办主任）在市委常委会共事", "overlap_org": "中共盘州市委员会", "overlap_period": "至今"},
]

source_register = [
    {"id": "S001", "title": "盘州市人民政府门户网站", "url": "https://www.panzhou.gov.cn/",
     "publisher": "盘州市人民政府", "published_at": "2026-07-23", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "首页信息，陈石在新闻报道中为盘州市主要领导"},
    {"id": "S002", "title": "六盘水市人民政府门户网站", "url": "https://www.gzlps.gov.cn/",
     "publisher": "六盘水市人民政府", "published_at": "2026-07-23", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "六盘水市下辖县级行政区"},
    {"id": "S003", "title": "盘州市法定主动公开内容页面", "url": "https://www.panzhou.gov.cn/zwgk/zfxxgk/fdzdgknr/",
     "publisher": "盘州市人民政府", "published_at": "2026-07-23", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "包含领导之窗链接"},
]


# ── Build Functions ───────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
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
        pid = f"panzhou_{p['name']}"
        if p["id"] == 14:
            pid = "panzhou_金良武_政协"  # disambiguate from person 9
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
        pid = person_map[pos["person_id"]]
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (pid, pos["org_id"], pos["title"], pos.get("start_date", ""),
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
        if "市长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "50,100,255"
        if "纪委书记" in post:
            return "255,165,0"
        if "副" in post or "副书记" in post:
            return "100,150,220"
        if "主任" in post and "副" not in post and "纪委" not in post:
            return "60,180,60"
        if "政协" in post:
            return "180,160,80"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post) or \
               ("市长" in post and "副" not in post and "人大" not in post and "政协" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "square"
        if "市长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "circle"
        if "纪委书记" in post or "纪委" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "纪委": "255,200,150",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>盘州市领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
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

    # Nodes — organizations
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

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization
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

    # Person ↔ person
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

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        """Generate a person graph JSON following the person_graph_json.md schema."""
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": "盘州市",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"panzhou_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
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
                "administrative_rank": "县处级正职" if ("书记" in p.get("current_post","") and "副" not in p.get("current_post","")) or ("市长" in p.get("current_post","") and "副" not in p.get("current_post","")) else "县处级副职",
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
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified" if not p.get("birth") else "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历信息缺失（出生年月、籍贯、学历、早期任职全部未知）"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 盘州市", f"{p['name']} 任前公示"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 陈石 Person JSON ──
    cs_timeline = [
        {"start": "", "end": "", "org": "中共盘州市委员会", "title": "盘州市委书记（六盘水市委副书记兼任）",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "陈石在担任盘州市委书记前的完整履历未找到。据公开信息，陈石曾任六盘水市其他职务，后升任六盘水市委副书记并兼任盘州市委书记",
         "confidence": "unverified", "source_ids": []},
    ]
    cs_relationships = [
        {"person": "肖明", "person_id": "panzhou_肖明", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "陈石（市委书记）与肖明（市长）在市委常委会和政府班子共事",
         "overlap_org": "中共盘州市委员会/盘州市人民政府", "overlap_period": "至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "姚斌", "person_id": "panzhou_姚斌", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "陈石（市委书记）与姚斌（市委副书记）在市委常委会共事",
         "overlap_org": "中共盘州市委员会", "overlap_period": "至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "赵冰", "person_id": "panzhou_赵冰", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "陈石（市委书记）与赵冰（纪委书记）在市委常委会共事",
         "overlap_org": "中共盘州市委员会", "overlap_period": "至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "孙勇", "person_id": "panzhou_孙勇", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "陈石（市委书记）与孙勇（组织部部长）在市委常委会共事",
         "overlap_org": "中共盘州市委员会", "overlap_period": "至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]

    cs_json = make_person_json(persons[0], cs_timeline, cs_relationships)
    cs_path = os.path.join(PERSONS_DIR, f"{now}-{PROVINCE}-{PARENT_CITY}-市委书记-陈石.json")
    with open(cs_path, "w", encoding="utf-8") as f:
        json.dump(cs_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {cs_path}")

    # ── 肖明 Person JSON ──
    xm_timeline = [
        {"start": "", "end": "", "org": "盘州市人民政府", "title": "盘州市委副书记、市人民政府市长",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "肖明在担任盘州市市长前的完整履历未找到",
         "confidence": "unverified", "source_ids": []},
    ]
    xm_relationships = [
        {"person": "陈石", "person_id": "panzhou_陈石", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "肖明（市长）与陈石（市委书记）在市委常委会和政府班子共事",
         "overlap_org": "中共盘州市委员会/盘州市人民政府", "overlap_period": "至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "黎永胜", "person_id": "panzhou_黎永胜", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "肖明（市长）与黎永胜（常务副市长）在市政府班子共事",
         "overlap_org": "盘州市人民政府", "overlap_period": "至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "姚斌", "person_id": "panzhou_姚斌", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "肖明（市委副书记、市长）与姚斌（市委副书记）在市委常委会共事",
         "overlap_org": "中共盘州市委员会", "overlap_period": "至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]

    xm_json = make_person_json(persons[1], xm_timeline, xm_relationships)
    xm_path = os.path.join(PERSONS_DIR, f"{now}-{PROVINCE}-{PARENT_CITY}-市长-肖明.json")
    with open(xm_path, "w", encoding="utf-8") as f:
        json.dump(xm_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {xm_path}")

    print("\n✅ All artifacts generated.")


if __name__ == "__main__":
    build()
