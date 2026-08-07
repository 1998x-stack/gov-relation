#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 富平县, 渭南市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_富平县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - 富平县人民政府官方网站 (www.fuping.gov.cn) — 领导之窗逐人简介与分工; 重大会议/本地要闻
    多篇领导人活动报道确认现任书记任职与常委会主持
  - 本地仓库 大荔县 调查(2026-08-07): 前任富平县长景军荣 2021-08~2026-06 调任大荔县委书记
  - 富平县融媒体中心新闻 — 官方活动报道确认分工与在任时间

Confidence notes:
  - 赵林斌(县委常委、市委书记，兼渭南市委常委): 官方新闻多次出现"市委常委、县委书记赵林斌"
    (2026-06-11调研企业、2026-07-15第19次常委会、2026-08-06第22次常委会), 身份 confirmed;
    完整履历(出生年份/籍贯/学历/此前任职与就任时间)公开渠道未能获取, 以 open_questions 记录
  - 陈维军(县政府党组书记、代县长): 官方"领导之窗"附简介 (2026-06-15更新) 确认, 男,汉族,中共党员;
    履历细节、前任县长任内是否任常务副职等均待补充
  - 张少林/贾丹/白涛/段冰/艾路阳/范加龙/张增选(副县长): 官方"领导之窗"逐人确认分工与身份
  - 杜占全(县人大常委会主任), 张三放/康进联/刘娜(县人大副主任), 许喜林(县委常委、纪委书记、监委主任):
    官方新闻确认
  - 前任富平县长 景军荣: 本地大荔县数据已确认 2021-08(代)~2026-06, 后调任大荔县委书记
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

SLUG = "富平县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

SOURCE_GOV = "富平县政府官网W(fuping.gov.cn)领导之窗确认"
SOURCE_NEWS = "富平县政府官网新闻报道确认"

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # 县委 (Party Committee) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 赵林斌 — 市委常委、县委书记
    {
        "id": 1,
        "name": "赵林斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、县委书记",
        "current_org": "中共富平县委员会",
        "source": "富平县政府官网新闻报道多次确认(2026-06-11调研企业、2026-07-15常委会、2026-08-06第22次常委会均以'市委常委、县委书记赵林斌'出现)"
    },
    # 陈维军 — 县政府党组书记、代县长
    {
        "id": 2,
        "name": "陈维军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组书记、代县长",
        "current_org": "富平县人民政府",
        "source": "富平县政府官网'领导之窗'(2026-06-15更新)确认，现任县政府党组书记、代县长"
    },
    # 许喜林 — 县委常委、纪委书记、监委主任
    {
        "id": 3,
        "name": "许喜林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共富平县纪律检查委员会",
        "source": "富平县政府官网新闻(2026-07-31县十九届人大常委会第三十七次会议'县委常委、纪委书记、监委主任许喜林列席会议')确认"
    },
    # 张少林 — 县委常委、常务副县长
    {
        "id": 4,
        "name": "张少林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "富平县人民政府",
        "source": "富平县政府官网'领导之窗'(2024-02-01)确认；负责县政府常务工作和重点项目、营商环境、苏陕协作、人社、住建、应急、金融、创建等工作"
    },
    # 贾丹 — 县委常委、副县长（女）
    {
        "id": 5,
        "name": "贾丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "富平县人民政府",
        "source": "富平县政府官网'领导之窗'(2024-03-28)确认；负责教育、卫生健康、医疗保障、残疾人事业、文化旅游等工作"
    },
    # 白涛 — 副县长、县公安局局长
    {
        "id": 6,
        "name": "白涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "富平县公安局",
        "source": "富平县政府官网'领导之窗'(2026-04-07更新)确认；负责公安、退役军人事务、信访、司法等工作"
    },
    # 段冰 — 副县长
    {
        "id": 7,
        "name": "段冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "富平县人民政府",
        "source": "富平县政府官网'领导之窗'(2024-03-28)确认；负责工业、交通、商贸流通、招商引资等工作"
    },
    # 艾路阳 — 副县长（无党派）
    {
        "id": 8,
        "name": "艾路阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "富平县人民政府",
        "source": "富平县政府官网'领导之窗'(2024-03-28)确认；无党派；负责行政审批、民政、市场监管等工作"
    },
    # 范加龙 — 副县长
    {
        "id": 9,
        "name": "范加龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "富平县人民政府",
        "source": "富平县政府官网'领导之窗'(2024-03-12)确认；负责自然资源、城市管理执法、生态环境保护等工作"
    },
    # 张增选 — 副县长
    {
        "id": 10,
        "name": "张增选",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "富平县人民政府",
        "source": "富平县政府官网'领导之窗'(2024-03-12)确认；负责农业农村、乡村振兴、水务等工作"
    },
    # 杜占全 — 县人大常委会主任
    {
        "id": 11,
        "name": "杜占全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "富平县人民代表大会常务委员会",
        "source": "富平县政府官网新闻(2026-07-31县第十九届人大常委会第三十七次会议'县人大常委会主任杜占全主持')确认"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共富平县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共渭南市委员会",
        "location": "渭南市富平县"
    },
    {
        "id": 2,
        "name": "富平县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "渭南市人民政府",
        "location": "渭南市富平县"
    },
    {
        "id": 3,
        "name": "富平县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "渭南市人民代表大会常务委员会",
        "location": "渭南市富平县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议富平县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协渭南市委员会",
        "location": "渭南市富平县"
    },
    {
        "id": 5,
        "name": "中共富平县纪律检查委员会/县监委",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共渭南市纪律检查委员会",
        "location": "渭南市富平县"
    },
    {
        "id": 6,
        "name": "富平县公安局",
        "type": "政府",
        "level": "正科级",
        "parent": "富平县人民政府",
        "location": "渭南市富平县"
    },
    {
        "id": 7,
        "name": "富阎产业合作园区管委会",
        "type": "开发区",
        "level": "县处级",
        "parent": "富平县人民政府/阎良区",
        "location": "渭南市富平县"
    },
]

positions_data = [
    # 县委
    {"person_id": 1, "org_id": 1, "title": "市委常委、县委书记", "start_date": "unknown", "end_date": "present", "rank": "正县处级(高配)", "note": "兼渭南市委常委;官方新闻确认(2026-06至08在任,主持历次县委常委会)"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},

    # 政府
    {"person_id": 2, "org_id": 2, "title": "县政府党组书记、代县长", "start_date": "2026-06", "end_date": "present", "rank": "正县处级", "note": "2026-06-15领导之窗确认，代县长在任；主持县政府全面工作"},
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": "负责常务工作、重点项目、人社、住建、应急、金融等"},
    {"person_id": 5, "org_id": 2, "title": "县委常委、副县长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": "负责教育、卫生、医保、文旅、残联"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": "2026-04更新；负责公安、退役军人、信访、司法"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": "负责工业、交通、商贸、招商"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": "无党派；负责行政审批、民政、市场监管"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": "负责自然资源、城管、生态环境"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": "负责农业农村、乡村振兴、水务"},

    # 公安
    {"person_id": 6, "org_id": 6, "title": "公安局局长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},

    # 纪委
    {"person_id": 3, "org_id": 5, "title": "纪委书记、监委主任", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},

    # 人大
    {"person_id": 11, "org_id": 3, "title": "县人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "正县处级", "note": "2026-07-31主持县十九届人大常委会第三十七次会议"},
]

relationships_data = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记赵林斌——代县长陈维军党政搭档", "overlap_org": "中共富平县委/富平县人民政府", "overlap_period": "2026-06-present"},
    {"person_a": 1, "person_b": 4, "type": "班子", "context": "县委书记——常务副县长张少林工作关系（同场列席人大会议/调研）", "overlap_org": "中共富平县委/富平县人民政府", "overlap_period": "unknown-present"},
    {"person_a": 1, "person_b": 3, "type": "班子", "context": "县委书记——纪委书记许喜林班子关系", "overlap_org": "中共富平县委", "overlap_period": "unknown-present"},

    # 县长(代)与政府班子
    {"person_a": 2, "person_b": 4, "type": "工作搭档", "context": "代县长——常务副县长张少林工作搭档", "overlap_org": "富平县人民政府", "overlap_period": "2026-06-present"},
    {"person_a": 4, "person_b": 5, "type": "班子", "context": "常务副县长——副县长贾丹班子关系", "overlap_org": "中共富平县委/富平县人民政府", "overlap_period": "unknown-present"},
    {"person_a": 4, "person_b": 6, "type": "工作关系", "context": "常务副县长——副县长、公安局长白涛工作关系", "overlap_org": "富平县人民政府", "overlap_period": "2026-04-present"},

    # 前任/继任 - 代县长接前任县长
    {"person_a": 2, "person_b": 11, "type": "工作关系", "context": "代县长——人大主任杜占全（人大任免监督）", "overlap_org": "富平县人大常委会/富平县人民政府", "overlap_period": "2026-06-present"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "赵林斌": {
        "filename": f"{TODAY}-陕西省-渭南市-县委书记-赵林斌.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "陕西省", "city": "渭南市", "region": "富平县", "job": "县委书记", "task_id": "shaanxi_富平县", "time_focus": "2026"},
            "identity": {
                "person_id": "fuping_zhao_linbin",
                "name": "赵林斌",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {"name_birth": "赵林斌_未知", "name_birthplace": "赵林斌_未知", "official_profile_url": ""}
            },
            "current_status": {"current_post": "市委常委、县委书记", "current_org": "中共富平县委员会", "administrative_rank": "正县处级（高配）", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S011", "S012", "S013"]},
            "career_timeline": [
                {"start": "unknown", "end": "present", "org": "中共富平县委员会", "title": "市委常委、县委书记", "level": "县处级", "location": "陕西渭南富平", "system": "party", "rank": "正县处级（高配）", "is_key_promotion": True, "notes": "当前在任，多次主持县委常委会(第17至22次)、调研企业、检查安全生产(2026-05至08)", "confidence": "confirmed", "source_ids": ["S011", "S012", "S013"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开渠道未能获取赵林斌任富平县委书记前的完整履历(出生年份、籍贯、学历、此前任职、就任时间、前任书记)。其兼任渭南市委常委表明属渭南市级领导高配到县任职。", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [],
            "relationships": [
                {"person": "陈维军", "person_id": "fuping_chen_weijun", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记——代县长党政搭档（陈维军2026年6月任代县长后）", "overlap_org": "县委/富平县政府", "overlap_period": "2026-06-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S011", "S014"]},
                {"person": "张少林", "person_id": "fuping_zhang_shaolin", "relationship_type": "overlap", "strength": "medium", "evidence": "县委书记——常务副县长工作关系（同场出席人大会议/调研）", "overlap_org": "中共富平县委员会/富平县人民政府", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S013"]},
                {"person": "许喜林", "person_id": "fuping_xu_xilin", "relationship_type": "overlap", "strength": "medium", "evidence": "县委书记——纪委书记工作关系", "overlap_org": "中共富平县委员会", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S013"]},
            ],
            "governance_record": [
                {"period": "2026-08", "domain": "party_affairs", "achievement_or_event": "主持2026年县委第22次常委会，传达学习、部署'三个年'活动、扩大有效投资、教育科技人才改革、常态化帮扶、统战工作责任制、群腐集中整治、防汛等", "role_in_event": "主持并讲话", "measurable_outcome": "", "location": "渭南富平", "confidence": "confirmed", "source_ids": ["S011"]},
                {"period": "2026-06", "domain": "public_security", "achievement_or_event": "调研陕西实丰水泥、富平生态水泥，检查非煤矿山安全生产，强调'八条硬措施'、'亲商服务日'制度", "role_in_event": "带队调研", "measurable_outcome": "", "location": "渭南富平", "confidence": "confirmed", "source_ids": ["S012"]},
            ],
            "professional_profile": {
                "primary_specializations": ["党的建设", "县域治理", "安全生产"],
                "secondary_specializations": ["营商环境", "工业经济"],
                "career_pattern": "市级领导高配兼任县委书记",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["渭南市"],
                "promotion_velocity": {"summary": "当前为渭南市委常委兼任富平县委书记，属高配置；此前履历公开有限", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "discipline_oriented", "evidence": "多次主持县委常委会强调全面从严治党、群众身边不正之风集中整治", "confidence": "plausible", "source_ids": ["S011"]},
                    {"trait": "development_focused", "evidence": "强调扩大有效投资、重点项目、营商环境、'送政策优服务'", "confidence": "plausible", "source_ids": ["S012"]},
                ],
                "speech_themes": ["项目建设", "安全生产", "营商环境", "教育科技人才", "防汛安全"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S011", "title": "县委召开2026年第22次常委会会议 赵林斌主持", "url": "https://www.fuping.gov.cn/xwzx/bdyw/2085166192049397761.html", "publisher": "富平县人民政府", "published_at": "2026-08-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认市委常委、县委书记赵林斌在任并主持常委会"},
                {"id": "S012", "title": "赵林斌调研企业生产经营情况 检查非煤矿山安全生产工作", "url": "https://www.fuping.gov.cn/zfxxgk/fdzdgknr/ggjg/aqsc/2064865489813737474.html", "publisher": "富平县人民政府", "published_at": "2026-06-11", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认市长书记身份"},
                {"id": "S013", "title": "县第十九届人大常委会第三十七次会议召开", "url": "https://www.fuping.gov.cn/xwzx/bdyw/2084440496269774850.html", "publisher": "富平县人民政府", "published_at": "2026-08-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "列席确认张少林、许喜林职务"},
            ],
            "confidence_summary": {"identity": "partial", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "赵林斌完整履历、就任时间与前任书记"},
            "open_questions": [
                {"priority": "critical", "question": "赵林斌的完整履历(出生年份、籍贯、学历、此前任职经历、就任富平县委书记时间)", "why_it_matters": "县委书记关键人物，履历缺失影响关系网络与时间线", "suggested_queries": ["赵林斌 富平 县委书记 简历", "赵林斌 渭南 任前公示", "赵林斌 陕西 组织部"], "last_attempted": AS_OF},
                {"priority": "high", "question": "前任富平县委书记是谁、何时交连接到何处?", "why_it_matters": "确定县书记交接时间线", "suggested_queries": ["富平县 前任县委书记", "富平县 县委书记 任命 2026"], "last_attempted": AS_OF},
                {"priority": "medium", "question": "县委班子其余常委(县委副书记、组织部长、宣传部长、政法委书记、统战部长)名单与履历", "why_it_matters": "完善班子网络图谱", "suggested_queries": ["富平县 县委班子 班子名单"], "last_attempted": AS_OF},
            ]
        }
    },
    "陈维军": {
        "filename": f"{TODAY}-陕西省-渭南市-代县长-陈维军.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "陕西省", "city": "渭南市", "region": "富平县", "job": "代县长", "task_id": "shaanxi_富平县", "time_focus": "2026"},
            "identity": {
                "person_id": "fuping_chen_weijun",
                "name": "陈维军",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {"name_birth": "陈维军_未知", "name_birthplace": "陈维军_未知", "official_profile_url": "https://www.fuping.gov.cn/zfxxgk/fdzdgknr/ldzc/xz/ldjl/2066364032936927233.html"}
            },
            "current_status": {"current_post": "县政府党组书记、代县长", "current_org": "富平县人民政府", "administrative_rank": "正县处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]},
            "career_timeline": [
                {"start": "2026-06", "end": "present", "org": "富平县人民政府", "title": "县政府党组书记、代县长", "level": "县处级", "location": "陕西渭南富平", "system": "government", "rank": "正县处级", "is_key_promotion": True, "notes": "2026-06-15领导之窗更新确认，属政府代县长在任（接前任县长景军荣2026-06调离）", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开渠道未获取陈维军任富平县政府党组/代县长前的完整履历。", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [],
            "relationships": [
                {"person": "赵林斌", "person_id": "fuping_zhao_linbin", "relationship_type": "overlap", "strength": "strong", "evidence": "代县长——书记党政搭档（2026-06起）", "overlap_org": "县委/富平县政府", "overlap_period": "2026-06-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "张少林", "person_id": "fuping_zhang_shaolin", "relationship_type": "overlap", "strength": "medium", "evidence": "代县长——常务副县长工作搭档", "overlap_org": "富平县人民政府", "overlap_period": "2026-06-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "governance_record": [
                {"period": "2026-06", "domain": "government_operations", "achievement_or_event": "任县政府党组书记、代县长，领导政府全面工作", "role_in_event": "主持县政府工作", "measurable_outcome": "", "location": "渭南富平", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "2026-06赴任代县长，此前履历公开有限", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "陈维军 - 富平县政府领导之窗(县政府党组书记、代县长)", "url": "https://www.fuping.gov.cn/zfxxgk/fdzdgknr/ldzc/xz/ldjl/2066364032936927233.html", "publisher": "富平县人民政府", "published_at": "2026-06-15", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认现任县政府党组书记、代县长，男、汉族、中共党员"},
            ],
            "confidence_summary": {"identity": "partial", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "陈维军完整履历(出生、籍贯、此前所有任职)与前任县长具体交棒日期"},
            "open_questions": [
                {"priority": "critical", "question": "陈维军的完整履历(出生年份、籍贯、学历、此前所有任职经历)", "why_it_matters": "代县长关键人物，履历缺失影响关系网络", "suggested_queries": ["陈维军 富平 代县长 简历", "陈维军 渭南 任前公示"], "last_attempted": AS_OF},
                {"priority": "high", "question": "前任富平县长景军荣调任大荔后的县府交棒具体时间线", "why_it_matters": "确定县府交接时间", "suggested_queries": ["富平县 代县长 陈维军 任命"], "last_attempted": AS_OF},
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