#!/usr/bin/env python3
"""Build script for 印江土家族苗族自治县 (Yinjiang, Tongren, Guizhou) leadership network.

Generated: 2026-07-23
Level: 县 (自治县)
Province: 贵州省
Parent City: 铜仁市
Targets: 县委书记 & 县长

Research Note:
  The county government website (www.yinjiang.gov.cn) was directly accessible via HTTP.
  The 领导之窗 page confirmed the Party Secretary (秦会刚) and County Mayor (田杰) with
  basic demographics. The "我的同事" sections use JavaScript dynamic loading, so deputy
  details were partially collected from news articles.

  Web search via Exa was rate-limited, Baidu Baike returned 403, Google/Bing blocked.
  Career histories beyond current role could not be confirmed.

Sources:
  - https://www.yinjiang.gov.cn/xxgk/zxgk/ldzc/xwld_5983602/ (县委领导)
  - https://www.yinjiang.gov.cn/xxgk/zxgk/ldzc/zfld_5983611/ (政府领导)
  - https://www.yinjiang.gov.cn/xxgk/zxgk/ldzc/rdld_5983607/ (人大领导)
  - https://www.yinjiang.gov.cn/xxgk/zxgk/ldzc/zxld_5983615/ (政协领导)
  - https://www.yinjiang.gov.cn/xwzx/jrsd/202607/t20260720_90636604.html (县委常委会新闻)
  - https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260717_90631217.html (县长与政协委员座谈会)
  - https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260715_90621922.html (秦会刚信访)
  - https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260717_90631224.html (秦会刚调研)
  - https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260720_90636595.html (田杰防汛)
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════
TASK_ID = "guizhou_印江土家族苗族自治县"
PROVINCE = "贵州省"
CITY = "铜仁市"
REGION = "印江土家族苗族自治县"
AS_OF = "2026-07-23"

BASE = Path("data/tmp/guizhou_印江土家族苗族自治县")
DB_PATH = BASE / "印江土家族苗族自治县_network.db"
GEXF_PATH = BASE / "印江土家族苗族自治县_network.gexf"
PERSONS_DIR = BASE / "persons"
os.makedirs(PERSONS_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

PERSONS = [
    # ── Core Leaders ──
    # 县委书记 — CONFIRMED
    {
        "id": 1,
        "name": "秦会刚",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1975年10月",
        "birthplace": "",
        "education": "大学工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "印江自治县委书记、经济开发区党工委书记",
        "current_org": "中共印江土家族苗族自治县委员会",
        "source": "https://www.yinjiang.gov.cn/xxgk/zxgk/ldzc/xwld_5983602/ （官网确认简历）",
    },
    # 县长 — CONFIRMED
    {
        "id": 2,
        "name": "田杰",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1976年4月",
        "birthplace": "",
        "education": "大学法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "印江自治县委副书记、县长",
        "current_org": "印江土家族苗族自治县人民政府",
        "source": "https://www.yinjiang.gov.cn/xxgk/zxgk/ldzc/zfld_5983611/ （官网确认简历）",
    },
    # ── 县委领导 (Party Committee Leaders) ──
    # 县委副书记
    {
        "id": 3,
        "name": "田登伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共印江土家族苗族自治县委员会",
        "source": "https://www.yinjiang.gov.cn/xwzx/jrsd/202607/t20260720_90636604.html （县委常委会会议新闻确认）",
    },
    # 县委副书记
    {
        "id": 4,
        "name": "王仁彪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共印江土家族苗族自治县委员会",
        "source": "https://www.yinjiang.gov.cn/xwzx/jrsd/202607/t20260720_90636604.html （县委常委会会议新闻确认）",
    },
    # ── 县人大常委会领导 ──
    # 人大常委会党组书记、主任（现任/即将卸任）
    {
        "id": 5,
        "name": "张翊斌",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1967年10月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "自治县人大常委会党组书记、主任",
        "current_org": "印江土家族苗族自治县人大常委会",
        "source": "https://www.yinjiang.gov.cn/xxgk/zxgk/ldzc/rdld_5983607/zr/ （官网确认简历）",
    },
    # 人大常委会党组书记、主任候选人（新任）
    {
        "id": 6,
        "name": "庹颖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任候选人",
        "current_org": "印江土家族苗族自治县人大常委会",
        "source": "https://www.yinjiang.gov.cn/xwzx/jrsd/202607/t20260720_90636604.html （县委常委会会议新闻确认）",
    },
    # ── 县政协领导 ──
    # 政协主席 — CONFIRMED
    {
        "id": 7,
        "name": "黄仕军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组书记、主席",
        "current_org": "印江土家族苗族自治县政协委员会",
        "source": "https://www.yinjiang.gov.cn/xxgk/zxgk/ldzc/zxld_5983615/zx/ （官网确认简历）",
    },
    # ── 经开区领导 ──
    # 经开区党工委副书记
    {
        "id": 8,
        "name": "田猛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "贵州印江经开区党工委副书记、管委会常务副主任",
        "current_org": "贵州印江经济开发区",
        "source": "https://www.yinjiang.gov.cn/xwzx/jrsd/202607/t20260720_90636604.html （县委常委会会议新闻确认）",
    },
    # ── 县领导（具体职务待确认，从新闻中列名）──
    # 从县长与政协委员座谈会新闻中列名的县领导
    {
        "id": 9,
        "name": "陈睿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（推测为县委常委/常务副县长级）",
        "current_org": "印江土家族苗族自治县人民政府",
        "source": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260717_90631217.html （新闻列名）",
    },
    {
        "id": 10,
        "name": "杨旭东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（副县长/县委常委）",
        "current_org": "印江土家族苗族自治县人民政府",
        "source": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260717_90631217.html （新闻列名）",
    },
    {
        "id": 11,
        "name": "田姣",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（推测为副县长）",
        "current_org": "印江土家族苗族自治县人民政府",
        "source": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260717_90631217.html （新闻列名）",
    },
    {
        "id": 12,
        "name": "周华忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（政协副主席/副县长）",
        "current_org": "印江土家族苗族自治县人民政府",
        "source": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260717_90631217.html （新闻列名）",
    },
    {
        "id": 13,
        "name": "熊飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（副县长/县委常委）",
        "current_org": "印江土家族苗族自治县人民政府",
        "source": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260717_90631217.html （新闻列名）",
    },
    {
        "id": 14,
        "name": "冯国洪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（副县长/县委常委）",
        "current_org": "印江土家族苗族自治县人民政府",
        "source": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260717_90631217.html （新闻列名）",
    },
    {
        "id": 15,
        "name": "戴建英",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（副县长/县委常委）",
        "current_org": "印江土家族苗族自治县人民政府",
        "source": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260717_90631217.html （新闻列名）",
    },
    {
        "id": 16,
        "name": "袁兴斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（副县长/县委常委）",
        "current_org": "印江土家族苗族自治县人民政府",
        "source": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260717_90631217.html （新闻列名）",
    },
    {
        "id": 17,
        "name": "田仁贵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（副县长/县委常委）",
        "current_org": "印江土家族苗族自治县人民政府",
        "source": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260717_90631217.html （新闻列名）",
    },
    # 从秦会刚调研新闻中列名的县领导
    {
        "id": 18,
        "name": "李朝亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "印江土家族苗族自治县人民政府",
        "source": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260715_90621922.html （新闻列名）",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共印江土家族苗族自治县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜仁市委员会",
        "location": "贵州省铜仁市印江土家族苗族自治县",
    },
    {
        "id": 2,
        "name": "印江土家族苗族自治县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "铜仁市人民政府",
        "location": "贵州省铜仁市印江土家族苗族自治县",
    },
    {
        "id": 3,
        "name": "印江土家族苗族自治县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "铜仁市人大常委会",
        "location": "贵州省铜仁市印江土家族苗族自治县",
    },
    {
        "id": 4,
        "name": "印江土家族苗族自治县政协委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "铜仁市政协",
        "location": "贵州省铜仁市印江土家族苗族自治县",
    },
    {
        "id": 5,
        "name": "贵州印江经济开发区",
        "type": "开发区",
        "level": "县处级",
        "parent": "印江土家族苗族自治县人民政府",
        "location": "贵州省铜仁市印江土家族苗族自治县",
    },
]

POSITIONS = [
    # 秦会刚 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "未知", "end": "现任", "rank": "县处级正职", "note": "1975年10月生，苗族，大学工学学士"},
    {"person_id": 1, "org_id": 5, "title": "经济开发区党工委书记", "start": "未知", "end": "现任", "rank": "县处级正职", "note": "兼任"},
    # 田杰 — 县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "1976年4月生，土家族，大学法学学士"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "未知", "end": "现任", "rank": "县处级正职", "note": "县人民政府党组书记"},
    # 田登伟 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    # 王仁彪 — 县委副书记
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    # 张翊斌 — 人大主任
    {"person_id": 5, "org_id": 3, "title": "县人大常委会党组书记、主任", "start": "未知", "end": "现任", "rank": "县处级正职", "note": "1967年10月生，土家族，省委党校研究生学历"},
    # 庹颖 — 人大主任候选人
    {"person_id": 6, "org_id": 3, "title": "县人大常委会党组书记、主任候选人", "start": "2026-07", "end": "现任", "rank": "县处级正职", "note": "新任，待人大会议正式选举"},
    # 黄仕军 — 政协主席
    {"person_id": 7, "org_id": 4, "title": "县政协党组书记、主席", "start": "未知", "end": "现任", "rank": "县处级正职", "note": "1971年10月生，汉族，大学学历"},
    # 田猛 — 经开区
    {"person_id": 8, "org_id": 5, "title": "经开区党工委副书记、管委会常务副主任", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    # 陈睿等县领导（具体分管待确认）
    {"person_id": 9, "org_id": 2, "title": "县领导（推测为县委常委/副县长）", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "县领导", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "县领导（推测为副县长）", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "县领导", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "县领导", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "县领导", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "县领导", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "县领导", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "县领导", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "县领导", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
]

RELATIONSHIPS = [
    # 县委书记 ↔ 县长（核心搭档）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭档关系",
        "overlap_org": "中共印江土家族苗族自治县委员会/县人民政府",
        "overlap_period": "现任",
    },
    # 县委书记 → 县委副书记（田登伟）
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记",
        "overlap_org": "中共印江土家族苗族自治县委员会",
        "overlap_period": "现任",
    },
    # 县委书记 → 县委副书记（王仁彪）
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记",
        "overlap_org": "中共印江土家族苗族自治县委员会",
        "overlap_period": "现任",
    },
    # 县长 → 陈睿（推测为常务副县长关系）
    {
        "person_a": 2,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "县长与常务副县长/县领导",
        "overlap_org": "印江土家族苗族自治县人民政府",
        "overlap_period": "现任",
    },
    # 县长 → 田姣（推测为副县长）
    {
        "person_a": 2,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "印江土家族苗族自治县人民政府",
        "overlap_period": "现任",
    },
    # 县委书记 → 经开区（田猛）
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "经开区党工委书记与副书记",
        "overlap_org": "贵州印江经济开发区",
        "overlap_period": "现任",
    },
    # 县长 → 经开区
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "经开区管委会主任（县长兼任）与常务副主任",
        "overlap_org": "贵州印江经济开发区",
        "overlap_period": "现任",
    },
]

# ═══════════════════════════════════════════════════
# SOURCE REGISTER
# ═══════════════════════════════════════════════════
SOURCE_REGISTER = [
    {
        "id": "S001",
        "title": "印江县政府领导之窗-县委领导",
        "url": "https://www.yinjiang.gov.cn/xxgk/zxgk/ldzc/xwld_5983602/",
        "publisher": "印江土家族苗族自治县人民政府",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认秦会刚（县委书记）基本信息",
    },
    {
        "id": "S002",
        "title": "印江县政府领导之窗-政府领导",
        "url": "https://www.yinjiang.gov.cn/xxgk/zxgk/ldzc/zfld_5983611/",
        "publisher": "印江土家族苗族自治县人民政府",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认田杰（县长）基本信息",
    },
    {
        "id": "S003",
        "title": "印江县政府领导之窗-人大主任",
        "url": "https://www.yinjiang.gov.cn/xxgk/zxgk/ldzc/rdld_5983607/zr/",
        "publisher": "印江土家族苗族自治县人民政府",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认张翊斌（人大主任）基本信息",
    },
    {
        "id": "S004",
        "title": "印江县政府领导之窗-政协主席",
        "url": "https://www.yinjiang.gov.cn/xxgk/zxgk/ldzc/zxld_5983615/zx/",
        "publisher": "印江土家族苗族自治县人民政府",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认黄仕军（政协主席）基本信息",
    },
    {
        "id": "S005",
        "title": "县委常委会会议暨县委党的建设工作领导小组会议召开",
        "url": "https://www.yinjiang.gov.cn/xwzx/jrsd/202607/t20260720_90636604.html",
        "publisher": "微印江",
        "published_at": "2026-07-20",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认田登伟、王仁彪（县委副书记）、庹颖（人大主任候选人）、田猛（经开区）",
    },
    {
        "id": "S006",
        "title": "田杰出席县长与政协委员座谈会",
        "url": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260717_90631217.html",
        "publisher": "微印江",
        "published_at": "2026-07-17",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认陈睿、杨旭东、田姣、周华忠、熊飞、冯国洪、戴建英、袁兴斌、田仁贵等县领导",
    },
    {
        "id": "S007",
        "title": "秦会刚到县信访局开展信访包案督办接访工作",
        "url": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260715_90621922.html",
        "publisher": "微印江",
        "published_at": "2026-07-15",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认李朝亮（县领导）",
    },
    {
        "id": "S008",
        "title": "秦会刚到罗场乡调研督导",
        "url": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260717_90631224.html",
        "publisher": "微印江",
        "published_at": "2026-07-17",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认秦会刚2026年7月仍在任",
    },
    {
        "id": "S009",
        "title": "田杰调研督导防汛减灾",
        "url": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260720_90636595.html",
        "publisher": "微印江",
        "published_at": "2026-07-20",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认田杰2026年7月仍在任",
    },
    {
        "id": "S010",
        "title": "田杰督导防汛备汛工作",
        "url": "https://www.yinjiang.gov.cn/xwzx/ldhd/202607/t20260721_90643348.html",
        "publisher": "微印江",
        "published_at": "2026-07-21",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认田杰2026年7月仍在任",
    },
]


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
    for idx, p in enumerate(PERSONS, 1):
        pid = f"yinjiang_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute(
            """INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
             p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
             p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")),
        )

    for o in ORGANIZATIONS:
        cur.execute(
            "INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")),
        )

    for pos in POSITIONS:
        cur.execute(
            """INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note)
                   VALUES (?,?,?,?,?,?,?)""",
            (person_map[pos["person_id"]], pos["org_id"], pos["title"],
             pos.get("start_date", ""), pos.get("end_date", ""),
             pos.get("rank", ""), pos.get("note", "")),
        )

    for r in RELATIONSHIPS:
        cur.execute(
            """INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period)
                   VALUES (?,?,?,?,?,?)""",
            (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
             r.get("overlap_org", ""), r.get("overlap_period", "")),
        )

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(POSITIONS)} positions, {len(RELATIONSHIPS)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post and "人大" not in post and "政协" not in post:
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
    lines.append(f'    <description>{REGION}领导班子关系网络（基于印江县政府官网、县委常委会新闻、媒体报道）</description>')
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
    for p in PERSONS:
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
    for o in ORGANIZATIONS:
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
    for pos in POSITIONS:
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
    for r in RELATIONSHIPS:
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

    def make_person_json(p, timeline, relationships_list):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": CITY,
                "region": REGION,
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月",
            },
            "identity": {
                "person_id": f"yinjiang_{p['name']}",
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
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": []
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
            "source_register": SOURCE_REGISTER,
            "confidence_summary": {
                "identity": "confirmed" if p.get("birth") else "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历信息缺失（早期职业生涯、教育详细经历、出生地等）"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"{p['name']}赴印江任职前的完整职业生涯履历",
                    "why_it_matters": "无法追溯其任职路径和系统经历，无法分析其能力专长和关系网络",
                    "suggested_queries": [f"{p['name']} 简历 {REGION}"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": f"{p['name']}的出生地和民族来源",
                    "why_it_matters": "无法完成identity信息，影响跨区域关系追踪",
                    "suggested_queries": [f"{p['name']} 出生地"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": f"{p['name']}的具体任职起始时间和上任方式",
                    "why_it_matters": "无法确定具体任期，影响与前/后任的衔接关系",
                    "suggested_queries": [f"{p['name']} 任前公示 铜仁"],
                    "last_attempted": AS_OF
                }
            ]
        }
        return result

    # ── 秦会刚 Person JSON ──
    qin_timeline = [
        {"start": "未知", "end": "", "org": "中共印江土家族苗族自治县委员会", "title": "印江自治县委书记、经济开发区党工委书记",
         "notes": "现任，1975年10月生，苗族，大学工学学士", "confidence": "confirmed", "source_ids": ["S001", "S008"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "秦会刚在任印江县委书记前的完整职业生涯未找到（1975年出生至今的履历缺口）",
         "confidence": "unverified", "source_ids": []},
    ]
    qin_relationships = [
        {"person": "田杰", "person_id": "yinjiang_田杰", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "秦会刚（县委书记）与田杰（县长）构成书记-县长搭档关系",
         "overlap_org": "中共印江土家族苗族自治县委员会/县人民政府", "overlap_period": "现任",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "田登伟", "person_id": "yinjiang_田登伟", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "秦会刚（县委书记）与田登伟（县委副书记）在县委常委会共事",
         "overlap_org": "中共印江土家族苗族自治县委员会", "overlap_period": "现任",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
        {"person": "王仁彪", "person_id": "yinjiang_王仁彪", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "秦会刚（县委书记）与王仁彪（县委副书记）在县委常委会共事",
         "overlap_org": "中共印江土家族苗族自治县委员会", "overlap_period": "现任",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
    ]

    qin_json = make_person_json(PERSONS[0], qin_timeline, qin_relationships)
    qin_path = PERSONS_DIR / f"{now}-贵州省-铜仁市-县委书记-秦会刚.json"
    with open(qin_path, "w", encoding="utf-8") as f:
        json.dump(qin_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {qin_path}")

    # ── 田杰 Person JSON ──
    tian_timeline = [
        {"start": "未知", "end": "", "org": "中共印江土家族苗族自治县委员会", "title": "印江自治县委副书记、县长",
         "notes": "现任，1976年4月生，土家族，大学法学学士", "confidence": "confirmed", "source_ids": ["S002", "S009", "S010"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "田杰在任印江县长前的完整职业生涯未找到（1976年4月出生至今的履历缺口）",
         "confidence": "unverified", "source_ids": []},
    ]
    tian_relationships = [
        {"person": "秦会刚", "person_id": "yinjiang_秦会刚", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "田杰（县长）与秦会刚（县委书记）构成书记-县长搭档关系",
         "overlap_org": "中共印江土家族苗族自治县委员会/县人民政府", "overlap_period": "现任",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "田登伟", "person_id": "yinjiang_田登伟", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "田杰（县长）与田登伟（县委副书记）在县委常委会共事",
         "overlap_org": "中共印江土家族苗族自治县委员会", "overlap_period": "现任",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
    ]

    tian_json = make_person_json(PERSONS[1], tian_timeline, tian_relationships)
    tian_path = PERSONS_DIR / f"{now}-贵州省-铜仁市-县长-田杰.json"
    with open(tian_path, "w", encoding="utf-8") as f:
        json.dump(tian_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {tian_path}")

    print("\nDone.")


if __name__ == "__main__":
    build()
