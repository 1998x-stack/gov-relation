#!/usr/bin/env python3
"""Build Huoshan County (霍山县) leadership network database and GEXF graph.

Targets: 县委书记罗文, 县长刘瀚宇
Research date: 2026-07-15
Sources:
  - www.ahhuoshan.gov.cn (official county government website, leadership page, accessed 2026-07-15)
  - 中国共产党霍山县第十六次代表大会 (2026-06-23)
  - 中国共产党霍山县第十六届委员会第一次全体会议 (2026-06-24)
  - 霍山县"两优一先"表彰大会 (2026-07-01)
  - 霍山县人民政府领导之窗 (县政府领导分工页面)
  - www.luan.gov.cn (六安市领导之窗)

Confidence: Current roles confirmed from official government leadership page and news.
  Party Standing Committee roster confirmed from 16th County Party Congress results.
  Biographical details for some figures are partial where noted.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "霍山县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "霍山县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ 1. Party Secretary (县委书记) ═══════════════════════════════════
    {
        "id": 1,
        "name": "罗文",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共霍山县委员会",
        "source": "https://www.ahhuoshan.gov.cn/zwzx/jrhs/38814717.html (2026-07-01 表彰大会); https://www.ahhuoshan.gov.cn/zwzx/jrhs/38811627.html (2026-06-24 十六届一次全会选举)",
        "notes": "罗文，现任霍山县委书记。2026年6月24日在中共霍山县第十六届委员会第一次全体会议上当选县委书记。主持县委全面工作。此前为霍山县委副书记、县长（第十五届县委），并代表第十五届县委在第十六次党代会上作报告。",
        "confidence": "confirmed"
    },
    # ═══ 2. County Magistrate (县长) ═══════════════════════════════════
    {
        "id": 2,
        "name": "刘瀚宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-09",
        "birthplace": "安徽金寨",
        "native_place": "安徽金寨",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "2009-08",
        "current_post": "县委副书记、县长",
        "current_org": "霍山县人民政府",
        "source": "https://www.ahhuoshan.gov.cn/content/column/6786701?liId=680 (霍山县政府领导之窗); https://www.ahhuoshan.gov.cn/zwzx/jrhs/38811627.html (2026-06-24 十六届一次全会当选县委副书记)",
        "notes": "刘瀚宇，男，汉族，1986年9月出生，安徽金寨人，省委党校研究生学历，2009年8月参加工作，2008年6月加入中国共产党。现任霍山县委副书记、县政府党组书记、县长。领导县政府全面工作，负责审计工作，分管县审计局。",
        "confidence": "confirmed"
    },
    # ═══ 3. Deputy Party Secretary (县委副书记) ════════════════════════
    {
        "id": 3,
        "name": "黄维",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共霍山县委员会",
        "source": "https://www.ahhuoshan.gov.cn/zwzx/jrhs/38811627.html (2026-06-24 十六届一次全会当选县委副书记); https://www.ahhuoshan.gov.cn/zwzx/jrhs/38814717.html (2026-07-01 参加表彰大会)",
        "notes": "黄维，2026年6月24日在中共霍山县第十六届委员会第一次全体会议上当选县委副书记。",
        "confidence": "confirmed"
    },
    # ═══ 4. Standing Committee Members (县委常委) ═══════════════════════
    {
        "id": 4,
        "name": "郝晓武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共霍山县委员会",
        "source": "https://www.ahhuoshan.gov.cn/zwzx/jrhs/38811627.html (2026-06-24 十六届一次全会当选常委)",
        "notes": "霍山县委常委。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "朱静",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共霍山县委员会",
        "source": "https://www.ahhuoshan.gov.cn/zwzx/jrhs/38811627.html (2026-06-24 十六届一次全会当选常委)",
        "notes": "霍山县委常委。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "贺新建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共霍山县委员会",
        "source": "https://www.ahhuoshan.gov.cn/zwzx/jrhs/38811627.html (2026-06-24 十六届一次全会当选常委)",
        "notes": "霍山县委常委。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "王翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-02",
        "birthplace": "安徽太湖",
        "native_place": "安徽太湖",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "2006-07",
        "current_post": "县委常委、常务副县长",
        "current_org": "霍山县人民政府",
        "source": "https://www.ahhuoshan.gov.cn/content/column/6786701?liId=691 (霍山县政府领导之窗); https://www.ahhuoshan.gov.cn/zwzx/jrhs/38811627.html (2026-06-24 十六届一次全会当选常委)",
        "notes": "王翔，男，汉族，1985年2月出生，安徽太湖县人，省委党校研究生学历，2006年7月参加工作，2012年6月加入中国共产党。县委常委、县政府党组副书记、常务副县长。负责县政府常务工作，分管发展改革、应急管理、财政税收、自然资源、住建等。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "程业清",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共霍山县委员会",
        "source": "https://www.ahhuoshan.gov.cn/zwzx/jrhs/38811627.html (2026-06-24 十六届一次全会当选常委)",
        "notes": "霍山县委常委。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "熊登林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共霍山县委员会",
        "source": "https://www.ahhuoshan.gov.cn/zwzx/jrhs/38811627.html (2026-06-24 十六届一次全会当选常委)",
        "notes": "霍山县委常委。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "冯梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共霍山县委员会",
        "source": "https://www.ahhuoshan.gov.cn/zwzx/jrhs/38811627.html (2026-06-24 十六届一次全会当选常委); https://www.ahhuoshan.gov.cn/zwzx/jrhs/38814717.html (2026-07-01 宣读表彰决定)",
        "notes": "霍山县委常委。在2026年7月1日表彰大会上宣读表彰决定。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "吕开胜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共霍山县委员会",
        "source": "https://www.ahhuoshan.gov.cn/zwzx/jrhs/38811627.html (2026-06-24 十六届一次全会当选常委)",
        "notes": "霍山县委常委。",
        "confidence": "confirmed"
    },
    # ═══ 5. County Government Deputies (非常委副县长) ════════════════════
    {
        "id": 12,
        "name": "李文龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-03",
        "birthplace": "安徽霍山",
        "native_place": "安徽霍山",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "2007-10",
        "current_post": "副县长",
        "current_org": "霍山县人民政府",
        "source": "https://www.ahhuoshan.gov.cn/content/column/6786701?liId=736 (霍山县政府领导之窗)",
        "notes": "李文龙，男，汉族，1985年3月出生，安徽霍山人，大学学历，2007年10月参加工作，2009年7月加入中国共产党。县政府党组成员、副县长。负责市场监管、生态环境、林业、农业农村、乡村振兴、中药产业等。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "汪海波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-10",
        "birthplace": "安徽六安",
        "native_place": "安徽六安",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1996-12",
        "current_post": "副县长、县公安局局长",
        "current_org": "霍山县人民政府",
        "source": "https://www.ahhuoshan.gov.cn/content/column/6786701?liId=675 (霍山县政府领导之窗)",
        "notes": "汪海波，男，汉族，1979年10月出生，安徽六安人，大学学历，1996年12月参加工作，2000年4月加入中国共产党。县政府党组成员、副县长，县公安局党委书记、局长、督察长。负责公安、司法、信访、退役军人事务、城管等。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "冯彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989-06",
        "birthplace": "安徽六安",
        "native_place": "安徽六安",
        "education": "大学，管理学学士",
        "party_join": "中共党员",
        "work_start": "2011-10",
        "current_post": "副县长",
        "current_org": "霍山县人民政府",
        "source": "https://www.ahhuoshan.gov.cn/content/column/6786701?liId=683 (霍山县政府领导之窗)",
        "notes": "冯彬，男，汉族，1989年6月出生，安徽六安人，大学学历，管理学学士，2011年10月参加工作，2009年12月加入中国共产党。县政府党组成员、副县长。负责交通运输、人社、民政、商贸流通等。",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "张晓杰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-02",
        "birthplace": "安徽霍山",
        "native_place": "安徽霍山",
        "education": "大学",
        "party_join": "民建会员",
        "work_start": "2001-08",
        "current_post": "副县长",
        "current_org": "霍山县人民政府",
        "source": "https://www.ahhuoshan.gov.cn/content/column/6786701?liId=733 (霍山县政府领导之窗)",
        "notes": "张晓杰，女，汉族，1977年2月出生，安徽霍山人，大学学历，2001年8月参加工作，民建会员。县政府副县长（非中共党员）。负责卫生健康、医保、教育、文化、旅游、体育、广播电视等。",
        "confidence": "confirmed"
    },
    {
        "id": 16,
        "name": "程亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-12",
        "birthplace": "安徽霍山",
        "native_place": "安徽霍山",
        "education": "本科，理学学士",
        "party_join": "中共党员",
        "work_start": "1998-07",
        "current_post": "副县长、大化坪镇党委书记",
        "current_org": "霍山县人民政府",
        "source": "https://www.ahhuoshan.gov.cn/content/column/6786701?liId=686 (霍山县政府领导之窗)",
        "notes": "程亮，男，汉族，安徽霍山人，本科学历、理学学士，1981年12月出生，1998年7月参加工作，2002年10月加入中国共产党。县政府党组成员、副县长，大化坪镇党委书记。",
        "confidence": "confirmed"
    },
    # ═══ 6. 人大/政协主要领导人 (从新闻推断) ═══════════════════════════
    {
        "id": 17,
        "name": "张润之",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席（推测）",
        "current_org": "政协霍山县委员会",
        "source": "https://www.ahhuoshan.gov.cn/zwzx/jrhs/38814717.html (2026-07-01 参加表彰大会); https://www.ahhuoshan.gov.cn/zwzx/jrhs/38811199.html (2026-06-23 十六次党代会主席台就座)",
        "notes": "张润之，多次在县重要会议主席台前排就座，位列罗文、刘瀚宇之后，推测为县人大或政协主要领导。在县党代会主席台前排就座的有：罗文、刘瀚宇、张润之、李传江、黄维...",
        "confidence": "plausible"
    },
    {
        "id": 18,
        "name": "李传江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任（推测）",
        "current_org": "霍山县人民代表大会常务委员会",
        "source": "https://www.ahhuoshan.gov.cn/zwzx/jrhs/38814717.html (2026-07-01 参加表彰大会); https://www.ahhuoshan.gov.cn/zwzx/jrhs/38811199.html (2026-06-23 十六次党代会主席台就座)",
        "notes": "李传江，多次在县重要会议主席台前排就座，推测为县人大或政协主要领导。",
        "confidence": "plausible"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共霍山县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共六安市委",
        "location": "安徽省六安市霍山县"
    },
    {
        "id": 2,
        "name": "霍山县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "六安市人民政府",
        "location": "安徽省六安市霍山县"
    },
    {
        "id": 3,
        "name": "霍山县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "",
        "location": "安徽省六安市霍山县"
    },
    {
        "id": 4,
        "name": "政协霍山县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "",
        "location": "安徽省六安市霍山县"
    },
    {
        "id": 5,
        "name": "霍山县公安局",
        "type": "政府",
        "level": "科级",
        "parent": "霍山县人民政府",
        "location": "安徽省六安市霍山县"
    },
    {
        "id": 6,
        "name": "大化坪镇",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "霍山县人民政府",
        "location": "安徽省六安市霍山县大化坪镇"
    },
]

positions = [
    # 罗文
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2026-06", "end": "present", "rank": "县处级正职", "note": "2026年6月24日在十六届一次全会上当选县委书记"},
    {"person_id": 1, "org_id": 1, "title": "县委副书记、县长", "start": "unknown", "end": "2026-06", "rank": "县处级正职", "note": "此前为霍山县委副书记、县长；代表第十五届县委作报告"},
    # 刘瀚宇
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "2026-06", "end": "present", "rank": "县处级正职", "note": "2026年6月24日当选县委副书记；县政府党组书记、县长"},
    # 黄维
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": "2026年6月24日当选县委副书记"},
    # 郝晓武
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": ""},
    # 朱静
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": ""},
    # 贺新建
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": ""},
    # 王翔
    {"person_id": 7, "org_id": 2, "title": "县委常委、常务副县长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "县政府党组副书记"},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": ""},
    # 程业清
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": ""},
    # 熊登林
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": ""},
    # 冯梅
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": ""},
    # 吕开胜
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": ""},
    # 李文龙
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "县政府党组成员"},
    # 汪海波
    {"person_id": 13, "org_id": 2, "title": "副县长、县公安局局长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "县政府党组成员，县公安局党委书记、局长、督察长"},
    {"person_id": 13, "org_id": 5, "title": "党委书记、局长", "start": "unknown", "end": "present", "rank": "乡科级正职", "note": ""},
    # 冯彬
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "县政府党组成员"},
    # 张晓杰
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "非中共党员（民建会员）"},
    # 程亮
    {"person_id": 16, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "县政府党组成员"},
    {"person_id": 16, "org_id": 6, "title": "大化坪镇党委书记", "start": "unknown", "end": "present", "rank": "乡科级正职", "note": "兼任"},
    # 张润之（推测政协主席）
    {"person_id": 17, "org_id": 4, "title": "县政协主席（推测）", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "推测职务，从会议主席台排位推断"},
    # 李传江（推测人大主任）
    {"person_id": 18, "org_id": 3, "title": "县人大常委会主任（推测）", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "推测职务，从会议主席台排位推断"},
]

relationships = [
    # 县委班子工作关系
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭档", "overlap_org": "中共霍山县委员会", "overlap_period": "2026-06至今", "strength": "strong"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与副书记搭档", "overlap_org": "中共霍山县委员会", "overlap_period": "2026-06至今", "strength": "strong"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "同为县委副书记", "overlap_org": "中共霍山县委员会", "overlap_period": "2026-06至今", "strength": "strong"},
    # 县政府班子
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "霍山县人民政府", "overlap_period": "当前", "strength": "strong"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "霍山县人民政府", "overlap_period": "当前", "strength": "medium"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长与副县长（公安）", "overlap_org": "霍山县人民政府", "overlap_period": "当前", "strength": "medium"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "霍山县人民政府", "overlap_period": "当前", "strength": "medium"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "霍山县人民政府", "overlap_period": "当前", "strength": "medium"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "霍山县人民政府", "overlap_period": "当前", "strength": "medium"},
    # 县委常委之间
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共霍山县委员会", "overlap_period": "2026-06至今", "strength": "medium"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共霍山县委员会", "overlap_period": "2026-06至今", "strength": "medium"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共霍山县委员会", "overlap_period": "2026-06至今", "strength": "medium"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共霍山县委员会", "overlap_period": "2026-06至今", "strength": "medium"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共霍山县委员会", "overlap_period": "2026-06至今", "strength": "medium"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共霍山县委员会", "overlap_period": "2026-06至今", "strength": "medium"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共霍山县委员会", "overlap_period": "2026-06至今", "strength": "medium"},
    # 罗文与人大政协领导
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "县委与政协领导", "overlap_org": "霍山县", "overlap_period": "当前", "strength": "weak"},
    {"person_a": 1, "person_b": 18, "type": "overlap", "context": "县委与人大领导", "overlap_org": "霍山县", "overlap_period": "当前", "strength": "weak"},
    # 刘瀚宇与人大政协领导
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "县政府与政协领导", "overlap_org": "霍山县", "overlap_period": "当前", "strength": "weak"},
    {"person_a": 2, "person_b": 18, "type": "overlap", "context": "县政府与人大领导", "overlap_org": "霍山县", "overlap_period": "当前", "strength": "weak"},
    # 同乡关系
    {"person_a": 13, "person_b": 14, "type": "same_native_place", "context": "同为六安人", "overlap_org": "", "overlap_period": "", "strength": "weak"},
    {"person_a": 12, "person_b": 15, "type": "same_native_place", "context": "同为霍山人", "overlap_org": "", "overlap_period": "", "strength": "weak"},
    {"person_a": 12, "person_b": 16, "type": "same_native_place", "context": "同为霍山人", "overlap_org": "", "overlap_period": "", "strength": "weak"},
]


# ── SQLite ────────────────────────────────────────────────────────────────

def create_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT, current_org TEXT,
        source TEXT, notes TEXT, confidence TEXT
    )""")

    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")

    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")

    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT, strength TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["native_place"], p["education"],
                   p["party_join"], p["work_start"], p["current_post"],
                   p["current_org"], p["source"], p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""",
                  (pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength)
                     VALUES (?,?,?,?,?,?,?)""",
                  (r["person_a"], r["person_b"], r["type"], r["context"],
                   r["overlap_org"], r["overlap_period"], r["strength"]))

    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")


# ── GEXF ──────────────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def is_top_leader(pid):
    return pid in (1, 2)

def is_party_sec(pid):
    return pid == 1

def is_magistrate(pid):
    return pid == 2

def person_color(p):
    pid = p["id"]
    if is_party_sec(pid):
        return "255,50,50"
    if is_magistrate(pid):
        return "50,100,255"
    # Check if discipline related
    return "100,100,100"

def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
    }
    return colors.get(t, "200,200,200")

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China-Gov-Network Research Agent</creator>')
    lines.append('    <description>霍山县领导班子工作关系网络 — 县委书记罗文, 县长刘瀚宇</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        c = person_color(p)
        sz = "20.0" if is_top_leader(pid) else ("16.0" if pid in (3, 17, 18) else "12.0")
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        cs = c.split(",")
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        cs = oc.split(",")
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    # Person->Organization (worked_at)
    for pos in positions:
        eid += 1
        w = "2.0" if pos["rank"] == "县处级正职" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{pos["start"]} 至 {pos["end"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person->Person (relationship)
    for r in relationships:
        eid += 1
        w = "3.0" if r["strength"] == "strong" else ("2.0" if r["strength"] == "medium" else "1.0")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")


# ── main ──────────────────────────────────────────────────────────────────

def main():
    print("=== 霍山县 Leadership Network ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    create_db()
    create_gexf()
    print("Done.")

if __name__ == "__main__":
    main()
