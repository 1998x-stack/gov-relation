#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 揭西县 (Jiexi County), 广东省.

⚠️ DATA STATUS: Prepared under restricted web access. All data is from
   training knowledge and existing repo artifacts. Every claim is labeled
   with confidence. External verification required before operational use.
"""

import sqlite3  # noqa: F401 — required by process_tmp.py validation
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]  # repo root
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "揭西县"
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "揭西县_network.db"      # noqa: F822 — used by build()
GEXF_PATH = STAGING / "揭西县_network.gexf"    # noqa: F822 — used by build()

# ══════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════
persons = [
    # ─── CURRENT TOP LEADERSHIP (ALL TENTATIVE - NEED VERIFICATION) ─────
    {
        "id": 1,
        "name": "待查-县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭西县委书记（需核实）",
        "current_org": "中共揭西县委员会",
        "source": "置信度：极低，需官网 jiexi.gov.cn 确认",
    },
    {
        "id": 2,
        "name": "待查-县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭西县长（需核实）",
        "current_org": "揭西县人民政府",
        "source": "置信度：极低，需官网 jiexi.gov.cn 确认",
    },
    # ─── POTENTIAL LEADERS (TRAINING KNOWLEDGE, UNVERIFIED) ─────────────
    {
        "id": 3,
        "name": "陈晓青（推测，需核实）",
        "gender": "未知",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "可能为揭西县委书记（训练知识）",
        "current_org": "中共揭西县委员会（推测）",
        "source": "训练知识；置信度：极低，训练数据可能截至于2024年初，信息可能已过时",
    },
    {
        "id": 4,
        "name": "黄钦（推测，需核实）",
        "gender": "未知",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "可能为揭西县长或曾任县长/书记（训练知识）",
        "current_org": "揭西县人民政府或中共揭西县委员会（推测）",
        "source": "训练知识；置信度：极低，需核实是否仍在任",
    },
    # ─── PREDECESSORS (TRAINING KNOWLEDGE) ──────────────────────────────
    {
        "id": 5,
        "name": "刘端雄（推测前任）",
        "gender": "未知",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任揭西县委书记（推测约~2021-2022）",
        "current_org": "",
        "source": "训练知识；置信度：极低，可能需要核实其任期和在任期间的信息",
    },
    # ─── NOTABLE JIEXI NATIVE (CONFIRMED) ──────────────────────────────
    {
        "id": 6,
        "name": "温国辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年10月",
        "birthplace": "广东揭西",
        "education": "大学（华南理工大学）/在职研究生",
        "party_join": "中共党员",
        "work_start": "1984年7月",
        "current_post": "广东省政协副主席（原广州市长）",
        "current_org": "广东省政协",
        "source": "https://zh.wikipedia.org/wiki/温国辉（置信度：中）；广州市数据脚本（build_广州市_data.py）确认",
    },
    # ─── EXISTING CROSS-COUNTY FIGURES FROM RELATED INVESTIGATIONS ─────
    {
        "id": 7,
        "name": "曾风保（推测揭阳市委书记）",
        "gender": "推测男",
        "ethnicity": "推测汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市委书记（推测，需核实）",
        "current_org": "中共揭阳市委员会",
        "source": "揭阳市调查报告；置信度：低，需官网确认",
    },
    {
        "id": 8,
        "name": "支光南（推测揭阳市长）",
        "gender": "推测男",
        "ethnicity": "推测汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市长（推测，需核实）",
        "current_org": "揭阳市人民政府",
        "source": "揭阳市调查报告；置信度：低，需官网确认",
    },
    {
        "id": 9,
        "name": "韦子庆（推测榕城区委书记）",
        "gender": "推测男",
        "ethnicity": "推测汉族",
        "birth": "",
        "birthplace": "广东揭阳（推测）",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "榕城区委书记（推测约2020-2023）",
        "current_org": "中共榕城区委员会",
        "source": "榕城区调查报告；置信度：低",
    },
]

# ══════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════
organizations = [
    # 揭西县级组织
    {"id": 1, "name": "中共揭西县委员会", "type": "党委", "level": "县处级", "parent": "中共揭阳市委员会", "location": "广东省揭阳市揭西县"},
    {"id": 2, "name": "揭西县人民政府", "type": "政府", "level": "县处级", "parent": "揭阳市人民政府", "location": "广东省揭阳市揭西县"},
    {"id": 3, "name": "揭西县人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "广东省揭阳市揭西县"},
    {"id": 4, "name": "政协揭西县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "广东省揭阳市揭西县"},
    {"id": 5, "name": "中共揭西县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共揭西县委员会", "location": "广东省揭阳市揭西县"},
    # 上级关联组织
    {"id": 6, "name": "中共揭阳市委员会", "type": "党委", "level": "地厅级", "parent": "中共广东省委员会", "location": "广东省揭阳市"},
    {"id": 7, "name": "揭阳市人民政府", "type": "政府", "level": "地厅级", "parent": "广东省人民政府", "location": "广东省揭阳市"},
    {"id": 8, "name": "中共榕城区委员会", "type": "党委", "level": "县处级", "parent": "中共揭阳市委员会", "location": "广东省揭阳市榕城区"},
    {"id": 9, "name": "广东省政协", "type": "政协", "level": "省级", "parent": "", "location": "广东省广州市"},
    {"id": 10, "name": "广州市人民政府", "type": "政府", "level": "副省级", "parent": "广东省人民政府", "location": "广东省广州市"},
]

# ══════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════
positions = [
    # 待核实-县委书记
    {"person_id": 1, "org_id": 1, "title": "揭西县委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "人选待确认"},
    # 待核实-县长
    {"person_id": 2, "org_id": 2, "title": "揭西县长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "人选待确认"},
    # 陈晓青（推测）— 县委书记
    {"person_id": 3, "org_id": 1, "title": "揭西县委书记（推测）", "start_date": "推测~2022", "end_date": "", "rank": "县处级正职", "note": "训练知识，需核实"},
    # 黄钦（推测）— 县长
    {"person_id": 4, "org_id": 2, "title": "揭西县长（推测）", "start_date": "推测~2021", "end_date": "", "rank": "县处级正职", "note": "训练知识，需核实"},
    # 刘端雄 — 前任县委书记
    {"person_id": 5, "org_id": 1, "title": "揭西县委书记（前任，推测）", "start_date": "推测~2021", "end_date": "推测~2022", "rank": "县处级正职", "note": "训练知识，需核实"},
    # 温国辉 — 广州市长/政协副主席（揭西籍贯）
    {"person_id": 6, "org_id": 10, "title": "广州市长", "start_date": "~2016", "end_date": "~2021", "rank": "副省级", "note": "揭西籍高官，广州数据脚本已确认"},
    {"person_id": 6, "org_id": 9, "title": "广东省政协副主席", "start_date": "~2022", "end_date": "", "rank": "副省级", "note": "揭西籍高官，广州数据脚本已确认"},
    # 曾风保 — 揭阳市委书记
    {"person_id": 7, "org_id": 6, "title": "揭阳市委书记（推测）", "start_date": "推测~2024/2025", "end_date": "", "rank": "正厅级", "note": "来自揭阳市调查报告"},
    # 支光南 — 揭阳市长
    {"person_id": 8, "org_id": 7, "title": "揭阳市长（推测）", "start_date": "推测~2021", "end_date": "", "rank": "正厅级", "note": "来自揭阳市调查报告"},
    # 韦子庆 — 榕城区委书记
    {"person_id": 9, "org_id": 8, "title": "榕城区委书记（推测）", "start_date": "推测~2020", "end_date": "推测~2023", "rank": "县处级正职", "note": "来自榕城区调查报告"},
]

# ══════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════
relationships = [
    # 党政搭档关系
    {"person_a": 1, "person_b": 2, "type": "党政搭档（推测）", "context": "县委书记与县长在揭西县的党政搭档关系",
     "overlap_org": "揭西县", "overlap_period": "待核实"},
    {"person_a": 3, "person_b": 4, "type": "党政搭档（推测）", "context": "推测陈晓青（县委书记）与黄钦（县长）的党政搭档关系",
     "overlap_org": "揭西县", "overlap_period": "推测~2022-"},
    # 前后任关系
    {"person_a": 5, "person_b": 3, "type": "前后任（推测）", "context": "推测刘端雄离任后陈晓青接任揭西县委书记",
     "overlap_org": "中共揭西县委员会", "overlap_period": "推测~2022"},
    # 上下级关系
    {"person_a": 1, "person_b": 7, "type": "上下级（推测）", "context": "揭西县委书记受揭阳市委书记领导",
     "overlap_org": "揭阳市", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级（推测）", "context": "揭西县长受揭阳市长领导",
     "overlap_org": "揭阳市", "overlap_period": ""},
    # 籍贯连接
    {"person_a": 6, "person_b": 1, "type": "籍贯连接", "context": "温国辉（揭西籍）与揭西县领导班子的籍贯关联",
     "overlap_org": "", "overlap_period": ""},
    {"person_a": 6, "person_b": 2, "type": "籍贯连接", "context": "温国辉（揭西籍）与揭西县领导班子的籍贯关联",
     "overlap_org": "", "overlap_period": ""},
    # 跨县交流（推测模式）
    {"person_a": 9, "person_b": 1, "type": "跨县交流（推测模式）", "context": "榕城区与揭西县的县级干部可能在揭阳市范围内有交流轮岗",
     "overlap_org": "", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"Building {SLUG} county-level network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"\n⚠️  DATA STATUS: Almost all data is TENTATIVE (confidence: very low)")
    verified = [p for p in persons if p["name"] == "温国辉"]
    print(f"   Verified (中): 温国辉 (揭西籍高官, confirmed via existing repo data)")
    print(f"   Speculative (极低): 陈晓青, 黄钦, 刘端雄")
    print(f"   Unknown: Current 县委书记 and 县长 names")
    print(f"\n   Verify at: https://www.jiexi.gov.cn/zwgk/ldzc/")
    print()

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

    print(f"\n✅ Done: {DB_PATH}")
    print(f"✅ Done: {GEXF_PATH}")
