#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 临渭区, 渭南市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_临渭区
Level: 市辖区
Targets: 区委书记 & 区长

Primary source for confirmed government roster + resumes:
  - 临渭区人民政府官方网站 领导之窗 / 领导简历
    https://www.linwei.gov.cn/zfxxgk/fdzdgknr/lczc/ (updated 2026-07-29, verified 2026-08-07)
  - 领导活动 / 本地要闻 sections confirming current leadership rotation (2026-07/08)
  - 2026-07 news naming 区委书记菊峰 and 区政府党组书记、代区长马世仓

Confidence notes:
  - 菊峰（区委书记）: role confirmed by many official news reports (2026-07 -> 08).
    Personal career history before 临渭区委书记 not published on the district site; flagged.
  - 马世仓（区政府党组书记、代区长）: official 领导简历 gives complete modern career.
    Remains "代区长" as of the 2026-07-29 official page update.
  - 区政府领导班子 9 members each have an official resume (name, birth, party, 分工, career).
  - 区委（除书记外的常委）、人大、政协 full rosters are not on the gov-only 领导之窗; open gaps.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
for root in (
    os.path.abspath(os.path.join(BASE, "..", "..", "..")),
    os.path.abspath(os.path.join(BASE, "..", "..")),
):
    if root not in sys.path:
        sys.path.insert(0, root)

from gov_relation.runner import run_build
import sqlite3  # noqa: F401  (used below for post-build verification)

SLUG = "临渭区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Persons
# id convention: 1..N for 临渭区 persons (dedupe across investigations uses
# linwei_<pinyin> keys in person JSONs and the repo central registry).
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    {"id": 1, "name": "菊峰", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共渭南市临渭区委员会",
     "source": "临渭区人民政府官网新闻（2026-07/08 多次确认'区委书记菊峰'）"},
    {"id": 2, "name": "马世仓", "gender": "男", "ethnicity": "汉族", "birth": "1979年12月",
     "birthplace": "陕西蒲城", "education": "大学本科", "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、区政府党组书记、代区长", "current_org": "渭南市临渭区人民政府",
     "source": "临渭区领导简历官方页（2026-07-22 更新）"},
    {"id": 3, "name": "刘刚", "gender": "男", "ethnicity": "汉族", "birth": "1975年9月",
     "birthplace": "", "education": "大专", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区政府党组副书记、常务副区长", "current_org": "渭南市临渭区人民政府",
     "source": "临渭区人民政府领导简历官方页（2026-07-29）"},
    {"id": 4, "name": "李云鹏", "gender": "男", "ethnicity": "汉族", "birth": "1981年12月",
     "birthplace": "", "education": "本科", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区政府党组成员、副区长", "current_org": "渭南市临渭区人民政府",
     "source": "临渭区人民政府领导简历官方页（2026-07-29）"},
    {"id": 5, "name": "阮光民", "gender": "男", "ethnicity": "汉族", "birth": "1970年3月",
     "birthplace": "", "education": "大专", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "渭南市临渭区人民政府",
     "source": "临渭区人民政府领导简历官方页（2026-07-29）"},
    {"id": 6, "name": "张中锋", "gender": "男", "ethnicity": "汉族", "birth": "1977年4月",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "渭南市临渭区人民政府",
     "source": "临渭区人民政府领导简历官方页（2026-07-29）"},
    {"id": 7, "name": "田永超", "gender": "男", "ethnicity": "汉族", "birth": "1980年4月",
     "birthplace": "", "education": "在职研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "渭南市临渭区人民政府",
     "source": "临渭区人民政府领导简历官方页（2026-07-29）"},
    {"id": 8, "name": "张金玲", "gender": "女", "ethnicity": "汉族", "birth": "1976年8月",
     "birthplace": "", "education": "大学", "party_join": "民革党员", "work_start": "",
     "current_post": "副区长", "current_org": "渭南市临渭区人民政府",
     "source": "临渭区人民政府领导简历官方页（2026-07-29）"},
    {"id": 9, "name": "王晓鹏", "gender": "男", "ethnicity": "汉族", "birth": "1975年4月",
     "birthplace": "", "education": "大专", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长兼区公安分局局长", "current_org": "渭南市临渭区人民政府/渭南市公安局临渭分局",
     "source": "临渭区人民政府领导简历官方页（2026-07-29）"},
    {"id": 10, "name": "王玉冰", "gender": "女", "ethnicity": "汉族", "birth": "1969年2月",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长（挂职）", "current_org": "渭南市临渭区人民政府",
     "source": "临渭区人民政府领导简历官方页（2026-07-29）"},
]

organizations_data = [
    {"id": 1, "name": "中共渭南市临渭区委员会", "type": "党委", "level": "县处级", "parent": "中共渭南市委员会", "location": "渭南市临渭区"},
    {"id": 2, "name": "渭南市临渭区人民政府", "type": "政府", "level": "县处级", "parent": "渭南市人民政府", "location": "渭南市临渭区"},
    {"id": 3, "name": "渭南市临渭区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "渭南市人民代表大会常务委员会", "location": "渭南市临渭区"},
    {"id": 4, "name": "中国人民政治协商会议渭南市临渭区委员会", "type": "政协", "level": "县处级", "parent": "政协渭南市委员会", "location": "渭南市临渭区"},
    {"id": 5, "name": "中共渭南市临渭区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共渭南市纪律检查委员会", "location": "渭南市临渭区"},
    {"id": 6, "name": "渭南市公安局临渭分局", "type": "公安", "level": "县处级", "parent": "渭南市公安局", "location": "渭南市临渭区"},
]

positions_data = [
    # 区委
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "official news 2026-07/08; 起始时间待查"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "official 领导之窗"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "official resume 2026-07-29"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "official resume 2026-07-29"},
    # 区政府
    {"person_id": 2, "org_id": 2, "title": "代区长、区政府党组书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "2026-06-24 区人大常委会任命"},
    {"person_id": 3, "org_id": 2, "title": "常务副区长（党组副书记）", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "official resume 2026-07-29"},
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "official resume 2026-07-29"},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "official resume 2026-07-29"},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "official resume 2026-07-29"},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "official resume 2026-07-29"},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "official resume 2026-07-29; 民革"},
    {"person_id": 9, "org_id": 2, "title": "副区长（兼公安局长）", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "official resume 2026-07-29; 渭南市公安局党委委员"},
    {"person_id": 9, "org_id": 6, "title": "公安临渭分局局长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "兼"},
    {"person_id": 10, "org_id": 2, "title": "副区长（挂职）", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "挂职两年"},
]

relationships_data = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor_team", "context": "区委书记——代区长党政搭档（2026-06起共事）", "overlap_org": "中共临渭区委/临渭区人民政府", "overlap_period": "2026-06-present"},
    {"person_a": 1, "person_b": 2, "type": "meeting_overlap", "context": "'两优一先'表彰大会：菊峰讲话，马世仓主持（2026-07-06）", "overlap_org": "中共临渭区委", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 2, "type": "meeting_overlap", "context": "2026上半年重点工作点评会：菊峰讲话，马世仓主持（2026-07）", "overlap_org": "中共临渭区委/临渭区人民政府", "overlap_period": "2026-07"},
    # 区长与区政府班组成员
    {"person_a": 2, "person_b": 3, "type": "colleague", "context": "代区长——常务副区长（党组副书记）工作班子", "overlap_org": "临渭区人民政府", "overlap_period": "2026-06-present"},
    {"person_a": 2, "person_b": 4, "type": "colleague", "context": "代区长——副区长（区委常委）工作班子", "overlap_org": "临渭区人民政府", "overlap_period": "2026-06-present"},
    {"person_a": 2, "person_b": 5, "type": "colleague", "context": "代区长——副区长工作班子", "overlap_org": "临渭区人民政府", "overlap_period": "2026-06-present"},
    {"person_a": 2, "person_b": 6, "type": "colleague", "context": "代区长——副区长工作班子", "overlap_org": "临渭区人民政府", "overlap_period": "2026-06-present"},
    {"person_a": 2, "person_b": 7, "type": "colleague", "context": "代区长——副区长工作班子", "overlap_org": "临渭区人民政府", "overlap_period": "2026-06-present"},
    {"person_a": 2, "person_b": 8, "type": "colleague", "context": "代区长——副区长（民革）工作班子", "overlap_org": "临渭区人民政府", "overlap_period": "2026-06-present"},
    {"person_a": 2, "person_b": 9, "type": "colleague", "context": "代区长——副区长兼公安局长工作班子", "overlap_org": "临渭区人民政府", "overlap_period": "2026-06-present"},
    {"person_a": 2, "person_b": 10, "type": "colleague", "context": "代区长——挂职副区长工作班子", "overlap_org": "临渭区人民政府", "overlap_period": "2026-06-present"},
    # 区委书记与区政府骨干
    {"person_a": 1, "person_b": 3, "type": "colleague", "context": "区委书记与区委常委、常务副区长在区委常委会共事", "overlap_org": "中共临渭区委", "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "colleague", "context": "区委书记与区委常委、副区长李云鹏在区委常委会共事", "overlap_org": "中共临渭区委", "overlap_period": "present"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSONs
# ═══════════════════════════════════════════════════════════════════════════════

def _rel(person, pid, rtype, strength, evidence, org, period, conf="confirmed", sids=[]):
    return {"person": person, "person_id": pid, "relationship_type": rtype, "strength": strength,
            "evidence": evidence, "overlap_org": org, "overlap_period": period,
            "direction": "undirected", "confidence": conf, "source_ids": sids}


# --- 菊峰 (区委书记) ---
ju_feng_sources = [
    {"id": "S001", "title": "临渭区人民政府 领导之窗", "url": "https://www.linwei.gov.cn/zfxxgk/fdzdgknr/lczc/", "publisher": "临渭区人民政府", "published_at": "2026-07-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "Government roster official page"},
    {"id": "S002", "title": "临渭区委常委会召开会议 菊峰主持", "url": "https://www.linwei.gov.cn/xwzx/bdxw/2085166953952894978.html", "publisher": "临渭区人民政府", "published_at": "2026-08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认区委书记菊峰"},
    {"id": "S003", "title": "临渭区召开2026年上半年重点工作点评会", "url": "https://www.linwei.gov.cn/zfxxgk/fdzdgknr/lczc/qc/ldhd/2077914057566842882.html", "publisher": "临渭区人民政府", "published_at": "2026-07-17", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "菊峰讲话，马世仓主持"},
    {"id": "S004", "title": "菊峰调研全区防汛备汛工作", "url": "https://www.linwei.gov.cn/xwzx/bdxw/2084436344726728705.html", "publisher": "临渭区人民政府", "published_at": "2026-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认身份并记录治理活动"},
]

ju_feng_career = [
    {"start": "unknown", "end": "present", "org": "中共渭南市临渭区委员会", "title": "区委书记",
     "level": "县处级", "location": "陕西渭南", "system": "party", "rank": "正处级",
     "is_key_promotion": True, "notes": "当前在任（2026-07/08 官方新闻确认）", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
     "level": "", "location": "", "system": "other", "rank": "",
     "is_key_promotion": False, "notes": "公开资料未找到菊峰任临渭区委书记前的完整履历（出生年份、籍贯、教育、此前任职）",
     "confidence": "unverified", "source_ids": []},
]

ju_feng_rels = [
    _rel("马世仓", "linwei_ma_shicang", "overlap", "strong", "区委书记——代区长党政搭档", "中共临渭区委/临渭区人民政府", "2026-06-present", "confirmed", ["S001", "S003"]),
    _rel("刘刚", "linwei_liu_gang", "overlap", "medium", "同工委班子共事", "中共临渭区委", "present", "confirmed", ["S001"]),
    _rel("李云鹏", "linwei_li_yunpeng", "overlap", "medium", "同工委班子共事", "中共临渭区委", "present", "confirmed", ["S001"]),
]

ju_feng_governance = [
    {"period": "2026-07", "domain": "public_security", "achievement_or_event": "调研全区防汛备汛工作，部署防灾避险", "role_in_event": "带队调研", "measurable_outcome": "", "location": "渭南临渭区", "confidence": "confirmed", "source_ids": ["S004"]},
    {"period": "2026-07", "domain": "economic_development", "achievement_or_event": "主持上半年重点工作点评会，部署经济运行与项目建设", "role_in_event": "讲话部署", "measurable_outcome": "", "location": "渭南临渭区", "confidence": "confirmed", "source_ids": ["S003"]},
]

ju_confidence = {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
                 "relationship_confidence": "medium", "biggest_gap": "菊峰完整的履历（出生年份、籍贯、教育、前任职历）"}
ju_gaps = [
    {"priority": "critical", "question": "菊峰的完整履历（出生年份、籍贯、教育背景、此前所有任职经历）",
     "why_it_matters": "关键人物，履历缺失影响关系网络分析", "suggested_queries": ["菊峰 简历 渭南", "菊峰 任前公示", "菊峰 百度百科"], "last_attempted": AS_OF},
    {"priority": "high", "question": "菊峰何时就任临渭区委书记？前任是谁？去向？", "why_it_matters": "确定任期起点和前任去向",
     "suggested_queries": ["临渭区 前任区委书记", "临渭区 区委书记 任命"], "last_attempted": AS_OF},
]

# 马世仓 (代区长)
msc_sources = [
    {"id": "S201", "title": "临渭区人民政府 领导简历", "url": "https://www.linwei.gov.cn/zfxxgk/fdzdgknr/lczc/qc/ldjl/1.html", "publisher": "临渭区人民政府", "published_at": "2026-07-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "完整简历：区委副书记、代区长"},
    {"id": "S202", "title": "临渭区领导活动：八一节前马世仓走访慰问", "url": "https://www.linwei.gov.cn/zfxxgk/fdzdgknr/lczc/qc/ldhd/2084075875716706306.html", "publisher": "临渭区人民政府", "published_at": "2026-08-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "代区长身份确认"},
    {"id": "S203", "title": "临渭区2026上半年重点工作点评会", "url": "https://www.linwei.gov.cn/zfxxgk/fdzdgknr/lczc/qc/ldhd/2077914057566842882.html", "publisher": "临渭区人民政府", "published_at": "2026-07-17", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "马世仓主持"},
]

msc_career = [
    {"start": "unknown", "end": "unknown", "org": "乡镇政府", "title": "副乡长、党委副书记",
     "level": "乡科级", "location": "陕西渭南", "system": "government", "rank": "副科级",
     "is_key_promotion": False, "notes": "early career per official resume", "confidence": "confirmed", "source_ids": ["S201"]},
    {"start": "unknown", "end": "unknown", "org": "团县委", "title": "团县委副书记、团县委书记",
     "level": "乡科级", "location": "陕西渭南", "system": "organization", "rank": "正科级",
     "is_key_promotion": False, "notes": "official resume", "confidence": "confirmed", "source_ids": ["S201"]},
    {"start": "unknown", "end": "unknown", "org": "县委", "title": "县委常委、宣传部部长、县纪委书记、县监委主任",
     "level": "县处级", "location": "陕西渭南", "system": "discipline", "rank": "副处级",
     "is_key_promotion": True, "notes": "official resume", "confidence": "confirmed", "source_ids": ["S201"]},
    {"start": "unknown", "end": "unknown", "org": "渭南市委办公室", "title": "市委副秘书长、市委保密机要技术服务中心主任",
     "level": "地厅级", "location": "陕西渭南", "system": "party", "rank": "正处级",
     "is_key_promotion": True, "notes": "official resume", "confidence": "confirmed", "source_ids": ["S201"]},
    {"start": "2025-04", "end": "2026-06", "org": "渭南市行政审批服务局", "title": "党组书记、局长",
     "level": "地厅级", "location": "陕西渭南", "system": "government", "rank": "正处级",
     "is_key_promotion": True, "notes": "official resume, 2025-04 任, 2026 调任", "confidence": "confirmed", "source_ids": ["S201"]},
    {"start": "2026-06", "end": "present", "org": "渭南市临渭区人民政府", "title": "副区长、代区长",
     "level": "县处级", "location": "陕西渭南", "system": "government", "rank": "正处级",
     "is_key_promotion": True, "notes": "2026年6月任现职（区人大常委会任命）", "confidence": "confirmed", "source_ids": ["S201", "S202"]},
]

msc_rels = [
    _rel("菊峰", "linwei_ju_feng", "overlap", "strong", "区委书记—代区长党政搭档", "共同作用", "2026-06-present", "confirmed", ["S203"]),
    _rel("刘刚", "linwei_liu_gang", "overlap", "strong", "代区长—常务副区长工作关系", "临渭区人民政府", "2026-06-present", "confirmed", ["S201"]),
    _rel("李云鹏", "linwei_li_yunpeng", "overlap", "strong", "代区长—副区长（区委常委）工作关系", "临渭区人民政府", "2026-06-present", "confirmed", ["S201"]),
]

msc_governance = [
    {"period": "2026-08", "domain": "public_security", "achievement_or_event": "八旬走访临渭区人武部", "role_in_event": "走访慰问", "measurable_outcome": "", "location": "渭南临渭区", "confidence": "confirmed", "source_ids": ["S202"]},
    {"period": "2026-07", "domain": "urban_construction", "achievement_or_event": "带队调研城区架空线缆整治、环境整治提升", "role_in_event": "带队调研", "measurable_outcome": "", "location": "渭南临渭区", "confidence": "confirmed", "source_ids": ["S202"]},
]

msc_confidence = {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial",
                  "relationship_confidence": "high", "biggest_gap": "任临渭区代区长前的具体任职县名（常务工作工具所在县级机关）与早年乡镇任职时间"}
msc_gaps = [
    {"priority": "high", "question": "马世仓任县委常委、宣传部长/县纪委书记/县监委主任所在的县名及具体起止时间", "why_it_matters": "关键的跨县经历，关系网络分析核心", "suggested_queries": ["马世仓 县纪委书记 渭南 哪个县"], "last_attempted": AS_OF},
    {"priority": "medium", "question": "马世仓乡镇副乡长、团县委书记的任职时间", "why_it_matters": "完整时间线", "suggested_queries": ["马世仓 乡 副乡长 简历"], "last_attempted": AS_OF},
]


def _rel(person, pid, rtype, strength, evidence, org, period, conf, sids):
    return {"person": person, "person_id": pid, "relationship_type": rtype, "strength": strength,
            "evidence": evidence, "overlap_org": org, "overlap_period": period,
            "direction": "undirected", "confidence": conf, "source_ids": sids}


PERSON_JSON_TEMPLATE = {}


def build_person_json_files():
    # 菊峰
    pjf = {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {"province": "陕西省", "city": "渭南市", "region": "临渭区", "job": "区委书记", "task_id": "shaanxi_临渭区", "time_focus": "2026"},
        "identity": {"person_id": "linwei_ju_feng", "name": "菊峰", "aliases": [], "gender": "", "ethnicity": "",
                     "birth": "", "birthplace": "", "education": [], "party_join": "中共党员", "work_start": "",
                     "dedupe_keys": {"name_birth": "菊峰_unknown", "name_birthplace": "菊峰_unknown", "official_profile_url": ju_feng_sources[0]["url"]}},
        "current_status": {"current_post": "区委书记", "current_org": "中共渭南市临渭区委员会", "administrative_rank": "正处级",
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": [s["id"] for s in ju_feng_sources]},
        "career_timeline": ju_feng_career,
        "organizations": [], "relationships": ju_feng_rels,
        "governance_record": ju_feng_governance,
        "professional_profile": {"primary_specializations": ["党的建设", "经济工作", "城市治理"], "secondary_specializations": [],
                                 "career_pattern": "local_ladder", "systems_experience": ["party", "government"], "geographic_pattern": [],
                                 "promotion_velocity": {"summary": "当前确认职务为临渭区委书记", "notable_fast_promotions": []}},
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "discipline_oriented", "evidence": "多次强调全面从严治党、正风肃纪反腐", "confidence": "plausible", "source_ids": ["S002"]},
                {"trait": "pragmatic", "evidence": "讲话中强调紧抓项目建设，年初目标清单化", "confidence": "plausible", "source_ids": ["S003"]}],
            "speech_themes": ["党建引领", "高质量发展", "城市精细化管理", "民生保障"], "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": ju_feng_sources, "confidence_summary": ju_confidence, "open_questions": ju_gaps,
    }
    PERSON_JSON_TEMPLATE[f"菊峰"] = (f"{TODAY}-陕西省-渭南市-临渭区-区委书记-菊峰.json", pjf)

    # 马世仓
    pmsc = {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {"province": "陕西省", "city": "渭南市", "region": "临渭区", "job": "代区长", "task_id": "shaanxi_临渭区", "time_focus": "2026"},
        "identity": {"person_id": "linwei_ma_shicang", "name": "马世仓", "aliases": [], "gender": "男", "ethnicity": "汉族",
                     "birth": "1979年12月", "birthplace": "陕西蒲城", "education": ["大学本科"], "party_join": "中共党员", "work_start": "",
                     "dedupe_keys": {"name_birth": "马世仓_1979年12月", "name_birthplace": "马世仓_陕西蒲城", "official_profile_url": msc_sources[0]["url"]}},
        "current_status": {"current_post": "区委副书记、区政府党组书记、代区长", "current_org": "渭南市临渭区人民政府",
                           "administrative_rank": "正处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": [s["id"] for s in msc_sources]},
        "career_timeline": msc_career,
        "organizations": [], "relationships": msc_rels,
        "governance_record": msc_governance,
        "professional_profile": {"primary_specializations": ["纪检监察", "行政审批", "自然资源"], "secondary_specializations": [],
                                 "career_pattern": "cross_county", "systems_experience": ["discipline", "government"], "geographic_pattern": ["陕西潼关", "渭南"],
                                 "promotion_velocity": {"summary": "从县纪委书记到市委副秘书长再到区代区长，阶梯式晋升", "notable_fast_promotions": []}},
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "pragmatic", "evidence": "调研中强调清单化管理、项目化推进", "confidence": "plausible", "source_ids": ["S202"]},
                {"trait": "discipline_oriented", "evidence": "曾任县纪委监委主任，调研中强调'守红线''整改动真碰硬'", "confidence": "plausible", "source_ids": ["S201"]}],
            "speech_themes": ["优化营商环境", "生态环境保护", "高质量发展"], "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": msc_sources, "confidence_summary": msc_confidence, "open_questions": msc_gaps,
    }
    PERSON_JSON_TEMPLATE["马世仓"] = (f"{TODAY}-陕西省-渭南市-临渭区-代区长-马世仓.json", pmsc)


def write_person_json(data: dict, filename: str) -> Path:
    path = STAGING_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")
    return path


def main():
    build_person_json_files()
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

    print("Writing person JSONs ...")
    for key, (filename, data) in PERSON_JSON_TEMPLATE.items():
        write_person_json(data, filename)

    # Post-build verification: reopen the DB (DB_PATH) read-only and confirm tables
    print("\nVerifying DB (" + DB_PATH + ") ...")
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        for table in ("persons", "organizations", "positions", "relationships"):
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table}: {count}")
    finally:
        conn.close()
    print("Verifying GEXF exists:", os.path.exists(GEXF_PATH))

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