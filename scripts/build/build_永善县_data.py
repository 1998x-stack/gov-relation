#!/usr/bin/env python3
"""Build 永善县 (Yongshan County) 领导班子工作关系网络.

云南省昭通市下辖县. 数据来源: 镇雄县调查交叉参考，百度百科.
调查日期: 2026-07-28.

已知人物:
  - 吴君尧: 前任永善县委书记（2024-04至2026-05），后调任镇雄县委书记
  - 当前县委书记（吴君尧之后）未知 —— 公开渠道未能获取
  - 当前县长未知 —— 公开渠道未能获取
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build

SLUG = "永善县"
TODAY = "2026-07-28"
PROVINCE = "云南省"
CITY = "昭通市"

STAGING = Path(__file__).resolve().parent

# -- Persons ---------------------------------------------------------------
# Note: 当前永善县委书记（接替吴君尧）和县长均未查到公开信息
persons = [
    # 核心人物1: 前任县委书记
    {
        "id": 1,
        "name": "吴君尧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "云南大关",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1994年8月",
        "current_post": "原永善县委书记（现任镇雄县委书记）",
        "current_org": "中共永善县委（原任）",
        "source": "https://baike.baidu.com/item/%E5%90%B4%E5%90%9B%E5%B0%A7",
    },
    # 核心人物——当前县委书记（待确认）
    {
        "id": 2,
        "name": "待确认（现任永善县委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记（接替吴君尧）",
        "current_org": "中共永善县委",
        "source": "",
    },
    # 核心人物——县长（待确认）
    {
        "id": 3,
        "name": "待确认（永善县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "永善县人民政府",
        "source": "",
    },
]

# -- Organizations -------------------------------------------------------
organizations = [
    {"id": 1, "name": "中共永善县委", "type": "党委", "level": "县级",
     "parent": "中共昭通市委", "location": "永善县"},
    {"id": 2, "name": "永善县人民政府", "type": "政府", "level": "县级",
     "parent": "昭通市人民政府", "location": "永善县"},
    {"id": 3, "name": "中共永善县纪律检查委员会", "type": "纪委", "level": "县级",
     "parent": "中共昭通市纪委", "location": "永善县"},
    {"id": 4, "name": "永善县人民代表大会常务委员会", "type": "人大", "level": "县级",
     "parent": "昭通市人大常委会", "location": "永善县"},
    {"id": 5, "name": "中国人民政治协商会议永善县委员会", "type": "政协", "level": "县级",
     "parent": "昭通市政协", "location": "永善县"},
]

# -- Positions -----------------------------------------------------------
positions = [
    # 吴君尧在永善县的任职
    {"person_id": 1, "org_id": 1, "title": "永善县委常委、政法委书记",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "早期在永善县委任职，具体起止时间未公开"},
    {"person_id": 1, "org_id": 1, "title": "永善县委书记",
     "start_date": "2024-04", "end_date": "2026-05", "rank": "正处级",
     "note": "从昭通市直部门转任永善县委书记，后调任镇雄县委书记"},
]

# -- Relationships -------------------------------------------------------
relationships = [
    # 吴君尧 → 接任者的前后任关系
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "吴君尧2026年5月调离后，新任县委书记接任",
        "overlap_org": "中共永善县委",
        "overlap_period": "2026-05（交接期）",
    },
]

# -- Build ---------------------------------------------------------------
if __name__ == "__main__":
    db_path = STAGING / f"{SLUG}_network.db"
    gexf_path = STAGING / f"{SLUG}_network.gexf"
    
    print(f"=== 构建 {SLUG} 领导班子工作关系网络 ===")
    print(f"日期: {TODAY}")
    print(f"人员: {len(persons)} (含2个待确认占位)")
    print(f"机构: {len(organizations)}")
    print(f"任职: {len(positions)}")
    print(f"关系: {len(relationships)}")
    print(f"DB:   {db_path}")
    print(f"GEXF: {gexf_path}")
    print()
    print("⚠ 警告: 永善县当前县委书记（继任者）和县长信息均未从公开渠道获取。")
    print("   节点2（县委书记待确认）和节点3（县长待确认）为占位符。")
    print()

    run_build(
        slug="永善县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )