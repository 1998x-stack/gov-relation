#!/usr/bin/env python3
"""丹东市领导班子工作关系网络 - 数据构建脚本"""

import sqlite3
import sys
from pathlib import Path

# Allow running from repo root or staging dir
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent  # data/tmp/liaoning_丹东市/../../../ -> repo root
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

AS_OF = "2026-07-25"
SLUG = "丹东市"

# ── Data ────────────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "蒋冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共丹东市委",
        "source": "https://www.dandong.gov.cn/html/DDSZF/202607/0178485338846086.html",
        "notes": "此前曾任丹东市市长；2026年7月以市委书记身份主持市委常委会",
    },
    {
        "id": 2,
        "name": "张丹",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1977年6月",
        "birthplace": "",
        "education": "研究生学历，理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "丹东市人民政府",
        "source": "https://www.dandong.gov.cn/html/DDSZF/202603/0166668115950642.html",
        "notes": "市委副书记、市长、市政府党组书记；2026年6月更新官方简历",
    },
    {
        "id": 3,
        "name": "黄学利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "丹东市人民政府",
        "source": "https://www.dandong.gov.cn/ddszf/zfxxgk/fdzdgknr/jgjj/index.html",
        "notes": "",
    },
    {
        "id": 4,
        "name": "钱绍勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "丹东市人民政府",
        "source": "https://www.dandong.gov.cn/ddszf/zfxxgk/fdzdgknr/jgjj/index.html",
        "notes": "",
    },
    {
        "id": 5,
        "name": "李海峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "丹东市人民政府",
        "source": "https://www.dandong.gov.cn/ddszf/zfxxgk/fdzdgknr/jgjj/index.html",
        "notes": "",
    },
    {
        "id": 6,
        "name": "欧阳群超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "丹东市人民政府",
        "source": "https://www.dandong.gov.cn/ddszf/zfxxgk/fdzdgknr/jgjj/index.html",
        "notes": "",
    },
    {
        "id": 7,
        "name": "时燕",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "丹东市人民政府",
        "source": "https://www.dandong.gov.cn/ddszf/zfxxgk/fdzdgknr/jgjj/index.html",
        "notes": "",
    },
    {
        "id": 8,
        "name": "迟磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "丹东市人民政府",
        "source": "https://www.dandong.gov.cn/ddszf/zfxxgk/fdzdgknr/jgjj/index.html",
        "notes": "",
    },
    {
        "id": 9,
        "name": "姜春国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "丹东市人民政府",
        "source": "https://www.dandong.gov.cn/ddszf/zfxxgk/fdzdgknr/jgjj/index.html",
        "notes": "",
    },
    {
        "id": 10,
        "name": "冯刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "丹东市人民政府",
        "source": "https://www.dandong.gov.cn/ddszf/zfxxgk/fdzdgknr/jgjj/index.html",
        "notes": "",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共丹东市委",
        "type": "党委",
        "level": "地级市",
        "parent": "中共辽宁省委",
        "location": "辽宁省丹东市",
    },
    {
        "id": 2,
        "name": "丹东市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "辽宁省人民政府",
        "location": "辽宁省丹东市",
    },
]

positions = [
    # 蒋冰 (市委)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正厅级", "note": "2026年7月任现职；此前任丹东市市长"},
    # 张丹 (市政府)
    {"person_id": 2, "org_id": 2, "title": "市长、市委副书记、市政府党组书记", "start": "2026-06", "end": "present", "rank": "正厅级", "note": "2026年6月官方简历更新为市长"},
    # 副市长
    {"person_id": 3, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "市政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "蒋冰任市委书记，张丹任市长，党政正职搭档",
        "overlap_org": "中共丹东市委/丹东市人民政府",
        "overlap_period": "2026年6月至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "蒋冰此前任丹东市市长，张丹接任市长",
        "overlap_org": "丹东市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
]

# ── Paths ───────────────────────────────────────────────────────────────

DB_PATH = SCRIPT_DIR / f"{SLUG}_network.db"
GEXF_PATH = SCRIPT_DIR / f"{SLUG}_network.gexf"

# ── Build ───────────────────────────────────────────────────────────────

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
    print(f"\n✅ Build complete: {SLUG}")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
