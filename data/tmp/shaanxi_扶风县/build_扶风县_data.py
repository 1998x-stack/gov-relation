#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 扶风县, 宝鸡市, 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_扶风县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - 扶风县人民政府官方网站 (www.fufeng.gov.cn) — 无法连接
  - 百度百科 扶风县条目 — 403 forbidden
  - 澎湃新闻搜索 — 连接超时
  - 宝鸡市开放缺口中确认扶风县领导信息尚未收集

Confidence notes:
  - 因网络搜索全面受阻（扶风县政府网站连接超时、百度百科403、百度搜索不可用），所有数据基于
    已知公共信息构建，置信度受限
  - 县委书记姓名、县长姓名待核实
  - 完整履历、出生年月、籍贯等信息缺失
  - 所有数据标记为unverified
  - 期望在后续调查中补充完善

Fufeng County (扶风县) is located in Baoji City (宝鸡市), Shaanxi Province (陕西省).
"""

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
TMP_MARKER = os.path.sep + "tmp" + os.path.sep
if TMP_MARKER in BASE:
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
elif os.path.basename(BASE).startswith("shaanxi_"):
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
else:
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "扶风县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (县委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 县委书记 — 待查/待核实
    {
        "id": 1,
        "name": "待查_县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共扶风县委员会",
        "source": "扶风县人民政府网站无法连接，需要后续调查确认"
    },

    # 县长 — 待查/待核实
    {
        "id": 2,
        "name": "待查_县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "扶风县人民政府",
        "source": "扶风县人民政府网站无法连接，需要后续调查确认"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Standing Committee of 县委 (县委常委) — 待查
    # ══════════════════════════════════════════════════════════════════════════

    # 县委副书记（通常由县长兼任）
    {
        "id": 3,
        "name": "待查_县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记（通常由县长兼任）",
        "current_org": "中共扶风县委员会",
        "source": "需后续调查确认"
    },

    # 常务副县长
    {
        "id": 4,
        "name": "待查_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "扶风县人民政府",
        "source": "需后续调查确认"
    },

    # 纪委书记
    {
        "id": 5,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共扶风县纪律检查委员会",
        "source": "需后续调查确认"
    },

    # 组织部长
    {
        "id": 6,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共扶风县委组织部",
        "source": "需后续调查确认"
    },

    # 宣传部长
    {
        "id": 7,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共扶风县委宣传部",
        "source": "需后续调查确认"
    },

    # 政法委书记
    {
        "id": 8,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共扶风县委政法委员会",
        "source": "需后续调查确认"
    },

    # 统战部长
    {
        "id": 9,
        "name": "待查_统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共扶风县委统战部",
        "source": "需后续调查确认"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # County Government (县政府) Leadership — 待查
    # ══════════════════════════════════════════════════════════════════════════

    # 副县长 (分管农业/农村)
    {
        "id": 10,
        "name": "待查_副县长（农业农村）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "扶风县人民政府",
        "source": "需后续调查确认"
    },

    # 副县长 (分管教育/卫生)
    {
        "id": 11,
        "name": "待查_副县长（教科文卫）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "扶风县人民政府",
        "source": "需后续调查确认"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # County People's Congress & CPPCC — 待查
    # ══════════════════════════════════════════════════════════════════════════

    # 县人大常委会主任
    {
        "id": 12,
        "name": "待查_人大主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "扶风县人民代表大会常务委员会",
        "source": "需后续调查确认"
    },

    # 县政协主席
    {
        "id": 13,
        "name": "待查_政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议扶风县委员会",
        "source": "需后续调查确认"
    },
]

# ═══════════════════════════════════════════════════════════════════════════════

organizations_data = [
    # 党委系统
    {
        "id": 1,
        "name": "中共扶风县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共宝鸡市委员会",
        "location": "陕西省宝鸡市扶风县"
    },
    {
        "id": 2,
        "name": "中共扶风县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共扶风县委员会",
        "location": "陕西省宝鸡市扶风县"
    },
    {
        "id": 3,
        "name": "中共扶风县委组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共扶风县委员会",
        "location": "陕西省宝鸡市扶风县"
    },
    {
        "id": 4,
        "name": "中共扶风县委宣传部",
        "type": "党委",
        "level": "县",
        "parent": "中共扶风县委员会",
        "location": "陕西省宝鸡市扶风县"
    },
    {
        "id": 5,
        "name": "中共扶风县委政法委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共扶风县委员会",
        "location": "陕西省宝鸡市扶风县"
    },
    {
        "id": 6,
        "name": "中共扶风县委统战部",
        "type": "党委",
        "level": "县",
        "parent": "中共扶风县委员会",
        "location": "陕西省宝鸡市扶风县"
    },

    # 政府系统
    {
        "id": 7,
        "name": "扶风县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "宝鸡市人民政府",
        "location": "陕西省宝鸡市扶风县"
    },

    # 人大/政协
    {
        "id": 8,
        "name": "扶风县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "宝鸡市人民代表大会常务委员会",
        "location": "陕西省宝鸡市扶风县"
    },
    {
        "id": 9,
        "name": "中国人民政治协商会议扶风县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议宝鸡市委员会",
        "location": "陕西省宝鸡市扶风县"
    },

    # 乡镇/街道
    {
        "id": 10,
        "name": "城关街道办事处",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "扶风县人民政府",
        "location": "陕西省宝鸡市扶风县城关街道"
    },
    {
        "id": 11,
        "name": "绛帐镇人民政府",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "扶风县人民政府",
        "location": "陕西省宝鸡市扶风县绛帐镇"
    },
    {
        "id": 12,
        "name": "法门镇人民政府",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "扶风县人民政府",
        "location": "陕西省宝鸡市扶风县法门镇"
    },
    {
        "id": 13,
        "name": "杏林镇人民政府",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "扶风县人民政府",
        "location": "陕西省宝鸡市扶风县杏林镇"
    },
    {
        "id": 14,
        "name": "天度镇人民政府",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "扶风县人民政府",
        "location": "陕西省宝鸡市扶风县天度镇"
    },
    {
        "id": 15,
        "name": "召公镇人民政府",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "扶风县人民政府",
        "location": "陕西省宝鸡市扶风县召公镇"
    },
    {
        "id": 16,
        "name": "午井镇人民政府",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "扶风县人民政府",
        "location": "陕西省宝鸡市扶风县午井镇"
    },
    {
        "id": 17,
        "name": "段家镇人民政府",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "扶风县人民政府",
        "location": "陕西省宝鸡市扶风县段家镇"
    },
]

# ═══════════════════════════════════════════════════════════════════════════════

positions_data = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 县长
    {"person_id": 2, "org_id": 7, "title": "县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 县委副书记（县长兼任）
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": "通常由县长兼任"},
    # 常务副县长
    {"person_id": 4, "org_id": 7, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 纪委书记
    {"person_id": 5, "org_id": 2, "title": "纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 组织部长
    {"person_id": 6, "org_id": 3, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 宣传部长
    {"person_id": 7, "org_id": 4, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 政法委书记
    {"person_id": 8, "org_id": 5, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 统战部长
    {"person_id": 9, "org_id": 6, "title": "统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 副县长（农业农村）
    {"person_id": 10, "org_id": 7, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管农业农村"},
    # 副县长（教科文卫）
    {"person_id": 11, "org_id": 7, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管教育科技文化卫生"},
    # 人大主任
    {"person_id": 12, "org_id": 8, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 政协主席
    {"person_id": 13, "org_id": 9, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
]

# ═══════════════════════════════════════════════════════════════════════════════

relationships_data = [
    # 书记与县长 — 搭班
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "县委书记与县长搭班",
        "overlap_org": "中共扶风县委员会/扶风县人民政府",
        "overlap_period": "待确认",
        "strength": "strong",
        "confidence": "unverified"
    },
    # 书记与人大主任
    {
        "person_a": 1,
        "person_b": 12,
        "type": "overlap",
        "context": "县委书记与县人大常委会主任",
        "overlap_org": "扶风县",
        "overlap_period": "待确认",
        "strength": "medium",
        "confidence": "unverified"
    },
    # 县长与常务副县长
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与常务副县长工作搭档",
        "overlap_org": "扶风县人民政府",
        "overlap_period": "待确认",
        "strength": "strong",
        "confidence": "unverified"
    },
    # 书记与纪委书记
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记与纪委书记（县委班子）",
        "overlap_org": "中共扶风县委员会",
        "overlap_period": "待确认",
        "strength": "medium",
        "confidence": "unverified"
    },
    # 书记与组织部长
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县委书记与组织部部长",
        "overlap_org": "中共扶风县委员会",
        "overlap_period": "待确认",
        "strength": "medium",
        "confidence": "unverified"
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\nDone. Staged artifacts in: {STAGING_DIR}")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    print(f"\nTo promote to canonical paths:")
    print(f"  python3 scripts/process_tmp.py data/tmp/shaanxi_扶风县")
    print(f"  python3 scripts/process_tmp.py data/tmp/shaanxi_扶风县 --apply")

if __name__ == "__main__":
    main()
