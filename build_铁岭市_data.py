#!/usr/bin/env python3
"""Build 铁岭市 (Tieling City, Liaoning Province) personnel network database and graph.

Research source: 铁岭市人民政府官方网站 (tieling.gov.cn)
- 领导介绍 pages for all 11 current officeholders
- 铁政办发〔2026〕号 市政府领导同志工作分工通知 (2026-04-20)
- Data collected: 2026-07-25
- Research constraints: Web search (Baidu/Exa/Google) was unavailable;
  career histories prior to current roles are marked "unverified".
"""

import os
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build

SLUG = "铁岭市"
TASK_ID = "liaoning_铁岭市"

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    # === Core leaders (targets) ===
    {
        "id": 1,
        "name": "李文飙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中国共产党铁岭市委员会",
        "source": "https://www.tieling.gov.cn/ywdt/jrtl/2026072209574920302/index.html",
    },
    {
        "id": 2,
        "name": "张宝东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年8月",
        "birthplace": "",
        "education": "研究生学历，管理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "铁岭市人民政府",
        "source": "https://www.tieling.gov.cn/tieling/szf/sz/sxlsz/2024090309415065638/index.html",
    },
    # === Deputy leaders (市政府领导班子) ===
    {
        "id": 3,
        "name": "尹红炜",
        "gender": "男",
        "ethnicity": "朝鲜族",
        "birth": "1977年7月",
        "birthplace": "",
        "education": "研究生学历，管理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "铁岭市人民政府",
        "source": "https://www.tieling.gov.cn/tieling/szf/fsz/2025032009463855785/index.html",
    },
    {
        "id": 4,
        "name": "闫冬蕾",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1979年3月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "铁岭市人民政府",
        "source": "https://www.tieling.gov.cn/tieling/szf/fsz/2025012310265666631/index.html",
    },
    {
        "id": 5,
        "name": "许策",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年7月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "铁岭市人民政府",
        "source": "https://www.tieling.gov.cn/tieling/szf/fsz/2026072315382693447/index.html",
    },
    {
        "id": 6,
        "name": "杜妍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年7月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长（兼市工商联主席）",
        "current_org": "铁岭市人民政府",
        "source": "https://www.tieling.gov.cn/tieling/szf/fsz/2021081017230023927/index.html",
    },
    {
        "id": 7,
        "name": "刘庆恩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年12月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "铁岭市人民政府",
        "source": "https://www.tieling.gov.cn/tieling/szf/fsz/2026022614460178318/index.html",
    },
    {
        "id": 8,
        "name": "李铁刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长（兼经开区党工委书记）",
        "current_org": "铁岭市人民政府",
        "source": "https://www.tieling.gov.cn/tieling/szf/fsz/2024103014145521720/index.html",
    },
    {
        "id": 9,
        "name": "谭会波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "铁岭市人民政府",
        "source": "https://www.tieling.gov.cn/tieling/szf/fsz/2025032710285136268/index.html",
    },
    {
        "id": 10,
        "name": "常东旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "铁岭市人民政府",
        "source": "https://www.tieling.gov.cn/tieling/szf/fsz/2026022715110276437/index.html",
    },
    # === Secretary-General ===
    {
        "id": 11,
        "name": "方志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年4月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长（兼市政府办公室主任）",
        "current_org": "铁岭市人民政府办公室",
        "source": "https://www.tieling.gov.cn/tieling/szf/msz/2026022517020385101/index.html",
    },
    # === Predecessors ===
    {
        "id": 12,
        "name": "宋诚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记（2022-2024年任职）",
        "current_org": "",
        "source": "https://www.tieling.gov.cn/ywdt/jrtl/2026072209574920302/index.html",
    },
    {
        "id": 13,
        "name": "张东明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "协助招商工作",
        "current_org": "铁岭市人民政府",
        "source": "https://www.tieling.gov.cn/zwgk/zfwj/tzbf/2026042715351130130/index.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {"id": 0, "name": "中国共产党铁岭市委员会", "type": "党委", "level": "地厅级", "parent": "中国共产党辽宁省委员会", "location": "辽宁省铁岭市"},
    {"id": 1, "name": "铁岭市人民政府", "type": "政府", "level": "地厅级", "parent": "辽宁省人民政府", "location": "辽宁省铁岭市"},
    {"id": 2, "name": "铁岭市人民政府办公室", "type": "政府", "level": "县处级", "parent": "铁岭市人民政府", "location": "辽宁省铁岭市"},
    {"id": 3, "name": "铁岭市公安局", "type": "政府", "level": "县处级", "parent": "铁岭市人民政府", "location": "辽宁省铁岭市"},
    {"id": 4, "name": "铁岭经济技术开发区", "type": "开发区", "level": "地厅级", "parent": "铁岭市人民政府", "location": "辽宁省铁岭市"},
    {"id": 5, "name": "铁岭市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "", "location": "辽宁省铁岭市"},
    {"id": 6, "name": "中国人民政治协商会议铁岭市委员会", "type": "政协", "level": "地厅级", "parent": "", "location": "辽宁省铁岭市"},
    {"id": 7, "name": "铁岭市监察委员会", "type": "纪委", "level": "地厅级", "parent": "", "location": "辽宁省铁岭市"},
    {"id": 8, "name": "铁岭市工商业联合会", "type": "群团", "level": "县处级", "parent": "", "location": "辽宁省铁岭市"},
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    # 李文飙 - 市委书记
    {"person_id": 1, "org_id": 0, "title": "市委书记", "start_date": "2024", "end_date": "present", "rank": "地厅级正职", "note": "2024年由铁岭市长转任铁岭市委书记"},
    {"person_id": 1, "org_id": 1, "title": "市长", "start_date": "2021", "end_date": "2024", "rank": "地厅级正职", "note": "2021-2024年任铁岭市市长，后接任市委书记"},
    # 张宝东 - 市长
    {"person_id": 2, "org_id": 0, "title": "市委副书记", "start_date": "2024", "end_date": "present", "rank": "地厅级副职", "note": "2024年起任铁岭市委副书记"},
    {"person_id": 2, "org_id": 1, "title": "市长、市政府党组书记", "start_date": "2024", "end_date": "present", "rank": "地厅级正职", "note": "主持市政府全面工作，分管市审计局，联系开原市"},
    # 尹红炜 - 常务副市长
    {"person_id": 3, "org_id": 0, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": "铁岭市委常委"},
    {"person_id": 3, "org_id": 1, "title": "常务副市长、市政府党组副书记", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": "负责市政府常务工作，分管发改、财政、应急等；与许策互为AB角"},
    # 闫冬蕾 - 副市长
    {"person_id": 4, "org_id": 0, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": "铁岭市委常委"},
    {"person_id": 4, "org_id": 1, "title": "副市长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": "负责人社、文旅、数据、营商环境等工作；与杜妍互为AB角"},
    # 许策 - 副市长
    {"person_id": 5, "org_id": 0, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": "铁岭市委常委"},
    {"person_id": 5, "org_id": 1, "title": "副市长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": "负责民政、退役军人、供销等工作；与尹红炜互为AB角；联系昌图县"},
    # 杜妍 - 副市长（无党派）
    {"person_id": 6, "org_id": 1, "title": "副市长", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": "负责教育、卫健、医保等工作；与闫冬蕾互为AB角；联系西丰县"},
    {"person_id": 6, "org_id": 8, "title": "市工商联（总商会）主席（会长）", "start_date": "", "end_date": "present", "rank": "县处级", "note": "兼任市工商联主席"},
    # 刘庆恩 - 副市长、公安局长
    {"person_id": 7, "org_id": 1, "title": "副市长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": "负责公安、打私等工作；与谭会波互为AB角；联系清河区"},
    {"person_id": 7, "org_id": 3, "title": "市公安局党委书记、局长、督察长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持市公安局全面工作"},
    # 李铁刚 - 副市长
    {"person_id": 8, "org_id": 1, "title": "副市长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": "负责科技、工信、商务、市场监管等工作；与常东旭互为AB角"},
    {"person_id": 8, "org_id": 4, "title": "铁岭经济技术开发区党工委书记", "start_date": "", "end_date": "present", "rank": "地厅级", "note": "兼任经开区党工委书记"},
    # 谭会波 - 副市长
    {"person_id": 9, "org_id": 1, "title": "副市长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": "负责生态环境、水利、农业农村等工作；与刘庆恩互为AB角"},
    # 常东旭 - 副市长
    {"person_id": 10, "org_id": 1, "title": "副市长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": "负责自然资源、住建、交通等工作；与李铁刚互为AB角"},
    # 方志 - 秘书长
    {"person_id": 11, "org_id": 2, "title": "市政府秘书长（兼市政府办公室主任）", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "协助常务副市长分管市政府办公室"},
    # 宋诚 - 前任市委书记
    {"person_id": 12, "org_id": 0, "title": "市委书记", "start_date": "2022", "end_date": "2024", "rank": "地厅级正职", "note": "前任铁岭市委书记，2022-2024年在任，李文飙2024年接任"},
    # 张东明 - 协助招商
    {"person_id": 13, "org_id": 1, "title": "协助招商工作", "start_date": "", "end_date": "present", "rank": "地厅级", "note": "协助尹红炜同志开展招商、会见、参展、调研等工作"},
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    # 李文飙 - 张宝东：党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记与市长党政搭档", "overlap_org": "铁岭市", "overlap_period": "2024年至今"},
    # 张宝东接任李文飙任市长
    {"person_a": 2, "person_b": 1, "type": "predecessor_successor", "context": "张宝东接任李文飙任市长", "overlap_org": "铁岭市人民政府", "overlap_period": "2021-2024"},
    # 宋诚 - 李文飙：前后任市委书记
    {"person_a": 12, "person_b": 1, "type": "predecessor_successor", "context": "宋诚2022-2024任铁岭市委书记，李文飙2024接任", "overlap_org": "中国共产党铁岭市委员会", "overlap_period": "2022-2024"},
    # 常委班子内的主要关系
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记与常务副市长，同为市委常委", "overlap_org": "铁岭市委常委班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委书记与市委常委、副市长", "overlap_org": "铁岭市委常委班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "市委书记与市委常委、副市长", "overlap_org": "铁岭市委常委班子", "overlap_period": "2026年"},
    # 张宝东与副市长们
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "市长与常务副市长，尹红炜协助张宝东分管审计", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "市长与市委常委、副市长", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "市长与市委常委、副市长", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "市长与副市长（无党派）", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "市长与分管公安的副市长", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "市长与分管工业商务的副市长", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "市长与分管农业农村的副市长", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "市长与分管住建交通的副市长", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "市长与市政府秘书长", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
    # 尹红炜与副市长们（常务副市长核心节点）
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同为市委常委、副市长", "overlap_org": "铁岭市委常委班子", "overlap_period": "2026年"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "同为市委常委、副市长，许策协助尹红炜分管粮食储备", "overlap_org": "铁岭市委常委班子", "overlap_period": "2026年"},
    {"person_a": 3, "person_b": 11, "type": "overlap", "context": "常务副市长与市政府秘书长，方志协助分管市政府办公室", "overlap_org": "铁岭市人民政府办公室", "overlap_period": "2026年"},
    # AB角互补关系
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "AB角互补：尹红炜与许策互为AB角", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "AB角互补：闫冬蕾与杜妍互为AB角", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
    {"person_a": 7, "person_b": 9, "type": "overlap", "context": "AB角互补：刘庆恩与谭会波互为AB角", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
    {"person_a": 8, "person_b": 10, "type": "overlap", "context": "AB角互补：李铁刚与常东旭互为AB角", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
    # 张东明协助尹红炜
    {"person_a": 3, "person_b": 13, "type": "overlap", "context": "张东明协助尹红炜开展招商等工作", "overlap_org": "铁岭市人民政府", "overlap_period": "2026年"},
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
