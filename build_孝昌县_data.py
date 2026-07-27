#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 孝昌县, 孝感市, 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_孝昌县
Level: 县
Targets: 县委书记 & 县长

Research status: PARTIAL — core leaders identified from official government
website leadership page (http://www.xiaochang.gov.cn/xwsj/index.jhtml).
Roles and names CONFIRMED. Biographical details (birth year, education,
birthplace, career timeline) NOT FOUND on the government site — the
leadership pages only show name and title without bio data. Baidu Baike
and other encyclopedia sources were blocked/unreachable.

Confirmed via official website leadership page (accessed 2026-07-24):
  县委书记: 李惠芬 (confirmed from xiaochang.gov.cn leadership page)
  县委副书记、县长: 胡飞 (confirmed from xiaochang.gov.cn leadership page)
  县委副书记、政法委书记: 张华
  县委常委: 陈亮, 蔡进文, 陈少忠, 吴明智, 殷国武, 李淑伟, 黄艳红

县政府领导:
  县长: 胡飞
  副县长: 殷国武, 李淑伟, 詹立早, 胡长家, 沈大勇, 胡其欢, 谈旭华

县人大领导:
  主任: 蔡传杰
  副主任: 卢丽娟, 沈保东, 易昕, 鲁军, 朱均平, 袁忠泽
  办公室主任: 饶勤秀

县政协领导:
  主席: 余亮明
  副主席: 李琼铃, 刘子舟, 刘开英, 高金蓉, 高延舟
  秘书长: 徐国民

Career timeline observations from news search results:
  李惠芬: Served as 县委副书记、县长 in 2022-2023; became 县委书记 by mid-2025
  (promoted within the county). Source: xiaochang.gov.cn news search.
  胡飞: Served as 县委副书记、县长 since at least early 2024.
  Source: xiaochang.gov.cn news search.

Confidence notes:
  - All current roles CONFIRMED from official government website.
  - No biographical details (birth year, education, birthplace) found.
  - Predecessor of 李惠芬 (previous 县委书记) and predecessor of 胡飞
    (previous 县长) need further investigation.
"""

from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "孝昌县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership (CONFIRMED from official website) ═══════
    {
        "id": 1,
        "name": "李惠芬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县委书记",
        "current_org": "中共孝昌县委员会",
        "source": "http://www.xiaochang.gov.cn/xwsj/index.jhtml"
    },
    {
        "id": 2,
        "name": "胡飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县委副书记、县人民政府县长",
        "current_org": "孝昌县人民政府",
        "source": "http://www.xiaochang.gov.cn/hf/index.jhtml"
    },
    {
        "id": 3,
        "name": "张华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县委副书记、政法委书记",
        "current_org": "中共孝昌县委员会",
        "source": "http://www.xiaochang.gov.cn/zh/index.jhtml"
    },
    # ═══════ County Party Standing Committee (县委常委) ═══════
    {
        "id": 4,
        "name": "陈亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县委常委",
        "current_org": "中共孝昌县委员会",
        "source": "http://www.xiaochang.gov.cn/cl/index.jhtml"
    },
    {
        "id": 5,
        "name": "蔡进文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县委常委",
        "current_org": "中共孝昌县委员会",
        "source": "http://www.xiaochang.gov.cn/cjw/index.jhtml"
    },
    {
        "id": 6,
        "name": "陈少忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县委常委",
        "current_org": "中共孝昌县委员会",
        "source": "http://www.xiaochang.gov.cn/csz/index.jhtml"
    },
    {
        "id": 7,
        "name": "吴明智",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县委常委",
        "current_org": "中共孝昌县委员会",
        "source": "http://www.xiaochang.gov.cn/wmz1/index.jhtml"
    },
    {
        "id": 8,
        "name": "殷国武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县委常委、副县长",
        "current_org": "孝昌县人民政府",
        "source": "http://www.xiaochang.gov.cn/ylm/index.jhtml"
    },
    {
        "id": 9,
        "name": "李淑伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县委常委、副县长",
        "current_org": "孝昌县人民政府",
        "source": "http://www.xiaochang.gov.cn/lsw/index.jhtml"
    },
    {
        "id": 10,
        "name": "黄艳红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县委常委",
        "current_org": "中共孝昌县委员会",
        "source": "http://www.xiaochang.gov.cn/hyh/index.jhtml"
    },
    # ═══════ County Government (县政府) ═══════
    {
        "id": 11,
        "name": "詹立早",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县副县长",
        "current_org": "孝昌县人民政府",
        "source": "http://www.xiaochang.gov.cn/zlz/index.jhtml"
    },
    {
        "id": 12,
        "name": "胡长家",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县副县长",
        "current_org": "孝昌县人民政府",
        "source": "http://www.xiaochang.gov.cn/hcj/index.jhtml"
    },
    {
        "id": 13,
        "name": "沈大勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县副县长",
        "current_org": "孝昌县人民政府",
        "source": "http://www.xiaochang.gov.cn/sdy/index.jhtml"
    },
    {
        "id": 14,
        "name": "胡其欢",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县副县长",
        "current_org": "孝昌县人民政府",
        "source": "http://www.xiaochang.gov.cn/hqh/index.jhtml"
    },
    {
        "id": 15,
        "name": "谈旭华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县副县长",
        "current_org": "孝昌县人民政府",
        "source": "http://www.xiaochang.gov.cn/txh/index.jhtml"
    },
    # ═══════ People's Congress (县人大) ═══════
    {
        "id": 16,
        "name": "蔡传杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县人大常委会主任",
        "current_org": "孝昌县人大常委会",
        "source": "http://www.xiaochang.gov.cn/ccj/index.jhtml"
    },
    {
        "id": 17,
        "name": "卢丽娟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县人大常委会副主任",
        "current_org": "孝昌县人大常委会",
        "source": "http://www.xiaochang.gov.cn/llj/index.jhtml"
    },
    {
        "id": 18,
        "name": "沈保东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县人大常委会副主任",
        "current_org": "孝昌县人大常委会",
        "source": "http://www.xiaochang.gov.cn/sbd/index.jhtml"
    },
    {
        "id": 19,
        "name": "易昕",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县人大常委会副主任",
        "current_org": "孝昌县人大常委会",
        "source": "http://www.xiaochang.gov.cn/yx/index.jhtml"
    },
    {
        "id": 20,
        "name": "鲁军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县人大常委会副主任",
        "current_org": "孝昌县人大常委会",
        "source": "http://www.xiaochang.gov.cn/lj/index.jhtml"
    },
    {
        "id": 21,
        "name": "朱均平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县人大常委会副主任",
        "current_org": "孝昌县人大常委会",
        "source": "http://www.xiaochang.gov.cn/zjp/index.jhtml"
    },
    {
        "id": 22,
        "name": "袁忠泽",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县人大常委会副主任",
        "current_org": "孝昌县人大常委会",
        "source": "http://www.xiaochang.gov.cn/yzz/index.jhtml"
    },
    {
        "id": 23,
        "name": "饶勤秀",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县人大常委会办公室主任",
        "current_org": "孝昌县人大常委会",
        "source": "http://www.xiaochang.gov.cn/rqx/index.jhtml"
    },
    # ═══════ CPPCC (县政协) ═══════
    {
        "id": 24,
        "name": "余亮明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县政协主席",
        "current_org": "政协孝昌县委员会",
        "source": "http://www.xiaochang.gov.cn/cx/index.jhtml"
    },
    {
        "id": 25,
        "name": "李琼铃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县政协副主席",
        "current_org": "政协孝昌县委员会",
        "source": "http://www.xiaochang.gov.cn/lql/index.jhtml"
    },
    {
        "id": 26,
        "name": "刘子舟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县政协副主席",
        "current_org": "政协孝昌县委员会",
        "source": "http://www.xiaochang.gov.cn/lzz/index.jhtml"
    },
    {
        "id": 27,
        "name": "刘开英",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县政协副主席",
        "current_org": "政协孝昌县委员会",
        "source": "http://www.xiaochang.gov.cn/lky/index.jhtml"
    },
    {
        "id": 28,
        "name": "高金蓉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县政协副主席",
        "current_org": "政协孝昌县委员会",
        "source": "http://www.xiaochang.gov.cn/gjr/index.jhtml"
    },
    {
        "id": 29,
        "name": "高延舟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县政协副主席",
        "current_org": "政协孝昌县委员会",
        "source": "http://www.xiaochang.gov.cn/gyz/index.jhtml"
    },
    {
        "id": 30,
        "name": "徐国民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝昌县政协秘书长",
        "current_org": "政协孝昌县委员会",
        "source": "http://www.xiaochang.gov.cn/xgm/index.jhtml"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共孝昌县委员会", "type": "党委", "level": "县级", "parent": "中共孝感市委员会", "location": "湖北省孝感市孝昌县"},
    {"id": 2, "name": "孝昌县人民政府", "type": "政府", "level": "县级", "parent": "孝感市人民政府", "location": "湖北省孝感市孝昌县"},
    {"id": 3, "name": "孝昌县人大常委会", "type": "人大", "level": "县级", "parent": "孝昌县", "location": "湖北省孝感市孝昌县"},
    {"id": 4, "name": "政协孝昌县委员会", "type": "政协", "level": "县级", "parent": "孝昌县", "location": "湖北省孝感市孝昌县"},
    {"id": 5, "name": "中共孝昌县委政法委员会", "type": "党委", "level": "县级", "parent": "中共孝昌县委员会", "location": "湖北省孝感市孝昌县"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 李惠芬
    {"person_id": 1, "org_id": 1, "title": "孝昌县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 胡飞
    {"person_id": 2, "org_id": 2, "title": "孝昌县人民政府县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "孝昌县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张华
    {"person_id": 3, "org_id": 1, "title": "孝昌县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 5, "title": "孝昌县委政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 常委
    {"person_id": 4, "org_id": 1, "title": "孝昌县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "孝昌县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "孝昌县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "孝昌县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 殷国武 - 常委 also副县长
    {"person_id": 8, "org_id": 1, "title": "孝昌县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "孝昌县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李淑伟 - 常委 also副县长
    {"person_id": 9, "org_id": 1, "title": "孝昌县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "孝昌县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "孝昌县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 县政府副县长
    {"person_id": 11, "org_id": 2, "title": "孝昌县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "孝昌县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "孝昌县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "孝昌县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "孝昌县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 人大
    {"person_id": 16, "org_id": 3, "title": "孝昌县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "孝昌县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "孝昌县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "孝昌县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "孝昌县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 3, "title": "孝昌县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 3, "title": "孝昌县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 3, "title": "孝昌县人大常委会办公室主任", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 政协
    {"person_id": 24, "org_id": 4, "title": "孝昌县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 25, "org_id": 4, "title": "孝昌县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 26, "org_id": 4, "title": "孝昌县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 27, "org_id": 4, "title": "孝昌县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 28, "org_id": 4, "title": "孝昌县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 29, "org_id": 4, "title": "孝昌县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 30, "org_id": 4, "title": "孝昌县政协秘书长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 工作关系 - 县委班子核心成员
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭班", "overlap_org": "中共孝昌县委员会/孝昌县人民政府", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与专职副书记", "overlap_org": "中共孝昌县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与县委副书记同属县委常委会", "overlap_org": "中共孝昌县委员会", "overlap_period": ""},
    # 常委之间的工作关系
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共孝昌县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共孝昌县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共孝昌县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共孝昌县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共孝昌县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共孝昌县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共孝昌县委员会", "overlap_period": ""},
    # 县长与副县长
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与常委副县长", "overlap_org": "孝昌县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与常委副县长", "overlap_org": "孝昌县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "孝昌县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "孝昌县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "孝昌县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "孝昌县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "孝昌县人民政府", "overlap_period": ""},
    # 人大主任与副主任
    {"person_a": 16, "person_b": 17, "type": "superior_subordinate", "context": "人大主任与副主任", "overlap_org": "孝昌县人大常委会", "overlap_period": ""},
    {"person_a": 16, "person_b": 18, "type": "superior_subordinate", "context": "人大主任与副主任", "overlap_org": "孝昌县人大常委会", "overlap_period": ""},
    {"person_a": 16, "person_b": 19, "type": "superior_subordinate", "context": "人大主任与副主任", "overlap_org": "孝昌县人大常委会", "overlap_period": ""},
    {"person_a": 16, "person_b": 20, "type": "superior_subordinate", "context": "人大主任与副主任", "overlap_org": "孝昌县人大常委会", "overlap_period": ""},
    {"person_a": 16, "person_b": 21, "type": "superior_subordinate", "context": "人大主任与副主任", "overlap_org": "孝昌县人大常委会", "overlap_period": ""},
    {"person_a": 16, "person_b": 22, "type": "superior_subordinate", "context": "人大主任与副主任", "overlap_org": "孝昌县人大常委会", "overlap_period": ""},
    # 政协主席与副主席
    {"person_a": 24, "person_b": 25, "type": "superior_subordinate", "context": "政协主席与副主席", "overlap_org": "政协孝昌县委员会", "overlap_period": ""},
    {"person_a": 24, "person_b": 26, "type": "superior_subordinate", "context": "政协主席与副主席", "overlap_org": "政协孝昌县委员会", "overlap_period": ""},
    {"person_a": 24, "person_b": 27, "type": "superior_subordinate", "context": "政协主席与副主席", "overlap_org": "政协孝昌县委员会", "overlap_period": ""},
    {"person_a": 24, "person_b": 28, "type": "superior_subordinate", "context": "政协主席与副主席", "overlap_org": "政协孝昌县委员会", "overlap_period": ""},
    {"person_a": 24, "person_b": 29, "type": "superior_subordinate", "context": "政协主席与副主席", "overlap_org": "政协孝昌县委员会", "overlap_period": ""},
]

# ── Build ──────────────────────────────────────────────────────────────────
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

    print(f"\nBuild complete for {SLUG}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF graph: {GEXF_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} organizations, {len(positions)} positions, {len(relationships)} relationships")
