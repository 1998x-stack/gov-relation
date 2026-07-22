#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
灌阳县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 桂林市
Region: 灌阳县
Targets: 县委书记 & 县长

数据来源:
- 灌阳县政府官网领导之窗 (http://www.guanyang.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/)
- 灌阳县政府官网政务动态、主要领导活动报道
- 百度百科灌阳县词条（统计截至2026年2月）
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "灌阳县"
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
        "name": "韦戴卓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "灌阳县委书记",
        "current_org": "中共灌阳县委员会",
        "source": "confirmed — 灌阳县政府官网新闻「县委常委会召开会议 韦戴卓主持」(2026-07-15)确认灌阳县委书记身份。来源: http://www.guanyang.gov.cn/zwdt/gyyw/t27893138.shtml",
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "徐宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "江西玉山",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "1994年7月",
        "current_post": "灌阳县委副书记、县长",
        "current_org": "灌阳县人民政府",
        "source": "confirmed — 灌阳县政府官网县长个人简介页面。来源: http://www.guanyang.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/xz/t27303681.shtml",
    },
    # ════════════════════════════════════════
    # 县人大常委会主任（待确认）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查（人大主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "",
        "work_start": "待查",
        "current_post": "灌阳县人大常委会主任",
        "current_org": "灌阳县人大常委会",
        "source": "unverified — 需通过政府官网确认。",
    },
    # ════════════════════════════════════════
    # 县政协主席（待确认）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待查（政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "",
        "work_start": "待查",
        "current_post": "灌阳县政协主席",
        "current_org": "灌阳县政协",
        "source": "unverified — 需通过政府官网确认。",
    },
    # ════════════════════════════════════════
    # 县委常委、常务副县长 周恒志
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "周恒志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "灌阳县委常委、常务副县长",
        "current_org": "灌阳县人民政府",
        "source": "confirmed — 百度百科灌阳县词条（2026年2月统计）。来源: https://baike.baidu.com/item/灌阳县",
    },
    # ════════════════════════════════════════
    # 县委常委、副县长 王盛(挂职)
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "王盛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年3月",
        "birthplace": "河北定州",
        "education": "研究生学历，桂林理工大学地球探测与信息技术专业毕业",
        "party_join": "2002年5月",
        "work_start": "2004年7月",
        "current_post": "灌阳县委常委、副县长（挂任期2年）",
        "current_org": "灌阳县人民政府",
        "source": "confirmed — 灌阳县政府官网领导之窗页面。来源: http://www.guanyang.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/fxz/t27303653.shtml",
    },
    # ════════════════════════════════════════
    # 副县长 肖逸
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "肖逸",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年3月",
        "birthplace": "广西临桂",
        "education": "全日制大学学历",
        "party_join": "",
        "work_start": "2006年3月",
        "current_post": "灌阳县副县长",
        "current_org": "灌阳县人民政府",
        "source": "confirmed — 灌阳县政府官网领导之窗页面。来源: http://www.guanyang.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/fxz/t27303643.shtml",
    },
    # ════════════════════════════════════════
    # 副县长 吕新志
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "吕新志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年12月",
        "birthplace": "广西永福",
        "education": "大学本科学历",
        "party_join": "2000年4月",
        "work_start": "2002年7月",
        "current_post": "灌阳县副县长",
        "current_org": "灌阳县人民政府",
        "source": "confirmed — 灌阳县政府官网领导之窗页面。来源: http://www.guanyang.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/fxz/t27303631.shtml",
    },
    # ════════════════════════════════════════
    # 副县长、县公安局局长 赵强
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "赵强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年7月",
        "birthplace": "辽宁锦州",
        "education": "大学学历",
        "party_join": "2005年6月",
        "work_start": "2001年9月",
        "current_post": "灌阳县副县长、县公安局局长",
        "current_org": "灌阳县人民政府",
        "source": "confirmed — 灌阳县政府官网领导之窗页面。来源: http://www.guanyang.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/fxz/t27303616.shtml",
    },
    # ════════════════════════════════════════
    # 副县长 周围
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "周围",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年6月",
        "birthplace": "广西灌阳",
        "education": "在职大学学历",
        "party_join": "2006年11月",
        "work_start": "1998年9月",
        "current_post": "灌阳县副县长",
        "current_org": "灌阳县人民政府",
        "source": "confirmed — 灌阳县政府官网领导之窗页面。来源: http://www.guanyang.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/fxz/t27303601.shtml",
    },
    # ════════════════════════════════════════
    # 前任县委书记 卢嵩
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "卢嵩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（前任灌阳县委书记，已离任）",
        "current_org": "",
        "source": "confirmed — 百度百科灌阳县词条记载2023年8月任灌阳县委书记。去向待查。",
    },
    # ════════════════════════════════════════
    # 前任县长 孙清洪
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "孙清洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（前任灌阳县县长，已离任）",
        "current_org": "",
        "source": "confirmed — 百度百科灌阳县词条记载2023年8月任灌阳县委副书记、县长提名人选。徐宁2024年6月接任县长。",
    },
    # ════════════════════════════════════════
    # 凤彬（灌阳籍，现秀峰区副区长）
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "凤彬",
        "gender": "女",
        "ethnicity": "瑶族",
        "birth": "1984年1月",
        "birthplace": "广西灌阳",
        "education": "西南政法大学",
        "party_join": "无党派",
        "work_start": "待查",
        "current_post": "秀峰区副区长",
        "current_org": "桂林市秀峰区人民政府",
        "source": "confirmed — 桂林市秀峰区政府官网简历。来源: http://www.glxfq.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/fqz/t26634318.shtml",
    },
    # ════════════════════════════════════════
    # 吕佳军（灌阳籍，桂林市商务局副局长）
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "吕佳军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年9月",
        "birthplace": "广西灌阳",
        "education": "广西大学化工系无机化工专业",
        "party_join": "1993年5月",
        "work_start": "1991年7月",
        "current_post": "桂林市商务局党组成员、副局长",
        "current_org": "桂林市商务局",
        "source": "confirmed — 全州县政府官网及桂林市商务局官网。来源: 全州县调研数据",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共灌阳县委员会", "type": "党委", "level": "县", "location": "灌阳县"},
    {"id": 2, "name": "灌阳县人民政府", "type": "政府", "level": "县", "location": "灌阳县"},
    {"id": 3, "name": "灌阳县人大常委会", "type": "人大", "level": "县", "location": "灌阳县"},
    {"id": 4, "name": "灌阳县政协", "type": "政协", "level": "县", "location": "灌阳县"},
    {"id": 5, "name": "中共灌阳县纪律检查委员会", "type": "党委", "level": "县", "location": "灌阳县"},
    {"id": 6, "name": "灌阳县公安局", "type": "政府", "level": "县", "location": "灌阳县"},
    {"id": 7, "name": "中共桂林市委员会", "type": "党委", "level": "地级市", "location": "桂林市"},
    {"id": 8, "name": "桂林市人民政府", "type": "政府", "level": "地级市", "location": "桂林市"},
    {"id": 9, "name": "桂林市秀峰区人民政府", "type": "政府", "level": "县", "location": "桂林市秀峰区"},
    {"id": 10, "name": "桂林市商务局", "type": "政府", "level": "地级市", "location": "桂林市"},
    {"id": 11, "name": "桂林理工大学", "type": "事业单位", "level": "地级市", "location": "桂林市"},
    # 永福县相关组织
    {"id": 12, "name": "中共永福县委员会", "type": "党委", "level": "县", "location": "桂林市永福县"},
    # 桂林市公安局
    {"id": 13, "name": "桂林市公安局", "type": "政府", "level": "地级市", "location": "桂林市"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 核心领导
    {"person_id": 1, "org_id": 1, "title": "灌阳县委书记", "start": "约2025年末-2026年初", "end": "present", "rank": "正处级", "note": "接替卢嵩任县委书记"},
    {"person_id": 2, "org_id": 1, "title": "灌阳县委副书记", "start": "2024年6月", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "灌阳县县长", "start": "2024年6月18日", "end": "present", "rank": "正处级", "note": "当选为灌阳县人民政府县长"},
    # 人大政协（待确认姓名）
    {"person_id": 3, "org_id": 3, "title": "灌阳县人大常委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": "姓名待确认"},
    {"person_id": 4, "org_id": 4, "title": "灌阳县政协主席", "start": "待查", "end": "present", "rank": "正处级", "note": "姓名待确认"},
    # 县政府班子
    {"person_id": 5, "org_id": 2, "title": "灌阳县委常委、常务副县长", "start": "待查", "end": "present", "rank": "副处级", "note": "百度百科统计截止2026年2月"},
    {"person_id": 6, "org_id": 1, "title": "灌阳县委常委（挂职）", "start": "待查", "end": "present", "rank": "副处级", "note": "桂林理工大学挂职干部"},
    {"person_id": 6, "org_id": 2, "title": "灌阳县副县长（挂职）", "start": "待查", "end": "present", "rank": "副处级", "note": "广西驻村工作队灌阳县工作队队长，挂任期2年"},
    {"person_id": 7, "org_id": 2, "title": "灌阳县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "灌阳县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "灌阳县副县长、县公安局局长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "灌阳县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": "本县提拔，曾任灌阳镇镇长、文市镇党委书记"},
    # 前任领导
    {"person_id": 11, "org_id": 1, "title": "灌阳县委书记", "start": "2023年8月", "end": "约2025年末", "rank": "正处级", "note": "2023年8月桂林市委决定任命，已离任"},
    {"person_id": 12, "org_id": 1, "title": "灌阳县委副书记", "start": "2023年8月", "end": "2024年6月", "rank": "正处级", "note": "2023年8月任县委副书记、县长提名人选"},
    {"person_id": 12, "org_id": 2, "title": "灌阳县县长（提名）", "start": "2023年8月", "end": "2024年6月", "rank": "正处级", "note": "未当选，徐宁2024年6月接任"},
    # 前任领导早期职务
    {"person_id": 2, "org_id": 8, "title": "桂林市商务局党组书记、局长", "start": "待查", "end": "约2024年", "rank": "正处级", "note": "徐宁任灌阳县县长前职务"},
    {"person_id": 2, "org_id": 8, "title": "桂林市发展和改革委员会副主任", "start": "待查", "end": "待查", "rank": "副处级", "note": "曾任桂林市发改委副主任、总经济师"},
    {"person_id": 2, "org_id": 8, "title": "桂林市发展计划委员会办公室副主任", "start": "待查", "end": "待查", "rank": "正科级", "note": "早期职业生涯"},
    # 灌阳籍在外官员
    {"person_id": 13, "org_id": 9, "title": "秀峰区副区长", "start": "待查", "end": "present", "rank": "副处级", "note": "灌阳籍干部，县→区交流"},
    {"person_id": 14, "org_id": 10, "title": "桂林市商务局副局长", "start": "约2019年", "end": "present", "rank": "副处级", "note": "灌阳籍干部，曾任全州县委副书记"},
    {"person_id": 14, "org_id": 12, "title": "全州县委副书记（前职）", "start": "约2017年", "end": "约2019年", "rank": "副处级", "note": "全州县委副书记，此前担任组织部部长、常务副县长"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政主要领导
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "韦戴卓（县委书记）与徐宁（县长）为灌阳县党政主要搭档", "overlap_org": "灌阳县党政班子", "overlap_period": "2024年至今"},
    # 县委书记 vs 县政府班子成员
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "韦戴卓（县委书记）与周恒志（县委常委、常务副县长）为县委县政府领导关系", "overlap_org": "灌阳县党政班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "韦戴卓（县委书记）与王盛（县委常委、挂职副县长）为领导关系", "overlap_org": "中共灌阳县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "韦戴卓（县委书记）与肖逸（副县长）为领导关系", "overlap_org": "灌阳县党政班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "韦戴卓（县委书记）与吕新志（副县长）为领导关系", "overlap_org": "灌阳县党政班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "韦戴卓（县委书记）与赵强（副县长、公安局局长）为领导关系", "overlap_org": "灌阳县党政班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "韦戴卓（县委书记）与周围（副县长）为领导关系", "overlap_org": "灌阳县党政班子", "overlap_period": ""},
    # 县长 vs 副县长
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "徐宁（县长）与周恒志（常务副县长）为县政府班子正副职关系", "overlap_org": "灌阳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "徐宁（县长）与王盛（挂职副县长）为县政府班子正副职关系", "overlap_org": "灌阳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "徐宁（县长）与肖逸（副县长）为县政府班子正副职关系", "overlap_org": "灌阳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "徐宁（县长）与吕新志（副县长）为县政府班子正副职关系", "overlap_org": "灌阳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "徐宁（县长）与赵强（副县长、公安局局长）为县政府班子正副职关系", "overlap_org": "灌阳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "徐宁（县长）与周围（副县长）为县政府班子正副职关系", "overlap_org": "灌阳县人民政府", "overlap_period": ""},
    # 前任与现任
    {"person_a": 1, "person_b": 11, "type": "前后任", "context": "韦戴卓接替卢嵩任灌阳县委书记", "overlap_org": "中共灌阳县委员会", "overlap_period": "前后任交接"},
    {"person_a": 2, "person_b": 12, "type": "前后任", "context": "徐宁接替孙清洪任灌阳县县长", "overlap_org": "灌阳县人民政府", "overlap_period": "前后任交接（2024年6月）"},
    # 人大与党委
    {"person_a": 1, "person_b": 3, "type": "党政/人大关系", "context": "韦戴卓（县委书记）与人大主任为县四家班子主要领导", "overlap_org": "灌阳县四家班子", "overlap_period": ""},
    # 政协与党委
    {"person_a": 1, "person_b": 4, "type": "党政/政协关系", "context": "韦戴卓（县委书记）与政协主席为县四家班子主要领导", "overlap_org": "灌阳县四家班子", "overlap_period": ""},
    # 灌阳籍在外关系
    {"person_a": 1, "person_b": 13, "type": "外出干部", "context": "凤彬（灌阳籍，秀峰区副区长）与韦戴卓（灌阳县委书记）为灌阳县关联", "overlap_org": "灌阳县（籍贯地）", "overlap_period": ""},
    {"person_a": 1, "person_b": 14, "type": "外出干部", "context": "吕佳军（灌阳籍，桂林市商务局副局长）与韦戴卓（灌阳县委书记）为灌阳县关联", "overlap_org": "灌阳县（籍贯地）", "overlap_period": ""},
    # 前任书记与前任县长
    {"person_a": 11, "person_b": 12, "type": "党政搭档", "context": "卢嵩（县委书记）与孙清洪（县长提名人选）为前任党政搭档", "overlap_org": "灌阳县党政班子", "overlap_period": "2023年8月至2024年6月"},
    # 挂职关系
    {"person_a": 6, "person_b": 11, "type": "派出单位关系", "context": "王盛由桂林理工大学派出挂职，与灌阳县属高校-地方合作", "overlap_org": "桂林理工大学/灌阳县", "overlap_period": ""},
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
    elif "县长" in post or "副县长" in post or "常务" in post:
        return "50,100,255"  # blue for government
    elif "纪委" in post or "监委" in post:
        return "255,165,0"  # orange for discipline
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
    return p["id"] in (1, 2)

def create_gexf():
    now = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{now}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>灌阳县领导班子工作关系网络 — 广西壮族自治区桂林市灌阳县</description>')
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
    person_id = f"guanyang_{person['name']}"
    # Clean the post for filename
    post_clean = person['current_post'].replace('灌阳','').replace('（','').replace('）','').strip()
    if not post_clean:
        post_clean = person['current_post']
    filename = f"{TODAY}-广西壮族自治区-桂林市-{post_clean}-{person['name']}.json"
    filepath = os.path.join(PERSONS_DIR, filename)

    rels_out = []
    for r in relationships_for_person:
        other_id = r["person_b"] if r["person_a"] == person["id"] else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        rels_out.append({
            "person": other["name"] if other else "未知",
            "person_id": f"guanyang_{other['name']}" if other else "unknown",
            "relationship_type": r["type"],
            "strength": "weak",
            "evidence": r["context"],
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("source","").startswith("confirmed") else "unverified",
            "source_ids": []
        })

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "桂林市",
            "region": "灌阳县",
            "job": person["current_post"],
            "task_id": "guangxi_灌阳县",
            "time_focus": "当前任期"
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
            "administrative_rank": "正处级" if person["id"] in (1,2,3,4,11,12) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("source","").startswith("confirmed"),
            "source_ids": []
        },
        "career_timeline": [
            {
                "start": "待查",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "正处级" if person["id"] in (1,2,3,4,11,12) else "副处级",
                "location": "灌阳县",
                "system": "party" if "委" in person["current_org"] else "government",
                "rank": "",
                "is_key_promotion": False,
                "notes": "需通过网络搜索补充完整履历",
                "confidence": "confirmed" if person.get("source","").startswith("confirmed") else "unverified",
                "source_ids": []
            }
        ],
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
            "caveat": "由于网络访问受限，未获取到公开风格信息。需后续补充。"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "因网络访问受限，未搜索到负面信息。不代表无风险。",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "灌阳县人民政府官方网站",
                "url": "http://www.guanyang.gov.cn/",
                "publisher": "灌阳县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "成功访问，获取到领导之窗页面"
            },
            {
                "id": "S002",
                "title": "灌阳县县长个人简介",
                "url": "http://www.guanyang.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/xz/t27303681.shtml",
                "publisher": "灌阳县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "徐宁完整简历"
            },
            {
                "id": "S003",
                "title": "灌阳县副县长简历",
                "url": "http://www.guanyang.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/fxz/",
                "publisher": "灌阳县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "王盛、肖逸、吕新志、赵强、周围简历"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed" if person.get("source","").startswith("confirmed") else "unverified",
            "current_role": "confirmed" if person.get("source","").startswith("confirmed") else "unverified",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "履历信息不完整" if person.get("birth","") == "待查" else "缺乏早期职业生涯详情"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（出生年月、籍贯、教育背景、历任职务）",
                "why_it_matters": "核心领导的基础信息，是评估其政治晋升路径和关系网络的基础",
                "suggested_queries": [
                    f"{person['name']} 简历 灌阳",
                    f"{person['name']} 任前公示",
                    f"{person['name']} 百度百科"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的现任职务是否准确",
                "why_it_matters": "确认当前在任状态，避免使用已过时信息",
                "suggested_queries": [
                    "灌阳县领导之窗",
                    f"灌阳县 {person['name']} 职务"
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
    print(f"灌阳县领导班子工作关系网络 — 数据构建")
    print(f"As of: {AS_OF}")
    print("=" * 60)
    print()

    # Create DB
    create_db()
    print()

    # Create GEXF
    create_gexf()
    print()

    # Create person JSON files for core leaders with known info
    core_ids = [1, 2]  # 县委书记 & 县长
    written = []
    for pid in core_ids:
        person = next((p for p in persons if p["id"] == pid), None)
        if person:
            rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
            path = write_person_json(person, rels)
            written.append(path)

    # Also write person JSON for key deputies with confirmed info
    for pid in [5, 6, 7, 8, 9, 10]:
        person = next((p for p in persons if p["id"] == pid), None)
        if person and person.get("birth","") != "待查":  # only write if we have some data
            rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
            path = write_person_json(person, rels)
            written.append(path)

    # Write predecessors and cross-county connections
    for pid in [11, 12, 13, 14]:
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
