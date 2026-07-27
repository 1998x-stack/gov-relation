#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 商州区, 商洛市, 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_商州区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - 商州区人民政府官方网站 (www.shangzhou.gov.cn) — 领导之窗页面确认全体区委领导、区政府领导信息
  - 商州区人民政府官方网站 (www.shangzhou.gov.cn) — 区委十九届十次全会报道（2026年1月24日）
  - 商州区人民政府官方网站 — 陈泽勇调研报道（2025年3月4日等多篇）
  - 商州区人民政府官方网站 — 支朝奇主持区政府常务会议系列报道

Confidence notes:
  - 陈泽勇（区委书记）: 官方领导之窗页面认证，2026年1月区委全会报道明确标注"区委书记陈泽勇主持"，身份确认
  - 支朝奇（区委副书记、区长）: 官方领导之窗页面认证，多次在政府常务会议报道中标注"区长支朝奇主持"
  - 陈泽勇的完整履历（出生年份1973年11月、大学学历已确认，但籍贯、教育背景、早期任职等细节待查）
  - 支朝奇的完整履历（出生1975年10月、省委党校研究生学历已确认，籍贯、教育背景等细节待查）
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

sys.path.insert(0, os.path.abspath(os.path.join(BASE, "..", "..", "..", "..")))

import sqlite3

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "商州区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (区委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 陈泽勇 — 区委书记
    {
        "id": 1,
        "name": "陈泽勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共商洛市商州区委员会",
        "source": "商州区政府官网领导之窗（信息/3741/571641.htm）及区委十九届十次全会报道（2026-01-24）确认"
    },
    # 支朝奇 — 区委副书记、区长
    {
        "id": 2,
        "name": "支朝奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "商洛市商州区人民政府",
        "source": "商州区政府官网领导之窗（信息/3751/571741.htm）确认"
    },
    # 许永山 — 区委副书记（商洛高新区党工委书记、管委会主任兼任）
    {
        "id": 3,
        "name": "许永山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记（兼）",
        "current_org": "商洛高新区（商丹园区）党工委、管委会",
        "source": "区委十九届十次全会报道（2026-01-24）确认"
    },
    # 魏涛 — 区委副书记
    {
        "id": 4,
        "name": "魏涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共商洛市商州区委员会",
        "source": "区委十九届十次全会报道（2026-01-24）确认"
    },
    # 王沛 — 区委常委、组织部部长
    {
        "id": 5,
        "name": "王沛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共商洛市商州区委员会组织部",
        "source": "商州区政府官网领导之窗（信息/3741/571621.htm）确认"
    },
    # 赵新选 — 区委常委、常务副区长
    {
        "id": 6,
        "name": "赵新选",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年5月",
        "birthplace": "",
        "education": "中央党校大学学历（在职本科）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "商洛市商州区人民政府",
        "source": "商州区政府官网领导之窗（信息/3751/571731.htm）及陈泽勇调研报道确认"
    },
    # 顾鹏 — 区委常委、副区长
    {
        "id": 7,
        "name": "顾鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年10月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "商洛市商州区人民政府",
        "source": "商州区政府官网领导之窗（信息/3751/1507401.htm）确认"
    },
    # 杨浩 — 区委常委、区纪委书记、监委会主任
    {
        "id": 8,
        "name": "杨浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年4月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、监委会主任",
        "current_org": "中共商洛市商州区纪律检查委员会、商州区监察委员会",
        "source": "商州区政府官网领导之窗（信息/3741/571591.htm）确认"
    },
    # 高林波 — 区委常委、副区长
    {
        "id": 9,
        "name": "高林波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "",
        "education": "大学本科学历，高级经济师",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "商洛市商州区人民政府",
        "source": "商州区政府官网领导之窗（信息/3751/1507411.htm）确认"
    },
    # 安怡 — 区委常委、统战部部长
    {
        "id": 10,
        "name": "安怡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共商洛市商州区委员会统战部",
        "source": "商州区政府官网领导之窗（信息/3741/571581.htm）确认"
    },
    # 焦丹龙 — 区委常委、宣传部部长
    {
        "id": 11,
        "name": "焦丹龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年9月",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共商洛市商州区委员会宣传部",
        "source": "商州区政府官网领导之窗（信息/3741/571561.htm）确认"
    },
    # 陈新波 — 区委常委、副区长
    {
        "id": 12,
        "name": "陈新波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "商洛市商州区人民政府",
        "source": "商州区政府官网领导之窗（信息/3751/571701.htm）确认"
    },
    # 陈强 — 区委常委、区人武部部长
    {
        "id": 13,
        "name": "陈强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年9月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区人武部部长",
        "current_org": "商洛市商州区人民武装部",
        "source": "商州区政府官网领导之窗（信息/3741/571551.htm）确认"
    },
    # ══════════════════════════════════════════════════════════════════════════
    # Government (区政府) Deputy Mayors not in Standing Committee
    # ══════════════════════════════════════════════════════════════════════════

    # 王莉 — 副区长
    {
        "id": 14,
        "name": "王莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年6月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "商洛市商州区人民政府",
        "source": "商州区政府官网领导之窗（信息/3751/571691.htm）确认"
    },
    # 周军平 — 副区长、商州公安分局局长
    {
        "id": 15,
        "name": "周军平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "陕西洛南",
        "education": "大学学历",
        "party_join": "中共党员（2002年6月入党）",
        "work_start": "1997年7月",
        "current_post": "副区长、商州公安分局局长",
        "current_org": "商洛市商州区人民政府、商洛市公安局商州分局",
        "source": "商州区政府官网领导之窗（信息/3751/571681.htm）确认"
    },
    # 陈丹涛 — 副区长
    {
        "id": 16,
        "name": "陈丹涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年11月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "商洛市商州区人民政府",
        "source": "商州区政府官网领导之窗（信息/3751/571671.htm）确认"
    },
    # 李涛 — 副区长
    {
        "id": 17,
        "name": "李涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "商洛市商州区人民政府",
        "source": "商州区政府官网领导之窗（信息/3751/571661.htm）确认"
    },
    # 张锋山 — 副区长
    {
        "id": 18,
        "name": "张锋山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年8月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "商洛市商州区人民政府",
        "source": "商州区政府官网领导之窗（信息/3751/571521.htm）确认"
    },
    # ══════════════════════════════════════════════════════════════════════════
    # NPC (区人大常委会) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 周建政 — 区人大常委会主任
    {
        "id": 19,
        "name": "周建政",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "商洛市商州区人民代表大会常务委员会",
        "source": "区委十九届十次全会报道（2026-01-24）确认"
    },
    # ══════════════════════════════════════════════════════════════════════════
    # CPPCC (区政协) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 闫争民 — 区政协主席
    {
        "id": 20,
        "name": "闫争民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议商洛市商州区委员会",
        "source": "区委十九届十次全会报道（2026-01-24）确认"
    },
]

organizations_data = [
    # Party committee
    {
        "id": 1,
        "name": "中共商洛市商州区委员会",
        "type": "党委",
        "level": "县处级",
        "location": "商洛市商州区"
    },
    # Government
    {
        "id": 2,
        "name": "商洛市商州区人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "商洛市商州区"
    },
    # Discipline Commission
    {
        "id": 3,
        "name": "中共商洛市商州区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "location": "商洛市商州区"
    },
    # Supervisory Commission
    {
        "id": 4,
        "name": "商州区监察委员会",
        "type": "党委",
        "level": "县处级",
        "location": "商洛市商州区"
    },
    # Organization Department
    {
        "id": 5,
        "name": "中共商洛市商州区委员会组织部",
        "type": "党委",
        "level": "县处级",
        "location": "商洛市商州区"
    },
    # United Front Department
    {
        "id": 6,
        "name": "中共商洛市商州区委员会统战部",
        "type": "党委",
        "level": "县处级",
        "location": "商洛市商州区"
    },
    # Propaganda Department
    {
        "id": 7,
        "name": "中共商洛市商州区委员会宣传部",
        "type": "党委",
        "level": "县处级",
        "location": "商洛市商州区"
    },
    # People's Armed Forces Department
    {
        "id": 8,
        "name": "商洛市商州区人民武装部",
        "type": "事业单位",
        "level": "县处级",
        "location": "商洛市商州区"
    },
    # NPC
    {
        "id": 9,
        "name": "商洛市商州区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "location": "商洛市商州区"
    },
    # CPPCC
    {
        "id": 10,
        "name": "中国人民政治协商会议商洛市商州区委员会",
        "type": "政协",
        "level": "县处级",
        "location": "商洛市商州区"
    },
    # Public Security Bureau
    {
        "id": 11,
        "name": "商洛市公安局商州分局",
        "type": "政府",
        "level": "乡科级",
        "location": "商洛市商州区"
    },
    # High-tech Zone
    {
        "id": 12,
        "name": "商洛高新区（商丹园区）党工委、管委会",
        "type": "开发区",
        "level": "县处级",
        "location": "商洛市商州区"
    },
]

positions_data = [
    # 陈泽勇
    {"id": 1, "person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 支朝奇
    {"id": 2, "person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 许永山
    {"id": 4, "person_id": 3, "org_id": 1, "title": "区委副书记（兼）", "start": "", "end": "present", "source": "区委十九届十次全会报道"},
    {"id": 5, "person_id": 3, "org_id": 12, "title": "党工委书记、管委会主任", "start": "", "end": "present", "source": "区委十九届十次全会报道"},
    # 魏涛
    {"id": 6, "person_id": 4, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "source": "区委十九届十次全会报道"},
    # 王沛
    {"id": 7, "person_id": 5, "org_id": 5, "title": "区委常委、组织部部长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 赵新选
    {"id": 8, "person_id": 6, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    {"id": 9, "person_id": 6, "org_id": 2, "title": "常务副区长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 顾鹏
    {"id": 10, "person_id": 7, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    {"id": 11, "person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 杨浩
    {"id": 12, "person_id": 8, "org_id": 1, "title": "区委常委、区纪委书记", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    {"id": 13, "person_id": 8, "org_id": 4, "title": "监委会主任", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 高林波
    {"id": 14, "person_id": 9, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    {"id": 15, "person_id": 9, "org_id": 2, "title": "副区长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 安怡
    {"id": 16, "person_id": 10, "org_id": 6, "title": "区委常委、统战部部长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 焦丹龙
    {"id": 17, "person_id": 11, "org_id": 7, "title": "区委常委、宣传部部长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 陈新波
    {"id": 18, "person_id": 12, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    {"id": 19, "person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 陈强
    {"id": 20, "person_id": 13, "org_id": 8, "title": "区委常委、区人武部部长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 王莉
    {"id": 21, "person_id": 14, "org_id": 2, "title": "副区长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 周军平
    {"id": 22, "person_id": 15, "org_id": 2, "title": "副区长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    {"id": 23, "person_id": 15, "org_id": 11, "title": "党委书记、局长、督察长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 陈丹涛
    {"id": 24, "person_id": 16, "org_id": 2, "title": "副区长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 李涛
    {"id": 25, "person_id": 17, "org_id": 2, "title": "副区长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 张锋山
    {"id": 26, "person_id": 18, "org_id": 2, "title": "副区长", "start": "", "end": "present", "source": "商州区政府官网领导之窗"},
    # 周建政
    {"id": 27, "person_id": 19, "org_id": 9, "title": "区人大常委会主任", "start": "", "end": "present", "source": "区委十九届十次全会报道"},
    # 闫争民
    {"id": 28, "person_id": 20, "org_id": 10, "title": "区政协主席", "start": "", "end": "present", "source": "区委十九届十次全会报道"},
]

relationships_data = [
    # 陈泽勇 — 支朝奇：党政主要领导搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "区委书记与区长党政正职搭档关系",
        "overlap_org": "中共商洛市商州区委员会",
        "overlap_period": "当前",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 陈泽勇 — 许永山：区委副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "区委书记与副书记（兼）工作关系",
        "overlap_org": "中共商洛市商州区委员会",
        "overlap_period": "当前",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 陈泽勇 — 魏涛：区委副书记
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "区委书记与专职副书记工作关系",
        "overlap_org": "中共商洛市商州区委员会",
        "overlap_period": "当前",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 支朝奇 — 赵新选：区长与常务副区长
    {
        "person_a": 2,
        "person_b": 6,
        "type": "overlap",
        "context": "区长与常务副区长政府工作搭档",
        "overlap_org": "商洛市商州区人民政府",
        "overlap_period": "当前",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 支朝奇 — 周建政：区长与人大主任
    {
        "person_a": 2,
        "person_b": 19,
        "type": "overlap",
        "context": "政府与人大工作关系",
        "overlap_org": "商洛市商州区",
        "overlap_period": "当前",
        "strength": "weak",
        "confidence": "confirmed",
    },
    # 支朝奇 — 闫争民：区长与政协主席
    {
        "person_a": 2,
        "person_b": 20,
        "type": "overlap",
        "context": "政府与政协工作关系",
        "overlap_org": "商洛市商州区",
        "overlap_period": "当前",
        "strength": "weak",
        "confidence": "confirmed",
    },
    # 陈泽勇 — 周建政：区委书记与人大主任
    {
        "person_a": 1,
        "person_b": 19,
        "type": "overlap",
        "context": "区委与人大工作关系（陈泽勇分工中联系区人大工作）",
        "overlap_org": "商洛市商州区",
        "overlap_period": "当前",
        "strength": "weak",
        "confidence": "confirmed",
    },
    # 陈泽勇 — 赵新选：区委书记与常务副区长
    {
        "person_a": 1,
        "person_b": 6,
        "type": "overlap",
        "context": "区委书记与常务副区长（赵新选陪同调研工业经济）",
        "overlap_org": "中共商洛市商州区委员会",
        "overlap_period": "当前",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 周军平 — 赵新选：公安局长与常务副区长（工作关联）
    {
        "person_a": 15,
        "person_b": 6,
        "type": "overlap",
        "context": "周军平分工中协助常务副区长分管消防安全和信访工作",
        "overlap_org": "商洛市商州区人民政府",
        "overlap_period": "当前",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 支朝奇 — 顾鹏：区长与副区长
    {
        "person_a": 2,
        "person_b": 7,
        "type": "overlap",
        "context": "区长与副区长政府班子关系",
        "overlap_org": "商洛市商州区人民政府",
        "overlap_period": "当前",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 支朝奇 — 高林波：区长与副区长
    {
        "person_a": 2,
        "person_b": 9,
        "type": "overlap",
        "context": "区长与副区长政府班子关系",
        "overlap_org": "商洛市商州区人民政府",
        "overlap_period": "当前",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 支朝奇 — 陈新波：区长与副区长
    {
        "person_a": 2,
        "person_b": 12,
        "type": "overlap",
        "context": "区长与副区长政府班子关系",
        "overlap_org": "商洛市商州区人民政府",
        "overlap_period": "当前",
        "strength": "medium",
        "confidence": "confirmed",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"✅ Build complete: {DB_PATH}")
    print(f"✅ Build complete: {GEXF_PATH}")
