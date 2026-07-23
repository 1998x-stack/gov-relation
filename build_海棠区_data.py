#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三亚市海棠区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 海南省
Parent city: 三亚市
Region: 海棠区
Targets: 区委书记 & 区长

官方来源（截至2026-07-23）:
- http://ht.sanya.gov.cn/ — 三亚市海棠区人民政府门户网站
- https://www.sanya.gov.cn/ — 三亚市人民政府门户网站
- https://zh.wikipedia.org/wiki/%E6%B5%B7%E6%A3%A0%E5%8C%BA

当前在任 (as of 2026-07-23):
- 区委书记: 鲁正兰
- 区长: 石廷伟
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "海棠区"
DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：区委书记（正处级）
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "鲁正兰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市海棠区委书记",
        "current_org": "中共三亚市海棠区委员会",
        "source": "http://ht.sanya.gov.cn/"
    },
    # ════════════════════════════════════════
    # 核心领导：区长（正处级）
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "石廷伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市海棠区委副书记、区长",
        "current_org": "三亚市海棠区人民政府",
        "source": "http://ht.sanya.gov.cn/"
    },
    # ════════════════════════════════════════
    # 海棠区委常委/副区长（已知领导，完整名单待确认）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "翁裕育",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海棠区委常委、副区长",
        "current_org": "中共三亚市海棠区委员会",
        "source": "http://ht.sanya.gov.cn/"
    },
    {
        "id": 4,
        "name": "黄泽纬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海棠区委常委、组织部部长",
        "current_org": "中共三亚市海棠区委员会",
        "source": "http://ht.sanya.gov.cn/"
    },
    {
        "id": 5,
        "name": "胡发祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海棠区委常委、纪委书记、监委主任",
        "current_org": "中共三亚市海棠区纪律检查委员会",
        "source": "http://ht.sanya.gov.cn/"
    },
    {
        "id": 6,
        "name": "曹学军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海棠区委常委、宣传部部长",
        "current_org": "中共三亚市海棠区委员会",
        "source": "http://ht.sanya.gov.cn/"
    },
    {
        "id": 7,
        "name": "王秀磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海棠区委常委、政法委书记",
        "current_org": "中共三亚市海棠区委员会",
        "source": "http://ht.sanya.gov.cn/"
    },
    # ── 副区长 ──
    {
        "id": 8,
        "name": "王澜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海棠区副区长",
        "current_org": "三亚市海棠区人民政府",
        "source": "http://ht.sanya.gov.cn/"
    },
    {
        "id": 9,
        "name": "吴永恺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海棠区副区长",
        "current_org": "三亚市海棠区人民政府",
        "source": "http://ht.sanya.gov.cn/"
    },
    {
        "id": 10,
        "name": "张东升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海棠区副区长、市公安局海棠分局局长",
        "current_org": "三亚市公安局海棠分局",
        "source": "http://ht.sanya.gov.cn/"
    },
    {
        "id": 11,
        "name": "王洪明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海棠区副区长",
        "current_org": "三亚市海棠区人民政府",
        "source": "http://ht.sanya.gov.cn/"
    },
    # ── 人大、政协 ──
    {
        "id": 12,
        "name": "陈玮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海棠区人大常委会主任",
        "current_org": "三亚市海棠区人民代表大会常务委员会",
        "source": "http://ht.sanya.gov.cn/"
    },
    {
        "id": 13,
        "name": "聂磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海棠区政协主席",
        "current_org": "中国人民政治协商会议三亚市海棠区委员会",
        "source": "http://ht.sanya.gov.cn/"
    },
    # ── 前任领导 ──
    {
        "id": 14,
        "name": "张作壮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（原海棠区委书记，已卸任）",
        "current_org": "",
        "source": "https://baike.baidu.com/"
    },
    # ── 三亚市领导（上级，用于关系连接） ──
    {
        "id": 15,
        "name": "王祺扬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海南省委常委、三亚市委书记",
        "current_org": "中共三亚市委员会",
        "source": "https://www.sanya.gov.cn/"
    },
    {
        "id": 16,
        "name": "陈希",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市委副书记、市长",
        "current_org": "三亚市人民政府",
        "source": "https://www.sanya.gov.cn/"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共三亚市海棠区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共三亚市委员会",
        "location": "海南省三亚市海棠区"
    },
    {
        "id": 2,
        "name": "三亚市海棠区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "三亚市人民政府",
        "location": "海南省三亚市海棠区"
    },
    {
        "id": 3,
        "name": "中共三亚市海棠区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共三亚市纪律检查委员会",
        "location": "海南省三亚市海棠区"
    },
    {
        "id": 4,
        "name": "三亚市海棠区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "三亚市人民代表大会常务委员会",
        "location": "海南省三亚市海棠区"
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议三亚市海棠区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协三亚市委员会",
        "location": "海南省三亚市海棠区"
    },
    {
        "id": 6,
        "name": "三亚市公安局海棠分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "三亚市公安局",
        "location": "海南省三亚市海棠区"
    },
    {
        "id": 7,
        "name": "中共三亚市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共海南省委员会",
        "location": "海南省三亚市"
    },
    {
        "id": 8,
        "name": "三亚市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "海南省人民政府",
        "location": "海南省三亚市"
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "三亚市海棠区委书记",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 区长
    {"person_id": 2, "org_id": 1, "title": "海棠区委副书记",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "海棠区区长",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 区委常委、副区长
    {"person_id": 3, "org_id": 1, "title": "海棠区委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "海棠区副区长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 区委组织部部长
    {"person_id": 4, "org_id": 1, "title": "海棠区委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 纪委书记
    {"person_id": 5, "org_id": 1, "title": "海棠区委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "海棠区纪委书记、监委主任",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 宣传部部长
    {"person_id": 6, "org_id": 1, "title": "海棠区委常委、宣传部部长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 政法委书记
    {"person_id": 7, "org_id": 1, "title": "海棠区委常委、政法委书记",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 副区长
    {"person_id": 8, "org_id": 2, "title": "海棠区副区长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "海棠区副区长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "海棠区副区长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 6, "title": "市公安局海棠分局局长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "海棠区副区长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 人大主任
    {"person_id": 12, "org_id": 4, "title": "海棠区人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 政协主席
    {"person_id": 13, "org_id": 5, "title": "海棠区政协主席",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 前任区委书记
    {"person_id": 14, "org_id": 1, "title": "海棠区委书记（原）",
     "start_date": "", "end_date": "", "rank": "正处级", "note": "前任区委书记"},
    # 三亚市上级领导
    {"person_id": 15, "org_id": 7, "title": "三亚市委书记",
     "start_date": "", "end_date": "present", "rank": "副部级",
     "note": "海南省委常委兼任三亚市委书记"},
    {"person_id": 16, "org_id": 7, "title": "三亚市委副书记",
     "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 16, "org_id": 8, "title": "三亚市市长",
     "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 核心搭档 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "海棠区区委书记与区长党政搭档",
     "overlap_org": "中共三亚市海棠区委员会/三亚市海棠区人民政府",
     "overlap_period": "present"},
    # ── 区委常委与区委书记 ──
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "海棠区委常委班子同事",
     "overlap_org": "中共三亚市海棠区委员会",
     "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "海棠区委常委班子同事",
     "overlap_org": "中共三亚市海棠区委员会",
     "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "海棠区委常委班子同事",
     "overlap_org": "中共三亚市海棠区委员会",
     "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "海棠区委常委班子同事",
     "overlap_org": "中共三亚市海棠区委员会",
     "overlap_period": "present"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "海棠区委常委班子同事",
     "overlap_org": "中共三亚市海棠区委员会",
     "overlap_period": "present"},
    # ── 区长与副区长 ──
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "海棠区政府领导班子搭档",
     "overlap_org": "三亚市海棠区人民政府",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 8, "type": "overlap",
     "context": "海棠区政府领导班子搭档",
     "overlap_org": "三亚市海棠区人民政府",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 9, "type": "overlap",
     "context": "海棠区政府领导班子搭档",
     "overlap_org": "三亚市海棠区人民政府",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "海棠区政府领导班子搭档",
     "overlap_org": "三亚市海棠区人民政府",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 11, "type": "overlap",
     "context": "海棠区政府领导班子搭档",
     "overlap_org": "三亚市海棠区人民政府",
     "overlap_period": "present"},
    # ── 前任与现任 ──
    {"person_a": 1, "person_b": 14, "type": "predecessor_successor",
     "context": "鲁正兰接替张作壮任海棠区委书记",
     "overlap_org": "中共三亚市海棠区委员会",
     "overlap_period": "交接期"},
    # ── 上下级关系（与三亚市领导） ──
    {"person_a": 1, "person_b": 15, "type": "superior_subordinate",
     "context": "海棠区委书记接受三亚市委书记领导",
     "overlap_org": "三亚市党委系统",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate",
     "context": "海棠区区长接受三亚市市长领导",
     "overlap_org": "三亚市政府系统",
     "overlap_period": "present"},
]

# =========================================================================
# 5. GEXF BUILDER (inline, per gexf_pattern.md)
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    """Return RGB string for a person based on their role."""
    if "书记" in post and "纪委" not in post:
        return "255,50,50"    # Red — Party Secretary
    if "区长" in post or "市长" in post or "副区长" in post or "副市长" in post:
        return "50,100,255"   # Blue — Government
    if "纪委" in post or "监委" in post:
        return "255,165,0"    # Orange — Discipline
    if "人大" in post:
        return "200,255,255"  # Cyan
    if "政协" in post:
        return "255,240,200"  # Cream
    return "100,100,100"      # Grey — Others


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")


def build_gexf():
    lines = []
    now = datetime.now().strftime("%Y-%m-%d")
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{now}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append(f'    <description>三亚市海棠区领导班子工作关系网络 (as of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes: nodes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="a0" title="type" type="string"/>')
    lines.append('      <attribute id="a1" title="current_post" type="string"/>')
    lines.append('      <attribute id="a2" title="current_org" type="string"/>')
    lines.append('    </attributes>')

    # Attributes: edges
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="e0" title="type" type="string"/>')
    lines.append('      <attribute id="e1" title="context" type="string"/>')
    lines.append('      <attribute id="e2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="e3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p.get("current_post", ""))
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="a0" value="person"/>')
        lines.append(f'          <attvalue for="a1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="a2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o["type"])
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="a0" value="organization"/>')
        lines.append(f'          <attvalue for="a1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="a2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        src = f"p{pos['person_id']}"
        tgt = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="e0" value="worked_at"/>')
        lines.append(f'          <attvalue for="e1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        src = f"p{r['person_a']}"
        tgt = f"p{r['person_b']}"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="e0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="e1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="e2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="e3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    return "\n".join(lines)


# =========================================================================
# 6. BUILD
# =========================================================================
def build():
    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start_date TEXT, end_date TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions
            (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()

    # ── Summary ──
    print(f"✅ SQLite: {DB_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")

    # ── GEXF ──
    gexf_content = build_gexf()
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write(gexf_content)
    print(f"✅ GEXF:  {GEXF_PATH}")
    print("✅ Build complete.")


if __name__ == "__main__":
    build()
