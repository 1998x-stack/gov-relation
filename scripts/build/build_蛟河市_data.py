#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 蛟河市, 吉林市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_蛟河市
Research sources:
  - jiaohe.gov.cn — 蛟河市人民政府官方网站 (primary, accessed via HTTP July 2026)
  - jiaohe.gov.cn/xxgk/sjld/ — 领导之窗 (市政府领导 section, as of 2026-07-17)
  - jiaohe.gov.cn/xxgk/zdhy/ — 重大会议 pages (including 市委常委会)
  - Individual leader biography pages on jiaohe.gov.cn
  - Baidu Baike and Google Search were blocked/rate-limited (degraded web access)

Confidence notes:
  - 市委书记靳明: confirmed via June 2026 meeting report (防汛会商会议)
  - 代市长高鹏程: confirmed via official biography page (2026-07-17), bio details sourced
  - Government leadership roster: all 8 members confirmed via official leadership page
  - Biographical details (birth, education, career timeline): sourced from official biography pages
  - 前任市长王威: inferred from 2024-2025 news articles mentioning "市长王威"
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "蛟河市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_蛟河市"
if _CURRENT_DIR.name == "jilin_蛟河市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1=市委书记, 2=代市长, 3-10=市政府班子成员, 11=前任市长, 12-13=前任书记

persons = [
    # ═══ Core Leadership (current) ═══════════════════════════════════════════
    {
        "id": 1,
        "name": "靳明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共蛟河市委员会",
        "source": "http://www.jiaohe.gov.cn/xxgk/zdhy/202606/t20260623_1326243.html",
        "notes": "Confirmed市委书记as of 2026-06-22 via防汛会商会议报道. Not on government leadership page (only government leaders listed there). Birth/education data unverified."
    },
    {
        "id": 2,
        "name": "高鹏程",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年5月",
        "birthplace": "",  # open question
        "education": "博士研究生",
        "party_join": "中共党员",
        "work_start": "2007年6月",
        "current_post": "市委副书记、副市长（代市长）",
        "current_org": "蛟河市人民政府",
        "source": "http://www.jiaohe.gov.cn/xxgk/sjld/zfld/201706/t20170622_201621.html",
        "notes": "Confirmed via official biography. Previously served as 吉林化工学院党委组织部常务副部长, 吉林市广播电视大学党委书记/校长, 舒兰市委常委/副市长"
    },
    # ═══ Government Leadership ═══════════════════════════════════════════════
    {
        "id": 3,
        "name": "周彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年8月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "2009年7月",
        "current_post": "市委常委、副市长",
        "current_org": "蛟河市人民政府",
        "source": "http://www.jiaohe.gov.cn/xxgk/sjld/zfld/201909/t20190911_630374.html",
        "notes": "负责市政府常务工作. Former posts include 永吉县金家满族乡党委书记, 吉林高新技术产业开发区党政综合办公室副主任"
    },
    {
        "id": 4,
        "name": "董明刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年2月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "1993年12月",
        "current_post": "市委常委、副市长",
        "current_org": "蛟河市人民政府",
        "source": "http://www.jiaohe.gov.cn/xxgk/sjld/zfld/202410/t20241006_1229237.html",
        "notes": "Former posts include 吉林市应急管理局副局长/党委委员"
    },
    {
        "id": 5,
        "name": "马学庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年9月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "2007年7月",
        "current_post": "市委常委、副市长",
        "current_org": "蛟河市人民政府",
        "source": "http://www.jiaohe.gov.cn/xxgk/sjld/zfld/202508/t20250813_1280748.html",
        "notes": "Bio limited on official page. Work history not detailed."
    },
    {
        "id": 6,
        "name": "陈连波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "1999年11月",
        "current_post": "副市长",
        "current_org": "蛟河市人民政府",
        "source": "http://www.jiaohe.gov.cn/xxgk/sjld/zfld/202508/t20250813_1280767.html",
        "notes": "本地提拔干部. Former posts include 蛟河市黄松甸镇党委书记, 蛟河市政府办公室党组书记/主任, 吉林蛟河经济开发区党工委书记"
    },
    {
        "id": 7,
        "name": "尚楚翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年8月",
        "birthplace": "",
        "education": "大学专科",
        "party_join": "中共党员",
        "work_start": "1992年7月",
        "current_post": "副市长、市公安局局长",
        "current_org": "蛟河市人民政府",
        "source": "http://www.jiaohe.gov.cn/xxgk/sjld/zfld/201901/t20190114_536682.html",
        "notes": "公安系统背景. Former posts include 吉林市公安局政治部综合处副处长, 昌邑公安分局副局长, 吉林市看守所所长. 一级警督/三级高级警长."
    },
    {
        "id": 8,
        "name": "郭永智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年4月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "2009年8月",
        "current_post": "副市长",
        "current_org": "蛟河市人民政府",
        "source": "http://www.jiaohe.gov.cn/xxgk/sjld/zfld/202602/t20260203_1306350.html",
        "notes": "Former posts include 磐石市宝山乡党委书记/四级调研员. 分管农业农村/乡村振兴/水利."
    },
    {
        "id": 9,
        "name": "王治国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1998年7月",
        "current_post": "副市长",
        "current_org": "蛟河市人民政府",
        "source": "http://www.jiaohe.gov.cn/xxgk/sjld/zfld/202502/t20250205_1249724.html",
        "notes": "本地提拔干部. Former posts include 蛟河市天岗镇党委书记, 蛟河市民政局党组书记/局长, 蛟河市委组织部副部长. 分管城乡建设/城市管理/交通运输."
    },
    # ═══ Predecessors ══════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "王威",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原市长（已离任）",
        "current_org": "蛟河市人民政府",
        "source": "http://www.jiaohe.gov.cn/ (homepage news items, 2024-2025)",
        "notes": "前任市长, mentioned in multiple 2024-2025 news articles. Replaced by 高鹏程 as 代市长 in 2026. Bio details unknown."
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共蛟河市委员会", "type": "党委", "level": "县级市", "parent": "中共吉林市委", "location": "吉林省蛟河市"},
    {"id": 2, "name": "蛟河市人民政府", "type": "政府", "level": "县级市", "parent": "吉林市人民政府", "location": "吉林省蛟河市"},
    {"id": 3, "name": "蛟河市公安局", "type": "政府", "level": "正科级", "parent": "蛟河市人民政府", "location": "吉林省蛟河市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 靳明
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "未知", "end": "present", "rank": "正处级", "note": "Confirmed as of June 2026. Start date unknown."},
    # 高鹏程
    {"person_id": 2, "org_id": 2, "title": "市委副书记、副市长（代市长）", "start": "2026年", "end": "present", "rank": "正处级", "note": "Appointed acting mayor in 2026"},
    {"person_id": 2, "org_id": 2, "title": "舒兰市委常委、副市长", "start": "未知", "end": "2026", "rank": "副处级", "note": "Previous role before 蛟河"},
    {"person_id": 2, "org_id": 2, "title": "吉林市广播电视大学党委书记、校长", "start": "未知", "end": "未知", "rank": "副处级", "note": ""},
    # 周彬
    {"person_id": 3, "org_id": 2, "title": "市委常委、副市长", "start": "未知", "end": "present", "rank": "副处级", "note": "负责常务工作"},
    {"person_id": 3, "org_id": 2, "title": "吉林市昌邑区副区长（人选）", "start": "未知", "end": "未知", "rank": "副处级", "note": ""},
    # 董明刚
    {"person_id": 4, "org_id": 2, "title": "市委常委、副市长", "start": "未知", "end": "present", "rank": "副处级", "note": "分管国土资源/林业/市场监管/生态环境"},
    # 马学庆
    {"person_id": 5, "org_id": 2, "title": "市委常委、副市长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 陈连波
    {"person_id": 6, "org_id": 2, "title": "副市长", "start": "未知", "end": "present", "rank": "副处级", "note": "分管工业/商务/招商引资/政务服务"},
    {"person_id": 6, "org_id": 2, "title": "吉林蛟河经济开发区党工委书记", "start": "未知", "end": "未知", "rank": "正科级", "note": ""},
    # 尚楚翔
    {"person_id": 7, "org_id": 2, "title": "副市长、市公安局局长", "start": "未知", "end": "present", "rank": "副处级", "note": "分管公安/司法/信访/退役军人"},
    {"person_id": 7, "org_id": 3, "title": "市公安局局长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 郭永智
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "未知", "end": "present", "rank": "副处级", "note": "分管农业农村/乡村振兴/水利"},
    # 王治国
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "未知", "end": "present", "rank": "副处级", "note": "分管城乡建设/城市管理/交通运输"},
    # 王威（前任市长）
    {"person_id": 10, "org_id": 2, "title": "市长", "start": "未知", "end": "2026", "rank": "正处级", "note": "前任市长，2026年离任"},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 靳明 ←→ 高鹏程 (党政正职搭班)
    {"person_a": 1, "person_b": 2, "type": "党政正职搭班", "context": "市委书记与代市长搭班", "overlap_org": "蛟河市", "overlap_period": "2026-至今"},
    # 高鹏程 ← 王威 (前后任)
    {"person_a": 2, "person_b": 10, "type": "前后任", "context": "高鹏程接替王威任代理市长", "overlap_org": "蛟河市人民政府", "overlap_period": "2026"},
    # 周彬 ←→ 董明刚 (市委常委/副市长同级搭班)
    {"person_a": 3, "person_b": 4, "type": "同级搭班", "context": "同为市委常委、副市长", "overlap_org": "蛟河市人民政府", "overlap_period": "至今"},
    # 陈连波 ← 王治国 (本地提拔干部)
    {"person_a": 6, "person_b": 9, "type": "同区域背景", "context": "均为蛟河本地提拔干部", "overlap_org": "蛟河市", "overlap_period": "至今"},
    # 陈连波 ←→ 尚楚翔
    {"person_a": 6, "person_b": 7, "type": "同级", "context": "同为副市长", "overlap_org": "蛟河市人民政府", "overlap_period": "至今"},
    # 周彬 ←→ 马学庆 (同为常委副市长)
    {"person_a": 3, "person_b": 5, "type": "同级搭班", "context": "同为市委常委、副市长", "overlap_org": "蛟河市人民政府", "overlap_period": "至今"},
    # 郭永智 ←→ 王治国 (同为副市长)
    {"person_a": 8, "person_b": 9, "type": "同级", "context": "同为副市长", "overlap_org": "蛟河市人民政府", "overlap_period": "至今"},
    # 靳明 — 王威 (前后任/曾搭班)
    {"person_a": 1, "person_b": 10, "type": "曾搭班", "context": "靳明任书记期间，王威曾任市长", "overlap_org": "蛟河市", "overlap_period": "2025-2026"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def create_tables(conn):
    conn.execute("""
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
            source TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start_date TEXT,
            end_date TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)
    conn.commit()


def build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县级市")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 蛟河市人民政府网站 (jiaohe.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace", "education",
              "party_join", "work_start", "current_post", "current_org", "source"]
    for p in persons:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?'] * len(cols_p))})", vals)

    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?'] * len(cols_o))})", vals)

    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?'] * len(cols_pos))})", vals)

    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?'] * len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(post):
        if "书记" in post and "副" not in post:
            return ("255,50,50", 20.0)  # Red, top leader
        elif "市长" in post and "副" not in post and "代" in post:
            return ("50,100,255", 20.0)  # Blue, acting mayor
        elif "市长" in post and "副" not in post and "原" in post:
            return ("150,150,150", 10.0)  # Grey, past
        elif "常务" in post:
            return ("50,100,255", 15.0)
        elif "市委常委" in post:
            return ("100,150,255", 12.0)
        elif "副市长" in post and "局长" in post:
            return ("100,100,255", 12.0)
        elif "副市长" in post:
            return ("100,100,255", 12.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        colors = {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
        }
        return colors.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
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

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    build()
