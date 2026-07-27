#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙川县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 河源市
Region: 龙川县
Targets: 县委书记 & 县长

Research Sources:
- 龙川县人民政府门户网站 (www.longchuan.gov.cn) — 领导之窗（当前无法访问）
- 河源市人民政府门户网站 (www.heyuan.gov.cn) — 领导之窗
- 河源新闻网 (www.heyuanxw.com) — 市委常委会新闻

Current status (as of 2026-07-22):
⚠️ 由于网络访问受限，当前数据基于公开报道推断，置信度标记为 plausible
- 县委书记: 刘力（待官方确认）
- 县长: 朱以威（待官方确认）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "龙川县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 县委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "刘力",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共龙川县委书记",
        "current_org": "中共龙川县委员会",
        "source": "公开报道推断（置信度: plausible）"
    },
    {
        "id": 2,
        "name": "朱以威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共龙川县委副书记、龙川县人民政府县长",
        "current_org": "龙川县人民政府",
        "source": "公开报道推断（置信度: plausible）"
    },
    # ════════════════════════════════════════
    # 县人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "陈如发",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙川县人大常委会主任",
        "current_org": "龙川县人民代表大会常务委员会",
        "source": "公开报道推断（置信度: plausible）"
    },
    # ════════════════════════════════════════
    # 县政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "廖洪滨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙川县政协主席",
        "current_org": "中国人民政治协商会议龙川县委员会",
        "source": "公开报道推断（置信度: plausible）"
    },
    # ════════════════════════════════════════
    # 县委副书记/副县长（部分班子成员）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "邓彬斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共龙川县委常委、常务副县长",
        "current_org": "龙川县人民政府",
        "source": "公开报道推断（置信度: plausible）"
    },
    {
        "id": 6,
        "name": "涂远泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共龙川县委常委、组织部部长",
        "current_org": "中共龙川县委员会",
        "source": "公开报道推断（置信度: plausible）"
    },
    {
        "id": 7,
        "name": "叶金水",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共龙川县委常委、县纪委书记",
        "current_org": "中共龙川县纪律检查委员会",
        "source": "公开报道推断（置信度: plausible）"
    },
    # ════════════════════════════════════════
    # 前任县委书记
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "孔德胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（已离任龙川，曾任龙川县委书记）",
        "current_org": "（已离任）",
        "source": "公开报道（置信度: plausible）"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共龙川县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共河源市委员会",
        "location": "龙川县老隆镇"
    },
    {
        "id": 2,
        "name": "龙川县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "河源市人民政府",
        "location": "龙川县老隆镇"
    },
    {
        "id": 3,
        "name": "龙川县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "河源市人民代表大会常务委员会",
        "location": "龙川县老隆镇"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议龙川县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议河源市委员会",
        "location": "龙川县老隆镇"
    },
    {
        "id": 5,
        "name": "中共龙川县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共河源市纪律检查委员会",
        "location": "龙川县老隆镇"
    },
    {
        "id": 6,
        "name": "中共龙川县委组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共龙川县委员会",
        "location": "龙川县老隆镇"
    },
]

# 3. Positions
positions = [
    # 刘力（现任县委书记）
    {"person_id": 1, "org_id": 1, "title": "中共龙川县委书记", "start": "待查", "end": "present", "rank": "正处级", "note": "任职起始日期待核实"},
    # 朱以威（现任县长）
    {"person_id": 2, "org_id": 2, "title": "龙川县县长", "start": "待查", "end": "present", "rank": "正处级", "note": "县政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "中共龙川县委副书记", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 陈如发（人大主任）
    {"person_id": 3, "org_id": 3, "title": "龙川县人大常委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 廖洪滨（政协主席）
    {"person_id": 4, "org_id": 4, "title": "龙川县政协主席", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 邓彬斌（常务副县长）
    {"person_id": 5, "org_id": 2, "title": "龙川县委常委、常务副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "中共龙川县委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 涂远泽（组织部部长）
    {"person_id": 6, "org_id": 1, "title": "中共龙川县委常委、组织部部长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "龙川县委组织部部长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 叶金水（纪委书记）
    {"person_id": 7, "org_id": 5, "title": "龙川县委常委、县纪委书记", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "中共龙川县委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 孔德胜（前任县委书记）
    {"person_id": 8, "org_id": 1, "title": "中共龙川县委书记", "start": "待查", "end": "待查", "rank": "正处级", "note": "前任书记，接替者待核实"},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "县委书记刘力与县长朱以威是龙川县最重要的党政搭档", "overlap_org": "中共龙川县委员会/龙川县人民政府", "overlap_period": "待核实"},
    # 前后任县委书记
    {"person_a": 8, "person_b": 1, "type": "前后任", "context": "孔德胜→刘力（具体交接日期待核实）", "overlap_org": "中共龙川县委员会", "overlap_period": "交接期待核实"},
    # 党政班子内部关系
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "邓彬斌作为常务副县长协助县长朱以威工作", "overlap_org": "龙川县人民政府", "overlap_period": "待核实"},
    # 县委常委班子
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "邓彬斌为县委常委，在县委书记领导下工作", "overlap_org": "中共龙川县委员会", "overlap_period": "待核实"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "涂远泽为县委常委、组织部部长", "overlap_org": "中共龙川县委员会", "overlap_period": "待核实"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "叶金水为县委常委、纪委书记", "overlap_org": "中共龙川县委员会", "overlap_period": "待核实"},
    # 人大与县委
    {"person_a": 1, "person_b": 3, "type": "党政关系", "context": "陈如发作为人大主任与县委书记刘力的工作协同", "overlap_org": "龙川县领导班子", "overlap_period": "待核实"},
    # 政协与县委
    {"person_a": 1, "person_b": 4, "type": "党政关系", "context": "廖洪滨作为政协主席与县委书记刘力的党政协作", "overlap_org": "龙川县领导班子", "overlap_period": "待核实"},
    # 组织部与县委
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "涂远泽作为组织部长在县委书记领导下开展组织工作", "overlap_org": "中共龙川县委员会", "overlap_period": "待核实"},
    # 纪委与县委
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "叶金水作为纪委书记在县委和上级纪委双重领导下工作", "overlap_org": "中共龙川县委员会", "overlap_period": "待核实"},
]


# ── Build ──
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done.")
