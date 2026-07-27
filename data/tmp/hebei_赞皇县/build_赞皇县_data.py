#!/usr/bin/env python3
"""
赞皇县领导班子工作关系网络 — Build script
河北省石家庄市赞皇县

Confirmed sources:
- 赞皇县人民政府关于县长副县长分工通知 (2026-03-24): confirms 卢占军 as 县长 and all deputy-level leaders
- 赞皇县人民政府门户网站 领导之窗: confirms 曹彦鹏, 李杨, 赵太民

Research date: 2026-07-23
"""

import json
import os
import sys
from datetime import date

# Add repo root to path
_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

AS_OF = "2026-07-23"

# ── PERSONS ──
persons = [
    # ── 县委书记 (Party Secretary) ──
    {
        "id": 1,
        "name": "陈宏锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968?",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "赞皇县委书记",
        "current_org": "中共石家庄市赞皇县委员会",
        "source": "https://www.zanhuang.gov.cn/",
    },
    # ── 县长 (County Mayor) ──
    {
        "id": 2,
        "name": "卢占军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "赞皇县委副书记、县长",
        "current_org": "赞皇县人民政府/中共石家庄市赞皇县委员会",
        "source": "https://www.zanhuang.gov.cn/columns/42a0f87f-5f58-4117-983e-32a9a0f8c306/202603/24/18ca6370-a21d-45d8-8364-ada5b898e152.html",
    },
    # ── 常务副县长 ──
    {
        "id": 3,
        "name": "曹彦鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长（分工常务工作）",
        "current_org": "赞皇县人民政府",
        "source": "https://www.zanhuang.gov.cn/columns/7eec0479-4f1b-4603-b53f-06de98d6ebee/202603/24/c6e19802-21f5-4fc4-a80c-7d0cf114f5ed.html",
    },
    # ── 副县长 ──
    {
        "id": 4,
        "name": "杜晓伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "赞皇县人民政府",
        "source": "赞皇县人民政府关于县长副县长分工通知 (2026-03-24)",
    },
    # ── 副县长、公安局局长 ──
    {
        "id": 5,
        "name": "于得水",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "赞皇县人民政府/赞皇县公安局",
        "source": "赞皇县人民政府关于县长副县长分工通知 (2026-03-24)",
    },
    # ── 副县长 ──
    {
        "id": 6,
        "name": "张晨光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "赞皇县人民政府",
        "source": "赞皇县人民政府关于县长副县长分工通知 (2026-03-24)",
    },
    # ── 副县长 ──
    {
        "id": 7,
        "name": "宋利锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "赞皇县人民政府",
        "source": "赞皇县人民政府关于县长副县长分工通知 (2026-03-24)",
    },
    # ── 副县长 ──
    {
        "id": 8,
        "name": "刘冠然",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "赞皇县人民政府",
        "source": "赞皇县人民政府关于县长副县长分工通知 (2026-03-24)",
    },
    # ── 副县长（挂职） ──
    {
        "id": 9,
        "name": "李杨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "赞皇县人民政府",
        "source": "https://www.zanhuang.gov.cn/columns/7eec0479-4f1b-4603-b53f-06de98d6ebee/202408/13/3f243b51-8755-4de0-88cc-9e26591062a9.html",
    },
    # ── 开发区党工委副书记 ──
    {
        "id": 10,
        "name": "朱晓辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开发区党工委副书记兼管委会常务副主任",
        "current_org": "赞皇经济开发区",
        "source": "赞皇县人民政府关于县长副县长分工通知 (2026-03-24)",
    },
    # ── 县政府三级调研员 ──
    {
        "id": 11,
        "name": "赵太民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府三级调研员",
        "current_org": "赞皇县人民政府",
        "source": "https://www.zanhuang.gov.cn/columns/7eec0479-4f1b-4603-b53f-06de98d6ebee/202108/17/c976136e-1f60-4122-a91b-412f40d27de1.html",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共石家庄市赞皇县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共石家庄市委员会",
        "location": "河北省石家庄市赞皇县",
    },
    {
        "id": 2,
        "name": "赞皇县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "石家庄市人民政府",
        "location": "河北省石家庄市赞皇县",
    },
    {
        "id": 3,
        "name": "赞皇县公安局",
        "type": "政府",
        "level": "县",
        "parent": "赞皇县人民政府/石家庄市公安局",
        "location": "河北省石家庄市赞皇县",
    },
    {
        "id": 4,
        "name": "赞皇经济开发区",
        "type": "开发区",
        "level": "县",
        "parent": "赞皇县人民政府",
        "location": "河北省石家庄市赞皇县",
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 陈宏锋 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "赞皇县委书记",
     "start_date": "2021?", "end_date": "present",
     "rank": "正处级", "note": "约2021年起任赞皇县委书记"},
    # 卢占军 — 县委副书记、县长
    {"person_id": 2, "org_id": 1, "title": "赞皇县委副书记",
     "start_date": "?", "end_date": "present",
     "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "赞皇县县长",
     "start_date": "?", "end_date": "present",
     "rank": "正处级", "note": "截至2026年3月在任"},
    # 曹彦鹏 — 县委常委、常务副县长
    {"person_id": 3, "org_id": 1, "title": "县委常委",
     "start_date": "?", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副县长（分工常务工作）",
     "start_date": "?", "end_date": "present",
     "rank": "副处级", "note": "协助县长负责审计、经济开发区工作"},
    # 杜晓伟 — 副县长
    {"person_id": 4, "org_id": 2, "title": "副县长",
     "start_date": "?", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 于得水 — 副县长、公安局局长
    {"person_id": 5, "org_id": 2, "title": "副县长",
     "start_date": "?", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "公安局局长",
     "start_date": "?", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 张晨光 — 副县长
    {"person_id": 6, "org_id": 2, "title": "副县长",
     "start_date": "?", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 宋利锋 — 副县长
    {"person_id": 7, "org_id": 2, "title": "副县长",
     "start_date": "?", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 刘冠然 — 副县长
    {"person_id": 8, "org_id": 2, "title": "副县长",
     "start_date": "?", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 李杨 — 副县长（挂职）
    {"person_id": 9, "org_id": 2, "title": "副县长（挂职）",
     "start_date": "?", "end_date": "present",
     "rank": "副处级（挂职）", "note": "中央港澳办挂职干部，负责外事及对口帮扶"},
    # 朱晓辉 — 开发区副主任
    {"person_id": 10, "org_id": 4, "title": "开发区党工委副书记兼管委会常务副主任",
     "start_date": "?", "end_date": "present",
     "rank": "正科级?", "note": ""},
    # 赵太民 — 三级调研员
    {"person_id": 11, "org_id": 2, "title": "县政府三级调研员",
     "start_date": "?", "end_date": "present",
     "rank": "副处级（职级）", "note": "协助曹彦鹏做好安全生产，协助张晨光做好防汛"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "赞皇县委书记与县长党政搭档",
     "overlap_org": "中共石家庄市赞皇县委员会/赞皇县人民政府",
     "overlap_period": "2021?-present"},
    # 卢占军 ↔ 曹彦鹏 — 直接分工关系
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "曹彦鹏协助卢占军负责审计、经济开发区工作",
     "overlap_org": "赞皇县人民政府",
     "overlap_period": "present"},
    # 曹彦鹏 ↔ 赵太民 — 协助关系
    {"person_a": 3, "person_b": 11, "type": "superior_subordinate",
     "context": "赵太民协助曹彦鹏做好安全生产相关工作",
     "overlap_org": "赞皇县人民政府",
     "overlap_period": "present"},
    # 张晨光 ↔ 赵太民 — 协助关系
    {"person_a": 6, "person_b": 11, "type": "superior_subordinate",
     "context": "赵太民协助张晨光做好防汛相关工作",
     "overlap_org": "赞皇县人民政府",
     "overlap_period": "present"},
    # 卢占军 ↔ 李杨 — 对口帮扶关系
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "李杨协助县长负责巩固脱贫成果和乡村振兴工作",
     "overlap_org": "赞皇县人民政府",
     "overlap_period": "present"},
    # 卢占军 ↔ 于得水 — 公安工作关系
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "于得水分管公安工作，向县长负责",
     "overlap_org": "赞皇县人民政府",
     "overlap_period": "present"},
]

# =========================================================================
# 5. BUILD
# =========================================================================
if __name__ == "__main__":
    staging_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(staging_dir, "赞皇县_network.db")
    gexf_path = os.path.join(staging_dir, "赞皇县_network.gexf")
    
    run_build(
        slug="赞皇县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
    )
    print("Build complete.")
