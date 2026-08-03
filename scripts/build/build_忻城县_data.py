#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 忻城县 (Xincheng County, Guangxi) leadership network.

Research date: 2026-08-03
Sources:
  - gxxc.gov.cn (official county government website - leadership pages)
  - baike.baidu.com (覃燕由, 沈国章 individual pages)
  - 163.com news articles (appointment notices)
  - County government leadership division notice (2026-07-29)
"""

import sqlite3
import os
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "忻城县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "忻城县_network.gexf")

# ── DATA ────────────────────────────────────────────────────────────

persons = [
    # ════════════════════════════════════════════════════════════════
    # 1. CURRENT TOP LEADERS — 县委
    # ════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "覃燕由",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1978-02",
        "birthplace": "广西象州县",
        "education": "广西壮族自治区委党校研究生",
        "party_join": "1999-10",
        "work_start": "1997-07",
        "current_post": "忻城县委书记",
        "current_org": "中共忻城县委员会",
        "source": "https://baike.baidu.com/item/%E8%A6%83%E7%87%95%E7%94%B1/19838621"
    },
    {
        "id": 2,
        "name": "李耿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-02",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "忻城县委副书记、代理县长",
        "current_org": "忻城县人民政府",
        "source": "http://www.gxxc.gov.cn/zfxxgk/fdzdgknr/zfld_1/xz/xz.shtml"
    },
    # ════════════════════════════════════════════════════════════════
    # 2. STANDING COMMITTEE 县委常委
    # ════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "覃春富",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "忻城县委副书记",
        "current_org": "中共忻城县委员会",
        "source": "http://www.gxxc.gov.cn/"
    },
    {
        "id": 4,
        "name": "廖珊珊",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "1982-12",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "忻城县委常委、常务副县长",
        "current_org": "忻城县人民政府",
        "source": "http://www.gxxc.gov.cn/zfxxgk/fdzdgknr/zfld_1/fxz/fxz.shtml"
    },
    {
        "id": 5,
        "name": "黄新昌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "忻城县委常委、县纪委书记、县监委主任",
        "current_org": "中共忻城县纪律检查委员会",
        "source": "http://www.gxxc.gov.cn/"
    },
    {
        "id": 6,
        "name": "曹新华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "忻城县委常委",
        "current_org": "中共忻城县委员会",
        "source": "http://www.gxxc.gov.cn/"
    },
    {
        "id": 7,
        "name": "谢立尔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "忻城县委常委",
        "current_org": "中共忻城县委员会",
        "source": "http://www.gxxc.gov.cn/"
    },
    {
        "id": 8,
        "name": "王大振",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "忻城县委常委",
        "current_org": "中共忻城县委员会",
        "source": "http://www.gxxc.gov.cn/"
    },
    {
        "id": 9,
        "name": "范艳红",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "忻城县委常委",
        "current_org": "中共忻城县委员会",
        "source": "http://www.gxxc.gov.cn/"
    },
    {
        "id": 10,
        "name": "袁操",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-08",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "忻城县委常委、统战部部长、副县长",
        "current_org": "中共忻城县委统战部",
        "source": "http://www.gxxc.gov.cn/"
    },
    {
        "id": 11,
        "name": "黄爱柳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "忻城县委常委",
        "current_org": "中共忻城县委员会",
        "source": "http://www.gxxc.gov.cn/"
    },
    # ════════════════════════════════════════════════════════════════
    # 3. GOVERNMENT LEADERS — 副县长 (非县委常委)
    # ════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "谢启凡",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1990-05",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "忻城县副县长",
        "current_org": "忻城县人民政府",
        "source": "http://www.gxxc.gov.cn/zfxxgk/fdzdgknr/zfld_1/fxz/fxz.shtml"
    },
    {
        "id": 13,
        "name": "韦松婷",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "1986-11",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "忻城县副县长",
        "current_org": "忻城县人民政府",
        "source": "http://www.gxxc.gov.cn/zfxxgk/fdzdgknr/zfld_1/fxz/fxz.shtml"
    },
    {
        "id": 14,
        "name": "陆华",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1978-11",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "忻城县副县长、县公安局局长",
        "current_org": "忻城县公安局",
        "source": "http://www.gxxc.gov.cn/zfxxgk/fdzdgknr/zfld_1/fxz/fxz.shtml"
    },
    {
        "id": 15,
        "name": "肖玉周",
        "gender": "女",
        "ethnicity": "瑶族",
        "birth": "1989-03",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "忻城县副县长",
        "current_org": "忻城县人民政府",
        "source": "http://www.gxxc.gov.cn/zfxxgk/fdzdgknr/zfld_1/fxz/fxz.shtml"
    },
    # ════════════════════════════════════════════════════════════════
    # 4. 挂职 LEADERS
    # ════════════════════════════════════════════════════════════════
    {
        "id": 16,
        "name": "王溪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-07",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "忻城县委常委（挂职）、副县长（定点帮扶）",
        "current_org": "忻城县人民政府",
        "source": "http://www.gxxc.gov.cn/"
    },
    {
        "id": 17,
        "name": "吴小红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973-07",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "忻城县委常委（挂职）、副县长（粤桂协作）",
        "current_org": "忻城县人民政府",
        "source": "http://www.gxxc.gov.cn/"
    },
    {
        "id": 18,
        "name": "吴玉龙",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1984-03",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "忻城县副县长（挂职，驻村工作队队长）",
        "current_org": "忻城县人民政府",
        "source": "http://www.gxxc.gov.cn/"
    },
    # ════════════════════════════════════════════════════════════════
    # 5. PREDECESSORS
    # ════════════════════════════════════════════════════════════════
    {
        "id": 19,
        "name": "韦猛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "来宾市委副秘书长（正处长级）、二级巡视员",
        "current_org": "中共来宾市委员会",
        "source": "https://www.163.com/dy/article/GFBOIC4305527KD9.html"
    },
    {
        "id": 20,
        "name": "沈国章",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-07",
        "birthplace": "江苏淮安",
        "education": "清华大学热能工程系博士",
        "party_join": "2005-05",
        "work_start": "2011-07",
        "current_post": "来宾市市场监督管理局党组书记、局长",
        "current_org": "来宾市市场监督管理局",
        "source": "https://baike.baidu.com/item/%E6%B2%88%E5%9B%BD%E7%AB%A0/1333649"
    },
    # ════════════════════════════════════════════════════════════════
    # 6. OTHER LEADERS
    # ════════════════════════════════════════════════════════════════
    {
        "id": 21,
        "name": "樊广平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "忻城县人大常委会主任",
        "current_org": "忻城县人大常委会",
        "source": "https://baike.baidu.com/item/%E5%BF%BB%E5%9F%8E%E5%8E%BF/7180951"
    },
    {
        "id": 22,
        "name": "卢玉容",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "忻城县政协主席",
        "current_org": "忻城县政协",
        "source": "http://www.gxxc.gov.cn/"
    },
    # ════════════════════════════════════════════════════════════════
    # 7. DISCIPLINE COMMISSION STANDING
    # ════════════════════════════════════════════════════════════════
    {
        "id": 23,
        "name": "谭克飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "忻城县纪委副书记",
        "current_org": "中共忻城县纪律检查委员会",
        "source": "http://www.gxxc.gov.cn/"
    },
    {
        "id": 24,
        "name": "黄敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "忻城县纪委副书记",
        "current_org": "中共忻城县纪律检查委员会",
        "source": "http://www.gxxc.gov.cn/"
    },
]

organizations = [
    {"id": 1, "name": "中共忻城县委员会", "type": "党委", "level": "县级",
     "parent": "中共来宾市委员会", "location": "广西来宾市忻城县"},
    {"id": 2, "name": "忻城县人民政府", "type": "政府", "level": "县级",
     "parent": "来宾市人民政府", "location": "广西来宾市忻城县"},
    {"id": 3, "name": "中共忻城县纪律检查委员会", "type": "纪委", "level": "县级",
     "parent": "中共来宾市纪律检查委员会", "location": "广西来宾市忻城县"},
    {"id": 4, "name": "忻城县人大常委会", "type": "人大", "level": "县级",
     "parent": "来宾市人大常委会", "location": "广西来宾市忻城县"},
    {"id": 5, "name": "忻城县政协", "type": "政协", "level": "县级",
     "parent": "来宾市政协", "location": "广西来宾市忻城县"},
    {"id": 6, "name": "忻城县公安局", "type": "政府", "level": "县级",
     "parent": "忻城县人民政府", "location": "广西来宾市忻城县"},
    {"id": 7, "name": "中共忻城县委统战部", "type": "党委", "level": "县级",
     "parent": "中共忻城县委员会", "location": "广西来宾市忻城县"},
    # Predecessor orgs
    {"id": 8, "name": "来宾市林业局", "type": "政府", "level": "地级",
     "parent": "来宾市人民政府", "location": "广西来宾市"},
    {"id": 9, "name": "来宾市自然资源局", "type": "政府", "level": "地级",
     "parent": "来宾市人民政府", "location": "广西来宾市"},
    {"id": 10, "name": "中共武宣县委员会", "type": "党委", "level": "县级",
     "parent": "中共来宾市委员会", "location": "广西来宾市武宣县"},
    {"id": 11, "name": "中共来宾市委员会", "type": "党委", "level": "地级",
     "parent": "中共广西壮族自治区委员会", "location": "广西来宾市"},
    {"id": 12, "name": "来宾市人民政府", "type": "政府", "level": "地级",
     "parent": "广西壮族自治区人民政府", "location": "广西来宾市"},
    {"id": 13, "name": "来宾市市场监督管理局", "type": "政府", "level": "地级",
     "parent": "来宾市人民政府", "location": "广西来宾市"},
]

positions = [
    # ── Current appointments ──
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2026-07", "end_date": "present",
     "rank": "正处级", "note": "2026年6月任前公示，7月正式任职"},
    {"person_id": 2, "org_id": 2, "title": "副县长、代理县长", "start_date": "2026-07", "end_date": "present",
     "rank": "正处级", "note": "县委副书记、县人民政府党组书记、代理县长"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "同时担任副县长"},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 6, "title": "县公安局局长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "兼职"},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present",
     "rank": "", "note": "定点帮扶挂职"},
    {"person_id": 17, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present",
     "rank": "", "note": "粤桂协作挂职"},
    {"person_id": 18, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present",
     "rank": "", "note": "驻村工作队挂职"},
    {"person_id": 21, "org_id": 4, "title": "县人大常委会主任", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": ""},
    {"person_id": 22, "org_id": 5, "title": "县政协主席", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": ""},
    {"person_id": 23, "org_id": 3, "title": "县纪委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 24, "org_id": 3, "title": "县纪委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},

    # ── Predecessors' current positions ──
    {"person_id": 19, "org_id": 11, "title": "市委副秘书长", "start_date": "2026-07", "end_date": "present",
     "rank": "正处级", "note": "原忻城县委书记（2021.07-2026.06）"},
    {"person_id": 20, "org_id": 13, "title": "市场监督管理局党组书记、局长", "start_date": "2026-07", "end_date": "present",
     "rank": "正处级", "note": "原忻城县长（2021.08-2026.07）"},
]

relationships = [
    # ── Party Secretary ↔ County Magistrate (working pair) ──
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记与代理县长", "overlap_org": "忻城县",
     "overlap_period": "2026-07至今"},
    # ── Party Secretary ↔ Deputy Secretary (领导集体) ──
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记与县委副书记", "overlap_org": "中共忻城县委员会",
     "overlap_period": "2026-07至今"},
    # ── 县长（现任）↔ Executive Deputy Magistrate ──
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "县长与常务副县长", "overlap_org": "忻城县人民政府",
     "overlap_period": "2026-07至今"},
    # ── County Leadership (standing committee) overlaps ──
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "县委书记主导的常委班子",
     "overlap_org": "中共忻城县委员会", "overlap_period": "2026-07至今"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "县委常委会成员",
     "overlap_org": "中共忻城县委员会", "overlap_period": "2026-07至今"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "县委常委会成员",
     "overlap_org": "中共忻城县委员会", "overlap_period": "2026-07至今"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "县委常委会成员",
     "overlap_org": "中共忻城县委员会", "overlap_period": "2026-07至今"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "县委常委会成员",
     "overlap_org": "中共忻城县委员会", "overlap_period": "2026-07至今"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "县委常委会成员",
     "overlap_org": "中共忻城县委员会", "overlap_period": "2026-07至今"},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "县委常委会成员",
     "overlap_org": "中共忻城县委员会", "overlap_period": "2026-07至今"},
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "县委常委会成员",
     "overlap_org": "中共忻城县委员会", "overlap_period": "2026-07至今"},
    # ── Government team overlaps ──
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "县长与副县长",
     "overlap_org": "忻城县人民政府", "overlap_period": "2026-07至今"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "县长与副县长",
     "overlap_org": "忻城县人民政府", "overlap_period": "2026-07至今"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "县长与公安局长",
     "overlap_org": "忻城县人民政府", "overlap_period": "2026-07至今"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "县长与副县长",
     "overlap_org": "忻城县人民政府", "overlap_period": "2026-07至今"},
    # ── Predecessor-Successor ──
    {"person_a": 19, "person_b": 1, "type": "前后任", "context": "原任忻城县委书记与现任县委书记",
     "overlap_org": "中共忻城县委员会", "overlap_period": "2021.07-2026.07（前任）→ 2026.07至今（现任）"},
    {"person_a": 20, "person_b": 2, "type": "前后任", "context": "原忻城县长与现任代理县长",
     "overlap_org": "忻城县人民政府", "overlap_period": "2021.08-2026.07（前任）→ 2026.07至今（现任）"},
    # ── 覃燕由 ↔ 沈国章 (曾共事) ──
    {"person_a": 1, "person_b": 20, "type": "共事", "context": "覃燕由任县委书记时沈国章担任县长",
     "overlap_org": "忻城县", "overlap_period": "2026.07"},

    # ── 韦猛 ↔ 沈国章 (老搭档: 韦猛忻城县委书记任上沈国章任县长) ──
    {"person_a": 19, "person_b": 20, "type": "共事", "context": "韦猛任县委书记时沈国章任县长",
     "overlap_org": "忻城县", "overlap_period": "2021.08-2026.06"},
    # ── 韦猛 ↔ 李耿 (韦猛任书记时李耿任政府领导) ──
    {"person_a": 19, "person_b": 2, "type": "共事", "context": "韦猛任县委书记时李耿进入县政府班子",
     "overlap_org": "忻城县", "overlap_period": "2026"},
]


# ── BUILD ───────────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build():
    # ── SQLite ──
    import sys
    repo_root = REPO_ROOT
    sys.path.insert(0, repo_root)
    from gov_relation.schema import create_tables, insert_persons, insert_organizations, insert_positions, insert_relationships

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn, overwrite=True)
    insert_persons(conn, persons)
    insert_organizations(conn, organizations)
    insert_positions(conn, positions)
    insert_relationships(conn, relationships)
    conn.close()
    print(f"Database created: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")

    # ── GEXF graph ──
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>忻城县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="gender" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="5" title="birth" type="string"/>')
    lines.append('      <attribute id="6" title="source" type="string"/>')
    lines.append('      <attribute id="7" title="org_type" type="string"/>')
    lines.append('      <attribute id="8" title="level" type="string"/>')
    lines.append('      <attribute id="9" title="location" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    def person_color(current_post):
        if "书记" in current_post and "纪委" not in current_post and "副" not in current_post:
            return "200,30,30"  # 红色 — 一把手
        if "县长" in current_post or "副县长" in current_post:
            if "常务" in current_post:
                return "50,100,255"  # 深蓝 — 常务副县长
            return "30,100,200"  # 蓝色 — 政府
        if "纪委" in current_post or "监委" in current_post:
            return "255,165,0"  # 橙色 — 纪检
        if "副" in current_post or "副书记" in current_post:
            return "100,150,220"  # 浅蓝 — 副职
        if "常委" in current_post:
            return "180,100,180"  # 紫色 — 常委
        if "人大" in current_post:
            return "60,180,60"  # 绿色
        if "政协" in current_post:
            return "60,180,60"  # 绿色
        return "100,100,100"  # 灰色

    def org_color(org_type):
        m = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
             "政协": "255,240,200", "纪委": "255,200,150"}
        return m.get(org_type, "200,200,200")

    def node_sz(current_post):
        if "书记" in current_post and "纪委" not in current_post and "副" not in current_post:
            return "20.0"
        elif "县长" in current_post:
            return "20.0"
        elif "副" in current_post or "常委" in current_post:
            return "12.0"
        else:
            return "12.0"

    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        c = person_color(p.get("current_post", ""))
        sz = node_sz(p.get("current_post", ""))
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("gender",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("ethnicity",""))}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        cs = c.split(",")
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        oid = o["id"] + 100000
        c = org_color(o.get("type", ""))
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="7" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="8" value="{esc(o.get("level",""))}"/>')
        lines.append(f'          <attvalue for="9" value="{esc(o.get("location",""))}"/>')
        lines.append('        </attvalues>')
        cs = c.split(",")
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # person→organization edges
    for pos in positions:
        eid += 1
        pid = pos["person_id"]
        oid = pos["org_id"] + 100000
        title = pos.get("title", "")
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("start_date","") + "-" + pos.get("end_date",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person↔person edges
    for rel in relationships:
        eid += 1
        pa = rel["person_a"]
        pb = rel["person_b"]
        lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(rel["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(rel.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH} ({len(persons)} person nodes, {len(organizations)} org nodes, {eid} edges)")


if __name__ == "__main__":
    build()