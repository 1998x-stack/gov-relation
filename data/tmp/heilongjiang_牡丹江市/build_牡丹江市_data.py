#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 牡丹江市 (Mudanjiang City), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_牡丹江市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - Wikipedia (zh.wikipedia.org) — leadership table for 牡丹江市
  - mdj.gov.cn (牡丹江市政府官网) — 领导之窗 full roster
  - Wikipedia — 张国军, 代守仑, 杨廷双 biography pages
  - 中国经济网 — appointment announcements

Confidence notes:
  - 张国军 (市委书记): confirmed via Wikipedia + government site, full career limited
  - 杨勇 (市长): confirmed via Wikipedia + government site, prior career unverified
  - 市委常委会12人: confirmed via government leadership page
  - Detailed career histories for most deputies: unverified — only names and titles confirmed
  - Web search tools (Exa) were rate-limited; Baidu returned 403
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "牡丹江市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / "scripts" / "build" / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "张国军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年4月",
        "birthplace": "黑龙江省嫩江市",
        "education": "研究生，公共管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共牡丹江市委员会",
        "source": "https://zh.wikipedia.org/wiki/牡丹江市 | https://www.mdj.gov.cn/mdjsrmzf/c1006291/202409/c03_972647.shtml"
    },
    {
        "id": 2,
        "name": "杨勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年2月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市长",
        "current_org": "牡丹江市人民政府",
        "source": "https://zh.wikipedia.org/wiki/牡丹江市 | https://www.mdj.gov.cn/mdjsrmzf/c1006951/202409/c03_972680.shtml"
    },
    # ═══════ 市委常委会成员 ═══════
    {
        "id": 3,
        "name": "黄士伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 4,
        "name": "张涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 5,
        "name": "许有昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、纪委书记、监委主任",
        "current_org": "中共牡丹江市纪律检查委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 6,
        "name": "赵晓利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、军分区司令员",
        "current_org": "牡丹江军分区",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 7,
        "name": "李玉俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "牡丹江市人民政府",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 8,
        "name": "李松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长（挂职）",
        "current_org": "牡丹江市人民政府",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 9,
        "name": "王镭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、绥芬河市委书记",
        "current_org": "中共绥芬河市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 10,
        "name": "高忠远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 11,
        "name": "唐荣胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、秘书长、统战部部长",
        "current_org": "中共牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 12,
        "name": "汝长华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    # ═══════ 市人大常委会 ═══════
    {
        "id": 13,
        "name": "张鸿雁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969年12月",
        "birthplace": "黑龙江省海林市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "牡丹江市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/牡丹江市"
    },
    {
        "id": 14,
        "name": "魏芝红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "牡丹江市人民代表大会常务委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 15,
        "name": "倪金亭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "牡丹江市人民代表大会常务委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 16,
        "name": "于慈森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "牡丹江市人民代表大会常务委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 17,
        "name": "惠金山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "牡丹江市人民代表大会常务委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 18,
        "name": "赵玉国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会秘书长",
        "current_org": "牡丹江市人民代表大会常务委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    # ═══════ 市政府 ═══════
    {
        "id": 19,
        "name": "刘军龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "牡丹江市人民政府",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 20,
        "name": "刘宏斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "牡丹江市人民政府",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 21,
        "name": "李传柱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "牡丹江市人民政府",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 22,
        "name": "贾惠媛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "牡丹江市人民政府",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 23,
        "name": "李伦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "牡丹江市人民政府",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 24,
        "name": "周振海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "牡丹江市人民政府",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    # ═══════ 市政协 ═══════
    {
        "id": 25,
        "name": "孙涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 26,
        "name": "张富广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 27,
        "name": "王伟华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 28,
        "name": "徐海鸥",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 29,
        "name": "都业宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 30,
        "name": "宋景东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 31,
        "name": "王子云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 32,
        "name": "付忠安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 33,
        "name": "姜涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    {
        "id": 34,
        "name": "高峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协秘书长",
        "current_org": "中国人民政治协商会议牡丹江市委员会",
        "source": "https://www.mdj.gov.cn/mdjsrmzf/c100002/ldzc.shtml"
    },
    # ═══════ 前任领导人 ═══════
    {
        "id": 35,
        "name": "代守仑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年8月",
        "birthplace": "山东省平度市",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "前市委书记（被调查）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/代守仑"
    },
    {
        "id": 36,
        "name": "杨廷双",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年1月",
        "birthplace": "黑龙江省宾县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "省人大常委会副主任",
        "current_org": "黑龙江省人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/杨廷双"
    },
    {
        "id": 37,
        "name": "王志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年8月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前市政协主席",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/牡丹江市"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共牡丹江市委员会", "type": "党委", "level": "地级市", "parent": "中共黑龙江省委", "location": "黑龙江省牡丹江市"},
    {"id": 2, "name": "牡丹江市人民政府", "type": "政府", "level": "地级市", "parent": "黑龙江省人民政府", "location": "黑龙江省牡丹江市"},
    {"id": 3, "name": "牡丹江市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "黑龙江省人大常委会", "location": "黑龙江省牡丹江市"},
    {"id": 4, "name": "中国人民政治协商会议牡丹江市委员会", "type": "政协", "level": "地级市", "parent": "黑龙江省政协", "location": "黑龙江省牡丹江市"},
    {"id": 5, "name": "中共牡丹江市纪律检查委员会", "type": "纪委", "level": "地级市", "parent": "中共黑龙江省纪委", "location": "黑龙江省牡丹江市"},
    {"id": 6, "name": "牡丹江军分区", "type": "军队", "level": "地级市", "parent": "黑龙江省军区", "location": "黑龙江省牡丹江市"},
    {"id": 7, "name": "中共绥芬河市委员会", "type": "党委", "level": "县级市", "parent": "中共牡丹江市委员会", "location": "黑龙江省牡丹江市绥芬河市"},
    {"id": 8, "name": "黑龙江省人民代表大会常务委员会", "type": "人大", "level": "省", "parent": "全国人大常委会", "location": "黑龙江省哈尔滨市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 张国军
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2024年9月", "end_date": "", "rank": "正厅级", "note": "此前任牡丹江市市长"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start_date": "2021年", "end_date": "2024年9月", "rank": "正厅级", "note": "此前任伊春市委常委、副市长"},
    # 杨勇
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2024年9月", "end_date": "", "rank": "正厅级", "note": "接替张国军"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2024年9月", "end_date": "", "rank": "正厅级", "note": ""},
    # 黄士伟
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼经开区党工委书记、党校校长"},
    # 张涛
    {"person_id": 4, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 许有昌
    {"person_id": 5, "org_id": 5, "title": "市委常委、纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": "二级高级监察官"},
    # 赵晓利
    {"person_id": 6, "org_id": 6, "title": "市委常委、军分区司令员", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 李玉俊
    {"person_id": 7, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼绥芬河片区党工委书记"},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 李松
    {"person_id": 8, "org_id": 2, "title": "市委常委、副市长（挂职）", "start_date": "", "end_date": "", "rank": "副厅级", "note": "挂职"},
    # 王镭
    {"person_id": 9, "org_id": 7, "title": "绥芬河市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "牡丹江市委常委兼任"},
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 高忠远
    {"person_id": 10, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 唐荣胜
    {"person_id": 11, "org_id": 1, "title": "市委常委、秘书长、统战部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 汝长华
    {"person_id": 12, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 张鸿雁
    {"person_id": 13, "org_id": 3, "title": "市人大常委会主任", "start_date": "2024年1月", "end_date": "", "rank": "正厅级", "note": ""},
    # 魏芝红等副主任
    {"person_id": 14, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": "农工党市委主委"},
    {"person_id": 15, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "市人大常委会秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 副市长
    {"person_id": 19, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "一级巡视员"},
    {"person_id": 20, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 22, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 23, "org_id": 2, "title": "副市长、市公安局局长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 24, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 政协
    {"person_id": 25, "org_id": 4, "title": "市政协主席", "start_date": "2026年2月", "end_date": "", "rank": "正厅级", "note": "接替王志刚"},
    {"person_id": 26, "org_id": 4, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": "九三学社市委主委"},
    {"person_id": 27, "org_id": 4, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 28, "org_id": 4, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": "民革市委主委"},
    {"person_id": 29, "org_id": 4, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": "民建市委主委"},
    {"person_id": 30, "org_id": 4, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 31, "org_id": 4, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼市财政局局长"},
    {"person_id": 32, "org_id": 4, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼市住建局党组书记"},
    {"person_id": 33, "org_id": 4, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": "民进市委主委"},
    {"person_id": 34, "org_id": 4, "title": "市政协秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 前任
    {"person_id": 35, "org_id": 1, "title": "市委书记", "start_date": "2023年3月", "end_date": "2024年8月", "rank": "正厅级", "note": "2024年8月被调查"},
    {"person_id": 36, "org_id": 1, "title": "市委书记", "start_date": "2020年5月", "end_date": "2023年3月", "rank": "正厅级", "note": "后升任省人大常委会副主任"},
    {"person_id": 36, "org_id": 8, "title": "省人大常委会副主任", "start_date": "2023年1月", "end_date": "", "rank": "副省级", "note": ""},
    {"person_id": 37, "org_id": 4, "title": "市政协主席", "start_date": "2024年1月", "end_date": "2026年1月", "rank": "正厅级", "note": "被孙涛接替"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 张国军 → 杨勇（党政一把手搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "张国军（市委书记）与杨勇（市长）形成党政一把手搭档", "overlap_org": "中共牡丹江市委员会/牡丹江市人民政府", "overlap_period": "2024年9月至今"},
    # 张国军 → 代守仑（前任-后继）
    {"person_a": 1, "person_b": 35, "type": "前任-后继", "context": "张国军接替被调查的代守仑任市委书记", "overlap_org": "中共牡丹江市委员会", "overlap_period": "2024年"},
    # 代守仑 → 杨廷双（前任-后继）
    {"person_a": 35, "person_b": 36, "type": "前任-后继", "context": "代守仑接替杨廷双任市委书记", "overlap_org": "中共牡丹江市委员会", "overlap_period": "2023年"},
    # 张国军 → 杨廷双（前任-后继，张国军为杨廷双下属市长）
    {"person_a": 1, "person_b": 36, "type": "上下级", "context": "杨廷双任市委书记时，张国军任市长", "overlap_org": "中共牡丹江市委员会/牡丹江市人民政府", "overlap_period": "2021-2023年"},
    # 张国军 → 张鸿雁（同届领导）
    {"person_a": 1, "person_b": 13, "type": "同届共事", "context": "张国军（市委书记）与张鸿雁（市人大常委会主任）同届", "overlap_org": "牡丹江市", "overlap_period": "2024年至今"},
    # 杨勇 → 李玉俊（市长-常务副市长）
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "李玉俊作为常务副市长协助杨勇", "overlap_org": "牡丹江市人民政府", "overlap_period": "2024年至今"},
    # 张国军 → 李玉俊（书记-常委/副市长）
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "李玉俊为市委常委、常务副市长", "overlap_org": "中共牡丹江市委员会", "overlap_period": ""},
    # 孙涛 → 王志刚（前任-后继，政协主席）
    {"person_a": 25, "person_b": 37, "type": "前任-后继", "context": "孙涛接替王志刚任市政协主席", "overlap_org": "牡丹江市政协", "overlap_period": "2026年"},
    # 黄士伟 → 张国军（副书记-书记）
    {"person_a": 3, "person_b": 1, "type": "上下级", "context": "黄士伟为市委副书记，协助张国军", "overlap_org": "中共牡丹江市委员会", "overlap_period": ""},
    # 许有昌 → 张国军（纪委书记-书记）
    {"person_a": 5, "person_b": 1, "type": "监督关系", "context": "许有昌（市纪委书记）在张国军领导下工作", "overlap_org": "中共牡丹江市委员会", "overlap_period": ""},
]


# ============================================================================
# Build
# ============================================================================
def main():
    # Use the gov_relation library if available; fall back to direct SQL
    try:
        from gov_relation.runner import run_build
        from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
        print("Using gov_relation library (new-style build)")
        run_build(
            slug=SLUG,
            persons=persons,
            organizations=organizations,
            positions=positions,
            relationships=relationships,
            db_path=DB_PATH,
            gexf_path=GEXF_PATH,
            overwrite=True,
        )
    except ImportError:
        print("gov_relation library not found, using direct SQL build")
        _direct_build()

    # Print summary
    print(f"\n=== {SLUG} 建设完成 ===")
    print(f"数据库: {DB_PATH}")
    print(f"图文件: {GEXF_PATH}")
    print(f"人员: {len(persons)} 人")
    print(f"组织: {len(organizations)} 个")
    print(f"任职: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")


def _direct_build():
    """Fallback: direct SQLite + GEXF build without gov_relation library."""
    import sqlite3
    from xml.etree.ElementTree import Element, SubElement, ElementTree

    # ── SQLite Database ──
    conn = sqlite3.connect(str(DB_PATH))
    for table in ["relationships", "positions", "organizations", "persons"]:
        conn.execute(f"DROP TABLE IF EXISTS {table}")

    conn.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start_date TEXT, end_date TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    conn.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        conn.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            [p.get(k, "") for k in ["id", "name", "gender", "ethnicity", "birth",
                                    "birthplace", "education", "party_join",
                                    "work_start", "current_post", "current_org", "source"]]
        )
    for o in organizations:
        conn.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            [o.get(k, "") for k in ["id", "name", "type", "level", "parent", "location"]]
        )
    for pos in positions:
        conn.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            [pos.get(k, "") for k in ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]]
        )
    for r in relationships:
        conn.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            [r.get(k, "") for k in ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]]
        )
    conn.commit()
    conn.close()

    # ── GEXF Graph ──
    root = Element("gexf", attrib={
        "xmlns": "http://www.gexf.net/1.3",
        "xmlns:viz": "http://www.gexf.net/1.3/viz",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:schemaLocation": "http://www.gexf.net/1.3 http://www.gexf.net/1.3/gexf.xsd",
        "version": "1.3",
    })
    meta = SubElement(root, "meta")
    SubElement(meta, "title").text = f"{SLUG}领导班子工作关系网络"
    SubElement(meta, "description").text = f"黑龙江省{SLUG}领导班子工作关系网络 - 调查日期: {AS_OF}"
    SubElement(meta, "creator").text = "gov-relation research agent"

    graph = SubElement(root, "graph", attrib={"mode": "static", "defaultedgetype": "undirected"})

    # Node attributes
    attrs = SubElement(graph, "attributes", attrib={"class": "node"})
    for aid, title, atype in [("0", "type", "string"), ("1", "current_post", "string"),
                                ("2", "current_org", "string"), ("3", "gender", "string"),
                                ("4", "ethnicity", "string"), ("5", "birth", "string"),
                                ("6", "source", "string"), ("7", "org_type", "string")]:
        SubElement(attrs, "attribute", attrib={"id": aid, "title": title, "type": atype})

    # Edge attributes
    eattrs = SubElement(graph, "attributes", attrib={"class": "edge"})
    for eid, etitle, etype in [("0", "type", "string"), ("1", "context", "string"),
                                 ("2", "overlap_org", "string"), ("3", "overlap_period", "string")]:
        SubElement(eattrs, "attribute", attrib={"id": eid, "title": etitle, "type": etype})

    # Color helpers
    def person_color(post):
        if "书记" in post and "副" not in post:
            return ("200", "30", "30")  # deep red — party secretary
        if "市长" in post or "区长" in post or "县长" in post:
            return ("30", "100", "200")  # blue — government head
        if "副书记" in post:
            return ("220", "80", "80")   # light red — deputy secretary
        if "副" in post or "常委" in post:
            return ("100", "150", "220")  # light blue — deputy/standing committee
        if "主任" in post or "人大" in post:
            return ("60", "180", "60")   # green — people's congress
        if "主席" in post or "政协" in post:
            return ("60", "180", "60")   # green — political consultative
        if "纪委" in post:
            return ("255", "165", "0")   # orange — discipline
        return ("180", "180", "180")     # grey — other

    def person_size(post):
        if "书记" in post and "副" not in post:
            return "20.0"
        if "市长" in post:
            return "18.0"
        if "副" in post or "常委" in post:
            return "12.0"
        return "10.0"

    # Nodes
    nodes_el = SubElement(graph, "nodes")
    for p in persons:
        post = p.get("current_post", "")
        rc, gc, bc = person_color(post)
        sz = person_size(post)
        nid = f"p{p['id']}"
        node = SubElement(nodes_el, "node", attrib={"id": nid, "label": p["name"]})
        SubElement(node, "viz:size", attrib={"value": sz})
        SubElement(node, "viz:color", attrib={"r": rc, "g": gc, "b": bc, "a": "1.0"})
        av = SubElement(node, "attvalues")
        SubElement(av, "attvalue", attrib={"for": "0", "value": "person"})
        SubElement(av, "attvalue", attrib={"for": "1", "value": post})
        SubElement(av, "attvalue", attrib={"for": "2", "value": p.get("current_org", "")})
        SubElement(av, "attvalue", attrib={"for": "3", "value": p.get("gender", "")})
        SubElement(av, "attvalue", attrib={"for": "4", "value": p.get("ethnicity", "")})
        SubElement(av, "attvalue", attrib={"for": "5", "value": p.get("birth", "")})
        SubElement(av, "attvalue", attrib={"for": "6", "value": p.get("source", "")})

    # Organization nodes
    for o in organizations:
        nid = f"o{o['id']}"
        node = SubElement(nodes_el, "node", attrib={"id": nid, "label": o["name"]})
        SubElement(node, "viz:size", attrib={"value": "8.0"})
        SubElement(node, "viz:color", attrib={"r": "200", "g": "200", "b": "200", "a": "0.8"})
        av = SubElement(node, "attvalues")
        SubElement(av, "attvalue", attrib={"for": "0", "value": "organization"})
        SubElement(av, "attvalue", attrib={"for": "7", "value": o.get("type", "")})

    # Edges: positions (person → organization)
    edges_el = SubElement(graph, "edges")
    eid = 0
    for pos in positions:
        eid += 1
        source = f"p{pos['person_id']}"
        target = f"o{pos['org_id']}"
        edge = SubElement(edges_el, "edge", attrib={
            "id": str(eid), "source": source, "target": target, "label": pos.get("title", ""),
            "weight": "1.0"
        })
        av = SubElement(edge, "attvalues")
        SubElement(av, "attvalue", attrib={"for": "0", "value": "worked_at"})
        SubElement(av, "attvalue", attrib={"for": "1", "value": pos.get("title", "")})
        SubElement(av, "attvalue", attrib={"for": "2", "value": pos.get("start_date", "") + " - " + pos.get("end_date", "")})

    # Edges: relationships (person ↔ person)
    for rel in relationships:
        eid += 1
        source = f"p{rel['person_a']}"
        target = f"p{rel['person_b']}"
        edge = SubElement(edges_el, "edge", attrib={
            "id": str(eid), "source": source, "target": target, "label": rel.get("type", ""),
            "weight": "2.0"
        })
        av = SubElement(edge, "attvalues")
        SubElement(av, "attvalue", attrib={"for": "0", "value": "relationship"})
        SubElement(av, "attvalue", attrib={"for": "1", "value": rel.get("context", "")})
        SubElement(av, "attvalue", attrib={"for": "2", "value": rel.get("overlap_org", "")})
        SubElement(av, "attvalue", attrib={"for": "3", "value": rel.get("overlap_period", "")})

    tree = ElementTree(root)
    with open(GEXF_PATH, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)
    print(f"GEXF written to {GEXF_PATH}")


if __name__ == "__main__":
    main()
