#!/usr/bin/env python3
"""夷陵区 (Yiling District, Yichang, Hubei) — Leadership relationship network build script.

Sources:
- 夷陵区人民政府官方网站 领导之窗: https://www.yiling.gov.cn/list-5345-1.html
- 夷陵区六届人大七次会议: https://www.yiling.gov.cn/content-635-560697-1.html
- 宜昌市人民政府 领导之窗: https://www.yichang.gov.cn/list-64273-1.html
调查日期: 2026-08-03
"""

import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TODAY = "2026-08-03"
AS_OF = TODAY
SLUG = "夷陵区"
DB_PATH = os.path.join(SCRIPT_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, f"{SLUG}_network.gexf")

# ── Data ───────────────────────────────────────────────────────────────────────

persons = [
    # ── Party Committee (区委) ──
    {
        "id": 1,
        "name": "张锴",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区委书记",
        "current_org": "中共夷陵区委员会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "2026年7月31日主持区六届人大七次会议。前任为肖鹏飞（已升任宜昌市委常委、市委秘书长）。",
        "open_questions": "完整履历、出生年月、籍贯、教育背景待查"
    },
    {
        "id": 2,
        "name": "覃涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区委副书记、区政府区长",
        "current_org": "夷陵区人民政府",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "2026年7月31日当选夷陵区人民政府区长。",
        "open_questions": "完整履历、出生年月、籍贯、学历背景待查"
    },
    {
        "id": 3,
        "name": "张杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区委副书记",
        "current_org": "中共夷陵区委员会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "完整履历、出生年月待查"
    },
    {
        "id": 4,
        "name": "王寅成",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区委副书记（挂职）",
        "current_org": "中共夷陵区委员会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "挂职",
        "open_questions": "来源单位、履历待查"
    },
    {
        "id": 5,
        "name": "高秉政",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区委常委",
        "current_org": "中共夷陵区委员会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "职务分工、履历待查"
    },
    {
        "id": 6,
        "name": "王晓艳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区委常委",
        "current_org": "中共夷陵区委员会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "职务分工、履历待查"
    },
    {
        "id": 7,
        "name": "梅復雄",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区委常委、区政府副区长",
        "current_org": "夷陵区人民政府",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "区委常委同时也是副区长",
        "open_questions": "具体分工、履历待查"
    },
    {
        "id": 8,
        "name": "许祖钢",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区委常委、区政府副区长",
        "current_org": "夷陵区人民政府",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "区委常委同时也是副区长",
        "open_questions": "具体分工、履历待查"
    },
    {
        "id": 9,
        "name": "殷玉辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区委常委",
        "current_org": "中共夷陵区委员会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "2026年7月31日人大会议主席团成员",
        "open_questions": "职务分工、履历待查"
    },
    {
        "id": 10,
        "name": "张潇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区委常委",
        "current_org": "中共夷陵区委员会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "职务分工、履历待查"
    },
    {
        "id": 11,
        "name": "秦玉龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区委常委",
        "current_org": "中共夷陵区委员会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "2026年7月31日人大会议主席团成员",
        "open_questions": "职务分工、履历待查"
    },
    {
        "id": 12,
        "name": "刘宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区委常委",
        "current_org": "中共夷陵区委员会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "职务分工、履历待查"
    },
    {
        "id": 13,
        "name": "张军锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区委常委",
        "current_org": "中共夷陵区委员会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "职务分工、履历待查"
    },
    # ── District Government (区政府) 副区长 ──
    {
        "id": 14,
        "name": "严军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区副区长",
        "current_org": "夷陵区人民政府",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "分工、履历待查"
    },
    {
        "id": 15,
        "name": "许峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区副区长",
        "current_org": "夷陵区人民政府",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "分工、履历待查"
    },
    {
        "id": 16,
        "name": "覃亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区副区长",
        "current_org": "夷陵区人民政府",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "分工、履历待查"
    },
    {
        "id": 17,
        "name": "文鸿晨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夷陵区副区长",
        "current_org": "夷陵区人民政府",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "分工、履历待查"
    },
    {
        "id": 18,
        "name": "程琼",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夷陵区副区长",
        "current_org": "夷陵区人民政府",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "分工、履历待查"
    },
    {
        "id": 19,
        "name": "罗禹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区副区长（挂职）",
        "current_org": "夷陵区人民政府",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "挂职",
        "open_questions": "来源单位、履历待查"
    },
    # ── 区人大常委会 ──
    {
        "id": 20,
        "name": "汪宏斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区人大常委会主任",
        "current_org": "夷陵区人大常委会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "2026年7月31日人大会议执行主席",
        "open_questions": "履历待查"
    },
    {
        "id": 21,
        "name": "赵长城",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区人大常委会副主任",
        "current_org": "夷陵区人大常委会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "2026年7月31日人大会议执行主席",
        "open_questions": "履历待查"
    },
    {
        "id": 22,
        "name": "刘广胜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区人大常委会副主任",
        "current_org": "夷陵区人大常委会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "2026年7月31日人大会议执行主席",
        "open_questions": "履历待查"
    },
    {
        "id": 23,
        "name": "彭伏林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区人大常委会副主任",
        "current_org": "夷陵区人大常委会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "2026年7月31日人大会议执行主席",
        "open_questions": "履历待查"
    },
    {
        "id": 24,
        "name": "鲁秉格",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区人大常委会副主任",
        "current_org": "夷陵区人大常委会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "2026年7月31日人大会议执行主席",
        "open_questions": "履历待查"
    },
    {
        "id": 25,
        "name": "陈立",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区人大常委会副主任",
        "current_org": "夷陵区人大常委会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "2026年7月31日人大会议执行主席",
        "open_questions": "履历待查"
    },
    {
        "id": 26,
        "name": "谭宏清",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区人大常委会副主任",
        "current_org": "夷陵区人大常委会",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "2026年7月31日人大会议执行主席",
        "open_questions": "履历待查"
    },
    # ── 区政协 ──
    {
        "id": 27,
        "name": "万犁昌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夷陵区政协主席",
        "current_org": "夷陵区政协",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "2026年7月31日人大会议执行主席",
        "open_questions": "履历待查"
    },
    {
        "id": 28,
        "name": "刘红",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夷陵区政协副主席",
        "current_org": "夷陵区政协",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "履历待查"
    },
    {
        "id": 29,
        "name": "黄利红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夷陵区政协副主席",
        "current_org": "夷陵区政协",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "履历待查"
    },
    {
        "id": 30,
        "name": "王兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夷陵区政协副主席",
        "current_org": "夷陵区政协",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "履历待查"
    },
    {
        "id": 31,
        "name": "陈超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夷陵区政协副主席",
        "current_org": "夷陵区政协",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "履历待查"
    },
    {
        "id": 32,
        "name": "谭芳芳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夷陵区政协副主席",
        "current_org": "夷陵区政协",
        "source": "https://www.yiling.gov.cn/list-5345-1.html",
        "notes": "",
        "open_questions": "履历待查"
    },
    # ── Previous Leaders (前任) ──
    {
        "id": 33,
        "name": "肖鹏飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年12月",
        "birthplace": "",
        "education": "大学、工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市委常委、市委秘书长（曾任夷陵区委书记）",
        "current_org": "中共宜昌市委办公室",
        "source": "https://www.yichang.gov.cn/list-64273-1.html",
        "notes": "前任夷陵区委书记，已升任宜昌市委常委、市委秘书长"
    },
]

organizations = [
    {"id": 1, "name": "中共夷陵区委员会", "type": "党委", "level": "县处级", "parent": "中共宜昌市委员会", "location": "宜昌市夷陵区"},
    {"id": 2, "name": "夷陵区人民政府", "type": "政府", "level": "县处级", "parent": "宜昌市人民政府", "location": "宜昌市夷陵区"},
    {"id": 3, "name": "夷陵区人大常委会", "type": "人大", "level": "县处级", "parent": "宜昌市人大常委会", "location": "宜昌市夷陵区"},
    {"id": 4, "name": "夷陵区政协", "type": "政协", "level": "县处级", "parent": "宜昌市政协", "location": "宜昌市夷陵区"},
    {"id": 5, "name": "中央宜昌市委办公室", "type": "党委", "level": "副厅级", "parent": "中共宜昌市委员会", "location": "宜昌市"},
]

positions = [
    # 区委
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "区委主要负责人"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2026-07-31", "end_date": "present", "rank": "县处级正职", "note": "2026年7月31日当选"},
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "专职副书记"},
    {"person_id": 4, "org_id": 1, "title": "区委副书记（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "挂职"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 区政府 副区长
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "挂职"},
    # 人大
    {"person_id": 20, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 21, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 22, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 23, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 24, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 25, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 26, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 政协
    {"person_id": 27, "org_id": 4, "title": "区政协主席、党组书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 28, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 29, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 30, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 31, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 32, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 前任
    {"person_id": 33, "org_id": 1, "title": "区委书记（原任，已离任）", "start_date": "", "end_date": "2026", "rank": "县处级正职", "note": "前任夷陵区委书记，已升任宜昌市委常委、市委秘书长"},
    {"person_id": 33, "org_id": 5, "title": "中共宜昌市委常委、市委秘书长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "现任"},
]

# ── Relationships ──────────────────────────────────────────────────────────────

relationships = [
    # 张锴（区委书记）↔ 核心同事
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长党政搭班", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与专职副书记", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区委书记与区委常委、副区长", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区委书记与区委常委、副区长", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 张锴 ↔ 前任
    {"person_a": 1, "person_b": 33, "type": "predecessor_successor", "context": "张锴接替肖鹏飞任夷陵区委书记", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026", "confidence": "plausible"},
    # 覃涛（区长）↔ 区政府团队
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长（区委常委兼任）", "overlap_org": "夷陵区人民政府", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长与副区长（区委常委兼任）", "overlap_org": "夷陵区人民政府", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "夷陵区人民政府", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "夷陵区人民政府", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "夷陵区人民政府", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "夷陵区人民政府", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 18, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "夷陵区人民政府", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 19, "type": "superior_subordinate", "context": "区长与挂职副区长", "overlap_org": "夷陵区人民政府", "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 区委常委会内部横向关系
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "同在区委常委会", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "同在区委常委会", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "区委副书记与常委副区长", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "区委副书记与常委副区长", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "同在区委常委会", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 10, "type": "overlap", "context": "同在区委常委会", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 11, "type": "overlap", "context": "同在区委常委会", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 12, "type": "overlap", "context": "同在区委常委会", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 13, "type": "overlap", "context": "同在区委常委会", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 区人大 ↔ 区委
    {"person_a": 20, "person_b": 1, "type": "overlap", "context": "区人大常委会主任与区委书记", "overlap_org": "夷陵区", "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 区政协 ↔ 区委
    {"person_a": 27, "person_b": 1, "type": "overlap", "context": "区政协主席与区委书记", "overlap_org": "夷陵区", "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 副区长之间
    {"person_a": 14, "person_b": 15, "type": "overlap", "context": "同为副区长", "overlap_org": "夷陵区人民政府", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 14, "person_b": 16, "type": "overlap", "context": "同为副区长", "overlap_org": "夷陵区人民政府", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 15, "person_b": 16, "type": "overlap", "context": "同为副区长", "overlap_org": "夷陵区人民政府", "overlap_period": "2026-至今", "confidence": "confirmed"},
    {"person_a": 17, "person_b": 18, "type": "overlap", "context": "同为副区长", "overlap_org": "夷陵区人民政府", "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 前任相关
    {"person_a": 33, "person_b": 1, "type": "predecessor_successor", "context": "肖鹏飞升任宜昌市委常委后，张锴接任夷陵区委书记", "overlap_org": "中共夷陵区委员会", "overlap_period": "2026", "confidence": "plausible"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start_date TEXT,
            end_date TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)
    conn.commit()


def build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 夷陵区人民政府官方网站 (yiling.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace",
              "education", "party_join", "work_start", "current_post",
              "current_org", "source", "notes"]
    for p in persons:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?'] * len(cols_p))})", vals)

    # Insert organizations
    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?'] * len(cols_o))})", vals)

    # Insert positions
    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?'] * len(cols_pos))})", vals)

    # Insert relationships
    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period", "confidence"]
    for r in relationships:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?'] * len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color_and_size(post):
        if "区委书记" in post and "副" not in post and "原" not in post:
            return ("255,50,50", 20.0)  # Red, top leader
        elif "区长" in post and "副" not in post and "原" not in post:
            return ("50,100,255", 20.0)  # Blue
        elif "区委副书记" in post:
            return ("150,50,50", 15.0)  # Dark red
        elif "人大常委会主任" in post:
            return ("200,255,255", 15.0)  # Cyan
        elif "政协主席" in post:
            return ("255,240,200", 15.0)  # Cream
        elif "原" in post or "前任" in post or "原任" in post or "曾" in post:
            return ("150,150,150", 10.0)  # Grey, past
        else:
            return ("100,100,100", 12.0)  # Grey

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,255"),
            "政协": ("255,240,200"),
        }.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络</description>',
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
        c, sz = person_color_and_size(p["current_post"])
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
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    # person → org edges
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person edges
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
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


if __name__ == "__main__":
    build()