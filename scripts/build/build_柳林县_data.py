#!/usr/bin/env python3
"""Build 柳林县 leadership network database and GEXF graph.

Current leadership as of 2026-07-26:

县委书记: 杨月祥
  - Born 1971.02, 山西方山人, 省委党校研究生
  - Previously: 方山县委副书记, 吕梁市信访局长, 吕梁市商务局长
  - Appointed 柳林县委书记: ~2021 (succeeding 郝继平)
  - Source: Baidu Baike + thepaper.cn

县委副书记、县长: 燕明星
  - Born 1972.06, 山西临县人, 省委党校研究生
  - Previously: 柳林县委常委、常务副县长, 柳林县委副书记
  - Promoted to 县长: 2022
  
- 县委副书记、统战部长: 赵日政 (also known as 赵燕 in some sources)
  - Born 1969.05, 山西方山人, 省委党校大学
  - Previously: 柳林县委常委、组织部长, 文水县委常委、组织部长, 孝义市委常委、组织部长
  
  - 组织部长: 王卫国
    - Born 1977.12, 山西人, 大学学历
    - Previously: 柳林县副县长, 方山县委常委、组织部长
  
- 纪委书记: 薛茂荣
  - Previously: 吕梁市委组织部干部监督科长

- 副县长: 李喜平
  - Born 1978.05, 山西中阳人
  - Previously: 方山县政府副县长, 中阳县委副书记, 中阳县长

- 副县长: 赵志强 (兼公安局长)

Research limitations (2026-07-26):
- Some government website data may be stale
- Career timeline gaps for some deputy leaders
- Specific relationship evidence is inferred from organizational overlap

Artifact conventions:
- Build script: build_柳林县_data.py -> scripts/build/build_柳林县_data.py
- Database: data/database/柳林县_network.db
- GEXF: data/graph/柳林县_network.gexf
"""

from pathlib import Path
import sys
import sqlite3  # Direct import for process_tmp validation

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

STAGING_DIR = Path(__file__).parent
DB_PATH = STAGING_DIR / "柳林县_network.db"
GEXF_PATH = STAGING_DIR / "柳林县_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════════
# Persons
# ═══════════════════════════════════════════════════════════════════════════════

persons = [
    {
        "id": 1,
        "name": "杨月祥",
        "gender": "男",
        "birth": "1969.02",
        "birthplace": "山西省吕梁市方山县",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "柳林县委书记",
        "current_org": "中共柳林县委员会",
        "source": "https://www.thepaper.cn/newsDetail_forward_29067862",
    },
    {
        "id": 2,
        "name": "燕明星",
        "gender": "男",
        "birth": "1972.06",
        "birthplace": "山西省吕梁市临县",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "柳林县委副书记、县长",
        "current_org": "柳林县人民政府",
        "source": "https://www.thepaper.cn/newsDetail_forward_29067862",
    },
    {
        "id": 3,
        "name": "赵日政",
        "gender": "男",
        "birth": "1969.05",
        "birthplace": "山西省方山县",
        "education": "省委党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "柳林县委副书记、统战部长",
        "current_org": "中共柳林县委员会",
        "source": "百度百科",
    },
    {
        "id": 4,
        "name": "王卫国",
        "gender": "男",
        "birth": "1977.12",
        "birthplace": "山西省",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "柳林县委常委、组织部长",
        "current_org": "中共柳林县委员会",
        "source": "柳林县政府网站",
    },
    {
        "id": 5,
        "name": "薛茂荣",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "柳林县委常委、县纪委书记、县监委主任",
        "current_org": "中共柳林县纪律检查委员会",
        "source": "柳林县政府网站",
    },
    {
        "id": 6,
        "name": "李喜平",
        "gender": "男",
        "birth": "1978.05",
        "birthplace": "山西省",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "柳林县人民政府副县长",
        "current_org": "柳林县人民政府",
        "source": "柳林县政府网站",
    },
    {
        "id": 7,
        "name": "赵一政",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "柳林县人民政府副县长、县公安局局长",
        "current_org": "柳林县人民政府",
        "source": "news article",
    },
    {
        "id": 8,
        "name": "杨建军",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "方山县委书记 (predecessor as 柳林县长)",
        "current_org": "中共方山县委员会",
        "source": "thepaper.cn",
    },
    {
        "id": 9,
        "name": "郝继平",
        "gender": "男",
        "birth": "",
        "birthplace": "山西省",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吕梁市马列主义管理服务中心 / 市政协 (前柳林县委书记)",
        "current_org": "吕梁市政协",
        "source": "thepaper.cn",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共柳林县委员会",
        "type": "党委",
        "level": "县级",
        "location": "柳林县",
    },
    {
        "id": 2,
        "name": "柳林县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "柳林县",
    },
    {
        "id": 3,
        "name": "中共柳林县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "location": "柳林县",
    },
    {
        "id": 4,
        "name": "中共吕梁市委组织部",
        "type": "组织部",
        "level": "地市级",
        "location": "吕梁市",
    },
    {
        "id": 5,
        "name": "中共方山县委员会",
        "type": "党委",
        "level": "县级",
        "location": "方山县",
    },
    {
        "id": 6,
        "name": "方山县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "方山县",
    },
    {
        "id": 7,
        "name": "吕梁市政协",
        "type": "政协",
        "level": "地市级",
        "location": "吕梁市",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Positions
# ═══════════════════════════════════════════════════════════════════════════════

positions = [
    # 杨月祥 (id=1) - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2021-", "end_date": "", "rank": "正县级", "note": "现任柳林县委书记"},
    {"person_id": 1, "org_id": 5, "title": "县委副书记", "start_date": "", "end_date": "2021", "rank": "副县级", "note": "方山县委副书记"},
    {"person_id": 1, "org_id": 4, "title": "吕梁市委政法委副书记?", "start_date": "", "end_date": "", "rank": "正处级", "note": "履历细节待查"},
    {"person_id": 1, "org_id": 5, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "方山县副县长，早期经历"},

    # 燕明星 (position=2) - 县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2022-02", "end_date": "", "rank": "正县级", "note": "柳林县委副书记、县长"},
    {"person_id": 2, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "2022-02", "rank": "副县级", "note": "柳林县常务副县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "提拔为县长前曾任县委副书记"},

    # 赵日政 (position=3) - 副书记/统战部长
    {"person_id": 3, "org_id": 1, "title": "县委副书记、统战部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任，分管统战"},
    {"person_id": 3, "org_id": 1, "title": "县委常委、组织部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "前任柳林县委组织部长"},
    {"person_id": 3, "org_id": 1, "title": "县委常委、组织部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "文水县委常委、组织部长"},
    {"person_id": 3, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "孝义市副市长"},

    # 王卫国 (position=4) - 组织部长
    {"person_id": 4, "org_id": 1, "title": "县委常委、组织部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任组织部长"},
    {"person_id": 4, "org_id": 5, "title": "县委常委、组织部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "曾任方山县委组织部长"},

    # 薛茂荣 (position=5) - 纪委书记
    {"person_id": 5, "org_id": 3, "title": "县委常委、纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "柳林县纪委书记"},
    {"person_id": 5, "org_id": 4, "title": "干部监督科长/组织科长", "start_date": "", "end_date": "", "rank": "正科级", "note": "吕梁市委组织部"},

    # 李喜平 (position=6) - 副县长
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "柳林县副县长"},

    # 趙一政 (position=7) - 副县长/公安局长
    {"person_id": 7, "org_id": 2, "title": "副县长、公安局长", "start_date": "", "end_date": "", "rank": "副县级", "note": "柳林县公安局长"},

    # 杨建军 (position=8) - 前县长
    {"person_id": 8, "org_id": 2, "title": "县长", "start_date": "", "end_date": "2020", "rank": "正县级", "note": "前任柳林县长，后任方山县委书记"},
    {"person_id": 8, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "方山县委书记"},

    # 郝继平 (position=9) - 前县委书记
    {"person_id": 9, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "2021", "rank": "正县级", "note": "前任柳林县委书记"},
    {"person_id": 9, "org_id": 7, "title": "主席", "start_date": "", "end_date": "", "rank": "正县级", "note": "吕梁市政协"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "杨月祥(县委书记)与燕明星(县长)为柳林县现任党政正职",
        "overlap_org": "柳林县",
        "overlap_period": "2022-至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "班子共事",
        "context": "杨月祥与赵日政在柳林县委班子共事",
        "overlap_org": "中共柳林县委员会",
        "overlap_period": "2021-至今",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "班子共事",
        "context": "王卫国调任柳林组织部长后与杨月祥共事",
        "overlap_org": "中共柳林县委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "前后任",
        "context": "赵日政曾任柳林组织部长，王卫国接任组织部长",
        "overlap_org": "中共柳林县委组织部",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "前后任",
        "context": "杨建军由柳林县长提任方山县委书记，杨月祥接任柳林县委书记(是否同一系统)",
        "overlap_org": "柳林县",
        "overlap_period": "2021年前后",
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "前后任",
        "context": "郝继平是前任柳林县委书记，杨月祥接任",
        "overlap_org": "中共柳林县委员会",
        "overlap_period": "2021交接",
    },
    {
        "person_a": 8,
        "person_b": 2,
        "type": "前上级",
        "context": "杨建军原为柳林县长，燕明星后续任柳林县长",
        "overlap_org": "柳林县人民政府",
        "overlap_period": "前后任过渡",
    },
    {
        "person_a": 3,
        "person_b": 5,
        "type": "班子共事",
        "context": "赵日政与薛茂荣在柳林县委班子共事",
        "overlap_org": "中共柳林县委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "上下级",
        "context": "燕明星(县长)与李喜平(副县长)在政府班子共事",
        "overlap_org": "柳林县人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "上下级",
        "context": "燕明星(县长)与赵一政(副县长、公安局长)在政府班子共事",
        "overlap_org": "柳林县人民政府",
        "overlap_period": "至今",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="柳林县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )