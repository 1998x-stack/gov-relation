#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Datong Hui and Tu Autonomous County leadership network."""

import os
import sqlite3
import sys
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "大通回族土族自治县"
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "大通回族土族自治县_network.db")
GEXF_PATH = os.path.join(BASE, "大通回族土族自治县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {"id": 1, "name": "马明旭", "gender": "男", "ethnicity": "回族",
     "birth": "1979-08", "birthplace": "青海海东",
     "education": "省委党校研究生，行政管理硕士学位",
     "party_join": "2005-12", "work_start": "2000-07",
     "current_post": "县委书记", "current_org": "中共大通回族土族自治县委员会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 2, "name": "王生龙", "gender": "男", "ethnicity": "土族",
     "birth": "1988-04", "birthplace": "青海西宁",
     "education": "青海省委党校研究生学历",
     "party_join": "2008-05", "work_start": "2009-11",
     "current_post": "县委副书记、县政府县长", "current_org": "大通回族土族自治县人民政府",
     "source": "https://www.datong.gov.cn/"},

    # ── Other County Party Committee Secretaries (县委常委) ──
    {"id": 3, "name": "娄杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-05", "birthplace": "江苏南京",
     "education": "在职大学学历",
     "party_join": "2004-10", "work_start": "1999-01",
     "current_post": "县委副书记、县政府副县长（挂职）", "current_org": "中共大通回族土族自治县委员会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 4, "name": "赵寿", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-11", "birthplace": "青海西宁",
     "education": "中央党校大学学历",
     "party_join": "2007-10", "work_start": "2002-01",
     "current_post": "县委副书记", "current_org": "中共大通回族土族自治县委员会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 5, "name": "鲍赟", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1984-06", "birthplace": "青海乌兰",
     "education": "研究生学历，应用经济学硕士",
     "party_join": "2008-05", "work_start": "2008-10",
     "current_post": "县委常委、政法委书记", "current_org": "中共大通回族土族自治县委员会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 6, "name": "蔡秀珍", "gender": "女", "ethnicity": "汉族",
     "birth": "1980-01", "birthplace": "青海西宁",
     "education": "大专学历",
     "party_join": "2006-09", "work_start": "2000-10",
     "current_post": "县委常委、宣传部部长、县总工会主席", "current_org": "中共大通回族土族自治县委员会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 7, "name": "谢骥", "gender": "男", "ethnicity": "土族",
     "birth": "1977-11", "birthplace": "青海大通",
     "education": "省委党校研究生学历",
     "party_join": "1997-06", "work_start": "1997-08",
     "current_post": "县委常委、统战部部长", "current_org": "中共大通回族土族自治县委员会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 8, "name": "王全", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-10", "birthplace": "青海海东",
     "education": "大学学历",
     "party_join": "2004-06", "work_start": "1999-09",
     "current_post": "县委常委、纪委书记、监委主任", "current_org": "中共大通回族土族自治县纪律检查委员会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 9, "name": "董元基", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-03", "birthplace": "青海湟源",
     "education": "大学学历，理学学士学位",
     "party_join": "2017-06", "work_start": "2009-08",
     "current_post": "县委常委、组织部部长", "current_org": "中共大通回族土族自治县委员会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 10, "name": "陈贤", "gender": "男", "ethnicity": "汉族",
     "birth": "1989-11", "birthplace": "湖南祁东",
     "education": "研究生学历，法学硕士",
     "party_join": "2008-06", "work_start": "2014-07",
     "current_post": "县委常委、县政府副县长（挂职）", "current_org": "大通回族土族自治县人民政府",
     "source": "https://www.datong.gov.cn/"},

    # ── County Government Deputy Leaders ──
    {"id": 11, "name": "雷振刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-05", "birthplace": "青海西宁",
     "education": "大专学历",
     "party_join": "1999-05", "work_start": "1999-11",
     "current_post": "县政府副县长、县公安局局长", "current_org": "大通回族土族自治县人民政府",
     "source": "https://www.datong.gov.cn/"},
    {"id": 12, "name": "车贤仁", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-02", "birthplace": "青海大通",
     "education": "在职本科学历，汉语言文学学位",
     "party_join": "2001-06", "work_start": "1997-07",
     "current_post": "县政府副县长", "current_org": "大通回族土族自治县人民政府",
     "source": "https://www.datong.gov.cn/"},
    {"id": 13, "name": "李智呈", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-06", "birthplace": "青海大通",
     "education": "在职大学学历",
     "party_join": "2003-06", "work_start": "2001-09",
     "current_post": "县政府副县长", "current_org": "大通回族土族自治县人民政府",
     "source": "https://www.datong.gov.cn/"},
    {"id": 14, "name": "张明", "gender": "男", "ethnicity": "藏族",
     "birth": "1987-11", "birthplace": "青海民和",
     "education": "党校研究生学历，法学学士学位",
     "party_join": "2008-11", "work_start": "2009-09",
     "current_post": "县政府副县长", "current_org": "大通回族土族自治县人民政府",
     "source": "https://www.datong.gov.cn/"},
    {"id": 15, "name": "韩超", "gender": "男", "ethnicity": "回族",
     "birth": "1988-04", "birthplace": "青海大通",
     "education": "大学学历",
     "party_join": "2012-03", "work_start": "2011-10",
     "current_post": "县政府副县长", "current_org": "大通回族土族自治县人民政府",
     "source": "https://www.datong.gov.cn/"},

    # ── People's Congress (县人大) ──
    {"id": 16, "name": "王占福", "gender": "男", "ethnicity": "藏族",
     "birth": "1974-06", "birthplace": "青海互助",
     "education": "省委党校研究生学历",
     "party_join": "1998-11", "work_start": "1999-09",
     "current_post": "县人大常委会党组书记、主任", "current_org": "大通回族土族自治县人大常委会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 17, "name": "李承宽", "gender": "男", "ethnicity": "土族",
     "birth": "1967-06", "birthplace": "青海大通",
     "education": "省委党校研究生学历",
     "party_join": "1993-01", "work_start": "1987-07",
     "current_post": "县人大常委会党组成员、副主任", "current_org": "大通回族土族自治县人大常委会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 18, "name": "兰存义", "gender": "男", "ethnicity": "藏族",
     "birth": "1968-05", "birthplace": "青海大通",
     "education": "省委党校研究生学历",
     "party_join": "1994-11", "work_start": "1991-07",
     "current_post": "县人大常委会党组成员、副主任", "current_org": "大通回族土族自治县人大常委会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 19, "name": "吴晓钟", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-05", "birthplace": "青海化隆",
     "education": "大学学历",
     "party_join": "2000-05", "work_start": "1996-07",
     "current_post": "县人大常委会党组成员、副主任", "current_org": "大通回族土族自治县人大常委会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 20, "name": "马笑瑛", "gender": "女", "ethnicity": "回族",
     "birth": "1973-03", "birthplace": "青海西宁",
     "education": "大学学历，文学学士学位",
     "party_join": "民革党员", "work_start": "1995-09",
     "current_post": "县人大常委会副主任", "current_org": "大通回族土族自治县人大常委会",
     "source": "https://www.datong.gov.cn/"},

    # ── CPPCC (县政协) ──
    {"id": 21, "name": "井绪华", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-01", "birthplace": "山东汶上",
     "education": "中央党校大学学历",
     "party_join": "2000-09", "work_start": "1990-10",
     "current_post": "县政协党组书记、主席", "current_org": "政协大通回族土族自治县委员会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 22, "name": "李春", "gender": "女", "ethnicity": "汉族",
     "birth": "1972-05", "birthplace": "青海乐都",
     "education": "党校研究生学历",
     "party_join": "1997-06", "work_start": "1991-07",
     "current_post": "县政协副主席", "current_org": "政协大通回族土族自治县委员会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 23, "name": "白统龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-09", "birthplace": "青海大通",
     "education": "本科学历",
     "party_join": "民建会员", "work_start": "1998-07",
     "current_post": "县政协副主席、民建西宁市委副主委（兼职）", "current_org": "政协大通回族土族自治县委员会",
     "source": "https://www.datong.gov.cn/"},
    {"id": 24, "name": "张宝贵", "gender": "男", "ethnicity": "土族",
     "birth": "1969-09", "birthplace": "青海大通",
     "education": "大学学历",
     "party_join": "1996-01", "work_start": "1996-07",
     "current_post": "县政协副主席", "current_org": "政协大通回族土族自治县委员会",
     "source": "https://www.datong.gov.cn/"},
]

organizations = [
    {"id": 1, "name": "中共大通回族土族自治县委员会", "type": "党委", "level": "县级", "parent": "中共西宁市委员会", "location": "青海省西宁市大通县"},
    {"id": 2, "name": "大通回族土族自治县人民政府", "type": "政府", "level": "县级", "parent": "西宁市人民政府", "location": "青海省西宁市大通县"},
    {"id": 3, "name": "中共大通回族土族自治县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共西宁市纪律检查委员会", "location": "青海省西宁市大通县"},
    {"id": 4, "name": "大通回族土族自治县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "青海省西宁市大通县"},
    {"id": 5, "name": "政协大通回族土族自治县委员会", "type": "政协", "level": "县级", "parent": "", "location": "青海省西宁市大通县"},
    {"id": 6, "name": "大通回族土族自治县公安局", "type": "政府", "level": "科级", "parent": "大通回族土族自治县人民政府", "location": "青海省西宁市大通县"},
]

# Positions: person_id, org_id, title, start_date, end_date, rank, note
positions = [
    # 马明旭
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 王生龙
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县政府县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 娄杰
    {"person_id": 3, "org_id": 1, "title": "县委副书记、县政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "", "note": "东西部协作挂职"},
    # 赵寿
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 鲍赟
    {"person_id": 5, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 蔡秀珍
    {"person_id": 6, "org_id": 1, "title": "县委常委、宣传部部长、县总工会主席", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 谢骥
    {"person_id": 7, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 王全
    {"person_id": 8, "org_id": 3, "title": "县委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 董元基
    {"person_id": 9, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 陈贤
    {"person_id": 10, "org_id": 2, "title": "县委常委、县政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "", "note": "挂职"},
    # 雷振刚
    {"person_id": 11, "org_id": 2, "title": "县政府副县长、县公安局局长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 车贤仁
    {"person_id": 12, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管农业农村、水利、乡村振兴"},
    # 李智呈
    {"person_id": 13, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管自然资源、住建、城管、交通"},
    # 张明
    {"person_id": 14, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管生态环境、民政、市场监管、林草"},
    # 韩超
    {"person_id": 15, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 人大
    {"person_id": 16, "org_id": 4, "title": "县人大常委会党组书记、主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 17, "org_id": 4, "title": "县人大常委会党组成员、副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 18, "org_id": 4, "title": "县人大常委会党组成员、副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "县人大常委会党组成员、副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 政协
    {"person_id": 21, "org_id": 5, "title": "县政协党组书记、主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 22, "org_id": 5, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 23, "org_id": 5, "title": "县政协副主席、民建西宁市委副主委（兼职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 24, "org_id": 5, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
]

# Relationships
relationships = [
    # 马明旭 <-> 王生龙: 上下级关系 (县委书记/县长)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政领导班子核心搭档", "overlap_org": "中共大通回族土族自治县委员会", "overlap_period": ""},
    # 马明旭 <-> other county party committee members: 领导班子成员
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共大通回族土族自治县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共大通回族土族自治县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共大通回族土族自治县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共大通回族土族自治县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共大通回族土族自治县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共大通回族土族自治县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共大通回族土族自治县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共大通回族土族自治县委员会", "overlap_period": ""},
    # 王生龙 <-> deputy mayors: 县政府领导班子
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "县长与副县长工作关系", "overlap_org": "大通回族土族自治县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "县长与副县长工作关系", "overlap_org": "大通回族土族自治县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "县长与副县长工作关系", "overlap_org": "大通回族土族自治县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "县长与副县长工作关系", "overlap_org": "大通回族土族自治县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "县长与副县长工作关系", "overlap_org": "大通回族土族自治县人民政府", "overlap_period": ""},
    # 王生龙 <-> 陈贤 (挂职副县长, 也是县委常委)
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "县政府班子成员", "overlap_org": "大通回族土族自治县人民政府", "overlap_period": ""},
]


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
    print(f"Done: {DB_PATH}, {GEXF_PATH}")
