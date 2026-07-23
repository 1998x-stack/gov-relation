#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
瓮安县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 贵州省
Parent City: 黔南布依族苗族自治州
Region: 瓮安县
Task: guizhou_瓮安县
Targets: 县委书记 & 县长

当前在任 (as of 2026-07-23):
- 县委书记: 罗仕凯 (confirmed from wengan.gov.cn leadership page, July 2026 appointment;
              succeeded 杨朝伟, who was 州委常委、县委书记 through mid-July 2026)
- 县委副书记、县人民政府县长: 刘祥祯 (confirmed from leadership page and county常务会议 news)
- 县委副书记（挂职）: 武越锋
- 县委常委、县纪委书记、县监委主任: 李丹
- 县委常委、县委组织部部长: 覃建彬
- 县委常委、常务副县长: 刘汉乾
- 县委常委、县委政法委书记: 王大伟
- 县委常委: 唐连江
- 县委常委、副县长: 吴笛
- 县委常委、县委办公室主任: 汪福桥
- 县委常委、宣传部部长、统战部部长: 汤玉洁
- 县委常委、副县长: 张文涛
- 副县长: 张林才、桂雪松、胡云健、罗林（兼公安局长）、张少伟
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
TASK_ID = "guizhou_瓮安县"
SLUG = "瓮安县"
AS_OF = "2026-07-23"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = BASE

# =========================================================================
# 1. SOURCE REGISTER
# =========================================================================
source_register = [
    {"id": "S001", "title": "瓮安县人民政府门户网站——领导之窗·县委",
     "url": "http://www.wengan.gov.cn/gk/zfgk/ldzc/xw/",
     "publisher": "瓮安县人民政府", "published_at": "2026-07-23", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "列出县委领导班子12人：县委书记罗仕凯等"},
    {"id": "S002", "title": "瓮安县人民政府门户网站——领导之窗·政府",
     "url": "http://www.wengan.gov.cn/gk/zfgk/ldzc/xw/",
     "publisher": "瓮安县人民政府", "published_at": "2026-07-23", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "列出县政府领导班子9人：县长刘祥祯及8位副县长"},
    {"id": "S003", "title": "瓮安县人民政府门户网站——领导之窗·人大",
     "url": "http://www.wengan.gov.cn/gk/zfgk/ldzc/xw/",
     "publisher": "瓮安县人民政府", "published_at": "2026-07-23", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "列出县人大常委会领导班子：主任韦松等"},
    {"id": "S004", "title": "瓮安县人民政府门户网站——领导之窗·政协",
     "url": "http://www.wengan.gov.cn/gk/zfgk/ldzc/xw/",
     "publisher": "瓮安县人民政府", "published_at": "2026-07-23", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "列出县政协领导班子：主席孟先锋等"},
    {"id": "S005", "title": "瓮安县人民政府门户网站——罗仕凯到猴场镇开展革命传统教育并督导调研重点工作",
     "url": "http://www.wengan.gov.cn/xw/zwyw/202607/t20260722_90647761.html",
     "publisher": "瓮安县融媒体中心", "published_at": "2026-07-22", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认罗仕凯以县委书记身份调研"},
    {"id": "S006", "title": "瓮安县人民政府门户网站——杨朝伟主持召开县委常委会第251次扩大会议",
     "url": "http://www.wengan.gov.cn/xw/zwyw/202607/t20260715_90626887.html",
     "publisher": "瓮安县融媒体中心", "published_at": "2026-07-15", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认杨朝伟为州委常委、县委书记（7月中旬在任）；刘祥祯为县委副书记、县长"},
    {"id": "S007", "title": "瓮安县人民政府门户网站——瓮安县十八届人民政府第107次常务会议召开",
     "url": "http://www.wengan.gov.cn/xw/zwyw/202607/t20260714_90621092.html",
     "publisher": "瓮安县融媒体中心", "published_at": "2026-07-14", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认刘祥祯以县委副书记、县长身份主持召开县政府常务会议"},
    {"id": "S008", "title": "瓮安县人民政府门户网站——罗仕凯看望部分退休老干部",
     "url": "http://www.wengan.gov.cn/xw/zwyw/202607/t20260722_90647763.html",
     "publisher": "瓮安县融媒体中心", "published_at": "2026-07-22", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认罗仕凯以县委书记身份开展工作"},
]

# =========================================================================
# 2. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {"id": 1, "name": "罗仕凯", "gender": "男", "ethnicity": "布依族",
     "birth": "1980-08", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县委书记", "current_org": "中共瓮安县委员会",
     "source": "S001"},

    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {"id": 2, "name": "刘祥祯", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县委副书记、县人民政府县长、党组书记",
     "current_org": "瓮安县人民政府",
     "source": "S001"},

    # ════════════════════════════════════════
    # 县委领导班子
    # ════════════════════════════════════════
    {"id": 3, "name": "武越锋", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县委副书记（挂职）", "current_org": "中共瓮安县委员会",
     "source": "S001"},

    {"id": 4, "name": "李丹", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县委常委、县纪委书记、县监委主任",
     "current_org": "中共瓮安县纪律检查委员会",
     "source": "S001"},

    {"id": 5, "name": "覃建彬", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县委常委、县委组织部部长、县委党校校长",
     "current_org": "中共瓮安县委员会",
     "source": "S001"},

    {"id": 6, "name": "刘汉乾", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县委常委、县政府党组副书记、常务副县长",
     "current_org": "瓮安县人民政府",
     "source": "S001"},

    {"id": 7, "name": "王大伟", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县委常委、县委政法委书记",
     "current_org": "中共瓮安县委员会",
     "source": "S001"},

    {"id": 8, "name": "唐连江", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县委常委、瓮安经济开发区党工委委员、副书记",
     "current_org": "瓮安经济开发区",
     "source": "S001"},

    {"id": 9, "name": "吴笛", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县委常委、县人民政府党组成员、副县长",
     "current_org": "瓮安县人民政府",
     "source": "S001"},

    {"id": 10, "name": "汪福桥", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县委常委、县委办公室主任、县直属机关工委书记",
     "current_org": "中共瓮安县委员会",
     "source": "S001"},

    {"id": 11, "name": "汤玉洁", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县委常委、县委宣传部部长、县委统战部部长",
     "current_org": "中共瓮安县委员会",
     "source": "S001"},

    {"id": 12, "name": "张文涛", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县委常委、县人民政府副县长",
     "current_org": "瓮安县人民政府",
     "source": "S001"},

    # ════════════════════════════════════════
    # 县政府副县长（不含常委）
    # ════════════════════════════════════════
    {"id": 13, "name": "张林才", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县人民政府党组成员、副县长",
     "current_org": "瓮安县人民政府",
     "source": "S002"},

    {"id": 14, "name": "桂雪松", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县人民政府党组成员、副县长",
     "current_org": "瓮安县人民政府",
     "source": "S002"},

    {"id": 15, "name": "胡云健", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县人民政府党组成员、副县长",
     "current_org": "瓮安县人民政府",
     "source": "S002"},

    {"id": 16, "name": "罗林", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县人民政府党组成员、副县长，县公安局党委书记、局长",
     "current_org": "瓮安县人民政府",
     "source": "S002"},

    {"id": 17, "name": "张少伟", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县人民政府党组成员、副县长",
     "current_org": "瓮安县人民政府",
     "source": "S002"},

    # ════════════════════════════════════════
    # 前任县委书记（重要 predecessor）
    # ════════════════════════════════════════
    {"id": 18, "name": "杨朝伟", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原）黔南州委常委、瓮安县委书记",
     "current_org": "中共黔南州委员会",
     "source": "S006"},

    # ════════════════════════════════════════
    # 人大、政协主要领导
    # ════════════════════════════════════════
    {"id": 19, "name": "韦松", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县人大常委会党组书记、主任",
     "current_org": "瓮安县人民代表大会常务委员会",
     "source": "S003"},

    {"id": 20, "name": "孟先锋", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓮安县政协党组书记、主席",
     "current_org": "中国人民政治协商会议瓮安县委员会",
     "source": "S004"},
]

# =========================================================================
# 3. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共瓮安县委员会", "type": "党委", "level": "县处级",
     "parent": "中共黔南布依族苗族自治州委员会", "location": "贵州省黔南州瓮安县"},
    {"id": 2, "name": "瓮安县人民政府", "type": "政府", "level": "县处级",
     "parent": "黔南布依族苗族自治州人民政府", "location": "贵州省黔南州瓮安县"},
    {"id": 3, "name": "瓮安县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "黔南布依族苗族自治州人民代表大会常务委员会", "location": "贵州省黔南州瓮安县"},
    {"id": 4, "name": "中国人民政治协商会议瓮安县委员会", "type": "政协", "level": "县处级",
     "parent": "", "location": "贵州省黔南州瓮安县"},
    {"id": 5, "name": "中共瓮安县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共黔南布依族苗族自治州纪律检查委员会", "location": "贵州省黔南州瓮安县"},
    {"id": 6, "name": "瓮安经济开发区", "type": "开发区", "level": "县处级",
     "parent": "瓮安县人民政府", "location": "贵州省黔南州瓮安县"},
    {"id": 7, "name": "瓮安县公安局", "type": "政府", "level": "正科级",
     "parent": "瓮安县人民政府", "location": "贵州省黔南州瓮安县"},
    {"id": 8, "name": "中共黔南州委员会", "type": "党委", "level": "地厅级",
     "parent": "中共贵州省委", "location": "贵州省黔南州都匀市"},
]

# =========================================================================
# 4. POSITIONS
# =========================================================================
positions = [
    # ── 罗仕凯 ──
    {"person_id": 1, "org_id": 1, "title": "瓮安县委书记",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "现任，2026年7月确认在任；接替杨朝伟"},

    # ── 刘祥祯 ──
    {"person_id": 2, "org_id": 1, "title": "瓮安县委副书记",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "瓮安县人民政府党组书记、县长",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    {"person_id": 2, "org_id": 6, "title": "瓮安经济开发区党工委副书记、管委会主任",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "兼任"},

    # ── 武越锋 ──
    {"person_id": 3, "org_id": 1, "title": "瓮安县委副书记（挂职）",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "挂职"},

    # ── 李丹 ──
    {"person_id": 4, "org_id": 1, "title": "瓮安县委常委",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 4, "org_id": 5, "title": "瓮安县纪委书记、县监委主任",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 4, "org_id": 6, "title": "瓮安经济开发区党工委委员、纪检监察工委书记",
     "start_date": "", "end_date": "", "rank": "", "note": "兼任"},

    # ── 覃建彬 ──
    {"person_id": 5, "org_id": 1, "title": "瓮安县委常委、县委组织部部长、县委党校校长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 刘汉乾 ──
    {"person_id": 6, "org_id": 1, "title": "瓮安县委常委",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 6, "org_id": 2, "title": "瓮安县人民政府党组副书记、常务副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 王大伟 ──
    {"person_id": 7, "org_id": 1, "title": "瓮安县委常委、县委政法委书记",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 唐连江 ──
    {"person_id": 8, "org_id": 1, "title": "瓮安县委常委",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 8, "org_id": 6, "title": "瓮安经济开发区党工委委员、副书记",
     "start_date": "", "end_date": "", "rank": "", "note": "兼任"},

    # ── 吴笛 ──
    {"person_id": 9, "org_id": 1, "title": "瓮安县委常委",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 9, "org_id": 2, "title": "瓮安县人民政府党组成员、副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 汪福桥 ──
    {"person_id": 10, "org_id": 1, "title": "瓮安县委常委、县委办公室主任、县直属机关工委书记",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 汤玉洁 ──
    {"person_id": 11, "org_id": 1, "title": "瓮安县委常委、县委宣传部部长、县委统战部部长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 张文涛 ──
    {"person_id": 12, "org_id": 1, "title": "瓮安县委常委",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 12, "org_id": 2, "title": "瓮安县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 张林才 ──
    {"person_id": 13, "org_id": 2, "title": "瓮安县人民政府党组成员、副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 桂雪松 ──
    {"person_id": 14, "org_id": 2, "title": "瓮安县人民政府党组成员、副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 胡云健 ──
    {"person_id": 15, "org_id": 2, "title": "瓮安县人民政府党组成员、副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 罗林 ──
    {"person_id": 16, "org_id": 2, "title": "瓮安县人民政府党组成员、副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 16, "org_id": 7, "title": "瓮安县公安局党委书记、局长",
     "start_date": "", "end_date": "", "rank": "正科级", "note": "兼任"},

    # ── 张少伟 ──
    {"person_id": 17, "org_id": 2, "title": "瓮安县人民政府党组成员、副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 杨朝伟（前任县委书记） ──
    {"person_id": 18, "org_id": 8, "title": "黔南州委常委",
     "start_date": "", "end_date": "", "rank": "地厅级副职", "note": "仍在州委常委任上"},
    {"person_id": 18, "org_id": 1, "title": "瓮安县委书记（前任）",
     "start_date": "", "end_date": "2026-07", "rank": "县处级正职",
     "note": "曾任瓮安县委书记；至2026年7月中旬仍在任（主持县委常委会第251次会议）；后由罗仕凯接替"},

    # ── 韦松 ──
    {"person_id": 19, "org_id": 3, "title": "瓮安县人大常委会党组书记、主任",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},

    # ── 孟先锋 ──
    {"person_id": 20, "org_id": 4, "title": "瓮安县政协党组书记、主席",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
]

# =========================================================================
# 5. RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 党政主要领导 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "罗仕凯（县委书记）与刘祥祯（县委副书记、县长）构成书记-县长搭档",
     "overlap_org": "中共瓮安县委员会/瓮安县人民政府", "overlap_period": "2026-07~"},

    # ── 县委书记与县委常委班子 ──
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "罗仕凯（书记）与武越锋（副书记挂职）在县委班子共事",
     "overlap_org": "中共瓮安县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "罗仕凯（书记）与李丹（纪委书记）在县委班子共事",
     "overlap_org": "中共瓮安县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "罗仕凯（书记）与覃建彬（组织部长）在县委班子共事",
     "overlap_org": "中共瓮安县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "罗仕凯（书记）与王大伟（政法委书记）在县委班子共事",
     "overlap_org": "中共瓮安县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "罗仕凯（书记）与汪福桥（县委办主任）在县委班子共事",
     "overlap_org": "中共瓮安县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "罗仕凯（书记）与汤玉洁（宣传部长）在县委班子共事",
     "overlap_org": "中共瓮安县委员会", "overlap_period": ""},

    # ── 县长与副县长班子 ──
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "刘祥祯（县长）与刘汉乾（常务副县长）在县政府班子共事",
     "overlap_org": "瓮安县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "overlap",
     "context": "刘祥祯（县长）与吴笛（副县长）在县政府班子共事",
     "overlap_org": "瓮安县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "overlap",
     "context": "刘祥祯（县长）与张文涛（副县长）在县政府班子共事",
     "overlap_org": "瓮安县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "overlap",
     "context": "刘祥祯（县长）与张林才（副县长）在县政府班子共事",
     "overlap_org": "瓮安县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "overlap",
     "context": "刘祥祯（县长）与桂雪松（副县长）在县政府班子共事",
     "overlap_org": "瓮安县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "overlap",
     "context": "刘祥祯（县长）与胡云健（副县长）在县政府班子共事",
     "overlap_org": "瓮安县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "overlap",
     "context": "刘祥祯（县长）与罗林（副县长兼公安局长）在县政府班子共事",
     "overlap_org": "瓮安县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "overlap",
     "context": "刘祥祯（县长）与张少伟（副县长）在县政府班子共事",
     "overlap_org": "瓮安县人民政府", "overlap_period": ""},

    # ── 前任县委书记与现有班子 ──
    {"person_a": 18, "person_b": 2, "type": "overlap",
     "context": "杨朝伟（前任州委常委、县委书记）与刘祥祯（县长）曾在县委班子共事",
     "overlap_org": "中共瓮安县委员会", "overlap_period": ""},
    {"person_a": 18, "person_b": 1, "type": "predecessor_successor",
     "context": "杨朝伟为前任瓮安县委书记，罗仕凯为其接替者",
     "overlap_org": "中共瓮安县委员会", "overlap_period": "~2026-07"},

    # ── 县委常委会成员之间 ──
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "李丹（纪委书记）与覃建彬（组织部长）在县委班子共事",
     "overlap_org": "中共瓮安县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "overlap",
     "context": "覃建彬（组织部长）与王大伟（政法委书记）在县委班子共事",
     "overlap_org": "中共瓮安县委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 9, "type": "overlap",
     "context": "刘汉乾（常务副县长）与吴笛（副县长）在县政府班子共事",
     "overlap_org": "瓮安县人民政府", "overlap_period": ""},

    # ── 人大、政协主要领导 ──
    {"person_a": 1, "person_b": 19, "type": "overlap",
     "context": "罗仕凯（书记）与韦松（人大主任）在县级班子共事",
     "overlap_org": "瓮安县", "overlap_period": ""},
    {"person_a": 1, "person_b": 20, "type": "overlap",
     "context": "罗仕凯（书记）与孟先锋（政协主席）在县级班子共事",
     "overlap_org": "瓮安县", "overlap_period": ""},
    {"person_a": 2, "person_b": 19, "type": "overlap",
     "context": "刘祥祯（县长）与韦松（人大主任）在县级班子共事",
     "overlap_org": "瓮安县", "overlap_period": ""},
    {"person_a": 2, "person_b": 20, "type": "overlap",
     "context": "刘祥祯（县长）与孟先锋（政协主席）在县级班子共事",
     "overlap_org": "瓮安县", "overlap_period": ""},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build():
    os.makedirs(BASE, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
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
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"wengan_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "255,50,50"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "50,100,255"
        if "纪委书记" in post:
            return "255,165,0"
        if "副" in post or "副书记" in post:
            return "100,150,220"
        if "主任" in post and "副" not in post:
            return "60,180,60"
        if "政协" in post:
            return "180,160,80"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post) or \
               ("县长" in post and "副" not in post and "人大" not in post and "政协" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "square"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "circle"
        if "纪委书记" in post or "纪委" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "纪委": "255,200,150",
            "开发区": "200,255,200",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>瓮安县领导班子关系网络（基于瓮安县人民政府门户网站）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization
    for pos in positions:
        if pos["org_id"] == 99:
            continue
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person
    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person Graph JSONs ──
    now = AS_OF.replace("-", "")

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        """Generate a person graph JSON following the person_graph_json.md schema."""
        rank = "县处级正职" if (
            ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "纪委" not in p.get("current_post", ""))
            or ("县长" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "人大" not in p.get("current_post", "") and "政协" not in p.get("current_post", ""))
        ) else "县处级副职"

        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "贵州省",
                "city": "黔南布依族苗族自治州",
                "region": "瓮安县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"wengan_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
                ] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": rank,
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S005"] if p["id"] == 1 else ["S001", "S007"] if p["id"] == 2 else ["S001"]
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": relationships_list,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "confirmed" if p.get("birth") else "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": ""
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 瓮安"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 罗仕凯 Person JSON ──
    lsk_timeline = [
        {"start": "", "end": "", "org": "中共瓮安县委员会", "title": "瓮安县委书记",
         "notes": "现任，布依族，1980年8月出生，2026年7月瓮安县人民政府网站领导之窗确认；接替杨朝伟",
         "confidence": "confirmed", "source_ids": ["S001", "S005"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "罗仕凯任瓮安县委书记之前的完整履历未找到（籍贯、教育背景、早期任职经历等信息缺失）",
         "confidence": "unverified", "source_ids": []},
    ]
    lsk_relationships = [
        {"person": "刘祥祯", "person_id": "wengan_刘祥祯", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "罗仕凯（县委书记）与刘祥祯（县委副书记、县长）构成书记-县长搭档",
         "overlap_org": "中共瓮安县委员会/瓮安县人民政府", "overlap_period": "2026-07~",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]

    lsk_json = make_person_json(persons[0], lsk_timeline, lsk_relationships)
    lsk_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-黔南布依族苗族自治州-县委书记-罗仕凯.json")
    with open(lsk_path, "w", encoding="utf-8") as f:
        json.dump(lsk_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lsk_path}")

    # ── 刘祥祯 Person JSON ──
    lxz_timeline = [
        {"start": "", "end": "", "org": "瓮安县人民政府", "title": "瓮安县委副书记、县人民政府县长、党组书记",
         "notes": "现任，同时兼任瓮安经济开发区党工委副书记、管委会主任",
         "confidence": "confirmed", "source_ids": ["S001", "S007"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "刘祥祯任瓮安县长前的完整履历未找到（出生年月、籍贯、教育背景、早期任职经历等信息缺失）",
         "confidence": "unverified", "source_ids": []},
    ]
    lxz_relationships = [
        {"person": "罗仕凯", "person_id": "wengan_罗仕凯", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "刘祥祯（县长）与罗仕凯（县委书记）构成书记-县长搭档",
         "overlap_org": "中共瓮安县委员会/瓮安县人民政府", "overlap_period": "2026-07~",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S007"]},
        {"person": "刘汉乾", "person_id": "wengan_刘汉乾", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "刘祥祯（县长）与刘汉乾（常务副县长）在县政府班子共事",
         "overlap_org": "瓮安县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "张林才", "person_id": "wengan_张林才", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "刘祥祯（县长）与张林才（副县长）在县政府班子共事",
         "overlap_org": "瓮安县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]

    lxz_json = make_person_json(persons[1], lxz_timeline, lxz_relationships)
    lxz_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-黔南布依族苗族自治州-县长-刘祥祯.json")
    with open(lxz_path, "w", encoding="utf-8") as f:
        json.dump(lxz_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lxz_path}")

    print("\nDone. All artifacts generated in staging directory.")


if __name__ == "__main__":
    build()
