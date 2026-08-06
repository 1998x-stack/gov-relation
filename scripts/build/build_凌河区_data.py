#!/usr/bin/env python3
"""
锦州市凌河区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Linghe District (凌河区) leadership.

Level: 市辖区 (县处级)
Province: 辽宁省
Parent City: 锦州市
Targets: 区委书记 (赵宏亮) & 区长 (李子元)

Sources (一手/官方):
- 凌河区人民政府官网 www.jzlhqzf.gov.cn — 政府领导页 (zwgk1/fdzdgknr/jg/zfld1.htm),
  凌河要闻 (赵宏亮 调研/会见), 领导接访安排 (信访局), 政府工作报告 (2022—2026).
- 锦州市人民政府官网 www.jz.gov.cn — 政府领导页, 人事任免 (李子元免职, 2026-01-04).
- 太和区人民政府官网 www.jzth.gov.cn — 确认 尹璐 现任 太和区委书记 (前任凌河区长, 跨区交流).
- 本地仓库既有 古塔区/太和区 person 数据 (20260806/20260725).

注意 (source_fallbacks playbook)：Exa 限流、Baidu/Jina 不可用，故部分人物传记字段缺失；
缺失字段不入库臆造，写入 person JSON open_questions 与 report/open_gaps.md。
"""

import sqlite3  # noqa: F401 (required token by process_tmp.py; used via gov_relation.runner)
import sys
from pathlib import Path

# Ensure gov_relation is importable
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]  # data/tmp/<task_id>/ -> data/ -> repo root
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

# ════════════════════════════════════════════
# SLUG
# ════════════════════════════════════════════
SLUG = "凌河区"

# ════════════════════════════════════════════
# PATHS (staging: updated by process_tmp.py on promotion)
# ════════════════════════════════════════════
DB_PATH = SCRIPT_DIR / f"{SLUG}_network.db"
GEXF_PATH = SCRIPT_DIR / f"{SLUG}_network.gexf"

# ════════════════════════════════════════════
# PERSONS
# ════════════════════════════════════════════
persons = [
    # ── 区委书记 (Party Secretary): 赵宏亮 ──
    {
        "id": 1,
        "name": "赵宏亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共锦州市凌河区委员会",
        "source": "凌河区人民政府官网 (要闻: 2026-07-17 区委书记赵宏亮调研教育系统; 一般接访安排 2026-07-31)",
    },
    # ── 区委副书记、区长 (District Mayor): 李子元 ──
    {
        "id": 2,
        "name": "李子元",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "凌河区人民政府",
        "source": "凌河区官网政府领导页 (2026); 2026年政府工作报告署名'代区长 李子元' (2025-12-29)",
    },
    # ── 区委副书记: 张进 ──
    {
        "id": 3,
        "name": "张进",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共锦州市凌河区委员会",
        "source": "凌河区领导一般接访安排 (2026-07-31 发布, 官方)",
    },
    # ── 区委常委、常务副区长: 安锟 ──
    {
        "id": 4,
        "name": "安锟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "凌河区人民政府",
        "source": "凌河区政府领导页 + 一般接访安排 (2026, 官方)",
    },
    # ── 区委常委、副区长: 黄强 ──
    {
        "id": 5,
        "name": "黄强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "凌河区人民政府",
        "source": "凌河区政府领导页 + 一般接访 (2026, 官方)",
    },
    # ── 区委常委、区委组织部部长、副区长: 谭丽娜 ──
    {
        "id": 6,
        "name": "谭丽娜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区委组织部部长、副区长",
        "current_org": "中共锦州市凌河区委组织部 / 凌河区人民政府",
        "source": "凌河区政府领导页; 新闻 (2026-07-17 参加赵宏亮调研, 官方)",
    },
    # ── 区委常委、宣传部部长: 王锦程 ──
    {
        "id": 7,
        "name": "王锦程",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共锦州市凌河区委宣传部",
        "source": "凌河区领导一般接访安排 (2026-07-31, 官方)",
    },
    # ── 区委常委、副区长 (苏锦合作): 沈卫林 ──
    {
        "id": 8,
        "name": "沈卫林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "凌河区人民政府",
        "source": "凌河区政府领导页 (2026, 官方)",
    },
    # ── 副区长、市公安局凌河分局局长: 王俊岭 ──
    {
        "id": 9,
        "name": "王俊岭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长、市公安局凌河分局局长",
        "current_org": "凌河区人民政府 / 锦州市公安局凌河分局",
        "source": "凌河区政府领导页 (2026, 官方)",
    },
    # ── 副区长 (挂职): 张宇 ──
    {
        "id": 10,
        "name": "张宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长 (外出挂职)",
        "current_org": "凌河区人民政府",
        "source": "凌河区政府领导页 (2026, 官方)",
    },
    # ── 副区长: 白涛 ──
    {
        "id": 11,
        "name": "白涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "凌河区人民政府",
        "source": "凌河区政府领导页 (2026, 官方)",
    },
    # ── 前任凌河区区长 → 现任太和区委书记: 尹璐 (跨区交流, 关键) ──
    {
        "id": 12,
        "name": "尹璐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "太和区委书记 (由 凌河区长 调任)",
        "current_org": "中共锦州市太和区委员会",
        "source": "凌河区政府工作报告 (2022-2024 署名'区长 尹璐'); 太和区官网 2026-08 首页 '区委书记尹璐带队调研'",
    },
    # ── 前任凌河区委书记 (2020): 于鹏 ──
    {
        "id": 13,
        "name": "于鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曾任凌河区委书记 (2020)",
        "current_org": "中共锦州市凌河区委员会",
        "source": "凌河区官网 2020-06 新闻 '凌河区委书记于鹏督导检查老旧小区改造'",
    },
]

# ════════════════════════════════════════════
# ORGANIZATIONS
# ════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共锦州市凌河区委员会", "type": "党委", "level": "县处级", "parent": "中共锦州市委员会", "location": "辽宁省锦州市凌河区"},
    {"id": 2, "name": "凌河区人民政府", "type": "政府", "level": "县处级", "parent": "锦州市人民政府", "location": "辽宁省锦州市凌河区"},
    {"id": 3, "name": "中共锦州市凌河区委组织部", "type": "党委", "level": "乡科级", "parent": "中共锦州市凌河区委员会", "location": "辽宁省锦州市凌河区"},
    {"id": 4, "name": "中共锦州市凌河区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共锦州市凌河区委员会", "location": "辽宁省锦州市凌河区"},
    {"id": 5, "name": "锦州市公安局凌河分局", "type": "政府", "level": "乡科级", "parent": "锦州市公安局", "location": "辽宁省锦州市凌河区"},
    {"id": 6, "name": "中共锦州市太和区委员会", "type": "党委", "level": "县处级", "parent": "中共锦州市委员会", "location": "辽宁省锦州市太和区"},
]

# ════════════════════════════════════════════
# POSITIONS
# ════════════════════════════════════════════
positions = [
    # 赵宏亮 (区委书记)
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持区委全面工作"},
    # 李子元 (区委副书记、区长)
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长 (曾任代区长)", "start_date": "2025-12", "end_date": "present", "rank": "正处级", "note": "2026年政府工作报告署'代区长 李子元'; 现已任区长"},
    # 张进 (区委副书记)
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管区委办、党史室、群团、综合服务中心"},
    # 安锟 (常务副区长)
    {"person_id": 4, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责政府日常工作"},
    # 黄强 (副区长)
    {"person_id": 5, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "大数据、商务、外贸、市场监管、招商"},
    # 谭丽娜 (组织部部长、副区长)
    {"person_id": 6, "org_id": 3, "title": "区委常委、区委组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "区政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "教育、科技、文旅、卫健"},
    # 王锦程 (宣传部部长)
    {"person_id": 7, "org_id": 4, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "宣传、网信"},
    # 沈卫林 (副区长)
    {"person_id": 8, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "苏锦合作"},
    # 王俊岭 (副区长、公安分局局长)
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "公安、司法"},
    {"person_id": 9, "org_id": 5, "title": "市公安局凌河分局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张宇 (副区长, 挂职)
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "外出挂职不参与分工"},
    # 白涛 (副区长)
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "住建、城管、交通、人防、自然资源"},
    # 尹璐 (前任区长 → 太和区委)
    {"person_id": 12, "org_id": 2, "title": "区长 (前任)", "start_date": "2022", "end_date": "2025", "rank": "正处级", "note": "2022-2024 凌河区长; 后转任太和区委书记"},
    {"person_id": 12, "org_id": 6, "title": "太和区委书记 (现任)", "start_date": "2026", "end_date": "present", "rank": "正处级", "note": "跨区交流: 凌河区长→太和区委书记"},
    # 于鹏 (前任区委书记)
    {"person_id": 13, "org_id": 1, "title": "区委书记 (前任)", "start_date": "", "end_date": "2020 (任内)", "rank": "正处级", "note": "2020-06 在任"},
]

# ════════════════════════════════════════════
# RELATIONSHIPS
# ════════════════════════════════════════════
relationships = [
    # 党政一把手 (现任)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长，党政主要负责人搭档", "overlap_org": "中共锦州市凌河区委员会/凌河区人民政府", "overlap_period": "至今"},
    # 书记—各部门 (区委班子)
    {"person_a": 1, "person_b": 3, "type": "领导", "context": "区委书记—区委副书记张进", "overlap_org": "中共锦州市凌河区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "领导", "context": "区委书记—宣传部部长王锦程", "overlap_org": "中共锦州市凌河区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "领导", "context": "区委书记—组织部部长谭丽娜", "overlap_org": "中共锦州市凌河区委员会", "overlap_period": ""},
    # 区长—副区长们 (政府班子)
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "区长—常务副区长安锟", "overlap_org": "凌河区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "区长—区委常委、副区长黄强", "overlap_org": "凌河区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "区长—区委常委、副区长沈卫林", "overlap_org": "凌河区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "区长—副区长（兼公安分局局长）王俊岭", "overlap_org": "凌河区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "区长—副区长白涛", "overlap_org": "凌河区人民政府", "overlap_period": ""},
    # 前任区长 尹璐 ↔ 现任区长 (职务更迭)
    {"person_a": 2, "person_b": 12, "type": "前任", "context": "李子元接替尹璐任凌河区区长", "overlap_org": "凌河区人民政府", "overlap_period": "2025-12"},
    # 前任区委书记 于鹏
    {"person_a": 1, "person_b": 13, "type": "继承", "context": "赵宏亮为于鹏之后的凌河区委书记（更迭细节开放项）", "overlap_org": "中共锦州市凌河区委员会", "overlap_period": ""},
]

# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════
if __name__ == "__main__":
    print(f"Building {SLUG} leadership network...")
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
    print(f"[OK] DB: {DB_PATH}")
    print(f"[OK] GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")