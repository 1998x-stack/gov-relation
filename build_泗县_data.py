#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 泗县 leadership network.
Task: anhui_泗县 - 县委书记 & 县长
Province: 安徽省
City: 宿州市
County: 泗县
Generated: 2026-07-15
Sources:
  - https://www.sixian.gov.cn/ldzc/index.html (official leadership page, accessed 2026-07-15)
  - https://www.sixian.gov.cn/content/column/11465673?liId=16661 (杨松涛 profile)
  - https://www.sixian.gov.cn/content/column/11465673?liId=16631 (谢颖锋 profile)
  - https://www.sixian.gov.cn/content/column/11465673?liId=16151 (邱磊 profile)
  - https://www.sixian.gov.cn/content/column/11465673?liId=16161 (冉昊 profile)
  - https://www.sixian.gov.cn/content/column/11465673?liId=16011 (刘朋 profile)
  - https://www.sixian.gov.cn/content/column/11465673?liId=16601 (周志 profile)
  - https://www.sixian.gov.cn/content/column/11465673?liId=16531 (杜煜 profile)
  - https://www.sixian.gov.cn/content/column/11465673?liId=16721 (史肖生 profile)
  - https://www.sixian.gov.cn/content/column/11465673?liId=16381 (江利景 profile)
  - https://www.sixian.gov.cn/content/column/11465673?liId=16731 (刘琪 profile)
  - https://www.sixian.gov.cn/content/column/11465673?liId=15741 (刘培培 profile)
  - https://www.sixian.gov.cn/content/column/11465673?liId=16131 (余浩 profile)
  - https://www.sixian.gov.cn/content/column/11465673?liId=16441 (骆松 profile)
  - https://www.sixian.gov.cn/content/column/11465673?liId=16331 (雷广州 profile)
  - https://www.sixian.gov.cn/public/25072/163926711.html (县政府第45次常务会议)
  - https://www.ahsz.gov.cn/zwzx/zwyw/196452051.html (任东在泗县调研 2026-07-14)
Notes:
  - Current roles confirmed from official gov site (as of 2026-07-15).
  - Biographical details beyond basic info (birth, education) are limited.
  - Predecessor info, cross-county exchange data not available via web search.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
STAGING = BASE
DB_PATH = os.path.join(STAGING, "泗县_network.db")
GEXF_PATH = os.path.join(STAGING, "泗县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════════
    # Core Leaders
    # ═══════════════════════════════════════════════════════════════════
    {"id": 1, "name": "杨松涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年3月", "birthplace": "",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委书记、一级调研员",
     "current_org": "中共泗县委员会",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16661",
     "notes": "主持县委全面工作。1975年3月出生，研究生学历。2026年7月仍在任。频繁出席调研活动（生态环保、防汛备汛、房屋建筑安全等）。",
     "confidence": "confirmed"},

    {"id": 2, "name": "谢颖锋", "gender": "男", "ethnicity": "汉族",
     "birth": "1981年9月", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委副书记、县长",
     "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16631",
     "notes": "领导县政府全面工作。1981年9月出生，大学学历。2026年7月4日主持县政府第45次常务会议。",
     "confidence": "confirmed"},

    # ═══════════════════════════════════════════════════════════════════
    # 县委领导班子
    # ═══════════════════════════════════════════════════════════════════
    {"id": 3, "name": "邱磊", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年6月", "birthplace": "",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委副书记",
     "current_org": "中共泗县委员会",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16151",
     "notes": "协助杨松涛同志抓党的建设工作。1978年6月出生，研究生学历。",
     "confidence": "confirmed"},

    {"id": 4, "name": "冉昊", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年2月", "birthplace": "",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、常务副县长",
     "current_org": "中共泗县委员会",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16161",
     "notes": "负责财政、国资、金融、税务、应急、消防、生态环境、卫健、医保等工作。协助县长分管审计局。1977年2月出生，研究生学历。",
     "confidence": "confirmed"},

    {"id": 5, "name": "桂连成", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、县人武部部长",
     "current_org": "泗县人民武装部",
     "source": "https://www.sixian.gov.cn/ldzc/index.html",
     "notes": "县委常委、县人武部部长。具体出生年月未在公开页面上显示。",
     "confidence": "confirmed"},

    {"id": 6, "name": "刘朋", "gender": "男", "ethnicity": "回族",
     "birth": "1983年9月", "birthplace": "",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、组织部部长",
     "current_org": "中共泗县委员会组织部",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16011",
     "notes": "负责组织部全面工作。1983年9月出生，回族（领导班子中唯一少数民族），研究生学历。",
     "confidence": "confirmed"},

    {"id": 7, "name": "周志", "gender": "男", "ethnicity": "汉族",
     "birth": "1988年10月", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、宣传部部长",
     "current_org": "中共泗县委员会宣传部",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16601",
     "notes": "负责宣传思想文化工作。1988年10月出生，大学学历。领导班子中最年轻的男性常委。",
     "confidence": "confirmed"},

    {"id": 8, "name": "杜煜", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年4月", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、纪委书记、监委主任",
     "current_org": "中共泗县纪律检查委员会",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16531",
     "notes": "负责纪检监察工作和县委巡察工作。1982年4月出生，大学学历。",
     "confidence": "confirmed"},

    {"id": 9, "name": "史肖生", "gender": "男", "ethnicity": "汉族",
     "birth": "1983年2月", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、社工部部长、政法委书记，县政府副县长",
     "current_org": "中共泗县委员会",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16721",
     "notes": "负责政法、信访、自然资源、住建、城管、房产、重点工程、文明创建、石龙湖湿地管理等工作。1983年2月出生，大学学历。",
     "confidence": "confirmed"},

    {"id": 10, "name": "江利景", "gender": "男", "ethnicity": "汉族",
     "birth": "1991年7月", "birthplace": "",
     "education": "研究生学历、管理学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、县政府副县长人选",
     "current_org": "中共泗县委员会",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16381",
     "notes": "负责发改、粮食、统计、工信、科技、招商引资、供电、商务、经济开发区等工作。1991年7月出生，管理学博士。非常年轻的博士领导干部。",
     "confidence": "confirmed"},

    {"id": 11, "name": "刘琪", "gender": "女", "ethnicity": "汉族",
     "birth": "1985年10月", "birthplace": "",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、统战部部长、大庄镇党委书记",
     "current_org": "中共泗县委员会统战部",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16731",
     "notes": "负责统战工作，兼任大庄镇党委书记。1985年10月出生，研究生学历。领导班子中唯一女性常委。",
     "confidence": "confirmed"},

    # ═══════════════════════════════════════════════════════════════════
    # 县政府领导班子（不含已在县委列出的）
    # ═══════════════════════════════════════════════════════════════════
    {"id": 12, "name": "刘培培", "gender": "女", "ethnicity": "汉族",
     "birth": "1984年3月", "birthplace": "",
     "education": "研究生学历",
     "party_join": "致公党党员", "work_start": "",
     "current_post": "泗县副县长",
     "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=15741",
     "notes": "负责人社、市场监管、教育、体育、文旅、广电、融媒体、残联等工作。1984年3月出生，研究生学历，致公党党员。领导班子中唯一非中共党员。",
     "confidence": "confirmed"},

    {"id": 13, "name": "余浩", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年3月", "birthplace": "",
     "education": "大专学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县副县长、县公安局党委书记、局长",
     "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16131",
     "notes": "负责公安、司法、退役军人事务、信访等工作。1978年3月出生，大专学历。",
     "confidence": "confirmed"},

    {"id": 14, "name": "骆松", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年12月", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县副县长",
     "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16441",
     "notes": "负责交通、公路、民政、数据资源、政务服务、公共资源交易等工作。1977年12月出生，大学学历。",
     "confidence": "confirmed"},

    {"id": 15, "name": "雷广州", "gender": "男", "ethnicity": "汉族",
     "birth": "1985年5月", "birthplace": "",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县副县长（挂职）",
     "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16331",
     "notes": "挂职副县长。协助工信、科技、商务、招商引资、乡村振兴、文旅、农业农村等工作。1985年5月出生，研究生学历。",
     "confidence": "confirmed"},

    # ═══════════════════════════════════════════════════════════════════
    # 其他县领导
    # ═══════════════════════════════════════════════════════════════════
    {"id": 16, "name": "陈曦", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泗县人民政府党组成员（推测）",
     "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/public/25072/163926711.html",
     "notes": "出席县政府第45次常务会议（2026年7月4日）的县领导，具体职务待确认，可能为副县长或县政府党组成员。",
     "confidence": "plausible"},

    {"id": 17, "name": "张广洋", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泗县人民政府党组成员（推测）",
     "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/public/25072/163926711.html",
     "notes": "出席县政府第45次常务会议（2026年7月4日）的县领导，具体职务待确认。",
     "confidence": "plausible"},

    {"id": 18, "name": "惠友华", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泗县人大常委会副主任",
     "current_org": "泗县人民代表大会常务委员会",
     "source": "https://www.sixian.gov.cn/public/25072/163926711.html",
     "notes": "县人大常委会副主任。列席县政府第45次常务会议。",
     "confidence": "confirmed"},

    {"id": 19, "name": "王毅", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泗县政协副主席、县水利局局长",
     "current_org": "政协泗县委员会",
     "source": "https://www.sixian.gov.cn/public/25072/163926711.html",
     "notes": "县政协副主席、县水利局局长。列席县政府第45次常务会议。",
     "confidence": "confirmed"},
]

# ── Organizations ────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共泗县委员会", "type": "党委", "level": "县",
     "parent": "中共宿州市委员会", "location": "安徽省宿州市泗县"},
    {"id": 2, "name": "泗县人民政府", "type": "政府", "level": "县",
     "parent": "宿州市人民政府", "location": "安徽省宿州市泗县"},
    {"id": 3, "name": "中共泗县纪律检查委员会", "type": "纪委", "level": "县",
     "parent": "中共宿州市纪律检查委员会", "location": "安徽省宿州市泗县"},
    {"id": 4, "name": "泗县人民代表大会常务委员会", "type": "人大", "level": "县",
     "parent": "宿州市人民代表大会常务委员会", "location": "安徽省宿州市泗县"},
    {"id": 5, "name": "政协泗县委员会", "type": "政协", "level": "县",
     "parent": "政协宿州市委员会", "location": "安徽省宿州市泗县"},
    {"id": 6, "name": "泗县人民武装部", "type": "事业单位", "level": "县",
     "parent": "宿州军分区", "location": "安徽省宿州市泗县"},
    {"id": 7, "name": "中共泗县委员会组织部", "type": "党委", "level": "县",
     "parent": "中共泗县委员会", "location": "安徽省宿州市泗县"},
    {"id": 8, "name": "中共泗县委员会宣传部", "type": "党委", "level": "县",
     "parent": "中共泗县委员会", "location": "安徽省宿州市泗县"},
    {"id": 9, "name": "中共泗县委员会统战部", "type": "党委", "level": "县",
     "parent": "中共泗县委员会", "location": "安徽省宿州市泗县"},
    {"id": 10, "name": "泗县公安局", "type": "政府", "level": "县",
     "parent": "泗县人民政府", "location": "安徽省宿州市泗县"},
]

# ── Positions ────────────────────────────────────────────────────────

positions = [
    # 杨松涛
    {"person_id": 1, "org_id": 1, "title": "泗县县委书记、一级调研员",
     "start": "", "end": "present", "rank": "正县级", "note": "主持县委全面工作"},
    # 谢颖锋
    {"person_id": 2, "org_id": 1, "title": "泗县县委副书记",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "泗县县长",
     "start": "", "end": "present", "rank": "正县级", "note": "领导县政府全面工作"},
    # 邱磊
    {"person_id": 3, "org_id": 1, "title": "泗县县委副书记",
     "start": "", "end": "present", "rank": "副县级",
     "note": "协助杨松涛同志抓党的建设工作"},
    # 冉昊
    {"person_id": 4, "org_id": 1, "title": "泗县县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "泗县常务副县长",
     "start": "", "end": "present", "rank": "副县级",
     "note": "负责财政、金融、应急等工作"},
    # 桂连成
    {"person_id": 5, "org_id": 1, "title": "泗县县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "泗县人武部部长",
     "start": "", "end": "present", "rank": "正团级", "note": ""},
    # 刘朋
    {"person_id": 6, "org_id": 1, "title": "泗县县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "泗县县委组织部部长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 周志
    {"person_id": 7, "org_id": 1, "title": "泗县县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 8, "title": "泗县县委宣传部部长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 杜煜
    {"person_id": 8, "org_id": 1, "title": "泗县县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 3, "title": "泗县纪委书记、监委主任",
     "start": "", "end": "present", "rank": "副县级", "note": "负责纪检监察和巡察工作"},
    # 史肖生
    {"person_id": 9, "org_id": 1, "title": "泗县县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "泗县县委社工部部长、政法委书记",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "泗县副县长",
     "start": "", "end": "present", "rank": "副县级",
     "note": "负责政法、信访、自然资源、住建等工作"},
    # 江利景
    {"person_id": 10, "org_id": 1, "title": "泗县县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "泗县副县长人选",
     "start": "", "end": "present", "rank": "副县级",
     "note": "负责发改、工信、科技、招商、经济开发区等工作"},
    # 刘琪
    {"person_id": 11, "org_id": 1, "title": "泗县县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 9, "title": "泗县县委统战部部长",
     "start": "", "end": "present", "rank": "副县级", "note": "兼任大庄镇党委书记"},
    # 刘培培
    {"person_id": 12, "org_id": 2, "title": "泗县副县长",
     "start": "", "end": "present", "rank": "副县级",
     "note": "负责教育、体育、文旅、市场监管等工作。致公党党员。"},
    # 余浩
    {"person_id": 13, "org_id": 2, "title": "泗县副县长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 10, "title": "泗县公安局党委书记、局长",
     "start": "", "end": "present", "rank": "副县级", "note": "负责公安、司法等工作"},
    # 骆松
    {"person_id": 14, "org_id": 2, "title": "泗县副县长",
     "start": "", "end": "present", "rank": "副县级",
     "note": "负责交通、民政、数据资源等工作"},
    # 雷广州
    {"person_id": 15, "org_id": 2, "title": "泗县副县长（挂职）",
     "start": "", "end": "present", "rank": "副县级",
     "note": "挂职。协助工信、科技、商务、乡村振兴等工作。"},
    # 惠友华
    {"person_id": 18, "org_id": 4, "title": "泗县人大常委会副主任",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 王毅
    {"person_id": 19, "org_id": 5, "title": "泗县政协副主席",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "泗县水利局局长",
     "start": "", "end": "present", "rank": "正科级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────

relationships = [
    # Core 书记-县长
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "杨松涛（县委书记）与谢颖锋（县长）为泗县党政主要领导搭档",
     "overlap_org": "中共泗县委员会/泗县人民政府",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},

    # 书记-专职副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "邱磊作为专职副书记协助杨松涛抓党的建设工作",
     "overlap_org": "中共泗县委员会",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},

    # 县长-常务副县长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "冉昊作为常务副县长协助谢颖锋分管审计局、财政等工作",
     "overlap_org": "泗县人民政府",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},

    # 书记-纪委书记
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "杜煜作为纪委书记在县委领导下负责纪检监察工作",
     "overlap_org": "中共泗县委员会",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},

    # 书记-组织部长
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "刘朋作为组织部部长在县委领导下负责人事组织工作",
     "overlap_org": "中共泗县委员会",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},

    # 书记-政法委书记
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "史肖生陪同杨松涛调研安全生产工作",
     "overlap_org": "中共泗县委员会",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},

    # 所有常委同事关系
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "周志作为县委常委、宣传部部长在杨松涛领导下工作",
     "overlap_org": "中共泗县委员会",
     "overlap_period": "当前", "strength": "medium", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "刘琪作为县委常委、统战部部长在杨松涛领导下工作",
     "overlap_org": "中共泗县委员会",
     "overlap_period": "当前", "strength": "medium", "confidence": "confirmed"},

    # 县长-致公党副县长
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "刘培培作为副县长在谢颖锋领导下分管教育文旅等工作",
     "overlap_org": "泗县人民政府",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},

    # 县长-公安局长
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "余浩作为副县长兼公安局长在谢颖锋领导下工作",
     "overlap_org": "泗县人民政府",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},
]


# ═════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' color string based on role."""
    title = p.get("current_post", "")
    if "县委书记" in title or "书记" in title and "县委" in title:
        return "255,50,50"
    elif "县长" in title or "副县长" in title:
        return "50,100,255"
    elif "纪委书记" in title or "监委" in title:
        return "255,165,0"
    else:
        return "100,100,100"

def is_top_leader(p):
    return p["id"] in [1, 2]

def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
    }
    return colors.get(t, "200,200,200")


# ═════════════════════════════════════════════════════════════════════
# Build SQLite Database
# ═════════════════════════════════════════════════════════════════════

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT,
        source TEXT, notes TEXT, confidence TEXT
    )""")

    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")

    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT,
        rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")

    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        strength TEXT, confidence TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"],
                   p["birth"], p["birthplace"], p["education"],
                   p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"],
                   p["source"], p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"],
                   o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""",
                  (pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
                     VALUES (?,?,?,?,?,?,?,?)""",
                  (r["person_a"], r["person_b"], r["type"],
                   r["context"], r["overlap_org"],
                   r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()

    return f"DB created: {DB_PATH}"


# ═════════════════════════════════════════════════════════════════════
# Build GEXF Graph
# ═════════════════════════════════════════════════════════════════════

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>泗县领导班子工作关系网络 - 含19人、7机构、25任职、10关系</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="education" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="confidence" type="string"/>')
    lines.append('      <attribute id="2" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p).split(",")
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = p.get("current_post", "")
        org = p.get("current_org", "")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("education",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        oc = org_color(o).split(",")
        lines.append(f'        <viz:color r="{oc[0]}" g="{oc[1]}" b="{oc[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Person -> Organization edges (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="confirmed"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person edges (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["confidence"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return f"GEXF created: {GEXF_PATH}"


# ═════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  泗县领导班子关系网络 - 数据生成")
    print("=" * 60)
    print()

    print("[1/2] Building SQLite database...")
    result = build_db()
    print(f"  ✅ {result}")

    print()
    print("[2/2] Building GEXF graph...")
    result = build_gexf()
    print(f"  ✅ {result}")

    print()
    print("─" * 60)
    print(f"  摘要统计")
    print(f"  • 人物: {len(persons)} 人")
    print(f"  • 机构: {len(organizations)} 个")
    print(f"  • 任职: {len(positions)} 条")
    print(f"  • 关系: {len(relationships)} 条")
    print("─" * 60)
    print()
    print("文件位置:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()
