#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 宁安市 (Ning'an City), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_宁安市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - ningan.gov.cn (宁安市政府官网) — 领导之窗 full leadership roster (confirmed as-of 2026-07-24)
  - Baidu Baike — 徐利刃 biography (前宁安市委书记, now 省政协秘书长)
  - Wikipedia (zh.wikipedia.org) — 宁安市 page for basic info

Confidence notes:
  - 程亮 (市委书记): confirmed via official government leadership page; detailed career history unverified
  - 王树军 (代市长): confirmed via official government leadership page; 蒙古族, 1977年1月, 研究生学历
  - Full leadership roster: confirmed via government leadership page (19 leaders listed)
  - Career histories for most leaders: unverified — only current names and titles confirmed
  - Exa search was rate-limited; Baidu returned CAPTCHA
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "宁安市"
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
        "name": "程亮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共宁安市委员会",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 2,
        "name": "王树军",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1977年1月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "代市长",
        "current_org": "宁安市人民政府",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104577/202607/c03_1052791.shtml"
    },
    # ═══════ 市委领导 ═══════
    {
        "id": 3,
        "name": "林勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共宁安市委员会",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 4,
        "name": "夏庆超",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记（挂职）",
        "current_org": "中共宁安市委员会",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 5,
        "name": "胡寒冰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委 市纪委书记 监委主任",
        "current_org": "中共宁安市纪律检查委员会",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 6,
        "name": "李树新",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委 政法委书记",
        "current_org": "中共宁安市委员会",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 7,
        "name": "张明新",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委 副市长",
        "current_org": "宁安市人民政府",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 8,
        "name": "王超",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委 副市长",
        "current_org": "宁安市人民政府",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 9,
        "name": "张忠伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委 组织部部长",
        "current_org": "中共宁安市委员会组织部",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 10,
        "name": "杨润",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委 人武部部长",
        "current_org": "宁安市人民武装部",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 11,
        "name": "徐竣怡",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委 宣传部部长",
        "current_org": "中共宁安市委员会宣传部",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    # ═══════ 人大领导 ═══════
    {
        "id": 12,
        "name": "贾洪新",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大主任",
        "current_org": "宁安市人民代表大会常务委员会",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 13,
        "name": "贾维国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大副主任",
        "current_org": "宁安市人民代表大会常务委员会",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 14,
        "name": "吴洪波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大副主任",
        "current_org": "宁安市人民代表大会常务委员会",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 15,
        "name": "郭成",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大副主任",
        "current_org": "宁安市人民代表大会常务委员会",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 16,
        "name": "关雨尧",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大副主任",
        "current_org": "宁安市人民代表大会常务委员会",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    # ═══════ 政府领导 ═══════
    {
        "id": 17,
        "name": "林鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "宁安市人民政府",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 18,
        "name": "张鑫",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长 公安局局长",
        "current_org": "宁安市人民政府",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 19,
        "name": "李丹",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "宁安市人民政府",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 20,
        "name": "迟龙飞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "宁安市人民政府",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    # ═══════ 政协领导 ═══════
    {
        "id": 21,
        "name": "杨冬梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议宁安市委员会",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 22,
        "name": "田忠青",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议宁安市委员会",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 23,
        "name": "张延安",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议宁安市委员会",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    {
        "id": 24,
        "name": "张志超",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议宁安市委员会",
        "source": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml"
    },
    # ═══════ 前领导（徐利刃，已完成宁安任期） ═══════
    {
        "id": 25,
        "name": "徐利刃",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年4月",
        "birthplace": "黑龙江省牡丹江市",
        "education": "黑龙江大学经济学学士（工商行政管理专业）",
        "party_join": "2000年12月",
        "work_start": "1989年9月",
        "current_post": "黑龙江省政协秘书长",
        "current_org": "中国人民政治协商会议黑龙江省委员会",
        "source": "https://baike.baidu.com/item/%E5%BE%90%E5%88%A9%E5%88%83"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共宁安市委员会", "type": "党委", "level": "县级", "parent": "中共牡丹江市委员会", "location": "宁安市"},
    {"id": 2, "name": "宁安市人民政府", "type": "政府", "level": "县级", "parent": "牡丹江市人民政府", "location": "宁安市"},
    {"id": 3, "name": "中共宁安市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共宁安市委员会", "location": "宁安市"},
    {"id": 4, "name": "宁安市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "宁安市"},
    {"id": 5, "name": "中国人民政治协商会议宁安市委员会", "type": "政协", "level": "县级", "parent": "", "location": "宁安市"},
    {"id": 6, "name": "中共宁安市委员会组织部", "type": "党委部门", "level": "县级", "parent": "中共宁安市委员会", "location": "宁安市"},
    {"id": 7, "name": "中共宁安市委员会宣传部", "type": "党委部门", "level": "县级", "parent": "中共宁安市委员会", "location": "宁安市"},
    {"id": 8, "name": "宁安市人民武装部", "type": "政府部门", "level": "县级", "parent": "", "location": "宁安市"},
    {"id": 9, "name": "宁安市公安局", "type": "政府部门", "level": "县级", "parent": "宁安市人民政府", "location": "宁安市"},
    {"id": 10, "name": "中国人民政治协商会议黑龙江省委员会", "type": "政协", "level": "省级", "parent": "", "location": "哈尔滨市"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 程亮
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "市政府党组书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "经开区党工委书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 王树军
    {"person_id": 2, "org_id": 2, "title": "副市长、代市长", "start_date": "", "end_date": "", "rank": "正处级", "note": "一级调研员"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 林勇
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "", "note": "国家安全委员会办公室主任"},
    # 夏庆超
    {"person_id": 4, "org_id": 1, "title": "市委副书记（挂职）", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 胡寒冰
    {"person_id": 5, "org_id": 3, "title": "市纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "", "note": "四级高级监察官"},
    # 李树新
    {"person_id": 6, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "", "note": "市法学会会长"},
    # 张明新
    {"person_id": 7, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "", "rank": "", "note": "市政府党组副书记"},
    # 王超
    {"person_id": 8, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 张忠伟
    {"person_id": 9, "org_id": 6, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "", "note": "党校第一副校长"},
    # 杨润
    {"person_id": 10, "org_id": 8, "title": "市委常委、人武部部长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 徐竣怡
    {"person_id": 11, "org_id": 7, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 人大
    {"person_id": 12, "org_id": 4, "title": "市人大主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 13, "org_id": 4, "title": "市人大副主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 14, "org_id": 4, "title": "市人大副主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 15, "org_id": 4, "title": "市人大副主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 16, "org_id": 4, "title": "市人大副主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 政府
    {"person_id": 17, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "副市长、公安局局长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 18, "org_id": 9, "title": "公安局局长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 政协
    {"person_id": 21, "org_id": 5, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 22, "org_id": 5, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 23, "org_id": 5, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "", "note": "市工商联主席"},
    {"person_id": 24, "org_id": 5, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 徐利刃 — 前宁安市委书记
    {"person_id": 25, "org_id": 1, "title": "宁安市委书记（2017-2019）", "start_date": "2017", "end_date": "2019", "rank": "正处级→副厅级", "note": "徐利刃2010-2019在宁安工作，历任副书记、市长、书记"},
    {"person_id": 25, "org_id": 10, "title": "省政协秘书长（2025-）", "start_date": "2025-01", "end_date": "", "rank": "正厅级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 程亮 ↔ 王树军（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "程亮任市委书记，王树军任市委副书记、代市长", "overlap_org": "宁安市", "overlap_period": "2026-"},
    # 程亮 ↔ 张明新（共事）
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "张明新任市委常委、副市长，程亮为市委书记", "overlap_org": "宁安市人民政府", "overlap_period": ""},
    # 程亮 ↔ 王超（共事）
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "王超任市委常委、副市长", "overlap_org": "宁安市人民政府", "overlap_period": ""},
    # 徐利刃 → 程亮（前后任书记）
    {"person_a": 25, "person_b": 1, "type": "前后任", "context": "徐利刃2017-2019任宁安市委书记，其后继者中包括程亮", "overlap_org": "中共宁安市委员会", "overlap_period": ""},
    # 程亮 ↔ 胡寒冰（市委班子）
    {"person_a": 1, "person_b": 5, "type": "市委班子", "context": "胡寒冰任市委常委、市纪委书记", "overlap_org": "中共宁安市委员会", "overlap_period": ""},
    # 程亮 ↔ 李树新（市委班子）
    {"person_a": 1, "person_b": 6, "type": "市委班子", "context": "李树新任市委常委、政法委书记", "overlap_org": "中共宁安市委员会", "overlap_period": ""},
    # 程亮 ↔ 张忠伟（市委班子）
    {"person_a": 1, "person_b": 9, "type": "市委班子", "context": "张忠伟任市委常委、组织部部长", "overlap_org": "中共宁安市委员会", "overlap_period": ""},
    # 程亮 ↔ 徐竣怡（市委班子）
    {"person_a": 1, "person_b": 11, "type": "市委班子", "context": "徐竣怡任市委常委、宣传部部长", "overlap_org": "中共宁安市委员会", "overlap_period": ""},
    # 程亮 ↔ 林勇（市委班子）
    {"person_a": 1, "person_b": 3, "type": "市委班子", "context": "林勇任市委副书记", "overlap_org": "中共宁安市委员会", "overlap_period": ""},
    # 王树军 ↔ 张明新（政府共事）
    {"person_a": 2, "person_b": 7, "type": "政府班子", "context": "张明新任市委常委、副市长（市政府党组副书记）", "overlap_org": "宁安市人民政府", "overlap_period": ""},
    # 王树军 ↔ 王超（政府共事）
    {"person_a": 2, "person_b": 8, "type": "政府班子", "context": "王超任市委常委、副市长", "overlap_org": "宁安市人民政府", "overlap_period": ""},
    # 王树军 ↔ 林鹏（政府共事）
    {"person_a": 2, "person_b": 17, "type": "政府班子", "context": "林鹏任副市长", "overlap_org": "宁安市人民政府", "overlap_period": ""},
    # 王树军 ↔ 张鑫（政府共事）
    {"person_a": 2, "person_b": 18, "type": "政府班子", "context": "张鑫任副市长、公安局局长", "overlap_org": "宁安市人民政府", "overlap_period": ""},
    # 王树军 ↔ 李丹（政府共事）
    {"person_a": 2, "person_b": 19, "type": "政府班子", "context": "李丹任副市长", "overlap_org": "宁安市人民政府", "overlap_period": ""},
    # 王树军 ↔ 迟龙飞（政府共事）
    {"person_a": 2, "person_b": 20, "type": "政府班子", "context": "迟龙飞任副市长", "overlap_org": "宁安市人民政府", "overlap_period": ""},
    # 徐利刃 — 王树军（前后任市长关系）
    {"person_a": 25, "person_b": 2, "type": "前后任", "context": "徐利刃2011-2017任宁安市市长，王树军2026年代市长", "overlap_org": "宁安市人民政府", "overlap_period": ""},
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
    from gov_relation.schema import insert_persons
    import sqlite3

    person_files = [
        {
            "id": 1,
            "name": "程亮",
            "job": "市委书记",
            "data": {
                "identity": {
                    "person_id": "ningan_chengliang",
                    "name": "程亮",
                },
                "current_status": {
                    "current_post": "市委书记",
                    "current_org": "中共宁安市委员会",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                },
                "career_timeline": [],
                "organizations": [],
                "relationships": [],
                "governance_record": [],
                "professional_profile": {"career_pattern": "unknown"},
                "work_style_and_personality": {"caveat": "缺乏公开资料"},
                "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}],
                "source_register": [{"id": "S001", "title": "宁安市领导之窗", "url": "https://www.ningan.gov.cn/nasrmzf/c104574/ldzc.shtml", "source_type": "official", "reliability": "high"}],
                "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "low", "biggest_gap": "程亮完整履历未找到"},
                "open_questions": [{"priority": "critical", "question": "程亮的完整履历是什么？", "why_it_matters": "作为当前一把手，其职业背景对理解政治网络至关重要", "suggested_queries": ["程亮 简历 宁安", "程亮 任前公示", "程亮 百度百科"], "last_attempted": AS_OF}],
            },
        },
        {
            "id": 2,
            "name": "王树军",
            "job": "代市长",
            "data": {
                "identity": {
                    "person_id": "ningan_wangshujun",
                    "name": "王树军",
                    "ethnicity": "蒙古族",
                    "birth": "1977年1月",
                    "education": [{"degree": "研究生", "study_type": "unknown"}],
                },
                "current_status": {
                    "current_post": "副市长、代市长",
                    "current_org": "宁安市人民政府",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                },
                "career_timeline": [],
                "organizations": [],
                "relationships": [],
                "governance_record": [],
                "professional_profile": {"career_pattern": "unknown"},
                "work_style_and_personality": {"caveat": "缺乏公开资料"},
                "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}],
                "source_register": [{"id": "S001", "title": "王树军-宁安市人民政府", "url": "https://www.ningan.gov.cn/nasrmzf/c104577/202607/c03_1052791.shtml", "source_type": "official", "reliability": "high"}],
                "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "low", "biggest_gap": "王树军完整履历和晋升路径未找到"},
                "open_questions": [{"priority": "critical", "question": "王树军来宁安之前的任职经历是什么？", "why_it_matters": "了解代市长的晋升路径和政治网络", "suggested_queries": ["王树军 简历 宁安 代市长", "王树军 任前公示 牡丹江"], "last_attempted": AS_OF}],
            },
        },
        {
            "id": 25,
            "name": "徐利刃",
            "job": "前市委书记",
            "data": {
                "identity": {
                    "person_id": "ningan_xuliren",
                    "name": "徐利刃",
                    "ethnicity": "汉族",
                    "birth": "1968年4月",
                    "birthplace": "黑龙江省牡丹江市",
                    "education": [{"institution": "黑龙江大学", "major": "工商行政管理", "degree": "经济学学士", "study_type": "part_time"}],
                    "party_join": "2000年12月",
                    "work_start": "1989年9月",
                },
                "current_status": {
                    "current_post": "黑龙江省政协秘书长",
                    "current_org": "中国人民政治协商会议黑龙江省委员会",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                },
                "career_timeline": [
                    {"start": "1987-09", "end": "1989-09", "org": "牡丹江石化技工学校", "title": "学生（化工仪表专业）", "confidence": "confirmed"},
                    {"start": "1989-09", "end": "1995-05", "org": "牡丹江市制药厂", "title": "工人", "confidence": "confirmed"},
                    {"start": "1995-05", "end": "1997-06", "org": "牡丹江市金属饮料罐厂", "title": "副厂长", "confidence": "confirmed"},
                    {"start": "1997-06", "end": "1999-09", "org": "牡丹江市委政研室", "title": "综合组科员", "confidence": "confirmed"},
                    {"start": "1999-09", "end": "2002-01", "org": "牡丹江市委政研室", "title": "综合组副组长", "confidence": "confirmed"},
                    {"start": "2002-01", "end": "2004-04", "org": "牡丹江市委政研室", "title": "综合组组长", "confidence": "confirmed"},
                    {"start": "2004-04", "end": "2005-05", "org": "牡丹江市委政研室", "title": "办公室主任", "confidence": "confirmed"},
                    {"start": "2005-05", "end": "2007-07", "org": "牡丹江市委政研室", "title": "综合组组长", "confidence": "confirmed"},
                    {"start": "2007-07", "end": "2010-05", "org": "牡丹江市委政研室", "title": "副主任", "confidence": "confirmed"},
                    {"start": "2010-05", "end": "2011-11", "org": "中共宁安市委员会", "title": "市委副书记（正处级）", "confidence": "confirmed"},
                    {"start": "2011-11", "end": "2011-12", "org": "宁安市人民政府", "title": "副市长、代市长", "confidence": "confirmed"},
                    {"start": "2011-12", "end": "2017-05", "org": "宁安市人民政府", "title": "市长", "confidence": "confirmed"},
                    {"start": "2017-05", "end": "2018-01", "org": "中共宁安市委员会", "title": "市委书记、市长", "confidence": "confirmed"},
                    {"start": "2018-01", "end": "2019-05", "org": "中共宁安市委员会", "title": "市委书记", "confidence": "confirmed"},
                    {"start": "2019-05", "end": "2019-06", "org": "中共牡丹江市委", "title": "市委常委", "confidence": "confirmed"},
                    {"start": "2019-06", "end": "2021-08", "org": "中共牡丹江市委", "title": "市委常委、秘书长", "confidence": "confirmed"},
                    {"start": "2021-08", "end": "2025-01", "org": "中共绥化市委/黑龙江省委", "title": "绥化市委常委组织部部长→省委副秘书长办公厅主任", "confidence": "confirmed"},
                    {"start": "2025-01", "end": "present", "org": "黑龙江省政协", "title": "党组成员、秘书长", "confidence": "confirmed"},
                ],
                "organizations": [],
                "relationships": [
                    {"person": "程亮", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "徐利刃2017-2019任宁安市委书记，其后继者中包括程亮", "overlap_org": "中共宁安市委员会", "confidence": "plausible"},
                ],
                "governance_record": [],
                "professional_profile": {"career_pattern": "local_ladder", "primary_specializations": ["政策研究", "组织人事"], "systems_experience": ["政研室", "党委", "政府", "政协"], "geographic_pattern": ["牡丹江市", "宁安市", "绥化市", "哈尔滨市"]},
                "work_style_and_personality": {"caveat": "缺乏公开资料"},
                "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}],
                "source_register": [{"id": "S001", "title": "徐利刃-百度百科", "url": "https://baike.baidu.com/item/%E5%BE%90%E5%88%A9%E5%88%83", "source_type": "encyclopedia", "reliability": "medium"}],
                "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "complete", "relationship_confidence": "medium", "biggest_gap": "1977-1987早期教育细节"},
                "open_questions": [{"priority": "low", "question": "徐利刃的出生地具体到哪个乡镇？", "why_it_matters": "同乡关系分析", "suggested_queries": ["徐利刃 宁安 出生地"], "last_attempted": AS_OF}],
            },
        },
    ]

    for pf in person_files:
        fname = f"{TODAY}-黑龙江省-牡丹江市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  ✅ Person JSON: {path}")

    # ── Copy to canonical paths ────────────────────────────────────────
    import shutil

    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_BUILD.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_PERSONS.mkdir(parents=True, exist_ok=True)

    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
    shutil.copy2(__file__, CANONICAL_BUILD)

    for pf in person_files:
        src = PERSONS_DIR / f"{TODAY}-黑龙江省-牡丹江市-{pf['job']}-{pf['name']}.json"
        dst = CANONICAL_PERSONS / src.name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Canonical person JSON: {dst}")

    print(f"\n📦 Canonical build script: {CANONICAL_BUILD}")
    print(f"📦 Canonical DB: {CANONICAL_DB}")
    print(f"📦 Canonical GEXF: {CANONICAL_GEXF}")
    print(f"\n✅ Done — {SLUG} data build complete.")


if __name__ == "__main__":
    main()
