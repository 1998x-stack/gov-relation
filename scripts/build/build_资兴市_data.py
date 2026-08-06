#!/usr/bin/env python3
"""
资兴市领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for 资兴市 leadership network.
Investigation date: 2026-08-06
Task: hunan_资兴市 (湖南省 / 郴州市 / 资兴市 / 县级市)

IMPORTANT RESEARCH BASIS (2026-08-06):
  - 现任市委书记: 陈占华。2026-03-19 湖南省委组织部公示"拟进一步使用"；
    2026-03-29 资兴市委召开全市领导干部大会，省委决定陈占华任中共资兴市委书记
    （来源: 华声在线/红网/红星郴州）。此前 2021-07 起任资兴市委副书记、市长。
  - 现任代市长: 覃志名。2026-05-19 郴州市委管理干部任前公示拟提名为县市区人民政府正职人选；
    2026-06-16 资兴市人大常委会决定任命其为资兴市副市长、代理市长；2026-07-28 仍代理市长。
  - 前任市委书记: 杨理诚。2021-07-13 起任资兴市委书记；2026-03 前后调任中南林业科技大学党委副书记
    （来源：中南林业科技大学现任领导页/新闻网、网易）。
  - 前任(更早)书记: 黄峥嵘。2021-07-13 不再担任资兴市委书记。

Confirmed current leadership (as of 2026-07-29):
    市委书记: 陈占华 (2026-03-29 起; 此前2021.07起任市长)
    代市长:   覃志名 (2026-06-16 人大常委会任命; 原郴州跨市交流干部，曾任株洲市应急管理局局长)
    人大主任: 王仁庆 (湖南安仁, 1968-11)
    政协主席: 陈一之 (2021-07 起)

Uncertain / gaps:
    - 陈占华 2021 年任资兴市长之前的完整履历（1991 参加工作后的具体职位无一手来源）
    - 覃志名性别/民族信息为数据库来源（百度百科/AI摘要）；其在株洲市、援藏等任职路径已确认
       但资兴代市长转正时间未确
    - 2026 年 3 月杨理诚调任中南林业科技大学后的继任书记（陈占华）之后的市长继任
       即为覃志名，属市场交换（株洲->郴州）；其他跨市县干部流动个案未逐一核实
"""

import os
import sqlite3
from datetime import datetime

# ── Paths (relative to repo root) ──
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Staging-aware paths — when in data/tmp, write there; otherwise write to canonical locations
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING_CANDIDATE = os.path.join(REPO_ROOT, "data", "tmp", "hunan_资兴市")
if os.path.basename(THIS_DIR) == "hunan_资兴市":
    STAGING_DIR = THIS_DIR
    DB_PATH = os.path.join(STAGING_DIR, "资兴市_network.db")
    GEXF_PATH = os.path.join(STAGING_DIR, "资兴市_network.gexf")
else:
    DB_PATH = os.path.join(REPO_ROOT, "data", "database", "资兴市_network.db")
    GEXF_PATH = os.path.join(REPO_ROOT, "data", "graph", "资兴市_network.gexf")

# ════════════════════════════════════════════════════════════════
# RESEARCH DATA
# ════════════════════════════════════════════════════════════════

PERSONS = [
    # ── 1. 市委书记 (2026-03-29 任) ──
    {
        "id": 1,
        "name": "陈占华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-02",
        "birthplace": "湖南省永兴县",
        "education": "在职大学（郴州师范）",
        "party_join": "1997-12",
        "work_start": "1991-07",
        "current_post": "市委书记",
        "current_org": "中共资兴市委员会",
        "source": "https://www.hnls.com.cn (华声在线 2026-03-29); 红网; 委组织部公示 2026-03-19",
        "notes": "男，汉族，湖南永兴人，1973年2月出生，在职大学，中共党员。1991年7月参加工作，1997年12月加入中国共产党。2021-07-20 任资兴市委副书记、市长；2026-03-19 委组织部公示拟进一步使用；2026-03-29 全市领导干部会宣布任资兴市委书记。",
    },
    # ── 2. 代市长 (2026-06-16 任命) ──
    {
        "id": 2,
        "name": "覃志名",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1983-09",
        "birthplace": "湖南省石门县",
        "education": "大学（管理学学士）",
        "party_join": "2005-04",
        "work_start": "2006-08",
        "current_post": "代市长",
        "current_org": "资兴市人民政府",
        "source": "https://www.baike.baidu.com (覃志名)/郴州市委组织部任前公示 2026-05-19；新浪网2026-07-28",
        "notes": "男，土家族，1983年9月出生，湖南石门人，大学本科学历（管理学学士），2005年4月加入中国共产党，2006年8月参加工作。曾任湖南省第十批援藏工作总领队、西藏自治区山南市扎囊县委副书记（政府常务副县长）；2025年9月任株洲市应急管理局党委书记，同年11月任局长。郴州市委组织部2026-05-19任前公示拟提名为县市区人民政府正职人选；2026-06-16 资兴市人大常委会决定任命为副市长、代市长。",
    },
    # ── 3. 前任书记 (杨理诚 2021-07~2026-03) ──
    {
        "id": 3,
        "name": "杨理诚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-08",
        "birthplace": "湖南省湘阴县",
        "education": "博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中南林业科技大学党委副书记",
        "current_org": "中南林业科技大学",
        "source": "岳阳日报 2020-08-25 任前公示；中南林业科技大学现任领导页；网易 2026-03-21",
        "notes": "男，汉族，1976年8月生，湖南湘阴人，中共党员，博士，教授，硕士生导师，省'121人才工程'人选。曾任安仁县委副书记；2020-09 提名资兴市长；2021-07 任资兴市委书记；2026-03 前后调任中南林业科技大学党委副书记（现任领导页在列，分管组织部、党校、离退休工作处、工会）。",
    },
    # ── 4. 前任书记 (黄峥嵘 卸任 2021-07-13) ──
    {
        "id": 4,
        "name": "黄峥嵘",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原）资兴市委书记",
        "current_org": "中共资兴市委员会",
        "source": "红网 2021-07-14：资兴市委全市领导干部大会",
        "notes": "2021-07-13 郴州市委宣布 潇何不再担任资兴市委书记、常委、委员职务，杨理诚接任。其此前任职与去向未在可访问来源核实。",
    },
# ── 5. 市人大主任 ──
    {
        "id": 5,
        "name": "王仁庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-11",
        "birthplace": "湖南省安仁县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "资兴市人民代表大会常务委员会",
        "source": "资兴市第十八届人民代表大会第五次会议（2025-12-23）；zh.wikipedia.org/wiki/资兴市",
        "notes": "2021-07 起任资兴市人大常委会主任、党组书记。出席并主持 2025-12-23 市人大五次会议。",
    },
    # ── 6. 市政协主席 ──
    {
        "id": 6,
        "name": "陈一之",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议资兴市委员会",
        "source": "https://zh.wikipedia.org/wiki/资兴市；市人大五次会议主席台名单",
        "notes": "2021-07 起任资兴市政协主席。2025-12-23 市人大五次会议在主席台就座。",
    },
    # ── 7. 市委副书记 (2021 十三届) ──
    {
        "id": 7,
        "name": "龙柏武",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共资兴市委员会",
        "source": "网易 2021-08-02：湖南最新一批人事任命",
        "notes": "2021-07-31 资兴市第十三届一次全会当选市委副书记（与市委书记杨理诚、副书记陈占华同期）。",
    },
]

# NOTE: 人物 id 已分配 1..7。陈占华任市长（2021-2026）与书记（2026至今）的履历在同一个人记录（id1）中体现，
# 其 '市委副书记、市长' 身份亦由 POSITIONS 的 org2 记录覆盖。故不再额外引入重复人物。

ORGANIZATIONS = [
    {"id": 1, "name": "中共资兴市委员会", "type": "党委", "level": "县处级", "parent": "中共郴州市委", "location": "湖南省郴州市资兴市"},
    {"id": 2, "name": "资兴市人民政府", "type": "政府", "level": "县处级", "parent": "郴州市人民政府", "location": "湖南省郴州市资兴市"},
    {"id": 3, "name": "资兴市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "郴州市人大常委会", "location": "湖南省郴州市资兴市"},
    {"id": 4, "name": "中国人民政治协商会议资兴市委员会", "type": "政协", "level": "县处级", "parent": "政协郴州市委员会", "location": "湖南省郴州市资兴市"},
    {"id": 5, "name": "中共资兴市纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共资兴市委员会", "location": "湖南省郴州市资兴市"},
    {"id": 6, "name": "中共郴州市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "湖南省郴州市"},
    {"id": 7, "name": "郴州市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "湖南省郴州市"},
    {"id": 8, "name": "湖南省株洲市应急管理局", "type": "政府", "level": "地市级", "parent": "株洲市人民政府", "location": "湖南省株洲市"},
    {"id": 9, "name": "中南林业科技大学", "type": "事业单位", "level": "副厅级", "parent": "湖南省人民政府", "location": "湖南省长沙市"},
]

POSITIONS = [
    # 市委书记 陈占华 (id1)
    {"person_id": 1, "org_id": 1, "title": "资兴市委书记", "start": "2026-03", "end": "present", "rank": "正处级", "note": "2026-03-29 全市领导干部会宣布"},
    {"person_id": 1, "org_id": 2, "title": "资兴市市长", "start": "2021-07", "end": "2026-03", "rank": "正处级", "note": "2021-07-20 提名/任市长，2026-03 晋升书记"},
    # 代市长 覃志远 (id2)
    {"person_id": 2, "org_id": 2, "title": "资兴市代市长", "start": "2026-06", "end": "present", "rank": "正处级", "note": "2026-06-16 市人大常委会任命"},
    {"person_id": 2, "org_id": 8, "title": "株洲市应急管理局局长", "start": "2025-11", "end": "2026-05", "rank": "正处级", "note": "2025-09 任党委书记，11月任局长；后交流至郴州"},
    {"person_id": 2, "org_id": 8, "title": "株洲市应急管理局党委书记", "start": "2025-09", "end": "2026-05", "rank": "正处级", "note": ""},
    # 前任书记 杨立诚 (id3)
    {"person_id": 3, "org_id": 1, "title": "资兴市委书记", "start": "2021-07", "end": "2026-03", "rank": "正处级", "note": "2021-07-13 干部大会宣布接任黄峥嵘"},
    {"person_id": 3, "org_id": 2, "title": "资兴市市长", "start": "2020-09", "end": "2021-07", "rank": "正处级", "note": "2020-08-23 公示，2020-09 提名为市长候选人"},
    {"person_id": 3, "org_id": 9, "title": "中南林业科技大学党委副书记", "start": "2026-03", "end": "present", "rank": "副厅级", "note": "由资兴市委书记转任高校党委副书记"},
    # 前任书记 黄峥嵘 (id4)
    {"person_id": 4, "org_id": 1, "title": "资兴市委书记", "start": "", "end": "2021-07", "rank": "正处级", "note": "2021-07-13 不再担任"},
    # 人大 / 政协
    {"person_id": 5, "org_id": 3, "title": "市人大常委会主任", "start": "2021-07", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "市政协主席", "start": "2021-07", "end": "present", "rank": "正处级", "note": ""},
    # 副书记 龙柏武 (id7)
    {"person_id": 7, "org_id": 1, "title": "市委副书记", "start": "2021-07", "end": "", "rank": "副处级", "note": "2021-07-31 十三届一次全会当选"},
]

# 陈占华任市委副书记、市长（2021-2026）与市委书记（2026至今）的二元身份在同一人物记录（id1）中体现，
# 其经历即由 POSITIONS 的 org1/org2 两条记录覆盖。

RELATIONSHIPS = [
    # 党政正职（现任）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "2026年市委书记陈占华与代市长覃志名搭档主政资兴", "overlap_org": "资兴市", "overlap_period": "2026至今"},
    # 前·后继任（市长->书记）
    {"person_a": 3, "person_b": 1, "type": "前任继任", "context": "杨理诚2026-03调任高校，陈占华接任资兴市委书记", "overlap_org": "中共资兴市委员会", "overlap_period": "2026-03"},
    {"person_a": 4, "person_b": 3, "type": "前任继任", "context": "黄峥嵘2021-07卸任，杨理诚接任资兴市委书记", "overlap_org": "中共资兴市委员会", "overlap_period": "2021-07"},
    # 党政搭档（历史）
    {"person_a": 1, "person_b": 3, "type": "党政搭档", "context": "2021-2026年期间杨理诚任书记、陈占华任市长搭档主政资兴", "overlap_org": "资兴市", "overlap_period": "2021-2026"},
    # 跨市域交流（株洲 -> 资兴）
    {"person_a": 2, "person_b": 1, "type": "跨市干部交流", "context": "覃志名自株洲市应急管理局交流至资兴任代市长，属市际干部流动", "overlap_org": "郴州市", "overlap_period": "2026"},
    # 四套班子
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "市委书记与人大主任同属资兴市四套班子", "overlap_org": "资兴市", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "市委书记与政协主席同属资兴市四套班子", "overlap_org": "资兴市", "overlap_period": "2026至今"},
]

# ════════════════════════════════════════════════════════════════
# DATABASE BUILD
# ════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


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
# GEXF BUILD — 使用字符串拼接避免 ElementTree 的 namespace 问题
# ════════════════════════════════════════════════════════════════

def person_color(title):
    t = title or ""
    if "市委书记" in t:
        return "255,50,50"
    if "市长" in t and "副" not in t and "书记" not in t:
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
        "事业单位": "220,220,220",
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
    lines.append('    <description>资兴市领导班子工作关系网络（2026-03 市委书记换届后）</description>')
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

    persons = build_persons()
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["current_post"])
        cr, cg, cb = c.split(",")
        sz = "20.0" if p["id"] in (1, 2, 3, 4) else "12.0"
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
    added = set()
    for pos in POSITIONS:
        pid, oid = pos["person_id"], pos["org_id"]
        key = f"p{pid}-o{oid}-{pos['title']}"
        if key in added:
            continue
        added.add(key)
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o_name(oid))}"/>')
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


def build_persons():
    return PERSONS


def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"  {table}: {c.fetchone()[0]}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  资兴市领导班子工作关系网络 — 数据构建")
    print("  调查日期: 2026-08-06")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()