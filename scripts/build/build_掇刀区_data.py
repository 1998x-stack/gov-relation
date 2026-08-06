#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database and GEXF graph for 荆门市掇刀区 leadership network.

Level: 市辖区
Province: 湖北省
Parent City: 荆门市
Region: 掇刀区
Targets: 区委书记 & 区长

Research Date: 2026-08-06 (task hubei_掇刀区)
Evidence quality: primary-source confirmation from official 掇刀区人民政府 portal
(www.duodao.gov.cn) and 荆门市人民政府 portal (www.jingmen.gov.cn), both reachable over
HTTPS. Exa websearch rate-limited, Sogou/Baidu captcha-gated, Bing/jina mirrors timed out,
so roster below is built from official 领导简介与分工 pages (B013001) + party/military
activity notices.

CONFIRMED (primary/official, as of 2026-08):
  - 区委书记 王玮: 男，汉族，1976年11月生，省委党校研究生，中共党员。现任荆门市政府党组成员、
    荆门高新区党工委书记、管委会主任、掇刀区委书记，兼区人武部党委第一书记。
    (jingmen.gov.cn/art/2026/7/6/art_29223_28.html; duodao 区委常委会主持 2026-08-05/08-01 人武部命令大会)
  - 区长 邹茹粘: 区委副书记、区政府党组书记、区长，荆门高新区党工委副书记、管委会常务副主任。
    男，汉族，1976年12月生，湖北松滋人，中共党员，省委党校在职研究生，1996年9月参加工作。
  - 常务副区长 陈启富: 区委常委、区政府党组副书记、常务副区长，高新区党工委委员/管委会副主任、区行政学校校长。
    男，汉族，1967年8月生，湖北沙洋人，省委党校在职大学，1983年9月参加工作。
  - 副区长 双辉/郭剑林/黄健: 均为区政府党组成员/高新区党工委委员、管委会副主任（副区长）。
    双  阳 — 男，1972年9月生，荆门东宝人，在职大学，1993年9月参加工作（住建/城管/循环经济）；
    郭剑林 — 男，1980年9月生，荆门掇刀人，大学，2004年7月参加工作（工业/交通/金融）；
    黄  健 — 区委常委、区政府党组成员、副区长，男，汉族，1983年9月生，湖北武汉人，省委党校在职研究生，2006年7月参加工作（招商引资/商务/内陆港）。
  - 区人武部上校政治委员 张鹏飞；2026-07 新任一区人武部上校部长 徐涛.
  - 体制: 荆门高新区 ⊃ 掇刀区 "一套班子、两块牌子" —— 高新区党工委书记=区委书记；管委会常务副主任=区长。
      掇刀区第六次代表大会（换届） 筹备中（2026-08-05 常委会研究部署）。

UNVERIFIED / open gaps (见 report/open_gaps.md 与各 person JSON open_questions):
  - 前任区委书记（王玮上任前）与前任区长；王玮/邹昭粘 任现职前的完整职务序列。
  - 掇刀区委常委及兼职（纪委/组织/宣传/政法/统战）与人大主任、政协主席名单。
  - 六次党代会后新任班子最终名单。

regional: 掇刀区 — 荆门市主城区辖区，与荆门高新区融合运行；辖 掇刀石、白庙、龙泉 等街道
与 团林铺镇、麻城镇 等乡镇（区情详见政府门户）。
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

# 由暂存目录运行: data/tmp/hubei_掇刀区/build_掇刀区_data.py => parents[3] = repo root
BASE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "掇刀区"

# 入库（暂存/规范化）用 STAGING_DIR 环境变量覆盖输出目录；否则写规范化目录
_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(_STAGING, f"{SLUG}_network.gexf")
else:
    DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
    GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共荆门市掇刀区委员会", "type": "党委", "level": "县处级",
     "parent": "中共荆门市委", "location": "湖北省荆门市掇刀区"},
    {"id": 2, "name": "荆门市掇刀区人民政府", "type": "政府", "level": "县处级",
     "parent": "荆门市人民政府", "location": "湖北省荆门市掇刀区"},
    {"id": 3, "name": "荆门高新区党工委/管委会", "type": "开发区", "level": "国家级高新区",
     "parent": "荆门市人民政府", "location": "湖北省荆门市掇刀区"},
    {"id": 4, "name": "荆门市掇刀区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "荆门市人大常委会", "location": "湖北省荆门市掇刀区"},
    {"id": 5, "name": "中国人民政治协商会议荆门市掇刀区委员会", "type": "政协", "level": "县处级",
     "parent": "政协荆门市委员会", "location": "湖北省荆门市掇刀区"},
    {"id": 6, "name": "荆门市掇刀区纪律检查委员会/监察委员会", "type": "纪委", "level": "县处级",
     "parent": "中共荆门市纪委", "location": "湖北省荆门市掇刀区"},
    {"id": 7, "name": "荆门市掇刀区人民武装部", "type": "政府", "level": "县处级",
     "parent": "荆门军分区", "location": "湖北省荆门市掇刀区"},
    {"id": 8, "name": "荆门市人民政府", "type": "政府", "level": "市厅级",
     "parent": "湖北省人民政府", "location": "湖北省荆门市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 王玮 — 区委书记/高新区党工委书记·管委会主任/市政府党组成员
    {"id": 1, "name": "王玮", "gender": "男", "ethnicity": "汉族", "birth": "1976年11月",
     "birthplace": "待查", "education": "省委党校研究生",
     "party_join": "中共党员（入党时间待查）", "work_start": "待查",
     "current_post": "荆门市政府党组成员，荆门高新区党工委书记、管委会主任，掇刀区委书记（兼区人武部党委第一书记）",
     "current_org": "中共荆门市掇刀区委员会",
     "source": "https://www.jingmen.gov.cn/art/2026/7/6/art_29223_28.html"},
    # 2 — 邹茹粘 — 区长/区委副书记/高新区党工委副书记
    {"id": 2, "name": "邹茹粘", "gender": "男", "ethnicity": "汉族", "birth": "1976年12月",
     "birthplace": "湖北松滋（籍）", "education": "省委党校在职研究生",
     "party_join": "中共党员（入党时间待查）", "work_start": "1996年9月",
     "current_post": "掇刀区委副书记、区长、区政府党组书记；荆门高新区党工委副书记、管委会常务副主任",
     "current_org": "荆门市掇刀区人民政府",
     "source": "https://www.duodao.gov.cn/art/2026/2/9/art_2603_1205053.html"},
    # 3 — 陈启富 — 常务副区长/区委常委
    {"id": 3, "name": "陈启富", "gender": "男", "ethnicity": "汉族", "birth": "1967年8月",
     "birthplace": "湖北沙洋（籍）", "education": "省委党校在职大学",
     "party_join": "中共党员（入党时间待查）", "work_start": "1983年9月",
     "current_post": "掇刀区委常委、区政府党组副书记、常务副区长、区行政学校校长；高新区党工委委员、管委会副主任",
     "current_org": "荆门市掇刀区人民政府",
     "source": "https://www.duodao.gov.cn/art/2026/2/9/art_2603_682922.html"},
    # 4 — 黄健 — 区委常委/副区长
    {"id": 4, "name": "黄健", "gender": "男", "ethnicity": "汉族", "birth": "1983年9月",
     "birthplace": "湖北武汉（籍）", "education": "省委党校在职研究生",
     "party_join": "中共党员（入党时间待查）", "work_start": "2006年7月",
     "current_post": "掇刀区委常委、区政府党组成员、副区长",
     "current_org": "荆门市掇刀区人民政府",
     "source": "https://www.duodao.gov.cn/art/2026/2/9/art_2603_1205058.html"},
    # 5 — 郭剑林 — 副区长
    {"id": 5, "name": "郭剑林", "gender": "男", "ethnicity": "", "birth": "1980年9月",
     "birthplace": "荆门掇刀（籍）", "education": "大学",
     "party_join": "中共党员（入党时间待查）", "work_start": "2004年7月",
     "current_post": "掇刀区政府党组成员、副区长；高新区党工委委员、管委会副主任",
     "current_org": "荆门市掇刀区人民政府",
     "source": "https://www.duodao.gov.cn/art/2026/2/9/art_2603_835074.html"},
    # 6 — 双晖 — 副区长
    {"id": 6, "name": "双晖", "gender": "男", "ethnicity": "", "birth": "1972年9月",
     "birthplace": "荆门东宝（籍）", "education": "在职大学",
     "party_join": "中共党员（入党时间待确认）", "work_start": "1993年9月",
     "current_post": "掇刀区政府党组成员、副区长；高新区党工委委员、管委会副主任",
     "current_org": "荆门市掇刀区人民政府",
     "source": "https://www.duodao.gov.cn/art/2026/2/9/art_2603_835077.html"},
    # 7 — 张鹏飞 — 区人武部上校政治委员
    {"id": 7, "name": "张鹏飞", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "荆门市掇刀区人民武装部上校政治委员",
     "current_org": "荆门市掇刀区人民武装部",
     "source": "https://www.duodao.gov.cn/art/2026/7/18/art_7565_1229962.html"},
    # 8 — 徐涛 — 区人武部上校部长(新任命)
    {"id": 8, "name": "徐涛", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "荆门市掇刀区人民武装部上校部长（2026-07-17 任命）",
     "current_org": "荆门市掇刀区人民武装部",
     "source": "https://www.duodao.gov.cn/art/2026/7/18/art_7565_1229962.html"},
    # 9 — 唐良军 — 区委领导（具体职务待核）
    {"id": 9, "name": "唐良军", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "掇刀区领导（区委领导，具体职务待核）",
     "current_org": "中共荆门市掇刀区委员会",
     "source": "https://www.duodao.gov.cn/art/2026/8/6/art_7562_1232140.html"},
    # 10 — 刘星 — 区委领导（2026-08 出席会议）
    {"id": 10, "name": "刘星", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "掇刀区领导（具体职务待核）",
     "current_org": "中共荆门市掇刀区委员会",
     "source": "https://www.duodao.gov.cn/art/2026/8/6/art_7562_1232140.html"},
    # 11 — 郑文奇 — 区领导（2026-08-04 调研督导出席）
    {"id": 11, "name": "郑文奇", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "掇刀区领导（具体职务待核）",
     "current_org": "掇刀区",
     "source": "https://www.duodao.gov.cn/art/2026/8/4/art_7562_1231726.html"},
    # 12 — 李安波 — 区领导（2026-08-04 出席）
    {"id": 12, "name": "李安波", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "掇刀区领导（具体职务待核）",
     "current_org": "掇刀区",
     "source": "https://www.duodao.gov.cn/art/2026/8/4/art_7562_1231726.html"},
    # 13 — 彭炜炜 — 区政府党组成员
    {"id": 13, "name": "彭炜炜", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "掇刀区政府党组成员（2026-08-04）",
     "current_org": "荆门市掇刀区人民政府",
     "source": "https://www.duodao.gov.cn/art/2026/8/4/art_7562_1231726.html"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 王玮
    {"person_id": 1, "org_id": 8, "title": "荆门市政府党组成员", "start_date": "", "end_date": "present",
     "rank": "", "note": "市政府领导序列"},
    {"person_id": 1, "org_id": 3, "title": "荆门高新区党工委书记、管委会主任", "start_date": "", "end_date": "present",
     "rank": "", "note": "国家级高新区"},
    {"person_id": 1, "org_id": 1, "title": "掇刀区委书记", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "主持掇刀区委全面工作；兼区人武部党委第一书记"},
    # 邹茹粘
    {"person_id": 2, "org_id": 2, "title": "掇刀区长、区政府党组书记", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "主持区政府全面工作、分管审计"},
    {"person_id": 2, "org_id": 1, "title": "掇刀区委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 3, "title": "荆门高新区党工委副书记、管委会常务副主任", "start_date": "", "end_date": "present",
     "rank": "", "note": "负责高新区管委会日常工作"},
    # 陈启富
    {"person_id": 3, "org_id": 2, "title": "常务副区长、区政府党组副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "负责政府常务工作"},
    {"person_id": 3, "org_id": 1, "title": "掇刀区委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "荆门高新区党工委委员、管委会副主任", "start_date": "", "end_date": "present",
     "rank": "", "note": ""},
    # 黄健
    {"person_id": 4, "org_id": 2, "title": "副区长、区政府党组成员", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "招商引资/商务/内陆港"},
    {"person_id": 4, "org_id": 1, "title": "掇刀区委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 郭剑林
    {"person_id": 5, "org_id": 2, "title": "副区长、区政府党组成员", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "工业/交通/金融"},
    {"person_id": 5, "org_id": 3, "title": "荆门高新区党工委委员、管委会副主任", "start_date": "", "end_date": "present",
     "rank": "", "note": ""},
    # 双晖
    {"person_id": 6, "org_id": 2, "title": "副区长、区政府党组成员", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "住建/城管/循环经济"},
    {"person_id": 6, "org_id": 3, "title": "荆门高新区党工委委员、管委会副主任", "start_date": "", "end_date": "present",
     "rank": "", "note": ""},
    # 张鹏飞 / 徐涛
    {"person_id": 7, "org_id": 7, "title": "区人武部上校政治委员", "start_date": "", "end_date": "present",
     "rank": "", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "区人武部上校部长", "start_date": "2026-07-17", "end_date": "present",
     "rank": "", "note": "中央军委国防动员部命令任命"},
    # 唐良军/刘星 — 区委领导
    {"person_id": 9, "org_id": 1, "title": "掇刀区委领导（职务待核）", "start_date": "", "end_date": "present",
     "rank": "", "note": "2026-08-05 招商引资调度会出席"},
    {"person_id": 10, "org_id": 1, "title": "掇刀区委领导（职务待核）", "start_date": "", "end_date": "present",
     "rank": "", "note": "2026-08-05 招商引资调度会出席"},
    # 郑文奇/李安波/彭炜炜 — 区政府领导
    {"person_id": 11, "org_id": 2, "title": "掇刀区领导（职务待核）", "start_date": "", "end_date": "present",
     "rank": "", "note": "2026-08-03 民生项目调研出席"},
    {"person_id": 12, "org_id": 2, "title": "掇刀区领导（职务待核）", "start_date": "", "end_date": "present",
     "rank": "", "note": "2026-08-03 民生项目调研出席"},
    {"person_id": 13, "org_id": 2, "title": "掇刀区政府党组成员", "start_date": "", "end_date": "present",
     "rank": "", "note": "2026-08-04"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 党政正职
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记(高新区党工委书记/管委会主任)与区长(高新区党工委副书记/管委会常务副主任)党政正职搭档",
     "overlap_org": "荆门高新区·掇刀区", "overlap_period": "current", "strength": "strong"},
    # 区委班子
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区委常委、常务副区长", "overlap_org": "中共荆门市掇刀区委员会", "overlap_period": "current", "strength": "medium"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记与区委常委、副区长", "overlap_org": "中共荆门市掇刀区委员会", "overlap_period": "current", "strength": "medium"},
    # 区政府班子内部
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "常务副区长与区委常委/副区长 共事", "overlap_org": "掇刀区人民政府", "overlap_period": "current", "strength": "medium"},
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "常务副区长与副区长(工业/交通)同事", "overlap_org": "掇刀区人民政府", "overlap_period": "current", "strength": "medium"},
    # 军地
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "区委书记(人武部党委第一书记)与区人武部政治委员", "overlap_org": "荆门市掇刀区人民武装部", "overlap_period": "current", "strength": "medium"},
    {"person_a": 8, "person_b": 7, "type": "overlap",
     "context": "区人武部部长与政治委员 同班子", "overlap_org": "荆门市掇刀区人民武装部", "overlap_period": "2026-07-", "strength": "medium"},
    # 区委领导与党政正职
    {"person_a": 9, "person_b": 1, "type": "overlap",
     "context": "区委领导唐良军与区委书记 同区委班子", "overlap_org": "中共荆门市掇刀区委员会", "overlap_period": "2026", "strength": "weak"},
    {"person_a": 10, "person_b": 1, "type": "overlap",
     "context": "区委领导刘星与区委书记 同区委班子", "overlap_org": "中共荆门市掇刀区委员会", "overlap_period": "2026", "strength": "weak"},
    # 区政府领导与区长
    {"person_a": 11, "person_b": 2, "type": "overlap",
     "context": "区领导郑文奇与区长同在工作现场", "overlap_org": "掇刀区", "overlap_period": "2026", "strength": "weak"},
    {"person_a": 12, "person_b": 2, "type": "overlap",
     "context": "区领导李安波与区长同在工作现场", "overlap_org": "掇刀区", "overlap_period": "2026", "strength": "weak"},
    {"person_a": 13, "person_b": 2, "type": "overlap",
     "context": "区政府党组成员彭炜炜与区长 同区政府班子", "overlap_org": "荆门市掇刀区人民政府", "overlap_period": "2026", "strength": "medium"},
]

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
    print(f"\nDone: {SLUG} staging build complete.")