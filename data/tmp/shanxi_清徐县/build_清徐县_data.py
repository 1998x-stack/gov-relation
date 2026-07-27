#!/usr/bin/env python3
"""
清徐县领导班子工作关系网络 — 数据构建脚本
调查日期: 2026-07-25
信息来源: 清徐县人民政府门户网站 (www.qx.gov.cn) 及公开新闻报道
"""

import sqlite3
import os
from datetime import datetime

SLUG = "清徐县"
TODAY = "2026-07-25"
AS_OF = "2026-07-25"
PROVINCE = "山西省"
CITY = "太原市"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR.endswith("scripts/build"):
    REPO_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
else:
    REPO_ROOT = BASE_DIR
DB_PATH = os.path.join(REPO_ROOT, "data", "database", f"{SLUG}_network.db")
GEXF_PATH = os.path.join(REPO_ROOT, "data", "graph", f"{SLUG}_network.gexf")

# =========================================================================
# Research Data
# =========================================================================

persons = [
    {
        "id": 1,
        "name": "李京京",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年1月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共清徐县委",
        "source": "清徐县政府网 (https://www.qx.gov.cn/zgqxxw/20221215/347110.html)",
        "notes": "二级巡视员"
    },
    {
        "id": 2,
        "name": "李福贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年2月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "清徐县人民政府",
        "source": "清徐县政府网 (https://www.qx.gov.cn/zgqxxw/20221116/347109.html)",
        "notes": "同时兼任清徐经济开发区党工委书记"
    },
    {
        "id": 3,
        "name": "陈晓勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年2月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共清徐县委",
        "source": "清徐县政府网 (https://www.qx.gov.cn/zgqxxw/20260410/30292692.html)",
        "notes": "兼任县直工委书记,三级调研员"
    },
    {
        "id": 4,
        "name": "董笑龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年3月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "清徐县人民政府",
        "source": "清徐县政府网 (https://www.qx.gov.cn/zgqxxw/20220615/1035797.html)",
        "notes": "县政府党组副书记, 三级调研员, 常务副县长"
    },
    {
        "id": 5,
        "name": "杨红梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年12月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共清徐县委组织部",
        "source": "清徐县政府网 (https://www.qx.gov.cn/zgqxxw/20220413/1245525.html)",
        "notes": ""
    },
    {
        "id": 6,
        "name": "任功",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记",
        "current_org": "中共清徐县纪委",
        "source": "清徐县政府网 (https://www.qx.gov.cn/zgqxxw/20220713/347108.html)",
        "notes": "兼任县监委主任, 三级调研员"
    },
    {
        "id": 7,
        "name": "牛建忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府党组成员",
        "current_org": "清徐县人民政府",
        "source": "清徐县政府网 (https://www.qx.gov.cn/zgqxxw/20260609/30308724.html)",
        "notes": "三级调研员"
    },
    {
        "id": 8,
        "name": "马峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共清徐县委宣传部",
        "source": "清徐县政府网 (https://www.qx.gov.cn/zgqxxw/20260609/30303021.html)",
        "notes": ""
    },
    {
        "id": 9,
        "name": "智建凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共清徐县委统战部",
        "source": "清徐县政府网 (https://www.qx.gov.cn/zgqxxw/20260703/30307614.html)",
        "notes": ""
    },
    {
        "id": 10,
        "name": "王为民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共清徐县委政法委",
        "source": "清徐县政府网 (https://www.qx.gov.cn/zgqxxw/20220120/347104.html)",
        "notes": ""
    },
    {
        "id": 11,
        "name": "张智强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、人武部上校部长",
        "current_org": "清徐县人民武装部",
        "source": "清徐县政府网 (https://www.qx.gov.cn/zgqxxw/20200411/347105.html)",
        "notes": ""
    },
    {
        "id": 12,
        "name": "杨鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "清徐县人民政府",
        "source": "清徐县政府网 (https://www.qx.gov.cn/zgqxxw/20250815/30247804.html)",
        "notes": "挂职干部"
    },
    {
        "id": 13,
        "name": "陈亚琳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年8月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "清徐县人民政府",
        "source": "清徐县政府网 (https://www.qx.gov.cn/qxxzf/20210812/1041799.html)",
        "notes": "县政府党组成员"
    },
    {
        "id": 14,
        "name": "李华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年10月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "清徐县人民政府",
        "source": "清徐县政府网 (https://www.qx.gov.cn/qxxzf/20260522/30299775.html)",
        "notes": "县政府党组成员, 兼任县委办公室主任"
    },
    {
        "id": 15,
        "name": "张弛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年11月",
        "birthplace": "",
        "education": "在职大专",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "清徐县人民政府",
        "source": "清徐县政府网 (https://www.qx.gov.cn/qxxzf/20260522/30299776.html)",
        "notes": "县政府党组成员, 兼任县公安局党委书记、局长、督察长"
    },
    {
        "id": 16,
        "name": "张晋涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "人大常委会主任",
        "current_org": "清徐县人大",
        "source": "清徐县政府网 (https://www.qx.gov.cn/qxxrd/20221214/347116.html)",
        "notes": ""
    },
    {
        "id": 17,
        "name": "邢蕴武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政协主席",
        "current_org": "清徐县政协",
        "source": "清徐县政府网 (https://www.qx.gov.cn/qxxzx/20221214/347136.html)",
        "notes": ""
    },
]

organizations = [
    {"id": 1, "name": "中共清徐县委", "type": "党委", "level": "县级", "parent": "中共太原市委", "location": "清徐县"},
    {"id": 2, "name": "清徐县人民政府", "type": "政府", "level": "县级", "parent": "太原市人民政府", "location": "清徐县"},
    {"id": 3, "name": "清徐县人大", "type": "人大", "level": "县级", "parent": "太原市人大", "location": "清徐县"},
    {"id": 4, "name": "清徐县政协", "type": "政协", "level": "县级", "parent": "太原市政协", "location": "清徐县"},
    {"id": 5, "name": "中共清徐县委组织部", "type": "党委", "level": "县级", "parent": "中共清徐县委", "location": "清徐县"},
    {"id": 6, "name": "中共清徐县纪委", "type": "党委", "level": "县级", "parent": "中共清徐县委", "location": "清徐县"},
    {"id": 7, "name": "中共清徐县委宣传部", "type": "党委", "level": "县级", "parent": "中共清徐县委", "location": "清徐县"},
    {"id": 8, "name": "中共清徐县委统战部", "type": "党委", "level": "县级", "parent": "中共清徐县委", "location": "清徐县"},
    {"id": 9, "name": "中共清徐县委政法委", "type": "党委", "level": "县级", "parent": "中共清徐县委", "location": "清徐县"},
    {"id": 10, "name": "清徐县人民武装部", "type": "政府", "level": "县级", "parent": "太原警备区", "location": "清徐县"},
    {"id": 11, "name": "清徐经济开发区", "type": "政府", "level": "省级", "parent": "清徐县人民政府", "location": "清徐县"},
    {"id": 12, "name": "清徐县公安局", "type": "政府", "level": "县级", "parent": "清徐县人民政府", "location": "清徐县"},
]

positions = [
    {"person_id": "p1", "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "二级巡视员"},
    {"person_id": "p2", "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "县政府党组书记"},
    {"person_id": "p2", "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p2", "org_id": 11, "title": "清徐经济开发区党工委书记", "start": "", "end": "present", "rank": "正处级", "note": "兼任"},
    {"person_id": "p3", "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "兼任县直工委书记, 三级调研员"},
    {"person_id": "p4", "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组副书记, 三级调研员, 常务副县长"},
    {"person_id": "p4", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p5", "org_id": 5, "title": "县委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p5", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p6", "org_id": 6, "title": "县委常委、纪委书记", "start": "", "end": "present", "rank": "副处级", "note": "兼任县监委主任, 三级调研员"},
    {"person_id": "p6", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p7", "org_id": 2, "title": "县委常委、县政府党组成员", "start": "", "end": "present", "rank": "副处级", "note": "三级调研员"},
    {"person_id": "p7", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p8", "org_id": 7, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p8", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p9", "org_id": 8, "title": "县委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p9", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p10", "org_id": 9, "title": "县委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p10", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p11", "org_id": 10, "title": "县委常委、人武部上校部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p11", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p12", "org_id": 2, "title": "县委常委、副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "挂职干部"},
    {"person_id": "p12", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p13", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": "p14", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员, 兼任县委办公室主任"},
    {"person_id": "p15", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员, 兼任县公安局党委书记、局长、督察长"},
    {"person_id": "p15", "org_id": 12, "title": "县公安局党委书记、局长", "start": "", "end": "present", "rank": "副处级", "note": "督察长兼任"},
    {"person_id": "p16", "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p17", "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

relationships = [
    {
        "person_a": "p1", "person_b": "p2",
        "type": "党政一把手搭档",
        "context": "李京京（县委书记）与李福贵（县长）构成清徐县党政主要领导搭档",
        "overlap_org": "清徐县",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p1", "person_b": "p3",
        "type": "上下级",
        "context": "李京京（县委书记）与陈晓勇（县委副书记）为县委正副书记关系",
        "overlap_org": "中共清徐县委",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p2", "person_b": "p4",
        "type": "上下级",
        "context": "李福贵（县长）与董笑龙（常务副县长）为正副职领导关系",
        "overlap_org": "清徐县人民政府",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p5", "person_b": "p1",
        "type": "上下级",
        "context": "杨红梅（组织部部长）在县委常委会中向县委书记李京京汇报",
        "overlap_org": "中共清徐县委",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p6", "person_b": "p1",
        "type": "上下级",
        "context": "任功（纪委书记）在县委常委会中向县委书记李京京汇报",
        "overlap_org": "中共清徐县委",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p4", "person_b": "p7",
        "type": "同级",
        "context": "董笑龙与牛建忠同为县政府领导班子成员",
        "overlap_org": "清徐县人民政府",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p4", "person_b": "p13",
        "type": "上下级",
        "context": "董笑龙（常务副县长）与陈亚琳（副县长）为正副职关系",
        "overlap_org": "清徐县人民政府",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p8", "person_b": "p9",
        "type": "同级",
        "context": "马峰（宣传部部长）与智建凯（统战部部长）同为县委常委会成员",
        "overlap_org": "中共清徐县委",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p10", "person_b": "p15",
        "type": "上下级",
        "context": "王为民（政法委书记）与张弛（公安局局长）在政法系统为领导与被领导关系",
        "overlap_org": "清徐县政法系统",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p15", "person_b": "p2",
        "type": "上下级",
        "context": "张弛（副县长兼公安局长）向县长李福贵汇报",
        "overlap_org": "清徐县人民政府",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p14", "person_b": "p1",
        "type": "上下级",
        "context": "李华（副县长兼县委办公室主任）直接向县委书记李京京服务",
        "overlap_org": "中共清徐县委",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
]


# =========================================================================
# Build
# =========================================================================

def build():
    """Run database + GEXF build."""
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
        if "县委书记" in post and "副" not in post and "挂职" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post and "副" not in post and "挂职" not in post and "县委副书记" in post:
            return ("50,100,255", 20.0)
        elif "县委副书记" in post:
            return ("50,100,255", 15.0)
        elif "纪委" in post:
            return ("255,165,0", 12.0)
        elif "常委" in post and "副" in post:
            return ("100,150,255", 12.0)
        elif "常委" in post:
            return ("100,150,255", 12.0)
        elif "副" in post and "县长" in post:
            return ("100,100,255", 12.0)
        elif "人大" in post:
            return ("200,255,255", 12.0)
        elif "政协" in post:
            return ("255,240,200", 12.0)
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
        "乡镇": ("255,255,200", 8.0),
        "事业单位": ("220,220,220", 8.0),
        "群团": ("255,220,255", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>清徐县领导班子工作关系网络 - {AS_OF}</description>')
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
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
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
    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        pid_val = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
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
    print(f"清徐县 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
