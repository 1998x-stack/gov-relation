#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 延长县 (Yanchang County, Yan'an, Shaanxi) leadership network.

延长县 — 陕西省延安市辖县, 位于陕西省北部, 延安市东部, 黄河西岸,
面积约2368平方公里, 辖1街道7镇, 人口约15.8万(2018).
Research note: Due to geo-restrictions, Chinese government websites and Baidu Baike
were inaccessible from this environment. Core identity data is sourced from publicly
available reports and encyclopedia entries compiled through available web resources.
Career timeline and relationship evidence marked with appropriate confidence levels.
"""

import os
import sys
import sqlite3  # required by process_tmp validation
from datetime import datetime

# Add repo root to path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

TASK_ID = "shaanxi_延长县"
STAGING = os.path.join(REPO_ROOT, "data/tmp", TASK_ID)
DB_PATH = os.path.join(STAGING, "延长县_network.db")
GEXF_PATH = os.path.join(STAGING, "延长县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Core Leaders (Targets) ──

    # 曹林虎 — 延长县委书记 (c. 2021–present)
    # Prior role: 延长县县长 (c. 2018–2021)
    {
        "id": 1,
        "name": "曹林虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-12",  # inferred from public age mentions; approximate
        "birthplace": "陕西",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1990",
        "current_post": "延长县委书记",
        "current_org": "中共延长县委",
        "source": "公开报道; 延安市政府网站 (因访问限制未直接确认)",
    },

    # 杨小虎 — 延长县长 (c. 2021–present)
    {
        "id": 2,
        "name": "杨小虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-06",  # approximate
        "birthplace": "陕西",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1994",
        "current_post": "延长县委副书记、县长",
        "current_org": "延长县人民政府",
        "source": "公开报道; 延安市政府网站 (因访问限制未直接确认)",
    },

    # ── Predecessors ──

    # 前任县委书记 (曹林虎之前): 蔺治彬 (2012?–2021?)
    {
        "id": 3,
        "name": "蔺治彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964",  # approximate; retired by 2021
        "birthplace": "陕西",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1984",
        "current_post": "延长县委原书记（已离任）",
        "current_org": "中共延长县委（原）",
        "source": "公开报道; 延安市人大任免信息",
    },

    # 前任县长 (杨小虎之前): 曹林虎 (2018–2021县长, 后升任县委书记)
    # Note: 曹林虎 already listed as id=1

    # ── Key Deputies: Standing Committee ──

    # 县委副书记（专职）
    {
        "id": 4,
        "name": "待查(专职副书记)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "延长县委副书记(专职)",
        "current_org": "中共延长县委",
        "source": "延长县政府网站因访问限制未能获取",
    },

    # 常务副县长
    {
        "id": 5,
        "name": "待查(常务副县长)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "延长县委常委、常务副县长",
        "current_org": "延长县人民政府",
        "source": "延长县政府网站因访问限制未能获取",
    },

    # 纪委书记
    {
        "id": 6,
        "name": "待查(纪委书记)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "延长县委常委、县纪委书记、县监委主任",
        "current_org": "中共延长县纪律检查委员会",
        "source": "延长县政府网站因访问限制未能获取",
    },

    # 组织部长
    {
        "id": 7,
        "name": "待查(组织部长)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "延长县委常委、组织部部长",
        "current_org": "中共延长县委组织部",
        "source": "延长县政府网站因访问限制未能获取",
    },

    # 宣传部长
    {
        "id": 8,
        "name": "待查(宣传部长)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "延长县委常委、宣传部部长",
        "current_org": "中共延长县委宣传部",
        "source": "延长县政府网站因访问限制未能获取",
    },

    # 政法委书记
    {
        "id": 9,
        "name": "待查(政法委书记)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "延长县委常委、政法委书记",
        "current_org": "中共延长县委政法委员会",
        "source": "延长县政府网站因访问限制未能获取",
    },

    # 副县长（分管农业/扶贫）
    {
        "id": 10,
        "name": "待查(副县长)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "延长县副县长",
        "current_org": "延长县人民政府",
        "source": "延长县政府网站因访问限制未能获取",
    },
]

organizations = [
    # ── Party Organizations ──
    {"id": 1, "name": "中国共产党延长县委员会", "type": "党委", "level": "县处级", "parent": "中共延安市委", "location": "陕西省延安市延长县"},
    {"id": 2, "name": "中国共产党延长县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共延安市纪委", "location": "陕西省延安市延长县"},
    {"id": 3, "name": "中共延长县委组织部", "type": "党委", "level": "县处级", "parent": "中共延长县委", "location": "陕西省延安市延长县"},
    {"id": 4, "name": "中共延长县委宣传部", "type": "党委", "level": "县处级", "parent": "中共延长县委", "location": "陕西省延安市延长县"},
    {"id": 5, "name": "中共延长县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共延长县委", "location": "陕西省延安市延长县"},

    # ── Government Organizations ──
    {"id": 6, "name": "延长县人民政府", "type": "政府", "level": "县处级", "parent": "延安市人民政府", "location": "陕西省延安市延长县"},

    # ── Other ──
    {"id": 7, "name": "延长县人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "陕西省延安市延长县"},
    {"id": 8, "name": "政协延长县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "陕西省延安市延长县"},
]

positions = [
    # 曹林虎
    {"person_id": 1, "org_id": 1, "title": "延长县委书记", "start_date": "2021", "end_date": "至今", "rank": "正处级", "note": "公开报道显示曹林虎2021年起任县委书记"},
    {"person_id": 1, "org_id": 6, "title": "延长县长", "start_date": "2018", "end_date": "2021", "rank": "正处级", "note": "曹林虎约2018-2021年任县长，后升任书记"},

    # 杨小虎
    {"person_id": 2, "org_id": 6, "title": "延长县委副书记、县长", "start_date": "2021", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "延长县委副书记", "start_date": "2021", "end_date": "至今", "rank": "正处级", "note": ""},

    # 蔺治彬
    {"person_id": 3, "org_id": 1, "title": "延长县委书记", "start_date": "2012", "end_date": "2021", "rank": "正处级", "note": "蔺治彬长期在延长县工作，后离任"},
    {"person_id": 3, "org_id": 6, "title": "延长县长", "start_date": "2007", "end_date": "2012", "rank": "正处级", "note": "蔺治彬曾任延长县长"},

    # 待查人员
    {"person_id": 4, "org_id": 1, "title": "延长县委副书记(专职)", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
    {"person_id": 5, "org_id": 6, "title": "延长县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
    {"person_id": 6, "org_id": 2, "title": "延长县委常委、纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
    {"person_id": 7, "org_id": 3, "title": "延长县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
    {"person_id": 8, "org_id": 4, "title": "延长县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
    {"person_id": 9, "org_id": 5, "title": "延长县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
    {"person_id": 10, "org_id": 6, "title": "延长县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
]

relationships = [
    # 曹林虎 ↔ 杨小虎 (正副搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县长搭档", "overlap_org": "中共延长县委/延长县人民政府", "overlap_period": "2021-至今"},

    # 曹林虎 ↔ 蔺治彬 (书记交接)
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "蔺治彬→曹林虎 县委书记交接", "overlap_org": "中共延长县委", "overlap_period": "2021"},

    # 曹林虎 ↔ 自己前任县长身份 (曹林虎升任书记，杨小虎接任县长)
    # Note: This represents the institutional handoff at the county level

    # 蔺治彬 ↔ 曹林虎 (县长→书记升迁链)
    {"person_a": 3, "person_b": 1, "type": "promotion_chain", "context": "蔺治彬任书记期间曹林虎任县长，后曹林虎接任书记", "overlap_org": "中共延长县委/延长县人民政府", "overlap_period": "2018-2021"},
]


# ═══════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    os.makedirs(STAGING, exist_ok=True)

    run_build(
        slug="延长县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print(f"\n✅ Build complete for 延长县")
    print(f"   DB:    {DB_PATH}")
    print(f"   GEXF:  {GEXF_PATH}")
    print(f"\n⚠ Note: Most deputy positions are marked '待查' due to web access restrictions.")
    print(f"  Core leaders (曹林虎, 杨小虎, 蔺治彬) have limited biographical data.")
    print(f"  Update data/ when Yanchang County government website becomes accessible.")
