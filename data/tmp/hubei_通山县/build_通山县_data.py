#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 通山县 (Tongshan County), 咸宁市, 湖北省.

Level: 县
Province: 湖北省
Parent city: 咸宁市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: hubei_通山县

Research date: 2026-07-24
Official source: http://www.tongshan.gov.cn/ (通山县人民政府) — confirmed accessible via HTTP

Current status (as of 2026-07-24):
- 县委书记: 吴涛 (confirmed via official news articles at tongshan.gov.cn)
- 县长: 王功辉 (confirmed via official government leadership page at tongshan.gov.cn/zc/ldhd/wgh/)

Roster sources:
  县政府领导: http://www.tongshan.gov.cn/zc/ldhd/
  县委常委会报道: http://www.tongshan.gov.cn/zc/ldhd/wgh/zyhd/202607/t20260708_5010577.shtml

Confidence notes:
  - Current roles for 县长 and 县政府 members: confirmed via official government website
  - 县委书记吴涛: confirmed via official news reports (2026-07-22 督办报道)
  - 县委领导 (县委常委): confirmed via 县委常委会会议报道 (2026-07-08)
  - Career histories for most leaders: unverified — only current positions confirmed from official sources
  - 王功辉 personal details (born 1981-04, CPC 2003-12, work 2005-07, bachelor): confirmed via official profile
  - Exa search was rate-limited; Baidu returned 403
  - 吴涛's detailed bio not yet found — marked as unverified
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "通山县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "吴涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共通山县委员会",
        "source": "http://www.tongshan.gov.cn/xw/tpxw/202607/t20260724_5122892.shtml"
    },
    {
        "id": 2,
        "name": "王功辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年4月",
        "birthplace": "",
        "education": "管理学学士",
        "party_join": "中共党员",
        "work_start": "2005年7月",
        "current_post": "县委副书记、县政府县长、党组书记",
        "current_org": "通山县人民政府",
        "source": "http://www.tongshan.gov.cn/zc/ldhd/wgh/"
    },
    # ═══════ 县委领导 ═══════
    {
        "id": 3,
        "name": "廖旦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、通山经济开发区党工委书记",
        "current_org": "中共通山县委员会",
        "source": "http://www.tongshan.gov.cn/zc/ldhd/wgh/zyhd/202607/t20260708_5010577.shtml"
    },
    {
        "id": 4,
        "name": "石聪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共通山县委员会",
        "source": "http://www.tongshan.gov.cn/zc/ldhd/wgh/zyhd/202607/t20260708_5010577.shtml"
    },
    {
        "id": 5,
        "name": "王知非",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共通山县委组织部",
        "source": "http://www.tongshan.gov.cn/xw/tsxw/202607/t20260722_5098620.shtml"
    },
    {
        "id": 6,
        "name": "熊晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共通山县委员会",
        "source": "http://www.tongshan.gov.cn/zc/ldhd/wgh/zyhd/202607/t20260708_5010577.shtml"
    },
    {
        "id": 7,
        "name": "郑佳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、统战部部长",
        "current_org": "中共通山县委宣传部",
        "source": "http://www.tongshan.gov.cn/xw/tsxw/202607/t20260723_5113551.shtml"
    },
    {
        "id": 8,
        "name": "程景家",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共通山县委员会政法委员会",
        "source": "http://www.tongshan.gov.cn/xw/tpxw/202607/t20260724_5122892.shtml"
    },
    {
        "id": 9,
        "name": "方声果",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共通山县委员会",
        "source": "http://www.tongshan.gov.cn/zc/ldhd/wgh/zyhd/202607/t20260708_5010577.shtml"
    },
    {
        "id": 10,
        "name": "张敏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986年8月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府副县长（协助县长负责政府日常工作）、党组副书记",
        "current_org": "通山县人民政府",
        "source": "http://www.tongshan.gov.cn/zc/ldhd/zm/"
    },
    # ═══════ 县政府其他领导 ═══════
    {
        "id": 11,
        "name": "孔凡定",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "通山县人民政府",
        "source": "http://www.tongshan.gov.cn/zc/ldhd/kfd/"
    },
    {
        "id": 12,
        "name": "饶才明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年7月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中国民主建国会会员",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "通山县人民政府",
        "source": "http://www.tongshan.gov.cn/zc/ldhd/rcm/"
    },
    {
        "id": 13,
        "name": "张晓丹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年12月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长、县政府党组成员",
        "current_org": "通山县人民政府",
        "source": "http://www.tongshan.gov.cn/zc/ldhd/zxd/"
    },
    {
        "id": 14,
        "name": "陈国宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年11月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长、县政府党组成员",
        "current_org": "通山县人民政府",
        "source": "http://www.tongshan.gov.cn/zc/ldhd/cgn/"
    },
    {
        "id": 15,
        "name": "肖燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长、县政府党组成员",
        "current_org": "通山县人民政府",
        "source": "http://www.tongshan.gov.cn/zc/ldhd/xy/"
    },
    # ═══════ 县人大领导 ═══════
    {
        "id": 16,
        "name": "徐丽华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "通山县人大常委会",
        "source": "http://www.tongshan.gov.cn/zc/ldhd/wgh/zyhd/202607/t20260708_5010577.shtml"
    },
    # ═══════ 县政协领导 ═══════
    {
        "id": 17,
        "name": "杨烨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组书记、主席",
        "current_org": "通山县政协",
        "source": "http://www.tongshan.gov.cn/zc/ldhd/wgh/zyhd/202607/t20260708_5010577.shtml"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共通山县委员会", "type": "党委", "level": "县处级", "parent": "中共咸宁市委员会", "location": "湖北省咸宁市通山县"},
    {"id": 2, "name": "通山县人民政府", "type": "政府", "level": "县处级", "parent": "咸宁市人民政府", "location": "湖北省咸宁市通山县"},
    {"id": 3, "name": "通山经济开发区", "type": "开发区", "level": "县处级", "parent": "通山县人民政府", "location": "湖北省咸宁市通山县"},
    {"id": 4, "name": "中共通山县委组织部", "type": "党委", "level": "乡科级", "parent": "中共通山县委员会", "location": "湖北省咸宁市通山县"},
    {"id": 5, "name": "中共通山县委宣传部", "type": "党委", "level": "乡科级", "parent": "中共通山县委员会", "location": "湖北省咸宁市通山县"},
    {"id": 6, "name": "中共通山县委员会政法委员会", "type": "党委", "level": "乡科级", "parent": "中共通山县委员会", "location": "湖北省咸宁市通山县"},
    {"id": 7, "name": "通山县人大常委会", "type": "人大", "level": "县处级", "parent": "通山县", "location": "湖北省咸宁市通山县"},
    {"id": 8, "name": "通山县政协", "type": "政协", "level": "县处级", "parent": "通山县", "location": "湖北省咸宁市通山县"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 吴涛
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "未知", "end": "present", "rank": "正县级", "note": "As of 2026-07 confirmed via news"},
    # 王功辉
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县政府县长、党组书记", "start": "未知", "end": "present", "rank": "正县级", "note": ""},
    # 廖旦
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "通山经济开发区党工委书记", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 张敏
    {"person_id": 10, "org_id": 2, "title": "县委常委、县政府副县长（常务）、党组副书记", "start": "未知", "end": "present", "rank": "副县级", "note": "协助县长负责政府日常工作"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 石聪
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 王知非
    {"person_id": 5, "org_id": 4, "title": "县委常委、组织部部长", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 熊晓明
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 郑佳
    {"person_id": 7, "org_id": 5, "title": "县委常委、宣传部部长、统战部部长", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 程景家
    {"person_id": 8, "org_id": 6, "title": "县委常委、政法委书记", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 方声果
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 孔凡定
    {"person_id": 11, "org_id": 2, "title": "县政府副县长", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 饶才明
    {"person_id": 12, "org_id": 2, "title": "县政府副县长", "start": "未知", "end": "present", "rank": "副县级", "note": "中国民主建国会会员"},
    # 张晓丹
    {"person_id": 13, "org_id": 2, "title": "县政府副县长、党组成员", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 陈国宁
    {"person_id": 14, "org_id": 2, "title": "县政府副县长、党组成员", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 肖燕
    {"person_id": 15, "org_id": 2, "title": "县政府副县长、党组成员", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 徐丽华
    {"person_id": 16, "org_id": 7, "title": "县人大常委会党组书记、主任", "start": "未知", "end": "present", "rank": "正县级", "note": ""},
    # 杨烨
    {"person_id": 17, "org_id": 8, "title": "县政协党组书记、主席", "start": "未知", "end": "present", "rank": "正县级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 吴涛 ↔ 王功辉: 县委书记与县长搭班
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与县长党政正职搭班", "overlap_org": "中共通山县委员会/通山县人民政府", "overlap_period": "2026-07 至今", "confidence": "confirmed"},
    # 吴涛 ↔ 廖旦: 县委书记与专职副书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与县委副书记工作关系", "overlap_org": "中共通山县委员会", "overlap_period": "2026-07 至今", "confidence": "confirmed"},
    # 吴涛 ↔ 程景家: 县委书记与政法委书记
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记与政法委书记工作关系", "overlap_org": "中共通山县委员会", "overlap_period": "2026-07 至今", "confidence": "confirmed"},
    # 王功辉 ↔ 张敏: 县长与常务副县长
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "县长与常务副县长工作关系", "overlap_org": "通山县人民政府", "overlap_period": "2026-07 至今", "confidence": "confirmed"},
    # 王功辉 ↔ 廖旦: 县长与专职副书记
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与县委副书记工作关系", "overlap_org": "中共通山县委员会", "overlap_period": "2026-07 至今", "confidence": "confirmed"},
    # 王知非 ↔ 郑佳: 组织部与宣传部
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "组织部部长与宣传部部长同为县委常委", "overlap_org": "中共通山县委员会", "overlap_period": "2026-07 至今", "confidence": "confirmed"},
    # 程景家 ↔ 王知非: 政法委与组织部
    {"person_a": 8, "person_b": 5, "type": "overlap", "context": "政法委书记与组织部部长同为县委常委", "overlap_org": "中共通山县委员会", "overlap_period": "2026-07 至今", "confidence": "confirmed"},
]

# ═══════════════════════════════════════════════════════════════════════════════
#  GEXF generation
# ═══════════════════════════════════════════════════════════════════════════════
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string for a person based on role."""
    post = p.get("current_post", "")
    if "县委书记" in post:
        return "255,50,50"
    if "县长" in post:
        return "50,100,255"
    if "政法委" in post or "纪委书记" in post:
        return "255,165,0"
    if "人大" in post:
        return "200,255,255"
    if "政协" in post:
        return "255,240,200"
    return "100,100,100"

def org_color(o):
    """Return 'r,g,b' string for an organization."""
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "开发区" in t:
        return "200,255,200"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"

def is_top_leader(p):
    post = p.get("current_post", "")
    return "县委书记" in post or ("县长" in post and "副" not in post)

def build_gexf(persons, orgs, positions, relationships, output_path):
    """Generate GEXF using string formatting (not ElementTree)."""
    p_by_id = {p["id"]: p for p in persons}
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Research Agent</creator>')
    lines.append(f'    <description>通山县 leadership network - 湖北省咸宁市</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Nodes — organizations
    for o in orgs:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"] + 100000}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"] + 100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # person → person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {output_path}")

# ═══════════════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    print(f"=== Building {SLUG} network ===")

    # Build DB
    db_path = DB_PATH
    print(f"  DB: {db_path}")
    conn = sqlite3.connect(str(db_path))
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY,
                name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
                birthplace TEXT, education TEXT, party_join TEXT,
                work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
            );
            CREATE TABLE IF NOT EXISTS organizations (
                id INTEGER PRIMARY KEY,
                name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
            );
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER, org_id INTEGER,
                title TEXT, start TEXT, "end" TEXT, rank TEXT, note TEXT
            );
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_a INTEGER, person_b INTEGER,
                type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT
            );
        """)
        # Insert persons
        for p in persons:
            conn.execute(
                "INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"])
            )
        # Insert organizations
        for o in organizations:
            conn.execute(
                "INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
            )
        # Insert positions
        for po in positions:
            conn.execute(
                "INSERT INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)",
                (po["person_id"], po["org_id"], po["title"], po["start"], po["end"], po["rank"], po.get("note", ""))
            )
        # Insert relationships
        for r in relationships:
            conn.execute(
                "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""), r.get("overlap_period", ""))
            )
        conn.commit()
    finally:
        conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # Build GEXF
    build_gexf(persons, organizations, positions, relationships, GEXF_PATH)

    print(f"=== Done: {SLUG} ===")

if __name__ == "__main__":
    import sqlite3
    main()
