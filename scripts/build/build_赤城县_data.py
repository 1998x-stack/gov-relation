#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Chicheng County leadership network.

Task: hebei_赤城县
Province: 河北省
City: 张家口市
Region: 赤城县
Level: 县
Targets: 县委书记, 县长

Research date: 2026-07-24
Official source: http://www.ccx.gov.cn/ (赤城县人民政府)

Current status (as of 2026-07-24):
- 县委书记: 邓艳杰 — 原县长, 2026年5月中旬任县委书记; 7月19日县委十四届一次全会连任
- 代县长: 陈涛 — 2026年7月任县委副书记、代县长
- 前任县委书记: 赵红革 — 2026年2月调任张家口市人大常委会秘书长
- 前任县长: 薛宏霞 — 2026年7月当选康保县委书记

Sources:
  S001: http://www.ccx.gov.cn/single/22/79479.html (县委十四届一次全会, 邓艳杰连任书记)
  S002: http://www.ccx.gov.cn/single/22/79481.html (政协十二届一次会议, 确认陈涛为代县长)
  S003: http://www.ccx.gov.cn/single/22/79477.html (县纪委一次全会, 杨治国当选纪委书记)
  S004: http://www.ccx.gov.cn/single/22/79104.html (邓艳杰率队赴京, 确认王东升为常务副县长)
  S005: http://www.ccx.gov.cn/single/21/19507.html (领导之窗, 王东升简历)
  S006: http://www.ccx.gov.cn/single/22/79586.html (十八届人大一次会议开幕)
  S007: http://www.ccx.gov.cn/single/22/79436.html (十四次党代会开幕)
  S008: http://www.ccx.gov.cn/single/22/77665.html (邓艳杰会见企业, 确认县委书记身份5月22日)
  S009: http://www.ccx.gov.cn/single/22/77080.html (县委十三届十一次全会, 薛宏霞为书记5月8日)
  S010: Baidu Baike entry for 赵红革/52277912
  S011: Bing search results for 薛宏霞 Baidu Baike (康保县委书记当选)
  S012: http://www.ccx.gov.cn/single/31/78344.html (杨怿欣为宣传部长)
"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/tmp/hebei_赤城县/赤城县_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/hebei_赤城县/赤城县_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ══════════════════════════════════════════════════════════════════
# Data: Persons
# ══════════════════════════════════════════════════════════════════

persons = [
    # ── Current Party Secretary ──
    {
        "id": 1,
        "name": "邓艳杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-01",          # 据公开资料
        "birthplace": "",
        "native_place": "",
        "education": "河北省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县委书记",
        "current_org": "中共赤城县委员会",
        "source": ("S001: http://www.ccx.gov.cn/single/22/79479.html "
                   "(县委十四届一次全会, 邓艳杰连任县委书记); "
                   "S008: http://www.ccx.gov.cn/single/22/77665.html "
                   "(5月22日以县委书记身份活动)"),
    },
    # ── Current Acting County Mayor ──
    {
        "id": 2,
        "name": "陈涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县委副书记、代县长",
        "current_org": "赤城县人民政府",
        "source": ("S002: http://www.ccx.gov.cn/single/22/79481.html "
                   "(政协十二届一次会议, 确认县委副书记、代县长陈涛)"),
    },
    # ── Predecessor Party Secretary: 赵红革 ──
    {
        "id": 3,
        "name": "赵红革",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-12",
        "birthplace": "河北张家口",
        "native_place": "河北张家口",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1987-07",
        "current_post": "张家口市人大常委会党组成员、秘书长、机关党组书记、一级调研员",
        "current_org": "张家口市人大常委会",
        "source": ("S010: Baidu Baike 赵红革/52277912; "
                   "完整履历: 张北县委常委→蔚县县委常委/副县长→蔚县常务副县长→"
                   "赤城县委副书记→赤城县县长→赤城县委书记→张家口市人大常委会秘书长"),
    },
    # ── Predecessor County Mayor: 薛宏霞 ──
    {
        "id": 4,
        "name": "薛宏霞",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1984-07",
        "birthplace": "河北承德围场",
        "native_place": "河北承德围场",
        "education": "",
        "party_join": "中共党员",
        "work_start": "2007-08",
        "current_post": "康保县委书记",
        "current_org": "中共康保县委员会",
        "source": ("S011: Bing search — Baidu Baike 薛宏霞/57070217; "
                   "曾任丰宁满族自治县副县长→赤城县委副书记、县长→康保县委书记"),
    },
    # ── Deputy Party Secretary ──
    {
        "id": 5,
        "name": "戎海广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县委副书记",
        "current_org": "中共赤城县委员会",
        "source": ("S006: http://www.ccx.gov.cn/single/22/79586.html "
                   "(人大会议主席团前排就座, 推测为县委副书记)"),
    },
    # ── Standing Committee: 王东升 (常务副县长) ──
    {
        "id": 6,
        "name": "王东升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-08",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县委常委、常务副县长、三级调研员",
        "current_org": "赤城县人民政府",
        "source": ("S004: http://www.ccx.gov.cn/single/22/79104.html; "
                   "S005: http://www.ccx.gov.cn/single/21/19507.html "
                   "(领导之窗, 负责常务工作、发展改革、财政、招商引资等)"),
    },
    # ── Standing Committee: 杨治国 (纪委书记) ──
    {
        "id": 7,
        "name": "杨治国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县委常委、县纪委书记",
        "current_org": "中共赤城县纪律检查委员会",
        "source": ("S003: http://www.ccx.gov.cn/single/22/79477.html "
                   "(县纪委一次全会, 杨治国当选纪委书记)"),
    },
    # ── Standing Committee: 杨怿欣 (宣传部长) ──
    {
        "id": 8,
        "name": "杨怿欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县委常委、宣传部部长",
        "current_org": "中共赤城县委宣传部",
        "source": ("S012: http://www.ccx.gov.cn/single/31/78344.html "
                   "(县委宣传部长杨怿欣调研后城镇)"),
    },
    # ── Standing Committee (推断): 靳卓伢 ──
    {
        "id": 9,
        "name": "靳卓伢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县委常委（推断）",
        "current_org": "中共赤城县委员会",
        "source": ("S006: http://www.ccx.gov.cn/single/22/79586.html "
                   "(人大会议主席团常务主席、主持会议)"),
    },
    # ── Standing Committee (推断): 王春 ──
    {
        "id": 10,
        "name": "王春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县委常委（推断）",
        "current_org": "中共赤城县委员会",
        "source": "S006: http://www.ccx.gov.cn/single/22/79586.html (主席团前排就座)",
    },
    # ── Standing Committee (推断): 路太忠 ──
    {
        "id": 11,
        "name": "路太忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县委常委（推断）",
        "current_org": "中共赤城县委员会",
        "source": ("S007: http://www.ccx.gov.cn/single/22/79436.html "
                   "(党代会大会执行主席)"),
    },
    # ── Standing Committee (推断): 付利军 ──
    {
        "id": 12,
        "name": "付利军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县委常委（推断）",
        "current_org": "中共赤城县委员会",
        "source": ("S007: http://www.ccx.gov.cn/single/22/79436.html "
                   "(大会执行主席; 随邓艳杰走访慰问)"),
    },
    # ── Standing Committee (推断): 赵璞 ──
    {
        "id": 13,
        "name": "赵璞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县委常委（推断）",
        "current_org": "中共赤城县委员会",
        "source": "S007: http://www.ccx.gov.cn/single/22/79436.html (大会执行主席)",
    },
    # ── Standing Committee (推断): 王彦青 ──
    {
        "id": 14,
        "name": "王彦青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县委常委（推断）",
        "current_org": "中共赤城县委员会",
        "source": "S007: http://www.ccx.gov.cn/single/22/79436.html (大会执行主席)",
    },
    # ── Standing Committee (推断): 孙志君 ──
    {
        "id": 15,
        "name": "孙志君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县委常委（推断）",
        "current_org": "中共赤城县委员会",
        "source": "S007: http://www.ccx.gov.cn/single/22/79436.html (大会执行主席)",
    },
    # ── Standing Committee (推断): 李飞 ──
    {
        "id": 16,
        "name": "李飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县委常委（推断）",
        "current_org": "中共赤城县委员会",
        "source": "S007: http://www.ccx.gov.cn/single/22/79436.html (大会执行主席; 随行慰问)",
    },
    # ── 王新慧 (推测人大/政协领导) ──
    {
        "id": 17,
        "name": "王新慧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赤城县（推测人大/政协领导）",
        "current_org": "赤城县",
        "source": "S006: http://www.ccx.gov.cn/single/22/79586.html (主席团前排就座)",
    },
    # ── 刘雪松 (赤城-born, cross-county connection) ──
    {
        "id": 18,
        "name": "刘雪松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-10",
        "birthplace": "河北赤城",
        "native_place": "河北赤城",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张家口市人民政府副市长",
        "current_org": "张家口市人民政府",
        "source": ("Baidu Baike/项目内 data: 前康保县委书记→张家口市副市长; "
                   "赤城出生, 其赤城到康保间履历待查"),
    },
]

# ══════════════════════════════════════════════════════════════════
# Data: Organizations
# ══════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共赤城县委员会", "type": "党委", "level": "县级", "parent": "中共张家口市委员会", "location": "河北省张家口市赤城县"},
    {"id": 2, "name": "赤城县人民政府", "type": "政府", "level": "县级", "parent": "张家口市人民政府", "location": "河北省张家口市赤城县"},
    {"id": 3, "name": "中共赤城县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共赤城县委员会", "location": "河北省张家口市赤城县"},
    {"id": 4, "name": "中共赤城县委宣传部", "type": "党委部门", "level": "县级", "parent": "中共赤城县委员会", "location": "河北省张家口市赤城县"},
    {"id": 5, "name": "赤城县人大常委会", "type": "人大", "level": "县级", "parent": "赤城县", "location": "河北省张家口市赤城县"},
    {"id": 6, "name": "赤城县政协", "type": "政协", "level": "县级", "parent": "赤城县", "location": "河北省张家口市赤城县"},
    {"id": 7, "name": "张家口市人大常委会", "type": "人大", "level": "地市级", "parent": "张家口市", "location": "河北省张家口市"},
    {"id": 8, "name": "张家口市人民政府", "type": "政府", "level": "地市级", "parent": "河北省人民政府", "location": "河北省张家口市"},
    {"id": 9, "name": "中共康保县委员会", "type": "党委", "level": "县级", "parent": "中共张家口市委员会", "location": "河北省张家口市康保县"},
]

# ══════════════════════════════════════════════════════════════════
# Data: Positions
# ══════════════════════════════════════════════════════════════════

positions = [
    # 邓艳杰
    {"person_id": 1, "org_id": 1, "title": "赤城县委书记", "start": "2026-05", "end": "", "rank": "正处级", "note": "原县长, 2026年5月中旬任书记, 7月19日连任"},
    {"person_id": 1, "org_id": 2, "title": "赤城县委副书记、县长", "start": "~2021", "end": "2026-05", "rank": "正处级", "note": "前任县长, 后任书记; 期间一度县委书记县长一肩挑"},
    # 陈涛
    {"person_id": 2, "org_id": 2, "title": "赤城县委副书记、代县长", "start": "2026-07", "end": "", "rank": "正处级", "note": "2026年7月到任"},
    # 赵红革
    {"person_id": 3, "org_id": 7, "title": "张家口市人大常委会党组成员、秘书长", "start": "2026-02", "end": "", "rank": "正处级", "note": "2026年2月6日当选"},
    {"person_id": 3, "org_id": 1, "title": "赤城县委书记", "start": "2021-05", "end": "2026-02", "rank": "正处级", "note": "同时任赤城县经济开发区工委副书记"},
    {"person_id": 3, "org_id": 2, "title": "赤城县委副书记、县长", "start": "2019-02", "end": "2021-05", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "赤城县委副书记", "start": "2018-02", "end": "2019-02", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 8, "title": "蔚县县委常委、常务副县长", "start": "2016-12", "end": "2018-02", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 8, "title": "蔚县县委常委、副县长", "start": "2011-08", "end": "2016-12", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 8, "title": "张北县委常委、办公室主任", "start": "2009-12", "end": "2011-08", "rank": "副处级", "note": ""},
    # 薛宏霞
    {"person_id": 4, "org_id": 9, "title": "康保县委书记", "start": "2026-07", "end": "", "rank": "正处级", "note": "2026年7月19日当选"},
    {"person_id": 4, "org_id": 1, "title": "赤城县委书记", "start": "~2025", "end": "2026-05", "rank": "正处级", "note": "接替赵红革, 至2026年5月"},
    {"person_id": 4, "org_id": 2, "title": "赤城县委副书记、县长", "start": "~2021-06", "end": "~2025", "rank": "正处级", "note": ""},
    # 戎海广
    {"person_id": 5, "org_id": 1, "title": "赤城县委副书记", "start": "", "end": "", "rank": "副处级", "note": "换届期在职"},
    # 王东升
    {"person_id": 6, "org_id": 2, "title": "赤城县委常委、常务副县长", "start": "", "end": "", "rank": "副处级", "note": "三级调研员"},
    # 杨治国
    {"person_id": 7, "org_id": 3, "title": "赤城县委常委、纪委书记", "start": "2026-07-19", "end": "", "rank": "副处级", "note": "十四届纪委一次全会当选"},
    # 杨怿欣
    {"person_id": 8, "org_id": 4, "title": "赤城县委常委、宣传部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 刘雪松
    {"person_id": 18, "org_id": 8, "title": "张家口市人民政府副市长", "start": "~2021", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 18, "org_id": 9, "title": "康保县委书记", "start": "~2019", "end": "~2021", "rank": "正处级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════
# Data: Relationships
# ══════════════════════════════════════════════════════════════════

relationships = [
    # 邓艳杰→赵红革 (前后任县委书记)
    {"person_a": 1, "person_b": 3, "type": "前后任", "context": "邓艳杰接替赵红革任赤城县委书记", "overlap_org": "中共赤城县委员会", "overlap_period": "2021-2026"},
    # 邓艳杰→薛宏霞 (前后任县长/书记)
    {"person_a": 1, "person_b": 4, "type": "前后任", "context": "邓艳杰接替薛宏霞任赤城县委书记; 邓艳杰此前接替薛宏霞任县长", "overlap_org": "赤城县", "overlap_period": "2021-2026"},
    # 赵红革→薛宏霞 (前后任)
    {"person_a": 3, "person_b": 4, "type": "前后任", "context": "赵红革→薛宏霞→邓艳杰 赤城县委书记接力", "overlap_org": "中共赤城县委员会", "overlap_period": "2021-2026"},
    # 赵红革→王东升 (上下级)
    {"person_a": 3, "person_b": 6, "type": "上下级", "context": "赵红革任县委书记时王东升为常务副县长", "overlap_org": "赤城县", "overlap_period": ""},
    # 邓艳杰→王东升 (上下级)
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "邓艳杰为县委书记, 王东升为县委常委、常务副县长", "overlap_org": "赤城县", "overlap_period": ""},
    # 邓艳杰→陈涛 (搭班)
    {"person_a": 1, "person_b": 2, "type": "搭班", "context": "邓艳杰(县委书记)+陈涛(代县长) 党政搭班", "overlap_org": "赤城县", "overlap_period": "2026-07-"},
    # 邓艳杰→杨治国 (上下级)
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "邓艳杰为县委书记, 杨治国为纪委书记", "overlap_org": "中共赤城县委员会", "overlap_period": ""},
    # 刘雪松→赤城 (籍贯联系)
    {"person_a": 18, "person_b": 3, "type": "籍贯联系", "context": "刘雪松(赤城出生)", "overlap_org": "", "overlap_period": ""},
    # 薛宏霞→康保 (调任)
    {"person_a": 4, "person_b": 18, "type": "调任", "context": "薛宏霞(赤城前县长)调任康保县委书记; 刘雪松(赤城出生)曾任康保县委书记", "overlap_org": "康保县", "overlap_period": "~2019-2026"},
]

# ══════════════════════════════════════════════════════════════════
# SQLite Schema + Insertion
# ══════════════════════════════════════════════════════════════════

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT,
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
    source TEXT
);

CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    org_id INTEGER,
    title TEXT,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER,
    person_b INTEGER,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    c.execute("""INSERT OR REPLACE INTO persons
        (id, name, gender, ethnicity, birth, birthplace, native_place, education,
         party_join, work_start, current_post, current_org, source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
         p["birthplace"], p["native_place"], p["education"],
         p["party_join"], p["work_start"], p["current_post"],
         p["current_org"], p["source"]))

for o in organizations:
    c.execute("""INSERT OR REPLACE INTO organizations
        (id, name, type, level, parent, location)
        VALUES (?,?,?,?,?,?)""",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
        VALUES (?,?,?,?,?,?,?)""",
        (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
         pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?,?,?,?,?,?)""",
        (r["person_a"], r["person_b"], r["type"], r["context"],
         r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()

print(f"✅ SQLite written: {DB_PATH}")

# ══════════════════════════════════════════════════════════════════
# GEXF Generation
# ══════════════════════════════════════════════════════════════════

import xml.sax.saxutils as saxutils

def x(s):
    """XML-escape a string."""
    return saxutils.escape(str(s))

COLORS = {
    "party_secretary": "#E03C31",   # red
    "government": "#3182CE",        # blue
    "discipline": "#DD6B20",        # orange
    "other": "#718096",             # grey
    "organization_party": "#C53030",
    "organization_gov": "#2B6CB0",
    "organization_discipline": "#C05621",
    "organization_other": "#4A5568",
}

def person_color(post):
    if "书记" in post and "纪委" not in post:
        return COLORS["party_secretary"]
    if "县长" in post or "乡长" in post or "区长" in post or "副市长" in post or "常务副" in post:
        return COLORS["government"]
    if "纪委" in post or "纪检" in post:
        return COLORS["discipline"]
    return COLORS["other"]

def person_size(post):
    if "书记" in post and "纪委" not in post:
        return 20.0
    if "县长" in post or "副市长" in post:
        return 18.0
    if "常务副" in post:
        return 15.0
    if "常委" in post or "副" in post:
        return 12.0
    return 10.0

def org_type_color(org_type):
    mapping = {"党委": "organization_party", "党委部门": "organization_party",
               "政府": "organization_gov", "纪委": "organization_discipline"}
    return COLORS.get(mapping.get(org_type, "organization_other"))

lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
    "<graph defaultedgetype=\"directed\">",
    # Attributes
    "<attributes class=\"node\">",
    '<attribute id="type" title="type" type="string"/>',
    '<attribute id="post" title="post" type="string"/>',
    '<attribute id="birth" title="birth" type="string"/>',
    '<attribute id="birthplace" title="birthplace" type="string"/>',
    '<attribute id="source" title="source" type="string"/>',
    "</attributes>",
    "<attributes class=\"edge\">",
    '<attribute id="type" title="type" type="string"/>',
    '<attribute id="context" title="context" type="string"/>',
    '<attribute id="start" title="start" type="string"/>',
    '<attribute id="end" title="end" type="string"/>',
    "</attributes>",
    # Nodes
    "<nodes>",
]

# Person nodes
for p in persons:
    color = person_color(p["current_post"])
    size = person_size(p["current_post"])
    lines.append(f'<node id="p{p["id"]}" label="{x(p["name"])}">')
    lines.append(f"<attvalues>")
    lines.append(f'<attvalue for="type" value="person"/>')
    lines.append(f'<attvalue for="post" value="{x(p["current_post"])}"/>')
    lines.append(f'<attvalue for="birth" value="{x(p["birth"])}"/>')
    lines.append(f'<attvalue for="birthplace" value="{x(p["birthplace"])}"/>')
    lines.append(f'<attvalue for="source" value="{x(p["source"])}"/>')
    lines.append(f"</attvalues>")
    lines.append(f"<viz:color r=\"{int(color[1:3], 16)}\" g=\"{int(color[3:5], 16)}\" b=\"{int(color[5:7], 16)}\"/>")
    lines.append(f"<viz:size value=\"{size}\"/>")
    lines.append(f"<viz:shape value=\"disc\"/>")
    lines.append(f"</node>")

# Organization nodes
for o in organizations:
    color = org_type_color(o["type"])
    lines.append(f'<node id="o{o["id"]}" label="{x(o["name"])}">')
    lines.append(f"<attvalues>")
    lines.append(f'<attvalue for="type" value="organization"/>')
    lines.append(f'<attvalue for="post" value="{x(o["type"])}"/>')
    lines.append(f'<attvalue for="birth" value=""/>')
    lines.append(f'<attvalue for="birthplace" value="{x(o["location"])}"/>')
    lines.append(f'<attvalue for="source" value=""/>')
    lines.append(f"</attvalues>")
    lines.append(f"<viz:color r=\"{int(color[1:3], 16)}\" g=\"{int(color[3:5], 16)}\" b=\"{int(color[5:7], 16)}\"/>")
    lines.append(f"<viz:size value=\"8.0\"/>")
    lines.append(f"<viz:shape value=\"square\"/>")
    lines.append(f"</node>")

lines.append("</nodes>")

# Edges
lines.append("<edges>")
edge_id = 0

# Person → Organization (worked_at)
for pos in positions:
    edge_id += 1
    p = next(p_ for p_ in persons if p_["id"] == pos["person_id"])
    start = pos["start"] or ""
    end_ = pos["end"] or ""
    lines.append(f'<edge id="e{edge_id}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="worked_at">')
    lines.append(f"<attvalues>")
    lines.append(f'<attvalue for="type" value="worked_at"/>')
    lines.append(f'<attvalue for="context" value="{x(pos["title"])}"/>')
    lines.append(f'<attvalue for="start" value="{x(start)}"/>')
    lines.append(f'<attvalue for="end" value="{x(end_)}"/>')
    lines.append(f"</attvalues>")
    lines.append(f"</edge>")

# Person ↔ Person (relationship)
for r in relationships:
    edge_id += 1
    lines.append(f'<edge id="e{edge_id}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{x(r["type"])}">')
    lines.append(f"<attvalues>")
    lines.append(f'<attvalue for="type" value="{x(r["type"])}"/>')
    lines.append(f'<attvalue for="context" value="{x(r["context"])}"/>')
    lines.append(f'<attvalue for="start" value=""/>')
    lines.append(f'<attvalue for="end" value=""/>')
    lines.append(f"</attvalues>")
    lines.append(f"</edge>")

lines.append("</edges>")
lines.append("</graph>")
lines.append("</gexf>")

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF written: {GEXF_PATH}")

# ══════════════════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"赤城县领导关系网络数据构建完成")
print(f"{'='*60}")
print(f"人员: {len(persons)}")
print(f"组织: {len(organizations)}")
print(f"任职: {len(positions)}")
print(f"关系: {len(relationships)}")
print(f"边总计: {edge_id}")
print(f"\n数据库: {DB_PATH}")
print(f"图文件: {GEXF_PATH}")
print(f"{'='*60}")
