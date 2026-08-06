#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大新县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广西壮族自治区
Parent City: 崇左市
Region: 大新县
Targets: 县委书记 & 县长
Task: guangxi_大新县

Research Sources (primary, all official 大新县人民政府门户网站 www.daxin.gov.cn):
- 领导之窗·县长 www.daxin.gov.cn/xxgk/jcxxgk/ldzc/xz/ 及 xz/t17267119.shtml (2024-06-14 陈蒙个人简介: 县委副书记、县长)
- 领导之窗·副县长 fxz/t17267233/t17267501/t17286609/t17267606/t17283532/t17267540/t27087354 (各副县长个人简介)
- 政务要闻 /xwzx/zwyw/t27973294.shtml (2026-07-31 中共大新县第十六次党代会闭幕, 陈蒙主持并作报告)
- 政务要闻 /xwzx/zwyw/t27967364.shtml (2026-07-30 党代会开幕, 付立群主持, 陈蒙作报告)
- 政务要闻 /xwzx/zwyw/t27986302.shtml (2026-08-04 县委第十六届常委会第1次会议, 县委书记陈蒙)
- 政务要闻 /xwzx/zwyw/t27980601.shtml (2026-08-03 县第十八届人大常委会第四十一次会议: 接受陈蒙辞去县长, 任命付立群代理县长, 何明龙代理监委主任)
- 政务要闻 /xwzx/zwyw/t27982219.shtml、t27977990.shtml (2026-08 县委副书记、县政府党组书记付立群走访慰问)
- 政务要闻 /xwzx/zwyw/t27924982.shtml (2026-07-21 县委书记施展到堪圩乡督导, 明确施展为前任书记)
- 政务要闻 /xwzx/zwyw/t27951692.shtml (2026-07-25 第十五届常委会第142次会议, 县委书记陈蒙)
- 政务要闻 /xwzx/zwyw/t27959130.shtml (2026-07-29 第十八届人大常委会第四十次会议, 主任凌焕忠)
- 政务要闻 /xwzx/zwyw/t27951795.shtml (2026-07-26 冯精敏: 县人大常委会党组书记、主任提名候选人)

Research Date: 2026-08-06

Confidence:
- 陈蒙(现任县委书记, 原兼县长)、付立群(县委副书记/代理县长)、施展(前任县委书记) 均由
  daxin.gov.cn 官方政务要闻跨 2026-07 报道证实 (confirmed)。
- 县长职务更替: 2026-08-03 人大第四十一次会议决定接受陈蒙辞去县长、任命付立群为代理县长 (confirmed)。
- 县委常委班子(陈蒙/付立群/俸余/农好伟/赵克林/林高云/闭金和/何明龙/农志刚等)由第十六次党代会
  主席台前排名单证实, 但部分人士具体分工未单独公布 → plausible。
- 批量身份字段(户籍/学历/具体任职起止) 多为 unverified, 已用 open_questions 明确。
- 施展另见于'天等县委书记'报道; 崇左县域 2026-07 同时召开党代会/换届, 存在跨县调配,
  施展卸任大新县委书记后的去向列为 open_gap。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "大新县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──────────────────────────────────────────────────────────────

# 1. Persons (id 1-99; 101+ 为机构)
persons = [
    # ═══ 现任核心领导 ═══
    {
        "id": 1,
        "name": "陈蒙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-10",
        "birthplace": "云南省宣威市",
        "education": "硕士研究生学历",
        "party_join": "2006-11",
        "work_start": "2011-07",
        "current_post": "大新县委书记 (原兼县长)",
        "current_org": "中共大新县委员会",
        "source": "official daxin.gov.cn /xxgk/jcxxgk/ldzc/xz/t17267119.shtml (2024-06-14 县委副书记、县长); /xwzx/zwyw/t27986302.shtml (2026-08-04 县委书记); confidence=confirmed",
    },
    {
        "id": 2,
        "name": "付立群",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大新县委副书记、县人民政府党组书记、代理县长",
        "current_org": "大新县人民政府",
        "source": "official daxin.gov.cn /xwzx/zwyw/t27980601.shtml (2026-08-03 代理县长); /xwzx/zwyw/t27982219.shtml (2026-08-04 县委副书记、县政府党组书记); confidence=confirmed",
    },
    # ═══ 前任县委书记 ═══
    {
        "id": 3,
        "name": "施展",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原大新县委书记 (2026-07 卸任, 去向待核)",
        "current_org": "中共大新县委员会",
        "source": "official daxin.gov.cn /xwzx/zwyw/t27924982.shtml (2026-07-21 县委书记施展); 另有'天等县委书记'报道, 去向待核; confidence=confirmed",
    },
    # ═══ 县委常委会 (第十六次党代会主席台前排) ═══
    {
        "id": 4,
        "name": "俸余",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大新县委副书记(分工待核)",
        "current_org": "中共大新县委员会",
        "source": "official daxin.gov.cn /xwzx/zwyw/t27973294.shtml (2026-07-31 党代会主席台前排); confidence=plausible",
    },
    {
        "id": 5,
        "name": "农好伟",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1977-03",
        "birthplace": "广西天等",
        "education": "大学学历(2010-06 广西民族大学法学)",
        "party_join": "待查",
        "work_start": "1997-07",
        "current_post": "大新县委常委、县政府党组副书记、常务副县长",
        "current_org": "大新县人民政府",
        "source": "official daxin.gov.cn /xxgk/jcxxgk/ldzc/fxz/t17267233.shtml; confidence=confirmed",
    },
    {
        "id": 6,
        "name": "赵克林",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委委员、县领导(分工待核)",
        "current_org": "中共大新县委员会",
        "source": "official daxin.gov.cn /xwzx/zwyw/t27973294.shtml (2026-07-31 党代会主席台前排); confidence=plausible",
    },
    {
        "id": 7,
        "name": "林高云",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委委员、县领导(分工待核)",
        "current_org": "中共大新县委员会",
        "source": "official daxin.gov.cn /xwzx/t27973294.shtml (2026-07-31 党代会主席台前排); confidence=plausible",
    },
    {
        "id": 8,
        "name": "闭金和",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委委员、县领导(分工待核)",
        "current_org": "中共大新县委员会",
        "source": "official daxin.gov.cn 会议报道 t27986302 等; confidence=plausible",
    },
    {
        "id": 9,
        "name": "关成涛",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委委员、县领导(分工待核)",
        "current_org": "中共大新县委员会",
        "source": "official daxin.gov.cn 会议报道; confidence=plausible",
    },
    {
        "id": 10,
        "name": "韦成刚",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1976-07",
        "birthplace": "广西大新",
        "education": "大学学历(2019-01 国家开放大学会计学)",
        "party_join": "2000-12",
        "work_start": "1996-08",
        "current_post": "县委委员、县政府党组成员、副县长",
        "current_org": "大新县人民政府",
        "source": "official daxin.gov.cn /xxgk/jcxxgk/ldzc/fxz/t27087354.shtml; confidence=confirmed",
    },
    {
        "id": 11,
        "name": "何明龙",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "代理大新县监察委员会主任",
        "current_org": "大新县监察委员会",
        "source": "official daxin.gov.cn /xwzx/zwyw/t27980601.shtml (2026-08-03 代理监委主任); confidence=confirmed",
    },
    {
        "id": 12,
        "name": "农志刚",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大新县委常委、县委办公室主任",
        "current_org": "中共大新县委办公室",
        "source": "official daxin.gov.cn /xwzx/zwyw/t27924982.shtml (2026-07-21 县委常委、县委办); confidence=confirmed",
    },
    # ═══ 县政府班子 (副县长) ═══
    {
        "id": 13,
        "name": "甘创新",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1974-03",
        "birthplace": "广西大新",
        "education": "大学学历(2005-12 广西区委党校法律)",
        "party_join": "1999-12",
        "work_start": "1997-01",
        "current_post": "大新县政府党组成员、副县长(分管农业/乡村振兴/民政/交通/水利)",
        "current_org": "大新县人民政府",
        "source": "official daxin.gov.cn /xxgk/jcxxgk/ldzc/fxz/t17267606.shtml; confidence=confirmed",
    },
    {
        "id": 14,
        "name": "韦晓权",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1987-04",
        "birthplace": "广西合山",
        "education": "中央党校研究生",
        "party_join": "2006-12",
        "work_start": "2008-09",
        "current_post": "大新县政府党组成员、副县长、县公安局局长/督察长(兼)、县委政法委副书记(兼)",
        "current_org": "大新县人民政府",
        "source": "official daxin.gov.cn /xxgk/jcxxgk/ldzc/fxz/t17283532.shtml; confidence=confirmed",
    },
    {
        "id": 15,
        "name": "卢芳菲",
        "gender": "女",
        "ethnicity": "仫佬族",
        "birth": "1985-01",
        "birthplace": "广西大化",
        "education": "研究生(2015-06 广西大学公共管理)",
        "party_join": "待查",
        "work_start": "2006-07",
        "current_post": "大新县政府副县长(分管教育/文旅/卫健/医保)",
        "current_org": "大新县人民政府",
        "source": "official daxin.gov.cn /xxgk/jcxxgk/ldzc/fxz/t17267540.shtml; confidence=confirmed",
    },
    {
        "id": 16,
        "name": "黎庆党",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-07",
        "birthplace": "广西贺州",
        "education": "研究生学历(1993-06 西安通信学院无线接力通信)",
        "party_join": "待查",
        "work_start": "1987-10",
        "current_post": "广西驻村工作队大新县工作队队长, 大新县委委员(挂任)、副县长(挂任)",
        "current_org": "大新县人民政府",
        "source": "official daxin.gov.cn /xxgk/jcxxgk/ldzc/fxz/t17286609.shtml; confidence=confirmed",
    },
    {
        "id": 17,
        "name": "陈国纯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-12",
        "birthplace": "广东恩平",
        "education": "本科学历(2004-06 华中科技大学法学)",
        "party_join": "2003-04",
        "work_start": "1997-07",
        "current_post": "广东省江门市江海区人大常委会党组成员、副主任, 大新县委常委(挂任)、副县长(挂任)",
        "current_org": "大新县人民政府",
        "source": "official daxin.gov.cn /xxgk/jcxxgk/ldzc/fxz/t17267501.shtml; confidence=confirmed",
    },
    # ═══ 县人大 ═══
    {
        "id": 18,
        "name": "凌焕忠",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大新县人大常委会主任(现任)",
        "current_org": "大新县人大常委会",
        "source": "official daxin.gov.cn /xwzx/zwyw/t27959130.shtml (2026-07-29 主持人大会议); confidence=confirmed",
    },
    {
        "id": 19,
        "name": "冯精敏",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大新县人大常委会党组书记、主任人选",
        "current_org": "大新县人大常委会",
        "source": "official daxin.gov.cn /xwzx/zwyw/t27951795.shtml (2026-07-26 党组书记、主任人选); confidence=plausible",
    },
    {
        "id": 20,
        "name": "赵英林",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大新县政协主席",
        "current_org": "政协大新县委员会",
        "source": "official daxin.gov.cn 2026-07 走访慰问报道; confidence=confirmed",
    },
    {
        "id": 21,
        "name": "黄大强",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大新县人大常委会副主任",
        "current_org": "大新县人大常委会",
        "source": "official daxin.gov.cn /xwzx/zwyw/t27959130.shtml (2026-07-29); confidence=confirmed",
    },
    {
        "id": 22,
        "name": "闭艳宁",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大新县人大常委会副主任",
        "current_org": "大新县人大常委会",
        "source": "official daxin.gov.cn /xzx/t27959130.shtml (2026-07-29); confidence=confirmed",
    },
    {
        "id": 23,
        "name": "周自龙",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大新县人大常委会副主任",
        "current_org": "大新县人大常委会",
        "source": "official daxin.gov.cn /xwzx/t27959130.shtml (2026-07-29); confidence=confirmed",
    },
    # ═══ 卸任相关 ═══
    {
        "id": 24,
        "name": "陆福都",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原大新县监察委员会主任(2026-08-03 辞去)",
        "current_org": "大新县监察委员会",
        "source": "official daxin.gov.cn /xwzx/t27980601.shtml (2026-08-03); confidence=confirmed",
    },
]

# 2. Organizations
organizations = [
    {"id": 101, "name": "中共大新县委员会", "type": "党委", "level": "县级", "parent": "中共崇左市委", "location": "广西崇左市大新县"},
    {"id": 102, "name": "大新县人民政府", "type": "政府", "level": "县级", "parent": "崇左市人民政府", "location": "广西崇左市大新县"},
    {"id": 103, "name": "大新县人大常委会", "type": "人大", "level": "县级", "parent": "崇左市人大常委会", "location": "广西崇左市大新县"},
    {"id": 104, "name": "政协大新县委员会", "type": "政协", "level": "县级", "parent": "政协崇左市委员会", "location": "广西崇左市大新县"},
    {"id": 105, "name": "大新县纪检监察(监委)委员会", "type": "纪委", "level": "县级", "parent": "崇左市纪委监委", "location": "广西崇左市大新县"},
    {"id": 106, "name": "中共大新县委办公室", "type": "党委", "level": "县级", "parent": "中共大新县委员会", "location": "广西崇左市大新县"},
    {"id": 107, "name": "大新县公安局", "type": "政府", "level": "县级", "parent": "大新县人民政府", "location": "广西崇左市大新县"},
    {"id": 120, "name": "中共崇左市委", "type": "党委", "level": "地级", "parent": "中共广西壮族自治区委员会", "location": "广西崇左市"},
]

# 3. 任职记录
positions = [
    # 核心领导
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start_date": "2026-07", "end_date": "present",
     "rank": "正处级", "note": "2026-07-30 党代会作报告; 2026-07-20 前为施展任内; 一肩挑演进"},
    {"person_id": 1, "org_id": 102, "title": "县委副书记、县长", "start_date": "约2021", "end_date": "2026-08-03",
     "rank": "正处级", "note": "2024-06-14 事例确认为县长; 2026-08-03 辞去县长转专任书记"},
    {"person_id": 2, "org_id": 102, "title": "县委副书记、县政府党组书记、代理县长", "start_date": "2026-08-03", "end_date": "present",
     "rank": "正处级", "note": "2026-08-03 人大第41次会议任命代理县长"},
    # 前任书记
    {"person_id": 3, "org_id": 101, "title": "县委书记(前任)", "start_date": "约2021", "end_date": "2026-07",
     "rank": "正处级", "note": "2026-07-20 仍主持工作; 7月下旬与陈蒙交接; 去向待核"},
    # 县委班子
    {"person_id": 4, "org_id": 101, "title": "县委副书记", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": "分工待核"},
    {"person_id": 5, "org_id": 102, "title": "县委常委、常务副县长", "start_date": "2024", "end_date": "present", "rank": "副处级", "note": "县政府党组副书记"},
    {"person_id": 6, "org_id": 101, "title": "县委委员/县领导", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": "分工待核"},
    {"person_id": 7, "org_id": 101, "title": "县委委员/县领导", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": "分工待核"},
    {"person_id": 8, "org_id": 101, "title": "县委委员/县领导", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": "分工待核"},
    {"person_id": 9, "org_id": 101, "title": "县委委员/县领导", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": "分工待核"},
    {"person_id": 10, "org_id": 102, "title": "县委常委、副县长", "start_date": "2024", "end_date": "present", "rank": "副处级", "note": "分管人社/自然资源/住建等"},
    {"person_id": 11, "org_id": 105, "title": "代理县监委主任", "start_date": "2026-08-03", "end_date": "present", "rank": "副处级", "note": "2026-08-03 人大第41次会议决定"},
    {"person_id": 12, "org_id": 106, "title": "县委常委、县委办公室主任", "start_date": "2024", "end_date": "present", "rank": "副处级", "note": "2026-07-21 参与督导"},
    # 副县长
    {"person_id": 13, "org_id": 102, "title": "副县长(农业/乡村振兴/民政/交通/水利)", "start_date": "2024", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 102, "title": "副县长(公安局长兼)", "start_date": "2024", "end_date": "present", "rank": "副处级", "note": "兼公安局长/督察长/政法委副书记"},
    {"person_id": 15, "org_id": 102, "title": "副县长(教育/文旅/卫健/医保)", "start_date": "2024", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 102, "title": "副县长(挂任)兼驻村工作队队长", "start_date": "2024", "end_date": "present", "rank": "副处级", "note": "挂任"},
    {"person_id": 17, "org_id": 102, "title": "副县长(挂任, 粤桂协作)", "start_date": "2024", "end_date": "present", "rank": "副处级", "note": "挂任; 广东江门江海区人大常委会副主任"},
    # 人大/政协
    {"person_id": 18, "org_id": 103, "title": "县人大常委会主任", "start_date": "2021", "end_date": "present", "rank": "正处级", "note": "2026-07-28 主持人大会议"},
    {"person_id": 19, "org_id": 103, "title": "人大常委会党组书记、主任提名人", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "待下一次人代会当选"},
    {"person_id": 20, "org_id": 104, "title": "县政协主席", "start_date": "2021", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 21, "org_id": 103, "title": "县人大常委会副主任", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 103, "title": "县人大常委会副主任", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 103, "title": "县人大常委会副主任", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    # 卸任
    {"person_id": 24, "org_id": 105, "title": "县监委主任(卸任)", "start_date": "2022", "end_date": "2026-08-03", "rank": "副处级", "note": "2026-08-03 辞去"},
]

# 4. 关系
relationships = [
    {'person_a': 1, 'person_b': 2, 'type': 'superior_subordinate',
     'context': '县委(书记与县委副书记/代理县长党政搭档, 2026-07 党代会同台; 陈蒙党政一肩挑后由付立群接县长',
     'overlap_org': '中共大新县委员会', 'overlap_period': '2026-07-present'},
    {'person_a': 3, 'person_b': 1, 'type': 'predecessor_successor',
     'context': '施展卸任大新县委书记→陈蒙接任 (2026-07)', 'overlap_org': '中共大新县委员会', 'overlap_period': '2026-07'},
    {'person_a': 1, 'person_b': 3, 'type': 'promotion_chain',
     'context': '陈蒙任县长(施展任内), 2026-07 直接升任县委书记', 'overlap_org': '中共大新县委员会', 'overlap_period': '2021-2026'},
    {'person_a': 5, 'person_b': 10, 'type': 'colleague',
     'context': '同在大新县政府班子长期共事', 'overlap_org': '大新县人民政府', 'overlap_period': '2024-present'},
    {'person_a': 5, 'person_b': 13, 'type': 'colleague',
     'context': '同为县政府副县长, 农业/乡村振兴条线部分重叠', 'overlap_org': '大新县人民政府', 'overlap_period': '2024-present'},
    {'person_a': 18, 'person_b': 19, 'type': 'predecessor_successor',
     'context': '凌焕忠为现任人大主任, 冯精敏为党组书记/主任提名人作传承', 'overlap_org': '大新县人大常委会', 'overlap_period': '2026'},
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
    )

    conn = sqlite3.connect(DB_PATH)
    for t in ("persons", "organizations", "positions", "relationships"):
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  [{t}] {n}")
    conn.close()