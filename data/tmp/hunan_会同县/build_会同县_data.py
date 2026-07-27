#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会同县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 湖南省
Parent City: 怀化市
Region: 会同县
Targets: 县委书记 & 县长

Research Sources:
- 会同县人民政府网站 (www.huitong.gov.cn) — 可访问
- 会同县领导之窗页面 — 确认县长信息
- 会同县新闻中心 — 确认县委书记活动

Research Date: 2026-07-24
Web Access: Partial — 县政府网站可访问，百度百科/Baidu不可用
Evidence Status: Good for current leaders, partial for biographies
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "会同县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons (use IDs 1-100 for persons)
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (会同县)
    # ════════════════════════════════════════
    # 苏振 — 会同县委书记
    # Confirmed by multiple news items (Jun-Jul 2026)
    # Also serves as 县人武部党委第一书记 (appointed Jul 22, 2026)
    {
        "id": 1,
        "name": "苏振",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共会同县委书记",
        "current_org": "中共会同县委员会",
        "source": "https://www.huitong.gov.cn (会同县新闻中心 2026年6-7月)",
    },
    # 李超 — 会同县委副书记、代理县长
    # Female, Han, born May 1985, 江西乐安人
    # Master of Engineering, started work May 2009, joined CPC May 2008
    {
        "id": 2,
        "name": "李超",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985-05",
        "birthplace": "江西乐安",
        "education": "工学硕士",
        "party_join": "中共党员",
        "work_start": "2009-05",
        "current_post": "会同县委副书记、代理县长",
        "current_org": "会同县人民政府",
        "source": "https://www.huitong.gov.cn/huitong/c1175481/xzf2020.shtml",
    },
    # ════════════════════════════════════════
    # Previous Leaders (Predecessors)
    # ════════════════════════════════════════
    # 前县委书记 (苏振的前任 — 具体姓名待确认)
    {
        "id": 3,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任会同县委书记 (已调离)",
        "current_org": "",
        "source": "信息待确认",
    },
    # 前县长 (李超的前任 — 有线索为"伍"姓，具体姓名待确认)
    {
        "id": 4,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任会同县人民政府县长 (已调离)",
        "current_org": "",
        "source": "信息待确认",
    },
    # ════════════════════════════════════════
    # Key Deputies (Standing Committee Members)
    # ════════════════════════════════════════
    # 兰利华 — 县政协主席 (confirmed from meeting news)
    {
        "id": 5,
        "name": "兰利华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "会同县政协主席",
        "current_org": "中国人民政治协商会议会同县委员会",
        "source": "https://www.huitong.gov.cn (2026-07-22 县委学习教育专题会)",
    },
    # 常务副县长 — 李志杰 (from 县政府 page, listed first among vice mayors)
    {
        "id": 6,
        "name": "李志杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "会同县委常委、常务副县长",
        "current_org": "会同县人民政府",
        "source": "https://www.huitong.gov.cn/huitong/c1175481/xzf2020.shtml",
    },
    # 罗祥柏 — 副县长
    {
        "id": 7,
        "name": "罗祥柏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "会同县人民政府副县长",
        "current_org": "会同县人民政府",
        "source": "https://www.huitong.gov.cn/huitong/c1175481/xzf2020.shtml",
    },
    # 杨小玲 — 副县长
    {
        "id": 8,
        "name": "杨小玲",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "会同县人民政府副县长",
        "current_org": "会同县人民政府",
        "source": "https://www.huitong.gov.cn/huitong/c1175481/xzf2020.shtml",
    },
    # 罗斌 — 副县长
    {
        "id": 9,
        "name": "罗斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "会同县人民政府副县长",
        "current_org": "会同县人民政府",
        "source": "https://www.huitong.gov.cn/huitong/c1175481/xzf2020.shtml",
    },
    # 屈祖兴 — 副县长
    {
        "id": 10,
        "name": "屈祖兴",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "会同县人民政府副县长",
        "current_org": "会同县人民政府",
        "source": "https://www.huitong.gov.cn/huitong/c1175481/xzf2020.shtml",
    },
    # 蒋杰松 — 副县长
    {
        "id": 11,
        "name": "蒋杰松",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "会同县人民政府副县长",
        "current_org": "会同县人民政府",
        "source": "https://www.huitong.gov.cn/huitong/c1175481/xzf2020.shtml",
    },
    # 杨跃华 — 副县长
    {
        "id": 12,
        "name": "杨跃华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "会同县人民政府副县长",
        "current_org": "会同县人民政府",
        "source": "https://www.huitong.gov.cn/huitong/c1175481/xzf2020.shtml",
    },
    # 吴峰 — 副县长
    {
        "id": 13,
        "name": "吴峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "会同县人民政府副县长",
        "current_org": "会同县人民政府",
        "source": "https://www.huitong.gov.cn/huitong/c1175481/xzf2020.shtml",
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共会同县委员会", "type": "党委", "level": "县级", "location": "湖南省怀化市会同县"},
    {"id": 2, "name": "会同县人民政府", "type": "政府", "level": "县级", "location": "湖南省怀化市会同县"},
    {"id": 3, "name": "中国共产党会同县纪律检查委员会", "type": "纪委", "level": "县级", "location": "湖南省怀化市会同县"},
    {"id": 4, "name": "会同县监察委员会", "type": "纪委", "level": "县级", "location": "湖南省怀化市会同县"},
    {"id": 5, "name": "中共会同县委组织部", "type": "党委", "level": "县级", "location": "湖南省怀化市会同县"},
    {"id": 6, "name": "中共会同县委宣传部", "type": "党委", "level": "县级", "location": "湖南省怀化市会同县"},
    {"id": 7, "name": "中共会同县委政法委员会", "type": "党委", "level": "县级", "location": "湖南省怀化市会同县"},
    {"id": 8, "name": "会同县人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "湖南省怀化市会同县"},
    {"id": 9, "name": "中国人民政治协商会议会同县委员会", "type": "政协", "level": "县级", "location": "湖南省怀化市会同县"},
    {"id": 10, "name": "中共怀化市委员会", "type": "党委", "level": "地市级", "location": "湖南省怀化市"},
    {"id": 11, "name": "怀化市人民政府", "type": "政府", "level": "地市级", "location": "湖南省怀化市"},
]

# 3. Positions: person_id -> org_id with title and dates
positions = [
    # 苏振 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共会同县委书记", "start": "?", "end": "至今", "note": "2026年5月-7月已以县委书记身份参加多次活动"},
    {"person_id": 1, "org_id": 1, "title": "会同县人武部党委第一书记", "start": "2026-07", "end": "至今", "note": "2026年7月22日任职"},
    {"person_id": 1, "org_id": 10, "title": "中共怀化市委委员", "start": "?", "end": "至今", "note": "县委书记自然为市委委员"},

    # 李超 — 代理县长
    {"person_id": 2, "org_id": 2, "title": "会同县委副书记、代理县长", "start": "2026-05", "end": "至今", "note": "2026年5月首次以代县长身份公开报道"},
    {"person_id": 2, "org_id": 1, "title": "中共会同县委副书记", "start": "2026-05", "end": "至今", "note": "代理县长兼任县委副书记"},

    # 前县委书记 (待查)
    # 前县长 (待查)

    # 兰利华 — 政协主席
    {"person_id": 5, "org_id": 9, "title": "会同县政协主席", "start": "?", "end": "至今", "note": "2026年7月仍在任"},

    # 李志杰 — 常务副县长
    {"person_id": 6, "org_id": 2, "title": "会同县委常委、常务副县长", "start": "?", "end": "至今", "note": "县政府官网显示为副县长列表首位"},

    # 副县长们
    {"person_id": 7, "org_id": 2, "title": "会同县人民政府副县长", "start": "?", "end": "至今", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "会同县人民政府副县长", "start": "?", "end": "至今", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "会同县人民政府副县长", "start": "?", "end": "至今", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "会同县人民政府副县长", "start": "?", "end": "至今", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "会同县人民政府副县长", "start": "?", "end": "至今", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "会同县人民政府副县长", "start": "?", "end": "至今", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "会同县人民政府副县长", "start": "?", "end": "至今", "note": ""},
]

# 4. Relationships
relationships = [
    # 苏振 ↔ 李超 (县委书记与代理县长搭班)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与代理县长搭班工作",
        "overlap_org": "会同县",
        "overlap_period": "2026-05-至今",
    },
    # 苏振 ↔ 兰利华 (县委书记与政协主席)
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "县委书记与政协主席同班子工作",
        "overlap_org": "会同县",
        "overlap_period": "2026-至今",
    },
    # 李超 ↔ 李志杰 (县长与常务副县长)
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县长与常务副县长上下级关系",
        "overlap_org": "会同县人民政府",
        "overlap_period": "2026-至今",
    },
    # 苏振 ↔ 李志杰 (县委书记与常务副县长)
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县委书记与常务副县长同班子工作",
        "overlap_org": "中共会同县委员会",
        "overlap_period": "2026-至今",
    },
    # 李志杰 ↔ 罗祥柏 (常务副县长与其他副县长)
    {
        "person_a": 6,
        "person_b": 7,
        "type": "overlap",
        "context": "县政府班子同僚",
        "overlap_org": "会同县人民政府",
        "overlap_period": "2026-至今",
    },
    # 李志杰 ↔ 杨小玲
    {
        "person_a": 6,
        "person_b": 8,
        "type": "overlap",
        "context": "县政府班子同僚",
        "overlap_org": "会同县人民政府",
        "overlap_period": "2026-至今",
    },
    # 李志杰 ↔ 罗斌
    {
        "person_a": 6,
        "person_b": 9,
        "type": "overlap",
        "context": "县政府班子同僚",
        "overlap_org": "会同县人民政府",
        "overlap_period": "2026-至今",
    },
    # 李志杰 ↔ 屈祖兴
    {
        "person_a": 6,
        "person_b": 10,
        "type": "overlap",
        "context": "县政府班子同僚",
        "overlap_org": "会同县人民政府",
        "overlap_period": "2026-至今",
    },
    # 李志杰 ↔ 蒋杰松
    {
        "person_a": 6,
        "person_b": 11,
        "type": "overlap",
        "context": "县政府班子同僚",
        "overlap_org": "会同县人民政府",
        "overlap_period": "2026-至今",
    },
    # 李志杰 ↔ 杨跃华
    {
        "person_a": 6,
        "person_b": 12,
        "type": "overlap",
        "context": "县政府班子同僚",
        "overlap_org": "会同县人民政府",
        "overlap_period": "2026-至今",
    },
    # 李志杰 ↔ 吴峰
    {
        "person_a": 6,
        "person_b": 13,
        "type": "overlap",
        "context": "县政府班子同僚",
        "overlap_org": "会同县人民政府",
        "overlap_period": "2026-至今",
    },
]

# ── Build ──

if __name__ == "__main__":
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
    print("Done!")
