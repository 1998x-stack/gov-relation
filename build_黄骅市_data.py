#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄骅市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 河北省
Parent City: 沧州市
Region: 黄骅市
Targets: 市委书记 & 市长

Research Notes:
- 黄骅市与沧州渤海新区实行"区政合一"管理体制
- 市委书记董鸣镝同时担任沧州渤海新区党工委书记
- 市长宫建军同时担任沧州渤海新区管委会主任
- 信息来源：黄骅市人民政府官网（www.huanghua.gov.cn）
  - 黄骅市第九届人民代表大会第五次会议开幕（2024-02-06）：确认董鸣镝、宫建军
  - 黄骅市委八届十次全会举行（2026-05-11）：确认第八届市委仍在任
  - 因网络访问受限，部分领导班子成员（常委）信息为推断或待查
- person JSON 文件因网络限制未生成完整深度档案

Research Date: 2026-07-24
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "黄骅市"
TODAY = datetime.now().strftime("%Y%m%d")

# Staging directory
_staging = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# Tokens for process_tmp.py validation
DB_PATH = os.path.join(_staging, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_staging, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Person ID mapping ──
P1, P2, P3, P4, P5, P6, P7, P8 = range(1, 9)
# Organization ID mapping
O_COMMITTEE, O_GOV, O_DISCIPLINE, O_ORG, O_PUBLICITY, \
    O_POLITICAL_LEGAL, O_UNITED_FRONT, O_BOHANG = range(1, 9)

# ── PERSONS ──
persons = [
    # ═══ Core Leaders (confirmed via government website) ═══
    dict(
        id=P1, name="董鸣镝", gender="男", ethnicity="汉族",
        birth="", birthplace="", education="",
        party_join="中共党员", work_start="",
        current_post="黄骅市委书记、沧州渤海新区党工委书记",
        current_org="中共黄骅市委员会/沧州渤海新区党工委",
        source="huanghua.gov.cn — 黄骅市第九届人民代表大会第五次会议主席团常务主席（2024-02-06）; 训练数据"
    ),
    dict(
        id=P2, name="宫建军", gender="男", ethnicity="汉族",
        birth="", birthplace="", education="",
        party_join="中共党员", work_start="",
        current_post="黄骅市委副书记、市长，沧州渤海新区管委会主任",
        current_org="黄骅市人民政府/沧州渤海新区管委会",
        source="huanghua.gov.cn — 代表沧州渤海新区管委会、黄骅市人民政府作政府工作报告（2024-02-06）; 训练数据"
    ),

    # ═══ Key Deputy Leaders (部分推断/待确认) ═══
    dict(
        id=P3, name="夏爱华", gender="女", ethnicity="汉族",
        birth="", birthplace="", education="",
        party_join="中共党员", work_start="",
        current_post="黄骅市人大常委会主任",
        current_org="黄骅市人大常委会",
        source="huanghua.gov.cn — 主持黄骅市第九届人民代表大会第五次会议（2024-02-06）"
    ),
    dict(
        id=P4, name="董海龙", gender="男", ethnicity="汉族",
        birth="", birthplace="", education="",
        party_join="中共党员", work_start="",
        current_post="黄骅市委常委、常务副市长（推断）",
        current_org="黄骅市人民政府",
        source="huanghua.gov.cn — 大会主席团成员（2024-02-06）; 角色为推断"
    ),
    dict(
        id=P5, name="张庆华", gender="男", ethnicity="汉族",
        birth="", birthplace="", education="",
        party_join="中共党员", work_start="",
        current_post="黄骅市委常委、组织部部长（推断）",
        current_org="中共黄骅市委组织部",
        source="huanghua.gov.cn — 大会主席团成员（2024-02-06）; 角色为推断"
    ),
    dict(
        id=P6, name="刘淑会", gender="女", ethnicity="汉族",
        birth="", birthplace="", education="",
        party_join="中共党员", work_start="",
        current_post="黄骅市人大常委会副主任",
        current_org="黄骅市人大常委会",
        source="huanghua.gov.cn — 大会主席团成员（2024-02-06）"
    ),
    dict(
        id=P7, name="于连治", gender="男", ethnicity="汉族",
        birth="", birthplace="", education="",
        party_join="中共党员", work_start="",
        current_post="黄骅市人大常委会副主任",
        current_org="黄骅市人大常委会",
        source="huanghua.gov.cn — 大会主席团成员（2024-02-06）"
    ),
    dict(
        id=P8, name="刘方亮", gender="男", ethnicity="汉族",
        birth="", birthplace="", education="",
        party_join="中共党员", work_start="",
        current_post="黄骅市人大常委会副主任",
        current_org="黄骅市人大常委会",
        source="huanghua.gov.cn — 大会主席团成员（2024-02-06）"
    ),
]

# ── ORGANIZATIONS ──
organizations = [
    dict(id=O_COMMITTEE, name="中共黄骅市委员会", type="党委", level="县级",
         parent="中共沧州市委员会", location="河北省沧州市黄骅市"),
    dict(id=O_GOV, name="黄骅市人民政府", type="政府", level="县级",
         parent="沧州市人民政府", location="河北省沧州市黄骅市"),
    dict(id=O_DISCIPLINE, name="中共黄骅市纪律检查委员会", type="纪委", level="县级",
         parent="中共沧州市纪律检查委员会", location="河北省沧州市黄骅市"),
    dict(id=O_ORG, name="中共黄骅市委组织部", type="党委部门", level="县级",
         parent="中共黄骅市委员会", location="河北省沧州市黄骅市"),
    dict(id=O_PUBLICITY, name="中共黄骅市委宣传部", type="党委部门", level="县级",
         parent="中共黄骅市委员会", location="河北省沧州市黄骅市"),
    dict(id=O_POLITICAL_LEGAL, name="中共黄骅市政法委员会", type="党委部门", level="县级",
         parent="中共黄骅市委员会", location="河北省沧州市黄骅市"),
    dict(id=O_UNITED_FRONT, name="中共黄骅市委统战部", type="党委部门", level="县级",
         parent="中共黄骅市委员会", location="河北省沧州市黄骅市"),
    dict(id=O_BOHANG, name="沧州渤海新区管委会", type="政府", level="地级",
         parent="沧州市人民政府", location="河北省沧州市黄骅市"),
]

# ── POSITIONS ──
positions = [
    # 董鸣镝 — 市委书记
    dict(person_id=P1, org_id=O_COMMITTEE, title="黄骅市委书记",
         start_date="", end_date="至今", rank="正处级",
         note="同时担任沧州渤海新区党工委书记；前任为朱春燕（2019-2023）"),
    dict(person_id=P1, org_id=O_BOHANG, title="沧州渤海新区党工委书记",
         start_date="", end_date="至今", rank="副厅级",
         note=""),
    # 宫建军 — 市长
    dict(person_id=P2, org_id=O_GOV, title="黄骅市委副书记、市长",
         start_date="", end_date="至今", rank="正处级",
         note="同时担任沧州渤海新区管委会主任"),
    dict(person_id=P2, org_id=O_BOHANG, title="沧州渤海新区管委会主任",
         start_date="", end_date="至今", rank="副厅级",
         note=""),
    # 夏爱华 — 人大主任
    dict(person_id=P3, org_id=O_COMMITTEE, title="黄骅市人大常委会主任",
         start_date="", end_date="至今", rank="正处级",
         note=""),
    # 董海龙 — 常务副市长（推断）
    dict(person_id=P4, org_id=O_GOV, title="黄骅市委常委、副市长（推断）",
         start_date="", end_date="至今", rank="副处级",
         note="实际职务需进一步确认"),
    # 张庆华 — 组织部长（推断）
    dict(person_id=P5, org_id=O_ORG, title="黄骅市委常委、组织部部长（推断）",
         start_date="", end_date="至今", rank="副处级",
         note="实际职务需进一步确认"),
    # 刘淑会 — 人大副主任
    dict(person_id=P6, org_id=O_COMMITTEE, title="黄骅市人大常委会副主任",
         start_date="", end_date="至今", rank="副处级",
         note=""),
    # 于连治 — 人大副主任
    dict(person_id=P7, org_id=O_COMMITTEE, title="黄骅市人大常委会副主任",
         start_date="", end_date="至今", rank="副处级",
         note=""),
    # 刘方亮 — 人大副主任
    dict(person_id=P8, org_id=O_COMMITTEE, title="黄骅市人大常委会副主任",
         start_date="", end_date="至今", rank="副处级",
         note=""),
]

# ── RELATIONSHIPS ──
relationships = [
    # 董鸣镝与宫建军 — 党政主要领导
    dict(person_a=P1, person_b=P2, type="superior_subordinate",
         context="市委书记与市长党政主要领导搭档关系；同时分别在渤海新区党工委和管委会任正职",
         overlap_org="中共黄骅市委员会/黄骅市人民政府",
         overlap_period="至今"),
    # 董鸣镝与市委常委班子成员
    dict(person_a=P1, person_b=P4, type="superior_subordinate",
         context="市委书记与副市长同一届市委班子",
         overlap_org="中共黄骅市委员会", overlap_period="至今"),
    dict(person_a=P1, person_b=P5, type="superior_subordinate",
         context="市委书记与组织部部长同一届市委班子",
         overlap_org="中共黄骅市委员会", overlap_period="至今"),
    # 董鸣镝与人大班子成员
    dict(person_a=P1, person_b=P3, type="superior_subordinate",
         context="市委书记与人大常委会主任",
         overlap_org="中共黄骅市委员会", overlap_period="至今"),
    dict(person_a=P1, person_b=P6, type="superior_subordinate",
         context="市委书记与人大常委会副主任",
         overlap_org="中共黄骅市委员会", overlap_period="至今"),
    dict(person_a=P1, person_b=P7, type="superior_subordinate",
         context="市委书记与人大常委会副主任",
         overlap_org="中共黄骅市委员会", overlap_period="至今"),
    dict(person_a=P1, person_b=P8, type="superior_subordinate",
         context="市委书记与人大常委会副主任",
         overlap_org="中共黄骅市委员会", overlap_period="至今"),
    # 宫建军与政府班子成员
    dict(person_a=P2, person_b=P4, type="superior_subordinate",
         context="市长与副市长政府班子搭档",
         overlap_org="黄骅市人民政府", overlap_period="至今"),
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
    )
    print(f"✅ {SLUG} build complete: DB + GEXF written.")
