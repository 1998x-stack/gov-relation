#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 来宾市 (Laibin City), 广西壮族自治区.

Investigation date: 2026-08-05
Task ID: guangxi_来宾市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.laibin.gov.cn (来宾市人民政府门户网站) 政务动态/新闻 — 确认现任班子（2026-07/08）
  - district.ce.cn (中国经济网 广西党政领导人物库) — 周春涌任代市长、廖和明辞去市长（2026-07-31）、
    周春涌任市委副书记、市政府党组书记（2026-07-30）、方毅任来宾市委书记（2025-09）
  - baike.so.com (360百科) — 方毅、廖和明、文东福、吴晓丽、何朝建人物履历
  - 澎湃/观察者/网易/新浪 — 方毅跨省调任报道（2025-09-29）

Confidence notes:
  - 方毅 (市委书记): confirmed via government news + 中国经济网 + 360百科（身份、跨省调任2025-09）
  - 周春涌 (代市长): confirmed via 中国经济网 2026-07-30/31 任命公告（瑶族，1975.4，湖北钟山，曾任贵港市委常委、统战部部长）
  - 文东福 (人大主任): 360百科确认（自治区党委组织部出道；曾任梧州/柳州组织部长）
  - 吴晓丽 (政协主席): 360百科确认（女，壮族，1973.11，东兰人；2021.09 当选来宾市委副书记）
  - 前任市委书记何朝建: 2025-09-12 被查、2026-05-10 双开（重大廉洁风险信号）
  - 前任市长廖和明: 2026-07-31 辞去市长（工作变动），去向待查
  - 部分职务分工、早期教育背景存在缺口 → open_questions 已标注
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "来宾市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 四大班子核心领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "方毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年1月",
        "birthplace": "浙江省杭州市淳安县",
        "education": "在职研究生，法学博士",
        "party_join": "1993年12月",
        "work_start": "1994年8月",
        "current_post": "市委书记",
        "current_org": "中共来宾市委员会",
        "source": "https://district.ce.cn/newarea/sddy/202509/t20250930_39394832.shtml"
    },
    {
        "id": 2,
        "name": "周春涌",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth": "1975年4月",
        "birthplace": "广西壮族自治区贺州市钟山县",
        "education": "大学（山东财政学院）",
        "party_join": "2001年5月",
        "work_start": "1997年8月",
        "current_post": "市委副书记、代市长",
        "current_org": "来宾市人民政府",
        "source": "https://district.ce.cn/newarea/sddy/202607/t20260731_3120716.shtml"
    },
    {
        "id": 3,
        "name": "文东福",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年8月",
        "birthplace": "广西壮族自治区桂林市灵川县",
        "education": "大学，法学硕士",
        "party_join": "1996年11月",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "来宾市人民代表大会常务委员会",
        "source": "https://baike.so.com/doc/30477840-32120282.html"
    },
    {
        "id": 4,
        "name": "吴晓丽",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "1973年11月",
        "birthplace": "广西壮族自治区河池市东兰县",
        "education": "研究生，公共管理硕士",
        "party_join": "1995年3月",
        "work_start": "1995年7月",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议来宾市委员会",
        "source": "https://baike.so.com/doc/6385328-6598981.html"
    },
    {
        "id": 5,
        "name": "蒋卫生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共来宾市委员会",
        "source": "https://www.laibin.gov.cn/xwzx/zwdt/t27982170.shtml"
    },
    {
        "id": 6,
        "name": "甘永辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共来宾市委员会",
        "source": "https://www.laibin.gov.cn/xwzx/zwdt/t27982170.shtml"
    },
    {
        "id": 7,
        "name": "梁仁省",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、秘书长",
        "current_org": "中共来宾市委员会",
        "source": "https://www.laibin.gov.cn/xwzx/zwdt/t27982170.shtml"
    },
    {
        "id": 8,
        "name": "农化",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "来宾市人民政府",
        "source": "https://www.laibin.gov.cn/xwzx/zwdt/t27982170.shtml"
    },
    {
        "id": 9,
        "name": "彭斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共来宾市委员会",
        "source": "https://www.laibin.gov.cn/xwzx/zwdt/t27982186.shtml"
    },
    {
        "id": 10,
        "name": "徐广成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记",
        "current_org": "中共来宾市纪律检查委员会",
        "source": "https://www.laibin.gov.cn/xwzx/zwdt/t27982170.shtml"
    },
    {
        "id": 11,
        "name": "韦焕清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "来宾市人民政府",
        "source": "https://www.laibin.gov.cn/xwzx/zwdt/t27982186.shtml"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任领导（含落马）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "何朝建",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1966年5月",
        "birthplace": "广西壮族自治区百色市田阳区",
        "education": "在职研究生，工学学士，高级工程师",
        "party_join": "1998年3月",
        "work_start": "1990年7月",
        "current_post": "前任市委书记（2021.12—2025.09，被查）",
        "current_org": "广西壮族自治区纪委监委",
        "source": "https://baike.so.com/doc/2996897-3160644.html"
    },
    {
        "id": 13,
        "name": "廖和明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年6月",
        "birthplace": "广西壮族自治区桂林市全州县",
        "education": "广西区委党校研究生，文学学士",
        "party_join": "1992年12月",
        "work_start": "1991年7月",
        "current_post": "前任市长（2021.08—2026.07，已辞）",
        "current_org": "（工作变动待查）",
        "source": "https://district.ce.cn/newarea/sddy/202607/t20260731_3120716.shtml"
    },
    {
        "id": 14,
        "name": "沙君俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原市人大常委会主任（2025.07被查）",
        "current_org": "广西壮族自治区纪委监委",
        "source": "https://baike.so.com/doc/4750115-4965436.html"
    },
    {
        "id": 15,
        "name": "农生文",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记（2021.09任期上任）",
        "current_org": "中共来宾市委员会（第五届）",
        "source": "https://baike.so.com/doc/29894739-31482038.html"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共来宾市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共广西壮族自治区委员会",
        "location": "来宾市"
    },
    {
        "id": 2,
        "name": "来宾市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "广西壮族自治区人民政府",
        "location": "来宾市"
    },
    {
        "id": 3,
        "name": "来宾市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级",
        "parent": "广西壮族自治区人民代表大会常务委员会",
        "location": "来宾市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议来宾市委员会",
        "type": "政协",
        "level": "地级",
        "parent": "中国人民政治协商会议广西壮族自治区委员会",
        "location": "来宾市"
    },
    {
        "id": 5,
        "name": "中共来宾市纪律检查委员会（市监委）",
        "type": "纪委",
        "level": "地级",
        "parent": "中共广西壮族自治区纪律检查委员会",
        "location": "来宾市"
    },
    {
        "id": 6,
        "name": "中共杭州市委员会",
        "type": "党委",
        "level": "副省级",
        "parent": "中共浙江省委员会",
        "location": "杭州市"
    },
    {
        "id": 7,
        "name": "杭州市人民政府",
        "type": "政府",
        "level": "副省级",
        "parent": "浙江省人民政府",
        "location": "杭州市"
    },
    {
        "id": 8,
        "name": "桐庐县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "杭州市人民政府",
        "location": "杭州市桐庐县"
    },
    {
        "id": 9,
        "name": "中共桐庐县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共杭州市委员会",
        "location": "杭州市桐庐县"
    },
    {
        "id": 10,
        "name": "中共贵港市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共广西壮族自治区委员会",
        "location": "贵港市"
    },
    {
        "id": 11,
        "name": "贵港市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "广西壮族自治区人民政府",
        "location": "贵港市"
    },
    {
        "id": 12,
        "name": "中共贺州市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共广西壮族自治区委员会",
        "location": "贺州市"
    },
    {
        "id": 13,
        "name": "贺州市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "广西壮族自治区人民政府",
        "location": "贺州市"
    },
    {
        "id": 14,
        "name": "中共柳州市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共广西壮族自治区委员会",
        "location": "柳州市"
    },
    {
        "id": 15,
        "name": "中共梧州市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共广西壮族自治区委员会",
        "location": "梧州市"
    },
    {
        "id": 16,
        "name": "中共河池市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共广西壮族自治区委员会",
        "location": "河池市"
    },
    {
        "id": 17,
        "name": "广西壮族自治区纪律检查委员会（监察委）",
        "type": "纪委",
        "level": "省级",
        "parent": "",
        "location": "南宁市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 方毅（市委书记）
    {"person_id": 1, "org_id": 1, "title": "来宾市委书记", "start_date": "2025-09", "end_date": "present", "rank": "正厅级", "note": "2025年9月29日自治区党委决定任命，跨省调任"},
    {"person_id": 1, "org_id": 7, "title": "杭州市副市长", "start_date": "2023-11", "end_date": "2025-09", "rank": "副省级", "note": "2023年11月任杭州市副市长"},
    {"person_id": 1, "org_id": 6, "title": "杭州市委常委、市政府党组成员", "start_date": "2023-08", "end_date": "2025-09", "rank": "副省级", "note": "2023年8月出任杭州市委常委、市政府党组成员"},
    {"person_id": 1, "org_id": 9, "title": "桐庐县委书记", "start_date": "2018-11", "end_date": "2023-08", "rank": "县处级", "note": "2018年11月任桐庐县委书记"},
    {"person_id": 1, "org_id": 8, "title": "桐庐县委副书记、县长", "start_date": "", "end_date": "2018-11", "rank": "县处级", "note": "曾任桐庐县委副书记、县长"},

    # 周春涌（代市长）
    {"person_id": 2, "org_id": 2, "title": "来宾市代市长、市长", "start_date": "2026-07-31", "end_date": "present", "rank": "正厅级", "note": "2026年7月31日市五届人大常委会四十四次会议任命为副市长、代理市长"},
    {"person_id": 2, "org_id": 1, "title": "来宾市委副书记、市政府党组书记", "start_date": "2026-07-30", "end_date": "present", "rank": "正厅级", "note": "2026年7月30日任市委副书记、市政府党组书记"},
    {"person_id": 2, "org_id": 10, "title": "贵港市委常委、统战部部长", "start_date": "2023-05", "end_date": "2026-07", "rank": "副厅级", "note": "2023年5月跻身贵港市委常委，分管统战"},
    {"person_id": 2, "org_id": 11, "title": "贵港市副市长", "start_date": "2021-08", "end_date": "2026-07", "rank": "副厅级", "note": "2021年8月任贵港市副市长"},

    # 文东福（人大主任）
    {"person_id": 3, "org_id": 3, "title": "来宾市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "接替被查的沙君俊，现任来宾市人大主任"},
    {"person_id": 3, "org_id": 14, "title": "柳州市委常委、组织部部长", "start_date": "2021", "end_date": "", "rank": "副厅级", "note": "2021年8月任柳州市委常委、组织部部长"},
    {"person_id": 3, "org_id": 15, "title": "梧州市委常委、组织部部长", "start_date": "", "end_date": "2021", "rank": "副厅级", "note": "曾任梧州市委常委、组织部部长、党校校长"},
    {"person_id": 3, "org_id": 17, "title": "自治区党委组织部干部监督室主任", "start_date": "", "end_date": "", "rank": "正处级", "note": "曾任自治区党委组织部干部监督室主任、举报中心主任"},

    # 吴晓丽
    {"person_id": 4, "org_id": 4, "title": "来宾市政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "现任来宾市政协主席"},
    {"person_id": 4, "org_id": 1, "title": "来宾市委副书记", "start_date": "2021-09", "end_date": "", "rank": "副厅级", "note": "2021年9月当选来宾市委副书记"},
    {"person_id": 4, "org_id": 16, "title": "河池市委常委、环江毛南族自治县委书记", "start_date": "2009-11", "end_date": "2011-12", "rank": "县处级", "note": "2009年11月任河池市委常委、环江毛南族自治县委书记"},

    # 蒋卫生（专职副书记）
    {"person_id": 5, "org_id": 1, "title": "来宾市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "2021年起任来宾市委常委，现任市委副书记"},

    # 甘永辉
    {"person_id": 6, "org_id": 1, "title": "来宾市委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "现任市委常委、组织部部长"},

    # 梁仁省
    {"person_id": 7, "org_id": 1, "title": "来宾市委常委、秘书长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "现任市委常委、秘书长"},

    # 农化
    {"person_id": 8, "org_id": 2, "title": "来宾市副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "市委常委、副市长"},
    {"person_id": 8, "org_id": 1, "title": "来宾市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 彭斌
    {"person_id": 9, "org_id": 1, "title": "来宾市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "市直领导（推定政法委/宣传）"},

    # 徐广成
    {"person_id": 10, "org_id": 5, "title": "来宾市纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "推定市纪委书记（领导名单）"},

    # 韦焕清
    {"person_id": 11, "org_id": 2, "title": "来宾市政府秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "市政府秘书长（2026-08 人大/政府会议）"},

    # 何朝建（前任书记，被查）
    {"person_id": 12, "org_id": 1, "title": "来宾市委书记", "start_date": "2021-12", "end_date": "2025-09", "rank": "正厅级", "note": "2021年12月至2025年9月任来宾市委书记；2025-09-12被查"},
    {"person_id": 12, "org_id": 17, "title": "接受纪律审查和监察调查", "start_date": "2025-09-12", "end_date": "2026-05-10", "rank": "", "note": "2025-09-12被查，2026-05-10被开除党籍和公职"},

    # 廖和明（前任市长）
    {"person_id": 13, "org_id": 2, "title": "来宾市人民政府市长", "start_date": "2021-08", "end_date": "2026-07-31", "rank": "正厅级", "note": "2021年8月任代市长，2026年7月31日因工作变动辞去市长职务"},
    {"person_id": 13, "org_id": 12, "title": "贺州市常务副市长", "start_date": "", "end_date": "2018-09", "rank": "副厅级", "note": "2018年9月由贺州常务副市长调任来宾"},

    # 沙君俊（原人大主任，被查）
    {"person_id": 14, "org_id": 3, "title": "来宾市人大常委会主任", "start_date": "", "end_date": "2025-07", "rank": "正厅级", "note": "2025-07-31被查"},

    # 农生文（2021届市委书记）
    {"person_id": 15, "org_id": 1, "title": "来宾市委书记（第五届）", "start_date": "2021-09", "end_date": "", "rank": "正厅级", "note": "2021年9月当选来宾市委第五届市委书记"},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "方毅任市委书记、周春涌任代市长，党政主要领导搭档",
        "overlap_org": "来宾市",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 12,
        "type": "predecessor_successor",
        "context": "方毅接替何朝建任来宾市委书记（何已被查）",
        "overlap_org": "中共来宾市委",
        "overlap_period": "2025-09",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "方毅与文东福在来宾市委、市人大共事",
        "overlap_org": "来宾市",
        "overlap_period": "2025-09至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "方毅与吴晓丽在来宾市委、市政协共事",
        "overlap_org": "来宾市",
        "overlap_period": "2025-09至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 13,
        "type": "predecessor_successor",
        "context": "周春涌接替廖和明任来宾市长",
        "overlap_org": "来宾市人民政府",
        "overlap_period": "2026-07-31",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "周春涌与文东福在来宾市共事（政府、人大）",
        "overlap_org": "来宾市",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "周春涌与吴晓丽在来宾市共事（政府、政协）",
        "overlap_org": "来宾市",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 11,
        "type": "superior_subordinate",
        "context": "代市长与市政府秘书长工作搭档",
        "overlap_org": "来宾市人民政府",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 3, "person_b": 14,
        "type": "predecessor_successor",
        "context": "文东福接任因被查而空缺的市人大常委会主任（沙君俊）",
        "overlap_org": "来宾市人大常委会",
        "overlap_period": "2025-07",
        "confidence": "plausible"
    },
    {
        "person_a": 12, "person_b": 15,
        "type": "predecessor_successor",
        "context": "何朝建接替农生文任来宾市委书记（第五届换届）",
        "overlap_org": "中共来宾市委",
        "overlap_period": "2021-12",
        "confidence": "plausible"
    },
    {
        "person_a": 13, "person_b": 12,
        "type": "superior_subordinate",
        "context": "廖和明（市长）与何朝建（书记）党政搭档",
        "overlap_org": "来宾市",
        "overlap_period": "2021-12至2025-09",
        "confidence": "confirmed"
    },
]


# ══════════════════════════════════════════════════════════════════════════
# Helper: XML escape
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════
# Build database
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;

        CREATE TABLE persons (
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
            source TEXT
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ══════════════════════════════════════════════════════════════════════════
# Build GEXF
# ══════════════════════════════════════════════════════════════════════════

def person_color(name):
    # Party Secretary — Red
    if name == "方毅":
        return "255,50,50"
    # Government leader — Blue
    if name in ("周春涌", "廖和明", "农化"):
        return "50,100,255"
    # 人大 — Cyan
    if name in ("文东福", "沙君俊"):
        return "200,255,255"
    # 政协 — Cream
    if name == "吴晓丽":
        return "255,240,200"
    # 纪委 — Orange
    if name == "徐广成":
        return "255,165,0"
    # 下落/前任 — Grey
    if name in ("何朝建", "农生文", "韦焕清"):
        return "150,150,150"
    # Others — Grey
    return "100,100,100"


def person_size(name):
    if name in ("方毅", "周春涌"):
        return "20.0"
    if name in ("何朝建", "廖和明"):
        return "14.0"
    return "12.0"


def org_color(o_type):
    if "党委" in o_type:
        return "255,200,200"
    if "政府" in o_type:
        return "200,200,255"
    if "人大" in o_type:
        return "200,255,255"
    if "政协" in o_type:
        return "255,240,200"
    if "纪委" in o_type:
        return "255,165,0"
    if "事业单位" in o_type:
        return "220,220,220"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>来宾市领导班子工作关系网络 - {SLUG}</description>')
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
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        sz = person_size(p["name"])
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        lines.append(f'      <edge id="{eid}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="2.0">')
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
    print(f"  GEXF: {GEXF_PATH} ({eid} edges)")


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

SOURCE_REGISTER = [
    {"id": "S001", "title": "来宾市人民政府门户网站—政务动态", "url": "http://www.laibin.gov.cn/xwzx/zwdt/", "publisher": "来宾市人民政府", "published_at": "2026-07/08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "招商引资会议、乡镇书记交流会、政绩观党课等确认当前班子"},
    {"id": "S002", "title": "中国经济网—周春涌任来宾市代市长 廖和明辞去市长职务", "url": "http://district.ce.cn/newarea/sddy/202607/t20260731_3120716.shtml", "publisher": "中国经济网", "published_at": "2026-07-31", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "确认周春涌任命为副市长、代理市长，廖和明辞职"},
    {"id": "S003", "title": "中国经济网—周春涌任来宾市委副书记、市政府党组书记", "url": "http://district.ce.cn/newarea/sddy/202607/t20260730_3117861.shtml", "publisher": "中国经济网", "published_at": "2026-07-30", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "确认周春涌本月初任市委副书记、市政府党组书记"},
    {"id": "S004", "title": "中国经济网—方毅任来宾市委书记", "url": "https://district.ce.cn", "publisher": "中国经济网", "published_at": "2025-09-30", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "确认方毅（1972.1，浙江淳安，杭州）跨省调任来宾市委书记"},
    {"id": "S005", "title": "360百科—方毅", "url": "https://baike.so.com", "publisher": "360百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "方毅完整履历（桐庐、杭州）"},
    {"id": "S006", "title": "360百科—廖和明", "url": "https://baike.so.com", "publisher": "360百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "廖和明履历（贺州常务副市长→来宾）"},
    {"id": "S007", "title": "360百科—文东福", "url": "https://baike.so.com/doc/30477840-32120282.html", "publisher": "360百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "文东福履历（自治区组织部→梧州→柳州）"},
    {"id": "S008", "title": "360百科—吴晓丽", "url": "https://baike.so.com/doc/6385328-6598981.html", "publisher": "360百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "吴晓丽履历（共青团、河池、自治区妇联）"},
    {"id": "S009", "title": "360百科—中国共产党来宾市委员会", "url": "https://baike.so.com/doc/29894739-31482038.html", "publisher": "360百科", "published_at": "2024-07-15", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "第五届市委班子名单（农生文/廖和明/吴晓丽等）"},
    {"id": "S010", "title": "360百科—何朝建（广西来宾市委原书记）", "url": "https://baike.so.com/doc/2996897-3160644.html", "publisher": "360百科", "published_at": "2026-05", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "high", "notes": "何朝建落马细节、2025-09-12被查、2026-05-10双开"},
    {"id": "S011", "title": "360百科—沙君俊（原人大主任）", "url": "https://baike.so.com/doc/4750115-4965436.html", "publisher": "360百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "2025-07-31涉嫌严重违纪违法被查"},
]


def make_person_json(p, timeline, relationships_list, source_ids=None):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "来宾市",
            "region": "来宾市",
            "job": p.get("current_post", ""),
            "task_id": "guangxi_来宾市",
            "time_focus": "2026年8月"
        },
        "identity": {
            "person_id": f"laibin_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正厅级" if p["id"] in (1, 2, 3, 4, 12, 13) else "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": p["id"] in (1, 2, 3, 4),
            "source_ids": source_ids or ["S001", "S002", "S003"]
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
            {"type": "none_found", "description": "在公开信息中未发现该人物负面信号", "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": SOURCE_REGISTER,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed" if p["id"] in (1, 2, 3, 4) else "plausible",
            "career_completeness": "partial" if p["id"] in (1, 2, 4) else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历（含早期职务、分工细节）需补充"
        },
        "open_questions": [
            {
                "priority": "critical" if p["id"] in (1, 2) else "high",
                "question": f"{p['name']}的完整职业生涯履历细节（含教育、历任职务、具体时间）",
                "why_it_matters": "核心人物，需完整履历支撑网络分析",
                "suggested_queries": [f"{p['name']} 简历 来宾", f"{p['name']} 任前公示"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    # === 1. 方毅（市委书记） ===
    fang_timeline = [
        {"start": "1994-08", "end": "2018-11", "org": "浙江省杭州市", "title": "早年职务（县委副书记、县长等）", "notes": "长期在杭州工作，曾任桐庐县委副书记、县长", "confidence": "plausible", "source_ids": ["S005"]},
        {"start": "2018-11", "end": "2023-08", "org": "桐庐县", "title": "桐庐县委书记", "notes": "2018年11月任桐庐县委书记", "confidence": "confirmed", "source_ids": ["S004", "S005"]},
        {"start": "2023-08", "end": "2023-11", "org": "杭州市", "title": "杭州市委常委、市政府党组成员", "notes": "2023年8月任", "confidence": "confirmed", "source_ids": ["S005"]},
        {"start": "2023-11", "end": "2025-09", "org": "杭州市人民政府", "title": "杭州市副市长", "notes": "2023年11月任杭州市副市长", "confidence": "confirmed", "source_ids": ["S004", "S005"]},
        {"start": "2025-09", "end": "present", "org": "中共来宾市委员会", "title": "来宾市委书记", "notes": "2025年9月跨省调任广西来宾市委书记（接替被查的何朝建）", "confidence": "confirmed", "source_ids": ["S004", "S005"]},
    ]
    fang_relationships = [
        {"person": "何朝建", "person_id": "laibin_何朝建", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "方毅接替何朝建任来宾市委书记（何已被查）", "overlap_org": "中共来宾市委", "overlap_period": "2025-09", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "周春涌", "person_id": "laibin_周春涌", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "市委书记与代市长党政搭档", "overlap_org": "来宾市", "overlap_period": "2026-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "文东福", "person_id": "laibin_文东福", "relationship_type": "overlap", "strength": "medium", "evidence": "在市委/人大共事", "overlap_org": "来宾市", "overlap_period": "2025-09至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "吴晓丽", "person_id": "laibin_吴晓丽", "relationship_type": "overlap", "strength": "medium", "evidence": "在市委/政协共事", "overlap_org": "来宾市", "overlap_period": "2025-09至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    fang_json = make_person_json(persons[0], fang_timeline, fang_relationships)
    fang_json["professional_profile"]["career_pattern"] = "cross_province_rotation"
    fang_json["professional_profile"]["geographic_pattern"] = ["浙江省", "广西壮族自治区"]
    fang_json["professional_profile"]["primary_specializations"] = ["城市建设", "政府管理", "经济工作"]
    fang_json["professional_profile"]["promotion_velocity"] = {
        "summary": "1972年生，2023年任杭州市副市长（副省级城市），2025年跨省任地级市市委书记（正厅级）",
        "notable_fast_promotions": ["跨省交流（杭州→广西）任地级市市委书记"]
    }
    fang_json["work_style_and_personality"]["public_style_indicators"] = [
        {"trait": "reform_oriented", "evidence": "招商引资“没有退路唯有奋进”、强调“四张报表”、“六对辩证关系”", "confidence": "plausible", "source_ids": ["S001"]}
    ]
    fang_json["open_questions"] = [
        {"priority": "critical", "question": "方毅2002-2018年前（桐庐县长之前的详细职务轨迹）", "why_it_matters": "核心人物早年履历细节", "suggested_queries": ["方毅 桐庐 简历 历任", "方毅 浙江 任职经历"], "last_attempted": AS_OF},
    ]
    fang_path = PERSONS_DIR / f"{TODAY}-广西壮族自治区-来宾市-市委书记-方毅.json"
    with open(fang_path, "w", encoding="utf-8") as f:
        json.dump(fang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fang_path.name}")

    # === 2. 周春涌（代市长） ===
    zhou_timeline = [
        {"start": "1997-08", "end": "2021", "org": "广西", "title": "早年经历", "notes": "广西钟山县人，山东财政学院毕业，2021年前从业及基层经历详查", "confidence": "plausible", "source_ids": ["S002", "S006"]},
        {"start": "2021-08", "end": "2023-05", "org": "贵港市人民政府", "title": "贵港市副市长", "notes": "2021年8月任贵港市副市长", "confidence": "confirmed", "source_ids": ["S006"]},
        {"start": "2023-05", "end": "2026-07", "org": "中共贵港市委员会", "title": "贵港市委常委、统战部部长", "notes": "2023年5月任贵港市委常委，后任统战部部长", "confidence": "confirmed", "source_ids": ["S002", "S006"]},
        {"start": "2026-07-30", "end": "present", "org": "中共来宾市委员会", "title": "来宾市委副书记、市政府党组书记", "notes": "2026年7月30日任", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "2026-07-31", "end": "present", "org": "来宾市人民政府", "title": "来宾市代市长", "notes": "2026年7月31日市五届人大常委会四十四次会议任命为副市长、代理市长", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    zhou_relationships = [
        {"person": "廖和明", "person_id": "laibin_廖和明", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "周春涌接替廖和明任来宾市市长", "overlap_org": "来宾市人民政府", "overlap_period": "2026-07-31", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "方毅", "person_id": "laibin_方毅", "relationship_type": "subordinate", "strength": "strong", "evidence": "代市长受市委书记领导", "overlap_org": "来宾市", "overlap_period": "2026-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    zhou_json = make_person_json(persons[1], zhou_timeline, zhou_relationships)
    zhou_json["professional_profile"]["career_pattern"] = "cross_county_rotation"
    zhou_json["professional_profile"]["systems_experience"] = ["government", "united_front", "party"]
    zhou_json["professional_profile"]["geographic_pattern"] = ["贵港", "来宾"]
    zhou_json["open_questions"] = [
        {"priority": "critical", "question": "周春涌1997-2021年（任贵港副市长前）的完整履历", "why_it_matters": "新任一市长，早年经历空白", "suggested_queries": ["周春涌 贵港 简历 历任", "周春涌 山东财政学院"], "last_attempted": AS_OF}
    ]
    zhou_path = PERSONS_DIR / f"{TODAY}-广西壮族自治区-来宾市-市长-周春涌.json"
    with open(zhou_path, "w", encoding="utf-8") as f:
        json.dump(zhou_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zhou_path.name}")

    # === 3. 文东福（人大主任） ===
    wdf_timeline = [
        {"start": "unknown", "end": "unknown", "org": "自治区党委组织部", "title": "干部监督室主任、举报中心主任", "notes": "组织系统出道", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "unknown", "end": "2021", "org": "梧州市", "title": "梧州市委常委、组织部部长", "notes": "曾任", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "2021-08", "end": "", "org": "柳州市委", "title": "柳州市委常委、组织部部长", "notes": "2021年8月任柳州市委常委、组织部部长", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "unknown", "end": "present", "org": "来宾市人大常委会", "title": "来宾市人大常委会主任", "notes": "接任被查的沙君俊", "confidence": "plausible", "source_ids": ["S001"]},
    ]
    wen_json = make_person_json(persons[2], wdf_timeline, [])
    wen_json["professional_profile"]["career_pattern"] = "organization_track"
    wen_json["professional_profile"]["systems_experience"] = ["organization"]
    wen_path = PERSONS_DIR / f"{TODAY}-广西壮族自治区-来宾市-人大主任-文东福.json"
    with open(wen_path, "w", encoding="utf-8") as f:
        json.dump(wen_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {wen_path.name}")

    # === 4. 吴晓丽（政协主席） ===
    wxl_timeline = [
        {"start": "1992-09", "end": "1995-07", "org": "广西民族学院", "title": "历史系文秘档案专业学生", "notes": "", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "1995-07", "end": "1997-07", "org": "东兰县武阳镇", "title": "专职团干→镇镇长助理→副镇长", "notes": "乡镇基层", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "1997-07", "end": "1999-07", "org": "共青团东兰县委", "title": "共青团东兰县委书记", "notes": "公开竞聘", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "1999-07", "end": "2001-05", "org": "东兰县弄占乡", "title": "乡党委书记", "notes": "", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2001-05", "end": "2008-12", "org": "共青团河池市委", "title": "书记、青联主席", "notes": "2006年任河池团市委书记", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2008-12", "end": "2011-12", "org": "河池市环江毛南族自治县", "title": "县委副书记→河池市委常委、环江县委书记", "notes": "2009年11月任河池市委常委、环江县委书记", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2011-12", "end": "2016-10", "org": "广西壮族自治区妇联", "title": "自治区妇联副主席、党组成员", "notes": "", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2016-10", "end": "2021-02", "org": "自治区新闻出版广电局/广播电视局", "title": "副局长、党组成员", "notes": "2021年2月免职广电局副局长", "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2021-09", "end": "", "org": "中共来宾市委员会", "title": "来宾市委副书记", "notes": "2021年9月当选来宾市委副书记", "confidence": "confirmed", "source_ids": ["S009"]},
        {"start": "unknown", "end": "present", "org": "来宾市政协", "title": "来宾市政协主席", "notes": "现任市政协主席", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    wxl_relationships = [
        {"person": "方毅", "person_id": "laibin_方毅", "relationship_type": "overlap", "strength": "medium", "evidence": "市委/政协共事", "overlap_org": "来宾市", "overlap_period": "2025-09至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    wxl_json = make_person_json(persons[3], wxl_timeline, wxl_relationships)
    wxl_json["professional_profile"]["career_pattern"] = "group_track"
    wxl_json["professional_profile"]["systems_experience"] = ["group_leagues", "media", "women_federation"]
    wxl_path = PERSONS_DIR / f"{TODAY}-广西壮族自治区-来宾市-政协主席-吴晓丽.json"
    with open(wxl_path, "w", encoding="utf-8") as f:
        json.dump(wxl_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {wxl_path.name}")

    # === 12. 何朝建（前任书记，落马） ===
    he_timeline = [
        {"start": "1985-09", "end": "1990-07", "org": "清华大学", "title": "土木工程系建筑管理工程专业", "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "1990-07", "end": "2002-05", "org": "百色地区", "title": "建委干部→建设局副局长→建设局局长", "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "2002-10", "end": "2006-08", "org": "百色市人民政府", "title": "百色市副市长", "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "2006-08", "end": "2008-12", "org": "自治区建设厅", "title": "总工程师、党组成员", "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "2008-12", "end": "2010-05", "org": "钦州市人民政府", "title": "钦州市副市长", "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "2013-01", "end": "2017-11", "title": "防城港市委副书记、市长", "notes": "2013年2月任防城港市市长", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "2017-11", "end": "2021-12", "title": "自治区民宗委党组书记", "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "2021-12", "end": "2025-09", "org": "中共来宾市委员会", "title": "来宾市委书记", "notes": "2021年12月至2025年9月", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "2025-09-12", "end": "2026-05-10", "org": "自治区纪委监委", "title": "涉嫌严重违纪违法被查、双开", "notes": "2025-09-12被查；2026-05-10开除党籍和公职（政治攀附、权钱交易、项目承揽等）", "confidence": "confirmed", "source_ids": ["S010"]},
    ]
    he_relationships = [
        {"person": "方毅", "person_id": "laibin_方毅", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "方毅接替何朝建任书记", "overlap_org": "中共来宾市委", "overlap_period": "2025-09", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "廖和明", "person_id": "laibin_廖和明", "relationship_type": "overlap", "strength": "medium", "evidence": "何朝建（书记）与廖和明（市长）党政搭档", "overlap_org": "来宾市", "overlap_period": "2021-12至2025-09", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S010"]},
    ]
    he_json = make_person_json(persons[11], he_timeline, he_relationships)
    he_json["current_status"]["is_current_role_confirmed"] = False
    he_json["risk_and_integrity_signals"] = [
        {"type": "disciplinary_action", "description": "2025-09-12涉嫌严重违纪违法被查；2026-05-10被开除党籍和公职；政治攀附、权钱交易、项目承揽等受贿", "date": "2025-09-12/2020-05-10", "confidence": "confirmed", "source_ids": ["S010"]}
    ]
    he_json["open_questions"] = [
        {"priority": "medium", "question": "何朝建去向（双开后处分决定详情）", "why_it_matters": "重大腐败案例背景补充", "suggested_queries": ["何朝建 双开 判决"], "last_attempted": AS_OF}
    ]
    he_path = PERSONS_DIR / f"{TODAY}-广西壮族自治区-来宾市-前任市委书记-何朝建.json"
    with open(he_path, "w", encoding="utf-8") as f:
        json.dump(he_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {he_path.name}")

    # === 13. 廖和明（前任市长） ===
    liao_timeline = [
        {"start": "1991-07", "end": "2018", "org": "广西", "title": "早年经历", "notes": "广西全州人，1991年参加工作，历任职务待查", "confidence": "plausible", "source_ids": ["S006"]},
        {"start": "", "end": "2018-09", "org": "贺州市人民政府", "title": "贺州市常务副市长", "notes": "2018年9月由贺州常务副市长调任来宾", "confidence": "confirmed", "source_ids": ["S006"]},
        {"start": "2018-09", "end": "2021-08", "org": "来宾市人民政府", "title": "来宾市委常委、副市长", "notes": "", "confidence": "confirmed", "source_ids": ["S006"]},
        {"start": "2021-08", "end": "2026-07-31", "org": "来宾市人民政府", "title": "来宾市政府代市长、市长", "notes": "2021年8月任代市长；2026年7月31日因工作变动辞去市长", "confidence": "confirmed", "source_ids": ["S002", "S006"]},
    ]
    liao_relationships = [
        {"person": "周春涌", "person_id": "laibin_周春涌", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "廖和明辞去，周春涌接任代市长", "overlap_org": "来宾市人民政府", "overlap_period": "2026-07-31", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    liao_json = make_person_json(persons[13], liao_timeline, liao_relationships)
    liao_json["current_status"]["as_of"] = AS_OF
    liao_path = PERSONS_DIR / f"{TODAY}-广西壮族自治区-来宾市-前任市长-廖和明.json"
    with open(liao_path, "w", encoding="utf-8") as f:
        json.dump(liao_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {liao_path.name}")


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"\nOutput files:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    for p in PERSONS_DIR.glob(f"{TODAY}-*.json"):
        print(f"  Person: {p}")
    print("Done.")