#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 龙城区 (Longcheng District), 朝阳市, 辽宁省.

Level: 市辖区
Province: 辽宁省
Parent city: 朝阳市
Targets: 区委书记 (Party Secretary: 李大为), 区长 (District Mayor: 李鼎)
Task ID: liaoning_龙城区

Research date: 2026-07-25
Official source: http://www.cylc.gov.cn/ (朝阳市龙城区人民政府)

Current status (as of 2026-07-25, verified via official district website www.cylc.gov.cn):

区委领导:
- 李大为 — 区委书记。男，汉族，代表中共龙城区第九届委员会向第十次党代会作报告。
  来源: 龙城区第十次党代会报道 (2026年7月23-24日)

区政府领导 (来源: www.cylc.gov.cn 政务公开-政府领导页):
- 李鼎 — 区委副书记、区长。男，汉族，1985年4月生，大学学历，公共管理硕士学位，中共党员。
  主持区政府全面工作。兼任朝阳高新技术产业开发区党工委书记。
  来源: https://www.cylc.gov.cn/html/LCQZF/202109/0163168690280868.html

- 齐景山 — 区委常委，区政府党组副书记，副区长（常务）。男，汉族，1974年9月生，在职研究生学历，中共党员。
  来源: https://www.cylc.gov.cn/html/LCQZF/202308/0169338354292641.html

- 刘凤玉 — 副区长。男，汉族，1975年11月生，大学学历，中共党员。现任朝阳高新技术产业开发区党工委副书记，管委会主任。
  来源: https://www.cylc.gov.cn/html/LCQZF/202111/0163774762571018.html

- 张继业 — 区委常委，副区长。男，汉族，1979年2月生，研究生学历，中共党员。
  来源: https://www.cylc.gov.cn/html/LCQZF/202408/0174900344478485.html

- 于泓志 — 副区长。男，汉族，1983年9月生，大学学历，学士学位。
  来源: https://www.cylc.gov.cn/html/LCQZF/202109/0163774762571024.html

- 于忠军 — 副区长（兼市公安局龙城分局局长）。男，蒙古族，1968年8月生，大学学历，学士学位，中共党员，二级高级警长。
  来源: https://www.cylc.gov.cn/html/LCQZF/202109/0163774762571030.html

- 张亚光 — 副区长。女，汉族，1975年11月生，大学学历，中共党员。
  来源: https://www.cylc.gov.cn/html/LCQZF/202109/0163774762571036.html

- 杜剑 — 副区长。男，汉族，1988年3月生，研究生学历，中共党员。
  来源: https://www.cylc.gov.cn/html/LCQZF/202408/0174900462109525.html

区委常委会其他执行主席 (来源: 龙城区第十次党代会报道):
- 国小舟, 金海欣, 赵国辉, 鲁海荣, 刘树义, 边巴央金, 刘学明

区人大、区政协领导:
- 邵永丰 (人大), 牛晓菊 (政协)

Leadership info sourced from:
  - http://www.cylc.gov.cn/ 龙城区人民政府官网
  - https://www.cylc.gov.cn/html/LCQZF/202109/0163168690280868.html (区长李鼎领导页)
  - https://www.cylc.gov.cn/html/LCQZF/202607/0178485573918912.html (第十次党代会-李大为)
  - https://www.cylc.gov.cn/html/LCQZF/202607/0178459593524532.html (区委常委会第169次会议)

Confidence notes:
  李大为身份为区委书记通过龙城区第十次党代会报道确认（2026年7月23-24日）。
  李鼎身份和简历通过区政府官方网站领导页确认（1985年4月生，公共管理硕士，中共党员）。
  李大为的详细职业履历（出生年月、教育背景、早期经历）需进一步核实。
  区政府班子成员简历通过官方网站确认。
  区委常委班子成员部分成员通过党代会报道确认。

Encyclopedia sources:
  百度百科因百度安全验证限制无法获取，李大为、李鼎的百度百科页面待补充访问。
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

SLUG = "龙城区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 李大为 — 区委书记
    {
        "id": 1,
        "name": "李大为",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共朝阳市龙城区委员会",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202607/0178485573918912.html",
    },
    # 2. 李鼎 — 区委副书记、区长
    {
        "id": 2,
        "name": "李鼎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年4月",
        "birthplace": "",
        "education": "大学学历，公共管理硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "朝阳市龙城区人民政府",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202109/0163168690280868.html",
    },

    # ════════════════════════════════════════
    # 区政府领导 (Government Leadership)
    # ════════════════════════════════════════

    # 3. 齐景山 — 区委常委、常务副区长
    {
        "id": 3,
        "name": "齐景山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "朝阳市龙城区人民政府",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202308/0169338354292641.html",
    },
    # 4. 刘凤玉 — 副区长/高新区管委会主任
    {
        "id": 4,
        "name": "刘凤玉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "朝阳市龙城区人民政府",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202111/0163774762571018.html",
    },
    # 5. 张继业 — 区委常委、副区长
    {
        "id": 5,
        "name": "张继业",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年2月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "朝阳市龙城区人民政府",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202408/0174900344478485.html",
    },
    # 6. 于泓志 — 副区长
    {
        "id": 6,
        "name": "于泓志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年9月",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "朝阳市龙城区人民政府",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202109/0163774762571024.html",
    },
    # 7. 于忠军 — 副区长/公安分局局长
    {
        "id": 7,
        "name": "于忠军",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1968年8月",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "朝阳市龙城区人民政府",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202109/0163774762571030.html",
    },
    # 8. 张亚光 — 副区长
    {
        "id": 8,
        "name": "张亚光",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "朝阳市龙城区人民政府",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202109/0163774762571036.html",
    },
    # 9. 杜剑 — 副区长
    {
        "id": 9,
        "name": "杜剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年3月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "朝阳市龙城区人民政府",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202408/0174900462109525.html",
    },

    # ════════════════════════════════════════
    # 区委常委 (Party Standing Committee)
    # ════════════════════════════════════════

    # 10. 国小舟 — 区委常委（党代会执行主席）
    {
        "id": 10,
        "name": "国小舟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共朝阳市龙城区委员会",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202607/0178485573918912.html",
    },
    # 11. 金海欣 — 区委常委（党代会执行主席）
    {
        "id": 11,
        "name": "金海欣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共朝阳市龙城区委员会",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202607/0178485573918912.html",
    },
    # 12. 赵国辉 — 区委常委（党代会执行主席）
    {
        "id": 12,
        "name": "赵国辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共朝阳市龙城区委员会",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202607/0178485573918912.html",
    },
    # 13. 鲁海荣 — 区委常委（党代会执行主席）
    {
        "id": 13,
        "name": "鲁海荣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共朝阳市龙城区委员会",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202607/0178485573918912.html",
    },
    # 14. 刘树义 — 区委常委（党代会执行主席）
    {
        "id": 14,
        "name": "刘树义",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共朝阳市龙城区委员会",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202607/0178485573918912.html",
    },
    # 15. 边巴央金 — 区委常委（党代会执行主席）
    {
        "id": 15,
        "name": "边巴央金",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共朝阳市龙城区委员会",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202607/0178485573918912.html",
    },
    # 16. 刘学明 — 区委常委（党代会执行主席）
    {
        "id": 16,
        "name": "刘学明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共朝阳市龙城区委员会",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202607/0178485573918912.html",
    },

    # ════════════════════════════════════════
    # 区人大、区政协领导
    # ════════════════════════════════════════

    # 17. 邵永丰 — 区人大常委会主任
    {
        "id": 17,
        "name": "邵永丰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "朝阳市龙城区人民代表大会常务委员会",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202607/0178485573918912.html",
    },
    # 18. 牛晓菊 — 区政协主席
    {
        "id": 18,
        "name": "牛晓菊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协朝阳市龙城区委员会",
        "source": "https://www.cylc.gov.cn/html/LCQZF/202607/0178485573918912.html",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    # 党委系统
    {"id": 1, "name": "中共朝阳市龙城区委员会", "type": "党委", "level": "县处级", "parent": "中共朝阳市委员会", "location": "朝阳市龙城区"},
    # 政府系统
    {"id": 2, "name": "朝阳市龙城区人民政府", "type": "政府", "level": "县处级", "parent": "朝阳市人民政府", "location": "朝阳市龙城区"},
    {"id": 3, "name": "朝阳市公安局龙城分局", "type": "政府", "level": "乡科级", "parent": "朝阳市龙城区人民政府", "location": "朝阳市龙城区"},
    {"id": 4, "name": "朝阳高新技术产业开发区", "type": "开发区", "level": "县处级", "parent": "朝阳市人民政府", "location": "朝阳市龙城区"},
    # 人大、政协
    {"id": 5, "name": "朝阳市龙城区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "朝阳市龙城区", "location": "朝阳市龙城区"},
    {"id": 6, "name": "政协朝阳市龙城区委员会", "type": "政协", "level": "县处级", "parent": "朝阳市龙城区", "location": "朝阳市龙城区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── 李大为 (id=1) ──
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "龙城区委书记，代表第九届委员会向第十次党代会作报告（2026年7月）"},

    # ── 李鼎 (id=2) ──
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "区委副书记、区长，主持区政府全面工作"},
    {"person_id": 2, "org_id": 4, "title": "朝阳高新技术产业开发区党工委书记（兼）", "start_date": "", "end_date": "至今", "rank": "", "note": ""},

    # ── 齐景山 (id=3) ──
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区委常委"},
    {"person_id": 3, "org_id": 2, "title": "副区长（常务）", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区政府党组副书记，负责区政府常务工作"},

    # ── 刘凤玉 (id=4) ──
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "负责商务、外事等工作"},
    {"person_id": 4, "org_id": 4, "title": "朝阳高新技术产业开发区党工委副书记、管委会主任", "start_date": "", "end_date": "至今", "rank": "", "note": ""},

    # ── 张继业 (id=5) ──
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区委常委"},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "负责水利、卫健、医保、市场监管、林草等工作"},

    # ── 于泓志 (id=6) ──
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "负责教育、民政、退役军人等工作"},

    # ── 于忠军 (id=7) ──
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "兼市公安局龙城分局局长"},
    {"person_id": 7, "org_id": 3, "title": "朝阳市公安局龙城分局局长（兼）", "start_date": "", "end_date": "至今", "rank": "二级高级警长", "note": "区政府党组成员"},

    # ── 张亚光 (id=8) ──
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "负责工信、科技、统计、大数据、营商环境、文旅体育等工作"},

    # ── 杜剑 (id=9) ──
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "负责住建、交通、城市管理等工作"},

    # ── 区委常委 (id=10~16) ──
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "党代会执行主席"},
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "党代会执行主席"},
    {"person_id": 12, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "党代会执行主席"},
    {"person_id": 13, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "党代会执行主席"},
    {"person_id": 14, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "党代会执行主席"},
    {"person_id": 15, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "党代会执行主席"},
    {"person_id": 16, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "党代会执行主席"},

    # ── 邵永丰 (id=17) ──
    {"person_id": 17, "org_id": 5, "title": "区人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "党代会在主席台前排就座"},
    # ── 牛晓菊 (id=18) ──
    {"person_id": 18, "org_id": 6, "title": "区政协主席", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "党代会在主席台前排就座"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 李大为 ↔ 李鼎 → 党政主官搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "李大为任区委书记，李鼎任区委副书记、区长，党政主官搭档",
        "overlap_org": "中共朝阳市龙城区委员会",
        "overlap_period": "",
    },

    # 李大为 ↔ 齐景山 → 上下级
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "李大为任区委书记，齐景山任区委常委、常务副区长",
        "overlap_org": "中共朝阳市龙城区委员会",
        "overlap_period": "",
    },

    # 李大为 ↔ 张继业 → 上下级
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "李大为任区委书记，张继业任区委常委、副区长",
        "overlap_org": "中共朝阳市龙城区委员会",
        "overlap_period": "",
    },

    # 李鼎 ↔ 齐景山 → 上下级（区长-常务副区长）
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "李鼎任区长，齐景山任区委常委、常务副区长（区政府党组副书记）",
        "overlap_org": "朝阳市龙城区人民政府",
        "overlap_period": "",
    },

    # 李鼎 ↔ 刘凤玉 → 上下级（区长-副区长/高新区主任）
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "李鼎任区长，刘凤玉任副区长/高新区管委会主任",
        "overlap_org": "朝阳市龙城区人民政府",
        "overlap_period": "",
    },

    # 李鼎 ↔ 张继业 → 上下级（区长-副区长）
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "李鼎任区长，张继业任区委常委、副区长",
        "overlap_org": "朝阳市龙城区人民政府",
        "overlap_period": "",
    },

    # 李鼎 ↔ 于泓志 → 上下级（区长-副区长）
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "李鼎任区长，于泓志任副区长",
        "overlap_org": "朝阳市龙城区人民政府",
        "overlap_period": "",
    },

    # 李鼎 ↔ 于忠军 → 上下级（区长-副区长/公安局长）
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "李鼎任区长，于忠军任副区长兼市公安局龙城分局局长",
        "overlap_org": "朝阳市龙城区人民政府",
        "overlap_period": "",
    },

    # 李鼎 ↔ 张亚光 → 上下级（区长-副区长）
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "李鼎任区长，张亚光任副区长",
        "overlap_org": "朝阳市龙城区人民政府",
        "overlap_period": "",
    },

    # 李鼎 ↔ 杜剑 → 上下级（区长-副区长）
    {
        "person_a": 2,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "李鼎任区长，杜剑任副区长",
        "overlap_org": "朝阳市龙城区人民政府",
        "overlap_period": "",
    },

    # 区委常委间共事关系
    {
        "person_a": 3,
        "person_b": 5,
        "type": "overlap",
        "context": "齐景山与张继业均任区委常委，共同参与区委决策",
        "overlap_org": "中共朝阳市龙城区委员会",
        "overlap_period": "",
    },

    # 李大为 ↔ 区委常委 → 上下级
    {
        "person_a": 1,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "李大为任区委书记，国小舟任区委常委",
        "overlap_org": "中共朝阳市龙城区委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "李大为任区委书记，金海欣任区委常委",
        "overlap_org": "中共朝阳市龙城区委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 12,
        "type": "superior_subordinate",
        "context": "李大为任区委书记，赵国辉任区委常委",
        "overlap_org": "中共朝阳市龙城区委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "李大为任区委书记，鲁海荣任区委常委",
        "overlap_org": "中共朝阳市龙城区委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 14,
        "type": "superior_subordinate",
        "context": "李大为任区委书记，刘树义任区委常委",
        "overlap_org": "中共朝阳市龙城区委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 15,
        "type": "superior_subordinate",
        "context": "李大为任区委书记，边巴央金任区委常委",
        "overlap_org": "中共朝阳市龙城区委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 16,
        "type": "superior_subordinate",
        "context": "李大为任区委书记，刘学明任区委常委",
        "overlap_org": "中共朝阳市龙城区委员会",
        "overlap_period": "",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

def write_person_json() -> None:
    """Write per-person JSON files for core figures."""

    # ── 李大为 Person JSON ──
    lidawei = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "朝阳市",
            "region": "龙城区",
            "job": "区委书记",
            "task_id": "liaoning_龙城区",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": "liaoning_chaoyang_longcheng_lidawei",
            "name": "李大为",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "李大为",
                "name_birthplace": "李大为",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": "区委书记",
            "current_org": "中共朝阳市龙城区委员会",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "未知",
                "end": "至今",
                "org": "中共朝阳市龙城区委员会",
                "title": "区委书记",
                "level": "正处级",
                "location": "朝阳市龙城区",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2026年7月代表第九届区委向第十次党代会作报告",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "未知",
                "end": "未知",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到李大为任龙城区委书记前的完整履历",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "organizations": [
            {"org_id": "org_chaoyang_longcheng_committee", "name": "中共朝阳市龙城区委员会", "role": "current_leader", "period": "至今"},
        ],
        "relationships": [
            {"person": "李鼎", "person_id": "liaoning_chaoyang_longcheng_liding_1985", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "李大为任区委书记，李鼎任区委副书记、区长", "overlap_org": "中共朝阳市龙城区委员会", "overlap_period": "", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            {"person": "齐景山", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "李大为任区委书记，齐景山任区委常委", "overlap_org": "中共朝阳市龙城区委员会", "overlap_period": "", "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S001"]},
            {"person": "张继业", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "李大为任区委书记，张继业任区委常委", "overlap_org": "中共朝阳市龙城区委员会", "overlap_period": "", "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S001"]},
        ],
        "governance_record": [
            {"period": "至今", "domain": "other", "achievement_or_event": "主持区委全面工作；代表第九届区委在第十次党代会上作工作报告", "role_in_event": "区委书记", "measurable_outcome": "", "location": "龙城区", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "因公开履历信息不足，尚无法评估晋升节奏",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [
                "正确政绩观",
                "举步新起点、奋进新征程",
                "中国式现代化龙城新篇章",
                "新质生产力",
                "科技创新与产业创新深度融合",
            ],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月25日，公开渠道未发现李大为的纪律处分、审计问题或负面媒体报道",
                "date": AS_OF,
                "confidence": "plausible",
                "source_ids": [],
            },
        ],
        "source_register": [
            {"id": "S001", "title": "龙城区第十次党代会开幕报道", "url": "https://www.cylc.gov.cn/html/LCQZF/202607/0178485573918912.html", "publisher": "龙城区人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "李大为代表第九届区委作报告"},
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "李大为的出生日期、教育背景、完整职业履历及前任区委书记信息均需补充",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "李大为的出生年月、籍贯、教育背景？",
                "why_it_matters": "核心人物基本身份信息缺失，影响身份去重和人物识别",
                "suggested_queries": ["李大为 龙城区 简历", "李大为 朝阳市 出生"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "李大为任区委书记之前的完整职业履历（曾任职务）？",
                "why_it_matters": "缺少前任岗位信息，无法构建完整的职业晋升路径",
                "suggested_queries": ["李大为 龙城区 任职经历", "李大为 朝阳 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "李大为的前任区委书记是谁？去向何处？",
                "why_it_matters": "完整的书记更替链有助于分析龙城区领导班子变动趋势",
                "suggested_queries": ["龙城区 前任区委书记", "龙城区 2022 2023 2024 2025 区委书记"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": "李大为的入党时间与开始工作时间？",
                "why_it_matters": "影响对政治资历和晋升节奏的评估",
                "suggested_queries": ["李大为 入党 工作"],
                "last_attempted": AS_OF,
            },
        ],
    }

    person_path = PERSONS_DIR / f"{TODAY}-辽宁省-朝阳市-区委书记-李大为.json"
    with open(person_path, "w", encoding="utf-8") as f:
        json.dump(lidawei, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {person_path.name}")

    # ── 李鼎 Person JSON ──
    liding = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "朝阳市",
            "region": "龙城区",
            "job": "区长",
            "task_id": "liaoning_龙城区",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": "liaoning_chaoyang_longcheng_liding_1985",
            "name": "李鼎",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1985年4月",
            "birthplace": "",
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": "公共管理硕士",
                    "study_type": "unknown",
                    "source_ids": ["S002"],
                },
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": "大学",
                    "study_type": "full_time",
                    "source_ids": ["S002"],
                },
            ],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "李鼎_1985",
                "name_birthplace": "李鼎",
                "official_profile_url": "https://www.cylc.gov.cn/html/LCQZF/202109/0163168690280868.html",
            },
        },
        "current_status": {
            "current_post": "区长",
            "current_org": "朝阳市龙城区人民政府",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S002"],
        },
        "career_timeline": [
            {
                "start": "未知",
                "end": "至今",
                "org": "朝阳市龙城区人民政府",
                "title": "区长",
                "level": "正处级",
                "location": "龙城区",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "区委副书记、区长，主持区政府全面工作；兼朝阳高新技术产业开发区党工委书记",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            },
            {
                "start": "未知",
                "end": "未知",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到李鼎任龙城区区长前的完整履历",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "organizations": [
            {"org_id": "org_chaoyang_longcheng_gov", "name": "朝阳市龙城区人民政府", "role": "current_leader", "period": "至今"},
            {"org_id": "org_chaoyang_high_tech_zone", "name": "朝阳高新技术产业开发区", "role": "current_leader", "period": "至今"},
        ],
        "relationships": [
            {"person": "李大为", "person_id": "liaoning_chaoyang_longcheng_lidawei", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "李鼎任区委副书记、区长，李大为任区委书记", "overlap_org": "中共朝阳市龙城区委员会", "overlap_period": "", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            {"person": "齐景山", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "齐景山任常务副区长，李鼎任区长", "overlap_org": "朝阳市龙城区人民政府", "overlap_period": "", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S002"]},
            {"person": "刘凤玉", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "刘凤玉任副区长兼高新区管委会主任，李鼎任区长兼高新区党工委书记", "overlap_org": "朝阳高新技术产业开发区", "overlap_period": "", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S002"]},
            {"person": "张继业", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "张继业任副区长，李鼎任区长", "overlap_org": "朝阳市龙城区人民政府", "overlap_period": "", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S002"]},
            {"person": "于泓志", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "于泓志任副区长，李鼎任区长", "overlap_org": "朝阳市龙城区人民政府", "overlap_period": "", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S002"]},
            {"person": "于忠军", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "于忠军任副区长兼公安局长，李鼎任区长", "overlap_org": "朝阳市龙城区人民政府", "overlap_period": "", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S002"]},
            {"person": "张亚光", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "张亚光任副区长，李鼎任区长", "overlap_org": "朝阳市龙城区人民政府", "overlap_period": "", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S002"]},
            {"person": "杜剑", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "杜剑任副区长，李鼎任区长", "overlap_org": "朝阳市龙城区人民政府", "overlap_period": "", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S002"]},
        ],
        "governance_record": [
            {"period": "至今", "domain": "other", "achievement_or_event": "主持区政府全面工作，负责审计、规划、农业农村、生态环境工作", "role_in_event": "区长", "measurable_outcome": "", "location": "龙城区", "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        "professional_profile": {
            "primary_specializations": ["公共管理"],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "1985年4月出生，大学学历、公共管理硕士，晋升节奏因早期履历不足无法评估",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, career trajectory, and reported governance actions, not private psychological assessment.",
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月25日，公开渠道未发现李鼎的纪律处分、审计问题或负面媒体报道",
                "date": AS_OF,
                "confidence": "plausible",
                "source_ids": [],
            },
        ],
        "source_register": [
            {"id": "S001", "title": "龙城区第十次党代会开幕报道", "url": "https://www.cylc.gov.cn/html/LCQZF/202607/0178485573918912.html", "publisher": "龙城区人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认李鼎党代会执行主席、大会主持人身份"},
            {"id": "S002", "title": "龙城区人民政府-区长李鼎领导页", "url": "https://www.cylc.gov.cn/html/LCQZF/202109/0163168690280868.html", "publisher": "龙城区人民政府", "published_at": "2025-12-02", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "含简历、分工信息"},
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "李鼎的早期职业履历、具体毕业院校、出生地等信息需补充",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "李鼎的完整职业履历（任龙城区区长之前的职务）？",
                "why_it_matters": "缺少前任岗位信息，无法构建完整的职业晋升路径",
                "suggested_queries": ["李鼎 龙城区 任职 简历", "李鼎 朝阳 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "李鼎的具体毕业院校和专业？",
                "why_it_matters": "教育背景中的大学学历和公共管理硕士的具体院校信息待补充",
                "suggested_queries": ["李鼎 龙城区 教育背景"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "李鼎出生地和籍贯？",
                "why_it_matters": "影响身份去重和地域背景分析",
                "suggested_queries": ["李鼎 出生 籍贯"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": "李鼎的前任区长是谁？",
                "why_it_matters": "完整的区长更替链有助于分析领导班子变动",
                "suggested_queries": ["龙城区 前任区长", "龙城区 2023 2024 区长 任免"],
                "last_attempted": AS_OF,
            },
        ],
    }

    person_path = PERSONS_DIR / f"{TODAY}-辽宁省-朝阳市-区长-李鼎.json"
    with open(person_path, "w", encoding="utf-8") as f:
        json.dump(liding, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {person_path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print("=" * 60)
    print(f"Building {SLUG} leadership network")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Persons: {PERSONS_DIR}")
    print("=" * 60)

    # Write person JSON files
    print("\nWriting person JSON files...")
    write_person_json()

    # Run the standard build (DB + GEXF)
    print("\nRunning standard build...")
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

    # Verify outputs
    print("\n" + "=" * 60)
    print("Verification:")
    for label, path in [
        ("DB", DB_PATH),
        ("GEXF", GEXF_PATH),
    ]:
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        print(f"  {label}: {'✓' if exists else '✗'} ({size} bytes)")

    person_count = len(list(PERSONS_DIR.glob("*.json")))
    print(f"  Person JSON files: {person_count}")

    print("\nDone!")


if __name__ == "__main__":
    main()
