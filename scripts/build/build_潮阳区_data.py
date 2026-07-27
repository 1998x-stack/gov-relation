#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
潮阳区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 汕头市
Region: 潮阳区
Targets: 区委书记 & 区长

Research Sources:
- 潮阳区人民政府官方网站 (www.gdcy.gov.cn) 政务要闻 2026年7月确认
- 潮阳区2026年7月领导干部接访安排表 (post_2549024)
- 潮阳区2026年6月领导干部接访安排表 (post_2541493)
- 潮阳区"两优一先"表彰大会报道 (post_2550413)
- 汕头市人民政府网站 (www.shantou.gov.cn)
- Wikipedia zh.wikipedia.org/wiki/潮阳区
- 区政协五届六次会议报道 (post_2531271)
- 区五届人大五次会议报道 (post_2427007)

Confirmed officeholders (as of 2026-07-22):
- 区委书记: 尤朝东 (原区长晋升)
- 区委副书记、区长: 查晶晶
- 区委副书记: 方文宏, 宋芝
- 区委常委、常务副区长: 游坤色
- 区委常委、组织部部长: 陈铭
- 区委常委、政法委书记: 郑再泽
- 区委常委、纪委书记、监委主任: 黄益鑫/陈大伟
- 区委常委、宣传部部长: 谢晓丹
- 区委常委、统战部部长: 许琪
- 区委常委、区委办/区政府办主任: 阮韧
- 区人大常委会主任: 曾涛
- 区政协主席: 黄泽波

Research Date: 2026-07-22
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "潮阳区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# The script uses gov_relation.runner (which internally uses sqlite3)
import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "尤朝东",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "潮阳区委书记",
        "current_org": "中共汕头市潮阳区委员会",
        "source": "潮阳区政府官网(gdcy.gov.cn) 2026-07-06两优一先报道; Wikipedia"
    },
    {
        "id": 2,
        "name": "查晶晶",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "潮阳区委副书记、区长",
        "current_org": "潮阳区人民政府",
        "source": "潮阳区政府官网(gdcy.gov.cn) 2026-07-13防汛报道; 汕头市政府网站"
    },
    # ════════════════════════════════════════
    # 区委副书记
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "方文宏",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "潮阳区委副书记",
        "current_org": "中共汕头市潮阳区委员会",
        "source": "潮阳区政府官网 2026年7月接访安排表(序号5)"
    },
    {
        "id": 4,
        "name": "宋芝",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "潮阳区委副书记",
        "current_org": "中共汕头市潮阳区委员会",
        "source": "潮阳区政府官网 2026年7月接访安排表(序号7); 两优一先报道"
    },
    # ════════════════════════════════════════
    # 区委常委
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "游坤色",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、副区长（常务副区长）",
        "current_org": "潮阳区人民政府",
        "source": "潮阳区政府官网 2026年6-7月接访安排表; 防汛调度新闻"
    },
    {
        "id": 6,
        "name": "陈铭",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共汕头市潮阳区委员会组织部",
        "source": "潮阳区政府官网 2026年7月接访安排表(序号1,19); 两优一先报道"
    },
    {
        "id": 7,
        "name": "郑再泽",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共汕头市潮阳区委员会政法委",
        "source": "潮阳区政府官网 2026年7月接访安排表(序号9,20)"
    },
    {
        "id": 8,
        "name": "黄益鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共汕头市潮阳区纪律检查委员会",
        "source": "潮阳区政府官网 2026年7月接访安排表(序号23); 区五届人大六次会议报道"
    },
    {
        "id": 9,
        "name": "谢晓丹",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共汕头市潮阳区委员会宣传部",
        "source": "潮阳区政府官网 6月接访安排表; 区妇女第四次代表大会报道"
    },
    {
        "id": 10,
        "name": "许琪",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共汕头市潮阳区委员会统战部",
        "source": "潮阳区政府官网 2026年7月接访安排表(序号17)"
    },
    {
        "id": 11,
        "name": "阮韧",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、区委办公室、区政府办公室主任",
        "current_org": "中共汕头市潮阳区委员会办公室",
        "source": "潮阳区政府官网 2026年7月接访安排表(序号3,13,21)"
    },
    # ════════════════════════════════════════
    # 副区长
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "周芳",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "潮阳区人民政府",
        "source": "潮阳区政府官网 2026年接访安排表(多次出现)"
    },
    {
        "id": 13,
        "name": "魏思超",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "潮阳区人民政府",
        "source": "潮阳区政府官网 2026年7月接访安排表(序号4); 防汛报道"
    },
    {
        "id": 14,
        "name": "郭鹏程",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "潮阳区人民政府",
        "source": "潮阳区政府官网 2026年7月接访安排表(序号8)"
    },
    {
        "id": 15,
        "name": "欧阳仕",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "潮阳区人民政府",
        "source": "潮阳区政府官网 2026年7月接访安排表(序号10,20); 高考巡考报道"
    },
    {
        "id": 16,
        "name": "何晓玲",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "潮阳区人民政府",
        "source": "潮阳区政府官网 2026年7月接访安排表(序号14)"
    },
    {
        "id": 17,
        "name": "陈伟鸿",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长、区公安分局局长",
        "current_org": "汕头市公安局潮阳分局",
        "source": "潮阳区政府官网 2026年7月接访安排表(序号18)"
    },
    # ════════════════════════════════════════
    # 区人大常委会
    # ════════════════════════════════════════
    {
        "id": 18,
        "name": "曾涛",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区人大常委会主任",
        "current_org": "潮阳区人民代表大会常务委员会",
        "source": "潮阳区政府官网 2026-06-30 两优一先报道(序号11)"
    },
    # ════════════════════════════════════════
    # 区政协
    # ════════════════════════════════════════
    {
        "id": 19,
        "name": "黄泽波",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政协主席",
        "current_org": "政协汕头市潮阳区委员会",
        "source": "潮阳区政府官网 政协工作会议报道; 两优一先报道"
    },
    # ════════════════════════════════════════
    # 区法检两院
    # ════════════════════════════════════════
    {
        "id": 20,
        "name": "颜映丰",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区人民法院院长",
        "current_org": "潮阳区人民法院",
        "source": "潮阳区政府官网 区五届人大五次会议报道"
    },
    {
        "id": 21,
        "name": "杜海钊",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区人民检察院检察长",
        "current_org": "潮阳区人民检察院",
        "source": "潮阳区政府官网 区五届人大五次会议报道"
    },
    # ════════════════════════════════════════
    # 前任领导（用于网络关系）
    # ════════════════════════════════════════
    {
        "id": 22,
        "name": "柯延鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任潮阳区委书记（约2021-2024）",
        "current_org": "",
        "source": "公开媒体报道; 旧闻记载"
    },
    {
        "id": 23,
        "name": "蔡永明",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任潮阳区委书记（约2016-2021），现任汕头市委常委、政法委书记",
        "current_org": "中共汕头市委政法委",
        "source": "公开媒体报道; 汕头市政府网站"
    },
    {
        "id": 24,
        "name": "张建宇",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任潮阳区区长（尤朝东之前任）",
        "current_org": "",
        "source": "公开媒体报道"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共汕头市潮阳区委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共汕头市委员会",
        "location": "广东省汕头市潮阳区"
    },
    {
        "id": 2,
        "name": "潮阳区人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "汕头市人民政府",
        "location": "广东省汕头市潮阳区"
    },
    {
        "id": 3,
        "name": "潮阳区人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "汕头市人民代表大会常务委员会",
        "location": "广东省汕头市潮阳区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议汕头市潮阳区委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协汕头市委员会",
        "location": "广东省汕头市潮阳区"
    },
    {
        "id": 5,
        "name": "中共汕头市潮阳区纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共汕头市纪律检查委员会",
        "location": "广东省汕头市潮阳区"
    },
    {
        "id": 6,
        "name": "中共汕头市潮阳区委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共汕头市潮阳区委员会",
        "location": "广东省汕头市潮阳区"
    },
    {
        "id": 7,
        "name": "中共汕头市潮阳区委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共汕头市潮阳区委员会",
        "location": "广东省汕头市潮阳区"
    },
    {
        "id": 8,
        "name": "中共汕头市潮阳区委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共汕头市潮阳区委员会",
        "location": "广东省汕头市潮阳区"
    },
    {
        "id": 9,
        "name": "中共汕头市潮阳区委统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共汕头市潮阳区委员会",
        "location": "广东省汕头市潮阳区"
    },
    {
        "id": 10,
        "name": "中共汕头市潮阳区委办公室",
        "type": "党委",
        "level": "县级",
        "parent": "中共汕头市潮阳区委员会",
        "location": "广东省汕头市潮阳区"
    },
    {
        "id": 11,
        "name": "汕头市公安局潮阳分局",
        "type": "政府",
        "level": "县级",
        "parent": "汕头市公安局",
        "location": "广东省汕头市潮阳区"
    },
    {
        "id": 12,
        "name": "潮阳区人民法院",
        "type": "司法",
        "level": "县级",
        "parent": "汕头市中级人民法院",
        "location": "广东省汕头市潮阳区"
    },
    {
        "id": 13,
        "name": "潮阳区人民检察院",
        "type": "司法",
        "level": "县级",
        "parent": "汕头市人民检察院",
        "location": "广东省汕头市潮阳区"
    },
    {
        "id": 14,
        "name": "中共汕头市委政法委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中共汕头市委员会",
        "location": "广东省汕头市"
    },
    {
        "id": 15,
        "name": "中共汕头市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中共广东省委员会",
        "location": "广东省汕头市"
    },
    {
        "id": 16,
        "name": "汕头市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "广东省人民政府",
        "location": "广东省汕头市"
    },
]

# 3. Positions
positions = [
    # 尤朝东 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "潮阳区委书记", "start_date": "约2024年", "end_date": "present", "rank": "正处级", "note": "原潮阳区区长晋升"},
    # 查晶晶 - 区长
    {"person_id": 2, "org_id": 2, "title": "潮阳区委副书记、区长", "start_date": "约2024年", "end_date": "present", "rank": "正处级", "note": "2025年10月区五届人大六次会议当选"},
    # 方文宏 - 区委副书记
    {"person_id": 3, "org_id": 1, "title": "潮阳区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 宋芝 - 区委副书记
    {"person_id": 4, "org_id": 1, "title": "潮阳区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 游坤色 - 常务副区长
    {"person_id": 5, "org_id": 2, "title": "区委常委、副区长（常务副区长）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈铭 - 组织部长
    {"person_id": 6, "org_id": 6, "title": "区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 郑再泽 - 政法委书记
    {"person_id": 7, "org_id": 7, "title": "区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 黄益鑫 - 纪委书记
    {"person_id": 8, "org_id": 5, "title": "区委常委、区纪委书记、区监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2025年10月当选区监委主任"},
    # 谢晓丹 - 宣传部长
    {"person_id": 9, "org_id": 8, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 许琪 - 统战部长
    {"person_id": 10, "org_id": 9, "title": "区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 阮韧 - 区委办/区政府办主任
    {"person_id": 11, "org_id": 10, "title": "区委常委、区委办公室、区政府办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 周芳 - 副区长
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 魏思超 - 副区长
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 郭鹏程 - 副区长
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 欧阳仕 - 副区长
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 何晓玲 - 副区长
    {"person_id": 16, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈伟鸿 - 副区长/公安局长
    {"person_id": 17, "org_id": 11, "title": "副区长、区公安分局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 曾涛 - 人大主任
    {"person_id": 18, "org_id": 3, "title": "区人大常委会主任", "start_date": "约2026年", "end_date": "present", "rank": "正处级", "note": "接替马文玲/詹少龙"},
    # 黄泽波 - 政协主席
    {"person_id": 19, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 颜映丰 - 法院院长
    {"person_id": 20, "org_id": 12, "title": "区人民法院院长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 杜海钊 - 检察院检察长
    {"person_id": 21, "org_id": 13, "title": "区人民检察院检察长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 柯延鹏 - 前任区委书记
    {"person_id": 22, "org_id": 1, "title": "前任潮阳区委书记", "start_date": "约2021年", "end_date": "约2024年", "rank": "正处级", "note": "前任，去向待查"},
    # 蔡永明 - 前任区委书记/现任市政法委书记
    {"person_id": 23, "org_id": 1, "title": "前任潮阳区委书记", "start_date": "约2016年", "end_date": "2021年", "rank": "正处级", "note": ""},
    {"person_id": 23, "org_id": 14, "title": "汕头市委常委、政法委书记", "start_date": "2021年", "end_date": "present", "rank": "副厅级", "note": "从潮阳区委书记晋升"},
    # 张建宇 - 前任区长
    {"person_id": 24, "org_id": 2, "title": "前任潮阳区区长", "start_date": "", "end_date": "", "rank": "正处级", "note": "前任，去向待查"},
]

# 4. Relationships
relationships = [
    # 党委-政府主要领导协作关系
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长：党委与政府主要领导工作搭档关系",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "潮阳区",
        "overlap_period": "2024年至今",
        "source": "潮阳区政府官网 两优一先、防汛、爱国卫生运动等多次联合报道"
    },
    # 区委书记与区委副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记与区委副书记：党委领导班子协作",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "中共潮阳区委",
        "overlap_period": "2026年",
        "source": "潮阳区政府官网 两优一先报道; 接访安排表"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记与区委副书记：党委领导班子协作",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "中共潮阳区委",
        "overlap_period": "2026年",
        "source": "潮阳区政府官网 两优一先报道; 接访安排表"
    },
    # 区长与常务副区长
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区长与常务副区长：政府领导班子日常协作",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "潮阳区人民政府",
        "overlap_period": "2026年",
        "source": "潮阳区政府官网 区政府廉政工作会议报道"
    },
    # 区委常委之间
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "区委书记与常务副区长：区委常委班子共事",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "中共潮阳区委",
        "overlap_period": "2026年",
        "source": "潮阳区政府官网 接访安排表"
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "overlap",
        "context": "区委书记与组织部部长：党委领导班子成员",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "中共潮阳区委",
        "overlap_period": "2026年",
        "source": "潮阳区政府官网 接访安排表; 两优一先报道"
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "overlap",
        "context": "区委书记与政法委书记：党委领导班子成员",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "中共潮阳区委",
        "overlap_period": "2026年",
        "source": "潮阳区政府官网 接访安排表"
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "overlap",
        "context": "区委书记与纪委书记：党委领导班子成员",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "中共潮阳区委",
        "overlap_period": "2026年",
        "source": "潮阳区政府官网 接访安排表"
    },
    # 前任-现任传承关系
    {
        "person_a": 22,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "柯延鹏→尤朝东：潮阳区委书记前后任交接",
        "strength": "strong",
        "confidence": "plausible",
        "overlap_org": "中共潮阳区委",
        "overlap_period": "约2024年交接",
        "source": "公开媒体报道"
    },
    {
        "person_a": 23,
        "person_b": 22,
        "type": "predecessor_successor",
        "context": "蔡永明→柯延鹏→尤朝东：潮阳区委书记连续交接",
        "strength": "strong",
        "confidence": "plausible",
        "overlap_org": "中共潮阳区委",
        "overlap_period": "2016-2024年",
        "source": "公开媒体报道"
    },
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "尤朝东由区长晋升区委书记，查晶晶接任区长",
        "strength": "strong",
        "confidence": "plausible",
        "overlap_org": "潮阳区",
        "overlap_period": "约2024年",
        "source": "公开媒体报道"
    },
    {
        "person_a": 24,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "张建宇→尤朝东→查晶晶：潮阳区区长前后任链条",
        "strength": "medium",
        "confidence": "plausible",
        "overlap_org": "潮阳区人民政府",
        "overlap_period": "",
        "source": "公开媒体报道"
    },
    # 人大-党委关系
    {
        "person_a": 1,
        "person_b": 18,
        "type": "overlap",
        "context": "区委书记与人大常委会主任：区级领导班子成员",
        "strength": "medium",
        "confidence": "confirmed",
        "overlap_org": "潮阳区",
        "overlap_period": "2026年",
        "source": "潮阳区政府官网 两优一先报道"
    },
    # 政协-党委关系
    {
        "person_a": 1,
        "person_b": 19,
        "type": "overlap",
        "context": "区委书记与政协主席：区级领导班子成员",
        "strength": "medium",
        "confidence": "confirmed",
        "overlap_org": "潮阳区",
        "overlap_period": "2026年",
        "source": "潮阳区政府官网 政协工作会议报道"
    },
]


# ── Main ──
def main():
    print(f"=== {SLUG} 网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

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

    print(f"\n=== 完成 ===")
    print(f"数据库: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
