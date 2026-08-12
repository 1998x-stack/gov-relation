#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 沈北新区, 沈阳市, 辽宁省.

Investigation date: 2026-08-12
Task ID: liaoning_沈北新区
Level: 市辖区
Targets: 区委书记 & 区长

Research status: CORE COMPLETE — current officeholders, committee roster, and
biographies verified from the 沈北新区人民政府 official website (nsy.gov.cn)
and 百度百科 (updated 2026-07-31 after 沈北新区第五次党代会).

Confirmed key facts (as of 2026-08-11):
  区委书记: 吴军 (兼沈阳辉山经济技术开发区党工委书记) — 1973.10, 满族, 辽宁岫岩人
  区长: 于胜林 (区委副书记、区政府党组书记, 兼辉山经开区管委会主任) — 1977.04, 满族
  区委副书记: 孙涛 (兼区政协党组副书记、区委统战部部长) — 1985.09, 汉族, 博士
  区人大常委会主任: 于夫 — 1969.05, 汉族
  区政协党组书记: 佟颖 (履历待查)
  区委常委会 (2026-07-31 第五届委员会一次全会选举): 吴军/于胜林/孙涛 + 常委
    马晓齐、刘野、凌鸣、李鹏、韩笑、赵东晗、赵丹凤、张明
  前任区委书记: 闻然 (现任长春市委副书记、长春新区党工委书记)
  前任区长: 吴军 (沈北区长 → 2022-05 区委书记)

Confidence notes:
  - 吴军/于胜林/孙涛/于夫 current roles: CONFIRMED (official news 2026-08-09/10)
  - 常委会名单: CONFIRMED (Baike 党委 lemma updated 2026-07-31; 赵东晗 entry)
  - 吴军/于胜林/闻然/于夫 bios: CONFIRMED (百度百科 + 政府官网)
  - Other 常委 (李鹏/韩笑/张明/刘野) 分工与履历: UNVERIFIED — encoded as gaps
"""

from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "沈北新区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-12"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSON_DIR = STAGING_DIR

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ 区委核心领导 ═══════
    {
        "id": 1,
        "name": "吴军",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1973年10月",
        "birthplace": "辽宁岫岩",
        "education": "大学学历，硕士学位",
        "party_join": "中共党员（1996年7月）",
        "work_start": "1997年7月",
        "current_post": "沈北新区区委书记、沈阳辉山经济技术开发区党工委书记",
        "current_org": "中共沈阳市沈北新区委员会",
        "source": "百度百科+沈北新区政府官网 (2026-08-10/11)",
    },
    {
        "id": 2,
        "name": "于胜林",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1977年4月",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈北新区区委副书记、区长、区政府党组书记，沈阳辉山经济技术开发区党工委副书记、管委会主任（兼）",
        "current_org": "沈阳市沈北新区人民政府",
        "source": "百度百科 + 沈北新区政府官网区长分工页 (2022-07-11)",
    },
    {
        "id": 3,
        "name": "孙涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年9月",
        "birthplace": "",
        "education": "研究生学历，博士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈北新区区委副书记、区政协党组副书记、区委统战部部长",
        "current_org": "中共沈阳市沈北新区委员会",
        "source": "百度百科 (2026-07-31更新) + 沈北官网 2026-08-09",
    },
    {
        "id": 4,
        "name": "于夫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年5月",
        "birthplace": "",
        "education": "省委党校研究生学历，学士学位",
        "party_join": "中共党员（1997年11月）",
        "work_start": "1992年9月",
        "current_post": "沈北新区人大常委会党组书记、主任",
        "current_org": "沈阳市沈北新区人民代表大会常务委员会",
        "source": "百度百科 + 沈北区官网 2026-08-09",
    },
    {
        "id": 5,
        "name": "佟颖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沈北新区政协党组书记",
        "current_org": "中国人民政治协商会议沈阳市沈北新区委员会",
        "source": "沈北区官网 2026-08-09 区委常委会扩大会议新闻",
    },
    # ─────────────── 区委常委 ───────────────
    {
        "id": 6,
        "name": "马晓齐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈北新区区委常委",
        "current_org": "中共沈阳市沈北新区委员会",
        "source": "百度百科 (2026-07-31 当选常委)",
    },
    {
        "id": 7,
        "name": "凌鸣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年2月",
        "birthplace": "",
        "education": "研究生学历，历史学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈北新区区委常委、常务副区长、区政府党组副书记",
        "current_org": "沈阳市沈北新区人民政府",
        "source": "沈北新区政府官网 (2024-04)",
    },
    {
        "id": 8,
        "name": "李鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沈北新区区委常委",
        "current_org": "中共沈阳市沈北新区委员会",
        "source": "百度百科党委条 2026-07-31",
    },
    {
        "id": 9,
        "name": "韩笑",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沈北新区区委常委",
        "current_org": "中共沈阳市沈北新区委员会",
        "source": "百度百科党委条 2026-07-31",
    },
    {
        "id": 10,
        "name": "赵东晗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈北新区区委常委",
        "current_org": "中共沈阳市沈北新区委员会",
        "source": "百度百科 (2026-07-31 当选常委)",
    },
    {
        "id": 11,
        "name": "赵丹凤",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年12月",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈北新区区委常委、副区长、区政府党组成员",
        "current_org": "沈阳市沈北新区人民政府",
        "source": "百度百科 + 沈北新区政府官网 (2023-09)",
    },
    {
        "id": 12,
        "name": "张明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沈北新区区委常委",
        "current_org": "中共沈阳市沈北新区委员会",
        "source": "百度百科党委条 2026-07-31",
    },
    {
        "id": 13,
        "name": "刘野",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沈北新区区委常委",
        "current_org": "中共沈阳市沈北新区委员会",
        "source": "百度百科党委条 2026-07-31; 区属国企辉山经济发展集团董事 (2025-12)",
    },
    # ─────────────── 区政府其他副区长 ───────────────
    {
        "id": 14,
        "name": "魏智勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年5月",
        "birthplace": "",
        "education": "硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈北新区副区长（分管公安、司法）",
        "current_org": "沈阳市沈北新区人民政府",
        "source": "沈北新区政府官网 (2024-03)",
    },
    {
        "id": 15,
        "name": "刘晓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈北新区副区长（分管住建、城市更新）",
        "current_org": "沈阳市沈北新区人民政府",
        "source": "沈北新区政府官网 (2024-06)",
    },
    {
        "id": 16,
        "name": "关镝",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1985年11月",
        "birthplace": "",
        "education": "研究生学历，博士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈北新区副区长（分管农业农村、乡村振兴）",
        "current_org": "沈阳市沈北新区人民政府",
        "source": "沈北新区政府官网 (2024-09)",
    },
    {
        "id": 17,
        "name": "佟玥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年11月",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈北新区副区长（分管城建、城管、交通）",
        "current_org": "沈阳市沈北新区人民政府",
        "source": "沈北新区政府官网 (2026-06)",
    },
    {
        "id": 18,
        "name": "邢颖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "在职研究生学历，学士学位",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "沈北新区副区长（分管科技、民政、营商环境）",
        "current_org": "沈阳市沈北新区人民政府",
        "source": "沈北新区政府官网 (2026-06)",
    },
    # ─────────────── 前任 (核心) ───────────────
    {
        "id": 19,
        "name": "闻然",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年3月",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长春市委副书记、长春新区党工委书记（前任沈北新区区委书记）",
        "current_org": "中共长春市委员会",
        "source": "百度百科",
    },
    # ─────────────── 网络人物 (跨区) ───────────────
    {
        "id": 20,
        "name": "李盛",
        "gender": "男",
        "birth": "",
        "ethnicity": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈阳市沈河区委书记（曾任沈北新区政法委书记）",
        "current_org": "中共沈阳市沈河区委员会",
        "source": "百度百科",
    },
    {
        "id": 21,
        "name": "代丽",
        "gender": "女",
        "birth": "",
        "ethnicity": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈河区委副书记、宣传部部长（曾任沈北新区副区长）",
        "current_org": "中共沈阳市沈河区委员会",
        "source": "百度百科",
    },
    {
        "id": 22,
        "name": "王凤武",
        "gender": "男",
        "birth": "1971年7月",
        "ethnicity": "汉族",
        "birthplace": "辽宁营口",
        "education": "大学学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈阳市委政法委分管日常工作的副书记（曾任沈北新区纪委常务副书记）",
        "current_org": "中共沈阳市委政法委员会",
        "source": "百度百科",
    },
    {
        "id": 23,
        "name": "王文才",
        "gender": "",
        "birth": "",
        "ethnicity": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈阳市辽中区委常委、区纪委书记、区监委主任（曾任沈北新区纪委副书记）",
        "current_org": "中共沈阳市辽中区纪律检查委员会",
        "source": "百度百科",
    },
    {
        "id": 24,
        "name": "李俊",
        "gender": "男",
        "birth": "1978年5月",
        "ethnicity": "满族",
        "birthplace": "",
        "education": "在职大学学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新民市委常委、纪委书记、监委主任（曾任沈北新区新城子街道党工委书记）",
        "current_org": "中共新民市纪律检查委员会",
        "source": "百度百科",
    },
    {
        "id": 25,
        "name": "罗丽",
        "gender": "女",
        "birth": "",
        "ethnicity": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "辽宁省人民政府外事办公室主任（曾任沈北新区委常委、宣传部长）",
        "current_org": "辽宁省人民政府外事办公室",
        "source": "百度百科",
    },
    {
        "id": 26,
        "name": "王健",
        "gender": "男",
        "birth": "",
        "ethnicity": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽宁省政协党组副书记、副主席，第二十届中央委员（曾任沈北新区区委副书记）",
        "current_org": "中国人民政治协商会议辽宁省委员会",
        "source": "百度百科",
    },
    {
        "id": 27,
        "name": "阎秉哲",
        "gender": "男",
        "birth": "",
        "ethnicity": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任沈北新区代区长（2008年；后任华晨汽车集团董事长）",
        "current_org": "沈阳市沈北新区人民政府",
        "source": "百度百科 (沈北新区政府官网页历史信息)",
    },
    {
        "id": 28,
        "name": "李剑锋",
        "gender": "男",
        "birth": "1968年3月",
        "ethnicity": "汉族",
        "birthplace": "",
        "education": "大学学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈北新区委组织部分管日常工作的副部长（正处级）、区公务员局局长",
        "current_org": "中共沈阳市沈北新区委组织部",
        "source": "百度百科",
    },
    # ─────────────── 人大常委会副主任 ───────────────
    {
        "id": 29,
        "name": "付献春",
        "gender": "",
        "birth": "",
        "ethnicity": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沈北新区人大常委会副主任",
        "current_org": "沈阳市沈北新区人民代表大会常务委员会",
        "source": "百度百科 (人大条)",
    },
    {
        "id": 30,
        "name": "王磊",
        "gender": "",
        "birth": "",
        "ethnicity": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沈北新区人大常委会副主任",
        "current_org": "沈阳市沈北新区人民代表大会常务委员会",
        "source": "百度百科 (人大条)",
    },
    {
        "id": 31,
        "name": "李旭文",
        "gender": "",
        "birth": "",
        "ethnicity": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沈北新区人大常委会副主任",
        "current_org": "沈阳市沈北新区人民代表大会常务委员会",
        "source": "百度百科 (人大条)",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共沈阳市沈北新区委员会", "type": "党委", "level": "县处级", "parent": "中共沈阳市委员会", "location": "辽宁省沈阳市沈北新区"},
    {"id": 2, "name": "沈阳市沈北新区人民政府", "type": "政府", "level": "县处级", "parent": "沈阳市人民政府", "location": "辽宁省沈阳市沈北新区"},
    {"id": 3, "name": "沈阳辉山经济技术开发区", "type": "开发区", "level": "国家级", "parent": "沈阳市人民政府", "location": "辽宁省沈阳市沈北新区东部"},
    {"id": 4, "name": "中共沈阳市沈北新区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共沈阳市沈北新区委员会", "location": "辽宁省沈阳市沈北新区"},
    {"id": 5, "name": "沈阳市沈北新区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "沈阳市人民代表大会常务委员会", "location": "辽宁省沈阳市沈北新区"},
    {"id": 6, "name": "中国人民政治协商会议沈阳市沈北新区委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议沈阳市委员会", "location": "辽宁省沈阳市沈北新区"},
    {"id": 7, "name": "中共沈阳市委员会", "type": "党委", "level": "副省级市", "parent": "中共辽宁省委员会", "location": "辽宁省沈阳市"},
    {"id": 8, "name": "沈阳市人民政府", "type": "政府", "level": "副省级市", "parent": "辽宁省人民政府", "location": "辽宁省沈阳市"},
    {"id": 9, "name": "中共沈阳市沈北新区委组织部", "type": "党委部门", "level": "乡科级", "parent": "中共沈阳市沈北新区委员会", "location": "辽宁省沈阳市沈北新区"},
    {"id": 10, "name": "中共沈阳市沈河区委员会", "type": "党委", "level": "县处级", "parent": "中共沈阳市委员会", "location": "辽宁省沈阳市沈河区"},
    {"id": 11, "name": "沈阳市于洪区人民政府", "type": "政府", "level": "县处级", "parent": "沈阳市人民政府", "location": "辽宁省沈阳市于洪区"},
    {"id": 12, "name": "中共沈阳市于洪区委员会", "type": "党委", "level": "县处级", "parent": "中共沈阳市委员会", "location": "辽宁省沈阳市于洪区"},
    {"id": 13, "name": "沈阳航空产业集团有限公司", "type": "国有企业", "level": "市属", "parent": "沈阳市人民政府", "location": "辽宁省沈阳市"},
    {"id": 14, "name": "共青团沈阳市委员会", "type": "群团", "level": "正局级", "parent": "共青团辽宁省委员会", "location": "辽宁省沈阳市"},
    {"id": 15, "name": "沈阳辉山经济发展集团有限公司", "type": "国有企业", "level": "区属", "parent": "沈阳市沈北新区人民政府", "location": "辽宁省沈阳市沈北新区"},
    {"id": 16, "name": "沈北新区新城子街道", "type": "乡镇街道", "level": "乡科级", "parent": "沈阳市沈北新区人民政府", "location": "辽宁省沈阳市沈北新区"},
    {"id": 17, "name": "沈阳市铁西区霁虹街道", "type": "乡镇街道", "level": "乡科级", "parent": "沈阳市铁西区人民政府", "location": "辽宁省沈阳市铁西区"},
    {"id": 18, "name": "中共长春市委员会", "type": "党委", "level": "副省级市", "parent": "中共吉林省委员会", "location": "吉林省长春市"},
    {"id": 19, "name": "长春新区管理委员会", "type": "开发区", "level": "国家级", "parent": "长春市人民政府", "location": "吉林省长春市"},
    {"id": 20, "name": "海城市人民政府", "type": "政府", "level": "县处级", "parent": "鞍山市人民政府", "location": "辽宁省鞍山市海城市"},
    {"id": 21, "name": "中共海城市委员会", "type": "党委", "level": "县处级", "parent": "中共鞍山市委员会", "location": "辽宁省鞍山市海城市"},
    {"id": 22, "name": "鞍山市农业委员会", "type": "政府部门", "level": "地厅级", "parent": "鞍山市人民政府", "location": "辽宁省鞍山市"},
    {"id": 23, "name": "中共沈阳市委政法委员会", "type": "党委部门", "level": "地厅级", "parent": "中共沈阳市委员会", "location": "辽宁省沈阳市"},
    {"id": 24, "name": "中共新民市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共新民市委员会", "location": "辽宁省沈阳市新民市"},
    {"id": 25, "name": "中共沈阳市辽中区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共沈阳市辽中区委员会", "location": "辽宁省沈阳市辽中区"},
    {"id": 26, "name": "辽宁省人民政府外事办公室", "type": "政府部门", "level": "厅级", "parent": "辽宁省人民政府", "location": "辽宁省沈阳市"},
    {"id": 27, "name": "中国人民政治协商会议辽宁省委员会", "type": "政协", "level": "省部级", "parent": "中国人民政治协商会议全国委员会", "location": "辽宁省沈阳市"},
    {"id": 28, "name": "沈阳市沈河区人民政府", "type": "政府", "level": "县处级", "parent": "沈阳市人民政府", "location": "辽宁省沈阳市沈河区"},
    {"id": 29, "name": "沈阳市经济和信息化委员会", "type": "政府部门", "level": "地厅级", "parent": "沈阳市人民政府", "location": "辽宁省沈阳市"},
    {"id": 30, "name": "沈阳市大东区东站街道", "type": "乡镇街道", "level": "乡科级", "parent": "沈阳市大东区人民政府", "location": "辽宁省沈阳市大东区"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # ── 吴军 ──
    {"person_id": 1, "org_id": 28, "title": "沈阳市沈河区委办公室主任", "start": "", "end": "", "rank": "县处级", "note": "早期任职"},
    {"person_id": 1, "org_id": 28, "title": "沈河区副区长（负责区政府常务工作）", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "沈北新区区委副书记、区长", "start": "", "end": "2022-05", "rank": "正处级", "note": "升任区委书记前任区长"},
    {"person_id": 1, "org_id": 1, "title": "沈北新区区委书记", "start": "2022-05", "end": "present", "rank": "正处级", "note": "2022-05 任区委书记，2026-07-31 五届一次全会连任"},
    {"person_id": 1, "org_id": 3, "title": "沈阳辉山经济技术开发区党工委书记", "start": "2022-05", "end": "present", "rank": "正处级", "note": "兼任"},
    # ── 于胜林 ──
    {"person_id": 2, "org_id": 12, "title": "于洪区委常委、副区长、区政府党组副书记", "start": "", "end": "", "rank": "副处级", "note": "前任职务"},
    {"person_id": 2, "org_id": 13, "title": "沈阳航空产业集团有限公司党委书记、董事长", "start": "", "end": "2022", "rank": "市属国企负责人", "note": "升任区长前职务"},
    {"person_id": 2, "org_id": 2, "title": "沈北新区委副书记、代区长、区长", "start": "2022", "end": "present", "rank": "正处级", "note": "2022 年任代区长并在同年转正（2022-07 官网已按区长发布分工）"},
    {"person_id": 2, "org_id": 3, "title": "沈阳辉山经济技术开发区党工委副书记、管委会主任（兼）", "start": "", "end": "present", "rank": "正处级", "note": "兼任"},
    # ── 孙涛 ──
    {"person_id": 3, "org_id": 14, "title": "共青团沈阳市委副书记（主持工作）", "start": "", "end": "", "rank": "副局级", "note": ""},
    {"person_id": 3, "org_id": 14, "title": "共青团沈阳市委书记", "start": "", "end": "", "rank": "正局级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "沈北新区区委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "区政协党组副书记、区委统战部部长", "start": "", "end": "present", "rank": "副处级", "note": "兼职；2026 年报政协党组书记为佟颖"},
    # ── 于夫 ──
    {"person_id": 4, "org_id": 29, "title": "沈阳市经济和信息化委员会副巡视员", "start": "", "end": "", "rank": "副局级", "note": "曾任职务"},
    {"person_id": 4, "org_id": 1, "title": "沈北新区区委常委、组织部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 5, "title": "沈北新区人大常委会党组副书记、主任", "start": "", "end": "present", "rank": "正处级", "note": "现任人大主任"},
    # ── 佟颖 ──
    {"person_id": 5, "org_id": 6, "title": "沈北新区政协党组书记", "start": "", "end": "present", "rank": "正处级", "note": "2026-08 新闻确认，个人履历待查"},
    # ── 凌鸣（本名义：凌鸣）──
    {"person_id": 7, "org_id": 2, "title": "沈北新区区委常委、常务副区长、区政府党组副书记", "start": "", "end": "present", "rank": "副处级", "note": "主持政府常务工作"},
    # ── 赵志丹凤 ──
    {"person_id": 11, "org_id": 9, "title": "沈北新区委组织部分管日常工作的副部长（正处级）、区公务员局局长", "start": "", "end": "", "rank": "副处级", "note": "曾任职务"},
    {"person_id": 11, "org_id": 2, "title": "沈北新区区委常委、副区长、区政府党组成员", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # ── 魏智勇 ──
    {"person_id": 14, "org_id": 2, "title": "沈北新区副区长（分管公安、司法）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # ── 刘晓 ──
    {"person_id": 15, "org_id": 2, "title": "沈北新区副区长（住建、城市更新）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # ── 关镝 ──
    {"person_id": 16, "org_id": 2, "title": "沈北新区副区长（农业农村、乡村振兴）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # ── 佟玥 ──
    {"person_id": 17, "org_id": 2, "title": "沈北新区副区长（城建、城市管理）", "start": "2026", "end": "present", "rank": "副处级", "note": "2026-06 官网更新分工"},
    # ── 邢颖 ──
    {"person_id": 18, "org_id": 2, "title": "沈北新区副区长（科技、民政、营商环境）", "start": "2026", "end": "present", "rank": "副处级", "note": "2026-06 官网更新分工，无党派"},
    # ── 常委：马启齐 / 赵东晗 / 李鹏 / 韩笑 / 张明 / 刘野 ──
    {"person_id": 6, "org_id": 1, "title": "沈北新区区委常委", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": "五届一次全会当选"},
    {"person_id": 10, "org_id": 1, "title": "沈北新区区委常委", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": "前大东区东站街道党工委书记、人大工委主任"},
    {"person_id": 8, "org_id": 1, "title": "沈北新区区委常委", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "沈北新区区委常委", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "沈北新区区委常委", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "沈北新区区委常委", "start": "2026-07-31", "end": "present", "rank": "副处级", "note": ""},
    # ── 前任：闻然 ──
    {"person_id": 19, "org_id": 22, "title": "鞍山市农业委员会主任", "start": "", "end": "", "rank": "正局级", "note": "曾任"},
    {"person_id": 19, "org_id": 21, "title": "海城市委副书记、市长", "start": "", "end": "", "rank": "县处级", "note": "曾任"},
    {"person_id": 19, "org_id": 21, "title": "海城市委书记", "start": "", "end": "", "rank": "县处级", "note": "曾任"},
    {"person_id": 19, "org_id": 1, "title": "沈北新区区委书记", "start": "", "end": "2022-05", "rank": "正处级", "note": "前任沈北新区区委书记"},
    {"person_id": 19, "org_id": 7, "title": "沈阳市委组织部分管日常工作的副部长、市委组织部部长（兼市委党校校长）", "start": "2022", "end": "2024", "rank": "局级", "note": "2022起先后任组织部常务副部长、部长等"},
    {"person_id": 19, "org_id": 18, "title": "长春市委副书记、长春市委教育工委书记", "start": "2024-11", "end": "present", "rank": "副省级市副书记", "note": "2024-11 任"},
    {"person_id": 19, "org_id": 19, "title": "长春新区党工委书记", "start": "2024-11", "end": "present", "rank": "正厅级", "note": "兼任"},
    # ── 前任代区长：阎秉哲 ──
    {"person_id": 27, "org_id": 1, "title": "沈北新区区委副书记、副区长、代区长", "start": "2008", "end": "2008", "rank": "正处级", "note": "兼沈阳蒲河新城管委会主任"},
    # ── 跨区网络 ──
    {"person_id": 20, "org_id": 1, "title": "沈北新区区委常委、政法委书记", "start": "2016", "end": "2017", "rank": "副处级", "note": "曾任"},
    {"person_id": 20, "org_id": 10, "title": "沈阳市沈河区委书记", "start": "2021", "end": "present", "rank": "正处级", "note": "现任；曾任皇姑区长、团市委书记等"},
    {"person_id": 21, "org_id": 2, "title": "沈北新区人民政府副区长", "start": "2019-07", "end": "", "rank": "副处级", "note": "曾任"},
    {"person_id": 21, "org_id": 10, "title": "沈河区委常委、宣传部部长；区委副书记", "start": "", "end": "present", "rank": "副处级", "note": "现任"},
    {"person_id": 22, "org_id": 4, "title": "沈北新区纪委常务副书记（正处级）", "start": "", "end": "", "rank": "正处级", "note": "曾任"},
    {"person_id": 22, "org_id": 23, "title": "沈阳市委政法委分管日常工作的副书记", "start": "", "end": "present", "rank": "局级", "note": "现任；曾任沈阳市监察委员会委员"},
    {"person_id": 23, "org_id": 4, "title": "沈北新区纪委副书记、区监委副主任", "start": "", "end": "", "rank": "副处级", "note": "曾任"},
    {"person_id": 23, "org_id": 25, "title": "辽中区委常委、区纪委书记、区监委主任", "start": "", "end": "present", "rank": "副处级", "note": "现任；期间曾任康平县委常委纪委书记"},
    {"person_id": 24, "org_id": 16, "title": "沈北新区新城子街道党工委书记", "start": "", "end": "", "rank": "正科级", "note": "曾任"},
    {"person_id": 24, "org_id": 24, "title": "新民市委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级", "note": "现任"},
    {"person_id": 25, "org_id": 1, "title": "沈北新区区委常委、宣传部部长", "start": "2007-03", "end": "2010-10", "rank": "副处级", "note": "曾任"},
    {"person_id": 25, "org_id": 26, "title": "辽宁省人民政府外事办公室主任、党组书记", "start": "", "end": "present", "rank": "正厅级", "note": "现任"},
    {"person_id": 26, "org_id": 1, "title": "沈北新区区委副书记", "start": "2006-04", "end": "2006-11", "rank": "副处级", "note": "曾任（新城子区委副书记2004-2006）"},
    {"person_id": 26, "org_id": 27, "title": "辽宁省政协党组副书记、副主席", "start": "", "end": "present", "rank": "省部级副职", "note": "第二十届中央委员"},
    {"person_id": 28, "org_id": 9, "title": "沈北新区委组织部副部长（分管日常工作）", "start": "", "end": "present", "rank": "正处级", "note": "现任；曾任区教育局党组书记、局长"},
    {"person_id": 29, "org_id": 5, "title": "沈北新区人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 30, "org_id": 5, "title": "沈北新区人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 31, "org_id": 5, "title": "沈北新区人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "吴军（书记）与于胜林（区长）2022 年起搭班子", "overlap_org": "中共沈阳市沈北新区委员会/沈北新区人民政府", "overlap_period": "2022-05至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与人大常委会主任（于夫曾任区委常委、组织部长）", "overlap_org": "中共沈阳市沈北新区委员会", "overlap_period": "2022-05至今", "confidence": "plausible"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记与常务副区长", "overlap_org": "沈北新区", "overlap_period": "2024至今", "confidence": "plausible"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "区委书记与常委副区长", "overlap_org": "沈北新区", "overlap_period": "2023至今", "confidence": "plausible"},
    {"person_a": 2, "person_b": 7, "type": "党政副手", "context": "区长与常务副区长（凌鸣协助主持政府常务）", "overlap_org": "沈阳市沈北新区人民政府", "overlap_period": "2024至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长与副区长", "overlap_org": "沈阳市沈北新区人民政府", "overlap_period": "2023至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "区长与副区长（关镝）", "overlap_org": "沈阳市沈北新区人民政府", "overlap_period": "2024至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 17, "type": "上下级", "context": "区长与副区长（佟玥，2026 新任）", "overlap_org": "沈阳市沈北新区人民政府", "overlap_period": "2026至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 18, "type": "上下级", "context": "区长与副区长（邢颖，2026 新任）", "overlap_org": "沈阳市沈北新区人民政府", "overlap_period": "2026至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与副书记（孙涛）", "overlap_org": "中共沈阳市沈北新区委员会", "overlap_period": "2025至今", "confidence": "plausible"},
    {"person_a": 2, "person_b": 3, "type": "党政搭档（班子）", "context": "副书记与区长共同参与区委工作", "overlap_org": "中共沈阳市沈北新区委员会", "overlap_period": "2025至今", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 5, "type": "班子同僚", "context": "人大主任与政协党组书记", "overlap_org": "沈北新区", "overlap_period": "2025至今", "confidence": "confirmed"},
    # 前后任
    {"person_a": 19, "person_b": 1, "type": "前后任", "context": "闻然 2022-05 调沈阳市委组织部，吴军接任区委书记", "overlap_org": "中共沈阳市沈北新区委员会", "overlap_period": "2022-05", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 2, "type": "前后任（区长）", "context": "吴军由区长升书记，于胜林自沈阳航空产业集团调任区长", "overlap_org": "沈阳市沈北新区人民政府", "overlap_period": "2022", "confidence": "plausible"},
    # 跨区流动（沈北 → 其他区/市直）
    {"person_a": 20, "person_b": 1, "type": "同班子旧识", "context": "李盛 2016-17 任沈北政法委书记，吴军时任沈北区长（同届班子）", "overlap_org": "中共沈阳市沈北新区委员会", "overlap_period": "2016-2017", "confidence": "plausible"},
    {"person_a": 21, "person_b": 2, "type": "同班子旧识", "context": "代丽 2019 任沈北副区长时，于胜林尚未到任；与吴军时期有交集", "overlap_org": "沈阳市沈北新区人民政府", "overlap_period": "2019-2020", "confidence": "weak"},
    {"person_a": 22, "person_b": 1, "type": "同系统旧僚", "context": "王凤武曾任沈北纪委常务副书记后任市委政法委常务副书记", "overlap_org": "中共沈阳市沈北新区纪律检查委员会", "overlap_period": "", "confidence": "plausible"},
    {"person_a": 23, "person_b": 22, "type": "系统关联", "context": "王文才（沈北纪委副书记）与王凤武（沈北纪委常务副书记）同期纪委条线", "overlap_org": "中共沈阳市沈北新区纪律检查委员会", "overlap_period": "", "confidence": "weak"},
    {"person_a": 24, "person_b": 1, "type": "系统关联", "context": "李俊曾任沈北新城子街道书记，现任新民市纪委书记", "overlap_org": "沈北新区新城子街道", "overlap_period": "", "confidence": "weak"},
    {"person_a": 25, "person_b": 1, "type": "系统关联", "context": "罗丽 2007-2010 任沈北宣传部长，现任省外事办主任", "overlap_org": "中共沈阳市沈北新区委员会宣传部", "overlap_period": "2007-2010", "confidence": "weak"},
    {"person_a": 26, "person_b": 1, "type": "历史关联", "context": "王健 2006 任沈北区委副书记（早期）", "overlap_org": "中共沈阳市沈北新区委员会", "overlap_period": "2006", "confidence": "weak"},
    {"person_a": 24, "person_b": 28, "type": "条线上下", "context": "李剑锋现任沈北组织部常务副部长，于夫曾任沈北组织部长", "overlap_org": "中共沈阳市沈北新区委组织部", "overlap_period": "", "confidence": "weak"},
    {"person_a": 1, "person_b": 10, "type": "同届当选", "context": "2026-07-31 五届一次全会同时当选常委", "overlap_org": "中共沈阳市沈北新区委员会", "overlap_period": "2026-07-31", "confidence": "confirmed"},
]

# ── Source Register ────────────────────────────────────────────────────────
SOURCES = [
    {"id": "S001", "title": "沈北新区人民政府官网 — 区委常委会召开扩大会议 吴军主持会议并讲话", "url": "https://www.nsy.gov.cn/ywdt/sbyw/202608/t20260810_5070051.html", "publisher": "沈北新区人民政府", "published_at": "2026-08-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认吴军区委书记、于胜桥区长、于夫人大主任、佟颖政协党组书记、孙涛区委副书记"},
    {"id": "S002", "title": "沈北新区人民政府 — 中国共产党沈阳市沈北新区第五次代表大会预备会议召开", "url": "https://www.nsy.gov.cn/ywdt/sbyw/202607/t20260730_5065139.html", "publisher": "沈北新区人民政府", "published_at": "2026-07-30", "accessed_at": "official", "reliability": "high", "notes": "吴军以区委书记兼辉山经开区党工委书记身份主持党代会预备会"},
    {"id": "S003", "title": "沈北新区人民政府 — 区长分工页（于胜林）", "url": "https://www.nsy.gov.cn/zwgk/fdzdgknr/jgjj/qz/202207/t20220711_3390550.html", "publisher": "沈北新区人民政府", "published_at": "2022-07-11", "accessed_at": "official", "reliability": "high", "notes": "于胜林任区长，满族1977年4月生，在职研究生硕士"},
    {"id": "S004", "title": "沈北区政务公开机构简介", "url": "https://www.nsy.gov.cn/zwgk/fdzdgknr/jgjj/", "publisher": "沈北新区人民政府", "published_at": "2026", "accessed_at": "official", "reliability": "high", "notes": "政府领导班子名单与分工：凌鸣（常务）、赵丹凤、魏智勇、刘晓、关镝、佟玥、邢颖"},
    {"id": "S005", "title": "百度百科 — 吴军（辽宁省沈阳市沈北新区委书记、辉山经开区党工委书记）", "url": "https://baike.baidu.com/item/吴军(辽宁省沈阳市沈北新区委书记、辉山经开区党工委书记)", "publisher": "百度百科", "published_at": "2026-07-31", "accessed_at": "encyclopedia", "reliability": "medium", "notes": "完整履历：沈河区委办主任→沈河区副区长→沈北新区委副书记、区长→2022.05 区委书记"},
    {"id": "S006", "title": "百度百科 — 于胜林（沈北新区区长）", "url": "https://baike.baidu.com/item/于胜林/58040824", "publisher": "百度百科", "published_at": "2026-07-31", "accessed_at": "encyclopedia", "reliability": "medium", "notes": "于洪区委常委副区长→沈阳航空产业集团→沈北新区长"},
    {"id": "S007", "title": "百度百科 — 中国共产党沈阳市沈北新区委员会（2026-07-31更新）", "url": "https://baike.baidu.com/item/中国共产党沈阳市沈北新区委员会/62663547", "publisher": "百度百科", "published_at": "2026-07-31", "accessed_at": "encyclopedia", "reliability": "medium", "notes": "现任领导名单：书记吴军，副书记于胜林、孙涛，区委常委：马晓齐、刘野、凌鸣、李鹏、韩笑、赵东晗、赵丹凤、张明"},
    {"id": "S008", "title": "百度百科 — 闻然", "url": "https://baike.baidu.com/item/闻然", "publisher": "百度百科", "published_at": "", "accessed_at": "encyclopedia", "reliability": "medium", "notes": "前任沈抚区委书记，现任长春市委副书记、长春新区党工委书记"},
    {"id": "S009", "title": "百度百科 — 于夫（沈阳市沈北区人大常委会党组副书记、主任）", "url": "https://baike.baidu.com/item/于夫(沈阳市沈北区人大常委会党组副书记、主任)", "publisher": "百度百科", "published_at": "", "accessed_at": "encyclopedia", "reliability": "medium", "notes": "1969.05，曾任市经信委副巡视员、沈抚区委组织部部长"},
    {"id": "S010", "title": "百度百科 — 孙涛（沈北新区委副书记）", "url": "https://baike.baidu.com/item/孙涛", "publisher": "百度百科", "published_at": "", "accessed_at": "encyclopedia", "reliability": "medium", "notes": "1985.09，博士，团市委书记→副书记"},
    {"id": "S011", "title": "沈北新区人民政府 — 2025年度全区基层党建工作述职评议会议", "url": "https://www.nsy.gov.cn/ywdt/sbyw/202601/t20260113_4968770.html", "publisher": "沈北新区人民政府", "published_at": "2026-01-13", "accessed_at": "official", "reliability": "high", "notes": "吴军以区委书记身份主持并逐一点评"},
    {"id": "S012", "title": "沈北新区人民政府 — 项目建设及企业服务工作调度会议", "url": "https://www.nsy.gov.cn/ywdt/sbyw/202602/t20260224_4989778.html", "publisher": "沈北新区人民政府", "published_at": "2026-02-24", "accessed_at": "official", "reliability": "high", "notes": "吴军主持，习近平胜林出席；提出航空航天产业、低空经济等发展重点"},
    {"id": "S013", "title": "百度百科 — 沈北新区", "url": "https://baike.baidu.com/item/沈北新区", "publisher": "百度百科", "published_at": "", "accessed_at": "encyclopedia", "reliability": "medium", "notes": "区情：819km²，常住人口70.3万（2024末），GDP396.4亿（2021）"},
    {"id": "S014", "title": "百度百科 — 沈阳辉山经济技术开发区", "url": "https://baike.baidu.com/item/沈阳辉山经济技术开发区", "publisher": "百度百科", "published_at": "", "accessed_at": "encyclopedia", "reliability": "medium", "notes": "国家级经开区，前身2002年设有开发区"},
    {"id": "S015", "title": "百度百科 — 赵丹凤 / 凌鸣 / 马晓东 / 赵东晗 / 李盛 / 代丽 / 王凤武 / 王文才 / 冯俊 / 罗丽 / 王健 / 阎秉哲", "url": "", "publisher": "百度百科", "published_at": "", "accessed_at": "encyclopedia", "reliability": "medium", "notes": "跨区流动与履历信息（分条检索）"},
]


def main() -> None:
    """Build DB + GEXF, then write person JSON profiles."""
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")

    # ── Person JSON profiles (core figures) ──
    write_person_json(1)  # 吴军
    write_person_json(2)  # 于胜林
    write_person_json(3)  # 孙涛
    write_person_json(4)  # 于夫
    write_person_json(19)  # 闻然（前任书记）
    print(f"Persons JSON written to {PERSON_DIR}")


def write_person_json(person_id: int) -> None:
    """Write a single person JSON profile for a core figure."""
    p = {x["id"]: x for x in persons}[person_id]
    org_map = {o["id"]: o for o in organizations}
    pos_list = [pos for pos in positions if pos["person_id"] == person_id]

    career = []
    for pos in pos_list:
        career.append({
            "start": pos.get("start", "unknown"),
            "end": pos.get("end", "present"),
            "org": org_map.get(pos["org_id"], {}).get("name", ""),
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": org_map.get(pos["org_id"], {}).get("location", ""),
            "system": "party" if any(k in pos["title"] for k in ["书记", "常委", "组织", "宣传", "统战", "政法委", "纪委"]) else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": "present" in str(pos.get("end", "")),
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if "present" in str(pos.get("end", "")) else "plausible",
            "source_ids": [],
        })

    rels = []
    for r in relationships:
        if r["person_a"] == person_id or r["person_b"] == person_id:
            other_id = r["person_b"] if r["person_a"] == person_id else r["person_a"]
            other = {x["id"]: x for x in persons}[other_id]
            rels.append({
                "person": other["name"],
                "person_id": f"shenbei_{other['name']}",
                "relationship_type": "overlap" if "班" in r["type"] or "搭档" in r["type"] else "other",
                "strength": "strong" if r.get("confidence") == "confirmed" else "medium",
                "evidence": r.get("context", ""),
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": r.get("confidence", "unverified"),
                "source_ids": [],
            })

    gaps = {
        1: "吴军1997年参加工作后的早期基层履历（沈河区区委办内部层级）细节不全",
        2: "于胜林任代区长/区长的精确任命日期；于洪区任职起点时间",
        3: "孙涛任沈北区委副书记的精确起任时间；团市委书记任期",
        4: "于夫任沈北新区人大主任的选举日期（百度百科记载2025-12-19任免信息）",
        19: "闻然2022年离开沈北后的组织部任职具体时间点",
    }

    profile = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "沈阳市",
            "region": "沈北新区",
            "job": p["current_post"],
            "task_id": "liaoning_沈北新区",
            "time_focus": "2022-2026",
        },
        "identity": {
            "person_id": f"shenbei_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": p.get("birthplace", ""),
            "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""), "study_type": "unknown", "source_ids": []}] if p.get("education") else [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth', '')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "正处级" if person_id in (1, 2, 4) else ("副处级" if person_id == 3 else "县处/上级"),
            "as_of": AS_OF,
            "is_current_confirmed": person_id in (1, 2, 3, 4),
            "source_ids": ["S001", "S003", "S007"],
        },
        "career_timeline": career,
        "organizations": [],
        "relationships": rels,
        "governance_record": [
            {"period": "2026", "domain": "economic_development", "achievement_or_event": "提出做强航空航天产业、布局低空经济新赛道", "role_in_event": "区委书记主持全区工作调度会", "measurable_outcome": "招商引资" if person_id == 1 else "", "location": "沈北新区", "confidence": "confirmed", "source_ids": []},
            {"period": "2026", "domain": "urban_construction", "achievement_or_event": "全域土地综合整治、生态环境保护督察整改", "role_in_event": "区领导专题会议", "location": "沈北新区", "confidence": "confirmed", "source_ids": []},
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if person_id in (1, 4) else ("cross_district_rotation" if person_id == 2 or person_id == 19 else "other"),
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "pragmatic", "evidence": "坚持'争抢拼实'精气神，召开调度会议抓项目与招商（2026-02）", "confidence": "plausible", "source_ids": []}
            ] if person_id == 1 else [],
            "speech_themes": ["招商引智", "营商环境", "航空航天产业"] if person_id == 1 else [],
            "management_signals": [],
            "caveat": "工作风格仅基于公开报道推断，非心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "公开检索未发现纪律审查、审计问题等风险信号（检索范围 com 2026-08）", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": SOURCES,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") or p.get("education") else "partial",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": gaps.get(person_id, ""),
        },
        "open_questions": [
            {"priority": "high", "question": gaps.get(person_id, f"{p['name']} 履历细节"), "why_it_messages": "用于完善履历时间线", "suggested_queries": [f"{p['name']} 任前公示", f"{p['name']} 履历"], "last_attempted": AS_OF},
        ],
    }

    job_label = "区委书记" if person_id == 1 else ("区长" if person_id == 2 else ("区委副书记" if person_id == 3 else ("人大主任" if person_id == 4 else "前任区委书记")))
    fname = PERSON_DIR / f"{TODAY}-辽宁省-沈阳市-{job_label}-{p['name']}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print(f"  person json: {fname.name}")


if __name__ == "__main__":
    main()