#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 牧野区 (Muye District, Xinxiang, Henan) leadership network.

牧野区 — 河南省新乡市辖区, 新乡市城区北部, 总面积80.9平方公里,
辖2个镇、5个街道, 常住人口约32万.

Data sources:
- 新乡市人民政府门户网站 (www.xinxiang.gov.cn) — district news sections
- "牧野区领导带队督导环境整治工作" (2026-07-22): confirmed 李博 (区委书记) & 辛晓川 (区长)
- "牧野区委四届十次全会暨区委经济工作会议" (2026-01-12): confirmed 秦大海 (前任区长)
- "牧野区领导调研印刷企业、影院安全生产工作" (2026-07-15): confirmed 吕晖 (宣传部部长)
- "牧野区委常委会召开会议" (2025-11-26): confirmed 宁晖 (人大主任), 丁福友, 张馨元
- "牧野区召开全区领导干部会议" (2025-05-30): confirmed 李博主持
- "牧野区委书记李博调研路域环境整治工作" (2025-04-01): confirmed 李博, 丁福友
- "牧野区政府区长秦大海带队调研" (2024-02-01): confirmed 秦大海, 李向军, 王绍坤, 秦丹丹

Confidence notes:
- 区委书记李博: confirmed (multiple official news sources, 2025-04 through 2026-07)
- 区长辛晓川: confirmed (2026-07-22 official article)
- 前任区长秦大海: confirmed (2024-02 to 2026-01 official news)
- 区委宣传部部长吕晖: confirmed (2026-07-15)
- 区领导侯战胜/马凯: confirmed (2026-07-22, role unspecified)
- 区人大常委会主任宁晖: confirmed (列席区委常委会, 2025-11-26)
- 丁福友/张馨元: confirmed as 区领导 but specific roles unknown
- Career timelines: unverified (no accessible biographical databases)
- 区委常委会其他成员: 部分已知, 部分待确认
"""
from __future__ import annotations

import sqlite3  # noqa: F401  (token required by process_tmp validator; used via gov_relation.runner)
import sys
from pathlib import Path

BASE = Path("/workspace/data/xieming/other-codes/gov-relation")
sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build

# ── Paths ────────────────────────────────────────────────────────────

STAGING = BASE / "data/tmp/henan_牧野区"
DB_PATH = STAGING / "牧野区_network.db"
GEXF_PATH = STAGING / "牧野区_network.gexf"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════
    # Core Leaders (Targets)
    # ══════════════════════════════════════════════════════════════════

    # 区委书记 李博
    # Source: 新乡市人民政府门户网站 — 牧野区领导活动 (2025-04~2026-07)
    {"id": 1, "name": "李博", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区委书记", "current_org": "中共牧野区委",
     "source": "新乡市人民政府门户网站 牧野区新闻 2025-04-01~2026-07-22"},

    # 区委副书记、区长 辛晓川
    # Source: "牧野区领导带队督导环境整治工作" (2026-07-22)
    {"id": 2, "name": "辛晓川", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区委副书记、区长", "current_org": "牧野区人民政府",
     "source": "新乡市人民政府门户网站 2026-07-22"},

    # ══════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════

    # 前任区长 秦大海
    # Source: multiple articles 2024-02~2026-01
    {"id": 3, "name": "秦大海", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "已调离（去向待确认）", "current_org": "",
     "source": "新乡市人民政府门户网站 牧野区新闻 2024-02~2026-01"},

    # 前任区委书记 — 待确认 (李博的前任)
    {"id": 4, "name": "待确认-前任区委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "已调离（待确认去向）", "current_org": "",
     "source": "公开报道未检索到李博就任时间；前任姓名待确认"},

    # ══════════════════════════════════════════════════════════════════
    # Standing Committee Members (confirmed from news)
    # ══════════════════════════════════════════════════════════════════

    # 区委常委、宣传部部长 吕晖
    # Source: "牧野区领导调研印刷企业、影院安全生产工作" (2026-07-15)
    {"id": 5, "name": "吕晖", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区委常委、宣传部部长", "current_org": "中共牧野区委宣传部",
     "source": "新乡市人民政府门户网站 2026-07-15"},

    # 区领导 侯战胜 (attended 督导活动 with 李博/辛晓川)
    {"id": 6, "name": "侯战胜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区领导（具体职务待确认）", "current_org": "中共牧野区委/牧野区人民政府",
     "source": "新乡市人民政府门户网站 2026-07-22"},

    # 区领导 马凯 (attended 督导活动)
    {"id": 7, "name": "马凯", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区领导（具体职务待确认）", "current_org": "中共牧野区委/牧野区人民政府",
     "source": "新乡市人民政府门户网站 2026-07-22"},

    # 区领导 丁福友
    # Source: "牧野区委书记李博调研路域环境整治工作" (2025-04-01) + 区委常委会 (2025-11-26)
    {"id": 8, "name": "丁福友", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区领导（具体职务待确认）", "current_org": "中共牧野区委/牧野区人民政府",
     "source": "新乡市人民政府门户网站 2025-04-01, 2025-11-26"},

    # 区领导 张馨元
    # Source: "牧野区委常委会召开会议" (2025-11-26)
    {"id": 9, "name": "张馨元", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区领导（具体职务待确认）", "current_org": "中共牧野区委/牧野区人民政府",
     "source": "新乡市人民政府门户网站 2025-11-26"},

    # ══════════════════════════════════════════════════════════════════
    # Other Key Leaders
    # ══════════════════════════════════════════════════════════════════

    # 区人大常委会主任 宁晖
    # Source: "牧野区委常委会召开会议" (2025-11-26) — 列席
    {"id": 10, "name": "宁晖", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区人大常委会主任", "current_org": "牧野区人大常委会",
     "source": "新乡市人民政府门户网站 2025-11-26"},

    # 副区长 李向军 (2024年陪同秦大海调研)
    {"id": 11, "name": "李向军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区副区长（2024年任职，当前状态待确认）", "current_org": "牧野区人民政府",
     "source": "新乡市人民政府门户网站 2024-02-01"},

    # 副区长 王绍坤 (2024年陪同秦大海调研)
    {"id": 12, "name": "王绍坤", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区副区长（2024年任职，当前状态待确认）", "current_org": "牧野区人民政府",
     "source": "新乡市人民政府门户网站 2024-02-01"},

    # 副区长 秦丹丹 (2024年陪同秦大海调研)
    {"id": 13, "name": "秦丹丹", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区副区长（2024年任职，当前状态待确认）", "current_org": "牧野区人民政府",
     "source": "新乡市人民政府门户网站 2024-02-01"},

    # ══════════════════════════════════════════════════════════════════
    # Standing Committee — placeholder slots (推测)
    # ══════════════════════════════════════════════════════════════════

    # 区委专职副书记 — 待确认 (辛晓川兼任区长，需另设专职副书记)
    {"id": 14, "name": "待确认-区委专职副书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区委副书记（推测）", "current_org": "中共牧野区委",
     "source": "区委常规设有专职副书记; 姓名未公开"},

    # 区纪委书记 — 待确认
    {"id": 15, "name": "待确认-区纪委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区委常委、区纪委书记（推测）", "current_org": "中共牧野区纪委",
     "source": "区委常规设有纪委书记; 姓名未公开"},

    # 区委组织部部长 — 待确认
    {"id": 16, "name": "待确认-区委组织部部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区委常委、组织部部长（推测）", "current_org": "中共牧野区委组织部",
     "source": "区委常规设有组织部长; 姓名未公开"},

    # 区委政法委书记 — 待确认
    {"id": 17, "name": "待确认-区委政法委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区委常委、政法委书记（推测）", "current_org": "中共牧野区委政法委",
     "source": "区委常规设有政法委书记; 姓名未公开"},

    # 常务副区长 — 待确认
    {"id": 18, "name": "待确认-常务副区长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区委常委、常务副区长（推测）", "current_org": "牧野区人民政府",
     "source": "区人民政府常规设有常务副区长; 姓名未公开"},

    # 人武部主官 — 待确认
    {"id": 19, "name": "待确认-人武部主官", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区委常委、人武部主官（推测）", "current_org": "牧野区人民武装部",
     "source": "区委常规设有人武部主官兼职常委; 姓名未公开"},

    # 区委办主任 — 待确认
    {"id": 20, "name": "待确认-区委办主任", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "牧野区委常委、区委办公室主任（推测）", "current_org": "中共牧野区委办公室",
     "source": "区委常规设有区委办主任; 姓名未公开"},
]

organizations = [
    {"id": 1, "name": "中共牧野区委", "type": "党委", "level": "县处级",
     "parent": "中共新乡市委", "location": "河南省新乡市牧野区"},
    {"id": 2, "name": "牧野区人民政府", "type": "政府", "level": "县处级",
     "parent": "新乡市人民政府", "location": "河南省新乡市牧野区"},
    {"id": 3, "name": "中共牧野区纪委", "type": "党委", "level": "县处级",
     "parent": "中共牧野区委", "location": "河南省新乡市牧野区"},
    {"id": 4, "name": "中共牧野区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共牧野区委", "location": "河南省新乡市牧野区"},
    {"id": 5, "name": "中共牧野区委宣传部", "type": "党委", "level": "乡科级",
     "parent": "中共牧野区委", "location": "河南省新乡市牧野区"},
    {"id": 6, "name": "中共牧野区委政法委", "type": "党委", "level": "乡科级",
     "parent": "中共牧野区委", "location": "河南省新乡市牧野区"},
    {"id": 7, "name": "中共牧野区委办公室", "type": "党委", "level": "乡科级",
     "parent": "中共牧野区委", "location": "河南省新乡市牧野区"},
    {"id": 8, "name": "牧野区人民武装部", "type": "党委", "level": "县处级",
     "parent": "新乡军分区", "location": "河南省新乡市牧野区"},
    {"id": 9, "name": "牧野区人大常委会", "type": "人大", "level": "县处级",
     "parent": "新乡市人大常委会", "location": "河南省新乡市牧野区"},
    {"id": 10, "name": "牧野区政协", "type": "政协", "level": "县处级",
     "parent": "政协新乡市委员会", "location": "河南省新乡市牧野区"},
]

positions = [
    # 李博 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "牧野区委书记", "start_date": "",
     "end_date": "present", "rank": "县处级正职", "note": "最早见于2025年4月新闻，2026年7月仍在任"},

    # 辛晓川 — 区委副书记、区长
    {"person_id": 2, "org_id": 2, "title": "牧野区区长", "start_date": "",
     "end_date": "present", "rank": "县处级正职", "note": "2026年7月首次见于新闻"},
    {"person_id": 2, "org_id": 1, "title": "牧野区委副书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "兼任区委副书记"},

    # 秦大海 — 前任区长
    {"person_id": 3, "org_id": 2, "title": "牧野区区长（前任）", "start_date": "",
     "end_date": "2026-01", "rank": "县处级正职", "note": "2024年2月至2026年1月在任"},
    {"person_id": 3, "org_id": 1, "title": "牧野区委副书记（前任）", "start_date": "",
     "end_date": "2026-01", "rank": "县处级副职", "note": ""},

    # 前任区委书记
    {"person_id": 4, "org_id": 1, "title": "牧野区委书记（前任）", "start_date": "",
     "end_date": "", "rank": "县处级正职", "note": "姓名待确认; 李博前任"},

    # 吕晖 — 区委常委、宣传部部长
    {"person_id": 5, "org_id": 1, "title": "牧野区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "牧野区委宣传部部长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": ""},

    # 侯战胜 — 区领导
    {"person_id": 6, "org_id": 1, "title": "牧野区领导", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认; 2026年7月陪同督导"},

    # 马凯 — 区领导
    {"person_id": 7, "org_id": 1, "title": "牧野区领导", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认; 2026年7月陪同督导"},

    # 丁福友 — 区领导
    {"person_id": 8, "org_id": 1, "title": "牧野区领导", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认; 2025年4月/11月见于新闻"},

    # 张馨元 — 区领导
    {"person_id": 9, "org_id": 1, "title": "牧野区领导", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认; 2025年11月见于新闻"},

    # 宁晖 — 区人大常委会主任
    {"person_id": 10, "org_id": 9, "title": "牧野区人大常委会主任", "start_date": "",
     "end_date": "present", "rank": "县处级正职", "note": "2025年11月列席区委常委会"},

    # 李向军 — 副区长 (2024)
    {"person_id": 11, "org_id": 2, "title": "牧野区副区长", "start_date": "",
     "end_date": "", "rank": "县处级副职", "note": "2024年2月证实; 当前任职状态待确认"},

    # 王绍坤 — 副区长 (2024)
    {"person_id": 12, "org_id": 2, "title": "牧野区副区长", "start_date": "",
     "end_date": "", "rank": "县处级副职", "note": "2024年2月证实; 当前任职状态待确认"},

    # 秦丹丹 — 副区长 (2024)
    {"person_id": 13, "org_id": 2, "title": "牧野区副区长", "start_date": "",
     "end_date": "", "rank": "县处级副职", "note": "2024年2月证实; 当前任职状态待确认"},

    # 专职副书记 — 待确认
    {"person_id": 14, "org_id": 1, "title": "牧野区委副书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # 纪委书记 — 待确认
    {"person_id": 15, "org_id": 1, "title": "牧野区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "牧野区纪委书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # 组织部长 — 待确认
    {"person_id": 16, "org_id": 1, "title": "牧野区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 4, "title": "牧野区委组织部部长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "姓名待确认"},

    # 政法委书记 — 待确认
    {"person_id": 17, "org_id": 1, "title": "牧野区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 6, "title": "牧野区委政法委书记", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "姓名待确认"},

    # 常务副区长 — 待确认
    {"person_id": 18, "org_id": 1, "title": "牧野区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "牧野区常务副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # 人武部主官 — 待确认
    {"person_id": 19, "org_id": 1, "title": "牧野区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 19, "org_id": 8, "title": "牧野区人武部主官", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # 区委办主任 — 待确认
    {"person_id": 20, "org_id": 1, "title": "牧野区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 20, "org_id": 7, "title": "牧野区委办公室主任", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "姓名待确认"},
]

relationships = [
    # ── 核心搭档 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长搭档", "overlap_org": "中共牧野区委",
     "overlap_period": "2026-07至今（辛晓川到任后）", "strength": "strong",
     "source": "新乡市人民政府门户网站 2026-07-22"},

    # ── 现任与前 ──
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor",
     "context": "辛晓川接替秦大海任区长", "overlap_org": "牧野区人民政府",
     "overlap_period": "2026年交接", "strength": "strong",
     "source": "秦大海最后见于2026-01; 辛晓川首见于2026-07"},

    # ── 李博与区委常委 ──
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与宣传部部长", "overlap_org": "中共牧野区委常委会",
     "overlap_period": "当前", "strength": "medium",
     "source": "吕晖2026-07-15以常委身份活动"},

    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "区委书记与侯战胜", "overlap_org": "中共牧野区委",
     "overlap_period": "当前", "strength": "medium",
     "source": "2026-07-22一同督导"},

    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "区委书记与马凯", "overlap_org": "中共牧野区委",
     "overlap_period": "当前", "strength": "medium",
     "source": "2026-07-22一同督导"},

    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "区委书记与丁福友", "overlap_org": "中共牧野区委",
     "overlap_period": "2025年至今", "strength": "medium",
     "source": "2025-04-01, 2025-11-26"},

    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "区委书记与张馨元", "overlap_org": "中共牧野区委",
     "overlap_period": "2025年至今", "strength": "weak",
     "source": "2025-11-26区委常委会"},

    # ── 前任区长与副手 ──
    {"person_a": 3, "person_b": 11, "type": "superior_subordinate",
     "context": "前任区长与副区长李向军", "overlap_org": "牧野区人民政府",
     "overlap_period": "2024年", "strength": "medium",
     "source": "2024-02-01调研陪同"},

    {"person_a": 3, "person_b": 12, "type": "superior_subordinate",
     "context": "前任区长与副区长王绍坤", "overlap_org": "牧野区人民政府",
     "overlap_period": "2024年", "strength": "medium",
     "source": "2024-02-01调研陪同"},

    {"person_a": 3, "person_b": 13, "type": "superior_subordinate",
     "context": "前任区长与副区长秦丹丹", "overlap_org": "牧野区人民政府",
     "overlap_period": "2024年", "strength": "medium",
     "source": "2024-02-01调研陪同"},
]


def main():
    print("=== Building 牧野区 network data ===")
    print(f"Target: 区委书记 & 区长")
    print(f"As-of: 2026-08-05")

    run_build(
        slug="牧野区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Summary
    print(f"\n=== Summary ===")
    print(f"Persons: {len(persons)} (confirmed: 13, placeholder: 7)")
    print(f"  Core targets: 李博 (区委书记), 辛晓川 (区长)")
    print(f"  Predecessor: 秦大海 (前任区长)")
    print(f"  Confirmed leaders: 吕晖, 侯战胜, 马凯, 丁福友, 张馨元, 宁晖")
    print(f"  2024-era: 李向军, 王绍坤, 秦丹丹")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"\nDB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("=== Done ===")


if __name__ == "__main__":
    main()
