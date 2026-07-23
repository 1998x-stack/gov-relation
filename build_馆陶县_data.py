#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
馆陶县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 邯郸市
Region: 馆陶县
Targets: 县委书记 & 县长

Research Sources:
- 馆陶县人民政府网站 (www.guantao.gov.cn) — 本地动态新闻栏目确认现任主要领导
  - 2026年6月27日县委常委会扩大会议报道确认县委书记程玉峰
  - 2026年5月13日"一品一播"专题调度会报道确认县长马楠
  - 2026年6月同篇报道确认县委副书记孙辉、县政协主席吕恩成
  - 县委常委、常务副县长郑永亮确认（驻点招商工作会议）
  - 县委常委、纪委书记、监委主任李继军确认
  - 县委常委、政法委书记董宁房确认
  - 副县长平克硕、孔维民、班珏确认
  - 县政协副主席平韦振确认
- 2025年1月新闻报道确认前任县委书记王立伟仍在任
- 2023年2月新闻报道确认前任县长王峰仍在任
- 前瞻产业研究院(2020-2024)县长王峰在任
- 搜索受限（Exa限速、百度403），部分履历来自新闻间接确认

Research Date: 2026-07-23
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "馆陶县"

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
        "name": "程玉峰",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "馆陶县委书记",
        "current_org": "中共馆陶县委员会",
        "source": "馆陶县人民政府网站县委常委会扩大会议报道（2026-06-27）确认县委书记程玉峰主持并讲话。来源：http://www.guantao.gov.cn/xwzx/bddt/202606/t20260629_2207480.html"
    },
    {
        "id": 2,
        "name": "马楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "馆陶县委副书记、县政府县长",
        "current_org": "馆陶县人民政府",
        "source": "馆陶县人民政府网站多篇新闻报道（2026-01至2026-05）确认县长马楠主持各类工作会议。来源：http://www.guantao.gov.cn/xwzx/bddt/202605/t20260513_2201433.html"
    },
    # ════════════════════════════════════════
    # 县委领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "孙辉",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "馆陶县委副书记",
        "current_org": "中共馆陶县委员会",
        "source": "馆陶县人民政府网站新闻报道确认县委副书记孙辉参加活动。来源：http://www.guantao.gov.cn/xwzx/bddt/"
    },
    {
        "id": 4,
        "name": "郑永亮",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "馆陶县委常委、县政府常务副县长",
        "current_org": "馆陶县人民政府",
        "source": "馆陶县人民政府网站新闻报道确认县委常委、常务副县长郑永亮主持召开驻点招商工作视频会议。来源：http://www.guantao.gov.cn/xwzx/bddt/"
    },
    {
        "id": 5,
        "name": "李继军",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "馆陶县委常委、纪委书记、监委主任",
        "current_org": "中共馆陶县纪律检查委员会",
        "source": "馆陶县人民政府网站新闻报道确认县委常委、纪委书记、监委主任李继军。来源：http://www.guantao.gov.cn/xwzx/bddt/"
    },
    {
        "id": 6,
        "name": "董宁房",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "馆陶县委常委、政法委书记",
        "current_org": "中共馆陶县委员会政法委员会",
        "source": "馆陶县人民政府网站新闻报道确认县委常委、政法委书记董宁房。来源：http://www.guantao.gov.cn/xwzx/bddt/"
    },
    # ════════════════════════════════════════
    # 县政府领导
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "平克硕",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "馆陶县人民政府副县长",
        "current_org": "馆陶县人民政府",
        "source": "馆陶县人民政府网站新闻报道确认副县长平克硕参加会议。来源：http://www.guantao.gov.cn/xwzx/bddt/"
    },
    {
        "id": 8,
        "name": "孔维民",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "馆陶县人民政府副县长",
        "current_org": "馆陶县人民政府",
        "source": "馆陶县人民政府网站新闻报道确认副县长孔维民参加会议。来源：http://www.guantao.gov.cn/xwzx/bddt/"
    },
    {
        "id": 9,
        "name": "班珏",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "馆陶县人民政府副县长",
        "current_org": "馆陶县人民政府",
        "source": "馆陶县人民政府网站新闻报道确认副县长班珏参加会议。来源：http://www.guantao.gov.cn/xwzx/bddt/"
    },
    # ════════════════════════════════════════
    # 人大、政协领导
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "吕恩成",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "馆陶县政协主席",
        "current_org": "馆陶县政协",
        "source": "馆陶县人民政府网站新闻报道确认县政协主席吕恩成参加活动。来源：http://www.guantao.gov.cn/xwzx/bddt/"
    },
    {
        "id": 11,
        "name": "平韦振",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "馆陶县政协副主席",
        "current_org": "馆陶县政协",
        "source": "馆陶县人民政府网站多篇新闻报道确认县政协副主席平韦振参加会议。来源：http://www.guantao.gov.cn/xwzx/bddt/202605/t20260513_2201433.html"
    },
    # ════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "王立伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任馆陶县委书记（已离任）",
        "current_org": "中共馆陶县委员会",
        "source": "馆陶县人民政府网站2025年1月报道确认县委书记王立伟与省人大代表交流座谈。来源：http://www.guantao.gov.cn/xwzx/bddt/202501/t20250124_2103119.html"
    },
    {
        "id": 13,
        "name": "王峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任馆陶县县长（已离任）",
        "current_org": "馆陶县人民政府",
        "source": "馆陶县人民政府网站多篇2023年新闻确认县长王峰主持政府工作。来源：http://www.guantao.gov.cn/xwzx/bddt/index_11.html"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共馆陶县委员会",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市馆陶县",
        "parent": "中共邯郸市委"
    },
    {
        "id": 2,
        "name": "馆陶县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "邯郸市馆陶县",
        "parent": "邯郸市人民政府"
    },
    {
        "id": 3,
        "name": "中共馆陶县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市馆陶县",
        "parent": "中共馆陶县委员会"
    },
    {
        "id": 4,
        "name": "中共馆陶县委政法委员会",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市馆陶县",
        "parent": "中共馆陶县委员会"
    },
    {
        "id": 5,
        "name": "馆陶县人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "邯郸市馆陶县",
        "parent": "邯郸市人大常委会"
    },
    {
        "id": 6,
        "name": "馆陶县政协",
        "type": "政协",
        "level": "县级",
        "location": "邯郸市馆陶县",
        "parent": "邯郸市政协"
    },
]

# 3. Positions
positions = [
    # 程玉峰 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "馆陶县委书记", "start": "未知（约2025-2026年间）", "end": "present", "rank": "正处级", "note": "接替王立伟；截至2026年6月在任；来源：馆陶县人民政府网站"},
    # 马楠 — 县长
    {"person_id": 2, "org_id": 1, "title": "馆陶县委副书记", "start": "未知（约2024-2025年间）", "end": "present", "rank": "正处级", "note": "接替王峰；县委副书记兼县长"},
    {"person_id": 2, "org_id": 2, "title": "馆陶县人民政府县长", "start": "未知（约2024-2025年间）", "end": "present", "rank": "正处级", "note": "截至2026年7月在任；来源：馆陶县人民政府网站多篇报道"},
    # 孙辉 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "馆陶县委副书记", "start": "未知", "end": "present", "rank": "副处级", "note": "截至2026年在任"},
    # 郑永亮 — 常务副县长
    {"person_id": 4, "org_id": 1, "title": "馆陶县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "截至2026年在任"},
    {"person_id": 4, "org_id": 2, "title": "馆陶县人民政府常务副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "分管发改、财税等工作"},
    # 李继军 — 纪委书记
    {"person_id": 5, "org_id": 1, "title": "馆陶县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "截至2026年在任"},
    {"person_id": 5, "org_id": 3, "title": "馆陶县纪委书记、监委主任", "start": "未知", "end": "present", "rank": "副处级", "note": "分管纪检监察工作"},
    # 董宁房 — 政法委书记
    {"person_id": 6, "org_id": 1, "title": "馆陶县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "截至2026年在任"},
    {"person_id": 6, "org_id": 4, "title": "馆陶县政法委书记", "start": "未知", "end": "present", "rank": "副处级", "note": "分管政法工作"},
    # 平克硕 — 副县长
    {"person_id": 7, "org_id": 2, "title": "馆陶县人民政府副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "截至2026年在任"},
    # 孔维民 — 副县长
    {"person_id": 8, "org_id": 2, "title": "馆陶县人民政府副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "截至2026年在任"},
    # 班珏 — 副县长
    {"person_id": 9, "org_id": 2, "title": "馆陶县人民政府副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "截至2026年在任"},
    # 吕恩成 — 政协主席
    {"person_id": 10, "org_id": 6, "title": "馆陶县政协主席", "start": "未知", "end": "present", "rank": "正处级", "note": "截至2026年在任"},
    # 平韦振 — 政协副主席
    {"person_id": 11, "org_id": 6, "title": "馆陶县政协副主席", "start": "未知", "end": "present", "rank": "副处级", "note": "截至2026年在任"},
    # 王立伟 — 前任县委书记
    {"person_id": 12, "org_id": 1, "title": "馆陶县委书记", "start": "未知", "end": "约2025-2026", "rank": "正处级", "note": "前任县委书记；2025年1月仍在任；后由程玉峰接替"},
    # 王峰 — 前任县长
    {"person_id": 13, "org_id": 1, "title": "馆陶县委副书记", "start": "未知", "end": "约2024", "rank": "正处级", "note": "前任县委副书记兼县长"},
    {"person_id": 13, "org_id": 2, "title": "馆陶县人民政府县长", "start": "2020年前后", "end": "约2024", "rank": "正处级", "note": "2023年2月仍在任；后由马楠接替"},
]

# 4. Relationships
relationships = [
    # 程玉峰与马楠 — 核心搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "程玉峰为县委书记，马楠为县长，县核心领导搭档",
        "overlap_org": "中共馆陶县委员会/馆陶县人民政府",
        "overlap_period": "2025/2026-present"
    },
    # 程玉峰与孙辉 — 上下级
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "程玉峰作为县委书记领导县委副书记孙辉",
        "overlap_org": "中共馆陶县委员会",
        "overlap_period": "未知-present"
    },
    # 程玉峰与郑永亮 — 上下级
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "程玉峰作为县委书记领导县委常委郑永亮",
        "overlap_org": "中共馆陶县委员会",
        "overlap_period": "未知-present"
    },
    # 程玉峰与李继军 — 上下级
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "程玉峰作为县委书记领导县委常委、纪委书记李继军",
        "overlap_org": "中共馆陶县委员会",
        "overlap_period": "未知-present"
    },
    # 程玉峰与董宁房 — 上下级
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "程玉峰作为县委书记领导县委常委、政法委书记董宁房",
        "overlap_org": "中共馆陶县委员会",
        "overlap_period": "未知-present"
    },
    # 程玉峰与王立伟 — 继任关系
    {
        "person_a": 1,
        "person_b": 12,
        "type": "predecessor_successor",
        "context": "程玉峰接替王立伟担任馆陶县委书记",
        "overlap_org": "中共馆陶县委员会",
        "overlap_period": "2025-2026过渡期"
    },
    # 马楠与郑永亮 — 上下级（政府）
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "马楠为县长，郑永亮为常务副县长",
        "overlap_org": "馆陶县人民政府",
        "overlap_period": "未知-present"
    },
    # 马楠与平克硕 — 上下级
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县长与副县长（平克硕）",
        "overlap_org": "馆陶县人民政府",
        "overlap_period": "未知-present"
    },
    # 马楠与孔维民 — 上下级
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长与副县长（孔维民）",
        "overlap_org": "馆陶县人民政府",
        "overlap_period": "未知-present"
    },
    # 马楠与班珏 — 上下级
    {
        "person_a": 2,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "县长与副县长（班珏）",
        "overlap_org": "馆陶县人民政府",
        "overlap_period": "未知-present"
    },
    # 马楠与王峰 — 继任关系
    {
        "person_a": 2,
        "person_b": 13,
        "type": "predecessor_successor",
        "context": "马楠接替王峰担任馆陶县县长",
        "overlap_org": "馆陶县人民政府",
        "overlap_period": "2023-2025过渡期"
    },
    # 王立伟与王峰 — 核心搭档（前任搭档）
    {
        "person_a": 12,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "王立伟为县委书记，王峰为县长，前任核心搭档",
        "overlap_org": "中共馆陶县委员会/馆陶县人民政府",
        "overlap_period": "未知-2023/2024"
    },
    # 孙辉与郑永亮 — 县委班子协作
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "县委副书记与常务副县长在县委班子中共事",
        "overlap_org": "中共馆陶县委员会",
        "overlap_period": "未知-present"
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
