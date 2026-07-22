#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
连州市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 广东省
Parent City: 清远市
Region: 连州市
Targets: 市委书记 & 市长

Research Sources:
- 连州市人民政府网 — 领导之窗 (www.lianzhou.gov.cn)
  - 市委: /zglzsw/
  - 市政府: /lzsrmzf/

Current status (as of 2026-07-22):
- 市委书记: 潘正焕（1980年7月生，研究生）
- 市长: 戴少枚（1978年8月生，大学）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "连州市"
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
        "name": "潘正焕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年7月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连州市委书记",
        "current_org": "中共连州市委员会",
        "source": "连州市人民政府网 — 领导之窗: zglzsw/sj/content/post_2143748.html"
    },
    {
        "id": 2,
        "name": "戴少枚",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连州市委副书记、市政府党组书记、市长",
        "current_org": "中共连州市委员会/连州市人民政府",
        "source": "连州市人民政府网 — 领导之窗: zglzsw/fsj/content/post_2151146.html"
    },
    {
        "id": 3,
        "name": "魏巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连州市委副书记（挂职）",
        "current_org": "中共连州市委员会",
        "source": "连州市人民政府网 — 领导之窗: zglzsw/fsj/content/post_2090460.html"
    },
    # ════════════════════════════════════════
    # 市委常委
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "邓勇军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、市委办公室主任、市直机关工委书记、清远民族工业园管委会党组书记，市政府党组副书记、副市长",
        "current_org": "中共连州市委员会/连州市人民政府",
        "source": "连州市人民政府网 — 领导之窗: zglzsw/cw/content/post_2156235.html; lzsrmzf/fsc/content/post_2168818.html"
    },
    {
        "id": 5,
        "name": "岑炜",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1985年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、副市长",
        "current_org": "中共连州市委员会/连州市人民政府",
        "source": "连州市人民政府网 — 领导之窗: zglzsw/cw/content/post_2095667.html"
    },
    {
        "id": 6,
        "name": "陆容新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、组织部部长、党校校长",
        "current_org": "中共连州市委员会",
        "source": "连州市人民政府网 — 领导之窗: zglzsw/cw/content/post_1891602.html"
    },
    {
        "id": 7,
        "name": "张帮东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共连州市委员会/连州市监察委员会",
        "source": "连州市人民政府网 — 领导之窗: zglzsw/cw/content/post_2096122.html"
    },
    {
        "id": 8,
        "name": "李艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共连州市委员会",
        "source": "连州市人民政府网 — 领导之窗: zglzsw/cw/content/post_1967140.html"
    },
    # ════════════════════════════════════════
    # 其他副市长
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "何永锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副市长",
        "current_org": "连州市人民政府",
        "source": "连州市人民政府网 — 领导之窗: lzsrmzf/fsc/content/post_2168818.html"
    },
    {
        "id": 10,
        "name": "吴鹤立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副市长、市公安局局长",
        "current_org": "连州市人民政府",
        "source": "连州市人民政府网 — 领导之窗: lzsrmzf/fsc/content/post_1727668.html"
    },
    {
        "id": 11,
        "name": "赖习兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副市长",
        "current_org": "连州市人民政府",
        "source": "连州市人民政府网 — 领导之窗: lzsrmzf/fsc/content/post_1747478.html"
    },
    {
        "id": 12,
        "name": "朱昆宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副市长（挂任，广州对口帮扶连州）",
        "current_org": "连州市人民政府",
        "source": "连州市人民政府网 — 领导之窗: lzsrmzf/fsc/content/post_1701766.html"
    },
    {
        "id": 13,
        "name": "蔡文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，工学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市政府党组成员、副市长",
        "current_org": "连州市人民政府",
        "source": "连州市人民政府网 — 领导之窗: lzsrmzf/fsc/content/post_1808652.html"
    },
    {
        "id": 14,
        "name": "曾凌飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市政府党组成员、副市长、连州镇党委书记",
        "current_org": "连州市人民政府",
        "source": "连州市人民政府网 — 领导之窗: lzsrmzf/fsc/content/post_2095736.html"
    },
    {
        "id": 15,
        "name": "周静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历，工学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副市长",
        "current_org": "连州市人民政府",
        "source": "连州市人民政府网 — 领导之窗: lzsrmzf/fsc/content/post_2142195.html"
    },
    # ════════════════════════════════════════
    # 人大、政协领导
    # ════════════════════════════════════════
    {
        "id": 16,
        "name": "罗永忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "连州市人大常委会主任",
        "current_org": "连州市人民代表大会常务委员会",
        "source": "连州市人民政府网 — 领导之窗: lzsrdcwh/zr/content/post_2157319.html"
    },
    {
        "id": 17,
        "name": "陈仪宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政协连州市委员会副主席",
        "current_org": "中国人民政治协商会议连州市委员会",
        "source": "连州市人民政府网 — 领导之窗"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共连州市委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共清远市委员会",
        "location": "连州市"
    },
    {
        "id": 2,
        "name": "连州市人民政府",
        "type": "政府",
        "level": "县级市",
        "parent": "清远市人民政府",
        "location": "连州市"
    },
    {
        "id": 3,
        "name": "连州市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级市",
        "parent": "清远市人民代表大会常务委员会",
        "location": "连州市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议连州市委员会",
        "type": "政协",
        "level": "县级市",
        "parent": "中国人民政治协商会议清远市委员会",
        "location": "连州市"
    },
    {
        "id": 5,
        "name": "连州市监察委员会",
        "type": "政府",
        "level": "县级市",
        "parent": "清远市监察委员会",
        "location": "连州市"
    },
    {
        "id": 6,
        "name": "中共清远市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "清远市"
    },
    {
        "id": 7,
        "name": "清远市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "清远市"
    },
    {
        "id": 8,
        "name": "清远民族工业园管委会",
        "type": "开发区",
        "level": "县级",
        "parent": "连州市人民政府",
        "location": "连州市"
    },
    {
        "id": 9,
        "name": "连州市公安局",
        "type": "政府",
        "level": "县级市",
        "parent": "连州市人民政府",
        "location": "连州市"
    },
    {
        "id": 10,
        "name": "连州镇",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "连州市",
        "location": "连州市"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 潘正焕（现任市委书记）
    {"person_id": 1, "org_id": 1, "title": "连州市委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持市委全面工作"},
    # 戴少枚（现任市长）
    {"person_id": 2, "org_id": 2, "title": "连州市市长", "start": "", "end": "present", "rank": "正处级", "note": "市政府党组书记，主持市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "连州市委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 魏巍（挂职副书记）
    {"person_id": 3, "org_id": 1, "title": "连州市委副书记（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "负责'百千万工程'对口帮扶协作工作"},
    # 邓勇军（常委、常务副市长）
    {"person_id": 4, "org_id": 1, "title": "市委常委、市委办公室主任、市直机关工委书记", "start": "", "end": "present", "rank": "副处级", "note": "清远民族工业园管委会党组书记"},
    {"person_id": 4, "org_id": 2, "title": "市政府党组副书记、副市长", "start": "", "end": "present", "rank": "副处级", "note": "协助市长负责市政府日常工作"},
    {"person_id": 4, "org_id": 8, "title": "清远民族工业园管委会党组书记", "start": "", "end": "present", "rank": "", "note": ""},
    # 岑炜（常委、副市长）
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "负责教育、工信、招商、科技、政务服务等"},
    # 陆容新（常委、组织部长）
    {"person_id": 6, "org_id": 1, "title": "市委常委、组织部部长、党校校长", "start": "", "end": "present", "rank": "副处级", "note": "协助书记抓党建工作"},
    # 张帮东（常委、纪委书记）
    {"person_id": 7, "org_id": 1, "title": "市委常委、市纪委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "市监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 李艳（常委、宣传部长）
    {"person_id": 8, "org_id": 1, "title": "市委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": "负责宣传、统战、网络信息安全等"},
    # 副市长
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "负责交通、水利、农业农村、乡村振兴、卫健、医保等"},
    {"person_id": 10, "org_id": 2, "title": "副市长、市公安局局长", "start": "", "end": "present", "rank": "副处级", "note": "负责公安、司法、依法治市"},
    {"person_id": 10, "org_id": 9, "title": "市公安局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "负责民政、人社、文旅、体育、退役军人、信访、生态环境等"},
    {"person_id": 12, "org_id": 2, "title": "副市长（挂任）", "start": "", "end": "present", "rank": "副处级", "note": "广州对口帮扶连州协作工作"},
    {"person_id": 13, "org_id": 2, "title": "市政府党组成员、副市长", "start": "", "end": "present", "rank": "副处级", "note": "负责自然资源、住建、城管、林业等"},
    {"person_id": 14, "org_id": 2, "title": "市政府党组成员、副市长", "start": "", "end": "present", "rank": "副处级", "note": "兼连州镇党委书记"},
    {"person_id": 14, "org_id": 10, "title": "连州镇党委书记", "start": "", "end": "present", "rank": "正科级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "分工待定"},
    # 人大、政协
    {"person_id": 16, "org_id": 3, "title": "连州市人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 4, "title": "政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# 4. Relationships
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "潘正焕（市委书记）与戴少枚（市长）是连州市最重要的党政搭档", "overlap_org": "中共连州市委员会/连州市人民政府", "overlap_period": "至今"},
    # 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "上下级关系", "context": "潘正焕与魏巍（挂职副书记）为市委班子上下级", "overlap_org": "中共连州市委员会", "overlap_period": "至今"},
    # 书记与常委
    {"person_a": 1, "person_b": 4, "type": "上下级关系", "context": "潘正焕与邓勇军（常委、市委办主任、常务副市长）为市委班子上下级，邓勇军负责协调市委具体工作运转", "overlap_org": "中共连州市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级关系", "context": "潘正焕与陆容新（常委、组织部长）为市委班子上下级，陆容新协助书记抓党建工作", "overlap_org": "中共连州市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级关系", "context": "潘正焕与张帮东（常委、纪委书记）为市委班子上下级", "overlap_org": "中共连州市委员会", "overlap_period": "至今"},
    # 市长与副市长
    {"person_a": 2, "person_b": 4, "type": "上下级关系", "context": "戴少枚与邓勇军（常务副市长）为市政府正副职", "overlap_org": "连州市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级关系", "context": "戴少枚与岑炜（常委、副市长）为市政府正副职", "overlap_org": "连州市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级关系", "context": "戴少枚与何永锋为市政府正副职", "overlap_org": "连州市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "上下级关系", "context": "戴少枚与吴鹤立（副市长兼公安局局长）为市政府正副职", "overlap_org": "连州市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "上下级关系", "context": "戴少枚与赖习兴为市政府正副职", "overlap_org": "连州市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "上下级关系", "context": "戴少枚与蔡文为市政府正副职", "overlap_org": "连州市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "上下级关系", "context": "戴少枚与曾凌飞（副市长兼连州镇党委书记）为市政府正副职", "overlap_org": "连州市人民政府", "overlap_period": "至今"},
    # 常委同僚关系
    {"person_a": 4, "person_b": 5, "type": "同僚关系", "context": "邓勇军（常务副市长）与岑炜（常委、副市长、协助邓勇军分管工业园）为政府副职同僚", "overlap_org": "连州市人民政府", "overlap_period": "至今"},
    {"person_a": 6, "person_b": 8, "type": "同僚关系", "context": "陆容新（组织部长）与李艳（宣传部长）均为市委常委", "overlap_org": "中共连州市委员会", "overlap_period": "至今"},
    {"person_a": 7, "person_b": 8, "type": "同僚关系", "context": "张帮东（纪委书记）与李艳（宣传部长）均为市委常委", "overlap_org": "中共连州市委员会", "overlap_period": "至今"},
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
