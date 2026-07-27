#!/usr/bin/env python3
"""振安区（丹东市）领导班子工作关系网络 - 数据构建脚本

注意：由于网络搜索工具受限（Exa 限流、Baidu 403、振安区政府网站无法访问），
当前数据为占位结构，核心领导的姓名和履历待补充。
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

AS_OF = "2026-07-25"
SLUG = "振安区"

# ═══════════════════════════════════════════════════════════════════════
# DATA — 数据待补充
# ═══════════════════════════════════════════════════════════════════════
#
# 振安区（丹东市市辖区）的现任区委书记和区长的姓名、履历均未能通过网络搜索确认。
# 政府网站 www.ddzhenan.gov.cn 无法访问，所有搜索引擎均受限或超时。
#
# 已知丹东市下辖三区：元宝区、振兴区、振安区。
# 元宝区已在先前调查中确认（区委书记赵洪绪、区长夏昌海）。
# 振安区待后续在有网络访问能力的环境下补充。

persons = [
    {
        "id": 1,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共振安区委",
        "source": "需通过振安区政府网站或百度搜索补充",
        "notes": "振安区委书记 — 姓名、完整履历均待确认。政府网站 www.ddzhenan.gov.cn 无法访问。",
    },
    {
        "id": 2,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "振安区人民政府",
        "source": "需通过振安区政府网站或百度搜索补充",
        "notes": "振安区区长 — 姓名、完整履历均待确认。政府网站 www.ddzhenan.gov.cn 无法访问。",
    },
]

organizations = [
    {"id": 1, "name": "中共振安区委", "type": "党委", "level": "市辖区", "parent": "中共丹东市委", "location": "辽宁省丹东市振安区"},
    {"id": 2, "name": "振安区人民政府", "type": "政府", "level": "市辖区", "parent": "丹东市人民政府", "location": "辽宁省丹东市振安区"},
    {"id": 3, "name": "振安区人大常委会", "type": "人大", "level": "市辖区", "parent": "丹东市人大常委会", "location": "辽宁省丹东市振安区"},
    {"id": 4, "name": "振安区政协", "type": "政协", "level": "市辖区", "parent": "丹东市政协", "location": "辽宁省丹东市振安区"},
    {"id": 5, "name": "振安区纪委监委", "type": "党委", "level": "市辖区", "parent": "中共丹东市纪委", "location": "辽宁省丹东市振安区"},
]

positions = []
relationships = []

# ═══════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / f"{SLUG}_network.db",
        gexf_path=GRAPH_DIR / f"{SLUG}_network.gexf",
        overwrite=True,
    )
    print(f"✅ {SLUG} 数据构建完成（占位数据 - 领导信息待补充）")
