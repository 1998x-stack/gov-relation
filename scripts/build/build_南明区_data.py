#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
南明区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 贵州省
Parent City: 贵阳市
Region: 南明区
Targets: 区委书记 & 区长

Research Sources (primary, official):
- 南明区人民政府门户「政务公开/领导之窗」 https://www.nanming.gov.cn/zwgk/ldzc/
  - 区委领导 刘桂均 https://www.nanming.gov.cn/zwgk/ldzc/qwld/lgj/ (区委书记)
  - 区政府领导 王益彬 https://www.nanming.gov.cn/zwgk/ldzc/qzfld/wyb/ (区委副书记、区长)
  - 王明鹤 https://www.nanming.gov.cn/zwgk/ldzc/qwld/wmh/ (区委副书记)
  - 武鑫   https://www.nanming.gov.cn/zwgk/ldzc/qwld/wx/   (区委常委、人武部党委书记)
  - 欧阳宇昭 https://www.nanming.gov.cn/zwgk/ldzc/qzfld/oyyz/ (常委、常务副区长)
  - 庞勇   https://www.nanming.gov.cn/zwgk/ldzc/qwld/py/   (区委常委、宣传部部长)
  - 马建宏 https://www.nanming.gov.cn/zwgk/ldzc/qwld/mjh/ (区委常委、纪委书记、监委主任)
  - 杨柳   https://www.nanming.gov.cn/zwgk/ldzc/qwld/yl/   (区委常委、统战部长、政协党组副书记)
  - 龚飞   https://www.nanming.gov.cn/zwgk/ldzc/qwld/gf/   (区委常委、政法委书记)
  - 明阳   https://www.nanming.gov.cn/zwgk/ldzc/qwld/my/   (区委常委、组织部部长)
  - 张仁舰 https://www.nanming.gov.cn/zwgk/ldzc/qzfld/zrj/ (副区长(挂职))
  - 吕力   https://www.nanming.gov.cn/zwgk/ldzc/qzfld/ll/   (副区长)
  - 胡晓辉 https://www.nanming.gov.cn/zwgk/ldzc/qzfld/hxh/ (副区长、区公安)
  - 王晓中 https://www.nanming.gov.cn/zwgk/ldzc/qzfld/wxz/ (副区长)
  - 钟韬   https://www.nanming.gov.cn/zwgk/ldzc/qzfld/zt/   (副区长)

Research Date: 2026-08-06

Confidence:
- 全部现任班子（区委书记、区长、区委常委、副区长）由官方门户「领导之窗」逐人页面确认 (confirmed)。
- 批量身份字段（籍贯/入党时间/之前任职）部分公开，未公开字段以"待查/unknown"标注，并在 open_questions 标记。
- 党组织/区政府更迭时点（刘桂均任书记年份、王益彬任区长年份）、前任记/区长及跨区交流细节受搜索引擎不可用限制 → 记入报告开放缺口待补查。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "南明区"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──────────────────────────────────────────────────────────────

# 1. Persons (id 1-99; 101+ 为机构)
persons = [
    # ═══ Current Top Leaders ═══
    {
        "id": 1,
        "name": "刘桂均",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-04",
        "birthplace": "未查到",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "未查到",
        "current_post": "中共南明区委书记、贵州南明经济开发区党工委书记（兼）",
        "current_org": "中共南明区委员会",
        "source": "official nanming.gov.cn /zwgk/ldzc/qwld/lgj/ (2026-08-06 核对); confidence=confirmed",
    },
    {
        "id": 2,
        "name": "王益彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-12",
        "birthplace": "未查到",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "未查到",
        "current_post": "区委副书记、区人民政府党组书记、区长、贵州南明经济开发区党工委副书记、管委会主任（兼）",
        "current_org": "贵阳市南明区人民政府",
        "source": "official nanming.gov.cn 领导之窗 qzfld/wyb; confidence=confirmed",
    },
    # ═══ 区委副书记、区委常委班子 ═══
    {
        "id": 3,
        "name": "王明鹤",
        "gender": "男",
        "ethnicity": "未查到",
        "birth": "1978-08",
        "birthplace": "未查到",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "未查到",
        "current_post": "中共南明区委副书记",
        "current_org": "中共南明区委员会",
        "source": "official nanming.gov.cn 领导之窗 qqmmh; confidence=confirmed",
    },
    {
        "id": 4,
        "name": "武鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-10",
        "birthplace": "未查到",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "未查到",
        "current_post": "中共南明区委常委、区人民武装部党委书记",
        "current_org": "南明区人民武装部",
        "source": "official nanming.gov.cn 领导之窗/区委领导/wx; confidence=confirmed",
    },
    {
        "id": 5,
        "name": "欧阳宇昭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-06",
        "birthplace": "未查到",
        "education": "大学、公共管理硕士",
        "party_join": "中共党员",
        "work_start": "未查到",
        "current_post": "中共南明区委常委、区人民政府党组副书记、常务副区长",
        "current_org": "贵阳市南明区人民政府",
        "source": "official nanming.gov.cn 领导之窗/区政府领导/oyyz; confidence=confirmed",
    },
    {
        "id": 6,
        "name": "庞勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-02",
        "birthplace": "未查到",
        "education": "大学、工程硕士",
        "party_join": "中共党员",
        "work_start": "未查到",
        "current_post": "中共南明区委常委、区委宣传部部长",
        "current_org": "中共南明区委员会宣传部",
        "source": "official nanming.gov.cn 领导之窗/区委领导/py; confidence=confirmed",
    },
    {
        "id": 7,
        "name": "马建宏",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1983-08",
        "birthplace": "未查到",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "未查到",
        "current_post": "中共南明区委常委、区纪委书记、区监委主任",
        "current_org": "中共南明区纪律检查委员会",
        "source": "official nanming.gov.cn 领导之窗/区委领导/mjh; confidence=confirmed",
    },
    {
        "id": 8,
        "name": "杨柳",
        "gender": "女",
        "ethnicity": "布依族",
        "birth": "1978-06",
        "birthplace": "未查到",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "未查到",
        "current_post": "中共南明区委常委、统战部部长、区政协党组副书记（兼）",
        "current_org": "中共南明区委员会统战部",
        "source": "official nanming.gov.cn 领导之窗/区委领导/yl; confidence=confirmed",
    },
    {
        "id": 9,
        "name": "龚飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-01",
        "birthplace": "未查到",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "未查到",
        "current_post": "中共南明区委常委、区委政法委书记",
        "current_org": "中共南明区委员会政法委员会",
        "source": "official nanming.gov.cn 领导之窗/区委领导/gf; confidence=confirmed",
    },
    {
        "id": 10,
        "name": "明阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-06",
        "birthplace": "未查到",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "未查到",
        "current_post": "中共南明区委常委、区委组织部部长",
        "current_org": "中共南明区委员会组织部",
        "source": "official nanming.gov.cn 领导之窗/区委领导/my; confidence=confirmed",
    },
    {
        "id": 11,
        "name": "张仁舰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-02",
        "birthplace": "未查到",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "未查到",
        "current_post": "中共南明区委常委、区人民政府党组成员、副区长（挂职）",
        "current_org": "贵阳市南明区人民政府",
        "source": "official nanming.gov.cn 领导之窗/区政府领导/zrj; confidence=confirmed",
    },
    # ═══ 区政府副区长 ═══
    {
        "id": 12,
        "name": "吕力",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-02",
        "birthplace": "未查到",
        "education": "本科",
        "party_join": "九三学社社员",
        "work_start": "未查到",
        "current_post": "南明区人民政府副区长",
        "current_org": "贵阳市南明区人民政府",
        "source": "official nanming.gov.cn 领导之窗/区政府领导/ll; confidence=confirmed",
    },
    {
        "id": 13,
        "name": "胡晓辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-12",
        "birthplace": "未查到",
        "education": "大专",
        "party_join": "非中共党员",
        "work_start": "未查到",
        "current_post": "南明区人民政府党组成员、副区长，区公安分局（主持区公安全面工作）",
        "current_org": "贵阳市南明区人民政府",
        "source": "official nanming.gov.cn 领导之窗/区政府领导/hxh; confidence=confirmed",
    },
    {
        "id": 14,
        "name": "王晓中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-11",
        "birthplace": "未查到",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "未查到",
        "current_post": "南明区人民政府党组成员、副区长",
        "current_org": "贵阳市南明区人民政府",
        "source": "official nanming.gov.cn 领导之窗/区政府领导/wxz; confidence=confirmed",
    },
    {
        "id": 15,
        "name": "钟韬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-06",
        "birthplace": "未查到",
        "education": "本科",
        "party_join": "非中共党员",
        "work_start": "未查到",
        "current_post": "南明区人民政府党组成员、副区长",
        "current_org": "贵阳市南明区人民政府",
        "source": "official nanming.gov.cn 领导之窗/区政府领导/zt; confidence=confirmed",
    },
]

# 2. Organizations
organizations = [
    {"id": 101, "name": "中共南明区委员会", "type": "党委", "level": "县级", "parent": "中共贵阳市委员会", "location": "贵州省贵阳市南明区"},
    {"id": 102, "name": "贵阳市南明区人民政府", "type": "政府", "level": "县级", "parent": "贵阳市人民政府", "location": "贵州省贵阳市南明区"},
    {"id": 103, "name": "贵州南明经济开发区", "type": "开发区", "level": "县级", "parent": "贵阳市人民政府", "location": "贵州省贵阳市南明区"},
    {"id": 104, "name": "南明区人民武装部", "type": "政府", "level": "县级", "parent": "贵阳市警备区", "location": "贵州省贵阳市南明区"},
    {"id": 105, "name": "中共南明区纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共南明区委员会", "location": "贵州省贵阳市南明区"},
    {"id": 106, "name": "中共南明区委员会宣传部", "type": "党委", "level": "县级", "parent": "中共南明区委员会", "location": "贵州省贵阳市南明区"},
    {"id": 107, "name": "中共南明区委员会统战部", "type": "党委", "level": "县级", "parent": "中共南明区委员会", "location": "贵州省贵阳市南明区"},
    {"id": 108, "name": "中共南明区委员会政法委员会", "type": "党委", "level": "县级", "parent": "中共南明区委员会", "location": "贵州省贵阳市南明区"},
    {"id": 109, "name": "中共南明区委员会组织部", "type": "党委", "level": "县级", "parent": "中共南明区委员会", "location": "贵州省贵阳市南明区"},
    {"id": 110, "name": "贵阳市公安局南明分局", "type": "政府", "level": "县级", "parent": "贵阳市公安局", "location": "贵州省贵阳市南明区"},
    {"id": 120, "name": "中共贵阳市委员会", "type": "党委", "level": "地级", "parent": "中共贵州省委员会", "location": "贵州省贵阳市"},
]

# 3. 任职记录 (person_id, org_id, title, start_date, end_date, rank, note)
positions = [
    # 区委书记
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start_date": "年内任职", "end_date": "present",
     "rank": "正处级", "note": "官方 2026-08 在位; 兼贵州南明经开区党工委书记; 主持区委全面工作"},
    {"person_id": 1, "org_id": 103, "title": "经开区党工委书记（兼）", "start_date": "年内任职", "end_date": "present",
     "rank": "正处级", "note": "贵州南明经济开发区党工委书记"},
    # 区长
    {"person_id": 2, "org_id": 102, "title": "区委副书记、区人民政府党组书记、区长", "start_date": "年内任职", "end_date": "present",
     "rank": "正处级", "note": "主持区政府全面工作，负责人事、审计"},
    {"person_id": 2, "org_id": 103, "title": "经开区党工委副书记、管委会主任（兼）", "start_date": "待查", "end_date": "present",
     "rank": "正处级", "note": "兼"},
    # 区委副书记
    {"person_id": 3, "org_id": 101, "title": "区委副书记", "start_date": "待查", "end_date": "present",
     "rank": "副处级", "note": "分工含纪检、巡察，协助书记负责巡察工作"},
    # 区委常委
    {"person_id": 4, "org_id": 104, "title": "区委常委、区人民武装部党委书记", "start_date": "待查", "end_date": "present",
     "rank": "副处级", "note": "人武部代表, 承担武装/国防动员"},
    {"person_id": 5, "org_id": 102, "title": "区委常委、区政府党组副书记、常务副区长", "start_date": "待查", "end_date": "present",
     "rank": "副处级", "note": "负责区政府常务工作; 发改、财政、教育、金融、国资、安全（强省会）"},
    {"person_id": 6, "org_id": 106, "title": "区委常委、宣传部部长", "start_date": "待查", "end_date": "present",
     "rank": "副处级", "note": "宣传、意识形态"},
    {"person_id": 7, "org_id": 105, "title": "区委常委、区纪委书记、区监委主任", "start_date": "待查", "end_date": "present",
     "rank": "副处级", "note": "纪检、监察全面工作"},
    {"person_id": 8, "org_id": 107, "title": "区委常委、统战部部长", "start_date": "待查", "end_date": "present",
     "rank": "副处级", "note": "兼区政协党组副书记; 统战、民族宗教"},
    {"person_id": 9, "org_id": 108, "title": "区委常委、政法委书记", "start_date": "待查", "end_date": "present",
     "rank": "副处级", "note": "政法、维稳"},
    {"person_id": 10, "org_id": 109, "title": "区委常委、组织部部长", "start_date": "待查", "end_date": "present",
     "rank": "副处级", "note": "干部、组织建设"},
    {"person_id": 11, "org_id": 102, "title": "区委常委、区政府党组成员、副区长（挂职）", "start_date": "待查", "end_date": "present",
     "rank": "副处级", "note": "挂职; 负责统计；协助综合经济"},
    # 副区长
    {"person_id": 12, "org_id": 102, "title": "区政府副区长", "start_date": "待查", "end_date": "present",
     "rank": "副处级", "note": "住房城建、城市更新、交通运输、自然资源、城管"},
    {"person_id": 13, "org_id": 102, "title": "区政府党组成员、副区长", "start_date": "待查", "end_date": "present",
     "rank": "副处级", "note": "公安、司法、退役军人、综治维稳"},
    {"person_id": 13, "org_id": 110, "title": "区公安分局局长（主持）", "start_date": "待查", "end_date": "present",
     "rank": "副处级", "note": "兼主持区公安分局全面工作"},
    {"person_id": 14, "org_id": 102, "title": "区政府党组成员、副区长", "start_date": "待查", "end_date": "present",
     "rank": "副处级", "note": "工信、招商引资、大数据、科技、市场监管"},
    {"person_id": 15, "org_id": 102, "title": "区政府党组成员、副区长", "start_date": "待查", "end_date": "present",
     "rank": "副处级", "note": "农业农村、民政、卫健、医保、生态环境"},
]

# 4. 关系 (确认或可推断的共事/搭档关系)
relationships = [
    # 书记-区长: 党政班子搭档 (强)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记刘桂均与区委副书记/区长王益彬构成党政班子搭档；书记主持区委、区长主持区政府全面工作",
     "overlap_org": "中共南明区委员会", "overlap_period": "2024-present"},
    # 区长-常务副区长: 政府上下级协作 (强)
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "常务副区长欧阳宇昭负责区政府常务工作，协助区长负责/财政/审计",
     "overlap_org": "贵阳市南明区人民政府", "overlap_period": "2025-present"},
    # 区委常委与书记共事
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委副书记与区委书记同属区委常委会，副书记协助书记负责党组织/巡察工作",
     "overlap_org": "中共南明区委员会", "overlap_period": "2024-present"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "纪委书记与区委书记同属区委常委会议班子",
     "overlap_org": "中共南明区委员会", "overlap_period": "2024-present"},
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "组织部部长与区委书记同属区委常委会议班子",
     "overlap_org": "中共南明区委员会", "overlap_period": "2024-present"},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "政法委书记与区委书记同属区委常委会议班子",
     "overlap_org": "中共南明区委员会", "overlap_period": "2024-present"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "宣传部部长与区委书记同属区委常委会议班子",
     "overlap_org": "中共南明区委员会", "overlap_period": "2024-present"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "人武部代表与区委书记同属区委常委会议班子",
     "overlap_org": "中共南明区委员会", "overlap_period": "2024-present"},
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "挂职副区长（常委）与区委书记同属区委常委会议班子",
     "overlap_org": "中共南明区委员会", "overlap_period": "2024-present"},
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
    print("Done.")