#!/usr/bin/env python3
"""Build script for 友好区 (Youhao District, Yichun, Heilongjiang) leadership network.

Generated: 2026-07-24
Level: 市辖区
Province: 黑龙江省
Parent City: 伊春市
Targets: 区委书记 & 区长

Research Note:
  All web search tools were degraded during this investigation:
  - Exa: rate-limited (free tier quota exhausted)
  - Baidu Baike/search: returning 403/blocked
  - Google via Jina Reader: timeouts
  - District government site (yhq.yc.gov.cn): DNS/timeout
  - City government site (www.yc.gov.cn): accessible but no leadership page found
  - Wikipedia (zh.wikipedia.org): accessible — confirmed 友好区 administrative info
  
  The city site confirmed 友好区 as a sub-site under yc.gov.cn but the actual
  subdomain (yhq.yc.gov.cn) was unreachable. City-level leadership confirmed:
  董文琴 (Party Secretary) and 苑芳江 (Mayor). District-level leadership names
  could not be confirmed from any accessible source.

  Under the source_fallbacks.md guidelines, this run produces structurally valid
  artifacts with explicit uncertainty markers.

Sources:
  - https://zh.wikipedia.org/wiki/友好区 (区划信息确认)
  - https://zh.wikipedia.org/wiki/伊春市 (市级领导确认)
  - https://www.yc.gov.cn/ (伊春市人民政府 — 市级领导确认)
"""

import sqlite3  # noqa: used by gov_relation.runner
from pathlib import Path

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    # 区委书记 (PARTY SECRETARY OF YOUHAO DISTRICT) — NOT FOUND via any accessible source
    {
        "id": 1,
        "name": "【待查】友好区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "友好区委书记（待查）",
        "current_org": "中共伊春市友好区委员会",
        "source": "GAP — 友好区委书记姓名未在任何可访问来源上找到；需通过伊春市委组织部任前公示、友好区政府官网(yhq.yc.gov.cn)或区党委网站补充",
    },
    # 区长 (DISTRICT MAYOR) — NOT FOUND via any accessible source
    {
        "id": 2,
        "name": "【待查】友好区区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "友好区区长（待查）",
        "current_org": "伊春市友好区人民政府",
        "source": "GAP — 友好区区长姓名未在任何可访问来源上找到；需通过伊春市政府官网或区委网站补充",
    },
    # ── City-level Leadership (from Wikipedia/Yichun city gov site) ──
    # 市委书记
    {
        "id": 3,
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
        "source": "https://zh.wikipedia.org/wiki/伊春市; https://www.yc.gov.cn/",
    },
    # 市长
    {
        "id": 4,
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
        "source": "https://zh.wikipedia.org/wiki/伊春市; https://www.yc.gov.cn/",
    },
    # 市政协主席
    {
        "id": 5,
        "name": "刘福军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年1月",
        "birthplace": "山东省梁山县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "伊春市政协主席",
        "current_org": "政协伊春市委员会",
        "source": "https://zh.wikipedia.org/wiki/伊春市",
    },
    # ── Deputy City Leaders (from city gov site: 陈岩, 田宁, 高见, 刘暾, 李东辉, 姜治富, 孟庆彤, 李长江) ──
    {
        "id": 6,
        "name": "陈岩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "伊春市领导（副市长等）",
        "current_org": "伊春市人民政府",
        "source": "https://www.yc.gov.cn/ （市政府官网领导名单）",
    },
    {
        "id": 7,
        "name": "田宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "伊春市领导（副市长等）",
        "current_org": "伊春市人民政府",
        "source": "https://www.yc.gov.cn/ （市政府官网领导名单）",
    },
    {
        "id": 8,
        "name": "高见",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "伊春市领导（副市长等）",
        "current_org": "伊春市人民政府",
        "source": "https://www.yc.gov.cn/ （市政府官网领导名单）",
    },
    {
        "id": 9,
        "name": "刘暾",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "伊春市领导（副市长等）",
        "current_org": "伊春市人民政府",
        "source": "https://www.yc.gov.cn/ （市政府官网领导名单）",
    },
    {
        "id": 10,
        "name": "李东辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "伊春市领导（副市长等）",
        "current_org": "伊春市人民政府",
        "source": "https://www.yc.gov.cn/ （市政府官网领导名单）",
    },
    {
        "id": 11,
        "name": "姜治富",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "伊春市领导（副市长等）",
        "current_org": "伊春市人民政府",
        "source": "https://www.yc.gov.cn/ （市政府官网领导名单）",
    },
    {
        "id": 12,
        "name": "孟庆彤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "伊春市领导（副市长等）",
        "current_org": "伊春市人民政府",
        "source": "https://www.yc.gov.cn/ （市政府官网领导名单）",
    },
    {
        "id": 13,
        "name": "李长江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "伊春市领导（副市长等）",
        "current_org": "伊春市人民政府",
        "source": "https://www.yc.gov.cn/ （市政府官网领导名单）",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共伊春市友好区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共伊春市委员会",
        "location": "黑龙江省伊春市友好区",
    },
    {
        "id": 2,
        "name": "伊春市友好区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "伊春市人民政府",
        "location": "黑龙江省伊春市友好区",
    },
    {
        "id": 3,
        "name": "伊春市友好区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "伊春市人大常委会",
        "location": "黑龙江省伊春市友好区",
    },
    {
        "id": 4,
        "name": "政协伊春市友好区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协伊春市委员会",
        "location": "黑龙江省伊春市友好区",
    },
    {
        "id": 5,
        "name": "伊春市友好区纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共伊春市纪律检查委员会",
        "location": "黑龙江省伊春市友好区",
    },
    # City-level organizations
    {
        "id": 6,
        "name": "中共伊春市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共黑龙江省委员会",
        "location": "黑龙江省伊春市伊美区",
    },
    {
        "id": 7,
        "name": "伊春市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "黑龙江省人民政府",
        "location": "黑龙江省伊春市伊美区",
    },
]

POSITIONS = [
    # GAP: 区委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "友好区委书记",
        "start_date": "未知",
        "end_date": "现任",
        "rank": "县处级正职",
        "note": "GAP — 姓名和履历均待查",
    },
    # GAP: 区长
    {
        "person_id": 2,
        "org_id": 1,
        "title": "友好区委副书记",
        "start_date": "未知",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "区政府党组书记（待查）",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "友好区区长",
        "start_date": "未知",
        "end_date": "现任",
        "rank": "县处级正职",
        "note": "GAP — 姓名和履历均待查",
    },
    # City-level confirmed positions
    {
        "person_id": 3,
        "org_id": 6,
        "title": "伊春市委书记",
        "start_date": "2024年9月",
        "end_date": "现任",
        "rank": "地厅级正职",
        "note": "",
    },
    {
        "person_id": 3,
        "org_id": 3,
        "title": "伊春市人大常委会主任",
        "start_date": "2025年1月",
        "end_date": "现任",
        "rank": "地厅级正职",
        "note": "",
    },
    {
        "person_id": 4,
        "org_id": 6,
        "title": "伊春市委副书记",
        "start_date": "2024年9月",
        "end_date": "现任",
        "rank": "地厅级副职",
        "note": "",
    },
    {
        "person_id": 4,
        "org_id": 7,
        "title": "伊春市市长",
        "start_date": "2024年9月",
        "end_date": "现任",
        "rank": "地厅级正职",
        "note": "代市长转正，具体日期待查",
    },
    {
        "person_id": 5,
        "org_id": 4,
        "title": "伊春市政协主席",
        "start_date": "2025年1月",
        "end_date": "现任",
        "rank": "地厅级正职",
        "note": "",
    },
    # Deputy city leaders — exact titles unknown but listed on city gov website
    {"person_id": 6, "org_id": 7, "title": "伊春市领导（副市长等）", "start_date": "未知", "end_date": "现任", "rank": "地厅级副职", "note": "具体职务待查"},
    {"person_id": 7, "org_id": 7, "title": "伊春市领导（副市长等）", "start_date": "未知", "end_date": "现任", "rank": "地厅级副职", "note": "具体职务待查"},
    {"person_id": 8, "org_id": 7, "title": "伊春市领导（副市长等）", "start_date": "未知", "end_date": "现任", "rank": "地厅级副职", "note": "具体职务待查"},
    {"person_id": 9, "org_id": 7, "title": "伊春市领导（副市长等）", "start_date": "未知", "end_date": "现任", "rank": "地厅级副职", "note": "具体职务待查"},
    {"person_id": 10, "org_id": 7, "title": "伊春市领导（副市长等）", "start_date": "未知", "end_date": "现任", "rank": "地厅级副职", "note": "具体职务待查"},
    {"person_id": 11, "org_id": 7, "title": "伊春市领导（副市长等）", "start_date": "未知", "end_date": "现任", "rank": "地厅级副职", "note": "具体职务待查"},
    {"person_id": 12, "org_id": 7, "title": "伊春市领导（副市长等）", "start_date": "未知", "end_date": "现任", "rank": "地厅级副职", "note": "具体职务待查"},
    {"person_id": 13, "org_id": 7, "title": "伊春市领导（副市长等）", "start_date": "未知", "end_date": "现任", "rank": "地厅级副职", "note": "具体职务待查"},
]

RELATIONSHIPS = [
    # 区委书记 <-> 区长 (both GAP)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长搭档关系（均待查）",
        "overlap_org": "中共伊春市友好区委员会",
        "overlap_period": "现任",
    },
    # City-level: 市委书记 <-> 市长
    {
        "person_a": 3,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "市委书记与市长搭档关系",
        "overlap_org": "中共伊春市委员会",
        "overlap_period": "2024年9月起至今",
    },
]

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "友好区_network.db"
GEXF_PATH = STAGING_DIR / "友好区_network.gexf"


def main():
    run_build(
        slug="友好区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Done.")


if __name__ == "__main__":
    main()
