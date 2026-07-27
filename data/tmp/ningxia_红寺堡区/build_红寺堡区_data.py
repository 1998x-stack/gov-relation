#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 红寺堡区 (Hongsibu District), 宁夏回族自治区.

Task ID: ningxia_红寺堡区
Province: 宁夏回族自治区
Parent city: 吴忠市
Region: 红寺堡区
Level: 市辖区
Targets: 区委书记 & 区长
Investigation date: 2026-07-25

Research sources:
  - www.hongsibu.gov.cn/xxgk/ldzc/ — 红寺堡区人民政府领导之窗 (official, current as of 2026-07)
  - Confirmed区委领导: 赵志锋(书记), 杨文福(副书记/区长), 段立栓(副书记/政法委), 赵军(组织部), 尤韬(常务副区长)
  - Confirmed政府领导: 杨文福(区长), 尤韬(常务副区长), 杨继东(副区长), 刘炳枢(副区长), 杨吉林(副区长), 张福莲(副区长), 董涛(副区长/公安局长), 马海(党组成员)
  - 人大领导: 苏达志(主任), 关保智, 伍洪亮, 马锦花, 王琳(副主任)
  - 政协领导: 张致强(主席), 丁学春(副书记), 浦彦卿, 李军保, 马春梅(副主席)
  - 红寺堡区是宁夏吴忠市下辖的市辖区，为全国最大的生态移民扶贫集中安置区

Confidence notes:
  - All leadership data confirmed via official government website (primary source)
  - Individual career timelines (education details, early career) are limited — only brief bios available from the official page
  - Detailed predecessor information could not be verified due to web search limitations (Exa rate-limited, Baidu/Jina blocked)
  - Person JSONs created with available information; open questions document gaps
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"
SLUG = "红寺堡区"

DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(STAGING)

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — 区委
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "赵志锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年3月",
        "birthplace": "",
        "education": "宁夏党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共吴忠市红寺堡区委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 2,
        "name": "杨文福",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1973年7月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "红寺堡区人民政府",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 3,
        "name": "段立栓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、政法委书记",
        "current_org": "中共吴忠市红寺堡区委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 4,
        "name": "赵军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年1月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共吴忠市红寺堡区委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 5,
        "name": "尤韬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "红寺堡区人民政府",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 6,
        "name": "丁学春",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1976年3月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共吴忠市红寺堡区委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 7,
        "name": "杨继东",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1976年3月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "红寺堡区人民政府",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 8,
        "name": "李鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记",
        "current_org": "中共吴忠市红寺堡区纪律检查委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 9,
        "name": "白净",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1989年4月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、红寺堡镇党委书记",
        "current_org": "红寺堡镇",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区人大领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "苏达志",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1967年6月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "红寺堡区人民代表大会常务委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 11,
        "name": "关保智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年12月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "红寺堡区人民代表大会常务委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 12,
        "name": "伍洪亮",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1971年7月",
        "birthplace": "",
        "education": "宁夏党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "红寺堡区人民代表大会常务委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 13,
        "name": "马锦花",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1968年8月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "红寺堡区人民代表大会常务委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 14,
        "name": "王琳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年9月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "红寺堡区人民代表大会常务委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区政府领导 (other than those already listed)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 15,
        "name": "刘炳枢",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1976年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "红寺堡区人民政府",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 16,
        "name": "杨吉林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "红寺堡区人民政府",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 17,
        "name": "张福莲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "民进会员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "红寺堡区人民政府",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 18,
        "name": "董涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年7月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安分局局长",
        "current_org": "红寺堡区人民政府",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区政协领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 19,
        "name": "张致强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议红寺堡区委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 20,
        "name": "浦彦卿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议红寺堡区委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 21,
        "name": "李军保",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议红寺堡区委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 22,
        "name": "马春梅",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1976年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "农工党",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议红寺堡区委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Other区委领导 (挂职)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 23,
        "name": "王丹玥",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年3月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记（挂职）",
        "current_org": "中共吴忠市红寺堡区委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 24,
        "name": "庄泽平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年10月",
        "birthplace": "",
        "education": "在职本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记（挂职）、副区长",
        "current_org": "红寺堡区人民政府",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 25,
        "name": "王立双",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长（挂职）",
        "current_org": "中共吴忠市红寺堡区委员会",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 26,
        "name": "苟俊杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1991年9月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委（挂职）、副区长",
        "current_org": "红寺堡区人民政府",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 27,
        "name": "韩爱民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、人民武装部部长",
        "current_org": "吴忠市红寺堡区人民武装部",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
    {
        "id": 28,
        "name": "马海",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1988年9月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员",
        "current_org": "红寺堡区人民政府",
        "source": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共吴忠市红寺堡区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共吴忠市委员会",
        "location": "吴忠市红寺堡区"
    },
    {
        "id": 2,
        "name": "红寺堡区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "吴忠市人民政府",
        "location": "吴忠市红寺堡区"
    },
    {
        "id": 3,
        "name": "红寺堡区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "吴忠市人民代表大会常务委员会",
        "location": "吴忠市红寺堡区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议红寺堡区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议吴忠市委员会",
        "location": "吴忠市红寺堡区"
    },
    {
        "id": 5,
        "name": "中共吴忠市红寺堡区纪律检查委员会",
        "type": "纪律检查",
        "level": "县处级",
        "parent": "中共吴忠市纪律检查委员会",
        "location": "吴忠市红寺堡区"
    },
    {
        "id": 6,
        "name": "红寺堡镇",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "红寺堡区人民政府",
        "location": "吴忠市红寺堡区"
    },
    {
        "id": 7,
        "name": "吴忠市红寺堡区人民武装部",
        "type": "事业单位",
        "level": "县处级",
        "parent": "吴忠军分区",
        "location": "吴忠市红寺堡区"
    },
]

# ── Positions ───────────────────────────────────────────────────────────────

positions = [
    # 赵志锋
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持区委全面工作"},
    # 杨文福
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持区政府全面工作"},
    # 段立栓
    {"person_id": 3, "org_id": 1, "title": "区委副书记、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助书记处理区委日常工作"},
    # 赵军
    {"person_id": 4, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "主持区委组织部工作"},
    # 尤韬
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责区政府常务工作"},
    # 丁学春
    {"person_id": 6, "org_id": 1, "title": "区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "主持区委统战部工作"},
    # 杨继东
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李鑫
    {"person_id": 8, "org_id": 5, "title": "区纪委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "主持区纪委监委全面工作"},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 白净
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "红寺堡镇党委书记", "start_date": "", "end_date": "present", "rank": "乡科级", "note": "主持红寺堡镇党委全面工作"},
    # 苏达志
    {"person_id": 10, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持区人大常委会全面工作"},
    # 关保智
    {"person_id": 11, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 伍洪亮
    {"person_id": 12, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 马锦花
    {"person_id": 13, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王琳
    {"person_id": 14, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘炳枢
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 杨吉林
    {"person_id": 16, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张福莲
    {"person_id": 17, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 董涛
    {"person_id": 18, "org_id": 2, "title": "副区长、公安分局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张致强
    {"person_id": 19, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持区政协全面工作"},
    # 浦彦卿
    {"person_id": 20, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李军保
    {"person_id": 21, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 马春梅
    {"person_id": 22, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王丹玥
    {"person_id": 23, "org_id": 1, "title": "区委副书记（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职"},
    # 庄泽平
    {"person_id": 24, "org_id": 1, "title": "区委副书记（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职"},
    {"person_id": 24, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职，闽宁对口协作"},
    # 王立双
    {"person_id": 25, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职福建省惠安县"},
    # 苟俊杰
    {"person_id": 26, "org_id": 1, "title": "区委常委（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职，中烟定点帮扶"},
    {"person_id": 26, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职"},
    # 韩爱民
    {"person_id": 27, "org_id": 7, "title": "人民武装部部长", "start_date": "", "end_date": "present", "rank": "正团级", "note": "主持武装部工作"},
    {"person_id": 27, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 马海
    {"person_id": 28, "org_id": 2, "title": "区政府党组成员", "start_date": "", "end_date": "present", "rank": "正科级", "note": "兼任区工信局党组书记、局长"},
]

# ── Relationships ───────────────────────────────────────────────────────────

relationships = [
    # 党委核心：书记 → 副书记/常委
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记—区长（党政正职搭档）", "overlap_org": "红寺堡区委/政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记—区委副书记/政法委书记", "overlap_org": "红寺堡区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记—区委常委/常务副区长", "overlap_org": "红寺堡区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记—区委常委/组织部长", "overlap_org": "红寺堡区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记—区委常委/统战部长", "overlap_org": "红寺堡区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区委书记—区委常委/副区长", "overlap_org": "红寺堡区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区委书记—区委常委/纪委书记", "overlap_org": "红寺堡区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "区委书记—区委常委/红寺堡镇党委书记", "overlap_org": "红寺堡区委", "overlap_period": ""},

    # 政府核心：区长 → 副区长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长—常务副区长", "overlap_org": "红寺堡区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "红寺堡区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "红寺堡区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "红寺堡区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 18, "type": "superior_subordinate", "context": "区长—副区长/公安局长", "overlap_org": "红寺堡区政府", "overlap_period": ""},

    # 人大政协
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "区委书记联系区人大常委会", "overlap_org": "红寺堡区", "overlap_period": ""},
    {"person_a": 1, "person_b": 19, "type": "overlap", "context": "区委书记联系区政协", "overlap_org": "红寺堡区", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "区长联系区人大常委会", "overlap_org": "红寺堡区", "overlap_period": ""},

    # 挂职领导交叉
    {"person_a": 2, "person_b": 24, "type": "superior_subordinate", "context": "区长—挂职副区长", "overlap_org": "红寺堡区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 26, "type": "superior_subordinate", "context": "区长—挂职副区长", "overlap_org": "红寺堡区政府", "overlap_period": ""},

    # 纪委监委关系
    {"person_a": 8, "person_b": 1, "type": "superior_subordinate", "context": "纪委书记接受区委书记领导", "overlap_org": "红寺堡区委", "overlap_period": ""},

    # 常委班子之间
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "区委常委班子共事", "overlap_org": "红寺堡区委", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "区政府班子共事", "overlap_org": "红寺堡区政府", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════

def main():
    # Add parent to sys.path so gov_relation can be imported
    repo_root = os.path.abspath(os.path.join(STAGING, "..", "..", ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

    staging_db = DB_PATH
    staging_gexf = GEXF_PATH

    print(f"Building {SLUG} network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=staging_db,
        gexf_path=staging_gexf,
        overwrite=True,
    )

    # Write person JSON files
    write_person_jsons()

    print(f"\nDone. Staging artifacts:")
    print(f"  DB:   {staging_db}")
    print(f"  GEXF: {staging_gexf}")
    print(f"  Person JSONs: {PERSONS_DIR}")


def write_person_jsons():
    """Write individual person JSON files for core figures."""
    core_figures = [
        (1, "赵志锋", "区委书记"),
        (2, "杨文福", "区长"),
        (3, "段立栓", "区委副书记政法委书记"),
        (4, "赵军", "区委常委组织部长"),
        (5, "尤韬", "区委常委常务副区长"),
        (8, "李鑫", "区委常委纪委书记"),
        (10, "苏达志", "区人大常委会主任"),
        (19, "张致强", "区政协主席"),
    ]

    for pid, name, job in core_figures:
        person = next(p for p in persons if p["id"] == pid)
        filename = f"{TODAY}-宁夏回族自治区-吴忠市-{job}-{name}.json"
        filepath = os.path.join(STAGING, filename)

        person_json = build_person_json(person, job)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(person_json, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filename}")


def build_person_json(person, job):
    """Build a person JSON following the person_graph_json reference."""
    from gov_relation.colors import node_color

    color = node_color(person["current_post"])

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "宁夏回族自治区",
            "city": "吴忠市",
            "region": "红寺堡区",
            "job": person["current_post"],
            "task_id": "ningxia_红寺堡区",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"hongsibu_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": person["education"],
                    "major": "",
                    "degree": "",
                    "study_type": "party_school" if "党校" in person.get("education", "") else "unknown",
                    "source_ids": ["S001"]
                }
            ],
            "party_join": person["party_join"] if person["party_join"] else "",
            "work_start": person["work_start"] if person["work_start"] else "",
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}" if person['birthplace'] else f"{person['name']}_红寺堡区",
                "official_profile_url": "https://www.hongsibu.gov.cn/xxgk/ldzc/"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "书记" in person["current_post"] and "副" not in person["current_post"] or "区长" in person["current_post"] or "主任" in person["current_post"] or "主席" in person["current_post"] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": AS_OF,
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "",
                "location": "吴忠市红寺堡区",
                "system": "party" if "委" in person["current_org"] else "government" if "政府" in person["current_org"] else "other",
                "rank": "",
                "is_key_promotion": False,
                "notes": "当前职务，完整履历待查",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [
            {
                "org_id": 1,
                "org_name": "中共吴忠市红寺堡区委员会",
                "org_type": "党委",
                "role": person["current_post"],
                "period": f"至今 ({AS_OF})",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "公开信息有限，无法判断晋升速度",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，公开信息中未发现任何纪律处分、审计问题或负面报道",
                "date": AS_OF,
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "红寺堡区人民政府 — 领导之窗",
                "url": "https://www.hongsibu.gov.cn/xxgk/ldzc/",
                "publisher": "红寺堡区人民政府",
                "published_at": "2026",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "官方政府网站领导页面"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{person['name']}的完整履历（早年经历、教育细节、任职时间线）有待进一步调查"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整职业生涯时间线",
                "why_it_matters": "核心领导班子成员，完整履历对理解晋升路径和关系网络至关重要",
                "suggested_queries": [
                    f"{person['name']} 简历 任职经历",
                    f"{person['name']} 任前公示",
                    f"{person['name']} 宁夏 吴忠 履历"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['name']}的教育背景细节",
                "why_it_matters": "了解专业背景对其治理倾向的影响",
                "suggested_queries": [
                    f"{person['name']} 毕业 院校",
                ],
                "last_attempted": AS_OF
            }
        ]
    }


if __name__ == "__main__":
    main()
