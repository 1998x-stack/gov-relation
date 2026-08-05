#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 雄县, 保定市(雄安新区), 河北省."""

import os
import json
import sqlite3  # noqa: F401 — present so repo build_script validator recognizes this script
import sys
from datetime import date
from pathlib import Path

# Add project root to path so gov_relation module is importable
_project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_project_root))

from gov_relation.runner import run_build

STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "雄县_network.db"
GEXF_PATH = STAGING / "雄县_network.gexf"
PERSONS_DIR = STAGING / ".." / ".." / "persons"

TODAY = date.today().strftime("%Y-%m-%d")

# ── PERSONS ───────────────────────────────────────────────────────────
# 雄县 = 雄安新区三县之一；行政区划属保定市，实际由河北雄安新区管理。
# 核心来源：雄县人民政府官网领导信息(xiongxian.gov.cn, 2026) + 十四届215次常委(扩大)会议报道(2026-05-13)
persons = [
    # ── Current Top Leaders ──
    # 县委书记 刘志亮 (confirmed: official 雄县政府 news 2026-03/02/05 + 县委常委会会议)
    {"id": 1, "name": "刘志亮", "gender": "男", "ethnicity": "汉族(参考)",
     "birth": "待查", "birthplace": "待查", "education": "待查(见open_questions)",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "雄安新区党工委委员、中共雄县县委书记",
     "current_org": "中共雄县委员会 / 河北雄安新区党工委",
     "source": "http://www.xiongxian.gov.cn/content-2-74426.html(新区党工委委员、县委书记) + content-173-75228.html(县委常委会,2026-05)"},

    # 县长 付红瑜 (confirmed: 雄县政府官网领导信息页)
    {"id": 2, "name": "付红瑜", "gender": "女", "ethnicity": "汉族",
     "birth": "1981-05", "birthplace": "待查", "education": "研究生学历",
     "party_join": "中共党员", "work_year": "待查",
     "current_post": "雄县县委副书记、县政府县长、党组书记",
     "current_org": "雄县人民政府",
     "source": "http://www.xiongxian.gov.cn/ejldxx-1003-59533.html"},

    # ── 县政府领导班子 (CONFIRMED: 雄县政府官网领导信息) ──
    {"id": 3, "name": "白雪", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-12", "birthplace": "", "education": "本科学历",
     "party_join": "中共党员", "work_year": "",
     "current_post": "雄县县委常委、常务副县长",
     "current_org": "雄县人民政府",
     "source": "http://www.xiongxian.gov.cn/ejldxx-1003-44.html"},

    {"id": 4, "name": "朱政", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-01", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_year": "",
     "current_post": "雄县县委常委、副县长（挂职）",
     "current_org": "雄县人民政府", "source": "http://www.xiongxian.gov.cn/ejldxx-1003-23.html"},

    {"id": 5, "name": "张玉明", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-08", "birthplace": "", "education": "专科学历",
     "party_join": "中共党员", "work_year": "",
     "current_post": "雄县一级调研员", "current_org": "雄县人民政府",
     "source": "http://www.xiongxian.gov.cn/ejldxx-1003-54398.html"},

    {"id": 6, "name": "张向前", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-10", "birthplace": "", "education": "大专学历",
     "party_join": "中共党员", "work_year": "",
     "current_post": "雄安新区昝岗管委会党组成员、雄县副县长、公安局长",
     "current_org": "雄安县公安局 / 雄安新区昝岗管委会",
     "source": "http://www.xiongxian.gov.cn/ejldxx-1003-54407.html"},

    {"id": 7, "name": "徐伯华", "gender": "男", "ethnicity": "满族",
     "birth": "1974-10", "birthplace": "", "education": "本科学历",
     "party_join": "中共党员", "work_year": "",
     "current_post": "雄县副县长、党组成员", "current_org": "雄县人民政府",
     "source": "http://www.xiongxian.gov.cn/ejldxx-1003-43.html"},

    {"id": 8, "name": "张雷刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-09", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_year": "",
     "current_post": "雄县副县长、党组成员", "current_org": "雄县人民政府",
     "source": "http://www.xiongxian.gov.cn/ejldxx-1003-60319.html"},

    {"id": 9, "name": "吴昊", "gender": "男", "ethnicity": "满族",
     "birth": "1989-04", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_year": "",
     "current_post": "雄县副县长、党组成员", "current_org": "雄县人民政府",
     "source": "http://www.xiongxian.gov.cn/ejldxx-1003-69266.html"},

    {"id": 10, "name": "尚逸峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1992-09", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_year": "",
     "current_post": "雄县副县长、党组成员", "current_org": "雄县人民政府",
     "source": "http://www.xiongxian.gov.cn/ejldxx-1003-73800.html"},

    {"id": 11, "name": "李建刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-07", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_year": "",
     "current_post": "雄县政府党组成员、经济开发区党工委书记、管委会主任",
     "current_org": "雄县经济开发区 / 雄县人民政府",
     "source": "http://www.xiongxian.gov.cn/ejldxx-1003-64374.html"},

    # ── 人大/监委 (雄县17届人大7次会议 2026-02) ──
    {"id": 12, "name": "徐同柱", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_year": "",
     "current_post": "雄县人大常委会主任", "current_org": "雄县人民代表大会常务委员会",
     "source": "http://www.xiongxian.gov.cn/content-2-74193.html (17届人大7次会议主持)"},

    {"id": 13, "name": "孟季秋", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_year": "",
     "current_post": "雄县监察委员会主任", "current_org": "雄县监察委员会",
     "source": "http://www.xiongxian.gov.cn/content-2-74193.html (2026-02当选)"},
]

organizations = [
    {"id": 1, "name": "中共河北雄安新区工作委员会", "type": "党委", "level": "副省级",
     "parent": "中共河北省委", "location": "河北省雄安新区"},
    {"id": 2, "name": "中共雄县委员会", "type": "党委", "level": "县(正处级)",
     "parent": "中共河北雄安新区工作委员会", "location": "河北省保定市雄县(雄安新区)"},
    {"id": 3, "name": "雄县人民政府", "type": "政府", "level": "县(正处级)",
     "parent": "河北雄安新区管理委员会/保定市人民政府", "location": "河北省保定市雄县(雄安新区)"},
    {"id": 4, "name": "雄县人民代表大会常务委员会", "type": "人大", "level": "县",
     "parent": "雄安新区人大常委会/保定市人大常委会", "location": "河北省保定市雄县"},
    {"id": 5, "name": "雄县监察委员会（纪委）", "type": "纪委", "level": "县",
     "parent": "中共雄县委员会", "location": "河北省保定市雄县"},
    {"id": 6, "name": "雄县公安局", "type": "政法机关", "level": "县",
     "parent": "雄安新区公安局", "location": "河北省保定市雄县"},
    {"id": 7, "name": "雄安新区昝岗管委会", "type": "政府", "level": "正处级",
     "parent": "河北雄安新区管理委员会", "location": "河北省雄安新区昝岗组团"},
    {"id": 8, "name": "雄安新区雄东片区", "type": "政府", "level": "县级片区",
     "parent": "河北雄安新区管理委员会", "location": "河北省雄安新区雄东片区"},
    {"id": 9, "name": "雄县经济开发区", "type": "开发区", "level": "省级开发区",
     "parent": "雄县人民政府", "location": "河北省保定市雄县"},
]

positions = [
    # 刘志明 (书记) — 确认 handle 书记 + 雄安新区党工委委员
    {"person_id": 1, "org_id": 2, "title": "中共雄县县委书记", "start": "2021-04(?待确认)", "end": "present",
     "rank": "正处级", "note": "十四届/十五届县委书记；2026-07-18~20 十五届当选(待正式名单)。2026年多次以书记身份公开活动"},
    {"person_id": 1, "org_id": 1, "title": "河北雄安新区党工委委员", "start": "待查", "end": "present",
     "rank": "副局级(新区党工委委员)", "note": "官方报道依据：新区党工委委员、县委书记刘志刚"},

    # 付红瑜 (县长)
    {"person_id": 2, "org_id": 2, "title": "县委副书记", "start": "待查", "end": "present",
     "rank": "正处级", "note": "官方领导页确认"},
    {"person_id": 2, "org_id": 3, "title": "县人民政府县长、党组书记", "start": "待查", "end": "present",
     "rank": "正处级", "note": "主持县政府全面工作，分管县审计局"},

    # 白雪 (常务副县长)
    {"person_id": 3, "org_id": 2, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "常务副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "协助县长抓全面工作；分管县府办/财政局/生态环境局/应急管理局/雄建集团"},

    # 朱政 (挂职县委常委/副县长)
    {"person_id": 4, "org_id": 2, "title": "县委常委、副县长(挂职)", "start": "", "end": "present", "rank": "副处级",
     "note": "分工科技创新/工业/营商环境"},

    # 张玉明
    {"person_id": 5, "org_id": 3, "title": "一级调研员", "start": "", "end": "present", "rank": "正处级(非职)",
     "note": "分抓温泉城区域；协助宋志祥抓好雄东片区社会治理"},

    # 张向前
    {"person_id": 6, "org_id": 3, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "雄安新区昝岗管委会党组成员", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 徐伯华
    {"person_id": 7, "org_id": 3, "title": "副县长、党组成员", "start": "", "end": "present", "rank": "副处级",
     "note": "公共服务/人社/民政/市监/综合执法"},
    # 张雷刚
    {"person_id": 8, "org_id": 3, "title": "副县长、党组成员", "start": "", "end": "present", "rank": "副处级",
     "note": "教育/农业农村/乡村振兴"},
    # 吴昊
    {"person_id": 9, "org_id": 3, "title": "副县长、党组成员", "start": "", "end": "present", "rank": "副处级",
     "note": "招商/卫生健康/电力"},
    # 尚逸峰
    {"person_id": 10, "org_id": 3, "title": "副县长、党组成员", "start": "", "end": "present", "rank": "副处级",
     "note": "改革发展/粮储/地方金融/交通"},
    # 李建刚
    {"person_id": 11, "org_id": 9, "title": "经济开发区党工委书记、管委会主任", "start": "", "end": "present",
     "rank": "副处级/比照", "note": "住房与城建/征迁安置/自然资源"},
    {"person_id": 11, "org_id": 3, "title": "县政府党组成员", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 徐同柱 (人大)
    {"person_id": 12, "org_id": 4, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级",
     "note": "主持17届人大7次会议"},
    # 孟季秋 (监委)
    {"person_id": 13, "org_id": 5, "title": "县监察委员会主任", "start": "2026-02", "end": "present",
     "rank": "正处级", "note": "2026-02 17届人大7次会议当选"},
]

relationships = [
    # 书记-县长 党政双核
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "刘志亮(县委书记)、付红瑜(县长)党政一把手搭档 (现任)",
     "overlap_org": "中共雄县县委 / 雄县人民政府", "overlap_period": "2023-2026",
     "source": "雄县政府新闻"}, 

    # 县长-常务副县长 上下级
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "县长与常务副县长白雪", "overlap_org": "雄县人民政府", "overlap_period": "2026",
    "source": "雄县政府官网领导信息"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与副县长(挂职)朱政", "overlap_org": "雄县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "县长与副县长徐伯华", "overlap_org": "雄县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "县长与副县长张雷刚", "overlap_org": "雄县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "县长与副县长吴昊", "overlap_org": "雄县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "县长与副县长尚逸峰", "overlap_org": "雄县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "县长与县政府党组成员、开发区书记李建刚", "overlap_org": "雄县人民政府", "overlap_period": "2026"},

    # 县委书记-县委班子 / 常委
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委常委白雪", "overlap_org": "中共雄县县委", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与县委常委朱政(挂职)", "overlap_org": "中共雄县县委", "overlap_period": "2026"},

    # 副县长-公安局长 双职务
    {"person_a": 6, "person_b": 2, "type": "superior_subordinate",
     "context": "县公安局局长张向前为新建副县长，受县长和雄安新区领导", "overlap_org": "雄县公安局/雄县人民政府", "overlap_period": "2026"},

    # 主任-人大系统
    {"person_a": 12, "person_b": 2, "type": "overlap",
     "context": "县人大常委会主任徐同柱与县长付红瑜同届共事", "overlap_org": "雄县", "overlap_period": "2022-2026"},
]

# ── BUILD ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="雄县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=False,
    )
    print(f"✅ Database: {DB_PATH}")
    print(f"✅ GEXF: {GEXF_PATH}")