#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 绥化市北林区 leadership network.

北林区隶属黑龙江省绥化市，为绥化市人民政府驻地（市辖区）。

**Current leadership as of 2026-08 (官方 hljbeilin.gov.cn):**
- 区委书记兼区长：张铁峰（一肩挑；2023 代区长 → 2024-2026 区长 → 2026 任区委书记兼区长）
- 区委副书记、副区长：邵景权（主持区委人大/政协工作会议、区政府常务会议，二把手）
- 区政协党组书记、主席：苏航
- 区人大常委会主任：邵广才（plausible，待确认）
- 前任区长：付秀芳（2019 代区长 → 2021 区长 → ~2023 去职，去向待核）

资料来源（官方 hljbeilin.gov.cn）：区委常委会（扩大）会议、区政府常务会议、区委人大
工作会议、区委政协工作会议等 2026-07/08 会议通稿；履历依据《2024-2026 年北林区
政府工作报告》。多数常委身份与历任书记精确履历在受限网络下未能逐项核实，已列入
report/ 与 open_gaps 相关说明。
"""

import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _parent in REPO_ROOT.parents:
    if (_parent / "gov_relation").is_dir():
        REPO_ROOT = _parent
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "北林区"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "北林区_network.db")
    GEXF_PATH = os.path.join(_STAGING, "北林区_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "北林区_network.db"
    GEXF_PATH = GRAPH_DIR / "北林区_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共北林区委员会", "type": "党委", "level": "县处级", "parent": "中共绥化市委", "location": "黑龙江省绥化市北林区"},
    {"id": 2, "name": "北林区人民政府", "type": "政府", "level": "县处级", "parent": "绥化市人民政府", "location": "黑龙江省绥化市北林区"},
    {"id": 3, "name": "北林区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "绥化市人大常委会", "location": "黑龙江省绥化市北林区"},
    {"id": 4, "name": "中国人民政治协商会议北林区委员会", "type": "政协", "level": "县处级", "parent": "政协绥化市委员会", "location": "黑龙江省绥化市北林区"},
    {"id": 5, "name": "中共北林区纪律检查委员会/北林区监察委员会", "type": "纪委", "level": "县处级", "parent": "中共绥化市纪委", "location": "黑龙江省绥化市北林区"},
    {"id": 6, "name": "中共绥化市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委", "location": "黑龙江省绥化市北林区"},
    {"id": 7, "name": "绥化市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省绥化市北林区"},
    {"id": 8, "name": "中共黑龙江省委员会", "type": "党委", "level": "省部级", "parent": "", "location": "黑龙江省哈尔滨市"},
    {"id": 9, "name": "黑龙江省人民政府", "type": "政府", "level": "省部级", "parent": "", "location": "黑龙江省哈尔滨市"},
    {"id": 10, "name": "绥胜镇人民政府", "type": "乡镇/街道", "level": "乡科级", "parent": "北林区人民政府", "location": "黑龙江省绥化市北林区绥胜镇"},
    {"id": 11, "name": "双河镇人民政府", "type": "乡镇/街道", "level": "乡科级", "parent": "北林区人民政府", "location": "黑龙江省绥化市北林区双河镇"},
    {"id": 12, "name": "兴和朝鲜族乡人民政府", "type": "乡镇/街道", "level": "乡科级", "parent": "北林区人民政府", "location": "黑龙江省绥化市北林区兴和朝鲜族乡"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 张铁峰 — 现任区委书记兼区长（confirmed）
    {"id": 1, "name": "张铁峰", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "中共北林区委书记、北林区人民政府区长", "current_org": "中共北林区委员会",
     "source": "https://www.hljbeilin.gov.cn/bl/blyw/202607/c12_db680fbd52c742de87ea854383d34128.shtml"},
    # 2 邵景权 — 区委副书记、副区长（confirmed）
    {"id": 2, "name": "邵景权", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "北林区委副书记、北林区人民政府副区长", "current_org": "中共北林区委员会",
     "source": "https://www.hljbeilin.gov.cn/bl/blyw/202607/"},
    # 3 苏航 — 北林区政协主席（confirmed）
    {"id": 3, "name": "苏航", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "北林区政协党组书记、主席", "current_org": "政协北林区委员会",
     "source": "https://www.hljbeilin.gov.cn/bl/blyw/202607/"},
    # 4 付秀芳 — 前式区长（confirmed via 政府工作报告；去向待核）
    {"id": 4, "name": "付秀芳", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "历任北林区区长", "current_org": "北林区人民政府",
     "source": "https://www.hljbeilin.gov.cn/bl/zfgzbg/202103/"},
    # 5 — 户秀才 — 区人大常委会主任（plausible）
    {"id": 5, "name": "邵广才", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "北林区人大常委会主任（plausible）", "current_org": "北林区人民代表大会常务委员会",
     "source": "https://www.hljbeilin.gov.cn/bl/blyw/202607/c12_d1595871c2f4830d34101f612124aac.shtml"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "北林区委书记", "start": "2026", "end": "present", "rank": "正县处级", "note": "2026 任区委书记（兼任区长）"},
    {"person_id": 1, "org_id": 2, "title": "北林区人民政府区长", "start": "2023", "end": "present", "rank": "正县处级", "note": "2023 代区长，2024 起区长；2026 兼任书记"},
    {"person_id": 2, "org_id": 1, "title": "北林区委副书记", "start": "", "end": "present", "rank": "副县处级", "note": "主持区委人大/政协工作会议"},
    {"person_id": 2, "org_id": 2, "title": "北林区人民政府副区长", "start": "", "end": "present", "rank": "副县处级", "note": "区政府常务会议主持人（常务副区长）"},
    {"person_id": 3, "org_id": 4, "title": "北林区政协党组书记、主席", "start": "", "end": "present", "rank": "正县处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "北林区人大常委会主任（plausible）", "start": "", "end": "present", "rank": "正县处级", "note": "待确认"},
    {"person_id": 4, "org_id": 2, "title": "北林区代区长/区长", "start": "2019", "end": "2022", "rank": "正县处级", "note": "2019 代区长，2021 正式；2023 前卸任"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "张铁峰（区委书记兼区长）与邵景权（区委副书记、副区长）为北林区现任党政主要领导-常务副手搭档", "overlap_org": "北林区", "overlap_period": "2023至今"},
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor", "context": "张铁峰接付秀芳任北林区长（付 2019-2022 → 张 2023）", "overlap_org": "北林区人民政府", "overlap_period": "2023"},
    {"person_a": 1, "person_b": 3, "type": "党政同区共事", "context": "张铁峰（书记兼区长）与苏航（区政协主席）同在北林区领导班子", "overlap_org": "北林区", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 5, "type": "党政同区共事", "context": "张铁峰与区人大常委会主任邵广才（plausible）同在北林区领导班子", "overlap_org": "北林区", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 3, "type": "党政同区共事", "context": "邵景权（副书记/副区长）与苏航（政协主席）出席区委人大/政协工作会议", "overlap_org": "北林区", "overlap_period": "2026"},
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
        overwrite=True,
    )
    print(f"Wrote DB: {DB_PATH}")
    print(f"Wrote GEXF: {GEXF_PATH}")
    print(f"Stats: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")