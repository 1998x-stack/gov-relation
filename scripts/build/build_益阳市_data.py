#!/usr/bin/env python3
"""
益阳市领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Yiyang City leadership network.
Investigation date: 2026-07-24

Current leadership (as of 2026-05-16):
  市委书记: 向世聪 (from 湖南省统计局)
  市长: 刘勇会 (acting mayor from 2026-04, previously 安化县委书记/副市长)
  Predecessor 书记: 陈竞 (now 长沙市委书记、省委常委)
  Predecessor 市长: 熊炜 (now 省政府副秘书长)
"""

import sqlite3
import os
import sys

# ── Paths (relative to repo root) ──
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DB_PATH = os.path.join(REPO_ROOT, "data", "database", "益阳市_network.db")
GEXF_PATH = os.path.join(REPO_ROOT, "data", "graph", "益阳市_network.gexf")

# ═══════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════

PERSONS = [
    # ─── Top Leaders ───
    {
        "id": 1,
        "name": "向世聪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-12",
        "birthplace": "湖南省隆回县",
        "education": "在职研究生，管理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共益阳市委书记",
        "current_org": "中共益阳市委",
        "source": "中国经济网 http://district.ce.cn/newarea/sddy/202605/t20260516_2970838.shtml",
    },
    {
        "id": 2,
        "name": "刘勇会",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-05",
        "birthplace": "湖南省永州市",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共益阳市委副书记、市人民政府代市长",
        "current_org": "益阳市人民政府",
        "source": "维基百科 https://zh.wikipedia.org/wiki/%E5%88%98%E5%8B%87%E4%BC%9A · 中国经济网",
    },
    # ─── Predecessors ───
    {
        "id": 3,
        "name": "陈竞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-02",
        "birthplace": "湖南省长沙市",
        "education": "大学学历，公共管理硕士（省委党校）",
        "party_join": "1993-12",
        "work_start": "1990-07",
        "current_post": "湖南省副省长、长沙市委书记、省委常委",
        "current_org": "中共长沙市委",
        "source": "维基百科 https://zh.wikipedia.org/wiki/%E9%99%88%E7%AB%9E_(1971%E5%B9%B4)",
    },
    {
        "id": 4,
        "name": "熊炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湖南省人民政府副秘书长",
        "current_org": "湖南省人民政府",
        "source": "中国经济网",
    },
    # ─── City Leadership Roster ───
    {
        "id": 5,
        "name": "邓斌",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共益阳市委副书记、统战部部长",
        "current_org": "中共益阳市委",
        "source": "维基百科",
    },
    {
        "id": 6,
        "name": "刘泽友",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-11",
        "birthplace": "湖南省新邵县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "益阳市人大常委会主任",
        "current_org": "益阳市人大常委会",
        "source": "中国经济网",
    },
    {
        "id": 7,
        "name": "胡立安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-04",
        "birthplace": "湖南省安化县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "益阳市政协主席",
        "current_org": "益阳市政协",
        "source": "维基百科",
    },
    # ─── District/County Leaders ───
    {
        "id": 8,
        "name": "付振南",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共资阳区委书记",
        "current_org": "中共益阳市资阳区委员会",
        "source": "维基百科 · 资阳区政府网站",
    },
    {
        "id": 9,
        "name": "黄瑛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资阳区区长",
        "current_org": "资阳区人民政府",
        "source": "维基百科 · 资阳区政府网站",
    },
    {
        "id": 10,
        "name": "李丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共赫山区委书记、区长",
        "current_org": "中共益阳市赫山区委员会",
        "source": "百度百科",
    },
    {
        "id": 11,
        "name": "钟剑波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共南县委书记、县人民政府县长",
        "current_org": "中共南县委员会",
        "source": "维基百科",
    },
    {
        "id": 12,
        "name": "向荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "湖南省沅江市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共桃江县委书记",
        "current_org": "中共桃江县委员会",
        "source": "维基百科",
    },
    {
        "id": 13,
        "name": "周登高",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-09",
        "birthplace": "湖南省宁乡市",
        "education": "湘潭大学行政管理专业硕士",
        "party_join": "中共党员",
        "work_start": "2000",
        "current_post": "桃江县人民政府县长",
        "current_org": "桃江县人民政府",
        "source": "维基百科 https://zh.wikipedia.org/wiki/%E5%91%A8%E7%99%BB%E9%AB%98",
    },
    {
        "id": 14,
        "name": "石录明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-10",
        "birthplace": "湖南省益阳市资阳区",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共安化县委书记",
        "current_org": "中共安化县委员会",
        "source": "维基百科",
    },
    {
        "id": 15,
        "name": "潘文剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-07",
        "birthplace": "湖南省南县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "安化县人民政府县长",
        "current_org": "安化县人民政府",
        "source": "维基百科",
    },
    {
        "id": 16,
        "name": "杨智勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-11",
        "birthplace": "湖南省宁乡市",
        "education": "湖南师范大学历史学博士",
        "party_join": "中共党员",
        "work_start": "1997",
        "current_post": "中共沅江市委书记",
        "current_org": "中共沅江市委员会",
        "source": "维基百科 https://zh.wikipedia.org/wiki/%E6%9D%A8%E6%99%BA%E5%8B%87",
    },
    {
        "id": 17,
        "name": "罗必胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-04",
        "birthplace": "湖南省安化县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沅江市人民政府市长",
        "current_org": "沅江市人民政府",
        "source": "维基百科",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共益阳市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "湖南省益阳市"},
    {"id": 2, "name": "益阳市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "湖南省益阳市"},
    {"id": 3, "name": "益阳市人大常委会", "type": "人大", "level": "地市级", "parent": "湖南省人大常委会", "location": "湖南省益阳市"},
    {"id": 4, "name": "益阳市政协", "type": "政协", "level": "地市级", "parent": "湖南省政协", "location": "湖南省益阳市"},
    {"id": 5, "name": "中共益阳市资阳区委员会", "type": "党委", "level": "县处级", "parent": "中共益阳市委", "location": "湖南省益阳市资阳区"},
    {"id": 6, "name": "资阳区人民政府", "type": "政府", "level": "县处级", "parent": "益阳市人民政府", "location": "湖南省益阳市资阳区"},
    {"id": 7, "name": "中共益阳市赫山区委员会", "type": "党委", "level": "县处级", "parent": "中共益阳市委", "location": "湖南省益阳市赫山区"},
    {"id": 8, "name": "赫山区人民政府", "type": "政府", "level": "县处级", "parent": "益阳市人民政府", "location": "湖南省益阳市赫山区"},
    {"id": 9, "name": "中共南县委员会", "type": "党委", "level": "县处级", "parent": "中共益阳市委", "location": "湖南省益阳市南县"},
    {"id": 10, "name": "南县人民政府", "type": "政府", "level": "县处级", "parent": "益阳市人民政府", "location": "湖南省益阳市南县"},
    {"id": 11, "name": "中共桃江县委员会", "type": "党委", "level": "县处级", "parent": "中共益阳市委", "location": "湖南省益阳市桃江县"},
    {"id": 12, "name": "桃江县人民政府", "type": "政府", "level": "县处级", "parent": "益阳市人民政府", "location": "湖南省益阳市桃江县"},
    {"id": 13, "name": "中共安化县委员会", "type": "党委", "level": "县处级", "parent": "中共益阳市委", "location": "湖南省益阳市安化县"},
    {"id": 14, "name": "安化县人民政府", "type": "政府", "level": "县处级", "parent": "益阳市人民政府", "location": "湖南省益阳市安化县"},
    {"id": 15, "name": "中共沅江市委员会", "type": "党委", "level": "县处级", "parent": "中共益阳市委", "location": "湖南省益阳市沅江市"},
    {"id": 16, "name": "沅江市人民政府", "type": "政府", "level": "县处级", "parent": "益阳市人民政府", "location": "湖南省益阳市沅江市"},
    {"id": 17, "name": "中共长沙市委", "type": "党委", "level": "副省级", "parent": "中共湖南省委", "location": "湖南省长沙市"},
    {"id": 18, "name": "湖南省统计局", "type": "政府", "level": "厅局级", "parent": "湖南省人民政府", "location": "湖南省长沙市"},
    {"id": 19, "name": "湖南省人民政府", "type": "政府", "level": "省部级", "parent": "", "location": "湖南省长沙市"},
    {"id": 20, "name": "中共安化县委员会（历史）", "type": "党委", "level": "县处级", "parent": "", "location": "湖南省益阳市安化县"},
    {"id": 21, "name": "中共道县委员会", "type": "党委", "level": "县处级", "parent": "中共永州市委", "location": "湖南省永州市道县"},
]

POSITIONS = [
    # ─── 向世聪 ───
    {"person_id": 1, "org_id": 18, "title": "湖南省统计局党组书记、局长", "start": "", "end": "2026-05", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "中共益阳市委书记", "start": "2026-05-16", "end": "", "rank": "正厅级", "note": "现任"},

    # ─── 刘勇会 ───
    {"person_id": 2, "org_id": 21, "title": "中共道县委副书记、县长", "start": "", "end": "2016-07", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 21, "title": "中共道县委书记", "start": "2016-08", "end": "2019-03", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 13, "title": "中共安化县委书记", "start": "2019-04", "end": "2021-10", "rank": "正处级", "note": "获评2021年全国优秀县委书记"},
    {"person_id": 2, "org_id": 1, "title": "中共益阳市委常委", "start": "2021-10", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "益阳市人民政府副市长", "start": "2022-01", "end": "2026-04", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "中共益阳市委副书记", "start": "2026-04", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "益阳市人民政府代市长", "start": "2026-04", "end": "", "rank": "正厅级", "note": "现任"},

    # ─── 陈竞 ───
    {"person_id": 3, "org_id": 19, "title": "长沙市节约用水办公室干部", "start": "1990", "end": "1994", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 19, "title": "中国建设银行长沙市分行", "start": "1994", "end": "1995", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 19, "title": "共青团湖南省委（历任职员至部长）", "start": "1995", "end": "2007", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 19, "title": "中共张家界市永定区委副书记、代区长→区长", "start": "2007-02", "end": "2011-12", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 19, "title": "中共慈利县委书记", "start": "2011-12", "end": "2013-12", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 19, "title": "中共衡阳市石鼓区委书记", "start": "2013-12", "end": "2015-02", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 19, "title": "衡阳市人民政府副市长", "start": "2015-02", "end": "2016-09", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 19, "title": "中共衡阳市委常委、组织部部长", "start": "2016-09", "end": "2019-10", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 19, "title": "湖南省委组织部副部长、省公务员局局长（兼）", "start": "2019-10", "end": "2021-07", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "益阳市人民政府市长", "start": "2021-08", "end": "2023-02", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "中共益阳市委书记", "start": "2023-02", "end": "2026-05", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 19, "title": "湖南省副省长（兼益阳书记至2026.05）", "start": "2025-07", "end": "", "rank": "副部级", "note": ""},
    {"person_id": 3, "org_id": 17, "title": "中共长沙市委书记、省委常委", "start": "2026-06", "end": "", "rank": "副部级", "note": "现任"},

    # ─── 熊炜 ───
    {"person_id": 4, "org_id": 2, "title": "益阳市人民政府市长", "start": "2023-02", "end": "2026-04", "rank": "正厅级", "note": "辞职调任"},
    {"person_id": 4, "org_id": 19, "title": "湖南省人民政府副秘书长", "start": "2026-04", "end": "", "rank": "正厅级", "note": "现任"},

    # ─── 邓斌 ───
    {"person_id": 5, "org_id": 1, "title": "中共益阳市委副书记、统战部长", "start": "", "end": "", "rank": "副厅级", "note": ""},

    # ─── 刘泽友 ───
    {"person_id": 6, "org_id": 3, "title": "益阳市人大常委会主任", "start": "2024-12", "end": "", "rank": "正厅级", "note": ""},

    # ─── 胡立安 ───
    {"person_id": 7, "org_id": 4, "title": "益阳市政协主席", "start": "2022-01", "end": "", "rank": "正厅级", "note": ""},

    # ─── 付振南 ───
    {"person_id": 8, "org_id": 5, "title": "中共资阳区委书记", "start": "", "end": "", "rank": "正处级", "note": ""},

    # ─── 黄瑛 ───
    {"person_id": 9, "org_id": 6, "title": "资阳区区长", "start": "", "end": "", "rank": "正处级", "note": ""},

    # ─── 李丰 ───
    {"person_id": 10, "org_id": 7, "title": "中共赫山区委书记、区长", "start": "", "end": "", "rank": "正处级", "note": ""},

    # ─── 钟剑波 ───
    {"person_id": 11, "org_id": 9, "title": "中共南县委书记、县长", "start": "", "end": "", "rank": "正处级", "note": "2021.10任县长，2025.02兼任书记"},

    # ─── 向荣 ───
    {"person_id": 12, "org_id": 11, "title": "中共桃江县委书记", "start": "", "end": "", "rank": "正处级", "note": ""},

    # ─── 周登高 ───
    {"person_id": 13, "org_id": 19, "title": "道林镇中心学校教师", "start": "2000", "end": "2005", "rank": "", "note": ""},
    {"person_id": 13, "org_id": 19, "title": "湘潭大学行政管理专业硕士", "start": "2005", "end": "2008", "rank": "", "note": "全日制学习"},
    {"person_id": 13, "org_id": 19, "title": "益阳市龙岭工业园管委会党政综合办公室主任", "start": "2008", "end": "2009", "rank": "", "note": ""},
    {"person_id": 13, "org_id": 19, "title": "益阳市沧水铺镇循环经济工业园管委会办公室主任", "start": "2009", "end": "2010-03", "rank": "", "note": ""},
    {"person_id": 13, "org_id": 7, "title": "赫山区委办公室调研室主任", "start": "2010-03", "end": "2010-10", "rank": "", "note": ""},
    {"person_id": 13, "org_id": 19, "title": "桃江县经济合作局党组副书记/局长", "start": "2010-10", "end": "2012-09", "rank": "", "note": ""},
    {"person_id": 13, "org_id": 20, "title": "安化县人民政府副县长", "start": "2012-11", "end": "2016-08", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "益阳市委办公室副主任", "start": "2016-08", "end": "2017-05", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "益阳市委副秘书长", "start": "2017-05", "end": "2020-04", "rank": "正处级", "note": ""},
    {"person_id": 13, "org_id": 20, "title": "中共安化县委副书记", "start": "2020-04", "end": "2021-07", "rank": "正处级", "note": ""},
    {"person_id": 13, "org_id": 12, "title": "桃江县人民政府县长", "start": "2021-07", "end": "", "rank": "正处级", "note": "现任"},

    # ─── 石录明 ───
    {"person_id": 14, "org_id": 13, "title": "中共安化县委书记", "start": "", "end": "", "rank": "正处级", "note": ""},

    # ─── 潘文剑 ───
    {"person_id": 15, "org_id": 14, "title": "安化县人民政府县长", "start": "", "end": "", "rank": "正处级", "note": ""},

    # ─── 杨智勇 ───
    {"person_id": 16, "org_id": 19, "title": "湖南师范大学留校工作", "start": "1997", "end": "2016", "rank": "", "note": "获历史学硕士、博士学位"},
    {"person_id": 16, "org_id": 5, "title": "中共资阳区委副书记", "start": "2016-08", "end": "2017-05", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 15, "title": "中共沅江市委副书记、市长→书记", "start": "2017-05", "end": "", "rank": "正处级", "note": "2017.08 代市长，2017.12 市长，2021.07 书记"},

    # ─── 罗必胜 ───
    {"person_id": 17, "org_id": 16, "title": "沅江市人民政府市长", "start": "", "end": "", "rank": "正处级", "note": ""},
]

RELATIONSHIPS = [
    # 陈竞 ↔ 刘勇会（直接上下级约5年）
    {"person_a": 3, "person_b": 2, "type": "superior_subordinate", "context": "陈竞任益阳市委书记期间刘勇会先后任市委常委、副市长、副书记、代市长，直接上下级关系", "overlap_org": "中共益阳市委/益阳市人民政府", "overlap_period": "2021-2026"},

    # 陈竞 ↔ 熊炜（书记-市长搭档）
    {"person_a": 3, "person_b": 4, "type": "superior_subordinate", "context": "陈竞任书记、熊炜任市长期间搭档约2年（2023.02-2024.04）", "overlap_org": "中共益阳市委/益阳市人民政府", "overlap_period": "2023-2024"},

    # 刘勇会 ↔ 石录明（前后任安化县委书记）
    {"person_a": 2, "person_b": 14, "type": "predecessor_successor", "context": "刘勇会2019-2021任安化县委书记，石录明后接任", "overlap_org": "中共安化县委员会", "overlap_period": "2019-2021"},

    # 刘勇会 ↔ 杨智勇（市级班子成员）
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "刘勇会任市委常委/副市长/代市长期间与沅江市委书记杨智勇在益阳市级层面共事", "overlap_org": "益阳市", "overlap_period": "2021-至今"},

    # 周登高 ↔ 安化县（曾任副县长、副书记共7年以上）
    {"person_a": 13, "person_b": 14, "type": "overlap", "context": "周登高任安化县副县长期间后与石录明同县工作", "overlap_org": "安化县", "overlap_period": "2012-2016"},

    # 杨智勇 ↔ 资阳区（曾任区委副书记）
    {"person_a": 16, "person_b": 8, "type": "overlap", "context": "杨智勇曾在资阳区委任副书记（2016-2017），付振南现任资阳区委书记", "overlap_org": "中共资阳区委员会", "overlap_period": "2016-2017"},

    # 周振宇（常德市长）↔ 益阳市（在益阳15年经历） — 跨市连接
    # 陈竞 ↔ 长沙（陈竞现为长沙书记，前益阳书记）
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "陈竞2023.02-2026.05任益阳市委书记，向世聪2026.05接任", "overlap_org": "中共益阳市委", "overlap_period": "2026-05"},

    # 向世聪 ↔ 省统计局（前任职务）
    # 周登高 ↔ 刘勇会（均历任安化县）
    {"person_a": 13, "person_b": 2, "type": "overlap", "context": "周登高任安化副县长+副书记期间，与刘勇会（安化县委书记2019-2021）先后共事", "overlap_org": "安化县", "overlap_period": "2020-2021"},
]

# ═══════════════════════════════════════════════════════════
# DATABASE BUILD
# ═══════════════════════════════════════════════════════════

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    # Drop existing tables
    for t in ["relationships", "positions", "organizations", "persons"]:
        conn.execute(f"DROP TABLE IF EXISTS {t}")

    conn.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        )
    """)
    conn.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    conn.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    conn.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace",
              "education", "party_join", "work_start", "current_post", "current_org", "source"]
    for p in PERSONS:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in ORGANIZATIONS:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in POSITIONS:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in RELATIONSHIPS:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ═══════════════════════════════════════════════════════════
# GEXF BUILD
# ═══════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(title):
    """Return 'r,g,b' string based on role."""
    t = title
    if "书记" in t and "副" not in t:
        return "200,30,30"
    if "市长" in t or "区长" in t or "县长" in t:
        if "副" in t:
            return "100,150,220"
        return "30,100,200"
    if "副书记" in t:
        return "220,80,80"
    if "主任" in t or "主席" in t:
        return "60,180,60"
    if "副" in t:
        return "100,150,220"
    return "180,180,180"

def is_top_leader(name):
    return name in ["向世聪", "刘勇会"]

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")

def generate_gexf():
    from datetime import datetime
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>益阳市领导班子工作关系网络 — 含市领导及区县党政正职</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        c = person_color(p["current_post"])
        sz = "60.0" if is_top_leader(p["name"]) else "35.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        cr, cg, cb = c.split(",")
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in ORGANIZATIONS:
        c = org_color(o["type"])
        cr, cg, cb = c.split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>')
        lines.append('        <viz:size value="20.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    added_edges = set()
    for pos in POSITIONS:
        pid = pos["person_id"]
        oid = pos["org_id"]
        eid += 1
        edge_key = f"p{pid}-o{oid}-{pos['title']}"
        if edge_key in added_edges:
            continue
        added_edges.add(edge_key)
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["start"])}—{esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")


def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  益阳市领导班子工作关系网络 — 数据构建")
    print("  调查日期: 2026-07-24")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()
    print("Done.")
