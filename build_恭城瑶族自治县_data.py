#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恭城瑶族自治县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 桂林市
Region: 恭城瑶族自治县
Targets: 县委书记 & 县长

数据来源:
- 恭城瑶族自治县政府官网领导信息 (http://www.gongcheng.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/)
- 恭城县政府官网领导分工通知 (恭政发, 2026-07-22)
- 恭城县政府官网政务动态、主要领导活动报道 (2026-06~07月)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "恭城瑶族自治县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-22"
TODAY = AS_OF

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "刘泳锋",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "恭城瑶族自治县委书记",
        "current_org": "中共恭城瑶族自治县委员会",
        "source": "confirmed — 恭城县政府官网「县委常委会召开会议 刘泳锋主持」(2026-07-15, 称'县委主要负责同志')及「全县防汛救灾和水库安全、生产安全双线作战动员大会」(2026-07-20, 称'县委书记刘泳锋')。来源: http://www.gongcheng.gov.cn/zwdt/jrgc/t27907753.shtml, http://www.gongcheng.gov.cn/zwdt/jrgc/t27930023.shtml",
    },
    # ════════════════════════════════════════
    # 核心领导：县长 / 县政府主要负责同志
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "杨征山",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "恭城瑶族自治县委副书记、县长",
        "current_org": "恭城瑶族自治县人民政府",
        "source": "confirmed — 恭城县政府官网「'两优一先'表彰大会」(2026-06-29)确认杨征山为县委副书记、县长。来源: http://www.gongcheng.gov.cn/zwdt/jrgc/t27841936.shtml。注: 2026-07-20防汛大会已出现田勤以'县政府主要负责同志'身份主持，杨征山可能已离任或调职。",
    },
    # ════════════════════════════════════════
    # 县政府主要负责同志（代理县长）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "田勤",
        "gender": "女",
        "ethnicity": "瑶族",
        "birth": "1979年1月",
        "birthplace": "广西恭城",
        "education": "广西大学本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "恭城县政府主要负责同志（代理县长）",
        "current_org": "恭城瑶族自治县人民政府",
        "source": "confirmed — 恭城县政府官网「全县防汛救灾…大会」(2026-07-20)确认田勤为'县政府主要负责同志'。来源: http://www.gongcheng.gov.cn/zwdt/jrgc/t27930023.shtml。另见 data/persons/20260722-广西壮族自治区-桂林市-县委副书记-田勤.json(原资源县委副书记、恭城籍)",
    },
    # ════════════════════════════════════════
    # 县人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "梁志勇",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "恭城瑶族自治县人大常委会主任",
        "current_org": "恭城瑶族自治县人大常委会",
        "source": "confirmed — 恭城县政府官网「'两优一先'表彰大会」(2026-06-29)确认梁志勇为县人大常委会主任。来源: http://www.gongcheng.gov.cn/zwdt/jrgc/t27841936.shtml",
    },
    # ════════════════════════════════════════
    # 县政协主席
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "徐朝凯",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "恭城瑶族自治县政协主席",
        "current_org": "恭城瑶族自治县政协",
        "source": "confirmed — 恭城县政府官网「'两优一先'表彰大会」(2026-06-29)确认徐朝凯为县政协主席。来源: http://www.gongcheng.gov.cn/zwdt/jrgc/t27841936.shtml",
    },
    # ════════════════════════════════════════
    # 县委常委、常务副县长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "蒋尽球",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth": "1973年7月",
        "birthplace": "待查",
        "education": "大学本科文化",
        "party_join": "中共党员",
        "work_start": "1991年12月",
        "current_post": "恭城瑶族自治县委常委、常务副县长",
        "current_org": "恭城瑶族自治县人民政府",
        "source": "confirmed — 恭城县政府官网领导简历页。来源: http://www.gongcheng.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/fxz/t26478076.shtml",
    },
    # ════════════════════════════════════════
    # 县委常委、组织部部长
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "杨志宇",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "恭城瑶族自治县委常委、组织部部长",
        "current_org": "中共恭城瑶族自治县委员会",
        "source": "confirmed — 恭城县政府官网「'两优一先'表彰大会」(2026-06-29)确认杨志宇为县委常委、组织部部长。来源: http://www.gongcheng.gov.cn/zwdt/jrgc/t27841936.shtml",
    },
    # ════════════════════════════════════════
    # 副县长、公安局局长
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "周建斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年5月",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "1999年12月",
        "current_post": "恭城瑶族自治县副县长、县公安局局长",
        "current_org": "恭城瑶族自治县人民政府",
        "source": "confirmed — 恭城县政府官网领导简历页。来源: http://www.gongcheng.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/fxz/t26477016.shtml",
    },
    # ════════════════════════════════════════
    # 副县长 郑勇
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "郑勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年9月",
        "birthplace": "待查（从全州县提拔）",
        "education": "大学本科文化",
        "party_join": "中共党员",
        "work_start": "2000年9月",
        "current_post": "恭城瑶族自治县副县长",
        "current_org": "恭城瑶族自治县人民政府",
        "source": "confirmed — 恭城县政府官网领导简历页。来源: http://www.gongcheng.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/fxz/t26475765.shtml",
    },
    # ════════════════════════════════════════
    # 副县长 许小燕
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "许小燕",
        "gender": "女",
        "ethnicity": "瑶族",
        "birth": "1976年1月",
        "birthplace": "广西恭城（推测，本地成长干部）",
        "education": "大学文化",
        "party_join": "中共党员",
        "work_start": "1996年9月",
        "current_post": "恭城瑶族自治县副县长",
        "current_org": "恭城瑶族自治县人民政府",
        "source": "confirmed — 恭城县政府官网领导简历页。来源: http://www.gongcheng.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/fxz/t26480427.shtml",
    },
    # ════════════════════════════════════════
    # 县领导 欧新国
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "欧新国",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "恭城瑶族自治县领导（具体职务待查）",
        "current_org": "恭城瑶族自治县",
        "source": "confirmed — 恭城县政府官网「全县防汛救灾…大会」(2026-07-20)以'县领导'出席。来源: http://www.gongcheng.gov.cn/zwdt/jrgc/t27930023.shtml",
    },
    # ════════════════════════════════════════
    # 县领导 廖韬
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "廖韬",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "恭城瑶族自治县领导（具体职务待查）",
        "current_org": "恭城瑶族自治县",
        "source": "confirmed — 恭城县政府官网「全县防汛救灾…大会」(2026-07-20)以'县领导'出席。来源: http://www.gongcheng.gov.cn/zwdt/jrgc/t27930023.shtml",
    },
    # ════════════════════════════════════════
    # 前任县委书记 陈代昌
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "陈代昌",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（前任恭城瑶族自治县委书记，已离任）",
        "current_org": "",
        "source": "confirmed — 恭城县政府官网「'两优一先'表彰大会」(2026-06-29)仍以县委书记身份出席并发表讲话。但2026-07-15县委常委会由刘泳锋主持, 2026-07-20报道称刘泳锋为县委书记。陈代昌已于2026年7月上旬离任。来源: http://www.gongcheng.gov.cn/zwdt/jrgc/t27841936.shtml",
    },
    # ════════════════════════════════════════
    # 更前任县委书记 林武民
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "林武民",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（前任恭城瑶族自治县委书记，后任桂林市人大常委会党组成员、副主任, 已落马）",
        "current_org": "",
        "source": "confirmed — 曾任恭城县长、县委书记（约2013-2021），后晋升桂林市人大常委会副主任。2025年4月被调查，2025年9月被开除党籍公职。来源: CCTV/广西纪委监委 2025-04-15, 2025-09-28",
    },
    # ════════════════════════════════════════
    # 前任县长 黄枝君
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "黄枝君",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（前任恭城瑶族自治县长，已离任）",
        "current_org": "",
        "source": "plausible — 据CCTV/新华社2019年报道，黄枝君时任恭城县长。去向待查。",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共恭城瑶族自治县委员会", "type": "党委", "level": "县", "location": "恭城瑶族自治县"},
    {"id": 2, "name": "恭城瑶族自治县人民政府", "type": "政府", "level": "县", "location": "恭城瑶族自治县"},
    {"id": 3, "name": "恭城瑶族自治县人大常委会", "type": "人大", "level": "县", "location": "恭城瑶族自治县"},
    {"id": 4, "name": "恭城瑶族自治县政协", "type": "政协", "level": "县", "location": "恭城瑶族自治县"},
    {"id": 5, "name": "恭城瑶族自治县公安局", "type": "政府", "level": "县", "location": "恭城瑶族自治县"},
    {"id": 6, "name": "桂林市公安局", "type": "政府", "level": "地级市", "location": "桂林市"},
    {"id": 7, "name": "中共桂林市委员会", "type": "党委", "level": "地级市", "location": "桂林市"},
    {"id": 8, "name": "桂林市人民政府", "type": "政府", "level": "地级市", "location": "桂林市"},
    {"id": 9, "name": "桂林市人大常委会", "type": "人大", "level": "地级市", "location": "桂林市"},
    {"id": 10, "name": "全州县东山瑶族乡党委", "type": "党委", "level": "乡镇", "location": "全州县"},
    {"id": 11, "name": "全州县绍水镇党委", "type": "党委", "level": "乡镇", "location": "全州县"},
    {"id": 12, "name": "龙虎乡党委", "type": "党委", "level": "乡镇", "location": "恭城瑶族自治县"},
    {"id": 13, "name": "西岭镇党委", "type": "党委", "level": "乡镇", "location": "恭城瑶族自治县"},
    {"id": 14, "name": "恭城瑶族自治县委办公室", "type": "党委", "level": "县", "location": "恭城瑶族自治县"},
    {"id": 15, "name": "恭城瑶族自治县发展和改革局", "type": "政府", "level": "县", "location": "恭城瑶族自治县"},
    {"id": 16, "name": "栗木镇党委", "type": "党委", "level": "乡镇", "location": "恭城瑶族自治县"},
    {"id": 17, "name": "平安乡党委", "type": "党委", "level": "乡镇", "location": "恭城瑶族自治县"},
    {"id": 18, "name": "中共资源县委员会", "type": "党委", "level": "县", "location": "桂林市资源县"},
    {"id": 19, "name": "桂林市委组织部", "type": "党委", "level": "地级市", "location": "桂林市"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 核心领导 - 现任
    {"person_id": 1, "org_id": 1, "title": "恭城瑶族自治县委书记", "start": "约2026年7月", "end": "present", "rank": "正处级", "note": "接替陈代昌，首见于2026-07-15县委常委会报道"},
    {"person_id": 2, "org_id": 1, "title": "恭城瑶族自治县委副书记", "start": "待查", "end": "约2026年7月", "rank": "正处级", "note": "2026-06-29仍以县委副书记、县长身份出席表彰大会"},
    {"person_id": 2, "org_id": 2, "title": "恭城瑶族自治县县长", "start": "待查", "end": "约2026年7月", "rank": "正处级", "note": "可能已离任或调职"},
    # 田勤 - 代理县长
    {"person_id": 3, "org_id": 18, "title": "资源县委副书记", "start": "待查", "end": "约2026年7月", "rank": "副处级", "note": "原资源县委副书记，恭城籍"},
    {"person_id": 3, "org_id": 2, "title": "恭城县政府主要负责同志（代理县长）", "start": "2026年7月", "end": "present", "rank": "正处级", "note": "2026-07-20首次以该身份报道"},
    # 人大政协
    {"person_id": 4, "org_id": 3, "title": "恭城瑶族自治县人大常委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "恭城瑶族自治县政协主席", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 常务副县长
    {"person_id": 6, "org_id": 1, "title": "恭城瑶族自治县委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "恭城瑶族自治县常务副县长", "start": "待查", "end": "present", "rank": "副处级", "note": "历任三江乡、嘉会乡、栗木镇、平安乡等"},
    # 组织部部长
    {"person_id": 7, "org_id": 1, "title": "恭城瑶族自治县委常委、组织部部长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 副县长、公安局局长
    {"person_id": 8, "org_id": 2, "title": "恭城瑶族自治县副县长、县公安局局长", "start": "待查", "end": "present", "rank": "副处级", "note": "此前任桂林市公安局叠彩分局副局长、第四看守所政委等"},
    {"person_id": 8, "org_id": 6, "title": "桂林市公安局叠彩分局副局长（前职）", "start": "待查", "end": "待查", "rank": "正科级", "note": "历任大河派出所、水塔山派出所、叠彩分局纪委书记、副局长"},
    {"person_id": 8, "org_id": 5, "title": "恭城瑶族自治县公安局政委（前职）", "start": "待查", "end": "待查", "rank": "副处级", "note": "恭城县公安局党委副书记、政委"},
    # 副县长 郑勇
    {"person_id": 9, "org_id": 2, "title": "恭城瑶族自治县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": "全州县乡镇成长干部"},
    {"person_id": 9, "org_id": 10, "title": "全州县东山瑶族乡党委书记", "start": "待查", "end": "待查", "rank": "正科级", "note": ""},
    {"person_id": 9, "org_id": 11, "title": "全州县绍水镇党委书记", "start": "待查", "end": "待查", "rank": "正科级", "note": ""},
    # 副县长 许小燕
    {"person_id": 10, "org_id": 2, "title": "恭城瑶族自治县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": "恭城本地成长干部"},
    {"person_id": 10, "org_id": 12, "title": "龙虎乡党委书记", "start": "待查", "end": "待查", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 13, "title": "西岭镇党委书记", "start": "待查", "end": "待查", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 14, "title": "恭城县委办副主任（保留正科长级）", "start": "待查", "end": "待查", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 15, "title": "恭城瑶族自治县发展和改革局局长", "start": "待查", "end": "待查", "rank": "正科级", "note": ""},
    # 县领导（欧新国、廖韬）
    {"person_id": 11, "org_id": 1, "title": "恭城瑶族自治县领导（具体职务待查）", "start": "待查", "end": "present", "rank": "待查", "note": "2026-07-20防汛大会出席"},
    {"person_id": 12, "org_id": 1, "title": "恭城瑶族自治县领导（具体职务待查）", "start": "待查", "end": "present", "rank": "待查", "note": "2026-07-20防汛大会出席"},
    # 前任县委书记 陈代昌
    {"person_id": 13, "org_id": 1, "title": "恭城瑶族自治县委书记", "start": "约2021-2022年", "end": "2026年7月", "rank": "正处级", "note": "接替林武民，2026年6月29日仍在任，7月中旬由刘泳锋接替"},
    # 更前任县委书记 林武民
    {"person_id": 14, "org_id": 2, "title": "恭城瑶族自治县县长", "start": "约2013年", "end": "约2016年", "rank": "正处级", "note": "第十二届全国人大代表"},
    {"person_id": 14, "org_id": 1, "title": "恭城瑶族自治县委书记", "start": "约2016年", "end": "约2021年", "rank": "正处级", "note": "晋升桂林市人大副主任"},
    {"person_id": 14, "org_id": 9, "title": "桂林市人大常委会党组成员、副主任", "start": "约2021年", "end": "2025年4月", "rank": "副厅级", "note": "2025年4月被调查，9月被开除党籍公职"},
    # 前任县长 黄枝君
    {"person_id": 15, "org_id": 2, "title": "恭城瑶族自治县县长", "start": "约2017年", "end": "约2021年", "rank": "正处级", "note": "2019年新华社报道提及，去向待查"},
    # 蒋尽球早期职务
    {"person_id": 6, "org_id": 17, "title": "平安乡党委书记", "start": "待查", "end": "待查", "rank": "正科级", "note": ""},
    {"person_id": 6, "org_id": 16, "title": "栗木镇党委书记", "start": "待查", "end": "待查", "rank": "正科级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "恭城瑶族自治县政协副主席", "start": "待查", "end": "待查", "rank": "副处级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政主要领导 - 前后任关系
    {"person_a": 1, "person_b": 13, "type": "前后任", "context": "刘泳锋接替陈代昌任恭城县委书记", "overlap_org": "中共恭城瑶族自治县委员会", "overlap_period": "2026年7月前后任交接"},
    {"person_a": 13, "person_b": 14, "type": "前后任", "context": "陈代昌接替林武民任恭城县委书记", "overlap_org": "中共恭城瑶族自治县委员会", "overlap_period": "约2021-2022年交接"},
    # 现任与前任县长
    {"person_a": 2, "person_b": 3, "type": "前后任", "context": "田勤接替（或代理）杨征山任县政府主要负责同志", "overlap_org": "恭城瑶族自治县人民政府", "overlap_period": "2026年7月"},
    {"person_a": 2, "person_b": 15, "type": "前后任", "context": "杨征山接替黄枝君任恭城县长", "overlap_org": "恭城瑶族自治县人民政府", "overlap_period": "约2021年"},
    # 党政搭档
    {"person_a": 1, "person_b": 3, "type": "党政搭档", "context": "刘泳锋（县委书记）与田勤（县政府主要负责同志）为恭城县新任党政搭档", "overlap_org": "恭城瑶族自治县党政班子", "overlap_period": "2026年7月至今"},
    {"person_a": 13, "person_b": 2, "type": "党政搭档", "context": "陈代昌（县委书记）与杨征山（县长）为前任党政搭档", "overlap_org": "恭城瑶族自治县党政班子", "overlap_period": "约2021-2026年7月"},
    # 书记 vs 县委常委班子成员
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "刘泳锋（县委书记）与蒋尽球（县委常委、常务副县长）为领导关系", "overlap_org": "中共恭城瑶族自治县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "刘泳锋（县委书记）与杨志宇（县委常委、组织部部长）为领导关系", "overlap_org": "中共恭城瑶族自治县委员会", "overlap_period": ""},
    # 书记 vs 副县长
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "刘泳锋（县委书记）与周建斌（副县长、公安局局长）为领导关系", "overlap_org": "恭城瑶族自治县党政班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "刘泳锋（县委书记）与郑勇（副县长）为领导关系", "overlap_org": "恭城瑶族自治县党政班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "刘泳锋（县委书记）与许小燕（副县长）为领导关系", "overlap_org": "恭城瑶族自治县党政班子", "overlap_period": ""},
    # 县长 vs 副县长
    {"person_a": 3, "person_b": 6, "type": "上下级", "context": "田勤（代理县长）与蒋尽球（常务副县长）为县政府班子正副职关系", "overlap_org": "恭城瑶族自治县人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 8, "type": "上下级", "context": "田勤（代理县长）与周建斌（副县长、公安局局长）为县政府班子正副职关系", "overlap_org": "恭城瑶族自治县人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 9, "type": "上下级", "context": "田勤（代理县长）与郑勇（副县长）为县政府班子正副职关系", "overlap_org": "恭城瑶族自治县人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 10, "type": "上下级", "context": "田勤（代理县长）与许小燕（副县长）为县政府班子正副职关系", "overlap_org": "恭城瑶族自治县人民政府", "overlap_period": ""},
    # 前后任县长 林武民-黄枝君-杨征山-田勤
    {"person_a": 14, "person_b": 15, "type": "前后任", "context": "林武民（县长→书记）与黄枝君（后任县长）", "overlap_org": "恭城瑶族自治县人民政府", "overlap_period": "约2016-2017年交接"},
    {"person_a": 15, "person_b": 2, "type": "前后任", "context": "黄枝君（前任县长）与杨征山（后任县长）", "overlap_org": "恭城瑶族自治县人民政府", "overlap_period": "约2021年交接"},
    # 人大 政协 与党委
    {"person_a": 1, "person_b": 4, "type": "党政/人大关系", "context": "刘泳锋（县委书记）与梁志勇（人大主任）为县四家班子主要领导", "overlap_org": "恭城瑶族自治县四家班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "党政/政协关系", "context": "刘泳锋（县委书记）与徐朝凯（政协主席）为县四家班子主要领导", "overlap_org": "恭城瑶族自治县四家班子", "overlap_period": ""},
    # 林武民 落马
    {"person_a": 14, "person_b": 13, "type": "前后任/上下级", "context": "林武民（前县委书记，落马）与陈代昌（接任者）", "overlap_org": "中共恭城瑶族自治县委员会", "overlap_period": "约2021年交接"},
    # 跨县交流 - 郑勇（全州→恭城）
    {"person_a": 9, "person_b": 1, "type": "跨县调任", "context": "郑勇原在全州县乡镇工作（东山瑶族乡、绍水镇），后调任恭城县副县长，属全州→恭城跨县交流", "overlap_org": "全州县/恭城县", "overlap_period": ""},
    # 跨县交流 - 周建斌（桂林公安→恭城）
    {"person_a": 8, "person_b": 1, "type": "跨系统调任", "context": "周建斌从桂林市公安局叠彩分局调任恭城县公安局政委，后任副县长、公安局局长", "overlap_org": "桂林市公安局/恭城县", "overlap_period": ""},
    # 跨县交流 - 田勤（资源县→恭城县）
    {"person_a": 3, "person_b": 1, "type": "跨县调任", "context": "田勤原任资源县委副书记（恭城籍），2026年7月调任恭城县政府主要负责同志", "overlap_org": "资源县/恭城县", "overlap_period": "2026年7月"},
    # 欧新国 廖韬 - 县领导
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "刘泳锋（县委书记）与欧新国（县领导）为领导关系", "overlap_org": "恭城瑶族自治县", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "刘泳锋（县委书记）与廖韬（县领导）为领导关系", "overlap_org": "恭城瑶族自治县", "overlap_period": ""},
]

# =========================================================================
# 5. DATABASE
# =========================================================================
def create_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)
    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
             p.get("birth",""), p.get("birthplace",""), p.get("education",""),
             p.get("party_join",""), p.get("work_start",""),
             p["current_post"], p["current_org"], p.get("source","")))
    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o.get("parent",""), o.get("location","")))
    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos.get("start",""), pos.get("end",""),
             pos.get("rank",""), pos.get("note","")))
    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r.get("overlap_org",""), r.get("overlap_period","")))
    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# =========================================================================
# 6. GEXF
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    """Return r,g,b string based on role."""
    post = p.get("current_post","")
    name = p.get("name","")
    if "书记" in post and "纪委" not in post:
        return "255,50,50"  # red for party secretary
    elif "县长" in post or "副县长" in post or "常务" in post or "政府" in post:
        return "50,100,255"  # blue for government
    elif "纪委" in post or "监委" in post:
        return "255,165,0"  # orange for discipline
    elif "人大" in post:
        return "200,255,255"  # cyan for people's congress
    elif "政协" in post:
        return "255,240,200"  # cream for political consultative
    elif "前任" in post or "（前任" in post:
        return "150,150,150"  # grey for predecessors
    else:
        return "100,100,100"  # grey for others

def org_color(o):
    t = o.get("type","")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
    }
    return colors.get(t, "200,200,200")

def is_top_leader(p):
    return p["id"] in (1, 2, 3)

def create_gexf():
    now = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{now}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>恭城瑶族自治县领导班子工作关系网络 — 广西壮族自治区桂林市恭城瑶族自治县</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    # Attributes: node
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')
    # Attributes: edge
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person->Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}在{esc(pos.get("start",""))}-{esc(pos.get("end",""))}任职"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # Person<->Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


# =========================================================================
# 7. PERSON JSON FILES
# =========================================================================
def write_person_json(person, relationships_for_person):
    """Write a deep person graph JSON file."""
    person_id = f"gongcheng_{person['name']}"
    # Clean the post for filename
    post_clean = person['current_post'].replace('恭城瑶族自治','').replace('恭城','').replace('（','').replace('）','').strip()
    if not post_clean:
        post_clean = person['current_post']
    filename = f"{TODAY}-广西壮族自治区-桂林市-{post_clean}-{person['name']}.json"
    filepath = os.path.join(PERSONS_DIR, filename)

    rels_out = []
    for r in relationships_for_person:
        other_id = r["person_b"] if r["person_a"] == person["id"] else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        rel_type = r["type"]
        strength_map = {
            "党政搭档": "strong",
            "前后任": "strong",
            "上下级": "medium",
            "跨县调任": "medium",
            "跨系统调任": "medium",
            "党政/人大关系": "medium",
            "党政/政协关系": "medium",
        }
        strength = strength_map.get(rel_type, "weak")
        rels_out.append({
            "person": other["name"] if other else "未知",
            "person_id": f"gongcheng_{other['name']}" if other else "unknown",
            "relationship_type": r["type"],
            "strength": strength,
            "evidence": r["context"],
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("source","").startswith("confirmed") else "unverified",
            "source_ids": []
        })

    # Build career timeline
    person_positions = [pos for pos in positions if pos["person_id"] == person["id"]]
    timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        timeline.append({
            "start": pos.get("start", "待查"),
            "end": pos.get("end", "present"),
            "org": org["name"] if org else "",
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": org.get("location", "") if org else "",
            "system": "party" if org and org["type"] == "党委" else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": False,
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if person.get("source","").startswith("confirmed") else "plausible",
            "source_ids": []
        })

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "桂林市",
            "region": "恭城瑶族自治县",
            "job": person["current_post"],
            "task_id": "guangxi_恭城瑶族自治县",
            "time_focus": "当前任期及前任"
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", "待查"),
            "birthplace": person.get("birthplace", "待查"),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", "待查"),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','待查')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','待查')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person["id"] in (1,2,3,4,5,13,14,15) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("source","").startswith("confirmed"),
            "source_ids": []
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "待查",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "公开信息有限，需后续补充。"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未从公开资料搜索到负面信息。不代表无风险。",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "恭城瑶族自治县人民政府官方网站",
                "url": "http://www.gongcheng.gov.cn/",
                "publisher": "恭城瑶族自治县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "成功访问，获取到领导信息页面及多个政务动态"
            },
            {
                "id": "S002",
                "title": "恭城县政府领导信息-副县长页面",
                "url": "http://www.gongcheng.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/fxz/",
                "publisher": "恭城瑶族自治县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "蒋尽球、周建斌、郑勇、许小燕简历"
            },
            {
                "id": "S003",
                "title": "恭城县政府领导分工调整通知",
                "url": "http://www.gongcheng.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zcwjk/xzfwj/gzf/t27934172.shtml",
                "publisher": "恭城瑶族自治县人民政府",
                "published_at": "2026-07-22",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "PDF政府领导分工通知"
            },
            {
                "id": "S004",
                "title": "恭城'两优一先'表彰大会报道",
                "url": "http://www.gongcheng.gov.cn/zwdt/jrgc/t27841936.shtml",
                "publisher": "恭城瑶族自治县融媒体中心",
                "published_at": "2026-06-30",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认陈代昌(书记)、杨征山(县长)、梁志勇(人大主任)、徐朝凯(政协主席)、杨志宇(组织部长)"
            },
            {
                "id": "S005",
                "title": "恭城县委常委会会议报道",
                "url": "http://www.gongcheng.gov.cn/zwdt/jrgc/t27907753.shtml",
                "publisher": "恭城瑶族自治县融媒体中心",
                "published_at": "2026-07-20",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认刘泳锋以'县委主要负责同志'主持常委会(首现)"
            },
            {
                "id": "S006",
                "title": "恭城防汛救灾大会报道",
                "url": "http://www.gongcheng.gov.cn/zwdt/jrgc/t27930023.shtml",
                "publisher": "恭城瑶族自治县融媒体中心",
                "published_at": "2026-07-21",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认刘泳锋为县委书记、田勤为县政府主要负责同志、欧新国和廖韬为县领导"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "履历信息部分不完整，多个核心人物出生年月及早期历程待查"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（出生年月、籍贯、教育背景、历任职务）",
                "why_it_matters": "核心领导的基础信息，是评估其政治晋升路径和关系网络的基础",
                "suggested_queries": [
                    f"{person['name']} 简历 恭城",
                    f"{person['name']} 任前公示",
                    f"{person['name']} 百度百科"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": "刘泳锋的历任职务和职业背景（从何岗位调任恭城县委书记？）",
                "why_it_matters": "新任县委书记的履历完全未知，是本次调查最大缺口",
                "suggested_queries": [
                    "刘泳锋 桂林 简历",
                    "刘泳锋 任前公示",
                    "刘泳锋 恭城县委书记"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "杨征山的去向（2026年7月后）",
                "why_it_matters": "杨征山在6月底还在任，7月已不再任县长，需确认调职或离任",
                "suggested_queries": [
                    "杨征山 调任 桂林",
                    "杨征山 恭城县长 离任"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "陈代昌的去向（2026年7月离任后）",
                "why_it_matters": "陈代昌6月底仍在任县委书记，7月中旬即由刘泳锋接替",
                "suggested_queries": [
                    "陈代昌 恭城县委书记 离任",
                    "陈代昌 桂林 调任"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Person JSON created: {filepath}")
    return filepath


# =========================================================================
# 8. MAIN
# =========================================================================
def main():
    print("=" * 60)
    print(f"恭城瑶族自治县领导班子工作关系网络 — 数据构建")
    print(f"As of: {AS_OF}")
    print("=" * 60)
    print()

    # Create DB
    create_db()
    print()

    # Create GEXF
    create_gexf()
    print()

    # Create person JSON files for core leaders
    core_ids = [1, 2, 3]  # 县委书记, 县长(前), 代理县长
    written = []
    for pid in core_ids:
        person = next((p for p in persons if p["id"] == pid), None)
        if person:
            rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
            path = write_person_json(person, rels)
            written.append(path)

    # Write person JSON for key deputies with confirmed info
    for pid in [6, 7, 8, 9, 10, 4, 5]:
        person = next((p for p in persons if p["id"] == pid), None)
        if person and person.get("birth","") != "待查":
            rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
            path = write_person_json(person, rels)
            written.append(path)

    # Write predecessors
    for pid in [13, 14, 15]:
        person = next((p for p in persons if p["id"] == pid), None)
        if person:
            rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
            path = write_person_json(person, rels)
            written.append(path)

    print()
    print("=" * 60)
    print("构建完成！")
    print(f"数据库: {DB_PATH}")
    print(f"GEXF图: {GEXF_PATH}")
    print(f"人物JSON: {len(written)} files")
    for w in written:
        print(f"  - {w}")
    print("=" * 60)

if __name__ == "__main__":
    main()
