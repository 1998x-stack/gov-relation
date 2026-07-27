#!/usr/bin/env python3
"""Build 周口市川汇区 (Zhoukou Chuanhui District) leadership network data.

Level: 市辖区
Province: 河南省
Parent city: 周口市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: henan_川汇区

Research date: 2026-07-24
Official source: https://www.chuanhui.gov.cn/ (川汇区人民政府)

Current status (as of 2026-07-24, verified via government website):
- 区委书记: 刘德君 — 2026年7月现任。多次以区委书记身份调研督导工作
- 区长: 胡友涛 — 2025年8月起任区长。主持区政府全面工作

Confirmed leadership roster (from government documents and news articles):
- 区委书记: 刘德君
- 区委副书记、区长: 胡友涛
- 区委副书记、政法委书记: 张兴龙
- 区委常委、常务副区长: 王晖
- 区委常委、组织部部长: 张燕
- 区委常委、纪委书记、监委主任: 范凯
- 区委常委: 于海涛
- 区委常委: 张剑飞
- 区委常委、宣传部部长、副区长: 张兴龙 (2025年8月时任，后任副书记)
- 区委常委、区政府党组成员: 张朝霞
- 副区长、公安分局: 朱成刚
- 副区长: 杨鑫
- 副区长: 马凯
- 副区长: 赵虹旭
- 区政府党组成员、政府办主任: 魏宏

Key sources:
- 川政办〔2025〕25号 关于调整区政府领导班子成员工作分工的通知 (2025-08-07)
- 川汇区"两优一先"表彰大会 (2026-07-02) — 区长胡友涛出席
- 刘德君暗访调研 (2026-07-23) — 确认区委书记身份
- 区委理论学习中心组 (2026-07-15) — 确认区委常委名单
- 区纪委第一次全体会议 (2026-06-25) — 范凯当选纪委书记
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "川汇区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = datetime.now().strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y%m%d")

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "刘德君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "川汇区委书记",
        "current_org": "中共周口市川汇区委员会",
        "source": ("官方: https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/"
                    "article7bb08a0cfba241489a477a6a52eb1f80.html "
                    "(2026-07-24 刘德君暗访调研)"),
    },
    {
        "id": 2,
        "name": "胡友涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "川汇区委副书记、区长",
        "current_org": "川汇区人民政府",
        "source": ("官方: https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwgk/jcxxgk/zfwj/cz/"
                    "article5f71d9cf87a647e4bdf83712ce96a23b.html "
                    "(川政办〔2025〕25号 区长胡友涛)"),
    },
    {
        "id": 3,
        "name": "张兴龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "川汇区委副书记、政法委书记",
        "current_org": "中共周口市川汇区委员会",
        "source": ("官方: https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/"
                    "article5763bd12f5bd412980c29f3b67ec39b5.html "
                    "(2026-07-02 两优一先表彰大会)"),
    },
    {
        "id": 4,
        "name": "王晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "川汇区委常委、常务副区长",
        "current_org": "川汇区人民政府",
        "source": ("官方: https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwgk/jcxxgk/zfwj/cz/"
                    "article5f71d9cf87a647e4bdf83712ce96a23b.html "
                    "(川政办〔2025〕25号)"),
    },
    {
        "id": 5,
        "name": "张燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "川汇区委常委、组织部部长",
        "current_org": "中共周口市川汇区委员会组织部",
        "source": ("官方: https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/"
                    "article12361f56609a4b2b9c457c6f904eff1c.html "
                    "(2026-07-15 区委理论学习中心组)"),
    },
    {
        "id": 6,
        "name": "范凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "川汇区委常委、纪委书记、监委主任",
        "current_org": "中共周口市川汇区纪律检查委员会",
        "source": ("官方: https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/"
                    "articlef77e547bc2354a17ab3797e2a2973c01.html "
                    "(2026-06-25 纪委第一次全委会 范凯当选纪委书记)"),
    },
    {
        "id": 7,
        "name": "于海涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "川汇区委常委",
        "current_org": "中共周口市川汇区委员会",
        "source": ("官方: https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/"
                    "article12361f56609a4b2b9c457c6f904eff1c.html "
                    "(2026-07-15 区委理论学习中心组)"),
    },
    {
        "id": 8,
        "name": "张剑飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "川汇区委常委",
        "current_org": "中共周口市川汇区委员会",
        "source": ("官方: https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/"
                    "article12361f56609a4b2b9c457c6f904eff1c.html "
                    "(2026-07-15 区委理论学习中心组)"),
    },
    # ════════════════════════════════════════
    # 区政府领导 (District Government)
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "张朝霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "川汇区委常委、区政府党组成员",
        "current_org": "川汇区人民政府",
        "source": ("官方: https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwgk/jcxxgk/zfwj/cz/"
                    "article5f71d9cf87a647e4bdf83712ce96a23b.html "
                    "(川政办〔2025〕25号)"),
    },
    {
        "id": 10,
        "name": "朱成刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "川汇区副区长、市公安局川汇分局局长",
        "current_org": "川汇区人民政府",
        "source": ("官方: https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwgk/jcxxgk/zfwj/cz/"
                    "article5f71d9cf87a647e4bdf83712ce96a23b.html "
                    "(川政办〔2025〕25号)"),
    },
    {
        "id": 11,
        "name": "杨鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "川汇区副区长",
        "current_org": "川汇区人民政府",
        "source": ("官方: https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwgk/jcxxgk/zfwj/cz/"
                    "article5f71d9cf87a647e4bdf83712ce96a23b.html "
                    "(川政办〔2025〕25号)"),
    },
    {
        "id": 12,
        "name": "马凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "川汇区副区长",
        "current_org": "川汇区人民政府",
        "source": ("官方: https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwgk/jcxxgk/zfwj/cz/"
                    "article5f71d9cf87a647e4bdf83712ce96a23b.html "
                    "(川政办〔2025〕25号)"),
    },
    {
        "id": 13,
        "name": "赵虹旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "川汇区副区长",
        "current_org": "川汇区人民政府",
        "source": ("官方: https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwgk/jcxxgk/zfwj/cz/"
                    "article5f71d9cf87a647e4bdf83712ce96a23b.html "
                    "(川政办〔2025〕25号)"),
    },
    {
        "id": 14,
        "name": "魏宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "川汇区政府党组成员、政府办主任",
        "current_org": "川汇区人民政府",
        "source": ("官方: https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwgk/jcxxgk/zfwj/cz/"
                    "article5f71d9cf87a647e4bdf83712ce96a23b.html "
                    "(川政办〔2025〕25号)"),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共周口市川汇区委员会", "type": "党委", "level": "县级", "parent": "中共周口市委", "location": "河南省周口市川汇区"},
    {"id": 2, "name": "川汇区人民政府", "type": "政府", "level": "县级", "parent": "周口市人民政府", "location": "河南省周口市川汇区"},
    {"id": 3, "name": "中共周口市川汇区纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共周口市川汇区委员会", "location": "河南省周口市川汇区"},
    {"id": 4, "name": "中共周口市川汇区委员会组织部", "type": "党委", "level": "县级", "parent": "中共周口市川汇区委员会", "location": "河南省周口市川汇区"},
    {"id": 5, "name": "中共周口市川汇区委员会政法委员会", "type": "党委", "level": "县级", "parent": "中共周口市川汇区委员会", "location": "河南省周口市川汇区"},
    {"id": 6, "name": "周口市公安局川汇分局", "type": "政府", "level": "县级", "parent": "川汇区人民政府", "location": "河南省周口市川汇区"},
    {"id": 7, "name": "中共周口市川汇区委员会宣传部", "type": "党委", "level": "县级", "parent": "中共周口市川汇区委员会", "location": "河南省周口市川汇区"},
    {"id": 8, "name": "周口高新技术产业开发区", "type": "开发区", "level": "县级", "parent": "川汇区人民政府", "location": "河南省周口市川汇区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 刘德君 (区委书记)
    {"person_id": 1, "org_id": 1, "title": "川汇区委书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "2026年7月现任，多次以四不两直方式调研"},
    # 胡友涛 (区长)
    {"person_id": 2, "org_id": 1, "title": "川汇区委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "2025年8月时任区长"},
    {"person_id": 2, "org_id": 2, "title": "川汇区区长", "start_date": "", "end_date": "", "rank": "正县级", "note": "主持区政府全面工作。负责审计方面工作"},
    # 张兴龙 (区委副书记、政法委书记)
    {"person_id": 3, "org_id": 1, "title": "川汇区委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 5, "title": "川汇区委政法委书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "2026年7月兼任（原任宣传部部长、副区长）"},
    # 王晖 (常务副区长)
    {"person_id": 4, "org_id": 1, "title": "川汇区委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "川汇区常务副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责经济运行、发展改革、财政金融等"},
    # 张燕 (组织部长)
    {"person_id": 5, "org_id": 1, "title": "川汇区委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "川汇区委组织部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 范凯 (纪委书记)
    {"person_id": 6, "org_id": 1, "title": "川汇区委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "2026年6月当选"},
    {"person_id": 6, "org_id": 3, "title": "川汇区纪委书记、监委主任", "start_date": "2026-06", "end_date": "", "rank": "副县级", "note": "2026年6月25日区纪委六届一次全会当选"},
    # 于海涛 (区委常委)
    {"person_id": 7, "org_id": 1, "title": "川汇区委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "具体分工待确认"},
    # 张剑飞 (区委常委)
    {"person_id": 8, "org_id": 1, "title": "川汇区委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "具体分工待确认"},
    # 张朝霞 (区委常委、区政府党组成员)
    {"person_id": 9, "org_id": 1, "title": "川汇区委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "川汇区政府党组成员", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责农业农村、乡村振兴"},
    # 朱成刚 (副区长、公安分局)
    {"person_id": 10, "org_id": 2, "title": "川汇区副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责公安、司法、信访、民族宗教"},
    {"person_id": 10, "org_id": 6, "title": "市公安局川汇分局局长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 杨鑫 (副区长)
    {"person_id": 11, "org_id": 2, "title": "川汇区副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责文化旅游、卫生健康、医疗保障"},
    # 马凯 (副区长)
    {"person_id": 12, "org_id": 2, "title": "川汇区副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责城乡建设、城市管理、交通运输等"},
    # 赵虹旭 (副区长)
    {"person_id": 13, "org_id": 2, "title": "川汇区副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责教育体育、民政、市场监管等"},
    # 魏宏 (政府办主任)
    {"person_id": 14, "org_id": 2, "title": "川汇区政府党组成员、政府办主任", "start_date": "", "end_date": "", "rank": "正科级", "note": "协助胡友涛区长负责区政府日常工作"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 书记 ↔ 区长（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长党政工作搭档", "overlap_org": "川汇区", "overlap_period": ""},
    # 书记 ↔ 副书记/政法委书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与区委副书记", "overlap_org": "中共川汇区委", "overlap_period": ""},
    # 区长 ↔ 常务副区长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长与常务副区长工作搭档", "overlap_org": "川汇区政府", "overlap_period": ""},
    # 书记 ↔ 组织部长
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记与组织部长", "overlap_org": "中共川汇区委", "overlap_period": ""},
    # 书记 ↔ 纪委书记
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记与纪委书记", "overlap_org": "中共川汇区委", "overlap_period": ""},
    # 书记 ↔ 于海涛
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记与区委常委", "overlap_org": "中共川汇区委", "overlap_period": ""},
    # 书记 ↔ 张剑飞
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记与区委常委", "overlap_org": "中共川汇区委", "overlap_period": ""},
    # 区长 ↔ 副区长（张朝霞）
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长与区政府党组成员", "overlap_org": "川汇区政府", "overlap_period": ""},
    # 区长 ↔ 副区长（朱成刚）
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区长与副区长（公安）", "overlap_org": "川汇区政府", "overlap_period": ""},
    # 区长 ↔ 副区长（杨鑫）
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长与副区长", "overlap_org": "川汇区政府", "overlap_period": ""},
    # 区长 ↔ 副区长（马凯）
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长与副区长", "overlap_org": "川汇区政府", "overlap_period": ""},
    # 区长 ↔ 副区长（赵虹旭）
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "区长与副区长", "overlap_org": "川汇区政府", "overlap_period": ""},
    # 区长 ↔ 政府办主任
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "区长与政府办主任", "overlap_org": "川汇区政府", "overlap_period": ""},
    # 常务副区长 ↔ 副区长（横向协作）
    {"person_a": 4, "person_b": 12, "type": "同级协作", "context": "常务副区长与副区长（城建）工作协作", "overlap_org": "川汇区政府", "overlap_period": ""},
    # 纪委书记 ↔ 组织部
    {"person_a": 5, "person_b": 6, "type": "同级协作", "context": "组织与纪委在干部监督中协作", "overlap_org": "中共川汇区委", "overlap_period": ""},
    # 副书记 ↔ 常务副区长
    {"person_a": 3, "person_b": 4, "type": "同级协作", "context": "区委副书记与常务副区长工作协作", "overlap_org": "川汇区", "overlap_period": ""},
    # 副书记 ↔ 组织部长
    {"person_a": 3, "person_b": 5, "type": "同级协作", "context": "区委副书记与组织部长在组织工作中协作", "overlap_org": "中共川汇区委", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTER
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "周口市川汇区人民政府办公室关于调整区政府领导班子成员工作分工的通知 川政办〔2025〕25号",
         "url": "https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwgk/jcxxgk/zfwj/cz/article5f71d9cf87a647e4bdf83712ce96a23b.html",
         "publisher": "川汇区人民政府", "published_at": "2025-08-07", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "官方政府领导班子分工文件"},
        {"id": "S002", "title": "刘德君暗访调研党建引领基层高效能治理工作",
         "url": "https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/article7bb08a0cfba241489a477a6a52eb1f80.html",
         "publisher": "云上周口", "published_at": "2026-07-24", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "刘德君以区委书记身份调研"},
        {"id": "S003", "title": "胡友涛夜查基层高效能治理、高层建筑消防安全和物业服务工作",
         "url": "https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/articleda484643751845f2886d3fc609f27196.html",
         "publisher": "云上周口", "published_at": "2026-07-23", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "胡友涛以区长身份带队夜查"},
        {"id": "S004", "title": "川汇区两优一先表彰大会召开",
         "url": "https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/article5763bd12f5bd412980c29f3b67ec39b5.html",
         "publisher": "云上周口", "published_at": "2026-07-02", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "区长胡友涛讲话，张兴龙以区委副书记、政法委书记身份主持"},
        {"id": "S005", "title": "川汇区党建引领基层高效能治理暨安全生产和防汛备汛工作推进会召开",
         "url": "https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/article7961efeb425b46ca8205f6169eb9a542.html",
         "publisher": "云上周口", "published_at": "2026-07-22", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "刘德君主持、胡友涛作安排、张兴龙段晓作工作安排"},
        {"id": "S006", "title": "川汇区：区委理论学习中心组举行集体学习研讨",
         "url": "https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/article12361f56609a4b2b9c457c6f904eff1c.html",
         "publisher": "云上周口", "published_at": "2026-07-16", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "刘德君主持，胡友涛、张兴龙、王晖、张燕、范凯、于海涛、张剑飞、马凯、赵虹旭等参加"},
        {"id": "S007", "title": "中国共产党周口市川汇区第六届纪律检查委员会举行第一次全体会议",
         "url": "https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/articlef77e547bc2354a17ab3797e2a2973c01.html",
         "publisher": "云上周口", "published_at": "2026-06-25", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "范凯当选纪委书记"},
        {"id": "S008", "title": "刘德君带队暗访高层建筑消防安全工作",
         "url": "https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/articledefe96e6f6814569b1f47e1ff8189be6.html",
         "publisher": "云上周口", "published_at": "2026-07-21", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "刘德君以区委书记身份带队暗访，王晖、马凯参加"},
        {"id": "S009", "title": "刘德君调研安全生产、群众身边不正之风和腐败问题集中整治工作",
         "url": "https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/article7492280e1e2b437ba4e4602eedfde4e8.html",
         "publisher": "云上周口", "published_at": "2026-07-19", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "刘德君以区委书记身份调研"},
        {"id": "S010", "title": "川汇区生态环境保护工作会议召开",
         "url": "https://www.chuanhui.gov.cn/sitesources/chq/page_pc/zwyw/jryw/article6619b82149aa454aadd01fbefa28104e.html",
         "publisher": "云上周口", "published_at": "2026-07-22", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "刘德君主持、胡友涛作安排"},
    ]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON GRAPH JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_person_json(person: dict, timeline: list[dict], person_relationships: list[dict],
                     source_register: list[dict]) -> dict:
    """Build a Person Graph JSON v1.0 record."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "周口市",
            "region": "川汇区",
            "job": person.get("current_post", ""),
            "task_id": "henan_川汇区",
            "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": f"chuanhuiqu_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "",
                           "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": person_relationships,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "",
                                         "confidence": "unverified", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": "完整履历（出生年月、早期职业生涯）未公开",
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的出生年月和早期职业生涯",
             "why_it_matters": "完整履历是评估晋升路径和人际关系的基础",
             "suggested_queries": [f"{person['name']} 简历 周口", f"{person['name']} 任前公示",
                                   f"{person['name']} 百度百科"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": f"{person['name']}的出生地和籍贯",
             "why_it_matters": "地域关系是人际关系网络的重要维度",
             "suggested_queries": [f"{person['name']} 出生", f"{person['name']} 籍贯"],
             "last_attempted": AS_OF},
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print("  周口市川汇区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 川汇区政府网站 (chuanhui.gov.cn)")
    print("=" * 60)

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
    print(f"\n✅ 川汇区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 刘德君 (区委书记)
    liu_timeline = [
        {"start": "", "end": "", "org": "中共周口市川汇区委员会", "title": "川汇区委书记",
         "notes": "2026年7月现任，多次以区委书记身份调研督导安全生产、基层治理等工作",
         "confidence": "confirmed", "source_ids": ["S002", "S005", "S006", "S008", "S009"]},
    ]
    liu_relationships = [
        {"person": "胡友涛", "person_id": "chuanhuiqu_胡友涛", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区委书记与区长党政工作搭档",
         "overlap_org": "川汇区", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005", "S006", "S010"]},
        {"person": "张兴龙", "person_id": "chuanhuiqu_张兴龙", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区委书记与区委副书记",
         "overlap_org": "中共川汇区委", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
        {"person": "王晖", "person_id": "chuanhuiqu_王晖", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区委书记与区委常委、常务副区长",
         "overlap_org": "中共川汇区委", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006", "S008"]},
        {"person": "范凯", "person_id": "chuanhuiqu_范凯", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区委书记与纪委书记",
         "overlap_org": "中共川汇区委", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
        {"person": "马凯", "person_id": "chuanhuiqu_马凯", "relationship_type": "overlap",
         "strength": "medium", "evidence": "区委书记与副区长（刘德君暗访消防安全时马凯参加）",
         "overlap_org": "川汇区", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S008"]},
    ]
    liu_json = make_person_json(persons[0], liu_timeline, liu_relationships, source_register)

    # Add governance record for 刘德君
    liu_json["governance_record"] = [
        {"period": "2026-07", "domain": "public_security", "achievement_or_event": "暗访高层建筑消防安全",
         "role_in_event": "区委书记带队暗访", "measurable_outcome": "现场排查隐患、压实责任",
         "location": "川汇区", "confidence": "confirmed", "source_ids": ["S008"]},
        {"period": "2026-07", "domain": "discipline", "achievement_or_event": "调研群众身边不正之风和腐败问题集中整治",
         "role_in_event": "区委书记调研督导", "measurable_outcome": "",
         "location": "川汇区城北街道", "confidence": "confirmed", "source_ids": ["S009"]},
        {"period": "2026-07", "domain": "other", "achievement_or_event": "暗访调研党建引领基层高效能治理",
         "role_in_event": "区委书记以四不两直方式调研", "measurable_outcome": "",
         "location": "川汇区城北街道李楼行政村", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    liu_json["work_style_and_personality"]["public_style_indicators"] = [
        {"trait": "pragmatic", "evidence": "多次以'四不两直'方式暗访调研，直接深入基层了解实情",
         "confidence": "confirmed", "source_ids": ["S002", "S008", "S009"]},
        {"trait": "discipline_oriented", "evidence": "强调安全生产、群众身边不正之风和腐败问题集中整治",
         "confidence": "confirmed", "source_ids": ["S009"]},
    ]
    liu_path = PERSONS_DIR / f"{TODAY}-河南省-周口市-区委书记-刘德君.json"
    with open(liu_path, "w", encoding="utf-8") as f:
        json.dump(liu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {liu_path.name}")

    # 2. 胡友涛 (区长)
    hu_timeline = [
        {"start": "", "end": "", "org": "", "title": "履历缺口",
         "notes": "公开资料未找到胡友涛的早期任职履历",
         "confidence": "unverified", "source_ids": []},
        {"start": "", "end": "", "org": "川汇区人民政府", "title": "川汇区区长",
         "notes": "2025年8月已任区长。主持区政府全面工作",
         "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    hu_relationships = [
        {"person": "刘德君", "person_id": "chuanhuiqu_刘德君", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区长与区委书记党政工作搭档",
         "overlap_org": "川汇区", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005", "S006", "S010"]},
        {"person": "王晖", "person_id": "chuanhuiqu_王晖", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区长与常务副区长工作搭档",
         "overlap_org": "川汇区政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "张兴龙", "person_id": "chuanhuiqu_张兴龙", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区长与区委副书记",
         "overlap_org": "川汇区", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    hu_json = make_person_json(persons[1], hu_timeline, hu_relationships, source_register)

    hu_json["governance_record"] = [
        {"period": "2026-07", "domain": "public_security", "achievement_or_event": "夜查高层建筑消防安全和物业服务工作",
         "role_in_event": "区长带队调研", "measurable_outcome": "",
         "location": "川汇区幸福花开文苑、北辰桂园", "confidence": "confirmed", "source_ids": ["S003"]},
        {"period": "2025-08", "domain": "other", "achievement_or_event": "主持区政府全面工作，牵头审计",
         "role_in_event": "区长，区政府法定代表人", "measurable_outcome": "",
         "location": "川汇区", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    hu_json["work_style_and_personality"]["public_style_indicators"] = [
        {"trait": "pragmatic", "evidence": "带队夜查基层，直接发现问题",
         "confidence": "confirmed", "source_ids": ["S003"]},
        {"trait": "grassroots_oriented", "evidence": "深入住宅小区逐栋逐层察看消防设施",
         "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    hu_path = PERSONS_DIR / f"{TODAY}-河南省-周口市-区长-胡友涛.json"
    with open(hu_path, "w", encoding="utf-8") as f:
        json.dump(hu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {hu_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()
