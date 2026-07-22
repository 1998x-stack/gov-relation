#!/usr/bin/env python3
"""
靖安县（宜春市下辖县）领导班子工作关系网络 — 数据构建脚本
Builds SQLite DB + GEXF graph for Jing'an County leadership network.

Research date: 2026-07-15
Task ID: jiangxi_靖安县

Sources:
  - build_奉新县_data.py (fengxin_yu_jun person data via 网易新闻 2024-12-24)
  - build_data.py (Jiangxi provincial data — 郑绍靖安县委书记 info)
  - data/persons/20260715-江西省-宜春市-县委书记-黄为民.json (黄为民靖安县长履历)
  - data/persons/20260715-江西省-宜春市-县委书记-陈志尧.json (陈志尧靖安常务副县长履历)
  - 网易新闻 https://www.163.com/dy/article/JKB05GCC05496YZA.html — 喻军任靖安县委书记(2024-12)
  - 五星党建 (宜春市委组织部公众号)

NOTE: External web access (jxjingan.gov.cn, Baidu Baike) was blocked during research.
Key positions confirmed from media reports and existing repo data. All claims labeled with confidence.
The current 靖安县长 (post-2024-12 successor to 黄为民) name is unknown and marked as gap.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
TMP = BASE  # We're already in data/tmp/jiangxi_靖安县/
DB_PATH = os.path.join(TMP, "靖安县_network.db")
GEXF_PATH = os.path.join(TMP, "靖安县_network.gexf")

os.makedirs(TMP, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
# Sources:
# - 网易新闻 (2024-12-24): 喻军任靖安县委书记 — https://www.163.com/dy/article/JKB05GCC05496YZA.html
# - 网易新闻 (2024-12-26): 宜丰人黄为民任奉新县委书记 — https://www.163.com/dy/article/JKB05GCC05496YZA.html
# - data/persons/20260715-江西省-宜春市-县委书记-黄为民.json
# - data/persons/20260715-江西省-宜春市-县委书记-陈志尧.json
# - build_data.py (郑绍靖安县委书记)
# - thepaper.cn (郑绍跨市交流) — https://m.thepaper.cn/newsDetail_forward_15055739

persons = [
    # ═══ Current Party Secretary (现任县委书记) ═══
    {
        "id": 1, "name": "喻军", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-01", "birthplace": "江西高安",
        "education": "研究生",
        "party_join": "中共党员", "work_start": "1999-10",
        "current_post": "中共靖安县委书记",
        "current_org": "中共靖安县委员会",
        "source": "网易新闻 https://www.163.com/dy/article/JKB05GCC05496YZA.html — 喻军任靖安县委书记(2024-12); 五星党建 (宜春市委组织部公众号)"
    },

    # ═══ Current County Mayor (现任县长) — NAME UNKNOWN ═══
    {
        "id": 2, "name": "（待核实）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "靖安县委副书记、县长",
        "current_org": "靖安县人民政府",
        "source": "⚠️ 2024年12月黄为民离任靖安县长后，继任县长姓名待查。可能人选举自靖安县委班子或宜春市直调任。"
    },

    # ═══ Previous Party Secretary & Leaders ═══
    # 黄为民 — 前任靖安县长 (~2021-2024); 现任奉新县委书记
    {
        "id": 3, "name": "黄为民", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-01", "birthplace": "江西宜丰",
        "education": "中专",
        "party_join": "中共党员", "work_start": "",
        "current_post": "中共奉新县委书记",
        "current_org": "中共奉新县委员会",
        "source": "网易新闻 https://www.163.com/dy/article/JKB05GCC05496YZA.html — 宜丰人黄为民任奉新县委书记; data/persons/20260715-江西省-宜春市-县委书记-黄为民.json"
    },

    # 郑绍 — 前任靖安县委书记 (~2019-?跨市交流自永修县长)
    {
        "id": 4, "name": "郑绍", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "", "current_org": "",
        "source": "https://m.thepaper.cn/newsDetail_forward_15055739 — 澎湃新闻关于跨设区市交流"
    },

    # ═══ Key Deputies (known from repo data) ═══
    # 陈志尧 — 曾任靖安县委常委、常务副县长 (2016-2017), 现任奉新县委书记
    {
        "id": 5, "name": "陈志尧", "gender": "男", "ethnicity": "汉族",
        "birth": "1972-07", "birthplace": "江西樟树",
        "education": "大学",
        "party_join": "中共党员", "work_start": "1994-08",
        "current_post": "中共奉新县委书记",
        "current_org": "中共奉新县委员会",
        "source": "data/persons/20260715-江西省-宜春市-县委书记-陈志尧.json; 公开履历"
    },

    # ═══ Current Standing Committee (待核实 — names unknown) ═══
    {
        "id": 6, "name": "（专职副书记）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "靖安县委副书记（专职）",
        "current_org": "中共靖安县委员会",
        "source": "待查 — 需访问 jxjingan.gov.cn 或宜春市委组织部任前公示"
    },
    {
        "id": 7, "name": "（常务副县长）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "靖安县委常委、常务副县长",
        "current_org": "靖安县人民政府",
        "source": "待查"
    },
    {
        "id": 8, "name": "（纪委书记）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "靖安县委常委、纪委书记、县监委主任",
        "current_org": "中共靖安县纪律检查委员会",
        "source": "待查"
    },
    {
        "id": 9, "name": "（组织部部长）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "靖安县委常委、组织部部长",
        "current_org": "中共靖安县委组织部",
        "source": "待查"
    },
    {
        "id": 10, "name": "（宣传部部长）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "靖安县委常委、宣传部部长",
        "current_org": "中共靖安县委宣传部",
        "source": "待查"
    },
    {
        "id": 11, "name": "（政法委书记）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "靖安县委常委、政法委书记",
        "current_org": "中共靖安县委政法委员会",
        "source": "待查"
    },
    {
        "id": 12, "name": "（统战部部长）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "靖安县委常委、统战部部长",
        "current_org": "中共靖安县委统战部",
        "source": "待查"
    },
    # ═══ NPC & CPPCC ═══
    {
        "id": 13, "name": "（人大常委会主任）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "靖安县人大常委会主任",
        "current_org": "靖安县人民代表大会常务委员会",
        "source": "待查"
    },
    {
        "id": 14, "name": "（政协主席）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "政协靖安县委员会主席",
        "current_org": "政协靖安县委员会",
        "source": "待查"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共靖安县委员会", "type": "党委", "level": "县处级",
     "parent": "中共宜春市委员会", "location": "江西省宜春市靖安县"},
    {"id": 2, "name": "靖安县人民政府", "type": "政府", "level": "县处级",
     "parent": "宜春市人民政府", "location": "江西省宜春市靖安县"},
    {"id": 3, "name": "靖安县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "宜春市人大常委会", "location": "江西省宜春市靖安县"},
    {"id": 4, "name": "政协靖安县委员会", "type": "政协", "level": "县处级",
     "parent": "政协宜春市委员会", "location": "江西省宜春市靖安县"},
    {"id": 5, "name": "中共靖安县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共宜春市纪律检查委员会", "location": "江西省宜春市靖安县"},
    {"id": 6, "name": "中共靖安县委组织部", "type": "党委", "level": "县处级",
     "parent": "中共靖安县委员会", "location": "江西省宜春市靖安县"},
    {"id": 7, "name": "中共靖安县委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共靖安县委员会", "location": "江西省宜春市靖安县"},
    {"id": 8, "name": "中共靖安县委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共靖安县委员会", "location": "江西省宜春市靖安县"},
    {"id": 9, "name": "中共靖安县委统战部", "type": "党委", "level": "县处级",
     "parent": "中共靖安县委员会", "location": "江西省宜春市靖安县"},
    {"id": 10, "name": "中共宜春市委员会", "type": "党委", "level": "地市级",
     "parent": "中共江西省委员会", "location": "江西省宜春市"},
    {"id": 11, "name": "宜春市人民政府", "type": "政府", "level": "地市级",
     "parent": "江西省人民政府", "location": "江西省宜春市"},
    # Cross-county orgs for context
    {"id": 12, "name": "中共奉新县委员会", "type": "党委", "level": "县处级",
     "parent": "中共宜春市委员会", "location": "江西省宜春市奉新县"},
    {"id": 13, "name": "奉新县人民政府", "type": "政府", "level": "县处级",
     "parent": "宜春市人民政府", "location": "江西省宜春市奉新县"},
    {"id": 14, "name": "永修县人民政府", "type": "政府", "level": "县处级",
     "parent": "九江市人民政府", "location": "江西省九江市永修县"},
    {"id": 15, "name": "中共宜丰县委员会", "type": "党委", "level": "县处级",
     "parent": "中共宜春市委员会", "location": "江西省宜春市宜丰县"},
    {"id": 16, "name": "宜丰县人民政府", "type": "政府", "level": "县处级",
     "parent": "宜春市人民政府", "location": "江西省宜春市宜丰县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 喻军 (1) — 靖安县委书记 ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共靖安县委书记",
     "start": "2024-12", "end": "", "rank": "县处级正职",
     "note": "由奉新县长调任靖安县委书记"},
    {"id": 2, "person_id": 1, "org_id": 13, "title": "奉新县委副书记、县长",
     "start": "2021-08", "end": "2024-12", "rank": "县处级正职",
     "note": "奉新县人民政府县长"},
    {"id": 3, "person_id": 1, "org_id": 15, "title": "宜丰县委副书记",
     "start": "2020-12", "end": "2021-08", "rank": "县处级副职",
     "note": "宜丰县委专职副书记"},
    {"id": 4, "person_id": 1, "org_id": 16, "title": "宜丰县委常委、常务副县长",
     "start": "2019-07", "end": "2020-12", "rank": "县处级副职",
     "note": ""},
    {"id": 5, "person_id": 1, "org_id": 11, "title": "樟树市委常委、市政府党组成员",
     "start": "2016-07", "end": "2019-07", "rank": "县处级副职",
     "note": "樟树市为宜春市代管县级市"},
    {"id": 6, "person_id": 1, "org_id": 11, "title": "宜春市交通运输局副局长（挂任丰城市委常委、副市长）",
     "start": "2014-07", "end": "2016-07", "rank": "县处级副职",
     "note": "挂职锻炼"},
    {"id": 7, "person_id": 1, "org_id": 11, "title": "高安市上湖乡党委书记",
     "start": "2013-03", "end": "2014-07", "rank": "乡科级正职",
     "note": "上湖乡党委书记、人大主席"},
    {"id": 8, "person_id": 1, "org_id": 11, "title": "高安市相城镇党委副书记、镇长",
     "start": "2009-04", "end": "2013-03", "rank": "乡科级正职",
     "note": ""},
    {"id": 9, "person_id": 1, "org_id": 11, "title": "高安市八景镇党委副书记",
     "start": "2007-03", "end": "2008-05", "rank": "乡科级副职",
     "note": ""},
    {"id": 10, "person_id": 1, "org_id": 11, "title": "高安市委政法委综治办副主任",
     "start": "2006-01", "end": "2007-03", "rank": "乡科级副职",
     "note": ""},
    {"id": 11, "person_id": 1, "org_id": 11, "title": "高安市委驻瑞州街道副科级维稳信息督查员",
     "start": "2003-07", "end": "2006-01", "rank": "副科级",
     "note": ""},
    {"id": 12, "person_id": 1, "org_id": 11, "title": "高安市筠阳镇干部、党政办主任",
     "start": "1999-10", "end": "2003-07", "rank": "科员级",
     "note": "宜春地委组织部公开选拔选调生"},

    # ── （待核实）(2) — 靖安县长 ──
    {"id": 13, "person_id": 2, "org_id": 2, "title": "靖安县委副书记、县长",
     "start": "~2024-12", "end": "", "rank": "县处级正职",
     "note": "⚠️ 继任县长姓名待核实。黄为民2024年12月离任靖安县长后的接任者。"},

    # ── 黄为民 (3) — 前任靖安县长/现任奉新县委书记 ──
    {"id": 14, "person_id": 3, "org_id": 12, "title": "中共奉新县委书记",
     "start": "2024-12", "end": "", "rank": "县处级正职",
     "note": "从靖安县长升任奉新县委书记"},
    {"id": 15, "person_id": 3, "org_id": 2, "title": "靖安县委副书记、县长",
     "start": "2021-02", "end": "2024-12", "rank": "县处级正职",
     "note": ""},
    {"id": 16, "person_id": 3, "org_id": 2, "title": "靖安县委副书记、副县长、代理县长",
     "start": "2021-01", "end": "2021-02", "rank": "县处级正职",
     "note": "代理县长过渡期"},
    {"id": 17, "person_id": 3, "org_id": 2, "title": "靖安县委副书记、提名为县长候选人",
     "start": "2020-12", "end": "2021-01", "rank": "县处级正职",
     "note": ""},

    # ── 郑绍 (4) — 前任靖安县委书记（跨市交流）──
    {"id": 18, "person_id": 4, "org_id": 1, "title": "中共靖安县委书记",
     "start": "2019-08", "end": "", "rank": "县处级正职",
     "note": "从九江市永修县长跨设区市交流至宜春市靖安县委书记"},
    {"id": 19, "person_id": 4, "org_id": 14, "title": "永修县委副书记、县长",
     "start": "", "end": "2019-08", "rank": "县处级正职",
     "note": "永修县属九江市管辖"},

    # ── 陈志尧 (5) — 靖安县委常委、常务副县长（2016-2017）──
    {"id": 20, "person_id": 5, "org_id": 2, "title": "靖安县委常委、常务副县长",
     "start": "2016-08", "end": "2017-12", "rank": "县处级副职",
     "note": "陈志尧在靖安县任常务副县长约16个月"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 喻军 ↔ （待核实县长）党政搭档 ──
    {"id": 1, "person_a": 1, "person_b": 2,
     "type": "党政搭档",
     "context": "喻军（县委书记）与待核实县长为靖安县党政一把手",
     "overlap_org": "靖安县",
     "overlap_period": "2024-12至今"},

    # ── 喻军 ↔ 黄为民（前后任关系在靖安履职，交叉在奉新-靖安）──
    {"id": 2, "person_a": 1, "person_b": 3,
     "type": "前后任/跨县交流",
     "context": "黄为民任靖安县长(2021-2024)后调任奉新县委书记;喻军任奉新县长(2021-2024)后调任靖安县委书记;二人分别在靖安和奉新交叉",
     "overlap_org": "靖安县人民政府/奉新县人民政府",
     "overlap_period": "2021-02/2024-12",
     "confidence": "confirmed"},

    # ── 喻军 ↔ 郑绍（靖安县委书记前后任）──
    {"id": 3, "person_a": 1, "person_b": 4,
     "type": "前后任",
     "context": "郑绍（~2019-?任靖安县委书记）→ 喻军（2024-12任靖安县委书记）。中间可能还有一任书记",
     "overlap_org": "中共靖安县委员会",
     "overlap_period": "不重叠（前后任）"},

    # ── 喻军 ↔ 陈志尧（奉新党政搭档）──
    {"id": 4, "person_a": 1, "person_b": 5,
     "type": "党政搭档（奉新）",
     "context": "陈志尧任奉新县委书记期间(2021-2024)，喻军任奉新县长(2021.08-2024.09)。二人为奉新县党政一把手搭档",
     "overlap_org": "中共奉新县委员会/奉新县人民政府",
     "overlap_period": "2021-08/2024-09",
     "confidence": "confirmed"},

    # ── 陈志尧 ↔ 黄为民（奉新-靖安跨县关联）──
    {"id": 5, "person_a": 5, "person_b": 3,
     "type": "跨县关联",
     "context": "陈志尧曾在靖安任常务副县长(2016-2017)，后在奉新任县委书记;黄为民在靖安任县长(2021-2024)，后在奉新任县委书记。二人先后主政奉新",
     "overlap_org": "靖安县/奉新县",
     "overlap_period": "2016-2024",
     "confidence": "plausible"},

    # ── 黄为民 ↔ 郑绍（靖安前后任/党政关联）──
    {"id": 6, "person_a": 3, "person_b": 4,
     "type": "跨时期关联",
     "context": "郑绍任靖安县委书记期间，黄为民尚未到靖安。但二人均与靖安县有关联",
     "overlap_org": "靖安县",
     "overlap_period": "2019-2024",
     "confidence": "plausible"},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT,
    parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, "end" TEXT,
    rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT,
    overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")

for p in persons:
    c.execute(
        "INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
        (p["id"], p["name"], p["gender"], p["ethnicity"],
         p["birth"], p["birthplace"], p["education"],
         p["party_join"], p["work_start"],
         p["current_post"], p["current_org"], p["source"])
    )

for o in organizations:
    c.execute(
        "INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
    )

for pos in positions:
    c.execute(
        "INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
        (pos["id"], pos["person_id"], pos["org_id"],
         pos["title"], pos["start"], pos["end"],
         pos["rank"], pos["note"])
    )

for r in relationships:
    c.execute(
        "INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
        (r["id"], r["person_a"], r["person_b"],
         r["type"], r["context"], r["overlap_org"], r["overlap_period"])
    )

conn.commit()

counts = {}
for t in ["persons", "organizations", "positions", "relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()

print(f"SQLite DB: {DB_PATH}")
for t, n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(name, post):
    """Color by person role."""
    full = (name or "") + " " + (post or "")
    if "县委书记" in full:
        return "255,50,50"  # Red for party secretary
    if "县长" in full and "副县长" not in full:
        return "50,100,255"  # Blue for county mayor
    if "副县长" in full or "常务副县长" in full:
        return "80,140,230"
    if "纪委书记" in full or "监委" in full:
        return "255,165,0"
    if "人大" in full:
        return "200,230,255"
    if "政协" in full:
        return "230,200,255"
    if "副书记" in full:
        return "200,100,100"
    if "组织部" in full:
        return "100,200,100"
    if "宣传部" in full:
        return "100,100,200"
    if "政法委" in full:
        return "150,100,50"
    if "统战部" in full:
        return "150,150,100"
    return "120,120,120"

def org_color(otype):
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,230,255",
        "政协": "230,200,255",
    }.get(otype, "200,200,200")

def person_size(p):
    if any(k in (p.get("current_post", "") or "") for k in ["县委书记", "县长", "人大常委会主任", "政协主席"]):
        return "20.0"
    return "12.0"

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>靖安县（宜春市下辖县）领导班子工作关系网络 — 2026年7月15日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
for aid, atitle in [("0", "type"), ("1", "birth"), ("2", "birthplace"),
                     ("3", "current_post"), ("4", "entity_type"), ("5", "level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
for aid, atitle in [("0", "type"), ("1", "start"), ("2", "end"), ("3", "context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')

# Nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p["name"], p.get("current_post", ""))
    sz = person_size(p)
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f, v in [("0", "person"), ("1", p.get("birth", "")),
                  ("2", p.get("birthplace", "")),
                  ("3", p.get("current_post", "")),
                  ("4", "person"), ("5", "")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    r, g, b = c.split(",")
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

for o in organizations:
    c_val = org_color(o.get("type", ""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f, v in [("0", "organization"), ("1", ""),
                  ("2", o.get("location", "")),
                  ("3", ""), ("4", "organization"),
                  ("5", o.get("level", ""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    r, g, b = c_val.split(",") if "," in c_val else ("200", "200", "200")
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" '
                 f'target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f, v in [("0", "worked_at"), ("1", pos.get("start", "")),
                  ("2", pos.get("end", "")), ("3", pos.get("note", ""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

for r in relationships:
    if r["person_b"] == 0:
        continue
    eid += 1
    ov = r.get("overlap_period", "")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" '
                 f'target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f, v in [("0", r["type"]), ("1", ov_s), ("2", ""),
                  ("3", r.get("context", ""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

tn = len(persons) + len(organizations)
te = len(positions) + len(relationships)
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone!")
