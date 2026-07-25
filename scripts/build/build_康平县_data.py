#!/usr/bin/env python3
"""Build 康平县 (Kangping County, Shenyang, Liaoning) personnel network database and graph."""

import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build

SLUG = "康平县"
TASK_ID = "liaoning_康平县"

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "王立勋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中国共产党康平县委员会",
        "source": "https://www.kangping.gov.cn/jrkp/jryw/202607/t20260724_5061980.html",
    },
    {
        "id": 2,
        "name": "齐鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "康平县人民政府",
        "source": "https://www.kangping.gov.cn/zwgk/fdzdgknr/jgjj/ldcygzfg/xz/202305/t20230526_4470543.html",
    },
    {
        "id": 3,
        "name": "邓国强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年4月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "康平县人民政府",
        "source": "https://www.kangping.gov.cn/zwgk/fdzdgknr/jgjj/ldcygzfg/fxz/202208/t20220808_3858090.html",
    },
    {
        "id": 4,
        "name": "陈巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年5月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "康平县人民政府",
        "source": "https://www.kangping.gov.cn/zwgk/fdzdgknr/jgjj/ldcygzfg/fxz/202211/t20221123_4336144.html",
    },
    {
        "id": 5,
        "name": "朱连顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年3月",
        "birthplace": "",
        "education": "法学学士",
        "party_join": "无党派人士",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "康平县人民政府",
        "source": "https://www.kangping.gov.cn/zwgk/fdzdgknr/jgjj/ldcygzfg/fxz/202208/t20220808_3854749.html",
    },
    {
        "id": 6,
        "name": "肖壮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年7月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "康平县公安局",
        "source": "https://www.kangping.gov.cn/zwgk/fdzdgknr/jgjj/ldcygzfg/fxz/202208/t20220808_3856401.html",
    },
    {
        "id": 7,
        "name": "吕明欣",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年5月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "康平县人民政府",
        "source": "https://www.kangping.gov.cn/zwgk/fdzdgknr/jgjj/ldcygzfg/fxz/202502/t20250206_4805996.html",
    },
    {
        "id": 8,
        "name": "王大为",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "康平县人民代表大会常务委员会",
        "source": "https://www.kangping.gov.cn/jrkp/jryw/202607/t20260724_5061980.html",
    },
    {
        "id": 9,
        "name": "轩维铁",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议康平县委员会",
        "source": "https://www.kangping.gov.cn/jrkp/jryw/202607/t20260724_5061980.html",
    },
    {
        "id": 10,
        "name": "田利国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、县政府办公室主任",
        "current_org": "康平县人民政府办公室",
        "source": "https://www.kangping.gov.cn/zwgk/fdzdgknr/jgjj/gbmld/202208/t20220824_4179534.html",
    },
    {
        "id": 11,
        "name": "朱少华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府办公室副主任",
        "current_org": "康平县人民政府办公室",
        "source": "https://www.kangping.gov.cn/zwgk/fdzdgknr/jgjj/gbmld/202208/t20220824_4179534.html",
    },
    {
        "id": 12,
        "name": "史洪蕊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府办公室副主任",
        "current_org": "康平县人民政府办公室",
        "source": "https://www.kangping.gov.cn/zwgk/fdzdgknr/jgjj/gbmld/202208/t20220824_4179534.html",
    },
    {
        "id": 13,
        "name": "高晨阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府办公室副主任",
        "current_org": "康平县人民政府办公室",
        "source": "https://www.kangping.gov.cn/zwgk/fdzdgknr/jgjj/gbmld/202208/t20220824_4179534.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {"id": 0, "name": "中国共产党康平县委员会", "type": "党委", "level": "县处级", "parent": "中国共产党沈阳市委员会", "location": "辽宁省沈阳市康平县"},
    {"id": 1, "name": "康平县人民政府", "type": "政府", "level": "县处级", "parent": "沈阳市人民政府", "location": "辽宁省沈阳市康平县"},
    {"id": 2, "name": "康平县公安局", "type": "政府", "level": "乡科级", "parent": "康平县人民政府", "location": "辽宁省沈阳市康平县"},
    {"id": 3, "name": "康平县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "辽宁省沈阳市康平县"},
    {"id": 4, "name": "中国人民政治协商会议康平县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "辽宁省沈阳市康平县"},
    {"id": 5, "name": "康平县人民政府办公室", "type": "政府", "level": "乡科级", "parent": "康平县人民政府", "location": "辽宁省沈阳市康平县"},
    {"id": 6, "name": "辽宁康平经济开发区管理委员会", "type": "开发区", "level": "", "parent": "康平县人民政府", "location": "辽宁省沈阳市康平县"},
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 0, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "截至2026年7月在任"},
    {"person_id": 2, "org_id": 0, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼任政法委书记"},
    {"person_id": 2, "org_id": 1, "title": "县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "县政府党组书记"},
    {"person_id": 2, "org_id": 6, "title": "管委会主任（兼）", "start_date": "", "end_date": "present", "rank": "", "note": "辽宁康平经济开发区党工委副书记、管委会主任"},
    {"person_id": 3, "org_id": 0, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "县政府党组副书记，负责县政府常务工作"},
    {"person_id": 4, "org_id": 0, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "县政府党组成员"},
    {"person_id": 5, "org_id": 1, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "无党派人士"},
    {"person_id": 6, "org_id": 1, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "县政府党组成员"},
    {"person_id": 6, "org_id": 2, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "县公安局党组书记、督察长"},
    {"person_id": 7, "org_id": 1, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "县政府党组成员"},
    {"person_id": 8, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 9, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 10, "org_id": 5, "title": "县政府办公室主任", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "县政府党组成员、县政府办公室党组书记"},
    {"person_id": 11, "org_id": 5, "title": "县政府办公室副主任", "start_date": "", "end_date": "present", "rank": "乡科级副职", "note": "协调陈巍、朱连顺、吕明欣副县长工作"},
    {"person_id": 12, "org_id": 5, "title": "县政府办公室副主任", "start_date": "", "end_date": "present", "rank": "乡科级副职", "note": "协调邓国强、肖壮副县长工作"},
    {"person_id": 13, "org_id": 5, "title": "县政府办公室副主任", "start_date": "", "end_date": "present", "rank": "乡科级副职", "note": "负责文字综合、政研信息"},
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    # 王立勋 - 齐鑫：党政一把手共事
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与县长党政搭档", "overlap_org": "康平县", "overlap_period": "2026年"},
    # 齐鑫 - 邓国强：县长与常务副县长
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与常务副县长工作关系", "overlap_org": "康平县人民政府", "overlap_period": "2026年"},
    # 邓国强 - 陈巍：同为县委常委、副县长
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同为县委常委、副县长", "overlap_org": "康平县委常委班子", "overlap_period": "2026年"},
    # 王立勋 - 王大为：党委与人大
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记与人大常委会主任", "overlap_org": "康平县", "overlap_period": "2026年"},
    # 王立勋 - 轩维铁：党委与政协
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记与政协主席", "overlap_org": "康平县", "overlap_period": "2026年"},
    # 齐鑫 - 肖壮：县长与公安局长
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县长与分管公安副县长", "overlap_org": "康平县人民政府", "overlap_period": "2026年"},
    # 齐鑫 - 吕明欣：县长与副县长
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县长与分管副县长", "overlap_org": "康平县人民政府", "overlap_period": "2026年"},
    # 齐鑫 - 朱连顺：县长与副县长
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县长与副县长", "overlap_org": "康平县人民政府", "overlap_period": "2026年"},
    # 田利国 - 高晨阳：县政府办公室上下级
    {"person_a": 10, "person_b": 13, "type": "overlap", "context": "县政府办公室主任与副主任", "overlap_org": "康平县人民政府办公室", "overlap_period": "2026年"},
    # 田利国 - 朱少华：县政府办公室上下级
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "县政府办公室主任与副主任", "overlap_org": "康平县人民政府办公室", "overlap_period": "2026年"},
    # 田利国 - 史洪蕊：县政府办公室上下级
    {"person_a": 10, "person_b": 12, "type": "overlap", "context": "县政府办公室主任与副主任", "overlap_org": "康平县人民政府办公室", "overlap_period": "2026年"},
]

if __name__ == "__main__":
    import sys
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
