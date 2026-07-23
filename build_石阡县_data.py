#!/usr/bin/env python3
"""Build script for 石阡县 (Shiqian County, Tongren, Guizhou) leadership network.

Generated: 2026-07-23
Level: 县
Province: 贵州省
Parent City: 铜仁市
Targets: 县委书记 & 县长

Research Note:
  The county government website (www.shiqian.gov.cn) was accessible via direct HTTP.
  Current leadership was confirmed through multiple news articles published in June-July 2026
  on the official county website. The county party secretary (史麒麟) concurrently serves as
  铜仁市委副书记 (deputy secretary of the municipal party committee) — a "高配" appointment.

  Web search via Exa was rate-limited and Baidu search was unavailable (403/captcha).
  All research was done via direct HTTP access to the county government website.

Sources:
  - http://www.shiqian.gov.cn/ (石阡县人民政府)
  - http://www.shiqian.gov.cn/ywjj/zwyw/202607/t20260702_90581660.html (两优一先表彰大会)
  - http://www.shiqian.gov.cn/ywjj/zwyw/202606/t20260618_90538422.html (龙川街道揭牌仪式)
  - http://www.shiqian.gov.cn/ywjj/zwyw/202606/t20260605_90480259.html (史麒麟思政课)
  - http://www.shiqian.gov.cn/ywjj/zwyw/202606/t20260605_90483196.html (姚建思政课)
  - http://www.shiqian.gov.cn/ywjj/zwyw/202607/t20260715_90622788.html (姚建防溺水调研)
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
    # 县委书记 (PARTY SECRETARY) — CONFIRMED
    {
        "id": 1,
        "name": "史麒麟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "铜仁市委副书记、石阡县委书记",
        "current_org": "中共铜仁市委员会 / 中共石阡县委员会",
        "source": "http://www.shiqian.gov.cn/ywjj/zwyw/202606/t20260618_90538422.html （官网确认 - 报道中称\u201c市委副书记、县委书记史麒麟\u201d）",
    },
    # 县长 (COUNTY MAYOR) — CONFIRMED
    {
        "id": 2,
        "name": "姚建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石阡县委副书记、县长",
        "current_org": "石阡县人民政府",
        "source": "http://www.shiqian.gov.cn/ywjj/zwyw/202607/t20260702_90581660.html （官网确认 — 报道中主持两优一先表彰大会）",
    },
    # ── 县委领导 (County Party Committee Leaders) ──
    # 县委副书记 #1
    {
        "id": 3,
        "name": "肖贵勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石阡县委副书记",
        "current_org": "中共石阡县委员会",
        "source": "http://www.shiqian.gov.cn/ywjj/zwyw/202607/t20260702_90581660.html （官网确认 — 主持表彰大会）",
    },
    # 县委副书记 #2
    {
        "id": 4,
        "name": "王彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石阡县委副书记",
        "current_org": "中共石阡县委员会",
        "source": "http://www.shiqian.gov.cn/ywjj/zwyw/202607/t20260702_90581660.html （官网确认 — 报道中列出）",
    },
    # 县委常委、组织部部长
    {
        "id": 5,
        "name": "甘卫国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石阡县委常委、县委组织部部长",
        "current_org": "中共石阡县委员会组织部",
        "source": "http://www.shiqian.gov.cn/ywjj/zwyw/202607/t20260702_90581660.html （官网确认 — 宣读表彰决定）",
    },
    # 县委常委、政法委书记
    {
        "id": 6,
        "name": "符前江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石阡县委常委、县委政法委书记",
        "current_org": "中共石阡县委员会政法委员会",
        "source": "http://www.shiqian.gov.cn/ywjj/zwyw/202607/t20260715_90622788.html （官网确认 — 陪同姚建调研防溺水）",
    },
    # 县领导（常委级）
    {
        "id": 7,
        "name": "马辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石阡县领导（县委常委级）",
        "current_org": "中共石阡县委员会",
        "source": "http://www.shiqian.gov.cn/ywjj/zwyw/202606/t20260618_90538422.html （官网确认 — 龙川街道揭牌仪式中列名）",
    },
    # 县领导（常委级）
    {
        "id": 8,
        "name": "周胜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石阡县领导（县委常委级）",
        "current_org": "中共石阡县委员会",
        "source": "http://www.shiqian.gov.cn/ywjj/zwyw/202606/t20260605_90480259.html （官网确认 — 陪同史麒麟调研乡村振兴班）",
    },
    # 县领导
    {
        "id": 9,
        "name": "田永先",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石阡县领导",
        "current_org": "石阡县人民政府",
        "source": "http://www.shiqian.gov.cn/ywjj/zwyw/202606/t20260618_90538422.html （官网确认 — 龙川街道揭牌仪式中列名）",
    },
    # 县领导
    {
        "id": 10,
        "name": "田莉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石阡县领导",
        "current_org": "石阡县人民政府",
        "source": "http://www.shiqian.gov.cn/ywjj/zwyw/202606/t20260618_90538422.html （官网确认 — 龙川街道揭牌仪式中列名）",
    },
    # ── 人大领导 ──
    # 县人大常委会党组书记
    {
        "id": 11,
        "name": "张永恒",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石阡县人大常委会党组书记",
        "current_org": "石阡县人民代表大会常务委员会",
        "source": "http://www.shiqian.gov.cn/ywjj/zwyw/202607/t20260702_90581660.html （官网确认 — 报道中列名）",
    },
    # ── 政协领导 ──
    # 县政协主席
    {
        "id": 12,
        "name": "王刚强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石阡县政协主席",
        "current_org": "中国人民政治协商会议石阡县委员会",
        "source": "http://www.shiqian.gov.cn/ywjj/zwyw/202607/t20260702_90581660.html （官网确认 — 报道中列名）",
    },
]

ORGANIZATIONS = [
    # ── Party Organizations ──
    {
        "id": 1,
        "name": "中共铜仁市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中共贵州省委员会",
        "location": "贵州省铜仁市",
    },
    {
        "id": 2,
        "name": "中共石阡县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共铜仁市委员会",
        "location": "贵州省铜仁市石阡县",
    },
    {
        "id": 3,
        "name": "中共石阡县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共石阡县委员会",
        "location": "贵州省铜仁市石阡县",
    },
    {
        "id": 4,
        "name": "中共石阡县委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共石阡县委员会",
        "location": "贵州省铜仁市石阡县",
    },
    # ── Government Organizations ──
    {
        "id": 5,
        "name": "石阡县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "铜仁市人民政府",
        "location": "贵州省铜仁市石阡县",
    },
    # ── People's Congress ──
    {
        "id": 6,
        "name": "石阡县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "铜仁市人民代表大会常务委员会",
        "location": "贵州省铜仁市石阡县",
    },
    # ── Political Consultative Conference ──
    {
        "id": 7,
        "name": "中国人民政治协商会议石阡县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议铜仁市委员会",
        "location": "贵州省铜仁市石阡县",
    },
]

POSITIONS = [
    # 史麒麟 — multiple concurrent roles
    {"person_id": 1, "org_id": 1, "title": "铜仁市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "高配 — 同时担任石阡县委书记"},
    {"person_id": 1, "org_id": 2, "title": "石阡县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 姚建
    {"person_id": 2, "org_id": 2, "title": "石阡县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 5, "title": "石阡县县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 肖贵勇
    {"person_id": 3, "org_id": 2, "title": "石阡县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 王彬
    {"person_id": 4, "org_id": 2, "title": "石阡县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 甘卫国
    {"person_id": 5, "org_id": 2, "title": "石阡县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "石阡县委组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 符前江
    {"person_id": 6, "org_id": 2, "title": "石阡县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "石阡县委政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马辉
    {"person_id": 7, "org_id": 2, "title": "石阡县领导（县委常委级）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体职务待进一步确认"},
    # 周胜
    {"person_id": 8, "org_id": 2, "title": "石阡县领导（县委常委级）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体职务待进一步确认"},
    # 田永先
    {"person_id": 9, "org_id": 5, "title": "石阡县领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体职务待进一步确认"},
    # 田莉
    {"person_id": 10, "org_id": 5, "title": "石阡县领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体职务待进一步确认"},
    # 张永恒
    {"person_id": 11, "org_id": 6, "title": "石阡县人大常委会党组书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 王刚强
    {"person_id": 12, "org_id": 7, "title": "石阡县政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
]

RELATIONSHIPS = [
    # ── Top-two leadership relationship ──
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭班子",
        "overlap_org": "中共石阡县委员会 / 石阡县人民政府",
        "overlap_period": "2026年至今",
    },
    # ── 县委副书记之间 ──
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "均为石阡县委副书记",
        "overlap_org": "中共石阡县委员会",
        "overlap_period": "2026年",
    },
    # ── 县领导与县长 ──
    {
        "person_a": 5, "person_b": 2,
        "type": "superior_subordinate",
        "context": "组织部长在县长领导下工作",
        "overlap_org": "中共石阡县委员会",
        "overlap_period": "2026年",
    },
    {
        "person_a": 6, "person_b": 2,
        "type": "superior_subordinate",
        "context": "政法委书记在县长领导下工作",
        "overlap_org": "中共石阡县委员会",
        "overlap_period": "2026年",
    },
]

# fmt: on

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "石阡县_network.db"
GEXF_PATH = STAGING_DIR / "石阡县_network.gexf"


def main() -> None:
    run_build(
        slug="石阡县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("✅ 石阡县 network build complete.")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
