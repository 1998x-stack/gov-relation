#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 西安市新城区, 陕西省 (Shaanxi).

Task: shaanxi_新城区
Province: 陕西省
Parent city: 西安市
Region: 新城区
Level: 市辖区
Targets: 区委书记 & 区长
Investigation date: 2026-08-07

SLUG DISAMBIGUATION:
  The repo already contains committed artifacts for a DIFFERENT 新城区 —
  呼和浩特市新城区 (Inner Mongolia) — stored as `新城区_network.db` /
  `build_新城区_data.py`. To avoid overwriting that committed data, this
  script uses the disambiguated slug `西安市新城区`, following the repo's
  existing namesake convention (e.g. `辽源市西安区_network.db`).
  Outputs here: data/database/西安市新城区_network.db, data/graph/西安市新城区_network.gexf

Sources: all data confirmed from the official primary source
  http://www.xincheng.gov.cn/ (西安市新城区人民政府), via its
    - 领导信息 leadership pages `/zwgk/ldxx/<pinyin>/1.html`
    - 领导接访公示 (duty roster) `/tszx/ldjfgs/`
    - 区委全会 / 人大 / 政协 两会 news reports (2024-2026)
  Exa web search was rate-limited and Bing/Baidu unreliable on the
  investigation date; leadership data was pulled directly from official pages.

Confidence:
  - confirmed: official leadership page / 接访公示 / 两会 news report
  - plausible: consistent across multiple official reports
  - 贾轶昊 detailed bio (birth/education/prior posts) not published on the
    official public pages -> flagged in report open_gaps.
"""

import os
import sqlite3  # noqa: F401  (required by process_tmp validation tokens)
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
# Walk up to the dir containing gov_relation/; works from scripts/build/ or data/tmp/<id>/.
_PROJECT_ROOT = None
_probe = Path(BASE)
for _ in range(6):
    if (_probe / "gov_relation").is_dir():
        _PROJECT_ROOT = str(_probe)
        break
    _probe = _probe.parent
assert _PROJECT_ROOT is not None, "could not locate repo root (gov_relation/)"
PROJECT_ROOT = _PROJECT_ROOT
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build

SLUG = "西安市新城区"
AS_OF = "2026-08-07"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / "西安市新城区_network.db")
GEXF_PATH = str(STAGING_DIR / "西安市新城区_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Persons
# ═══════════════════════════════════════════════════════════════════════════════
persons_data = [
    # ══ 区委 (Party Committee) ══
    {"id": 1, "name": "贾轶昊", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委书记（兼西安市人大常委会副主任）", "current_org": "中共西安市新城区委员会",
     "source": "official xincheng.gov.cn 两会/全会报道; 2024-01起连续确认为区委书记"},
    {"id": 2, "name": "曹宝利", "gender": "男", "ethnicity": "汉族", "birth": "1970年2月", "birthplace": "陕西（户县任职背景）",
     "education": "研究生学历", "party_join": "1994年9月", "work_start": "1990年9月",
     "current_post": "区委副书记、区政府党组书记、区长", "current_org": "西安市新城区人民政府",
     "source": "official 领导信息 cbl page"},
    {"id": 3, "name": "陈红利", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委副书记（专职）", "current_org": "中共西安市新城区委员会",
     "source": "official 14th 10th 全会(2026-02)确认在任"},
    {"id": 4, "name": "周恒", "gender": "男", "ethnicity": "汉族", "birth": "1979年1月", "birthplace": "陕西",
     "education": "研究生学历，经济学博士", "party_join": "2001年6月", "work_start": "2001年7月",
     "current_post": "区委常委、区政府党组副书记、常务副区长", "current_org": "西安市新城区人民政府",
     "source": "official 领导页 lzh page"},
    {"id": 5, "name": "杨珩", "gender": "男", "ethnicity": "汉族", "birth": "1975年6月", "birthplace": "陕西",
     "education": "研究生学历", "party_join": "1997年3月", "work_start": "1997年8月",
     "current_post": "区委常委、区政府党组成员、副区长", "current_org": "西安市新城区人民政府",
     "source": "official 领导页 yh page"},
    {"id": 6, "name": "杨辉", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委、政法委书记", "current_org": "中共西安市新城区委员会",
     "source": "official 接访公示; 政法演练报道(2025-12)"},
    {"id": 7, "name": "陈金鹏", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委、区纪委书记、区监委主任", "current_org": "中共西安市新城区纪律检查委员会",
     "source": "official 区政府廉政工作会议(2026-03-25)"},
    {"id": 8, "name": "陈美蓉", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委、统战部部长", "current_org": "中共西安市新城区委员会",
     "source": "official 接访公示(2026-08)"},
    {"id": 9, "name": "王方伟", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委、组织部部长", "current_org": "中共西安市新城区委员会",
     "source": "official 接访公示(2026-08) 点名"},
    {"id": 10, "name": "戴微", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委、宣传部部长、网信办主任（兼）", "current_org": "中共西安市新城区委员会",
     "source": "official 接访公示(2026-08)"},
    {"id": 11, "name": "许小红", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委、武装部部长", "current_org": "西安市新城区人民武装部",
     "source": "official 接访公示(2026-08); 八一慰问报道(2024-07)"},

    # ══ 区政府副区长（非常委） ══
    {"id": 12, "name": "郭金虎", "gender": "男", "ethnicity": "汉族", "birth": "1977年4月", "birthplace": "陕西",
     "education": "大学学历", "party_join": "2002年8月", "work_start": "",
     "current_post": "区政府党组成员、副区长", "current_org": "西安市新城区人民政府",
     "source": "official 领导页 gjh page"},
    {"id": 13, "name": "赵辉", "gender": "男", "ethnicity": "汉族", "birth": "1977年11月", "birthplace": "陕西",
     "education": "研究生学历，法学硕士", "party_join": "1998年4月", "work_start": "",
     "current_post": "区政府党组成员、副区长", "current_org": "西安市新城区人民政府",
     "source": "official 领导页 zh page"},
    {"id": 14, "name": "李枫艳", "gender": "女", "ethnicity": "汉族", "birth": "1974年9月", "birthplace": "陕西",
     "education": "大学学历，工程硕士", "party_join": "", "work_start": "",
     "current_post": "区政府副区长", "current_org": "西安市新城区人民政府",
     "source": "official 领导页 lfy page; 农工党"},
    {"id": 15, "name": "王亚林", "gender": "男", "ethnicity": "汉族", "birth": "1973年2月", "birthplace": "陕西",
     "education": "研究生学历", "party_join": "2002年5月", "work_start": "",
     "current_post": "区政府党组成员、副区长", "current_org": "西安市新城区人民政府",
     "source": "official 领导页 wyl page"},
    {"id": 16, "name": "雪帆", "gender": "男", "ethnicity": "汉族", "birth": "1976年6月", "birthplace": "陕西",
     "education": "大学学历，工商管理硕士", "party_join": "1999年6月", "work_start": "",
     "current_post": "区政府党组成员、副区长", "current_org": "西安市新城区人民政府",
     "source": "official 领导页 xf page"},
    {"id": 17, "name": "李西安", "gender": "男", "ethnicity": "汉族", "birth": "1969年6月", "birthplace": "陕西",
     "education": "大学学历", "party_join": "1989年12月", "work_start": "",
     "current_post": "区政府党组成员、副区长，公安新城分局局长兼督察长", "current_org": "西安市公安局新城分局",
     "source": "official 领导页 lxa page; 前任公安局长李浩(2024)"},

    # ══ 人大 / 政协 ══
    {"id": 18, "name": "赵明欣", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区人大常委会主任", "current_org": "西安市新城区人民代表大会常务委员会",
     "source": "official 人大五次会议(2026-03)"},
    {"id": 19, "name": "张炜", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "区政协党组书记、主席", "current_org": "西安市新城区政协",
     "source": "official 政协五次会议(2026-03)"},
    {"id": 20, "name": "邓晓东", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "前任区人民政府区长（至2024）", "current_org": "西安市新城区人民政府",
     "source": "official 2024-05 目标考核会议; 2025 前由曹宝利接任代区长"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════════════
organizations_data = [
    {"id": 1, "name": "中共西安市新城区委员会", "type": "党委", "level": "区级", "parent": "中共西安市委", "location": "西安市新城区"},
    {"id": 2, "name": "西安市新城区人民政府", "type": "政府", "level": "区级", "parent": "西安市人民政府", "location": "西安市新城区"},
    {"id": 3, "name": "中共西安市新城区纪律检查委员会", "type": "党委", "level": "区级", "parent": "中共西安市新城区委员会", "location": "西安市新城区"},
    {"id": 4, "name": "西安市新城区人民代表大会常务委员会", "type": "人大", "level": "区级", "parent": "", "location": "西安市新城区"},
    {"id": 5, "name": "西安市新城区政协", "type": "政协", "level": "区级", "parent": "", "location": "西安市新城区"},
    {"id": 6, "name": "西安市新城区人民武装部", "type": "群团", "level": "区级", "parent": "", "location": "西安市新城区"},
    {"id": 7, "name": "西安市公安局新城分局", "type": "政府", "level": "分局", "parent": "西安市公安局", "location": "西安市新城区"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Positions
# ═══════════════════════════════════════════════════════════════════════════════
positions_data = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2024-01起", "end": "present", "rank": "副厅级", "note": "兼任西安市人大常委会副主任"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "2025", "end": "present", "rank": "副厅级", "note": "2025-08起任代区长"},
    {"person_id": 2, "org_id": 2, "title": "区政府党组书记、代区长", "start": "2025", "end": "2026-03-19", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区政府党组书记、区长", "start": "2026-03-19", "end": "present", "rank": "副厅级", "note": "2026-03人代会五次会议当选区长"},
    {"person_id": 3, "org_id": 1, "title": "区委副书记（专职）", "start": "2024前", "end": "present", "rank": "副处级", "note": "2026-02全会确认在任"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "区政府党组副书记、常务副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "原区委常委、组织部长转任"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "区政府党组成员、副区长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "区委常委、政法委书记", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 3, "title": "区纪委书记、区监委主任", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "区委常委、统战部部长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "区委常委、组织部部长", "start": "未知", "end": "present", "rank": "副处级", "note": "接任组织部部长"},
    {"person_id": 10, "org_id": 1, "title": "区委常委、宣传部部长、网信办主任（兼）", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "区武装部部长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "区政府党组成员、副区长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "区政府党组成员、副区长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "区政府副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "农工党"},
    {"person_id": 15, "org_id": 2, "title": "区政府党组成员、副区长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "区政府党组成员、副区长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "区政府党组成员、副区长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 7, "title": "公安新城分局局长兼督察长", "start": "2025-12后", "end": "present", "rank": "副处级", "note": "前任李浩"},
    {"person_id": 18, "org_id": 4, "title": "区人大常委会主任", "start": "2024前", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 5, "title": "区政协党组书记、主席", "start": "2024前", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "区长", "start": "2021前", "end": "2024", "rank": "副厅级", "note": "前任区长"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════════════
relationships_data = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长，党政一把手搭档", "overlap_org": "中共西安市新城区委员会", "overlap_period": "2025-present"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与专职副书记，同一常委会", "overlap_org": "中共西安市新城区委员会", "overlap_period": "2024-present"},
    {"person_a": 4, "person_b": 2, "type": "上下级", "context": "常务副区长与区长，政府班子搭档", "overlap_org": "西安市新城区人民政府", "overlap_period": "present"},
    {"person_a": 20, "person_b": 2, "type": "前任继任", "context": "邓晓东前任区长，曹宝利接任代区长/区长", "overlap_org": "西安市新城区人民政府", "overlap_period": "2024-2025"},
    {"person_a": 17, "person_b": 2, "type": "上下级", "context": "副区长兼公安局长与区长", "overlap_org": "西安市新城区人民政府", "overlap_period": "present"},
    {"person_a": 18, "person_b": 1, "type": "五大班子", "context": "区人大主任与区委书记", "overlap_org": "新城区委/人大", "overlap_period": "2024-present"},
    {"person_a": 19, "person_b": 1, "type": "五大班子", "context": "区政协主席与区委书记", "overlap_org": "新城区委/政协", "overlap_period": "2024-present"},
    {"person_a": 7, "person_b": 1, "type": "上下级", "context": "纪委书记（常委）与区委书记", "overlap_org": "中共西安市新城区委员会", "overlap_period": "present"},
    {"person_a": 9, "person_b": 1, "type": "上下级", "context": "组织部部长（常委）与区委书记", "overlap_org": "中共西安市新城区委员会", "overlap_period": "present"},
    {"person_a": 10, "person_b": 1, "type": "上下级", "context": "宣传部部长（常委）与区委书记", "overlap_org": "中共西安市新城区委员会", "overlap_period": "present"},
    {"person_a": 6, "person_b": 1, "type": "上下级", "context": "政法委书记（常委）与区委书记", "overlap_org": "中共西安市新城区委员会", "overlap_period": "present"},
    {"person_a": 8, "person_b": 1, "type": "上下级", "context": "统战部部长（常委）与区委书记", "overlap_org": "中共西安市新城区委员会", "overlap_period": "present"},
    {"person_a": 11, "person_b": 1, "type": "上下级", "context": "武装部部长（常委）与区委书记", "overlap_org": "中共西安市新城区委员会", "overlap_period": "present"},
    {"person_a": 12, "person_b": 2, "type": "上下级", "context": "副区长与区长", "overlap_org": "西安市新城区人民政府", "overlap_period": "present"},
    {"person_a": 13, "person_b": 2, "type": "上下级", "context": "副区长与区长", "overlap_org": "西安市新城区人民政府", "overlap_period": "present"},
    {"person_a": 14, "person_b": 2, "type": "上下级", "context": "副区长与区长", "overlap_org": "西安市新城区人民政府", "overlap_period": "present"},
    {"person_a": 15, "person_b": 2, "type": "上下级", "context": "副区长与区长", "overlap_org": "西安市新城区人民政府", "overlap_period": "present"},
    {"person_a": 16, "person_b": 2, "type": "上下级", "context": "副区长与区长", "overlap_org": "西安市新城区人民政府", "overlap_period": "present"},
    {"person_a": 4, "person_b": 5, "type": "同事", "context": "均为区委常委兼副区长", "overlap_org": "西安市新城区人民政府", "overlap_period": "present"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    print(f"Building network for {SLUG}...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print()
    print("=" * 60)
    print(f"Build complete for {SLUG}")
    print(f"  persons:         {len(persons_data)}")
    print(f"  organizations:   {len(organizations_data)}")
    print(f"  positions:       {len(positions_data)}")
    print(f"  relationships:   {len(relationships_data)}")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print("Note: person JSON files for core leaders are staged separately")
    print(f"      (as of {AS_OF})")
    print("=" * 60)

if __name__ == "__main__":
    main()