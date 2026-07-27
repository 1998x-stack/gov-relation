#!/usr/bin/env python3
"""濮阳市华龙区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区
调查日期: 2026-07-24
信息来源:
  - 华龙区人民政府网站 (pyhualong.gov.cn)
  - 中国共产党濮阳市华龙区第五次代表大会新闻报道
  - 华龙区人民政府政府领导页面
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "华龙区"
TODAY = "2026-07-24"
STAGING = Path(__file__).resolve().parent

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee, 2xxx = government

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 丁国梁 — 区委书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1001,
        "name": "丁国梁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区委书记",
        "current_org": "中共濮阳市华龙区委员会",
        "source": "http://www.pyhualong.gov.cn/content/2026/1280150.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 魏志峰 — 区委副书记、区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "魏志峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区委副书记、区人民政府党组书记、区长",
        "current_org": "华龙区人民政府",
        "source": "http://www.pyhualong.gov.cn/zfld.thtml?cid=12130",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 王建斋 — 区委副书记（推定）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1003,
        "name": "王建斋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区委副书记（推定）",
        "current_org": "中共濮阳市华龙区委员会",
        "source": "http://www.pyhualong.gov.cn/content/2026/1280150.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. 邵宁 — 区委常委、常务副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1004,
        "name": "邵宁",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区委常委、区人民政府党组副书记、副区长",
        "current_org": "华龙区人民政府",
        "source": "http://www.pyhualong.gov.cn/zfld.thtml?cid=12130",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 5. 张静 — 区委常委、副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1005,
        "name": "张静",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区委常委、区人民政府党组副书记、副区长",
        "current_org": "华龙区人民政府",
        "source": "http://www.pyhualong.gov.cn/zfld.thtml?cid=12130",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 6. 王秋英 — 副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2001,
        "name": "王秋英",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区人民政府副区长",
        "current_org": "华龙区人民政府",
        "source": "http://www.pyhualong.gov.cn/zfld.thtml?cid=12130",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 7. 季景力 — 副区长、市公安局华龙分局局长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2002,
        "name": "季景力",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区人民政府副区长，濮阳市公安局华龙区分局党委书记、局长",
        "current_org": "濮阳市公安局华龙区分局",
        "source": "http://www.pyhualong.gov.cn/zfld.thtml?cid=12130",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 8. 杨峰 — 副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2003,
        "name": "杨峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区人民政府党组成员、副区长",
        "current_org": "华龙区人民政府",
        "source": "http://www.pyhualong.gov.cn/zfld.thtml?cid=12130",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 9. 谢国贤 — 副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2004,
        "name": "谢国贤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区人民政府副区长",
        "current_org": "华龙区人民政府",
        "source": "http://www.pyhualong.gov.cn/zfld.thtml?cid=12130",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 10. 海军 — 二级调研员（分管教育）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2005,
        "name": "海军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区人民政府二级调研员",
        "current_org": "华龙区人民政府",
        "source": "http://www.pyhualong.gov.cn/zfld.thtml?cid=12130",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 11. 王宏耀 — 区委常委（纪委/监委推定）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1006,
        "name": "王宏耀",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区委常委（推定纪委书记）",
        "current_org": "中共濮阳市华龙区纪律检查委员会",
        "source": "http://www.pyhualong.gov.cn/content/2026/1280150.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 12. 郝国华 — 区委常委（推定政法委书记）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1007,
        "name": "郝国华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区委常委（推定政法委书记）",
        "current_org": "中共濮阳市华龙区委员会",
        "source": "http://www.pyhualong.gov.cn/content/2026/1280150.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 13. 张兵宽 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1008,
        "name": "张兵宽",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区委常委",
        "current_org": "中共濮阳市华龙区委员会",
        "source": "http://www.pyhualong.gov.cn/content/2026/1280150.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 14. 李恒山 — 区委常委、宣传部部长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1009,
        "name": "李恒山",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区委常委、宣传部部长",
        "current_org": "中共濮阳市华龙区委员会",
        "source": "http://www.pyhualong.gov.cn/content/2026/1281001.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 15. 姜士波 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1010,
        "name": "姜士波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区委常委（推定组织部长）",
        "current_org": "中共濮阳市华龙区委员会",
        "source": "http://www.pyhualong.gov.cn/content/2026/1280150.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 16. 刘法军 — 区委常委（推定统战部长/武装部）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1011,
        "name": "刘法军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区委常委",
        "current_org": "中共濮阳市华龙区委员会",
        "source": "http://www.pyhualong.gov.cn/content/2026/1280150.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 17. 梅兴秦 — 前任区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1012,
        "name": "梅兴秦",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已调任（前任华龙区区长）",
        "current_org": "",
        "source": "http://www.pyhualong.gov.cn/content/2026/1266004.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 18. 杨理宏 — 人大主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1013,
        "name": "杨理宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区人大常委会主任",
        "current_org": "华龙区人民代表大会常务委员会",
        "source": "http://www.pyhualong.gov.cn/content/2026/1280150.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 19. 侯富浩 — 政协主席
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1014,
        "name": "侯富浩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "华龙区政协主席",
        "current_org": "中国人民政治协商会议濮阳市华龙区委员会",
        "source": "http://www.pyhualong.gov.cn/content/2026/1280150.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 20. 姜凯 — 濮阳高新技术产业开发区管委会主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1015,
        "name": "姜凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "濮阳高新技术产业开发区管委会主任",
        "current_org": "濮阳高新技术产业开发区",
        "source": "http://www.pyhualong.gov.cn/content/2026/1276740.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 10,
        "name": "中共濮阳市华龙区委员会",
        "type": "party",
        "level": "district",
        "parent": "中共濮阳市委员会",
        "location": "华龙区",
    },
    {
        "id": 11,
        "name": "华龙区人民政府",
        "type": "government",
        "level": "district",
        "parent": "濮阳市人民政府",
        "location": "华龙区",
    },
    {
        "id": 12,
        "name": "中共濮阳市华龙区纪律检查委员会",
        "type": "party_discipline",
        "level": "district",
        "parent": "中共濮阳市纪律检查委员会",
        "location": "华龙区",
    },
    {
        "id": 13,
        "name": "华龙区人民代表大会常务委员会",
        "type": "npc",
        "level": "district",
        "parent": "濮阳市人民代表大会常务委员会",
        "location": "华龙区",
    },
    {
        "id": 14,
        "name": "中国人民政治协商会议濮阳市华龙区委员会",
        "type": "cppcc",
        "level": "district",
        "parent": "政协濮阳市委员会",
        "location": "华龙区",
    },
    {
        "id": 15,
        "name": "濮阳市公安局华龙区分局",
        "type": "government",
        "level": "district",
        "parent": "濮阳市公安局",
        "location": "华龙区",
    },
    {
        "id": 16,
        "name": "濮阳高新技术产业开发区",
        "type": "development_zone",
        "level": "district",
        "parent": "华龙区人民政府",
        "location": "华龙区",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 丁国梁 — 区委书记
    {"person_id": 1001, "org_id": 10, "title": "华龙区委书记", "start": "", "end": "present", "rank": "正县级", "note": "2026年6月连任第五届区委书记"},
    # 魏志峰 — 区长
    {"person_id": 1002, "org_id": 11, "title": "华龙区委副书记、区人民政府党组书记、区长", "start": "2026", "end": "present", "rank": "正县级", "note": "2026年新任区长"},
    {"person_id": 1002, "org_id": 10, "title": "华龙区委副书记", "start": "2026", "end": "present", "rank": "副厅?", "note": ""},
    # 王建斋 — 区委副书记
    {"person_id": 1003, "org_id": 10, "title": "华龙区委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 邵宁 — 常务副区长
    {"person_id": 1004, "org_id": 11, "title": "华龙区委常委、区人民政府党组副书记、副区长", "start": "", "end": "present", "rank": "副县级", "note": "负责区政府常务工作"},
    {"person_id": 1004, "org_id": 10, "title": "华龙区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 张静 — 副区长
    {"person_id": 1005, "org_id": 11, "title": "华龙区委常委、区人民政府党组副书记、副区长", "start": "", "end": "present", "rank": "副县级", "note": "负责工业、商务、科技等"},
    {"person_id": 1005, "org_id": 10, "title": "华龙区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 王秋英 — 副区长
    {"person_id": 2001, "org_id": 11, "title": "华龙区人民政府副区长", "start": "", "end": "present", "rank": "副县级", "note": "负责农业农村、水利、文旅、卫健等"},
    # 季景力 — 副区长兼公安局长
    {"person_id": 2002, "org_id": 11, "title": "华龙区人民政府副区长", "start": "", "end": "present", "rank": "副县级", "note": "负责公安、司法、信访"},
    {"person_id": 2002, "org_id": 15, "title": "濮阳市公安局华龙区分局党委书记、局长", "start": "", "end": "present", "rank": "一级高级警长", "note": "同时任濮阳市公安局党委委员、副局长"},
    # 杨峰 — 副区长
    {"person_id": 2003, "org_id": 11, "title": "华龙区人民政府党组成员、副区长", "start": "", "end": "present", "rank": "副县级", "note": "负责住建、城管、交通等"},
    # 谢国贤 — 副区长
    {"person_id": 2004, "org_id": 11, "title": "华龙区人民政府副区长", "start": "", "end": "present", "rank": "副县级", "note": "负责金融工作"},
    # 海军 — 二级调研员
    {"person_id": 2005, "org_id": 11, "title": "华龙区人民政府二级调研员", "start": "", "end": "present", "rank": "副县级", "note": "负责教育工作"},
    # 王宏耀 — 推定纪委书记
    {"person_id": 1006, "org_id": 12, "title": "华龙区委常委、纪委书记（推定）", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 1006, "org_id": 10, "title": "华龙区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 郝国华 — 推定政法委书记
    {"person_id": 1007, "org_id": 10, "title": "华龙区委常委（推定政法委书记）", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 张兵宽 — 区委常委
    {"person_id": 1008, "org_id": 10, "title": "华龙区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 李恒山 — 宣传部长
    {"person_id": 1009, "org_id": 10, "title": "华龙区委常委、宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 姜士波 — 推定组织部长
    {"person_id": 1010, "org_id": 10, "title": "华龙区委常委（推定组织部长）", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 刘法军 — 区委常委
    {"person_id": 1011, "org_id": 10, "title": "华龙区委常委", "start": "", "end": "present", "rank": "副县级", "note": "推定统战部长或武装部长"},
    # 梅兴秦 — 前任区长
    {"person_id": 1012, "org_id": 11, "title": "华龙区区长（前任）", "start": "", "end": "2026", "rank": "正县级", "note": "2026年4月仍在区长任上，后由魏志峰接任"},
    # 杨理宏 — 人大主任
    {"person_id": 1013, "org_id": 13, "title": "华龙区人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # 侯富浩 — 政协主席
    {"person_id": 1014, "org_id": 14, "title": "华龙区政协主席", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # 姜凯 — 高新区管委会主任
    {"person_id": 1015, "org_id": 16, "title": "濮阳高新技术产业开发区管委会主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 丁国梁 ↔ 魏志峰 — 书记+区长搭档
    {
        "person_a": 1001,
        "person_b": 1002,
        "type": "superior_subordinate",
        "context": "区委书记与区长搭档关系",
        "overlap_org": "中共濮阳市华龙区委员会",
        "overlap_period": "2026至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 丁国梁 ↔ 王建斋 — 书记+副书记
    {
        "person_a": 1001,
        "person_b": 1003,
        "type": "superior_subordinate",
        "context": "区委书记与区委副书记",
        "overlap_org": "中共濮阳市华龙区委员会",
        "overlap_period": "2026至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 魏志峰 — 梅兴秦 前后任区长
    {
        "person_a": 1002,
        "person_b": 1012,
        "type": "predecessor_successor",
        "context": "魏志峰接替梅兴秦任区长",
        "overlap_org": "华龙区人民政府",
        "overlap_period": "2026",
        "strength": "medium",
        "confidence": "plausible",
    },
    # 丁国梁 — 区委常委班子全体
    {
        "person_a": 1001,
        "person_b": 1003,
        "type": "superior_subordinate",
        "context": "区委书记与副书记",
        "overlap_org": "中共濮阳市华龙区委员会",
        "overlap_period": "2026至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1001,
        "person_b": 1004,
        "type": "superior_subordinate",
        "context": "区委书记与常委、常务副区长",
        "overlap_org": "中共濮阳市华龙区委员会",
        "overlap_period": "2026至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1001,
        "person_b": 1005,
        "type": "superior_subordinate",
        "context": "区委书记与常委、副区长",
        "overlap_org": "中共濮阳市华龙区委员会",
        "overlap_period": "2026至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1001,
        "person_b": 1006,
        "type": "superior_subordinate",
        "context": "区委书记与纪委书记",
        "overlap_org": "中共濮阳市华龙区委员会",
        "overlap_period": "2026至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1001,
        "person_b": 1007,
        "type": "superior_subordinate",
        "context": "区委书记与常委",
        "overlap_org": "中共濮阳市华龙区委员会",
        "overlap_period": "2026至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1001,
        "person_b": 1008,
        "type": "superior_subordinate",
        "context": "区委书记与常委",
        "overlap_org": "中共濮阳市华龙区委员会",
        "overlap_period": "2026至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1001,
        "person_b": 1009,
        "type": "superior_subordinate",
        "context": "区委书记与宣传部长",
        "overlap_org": "中共濮阳市华龙区委员会",
        "overlap_period": "2026至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1001,
        "person_b": 1010,
        "type": "superior_subordinate",
        "context": "区委书记与常委",
        "overlap_org": "中共濮阳市华龙区委员会",
        "overlap_period": "2026至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1001,
        "person_b": 1011,
        "type": "superior_subordinate",
        "context": "区委书记与常委",
        "overlap_org": "中共濮阳市华龙区委员会",
        "overlap_period": "2026至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 邵宁 ↔ 张静 — 同为政府副职
    {
        "person_a": 1004,
        "person_b": 1005,
        "type": "overlap",
        "context": "同为区政府副职（均为区委常委、副区长）",
        "overlap_org": "华龙区人民政府",
        "overlap_period": "2026至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 王秋英 ↔ 杨峰 — 同为副区长
    {
        "person_a": 2001,
        "person_b": 2003,
        "type": "overlap",
        "context": "同为华龙区副区长",
        "overlap_org": "华龙区人民政府",
        "overlap_period": "2026至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
]

# ── Build ─────────────────────────────────────────────────────────────────────
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

    # Print summary for logging
    print(f"\n华龙区 network build complete.")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
