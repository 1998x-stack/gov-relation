#!/usr/bin/env python3
"""黄冈市黄州区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区
调查日期: 2026-07-24
信息来源: 黄州区人民政府网站 (huangzhou.gov.cn), 黄冈市人民政府网站 (hg.gov.cn)
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Ensure gov_relation package is importable
_repo_root = Path(__file__).resolve().parents[2]  # data/tmp/hubei_黄州区/ -> .. -> repo root
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "黄州区"
TODAY = "2026-07-24"
STAGING = Path(__file__).resolve().parent

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"


def org_id(base: int) -> int:
    """Offset org IDs into the 100000+ range per runner convention."""
    return base + 100000


# ── Persons ──────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee, 2xxx = government, 3xxx = other

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 黄芳帅 — 区委书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1001,
        "name": "黄芳帅",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区委书记",
        "current_org": "中共黄州区委",
        "source": "huangzhou.gov.cn official news (2026-01, 2026-02)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 陈风 — 区委副书记、区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "陈风",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区委副书记、区长",
        "current_org": "黄州区人民政府",
        "source": "huangzhou.gov.cn leadership page",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 童承志 — 区委副书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1003,
        "name": "童承志",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区委副书记",
        "current_org": "中共黄州区委",
        "source": "huangzhou.gov.cn official news (2026-02-06)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. 何志春 — 区人大常委会主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1004,
        "name": "何志春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区人大常委会主任",
        "current_org": "黄州区人大常委会",
        "source": "huangzhou.gov.cn official news (2026-01, 2026-02)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 5. 陈青 — 区政协主席
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1005,
        "name": "陈青",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区政协主席",
        "current_org": "黄州区政协",
        "source": "huangzhou.gov.cn official news (2026-01, 2026-02)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 6. 陈威 — 区委常委、常务副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1006,
        "name": "陈威",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区委常委、区政府常务副区长",
        "current_org": "黄州区人民政府",
        "source": "huangzhou.gov.cn official news (2026-01-19, 2026-02-03)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 7. 李银飞 — 区委常委、组织部部长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1007,
        "name": "李银飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区委常委、组织部部长",
        "current_org": "中共黄州区委组织部",
        "source": "huangzhou.gov.cn official news (2026-02-06)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 8. 涂薇 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1008,
        "name": "涂薇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区委常委",
        "current_org": "中共黄州区委",
        "source": "huangzhou.gov.cn official news (2026-02-03)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 9. 赵海刚 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1009,
        "name": "赵海刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区委常委",
        "current_org": "中共黄州区委",
        "source": "huangzhou.gov.cn official news (2026-02-03)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 10. 曹幼松 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1010,
        "name": "曹幼松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区委常委",
        "current_org": "中共黄州区委",
        "source": "huangzhou.gov.cn official news (2026-02-03)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 11. 郭薇 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1011,
        "name": "郭薇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区委常委",
        "current_org": "中共黄州区委",
        "source": "huangzhou.gov.cn official news (2026-02-03)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 12. 蔡宁 — 副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1012,
        "name": "蔡宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区副区长",
        "current_org": "黄州区人民政府",
        "source": "huangzhou.gov.cn official news (2026-01-19)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 13. 胡刚 — 提名副区长、黄州公安分局局长（2026-07）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1013,
        "name": "胡刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区提名副区长、市公安局黄州分局局长",
        "current_org": "黄州区人民政府",
        "source": "huangzhou.gov.cn official news (2026-07-15)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 14. 王立三 — 区政协党组副书记、副主席
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1014,
        "name": "王立三",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区政协党组副书记、副主席",
        "current_org": "黄州区政协",
        "source": "huangzhou.gov.cn official news (2026-01-21)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 15. 许春梅 — 区政协副主席
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1015,
        "name": "许春梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区政协副主席",
        "current_org": "黄州区政协",
        "source": "huangzhou.gov.cn official news (2026-01-21)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 16. 邓建军 — 区政协副主席
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1016,
        "name": "邓建军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区政协副主席",
        "current_org": "黄州区政协",
        "source": "huangzhou.gov.cn official news (2026-01-21)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 17. 胡晓辉 — 区政协副主席
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1017,
        "name": "胡晓辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区政协副主席",
        "current_org": "黄州区政协",
        "source": "huangzhou.gov.cn official news (2026-01-21)",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 18. 杨小晖 — 区政协副主席
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1018,
        "name": "杨小晖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄州区政协副主席",
        "current_org": "黄州区政协",
        "source": "huangzhou.gov.cn official news (2026-01-21)",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共黄州区委", "type": "党委", "level": "县处级", "parent": "中共黄冈市委", "location": "黄冈市黄州区"},
    {"id": 2, "name": "黄州区人民政府", "type": "政府", "level": "县处级", "parent": "黄冈市人民政府", "location": "黄冈市黄州区"},
    {"id": 3, "name": "黄州区人大常委会", "type": "人大", "level": "县处级", "parent": "黄州区", "location": "黄冈市黄州区"},
    {"id": 4, "name": "黄州区政协", "type": "政协", "level": "县处级", "parent": "黄州区", "location": "黄冈市黄州区"},
    {"id": 5, "name": "中共黄州区委组织部", "type": "党委部门", "level": "乡科级", "parent": "中共黄州区委", "location": "黄冈市黄州区"},
    {"id": 6, "name": "黄州区纪委监委", "type": "纪委", "level": "县处级", "parent": "中共黄州区委", "location": "黄冈市黄州区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 黄芳帅
    {"person_id": 1001, "org_id": org_id(1), "title": "黄州区委书记", "start_date": "未知", "end_date": "present",
     "rank": "县处级正职", "note": "区委一把手"},
    # 陈风
    {"person_id": 1002, "org_id": org_id(1), "title": "黄州区委副书记", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 1002, "org_id": org_id(2), "title": "黄州区区长", "start_date": "未知", "end_date": "present",
     "rank": "县处级正职", "note": "区政府一把手"},
    # 童承志
    {"person_id": 1003, "org_id": org_id(1), "title": "黄州区委副书记", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # 何志春
    {"person_id": 1004, "org_id": org_id(3), "title": "黄州区人大常委会主任", "start_date": "未知", "end_date": "present",
     "rank": "县处级正职", "note": ""},
    # 陈青
    {"person_id": 1005, "org_id": org_id(4), "title": "黄州区政协主席", "start_date": "未知", "end_date": "present",
     "rank": "县处级正职", "note": ""},
    # 陈威
    {"person_id": 1006, "org_id": org_id(1), "title": "黄州区委常委", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 1006, "org_id": org_id(2), "title": "黄州区常务副区长", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # 李银飞
    {"person_id": 1007, "org_id": org_id(5), "title": "黄州区委组织部部长", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": "区委常委兼任"},
    # 涂薇
    {"person_id": 1008, "org_id": org_id(1), "title": "黄州区委常委", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # 赵海刚
    {"person_id": 1009, "org_id": org_id(1), "title": "黄州区委常委", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # 曹幼松
    {"person_id": 1010, "org_id": org_id(1), "title": "黄州区委常委", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # 郭薇
    {"person_id": 1011, "org_id": org_id(1), "title": "黄州区委常委", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # 蔡宁
    {"person_id": 1012, "org_id": org_id(2), "title": "黄州区副区长", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # 胡刚
    {"person_id": 1013, "org_id": org_id(2), "title": "黄州区提名副区长、公安分局局长", "start_date": "2026-07", "end_date": "present",
     "rank": "县处级副职", "note": "2026年7月提名副区长"},
    # 王立三
    {"person_id": 1014, "org_id": org_id(4), "title": "黄州区政协副主席", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": "党组副书记"},
    # 许春梅
    {"person_id": 1015, "org_id": org_id(4), "title": "黄州区政协副主席", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # 邓建军
    {"person_id": 1016, "org_id": org_id(4), "title": "黄州区政协副主席", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # 胡晓辉
    {"person_id": 1017, "org_id": org_id(4), "title": "黄州区政协副主席", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # 杨小晖
    {"person_id": 1018, "org_id": org_id(4), "title": "黄州区政协副主席", "start_date": "未知", "end_date": "present",
     "rank": "县处级副职", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 黄芳帅 - 陈风：书记+区长搭档
    {"person_a": 1001, "person_b": 1002, "type": "overlap",
     "context": "区委书记与区长党政搭档",
     "overlap_org": "黄州区委/区政府", "overlap_period": "当前"},
    # 黄芳帅 - 童承志：书记+副书记
    {"person_a": 1001, "person_b": 1003, "type": "overlap",
     "context": "区委书记与专职副书记",
     "overlap_org": "中共黄州区委", "overlap_period": "当前"},
    # 陈风 - 陈威：区长+常务副区长
    {"person_a": 1002, "person_b": 1006, "type": "overlap",
     "context": "区长与常务副区长",
     "overlap_org": "黄州区人民政府", "overlap_period": "当前"},
    # 黄芳帅 - 何志春：区委书记+人大主任
    {"person_a": 1001, "person_b": 1004, "type": "overlap",
     "context": "区委书记与人大常委会主任",
     "overlap_org": "黄州区四套班子", "overlap_period": "当前"},
    # 陈风 - 陈青：区长+政协主席
    {"person_a": 1002, "person_b": 1005, "type": "overlap",
     "context": "区长与政协主席",
     "overlap_org": "黄州区四套班子", "overlap_period": "当前"},
    # 黄芳帅 - 李银飞：书记+组织部长
    {"person_a": 1001, "person_b": 1007, "type": "overlap",
     "context": "区委书记与组织部部长（干部人事关键关系）",
     "overlap_org": "中共黄州区委", "overlap_period": "当前"},
    # 黄芳帅 - 陈威：书记+常务副区长
    {"person_a": 1001, "person_b": 1006, "type": "overlap",
     "context": "区委书记与常务副区长",
     "overlap_org": "黄州区委", "overlap_period": "当前"},
    # 黄芳帅 - 涂薇：区委常委班子
    {"person_a": 1001, "person_b": 1008, "type": "overlap",
     "context": "区委常委会共同工作",
     "overlap_org": "中共黄州区委", "overlap_period": "当前"},
    # 黄芳帅 - 赵海刚：区委常委班子
    {"person_a": 1001, "person_b": 1009, "type": "overlap",
     "context": "区委常委会共同工作",
     "overlap_org": "中共黄州区委", "overlap_period": "当前"},
    # 黄芳帅 - 曹幼松：区委常委班子
    {"person_a": 1001, "person_b": 1010, "type": "overlap",
     "context": "区委常委会共同工作",
     "overlap_org": "中共黄州区委", "overlap_period": "当前"},
    # 黄芳帅 - 郭薇：区委常委班子
    {"person_a": 1001, "person_b": 1011, "type": "overlap",
     "context": "区委常委会共同工作",
     "overlap_org": "中共黄州区委", "overlap_period": "当前"},
    # 陈风 - 蔡宁：区长+副区长
    {"person_a": 1002, "person_b": 1012, "type": "overlap",
     "context": "区长与副区长",
     "overlap_org": "黄州区人民政府", "overlap_period": "当前"},
    # 陈风 - 胡刚：区长+公安分局局长
    {"person_a": 1002, "person_b": 1013, "type": "overlap",
     "context": "区长与公安分局局长（政府班子成员）",
     "overlap_org": "黄州区人民政府", "overlap_period": "当前"},
]

# ── Build ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"=== 构建黄州区领导班子关系网络 ===")
    print(f"人员: {len(persons)} 人")
    print(f"机构: {len(organizations)} 个")
    print(f"任职: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

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

    print(f"\n数据库: {DB_PATH}")
    print(f"图文件: {GEXF_PATH}")
    print("=== 构建完成 ===")
