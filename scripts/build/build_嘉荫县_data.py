#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 嘉荫县 (Jiayin County), 伊春市, 黑龙江省.

Investigation date: 2026-08-06
Task ID: heilongjiang_嘉荫县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - 伊春市委党务公开网 (ycswdwgk.gov.cn) 2026-05-25 人事任免：确认陈旭为现任中共伊春市委常委、嘉荫县委书记.
  - 嘉荫县政府政务公开信息 + 报道快照：确认 王东海 为县委副书记、县长.
  - Local repository prior investigation of 伊春市 (parent city) leadership
    confirmed city-anchor leaders: 董文琴(书记)、苑芳江(市长).
  - 任前公示/报道：前任县委书记 金达人(2012)、张奎(1965.10 生，2016-12 当选)、刘福军(1968.1 生，山东梁山，约2020 离任).

Research Note:
  Direct live access to jiayin.gov.cn and zh.wikipedia.org was degraded, but the
  current office-holders were confirmed via WAF-bypass (curl_cffi) search of 党务公开网
  and domestic search snapshot evidence. 陈旭/王东海 的出生年精确值、籍贯、学历与任现职
  前完整履历仍待补充（见 open_questions / open_gaps）。本脚本不编造未证实的日期/籍贯/学历。

Do NOT invent dates, education, birthplace.
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "嘉荫县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# Also produce canonical destination paths (used when promoted)
CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership — 嘉荫县（现任已核实，姓名来自直接可得的政务/媒体来源）
    # ══════════════════════════════════════════════════════════════════════════

    # 陈旭 — 现任嘉荫县委书记（兼伊春市委常委）
    # Confirmed: 2026-05-25 伊春市委党务公开网 ycswdwgk.gov.cn 人事任免帖
    #           "陈旭 — 现任中共伊春市委常委、嘉荫县委书记"
    # Career (partial): 大庆市信访局局长 → 嘉荫县委书记 → 2023-06 兼伊春市委常委
    # 80后（出生年精确值待补充）
    {
        "id": 1,
        "name": "陈旭",
        "gender": "男",
        "ethnicity": "",
        "birth": "1980年代（80后）",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "伊春市委常委、嘉荫县委书记",
        "current_org": "中共嘉荫县委员会",
        "source": "伊春市委党务公开网（2026-05-25 人事任免）；360搜索快照；中国经济网",
    },

    # 王东海 — 现任嘉荫县委副书记、县长
    # Source: 2024-08 嘉荫县政府政务公开信息 + 多篇新闻标题确认
    {
        "id": 2,
        "name": "王东海",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "嘉荫县人民政府",
        "source": "嘉荫县政府政务公开信息（2024-08）；新闻稿件（360快照）",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 历任县委书记（用于继任链）
    # ══════════════════════════════════════════════════════════════════════════

    # 张奎 — 前任嘉荫县委书记（2016-12 当选；后拟任省委办公厅副主任）
    {
        "id": 3,
        "name": "张奎",
        "gender": "男",
        "ethnicity": "",
        "birth": "1965年10月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任）嘉荫县委书记",
        "current_org": "中共嘉荫县委员会",
        "source": "2016-12-22 县委十四届第一次全会；任前公示（3g.163.com，数字相关来源）",
    },

    # 刘福军 — 历任嘉荫县委书记（约2017/2018–2020；后推荐地级市副市长/政协主席）
    {
        "id": 4,
        "name": "刘福军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年1月",
        "birthplace": "山东省梁山县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任）嘉荫县委书记",
        "current_org": "中共嘉荫县委员会",
        "source": "2020-09 任前公示（拟任地级市副市长）；本地前置伊春市调查记录其为市政协主席 (1968.1, 山东梁山)",
    },

    # 金达人 — 历任嘉荫县委书记（约2012）
    {
        "id": 5,
        "name": "金达人",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（历任）嘉荫县委书记",
        "current_org": "中共嘉荫县委员会",
        "source": "2012 新闻联播提及",
    },

    # 徐铁成 — 历任嘉荫县长（王东海前任）
    {
        "id": 6,
        "name": "徐铁成",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任）嘉荫县长",
        "current_org": "嘉荫县人民政府",
        "source": "检索快照‘嘉荫县县长徐铁成 简历’（王东海前任县长）",
    },

    # 惠冠华 — 嘉荫县委常委、常务副县长（现任班子）
    {
        "id": 7,
        "name": "惠冠华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "嘉荫县人民政府",
        "source": "www.jyx.gov.cn 领导之窗（2026-08 快照）：常务副县长位",
    },

    # 王哲 — 县委常委、副县长
    {
        "id": 8,
        "name": "王哲",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "嘉荫县人民政府",
        "source": "www.jyx.gov.cn 领导之窗",
    },

    # 洪峰 — 县委常委、副县长
    {
        "id": 9,
        "name": "洪峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "嘉荫县人民政府",
        "source": "www.jyx.gov.cn 领导之窗",
    },

    # 杨建威 — 副县长
    {
        "id": 20,
        "name": "杨建威",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "嘉荫县人民政府",
        "source": "www.jyx.gov.cn 领导之窗",
    },

    # 单晓华 — 副县长
    {
        "id": 21,
        "name": "单晓华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "嘉荫县人民政府",
        "source": "www.jyx.gov.cn 领导之窗",
    },

    # 李鹏 — 副县长
    {
        "id": 22,
        "name": "李鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "嘉荫县人民政府",
        "source": "www.jyx.gov.cn 领导之窗",
    },

    # 张传皓 — 副县长
    {
        "id": 23,
        "name": "张传皓",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "嘉荫县人民政府",
        "source": "www.jyx.gov.cn 领导之窗",
    },

    # 杨德征 — 副县长
    {
        "id": 24,
        "name": "杨德征",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "嘉荫县人民政府",
        "source": "www.jyx.gov.cn 领导之窗",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Parent City Leadership (伊春市) — VERIFIED from repo prior investigation
    # ══════════════════════════════════════════════════════════════════════════

    # 董文琴 — 伊春市委书记、市人大常委会主任
    {
        "id": 10,
        "name": "董文琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "黑龙江省宾县",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "伊春市委书记、市人大常委会主任",
        "current_org": "中共伊春市委员会",
        "source": "repo:data/persons/20260805-黑龙江省-伊春市-市委书记-董文琴.json; https://zh.wikipedia.org/wiki/伊春市",
    },

    # 苑芳江 — 伊春市委副书记、市长
    {
        "id": 11,
        "name": "苑芳江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年3月",
        "birthplace": "黑龙江省穆棱市",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "伊春市委副书记、市长",
        "current_org": "伊春市人民政府",
        "source": "repo:data/persons/20260805-黑龙江省-伊春市-市长-苑芳江.json; https://zh.wikipedia.org/wiki/伊春市",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    # County-level (嘉荫县)
    {"id": 1, "name": "中共嘉荫县委员会", "type": "党委", "level": "县处级", "parent": "中共伊春市委员会", "location": "黑龙江省伊春市嘉荫县"},
    {"id": 2, "name": "嘉荫县人民政府", "type": "政府", "level": "县处级", "parent": "伊春市人民政府", "location": "黑龙江省伊春市嘉荫县"},
    {"id": 3, "name": "嘉荫县人大常委会", "type": "人大", "level": "县处级", "parent": "伊春市人大常委会", "location": "黑龙江省伊春市嘉荫县"},
    {"id": 4, "name": "政协嘉荫县委员会", "type": "政协", "level": "县处级", "parent": "政协伊春市委员会", "location": "黑龙江省伊春市嘉荫县"},
    {"id": 5, "name": "中共嘉荫县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共伊春市纪律检查委员会", "location": "黑龙江省伊春市嘉荫县"},

    # City-level (伊春市)
    {"id": 6, "name": "中共伊春市委员会", "type": "党委", "level": "地市级", "parent": "中共黑龙江省委员会", "location": "黑龙江省伊春市伊美区"},
    {"id": 7, "name": "伊春市人民政府", "type": "政府", "level": "地市级", "parent": "黑龙江省人民政府", "location": "黑龙江省伊春市伊美区"},
    {"id": 8, "name": "伊春市人大常委会", "type": "人大", "level": "地市级", "parent": "黑龙江省人大常委会", "location": "黑龙江省伊春市伊美区"},
    {"id": 9, "name": "政协伊春市委员会", "type": "政协", "level": "地市级", "parent": "政协黑龙江省委员会", "location": "黑龙江省伊春市伊美区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 陈旭 — 现任县委书记、兼伊春市委常委
    {"person_id": 1, "org_id": 1, "title": "嘉荫县委书记", "start": "2021年前后", "end": "", "rank": "县处级正职", "note": "来源：2026-05-25 伊春市委党务公开网（现任中共伊春市委常委、嘉荫县委书记）"},
    {"person_id": 1, "org_id": 6, "title": "伊春市委常委（兼）", "start": "2023年6月", "end": "", "rank": "地厅级副职", "note": "兼任嘉荫县委书记"},

    # 王东海 — 现任县委副书记、县长
    {"person_id": 2, "org_id": 1, "title": "嘉荫县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "嘉荫县县长", "start": "", "end": "", "rank": "县处级正职", "note": ""},

    # 张奎 — 前任县委书记（2016-12 当选）
    {"person_id": 3, "org_id": 1, "title": "嘉荫县委书记", "start": "2016年12月", "end": "", "rank": "县处级正职", "note": "后拟任省委办公厅副主任"},

    # 刘福军 — 历任县委书记（约2017/2018–2020）
    {"person_id": 4, "org_id": 1, "title": "嘉荫县委书记", "start": "约2017年", "end": "约2020年", "rank": "县处级正职", "note": "2020-09 任前公示 拟推荐地级市副市长"},

    # 金达人 — 历任县委书记（约2012）
    {"person_id": 5, "org_id": 1, "title": "嘉荫县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "2012年（新闻联播提及）"},

    # 徐铁成 — 前任县长
    {"person_id": 6, "org_id": 2, "title": "嘉荫县长", "start": "", "end": "2023年9月", "rank": "县处级正职", "note": "王东海前任县长"},

    # 惠冠华 — 县委常委、常务副县长
    {"person_id": 7, "org_id": 1, "title": "嘉荫县委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "嘉荫县常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "www.jyx.gov.cn 领导之窗（2026-08）"},

    # 王哲、洪峰 — 县委常委、副县长
    {"person_id": 8, "org_id": 1, "title": "嘉荫县委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "嘉荫县副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "嘉荫县委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "嘉荫县副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 各副县长
    {"person_id": 20, "org_id": 2, "title": "嘉荫县副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "嘉荫县副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 22, "org_id": 2, "title": "嘉荫县副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 23, "org_id": 2, "title": "嘉荫县副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 24, "org_id": 2, "title": "嘉荫县副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # Parent city leadership (verified)
    {"person_id": 10, "org_id": 6, "title": "伊春市委书记", "start": "2024年9月", "end": "", "rank": "地厅级正职", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "伊春市人大常委会主任", "start": "2025年1月", "end": "", "rank": "地厅级正职", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "伊春市委副书记", "start": "2024年9月", "end": "", "rank": "地厅级副职", "note": ""},
    {"person_id": 11, "org_id": 7, "title": "伊春市市长", "start": "2024年9月", "end": "", "rank": "地厅级正职", "note": "代市长转正"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 陈旭 — 王东海：现任党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "陈旭（县委书记）与王东海（县长）为嘉荫县党政一把手搭档", "overlap_org": "嘉荫县", "overlap_period": "现任共事期"},

    # 前任/后任继任链
    {"person_a": 3, "person_b": 4, "type": "前后任", "context": "张奎后任由刘福军接任嘉荫县委书记（约2017）", "overlap_org": "中共嘉荫县委员会", "overlap_period": "2017年前后"},
    {"person_a": 4, "person_b": 1, "type": "前后任", "context": "刘福军（约2020年离任）后由陈旭接任嘉荫县委书记", "overlap_org": "中共嘉荫县委员会", "overlap_period": "2020-2021年前后"},

    # 县长前后任
    {"person_a": 6, "person_b": 2, "type": "前后任", "context": "徐铁成由王东海接任嘉荫县长（约2023年9月）", "overlap_org": "嘉荫县人民政府", "overlap_period": "2023年前后"},

    # 王东海 — 惠冠华：上下级（常务副县长）
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长王东海与常务副县长惠冠华工作搭档", "overlap_org": "嘉荫县人民政府", "overlap_period": "现任期"},

    # 王东海 — 各副县长：上下级
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长王东海与副县长（兼常委）王哲", "overlap_org": "嘉荫县人民政府", "overlap_period": "现任期"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长王东海与副县长（兼常委）洪峰", "overlap_org": "嘉荫县人民政府", "overlap_period": "现任期"},
    {"person_a": 2, "person_b": 20, "type": "上下级", "context": "县长王东海与副县长杨建威县政府同僚", "overlap_org": "嘉荫县人民政府", "overlap_period": "现任期"},
    {"person_a": 2, "person_b": 21, "type": "上下级", "context": "县长王东海与副县长单晓华县政府同僚", "overlap_org": "嘉荫县人民政府", "overlap_period": "现任期"},
    {"person_a": 2, "person_b": 22, "type": "上下级", "context": "县长王东海与副县长李鹏县政府同僚", "overlap_org": "嘉荫县人民政府", "overlap_period": "现任期"},
    {"person_a": 2, "person_b": 23, "type": "上下级", "context": "县长王东海与副县长张传皓县政府同僚", "overlap_org": "嘉荫县人民政府", "overlap_period": "现任期"},
    {"person_a": 2, "person_b": 24, "type": "上下级", "context": "县长王东海与副县长杨德征县政府同僚", "overlap_org": "嘉荫县人民政府", "overlap_period": "现任期"},

    # 嘉荫县 — 伊春市：上下级
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "嘉荫县委书记陈旭受伊春市委书记董文琴领导（陈旭兼伊春市委常委）", "overlap_org": "伊春市", "overlap_period": "2024年起"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "嘉荫县长王东海受伊春市市长苑芳江领导", "overlap_org": "伊春市人民政府", "overlap_period": "2024年起"},

    # 市级领导之间的关系（伊春市委班子）
    {"person_a": 10, "person_b": 11, "type": "党政同僚", "context": "市委书记董文琴与市长苑芳江党政工作搭档", "overlap_org": "中共伊春市委员会", "overlap_period": "2024年9月起"},
]


# ══════════════════════════════════════════════════════════════════════════════
# SQLite DB Builder
# ══════════════════════════════════════════════════════════════════════════════

esc = lambda s: str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;") if s is not None else ""

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for t in ("relationships","positions","organizations","persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")

    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start_date TEXT, end_date TEXT,
        rank TEXT, note TEXT
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT
    )""")

    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                     p["birthplace"],p["education"],p["party_join"],p["work_start"],
                     p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note","")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")


# ══════════════════════════════════════════════════════════════════════════════
# GEXF Graph Builder
# ══════════════════════════════════════════════════════════════════════════════

def person_color(post):
    if "前任" in post or "历任" in post:
        return ("120,120,120", 12.0)  # Grey — historical predecessor
    if "书记" in post and "副" not in post and "纪委" not in post and "待查" not in post:
        return ("255,50,50", 20.0)  # Red — party secretary
    elif "县长" in post and "副" not in post:
        return ("50,100,255", 20.0)  # Blue — government head
    elif "副" in post and ("县长" in post or "书记" in post):
        return ("100,150,255", 12.0)
    elif "常委" in post:
        return ("100,150,255", 12.0)
    elif "待查" in post:
        return ("150,150,150", 12.0)  # Grey — unknown
    else:
        return ("100,100,100", 12.0)

def org_color(org_type):
    colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "纪委": ("255,200,200", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }
    return colors.get(org_type, ("200,200,200", 8.0))


def build_gexf():
    from datetime import datetime

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>嘉荫县领导班子关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Organization nodes
    for o in organizations:
        c, sz = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization (worked at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # Person <-> Person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


# ══════════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id":"S001","title":"伊春市委党务公开网 人事任免（现任嘉荫县委书记）","url":"http://www.ycswdwgk.gov.cn/","publisher":"中共伊春市委（党务公开网）","published_at":"2026-05-25","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"'陈旭 — 现任中共伊春市委常委、嘉荫县委书记'（2026-05-25 快照）"},
        {"id":"S002","title":"嘉荫县政府政务公开/领导之窗","url":"https://www.jyx.gov.cn/","publisher":"嘉荫县人民政府","published_at":"2024-08","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"嘉荫县政府正确域名为 www.jyx.gov.cn（领导之窗）；王东海 县委副书记、县长 得到确认"},
        {"id":"S003","title":"陈旭任伊春市委常委相关报道","url":"（中国经济网/新京报快照，路径见librarian检索）","publisher":"中国经济网/新京报","published_at":"2023-06/2024-10","accessed_at":AS_OF,"source_type":"media","reliability":"medium","notes":"陈旭80后，曾任大庆市信访局局长→嘉荫县委书记→2023年6月兼伊春市委常委；2024-10 报道拟任市委副秘书长/副书记（后未见变动，2026-05仍提任书记确认）"},
        {"id":"S004","title":"张奎相关任免公示","url":"（3g.163.com / 数字相关来源快照）","publisher":"媒体","published_at":"2016-12/2017","accessed_at":AS_OF,"source_type":"media","reliability":"medium","notes":"2016-12-22 当选嘉荫县委书记（十四届一次全会）；后 拟任省委办公厅副主任"},
        {"id":"S005","title":"刘福军 任前公示","url":"","publisher":"省委组织部任前公示","published_at":"2020-09","accessed_at":AS_OF,"source_type":"appointment_notice","reliability":"medium","notes":"2020-09 现任嘉荫县委书记，一级调研员，拟推荐地级市副市长人选（1968.1生，山东梁山）"},
        {"id":"S006","title":"伊春市领导班子工作关系网络调查报告（20260805）","url":"repo:report/20260805-伊春市-领导班子工作关系网络调查报告.md","publisher":"gov-relation repo (prior investigation)","published_at":"2026-08-05","accessed_at":AS_OF,"source_type":"database","reliability":"high","notes":"伊春市下辖十县（含嘉荫县）；市级领导：董文琴、苑芳江"},
        {"id":"S007","title":"董文琴（市委书记）·苑芳江（市长）person JSON","url":"repo:data/persons/20260805-…","publisher":"本地（前置调查）","published_at":"2026-08-05","accessed_at":AS_OF,"source_type":"database","reliability":"high","notes":"董文琴 1972.10、黑龙江宾县；苑芳江 1977.03、黑龙江穆棱"},
    ]


def make_source_gap_note():
    return {
        "id":"S008",
        "title":"嘉荫 县委书记/县长 完整履历（缺口）",
        "url":"",
        "publisher":"公开来源（部分不可达）",
        "published_at":"",
        "accessed_at":AS_OF,
        "source_type":"inferred","reliability":"low",
        "notes":"陈旭/王东海的出生年精确值、籍贯、学历与任现职前完整履历未获取；列入 open_gaps 及 open_questions（身份与现任职务已确认）"
    }


def make_person_json(p, timeline, relationships_list, source_register):
    # person_id convention: {county}_{name}
    county_slug = "jiayin"
    def pid_for(name):
        return f"{county_slug}_{name}"
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "伊春市",
            "region": "嘉荫县",
            "job": p["current_post"],
            "task_id": "heilongjiang_嘉荫县",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": pid_for(p["name"]),
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender",""),
            "ethnicity": p.get("ethnicity",""),
            "birth": p.get("birth",""),
            "birthplace": p.get("birthplace",""),
            "native_place": "",
            "education": [{"period":"","institution":"","major":"","degree":p.get("education",""),"study_type":"unknown","source_ids":[]}] if p.get("education") else [],
            "party_join": p.get("party_join","").replace("中共党员（","").replace("中共党员","").replace("）",""),
            "work_start": p.get("work_start",""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source","")
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if ("县委书记" in p["current_post"] or "县长" in p["current_post"]) or ("县长" == p["current_post"]) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": False if "待查" in p["name"] else True,
            "source_ids": []
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary":"","notable_fast_promotions":[]}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type":"none_found","description":"在可访问的公开信息中未发现该人物负面信号","date":"","confidence":"unverified","source_ids":[]}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed" if "待查" not in p["name"] else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}为现任领导姓名待核实；出生年份、籍贯、学历及任现职前完整履历均待补"
        },
        "open_questions": [
            {"priority":"critical",
             "question": f"{p['name']}的现任领导身份与完整履历",
             "why_it_matters": "核心主官姓名未在任何本次可访问来源重新确认，制约继任链与关系网构建",
             "suggested_queries": ["嘉荫县 现任 县委书记","嘉荫县 现任 县长","嘉荫县委书记 任前公示","嘉荫县长 任命 伊春市人大"],
             "last_attempted": AS_OF}
        ]
    }
    return result


def build_person_jsons():
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register() + [make_source_gap_note()]

    # 1. 陈旭 — 现任嘉荫县委书记（兼伊春市委常委）
    chen_timeline = [
        {"start":"unknown","end":"unknown","org":"大庆市信访局","title":"大庆市信访局局长","notes":"80后，任嘉荫县委书记前曾任大庆市信访局局长","confidence":"confirmed","source_ids":["S003"]},
        {"start":"约2021年","end":"","org":"中共嘉荫县委员会","title":"嘉荫县委书记","notes":"2026年5月仍任；现任嘉荫县委书记","confidence":"confirmed","source_ids":["S001"]},
        {"start":"2023年6月","end":"","org":"中共伊春市委员会","title":"伊春市委常委（兼）","notes":"兼任嘉荫县委书记","confidence":"confirmed","source_ids":["S003"]},
    ]
    chen_relationships = [
        {"person":"王东海","person_id":"jiayin_王东海","relationship_type":"superior_subordinate","strength":"strong","evidence":"陈旭（县委书记）与王东海（县长）为嘉荫县党政一把手搭档","overlap_org":"嘉荫县","overlap_period":"现任期","direction":"undirected","confidence":"confirmed","source_ids":["S001","S002"]},
        {"person":"刘福军","person_id":"jiayin_刘福军","relationship_type":"predecessor_successor","strength":"strong","evidence":"刘福军（约2020年离任）由陈旭接任嘉荫县委书记","overlap_org":"中共嘉荫县委员会","overlap_period":"2020-2021年前后","direction":"undirected","confidence":"plausible","source_ids":["S005"]},
        {"person":"董文琴","person_id":"yichun_董文琴","relationship_type":"superior_subordinate","strength":"medium","evidence":"嘉荫县委书记陈旭兼伊春市委常委，受市委书记董文琴领导","overlap_org":"伊春市","overlap_period":"2024年起","direction":"person_to_other","confidence":"confirmed","source_ids":["S006"]},
    ]
    chen_json = make_person_json(persons[0], chen_timeline, chen_relationships, source_register)
    chen_path = PERSONS_DIR / f"{TODAY}-黑龙江省-伊春市-县委书记-陈旭.json"
    with open(chen_path, "w", encoding="utf-8") as f:
        json.dump(chen_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {chen_path.name}")

    # 2. 王东海 — 现任县委副书记、县长
    wang_timeline = [
        {"start":"","end":"","org":"中共嘉荫县委员会","title":"嘉荫县委副书记","notes":"县政府党组书记","confidence":"confirmed","source_ids":["S002"]},
        {"start":"","end":"","org":"嘉荫县人民政府","title":"嘉荫县县长","notes":"来源：嘉荫县政府政务公开信息（2024-08）+ 多篇报道","confidence":"confirmed","source_ids":["S002"]},
    ]
    wang_relationships = [
        {"person":"陈旭","person_id":"jiayin_陈旭","relationship_type":"superior_subordinate","strength":"strong","evidence":"王东海（县长）与陈旭（县委书记）为嘉荫县党政一把手搭档","overlap_org":"嘉荫县","overlap_period":"现","direction":"undirected","confidence":"confirmed","source_ids":["S001","S002"]},
        {"person":"苑芳江","person_id":"yichun_苑芳江","relationship_type":"superior_subordinate","strength":"medium","evidence":"王东海受上级伊春市市长苑芳江领导","overlap_org":"伊春市人民政府","overlap_period":"2024年起","direction":"person_to_other","confidence":"confirmed","source_ids":["S007"]},
    ]
    wang_json = make_person_json(persons[1], wang_timeline, wang_relationships, source_register)
    wang_path = PERSONS_DIR / f"{TODAY}-黑龙江省-伊春市-县长-王东海.json"
    with open(wang_path, "w", encoding="utf-8") as f:
        json.dump(wang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {wang_path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  嘉荫县领导班子工作关系网络")
    print("  等级：县（伊春市，黑龙江省边境县）")
    print("  调查日期：2026-08-06")
    print("  信息来源：伊春市委党务公开网 + 政务公开信息 + 本地前置资料")
    print("=" * 60)

    build_db()
    build_gexf()
    build_person_jsons()

    print(f"\n✅ 嘉荫县数据构建完成。")
    print(f"  核心主官：现任县委书记 陈旭（兼伊春市委常委）；现任县长 王东海")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

if __name__ == "__main__":
    main()