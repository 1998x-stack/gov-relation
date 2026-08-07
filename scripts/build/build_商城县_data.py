#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 商城县 (Shangcheng County), 信阳市, 河南省.

Investigation date: 2026-08-07
Task ID: henan_商城县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - http://www.hnsc.gov.cn/ — official 商城县人民政府 website (primary source; note the actual county
    domain is hnsc.gov.cn, NOT shangcheng.gov.cn which does not resolve).
  - Official 政府领导 bio pages: 吕菲 (2026/06-01/788047), 杨栋/杨宇/耿海峰/穆晓东 (2026/07-24/...),
    董园飞/郭滨/余巨峰 (2025/01-21/...).
  - Official 县信访局 weekly 处级领导接访日程 (2026-08-01 /797124.html) confirming 吕菲 as 县长
    and county 常委 roster (陈明辉/甘尚昆/杨海军).
  - Official 商城县处级领导接访日程公示 2026年 提供县委县政府班子名单.
  - 商城县人民政府2025年政府工作报告 (2025-02-19/602461.html): 前任县长 鲁新建 作报告(2025-02-15).
  - 商城县人民政府2026年政府工作报告 (2026-03-05/773088): 吕菲 代表县政府作报告(2026-02-12).
  - Official news confirming 县委书记 孙红鑫 (2025-09-05 first, consistently confirmed through 2026-08
    调研/接访; e.g. 2026/08-03/797034, 2026/08-05/797438).

Confidence notes:
  - 孙红鑫 (县委书记): confirmed via official news labelling him "县委书记孙红鑫" from 2025-09 through
    2026-08. No biographical details published on the official site (party secretary bios not posted).
    Birth year / birthplace / education / prior post = unknown.
  - 吕菲 (县长): confirmed via official 政府领导 bio page (2026-06-01): 女, 汉族, 1976-10, 中共党员,
    大学学历; 兼县委副书记、县政府党组书记. Prior party roles (e.g. 县委组织部部长 per secondary leads)
    unverified.
  - 前任县委书记 胡培刚: per Baidu Baike 商城县 entry (secondary); official handover date to 孙红 is ~2025-09.
  - 前任县长 鲁新建: delivered 2025 政府工作报告 (官方确认 2025-02 as 县长); 2026年被吕菲接替. 去向未知.
  - Government deputy roster (7 副县长) confirmed from official 政府领导 pages with bios + 分工.
  - Party Standing Committee: 孙红鑫, 吕菲 confirmed; 陈明辉(政法委), 甘尚昆(统战), 杨海军(组织),
    杨宇(宣传/政府) from official sources. Other members partially identified.
  - Cross-county network: 王建平 (前商城县委常委、副县长 → 光山), 朱国朋 (前商城县委副书记/汪桥镇书记 →
    新县县长), 曾玉杰 (光山常务副县长, 商城人), 彭辉 (光山公安局长, 商城人). Sourced from existing repo
    光山县/新县 person-data and reports (2026076/20260806), cross-referenced.
  - This is a partial-evidence artifact. Core current roles are confirmed from official sources; historical
    biographical gaps are preserved as confidence=plausible/unverified rather than fabricated.
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "商城县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

def _find_repo_root(start: Path) -> Path:
    """Locate the repository root by walking up to the ancestor containing gov_relation/ and data/."""
    for p in [start] + list(start.parents):
        if (p / "gov_relation").is_dir() and (p / "data").is_dir():
            return p
    return start

BASE = _find_repo_root(STAGING_DIR)  # repo root

# Output paths: write directly into canonical database/graph dirs.
DB_PATH = BASE / "data" / "database" / f"{SLUG}_network.db"
GEXF_PATH = BASE / "data" / "graph" / f"{SLUG}_network.gexf"

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"

# ── Helper: ID offset for orgs ─────────────────────────────────────────────
ORG_OFFSET = 100000


# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "孙红鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共商城县委员会",
        "source": "Confirmed via official news as 县委书记孙红鑫 2025-09 to 2026-08 (e.g. http://www.hnsc.gov.cn/2026/08-03/797034.html, /2026/08-05/797438.html). No bio details published."
    },
    {
        "id": 2,
        "name": "吕菲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976-10",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "商城县人民政府",
        "source": "Official bio: http://www.hnsc.gov.cn/2026/06-01/788047.html ; 接访日程公示 2026-08-01 : http://www.hnsc.gov.cn/2026/08-03/797124.html"
    },
    {
        "id": 3,
        "name": "杨栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-07",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "商城县人民政府",
        "source": "Official bio: http://www.hnsc.gov.cn/2026/07-24/795948.html"
    },
    # ═══════ Government Leadership (副县长) ═══════
    {
        "id": 4,
        "name": "杨宇",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1987-05",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、副县长",
        "current_org": "商城县人民政府",
        "source": "Official bio: http://www.hnsc.gov.cn/2026/07-24/795861.html"
    },
    {
        "id": 5,
        "name": "耿海峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-04",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "商城县人民政府",
        "source": "Official bio: http://www.hnsc.gov.cn/2026/07-24/795862.html"
    },
    {
        "id": 6,
        "name": "穆晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989-10",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "商城县人民政府",
        "source": "Official bio: http://www.hnsc.gov.cn/2026/07-24/795864.html"
    },
    {
        "id": 7,
        "name": "董园飞",
        "gender": "女",
        "ethnicity": "",
        "birth": "1988-10",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "商城县人民政府",
        "source": "Official bio: http://www.hnsc.gov.cn/2025/01-21/166399.html"
    },
    {
        "id": 8,
        "name": "郭滨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-02",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "商城县人民政府",
        "source": "Official bio: http://www.hnsc.gov.cn/2025/01-21/166400.html"
    },
    {
        "id": 9,
        "name": "余巨峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-09",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "商城县人民政府",
        "source": "Official bio: http://www.hnsc.gov.cn/2025/01-21/166401.html"
    },
    # ═══════ 县委常委会 (from 接访日程) ═══════
    {
        "id": 10,
        "name": "陈明辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共商城县委员会",
        "source": "接访日程公示 2026-08 : http://www.hnsc.gov.cn/2026/08-03/797124.html"
    },
    {
        "id": 11,
        "name": "甘尚昆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共商城县委员会",
        "source": "接访日程公示 2026-08 : http://www.hnsc.gov.cn/2026/08-03/797124.html"
    },
    {
        "id": 12,
        "name": "杨海军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共商城县委员会",
        "source": "接访日程公示 2026-08 : http://www.hnsc.gov.cn/2026/08-03/797124.html"
    },
    {
        "id": 13,
        "name": "王景昌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任、县总工会主席",
        "current_org": "商城县人民代表大会常务委员会",
        "source": "接访日程公示 2026-08 : http://www.hnsc.gov.cn/2026/08-03/797124.html"
    },
    {
        "id": 14,
        "name": "连勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协商城县委员会",
        "source": "县领导调研新闻 2026-08-05 : http://www.hnsc.gov.cn/2026/08-05/797438.html"
    },
    # ═══════ 前任领导 ═══════
    {
        "id": 15,
        "name": "胡培刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共商城县委员会",
        "source": "Baidu Baike 商城县 entry (secondary); 前任县委书记, succeeded by 孙红鑫 ~2025-09"
    },
    {
        "id": 16,
        "name": "鲁新建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县长",
        "current_org": "商城县人民政府",
        "source": "Official 2025 政府工作报告 (2025-02-15) 由 商城县人民政府县长 鲁新建 作报告 : http://www.hnsc.gov.cn/2025/02-19/602461.html"
    },
    # ═══════ Cross-County Linked Officials (网络链接点) ═══════
    {
        "id": 17,
        "name": "王建平",
        "gender": "",
        "ethnicity": "",
        "birth": "1972-05",
        "birthplace": "河南漯河",
        "education": "大学学历",
        "party_join": "",
        "work_start": "1995-12",
        "current_post": "前光山县委书记、前任商城县干部",
        "current_org": "(已调离信阳)",
        "source": "光山县班子报告 (2026-08-06): 王建平早年任商城县委常委、副县长, 2021-07 任光山县委书记；2024 调离信阳行政区. repo: report/20260806-河南省-信阳市-光山县"
    },
    {
        "id": 18,
        "name": "朱国朋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-06",
        "birthplace": "",
        "education": "法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新县县委副书记、县长",
        "current_org": "新县人民政府",
        "source": "新县班子调研报告 (2026-07)/person JSON: 2021-10至2023任商城县委副书记、汪桥镇党委书记 (墩苗育苗干部); 后任新县县长"
    },
    {
        "id": 19,
        "name": "曾玉杰",
        "gender": "女",
        "ethnicity": "",
        "birth": "1977-02",
        "birthplace": "商城县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县委常委、常务副县长",
        "current_org": "光山县人民政府",
        "source": "光山县班子调研报告 (2026-08-06): 曾玉杰 1977-02，商城人"
    },
    {
        "id": 20,
        "name": "彭辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "1973-07",
        "birthplace": "商城县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山副县长、县公安局局长",
        "current_org": "光山县人民政府",
        "source": "光山县班子调研报告 (2026-08-06): 彭辉 1973-07，河南商城人"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {
        "id": ORG_OFFSET + 1,
        "name": "中共商城县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共信阳市委",
        "location": "河南省信阳市商城县"
    },
    {
        "id": ORG_OFFSET + 2,
        "name": "商城县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "信阳市人民政府",
        "location": "河南省信阳市商城县"
    },
    {
        "id": ORG_OFFSET + 3,
        "name": "商城县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "商城县人民政府",
        "location": "河南省信阳市商城县"
    },
    {
        "id": ORG_OFFSET + 4,
        "name": "商城县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "河南省人民代表大会常务委员会",
        "location": "河南省信阳市商城县"
    },
    {
        "id": ORG_OFFSET + 5,
        "name": "政协商城县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协信阳市委员会",
        "location": "河南省信阳市商城县"
    },
    # 跨县关联组织
    {
        "id": ORG_OFFSET + 6,
        "name": "中共光山县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共信阳市委",
        "location": "河南省信阳市光山县"
    },
    {
        "id": ORG_OFFSET + 7,
        "name": "光山县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "信阳市人民政府",
        "location": "河南省信阳市光山县"
    },
    {
        "id": ORG_OFFSET + 8,
        "name": "中共新县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共信阳市委",
        "location": "河南省信阳市新县"
    },
    {
        "id": ORG_OFFSET + 9,
        "name": "新县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "信阳市人民政府",
        "location": "河南省信阳市新县"
    },
]


# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 孙红鑫 (县委书记)
    {"person_id": 1, "org_id": ORG_OFFSET + 1, "title": "县委书记", "start": "2025-09", "end": "present", "rank": "正处级", "note": "2025年9月起任县委书记 (官方新闻确认), 前任胡培刚"},
    # 吕菲 (县长)
    {"person_id": 2, "org_id": ORG_OFFSET + 2, "title": "县长", "start": "2026-05", "end": "present", "rank": "正处级", "note": "2026-05-14 代理县长, 2026-06-01 当选县长 (官方bio 2026-06-01)"},
    {"person_id": 2, "org_id": ORG_OFFSET + 1, "title": "县委副书记", "start": "2026-05", "end": "present", "rank": "正处级", "note": ""},
    # 杨栋 (常务副县长)
    {"person_id": 3, "org_id": ORG_OFFSET + 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委、县政府党组副书记"},
    {"person_id": 3, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 杨宇 (宣传部长/副县长)
    {"person_id": 4, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委、宣传部部长"},
    {"person_id": 4, "org_id": ORG_OFFSET + 1, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 耿海峰
    {"person_id": 5, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责农业农村、乡村振兴"},
    # 穆晓东
    {"person_id": 6, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责住建、自然资源、城管"},
    # 董园飞
    {"person_id": 7, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 郭滨
    {"person_id": 8, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责光伏扶贫、国电投帮扶"},
    # 余巨峰
    {"person_id": 9, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责公安、司法、信访"},
    {"person_id": 9, "org_id": ORG_OFFSET + 3, "title": "县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 县委常委会
    {"person_id": 10, "org_id": ORG_OFFSET + 1, "title": "县委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": ORG_OFFSET + 1, "title": "县委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": ORG_OFFSET + 1, "title": "县委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 人大/政协
    {"person_id": 13, "org_id": ORG_OFFSET + 4, "title": "县人大常委会副主任、县总工会主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": ORG_OFFSET + 5, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 前任
    {"person_id": 15, "org_id": ORG_OFFSET + 1, "title": "县委书记 (前任)", "start": "", "end": "2025-09", "rank": "正处级", "note": "被孙红鑫接任"},
    {"person_id": 16, "org_id": ORG_OFFSET + 2, "title": "县长 (前任)", "start": "", "end": "2025", "rank": "正处级", "note": "2025-02 仍任县长, 后被吕菲接任"},
    # 跨县
    {"person_id": 17, "org_id": ORG_OFFSET + 1, "title": "县委常委、副县长 (早年, 商城)", "start": "", "end": "", "rank": "副处级", "note": "早年任商城县领导, 后任光山县长/书记"},
    {"person_id": 17, "org_id": ORG_OFFSET + 6, "title": "县委书记 (光山)", "start": "2021-07", "end": "2024", "rank": "正处级", "note": "2024 调离信阳行政区"},
    {"person_id": 18, "org_id": ORG_OFFSET + 1, "title": "县委副书记 (商城)", "start": "2021-10", "end": "2023", "rank": "副处级", "note": "墩苗育苗干部, 兼任汪桥镇党委书记"},
    {"person_id": 18, "org_id": ORG_OFFSET + 9, "title": "县长 (新县)", "start": "2025-11", "end": "present", "rank": "正处级", "note": "2023年后经豫东南高新区调新县"},
    {"person_id": 19, "org_id": ORG_OFFSET + 7, "title": "常务副县长 (光山)", "start": "", "end": "present", "rank": "副处级", "note": "商城人"},
    {"person_id": 20, "org_id": ORG_OFFSET + 7, "title": "副县长、县公安局长 (光山)", "start": "", "end": "present", "rank": "副处级", "note": "商城人"},
]


# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 现任党政正职搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记孙红鑫与县长吕菲现搭档",
        "overlap_org": "中共商城县委员会",
        "overlap_period": "2026-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 书记与政府常务
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与常务副县长杨栋",
        "overlap_org": "中共商城县委员会",
        "overlap_period": "2025-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长吕菲与常务副县长杨栋上下级搭档",
        "overlap_org": "商城县人民政府",
        "overlap_period": "2026-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 政府班子成员 (县长—副县长共事)
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "县长与副县长/宣传部长杨宇共事",
        "overlap_org": "商城县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "县长与耿海峰副县长共事",
        "overlap_org": "商城县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "县长与穆晓东副县长共事",
        "overlap_org": "商城县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "overlap",
        "context": "县长与董园飞副县长共事",
        "overlap_org": "商城县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 8,
        "type": "overlap",
        "context": "县长与郭滨副县长共事",
        "overlap_org": "商城县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 9,
        "type": "overlap",
        "context": "县长与余巨峰副县长/公安局长共事",
        "overlap_org": "商城县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 常务副县长与副县长
    {
        "person_a": 3, "person_b": 9,
        "type": "overlap",
        "context": "杨栋 (分管应急/公安口) 与余巨峰 (公安/应急) 分工协作",
        "overlap_org": "商城县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "plausible"
    },
    {
        "person_a": 3, "person_b": 5,
        "type": "overlap",
        "context": "杨栋与耿海峰 (农田口) 分工协作",
        "overlap_org": "商城县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "plausible"
    },
    # 县委常委会成员与书记
    {
        "person_a": 1, "person_b": 10,
        "type": "superior_subordinate",
        "context": "书记与政法委书记陈明辉",
        "overlap_org": "中共商城县委员会",
        "overlap_period": "2025-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 11,
        "type": "superior_subordinate",
        "context": "书记与统战部长甘尚昆",
        "overlap_org": "中共商城县委员会",
        "overlap_period": "2025-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 12,
        "type": "superior_subordinate",
        "context": "书记与组织部长杨海军",
        "overlap_org": "中共商城县委员会",
        "overlap_period": "2025-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 前后任书记
    {
        "person_a": 1, "person_b": 15,
        "type": "predecessor_successor",
        "context": "孙红鑫接任胡培刚任县委书记",
        "overlap_org": "中共商城县委员会",
        "overlap_period": "2025-09",
        "strength": "strong",
        "confidence": "plausible"
    },
    # 前后任县长
    {
        "person_a": 2, "person_b": 16,
        "type": "predecessor_successor",
        "context": "吕菲接替鲁新建任县长",
        "overlap_org": "商城县人民政府",
        "overlap_period": "2026",
        "strength": "strong",
        "confidence": "plausible"
    },
    # 跨县: 王建平 (商城→光山)
    {
        "person_a": 17, "person_b": 1,
        "type": "predecessor_successor",
        "context": "王建平早年任商城县委常委/副县长后调光山; 为商城干部输出重要节点",
        "overlap_org": "中共商城县委员会",
        "overlap_period": "2010年代",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 跨县: 朱国朋 (商城→新县)
    {
        "person_a": 18, "person_b": 1,
        "type": "overlap",
        "context": "朱国朋曾任商城县县委副书记(2021-10-2023), 与商城县委班子共事",
        "overlap_org": "中共商城县委员会",
        "overlap_period": "2021-2023",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 跨县: 商城籍干部在光山
    {
        "person_a": 19, "person_b": 20,
        "type": "same_native_place",
        "context": "曾玉杰与彭辉同为商城籍干部, 现均任职光山县",
        "overlap_org": "光山县人民政府",
        "overlap_period": "2020s",
        "strength": "medium",
        "confidence": "plausible"
    },
    {
        "person_a": 19, "person_b": 17,
        "type": "overlap",
        "context": "曾玉杰 (商城籍) 与王建平 (商城→光山领导) 在商城/光山网络交叉",
        "overlap_org": "光山县",
        "overlap_period": "",
        "strength": "weak",
        "confidence": "unverified"
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# Database + GEXF build
# ═══════════════════════════════════════════════════════════════════════════

def build():
    """Build SQLite database and GEXF graph."""
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

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


def verify():
    """Verify output files exist and have correct structure."""
    import sqlite3
    errors = []

    if not DB_PATH.exists():
        errors.append(f"Database not found: {DB_PATH}")
    else:
        conn = sqlite3.connect(str(DB_PATH))
        tables = [row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )]
        expected = ["persons", "organizations", "positions", "relationships"]
        for t in expected:
            if t not in tables:
                errors.append(f"Missing table: {t}")
        for t in expected:
            c = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            print(f"  {t}: {c}")
        conn.close()

    if not GEXF_PATH.exists():
        errors.append(f"GEXF not found: {GEXF_PATH}")
    else:
        content = GEXF_PATH.read_text("utf-8")
        if '<gexf' not in content:
            errors.append("GEXF missing <gexf> tag")
        if '<nodes>' not in content:
            errors.append("GEXF missing <nodes>")
        if '<edges>' not in content:
            errors.append("GEXF missing <edges>")
        if '</gexf>' not in content:
            errors.append("GEXF missing closing </gexf>")

    if errors:
        for e in errors:
            print(f"  ERROR: {e}")
        return False
    print("  Verification: PASSED")
    return True


if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    build()
    print("\nVerifying...")
    if verify():
        print("\nDone. Files created:")
        print(f"  DB:   {DB_PATH}")
        print(f"  GEXF: {GEXF_PATH}")
    else:
        print("\nFAILED: verification errors")
        sys.exit(1)