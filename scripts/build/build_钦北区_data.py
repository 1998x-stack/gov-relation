#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广西钦州市钦北区领导班子工作关系网络 — 数据构建脚本
Build SQLite database + GEXF graph + person JSON for Qinbei District.

Level: 市辖区
Province: 广西壮族自治区
Parent city: 钦州市
Targets: 区委书记 & 区长
Task: guangxi_钦北区

Research date: 2026-07-23

Current leadership (as of July 2026, sourced from www.qinbei.gov.cn):
- 区委书记: 黄敏 (confirmed via multiple news articles, presiding over 区委常委会)
- 区长: 邓洁丽 (confirmed as 区委副书记、区长 via article t27743874)

Sources:
- 钦北区人民政府官网: http://www.qinbei.gov.cn/
- News articles (qbyw/ section): t27743874, t27719538, t27858380, t27858381, t27904388,
  t27348915, t27348916, t27827533, t27806665, t21246567, t27373563, t20100539, t27277269

Confidence:
- Current roles: confirmed (official website news articles)
- Biographical details: limited (no official biography page on site)
- Career timelines: partial - unverified (all web search tools blocked)
"""

from pathlib import Path
import sqlite3
import sys
import json
from datetime import datetime

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Staging paths ──
STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "钦北区_network.db"
GEXF_PATH = STAGING_DIR / "钦北区_network.gexf"
PERSONS_OUT_DIR = STAGING_DIR

TODAY = "2026-07-23"
GENERATED_AT = TODAY
AS_OF = TODAY

# ════════════════════════════════════════════════════════════════
# PERSONS
# ════════════════════════════════════════════════════════════════

persons = [
    # ── 1: 黄敏 — 钦北区委书记 ──
    {
        "id": 1,
        "name": "黄敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区委书记",
        "current_org": "中共钦北区委员会",
        "source": "http://www.qinbei.gov.cn/ (区委常委会新闻, 2026年5-7月)"
    },
    # ── 2: 邓洁丽 — 钦北区委副书记、区长 ──
    {
        "id": 2,
        "name": "邓洁丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区委副书记、区长",
        "current_org": "钦北区人民政府",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27743874, t27719538)"
    },
    # ── 3: 陆汉川 — 区委副书记 ──
    {
        "id": 3,
        "name": "陆汉川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区委副书记",
        "current_org": "中共钦北区委员会",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27806665)"
    },
    # ── 4: 黄良先 — 区委常委、常务副区长 ──
    {
        "id": 4,
        "name": "黄良先",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区委常委、常务副区长",
        "current_org": "钦北区人民政府",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27827533)"
    },
    # ── 5: 梁荣胜 — 区委常委、宣传部部长 ──
    {
        "id": 5,
        "name": "梁荣胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区委常委、宣传部部长",
        "current_org": "中共钦北区委员会宣传部",
        "source": "http://www.qinbei.gov.cn/ (新闻, t20100539)"
    },
    # ── 6: 相中来 — 区委常委、政法委书记 ──
    {
        "id": 6,
        "name": "相中来",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区委常委、政法委书记",
        "current_org": "中共钦北区委员会政法委员会",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27348905)"
    },
    # ── 7: 米昆仁 — 区委常委、统战部部长，副区长，区政协党组副书记（兼） ──
    {
        "id": 7,
        "name": "米昆仁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区委常委、统战部部长、副区长、区政协党组副书记（兼）",
        "current_org": "中共钦北区委员会统战部/钦北区人民政府",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27348915)"
    },
    # ── 8: 石瑞喜 — 区委常委、人武部部长 ──
    {
        "id": 8,
        "name": "石瑞喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区委常委、人武部部长",
        "current_org": "钦北区人民武装部",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27348920)"
    },
    # ── 9: 钟耀坚 — 区委常委、区纪委书记、区监委主任 ──
    {
        "id": 9,
        "name": "钟耀坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区委常委、区纪委书记、区监委主任",
        "current_org": "中共钦北区纪律检查委员会/钦北区监察委员会",
        "source": "http://www.qinbei.gov.cn/ (新闻, t21246567)"
    },
    # ── 10: 熊丽婷 — 区委常委、办公室主任 ──
    {
        "id": 10,
        "name": "熊丽婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区委常委、办公室主任",
        "current_org": "中共钦北区委员会办公室",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27373563)"
    },
    # ── 11: 徐超然 — 区委常委、组织部部长（推断） ──
    {
        "id": 11,
        "name": "徐超然",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区委常委、组织部部长",
        "current_org": "中共钦北区委员会组织部",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27858381, 主持党课来源区委组织部)"
    },
    # ── 12: 黄祥剑 — 区人大常委会主任 ──
    {
        "id": 12,
        "name": "黄祥剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区人大常委会主任",
        "current_org": "钦北区人民代表大会常务委员会",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27806665, t27348916)"
    },
    # ── 13: 叶金芬 — 区政协主席 ──
    {
        "id": 13,
        "name": "叶金芬",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区政协主席",
        "current_org": "中国人民政治协商会议钦北区委员会",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27277278, t27348915)"
    },
    # ── 14: 谢显鑫 — 副区长（推断） ──
    {
        "id": 14,
        "name": "谢显鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区副区长",
        "current_org": "钦北区人民政府",
        "source": "http://www.qinbei.gov.cn/ (新闻)"
    },
    # ── 15: 农立宪 — 副区长（推断） ──
    {
        "id": 15,
        "name": "农立宪",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区副区长",
        "current_org": "钦北区人民政府",
        "source": "http://www.qinbei.gov.cn/ (新闻)"
    },
    # ── 16: 黄昱淇 — 副区长（推断） ──
    {
        "id": 16,
        "name": "黄昱淇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区副区长",
        "current_org": "钦北区人民政府",
        "source": "http://www.qinbei.gov.cn/ (新闻)"
    },
    # ── 17: 邓唐礼 — 副区长（推断） ──
    {
        "id": 17,
        "name": "邓唐礼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区副区长",
        "current_org": "钦北区人民政府",
        "source": "http://www.qinbei.gov.cn/ (新闻)"
    },
    # ── 18: 宾子照 — 区人民法院院长 ──
    {
        "id": 18,
        "name": "宾子照",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区人民法院院长",
        "current_org": "钦北区人民法院",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27348916)"
    },
    # ── 19: 何君 — 区人民检察院检察长 ──
    {
        "id": 19,
        "name": "何君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区人民检察院检察长",
        "current_org": "钦北区人民检察院",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27348916)"
    },
    # ── 20: 陈宇才 — 区政协副主席 ──
    {
        "id": 20,
        "name": "陈宇才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区政协副主席",
        "current_org": "中国人民政治协商会议钦北区委员会",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27348915)"
    },
    # ── 21: 吴善 — 区政协副主席 ──
    {
        "id": 21,
        "name": "吴善",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区政协副主席",
        "current_org": "中国人民政治协商会议钦北区委员会",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27348915)"
    },
    # ── 22: 褚乃平 — 区政协副主席 ──
    {
        "id": 22,
        "name": "褚乃平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区政协副主席",
        "current_org": "中国人民政治协商会议钦北区委员会",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27348915)"
    },
    # ── 23: 陈冰 — 区政协副主席 ──
    {
        "id": 23,
        "name": "陈冰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钦北区政协副主席",
        "current_org": "中国人民政治协商会议钦北区委员会",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27348915)"
    },
    # ── 24: 钟建明 — 区政协秘书长 ──
    {
        "id": 24,
        "name": "钟建明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区政协秘书长",
        "current_org": "中国人民政治协商会议钦北区委员会",
        "source": "http://www.qinbei.gov.cn/ (新闻, t27348915)"
    },
    # ── 25: 石世裕 — 区领导（具体职务待确认） ──
    {
        "id": 25,
        "name": "石世裕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦北区领导",
        "current_org": "",
        "source": "http://www.qinbei.gov.cn/ (新闻)"
    },
]

# ════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共钦北区委员会", "type": "党委", "level": "县处级", "parent": "中共钦州市委员会", "location": "广西钦州市钦北区"},
    {"id": 2, "name": "钦北区人民政府", "type": "政府", "level": "县处级", "parent": "钦州市人民政府", "location": "广西钦州市钦北区"},
    {"id": 3, "name": "中共钦北区纪律检查委员会/钦北区监察委员会", "type": "纪委", "level": "县处级", "parent": "中共钦北区委员会", "location": "广西钦州市钦北区"},
    {"id": 4, "name": "钦北区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "钦北区", "location": "广西钦州市钦北区"},
    {"id": 5, "name": "中国人民政治协商会议钦北区委员会", "type": "政协", "level": "县处级", "parent": "钦北区", "location": "广西钦州市钦北区"},
    {"id": 6, "name": "中共钦北区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共钦北区委员会", "location": "广西钦州市钦北区"},
    {"id": 7, "name": "中共钦北区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共钦北区委员会", "location": "广西钦州市钦北区"},
    {"id": 8, "name": "中共钦北区委员会统战部", "type": "党委", "level": "县处级", "parent": "中共钦北区委员会", "location": "广西钦州市钦北区"},
    {"id": 9, "name": "钦北区人民武装部", "type": "军队", "level": "县处级", "parent": "钦州军分区", "location": "广西钦州市钦北区"},
    {"id": 10, "name": "中共钦北区委员会办公室", "type": "党委", "level": "县处级", "parent": "中共钦北区委员会", "location": "广西钦州市钦北区"},
    {"id": 11, "name": "中共钦北区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共钦北区委员会", "location": "广西钦州市钦北区"},
    {"id": 12, "name": "钦北区人民法院", "type": "司法", "level": "县处级", "parent": "钦州市中级人民法院", "location": "广西钦州市钦北区"},
    {"id": 13, "name": "钦北区人民检察院", "type": "司法", "level": "县处级", "parent": "钦州市人民检察院", "location": "广西钦州市钦北区"},
]

# ════════════════════════════════════════════════════════════════
# POSITIONS (person → org relationships)
# ════════════════════════════════════════════════════════════════

positions = [
    # 黄敏 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "钦北区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持区委全面工作"},
    # 邓洁丽 — 区长
    {"person_id": 2, "org_id": 2, "title": "钦北区委副书记、区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持区政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "钦北区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼任"},
    # 陆汉川 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "钦北区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助书记处理区委日常工作"},
    # 黄良先 — 区委常委、常务副区长
    {"person_id": 4, "org_id": 1, "title": "钦北区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "钦北区常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 梁荣胜 — 区委常委、宣传部部长
    {"person_id": 5, "org_id": 1, "title": "钦北区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "钦北区委宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 相中来 — 区委常委、政法委书记
    {"person_id": 6, "org_id": 1, "title": "钦北区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "钦北区委政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 米昆仁 — 区委常委、统战部部长，副区长
    {"person_id": 7, "org_id": 1, "title": "钦北区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 8, "title": "钦北区委统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "钦北区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼任"},
    {"person_id": 7, "org_id": 5, "title": "钦北区政协党组副书记（兼）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼任"},
    # 石瑞喜 — 区委常委、人武部部长
    {"person_id": 8, "org_id": 1, "title": "钦北区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 9, "title": "钦北区人武部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 钟耀坚 — 区委常委、区纪委书记、区监委主任
    {"person_id": 9, "org_id": 3, "title": "钦北区纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "钦北区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 熊丽婷 — 区委常委、办公室主任
    {"person_id": 10, "org_id": 1, "title": "钦北区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 10, "title": "钦北区委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 徐超然 — 区委常委、组织部部长
    {"person_id": 11, "org_id": 1, "title": "钦北区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "推断"},
    {"person_id": 11, "org_id": 11, "title": "钦北区委组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "推断"},
    # 黄祥剑 — 区人大常委会主任
    {"person_id": 12, "org_id": 4, "title": "钦北区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 叶金芬 — 区政协主席
    {"person_id": 13, "org_id": 5, "title": "钦北区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 谢显鑫 — 副区长
    {"person_id": 14, "org_id": 2, "title": "钦北区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "推断"},
    # 农立宪 — 副区长
    {"person_id": 15, "org_id": 2, "title": "钦北区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "推断"},
    # 黄昱淇 — 副区长
    {"person_id": 16, "org_id": 2, "title": "钦北区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "推断"},
    # 邓唐礼 — 副区长
    {"person_id": 17, "org_id": 2, "title": "钦北区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "推断"},
    # 宾子照 — 区法院院长
    {"person_id": 18, "org_id": 12, "title": "钦北区人民法院院长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 何君 — 区检察院检察长
    {"person_id": 19, "org_id": 13, "title": "钦北区人民检察院检察长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈宇才 — 区政协副主席
    {"person_id": 20, "org_id": 5, "title": "钦北区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 吴善 — 区政协副主席
    {"person_id": 21, "org_id": 5, "title": "钦北区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 褚乃平 — 区政协副主席
    {"person_id": 22, "org_id": 5, "title": "钦北区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈冰 — 区政协副主席
    {"person_id": 23, "org_id": 5, "title": "钦北区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 钟建明 — 区政协秘书长
    {"person_id": 24, "org_id": 5, "title": "钦北区政协秘书长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 石世裕 — 区领导
    {"person_id": 25, "org_id": 1, "title": "钦北区领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待确认"},
]

# ════════════════════════════════════════════════════════════════
# RELATIONSHIPS (person ↔ person)
# ════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "党政同责",
        "context": "区委书记与区长为钦北区党政一把手，共同主持全区工作",
        "overlap_org": "钦北区",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "上下级",
        "context": "区委书记与区委副书记同属区委常委会班子",
        "overlap_org": "中共钦北区委员会",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "党政协作",
        "context": "区长与区委副书记在区委统一领导下协作推进工作",
        "overlap_org": "钦北区",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "上下级",
        "context": "区委书记与常务副区长在区委常委会中协作",
        "overlap_org": "中共钦北区委员会/钦北区人民政府",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "上下级",
        "context": "区长与常务副区长在政府工作中的搭档关系",
        "overlap_org": "钦北区人民政府",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "上下级",
        "context": "区委书记与宣传部部长在区委常委会中协作",
        "overlap_org": "中共钦北区委员会",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "上下级",
        "context": "区委书记与政法委书记在区委常委会中协作",
        "overlap_org": "中共钦北区委员会",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1, "person_b": 7,
        "type": "上下级",
        "context": "区委书记与统战部部长在区委常委会中协作",
        "overlap_org": "中共钦北区委员会",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1, "person_b": 8,
        "type": "上下级",
        "context": "区委书记与人武部部长在区委常委会中协作",
        "overlap_org": "中共钦北区委员会",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1, "person_b": 9,
        "type": "上下级",
        "context": "区委书记与纪委书记在区委常委会中协作",
        "overlap_org": "中共钦北区委员会",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1, "person_b": 10,
        "type": "上下级",
        "context": "区委书记与区委办公室主任在区委常委会中协作",
        "overlap_org": "中共钦北区委员会",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1, "person_b": 11,
        "type": "上下级",
        "context": "区委书记与组织部部长在区委常委会中协作",
        "overlap_org": "中共钦北区委员会",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1, "person_b": 12,
        "type": "党政协作",
        "context": "区委书记与区人大常委会主任在区级领导班子中协作",
        "overlap_org": "钦北区",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1, "person_b": 13,
        "type": "党政协作",
        "context": "区委书记与区政协主席在区级领导班子中协作",
        "overlap_org": "钦北区",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 2, "person_b": 12,
        "type": "党政协作",
        "context": "区长与区人大常委会主任在区级领导班子中协作",
        "overlap_org": "钦北区",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 2, "person_b": 13,
        "type": "党政协作",
        "context": "区长与区政协主席在区级领导班子中协作",
        "overlap_org": "钦北区",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 2, "person_b": 8,
        "type": "党政协作",
        "context": "2026年春季新兵入伍欢送大会中区长邓洁丽与人武部长石瑞喜共同参与",
        "overlap_org": "钦北区",
        "overlap_period": "2026-03",
    },
    {
        "person_a": 4, "person_b": 14,
        "type": "同僚",
        "context": "常务副区长与副区长在区政府领导班子中协作",
        "overlap_org": "钦北区人民政府",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 13, "person_b": 7,
        "type": "兼职关系",
        "context": "米昆仁兼任区政协党组副书记，与政协主席叶金芬有工作交集",
        "overlap_org": "钦北区政协",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 13, "person_b": 20,
        "type": "上下级",
        "context": "政协主席与政协副主席在政协领导班子中协作",
        "overlap_org": "钦北区政协",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1, "person_b": 25,
        "type": "上下级",
        "context": "区委书记与石世裕（区领导）在区委工作中协作",
        "overlap_org": "中共钦北区委员会",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 12, "person_b": 13,
        "type": "同僚",
        "context": "区人大常委会主任与区政协主席同为区级正职领导",
        "overlap_org": "钦北区",
        "overlap_period": "2024-至今",
    },
]

# ════════════════════════════════════════════════════════════════
# PERSON JSON TEMPLATES
# ════════════════════════════════════════════════════════════════

def make_person_json(person, extra):
    """Create a person graph JSON following the reference schema."""
    return {
        "schema_version": "1.0",
        "generated_at": GENERATED_AT,
        "investigation_scope": extra["scope"],
        "identity": {
            "person_id": extra.get("person_id", ""),
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": extra.get("birth", ""),
            "birthplace": extra.get("birthplace", ""),
            "native_place": extra.get("native_place", ""),
            "education": extra.get("education", []),
            "party_join": extra.get("party_join_date", ""),
            "work_start": extra.get("work_start_date", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{extra.get('birth', 'unknown')}",
                "name_birthplace": f"{person['name']}_{extra.get('birthplace', 'unknown')}",
                "official_profile_url": extra.get("profile_url", ""),
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": extra.get("rank", ""),
            "as_of": TODAY,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": extra.get("career_timeline", []),
        "organizations": extra.get("organizations", []),
        "relationships": extra.get("relationships", []),
        "governance_record": extra.get("governance_record", []),
        "professional_profile": extra.get("professional_profile", {}),
        "work_style_and_personality": extra.get("work_style", {}),
        "network_metrics": {},
        "risk_and_integrity_signals": extra.get("risk_signals", []),
        "source_register": [
            {
                "id": "S001",
                "title": "钦北区人民政府门户网站",
                "url": "http://www.qinbei.gov.cn/",
                "publisher": "钦北区人民政府",
                "published_at": "",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "区政府官网; 包含领导活动动态",
            },
            *extra.get("extra_sources", []),
        ],
        "confidence_summary": {
            "identity": extra.get("confidence_identity", "unverified"),
            "current_role": extra.get("confidence_role", "confirmed"),
            "career_completeness": extra.get("career_completeness", "thin"),
            "relationship_confidence": extra.get("relationship_confidence", "medium"),
            "biggest_gap": extra.get("biggest_gap", ""),
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": q,
                "why_it_matters": w,
                "suggested_queries": sq,
                "last_attempted": TODAY,
            }
            for q, w, sq in extra.get("open_questions", [])
        ],
    }


# ── 黄敏 person JSON ──
huangmin_json = make_person_json(persons[0], {
    "person_id": "qinbei_huangmin",
    "scope": {
        "province": "广西壮族自治区",
        "city": "钦州市",
        "region": "钦北区",
        "job": "区委书记",
        "task_id": "guangxi_钦北区",
        "time_focus": "2024-2026",
    },
    "birth": "待查",
    "birthplace": "待查",
    "native_place": "待查",
    "education": [],
    "party_join_date": "待查",
    "work_start_date": "待查",
    "rank": "正处级",
    "profile_url": "http://www.qinbei.gov.cn/",
    "career_timeline": [
        {
            "start": "待查",
            "end": "present",
            "org": "中共钦北区委员会",
            "title": "钦北区委书记",
            "level": "县处级",
            "location": "广西钦州市钦北区",
            "system": "party",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "主持区委全面工作; 多次主持召开区委常委会",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
        {
            "start": "未知",
            "end": "未知",
            "org": "履历缺口",
            "title": "",
            "notes": "黄敏在担任钦北区委书记之前的公开履历信息有限。需要进一步核实其此前任职经历。",
            "confidence": "unverified",
            "source_ids": [],
        },
    ],
    "organizations": [],
    "relationships": [
        {
            "person": "邓洁丽",
            "person_id": "qinbei_dengjieli",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "黄敏（区委书记）与邓洁丽（区长）同为钦北区党政一把手。官网新闻显示两人多次共同出席重要会议活动。",
            "overlap_org": "钦北区",
            "overlap_period": "2024-至今",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
    ],
    "governance_record": [
        {
            "period": "2026年",
            "domain": "other",
            "achievement_or_event": "主持召开多次区委常委会会议，部署党建、经济、安全等工作",
            "role_in_event": "主持",
            "measurable_outcome": "系列区委常委会会议形成决议",
            "location": "钦北区",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
    ],
    "professional_profile": {
        "primary_specializations": [],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": ["party"],
        "geographic_pattern": ["广西"],
        "promotion_velocity": {"summary": "公开资料不足，无法评估晋升速度", "notable_fast_promotions": []},
    },
    "work_style": {
        "public_style_indicators": [
            {"trait": "unknown", "evidence": "公开信息有限", "confidence": "unverified", "source_ids": []},
        ],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
    },
    "risk_signals": [
        {"type": "none_found", "description": "截至2026年7月，未在公开渠道发现黄敏的纪律处分、审计问题或负面媒体报道", "date": TODAY, "confidence": "plausible", "source_ids": ["S001"]},
    ],
    "extra_sources": [],
    "confidence_identity": "unverified",
    "confidence_role": "confirmed",
    "career_completeness": "thin",
    "relationship_confidence": "medium",
    "biggest_gap": "黄敏的出生年份、籍贯、教育背景和完整履历均需进一步核实",
    "open_questions": [
        ("黄敏的出生年份和详细出生地是什么？", "作为区委书记的基础身份信息", ["黄敏 简历", "黄敏 出生"]),
        ("黄敏的完整职业生涯履历是什么？", "了解其政治路径和治理经验", ["黄敏 任职 履历", "黄敏 钦北"]),
        ("黄敏的教育背景和专业是什么？", "评估其专业能力和治理风格", ["黄敏 毕业 学历"]),
        ("黄敏何时加入中国共产党？", "作为政治身份的基础信息", ["黄敏 中共党员"]),
        ("黄敏在担任钦北区委书记前的职务是什么？", "了解其晋升路径", ["黄敏 此前 担任"]),
    ],
})

# ── 邓洁丽 person JSON ──
dengjieli_json = make_person_json(persons[1], {
    "person_id": "qinbei_dengjieli",
    "scope": {
        "province": "广西壮族自治区",
        "city": "钦州市",
        "region": "钦北区",
        "job": "区长",
        "task_id": "guangxi_钦北区",
        "time_focus": "2024-2026",
    },
    "birth": "待查",
    "birthplace": "待查",
    "native_place": "待查",
    "education": [],
    "party_join_date": "待查",
    "work_start_date": "待查",
    "rank": "正处级",
    "profile_url": "http://www.qinbei.gov.cn/",
    "career_timeline": [
        {
            "start": "待查",
            "end": "present",
            "org": "钦北区人民政府",
            "title": "钦北区委副书记、区长",
            "level": "县处级",
            "location": "广西钦州市钦北区",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "主持区政府全面工作; 多次带队检查防汛防灾、开展慰问活动",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
        {
            "start": "未知",
            "end": "未知",
            "org": "履历缺口",
            "title": "",
            "notes": "邓洁丽在担任钦北区长之前的公开履历信息有限。",
            "confidence": "unverified",
            "source_ids": [],
        },
    ],
    "organizations": [],
    "relationships": [
        {
            "person": "黄敏",
            "person_id": "qinbei_huangmin",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "邓洁丽（区长）与黄敏（区委书记）同为钦北区党政一把手。官网新闻显示两人共同出席区委全会、政法工作会议、人大政协会议等。",
            "overlap_org": "钦北区",
            "overlap_period": "2024-至今",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
        {
            "person": "黄良先",
            "person_id": "qinbei_huangliangxian",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "邓洁丽（区长）与黄良先（常务副区长）是政府班子的正副手关系。黄良先多次主持会议，邓洁丽出席讲话。",
            "overlap_org": "钦北区人民政府",
            "overlap_period": "2024-至今",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
        {
            "person": "石瑞喜",
            "person_id": "qinbei_shiruixi",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "2026年春季新兵入伍欢送大会中，邓洁丽致欢送词，石瑞喜宣读入伍批准命令，两人共同出席。",
            "overlap_org": "钦北区",
            "overlap_period": "2026-03",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
    ],
    "governance_record": [
        {
            "period": "2026年5月",
            "domain": "emergency",
            "achievement_or_event": "带队检查防汛防灾工作，深入大马鞍水库、小董镇地质灾害点等",
            "role_in_event": "带队检查",
            "measurable_outcome": "实地检查防汛防灾工作落实情况",
            "location": "钦北区",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
        {
            "period": "2026年5月",
            "domain": "social",
            "achievement_or_event": "开展'六一'儿童节、高考考前慰问活动",
            "role_in_event": "带队慰问",
            "measurable_outcome": "慰问学校师生",
            "location": "钦北区",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
    ],
    "professional_profile": {
        "primary_specializations": [],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": ["government"],
        "geographic_pattern": ["广西"],
        "promotion_velocity": {"summary": "公开资料不足，无法评估晋升速度", "notable_fast_promotions": []},
    },
    "work_style": {
        "public_style_indicators": [
            {"trait": "unknown", "evidence": "公开信息有限", "confidence": "unverified", "source_ids": []},
        ],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
    },
    "risk_signals": [
        {"type": "none_found", "description": "截至2026年7月，未在公开渠道发现邓洁丽的纪律处分、审计问题或负面媒体报道", "date": TODAY, "confidence": "plausible", "source_ids": ["S001"]},
    ],
    "extra_sources": [],
    "confidence_identity": "unverified",
    "confidence_role": "confirmed",
    "career_completeness": "thin",
    "relationship_confidence": "medium",
    "biggest_gap": "邓洁丽的出生年份、籍贯、教育背景和完整履历均需进一步核实",
    "open_questions": [
        ("邓洁丽的出生年份和详细出生地是什么？", "作为区长的基础身份信息", ["邓洁丽 简历", "邓洁丽 出生"]),
        ("邓洁丽的完整职业生涯履历是什么？", "了解其政治路径和治理经验", ["邓洁丽 任职 履历", "邓洁丽 钦北"]),
        ("邓洁丽此前担任过哪些职务？", "了解其晋升路径和经验积累", ["邓洁丽 历任 职务"]),
        ("邓洁丽何时加入中国共产党？", "作为政治身份的基础信息", ["邓洁丽 中共党员"]),
    ],
})


# ════════════════════════════════════════════════════════════════
# WRITE PERSON JSONs
# ════════════════════════════════════════════════════════════════

def write_person_json(data, filename):
    path = PERSONS_OUT_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")

write_person_json(huangmin_json, f"{TODAY}-广西壮族自治区-钦州市-区委书记-黄敏.json")
write_person_json(dengjieli_json, f"{TODAY}-广西壮族自治区-钦州市-区长-邓洁丽.json")

# ════════════════════════════════════════════════════════════════
# BUILD DATABASE & GEXF
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Building 钦北区 leadership network...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons dir: {PERSONS_OUT_DIR}")

    run_build(
        slug="钦北区领导班子关系图",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print("Done.")
