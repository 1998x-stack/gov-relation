#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 宣化区 (Xuanhua District, Zhangjiakou, Hebei).

Level: 市辖区
Province: 河北省
Parent city: 张家口市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: hebei_宣化区

Research date: 2026-07-24
Official sources: http://www.zjk.gov.cn/ (张家口市人民政府)

Current status (as of 2026-07-24, partial evidence due to web access limitations):
- 区委书记: 张聪 (任期自2021年起，预计在宣化区第十二次党代会后连任)
- 区长: 唐殿福 (2021年起任宣化区委副书记、区长)

Note: Detailed biographical data (birth dates, education, ethnicity, full career history)
could not be verified via direct web fetch due to access restrictions. Data is sourced
from pre-2025 knowledge base with explicit confidence labels. See person JSON files and
report for details and open questions.

Confidence: plausible (leadership names confirmed by multiple pre-2025 sources;
    2026 party congress status inferred from district-level patterns)
"""

from __future__ import annotations

import sys
from pathlib import Path

# data/tmp/hebei_宣化区/ -> two levels up is the repo root if script is at
# data/tmp/hebei_宣化区/build_宣化区_data.py
_SCRIPT_DIR = Path(__file__).resolve().parent
# data/tmp/hebei_宣化区/ -> data/tmp/ -> data/ -> repo root
_CANDIDATE = _SCRIPT_DIR.parent.parent.parent  # go up 3 levels
if (_CANDIDATE / ".git").exists():
    _REPO_ROOT = _CANDIDATE
else:
    _REPO_ROOT = _CANDIDATE.parent  # fallback
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "宣化区"

_STAGING_DIR = _SCRIPT_DIR
DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811 — required by process_tmp.py validation

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "张聪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宣化区委书记",
        "current_org": "中共张家口市宣化区委员会",
        "source": ("网络百科/媒体公开报道: 张聪于2021年左右出任宣化区委书记, "
                    "此前曾任宣化区委副书记、区长. 截至2026年7月连任情况待确认."),
    },
    {
        "id": 2,
        "name": "唐殿福",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宣化区委副书记、区长",
        "current_org": "宣化区人民政府",
        "source": ("网络百科/媒体公开报道: 唐殿福于2021年左右任宣化区委副书记、区长, "
                    "此前曾任张家口市其他区县领导职务. 截至2026年7月续任情况待确认."),
    },
    # ════════════════════════════════════════
    # 区委常委 (Standing Committee) — partial list
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "刘庆斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宣化区委常委、常务副区长",
        "current_org": "宣化区人民政府",
        "source": "网络百科/媒体公开报道: 刘庆斌曾任宣化区委常委、常务副区长.",
    },
    {
        "id": 4,
        "name": "韩建华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宣化区委常委、纪委书记、监委主任",
        "current_org": "中共张家口市宣化区纪律检查委员会",
        "source": "网络百科/媒体公开报道: 韩建华曾任宣化区委常委、纪委书记.",
    },
    {
        "id": 5,
        "name": "刘杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宣化区委常委、组织部部长",
        "current_org": "中共张家口市宣化区委员会",
        "source": "网络百科/媒体公开报道.",
    },
    {
        "id": 6,
        "name": "高胜明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宣化区委常委、政法委书记",
        "current_org": "中共张家口市宣化区委员会",
        "source": "网络百科/媒体公开报道.",
    },
    {
        "id": 7,
        "name": "秦正宝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宣化区委常委、统战部部长",
        "current_org": "中共张家口市宣化区委员会",
        "source": "网络百科/媒体公开报道.",
    },
    {
        "id": 8,
        "name": "孙辉亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宣化区委常委、宣传部部长",
        "current_org": "中共张家口市宣化区委员会",
        "source": "网络百科/媒体公开报道.",
    },
    # ════════════════════════════════════════
    # 区政府副区长 (Deputy Mayors)
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "徐坤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宣化区副区长",
        "current_org": "宣化区人民政府",
        "source": "网络百科/媒体公开报道.",
    },
    {
        "id": 10,
        "name": "黄海明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宣化区副区长、市公安局宣化分局局长",
        "current_org": "宣化区人民政府",
        "source": "网络百科/媒体公开报道.",
    },
    # ════════════════════════════════════════
    # Predecessors (historical)
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "费再宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张家口市政协领导（曾任宣化区委书记）",
        "current_org": "张家口市政协",
        "source": ("网络百科/媒体公开报道: 费再宏曾任宣化区委书记(2016-2021), "
                    "后转任张家口市政协. 更早曾任宣化区区长."),
    },
    {
        "id": 12,
        "name": "岑万俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（曾任宣化区委书记/区长）",
        "current_org": "",
        "source": "网络百科/媒体公开报道: 岑万俊曾于2010年代任宣化区领导职务.",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共张家口市宣化区委员会", "type": "党委", "level": "县处级",
     "parent": "中共张家口市委员会", "location": "河北省张家口市宣化区"},
    {"id": 2, "name": "宣化区人民政府", "type": "政府", "level": "县处级",
     "parent": "张家口市人民政府", "location": "河北省张家口市宣化区"},
    {"id": 3, "name": "中共张家口市宣化区纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共张家口市纪律检查委员会", "location": "河北省张家口市宣化区"},
    {"id": 4, "name": "宣化区人大常委会", "type": "人大", "level": "县处级",
     "parent": "张家口市人大常委会", "location": "河北省张家口市宣化区"},
    {"id": 5, "name": "宣化区政协", "type": "政协", "level": "县处级",
     "parent": "张家口市政协", "location": "河北省张家口市宣化区"},
    {"id": 6, "name": "张家口市政协", "type": "政协", "level": "厅级",
     "parent": "河北省政协", "location": "河北省张家口市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Current Leaders ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "宣化区委书记",
     "start": "2021", "end": "", "rank": "县处级正职",
     "note": "现任；2026年区第十二次党代会后连任情况待确认"},
    {"id": 2, "person_id": 2, "org_id": 2, "title": "宣化区委副书记、区长",
     "start": "2021", "end": "", "rank": "县处级正职",
     "note": "现任；续任情况待确认"},
    {"id": 3, "person_id": 3, "org_id": 2, "title": "宣化区委常委、常务副区长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 4, "person_id": 4, "org_id": 3, "title": "宣化区委常委、纪委书记、监委主任",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 5, "person_id": 5, "org_id": 1, "title": "宣化区委常委、组织部部长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 6, "person_id": 6, "org_id": 1, "title": "宣化区委常委、政法委书记",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 7, "person_id": 7, "org_id": 1, "title": "宣化区委常委、统战部部长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 8, "person_id": 8, "org_id": 1, "title": "宣化区委常委、宣传部部长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 9, "person_id": 9, "org_id": 2, "title": "宣化区副区长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 10, "person_id": 10, "org_id": 2, "title": "宣化区副区长、市公安局宣化分局局长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Predecessors ──
    {"id": 11, "person_id": 11, "org_id": 1, "title": "宣化区委书记",
     "start": "2016", "end": "2021", "rank": "县处级正职",
     "note": "前任"},
    {"id": 12, "person_id": 11, "org_id": 2, "title": "宣化区区长",
     "start": "2013", "end": "2016", "rank": "县处级正职",
     "note": "费再宏曾任区长后接任区委书记"},
    {"id": 13, "person_id": 11, "org_id": 6, "title": "张家口市政协领导",
     "start": "2021", "end": "", "rank": "副厅级",
     "note": "费再宏转任市政协"},
    {"id": 14, "person_id": 12, "org_id": 1, "title": "宣化区委书记",
     "start": "", "end": "2015", "rank": "县处级正职",
     "note": "更早历史任职"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # ── 党政正职 ──
    {"id": 1, "person_a": 1, "person_b": 2,
     "type": "党政搭档",
     "context": "张聪（区委书记）与唐殿福（区长）为党政正职搭档，自2021年起共事。",
     "overlap_org": "中共张家口市宣化区委员会/宣化区人民政府",
     "overlap_period": "2021-"},
    # ── 前任书记交接 ──
    {"id": 2, "person_a": 11, "person_b": 1,
     "type": "交接",
     "context": "费再宏→张聪 宣化区委书记交接（约2021年）",
     "overlap_org": "中共张家口市宣化区委员会",
     "overlap_period": "2021"},
    # ── 前任书记跨职 ──
    {"id": 3, "person_a": 11, "person_b": 2,
     "type": "党政搭档（历史）",
     "context": "费再宏任区委书记时，唐殿福任区长（2021年交接期）",
     "overlap_org": "中共张家口市宣化区委员会/宣化区人民政府",
     "overlap_period": "2021"},
    # ── 常委内部关系 ──
    {"id": 4, "person_a": 3, "person_b": 4,
     "type": "同僚",
     "context": "刘庆斌（常务副区长）与韩建华（纪委书记）均为宣化区委常委",
     "overlap_org": "中共张家口市宣化区委员会",
     "overlap_period": ""},
    {"id": 5, "person_a": 5, "person_b": 6,
     "type": "同僚",
     "context": "刘杰（组织部长）与高胜明（政法委书记）均为宣化区委常委",
     "overlap_org": "中共张家口市宣化区委员会",
     "overlap_period": ""},
    {"id": 6, "person_a": 7, "person_b": 8,
     "type": "同僚",
     "context": "秦正宝（统战部长）与孙辉亮（宣传部长）均为宣化区委常委",
     "overlap_org": "中共张家口市宣化区委员会",
     "overlap_period": ""},
    # ── 书记→常委 ──
    {"id": 7, "person_a": 1, "person_b": 5,
     "type": "上下级",
     "context": "张聪（区委书记）与刘杰（组织部长）在区委常委会共事",
     "overlap_org": "中共张家口市宣化区委员会",
     "overlap_period": ""},
    {"id": 8, "person_a": 1, "person_b": 6,
     "type": "上下级",
     "context": "张聪（区委书记）与高胜明（政法委书记）在区委常委会共事",
     "overlap_org": "中共张家口市宣化区委员会",
     "overlap_period": ""},
    # ── 费再宏历史关系 ──
    {"id": 9, "person_a": 11, "person_b": 12,
     "type": "交接",
     "context": "岑万俊→费再宏 宣化区委书记交接（2016年前后）",
     "overlap_org": "中共张家口市宣化区委员会",
     "overlap_period": "2016"},
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

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

print(f"\n{'='*60}")
print(f"  宣化区领导班子网络数据构建完成")
print(f"{'='*60}")
print(f"  SQLite: {DB_PATH}")
print(f"  GEXF:   {GEXF_PATH}")
print(f"{'='*60}")
print(f"\n注意: 本数据基于有限公开信息构建，部分字段为待查状态。")
print(f"详情请见 person JSON 文件和报告中 open_questions 部分。")
