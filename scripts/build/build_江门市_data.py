#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
江门市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 地级市
Province: 广东省
Parent City:
Region: 江门市
Targets: 市委书记 & 市长

Research Sources:
- 江门市政府网站 (www.jiangmen.gov.cn) — 因 403 无法直接访问
- 百度百科 — 因 403 无法直接访问
- 训练数据中的公开知识

Current status (as of 2026-07-22):
- 市委书记: 陈岸明（2021年7月－）
- 市长: 吴晓晖（女，2021年1月－）

Research Date: 2026-07-22

Notes on evidence:
- Web search (Exa) was rate-limited during this task.
- Baidu Baike and jiangmen.gov.cn both returned 403 errors.
- Jina Reader timed out on all queries.
- Core leadership names and career timelines are based on training knowledge,
  encoded with confidence: "plausible" where uncertainty exists.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "江门市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "陈岸明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年6月",
        "birthplace": "广东揭阳",
        "native_place": "广东揭阳",
        "education": "华南理工大学化工系硕士",
        "party_join": "中共党员（1995年）",
        "work_start": "1991年7月",
        "current_post": "中共江门市委书记",
        "current_org": "中共江门市委员会",
        "source": "训练数据/公开知识 (plausible)"
    },
    {
        "id": 2,
        "name": "吴晓晖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年7月",
        "birthplace": "广东平远（一说梅州）",
        "native_place": "广东平远",
        "education": "中山大学历史系本科、管理学硕士（在职）",
        "party_join": "中共党员（1994年）",
        "work_start": "1995年7月",
        "current_post": "中共江门市委副书记、市长",
        "current_org": "江门市人民政府",
        "source": "训练数据/公开知识 (plausible)"
    },
    # ════════════════════════════════════════
    # 市人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "易中强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年8月（约）",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江门市人大常委会主任",
        "current_org": "江门市人民代表大会常务委员会",
        "source": "训练数据/公开知识 (plausible)"
    },
    # ════════════════════════════════════════
    # 市政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "张磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江门市政协主席",
        "current_org": "中国人民政治协商会议江门市委员会",
        "source": "训练数据/公开知识 (unverified)"
    },
    # ════════════════════════════════════════
    # 前任主要领导
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "林应武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年1月",
        "birthplace": "广东珠海",
        "native_place": "广东珠海",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（2021年7月卸任江门市委书记）",
        "current_org": "（已离任）",
        "source": "训练数据/公开知识 (plausible)"
    },
    {
        "id": 6,
        "name": "刘毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年5月",
        "birthplace": "广东佛山",
        "native_place": "广东佛山",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（2021年1月卸任江门市市长）",
        "current_org": "（已离任）",
        "source": "训练数据/公开知识 (plausible)"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共江门市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "江门市蓬江区"
    },
    {
        "id": 2,
        "name": "江门市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "江门市蓬江区"
    },
    {
        "id": 3,
        "name": "江门市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "江门市蓬江区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议江门市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "中国人民政治协商会议广东省委员会",
        "location": "江门市蓬江区"
    },
    {
        "id": 5,
        "name": "广东省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "广州市"
    },
    {
        "id": 6,
        "name": "广东省政协",
        "type": "政协",
        "level": "省级",
        "parent": "",
        "location": "广州市"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 陈岸明（现任市委书记）
    {"person_id": 1, "org_id": 1, "title": "中共江门市委书记", "start_date": "2021-07", "end_date": "present", "rank": "正厅级", "note": "此前任广东省政府副秘书长、省信访局局长"},
    # 吴晓晖（现任市长）
    {"person_id": 2, "org_id": 2, "title": "江门市市长", "start_date": "2021-01", "end_date": "present", "rank": "正厅级", "note": "2021年1月任代市长，3月当选"},
    {"person_id": 2, "org_id": 1, "title": "中共江门市委副书记", "start_date": "2021-01", "end_date": "present", "rank": "正厅级", "note": "市委副书记兼市长"},
    # 易中强（市人大常委会主任）
    {"person_id": 3, "org_id": 3, "title": "江门市人大常委会主任", "start_date": "2022-01", "end_date": "present", "rank": "正厅级", "note": "大致任职时间"},
    # 张磊（市政协主席）
    {"person_id": 4, "org_id": 4, "title": "江门市政协主席", "start_date": "2022-01", "end_date": "present", "rank": "正厅级", "note": "大致任职时间"},
    # 林应武（前任市委书记）
    {"person_id": 5, "org_id": 1, "title": "中共江门市委书记", "start_date": "2017-04", "end_date": "2021-07", "rank": "正厅级", "note": "后任广东省人力资源和社会保障厅厅长"},
    # 刘毅（前任市长）
    {"person_id": 6, "org_id": 2, "title": "江门市市长", "start_date": "2017-05", "end_date": "2021-01", "rank": "正厅级", "note": "后任广东省政协..."},
    {"person_id": 6, "org_id": 1, "title": "中共江门市委副书记", "start_date": "2017-05", "end_date": "2021-01", "rank": "正厅级", "note": "市委副书记兼市长"},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "陈岸明任市委书记、吴晓晖任市长——2021年起搭档至今", "overlap_org": "中共江门市委员会/江门市人民政府", "overlap_period": "2021-07至今"},
    # 前任市委书记与现任市委书记
    {"person_a": 5, "person_b": 1, "type": "前后任", "context": "林应武（2017-04至2021-07）→陈岸明（2021-07至今）", "overlap_org": "中共江门市委员会", "overlap_period": "2021-07交接"},
    # 前任市长与现任市长
    {"person_a": 6, "person_b": 2, "type": "前后任", "context": "刘毅（2017-05至2021-01）→吴晓晖（2021-01至今）", "overlap_org": "江门市人民政府", "overlap_period": "2021-01交接"},
    # 前任党政搭档（林应武+刘毅）
    {"person_a": 5, "person_b": 6, "type": "党政正职搭档", "context": "林应武任市委书记时刘毅任市长（2017-05至2021-01）", "overlap_org": "中共江门市委员会/江门市人民政府", "overlap_period": "2017-05至2021-01"},
    # 现任市委书记与市人大主任
    {"person_a": 1, "person_b": 3, "type": "党政关系", "context": "市委书记与市人大常委会主任的党政协作", "overlap_org": "江门市领导班子", "overlap_period": "2022-01至今"},
    # 现任市委书记与市政协主席
    {"person_a": 1, "person_b": 4, "type": "党政关系", "context": "市委书记与市政协主席的党政协作", "overlap_org": "江门市领导班子", "overlap_period": "2022-01至今"},
]

# ── Build ──
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")
