#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 南乐县 leadership network.

调查日期: 2026-08-05
信息来源: 南乐县人民政府网站 (nanle.gov.cn), 濮阳市人民政府网站 (puyang.gov.cn)
调查级别: 县
目标: 县委书记 & 县长
"""

import json
import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "南乐县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "南乐县_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"
SLUG = "河南省濮阳市南乐县"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 县委领导 (Party Committee)
    # ═══════════════════════════════

    # 梅兴秦 — 县委书记
    {
        "id": 1,
        "name": "梅兴秦",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共南乐县委书记",
        "current_org": "中共南乐县委员会",
        "source": "http://www.nanle.gov.cn/content/2026/1287250.html",
    },
    # 周笃铭 — 县委副书记、县长
    {
        "id": 2,
        "name": "周笃铭",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县人民政府县长",
        "current_org": "南乐县人民政府",
        "source": "http://www.nanle.gov.cn/content/2026/1315177.html",
    },
    # 孙丽君 — 县委副书记
    {
        "id": 3,
        "name": "孙丽君",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共南乐县委副书记",
        "current_org": "中共南乐县委员会",
        "source": "http://www.nanle.gov.cn/content/2026/1287250.html",
    },
    # 谢海萌 — 县委常委、组织部部长
    {
        "id": 4,
        "name": "谢海萌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县委常委、县委组织部部长",
        "current_org": "中共南乐县委员会",
        "source": "http://www.nanle.gov.cn/content/2026/1291208.html",
    },
    # 弓晓飞 — 县委常委
    {
        "id": 5,
        "name": "弓晓飞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县委常委",
        "current_org": "中共南乐县委员会",
        "source": "http://www.nanle.gov.cn/content/2026/1287250.html",
    },
    # 徐娅 — 县委常委
    {
        "id": 6,
        "name": "徐娅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县委常委",
        "current_org": "中共南乐县委员会",
        "source": "http://www.nanle.gov.cn/content/2026/1287250.html",
    },
    # 张钤 — 县委常委
    {
        "id": 7,
        "name": "张钤",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县委常委",
        "current_org": "中共南乐县委员会",
        "source": "http://www.nanle.gov.cn/content/2026/1287250.html",
    },
    # 王昊 — 县委常委
    {
        "id": 8,
        "name": "王昊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县委常委",
        "current_org": "中共南乐县委员会",
        "source": "http://www.nanle.gov.cn/content/2026/1287250.html",
    },
    # 李扬 — 县委常委
    {
        "id": 9,
        "name": "李扬",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县委常委",
        "current_org": "中共南乐县委员会",
        "source": "http://www.nanle.gov.cn/content/2026/1287250.html",
    },
    # 杨二卫 — 县委常委
    {
        "id": 10,
        "name": "杨二卫",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县委常委",
        "current_org": "中共南乐县委员会",
        "source": "http://www.nanle.gov.cn/content/2026/1287250.html",
    },
    # ═══════════════════════════════
    # 人大常委会 (People's Congress)
    # ═══════════════════════════════
    # 孙思群 — 县人大常委会主任
    {
        "id": 11,
        "name": "孙思群",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县人大常委会主任",
        "current_org": "南乐县人民代表大会常务委员会",
        "source": "http://www.nanle.gov.cn/content/2026/1291208.html",
    },
    # ═══════════════════════════════
    # 县人民政府 (County Government)
    # ═══════════════════════════════
    # 王坤 — 县领导（副县长级）
    {
        "id": 12,
        "name": "王坤",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县领导",
        "current_org": "南乐县人民政府",
        "source": "http://www.nanle.gov.cn/content/2026/1316148.html",
    },
    # 闫茂俭 — 县领导
    {
        "id": 13,
        "name": "闫茂俭",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县领导",
        "current_org": "南乐县人民政府",
        "source": "http://www.nanle.gov.cn/content/2026/1315177.html",
    },
    # 靳卫军 — 县领导
    {
        "id": 14,
        "name": "靳卫军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县领导",
        "current_org": "南乐县人民政府",
        "source": "http://www.nanle.gov.cn/content/2026/1316148.html",
    },
    # 史朝斌 — 县领导
    {
        "id": 15,
        "name": "史朝斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县领导",
        "current_org": "南乐县人民政府",
        "source": "http://www.nanle.gov.cn/content/2026/1315177.html",
    },
    # 夏云强 — 县领导
    {
        "id": 16,
        "name": "夏云强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县领导",
        "current_org": "南乐县人民政府",
        "source": "http://www.nanle.gov.cn/content/2026/1315177.html",
    },
    # 王振武 — 县领导
    {
        "id": 17,
        "name": "王振武",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县领导",
        "current_org": "南乐县人民政府",
        "source": "http://www.nanle.gov.cn/content/2026/1315177.html",
    },
    # 邢晓伟 — 县领导
    {
        "id": 18,
        "name": "邢晓伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县领导",
        "current_org": "南乐县人民政府",
        "source": "http://www.nanle.gov.cn/content/2026/1315177.html",
    },
    # 郭专政 — 县领导
    {
        "id": 19,
        "name": "郭专政",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县领导",
        "current_org": "南乐县人民政府",
        "source": "http://www.nanle.gov.cn/content/2026/1316148.html",
    },
    # 师啸宇 — 县领导
    {
        "id": 20,
        "name": "师啸宇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县领导",
        "current_org": "南乐县人民政府",
        "source": "http://www.nanle.gov.cn/content/2026/1316148.html",
    },
    # 张进良 — 县领导
    {
        "id": 21,
        "name": "张进良",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南乐县领导",
        "current_org": "南乐县人民政府",
        "source": "http://www.nanle.gov.cn/content/2026/1316148.html",
    },
    # ═══════════════════════════════
    # 历史人物 / 前任接任链
    # ═══════════════════════════════
    # 刘冰 — 前任县委书记（2018-2021, 现已调任南阳市长）
    {
        "id": 101,
        "name": "刘冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南阳市人民政府市长（前任南乐县委书记）",
        "current_org": "南阳市人民政府",
        "source": "data/persons/20260724-河南省-南阳市-市长-刘冰.json",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共南乐县委员会", "type": "党委", "level": "县级", "parent": "中共濮阳市委员会", "location": "河南省濮阳市南乐县"},
    {"id": 2, "name": "南乐县人民政府", "type": "政府", "level": "县级", "parent": "濮阳市人民政府", "location": "河南省濮阳市南乐县"},
    {"id": 3, "name": "南乐县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "南乐县", "location": "河南省濮阳市南乐县"},
    {"id": 4, "name": "中共华龙区委员会", "type": "党委", "level": "县级", "parent": "中共濮阳市委员会", "location": "河南省濮阳市华龙区"},
    {"id": 5, "name": "华龙区人民政府", "type": "政府", "level": "县级", "parent": "濮阳市人民政府", "location": "河南省濮阳市华龙区"},
    {"id": 6, "name": "中共濮阳市委员会", "type": "党委", "level": "地市级", "parent": "中共河南省委", "location": "河南省濮阳市"},
    {"id": 7, "name": "濮阳市人民政府", "type": "政府", "level": "地市级", "parent": "河南省人民政府", "location": "河南省濮阳市"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 梅兴秦
    {"person_id": 1, "org_id": 1, "title": "中共南乐县委书记",
     "start_date": "2026-06", "end_date": "", "rank": "正处级",
     "note": "主持中共南乐县委全面工作；南乐县第十四次党代会召开后任十四届县委书记；为县第一总河长"},
    {"person_id": 1, "org_id": 5, "title": "华龙区区长（前任职务）",
     "start_date": "未知", "end_date": "2026", "rank": "正处级",
     "note": "曾任濮阳市华龙区区长，2026年4月仍在任；后调任南乐县委书记"},
    # 周笃铭
    {"person_id": 2, "org_id": 2, "title": "南乐县人民政府县长",
     "start_date": "2026-07", "end_date": "", "rank": "正处级",
     "note": "县委副书记、县政府党组书记、县长；主持县政府全面工作。十六届人大七次会议确认（2026-07）"},
    {"person_id": 2, "org_id": 1, "title": "南乐县委副书记",
     "start_date": "2026-06", "end_date": "", "rank": "正处级",
     "note": "兼任县政府党组书记"},
    # 孙丽君
    {"person_id": 3, "org_id": 1, "title": "南乐县委副书记",
     "start_date": "2026-06", "end_date": "", "rank": "副处级", "note": "专职县委副书记"},
    # 谢海萌
    {"person_id": 4, "org_id": 1, "title": "南乐县委常委、县委组织部部长",
     "start_date": "2026-06", "end_date": "", "rank": "副处级", "note": "兼任县委组织部部长"},
    # 常委
    {"person_id": 5, "org_id": 1, "title": "南乐县委常委", "start_date": "2026-06", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "南乐县委常委", "start_date": "2026-06", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "南乐县委常委", "start_date": "2026-06", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "南乐县委常委", "start_date": "2026-06", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "南乐县委常委", "start_date": "2026-06", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "南乐县委常委", "start_date": "2026-06", "end_date": "", "rank": "副处级", "note": ""},
    # 孙思群
    {"person_id": 11, "org_id": 3, "title": "南乐县人大常委会主任",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "十六届人大七次会议主席团执行主席；常委会议定列席人员"},
    {"person_id": 11, "org_id": 4, "title": "南乐县领导（历任）", "start_date": "", "end_date": "", "rank": "", "note": "列席县委常委会"},
    # 县领导
    {"person_id": 12, "org_id": 2, "title": "南乐县领导（副县长级）", "start_date": "", "end_date": "", "rank": "副处级", "note": "参加县长调研活动"},
    {"person_id": 13, "org_id": 2, "title": "南乐县领导", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "南乐县领导", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "南乐县领导", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "南乐县领导", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "南乐县领导", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "南乐县领导", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "南乐县领导", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "南乐县领导", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "南乐县领导", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 刘冰
    {"person_id": 101, "org_id": 1, "title": "中共南乐县委书记（前任）",
     "start_date": "2018-11", "end_date": "2022-08", "rank": "正处级",
     "note": "前任南乐县委书记；2021-09升任濮阳市委常委仍兼南乐县委书记至2022-08"},
    {"person_id": 101, "org_id": 2, "title": "南乐县人民政府县长（前任）",
     "start_date": "2016-04", "end_date": "2018-11", "rank": "正处级",
     "note": "时任南乐县长"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 县委领导班子内部
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长——党政主要领导搭档；梅兴秦主持县委常委会，周笃铭主持县政府工作",
     "overlap_org": "中共南乐县委员会 / 南乐县人民政府", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "县委书记与专职县委副书记孙丽君——十四届县委常委会共事",
     "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "县委书记与组织部长谢海萌——县委常委会共事；谢海萌负责干部人事工作",
     "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今"},
    # 县委常委会成员互相
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "副书记用法与孙丽君——县委副书记之间共事",
     "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "县长与组织部长谢海萌——县委常委会共事",
     "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "专职副书记与组织部长——干部人事工作配合",
     "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今"},
    # 常委内部
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "县委常委会班子成员", "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "县委常委会班子成员", "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "县委常委会班子成员", "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 6, "person_b": 8, "type": "overlap", "context": "县委常委会班子成员", "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 7, "person_b": 9, "type": "overlap", "context": "县委常委会班子成员", "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 8, "person_b": 10, "type": "overlap", "context": "县委常委会班子成员", "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今"},
    # 人大
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "县委书记与人大会会主任——列席县委常委会，孙思群为县人大主任",
     "overlap_org": "南乐县", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 11, "type": "overlap",
     "context": "县长与人太主任——政府向人大报告工作关系；人大会议选举确认县长人选",
     "overlap_org": "南乐县人大常委会 / 南乐县人民政府", "overlap_period": "2026"},
    # 县政府班子
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县长与县领导王坤——县政府班子，王坤参加调研", "overlap_org": "南乐县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县长与县领导委卫军——县政府班子", "overlap_org": "南乐县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 19, "type": "overlap", "context": "县长与郭专政——县政府班子", "overlap_org": "南乐县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 20, "type": "overlap", "context": "县长与师啸宇——县政府班子", "overlap_org": "南乐县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 21, "type": "overlap", "context": "县长与张进良——县政府班子", "overlap_org": "南乐县人民政府", "overlap_period": "2026"},
    # 前任（历史）继任链
    {"person_a": 101, "person_b": 1, "type": "predecessor_successor",
     "context": "刘冰2018-2022任南乐县委书记；梅兴秦2026年继任南乐县委书记（中间历任未知）",
     "overlap_org": "中共南乐县委员会", "overlap_period": "2018-2026"},
    {"person_a": 101, "person_b": 2, "type": "predecessor_successor",
     "context": "刘冰2016-2018任南乐县长；周笃铭2026年任南乐县长（继任链）",
     "overlap_org": "南乐县人民政府", "overlap_period": "2016-2026"},
]

# ═══════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════

import sqlite3


def create_tables(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

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
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

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
        );

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
        );
    """)
    conn.commit()


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 南乐县人民政府网站 (nanle.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    # Insert organizations
    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    # Insert positions
    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c,"") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    # Insert relationships
    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c,"") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "书记" in post and "县委" in post and "副" not in post:
            return ("255,50,50", 20.0)  # Red, top leader
        elif "县长" in post and "副" not in post:
            return ("50,100,255", 20.0)  # Blue
        elif "副书记" in post:
            return ("100,100,255", 15.0)  # Deputy secretary
        elif "县委常委" in post or "部长" in post:
            return ("50,100,255", 12.0)
        elif "人大" in post:
            return ("200,255,255", 12.0)  # Cyan for congress
        else:
            return ("100,100,100", 12.0)  # Grey

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,255"),
        }.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络 — 截至{AS_OF}</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    # Person nodes
    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    # person → org edges
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person edges
    for r in relationships:
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

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


# ═══════════════════════════════════════════════════════════════════
# PERSON JSON GENERATION
# ═══════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "南乐县十四届县委第1次常委会会议召开",
         "url": "http://www.nanle.gov.cn/content/2026/1287250.html",
         "publisher": "南乐县人民政府", "published_at": "2026-07-08",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认县委书记梅兴秦、县委副书记（县长人选）周笃铭、县委副书记孙丽君、县委常委谢海萌/弓晓飞/徐娅/张钤/王昊/李扬/杨二卫；孙思群、王坤列席"},
        {"id": "S002", "title": "南乐县十四届县委2026年第3次书记专题会议",
         "url": "http://www.nanle.gov.cn/content/2026/1315177.html",
         "publisher": "南乐县人民政府", "published_at": "2026-07-29",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认周笃铭已成为县委副书记、县长；同场常委谢海萌等出席"},
        {"id": "S003", "title": "县长周骞铭带队调研2026年民生实事推进情况",
         "url": "http://www.nanle.gov.cn/content/2026/1316148.html",
         "publisher": "南乐县人民政府", "published_at": "2026-08-01",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认县长周笃铭带县领导王坤、靳卫军、郭专政、师啸宇、张进良调研"},
        {"id": "S004", "title": "南乐县十六届人大七次会议举行第一次全体大会",
         "url": "http://www.nanle.gov.cn/content/2026/1291208.html",
         "publisher": "南乐县人民政府", "published_at": "2026-07-16",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "孙思群=县人大常委会主任；谢海萌=县委常委、县委组织部部长"},
        {"id": "S005", "title": "南乐县人民政府门户网站首页",
         "url": "http://www.nanle.gov.cn/",
         "publisher": "南乐县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "首页与政务要闻频道显示梅兴秦、周笃铭近期活动"},
    ]


def make_person_json(person, timeline, rels, source_reg):
    """Build a person graph JSON following the V1 schema."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "濮阳市",
            "region": "南乐县",
            "job": person["current_post"],
            "task_id": "henan_南乐县",
            "time_focus": "截至2026年7-8月"
        },
        "identity": {
            "person_id": f"nanlexian_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if ("书记" in person["current_post"] and "副" not in person["current_post"]) or ("县长" in person["current_post"] and "副" not in person["current_post"]) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至{AS_OF}，公开渠道未发现{person['name']}的负面信号",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": source_reg,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{person['name']}的出生年份、籍贯、教育背景和任现职前的完整履历均缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}任{person['current_post']}前的完整履历是什么？",
                "why_it_matters": "无法评估其职业路径、来源系统和晋升模式",
                "suggested_queries": [f"{person['name']} 简历 南乐", f"{person['name']} 任前公示", f"{person['name']} Baidu Baike"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年份、籍贯、教育背景是什么？",
                "why_it_matters": "缺少基础身份信息，无法进行去重和人口统计分析",
                "suggested_queries": [f"{person['name']} 出生", f"{person['name']} 濮阳"],
                "last_attempted": AS_OF,
            },
        ],
    }


if __name__ == "__main__":
    run_build()

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 梅兴秦 (县委书记)
    mxq_timeline = [
        {"start": "2026-06", "end": "至今", "org": "中共南乐县委员会",
         "title": "中共南乐县委书记、县第一总河长",
         "notes": "主持十四届县委常委会、书记专题会议；县第十四次党代会召开后任新一届县委书记。",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "未知", "end": "2026", "org": "华龙区人民政府",
         "title": "濮阳市华龙区区长（前任职务）",
         "notes": "2026年4月仍以华龙区区长活动；后调任南乐县委书记。",
         "confidence": "plausible", "source_ids": ["S005"]},
    ]
    mxq_rels = [
        {"person": "周笃铭", "person_id": "nanlexian_周笃铭",
         "relationship_type": "superior_subordinate", "strength": "strong",
         "evidence": "县委书记与县长——党政主要领导搭档，梅兴秦主持县委常委会，周笃铭主持县政府工作",
         "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"person": "孙丽君", "person_id": "nanlexian_孙丽君",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "县委书记与专职副书记在县委常委会共事",
         "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "谢海萌", "person_id": "nanlexian_谢海萌",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "县委书记与组织部长——县委常委会共事，组织部长负责人事工作",
         "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S004"]},
        {"person": "刘冰", "person_id": "nanlexian_刘冰",
         "relationship_type": "predecessor_successor", "strength": "medium",
         "evidence": "刘冰2018-2022任南乐县委书记，梅兴秦2026年继任（其中间隔多年/多任）",
         "overlap_org": "中共南乐县委员会", "overlap_period": "2018-2026",
         "direction": "person_to_other", "confidence": "plausible",
         "source_ids": ["S005"]},
    ]
    mxq_json = make_person_json(persons[0], mxq_timeline, mxq_rels, source_register)
    mxq_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-濮阳市-县委书记-梅兴秦.json")
    with open(mxq_path, "w", encoding="utf-8") as f:
        json.dump(mxq_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(mxq_path)}")

    # 周笃铭 (县长)
    zdm_timeline = [
        {"start": "2026-07", "end": "至今", "org": "南乐县人民政府",
         "title": "南乐县委副书记、县人民政府县长",
         "notes": "主持县政府全面工作；十六届人大七次会议确认（2026-07）；负责审计等。",
         "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"start": "2026-06", "end": "2026-07", "org": "南乐县人民政府",
         "title": "县委副书记、县政府党组书记、县长人选",
         "notes": "十四届县委首次常委会时以县长人选身份出席；作为县政府党组书记主持政府常务会议。",
         "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    zdm_rels = [
        {"person": "梅兴秦", "person_id": "nanlexian_梅兴秦",
         "relationship_type": "superior_subordinate", "strength": "strong",
         "evidence": "县长与县委书记——党政主要领导搭档",
         "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"person": "孙丽君", "person_id": "nanlexian_孙丽君",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "县委副书记之间在县委常委会共事",
         "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "孙思群", "person_id": "nanlexian_孙思群",
         "relationship_type": "superior_subordinate", "strength": "medium",
         "evidence": "县长在人大七次会议接受人大常委会选举与监督",
         "overlap_org": "南乐县人大 / 南乐县人民政府", "overlap_period": "2026-07",
         "direction": "other_to_person", "confidence": "confirmed",
         "source_ids": ["S004"]},
        {"person": "刘冰", "person_id": "nanlexian_刘冰",
         "relationship_type": "predecessor_successor", "strength": "medium",
         "evidence": "刘冰2016-2018任南乐县长，周笃铭2026年继任",
         "overlap_org": "南乐县人民政府", "overlap_period": "2016-2026",
         "direction": "person_to_other", "confidence": "plausible",
         "source_ids": ["S005"]},
    ]
    zdm_json = make_person_json(persons[1], zdm_timeline, zdm_rels, source_register)
    zdm_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-濮阳市-县长-周笃铭.json")
    with open(zdm_path, "w", encoding="utf-8") as f:
        json.dump(zdm_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(zdm_path)}")

    # 孙丽君 (县委副书记)
    slj_timeline = [
        {"start": "2026-06", "end": "至今", "org": "中共南乐县委员会",
         "title": "南乐县委副书记",
         "notes": "专职县委副书记，出席十四届县委常委会。",
         "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    slj_rels = [
        {"person": "梅兴秦", "person_id": "nanlexian_梅兴秦",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "专职副书记与县委书记在县委常委会共事",
         "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "周笃铭", "person_id": "nanlexian_周笃铭",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "两位县委副书记在县委常委会共事",
         "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    slj_json = make_person_json(persons[2], slj_timeline, slj_rels, source_register)
    slj_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-濮阳市-县委副书记-孙丽君.json")
    with open(slj_path, "w", encoding="utf-8") as f:
        json.dump(slj_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(slj_path)}")

    # 谢海萌 (县委组织部长)
    xhm_timeline = [
        {"start": "2026-06", "end": "至今", "org": "中共南乐县委员会",
         "title": "南乐县委常委、县委组织部部长",
         "notes": "承担干部人事与换届候选人酝酿推荐工作；出席县委常委会。",
         "confidence": "confirmed", "source_ids": ["S001", "S004"]},
    ]
    xhm_rels = [
        {"person": "梅兴秦", "person_id": "nanlexian_梅兴秦",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "组织部长与县委书记在县委常委会共事",
         "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "周笃铭", "person_id": "nanlexian_周笃铭",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "组织部长与县长在县委常委会共事",
         "overlap_org": "中共南乐县委员会", "overlap_period": "2026-06至今",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    xhm_json = make_person_json(persons[3], xhm_timeline, xhm_rels, source_register)
    xhm_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-濮阳市-县委组织部长-谢海萌.json")
    with open(xhm_path, "w", encoding="utf-8") as f:
        json.dump(xhm_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(xhm_path)}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")