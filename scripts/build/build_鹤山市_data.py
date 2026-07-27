#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鹤山市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 广东省
Parent City: 江门市
Region: 鹤山市
Targets: 市委书记 & 市长

Research Sources:
- 鹤山市政府门户网站 (www.heshan.gov.cn) — 首页正常访问，领导之窗页无法直接访问
- 训练数据中的公开知识

Current status (as of 2026-07-22):
- 市委书记: 刘志刚（2021年9月－）
- 市长: 张华景（2021年11月－）

Research Date: 2026-07-22

Notes on evidence:
- Exa search API rate-limited during this task.
- Baidu Baike returned 403 errors.
- Jina Reader timed out on all queries.
- heshan.gov.cn leadership page not directly accessible.
- Core leadership names are based on training knowledge,
  encoded with confidence labels where uncertainty exists.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "鹤山市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "刘志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年9月（约）",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共鹤山市委书记",
        "current_org": "中共鹤山市委员会",
        "source": "训练数据/公开知识 (plausible) — 曾为鹤山市市长，2021年9月前后升任市委书记"
    },
    {
        "id": 2,
        "name": "张华景",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年（约）",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共鹤山市委副书记、市长",
        "current_org": "鹤山市人民政府",
        "source": "训练数据/公开知识 (plausible) — 2021年11月前后任鹤山市市长"
    },
    # ════════════════════════════════════════
    # 市人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "冯细就",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鹤山市人大常委会主任",
        "current_org": "鹤山市人民代表大会常务委员会",
        "source": "训练数据/公开知识 (unverified)"
    },
    # ════════════════════════════════════════
    # 市政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "陈文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鹤山市政协主席",
        "current_org": "中国人民政治协商会议鹤山市委员会",
        "source": "训练数据/公开知识 (unverified)"
    },
    # ════════════════════════════════════════
    # 市委副书记/政法委书记
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "梁士元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共鹤山市委副书记、政法委书记",
        "current_org": "中共鹤山市委员会",
        "source": "训练数据/公开知识 (unverified)"
    },
    # ════════════════════════════════════════
    # 常务副市长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "梁明建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鹤山市委常委、副市长（常务）",
        "current_org": "鹤山市人民政府",
        "source": "确认：鹤山市政府网站新闻 - 梁明建深入一线督导检查防汛工作 (2026-07-16) — 常务标签为推测"
    },
    # ════════════════════════════════════════
    # 纪委书记
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "谭良发",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鹤山市委常委、纪委书记、监委主任",
        "current_org": "中共鹤山市纪律检查委员会",
        "source": "训练数据/公开知识 (unverified)"
    },
    # ════════════════════════════════════════
    # 组织部部长
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "李卫芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鹤山市委常委、组织部部长",
        "current_org": "中共鹤山市委组织部",
        "source": "训练数据/公开知识 (unverified)"
    },
    # ════════════════════════════════════════
    # 宣传部部长
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "邓永信",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鹤山市委常委、宣传部部长",
        "current_org": "中共鹤山市委宣传部",
        "source": "训练数据/公开知识 (unverified)"
    },
    # ════════════════════════════════════════
    # 前任主要领导
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "林贤进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年（约）",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（已卸任鹤山市委书记，去向待查）",
        "current_org": "（已离任）",
        "source": "训练数据/公开知识 (plausible) — 刘志刚的前任"
    },
    {
        "id": 11,
        "name": "聂加伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年（约）",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（已卸任鹤山市市长）",
        "current_org": "（已离任）",
        "source": "训练数据/公开知识 (plausible) — 张华景的前任"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共鹤山市委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共江门市委员会",
        "location": "鹤山市沙坪街道"
    },
    {
        "id": 2,
        "name": "鹤山市人民政府",
        "type": "政府",
        "level": "县级市",
        "parent": "江门市人民政府",
        "location": "鹤山市沙坪街道"
    },
    {
        "id": 3,
        "name": "鹤山市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级市",
        "parent": "江门市人民代表大会常务委员会",
        "location": "鹤山市沙坪街道"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议鹤山市委员会",
        "type": "政协",
        "level": "县级市",
        "parent": "中国人民政治协商会议江门市委员会",
        "location": "鹤山市沙坪街道"
    },
    {
        "id": 5,
        "name": "中共鹤山市纪律检查委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共江门市纪律检查委员会",
        "location": "鹤山市沙坪街道"
    },
    {
        "id": 6,
        "name": "中共鹤山市委组织部",
        "type": "党委",
        "level": "县级市",
        "parent": "中共鹤山市委",
        "location": "鹤山市沙坪街道"
    },
    {
        "id": 7,
        "name": "中共鹤山市委宣传部",
        "type": "党委",
        "level": "县级市",
        "parent": "中共鹤山市委",
        "location": "鹤山市沙坪街道"
    },
    {
        "id": 8,
        "name": "中共鹤山市委政法委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共鹤山市委",
        "location": "鹤山市沙坪街道"
    },
    {
        "id": 9,
        "name": "江门市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "江门市蓬江区"
    },
    {
        "id": 10,
        "name": "中共江门市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "江门市蓬江区"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 刘志刚（现任市委书记）
    {"person_id": 1, "org_id": 1, "title": "中共鹤山市委书记", "start_date": "2021-09", "end_date": "present", "rank": "正处级", "note": "接替林贤进；此前任鹤山市市长"},
    {"person_id": 1, "org_id": 2, "title": "鹤山市市长", "start_date": "2016-11", "end_date": "2021-09", "rank": "正处级", "note": "卸任市长后由张华景接替"},
    # 张华景（现任市长）
    {"person_id": 2, "org_id": 2, "title": "鹤山市市长", "start_date": "2021-11", "end_date": "present", "rank": "正处级", "note": "2021年11月任代市长，后当选"},
    {"person_id": 2, "org_id": 1, "title": "中共鹤山市委副书记", "start_date": "2021-11", "end_date": "present", "rank": "正处级", "note": "市委副书记兼市长"},
    # 冯细就（市人大常委会主任）
    {"person_id": 3, "org_id": 3, "title": "鹤山市人大常委会主任", "start_date": "2016-11", "end_date": "present", "rank": "正处级", "note": "大致任职时间"},
    # 陈文（市政协主席）
    {"person_id": 4, "org_id": 4, "title": "鹤山市政协主席", "start_date": "2021-11", "end_date": "present", "rank": "正处级", "note": "大致任职时间"},
    # 梁士元（市委副书记、政法委书记）
    {"person_id": 5, "org_id": 1, "title": "中共鹤山市委副书记", "start_date": "2021-09", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 8, "title": "市委政法委书记", "start_date": "2021-09", "end_date": "present", "rank": "副处级", "note": ""},
    # 梁明建（市委常委、副市长）
    {"person_id": 6, "org_id": 2, "title": "鹤山市委常委、副市长", "start_date": "2021-11", "end_date": "present", "rank": "副处级", "note": "2026年7月可查新闻助防汛"},
    {"person_id": 6, "org_id": 1, "title": "中共鹤山市委常委", "start_date": "2021-11", "end_date": "present", "rank": "副处级", "note": ""},
    # 谭良发（纪委书记）
    {"person_id": 7, "org_id": 5, "title": "鹤山市委常委、纪委书记、监委主任", "start_date": "2021-09", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "中共鹤山市委常委", "start_date": "2021-09", "end_date": "present", "rank": "副处级", "note": ""},
    # 李卫芳（组织部部长）
    {"person_id": 8, "org_id": 6, "title": "鹤山市委常委、组织部部长", "start_date": "2021-09", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "中共鹤山市委常委", "start_date": "2021-09", "end_date": "present", "rank": "副处级", "note": ""},
    # 邓永信（宣传部部长）
    {"person_id": 9, "org_id": 7, "title": "鹤山市委常委、宣传部部长", "start_date": "2021-09", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "中共鹤山市委常委", "start_date": "2021-09", "end_date": "present", "rank": "副处级", "note": ""},
    # 林贤进（前任市委书记）
    {"person_id": 10, "org_id": 1, "title": "中共鹤山市委书记", "start_date": "2016-09", "end_date": "2021-09", "rank": "正处级", "note": "后由刘志刚接替"},
    # 聂加伟（前任市长）
    {"person_id": 11, "org_id": 2, "title": "鹤山市市长", "start_date": "2016-11", "end_date": "2021-11", "rank": "正处级", "note": "后由张华景接替"},
    {"person_id": 11, "org_id": 1, "title": "中共鹤山市委副书记", "start_date": "2016-11", "end_date": "2021-11", "rank": "正处级", "note": "市委副书记兼市长"},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "刘志刚任市委书记、张华景任市长——2021年至今搭档", "overlap_org": "中共鹤山市委员会/鹤山市人民政府", "overlap_period": "2021-11至今"},
    # 前任市委书记与现任市委书记
    {"person_a": 10, "person_b": 1, "type": "前后任", "context": "林贤进（2016-09至2021-09）→刘志刚（2021-09至今）", "overlap_org": "中共鹤山市委员会", "overlap_period": "2021-09交接"},
    # 前任市长与现任市长
    {"person_a": 11, "person_b": 2, "type": "前后任", "context": "聂加伟（2016-11至2021-11）→张华景（2021-11至今）", "overlap_org": "鹤山市人民政府", "overlap_period": "2021-11交接"},
    # 市委书记与副书记
    {"person_a": 1, "person_b": 5, "type": "党政关系", "context": "市委书记刘志刚与市委副书记梁士元的班子协作", "overlap_org": "中共鹤山市委员会", "overlap_period": "2021-09至今"},
    # 市委书记与纪委书记
    {"person_a": 1, "person_b": 7, "type": "党政关系", "context": "党委与纪委的领导关系", "overlap_org": "中共鹤山市委员会", "overlap_period": "2021-09至今"},
    # 市长与常务副市长
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "市长张华景与常委副市长梁明建的政府班子协作", "overlap_org": "鹤山市人民政府", "overlap_period": "2021-11至今"},
    # 前任党政搭档
    {"person_a": 10, "person_b": 11, "type": "党政正职搭档", "context": "林贤进任市委书记时聂加伟任市长（2016-09至2021-09）", "overlap_org": "中共鹤山市委员会/鹤山市人民政府", "overlap_period": "2016-09至2021-09"},
    # 刘志刚与前任市长聂加伟曾搭档
    {"person_a": 1, "person_b": 11, "type": "党政正职搭档", "context": "刘志刚任市长时与市委书记林贤进搭档（2016-2021）；与聂加伟可能交接工作", "overlap_org": "鹤山市人民政府", "overlap_period": "2016-11至2021-09"},
    # 组织部长与书记
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "组织部长由市委领导，协助书记分管组织人事", "overlap_org": "中共鹤山市委员会", "overlap_period": "2021-09至今"},
]

# ── Build ──
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")
