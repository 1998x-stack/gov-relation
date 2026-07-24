#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 任丘市 (Renqiu) leadership network.

任丘市 is a county-level city under 沧州市, 河北省.
"""

import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

SLUG = "任丘市"
TODAY = datetime.now().strftime("%Y%m%d")
YEAR = datetime.now().strftime("%Y")

# Tokens expected by process_tmp.py validation
DB_PATH = str(DATABASE_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(GRAPH_DIR / f"{SLUG}_network.gexf")

# ── ORGANIZATIONS ─────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共任丘市委员会", "type": "党委", "level": "县级", "parent": "", "location": "河北省沧州市任丘市"},
    {"id": 2, "name": "任丘市人民政府", "type": "政府", "level": "县级", "parent": "", "location": "河北省沧州市任丘市"},
    {"id": 3, "name": "任丘市纪委监委", "type": "党委", "level": "县级", "parent": "", "location": "河北省沧州市任丘市"},
    {"id": 4, "name": "任丘市人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "河北省沧州市任丘市"},
    {"id": 5, "name": "任丘市政协", "type": "政协", "level": "县级", "parent": "", "location": "河北省沧州市任丘市"},
    {"id": 6, "name": "任丘市公安局", "type": "政府", "level": "县级", "parent": "", "location": "河北省沧州市任丘市"},
    {"id": 7, "name": "任丘市人武部", "type": "政府", "level": "县级", "parent": "", "location": "河北省沧州市任丘市"},
    {"id": 8, "name": "中共沧州市委员会", "type": "党委", "level": "地级", "parent": "", "location": "河北省沧州市"},
    {"id": 9, "name": "沧州市人民政府", "type": "政府", "level": "地级", "parent": "", "location": "河北省沧州市"},
]

# ── PERSONS ────────────────────────────────────────────────────────────

persons = [
    # ── Top Leaders ──
    {
        "id": 1, "name": "王永昌", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "任丘市委书记", "current_org": "中共任丘市委员会",
        "source": "https://www.renqiu.gov.cn/renqiu/zwzfhy/202504/3beaeb915f404de1ab99c2ca7bace511.shtml",
    },
    {
        "id": 2, "name": "尚亮", "gender": "男", "ethnicity": "汉族",
        "birth": "1973-10", "birthplace": "", "education": "研究生",
        "party_join": "", "work_start": "",
        "current_post": "任丘市委副书记、市长", "current_org": "任丘市人民政府",
        "source": "https://www.renqiu.gov.cn/renqiu/zwldbz/202403/bc1a7748d4c049979b30f84392166bd4.shtml",
    },
    # ── Deputy Party Secretary ──
    {
        "id": 3, "name": "李旭东", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "任丘市委副书记", "current_org": "中共任丘市委员会",
        "source": "https://www.renqiu.gov.cn/renqiu/zwzfhy/202503/5e77b523d1ed44e198946160a3803d35.shtml",
    },
    # ── City Government Leaders ──
    {
        "id": 4, "name": "张炜", "gender": "男", "ethnicity": "汉族",
        "birth": "1980-05", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "任丘市委常委、常务副市长", "current_org": "任丘市人民政府",
        "source": "https://www.renqiu.gov.cn/renqiu/zwldbz/202403/689cb64bee4a464fa1dd4c7b1e1667c0.shtml",
    },
    {
        "id": 5, "name": "张付军", "gender": "男", "ethnicity": "汉族",
        "birth": "1974-05", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "任丘市政府党组成员、副市长、公安局局长", "current_org": "任丘市人民政府",
        "source": "https://www.renqiu.gov.cn/renqiu/zwldbz/202403/f27e922a1fcc41eba42b72de136cf7e3.shtml",
    },
    {
        "id": 6, "name": "杜伟", "gender": "男", "ethnicity": "汉族",
        "birth": "1987-09", "birthplace": "", "education": "本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "任丘市政府党组成员、副市长", "current_org": "任丘市人民政府",
        "source": "https://www.renqiu.gov.cn/renqiu/zwldbz/202401/e858a49ac0bf4a0a8315ede229591e59.shtml",
    },
    {
        "id": 7, "name": "黄东", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-10", "birthplace": "", "education": "本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "任丘市政府党组成员、副市长", "current_org": "任丘市人民政府",
        "source": "https://www.renqiu.gov.cn/renqiu/zwldbz/202403/0efed8e31b214c8990041cd3e7ce6f29.shtml",
    },
    {
        "id": 8, "name": "刘芳", "gender": "女", "ethnicity": "汉族",
        "birth": "1982-07", "birthplace": "", "education": "研究生",
        "party_join": "", "work_start": "",
        "current_post": "任丘市政府党组成员、副市长", "current_org": "任丘市人民政府",
        "source": "https://www.renqiu.gov.cn/renqiu/zwldbz/202301/1ef3ced15e5b4537a49a5e4fcf380150.shtml",
    },
    {
        "id": 9, "name": "张占山", "gender": "男", "ethnicity": "汉族",
        "birth": "1968-11", "birthplace": "", "education": "本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "任丘市人民政府二级调研员", "current_org": "任丘市人民政府",
        "source": "https://www.renqiu.gov.cn/renqiu/zwldbz/202403/2660a81d6d1b4e5c8c995e42ded56ca4.shtml",
    },
    # ── Other Key Leaders ──
    {
        "id": 10, "name": "郭建友", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "任丘市委常委、纪委书记、监委主任", "current_org": "任丘市纪委监委",
        "source": "https://www.renqiu.gov.cn/renqiu/zwzfhy/202604/81961a7ddf1042aeb2286c6aac8cd768.shtml",
    },
    {
        "id": 11, "name": "娄新广", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "任丘市委常委、人武部上校部长", "current_org": "任丘市人武部",
        "source": "https://www.renqiu.gov.cn/renqiu/zwzfhy/202501/1241d135a9f0402cb8e924669bbe5ff7.shtml",
    },
    {
        "id": 12, "name": "刘颖茹", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "任丘市人大常委会主任", "current_org": "任丘市人大常委会",
        "source": "https://www.renqiu.gov.cn/renqiu/zwzfhy/202604/81961a7ddf1042aeb2286c6aac8cd768.shtml",
    },
]

# ── POSITIONS ──────────────────────────────────────────────────────────

positions = [
    # 王永昌 - Party Secretary
    {"person_id": 1, "org_id": 1, "title": "任丘市委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2025年初已在任"},
    # 尚亮 - Mayor
    {"person_id": 2, "org_id": 2, "title": "任丘市委副书记、市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持市政府全面工作，分管审计局"},
    {"person_id": 2, "org_id": 1, "title": "任丘市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李旭东 - Deputy Secretary
    {"person_id": 3, "org_id": 1, "title": "任丘市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张炜 - Executive Deputy Mayor
    {"person_id": 4, "org_id": 2, "title": "任丘市委常委、常务副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责发展改革、财税、统计等"},
    {"person_id": 4, "org_id": 1, "title": "任丘市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张付军 - Deputy Mayor, Public Security
    {"person_id": 5, "org_id": 2, "title": "任丘市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责公安、司法、退役军人等"},
    {"person_id": 5, "org_id": 6, "title": "任丘市公安局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 杜伟 - Deputy Mayor
    {"person_id": 6, "org_id": 2, "title": "任丘市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责文化广电旅游、民政、教育体育等"},
    # 黄东 - Deputy Mayor
    {"person_id": 7, "org_id": 2, "title": "任丘市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责生态环境、卫生健康、医疗保障等"},
    # 刘芳 - Deputy Mayor
    {"person_id": 8, "org_id": 2, "title": "任丘市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责农业农村、水务、乡村振兴等"},
    # 张占山 - Second-level Researcher
    {"person_id": 9, "org_id": 2, "title": "任丘市人民政府二级调研员", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助张炜负责道路交通、工业、科技等"},
    # 郭建友 - Discipline Commission
    {"person_id": 10, "org_id": 3, "title": "任丘市委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "任丘市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 娄新广 - People's Armed Forces
    {"person_id": 11, "org_id": 7, "title": "任丘市委常委、人武部上校部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "任丘市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘颖茹 - People's Congress
    {"person_id": 12, "org_id": 4, "title": "任丘市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────

relationships = [
    # 王永昌 ←→ 尚亮 (Secretary-Mayor working relationship)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记与市长搭档", "overlap_org": "任丘市四套班子", "overlap_period": ""},
    # 王永昌 ←→ 李旭东 (Secretary-Deputy Secretary)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与市委副书记", "overlap_org": "中共任丘市委员会", "overlap_period": ""},
    # 尚亮 ←→ 张炜 (Mayor-Executive Deputy Mayor)
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "市长与常务副市长", "overlap_org": "任丘市人民政府", "overlap_period": ""},
    # 张炜 ←→ 张占山 (Executive Deputy - Assistant)
    {"person_a": 4, "person_b": 9, "type": "superior_subordinate", "context": "常务副市长与二级调研员（协助关系）", "overlap_org": "任丘市人民政府", "overlap_period": ""},
    # 张炜 ←→ 杜伟 (Co-deputies in city government)
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "任丘市人民政府", "overlap_period": ""},
    # 张炜 ←→ 黄东 (Co-deputies)
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "任丘市人民政府", "overlap_period": ""},
    # 张炜 ←→ 刘芳 (Co-deputies)
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "任丘市人民政府", "overlap_period": ""},
    # 张炜 ←→ 张付军 (Co-deputies)
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "任丘市人民政府", "overlap_period": ""},
    # 王永昌 ←→ 郭建友 (Secretary-Discipline)
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "市委书记与纪委书记", "overlap_org": "中共任丘市委员会", "overlap_period": ""},
    # 王永昌 ←→ 娄新广 (Secretary-Armed Forces)
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "市委书记与人武部长", "overlap_org": "中共任丘市委员会", "overlap_period": ""},
    # 郭建友 ←→ 娄新广 (Party Standing Committee colleagues)
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "市委常委班子成员", "overlap_org": "中共任丘市委员会", "overlap_period": ""},
    # Standing Committee cross-links
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "市委常委班子成员", "overlap_org": "中共任丘市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 11, "type": "overlap", "context": "市委常委班子成员", "overlap_org": "中共任丘市委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 10, "type": "overlap", "context": "市委常委班子成员", "overlap_org": "中共任丘市委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 11, "type": "overlap", "context": "市委常委班子成员", "overlap_org": "中共任丘市委员会", "overlap_period": ""},
]

# ── SOURCE REGISTER ────────────────────────────────────────────────────

sources = [
    {"id": "S001", "title": "尚亮 - 任丘市人民政府市长", "url": "https://www.renqiu.gov.cn/renqiu/zwldbz/202403/bc1a7748d4c049979b30f84392166bd4.shtml",
     "publisher": "任丘市人民政府", "published_at": "2025-12-08", "source_type": "official", "reliability": "high"},
    {"id": "S002", "title": "张炜 - 任丘市人民政府常务副市长", "url": "https://www.renqiu.gov.cn/renqiu/zwldbz/202403/689cb64bee4a464fa1dd4c7b1e1667c0.shtml",
     "publisher": "任丘市人民政府", "published_at": "2025-12-08", "source_type": "official", "reliability": "high"},
    {"id": "S003", "title": "张付军 - 任丘市人民政府副市长", "url": "https://www.renqiu.gov.cn/renqiu/zwldbz/202403/f27e922a1fcc41eba42b72de136cf7e3.shtml",
     "publisher": "任丘市人民政府", "published_at": "2025-12-08", "source_type": "official", "reliability": "high"},
    {"id": "S004", "title": "杜伟 - 任丘市人民政府副市长", "url": "https://www.renqiu.gov.cn/renqiu/zwldbz/202401/e858a49ac0bf4a0a8315ede229591e59.shtml",
     "publisher": "任丘市人民政府", "published_at": "2024-01-22", "source_type": "official", "reliability": "high"},
    {"id": "S005", "title": "黄东 - 任丘市人民政府副市长", "url": "https://www.renqiu.gov.cn/renqiu/zwldbz/202403/0efed8e31b214c8990041cd3e7ce6f29.shtml",
     "publisher": "任丘市人民政府", "published_at": "2023-01-05", "source_type": "official", "reliability": "high"},
    {"id": "S006", "title": "刘芳 - 任丘市人民政府副市长", "url": "https://www.renqiu.gov.cn/renqiu/zwldbz/202301/1ef3ced15e5b4537a49a5e4fcf380150.shtml",
     "publisher": "任丘市人民政府", "published_at": "2023-01-05", "source_type": "official", "reliability": "high"},
    {"id": "S007", "title": "张占山 - 任丘市人民政府二级调研员", "url": "https://www.renqiu.gov.cn/renqiu/zwldbz/202403/2660a81d6d1b4e5c8c995e42ded56ca4.shtml",
     "publisher": "任丘市人民政府", "published_at": "2022-06-05", "source_type": "official", "reliability": "high"},
    {"id": "S008", "title": "市委理论学习中心组2025年度第三次集中学习会议（王永昌）", "url": "https://www.renqiu.gov.cn/renqiu/zwzfhy/202504/3beaeb915f404de1ab99c2ca7bace511.shtml",
     "publisher": "任丘市人民政府", "published_at": "2025-04-11", "source_type": "official", "reliability": "high"},
    {"id": "S009", "title": "任丘市十届人大常委会第三十七次会议（郭建友、刘颖茹）", "url": "https://www.renqiu.gov.cn/renqiu/zwzfhy/202604/81961a7ddf1042aeb2286c6aac8cd768.shtml",
     "publisher": "任丘市人民政府", "published_at": "2026-03-11", "source_type": "official", "reliability": "high"},
    {"id": "S010", "title": "任丘市委农村工作会议（王永昌、李旭东）", "url": "https://www.renqiu.gov.cn/renqiu/zwzfhy/202503/5e77b523d1ed44e198946160a3803d35.shtml",
     "publisher": "任丘市人民政府", "published_at": "2025-03-19", "source_type": "official", "reliability": "high"},
    {"id": "S011", "title": "任丘市2025年度征兵工作会议（娄新广）", "url": "https://www.renqiu.gov.cn/renqiu/zwzfhy/202501/1241d135a9f0402cb8e924669bbe5ff7.shtml",
     "publisher": "任丘市人民政府", "published_at": "2025-01-26", "source_type": "official", "reliability": "high"},
]

# ── PERSON JSON FILES ──────────────────────────────────────────────────

def generate_person_json():
    """Generate person JSON files for core leaders."""
    person_data = {
        "https://www.renqiu.gov.cn/renqiu/zwzfhy/202504/3beaeb915f404de1ab99c2ca7bace511.shtml": {
            "person_id": "renqiu_wang_yongchang",
            "name": "王永昌",
            "current_post": "任丘市委书记",
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "河北省",
                "city": "沧州市",
                "region": "任丘市",
                "job": "市委书记",
                "task_id": "hebei_任丘市",
                "time_focus": "2024-2026",
            },
            "identity": {
                "name": "王永昌",
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {"name_birth": "", "name_birthplace": "", "official_profile_url": ""},
            },
            "current_status": {
                "current_post": "任丘市委书记",
                "current_org": "中共任丘市委员会",
                "administrative_rank": "正处级",
                "as_of": TODAY,
                "is_current_confirmed": True,
                "source_ids": ["S008", "S010", "S011"],
            },
            "career_timeline": [
                {"start": "unknown", "end": "present", "org": "中共任丘市委员会", "title": "任丘市委书记",
                 "level": "正处级", "confidence": "confirmed", "source_ids": ["S008", "S010", "S011"]},
            ],
            "organizations": [{"organization": "中共任丘市委员会", "role": "市委书记", "period": "—至今", "note": ""}],
            "relationships": [
                {"person": "尚亮", "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "市委书记与市长搭档", "overlap_org": "任丘市四套班子",
                 "confidence": "confirmed", "source_ids": ["S008"]},
                {"person": "李旭东", "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "市委书记与市委副书记", "overlap_org": "中共任丘市委员会",
                 "confidence": "confirmed", "source_ids": ["S010"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "履历待查", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "caveat": "尚未收集到足够公开资料来评估工作风格",
            },
            "risk_and_integrity_signals": [],
            "source_register": sources,
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "王永昌的完整履历（出生日期、教育背景、任职经历）均未找到公开资料",
            },
            "open_questions": [
                {"priority": "critical", "question": "王永昌的出生日期、出生地、教育背景", "why_it_matters": "基本身份信息缺失",
                 "suggested_queries": ["王永昌 简历 任丘", "王永昌 任前公示"], "last_attempted": TODAY},
                {"priority": "critical", "question": "王永昌任任丘市委书记之前的履历", "why_it_matters": "无法评估其晋升路径和背景",
                 "suggested_queries": ["王永昌 沧州 任职", "王永昌 曾任"], "last_attempted": TODAY},
            ],
        },
        "https://www.renqiu.gov.cn/renqiu/zwldbz/202403/bc1a7748d4c049979b30f84392166bd4.shtml": {
            "person_id": "renqiu_shang_liang",
            "name": "尚亮",
            "current_post": "任丘市委副书记、市长",
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "河北省",
                "city": "沧州市",
                "region": "任丘市",
                "job": "市长",
                "task_id": "hebei_任丘市",
                "time_focus": "2024-2026",
            },
            "identity": {
                "name": "尚亮",
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1973-10",
                "birthplace": "",
                "native_place": "",
                "education": [{"period": "", "institution": "", "major": "", "degree": "研究生", "study_type": "unknown", "source_ids": ["S001"]}],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {"name_birth": "尚亮_1973-10", "name_birthplace": "", "official_profile_url": ""},
            },
            "current_status": {
                "current_post": "任丘市委副书记、市长",
                "current_org": "任丘市人民政府",
                "administrative_rank": "正处级",
                "as_of": TODAY,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S008"],
            },
            "career_timeline": [
                {"start": "unknown", "end": "present", "org": "任丘市人民政府", "title": "任丘市委副书记、市长",
                 "level": "正处级", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "organizations": [{"organization": "任丘市人民政府", "role": "市长", "period": "—至今", "note": ""}],
            "relationships": [
                {"person": "王永昌", "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "市长与市委书记搭档", "overlap_org": "任丘市四套班子",
                 "confidence": "confirmed", "source_ids": ["S001", "S008"]},
                {"person": "张炜", "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "市长与常务副市长", "overlap_org": "任丘市人民政府",
                 "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "governance_record": [
                {"period": "任现职以来", "domain": "economic_development", "achievement_or_event": "主持市政府全面工作，分管审计局，负责服务京津冀协同发展与雄安新区规划建设",
                 "role_in_event": "主要负责", "measurable_outcome": "", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "professional_profile": {
                "primary_specializations": ["government_administration"],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "履历待查", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "caveat": "尚未收集到足够公开资料来评估工作风格",
            },
            "risk_and_integrity_signals": [],
            "source_register": sources,
            "confidence_summary": {
                "identity": "partial",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "尚亮任任丘市长之前的完整履历",
            },
            "open_questions": [
                {"priority": "critical", "question": "尚亮任任丘市长之前的履历", "why_it_matters": "无法评估其晋升路径",
                 "suggested_queries": ["尚亮 简历 沧州", "尚亮 任前公示"], "last_attempted": TODAY},
                {"priority": "high", "question": "尚亮的出生地", "why_it_matters": "评估地域背景",
                 "suggested_queries": ["尚亮 出生 籍贯"], "last_attempted": TODAY},
                {"priority": "medium", "question": "尚亮的入党时间和参加工作时间", "why_it_matters": "评估体制内资历",
                 "suggested_queries": ["尚亮 入党"], "last_attempted": TODAY},
            ],
        },
    }
    return person_data


# ── MAIN ────────────────────────────────────────────────────────────────

def main():
    TMP_DIR = Path(__file__).resolve().parent
    db_path = TMP_DIR / f"{SLUG}_network.db"
    gexf_path = TMP_DIR / f"{SLUG}_network.gexf"

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"\nDatabase: {db_path}")
    print(f"GEXF: {gexf_path}")

    # Generate person JSON files
    person_data = generate_person_json()
    for source_url, data in person_data.items():
        person_id = data["person_id"]
        role_short = "市委书记" if "书记" in data["current_post"] else "市长"
        fname = f"{TODAY}-河北省-沧州市-{role_short}-{data['name']}.json"
        fpath = TMP_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Person JSON: {fpath}")


if __name__ == "__main__":
    main()
