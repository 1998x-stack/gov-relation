#!/usr/bin/env python3
"""
永兴县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for 永兴县 leadership network.
Investigation date: 2026-08-06
Task: hunan_永兴县 (湖南省 / 郴州市 / 永兴县)

IMPORTANT RESEARCH BASIS:
  - 2026-07-31 中国共产党永兴县第十四次代表大会及十四届一次全会选举产生新一届县委班子。
  - 来源: 永兴县融媒体中心 (www.yxrm.cn) 相关报道 (宾心华当选县委书记)。
  - 该县县委书记由原县长 宾心华 升任。现任县长人选尚未在可访问来源中确认 (开放缺口)。
  - 早年人物履历部分由本地既有资料 (Wikipedia zh / build_chenzhou_data.py) 佐证。

Confirmed current leadership (as of 2026-08-06):
    县委书记: 宾心华 (2026-07-31 当选; 此前2021.06起任县长)
    县委副书记: 王武文(瑶族)、尹涛
    县委常委: 曹清华、李超斌、李和、李平松、胡训忠(兼纪委书记)、李国斌、李立彪、黄芳红(女)
    人大主任: 王梅 / 政协主席: 李玲华 (均在2026.07县领导列席名单确认)
    县长: 待查 (宾心华升任书记后的继任者; 候选人可能从副书记或跨县调任中产生)
    前任县委书记: 刘朝晖 (2021-05 ~ 2026-07)
"""

import os
import sqlite3
from datetime import datetime

# ── Paths (relative to repo root) ──
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Staging-aware paths — when in data/tmp, write there; otherwise write to canonical locations
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING_CANDIDATE = os.path.join(REPO_ROOT, "data", "tmp", "hunan_永兴县")
if os.path.basename(THIS_DIR) == "hunan_永兴县":
    STAGING_DIR = THIS_DIR
    DB_PATH = os.path.join(STAGING_DIR, "永兴县_network.db")
    GEXF_PATH = os.path.join(STAGING_DIR, "永兴县_network.gexf")
else:
    DB_PATH = os.path.join(REPO_ROOT, "data", "database", "永兴县_network.db")
    GEXF_PATH = os.path.join(REPO_ROOT, "data", "graph", "永兴县_network.gexf")

# ════════════════════════════════════════════════════════════════
# RESEARCH DATA
# ════════════════════════════════════════════════════════════════

PERSONS = [
    # ── 1. 县委书记 (2026-07-31 当选) ──
    {
        "id": 1,
        "name": "宾心华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-06",
        "birthplace": "湖南省衡山县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共永兴县委员会",
        "source": "https://www.yxrm.cn/content/17558065 (永兴县融媒体中心)",
        "notes": "2026-07-31 中国共产党永兴县第十四届委员会第一次全体会议当选县委书记。此前任永兴县委副书记、县长（2021-06 起）。80后干部。",
    },
    # ── 2. 县长 (继任待查) ──
    {
        "id": 2,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "永兴县人民政府",
        "source": "开放缺口：宾心华升任书记后县长的继任人选未在可访问来源确认",
        "notes": "2026-07 宾心华由县长升任县委书记后，县长一职继任者为待查。可能从县委副书记（王武文/尹涛）或跨县调任产生。",
    },
    # ── 3. 县委副书记 ──
    {
        "id": 3,
        "name": "王武文",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共永兴县委员会",
        "source": "https://www.yxrm.cn/news/17558065（永兴县融媒体中心）",
        "notes": "2026-07-31 当选永兴县委副书记（瑶族）。",
    },
    {
        "id": 4,
        "name": "尹涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共永兴县委员会",
        "source": "https://www.yxrm.cn/news/17558065（永兴县融媒体中心）",
        "notes": "2026-07-31 当选永兴县委副书记。",
    },
    # ── 4. 县委常委 ──
    {
        "id": 5,
        "name": "曹清华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委委员、常委",
        "current_org": "中共永兴县委员会",
        "source": "https://www.yxrm.cn/news/17558065（永兴县融媒体中心）",
        "notes": "2026-07-31 当选永兴县委常委。",
    },
    {
        "id": 6,
        "name": "李超斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共永兴县委员会",
        "source": "https://www.yxrm.cn/news/17558065（永兴县融媒体中心）",
        "notes": "",
    },
    {
        "id": 7,
        "name": "李和",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共永兴县委员会",
        "source": "https://www.yxrm.cn/news/17558065（永兴县融媒体中心）",
        "notes": "",
    },
    {
        "id": 8,
        "name": "李平松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共永兴县委员会",
        "source": "https://www.yxrm.cn/news/17558065（永兴县融媒体中心）",
        "notes": "",
    },
    {
        "id": 9,
        "name": "胡训忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记",
        "current_org": "中共永兴县纪律检查委员会",
        "source": "https://www.yxrm.cn/news/17557970（永兴县融媒体中心）",
        "notes": "2026-07-31 当选永兴县委常委，并当选第十四届纪委书记。",
    },
    {
        "id": 10,
        "name": "李国斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共永兴县委员会",
        "source": "https://www.yxrm.cn/news/17558065（永兴县融媒体中心）",
        "notes": "",
    },
    {
        "id": 11,
        "name": "李立彪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共永兴县委员会",
        "source": "https://www.yxrm.cn/news/17558065（永兴县融媒体中心）",
        "notes": "",
    },
    {
        "id": 12,
        "name": "黄芳红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委会委员",
        "current_org": "中共永兴县委员会",
        "source": "https://www.yxrm.cn/news/17558065（永兴县融媒体中心）",
        "notes": "2026-07-31 当选永兴县委常委（女性）。",
    },
    # ── 13. 人大主任 (2021 起, 2026-07 仍在) ──
    {
        "id": 13,
        "name": "王梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969-09",
        "birthplace": "安徽省凤台县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "永兴县人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/永兴县；www.yxrm.cn/news/17557275",
        "notes": "2021-07 起任永兴县人大常委会主任；2026-07-31 党代会资料显示其仍在县领导之列。",
    },
    # ── 14. 政协主席 ──
    {
        "id": 14,
        "name": "李玲华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969-08",
        "birthplace": "湖南省耒阳市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议永兴县委员会",
        "source": "https://zh.wikipedia.org/wiki/永兴县；www.yxrc.cn/news/17557275",
        "notes": "2021-07 起任永兴县政协主席；2026-07-31 仍列席县领导。",
    },
    # ── 15. 前任县委书记 ──
    {
        "id": 15,
        "name": "刘朝晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-02",
        "birthplace": "湖南省攸县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永兴县委原书记（另有任用）",
        "current_org": "（原）中共永兴县委员会",
        "source": "https://zh.wikipedia.org/wiki/永兴县；www.yxrc.cn/news/17558065",
        "notes": "2021-05 起任永兴县委书记。2026-07 换届后未再出现在新一届县委名单，其继任为县委书记宾心华（2026-07-31），去向待查。",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共永兴县委员会", "type": "党委", "level": "县处级", "parent": "中共郴州市委", "location": "湖南省郴州市永兴县"},
    {"id": 2, "name": "永兴县人民政府", "type": "政府", "level": "县处级", "parent": "郴州市人民政府", "location": "湖南省郴州市永兴县"},
    {"id": 3, "name": "永兴县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "郴州市人大常委会", "location": "湖南省郴州市永兴县"},
    {"id": 4, "name": "中国人民政治协商会议永兴县委员会", "type": "政协", "level": "县处级", "parent": "政协郴州市委员会", "location": "湖南省郴州市永兴县"},
    {"id": 5, "name": "中共永兴县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共永兴县委员会", "location": "湖南省郴州市永兴县"},
    {"id": 6, "name": "中共郴州市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "湖南省郴州市"},
    {"id": 7, "name": "郴州市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "湖南省郴州市"},
]

POSITIONS = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "永兴县委书记", "start": "2026-07-31", "end": "present", "rank": "正处级", "note": "第十四届一次全会当选"},
    {"person_id": 1, "org_id": 2, "title": "永兴县县长", "start": "2021-06", "end": "2026-07", "rank": "正处级", "note": "此前任县长，换届升任书记"},
    # 县长（待查占位）
    {"person_id": 2, "org_id": 2, "title": "永兴县县长", "start": "", "end": "", "rank": "正处级", "note": "继任人选待确认"},
    # 副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": "瑶族"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": ""},
    # 常委
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 5, "title": "县纪委书记、县委常委", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": "第十四届纪委书记"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": "女性"},
    # 人大 / 政协
    {"person_id": 13, "org_id": 3, "title": "县人大常委会主任", "start": "2021-07", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 4, "title": "县政协主席", "start": "2021-07", "end": "present", "rank": "正处级", "note": ""},
    # 前任书记
    {"person_id": 15, "org_id": 1, "title": "永兴县委书记", "start": "2021-05", "end": "2026-07", "rank": "正处级", "note": "2026-07 换届卸任"},
]

RELATIONSHIPS = [
    # 党政正职 (书记 × 现任县长-待查)
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "县委书记与县长为永兴县党政正职搭档关系；现任县长继任待确认", "overlap_org": "永兴县", "overlap_period": "2026至今"},
    # 书记 前任·继任 (宾心华 <- 刘朝晖)
    {"person_a": 15, "person_b": 1, "type": "前任继任", "context": "刘朝晖2026年7月卸任县委书记，宾心华2026-07-31接任", "overlap_org": "中共永兴县委员会", "overlap_period": "2026-07"},
    # 党政搭档（前任，宾心华时任县长 刘朝晖时任书记）
    {"person_a": 15, "person_b": 1, "type": "党政搭档", "context": "刘朝晖2021-05起任书记、宾心华2021-06起任县长，两人搭档主政永兴约五年", "overlap_org": "永兴县", "overlap_period": "2021-2026"},
    # 四套班子班子成员
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "县委书记与人大常委会主任同属永兴县四套班子", "overlap_org": "永兴县", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "县委书记与政协主席同属永兴县四套班子", "overlap_org": "永兴县", "overlap_period": "2026至今"},
    # 纪委与县委
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "纪委书记胡训忠为县委常委会班子成员、受县委领导", "overlap_org": "中共永兴县委员会", "overlap_period": "2026至今"},
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
    """XML-escape a string."""
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


def generate_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>永兴县领导班子工作关系网络（2026-07-31 换届选举后）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        c = person_color(p["current_post"])
        cr, cg, cb = c.split(",")
        sz = "20.0" if p["id"] in (1, 2, 15) else "12.0"
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

    # Edges
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


def o_name(oid):
    for o in ORGANIZATIONS:
        if o["id"] == oid:
            return o["name"]
    return ""


def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"  {table}: {c.fetchone()[0]}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  永兴县领导班子工作关系网络 — 数据构建")
    print("  调查日期: 2026-08-06")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()
    print("\n⚠️  县长继任人选为开放缺口；详见 person JSON 与 open_gaps。")