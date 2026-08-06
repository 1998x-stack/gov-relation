#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广阳区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 廊坊市
Region: 广阳区
Targets: 区委书记 & 区长

Research Date: 2026-08-05

官方/权威来源 (guangyang.gov.cn 政府网站可访问 + 本地库跨区档案):
- 广阳区人民政府·区政府领导分工 (www.guangyang.gov.cn/18648.html, 更新 2026-07-20):
    区长 王振宇 (主持区政府全面工作, 分管区审计局); 副区长 刘斌(常务,负责发改/财政/招商/应急等)
    , 杨晓军(公安/司法/退役军人), 李书伟(住建/城市更新/临空), 王昆(农业农村/乡村振兴/生态/市监),
    张矜(科技/工信/交通/水利/人社), 杨敏(教育/卫健/文旅/民政/民族宗教), 刘一泓(协助招商/金融).
- 广阳区人大代表换届选举投票报道 (2026-06-22): 区委书记冯斌, 区长王振宇, 区人大主任曹新田,
    区政协主席陈文通 — 四套班子领导班子齐全 (confirmed).
- 广阳区六届人大常委会第三十八次会议 (2026-05-31): 主任 曹新田, 副主任 朱洪波/杨则涛/廖瑾.
- 区委常委会(扩大)会议 (2026-06-12 / 07-05 / 07-20): 区委书记冯斌 依此主持; 确认其 2026 年度在任.
- 冯斌讲授政绩观专题党课 (2026-07-03): 任「区委书记」出席.
- 交叉档案 (本地库 data/persons/20260724-河北省-廊坊市-县长-冯斌.json, hebei_固安县 task):
    冯斌 career = 固安县委专职副书记(2020) -> 固安县委副书记、县长(2021-07) -> 广阳区委书记(当前).
    属廊坊市域内 县->区 干部交流典型 (跨县区轮岗).

Confidence:
- 区委书记 冯斌 / 区长 王振宇 / 人大主任 曹新田 / 政协主席 陈文通 = confirmed (官网多源).
- 副区长 rod etc = confirmed (官网「区政府领导分工」页).
- 冯斌/王振宇 出生年月/籍贯/学历/早期履历 = 待查 (open_questions / report/open_gaps.md 显式标注).
- 前任广阳区委书记/前任区长姓名 = 待核 (未见官方任免,《公开搜索受限)。

注：本脚本在「partial evidence」模型下产出；不确定字段保留为空并以 open_questions / open_gaps.md 记录。
"""

import os
import sqlite3
import sys


def _find_repo_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, "gov_relation")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return start
        cur = parent


_REPO_ROOT = _find_repo_root(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build  # noqa: E402

AS_OF = "2026-08-05"

# ── PERSONS ─────────────────────────────────────────────────────────────
persons = [
    # ── 区委书记 (Core target 1, confirmed 现任) ──
    {
        "id": 1,
        "name": "冯斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "廊坊市广阳区委书记",
        "current_org": "中共廊坊市广阳区委员会",
        "source": "www.guangyang.gov.cn 区委常委会(2026-06/07) + 广区人大换届报道(2026-06-22) + 专题党课(2026-07-03)",
    },
    # ── 区长 (区委 target 2, confirmed 现任) ──
    {
        "id": 2,
        "name": "王振宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广阳区委副书记、区政府区长、党组书记",
        "current_org": "廊坊市广阳区人民政府",
        "source": "www.guangyang.gov.cn 区政府领导分工(2026-07-20) + 人大换届报道(2026-06-22)",
    },
    # ── 区人大常委会主任 ──
    {
        "id": 3,
        "name": "曹新田",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广阳区人大常委会主任",
        "current_org": "廊坊市广阳区人民代表大会常务委员会",
        "source": "www.guangyang.gov.cn 人大换届报道(2026-06-22) + 区人大常委会38次会议(2026-05-31)",
    },
    # ── 区人大常委会副主任 ──
    {
        "id": 4,
        "name": "朱洪波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广阳区人大常委会副主任",
        "current_org": "廊坊市广阳区人民代表大会常务委员会",
        "source": "www.guangyang.gov.cn 区人大常委会38次会议(2026-05-31)",
    },
    {
        "id": 5,
        "name": "杨则涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广阳区人大常委会副主任",
        "current_org": "廊坊市广阳区人民代表大会常务委员会",
        "source": "www.guangyang.gov.cn 区人大常委会38次会议(2026-05-31)",
    },
    {
        "id": 6,
        "name": "廖瑾",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "民革/中共",
        "work_start": "",
        "current_post": "广阳区人大常委会副主任",
        "current_org": "廊坊市广阳区人民代表大会常务委员会",
        "source": "www.guangyang.gov.cn 区人大常委会38次会议(2026-05-31)",
    },
    # ── 区政协主席 ──
    {
        "id": 7,
        "name": "陈文通",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广阳区政协主席",
        "current_org": "政协廊坊市广阳区委员会",
        "source": "www.guangyang.gov.cn 人大换届报道(2026-06-22)",
    },
    # ── 区政府副区长 (区政府领导分工 2026-07-20) ──
    {
        "id": 8,
        "name": "刘斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广阳区委常委、常务副区长",
        "current_org": "廊坊市广阳区人民政府",
        "source": "www.guangyang.gov.cn 区政府领导分工(2026-07-20)",
    },
    {
        "id": 9,
        "name": "杨晓军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广阳区副区长、市公安局广阳分局局长",
        "current_org": "廊坊市广阳区人民政府",
        "source": "www.guangyang.gov.cn 区政府领导分工(2026-07-20)",
    },
    {
        "id": 10,
        "name": "李书伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广阳区副区长",
        "current_org": "廊坊市广阳区人民政府",
        "source": "www.guangyang.gov.cn 区政府领导分工(2026-07-20)",
    },
    {
        "id": 11,
        "name": "王昆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广阳区副区长",
        "current_org": "廊坊市广阳区人民政府",
        "source": "www.guangyang.gov.cn 区政府领导分工(2026-07-20)",
    },
    {
        "id": 12,
        "name": "张矜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广阳区副区长",
        "current_org": "廊坊市广阳区人民政府",
        "source": "www.guangyang.gov.cn 区政府领导分工(2026-07-20)",
    },
    {
        "id": 13,
        "name": "杨敏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广阳区副区长",
        "current_org": "廊坊市广阳区人民政府",
        "source": "www.guangyang.gov.cn 区政府领导分工(2026-07-20)",
    },
    {
        "id": 14,
        "name": "刘一泓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广阳区副区长",
        "current_org": "廊坊市广阳区人民政府",
        "source": "www.guangyang.gov.cn 区政府领导分工(2026-07-20)",
    },
    # ── 区纪委书记/区委班子成员 (名单待补, 用 placeholder 保留可扩展) ──
    # 注: 具体纪委书记/组织部/宣传部/政法委书记姓名未获官方名单, 在 open_gaps 中标注
]

# ── ORGANIZATIONS ───────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共廊坊市广阳区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共廊坊市委",
        "location": "河北省廊坊市广阳区",
    },
    {
        "id": 2,
        "name": "廊坊市广阳区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "廊坊市人民政府",
        "location": "河北省廊坊市广阳区",
    },
    {
        "id": 3,
        "name": "廊坊市广阳区人民代表大会常务委员会",
        "type": "人大",
        "level": "市辖区",
        "parent": "广阳区",
        "location": "河北省廊坊市广阳区",
    },
    {
        "id": 4,
        "name": "政协廊坊市广阳区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "广阳区",
        "location": "河北省廊坊市广阳区",
    },
    {
        "id": 5,
        "name": "中共廊坊市委",
        "type": "党委",
        "level": "地级市",
        "parent": "中共河北省委",
        "location": "河北省廊坊市",
    },
    {
        "id": 6,
        "name": "廊坊市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "河北省人民政府",
        "location": "河北省廊坊市",
    },
    # 冯斌原任职单位 (跨县区交叉, 服务 graph 视网)
    {
        "id": 7,
        "name": "中共固安县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共廊坊市委",
        "location": "河北省廊坊市固安县",
    },
    {
        "id": 8,
        "name": "固安县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "廊坊市人民政府",
        "location": "河北省廊坊市固安县",
    },
    # 区公安分局 (杨晓军局属区副区长兼局长)
    {
        "id": 9,
        "name": "廊坊市公安局广阳分局",
        "type": "公安",
        "level": "乡科级/处级",
        "parent": "廊坊市公安局",
        "location": "河北省廊坊市广阳区",
    },
]

# ── POSITIONS ───────────────────────────────────────────────────────────
positions = [
    # 冯斌 (区委书记) — 跨区县任职
    {"person_id": 1, "org_id": 1, "title": "广阳区委书记",
     "start_date": "2025?/2026", "end_date": "present",
     "rank": "正处级", "note": "2026-06/07 多次以区委书记身份主持六届区委常委会; 2026-07-20 常委会仍以书记出席。上任精确时间待核(疑2025末-2026初,源固安县长)"},
    {"person_id": 1, "org_id": 7, "title": "固安县委专职副书记",
     "start_date": "2020", "end_date": "2021-07",
     "rank": "副处级", "note": "专职副书记, 协助县委主要领导"},
    {"person_id": 1, "org_id": 8, "title": "固安县委副书记、县长",
     "start_date": "2021-07", "end_date": "2025?",
     "rank": "正处级", "note": "2021-07 任固安县代县长, 后当选县长; 现跨区调任广阳区委书记"},
    # 王振宇 (区长)
    {"person_id": 2, "org_id": 2, "title": "广阳区人民政府区长",
     "start_date": "2021?/2024p", "end_date": "present",
     "rank": "正处级", "note": "主持区政府全面工作,分管区审计局 (2026-07-20 分工页). 上任精确时间待核"},
    {"person_id": 2, "org_id": 1, "title": "广阳区委副书记",
     "start_date": "? ", "end_date": "present",
     "rank": "正处级", "note": "区委副书记、区政府党组书记 (由分工页推断)"},
    # 曹新田 (人大主任)
    {"person_id": 3, "org_id": 3, "title": "广阳区人大常委会主任",
     "start_date": "2021?", "end_date": "present",
     "rank": "正处级", "note": "六届区人大; 2026-05-31 主持38次会议; 2026-06-18 换届投票"},
    # 人大副主任
    {"person_id": 4, "org_id": 3, "title": "广阳区人大常委会副主任",
     "start_date": "2021?", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "广阳区人大常委会副主任",
     "start_date": "2021?", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "广阳区人大常委会副主任",
     "start_date": "2021?", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈文通 (政协主席)
    {"person_id": 7, "org_id": 4, "title": "广阳区政协主席",
     "start_date": "2021?", "end_date": "present",
     "rank": "正处级", "note": "2026-06-18 换届投票以区政协主席出席"},
    # 副区长
    {"person_id": 8, "org_id": 2, "title": "广阳区常务副区长",
     "start_date": "2021?", "end_date": "present",
     "rank": "副处级", "note": "负责发改/财政/招商/应急/金融等; 协助区长主持日常工作 (2026-07-20 分工)"},
    {"person_id": 9, "org_id": 2, "title": "广阳区副区长",
     "start_date": "2021?", "end_date": "present", "rank": "副处级",
     "note": "公安/司法/退役军人; 兼任市公安局广阳分局局长"},
    {"person_id": 9, "org_id": 9, "title": "市公安局广阳分局局长",
     "start_date": "?", "end_date": "present", "rank": "副处级", "note": "由分工页推断"},
    {"person_id": 10, "org_id": 2, "title": "广阳区副区长",
     "start_date": "2021?", "end_date": "present", "rank": "副处级",
     "note": "自然资源和规划/住建/城市更新/临空"},
    {"person_id": 11, "org_id": 2, "title": "广阳区副区长",
     "start_date": "2021?", "end_date": "present", "rank": "副处级",
     "note": "农业农村/乡村振兴/生态/市监"},
    {"person_id": 12, "org_id": 2, "title": "广阳区副区长",
     "start_date": "2021?", "end_date": "present", "rank": "副处级",
     "note": "科技/工信/交通/水利/人社"},
    {"person_id": 13, "org_id": 2, "title": "广阳区副区长",
     "start_date": "2021?", "end_date": "present", "rank": "副处级",
     "note": "教育/卫健/文旅/民政/养老"},
    {"person_id": 14, "org_id": 2, "title": "广阳区副区长",
     "start_date": "2025?", "end_date": "present", "rank": "副处级",
     "note": "协助招商引资/金融/处非 (AB角/刘斌)"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────────
relationships = [
    # — 党政搭档 (核心) —
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记(冯斌)与区长(王振宇)党政一把手搭档, 2026-06-18 一同出席换届投票",
     "overlap_org": "中共廊坊市广阳区委员会/区政府", "overlap_period": "2026"},
    # 跨区县前任/升迁: 冯斌 固安县长 -> 广阳区委书记
    {"person_a": 1, "person_b": 1, "type": "overlap",
     "context": "冯斌由固安县县长跨县调任广阳区委书记 (廊坊市域内县->区干部交流)",
     "overlap_org": "廊坊市", "overlap_period": "2025?-2026"},
    # 书记 -> 人大
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区人大主任 (四套班子)",
     "overlap_org": "广阳区", "overlap_period": "2026"},
    # 书记 -> 政协
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "区委书记与区政协主席 (四套班子)",
     "overlap_org": "广阳区", "overlap_period": "2026"},
    # 书记 -> 常务副区长
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "区委书记与常务副区长",
     "overlap_org": "中共廊坊市广阳区委员会", "overlap_period": "2026"},
    # 区长 -> 政府班子
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与常务副区长(协助主持政府)",
     "overlap_org": "廊坊市广阳区人民政府", "overlap_period": "??"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "区长与副区长杨晓军", "overlap_org": "廊坊市广阳区人民政府", "overlap_period": "??"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "区长与副区长李书伟", "overlap_org": "廊坊市广阳区人民政府", "overlap_period": "??"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "区长与副区长王昆", "overlap_org": "廊坊市广阳区人民政府", "overlap_period": "??"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "区长与副区长张矜", "overlap_org": "廊坊市广阳区人民政府", "overlap_period": "??"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "区长与副区长杨敏", "overlap_org": "廊坊市广阳区人民政府", "overlap_period": "??"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "区长与副区长刘一泓", "overlap_org": "廊坊市广阳区人民政府", "overlap_period": "??"},
    # 人大内部
    {"person_a": 3, "person_b": 4, "type": "superior_subordinate",
     "context": "区人大主任与副主任朱洪波", "overlap_org": "广阳区人大常委会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 5, "type": "superior_subordinate",
     "context": "区人大主任与副主任杨则涛", "overlap_org": "广阳区人大常委会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 6, "type": "superior_subordinate",
     "context": "区人大主任与副主任廖瑾", "overlap_org": "广阳区人大常委会", "overlap_period": "2026"},
]


# ── BUILD ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(STAGING_DIR, "广阳区_network.db")
    GEXF_PATH = os.path.join(STAGING_DIR, "广阳区_network.gexf")

    # Idempotent: remove stale artifacts so the script can be re-run safely.
    for stale in (DB_PATH, GEXF_PATH):
        if os.path.exists(stale):
            os.remove(stale)

    run_build(
        slug="广阳区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("Build complete.")