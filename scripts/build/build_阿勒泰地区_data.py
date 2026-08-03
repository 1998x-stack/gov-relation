#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 阿勒泰地区 (Altay Prefecture), 新疆."""
import sqlite3
import sys
from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "阿勒泰地区"
DB_PATH = SCRIPT_DIR / "阿勒泰地区_network.db"
GEXF_PATH = SCRIPT_DIR / "阿勒泰地区_network.gexf"

# ── DATA ────────────────────────────────────────────────────────────────────

persons = [
    # ── Top leaders ──
    {"id": 1, "name": "谢少迪", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-04", "birthplace": "广东省郁南县",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "阿勒泰地委书记", "current_org": "中共阿勒泰地区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%98%BF%E5%8B%92%E6%B3%B0%E5%9C%B0%E5%8C%BA"},
    {"id": 2, "name": "木合塔尔·卡里木别克", "gender": "男", "ethnicity": "哈萨克族",
     "birth": "1974-11", "birthplace": "新疆维吾尔自治区塔城市",
     "education": "中央党校研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "阿勒泰地委副书记、地区行署专员", "current_org": "阿勒泰地区行政公署",
     "source": "https://www.xjalt.gov.cn/ ; https://zh.wikipedia.org/wiki/%E9%98%BF%E5%8B%92%E6%B3%B0%E5%9C%B0%E5%8C%BA"},

    # ── Other four-bureau leaders ──
    {"id": 3, "name": "赛力克·哈布肯", "gender": "男", "ethnicity": "哈萨克族",
     "birth": "1967-07", "birthplace": "新疆维吾尔自治区布尔津县",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "伊犁州人大常委会阿勒泰地区工委主任", "current_org": "伊犁州人大常委会阿勒泰地区工作委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%98%BF%E5%8B%92%E6%B3%B0%E5%9C%B0%E5%8C%BA"},
    {"id": 4, "name": "赛力克·马哈提", "gender": "男", "ethnicity": "哈萨克族",
     "birth": "1968-04", "birthplace": "新疆维吾尔自治区特克斯县",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "伊犁州政协阿勒泰地区工委主任", "current_org": "伊犁州政协阿勒泰地区工作委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%98%BF%E5%8B%92%E6%B3%B0%E5%9C%B0%E5%8C%BA"},

    # ── Predecessors ──
    {"id": 5, "name": "杰恩斯·哈德斯", "gender": "男", "ethnicity": "哈萨克族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "原阿勒泰地区行署专员（前任）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/%E9%98%BF%E5%8B%92%E6%B3%B0%E5%9C%B0%E5%8C%BA"},

    # ── Deputy leaders and important officials ──
    {"id": 6, "name": "阿勒泰地委副书记（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "阿勒泰地委副书记（待查）", "current_org": "中共阿勒泰地区委员会",
     "source": ""},
    {"id": 7, "name": "阿勒泰地委委员（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "阿勒泰地委委员（待查）", "current_org": "中共阿勒泰地区委员会",
     "source": ""},
]

organizations = [
    {"id": 1, "name": "中共阿勒泰地区委员会", "type": "党委", "level": "地市级",
     "parent": "中共新疆维吾尔自治区委员会", "location": "新疆维吾尔自治区阿勒泰地区阿勒泰市"},
    {"id": 2, "name": "阿勒泰地区行政公署", "type": "政府", "level": "地市级",
     "parent": "新疆维吾尔自治区人民政府", "location": "新疆维吾尔自治区阿勒泰地区阿勒泰市"},
    {"id": 3, "name": "伊犁州人大常委会阿勒泰地区工作委员会", "type": "人大", "level": "地市级",
     "parent": "伊犁哈萨克自治州人大常委会", "location": "新疆维吾尔自治区阿勒泰地区阿勒泰市"},
    {"id": 4, "name": "伊犁州政协阿勒泰地区工作委员会", "type": "政协", "level": "地市级",
     "parent": "伊犁哈萨克自治州政协", "location": "新疆维吾尔自治区阿勒泰地区阿勒泰市"},
    {"id": 5, "name": "中共伊犁哈萨克自治州委员会", "type": "党委", "level": "副省级",
     "parent": "中共新疆维吾尔自治区委员会", "location": "新疆维吾尔自治区伊犁哈萨克自治州伊宁市"},
    {"id": 6, "name": "伊犁哈萨克自治州人民政府", "type": "政府", "level": "副省级",
     "parent": "新疆维吾尔自治区人民政府", "location": "新疆维吾尔自治区伊犁哈萨克自治州伊宁市"},
]

positions = [
    # 谢少迪 (1)
    {"person_id": 1, "org_id": 1, "title": "阿勒泰地委书记", "start_date": "2023-01", "end_date": "",
     "rank": "正厅级", "note": "2023年1月任现职"},

    # 木合塔尔·卡里木别克 (2)
    {"person_id": 2, "org_id": 1, "title": "阿勒泰地委副书记", "start_date": "2026-05", "end_date": "",
     "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "阿勒泰地区行署专员", "start_date": "2026-05", "end_date": "",
     "rank": "正厅级", "note": "2026年5月任现职"},

    # 赛力克·哈布肯 (3)
    {"person_id": 3, "org_id": 3, "title": "伊犁州人大常委会阿勒泰地区工委主任", "start_date": "2024-12", "end_date": "",
     "rank": "正厅级", "note": "2024年12月任现职"},

    # 赛力克·马哈提 (4)
    {"person_id": 4, "org_id": 4, "title": "伊犁州政协阿勒泰地区工委主任", "start_date": "2024-12", "end_date": "",
     "rank": "正厅级", "note": "2024年12月任现职"},

    # 杰恩斯·哈德斯 (5) - 前任专员
    {"person_id": 5, "org_id": 2, "title": "阿勒泰地区行署专员", "start_date": "2021-04", "end_date": "2026-05",
     "rank": "正厅级", "note": "前任专员，2026年5月卸任"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "谢少迪（地委书记）与木合塔尔·卡里木别克（行署专员）为阿勒泰地区党政一把手",
     "overlap_org": "阿勒泰地区", "overlap_period": "2026-05至今"},
    {"person_a": 2, "person_b": 5, "type": "前后任",
     "context": "木合塔尔·卡里木别克接替杰恩斯·哈德斯任阿勒泰地区行署专员",
     "overlap_org": "阿勒泰地区行政公署", "overlap_period": "2026-05"},
    {"person_a": 1, "person_b": 3, "type": "同僚",
     "context": "谢少迪（地委书记）与赛力克·哈布肯（人大工委主任）在阿勒泰领导班子中共事",
     "overlap_org": "阿勒泰地区", "overlap_period": "2024-12至今"},
    {"person_a": 1, "person_b": 4, "type": "同僚",
     "context": "谢少迪（地委书记）与赛力克·马哈提（政协工委主任）在阿勒泰领导班子中共事",
     "overlap_org": "阿勒泰地区", "overlap_period": "2024-12至今"},
    {"person_a": 2, "person_b": 3, "type": "同僚",
     "context": "木合塔尔·卡里木别克（专员）与赛力克·哈布肯（人大工委主任）在阿勒泰领导班子中共事",
     "overlap_org": "阿勒泰地区", "overlap_period": "2024-12至今"},
    {"person_a": 2, "person_b": 4, "type": "同僚",
     "context": "木合塔尔·卡里木别克（专员）与赛力克·马哈提（政协工委主任）在阿勒泰领导班子中共事",
     "overlap_org": "阿勒泰地区", "overlap_period": "2024-12至今"},
]

# ── BUILD ────────────────────────────────────────────────────────────────────
run_build(
    slug=SLUG,
    persons=persons,
    organizations=organizations,
    positions=positions,
    relationships=relationships,
    db_path=DB_PATH,
    gexf_path=GEXF_PATH,
    overwrite=True,
)

print(f"\nDone! DB: {DB_PATH}  GEXF: {GEXF_PATH}")