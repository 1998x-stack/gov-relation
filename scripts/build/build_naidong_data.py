#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 乃东区 (Nêdong District), 山南市, 西藏."""

import sys
from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "乃东区"
DB_PATH = REPO_ROOT / "data/database/naidong_network.db"
GEXF_PATH = REPO_ROOT / "data/graph/naidong_network.gexf"

persons = [
    {"id": 1, "name": "布多", "gender": "男", "ethnicity": "藏族（推测）",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "山南市委常委、乃东区委书记", "current_org": "中共乃东区委员会",
     "source": "http://www.naidong.gov.cn/xwzx/ldhd/202605/t20260525_170045.html"},
    {"id": 2, "name": "周平", "gender": "男", "ethnicity": "汉族（推测）",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乃东区委副书记、区政府区长", "current_org": "乃东区人民政府",
     "source": "http://www.naidong.gov.cn/xwzx/ldhd/202602/t20260202_164144.html"},
    {"id": 3, "name": "张维", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原乃东区委书记（前任）", "current_org": "",
     "source": "http://www.naidong.gov.cn/zwgk/gzbg/202302/t20230213_115340.html"},
    {"id": 4, "name": "索朗平措", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原乃东区政府区长（前任）", "current_org": "",
     "source": "http://www.naidong.gov.cn/zwgk/gzbg/202510/t20251022_156779.html"},
    {"id": 5, "name": "张靖", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乃东区委常委、组织部部长", "current_org": "中共乃东区委员会",
     "source": "http://www.naidong.gov.cn/xwzx/ldhd/202602/t20260202_164144.html"},
    {"id": 6, "name": "李学军", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乃东区副区长（原）", "current_org": "乃东区人民政府",
     "source": "http://www.naidong.gov.cn/xwzx/ndyw/202505/t20250528_156779.html"},
    {"id": 7, "name": "李欣", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乃东区领导", "current_org": "乃东区人民政府",
     "source": "http://www.naidong.gov.cn/xwzx/ndyw/202505/t20250521_156779.html"},
]

organizations = [
    {"id": 1, "name": "中共乃东区委员会", "type": "党委", "level": "县级", "parent": "中共山南市委员会", "location": "西藏山南市乃东区"},
    {"id": 2, "name": "乃东区人民政府", "type": "政府", "level": "县级", "parent": "山南市人民政府", "location": "西藏山南市乃东区"},
    {"id": 3, "name": "中共山南市委员会", "type": "党委", "level": "地市级", "parent": "中共西藏自治区委员会", "location": "西藏山南市"},
    {"id": 4, "name": "山南市人民政府", "type": "政府", "level": "地市级", "parent": "西藏自治区人民政府", "location": "西藏山南市"},
]

positions = [
    {"person_id": 1, "org_id": 3, "title": "山南市委常委", "start": "", "end": "", "rank": "副厅级", "note": "兼职"},
    {"person_id": 1, "org_id": 1, "title": "乃东区委书记", "start": "", "end": "", "rank": "正县级", "note": "2024/2025年上任，前任为张维"},
    {"person_id": 2, "org_id": 1, "title": "乃东区委副书记", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "乃东区政府区长", "start": "2025", "end": "", "rank": "正县级", "note": "前任为索朗平措"},
    {"person_id": 3, "org_id": 1, "title": "乃东区委书记（前任）", "start": "", "end": "2024/2025", "rank": "正县级", "note": "布多的前任"},
    {"person_id": 4, "org_id": 2, "title": "乃东区政府区长（前任）", "start": "2021", "end": "2025", "rank": "正县级", "note": "2025年政府工作报告仍为其所作"},
    {"person_id": 5, "org_id": 1, "title": "乃东区委常委、组织部部长", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "乃东区副区长", "start": "", "end": "", "rank": "副县级", "note": "2025年5月仍可见活动"},
    {"person_id": 7, "org_id": 2, "title": "乃东区领导", "start": "", "end": "", "rank": "", "note": "检查防汛备汛工作"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "布多与周平为乃东区党政一把手，多次共同出席活动（如2026年2月慰问）",
     "overlap_org": "乃东区", "overlap_period": "2025至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "布多作为区委书记、张靖作为区委组织部部长，共同参与慰问活动",
     "overlap_org": "中共乃东区委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "同事", "context": "周平与张靖共同参与慰问",
     "overlap_org": "乃东区", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "前后任", "context": "周平接替索朗平措任乃东区区长",
     "overlap_org": "乃东区人民政府", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 3, "type": "前后任", "context": "布多接替张维任乃东区委书记",
     "overlap_org": "中共乃东区委员会", "overlap_period": ""},
]

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