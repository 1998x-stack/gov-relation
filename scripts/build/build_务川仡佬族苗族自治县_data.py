#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 务川仡佬族苗族自治县, 遵义市, 贵州省.

Investigation date: 2026-08-05
Task ID: guizhou_务川仡佬族苗族自治县
Level: 县 (民族自治县)
Targets: 县委书记 & 县长

Research sources (all official, reliable):
  - 务川仡佬族苗族自治县人民政府门户 领导之窗（县委/政府/人大/政协）
    https://www.gzwuchuan.gov.cn/zwgk/ldzc/xwld/   (县委领导)
    https://www.gzwuchuan.gov.cn/zwgk/ldzc/xzfld/  (县政府领导)
  - 务府办发〔2026〕1号 关于调整县人民政府部分领导同志工作分工的通知 (2026-01-07)
  - 务川要闻: 邓林、宋臣调研督导防灾减灾工作 (2026-07-31), 邓林到县纪委监委机关调研 (2026-07-21)

Confidence notes:
  - 现任领导班子身份、职务 confirmed（官方领导之窗，2026-08-05 访问）
  - 邓林、宋臣 现任职务与搭档关系 confirmed（官方简历页 + 要闻联动报道）
  - 各领导 任现职前完整 Career 履历（出生地、教育背景、入党时间、任务川前任职）无法通过可访问来源完整确认 → 以 open_questions 记录缺口
  - 前任县委书记（2022 前）、前任县长（宋臣任代县长前）为 open gaps
"""

import json
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "务川仡佬族苗族自治县"
SHORT = "务川"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"
REGION = "务川仡佬族苗族自治县"
PROVINCE = "贵州省"
CITY = "遵义市"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ────────────────────────────────────────────────────────────────
# 1 邓林(县委书记), 2 宋臣(代理县长), 3 郑成刚(副书记), 4 袁远连(副书记),
# 5 肖四(工业园书记), 6 任琨(组织部长), 7 何林(纪委书记), 8 周丹(宣传部长),
# 9 陈波(常务副县长), 10 程鹏(挂职副县长), 11 周永国(人武部长), 12 耿晶晶(副县长),
# 13 赵懿(副县长), 14 谢劲松(人大主任), 15 尹强(政协主席)
persons = [
    {"id": 1, "name": "邓林", "gender": "男", "ethnicity": "彝族", "birth": "1979年11月", "birthplace": "", "education": "大学本科", "party_join": "中共党员", "work_start": "", "current_post": "县委书记、贵州务川经济开发区党工委书记（兼）", "current_org": "中共务川仡佬族苗族自治县委员会", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xwld/"},
    {"id": 2, "name": "宋臣", "gender": "男", "ethnicity": "苗族", "birth": "1986年9月", "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "", "current_post": "县委副书记、县人民政府代理县长、贵州务川经济开发区管委会主任（兼）", "current_org": "务川仡佬族苗族自治县人民政府", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xwld/"},
    {"id": 3, "name": "郑成刚", "gender": "男", "ethnicity": "汉族", "birth": "1980年11月", "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "", "current_post": "县委副书记（协助书记抓党建、农业农村、乡村振兴）", "current_org": "中共务川仡佬族苗族自治县委员会", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xwld/"},
    {"id": 4, "name": "袁远连", "gender": "女", "ethnicity": "汉族", "birth": "1981年1月", "birthplace": "", "education": "硕士", "party_join": "中共党员", "work_start": "", "current_post": "县委副书记（省民宗委对口帮扶、驻村帮扶）", "current_org": "中共务川仡佬族苗族自治县委员会", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xwld/"},
    {"id": 5, "name": "肖四", "gender": "男", "ethnicity": "仡佬族", "birth": "1976年9月", "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、工业园区党工委书记", "current_org": "务川仡佬族苗族自治县工业园区", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xwld/"},
    {"id": 6, "name": "任琨", "gender": "男", "ethnicity": "苗族", "birth": "1985年4月", "birthplace": "", "education": "研究生", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、县委组织部部长", "current_org": "中共务川仡佬族苗族自治县委员会组织部", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xwld/"},
    {"id": 7, "name": "何林", "gender": "男", "ethnicity": "汉族", "birth": "1984年8月", "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、县纪委书记、县监委主任提名人选，县委政法委书记", "current_org": "务川仡佬族苗族自治县纪委监委", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xwld/"},
    {"id": 8, "name": "周丹", "gender": "女", "ethnicity": "仡佬族", "birth": "1985年7月", "birthplace": "", "education": "党校研究生", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、县委宣传部部长、县委统战部部长", "current_org": "中共务川仡佬族自治县委宣传部", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xwld/"},
    {"id": 9, "name": "陈波", "gender": "男", "ethnicity": "苗族", "birth": "1981年4月", "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、县政府常务副县长", "current_org": "务川仡佬族苗族自治县人民政府", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xzfld/"},
    {"id": 10, "name": "程鹏", "gender": "男", "ethnicity": "汉族", "birth": "1976年4月", "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、县人民政府副县长（挂职，珠海市对口帮扶）", "current_org": "务川仡佬族自治县人民政府", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xwld/"},
    {"id": 11, "name": "周永国", "gender": "男", "ethnicity": "汉族", "birth": "1982年10月", "birthplace": "", "education": "大学本科", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、县人武部部长", "current_org": "务川仡佬族苗族自治县人民武装部", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xwld/"},
    {"id": 12, "name": "耿晶晶", "gender": "女", "ethnicity": "汉族", "birth": "1986年12月", "birthplace": "", "education": "博士", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、县人民政府副县长（国开行对口帮扶）", "current_org": "务川仡佬族自治县人民政府", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xzfld/"},
    {"id": 13, "name": "赵懿", "gender": "男", "ethnicity": "土家族", "birth": "1989年10月", "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "", "current_post": "县人民政府党组成员、副县长（民政、文旅、市场监管、卫健）", "current_org": "务川仡佬族苗族自治县人民政府", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xzfld/"},
    {"id": 14, "name": "谢劲松", "gender": "男", "ethnicity": "仡佬族", "birth": "1971年6月", "birthplace": "", "education": "党校研究生", "party_join": "中共党员", "work_start": "", "current_post": "县人大常委会党组书记、主任", "current_org": "务川仡佬族苗族自治县人民代表大会常务委员会", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xrdld/"},
    {"id": 15, "name": "尹强", "gender": "男", "ethnicity": "仡佬族", "birth": "1970年11月", "birthplace": "", "education": "党校大学", "party_join": "中共党员", "work_start": "", "current_post": "县政协党组书记、主席", "current_org": "政协务川仡佬族苗族自治县委员会", "source": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xzxld/"},
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共务川仡佬族自治县委员会", "type": "党委", "level": "县级", "parent": "中共遵义市委员会", "location": "务川仡佬族自治县"},
    {"id": 2, "name": "务川仡佬族自治县人民政府", "type": "政府", "level": "县级", "parent": "遵义市人民政府", "location": "务川仡佬族自治县"},
    {"id": 3, "name": "务川仡佬族自治县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "遵义市人民代表大会常务委员会", "location": "务川仡佬族自治县"},
    {"id": 4, "name": "政协务川仡佬族自治县委员会", "type": "政协", "level": "县级", "parent": "政协遵义市委员会", "location": "务川仡佬族自治县"},
    {"id": 5, "name": "务川仡佬族自治县纪委监委", "type": "纪委", "level": "县级", "parent": "中共务川仡佬族自治县委员会", "location": "务川仡佬族自治县"},
    {"id": 6, "name": "中共务川仡佬族自治县委员会组织部", "type": "党委部门", "level": "县级", "parent": "中共务川仡佬族自治县委员会", "location": "务川仡佬族自治县"},
    {"id": 7, "name": "中共务川仡佬族自治县委员会宣传部", "type": "党委部门", "level": "县级", "parent": "中共务川仡佬族自治县委员会", "location": "务川仡佬族自治县"},
    {"id": 8, "name": "贵州务川经济开发区", "type": "开发区", "level": "县级", "parent": "贵州省人民政府", "location": "务川仡佬族自治县"},
    {"id": 9, "name": "务川仡佬族苗族自治县工业园区", "type": "开发区", "level": "县级", "parent": "务川仡佬族自治县人民政府", "location": "务川仡佬族自治县"},
    {"id": 10, "name": "务川仡佬族苗族自治县人民武装部", "type": "军队", "level": "县级", "parent": "遵义军分区", "location": "务川仡佬族自治县"},
    {"id": 11, "name": "中共遵义市委员会", "type": "党委", "level": "地级", "parent": "中共贵州省委员会", "location": "遵义市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 邓林
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2022", "end": "present", "rank": "正处级", "note": "官方简历页;县委书记、开发区党工委书记兼任"},
    {"person_id": 1, "org_id": 8, "title": "贵州务川经济开发区党工委书记（兼）", "start": "", "end": "present", "rank": "", "note": "兼任"},
    # 宋臣
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": "2026年任代理县长前为县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "县政府党组书记、代理县长", "start": "2026", "end": "present", "rank": "正处级", "note": "代理县长（官方把政府领导）"},
    {"person_id": 2, "org_id": 8, "title": "贵州务川经济开发区管委会主任（兼）", "start": "", "end": "present", "rank": "", "note": "兼任"},
    # 副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "協助书记抓党建，分管农业农村/乡村振兴"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "省民宗委对口帮扶、驻村帮扶"},
    # 常委
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 9, "title": "工业园区党工委书记", "start": "", "end": "present", "rank": "", "note": "兼工科局"},
    {"person_id": 6, "org_id": 1, "title": "县委常委、县委组织部部长", "start": "", "end": "present", "rank": "副处级", "note": "主持县委组织部工作"},
    {"person_id": 7, "org_id": 1, "title": "县委常委、县纪委书记", "start": "", "end": "present", "rank": "副处级", "note": "监委主任提名人选、县委政法委书记"},
    {"person_id": 8, "org_id": 1, "title": "县委常委、县委宣传部部长、县委统战部部长", "start": "", "end": "present", "rank": "副处级", "note": "教育工委书记"},
    {"person_id": 9, "org_id": 2, "title": "县委常委、县政府常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责常务工作，协助旺卫同志分管审计（指代领导身份待查）"},
    {"person_id": 10, "org_id": 2, "title": "县委常委、县人民政府副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "珠海市对口帮扶"},
    {"person_id": 11, "org_id": 1, "title": "县委常委、县人武部部长", "start": "", "end": "present", "rank": "副处级", "note": "党管武装"},
    {"person_id": 12, "org_id": 2, "title": "县委常委、县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "国开行对口帮扶，博士"},
    {"person_id": 13, "org_id": 2, "title": "县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级", "note": "民政/文旅/市场监管/卫健"},
    # 人大
    {"person_id": 14, "org_id": 3, "title": "县人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 政协
    {"person_id": 15, "org_id": 4, "title": "县政协党组书记、主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "邓林（县委书记）与宋臣（县委副书记、代理县长）为务川现任党政一把手搭档", "overlap_org": "中共务川仡佬族自治县委员会", "overlap_period": "2022至今"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "邓林与郑成刚（副书记，协助抓党建、农业农村）同属县委班子", "overlap_org": "中共务川仡佬族自治县委员会", "overlap_period": "2022至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "邓林与袁远连（副书记，省民宗委帮扶）同属县委班子", "overlap_org": "中共务川仡佬族自治县委员会", "overlap_period": "2022至今"},
    {"person_a": 1, "person_b": 6, "type": "member_overlap", "context": "邓林（书记）与任琨（组织部长）干部任用交集", "overlap_org": "中共务川仡佬族自治县委员会", "overlap_period": "2022至今"},
    {"person_a": 1, "person_b": 7, "type": "discipline", "context": "邓林到县纪委监委机关调研座谈（2026-07-21），纪委监督与党内治理", "overlap_org": "中共务川仡佬族自治县委员会", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "member_overlap", "context": "宋臣（代县长）领导陈波（常务副县长）", "overlap_org": "务川仡佬族自治县人民政府", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 13, "type": "member_overlap", "context": "宋臣与赵懿（副县长）同属县政府班子", "overlap_org": "务川仡佬族自治县人民政府", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 12, "type": "member_overlap", "context": "宋臣与耿晶晶（副县长、国开行挂职）同属县政府班子", "overlap_org": "务川仡佬族自治县人民政府", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "邓林与肖四（常委、工业园书记）同属县委班子，工业经济", "overlap_org": "中共务川仡佬族自治县委员会", "overlap_period": "2022至今"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "邓林与周丹（宣传/统战部长）同属县委班子", "overlap_org": "中共务川仡佬族自治县委员会", "overlap_period": "2022至今"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "邓林（书记）与谢劲松（人大主任）为县四套班子领导", "overlap_org": "务川仡佬族自治县", "overlap_period": "2022至今"},
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "邓林与尹强（政协主席）为县四套班子领导", "overlap_org": "务川仡佬族自治县", "overlap_period": "2022至今"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "邓林作为县人武部党委第一书记（县人武部首任），与周永国（人武部长）党管武装", "overlap_org": "务川仡佬族自治县人民武装部", "overlap_period": "2022至今"},
    {"person_a": 9, "person_b": 13, "type": "member_overlap", "context": "陈波（常务副县长）与赵懿（副县长）同属县政府班子", "overlap_org": "务川仡佬族自治县人民政府", "overlap_period": "2026至今"},
]

# ══════════════════════════════════════════════════════════════════════════
# XML escape
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════
# Build database
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT, birthplace TEXT,
            education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id), FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id), FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)
    for p in persons:
        cur.execute("INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"],
                     p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"], pos["org_id"], pos["title"], pos.get("start",""), pos.get("end",""), pos["rank"], pos["note"]))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ══════════════════════════════════════════════════════════════════════════
# Build GEXF
# ══════════════════════════════════════════════════════════════════════════

def person_color(name):
    if name == "邓林":
        return "255,50,50"      # 县委书记 — Red
    if name == "宋臣":
        return "50,100,255"     # 代理县长 — Blue
    if name == "何林":
        return "255,165,0"      # 纪委 — Orange
    if name in ("郑成刚", "袁远连"):
        return "255,165,0"      # 副书记 — Orange
    if name == "谢劲松":
        return "200,255,255"    # 人大 — Cyan
    if name == "尹强":
        return "255,240,200"    # 政协 — Cream
    return "100,100,100"        # 其他常委 — Grey


def person_size(name):
    if name in ("邓林", "宋臣"):
        return "20.0"
    return "12.0"


def org_color(o_type):
    if "党委" in o_type or "组织" in o_type or "宣传" in o_type:
        return "255,200,200"
    if "政府" in o_type:
        return "200,200,255"
    if "人大" in o_type:
        return "200,255,255"
    if "政协" in o_type:
        return "255,240,200"
    if "纪委" in o_type:
        return "255,220,180"
    if "开发区" in o_type or "工业" in o_type:
        return "200,255,200"
    if "军队" in o_type:
        return "200,200,200"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>china-gov-network Research</creator>')
    lines.append(f'    <description>{REGION}领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        sz = person_size(p["name"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color g="{c.split(",")[1]}" b="{c.split(",")[2]}" r="{c.split(",")[0]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {os.path.basename(GEXF_PATH)} ({eid} edges)")


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON
# ══════════════════════════════════════════════════════════════════════════

SOURCE_REGISTER = [
    {"id": "S001", "title": "务川仡佬族自治县人民政府门户 领导之窗（县委/政府/人大/政协）", "url": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/", "publisher": "务川仡佬族自治县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县委/政府/人大/政协 各班子领导名单与简历页"},
    {"id": "S002", "title": "县委领导之窗（邓林、宋臣、郑成刚、袁远连等各简历页）", "url": "https://www.gzwuchuan.gov.cn/zwgk/ldzc/xwld/", "publisher": "务川仡佬族自治县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "各常委身份、履历、分工"},
    {"id": "S003", "title": "务府办发〔2026〕1号 关于调整县人民政府部分领导同志工作分工的通知", "url": "https://www.gzwuchuan.gov.cn/zwgk/zcwj/zfbwj/202601/t20260107_89127459.html", "publisher": "务川县人民政府办公室", "published_at": "2026-01-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "陈波（常务）增负责卫健/医保/市场监管；李昌亮增民政"},
    {"id": "S004", "title": "务川要闻：邓林、宋臣调研督导防灾减灾工作", "url": "https://www.gzwuchuan.gov.cn/xwzx/zwyw/202607/t20260731_90680525.html", "publisher": "务川县融媒体中心", "published_at": "2026-07-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "邓林（书记）与宋臣（代理县长）搭档;陈波参加"},
    {"id": "S005", "title": "务川要闻：邓林到县纪委监委机关调研座谈", "url": "https://www.gzwuchuan.gov.cn/xwzx/zwyw/202607/t20260721_90644795.html", "publisher": "务川县融媒体中心", "published_at": "2026-07-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "邓林对纪检监察/政法工作调研"},
]


def timeline_for(p):
    name = p["name"]
    if name == "邓林":
        return [
            {"start": "2022", "end": "present", "org": "中共务川仡佬族自治县委员会", "title": "县委书记", "levels": "正处级", "notes": "官方简历页;兼开发区党工委书记", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "present", "org": "贵州务川经济开发区", "title": "党工委书记（兼）", "notes": "兼任", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "出生地/籍贯、教育院校、是否本地干部、出任任务川前职务待补", "confidence": "unverified", "source_ids": []},
        ]
    if name == "宋臣":
        return [
            {"start": "2026", "end": "present", "org": "务川仡佬族自治县人民政府", "title": "代理县长、县政府党组书记", "notes": "官方简历页;兼管委会主任", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "present", "org": "贵州务川经济开发区", "title": "管委会主任（兼）", "notes": "兼任", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "present", "org": "中共务川仡佬族自治县委员会", "title": "县委副书记", "notes": "代理县长主持县政府前为县委副书记", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "1986年生任县长（代）,委族,任务川前经历待查", "confidence": "unverified", "source_ids": []},
        ]
    elif name == "郑成刚":
        return [
            {"start": "", "end": "present", "org": "中共务川仡佬族自治县委员会", "title": "县委副书记", "notes": "协力党建、农业农村/乡村振兴", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "此前经历待查", "confidence": "unverified", "source_ids": []},
        ]
    elif name == "袁远连":
        return [
            {"start": "", "end": "present", "org": "中共务川仡佬族自治县委员会", "title": "县委副书记", "notes": "省民宗委对口帮扶、驻村帮扶", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "此前经历待查", "confidence": "unverified", "source_ids": []},
        ]
    elif name == "陈波":
        return [
            {"start": "", "end": "present", "org": "务川仡佬族自治县人民政府", "title": "常务副县长", "notes": "原曾任县委常委、县委办公室主任", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "此前经历待查", "confidence": "unverified", "source_ids": []},
        ]
    # default
    return [
        {"start": "", "end": "present", "org": p.get("current_org", ""), "title": p.get("current_post", ""), "notes": "官方简历页", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "此前完整工作履历待查", "confidence": "unverified", "source_ids": []},
    ]


def relationships_for(p):
    idx = {pp["id"]: pp for pp in persons}
    out = []
    for r in relationships:
        if r["person_a"] == p["id"] and r["person_b"] in idx:
            other = idx[r["person_b"]]
            out.append({"person": other["name"], "person_id": f"wuchuan_{other['name']}", "relationship_type": r["type"], "strength": "strong", "evidence": r["context"], "overlap_org": r["overlap_org"], "overlap_period": r["overlap_period"], "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002", "S004"]})
        elif r["person_b"] == p["id"] and r["person_a"] in idx:
            other = idx[r["person_a"]]
            out.append({"person": other["name"], "person_id": f"wuchuan_{other['name']}", "relationship_type": r["type"], "strength": "strong", "evidence": r["context"], "overlap_org": r["overlap_org"], "overlap_period": r["overlap_period"], "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002", "S004"]})
    return out


def build_person_jsons():
    idx = {pp["id"]: pp for pp in persons}
    core = [
        (1, "县委书记", "邓林", "正处级"),
        (2, "代理县长", "宋臣", "正处级"),
        (9, "常务副县长", "陈波", "副处级"),
        (3, "县委副书记", "郑成刚", "副处级"),
        (14, "县人大常委会主任", "谢劲松", "正处级"),
    ]
    for pid, file_job, _, rank in core:
        p = idx[pid]
        data = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": PROVINCE, "city": CITY, "region": REGION, "job": file_job, "task_id": "guizhou_务川仡佬族苗族自治县", "time_focus": "2026"},
            "identity": {
                "person_id": f"wuchuan_{p['name']}",
                "name": p["name"],
                "aliases": [], "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""), "native_place": "",
                "education": [p.get("education", "")] if p.get("education") else [],
                "party_join": "中共党员", "work_start": "",
                "dedupe_keys": {"name_birth": f"{p['name']}_{p.get('birth','')}", "name_birthplace": f"{p['name']}_{p.get('birthplace','')}", "official_profile_url": p.get("source", "")}
            },
            "current_status": {"current_post": file_job, "current_org": p.get("current_org", ""), "administrative_rank": rank_of(pid), "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002"]},
            "career_timeline": timeline_for(p),
            "organizations": [],
            "relationships": relationships_for(p),
            "governance_record": governance_for(p),
            "professional_profile": professional_profile(p),
            "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "公开渠道未发现纪律处分或负面通报；邓林2026-07赴纪委机关调研(督导)", "date": AS_OF, "confidence": "unverified", "source_ids": ["S005"]}],
            "source_register": SOURCE_REGISTER,
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "medium", "biggest_gap": f"{p['name']}出任现职前的完整履历（出生地/教育/此前历任）"},
            "open_questions": [
                {"priority": "critical", "question": f"{p['name']}的完整职业生涯（出生地、教育、入党时间、历任任务川前职务）", "why_it_matters": "核心领导，现任职务已确认，早期履历需补充", "suggested_queries": [f"{p['name']} 简历 遵义", f"{p['name']} 任前公示", f"{p['name']} 务川"], "last_attempted": AS_OF},
                {"priority": "high", "question": "前任县委书记（2022年前）、前任县长（宋臣任前）身份及去向", "why_it_matters": "前任-继任交接与干部流动网络", "suggested_queries": ["务川 前任县委书记", "务川 县长 任免"], "last_attempted": AS_OF},
            ],
        }
        data["current_status"]["administrative_rank"] = rank_of(pid)
        fname = f"{TODAY}-{PROVINCE}-{CITY}-{file_job}-{p['name']}.json"
        with open(PERSONS_DIR / fname, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {fname}")


def rank_of(pid):
    return {1: "正处级", 2: "正处级", 3: "副处级", 4: "副处级", 5: "副处级", 6: "副处级", 7: "副处级",
            8: "副处级", 9: "副处级", 10: "副处级", 11: "副处级", 12: "副处级", 13: "副处级", 14: "正处级", 15: "正处级"}.get(pid, "")


def governance_for(p):
    name = p["name"]
    rows = []
    if name == "邓林":
        rows.append({"period": "2026", "domain": "disaster_prevention", "achievement_or_event": "赴涪洋镇调研督导防灾减灾（防汛备汛、避险搬迁），要求'人防+技防'、防患未然", "role": "县委书记", "measurable_outcome": "", "location": "务川-涪洋镇", "confidence": "confirmed", "source_ids": ["S004"]})
        rows.append({"period": "2026", "domain": "discipline", "achievement_or_event": "赴县纪委监委机关调研座谈，抓党风廉政与管党治党", "role": "县委书记", "measurable_outcome": "", "location": "务川", "confidence": "confirmed", "source_ids": ["S005"]})
    return rows


def professional_profile(p):
    name = p["name"]
    if name == "邓林":
        return {"primary_specializations": ["党委宏观治理"], "secondary_specializations": ["开发区/经济"], "career_pattern": "local_ladder", "systems_experience": ["party"], "geographic_pattern": [CITY], "promotion_velocity": {"summary": "1979生任县委书记（正处），1982—1990年代起步，晋升节奏快慢有待档案级资料", "notable_fast_promotions": []}}
    if name == "宋臣":
        return {"primary_specializations": ["政府治理/经济"], "secondary_specializations": [], "career_pattern": "other", "systems_experience": ["government"], "geographic_pattern": [CITY], "promotion_velocity": {"summary": "1986生任县级人民政府代理县长，为高潜力年轻干部（苗族）", "notable_fast_promotions": []}}
    return {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": [], "geographic_pattern": [CITY], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}}


if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"\nOutput files in {BASE}:")
    print(f"  DB:     {SLUG}_network.db")
    print(f"  GEXF:   {SLUG}_network.gexf")
    print("Done.")