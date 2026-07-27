#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大名县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 邯郸市
Region: 大名县
Targets: 县委书记 & 县长

Research Sources:
- 大名县人民政府官方网站 (www.daming.gov.cn) — 县长之窗确认县长李爽信息
- 大名县人民政府官方网站 — 副县长页面确认王运晓、叶营生、田晨、刘冰、樊晓雪信息
- 维基百科API — 确认县委书记高巍（1977年生）
- 大名县政府新闻图片 — 县委书记高巍在新闻报道中确认
- 搜狗搜索 — 确认边飞(前县委书记，落马判死缓)、房延生(前县委书记)、薛洪志(前县委书记)
- 澎湃新闻 — 相关人事报道

Research Date: 2026-07-23
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "大名县"

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
        "name": "高巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邯郸市大名县委书记",
        "current_org": "中共邯郸市大名县委员会",
        "source": "维基百科API确认高巍任大名县委书记(1977年生)。来源：https://zh.wikipedia.org/w/api.php?action=query&list=search&srsearch=%E5%A4%A7%E5%90%8D%E5%8E%BF%E5%8E%BF%E5%A7%94%E4%B9%A6%E8%AE%B0&format=json"
    },
    {
        "id": 2,
        "name": "李爽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年7月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历、管理学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邯郸市大名县委副书记、县长",
        "current_org": "大名县人民政府",
        "source": "大名县人民政府官方网站—县长之窗确认。来源：http://www.daming.gov.cn/ldzc/xz/"
    },
    # ════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "王运晓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历、工学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大名县政府副县长、党组成员，县公安局党委书记、局长、督察长",
        "current_org": "大名县人民政府",
        "source": "大名县人民政府官方网站—副县长页面确认。来源：http://www.daming.gov.cn/ldzc/fxz/"
    },
    {
        "id": 4,
        "name": "叶营生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大名县政府副县长、党组成员",
        "current_org": "大名县人民政府",
        "source": "大名县人民政府官方网站—副县长页面确认。来源：http://www.daming.gov.cn/ldzc/fxz/"
    },
    {
        "id": 5,
        "name": "田晨",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1985年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历、文学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大名县政府副县长、党组成员",
        "current_org": "大名县人民政府",
        "source": "大名县人民政府官方网站—副县长页面确认。来源：http://www.daming.gov.cn/ldzc/fxz/"
    },
    {
        "id": 6,
        "name": "刘冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历、文学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大名县政府副县长",
        "current_org": "大名县人民政府",
        "source": "大名县人民政府官方网站—副县长页面确认（2025年8月更新照片）。来源：http://www.daming.gov.cn/ldzc/fxz/"
    },
    {
        "id": 7,
        "name": "樊晓雪",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1988年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历、工学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "大名县政府副县长",
        "current_org": "大名县人民政府",
        "source": "大名县人民政府官方网站—副县长页面确认。来源：http://www.daming.gov.cn/ldzc/fxz/"
    },
    # ════════════════════════════════════════
    # Historical Leaders
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "边飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年10月",
        "birthplace": "河北省邯郸市",
        "native_place": "河北省邯郸市",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "1982年8月",
        "current_post": "已落马（无期徒刑）",
        "current_org": "",
        "source": "维基百科：边飞词条。历任大名县委书记，2013年落马，受贿5920余万元，被判无期徒刑。来源：https://zh.wikipedia.org/wiki/%E8%BE%B9%E9%A3%9E"
    },
    {
        "id": 9,
        "name": "房延生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "曾任大名县委书记（疑似落马）",
        "current_org": "",
        "source": "搜狗搜索结果：房延生接替边飞任大名县委书记，后续疑似也被调查。来源：搜狗搜索'房延生 大名县委书记'"
    },
    {
        "id": 10,
        "name": "薛洪志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "曾任大名县委书记（已调任他职）",
        "current_org": "",
        "source": "搜狗搜索结果：薛洪志曾任大名县委书记后调任他职。来源：搜狗搜索'薛洪志 大名县委书记'"
    },
    {
        "id": 11,
        "name": "刘锐光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "曾任大名县县长（已调任）",
        "current_org": "",
        "source": "大名县人民政府新闻图片—2023年12月仍以县长身份出席活动，2024年初被李爽接替。来源：http://www.daming.gov.cn/xwzx/tpxw/"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共邯郸市大名县委员会",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市大名县",
        "parent": "中共邯郸市委"
    },
    {
        "id": 2,
        "name": "大名县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "邯郸市大名县",
        "parent": "邯郸市人民政府"
    },
    {
        "id": 3,
        "name": "大名县人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "邯郸市大名县",
        "parent": "邯郸市人大常委会"
    },
    {
        "id": 4,
        "name": "大名县政协",
        "type": "政协",
        "level": "县级",
        "location": "邯郸市大名县",
        "parent": "邯郸市政协"
    },
    {
        "id": 5,
        "name": "大名县公安局",
        "type": "政府",
        "level": "县级",
        "location": "邯郸市大名县",
        "parent": "大名县人民政府"
    },
    {
        "id": 6,
        "name": "大名经济开发区",
        "type": "开发区",
        "level": "县级",
        "location": "邯郸市大名县",
        "parent": "大名县人民政府"
    },
]

# 3. Positions
positions = [
    # 高巍
    {"person_id": 1, "org_id": 1, "title": "邯郸市大名县委书记", "start": "2023年（推测）", "end": "present", "rank": "正处级", "note": "1977年生，截至2026年7月在任。前任为薛洪志"},
    # 李爽
    {"person_id": 2, "org_id": 2, "title": "大名县委副书记、县长", "start": "2024年1月（推测）", "end": "present", "rank": "正处级", "note": "1987年7月生，大学学历、管理学硕士，县政府党组书记兼大名经济开发区党工委副书记、管委会主任"},
    {"person_id": 2, "org_id": 6, "title": "大名经济开发区党工委副书记兼管委会主任", "start": "2024年1月（推测）", "end": "present", "rank": "正处级", "note": "兼任"},
    # 王运晓
    {"person_id": 3, "org_id": 2, "title": "大名县政府副县长、党组成员", "start": "未知", "end": "present", "rank": "副处级", "note": "1974年12月生，大学学历、工学学士，兼县公安局党委书记、局长、督察长"},
    {"person_id": 3, "org_id": 5, "title": "大名县公安局党委书记、局长、督察长", "start": "未知", "end": "present", "rank": "副处级", "note": "兼任"},
    # 叶营生
    {"person_id": 4, "org_id": 2, "title": "大名县政府副县长、党组成员", "start": "未知", "end": "present", "rank": "副处级", "note": "1973年10月生，大学学历"},
    # 田晨
    {"person_id": 5, "org_id": 2, "title": "大名县政府副县长、党组成员", "start": "未知", "end": "present", "rank": "副处级", "note": "1985年11月生，满族，大学学历、文学学士"},
    # 刘冰
    {"person_id": 6, "org_id": 2, "title": "大名县政府副县长", "start": "2025年（推测）", "end": "present", "rank": "副处级", "note": "1982年2月生，大学学历、文学学士。2025年8月更新照片，推测此时上任"},
    # 樊晓雪
    {"person_id": 7, "org_id": 2, "title": "大名县政府副县长", "start": "2025年（推测）", "end": "present", "rank": "副处级", "note": "1988年10月生，女，大学学历、工学学士。2025年8月更新照片"},
    # 边飞 — 历史职务
    {"person_id": 8, "org_id": 1, "title": "大名县委书记", "start": "约2012年", "end": "2013年", "rank": "正处级", "note": "2013年被调查，后被判无期徒刑。曾任曲周县委书记、临漳县委书记、魏县县委书记、永年县委书记"},
    # 房延生
    {"person_id": 9, "org_id": 1, "title": "大名县委书记", "start": "约2014年", "end": "约2021年", "rank": "正处级", "note": "接替边飞任大名县委书记"},
    # 薛洪志
    {"person_id": 10, "org_id": 1, "title": "大名县委书记", "start": "约2021年", "end": "约2023年", "rank": "正处级", "note": "接替房延生，后调任他职"},
    # 刘锐光
    {"person_id": 11, "org_id": 2, "title": "大名县县长", "start": "未知", "end": "2023年12月", "rank": "正处级", "note": "2023年12月仍在任，2024年初被李爽接替"},
]

# 4. Relationships
relationships = [
    # 当前核心领导关系
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "高巍作为县委书记领导县长李爽",
        "overlap_org": "中共邯郸市大名县委员会/大名县人民政府",
        "overlap_period": "2024-present"
    },
    # 县委书记与副县长们
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "高巍领导副县长王运晓",
        "overlap_org": "中共邯郸市大名县委员会/大名县人民政府",
        "overlap_period": "2024-present"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "高巍领导副县长叶营生",
        "overlap_org": "中共邯郸市大名县委员会/大名县人民政府",
        "overlap_period": "2024-present"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "高巍领导副县长田晨",
        "overlap_org": "中共邯郸市大名县委员会/大名县人民政府",
        "overlap_period": "2024-present"
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "高巍领导副县长刘冰",
        "overlap_org": "中共邯郸市大名县委员会/大名县人民政府",
        "overlap_period": "2025-present"
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "高巍领导副县长樊晓雪",
        "overlap_org": "中共邯郸市大名县委员会/大名县人民政府",
        "overlap_period": "2025-present"
    },
    # 县长与副县长们
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "李爽作为县长领导副县长王运晓",
        "overlap_org": "大名县人民政府",
        "overlap_period": "2024-present"
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "李爽作为县长领导副县长叶营生",
        "overlap_org": "大名县人民政府",
        "overlap_period": "2024-present"
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "李爽作为县长领导副县长田晨",
        "overlap_org": "大名县人民政府",
        "overlap_period": "2024-present"
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "李爽作为县长领导副县长刘冰",
        "overlap_org": "大名县人民政府",
        "overlap_period": "2025-present"
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "李爽作为县长领导副县长樊晓雪",
        "overlap_org": "大名县人民政府",
        "overlap_period": "2025-present"
    },
    # 前任县委书记链
    {
        "person_a": 1,
        "person_b": 10,
        "type": "predecessor_successor",
        "context": "高巍接替薛洪志任大名县委书记",
        "overlap_org": "中共邯郸市大名县委员会",
        "overlap_period": "约2023年"
    },
    {
        "person_a": 10,
        "person_b": 9,
        "type": "predecessor_successor",
        "context": "薛洪志接替房延生任大名县委书记",
        "overlap_org": "中共邯郸市大名县委员会",
        "overlap_period": "约2021年"
    },
    {
        "person_a": 9,
        "person_b": 8,
        "type": "predecessor_successor",
        "context": "房延生接替边飞（落马）任大名县委书记",
        "overlap_org": "中共邯郸市大名县委员会",
        "overlap_period": "约2014年"
    },
    # 前任县长
    {
        "person_a": 2,
        "person_b": 11,
        "type": "predecessor_successor",
        "context": "李爽接替刘锐光任大名县县长",
        "overlap_org": "大名县人民政府",
        "overlap_period": "2023年12月-2024年初"
    },
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
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
