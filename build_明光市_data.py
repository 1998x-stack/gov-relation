#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 明光市 (Mingguang, Chuzhou, Anhui) leadership network.

Generated: 2026-07-16
Task: anhui_明光市 - 市委书记 & 市长
Sources:
  - Mingguang City Government Website (www.mingguang.gov.cn) — leadership page, news articles
  - Mingguang 16th Party Congress reports (June 2026)
  - Official leadership page at www.mingguang.gov.cn/zwgk/ldzc/

Confidence note: Web search tools (Exa, Google) were rate-limited or blocked during research.
Official government website was used as primary source. Party committee leadership data obtained
from congress coverage. Some career timeline data for 刘梦汝 is partial and should be verified
against organization department appointment notices.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ─────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = SCRIPT_DIR
# If running from staging directory
if "data/tmp" in BASE:
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))
STAGING = os.path.join(BASE, "data/tmp/anhui_明光市")
DB_PATH = os.path.join(STAGING, "明光市_network.db")
GEXF_PATH = os.path.join(STAGING, "明光市_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── RESEARCH DATA ────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 市委书记
    {
        "id": "mg_liu_mengru",
        "name": "刘梦汝",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委书记",
        "current_org": "中共明光市委员会",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429753.html (市委理论学习中心组学习会议报道, 2026-07-14)",
        "notes": "刘梦汝以市委书记身份主持明光市第十六次党代会（2026-06-26至06-27），并在十五届市委报告中回顾五年工作，说明其至少在2021年已任明光市委书记。完整履历和具体任职起始时间待核实。",
        "confidence": "confirmed"
    },

    # 市委副书记、市长
    {
        "id": "mg_tian_haisong",
        "name": "田海松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-05",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委副书记、市政府市长、党组书记",
        "current_org": "明光市人民政府",
        "source": "https://www.mingguang.gov.cn/zwgk/ldzc/ (领导之窗页面, 2026-07-16)",
        "notes": "曾任县政府工作部门副职、省直单位内设处室主任科员、县政府副县长、县委常委、地级市市政府直属单位正职等。",
        "confidence": "confirmed"
    },

    # ══════════════ 市人大、政协主要领导 ══════════════

    {
        "id": "mg_cao_yingchun",
        "name": "曹迎春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市人大常委会主任",
        "current_org": "明光市人大常委会",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429753.html (市委理论学习中心组学习会议, 2026-07-14)",
        "notes": "出席市委理论学习中心组学习会议。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_xue_rulin",
        "name": "薛如林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市政协主席",
        "current_org": "政协明光市委员会",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429753.html (市委理论学习中心组学习会议, 2026-07-14)",
        "notes": "出席市委理论学习中心组学习会议。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_zhang_yanping",
        "name": "张言平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市政协一级调研员",
        "current_org": "政协明光市委员会",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429753.html (市委理论学习中心组学习会议, 2026-07-14)",
        "notes": "原市政协主席转一级调研员。",
        "confidence": "confirmed"
    },

    # ══════════════ 市委领导班子 ══════════════

    {
        "id": "mg_ran_lei",
        "name": "冉磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委副书记",
        "current_org": "中共明光市委员会",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429753.html (市委理论学习中心组学习会议, 2026-07-14)",
        "notes": "市委副书记。曾参加市第十六次党代会第二代表团讨论。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_xu_lifeng",
        "name": "徐礼锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委常委",
        "current_org": "中共明光市委员会",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429607.html (刘梦汝开展信访接待活动, 2026-07-07)",
        "notes": "市委常委，参加信访接待活动。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_yao_zhengyu",
        "name": "姚正玉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委常委",
        "current_org": "中共明光市委员会",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429607.html (刘梦汝开展信访接待活动, 2026-07-07)",
        "notes": "市委常委，参加信访接待活动。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_wang_peng",
        "name": "王鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委常委、组织部部长",
        "current_org": "中共明光市委组织部",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429199.html (滁州市庆祝建党105周年展演报道, 2026-06-28)",
        "notes": "市委常委、组织部部长。参加滁州市建党105周年展演活动。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_dong_jianguo",
        "name": "董建国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委常委、副市长",
        "current_org": "明光市人民政府",
        "source": "https://www.mingguang.gov.cn/zwgk/ldzc/ (领导之窗页面, 2026-07-16)",
        "notes": "市委常委、副市长，市政府排名第一的副市长。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_tang_zhongzhu",
        "name": "唐中柱",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委常委、副市长",
        "current_org": "明光市人民政府",
        "source": "https://www.mingguang.gov.cn/zwgk/ldzc/ (领导之窗页面, 2026-07-16)",
        "notes": "市委常委、副市长。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_ding_zhiguo",
        "name": "丁志国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委常委、市纪委书记、市监委主任",
        "current_org": "中共明光市纪律检查委员会",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429195.html (市纪委第一次全体会议, 2026-06-27)",
        "notes": "2026年6月27日当选十六届市纪委书记。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_miao_qun",
        "name": "缪群",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委常委",
        "current_org": "中共明光市委员会",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429145.html (市第十六次党代会开幕, 2026-06-26)",
        "notes": "十六次党代会主席团成员。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_li_ming",
        "name": "李明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委常委",
        "current_org": "中共明光市委员会",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429145.html (市第十六次党代会开幕, 2026-06-26)",
        "notes": "十六次党代会主席团成员。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_ge_tao",
        "name": "葛弢",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委常委",
        "current_org": "中共明光市委员会",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429145.html (市第十六次党代会开幕, 2026-06-26)",
        "notes": "十六次党代会主席团成员。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_yu_wenlong",
        "name": "于文龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委常委",
        "current_org": "中共明光市委员会",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429145.html (市第十六次党代会开幕, 2026-06-26)",
        "notes": "十六次党代会主席团成员。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_shi_liqing",
        "name": "史立清",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委常委",
        "current_org": "中共明光市委员会",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429145.html (市第十六次党代会开幕, 2026-06-26)",
        "notes": "十六次党代会主席团成员。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_zhang_ming",
        "name": "张明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "明光市委常委",
        "current_org": "中共明光市委员会",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429145.html (市第十六次党代会开幕, 2026-06-26)",
        "notes": "十六次党代会主席团成员。",
        "confidence": "confirmed"
    },

    # ══════════════ 市政府领导班子 ══════════════

    {
        "id": "mg_miao_chuanfeng",
        "name": "缪传凤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "明光市副市长",
        "current_org": "明光市人民政府",
        "source": "https://www.mingguang.gov.cn/zwgk/ldzc/ (领导之窗页面, 2026-07-16)",
        "notes": "市政府副市长。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_liu_yu",
        "name": "刘雨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "明光市副市长（挂职）",
        "current_org": "明光市人民政府",
        "source": "https://www.mingguang.gov.cn/zwgk/ldzc/ (领导之窗页面, 2026-07-16)",
        "notes": "挂职副市长。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_huang_kouming",
        "name": "黄扣明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "明光市副市长",
        "current_org": "明光市人民政府",
        "source": "https://www.mingguang.gov.cn/zwgk/ldzc/ (领导之窗页面, 2026-07-16)",
        "notes": "市政府副市长。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_zhu_qihao",
        "name": "朱其昊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "明光市副市长",
        "current_org": "明光市人民政府",
        "source": "https://www.mingguang.gov.cn/zwgk/ldzc/ (领导之窗页面, 2026-07-16)",
        "notes": "市政府副市长。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_ye_shanzeng",
        "name": "叶善增",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "明光市副市长（挂职）",
        "current_org": "明光市人民政府",
        "source": "https://www.mingguang.gov.cn/zwgk/ldzc/ (领导之窗页面, 2026-07-16)",
        "notes": "挂职副市长。",
        "confidence": "confirmed"
    },
    {
        "id": "mg_sang_linqing",
        "name": "桑林庆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "明光市领导（拟为副市长）",
        "current_org": "明光市人民政府",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429726.html (产业投资基金专题讲座报道, 2026-07-11)",
        "notes": "出席产业投资基金专题讲座。党代会主席团成员之一，应为市领导。具体职务待确认。",
        "confidence": "plausible"
    },
    {
        "id": "mg_yuan_jiaxiang",
        "name": "袁家祥",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "明光市领导",
        "current_org": "",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429145.html (市第十六次党代会开幕, 2026-06-26)",
        "notes": "十六次党代会主席团成员。具体职务待确认。",
        "confidence": "plausible"
    },
    {
        "id": "mg_wan_jie",
        "name": "万杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "明光市领导",
        "current_org": "",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429145.html (市第十六次党代会开幕, 2026-06-26)",
        "notes": "十六次党代会主席团成员。具体职务待确认。",
        "confidence": "plausible"
    },
    {
        "id": "mg_yu_xing",
        "name": "於星",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "明光市领导",
        "current_org": "",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429145.html (市第十六次党代会开幕, 2026-06-26)",
        "notes": "十六次党代会主席团成员。具体职务待确认。",
        "confidence": "plausible"
    },
    {
        "id": "mg_zhang_zaibing",
        "name": "张在兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "明光市领导",
        "current_org": "",
        "source": "https://www.mingguang.gov.cn/zwdt/zwyw/278429145.html (市第十六次党代会开幕, 2026-06-26)",
        "notes": "十六次党代会主席团成员。具体职务待确认。",
        "confidence": "plausible"
    },
]

organizations = [
    {
        "id": "org_cpc_mingguang",
        "name": "中共明光市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共滁州市委",
        "location": "安徽省滁州市明光市",
    },
    {
        "id": "org_gov_mingguang",
        "name": "明光市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "滁州市人民政府",
        "location": "安徽省滁州市明光市",
    },
    {
        "id": "org_npc_mingguang",
        "name": "明光市人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "滁州市人大常委会",
        "location": "安徽省滁州市明光市",
    },
    {
        "id": "org_cppcc_mingguang",
        "name": "政协明光市委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协滁州市委员会",
        "location": "安徽省滁州市明光市",
    },
    {
        "id": "org_cdi_mingguang",
        "name": "中共明光市纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共滁州市纪律检查委员会",
        "location": "安徽省滁州市明光市",
    },
    {
        "id": "org_od_mingguang",
        "name": "中共明光市委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共明光市委员会",
        "location": "安徽省滁州市明光市",
    },
]

positions = [
    # ── 刘梦汝 ──
    {"person_id": "mg_liu_mengru", "org_id": "org_cpc_mingguang", "title": "明光市委书记", "start": "2021?", "end": "present", "rank": "正县级", "note": "至少自2021年起任职，2026年6月主持第十六次党代会"},
    # ── 田海松 ──
    {"person_id": "mg_tian_haisong", "org_id": "org_gov_mingguang", "title": "明光市市长", "start": "", "end": "present", "rank": "正县级", "note": "现任市委副书记、市长、党组书记。曾任县政府工作部门副职、省直单位主任科员、副县长、县委常委、市直单位正职"},
    {"person_id": "mg_tian_haisong", "org_id": "org_cpc_mingguang", "title": "明光市委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 曹迎春 ──
    {"person_id": "mg_cao_yingchun", "org_id": "org_npc_mingguang", "title": "明光市人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # ── 薛如林 ──
    {"person_id": "mg_xue_rulin", "org_id": "org_cppcc_mingguang", "title": "明光市政协主席", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # ── 张言平 ──
    {"person_id": "mg_zhang_yanping", "org_id": "org_cppcc_mingguang", "title": "明光市政协一级调研员", "start": "", "end": "present", "rank": "正县级", "note": "原市政协主席转一级调研员"},
    # ── 冉磊 ──
    {"person_id": "mg_ran_lei", "org_id": "org_cpc_mingguang", "title": "明光市委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 徐礼锋 ──
    {"person_id": "mg_xu_lifeng", "org_id": "org_cpc_mingguang", "title": "明光市委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 姚正玉 ──
    {"person_id": "mg_yao_zhengyu", "org_id": "org_cpc_mingguang", "title": "明光市委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 王鹏 ──
    {"person_id": "mg_wang_peng", "org_id": "org_od_mingguang", "title": "明光市委常委、组织部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 董建国 ──
    {"person_id": "mg_dong_jianguo", "org_id": "org_gov_mingguang", "title": "明光市委常委、副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 唐中柱 ──
    {"person_id": "mg_tang_zhongzhu", "org_id": "org_gov_mingguang", "title": "明光市委常委、副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 丁志国 ──
    {"person_id": "mg_ding_zhiguo", "org_id": "org_cdi_mingguang", "title": "明光市纪委书记", "start": "2026-06", "end": "present", "rank": "副县级", "note": "2026年6月27日当选十六届市纪委书记"},
    # ── 缪群 ──
    {"person_id": "mg_miao_qun", "org_id": "org_cpc_mingguang", "title": "明光市委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 李明 ──
    {"person_id": "mg_li_ming", "org_id": "org_cpc_mingguang", "title": "明光市委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 葛弢 ──
    {"person_id": "mg_ge_tao", "org_id": "org_cpc_mingguang", "title": "明光市委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 于文龙 ──
    {"person_id": "mg_yu_wenlong", "org_id": "org_cpc_mingguang", "title": "明光市委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 史立清 ──
    {"person_id": "mg_shi_liqing", "org_id": "org_cpc_mingguang", "title": "明光市委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 张明 ──
    {"person_id": "mg_zhang_ming", "org_id": "org_cpc_mingguang", "title": "明光市委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 缪传凤 ──
    {"person_id": "mg_miao_chuanfeng", "org_id": "org_gov_mingguang", "title": "明光市副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 刘雨 ──
    {"person_id": "mg_liu_yu", "org_id": "org_gov_mingguang", "title": "明光市副市长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 黄扣明 ──
    {"person_id": "mg_huang_kouming", "org_id": "org_gov_mingguang", "title": "明光市副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 朱其昊 ──
    {"person_id": "mg_zhu_qihao", "org_id": "org_gov_mingguang", "title": "明光市副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 叶善增 ──
    {"person_id": "mg_ye_shanzeng", "org_id": "org_gov_mingguang", "title": "明光市副市长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 桑林庆 ──
    {"person_id": "mg_sang_linqing", "org_id": "org_gov_mingguang", "title": "明光市领导（拟为副市长）", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
]

relationships = [
    {
        "person_a": "mg_liu_mengru",
        "person_b": "mg_tian_haisong",
        "type": "superior_subordinate",
        "context": "市委书记与市长搭档",
        "overlap_org": "中共明光市委员会",
        "overlap_period": "2021?-present",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "mg_liu_mengru",
        "person_b": "mg_ran_lei",
        "type": "superior_subordinate",
        "context": "市委书记与市委副书记",
        "overlap_org": "中共明光市委员会",
        "overlap_period": "present",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "mg_liu_mengru",
        "person_b": "mg_ding_zhiguo",
        "type": "superior_subordinate",
        "context": "市委书记与市纪委书记",
        "overlap_org": "中共明光市委员会",
        "overlap_period": "present",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a": "mg_liu_mengru",
        "person_b": "mg_wang_peng",
        "type": "superior_subordinate",
        "context": "市委书记与组织部部长",
        "overlap_org": "中共明光市委员会",
        "overlap_period": "present",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a": "mg_tian_haisong",
        "person_b": "mg_dong_jianguo",
        "type": "superior_subordinate",
        "context": "市长与常务副市长",
        "overlap_org": "明光市人民政府",
        "overlap_period": "present",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "mg_tian_haisong",
        "person_b": "mg_tang_zhongzhu",
        "type": "superior_subordinate",
        "context": "市长与副市长",
        "overlap_org": "明光市人民政府",
        "overlap_period": "present",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "mg_liu_mengru",
        "person_b": "mg_cao_yingchun",
        "type": "overlap",
        "context": "市委书记与人大常委会主任",
        "overlap_org": "中共明光市委员会",
        "overlap_period": "present",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a": "mg_liu_mengru",
        "person_b": "mg_xue_rulin",
        "type": "overlap",
        "context": "市委书记与政协主席",
        "overlap_org": "中共明光市委员会",
        "overlap_period": "present",
        "strength": "medium",
        "confidence": "confirmed",
    },
]

# ── SQLite Build ─────────────────────────────────────────────────────

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons(
            id, name, gender, ethnicity, birth, birthplace, education,
            party_join, work_start, current_post, current_org, source
        );
        CREATE TABLE organizations(
            id, name, type, level, parent, location
        );
        CREATE TABLE positions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id, org_id, title, start, "end", rank, note
        );
        CREATE TABLE relationships(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a, person_b, type, context, overlap_org, overlap_period,
            strength, confidence
        );
    """)

    for p in persons:
        c.execute("""INSERT INTO persons(id,name,gender,ethnicity,birth,birthplace,education,
                    party_join,work_start,current_post,current_org,source)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p.get("birthplace", ""), p.get("education", ""),
                   p["party_join"], p.get("work_start", ""),
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations(id,name,type,level,parent,location)
                    VALUES(?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"],
                   o["parent"], o["location"]))

    for po in positions:
        c.execute("""INSERT INTO positions(person_id,org_id,title,start,"end",rank,note)
                    VALUES(?,?,?,?,?,?,?)""",
                  (po["person_id"], po["org_id"], po["title"],
                   po.get("start", ""), po.get("end", ""),
                   po.get("rank", ""), po.get("note", "")))

    for r in relationships:
        c.execute("""INSERT INTO relationships(person_a,person_b,type,context,
                    overlap_org,overlap_period,strength,confidence)
                    VALUES(?,?,?,?,?,?,?,?)""",
                  (r["person_a"], r["person_b"], r["type"], r["context"],
                   r["overlap_org"], r["overlap_period"],
                   r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"  Database written: {DB_PATH}")


# ── GEXF Build ──────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Color by role."""
    post = p.get("current_post", "")
    if "书记" in post and "纪委" not in post and "副书记" not in post:
        return "255,50,50"      # Party Secretary - Red
    elif "市长" in post or "县长" in post or "区长" in post:
        return "50,100,255"     # Mayor/County Head - Blue
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"      # Discipline Inspection - Orange
    elif "副书记" in post:
        return "50,100,255"     # Deputy Secretary - Blue
    elif "主任" in post or "主席" in post:
        return "100,180,100"    # NPC/CPPCC leader - Green
    elif "常委" in post:
        return "180,180,50"     # Standing Committee - Yellow-green
    elif "副市长" in post:
        return "50,100,255"     # Deputy Mayor - Blue
    else:
        return "100,100,100"    # Others - Grey

def org_color(o):
    t = o.get("type", "")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,200,150",
    }
    return colors.get(t, "200,200,200")

def is_top_leader(p):
    post = p.get("current_post", "")
    return ("书记" in post and "纪委" not in post and "副书记" not in post and "常委" not in post) or \
           ("市长" in post or "县长" in post or "区长" in post) and "副" not in post

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>明光市领导关系网络 - Mingguang City Leadership Network</description>')
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
    lines.append('    </attributes>')

    # Nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        pid = "p" + p["id"]
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Nodes - organizations
    for o in organizations:
        oid = "o" + o["id"]
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("location", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges - positions (person -> org)
    lines.append('    <edges>')
    eid = 0
    for po in positions:
        eid += 1
        pid = "p" + po["person_id"]
        oid = "o" + po["org_id"]
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(po["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(po.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges - relationships (person <-> person)
    for r in relationships:
        eid += 1
        pa = "p" + r["person_a"]
        pb = "p" + r["person_b"]
        w = "2.0" if r["strength"] == "strong" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")


# ── Main ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(STAGING, exist_ok=True)
    print("Building 明光市 network data...")
    print(f"  Staging: {STAGING}")
    build_db()
    build_gexf()
    print("Done.")
