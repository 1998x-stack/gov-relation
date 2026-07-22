#!/usr/bin/env python3
"""Build script for 武隆区 (Wulong District, Chongqing) — Leadership Network Database & GEXF Graph.

Sources:
  - Official government website: https://www.cqwl.gov.cn/zwgk_170/ldxx_45782/qzfld/
  - Wulong District news articles (July 2026)
  - Baidu Baike (encyclopedia)

Confidence legend: confirmed (official source), plausible (media/encyclopedia), unverified (lead)
"""

import os
import sqlite3
from datetime import datetime

TODAY = datetime.now().strftime("%Y-%m-%d")
STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "武隆区_network.db")
GEXF_PATH = os.path.join(STAGING, "武隆区_network.gexf")

# ── DATA ────────────────────────────────────────────────────────────────

persons = [
    {
        "id": "wulong_fan_lixin",
        "name": "范立新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共重庆市武隆区委",
        "source": "https://www.cqwl.gov.cn/zwxx_170/wldt/t_15807157.html",
        "notes": "2026年7月确认为武隆区委书记；履历待查",
        "confidence": "confirmed",
    },
    {
        "id": "wulong_wei_xinggui",
        "name": "魏兴贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年8月",
        "birthplace": "",
        "native_place": "",
        "education": "医学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "重庆市武隆区人民政府",
        "source": "https://www.cqwl.gov.cn/zwgk_170/ldxx_45782/qzfld/qz/wxg/202511/t20251121_15178232.html",
        "notes": "1974年8月出生，医学学士学位",
        "confidence": "confirmed",
    },
    {
        "id": "wulong_liu_gaoyong",
        "name": "刘高永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年8月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长（常务）",
        "current_org": "重庆市武隆区人民政府",
        "source": "https://www.cqwl.gov.cn/zwgk_170/ldxx_45782/qzfld/fqz/lgy_47291/201701/t20170111_6145061.html",
        "notes": "1973年8月出生，研究生学历；负责区政府常务工作",
        "confidence": "confirmed",
    },
    {
        "id": "wulong_ma_yinghua",
        "name": "马应华",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1973年10月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "重庆市武隆区人民政府",
        "source": "https://www.cqwl.gov.cn/zwgk_170/ldxx_45782/qzfld/fqz/myh/",
        "notes": "1973年10月出生，苗族，研究生学历",
        "confidence": "confirmed",
    },
    {
        "id": "wulong_liu_guihu",
        "name": "刘桂虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共重庆市武隆区委",
        "source": "https://www.cqwl.gov.cn/zwxx_170/wldt/t_15807157.html",
        "notes": "区委常委，具体职务待查（可能为组织部长或政法委书记）",
        "confidence": "confirmed",
    },
    {
        "id": "wulong_wang_chunrui",
        "name": "王春瑞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "重庆市武隆区人民政府",
        "source": "https://www.cqwl.gov.cn/zwgk_170/ldxx_45782/qzfld/",
        "notes": "挂职副区长",
        "confidence": "confirmed",
    },
    {
        "id": "wulong_zhang_yong",
        "name": "张永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "重庆市武隆区人民政府",
        "source": "https://www.cqwl.gov.cn/zwgk_170/ldxx_45782/qzfld/",
        "notes": "副区长",
        "confidence": "confirmed",
    },
    {
        "id": "wulong_he_shengchun",
        "name": "何圣春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "重庆市武隆区人民政府",
        "source": "https://www.cqwl.gov.cn/zwgk_170/ldxx_45782/qzfld/",
        "notes": "副区长",
        "confidence": "confirmed",
    },
    {
        "id": "wulong_liu_zhuang",
        "name": "刘壮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "重庆市武隆区人民政府",
        "source": "https://www.cqwl.gov.cn/zwgk_170/ldxx_45782/qzfld/",
        "notes": "副区长",
        "confidence": "confirmed",
    },
    {
        "id": "wulong_zeng_yuan",
        "name": "曾媛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "重庆市武隆区人民政府",
        "source": "https://www.cqwl.gov.cn/zwgk_170/ldxx_45782/qzfld/",
        "notes": "副区长",
        "confidence": "confirmed",
    },
    {
        "id": "wulong_yuan_ding",
        "name": "袁丁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "重庆市武隆区人民政府",
        "source": "https://www.cqwl.gov.cn/zwgk_170/ldxx_45782/qzfld/",
        "notes": "副区长",
        "confidence": "confirmed",
    },
    {
        "id": "wulong_qin_lin",
        "name": "覃琳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "重庆市武隆区人民政府",
        "source": "https://www.cqwl.gov.cn/zwgk_170/ldxx_45782/qzfld/",
        "notes": "副区长",
        "confidence": "confirmed",
    },
    {
        "id": "wulong_gao_guanpeng",
        "name": "高冠鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "重庆市武隆区人民政府",
        "source": "https://www.cqwl.gov.cn/zwgk_170/ldxx_45782/qzfld/",
        "notes": "挂职副区长",
        "confidence": "confirmed",
    },
    {
        "id": "wulong_gao_bo",
        "name": "高博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府党组成员（挂职）",
        "current_org": "重庆市武隆区人民政府",
        "source": "https://www.cqwl.gov.cn/zwgk_170/ldxx_45782/qzfld/",
        "notes": "挂职区政府党组成员",
        "confidence": "confirmed",
    },
    # Predecessors
    {
        "id": "wulong_he_qing",
        "name": "何庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "",
        "source": "公开新闻报道",
        "notes": "前任武隆区委书记；2023-2024年左右离任；去向待确认",
        "confidence": "plausible",
    },
]

organizations = [
    {
        "id": "org_cqwl_party",
        "name": "中共重庆市武隆区委",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共重庆市委",
        "location": "重庆市武隆区",
    },
    {
        "id": "org_cqwl_gov",
        "name": "重庆市武隆区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "重庆市人民政府",
        "location": "重庆市武隆区",
    },
    {
        "id": "org_cqwl_discipline",
        "name": "中共重庆市武隆区纪律检查委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共重庆市武隆区委",
        "location": "重庆市武隆区",
    },
    {
        "id": "org_cqwl_police",
        "name": "重庆市武隆区公安局",
        "type": "政府",
        "level": "市辖区",
        "parent": "重庆市武隆区人民政府",
        "location": "重庆市武隆区",
    },
]

positions = [
    # 范立新 - 区委书记
    {"person_id": "wulong_fan_lixin", "org_id": "org_cqwl_party", "title": "区委书记", "start": "~2024", "end": "present", "rank": "正厅级", "note": "2026年7月仍在任"},
    # 魏兴贵 - 区长
    {"person_id": "wulong_wei_xinggui", "org_id": "org_cqwl_gov", "title": "区长", "start": "", "end": "present", "rank": "正厅级", "note": "区政府党组书记"},
    {"person_id": "wulong_wei_xinggui", "org_id": "org_cqwl_party", "title": "区委副书记", "start": "", "end": "present", "rank": "", "note": "区委副书记"},
    # 刘高永 - 常务副区长
    {"person_id": "wulong_liu_gaoyong", "org_id": "org_cqwl_gov", "title": "副区长（常务）", "start": "", "end": "present", "rank": "副厅级", "note": "负责区政府常务工作"},
    {"person_id": "wulong_liu_gaoyong", "org_id": "org_cqwl_party", "title": "区委常委", "start": "", "end": "present", "rank": "", "note": "区委常委"},
    # 马应华
    {"person_id": "wulong_ma_yinghua", "org_id": "org_cqwl_gov", "title": "副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "wulong_ma_yinghua", "org_id": "org_cqwl_party", "title": "区委常委", "start": "", "end": "present", "rank": "", "note": "区委常委"},
    # 刘桂虎
    {"person_id": "wulong_liu_guihu", "org_id": "org_cqwl_party", "title": "区委常委", "start": "", "end": "present", "rank": "", "note": "具体职务待查"},
    # 副区长们
    {"person_id": "wulong_wang_chunrui", "org_id": "org_cqwl_gov", "title": "副区长（挂职）", "start": "", "end": "present", "rank": "副厅级", "note": "挂职"},
    {"person_id": "wulong_zhang_yong", "org_id": "org_cqwl_gov", "title": "副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "wulong_he_shengchun", "org_id": "org_cqwl_gov", "title": "副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "wulong_liu_zhuang", "org_id": "org_cqwl_gov", "title": "副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "wulong_zeng_yuan", "org_id": "org_cqwl_gov", "title": "副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "wulong_yuan_ding", "org_id": "org_cqwl_gov", "title": "副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "wulong_qin_lin", "org_id": "org_cqwl_gov", "title": "副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "wulong_gao_guanpeng", "org_id": "org_cqwl_gov", "title": "副区长（挂职）", "start": "", "end": "present", "rank": "副厅级", "note": "挂职"},
    {"person_id": "wulong_gao_bo", "org_id": "org_cqwl_gov", "title": "区政府党组成员（挂职）", "start": "", "end": "present", "rank": "副厅级", "note": "挂职"},
    # 何庆 - 前任
    {"person_id": "wulong_he_qing", "org_id": "org_cqwl_party", "title": "区委书记（前任）", "start": "~2021", "end": "~2024", "rank": "正厅级", "note": "前任区委书记，去向待确认"},
]

relationships = [
    # 范立新 ↔ 魏兴贵（党政一把手）
    {"person_a": "wulong_fan_lixin", "person_b": "wulong_wei_xinggui", "type": "党政一把手", "context": "2024年至今在武隆区担任区委书记和区长搭档", "overlap_org": "中共重庆市武隆区委", "overlap_period": "2024年至今", "strength": "strong", "confidence": "confirmed"},
    # 魏兴贵 ↔ 刘高永（正副区长）
    {"person_a": "wulong_wei_xinggui", "person_b": "wulong_liu_gaoyong", "type": "正副区长", "context": "区长与常务副区长日常工作关系", "overlap_org": "重庆市武隆区人民政府", "overlap_period": "", "strength": "strong", "confidence": "confirmed"},
    # 刘高永 ↔ 马应华（同为区委常委、副区长）
    {"person_a": "wulong_liu_gaoyong", "person_b": "wulong_ma_yinghua", "type": "区委常委同事", "context": "同为区委常委、副区长", "overlap_org": "中共重庆市武隆区委", "overlap_period": "", "strength": "strong", "confidence": "confirmed"},
    # 范立新 ↔ 刘桂虎
    {"person_a": "wulong_fan_lixin", "person_b": "wulong_liu_guihu", "type": "上下级", "context": "区委书记与区委常委", "overlap_org": "中共重庆市武隆区委", "overlap_period": "", "strength": "strong", "confidence": "confirmed"},
    # 范立新 → 何庆（前任-继任）
    {"person_a": "wulong_he_qing", "person_b": "wulong_fan_lixin", "type": "前任继任", "context": "何庆为前任武隆区委书记，范立新继任", "overlap_org": "中共重庆市武隆区委", "overlap_period": "交接期", "strength": "medium", "confidence": "plausible"},
    # 其他副区长同事关系（确认的同事）
    {"person_a": "wulong_zhang_yong", "person_b": "wulong_he_shengchun", "type": "同事", "context": "同为武隆区副区长", "overlap_org": "重庆市武隆区人民政府", "overlap_period": "", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "wulong_liu_zhuang", "person_b": "wulong_zeng_yuan", "type": "同事", "context": "同为武隆区副区长", "overlap_org": "重庆市武隆区人民政府", "overlap_period": "", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "wulong_yuan_ding", "person_b": "wulong_qin_lin", "type": "同事", "context": "同为武隆区副区长", "overlap_org": "重庆市武隆区人民政府", "overlap_period": "", "strength": "medium", "confidence": "confirmed"},
]


# ── HELPERS ─────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p.get("current_post", "")
    if "书记" in post and "区委" in post:
        return "255,50,50"   # red — party secretary
    if "区长" in post or "县长" in post:
        return "50,100,255"  # blue — government leader
    if "纪委书记" in post:
        return "255,165,0"   # orange — discipline
    if "人大" in post or "政协" in post:
        return "100,180,100" # green — congress/CPPCC
    return "100,100,100"     # grey — others


def is_top_leader(p):
    post = p.get("current_post", "")
    return "区委书记" in post or "区长" in post


def org_color(o):
    t = o["type"]
    if "党委" in t:
        return "255,200,200"  # pink
    if "政府" in t:
        return "200,200,255"  # light blue
    if "人大" in t:
        return "200,255,255"  # cyan
    if "政协" in t:
        return "255,240,200"  # cream
    return "200,200,200"


# ── BUILD FUNCTIONS ─────────────────────────────────────────────────────

def build_db():
    """Create SQLite database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                                 native_place, education, party_join, work_start,
                                 current_post, current_org, source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
            p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
            p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
            p.get("current_post", ""), p.get("current_org", ""),
            p.get("source", ""), p.get("notes", ""), p.get("confidence", ""),
        ))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pos["person_id"], pos["org_id"], pos["title"],
            pos.get("start", ""), pos.get("end", ""),
            pos.get("rank", ""), pos.get("note", ""),
        ))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context,
                                       overlap_org, overlap_period, strength)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            r["person_a"], r["person_b"], r["type"], r.get("context", ""),
            r.get("overlap_org", ""), r.get("overlap_period", ""), r.get("strength", ""),
        ))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def build_gexf():
    """Create GEXF graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>武隆区 (Wulong District, Chongqing) — Leadership Network Graph</description>')
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
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    persons_map = {p["id"]: p for p in persons}

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person edges
    for r in relationships:
        weight = "2.0" if r.get("strength") == "strong" else "1.5" if r.get("strength") == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("strength", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[GEXF] Created: {GEXF_PATH}")
    print(f"[GEXF] Nodes: {len(persons)} persons + {len(organizations)} orgs")
    print(f"[GEXF] Edges: {len(positions)} worked_at + {len(relationships)} relationships")


def main():
    os.makedirs(STAGING, exist_ok=True)
    build_db()
    build_gexf()

    # Summary
    print(f"\n{'=' * 50}")
    print(f"武隆区 Leadership Network — Build Complete")
    print(f"{'=' * 50}")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"\nOutput files:")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
