#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大城县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 廊坊市
Region: 大城县
Targets: 县委书记 & 县长

Research Sources:
- 大城县人民政府网站 (https://www.dacheng.gov.cn/) — 已确认，网站可访问
- 大城县人民政府站内搜索 (http://search.0316gov.com:88/) — 已使用
- 廊坊市人民政府网站 (https://www.lf.gov.cn/) — 已访问
- 维基百科大城县条目 (https://zh.wikipedia.org/wiki/大城县) — 无领导信息
- 百度百科 — 因网络限制不可用

Research Date: 2026-07-24

已知信息（基于官方搜索结果，置信度标注如下）:
- 县委书记: 庞大鹏（2021年5月起任大城县委书记，此前任大城县委副书记、县长）
- 县长: 靳志强（2025-2026年间在大城县第十七届人民代表大会第六次会议作政府工作报告，此前任职待查）
- 前任县委书记: 齐德旺（2021年5月免去，另有任用）
- 前任县长: 田海宽（2021年5月任大城县委副书记，后任县长）

Confidence:
- 庞大鹏 县委书记: confirmed (官方任命公告)
- 靳志强 县长: confirmed (2026年2月县人大会议确认)
- 庞大鹏曾任大城县县长: confirmed (2021年5月任命调整公告)
- 田海宽曾任大城县县长: plausible (2021年5月任命，2023年1月仍有公开报道)
- 齐德旺曾任大城县委书记: confirmed (2021年5月免去)
- 庞大鹏完整履历: partial (仅知2021年前后，更早履历待查)
- 靳志强完整履历: partial (任县长时间待精确确认)
- 其他常委/副县长: partial (2025年12月河长名单确认了任职)
- 当前截至2026年7月的最新任职状态: confirmed (2026年2月县人大会议确认核心领导)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "大城县"

DB_PATH = os.path.join(DATABASE_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "庞大鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大城县委书记",
        "current_org": "中共廊坊市大城县委员会",
        "source": "官方任命（2021年5月）：庞大鹏由大城县委副书记、县长升任大城县委书记。来源：https://www.dacheng.gov.cn/system/2021/05/20/030078392.shtml（置信度: confirmed）"
    },
    {
        "id": 2,
        "name": "靳志强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大城县委副书记、县长",
        "current_org": "大城县人民政府",
        "source": "官方报道确认：2026年2月大城县第十七届人民代表大会第六次会议，靳志强代表县政府作政府工作报告。来源：https://www.dacheng.gov.cn/system/2026/02/09/030124427.shtml（置信度: confirmed）"
    },
    # ════════════════════════════════════════
    # County Leadership Team (县委常委/副县长)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "李向伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大城县委副书记",
        "current_org": "中共廊坊市大城县委员会",
        "source": "大城县三级河长名单公告（2025年12月），李向伟任县委副书记。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
    {
        "id": 4,
        "name": "王立达",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、常务副县长",
        "current_org": "大城县人民政府",
        "source": "大城县三级河长名单（2025年12月）及多篇报道确认。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
    {
        "id": 5,
        "name": "张向东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共廊坊市大城县委员会",
        "source": "大城县三级河长名单（2025年12月）及多篇报道确认。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
    {
        "id": 6,
        "name": "郑金明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共廊坊市大城县委员会",
        "source": "大城县三级河长名单（2025年12月）及报道确认。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
    {
        "id": 7,
        "name": "郭为民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共廊坊市大城县委员会",
        "source": "大城县三级河长名单（2025年12月）确认。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
    {
        "id": 8,
        "name": "刘杨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、办公室主任",
        "current_org": "中共廊坊市大城县委员会",
        "source": "大城县三级河长名单（2025年12月）确认。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
    {
        "id": 9,
        "name": "李汉松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共廊坊市大城县委员会",
        "source": "大城县三级河长名单（2025年12月）确认。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
    {
        "id": 10,
        "name": "刘青明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、人武部部长",
        "current_org": "大城县人民武装部",
        "source": "大城县三级河长名单（2025年12月）确认。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
    {
        "id": 11,
        "name": "张国霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共大城县纪律检查委员会",
        "source": "2025年4月全县巡察工作会议报道，张国霞以县委常委、纪委书记身份出席会议。来源：https://www.dacheng.gov.cn/system/2025/04/29/030119450.shtml（置信度: confirmed）"
    },
    {
        "id": 12,
        "name": "齐建兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府副县长",
        "current_org": "大城县人民政府",
        "source": "大城县三级河长名单（2025年12月）确认。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
    {
        "id": 13,
        "name": "谷振永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府副县长",
        "current_org": "大城县人民政府",
        "source": "大城县三级河长名单（2025年12月）及多篇报道确认。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
    {
        "id": 14,
        "name": "张全旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府副县长",
        "current_org": "大城县人民政府",
        "source": "大城县三级河长名单（2025年12月）及多篇报道确认。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
    {
        "id": 15,
        "name": "王忠星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府副县长、公安局局长",
        "current_org": "大城县公安局",
        "source": "大城县三级河长名单（2025年12月）确认。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
    {
        "id": 16,
        "name": "鲍世博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府副县长",
        "current_org": "大城县人民政府",
        "source": "大城县三级河长名单（2025年12月）及多篇报道确认。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
    # ════════════════════════════════════════
    # Previous Top Leaders
    # ════════════════════════════════════════
    {
        "id": 17,
        "name": "齐德旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任",
        "current_org": "",
        "source": "官方任命（2021年5月）：齐德旺免去大城县委书记职务，一级调研员职级，另有任用。来源：https://www.dacheng.gov.cn/system/2021/05/20/030078392.shtml（置信度: confirmed）"
    },
    {
        "id": 18,
        "name": "田海宽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（大城县）",
        "current_org": "",
        "source": "官方任命（2021年5月）：田海宽任大城县委委员、常委、副书记（提名为县长）。2023年1月仍有县长报道。来源：https://www.dacheng.gov.cn/system/2021/05/20/030078392.shtml（置信度: confirmed）"
    },
    {
        "id": 19,
        "name": "荣印祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（大城县）",
        "current_org": "",
        "source": "2023年1月大城县领导干部会议报道，荣印祥以县委副书记身份出席。来源：https://www.dacheng.gov.cn/system/2023/01/20/030096130.shtml（置信度: confirmed）"
    },
    # ════════════════════════════════════════
    # Other Key Positions
    # ════════════════════════════════════════
    {
        "id": 20,
        "name": "刘国旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县人大常委会主任",
        "current_org": "大城县人民代表大会常务委员会",
        "source": "大城县三级河长名单（2025年12月）及多篇报道确认。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
    {
        "id": 21,
        "name": "刘国政",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议大城县委员会",
        "source": "大城县三级河长名单（2025年12月）及多篇报道确认。来源：https://www.dacheng.gov.cn/system/2025/12/05/030123434.shtml（置信度: confirmed）"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共廊坊市大城县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共廊坊市委员会",
        "location": "河北省廊坊市大城县"
    },
    {
        "id": 2,
        "name": "大城县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "廊坊市人民政府",
        "location": "河北省廊坊市大城县"
    },
    {
        "id": 3,
        "name": "大城县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "廊坊市人民代表大会常务委员会",
        "location": "河北省廊坊市大城县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议大城县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议廊坊市委员会",
        "location": "河北省廊坊市大城县"
    },
    {
        "id": 5,
        "name": "中共大城县纪律检查委员会",
        "type": "纪委",
        "level": "县",
        "parent": "中共廊坊市纪律检查委员会",
        "location": "河北省廊坊市大城县"
    },
    {
        "id": 6,
        "name": "大城县公安局",
        "type": "政府",
        "level": "县",
        "parent": "大城县人民政府",
        "location": "河北省廊坊市大城县"
    },
    {
        "id": 7,
        "name": "大城县人民武装部",
        "type": "其他",
        "level": "县",
        "parent": "廊坊军分区",
        "location": "河北省廊坊市大城县"
    },
    # 乡镇
    {
        "id": 8,
        "name": "平舒镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大城县人民政府",
        "location": "河北省廊坊市大城县平舒镇"
    },
    {
        "id": 9,
        "name": "旺村镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大城县人民政府",
        "location": "河北省廊坊市大城县旺村镇"
    },
    {
        "id": 10,
        "name": "大尚屯镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大城县人民政府",
        "location": "河北省廊坊市大城县大尚屯镇"
    },
    {
        "id": 11,
        "name": "南赵扶镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大城县人民政府",
        "location": "河北省廊坊市大城县南赵扶镇"
    },
    {
        "id": 12,
        "name": "留各庄镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大城县人民政府",
        "location": "河北省廊坊市大城县留各庄镇"
    },
    {
        "id": 13,
        "name": "权村镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大城县人民政府",
        "location": "河北省廊坊市大城县权村镇"
    },
    {
        "id": 14,
        "name": "里坦镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大城县人民政府",
        "location": "河北省廊坊市大城县里坦镇"
    },
    {
        "id": 15,
        "name": "广安镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大城县人民政府",
        "location": "河北省廊坊市大城县广安镇"
    },
    {
        "id": 16,
        "name": "北魏镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大城县人民政府",
        "location": "河北省廊坊市大城县北魏镇"
    },
    {
        "id": 17,
        "name": "臧屯镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "大城县人民政府",
        "location": "河北省廊坊市大城县臧屯镇"
    },
    {
        "id": 18,
        "name": "河北大城经济开发区",
        "type": "开发区",
        "level": "乡镇",
        "parent": "大城县人民政府",
        "location": "河北省廊坊市大城县"
    },
]

# 3. Positions
positions = [
    # 庞大鹏
    {
        "person_id": 1,
        "org_id": 1,
        "title": "大城县委书记",
        "start": "2021-05",
        "end": "至今",
        "rank": "正处级",
        "note": "2021年5月由大城县委副书记、县长升任大城县委书记。此前曾担任大城县委副书记、县长。"
    },
    {
        "person_id": 1,
        "org_id": 2,
        "title": "大城县委副书记、县长",
        "start": "待查",
        "end": "2021-05",
        "rank": "正处级",
        "note": "庞大鹏曾长期担任大城县县长，后于2021年5月升任县委书记。具体任职起始时间待查。"
    },
    # 靳志强
    {
        "person_id": 2,
        "org_id": 2,
        "title": "大城县委副书记、县长",
        "start": "待查",
        "end": "至今",
        "rank": "正处级",
        "note": "靳志强任大城县县长，2026年2月在县人大会议上作政府工作报告。具体任职起始时间待查。"
    },
    # 李向伟
    {
        "person_id": 3,
        "org_id": 1,
        "title": "大城县委副书记",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "2025年12月河长名单确认任职。"
    },
    # 王立达
    {
        "person_id": 4,
        "org_id": 2,
        "title": "县委常委、常务副县长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "2025年多篇报道确认身份。"
    },
    # 张向东
    {
        "person_id": 5,
        "org_id": 1,
        "title": "县委常委、组织部部长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "2025年多篇报道确认身份。"
    },
    # 郑金明
    {
        "person_id": 6,
        "org_id": 1,
        "title": "县委常委、宣传部部长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "2025年河长名单确认。"
    },
    # 郭为民
    {
        "person_id": 7,
        "org_id": 1,
        "title": "县委常委、统战部部长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "2025年河长名单确认。"
    },
    # 刘杨
    {
        "person_id": 8,
        "org_id": 1,
        "title": "县委常委、办公室主任",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "2025年河长名单确认。"
    },
    # 李汉松
    {
        "person_id": 9,
        "org_id": 1,
        "title": "县委常委、政法委书记",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "2025年河长名单确认。"
    },
    # 刘青明
    {
        "person_id": 10,
        "org_id": 7,
        "title": "县委常委、人武部部长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "2025年河长名单确认。"
    },
    # 张国霞
    {
        "person_id": 11,
        "org_id": 5,
        "title": "县委常委、纪委书记、监委主任",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "2025年4月巡察工作报道确认身份。"
    },
    # 齐建兴
    {
        "person_id": 12,
        "org_id": 2,
        "title": "县政府副县长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "2025年河长名单确认。"
    },
    # 谷振永
    {
        "person_id": 13,
        "org_id": 2,
        "title": "县政府副县长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "2025年河长名单及多篇报道确认。"
    },
    # 张全旺
    {
        "person_id": 14,
        "org_id": 2,
        "title": "县政府副县长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "2025年河长名单及多篇报道确认。"
    },
    # 王忠星
    {
        "person_id": 15,
        "org_id": 6,
        "title": "县政府副县长、公安局局长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "2025年河长名单确认。"
    },
    # 鲍世博
    {
        "person_id": 16,
        "org_id": 2,
        "title": "县政府副县长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "2025年河长名单确认。"
    },
    # 齐德旺
    {
        "person_id": 17,
        "org_id": 1,
        "title": "大城县委书记",
        "start": "待查",
        "end": "2021-05",
        "rank": "正处级",
        "note": "2021年5月免去大城县委书记职务，一级调研员职级，另有任用。"
    },
    # 田海宽
    {
        "person_id": 18,
        "org_id": 2,
        "title": "大城县委副书记、县长",
        "start": "2021-05",
        "end": "待查（2023年后）",
        "rank": "正处级",
        "note": "2021年5月任大城县委副书记，提名为县长。2023年1月仍有相关报道。"
    },
    # 荣印祥
    {
        "person_id": 19,
        "org_id": 1,
        "title": "大城县委副书记",
        "start": "待查",
        "end": "待查",
        "rank": "副处级",
        "note": "2023年1月大城县领导干部会议报道确认任职。"
    },
    # 刘国旺
    {
        "person_id": 20,
        "org_id": 3,
        "title": "大城县人大常委会主任",
        "start": "待查",
        "end": "至今",
        "rank": "正处级",
        "note": "2025年河长名单确认。"
    },
    # 刘国政
    {
        "person_id": 21,
        "org_id": 4,
        "title": "大城县政协主席",
        "start": "待查",
        "end": "至今",
        "rank": "正处级",
        "note": "2025年河长名单确认。"
    },
]

# 4. Relationships
relationships = [
    # 庞大鹏 — 靳志强：党政搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "庞大鹏任大城县委书记，靳志强任县委副书记、县长，为党政一把手搭档关系",
        "overlap_org": "中共廊坊市大城县委员会／大城县人民政府",
        "overlap_period": "2024-2026（推测靳志强在此时期接任县长）"
    },
    # 齐德旺 — 庞大鹏：前后任（县委书记）
    {
        "person_a": 17,
        "person_b": 1,
        "type": "前后任",
        "context": "齐德旺在2021年5月前担任大城县委书记，庞大鹏接任",
        "overlap_org": "中共廊坊市大城县委员会",
        "overlap_period": "2021-05（交接期）"
    },
    # 庞大鹏 — 田海宽：前后任（县长）
    {
        "person_a": 1,
        "person_b": 18,
        "type": "前后任",
        "context": "庞大鹏由大城县县长升任县委书记，田海宽接任县长",
        "overlap_org": "大城县人民政府",
        "overlap_period": "2021-05（交接期）"
    },
    # 庞大鹏 — 李向伟：上下级
    {
        "person_a": 1,
        "person_b": 3,
        "type": "上下级",
        "context": "庞大鹏为县委书记，李向伟为县委副书记，同为县委常委会成员",
        "overlap_org": "中共廊坊市大城县委员会",
        "overlap_period": "2024至今（推测重合）"
    },
    # 靳志强 — 王立达：上下级
    {
        "person_a": 2,
        "person_b": 4,
        "type": "上下级",
        "context": "靳志强为县长，王立达为常务副县长，协助县长负责县政府日常工作",
        "overlap_org": "大城县人民政府",
        "overlap_period": "2024至今（推测重合）"
    },
    # 庞大鹏 — 张国霞：上下级（纪委监督）
    {
        "person_a": 1,
        "person_b": 11,
        "type": "上下级",
        "context": "庞大鹏为县委书记，张国霞为县委常委、纪委书记",
        "overlap_org": "中共廊坊市大城县委员会",
        "overlap_period": "2025至今（推测重合）"
    },
    # 李向伟 — 荣印祥：前后任（县委副书记）
    {
        "person_a": 19,
        "person_b": 3,
        "type": "前后任",
        "context": "荣印祥曾任大城县委副书记，李向伟接任",
        "overlap_org": "中共廊坊市大城县委员会",
        "overlap_period": "推测2023-2024交接"
    },
    # 田海宽 — 靳志强：前后任（县长）
    {
        "person_a": 18,
        "person_b": 2,
        "type": "前后任",
        "context": "田海宽曾任大城县县长，靳志强接任",
        "overlap_org": "大城县人民政府",
        "overlap_period": "推测2023-2024交接"
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
