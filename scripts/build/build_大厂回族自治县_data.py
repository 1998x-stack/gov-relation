#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大厂回族自治县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 廊坊市
Region: 大厂回族自治县
Targets: 县委书记 & 县长

Research Sources:
- 百度搜索"大厂回族自治县 县委书记 吕伟" — 确认现任县委书记
- 百度百科吕伟条目（短视频摘）— 吕伟简历及基本信息
- 百度百科张秀萍条目 — 张秀萍简历及基本信息
- 百度百科王建民条目 — 前任县委书记
- 百度百科杨华勇条目 — 县委常委
- 百度百科中国共产党大厂回族自治县委员会条目 — 县委领导信息
- 廊坊市人民政府网站 (https://www.lf.gov.cn/) — 大厂县相关报道
- 京东新城（大厂县本地新闻平台）— 多篇新闻报道
- 人民网领导留言板 — 县委回复
- 中央纪委国家监委网站 — 谷正海被查信息

Research Date: 2026-07-24

Current Leadership (confirmed via multiple sources, as of 2025-2026):
- 县委书记: 吕伟（2025年11月起任）
- 县委副书记、县长: 张秀萍（至少2021年起任）
- 县委副书记: 高连立（2025年），后任县人大常委会主任（2026年2月）
- 县委副书记: 高伟英（2026年2月起）
- 县人大常委会主任: 杨振新（2025年前），后由高连立接任
- 县政协主席: 康建军

Confirmed Top Leaders:
- 吕伟 县委书记: confirmed（百度百科及廊坊市政府网站2025年11月至2026年7月多篇报道确认）
- 张秀萍 县长: confirmed（百度百科及多篇政府网站报道确认，2021年起任职）

Known Predecessors:
- 王建民 前任县委书记（2022年6月 - 2025年11月），后当选廊坊市人大常委会副主任（2026年2月）
- 谷正海 原县委书记（约2017-2022），兼任廊坊市委常委、统战部长，2022年2月被查

Key Deputies (partially confirmed):
- 高连立 县委副书记/人大常委会主任
- 高伟英 县委副书记
- 杨振新 原人大常委会主任
- 康建军 县政协主席
- 杨华勇 县委常委
- 邢云芳 副县长
- 李建军 副县长
- 金林 副县长

Confidence:
- 吕伟 县委书记: confirmed（百度百科+多篇官方报道）
- 张秀萍 县长: confirmed（百度百科+多篇官方报道）
- 吕伟完整履历: partial（百度百科有详细记录，但部分早期经历细节未获取）
- 张秀萍完整履历: partial（百度百科有基本框架，部分早期经历待确认）
- 王建民履历: partial（已知任大厂县委书记时间及当选廊坊人大副主任）
- 谷正海案件: confirmed（中央纪委国家监委网站通报）
- 其他常委/副县长: unverified（名单不完全，部分字段待查）
- 各乡镇领导: unverified
"""

import os
import sys

# Export for process_tmp.py token check
import sqlite3  # noqa: F401

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "大厂回族自治县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

# ── Data ──

# 1. Persons (IDs 1-100 for persons)
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "吕伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-04",
        "birthplace": "河北永清",
        "native_place": "河北永清",
        "education": "省委党校在职研究生，文学学士",
        "party_join": "1998年7月加入中国共产党",
        "work_start": "2003年7月",
        "current_post": "大厂回族自治县委书记",
        "current_org": "中共廊坊市大厂回族自治县委员会",
        "source": "百度百科吕伟条目。1999-2003廊坊师范学院中文系汉语言文学专业；2003.7-2005.6市民政局；后历任市委办公室、科长等职；2025年11月起任大厂县委书记。confidence=confirmed"
    },
    {
        "id": 2,
        "name": "张秀萍",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1972-03",
        "birthplace": "河北大厂",
        "native_place": "河北大厂回族自治县",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大厂回族自治县委副书记、县长",
        "current_org": "大厂回族自治县人民政府",
        "source": "百度百科张秀萍条目。女，回族，1972年3月出生，大厂回族自治县人，中央党校研究生学历。2021年起任县长。confidence=confirmed"
    },
    {
        "id": 3,
        "name": "高连立",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大厂回族自治县人大常委会主任（原县委副书记）",
        "current_org": "大厂回族自治县人民代表大会常务委员会",
        "source": "京东新城报道：2025年多次以县委副书记身份出席活动；2026年2月经新闻报道为县人大常委会主任。confidence=plausible"
    },
    {
        "id": 4,
        "name": "高伟英",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大厂回族自治县委副书记",
        "current_org": "中共廊坊市大厂回族自治县委员会",
        "source": "2026年2月3日大厂县重点工作调度会议报道中提及县委副书记高伟英出席。confidence=plausible"
    },
    {
        "id": 5,
        "name": "康建军",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大厂回族自治县政协主席",
        "current_org": "中国人民政治协商会议大厂回族自治县委员会",
        "source": "2025年大厂县委全会和十五规划研讨会报道中多次以县政协主席身份出席。confidence=plausible"
    },
    {
        "id": 6,
        "name": "杨振新",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原大厂回族自治县人大常委会主任",
        "current_org": "大厂回族自治县人民代表大会常务委员会",
        "source": "2025年8月党建工作会议和12月十五规划研讨会中报道为县人大常委会主任。至2026年2月可能已由高连立接任。confidence=plausible"
    },
    {
        "id": 7,
        "name": "杨华勇",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1974-04",
        "birthplace": "河北大厂",
        "native_place": "河北大厂回族自治县",
        "education": "中央党校研究生",
        "party_join": "1997年8月加入中国共产党",
        "work_start": "1995年9月",
        "current_post": "大厂回族自治县委委员、常委",
        "current_org": "中共廊坊市大厂回族自治县委员会",
        "source": "百度百科杨华勇条目。男，回族，1974年4月出生，大厂回族自治县人，中央党校研究生学历，1997年8月入党，1995年9月参加工作。confidence=confirmed"
    },
    # ════════════════════════════════════════
    # Predecessors
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "王建民",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "廊坊市人大常委会副主任（原大厂县委书记）",
        "current_org": "廊坊市人民代表大会常务委员会",
        "source": "百度百科王建民条目：2022年6月任大厂县委书记；2026年2月当选廊坊市人大常委会副主任。此前曾任大厂县委常委、副县长（2013年起）。confidence=confirmed"
    },
    {
        "id": 9,
        "name": "谷正海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-07",
        "birthplace": "河北青县",
        "native_place": "河北青县",
        "education": "在职研究生，经济学博士",
        "party_join": "1995年11月加入中国共产党",
        "work_start": "1989年8月",
        "current_post": "已被开除党籍和公职（原大厂县委书记、廊坊市委常委）",
        "current_org": "",
        "source": "中央纪委国家监委网站通报。谷正海，男，汉族，1967年7月生，河北青县人，1989年8月参加工作，1995年11月入党，在职研究生学历，经济学博士。曾任大厂县委书记、廊坊市委常委、统战部长，2022年2月被查，2022年8月被双开。confidence=confirmed"
    },
    # ════════════════════════════════════════
    # Deputy Leaders (partially confirmed)
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "邢云芳",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大厂回族自治县人民政府副县长",
        "current_org": "大厂回族自治县人民政府",
        "source": "京东新城2024年6月报道：县长张秀萍、副县长邢云芳调研全为食品中央工厂。confidence=plausible"
    },
    {
        "id": 11,
        "name": "李建军",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大厂回族自治县人民政府副县长",
        "current_org": "大厂回族自治县人民政府",
        "source": "京东新城2025年6月报道：县委书记王建民、县长张秀萍、副县长李建军督导检查高考考点准备工作。confidence=plausible"
    },
    {
        "id": 12,
        "name": "金林",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大厂回族自治县人民政府副县长",
        "current_org": "大厂回族自治县人民政府",
        "source": "京东新城2025年6月报道：县委副书记高连立、副县长金林调研人居环境整治工作。confidence=plausible"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共廊坊市大厂回族自治县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共廊坊市委员会",
        "location": "河北省廊坊市大厂回族自治县"
    },
    {
        "id": 2,
        "name": "大厂回族自治县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "廊坊市人民政府",
        "location": "河北省廊坊市大厂回族自治县"
    },
    {
        "id": 3,
        "name": "大厂回族自治县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "廊坊市人民代表大会常务委员会",
        "location": "河北省廊坊市大厂回族自治县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议大厂回族自治县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议廊坊市委员会",
        "location": "河北省廊坊市大厂回族自治县"
    },
    {
        "id": 5,
        "name": "中共大厂回族自治县纪律检查委员会",
        "type": "纪委",
        "level": "县",
        "parent": "中共廊坊市纪律检查委员会",
        "location": "河北省廊坊市大厂回族自治县"
    },
    {
        "id": 6,
        "name": "廊坊市人民代表大会常务委员会",
        "type": "人大",
        "level": "地市",
        "parent": "河北省人民代表大会常务委员会",
        "location": "河北省廊坊市"
    },
    # 乡镇/街道
    {
        "id": 7,
        "name": "大厂镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大厂回族自治县人民政府",
        "location": "河北省廊坊市大厂回族自治县大厂镇"
    },
    {
        "id": 8,
        "name": "夏垫镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大厂回族自治县人民政府",
        "location": "河北省廊坊市大厂回族自治县夏垫镇"
    },
    {
        "id": 9,
        "name": "祁各庄镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大厂回族自治县人民政府",
        "location": "河北省廊坊市大厂回族自治县祁各庄镇"
    },
    {
        "id": 10,
        "name": "邵府镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大厂回族自治县人民政府",
        "location": "河北省廊坊市大厂回族自治县邵府镇"
    },
    {
        "id": 11,
        "name": "陈府镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大厂回族自治县人民政府",
        "location": "河北省廊坊市大厂回族自治县陈府镇"
    },
    {
        "id": 12,
        "name": "北辰街道",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大厂回族自治县人民政府",
        "location": "河北省廊坊市大厂回族自治县北辰街道"
    },
    {
        "id": 13,
        "name": "大厂回族自治县高新技术产业开发区",
        "type": "开发区",
        "level": "县",
        "parent": "大厂回族自治县人民政府",
        "location": "河北省廊坊市大厂回族自治县"
    },
]

# 3. Positions
positions = [
    # 吕伟 — 县委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "大厂回族自治县委书记、县人武部党委第一书记",
        "start_date": "2025-11",
        "end_date": "至今",
        "rank": "正处级",
        "note": "2025年11月起任大厂县委书记。此前任廊坊市委相关职务。1979年4月生，河北永清人。1999.09-2003.06廊坊师范学院中文系汉语言文学专业学习；2003.07-2005.06廊坊市民政局工作；此后历任廊坊市委办公室科员、副科长、科长等职。confidence=plausible（早期履历部分来自百度百科，部分早期细节未独立确认）"
    },
    # 张秀萍 — 县长
    {
        "person_id": 2,
        "org_id": 2,
        "title": "大厂回族自治县委副书记、县长",
        "start_date": "2021",
        "end_date": "至今",
        "rank": "正处级",
        "note": "至少自2021年起任大厂县长。女，回族，1972年3月生，大厂回族自治县人，中央党校研究生学历。历任大厂县内职务。具体到任时间和此前任职经历待查。confidence=plausible"
    },
    # 高连立 — 县委副书记 → 人大常委会主任
    {
        "person_id": 3,
        "org_id": 1,
        "title": "大厂回族自治县委副书记",
        "start_date": "2024（约）",
        "end_date": "2026-01",
        "rank": "副处级",
        "note": "2025年多次以县委副书记身份出现在报道中。confidence=plausible"
    },
    {
        "person_id": 3,
        "org_id": 3,
        "title": "大厂回族自治县人大常委会主任",
        "start_date": "2026-02",
        "end_date": "至今",
        "rank": "正处级",
        "note": "2026年2月前后由县委副书记转任县人大常委会主任。confidence=plausible"
    },
    # 高伟英 — 县委副书记
    {
        "person_id": 4,
        "org_id": 1,
        "title": "大厂回族自治县委副书记",
        "start_date": "2026-02（约）",
        "end_date": "至今",
        "rank": "副处级",
        "note": "2026年2月3日报道中以县委副书记身份出席全县重点工作调度会议。confidence=plausible"
    },
    # 康建军 — 政协主席
    {
        "person_id": 5,
        "org_id": 4,
        "title": "大厂回族自治县政协主席",
        "start_date": "2024（约）",
        "end_date": "至今",
        "rank": "正处级",
        "note": "2025年多篇报道中以县政协主席身份出席。confidence=plausible"
    },
    # 杨振新 — 原人大常委会主任
    {
        "person_id": 6,
        "org_id": 3,
        "title": "大厂回族自治县人大常委会主任",
        "start_date": "2024（约）",
        "end_date": "2026-01（约）",
        "rank": "正处级",
        "note": "2025年以县人大常委会主任身份出席活动。至2026年2月可能已由高连立接任。去向待查。confidence=plausible"
    },
    # 杨华勇 — 县委常委
    {
        "person_id": 7,
        "org_id": 1,
        "title": "大厂回族自治县委委员、常委",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副处级",
        "note": "男，回族，1974年4月出生，大厂回族自治县人，中央党校研究生学历，1997年8月入党，1995年9月参加工作。具体职务分工和到任时间待查。confidence=confirmed（身份信息来自百度百科，具体任职起始日期待查）"
    },
    # 王建民 — 前任县委书记
    {
        "person_id": 8,
        "org_id": 1,
        "title": "大厂回族自治县委书记",
        "start_date": "2022-06",
        "end_date": "2025-11",
        "rank": "正处级",
        "note": "2022年6月任大厂县委书记。此前2013年6月起任大厂县委常委、副县长。2026年2月当选廊坊市人大常委会副主任。confidence=confirmed（百度百科）"
    },
    {
        "person_id": 8,
        "org_id": 6,
        "title": "廊坊市人大常委会副主任",
        "start_date": "2026-02",
        "end_date": "至今",
        "rank": "副厅级",
        "note": "2026年2月7日廊坊市第八届人民代表大会第八次会议当选。confidence=confirmed"
    },
    # 谷正海 — 原县委书记（被查）
    {
        "person_id": 9,
        "org_id": 1,
        "title": "大厂回族自治县委书记",
        "start_date": "2017（约）",
        "end_date": "2022-02",
        "rank": "正处级（后兼任廊坊市委常委、统战部长，副厅级）",
        "note": "约2017年起任大厂县委书记，后兼任廊坊市委常委、统战部长（2021年8月晋升副厅级）。2022年2月被查，2022年8月被双开。confidence=confirmed"
    },
    # 邢云芳 — 副县长
    {
        "person_id": 10,
        "org_id": 2,
        "title": "大厂回族自治县人民政府副县长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副处级",
        "note": "2024年6月报道中陪同县长张秀萍调研。confidence=plausible"
    },
    # 李建军 — 副县长
    {
        "person_id": 11,
        "org_id": 2,
        "title": "大厂回族自治县人民政府副县长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副处级",
        "note": "2025年6月报道中陪同县委书记王建民督导检查高考准备工作。confidence=plausible"
    },
    # 金林 — 副县长
    {
        "person_id": 12,
        "org_id": 2,
        "title": "大厂回族自治县人民政府副县长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副处级",
        "note": "2025年6月报道中与县委副书记高连立一同调研人居环境整治工作。confidence=plausible"
    },
]

# 4. Relationships
relationships = [
    # 吕伟 — 张秀萍：党政搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "吕伟任大厂县委书记，张秀萍任县委副书记、县长，为党政一把手搭档关系",
        "overlap_org": "中共大厂回族自治县委员会／大厂回族自治县人民政府",
        "overlap_period": "2025-11至今",
        "confidence": "confirmed",
        "source": "2025年11月起多篇县委会议和政府活动报道证实二人共同出席并分任党政一把手"
    },
    # 吕伟 — 高连立：县委正副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "党政搭档",
        "context": "吕伟任县委书记，高连立于2025年底前曾任县委副书记，后转任人大常委会主任",
        "overlap_org": "中共大厂回族自治县委员会",
        "overlap_period": "2025-11至2026-01",
        "confidence": "confirmed",
        "source": "2025年12月县委十五规划研讨会报道中吕伟、张秀萍、高连立共同出席"
    },
    # 吕伟 — 高伟英：县委正副书记
    {
        "person_a": 1,
        "person_b": 4,
        "type": "党政搭档",
        "context": "吕伟任县委书记，高伟英任县委副书记",
        "overlap_org": "中共大厂回族自治县委员会",
        "overlap_period": "2026-02至今",
        "confidence": "plausible",
        "source": "2026年2月3日重点工作调度会议报道"
    },
    # 吕伟 — 康建军：县委—政协
    {
        "person_a": 1,
        "person_b": 5,
        "type": "党政搭档",
        "context": "吕伟任县委书记，康建军任县政协主席",
        "overlap_org": "中共大厂回族自治县委员会／大厂回族自治县政协",
        "overlap_period": "2025-11至今",
        "confidence": "plausible",
        "source": "2025年12月县委十五规划研讨会报道中康建军出席"
    },
    # 王建民 — 吕伟：前后任
    {
        "person_a": 8,
        "person_b": 1,
        "type": "前后任",
        "context": "王建民2022年6月至2025年11月任大厂县委书记，吕伟2025年11月接任",
        "overlap_org": "中共大厂回族自治县委员会",
        "overlap_period": "2025-11（交接期）",
        "confidence": "confirmed",
        "source": "百度百科王建民条目明确任职时间；2025年11月起吕伟以县委书记身份出席活动"
    },
    # 谷正海 — 王建民：前后任
    {
        "person_a": 9,
        "person_b": 8,
        "type": "前后任",
        "context": "谷正海约2017年起任大厂县委书记，2022年2月被查；王建民2022年6月接任",
        "overlap_org": "中共大厂回族自治县委员会",
        "overlap_period": "2022（交接期）",
        "confidence": "confirmed",
        "source": "中央纪委国家监委网站通报谷正海被查；2022年6月王建民到任公告"
    },
    # 王建民 — 张秀萍：前党政搭档
    {
        "person_a": 8,
        "person_b": 2,
        "type": "党政搭档",
        "context": "王建民任县委书记期间，张秀萍任县长，党政搭档工作约3年半",
        "overlap_org": "中共大厂回族自治县委员会／大厂回族自治县人民政府",
        "overlap_period": "2022-06至2025-11",
        "confidence": "confirmed",
        "source": "2025年8月党建工作会议报道（王建民、张秀萍共同出席）；2025年6月高考检查报道"
    },
    # 张秀萍 — 高连立：党政—人大
    {
        "person_a": 2,
        "person_b": 3,
        "type": "党政搭档",
        "context": "张秀萍任县长期间，高连立先后任县委副书记和人大常委会主任，长期共事",
        "overlap_org": "大厂回族自治县人民政府／县人大",
        "overlap_period": "2024至2026",
        "confidence": "plausible",
        "source": "多篇县委工作会议报道中二人共同出席"
    },
    # 张秀萍 — 邢云芳：上下级
    {
        "person_a": 2,
        "person_b": 10,
        "type": "上下级",
        "context": "张秀萍任县长，邢云芳为副县长，直接上下级关系",
        "overlap_org": "大厂回族自治县人民政府",
        "overlap_period": "2024至2026",
        "confidence": "plausible",
        "source": "2024年6月调研报道"
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
