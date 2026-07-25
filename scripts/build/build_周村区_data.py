#!/usr/bin/env python3
"""Build the 周村区（淄博市）leadership network database and GEXF graph.

Task: shandong_周村区
Province: 山东省
Parent city: 淄博市
Region: 周村区
Level: 市辖区
Targets: 区委书记 & 区长

Current leaders (as of 2026-07-25):
- 李德刚: 区委书记, 文昌湖省级旅游度假区工委书记
- 李晓红: 区委副书记、区长, 文昌湖省级旅游度假区工委副书记、管委会主任
"""

import sys
import sqlite3  # noqa: F401 — required by process_tmp validation
from pathlib import Path

# Allow running from repo root
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "周村区"
STAGING = Path("data/tmp/shandong_周村区")
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons (starting from ID 1) ───────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "李德刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共周村区委员会",
        "source": "http://www.zhoucun.gov.cn/art/2026/3/6/art_6027_2989273.html",
    },
    {
        "id": 2,
        "name": "李晓红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "周村区人民政府",
        "source": "http://www.zhoucun.gov.cn/art/2026/1/16/art_6027_2981719.html",
    },
    {
        "id": 3,
        "name": "陈安平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "周村区人大常委会",
        "source": "http://www.zhoucun.gov.cn/art/2026/1/16/art_6027_2981719.html",
    },
    {
        "id": 4,
        "name": "齐军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共周村区委员会",
        "source": "http://www.zhoucun.gov.cn/art/2026/3/6/art_6027_2989273.html",
    },
    {
        "id": 5,
        "name": "汪德江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、办公室主任",
        "current_org": "中共周村区委员会",
        "source": "http://www.zhoucun.gov.cn/art/2026/7/21/art_5349_3011916.html",
    },
    {
        "id": 6,
        "name": "尹斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共周村区委员会",
        "source": "http://www.zhoucun.gov.cn/art/2026/6/1/art_6027_3003855.html",
    },
    {
        "id": 7,
        "name": "薛华伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共周村区委员会",
        "source": "http://www.zhoucun.gov.cn/art/2026/6/1/art_6027_3003855.html",
    },
    {
        "id": 8,
        "name": "宗浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共周村区委员会",
        "source": "http://www.zhoucun.gov.cn/art/2026/7/23/art_5349_3012339.html",
    },
    {
        "id": 9,
        "name": "解金章",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "文昌湖省级旅游度假区工委副书记",
        "current_org": "文昌湖省级旅游度假区",
        "source": "http://www.zhoucun.gov.cn/art/2026/3/6/art_6027_2989273.html",
    },
    {
        "id": 10,
        "name": "张震",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共周村区委员会",
        "source": "http://www.zhoucun.gov.cn/art/2026/7/17/art_5349_3011915.html",
    },
    {
        "id": 11,
        "name": "赵争光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "文昌湖省级旅游度假区领导",
        "current_org": "文昌湖省级旅游度假区",
        "source": "http://www.zhoucun.gov.cn/art/2026/3/6/art_6027_2989273.html",
    },
    {
        "id": 12,
        "name": "刘智平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会",
        "current_org": "周村区人大常委会",
        "source": "http://www.zhoucun.gov.cn/art/2026/1/16/art_6027_2981719.html",
    },
    {
        "id": 13,
        "name": "国卫兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "周村区政协",
        "source": "http://www.zhoucun.gov.cn/art/2026/1/16/art_6027_2981719.html",
    },
    {
        "id": 14,
        "name": "王文晓",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "周村区人民政府",
        "source": "http://www.zhoucun.gov.cn/art/2026/7/22/art_5349_3012331.html",
    },
    {
        "id": 15,
        "name": "胡强强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "周村区人民政府",
        "source": "http://www.zhoucun.gov.cn/art/2026/7/22/art_5349_3012331.html",
    },
]

# ── Organizations (IDs 100001+ in GEXF) ────────────────────────────────
organizations = [
    {"id": 1, "name": "中共周村区委员会", "type": "党委", "level": "县级", "parent": "中共淄博市委", "location": "淄博市周村区"},
    {"id": 2, "name": "周村区人民政府", "type": "政府", "level": "县级", "parent": "淄博市人民政府", "location": "淄博市周村区"},
    {"id": 3, "name": "周村区人大常委会", "type": "人大", "level": "县级", "parent": "淄博市人大常委会", "location": "淄博市周村区"},
    {"id": 4, "name": "周村区政协", "type": "政协", "level": "县级", "parent": "淄博市政协", "location": "淄博市周村区"},
    {"id": 5, "name": "文昌湖省级旅游度假区", "type": "开发区", "level": "县级", "parent": "淄博市政府", "location": "淄博市周村区"},
]

# ── Positions (person_id, org_id, title) ──────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "正处级"},
    {"person_id": 1, "org_id": 5, "title": "文昌湖省级旅游度假区工委书记", "start_date": "", "end_date": "present", "rank": "正处级"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present", "rank": "正处级"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "正处级"},
    {"person_id": 2, "org_id": 5, "title": "文昌湖省级旅游度假区工委副书记、管委会主任", "start_date": "", "end_date": "present", "rank": "正处级"},
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级"},
    {"person_id": 4, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级"},
    {"person_id": 5, "org_id": 1, "title": "区委常委、办公室主任", "start_date": "", "end_date": "present", "rank": "副处级"},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级"},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级"},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级"},
    {"person_id": 9, "org_id": 5, "title": "文昌湖省级旅游度假区工委副书记", "start_date": "", "end_date": "present", "rank": "副处级"},
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级"},
    {"person_id": 11, "org_id": 5, "title": "文昌湖省级旅游度假区领导", "start_date": "", "end_date": "present", "rank": ""},
    {"person_id": 12, "org_id": 3, "title": "区人大常委会组成人员", "start_date": "", "end_date": "present", "rank": ""},
    {"person_id": 13, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "正处级"},
    {"person_id": 14, "org_id": 2, "title": "区领导", "start_date": "", "end_date": "present", "rank": ""},
    {"person_id": 15, "org_id": 2, "title": "区领导", "start_date": "", "end_date": "present", "rank": ""},
]

# ── Relationships (person <-> person) ──────────────────────────────────
relationships = [
    # 书记-区长：主要领导搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "区委书记与区长是党政主要领导搭档关系，共同出席区委审计委员会会议（2026年7月10日）、人代会（2026年1月）、理论学习中心组学习等多次重要会议",
        "overlap_org": "周村区",
        "overlap_period": "2026-",
    },
    # 书记-陈安平（人大主任）
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "区委书记与区人大常委会主任，共同出席人代会",
        "overlap_org": "周村区",
        "overlap_period": "2026-",
    },
    # 书记-齐军（区委副书记）
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记与区委副书记，共同参加理论学习中心组学习、实地调研、党外人士座谈会等",
        "overlap_org": "中共周村区委员会",
        "overlap_period": "2026-",
    },
    # 书记-汪德江（区委常委、办公室主任）
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委、办公室主任，汪德江多次陪同李德刚调研（如安全生产督导7月21日、山东理工大来访7月22日）",
        "overlap_org": "中共周村区委员会",
        "overlap_period": "2026-",
    },
    # 书记-尹斌
    {
        "person_a": 1, "person_b": 6,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委，共同出席理论学习中心组学习（2026年7月）和人代会",
        "overlap_org": "中共周村区委员会",
        "overlap_period": "2026-",
    },
    # 书记-宗浩
    {
        "person_a": 1, "person_b": 8,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委，共同出席党外人士座谈会（2026年7月23日）",
        "overlap_org": "中共周村区委员会",
        "overlap_period": "2026-",
    },
    # 书记-解金章（文昌湖工委副书记）
    {
        "person_a": 1, "person_b": 9,
        "type": "superior_subordinate",
        "context": "区委书记兼文昌湖工委书记与文昌湖工委副书记，共同出席调研活动（2026年3月6日）",
        "overlap_org": "文昌湖省级旅游度假区",
        "overlap_period": "2026-",
    },
    # 区长-齐军（区委副书记）
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "区长与区委副书记，共同出席人代会和区级重要会议",
        "overlap_org": "周村区",
        "overlap_period": "2026-",
    },
    # 区长-陈安平（人大主任）
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "区长与人大主任，人大会议上李晓红作工作报告，陈安平主持会议",
        "overlap_org": "周村区",
        "overlap_period": "2026-",
    },
    # 区长-薛华伟
    {
        "person_a": 2, "person_b": 7,
        "type": "overlap",
        "context": "区长与区委常委，共同参加六一慰问活动（2026年5月28-29日）",
        "overlap_org": "周村区",
        "overlap_period": "2026-",
    },
    # 区长-尹斌
    {
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "区长与区委常委，共同出席六一慰问活动",
        "overlap_org": "周村区",
        "overlap_period": "2026-",
    },
    # 区长-宗浩
    {
        "person_a": 2, "person_b": 8,
        "type": "overlap",
        "context": "区长与区委常委，共同出席六一慰问活动",
        "overlap_org": "周村区",
        "overlap_period": "2026-",
    },
    # 区长-解金章
    {
        "person_a": 2, "person_b": 9,
        "type": "overlap",
        "context": "区长（兼任文昌湖工委副书记、管委会主任）与文昌湖工委副书记",
        "overlap_org": "文昌湖省级旅游度假区",
        "overlap_period": "2026-",
    },
    # 区长-国卫兵（政协主席）
    {
        "person_a": 2, "person_b": 13,
        "type": "overlap",
        "context": "区长与政协主席，共同出席人代会",
        "overlap_org": "周村区",
        "overlap_period": "2026-",
    },
]

# ── Run build ──────────────────────────────────────────────────────────
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
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
