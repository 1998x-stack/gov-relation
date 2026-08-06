#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 井陉县 leadership network.

Province: 河北省石家庄市
Level: 县
Research date: 2026-08-06
Task: hebei_井陉县 (targets: 县委书记 & 县长)

Confirmed leaders (official sources):
- 县委副书记、县长: 赵振国 ★ 井政〔2026〕11号（2026-02-04）确认其在井陉县第十八届人大七次会议
  （2026-01-31）作《政府工作报告》，报告抬头"井陉县人民政府县长 赵振国"。
- 前任县长: 张亚松 ★ 官网政策解读确认 2025-01-14 在县十八届人大五次会议作《政府工作报告》。
- 县人大常委会主任: 霍爱民（前期纪要, plausible）
- 县政协主席: 赵建军（据词条, plausible）
- 现任县委书记: 宫世友 ★ 官方（www.sjzjx.gov.cn 十一届九次全会2025-08-08；mp.weixin 2025-12 十次全会、2026-04-08读书班）确认其为现行县委书记；约20万5年2-3月由刘丽香处接任。
- 前任县委书记: 刘丽香（官方2025-01-07 八次全会仍任，后卸任）
- 前任县长: 张亚松 ★ 井政〔2025〕1号（2025-01-14作2025政府工作报告）；2022-2024任县委副书记县长
- 县委副书记: 陈继东（2026-04, confirmed）

Confidence note: Web 检索高度受限（Exa限流、百度/搜狗/必应反爬、Jina超时）。核心任职通过
井陉县人民政府官网的政府工作报告 docx 附件全文核实；其余以 confidence 标签区分。
"""

import os
import sqlite3
import sys
from pathlib import Path

# Locate repo root by walking up until we find the gov_relation package.
_here = Path(__file__).resolve().parent
_REPO_ROOT = _here
for _parent in (Path.cwd(), *_here.parents):
    if (_parent / "gov_relation").is_dir():
        _REPO_ROOT = _parent
        break
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build  # noqa: E402

SLUG = "井陉县"
AS_OF = "2026-08-06"

DB_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.gexf"

# ── Persons ──
persons = [
    {
        "id": 1,
        "name": "赵振国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-07（待核实）",
        "birthplace": "河北省石家庄市（鹿泉区/灵寿待核实）",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "井陉县委副书记、县长",
        "current_org": "井陉县人民政府",
        "source": "井政〔2026〕11号（sjzjx.gov.cn，2026-02-04）",
    },
    {
        "id": 2,
        "name": "张亚松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "井陉县前任县长（2025）",
        "current_org": "井陉县人民政府",
        "source": "官网《井陉县2025年政府工作报告》政策解读",
    },
    {
        "id": 3,
        "name": "霍爱民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-04（据前期纪要）",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "井陉县人大常委会主任",
        "current_org": "井陉县人民代表大会常务委员会",
        "source": "前期调查纪要（2026-08-05）",
    },
    {
        "id": 4,
        "name": "赵建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "井陉县政协主席",
        "current_org": "政协井陉县委员会",
        "source": "井陉县词条（截至2025-12，plausible）",
    },
    {
        "id": 5,
        "name": "宫世友",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "井陉县委书记",
        "current_org": "中共井陉县委员会",
        "source": "官方：sjzjx.gov.cn 十一届九次全会(2025-08-08)；mp.weixin 十次全会(2025-12)、读书班(2026-04-08)",
    },
    {
        "id": 6,
        "name": "刘丽香",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "井陉县前任县委书记（~2021-2025-01）",
        "current_org": "中共井陉县委员会",
        "source": "官方：井陉县委十一届八次全会(2025-01-07)仍任县委书记",
    },
    {
        "id": 7,
        "name": "陈继东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "井陉县委副书记",
        "current_org": "中共井陉县委员会",
        "source": "mp.weixin 干部读书班(2026-04-08)确认",
    },
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共井陉县委员会", "type": "党委", "level": "县处级", "parent": "中共石家庄市委员会", "location": "井陉县"},
    {"id": 2, "name": "井陉县人民政府", "type": "政府", "level": "县处级", "parent": "石家庄市人民政府", "location": "井陉县"},
    {"id": 3, "name": "井陉县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "石家庄市人民代表大会常务委员会", "location": "井陉县"},
    {"id": 4, "name": "政协井陉县委员会", "type": "政协", "level": "县处级", "parent": "政协石家庄市委员会", "location": "井陉县"},
    {"id": 5, "name": "中共石家庄市委员会", "type": "党委", "level": "地厅级", "parent": "中共河北省委员会", "location": "石家庄市"},
    {"id": 6, "name": "石家庄市人民政府", "type": "政府", "level": "地厅级", "parent": "河北省人民政府", "location": "石家庄市"},
]

# ── Positions ──
positions = [
    {"person_id": 1, "org_id": 2, "title": "井陉县委副书记、县长",
     "start_date": "2025-12", "end_date": "present", "rank": "正处级",
     "note": "★confirmed 井政〔2026〕11号：2026-01-31 十八届人大七次会议作报告，为现任县长；2025-12 人大六次会议当选(plausible)"},
    {"person_id": 2, "org_id": 2, "title": "井陉县县长（前任）",
     "start_date": "≤2025-01", "end_date": "2025-12", "rank": "正处级",
     "note": "★confirmed 2025-01-14 县十八届人大五次会议作《政府工作报告》"},
    {"person_id": 3, "org_id": 3, "title": "井陉县人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "plausible 前期纪要：2021-07-25当选十八届人大常委会主任"},
    {"person_id": 4, "org_id": 4, "title": "井陉县政协主席",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "plausible 据词条截至2025-12"},
    {"person_id": 5, "org_id": 1, "title": "井陉县委书记",
     "start_date": "~2025-02", "end_date": "present", "rank": "正处级",
     "note": "★官方 confirmed：十一届九次全会(2025-08-08)以县委书记身份讲话；十一届十次全会(2025-12-09)、2026-04-08读书班仍任。接任刘丽香约在2025-02/03。"},
    {"person_id": 6, "org_id": 1, "title": "井陉县委书记（前任）",
     "start_date": "~2021", "end_date": "~2025-02", "rank": "正处级",
     "note": "★confirmed：2025-01-07 十一届八次全会仍以县委书记身份讲话；后由宫世友接任，去向待查。"},
    {"person_id": 7, "org_id": 1, "title": "井陉县委副书记",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "confirmed：2026-04-08 干部读书班出席"},
]

# ── Relationships ──
relationships = [
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "赵振国接任张亚松任井陉县县长（2025交接）",
     "overlap_org": "井陉县人民政府", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县长与县人大常委会主任（党政人大关系）",
     "overlap_org": "井陉县", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与县政协主席（党政政协关系）",
     "overlap_org": "井陉县", "overlap_period": ""},
    {"person_a": 5, "person_b": 1, "type": "superior_subordinate",
     "context": "宫世友（县委书记）与赵振国（县委副书记、县长）党政正职搭档（自2025年起，至2026-04同台）",
     "overlap_org": "中共井陉县委员会", "overlap_period": "2025-2026"},
    {"person_a": 5, "person_b": 6, "type": "predecessor_successor",
     "context": "宫世友接任刘丽香任井陉县委书记（约2025年2/3月）",
     "overlap_org": "中共井陉县委员会", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "赵振国（常务副县长/县长）曾在刘丽香书记任内任职",
     "overlap_org": "井陉县", "overlap_period": "2022-2025"},
    {"person_a": 1, "person_b": 7, "type": "colleague",
     "context": "赵振国（县长）与陈继东（县委副书记）同届县委班子共事",
     "overlap_org": "中共井陉县委员会", "overlap_period": "2026"},
]

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print(f"Done. DB: {DB_PATH}")
    print(f"Done. GEXF: {GEXF_PATH}")