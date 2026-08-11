#!/usr/bin/env python3
"""Build 镇雄县 (Zhenxiong County) 领导班子工作关系网络.

云南省昭通市下辖县. 数据来源: 镇雄县人民政府网站, 百度百科, 新华网,
云岭先锋 (云南省委组织部任前公示).
调查日期: 2026-07-28.
"""

import sys
from pathlib import Path

# Allow importing gov_relation from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# -- Metadata --------------------------------------------------------------
SLUG = "镇雄县"
TODAY = "2026-07-28"
PROVINCE = "云南省"
CITY = "昭通市"

STAGING = Path(__file__).resolve().parent

# -- Persons ---------------------------------------------------------------
# id: unique int per person
persons = [
    # -- 县委常委 (14届县委, 2026年6月28日选举产生) --
    {
        "id": 1,
        "name": "吴君尧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "云南大关",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1994年8月",
        "current_post": "县委书记",
        "current_org": "中共镇雄县委",
        "source": "https://baike.baidu.com/item/%E5%90%B4%E5%90%9B%E5%B0%A7",
    },
    {
        "id": 2,
        "name": "杨绪春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年2月",
        "birthplace": "云南绥江",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1996年9月",
        "current_post": "县委副书记、县长",
        "current_org": "镇雄县人民政府",
        "source": "https://baike.baidu.com/item/%E6%9D%A8%E7%BB%AA%E6%98%A5",
    },
    {
        "id": 3,
        "name": "邓荣强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共镇雄县委",
        "source": "https://www.zhenxiong.gov.cn/",
    },
    {
        "id": 4,
        "name": "王国荣",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共镇雄县纪委",
        "source": "https://www.zhenxiong.gov.cn/",
    },
    {
        "id": 5,
        "name": "沈灿",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共镇雄县委",
        "source": "https://www.zhenxiong.gov.cn/",
    },
    {
        "id": 6,
        "name": "罗华钧",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共镇雄县委",
        "source": "https://www.zhenxiong.gov.cn/",
    },
    {
        "id": 7,
        "name": "文仕军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共镇雄县委",
        "source": "https://www.zhenxiong.gov.cn/",
    },
    {
        "id": 8,
        "name": "冯大勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共镇雄县委",
        "source": "https://www.zhenxiong.gov.cn/",
    },
    {
        "id": 9,
        "name": "李宗银",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共镇雄县委",
        "source": "https://www.zhenxiong.gov.cn/",
    },
    # -- 前任领导 --
    {
        "id": 10,
        "name": "肖顺兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年5月",
        "birthplace": "云南永善",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1996年10月",
        "current_post": "昭通市人民政府副市长",
        "current_org": "昭通市人民政府",
        "source": "https://baike.baidu.com/item/%E8%82%96%E9%A1%BA%E5%85%B4",
    },
    {
        "id": 11,
        "name": "翟玉龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/item/%E7%BF%9F%E7%8E%89%E9%BE%99",
    },
    # -- 副县长级 --
    {
        "id": 12,
        "name": "朱取",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县纪委副书记",
        "current_org": "中共镇雄县纪委",
        "source": "https://www.zhenxiong.gov.cn/",
    },
    {
        "id": 13,
        "name": "谭春",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县纪委副书记",
        "current_org": "中共镇雄县纪委",
        "source": "https://www.zhenxiong.gov.cn/",
    },
]

# -- Organizations --------------------------------------------------------
organizations = [
    {"id": 1, "name": "中共镇雄县委员会", "type": "党委", "level": "县级", "parent": "中共昭通市委", "location": "镇雄县"},
    {"id": 2, "name": "镇雄县人民政府", "type": "政府", "level": "县级", "parent": "昭通市人民政府", "location": "镇雄县"},
    {"id": 3, "name": "中共镇雄县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共昭通市纪委", "location": "镇雄县"},
    {"id": 4, "name": "镇雄县监察委员会", "type": "政府", "level": "县级", "parent": "镇雄县人民政府", "location": "镇雄县"},
    {"id": 5, "name": "昭通市人民政府", "type": "政府", "level": "地市级", "parent": "云南省人民政府", "location": "昭通市"},
    {"id": 6, "name": "中共威信县委", "type": "党委", "level": "县级", "parent": "中共昭通市委", "location": "威信县"},
    {"id": 7, "name": "威信县人民政府", "type": "政府", "level": "县级", "parent": "昭通市人民政府", "location": "威信县"},
    {"id": 8, "name": "中共永善县委", "type": "党委", "level": "县级", "parent": "中共昭通市委", "location": "永善县"},
    {"id": 9, "name": "昭通市自然资源和规划局", "type": "政府", "level": "地市级", "parent": "昭通市人民政府", "location": "昭通市"},
    {"id": 10, "name": "昭通市审计局", "type": "政府", "level": "地市级", "parent": "昭通市人民政府", "location": "昭通市"},
    {"id": 11, "name": "中共鲁甸县委", "type": "党委", "level": "县级", "parent": "中共昭通市委", "location": "鲁甸县"},
    {"id": 12, "name": "鲁甸县人民政府", "type": "政府", "level": "县级", "parent": "昭通市人民政府", "location": "鲁甸县"},
    {"id": 13, "name": "中共绥江县委", "type": "党委", "level": "县级", "parent": "中共昭通市委", "location": "绥江县"},
]

# -- Positions (career timeline entries) -----------------------------------
positions = [
    # -- 吴君尧 --
    {"person_id": 1, "org_id": 8, "title": "永善县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "早期履历"},
    {"person_id": 1, "org_id": 11, "title": "鲁甸县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "鲁甸县委副书记、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "昭通市审计局党组书记、局长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "昭通市自然资源和规划局党组书记、局长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "永善县委书记", "start_date": "2024-04", "end_date": "2026-05", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "镇雄县委书记", "start_date": "2026-05-26", "end_date": "", "rank": "正处级", "note": "2026年5月26日省委市委决定任命; 2026年6月28日14届县委一次全会选举"},
    # -- 杨绪春 --
    {"person_id": 2, "org_id": 13, "title": "（早期履历待查）", "start_date": "1996-09", "end_date": "", "rank": "", "note": "1996年9月参加工作, 早期履历未公开"},
    {"person_id": 2, "org_id": 2, "title": "镇雄县委副书记、县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "现任"},
    # -- 邓荣强 --
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026年6月28日14届县委一次全会选举"},
    # -- 王国荣 --
    {"person_id": 4, "org_id": 3, "title": "县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026年6月28日14届县委一次全会选举"},
    # -- 沈灿 --
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026年6月28日14届县委一次全会选举"},
    # -- 罗华钧 --
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026年6月28日14届县委一次全会选举"},
    # -- 文仕军 --
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026年6月28日14届县委一次全会选举"},
    # -- 冯大勇 --
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026年6月28日14届县委一次全会选举"},
    # -- 李宗银 --
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026年6月28日14届县委一次全会选举"},
    # -- 肖顺兴 (前任县委书记, 现任副市长) --
    {"person_id": 10, "org_id": 1, "title": "镇雄县委书记", "start_date": "", "end_date": "2026-05", "rank": "正处级", "note": "前任县委书记"},
    {"person_id": 10, "org_id": 6, "title": "威信县（县长/书记）", "start_date": "", "end_date": "", "rank": "正处级", "note": "调任镇雄前曾任威信县领导"},
    {"person_id": 10, "org_id": 5, "title": "昭通市人民政府副市长", "start_date": "2026-06-18", "end_date": "", "rank": "副厅级", "note": "2026年6月18日昭通市五届人大常委会第40次会议任"},
    # -- 翟玉龙 (前期县委书记) --
    {"person_id": 11, "org_id": 1, "title": "镇雄县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "前期县委书记, 任期约至2021-2024"},
    {"person_id": 11, "org_id": 11, "title": "鲁甸县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "调任镇雄前任鲁甸县委书记"},
    # -- 纪委副书记 --
    {"person_id": 12, "org_id": 3, "title": "县纪委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "县纪委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
]

# -- Relationships ---------------------------------------------------------
relationships = [
    # 吴君尧 vs 杨绪春—党政一把手共事
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县长工作搭档", "overlap_org": "镇雄县党政班子", "overlap_period": "2026-05至今"},
    # 吴君尧 vs 邓荣强—书记与专职副书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记—县委副书记", "overlap_org": "中共镇雄县委", "overlap_period": "2026-06至今"},
    # 杨绪春 vs 邓荣强—县长与专职副书记
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长—县委副书记同届共事", "overlap_org": "中共镇雄县委", "overlap_period": "2026-06至今"},
    # 肖顺兴—吴君尧 前后任交接
    {"person_a": 10, "person_b": 1, "type": "predecessor_successor", "context": "镇雄县委书记前后任交接", "overlap_org": "中共镇雄县委", "overlap_period": "2026-05"},
    # 翟玉龙—肖顺兴 前后任交接
    {"person_a": 11, "person_b": 10, "type": "predecessor_successor", "context": "镇雄县委书记前后任交接", "overlap_org": "中共镇雄县委", "overlap_period": "2021"},
    # 吴君尧—王国荣 书记与纪委书记
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记—县纪委书记", "overlap_org": "中共镇雄县委常委会", "overlap_period": "2026-06至今"},
    # 肖顺兴—杨绪春 前后任县长/书记搭档
    {"person_a": 10, "person_b": 2, "type": "overlap", "context": "县委书记—县长工作搭档", "overlap_org": "镇雄县党政班子", "overlap_period": "2021-2026"},
]


# -- Build -----------------------------------------------------------------
if __name__ == "__main__":
    db_path = STAGING / f"{SLUG}_network.db"
    gexf_path = STAGING / f"{SLUG}_network.gexf"

    print(f"Building {SLUG} network...")
    print(f"  DB:   {db_path}")
    print(f"  GEXF: {gexf_path}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:    {len(organizations)}")
    print(f"  Posns:   {len(positions)}")
    print(f"  Rels:    {len(relationships)}")

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
    print("Done.")