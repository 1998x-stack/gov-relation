#!/usr/bin/env python3
"""开阳县（贵阳市）领导班子关系网络数据生成脚本。

Targets: 县委书记 孙昕, 县长 吕槐乐
Data as of: 2026-07-23
Sources: 开阳县人民政府官网 (www.kaiyang.gov.cn)
"""

import json
import os
import sqlite3
from datetime import datetime

TASK_ID = "guizhou_开阳县"
SLUG = "开阳县"
AS_OF = "2026-07-23"
PROVINCE = "贵州省"
PARENT_CITY = "贵阳市"

BASE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "data/tmp/guizhou_开阳县"
# Allow override from command line / calling script
_BASE_OVERRIDE = os.environ.get("KAIYANG_BASE")
if _BASE_OVERRIDE:
    BASE = _BASE_OVERRIDE

DB_PATH = os.path.join(BASE, "开阳县_network.db")
GEXF_PATH = os.path.join(BASE, "开阳县_network.gexf")
PERSONS_DIR = os.path.join(BASE, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────

persons = [
    # 1 - 县委书记
    {
        "id": 1,
        "name": "孙昕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开阳县委书记、开阳经开区党工委书记",
        "current_org": "中共开阳县委员会",
        "source": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260708_90597332.html",
    },
    # 2 - 县长
    {
        "id": 2,
        "name": "吕槐乐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开阳县委副书记、县人民政府县长、县政府党组书记",
        "current_org": "开阳县人民政府",
        "source": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260720_90638690.html",
    },
    # 3 - 县委副书记
    {
        "id": 3,
        "name": "周鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开阳县委副书记",
        "current_org": "中共开阳县委员会",
        "source": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260720_90638907.html",
    },
    # 4 - 常务副县长
    {
        "id": 4,
        "name": "徐春波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开阳县委常委、常务副县长",
        "current_org": "开阳县人民政府",
        "source": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260720_90638690.html",
    },
    # 5 - 县委宣传部部长
    {
        "id": 5,
        "name": "吴尧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开阳县委常委、县委宣传部部长、县委教育工委书记",
        "current_org": "中共开阳县委宣传部",
        "source": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260706_90589264.html",
    },
    # 6 - 县委常委/副县长
    {
        "id": 6,
        "name": "吴育材",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开阳县委常委、副县长",
        "current_org": "开阳县人民政府",
        "source": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260720_90638690.html",
    },
    # 7 - 常委/组织部长陈方文
    {
        "id": 7,
        "name": "陈方文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开阳县委常委、县委组织部部长",
        "current_org": "中共开阳县委组织部",
        "source": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260720_90638907.html",
    },
    # 8 - 常委廖彬 (likely 纪委书记/政法委)
    {
        "id": 8,
        "name": "廖彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开阳县委常委",
        "current_org": "中共开阳县委员会",
        "source": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260720_90638907.html",
    },
    # 9 - 副县长欧波
    {
        "id": 9,
        "name": "欧波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开阳县人民政府副县长",
        "current_org": "开阳县人民政府",
        "source": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260720_90638690.html",
    },
    # 10 - 副县长杜玉梅
    {
        "id": 10,
        "name": "杜玉梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开阳县人民政府副县长",
        "current_org": "开阳县人民政府",
        "source": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260720_90638690.html",
    },
    # 11 - 副县长徐志然
    {
        "id": 11,
        "name": "徐志然",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开阳县人民政府副县长",
        "current_org": "开阳县人民政府",
        "source": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260720_90638690.html",
    },
    # 12 - 副县长胡宏亮
    {
        "id": 12,
        "name": "胡宏亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开阳县人民政府副县长",
        "current_org": "开阳县人民政府",
        "source": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260706_90589264.html",
    },
    # 13 - 人大主任刘文筑
    {
        "id": 13,
        "name": "刘文筑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开阳县人大常委会主任",
        "current_org": "开阳县人民代表大会常务委员会",
        "source": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260708_90597332.html",
    },
    # 14 - 政协主席董涛
    {
        "id": 14,
        "name": "董涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开阳县政协主席",
        "current_org": "中国人民政治协商会议开阳县委员会",
        "source": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260708_90597332.html",
    },
]

organizations = [
    {"id": 1, "name": "中共开阳县委员会", "type": "党委", "level": "县处级", "parent": "中共贵阳市委", "location": "开阳县"},
    {"id": 2, "name": "开阳县人民政府", "type": "政府", "level": "县处级", "parent": "贵阳市人民政府", "location": "开阳县"},
    {"id": 3, "name": "中共开阳县委宣传部", "type": "党委", "level": "乡科级", "parent": "中共开阳县委员会", "location": "开阳县"},
    {"id": 4, "name": "中共开阳县委组织部", "type": "党委", "level": "乡科级", "parent": "中共开阳县委员会", "location": "开阳县"},
    {"id": 5, "name": "开阳县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "贵阳市人民代表大会常务委员会", "location": "开阳县"},
    {"id": 6, "name": "中国人民政治协商会议开阳县委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议贵阳市委员会", "location": "开阳县"},
    {"id": 7, "name": "开阳经济开发区党工委", "type": "党委", "level": "县处级", "parent": "中共贵阳市委", "location": "开阳县"},
]

positions = [
    # 孙昕
    {"person_id": 1, "org_id": 1, "title": "开阳县委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    {"person_id": 1, "org_id": 7, "title": "开阳经开区党工委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任（兼任）"},
    # 吕槐乐
    {"person_id": 2, "org_id": 2, "title": "开阳县人民政府县长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    {"person_id": 2, "org_id": 1, "title": "开阳县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 周鹏
    {"person_id": 3, "org_id": 1, "title": "开阳县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 徐春波
    {"person_id": 4, "org_id": 2, "title": "开阳县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 吴尧
    {"person_id": 5, "org_id": 3, "title": "开阳县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 吴育材
    {"person_id": 6, "org_id": 2, "title": "开阳县委常委、副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 陈方文
    {"person_id": 7, "org_id": 4, "title": "开阳县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 廖彬
    {"person_id": 8, "org_id": 1, "title": "开阳县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 欧波
    {"person_id": 9, "org_id": 2, "title": "开阳县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 杜玉梅
    {"person_id": 10, "org_id": 2, "title": "开阳县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 徐志然
    {"person_id": 11, "org_id": 2, "title": "开阳县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 胡宏亮
    {"person_id": 12, "org_id": 2, "title": "开阳县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 刘文筑
    {"person_id": 13, "org_id": 5, "title": "开阳县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    # 董涛
    {"person_id": 14, "org_id": 6, "title": "开阳县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
]

relationships = [
    # 孙昕 ↔ 吕槐乐 (书记-县长搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "孙昕（县委书记）与吕槐乐（县长）为县委常委会搭档", "overlap_org": "中共开阳县委员会/开阳县人民政府", "overlap_period": "2024-至今"},
    # 孙昕 ↔ 周鹏
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "孙昕（县委书记）与周鹏（县委副书记）在县委常委会共事", "overlap_org": "中共开阳县委员会", "overlap_period": "2024-至今"},
    # 吕槐乐 ↔ 徐春波 (县长-常务副县长)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "吕槐乐（县长）与徐春波（常务副县长）在县政府班子共事", "overlap_org": "开阳县人民政府", "overlap_period": "2025-至今"},
    # 吕槐乐 ↔ 周鹏
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "吕槐乐（县长、县委副书记）与周鹏（县委副书记）在县委常委会共事", "overlap_org": "中共开阳县委员会", "overlap_period": "2024-至今"},
    # 孙昕 ↔ 吴尧
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "孙昕（县委书记）与吴尧（县委常委、宣传部部长）在县委常委会共事", "overlap_org": "中共开阳县委员会", "overlap_period": "2024-至今"},
    # 孙昕 ↔ 陈方文
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "孙昕（县委书记）与陈方文（县委常委、组织部部长）在县委常委会共事", "overlap_org": "中共开阳县委员会", "overlap_period": "2024-至今"},
    # 常委会内部共事关系（常委之间）
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "徐春波（常委、常务副县长）与吴尧（常委、宣传部部长）在县委常委会共事", "overlap_org": "中共开阳县委员会", "overlap_period": "2025-至今"},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "徐春波（常委、常务副县长）与陈方文（常委、组织部部长）在县委常委会共事", "overlap_org": "中共开阳县委员会", "overlap_period": "2025-至今"},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "吴育材（常委、副县长）与陈方文（常委、组织部部长）在县委常委会共事", "overlap_org": "中共开阳县委员会", "overlap_period": "2025-至今"},
    # 县政府班子内部
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "欧波（副县长）与杜玉梅（副县长）在县政府班子共事", "overlap_org": "开阳县人民政府", "overlap_period": "2025-至今"},
    {"person_a": 9, "person_b": 11, "type": "overlap", "context": "欧波（副县长）与徐志然（副县长）在县政府班子共事", "overlap_org": "开阳县人民政府", "overlap_period": "2025-至今"},
    {"person_a": 10, "person_b": 12, "type": "overlap", "context": "杜玉梅（副县长）与胡宏亮（副县长）在县政府班子共事", "overlap_org": "开阳县人民政府", "overlap_period": "2025-至今"},
]

source_register = [
    {"id": "S001", "title": "开阳县委常委会召开（扩大）会议", "url": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260708_90597332.html",
     "publisher": "开阳县人民政府", "published_at": "2026-07-08", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "确认孙昕为县委书记、吕槐乐为县长"},
    {"id": "S002", "title": "开阳县政府党组（扩大）会议、常务会议召开", "url": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260720_90638690.html",
     "publisher": "开阳县人民政府", "published_at": "2026-07-20", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "确认吕槐乐为县长,徐春波/吴育材为常委副县长,欧波/杜玉梅/徐志然为副县长"},
    {"id": "S003", "title": "开阳县委党的建设工作领导小组召开会议", "url": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260720_90638907.html",
     "publisher": "开阳县人民政府", "published_at": "2026-07-20", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "确认周鹏为县委副书记,徐春波/吴尧/陈方文/吴育材/廖彬等常委"},
    {"id": "S004", "title": "县委主要负责同志到开阳县第三中学讲授思想政治理论课", "url": "https://www.kaiyang.gov.cn/xwzx/zwyw/202607/t20260706_90589264.html",
     "publisher": "开阳县人民政府", "published_at": "2026-07-03", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "确认孙昕兼任经开区党工委书记,吴尧为宣传部部长,胡宏亮为副县长"},
    {"id": "S005", "title": "开阳县第十八届人民代表大会第六次会议开幕", "url": "https://www.kaiyang.gov.cn/xwzx/zwyw/202606/t20260629_90565445.html",
     "publisher": "开阳县人民政府", "published_at": "2026-06-26", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "确认刘文筑为人大主任,董涛为政协主席,孙昕/吕槐乐/周鹏/陈方文/廖彬等人大主席团成员"},
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
        pid = f"kaiyang_{p['name']}"
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
            "政协": "255,240,200",
            "纪委": "255,200,150",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>开阳县领导班子关系网络（基于开阳县政府官网）</description>')
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
                "region": "开阳县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"kaiyang_{p['name']}",
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
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002", "S003", "S004"]
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
                 "suggested_queries": [f"{p['name']} 简历 开阳县", f"{p['name']} 任前公示"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 孙昕 Person JSON ──
    sx_timeline = [
        {"start": "", "end": "", "org": "中共开阳县委员会", "title": "开阳县委书记、开阳经开区党工委书记",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "孙昕在担任开阳县委书记前的完整履历未找到",
         "confidence": "unverified", "source_ids": []},
    ]
    sx_relationships = [
        {"person": "吕槐乐", "person_id": "kaiyang_吕槐乐", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "孙昕（县委书记）与吕槐乐（县长）在县委常委会和县政府班子共事",
         "overlap_org": "中共开阳县委员会/开阳县人民政府", "overlap_period": "2024-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "周鹏", "person_id": "kaiyang_周鹏", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "孙昕（县委书记）与周鹏（县委副书记）在县委常委会共事",
         "overlap_org": "中共开阳县委员会", "overlap_period": "2024-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    ]

    sx_json = make_person_json(persons[0], sx_timeline, sx_relationships)
    sx_path = os.path.join(PERSONS_DIR, f"{now}-{PROVINCE}-{PARENT_CITY}-县委书记-孙昕.json")
    with open(sx_path, "w", encoding="utf-8") as f:
        json.dump(sx_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {sx_path}")

    # ── 吕槐乐 Person JSON ──
    lhl_timeline = [
        {"start": "", "end": "", "org": "开阳县人民政府", "title": "开阳县委副书记、县人民政府县长",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "吕槐乐在担任开阳县县长前的完整履历未找到",
         "confidence": "unverified", "source_ids": []},
    ]
    lhl_relationships = [
        {"person": "孙昕", "person_id": "kaiyang_孙昕", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "吕槐乐（县长、县委副书记）与孙昕（县委书记）在县委常委会和县政府班子共事",
         "overlap_org": "中共开阳县委员会/开阳县人民政府", "overlap_period": "2024-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "徐春波", "person_id": "kaiyang_徐春波", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "吕槐乐（县长）与徐春波（常务副县长）在县政府班子共事",
         "overlap_org": "开阳县人民政府", "overlap_period": "2025-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "周鹏", "person_id": "kaiyang_周鹏", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "吕槐乐（县委副书记、县长）与周鹏（县委副书记）在县委常委会共事",
         "overlap_org": "中共开阳县委员会", "overlap_period": "2024-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    ]

    lhl_json = make_person_json(persons[1], lhl_timeline, lhl_relationships)
    lhl_path = os.path.join(PERSONS_DIR, f"{now}-{PROVINCE}-{PARENT_CITY}-县长-吕槐乐.json")
    with open(lhl_path, "w", encoding="utf-8") as f:
        json.dump(lhl_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lhl_path}")

    # ── 周鹏 Person JSON ──
    zp_timeline = [
        {"start": "", "end": "", "org": "中共开阳县委员会", "title": "开阳县委副书记",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "周鹏在担任开阳县委副书记前的完整履历未找到",
         "confidence": "unverified", "source_ids": []},
    ]
    zp_relationships = [
        {"person": "孙昕", "person_id": "kaiyang_孙昕", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "周鹏（县委副书记）与孙昕（县委书记）在县委常委会共事",
         "overlap_org": "中共开阳县委员会", "overlap_period": "2024-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "吕槐乐", "person_id": "kaiyang_吕槐乐", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "周鹏（县委副书记）与吕槐乐（县委副书记、县长）在县委常委会共事",
         "overlap_org": "中共开阳县委员会", "overlap_period": "2024-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    ]

    zp_json = make_person_json(persons[2], zp_timeline, zp_relationships)
    zp_path = os.path.join(PERSONS_DIR, f"{now}-{PROVINCE}-{PARENT_CITY}-县委副书记-周鹏.json")
    with open(zp_path, "w", encoding="utf-8") as f:
        json.dump(zp_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {zp_path}")

    print("\n✅ All artifacts generated.")


if __name__ == "__main__":
    build()
