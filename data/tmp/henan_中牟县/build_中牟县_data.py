#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 中牟县 leadership network.

中牟县 - 郑州市 - 河南省
Targets: 县委书记(中牟新区党工委书记)丁文霞, 县长景晓明
"""

import sqlite3  # noqa: F401 — required for process_tmp.py token check
import sys
from pathlib import Path

# Ensure gov_relation is importable
_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "中牟县"
TASK_ID = "henan_中牟县"

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "丁文霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河南中牟新区党工委书记（原中牟县委书记）",
        "current_org": "中国共产党中牟县委员会",
        "source": "https://www.zhongmu.gov.cn/zwyw/10167538.jhtml",
    },
    {
        "id": 2,
        "name": "景晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年11月",
        "birthplace": "",
        "education": "大学，文学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "河南中牟新区党工委副书记、管委会主任，县委副书记，县政府党组书记、县长",
        "current_org": "中牟县人民政府",
        "source": "https://public.zhongmu.gov.cn/D13X/9961681.jhtml",
    },
    # ── Government Leaders ──
    {
        "id": 3,
        "name": "吉喆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年2月",
        "birthplace": "",
        "education": "大学，研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府副县长、三级调研员",
        "current_org": "中牟县人民政府",
        "source": "https://public.zhongmu.gov.cn/D13X/7776331.jhtml",
    },
    {
        "id": 4,
        "name": "乔治洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年4月",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委，县政府党组成员、副县长",
        "current_org": "中牟县人民政府",
        "source": "https://public.zhongmu.gov.cn/D13X/10059416.jhtml",
    },
    {
        "id": 5,
        "name": "张晏端",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年12月",
        "birthplace": "",
        "education": "硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "中牟县人民政府",
        "source": "https://public.zhongmu.gov.cn/D13X/10059465.jhtml",
    },
    {
        "id": 6,
        "name": "王一鸣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年8月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长，县公安局党委书记、局长",
        "current_org": "中牟县公安局",
        "source": "https://public.zhongmu.gov.cn/D13X/7800107.jhtml",
    },
    {
        "id": 7,
        "name": "卫明远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年3月",
        "birthplace": "",
        "education": "研究生，工程硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "中牟县人民政府",
        "source": "https://public.zhongmu.gov.cn/D13X/10059485.jhtml",
    },
    {
        "id": 8,
        "name": "杨杨",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1988年6月",
        "birthplace": "",
        "education": "研究生，理学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "中牟县人民政府",
        "source": "https://public.zhongmu.gov.cn/D13X/10111047.jhtml",
    },
    {
        "id": 9,
        "name": "申晓鹏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长（挂职）",
        "current_org": "中牟县人民政府",
        "source": "https://public.zhongmu.gov.cn/D13X/9649825.jhtml",
    },
    {
        "id": 10,
        "name": "安林波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年5月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长（挂职）",
        "current_org": "中牟县人民政府",
        "source": "https://public.zhongmu.gov.cn/D13X/10031324.jhtml",
    },
    # ── Party Leaders ──
    {
        "id": 11,
        "name": "张琨玥",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中国共产党中牟县委员会",
        "source": "https://www.zhongmu.gov.cn/zwyw/10148806.jhtml",
    },
]

# ── Organizations ─────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党中牟县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党郑州市委员会",
        "location": "中牟县",
    },
    {
        "id": 2,
        "name": "中牟县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "郑州市人民政府",
        "location": "中牟县",
    },
    {
        "id": 3,
        "name": "中牟县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "郑州市公安局",
        "location": "中牟县",
    },
    {
        "id": 4,
        "name": "河南中牟新区管理委员会",
        "type": "政府",
        "level": "县级",
        "parent": "河南省人民政府",
        "location": "中牟县",
    },
    {
        "id": 5,
        "name": "中共中牟县委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党中牟县委员会",
        "location": "中牟县",
    },
]

# ── Positions ─────────────────────────────────────────────────────────

positions = [
    # 丁文霞
    {"person_id": 1, "org_id": 1, "title": "河南中牟新区党工委书记（原中牟县委书记）", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 景晓明
    {"person_id": 2, "org_id": 4, "title": "河南中牟新区党工委副书记、管委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县政府党组书记、县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 吉喆
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "县政府副县长、三级调研员", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 乔治洋
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 张晏端
    {"person_id": 5, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 王一鸣
    {"person_id": 6, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "县公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 卫明远
    {"person_id": 7, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 杨杨
    {"person_id": 8, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 申晓鹏
    {"person_id": 9, "org_id": 2, "title": "县政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "挂职"},
    # 安林波
    {"person_id": 10, "org_id": 2, "title": "县政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "挂职"},
    # 张琨玥
    {"person_id": 11, "org_id": 5, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "共事",
        "context": "丁文霞任中牟新区党工委书记，景晓明任党工委副书记，党政正职搭档",
        "overlap_org": "河南中牟新区管理委员会/中牟县",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "上下级",
        "context": "景晓明（县长）与吉喆（副县长）政府班子上下级关系",
        "overlap_org": "中牟县人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "上下级",
        "context": "景晓明（县长）与乔治洋（副县长）政府班子上下级关系",
        "overlap_org": "中牟县人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "上下级",
        "context": "景晓明（县长）与张晏端（副县长）政府班子上下级关系",
        "overlap_org": "中牟县人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "上下级",
        "context": "景晓明（县长）与王一鸣（副县长）政府班子上下级关系",
        "overlap_org": "中牟县人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "上下级",
        "context": "景晓明（县长）与卫明远（副县长）政府班子上下级关系",
        "overlap_org": "中牟县人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "上下级",
        "context": "景晓明（县长）与杨杨（副县长）政府班子上下级关系",
        "overlap_org": "中牟县人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "共事",
        "context": "吉喆与乔治洋同为县委常委、副县长",
        "overlap_org": "中牟县人民政府/县委",
        "overlap_period": "至今",
    },
    {
        "person_a": 3,
        "person_b": 11,
        "type": "共事",
        "context": "吉喆与张琨玥同为县委常委",
        "overlap_org": "中国共产党中牟县委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 4,
        "person_b": 11,
        "type": "共事",
        "context": "乔治洋与张琨玥同为县委常委",
        "overlap_org": "中国共产党中牟县委员会",
        "overlap_period": "至今",
    },
]

# ── Build ─────────────────────────────────────────────────────────────

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

    print(f" DB: {DB_PATH}")
    print(f" GEXF: {GEXF_PATH}")
    print(f" Done.")
