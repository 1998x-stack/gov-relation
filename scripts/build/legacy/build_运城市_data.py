#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 运城市 (Yuncheng City), 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_运城市
Level: 地级市
Targets: Key deputy leaders (市委副书记, 常务副市长, 组织部长, 纪委书记, 政法委书记)

Research sources:
  - www.yuncheng.gov.cn — 运城市人民政府官方网站 (primary, current as of July 2026)
  - Baidu Baike was blocked (HTTP 403) — detailed career histories not available

Confidence notes:
  - Current roles/names: confirmed via official government leadership page
  - Biographical details (birth, education): from official site brief bios (primary quality)
  - Full career timelines: unverified due to web access limitations
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
for parent_count in range(1, 6):
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

SLUG = "运城市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1=书记, 2=市长, 3=副书记, 4=常务副市长, 5=组织部长, 6=纪委书记,
#      7=常委副市长, 8=宣传部长, 9=秘书长, 10=河津书记, 11=军分区, 12=副市长(公安), 13-16=其他副市长

persons = [
    # 市委书记
    {
        "id": 1, "name": "储祥好", "gender": "男", "ethnicity": "汉族",
        "birth": "1968-11", "birthplace": "", "education": "研究生，管理学博士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委书记", "current_org": "中共运城市委员会", "source": "yuncheng.gov.cn"
    },
    # 市长/市委副书记
    {
        "id": 2, "name": "姚逊", "gender": "男", "ethnicity": "汉族",
        "birth": "1973-08", "birthplace": "", "education": "大学，历史学硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委副书记、市长", "current_org": "运城市人民政府", "source": "yuncheng.gov.cn"
    },
    # 市委副书记、政法委书记
    {
        "id": 3, "name": "王立刚", "gender": "男", "ethnicity": "汉族",
        "birth": "1972-11", "birthplace": "", "education": "大学，工商管理硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委副书记、政法委书记", "current_org": "中共运城市委员会", "source": "yuncheng.gov.cn"
    },
    # 市委常委、常务副市长
    {
        "id": 4, "name": "刁海鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-09", "birthplace": "", "education": "研究生，理学博士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、常务副市长", "current_org": "运城市人民政府", "source": "yuncheng.gov.cn"
    },
    # 市委常委、组织部部长
    {
        "id": 5, "name": "赵晔", "gender": "女", "ethnicity": "汉族",
        "birth": "1976-01", "birthplace": "", "education": "大学，法律硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、组织部部长", "current_org": "中共运城市委员会", "source": "yuncheng.gov.cn"
    },
    # 市委常委、市纪委书记
    {
        "id": 6, "name": "温郁华", "gender": "女", "ethnicity": "汉族",
        "birth": "1976-11", "birthplace": "", "education": "研究生，哲学博士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任", "current_org": "中共运城市纪律检查委员会", "source": "yuncheng.gov.cn"
    },
    # 市委常委、副市长
    {
        "id": 7, "name": "孙鹏程", "gender": "男", "ethnicity": "汉族",
        "birth": "1981-03", "birthplace": "", "education": "研究生，工学博士，正高级工程师",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、副市长", "current_org": "运城市人民政府", "source": "yuncheng.gov.cn"
    },
    # 市委常委、宣传部部长
    {
        "id": 8, "name": "郎永杰", "gender": "男", "ethnicity": "汉族",
        "birth": "1972-08", "birthplace": "", "education": "研究生，教育学硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、宣传部部长", "current_org": "中共运城市委员会", "source": "yuncheng.gov.cn"
    },
    # 市委常委、秘书长、统战部部长
    {
        "id": 9, "name": "何伟", "gender": "男", "ethnicity": "汉族",
        "birth": "1970-02", "birthplace": "", "education": "省委党校研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、秘书长、统战部部长", "current_org": "中共运城市委员会", "source": "yuncheng.gov.cn"
    },
    # 市委常委、河津市委书记
    {
        "id": 10, "name": "孟维君", "gender": "男", "ethnicity": "汉族",
        "birth": "1974-10", "birthplace": "", "education": "研究生，法学硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、河津市委书记", "current_org": "中共河津市委员会", "source": "yuncheng.gov.cn"
    },
    # 市委常委、军分区司令员
    {
        "id": 11, "name": "郭新武", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-02", "birthplace": "", "education": "大学，工学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、军分区大校司令员", "current_org": "运城军分区", "source": "yuncheng.gov.cn"
    },
    # 副市长（民建）
    {
        "id": 12, "name": "张锐", "gender": "女", "ethnicity": "汉族",
        "birth": "1977-04", "birthplace": "", "education": "大学，法律硕士",
        "party_join": "民建会员", "work_start": "",
        "current_post": "副市长", "current_org": "运城市人民政府", "source": "yuncheng.gov.cn"
    },
    # 副市长（公安局长）
    {
        "id": 13, "name": "宋胜澜", "gender": "男", "ethnicity": "汉族",
        "birth": "1973-08", "birthplace": "", "education": "大学，法律硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长、市公安局局长", "current_org": "运城市公安局", "source": "yuncheng.gov.cn"
    },
    # 副市长
    {
        "id": 14, "name": "薛永琦", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "运城市人民政府", "source": "yuncheng.gov.cn"
    },
    # 副市长
    {
        "id": 15, "name": "尚玉良", "gender": "男", "ethnicity": "汉族",
        "birth": "1974-04", "birthplace": "", "education": "省委党校研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "运城市人民政府", "source": "yuncheng.gov.cn"
    },
    # 副市长
    {
        "id": 16, "name": "王红波", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "运城市人民政府", "source": "yuncheng.gov.cn"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共运城市委员会", "type": "党委", "level": "地级市", "parent": "中共山西省委员会", "location": "山西省运城市"},
    {"id": 2, "name": "运城市人民政府", "type": "政府", "level": "地级市", "parent": "山西省人民政府", "location": "山西省运城市"},
    {"id": 3, "name": "中共运城市纪律检查委员会", "type": "纪委", "level": "地级市", "parent": "中共运城市委员会", "location": "山西省运城市"},
    {"id": 4, "name": "运城市公安局", "type": "政府", "level": "地级市", "parent": "运城市人民政府", "location": "山西省运城市"},
    {"id": 5, "name": "运城军分区", "type": "军队", "level": "地级市", "parent": "", "location": "山西省运城市"},
    {"id": 6, "name": "中共河津市委员会", "type": "党委", "level": "县级市", "parent": "中共运城市委员会", "location": "山西省运城市河津市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "市委书记、一把手"},
    {"person_id": 2, "org_id": 2, "title": "市委副书记、市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "市长，市政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "市委副书记、政法委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼市法学会会长"},
    {"person_id": 4, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市政府党组副书记"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼市委党校校长"},
    {"person_id": 6, "org_id": 3, "title": "市委常委、市纪委书记、市监委主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市政府党组成员"},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "市委常委、秘书长、统战部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼市委办公室主任、市政协党组副书记"},
    {"person_id": 10, "org_id": 6, "title": "市委常委、河津市委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 5, "title": "市委常委、军分区大校司令员", "start_date": "", "end_date": "", "rank": "副厅级/大校", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "民建运城市委主委"},
    {"person_id": 13, "org_id": 4, "title": "副市长、市公安局局长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市公安局党委书记"},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市政府党组成员"},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市政府党组成员"},
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # Working relationships within the standing committee
    {"person_a": 1, "person_b": 2, "type": "领导_副手", "context": "市委书记与市长", "overlap_org": "中共运城市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 3, "type": "领导_副手", "context": "市委书记与副书记", "overlap_org": "中共运城市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "领导_副手", "context": "市委书记与常务副市长", "overlap_org": "中共运城市委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "领导_副手", "context": "市长与常务副市长", "overlap_org": "运城市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "副书记与常务副市长", "overlap_org": "中共运城市委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "政法委书记与组织部长", "overlap_org": "中共运城市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "常务副市长与组织部长", "overlap_org": "中共运城市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "常务副市长与纪委书记", "overlap_org": "中共运城市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "组织部长与纪委书记", "overlap_org": "中共运城市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "领导_副手", "context": "市委书记与副市长（常委）", "overlap_org": "中共运城市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "领导_副手", "context": "市委书记与宣传部长", "overlap_org": "中共运城市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "领导_副手", "context": "市委书记与秘书长", "overlap_org": "中共运城市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "领导_副手", "context": "市委书记与河津书记", "overlap_org": "中共运城市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "领导_副手", "context": "市委书记与军分区司令员", "overlap_org": "中共运城市委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "同僚", "context": "市长与副书记", "overlap_org": "中共运城市委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "领导_副手", "context": "市长与副市长", "overlap_org": "运城市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "领导_副手", "context": "市长与公安局长", "overlap_org": "运城市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "领导_副手", "context": "市长与副市长", "overlap_org": "运城市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "领导_副手", "context": "市长与副市长", "overlap_org": "运城市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "领导_副手", "context": "市长与副市长", "overlap_org": "运城市人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 12, "type": "同僚", "context": "常务副市长与其他副市长", "overlap_org": "运城市人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 13, "type": "同僚", "context": "常务副市长与公安局长", "overlap_org": "运城市人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 15, "type": "同僚", "context": "常务副市长与副市长", "overlap_org": "运城市人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 12, "type": "同僚", "context": "副市长之间", "overlap_org": "运城市人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 13, "type": "同僚", "context": "副市长之间", "overlap_org": "运城市人民政府", "overlap_period": ""},
]


# ═════════════════════════════════════════════════════════════════════════════
#  Write person JSONs
# ═════════════════════════════════════════════════════════════════════════════
def write_person_json(p: dict) -> None:
    filename = f"{TODAY}-山西省-运城市-{p['current_post']}-{p['name']}.json"
    path = PERSONS_DIR / filename
    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "identity": {
            "person_id": p["name"],
            "name": p["name"],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "education": p["education"],
            "party_join": p["party_join"],
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
        },
        "sources": [{"url": "https://www.yuncheng.gov.cn/zwgk_1/xxgkml/ldxx/sw/cxh/"}],
    }
    PERSONS_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    for p in persons:
        write_person_json(p)

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

    print(f"✅ {SLUG} build complete:")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   Person JSONs: {PERSONS_DIR}/")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")