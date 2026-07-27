#!/usr/bin/env python3
"""濮阳市台前县领导班子工作关系网络 — 数据构建脚本。

等级: 县
调查日期: 2026-07-24
信息来源:
  - 台前县人民政府网站 (www.taiqian.gov.cn)
  - 台前县人民政府政府领导页面 (zfxx_gk/zfxx_ldjj.thtml?id=20579)
  - 台前县第十一次党代会新闻报道
  - 台前县人民政府网站搜索 (关键词: 县委书记)
"""

from __future__ import annotations

import json
import sqlite3  # used by gov_relation.runner via run_build
import sys
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "台前县"
TODAY = "2026-07-24"
STAGING = Path(__file__).resolve().parent

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee, 2xxx = government

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 县委书记 — 待确认
    # ═══════════════════════════════════════════════════════════════════════
    # 孙庆伟在2024年12月仍以县委书记身份活动。台前县第十一次党代会于2026年6月召开，
    # 新的县委书记应已产生，但公开信息中尚未明确。
    {
        "id": 1001,
        "name": "（县委书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "台前县委书记（待确认）",
        "current_org": "中共台前县委员会",
        "source": "http://www.taiqian.gov.cn/search/index.thtml?keyword=县委书记",  # search shows 孙庆伟 latest Dec 2024
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 郑广田 — 县委副书记、县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2001,
        "name": "郑广田",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-03",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "中共台前县委副书记、县人民政府党组书记、县长",
        "current_org": "台前县人民政府",
        "source": "http://www.taiqian.gov.cn/zfxx_gk/zfxx_ldjj.thtml?id=20579",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 刘文博 — 县委常委、常务副县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2002,
        "name": "刘文博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-11",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "中共台前县委常委、县政府党组副书记、常务副县长",
        "current_org": "台前县人民政府",
        "source": "http://www.taiqian.gov.cn/zfxx_gk/zfxx_ldjj.thtml?id=20579",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. 黄山根 — 县委常委、副县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2003,
        "name": "黄山根",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-03",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "中共台前县委常委、县人民政府副县长",
        "current_org": "台前县人民政府",
        "source": "http://www.taiqian.gov.cn/zfxx_gk/zfxx_ldjj.thtml?id=20579",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 5. 白雪飞 — 副县长、县公安局局长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2004,
        "name": "白雪飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-06",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "台前县人民政府副县长、兼任县公安局局长",
        "current_org": "台前县人民政府",
        "source": "http://www.taiqian.gov.cn/zfxx_gk/zfxx_ldjj.thtml?id=20579",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 6. 刘燕南 — 副县长、吴坝镇党委书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2005,
        "name": "刘燕南",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986-12",
        "birthplace": "",
        "education": "本科",
        "party_join": "",
        "work_start": "",
        "current_post": "台前县人民政府副县长、兼任吴坝镇党委书记",
        "current_org": "台前县人民政府",
        "source": "http://www.taiqian.gov.cn/zfxx_gk/zfxx_ldjj.thtml?id=20579",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 7. 赵宪生 — 副县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2006,
        "name": "赵宪生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-05",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "台前县人民政府副县长",
        "current_org": "台前县人民政府",
        "source": "http://www.taiqian.gov.cn/zfxx_gk/zfxx_ldjj.thtml?id=20579",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 8. 李扬 — 副县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2007,
        "name": "李扬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-05",
        "birthplace": "",
        "education": "研究生，管理学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "台前县人民政府副县长",
        "current_org": "台前县人民政府",
        "source": "http://www.taiqian.gov.cn/zfxx_gk/zfxx_ldjj.thtml?id=20579",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 9. 孙庆伟 — 前任县委书记（~2022–2025/2026）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "孙庆伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（已离任台前县委书记，现任职务待查）",
        "current_org": "",
        "source": "http://www.taiqian.gov.cn/search/index.thtml?keyword=县委书记",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 10. 王俊海 — 前任县委书记（~2021–2022）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1003,
        "name": "王俊海",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（已离任台前县委书记，现任职务待查）",
        "current_org": "",
        "source": "http://www.taiqian.gov.cn/search/index.thtml?keyword=县委书记",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 11. 李志华 — 前任县长（~2022–2025）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1004,
        "name": "李志华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（已离任台前县长，现任职务待查）",
        "current_org": "",
        "source": "http://www.taiqian.gov.cn/content/2024/1143513.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 12. 张雁 — 前县委常委、常务副县长（~2025）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2008,
        "name": "张雁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（已离任台前县委常委、常务副县长，现任职务待查）",
        "current_org": "",
        "source": "http://www.taiqian.gov.cn/content/2025/1144348.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
# Org IDs: 1–99 for party/government core, 100+ for departments

organizations = [
    {
        "id": 1,
        "name": "中共台前县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共濮阳市委",
        "location": "台前县",
    },
    {
        "id": 2,
        "name": "台前县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "濮阳市人民政府",
        "location": "台前县",
    },
    {
        "id": 3,
        "name": "台前县纪委监委",
        "type": "纪律检查",
        "level": "县处级",
        "parent": "濮阳市纪委监委",
        "location": "台前县",
    },
    {
        "id": 4,
        "name": "台前县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "濮阳市人大常委会",
        "location": "台前县",
    },
    {
        "id": 5,
        "name": "台前县政协",
        "type": "政协",
        "level": "县处级",
        "parent": "濮阳市政协",
        "location": "台前县",
    },
    {
        "id": 6,
        "name": "台前县公安局",
        "type": "政府",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
    {
        "id": 7,
        "name": "中共吴坝镇委员会",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "中共台前县委员会",
        "location": "台前县吴坝镇",
    },
    {
        "id": 8,
        "name": "台前县审计局",
        "type": "政府",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
    {
        "id": 9,
        "name": "台前县发展和改革委员会",
        "type": "政府",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
    {
        "id": 10,
        "name": "台前县财政局",
        "type": "政府",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
    {
        "id": 11,
        "name": "台前县先进制造业开发区",
        "type": "开发区",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
    {
        "id": 12,
        "name": "台前县应急管理局",
        "type": "政府",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
    {
        "id": 13,
        "name": "台前县农业农村局",
        "type": "政府",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
    {
        "id": 14,
        "name": "濮阳市生态环境局台前分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "濮阳市生态环境局",
        "location": "台前县",
    },
    {
        "id": 15,
        "name": "台前县住房和城乡建设局",
        "type": "政府",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
    {
        "id": 16,
        "name": "台前县城市管理局",
        "type": "政府",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
    {
        "id": 17,
        "name": "台前县自然资源局",
        "type": "政府",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
    {
        "id": 18,
        "name": "台前县交通运输局",
        "type": "政府",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
    {
        "id": 19,
        "name": "台前县商务局",
        "type": "政府",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
    {
        "id": 20,
        "name": "台前县市场监督管理局",
        "type": "政府",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
    {
        "id": 21,
        "name": "台前县司法局",
        "type": "政府",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
    {
        "id": 22,
        "name": "台前县信访局",
        "type": "政府",
        "level": "乡科级",
        "parent": "台前县人民政府",
        "location": "台前县",
    },
]

# ── Positions ─────────────────────────────────────────────────────────────────
# position id: person_org_seq

positions = [
    # 县委书记（待确认）
    {"id": 100101, "person_id": 1001, "org_id": 1, "title": "县委书记（待确认）", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 郑广田
    {"id": 200101, "person_id": 2001, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"id": 200102, "person_id": 2001, "org_id": 2, "title": "县长、党组书记", "start": "", "end": "present", "rank": "正处级", "note": "主持县政府全面工作，分管审计局"},
    # 刘文博
    {"id": 200201, "person_id": 2002, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"id": 200202, "person_id": 2002, "org_id": 2, "title": "常务副县长、党组副书记", "start": "", "end": "present", "rank": "副处级", "note": "负责发改、财政、人社、应急、统计、金融、营商环境、先进制造业开发区等工作"},
    # 黄山根
    {"id": 200301, "person_id": 2003, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"id": 200302, "person_id": 2003, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责工信、交通、商务、市场监管、供电、通讯等工作"},
    # 白雪飞
    {"id": 200401, "person_id": 2004, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"id": 200402, "person_id": 2004, "org_id": 6, "title": "县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": "负责公安、司法、信访等工作"},
    # 刘燕南
    {"id": 200501, "person_id": 2005, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"id": 200502, "person_id": 2005, "org_id": 7, "title": "吴坝镇党委书记（兼）", "start": "", "end": "present", "rank": "乡科级", "note": "主持吴坝镇党委全面工作"},
    # 赵宪生
    {"id": 200601, "person_id": 2006, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责农业农村、乡村振兴、水利、民政等工作"},
    # 李扬
    {"id": 200701, "person_id": 2007, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责生态环境、住建、城管、自然资源等工作"},
    # 孙庆伟（前任县委书记，2022–2025/2026）
    {"id": 100201, "person_id": 1002, "org_id": 1, "title": "县委书记", "start": "~2022", "end": "~2025/2026", "rank": "正处级", "note": "前任县委书记，2024年12月仍有相关报道"},
    # 王俊海（前任县委书记，~2021–2022）
    {"id": 100301, "person_id": 1003, "org_id": 1, "title": "县委书记", "start": "~2021", "end": "~2022", "rank": "正处级", "note": "2022年多次出现在公开报道中"},
    # 李志华（前任县长）
    {"id": 100401, "person_id": 1004, "org_id": 2, "title": "县长", "start": "~2022", "end": "~2025", "rank": "正处级", "note": "2024年6月与孙庆伟共同活动"},
    # 张雁（前常务副县长）
    {"id": 200801, "person_id": 2008, "org_id": 2, "title": "常务副县长", "start": "~2023", "end": "~2025", "rank": "副处级", "note": "2025年3月报道为县委常委、常务副县长"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
# Relationship IDs: 10000+

relationships = [
    # ── 郑广田 <-> 刘文博: 上下级（县长–常务副县长） ──
    {
        "id": 10001,
        "person_a": 2001,
        "person_b": 2002,
        "type": "superior_subordinate",
        "context": "县长与常务副县长，县政府党组同僚",
        "overlap_org": "台前县人民政府",
        "overlap_period": "2025–2026",
    },
    # ── 郑广田 <-> 黄山根: 上下级（县长–副县长） ──
    {
        "id": 10002,
        "person_a": 2001,
        "person_b": 2003,
        "type": "superior_subordinate",
        "context": "县长与县委常委、副县长",
        "overlap_org": "台前县人民政府",
        "overlap_period": "2025–2026",
    },
    # ── 郑广田 <-> 白雪飞: 上下级（县长–副县长/公安局长） ──
    {
        "id": 10003,
        "person_a": 2001,
        "person_b": 2004,
        "type": "superior_subordinate",
        "context": "县长与副县长兼公安局长",
        "overlap_org": "台前县人民政府",
        "overlap_period": "2025–2026",
    },
    # ── 郑广田 <-> 赵宪生: 上下级（县长–副县长） ──
    {
        "id": 10004,
        "person_a": 2001,
        "person_b": 2006,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "台前县人民政府",
        "overlap_period": "2025–2026",
    },
    # ── 郑广田 <-> 李扬: 上下级（县长–副县长） ──
    {
        "id": 10005,
        "person_a": 2001,
        "person_b": 2007,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "台前县人民政府",
        "overlap_period": "2025–2026",
    },
    # ── 刘文博 <-> 郑广田: 常务副县长协助县长 ──
    {
        "id": 10006,
        "person_a": 2002,
        "person_b": 2001,
        "type": "overlap",
        "context": "常务副县长协助县长主持县政府常务工作",
        "overlap_org": "台前县人民政府",
        "overlap_period": "2025–2026",
    },
    # ── 黄山根 <-> 刘文博: 工作交叉（应急管理） ──
    {
        "id": 10007,
        "person_a": 2003,
        "person_b": 2002,
        "type": "overlap",
        "context": "黄山根协助刘文博负责应急管理工作",
        "overlap_org": "台前县人民政府",
        "overlap_period": "2025–2026",
    },
    # ── 白雪飞 <-> 公安局: 公安局长 ──
    {
        "id": 10008,
        "person_a": 2004,
        "person_b": 2004,
        "type": "overlap",
        "context": "副县长兼任公安局长",
        "overlap_org": "台前县人民政府",
        "overlap_period": "2025–2026",
    },
    # ── 孙庆伟 -> 郑广田: 前后任（县委书记–县长共事） ──
    {
        "id": 10009,
        "person_a": 1002,
        "person_b": 2001,
        "type": "predecessor_successor",
        "context": "孙庆伟任县委书记期间，郑广田继李志华之后接任县长",
        "overlap_org": "台前县",
        "overlap_period": "~2025",
    },
    # ── 孙庆伟 -> 李志华: 县委书记–县长（搭档） ──
    {
        "id": 10010,
        "person_a": 1002,
        "person_b": 1004,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭档",
        "overlap_org": "台前县",
        "overlap_period": "~2022–2025",
    },
    # ── 王俊海 -> 孙庆伟: 前后任县委书记 ──
    {
        "id": 10011,
        "person_a": 1003,
        "person_b": 1002,
        "type": "predecessor_successor",
        "context": "王俊海离任后孙庆伟接任县委书记",
        "overlap_org": "中共台前县委员会",
        "overlap_period": "~2022",
    },
    # ── 张雁 -> 刘文博: 前后任常务副县长 ──
    {
        "id": 10012,
        "person_a": 2008,
        "person_b": 2002,
        "type": "predecessor_successor",
        "context": "张雁之前任常务副县长，刘文博接任",
        "overlap_org": "台前县人民政府",
        "overlap_period": "~2025",
    },
    # ── 刘燕南 <-> 吴坝镇: 兼任党委书记 ──
    {
        "id": 10013,
        "person_a": 2005,
        "person_b": 2005,
        "type": "overlap",
        "context": "副县长兼任吴坝镇党委书记",
        "overlap_org": "台前县人民政府",
        "overlap_period": "2025–2026",
    },
]


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )


if __name__ == "__main__":
    main()
