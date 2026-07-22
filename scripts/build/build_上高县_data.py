#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 上高县 leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/jiangxi_上高县")
DB_PATH = os.path.join(TMP, "上高县_network.db")
GEXF_PATH = os.path.join(TMP, "上高县_network.gexf")

os.makedirs(TMP, exist_ok=True)

# ── DATA ─────────────────────────────────────────────────────────────
# Sources:
# - shanggao.gov.cn 政府领导分工 (2022-09-26): 上府字〔2022〕32号
# - shanggao.gov.cn 政务动态 articles (2026-06 to 2026-07)
# - baike.baidu.com 陈爱红 (multi-entry, "江西省宜春市上高县委书记" confirmed)
# - baike.baidu.com 文浪 (multi-entry, "上高县委副书记、县政府县长提名人选" confirmed)
# - shanggao.gov.cn articles: 金彪调研 (2026-06-17, 2026-06-25, 2026-06-26, 2026-06-29)
# - shanggao.gov.cn: 七一表彰大会 (2026-06-29, 金彪以县委书记身份出席)
# - shanggao.gov.cn: 陈爱红、文浪走访老同志 (2026-07-02, 陈爱红以县委书记、文浪以县长提名人选身份)
# - shanggao.gov.cn: 陈爱红调研 (2026-07-08, 陈爱红以县委书记身份)

persons = [
    # ── Current Party Secretary (现任县委书记) ──
    {"id": 1, "name": "陈爱红", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共上高县委书记", "current_org": "中共上高县委员会",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2075019778716442624/content_2075019778716442624.html"},
    
    # ── Current County Mayor Nominee (现任县长提名人选) ──
    {"id": 2, "name": "文浪", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "上高县委副书记、县政府县长提名人选", "current_org": "上高县人民政府",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2072942467590496256/content_2072942467590496256.html"},
    
    # ── Previous Party Secretary (前任县委书记) ──
    {"id": 3, "name": "金彪", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2067041640887705600/content_2067041640887705600.html"},

    # ── Deputy Party Secretary (县委副书记) ──
    {"id": 4, "name": "李微", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "上高县委副书记", "current_org": "中共上高县委员会",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2070433873884192768/content_2070433873884192768.html"},

    # ── Organization Department Head (县委常委、组织部部长) ──
    {"id": 5, "name": "徐芳", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "上高县委常委、组织部部长", "current_org": "中共上高县委员会",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2072942467590496256/content_2072942467590496256.html"},

    # ── County Leaders (县领导) from recent articles ──
    {"id": 6, "name": "梁辉", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2075019778716442624/content_2075019778716442624.html"},

    {"id": 7, "name": "严雪如", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "上高县人民政府党组成员、副县长", "current_org": "上高县人民政府",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2075019778716442624/content_2075019778716442624.html"},

    {"id": 8, "name": "冷功勋", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2075019778716442624/content_2075019778716442624.html"},

    {"id": 9, "name": "樊亮亮", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2075019778716442624/content_2075019778716442624.html"},

    {"id": 10, "name": "章自力", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2070395806129430528/content_2070395806129430528.html"},

    {"id": 11, "name": "冷国华", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2070395806129430528/content_2070395806129430528.html"},

    {"id": 12, "name": "冷水清", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2067041640887705600/content_2067041640887705600.html"},

    {"id": 13, "name": "邓志刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "上高县人民政府党组成员、副县长", "current_org": "上高县人民政府",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2067041640887705600/content_2067041640887705600.html"},

    {"id": 14, "name": "王闰春", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2072863259803623424/content_2072863259803623424.html"},

    {"id": 15, "name": "黄锐琴", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zwdt/pc/content/2072863259803623424/content_2072863259803623424.html"},

    # ── Predecessor government leaders (2022 team, from 上府字〔2022〕32号) ──
    {"id": 16, "name": "刘战平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zcwj/pc/content/2036071847670161408/content_2036071847670161408.html"},

    {"id": 17, "name": "胡贵明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zcwj/pc/content/2036071847670161408/content_2036071847670161408.html"},

    {"id": 18, "name": "王萍", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zcwj/pc/content/2036071847670161408/content_2036071847670161408.html"},

    {"id": 19, "name": "汪晓艳", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zcwj/pc/content/2036071847670161408/content_2036071847670161408.html"},

    {"id": 20, "name": "卢友华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zcwj/pc/content/2036071847670161408/content_2036071847670161408.html"},

    {"id": 21, "name": "张鲛", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.shanggao.gov.cn/sgxrmzf/zcwj/pc/content/2036071847670161408/content_2036071847670161408.html"},
]

organizations = [
    {"id": 1, "name": "中共上高县委员会", "type": "党委", "level": "县处级", "parent": "中共宜春市委员会", "location": "江西宜春上高"},
    {"id": 2, "name": "上高县人民政府", "type": "政府", "level": "县处级", "parent": "宜春市人民政府", "location": "江西宜春上高"},
    {"id": 3, "name": "中共上高县委组织部", "type": "党委部门", "level": "县处级", "parent": "中共上高县委员会", "location": "江西宜春上高"},
]

positions = [
    # ── 陈爱红 career ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共上高县委书记", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "现任; 2026年7月起任县委书记"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "上高县人民政府县长", "start": "2022-09", "end": "2026-06", "rank": "县处级正职", "note": "前任职务; 上府字〔2022〕32号"},
    {"id": 3, "person_id": 1, "org_id": 1, "title": "上高县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ── 文浪 ──
    {"id": 4, "person_id": 2, "org_id": 2, "title": "上高县人民政府县长提名人选", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "现任; 2026年7月起任"},
    {"id": 5, "person_id": 2, "org_id": 1, "title": "上高县委副书记", "start": "2026-07", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── 金彪 ──
    {"id": 6, "person_id": 3, "org_id": 1, "title": "中共上高县委书记", "start": "", "end": "2026-06", "rank": "县处级正职", "note": "2026年6月底前离任"},
    {"id": 7, "person_id": 3, "org_id": 1, "title": "上高县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ── 李微 ──
    {"id": 8, "person_id": 4, "org_id": 1, "title": "上高县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── 徐芳 ──
    {"id": 9, "person_id": 5, "org_id": 3, "title": "上高县委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── 严雪如 (2022 副县长, still active 2026) ──
    {"id": 10, "person_id": 7, "org_id": 2, "title": "上高县人民政府党组成员、副县长", "start": "2022-09", "end": "", "rank": "县处级副职", "note": "分管住房城乡建设、人防、自然资源、城管、交通运输"},
    {"id": 11, "person_id": 7, "org_id": 2, "title": "上高县人民政府副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ── 邓志刚 (2022 副县长, still active 2026) ──
    {"id": 12, "person_id": 13, "org_id": 2, "title": "上高县人民政府党组成员、副县长", "start": "2022-09", "end": "", "rank": "县处级副职", "note": "分管公安、司法"},

    # ── 刘战平 (2022 常务副县长) ──
    {"id": 13, "person_id": 16, "org_id": 2, "title": "上高县人民政府党组副书记、副县长", "start": "2022-09", "end": "", "rank": "县处级副职", "note": "常务副县长, 分管政府常务工作"},
    {"id": 14, "person_id": 16, "org_id": 1, "title": "上高县人民政府党组副书记", "start": "", "end": "", "rank": "", "note": ""},

    # ── 胡贵明 ──
    {"id": 15, "person_id": 17, "org_id": 2, "title": "上高县人民政府党组成员、副县长", "start": "2022-09", "end": "", "rank": "县处级副职", "note": "分管工业、数字经济、生态环境"},
    
    # ── 王萍 (非中共党员) ──
    {"id": 16, "person_id": 18, "org_id": 2, "title": "上高县人民政府副县长", "start": "2022-09", "end": "", "rank": "县处级副职", "note": "分管开放型经济、商务、文化旅游"},
    
    # ── 汪晓艳 ──
    {"id": 17, "person_id": 19, "org_id": 2, "title": "上高县人民政府党组成员、副县长", "start": "2022-09", "end": "", "rank": "县处级副职", "note": "分管水利、农业农村、林业、乡村振兴"},
    
    # ── 卢友华 ──
    {"id": 18, "person_id": 20, "org_id": 2, "title": "上高县人民政府党组成员、副县长", "start": "2022-09", "end": "", "rank": "县处级副职", "note": "分管教育体育、卫生健康、民政、医疗保障、科技"},
    
    # ── 张鲛 ──
    {"id": 19, "person_id": 21, "org_id": 2, "title": "上高县人民政府一级调研员", "start": "2022-09", "end": "", "rank": "县处级", "note": "协助负责卫生健康、医疗保障"},
]

relationships = [
    # ── Predecessor-Successor ──
    {"id": 1, "person_a_id": 3, "person_b_id": 1, "type": "交接", "context": "金彪→陈爱红 上高县委书记交接（2026年6月底-7月初）", "overlap_org": "中共上高县委员会", "overlap_period": "2026-06/07"},
    {"id": 2, "person_a_id": 1, "person_b_id": 2, "type": "交接", "context": "陈爱红→文浪 上高县长交接（2026年7月，陈爱红升任县委书记，文浪接县长提名人选）", "overlap_org": "上高县人民政府", "overlap_period": "2026-07"},
    {"id": 3, "person_a_id": 1, "person_b_id": 3, "type": "党政搭档", "context": "金彪任县委书记时，陈爱红任县长（2022-2026年6月）", "overlap_org": "上高县人民政府", "overlap_period": "2022-2026"},

    # ── Current Leadership Team Connections ──
    {"id": 4, "person_a_id": 1, "person_b_id": 4, "type": "上下级", "context": "陈爱红（县委书记）与李微（县委副书记）为上下级关系", "overlap_org": "中共上高县委员会", "overlap_period": "2026"},
    {"id": 5, "person_a_id": 1, "person_b_id": 5, "type": "上下级", "context": "陈爱红（县委书记）与徐芳（县委常委、组织部部长）为上下级关系", "overlap_org": "中共上高县委员会", "overlap_period": "2026"},
    {"id": 6, "person_a_id": 1, "person_b_id": 7, "type": "党政搭档", "context": "陈爱红（县委书记）与严雪如（副县长）在同届班子共事", "overlap_org": "中共上高县委员会", "overlap_period": "2022-2026"},
    {"id": 7, "person_a_id": 1, "person_b_id": 13, "type": "党政搭档", "context": "陈爱红（县长/县委书记）与邓志刚（副县长）在政府班子共事", "overlap_org": "上高县人民政府", "overlap_period": "2022-2026"},
    {"id": 8, "person_a_id": 2, "person_b_id": 4, "type": "同僚", "context": "文浪（县长提名人选）与李微（县委副书记）均为县委副书记", "overlap_org": "中共上高县委员会", "overlap_period": "2026"},

    # ── Old government team connections ──
    {"id": 9, "person_a_id": 1, "person_b_id": 16, "type": "党政搭档", "context": "陈爱红（县长）与刘战平（常务副县长）在政府班子共事", "overlap_org": "上高县人民政府", "overlap_period": "2022-2026"},
    {"id": 10, "person_a_id": 1, "person_b_id": 17, "type": "党政搭档", "context": "陈爱红（县长）与胡贵明（副县长）在政府班子共事", "overlap_org": "上高县人民政府", "overlap_period": "2022-2026"},
    {"id": 11, "person_a_id": 1, "person_b_id": 18, "type": "党政搭档", "context": "陈爱红（县长）与王萍（副县长）在政府班子共事", "overlap_org": "上高县人民政府", "overlap_period": "2022-2026"},
    {"id": 12, "person_a_id": 1, "person_b_id": 19, "type": "党政搭档", "context": "陈爱红（县长）与汪晓艳（副县长）在政府班子共事", "overlap_org": "上高县人民政府", "overlap_period": "2022-2026"},
    {"id": 13, "person_a_id": 1, "person_b_id": 20, "type": "党政搭档", "context": "陈爱红（县长）与卢友华（副县长）在政府班子共事", "overlap_org": "上高县人民政府", "overlap_period": "2022-2026"},

    # ── Current leadership team (县领导) ──
    {"id": 14, "person_a_id": 6, "person_b_id": 7, "type": "同僚", "context": "梁辉与严雪如均为现届县领导", "overlap_org": "中共上高县委员会", "overlap_period": "2026"},
    {"id": 15, "person_a_id": 8, "person_b_id": 9, "type": "同僚", "context": "冷功勋与樊亮亮均为现届县领导", "overlap_org": "中共上高县委员会", "overlap_period": "2026"},
    {"id": 16, "person_a_id": 10, "person_b_id": 11, "type": "同僚", "context": "章自力与冷国华均为县领导", "overlap_org": "中共上高县委员会", "overlap_period": "2026"},
    {"id": 17, "person_a_id": 12, "person_b_id": 13, "type": "同僚", "context": "冷水清与邓志刚一同参加金彪调研活动", "overlap_org": "中共上高县委员会", "overlap_period": "2026-06"},
    {"id": 18, "person_a_id": 14, "person_b_id": 15, "type": "同僚", "context": "王闰春与黄锐琴一同参加会见活动", "overlap_org": "中共上高县委员会", "overlap_period": "2026-07"},

    # ── Cross-team connections ──
    {"id": 19, "person_a_id": 3, "person_b_id": 16, "type": "上下级", "context": "金彪（县委书记）与刘战平（常务副县长）在同一届班子", "overlap_org": "中共上高县委员会", "overlap_period": ""},
    {"id": 20, "person_a_id": 3, "person_b_id": 12, "type": "上下级", "context": "金彪调研时冷水清一同参加", "overlap_org": "中共上高县委员会", "overlap_period": "2026-06"},
]


# ── BUILD SQLite DATABASE ────────────────────────────────────────────

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT,
    ethnicity TEXT,
    birth TEXT,
    birthplace TEXT,
    education TEXT,
    party_join TEXT,
    work_start TEXT,
    current_post TEXT,
    current_org TEXT,
    source TEXT
);

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary stats
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>上高县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    pid = p["id"]
    # Color by role
    if pid == 1:  # Party Secretary (current)
        color_hex = '#E03C31'  # Red
        size = 20.0
    elif pid == 3:  # Party Secretary (former)
        color_hex = '#E03C31'  # Red
        size = 18.0
    elif pid == 2:  # County Mayor (nominee)
        color_hex = '#2980B9'  # Blue
        size = 18.0
    elif pid in [4, 5]:  # Key deputies
        color_hex = '#2980B9'  # Blue
        size = 14.0
    else:
        color_hex = '#95A5A6'  # Grey: others
        size = 12.0

    r_val = int(color_hex[1:3], 16)
    g_val = int(color_hex[3:5], 16)
    b_val = int(color_hex[5:7], 16)

    lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r_val}" g="{g_val}" b="{b_val}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="44" g="62" b="80"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(pos["start"] or "?")} → {esc(pos["end"] or "今")}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r["overlap_period"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
