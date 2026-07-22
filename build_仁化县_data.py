#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仁化县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 韶关市
Region: 仁化县
Targets: 县委书记 & 县长

Research Sources:
- 仁化县人民政府门户网站 (www.sgrh.gov.cn)
- 仁化县领导之窗 (sgrh.gov.cn/zwgk/stbz/rhxrmzf/)
- 仁化县政府新闻存档 (sgrh.gov.cn/xwzx/)
- Wikipedia: 仁化县

Current status (as of 2026-07-22):
- 县委书记: 张毅（2026年4月－）
- 县长: 刘拥军（2024年10月－）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "仁化县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 县委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "张毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共仁化县委书记",
        "current_org": "中共仁化县委员会",
        "source": "仁化县人民政府官网 (sgrh.gov.cn), 新闻: 县委十四届第193次常委会会议 (2026-07-21)"
    },
    {
        "id": 2,
        "name": "刘拥军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历，法律硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共仁化县委副书记、县长",
        "current_org": "仁化县人民政府",
        "source": "仁化县领导之窗官方个人页面 (sgrh.gov.cn/zwgk/stbz/rhxrmzf/content/post_2622368.html)"
    },
    {
        "id": 3,
        "name": "陈晟平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仁化县委常委、常务副县长",
        "current_org": "仁化县人民政府",
        "source": "仁化县领导之窗官方页面 (sgrh.gov.cn/zwgk/stbz/rhxrmzf/content/post_2551241.html)"
    },
    {
        "id": 4,
        "name": "潘文辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仁化县委常委、县政府党组成员",
        "current_org": "仁化县人民政府",
        "source": "仁化县领导之窗官方页面 (sgrh.gov.cn/zwgk/stbz/rhxrmzf/content/post_2622266.html)"
    },
    {
        "id": 5,
        "name": "李伟杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仁化县委常委、组织部部长",
        "current_org": "中共仁化县委组织部",
        "source": "南方Plus: 李伟杰发表文章 (2022-11)"
    },
    {
        "id": 6,
        "name": "叶剑斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仁化县副县长",
        "current_org": "仁化县人民政府",
        "source": "仁化县领导之窗官方页面 (sgrh.gov.cn)"
    },
    {
        "id": 7,
        "name": "张伙胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仁化县副县长、县公安局局长",
        "current_org": "仁化县公安局",
        "source": "仁化县领导之窗官方页面 (sgrh.gov.cn)"
    },
    {
        "id": 8,
        "name": "江艳芬",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仁化县副县长",
        "current_org": "仁化县人民政府",
        "source": "仁化县领导之窗官方页面 (sgrh.gov.cn)"
    },
    {
        "id": 9,
        "name": "黄恒超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仁化县副县长",
        "current_org": "仁化县人民政府",
        "source": "仁化县领导之窗官方页面 (sgrh.gov.cn)"
    },
    {
        "id": 10,
        "name": "万志明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仁化县副县长",
        "current_org": "仁化县人民政府",
        "source": "仁化县领导之窗官方页面 (sgrh.gov.cn)"
    },
    {
        "id": 11,
        "name": "叶景秋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仁化县政府党组成员",
        "current_org": "仁化县人民政府",
        "source": "仁化县领导之窗官方页面 (sgrh.gov.cn)"
    },
    {
        "id": 12,
        "name": "董明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仁化县委副书记",
        "current_org": "中共仁化县委员会",
        "source": "仁化县新闻: 县委常委会会议出席 (2026-07)"
    },
    {
        "id": 13,
        "name": "谢建发",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仁化县委副书记",
        "current_org": "中共仁化县委员会",
        "source": "仁化县新闻: 县委常委会会议出席 (2026-07)"
    },
    # ════════════════════════════════════════
    # 前任领导（用于关系网络）
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "陈夏广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中山市副市长（调任）",
        "current_org": "中山市人民政府",
        "source": "Google News: 广东四地市新任命副市长 (2026-01-22); 仁化县政府新闻 (2024-2025)"
    },
    {
        "id": 15,
        "name": "刘锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（已离开仁化县）",
        "current_org": "待查",
        "source": "Wikipedia: 仁化县 (已过时条目, 2025-05); 待进一步核实"
    },
    {
        "id": 16,
        "name": "邱志坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仁化县人大常委会主任",
        "current_org": "仁化县人大常委会",
        "source": "仁化县新闻: 县党代会活动 (2021-10)"
    },
    {
        "id": 17,
        "name": "谢林茂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仁化县政协主席",
        "current_org": "仁化县政协",
        "source": "仁化县新闻: 县党代会活动 (2021-10)"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共仁化县委员会", "type": "党委", "level": "县处级", "parent": "中共韶关市委员会", "location": "广东省韶关市仁化县"},
    {"id": 2, "name": "仁化县人民政府", "type": "政府", "level": "县处级", "parent": "韶关市人民政府", "location": "广东省韶关市仁化县"},
    {"id": 3, "name": "中共仁化县委组织部", "type": "党委", "level": "县处级", "parent": "中共仁化县委员会", "location": "广东省韶关市仁化县"},
    {"id": 4, "name": "仁化县公安局", "type": "政府", "level": "县处级", "parent": "仁化县人民政府", "location": "广东省韶关市仁化县"},
    {"id": 5, "name": "仁化县人大常委会", "type": "人大", "level": "县处级", "parent": "仁化县", "location": "广东省韶关市仁化县"},
    {"id": 6, "name": "仁化县政协", "type": "政协", "level": "县处级", "parent": "仁化县", "location": "广东省韶关市仁化县"},
    {"id": 7, "name": "中山市人民政府", "type": "政府", "level": "地厅级", "parent": "广东省人民政府", "location": "广东省中山市"},
]

# 3. Positions
positions = [
    # 张毅
    {"person_id": 1, "org_id": 1, "title": "中共仁化县委书记", "start": "2026-04", "end": "present", "rank": "县处级正职", "note": "最早可追溯至2026年4月14日'县委书记张毅到县纪委监委机关调研'新闻"},
    # 刘拥军
    {"person_id": 2, "org_id": 2, "title": "仁化县县长", "start": "2024-10", "end": "present", "rank": "县处级正职", "note": "最早出现在2024年10月新闻中"},
    {"person_id": 2, "org_id": 1, "title": "中共仁化县委副书记", "start": "2024-10", "end": "present", "rank": "县处级副职", "note": ""},
    # 陈晟平
    {"person_id": 3, "org_id": 2, "title": "仁化县常务副县长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "仁化县委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    # 潘文辉
    {"person_id": 4, "org_id": 2, "title": "仁化县政府党组成员", "start": "待查", "end": "present", "rank": "县处级副职", "note": "负责水务工作"},
    {"person_id": 4, "org_id": 1, "title": "仁化县委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    # 李伟杰
    {"person_id": 5, "org_id": 3, "title": "仁化县委组织部部长", "start": "待查", "end": "present", "rank": "县处级副职", "note": "2022年已有此身份"},
    {"person_id": 5, "org_id": 1, "title": "仁化县委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    # 叶剑斌
    {"person_id": 6, "org_id": 2, "title": "仁化县副县长", "start": "待查", "end": "present", "rank": "县处级副职", "note": "分管教育、民政、退役军人、卫生健康、红十字会"},
    # 张伙胜
    {"person_id": 7, "org_id": 2, "title": "仁化县副县长、县公安局局长", "start": "待查", "end": "present", "rank": "县处级副职", "note": "负责公安、维稳"},
    {"person_id": 7, "org_id": 4, "title": "仁化县公安局局长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    # 江艳芬
    {"person_id": 8, "org_id": 2, "title": "仁化县副县长", "start": "待查", "end": "present", "rank": "县处级副职", "note": "分管农业农村、林业、乡村振兴、供销"},
    # 黄恒超
    {"person_id": 9, "org_id": 2, "title": "仁化县副县长", "start": "待查", "end": "present", "rank": "县处级副职", "note": "分管住建、交通运输、人社、医保"},
    # 万志明
    {"person_id": 10, "org_id": 2, "title": "仁化县副县长", "start": "待查", "end": "present", "rank": "县处级副职", "note": "分管工业信息、科技商务、招商引资、生态环境"},
    # 叶景秋
    {"person_id": 11, "org_id": 2, "title": "仁化县政府党组成员", "start": "待查", "end": "present", "rank": "县处级副职", "note": "虎门-仁化对口帮扶协作"},
    # 董明
    {"person_id": 12, "org_id": 1, "title": "仁化县委副书记", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    # 谢建发
    {"person_id": 13, "org_id": 1, "title": "仁化县委副书记", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    # 陈夏广
    {"person_id": 14, "org_id": 1, "title": "中共仁化县委书记（前）", "start": "2024-02", "end": "2026-03", "rank": "县处级正职", "note": "最早2024年2月确认就职"},
    {"person_id": 14, "org_id": 2, "title": "仁化县县长（前）", "start": "待查", "end": "2024-09", "rank": "县处级正职", "note": "后升任县委书记"},
    {"person_id": 14, "org_id": 7, "title": "中山市副市长", "start": "2026-01", "end": "present", "rank": "地厅级副职", "note": "2026年1月22日任命"},
    # 刘锋
    {"person_id": 15, "org_id": 1, "title": "中共仁化县委书记（前）", "start": "待查", "end": "2024-01", "rank": "县处级正职", "note": "Wikipedia已过时记录"},
    # 邱志坚
    {"person_id": 16, "org_id": 5, "title": "仁化县人大常委会主任", "start": "待查", "end": "present", "rank": "县处级正职", "note": ""},
    # 谢林茂
    {"person_id": 17, "org_id": 6, "title": "仁化县政协主席", "start": "待查", "end": "present", "rank": "县处级正职", "note": ""},
]

# 4. Relationships
relationships = [
    # 县委书记-县长（上下级合作关系）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政领导搭档", "overlap_org": "中共仁化县委员会/仁化县人民政府", "overlap_period": "2026-04至今"},
    # 县委书记-常务副县长
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与常务副县长", "overlap_org": "中共仁化县委员会/仁化县人民政府", "overlap_period": "2026-04至今"},
    # 县长-常务副县长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与常务副县长（助手）", "overlap_org": "仁化县人民政府", "overlap_period": "2024-10至今"},
    # 县委书记-县委常委
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共仁化县委员会", "overlap_period": "2026-04至今"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与组织部长", "overlap_org": "中共仁化县委员会", "overlap_period": "2026-04至今"},
    # 前任-现任县委书记
    {"person_a": 14, "person_b": 1, "type": "predecessor_successor", "context": "县委书记更替", "overlap_org": "中共仁化县委员会", "overlap_period": "2026-03/04"},
    # 前任县委书记-现任县长
    {"person_a": 14, "person_b": 2, "type": "superior_subordinate", "context": "前任县委书记与县长搭档", "overlap_org": "中共仁化县委员会/仁化县人民政府", "overlap_period": "2024-10至2026-03"},
    # 前任县委书记-前前县委书记
    {"person_a": 14, "person_b": 15, "type": "predecessor_successor", "context": "县委书记更替（刘锋→陈夏广）", "overlap_org": "中共仁化县委员会", "overlap_period": "约2024年初"},
    # 县长-副县长们
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "仁化县人民政府", "overlap_period": "2024-10至今"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长兼公安局长", "overlap_org": "仁化县人民政府", "overlap_period": "2024-10至今"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "仁化县人民政府", "overlap_period": "2024-10至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "仁化县人民政府", "overlap_period": "2024-10至今"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "仁化县人民政府", "overlap_period": "2024-10至今"},
    # 县委班子成员之间
    {"person_a": 12, "person_b": 13, "type": "overlap", "context": "两位县委副书记同届共事", "overlap_org": "中共仁化县委员会", "overlap_period": "待查至今"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共仁化县委员会", "overlap_period": "待查至今"},
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共仁化县委员会", "overlap_period": "待查至今"},
]

# ── Run Build ──
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
    print(f"Done! DB: {DB_PATH}")
    print(f"Done! GEXF: {GEXF_PATH}")
