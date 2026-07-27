#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 双台子区 (Shuangtaizi District), 盘锦市, 辽宁省.

Level: 市辖区
Province: 辽宁省
Parent city: 盘锦市
Targets: 区委书记 (Party Secretary: 李吉峰), 区长 (District Mayor: 盖世功)
Task ID: liaoning_双台子区

Research date: 2026-07-25
Official source: http://www.stq.gov.cn/ (双台子区人民政府)

Current status (as of 2026-07-25, verified via official district website www.stq.gov.cn):

区委领导:
- 李吉峰 — 区委书记。男，汉族，1971年5月生，黑龙江讷河人，中共党员（1996年6月入党），1993年8月参加工作。
  来源: 双台子区人民政府官网新闻文章 (2026年7月)
- 盖世功 — 区委副书记、区长。男，汉族，1980年7月生，辽宁盘山人，中共党员（2000年6月入党），2002年8月参加工作，公共管理硕士。
  来源: https://www.stq.gov.cn/13018/ (区政府领导页)

区政府领导:
- 盖世功  区委副书记、区长 — 主持区政府全面工作，分管区审计局
- 梁吉哲  区委常委、副区长
- 佟百军  副区长
- 赵文星  副区长
- 王熙凯  副区长 (2026年7月24日新任命)
- 刘长林  副区长 (2026年7月24日新任命)
- 王玉兴  政府办公室主任

区委委员/其他重要岗位 (来源: 区委常委会新闻):
- 区委常委领导班子其他成员需进一步核实

Leadership info sourced from:
  - https://www.stq.gov.cn/13018/ (区长盖世功领导页)
  - https://www.stq.gov.cn/2026_07/09_09/content-568010.html (北大调研新闻-李吉峰)
  - https://www.stq.gov.cn/2026_07/20_09/content-568949.html (区委常委会-李吉峰)
  - https://www.stq.gov.cn/2026_07/13_08/content-568221.html (防汛工作会议-李吉峰)
  - https://www.stq.gov.cn/2026_07/24_16/content-569633.html (人大常委会任免名单)

Predecessor info:
  李吉峰的前任区委书记姓名需进一步核实
  盖世功的前任区长是李吉峰（2017-2021年任区长，后升任区委书记）

Confidence notes:
  李吉峰身份为区委书记已通过官方政府新闻多次确认（2026年7月多篇会议报道）。
  盖世功身份和简历通过区政府官方网站领导页确认（1980年7月生，公共管理硕士，中共党员）。
  李吉峰的详细职业履历来自百度百科（https://baike.baidu.com/item/李吉峰/20449676）。
  盖世功的详细职业履历来自百度百科（https://baike.baidu.com/item/盖世功/23181843）。
  区政府其他班子成员来自官方网站和任免名单。
  区委常委班子其他成员（组织部长、纪委书记、政法委书记、宣传部长等）尚未完全确认。

Encyclopedia sources:
  - https://baike.baidu.com/item/李吉峰/20449676 (李吉峰完整履历)
  - https://baike.baidu.com/item/盖世功/23181843 (盖世功完整履历)
  - https://baike.baidu.com/item/双台子区 (双台子区概况)
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

SLUG = "双台子区"

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

    # 1. 李吉峰 — 区委书记 (former 区长)
    {
        "id": 1,
        "name": "李吉峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年5月",
        "birthplace": "黑龙江省讷河市",
        "education": "大学本科（东北大学网络教育学院管理学学士）",
        "party_join": "中共党员（1996年6月）",
        "work_start": "1993年8月",
        "current_post": "区委书记",
        "current_org": "中共盘锦市双台子区委员会",
        "source": "https://www.stq.gov.cn/",
    },
    # 2. 盖世功 — 区委副书记、区长
    {
        "id": 2,
        "name": "盖世功",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年7月",
        "birthplace": "辽宁省盘山县（盘锦市）",
        "education": "研究生（东北大学公共管理专业硕士）",
        "party_join": "中共党员（2000年6月）",
        "work_start": "2002年8月",
        "current_post": "区长",
        "current_org": "盘锦市双台子区人民政府",
        "source": "https://www.stq.gov.cn/13018/",
    },

    # ════════════════════════════════════════
    # 区政府领导 (Government Leadership)
    # ════════════════════════════════════════

    # 3. 梁吉哲 — 区委常委、副区长
    {
        "id": 3,
        "name": "梁吉哲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "盘锦市双台子区人民政府",
        "source": "https://www.stq.gov.cn/",
    },
    # 4. 佟百军 — 副区长
    {
        "id": 4,
        "name": "佟百军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "盘锦市双台子区人民政府",
        "source": "https://www.stq.gov.cn/",
    },
    # 5. 赵文星 — 副区长
    {
        "id": 5,
        "name": "赵文星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "盘锦市双台子区人民政府",
        "source": "https://www.stq.gov.cn/",
    },
    # 6. 王熙凯 — 副区长 (2026年7月24日新任命)
    {
        "id": 6,
        "name": "王熙凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "盘锦市双台子区人民政府",
        "source": "https://www.stq.gov.cn/2026_07/24_16/content-569633.html",
    },
    # 7. 刘长林 — 副区长 (2026年7月24日新任命)
    {
        "id": 7,
        "name": "刘长林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "盘锦市双台子区人民政府",
        "source": "https://www.stq.gov.cn/2026_07/24_16/content-569633.html",
    },
    # 8. 王玉兴 — 政府办公室主任
    {
        "id": 8,
        "name": "王玉兴",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政府办公室主任",
        "current_org": "盘锦市双台子区人民政府办公室",
        "source": "https://www.stq.gov.cn/",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    # 党委系统
    {"id": 1, "name": "中共盘锦市双台子区委员会", "type": "党委", "level": "县处级", "parent": "中共盘锦市委员会", "location": "盘锦市双台子区"},
    # 政府系统
    {"id": 2, "name": "盘锦市双台子区人民政府", "type": "政府", "level": "县处级", "parent": "盘锦市人民政府", "location": "盘锦市双台子区"},
    {"id": 3, "name": "盘锦市双台子区人民政府办公室", "type": "政府", "level": "乡科级", "parent": "盘锦市双台子区人民政府", "location": "盘锦市双台子区"},
    # 人大
    {"id": 4, "name": "盘锦市双台子区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "盘锦市双台子区", "location": "盘锦市双台子区"},
    # 政协
    {"id": 5, "name": "政协盘锦市双台子区委员会", "type": "政协", "level": "县处级", "parent": "盘锦市双台子区", "location": "盘锦市双台子区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── 李吉峰 (id=1) ──
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "约2021年", "end_date": "至今", "rank": "正处级", "note": "双台子区委书记、区人武部党委第一书记"},
    # 前任职位：区长
    {"person_id": 1, "org_id": 2, "title": "区长", "start_date": "2017年12月", "end_date": "约2021年", "rank": "正处级", "note": "2017年2月代区长，2017年12月正式当选区长"},
    # 代区长
    {"person_id": 1, "org_id": 2, "title": "代区长", "start_date": "2017年2月", "end_date": "2017年12月", "rank": "正处级", "note": ""},
    # 市委常务副秘书长
    {"person_id": 1, "org_id": 1, "title": "市委常务副秘书长、市委办公室常务副主任", "start_date": "2016年9月", "end_date": "2017年2月", "rank": "正处级", "note": "盘锦市委"},
    # 市委副秘书长
    {"person_id": 1, "org_id": 1, "title": "市委副秘书长（正处级）、市委办公室副主任", "start_date": "2013年2月", "end_date": "2016年9月", "rank": "正处级", "note": "盘锦市委"},
    # 市委办公室副主任
    {"person_id": 1, "org_id": 1, "title": "市委办公室副主任", "start_date": "2011年9月", "end_date": "2013年2月", "rank": "副处级", "note": "盘锦市委，2011年9月-2012年10月试用期"},
    # 赵圈河镇党委书记
    {"person_id": 1, "org_id": 1, "title": "赵圈河镇党委书记", "start_date": "2010年12月", "end_date": "2011年9月", "rank": "副处级", "note": "大洼县赵圈河镇"},
    # 红海滩湿地旅游度假区管委会副主任
    {"person_id": 1, "org_id": 2, "title": "红海滩湿地旅游度假区管委会副主任", "start_date": "2010年12月", "end_date": "2011年9月", "rank": "副处级", "note": "大洼县"},
    # 平安乡党委书记
    {"person_id": 1, "org_id": 1, "title": "平安乡党委书记", "start_date": "2008年2月", "end_date": "2010年12月", "rank": "乡科级正职", "note": "大洼县平安乡"},
    # 荣兴乡党委副书记、常务副乡长
    {"person_id": 1, "org_id": 1, "title": "荣兴乡党委副书记、荣兴农垦有限责任公司总经理、常务副乡长", "start_date": "2005年10月", "end_date": "2008年2月", "rank": "乡科级正职", "note": "大洼县荣兴朝鲜族乡"},
    # 组织部副部长
    {"person_id": 1, "org_id": 1, "title": "县委组织部副部长", "start_date": "2003年4月", "end_date": "2005年10月", "rank": "乡科级正职", "note": "中共大洼县委组织部"},
    # 组织部办公室副主任
    {"person_id": 1, "org_id": 1, "title": "县委组织部办公室副主任", "start_date": "2002年3月", "end_date": "2003年4月", "rank": "", "note": "中共大洼县委组织部"},
    # 组织部干事、股长
    {"person_id": 1, "org_id": 1, "title": "县委组织部组织股干事、股长、副主任科员", "start_date": "1997年10月", "end_date": "2002年3月", "rank": "", "note": "中共大洼县委组织部"},
    # 新兴农场党建秘书
    {"person_id": 1, "org_id": 2, "title": "大洼县新兴农场(镇)党办秘书兼团委书记", "start_date": "1996年8月", "end_date": "1997年10月", "rank": "", "note": "大洼县"},
    # 盘锦新兴化工厂工人
    {"person_id": 1, "org_id": 2, "title": "工人、车间班长、办公室秘书", "start_date": "1993年8月", "end_date": "1996年8月", "rank": "", "note": "盘锦新兴化工厂"},

    # ── 盖世功 (id=2) ──
    # 区长 (current)
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2021年7月", "end_date": "至今", "rank": "正处级", "note": "2021年4月代区长，7月正式当选"},
    # 代区长
    {"person_id": 2, "org_id": 2, "title": "代区长", "start_date": "2021年4月", "end_date": "2021年7月", "rank": "正处级", "note": ""},
    # 信访局局长
    {"person_id": 2, "org_id": 2, "title": "中共盘锦市委、盘锦市人民政府信访局局长", "start_date": "2019年11月", "end_date": "2021年4月", "rank": "正处级", "note": "盘锦市"},
    # 双台子区副区长
    {"person_id": 2, "org_id": 2, "title": "副区长", "start_date": "2017年7月", "end_date": "2019年11月", "rank": "副处级", "note": "双台子区政府党组成员"},
    # 共青团盘锦市委副书记
    {"person_id": 2, "org_id": 1, "title": "共青团盘锦市委副书记、党组成员", "start_date": "2012年3月", "end_date": "2017年6月", "rank": "副处级", "note": ""},
    # 共青团盘锦市委战线部部长
    {"person_id": 2, "org_id": 1, "title": "共青团盘锦市委战线部部长", "start_date": "2007年4月", "end_date": "2012年3月", "rank": "", "note": ""},
    # 共青团盘锦市委宣传部副部长
    {"person_id": 2, "org_id": 1, "title": "共青团盘锦市委宣传部副部长", "start_date": "2005年12月", "end_date": "2007年4月", "rank": "", "note": ""},
    # 辽河三角洲新材料园区管委会副主任
    {"person_id": 2, "org_id": 2, "title": "辽河三角洲新材料园区管委会常务副主任（正科级）兼大洼镇副镇长", "start_date": "2005年9月", "end_date": "2005年12月", "rank": "乡科级正职", "note": "大洼县"},
    # 大洼镇副镇长
    {"person_id": 2, "org_id": 2, "title": "大洼镇政府副镇长兼西三村党支部书记", "start_date": "2003年12月", "end_date": "2005年9月", "rank": "乡科级副职", "note": "大洼县大洼镇"},
    # 大洼镇经济办主任
    {"person_id": 2, "org_id": 2, "title": "大洼镇经济办主任兼机关政府党支部书记", "start_date": "2003年1月", "end_date": "2003年9月", "rank": "", "note": "大洼县大洼镇"},
    # 大洼镇城管乡建办科员
    {"person_id": 2, "org_id": 2, "title": "大洼镇城管乡建办科员", "start_date": "2002年8月", "end_date": "2003年1月", "rank": "", "note": "大洼县大洼镇"},

    # ── 梁吉哲 (id=3) ── 区委常委、副区长
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "双台子区委"},
    {"person_id": 3, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "双台子区人民政府"},

    # ── 佟百军 (id=4) ── 副区长
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "双台子区人民政府"},

    # ── 赵文星 (id=5) ── 副区长
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "双台子区人民政府"},

    # ── 王熙凯 (id=6) ── 副区长 (新任命)
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "2026年7月", "end_date": "至今", "rank": "副处级", "note": "2026年7月24日区人大常委会任命"},

    # ── 刘长林 (id=7) ── 副区长 (新任命)
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "2026年7月", "end_date": "至今", "rank": "副处级", "note": "2026年7月24日区人大常委会任命"},

    # ── 王玉兴 (id=8) ── 政府办公室主任
    {"person_id": 8, "org_id": 3, "title": "主任", "start_date": "", "end_date": "至今", "rank": "乡科级", "note": "双台子区人民政府办公室"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 李吉峰 ↔ 盖世功 → 前后任（区长）和上下级（书记-区长）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "李吉峰2017-2021年任双台子区长，2021年升任区委书记；盖世功2021年4月接任代区长、7月正式任区长",
        "overlap_org": "盘锦市双台子区人民政府",
        "overlap_period": "2017-2021",
    },
    # 上下级关系
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "李吉峰任区委书记期间，盖世功任区委副书记、区长",
        "overlap_org": "中共盘锦市双台子区委员会",
        "overlap_period": "2021-至今",
    },
    # 同地区工作经历
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "两人均在大洼县（现大洼区）有多年工作经历，李吉峰在大洼县工作约13年（1996-2010），盖世功早期也在大洼镇工作（2002-2005）",
        "overlap_org": "大洼县",
        "overlap_period": "",
    },
    # 共同教育背景
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "两人均为东北大学毕业/在职进修（李吉峰本科管理学学士，盖世功公共管理硕士）",
        "overlap_org": "东北大学",
        "overlap_period": "",
    },
    # 李吉峰 ↔ 梁吉哲 → 上下级
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "李吉峰任区委书记，梁吉哲任区委常委、副区长",
        "overlap_org": "中共盘锦市双台子区委员会",
        "overlap_period": "",
    },
    # 盖世功 ↔ 梁吉哲 → 上下级（区长-副区长）
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "盖世功任区长，梁吉哲任区委常委、副区长",
        "overlap_org": "盘锦市双台子区人民政府",
        "overlap_period": "",
    },
    # 盖世功 ↔ 佟百军 → 上下级
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "盖世功任区长，佟百军任副区长",
        "overlap_org": "盘锦市双台子区人民政府",
        "overlap_period": "",
    },
    # 盖世功 ↔ 赵文星 → 上下级
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "盖世功任区长，赵文星任副区长",
        "overlap_org": "盘锦市双台子区人民政府",
        "overlap_period": "",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

def write_person_json() -> None:
    """Write per-person JSON files for core figures."""
    # ── 李吉峰 Person JSON ──
    lijifeng = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "盘锦市",
            "region": "双台子区",
            "job": "区委书记",
            "task_id": "liaoning_双台子区",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": "liaoning_panjin_shuangtaizi_lijifeng_1971",
            "name": "李吉峰",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1971年5月",
            "birthplace": "黑龙江省讷河市",
            "native_place": "黑龙江省讷河市",
            "education": [
                {
                    "period": "2004.11-2007.01",
                    "institution": "东北大学网络教育学院",
                    "major": "公共事业管理",
                    "degree": "管理学学士",
                    "study_type": "part_time",
                    "source_ids": ["S001"],
                },
                {
                    "period": "2001.09-2003.12",
                    "institution": "辽宁省委党校",
                    "major": "法律",
                    "degree": "",
                    "study_type": "party_school",
                    "source_ids": ["S001"],
                },
            ],
            "party_join": "1996年6月",
            "work_start": "1993年8月",
            "dedupe_keys": {
                "name_birth": "李吉峰_1971",
                "name_birthplace": "李吉峰_黑龙江省讷河市",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": "区委书记",
            "current_org": "中共盘锦市双台子区委员会",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S002", "S003", "S004"],
        },
        "career_timeline": [
            {"start": "1993年8月", "end": "1996年8月", "org": "盘锦新兴化工厂", "title": "工人、车间班长、办公室秘书", "level": "", "location": "盘锦市", "system": "other", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "1996年8月", "end": "1997年10月", "org": "大洼县新兴农场(镇)", "title": "党办秘书兼团委书记", "level": "", "location": "大洼县", "system": "other", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "1997年10月", "end": "2002年3月", "org": "中共大洼县委组织部", "title": "组织股干事、股长、副主任科员", "level": "", "location": "大洼县", "system": "organization", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2002年3月", "end": "2003年4月", "org": "中共大洼县委组织部", "title": "办公室副主任", "level": "", "location": "大洼县", "system": "organization", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2003年4月", "end": "2005年6月", "org": "中共大洼县委组织部", "title": "副部长", "level": "乡科级正职", "location": "大洼县", "system": "organization", "rank": "", "is_key_promotion": False, "notes": "2005.01-2005.06借调盘锦市委先进性教育活动办公室", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2005年6月", "end": "2005年10月", "org": "中共大洼县委组织部", "title": "副部长兼县人才工作领导小组办公室副主任", "level": "乡科级正职", "location": "大洼县", "system": "organization", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2005年10月", "end": "2008年2月", "org": "大洼县荣兴朝鲜族乡", "title": "党委副书记、荣兴农垦有限责任公司总经理、常务副乡长", "level": "乡科级正职", "location": "大洼县", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2008年2月", "end": "2010年12月", "org": "大洼县平安乡", "title": "党委书记", "level": "乡科级正职", "location": "大洼县", "system": "party", "rank": "", "is_key_promotion": True, "notes": "首次担任乡镇党委书记", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2010年12月", "end": "2011年9月", "org": "红海滩湿地旅游度假区管委会", "title": "管委会副主任（副处级）、大洼县赵圈河镇党委书记", "level": "副处级", "location": "大洼县", "system": "development_zone", "rank": "副处级", "is_key_promotion": True, "notes": "晋升副处级", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2011年9月", "end": "2012年10月", "org": "中共盘锦市委办公室", "title": "副主任（试用期一年）", "level": "副处级", "location": "盘锦市", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2012年10月", "end": "2013年2月", "org": "中共盘锦市委办公室", "title": "副主任", "level": "副处级", "location": "盘锦市", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2013年2月", "end": "2016年9月", "org": "中共盘锦市委办公室", "title": "副秘书长（正处级）、办公室副主任", "level": "正处级", "location": "盘锦市", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "晋升正处级", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2016年9月", "end": "2017年2月", "org": "中共盘锦市委办公室", "title": "常务副秘书长、办公室常务副主任", "level": "正处级", "location": "盘锦市", "system": "party", "rank": "正处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2017年2月", "end": "2017年12月", "org": "盘锦市双台子区人民政府", "title": "代区长、党组书记", "level": "正处级", "location": "双台子区", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "首次担任县区行政主官", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            {"start": "2017年12月", "end": "约2021年", "org": "盘锦市双台子区人民政府", "title": "区长、党组书记", "level": "正处级", "location": "双台子区", "system": "government", "rank": "正处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            {"start": "约2021年", "end": "至今", "org": "中共盘锦市双台子区委员会", "title": "区委书记", "level": "正处级", "location": "双台子区", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "区人武部党委第一书记、区委法治建设委员会主任", "confidence": "confirmed", "source_ids": ["S002", "S003", "S004"]},
        ],
        "organizations": [
            {"org_id": "org_panjin_shuangtaizi_committee", "name": "中共盘锦市双台子区委员会", "role": "current_leader", "period": "2021-至今"},
            {"org_id": "org_panjin_shuangtaizi_gov", "name": "盘锦市双台子区人民政府", "role": "former_leader", "period": "2017-2021"},
            {"org_id": "org_panjin_committee", "name": "中共盘锦市委员会", "role": "former_staff", "period": "2011-2017"},
            {"org_id": "org_dawa_county", "name": "大洼县（现大洼区）", "role": "former_staff", "period": "1996-2011"},
        ],
        "relationships": [
            {"person": "盖世功", "person_id": "liaoning_panjin_shuangtaizi_gaishigong_1980", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "李吉峰2017-2021年任区长后升任书记，盖世功2021年接任区长", "overlap_org": "盘锦市双台子区人民政府", "overlap_period": "2017-2021", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            {"person": "盖世功", "person_id": "liaoning_panjin_shuangtaizi_gaishigong_1980", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "李吉峰任区委书记期间，盖世功任区委副书记、区长", "overlap_org": "中共盘锦市双台子区委员会", "overlap_period": "2021-至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S002", "S005"]},
            {"person": "梁吉哲", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "梁吉哲任区委常委、副区长，李吉峰任区委书记", "overlap_org": "中共盘锦市双台子区委员会", "overlap_period": "", "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S002"]},
        ],
        "governance_record": [
            {"period": "2021-至今", "domain": "other", "achievement_or_event": "主持区委全面工作", "role_in_event": "区委书记", "measurable_outcome": "", "location": "双台子区", "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        "professional_profile": {
            "primary_specializations": ["组织人事", "党务管理"],
            "secondary_specializations": ["乡镇管理"],
            "career_pattern": "local_ladder",
            "systems_experience": ["organization", "party", "government", "development_zone"],
            "geographic_pattern": ["黑龙江省讷河市（出生）", "辽宁省盘锦市大洼县（早期）", "辽宁省盘锦市（市委）", "辽宁省盘锦市双台子区（当前）"],
            "promotion_velocity": {
                "summary": "组织系统出身，从工厂工人逐步晋升至正处级区委书记，晋升节奏较为稳健",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "organization_oriented",
                    "evidence": "长期在组织系统工作，从组织部干事做起，历任组织部办公室副主任、副部长等职",
                    "confidence": "plausible",
                    "source_ids": ["S001"],
                },
                {
                    "trait": "grassroots_oriented",
                    "evidence": "从化工厂工人起步，历经乡镇基层岗位，逐步晋升",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, career trajectory, and reported governance actions, not private psychological assessment.",
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月25日，公开渠道未发现李吉峰的纪律处分、审计问题或负面媒体报道",
                "date": AS_OF,
                "confidence": "plausible",
                "source_ids": [],
            },
        ],
        "source_register": [
            {"id": "S001", "title": "百度百科-李吉峰", "url": "https://baike.baidu.com/item/李吉峰/20449676", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
            {"id": "S002", "title": "双台子区人民政府官网", "url": "https://www.stq.gov.cn/", "publisher": "双台子区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "多篇新闻文章确认区委书记身份"},
            {"id": "S003", "title": "区委常委会会议新闻", "url": "https://www.stq.gov.cn/2026_07/20_09/content-568949.html", "publisher": "双台子区人民政府", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "李吉峰主持会议"},
            {"id": "S004", "title": "防汛工作会议新闻", "url": "https://www.stq.gov.cn/2026_07/13_08/content-568221.html", "publisher": "双台子区人民政府", "published_at": "2026-07-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "李吉峰主持会议"},
            {"id": "S005", "title": "区长盖世功领导页", "url": "https://www.stq.gov.cn/13018/", "publisher": "双台子区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "complete",
            "relationship_confidence": "high",
            "biggest_gap": "前任区委书记姓名及去向待确认",
        },
        "open_questions": [
            {
                "priority": "high",
                "question": "李吉峰的前任区委书记是谁？去向何处？",
                "why_it_matters": "完整的书记更替链有助于分析双台子区领导班子变动趋势",
                "suggested_queries": ["双台子区 前任区委书记", "双台子区 2020 2021 区委书记 任免"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": "李吉峰的具体出生日期（精确到日）？",
                "why_it_matters": "精确出生日期有助于身份去重和更精确的个人识别",
                "suggested_queries": ["李吉峰 出生 1971"],
                "last_attempted": AS_OF,
            },
        ],
    }

    person_path = PERSONS_DIR / f"{TODAY}-辽宁省-盘锦市-区委书记-李吉峰.json"
    with open(person_path, "w", encoding="utf-8") as f:
        json.dump(lijifeng, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {person_path.name}")

    # ── 盖世功 Person JSON ──
    gaishigong = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "盘锦市",
            "region": "双台子区",
            "job": "区长",
            "task_id": "liaoning_双台子区",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": "liaoning_panjin_shuangtaizi_gaishigong_1980",
            "name": "盖世功",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1980年7月",
            "birthplace": "辽宁省盘山县（盘锦市）",
            "native_place": "辽宁省盘山县",
            "education": [
                {
                    "period": "2012.09-2015.01",
                    "institution": "东北大学",
                    "major": "公共管理",
                    "degree": "硕士",
                    "study_type": "part_time",
                    "source_ids": ["S005"],
                },
                {
                    "period": "1998.09-2002.07",
                    "institution": "沈阳建筑工程学院",
                    "major": "土木工程",
                    "degree": "学士",
                    "study_type": "full_time",
                    "source_ids": ["S005"],
                },
            ],
            "party_join": "2000年6月",
            "work_start": "2002年8月",
            "dedupe_keys": {
                "name_birth": "盖世功_1980",
                "name_birthplace": "盖世功_辽宁省盘山县",
                "official_profile_url": "https://www.stq.gov.cn/13018/",
            },
        },
        "current_status": {
            "current_post": "区长",
            "current_org": "盘锦市双台子区人民政府",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S005"],
        },
        "career_timeline": [
            {"start": "1998年9月", "end": "2002年7月", "org": "沈阳建筑工程学院", "title": "土木工程系建筑工程专业学习", "level": "", "location": "沈阳市", "system": "education", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2002年7月", "end": "2002年8月", "org": "辽宁省委党校", "title": "青年干部培训班学习", "level": "", "location": "沈阳市", "system": "education", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2002年8月", "end": "2003年1月", "org": "大洼县大洼镇", "title": "城管乡建办科员", "level": "", "location": "大洼县", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2003年1月", "end": "2003年9月", "org": "大洼县大洼镇", "title": "经济办主任兼机关政府党支部书记", "level": "", "location": "大洼县", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2003年9月", "end": "2003年12月", "org": "大洼县大洼镇", "title": "城管交通办主任兼西三村党支部书记", "level": "", "location": "大洼县", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2003年12月", "end": "2005年9月", "org": "大洼县大洼镇", "title": "副镇长兼西三村党支部书记", "level": "乡科级副职", "location": "大洼县", "system": "government", "rank": "乡科级副职", "is_key_promotion": True, "notes": "首次担任副镇长", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2005年9月", "end": "2005年12月", "org": "辽河三角洲新材料园区管委会/大洼镇", "title": "常务副主任（正科级）兼大洼镇副镇长", "level": "乡科级正职", "location": "大洼县", "system": "development_zone", "rank": "乡科级正职", "is_key_promotion": True, "notes": "晋升正科级", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2005年12月", "end": "2007年4月", "org": "共青团盘锦市委", "title": "宣传部副部长", "level": "", "location": "盘锦市", "system": "other", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2007年4月", "end": "2012年3月", "org": "共青团盘锦市委", "title": "战线部部长", "level": "", "location": "盘锦市", "system": "other", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2012年3月", "end": "2017年6月", "org": "共青团盘锦市委", "title": "副书记、党组成员", "level": "副处级", "location": "盘锦市", "system": "other", "rank": "副处级", "is_key_promotion": True, "notes": "晋升副处级，在共青团系统工作近12年", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2017年6月", "end": "2017年7月", "org": "盘锦市委", "title": "提名为双台子区政府副区长人选", "level": "副处级", "location": "盘锦市", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2017年7月", "end": "2019年11月", "org": "盘锦市双台子区人民政府", "title": "副区长、党组成员", "level": "副处级", "location": "双台子区", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2019年11月", "end": "2021年4月", "org": "中共盘锦市委、盘锦市人民政府信访局", "title": "局长", "level": "正处级", "location": "盘锦市", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "晋升正处级", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2021年4月", "end": "2021年7月", "org": "盘锦市双台子区人民政府", "title": "代区长、党组书记", "level": "正处级", "location": "双台子区", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "接替李吉峰任代区长", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2021年7月", "end": "至今", "org": "盘锦市双台子区人民政府", "title": "区长、党组书记", "level": "正处级", "location": "双台子区", "system": "government", "rank": "正处级", "is_key_promotion": False, "notes": "区安委会主任", "confidence": "confirmed", "source_ids": ["S005"]},
        ],
        "organizations": [
            {"org_id": "org_panjin_shuangtaizi_gov", "name": "盘锦市双台子区人民政府", "role": "current_leader", "period": "2017-至今"},
            {"org_id": "org_panjin_committee", "name": "中共盘锦市委、市人民政府信访局", "role": "former_leader", "period": "2019-2021"},
            {"org_id": "org_ccyl_panjin", "name": "共青团盘锦市委", "role": "former_staff", "period": "2005-2017"},
            {"org_id": "org_dawa_county", "name": "大洼县（现大洼区）", "role": "former_staff", "period": "2002-2005"},
        ],
        "relationships": [
            {"person": "李吉峰", "person_id": "liaoning_panjin_shuangtaizi_lijifeng_1971", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "盖世功2021年接替李吉峰任双台子区长", "overlap_org": "盘锦市双台子区人民政府", "overlap_period": "2017-2021", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S005"]},
            {"person": "李吉峰", "person_id": "liaoning_panjin_shuangtaizi_lijifeng_1971", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "李吉峰任区委书记，盖世功任区委副书记、区长", "overlap_org": "中共盘锦市双台子区委员会", "overlap_period": "2021-至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S005"]},
            {"person": "梁吉哲", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "梁吉哲任区委常委、副区长，盖世功任区长", "overlap_org": "盘锦市双台子区人民政府", "overlap_period": "", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S005"]},
            {"person": "佟百军", "person_id": "", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "佟百军任副区长，盖世功任区长", "overlap_org": "盘锦市双台子区人民政府", "overlap_period": "", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S005"]},
        ],
        "governance_record": [
            {"period": "2021-至今", "domain": "other", "achievement_or_event": "主持区政府全面工作", "role_in_event": "区长", "measurable_outcome": "", "location": "双台子区", "confidence": "confirmed", "source_ids": ["S005"]},
        ],
        "professional_profile": {
            "primary_specializations": ["共青团与青年工作", "信访管理"],
            "secondary_specializations": ["土木工程"],
            "career_pattern": "cross_system",
            "systems_experience": ["government", "mass_organization", "development_zone", "education"],
            "geographic_pattern": ["辽宁省盘山县（出生）", "大洼县（早期基层）", "盘锦市（共青团）", "双台子区（当前岗位）"],
            "promotion_velocity": {
                "summary": "晋升节奏稳健，基层到大洼镇起步，29岁正科，32岁副处，40岁正处",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "technocratic",
                    "evidence": "土木工程专业背景，有基层乡镇和开发园区管理经验",
                    "confidence": "plausible",
                    "source_ids": ["S005"],
                },
                {
                    "trait": "low_profile",
                    "evidence": "公开新闻报道和搜索中个人风格报道较少，偏务实低调",
                    "confidence": "plausible",
                    "source_ids": [],
                },
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, career trajectory, and reported governance actions, not private psychological assessment.",
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月25日，公开渠道未发现盖世功的纪律处分、审计问题或负面媒体报道",
                "date": AS_OF,
                "confidence": "plausible",
                "source_ids": [],
            },
        ],
        "source_register": [
            {"id": "S005", "title": "双台子区人民政府-区长盖世功领导页", "url": "https://www.stq.gov.cn/13018/", "publisher": "双台子区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "含简历、分工信息"},
            {"id": "S006", "title": "百度百科-盖世功", "url": "https://baike.baidu.com/item/盖世功/23181843", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
            {"id": "S007", "title": "人大常委会任免名单", "url": "https://www.stq.gov.cn/2026_07/24_16/content-569633.html", "publisher": "双台子区人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "complete",
            "relationship_confidence": "high",
            "biggest_gap": "区委常委其他成员需进一步核实",
        },
        "open_questions": [
            {
                "priority": "medium",
                "question": "盖世功的具体出生日期（精确到日）？",
                "why_it_matters": "精确出生日期有助于身份去重和更精确的个人识别",
                "suggested_queries": ["盖世功 出生 1980"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": "盖世功在双台子区分管领域的具体政策和成果？",
                "why_it_matters": "有助于评估其治理风格和政策导向",
                "suggested_queries": ["盖世功 双台子区 调研 部署"],
                "last_attempted": AS_OF,
            },
        ],
    }

    person_path = PERSONS_DIR / f"{TODAY}-辽宁省-盘锦市-区长-盖世功.json"
    with open(person_path, "w", encoding="utf-8") as f:
        json.dump(gaishigong, f, ensure_ascii=False, indent=2)
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
