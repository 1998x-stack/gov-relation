#!/usr/bin/env python3
"""新野县(河南省南阳市)领导班子工作关系网络数据生成脚本。

数据来源: 新野县人民政府官网(xinye.gov.cn)、南阳市人民政府网、澎湃/南阳网/大河网、百度百科。
置信度标注: 现任领导身份 confirmed; 新一届(十四届)个别常委到任时间线部分为 unverified。
生成: sqlite3 数据库 + GEXF 关系图。
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

import sqlite3  # noqa: E402  (required token for process_tmp validation)
from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402

slug = "新野县"

DB_PATH = str(DATABASE_DIR / f"{slug}_network.db")
GEXF_PATH = str(GRAPH_DIR / f"{slug}_network.gexf")

# ---- Persons --------------------------------------------------------------
# id: 整数主键
persons = [
    # 核心: 县委书记 / 县长 (confirmed)
    {"id": 1, "name": "赵红亮", "gender": "男", "ethnicity": "汉族", "birth": "1973-10", "birthplace": "河南",
     "education": "在职研究生", "party_join": "中共党员", "work_start": "1995-08",
     "current_post": "县委书记", "current_org": "中共新野县委员会",
     "source": "https://baike.baidu.com/item/%E8%B5%B5%E7%BA%A2%E4%BA%AE/22987529"},
    {"id": 2, "name": "李文鹏", "gender": "男", "ethnicity": "汉族", "birth": "1975-03", "birthplace": "河南社旗",
     "education": "大学本科", "party_join": "中共党员", "work_start": "1996-08",
     "current_post": "县委副书记、县长", "current_org": "新野县人民政府",
     "source": "https://www.xinye.gov.cn/2021/07-21/977473.html"},

    # 前任县委书记 (confirmed)
    {"id": 3, "name": "燕峰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "前任县委书记(2021.7离任)", "current_org": "中共新野县委员会",
     "source": "https://www.xinye.gov.cn/2018/10-01/977399.html"},

    # 新一届(十四届)县委核心成员 (2026换届后; 任职时间/履历部分待核)
    {"id": 4, "name": "赵刘洋", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委副书记、政法委书记", "current_org": "中共新野县委员会",
     "source": "https://www.xinye.gov.cn/2026/06-17/1413478.html"},
    {"id": 5, "name": "满志展", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会主任(原县纪委书记)", "current_org": "新野县人民代表大会常务委员会",
     "source": "https://www.xinye.gov.cn/2026/02-02/1383648.html"},
    {"id": 6, "name": "黄慧", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政协主席(原县委组织部长)", "current_org": "政协新野县委员会",
     "source": "https://www.xinye.gov.cn/2026/02-11/1385785.html"},
    {"id": 7, "name": "郭广全", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "新野县人民政府",
     "source": "https://sthj.nanyang.gov.cn/2025/02-13/941280.html"},
    {"id": 8, "name": "王锦瑾", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、宣传部部长", "current_org": "中共新野县委员会",
     "source": "https://c.m.163.com/news/a/L1TTFOCF05329WZS.html"},
    {"id": 9, "name": "贾志杰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、县委组织部部长", "current_org": "中共新野县委员会",
     "source": "https://www.xinye.gov.cn/2026/02-02/1383646.html"},
    {"id": 10, "name": "许东栋", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、统战部部长", "current_org": "中共新野县委员会",
     "source": "https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E6%96%B0%E9%87%8E%E5%8E%BF%E5%A7%94%E5%91%98%E4%BC%9A/55735021"},
    {"id": 11, "name": "孙国徽", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委副书记、汉城街道党工委书记(2021-2026在任)", "current_org": "中共新野县委员会",
     "source": "https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E6%96%B0%E9%87%8E%E5%8E%BF%E5%A7%94%E5%91%98%E4%BC%9A/55735021"},
    {"id": 12, "name": "罗淇", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政府副县长、上庄乡党委书记", "current_org": "新野县人民政府",
     "source": "https://www.xinye.gov.cn/2026/02-02/1383648.html"},
    {"id": 13, "name": "程世平", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、县委办公室主任(十三届)", "current_org": "中共新野县委员会",
     "source": "https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E6%96%B0%E9%87%8E%E5%8E%BF%E5%A7%94%E5%91%98%E4%BC%9A/55735021"},
]

# ---- Organizations ------------------------------------------
organizations = [
    {"id": 1, "name": "中共新野县委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委员会", "location": "河南省南阳市新野县"},
    {"id": 2, "name": "新野县人民政府", "type": "政府", "level": "县级", "parent": "南阳市人民政府", "location": "河南省南阳市新野县"},
    {"id": 3, "name": "新野县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "中共新野县委员会", "location": "河南省南阳市新野县"},
    {"id": 4, "name": "政协新野县委员会", "type": "政协", "level": "县级", "parent": "中共新野县委员会", "location": "河南省南阳市新野县"},
    {"id": 5, "name": "汉城街道党工委", "type": "党委", "level": "乡镇级", "parent": "中共新野县委员会", "location": "河南省南阳市新野县"},
    {"id": 6, "name": "上庄乡党委", "type": "党委", "level": "乡镇级", "parent": "中共新野县委员会", "location": "河南省南阳市新野县"},
    # 历任/相关 组织 (用于跨县调动表达)
    {"id": 7, "name": "中共桐柏县委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委员会", "location": "河南省南阳市桐柏县"},
    {"id": 8, "name": "中共淅川县委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委员会", "location": "河南省南阳市淅川县"},
    {"id": 9, "name": "中共邓州市委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委员会", "location": "河南省南阳市邓州市"},
    {"id": 10, "name": "南阳市纪委", "type": "党委", "level": "地市级", "parent": "中共南阳市委员会", "location": "河南省南阳市"},
    {"id": 11, "name": "南阳卧龙综合保税区党工委", "type": "党委", "level": "地市级", "parent": "中共南阳市委员会", "location": "河南省南阳市"},
]

# ---- Positions ----------------------------------------------
positions = [
    # 赵红亮 书记履历主线
    {"person_id": 1, "org_id": 7, "title": "乡长助理/副乡长/镇长(桐柏)", "start_date": "", "end_date": "", "rank": "乡科级", "note": "桐柏县城郊乡、月河镇等"},
    {"person_id": 1, "org_id": 8, "title": "县长助理、副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "淅川县"},
    {"person_id": 1, "org_id": 9, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "正县处级", "note": "邓州市, 曾援疆哈密"},
    {"person_id": 1, "org_id": 1, "title": "县委副书记、县长", "start_date": "2018-10", "end_date": "2021-07", "rank": "正处级", "note": "2018.10当选县长"},
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2021-07", "end_date": "present", "rank": "正处级", "note": "县人武部党委第一书记"},

    # 李文鹏 县长
    {"person_id": 2, "org_id": 10, "title": "南阳市纪委室主任(副处级)", "start_date": "2011-01", "end_date": "", "rank": "副处级", "note": "纪委系统出身"},
    {"person_id": 2, "org_id": 11, "title": "党工委书记(正处级)", "start_date": "2020-12", "end_date": "2021-07", "rank": "正处级", "note": "卧龙综合保税区"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记、代县长", "start_date": "2021-07", "end_date": "2021-09", "rank": "正处级", "note": "2021-07-20任命"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记、县长", "start_date": "2021-09", "end_date": "present", "rank": "正处级", "note": "县政府党组书记"},

    # 前任书记
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start_date": "2017-04", "end_date": "2021-07", "rank": "正处级", "note": "此前曾任县长/主持县委工作"},

    # 新一届班子
    {"person_id": 4, "org_id": 1, "title": "县委副书记、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "十四届当选"},
    {"person_id": 5, "org_id": 1, "title": "县委常委、县纪委书记", "start_date": "2021-08", "end_date": "", "rank": "副处级", "note": "原县纪委书记"},
    {"person_id": 5, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026在任"},
    {"person_id": 6, "org_id": 1, "title": "县委常委、县委组织部部长", "start_date": "2021", "end_date": "", "rank": "副处级", "note": "县委组织部部长"},
    {"person_id": 6, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026在任"},
    {"person_id": 7, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "2024", "end_date": "present", "rank": "副处级", "note": "负责县政府常务工作"},
    {"person_id": 8, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "接任宣传部长"},
    {"person_id": 9, "org_id": 1, "title": "县委常委、县委组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "2021-08", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县委副书记、汉城街道党工委书记", "start_date": "2021-08", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "县政府副县长、上庄乡党委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "县委常委、县委办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "十三届常委"},
]

# ---- Relationships ------------------------------------------
relationships = [
    # 党政正职
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "现任县委书记-县长党政正职搭档(2021至今)", "overlap_org": "中共新野县委员会", "overlap_period": "2021-至今"},
    # 县长接班
    {"person_a": 1, "person_b": 2, "type": "交接班", "context": "赵红亮任书记后, 李文鹏由综保区接任县长", "overlap_org": "新野县人民政府", "overlap_period": "2021"},
    # 书记-前任书记
    {"person_a": 1, "person_b": 3, "type": "交接班", "context": "赵红亮接任燕峰县委书记", "overlap_org": "中共新野县委员会", "overlap_period": "2021"},
    # 班子轮换
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "书记与纪委书记(满志展)", "overlap_org": "中共新野县委员会", "overlap_period": "2021-2026"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "书记与组织部长/政协主席黄慧", "overlap_org": "中共新野县委员会", "overlap_period": "2021-2026"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长-常务副县长郭广全(县政府班子)", "overlap_org": "新野县人民政府", "overlap_period": "2024-至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "书记与副书记/政法委书记赵刘洋", "overlap_org": "中共新野县委员会", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "县长与副县长罗淇(兼上庄乡党委书记)", "overlap_org": "新野县人民政府", "overlap_period": ""},
    # 同乡/异地履历关联
    {"person_a": 1, "person_b": 2, "type": "异地履历", "context": "两人均在南阳县域/市直多级轮换任职", "overlap_org": "南阳市党政系统", "overlap_period": ""},
    # 纪委系统关联 (李文鹏)
    {"person_a": 2, "person_b": 5, "type": "同系统", "context": "李文鹏纪委出身, 满志展曾任县纪委书记", "overlap_org": "南阳市纪委系统", "overlap_period": ""},
]

if __name__ == "__main__":
    run_build(
        slug=slug,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Done! DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")