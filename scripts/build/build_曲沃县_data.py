#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 曲沃县 (Quwo County, Linfen, Shanxi) leadership network.

Task: shanxi_曲沃县
Targets: 县委书记 吴滨, 县长 孙惠生
Province: 山西省
Parent City: 临汾市
Level: 县
Generated: 2026-08-03
As-of: 2026-07-31 (sourced from quwo.gov.cn party congress coverage)
"""

from pathlib import Path
import sys

_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
import sqlite3  # noqa: F401 — used implicitly by run_build

SLUG = "曲沃县"

DB_PATH = Path(__file__).parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).parent / f"{SLUG}_network.gexf"

# ── PERSONS ────────────────────────────────────────────────────────────
persons = [
    # ── Top Leaders ──
    {
        "id": 1,
        "name": "吴滨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县委书记",
        "current_org": "中共曲沃县委员会",
        "source": "http://www.quwo.gov.cn/contents/6557/7404.html (16th Party Congress first plenum, 2026-07-30)",
    },
    {
        "id": 2,
        "name": "孙惠生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-12",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县委副书记、县长",
        "current_org": "曲沃县人民政府",
        "source": "http://www.quwo.gov.cn/contents/6657/1077.html (县长官方页面)",
    },
    # ── Party Committee Standing Committee ──
    {
        "id": 3,
        "name": "张军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县委副书记",
        "current_org": "中共曲沃县委员会",
        "source": "http://www.quwo.gov.cn/contents/6557/7404.html (16届县委第一次全会)",
    },
    {
        "id": 4,
        "name": "李峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县委常委",
        "current_org": "中共曲沃县委员会",
        "source": "http://www.quwo.gov.cn/contents/6557/7404.html (16届县委第一次全会)",
    },
    {
        "id": 5,
        "name": "张凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县委常委",
        "current_org": "中共曲沃县委员会",
        "source": "http://www.quwo.gov.cn/contents/6557/7404.html (16届县委第一次全会)",
    },
    {
        "id": 6,
        "name": "杨洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-07",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县委常委、县政府党组副书记、副县长",
        "current_org": "曲沃县人民政府",
        "source": "http://www.quwo.gov.cn/contents/6658/1078.html (副县长官方页面)",
    },
    {
        "id": 7,
        "name": "王婧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县委常委",
        "current_org": "中共曲沃县委员会",
        "source": "http://www.quwo.gov.cn/contents/6557/7404.html (16届县委第一次全会)",
    },
    {
        "id": 8,
        "name": "迟红霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976-03",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县委常委、副县长",
        "current_org": "曲沃县人民政府",
        "source": "http://www.quwo.gov.cn/contents/6658/1082.html (副县长官方页面)",
    },
    {
        "id": 9,
        "name": "邓明明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县委常委",
        "current_org": "中共曲沃县委员会",
        "source": "http://www.quwo.gov.cn/contents/6557/7404.html (16届县委第一次全会)",
    },
    {
        "id": 10,
        "name": "梁爽",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县委常委",
        "current_org": "中共曲沃县委员会",
        "source": "http://www.quwo.gov.cn/contents/6557/7404.html (16届县委第一次全会)",
    },
    {
        "id": 11,
        "name": "叶晓晨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县委常委",
        "current_org": "中共曲沃县委员会",
        "source": "http://www.quwo.gov.cn/contents/6557/7404.html (16届县委第一次全会)",
    },
    # ── Other Government Deputies ──
    {
        "id": 12,
        "name": "陈卓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-10",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县政府副县长",
        "current_org": "曲沃县人民政府",
        "source": "http://www.quwo.gov.cn/contents/6658/1080.html (副县长官方页面)",
    },
    {
        "id": 13,
        "name": "樊奇选",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-07",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县政府党组成员、副县长",
        "current_org": "曲沃县人民政府",
        "source": "http://www.quwo.gov.cn/contents/6658/1081.html (副县长官方页面)",
    },
    {
        "id": 14,
        "name": "闫探宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-08",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县政府党组成员、副县长、县公安局党委书记、局长",
        "current_org": "曲沃县公安局",
        "source": "http://www.quwo.gov.cn/contents/6658/1079.html (副县长官方页面)",
    },
    # ── Other Key County Leaders ──
    {
        "id": 15,
        "name": "武文军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县人大常委会党组书记",
        "current_org": "曲沃县人民代表大会常务委员会",
        "source": "http://www.quwo.gov.cn/contents/6557/7415.html (人大常委会第66次主任会议, 2026-07-31)",
    },
    {
        "id": 16,
        "name": "秦康杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县领导(主席团成员)",
        "current_org": "中共曲沃县委员会",
        "source": "http://www.quwo.gov.cn/contents/6557/7405.html (16th Party Congress closing ceremony)",
    },
    {
        "id": 17,
        "name": "裴猛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲沃县领导",
        "current_org": "中共曲沃县委员会",
        "source": "http://www.quwo.gov.cn/contents/6557/7417.html (八一慰问活动, 2026-07-31)",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共曲沃县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共临汾市委员会",
        "location": "山西省临汾市曲沃县",
    },
    {
        "id": 2,
        "name": "曲沃县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "临汾市人民政府",
        "location": "山西省临汾市曲沃县",
    },
    {
        "id": 3,
        "name": "中共曲沃县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共曲沃县委员会",
        "location": "山西省临汾市曲沃县",
    },
    {
        "id": 4,
        "name": "曲沃县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "曲沃县",
        "location": "山西省临汾市曲沃县",
    },
    {
        "id": 5,
        "name": "曲沃县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "曲沃县人民政府",
        "location": "山西省临汾市曲沃县",
    },
    {
        "id": 6,
        "name": "曲沃县人民武装部",
        "type": "政府",
        "level": "县级",
        "parent": "曲沃县",
        "location": "山西省临汾市曲沃县",
    },
]

# ── POSITIONS ──────────────────────────────────────────────────────────
positions = [
    # Party Secretary
    {"person_id": 1, "org_id": 1, "title": "曲沃县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "re-elected as Party Secretary at 16th Party Congress first plenum, 2026-07-30"},
    # County Mayor
    {"person_id": 2, "org_id": 1, "title": "曲沃县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "re-elected as deputy secretary, 2026-07-30"},
    {"person_id": 2, "org_id": 2, "title": "曲沃县人民政府县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "official leadership page, confirmed by multiple news articles"},
    # Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "曲沃县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "elected at 16th Party Congress, 2026-07-30"},
    # Standing Committee Members
    {"person_id": 4, "org_id": 1, "title": "曲沃县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "elected at 16th Party Congress, 2026-07-30"},
    {"person_id": 5, "org_id": 1, "title": "曲沃县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "elected at 16th Party Congress, 2026-07-30"},
    {"person_id": 6, "org_id": 1, "title": "曲沃县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "elected at 16th Party Congress, 2026-07-30"},
    {"person_id": 6, "org_id": 2, "title": "曲沃县委常委、县政府党组副书记、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official leadership page"},
    {"person_id": 7, "org_id": 1, "title": "曲沃县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "elected at 16th Party Congress, 2026-07-30"},
    {"person_id": 8, "org_id": 1, "title": "曲沃县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "elected at 16th Party Congress, 2026-07-30"},
    {"person_id": 8, "org_id": 2, "title": "曲沃县委常委、县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official leadership page"},
    {"person_id": 9, "org_id": 1, "title": "曲沃县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "elected at 16th Party Congress, 2026-07-30"},
    {"person_id": 10, "org_id": 1, "title": "曲沃县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "elected at 16th Party Congress, 2026-07-30"},
    {"person_id": 11, "org_id": 1, "title": "曲沃县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "elected at 16th Party Congress, 2026-07-30"},
    # Government Deputies
    {"person_id": 12, "org_id": 2, "title": "曲沃县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "无党派民主人士; official leadership page"},
    {"person_id": 13, "org_id": 2, "title": "曲沃县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official leadership page"},
    {"person_id": 14, "org_id": 2, "title": "曲沃县政府党组成员、副县长、县公安局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official leadership page"},
    {"person_id": 14, "org_id": 5, "title": "县公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "official leadership page"},
    # Other leaders
    {"person_id": 15, "org_id": 4, "title": "曲沃县人大常委会党组书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "mentioned in news articles, 2026-07-31"},
    {"person_id": 16, "org_id": 1, "title": "曲沃县领导(主席团成员)", "start_date": "", "end_date": "present", "rank": "", "note": "seated in front row at Party Congress"},
    {"person_id": 17, "org_id": 1, "title": "曲沃县领导", "start_date": "", "end_date": "present", "rank": "", "note": "participated in Army Day event, 2026-07-31"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────
relationships = [
    # 吴滨 <-> 孙惠生: party secretary and mayor
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县长搭档，同时当选第十六届县委常委", "overlap_org": "中共曲沃县委员会", "overlap_period": "2026-"},
    # 吴滨 <-> 张军: party secretary and deputy secretary
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记—县委副书记班子", "overlap_org": "中共曲沃县委员会", "overlap_period": "2026-"},
    # 孙惠生 <-> 张军: two deputy secretaries
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与专职副书记同届班子成员", "overlap_org": "中共曲沃县委员会", "overlap_period": "2026-"},
    # 吴滨 <-> 杨洋: secretary and standing committee member
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记—常委班子", "overlap_org": "中共曲沃县委员会", "overlap_period": "2026-"},
    # 吴滨 <-> 迟红霞: secretary and standing committee member
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记—常委班子", "overlap_org": "中共曲沃县委员会", "overlap_period": "2026-"},
    # 孙惠生 <-> 杨洋: mayor and executive deputy mayor
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县长—常务副县长工作搭档", "overlap_org": "曲沃县人民政府", "overlap_period": "2026-"},
    # 孙惠生 <-> 迟红霞: mayor and deputy mayor
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县长—副县长工作搭档", "overlap_org": "曲沃县人民政府", "overlap_period": "2026-"},
    # All standing committee members overlap at county party committee
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "同一届县委常委会", "overlap_org": "中共曲沃县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "同一届县委常委会", "overlap_org": "中共曲沃县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "同一届县委常委会", "overlap_org": "中共曲沃县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "同一届县委常委会", "overlap_org": "中共曲沃县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "同一届县委常委会", "overlap_org": "中共曲沃县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "同一届县委常委会", "overlap_org": "中共曲沃县委员会", "overlap_period": "2026-"},
    # 孙惠生 with other government deputies
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县长—副县长", "overlap_org": "曲沃县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县长—副县长", "overlap_org": "曲沃县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县长—公安局长", "overlap_org": "曲沃县人民政府", "overlap_period": "2026-"},
    # 吴滨 <-> 武文军: party secretary and congress chair
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "县委书记—人大党组书记", "overlap_org": "曲沃县", "overlap_period": "2026-"},
    # 吴滨 <-> 秦康杰: party committee
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "县委领导", "overlap_org": "曲沃县", "overlap_period": "2026-"},
]

# ── BUILD ──────────────────────────────────────────────────────────────
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
    print(f"✅ 曲沃县 network built: {DB_PATH}, {GEXF_PATH}")