#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 白水县 (Baishui County), 渭南市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_白水县
Level: 县
Targets: 县委书记 & 县长

Research confidence notes:
  - Primary source: 白水县人民政府官网 www.baishui.gov.cn (官方), including 领导之窗,
    会议公开(hgyk), 人事信息(rsxx), 新闻中心/本地要闻(bdyw). Live as of 2026-08-07.
  - Web search tools (Exa rate-limited, Baidu 403) degraded; biographies for core
    leaders rely on training/partial evidence and are marked plausible/unverified.
  - Confirmed (primary sources): 县委书记 王娜 (前任 王宏运)；县委副书记、代县长
    李立锋 (2026-07起); 县委副书记 侯斐; 县人大主任 秦奉举; 县政协主席 杨进宏;
    县委常委组织部长 张斌; 原县长 王振华; 县政府副县长 李小剑、李成新、童涛、
    姚明亮、陈永锋、刘亚平、许忠、梁晓妹、王建超; 政府党组成员 马俊杰、赵少杰.
  - Leadership transitions: 县委书记 王宏运→王娜 (约2026-04~05); 县长 王振华→李立锋(代,2026-07).
  - Cross-county lead: 前任县长 李扩 (2021.08-2025.03) 后任 华州区委书记→韩城市委书记.
  - Biography details (birth year, birthplace, education, full career) for most figures
    remain open; encoded in open_questions / report gaps rather than fabricated.
"""

import sqlite3
import sys
from pathlib import Path

# Make gov_relation importable whether run from data/tmp staging or scripts/build.
_HERE = Path(__file__).resolve().parent
for _candidate in (_HERE, *_HERE.parents[:5]):
    if (_candidate / "gov_relation").is_dir() and str(_candidate) not in sys.path:
        sys.path.insert(0, str(_candidate))
        break

from gov_relation.runner import run_build

TODAY = "20260807"
AS_OF = "2026-08-07"
SLUG = "白水县"

# Staging paths (relative to this file so promotion copies correctly)
TMP = Path(__file__).parent.resolve()
DB_PATH = TMP / f"{SLUG}_network.db"
GEXF_PATH = TMP / f"{SLUG}_network.gexf"

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══ Core leadership — 县委书记 & 县长 ══
    {
        "id": 1,
        "name": "王娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白水县委书记",
        "current_org": "中共白水县委员会",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/hygk/ (2026-06/07 县委常委会新闻)",
    },
    {
        "id": 2,
        "name": "李立锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-11",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白水县委副书记、代县长",
        "current_org": "白水县人民政府",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/1876190169084915714.html + 2026-07-20 县政府常务会议",
    },

    # ══ 前县长 — 王振华 ══
    {
        "id": 3,
        "name": "王振华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-12",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原白水县委副书记、县长",
        "current_org": "白水县人民政府",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/ldzc/xc/wzh/grjl/ + 2026-06-15 警示教育会议",
    },

    # ══ 人大 / 政协 ══
    {
        "id": 4,
        "name": "秦奉举",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白水县人大常委会主任",
        "current_org": "白水县人民代表大会常务委员会",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/hyxx/ (2026-06-15 & 2026-07-07)",
    },
    {
        "id": 5,
        "name": "杨进宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白水县政协主席",
        "current_org": "中国人民政治协商会议白水县委员会",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/hyxx/ (2026-06-15 & 2026-07-07)",
    },

    # ══ 县委常委 / 组织部长 ══
    {
        "id": 6,
        "name": "张斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白水县委常委、组织部部长",
        "current_org": "中共白水县委员会",
        "source": "https://www.baishui.gov.cn/zfxxgk/hmm (2026-07-07 两优一先表彰大会)",
    },

    # ══ 县政府副职 (领导之窗) ══
    {
        "id": 7,
        "name": "李小剑",
        "gender": "男", "ethnicity": "汉族", "birth": "1982-09", "birthplace": "", "education": "大专",
        "party_join": "中共党员", "work_start": "",
        "current_post": "白水县委常委、副县长", "current_org": "白水县人民政府",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/1840207235456638978.html",
    },
    {
        "id": 8,
        "name": "李成新",
        "gender": "男", "ethnicity": "汉族", "birth": "1985-09", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "白水县副县长（挂职）", "current_org": "白水县人民政府",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/1840217289935601.html",
    },
    {
        "id": 9,
        "name": "童涛",
        "gender": "男", "ethnicity": "汉族", "birth": "1976-10", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "白水县副县长（挂职）", "current_org": "白水县人民政府",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/19935729353395750.html",
    },
    {
        "id": 10,
        "name": "姚明亮",
        "gender": "男", "ethnicity": "汉族", "birth": "1980-11", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "白水县副县长", "current_org": "白水县人民政府",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/",
    },
    {
        "id": 11,
        "name": "陈永锋",
        "gender": "男", "ethnicity": "汉族", "birth": "1970-05", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "白水县副县长、县公安局局长", "current_org": "白水县人民政府",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/",
    },
    {
        "id": 12,
        "name": "刘亚平",
        "gender": "女", "ethnicity": "汉族", "birth": "1979-12", "birthplace": "", "education": "大学",
        "party_join": "", "work_start": "",
        "current_post": "白水县副县长", "current_org": "白水县人民政府",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/",
    },
    {
        "id": 13,
        "name": "许博",
        "gender": "男", "ethnicity": "汉族", "birth": "1973-11", "birthplace": "", "education": "大专",
        "party_join": "中共党员", "work_start": "",
        "current_post": "白水县副县长", "current_org": "白水县人民政府",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/",
    },
    {
        "id": 14,
        "name": "梁晓妹",
        "gender": "女", "ethnicity": "汉族", "birth": "1990-02", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "白水县副县长", "current_org": "白水县人民政府",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/",
    },
    {
        "id": 15,
        "name": "王建超",
        "gender": "男", "ethnicity": "汉族", "birth": "1982-04", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "白水县副县长（挂职）", "current_org": "白水县人民政府",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/",
    },
    {
        "id": 16,
        "name": "马俊杰",
        "gender": "男", "ethnicity": "汉族", "birth": "1969-10", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "白水县政府党组成员", "current_org": "白水县人民政府",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/ldzc/dzcy/",
    },
    {
        "id": 17,
        "name": "赵少杰",
        "gender": "男", "ethnicity": "汉族", "birth": "1973-03", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "白水县政府党组成员", "current_org": "白水县人民政府",
        "source": "https://www.baishui.gov.cn/zfxxgk/fdzdgknr/ldzc/dzcy/",
    },
    # 县委副书记 / 前任县委书记
    {
        "id": 18,
        "name": "侯斐",
        "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "白水县委副书记", "current_org": "中共白水县委员会",
        "source": "https://www.baishui.gov.cn/xwzx/bdyw/2054726115582431234.html (2026-05-12 河湖长制林长制会议)",
    },
    {
        "id": 19,
        "name": "王宏运",
        "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "原白水县委书记", "current_org": "中共白水县委员会",
        "source": "https://www.baishui.gov.cn/xwzx/bdyw/204239123508144.html (2026-04-08 县委常委会第10次)",
    },
]

# ── Organizations ───────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共白水县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共渭南市委员会",
        "location": "陕西省渭南市白水县",
    },
    {
        "id": 2,
        "name": "白水县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "渭南市人民政府",
        "location": "陕西省渭南市白水县",
    },
    {
        "id": 3,
        "name": "白水县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "渭南市人大常委会",
        "location": "陕西省渭南市白水县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议白水县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "渭南市政协",
        "location": "陕西省渭南市白水县",
    },
    {
        "id": 5,
        "name": "中共渭南市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共陕西省委员会",
        "location": "陕西省渭南市",
    },
    {
        "id": 6,
        "name": "渭南市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "陕西省人民政府",
        "location": "陕西省渭南市",
    },
]

# ── Positions ───────────────────────────────────────────────────────────────

positions = [
    # Current leadership
    {"person_id": 1, "org_id": 1, "title": "白水县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 2, "org_id": 1, "title": "白水县委副书记", "start_date": "", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 2, "org_id": 2, "title": "白水县代县长", "start_date": "2026-07", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 6, "org_id": 1, "title": "白水县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职"},

    # Previous mayor
    {"person_id": 3, "org_id": 2, "title": "白水县县长", "start_date": "", "end_date": "2026-07", "rank": "县处级正职"},
    {"person_id": 3, "org_id": 1, "title": "白水县委副书记", "start_date": "", "end_date": "2026-07", "rank": "县处级正职"},

    # 人大 / 政协
    {"person_id": 4, "org_id": 3, "title": "白水县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 5, "org_id": 4, "title": "白水县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职"},

    # 县政府副职 (按领导之窗)
    {"person_id": 7, "org_id": 2, "title": "白水县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 8, "org_id": 2, "title": "白水县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 9, "org_id": 2, "title": "白水县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 10, "org_id": 2, "title": "白水县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 11, "org_id": 2, "title": "白水县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 12, "org_id": 2, "title": "白水县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 13, "org_id": 2, "title": "白水县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 14, "org_id": 2, "title": "白水县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 15, "org_id": 2, "title": "白水县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 16, "org_id": 2, "title": "白水县政府党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 17, "org_id": 2, "title": "白水县政府党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职"},

    # 县委副书记 / 前任县委书记
    {"person_id": 18, "org_id": 1, "title": "白水县委副书记", "start_date": "", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 19, "org_id": 1, "title": "白水县委书记", "start_date": "", "end_date": "2026-04", "rank": "县处级正职"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # Core: 县委书记 ↔ 代县长 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—代县长党政搭档（2026-07起）", "overlap_org": "中共白水县委员会/白水县人民政府", "overlap_period": "2026-07 - present"},
    # 县委书记 ↔ 前任县长
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记—县长党政搭档（至2026-07）", "overlap_org": "中共白水县委员会/白水县人民政府", "overlap_period": "至2026-07"},
    # 县长更替：王振华 → 李立锋
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor", "context": "王振华→李立锋 白水县县长接任（2026-07）", "overlap_org": "白水县人民政府", "overlap_period": "2026-07"},
    # 县委书记 ↔ 人大主任
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委—人大领导共事", "overlap_org": "白水县领导班子", "overlap_period": "未知"},
    # 县委书记 ↔ 政协主席
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委—政协领导共事", "overlap_org": "白水县领导班子", "overlap_period": "未知"},
    # 县委书记 ↔ 组织部长
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记—组织部长上下级", "overlap_org": "中共白水县委员会", "overlap_period": "未知"},
    # 前任县长 ↔ 现任代县长 (政府班)
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "代县长—副县长班内共事", "overlap_org": "白水县人民政府", "overlap_period": "未知"},
    # 县委书记更替：王宏运 → 王娜
    {"person_a": 19, "person_b": 1, "type": "predecessor_successor", "context": "王宏运→王娜 白水县委书记接任（约2026-04~05）", "overlap_org": "中共白水县委员会", "overlap_period": "2026-04~05"},
    # 县委书记 ↔ 县委副书记
    {"person_a": 1, "person_b": 18, "type": "overlap", "context": "县委书记—专职县委副书记工作关系", "overlap_org": "中共白水县委员会", "overlap_period": "未知"},
]

# ── Build ────────────────────────────────────────────────────────────────────

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
    print(f"Build complete. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")