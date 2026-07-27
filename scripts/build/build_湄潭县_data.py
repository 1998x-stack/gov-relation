#!/usr/bin/env python3
"""
Build 湄潭县 (Meitan County — county under 遵义市, 贵州省)
government personnel network database and GEXF graph.

Current leadership as of 2026-07-23:
- 张如仲: 湄潭县委书记、县人民政府县长 (县委书记 appointed ~July 2026, previously 县长)
- 游海燕: 前任湄潭县委书记 (departed ~June/July 2026)

Based on official sources from www.meitan.gov.cn leadership pages and news articles.
"""
import os
import sqlite3
import sys
from datetime import datetime

# ── Add repo root to path ──────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

today = datetime.now().strftime("%Y-%m-%d")

# ── Paths ──────────────────────────────────────────────────────────────
DB_PATH = os.path.join(BASE, "湄潭县_network.db")
GEXF_PATH = os.path.join(BASE, "湄潭县_network.gexf")

# =========================================================================
# DATA
# =========================================================================

persons = [
    # ── Core Leaders (县委) ──
    {
        "id": 1,
        "name": "张如仲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989-09",
        "birthplace": "",
        "education": "研究生（经济学硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湄潭县委书记、县人民政府县长",
        "current_org": "中共湄潭县委员会",
        "source": "湄潭县人民政府领导之窗(www.meitan.gov.cn)—县委副书记、县政府党组书记、县人民政府县长；2026年7月13日湄潭要闻《张如仲张宇走访慰问老同志》中张如仲以县委书记身份出现（meitan.gov.cn/mtzx/mtyw/202607/t20260714_90617317.html）",
    },
    {
        "id": 2,
        "name": "游海燕",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任湄潭县委书记（~2026年6月离任）",
        "current_org": "中共湄潭县委员会（前任）",
        "source": "湄潭要闻—2026年6月26日县委常委会会议（meitan.gov.cn/mtzx/mtyw/202606/t20260629_90563539.html）提及县委书记游海燕主持会议；6月29日县委党的建设工作领导小组会议同样提及",
    },
    {
        "id": 3,
        "name": "张宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湄潭县委副书记",
        "current_org": "中共湄潭县委员会",
        "source": "湄潭要闻—2026年7月13日《张如仲张宇走访慰问老同志》（meitan.gov.cn/mtzx/mtyw/202607/t20260714_90617317.html）",
    },
    {
        "id": 4,
        "name": "陈兴建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湄潭县委副书记",
        "current_org": "中共湄潭县委员会",
        "source": "湄潭要闻—2026年6月26日县委常委会会议（meitan.gov.cn/mtzx/mtyw/202606/t20260629_90563539.html）提及县委副书记陈兴建",
    },
    # ── Government Leaders ──
    {
        "id": 5,
        "name": "张修德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-03",
        "birthplace": "贵州遵义",
        "education": "清华大学土木工程专业，研究生学历",
        "party_join": "中共党员（2005-12入党）",
        "work_start": "2011-07",
        "current_post": "湄潭县人民政府党组成员、副县长",
        "current_org": "湄潭县人民政府",
        "source": "湄潭县人民政府领导之窗(www.meitan.gov.cn/zwgk/ldzc_5981454/202503/t20250321_87223744.html)",
    },
    {
        "id": 6,
        "name": "肖艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984-07",
        "birthplace": "四川安岳",
        "education": "大学理学学士，省委党校在职研究生",
        "party_join": "中共党员（2004-11入党）",
        "work_start": "2005-10",
        "current_post": "湄潭县人民政府副县长",
        "current_org": "湄潭县人民政府",
        "source": "湄潭县人民政府领导之窗(www.meitan.gov.cn/zwgk/ldzc_5981454/202512/t20251201_89003427.html)",
    },
    {
        "id": 7,
        "name": "冯波",
        "gender": "男",
        "ethnicity": "仡佬族",
        "birth": "1983-10",
        "birthplace": "贵州正安",
        "education": "贵州大学光信息科学与技术专业，大学本科",
        "party_join": "中共党员（2010-08入党）",
        "work_start": "2006-12",
        "current_post": "湄潭县人民政府党组成员、副县长、县公安局局长",
        "current_org": "湄潭县人民政府",
        "source": "湄潭县人民政府领导之窗(www.meitan.gov.cn/zwgk/ldzc_5981454/202503/t20250321_87223739.html)",
    },
    {
        "id": 8,
        "name": "周洁",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1983-02",
        "birthplace": "贵州湄潭",
        "education": "贵州师范大学图书馆学专业，大学学历",
        "party_join": "中共党员（2007-08入党）",
        "work_start": "2006-07",
        "current_post": "湄潭县人民政府党组成员、副县长",
        "current_org": "湄潭县人民政府",
        "source": "湄潭县人民政府领导之窗(www.meitan.gov.cn/zwgk/ldzc_5981454/202503/t20250321_87223738.html)",
    },
    # ──人大、政协──
    {
        "id": 9,
        "name": "袁朝辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湄潭县人大常委会主任",
        "current_org": "湄潭县人大常委会",
        "source": "湄潭要闻—2026年6月26日县委常委会会议（meitan.gov.cn/mtzx/mtyw/202606/t20260629_90563539.html）",
    },
    {
        "id": 10,
        "name": "卢天宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湄潭县政协主席",
        "current_org": "政协湄潭县委员会",
        "source": "湄潭要闻—2026年6月26日县委常委会会议（meitan.gov.cn/mtzx/mtyw/202606/t20260629_90563539.html）",
    },
    # ──其他县领导──
    {
        "id": 11,
        "name": "兰新彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湄潭县领导",
        "current_org": "中共湄潭县委员会",
        "source": "湄潭要闻—2026年7月13日《张如仲张宇走访慰问老同志》（meitan.gov.cn/mtzx/mtyw/202607/t20260714_90617317.html）",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共湄潭县委员会",
        "type": "党委",
        "level": "县级",
        "location": "贵州省遵义市湄潭县",
    },
    {
        "id": 2,
        "name": "湄潭县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "贵州省遵义市湄潭县",
    },
    {
        "id": 3,
        "name": "湄潭县人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "贵州省遵义市湄潭县",
    },
    {
        "id": 4,
        "name": "政协湄潭县委员会",
        "type": "政协",
        "level": "县级",
        "location": "贵州省遵义市湄潭县",
    },
    {
        "id": 5,
        "name": "中共遵义市委员会",
        "type": "党委",
        "level": "地市级",
        "location": "贵州省遵义市",
    },
]

positions = [
    # 张如仲 — 县委书记兼县长
    {"person_id": 1, "org_id": 1, "title": "湄潭县委书记", "start": "~2026-07", "end": "", "rank": "正县级", "note": "原县长升任县委书记"},
    {"person_id": 1, "org_id": 2, "title": "湄潭县人民政府县长", "start": "~2025", "end": "", "rank": "正县级", "note": "县委副书记、县政府党组书记"},
    # 游海燕
    {"person_id": 2, "org_id": 1, "title": "湄潭县委书记（前任）", "start": "", "end": "~2026-06", "rank": "正县级", "note": "2026年6月仍在岗，7月已由张如仲接任"},
    # 张宇
    {"person_id": 3, "org_id": 1, "title": "湄潭县委副书记", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 陈兴建
    {"person_id": 4, "org_id": 1, "title": "湄潭县委副书记", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 张修德
    {"person_id": 5, "org_id": 2, "title": "湄潭县人民政府副县长", "start": "", "end": "", "rank": "副县级", "note": "县政府党组成员，分管交通运输、卫健、医保、民政等"},
    # 肖艳
    {"person_id": 6, "org_id": 2, "title": "湄潭县人民政府副县长", "start": "", "end": "", "rank": "副县级", "note": "分管文化旅游、市场监管、招商引资等"},
    # 冯波
    {"person_id": 7, "org_id": 2, "title": "湄潭县人民政府副县长、县公安局局长", "start": "", "end": "", "rank": "副县级", "note": "分管公安、司法、退役军人等"},
    # 周洁
    {"person_id": 8, "org_id": 2, "title": "湄潭县人民政府副县长", "start": "", "end": "", "rank": "副县级", "note": "分管农业农村、茶产业、林业等"},
    # 袁朝辉
    {"person_id": 9, "org_id": 3, "title": "湄潭县人大常委会主任", "start": "", "end": "", "rank": "正县级", "note": ""},
    # 卢天宇
    {"person_id": 10, "org_id": 4, "title": "政协湄潭县委员会主席", "start": "", "end": "", "rank": "正县级", "note": ""},
    # 兰新彬
    {"person_id": 11, "org_id": 1, "title": "湄潭县领导", "start": "", "end": "", "rank": "", "note": ""},
]

relationships = [
    # 工作交接关系 - 游海燕→张如仲
    {"person_a": 2, "person_b": 1, "type": "succession", "context": "游海燕与张如仲完成县委书记交接（2026年6-7月）", "overlap_org": "中共湄潭县委员会", "overlap_period": "2026"},
    # 党政搭档 - 张如仲(书记+县长)与县委副书记们
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "张如仲（县委书记）与张宇（县委副书记）", "overlap_org": "中共湄潭县委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "张如仲（县委书记）与陈兴建（县委副书记）", "overlap_org": "中共湄潭县委员会", "overlap_period": "2026"},
    # 县政府班子
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "张如仲（县长）与张修德（副县长）", "overlap_org": "湄潭县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "张如仲（县长）与肖艳（副县长）", "overlap_org": "湄潭县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "张如仲（县长）与冯波（副县长）", "overlap_org": "湄潭县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "张如仲（县长）与周洁（副县长）", "overlap_org": "湄潭县人民政府", "overlap_period": ""},
    # 县委与人大、政协
    {"person_a": 1, "person_b": 9, "type": "colleague", "context": "张如仲（县委书记）与袁朝辉（人大主任）", "overlap_org": "湄潭县", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "colleague", "context": "张如仲（县委书记）与卢天宇（政协主席）", "overlap_org": "湄潭县", "overlap_period": ""},
]

# =========================================================================
# BUILD
# =========================================================================

if __name__ == "__main__":
    run_build(
        slug="湄潭县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"✅ Database: {DB_PATH}")
    print(f"✅ GEXF: {GEXF_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")
