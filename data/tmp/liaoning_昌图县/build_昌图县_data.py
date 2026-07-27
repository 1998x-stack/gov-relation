#!/usr/bin/env python3
"""Build 昌图县 (Changtu County, Tieling City, Liaoning Province) personnel network database and graph.

Research source: 昌图县人民政府官方网站 (changtu.gov.cn)
- 昌政办发〔2025〕7号 县政府领导同志工作分工通知 (2025-08-15)
- Government meeting records 2024-2025
- News articles: 县委书记孙佐强督导检查节前食品安全工作 (2026-06-16)
- Data collected: 2026-07-25
- Research constraints: Web search (Exa/Baidu/Google) was rate-limited or blocked;
  career histories prior to current roles are marked "unverified" except where official source confirms.
"""

import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build

SLUG = "昌图县"
TASK_ID = "liaoning_昌图县"

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    # === Core leaders (targets) ===
    {
        "id": 1,
        "name": "孙佐强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中国共产党昌图县委员会",
        "source": "https://www.changtu.gov.cn/changtu/ywdt/zwyw/2026061609015266997/index.html",
    },
    {
        "id": 3,
        "name": "待查_县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "昌图县人民政府",
        "source": "",
    },
    # === Deputy leaders (县政府领导班子, from 昌政办发〔2025〕7号) ===
    {
        "id": 4,
        "name": "刘婉夏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "昌图县人民政府",
        "source": "https://www.changtu.gov.cn/changtu/zwgk/zfwj13/xzfbgswj/2025120315001136917/index.html",
    },
    {
        "id": 5,
        "name": "郑仕才",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "昌图县人民政府",
        "source": "https://www.changtu.gov.cn/changtu/zwgk/zfwj13/xzfbgswj/2025120315001136917/index.html",
    },
    {
        "id": 6,
        "name": "李刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "昌图县人民政府",
        "source": "https://www.changtu.gov.cn/changtu/zwgk/zfwj13/xzfbgswj/2025120315001136917/index.html",
    },
    {
        "id": 7,
        "name": "赵俊峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（兼公安局局长）",
        "current_org": "昌图县人民政府",
        "source": "https://www.changtu.gov.cn/changtu/zwgk/zfwj13/xzfbgswj/2025120315001136917/index.html",
    },
    {
        "id": 8,
        "name": "寇巍威",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "昌图县人民政府",
        "source": "https://www.changtu.gov.cn/changtu/zwgk/zfwj13/xzfbgswj/2025120315001136917/index.html",
    },
    {
        "id": 9,
        "name": "王春东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "昌图县人民政府",
        "source": "https://www.changtu.gov.cn/changtu/zwgk/zfwj13/xzfbgswj/2025120315001136917/index.html",
    },
    {
        "id": 10,
        "name": "张坤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "昌图县人民政府",
        "source": "https://www.changtu.gov.cn/changtu/zwgk/zfwj13/xzfbgswj/2025120315001136917/index.html",
    },
    {
        "id": 11,
        "name": "李迪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府办公室主任",
        "current_org": "昌图县人民政府办公室",
        "source": "https://www.changtu.gov.cn/changtu/zwgk/zfwj13/xzfbgswj/2025120315001136917/index.html",
    },
    # === Predecessors ===
    {
        "id": 12,
        "name": "苗宇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县长（~2021-2024年任职）",
        "current_org": "",
        "source": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/lzyj/zfhy/2025022014161474714/index.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {"id": 0, "name": "中国共产党昌图县委员会", "type": "党委", "level": "县处级", "parent": "中国共产党铁岭市委员会", "location": "辽宁省铁岭市昌图县"},
    {"id": 1, "name": "昌图县人民政府", "type": "政府", "level": "县处级", "parent": "铁岭市人民政府", "location": "辽宁省铁岭市昌图县"},
    {"id": 2, "name": "昌图县人民政府办公室", "type": "政府", "level": "乡镇级", "parent": "昌图县人民政府", "location": "辽宁省铁岭市昌图县"},
    {"id": 3, "name": "昌图县公安局", "type": "政府", "level": "乡镇级", "parent": "昌图县人民政府", "location": "辽宁省铁岭市昌图县"},
    {"id": 4, "name": "昌图县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "辽宁省铁岭市昌图县"},
    {"id": 5, "name": "中国人民政治协商会议昌图县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "辽宁省铁岭市昌图县"},
    {"id": 6, "name": "昌图县监察委员会", "type": "纪委", "level": "县处级", "parent": "", "location": "辽宁省铁岭市昌图县"},
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    # 孙佐强 - 现任县委书记，前任县长
    {"person_id": 1, "org_id": 0, "title": "县委书记", "start_date": "~2025/2026", "end_date": "present", "rank": "县处级正职", "note": "接任县委书记，2026年6月新闻报道已称'县委书记孙佐强'"},
    {"person_id": 1, "org_id": 1, "title": "县长、县政府党组书记", "start_date": "~2021/2024", "end_date": "~2025/2026", "rank": "县处级正职", "note": "任县长期间主持县政府全面工作；2025年8月分工通知仍为县长；2025年3月28日以'县委副书记、县长'身份主持会议"},
    # 县长 - 待查
    {"person_id": 3, "org_id": 1, "title": "县长", "start_date": "unknown", "end_date": "present", "rank": "县处级正职", "note": "孙佐强转任县委书记后，县长人选待查"},
    # 刘婉夏 - 常务副县长
    {"person_id": 4, "org_id": 1, "title": "常务副县长、县政府党组副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责县政府常务工作，分管发改、财政、人社、应急等；协助县长分管审计"},
    # 郑仕才 - 副县长
    {"person_id": 5, "org_id": 1, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责招商引资、商务、外事工作"},
    # 李刚 - 副县长
    {"person_id": 6, "org_id": 1, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责农业农村、乡村振兴、水利、生态环境、林业草原等工作"},
    # 赵俊峰 - 副县长、公安局长
    {"person_id": 7, "org_id": 1, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责公安、司法、打击走私等工作"},
    {"person_id": 7, "org_id": 3, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "乡镇级正职", "note": "负责县公安局全面工作"},
    # 寇巍威 - 副县长
    {"person_id": 8, "org_id": 1, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责教育、文旅、体育、卫健、医保、供销等工作"},
    # 王春东 - 副县长
    {"person_id": 9, "org_id": 1, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责民政、自然资源、规划、交通、住建、综合执法等工作"},
    # 张坤 - 副县长
    {"person_id": 10, "org_id": 1, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责工业、科技、市场监管、退役军人、营商环境等工作"},
    # 李迪 - 办公室主任
    {"person_id": 11, "org_id": 2, "title": "县政府办公室主任", "start_date": "", "end_date": "present", "rank": "乡镇级正职", "note": "协助处理县政府日常工作"},
    # 苗宇 - 前任县长
    {"person_id": 12, "org_id": 1, "title": "县长", "start_date": "~2021", "end_date": "~2024", "rank": "县处级正职", "note": "前任县长，主持县政府常务会议至2024年6月；2024年后由孙佐强接任县长"},
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    # 孙佐强→苗宇：前后任县长
    {"person_a": 1, "person_b": 12, "type": "predecessor_successor", "context": "苗宇~2021-2024年任昌图县长，孙佐强接任县长", "overlap_org": "昌图县人民政府", "overlap_period": "~2021-~2024"},
    # 孙佐强→刘婉夏：县长与常务副县长
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "孙佐强任县长/县委书记期间与常务副县长刘婉夏共事", "overlap_org": "昌图县人民政府", "overlap_period": "2025-2026"},
    # 孙佐强→副县长们：县长与各副县长
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县长与分管招商的副县长", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县长与分管农业农村的副县长", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县长与分管公安的副县长", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县长与分管教育文旅的副县长", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县长与分管住建交通的副县长", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县长与分管工业科技的副县长", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县长与县政府办公室主任", "overlap_org": "昌图县人民政府办公室", "overlap_period": "2025"},
    # 刘婉夏与副县长们（常务副县长核心节点）
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "常务副县长与其他副县长共事", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "常务副县长与农业农村副县长", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "常务副县长与公安副县长", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "常务副县长与教育文旅副县长", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "常务副县长与住建交通副县长", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "常务副县长与工业科技副县长", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
    {"person_a": 4, "person_b": 11, "type": "overlap", "context": "常务副县长与县政府办公室主任", "overlap_org": "昌图县人民政府办公室", "overlap_period": "2025"},
    # AB角互补关系
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "AB角互补：刘婉夏与寇巍威互为AB角", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
    {"person_a": 6, "person_b": 9, "type": "overlap", "context": "AB角互补：李刚与王春东互为AB角", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
    {"person_a": 7, "person_b": 10, "type": "overlap", "context": "AB角互补：赵俊峰与张坤互为AB角", "overlap_org": "昌图县人民政府", "overlap_period": "2025"},
]

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
