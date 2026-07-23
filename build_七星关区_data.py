#!/usr/bin/env python3
"""Build script for 七星关区 (Qixingguan District, Bijie, Guizhou) leadership network.

Generated: 2026-07-23
Level: 市辖区
Province: 贵州省
Parent City: 毕节市
Targets: 区委书记 & 区长

Research Note:
  The district government website (www.bjqixingguan.gov.cn) was partially accessible.
  The 政务公开 page confirmed 黄海刚 as District Mayor (区长), and listed 11 other
  district leaders by name. However, the 区委书记 (Party Secretary) name was not
  found on any accessible page. The party committee site may be behind a separate
  domain or firewall.

  Web search was severely degraded: Exa rate-limited, Baidu 403, Jina Reader timed out,
  Wikipedia blocked. All research was done via direct HTTP access to the district
  government website.

Sources:
  - http://www.bjqixingguan.gov.cn/zwgk_500441/ (confirmed 黄海刚 as 区长, leader roster)
  - http://www.bjqixingguan.gov.cn/home/index.html (news articles confirming 黄海刚 activities)
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
    # 区委书记 (PARTY SECRETARY) — NOT FOUND
    {
        "id": 1,
        "name": "【待查】七星关区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星关区委书记（待查）",
        "current_org": "中共毕节市七星关区委员会",
        "source": "GAP — 区委书记姓名未在区政府网站上公开；需通过毕节市委组织部任前公示或区党委网站补充",
    },
    # 区长 (DISTRICT MAYOR) — CONFIRMED
    {
        "id": 2,
        "name": "黄海刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "七星关区委副书记、区人民政府党组书记、区长",
        "current_org": "毕节市七星关区人民政府",
        "source": "http://www.bjqixingguan.gov.cn/zwgk_500441/ （区政府官网领导之窗确认简历）",
    },
    # ── Deputy Leaders (names found but roles unknown) ──
    {
        "id": 3,
        "name": "彭令",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星关区领导（具体职务待查）",
        "current_org": "毕节市七星关区",
        "source": "http://www.bjqixingguan.gov.cn/zwgk_500441/ （区政府官网领导之窗名单）",
    },
    {
        "id": 4,
        "name": "袁远兴",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星关区领导（具体职务待查）",
        "current_org": "毕节市七星关区",
        "source": "http://www.bjqixingguan.gov.cn/zwgk_500441/ （区政府官网领导之窗名单）",
    },
    {
        "id": 5,
        "name": "唐国华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星关区领导（具体职务待查）",
        "current_org": "毕节市七星关区",
        "source": "http://www.bjqixingguan.gov.cn/zwgk_500441/ （区政府官网领导之窗名单）",
    },
    {
        "id": 6,
        "name": "王春永",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星关区领导（具体职务待查）",
        "current_org": "毕节市七星关区",
        "source": "http://www.bjqixingguan.gov.cn/zwgk_500441/ （区政府官网领导之窗名单）",
    },
    {
        "id": 7,
        "name": "杨华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星关区领导（具体职务待查）",
        "current_org": "毕节市七星关区",
        "source": "http://www.bjqixingguan.gov.cn/zwgk_500441/ （区政府官网领导之窗名单）",
    },
    {
        "id": 8,
        "name": "陈果",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星关区领导（具体职务待查）",
        "current_org": "毕节市七星关区",
        "source": "http://www.bjqixingguan.gov.cn/zwgk_500441/ （区政府官网领导之窗名单）",
    },
    {
        "id": 9,
        "name": "宋尚万",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星关区领导（具体职务待查）",
        "current_org": "毕节市七星关区",
        "source": "http://www.bjqixingguan.gov.cn/zwgk_500441/ （区政府官网领导之窗名单）",
    },
    {
        "id": 10,
        "name": "刘歆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星关区领导（具体职务待查）",
        "current_org": "毕节市七星关区",
        "source": "http://www.bjqixingguan.gov.cn/zwgk_500441/ （区政府官网领导之窗名单）",
    },
    {
        "id": 11,
        "name": "胡从洋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星关区领导（具体职务待查）",
        "current_org": "毕节市七星关区",
        "source": "http://www.bjqixingguan.gov.cn/zwgk_500441/ （区政府官网领导之窗名单）",
    },
    {
        "id": 12,
        "name": "邓涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星关区领导（具体职务待查）",
        "current_org": "毕节市七星关区",
        "source": "http://www.bjqixingguan.gov.cn/zwgk_500441/ （区政府官网领导之窗名单）",
    },
    {
        "id": 13,
        "name": "吴锦煜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七星关区领导（具体职务待查）",
        "current_org": "毕节市七星关区",
        "source": "http://www.bjqixingguan.gov.cn/zwgk_500441/ （区政府官网领导之窗名单）",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共毕节市七星关区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共毕节市委员会",
        "location": "贵州省毕节市七星关区",
    },
    {
        "id": 2,
        "name": "毕节市七星关区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "毕节市人民政府",
        "location": "贵州省毕节市七星关区",
    },
    {
        "id": 3,
        "name": "毕节市七星关区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "毕节市人大常委会",
        "location": "贵州省毕节市七星关区",
    },
    {
        "id": 4,
        "name": "毕节市七星关区政协委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "毕节市政协",
        "location": "贵州省毕节市七星关区",
    },
    {
        "id": 5,
        "name": "毕节市七星关区纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共毕节市纪律检查委员会",
        "location": "贵州省毕节市七星关区",
    },
]

POSITIONS = [
    # 区委书记 (GAP)
    {
        "person_id": 1,
        "org_id": 1,
        "title": "七星关区委书记",
        "start": "未知",
        "end": "现任",
        "rank": "县处级正职",
        "note": "GAP — 姓名和履历均待查",
    },
    # 黄海刚
    {
        "person_id": 2,
        "org_id": 1,
        "title": "七星关区委副书记",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "区政府党组书记",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "七星关区区长",
        "start": "未知",
        "end": "现任",
        "rank": "县处级正职",
        "note": "1976年6月生，汉族，大学学历，中共党员",
    },
    # Deputy leaders — roles unknown
    {"person_id": 3, "org_id": 2, "title": "七星关区领导（副区长等）", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "具体职务待查"},
    {"person_id": 4, "org_id": 2, "title": "七星关区领导（副区长等）", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "具体职务待查"},
    {"person_id": 5, "org_id": 2, "title": "七星关区领导（副区长等）", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "具体职务待查"},
    {"person_id": 6, "org_id": 2, "title": "七星关区领导（副区长等）", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "具体职务待查"},
    {"person_id": 7, "org_id": 2, "title": "七星关区领导（副区长等）", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "具体职务待查"},
    {"person_id": 8, "org_id": 2, "title": "七星关区领导（副区长等）", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "具体职务待查"},
    {"person_id": 9, "org_id": 2, "title": "七星关区领导（副区长等）", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "具体职务待查"},
    {"person_id": 10, "org_id": 2, "title": "七星关区领导（副区长等）", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "具体职务待查"},
    {"person_id": 11, "org_id": 2, "title": "七星关区领导（副区长等）", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "具体职务待查"},
    {"person_id": 12, "org_id": 2, "title": "七星关区领导（副区长等）", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "具体职务待查"},
    {"person_id": 13, "org_id": 2, "title": "七星关区领导（副区长等）", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "具体职务待查"},
]

RELATIONSHIPS = [
    # 黄海刚 is subordinate to the party secretary (who reports to the higher-level party committee)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长搭档关系（区委书记待查）",
        "overlap_org": "中共毕节市七星关区委员会",
        "overlap_period": "现任",
    },
]

DB_PATH = Path("data/tmp/guizhou_七星关区") / "七星关区_network.db"
GEXF_PATH = Path("data/tmp/guizhou_七星关区") / "七星关区_network.gexf"


def main():
    run_build(
        slug="七星关区",
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
