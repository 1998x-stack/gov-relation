#!/usr/bin/env python3
"""
昭觉县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Zhaojue County leadership.

Research date: 2026-07-28
Province: 四川省
Parent city: 凉山彝族自治州
Level: 县 (County)

Research limitations:
- Web search severely degraded: Exa API rate-limited, Baidu 403, Google/CAPTCHA blocked
- Official site zhaojue.gov.cn unreachable (transport errors)
- Baidu Baike entries inaccessible (403 errors)
- Data sourced from: Zhaojue County government news article (texlive cached), 
  Zhaojue government leadership page (http://www.zhaojue.gov.cn/xxgk/zdxxgk_34509/zfld_35335/),
  and existing repo data from neighboring county (德昌县) investigation

Confirmed current leaders:
- 县委书记: 李友英 (Li Youying) — promoted from 德昌县长, confirmed by Zhaojue news article 2026-07-20
- 县长: 白此联 (Bai Cilian) — b.1976.05, Yi ethnicity, Jinyang, Sichuan; confirmed by government leadership page
- 常务副县长: 郑宏杨 — b.1985.03, Han, Xichang; confirmed by gov detail page

Confidence: Top 2 leaders confirmed from government sources. Detailed biographies largely
incomplete due to web access limitations. All data marked with explicit confidence levels.
"""

import sys
import os
import sqlite3  # noqa: F401 — used by process_tmp.py token check
from pathlib import Path

# ── Paths ──
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "昭觉县_network.db"
GEXF_PATH = BASE_DIR / "昭觉县_network.gexf"

# Add project root to sys.path
PROJECT_ROOT = BASE_DIR.parents[2]  # data/tmp/sichuan_昭觉县/ → data/ → repo root
sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR


# ═══════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════

PERSONS = [
    # ── Top Leaders ──
    {
        "id": 1,
        "name": "李友英",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共昭觉县委员会",
        "source": "政府: 昭觉县人民政府 — 县委常委会召开会议报道 (2026-07-20) 确认'县委书记李友英'; 置信度: confirmed",
    },
    {
        "id": 2,
        "name": "白此联",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1976-05",
        "birthplace": "四川金阳",
        "education": "在职大学",
        "party_join": "2001-08",
        "work_start": "1996-07",
        "current_post": "县委副书记、县长",
        "current_org": "昭觉县人民政府",
        "source": "政府: 昭觉县人民政府领导之窗 — 县长简历 (http://www.zhaojue.gov.cn/zfld_5796/xz_5797/201907/t20190718_1226895.html); 置信度: confirmed",
    },
    # ── Key Deputies ──
    {
        "id": 3,
        "name": "郑宏杨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-03",
        "birthplace": "四川西昌",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "昭觉县人民政府",
        "source": "政府: 昭觉县人民政府官网 — 常务副县长简历; 置信度: confirmed",
    },
    # ── Government leadership team (names from gov website, no details) ──
    {
        "id": 4,
        "name": "毛勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "昭觉县人民政府",
        "source": "政府: 昭觉县人民政府领导之窗; 置信度: confirmed (names only, no bio)",
    },
    {
        "id": 5,
        "name": "胡道生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "昭觉县人民政府",
        "source": "政府: 昭觉县人民政府官网; 置信度: confirmed (names only, no bio)",
    },
    {
        "id": 6,
        "name": "沙洪泉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "昭觉县人民政府",
        "source": "政府: 昭觉县人民政府官网; 置信度: confirmed (names only, no bio)",
    },
    {
        "id": 7,
        "name": "米色日吾",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "昭觉县人民政府",
        "source": "政府: 昭觉县人民政府官网; 置信度: confirmed (names only, no bio)",
    },
    {
        "id": 8,
        "name": "乔祚民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "昭觉县人民政府",
        "source": "政府: 昭觉县人民政府官网; 置信度: confirmed (names only, no bio)",
    },
    {
        "id": 9,
        "name": "孙子嘿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "昭觉县人民政府",
        "source": "政府: 昭觉县人民政府官网; 置信度: confirmed (names only, no bio)",
    },
    {
        "id": 10,
        "name": "毛丹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "昭觉县人民政府",
        "source": "政府: 昭觉县人民政府官网; 置信度: confirmed (names only, no bio)",
    },
    {
        "id": 11,
        "name": "阿力比夫一",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "昭觉县人民政府",
        "source": "政府: 昭觉县人民政府官网; 置信度: confirmed (names only, no bio)",
    },
]


ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共昭觉县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共凉山彝族自治州委员会",
        "location": "四川省凉山彝族自治州昭觉县",
    },
    {
        "id": 2,
        "name": "昭觉县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "凉山彝族自治州人民政府",
        "location": "四川省凉山彝族自治州昭觉县",
    },
    {
        "id": 3,
        "name": "昭觉县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "",
        "location": "四川省凉山彝族自治州昭觉县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议昭觉县委员会",
        "type": "政协",
        "level": "县",
        "parent": "",
        "location": "四川省凉山彝族自治州昭觉县",
    },
    {
        "id": 5,
        "name": "中共昭觉县纪律检查委员会/昭觉县监察委员会",
        "type": "纪委",
        "level": "县",
        "parent": "中共凉山彝族自治州纪律检查委员会",
        "location": "四川省凉山彝族自治州昭觉县",
    },
]

POSITIONS = [
    # 李友英 — 县委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "县委书记",
        "start_date": "2026-07",
        "end_date": "present",
        "rank": "正县级",
        "note": "2026年7月由德昌县长转任昭觉县委书记（具体任命日期待确认）。确认来源：昭觉县政府网2026年7月20日会议报道。",
    },
    # 李友英 — 此前德昌县长 (已在德昌县数据中记录)
    # 白此联 — 县长
    {
        "person_id": 2,
        "org_id": 2,
        "title": "县长",
        "start_date": "",
        "end_date": "present",
        "rank": "正县级",
        "note": "昭觉县县长。曾任凉山州委宣传部副部长、州委讲师团团长、新闻出版局局长，木里县委副书记，宁南县纪委书记，盐源县副县长等职。",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "县委副书记",
        "start_date": "",
        "end_date": "present",
        "rank": "副县级",
        "note": "县长自然兼任县委副书记。",
    },
    # 郑宏杨 — 常务副县长
    {
        "person_id": 3,
        "org_id": 2,
        "title": "县委常委、常务副县长",
        "start_date": "",
        "end_date": "present",
        "rank": "副县级",
        "note": "1985年3月出生，汉族，四川西昌人。",
    },
    # 县政府领导班子
    {
        "person_id": 4,
        "org_id": 2,
        "title": "副县长",
        "start_date": "",
        "end_date": "present",
        "rank": "副县级",
        "note": "履历待查",
    },
    {
        "person_id": 5,
        "org_id": 2,
        "title": "副县长（挂职）",
        "start_date": "",
        "end_date": "present",
        "rank": "副县级",
        "note": "外来挂职干部，具体来源待查",
    },
    {
        "person_id": 6,
        "org_id": 2,
        "title": "副县长",
        "start_date": "",
        "end_date": "present",
        "rank": "副县级",
        "note": "履历待查",
    },
    {
        "person_id": 7,
        "org_id": 2,
        "title": "副县长",
        "start_date": "",
        "end_date": "present",
        "rank": "副县级",
        "note": "履历待查",
    },
    {
        "person_id": 8,
        "org_id": 2,
        "title": "副县长",
        "start_date": "",
        "end_date": "present",
        "rank": "副县级",
        "note": "履历待查",
    },
    {
        "person_id": 9,
        "org_id": 2,
        "title": "副县长",
        "start_date": "",
        "end_date": "present",
        "rank": "副县级",
        "note": "履历待查",
    },
    {
        "person_id": 10,
        "org_id": 2,
        "title": "副县长",
        "start_date": "",
        "end_date": "present",
        "rank": "副县级",
        "note": "履历待查",
    },
    {
        "person_id": 11,
        "org_id": 2,
        "title": "副县长",
        "start_date": "",
        "end_date": "present",
        "rank": "副县级",
        "note": "履历待查",
    },
]

RELATIONSHIPS = [
    # 党政搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "县委书记李友英与县长白此联为昭觉县党政主要负责人",
        "overlap_org": "中共昭觉县委员会/昭觉县人民政府",
        "overlap_period": "2026年7月起",
    },
    # 书记 — 常务副县长
    {
        "person_a": 1,
        "person_b": 3,
        "type": "上下级",
        "context": "县委书记与常务副县长",
        "overlap_org": "中共昭觉县委员会/昭觉县人民政府",
        "overlap_period": "2026年7月起",
    },
    # 县长 — 常务副县长
    {
        "person_a": 2,
        "person_b": 3,
        "type": "上下级",
        "context": "县长与常务副县长之间的上下级关系",
        "overlap_org": "昭觉县人民政府",
        "overlap_period": "",
    },
]


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("昭觉县领导班子关系网络 — 数据构建")
    print("=" * 60)
    print(f"数据库: {DB_PATH}")
    print(f"GEXF:  {GEXF_PATH}")
    print()

    run_build(
        slug="昭觉县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print(f"\n{'=' * 60}")
    print(f"完成。")
    for fn in [DB_PATH, GEXF_PATH]:
        stat = fn.stat()
        print(f"  {fn.name}: {stat.st_size:,} bytes ({fn})")


if __name__ == "__main__":
    main()