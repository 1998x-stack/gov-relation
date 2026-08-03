#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 轮台县 (Luntai County) leadership network.

轮台县 is a county under 巴音郭楞蒙古自治州 (Bayingolin Mongol Autonomous
Prefecture), Xinjiang Uyghur Autonomous Region.

Targets: 县委书记 (Party Secretary) & 县长 (County Mayor)
"""
import os
import sys
import sqlite3
from pathlib import Path

_script_path = Path(__file__).resolve()
STAGING_DIR = _script_path.parent
_REPO = _script_path.parents[2] if _script_path.parents[2].name == 'gov-relation' else _script_path.parents[3]
sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build

DB_PATH = STAGING_DIR / "轮台县_network.db"
GEXF_PATH = STAGING_DIR / "轮台县_network.gexf"

# ── DATA ──

persons = [
    # ════════════════════════════════════════════════
    # Top Leaders
    # ════════════════════════════════════════════════
    # ── 1. Party Secretary (县委书记) ──
    {
        "id": 1, "name": "肖旭",
        "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "轮台县委书记",
        "current_org": "中共轮台县委员会",
        "source": "https://mp.weixin.qq.com/s/DhWvsAikAkN1Gv-YQyOdPg",
    },
    # ── 2. County Mayor (县长) ──
    {
        "id": 2, "name": "艾尼瓦尔·尼亚孜",
        "gender": "男", "ethnicity": "维吾尔族",
        "birth": "1976-09", "birthplace": "新疆",
        "education": "大学学历，管理学学士",
        "party_join": "", "work_start": "",
        "current_post": "轮台县委副书记、县长",
        "current_org": "轮台县人民政府",
        "source": "https://www.xjlt.gov.cn/xjltx/c110364/202112/6d29adf096134ae884fdf4cac03f4e2b.shtml",
    },
    # ════════════════════════════════════════════════
    # Government Deputy Leaders (副县长)
    # ════════════════════════════════════════════════
    # ── 3. Executive Deputy County Mayor (常务副县长) ──
    {
        "id": 3, "name": "陈志成",
        "gender": "男", "ethnicity": "汉族",
        "birth": "1975-07", "birthplace": "",
        "education": "大专学历",
        "party_join": "", "work_start": "",
        "current_post": "轮台县委常委、常务副县长",
        "current_org": "轮台县人民政府",
        "source": "https://www.xjlt.gov.cn/xjltx/c110364/202112/04b8a870c09e4c618bc492e8a54f4450.shtml",
    },
    # ── 4. Standing Cmte, Deputy County Mayor (挂职) ──
    {
        "id": 4, "name": "刘元兵",
        "gender": "男", "ethnicity": "汉族",
        "birth": "1973-07", "birthplace": "湖北潜江",
        "education": "研究生学历，管理学硕士",
        "party_join": "", "work_start": "",
        "current_post": "轮台县委常委、副县长（挂职）",
        "current_org": "轮台县人民政府",
        "source": "https://www.xjlt.gov.cn/xjltx/c110364/202112/94a8582a516340e5214c3aad195d92bb2.shtml",
    },
    # ── 5. Deputy County Mayor / PSB Chief ──
    {
        "id": 5, "name": "王勇",
        "gender": "男", "ethnicity": "汉族",
        "birth": "1981-08", "birthplace": "山东曹县",
        "education": "大学学历",
        "party_join": "", "work_start": "",
        "current_post": "轮台县副县长、县公安局局长",
        "current_org": "轮台县人民政府",
        "source": "https://www.xjlt.gov.cn/xjltx/c110364/202509/6a6a769abe8f44fc8fe02db808ff21f8.shtml",
    },
    # ── 6. Deputy County Mayor ──
    {
        "id": 6, "name": "吐尔洪·库尔班",
        "gender": "男", "ethnicity": "维吾尔族",
        "birth": "1974-02", "birthplace": "新疆库车",
        "education": "大学学历",
        "party_join": "", "work_start": "",
        "current_post": "轮台县副县长",
        "current_org": "轮台县人民政府",
        "source": "https://www.xjlt.gov.cn/xjltx/c110364/202112/492d0d9d0cc54286a011a3d6631a6b200.shtml",
    },
    # ── 7. Standing Cmte & Deputy County Mayor (挂职) ──
    {
        "id": 7, "name": "蔡献峰",
        "gender": "男", "ethnicity": "汉族",
        "birth": "1976-07", "birthplace": "河南洛阳",
        "education": "大专学历",
        "party_join": "", "work_start": "",
        "current_post": "轮台县委常委、副县长（挂职）",
        "current_org": "轮台县人民政府",
        "source": "https://www.xjlt.gov.cn/xjltx/c110364/202112/fade327fe2216ae917c4856309ef0176.shtml",
    },
    # ── 8. Deputy County Mayor ──
    {
        "id": 8, "name": "陈长彬",
        "gender": "男", "ethnicity": "汉族",
        "birth": "1990-08", "birthplace": "山东东阿",
        "education": "大学本科学历",
        "party_join": "2017-09", "work_start": "2012-12",
        "current_post": "轮台县副县长",
        "current_org": "轮台县人民政府",
        "source": "https://www.xjlt.gov.cn/xjltx/c110364/202205/43ab8a61619d4020b1069b223d10f9e23.shtml",
    },
    # ── 9. Deputy County Mayor ──
    {
        "id": 9, "name": "李大军",
        "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "大学学历",
        "party_join": "", "work_start": "",
        "current_post": "轮台县副县长",
        "current_org": "轮台县人民政府",
        "source": "https://www.xjlt.gov.cn/xjltx/c110364/202112/d4c35499dc2d4e70b911f4a0d53baa5d.shtml",
    },
    # ── 10. Standing Cmte, Deputy County Mayor ──
    {
        "id": 10, "name": "段成伟",
        "gender": "男", "ethnicity": "汉族",
        "birth": "1983-08", "birthplace": "河北泊头",
        "education": "在职研究生学历，管理学/法学学士",
        "party_join": "", "work_start": "",
        "current_post": "轮台县委常委、副县长、轮台工业园区管委会副主任",
        "current_org": "轮台县人民政府",
        "source": "https://www.xjlt.gov.cn/xjltx/c110364/202112/460cf73d71c849418e012746b78b0fe60d.shtml",
    },
]

organizations = [
    {"id": 1, "name": "中共轮台县委员会", "type": "党委", "level": "县级", "parent": "中共巴音郭楞蒙古自治州委员会", "location": "轮台镇"},
    {"id": 2, "name": "轮台县人民政府", "type": "政府", "level": "县级", "parent": "巴音郭楞蒙古自治州人民政府", "location": "轮台镇"},
    {"id": 3, "name": "轮台县公安局", "type": "政府", "level": "县级", "parent": "轮台县人民政府", "location": "轮台镇"},
    {"id": 4, "name": "轮台工业园区管委会", "type": "开发区", "level": "县级", "parent": "轮台县人民政府", "location": "轮台县"},
    {"id": 5, "name": "轮台县人大常委会", "type": "人大", "level": "县级", "parent": "巴音郭楞蒙古自治州人大常委会", "location": "轮台镇"},
    {"id": 6, "name": "轮台县政协", "type": "政协", "level": "县级", "parent": "巴音郭楞蒙古自治州政协", "location": "轮台镇"},
]

positions = [
    # ── 肖旭 (Party Secretary) ──
    {"person_id": 1, "org_id": 1, "title": "轮台县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "经轮台县十三届党委常委会(2026-07-29)确认任职"},
    # ── 艾尼瓦尔·尼亚孜 (County Mayor) ──
    {"person_id": 2, "org_id": 2, "title": "轮台县委副书记、县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县人民政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "轮台县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 陈志成 (Exec Deputy) ──
    {"person_id": 3, "org_id": 2, "title": "轮台县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责县人民政府常务工作"},
    {"person_id": 3, "org_id": 1, "title": "轮台县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 刘元兵 (Deputy, temp) ──
    {"person_id": 4, "org_id": 2, "title": "轮台县委常委、副县长（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "湖北潜江人，管理学硕士，高级政工师"},
    {"person_id": 4, "org_id": 1, "title": "轮台县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 王勇 (Deputy, PSB) ──
    {"person_id": 5, "org_id": 2, "title": "轮台副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼县公安局局长"},
    {"person_id": 5, "org_id": 3, "title": "轮台县公安局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 吐尔洪·库尔班 (Deputy) ──
    {"person_id": 6, "org_id": 2, "title": "轮台县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "新疆库车人，兼任县委政法委副书记"},
    # ── 蔡献峰 (Deputy, temp) ──
    {"person_id": 7, "org_id": 2, "title": "轮台县委常委、副县长（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "河南洛阳人"},
    {"person_id": 7, "org_id": 1, "title": "轮台县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 陈长彬 (Deputy) ──
    {"person_id": 8, "org_id": 2, "title": "轮台县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "山东东阿人，2012.12参加工作，2017.09入党"},
    # ── 李满军 (Deputy) ──
    {"person_id": 9, "org_id": 2, "title": "轮台县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 段成伟 (Deputy) ──
    {"person_id": 10, "org_id": 2, "title": "轮台县委常委、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "河北泊头人，兼轮台工业园区管委会副主任"},
    {"person_id": 10, "org_id": 1, "title": "轮台县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 4, "title": "轮台工业园区管委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

relationships = [
    # ── 肖旭 ↔ 艾尼瓦尔·尼亚孜 (Party Secretary ↔ County Mayor) ──
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "党政正职搭档（县委书记+县长）", "overlap_org": "中共轮台县委员会", "overlap_period": "2025/2026至今"},
    # ── 肖旭 ↔ 县委常委 each ──
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "党委书记-常务副县长", "overlap_org": "中共轮台县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "党委书记-县委常委（挂职）", "overlap_org": "中共轮台县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "党委书记-县委常委（挂职）", "overlap_org": "中共轮台县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "党委书记-县委常委/园区副主任", "overlap_org": "中共轮台县委员会", "overlap_period": "至今"},
    # ── 艾尼瓦尔·尼亚孜 ↔ 各副县长 ──
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长-常务副县长", "overlap_org": "轮台县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长-副县长（挂职）", "overlap_org": "轮台县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长-副县长/公安局长", "overlap_org": "轮台县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长-副县长", "overlap_org": "轮台县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长-副县长（挂职）", "overlap_org": "轮台县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长-副县长", "overlap_org": "轮台县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长-副县长", "overlap_org": "轮台县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长-副县长", "overlap_org": "轮台县人民政府", "overlap_period": "至今"},
    # ── 挂职group (刘元兵, 蔡献峰) ──
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "同为挂职副县长", "overlap_org": "轮台县人民政府", "overlap_period": "至今"},
    # ── 山东籍 (王勇、陈长彬) ──
    {"person_a": 5, "person_b": 8, "type": "overlap", "context": "同乡（山东籍）", "overlap_org": "轮台县人民政府", "overlap_period": "至今"},
]


if __name__ == "__main__":
    run_build(
        slug="轮台县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Build complete.")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:    {len(organizations)}")
    print(f"  Pos:     {len(positions)}")
    print(f"  Rel:     {len(relationships)}")