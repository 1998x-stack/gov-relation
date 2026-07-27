#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 蓬江区 (Pengjiang District), Jiangmen, Guangdong.
   
   Research date: 2026-07-22
   Sources: pjq.gov.cn leadership page, government news articles,
            media reports, appointment records.
   
   Official leadership roster source: http://www.pjq.gov.cn/zwgk/ldzc/
   Accessed: 2026-07-22
   
   Note: Full career biographies for most leaders could not be verified
   due to degraded web access during research. All current roles are
   confirmed from the official government leadership page.
"""

import sqlite3
import os
import json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangdong_蓬江区")
DB_PATH = os.path.join(TMP, "蓬江区_network.db")
GEXF_PATH = os.path.join(TMP, "蓬江区_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Current Top Leaders ──

    # 李志坚 - 蓬江区委书记 (Party Secretary)
    {"id": 1, "name": "李志坚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江门市蓬江区委书记",
     "current_org": "中共江门市蓬江区委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    # 黄嘉仪 - 区长兼区委副书记 (District Mayor & Deputy Party Secretary)
    {"id": 2, "name": "黄嘉仪", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江门市蓬江区委副书记、区长",
     "current_org": "江门市蓬江区人民政府",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    # ── 区委常委 (Standing Committee Members) ──
    {"id": 3, "name": "王坚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蓬江区委常委、滨江新区管委会副主任",
     "current_org": "中共江门市蓬江区委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 4, "name": "梁海标", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蓬江区委常委",
     "current_org": "中共江门市蓬江区委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 5, "name": "谢树浓", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蓬江区委常委、副区长",
     "current_org": "中共江门市蓬江区委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 6, "name": "梁雁仙", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蓬江区委常委",
     "current_org": "中共江门市蓬江区委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 7, "name": "梁柏旺", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蓬江区委常委",
     "current_org": "中共江门市蓬江区委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 8, "name": "唐春", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蓬江区委常委、滨江新区管委会副主任",
     "current_org": "中共江门市蓬江区委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    # ── 副区长 (Deputy District Mayors) ──
    {"id": 9, "name": "吴健明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区副区长",
     "current_org": "江门市蓬江区人民政府",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 10, "name": "陈健敏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区副区长",
     "current_org": "江门市蓬江区人民政府",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 11, "name": "吕文光", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区副区长",
     "current_org": "江门市蓬江区人民政府",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 12, "name": "蒙晓波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区副区长",
     "current_org": "江门市蓬江区人民政府",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 13, "name": "徐瑀琨", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区副区长",
     "current_org": "江门市蓬江区人民政府",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    # ── 区人大 (District People's Congress) ──
    {"id": 14, "name": "李达成", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蓬江区人大常委会主任",
     "current_org": "江门市蓬江区人民代表大会常务委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 15, "name": "黄月嫦", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区人大常委会副主任",
     "current_org": "江门市蓬江区人民代表大会常务委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 16, "name": "林贤光", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区人大常委会副主任",
     "current_org": "江门市蓬江区人民代表大会常务委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 17, "name": "谢强伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区人大常委会副主任",
     "current_org": "江门市蓬江区人民代表大会常务委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 18, "name": "卢永生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区人大常委会副主任",
     "current_org": "江门市蓬江区人民代表大会常务委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 19, "name": "林晖", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区人大常委会副主任",
     "current_org": "江门市蓬江区人民代表大会常务委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    # ── 区政协 (District CPPCC) ──
    {"id": 20, "name": "黄文坚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区政协副主席",
     "current_org": "中国人民政治协商会议江门市蓬江区委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 21, "name": "吕琼峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区政协副主席",
     "current_org": "中国人民政治协商会议江门市蓬江区委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 22, "name": "林永康", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区政协副主席",
     "current_org": "中国人民政治协商会议江门市蓬江区委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 23, "name": "李茂槐", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区政协副主席",
     "current_org": "中国人民政治协商会议江门市蓬江区委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 24, "name": "黄国昌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "蓬江区政协副主席",
     "current_org": "中国人民政治协商会议江门市蓬江区委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    # ── 滨江新区 (Riverside New District) ──
    {"id": 25, "name": "林伟勤", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "滨江新区管委会副主任",
     "current_org": "滨江新区管理委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    {"id": 26, "name": "温国宁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "滨江新区管委会副主任",
     "current_org": "滨江新区管理委员会",
     "source": "http://www.pjq.gov.cn/zwgk/ldzc/ (2026-07-22)"},

    # ── Previous Leaders (known from news and appointment records) ──
    {"id": 27, "name": "劳茂昌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前蓬江区委书记（已离任）",
     "current_org": "",
     "source": "江门市干部任免信息 - media reports (前任区委书记)"},

    {"id": 28, "name": "文丽", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前蓬江区区长（已离任）",
     "current_org": "",
     "source": "江门市干部任免信息 - media reports (前任区长)"},

    {"id": 29, "name": "马品高", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前蓬江区区长（已离任）",
     "current_org": "",
     "source": "江门市干部任免信息 - media reports (前任区长)"},
]

organizations = [
    {"id": 1, "name": "中共江门市蓬江区委员会", "type": "党委", "level": "县处级",
     "parent": "中共江门市委员会", "location": "广东省江门市蓬江区"},
    {"id": 2, "name": "江门市蓬江区人民政府", "type": "政府", "level": "县处级",
     "parent": "江门市人民政府", "location": "广东省江门市蓬江区"},
    {"id": 3, "name": "江门市蓬江区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "江门市人民代表大会常务委员会", "location": "广东省江门市蓬江区"},
    {"id": 4, "name": "中国人民政治协商会议江门市蓬江区委员会", "type": "政协", "level": "县处级",
     "parent": "江门市政协", "location": "广东省江门市蓬江区"},
    {"id": 5, "name": "滨江新区管理委员会", "type": "开发区", "level": "县处级",
     "parent": "江门市人民政府", "location": "广东省江门市蓬江区"},
]

positions = [
    # 李志坚 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "江门市蓬江区委书记",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "2026年7月仍在任, 公开活动频繁"},

    # 黄嘉仪 — 区委副书记、区长
    {"person_id": 2, "org_id": 1, "title": "蓬江区委副书记",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "兼任区长"},
    {"person_id": 2, "org_id": 2, "title": "蓬江区区长",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "区政府主要负责人"},

    # 王坚 — 区委常委、滨江新区副主任
    {"person_id": 3, "org_id": 1, "title": "蓬江区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 5, "title": "滨江新区管委会副主任",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 梁海标 — 区委常委
    {"person_id": 4, "org_id": 1, "title": "蓬江区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 谢树浓 — 区委常委、副区长
    {"person_id": 5, "org_id": 1, "title": "蓬江区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "蓬江区副区长",
     "start": "", "end": "", "rank": "县处级副职", "note": "常务副区长或分管重点领域"},

    # 梁雁仙 — 区委常委
    {"person_id": 6, "org_id": 1, "title": "蓬江区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 梁柏旺 — 区委常委
    {"person_id": 7, "org_id": 1, "title": "蓬江区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 唐春 — 区委常委、滨江新区副主任
    {"person_id": 8, "org_id": 1, "title": "蓬江区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "滨江新区管委会副主任",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 吴健明 — 副区长
    {"person_id": 9, "org_id": 2, "title": "蓬江区副区长",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 陈健敏 — 副区长
    {"person_id": 10, "org_id": 2, "title": "蓬江区副区长",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 吕文光 — 副区长
    {"person_id": 11, "org_id": 2, "title": "蓬江区副区长",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 蒙晓波 — 副区长
    {"person_id": 12, "org_id": 2, "title": "蓬江区副区长",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 徐瑀琨 — 副区长
    {"person_id": 13, "org_id": 2, "title": "蓬江区副区长",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 李达成 — 区人大常委会主任
    {"person_id": 14, "org_id": 3, "title": "蓬江区人大常委会主任",
     "start": "", "end": "", "rank": "县处级正职", "note": ""},

    # 区人大副主任们
    {"person_id": 15, "org_id": 3, "title": "蓬江区人大常委会副主任",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "蓬江区人大常委会副主任",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "蓬江区人大常委会副主任",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "蓬江区人大常委会副主任",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "蓬江区人大常委会副主任",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 区政协
    {"person_id": 20, "org_id": 4, "title": "蓬江区政协副主席",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "蓬江区政协副主席",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 22, "org_id": 4, "title": "蓬江区政协副主席",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 23, "org_id": 4, "title": "蓬江区政协副主席",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 24, "org_id": 4, "title": "蓬江区政协副主席",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 滨江新区
    {"person_id": 25, "org_id": 5, "title": "滨江新区管委会副主任",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 温国宁 — 滨江新区副主任
    {"person_id": 26, "org_id": 5, "title": "滨江新区管委会副主任",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 劳茂昌 — 前任区委书记
    {"person_id": 27, "org_id": 1, "title": "蓬江区委书记（前）",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "前任区委书记；李志坚前任"},

    # 文丽 — 前任区长
    {"person_id": 28, "org_id": 2, "title": "蓬江区区长（前）",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "前任区长"},

    # 马品高 — 前任区长
    {"person_id": 29, "org_id": 2, "title": "蓬江区区长（前）",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "前任区长"},
]

relationships = [
    # 李志坚 ↔ 黄嘉仪：书记—区长搭档
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长，党政主要负责人",
     "overlap_org": "中共江门市蓬江区委员会/区人民政府",
     "overlap_period": "至今"},

    # 李志坚 ↔ 劳茂昌：前后任区委书记
    {"person_a": 1, "person_b": 27, "type": "接任", "context": "李志坚接替劳茂昌任蓬江区委书记",
     "overlap_org": "中共江门市蓬江区委员会",
     "overlap_period": ""},

    # 黄嘉仪 ↔ 文丽：前后任区长
    {"person_a": 2, "person_b": 28, "type": "接任", "context": "黄嘉仪接替文丽任蓬江区区长",
     "overlap_org": "江门市蓬江区人民政府",
     "overlap_period": ""},

    # 黄嘉仪 ↔ 马品高：前后任区长
    {"person_a": 2, "person_b": 29, "type": "接任", "context": "黄嘉仪接替马品高（中间任）",
     "overlap_org": "江门市蓬江区人民政府",
     "overlap_period": ""},

    # 区委常委之间共事关系
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市蓬江区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市蓬江区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "区委书记—区委常委/副区长",
     "overlap_org": "中共江门市蓬江区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市蓬江区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市蓬江区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市蓬江区委员会",
     "overlap_period": "至今"},

    # 黄嘉仪（区长）↔ 副区长们
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "区长—区委常委/副区长",
     "overlap_org": "江门市蓬江区人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "区长—副区长",
     "overlap_org": "江门市蓬江区人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "区长—副区长",
     "overlap_org": "江门市蓬江区人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "区长—副区长",
     "overlap_org": "江门市蓬江区人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "区长—副区长",
     "overlap_org": "江门市蓬江区人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "区长—副区长",
     "overlap_org": "江门市蓬江区人民政府",
     "overlap_period": "至今"},

    # 滨江新区交叉任职
    {"person_a": 3, "person_b": 8, "type": "共事", "context": "同时任区委常委和滨江新区管委会副主任",
     "overlap_org": "滨江新区管理委员会",
     "overlap_period": "至今"},
    {"person_a": 3, "person_b": 25, "type": "共事", "context": "滨江新区管委会班子成员",
     "overlap_org": "滨江新区管理委员会",
     "overlap_period": "至今"},
    {"person_a": 3, "person_b": 26, "type": "共事", "context": "滨江新区管委会班子成员",
     "overlap_org": "滨江新区管理委员会",
     "overlap_period": "至今"},
    {"person_a": 8, "person_b": 25, "type": "共事", "context": "滨江新区管委会班子成员",
     "overlap_org": "滨江新区管理委员会",
     "overlap_period": "至今"},
    {"person_a": 8, "person_b": 26, "type": "共事", "context": "滨江新区管委会班子成员",
     "overlap_org": "滨江新区管理委员会",
     "overlap_period": "至今"},
]


# ═══════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title and "人大" not in title and "政协" not in title:
        return "255,50,50"
    if "区长" in title:
        return "50,100,255"
    if "政协" in title:
        return "255,240,200"
    if "人大" in title:
        return "200,255,255"
    if "纪委" in title or "监委" in title:
        return "255,165,0"
    if "常委" in title:
        return "200,100,100"
    if "副区长" in title:
        return "100,100,200"
    if "管委会" in title:
        return "200,255,200"
    return "100,100,100"

def person_size(p):
    title = p["current_post"]
    if "区委书记" in title:
        return "20.0"
    if "区长" in title:
        return "18.0"
    if "人大常委会主任" in title:
        return "16.0"
    if "常委" in title:
        return "14.0"
    if "副区长" in title:
        return "12.0"
    if "政协" in title or "人大" in title:
        return "12.0"
    if "管委会" in title:
        return "12.0"
    return "10.0"

def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
        "乡镇/街道": "255,255,200",
    }
    return colors.get(t, "200,200,200")

# ═══════════════════════════════════════════════════════════════════════
# BUILD DATABASE
# ═══════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    c.execute("DELETE FROM persons")
    c.execute("DELETE FROM organizations")
    c.execute("DELETE FROM positions")
    c.execute("DELETE FROM relationships")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            str(p["id"]), p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], "", p["education"],
            p["party_join"], p["work_start"], p["current_post"],
            p["current_org"], p["source"]
        ))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            str(o["id"]), o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            str(pos["person_id"]), str(pos["org_id"]), pos["title"],
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (
            str(r["person_a"]), str(r["person_b"]), r["type"], r["context"],
            r["overlap_org"], r["overlap_period"]
        ))

    conn.commit()
    conn.close()

# ═══════════════════════════════════════════════════════════════════════
# BUILD GEXF
# ═══════════════════════════════════════════════════════════════════════

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>江门市蓬江区领导班子工作关系网络 - 数据来源: pjq.gov.cn及公开报道</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')

    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="江门市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="江门市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0

    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = "plausible"
        if r["type"] in ("共事", "接任"):
            conf = "confirmed"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    print(f"=== 江门市蓬江区网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")

if __name__ == "__main__":
    main()
