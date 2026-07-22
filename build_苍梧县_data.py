#!/usr/bin/env python3
"""Build script for 苍梧县 (Cangwu County, Wuzhou, Guangxi) leadership network.

Generated: 2026-07-23
Level: 县
Province: 广西壮族自治区
Parent City: 梧州市
Targets: 县委书记 & 县长

Research Note:
  All data sourced from cangwu.gov.cn official website (accessible via HTTP).
  The county government site (www.cangwu.gov.cn) was reachable and provided
  leadership bios, news articles, and meeting coverage.
  Baidu Baike, Exa, and several Chinese government sites were unreachable
  during this investigation.

Confirmed findings (as of 2026-07-22):
  - 瞿志英 (Qu Zhiying) — 苍梧县委书记 (confirmed by multiple news articles)
  - 张东方 (Zhang Dongfang) — 苍梧县委副书记、县长 (confirmed by multiple news articles)
  - Full deputy roster from cangwu.gov.cn leadership page (as of 2026-02-12):
    吕尚琳, 吴小龙, 李华, 陈璐然, 曹璋, 邓雄彬, 陈超文

Sources:
  - http://www.cangwu.gov.cn/ (苍梧县人民政府门户网站)
  - http://www.cangwu.gov.cn/xxgk/gkbz/fdzdgknr/ldjj/ (领导简介)
  - http://www.cangwu.gov.cn/xxgk/gkbz/fdzdgknr/ldjj/fuxianzhang/ (副县长列表)
  - Individual deputy bio pages (t27090092.shtml through t2910100.shtml)
  - News articles from cangwu.gov.cn: t27528245, t27550292, t27736230, etc.
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
    {
        "id": 1,
        "name": "瞿志英",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "苍梧县委书记",
        "current_org": "中共苍梧县委员会",
        "source": "http://www.cangwu.gov.cn/ — 苍梧县新闻多次报道瞿志英以县委书记身份出席会议、调研检查（2026-05至07月）",
    },
    {
        "id": 2,
        "name": "张东方",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "苍梧县委副书记、县长",
        "current_org": "苍梧县人民政府",
        "source": "http://www.cangwu.gov.cn/ — 新闻报道确认张东方以县委副书记、县长身份出席活动（2026-05）",
    },
    # ── 县委常委、常务副县长 ──
    {
        "id": 3,
        "name": "吕尚琳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年8月",
        "birthplace": "",
        "education": "研究生学历，法律硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "苍梧县委常委（保留正处长级）、副县长（常务）",
        "current_org": "苍梧县人民政府",
        "source": "http://www.cangwu.gov.cn/xxgk/gkbz/fdzdgknr/ldjj/fuxianzhang/t27090092.shtml (2026-02-12)",
    },
    # ── 挂职县委常委、副县长 ──
    {
        "id": 4,
        "name": "吴小龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年7月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "苍梧县委委员、常委、副县长（挂职），广西驻村工作队苍梧县工作队队长",
        "current_org": "苍梧县人民政府",
        "source": "http://www.cangwu.gov.cn/xxgk/gkbz/fdzdgknr/ldjj/fuxianzhang/t2910090.shtml (2026-02-12)",
    },
    # ── 县委常委、统战部部长、副县长 ──
    {
        "id": 5,
        "name": "李华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年2月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "苍梧县委常委、统战部部长、副县长",
        "current_org": "苍梧县人民政府",
        "source": "http://www.cangwu.gov.cn/xxgk/gkbz/fdzdgknr/ldjj/fuxianzhang/t19944383.shtml (2026-02-12)",
    },
    # ── 副县长 ──
    {
        "id": 6,
        "name": "陈璐然",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "",
        "education": "农学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "苍梧县人民政府副县长",
        "current_org": "苍梧县人民政府",
        "source": "http://www.cangwu.gov.cn/xxgk/gkbz/fdzdgknr/ldjj/fuxianzhang/t2910100.shtml (2026-02-12)",
    },
    # ── 副县长 ──
    {
        "id": 7,
        "name": "曹璋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年9月",
        "birthplace": "",
        "education": "工学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "苍梧县人民政府副县长",
        "current_org": "苍梧县人民政府",
        "source": "http://www.cangwu.gov.cn/xxgk/gkbz/fdzdgknr/ldjj/fuxianzhang/t2910107.shtml (2026-02-12)",
    },
    # ── 副县长 ──
    {
        "id": 8,
        "name": "邓雄彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年8月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "苍梧县人民政府副县长",
        "current_org": "苍梧县人民政府",
        "source": "http://www.cangwu.gov.cn/xxgk/gkbz/fdzdgknr/ldjj/fuxianzhang/t18892461.shtml (2026-02-12)",
    },
    # ── 副县长、县公安局局长 ──
    {
        "id": 9,
        "name": "陈超文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年2月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "苍梧县人民政府副县长、县公安局党委书记、局长",
        "current_org": "苍梧县人民政府",
        "source": "http://www.cangwu.gov.cn/xxgk/gkbz/fdzdgknr/ldjj/fuxianzhang/t2910095.shtml (2026-02-12)",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共苍梧县委员会",
        "type": "党委",
        "level": "县",
        "parent": "梧州市",
        "location": "苍梧县",
    },
    {
        "id": 2,
        "name": "苍梧县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "梧州市",
        "location": "苍梧县",
    },
]

POSITIONS = [
    # 瞿志英 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "苍梧县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "截至2026-07-22在任"},
    # 张东方 - 县长
    {"person_id": 2, "org_id": 2, "title": "苍梧县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "截至2026-05-01在任"},
    # 吕尚琳 - 常务副县长
    {"person_id": 3, "org_id": 2, "title": "苍梧县委常委、副县长（常务）", "start_date": "", "end_date": "present", "rank": "正处级（保留）", "note": "截至2026-02-12在任"},
    # 吴小龙 - 挂职副县长
    {"person_id": 4, "org_id": 2, "title": "苍梧县委委员、常委、副县长（挂职）", "start_date": "", "end_date": "present", "rank": "", "note": "广西驻村工作队苍梧县工作队队长"},
    # 李华 - 统战部长、副县长
    {"person_id": 5, "org_id": 2, "title": "苍梧县委常委、统战部部长、副县长", "start_date": "", "end_date": "present", "rank": "", "note": "截至2026-02-12在任"},
    # 陈璐然 - 副县长
    {"person_id": 6, "org_id": 2, "title": "苍梧县人民政府副县长", "start_date": "", "end_date": "present", "rank": "", "note": "截至2026-02-12在任"},
    # 曹璋 - 副县长
    {"person_id": 7, "org_id": 2, "title": "苍梧县人民政府副县长", "start_date": "", "end_date": "present", "rank": "", "note": "截至2026-02-12在任"},
    # 邓雄彬 - 副县长
    {"person_id": 8, "org_id": 2, "title": "苍梧县人民政府副县长", "start_date": "", "end_date": "present", "rank": "", "note": "截至2026-02-12在任"},
    # 陈超文 - 副县长、公安局局长
    {"person_id": 9, "org_id": 2, "title": "苍梧县人民政府副县长、县公安局局长", "start_date": "", "end_date": "present", "rank": "", "note": "截至2026-02-12在任"},
]

RELATIONSHIPS = [
    # 瞿志英 <-> 张东方：党政一把手工作搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长党政搭档关系",
        "overlap_org": "中共苍梧县委员会/苍梧县人民政府",
        "overlap_period": "2026",
    },
    # 瞿志英 <-> 吕尚琳：县委常委会搭档
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委/常务副县长上下级关系",
        "overlap_org": "中共苍梧县委员会",
        "overlap_period": "2026",
    },
    # 张东方 <-> 吕尚琳：政府班子搭档
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与常务副县长政府班子搭档",
        "overlap_org": "苍梧县人民政府",
        "overlap_period": "2026",
    },
    # 张东方 <-> 曹璋：政府班子搭档（招商考察同往）
    {
        "person_a": 2, "person_b": 7,
        "type": "overlap",
        "context": "张东方率队赴上海广州招商考察时，曹璋陪同",
        "overlap_org": "苍梧县人民政府",
        "overlap_period": "2026-05",
    },
    # 张东方 <-> 邓雄彬：政府班子搭档（招商考察同往）
    {
        "person_a": 2, "person_b": 8,
        "type": "overlap",
        "context": "张东方率队赴上海广州招商考察时，邓雄彬陪同",
        "overlap_org": "苍梧县人民政府",
        "overlap_period": "2026-05",
    },
]

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

SLUG = "苍梧县"
DB_PATH = Path("data/tmp/guangxi_苍梧县") / f"{SLUG}_network.db"
GEXF_PATH = Path("data/tmp/guangxi_苍梧县") / f"{SLUG}_network.gexf"


def main():
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )


if __name__ == "__main__":
    main()
