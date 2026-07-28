#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 吉首市 (Jishou City).

Task ID: hunan_吉首市
Level: 县级市
Province: 湖南省
Parent city: 湘西土家族苗族自治州
Targets: 市委书记 & 市长

Data sourced from:
- 中国经济网 (周立志任湘西州委常委、吉首市委书记): http://district.ce.cn/newarea/sddy/202310/17/t20231017_38752737.shtml
- 红网 (符家盛当选吉首市长): https://hn.rednet.cn/content/2020/05/27/7294146.html
- 百度百科 (周立志): https://baike.baidu.com/item/%E5%91%A8%E7%AB%8B%E5%BF%97/9534894
- 百度百科 (符家盛): https://baike.baidu.com/item/%E7%AC%A6%E5%AE%B6%E7%9B%9B
- 维基百科 (吉首市): https://zh.wikipedia.org/wiki/%E5%90%89%E9%A6%96%E5%B8%82
- 维基百科 (吉首市人民政府): https://zh.wikipedia.org/wiki/%E5%90%89%E9%A6%96%E5%B8%82%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C
- 维基百科 (中国共产党吉首市委员会): https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E5%90%89%E9%A6%96%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A
- 澎湃新闻: https://www.thepaper.cn/newsDetail_forward_24958167
- 三湘风纪网: https://www.sxfj.gov.cn/shen_cha_diao_cha/zhi_ji_shen_cha/222262696.shtml
- 湖南省政府网: http://www.hunan.gov.cn/topic/2025slh/yqd/ybg1/202501/t20250116_33566268.html
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for pc in [2, 3, 4, 5]:
    c = Path(__file__).resolve().parents[pc]
    if (c / "gov_relation").is_dir():
        REPO_ROOT = c
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "吉首市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-28"

# ── Staging paths ────────────────────────────────────────────────────
_CURRENT = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_吉首市"
STAGING = _CURRENT if _CURRENT.name == "hunan_吉首市" else _STAGING_CANDIDATE
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ══════════════════════════════════════════════════════════════════════
# RAW DATA
# ══════════════════════════════════════════════════════════════════════

P = lambda s: f"js_{s}"

# --- Persons ---
persons = [
    # ═══ Current top leaders ═══
    # 市委书记: 周立志 (since 2023-10)
    {
        "id": P("zhou_lizhi"), "name": "周立志", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-05", "birthplace": "湖南省永州市",
        "education": "大学本科（湘潭大学中共党史专业）",
        "party_join": "1998-03", "work_start": "2000-07",
        "current_post": "湘西州委常委、吉首市委书记", "current_org": "中共吉首市委员会",
        "source": "https://baike.baidu.com/item/%E5%91%A8%E7%AB%8B%E5%BF%97/9534894",
        "note": "兼吉首市人武部党委第一书记"
    },
    # 市长: 张俊 (since 2025-12, replaced 符家盛)
    {
        "id": P("zhang_jun"), "name": "张俊", "gender": "男", "ethnicity": "汉族",
        "birth": "1986-03", "birthplace": "湖南省岳阳市",
        "education": "博士研究生（工学）",
        "party_join": "", "work_start": "",
        "current_post": "吉首市委副书记、市长", "current_org": "吉首市人民政府",
        "source": "https://baike.baidu.com/item/%E5%BC%A0%E4%BF%8A/16647275"
    },
    # 前任市长: 符家盛 (2020-05 ~ 2025-09, 现为新晃县委书记)
    {
        "id": P("fu_jiasheng"), "name": "符家盛", "gender": "男", "ethnicity": "苗族",
        "birth": "1973-04", "birthplace": "湖南省龙山县",
        "education": "大学（省委党校选调生班）",
        "party_join": "1995-03", "work_start": "1996-06",
        "current_post": "新晃侗族自治县委书记", "current_org": "中共新晃侗族自治县委员会",
        "source": "https://hn.rednet.cn/content/2020/05/27/7294146.html"
    },

    # ═══ Other four-bānzi leaders ═══
    {
        "id": P("fu_qiyin"), "name": "符启银", "gender": "男", "ethnicity": "",
        "birth": "1969-01", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "市人大常委会主任", "current_org": "吉首市人大常委会",
        "source": "https://zh.wikipedia.org/wiki/%E5%90%89%E9%A6%96%E5%B8%82"
    },
    {
        "id": P("xiang_hongqiong"), "name": "向洪琼", "gender": "女", "ethnicity": "",
        "birth": "1969-05", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "市政协主席", "current_org": "政协吉首市委员会",
        "source": "https://zh.wikipedia.org/wiki/%E5%90%89%E9%A6%96%E5%B8%82"
    },

    # ═══ Predecessors ═══
    {
        "id": P("li_shixing"), "name": "李诗兴", "gender": "男", "ethnicity": "土家族",
        "birth": "1975-01", "birthplace": "湖南省泸溪县",
        "education": "在职研究生",
        "party_join": "", "work_start": "",
        "current_post": "前任吉首市委书记（被查）", "current_org": "",
        "source": "https://www.thepaper.cn/newsDetail_forward_25100644"
    },
    {
        "id": P("liu_zhenyu"), "name": "刘珍瑜", "gender": "男", "ethnicity": "土家族",
        "birth": "1970-08", "birthplace": "湖南省石门县",
        "education": "在职研究生学历，硕士学位",
        "party_join": "1996-12", "work_start": "1992-07",
        "current_post": "前任吉首市委书记（已双开）", "current_org": "",
        "source": "https://www.thepaper.cn/newsDetail_forward_24708986"
    },
]

# --- Organizations ---
organizations = [
    {"id": P("shiwei"), "name": "中共吉首市委员会", "type": "county_party", "level": "county", "parent": "湘西州委", "location": "吉首市"},
    {"id": P("zhengfu"), "name": "吉首市人民政府", "type": "county_gov", "level": "county", "parent": "湘西州政府", "location": "吉首市"},
    {"id": P("renda"), "name": "吉首市人大常委会", "type": "npc", "level": "county", "parent": "湘西州人大", "location": "吉首市"},
    {"id": P("zhengxie"), "name": "政协吉首市委员会", "type": "cppcc", "level": "county", "parent": "湘西州政协", "location": "吉首市"},
]

# --- Positions (person -> org) ---
positions = [
    # Current top leaders
    {"pid": P("zhou_lizhi"), "oid": P("shiwei"), "title": "湘西州委常委、吉首市委书记", "start": "2023-10", "end": "", "rank": "副厅级（州委常委）"},
    {"pid": P("zhang_jun"), "oid": P("zhengfu"), "title": "吉首市委副书记、市长", "start": "2025-12", "end": "", "rank": "正处级"},
    {"pid": P("fu_jiasheng"), "oid": P("zhengfu"), "title": "吉首市委副书记、市长", "start": "2020-05", "end": "2025-09", "rank": "正处级"},

    # Four-baozi
    {"pid": P("fu_qiyin"), "oid": P("renda"), "title": "市人大常委会主任", "start": "2021-10", "end": "", "rank": "正处级"},
    {"pid": P("xiang_hongqiong"), "oid": P("zhengxie"), "title": "市政协主席", "start": "2021-10", "end": "", "rank": "正处级"},

    # Predecessors - party secretaries
    {"pid": P("li_shixing"), "oid": P("shiwei"), "title": "吉首市委书记", "start": "2020-04", "end": "2023-08", "rank": "正处级"},
    {"pid": P("liu_zhenyu"), "oid": P("shiwei"), "title": "吉首市委书记", "start": "2014-05", "end": "2020-04", "rank": "正处级"},

    # Predecessor also served as mayor
    {"pid": P("li_shixing"), "oid": P("zhengfu"), "title": "吉首市市长", "start": "2015-12", "end": "2020-04", "rank": "正处级"},
]

# --- Relationships (person <-> person) ---
relationships = [
    # Current colleagues
    {"a": P("zhou_lizhi"), "b": P("zhang_jun"), "type": "colleague",
     "context": "周立志（市委）与张俊（市政府）搭班", "org": P("shiwei"), "period": "2025-12起"},
    {"a": P("zhou_lizhi"), "b": P("fu_jiasheng"), "type": "colleague",
     "context": "周立志（市委）与符家盛（市政府）搭班", "org": P("shiwei"), "period": "2023-10至2025-09"},

    # Predecessor-successor chains for party secretary
    {"a": P("liu_zhenyu"), "b": P("li_shixing"), "type": "predecessor_successor",
     "context": "刘珍瑜2020年4月卸任后李诗兴接任吉首市委书记", "org": P("shiwei"), "period": "2020-04"},
    {"a": P("li_shixing"), "b": P("zhou_lizhi"), "type": "predecessor_successor",
     "context": "李诗兴2023年8月卸任后周立志接任吉首市委书记", "org": P("shiwei"), "period": "2023-10"},

    # Predecessor-successor chains for mayor
    {"a": P("li_shixing"), "b": P("fu_jiasheng"), "type": "predecessor_successor",
     "context": "李诗兴2015-2020任市长后符家盛接任吉首市长", "org": P("zhengfu"), "period": "2020-04"},

    # Colleague relationships (predecessors)
    {"a": P("liu_zhenyu"), "b": P("li_shixing"), "type": "superior_subordinate",
     "context": "刘珍瑜（书记）与李诗兴（市长）搭班约5年", "org": P("shiwei"), "period": "2015-12至2020-04"},
    {"a": P("li_shixing"), "b": P("fu_jiasheng"), "type": "superior_subordinate",
     "context": "李诗兴（书记）与符家盛（市长）搭班约3年", "org": P("shiwei"), "period": "2020-04至2023-08"},

    # Integrity risk connection
    {"a": P("liu_zhenyu"), "b": P("li_shixing"), "type": "reported_association",
     "context": "刘珍瑜（2023.03被查/双开）与李诗兴（2023.10被查）先后落马，吉首连续两任市委书记被查", "org": P("shiwei"), "period": "2023"},
]

# ══════════════════════════════════════════════════════════════════════
# BUILD SQLite
# ══════════════════════════════════════════════════════════════════════

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE persons (id TEXT PRIMARY KEY, name TEXT NOT NULL, gender TEXT, ethnicity TEXT, birth TEXT, birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT, current_post TEXT, current_org TEXT, source TEXT);
CREATE TABLE organizations (id TEXT PRIMARY KEY, name TEXT NOT NULL, type TEXT, level TEXT, parent TEXT, location TEXT);
CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT, person_id TEXT, org_id TEXT, title TEXT, start TEXT, end TEXT, rank TEXT, FOREIGN KEY (person_id) REFERENCES persons(id), FOREIGN KEY (org_id) REFERENCES organizations(id));
CREATE TABLE relationships (id INTEGER PRIMARY KEY AUTOINCREMENT, person_a TEXT, person_b TEXT, type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT, FOREIGN KEY (person_a) REFERENCES persons(id), FOREIGN KEY (person_b) REFERENCES persons(id));
""")

for org in organizations:
    c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
              (org["id"], org["name"], org["type"], org["level"], org["parent"], org["location"]))

for p in persons:
    c.execute("INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
               p["education"], p["party_join"], p["work_start"],
               p["current_post"], p["current_org"], p["source"]))

for pos in positions:
    c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank) VALUES (?,?,?,?,?,?)",
              (pos["pid"], pos["oid"], pos["title"], pos["start"], pos["end"] or None, pos["rank"]))

for r in relationships:
    c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
              (r["a"] if isinstance(r.get("a"), str) else r.get("id", ""),
               r["b"] if isinstance(r.get("b"), str) else "",
               r["type"], r["context"], r["org"] or None, r["period"] or None))

conn.commit()
conn.close()
print(f"SQLite DB: {DB_PATH}")

# ══════════════════════════════════════════════════════════════════════
# BUILD GEXF
# ══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    post = p["current_post"]
    if "书记" in post: return "255,50,50"
    if "市长" in post or "主任" in post: return "50,100,255"
    if "主席" in post: return "180,100,180"
    if "前任" in post: return "150,150,150"
    return "100,100,100"

def org_color(o):
    t = o["type"]
    if "party" in t: return "255,200,200"
    if "gov" in t: return "200,200,255"
    if "npc" in t: return "200,255,255"
    if "cppcc" in t: return "255,240,200"
    return "200,200,200"

def node_size(p):
    post = p["current_post"]
    if "市委书记" in post: return 20.0
    if "市长" in post: return 16.0
    if "主任" in post or "主席" in post: return 12.0
    return 10.0

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
         '  <meta>',
         '    <creator>gov-relation investigator</creator>',
         f'    <description>吉首市领导班子工作关系网络 (updated {TODAY})</description>',
         f'    <date>{TODAY}</date>',
         '  </meta>',
         '  <graph mode="static" defaultedgetype="undirected">',
         '    <attributes class="node">',
         '      <attribute id="type" title="Type" type="string"/>',
         '      <attribute id="role" title="Role" type="string"/>',
         '      <attribute id="birth" title="Birth" type="string"/>',
         '      <attribute id="birthplace" title="Birthplace" type="string"/>',
         '      <attribute id="current_post" title="Current Post" type="string"/>',
         '      <attribute id="source" title="Source" type="string"/>',
         '    </attributes>',
         '    <attributes class="edge">',
         '      <attribute id="type" title="Type" type="string"/>',
         '      <attribute id="context" title="Context" type="string"/>',
         '      <attribute id="period" title="Period" type="string"/>',
         '    </attributes>',
         '    <nodes>']
for p in persons:
    c_str = person_color(p)
    sz = node_size(p)
    rgb = c_str.split(",")
    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues><attvalue for="type" value="person"/><attvalue for="role" value="{esc(p["current_post"])}"/><attvalue for="birth" value="{esc(p["birth"])}"/><attvalue for="birthplace" value="{esc(p["birthplace"])}"/><attvalue for="current_post" value="{esc(p["current_post"])}"/><attvalue for="source" value="{esc(p["source"])}"/></attvalues>')
    lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'        <viz:shape value="disc"/>')
    lines.append(f'      </node>')
for o in organizations:
    c_str = org_color(o)
    rgb = c_str.split(",")
    lines.append(f'      <node id="{o["id"]}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues><attvalue for="type" value="organization"/><attvalue for="role" value="{esc(o["type"])}"/><attvalue for="current_post" value=""/><attvalue for="source" value=""/></attvalues>')
    lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'        <viz:shape value="square"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    end_s = pos["end"] or "今"
    lines.append(f'      <edge id="e{eid}" source="{pos["pid"]}" target="{pos["oid"]}" type="directed">')
    lines.append(f'        <attvalues><attvalue for="type" value="worked_at"/><attvalue for="context" value="{esc(pos["title"])} ({esc(pos["start"])}~{esc(end_s)})"/><attvalue for="period" value="{esc(pos["start"])}~{esc(end_s)}"/></attvalues>')
    lines.append(f'        <viz:color r="180" g="180" b="180"/><viz:thickness value="1.0"/>')
    lines.append(f'      </edge>')
for r in relationships:
    eid += 1
    a = r["a"] if isinstance(r["a"], str) else r.get("id", "")
    b = r["b"] if isinstance(r["b"], str) else r.get("id", "")
    lines.append(f'      <edge id="e{eid}" source="{a}" target="{b}">')
    lines.append(f'        <attvalues><attvalue for="type" value="{esc(r["type"])}"/><attvalue for="context" value="{esc(r["context"])}"/><attvalue for="period" value="{esc(r["period"])}"/></attvalues>')
    if r["type"] in ("colleague", "superior_subordinate"):
        lines.append(f'        <viz:color r="201" g="169" b="78"/><viz:thickness value="2.5"/>')
    else:
        lines.append(f'        <viz:color r="100" g="150" b="255"/><viz:thickness value="1.5"/>')
    lines.append(f'      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"GEXF graph: {GEXF_PATH}")

print(f"\nSummary: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")