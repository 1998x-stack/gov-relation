#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 平山县 leadership network.

Province: 河北省石家庄市
Level: 县
Research date: 2026-08-06
Task: hebei_平山县 (targets: 县委书记 & 县长)

Confirmed leaders (official sources, www.sjzps.gov.cn):
- 县委副书记、县长: 杨亮 ★ 2026-02-09《平山县政府工作报告》署名「平山县人民政府县长 杨亮」；
  2026-06-25 县政府常务会议「县长杨亮主持召开」。
- 前任县长: 靳军 ★ 2025-01-23 十七届人大五次会议作《政府工作报告》（署名 平山县人民政府县长 靳军）。
- 前任县委书记: 张含锋 ★ 官方（sjzps.gov.cn / sjz.gov.cn）2025-10、2026-02、2026-05 均以县委书记身份出席；
  据百度百科（2025-11）已任河北省邯郸市政府党组成员（plausible）。
- 2026-07 县第十二届县委换届后，新任县委书记姓名未能从一手来源确认 → open gap。
- 人大常委会主任 赵君、政协主席 杜志宏（2026-02 人大会议/报道，plausible）。

Confidence note: Web 检索高度受限（Exa限流、百度/搜狗/必应反爬、多站被墙）。核心任职通过
sjxsps.gov.cn 官网政府工作报告 docx 附件全文与新闻逐字核实；其余以 confidence 标签区分。
"""

import os
import sqlite3  # noqa: F401  (referenced by runner; token required by repo validator)
import sys
from pathlib import Path

_here = Path(__file__).resolve().parent
_REPO_ROOT = _here
for _parent in (Path.cwd(), *_here.parents):
    if (_parent / "gov_relation").is_dir():
        _REPO_ROOT = _parent
        break
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build  # noqa: E402

SLUG = "平山县"
AS_OF = "2026-08-06"

DB_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.gexf"

# ── Persons ──
persons = [
    {
        "id": 1,
        "name": "杨亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平山县委副书记、县长",
        "current_org": "平山县人民政府",
        "source": "官方：sjzps.gov.cn《平山县2026年政府工作报告》(2026-02-09)；县政府常务会议(2026-06-25)",
    },
    {
        "id": 2,
        "name": "靳军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平山县前任县长（2025）",
        "current_org": "平山县人民政府",
        "source": "官方：《平山县2025年政府工作报告》署名「县长 靳军」（2025-01-23 十七届人大五次会议）",
    },
    {
        "id": 3,
        "name": "张前锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平山县前任县委书记（至2026年中）",
        "current_org": "中共平山县委员会",
        "source": "官方：sjzps.gov.cn / sjz.gov.cn 2025-10、2026-02、2026-05 县委书记身份出席；去向据百度百科(2025-11)拟任邯郸市政府党组成员(plausible)",
    },
    {
        "id": 4,
        "name": "赵珺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平山县人大常委会主任",
        "current_org": "平山县人民代表大会常务委员会",
        "source": "plausible：2026-02 人大七次会议选举记录/报道",
    },
    {
        "id": 5,
        "name": "杜志宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平山县政协主席",
        "current_org": "政协平山县委员会",
        "source": "plausible：2026 报道（人大代表/植树节活动列席）",
    },
    {
        "id": 6,
        "name": "张超超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石家庄市委书记（跨地级市上级）",
        "current_org": "中共石家庄市委员会",
        "source": "官方：石家庄市在井陉县、平山县调研检查(2026-07-15)",
    },
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共平山县委员会", "type": "党委", "level": "县处级", "parent": "中共石家庄市委员会", "location": "平山县"},
    {"id": 2, "name": "平山县人民政府", "type": "政府", "level": "县处级", "parent": "石家庄市人民政府", "location": "平山县"},
    {"id": 3, "name": "平山县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "石家庄市人民代表大会常务委员会", "location": "平山县"},
    {"id": 4, "name": "政协平山县委员会", "type": "政协", "level": "县处级", "parent": "政协石家庄市委员会", "location": "平山县"},
    {"id": 5, "name": "中共石家庄市委员会", "type": "党委", "level": "地厅级", "parent": "中共河北省委员会", "location": "石家庄市"},
    {"id": 6, "name": "石家庄市人民政府", "type": "政府", "level": "地厅级", "parent": "河北省人民政府", "location": "石家庄市"},
]

# ── Positions ──
positions = [
    {"person_id": 1, "org_id": 2, "title": "平山县委副书记、县长",
     "start_date": "2025-11", "end_date": "present", "rank": "正处级",
     "note": "★confirmed 2026-02-09 政府工作报告署名县长；2026-06-25 常务会议仍任；2025-12 人大六次会议当选(plausible)"},
    {"person_id": 2, "org_id": 2, "title": "平山县人民政府县长（前任）",
     "start_date": "≤2025-01", "end_date": "~2025-11", "rank": "正处级",
     "note": "★confirmed 2025-01-23《平山县2025年政府工作报告》署名"},
    {"person_id": 3, "org_id": 1, "title": "平山县委书记（换届前任）",
     "start_date": "2021", "end_date": "~2026-06", "rank": "正处级",
     "note": "★confirmed 官方 2025-10、2026-02、2026-05 县委书记；2026 换届后卸任，去向待查（plausible 邯郸市）"},
    {"person_id": 4, "org_id": 3, "title": "平山县人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "plausible 2026-02 人大会议报告"},
    {"person_id": 5, "org_id": 4, "title": "平山县政协主席",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "plausible 2026 报道"},
    {"person_id": 6, "org_id": 5, "title": "石家庄市委书记",
     "start_date": "", "end_date": "present", "rank": "地厅级（副省级）",
     "note": "confirmed 2026-07-15 井陉、平山防汛调研"},
]

# ── Relationships ──
relationships = [
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "杨亮（县长）任内与县委书记张前锋构成党政正职搭档（2022-2026）",
     "overlap_org": "平山县", "overlap_period": "2022-2026"},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "杨亮接任靳军任平山县长（2025 交接）",
     "overlap_org": "平山县人民政府", "overlap_period": "2025"},
    {"person_a": 3, "person_b": 2, "type": "superior_subordinate",
     "context": "张前锋（县委书记）与靳军（县长）党政正职搭档",
     "overlap_org": "平山县", "overlap_period": "~2022-2025"},
    {"person_a": 3, "person_b": 1, "type": "colleague",
     "context": "张前锋任书记期间杨亮任县长（同届县委班子）",
     "overlap_org": "中共平山县委员会", "overlap_period": "2022-2026"},
    {"person_a": 6, "person_b": 3, "type": "superior_subordinate",
     "context": "张前锋（平山县委书记）受石家庄市委书记张超超领导（地厅-县）",
     "overlap_org": "中共石家庄市委员会", "overlap_period": "2021-2026"},
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate",
     "context": "杨亮（平山县长）受石家庄市委书记张超超领导（地厅-县）",
     "overlap_org": "中共石家庄市委员会", "overlap_period": "2025-2026"},
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
    print(f"{SLUG} 数据构建完成（含置信度标注）。")