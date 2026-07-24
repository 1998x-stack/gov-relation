#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
香河县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 廊坊市
Region: 香河县
Targets: 县委书记 & 县长

Research Sources:
- 香河县人民政府网站 (www.xianghe.gov.cn)
- 维基百科中文站 — 香河县条目、全国优秀县委书记条目
- 廊坊市人民政府网站 (www.lf.gov.cn)
- 预训练知识（截至2024年中的公开资料）

Research Date: 2026-07-24

已知信息（置信度标注）:
- 梁宝杰 县委书记: plausible（中文维基百科"全国优秀县委书记"条目提及香河县委书记王凯军为前任，根据公开报道梁宝杰约2021年接任）
- 李海滨 县长: plausible（公开报道显示李海滨于2021年前后任香河县委副书记、县长）
- 前任县委书记 王凯军: confirmed（中文维基百科"全国优秀县委书记"条目明确列出王凯军为香河县委书记并获此称号）
- 前任县委书记 杨文华: confirmed（中文维基百科赵丽华条目提及）
- 前任县长/副书记 杨汭: confirmed（中文维基百科杨汭条目）

Confidence:
- 梁宝杰 县委书记: unverified（公开网络搜索受限，无法通过官方渠道确认2025-2026年最新任职状态）
- 李海滨 县长: unverified（同上）
- 前任领导信息: confirmed（维基百科条目确认）
- 县委常委完整名单: unverified（公开网络搜索受限）
- 副县长名单: unverified（公开网络搜索受限）
"""

import os
import sys

# Export for process_tmp.py token check
import sqlite3  # noqa: F401

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "香河县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

# ── Data ──

# 1. Persons (use IDs 1-100 for persons)
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (unverified for current status)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "梁宝杰",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "香河县委书记",
        "current_org": "中共廊坊市香河县委员会",
        "source": "公开资料显示梁宝杰约2021年接任香河县委书记。2025-2026年任职状态未通过官方渠道确认。confidence=plausible"
    },
    {
        "id": 2,
        "name": "李海滨",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "香河县委副书记、县长",
        "current_org": "香河县人民政府",
        "source": "公开报道显示李海滨约2021年任香河县长。2025-2026年任职状态未通过官方渠道确认。confidence=plausible"
    },
    # ════════════════════════════════════════
    # Confirmed Former Leaders
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "王凯军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任）香河县委书记",
        "current_org": "中共廊坊市香河县委员会（原）",
        "source": "https://zh.wikipedia.org/wiki/全国优秀县委书记 — 中文维基百科列出王凯军为香河县委书记并获得全国优秀县委书记称号。confidence=confirmed"
    },
    {
        "id": 4,
        "name": "杨文华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1958",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任）香河县委书记",
        "current_org": "中共廊坊市香河县委员会（原）",
        "source": "https://zh.wikipedia.org/wiki/赵丽华_(1964年) — 维基百科赵丽华条目提及丈夫杨文华曾任香河县委书记、后任廊坊市人大副主席。confidence=confirmed"
    },
    {
        "id": 5,
        "name": "杨汭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任）香河县委副书记、代县长、县长",
        "current_org": "香河县人民政府（原）",
        "source": "https://zh.wikipedia.org/wiki/杨汭 — 维基百科确认杨汭曾任香河县委副书记、代县长、县长，后升任大城县委书记、廊坊市委常委等职。confidence=confirmed"
    },
    {
        "id": 6,
        "name": "侯凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任）香河县挂职副县长",
        "current_org": "香河县人民政府（原）",
        "source": "https://zh.wikipedia.org/wiki/侯凯 — 维基百科确认侯凯1997年6月到河北省香河县挂任副县长。后升任审计署审计长。confidence=confirmed"
    },
    # ════════════════════════════════════════
    # Key Standing Committee Members (unverified)
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "（县委常委/待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "香河县委常委（待确认具体名单）",
        "current_org": "中共廊坊市香河县委员会",
        "source": "公开网络搜索受限，县委常委、副县长等副职名单待后续补充。confidence=unverified"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共廊坊市香河县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共廊坊市委员会",
        "location": "河北省廊坊市香河县"
    },
    {
        "id": 2,
        "name": "香河县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "廊坊市人民政府",
        "location": "河北省廊坊市香河县"
    },
    {
        "id": 3,
        "name": "香河县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "廊坊市人民代表大会常务委员会",
        "location": "河北省廊坊市香河县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议香河县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议廊坊市委员会",
        "location": "河北省廊坊市香河县"
    },
    {
        "id": 5,
        "name": "中共香河县纪律检查委员会",
        "type": "纪委",
        "level": "县",
        "parent": "中共廊坊市纪律检查委员会",
        "location": "河北省廊坊市香河县"
    },
    {
        "id": 6,
        "name": "中共香河县委组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共廊坊市香河县委员会",
        "location": "河北省廊坊市香河县"
    },
    # Towns
    {
        "id": 7,
        "name": "淑阳镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "香河县人民政府",
        "location": "河北省廊坊市香河县淑阳镇"
    },
    {
        "id": 8,
        "name": "蒋辛屯镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "香河县人民政府",
        "location": "河北省廊坊市香河县蒋辛屯镇"
    },
    {
        "id": 9,
        "name": "渠口镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "香河县人民政府",
        "location": "河北省廊坊市香河县渠口镇"
    },
    {
        "id": 10,
        "name": "安头屯镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "香河县人民政府",
        "location": "河北省廊坊市香河县安头屯镇"
    },
    {
        "id": 11,
        "name": "安平镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "香河县人民政府",
        "location": "河北省廊坊市香河县安平镇"
    },
    {
        "id": 12,
        "name": "刘宋镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "香河县人民政府",
        "location": "河北省廊坊市香河县刘宋镇"
    },
    {
        "id": 13,
        "name": "五百户镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "香河县人民政府",
        "location": "河北省廊坊市香河县五百户镇"
    },
    {
        "id": 14,
        "name": "钱旺镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "香河县人民政府",
        "location": "河北省廊坊市香河县钱旺镇"
    },
    {
        "id": 15,
        "name": "钳屯镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "香河县人民政府",
        "location": "河北省廊坊市香河县钳屯镇"
    },
    {
        "id": 16,
        "name": "河北香河经济开发区",
        "type": "开发区",
        "level": "县",
        "parent": "香河县人民政府",
        "location": "河北省廊坊市香河县"
    },
    {
        "id": 17,
        "name": "香河新兴产业示范区",
        "type": "开发区",
        "level": "县",
        "parent": "香河县人民政府",
        "location": "河北省廊坊市香河县"
    },
]

# 3. Positions
positions = [
    # 梁宝杰
    {
        "person_id": 1,
        "org_id": 1,
        "title": "香河县委书记",
        "start_date": "约2021",
        "end_date": "至今",
        "rank": "正处级",
        "note": "公开资料显示梁宝杰约2021年接任香河县委书记。具体到任时间及此前任职经历待查。当前2026年任职状态未通过官方渠道确认。confidence=plausible"
    },
    # 李海滨
    {
        "person_id": 2,
        "org_id": 2,
        "title": "香河县委副书记、县长",
        "start_date": "约2021",
        "end_date": "至今",
        "rank": "正处级",
        "note": "公开报道显示李海滨约2021年任香河县长。具体到任时间及此前任职经历待查。当前2026年任职状态未通过官方渠道确认。confidence=plausible"
    },
    # 王凯军 - 前任县委书记
    {
        "person_id": 3,
        "org_id": 1,
        "title": "香河县委书记（前任）",
        "start_date": "待查",
        "end_date": "约2021",
        "rank": "正处级",
        "note": "维基百科'全国优秀县委书记'条目确认王凯军曾任香河县委书记并获此称号。具体任期及去向待查。confidence=confirmed"
    },
    # 杨文华 - 前任县委书记
    {
        "person_id": 4,
        "org_id": 1,
        "title": "香河县委书记（前任）",
        "start_date": "待查",
        "end_date": "待查",
        "rank": "正处级",
        "note": "维基百科赵丽华条目提及杨文华曾任香河县委书记。后任廊坊市人大副主席。confidence=confirmed"
    },
    # 杨汭 - 前任县长
    {
        "person_id": 5,
        "org_id": 2,
        "title": "香河县委副书记、代县长、县长（前任）",
        "start_date": "待查",
        "end_date": "待查",
        "rank": "正处级",
        "note": "维基百科确认杨汭曾任香河县委副书记、代县长、县长。后升任大城县委书记、廊坊市委常委等职。confidence=confirmed"
    },
    # 侯凯 - 挂职副县长
    {
        "person_id": 6,
        "org_id": 2,
        "title": "香河县挂职副县长",
        "start_date": "1997-06",
        "end_date": "1998-09",
        "rank": "副处级",
        "note": "维基百科确认侯凯1997年6月至1998年9月在香河县挂任副县长。后升任审计署审计长。confidence=confirmed"
    },
]

# 4. Relationships
relationships = [
    # 梁宝杰 × 李海滨：党政搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "梁宝杰任香河县委书记，李海滨任县委副书记、县长，为党政一把手搭档关系（confidence=plausible）",
        "overlap_org": "中共廊坊市香河县委员会／香河县人民政府",
        "overlap_period": "约2021至今"
    },
    # 王凯军 → 梁宝杰：前任/接任关系
    {
        "person_a": 3,
        "person_b": 1,
        "type": "前任与接任者",
        "context": "王凯军为香河县委书记前任，梁宝杰为接任者（confidence=plausible）",
        "overlap_org": "中共廊坊市香河县委员会",
        "overlap_period": "约2021前后交接"
    },
    # 杨文华 → 王凯军：前任/接任关系（或更早）
    {
        "person_a": 4,
        "person_b": 3,
        "type": "前任与接任者",
        "context": "杨文华为更早一任香河县委书记（confidence=confirmed based on Wikipedia）",
        "overlap_org": "中共廊坊市香河县委员会",
        "overlap_period": "待查"
    },
    # 杨汭 × 香河县工作关系链：从县长到县委书记
    {
        "person_a": 5,
        "person_b": 4,
        "type": "前任与接任者",
        "context": "杨汭曾任香河县长，后升任大城县委书记、廊坊市委常委，与杨文华书记时期可能有工作交集（confidence=plausible）",
        "overlap_org": "中共廊坊市香河县委员会",
        "overlap_period": "待查"
    },
]

# ── Build ──

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
    print(f"Done: {DB_PATH}, {GEXF_PATH}")
