#!/usr/bin/env python3
"""Build SQLite DB and GEXF for 塔什库尔干塔吉克自治县 (Taxkorgan Tajik Autonomous County).

Data sources (all confirmed from official county website www.tskeg.gov.cn):
- 2026-07-01 news: Party Secretary 李锋 leads 七一走访慰问
- Leadership pages: 开巴奴·斯提卡达木 and all 副县长 bios
- 2026-07-22 news: 库尔班库力·卡马斯 as 人大常委会主任
"""

import sys, os
from pathlib import Path

_script_path = Path(__file__).resolve()
_repo_root = _script_path.parents[2]
sys.path.insert(0, str(_repo_root))

from gov_relation.runner import run_build
import sqlite3

STAGING_DIR = _repo_root / "data/tmp/xinjiang_塔什库尔干塔吉克自治县"
DB_PATH = STAGING_DIR / "塔什库尔干塔吉克自治县_network.db"
GEXF_PATH = STAGING_DIR / "塔什库尔干塔吉克自治县_network.gexf"

# ═══════════════════════════════════════════════════════════════════════
# Persons — all confirmed from www.tskeg.gov.cn (official source)
# ═══════════════════════════════════════════════════════════════════════
persons = [
    {
        "id": 1, "name": "李锋", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "塔什库尔干塔吉克自治县委书记",
        "current_org": "中共塔什库尔干塔吉克自治县委员会",
        "source": "www.tskeg.gov.cn 2026-07-01 七一慰问报道",
    },
    {
        "id": 2, "name": "开巴奴·斯提卡达木", "gender": "女",
        "ethnicity": "塔吉克族", "birth": "1986年5月",
        "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "塔什库尔干塔吉克自治县委副书记、人民政府党组书记、县长",
        "current_org": "塔什库尔干塔吉克自治县人民政府",
        "source": "www.tskeg.gov.cn/tskeg/ldzc/202107/267fb3736bf04fa1ab9e704258215bf6.shtml",
    },
    {
        "id": 3, "name": "赵广为", "gender": "男", "ethnicity": "汉族",
        "birth": "1983年7月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "塔什库尔干县委常委、人民政府党组成员、副县长（挂职）",
        "current_org": "塔什库尔干塔吉克自治县人民政府",
        "source": "www.tskeg.gov.cn/tskeg/ldzc/202309/cb92980d3ee14ea843e702db2b2ae27.shtml",
    },
    {
        "id": 4, "name": "夏尔亚德·达吾提", "gender": "男",
        "ethnicity": "塔吉克族", "birth": "1984年1月",
        "birthplace": "", "education": "大专",
        "party_join": "中共党员", "work_start": "",
        "current_post": "塔什库尔干县人民政府党组成员、副县长",
        "current_org": "塔什库尔干塔吉克自治县人民政府",
        "source": "www.tskeg.gov.cn/tskeg/ldzc/202107/d92150d8be25430e93d2906897bc6c24.shtml",
    },
    {
        "id": 5, "name": "马明", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年7月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "塔什库尔干县人民政府党组成员、副县长",
        "current_org": "塔什库尔干塔吉克自治县人民政府",
        "source": "www.tskeg.gov.cn/tskeg/ldzc/202405/ac478f22bc36442c1258b3a698c2083e.shtml",
    },
    {
        "id": 6, "name": "阿曼古丽·约力瓦斯", "gender": "女",
        "ethnicity": "塔吉克族", "birth": "1992年8月",
        "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "塔什库尔干县人民政府党组成员、副县长",
        "current_org": "塔什库尔干塔吉克自治县人民政府",
        "source": "www.tskeg.gov.cn/tskeg/ldzc/202412/b4130058ef394708ace500000b4d22528.shtml",
    },
    {
        "id": 7, "name": "李兆轩", "gender": "男", "ethnicity": "汉族",
        "birth": "1986年10月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "塔什库尔干县人民政府党组成员、副县长、公安局党委书记、局长、四级高级警长",
        "current_org": "塔什库尔干塔吉克自治县公安局",
        "source": "www.tskeg.gov.cn/tskeg/ldzc/202503/cfcc9ddd29cd4675927385aeb9bac4b6.shtml",
    },
    {
        "id": 8, "name": "库尔班库力·卡马斯", "gender": "男",
        "ethnicity": "塔吉克族", "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "塔什库尔干县人大常委会党组副书记、主任",
        "current_org": "塔什库尔干县人民代表大会常务委员会",
        "source": "www.tskeg.gov.cn 2026-07-22 人大常委会会议报道",
    },
]

# ═══════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════
organizations = [
    {
        "id": 1, "name": "中共塔什库尔干塔吉克自治县委员会",
        "type": "党委", "level": "县处级",
        "parent": "中共喀什地委",
        "location": "新疆维吾尔自治区喀什地区塔什库尔干塔吉克自治县",
    },
    {
        "id": 2, "name": "塔什库尔干塔吉克自治县人民政府",
        "type": "政府", "level": "县处级",
        "parent": "喀什地区行政公署",
        "location": "新疆维吾尔自治区喀什地区塔什库尔干塔吉克自治县",
    },
    {
        "id": 3, "name": "塔什库尔干塔吉克自治县公安局",
        "type": "政府", "level": "乡科级",
        "parent": "塔什库尔干塔吉克自治县人民政府",
        "location": "新疆维吾尔自治区喀什地区塔什库尔干塔吉克自治县",
    },
    {
        "id": 4, "name": "塔什库尔干塔吉克自治县人民代表大会常务委员会",
        "type": "人大", "level": "县处级",
        "parent": "喀什地区人大工作委员会",
        "location": "新疆维吾尔自治区喀什地区塔什库尔干塔吉克自治县",
    },
]

# ═══════════════════════════════════════════════════════════════════════
# Positions — confirmed current roles as of 2026-07
# ═══════════════════════════════════════════════════════════════════════
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记",
     "start_date": "", "end_date": "", "rank": "正县级",
     "note": "as of 2026-07-01 confirmed"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记",
     "start_date": "", "end_date": "", "rank": "正县级",
     "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长、政府党组书记",
     "start_date": "", "end_date": "", "rank": "正县级",
     "note": ""},
    {"person_id": 3, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "", "rank": "副县级",
     "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副县长（挂职）",
     "start_date": "", "end_date": "", "rank": "副县级",
     "note": "挂职干部来自鞍钢集团"},
    {"person_id": 4, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "", "rank": "副县级",
     "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "", "rank": "副县级",
     "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "", "rank": "副县级",
     "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "", "rank": "副县级",
     "note": ""},
    {"person_id": 7, "org_id": 3, "title": "公安局党委书记、局长、四级高级警长",
     "start_date": "", "end_date": "", "rank": "副县级",
     "note": ""},
    {"person_id": 8, "org_id": 4, "title": "县人大常委会党组副书记、主任",
     "start_date": "", "end_date": "", "rank": "正县级",
     "note": "confirmed 2026-07-21"},
]

# ═══════════════════════════════════════════════════════════════════════
# Relationships — work overlap confirmed from same org/time
# ═══════════════════════════════════════════════════════════════════════
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "党政搭档",
        "context": "县委书记与县长（党政主要领导）",
        "overlap_org": "中共塔什库尔干塔吉克自治县委员会",
        "overlap_period": "2026年至今",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "上下级",
        "context": "县长与副县长（挂职）",
        "overlap_org": "塔什库尔干塔吉克自治县人民政府",
        "overlap_period": "2026年至今",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "上下级",
        "context": "县长与副县长",
        "overlap_org": "塔什库尔干塔吉克自治县人民政府",
        "overlap_period": "2026年至今",
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "上下级",
        "context": "县长与副县长",
        "overlap_org": "塔什库尔干塔吉克自治县人民政府",
        "overlap_period": "2026年至今",
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "上下级",
        "context": "县长与副县长",
        "overlap_org": "塔什库尔干塔吉克自治县人民政府",
        "overlap_period": "2026年至今",
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "上下级",
        "context": "县长与副县长兼公安局长",
        "overlap_org": "塔什库尔干塔吉克自治县人民政府",
        "overlap_period": "2026年至今",
    },
    {
        "person_a": 1, "person_b": 8,
        "type": "工作关系",
        "context": "县委与人大常委会主要领导之间协作",
        "overlap_org": "塔什库尔干塔吉克自治县",
        "overlap_period": "2026年至今",
    },
]

# ═══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    os.makedirs(str(STAGING_DIR), exist_ok=True)
    db_path = str(DB_PATH)
    gexf_path = str(GEXF_PATH)

    run_build(
        slug="塔什库尔干塔吉克自治县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"\n{'='*60}")
    print(f"Build complete for 塔什库尔干塔吉克自治县")
    print(f"  DB:   {db_path}")
    print(f"  GEXF: {gexf_path}")
    print(f"  Persons:       {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions:     {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"{'='*60}")