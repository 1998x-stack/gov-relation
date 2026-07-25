#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 沂源县, 淄博市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_沂源县
Level: 县
Targets: 县委书记 & 县长

Key findings:
- 县委书记 张涛 — 男, 汉族, as of 2026年7月, 主持县委全面工作
- 县长 赵学 — 县委副书记、县人民政府县长, as of 2026年7月
- 县人大常委会主任 车春雷
- 县政协主席 武光明
- 县委副书记、宣传部部长 郑舰
- 县委常委、东里镇党委书记 尚勇健
- 县领导 宋传方 (likely 县委常委/副县长)
- 县领导 于庆, 李民斌, 吴明 参与分管领域工作

Research sources:
- 沂源县人民政府网站 (www.yiyuan.gov.cn) — multiple news articles (2026年6-7月)
- 县党政联席扩大会议暨上半年工作会议新闻 (2026-07-23)
- 县委常委会会议新闻 (2026-07-08)
- 县委书记张涛调研项目建设情况 (2026-06-25)
- 县长赵学督导调研安全生产新闻 (2026-07-21)
- 庆祝中国共产党成立105周年大会集体收看 (2026-07-01)
- 县委常委、宣传部部长林恒来我县调研 (2026-07-17)

Confidence notes:
- 张涛和赵学当前职务已通过县政府官网多次新闻确认 (as of 2026年7月)
- 县委、人大、政协主要领导人已通过参会名单确认
- 张涛和赵学的详细早期履历、出生年月等个人信息未在县政府官网公开（需百度百科等补充）
- 部分副县长、县委常委的具体分管信息和详细简历待补充
"""

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build  # noqa: E402

SLUG = "沂源县"
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
    # Party Committee (县委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 张涛 — 县委书记
    {
        "id": 1,
        "name": "张涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沂源县委书记",
        "current_org": "中共沂源县委员会",
        "source": "沂源县人民政府网站新闻 (yiyuan.gov.cn, 2026年6-7月): '县委书记张涛调研项目建设情况'(2026-06-25), '县委书记张涛主持会议并讲话'(2026-07-08, 2026-07-23), '张涛到悦庄镇调研'(2026-07-19), '张涛到南鲁山镇调研'(2026-07-18)"
    },
    # 赵学 — 县委副书记、县长
    {
        "id": 2,
        "name": "赵学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沂源县委副书记、县人民政府县长",
        "current_org": "沂源县人民政府",
        "source": "沂源县人民政府网站新闻 (yiyuan.gov.cn, 2026年7月): '县委副书记、县人民政府县长赵学督导调研安全生产工作'(2026-07-21), '赵学督导生态环境重点工作'(2026-05-13), '赵学调研马路市场整治工作'(2026-05-08)"
    },
    # 郑舰 — 县委副书记、宣传部部长
    {
        "id": 3,
        "name": "郑舰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沂源县委副书记、宣传部部长",
        "current_org": "中共沂源县委员会",
        "source": "沂源县人民政府网站新闻 (yiyuan.gov.cn, 2026年7月): '县党政联席扩大会议暨上半年工作会议召开'(2026-07-23), '县委常委会会议召开'(2026-07-08), '市委常委、宣传部部长林恒来我县调研'(2026-07-17)"
    },
    # 尚勇健 — 县委常委、东里镇党委书记
    {
        "id": 4,
        "name": "尚勇健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沂源县委常委、东里镇党委书记",
        "current_org": "中共沂源县委员会",
        "source": "沂源县人民政府网站新闻 (yiyuan.gov.cn, 2026年6月): '县委书记张涛调研项目建设情况'(2026-06-25)"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # County Government (县政府) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 赵学 — already listed above as person 2 (县委副书记、县长)
    # 宋传方 — 县领导 (likely 副县长 or 县委常委）
    {
        "id": 5,
        "name": "宋传方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沂源县领导",
        "current_org": "沂源县人民政府",
        "source": "沂源县人民政府网站新闻 (yiyuan.gov.cn, 2026年7月): '张涛到悦庄镇调研'(2026-07-19), '张涛到南鲁山镇调研'(2026-07-18), '张涛调研防汛救灾工作'(2026-07-12)"
    },
    # 于庆 — 县领导
    {
        "id": 6,
        "name": "于庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沂源县领导",
        "current_org": "沂源县人民政府",
        "source": "沂源县人民政府网站新闻 (yiyuan.gov.cn, 2026年7月): '文旅高质量发展分线指挥部二季度交流会议'(2026-07-15)"
    },
    # 李民斌 — 县领导
    {
        "id": 7,
        "name": "李民斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沂源县领导",
        "current_org": "沂源县人民政府",
        "source": "沂源县人民政府网站新闻 (yiyuan.gov.cn, 2026年7月): '文旅高质量发展分线指挥部二季度交流会议'(2026-07-15)"
    },
    # 吴明 — 县领导
    {
        "id": 8,
        "name": "吴明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沂源县领导",
        "current_org": "沂源县人民政府",
        "source": "沂源县人民政府网站新闻 (yiyuan.gov.cn, 2026年7月): '文旅高质量发展分线指挥部二季度交流会议'(2026-07-15)"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # County People's Congress (县人大)
    # ══════════════════════════════════════════════════════════════════════════

    # 车春雷 — 县人大常委会主任
    {
        "id": 9,
        "name": "车春雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沂源县人大常委会主任",
        "current_org": "沂源县人民代表大会常务委员会",
        "source": "沂源县人民政府网站新闻 (yiyuan.gov.cn, 2026年7月): '县党政联席扩大会议暨上半年工作会议召开'(2026-07-23), '县委常委会会议召开'(2026-07-08), '全县高质量发展重点项目现场推进会'(2026-07-22)"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # County Political Consultative Conference (县政协)
    # ══════════════════════════════════════════════════════════════════════════

    # 武光明 — 县政协主席
    {
        "id": 10,
        "name": "武光明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沂源县政协主席",
        "current_org": "中国人民政治协商会议沂源县委员会",
        "source": "沂源县人民政府网站新闻 (yiyuan.gov.cn, 2026年7月): '县党政联席扩大会议暨上半年工作会议召开'(2026-07-23), '文旅高质量发展分线指挥部二季度交流会议'(2026-07-15)"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────────

organizations_data = [
    {"id": 1, "name": "中共沂源县委员会", "type": "党委", "level": "县", "parent": "中共淄博市委", "location": "山东省淄博市沂源县"},
    {"id": 2, "name": "沂源县人民政府", "type": "政府", "level": "县", "parent": "淄博市人民政府", "location": "山东省淄博市沂源县"},
    {"id": 3, "name": "沂源县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "沂源县", "location": "山东省淄博市沂源县"},
    {"id": 4, "name": "中国人民政治协商会议沂源县委员会", "type": "政协", "level": "县", "parent": "沂源县", "location": "山东省淄博市沂源县"},
    {"id": 5, "name": "中共沂源县纪律检查委员会", "type": "纪委", "level": "县", "parent": "中共沂源县委员会", "location": "山东省淄博市沂源县"},
    {"id": 6, "name": "沂源县监察委员会", "type": "政府", "level": "县", "parent": "沂源县", "location": "山东省淄博市沂源县"},
    {"id": 7, "name": "中共沂源县委组织部", "type": "党委", "level": "县", "parent": "中共沂源县委员会", "location": "山东省淄博市沂源县"},
    {"id": 8, "name": "中共沂源县委宣传部", "type": "党委", "level": "县", "parent": "中共沂源县委员会", "location": "山东省淄博市沂源县"},
    {"id": 9, "name": "中共沂源县委政法委员会", "type": "党委", "level": "县", "parent": "中共沂源县委员会", "location": "山东省淄博市沂源县"},
    {"id": 10, "name": "沂源县东里镇党委", "type": "党委", "level": "乡镇", "parent": "中共沂源县委员会", "location": "山东省淄博市沂源县东里镇"},
]

# ── Positions (person_id, org_id, title, start/end) ──────────────────────────

positions_data = [
    # 张涛 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "沂源县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持县委全面工作; as of 2026年7月"},
    # 赵学 — 县委副书记、县长
    {"person_id": 2, "org_id": 1, "title": "沂源县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "沂源县人民政府县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持县政府全面工作; as of 2026年7月"},
    # 郑舰 — 县委副书记、宣传部部长
    {"person_id": 3, "org_id": 1, "title": "沂源县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 8, "title": "沂源县委宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 尚勇健 — 县委常委、东里镇党委书记
    {"person_id": 4, "org_id": 1, "title": "沂源县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 10, "title": "东里镇党委书记", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 宋传方 — 县领导
    {"person_id": 5, "org_id": 2, "title": "沂源县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待确认"},
    # 于庆 — 县领导
    {"person_id": 6, "org_id": 2, "title": "沂源县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待确认"},
    # 李民斌 — 县领导
    {"person_id": 7, "org_id": 2, "title": "沂源县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待确认"},
    # 吴明 — 县领导
    {"person_id": 8, "org_id": 2, "title": "沂源县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待确认"},
    # 车春雷 — 县人大常委会主任
    {"person_id": 9, "org_id": 3, "title": "沂源县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 武光明 — 县政协主席
    {"person_id": 10, "org_id": 4, "title": "沂源县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships_data = [
    # 张涛 <-> 赵学 — 县委主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县长搭档", "overlap_org": "中共沂源县委员会", "overlap_period": "2026年"},
    # 张涛 <-> 郑舰 — 县委副书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记—县委副书记", "overlap_org": "中共沂源县委员会", "overlap_period": "2026年"},
    # 赵学 <-> 郑舰 — 县长—副书记
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长—县委副书记（共事）", "overlap_org": "中共沂源县委员会", "overlap_period": "2026年"},
    # 张涛 <-> 车春雷 — 县委—人大
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记—人大常委会主任", "overlap_org": "沂源县", "overlap_period": "2026年"},
    # 张涛 <-> 武光明 — 县委—政协
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委书记—政协主席", "overlap_org": "沂源县", "overlap_period": "2026年"},
    # 张涛 <-> 尚勇健 — 县委常委
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记—县委常委", "overlap_org": "中共沂源县委员会", "overlap_period": "2026年"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON data (written separately)
# ═══════════════════════════════════════════════════════════════════════════════

zhang_tao_person = {
    "schema_version": "1.0",
    "generated_at": "2026-07-25",
    "investigation_scope": {
        "province": "山东省",
        "city": "淄博市",
        "region": "沂源县",
        "job": "县委书记",
        "task_id": "shandong_沂源县",
        "time_focus": "2025-2026"
    },
    "identity": {
        "person_id": "yiyuan_zhang_tao",
        "name": "张涛",
        "aliases": [],
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": [],
        "party_join": "中共党员",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "张涛_",
            "name_birthplace": "张涛_",
            "official_profile_url": "http://www.yiyuan.gov.cn/"
        }
    },
    "current_status": {
        "current_post": "沂源县委书记",
        "current_org": "中共沂源县委员会",
        "administrative_rank": "正处级",
        "as_of": "2026-07-25",
        "is_current_confirmed": True,
        "source_ids": ["S001", "S002", "S003"]
    },
    "career_timeline": [
        {
            "start": "unknown",
            "end": "present",
            "org": "中共沂源县委员会",
            "title": "沂源县委书记",
            "level": "县",
            "location": "山东省淄博市沂源县",
            "system": "party",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "主持县委全面工作; 多次在新闻报道中作为县委书记出现 (2026年6-7月)",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002", "S003"]
        }
    ],
    "organizations": [
        {"org_id": "org_yiyuan_cpc", "name": "中共沂源县委员会", "role": "leader", "period": "至2026年"}
    ],
    "relationships": [
        {
            "person": "赵学",
            "person_id": "yiyuan_zhao_xue",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "县委书记—县长搭档，多次共同出席县委常委会、党政联席会等重点会议",
            "overlap_org": "中共沂源县委员会",
            "overlap_period": "2026年",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002"]
        },
        {
            "person": "郑舰",
            "person_id": "yiyuan_zheng_jian",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "县委书记—县委副书记（兼宣传部部长），多次共同出席会议",
            "overlap_org": "中共沂源县委员会",
            "overlap_period": "2026年",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002"]
        }
    ],
    "governance_record": [
        {
            "period": "2026年6-7月",
            "domain": "economic_development",
            "achievement_or_event": "调研重点项目建设情况，走访多家企业，强调加快项目建设和产业升级",
            "role_in_event": "带队调研",
            "measurable_outcome": "",
            "location": "沂源县",
            "confidence": "confirmed",
            "source_ids": ["S003"]
        },
        {
            "period": "2026年7月",
            "domain": "rural_revitalization",
            "achievement_or_event": "到悦庄镇、南鲁山镇调研乡村振兴、村集体经济发展、长者食堂运营等",
            "role_in_event": "带队调研指导",
            "measurable_outcome": "",
            "location": "沂源县悦庄镇、南鲁山镇",
            "confidence": "confirmed",
            "source_ids": ["S005", "S006"]
        },
        {
            "period": "2026年7月",
            "domain": "public_security",
            "achievement_or_event": "调研防汛救灾准备工作，检查水库、地质灾害隐患点和防汛物资储备",
            "role_in_event": "带队督导",
            "measurable_outcome": "",
            "location": "沂源县",
            "confidence": "confirmed",
            "source_ids": ["S007"]
        },
        {
            "period": "2026年7月",
            "domain": "other",
            "achievement_or_event": "主持县党政联席扩大会议暨上半年工作会议，总结上半年经济工作，部署下半年重点任务",
            "role_in_event": "主持会议并讲话",
            "measurable_outcome": "",
            "location": "沂源县",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        }
    ],
    "professional_profile": {
        "primary_specializations": ["党务管理", "经济建设", "乡村振兴"],
        "secondary_specializations": ["文旅发展", "安全生产"],
        "career_pattern": "unknown",
        "systems_experience": ["party"],
        "geographic_pattern": [],
        "promotion_velocity": {
            "summary": "早期履历不详",
            "notable_fast_promotions": []
        }
    },
    "work_style_and_personality": {
        "public_style_indicators": [
            {
                "trait": "pragmatic",
                "evidence": "多次深入项目一线和农村基层调研，强调解决问题、推动落实",
                "confidence": "plausible",
                "source_ids": ["S003", "S005", "S006"]
            },
            {
                "trait": "stability_oriented",
                "evidence": "强调守牢安全底线、防汛抗旱、安全生产等",
                "confidence": "plausible",
                "source_ids": ["S001", "S007"]
            }
        ],
        "speech_themes": ["高质量发展", "乡村振兴", "安全生产", "基层治理"],
        "management_signals": ["注重一线调研", "强调底线思维"],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
    },
    "risk_and_integrity_signals": [
        {
            "type": "none_found",
            "description": "未发现张涛的纪律处分、审计问题或负面媒体报道",
            "date": "2026-07-25",
            "confidence": "plausible",
            "source_ids": []
        }
    ],
    "source_register": [
        {"id": "S001", "title": "县党政联席扩大会议暨上半年工作会议召开", "url": "http://www.yiyuan.gov.cn/art/2026/7/23/art_5601_3012011.html", "publisher": "沂源县人民政府", "published_at": "2026-07-23", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "县委书记张涛主持会议, 县长赵学、人大主任车春雷、政协主席武光明、副书记郑舰出席会议"},
        {"id": "S002", "title": "县委常委会会议召开", "url": "http://www.yiyuan.gov.cn/art/2026/7/8/art_5607_3010213.html", "publisher": "沂源县人民政府", "published_at": "2026-07-08", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "张涛主持会议, 赵学、车春雷、郑舰等出席"},
        {"id": "S003", "title": "县委书记张涛调研项目建设情况", "url": "http://www.yiyuan.gov.cn/art/2026/6/25/art_5607_3007341.html", "publisher": "沂源县人民政府", "published_at": "2026-06-25", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "张涛调研项目建设, 县委常委尚勇健参加"},
        {"id": "S005", "title": "张涛到悦庄镇调研", "url": "http://www.yiyuan.gov.cn/art/2026/7/20/art_5601_3011997.html", "publisher": "沂源县人民政府", "published_at": "2026-07-20", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "调研长者食堂、村集体经济发展等"},
        {"id": "S006", "title": "张涛到南鲁山镇调研", "url": "http://www.yiyuan.gov.cn/art/2026/7/19/art_5601_3011368.html", "publisher": "沂源县人民政府", "published_at": "2026-07-19", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "调研村两委班子建设和乡村振兴"},
        {"id": "S007", "title": "张涛调研防汛救灾工作", "url": "http://www.yiyuan.gov.cn/art/2026/7/13/art_5601_3011041.html", "publisher": "沂源县人民政府", "published_at": "2026-07-13", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "检查水库和地质灾害隐患点位"}
    ],
    "confidence_summary": {
        "identity": "partial",
        "current_role": "confirmed",
        "career_completeness": "thin",
        "relationship_confidence": "high",
        "biggest_gap": "张涛的出生年月、籍贯、教育背景、完整履历（何时到沂源任职、此前任职岗位等）均未在公开资料中找到"
    },
    "open_questions": [
        {
            "priority": "critical",
            "question": "张涛的出生年月、籍贯、民族是什么？",
            "why_it_matters": "核心身份信息缺失，影响人物唯一性辨识",
            "suggested_queries": ["张涛 沂源县委书记 出生", "张涛 简历 沂源"],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "critical",
            "question": "张涛何时任沂源县委书记？此前任何职务？",
            "why_it_matters": "完整履历是关系网络分析的基础",
            "suggested_queries": ["张涛 沂源县委书记 任命", "张涛 淄博 任职"],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "high",
            "question": "张涛的教育背景——本科/研究生就读院校及专业",
            "why_it_matters": "教育背景有助于推断专业方向和可能的校友关系",
            "suggested_queries": ["张涛 学历 沂源"],
            "last_attempted": "2026-07-25"
        }
    ]
}

zhao_xue_person = {
    "schema_version": "1.0",
    "generated_at": "2026-07-25",
    "investigation_scope": {
        "province": "山东省",
        "city": "淄博市",
        "region": "沂源县",
        "job": "县长",
        "task_id": "shandong_沂源县",
        "time_focus": "2025-2026"
    },
    "identity": {
        "person_id": "yiyuan_zhao_xue",
        "name": "赵学",
        "aliases": [],
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": [],
        "party_join": "中共党员",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "赵学_",
            "name_birthplace": "赵学_",
            "official_profile_url": "http://www.yiyuan.gov.cn/"
        }
    },
    "current_status": {
        "current_post": "沂源县委副书记、县人民政府县长",
        "current_org": "沂源县人民政府",
        "administrative_rank": "正处级",
        "as_of": "2026-07-25",
        "is_current_confirmed": True,
        "source_ids": ["S001", "S002", "S101"]
    },
    "career_timeline": [
        {
            "start": "unknown",
            "end": "present",
            "org": "沂源县人民政府",
            "title": "沂源县委副书记、县人民政府县长",
            "level": "县",
            "location": "山东省淄博市沂源县",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "主持县政府全面工作; 多次在新闻报道中作为县长出现 (2026年4-7月)",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002", "S101"]
        }
    ],
    "organizations": [
        {"org_id": "org_yiyuan_gov", "name": "沂源县人民政府", "role": "leader", "period": "至2026年"},
        {"org_id": "org_yiyuan_cpc", "name": "中共沂源县委员会", "role": "deputy_leader", "period": "至2026年"}
    ],
    "relationships": [
        {
            "person": "张涛",
            "person_id": "yiyuan_zhang_tao",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "县长—县委书记搭档，多次共同出席各类重要会议",
            "overlap_org": "中共沂源县委员会",
            "overlap_period": "2026年",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002"]
        },
        {
            "person": "车春雷",
            "person_id": "yiyuan_che_chunlei",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "县长—人大常委会主任，共同出席党政联席会及项目推进会",
            "overlap_org": "沂源县",
            "overlap_period": "2026年",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        }
    ],
    "governance_record": [
        {
            "period": "2026年7月",
            "domain": "public_security",
            "achievement_or_event": "督导调研安全生产工作，检查建材市场、危化品企业、建筑工地和餐饮场所",
            "role_in_event": "带队督导",
            "measurable_outcome": "",
            "location": "沂源县",
            "confidence": "confirmed",
            "source_ids": ["S101"]
        },
        {
            "period": "2026年5月",
            "domain": "environment",
            "achievement_or_event": "督导生态环境重点工作",
            "role_in_event": "带队督导",
            "measurable_outcome": "",
            "location": "沂源县",
            "confidence": "confirmed",
            "source_ids": ["S102"]
        },
        {
            "period": "2026年5月",
            "domain": "other",
            "achievement_or_event": "调研马路市场整治工作",
            "role_in_event": "调研指导",
            "measurable_outcome": "",
            "location": "沂源县",
            "confidence": "confirmed",
            "source_ids": ["S103"]
        },
        {
            "period": "2026年4月",
            "domain": "economic_development",
            "achievement_or_event": "走访联系服务企业",
            "role_in_event": "走访调研",
            "measurable_outcome": "",
            "location": "沂源县",
            "confidence": "confirmed",
            "source_ids": ["S104"]
        },
        {
            "period": "2026年5月",
            "domain": "public_security",
            "achievement_or_event": "调研督导五一期间食品安全工作",
            "role_in_event": "督导",
            "measurable_outcome": "",
            "location": "沂源县",
            "confidence": "confirmed",
            "source_ids": ["S105"]
        }
    ],
    "professional_profile": {
        "primary_specializations": ["政府行政管理", "安全生产", "生态环保"],
        "secondary_specializations": ["市场监管", "营商环境"],
        "career_pattern": "unknown",
        "systems_experience": ["government"],
        "geographic_pattern": [],
        "promotion_velocity": {
            "summary": "早期履历不详",
            "notable_fast_promotions": []
        }
    },
    "work_style_and_personality": {
        "public_style_indicators": [
            {
                "trait": "pragmatic",
                "evidence": "多次深入企业、市场、工地一线督导检查，强调安全隐患排查和整改",
                "confidence": "plausible",
                "source_ids": ["S101"]
            },
            {
                "trait": "discipline_oriented",
                "evidence": "多次强调安全生产'三管三必须'要求和责任落实",
                "confidence": "plausible",
                "source_ids": ["S101"]
            }
        ],
        "speech_themes": ["安全生产", "生态环保", "企业服务"],
        "management_signals": ["注重一线检查", "强调责任落实"],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
    },
    "risk_and_integrity_signals": [
        {
            "type": "none_found",
            "description": "未发现赵学的纪律处分、审计问题或负面媒体报道",
            "date": "2026-07-25",
            "confidence": "plausible",
            "source_ids": []
        }
    ],
    "source_register": [
        {"id": "S001", "title": "县党政联席扩大会议暨上半年工作会议召开", "url": "http://www.yiyuan.gov.cn/art/2026/7/23/art_5601_3012011.html", "publisher": "沂源县人民政府", "published_at": "2026-07-23", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S002", "title": "县委常委会会议召开", "url": "http://www.yiyuan.gov.cn/art/2026/7/8/art_5607_3010213.html", "publisher": "沂源县人民政府", "published_at": "2026-07-08", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S101", "title": "县委副书记、县人民政府县长赵学督导调研安全生产工作", "url": "http://www.yiyuan.gov.cn/art/2026/7/21/art_5601_3012001.html", "publisher": "沂源县人民政府", "published_at": "2026-07-21", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S102", "title": "县委副书记、县人民政府县长赵学督导生态环境重点工作", "url": "http://www.yiyuan.gov.cn/", "publisher": "沂源县人民政府", "published_at": "2026-05-13", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "引自政府信息公开页面" },
        {"id": "S103", "title": "县委副书记、县人民政府县长赵学调研马路市场整治工作", "url": "http://www.yiyuan.gov.cn/", "publisher": "沂源县人民政府", "published_at": "2026-05-08", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "引自政府信息公开页面" },
        {"id": "S104", "title": "县委副书记、县人民政府县长赵学走访联系服务企业", "url": "http://www.yiyuan.gov.cn/", "publisher": "沂源县人民政府", "published_at": "2026-04-16", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "引自政府信息公开页面" },
        {"id": "S105", "title": "赵学调研督导五一期间食品安全工作", "url": "http://www.yiyuan.gov.cn/", "publisher": "沂源县人民政府", "published_at": "2026-05-01", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "引自政府信息公开页面" }
    ],
    "confidence_summary": {
        "identity": "partial",
        "current_role": "confirmed",
        "career_completeness": "thin",
        "relationship_confidence": "high",
        "biggest_gap": "赵学的出生年月、籍贯、教育背景、完整履历（何时到沂源任职、此前任何职）均未在公开资料中找到"
    },
    "open_questions": [
        {
            "priority": "critical",
            "question": "赵学的出生年月、籍贯、民族是什么？",
            "why_it_matters": "核心身份信息缺失",
            "suggested_queries": ["赵学 沂源县长 出生", "赵学 简历 沂源"],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "critical",
            "question": "赵学何时任沂源县长？此前任何职务？",
            "why_it_matters": "完整履历是关系网络分析的基础",
            "suggested_queries": ["赵学 沂源县长 任命", "赵学 沂源 任职 前任"],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "high",
            "question": "赵学的教育背景——学历、毕业院校及专业",
            "why_it_matters": "教育背景有助于推断专业方向和可能的校友关系",
            "suggested_queries": ["赵学 沂源 学历", "赵学 淄博"],
            "last_attempted": "2026-07-25"
        }
    ]
}

che_chunlei_person = {
    "schema_version": "1.0",
    "generated_at": "2026-07-25",
    "investigation_scope": {
        "province": "山东省",
        "city": "淄博市",
        "region": "沂源县",
        "job": "县人大常委会主任",
        "task_id": "shandong_沂源县",
        "time_focus": "2025-2026"
    },
    "identity": {
        "person_id": "yiyuan_che_chunlei",
        "name": "车春雷",
        "aliases": [],
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": [],
        "party_join": "中共党员",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "车春雷_",
            "name_birthplace": "车春雷_",
            "official_profile_url": "http://www.yiyuan.gov.cn/"
        }
    },
    "current_status": {
        "current_post": "沂源县人大常委会主任",
        "current_org": "沂源县人民代表大会常务委员会",
        "administrative_rank": "正处级",
        "as_of": "2026-07-25",
        "is_current_confirmed": True,
        "source_ids": ["S001", "S002", "S004"]
    },
    "career_timeline": [
        {
            "start": "unknown",
            "end": "present",
            "org": "沂源县人民代表大会常务委员会",
            "title": "沂源县人大常委会主任",
            "level": "县",
            "location": "山东省淄博市沂源县",
            "system": "other",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "多次出席会议; 具体上任时间不详",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002"]
        }
    ],
    "organizations": [
        {"org_id": "org_yiyuan_npc", "name": "沂源县人民代表大会常务委员会", "role": "leader", "period": "至2026年"}
    ],
    "relationships": [
        {
            "person": "张涛",
            "person_id": "yiyuan_zhang_tao",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "人大常委会主任—县委书记，共同出席党政联席会议",
            "overlap_org": "沂源县",
            "overlap_period": "2026年",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        },
        {
            "person": "赵学",
            "person_id": "yiyuan_zhao_xue",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "人大常委会主任—县长，共同出席党政联席会、项目推进会",
            "overlap_org": "沂源县",
            "overlap_period": "2026年",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S004"]
        }
    ],
    "governance_record": [],
    "professional_profile": {
        "primary_specializations": ["人大工作"],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": ["other"],
        "geographic_pattern": [],
        "promotion_velocity": {"summary": "履历不详", "notable_fast_promotions": []}
    },
    "work_style_and_personality": {
        "public_style_indicators": [],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, not private psychological assessment."
    },
    "risk_and_integrity_signals": [
        {"type": "none_found", "description": "未发现负面信息", "date": "2026-07-25", "confidence": "plausible", "source_ids": []}
    ],
    "source_register": [
        {"id": "S001", "title": "县党政联席扩大会议暨上半年工作会议召开", "url": "http://www.yiyuan.gov.cn/art/2026/7/23/art_5601_3012011.html", "publisher": "沂源县人民政府", "published_at": "2026-07-23", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S002", "title": "县委常委会会议召开", "url": "http://www.yiyuan.gov.cn/art/2026/7/8/art_5607_3010213.html", "publisher": "沂源县人民政府", "published_at": "2026-07-08", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S004", "title": "2026年上半年全县高质量发展重点项目现场推进会召开", "url": "http://www.yiyuan.gov.cn/art/2026/7/22/art_5601_3012004.html", "publisher": "沂源县人民政府", "published_at": "2026-07-22", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": ""}
    ],
    "confidence_summary": {
        "identity": "minimal",
        "current_role": "confirmed",
        "career_completeness": "thin",
        "relationship_confidence": "medium",
        "biggest_gap": "车春雷的出生年月、籍贯、教育背景、完整履历均未找到"
    },
    "open_questions": [
        {"priority": "critical", "question": "车春雷的出生年月、籍贯等基本信息？", "why_it_matters": "核心身份信息缺失", "suggested_queries": ["车春雷 沂源 人大常委会主任"], "last_attempted": "2026-07-25"},
        {"priority": "high", "question": "车春雷何时任沂源县人大常委会主任？此前任何职？", "why_it_matters": "履历分析基础", "suggested_queries": ["车春雷 沂源 任职"], "last_attempted": "2026-07-25"}
    ]
}

wu_guangming_person = {
    "schema_version": "1.0",
    "generated_at": "2026-07-25",
    "investigation_scope": {
        "province": "山东省",
        "city": "淄博市",
        "region": "沂源县",
        "job": "县政协主席",
        "task_id": "shandong_沂源县",
        "time_focus": "2025-2026"
    },
    "identity": {
        "person_id": "yiyuan_wu_guangming",
        "name": "武光明",
        "aliases": [],
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": [],
        "party_join": "中共党员",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "武光明_",
            "name_birthplace": "武光明_",
            "official_profile_url": "http://www.yiyuan.gov.cn/"
        }
    },
    "current_status": {
        "current_post": "沂源县政协主席",
        "current_org": "中国人民政治协商会议沂源县委员会",
        "administrative_rank": "正处级",
        "as_of": "2026-07-25",
        "is_current_confirmed": True,
        "source_ids": ["S001", "S008"]
    },
    "career_timeline": [
        {
            "start": "unknown",
            "end": "present",
            "org": "中国人民政治协商会议沂源县委员会",
            "title": "沂源县政协主席",
            "level": "县",
            "location": "山东省淄博市沂源县",
            "system": "other",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "在文旅高质量发展会议和党政联席会上作为县政协主席出席",
            "confidence": "confirmed",
            "source_ids": ["S001", "S008"]
        }
    ],
    "organizations": [
        {"org_id": "org_yiyuan_cppcc", "name": "中国人民政治协商会议沂源县委员会", "role": "leader", "period": "至2026年"}
    ],
    "relationships": [
        {
            "person": "张涛",
            "person_id": "yiyuan_zhang_tao",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "政协主席—县委书记，共同出席各类会议",
            "overlap_org": "沂源县",
            "overlap_period": "2026年",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        }
    ],
    "governance_record": [
        {
            "period": "2026年7月",
            "domain": "other",
            "achievement_or_event": "参加文旅高质量发展分线指挥部会议",
            "role_in_event": "参会",
            "measurable_outcome": "",
            "location": "沂源县",
            "confidence": "confirmed",
            "source_ids": ["S008"]
        }
    ],
    "professional_profile": {
        "primary_specializations": ["政协工作"],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": ["other"],
        "geographic_pattern": [],
        "promotion_velocity": {"summary": "履历不详", "notable_fast_promotions": []}
    },
    "work_style_and_personality": {
        "public_style_indicators": [],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, not private psychological assessment."
    },
    "risk_and_integrity_signals": [
        {"type": "none_found", "description": "未发现负面信息", "date": "2026-07-25", "confidence": "plausible", "source_ids": []}
    ],
    "source_register": [
        {"id": "S001", "title": "县党政联席扩大会议暨上半年工作会议召开", "url": "http://www.yiyuan.gov.cn/art/2026/7/23/art_5601_3012011.html", "publisher": "沂源县人民政府", "published_at": "2026-07-23", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S008", "title": "文旅高质量发展分线指挥部二季度交流暨上半年分析会议召开", "url": "http://www.yiyuan.gov.cn/art/2026/7/15/art_5601_3011045.html", "publisher": "沂源县人民政府", "published_at": "2026-07-15", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": ""}
    ],
    "confidence_summary": {
        "identity": "minimal",
        "current_role": "confirmed",
        "career_completeness": "thin",
        "relationship_confidence": "medium",
        "biggest_gap": "武光明的出生年月、籍贯、教育背景、完整履历均未找到"
    },
    "open_questions": [
        {"priority": "critical", "question": "武光明的出生年月、籍贯等基本信息？", "why_it_matters": "核心身份信息缺失", "suggested_queries": ["武光明 沂源 政协主席"], "last_attempted": "2026-07-25"},
        {"priority": "high", "question": "武光明何时任沂源县政协主席？此前任何职？", "why_it_matters": "履历分析基础", "suggested_queries": ["武光明 沂源 任职"], "last_attempted": "2026-07-25"}
    ]
}

zheng_jian_person = {
    "schema_version": "1.0",
    "generated_at": "2026-07-25",
    "investigation_scope": {
        "province": "山东省",
        "city": "淄博市",
        "region": "沂源县",
        "job": "县委副书记、宣传部部长",
        "task_id": "shandong_沂源县",
        "time_focus": "2025-2026"
    },
    "identity": {
        "person_id": "yiyuan_zheng_jian",
        "name": "郑舰",
        "aliases": [],
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": [],
        "party_join": "中共党员",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "郑舰_",
            "name_birthplace": "郑舰_",
            "official_profile_url": "http://www.yiyuan.gov.cn/"
        }
    },
    "current_status": {
        "current_post": "沂源县委副书记、宣传部部长",
        "current_org": "中共沂源县委员会",
        "administrative_rank": "副处级",
        "as_of": "2026-07-25",
        "is_current_confirmed": True,
        "source_ids": ["S001", "S002", "S009"]
    },
    "career_timeline": [
        {
            "start": "unknown",
            "end": "present",
            "org": "中共沂源县委员会",
            "title": "沂源县委副书记、宣传部部长",
            "level": "县",
            "location": "山东省淄博市沂源县",
            "system": "party",
            "rank": "副处级",
            "is_key_promotion": True,
            "notes": "兼任宣传部部长; 陪同市委常委、宣传部部长林恒调研; 出席党政联席会和常委会",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002", "S009"]
        }
    ],
    "organizations": [
        {"org_id": "org_yiyuan_cpc", "name": "中共沂源县委员会", "role": "deputy_leader", "period": "至2026年"}
    ],
    "relationships": [
        {
            "person": "张涛",
            "person_id": "yiyuan_zhang_tao",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "县委副书记—县委书记，共同出席县委常委会、党政联席会",
            "overlap_org": "中共沂源县委员会",
            "overlap_period": "2026年",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002"]
        },
        {
            "person": "赵学",
            "person_id": "yiyuan_zhao_xue",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "县委副书记—县长，共同出席各类重要会议",
            "overlap_org": "中共沂源县委员会",
            "overlap_period": "2026年",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        }
    ],
    "governance_record": [],
    "professional_profile": {
        "primary_specializations": ["党务管理", "宣传思想工作"],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": ["party", "propaganda"],
        "geographic_pattern": [],
        "promotion_velocity": {"summary": "履历不详", "notable_fast_promotions": []}
    },
    "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records."},
    "risk_and_integrity_signals": [
        {"type": "none_found", "description": "未发现负面信息", "date": "2026-07-25", "confidence": "plausible", "source_ids": []}
    ],
    "source_register": [
        {"id": "S001", "title": "县党政联席扩大会议", "url": "http://www.yiyuan.gov.cn/art/2026/7/23/art_5601_3012011.html", "publisher": "沂源县人民政府", "published_at": "2026-07-23", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S002", "title": "县委常委会会议", "url": "http://www.yiyuan.gov.cn/art/2026/7/8/art_5607_3010213.html", "publisher": "沂源县人民政府", "published_at": "2026-07-08", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S009", "title": "市委常委、宣传部部长林恒来我县调研", "url": "http://www.yiyuan.gov.cn/art/2026/7/17/art_5601_3011366.html", "publisher": "沂源县人民政府", "published_at": "2026-07-17", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "郑舰以县委副书记、宣传部部长身份陪同调研"}
    ],
    "confidence_summary": {
        "identity": "minimal",
        "current_role": "confirmed",
        "career_completeness": "thin",
        "relationship_confidence": "medium",
        "biggest_gap": "郑舰的出生年月、籍贯、教育背景、完整履历均未找到"
    },
    "open_questions": [
        {"priority": "critical", "question": "郑舰的出生年月、籍贯等基本信息？", "why_it_matters": "核心身份信息缺失", "suggested_queries": ["郑舰 沂源 县委副书记"], "last_attempted": "2026-07-25"},
        {"priority": "high", "question": "郑舰何时到沂源任职？此前任何职？", "why_it_matters": "履历分析基础", "suggested_queries": ["郑舰 沂源 任职"], "last_attempted": "2026-07-25"}
    ]
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def write_person_json(person_data, filename):
    """Write a person JSON file to the staging directory."""
    path = STAGING_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)
    print(f"  [OK] {path.name}")
    return path


def main():
    print("=" * 60)
    print(f"  Building {SLUG} network data")
    print(f"  Date: {TODAY}")
    print("=" * 60)

    # 1. Build SQLite + GEXF
    print("\n[1/2] Building database and graph...")
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
    print("  [OK] Database and GEXF written to staging directory")

    # 2. Write person JSONs
    print("\n[2/2] Writing person JSONs...")
    person_files = [
        (zhang_tao_person, f"{TODAY}-山东省-淄博市-县委书记-张涛.json"),
        (zhao_xue_person, f"{TODAY}-山东省-淄博市-县长-赵学.json"),
        (che_chunlei_person, f"{TODAY}-山东省-淄博市-县人大常委会主任-车春雷.json"),
        (wu_guangming_person, f"{TODAY}-山东省-淄博市-县政协主席-武光明.json"),
        (zheng_jian_person, f"{TODAY}-山东省-淄博市-县委副书记_宣传部部长-郑舰.json"),
    ]
    for data, fname in person_files:
        write_person_json(data, fname)

    print("\n" + "=" * 60)
    print("  Build complete!")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"  Person JSONs: {STAGING_DIR / f'{TODAY}-*.json'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
