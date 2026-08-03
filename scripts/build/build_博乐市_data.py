#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 博乐市 (Bole City) leadership network.

博乐市 is a county-level city under 博尔塔拉蒙古自治州 (Bortala Mongol
Autonomous Prefecture), Xinjiang Uyghur Autonomous Region.

Targets: 市委书记 (Party Secretary) & 市长 (Mayor)
"""
import os
import sys
import sqlite3
from pathlib import Path

_script_path = Path(__file__).resolve()
REPO_ROOT = _script_path.parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

STAGING_DIR = REPO_ROOT / "data/tmp/xinjiang_博乐市"
DB_PATH = STAGING_DIR / "博乐市_network.db"
GEXF_PATH = STAGING_DIR / "博乐市_network.gexf"

# ── DATA ──

persons = [
    # ── Top Leaders ──
    {
        "id": 1, "name": "刘强",
        "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "博乐市委书记",
        "current_org": "中共博乐市委员会",
        "source": "https://www.xjbl.gov.cn/; zh.wikipedia.org",
    },
    {
        "id": 2, "name": "彭次克",
        "gender": "男", "ethnicity": "蒙古族",
        "birth": "1984-08", "birthplace": "",
        "education": "西北民族大学本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "博乐市委副书记、市政府党组书记、代理市长",
        "current_org": "博乐市人民政府",
        "source": "https://www.xjbl.gov.cn/xjbl/c126850/202607/af533812098844b191adcae94731fd89.shtml",
    },
    # ── Government Leadership ──
    {
        "id": 3, "name": "邱静波",
        "gender": "男", "ethnicity": "汉族",
        "birth": "1984-09", "birthplace": "",
        "education": "青岛农业大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "博乐市委常委、常务副市长",
        "current_org": "博乐市人民政府",
        "source": "https://www.xjbl.gov.cn/xjbl/c126851/202607/aa8b8fbbbddc4306a1e3eb0d4dc2b9ac.shtml",
    },
    {
        "id": 4, "name": "路漫游",
        "gender": "男", "ethnicity": "汉族",
        "birth": "1981-06", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "博乐市委常委、副市长（援疆）",
        "current_org": "博乐市人民政府",
        "source": "https://www.xjbl.gov.cn/xjbl/c126852/202508/e0ca16d03cf842559a07f5a299d79639.shtml",
    },
    {
        "id": 5, "name": "李岚",
        "gender": "女", "ethnicity": "汉族",
        "birth": "1988-04", "birthplace": "河南漯河",
        "education": "西北政法大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "博乐市委常委、副市长",
        "current_org": "博乐市人民政府",
        "source": "https://www.xjbl.gov.cn/xjbl/c126852/202607/c4a8de6210a74ae09f601d8dcd52e0d1.shtml",
    },
    {
        "id": 6, "name": "陈福领",
        "gender": "男", "ethnicity": "汉族",
        "birth": "1982-06", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "博乐市副市长（人选）",
        "current_org": "博乐市人民政府",
        "source": "https://www.xjbl.gov.cn/xjbl/c126852/202607/9f104ee318b64340890765ec59f2c5e0.shtml",
    },
    {
        "id": 7, "name": "巴哈尔古丽·阿依坦",
        "gender": "女", "ethnicity": "哈萨克族",
        "birth": "1977-05", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "博乐市副市长",
        "current_org": "博乐市人民政府",
        "source": "https://www.xjbl.gov.cn/xjbl/c126852/202607/bdbd4221f6b42158c27c6cadb84f053.shtml",
    },
    {
        "id": 8, "name": "肉孜买买提·努尔买买提",
        "gender": "男", "ethnicity": "维吾尔族",
        "birth": "1988-10", "birthplace": "",
        "education": "北京大学光华管理学院硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "博乐市副市长",
        "current_org": "博乐市人民政府",
        "source": "https://www.xjbl.gov.cn/xjbl/c126852/202607/0794c4b333aa47b69f0a05b9fe835ebb.shtml",
    },
    {
        "id": 9, "name": "张磊",
        "gender": "男", "ethnicity": "汉族",
        "birth": "1984-01", "birthplace": "",
        "education": "新疆农业大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "博乐市副市长",
        "current_org": "博乐市人民政府",
        "source": "https://www.xjbl.gov.cn/xjbl/c126852/202507/650e762adf2c49f8b0a547c2ce6a21ab.shtml",
    },
    {
        "id": 10, "name": "王先全",
        "gender": "男", "ethnicity": "汉族",
        "birth": "1988-12", "birthplace": "博乐",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "博乐市副市长",
        "current_org": "博乐市人民政府",
        "source": "https://www.xjbl.gov.cn/xjbl/c126852/202507/342075c364c40d799c0540ff3ec075d.shtml",
    },
    {
        "id": 11, "name": "吴义东",
        "gender": "男", "ethnicity": "汉族",
        "birth": "1985-11", "birthplace": "",
        "education": "新疆警官高等专科学校",
        "party_join": "中共党员", "work_start": "",
        "current_post": "博乐市副市长、市公安局局长、市委政法委副书记",
        "current_org": "博乐市人民政府",
        "source": "https://www.xjbl.gov.cn/bjbl/c126852/202507/140e02c5efe54cd7a1ed2da196039736.shtml",
    },
    # ── Historical Leaders ──
    {
        "id": 12, "name": "聂壮",
        "gender": "男", "ethnicity": "汉族",
        "birth": "1972-03", "birthplace": "江西丰城",
        "education": "在职大学（新疆经济管理干部学院国际商务专业）",
        "party_join": "1996-06", "work_start": "1992-08",
        "current_post": "新疆维吾尔自治区人民政府副主席、喀什地委书记",
        "current_org": "中共喀什地区委员会",
        "source": "https://baike.baidu.com/item/%E8%81%82%E5%A3%AE",
    },
]

organizations = [
    {"id": 1, "name": "中共博乐市委员会", "type": "党委", "level": "县级",
     "parent": "中共博尔塔拉蒙古自治州委员会", "location": "博乐市"},
    {"id": 2, "name": "博乐市人民政府", "type": "政府", "level": "县级",
     "parent": "博尔塔拉蒙古自治州人民政府", "location": "博乐市"},
    {"id": 3, "name": "博乐市公安局", "type": "政府", "level": "县级",
     "parent": "博乐市人民政府", "location": "博乐市"},
    {"id": 4, "name": "博乐市人大常委会", "type": "人大", "level": "县级",
     "parent": "博尔塔拉蒙古自治州人大常委会", "location": "博乐市"},
    {"id": 5, "name": "博乐市政协", "type": "政协", "level": "县级",
     "parent": "博尔塔拉蒙古自治州政协", "location": "博乐市"},
    {"id": 6, "name": "中共博尔塔拉蒙古自治州委员会", "type": "党委", "level": "地级",
     "parent": "中共新疆维吾尔自治区委员会", "location": "博乐市"},
    {"id": 7, "name": "博尔塔拉蒙古自治州人民政府", "type": "政府", "level": "地级",
     "parent": "新疆维吾尔自治区人民政府", "location": "博乐市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "博乐市委书记",
     "start": "", "end": "present", "rank": "正处级",
     "note": "现任市委书记"},
    {"person_id": 2, "org_id": 1, "title": "博乐市委副书记",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "博乐市代市长、市政府党组书记",
     "start": "", "end": "present", "rank": "正处级",
     "note": "代理市长"},
    {"person_id": 3, "org_id": 1, "title": "博乐市委常委",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "博乐市委常委、常务副市长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "博乐市委常委",
     "start": "", "end": "present", "rank": "副处级", "note": "援疆干部"},
    {"person_id": 4, "org_id": 2, "title": "博乐市委常委、副市长（援疆）",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "博乐市委常委",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "博乐市委常委、副市长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "博乐市副市长（人选）",
     "start": "", "end": "present", "rank": "副处级", "note": "副市长人选"},
    {"person_id": 7, "org_id": 2, "title": "博乐市副市长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "博乐市副市长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "博乐市副市长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "博乐市副市长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "博乐市副市长、市公安局局长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "兼任市委政法委副书记"},
    {"person_id": 11, "org_id": 3, "title": "博乐市公安局局长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "博乐市委书记",
     "start": "2016-08", "end": "2018-06", "rank": "副厅级",
     "note": "时任博尔塔拉蒙古自治州党委常委、博乐市委书记"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "刘强（市委书记）与彭次克（代理市长）为博乐市当前党政一把手",
     "overlap_org": "博乐市", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 12, "person_b": 1, "type": "predecessor_successor",
     "context": "聂壮于2018年6月离任博乐市委书记后继任者为刘强",
     "overlap_org": "中共博乐市委员会", "overlap_period": "2018",
     "strength": "medium", "confidence": "plausible"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "彭次克与邱静波在博乐市政府常务工作中密切配合",
     "overlap_org": "博乐市人民政府", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 2, "type": "superior_subordinate",
     "context": "路漫游作为援疆副市长，在彭次克领导下工作",
     "overlap_org": "博乐市人民政府", "overlap_period": "2026-至今",
     "strength": "medium", "confidence": "confirmed"},
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate",
     "context": "吴义东（副市长、公安局局长）向彭次克汇报公安工作",
     "overlap_org": "博乐市人民政府", "overlap_period": "2026-至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 12, "person_b": 2, "type": "跨地区连接",
     "context": "聂壮曾任博乐市委书记（2016-2018），与现任代理市长彭次克可能通过工作安排产生联系",
     "overlap_org": "博乐市", "overlap_period": "跨时期",
     "strength": "weak", "confidence": "unverified"},
]


if __name__ == "__main__":
    os.makedirs(str(STAGING_DIR), exist_ok=True)
    print(f"Building DB at {DB_PATH}")
    print(f"Building GEXF at {GEXF_PATH}")
    run_build(
        slug="博乐市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
    )
    print(f"DB size: {os.path.getsize(str(DB_PATH))} bytes")
    print(f"GEXF size: {os.path.getsize(str(GEXF_PATH))} bytes")
    print(f"Persons: {len(persons)}, Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}, Relationships: {len(relationships)}")
    print("Done.")