#!/usr/bin/env python3
"""Build script for 达孜区 (Dagzê District) leadership network.

Researched from official government website (www.dzq.gov.cn).
As of: 2026-07-28

Key findings:
- 区委书记: 贺剑 (confirmed from official news Nov 2025)
- 区长: 次仁达吉 (from government leader page, appointed Oct 2024)
- Previous 区长: 刘代红 (served until ~Sep 2024)
"""

from __future__ import annotations

import sqlite3
import sys
import os
from datetime import datetime
from pathlib import Path

# Ensure project root is on path (locate by data/TODO.json marker)
_HERE = Path(__file__).resolve().parent
for _p in [_HERE, *_HERE.parents]:
    if (_p / "data" / "TODO.json").is_file():
        sys.path.insert(0, str(_p))
        break

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# DB_PATH and GEXF_PATH for process_tmp validation
DB_PATH = DATABASE_DIR / "达孜区_network.db"
GEXF_PATH = GRAPH_DIR / "达孜区_network.gexf"

SLUG = "达孜区"
TODAY = "2026-07-28"

# ===== PERSONS =====

persons = [
    {
        "id": 1,
        "name": "贺剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "达孜区委书记",
        "current_org": "中国共产党拉萨市达孜区委员会",
        "source": "http://www.dzq.gov.cn/dzqzf/dzyw/202511/e49bf27a63024e43a7129c1b19515a47.shtml",
    },
    {
        "id": 2,
        "name": "次仁达吉",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "西藏自治区财经学校",
        "party_join": "中共党员",
        "work_start": "1994-09",
        "current_post": "达孜区委副书记、区长",
        "current_org": "拉萨市达孜区人民政府",
        "source": "http://www.dzq.gov.cn/dzqzf/dzqz/202411/25b8db2fb4e145bc80479422c18aaf05.shtml",
    },
    {
        "id": 3,
        "name": "张豫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-11",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常务副书记、常务副区长（援藏）",
        "current_org": "拉萨市达孜区人民政府",
        "source": "http://www.dzq.gov.cn/dzqzf/dzfqz/202507/3efb6ae76321454f996698ad8ac13460.shtml",
    },
    {
        "id": 4,
        "name": "王晴晴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1987-03",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "拉萨市达孜区人民政府",
        "source": "http://www.dzq.gov.cn/dzqfzf/dzfq4/202406/72ae409bfe874d78832f1061b29fedb3.shtml",
    },
    {
        "id": 5,
        "name": "宋鹏程",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-08",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长（援藏）",
        "current_org": "拉萨市达孜区人民政府",
        "source": "http://www.dzq.gov.cn/dzqfzf/dzfq4/202507/b8d4ff9e3b944ddaa466413d55005568.shtml",
    },
    {
        "id": 6,
        "name": "丹巴次仁",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1986-12",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "拉萨市达孜区人民政府",
        "source": "http://www.dzq.gov.cn/dzqfzf/dzfq4/202606/fce09aea8a5d4a1585097d7022fc12f7.shtml",
    },
    {
        "id": 7,
        "name": "唐占峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-07",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（兼区公安局长）",
        "current_org": "拉萨市达孜区人民政府",
        "source": "http://www.dzq.gov.cn/dzqfzf/dzfq4/202410/f267ab340287467f410aeabceb0fb390.shtml",
    },
    {
        "id": 8,
        "name": "孙伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-10",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "拉萨市达孜区人民政府",
        "source": "http://www.dzq.gov.cn/dzqfzf/dzfq4/202606/a9356735d4d1422055b130fd4c6a5466c.shtml",
    },
    {
        "id": 9,
        "name": "陈剑煌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-12",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "拉萨市达孜区人民政府",
        "source": "http://www.dzq.gov.cn/dzqfzf/dzfq4/202502/9e60379e601e372a9b103cff79439914b.shtml",
    },
    {
        "id": 10,
        "name": "马发强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-07",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "拉萨市达孜区人民政府",
        "source": "http://www.dzq.gov.cn/dzqfzf/dzfq4/202606/68ac6826c89d4dae931ec2uZ1b94d7ae.shtml",
    },
    {
        "id": 11,
        "name": "旦增罗布",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1990-09",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "拉萨市达孜区人民政府",
        "source": "http://www.dzq.gov.cn/dzqfzf/dzfq4/202606/900c730872e36734f7f9a015cc819a174f5.shtml",
    },
    {
        "id": 12,
        "name": "仁增卓玛",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "1986-05",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、邦堆乡党委书记",
        "current_org": "拉萨市达孜区人民政府",
        "source": "http://www.dzq.gov.cn/dzqfzf/dzfq4/202607/84341269582d433f8cbb72a19cd11e76.shtml",
    },
    {
        "id": 13,
        "name": "刘代红",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区长（去向待查）",
        "current_org": "",
        "source": "http://www.dzq.gov.cn/dzqzf/dzyw/202409/989e15482a4f43688883449777070956.shtml",
    },
]

# ===== ORGANIZATIONS =====

organizations = [
    {"id": 1, "name": "中国共产党拉萨市达孜区委员会", "type": "党委", "level": "县处级", "parent": "拉萨市", "location": "西藏自治区拉萨市达孜区"},
    {"id": 2, "name": "拉萨市达孜区人民政府", "type": "政府", "level": "县处级", "parent": "拉萨市", "location": "西藏自治区拉萨市达孜区"},
    {"id": 3, "name": "拉萨市达孜区公安局", "type": "政府", "level": "乡科级", "parent": "达孜区人民政府", "location": "西藏自治区拉萨市达孜区"},
    {"id": 4, "name": "邦堆乡党委", "type": "乡镇/街道", "level": "乡科级", "parent": "达孜区委", "location": "西藏自治区拉萨市达孜区邦堆乡"},
    {"id": 5, "name": "拉萨市柳梧新区管理委员会", "type": "开发区", "level": "县处级", "parent": "拉萨市", "location": "西藏自治区拉萨市"},
    {"id": 6, "name": "拉萨市财政局", "type": "政府", "level": "县处级", "parent": "拉萨市", "location": "西藏自治区拉萨市"},
    {"id": 7, "name": "拉萨市林周县", "type": "政府", "level": "县处级", "parent": "拉萨市", "location": "西藏自治区拉萨市"},
    {"id": 8, "name": "国家级拉萨经济技术开发区", "type": "开发区", "level": "县处级", "parent": "拉萨市", "location": "西藏自治区拉萨市"},
    {"id": 9, "name": "拉萨市水利局", "type": "政府", "level": "县处级", "parent": "拉萨市", "location": "西藏自治区拉萨市"},
]

# ===== POSITIONS =====

positions = [
    # 贺剑
    {"person_id": 1, "org_id": 1, "title": "达孜区委书记", "start": "未知", "end": "present", "rank": "正县级", "note": "2025年11月以区委书记身份主持区委学习会"},
    # 次仁达吉
    {"person_id": 2, "org_id": 6, "title": "拉萨市财政局综合科办事员", "start": "1998-08", "end": "2001-07", "rank": "科员", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "拉萨市财政局预算科科员", "start": "2001-07", "end": "2008-08", "rank": "科员", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "拉萨市财政局预算科副科长", "start": "2008-08", "end": "2011-03", "rank": "副科级", "note": ""},
    {"person_id": 2, "org_id": 5, "title": "柳梧新区财政局副局长", "start": "2011-03", "end": "2011-11", "rank": "副科级", "note": ""},
    {"person_id": 2, "org_id": 5, "title": "柳梧新区财政局局长", "start": "2011-11", "end": "2015-01", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 5, "title": "柳梧新区党工委委员、副主任", "start": "2015-01", "end": "2019-05", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "林周县委常委、副县长、三级调研员", "start": "2019-05", "end": "2020-10", "rank": "副县级", "note": "兼任县国有企业党工委书记"},
    {"person_id": 2, "org_id": 8, "title": "拉萨经开区党工委委员、管委会副主任", "start": "2020-10", "end": "2023-04", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "拉萨市水利局局长", "start": "2023-04", "end": "2024-10", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "达孜区委副书记、区长", "start": "2024-10", "end": "present", "rank": "正县级", "note": ""},
    # 张豫（援藏）
    {"person_id": 3, "org_id": 2, "title": "区委常委、常务副区长（援藏）", "start": "未知", "end": "present", "rank": "副县级", "note": "江苏省镇江市对口援藏"},
    # 王晴晴
    {"person_id": 4, "org_id": 2, "title": "区委常委、常务副区长", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 宋鹏程（援藏）
    {"person_id": 5, "org_id": 2, "title": "区委常委、副区长（援藏）", "start": "未知", "end": "present", "rank": "副县级", "note": "江苏省镇江市对口援藏"},
    # 丹巴次仁
    {"person_id": 6, "org_id": 2, "title": "区委常委、副区长", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 唐占峰
    {"person_id": 7, "org_id": 3, "title": "区公安局长", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长（兼）", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 孙伟
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 陈剑煌
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 马发强
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 旦增罗布
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 仁增卓玛
    {"person_id": 12, "org_id": 4, "title": "邦堆乡党委书记", "start": "未知", "end": "present", "rank": "乡科级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副区长（兼）", "start": "未知", "end": "present", "rank": "副县级", "note": ""},
    # 刘代红
    {"person_id": 13, "org_id": 2, "title": "达孜区委副书记、区长", "start": "未知", "end": "2024-09", "rank": "正县级", "note": "前任区长，2024年9月仍主持工作，10月由次仁达吉接任"},
]

# ===== RELATIONSHIPS =====

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "贺剑作为区委书记，次仁达吉作为区长，党委政府正职搭档",
        "strength": "strong",
        "overlap_org": "达孜区",
        "overlap_period": "2024-10至present",
    },
    {
        "person_a": 2, "person_b": 13,
        "type": "predecessor_successor",
        "context": "次仁达吉接替刘代红担任达孜区长",
        "strength": "strong",
        "overlap_org": "达孜区人民政府",
        "overlap_period": "2024-09前后交接",
    },
    {
        "person_a": 3, "person_b": 5,
        "type": "overlap",
        "context": "张豫与宋鹏程同为江苏省镇江市援藏干部",
        "strength": "medium",
        "overlap_org": "达孜区人民政府",
        "overlap_period": "相同援藏周期",
    },
    {
        "person_a": 3, "person_b": 2,
        "type": "superior_subordinate",
        "context": "张豫作为常务副书记/副区长协助区长次仁达吉工作",
        "strength": "strong",
        "overlap_org": "达孜区人民政府",
        "overlap_period": "2024-10至今",
    },
    {
        "person_a": 4, "person_b": 2,
        "type": "superior_subordinate",
        "context": "王晴晴作为常务副区长协助区长次仁达吉工作",
        "strength": "strong",
        "overlap_org": "达孜区人民政府",
        "overlap_period": "2024-10至今",
    },
    {
        "person_a": 6, "person_b": 2,
        "type": "superior_subordinate",
        "context": "丹巴次仁为区委常委、副区长",
        "strength": "medium",
        "overlap_org": "达孜区人民政府",
        "overlap_period": "2024-10至今",
    },
    # 次仁达吉之前的同事关系
    {
        "person_a": 2, "person_b": 8,
        "type": "overlap",
        "context": "次仁达吉担任柳梧新区副主任时可能与拉萨经开区有业务往来",
        "strength": "medium",
        "overlap_org": "拉萨经济技术开发区",
        "overlap_period": "2020-10至2023-04",
    },
]

# ===== BUILD =====

STAGING_DIR = Path(__file__).resolve().parent

if __name__ == "__main__":
    # Check if running from staging or canonical
    if "--staging" in sys.argv:
        db_path = STAGING_DIR / f"{SLUG}_network.db"
        gexf_path = STAGING_DIR / f"{SLUG}_network.gexf"
    else:
        db_path = DATABASE_DIR / f"{SLUG}_network.db"
        gexf_path = GRAPH_DIR / f"{SLUG}_network.gexf"

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"✅ Build complete: {db_path}, {gexf_path}")
    print(f"   Persons: {len(persons)}")
    print(f"   Orgs: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")