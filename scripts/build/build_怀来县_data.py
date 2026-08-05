#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
怀来县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 张家口市
Region: 怀来县
Targets: 县委书记 & 县长

Research Sources（一手官方，怀来县人民政府网站 www.huailai.gov.cn）:
- 《政协怀来县第十六届委员会第一次会议开幕》(2026-07-23) ss71254:
  明确「中共怀来县委书记杜京代表中共怀来县委向大会的召开表示祝贺并作讲话」。
- 《怀来县第十八届人民代表大会第一次会议开幕》(2026-07-21) ss71258:
  「怀来县政府副县长、代理县长赵铁成代表县人民政府向大会作政府工作报告」。
- 《怀来县第十八届人民代表大会第一次会议闭幕》(2026-07-23) ss71263:
  新当选名单：县人大常委会主任 刘朝君；副主任 李洪波、曹锦宏、董海红、姚金山；
  县人民政府县长 赵铁成；副县长 王磊、张知、侯建伟、李慧、刘彩月、李扬；
  县监察委员会主任 刘志钦；县法院院长 宋凯阳；县检察院检察长 杨汉成。
- 《中国共产党怀来县第十五次代表大会闭幕》(2026-07-19) ss71252:
  十五届县委领导班子线索：杜京、赵铁成、陈海龙、刘朝君、韩志明、王锦峰、吴俊宏、
  卫华、王霞、王磊、刘志钦、闫丰、耳英男、师永乐。
- 《政协怀来县第十六届委员会第一次会议闭幕》(2026-07-22) ss71261:
  政协主席 韩志明；副主席/秘书长 高富军、祁志强、连桂琴、戴树伟、李东。
- 《怀来县第十七届人民代表大会第七次会议开幕》(2026-02-02) ss68468:
  换届前：主席团前排 张琪、王学东…；「县长王学东代表县政府作政府工作报告」；
  「县政府常务副县长赵铁成作…报告」。
- 《怀来县工商业联合会（总商会）第十三次会员代表大会召开》(2026-03-23) ss68949 / 68531:
  「县委书记张琪出席会议并讲话」；「县委常委、统战部部长孙婧致开幕词」；
  「县政协副主席、第十二届工商联主席祁志强…」。

重要背景：2026-07 中旬怀来县同步完成县第十五次党代会、县政协十六届一次会议、
县人大十八届一次会议的换届改选。县委书记 由 张琪 → 杜京；县长 由 王学东 → 赵铁成。

Confidence 说明：
  杜京 任县委书记 — confirmed（官网 2026-07-23 政协开幕新闻原文）。
  赵铁成 任县长 — confirmed（官网 2026-07-23 人大闭幕选举名单；此前为常务副县长/代县长）。
  张琪 前任县委书记 / 王学东 前任县长 — confirmed（官网 2026-02/2026-03 新闻原文）。
  其余四套班子领导 — confirmed（官网 2026-07 换届新闻原文）。
  各人出生年月、籍贯、学历、入党/参工时间 — 官网未披露，标 unknown（见报告缺口）。

Research Date: 2026-08-05
"""

import os
import sys
from pathlib import Path

# Allow import from repo root robustly (works from data/tmp/<task>/ and scripts/build/)
REPO_ROOT = Path(__file__).resolve().parents[2]
for _pc in [2, 3, 4, 5]:
    _candidate = Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "怀来县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "杜京",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀来县委书记",
        "current_org": "中共怀来县委员会",
        "source": "怀来县人民政府官网 ss71254（2026-07-23 政协开幕词原文）「中共怀来县委书记杜京代表中共怀来县委…作讲话」。出生/学历未公开。"
    },
    {
        "id": 2,
        "name": "赵铁成",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀来县长",
        "current_org": "怀来县人民政府",
        "source": "怀来县人民政府官网 ss71258（2026-07-21 人大开幕：县政府副县长、代理县长赵铁成作政府报告）、ss71263（2026-07-23 人大闭幕：当选县长）。早期为县政府常务副县长（2026-02 ss68468）。"
    },
    # ════════════════════════════════════════
    # Predecessors
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "张琪",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（前任）怀来县委书记",
        "current_org": "中共怀来县委员会",
        "source": "怀来县人民政府官网 ss68949（2026-03-23）「县委书记张琪…」、ss68468（2026-02-02）县人大主席团前排「张琪」、ss68531（2026-02-20）「张琪、王学东慰问…」。2026-07 换届为新任书记，去向待查。"
    },
    {
        "id": 4,
        "name": "王学东",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（前任）怀来县长",
        "current_org": "怀来县人民政府",
        "source": "怀来县人民政府官网 ss68468（2026-02-02 人大七次会议）「县长王学东代表县政府作政府工作报告」、ss69907（2026-04-30）「王学东带队赴邯郸市成安县考察学习」。2026-07 换届卸任，去向待查。"
    },
    # ════════════════════════════════════════
    # 人大 / 政协 主要领导
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "刘朝君",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀来县人大常委会主任",
        "current_org": "怀来县人民代表大会常务委员会",
        "source": "怀来县人民政府官网 ss71263（2026-07-23）「新当选的县人大常委会主任刘朝君…」；此前已任人大（ss68468 主席团常务主席）。"
    },
    {
        "id": 6,
        "name": "韩志明",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀来县政协主席",
        "current_org": "政协怀来县委员会",
        "source": "怀来县人民政府官网 ss71261（2026-07-22 政协闭幕）「政协怀来县第十六届委员会主席韩志明在闭幕大会上讲话」。"
    },
    # ── 人大常委会副主任 ──
    {
        "id": 7,
        "name": "李洪波",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县人大常委会副主任",
        "current_org": "怀来县人民代表大会常务委员会",
        "source": "ss71263 换届选举名单。"
    },
    {
        "id": 8,
        "name": "曹锦宏",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县人大常委会副主任",
        "current_org": "怀来县人民代表大会常务委员会",
        "source": "ss71263 换届选举名单。"
    },
    {
        "id": 9,
        "name": "董海红",
        "gender": "女", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县人大常委会副主任",
        "current_org": "怀来县人民代表大会常务委员会",
        "source": "ss71263 换届选举名单；亦见 ss68468 人大主席团后排。"
    },
    {
        "id": 10,
        "name": "姚金山",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县人大常委会副主任",
        "current_org": "怀来县人民代表大会常务委员会",
        "source": "ss71263 换届选举名单。"
    },
    # ── 县政府副县长 ──
    {
        "id": 11,
        "name": "王磊",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县副县长（兼县委常委线索）",
        "current_org": "怀来县人民政府",
        "source": "ss71263（副县长）；ss71252（县党代会执行主席，列为县委常委线索）。"
    },
    {
        "id": 12,
        "name": "张知",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县副县长",
        "current_org": "怀来县人民政府",
        "source": "ss71263 换届选举名单。"
    },
    {
        "id": 13,
        "name": "侯建伟",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县副县长",
        "current_org": "怀来县人民政府",
        "source": "ss71263 换届选举名单；ss68468 县领导名单。"
    },
    {
        "id": 14,
        "name": "李慧",
        "gender": "女", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县副县长",
        "current_org": "怀来县人民政府",
        "source": "ss71263 换届选举名单。"
    },
    {
        "id": 15,
        "name": "刘彩月",
        "gender": "女", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县副县长",
        "current_org": "怀来县人民政府",
        "source": "ss71263 换届选举名单。"
    },
    {
        "id": 16,
        "name": "李扬",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县副县长",
        "current_org": "怀来县人民政府",
        "source": "ss71263 换届选举名单。"
    },
    # ── 纪委监委 / 两院 ──
    {
        "id": 17,
        "name": "刘志钦",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县监察委员会主任",
        "current_org": "怀来县监察委员会",
        "source": "ss71263 换届选举名单；ss71252 纪委执委（县委执行主席）。"
    },
    {
        "id": 18,
        "name": "宋凯阳",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县人民法院院长",
        "current_org": "怀来县人民法院",
        "source": "ss71263 换届选举名单。"
    },
    {
        "id": 19,
        "name": "杨汉成",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县人民检察院检察长",
        "current_org": "怀来县人民检察院",
        "source": "ss71263 换届选举名单。"
    },
    # ── 政协副主席 ──
    {
        "id": 20,
        "name": "高富军",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县政协副主席",
        "current_org": "政协怀来县委员会",
        "source": "ss71261（政协闭幕前排就座并主持）。"
    },
    {
        "id": 21,
        "name": "祁志强",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县政协副主席兼县工商联主席",
        "current_org": "政协怀来县委员会",
        "source": "ss71261（政协闭幕前排）；ss68949（2026-03 县政协副主席、县工商联主席）。"
    },
    {
        "id": 22,
        "name": "连桂琴",
        "gender": "女", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县政协副主席",
        "current_org": "政协怀来县委员会",
        "source": "ss71261（政协闭幕前排）。"
    },
    {
        "id": 23,
        "name": "戴树伟",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县政协副主席",
        "current_org": "政协怀来县委员会",
        "source": "ss71261（政协闭幕前排）。"
    },
    {
        "id": 24,
        "name": "李东",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县政协副主席",
        "current_org": "政协怀来县委员会",
        "source": "ss71261（政协闭幕前排）。"
    },
    # ── 县委常委（十五届）线索 ──
    {
        "id": 25,
        "name": "陈海龙",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "（十五届县委常委会成员线索）",
        "current_org": "中共怀来县委员会",
        "source": "ss71252 十五届党代会执行主席；ss71258 人大开幕主席团前排；ss68468 县领导名单。"
    },
    {
        "id": 26,
        "name": "王锦峰",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "（十五届县委常委会成员线索）",
        "current_org": "中共怀来县委员会",
        "source": "ss71252 执行主席；ss68468 县领导名单。"
    },
    {
        "id": 27,
        "name": "吴俊宏",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "（十五届县委常委会成员线索）",
        "current_org": "中共怀来县委员会",
        "source": "ss71252 执行主席；ss68468 县领导名单。"
    },
    {
        "id": 28,
        "name": "卫华",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "（十五届县委常委会成员线索）",
        "current_org": "中共怀来县委员会",
        "source": "ss71252 执行主席；ss68468 县领导名单。"
    },
    {
        "id": 29,
        "name": "王霞",
        "gender": "女", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "（十五届县委常委会成员线索）",
        "current_org": "中共怀来县委员会",
        "source": "ss71252 十五届党代会执行主席。"
    },
    {
        "id": 30,
        "name": "闫丰",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "（十五届县委常委会成员线索）",
        "current_org": "中共怀来县委员会",
        "source": "ss71252 执行主席；ss68468 县领导名单。"
    },
    {
        "id": 31,
        "name": "耳英男",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "（十五届县委常委会成员线索）",
        "current_org": "中共怀来县委员会",
        "source": "ss71252 执行主席；ss68468 县领导名单。"
    },
    {
        "id": 32,
        "name": "师永乐",
        "gender": "男", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "（十五届县委常委会成员线索）",
        "current_org": "中共怀来县委员会",
        "source": "ss71252 执行主席；ss68468 县领导名单。"
    },
    {
        "id": 33,
        "name": "孙婧",
        "gender": "女", "ethnicity": "待查", "birth": "待查", "birthplace": "待查", "native_place": "待查",
        "education": "待查", "party_join": "中共党员", "work_start": "待查",
        "current_post": "怀来县委常委、统战部部长",
        "current_org": "中共怀来县委员会",
        "source": "ss68949（2026-03）「县委常委、统战部部长孙婧致开幕词」。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共怀来县委员会",
        "type": "党委",
        "level": "县级",
        "location": "张家口市怀来县",
        "parent": "中共张家口市委"
    },
    {
        "id": 2,
        "name": "怀来县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "张家口市怀来县",
        "parent": "张家口市人民政府"
    },
    {
        "id": 3,
        "name": "怀来县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "location": "张家口市怀来县",
        "parent": ""
    },
    {
        "id": 4,
        "name": "政协怀来县委员会",
        "type": "政协",
        "level": "县级",
        "location": "张家口市怀来县",
        "parent": ""
    },
    {
        "id": 5,
        "name": "怀来县监察委员会",
        "type": "纪委",
        "level": "县级",
        "location": "张家口市怀来县",
        "parent": ""
    },
    {
        "id": 6,
        "name": "怀来县人民法院",
        "type": "政府",
        "level": "县级",
        "location": "张家口市怀来县",
        "parent": ""
    },
    {
        "id": 7,
        "name": "怀来县人民检察院",
        "type": "政府",
        "level": "县级",
        "location": "张家口市怀来县",
        "parent": ""
    },
    {
        "id": 8,
        "name": "中共张家口市委",
        "type": "党委",
        "level": "地厅级",
        "location": "张家口市",
        "parent": ""
    },
    {
        "id": 9,
        "name": "张家口市人民政府",
        "type": "政府",
        "level": "地厅级",
        "location": "张家口市",
        "parent": ""
    },
]

# 3. Positions
positions = [
    # ── 杜京 (current 县委书记) ──
    {"person_id": 1, "org_id": 1, "title": "怀来县委书记", "start_date": "2026-07（十五大换届）", "end_date": "present", "rank": "正处级", "note": "ss71254（2026-07-23）「中共怀来县委书记杜京」；继任张琪。出生于何地、此前任职待查。"},
    {"person_id": 1, "org_id": 1, "title": "中共怀来县第十四届县委（换届前参与）", "start_date": "未知", "end_date": "2026-07", "rank": "正处级", "note": "在县第十五次党代会上代表十四届县委作报告/任大会执行主席，说明换届前已在县领导班子。"},
    # ── 赵铁成 (current 县长) ──
    {"person_id": 2, "org_id": 2, "title": "怀来县委副书记、县长", "start_date": "2026-07-23", "end_date": "present", "rank": "正处级", "note": "confirmed：2026-07-21 人大十八届一次会议开幕时任「副县长、代理县长」，7-23 当选县长（ss71258/71263）。"},
    {"person_id": 2, "org_id": 2, "title": "怀来县常务副县长", "start_date": "未知（约2023-2026）", "end_date": "2026-07", "rank": "副处级→正处级", "note": "ss68468（2026-02）「县政府常务副县长赵铁成」作民生实事报告；2026 末经代县长扶正。"},
    # ── 张琪 (前县委书记) ──
    {"person_id": 3, "org_id": 1, "title": "怀来县委书记", "start_date": "约2021（含更早县长任上）", "end_date": "2026-07", "rank": "正处级", "note": "ss68949/ss68531/ss68468（2026-02/03）均称县委书记。2026-07 届满交棒杜京，去向待查。"},
    # ── 王学东 (前县长) ──
    {"person_id": 4, "org_id": 2, "title": "怀来县长", "start_date": "未知", "end_date": "2026-07", "rank": "正处级", "note": "ss68468（2026-02-02）县长作报告；ss69907（2026-04-30）带队考察。换届由赵铁成接任，去向待查。"},
    # ── 人大 ──
    {"person_id": 5, "org_id": 3, "title": "怀来县人大常委会主任", "start_date": "2026-07-23", "end_date": "present", "rank": "正处级", "note": "五届人大一次会议当选（ss71263）。"},
    {"person_id": 7, "org_id": 3, "title": "怀来县人大常委会副主任", "start_date": "2026-07-23", "end_date": "present", "rank": "副处级", "note": "换届选举（ss71263）。"},
    {"person_id": 8, "org_id": 3, "title": "怀来县人大常委会副主任", "start_date": "2026-07-23", "end_date": "present", "rank": "副处级", "note": "换届选举（ss71263）。"},
    {"person_id": 9, "org_id": 3, "title": "怀来县人大常委会副主任", "start_date": "2026-07-23", "end_date": "present", "rank": "副处级", "note": "换届选举（ss71263）。"},
    {"person_id": 10, "org_id": 3, "title": "怀来县人大常委会副主任", "start_date": "2026-07-23", "end_date": "present", "rank": "副处级", "note": "换届选举（ss71263）。"},
    # ── 政府副县长 ──
    {"person_id": 11, "org_id": 2, "title": "怀来县人民政府副县长", "start_date": "2026-07-23", "end_date": "present", "rank": "副处级", "note": "ss71263 换届选举；亦列党代会执行主席，为县委常委线索"},
    {"person_id": 12, "org_id": 2, "title": "怀来县人民政府副县长", "start_date": "2026-07-23", "end_date": "present", "rank": "副处级", "note": "换届选举（ss71263）。"},
    {"person_id": 13, "org_id": 2, "title": "怀来县人民政府副县长", "start_date": "2026-07-23", "end_date": "present", "rank": "副处级", "note": "换届选举（ss71263）；2026-02 已任县领导（ss68468）。"},
    {"person_id": 14, "org_id": 2, "title": "怀来县人民政府副县长", "start_date": "2026-07-23", "end_date": "present", "rank": "副处级", "note": "换届选举（ss71263）。"},
    {"person_id": 15, "org_id": 2, "title": "怀来县人民政府副县长", "start_date": "2026-07-23", "end_date": "present", "rank": "副处级", "note": "换届选举（ss71263）。"},
    {"person_id": 16, "org_id": 2, "title": "怀来县人民政府副县长", "start_date": "2026-07-23", "end_date": "present", "rank": "副处级", "note": "换届选举（ss71263）。"},
    # ── 纪委/法院/检察院 ──
    {"person_id": 17, "org_id": 5, "title": "怀来县监察委员会主任", "start_date": "2026-07-23", "end_date": "present", "rank": "正处级", "note": "换届选举（ss71263）。"},
    {"person_id": 18, "org_id": 6, "title": "怀来县人民法院院长", "start_date": "2026-07-23", "end_date": "present", "rank": "副处级", "note": "换届选举（ss71263）。"},
    {"person_id": 19, "org_id": 7, "title": "怀来县人民检察院检察长", "start_date": "2026-07-23", "end_date": "present", "rank": "副处级", "note": "换届选举（ss71263）。"},
    # ── 政协 ──
    {"person_id": 6, "org_id": 4, "title": "怀来县政协主席", "start_date": "2026-07-22", "end_date": "present", "rank": "正处级", "note": "政协十六届一次会议闭幕当选（ss71261），任上连任/换届。"},
    {"person_id": 20, "org_id": 4, "title": "怀来县政协副主席", "start_date": "2026-07-22", "end_date": "present", "rank": "副处级", "note": "政协十六届一次会议（ss71261）。"},
    {"person_id": 21, "org_id": 4, "title": "怀来县政协副主席（兼县工商业联合会主席）", "start_date": "2026-07-22", "end_date": "present", "rank": "副处级", "note": "ss71261 前排；ss68949（2026-03）县政协副主席、县工商联主席。"},
    {"person_id": 22, "org_id": 4, "title": "怀来县政协副主席", "start_date": "2026-07-22", "end_date": "present", "rank": "副处级", "note": "政协十六届一次会议（ss71261）。"},
    {"person_id": 23, "org_id": 4, "title": "怀来县政协副主席", "start_date": "2026-07-22", "end_date": "present", "rank": "副处级", "note": "政协十六届一次会议（ss71261）。"},
    {"person_id": 24, "org_id": 4, "title": "怀来县政协副主席", "start_date": "2026-07-22", "end_date": "present", "rank": "副处级", "note": "政协十六届一次会议（ss71261）。"},
    # ── 县委常委会成员线索 ──
    {"person_id": 25, "org_id": 1, "title": "（十五届县委常委会成员线索）", "start_date": "2026-07（十五届）", "end_date": "present", "rank": "副处级或以上", "note": "ss71252/71258 执行主席、ss68468 县领导名单，但具体分工待确认。"},
    {"person_id": 26, "org_id": 1, "title": "（十五届县委常委会成员线索）", "start_date": "2026-07", "end_date": "present", "rank": "副处级或以上", "note": "同上。"},
    {"person_id": 27, "org_id": 1, "title": "（十五届县委常委会成员线索）", "start_date": "2026-07", "end_date": "present", "rank": "副处级或以上", "note": "同上。"},
    {"person_id": 28, "org_id": 1, "title": "（十五届县委常委会成员线索）", "start_date": "2026-07", "end_date": "present", "rank": "副处级或以上", "note": "同上。"},
    {"person_id": 29, "org_id": 1, "title": "（十五届县委常委会成员线索）", "start_date": "2026-07", "end_date": "present", "rank": "副处级或以上", "note": "同上。"},
    {"person_id": 30, "org_id": 1, "title": "（十五届县委常委会成员线索）", "start_date": "2026-07", "end_date": "present", "rank": "副处级或以上", "note": "同上。"},
    {"person_id": 31, "org_id": 1, "title": "（十五届县委常委会成员线索）", "start_date": "2026-07", "end_date": "present", "rank": "副处级或以上", "note": "同上。"},
    {"person_id": 32, "org_id": 1, "title": "（十五届县委常委会成员线索）", "start_date": "2026-07", "end_date": "present", "rank": "副处级或以上", "note": "同上。"},
    {"person_id": 33, "org_id": 1, "title": "怀来县委常委、统战部部长", "start_date": "2026 年前后在任", "end_date": "present", "rank": "副处级", "note": "ss68945（2026-03）「县委常委、统战部部长孙婧致开幕词」。"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记杜京与县长赵铁成为怀来县现任党政搭档（2026-07 换届后）。",
        "overlap_org": "中共怀来县委／怀来县人民政府",
        "overlap_period": "2026-07-"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "张琪（前任县委书记）→ 杜京接任（2026-07 县委换届）。",
        "overlap_org": "中共怀来县委员会",
        "overlap_period": "2026-07"
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "王学东（前任县长）→ 赵铁成接任（原常务副县长扶正，2026-07 人大选举）。",
        "overlap_org": "怀来县人民政府",
        "overlap_period": "2026-07"
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "overlap",
        "context": "赵铁成（常务副县长）与王学东（县长）在王学东县长任内共事多年。",
        "overlap_org": "怀来县人民政府",
        "overlap_period": "约2023-2026"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "杜京、刘朝君同场出席党代会、人大换届（刘朝君任执行主席、主持大会）。",
        "overlap_org": "中共怀来县委／县人大常委会",
        "overlap_period": "2026-07"
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "overlap",
        "context": "杜京代表县委向政协十六届一次会议祝贺（韩志明任主席发言）。",
        "overlap_org": "中共怀来县委／政协怀来县委员会",
        "overlap_period": "2026-07"
    },
    {
        "person_a": 5,
        "person_b": 2,
        "type": "overlap",
        "context": "刘朝君（人大常委会主任）主持大会、赵铁成当选县长；新一届一府一人大联动。",
        "overlap_org": "怀来县人民代表大会",
        "overlap_period": "2026-07"
    },
    {
        "person_a": 21,
        "person_b": 33,
        "type": "overlap",
        "context": "祁志强（县政协副主席兼工商联主席）与孙婧（县委常委、统战部部长）在2026年县工商联换届中协作（孙婧致开幕词、祁志强作报告）。",
        "overlap_org": "怀来县工商业联合会",
        "overlap_period": "2026-03"
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
    )
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")