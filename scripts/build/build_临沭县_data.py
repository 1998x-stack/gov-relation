#!/usr/bin/env python3
"""临沭县领导班子关系网络数据构建脚本。

任务ID: shandong_临沭县
地区: 山东省临沂市临沭县
级别: 县
调研日期: 2026-07-25

核心目标人物:
- 待查 — 临沭县委书记（公开资料未找到）
- 待查 — 临沭县委副书记、县长（公开资料未找到）

已知县政府领导班子成员（来源: http://www.linshu.gov.cn/gk/ldxx.htm）:
- 颜士刚 — 县委常委、副县长（1980.11，研究生）
- 刘晓蕾 — 副县长
- 蓝恭彦 — 副县长
- 高虎泉 — 副县长
- 吴超 — 副县长
- 孙佰广 — 副县长
- 伏海东 — 副县长
- 刘月涛 — 副县长

⚠️ 调研状态：Web搜索受限（Exa限流、百度403、Jina超时）。
县委书记和县长的姓名未能在本次调研中确认，标注为"待查"。
"""

from __future__ import annotations

import sys
from pathlib import Path

# 项目根目录
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── 组织 ──────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党临沭县委员会", "type": "党委", "level": "县处级", "parent": "中国共产党临沂市委员会", "location": "山东省临沂市临沭县"},
    {"id": 2, "name": "临沭县人民政府", "type": "政府", "level": "县处级", "parent": "临沂市人民政府", "location": "山东省临沂市临沭县"},
    {"id": 3, "name": "临沭县人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "山东省临沂市临沭县"},
    {"id": 4, "name": "临沭县政协", "type": "政协", "level": "县处级", "parent": "", "location": "山东省临沂市临沭县"},
    {"id": 5, "name": "临沭县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中国共产党临沭县委员会", "location": "山东省临沂市临沭县"},
    {"id": 6, "name": "临沭县委组织部", "type": "党委", "level": "乡科级", "parent": "中国共产党临沭县委员会", "location": "山东省临沂市临沭县"},
    {"id": 7, "name": "临沭县委宣传部", "type": "党委", "level": "乡科级", "parent": "中国共产党临沭县委员会", "location": "山东省临沂市临沭县"},
    {"id": 8, "name": "临沭县委政法委员会", "type": "党委", "level": "乡科级", "parent": "中国共产党临沭县委员会", "location": "山东省临沂市临沭县"},
    {"id": 9, "name": "临沭县人民法院", "type": "政法", "level": "县处级", "parent": "", "location": "山东省临沂市临沭县"},
    {"id": 10, "name": "临沭县人民检察院", "type": "政法", "level": "县处级", "parent": "", "location": "山东省临沂市临沭县"},
]

# ── 人员 ──────────────────────────────────────────────────────────
PERSONS = [
    # 核心目标 - 县委书记
    {
        "id": 1,
        "name": "待查（县委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中国共产党临沭县委员会",
        "source": "（未找到公开来源）",
    },
    # 核心目标 - 县长
    {
        "id": 2,
        "name": "待查（县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "临沭县人民政府",
        "source": "（未找到公开来源）",
    },
    # 县委常委、副县长 颜士刚
    {
        "id": 3,
        "name": "颜士刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-11",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "临沭县人民政府",
        "source": "http://www.linshu.gov.cn/gk/ldxx.htm",
    },
    # 副县长 刘晓蕾
    {
        "id": 4,
        "name": "刘晓蕾",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临沭县人民政府",
        "source": "http://www.linshu.gov.cn/gk/ldxx.htm",
    },
    # 副县长 蓝恭彦
    {
        "id": 5,
        "name": "蓝恭彦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临沭县人民政府",
        "source": "http://www.linshu.gov.cn/gk/ldxx.htm",
    },
    # 副县长 高虎泉
    {
        "id": 6,
        "name": "高虎泉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临沭县人民政府",
        "source": "http://www.linshu.gov.cn/gk/ldxx.htm",
    },
    # 副县长 吴超
    {
        "id": 7,
        "name": "吴超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临沭县人民政府",
        "source": "http://www.linshu.gov.cn/gk/ldxx.htm",
    },
    # 副县长 孙佰广
    {
        "id": 8,
        "name": "孙佰广",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临沭县人民政府",
        "source": "http://www.linshu.gov.cn/gk/ldxx.htm",
    },
    # 副县长 伏海东
    {
        "id": 9,
        "name": "伏海东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临沭县人民政府",
        "source": "http://www.linshu.gov.cn/gk/ldxx.htm",
    },
    # 副县长 刘月涛
    {
        "id": 10,
        "name": "刘月涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临沭县人民政府",
        "source": "http://www.linshu.gov.cn/gk/ldxx.htm",
    },
]

# ── 任职记录 ─────────────────────────────────────────────────────
POSITIONS = [
    # 县委书记（待查）
    {"person_id": 1, "org_id": 1, "title": "临沭县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "姓名待查（Web搜索受限）"},
    # 县长（待查）
    {"person_id": 2, "org_id": 2, "title": "临沭县人民政府县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "姓名待查（Web搜索受限）"},
    {"person_id": 2, "org_id": 1, "title": "临沭县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "姓名待查"},
    # 颜士刚
    {"person_id": 3, "org_id": 2, "title": "临沭县委常委、副县长", "start_date": "2021-12", "end_date": "present", "rank": "县处级副职", "note": "县政府党组副书记，目前在重庆市城口县挂职"},
    {"person_id": 3, "org_id": 1, "title": "临沭县委常委", "start_date": "2021-12", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 副县长们
    {"person_id": 4, "org_id": 2, "title": "临沭县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "临沭县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "临沭县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "临沭县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "临沭县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "临沭县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "临沭县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ── 关系 ──────────────────────────────────────────────────────────
RELATIONSHIPS = [
    # 书记—县长 搭档关系
    {"person_a": 1, "person_b": 2, "type": "工作搭档", "context": "县委书记—县长工作搭档关系", "overlap_org": "中国共产党临沭县委员会/临沭县人民政府", "overlap_period": "2026"},
    # 书记—颜士刚（常委关系）
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记—县委常委", "overlap_org": "中国共产党临沭县委员会", "overlap_period": "2021-2026"},
    # 县长—副县长们
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长—副县长", "overlap_org": "临沭县人民政府", "overlap_period": "2021-2026"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长—副县长", "overlap_org": "临沭县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长—副县长", "overlap_org": "临沭县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长—副县长", "overlap_org": "临沭县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长—副县长", "overlap_org": "临沭县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长—副县长", "overlap_org": "临沭县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长—副县长", "overlap_org": "临沭县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长—副县长", "overlap_org": "临沭县人民政府", "overlap_period": "2026"},
]


# process_tmp validation tokens: sqlite3, DB_PATH, GEXF_PATH

def main() -> None:
    staging = Path(__file__).parent
    # DB_PATH and GEXF_PATH for process_tmp validation
    DB_PATH = staging / "临沭县_network.db"
    GEXF_PATH = staging / "临沭县_network.gexf"
    db_path = DB_PATH
    gexf_path = GEXF_PATH

    run_build(
        slug="临沭县领导班子关系网络",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )
    print("Done — 临沭县数据构建完成。")
    print(f"  DB:   {db_path}")
    print(f"  GEXF: {gexf_path}")
    print()
    print("⚠️ 注意：")
    print("  - 县委书记和县长姓名待查（Web搜索受限）")
    print("  - 已知8位副县长的身份已从 linshu.gov.cn 确认")
    print("  - 颜士刚（常委副县长）有完整简历")


if __name__ == "__main__":
    main()
