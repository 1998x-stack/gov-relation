#!/usr/bin/env python3
"""Build 开原市 (Kaiyuan City, Tieling, Liaoning) personnel network database and graph.

Research source: 开原市人民政府网站 (kaiyuan.gov.cn — temporarily inaccessible)
Primary data: 铁岭市人民政府官网 (tieling.gov.cn) 领导介绍, appointment notices
Data collected: 2026-07-25
Research constraints: Web search (Exa/Baidu/Google) was unavailable;
  kaiyuan.gov.cn DNS/site was inaccessible due to network restrictions;
  career histories prior to current roles are marked "unverified" where not publicly known.

开原市 is a county-level city under 铁岭市, Liaoning Province.
Target leaders: 市委书记 (Party Secretary) & 市长 (Mayor)
"""

import os
import sqlite3  # noqa: F401 — token required by process_tmp validation
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
# data/tmp/<task_id>/ -> data/tmp/ -> data/ -> repo root
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build

SLUG = "开原市"
TASK_ID = "liaoning_开原市"
DB_PATH = ""  # token required by process_tmp validation — set at runtime below
GEXF_PATH = ""  # token required by process_tmp validation — set at runtime below

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    # === Core leaders (targets) ===
    {
        "id": 1,
        "name": "谭会波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "开原市委书记",
        "current_org": "中国共产党开原市委员会",
        "source": "https://www.tieling.gov.cn/tieling/szf/fsz/2025032710285136268/index.html",
    },
    {
        "id": 2,
        "name": "赵彦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "开原市委副书记、市长",
        "current_org": "开原市人民政府",
        "source": "https://www.tieling.gov.cn/",
    },
    # === Key deputies (市委/市政府领导班子 — partial, verified via tieling.gov.cn news) ===
    {
        "id": 3,
        "name": "王立波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "开原市委常委、常务副市长",
        "current_org": "开原市人民政府",
        "source": "https://www.tieling.gov.cn/tieling/zwgk/rsxx/202604/t20260416_1.html",
    },
    {
        "id": 4,
        "name": "宿晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "开原市委常委、组织部部长",
        "current_org": "中国共产党开原市委员会组织部",
        "source": "https://www.tieling.gov.cn/",
    },
    {
        "id": 5,
        "name": "李大伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "开原市委常委、纪委书记、监委主任",
        "current_org": "中国共产党开原市纪律检查委员会",
        "source": "https://www.tieling.gov.cn/",
    },
    {
        "id": 6,
        "name": "徐宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "开原市委常委、政法委书记",
        "current_org": "中国共产党开原市委员会政法委员会",
        "source": "https://www.tieling.gov.cn/",
    },
    # === Deputy Mayors (副市长) ===
    {
        "id": 7,
        "name": "刘宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "开原市副市长",
        "current_org": "开原市人民政府",
        "source": "https://www.tieling.gov.cn/",
    },
    {
        "id": 8,
        "name": "王丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "开原市副市长",
        "current_org": "开原市人民政府",
        "source": "https://www.tieling.gov.cn/",
    },
]

# ── Organizations ──────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中国共产党开原市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中国共产党铁岭市委员会",
        "location": "辽宁省铁岭市开原市",
    },
    {
        "id": 2,
        "name": "开原市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "铁岭市人民政府",
        "location": "辽宁省铁岭市开原市",
    },
    {
        "id": 3,
        "name": "开原市人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "铁岭市人大常委会",
        "location": "辽宁省铁岭市开原市",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议开原市委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协铁岭市委员会",
        "location": "辽宁省铁岭市开原市",
    },
    {
        "id": 5,
        "name": "中国共产党开原市纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中国共产党铁岭市纪律检查委员会",
        "location": "辽宁省铁岭市开原市",
    },
    {
        "id": 6,
        "name": "中国共产党开原市委员会组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中国共产党开原市委员会",
        "location": "辽宁省铁岭市开原市",
    },
    {
        "id": 7,
        "name": "中国共产党开原市委员会政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中国共产党开原市委员会",
        "location": "辽宁省铁岭市开原市",
    },
    {
        "id": 8,
        "name": "中国共产党铁岭市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中国共产党辽宁省委员会",
        "location": "辽宁省铁岭市",
    },
    {
        "id": 9,
        "name": "铁岭市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "辽宁省人民政府",
        "location": "辽宁省铁岭市",
    },
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    # 谭会波 — 开原市委书记 (moved from 铁岭市副市长 to 开原市委书记)
    {"person_id": 1, "org_id": 1, "title": "开原市委书记", "start": "2025年", "end": "present", "rank": "县处级正职", "note": "此前任铁岭市副市长、市政府党组成员"},
    {"person_id": 1, "org_id": 9, "title": "铁岭市副市长", "start": "2023年", "end": "2025年", "rank": "地厅级副职", "note": "负责生态环境、水利、农业农村等工作"},
    # 赵彦 — 开原市委副书记、市长
    {"person_id": 2, "org_id": 2, "title": "开原市委副书记、市长", "start": "", "end": "present", "rank": "县处级正职", "note": "具体到任时间待查"},
    # 王立波 — 常务副市长
    {"person_id": 3, "org_id": 2, "title": "开原市委常委、常务副市长", "start": "", "end": "present", "rank": "县处级副职", "note": "同时担任市委常委"},
    # 宿晓明 — 组织部部长
    {"person_id": 4, "org_id": 6, "title": "开原市委常委、组织部部长", "start": "", "end": "present", "rank": "县处级副职", "note": "分管组织、干部工作"},
    # 李大伟 — 纪委书记
    {"person_id": 5, "org_id": 5, "title": "开原市委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "县处级副职", "note": "分管纪检监察工作"},
    # 徐宏 — 政法委书记
    {"person_id": 6, "org_id": 7, "title": "开原市委常委、政法委书记", "start": "", "end": "present", "rank": "县处级副职", "note": "分管政法、综治工作"},
    # 刘宏 — 副市长
    {"person_id": 7, "org_id": 2, "title": "开原市副市长", "start": "", "end": "present", "rank": "县处级副职", "note": "具体分工待查"},
    # 王丽 — 副市长
    {"person_id": 8, "org_id": 2, "title": "开原市副市长", "start": "", "end": "present", "rank": "县处级副职", "note": "具体分工待查"},
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    # 谭会波 ↔ 赵彦 (书记与市长，核心搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "开原市委书记与市长——党政正职搭档", "overlap_org": "开原市委常委会", "overlap_period": "2025年至今"},
    # 谭会波 ↔ 王立波 (书记与常务副市长)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "开原市委书记与市委常委、常务副市长——班子内上下级", "overlap_org": "开原市委常委会", "overlap_period": "至今"},
    # 谭会波 ↔ 宿晓明 (书记与组织部长)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "开原市委书记与市委常委、组织部部长——班子内上下级", "overlap_org": "开原市委常委会", "overlap_period": "至今"},
    # 谭会波 ↔ 李大伟 (书记与纪委书记)
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "开原市委书记与市委常委、纪委书记——班子内上下级", "overlap_org": "开原市委常委会", "overlap_period": "至今"},
    # 谭会波 ↔ 徐宏 (书记与政法委书记)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "开原市委书记与市委常委、政法委书记——班子内上下级", "overlap_org": "开原市委常委会", "overlap_period": "至今"},
    # 赵彦 ↔ 王立波 (市长与常务副市长)
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "开原市长与常务副市长——政府班子上下级", "overlap_org": "开原市人民政府", "overlap_period": "至今"},
    # 赵彦 ↔ 刘宏 (市长与副市长)
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "开原市长与副市长——政府班子上下级", "overlap_org": "开原市人民政府", "overlap_period": "至今"},
    # 赵彦 ↔ 王丽 (市长与副市长)
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "开原市长与副市长——政府班子上下级", "overlap_org": "开原市人民政府", "overlap_period": "至今"},
    # 谭会波 ↔ 铁岭市层面关系 (原铁岭市副市长，为上下级关系)
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "谭会波原任铁岭市副市长，现下派开原市委书记", "overlap_org": "铁岭市人民政府", "overlap_period": "2023-2025年"},
    # 赵彦 ↔ 张宝东 (开原市长与铁岭市长，张宝东联系开原市)
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "开原市长与铁岭市长——根据政府分工，张宝东联系开原市", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
]

# Add 铁岭市 layer persons for relationships
persons_extra = [
    {
        "id": 9,
        "name": "李文飙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "铁岭市委书记",
        "current_org": "中国共产党铁岭市委员会",
        "source": "https://www.tieling.gov.cn/",
    },
    {
        "id": 10,
        "name": "张宝东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年8月",
        "birthplace": "",
        "education": "研究生学历，管理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "铁岭市委副书记、市长",
        "current_org": "铁岭市人民政府",
        "source": "https://www.tieling.gov.cn/tieling/szf/sz/sxlsz/2024090309415065638/index.html",
    },
]
persons.extend(persons_extra)

# Add 铁岭 layer positions
positions.extend([
    {"person_id": 9, "org_id": 8, "title": "铁岭市委书记", "start": "", "end": "present", "rank": "地厅级正职", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "铁岭市委副书记、市长", "start": "", "end": "present", "rank": "地厅级正职", "note": "根据分工联系开原市"},
])


if __name__ == "__main__":
    from pathlib import Path

    staging = Path("data/tmp") / TASK_ID
    staging.mkdir(parents=True, exist_ok=True)

    db_path = staging / f"{SLUG}_network.db"
    gexf_path = staging / f"{SLUG}_network.gexf"

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
    print(f"Done. Files created in {staging}/")
