#!/usr/bin/env python3
"""
黄石市西塞山区领导班子工作关系网络 — 数据构建脚本
Build SQLite database + GEXF graph for Xisaishan District leadership.

Task ID: hubei_西塞山区
Province: 湖北省
Parent city: 黄石市
Region: 西塞山区
Level: 市辖区
Targets: 区委书记 & 区长
"""

import sqlite3
import sys
import os
from pathlib import Path

# Ensure gov_relation is importable
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

import os
os.chdir(str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── PERSON DATA ──────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {
        "id": 1,
        "name": "黄毕中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # Unknown
        "birthplace": "",  # Unknown
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共西塞山区委员会",
        "source": "https://www.xisaishan.gov.cn/zxxss/xssyw/202607/t20260713_1342753.html",
    },
    {
        "id": 2,
        "name": "梅浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、代理区长",
        "current_org": "西塞山区人民政府",
        "source": "https://www.xisaishan.gov.cn/zxxss/xssyw/202607/t20260715_1343446.html",
    },
    # ── Party Standing Committee (区委常委) ──
    {
        "id": 3,
        "name": "尹强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、政法委书记",
        "current_org": "中共西塞山区委员会",
        "source": "https://www.xisaishan.gov.cn/zxxss/xssyw/202606/t20260630_1338731.html",
    },
    {
        "id": 4,
        "name": "饶芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共西塞山区委组织部",
        "source": "https://www.xisaishan.gov.cn/zxxss/xssyw/202606/t20260630_1338731.html",
    },
    {
        "id": 5,
        "name": "梁顺兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共西塞山区委员会",
        "source": "https://www.xisaishan.gov.cn/zxxss/xssyw/202607/t20260713_1342753.html",
    },
    {
        "id": 6,
        "name": "王臣志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共西塞山区纪律检查委员会",
        "source": "https://www.xisaishan.gov.cn/zxxss/xssyw/202607/t20260724_1345730.html",
    },
    # ── Government Leaders (区政府) ──
    {
        "id": 7,
        "name": "鲁任胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西塞山区人民政府",
        "source": "https://www.xisaishan.gov.cn/xxgk/fdzdgknr/ldzc/",
    },
    {
        "id": 8,
        "name": "周斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西塞山区人民政府",
        "source": "https://www.xisaishan.gov.cn/xxgk/fdzdgknr/ldzc/",
    },
    {
        "id": 9,
        "name": "游玮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、区公安分局局长",
        "current_org": "西塞山区人民政府/西塞山区公安分局",
        "source": "https://www.xisaishan.gov.cn/xxgk/fdzdgknr/qtzdgknr/rsrm/202602/t20260225_1309886.html",
    },
    {
        "id": 10,
        "name": "苏朱勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西塞山区人民政府",
        "source": "https://www.xisaishan.gov.cn/xxgk/fdzdgknr/qtzdgknr/rsrm/202602/t20260225_1309891.html",
    },
    {
        "id": 11,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西塞山区人民政府",
        "source": "https://www.xisaishan.gov.cn/xxgk/fdzdgknr/ldzc/",
    },
    {
        "id": 12,
        "name": "陈国安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西塞山区人民政府",
        "source": "https://www.xisaishan.gov.cn/xxgk/fdzdgknr/ldzc/",
    },
    {
        "id": 13,
        "name": "周精灵",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西塞山区人民政府",
        "source": "https://www.xisaishan.gov.cn/xxgk/fdzdgknr/ldzc/",
    },
    {
        "id": 14,
        "name": "皮方艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西塞山区人民政府",
        "source": "https://www.xisaishan.gov.cn/xxgk/fdzdgknr/qtzdgknr/rsrm/202602/t20260225_1309889.html",
    },
    {
        "id": 15,
        "name": "徐东升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西塞山区人民政府",
        "source": "https://www.xisaishan.gov.cn/xxgk/fdzdgknr/qtzdgknr/rsrm/202602/t20260225_1309886.html",
    },
    # ── Government Party Members (党组成员) ──
    {
        "id": 16,
        "name": "刘志勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员",
        "current_org": "西塞山区人民政府",
        "source": "https://www.xisaishan.gov.cn/xxgk/fdzdgknr/ldzc/",
    },
    {
        "id": 17,
        "name": "杨明聪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员",
        "current_org": "西塞山区人民政府",
        "source": "https://www.xisaishan.gov.cn/xxgk/fdzdgknr/ldzc/",
    },
    # ──人大、政协领导 ──
    {
        "id": 18,
        "name": "李沈",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "西塞山区人民代表大会常务委员会",
        "source": "https://www.xisaishan.gov.cn/zxxss/xssyw/202606/t20260630_1338731.html",
    },
    {
        "id": 19,
        "name": "唐砚冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议西塞山区委员会",
        "source": "https://www.xisaishan.gov.cn/zxxss/xssyw/202606/t20260630_1338731.html",
    },
    # ── 前任领导（已知部分） ──
    {
        "id": 20,
        "name": "晏勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前区委书记（已离任）",
        "current_org": "（已离任）",
        "source": "inferred from timeline — 黄毕中继任",
    },
    {
        "id": 21,
        "name": "袁辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前副区长（已离任）",
        "current_org": "（已离任）",
        "source": "https://www.xisaishan.gov.cn/xxgk/fdzdgknr/qtzdgknr/rsrm/202602/t20260225_1309889.html",
    },
    {
        "id": 22,
        "name": "周永生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前副区长（已离任）",
        "current_org": "（已离任）",
        "source": "https://www.xisaishan.gov.cn/xxgk/fdzdgknr/qtzdgknr/rsrm/202602/t20260225_1309886.html",
    },
]

# ── ORGANIZATION DATA ────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共西塞山区委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黄石市委",
        "location": "湖北省黄石市西塞山区",
    },
    {
        "id": 2,
        "name": "西塞山区人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "黄石市人民政府",
        "location": "湖北省黄石市西塞山区",
    },
    {
        "id": 3,
        "name": "中共西塞山区委组织部",
        "type": "党委部门",
        "level": "正科级",
        "parent": "中共西塞山区委员会",
        "location": "湖北省黄石市西塞山区",
    },
    {
        "id": 4,
        "name": "中共西塞山区纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共黄石市纪委",
        "location": "湖北省黄石市西塞山区",
    },
    {
        "id": 5,
        "name": "中共西塞山区委政法委员会",
        "type": "党委部门",
        "level": "正科级",
        "parent": "中共西塞山区委员会",
        "location": "湖北省黄石市西塞山区",
    },
    {
        "id": 6,
        "name": "西塞山区公安分局",
        "type": "公安",
        "level": "正科级",
        "parent": "黄石市公安局",
        "location": "湖北省黄石市西塞山区",
    },
    {
        "id": 7,
        "name": "西塞山区人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "黄石市人大常委会",
        "location": "湖北省黄石市西塞山区",
    },
    {
        "id": 8,
        "name": "中国人民政治协商会议西塞山区委员会",
        "type": "政协",
        "level": "县级",
        "parent": "黄石市政协",
        "location": "湖北省黄石市西塞山区",
    },
    {
        "id": 9,
        "name": "西塞山区监察委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "黄石市监察委员会",
        "location": "湖北省黄石市西塞山区",
    },
]

# ── POSITION DATA ────────────────────────────────────────────────────

positions = [
    # 黄毕中
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "至今", "rank": "正县级", "note": "主持区委全面工作"},
    # 梅浩
    {"person_id": 2, "org_id": 2, "title": "代理区长", "start_date": "2026-07", "end_date": "至今", "rank": "正县级", "note": "区政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "至今", "rank": "正县级", "note": ""},
    # 尹强
    {"person_id": 3, "org_id": 1, "title": "区委副书记、政法委书记", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 5, "title": "政法委书记", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 饶芳
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "组织部部长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 梁顺兵
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副县级", "note": "具体分工待确认（可能为区委办主任）"},
    # 王臣志
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "区纪委书记、区监委主任", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 鲁任胜
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 周斌
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 游玮
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "2025-11", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "区公安分局局长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 苏朱勇
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "2025-12", "end_date": "至今", "rank": "副县级", "note": ""},
    # 刘涛
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 陈国安
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 周精灵
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 皮方艳
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "2025-10", "end_date": "至今", "rank": "副县级", "note": ""},
    # 徐东升
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "2025-11", "end_date": "至今", "rank": "副县级", "note": ""},
    # 刘志勇
    {"person_id": 16, "org_id": 2, "title": "区政府党组成员", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 杨明聪
    {"person_id": 17, "org_id": 2, "title": "区政府党组成员", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 李沈
    {"person_id": 18, "org_id": 7, "title": "区人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正县级", "note": ""},
    # 唐砚冰
    {"person_id": 19, "org_id": 8, "title": "区政协主席", "start_date": "", "end_date": "至今", "rank": "正县级", "note": ""},
    # 前任 - 晏勇（前区委书记）
    {"person_id": 20, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "黄毕中的前任"},
    # 前任 - 袁辉（前副区长）
    {"person_id": 21, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "2025-10", "rank": "副县级", "note": "2025年10月28日被免去"},
    # 前任 - 周永生（前副区长）
    {"person_id": 22, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "2025-11", "rank": "副县级", "note": "2025年11月21日被免去"},
]

# ── RELATIONSHIP DATA ────────────────────────────────────────────────

relationships = [
    # 黄毕中 ←→ 梅浩 （区委书记与代理区长的工作关系）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与代理区长，区委区政府主要领导工作关系", "overlap_org": "中共西塞山区委员会/西塞山区人民政府", "overlap_period": "2026-07至今"},
    # 黄毕中 ←→ 尹强 （区委书记与专职副书记）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与区委副书记", "overlap_org": "中共西塞山区委员会", "overlap_period": "至今"},
    # 黄毕中 ←→ 饶芳 （区委书记与组织部长）
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与组织部部长", "overlap_org": "中共西塞山区委员会", "overlap_period": "至今"},
    # 黄毕中 ←→ 王臣志 （区委书记与纪委书记）
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与区纪委书记", "overlap_org": "中共西塞山区委员会", "overlap_period": "至今"},
    # 梅浩 ←→ 各副区长 （区长与副区长）
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "西塞山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "西塞山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "西塞山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "西塞山区人民政府", "overlap_period": "2025-12至今"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "西塞山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "西塞山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "西塞山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "西塞山区人民政府", "overlap_period": "2025-10至今"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "西塞山区人民政府", "overlap_period": "2025-11至今"},
    # 黄毕中 -- 前任继任关系
    {"person_a": 20, "person_b": 1, "type": "predecessor_successor", "context": "前任区委书记与现任区委书记", "overlap_org": "中共西塞山区委员会", "overlap_period": "前后任"},
    # 副区长前任继任关系
    {"person_a": 21, "person_b": 14, "type": "predecessor_successor", "context": "皮方艳接替袁辉副区长职务", "overlap_org": "西塞山区人民政府", "overlap_period": "2025-10前后"},
    {"person_a": 22, "person_b": 9, "type": "predecessor_successor", "context": "游玮接替周永生副区长职务（游玮兼任公安局长）", "overlap_org": "西塞山区人民政府", "overlap_period": "2025-11前后"},
    # 区委常委之间的同僚关系
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同届区委常委班子成员", "overlap_org": "中共西塞山区委员会", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "同届区委常委班子成员", "overlap_org": "中共西塞山区委员会", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "同届区委常委班子成员", "overlap_org": "中共西塞山区委员会", "overlap_period": "至今"},
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "同届区委常委班子成员", "overlap_org": "中共西塞山区委员会", "overlap_period": "至今"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "同届区委常委班子成员", "overlap_org": "中共西塞山区委员会", "overlap_period": "至今"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "同届区委常委班子成员", "overlap_org": "中共西塞山区委员会", "overlap_period": "至今"},
    # 人大政协领导与区委的关系
    {"person_a": 1, "person_b": 18, "type": "overlap", "context": "区委书记与人大常委会主任", "overlap_org": "西塞山区", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 19, "type": "overlap", "context": "区委书记与政协主席", "overlap_org": "西塞山区", "overlap_period": "至今"},
]

# ── BUILD ────────────────────────────────────────────────────────────

STAGING_DIR = Path(__file__).parent
DB_PATH = STAGING_DIR / "西塞山区_network.db"
GEXF_PATH = STAGING_DIR / "西塞山区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="西塞山区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Done. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
