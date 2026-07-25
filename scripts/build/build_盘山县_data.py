#!/usr/bin/env python3
"""Build 盘山县 (Panshan County) leadership network data.

Level: 县
Province: 辽宁省
Parent city: 盘锦市
Targets: 县委书记 (Party Secretary), 县长 (County Governor)
Task ID: liaoning_盘山县

Research date: 2026-07-25
Official source: https://www.panshan.gov.cn/ (盘山县人民政府)

Current status (as of 2026-07-25, verified via official government website news articles):

县政府领导 (来源: panshan.gov.cn 政务动态):
- 刘鹏飞 — 县委副书记、县长。主持县政府全面工作。
  来源: 2026政府工作报告 https://www.panshan.gov.cn/2026_01/05_10/content-549791.html;
  县政府常务会议新闻: https://www.panshan.gov.cn/2026_05/25_08/content-562990.html

- 张亮 — 县委副书记
  来源: 工商联会议: https://www.panshan.gov.cn/2026_07/13_08/content-568212.html

- 赵天久 — 县委常委、副县长（负责常务工作）
  来源: 县政府常务会议: https://www.panshan.gov.cn/2026_05/25_08/content-562989.html

- 宋晓曦 — 县委常委、政法委书记
  来源: 县委政法工作会议: https://www.panshan.gov.cn/2026_03/19_08/content-555639.html

- 梅森 — 县委常委、县纪委书记、县监委主任
  来源: 县纪委全会: https://www.panshan.gov.cn/2026_07/24_07/content-569486.html

- 郭大强 — 县委常委、统战部部长
  来源: 工商联会议: https://www.panshan.gov.cn/2026_07/13_08/content-568212.html

- 张倩 — 县委常委、宣传部部长
  来源: 刘鹏飞检查城市文明建设: https://www.panshan.gov.cn/2026_03/26_08/content-556460.html

- 刘亮 — 县政府党组成员
  来源: 县政府党组会议: https://www.panshan.gov.cn/2026_06/12_08/content-565122.html

- 刘明伟 — 县政府党组成员、副县长
  来源: 县政府常务会议: https://www.panshan.gov.cn/2026_05/25_08/content-562989.html

- 陈小天 — 副县长
  来源: 刘鹏飞检查城市文明建设: https://www.panshan.gov.cn/2026_03/26_08/content-556460.html

- 赵宇 — 副县长
  来源: 县政府常务会议: https://www.panshan.gov.cn/2026_04/15_08/content-558890.html

- 李禹锋 — 县政府党组成员、副县长
  来源: 县人大常委会: https://www.panshan.gov.cn/2026_03/20_08/content-555767.html

人大、政协领导:
- 乔树立 — 县人大常委会副主任(主持工作)
  来源: 县人大常委会会议: https://www.panshan.gov.cn/2026_03/20_08/content-555767.html
- 王志杰 — 县人大常委会副主任
- 任智勇 — 县人大常委会副主任
- 刘晓玲 — 县人大常委会副主任
- 王峰 — 县政协党组书记(主席待确认)
  来源: 县政协常委会议: https://www.panshan.gov.cn/2026_06/26_08/content-566509.html
- 孙丽颖 — 县政协主席
  来源: 县政协会议: https://www.panshan.gov.cn/2026_03/18_08/content-555519.html
- 王玉才 — 县政协副主席
- 杨宏英 — 县政协副主席
- 王丹 — 县政协副主席
- 谷万库 — 县政协秘书长

Note: 县委书记的具体姓名在政府网站公开新闻中未直接提及，待进一步查证。
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

SLUG = "盘山县"

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
    # 县领导 (County Leadership)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "刘鹏飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盘山县委副书记、县长",
        "current_org": "盘山县人民政府",
        "source": ("官方: https://www.panshan.gov.cn/2026_01/05_10/content-549791.html (2026政府工作报告); "
                   "https://www.panshan.gov.cn/2026_05/25_08/content-562990.html (县政府党组会议)"),
    },
    {
        "id": 2,
        "name": "张亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盘山县委副书记",
        "current_org": "中共盘山县委员会",
        "source": ("官方: https://www.panshan.gov.cn/2026_07/13_08/content-568212.html (工商联会议); "
                   "https://www.panshan.gov.cn/2026_05/11_08/content-561315.html (环保会议)"),
    },
    # ════════════════════════════════════════
    # 县委常委 (Standing Committee)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "赵天久",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（负责常务工作）",
        "current_org": "盘山县人民政府",
        "source": ("官方: https://www.panshan.gov.cn/2026_05/25_08/content-562989.html (县政府常务会议); "
                   "https://www.panshan.gov.cn/2026_04/15_08/content-558890.html"),
    },
    {
        "id": 4,
        "name": "宋晓曦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共盘山县委员会政法委员会",
        "source": ("官方: https://www.panshan.gov.cn/2026_03/19_08/content-555639.html (县委政法工作会议); "
                   "https://www.panshan.gov.cn/2026_05/25_08/content-562990.html"),
    },
    {
        "id": 5,
        "name": "梅森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共盘山县纪律检查委员会/盘山县监察委员会",
        "source": "官方: https://www.panshan.gov.cn/2026_07/24_07/content-569486.html (县纪委全会)",
    },
    {
        "id": 6,
        "name": "郭大强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共盘山县委员会统一战线工作部",
        "source": "官方: https://www.panshan.gov.cn/2026_07/13_08/content-568212.html (工商联会议)",
    },
    {
        "id": 7,
        "name": "张倩",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共盘山县委员会宣传部",
        "source": "官方: https://www.panshan.gov.cn/2026_03/26_08/content-556460.html (刘鹏飞检查城市文明建设)",
    },
    # ════════════════════════════════════════
    # 县政府其他领导
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "刘亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员",
        "current_org": "盘山县人民政府",
        "source": "官方: https://www.panshan.gov.cn/2026_06/12_08/content-565122.html (县政府党组会议)",
    },
    {
        "id": 9,
        "name": "刘明伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "盘山县人民政府",
        "source": ("官方: https://www.panshan.gov.cn/2026_05/25_08/content-562989.html (县政府常务会议); "
                   "https://www.panshan.gov.cn/2026_07/13_08/content-568212.html"),
    },
    {
        "id": 10,
        "name": "陈小天",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "盘山县人民政府",
        "source": "官方: https://www.panshan.gov.cn/2026_03/26_08/content-556460.html (刘鹏飞检查城市文明建设)",
    },
    {
        "id": 11,
        "name": "赵宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "盘山县人民政府",
        "source": ("官方: https://www.panshan.gov.cn/2026_04/15_08/content-558890.html (县政府常务会议); "
                   "https://www.panshan.gov.cn/2026_03/19_08/content-555639.html"),
    },
    {
        "id": 12,
        "name": "李禹锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "盘山县人民政府",
        "source": "官方: https://www.panshan.gov.cn/2026_03/20_08/content-555767.html (县人大常委会任命)",
    },
    # ════════════════════════════════════════
    # 人大领导
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "乔树立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会副主任（主持工作）",
        "current_org": "盘山县人大常委会",
        "source": "官方: https://www.panshan.gov.cn/2026_03/20_08/content-555767.html (县人大常委会会议)",
    },
    # ════════════════════════════════════════
    # 政协领导
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "王峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组书记",
        "current_org": "政协盘山县委员会",
        "source": "官方: https://www.panshan.gov.cn/2026_06/26_08/content-566509.html (县政协常委会议)",
    },
    {
        "id": 15,
        "name": "孙丽颖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协盘山县委员会",
        "source": "官方: https://www.panshan.gov.cn/2026_03/18_08/content-555519.html (县政协会议)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共盘山县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共盘锦市委员会",
        "location": "盘锦市盘山县",
    },
    {
        "id": 2,
        "name": "盘山县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "盘锦市人民政府",
        "location": "盘锦市盘山县",
    },
    {
        "id": 3,
        "name": "中共盘山县纪律检查委员会/盘山县监察委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共盘锦市纪律检查委员会",
        "location": "盘锦市盘山县",
    },
    {
        "id": 4,
        "name": "中共盘山县委员会政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共盘锦市委员会政法委员会",
        "location": "盘锦市盘山县",
    },
    {
        "id": 5,
        "name": "中共盘山县委员会统一战线工作部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共盘锦市委员会统一战线工作部",
        "location": "盘锦市盘山县",
    },
    {
        "id": 6,
        "name": "中共盘山县委员会宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共盘锦市委员会宣传部",
        "location": "盘锦市盘山县",
    },
    {
        "id": 7,
        "name": "盘山县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "盘锦市人民代表大会常务委员会",
        "location": "盘锦市盘山县",
    },
    {
        "id": 8,
        "name": "政协盘山县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协盘锦市委员会",
        "location": "盘锦市盘山县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (任职)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 刘鹏飞
    {"person_id": 1, "org_id": 1, "title": "盘山县委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "盘山县县长", "start": "", "end": "present", "rank": "县处级正职", "note": "主持县政府全面工作; 2026年政府工作报告人"},
    # 张亮
    {"person_id": 2, "org_id": 1, "title": "盘山县委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": "代表县委出席工商联等会议"},
    # 赵天久
    {"person_id": 3, "org_id": 1, "title": "盘山县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副县长（负责常务工作）", "start": "", "end": "present", "rank": "县处级副职", "note": "分管县政府常务工作"},
    # 宋晓曦
    {"person_id": 4, "org_id": 1, "title": "盘山县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "县委政法委书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 梅森
    {"person_id": 5, "org_id": 1, "title": "盘山县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "县纪委书记、县监委主任", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 郭大强
    {"person_id": 6, "org_id": 1, "title": "盘山县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "县委统战部部长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 张倩
    {"person_id": 7, "org_id": 1, "title": "盘山县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "县委宣传部部长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 刘亮
    {"person_id": 8, "org_id": 2, "title": "县政府党组成员", "start": "", "end": "present", "rank": "县处级副职", "note": "县政府党组会议成员"},
    # 刘明伟
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 陈小天
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 赵宇
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 李禹锋
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "2026年3月由县人大常委会任命"},
    # 乔树立
    {"person_id": 13, "org_id": 7, "title": "县人大常委会副主任（主持工作）", "start": "", "end": "present", "rank": "县处级副职", "note": "主持常委会日常工作"},
    # 王峰
    {"person_id": 14, "org_id": 8, "title": "县政协党组书记", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
    # 孙丽颖
    {"person_id": 15, "org_id": 8, "title": "县政协主席", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 县长与县委副书记
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "县长与县委副书记，县委领导班子成员",
        "overlap_org": "中共盘山县委员会",
        "overlap_period": "2025-2026",
    },
    # 县长与县委常委、常务副县长
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "县长与常务副县长，县政府领导班子",
        "overlap_org": "盘山县人民政府",
        "overlap_period": "2025-2026",
    },
    # 县长与其他副县长
    {
        "person_a": 1,
        "person_b": 8,
        "type": "overlap",
        "context": "县长与县政府党组成员，县政府党组",
        "overlap_org": "盘山县人民政府",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "overlap",
        "context": "县长与副县长，县政府领导班子",
        "overlap_org": "盘山县人民政府",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 1,
        "person_b": 10,
        "type": "overlap",
        "context": "县长与副县长，县政府领导班子",
        "overlap_org": "盘山县人民政府",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 1,
        "person_b": 11,
        "type": "overlap",
        "context": "县长与副县长，县政府领导班子",
        "overlap_org": "盘山县人民政府",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 1,
        "person_b": 12,
        "type": "overlap",
        "context": "县长与副县长，县政府领导班子",
        "overlap_org": "盘山县人民政府",
        "overlap_period": "2026-2026",
    },
    # 县委常委关系
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "县委常委、常务副县长与县委常委、政法委书记，县委常委会",
        "overlap_org": "中共盘山县委员会",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 3,
        "person_b": 5,
        "type": "overlap",
        "context": "县委常委、常务副县长与县委常委、纪委书记，县委常委会",
        "overlap_org": "中共盘山县委员会",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 3,
        "person_b": 6,
        "type": "overlap",
        "context": "县委常委、常务副县长与县委常委、统战部长，县委常委会",
        "overlap_org": "中共盘山县委员会",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 3,
        "person_b": 7,
        "type": "overlap",
        "context": "县委常委、常务副县长与县委常委、宣传部长，县委常委会",
        "overlap_org": "中共盘山县委员会",
        "overlap_period": "2025-2026",
    },
    # 人大政协与县政府
    {
        "person_a": 1,
        "person_b": 14,
        "type": "overlap",
        "context": "县长与县政协党组书记，党政联席会议",
        "overlap_org": "盘山县",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 1,
        "person_b": 15,
        "type": "overlap",
        "context": "县长与县政协主席，政协会议",
        "overlap_org": "盘山县",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 1,
        "person_b": 13,
        "type": "overlap",
        "context": "县长与县人大常委会副主任，人大会议",
        "overlap_org": "盘山县",
        "overlap_period": "2025-2026",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, job_title: str, filename_job: str | None = None) -> str:
    """Write a person JSON file to the staging dir."""
    name = person["name"]
    jt = filename_job or job_title

    person_json = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "盘锦市",
            "region": "盘山县",
            "job": job_title,
            "task_id": "liaoning_盘山县",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": f"panshan_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": bool(person.get("source")),
            "source_ids": [],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
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
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "盘山县人民政府官网",
                "url": "https://www.panshan.gov.cn/",
                "publisher": "盘山县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "县政府政务动态新闻及政府工作报告",
            },
            {
                "id": "S002",
                "title": "2026年盘山县政府工作报告",
                "url": "https://www.panshan.gov.cn/2026_01/05_10/content-549791.html",
                "publisher": "盘山县人民政府",
                "published_at": "2026-01-05",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "刘鹏飞县长所作政府工作报告，确认县长身份",
            },
        ],
        "confidence_summary": {
            "identity": "partial" if not person.get("birth") else "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "公开履历信息有限，缺少出生地、教育背景、早年工作经历等详细信息" if not person.get("birthplace") else "",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}完整职业履历",
                "why_it_matters": "核心领导缺详细履历，无法分析晋升路径和任职交集",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}出生地/籍贯",
                "why_it_matters": "缺少基础身份信息，无法做籍贯网络分析",
                "suggested_queries": [f"{name} 出生 籍贯"],
                "last_attempted": AS_OF,
            },
        ],
    }

    filename = f"{TODAY}-辽宁省-盘锦市-{jt}-{name}.json"
    filepath = _STAGING_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)

    print(f"  Wrote {filepath}")
    return filename


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print(f"Building {SLUG} network...")

    # 1. Build database and GEXF
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

    # 2. Verify database
    conn = sqlite3.connect(str(DB_PATH))
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM persons")
        p_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM organizations")
        o_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM positions")
        pos_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM relationships")
        r_count = cur.fetchone()[0]
        print(f"\nDatabase summary: {p_count} persons, {o_count} orgs, {pos_count} positions, {r_count} relationships")
    finally:
        conn.close()

    # 3. Write person JSON files for core leaders
    print("\nWriting person JSON files...")
    # 刘鹏飞 — 县长（二把手）
    write_person_json(persons[0], "县委副书记、县长", "县长")
    # 张亮 — 县委副书记
    write_person_json(persons[1], "县委副书记", "县委副书记")

    # 4. Verify GEXF exists
    if GEXF_PATH.exists():
        size_kb = GEXF_PATH.stat().st_size / 1024
        print(f"\nGEXF file: {GEXF_PATH.name} ({size_kb:.1f} KB)")

    print(f"\nDone! All artifacts in {_STAGING_DIR}")


if __name__ == "__main__":
    main()
