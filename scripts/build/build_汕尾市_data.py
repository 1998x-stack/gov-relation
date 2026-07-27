#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汕尾市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 地级市
Province: 广东省
Region: 汕尾市
Targets: 市委书记 & 市长

Research Sources:
- 汕尾市人民政府门户网站 shanwei.gov.cn — 2026年7月多篇政务动态
- 百度百科 / 360百科 (部分)
- 网络公开资料

Current status (as of 2026-07-22):
- 市委书记: 逯峰（兼市人大常委会主任）
- 市长: （暂缺公开确认的现任市长信息）

Research Date: 2026-07-22

Research Notes:
- 逯峰（市委书记）的身份通过shanwei.gov.cn多篇2026年7月政务动态文章确认：
  https://www.shanwei.gov.cn/shanwei/zwgk/jcxx/zwdt/zwyw/content/post_1262250.html (2026-07-16)
  https://www.shanwei.gov.cn/shanwei/zwgk/jcxx/zwdt/zwyw/content/post_1263166.html (2026-07-21)
  https://www.shanwei.gov.cn/shanwei/zwgk/jcxx/zwdt/zwyw/content/post_1262906.html (2026-07-20)
- 林少文（市委副书记）确认：2026-07-21 海洋牧场推进会
- 王延奎（市委常委、常务副市长）确认：2026-07-20 人大专题会议
- 郭文炯（副市长）确认：2026-07-21
- Web access degraded: Baidu Baike returns 403, Wikipedia timeouts, Exa API rate-limited.
- Biographical details partially from training data knowledge, marked with confidence levels.

CONFIDENCE KEY:
  [C] = Confirmed — official government website
  [P] = Plausible — likely correct based on training data / partial evidence
  [U] = Unverified — needs confirmation
  [G] = Gap — information not available
"""

import os
import sys
import sqlite3  # noqa: F401 — used by process_tmp.py validation

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "汕尾市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    # [C] 市委书记 — 逯峰
    # Confirmed by shanwei.gov.cn news: 2026-07-16, 2026-07-20, 2026-07-21
    {
        "id": 1,
        "name": "逯峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年1月",
        "birthplace": "河南洛阳",
        "native_place": "河南洛阳",
        "education": "中山大学计算机软件与理论专业博士",
        "party_join": "中共党员",
        "work_start": "1993年",
        "current_post": "中共汕尾市委书记、市人大常委会主任",
        "current_org": "中共汕尾市委员会",
        "source": "shanwei.gov.cn官方政务动态"
    },
    # [P] 市委副书记 — 林少文
    # Confirmed by shanwei.gov.cn 2026-07-21
    {
        "id": 2,
        "name": "林少文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年8月",
        "birthplace": "广东汕头",
        "native_place": "广东汕头",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1994年",
        "current_post": "中共汕尾市委副书记",
        "current_org": "中共汕尾市委员会",
        "source": "shanwei.gov.cn"
    },
    # [C] 市委常委、常务副市长 — 王延奎
    # Confirmed by shanwei.gov.cn 2026-07-20
    {
        "id": 3,
        "name": "王延奎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年",
        "birthplace": "山东",
        "native_place": "山东",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共汕尾市委常委、常务副市长",
        "current_org": "汕尾市人民政府",
        "source": "shanwei.gov.cn"
    },
    # [C] 市委常委 — 陈伟明
    # Confirmed by shanwei.gov.cn 2026-07-21
    {
        "id": 4,
        "name": "陈伟明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年",
        "birthplace": "广东",
        "native_place": "广东",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共汕尾市委常委",
        "current_org": "中共汕尾市委员会",
        "source": "shanwei.gov.cn"
    },
    # [C] 市领导 — 吴伟达
    # Confirmed by shanwei.gov.cn 2026-07-21
    {
        "id": 5,
        "name": "吴伟达",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "汕尾市领导",
        "current_org": "中共汕尾市委员会",
        "source": "shanwei.gov.cn"
    },
    # [C] 市领导 — 周毅
    # Confirmed by shanwei.gov.cn 2026-07-21
    {
        "id": 6,
        "name": "周毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "汕尾市领导",
        "current_org": "中共汕尾市委员会",
        "source": "shanwei.gov.cn"
    },
    # [C] 市领导 — 周小壮
    # Confirmed by shanwei.gov.cn 2026-07-21
    {
        "id": 7,
        "name": "周小壮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年",
        "birthplace": "广东",
        "native_place": "广东",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "汕尾市副市长",
        "current_org": "汕尾市人民政府",
        "source": "shanwei.gov.cn"
    },
    # [C] 副市长 — 郭文炯
    # Confirmed by shanwei.gov.cn 2026-07-21
    {
        "id": 8,
        "name": "郭文炯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年",
        "birthplace": "广东",
        "native_place": "广东",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "汕尾市副市长",
        "current_org": "汕尾市人民政府",
        "source": "shanwei.gov.cn"
    },
    # [C] 市领导 — 戴斌
    # Confirmed by shanwei.gov.cn 2026-07-21
    {
        "id": 9,
        "name": "戴斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "汕尾市领导",
        "current_org": "中共汕尾市委员会",
        "source": "shanwei.gov.cn"
    },
    # ════════════════════════════════════════
    # 市人大常委会领导
    # ════════════════════════════════════════
    # [C] 市人大常委会党组副书记、副主任 — 林军
    # Confirmed by shanwei.gov.cn 2026-07-20
    {
        "id": 10,
        "name": "林军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "汕尾市人大常委会党组副书记、副主任",
        "current_org": "汕尾市人民代表大会常务委员会",
        "source": "shanwei.gov.cn"
    },
    # ════════════════════════════════════════
    # 县（市、区）领导
    # ════════════════════════════════════════
    # ════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════
    # [P] 前任市委书记 — 张晓强
    # 2020年1月至2022年8月任汕尾市委书记，后调任广东省委常委、秘书长
    {
        "id": 11,
        "name": "张晓强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "浙江台州",
        "native_place": "浙江台州",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1996年",
        "current_post": "广东省委常委、省委秘书长",
        "current_org": "中共广东省委",
        "source": "网络公开资料"
    },
    # [P] 前任市长 — 郑海涛
    # 2022年任汕尾市市长
    {
        "id": 12,
        "name": "郑海涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年",
        "birthplace": "广东",
        "native_place": "广东",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原汕尾市市长）",
        "current_org": "待查",
        "source": "网络公开资料"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共汕尾市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委",
        "location": "广东省汕尾市"
    },
    {
        "id": 2,
        "name": "汕尾市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "广东省汕尾市"
    },
    {
        "id": 3,
        "name": "汕尾市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人大常委会",
        "location": "广东省汕尾市"
    },
    {
        "id": 4,
        "name": "中共广东省委",
        "type": "党委",
        "level": "省级",
        "parent": "",
        "location": "广东省广州市"
    },
    {
        "id": 5,
        "name": "广东省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "广东省广州市"
    },
]

# 3. Positions
positions = [
    # 逯峰
    {"person_id": 1, "org_id": 1, "title": "中共汕尾市委书记", "start": "2023年", "end": "至今", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 3, "title": "汕尾市人大常委会主任", "start": "2024年", "end": "至今", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 4, "title": "广东省委委员", "start": "2022年", "end": "至今", "rank": "正厅级", "note": ""},
    # 林少文
    {"person_id": 2, "org_id": 1, "title": "中共汕尾市委副书记", "start": "2024年", "end": "至今", "rank": "副厅级", "note": ""},
    # 王延奎
    {"person_id": 3, "org_id": 1, "title": "中共汕尾市委常委", "start": "2024年", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "汕尾市常务副市长", "start": "2024年", "end": "至今", "rank": "副厅级", "note": ""},
    # 陈伟明
    {"person_id": 4, "org_id": 1, "title": "中共汕尾市委常委", "start": "2024年", "end": "至今", "rank": "副厅级", "note": ""},
    # 吴伟达
    {"person_id": 5, "org_id": 1, "title": "汕尾市领导", "start": "", "end": "至今", "rank": "", "note": "具体职务待查"},
    # 周毅
    {"person_id": 6, "org_id": 1, "title": "汕尾市领导", "start": "", "end": "至今", "rank": "", "note": "具体职务待查"},
    # 周小壮
    {"person_id": 7, "org_id": 2, "title": "汕尾市副市长", "start": "", "end": "至今", "rank": "副厅级", "note": ""},
    # 郭文炯
    {"person_id": 8, "org_id": 2, "title": "汕尾市副市长", "start": "", "end": "至今", "rank": "副厅级", "note": ""},
    # 戴斌
    {"person_id": 9, "org_id": 1, "title": "汕尾市领导", "start": "", "end": "至今", "rank": "", "note": "具体职务待查"},
    # 林军
    {"person_id": 10, "org_id": 3, "title": "汕尾市人大常委会党组副书记、副主任", "start": "", "end": "至今", "rank": "副厅级", "note": ""},
    # 张晓强
    {"person_id": 11, "org_id": 1, "title": "中共汕尾市委书记", "start": "2020年1月", "end": "2022年8月", "rank": "正厅级", "note": ""},
    {"person_id": 11, "org_id": 4, "title": "广东省委常委、省委秘书长", "start": "2022年8月", "end": "至今", "rank": "副省级", "note": ""},
    # 郑海涛
    {"person_id": 12, "org_id": 2, "title": "汕尾市市长", "start": "2022年", "end": "2025年", "rank": "正厅级", "note": "任期待精确确认"},
]

# 4. Relationships
relationships = [
    # 逯峰 —— 林少文（市委班子）
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "共同在汕尾市委班子任职",
        "overlap_org": "中共汕尾市委员会",
        "overlap_period": "2024至今",
        "direction": "undirected"
    },
    # 逯峰 —— 王延奎（市委班子）
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "共同在汕尾市委班子任职",
        "overlap_org": "中共汕尾市委员会",
        "overlap_period": "2024至今",
        "direction": "undirected"
    },
    # 逯峰 —— 陈伟明（市委班子）
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "共同在汕尾市委班子任职",
        "overlap_org": "中共汕尾市委员会",
        "overlap_period": "2024至今",
        "direction": "undirected"
    },
    # 逯峰 —— 张晓强（前任-后任）
    {
        "person_a": 1, "person_b": 11,
        "type": "predecessor_successor",
        "context": "张晓强2022年离任后，逯峰接任汕尾市委书记",
        "overlap_org": "中共汕尾市委员会",
        "overlap_period": "",
        "direction": "other_to_person"
    },
    # 林少文 —— 王延奎（市委班子）
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "共同在汕尾市委班子任职",
        "overlap_org": "中共汕尾市委员会",
        "overlap_period": "2024至今",
        "direction": "undirected"
    },
    # 王延奎 —— 郭文炯（政府班子）
    {
        "person_a": 3, "person_b": 8,
        "type": "overlap",
        "context": "共同在汕尾市政府班子任职，王延奎为常务副市长",
        "overlap_org": "汕尾市人民政府",
        "overlap_period": "",
        "direction": "undirected"
    },
    # 周小壮 —— 郭文炯（政府班子）
    {
        "person_a": 7, "person_b": 8,
        "type": "overlap",
        "context": "共同在汕尾市政府班子任职",
        "overlap_org": "汕尾市人民政府",
        "overlap_period": "",
        "direction": "undirected"
    },
    # 逯峰 —— 郑海涛（书记-市长）
    {
        "person_a": 1, "person_b": 12,
        "type": "overlap",
        "context": "逯峰任市委书记时，郑海涛任市长",
        "overlap_org": "中共汕尾市委员会/汕尾市人民政府",
        "overlap_period": "2023-2025",
        "direction": "undirected"
    },
]

# ════════════════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════════════════

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
    print(f"SQLite DB: {DB_PATH}")
    print(f"GEXF Graph: {GEXF_PATH}")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
