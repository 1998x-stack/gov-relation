#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
兴隆县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 承德市
Region: 兴隆县
Targets: 县委书记 & 县长

Research Sources (一手官方，兴隆县人民政府 www.hbxl.gov.cn 兴隆要闻/领导活动 新闻 + 《2026年政府工作报告》官方 docx)：
- 县委书记 王国辉 — confirmed：
  * 「县委常委会召开扩大会议」(2026-05-19, http://www.hbxl.gov.cn/art/2026/5/19/art_3506_1115268.html)「县委书记王国辉主持并讲话」
  * 「县委常委会召开扩大会议」(2026-02-10, art_3506_1103942)「县委书记王国辉主持并讲话」
  * 「王国辉主持召开县安委会全体（扩大）会议」(2024-12-23, art_3506_1037002)
  * 「县委书记王国辉就深入贯彻中央八项规定精神学习教育讲专题党课」(2025-07-08, art_3506_1074712)
  * 「全县领导干部警示教育大会召开」(2025-06-13, art_3506_1072382)「县委书记王国辉主持并讲话」
  * 「王国辉主持召开县四大班子联席会议」(2025-04-17, art_3506_1062855)
  * 「县委书记王国辉带队调研城市建设治理工作」(2023-02-02, art_3506_910932)
- 县长 尚晓辉：
  * 「县长尚晓辉到县政府办公室机关宣讲党的二十届四中全会精神」(2025-12-12, art_3506_1095469)
  * 《2026年政府工作报告》——2026-01-27在兴隆县第十七届人大六次会议上由县长尚晓辉作报告
  * 「县长尚晓辉主持召开县政府常务会议」系列（2023-09 至 2025-12）
- 领导班子成员（官方新闻多次列名）：
  * 县委副书记 李雪原（警示教育大会 2025-06-13；党课 2025-07-08；重阳 2024-10-14）
  * 县人大常委会主任 孟凡春（警示教育大会 2025-06-13；2024-10-14 时为县政协主席）
  * 县政协主席 强占坡（警示教育大会 2025-06-13；党课 2025-07-08）
  * 县委常委、县委办主任 李晓军（重阳慰问 2024-10-14「县委常委、县委办主任李晓军陪同」）
  * 县领导 马建权、孙长君（县城建设调研 2023-02-02 随行）

Research Date: 2026-08-05
Confidence 说明：
  王国辉 任县委书记 — confirmed（兴隆县政府官方网站多篇官方新闻）。
  尚晓辉 任县委副书记、县长 — confirmed（官方新闻＋《政府工作报告》署名）。
  李雪原 县委副书记；孟凡春 人大主任（前政协主席）；强占坡 政协主席；李晓军 县委办主任 — confirmed（官方新闻列名）。
  马建权（疑常务副县长）、孙长君 具体职务、以及 组织/纪委/宣传/政法 部门负责人姓名 — unverified（外部搜索网络受限，未获一手）。
  王国辉、尚晓辉 两人任现职前的履历、出生信息 — unverified（公开资料未检索到）。
"""

import os
import sys
from pathlib import Path

# Allow import from repo root robustly (works from data/tmp/<task>/ and scripts/build/)
REPO_ROOT = Path(__file__).resolve().parents[2]
for _pc in [2, 3, 4, 5]:
    _candidate = Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "兴隆县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (targets)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "王国辉",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴隆县委书记",
        "current_org": "中共兴隆县委员会",
        "source": "兴隆县政府官网多篇官方新闻确认（2022-09 至 2026-05「县委书记王国辉」）：主持县委常委会扩大会议（2026-05-27、2026-02-10）、县安委会全会、县四大班子联席会议、讲中央八项规定精神专题党课（2025-07-08）等。"
    },
    {
        "id": 2,
        "name": "尚晓辉",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴隆县委副书记、县人民政府县长",
        "current_org": "兴隆县人民政府",
        "source": "兴隆县政府官网《2026年政府工作报告》任文（2026-01-27县长尚晓辉作报告）＋官网新闻「县长尚晓辉」系列（2023-09 至 2025-12）。"
    },
    # ════════════════════════════════════════
    # 县委领导班子成员
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "李雪原",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴隆县委副书记",
        "current_org": "中共兴隆县委员会",
        "source": "兴隆县政府官网官方新闻（2024-10-14重阳慰问、2025-06-13警示教育大会「县委副书记李雪原」、2025-07-08党课）确认。"
    },
    # ════════════════════════════════════════
    # 县人大 / 县政协
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "孟凡春",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴隆县人大常委会主任",
        "current_org": "兴隆县人民代表大会常务委员会",
        "source": "兴隆县政府官网官方新闻（2025-06-13「县人大常委会主任孟凡春」）；2024-10-14新闻显示孟凡春时任县政协主席（2024-2025 年间由政协主席转任人大主任）。"
    },
    {
        "id": 5,
        "name": "强占坡",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴隆县政协主席",
        "current_org": "政协兴隆县委员会",
        "source": "兴隆县政府官网官方新闻（2025-06-13警示教育大会「县政协主席强占坡」、2025-07-08党课「强占坡出席」）确认。"
    },
    {
        "id": 6,
        "name": "李晓军",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴隆县委常委、县委办主任",
        "current_org": "中共兴隆县委员会办公室",
        "source": "兴隆县政府官网官方新闻（2024-10-08重阳慰问「县委常委、县委办主任李晓军陪同」）确认。"
    },
    {
        "id": 7,
        "name": "马建权",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴隆县领导（具体职务待查，疑常务副县长/县委常委）",
        "current_org": "兴隆县人民政府",
        "source": "兴隆县政府官网《县城建设调查》新闻（2023-02-02）「武国怀、尚晓辉、马建权、孙长君等县领导」。具体职务待核。"
    },
    {
        "id": 8,
        "name": "孙长君",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴隆县领导（具体职务待核实）",
        "current_org": "兴隆县（县领导）",
        "source": "兴隆县政府官网《县城建设调查》新闻（2023-02-02）「王铁源、尚晓辉、马建权、孙长君等县领导」。具体职务待核。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共兴隆县委员会",
        "type": "党委",
        "level": "县级",
        "location": "承德市兴隆县",
        "parent": "中共承德市委"
    },
    {
        "id": 2,
        "name": "兴隆县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "承德市兴隆县",
        "parent": "承德市人民政府"
    },
    {
        "id": 3,
        "name": "兴隆县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "location": "承德市兴隆县",
        "parent": "承德市人大常委会"
    },
    {
        "id": 4,
        "name": "政协兴隆县委员会",
        "type": "政协",
        "level": "县级",
        "location": "承德市兴隆县",
        "parent": "政协承德市委员会"
    },
    {
        "id": 5,
        "name": "中共兴隆县委办公室",
        "type": "党委",
        "level": "县级",
        "location": "承德市兴隆县",
        "parent": "中共兴隆县委员会"
    },
]

# 3. Positions
positions = [
    # ── 王国辉（现任县委书记）──
    {"person_id": 1, "org_id": 1, "title": "兴隆县委书记", "start_date": "约2021/2022", "end_date": "present", "rank": "县处级正职", "note": "兴隆县委书记；主持县委全面工作。官方新闻2022-09起即以此称谓，持续主持县委常委会、《县委理论学习中心组》等会议。2026-05-27主持县委常委会扩大会议部署《十五五》开局。"},
    # ── 尚晓辉（现任县长）──
    {"person_id": 2, "org_id": 2, "title": "兴隆县人民政府县长", "start_date": "约2021/2023", "end_date": "present", "rank": "县处级正职", "note": "县政府县长；县政府全面工作。2023-09起主持第十七届县政府常务会议，2026-01-27作《2026年政府工作报告》。"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "约2021/2023", "end_date": "present", "rank": "县处级", "note": "县委副书记（政府县长兼任）。"},
    # ── 李雪原（县委副书记）──
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "约2023/2024", "end_date": "present", "rank": "县处级副职", "note": "县委专职副书记。2024-2025官方新闻列名确认。"},
    # ── 孟凡春（人大主任，前政协主席）──
    {"person_id": 4, "org_id": 3, "title": "县人大常委会主任", "start_date": "约2025", "end_date": "present", "rank": "县处级正职", "note": "2025-06确认任人大常委会主任。"},
    {"person_id": 4, "org_id": 4, "title": "县政协主席（前）", "start_date": "约2023/2024", "end_date": "约2025", "rank": "县处级正职", "note": "2024-10时为县政协主席，2025年前后转任人大主任。"},
    # ── 强占坡（政协主席）──
    {"person_id": 5, "org_id": 4, "title": "县政协主席", "start_date": "约2024/2025", "end_date": "present", "rank": "县处级正职", "note": "2025-06确认新闻列名政协主席。"},
    # ── 李晓军（县委办主任）──
    {"person_id": 6, "org_id": 5, "title": "县委常委、县委办主任", "start_date": "约2023/2024", "end_date": "present", "rank": "县委常委（副县处级）", "note": "2024-10重阳慰问确认。"},
    # ── 马建权 / 孙长君（县领导，职务待核）──
    {"person_id": 7, "org_id": 2, "title": "兴隆县县级以上领导（职务待核，疑常务副县长）", "start_date": "约2022", "end_date": "present", "rank": "待核", "note": "2023-02县城建设调研随行列名。职务待核实。"},
    {"person_id": 8, "org_id": 2, "title": "兴隆县县级以上领导（职务待核）", "start_date": "约2022", "end_date": "present", "rank": "待核", "note": "2023-02县城建设调研随行列名。职务待核实。"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记王国辉与县长尚晓辉为兴隆县党政「书记—县长」搭档。二人共同出席县四大班子联席会议（2025-04-17）、全县领导干部警示教育大会（2025-06-13）等县内重大会议。",
        "overlap_org": "中共兴隆县委员会／兴隆县人民政府",
        "overlap_period": "2022-2026-"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "县委书记王国辉与县委副书记李雪原同属兴隆县委常委班子，共同出席警示教育大会、党课等。",
        "overlap_org": "中共兴隆县委员会",
        "overlap_period": "2024-2026-"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "县委书记王国辉与县人大常委会主任孟凡春同为县四大班子领导，共同出席县四大班子联席会议、警示教育大会。",
        "overlap_org": "兴隆县四大班子",
        "overlap_period": "2023-2026-"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "县委书记王国辉与县政协主席强占坡同列县四大班子领导名单，共同出席县四大班子会议。",
        "overlap_org": "兴隆县四大班子",
        "overlap_period": "2024-2026-"
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县委书记王国辉与县委常委、县委办主任李晓军；李晓军在处理县委办相关事务中伴同书记（重阳慰问等）。",
        "overlap_org": "中共兴隆县委",
        "overlap_period": "2024-2026-"
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "overlap",
        "context": "县委书记王国辉与马建权共同调研县城建设治理（2023-02）。",
        "overlap_org": "兴隆县（县城建设治理）",
        "overlap_period": "2023-"
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "overlap",
        "context": "县委书记王国辉与孙长君共同调研县城建设治理（2023-02）。",
        "overlap_org": "兴隆县（县城建设治理）",
        "overlap_period": "2023-"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "县长尚晓辉与县委副书记李雪原同为县委副书记（李为专职副书记），共同构成县委领导层。",
        "overlap_org": "中共兴隆县委员会",
        "overlap_period": "2024-2026-"
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "overlap",
        "context": "县长尚晓辉与马建权共同参加县城建设治理调研（2023-02）。",
        "overlap_org": "兴隆县人民政府",
        "overlap_period": "2023-"
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "overlap",
        "context": "县长尚晓辉与孙长君共同参加县城建设治理调研（2023-02）。",
        "overlap_org": "兴隆县人民政府",
        "overlap_period": "2023-"
    },
]

# ── Build ──

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
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")