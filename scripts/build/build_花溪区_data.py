#!/usr/bin/env python3
"""Build script for 花溪区 (Huaxi District, Guiyang, Guizhou) leadership network.

Generated: 2026-07-23
Level: 市辖区
Province: 贵州省
Parent City: 贵阳市
Targets: 区委书记 & 区长

Research Summary:
  Current officeholders confirmed via official Huaxi government website news articles
  (www.huaxi.gov.cn) dated 2026-07-23:
    - 区委书记: 蒋芳菊 (also 经开区党工委书记, 文创区党工委书记)
    - 区长: 申飞勇 (区委副书记、区长)

Sources:
  - https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652321.html (蒋芳菊 role confirmation)
  - https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652319.html (申飞勇 role confirmation)
  - https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652320.html (文创区党工委会议)
  - https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260721_90642853.html (人大常委会)
"""

import sys
from pathlib import Path

# Ensure gov_relation package is importable
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "蒋芳菊",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "经开区党工委书记、花溪区委书记、文创区党工委书记",
        "current_org": "中共贵阳市花溪区委员会",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652321.html (confirmed as 经开区党工委书记、花溪区委书记)",
    },
    {
        "id": 2,
        "name": "申飞勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区委副书记、区长",
        "current_org": "花溪区人民政府",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652319.html (confirmed as 区委副书记、区长)",
    },
    # ── District Leaders ──
    {
        "id": 3,
        "name": "邱波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区领导",
        "current_org": "花溪区人民政府",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652319.html",
    },
    {
        "id": 4,
        "name": "赵福春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区领导",
        "current_org": "花溪区人民政府",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652319.html",
    },
    {
        "id": 5,
        "name": "王纵横",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区领导",
        "current_org": "花溪区人民政府",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652319.html",
    },
    {
        "id": 6,
        "name": "岑励",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区领导",
        "current_org": "花溪区人民政府",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652319.html",
    },
    {
        "id": 7,
        "name": "罗军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区领导",
        "current_org": "花溪区人民政府",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652321.html (mentioned as 经开区、花溪区领导)",
    },
    {
        "id": 8,
        "name": "王强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区领导",
        "current_org": "花溪区人民政府",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652319.html",
    },
    {
        "id": 9,
        "name": "邓建华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "经开区、花溪区领导",
        "current_org": "花溪区人民政府",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652321.html",
    },
    # ── People's Congress ──
    {
        "id": 10,
        "name": "秦建军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区人大常委会党组书记、主任",
        "current_org": "花溪区人大常委会",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260721_90642853.html",
    },
    # ── CPPCC ──
    {
        "id": 11,
        "name": "禄竹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区政协党组书记、主席",
        "current_org": "花溪区政协",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652318.html",
    },
    # ── Deputy Leaders of People's Congress ──
    {
        "id": 12,
        "name": "李智",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区人大常委会党组副书记、副主任",
        "current_org": "花溪区人大常委会",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260721_90642853.html",
    },
    {
        "id": 13,
        "name": "瞿六亿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区人大常委会党组成员、副主任",
        "current_org": "花溪区人大常委会",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260721_90642853.html",
    },
    {
        "id": 14,
        "name": "赵福兰",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区人大常委会党组成员、副主任",
        "current_org": "花溪区人大常委会",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260721_90642853.html",
    },
    {
        "id": 15,
        "name": "简秀华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区人大常委会党组成员、副主任",
        "current_org": "花溪区人大常委会",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260721_90642853.html",
    },
    {
        "id": 16,
        "name": "王效宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区人大常委会党组成员、副主任",
        "current_org": "花溪区人大常委会",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260721_90642853.html",
    },
    # ── CPPCC Deputy Leaders ──
    {
        "id": 17,
        "name": "彭志伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区政协副主席",
        "current_org": "花溪区政协",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652318.html",
    },
    {
        "id": 18,
        "name": "危大勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区政协副主席",
        "current_org": "花溪区政协",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652318.html",
    },
    {
        "id": 19,
        "name": "李亦然",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区政协副主席",
        "current_org": "花溪区政协",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652318.html",
    },
    {
        "id": 20,
        "name": "黄兴翠",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区政协副主席",
        "current_org": "花溪区政协",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652318.html",
    },
    {
        "id": 21,
        "name": "徐国霞",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区政协副主席",
        "current_org": "花溪区政协",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652318.html",
    },
    {
        "id": 22,
        "name": "黄亚军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪区政协副主席",
        "current_org": "花溪区政协",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652318.html",
    },
    # ──文创区 ──
    {
        "id": 23,
        "name": "宋显胤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "花溪文创区党工委副书记、管委会主任",
        "current_org": "花溪文创区",
        "source": "https://www.huaxi.gov.cn/xwzx/hxyw/202607/t20260723_90652320.html",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共贵阳市花溪区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共贵阳市委",
        "location": "贵州省贵阳市花溪区",
    },
    {
        "id": 2,
        "name": "花溪区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "贵阳市人民政府",
        "location": "贵州省贵阳市花溪区",
    },
    {
        "id": 3,
        "name": "贵阳经济技术开发区党工委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共贵阳市委",
        "location": "贵州省贵阳市花溪区",
    },
    {
        "id": 4,
        "name": "花溪文创区党工委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共贵阳市委",
        "location": "贵州省贵阳市花溪区",
    },
    {
        "id": 5,
        "name": "花溪区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "花溪区",
        "location": "贵州省贵阳市花溪区",
    },
    {
        "id": 6,
        "name": "花溪区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "花溪区",
        "location": "贵州省贵阳市花溪区",
    },
]

POSITIONS = [
    # 蒋芳菊 - top leader holding multiple roles
    {"person_id": 1, "org_id": 1, "title": "花溪区委书记", "start": "", "end": "present", "rank": "正县处级", "note": "official source: 2026-07-23 news"},
    {"person_id": 1, "org_id": 3, "title": "经开区党工委书记", "start": "", "end": "present", "rank": "", "note": "concurrent role"},
    {"person_id": 1, "org_id": 4, "title": "文创区党工委书记", "start": "", "end": "present", "rank": "", "note": "concurrent role"},

    # 申飞勇 - district mayor
    {"person_id": 2, "org_id": 1, "title": "花溪区委副书记", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "花溪区区长", "start": "", "end": "present", "rank": "正县处级", "note": ""},

    # District government leaders
    {"person_id": 3, "org_id": 2, "title": "花溪区领导", "start": "", "end": "present", "rank": "", "note": "区政府党组成员/副区长之一"},
    {"person_id": 4, "org_id": 2, "title": "花溪区领导", "start": "", "end": "present", "rank": "", "note": "区政府党组成员/副区长之一"},
    {"person_id": 5, "org_id": 2, "title": "花溪区领导", "start": "", "end": "present", "rank": "", "note": "区政府党组成员/副区长之一"},
    {"person_id": 6, "org_id": 2, "title": "花溪区领导", "start": "", "end": "present", "rank": "", "note": "区政府党组成员/副区长之一"},
    {"person_id": 7, "org_id": 2, "title": "花溪区领导", "start": "", "end": "present", "rank": "", "note": "区政府党组成员/副区长之一"},
    {"person_id": 8, "org_id": 2, "title": "花溪区领导", "start": "", "end": "present", "rank": "", "note": "区政府党组成员/副区长之一"},
    {"person_id": 9, "org_id": 2, "title": "经开区、花溪区领导", "start": "", "end": "present", "rank": "", "note": "经开区/花溪区双重职务"},

    # People's Congress
    {"person_id": 10, "org_id": 5, "title": "花溪区人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正县处级", "note": ""},
    {"person_id": 12, "org_id": 5, "title": "花溪区人大常委会党组副书记、副主任", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 13, "org_id": 5, "title": "花溪区人大常委会党组成员、副主任", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 14, "org_id": 5, "title": "花溪区人大常委会党组成员、副主任", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 15, "org_id": 5, "title": "花溪区人大常委会党组成员、副主任", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 16, "org_id": 5, "title": "花溪区人大常委会党组成员、副主任", "start": "", "end": "present", "rank": "副县处级", "note": ""},

    # CPPCC
    {"person_id": 11, "org_id": 6, "title": "花溪区政协党组书记、主席", "start": "", "end": "present", "rank": "正县处级", "note": ""},
    {"person_id": 17, "org_id": 6, "title": "花溪区政协副主席", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 18, "org_id": 6, "title": "花溪区政协副主席", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 19, "org_id": 6, "title": "花溪区政协副主席", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 20, "org_id": 6, "title": "花溪区政协副主席", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 21, "org_id": 6, "title": "花溪区政协副主席", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 22, "org_id": 6, "title": "花溪区政协副主席", "start": "", "end": "present", "rank": "副县处级", "note": ""},

    # 文创区
    {"person_id": 23, "org_id": 4, "title": "花溪文创区党工委副书记、管委会主任", "start": "", "end": "present", "rank": "", "note": ""},
]

RELATIONSHIPS = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记-区长搭档，共同主持花溪区委、区政府工作",
        "overlap_org": "花溪区",
        "overlap_period": "2026-07（当前）",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "区委书记和区领导，共同参与生态环保督察整改工作",
        "overlap_org": "花溪区",
        "overlap_period": "2026-07（当前）",
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "区委书记和区领导，共同参与生态环保督察整改工作",
        "overlap_org": "花溪区/经开区",
        "overlap_period": "2026-07（当前）",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区长与区政府领导成员",
        "overlap_org": "花溪区人民政府",
        "overlap_period": "2026-07（当前）",
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区长与区政府领导成员",
        "overlap_org": "花溪区人民政府",
        "overlap_period": "2026-07（当前）",
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区长与区政府领导成员",
        "overlap_org": "花溪区人民政府",
        "overlap_period": "2026-07（当前）",
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区长与区政府领导成员",
        "overlap_org": "花溪区人民政府",
        "overlap_period": "2026-07（当前）",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "区长与区政府领导成员",
        "overlap_org": "花溪区人民政府",
        "overlap_period": "2026-07（当前）",
    },
    {
        "person_a": 1,
        "person_b": 23,
        "type": "superior_subordinate",
        "context": "文创区党工委书记与副书记、管委会主任",
        "overlap_org": "花溪文创区",
        "overlap_period": "2026-07（当前）",
    },
]

# fmt: on

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "花溪区_network.db"
GEXF_PATH = STAGING / "花溪区_network.gexf"


def main() -> None:
    run_build(
        slug="花溪区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )


if __name__ == "__main__":
    main()
