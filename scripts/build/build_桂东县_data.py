#!/usr/bin/env python3
"""
桂东县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for 桂东县 leadership network.
Investigation date: 2026-08-06
Task: hunan_桂东县 (湖南省 / 郴州市 / 桂东县)

IMPORTANT RESEARCH BASIS:
  - 中国共产党桂东县第十四次代表大会于 2026-07-28~30 召开。
  - 来源: 桂东县融媒体中心 (www.gdxww.cn) 官方报道：
      · 2026-07-30 十四次代表大会第四次全体会议胜利闭幕：蔡富强出席并讲话；
        尹建恒、李攀、龙彪、扶秀娟、李书鸿、杨漾、曹榼、谷新波、郭尚君 在主席台前排就座。
      · 2026-07-31 八一建军节走访慰问：县委书记蔡富强、县委副书记、县长尹建恒。
      · 2026-08-05 蔡富强接访信访群众；县领导郭建军参加。
  - 县第十六届人大五次会议 (2025-12, 桂东人大网) 列名：蔡富强、尹建恒、周国栋、欧凯娟、
    李火雄、郭福星、黄星、罗海燕、唐胜红、郭小诚、陈雄、郭元萍、李富珍、胡飞强、张盛君。
  - 前任县委书记伍志平：2015-12 起任桂东县委副书记、县长；2021 当选县委书记（第十三届）；
    2022-01 后兼任郴州市政协副主席；2025-02 完全转任，现任郴州市政协党组成员、副主席。

Confirmed current leadership (as of 2026-08-06):
    县委书记: 蔡富强 (2026-07/08 多项官方报道确认)
    县委副书记、县长: 尹建恒 (2026-05-30、2026-07-31 确认)
    县委班子(十四届党代会主席台前排就坐): 蔡富强、尹建恒、李攀、龙彪、扶秀娟、李书鸿、
        曹播、谷新波、郭尚君
    县委领导(活动/接访): 李攀、杨漾、张金泽、郭建军
    前任县委书记: 伍志平 (→郴州市政协副主席, 2025-02 后完全转任市政协)
    人大主任 / 政协主席: 待查 (open gap)

开放缺口: 蔡富强、尹建恒 的出生年份、籍贯、完整早年履历尚未从可访问来源确认；
县人大常委会主任、县政协主席人选待确认。均记入 person JSON open_questions 与 report。
"""

import os
import sqlite3
from datetime import datetime

# ── Paths (relative to repo root) ──
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Staging-aware paths — when in data/tmp, write there; otherwise write to canonical locations
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING_CANDIDATE = os.path.join(REPO_ROOT, "data", "tmp", "hunan_桂东县")
if os.path.basename(THIS_DIR) == "hunan_桂东县":
    STAGING_DIR = THIS_DIR
    DB_PATH = os.path.join(STAGING_DIR, "桂东县_network.db")
    GEXF_PATH = os.path.join(STAGING_DIR, "桂东县_network.gexf")
else:
    DB_PATH = os.path.join(REPO_ROOT, "data", "database", "桂东县_network.db")
    GEXF_PATH = os.path.join(REPO_ROOT, "data", "graph", "桂东县_network.gexf")

# ════════════════════════════════════════════════════════════════
# RESEARCH DATA
# ════════════════════════════════════════════════════════════════

PERSONS = [
    # ── 1. 县委书记 ──
    {
        "id": 1,
        "name": "蔡富强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共桂东县委员会",
        "source": "http://www.gdxww.net/content/17561235，17596955 (桂东县融媒体中心)",
        "notes": "2026-07-30 主持县第十四次党代会主席团第六次会议；2026-07-31 以县委书记身份走访慰问；2026-08-05 在县信访接待中心接访。最晚 2025-07 起任县委书记（2025-07-18 主持第13次县委常委会）。此前为郴州本地干部，具体晋升路径待查。",
    },
    # ── 2. 县长 ──
    {
        "id": 2,
        "name": "尹建恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "桂东县人民政府",
        "source": "http://www.gdxww.cn/content/30677335（桂东县融媒体中心），2026-05-30 新湖南专访",
        "notes": "2026-07-31 以'县委副书记、县长'身份走访慰问；2026-05-30 与县委书记蔡富强一同看望少年儿童。2025-07 已是县长。任现职时间、早年履历待查。",
    },
    # ── 县委主要班子 (十四届党代会主席台前排就座) ──
    {
        "id": 3,
        "name": "李攀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委领导",
        "current_org": "中共桂东县委员会",
        "source": "http://www.gdxww.cn/content/30677325（桂东县融媒体中心，十四届四全会主席台前排）",
        "notes": "中国共产党桂东县第十四次代表大会第四次全体会议在主席台前排就座；2026-07-31 走访慰问'县领导'。",
    },
    {
        "id": 4,
        "name": "龙彪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委领导",
        "current_org": "中共桂东县委员会",
        "source": "http://www.gdxww.cn/content/17559525（桂东县融媒体中心）",
        "notes": "2026-07-30 县十四届党代会第四次全体会议在主席台前排就座。",
    },
    {
        "id": 5,
        "name": "扶秀娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委领导",
        "current_org": "中共桂东县委员会",
        "source": "http://www.gdxww.cn/content/17559525（2026-07-30）；湖南红网2021-08 桂东十三届县委名单",
        "notes": "2021（第十三届）当选桂东县委常委，为延续任职的女领导；2026-07-30 十四届党代会仍在主席台前排。",
    },
    {
        "id": 6,
        "name": "李书鸿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委领导",
        "current_org": "中共桂东县委员会",
        "source": "http://www.gdxww.cn/content/17559525（2026-07-30）",
        "notes": "2026-07-30 桂东县第十四次党代会第四次全体会议在主席台前排就座。",
    },
    {
        "id": 7,
        "name": "杨漾",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委领导",
        "current_org": "中共桂东县委员会",
        "source": "http://www.gdxww.cn/content/17561235（2026-07-31）",
        "notes": "2026-07-30 县十四届党代会主席台前排就座；2026-07-31 参与八一走访'县领导'。",
    },
    {
        "id": 8,
        "name": "曹搡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委领导",
        "current_org": "中共桂东县委员会",
        "source": "http://www.gdxww.cn/content/17559525（2026-07-30）",
        "notes": "2026-07-30 县十四届党代会主席台前排就座。",
    },
    {
        "id": 9,
        "name": "谷新波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委领导",
        "current_org": "中共桂东县委员会",
        "source": "http://www.gdxww.cn/content/17559525（2026-07-30）",
        "notes": "2026-07-30 县十四届党代会主席台前排就座。",
    },
    {
        "id": 10,
        "name": "郭尚君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委领导",
        "current_org": "中共桂东县委员会",
        "source": "http://www.gdxww.cn/content/17559525（2026-07-30）",
        "notes": "2026-07-30 县十四届党代会主席台前排就座。",
    },
    # ── 纪委 / 监督 (第十三届) ──
    {
        "id": 11,
        "name": "郭建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "桂东县",
        "source": "http://www.gdxww.cn/content/17596955（2026-08-05）",
        "notes": "2026-08-05 陪同县委书记蔡富强参加信访接访的'县领导'。",
    },
    # ── 前任县委书记 ──
    {
        "id": 12,
        "name": "伍志平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郴州市政协党组成员、副主席",
        "current_org": "政协郴州市委员会",
        "source": "百度百科；桂东县融媒体中心历次报道",
        "notes": "2015-12 至 2022-01 先后任桂东县委副书记、县长；2022 当选第十三届桂东县委书记；2022-08 起兼任郴州市政协副主席；2025-02 完全转任市政协。现任郴州市政协党组成员、副主席。",
    },
    # ── 2021 十三届县委 (前任班子成员，网络参考) ──
    {
        "id": 13,
        "name": "刘真",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记（第十三届）",
        "current_org": "(原)中共桂东县委员会",
        "source": "湖南红网 2021-08 桂东十三届换届选举报道",
        "notes": "2021-08 当选桂东县委副书记（女）。后续去向待查。",
    },
    {
        "id": 14,
        "name": "李仕兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记（第十三届）",
        "current_org": "(原)中共桂东县委员会",
        "source": "郴州市11县市区党委换届选举报道",
        "notes": "2021-08 当选桂东县委副书记。后续去向待查。",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共桂东县委员会", "type": "党委", "level": "县处级", "parent": "中共郴州市委", "location": "湖南省郴州市桂东县"},
    {"id": 2, "name": "桂东县人民政府", "type": "政府", "level": "县处级", "parent": "郴州市人民政府", "location": "湖南省郴州市桂东县"},
    {"id": 3, "name": "桂东县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "郴州市人大常委会", "location": "湖南省郴州市桂东县"},
    {"id": 4, "name": "中国人民政治协商会议桂东县委员会", "type": "政协", "level": "县处级", "parent": "政协郴州市委员会", "location": "湖南省郴州市桂东县"},
    {"id": 5, "name": "中共桂东县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共桂东县委员会", "location": "湖南省郴州市桂东县"},
    {"id": 6, "name": "中共郴州市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "湖南省郴州市"},
    {"id": 7, "name": "郴州市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "湖南省郴州市"},
    {"id": 8, "name": "政协郴州市委员会", "type": "政协", "level": "地市级", "parent": "政协湖南省委员会", "location": "湖南省郴州市"},
]

POSITIONS = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "桂东县委书记", "start": "约2025", "end": "present", "rank": "正处级", "note": "2025-07 已主持常委会；2026-07 第十四届党代会确认"},
    # 县长
    {"person_id": 2, "org_id": 2, "title": "桂东县县长", "start": "", "end": "present", "rank": "正处级", "note": "兼县委副书记，任现职时间待查"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "2026-07 以县委副书记、县长身份活动"},
    # 县委主要班子 (第14届党代会主席台前排)
    {"person_id": 3, "org_id": 1, "title": "县委常委、常务副县长（待证）", "start": "2026-07", "end": "present", "rank": "副处级", "note": "主台前排就坐"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "2021-08", "end": "present", "rank": "副处级", "note": "第十三届当选常委延续"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "副处级", "note": "2026-08-05 陪同接访"},
    # 前任县委书记
    {"person_id": 12, "org_id": 1, "title": "桂东县委书记", "start": "2022-01", "end": "2025", "rank": "正处级", "note": "2022-01 起正式任书记"},
    {"person_id": 12, "org_id": 2, "title": "桂东县人民政府县长", "start": "2015-12", "end": "2022-01", "rank": "正处级", "note": "历任县委副书记、县长"},
    {"person_id": 12, "org_id": 8, "title": "郴州市政协副主席", "start": "2022-08", "end": "present", "rank": "副厅级", "note": "2022-08 起兼任，2025-02 后完全转任"},
    # 第十三届县委
    {"person_id": 13, "org_id": 1, "title": "县委副书记", "start": "2021-08", "end": "2026", "rank": "副处级", "note": "第十三届，女"},
    {"person_id": 14, "org_id": 1, "title": "县委副书记", "start": "2021-08", "end": "2026", "rank": "副处级", "note": "第十三届"},
]

RELATIONSHIPS = [
    # 党政正职 (书记×县长)
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "蔡富强（县委书记）与尹建恒（县委副书记、县长）为桂东县党政一把手搭档，2026年共同主持县十四届党代会并开展走访慰问", "overlap_org": "中共桂东县委员会/桂东县", "overlap_period": "2025至今"},
    # 前任·继任 (伍志平 -> 蔡富强)
    {"person_a": 12, "person_b": 1, "type": "前任继任", "context": "伍志平 2025 卸任桂东县委书记（转任郴州市政协副主席），蔡富强接任桂东县委书记", "overlap_org": "中共桂东县委员会", "overlap_period": "2025"},
    # 上下级：书记×班子
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "李攀等县委班子为县委书记蔡富强掌管的班子成员，2026年党代会主席台同台就座", "overlap_org": "中共桂东县委员会", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "扶秀娟为第十四届县委班子（前身为十三届常委），与蔡富强同属县委常委会", "overlap_org": "中共桂东县委员会", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "杨淛为县委班子，2026-07-30 党代会同台，2026-07-31 共同走访慰问", "overlap_org": "中共桂东县委员会", "overlap_period": "2026至今"},
    # 前任班子：伍志平时代
    {"person_a": 12, "person_b": 13, "type": "上下级", "context": "刘真（女）2021-08 当选县委副书记，伍志平任县委书记", "overlap_org": "中共桂东县委员会", "overlap_period": "2021-2025"},
    {"person_a": 12, "person_b": 14, "type": "上下级", "context": "李仕兵 2021-08 当选县委副书记，伍志平任县委书记", "overlap_org": "中共桂东县委员会", "overlap_period": "2021-2025"},
]

# ════════════════════════════════════════════════════════════════
# DATABASE BUILD
# ════════════════════════════════════════════════════════════════

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    for t in ["relationships", "positions", "organizations", "persons"]:
        conn.execute(f"DROP TABLE IF EXISTS {t}")

    conn.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL,
            gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '', education TEXT DEFAULT '', party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '', current_post TEXT DEFAULT '', current_org TEXT DEFAULT '',
            source TEXT DEFAULT '', notes TEXT DEFAULT ''
        )
    """)
    conn.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
            level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
        )
    """)
    conn.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL, org_id INTEGER NOT NULL, title TEXT DEFAULT '',
            start_date TEXT DEFAULT '', end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    conn.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL, person_b INTEGER NOT NULL, type TEXT DEFAULT '',
            context TEXT DEFAULT '', overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace", "education",
              "party_join", "work_start", "current_post", "current_org", "source", "notes"]
    for p in PERSONS:
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})",
                     [p.get(c, "") for c in cols_p])

    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in ORGANIZATIONS:
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})",
                     [o.get(c, "") for c in cols_o])

    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in POSITIONS:
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})",
                     [pos.get(c, "") for c in cols_pos])

    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in RELATIONSHIPS:
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})",
                     [r.get(c, "") for c in cols_r])

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ════════════════════════════════════════════════════════════════
# GEXF BUILD
# ════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(title):
    t = title
    if "县委书记" in t or (t.startswith("县委") and "书记" in t):
        return "255,50,50"
    if "县长" in t and "副" not in t:
        return "50,100,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "纪委" in t:
        return "255,165,0"
    if "副书记" in t:
        return "170,60,60"
    return "100,100,100"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")


def o_name(oid):
    for o in ORGANIZATIONS:
        if o["id"] == oid:
            return o["name"]
    return ""


def generate_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>桂东县领导班子工作关系网络（2026-07 十四届党代会后）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in PERSONS:
        c = person_color(p["current_post"])
        cr, cg, cb = c.split(",")
        sz = "20.0" if p["id"] in (1, 2, 12) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in ORGANIZATIONS:
        c = org_color(o["type"])
        cr, cg, cb = c.split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    added_edges = set()
    for pos in POSITIONS:
        pid, oid = pos["person_id"], pos["org_id"]
        edge_key = f"p{pid}-o{oid}-{pos['title']}"
        if edge_key in added_edges:
            continue
        added_edges.add(edge_key)
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o_name(pos["org_id"]))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["start"])}—{esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in RELATIONSHIPS:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")


def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"  {table}: {c.fetchone()[0]}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  桂东县领导班子工作关系网络 — 数据构建")
    print("  调查日期: 2026-08-06")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()