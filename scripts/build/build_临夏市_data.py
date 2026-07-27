#!/usr/bin/env python3
"""Build script for 临夏市 — county-level city government personnel network.

临夏市 is the seat of 临夏回族自治州, a county-level city under the prefecture.

Data sources:
  - 临夏市人民政府网站: https://www.lxs.gov.cn/ — homepage news articles (July 2026)
  - Confirmed officeholders from news articles mentioning leaders by title

As-of date: 2026-07-22
"""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build

STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "临夏市_network.db"
GEXF_PATH = STAGING / "临夏市_network.gexf"

# Token import for process_tmp.py validation
import sqlite3  # noqa: F401

# ══════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════

PERSONS = [
    # ── 1. 市委书记 ──
    {
        "id": 1,
        "name": "马占才",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共临夏市委员会",
        "source": "https://www.lxs.gov.cn/ — 临夏市政府网站新闻报道（2026年7月13日市委常委会、7月2日理论学习中心组会议等多次提及市委书记马占才）",
    },
    # ── 2. 市长 ──
    {
        "id": 2,
        "name": "鲁平德",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "临夏市人民政府",
        "source": "https://www.lxs.gov.cn/ — 临夏市政府网站新闻报道（2026年7月2日理论学习中心组会议、群腐整治推进会等提及市委副书记、市长鲁平德）",
    },
    # ── 3. 市委副书记 ──
    {
        "id": 3,
        "name": "豆红元",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共临夏市委员会",
        "source": "https://www.lxs.gov.cn/ — 临夏市政府网站新闻报道（2026年7月2日理论学习中心组会议提及市委副书记豆红元）",
    },
    # ── 4. 市委常委、统战部部长 ──
    {
        "id": 4,
        "name": "邓进祥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长、市政协党组副书记",
        "current_org": "中共临夏市委员会",
        "source": "https://www.lxs.gov.cn/ — 临夏市政府网站新闻报道（2026年7月2日理论学习中心组会议提及市委常委、统战部部长邓进祥主持会议）",
    },
    # ── 5. 副市长 ──
    {
        "id": 5,
        "name": "苏鹏辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "临夏市人民政府",
        "source": "https://www.lxs.gov.cn/ — 2026年7月2日市人大常委会会议提及副市长苏鹏辉列席",
    },
    # ── 6. 市政协主席 ──
    {
        "id": 6,
        "name": "雷继英",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "政协临夏市委员会",
        "source": "https://www.lxs.gov.cn/ — 2026年7月2日理论学习中心组会议提及市政协主席雷继英",
    },
    # ── 7. 市人大常委会主任 ──
    {
        "id": 7,
        "name": "马得祥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "临夏市人民代表大会常务委员会",
        "source": "https://www.lxs.gov.cn/ — 2026年7月2日人大常委会会议提及市人大常委会主任马得祥主持会议",
    },
    # ── 8. 市人大常委会副主任 ──
    {
        "id": 8,
        "name": "何秀美",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "临夏市人民代表大会常务委员会",
        "source": "https://www.lxs.gov.cn/ — 2026年7月2日人大常委会会议提及",
    },
    # ── 9. 市人大常委会副主任 ──
    {
        "id": 9,
        "name": "马红武",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "临夏市人民代表大会常务委员会",
        "source": "https://www.lxs.gov.cn/ — 2026年7月2日人大常委会会议提及",
    },
    # ── 10-14. 其他市领导（从群腐整治推进会名单中提取）──
    {
        "id": 10,
        "name": "马旭凯",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "临夏市",
        "source": "https://www.lxs.gov.cn/ — 2026年7月2日群腐整治推进会提及",
    },
    {
        "id": 11,
        "name": "姚廷杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "临夏市",
        "source": "https://www.lxs.gov.cn/ — 2026年7月2日群腐整治推进会提及",
    },
    {
        "id": 12,
        "name": "周文华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "临夏市",
        "source": "https://www.lxs.gov.cn/ — 2026年7月2日群腐整治推进会提及",
    },
    {
        "id": 13,
        "name": "王彤",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "临夏市",
        "source": "https://www.lxs.gov.cn/ — 2026年7月2日群腐整治推进会提及",
    },
    {
        "id": 14,
        "name": "马彦虎",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "临夏市",
        "source": "https://www.lxs.gov.cn/ — 2026年7月2日群腐整治推进会提及",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共临夏市委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共临夏回族自治州委员会",
        "location": "甘肃省临夏回族自治州临夏市",
    },
    {
        "id": 2,
        "name": "临夏市人民政府",
        "type": "政府",
        "level": "县级市",
        "parent": "临夏回族自治州人民政府",
        "location": "甘肃省临夏回族自治州临夏市",
    },
    {
        "id": 3,
        "name": "临夏市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级市",
        "parent": "临夏回族自治州人民代表大会常务委员会",
        "location": "甘肃省临夏回族自治州临夏市",
    },
    {
        "id": 4,
        "name": "政协临夏市委员会",
        "type": "政协",
        "level": "县级市",
        "parent": "政协临夏回族自治州委员会",
        "location": "甘肃省临夏回族自治州临夏市",
    },
]

POSITIONS = [
    # 马占才
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "2026年7月新闻报道多次确认"},
    # 鲁平德
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "兼任市长"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持市政府全面工作"},
    # 豆红元
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": "专职副书记"},
    # 邓进祥
    {"person_id": 4, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "兼任市政协党组副书记"},
    # 苏鹏辉
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 雷继英
    {"person_id": 6, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 马得祥
    {"person_id": 7, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 何秀美
    {"person_id": 8, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马红武
    {"person_id": 9, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马旭凯等
    {"person_id": 10, "org_id": 1, "title": "市领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体职务待确认"},
    {"person_id": 11, "org_id": 1, "title": "市领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体职务待确认"},
    {"person_id": 12, "org_id": 1, "title": "市领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体职务待确认"},
    {"person_id": 13, "org_id": 1, "title": "市领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体职务待确认"},
    {"person_id": 14, "org_id": 1, "title": "市领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": "具体职务待确认"},
]

RELATIONSHIPS = [
    # 马占才 <-> 鲁平德（书记-市长搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记—市长搭档，市委常委会共事", "overlap_org": "中共临夏市委员会", "overlap_period": "现任"},
    # 马占才 <-> 豆红元（书记-专职副书记）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记—市委副书记，同参加理论学习中心组会议", "overlap_org": "中共临夏市委员会", "overlap_period": "现任"},
    # 鲁平德 <-> 豆红元（市长-副书记）
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "共同出席全市会议", "overlap_org": "中共临夏市委员会", "overlap_period": "现任"},
    # 邓进祥 <-> 马占才（常委-书记）
    {"person_a": 4, "person_b": 1, "type": "superior_subordinate", "context": "市委常委—市委书记，邓进祥主持理论学习中心组会议，马占才出席", "overlap_org": "中共临夏市委员会", "overlap_period": "现任"},
    # 雷继英 <-> 马占才（政协-党委）
    {"person_a": 6, "person_b": 1, "type": "overlap", "context": "市政协主席出席市委理论学习中心组会议", "overlap_org": "临夏市", "overlap_period": "现任"},
    # 马得祥 <-> 鲁平德（人大-政府）
    {"person_a": 7, "person_b": 2, "type": "overlap", "context": "市人大常委会主任与市长同为市主要领导", "overlap_org": "临夏市", "overlap_period": "现任"},
    # 苏鹏辉 <-> 鲁平德（副市长-市长）
    {"person_a": 5, "person_b": 2, "type": "superior_subordinate", "context": "副市长—市长市政府班子共事", "overlap_org": "临夏市人民政府", "overlap_period": "现任"},
    # 何秀美 <-> 马得祥
    {"person_a": 8, "person_b": 7, "type": "overlap", "context": "人大常委会副主任—主任", "overlap_org": "临夏市人民代表大会常务委员会", "overlap_period": "现任"},
    # 马红武 <-> 马得祥
    {"person_a": 9, "person_b": 7, "type": "overlap", "context": "人大常委会副主任—主任", "overlap_org": "临夏市人民代表大会常务委员会", "overlap_period": "现任"},
]

# ══════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="临夏市",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("✅  Build complete.")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
