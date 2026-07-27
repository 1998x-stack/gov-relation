#!/usr/bin/env python3
"""Build the 洛龙区 (Luolong District, 洛阳市, 河南省) personnel network.

Research date: 2026-07-24
Sources: official luolong.gov.cn leadership page and news articles.
Confidence: Leader identities confirmed; career timeline data partial due to web access constraints.
"""

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from pathlib import Path

STAGING_DIR = Path(__file__).resolve().parent

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "韩建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛龙区委书记",
        "current_org": "中共洛龙区委员会",
        "source": "https://www.luolong.gov.cn/ — 新闻报道确认：韩建军以区委书记身份出席2026年4-7月系列会议",
    },
    {
        "id": 2,
        "name": "孙毅辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "洛龙区委副书记、区长",
        "current_org": "洛龙区人民政府",
        "source": "https://www.luolong.gov.cn/zwgk/wgkzl/glgk/ldzc/qzfld/ 官方领导之窗",
    },
    {
        "id": 3,
        "name": "张炜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛龙区委领导",
        "current_org": "中共洛龙区委员会",
        "source": "六届区委常委会第2次会议新闻报道（2026-07-08）",
    },
    {
        "id": 4,
        "name": "张华伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "洛龙区委常委、副区长",
        "current_org": "洛龙区人民政府",
        "source": "https://www.luolong.gov.cn/zwgk/wgkzl/glgk/ldzc/qzfld/ 官方领导之窗",
    },
    {
        "id": 5,
        "name": "赵阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛龙区委领导",
        "current_org": "中共洛龙区委员会",
        "source": "六届区委常委会第2次会议新闻报道（2026-07-08）",
    },
    {
        "id": 6,
        "name": "孙亚平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛龙区委领导",
        "current_org": "中共洛龙区委员会",
        "source": "六届区委常委会第2次会议新闻报道（2026-07-08）",
    },
    {
        "id": 7,
        "name": "赵艳辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛龙区委领导",
        "current_org": "中共洛龙区委员会",
        "source": "六届区委常委会第2次会议新闻报道（2026-07-08）",
    },
    {
        "id": 8,
        "name": "杨益",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛龙区委领导",
        "current_org": "中共洛龙区委员会",
        "source": "六届区委常委会第2次会议新闻报道（2026-07-08）",
    },
    {
        "id": 9,
        "name": "张会博",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛龙区委领导",
        "current_org": "中共洛龙区委员会",
        "source": "六届区委常委会第2次会议新闻报道（2026-07-08）",
    },
    {
        "id": 10,
        "name": "王国辉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年6月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "洛龙区委常委、宣传部部长、副区长",
        "current_org": "中共洛龙区委员会",
        "source": "https://www.luolong.gov.cn/zwgk/wgkzl/glgk/ldzc/qzfld/ 官方领导之窗",
    },
    {
        "id": 11,
        "name": "马竞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "洛龙区副区长",
        "current_org": "洛龙区人民政府",
        "source": "https://www.luolong.gov.cn/zwgk/wgkzl/glgk/ldzc/qzfld/ 官方领导之窗",
    },
    {
        "id": 12,
        "name": "黄鹏勃",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年7月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "洛龙区副区长、洛龙公安分局局长",
        "current_org": "洛龙区人民政府",
        "source": "https://www.luolong.gov.cn/zwgk/wgkzl/glgk/ldzc/qzfld/ 官方领导之窗",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共洛龙区委员会", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "洛阳市洛龙区"},
    {"id": 2, "name": "洛龙区人民政府", "type": "政府", "level": "县处级", "parent": "洛阳市人民政府", "location": "洛阳市洛龙区"},
    {"id": 3, "name": "洛龙区人大常委会", "type": "人大", "level": "县处级", "parent": "洛阳市人大常委会", "location": "洛阳市洛龙区"},
    {"id": 4, "name": "洛龙区政协", "type": "政协", "level": "县处级", "parent": "洛阳市政协", "location": "洛阳市洛龙区"},
    {"id": 5, "name": "洛龙区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "洛阳市纪委监委", "location": "洛阳市洛龙区"},
    {"id": 6, "name": "洛龙区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共洛龙区委员会", "location": "洛阳市洛龙区"},
    {"id": 7, "name": "洛龙公安分局", "type": "政府", "level": "乡科级", "parent": "洛阳市公安局", "location": "洛阳市洛龙区"},
    {"id": 8, "name": "洛龙区行政学校", "type": "事业单位", "level": "乡科级", "parent": "洛龙区人民政府", "location": "洛阳市洛龙区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 韩建军
    {"person_id": 1, "org_id": 1, "title": "洛龙区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026年4-7月以区委书记身份公开活动确认"},
    # 孙毅辉
    {"person_id": 2, "org_id": 1, "title": "洛龙区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "洛龙区区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "官方领导之窗确认"},
    # 张华伟
    {"person_id": 4, "org_id": 1, "title": "洛龙区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "洛龙区副区长（常务）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "区政府党组副书记、区行政学校校长"},
    # 王国辉
    {"person_id": 10, "org_id": 1, "title": "洛龙区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 6, "title": "洛龙区委宣传部部长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "洛龙区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 马竞
    {"person_id": 11, "org_id": 2, "title": "洛龙区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "区政府党组成员"},
    # 黄鹏勃
    {"person_id": 12, "org_id": 2, "title": "洛龙区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "区政府党组成员"},
    {"person_id": 12, "org_id": 7, "title": "洛龙公安分局局长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "党委书记"},
    # 其他区委常委/领导（列席区委常委会）
    {"person_id": 3, "org_id": 1, "title": "洛龙区委领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "列席六届区委常委会第2次会议"},
    {"person_id": 5, "org_id": 1, "title": "洛龙区委领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "列席六届区委常委会第2次会议"},
    {"person_id": 6, "org_id": 1, "title": "洛龙区委领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "列席六届区委常委会第2次会议"},
    {"person_id": 7, "org_id": 1, "title": "洛龙区委领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "列席六届区委常委会第2次会议"},
    {"person_id": 8, "org_id": 1, "title": "洛龙区委领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "列席六届区委常委会第2次会议"},
    {"person_id": 9, "org_id": 1, "title": "洛龙区委领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "列席六届区委常委会第2次会议"},
]

# ── Relationships ────────────────────────────────────────────────────────────
# All relationships are confirmed by the leadership page or meeting attendance records.

relationships = [
    # 韩建军 — 孙毅辉: 书记与区长的搭档关系
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长搭档", "overlap_org": "中共洛龙区委员会 / 洛龙区人民政府", "overlap_period": "当前"},
    # 韩建军 — 张华伟: 书记与常委兼副区长
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与区委常委、副区长", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    # 韩建军 — 王国辉: 书记与宣传部长
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "区委书记与区委常委、宣传部部长", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    # 孙毅辉 — 张华伟: 区长与常务副区长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与常务副区长", "overlap_org": "洛龙区人民政府", "overlap_period": "当前"},
    # 孙毅辉 — 马竞: 区长与副区长
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "洛龙区人民政府", "overlap_period": "当前"},
    # 孙毅辉 — 黄鹏勃: 区长与副区长兼公安局长
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "区长与副区长、公安分局局长", "overlap_org": "洛龙区人民政府", "overlap_period": "当前"},
    # 区委常委之间：张华伟 — 王国辉
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "同为区委常委", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    # 列席常委会的区领导（同事关系）
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    {"person_a": 5, "person_b": 8, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    {"person_a": 5, "person_b": 9, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    {"person_a": 6, "person_b": 8, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    {"person_a": 6, "person_b": 9, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    {"person_a": 7, "person_b": 9, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "同为区委领导（列席常委会）", "overlap_org": "中共洛龙区委员会", "overlap_period": "当前"},
]

# ── Run Build ────────────────────────────────────────────────────────────────

SLUG = "洛龙区"
DB_NAME = f"{SLUG}_network.db"
GEXF_NAME = f"{SLUG}_network.gexf"

if __name__ == "__main__":
    db_path = STAGING_DIR / DB_NAME
    gexf_path = STAGING_DIR / GEXF_NAME

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
    print(f"\nDone. Files in {STAGING_DIR}:")
    print(f"  DB:   {db_path}")
    print(f"  GEXF: {gexf_path}")
    print(f"\nSummary: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
