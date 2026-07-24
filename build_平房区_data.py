#!/usr/bin/env python3
"""Build 哈尔滨市平房区 (Pingfang District, Harbin, Heilongjiang) leadership network data.

Level: 市辖区
Province: 黑龙江省
Parent city: 哈尔滨市
Targets: 区委书记 (Party Secretary), 区长 (District Mayor)
Task ID: heilongjiang_平房区

Research date: 2026-07-24
Official source: http://www.hrbpf.gov.cn/ (哈尔滨市平房区人民政府)

Current status (as of 2026-07-24):
- 区委书记: 于振 — 1970年生，2026年初接替闫红蕾担任区委书记，同时兼任区长至2026年7月
- 区长候选人: 祁彦勇 — 2026年7月以区委副书记、区长候选人身份公开出现，待人大任命
- 区委副书记: 佟晓宇
- 区委常委、组织部部长: 金海燕
- 区委常委、副区长: 王宇
- 副区长: 王让
- 副区长: 车航
- 区人大常委会主任: 温善骋
- 区政协主席: 李杨
- 区人大常委会副主任: 秦朝晖、陈生
- 前任区委书记: 闫红蕾（曾任市委常委、平房区委书记、哈经开区党工委书记至2026年1月）

Key source pages:
- https://www.hrbpf.gov.cn/ (official homepage)
- https://www.hrbpf.gov.cn/pfq/c110066/202607/c01_1136588.shtml (于振 as 区委书记, 2026-07-22)
- https://www.hrbpf.gov.cn/pfq/c110066/202607/c01_1133296.shtml (于振 as 区委书记、区长, 2026-06-30)
- https://www.hrbpf.gov.cn/pfq/c110066/202607/c01_1135061.shtml (祁彦勇 as 区委副书记、区长候选人, 2026-07-11)
- https://www.hrbpf.gov.cn/pfq/c110066/202607/c01_1133305.shtml (金海燕 as 组织部部长, 佟晓宇 as 副书记, 2026-06-30)
- https://www.hrbpf.gov.cn/pfq/c110066/202607/c01_1133293.shtml (金海燕 as 区委常委、组织部部长, 2026-06-29)
- https://www.hrbpf.gov.cn/pfq/c110066/202604/c01_1118068.shtml (于振任人武部党委第一书记, 2026-04-07)
- https://www.hrbpf.gov.cn/pfq/c110066/202607/c01_1136277.shtml (佟晓宇 as 区委副书记, 2026-07-21)
- https://www.hrbpf.gov.cn/pfq/c110066/202606/c01_1131687.shtml (王让、王宇、秦朝晖 出席活动, 2026-06-22)
- https://www.hrbpf.gov.cn/pfq/c110067/202607/c01_1135780.shtml (车航 as 副区长, 2026-07-17)
- https://www.hrbpf.gov.cn/pfq/c110066/202601/c01_1105262.shtml (温善骋、李杨、佟晓宇、金海燕 etc., 2026-01-28)
- https://www.hrbpf.gov.cn/pfq/c110066/202601/c01_1099912.shtml (闫红蕾 as 市委常委、平房区委书记, 2026-01-05)
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "平房区"

_STAGING_DIR = _SCRIPT_DIR
DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"

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
        "name": "于振",
        "gender": "男",
        "ethnicity": "",
        "birth": "1970年",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平房区委书记、哈经开区党工委副书记、管委会主任、人武部党委第一书记",
        "current_org": "中共哈尔滨市平房区委员会",
        "source": "https://www.hrbpf.gov.cn/pfq/c110066/202607/c01_1133296.shtml (区委书记、区长身份) + https://www.hrbpf.gov.cn/pfq/c110066/202604/c01_1118068.shtml (人武部党委第一书记) + https://www.hrbpf.gov.cn/pfq/c110066/202603/c01_1111191.shtml (哈经开区党工委副书记、管委会主任)",
    },
    {
        "id": 2,
        "name": "祁彦勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平房区委副书记、区长候选人",
        "current_org": "中共哈尔滨市平房区委员会 / 哈尔滨市平房区人民政府",
        "source": "https://www.hrbpf.gov.cn/pfq/c110066/202607/c01_1135061.shtml (区委副书记、区长候选人, 2026-07-11)",
    },
    {
        "id": 3,
        "name": "佟晓宇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平房区委副书记、区委党校校长",
        "current_org": "中共哈尔滨市平房区委员会",
        "source": "https://www.hrbpf.gov.cn/pfq/c110066/202607/c01_1136277.shtml (区委副书记, 2026-07-21) + https://www.hrbpf.gov.cn/pfq/c110066/202604/c01_1121127.shtml (区委党校校长, 2026-04-21)",
    },
    {
        "id": 4,
        "name": "金海燕",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平房区委常委、组织部部长",
        "current_org": "中共哈尔滨市平房区委组织部",
        "source": "https://www.hrbpf.gov.cn/pfq/c110066/202607/c01_1133305.shtml (区委常委、组织部部长, 2026-06-30) + https://www.hrbpf.gov.cn/pfq/c110066/202607/c01_1133293.shtml (区委常委、组织部部长, 2026-06-29)",
    },
    {
        "id": 5,
        "name": "王宇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平房区委常委、副区长",
        "current_org": "哈尔滨市平房区人民政府",
        "source": "https://www.hrbpf.gov.cn/pfq/c110066/202607/c01_1136588.shtml (区委常委、副区长参加调研, 2026-07-22) + https://www.hrbpf.gov.cn/pfq/c110066/202606/c01_1131687.shtml (出席活动, 2026-06-22)",
    },
    # ════════════════════════════════════════
    # 区政府领导 (Government)
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "王让",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平房区副区长",
        "current_org": "哈尔滨市平房区人民政府",
        "source": "https://www.hrbpf.gov.cn/pfq/c110066/202606/c01_1131687.shtml (出席活动, 2026-06-22) + https://www.hrbpf.gov.cn/pfq/c110066/202606/c01_1130122.shtml (参加调研, 2026-06-10)",
    },
    {
        "id": 7,
        "name": "车航",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平房区副区长",
        "current_org": "哈尔滨市平房区人民政府",
        "source": "https://www.hrbpf.gov.cn/pfq/c110067/202607/c01_1135780.shtml (区政府副区长, 2026-07-17)",
    },
    {
        "id": 8,
        "name": "王新国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平房区领导",
        "current_org": "哈尔滨市平房区",
        "source": "https://www.hrbpf.gov.cn/pfq/c110066/202606/c01_1131687.shtml (区领导, 2026-06-22)",
    },
    # ════════════════════════════════════════
    # 人大、政协领导 (People's Congress & Political Consultative)
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "温善骋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平房区人大常委会主任",
        "current_org": "哈尔滨市平房区人民代表大会常务委员会",
        "source": "https://www.hrbpf.gov.cn/pfq/c110066/202607/c01_1133305.shtml (区人大常委会主任, 2026-06-30) + https://www.hrbpf.gov.cn/pfq/c110066/202601/c01_1105262.shtml (区人大常委会主任, 2026-01-28)",
    },
    {
        "id": 10,
        "name": "李杨",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平房区政协主席",
        "current_org": "中国人民政治协商会议哈尔滨市平房区委员会",
        "source": "https://www.hrbpf.gov.cn/pfq/c110066/202607/c01_1133305.shtml (区政协主席, 2026-06-30) + https://www.hrbpf.gov.cn/pfq/c110066/202601/c01_1105262.shtml (区政协主席, 2026-01-28)",
    },
    {
        "id": 11,
        "name": "秦朝晖",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平房区人大常委会副主任",
        "current_org": "哈尔滨市平房区人民代表大会常务委员会",
        "source": "https://www.hrbpf.gov.cn/pfq/c110067/202607/c01_1135780.shtml (区人大常委会副主任, 2026-07-17) + https://www.hrbpf.gov.cn/pfq/c110066/202606/c01_1131687.shtml (出席活动, 2026-06-22)",
    },
    {
        "id": 12,
        "name": "陈生",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平房区人大常委会副主任",
        "current_org": "哈尔滨市平房区人民代表大会常务委员会",
        "source": "https://www.hrbpf.gov.cn/pfq/c110067/202607/c01_1135780.shtml (区人大常委会副主任, 2026-07-17)",
    },
    # ════════════════════════════════════════
    # 前任领导 (Predecessor)
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "闫红蕾",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.hrbpf.gov.cn/pfq/c110066/202601/c01_1099912.shtml (市委常委、平房区委书记、哈经开区党工委书记, 2026-01-05) + https://www.hrbpf.gov.cn/pfq/c110066/202601/c01_1100499.shtml (主持区委十二届八次全会, 2026-01-08) + https://www.hrbpf.gov.cn/pfq/c110066/202512/c01_1098988.shtml (此前的最后报道, 2025-12-31)",
    },
    # ════════════════════════════════════════
    # 其他重要人物 (Other Key Figures)
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "刘广军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "哈尔滨市平房区",
        "source": "https://www.hrbpf.gov.cn/pfq/c110066/202601/c01_1105262.shtml (在主席台就座, 2026-01-28)",
    },
    {
        "id": 15,
        "name": "任文霞",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "哈尔滨市平房区",
        "source": "https://www.hrbpf.gov.cn/pfq/c110066/202601/c01_1105262.shtml (在主席台就座, 2026-01-28)",
    },
    {
        "id": 16,
        "name": "孙强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "哈尔滨市平房区",
        "source": "https://www.hrbpf.gov.cn/pfq/c110066/202601/c01_1105262.shtml (在主席台就座, 2026-01-28)",
    },
    {
        "id": 17,
        "name": "孙玉彬",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平房区人民检察院检察长",
        "current_org": "哈尔滨市平房区人民检察院",
        "source": "https://www.hrbpf.gov.cn/pfq/c110067/202607/c01_1135780.shtml (区人民检察院检察长, 2026-07-17) + https://www.hrbpf.gov.cn/pfq/c110066/202601/c01_1105262.shtml (在主席台就座, 2026-01-28)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共哈尔滨市平房区委员会", "type": "党委", "level": "正处级", "parent": "中共哈尔滨市委员会", "location": "哈尔滨市平房区"},
    {"id": 2, "name": "哈尔滨市平房区人民政府", "type": "政府", "level": "正处级", "parent": "哈尔滨市人民政府", "location": "哈尔滨市平房区"},
    {"id": 3, "name": "中共哈尔滨市平房区委组织部", "type": "党委", "level": "正科级", "parent": "中共哈尔滨市平房区委员会", "location": "哈尔滨市平房区"},
    {"id": 4, "name": "哈尔滨市平房区人民代表大会常务委员会", "type": "人大", "level": "正处级", "parent": "哈尔滨市人民代表大会常务委员会", "location": "哈尔滨市平房区"},
    {"id": 5, "name": "中国人民政治协商会议哈尔滨市平房区委员会", "type": "政协", "level": "正处级", "parent": "中国人民政治协商会议哈尔滨市委员会", "location": "哈尔滨市平房区"},
    {"id": 6, "name": "哈尔滨市平房区人民检察院", "type": "政府", "level": "副处级", "parent": "哈尔滨市人民检察院", "location": "哈尔滨市平房区"},
    {"id": 7, "name": "哈尔滨市平房区人民武装部", "type": "政府", "level": "正处级", "parent": "哈尔滨警备区", "location": "哈尔滨市平房区"},
    {"id": 8, "name": "哈尔滨经济技术开发区（哈经开区）", "type": "开发区", "level": "国家级", "parent": "哈尔滨市人民政府", "location": "哈尔滨市平房区"},
    {"id": 9, "name": "中共哈尔滨市委", "type": "党委", "level": "副省级", "parent": "中共黑龙江省委", "location": "哈尔滨市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 于振 — 区委书记、人武部党委第一书记（原兼区长至2026年7月）
    {"person_id": 1, "org_id": 1, "title": "平房区委书记", "start_date": "2026年初", "end_date": "present", "rank": "正处级", "note": "接替闫红蕾担任区委书记"},
    {"person_id": 1, "org_id": 2, "title": "平房区区长", "start_date": "", "end_date": "2026年7月", "rank": "正处级", "note": "党政一肩挑至2026年7月，此后交班给祁彦勇"},
    {"person_id": 1, "org_id": 7, "title": "人武部党委第一书记", "start_date": "2026年4月", "end_date": "present", "rank": "正处级", "note": "2026年4月7日任职大会宣布"},
    {"person_id": 1, "org_id": 8, "title": "哈经开区党工委副书记、管委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "平房区与哈经开区一体化运行"},
    # 祁彦勇 — 区长候选人
    {"person_id": 2, "org_id": 1, "title": "平房区委副书记", "start_date": "2026年7月", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "平房区区长候选人", "start_date": "2026年7月", "end_date": "present", "rank": "正处级", "note": "待区人大任命"},
    # 佟晓宇 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "平房区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼任区委党校校长"},
    # 金海燕 — 组织部部长
    {"person_id": 4, "org_id": 3, "title": "平房区委组织部长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王宇 — 区委常委、副区长
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王让 — 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 车航 — 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 温善骋 — 人大常委会主任
    {"person_id": 9, "org_id": 4, "title": "平房区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 李杨 — 政协主席
    {"person_id": 10, "org_id": 5, "title": "平房区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 秦朝晖 — 人大常委会副主任
    {"person_id": 11, "org_id": 4, "title": "平房区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈生 — 人大常委会副主任
    {"person_id": 12, "org_id": 4, "title": "平房区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 闫红蕾 — 前任区委书记
    {"person_id": 13, "org_id": 1, "title": "平房区委书记", "start_date": "", "end_date": "2026年1月", "rank": "正处级", "note": "同时担任哈经开区党工委书记；2026年1月初最后一次以书记名义主持常委会"},
    {"person_id": 13, "org_id": 9, "title": "哈尔滨市委常委", "start_date": "", "end_date": "2026年1月", "rank": "副省级城市副职", "note": "兼任平房区委书记期间"},
    # 孙玉彬 — 检察长
    {"person_id": 17, "org_id": 6, "title": "平房区人民检察院检察长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 于振与祁彦勇 — 区委书记与区长候选人
    {"person_a": 1, "person_b": 2, "type": "上下级", "context": "区委书记—区长候选人（交接过渡期）", "overlap_org": "平房区委常委会", "overlap_period": "2026年7月", "source": "official site", "confidence": "confirmed"},
    # 于振与佟晓宇 — 区委书记与副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记—区委副书记", "overlap_org": "平房区委常委会", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    # 于振与金海燕 — 区委书记与组织部长
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记—组织部长", "overlap_org": "平房区委常委会", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    # 于振与王宇 — 区委书记与区委常委、副区长
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记—区委常委、副区长", "overlap_org": "平房区委常委会", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    # 于振与各副区长
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区长—副区长", "overlap_org": "平房区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区长—副区长", "overlap_org": "平房区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    # 闫红蕾与于振 — 前后任区委书记
    {"person_a": 13, "person_b": 1, "type": "前任继任", "context": "前后任区委书记；于振原在闫红蕾领导下任区长", "overlap_org": "平房区委常委会", "overlap_period": "2025年-2026年1月", "source": "official site", "confidence": "confirmed"},
    # 于振与区人大、政协领导
    {"person_a": 1, "person_b": 9, "type": "同僚", "context": "区委书记—人大常委会主任", "overlap_org": "平房区", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "同僚", "context": "区委书记—政协主席", "overlap_org": "平房区", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    # 同级班子成员关系
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "同在区政府领导班子", "overlap_org": "平房区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "同在区政府领导班子", "overlap_org": "平房区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "同在区政府领导班子", "overlap_org": "平房区人民政府", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    # 人大政协之间
    {"person_a": 9, "person_b": 10, "type": "同僚", "context": "人大主任—政协主席", "overlap_org": "平房区", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    {"person_a": 9, "person_b": 11, "type": "上下级", "context": "人大主任—副主任", "overlap_org": "平房区人大常委会", "overlap_period": "2026年", "source": "official site", "confidence": "confirmed"},
    # 祁彦勇与佟晓宇 — 两位副书记
    {"person_a": 2, "person_b": 3, "type": "同僚", "context": "同为区委副书记", "overlap_org": "平房区委常委会", "overlap_period": "2026年7月", "source": "official site", "confidence": "confirmed"},
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
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
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons)}")
    print(f"Orgs: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
