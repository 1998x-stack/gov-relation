#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 资源县 leadership network.

Task: guangxi_资源县
Province: 广西壮族自治区
Parent City: 桂林市
Region: 资源县
Level: 县级
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)

Investigation Date: 2026-07-22

Confirmed Findings (Phase 1 & 2 Research):
1. 关小菊 (female, Zhuang, b.1978-08) - 资源县委书记, 县人武部党委第一书记 (confirmed).
   Former 桂林市体育局局长 (2020.12-2026.02). Appointed 人武部党委第一书记 on 2026-02-13.
2. 陈建华 (male, Han, b.1976-06) - 资源县委副书记、县长 (confirmed).
   Native of 阳朔, Guilin. Elected county mayor on 2025-04-30 at the 17th People's Congress 6th Session.
3. 田勤 (female, Yao, b.1979-01) - 资源县委副书记, 二级调研员, 县委党校校长.
   Proposed as county mayor candidate per public notice (2026-06-17).
4. 陶日桂 (male, Han, b.1979-10) - 县委常委、常务副县长. From 平乐, Guangxi.
5. 石克生 (male, Han) - 资源县委常委、县委办主任. Local of 资源县.
"""

import json
import os
import sys
from datetime import datetime

# Ensure gov_relation module is importable
_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.normpath(os.path.join(_HERE, "..", "..", ".."))
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)

from gov_relation.runner import run_build
from gov_relation.paths import REPO_ROOT

# These are needed by process_tmp.py validation
import sqlite3  # noqa: F401

AS_OF = "2026-07-22"
STAGING_DIR = _HERE
DB_PATH = os.path.join(STAGING_DIR, "资源县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "资源县_network.gexf")
PERSONS_DIR = STAGING_DIR

# =========================================================================
# DATA
# =========================================================================

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    # Current top leaders
    {
        "id": 1,
        "name": "关小菊",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "1978-08",
        "birthplace": "广西蒙山",
        "education": "广西区委党校在职研究生",
        "party_join": "1998-06",
        "work_start": "",
        "current_post": "资源县委书记、县人武部党委第一书记",
        "current_org": "中共资源县委员会",
        "source": "https://baike.baidu.com/item/%E5%85%B3%E5%B0%8F%E8%8F%8A"
    },
    {
        "id": 2,
        "name": "陈建华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-06",
        "birthplace": "广西阳朔",
        "education": "大学学历, 工学学士, 广西区委党校研究生",
        "party_join": "1999-05",
        "work_start": "",
        "current_post": "资源县委副书记、县长",
        "current_org": "资源县人民政府",
        "source": "http://www.ziyuan.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/xz/"
    },
    {
        "id": 3,
        "name": "田勤",
        "gender": "女",
        "ethnicity": "瑶族",
        "birth": "1979-01",
        "birthplace": "广西恭城",
        "education": "广西大学本科学历",
        "party_join": "2000-12",
        "work_start": "2001-09",
        "current_post": "资源县委副书记、二级调研员、县委党校校长",
        "current_org": "中共资源县委员会",
        "source": "https://baike.baidu.com/item/%E7%94%B0%E5%8B%A4/15873025"
    },
    {
        "id": 4,
        "name": "陶日桂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-10",
        "birthplace": "广西平乐",
        "education": "大学本科学历, 法学学士学位",
        "party_join": "1999-06",
        "work_start": "1999-10",
        "current_post": "资源县委常委、常务副县长",
        "current_org": "资源县人民政府",
        "source": "https://baike.baidu.com/item/%E9%99%B6%E6%97%A5%E6%A1%82"
    },
    {
        "id": 5,
        "name": "石克生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "广西资源",
        "education": "在职大学学历",
        "party_join": "1997-10",
        "work_start": "1995-07",
        "current_post": "资源县委常委、县委办主任",
        "current_org": "中共资源县委员会",
        "source": "https://baike.baidu.com/item/%E7%9F%B3%E5%85%8B%E7%94%9F"
    },
    # Predecessors
    {
        "id": 6,
        "name": "黄钦",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂林市领导（前任资源县委书记）",
        "current_org": "",
        "source": "Baidu search results — 黄钦于2025年10月任桂林市"
    },
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共资源县委员会", "type": "党委", "level": "县级",
     "parent": "中共桂林市委员会", "location": "桂林市资源县"},
    {"id": 2, "name": "资源县人民政府", "type": "政府", "level": "县级",
     "parent": "桂林市人民政府", "location": "桂林市资源县"},
    {"id": 3, "name": "资源县人大常委会", "type": "人大", "level": "县级",
     "parent": "", "location": "桂林市资源县"},
    {"id": 4, "name": "资源县人民武装部", "type": "事业单位", "level": "县级",
     "parent": "桂林警备区", "location": "桂林市资源县"},
    {"id": 5, "name": "桂林市体育局", "type": "政府", "level": "地级市",
     "parent": "桂林市人民政府", "location": "桂林市"},
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "资源县委书记、县人武部党委第一书记",
     "start_date": "2026-02", "end_date": "present",
     "rank": "正处级", "note": "2026年2月13日任人武部党委第一书记"},
    {"person_id": 1, "org_id": 5, "title": "桂林市体育局局长",
     "start_date": "2020-12", "end_date": "2026-02",
     "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "资源县县长",
     "start_date": "2025-04", "end_date": "present",
     "rank": "正处级", "note": "2025年4月30日补选为县长"},
    {"person_id": 2, "org_id": 1, "title": "资源县委副书记、县政府党组书记",
     "start_date": "", "end_date": "present",
     "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "资源县委副书记、二级调研员、县委党校校长",
     "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "2026年6月公示拟提名为县(市、区)长候选人"},
    {"person_id": 4, "org_id": 2, "title": "资源县委常委、常务副县长",
     "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "资源县委常委、县委办主任",
     "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "前任资源县委书记",
     "start_date": "", "end_date": "约2025",
     "rank": "正处级", "note": "黄钦于2025年10月任桂林市"},
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长搭档", "overlap_org": "资源县",
     "overlap_period": "2026-02至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委副书记", "overlap_org": "中共资源县委员会",
     "overlap_period": "2026-02至今"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与常务副县长", "overlap_org": "资源县人民政府",
     "overlap_period": ""},
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor",
     "context": "田勤拟提名为县长候选人，可能接替陈建华", "overlap_org": "资源县",
     "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "predecessor_successor",
     "context": "关小菊接替黄钦任资源县委书记", "overlap_org": "中共资源县委员会",
     "overlap_period": "2025/2026"},
]

# =========================================================================
# BUILD
# =========================================================================

if __name__ == "__main__":
    print(f"[{datetime.now().isoformat()}] Building 资源县 network...")
    run_build(
        slug="资源县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"[{datetime.now().isoformat()}] Done. DB={DB_PATH} GEXF={GEXF_PATH}")

    # Helper: write a report snippet
    report_path = os.path.join(STAGING_DIR, "20260722-广西壮族自治区-桂林市-资源县-调查报告.md")
    lines = [
        f"# 资源县领导班子调查简报",
        f"",
        f"调查日期：2026-07-22",
        f"任务ID：guangxi_资源县",
        f"",
        f"## 当前领导班子",
        f"",
        f"| 职务 | 姓名 | 性别 | 民族 | 出生 | 籍贯 | 学历 | 任职起始 | 来源 |",
        f"|------|------|------|------|------|------|------|----------|------|",
        f"| 县委书记 | 关小菊 | 女 | 壮族 | 1978-08 | 广西蒙山 | 广西区委党校在职研究生 | 2026-02 | 百度百科 |",
        f"| 县长 | 陈建华 | 男 | 汉族 | 1976-06 | 广西阳朔 | 大学/工学学士/党校研究生 | 2025-04 | 资源县政府网 |",
        f"| 县委副书记 | 田勤 | 女 | 瑶族 | 1979-01 | 广西恭城 | 广西大学本科 | - | 百度百科 |",
        f"| 常务副县长 | 陶日桂 | 男 | 汉族 | 1979-10 | 广西平乐 | 大学本科/法学学士 | - | 百度百科 |",
        f"| 县委常委/县委办主任 | 石克生 | 男 | 汉族 | - | 广西资源 | 在职大学 | - | 百度百科 |",
        f"",
        f"## 人员变动",
        f"",
        f"- 关小菊：原桂林市体育局局长（2020.12-2026.02），2026年2月任资源县委书记、县人武部党委第一书记。",
        f"- 陈建华：2025年4月30日资源县第十七届人民代表大会第六次会议补选为资源县人民政府县长。",
        f"- 黄钦：前任资源县委书记，约2025年10月调任桂林市。",
        f"- 田勤：2026年6月17日广西公示拟提名为县（市、区）长候选人。",
        f"",
        f"## 关键网络关系",
        f"",
        f"- 关小菊（县委）- 陈建华（政府）：党政一把手搭档（2026-02至今）。",
        f"- 关小菊 - 田勤：书记与副书记关系。",
        f"- 陈建华 - 陶日桂：县长与常务副县长工作关系。",
        f"- 田勤/陈建华：田勤拟提名为县长候选人（可能接替）。",
        f"",
        f"## 开放问题",
        f"",
        f"- 田勤的县长候选人提名具体去向（是接替陈建华还是调任其他县）尚未明确确认。",
        f"- 黄钦调任桂林市的具体职务未确认。",
        f"- 关小菊在担任桂林市体育局局长前的完整履历需要进一步补充。",
        f"- 陈建华在担任县长前的完整履历（曾任职务）需要进一步补充。",
        f"- 资源县其他县委常委（如纪委书记、组织部长、宣传部长、政法委书记等）名单待补充。",
        f"",
        f"## 来源",
        f"",
        f"- 关小菊百度百科: https://baike.baidu.com/item/%E5%85%B3%E5%B0%8F%E8%8F%8A",
        f"- 陈建华资料: http://www.ziyuan.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/xz/",
        f"- 田勤百度百科: https://baike.baidu.com/item/%E7%94%B0%E5%8B%A4/15873025",
        f"- 陶日桂百度百科: https://baike.baidu.com/item/%E9%99%B6%E6%97%A5%E6%A1%82",
        f"- 石克生百度百科: https://baike.baidu.com/item/%E7%9F%B3%E5%85%8B%E7%94%9F",
        f"- 广西政府网: http://www.gxzf.gov.cn/zwgk/zfxxgkzl_84988/fdzdgknr/rsxx/t27804934.shtml",
    ]
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[{datetime.now().isoformat()}] Report written: {report_path}")
