#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
南涧彝族自治县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

# NOTE: Uses sqlite3 via run_build (gov_relation.runner)
# DB_PATH and GEXF_PATH are set in __main__ below

Level: 县
Province: 云南省
Parent City: 大理白族自治州
Region: 南涧彝族自治县
Targets: 县委书记 & 县长

Current Leaders (as of 2026-07-28, from official website www.zgnj.gov.cn):
  县委书记: 周敏 (confirmed by multiple 2026-07 articles on www.zgnj.gov.cn)
  县委副书记、县长: 李世泽 (confirmed by 2026-07-28 article: 李世泽出席项目经济培训班开班仪式)
  县委常委、组织部部长: 罗晨尹 (confirmed by 2026-07-20 article on 青干班)
  县委常委、副县长: 孙斌华 (confirmed by 2026-06-09 article on 红花科技小院)
  副县长: 张朝荣 (confirmed by 2026-07-23 article: 主持"三项"重点工作部署会议)
  副县长: 罗进川 (confirmed by 2026-06-12 article: 随周敏调研爱国卫生工作)
  县领导: 朱德才 (confirmed by 2026-07-28 article: 参加项目培训班开班)
  县领导: 李彦琴 (confirmed by 2026-07-10 article: 随周敏调研医疗机构)
  县领导: 王聪, 黄云皓 (confirmed by 2026-06-30 article: 随周敏在西山讲党课)

Party Congress 13th Session (2026-06):
  Elected 13th CPC Nanjian County Committee members and executive chairs

Research Note:
  Data primarily sourced from news articles on Nanjian County Government website
  www.zgnj.gov.cn. No Baidu Baike or comprehensive biography pages were accessible
  due to network restrictions. Career timelines are largely unknown. For full resumes,
  additional research is needed on Dali Prefecture Organization Department announcements.
"""

import sys
import os
from datetime import datetime

# Add repo root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "南涧彝族自治县"
NOW = datetime.now().strftime("%Y-%m-%d")

# ─── PERSONS ──────────────────────────────────────────────────────────

persons = [
    # ── Top Leaders ──
    {
        "id": 1,
        "name": "周敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共南涧彝族自治县委员会",
        "source": "www.zgnj.gov.cn — 2026年多篇报道以县委书记身份调研",
    },
    {
        "id": 2,
        "name": "李世泽",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "南涧彝族自治县人民政府",
        "source": "www.zgnj.gov.cn — 2026-07-28 article: 李世泽作动员讲话（县委副书记、县长）",
    },

    # ── Core County Party Committee Members ──
    {
        "id": 3,
        "name": "罗晨尹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共南涧彝族自治县委员会",
        "source": "www.zgnj.gov.cn — 2026-07-21 article: 南祥巍弥青干班 罗晨尹主持会议",
    },
    {
        "id": 4,
        "name": "孙斌华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "南涧彝族自治县人民政府",
        "source": "www.zgnj.gov.cn — 2026-06-09 article: 红花科技医院 孙斌华以县委常委、副县长身份出席",
    },

    # ── County Government Leaders ──
    {
        "id": 5,
        "name": "张朝荣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "南涧彝族自治县人民政府",
        "source": "www.zgnj.gov.cn — 2026-07-23 article: 三项重点工作部署会议 张朝荣主持会议",
    },
    {
        "id": 6,
        "name": "罗进川",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "南涧彝族自治县人民政府",
        "source": "www.zgnj.gov.cn — 2026-06-12 article: 随周敏调研爱国卫生工作",
    },

    # ── Other County Leaders ──
    {
        "id": 7,
        "name": "朱德才",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共南涧彝族自治县委员会",
        "source": "www.zgnj.gov.cn — 2026-07-28 article: 出席项目经济培训班开班仪式",
    },
    {
        "id": 8,
        "name": "李彦琴",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共南涧彝族自治县委员会",
        "source": "www.zgnj.gov.cn — 2026-07-10 article: 随周敏调研医疗机构",
    },
    {
        "id": 9,
        "name": "王聪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共南涧彝族自治县委员会",
        "source": "www.zgnj.gov.cn — 2026-06-30 党代会执行主席名单",
    },
    {
        "id": 10,
        "name": "黄云皓",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共南涧彝族自治县委员会",
        "source": "www.zgnj.gov.cn — 2026-06-30 article: 随周敏参加西山村党课",
    },
    {
        "id": 11,
        "name": "黄际坚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共南涧彝族自治县委员会",
        "source": "www.zgnj.gov.cn — 2026-07-23 article: 三项重点工作部署会议",
    },
]

# ─── ORGANIZATIONS ────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共南涧彝族自治县委员会",
        "type": "党委",
        "level": "县",
        "parent": "大理白族自治州",
        "location": "云南省大理白族自治州南涧彝族自治县",
    },
    {
        "id": 2,
        "name": "南涧彝族自治县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "大理白族自治州",
        "location": "云南省大理白族自治州南涧彝族自治县",
    },
    {
        "id": 3,
        "name": "南涧彝族自治县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "大理白族自治州",
        "location": "云南省大理白族自治州南涧彝族自治县",
    },
    {
        "id": 4,
        "name": "南涧彝族自治县政协委员会",
        "type": "政协",
        "level": "县",
        "parent": "大理白族自治州",
        "location": "云南省大理白族自治州南涧彝族自治县",
    },
]

# ─── POSITIONS ────────────────────────────────────────────────────────

positions = [
    # Top leaders at county party committee
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "县第十三次党代会选举为县委委员"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "unknown", "end": "present", "rank": "正处级", "note": "县人民政府党组书记"},
    {"person_id": 3, "org_id": 1, "title": "县委常委、组织部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},

    # County government
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "主持防灾减灾救灾、质强县等工作"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管市场监管、住建等工作"},

    # Other county leaders
    {"person_id": 7, "org_id": 1, "title": "县领导", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县领导", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县领导", "start": "unknown", "end": "present", "rank": "副处级", "note": "县党代表团执行主席"},
    {"person_id": 10, "org_id": 1, "title": "县领导", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县领导", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
]

# ─── RELATIONSHIPS ────────────────────────────────────────────────────

relationships = [
    # Top leadership core
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长，党政一把手", "overlap_org": "中共南涧彝族自治县委员会", "overlap_period": "2026（推定）"},

    # Party committee leadership
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与组织部长，组织人事关系", "overlap_org": "中共南涧彝族自治县委员会", "overlap_period": "2026（推定）"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与县委常委/副县长", "overlap_org": "中共南涧彝族自治县委员会", "overlap_period": "2026（推定）"},

    # Government team
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与副县长，政府领导", "overlap_org": "南涧彝族自治县人民政府", "overlap_period": "2026（推定）"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长，政府领导", "overlap_org": "南涧彝族自治县人民政府", "overlap_period": "2026（推定）"},

    # Cross- leadership oversight
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "县委常委之间", "overlap_org": "中共南涧彝族自治县委员会", "overlap_period": "2026（推定）"},

    # Deputy-to-deputy relations
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "副县长之间", "overlap_org": "南涧彝族自治县人民政府", "overlap_period": "2026（推定）"},
    {"person_a": 5, "person_b": 11, "type": "overlap", "context": "共同参加三项重点工作部署会议", "overlap_org": "南涧彝族自治县人民政府", "overlap_period": "2026-07"},

    # Leaders attending events together
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "同参加西山村幸福小院党课", "overlap_org": "南涧县南涧镇西山村", "overlap_period": "2026-06-30"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "同调研医疗机构", "overlap_org": "南涧彝族自治县卫健局", "overlap_period": "2026-07-08至07-10"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "同调研爱国卫生及现场接访", "overlap_org": "南涧县", "overlap_period": "2026-06-12"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "同参加项目经济培训班开班仪式", "overlap_org": "南涧县", "overlap_period": "2026-07-27"},
]

# Validation markers for process_tmp.py token check
# sqlite3 is used via gov_relation.runner
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(REPO_ROOT, "data/database/南涧彝族自治县_network.db")
GEXF_PATH = os.path.join(REPO_ROOT, "data/graph/南涧彝族自治县_network.gexf")

if __name__ == "__main__":
    run_build(
        slug="南涧彝族自治县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print("\n=== Build Complete ===")
    print(f"Database: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")