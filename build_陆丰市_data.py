#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
陆丰市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 广东省
Parent City: 汕尾市
Region: 陆丰市
Targets: 市委书记 & 市长

Research Sources:
- 陆丰市人民政府门户网站 lufengshi.gov.cn — 2026年7月多篇政务动态
- 领导之窗页面 (ldfg/index.html) — 确认郭立坚（市长）及副市长团队
- 陆丰市第十六届人民代表大会公告（第二十号）— 郭立坚当选市长（2025-04-11）
- 市人大第37、35、44次会议任免名单
- 政务要闻文章确认陈伟明（市委书记）身份

Current status (as of 2026-07-22):
- 市委书记: 陈伟明（兼汕尾市委常委，confirmed by lufengshi.gov.cn 2026-07-20 news）
- 市长: 郭立坚（confirmed by 领导之窗页面，2025年4月11日当选）

Research Date: 2026-07-22

Research Notes:
- 陈伟明（市委书记）的身份通过lufengshi.gov.cn 2026-07-20 市委常委会扩大会议和7月22日调研文章确认
- 郭立坚（市长）通过领导之窗页面确认，简历显示：1973年9月出生，在职大学学历
- 郭立坚于2025年4月11日经陆丰市第十六届人民代表大会第五次会议选举为市长
- 副市长团队通过领导之窗页面确认：陈俊彦（常务）、金小明（挂职）、叶君玉、万伟城、叶志帆、袁晓兵、黄文伟、蔡汉展
- 陈伟明同时是汕尾市委常委（见build_汕尾市_data.py）
- 前任陆丰市委书记推测为陈德忠（约2021-2024），具体任期待精确确认
- Baidu Baike 403不可用，Bing/Google搜索超时
- Web access degraded: 百度/360/搜狗均被封
- 部分人物履历根据官方公开信息整理

CONFIDENCE KEY:
  [C] = Confirmed — official government website / official notice
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
SLUG = "陆丰市"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE_DIR, f"{SLUG}_network.gexf")

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    # [C] 市委书记 — 陈伟明
    # Confirmed by lufengshi.gov.cn news: 2026-07-20 市委常委会, 2026-07-22 调研
    # Also confirmed as 汕尾市委常委 in build_汕尾市_data.py
    {
        "id": 1,
        "name": "陈伟明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年",
        "birthplace": "广东",
        "native_place": "广东",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共陆丰市委书记",
        "current_org": "中共陆丰市委员会",
        "source": "lufengshi.gov.cn官方政务动态"
    },
    # ════════════════════════════════════════
    # 市政府领导
    # ════════════════════════════════════════
    # [C] 市委副书记、市长 — 郭立坚
    # Confirmed by 领导之窗 ldfg/index.html
    # Elected 2025-04-11 by 陆丰市第十六届人民代表大会第五次会议
    {
        "id": 2,
        "name": "郭立坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学学历",
        "party_join": "1997年11月",
        "work_start": "待查",
        "current_post": "陆丰市委副书记、市长",
        "current_org": "陆丰市人民政府",
        "source": "lufengshi.gov.cn领导之窗"
    },
    # [C] 市委常委、常务副市长 — 陈俊彦
    {
        "id": 3,
        "name": "陈俊彦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆丰市委常委、常务副市长",
        "current_org": "陆丰市人民政府",
        "source": "lufengshi.gov.cn领导之窗"
    },
    # [C] 副市长 — 金小明（挂职）
    # Confirmed by 人大第44次会议任命（2026-03-05）
    {
        "id": 4,
        "name": "金小明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆丰市副市长（挂职）",
        "current_org": "陆丰市人民政府",
        "source": "lufengshi.gov.cn人大第44次会议"
    },
    # [C] 副市长 — 叶君玉
    # Confirmed by 领导之窗 + 2026-07-17 医保局党课新闻
    {
        "id": 5,
        "name": "叶君玉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆丰市副市长",
        "current_org": "陆丰市人民政府",
        "source": "lufengshi.gov.cn领导之窗"
    },
    # [C] 副市长 — 万伟城
    {
        "id": 6,
        "name": "万伟城",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆丰市副市长",
        "current_org": "陆丰市人民政府",
        "source": "lufengshi.gov.cn领导之窗"
    },
    # [C] 副市长 — 叶志帆
    # Confirmed by 领导之窗 + 2026-07-20 防汛调研新闻
    {
        "id": 7,
        "name": "叶志帆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆丰市副市长",
        "current_org": "陆丰市人民政府",
        "source": "lufengshi.gov.cn领导之窗"
    },
    # [C] 副市长 — 袁晓兵
    {
        "id": 8,
        "name": "袁晓兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆丰市副市长",
        "current_org": "陆丰市人民政府",
        "source": "lufengshi.gov.cn领导之窗"
    },
    # [C] 副市长 — 黄文伟
    # Confirmed by 领导之窗 + 人大第35次会议任命（2025-04-02）
    {
        "id": 9,
        "name": "黄文伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆丰市副市长",
        "current_org": "陆丰市人民政府",
        "source": "lufengshi.gov.cn领导之窗/人大第35次会议"
    },
    # [C] 副市长 — 蔡汉展
    # Confirmed by 领导之窗 + 人大第37次会议任命（2025-06-19）
    {
        "id": 10,
        "name": "蔡汉展",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆丰市副市长",
        "current_org": "陆丰市人民政府",
        "source": "lufengshi.gov.cn领导之窗/人大第37次会议"
    },
    # ════════════════════════════════════════
    # 其他市领导
    # ════════════════════════════════════════
    # [C] 市领导 — 傅锦冲
    # Confirmed by 2026-07-22 汕尾人大调研新闻
    {
        "id": 11,
        "name": "傅锦冲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆丰市领导",
        "current_org": "陆丰市人民政府",
        "source": "lufengshi.gov.cn政务要闻"
    },
    # [C] 市领导 — 施汉阳
    # Confirmed by 2026-07-20 汕尾人大调研新闻
    {
        "id": 12,
        "name": "施汉阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "陆丰市领导",
        "current_org": "陆丰市人民政府",
        "source": "lufengshi.gov.cn政务要闻"
    },
    # ════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════
    # [P] 前任陆丰市委书记 — 陈德忠（推测）
    # 陈德忠曾任陆丰市委书记（约2021-2024年）
    # 后转任汕尾市委常委、政法委书记
    {
        "id": 13,
        "name": "陈德忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年",
        "birthplace": "广东",
        "native_place": "广东",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原汕尾市委常委、政法委书记、陆丰市委书记）",
        "current_org": "待查",
        "source": "网络公开资料"
    },
    # [P] 前任市长 — 高火君（推测）
    # 2021-2024年任陆丰市长
    {
        "id": 14,
        "name": "高火君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年",
        "birthplace": "广东",
        "native_place": "广东",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原陆丰市市长）",
        "current_org": "待查",
        "source": "网络公开资料"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共陆丰市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共汕尾市委",
        "location": "广东省汕尾市陆丰市"
    },
    {
        "id": 2,
        "name": "陆丰市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "汕尾市人民政府",
        "location": "广东省汕尾市陆丰市"
    },
    {
        "id": 3,
        "name": "陆丰市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "汕尾市人大常委会",
        "location": "广东省汕尾市陆丰市"
    },
    {
        "id": 4,
        "name": "中共汕尾市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委",
        "location": "广东省汕尾市"
    },
]

# 3. Positions
positions = [
    # 陈伟明
    {"person_id": 1, "org_id": 1, "title": "中共陆丰市委书记", "start": "约2024年", "end": "至今", "rank": "正处级", "note": "同时兼任汕尾市委常委"},
    {"person_id": 1, "org_id": 4, "title": "中共汕尾市委常委", "start": "约2024年", "end": "至今", "rank": "副厅级", "note": "同见build_汕尾市_data.py"},
    # 郭立坚
    {"person_id": 2, "org_id": 1, "title": "中共陆丰市委副书记", "start": "约2025年", "end": "至今", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "陆丰市人民政府市长", "start": "2025年4月", "end": "至今", "rank": "正处级", "note": "2025年4月11日经市人大五次会议选举"},
    # 陈俊彦
    {"person_id": 3, "org_id": 1, "title": "中共陆丰市委常委", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "陆丰市常务副市长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 金小明
    {"person_id": 4, "org_id": 2, "title": "陆丰市副市长（挂职）", "start": "2026年3月", "end": "至今", "rank": "副处级", "note": "2026年3月5日人大第44次会议任命"},
    # 叶君玉
    {"person_id": 5, "org_id": 2, "title": "陆丰市副市长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 万伟城
    {"person_id": 6, "org_id": 2, "title": "陆丰市副市长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 叶志帆
    {"person_id": 7, "org_id": 2, "title": "陆丰市副市长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 袁晓兵
    {"person_id": 8, "org_id": 2, "title": "陆丰市副市长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 黄文伟
    {"person_id": 9, "org_id": 2, "title": "陆丰市副市长", "start": "2025年4月", "end": "至今", "rank": "副处级", "note": "2025年4月2日人大第35次会议任命"},
    # 蔡汉展
    {"person_id": 10, "org_id": 2, "title": "陆丰市副市长", "start": "2025年6月", "end": "至今", "rank": "副处级", "note": "2025年6月19日人大第37次会议任命"},
    # 傅锦冲
    {"person_id": 11, "org_id": 2, "title": "陆丰市领导", "start": "", "end": "至今", "rank": "", "note": "具体职务待查"},
    # 施汉阳
    {"person_id": 12, "org_id": 2, "title": "陆丰市领导", "start": "", "end": "至今", "rank": "", "note": "具体职务待查"},
    # 陈德忠（前任市委书记）
    {"person_id": 13, "org_id": 1, "title": "中共陆丰市委书记", "start": "约2021年", "end": "约2024年", "rank": "正处级", "note": "任期待精确确认"},
    # 高火君（前任市长）
    {"person_id": 14, "org_id": 2, "title": "陆丰市市长", "start": "约2021年", "end": "约2024年", "rank": "正处级", "note": "任期待精确确认"},
]

# 4. Relationships
relationships = [
    # 陈伟明 —— 郭立坚（书记-市长搭档）
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "陈伟明任市委书记、郭立坚任市长，为党政领导核心搭档",
        "overlap_org": "中共陆丰市委员会/陆丰市人民政府",
        "overlap_period": "2025至今"
    },
    # 陈伟明 —— 陈俊彦（市委班子）
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "共同在陆丰市委班子任职",
        "overlap_org": "中共陆丰市委员会",
        "overlap_period": "至今"
    },
    # 郭立坚 —— 陈俊彦（政府班子）
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "郭立坚为市长、陈俊彦为常务副市长，共同在政府班子任职",
        "overlap_org": "陆丰市人民政府",
        "overlap_period": "至今"
    },
    # 陈伟明 —— 傅锦冲（市委班子）
    {
        "person_a": 1, "person_b": 11,
        "type": "overlap",
        "context": "共同参加政务活动",
        "overlap_org": "陆丰市人民政府",
        "overlap_period": "至今"
    },
    # 郭立坚 —— 叶君玉（政府班子）
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "共同在陆丰市政府班子任职",
        "overlap_org": "陆丰市人民政府",
        "overlap_period": "至今"
    },
    # 郭立坚 —— 叶志帆（政府班子）
    {
        "person_a": 2, "person_b": 7,
        "type": "overlap",
        "context": "共同在陆丰市政府班子任职，叶志帆陪同陈伟明调研防汛",
        "overlap_org": "陆丰市人民政府",
        "overlap_period": "至今"
    },
    # 陈伟明 —— 叶志帆（上下级）
    {
        "person_a": 1, "person_b": 7,
        "type": "superior_subordinate",
        "context": "叶志帆副市长陪同陈伟明书记调研防汛工作",
        "overlap_org": "陆丰市人民政府",
        "overlap_period": "至今"
    },
    # 陈俊彦 —— 金小明（政府班子）
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "共同在陆丰市政府班子任职",
        "overlap_org": "陆丰市人民政府",
        "overlap_period": "2026年3月至今"
    },
    # 陈俊彦 —— 万伟城（政府班子）
    {
        "person_a": 3, "person_b": 6,
        "type": "overlap",
        "context": "共同在陆丰市政府班子任职",
        "overlap_org": "陆丰市人民政府",
        "overlap_period": "至今"
    },
    # 陈俊彦 —— 袁晓兵（政府班子）
    {
        "person_a": 3, "person_b": 8,
        "type": "overlap",
        "context": "共同在陆丰市政府班子任职",
        "overlap_org": "陆丰市人民政府",
        "overlap_period": "至今"
    },
    # 陈俊彦 —— 黄文伟（政府班子）
    {
        "person_a": 3, "person_b": 9,
        "type": "overlap",
        "context": "共同在陆丰市政府班子任职",
        "overlap_org": "陆丰市人民政府",
        "overlap_period": "2025年4月至今"
    },
    # 陈俊彦 —— 蔡汉展（政府班子）
    {
        "person_a": 3, "person_b": 10,
        "type": "overlap",
        "context": "共同在陆丰市政府班子任职",
        "overlap_org": "陆丰市人民政府",
        "overlap_period": "2025年6月至今"
    },
    # 陈伟明 —— 陈德忠（前任-后任）
    {
        "person_a": 1, "person_b": 13,
        "type": "predecessor_successor",
        "context": "陈德忠此前任陆丰市委书记，陈伟明后接任",
        "overlap_org": "中共陆丰市委员会",
        "overlap_period": ""
    },
    # 郭立坚 —— 高火君（前任-后任）
    {
        "person_a": 2, "person_b": 14,
        "type": "predecessor_successor",
        "context": "高火君此前任陆丰市市长，郭立坚后接任",
        "overlap_org": "陆丰市人民政府",
        "overlap_period": ""
    },
    # 陈德忠 —— 高火君（书记-市长搭档）
    {
        "person_a": 13, "person_b": 14,
        "type": "overlap",
        "context": "陈德忠任市委书记、高火君任市长，为前任党政搭档",
        "overlap_org": "中共陆丰市委员会/陆丰市人民政府",
        "overlap_period": "约2021-2024"
    },
    # 郭立坚 —— 蔡汉展（政府班子）
    {
        "person_a": 2, "person_b": 10,
        "type": "overlap",
        "context": "郭立坚为市长、蔡汉展为副市长，共同参加汕尾人大调研活动",
        "overlap_org": "陆丰市人民政府",
        "overlap_period": "2025年6月至今"
    },
    # 陈伟明 —— 施汉阳
    {
        "person_a": 1, "person_b": 12,
        "type": "overlap",
        "context": "共同参加汕尾人大调研活动（施汉阳陪同调研基层公共卫生）",
        "overlap_org": "陆丰市人民政府",
        "overlap_period": "至今"
    },
    # 郭立坚 —— 傅锦冲
    {
        "person_a": 2, "person_b": 11,
        "type": "overlap",
        "context": "共同在陆丰市领导班子任职",
        "overlap_org": "陆丰市人民政府",
        "overlap_period": "至今"
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
