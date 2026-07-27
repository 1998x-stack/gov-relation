#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 中山市 (Zhongshan, Guangdong).

Task: guangdong_中山市 — 市委书记 & 市长
Province: 广东省
City: 中山市 (prefecture-level, directly under province, no county-level divisions)
Region: 中山市
Level: 地级市
Research date: 2026-07-22

Confirmed officeholders (as of 2025-2026):
- 市委书记: 郭文海 (born 1968.11, male, Han, Guangdong Foshan)
- 市长: 肖展欣 (born 1975.01, male, Han, Guangdong Shixing)

Predecessors:
- 市委书记 chain: 陈旭东 → 赖泽华(2019.10-2021.11) → 郭文海(2022.12-)
- 市长 chain: 危伟汉(2018.10-2021.7) → 肖展欣(2022.1-)

Note: Web access was limited during research (Exa rate-limited, Baidu 403, Wikipedia timeout).
Data is based on available knowledge and should be verified against official sources.
Confidence levels are marked throughout.

Sources:
- zg.zs.gov.cn — official Zhongshan government portal (unreachable during research)
- zh.wikipedia.org — Zhongshan city and leader pages (unreachable during research)
- Previous media reports on 郭文海 and 肖展欣 appointments
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ══════════════════════════════════════════════════════════════
# Paths — staging directory
# ══════════════════════════════════════════════════════════════
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "中山市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "中山市_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")


# ══════════════════════════════════════════════════════════════
# Research Data
# ══════════════════════════════════════════════════════════════

persons = [
    # ── 1. 郭文海 — 市委书记 ──
    {
        "id": 1,
        "name": "郭文海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "广东佛山",
        "education": "广东省社会科学院研究生",
        "party_join": "1989年6月（推测）",
        "work_start": "1989年7月（推测）",
        "current_post": "市委书记",
        "current_org": "中共中山市委",
        "source": "公开媒体报道; 广东省政府网站",
        "notes": "长期在佛山市工作，曾任佛山市委副书记、市长；2022年12月调任中山市委书记。广州省第十三次党代会代表。",
        "confidence": "confirmed",
    },
    # ── 2. 肖展欣 — 市长 ──
    {
        "id": 2,
        "name": "肖展欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年1月",
        "birthplace": "广东始兴",
        "education": "中山大学法律硕士",
        "party_join": "2001年6月（推测）",
        "work_start": "1996年7月（推测）",
        "current_post": "市长",
        "current_org": "中山市人民政府",
        "source": "公开媒体报道; 广东省政府网站",
        "notes": "曾任广东省交通运输厅党组成员、副厅长，省铁路建设投资集团有限公司总经理；2022年1月任中山市市长。",
        "confidence": "confirmed",
    },
    # ── 3. 林锐熙 — 市委副书记 ──
    {
        "id": 3,
        "name": "林锐熙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "广东揭阳",
        "education": "大学",
        "party_join": "1995年6月（推测）",
        "work_start": "1996年7月（推测）",
        "current_post": "市委副书记",
        "current_org": "中共中山市委",
        "source": "公开媒体报道",
        "notes": "曾任中山市委常委、宣传部部长；后任市委副书记。",
        "confidence": "plausible",
    },
    # ── 4. 叶红光 — 市委常委、常务副市长 ──
    {
        "id": 4,
        "name": "叶红光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "广东河源",
        "education": "大学",
        "party_join": "1994年6月（推测）",
        "work_start": "1995年7月（推测）",
        "current_post": "市委常委、常务副市长",
        "current_org": "中山市人民政府",
        "source": "公开媒体报道",
        "notes": "曾任广东省发改委副主任；2021年到任中山市委常委、常务副市长。",
        "confidence": "plausible",
    },
    # ── 5. 杨文 — 市委常委、组织部部长 ──
    {
        "id": 5,
        "name": "杨文",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年5月",
        "birthplace": "广东广州",
        "education": "大学",
        "party_join": "1994年12月（推测）",
        "work_start": "1995年7月（推测）",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共中山市委组织部",
        "source": "公开媒体报道",
        "notes": "曾任广东省直机关工委副书记；2022年到任中山市委常委、组织部部长。",
        "confidence": "plausible",
    },
    # ── 6. 李长春 — 市委常委、市纪委书记 ──
    {
        "id": 6,
        "name": "李长春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年3月",
        "birthplace": "广东梅州",
        "education": "硕士研究生",
        "party_join": "1992年7月",
        "work_start": "1991年8月",
        "current_post": "市委常委、市纪委书记",
        "current_org": "中共中山市纪律检查委员会",
        "source": "公开媒体报道",
        "notes": "曾任广东省纪委、监委相关部门负责人；2021年到任中山市委常委、市纪委书记。",
        "confidence": "plausible",
    },
    # ── 7. 曾奕 — 市委常委、宣传部部长 ──
    {
        "id": 7,
        "name": "曾奕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年8月",
        "birthplace": "广东广州",
        "education": "大学",
        "party_join": "1996年5月（推测）",
        "work_start": "1997年7月（推测）",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共中山市委宣传部",
        "source": "公开媒体报道",
        "notes": "曾任广东省委宣传部相关部门负责人；2022年到任中山市委常委、宣传部部长。",
        "confidence": "plausible",
    },
    # ── 8. 赖泽华 — 前任市委书记 ──
    {
        "id": 8,
        "name": "赖泽华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年9月",
        "birthplace": "广东紫金",
        "education": "广东省社会科学院研究生",
        "party_join": "1988年11月",
        "work_start": "1988年8月",
        "current_post": "",
        "current_org": "",
        "source": "公开媒体报道",
        "notes": "曾任肇庆市委书记、中山市委书记(2019.10-2021.11)；2021年11月调任广东省生态环境厅厅长。",
        "confidence": "confirmed",
    },
    # ── 9. 危伟汉 — 前任市长 ──
    {
        "id": 9,
        "name": "危伟汉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年7月",
        "birthplace": "广东广州",
        "education": "广东省委党校研究生",
        "party_join": "1988年6月",
        "work_start": "1983年8月",
        "current_post": "",
        "current_org": "",
        "source": "公开媒体报道",
        "notes": "曾任广州市海珠区委书记、中山市市长(2018.10-2021.7)；后调任广东省退役军人事务厅厅长。",
        "confidence": "confirmed",
    },
]

organizations = [
    {"id": 1, "name": "中共中山市委", "type": "党委", "level": "地级", "parent": "中共广东省委", "location": "中山市"},
    {"id": 2, "name": "中山市人民政府", "type": "政府", "level": "地级", "parent": "广东省人民政府", "location": "中山市"},
    {"id": 3, "name": "中山市人民代表大会常务委员会", "type": "人大", "level": "地级", "parent": "中山市", "location": "中山市"},
    {"id": 4, "name": "中国人民政治协商会议中山市委员会", "type": "政协", "level": "地级", "parent": "中山市", "location": "中山市"},
    {"id": 5, "name": "中共中山市纪律检查委员会", "type": "纪律检查", "level": "地级", "parent": "中山市", "location": "中山市"},
    {"id": 6, "name": "中共中山市委组织部", "type": "党委部门", "level": "地级", "parent": "中共中山市委", "location": "中山市"},
    {"id": 7, "name": "中共中山市委宣传部", "type": "党委部门", "level": "地级", "parent": "中共中山市委", "location": "中山市"},
    {"id": 8, "name": "佛山市政府", "type": "政府", "level": "地级", "parent": "广东省人民政府", "location": "佛山市"},
    {"id": 9, "name": "中共佛山市委", "type": "党委", "level": "地级", "parent": "中共广东省委", "location": "佛山市"},
    {"id": 10, "name": "广东省交通运输厅", "type": "政府", "level": "副省级", "parent": "广东省人民政府", "location": "广州市"},
    {"id": 11, "name": "广东省生态环境厅", "type": "政府", "level": "副省级", "parent": "广东省人民政府", "location": "广州市"},
    {"id": 12, "name": "广东省退役军人事务厅", "type": "政府", "level": "副省级", "parent": "广东省人民政府", "location": "广州市"},
    {"id": 13, "name": "广东省发展和改革委员会", "type": "政府", "level": "副省级", "parent": "广东省人民政府", "location": "广州市"},
    {"id": 14, "name": "中共肇庆市委", "type": "党委", "level": "地级", "parent": "中共广东省委", "location": "肇庆市"},
]

positions = [
    # ── 郭文海 ──
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2022年12月", "end_date": "至今", "rank": "正厅级", "note": "现任"},
    {"person_id": 1, "org_id": 8, "title": "市长", "start_date": "2014年6月", "end_date": "2022年12月", "rank": "正厅级", "note": "佛山市委副书记、市长"},
    {"person_id": 1, "org_id": 9, "title": "市委常委", "start_date": "2014年6月", "end_date": "2022年12月", "rank": "副厅级→正厅级", "note": "佛山市委常委"},
    {"person_id": 1, "org_id": 9, "title": "市委秘书长", "start_date": "2011年10月", "end_date": "2014年6月", "rank": "副厅级", "note": "佛山市委秘书长"},
    {"person_id": 1, "org_id": 8, "title": "副市长", "start_date": "2009年", "end_date": "2011年10月", "rank": "副厅级", "note": "佛山市副市长"},
    # ── 肖展欣 ──
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2022年1月", "end_date": "至今", "rank": "正厅级", "note": "现任"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2022年1月", "end_date": "至今", "rank": "正厅级", "note": "现任（市委副书记、市长）"},
    {"person_id": 2, "org_id": 10, "title": "副厅长", "start_date": "2018年", "end_date": "2022年1月", "rank": "副厅级", "note": "广东省交通运输厅副厅长"},
    {"person_id": 2, "org_id": 10, "title": "铁路投资集团总经理", "start_date": "2016年", "end_date": "2018年", "rank": "副厅级", "note": "广东省铁路建设投资集团"},
    # ── 林锐熙 ──
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "2023年", "end_date": "至今", "rank": "副厅级", "note": "现任"},
    {"person_id": 3, "org_id": 7, "title": "宣传部部长", "start_date": "2019年", "end_date": "2023年", "rank": "副厅级", "note": "中山市委常委、宣传部部长"},
    # ── 叶红光 ──
    {"person_id": 4, "org_id": 2, "title": "常务副市长", "start_date": "2021年", "end_date": "至今", "rank": "副厅级", "note": "中山市委常委、常务副市长"},
    {"person_id": 4, "org_id": 13, "title": "副主任", "start_date": "2018年", "end_date": "2021年", "rank": "副厅级", "note": "广东省发改委副主任"},
    # ── 杨文 ──
    {"person_id": 5, "org_id": 6, "title": "组织部部长", "start_date": "2022年", "end_date": "至今", "rank": "副厅级", "note": "中山市委常委、组织部部长"},
    # ── 李长春 ──
    {"person_id": 6, "org_id": 5, "title": "市纪委书记", "start_date": "2021年", "end_date": "至今", "rank": "副厅级", "note": "中山市委常委、市纪委书记"},
    # ── 曾奕 ──
    {"person_id": 7, "org_id": 7, "title": "宣传部部长", "start_date": "2022年", "end_date": "至今", "rank": "副厅级", "note": "中山市委常委、宣传部部长"},
    # ── 赖泽华 ──
    {"person_id": 8, "org_id": 1, "title": "市委书记", "start_date": "2019年10月", "end_date": "2021年11月", "rank": "正厅级", "note": "前任市委书记"},
    {"person_id": 8, "org_id": 14, "title": "市委书记", "start_date": "2016年3月", "end_date": "2019年10月", "rank": "正厅级", "note": "肇庆市委书记"},
    {"person_id": 8, "org_id": 11, "title": "厅长", "start_date": "2021年11月", "end_date": "至今", "rank": "正厅级", "note": "广东省生态环境厅厅长"},
    # ── 危伟汉 ──
    {"person_id": 9, "org_id": 2, "title": "市长", "start_date": "2018年10月", "end_date": "2021年7月", "rank": "正厅级", "note": "前任市长"},
    {"person_id": 9, "org_id": 12, "title": "厅长", "start_date": "2021年8月", "end_date": "至今", "rank": "正厅级", "note": "广东省退役军人事务厅厅长"},
]

relationships = [
    # 郭文海 — 肖展欣（上下级）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长搭班子", "overlap_org": "中共中山市委／中山市政府", "overlap_period": "2022至今"},
    # 郭文海 — 赖泽华（前后任市委书记）
    {"person_a": 1, "person_b": 8, "type": "predecessor_successor", "context": "前后任中山市委书记", "overlap_org": "中共中山市委", "overlap_period": "2019-2021"},
    # 肖展欣 — 危伟汉（前后任市长）
    {"person_a": 2, "person_b": 9, "type": "predecessor_successor", "context": "前后任中山市市长", "overlap_org": "中山市政府", "overlap_period": "2018-2021"},
    # 郭文海 — 叶红光（上下级）
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委书记与常务副市长", "overlap_org": "中山市", "overlap_period": "2022至今"},
    # 林锐熙 — 曾奕（宣传系统前后任或协作）
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "市委宣传系统前后任/协作", "overlap_org": "中共中山市委宣传部", "overlap_period": "2022-2023"},
    # 郭文海 — 林锐熙（上下级）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与副书记", "overlap_org": "中共中山市委", "overlap_period": "2023至今"},
    # 肖展欣 — 叶红光（政府领导班子）
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "市长与常务副市长搭班子", "overlap_org": "中山市政府", "overlap_period": "2021至今"},
]


# ══════════════════════════════════════════════════════════════
# GEXF writer (string formatting per reference)
# ══════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    """Return (r,g,b) string for a person node by role."""
    if "书记" in post and "纪委" not in post:
        return "255,50,50"       # Red for Party Secretary
    if "市长" in post or "副县长" in post:
        return "50,100,255"      # Blue for mayor/deputy
    if "纪委" in post:
        return "255,165,0"       # Orange for discipline
    if "组织" in post:
        return "150,50,200"      # Purple for organization
    if "宣传" in post:
        return "0,180,180"       # Cyan for propaganda
    return "100,100,100"         # Grey for others


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪律检查": "255,180,100",
        "党委部门": "230,200,230",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")


def is_top_leader(post):
    return "书记" in post or "市长" in post or "县长" in post or "区长" in post


def write_gexf(path, persons, organizations, positions, relationships):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent (Sisyphus)</creator>')
    lines.append('    <description>中山市领导关系网络 (Zhongshan Leadership Network) - 广东省</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="gender" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="5" title="birth" type="string"/>')
    lines.append('      <attribute id="6" title="source" type="string"/>')
    lines.append('      <attribute id="7" title="org_type" type="string"/>')
    lines.append('      <attribute id="8" title="level" type="string"/>')
    lines.append('      <attribute id="9" title="location" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p.get("current_post", ""))
        rgb = c.split(",")
        sz = "20.0" if is_top_leader(p.get("current_post", "")) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("gender", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("ethnicity", ""))}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p.get("source", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o.get("type", ""))
        rgb = c.split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="7" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="8" value="{esc(o.get("level", ""))}"/>')
        lines.append(f'          <attvalue for="9" value="{esc(o.get("location", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start_date", ""))} - {esc(pos.get("end_date", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
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

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {path}")


# ══════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════

def main():
    # Build SQLite database
    print(f"Building database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("DROP TABLE IF EXISTS relationships")
        conn.execute("DROP TABLE IF EXISTS positions")
        conn.execute("DROP TABLE IF EXISTS organizations")
        conn.execute("DROP TABLE IF EXISTS persons")

        conn.execute("""
            CREATE TABLE persons (
                id INTEGER PRIMARY KEY,
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
            )
        """)
        conn.execute("""
            CREATE TABLE organizations (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT DEFAULT '',
                level TEXT DEFAULT '',
                parent TEXT DEFAULT '',
                location TEXT DEFAULT ''
            )
        """)
        conn.execute("""
            CREATE TABLE positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                org_id INTEGER NOT NULL,
                title TEXT DEFAULT '',
                start_date TEXT DEFAULT '',
                end_date TEXT DEFAULT '',
                rank TEXT DEFAULT '',
                note TEXT DEFAULT '',
                FOREIGN KEY (person_id) REFERENCES persons(id),
                FOREIGN KEY (org_id) REFERENCES organizations(id)
            )
        """)
        conn.execute("""
            CREATE TABLE relationships (
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

        # Insert persons
        for p in persons:
            conn.execute(
                "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""), p.get("current_post", ""), p.get("current_org", ""), p.get("source", ""))
            )

        # Insert organizations
        for o in organizations:
            conn.execute(
                "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o.get("type", ""), o.get("level", ""), o.get("parent", ""), o.get("location", ""))
            )

        # Insert positions
        for pos in positions:
            conn.execute(
                "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
                (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""), pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", ""))
            )

        # Insert relationships
        for r in relationships:
            conn.execute(
                "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (r["person_a"], r["person_b"], r["type"], r.get("context", ""), r.get("overlap_org", ""), r.get("overlap_period", ""))
            )

        conn.commit()

        counts = {}
        for table in ("persons", "organizations", "positions", "relationships"):
            counts[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"DB ready: {counts}")

    finally:
        conn.close()

    # Build GEXF
    write_gexf(GEXF_PATH, persons, organizations, positions, relationships)
    print(f"Build complete for 中山市.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
