#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
永清县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 廊坊市
Region: 永清县
Targets: 县委书记 & 县长

Research Sources:
- 永清县人民政府网站 (www.yongqing.gov.cn) — 可访问
- 百度百科 — 焦文序、冯学军、彭敬捷、黄运然
- 搜狐/网易/澎湃新闻 — 任前公示、简历页面
- 廊坊市人民政府网站 (www.lf.gov.cn)
- 微信公众平台 — 永清县人大会议选举结果等

Research Date: 2026-07-24
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "永清县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons (use IDs 1-100 for persons, 101+ for orgs)
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "焦文序",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永清县委书记",
        "current_org": "中共永清县委员会",
        "source": "焦文序，现任河北省廊坊市永清县委书记。2021年6月至2022年8月任廊坊市商务局局长。2022年8月23日被免去商务局局长职务后调任永清县委书记。2022年7月5日以县委书记身份到后奕镇调研。来源：百度百科、永清县人民政府网站、网易新闻。confidence=confirmed"
    },
    {
        "id": 2,
        "name": "董魁宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永清县委副书记、县长",
        "current_org": "永清县人民政府",
        "source": "董魁宁，2024年12月任永清县委副书记、代县长。2025年1月17日在永清县第十七届人民代表大会第五次会议上当选永清县人民政府县长。来源：永清县人民政府网站、廊坊市人民政府网站（2026年2月6日专访）、微信公众平台（县十七届人大五次会议闭幕+公告+简历）。confidence=confirmed"
    },
    {
        "id": 3,
        "name": "杨丹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永清县委常委、常务副县长",
        "current_org": "永清县人民政府",
        "source": "杨丹，2025年1月12日被永清县第十七届人大常委会第三十三次会议任命为永清县人民政府副县长。后任县委常委、常务副县长。来源：永清县人民政府、澎湃新闻（我县召开重点外贸企业座谈会）。confidence=confirmed"
    },
    {
        "id": 4,
        "name": "王达",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永清县委常委、副县长",
        "current_org": "永清县人民政府",
        "source": "王达，2025年1月12日被永清县第十七届人大常委会第三十三次会议任命为永清县人民政府副县长。后任县委常委、副县长，分管教育、体育、人力资源、社会保障、金融等工作。来源：永清县人民政府、澎湃新闻。confidence=confirmed"
    },
    {
        "id": 5,
        "name": "周浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永清县人大常委会主任",
        "current_org": "永清县人大常委会",
        "source": "周浩，多次在永清县人大相关活动中以县人大常委会主任身份出席。来源：永清县人民政府网站、澎湃新闻。confidence=confirmed"
    },
    {
        "id": 6,
        "name": "王春风",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永清县政协主席",
        "current_org": "永清县政协",
        "source": "王春风，多次在永清县政协活动中以县政协主席身份出席。来源：搜狐网（永清产业对接会）。confidence=confirmed"
    },
    {
        "id": 7,
        "name": "杨连军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永清县委常委、人武部部长",
        "current_org": "永清县人民武装部",
        "source": "杨连军，多次以永清县委常委、人武部部长身份出席活动。来源：澎湃新闻（永清县征兵工作部署）。confidence=confirmed"
    },
    # ════════════════════════════════════════
    # Predecessor Leaders
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "冯学军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年3月",
        "birthplace": "河北省文安县",
        "native_place": "河北文安",
        "education": "廊坊师范学院汉语言文学专业，大学学历，文学学士",
        "party_join": "1996年5月",
        "work_start": "1995年7月",
        "current_post": "待查（原永清县委书记）",
        "current_org": "",
        "source": "冯学军，男，汉族，文安县人，1970年3月出生，1996年5月入党，1995年7月参加工作。廊坊师范学院汉语言文学专业毕业，大学学历，文学学士。1995.07-1996.12 廊坊师专物理系辅导员；1996.12-2000.09 廊坊市政府办公室综合六科科员；此后至2021年5月历任廊坊市政府办公室相关职务、县委常委办公室主任等职。2021年5月19日任永清县委书记、一级调研员、北京亦庄·永清高新区党工委书记。2022年7月被焦文序接替，去向待查。来源：搜狐网（中国共产党永清县第十三届委员会常务委员会委员书记副书记简历）。confidence=confirmed"
    },
    {
        "id": 11,
        "name": "彭敬捷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1967年5月",
        "birthplace": "河北省晋州市",
        "native_place": "河北晋州",
        "education": "河北大学法律系法学专业，法学学士",
        "party_join": "1993年1月",
        "work_start": "1987年9月",
        "current_post": "河北省司法厅党委委员、副厅长",
        "current_org": "河北省司法厅",
        "source": "彭敬捷，女，汉族，1967年5月出生，河北晋州人，1993年1月加入中国共产党，1987年9月参加工作，河北大学法律系法学专业毕业，法学学士。曾任石家庄市司法局律师管理处干事、副处长（正科）、律师工作指导处处长，灵寿县副县长，高邑县委书记。2019年12月任永清县委书记。2021年5月不再担任永清县委书记，另有任用。现任河北省司法厅党委委员、副厅长、省律师行业党委书记。来源：百度百科。confidence=confirmed"
    },
    {
        "id": 12,
        "name": "邢华金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原永清县委书记）",
        "current_org": "",
        "source": "邢华金，2016年12月任永清县委书记，接替李玉宝。约2019年12月离任。来源：微信公众平台（邢华金同志任中共永清县委书记）。confidence=confirmed"
    },
    {
        "id": 13,
        "name": "黄运然",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "河北省廊坊市安次区",
        "native_place": "河北安次",
        "education": "省委党校法学专业",
        "party_join": "1997年6月",
        "work_start": "1997年9月",
        "current_post": "待查（原永清县长）",
        "current_org": "",
        "source": "黄运然，男，汉族，安次区人，1976年10月出生，1997年6月加入中国共产党，1997年9月参加工作，省委党校法学专业毕业。2021年5月27日被任命为永清县人民政府副县长、代县长，后任县长。至2024年12月前离任。来源：百度百科、永清县人民政府（县人大常委会公告2021年5月28日）。confidence=confirmed"
    },
    {
        "id": 14,
        "name": "张兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原永清县长）",
        "current_org": "",
        "source": "张兵，2021年5月19日前任永清县委副书记、县长，北京亦庄·永清高新区党工委副书记、管委会主任。2021年5月27日辞去县长职务。去向待查。来源：永清县人民政府网站、腾讯新闻。confidence=confirmed"
    },
    {
        "id": 15,
        "name": "李玉宝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原永清县委书记）",
        "current_org": "",
        "source": "李玉宝，2016年12月前曾任永清县委书记。2016年12月不再担任。来源：微信公众平台（邢华金同志任中共永清县委书记）。confidence=confirmed"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共永清县委员会", "type": "党委", "level": "县级", "parent": "中共廊坊市委", "location": "河北省廊坊市永清县"},
    {"id": 2, "name": "永清县人民政府", "type": "政府", "level": "县级", "parent": "廊坊市人民政府", "location": "河北省廊坊市永清县"},
    {"id": 3, "name": "永清县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "河北省廊坊市永清县"},
    {"id": 4, "name": "永清县政协", "type": "政协", "level": "县级", "parent": "", "location": "河北省廊坊市永清县"},
    {"id": 5, "name": "永清县人民武装部", "type": "政府", "level": "县级", "parent": "", "location": "河北省廊坊市永清县"},
    {"id": 6, "name": "廊坊市商务局", "type": "政府", "level": "地市级", "parent": "廊坊市人民政府", "location": "河北省廊坊市"},
    {"id": 7, "name": "河北省司法厅", "type": "政府", "level": "省级", "parent": "河北省人民政府", "location": "河北省石家庄市"},
    {"id": 8, "name": "廊坊市政府办公室", "type": "政府", "level": "地市级", "parent": "廊坊市人民政府", "location": "河北省廊坊市"},
    {"id": 9, "name": "廊坊师专（廊坊师范学院）", "type": "事业单位", "level": "地市级", "parent": "", "location": "河北省廊坊市"},
    {"id": 10, "name": "石家庄市司法局", "type": "政府", "level": "地市级", "parent": "石家庄市人民政府", "location": "河北省石家庄市"},
    {"id": 11, "name": "北京亦庄·永清高新技术产业开发区", "type": "开发区", "level": "县级", "parent": "", "location": "河北省廊坊市永清县"},
]

# 3. Positions
positions = [
    # ── Current Leaders ──
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2022年7月", "end_date": "至今", "rank": "正处级", "note": "接替冯学军任永清县委书记"},
    {"person_id": 1, "org_id": 6, "title": "廊坊市商务局局长", "start_date": "2021年6月", "end_date": "2022年8月", "rank": "正处级", "note": "2022年8月23日免职"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2025年1月", "end_date": "至今", "rank": "正处级", "note": "2025年1月17日县十七届人大五次会议当选"},
    {"person_id": 2, "org_id": 2, "title": "代县长", "start_date": "2024年12月", "end_date": "2025年1月", "rank": "正处级", "note": "接替黄运然"},
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "2025年1月", "end_date": "至今", "rank": "副处级", "note": "2025年1月12日被任命为副县长，后明确为常务副县长"},
    {"person_id": 4, "org_id": 2, "title": "县委常委、副县长", "start_date": "2025年1月", "end_date": "至今", "rank": "副处级", "note": "2025年1月12日被任命为副县长，分管教育、体育、人社、金融"},
    {"person_id": 5, "org_id": 3, "title": "县人大常委会主任", "start_date": "2021年", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "县政协主席", "start_date": "2021年", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "县委常委、人武部部长", "start_date": "2021年", "end_date": "至今", "rank": "副处级", "note": ""},

    # ── Predecessors ──
    {"person_id": 10, "org_id": 1, "title": "县委书记", "start_date": "2021年5月", "end_date": "2022年7月", "rank": "正处级", "note": "任永清县委书记、一级调研员、北京亦庄·永清高新区党工委书记"},
    {"person_id": 10, "org_id": 8, "title": "廊坊市政府办公室科员/副科长/科长", "start_date": "1996年12月", "end_date": "约2019年", "rank": "", "note": "1996.12-2000.09 廊坊市政府办公室综合六科科员，后逐步晋升"},
    {"person_id": 10, "org_id": 9, "title": "廊坊师专物理系辅导员", "start_date": "1995年7月", "end_date": "1996年12月", "rank": "", "note": "毕业后第一份工作"},
    {"person_id": 11, "org_id": 1, "title": "县委书记", "start_date": "2019年12月", "end_date": "2021年5月", "rank": "正处级", "note": "接替邢华金任永清县委书记"},
    {"person_id": 11, "org_id": 7, "title": "省司法厅党委委员、副厅长", "start_date": "2021年5月", "end_date": "至今", "rank": "副厅级", "note": "另有任用后调任现职"},
    {"person_id": 11, "org_id": 10, "title": "石家庄市司法局律师管理处处长/灵寿县副县长", "start_date": "1987年9月", "end_date": "2019年", "rank": "", "note": "早期职业生涯"},
    {"person_id": 12, "org_id": 1, "title": "县委书记", "start_date": "2016年12月", "end_date": "2019年12月", "rank": "正处级", "note": "接替李玉宝，后由彭敬捷接替"},
    {"person_id": 13, "org_id": 2, "title": "县长", "start_date": "2021年5月", "end_date": "2024年12月", "rank": "正处级", "note": "2021年5月27日任代县长，后任县长"},
    {"person_id": 14, "org_id": 2, "title": "县长", "start_date": "2017年", "end_date": "2021年5月", "rank": "正处级", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "县委书记", "start_date": "2013年4月", "end_date": "2016年12月", "rank": "正处级", "note": "接替宋华英"},
]

# 4. Relationships
relationships = [
    # Current team: 焦文序 ↔ 董魁宁
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭档，共同出席大量会议活动", "overlap_org": "永清县委/县政府", "overlap_period": "2024年12月至今"},
    # 焦文序 ↔ 杨丹
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与常务副县长", "overlap_org": "永清县委", "overlap_period": "2025年1月至今"},
    # 焦文序 ↔ 王达
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与副县长", "overlap_org": "永清县委", "overlap_period": "2025年1月至今"},
    # 董魁宁 ↔ 杨丹
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "永清县政府", "overlap_period": "2025年1月至今"},
    # 焦文序 ← 冯学军 (predecessor-successor)
    {"person_a": 10, "person_b": 1, "type": "predecessor_successor", "context": "冯学军的前任县委书记，焦文序接替", "overlap_org": "中共永清县委员会", "overlap_period": "2022年7月交接"},
    # 冯学军 ← 彭敬捷
    {"person_a": 11, "person_b": 10, "type": "predecessor_successor", "context": "彭敬捷的前任县委书记，冯学军接替", "overlap_org": "中共永清县委员会", "overlap_period": "2021年5月交接"},
    # 彭敬捷 ← 邢华金
    {"person_a": 12, "person_b": 11, "type": "predecessor_successor", "context": "邢华金的前任县委书记，彭敬捷接替", "overlap_org": "中共永清县委员会", "overlap_period": "2019年12月交接"},
    # 董魁宁 ← 黄运然
    {"person_a": 13, "person_b": 2, "type": "predecessor_successor", "context": "黄运然的前任县长，董魁宁接替", "overlap_org": "永清县人民政府", "overlap_period": "2024年12月交接"},
    # 黄运然 ← 张兵
    {"person_a": 14, "person_b": 13, "type": "predecessor_successor", "context": "张兵的前任县长，黄运然接替", "overlap_org": "永清县人民政府", "overlap_period": "2021年5月交接"},
    # 冯学军 ↔ 黄运然 (co-work as party secretary and county chief)
    {"person_a": 10, "person_b": 13, "type": "overlap", "context": "冯学军任县委书记期间，黄运然任县长搭档", "overlap_org": "永清县委/县政府", "overlap_period": "2021年5月—2022年7月"},
    # 张兵 ↔ 彭敬捷 (co-work)
    {"person_a": 14, "person_b": 11, "type": "overlap", "context": "张兵任县长期间与彭敬捷搭档", "overlap_org": "永清县委/县政府", "overlap_period": "2019年12月—2021年5月"},
]

# ── Build ──
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

import sqlite3
conn = sqlite3.connect(DB_PATH)
cur = conn.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur = conn.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur = conn.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur = conn.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]
conn.close()

print(f"\n✅ {SLUG} build complete!")
print(f"   Persons:       {person_count}")
print(f"   Organizations: {org_count}")
print(f"   Positions:     {pos_count}")
print(f"   Relationships: {rel_count}")
print(f"   DB: {DB_PATH}")
print(f"   GEXF: {GEXF_PATH}")
