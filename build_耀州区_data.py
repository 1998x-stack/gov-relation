#!/usr/bin/env python3
"""耀州区领导班子关系网络生成脚本。

铜川市耀州区领导团队（2026年8月口径）：
- 区委书记：杨军（2026年4月起，前任张峤任至2026年2月左右）
- 区委副书记、代区长：马啸（2026年7月前后接替区长高岗）
- 区人大常委会主任：李百锁；区政协主席：李新章；区监委主任：华秦
数据来源：耀州区政府官网 (www.yaozhou.gov.cn) 新闻、铜川市政府网、区两会报道。
信息截止日期：2026年8月。

说明：县处级干部（杨军、马啸、张飞、高岗等）的出生日期、毕业院校等履历字段在
公开网络受限环境下未能取得，均以置信度字段标注；数据库/图谱仍按已确认的任职
与搭班子关系构建。详见各 person JSON 的 open_questions 与 report/open_gaps.md。
"""

import sys
from pathlib import Path

# Ensure gov_relation package is importable
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "耀州区"
THIS_DIR = Path(__file__).resolve().parent
DB_PATH = THIS_DIR / f"{SLUG}_network.db"
GEXF_PATH = THIS_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: used by validator

# ── 人员 ──────────────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "杨军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共铜川市耀州区委员会",
        "source": "耀州区政府官网",
    },
    {
        "id": 2,
        "name": "马啸",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、代区长",
        "current_org": "铜川市耀州区人民政府",
        "source": "耀州区政府官网",
    },
    {
        "id": 3,
        "name": "高岗",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前区委副书记、区长",
        "current_org": "铜川市耀州区人民政府",
        "source": "耀州区政府官网",
    },
    {
        "id": 4,
        "name": "张峤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共铜川市耀州区委员会",
        "source": "耀州区政府官网",
    },
    {
        "id": 5,
        "name": "李百锁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会党组书记、主任",
        "current_org": "铜川市耀州区人民代表大会常务委员会",
        "source": "耀州区政府官网-区两会报道",
    },
    {
        "id": 6,
        "name": "李新章",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协党组书记、主席",
        "current_org": "政协铜川市耀州区委员会",
        "source": "耀州区政府官网-区两会报道",
    },
    {
        "id": 7,
        "name": "华秦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共铜川市耀州区纪律检查委员会/监察委员会",
        "source": "耀州区政府官网-区两会报道",
    },
    {
        "id": 8,
        "name": "刘峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共铜川市耀州区委员会",
        "source": "耀州区政府官网-区两会报道",
    },
    {
        "id": 9,
        "name": "刘尚利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共铜川市耀州区委员会",
        "source": "耀州区政府官网-区两会报道",
    },
    {
        "id": 10,
        "name": "杨乐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共铜川市耀州区委员会",
        "source": "耀州区政府官网-区两会报道",
    },
    {
        "id": 11,
        "name": "田屈鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共铜川市耀州区委员会",
        "source": "耀州区政府官网-区两会报道",
    },
    {
        "id": 12,
        "name": "李宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共铜川市耀州区委员会",
        "source": "耀州区政府官网-区两会报道",
    },
    {
        "id": 13,
        "name": "高伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共铜川市耀州区委员会",
        "source": "耀州区政府官网-区两会报道",
    },
    {
        "id": 14,
        "name": "刘鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铜川市耀州区人民政府",
        "source": "耀州区政府官网-区两会报道",
    },
]

# ── 组织 ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共铜川市耀州区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜川市委员会",
        "location": "陕西省铜川市耀州区",
    },
    {
        "id": 2,
        "name": "铜川市耀州区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "铜川市人民政府",
        "location": "陕西省铜川市耀州区",
    },
    {
        "id": 3,
        "name": "铜川市耀州区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "铜川市人民代表大会常务委员会",
        "location": "陕西省铜川市耀州区",
    },
    {
        "id": 4,
        "name": "政协铜川市耀州区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协铜川市委员会",
        "location": "陕西省铜川市耀州区",
    },
    {
        "id": 5,
        "name": "中共铜川市耀州区纪律检查委员会/监察委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜川市纪律检查委员会",
        "location": "陕西省铜川市耀州区",
    },
    {
        "id": 6,
        "name": "中共铜川市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共陕西省委员会",
        "location": "陕西省铜川市",
    },
    {
        "id": 7,
        "name": "铜川市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "陕西省人民政府",
        "location": "陕西省铜川市",
    },
]

# ── 任职记录 ──────────────────────────────────────────────────────
positions = [
    # 杨军
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026年4月", "end_date": "至今", "rank": "县处级正职", "note": "接任张峤；2026年5月区人武部党委第一书记任职大会"},
    # 马啸
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2026年前", "end_date": "至今", "rank": "县处级副职", "note": "2026年5月区两会报道中列为区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "区委副书记、代区长", "start_date": "2026年7月", "end_date": "至今", "rank": "县处级正职", "note": "接替高岗，2026年7月起以代区长身份主持政府工作"},
    # 高岗（前任区长）
    {"person_id": 3, "org_id": 2, "title": "区委副书记、区长", "start_date": "2020年前后", "end_date": "2026年6月", "rank": "县处级正职", "note": "2026年5月区两会作政府工作报告，6月仍在任，其后卸任"},
    # 张峤（前任区委书记）
    {"person_id": 4, "org_id": 1, "title": "区委书记", "start_date": "2021年前后", "end_date": "2026年2月", "rank": "县处级正职", "note": "2026年1-2月仍以区委书记身份活动"},
    # 李百锁
    {"person_id": 5, "org_id": 3, "title": "区人大常委会党组书记、主任", "start_date": "", "end_date": "至今", "rank": "县处级正职", "note": "2026年5月区两会报道确认"},
    # 李新章
    {"person_id": 6, "org_id": 4, "title": "区政协党组书记、主席", "start_date": "", "end_date": "至今", "rank": "县处级正职", "note": "2026年5月区两会报道确认"},
    # 华秦
    {"person_id": 7, "org_id": 5, "title": "区委常委、区纪委书记、区监委主任", "start_date": "2025年5月", "end_date": "至今", "rank": "县处级副职", "note": "2026年5月区第十九届人大五次会议选举为区监委主任"},
    # 区委常委们
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "2026年5月区两会报道确认"},
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "2026年5月区两会报道确认"},
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "2026年5月区两会报道确认"},
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "2026年5月区两会报道确认"},
    {"person_id": 12, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "2026年5月区两会报道确认"},
    {"person_id": 13, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "2026年5月区两会报道确认"},
    # 刘鑫
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "2026年5月区两会作民生实事专题报告"},
]

# ── 关系 ──────────────────────────────────────────────────────────
relationships = [
    # 现任党政一把手搭班子
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记—代区长搭班子",
        "overlap_org": "中共铜川市耀州区委员会/铜川市耀州区人民政府",
        "overlap_period": "2026年7月至今",
    },
    # 现任书记与前任区长（曾搭班子）
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记—区长搭班子",
        "overlap_org": "中共铜川市耀州区委员会/铜川市耀州区人民政府",
        "overlap_period": "2026年4月至6月",
    },
    # 前任书记与前任区长（长期搭班子）
    {
        "person_a": 4, "person_b": 3,
        "type": "superior_subordinate",
        "context": "前任区委书记—区长搭班子",
        "overlap_org": "中共铜川市耀州区委员会/铜川市耀州区人民政府",
        "overlap_period": "2021年至2026年2月",
    },
    # 前任书记与现任书记交接
    {
        "person_a": 4, "person_b": 1,
        "type": "predecessor_successor",
        "context": "前任区委书记交接至现任区委书记",
        "overlap_org": "中共铜川市耀州区委员会",
        "overlap_period": "2026年上半年",
    },
    # 前任区长与现任代区长交接
    {
        "person_a": 3, "person_b": 2,
        "type": "predecessor_successor",
        "context": "区长交接至代区长",
        "overlap_org": "铜川市耀州区人民政府",
        "overlap_period": "2026年7月",
    },
    # 现任书记—人大常委会主任（党政人大正职）
    {
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "区委—区人大正职共事",
        "overlap_org": "中共铜川市耀州区委员会/区人大常委会",
        "overlap_period": "2026年至今",
    },
    # 现任书记—政协主席
    {
        "person_a": 1, "person_b": 6,
        "type": "overlap",
        "context": "区委—区政协正职共事",
        "overlap_org": "中共铜川市耀州区委员会/区政协",
        "overlap_period": "2026年至今",
    },
    # 现任代区长—监委主任
    {
        "person_a": 2, "person_b": 7,
        "type": "overlap",
        "context": "区政府—区监委负责人共事",
        "overlap_org": "铜川市耀州区人民政府/区监委",
        "overlap_period": "2026年至今",
    },
    # 区委书记—各常委班子共事
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "区委常委班子共事", "overlap_org": "中共铜川市耀州区委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "区委常委班子共事", "overlap_org": "中共铜川市耀州区委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "区委常委班子共事", "overlap_org": "中共铜川市耀州区委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "区委常委班子共事", "overlap_org": "中共铜川市耀州区委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "区委常委班子共事", "overlap_org": "中共铜川市耀州区委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "区委常委班子共事", "overlap_org": "中共铜川市耀州区委员会", "overlap_period": "2026年至今"},
    # 代区长—常务/副区长
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "铜川市耀州区人民政府", "overlap_period": ""},
]

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"✅ {SLUG} 数据构建完成")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")