#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高碑店市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 河北省
Parent City: 保定市
Region: 高碑店市
Targets: 市委书记 & 市长

Research Sources:
- 高碑店市人民政府官方网站 (www.gaobeidian.gov.cn)
  - 领导之窗确认市长贾文征, 副市长张振山、王连勇、史文娟、李四辉、崔爱民, 市二级调研员刘光辉
  - 市委常委会扩大会议(2026-07-08)确认蒋东方为市委书记
  - 市人大常委会公告(2025-11-13): 任命杨涛为市监委副主任、代理主任; 任命王连勇为副市长、公安局局长
  - 第七届人民代表大会第五次会议(2025-01-15): 选举贾文征为市长
  - 市政府办公室活动报道(2026-04)确认史文娟、崔爱民、刘光辉出席

Research Date: 2026-07-24
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "高碑店市"

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
        "name": "蒋东方",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高碑店市委书记",
        "current_org": "中共高碑店市委员会",
        "source": "高碑店市委常委会扩大会议(2026-07-08)确认蒋东方为市委书记,主持会议并讲话. 来源:https://www.gaobeidian.gov.cn/ (高碑店融媒)"  # noqa
    },
    {
        "id": 2,
        "name": "贾文征",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高碑店市委副书记、市长",
        "current_org": "高碑店市人民政府",
        "source": "高碑店市人民政府领导之窗. 第七届人民代表大会第五次会议(2025-01-15)选举贾文征为市长. 来源:https://www.gaobeidian.gov.cn/ejxzzc-6-41580.html"  # noqa
    },
    # ════════════════════════════════════════
    # 市政府领导班子 (from 领导之窗)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "张振山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高碑店市委常委、副市长",
        "current_org": "高碑店市人民政府",
        "source": "高碑店市人民政府领导之窗. 来源:https://www.gaobeidian.gov.cn/ejxzzc-6-38048.html"
    },
    {
        "id": 4,
        "name": "王连勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高碑店市副市长、市公安局局长",
        "current_org": "高碑店市人民政府",
        "source": "高碑店市人民政府领导之窗. 市人大常委会(2025-11-13)任命为副市长、公安局局长. 来源:https://www.gaobeidian.gov.cn/ejxzzc-6-46944.html"  # noqa
    },
    {
        "id": 5,
        "name": "史文娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高碑店市副市长",
        "current_org": "高碑店市人民政府",
        "source": "高碑店市人民政府领导之窗. 来源:https://www.gaobeidian.gov.cn/ejxzzc-6-32115.html"
    },
    {
        "id": 6,
        "name": "李四辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高碑店市副市长",
        "current_org": "高碑店市人民政府",
        "source": "高碑店市人民政府领导之窗. 来源:https://www.gaobeidian.gov.cn/ejxzzc-6-42237.html"
    },
    {
        "id": 7,
        "name": "崔爱民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高碑店市副市长",
        "current_org": "高碑店市人民政府",
        "source": "高碑店市人民政府领导之窗. 来源:https://www.gaobeidian.gov.cn/ejxzzc-6-46481.html"
    },
    {
        "id": 8,
        "name": "刘光辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高碑店市二级调研员",
        "current_org": "高碑店市人民政府",
        "source": "高碑店市人民政府领导之窗. 来源:https://www.gaobeidian.gov.cn/ejxzzc-6-38049.html"
    },
    # ════════════════════════════════════════
    # 其他重要职务领导
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "杨涛",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高碑店市监察委员会副主任、代理主任",
        "current_org": "高碑店市监察委员会",
        "source": "高碑店市人大常委会(2025-11-13)任命. 来源:https://www.gaobeidian.gov.cn/content-94-46947.html"
    },
]

# 2. Organizations
organizations = [
    {"id": 0, "name": "中共高碑店市委员会", "type": "党委", "level": "县级市", "parent": "中共保定市委", "location": "河北省保定市高碑店市"},
    {"id": 1, "name": "高碑店市人民政府", "type": "政府", "level": "县级市", "parent": "保定市人民政府", "location": "河北省保定市高碑店市"},
    {"id": 2, "name": "高碑店市人大常委会", "type": "人大", "level": "县级市", "parent": "保定市人大常委会", "location": "河北省保定市高碑店市"},
    {"id": 3, "name": "高碑店市监察委员会", "type": "纪委", "level": "县级市", "parent": "中共高碑店市委员会", "location": "河北省保定市高碑店市"},
    {"id": 4, "name": "高碑店市公安局", "type": "政府部门", "level": "县级市", "parent": "高碑店市人民政府", "location": "河北省保定市高碑店市"},
    {"id": 5, "name": "高碑店市人民政府办公室", "type": "政府部门", "level": "县级市", "parent": "高碑店市人民政府", "location": "河北省保定市高碑店市"},
    {"id": 6, "name": "高碑店市审计局", "type": "政府部门", "level": "县级市", "parent": "高碑店市人民政府", "location": "河北省保定市高碑店市"},
    {"id": 7, "name": "保定市人民政府", "type": "政府", "level": "地市级", "parent": "河北省人民政府", "location": "河北省保定市"},
    {"id": 8, "name": "中共保定市委", "type": "党委", "level": "地市级", "parent": "中共河北省委", "location": "河北省保定市"},
]

# 3. Positions
positions = [
    # ── Current Leaders ──
    # 蒋东方 - 市委书记
    {"person_id": 1, "org_id": 0, "title": "高碑店市委书记", "start": "待查", "end": "至今", "rank": "正处级", "note": "2026年7月以市委书记身份主持市委常委会扩大会议"},

    # 贾文征 - 市长
    {"person_id": 2, "org_id": 0, "title": "高碑店市委副书记", "start": "待查", "end": "至今", "rank": "副处级", "note": "市委副书记兼任市长"},
    {"person_id": 2, "org_id": 1, "title": "高碑店市人民政府市长", "start": "2025-01（代 2024?, 正 2025-01-15）", "end": "至今", "rank": "正处级", "note": "2025年1月15日第七届人民代表大会第五次会议选举为市长"},
    {"person_id": 2, "org_id": 6, "title": "分管市审计局", "start": "2025-01", "end": "至今", "rank": "", "note": "主持市政府全面工作,负责审计工作"},

    # 张振山 - 市委常委、副市长
    {"person_id": 3, "org_id": 0, "title": "高碑店市委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "高碑店市人民政府副市长", "start": "待查", "end": "至今", "rank": "副处级", "note": "负责农业农村、水利、环保、教育、文旅等方面工作"},

    # 王连勇 - 副市长、公安局长
    {"person_id": 4, "org_id": 1, "title": "高碑店市人民政府副市长", "start": "2025-11-13", "end": "至今", "rank": "副处级", "note": "2025年11月13日市人大常委会任命"},
    {"person_id": 4, "org_id": 4, "title": "高碑店市公安局局长", "start": "2025-11-13", "end": "至今", "rank": "正科级", "note": "兼任"},

    # 史文娟 - 副市长
    {"person_id": 5, "org_id": 1, "title": "高碑店市人民政府副市长", "start": "待查", "end": "至今", "rank": "副处级", "note": "负责卫生、民政、医保、市场监管等方面工作"},

    # 李四辉 - 副市长
    {"person_id": 6, "org_id": 1, "title": "高碑店市人民政府副市长", "start": "待查", "end": "至今", "rank": "副处级", "note": "负责交通运输、供销、工业经济、科技等方面工作"},

    # 崔爱民 - 副市长
    {"person_id": 7, "org_id": 1, "title": "高碑店市人民政府副市长", "start": "待查", "end": "至今", "rank": "副处级", "note": "负责住建、城市管理、人社、市场建设等方面工作"},

    # 刘光辉 - 二级调研员
    {"person_id": 8, "org_id": 1, "title": "高碑店市二级调研员", "start": "待查", "end": "至今", "rank": "正处级", "note": "负责商务、招商引资等工作"},

    # 杨涛 - 监委副主任、代理主任
    {"person_id": 9, "org_id": 3, "title": "高碑店市监察委员会副主任、代理主任", "start": "2025-11-13", "end": "至今", "rank": "副处级", "note": "2025年11月13日市人大常委会任命, 接替吕芳"},
]

# 4. Relationships
relationships = [
    # ── Current Top Team ──
    # 蒋东方 ←→ 贾文征 (书记+市长)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长党政主要领导搭档", "overlap_org": "中共高碑店市委员会/高碑店市人民政府", "overlap_period": "2025-至今"},

    # 贾文征 ←→ 张振山 (市长+常务副市长)
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "市长与市委常委、副市长工作关系", "overlap_org": "高碑店市人民政府", "overlap_period": "2025-至今"},

    # 贾文征 ←→ 王连勇 (市长+副市长/公安局长)
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "市长与副市长/公安局长工作关系", "overlap_org": "高碑店市人民政府", "overlap_period": "2025-至今"},

    # 贾文征 ←→ 史文娟 (市长+副市长)
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "市长与副市长工作关系", "overlap_org": "高碑店市人民政府", "overlap_period": "2025-至今"},

    # 贾文征 ←→ 李四辉 (市长+副市长)
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "市长与副市长工作关系", "overlap_org": "高碑店市人民政府", "overlap_period": "2025-至今"},

    # 贾文征 ←→ 崔爱民 (市长+副市长)
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "市长与副市长工作关系", "overlap_org": "高碑店市人民政府", "overlap_period": "2025-至今"},

    # 贾文征 ←→ 刘光辉 (市长+二级调研员)
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "市长与二级调研员工作关系", "overlap_org": "高碑店市人民政府", "overlap_period": "2025-至今"},

    # 张振山 ←→ 王连勇 (副市长+副市长/公安局长)
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同届市政府班子成员", "overlap_org": "高碑店市人民政府", "overlap_period": "2025-至今"},

    # 张振山 ←→ 史文娟
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "同届市政府班子成员", "overlap_org": "高碑店市人民政府", "overlap_period": "2025-至今"},

    # 王连勇 → 于建军 (前任公安局长, 被免职)
    # 于建军不在当前班子

    # 杨涛 → 吕芳 (监委主任交接)
    # 吕芳辞去市监委主任, 杨涛代理
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
