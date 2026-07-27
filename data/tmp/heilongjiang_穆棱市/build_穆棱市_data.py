#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 穆棱市 (Muling City), 黑龙江省.

Task ID: heilongjiang_穆棱市
Level: 县级市
Parent city: 牡丹江市
Targets: 市委书记 & 市长
Investigation date: 2026-07-24

Research sources:
  - muling.gov.cn (穆棱市政府官网) — 领导之窗 full leadership roster (confirmed as-of 2026-07-24)

Confidence notes:
  - 穆愔 (市委书记): confirmed via official government leadership page; 女，1976年4月，研究生/农业推广硕士
  - 徐勤刚 (市长): confirmed via official government leadership page; 男，1979年6月，研究生
  - Full leadership roster: confirmed via government leadership page (四大机构 all listed)
  - Career histories for most leaders: unverified — only current names, titles, basic identity confirmed
  - Baidu/Exa/Google search unavailable during this investigation cycle
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "穆棱市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / "scripts" / "build" / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "穆愔",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年4月",
        "birthplace": "",
        "education": "研究生，农业推广硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记、党校校长",
        "current_org": "中共穆棱市委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 2,
        "name": "徐勤刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年6月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、市政府市长、党组书记",
        "current_org": "穆棱市人民政府",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    # ═══════ 市委领导 ═══════
    {
        "id": 3,
        "name": "邓子龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共穆棱市委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 4,
        "name": "孙罡",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、纪委书记、监委主任",
        "current_org": "中共穆棱市纪律检查委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 5,
        "name": "董少宝",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共穆棱市委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 6,
        "name": "周鹤年",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市政府副市长、党组副书记",
        "current_org": "穆棱市人民政府",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 7,
        "name": "赵磊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共穆棱市委员会宣传部",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 8,
        "name": "项晓光",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "穆棱市委常委、组织部部长、市委党校第一副校长",
        "current_org": "中共穆棱市委员会组织部",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 9,
        "name": "刘建民",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、统战部部长、市政协党组副书记、市委办公室主任",
        "current_org": "中共穆棱市委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 10,
        "name": "张伟东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市政府副市长、党组成员",
        "current_org": "穆棱市人民政府",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 11,
        "name": "韩晓明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、人民武装部上校部长",
        "current_org": "穆棱市人民武装部",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    # ═══════ 市人大领导 ═══════
    {
        "id": 12,
        "name": "刘明伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任、党组书记",
        "current_org": "穆棱市人民代表大会常务委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 13,
        "name": "袁封华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "穆棱市人民代表大会常务委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 14,
        "name": "李俭波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任、党组副书记",
        "current_org": "穆棱市人民代表大会常务委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 15,
        "name": "李俊刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任、党组成员",
        "current_org": "穆棱市人民代表大会常务委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 16,
        "name": "崔桂林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任、党组成员",
        "current_org": "穆棱市人民代表大会常务委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    # ═══════ 市政府领导 ═══════
    {
        "id": 17,
        "name": "李福来",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "穆棱市人民政府",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 18,
        "name": "臧亚鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长、党组成员",
        "current_org": "穆棱市人民政府",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 19,
        "name": "刘海超",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长、党组成员、公安局局长",
        "current_org": "穆棱市人民政府",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 20,
        "name": "邢伟江",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长、党组成员",
        "current_org": "穆棱市人民政府",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 21,
        "name": "王国锋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长、党组成员",
        "current_org": "穆棱市人民政府",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 22,
        "name": "谢金鑫",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长、党组成员",
        "current_org": "穆棱市人民政府",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    # ═══════ 市政协领导 ═══════
    {
        "id": 23,
        "name": "刘学凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年7月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席、党组书记",
        "current_org": "中国人民政治协商会议穆棱市委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 24,
        "name": "巩艳梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席、党组成员",
        "current_org": "中国人民政治协商会议穆棱市委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 25,
        "name": "郝桂菊",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席、市人民法院副院长",
        "current_org": "中国人民政治协商会议穆棱市委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 26,
        "name": "林鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议穆棱市委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
    {
        "id": 27,
        "name": "康卫民",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协秘书长",
        "current_org": "中国人民政治协商会议穆棱市委员会",
        "source": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共穆棱市委员会", "type": "党委", "level": "县级", "parent": "中共牡丹江市委员会", "location": "穆棱市"},
    {"id": 2, "name": "穆棱市人民政府", "type": "政府", "level": "县级", "parent": "牡丹江市人民政府", "location": "穆棱市"},
    {"id": 3, "name": "中共穆棱市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共穆棱市委员会", "location": "穆棱市"},
    {"id": 4, "name": "穆棱市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "穆棱市"},
    {"id": 5, "name": "中国人民政治协商会议穆棱市委员会", "type": "政协", "level": "县级", "parent": "", "location": "穆棱市"},
    {"id": 6, "name": "中共穆棱市委员会组织部", "type": "党委部门", "level": "县级", "parent": "中共穆棱市委员会", "location": "穆棱市"},
    {"id": 7, "name": "中共穆棱市委员会宣传部", "type": "党委部门", "level": "县级", "parent": "中共穆棱市委员会", "location": "穆棱市"},
    {"id": 8, "name": "穆棱市人民武装部", "type": "政府部门", "level": "县级", "parent": "", "location": "穆棱市"},
    {"id": 9, "name": "穆棱市公安局", "type": "政府部门", "level": "县级", "parent": "穆棱市人民政府", "location": "穆棱市"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 穆愔 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记、党校校长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 徐勤刚 — 市长
    {"person_id": 2, "org_id": 2, "title": "市委副书记、市政府市长、党组书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 邓子龙 — 市委副书记
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 孙罡 — 纪委书记
    {"person_id": 4, "org_id": 3, "title": "市委常委、纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 董少宝 — 政法委书记
    {"person_id": 5, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 周鹤年 — 常务副市长
    {"person_id": 6, "org_id": 2, "title": "市委常委、市政府副市长、党组副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "常务副市长"},
    # 赵磊 — 宣传部部长
    {"person_id": 7, "org_id": 7, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 项晓光 — 组织部部长
    {"person_id": 8, "org_id": 6, "title": "市委常委、组织部部长、市委党校第一副校长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 刘建民 — 统战部部长兼市委办公室主任
    {"person_id": 9, "org_id": 1, "title": "市委常委、统战部部长、市政协党组副书记、市委办公室主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 张伟东 — 副市长
    {"person_id": 10, "org_id": 2, "title": "市委常委、市政府副市长、党组成员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 韩晓明 — 人武部部长
    {"person_id": 11, "org_id": 8, "title": "市委常委、人民武装部上校部长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 人大
    {"person_id": 12, "org_id": 4, "title": "市人大常委会主任、党组书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 13, "org_id": 4, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 14, "org_id": 4, "title": "市人大常委会副主任、党组副书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 15, "org_id": 4, "title": "市人大常委会副主任、党组成员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 16, "org_id": 4, "title": "市人大常委会副主任、党组成员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 政府
    {"person_id": 17, "org_id": 2, "title": "市政府副市长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "市政府副市长、党组成员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "市政府副市长、党组成员、公安局局长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 19, "org_id": 9, "title": "公安局局长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "市政府副市长、党组成员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "市政府副市长、党组成员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 22, "org_id": 2, "title": "市政府副市长、党组成员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 政协
    {"person_id": 23, "org_id": 5, "title": "市政协主席、党组书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 24, "org_id": 5, "title": "市政协副主席、党组成员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 25, "org_id": 5, "title": "市政协副主席、市人民法院副院长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 26, "org_id": 5, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 27, "org_id": 5, "title": "市政协秘书长", "start_date": "", "end_date": "", "rank": "", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 穆愔 ↔ 徐勤刚（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "穆愔任市委书记，徐勤刚任市长", "overlap_org": "穆棱市", "overlap_period": "2026-"},
    # 穆愔 ↔ 邓子龙（市委班子）
    {"person_a": 1, "person_b": 3, "type": "市委班子", "context": "邓子龙任市委副书记", "overlap_org": "中共穆棱市委员会", "overlap_period": ""},
    # 穆愔 ↔ 孙罡（市委班子）
    {"person_a": 1, "person_b": 4, "type": "市委班子", "context": "孙罡任市委常委、市纪委书记", "overlap_org": "中共穆棱市委员会", "overlap_period": ""},
    # 穆愔 ↔ 董少宝（市委班子）
    {"person_a": 1, "person_b": 5, "type": "市委班子", "context": "董少宝任市委常委、政法委书记", "overlap_org": "中共穆棱市委员会", "overlap_period": ""},
    # 穆愔 ↔ 周鹤年（市委班子/政府）
    {"person_a": 1, "person_b": 6, "type": "市委班子", "context": "周鹤年任市委常委、常务副市长", "overlap_org": "中共穆棱市委员会", "overlap_period": ""},
    # 穆愔 ↔ 赵磊（市委班子）
    {"person_a": 1, "person_b": 7, "type": "市委班子", "context": "赵磊任市委常委、宣传部部长", "overlap_org": "中共穆棱市委员会", "overlap_period": ""},
    # 穆愔 ↔ 项晓光（市委班子）
    {"person_a": 1, "person_b": 8, "type": "市委班子", "context": "项晓光任市委常委、组织部部长", "overlap_org": "中共穆棱市委员会", "overlap_period": ""},
    # 穆愔 ↔ 刘建民（市委班子）
    {"person_a": 1, "person_b": 9, "type": "市委班子", "context": "刘建民任市委常委、统战部部长", "overlap_org": "中共穆棱市委员会", "overlap_period": ""},
    # 穆愔 ↔ 张伟东（市委班子/政府）
    {"person_a": 1, "person_b": 10, "type": "市委班子", "context": "张伟东任市委常委、副市长", "overlap_org": "中共穆棱市委员会", "overlap_period": ""},
    # 穆愔 ↔ 韩晓明（市委班子）
    {"person_a": 1, "person_b": 11, "type": "市委班子", "context": "韩晓明任市委常委、人武部部长", "overlap_org": "中共穆棱市委员会", "overlap_period": ""},
    # 徐勤刚 ↔ 周鹤年（政府班子）
    {"person_a": 2, "person_b": 6, "type": "政府班子", "context": "周鹤年任市委常委、常务副市长", "overlap_org": "穆棱市人民政府", "overlap_period": ""},
    # 徐勤刚 ↔ 张伟东（政府班子）
    {"person_a": 2, "person_b": 10, "type": "政府班子", "context": "张伟东任市委常委、副市长", "overlap_org": "穆棱市人民政府", "overlap_period": ""},
    # 徐勤刚 ↔ 李福来（政府班子）
    {"person_a": 2, "person_b": 17, "type": "政府班子", "context": "李福来任副市长", "overlap_org": "穆棱市人民政府", "overlap_period": ""},
    # 徐勤刚 ↔ 臧亚鹏（政府班子）
    {"person_a": 2, "person_b": 18, "type": "政府班子", "context": "臧亚鹏任副市长", "overlap_org": "穆棱市人民政府", "overlap_period": ""},
    # 徐勤刚 ↔ 刘海超（政府班子）
    {"person_a": 2, "person_b": 19, "type": "政府班子", "context": "刘海超任副市长、公安局局长", "overlap_org": "穆棱市人民政府", "overlap_period": ""},
    # 徐勤刚 ↔ 邢伟江（政府班子）
    {"person_a": 2, "person_b": 20, "type": "政府班子", "context": "邢伟江任副市长", "overlap_org": "穆棱市人民政府", "overlap_period": ""},
    # 徐勤刚 ↔ 王国锋（政府班子）
    {"person_a": 2, "person_b": 21, "type": "政府班子", "context": "王国锋任副市长", "overlap_org": "穆棱市人民政府", "overlap_period": ""},
    # 徐勤刚 ↔ 谢金鑫（政府班子）
    {"person_a": 2, "person_b": 22, "type": "政府班子", "context": "谢金鑫任副市长", "overlap_org": "穆棱市人民政府", "overlap_period": ""},
    # 刘建民 ↔ 刘学凯（政协共管）
    {"person_a": 9, "person_b": 23, "type": "政协班子", "context": "刘建民任市政协党组副书记，刘学凯任市政协主席", "overlap_org": "穆棱市政协", "overlap_period": ""},
]


# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

    # Write DB+GEXF to staging
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

    # Write person JSON files
    person_files = [
        {
            "id": 1,
            "name": "穆愔",
            "job": "市委书记",
            "data": {
                "schema_version": "1.0",
                "generated_at": TODAY,
                "investigation_scope": {
                    "province": "黑龙江省",
                    "city": "牡丹江市",
                    "region": "穆棱市",
                    "job": "市委书记",
                    "task_id": "heilongjiang_穆棱市",
                    "time_focus": "2026-07"
                },
                "identity": {
                    "person_id": "muling_muyin",
                    "name": "穆愔",
                    "gender": "女",
                    "ethnicity": "汉族",
                    "birth": "1976年4月",
                    "education": [{"degree": "研究生，农业推广硕士", "study_type": "unknown"}],
                    "dedupe_keys": {"name_birth": "穆愔_1976", "name_birthplace": "", "official_profile_url": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"}
                },
                "current_status": {
                    "current_post": "市委书记、党校校长",
                    "current_org": "中共穆棱市委员会",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001"]
                },
                "career_timeline": [],
                "organizations": [],
                "relationships": [
                    {"person": "徐勤刚", "person_id": "muling_xuqingang", "relationship_type": "overlap", "strength": "strong", "evidence": "市委书记与市长党政工作搭档", "overlap_org": "穆棱市", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"person": "邓子龙", "person_id": "", "relationship_type": "overlap", "strength": "strong", "evidence": "市委副书记与市委书记共事", "overlap_org": "中共穆棱市委员会", "confidence": "confirmed", "source_ids": ["S001"]},
                ],
                "governance_record": [],
                "professional_profile": {
                    "primary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": [],
                    "geographic_pattern": [],
                    "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
                },
                "work_style_and_personality": {
                    "public_style_indicators": [],
                    "caveat": "缺乏公开资料，工作风格未评估"
                },
                "risk_and_integrity_signals": [
                    {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
                ],
                "source_register": [
                    {"id": "S001", "title": "穆棱市领导之窗", "url": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml", "source_type": "official", "reliability": "high", "accessed_at": AS_OF}
                ],
                "confidence_summary": {
                    "identity": "plausible",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "low",
                    "biggest_gap": "穆愔来穆棱前的完整履历未找到"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "穆愔的完整履历是什么？来穆棱前的任职经历？",
                        "why_it_matters": "作为穆棱市现任一把手，其职业背景对理解政治网络至关重要。名字中'愔'字较为罕见",
                        "suggested_queries": ["穆愔 简历 穆棱", "穆愔 任前公示 牡丹江", "穆愔 百度百科", "穆愔 女 市委书记"],
                        "last_attempted": AS_OF
                    }
                ]
            }
        },
        {
            "id": 2,
            "name": "徐勤刚",
            "job": "市长",
            "data": {
                "schema_version": "1.0",
                "generated_at": TODAY,
                "investigation_scope": {
                    "province": "黑龙江省",
                    "city": "牡丹江市",
                    "region": "穆棱市",
                    "job": "市长",
                    "task_id": "heilongjiang_穆棱市",
                    "time_focus": "2026-07"
                },
                "identity": {
                    "person_id": "muling_xuqingang",
                    "name": "徐勤刚",
                    "gender": "男",
                    "ethnicity": "汉族",
                    "birth": "1979年6月",
                    "education": [{"degree": "研究生", "study_type": "unknown"}],
                    "dedupe_keys": {"name_birth": "徐勤刚_1979", "name_birthplace": "", "official_profile_url": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"}
                },
                "current_status": {
                    "current_post": "市委副书记、市政府市长、党组书记",
                    "current_org": "穆棱市人民政府",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001"]
                },
                "career_timeline": [],
                "organizations": [],
                "relationships": [
                    {"person": "穆愔", "person_id": "muling_muyin", "relationship_type": "overlap", "strength": "strong", "evidence": "市长与市委书记党政工作搭档", "overlap_org": "穆棱市", "confidence": "confirmed", "source_ids": ["S001"]},
                ],
                "governance_record": [],
                "professional_profile": {
                    "primary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": [],
                    "geographic_pattern": [],
                    "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
                },
                "work_style_and_personality": {
                    "public_style_indicators": [],
                    "caveat": "缺乏公开资料，工作风格未评估"
                },
                "risk_and_integrity_signals": [
                    {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
                ],
                "source_register": [
                    {"id": "S001", "title": "穆棱市领导之窗", "url": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml", "source_type": "official", "reliability": "high", "accessed_at": AS_OF}
                ],
                "confidence_summary": {
                    "identity": "plausible",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "low",
                    "biggest_gap": "徐勤刚来穆棱前的完整履历未找到"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "徐勤刚的完整履历是什么？来穆棱前的任职经历？",
                        "why_it_matters": "作为穆棱市市长，其职业背景对理解地方政府运作和晋升路径至关重要",
                        "suggested_queries": ["徐勤刚 简历 穆棱", "徐勤刚 任前公示 牡丹江", "徐勤刚 百度百科"],
                        "last_attempted": AS_OF
                    }
                ]
            }
        },
        {
            "id": 23,
            "name": "刘学凯",
            "job": "市政协主席",
            "data": {
                "schema_version": "1.0",
                "generated_at": TODAY,
                "investigation_scope": {
                    "province": "黑龙江省",
                    "city": "牡丹江市",
                    "region": "穆棱市",
                    "job": "市政协主席",
                    "task_id": "heilongjiang_穆棱市",
                    "time_focus": "2026-07"
                },
                "identity": {
                    "person_id": "muling_liuxuekai",
                    "name": "刘学凯",
                    "gender": "男",
                    "ethnicity": "汉族",
                    "birth": "1970年7月",
                    "education": [{"degree": "研究生", "study_type": "unknown"}],
                    "dedupe_keys": {"name_birth": "刘学凯_1970", "name_birthplace": "", "official_profile_url": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml"}
                },
                "current_status": {
                    "current_post": "市政协主席、党组书记",
                    "current_org": "中国人民政治协商会议穆棱市委员会",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001"]
                },
                "career_timeline": [],
                "organizations": [],
                "relationships": [],
                "governance_record": [],
                "professional_profile": {"career_pattern": "unknown"},
                "work_style_and_personality": {"caveat": "缺乏公开资料"},
                "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}],
                "source_register": [{"id": "S001", "title": "穆棱市领导之窗", "url": "https://www.muling.gov.cn/mdjmlsrmzf/c103184/ldzc.shtml", "source_type": "official", "reliability": "high", "accessed_at": AS_OF}],
                "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "low", "biggest_gap": "刘学凯完整履历未找到"},
                "open_questions": [{"priority": "high", "question": "刘学凯任政协主席前的任职经历？", "why_it_matters": "四大机构正职中有两人出生年份不同，了解其职业路径有助于理解班子构成", "suggested_queries": ["刘学凯 穆棱 政协 主席 简历", "刘学凯 百度百科"], "last_attempted": AS_OF}]
            }
        },
    ]

    for pf in person_files:
        fname = f"{TODAY}-黑龙江省-牡丹江市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  ✅ Person JSON: {path}")

    print(f"\n✅ Done — {SLUG} data build complete (staged in {STAGING_DIR}).")
    print(f"   Run: python3 scripts/process_tmp.py {STAGING_DIR}")
    print(f"   Then: python3 scripts/process_tmp.py {STAGING_DIR} --apply")


if __name__ == "__main__":
    main()
