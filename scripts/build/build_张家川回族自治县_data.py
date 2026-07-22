#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 张家川回族自治县, 天水市, 甘肃省.

张家川回族自治县 — 甘肃省天水市下辖自治县, 位于天水市东北部,
是甘肃省唯一回族自治县.

Current leadership as of 2026-07:
  - 何敬忠 (县委书记)
  - 马杰 (县委副书记、县长, appointed acting mayor 2026-01-27)

Reference sources:
  - 张家川县人民政府官网领导之窗: https://www.zjc.gov.cn/ldzc1/ldjj.htm
  - 县委领导页: https://www.zjc.gov.cn/ldzc1/x_w_l_d.htm
  - 县政府领导页: https://www.zjc.gov.cn/ldzc1/xzfld.htm
  - 县人大领导页: https://www.zjc.gov.cn/ldzc1/xrdld.htm
  - 县政协领导页: https://www.zjc.gov.cn/ldzc1/xzxld.htm
  - 马杰代理县长决定: https://www.zjc.gov.cn/info/1821/1345752.htm
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/gansu_张家川回族自治县")
os.makedirs(TMP, exist_ok=True)

DB_PATH = os.path.join(TMP, "张家川回族自治县_network.db")
GEXF_PATH = os.path.join(TMP, "张家川回族自治县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════
    # CURRENT TOP LEADERS
    # ═══════════════════════════════════════════════════════════

    # 何敬忠 — 张家川县委书记 (as of 2026-07)
    {"id": 1, "name": "何敬忠", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-10", "birthplace": "",
     "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县委书记",
     "current_org": "中共张家川县委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/xwsj_hjz.htm"},

    # 马杰 — 张家川县委副书记、县长 (as of 2026-07)
    {"id": 2, "name": "马杰", "gender": "男", "ethnicity": "回族",
     "birth": "1984-04", "birthplace": "",
     "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县委副书记、县长",
     "current_org": "张家川县人民政府",
     "source": "https://www.zjc.gov.cn/ldzc1/xz_mj.htm; 2026-01-27任代县长 https://www.zjc.gov.cn/info/1821/1345752.htm"},

    # ═══════════════════════════════════════════════════════════
    # 县委领导 (Party Committee Leadership)
    # ═══════════════════════════════════════════════════════════

    # 刘润斌 — 县委副书记（专职）
    {"id": 3, "name": "刘润斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-03", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县委副书记（专职）",
     "current_org": "中共张家川县委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/x_w_l_d.htm"},

    # 赵亮 — 县委常委、宣传部部长
    {"id": 4, "name": "赵亮", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-05", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县委常委、宣传部部长",
     "current_org": "中共张家川县委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/x_w_l_d.htm"},

    # 薛天胜 — 县委常委、政法委书记
    {"id": 5, "name": "薛天胜", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-07", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县委常委、政法委书记",
     "current_org": "中共张家川县委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/x_w_l_d.htm"},

    # 王浩 — 县委常委、纪委书记、县监委主任
    {"id": 6, "name": "王浩", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-05", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县委常委、纪委书记、县监委主任",
     "current_org": "中共张家川县纪律检查委员会/张家川县监察委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/x_w_l_d.htm"},

    # 王志杰 — 县委常委、常务副县长
    {"id": 7, "name": "王志杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-06", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县委常委、常务副县长",
     "current_org": "中共张家川县委员会/张家川县人民政府",
     "source": "https://www.zjc.gov.cn/ldzc1/x_w_l_d.htm; https://www.zjc.gov.cn/ldzc1/xzfld.htm"},

    # 赵燚 — 县委常委、副县长（挂职）
    {"id": 8, "name": "赵燚", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-07", "birthplace": "",
     "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县委常委、副县长（挂职）",
     "current_org": "中共张家川县委员会/张家川县人民政府",
     "source": "https://www.zjc.gov.cn/ldzc1/x_w_l_d.htm"},

    # 马永平 — 县委常委、副县长
    {"id": 9, "name": "马永平", "gender": "男", "ethnicity": "回族",
     "birth": "1980-02", "birthplace": "",
     "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县委常委、副县长",
     "current_org": "中共张家川县委员会/张家川县人民政府",
     "source": "https://www.zjc.gov.cn/ldzc1/x_w_l_d.htm"},

    # 袁博 — 县委常委、人武部部长
    {"id": 10, "name": "袁博", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-12", "birthplace": "",
     "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县委常委、人武部部长",
     "current_org": "中共张家川县委员会/张家川县人民武装部",
     "source": "https://www.zjc.gov.cn/ldzc1/x_w_l_d.htm"},

    # 韩景红 — 县委常委、统战部部长，县政协党组副书记
    {"id": 11, "name": "韩景红", "gender": "女", "ethnicity": "汉族",
     "birth": "1986-03", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县委常委、统战部部长",
     "current_org": "中共张家川县委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/x_w_l_d.htm"},

    # 王国晟 — 县委常委、组织部部长
    {"id": 12, "name": "王国晟", "gender": "男", "ethnicity": "汉族",
     "birth": "1988-07", "birthplace": "",
     "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县委常委、组织部部长",
     "current_org": "中共张家川县委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/x_w_l_d.htm"},

    # ═══════════════════════════════════════════════════════════
    # 县政府其他领导 (not 县委常委)
    # ═══════════════════════════════════════════════════════════

    # 杨涛锋 — 副县长、县公安局局长
    {"id": 13, "name": "杨涛锋", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-04", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县副县长、县公安局局长",
     "current_org": "张家川县人民政府/张家川县公安局",
     "source": "https://www.zjc.gov.cn/ldzc1/xzfld.htm"},

    # 汪建全 — 副县长
    {"id": 14, "name": "汪建全", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-09", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县副县长",
     "current_org": "张家川县人民政府",
     "source": "https://www.zjc.gov.cn/ldzc1/xzfld.htm"},

    # 杨洛 — 副县长（挂职）
    {"id": 15, "name": "杨洛", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-01", "birthplace": "",
     "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县副县长（挂职）",
     "current_org": "张家川县人民政府",
     "source": "https://www.zjc.gov.cn/ldzc1/xzfld.htm"},

    # 杨龙飞 — 副县长（挂职）
    {"id": 16, "name": "杨龙飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1989-09", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县副县长（挂职）",
     "current_org": "张家川县人民政府",
     "source": "https://www.zjc.gov.cn/ldzc1/xzfld.htm"},

    # 钱花 — 副县长
    {"id": 17, "name": "钱花", "gender": "女", "ethnicity": "汉族",
     "birth": "1986-08", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县副县长",
     "current_org": "张家川县人民政府",
     "source": "https://www.zjc.gov.cn/ldzc1/xzfld.htm"},

    # ═══════════════════════════════════════════════════════════
    # 县人大领导
    # ═══════════════════════════════════════════════════════════

    # 麻小梅 — 县人大常委会主任
    {"id": 18, "name": "麻小梅", "gender": "女", "ethnicity": "回族",
     "birth": "1969-10", "birthplace": "",
     "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县人大常委会主任",
     "current_org": "张家川县人民代表大会常务委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/xrdld.htm"},

    # 赫金梅 — 县人大常委会副主任
    {"id": 19, "name": "赫金梅", "gender": "女", "ethnicity": "回族",
     "birth": "1974-05", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县人大常委会副主任",
     "current_org": "张家川县人民代表大会常务委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/xrdld.htm"},

    # 李元珍 — 县人大常委会副主任
    {"id": 20, "name": "李元珍", "gender": "男", "ethnicity": "回族",
     "birth": "1967-05", "birthplace": "",
     "education": "大学",
     "party_join": "", "work_start": "",
     "current_post": "张家川县人大常委会副主任",
     "current_org": "张家川县人民代表大会常务委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/xrdld.htm"},

    # 王保林 — 县人大常委会副主任
    {"id": 21, "name": "王保林", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-07", "birthplace": "",
     "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县人大常委会副主任",
     "current_org": "张家川县人民代表大会常务委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/xrdld.htm"},

    # 陈金海 — 县人大常委会副主任
    {"id": 22, "name": "陈金海", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-06", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县人大常委会副主任",
     "current_org": "张家川县人民代表大会常务委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/xrdld.htm"},

    # 马建军 — 县人大常委会副主任
    {"id": 23, "name": "马建军", "gender": "男", "ethnicity": "回族",
     "birth": "1973-05", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县人大常委会副主任",
     "current_org": "张家川县人民代表大会常务委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/xrdld.htm"},

    # ═══════════════════════════════════════════════════════════
    # 县政协领导
    # ═══════════════════════════════════════════════════════════

    # 马庭坚 — 县政协主席
    {"id": 24, "name": "马庭坚", "gender": "男", "ethnicity": "回族",
     "birth": "1970-05", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县政协主席",
     "current_org": "中国人民政治协商会议张家川县委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/xzxld.htm"},

    # 王小键 — 县政协副主席
    {"id": 25, "name": "王小键", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-05", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县政协副主席",
     "current_org": "中国人民政治协商会议张家川县委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/xzxld.htm"},

    # 马婷 — 县政协副主席
    {"id": 26, "name": "马婷", "gender": "女", "ethnicity": "回族",
     "birth": "1970-07", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县政协副主席",
     "current_org": "中国人民政治协商会议张家川县委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/xzxld.htm"},

    # 温泉 — 县政协副主席
    {"id": 27, "name": "温泉", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-04", "birthplace": "",
     "education": "大学",
     "party_join": "民建会员", "work_start": "",
     "current_post": "张家川县政协副主席",
     "current_org": "中国人民政治协商会议张家川县委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/xzxld.htm"},

    # 马彬 — 县政协副主席
    {"id": 28, "name": "马彬", "gender": "男", "ethnicity": "回族",
     "birth": "1969-05", "birthplace": "",
     "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县政协副主席",
     "current_org": "中国人民政治协商会议张家川县委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/xzxld.htm"},

    # 李毅 — 县政协副主席
    {"id": 29, "name": "李毅", "gender": "男", "ethnicity": "回族",
     "birth": "1973-05", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家川县政协副主席",
     "current_org": "中国人民政治协商会议张家川县委员会",
     "source": "https://www.zjc.gov.cn/ldzc1/xzxld.htm"},

    # ═══════════════════════════════════════════════════════════
    # PREDECESSORS — 县委书记 (information limited from open web)
    # ═══════════════════════════════════════════════════════════

    # 张思佳 — 前任张家川县委书记 (prior to 何敬忠)
    {"id": 30, "name": "张思佳", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原张家川县委书记",
     "current_org": "原中共张家川县委员会",
     "source": "public media reports; 2025年以县委书记身份出席活动"},

    # 马筱宁 — 前任张家川县县长 (prior to 马杰)
    {"id": 31, "name": "马筱宁", "gender": "男", "ethnicity": "回族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原张家川县委副书记、县长",
     "current_org": "原张家川县人民政府",
     "source": "public media reports"},

    # 马创成 — 前任张家川县县长 (prior to 马筱宁; also known as 马创成)
    {"id": 32, "name": "马创成", "gender": "男", "ethnicity": "回族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原张家川县委副书记、县长",
     "current_org": "原张家川县人民政府",
     "source": "public media reports; 2021-2023年任县长"},
]

organizations = [
    {"id": 1, "name": "中共张家川县委员会", "type": "党委", "level": "县处级",
     "parent": "中共天水市委员会", "location": "甘肃省天水市张家川回族自治县"},
    {"id": 2, "name": "张家川县人民政府", "type": "政府", "level": "县处级",
     "parent": "天水市人民政府", "location": "甘肃省天水市张家川回族自治县"},
    {"id": 3, "name": "张家川县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "天水市人大常委会", "location": "甘肃省天水市张家川回族自治县"},
    {"id": 4, "name": "中国人民政治协商会议张家川县委员会", "type": "政协", "level": "县处级",
     "parent": "天水市政协", "location": "甘肃省天水市张家川回族自治县"},
    {"id": 5, "name": "中共张家川县纪律检查委员会/张家川县监察委员会", "type": "党委", "level": "县处级",
     "parent": "中共天水市纪律检查委员会", "location": "甘肃省天水市张家川回族自治县"},
    {"id": 6, "name": "张家川县公安局", "type": "政府", "level": "乡科级",
     "parent": "张家川县人民政府/天水市公安局", "location": "甘肃省天水市张家川回族自治县"},
    {"id": 7, "name": "张家川县人民武装部", "type": "党委", "level": "县处级",
     "parent": "天水军分区", "location": "甘肃省天水市张家川回族自治县"},
    {"id": 8, "name": "中共天水市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共甘肃省委员会", "location": "甘肃省天水市"},
    {"id": 9, "name": "天水市人民政府", "type": "政府", "level": "地厅级",
     "parent": "甘肃省人民政府", "location": "甘肃省天水市"},
]

positions = [
    # ── 何敬忠 (id=1) ──
    {"person_id": 1, "org_id": 1, "title": "张家川县委书记", "start": "unknown", "end": "present", "rank": "副厅级",
     "note": "现任县委书记，具体任职起始时间待确认"},

    # ── 马杰 (id=2) ──
    {"person_id": 2, "org_id": 1, "title": "张家川县委副书记", "start": "2026-01", "end": "present", "rank": "正处级",
     "note": "2026年1月27日任副县长、代县长"},
    {"person_id": 2, "org_id": 2, "title": "张家川县县长", "start": "2026-01", "end": "present", "rank": "正处级",
     "note": "2026年1月27日县十七届人大常委会第三十七次会议决定代理县长职务"},

    # ── 刘润斌 (id=3) ──
    {"person_id": 3, "org_id": 1, "title": "张家川县委副书记（专职）", "start": "", "end": "present", "rank": "副处级",
     "note": "专职副书记"},

    # ── 赵亮 (id=4) ──
    {"person_id": 4, "org_id": 1, "title": "张家川县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 薛天胜 (id=5) ──
    {"person_id": 5, "org_id": 1, "title": "张家川县委常委、政法委书记", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 王浩 (id=6) ──
    {"person_id": 6, "org_id": 1, "title": "张家川县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 6, "org_id": 5, "title": "张家川县纪委书记、县监委主任", "start": "", "end": "present", "rank": "副处级",
     "note": "四级高级监察官"},

    # ── 王志杰 (id=7) ──
    {"person_id": 7, "org_id": 1, "title": "张家川县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 7, "org_id": 2, "title": "张家川县常务副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "县政府党组副书记、副县长"},

    # ── 赵燚 (id=8) ──
    {"person_id": 8, "org_id": 1, "title": "张家川县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": "挂职"},
    {"person_id": 8, "org_id": 2, "title": "张家川县副县长（挂职）", "start": "", "end": "present", "rank": "副处级",
     "note": "挂职"},

    # ── 马永平 (id=9) ──
    {"person_id": 9, "org_id": 1, "title": "张家川县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 9, "org_id": 2, "title": "张家川县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 袁博 (id=10) ──
    {"person_id": 10, "org_id": 1, "title": "张家川县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 10, "org_id": 7, "title": "张家川县人武部部长", "start": "", "end": "present", "rank": "上校",
     "note": "县人武部上校部长"},

    # ── 韩景红 (id=11) ──
    {"person_id": 11, "org_id": 1, "title": "张家川县委常委、统战部部长", "start": "", "end": "present", "rank": "副处级",
     "note": "县政协党组副书记"},

    # ── 王国晟 (id=12) ──
    {"person_id": 12, "org_id": 1, "title": "张家川县委常委、组织部部长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 杨涛锋 (id=13) ──
    {"person_id": 13, "org_id": 2, "title": "张家川县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 13, "org_id": 6, "title": "张家川县公安局局长", "start": "", "end": "present", "rank": "正科级",
     "note": "县公安局党委书记、局长、督察长"},

    # ── 汪建全 (id=14) ──
    {"person_id": 14, "org_id": 2, "title": "张家川县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 杨洛 (id=15) ──
    {"person_id": 15, "org_id": 2, "title": "张家川县副县长（挂职）", "start": "", "end": "present", "rank": "副处级",
     "note": "挂职"},

    # ── 杨龙飞 (id=16) ──
    {"person_id": 16, "org_id": 2, "title": "张家川县副县长（挂职）", "start": "", "end": "present", "rank": "副处级",
     "note": "挂职"},

    # ── 钱花 (id=17) ──
    {"person_id": 17, "org_id": 2, "title": "张家川县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 麻小梅 (id=18) ──
    {"person_id": 18, "org_id": 3, "title": "张家川县人大常委会主任", "start": "", "end": "present", "rank": "正处级",
     "note": "二级巡视员"},

    # ── 赫金梅 (id=19) ──
    {"person_id": 19, "org_id": 3, "title": "张家川县人大常委会副主任", "start": "", "end": "present", "rank": "副处级",
     "note": "党组副书记"},

    # ── 李元珍 (id=20) ──
    {"person_id": 20, "org_id": 3, "title": "张家川县人大常委会副主任", "start": "", "end": "present", "rank": "副处级",
     "note": "县伊斯兰教协会第八届会长"},

    # ── 王保林 (id=21) ──
    {"person_id": 21, "org_id": 3, "title": "张家川县人大常委会副主任", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 陈金海 (id=22) ──
    {"person_id": 22, "org_id": 3, "title": "张家川县人大常委会副主任", "start": "", "end": "present", "rank": "副处级",
     "note": "县总工会主席"},

    # ── 马建军 (id=23) ──
    {"person_id": 23, "org_id": 3, "title": "张家川县人大常委会副主任", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 马庭坚 (id=24) ──
    {"person_id": 24, "org_id": 4, "title": "张家川县政协主席", "start": "", "end": "present", "rank": "正处级",
     "note": ""},

    # ── 王小键 (id=25) ──
    {"person_id": 25, "org_id": 4, "title": "张家川县政协副主席", "start": "", "end": "present", "rank": "副处级",
     "note": "党组副书记"},

    # ── 马婷 (id=26) ──
    {"person_id": 26, "org_id": 4, "title": "张家川县政协副主席", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 温泉 (id=27) ──
    {"person_id": 27, "org_id": 4, "title": "张家川县政协副主席", "start": "", "end": "present", "rank": "副处级",
     "note": "民建会员"},

    # ── 马彬 (id=28) ──
    {"person_id": 28, "org_id": 4, "title": "张家川县政协副主席", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 李毅 (id=29) ──
    {"person_id": 29, "org_id": 4, "title": "张家川县政协副主席", "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # ── 张思佳 (id=30) ──
    {"person_id": 30, "org_id": 1, "title": "张家川县委书记", "start": "", "end": "~2025", "rank": "副厅级",
     "note": "前任县委书记，2025年仍在任，后由何敬忠接任"},

    # ── 马筱宁 (id=31) ──
    {"person_id": 31, "org_id": 2, "title": "张家川县委副书记、县长", "start": "", "end": "~2025", "rank": "正处级",
     "note": "前任县长"},

    # ── 马创成 (id=32) ──
    {"person_id": 32, "org_id": 2, "title": "张家川县委副书记、县长", "start": "~2021", "end": "~2023", "rank": "正处级",
     "note": "前任县长，2021-2023年在任"},
]

relationships = [
    # ── Current top leaders ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "何敬忠作为县委书记, 马杰作为县长, 是党政一把手搭档关系",
     "overlap_org": "中共张家川县委员会/张家川县人民政府",
     "overlap_period": "2026-01~present", "confidence": "confirmed"},

    # ── 县委班子 ──
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "strength": "strong",
     "context": "何敬忠作为县委书记, 刘润斌作为专职副书记, 是县委班子搭档",
     "overlap_org": "中共张家川县委员会",
     "overlap_period": "present", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 4, "type": "overlap", "strength": "medium",
     "context": "何敬忠与赵亮在县委班子共事",
     "overlap_org": "中共张家川县委员会",
     "overlap_period": "present", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 5, "type": "overlap", "strength": "medium",
     "context": "何敬忠与薛天胜在县委班子共事",
     "overlap_org": "中共张家川县委员会",
     "overlap_period": "present", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 6, "type": "overlap", "strength": "medium",
     "context": "何敬忠与王浩在县委班子共事",
     "overlap_org": "中共张家川县委员会",
     "overlap_period": "present", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 7, "type": "overlap", "strength": "medium",
     "context": "何敬忠与王志杰在县委班子共事",
     "overlap_org": "中共张家川县委员会",
     "overlap_period": "present", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 11, "type": "overlap", "strength": "medium",
     "context": "何敬忠与韩景红在县委班子共事",
     "overlap_org": "中共张家川县委员会",
     "overlap_period": "present", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 12, "type": "overlap", "strength": "medium",
     "context": "何敬忠与王国晟在县委班子共事",
     "overlap_org": "中共张家川县委员会",
     "overlap_period": "present", "confidence": "confirmed"},

    # ── 县长与副县长 ──
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "strength": "strong",
     "context": "马杰作为县长, 王志杰作为常务副县长, 是政府班子搭档",
     "overlap_org": "张家川县人民政府",
     "overlap_period": "2026-01~present", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "strength": "strong",
     "context": "马杰作为县长, 杨涛锋作为副县长兼公安局长",
     "overlap_org": "张家川县人民政府",
     "overlap_period": "2026-01~present", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "strength": "medium",
     "context": "马杰作为县长, 汪建全作为副县长",
     "overlap_org": "张家川县人民政府",
     "overlap_period": "2026-01~present", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 17, "type": "superior_subordinate", "strength": "medium",
     "context": "马杰作为县长, 钱花作为副县长",
     "overlap_org": "张家川县人民政府",
     "overlap_period": "2026-01~present", "confidence": "confirmed"},

    # ── Succession chain: 县委书记 ──
    {"person_a": 1, "person_b": 30, "type": "predecessor_successor", "strength": "strong",
     "context": "何敬忠接替张思佳任张家川县委书记",
     "overlap_org": "中共张家川县委员会",
     "overlap_period": "2025~2026", "confidence": "plausible"},

    # ── Succession chain: 县长 ──
    {"person_a": 2, "person_b": 31, "type": "predecessor_successor", "strength": "strong",
     "context": "马杰接替马筱宁任张家川县县长",
     "overlap_org": "张家川县人民政府",
     "overlap_period": "2025~2026", "confidence": "plausible"},

    {"person_a": 31, "person_b": 32, "type": "predecessor_successor", "strength": "medium",
     "context": "马筱宁接替马创成任张家川县县长",
     "overlap_org": "张家川县人民政府",
     "overlap_period": "~2023", "confidence": "plausible"},

    # ── Top leaders + Four major leadership ──
    {"person_a": 1, "person_b": 18, "type": "overlap", "strength": "medium",
     "context": "何敬忠与麻小梅在张家川县党政班子共事",
     "overlap_org": "中共张家川县委员会/张家川县人大常委会",
     "overlap_period": "present", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 24, "type": "overlap", "strength": "medium",
     "context": "何敬忠与马庭坚在张家川县党政班子共事",
     "overlap_org": "中共张家川县委员会/张家川县政协",
     "overlap_period": "present", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 18, "type": "overlap", "strength": "medium",
     "context": "马杰与麻小梅在张家川县党政班子共事",
     "overlap_org": "张家川县人民政府/张家川县人大常委会",
     "overlap_period": "2026-01~present", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 24, "type": "overlap", "strength": "medium",
     "context": "马杰与马庭坚在张家川县党政班子共事",
     "overlap_org": "张家川县人民政府/张家川县政协",
     "overlap_period": "2026-01~present", "confidence": "confirmed"},
]


# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p["current_post"]
    if "县委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "县长" in role and "副书记" in role:
        return "50,100,255"
    elif "县长" in role:
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    elif "原" in role:
        return "160,160,160"
    else:
        return "100,100,100"


def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")


def is_top_leader(p):
    role = p["current_post"]
    return "县委书记" in role or ("县长" in role and "副书记" in role)


def person_size(p):
    return "20.0" if is_top_leader(p) else ("14.0" if "原" not in p["current_post"] else "10.0")


# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>张家川回族自治县领导班子工作关系网络 - 甘肃省天水市张家川回族自治县</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
