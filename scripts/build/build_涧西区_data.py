#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 涧西区 (Jianxi District), 洛阳市, 河南省.

Level: 市辖区
Province: 河南省
Parent city: 洛阳市
Targets: 区委书记 (Party Secretary: 谢峰), 区长 (Mayor: 孙论兵)
Task ID: henan_涧西区

Research date: 2026-08-03
Official source: http://www.jxq.gov.cn/ (涧西区人民政府)

Current status (as of 2026-08-03):
- 区委书记: 谢峰 (confirmed via 涧西区人民政府 site, 2026-07-31 and 2026-06-24 party congress)
- 区长: 孙论兵 (confirmed via 涧西区政务公开 - 领导之窗, born 1976.11)

Leadership roster sourced from:
  - 涧西区人民政府: https://www.jxq.gov.cn/ (official site, news+leadership page)
  - 涧西区领导之窗: http://www.jxq.gov.cn/zfxxgk/ldzc (government leadership listing)
  - 洛阳市人民政府: https://www.ly.gov.cn/ (news listing: 涧西区委书记谢峰督导调研)
  - 涧西区第十一次党代会: http://www.jxq.gov.cn/2026/06-26/1069701.html

Party Standing Committee (11th Congress, elected 2026-06-24):
  谢峰、孙论兵、尚江涛、仲家玉、赵晖、张京波、韩静、程欢、刘超、王锐、何鹏、杜利峰、李龙飞

Government leaders (confirmed via gov leadership page + meeting minutes):
  - 孙论兵: 区委副书记、区长，高新区党工委副书记、管委会主任
  - 程欢: 区委常委、常务副区长 (1983.12, 研究生)
  - 王锐: 区委常委、宣传部长，副区长 (1983.09, 工学学士)
  - 周岩: 副区长 (1975.12, 研究生)
  - 胡全超: 副区长、涧西公安分局局长 (1973.09, 大学)
  - 王莎莎: 副区长 (1978.07, 大学)
  - 王鹏杰: 副区长 (1990.06, 研究生)
  - 任钊函: 副区长(挂职) (1984.01, 大学)
  - 陈聪聪: 副区长(挂职) (1986.04, 大学本科)

Detailed career histories before current roles not publicly available from web fetch sources.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "..").resolve()  # tmp/henan_涧西区/../.. = repo root
# Fall back to locate correct root
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_REPO_ROOT / "../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "涧西区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-03"
TODAY = "20260803"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 谢峰 — 区委书记
    {
        "id": 1,
        "name": "谢峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共涧西区委员会",
        "source": "http://www.jxq.gov.cn/ (涧西区人民政府), 2026-07-31新闻; 以及 https://www.ly.gov.cn/ 新闻条目：涧西区委书记、高新区党工委书记谢峰",
    },
    # 2. 孙论兵 — 区长
    {
        "id": 2,
        "name": "孙论兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "涧西区人民政府",
        "source": "http://www.jxq.gov.cn/2025/12-29/1025739.html (涧西区领导之窗 - 孙论兵个人简历)",
    },

    # ════════════════════════════════════════
    # Standing Committee Members (区委常委会)
    # ════════════════════════════════════════

    # 3. 程欢 — 区委常委、常务副区长
    {
        "id": 3,
        "name": "程欢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年12月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "涧西区人民政府",
        "source": "http://www.jxq.gov.cn/2025/12-29/1025738.html (涧西区领导之窗 - 程欢)",
    },
    # 4. 王锐 — 区委常委、宣传部长、副区长
    {
        "id": 4,
        "name": "王锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年9月",
        "birthplace": "",
        "education": "大学，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部长、副区长",
        "current_org": "中共涧西区委员会/涧西区人民政府",
        "source": "http://www.jxq.gov.cn/2025/12-29/1025737.html (涧西区领导之窗 - 王锐)",
    },
    # 5. 尚刚涛 — 区委常委
    {
        "id": 5,
        "name": "尚刚涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共涧西区委员会",
        "source": "http://www.jxq.gov.cn/ (涧西区第十一次党代会主席团名单, 2026-06-24/25)",
    },
    # 6. 仲家玉 — 区委常委
    {
        "id": 6,
        "name": "仲家玉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共涧西区委员会",
        "source": "http://www.jxq.gov.cn/ (涧西区第十一次党代会主席团名单, 2026-06-24/25)",
    },
    # 7. 赵晖 — 区委常委
    {
        "id": 7,
        "name": "赵晖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共涧西区委员会",
        "source": "http://www.jxq.gov.cn/ (涧西区第十一次党代会主席团名单, 2026-06-24/25)",
    },
    # 8. 张京波 — 区委常委
    {
        "id": 8,
        "name": "张京波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共涧西区委员会",
        "source": "http://www.jxq.gov.cn/ (涧西区第十一次党代会主席团名单, 2026-06-24/25)",
    },
    # 9. 韩静 — 区委常委
    {
        "id": 9,
        "name": "韩静",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共涧西区委员会",
        "source": "http://www.jxq.gov.cn/ (涧西区第十一次党代会主席团名单, 2026-06-24/25)",
    },
    # 10. 刘超 — 区委常委
    {
        "id": 10,
        "name": "刘超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共涧西区委员会",
        "source": "http://www.jxq.gov.cn/ (涧西区第十一次党代会闭幕主席团名单, 2026-06-25)",
    },
    # 11. 何鹏 — 区委常委
    {
        "id": 11,
        "name": "何鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共涧西区委员会",
        "source": "http://www.jxq.gov.cn/ (涧西区第十一次党代会闭幕主席团名单, 2026-06-25)",
    },
    # 12. 杜利峰 — 区委常委
    {
        "id": 12,
        "name": "杜利峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共涧西区委员会",
        "source": "http://www.jxq.gov.cn/ (涧西区第十一次党代会闭幕主席团名单, 2026-06-25)",
    },
    # 13. 李龙飞 — 区委常委
    {
        "id": 13,
        "name": "李龙飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共涧西区委员会",
        "source": "http://www.jxq.gov.cn/ (涧西区第十一次党代会闭幕主席团名单, 2026-06-25)",
    },

    # ════════════════════════════════════════
    # Government Deputy Leaders
    # ════════════════════════════════════════

    # 14. 周岩 — 副区长
    {
        "id": 14,
        "name": "周岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年12月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "涧西区人民政府",
        "source": "http://www.jxq.gov.cn/2025/12-29/1025732.html (涧西区领导之窗 - 周岩)",
    },
    # 15. 胡全超 — 副区长、公安分局长
    {
        "id": 15,
        "name": "胡全超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年9月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、涧西公安分局局长",
        "current_org": "涧西区人民政府/洛阳市公安局涧西分局",
        "source": "http://www.jxq.gov.cn/2025/12-29/1025736.html (涧西区领导之窗 - 胡全超)",
    },
    # 16. 王莎莎 — 副区长
    {
        "id": 16,
        "name": "王莎莎",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年7月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "涧西区人民政府",
        "source": "http://www.jxq.gov.cn/2025/12-29/1025735.html (涧西区领导之窗 - 王莎莎)",
    },
    # 17. 王鹏杰 — 副区长
    {
        "id": 17,
        "name": "王鹏杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990年6月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "涧西区人民政府",
        "source": "http://www.jxq.gov.cn/2026/06-09/1066752.html (涧西区领导之窗 - 王鹏杰)",
    },
    # 18. 任钊函 — 副区长 (挂职)
    {
        "id": 18,
        "name": "任钊函",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年1月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "涧西区人民政府",
        "source": "http://www.jxq.gov.cn/2026/05-12/1060614.html (涧西区领导之窗 - 任钊函)",
    },
    # 19. 陈聪聪 — 副区长 (挂职)
    {
        "id": 19,
        "name": "陈聪聪",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986年4月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "涧西区人民政府",
        "source": "http://www.jxq.gov.cn/2026/05-12/1060613.html (涧西区领导之窗 - 陈聪聪)",
    },
    # 20. 张涛 — 区政府党组成员、办公室主任
    {
        "id": 20,
        "name": "张涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、办公室主任",
        "current_org": "涧西区人民政府办公室",
        "source": "http://www.jxq.gov.cn/2025/12-29/1025734.html (涧西区领导之窗 - 张涛)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共涧西区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共洛阳市委员会",
        "location": "河南省洛阳市涧西区",
    },
    {
        "id": 2,
        "name": "涧西区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "洛阳市人民政府",
        "location": "河南省洛阳市涧西区",
    },
    {
        "id": 3,
        "name": "涧西区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "洛阳市人大常委会",
        "location": "河南省洛阳市涧西区",
    },
    {
        "id": 4,
        "name": "政协涧西区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协洛阳市委员会",
        "location": "河南省洛阳市涧西区",
    },
    {
        "id": 5,
        "name": "涧西区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共洛阳市纪律检查委员会",
        "location": "河南省洛阳市涧西区",
    },
    {
        "id": 6,
        "name": "洛阳高新区管委会",
        "type": "开发区",
        "level": "国家级高新区",
        "parent": "洛阳市人民政府",
        "location": "河南省洛阳市",
    },
    {
        "id": 7,
        "name": "洛阳市公安局涧西分局",
        "type": "政府",
        "level": "正科级",
        "parent": "洛阳市公安局",
        "location": "河南省洛阳市涧西区",
    },
    {
        "id": 8,
        "name": "涧西区人民政府办公室",
        "type": "政府",
        "level": "正科级",
        "parent": "涧西区人民政府",
        "location": "河南省洛阳市涧西区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 谢峰 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记",
     "start": "", "end": "present",
     "rank": "正处级",
     "note": "Also serves as 高新区党工委书记. Confirmed via 涧西区人民政府 news 2026-07-31 and 区第十一次党代会 2026-06-24"},
    # 孙论兵 - 区委副书记、区长
    {"person_id": 2, "org_id": 2, "title": "区长",
     "start": "", "end": "present",
     "rank": "正处级",
     "note": "Also serves as 区委副书记, 高新区党工委副书记、管委会主任. Confirmed via 领导之窗 page"},
    {"person_id": 2, "org_id": 6, "title": "高新区党工委副书记、管委会主任",
     "start": "", "end": "present",
     "rank": "正处级",
     "note": "Also serves as 自贸区洛阳片区、综保区党工委委员、管委会副主任"},

    # ── Party Standing Committee ──
    {"person_id": 3, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Elected at 11th District Party Congress 2026-06-24"},
    {"person_id": 3, "org_id": 2, "title": "常务副区长（区政府党组副书记）",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Also 高新区党工委委员、管委会副主任"},
    {"person_id": 4, "org_id": 1, "title": "区委常委、宣传部长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "区政府党组成员"},
    {"person_id": 5, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Elected at 2026-06-24 District Party Congress"},
    {"person_id": 6, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Elected at 2026-06-24 District Party Congress"},
    {"person_id": 7, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Elected at 2026-06-24 District Party Congress"},
    {"person_id": 8, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Elected at 2026-06-24 District Party Congress"},
    {"person_id": 9, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Elected at 2026-06-24 District Party Congress"},
    {"person_id": 10, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Elected at 2026-06-24 District Party Congress"},
    {"person_id": 11, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Elected at 2026-06-24 District Party Congress"},
    {"person_id": 12, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Elected at 2026-06-24 District Party Congress"},
    {"person_id": 13, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Elected at 2026-06-24 District Party Congress"},

    # ── Government Deputy Leaders ──
    {"person_id": 14, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "区政府党组成员"},
    {"person_id": 15, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Also serves as 涧西公安分局局长"},
    {"person_id": 15, "org_id": 7, "title": "涧西公安分局局长",
     "start": "", "end": "present",
     "rank": "正科级",
     "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "区政府党组成员"},
    {"person_id": 17, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "区政府党组成员"},
    {"person_id": 18, "org_id": 2, "title": "副区长（挂职）",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": ""},
    {"person_id": 19, "org_id": 2, "title": "副区长（挂职）",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": ""},
    {"person_id": 20, "org_id": 8, "title": "区政府办公室主任",
     "start": "", "end": "present",
     "rank": "正科级",
     "note": "区政府党组成员"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 谢峰 <-> 孙论兵: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记谢峰与区长孙论兵党政主要领导搭档; 共同负责涧西区全面工作; 在2026年第十一次党代会上一同当选新一届领导班子",
     "overlap_org": "中共涧西区委员会/涧西区人民政府",
     "overlap_period": "截至2026年8月"},

    # 程欢 — 常务副区长, 谢峰和孙论兵的主要助手
    {"person_a": 3, "person_b": 1, "type": "superior_subordinate",
     "context": "程欢作为常务副区长, 在区政府常务会议上协助区长孙论兵开展工作; 同时为区委常委参加区委常委会",
     "overlap_org": "中共涧西区委员会/涧西区人民政府",
     "overlap_period": "截至2026年8月"},

    # 所有区委常委与谢峰（书记）的常委班子关系
    {"person_a": 4, "person_b": 1, "type": "superior_subordinate",
     "context": "王锐为区委常委、宣传部长, 在区委常委会中向区委书记谢峰汇报",
     "overlap_org": "中共涧西区委员会",
     "overlap_period": "截至2026年8月"},
    {"person_a": 5, "person_b": 1, "type": "superior_subordinate",
     "context": "尚刚涛为区委常委, 在区委常委会中与谢峰共事",
     "overlap_org": "中共涧西区委员会",
     "overlap_period": "截至2026年8月"},
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate",
     "context": "仲家玉为区委常委, 在区委常委会中与谢峰共事",
     "overlap_org": "中共涧西区委员会",
     "overlap_period": "截至2026年8月"},
    {"person_a": 7, "person_b": 1, "type": "superior_subordinate",
     "context": "赵晖为区委常委, 在区委常委会中与谢峰共事",
     "overlap_org": "中共涧西区委员会",
     "overlap_period": "截至2026年8月"},
    {"person_a": 8, "person_b": 1, "type": "superior_subordinate",
     "context": "张京波为区委常委, 在区委常委会中与谢峰共事",
     "overlap_org": "中共涧西区委员会",
     "overlap_period": "截至2026年8月"},
    {"person_a": 9, "person_b": 1, "type": "superior_subordinate",
     "context": "韩静为区委常委, 在区委常委会中与谢峰共事",
     "overlap_org": "中共涧西区委员会",
     "overlap_period": "截至2026年8月"},
    {"person_a": 10, "person_b": 1, "type": "superior_subordinate",
     "context": "刘超为区委常委, 在区委常委会中与谢峰共事",
     "overlap_org": "中共涧西区委员会",
     "overlap_period": "截至2026年8月"},
    {"person_a": 11, "person_b": 1, "type": "superior_subordinate",
     "context": "何鹏为区委常委, 在区委常委会中与谢峰共事",
     "overlap_org": "中共涧西区委员会",
     "overlap_period": "截至2026年8月"},
    {"person_a": 12, "person_b": 1, "type": "superior_subordinate",
     "context": "杜利峰为区委常委, 在区委常委会中与谢峰共事",
     "overlap_org": "中共涧西区委员会",
     "overlap_period": "截至2026年8月"},
    {"person_a": 13, "person_b": 1, "type": "superior_subordinate",
     "context": "李龙飞为区委常委, 在区委常委会中与谢峰共事",
     "overlap_org": "中共涧西区委员会",
     "overlap_period": "截至2026年8月"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "涧西区人民政府 - 首页 - 要闻动态",
            "url": "http://www.jxq.gov.cn/",
            "publisher": "涧西区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "政府门户网站, 包含 涧西区委书记、高新区党工委书记谢峰督导调研防汛备汛工作 (2026-07-31); 涧西区政府第76次常务会议 (2026-07-29)",
        },
        {
            "id": "S002",
            "title": "涧西区人民政府 - 领导之窗 - 孙论兵",
            "url": "http://www.jxq.gov.cn/2025/12-29/1025739.html",
            "publisher": "涧西区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "孙论兵个人简历: 区委副书记、区政府党组书记、区长",
        },
        {
            "id": "S003",
            "title": "涧西区人民政府 - 领导之窗 - 程欢",
            "url": "http://www.jxq.gov.cn/2025/12-29/1025738.html",
            "publisher": "涧西区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "程欢个人简历: 区委常委、区政府党组副书记、副区长",
        },
        {
            "id": "S004",
            "title": "涧西区人民政府 - 领导之窗 - 王锐",
            "url": "http://www.jxq.gov.cn/2025/12-29/1025737.html",
            "publisher": "涧西区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "王锐个人简历: 区委常委、宣传部 部长, 区政府党组成员、副区长",
        },
        {
            "id": "S005",
            "title": "涧西区人民政府 - 领导之窗 - 周岩",
            "url": "http://www.jxq.gov.cn/2025/12-29/1025732.html",
            "publisher": "涧西区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "周岩个人简历: 区政府党组成员、副区长",
        },
        {
            "id": "S006",
            "title": "涧西区人民政府 - 领导之窗 - 胡全超",
            "url": "http://www.jxq.gov.cn/2025/12-29/1025736.html",
            "publisher": "涧西区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "胡全超个人简历: 区政府党组成员、副区长, 涧西公安分局局长",
        },
        {
            "id": "S007",
            "title": "涧西区人民政府 - 领导之窗 - 王莎莎",
            "url": "http://www.jxq.gov.cn/2025/12-29/1025735.html",
            "publisher": "涧西区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "王莎莎个人简历: 区政府党组成员、副区长",
        },
        {
            "id": "S008",
            "title": "涧西区人民政府 - 领导之窗 - 王鹏杰",
            "url": "http://www.jxq.gov.cn/2026/06-09/1066752.html",
            "publisher": "涧西区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "王鹏杰个人简历: 区政府党组成员、副区长",
        },
        {
            "id": "S009",
            "title": "涧西区人民政府 - 领导之窗 - 任钊函",
            "url": "http://www.jxq.gov.cn/2026/05-12/1060614.html",
            "publisher": "涧西区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "任钊函个人简历: 区政府副区长(挂职)",
        },
        {
            "id": "S010",
            "title": "涧西区人民政府 - 领导之窗 - 陈聪聪",
            "url": "http://www.jxq.gov.cn/2026/05-12/1060613.html",
            "publisher": "涧西区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "陈聪聪个人简历: 区政府副区长(挂职)",
        },
        {
            "id": "S011",
            "title": "涧西区人民政府 - 领导之窗 - 张涛",
            "url": "http://www.jxq.gov.cn/2025/12-29/1025734.html",
            "publisher": "涧西区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "张涛个人简历: 区政府党组成员, 办公室党组书记、主任",
        },
        {
            "id": "S012",
            "title": "洛阳市人民政府 - 要闻动态 - 县区",
            "url": "https://www.ly.gov.cn/",
            "publisher": "洛阳市人民政府",
            "published_at": "2026-07-31",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "新闻条目: 涧西区委书记、高新区党工委书记谢峰督导调研防汛备汛工作; 涧西区为荣获二级表彰现役军人家庭送喜报",
        },
        {
            "id": "S013",
            "title": "涧西区第十一次党代会开幕式",
            "url": "http://www.jxq.gov.cn/2026/06-26/1069701.html",
            "publisher": "涧西区人民政府",
            "published_at": "2026-06-24",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "开幕消息: 谢峰(书记) 孙论兵(副书记) 在主席台前排就座; 公布新一届5年工作方向",
        },
        {
            "id": "S014",
            "title": "涧西区第十一次党代会闭幕",
            "url": "http://www.jxq.gov.cn/2026/06-26/1069700.html",
            "publisher": "涧西区人民政府",
            "published_at": "2026-06-25",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "闭幕新闻稿: 公布11届区委常委名单（执行主席7名+多位常委）",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"jianxi_{name}"

    # ── 谢峰 (区委书记) ──
    if name == "谢峰":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "洛阳市",
                "region": "涧西区",
                "job": "区委书记",
                "task_id": "henan_涧西区",
                "time_focus": "当前",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "谢峰",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "谢峰_",
                    "name_birthplace": "谢峰_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共涧西区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S012", "S013"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共涧西区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "河南省洛阳市涧西区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "Confirmed as of 2026-06-24 (第十一次党代会), still active 2026-07-31 (防汛调研). Also serves as 高新区党工委书记. 到任时间及此前履历未公开。",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S012", "S013"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共涧西区委员会", "type": "党委",
                 "level": "县处级", "location": "河南省洛阳市涧西区"},
                {"org_id": 6, "name": "洛阳高新区管委会", "type": "开发区",
                 "level": "国家级高新区", "location": "河南省洛阳市"},
            ],
            "relationships": [
                {"person": "孙论兵", "person_id": "jianxi_孙论兵",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档; 共同主持第十一次党代会主席团",
                 "overlap_org": "中共涧西区委员会/涧西区人民政府",
                 "overlap_period": "截至2026年8月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002", "S013", "S014"]},
            ],
            "governance_record": [
                {
                    "period": "2026年",
                    "domain": "urban_construction",
                    "achievement_or_event": "开展防汛备汛调研督导",
                    "role_in_event": "主要领导(区委书记)",
                    "measurable_outcome": "",
                    "location": "涧西区",
                    "confidence": "confirmed",
                    "source_ids": ["S012"],
                },
                {
                    "period": "2026-06",
                    "domain": "other",
                    "achievement_or_event": "主持涧西区第十一次党代会, 作《高举旗帜 感恩奋进 奋力谱写中国式现代化涧西建设新篇章》工作报告",
                    "role_in_event": "大会执行主席/报告人",
                    "measurable_outcome": "选举产生第十一届区委班子、部署未来5年发展方向",
                    "location": "涧西区",
                    "confidence": "confirmed",
                    "source_ids": ["S013", "S014"],
                },
            ],
            "professional_profile": {
                "primary_specializations": ["party_leadership", "economic_development"],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "reform_oriented",
                        "evidence": "党代会报告提出打造'三高地一城区'和'现代强区—涧西'的5年目标",
                        "confidence": "plausible",
                        "source_ids": ["S013"],
                    },
                    {
                        "trait": "grassroots_oriented",
                        "evidence": "2026-07-31主动开展防汛调研",
                        "confidence": "plausible",
                        "source_ids": ["S012"],
                    },
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "工作风格来自公开报道和讲话, 非心理评估.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年8月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "high",
                "biggest_gap": "谢峰的全履历(出生日期、籍贯、教育背景、此前担任的职务等)均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "谢峰的出生日期、籍贯和学历背景？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["谢峰 简历 涧西区", "谢峰 洛阳 区委书记"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "谢峰何时开始担任涧西区区委书记？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["谢峰 任 涧西区 区委书记", "谢峰 任前公示", "涧西区 区委书记 前任"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "谢峰是否有Baidu Baike页面？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["谢峰 河南 简历"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 孙论兵 (区长) ──
    if name == "孙论兵":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "洛阳市",
                "region": "涧西区",
                "job": "区长",
                "task_id": "henan_涧西区",
                "time_focus": "当前",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "孙论兵",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1976年11月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": "本科",
                        "study_type": "unknown",
                        "source_ids": ["S002"],
                    }
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "孙论兵_197611",
                    "name_birthplace": "孙论兵_",
                    "official_profile_url": "http://www.jxq.gov.cn/2025/12-29/1025739.html",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "涧西区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S002"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "涧西区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "河南省洛阳市涧西区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "Also serves as 区委副书记, 高新区党工委副书记、管委会主任. 到任时间、此前职务不明。",
                    "confidence": "confirmed",
                    "source_ids": ["S002"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "涧西区人民政府", "type": "政府",
                 "level": "县处级", "location": "河南省洛阳市涧西区"},
                {"org_id": 6, "name": "洛阳高新区管委会", "type": "开发区",
                 "level": "国家级高新区", "location": "河南省洛阳市"},
            ],
            "relationships": [
                {"person": "谢峰", "person_id": "jianxi_谢峰",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档",
                 "overlap_org": "中共涧西区委员会/涧西区人民政府",
                 "overlap_period": "截至2026年8月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002", "S013", "S014"]},
            ],
            "governance_record": [
                {
                    "period": "2026-07-28",
                    "domain": "other",
                    "achievement_or_event": "主持涧西区政府第76次常务会议暨高新区管委会主任联席会",
                    "role_in_event": "主持人(区长)",
                    "measurable_outcome": "学习传达防汛、消防、法治政府等政策文件",
                    "location": "涧西区",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "professional_profile": {
                "primary_specializations": ["government_administration"],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "low_profile",
                        "evidence": "公开资料中只有日常工作报道，未见突出个人风格",
                        "confidence": "unverified",
                        "source_ids": [],
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "工作风格来自公开报道和讲话推断，非心理评估。",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年8月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "high",
                "biggest_gap": "孙论兵任区长前的完整履历、教育经历和此前职务均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "孙论兵的毕业院校和专业？",
                    "why_it_matters": "去重和档案建库的必需信息",
                    "suggested_queries": ["孙论兵 教育 背景", "孙论兵 毕业院校"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "孙论兵何时开始担任涧西区区长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["孙论兵 任 涧西区 区长", "孙论兵 任前公示", "孙论兵 此前 担任"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "孙论兵的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["孙论兵 简历", "孙论兵 洛阳市"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    return None


def write_person_json(p: dict, name: str) -> None:
    """Write single person JSON."""
    job = p["current_post"].replace("（", "(").replace("）", ")")
    data = generate_person_json(job, name)
    if data:
        # Shorten filename job to just core role
        short_job = p["current_post"]
        person_path = PERSONS_DIR / f"{TODAY}-河南省-洛阳市-{short_job}-{name}.json"
        with open(person_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {person_path.relative_to(_REPO_ROOT)}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def main():
    # Create DB and GEXF via runner
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for the two core targets
    name_to_check = {"谢峰", "孙论兵"}
    for p in persons:
        if p["name"] in name_to_check:
            write_person_json(p, p["name"])

    print("\nDone.")


if __name__ == "__main__":
    main()