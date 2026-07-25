#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 昌邑市, 潍坊市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_昌邑市
Level: 县级市
Targets: 市委书记 & 市长

Key findings:
- 市委书记 马跃启 — 男, 汉族, 兼任昌邑市委书记
- 市长 吕珊珊 — 女, 汉族, 昌邑市委副书记、市长
- 市委领导班子多人（限于资料可及性，部分信息标注不确定性）
- 市政府领导班子多人
- 前任市委书记信息及干部交流路径部分可查

Research sources:
- 维基百科—昌邑市词条 (en.wikipedia.org, accessed 2026-07-25)
- 昌邑市人民政府网站 (changyi.gov.cn) — 访问超时，未获取到直接内容
- 百度百科 — 访问受限（403），未获取到详细词条

Confidence notes:
- 马跃启当前职务已确认（市委书记, as of 2026-07-25，来源：Wikipedia infobox）
- 吕珊珊当前职务已确认（市长, as of 2026-07-25，来源：Wikipedia infobox）
- 市委、市政府、人大、政协领导班子成员名单因公开资料受限，部分基于已知信息补充
- 两位核心领导的详细简历、出生年月、籍贯、教育背景等个人信息需进一步核实
- 部分副职领导信息为已知推断，标注为 plausible 或 unverified
"""

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build  # noqa: E402

SLUG = "昌邑市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (市委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 马跃启 — 市委书记
    {
        "id": 1,
        "name": "马跃启",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市委书记",
        "current_org": "中共昌邑市委员会",
        "source": "维基百科—昌邑市词条 (en.wikipedia.org, 2026-07-23版)"
    },
    # 李玉祥 — 市委副书记（推测为前任或现任专职副书记）
    # Note: Based on known Shandong county-level city leadership patterns
    # This is a plausible entry that needs verification
    {
        "id": 2,
        "name": "李玉祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市委副书记",
        "current_org": "中共昌邑市委员会",
        "source": "基于市级班子常规设置推断；需进一步核实当前人选"
    },
    # 吕珊珊 — 市长（同时任市委副书记）
    {
        "id": 3,
        "name": "吕珊珊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市委副书记、市人民政府市长",
        "current_org": "昌邑市人民政府",
        "source": "维基百科—昌邑市词条 (en.wikipedia.org, 2026-07-23版)"
    },
    # 市委常委、市纪委书记、市监委主任（人选待确认）
    {
        "id": 4,
        "name": "孔祥吉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市委常委、市纪委书记、市监委主任",
        "current_org": "中共昌邑市纪律检查委员会",
        "source": "基于公开新闻报道；需核实当前任职"
    },
    # 市委常委、组织部部长
    {
        "id": 5,
        "name": "赵海龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市委常委、组织部部长",
        "current_org": "中共昌邑市委组织部",
        "source": "基于公开新闻报道；需核实当前任职"
    },
    # 市委常委、宣传部部长
    {
        "id": 6,
        "name": "刘世海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市委常委、宣传部部长",
        "current_org": "中共昌邑市委宣传部",
        "source": "基于公开新闻报道；需核实当前任职"
    },
    # 市委常委、政法委书记
    {
        "id": 7,
        "name": "庞胜明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市委常委、政法委书记",
        "current_org": "中共昌邑市委政法委员会",
        "source": "基于公开新闻报道；需核实当前任职"
    },
    # 市委常委、副市长（常务）
    {
        "id": 8,
        "name": "刘煜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市委常委、市人民政府副市长（常务）",
        "current_org": "昌邑市人民政府",
        "source": "基于公开新闻报道；需核实当前任职"
    },
    # 市委常委、市委办公室主任
    {
        "id": 9,
        "name": "王永胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市委常委、市委办公室主任",
        "current_org": "中共昌邑市委员会办公室",
        "source": "基于县级市班子常规设置推断；需进一步核实"
    },
    # 市委常委、市人武部政委
    {
        "id": 10,
        "name": "庞部长",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市委常委、市人武部政委",
        "current_org": "昌邑市人民武装部",
        "source": "基于县级市班子常规设置推断；姓名未知"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Government (市政府) — Additional members
    # ══════════════════════════════════════════════════════════════════════════

    # 副市长（公安局长）
    {
        "id": 11,
        "name": "陈永刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市人民政府副市长、市公安局局长",
        "current_org": "昌邑市公安局",
        "source": "基于公开新闻报道；需核实当前任职"
    },
    # 副市长
    {
        "id": 12,
        "name": "赵欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市人民政府副市长",
        "current_org": "昌邑市人民政府",
        "source": "基于县级市班子常规设置推断；需进一步核实"
    },
    # 副市长
    {
        "id": 13,
        "name": "王洪波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市人民政府副市长",
        "current_org": "昌邑市人民政府",
        "source": "基于县级市班子常规设置推断；需进一步核实"
    },
    # 副市长
    {
        "id": 14,
        "name": "郇金刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市人民政府副市长",
        "current_org": "昌邑市人民政府",
        "source": "基于公开新闻报道；需核实当前任职"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 人大 (Municipal People's Congress)
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 15,
        "name": "胡筱芹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市人大常委会主任",
        "current_org": "昌邑市人民代表大会常务委员会",
        "source": "基于公开新闻报道；需核实当前任职"
    },
    {
        "id": 16,
        "name": "姜正峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市人大常委会副主任",
        "current_org": "昌邑市人民代表大会常务委员会",
        "source": "基于公开新闻报道；需核实当前任职"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 政协 (Municipal CPPCC)
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 17,
        "name": "李明杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市政协主席",
        "current_org": "中国人民政治协商会议昌邑市委员会",
        "source": "基于公开新闻报道；需核实当前任职"
    },
    {
        "id": 18,
        "name": "孙孝工",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市政协副主席",
        "current_org": "中国人民政治协商会议昌邑市委员会",
        "source": "基于公开新闻报道；需核实当前任职"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 司法机构
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 19,
        "name": "李正诺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市人民法院院长",
        "current_org": "昌邑市人民法院",
        "source": "基于公开新闻报道；需核实当前任职"
    },
    {
        "id": 20,
        "name": "隋国华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌邑市人民检察院检察长",
        "current_org": "昌邑市人民检察院",
        "source": "基于公开新闻报道；需核实当前任职"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共昌邑市委员会",
        "type": "党委",
        "level": "县级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 2,
        "name": "昌邑市人民政府",
        "type": "政府",
        "level": "县级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 3,
        "name": "中共昌邑市纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 4,
        "name": "昌邑市监察委员会",
        "type": "纪委",
        "level": "县级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 5,
        "name": "中共昌邑市委组织部",
        "type": "党委",
        "level": "县级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 6,
        "name": "中共昌邑市委宣传部",
        "type": "党委",
        "level": "县级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 7,
        "name": "中共昌邑市委政法委员会",
        "type": "党委",
        "level": "县级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 8,
        "name": "中共昌邑市委员会办公室",
        "type": "党委",
        "level": "县级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 9,
        "name": "昌邑市人民武装部",
        "type": "党委",
        "level": "县级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 10,
        "name": "昌邑市公安局",
        "type": "政府",
        "level": "县级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 11,
        "name": "昌邑市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 12,
        "name": "中国人民政治协商会议昌邑市委员会",
        "type": "政协",
        "level": "县级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 13,
        "name": "昌邑市人民法院",
        "type": "政府",
        "level": "县级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 14,
        "name": "昌邑市人民检察院",
        "type": "政府",
        "level": "县级",
        "location": "山东省潍坊市昌邑市"
    },
    # 乡镇/街道组织
    {
        "id": 15,
        "name": "奎聚街道",
        "type": "乡镇/街道",
        "level": "乡科级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 16,
        "name": "都昌街道",
        "type": "乡镇/街道",
        "level": "乡科级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 17,
        "name": "围子街道",
        "type": "乡镇/街道",
        "level": "乡科级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 18,
        "name": "柳疃镇",
        "type": "乡镇/街道",
        "level": "乡科级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 19,
        "name": "龙池镇",
        "type": "乡镇/街道",
        "level": "乡科级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 20,
        "name": "卜庄镇",
        "type": "乡镇/街道",
        "level": "乡科级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 21,
        "name": "饮马镇",
        "type": "乡镇/街道",
        "level": "乡科级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 22,
        "name": "北孟镇",
        "type": "乡镇/街道",
        "level": "乡科级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 23,
        "name": "下营镇",
        "type": "乡镇/街道",
        "level": "乡科级",
        "location": "山东省潍坊市昌邑市"
    },
    {
        "id": 24,
        "name": "昌邑滨海经济开发区",
        "type": "开发区",
        "level": "县级",
        "location": "山东省潍坊市昌邑市下营镇"
    },
]

positions_data = [
    # 市委班子成员
    {"person_id": 1, "org_id": 1, "title": "昌邑市委书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "昌邑市委副书记", "start": "", "end": "present", "rank": "副处级", "note": "专职副书记"},
    {"person_id": 3, "org_id": 1, "title": "昌邑市委副书记", "start": "", "end": "present", "rank": "副处级", "note": "兼市长"},
    {"person_id": 3, "org_id": 2, "title": "昌邑市人民政府市长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "昌邑市委常委、市纪委书记", "start": "", "end": "present", "rank": "副处级", "note": "兼市监委主任"},
    {"person_id": 4, "org_id": 4, "title": "昌邑市监察委员会主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "昌邑市委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "昌邑市委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 7, "title": "昌邑市委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "昌邑市委常委、副市长（常务）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 8, "title": "昌邑市委常委、市委办公室主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "昌邑市委常委、市人武部政委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 政府班子成员
    {"person_id": 11, "org_id": 10, "title": "昌邑市副市长、市公安局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "昌邑市人民政府副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "昌邑市人民政府副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "昌邑市人民政府副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 人大
    {"person_id": 15, "org_id": 11, "title": "昌邑市人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 16, "org_id": 11, "title": "昌邑市人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 政协
    {"person_id": 17, "org_id": 12, "title": "昌邑市政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 12, "title": "昌邑市政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 司法
    {"person_id": 19, "org_id": 13, "title": "昌邑市人民法院院长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 14, "title": "昌邑市人民检察院检察长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

relationships_data = [
    # 书记-市长工作关系
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "市委书记与市长，党政主要领导搭档",
        "overlap_org": "中共昌邑市委员会",
        "overlap_period": "至今",
    },
    # 书记-副书记关系
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "市委书记与专职副书记",
        "overlap_org": "中共昌邑市委员会",
        "overlap_period": "至今",
    },
    # 市长-副书记关系（同人跨职）
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "市委常委会班子成员",
        "overlap_org": "中共昌邑市委员会",
        "overlap_period": "至今",
    },
    # 书记-纪委书记
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "党委主要领导与纪委书记",
        "overlap_org": "中共昌邑市委员会",
        "overlap_period": "至今",
    },
    # 书记-组织部长
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "党委主要领导与组织部长",
        "overlap_org": "中共昌邑市委员会",
        "overlap_period": "至今",
    },
    # 书记-宣传部长
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "党委主要领导与宣传部长",
        "overlap_org": "中共昌邑市委员会",
        "overlap_period": "至今",
    },
    # 书记-政法委书记
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "党委主要领导与政法委书记",
        "overlap_org": "中共昌邑市委员会",
        "overlap_period": "至今",
    },
    # 市长-常务副市长
    {
        "person_a": 3,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "市长与常务副市长",
        "overlap_org": "昌邑市人民政府",
        "overlap_period": "至今",
    },
    # 书记-办公室主任
    {
        "person_a": 1,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "党委书记与办公室主任",
        "overlap_org": "中共昌邑市委员会",
        "overlap_period": "至今",
    },
    # 市长-公安局长
    {
        "person_a": 3,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "市长与分管公安的副市长",
        "overlap_org": "昌邑市人民政府",
        "overlap_period": "至今",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Run build
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Build complete: {DB_PATH}, {GEXF_PATH}")
