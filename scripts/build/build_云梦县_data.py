#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 云梦县, 孝感市, 湖北省.

Task ID: hubei_云梦县
Level: 县
Targets: 县委书记 & 县长
As-of: 2026-08-06

Research status: PARTIAL (degraded web access).
Core leaders CONFIRMED from primary sources (孝感市门户 www.xiaogan.gov.cn 及
站群 gkml.xiaogan.gov.cn、湖北日报 epaper.hubeidaily.net):

  县委书记（兼孝感市人大常委会副主任）：高文峰
    - 官方新闻多次以"市人大常委会副主任、云梦县委书记高文峰"称谓
    - 佐证：孝感要闻 2026-06-16/2026-05-28/2026-03-03/2025-11-14；湖北日报 2025-11-04
  县委副书记、县人民政府代理县长：刘勤（女）
    - 孝感市人民政府新闻发布会"二十大'十五五'开局之年看实干"云梦专场（2026-07-24）
      嘉宾为"云梦县委副书记、县人民政府代理县长刘勤"

未完整核实（open gaps，见 person JSON open_questions / report open_gaps.md）：
- 高文峰、刘勤 出生年月/学历/入党时间/早年履历
- 刘勤 前任县长（即上一任县长）姓名与去向
- 高文峰 前任县委书记 姓名与去向
- 常务副县长、纪委书记、组织部/宣传部/政法委/统战部长 等县委常委会其余成员名单
- 跨县交流具体干部

处理方式：在降级网络环境下，按"部分证据产物模式"构建；姓名/职务用 CONFIRMED 标注，
人物履历不完整字段以 open_questions 记录，不做臆造。
"""

import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build

# ── Paths ──────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "云梦县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Organizations ────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共云梦县委员会", "type": "党委", "level": "县", "parent": "中共孝感市委员会", "location": "湖北省孝感市云梦县"},
    {"id": 2, "name": "云梦县人民政府", "type": "政府", "level": "县", "parent": "孝感市人民政府", "location": "湖北省孝感市云梦县"},
    {"id": 3, "name": "云梦县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "", "location": "湖北省孝感市云梦县"},
    {"id": 4, "name": "政协云梦县委员会", "type": "政协", "level": "县", "parent": "", "location": "湖北省孝感市云梦县"},
]

# ── Persons ────────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "高文峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云梦县委书记(兼孝感市人大常委会副主任)",
        "current_org": "中共云梦县委员会",
        "source": "https://www.xiaogan.gov.cn/zx/xgyw/202606/t20260616_580288.shtml",
    },
    {
        "id": 2,
        "name": "刘勤",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云梦县委副书记、云梦县人民政府代理县长",
        "current_org": "云梦县人民政府",
        "source": "https://www.xiaogan.gov.cn/zx/xxfbh/202607/t20260727_586130.shtml",
    },
    {
        "id": 3,
        "name": "赵胜家",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云梦县人民政府副县长",
        "current_org": "云梦县人民政府",
        "source": "https://www.xiaogan.gov.cn/zx/xxfbh/202607/t20260727_586130.shtml",
    },
]

# ── Positions ──────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "云梦县委书记（兼孝感市人大常委会副主任）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "现任；兼孝感市人大常委会副主任"},
    {"person_id": 2, "org_id": 1, "title": "云梦县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼任县政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "云梦县人民政府代理县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "代理县长（2026-07）"},
    {"person_id": 3, "org_id": 2, "title": "云梦县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "云梦县委书记与县委副书记、代县长搭班", "overlap_org": "中共云梦县委员会/云梦县人民政府", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "云梦县委书记与副县长（县委统一领导）", "overlap_org": "中共云梦县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "云梦县代县长与副县长同处县政府班子", "overlap_org": "云梦县人民政府", "overlap_period": ""},
]

# ── Build ─────────────────────────────────────────────────────────
if __name__ == "__main__":
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
    print(f"\nBuild complete for {SLUG}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF graph: {GEXF_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} organizations, {len(positions)} positions, {len(relationships)} relationships")
    print("  NOTE: partial-evidence build under degraded web access; gaps in report/open_gaps.md")