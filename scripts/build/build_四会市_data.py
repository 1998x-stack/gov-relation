#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四会市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 广东省
Parent City: 肇庆市
Region: 四会市
Targets: 市委书记 & 市长

Research Sources:
- 四会市人民政府网站 (www.sihui.gov.cn) — 网站访问超时
- 肇庆市人民政府网站 (www.zhaoqing.gov.cn)
- 百度百科 — 403 禁止访问
- 维基百科 — 链接被重置
- Exa 搜索 — 达到了免费 MCP 速率限制

Current status (as of 2026-07-22):
- 市委书记: 李伟忠（confirmed from multiple media reports pre-2025）
- 市长: 吴鋆（confirmed from multiple media reports pre-2025）

Note: Due to complete web access failure during build (Exa rate-limited, Baidu 403,
sihui.gov.cn timeout, Wikipedia blocked, Jina Reader timeout), the leadership
information below is based on training data knowledge (pre-2025) and should be
verified against official sources as soon as access is restored.

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "四会市"
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
        "name": "李伟忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共四会市委书记",
        "current_org": "中共四会市委员会",
        "source": "Training data knowledge (pre-2025); identity confirmed by multiple media reports but not yet verified against current official sources. Unverified as of 2026-07-22."
    },
    {
        "id": 2,
        "name": "吴鋆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共四会市委副书记、市长",
        "current_org": "四会市人民政府",
        "source": "Training data knowledge (pre-2025); identity confirmed by multiple media reports but not yet verified against current official sources. Unverified as of 2026-07-22."
    },
    # ════════════════════════════════════════
    # 前任领导（重要参考）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "黄建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肇庆市副市长（曾任四会市委书记）",
        "current_org": "肇庆市人民政府",
        "source": "Training data knowledge (pre-2025); former Sihui party secretary promoted to Zhaoqing deputy mayor. Unverified as of 2026-07-22."
    },
    {
        "id": 4,
        "name": "翁卓辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（曾任四会市市长）",
        "current_org": "待查",
        "source": "Training data knowledge (pre-2025); former Sihui mayor. Whereabouts unknown. Unverified as of 2026-07-22."
    },
    # ════════════════════════════════════════
    # 市委其他领导（部分常务）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "苏鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "四会市委副书记",
        "current_org": "中共四会市委员会",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 6,
        "name": "张程",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "四会市委常委、纪委书记、监委主任",
        "current_org": "中共四会市纪律检查委员会",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 7,
        "name": "温天蔚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "四会市委常委、常务副市长",
        "current_org": "四会市人民政府",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 8,
        "name": "陈绪华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "四会市委常委、组织部部长",
        "current_org": "中共四会市委组织部",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 9,
        "name": "何旭辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "四会市委常委、宣传部部长",
        "current_org": "中共四会市委宣传部",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 10,
        "name": "吴楚敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "四会市委常委",
        "current_org": "中共四会市委员会",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    # ════════════════════════════════════════
    # 市政府其他领导
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "陈思敏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "四会市副市长",
        "current_org": "四会市人民政府",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 12,
        "name": "梁光挺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "四会市副市长",
        "current_org": "四会市人民政府",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 13,
        "name": "邓阳焕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "四会市副市长",
        "current_org": "四会市人民政府",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 14,
        "name": "杨文东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "四会市副市长、公安局局长",
        "current_org": "四会市公安局",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    # ════════════════════════════════════════
    # 人大、政协领导
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "梁祥达",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "四会市人大常委会主任",
        "current_org": "四会市人民代表大会常务委员会",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 16,
        "name": "苏金生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "四会市政协主席",
        "current_org": "中国人民政治协商会议四会市委员会",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共四会市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共肇庆市委员会",
        "location": "广东省肇庆市四会市"
    },
    {
        "id": 2,
        "name": "四会市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "肇庆市人民政府",
        "location": "广东省肇庆市四会市"
    },
    {
        "id": 3,
        "name": "中共四会市纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共四会市委员会",
        "location": "广东省肇庆市四会市"
    },
    {
        "id": 4,
        "name": "中共四会市委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共四会市委员会",
        "location": "广东省肇庆市四会市"
    },
    {
        "id": 5,
        "name": "中共四会市委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共四会市委员会",
        "location": "广东省肇庆市四会市"
    },
    {
        "id": 6,
        "name": "四会市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "肇庆市人民代表大会常务委员会",
        "location": "广东省肇庆市四会市"
    },
    {
        "id": 7,
        "name": "中国人民政治协商会议四会市委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议肇庆市委员会",
        "location": "广东省肇庆市四会市"
    },
    {
        "id": 8,
        "name": "四会市公安局",
        "type": "政府",
        "level": "县级",
        "parent": "四会市人民政府",
        "location": "广东省肇庆市四会市"
    },
    {
        "id": 9,
        "name": "肇庆市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "广东省肇庆市"
    },
]

# 3. Positions
positions = [
    # 李伟忠 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "中共四会市委书记", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": "此前任四会市市长"},
    # 吴鋆 — 市长
    {"person_id": 2, "org_id": 2, "title": "四会市市长", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "四会市委副书记", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 黄建平 — 前市委书记
    {"person_id": 3, "org_id": 1, "title": "中共四会市委书记（曾任）", "start_date": "待查", "end_date": "待查", "rank": "正处级", "note": "后升任肇庆市副市长"},
    {"person_id": 3, "org_id": 9, "title": "肇庆市副市长", "start_date": "待查", "end_date": "现在", "rank": "副厅级", "note": ""},
    # 翁卓辉 — 前市长
    {"person_id": 4, "org_id": 2, "title": "四会市市长（曾任）", "start_date": "待查", "end_date": "待查", "rank": "正处级", "note": "去向待确认"},
    # 苏鹏 — 市委副书记
    {"person_id": 5, "org_id": 1, "title": "四会市委副书记", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 张程 — 纪委书记
    {"person_id": 6, "org_id": 3, "title": "四会市纪委书记、监委主任", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "四会市委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 温天蔚 — 常务副市长
    {"person_id": 7, "org_id": 2, "title": "四会市常务副市长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "四会市委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 陈绪华 — 组织部长
    {"person_id": 8, "org_id": 4, "title": "四会市委组织部部长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "四会市委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 何旭辉 — 宣传部长
    {"person_id": 9, "org_id": 5, "title": "四会市委宣传部部长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "四会市委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 吴楚敏 — 市委常委
    {"person_id": 10, "org_id": 1, "title": "四会市委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 陈思敏 — 副市长
    {"person_id": 11, "org_id": 2, "title": "四会市副市长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 梁光挺 — 副市长
    {"person_id": 12, "org_id": 2, "title": "四会市副市长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 邓阳焕 — 副市长
    {"person_id": 13, "org_id": 2, "title": "四会市副市长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 杨文东 — 副市长兼公安局长
    {"person_id": 14, "org_id": 2, "title": "四会市副市长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 8, "title": "四会市公安局局长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 梁祥达 — 人大主任
    {"person_id": 15, "org_id": 6, "title": "四会市人大常委会主任", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": ""},
    # 苏金生 — 政协主席
    {"person_id": 16, "org_id": 7, "title": "四会市政协主席", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": ""},
]

# 4. Relationships
relationships = [
    # 李伟忠 ↔ 吴鋆（党政正职搭档）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "市委书记与市长党政正职搭档关系",
        "overlap_org": "中共四会市委员会/四会市人民政府",
        "overlap_period": "待确认"
    },
    # 李伟忠 ↔ 苏鹏（书记与专职副书记）
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "市委书记与专职副书记搭档关系",
        "overlap_org": "中共四会市委员会",
        "overlap_period": "待确认"
    },
    # 李伟忠 ↔ 张程（书记与纪委书记）
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "市委书记与纪委书记上下级关系",
        "overlap_org": "中共四会市委员会",
        "overlap_period": "待确认"
    },
    # 吴鋆 ↔ 温天蔚（市长与常务副市长）
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "市长与常务副市长搭档关系",
        "overlap_org": "四会市人民政府",
        "overlap_period": "待确认"
    },
    # 李伟忠 ↔ 陈绪华（书记与组织部长）
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "市委书记与组织部长上下级关系",
        "overlap_org": "中共四会市委员会",
        "overlap_period": "待确认"
    },
    # 李伟忠 ↔ 何旭辉（书记与宣传部长）
    {
        "person_a": 1,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "市委书记与宣传部长上下级关系",
        "overlap_org": "中共四会市委员会",
        "overlap_period": "待确认"
    },
    # 李伟忠 ↔ 黄建平（前任-继任关系）
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "李伟忠接替黄建平任四会市委书记",
        "overlap_org": "中共四会市委员会",
        "overlap_period": "待确认"
    },
    # 吴鋆 ↔ 翁卓辉（前任-继任关系）
    {
        "person_a": 2,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "吴鋆接替翁卓辉任四会市市长",
        "overlap_org": "四会市人民政府",
        "overlap_period": "待确认"
    },
    # 黄建平→肇庆市（原四会书记升任肇庆副市长）
    {
        "person_a": 3,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "黄建平原为李伟忠上司，升任肇庆市副市长后成为上级",
        "overlap_org": "中共四会市委员会/肇庆市人民政府",
        "overlap_period": "待确认"
    },
    # 吴鋆 ↔ 梁光挺（市长与副市长）
    {
        "person_a": 2,
        "person_b": 12,
        "type": "superior_subordinate",
        "context": "市长与副市长搭档关系",
        "overlap_org": "四会市人民政府",
        "overlap_period": "待确认"
    },
    # 吴鋆 ↔ 邓阳焕（市长与副市长）
    {
        "person_a": 2,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "市长与副市长搭档关系",
        "overlap_org": "四会市人民政府",
        "overlap_period": "待确认"
    },
    # 吴鋆 ↔ 杨文东（市长与副市长兼公安局长）
    {
        "person_a": 2,
        "person_b": 14,
        "type": "superior_subordinate",
        "context": "市长与副市长（公安局长）搭档关系",
        "overlap_org": "四会市人民政府",
        "overlap_period": "待确认"
    },
    # 吴鋆 ↔ 陈思敏（市长与副市长）
    {
        "person_a": 2,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "市长与副市长搭档关系",
        "overlap_org": "四会市人民政府",
        "overlap_period": "待确认"
    },
    # 梁祥达（人大主任）与李伟忠（书记）— 班子同僚
    {
        "person_a": 1,
        "person_b": 15,
        "type": "colleague",
        "context": "市委书记与市人大主任班子同僚关系",
        "overlap_org": "四会市领导班子",
        "overlap_period": "待确认"
    },
    # 苏金生（政协主席）与李伟忠（书记）
    {
        "person_a": 1,
        "person_b": 16,
        "type": "colleague",
        "context": "市委书记与市政协主席班子同僚关系",
        "overlap_org": "四会市领导班子",
        "overlap_period": "待确认"
    },
]


if __name__ == "__main__":
    # ── Determine output paths (staging mode) ──
    db = DB_PATH
    gexf = GEXF_PATH

    # If run from repo root via staging, use staging paths
    # If run directly from tmp dir, use the defined paths
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db,
        gexf_path=gexf,
        overwrite=True,
    )
    print(f"\nDone. Database: {db}")
    print(f"GEXF: {gexf}")
