#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 合阳县, 渭南市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_合阳县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - 合阳县人民政府官方网站 (www.heyang.gov.cn) — 领导之窗逐人简介, 新闻中心/领导活动多篇新闻报道
  - 合阳县融媒体中心(合融媒)新闻 — 官方活动报道确认现任领导分工与在任时间
  - 渭南市/陕西省媒体 — 背景

Confidence notes:
  - 赵超（县委书记）: 官方新闻多次出现"县委书记赵超"(2026-05至08), 身份 confirmed; 完整履历(出生年份/籍贯/此前任职)公开渠道未能获取, 以 open_questions 记录
  - 亢鹏（县委副书记、县长）: 官方"领导之窗"附完整简历, 男,汉族,1976年11月生,在职研究生; 历任财政局局长、管委会副主任、党群工作部部长、县委副书记/政法委书记/镇党委书记; 2025年9月任现职(县长)
  - 王改(常务副县长)、许涛、李小锋、高永斌、井赵斌、杨红、罗莉、赵哲、温晓林: 官方"领导之窗"逐官方确认简历
  - 段武学(县委副书记)、赵乐(县委常委、宣传部部长): 官方新闻确认
  - 人大常委会主任王江平, 法院院长郝翎, 检察院检察长李翔: 官方新闻确认
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.abspath(os.path.join(BASE, "..", "..", "..")))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "合阳县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

SOURCE_GOV = "合阳县政府官网(www.heyang.gov.cn)领导之窗确认"

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # 县委 (Party Committee) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 赵超 — 县委书记
    {
        "id": 1,
        "name": "赵超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共合阳县委员会",
        "source": f"合阳县政府官网新闻报道多次确认(2026年5-8月多次报道'县委书记赵超'主持县委常委会、慰问等)"
    },
    # 亢鹏 — 县委副书记、县长
    {
        "id": 2,
        "name": "亢鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "合阳县人民政府",
        "source": f"合阳县政府官网'领导之窗'确认，附完整简历;2025年9月任现职"
    },
    # 段武学 — 县委副书记
    {
        "id": 3,
        "name": "段武学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共合阳县委员会",
        "source": "合阳县政府官网领导活动新闻(2026-02-03'县委副书记段武学走访慰问退休老干部')确认"
    },
    # 王改 — 县委常委、县政府党组副书记、常务副县长
    {
        "id": 4,
        "name": "王改",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年8月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府党组副书记、常务副县长",
        "current_org": "合阳县人民政府",
        "source": f"合阳县政府官网'领导之窗'确认，2023年6月任现职"
    },
    # 许涛 — 县委常委、副县长
    {
        "id": 5,
        "name": "许涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年4月",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "合阳县人民政府",
        "source": f"合阳县政府官网'领导之窗'确认，2023年9月任现职"
    },
    # 李小锋 — 县委常委、统战部部长，县政府党组成员，县政协党组副书记
    {
        "id": 6,
        "name": "李小锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长，县政府党组成员，县政协党组副书记",
        "current_org": "中共合阳县委统战部",
        "source": "合阳县政府官网'领导之窗'及新闻(2026-07-26夏日送清凉同场出席)确认"
    },
    # 赵乐 — 县委常委、宣传部部长
    {
        "id": 7,
        "name": "赵乐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共合阳县委宣传部",
        "source": "合阳县政府官网领导活动新闻(2026-03-04督导城市文明建设)确认"
    },
    # 高永斌 — 副县长、公安局局长、县委政法委第一副书记
    {
        "id": 8,
        "name": "高永斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "陕西澄城",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "1992年7月",
        "current_post": "副县长、公安局局长，县委政法委第一副书记（兼）",
        "current_org": "合阳县公安局",
        "source": f"合阳县政府官网'领导之窗'确认，曾任澄城县公安局党委副书记、政委(跨县公安干部)；2023年10月任现职"
    },
    # 井赵斌 — 副县长(党外, 九三学社)
    {
        "id": 9,
        "name": "井赵斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "",
        "education": "农学博士、园艺学博士后",
        "party_join": "九三学社社员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "合阳县人民政府",
        "source": f"合阳县政府官网'领导之窗'确认，2021年9月任现职(学院/研究院学术出身)"
    },
    # 罗莉 — 副县长
    {
        "id": 10,
        "name": "罗莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年9月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "合阳县人民政府",
        "source": f"合阳县政府官网'领导之窗'确认，2023年10月任现职"
    },
    # 赵哲 — 副县长
    {
        "id": 11,
        "name": "赵哲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年1月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "合阳县人民政府",
        "source": f"合阳县政府官网'领导之窗'确认，2025年5月任现职"
    },
    # 温晓林 — 副县长(新任)
    {
        "id": 12,
        "name": "温晓林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "合阳县人民政府",
        "source": f"合阳县政府官网'领导之窗'确认，2026年5月任现职(新任)"
    },
    # 王江平 — 人大常委会主任
    {
        "id": 13,
        "name": "王江平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "合阳县人民代表大会常务委员会",
        "source": "合阳县政府官网新闻(2026-08-04县十九届人大常委会第三十三次会议、2026-02-12走访慰问)确认"
    }
]

organizations_data = [
    {
        "id": 1,
        "name": "中共合阳县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共渭南市委员会",
        "location": "渭南市合阳县"
    },
    {
        "id": 2,
        "name": "合阳县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "渭南市人民政府",
        "location": "渭南市合阳县"
    },
    {
        "id": 3,
        "name": "合阳县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "渭南市人民代表大会常务委员会",
        "location": "渭南市合阳县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议合阳县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协渭南市委员会",
        "location": "渭南市合阳县"
    },
    {
        "id": 5,
        "name": "合阳县公安局",
        "type": "政府",
        "level": "县处级",
        "parent": "合阳县人民政府",
        "location": "渭南市合阳县"
    },
    {
        "id": 6,
        "name": "中共合阳县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共合阳县委员会",
        "location": "渭南市合阳县"
    },
    {
        "id": 7,
        "name": "中共合阳县委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共合阳县委员会",
        "location": "渭南市合阳县"
    },
    {
        "id": 8,
        "name": "合阳县人民代表大会常务委员会办公室",
        "type": "人大",
        "level": "县处级",
        "parent": "合阳县人民代表大会常务委员会",
        "location": "渭南市合阳县"
    },
]

positions_data = [
    # 县委
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "official news confirmed (2026-05 to 08)"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2025-09", "end_date": "present", "rank": "正处级", "note": "县委副书记、县长，2025年9月任现职"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "official via 2026-02 news"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "2023-08", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "official via 2026-03 news"},
    {"person_id": 8, "org_id": 1, "title": "县政府党组成员、副县长、县委政法委第一副书记（兼）", "start_date": "2023-10", "end_date": "present", "rank": "副处级", "note": ""},

    # 政府
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2025-09", "end_date": "present", "rank": "正处级", "note": "主持县政府全面工作，分管财政局、审计局"},
    {"person_id": 4, "org_id": 2, "title": "县委常委、县政府党组副书记、常务副县长", "start_date": "2023-06", "end_date": "present", "rank": "副处级", "note": "主持县政府日常工作"},
    {"person_id": 5, "org_id": 2, "title": "县委常委、副县长", "start_date": "2023-09", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "2023-10", "end_date": "present", "rank": "副处级", "note": "分管公安、司法、退役军人"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "2021-09", "end_date": "present", "rank": "副处级", "note": "分管民政、水务、文旅、行政审批、洽川管理"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "2023-10", "end_date": "present", "rank": "副处级", "note": "分管教育、卫生、医保、商务"},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "2025-05", "end_date": "present", "rank": "副处级", "note": "分管工信、交通、经开区"},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "2026-05", "end_date": "present", "rank": "副处级", "note": "新任"},

    # 公安局
    {"person_id": 8, "org_id": 5, "title": "公安局党委书记、局长", "start_date": "2023-10", "end_date": "present", "rank": "副处级", "note": ""},

    # 宣传部
    {"person_id": 7, "org_id": 6, "title": "宣传部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},

    # 统战部
    {"person_id": 6, "org_id": 7, "title": "统战部部长", "start_date": "2023-08", "end_date": "present", "rank": "副处级", "note": "兼县政府党组成员、县政协党组副书记"},

    # 人大
    {"person_id": 13, "org_id": 3, "title": "县人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "official via 2026-08/02 news"},
]

relationships_data = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记赵超——县长亢鹏党政搭档", "overlap_org": "中共合阳县委/合阳县人民政府", "overlap_period": "2025-09-present"},
    {"person_a": 1, "person_b": 3, "type": "班子", "context": "县委书记——县委副书记段武学班子关系", "overlap_org": "中共合阳县委", "overlap_period": "unknown-present"},

    # 书记与县政府班子(2026-07-26 夏日送清凉同场出席)
    {"person_a": 1, "person_b": 4, "type": "班子", "context": "县委书记——常务副县长王改工作关系", "overlap_org": "中共合阳县委/合阳县人民政府", "overlap_period": "unknown-present"},
    {"person_a": 1, "person_b": 6, "type": "班子", "context": "县委书记——统战部部长李小锋工作关系(同场出席)", "overlap_org": "中共合阳县委", "overlap_period": "unknown-present"},
    {"person_a": 1, "person_b": 8, "type": "班子", "context": "县委书记——副县长、公安局长高永斌工作关系(同场出席)", "overlap_org": "中共合阳县委/合阳县人民政府", "overlap_period": "unknown-present"},
    {"person_a": 1, "person_b": 10, "type": "班子", "context": "县委书记——副县长罗莉工作关系(同场出席)", "overlap_org": "中共合阳县委/合阳县人民政府", "overlap_period": "unknown-present"},

    # 县长与政府班子
    {"person_a": 2, "person_b": 4, "type": "工作搭档", "context": "县长——常务副县长王改工作搭档", "overlap_org": "合阳县人民政府", "overlap_period": "2025-09-present"},
    {"person_a": 2, "person_b": 8, "type": "工作关系", "context": "县长——副县长、公安局长高永斌工作关系", "overlap_org": "合阳县人民政府", "overlap_period": "2025-09-present"},
    {"person_a": 2, "person_b": 5, "type": "工作关系", "context": "县长——副县长许涛工作关系", "overlap_org": "合阳县人民政府", "overlap_period": "2025-09-present"},

    # 县委副书记与县长
    {"person_a": 3, "person_b": 2, "type": "班子", "context": "县委副书记段武学与县长亢鹏班子关系", "overlap_org": "中共合阳县委", "overlap_period": "unknown-present"},

    # 高永斌 — 跨县(澄城→合阳)公安交流
    {"person_a": 8, "person_b": 1, "type": "班子成员", "context": "副县长、公安局长与县委书记工作关系", "overlap_org": "中共合阳县委", "overlap_period": "unknown-present"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "赵超": {
        "filename": f"{TODAY}-陕西省-渭南市-县委书记-赵超.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "陕西省", "city": "渭南市", "region": "合阳县", "job": "县委书记", "task_id": "shaanxi_合阳县", "time_focus": "2026"},
            "identity": {
                "person_id": "heyang_zhao_chao",
                "name": "赵超",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {"name_birth": "赵超_未知", "name_birthplace": "赵超_未知", "official_profile_url": ""}
            },
            "current_status": {"current_post": "县委书记", "current_org": "中共合阳县委员会", "administrative_rank": "正处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S011", "S012", "S013"]},
            "career_timeline": [
                {"start": "unknown", "end": "present", "org": "中共合阳县委员会", "title": "县委书记", "level": "县处级", "location": "陕西渭南合阳", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "当前在任，多次主持县委常委会(第十八次、第十九次)、开展慰问调研(2026-05至08)", "confidence": "confirmed", "source_ids": ["S011", "S012", "S013"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开渠道未能获取赵超任合阳县委书记前的完整履历(出生年份、籍贯、学历、此前任职、就任时间、前任书记)。", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [],
            "relationships": [
                {"person": "亢鹏", "person_id": "heyang_kang_peng", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记——县长党政搭档(亢鹏2025年9月任县长后)", "overlap_org": "中共合阳县委/合阳县人民政府", "overlap_period": "2025-09-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S011", "S012"]},
                {"person": "段武学", "person_id": "heyang_duan_wuxue", "relationship_type": "overlap", "strength": "medium", "evidence": "县委书记——县委副书记工作关系", "overlap_org": "中共合阳县委", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S013"]},
                {"person": "李小锋", "person_id": "heyang_li_xiaofeng", "relationship_type": "overlap", "strength": "medium", "evidence": "县委书记——统战部长(2026-07-26夏日送清凉同场出席)", "overlap_org": "中共合阳县委", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S014"]},
                {"person": "高永斌", "person_id": "heyang_gao_yongbin", "relationship_type": "overlap", "strength": "medium", "evidence": "县委书记——副县长、公安局长(同场出席)", "overlap_org": "中共合阳县委/合阳县人民政府", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S014"]},
                {"person": "罗莉", "person_id": "heyang_luo_li", "relationship_type": "overlap", "strength": "medium", "evidence": "县委书记——副县长罗莉(同场出席)", "overlap_org": "中共合阳县委/合阳县人民政府", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S014"]},
            ],
            "governance_record": [
                {"period": "2026-08", "domain": "party_affairs", "achievement_or_event": "主持2026年县委第十九次常委会会议,传达省委全会、部署防汛、教育、侨务、党风廉政(群众身边不正之风集中整治)、双极带动/三区协同战略", "role_in_event": "主持会议", "measurable_outcome": "", "location": "渭南合阳", "confidence": "confirmed", "source_ids": ["S012"]},
                {"period": "2026-07", "domain": "public_security", "achievement_or_event": "开展夏日送清凉慰问活动,督导省十八运会保障与内涝治理项目建设", "role_in_event": "带队开展", "measurable_outcome": "", "location": "渭南合阳", "confidence": "confirmed", "source_ids": ["S014"]},
                {"period": "2026-07", "domain": "party_affairs", "achievement_or_event": "主持县委理论学习中心组第十一次会议和县委第十八次常委会会议", "role_in_event": "主持会议", "measurable_outcome": "", "location": "渭南合阳", "confidence": "confirmed", "source_ids": ["S011"]},
                {"period": "2026-07", "domain": "social_service", "achievement_or_event": "八一前夕走访慰问退役军人", "role_in_event": "慰问", "measurable_outcome": "", "location": "渭南合阳", "confidence": "confirmed", "source_ids": ["S013"]},
            ],
            "professional_profile": {
                "primary_specializations": ["党的建设", "县域治理"],
                "secondary_specializations": ["基层党建", "党风廉政"],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "当前确认职务为合阳县委书记,此前履历公开有限", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "discipline_oriented", "evidence": "多次主持县委常委会强调全面从严治党、群众身边不正之风和腐败问题集中整治", "confidence": "plausible", "source_ids": ["S012", "S011"]},
                    {"trait": "development_focused", "evidence": "强调'两县两区'建设目标、区域发展战略、项目建设与产业发展", "confidence": "plausible", "source_ids": ["S012"]},
                ],
                "speech_themes": ["党的建设", "教育", "防汛安全", "党风廉政", "区域发展"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S011", "title": "赵超主持召开2026年县委理论学习中心组第十一次和县委第十八次常委会", "url": "https://www.heyang.gov.cn/", "publisher": "合阳县人民政府", "published_at": "2026-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认县委书记赵超在职,主持常委会"},
                {"id": "S012", "title": "赵超主持召开2026年县委第十九次常委会会议", "url": "https://www.heyang.gov.cn/xwzx/bdyw/2084798054518415362.html", "publisher": "合阳县人民政府", "published_at": "2026-08-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认赵超为县委书记,部署教育、侨务、防汛、党风廉政"},
                {"id": "S013", "title": "赵超八一节前慰问退役军人", "url": "https://www.heyang.gov.cn/", "publisher": "合阳县人民政府", "published_at": "2026-07-28", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认赵超为县委书记"},
                {"id": "S014", "title": "赵超开展'夏日送清凉'慰问活动 看望省十八运赛事保障人员", "url": "https://www.heyang.gov.cn/zfxxgk/fdzdgknr/ldhd/2082265820590919681.html", "publisher": "合阳县人民政府", "published_at": "2026-07-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认赵超,以及李小锋、高永武、罗莉、刘春合同场出席"},
            ],
            "confidence_summary": {"identity": "partial", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "赵超任合县委书记前的完整履历及其就任时间、前任书记"},
            "open_questions": [
                {"priority": "critical", "question": "赵超的完整履历(出生年份、籍贯、学历、此前所有任职经历)", "why_it_matters": "县委书记关键人物,履历缺失严重影响关系网络与任职时间线", "suggested_queries": ["赵超 合阳 县委书记 简历", "赵超 渭南 任前公示", "赵超 陕西 组织部"], "last_attempted": AS_OF},
                {"priority": "high", "question": "赵超何时就任合阳县委书记?前任书记是谁且去向何处?", "whyit_matters": "确定交接时间与渭南干部流动脉络", "suggested_queries": ["合阳县 前任县委书记", "合阳县 县委书记 任命 2025"], "last_attempted": AS_OF},
                {"priority": "medium", "question": "县委班子其余常委(纪委书记、组织部长、政法委书记等)名单与履历", "why_it_matters": "完善班子网络图谱", "suggested_queries": ["合阳县委 班子 纪委 组织"], "last_attempted": AS_OF},
            ]
        }
    },
    "亢鹏": {
        "filename": f"{TODAY}-陕西省-渭南市-县长-亢鹏.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "陕西省", "city": "渭南市", "region": "合阳县", "job": "县长", "task_id": "shaanxi_合阳县", "time_focus": "2026"},
            "identity": {
                "person_id": "heyang_kang_peng",
                "name": "亢鹏",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1976年11月",
                "birthplace": "",
                "native_place": "",
                "education": [{"period": "", "institution": "", "major": "", "degree": "在职研究生", "study_type": "part_time", "source_ids": ["S001"]}],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {"name_birth": "亢鹏_1976年11月", "name_birthplace": "亢鹏_未知", "official_profile_url": "https://www.heyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xz/1636201381595480066.html"}
            },
            "current_status": {"current_post": "县委副书记、县长", "current_org": "合阳县人民政府", "administrative_rank": "正处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002"]},
            "career_timeline": [
                {"start": "unknown", "end": "unknown", "org": "财政局", "title": "财政局局长", "level": "县处级", "location": "渭南合阳", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "管委会", "title": "管委会副主任", "level": "县处级", "location": "渭南", "system": "development_zone", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "党群工作部", "title": "党群工作部部长", "level": "县处级", "location": "渭南", "system": "other", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "中共合阳县委", "title": "县委副书记、政法委书记", "level": "县处级", "location": "渭南合阳", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "某镇", "title": "镇党委书记", "level": "县处级", "location": "渭南", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2025-09", "end": "present", "org": "合阳县人民政府", "title": "县委副书记、县长", "level": "县处级", "location": "陕西渭南合阳", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2025年9月任现职,领导县政府全面工作,分管财政局、审计局", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            ],
            "organizations": [],
            "relationships": [
                {"person": "赵超", "person_id": "heyang_zhao_chao", "relationship_type": "overlap", "strength": "strong", "evidence": "县长——县委书记党政搭档", "overlap_org": "中共合阳县委/合阳县人民政府", "overlap_period": "2025-09-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
                {"person": "王改", "person_id": "heyang_wang_gai", "relationship_type": "overlap", "strength": "strong", "evidence": "县长——常务副县长工作搭档", "overlap_org": "合阳县人民政府", "overlap_period": "2025-09-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"person": "高永斌", "person_id": "heyang_gao_yongbin", "relationship_type": "overlap", "strength": "medium", "evidence": "县长——副县长、公安局长工作关系", "overlap_org": "合阳县人民政府", "overlap_period": "2025-09-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
            ],
            "governance_record": [
                {"period": "2026-08", "domain": "public_security", "achievement_or_event": "带队督导检查沿黄公路合阳段水毁塌陷抢修,部署汛期道路抢通与安全管控", "role_in_event": "带队督导", "measurable_outcome": "", "location": "渭南合阳", "confidence": "confirmed", "source_ids": ["S002"]},
                {"period": "2026-06", "domain": "public_security", "achievement_or_event": "带队督导检查震后重点领域安全隐患", "role_in_event": "带队督导", "measurable_outcome": "", "location": "渭南合阳", "confidence": "confirmed", "source_ids": ["S003"]},
                {"period": "2026-06", "domain": "education", "achievement_or_event": "深入合阳中学督导2026年高考考前筹备工作", "role_in_event": "督导", "measurable_outcome": "", "location": "渭南合阳", "confidence": "confirmed", "source_ids": ["S003"]},
                {"period": "2026-05", "domain": "government_operations", "achievement_or_event": "主持召开县政府第五次常务会议", "role_in_event": "主持会议", "measurable_outcome": "", "location": "渭南合阳", "confidence": "confirmed", "source_ids": ["S003"]},
            ],
            "professional_profile": {
                "primary_specializations": ["财政", "区域治理", "政法"],
                "secondary_specializations": ["防汛", "产业发展"],
                "career_pattern": "地方历练型(财政局长→开发区→乡镇→政法→县长)",
                "systems_experience": ["government", "party", "development_zone", "discipline"],
                "geographic_pattern": ["合阳本地深耕", "渭南"],
                "promotion_velocity": {"summary": "2025年9月由县委副书记/政法委书记/镇党委书记接任县长,履历覆盖财政、政法、乡镇基层", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "down_to_earth_oversight", "evidence": "多次带队赴一线督导检查防汛、震后安全等具体工作", "confidence": "plausible", "source_ids": ["S002", "S003"]},
                ],
                "speech_themes": ["防汛防灾", "安全生产", "民生保障", "县域经济"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "亢鹏 - 合阳县政府领导之窗(县长)", "url": "https://www.heyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xz/1636201381595480066.html", "publisher": "合阳县人民政府", "published_at": "2026-01-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "完整简历:1976年11月生,历任财政局长/管委会副主任/党群工作部长/县委副书记兼政法委书记/镇书记,2025年9月任县长"},
                {"id": "S002", "title": "亢鹏督导检查沿黄公路合阳段水毁塌陷抢修工作", "url": "https://www.heyang.gov.cn/xwzx/bdyw/2085157179769364482.html", "publisher": "合阳县人民政府", "published_at": "2026-08-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认'县长亢鹏'身份及防汛履职"},
                {"id": "S003", "title": "合阳县领导活动(亢鹏各篇)", "url": "https://www.heyang.gov.cn/zfxxgk/fdzdgknr/ldhd/1.html", "publisher": "合阳县人民政府", "published_at": "2026", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认县长主持政府常务会、高考督导、震后安全等履职记录"},
            ],
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "medium", "relationship_confidence": "medium", "biggest_gap": "亢鹏各段任职的具体起止时间与就任背景(可通过任前公示等补充)"},
            "open_questions": [
                {"priority": "medium", "question": "亢鹏各段任职(财政局局长、管委会副主任等)的具体起止时间与籍贯、毕业院校", "why_it_matters": "丰富县长履历时间线,支撑更精确的关系网络", "suggested_queries": ["亢鹏 合阳 简历 任职", "亢鹏 渭南 任前公示"], "last_attempted": AS_OF},
            ]
        }
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def write_person_json(data: dict, filename: str) -> Path:
    path = STAGING_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")
    return path

def main():
    print(f"Building network for {SLUG}...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()

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
    print()

    print("Writing person JSON files...")
    for key, entry in PERSON_JSON_TEMPLATE.items():
        write_person_json(entry["data"], entry["filename"])

    print()
    print("=" * 60)
    print(f"Build complete for {SLUG}")
    print(f"  {len(persons_data)} persons")
    print(f"  {len(organizations_data)} organizations")
    print(f"  {len(positions_data)} positions")
    print(f"  {len(relationships_data)} relationships")
    print(f"  {len(PERSON_JSON_TEMPLATE)} person JSONs")
    print("=" * 60)

if __name__ == "__main__":
    main()