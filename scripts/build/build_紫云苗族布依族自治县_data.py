#!/usr/bin/env python3
"""紫云苗族布依族自治县（安顺市）领导班子关系网络数据生成脚本。

Targets: 县委书记 黄浩洋, 县长 杨坚
Data as of: 2026-07-23
Sources: 紫云县人民政府官网 (www.gzzy.gov.cn), 安顺市人民政府官网 (www.anshun.gov.cn)
"""

import json
import os
import sqlite3
from datetime import datetime

TASK_ID = "guizhou_紫云苗族布依族自治县"
SLUG = "紫云苗族布依族自治县"
AS_OF = "2026-07-23"
PROVINCE = "贵州省"
PARENT_CITY = "安顺市"

BASE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "data/tmp/guizhou_紫云苗族布依族自治县"
_BASE_OVERRIDE = os.environ.get("ZIYUN_BASE")
if _BASE_OVERRIDE:
    BASE = _BASE_OVERRIDE

DB_PATH = os.path.join(BASE, "紫云苗族布依族自治县_network.db")
GEXF_PATH = os.path.join(BASE, "紫云苗族布依族自治县_network.gexf")
PERSONS_DIR = os.path.join(BASE, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────

persons = [
    # 1 - 县委书记
    {
        "id": 1,
        "name": "黄浩洋",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1980年5月",
        "birthplace": "贵州镇宁",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "紫云苗族布依族自治县委书记",
        "current_org": "中共紫云苗族布依族自治县委员会",
        "source": "http://www.gzzy.gov.cn/xwdt/ldhd/202607/t20260703_90582116.html",
    },
    # 2 - 县长
    {
        "id": 2,
        "name": "杨坚",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1979年11月",
        "birthplace": "",
        "education": "大学，理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "紫云苗族布依族自治县委副书记、县人民政府县长、党组书记",
        "current_org": "紫云苗族布依族自治县人民政府",
        "source": "http://www.gzzy.gov.cn/zwgk/ldzc1/202503/t20250313_87158572.html",
    },
    # 3 - 县委副书记
    {
        "id": 3,
        "name": "李茂强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "紫云苗族布依族自治县委副书记",
        "current_org": "中共紫云苗族布依族自治县委员会",
        "source": "http://www.gzzy.gov.cn/xwdt/ldhd/202607/t20260703_90582116.html",
    },
    # 4 - 县人大常委会主任
    {
        "id": 4,
        "name": "王俐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "紫云苗族布依族自治县人大常委会主任",
        "current_org": "紫云苗族布依族自治县人大常委会",
        "source": "http://www.gzzy.gov.cn/xwdt/ldhd/202607/t20260703_90582116.html",
    },
    # 5 - 县政协主席
    {
        "id": 5,
        "name": "吴开林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "紫云苗族布依族自治县政协主席",
        "current_org": "中国人民政治协商会议紫云苗族布依族自治县委员会",
        "source": "http://www.gzzy.gov.cn/xwdt/ldhd/202607/t20260703_90582116.html",
    },
    # 6 - 常务副县长
    {
        "id": 6,
        "name": "龙海斌",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1984年7月",
        "birthplace": "",
        "education": "大学，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "紫云苗族布依族自治县委常委、常务副县长、党组副书记",
        "current_org": "紫云苗族布依族自治县人民政府",
        "source": "http://www.gzzy.gov.cn/zwgk/ldzc1/202503/t20250313_87158737.html",
    },
    # 7 - 县委常委、副县长
    {
        "id": 7,
        "name": "高启然",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年5月",
        "birthplace": "",
        "education": "研究生，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "紫云苗族布依族自治县委常委、县人民政府副县长",
        "current_org": "紫云苗族布依族自治县人民政府",
        "source": "http://www.gzzy.gov.cn/zwgk/ldzc1/202509/t20250926_88655575.html",
    },
    # 8 - 县委常委、副县长（挂职）
    {
        "id": 8,
        "name": "冯恒文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年8月",
        "birthplace": "",
        "education": "研究生，工程管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "紫云苗族布依族自治县委常委、副县长（挂职）",
        "current_org": "紫云苗族布依族自治县人民政府",
        "source": "http://www.gzzy.gov.cn/zwgk/ldzc1/202503/t20250313_87159489.html",
    },
    # 9 - 县委常委、副县长（挂职，航空工业）
    {
        "id": 9,
        "name": "姬冠宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年2月",
        "birthplace": "",
        "education": "大学，管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "紫云苗族布依族自治县委常委、副县长（挂职）",
        "current_org": "紫云苗族布依族自治县人民政府",
        "source": "http://www.gzzy.gov.cn/zwgk/ldzc1/202507/t20250703_88226255.html",
    },
    # 10 - 副县长
    {
        "id": 10,
        "name": "齐松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年1月",
        "birthplace": "",
        "education": "大学",
        "party_join": "农工党",
        "work_start": "",
        "current_post": "紫云苗族布依族自治县人民政府副县长",
        "current_org": "紫云苗族布依族自治县人民政府",
        "source": "http://www.gzzy.gov.cn/zwgk/ldzc1/202503/t20250313_87159519.html",
    },
    # 11 - 副县长
    {
        "id": 11,
        "name": "陈凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年10月",
        "birthplace": "",
        "education": "省委党校大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "紫云苗族布依族自治县人民政府副县长",
        "current_org": "紫云苗族布依族自治县人民政府",
        "source": "http://www.gzzy.gov.cn/zwgk/ldzc1/202503/t20250313_87159529.html",
    },
    # 12 - 副县长、县公安局局长
    {
        "id": 12,
        "name": "李洪溪",
        "gender": "男",
        "ethnicity": "仡佬族",
        "birth": "1977年9月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "紫云苗族布依族自治县人民政府副县长、县公安局局长",
        "current_org": "紫云苗族布依族自治县人民政府",
        "source": "http://www.gzzy.gov.cn/zwgk/ldzc1/202503/t20250313_87159627.html",
    },
    # 13 - 副县长（女）
    {
        "id": 13,
        "name": "汪灵",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986年7月",
        "birthplace": "",
        "education": "大学，历史学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "紫云苗族布依族自治县人民政府副县长",
        "current_org": "紫云苗族布依族自治县人民政府",
        "source": "http://www.gzzy.gov.cn/zwgk/ldzc1/202503/t20250313_87159724.html",
    },
    # 14 - 前任县委书记
    {
        "id": 14,
        "name": "张天勇",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1966年6月",
        "birthplace": "贵州平坝",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安顺市生态移民局党组成员、副局长（正县长级）",
        "current_org": "安顺市生态移民局",
        "source": "https://baike.baidu.com/item/%E5%BC%A0%E5%A4%A9%E5%8B%87/23651443",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共紫云苗族布依族自治县委员会", "type": "党委", "level": "县", "parent": "中共安顺市委员会", "location": "紫云苗族布依族自治县"},
    {"id": 2, "name": "紫云苗族布依族自治县人民政府", "type": "政府", "level": "县", "parent": "安顺市人民政府", "location": "紫云苗族布依族自治县"},
    {"id": 3, "name": "紫云苗族布依族自治县人大常委会", "type": "人大", "level": "县", "parent": "", "location": "紫云苗族布依族自治县"},
    {"id": 4, "name": "中国人民政治协商会议紫云苗族布依族自治县委员会", "type": "政协", "level": "县", "parent": "", "location": "紫云苗族布依族自治县"},
    {"id": 5, "name": "紫云苗族布依族自治县公安局", "type": "政府", "level": "县", "parent": "紫云苗族布依族自治县人民政府", "location": "紫云苗族布依族自治县"},
    {"id": 6, "name": "安顺市生态移民局", "type": "政府", "level": "市", "parent": "安顺市人民政府", "location": "安顺市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # 黄浩洋
    {"person_id": 1, "org_id": 1, "title": "紫云苗族布依族自治县委书记", "start_date": "2021年6月", "end_date": "", "rank": "县处级正职", "note": "2021年6月起任紫云县委书记"},
    {"person_id": 1, "org_id": 2, "title": "紫云苗族布依族自治县委副书记、县长", "start_date": "2019年8月", "end_date": "2021年6月", "rank": "县处级正职", "note": "2019年8月任代理县长，9月正式当选"},
    # 杨坚
    {"person_id": 2, "org_id": 2, "title": "紫云苗族布依族自治县委副书记、县长、党组书记", "start_date": "2021年7月", "end_date": "", "rank": "县处级正职", "note": ""},
    # 李茂强
    {"person_id": 3, "org_id": 1, "title": "紫云苗族布依族自治县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 王俐
    {"person_id": 4, "org_id": 3, "title": "紫云苗族布依族自治县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 吴开林
    {"person_id": 5, "org_id": 4, "title": "紫云苗族布依族自治县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 龙海斌
    {"person_id": 6, "org_id": 2, "title": "紫云苗族布依族自治县委常委、常务副县长、党组副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 高启然
    {"person_id": 7, "org_id": 2, "title": "紫云苗族布依族自治县委常委、副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 冯恒文
    {"person_id": 8, "org_id": 2, "title": "紫云苗族布依族自治县委常委、副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "挂职干部"},
    # 姬冠宇
    {"person_id": 9, "org_id": 2, "title": "紫云苗族布依族自治县委常委、副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "航空工业集团挂职"},
    # 齐松
    {"person_id": 10, "org_id": 2, "title": "紫云苗族布依族自治县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "农工党"},
    # 陈凯
    {"person_id": 11, "org_id": 2, "title": "紫云苗族布依族自治县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 李洪溪
    {"person_id": 12, "org_id": 2, "title": "紫云苗族布依族自治县人民政府副县长、县公安局局长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 5, "title": "紫云苗族布依族自治县公安局局长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 汪灵
    {"person_id": 13, "org_id": 2, "title": "紫云苗族布依族自治县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 张天勇
    {"person_id": 14, "org_id": 1, "title": "紫云苗族布依族自治县委书记", "start_date": "2016年2月", "end_date": "2019年8月", "rank": "县处级正职", "note": "前任县委书记"},
    {"person_id": 14, "org_id": 6, "title": "安顺市生态移民局党组成员、副局长（正县长级）", "start_date": "2019年8月", "end_date": "", "rank": "县处级正职", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 黄浩洋 → 杨坚 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "黄浩洋（书记）与杨坚（县长）为紫云县党政正职搭档关系", "overlap_org": "紫云苗族布依族自治县", "overlap_period": "2021年至今"},
    # 黄浩洋 → 张天勇 (前后任书记)
    {"person_a": 1, "person_b": 14, "type": "predecessor_successor", "context": "张天勇（2016.02-2019.08任书记）→ 黄浩洋（2021.06起任书记），中间可能还有一位书记", "overlap_org": "中共紫云苗族布依族自治县委员会", "overlap_period": "2016-2021"},
    # 黄浩洋 → 龙海斌 (上下级)
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "黄浩洋（书记）与龙海斌（常务副县长）为县委常委会搭档", "overlap_org": "中共紫云苗族布依族自治县委员会", "overlap_period": ""},
    # 黄浩洋 → 李茂强 (上下级)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "黄浩洋（书记）与李茂强（副书记）为县委班子搭档", "overlap_org": "中共紫云苗族布依族自治县委员会", "overlap_period": ""},
    # 杨坚 → 龙海斌 (正副手)
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "杨坚（县长）与龙海斌（常务副县长）为县政府正副手搭档", "overlap_org": "紫云苗族布依族自治县人民政府", "overlap_period": ""},
    # 高启然 → 龙海斌 (县委常委同事)
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "同任紫云县委常委", "overlap_org": "中共紫云苗族布依族自治县委常委会", "overlap_period": ""},
    # 冯恒文 → 汪灵 (东西部协作搭档)
    {"person_a": 8, "person_b": 13, "type": "overlap", "context": "共同负责东西部协作工作（冯恒文挂职干部）", "overlap_org": "紫云苗族布依族自治县人民政府", "overlap_period": ""},
    # 李洪溪 → 杨坚 (公安-政府正职)
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "李洪溪（副县长兼公安局长）受杨坚（县长）领导", "overlap_org": "紫云苗族布依族自治县人民政府", "overlap_period": ""},
]

# ── Person JSON files ─────────────────────────────────────────────────────────

PERSON_JSONS = [
    {
        "filename": f"{AS_OF}-{PROVINCE}-{PARENT_CITY}-县委书记-黄浩洋.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": "紫云苗族布依族自治县",
                "job": "县委书记",
                "task_id": TASK_ID,
                "time_focus": "2019-2026"
            },
            "identity": {
                "person_id": "ziyun_huang_haoyang",
                "name": "黄浩洋",
                "aliases": [],
                "gender": "男",
                "ethnicity": "布依族",
                "birth": "1980年5月",
                "birthplace": "贵州镇宁",
                "native_place": "贵州镇宁",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "黄浩洋_1980.05",
                    "name_birthplace": "黄浩洋_贵州镇宁",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "紫云苗族布依族自治县委书记",
                "current_org": "中共紫云苗族布依族自治县委员会",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002", "S003"]
            },
            "career_timeline": [
                {"start": "2019年8月", "end": "2019年9月", "org": "紫云苗族布依族自治县人民政府", "title": "代理县长", "level": "县处级正职", "location": "紫云县", "system": "government", "rank": "", "is_key_promotion": True, "notes": "安顺市委任命为代理县长", "confidence": "confirmed", "source_ids": ["S004"]},
                {"start": "2019年9月", "end": "2021年6月", "org": "紫云苗族布依族自治县人民政府", "title": "县长", "level": "县处级正职", "location": "紫云县", "system": "government", "rank": "", "is_key_promotion": True, "notes": "正式当选县长", "confidence": "confirmed", "source_ids": ["S004"]},
                {"start": "2021年6月", "end": "至今", "org": "中共紫云苗族布依族自治县委员会", "title": "县委书记", "level": "县处级正职", "location": "紫云县", "system": "party", "rank": "", "is_key_promotion": True, "notes": "升任县委书记", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "未知", "end": "2019年8月", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "公开资料未找到2019年8月前的完整履历", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"id": "org_ziyun_party", "name": "中共紫云苗族布依族自治县委员会", "role": "现任领导", "period": "2021-06至今"},
                {"id": "org_ziyun_gov", "name": "紫云苗族布依族自治县人民政府", "role": "曾任县长", "period": "2019-08至2021-06"}
            ],
            "relationships": [
                {"person": "杨坚", "person_id": "ziyun_yang_jian", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "党政正职搭档，共同出席多次县委会议", "overlap_org": "紫云苗族布依族自治县", "overlap_period": "2021年至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "张天勇", "person_id": "ziyun_zhang_tianyong", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "张天勇2016-2019任紫云县委书记，黄浩洋2021年起接任", "overlap_org": "中共紫云苗族布依族自治县委员会", "overlap_period": "", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S004"]},
                {"person": "龙海斌", "person_id": "ziyun_long_haibin", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "书记与常务副县长，县委常委会搭档", "overlap_org": "中共紫云苗族布依族自治县委常委会", "overlap_period": "", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001", "S005"]},
            ],
            "governance_record": [
                {"period": "2026-07", "domain": "other", "achievement_or_event": "为全县领导干部讲授树立和践行正确政绩观专题党课", "role_in_event": "主讲人", "measurable_outcome": "", "location": "紫云县", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["镇宁县", "平坝区", "紫云县"],
                "promotion_velocity": {
                    "summary": "2019年从平坝区委副书记调任紫云县长，2021年升任书记，跨县级区域晋升",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": ["正确政绩观", "全面从严治党", "高质量发展"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面纪律审查或舆情信号", "date": "", "confidence": "plausible", "source_ids": []}
            ],
            "source_register": [
                {"id": "S001", "title": "黄浩洋为全县领导干部讲授专题党课", "url": "http://www.gzzy.gov.cn/xwdt/ldhd/202607/t20260703_90582116.html", "publisher": "亚鲁紫云/紫云县人民政府", "published_at": "2026-07-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认黄浩洋现任县委书记"},
                {"id": "S002", "title": "黄浩洋到猫营镇调研防汛防溺水工作", "url": "http://www.gzzy.gov.cn/xwdt/ldhd/202605/t20260529_90224273.html", "publisher": "亚鲁紫云/紫云县人民政府", "published_at": "2026-05-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认黄浩洋现任县委书记"},
                {"id": "S003", "title": "受县委书记黄浩洋委托杨坚主持召开会议", "url": "http://www.gzzy.gov.cn/xwdt/zyyw/202607/t20260713_90611385.html", "publisher": "亚鲁紫云/紫云县人民政府", "published_at": "2026-07-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认黄浩洋为县委书记"},
                {"id": "S004", "title": "百度百科: 黄浩洋", "url": "https://baike.baidu.com/item/%E9%BB%84%E6%B5%A9%E6%B4%8B/7874590", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "确认出生信息、民族、籍贯、履历"},
                {"id": "S005", "title": "龙海斌简历", "url": "http://www.gzzy.gov.cn/zwgk/ldzc1/202503/t20250313_87158737.html", "publisher": "紫云县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "常务副县长简历"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "high",
                "biggest_gap": "2019年8月前黄浩洋的完整职业生涯（在平坝区的具体职务、教育背景、入党时间、工作起始时间）"
            },
            "open_questions": [
                {"priority": "critical", "question": "黄浩洋2019年8月前的完整履历是什么？此前在平坝区担任什么具体职务？", "why_it_matters": "无法完整追溯其晋升路径和专业背景", "suggested_queries": ["黄浩洋 平坝 简历", "黄浩洋 任前公示"], "last_attempted": AS_OF},
                {"priority": "high", "question": "黄浩洋的教育背景（院校、专业、学位）和入党时间？", "why_it_matters": "无法评估其知识结构和政治资历", "suggested_queries": ["黄浩洋 教育背景", "黄浩洋 贵州"], "last_attempted": AS_OF},
                {"priority": "medium", "question": "黄浩洋的出生月份和具体日期？", "why_it_matters": "仅知1980年5月，精确日期未知", "suggested_queries": ["黄浩洋 出生"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "filename": f"{AS_OF}-{PROVINCE}-{PARENT_CITY}-县长-杨坚.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": "紫云苗族布依族自治县",
                "job": "县长",
                "task_id": TASK_ID,
                "time_focus": "2021-2026"
            },
            "identity": {
                "person_id": "ziyun_yang_jian",
                "name": "杨坚",
                "aliases": [],
                "gender": "男",
                "ethnicity": "苗族",
                "birth": "1979年11月",
                "birthplace": "贵州六枝",
                "native_place": "贵州六枝",
                "education": [{"period": "", "institution": "", "major": "", "degree": "理学学士", "study_type": "full_time", "source_ids": []}],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "杨坚_1979.11",
                    "name_birthplace": "杨坚_贵州六枝",
                    "official_profile_url": "http://www.gzzy.gov.cn/zwgk/ldzc1/202503/t20250313_87158572.html"
                }
            },
            "current_status": {
                "current_post": "紫云苗族布依族自治县委副书记、县人民政府县长、党组书记",
                "current_org": "紫云苗族布依族自治县人民政府",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S101"]
            },
            "career_timeline": [
                {"start": "2021年7月", "end": "至今", "org": "紫云苗族布依族自治县人民政府", "title": "县委副书记、县长、党组书记", "level": "县处级正职", "location": "紫云县", "system": "government", "rank": "", "is_key_promotion": True, "notes": "2021年6月从六盘水跨市调任紫云县，任代县长，7月正式当选", "confidence": "confirmed", "source_ids": ["S101"]},
                {"start": "未知", "end": "2021年6月", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "公开资料未找到2021年6月前的完整履历。据推测可能在六盘水市工作，为跨市调任干部", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"id": "org_ziyun_gov", "name": "紫云苗族布依族自治县人民政府", "role": "现任领导", "period": "2021-07至今"}
            ],
            "relationships": [
                {"person": "黄浩洋", "person_id": "ziyun_huang_haoyang", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "党政正职搭档关系", "overlap_org": "紫云苗族布依族自治县", "overlap_period": "2021年至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "龙海斌", "person_id": "ziyun_long_haibin", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "县长与常务副县长直接上下级", "overlap_org": "紫云县人民政府", "overlap_period": "", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S101", "S005"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["government"],
                "geographic_pattern": ["六盘水市", "安顺市"],
                "promotion_velocity": {
                    "summary": "从六盘水市跨市调任紫云县长，属于非常规跨市调动",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面纪律审查或舆情信号", "date": "", "confidence": "plausible", "source_ids": []}
            ],
            "source_register": [
                {"id": "S101", "title": "杨坚简历", "url": "http://www.gzzy.gov.cn/zwgk/ldzc1/202503/t20250313_87158572.html", "publisher": "紫云县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "政府官网简历"},
                {"id": "S102", "title": "百度百科: 杨坚", "url": "https://baike.baidu.com/item/%E6%9D%A8%E5%9D%9A/20613890", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "百度百科词条"},
                {"id": "S103", "title": "县政府领导分工通知", "url": "http://www.gzzy.gov.cn/zwgk/zcwj/202606/t20260610_90504761.html", "publisher": "紫云县人民政府", "published_at": "2026-06-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "紫府办发〔2026〕8号"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "high",
                "biggest_gap": "2021年6月调任紫云前的完整职业生涯（在六盘水市的全部经历）"
            },
            "open_questions": [
                {"priority": "critical", "question": "杨坚2021年6月之前在六盘水市的具体任职经历是什么？", "why_it_matters": "无法追踪其职业背景、专业领域和晋升路径", "suggested_queries": ["杨坚 六盘水 简历", "杨坚 六枝 任职"], "last_attempted": AS_OF},
                {"priority": "high", "question": "杨坚的教育背景（院校、专业）？", "why_it_matters": "仅知理学学士学位，具体院校专业未知", "suggested_queries": ["杨坚 紫云 县长 教育"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "filename": f"{AS_OF}-{PROVINCE}-{PARENT_CITY}-常务副县长-龙海斌.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": "紫云苗族布依族自治县",
                "job": "常务副县长",
                "task_id": TASK_ID,
                "time_focus": "当前"
            },
            "identity": {
                "person_id": "ziyun_long_haibin",
                "name": "龙海斌",
                "aliases": [],
                "gender": "男",
                "ethnicity": "布依族",
                "birth": "1984年7月",
                "birthplace": "",
                "native_place": "",
                "education": [{"period": "", "institution": "", "major": "", "degree": "工学学士", "study_type": "full_time", "source_ids": []}],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "龙海斌_1984.07",
                    "name_birthplace": "",
                    "official_profile_url": "http://www.gzzy.gov.cn/zwgk/ldzc1/202503/t20250313_87158737.html"
                }
            },
            "current_status": {
                "current_post": "紫云苗族布依族自治县委常委、常务副县长、党组副书记",
                "current_org": "紫云苗族布依族自治县人民政府",
                "administrative_rank": "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S201"]
            },
            "career_timeline": [],
            "organizations": [],
            "relationships": [],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["经济管理", "财政金融", "安全生产", "应急管理"],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信号", "date": "", "confidence": "plausible", "source_ids": []}
            ],
            "source_register": [
                {"id": "S201", "title": "龙海斌简历", "url": "http://www.gzzy.gov.cn/zwgk/ldzc1/202503/t20250313_87158737.html", "publisher": "紫云县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "任紫云县委常委、常务副县长前的全部经历"
            },
            "open_questions": [
                {"priority": "high", "question": "龙海斌任紫云县委常委、常务副县长前的完整履历", "why_it_matters": "无法评估其专业背景来源", "suggested_queries": ["龙海斌 紫云 履历"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "filename": f"{AS_OF}-{PROVINCE}-{PARENT_CITY}-前任县委书记-张天勇.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": "紫云苗族布依族自治县",
                "job": "前任县委书记",
                "task_id": TASK_ID,
                "time_focus": "2016-2019"
            },
            "identity": {
                "person_id": "ziyun_zhang_tianyong",
                "name": "张天勇",
                "aliases": [],
                "gender": "男",
                "ethnicity": "回族",
                "birth": "1966年6月",
                "birthplace": "贵州平坝",
                "native_place": "贵州平坝",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "张天勇_1966.06",
                    "name_birthplace": "张天勇_贵州平坝",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "安顺市生态移民局党组成员、副局长（正县长级）",
                "current_org": "安顺市生态移民局",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": ["S301"]
            },
            "career_timeline": [
                {"start": "2016年2月", "end": "2019年8月", "org": "中共紫云苗族布依族自治县委员会", "title": "县委书记", "level": "县处级正职", "location": "紫云县", "system": "party", "rank": "", "is_key_promotion": True, "notes": "2016年2月任紫云县委书记，至2019年8月离任", "confidence": "confirmed", "source_ids": ["S301"]},
                {"start": "2019年8月", "end": "至今", "org": "安顺市生态移民局", "title": "党组成员、副局长（正县长级）", "level": "县处级正职", "location": "安顺市", "system": "government", "rank": "", "is_key_promotion": False, "notes": "平调至安顺市直部门，保留正县长级", "confidence": "confirmed", "source_ids": ["S301"]}
            ],
            "organizations": [],
            "relationships": [
                {"person": "黄浩洋", "person_id": "ziyun_huang_haoyang", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "张天勇2016-2019任紫云县委书记，黄浩洋2021年起接任", "overlap_org": "中共紫云苗族布依族自治县委员会", "overlap_period": "", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S301"]}
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["平坝", "紫云", "安顺"],
                "promotion_velocity": {"summary": "从紫云县委书记平调至安顺市生态移民局，保留正县长级", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信号", "date": "", "confidence": "plausible", "source_ids": []}
            ],
            "source_register": [
                {"id": "S301", "title": "百度百科: 张天勇", "url": "https://baike.baidu.com/item/%E5%BC%A0%E5%A4%A9%E5%8B%87/23651443", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": ""}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "张天勇任紫云县委书记前（2016年2月前）的完整职业生涯"
            },
            "open_questions": [
                {"priority": "medium", "question": "张天勇2016年2月前的完整职业履历", "why_it_matters": "无法追踪其从平坝到紫云的完整路径", "suggested_queries": ["张天勇 履历 安顺"], "last_attempted": AS_OF}
            ]
        }
    }
]


# ═══════════════════════════════════════════════════════════════════════════════
#  Build functions
# ═══════════════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return GEXF color for a person based on role."""
    role = p.get("current_post", "")
    if "书记" in role and "副书记" not in role:
        return "255,50,50"  # Red for party secretary
    if "县长" in role or "乡长" in role or "区长" in role:
        return "50,100,255"  # Blue for government head
    if "常务副" in role:
        return "50,100,255"
    if "挂职" in role:
        return "150,150,150"  # Grey for temporary
    if "人大" in role:
        return "200,255,255"  # Cyan for NPC
    if "政协" in role:
        return "255,240,200"  # Cream for CPPCC
    if "副" in role:
        return "100,150,255"  # Light blue for deputies
    return "100,100,100"


def is_top_leader(p):
    """Return True if this is a top leader (larger node size)."""
    role = p.get("current_post", "")
    return "县委书记" in role or ("县长" in role and "副" not in role)


def org_color(o):
    """Return GEXF color for an organization."""
    t = o.get("type", "")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


def build_db():
    """Create and populate the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        )
    """)
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    # Insert persons
    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education,
                                 party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
              p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    # Insert organizations
    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
              o.get("parent", ""), o.get("location", "")))

    # Insert positions
    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos.get("start_date", ""), pos.get("end_date", ""),
              pos.get("rank", ""), pos.get("note", "")))

    # Insert relationships
    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r.get("type", ""),
              r.get("context", ""), r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()

    print(f"DB: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


def build_gexf():
    """Generate GEXF 1.3 graph file with viz namespace."""
    from datetime import datetime
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>紫云苗族布依族自治县领导班子关系网络 (as of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    eid = 0

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("12.0" if p["id"] <= 3 else "10.0")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("ethnicity", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append(f'          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')

    # person→org (worked_at)
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # person↔person (relationship)
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("type", ""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"GEXF: {GEXF_PATH}")
    print(f"  {len(persons)} person nodes")
    print(f"  {len(organizations)} org nodes")
    print(f"  {len(positions)} person-org edges")
    print(f"  {len(relationships)} person-person edges")


def write_person_jsons():
    """Write per-person JSON files."""
    for pj in PERSON_JSONS:
        path = os.path.join(PERSONS_DIR, pj["filename"])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pj["data"], f, ensure_ascii=False, indent=2)
        print(f"Person JSON: {path}")


def main():
    print(f"=" * 60)
    print(f"  紫云苗族布依族自治县领导班子关系网络")
    print(f"  Data as of: {AS_OF}")
    print(f"  Staging: {BASE}")
    print(f"=" * 60)
    print()
    build_db()
    print()
    build_gexf()
    print()
    write_person_jsons()
    print()
    print("Done.")


if __name__ == "__main__":
    main()
