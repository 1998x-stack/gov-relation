#!/usr/bin/env python3
"""鞍山市（辽宁省·地级市）领导班子工作关系网络 - 数据构建脚本"""

import sqlite3
import sys
from pathlib import Path

# Allow running from repo root, scripts/build, or staging dir
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve()
while not (REPO_ROOT / "gov_relation").is_dir() and REPO_ROOT != REPO_ROOT.parent:
    REPO_ROOT = REPO_ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

AS_OF = "2026-08-03"
SLUG = "鞍山市"

# ── Data ────────────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "吴开华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共鞍山市委",
        "source": "http://www.anshan.gov.cn/html/ASSZF/202608/0178572354367994.html",
        "notes": "2026-08-01主持市委常委会并发表讲话；主持市委全面工作。此为职务的一手官方确认。",
    },
    {
        "id": 2,
        "name": "杨济时",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、市长、市政府党组书记",
        "current_org": "鞍山市人民政府",
        "source": "http://www.anshan.gov.cn/html/ASSZF/202606/0178218416587948.html",
        "notes": "主持市政府全面工作，分管市审计局。官方分工文件（鞍政办发 2026-06-16）。",
    },
    {
        "id": 3,
        "name": "姜乃东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长、市政府党组副书记",
        "current_org": "鞍山市人民政府",
        "source": "http://www.anshan.gov.cn/html/ASSZF/202606/0178218416587948.html",
        "notes": "常务副市长；负责常务、发改、财税、应急、统计等；代管生态环境。",
    },
    {
        "id": 4,
        "name": "丁立",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长、市政府党组成员",
        "current_org": "鞍山市人民政府",
        "source": "http://www.anshan.gov.cn/html/ASSZF/202606/0178218416587948.html",
        "notes": "负责人社、退役军人事务、双拥共建；协管生态环保、招商、外事。",
    },
    {
        "id": 5,
        "name": "王植",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长、市政府党组成员",
        "current_org": "鞍山市人民政府",
        "source": "http://www.anshan.gov.cn/html/ASSZF/202606/0178218416587948.html",
        "notes": "负责科技、工信、金融、国资、营商等；代管自然资源、交通、鞍山机场。联系鞍钢集团。",
    },
    {
        "id": 6,
        "name": "张猛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市政府党组成员",
        "current_org": "鞍山市人民政府",
        "source": "http://www.anshan.gov.cn/html/ASSZF/202606/0178218416587948.html",
        "notes": "负责公安、司法、社会稳定、打击走私；分管市公安局、司法局。",
    },
    {
        "id": 7,
        "name": "柴锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "鞍山市人民政府",
        "source": "http://www.anshan.gov.cn/html/ASSZF/202606/0178218416587948.html",
        "notes": "协助王植负责科技创新工作，协管市科技局。",
    },
    {
        "id": 8,
        "name": "朱长悦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "鞍山市人民政府",
        "source": "http://www.anshan.gov.cn/html/ASSZF/202606/0178218416587948.html",
        "notes": "负责卫生健康、药品安全、医疗保障；分管市卫生健康委、市场监管（药监）、医保局。",
    },
    {
        "id": 9,
        "name": "杜伶",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市政府党组成员",
        "current_org": "鞍山市人民政府",
        "source": "http://www.anshan.gov.cn/html/ASSZF/202606/0178218416587948.html",
        "notes": "负责教育、民政、市场监管、文旅体；分管鞍山师范学院、职业技术学院等。",
    },
    {
        "id": 10,
        "name": "刘启星",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市政府党组成员",
        "current_org": "鞍山市人民政府",
        "source": "http://www.anshan.gov.cn/html/ASSZF/202606/0178218416587948.html",
        "notes": "负责水利、农业、乡村振兴、商务；代管住建、城管。",
    },
    {
        "id": 11,
        "name": "鲁壮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "秘书长、市政府党组成员",
        "current_org": "鞍山市人民政府",
        "source": "http://www.anshan.gov.cn/html/ASSZF/202606/0178218416587948.html",
        "notes": "协管住建、城市管理；分管市政府驻北京联络处。",
    },
]

organizations = [
    {"id": 1, "name": "中共鞍山市委", "type": "党委", "level": "地级市", "parent": "中共辽宁省委", "location": "辽宁省鞍山市"},
    {"id": 2, "name": "鞍山市人民政府", "type": "政府", "level": "地级市", "parent": "辽宁省人民政府", "location": "辽宁省鞍山市"},
    {"id": 3, "name": "鞍山市公安局", "type": "政府", "level": "地级市部门", "parent": "鞍山市人民政府", "location": "辽宁省鞍山市"},
    {"id": 4, "name": "鞍山市纪委监委", "type": "纪委", "level": "地级市", "parent": "中共辽宁省委", "location": "辽宁省鞍山市"},
    {"id": 5, "name": "鞍山市人大常委会", "type": "人大", "level": "地级市", "parent": "鞍山市", "location": "辽宁省鞍山市"},
    {"id": 6, "name": "政协鞍山市委员会", "type": "政协", "level": "地级市", "parent": "鞍山市", "location": "辽宁省鞍山市"},
    {"id": 7, "name": "鞍钢集团", "type": "央属企业", "level": "央企", "parent": "国务院国资委", "location": "辽宁省鞍山市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "主持市委全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "兼任市长，主持市政府全面工作"},
    {"person_id": 2, "org_id": 2, "title": "市长、市政府党组书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "分管市审计局"},
    {"person_id": 3, "org_id": 2, "title": "常务副市长、市政府党组副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责常务、发改、财税、应急等"},
    {"person_id": 4, "org_id": 2, "title": "副市长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "人社、退役军人、双拥"},
    {"person_id": 5, "org_id": 2, "title": "副市长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "科技、工信、金融、国资、营商"},
    {"person_id": 6, "org_id": 2, "title": "副市长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "公安、司法、社会稳定"},
    {"person_id": 6, "org_id": 3, "title": "分管领导", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "分管市公安局"},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "协助王植负责科技创新"},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "卫生健康、药品、医保"},
    {"person_id": 9, "org_id": 2, "title": "副市长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "教育、民政、文旅体"},
    {"person_id": 10, "org_id": 2, "title": "副市长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "水利、农业、乡村振兴、商务"},
    {"person_id": 11, "org_id": 2, "title": "秘书长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "正处级", "note": "协管住建、城管"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "吴开华（市委书记）与杨济时（市长）为鞍山市党政主官搭档", "overlap_org": "中共鞍山市委", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "姜乃东作为常务副市长协助市长杨济时主持市政府日常工作", "overlap_org": "鞍山市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "丁立作为副市长受市长杨济时领导", "overlap_org": "鞍山市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "王植作为副市长受市长杨济时领导", "overlap_org": "鞍山市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "张猛作为副市长受市长杨济时领导", "overlap_org": "鞍山市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "杜伶作为副市长受市长杨济时领导", "overlap_org": "鞍山市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "刘启星作为副市长受市长杨济时领导", "overlap_org": "鞍山市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "鲁壮作为市政府秘书长在杨济时领导下协调市政府日常工作", "overlap_org": "鞍山市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "柴锋作为副市长协助王植（科技副市长）负责科技创新工作", "overlap_org": "鞍山市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
]

# ── Paths ───────────────────────────────────────────────────────────────

DB_PATH = SCRIPT_DIR / f"{SLUG}_network.db"
GEXF_PATH = SCRIPT_DIR / f"{SLUG}_network.gexf"

# ── Build ───────────────────────────────────────────────────────────────

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
    print(f"\n✅ Build complete: {SLUG}")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")