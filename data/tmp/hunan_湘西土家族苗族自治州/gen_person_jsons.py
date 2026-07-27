#!/usr/bin/env python3
"""Generate person JSON files for key figures in 湘西土家族苗族自治州."""
import json, os
from datetime import datetime
from pathlib import Path

TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"
STAGING = Path("data/tmp/hunan_湘西土家族苗族自治州")
STAGING.mkdir(parents=True, exist_ok=True)

def write_json(filename, data):
    path = STAGING / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  {path}")

# ═══════════════════════════════════════════════
# Person 1: 刘涛 - 湘西州委书记
# ═══════════════════════════════════════════════
write_json(f"{TODAY}-湖南省-湘西土家族苗族自治州-湘西州委书记-刘涛.json", {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "湖南省",
        "city": "湘西土家族苗族自治州",
        "region": "湘西土家族苗族自治州",
        "job": "湘西州委书记",
        "task_id": "hunan_湘西土家族苗族自治州",
        "time_focus": "2026年7月"
    },
    "identity": {
        "person_id": "xiangxi_liu_tao",
        "name": "刘涛",
        "aliases": [],
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-06",
        "birthplace": "河南省方城县",
        "native_place": "河南省方城县",
        "education": [
            {"period": "~1990-1994", "institution": "河南大学中文系", "major": "语言文学", "degree": "学士", "study_type": "full_time", "source_ids": ["S001"]},
            {"period": "1994-1997", "institution": "河南大学文学院", "major": "中国现代文学", "degree": "硕士", "study_type": "full_time", "source_ids": ["S001"]}
        ],
        "party_join": "1996-11",
        "work_start": "1997-07",
        "dedupe_keys": {
            "name_birth": "刘涛_1971-06",
            "name_birthplace": "刘涛_河南省方城县",
            "official_profile_url": "https://baike.baidu.com/item/%E5%88%98%E6%B6%9B"
        }
    },
    "current_status": {
        "current_post": "湘西州委书记",
        "current_org": "中共湘西土家族苗族自治州委员会",
        "administrative_rank": "正厅级",
        "as_of": AS_OF,
        "is_current_confirmed": True,
        "source_ids": ["S001", "S002"]
    },
    "career_timeline": [
        {"start": "1997-07", "end": "~2008", "org": "河南省劳动和社会保障厅", "title": "副厅长", "level": "副厅级", "location": "郑州", "system": "government", "rank": "副厅级", "is_key_promotion": True, "notes": "具体到任时间需进一步确认", "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "2015-02", "end": "2017-12", "org": "中共焦作市委", "title": "焦作市委常委、组织部部长", "level": "副厅级", "location": "焦作", "system": "organization", "rank": "副厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2017-12", "end": "2021-07", "org": "中共焦作市委", "title": "焦作市委副书记（2018.01兼统战部长）", "level": "副厅级", "location": "焦作", "system": "party", "rank": "副厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2021-07", "end": "2024-10", "org": "许昌市人民政府", "title": "许昌市委副书记、市长", "level": "正厅级", "location": "许昌", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2024-10", "end": "present", "org": "中共湘西州委", "title": "湘西州委书记", "level": "正厅级", "location": "吉首", "system": "party", "rank": "正厅级", "is_key_promotion": True, "notes": "跨省调任，首位外省籍湘西州委书记", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]}
    ],
    "organizations": [],
    "relationships": [
        {"person": "虢正贵", "person_id": "xiangxi_guo_zhenggui", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "虢正贵卸任后刘涛接任", "overlap_org": "中共湘西州委", "overlap_period": "2024-10", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "尚生龙", "person_id": "xiangxi_shang_shenglong", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "书记-代理州长搭班", "overlap_org": "湘西州", "overlap_period": "2026-06起", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "陈华", "person_id": "xiangxi_chen_hua", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "刘涛任书记时陈华为州长", "overlap_org": "湘西州", "overlap_period": "2024-10至2026-06", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]}
    ],
    "governance_record": [
        {"period": "2024-10至2026-07", "domain": "public_security", "achievement_or_event": "多次暗访检查安全生产，推动安全生产翻身仗", "role_in_event": "州委书记（督导）", "measurable_outcome": "在全州推进安全生产单元格管理", "location": "湘西州", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
        {"period": "2026-07", "domain": "economic_development", "achievement_or_event": "走访调研花垣县吉首市重点企业", "role_in_event": "州委书记", "measurable_outcome": "为多家企业协调融资、用工等需求", "location": "花垣县、吉首市", "confidence": "confirmed", "source_ids": ["S005"]}
    ],
    "professional_profile": {
        "primary_specializations": ["组织人事", "地方治理"],
        "career_pattern": "cross_province_rotation",
        "systems_experience": ["organization", "party", "government"],
        "geographic_pattern": ["河南", "湖南"],
        "promotion_velocity": {"summary": "约27年从科员至正厅级", "notable_fast_promotions": []}
    },
    "work_style_and_personality": {
        "public_style_indicators": [
            {"trait": "grassroots_oriented", "evidence": "多次暗访、突击检查安全生产", "confidence": "confirmed", "source_ids": ["S003"]},
            {"trait": "discipline_oriented", "evidence": "在安全生产调度会上严厉批评事故暴露的问题", "confidence": "confirmed", "source_ids": []}
        ],
        "caveat": "Work style is inferred from public records."
    },
    "network_metrics": {},
    "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信号", "date": "", "confidence": "confirmed", "source_ids": []}],
    "source_register": [
        {"id": "S001", "title": "百度百科-刘涛", "url": "https://baike.baidu.com/item/%E5%88%98%E6%B6%9B", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
        {"id": "S002", "title": "湘西网-刘涛报道集", "url": "http://www.xxnet.com.cn/news/", "publisher": "湘西网", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "2026年7月仍在任"},
        {"id": "S003", "title": "刘涛到花垣县暗访安全生产", "url": "http://m.xxnet.com.cn/content/2026-07/20/content_332822.html", "publisher": "湘西网", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": ""},
        {"id": "S004", "title": "刘涛主持召开州委常委会会议", "url": "http://www.xxnet.com.cn/news/content/2026-07/13/content_332698.html", "publisher": "湘西网", "published_at": "2026-07-13", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": ""},
        {"id": "S005", "title": "刘涛到凤凰县调研文旅工作", "url": "https://www.toutiao.com/article/7662545945195741748/", "publisher": "今日头条/湘西网", "published_at": "2026-07-15", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": ""}
    ],
    "confidence_summary": {
        "identity": "confirmed",
        "current_role": "confirmed",
        "career_completeness": "partial",
        "relationship_confidence": "high",
        "biggest_gap": "1997-~2008年早期履历"
    },
    "open_questions": [
        {"priority": "medium", "question": "刘涛1997-2008年的具体履历（从硕士毕业到河南省劳动和社会保障厅副厅长之间）", "why_it_matters": "覆盖约10年的早期职业生涯", "suggested_queries": ["刘涛 河南省劳动厅"], "last_attempted": AS_OF}
    ]
})

# ═══════════════════════════════════════════════
# Person 2: 尚生龙 - 湘西州代理州长
# ═══════════════════════════════════════════════
write_json(f"{TODAY}-湖南省-湘西土家族苗族自治州-湘西州代理州长-尚生龙.json", {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "湖南省",
        "city": "湘西土家族苗族自治州",
        "region": "湘西土家族苗族自治州",
        "job": "湘西州代理州长",
        "task_id": "hunan_湘西土家族苗族自治州",
        "time_focus": "2026年7月"
    },
    "identity": {
        "person_id": "xiangxi_shang_shenglong",
        "name": "尚生龙",
        "aliases": [],
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1975-02",
        "birthplace": "湖南省桑植县",
        "native_place": "湖南省桑植县",
        "education": [
            {"period": "1994-1997", "institution": "湖南税务高等专科学校", "major": "税务", "degree": "大专", "study_type": "full_time", "source_ids": ["S001", "S004"]},
            {"period": "2000-2002", "institution": "中央党校函授学院", "major": "经济管理", "degree": "本科", "study_type": "part_time", "source_ids": ["S004"]},
            {"period": "2005-2008", "institution": "湖南省委党校", "major": "法学理论", "degree": "在职研究生", "study_type": "party_school", "source_ids": ["S001"]}
        ],
        "party_join": "1996-01",
        "work_start": "1997-07",
        "dedupe_keys": {
            "name_birth": "尚生龙_1975-02",
            "name_birthplace": "尚生龙_湖南省桑植县",
            "official_profile_url": "https://baike.baidu.com/item/%E5%B0%9A%E7%94%9F%E9%BE%99/9023713"
        }
    },
    "current_status": {
        "current_post": "湘西州代理州长",
        "current_org": "湘西土家族苗族自治州人民政府",
        "administrative_rank": "正厅级",
        "as_of": AS_OF,
        "is_current_confirmed": True,
        "source_ids": ["S001", "S002"]
    },
    "career_timeline": [
        {"start": "1997-07", "end": "1999-08", "org": "张家界市永定区三家馆乡", "title": "党政办秘书、综治办主任、人武部副部长", "level": "乡科级", "location": "张家界", "system": "government", "rank": "科员", "is_key_promotion": False, "notes": "基层起步", "confidence": "confirmed", "source_ids": ["S004"]},
        {"start": "1999-08", "end": "2000-09", "org": "张家界市永定区三家馆乡", "title": "乡党委委员、人武部部长", "level": "乡科级", "location": "张家界", "system": "government", "rank": "副科级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S004"]},
        {"start": "2000-09", "end": "2001-01", "org": "张家界市永定区三家馆乡", "title": "乡党委副书记、人武部部长", "level": "乡科级", "location": "张家界", "system": "government", "rank": "副科级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S004"]},
        {"start": "2001-01", "end": "2003-02", "org": "张家界市永定区三家馆乡", "title": "乡党委副书记、乡长", "level": "乡科级", "location": "张家界", "system": "government", "rank": "正科级", "is_key_promotion": True, "notes": "其间中央党校函授本科学习", "confidence": "confirmed", "source_ids": ["S004"]},
        {"start": "2003-02", "end": "2004-03", "org": "张家界市永定区三家馆乡", "title": "乡党委书记", "level": "乡科级", "location": "张家界", "system": "party", "rank": "正科级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S004"]},
        {"start": "2004-03", "end": "2004-12", "org": "中共张家界市永定区委", "title": "永定区委常委（兼三家馆乡党委书记）", "level": "副处级", "location": "张家界", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "进入区县级领导层", "confidence": "confirmed", "source_ids": ["S004"]},
        {"start": "2004-12", "end": "2006-06", "org": "张家界市永定区崇文街道", "title": "永定区委常委、崇文街道党委书记", "level": "副处级", "location": "张家界", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "挂职北京石景山区老山街道工委副书记", "confidence": "confirmed", "source_ids": ["S004"]},
        {"start": "2006-06", "end": "2007-12", "org": "中共桑植县委", "title": "桑植县委常委、澧源镇党委书记", "level": "副处级", "location": "桑植", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "调回家乡桑植县", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
        {"start": "2007-12", "end": "2009-04", "org": "桑植县人民政府", "title": "桑植县委常委、副县长", "level": "副处级", "location": "桑植", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "其间省委党校在职研究生学习", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
        {"start": "2009-04", "end": "2017-01", "org": "桑植县人民政府", "title": "桑植县委常委、常务副县长", "level": "副处级", "location": "桑植", "system": "government", "rank": "副处级", "is_key_promotion": True, "notes": "主持政府日常工作约8年", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
        {"start": "2017-01", "end": "2021-04", "org": "张家界市人民政府", "title": "张家界市副市长", "level": "副厅级", "location": "张家界", "system": "government", "rank": "副厅级", "is_key_promotion": True, "notes": "分管农业、农村、扶贫、水利、林业、民政等工作", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"start": "2021-04", "end": "2025-02", "org": "中共张家界市委", "title": "张家界市委常委、副市长/常务副市长", "level": "副厅级", "location": "张家界", "system": "party/gov", "rank": "副厅级", "is_key_promotion": True, "notes": "2022年1月连任副市长，后转任常务副市长", "confidence": "confirmed", "source_ids": ["S001", "S005"]},
        {"start": "2025-02", "end": "2026-06", "org": "中共邵阳市委", "title": "邵阳市委副书记、市委教育工委书记", "level": "副厅级", "location": "邵阳", "system": "party", "rank": "副厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S003", "S005"]},
        {"start": "2026-06", "end": "present", "org": "湘西州人民政府", "title": "湘西州代理州长、州委副书记", "level": "正厅级", "location": "吉首", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "2026.06.09任州委副书记；2026.06.17任副州长、代理州长", "confidence": "confirmed", "source_ids": ["S002"]}
    ],
    "organizations": [],
    "relationships": [
        {"person": "刘涛", "person_id": "xiangxi_liu_tao", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "州委书记与代理州长搭班", "overlap_org": "湘西州", "overlap_period": "2026-06起", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "陈华", "person_id": "xiangxi_chen_hua", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "接替陈华任代理州长", "overlap_org": "湘西州人民政府", "overlap_period": "2026-06", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]}
    ],
    "governance_record": [
        {"period": "2017-2021", "domain": "agriculture", "achievement_or_event": "分管农业、农村、扶贫、水利等工作", "role_in_event": "张家界市副市长", "measurable_outcome": "", "location": "张家界", "confidence": "confirmed", "source_ids": []},
        {"period": "2021-2025", "domain": "economic_development", "achievement_or_event": "负责宁张对口合作，推动张家界与南京合作", "role_in_event": "张家界市委常委、常务副市长", "measurable_outcome": "推进产业合作平台建设", "location": "张家界", "confidence": "confirmed", "source_ids": []}
    ],
    "professional_profile": {
        "primary_specializations": ["乡镇基层治理", "县域经济", "地方财政"],
        "career_pattern": "local_ladder",
        "systems_experience": ["government", "party"],
        "geographic_pattern": ["永定区", "桑植", "张家界", "邵阳", "湘西"],
        "promotion_velocity": {"summary": "从乡镇秘书起步，29年从科员至正厅级", "notable_fast_promotions": []}
    },
    "work_style_and_personality": {
        "public_style_indicators": [
            {"trait": "grassroots_oriented", "evidence": "从乡镇秘书起步，长期在基层工作", "confidence": "confirmed", "source_ids": ["S004"]},
            {"trait": "pragmatic", "evidence": "在环保督察整改、对口合作等工作中以务实著称", "confidence": "plausible", "source_ids": []}
        ],
        "caveat": "Work style is inferred from public records."
    },
    "network_metrics": {},
    "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信号", "date": "", "confidence": "confirmed", "source_ids": []}],
    "source_register": [
        {"id": "S001", "title": "百度百科-尚生龙", "url": "https://baike.baidu.com/item/%E5%B0%9A%E7%94%9F%E9%BE%99/9023713", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
        {"id": "S002", "title": "中国经济网-尚生龙任湘西州代州长", "url": "http://district.ce.cn/newarea/sddy/202606/t20260622_3044364.shtml", "publisher": "中国经济网", "published_at": "2026-06-22", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": ""},
        {"id": "S003", "title": "腾讯新闻-尚生龙任邵阳市委副书记", "url": "https://news.qq.com/rain/a/20250219A004RG00", "publisher": "腾讯新闻", "published_at": "2025-02-19", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": ""},
        {"id": "S004", "title": "jendow百科-尚生龙", "url": "https://www.jendow.com.tw/wiki/%E5%B0%9A%E7%94%9F%E9%BE%8D", "publisher": "jendow百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "含完整基层履历"},
        {"id": "S005", "title": "新湖南-尚生龙任邵阳副书记", "url": "https://m.voc.com.cn/xhn/news/202502/27771467.html", "publisher": "新湖南", "published_at": "2025-02-18", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": ""}
    ],
    "confidence_summary": {
        "identity": "confirmed",
        "current_role": "confirmed",
        "career_completeness": "complete",
        "relationship_confidence": "high",
        "biggest_gap": "无重大缺口"
    },
    "open_questions": []
})

# ═══════════════════════════════════════════════
# Person 3: 陈华 - 前任湘西州州长
# ═══════════════════════════════════════════════
write_json(f"{TODAY}-湖南省-湘西土家族苗族自治州-前任湘西州州长-陈华.json", {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "湖南省",
        "city": "湘西土家族苗族自治州",
        "region": "湘西土家族苗族自治州",
        "job": "前任湘西州州长",
        "task_id": "hunan_湘西土家族苗族自治州",
        "time_focus": "2026年7月"
    },
    "identity": {
        "person_id": "xiangxi_chen_hua",
        "name": "陈华",
        "aliases": [],
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1967-12",
        "birthplace": "湖南省石门县",
        "native_place": "湖南省石门县",
        "education": [
            {"period": "1987-1990", "institution": "常德师专", "major": "英语", "degree": "大专", "study_type": "full_time", "source_ids": ["S001"]},
            {"period": "1993-1996", "institution": "湖南师范大学", "major": "英语", "degree": "本科", "study_type": "part_time", "source_ids": ["S001"]},
            {"period": "2003-2006", "institution": "中央党校", "major": "经济管理", "degree": "研究生", "study_type": "party_school", "source_ids": ["S001"]}
        ],
        "party_join": "1990-06",
        "work_start": "1990-07",
        "dedupe_keys": {
            "name_birth": "陈华_1967-12",
            "name_birthplace": "陈华_湖南省石门县",
            "official_profile_url": "https://baike.baidu.com/item/%E9%99%88%E5%8D%8E/20117663"
        }
    },
    "current_status": {
        "current_post": "前任湘西州州长（另有任用）",
        "current_org": "",
        "administrative_rank": "正厅级",
        "as_of": AS_OF,
        "is_current_confirmed": True,
        "source_ids": ["S001", "S002"]
    },
    "career_timeline": [
        {"start": "1990-07", "end": "1995-02", "org": "石门县一中", "title": "教师", "level": "", "location": "石门", "system": "education", "rank": "", "is_key_promotion": False, "notes": "任教约5年", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "1995-02", "end": "1996-07", "org": "中共石门县委组织部", "title": "干部", "level": "副科级", "location": "石门", "system": "organization", "rank": "副科级", "is_key_promotion": True, "notes": "从教师转岗", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "1996-07", "end": "1998-01", "org": "石门县连杆厂", "title": "党支部副书记、厂长助理", "level": "副科级", "location": "石门", "system": "state_owned_enterprise", "rank": "副科级", "is_key_promotion": False, "notes": "企业任职", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "1998-01", "end": "2000-12", "org": "石门县二都乡", "title": "乡党委副书记、乡长", "level": "正科级", "location": "石门", "system": "government", "rank": "正科级", "is_key_promotion": True, "notes": "兼宝峰开发区党委副书记", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2000-12", "end": "2002-05", "org": "石门县维新镇", "title": "镇党委书记", "level": "正科级", "location": "石门", "system": "party", "rank": "正科级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2002-05", "end": "2005-08", "org": "中共常德市武陵区委", "title": "武陵区委常委、组织部部长", "level": "副处级", "location": "常德", "system": "organization", "rank": "副处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2005-08", "end": "2007-02", "org": "常德市人民政府", "title": "市政府副秘书长", "level": "副处级", "location": "常德", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2007-02", "end": "2009-09", "org": "常德市外侨办", "title": "市外侨办主任、党组书记", "level": "正处级", "location": "常德", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2009-09", "end": "2012-10", "org": "常德市文化局/文广新局", "title": "局长、党组书记", "level": "正处级", "location": "常德", "system": "government", "rank": "正处级", "is_key_promotion": False, "notes": "2012.02兼市委宣传部副部长", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2012-12", "end": "2016-09", "org": "常德市人民政府", "title": "常德市副市长", "level": "副厅级", "location": "常德", "system": "government", "rank": "副厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2016-09", "end": "2021-09", "org": "中共常德市委", "title": "常德市委常委、统战部部长", "level": "副厅级", "location": "常德", "system": "party", "rank": "副厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2021-09", "end": "2022-12", "org": "中共常德市委", "title": "常德市委副书记、统战部部长", "level": "副厅级", "location": "常德", "system": "party", "rank": "副厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2022-12", "end": "2023-01", "org": "湘西州人民政府", "title": "湘西州代州长", "level": "正厅级", "location": "吉首", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "跨市调任", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2023-01", "end": "2026-06", "org": "湘西州人民政府", "title": "湘西州州长", "level": "正厅级", "location": "吉首", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "第十四届全国人大代表", "confidence": "confirmed", "source_ids": ["S001", "S003"]}
    ],
    "organizations": [],
    "relationships": [
        {"person": "虢正贵", "person_id": "xiangxi_guo_zhenggui", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "虢正贵任书记时陈华为州长", "overlap_org": "湘西州", "overlap_period": "2023-01至2024-10", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "刘涛", "person_id": "xiangxi_liu_tao", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "搭班约1年半", "overlap_org": "湘西州", "overlap_period": "2024-10至2026-06", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]}
    ],
    "governance_record": [
        {"period": "2023-2026", "domain": "rural_revitalization", "achievement_or_event": "推进湘西州从'示范引领'到'全域跨越'的乡村振兴路径", "role_in_event": "州长", "measurable_outcome": "三分之二脱贫群众依靠产业稳定增收", "location": "湘西州", "confidence": "confirmed", "source_ids": ["S004"]},
        {"period": "2024-2026", "domain": "economic_development", "achievement_or_event": "推动'1+5+X'现代化产业体系建设", "role_in_event": "州长", "measurable_outcome": "", "location": "湘西州", "confidence": "confirmed", "source_ids": ["S004"]}
    ],
    "professional_profile": {
        "primary_specializations": ["组织人事", "文化事业", "统战工作"],
        "career_pattern": "cross_city_rotation",
        "systems_experience": ["organization", "government", "party", "education"],
        "geographic_pattern": ["石门", "常德", "湘西"],
        "promotion_velocity": {"summary": "从教师起步进入政界，32年从科员至正厅级", "notable_fast_promotions": []}
    },
    "work_style_and_personality": {
        "public_style_indicators": [
            {"trait": "pragmatic", "evidence": "强调'因地制宜发展新质生产力'", "confidence": "confirmed", "source_ids": ["S004"]}
        ],
        "caveat": "Work style is inferred from public records."
    },
    "network_metrics": {},
    "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信号", "date": "", "confidence": "confirmed", "source_ids": []}],
    "source_register": [
        {"id": "S001", "title": "百度百科-陈华", "url": "https://baike.baidu.com/item/%E9%99%88%E5%8D%8E/20117663", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
        {"id": "S002", "title": "中国经济网-尚生龙任湘西州委副书记 陈华另有任用", "url": "http://district.ce.cn/newarea/sddy/202606/t20260609_3019808.shtml", "publisher": "中国经济网", "published_at": "2026-06-09", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": ""},
        {"id": "S003", "title": "湘西州人大常委会人事任免", "url": "https://xx.voc.com.cn/news/202606/32929145.html", "publisher": "新湖南·湘西频道", "published_at": "2026-06-17", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S004", "title": "湖南省政府-陈华专访", "url": "http://www.hunan.gov.cn/topic/2026ybg/202602/t20260209_33913164.html", "publisher": "湖南省人民政府门户网站", "published_at": "2026-02-09", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""}
    ],
    "confidence_summary": {
        "identity": "confirmed",
        "current_role": "confirmed",
        "career_completeness": "complete",
        "relationship_confidence": "high",
        "biggest_gap": "卸任后的具体去向未知"
    },
    "open_questions": [
        {"priority": "critical", "question": "陈华2026年6月'另有任用'的具体去向", "why_it_matters": "前任州长的去向影响网络分析", "suggested_queries": ["陈华 另有任用 湘西 2026"], "last_attempted": AS_OF}
    ]
})

# ═══════════════════════════════════════════════
# Person 4: 虢正贵 - 前任湘西州委书记
# ═══════════════════════════════════════════════
write_json(f"{TODAY}-湖南省-湘西土家族苗族自治州-前任湘西州委书记-虢正贵.json", {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "湖南省",
        "city": "湘西土家族苗族自治州",
        "region": "湘西土家族苗族自治州",
        "job": "前任湘西州委书记",
        "task_id": "hunan_湘西土家族苗族自治州",
        "time_focus": "2026年7月"
    },
    "identity": {
        "person_id": "xiangxi_guo_zhenggui",
        "name": "虢正贵",
        "aliases": [],
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964-09",
        "birthplace": "湖南省长沙市望城区",
        "native_place": "湖南省长沙市望城区",
        "education": [
            {"period": "", "institution": "长沙基础大学", "major": "物理", "degree": "大专", "study_type": "full_time", "source_ids": ["S001"]}
        ],
        "party_join": "1984-06",
        "work_start": "1984-07",
        "dedupe_keys": {
            "name_birth": "虢正贵_1964-09",
            "name_birthplace": "虢正贵_湖南省长沙市望城区",
            "official_profile_url": "https://baike.baidu.com/item/%E8%99%A2%E6%AD%A3%E8%B4%B5"
        }
    },
    "current_status": {
        "current_post": "湖南省政协副主席",
        "current_org": "湖南省政协",
        "administrative_rank": "副部级",
        "as_of": AS_OF,
        "is_current_confirmed": True,
        "source_ids": ["S001"]
    },
    "career_timeline": [
        {"start": "2002-01", "end": "2006-09", "org": "宁乡县", "title": "宁乡县委书记", "level": "正处级", "location": "宁乡", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2006-09", "end": "~2008", "org": "长沙市人民政府", "title": "长沙市副市长", "level": "副厅级", "location": "长沙", "system": "government", "rank": "副厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "~2008", "end": "~2012", "org": "中共长沙市委", "title": "长沙市委常委", "level": "副厅级", "location": "长沙", "system": "party", "rank": "副厅级", "is_key_promotion": True, "notes": "历任统战部长、政法委书记", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "~2012", "end": "~2015", "org": "湖南省人民政府", "title": "省政府副秘书长", "level": "副厅级", "location": "长沙", "system": "government", "rank": "副厅级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "~2015", "end": "~2016", "org": "湖南省人民政府研究室", "title": "省政府研究室主任", "level": "正厅级", "location": "长沙", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "~2016", "end": "2021-03", "org": "湖南湘江新区", "title": "湘江新区管委会主任", "level": "正厅级", "location": "长沙", "system": "development_zone", "rank": "正厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2021-03", "end": "2024-10", "org": "中共湘西州委", "title": "湘西州委书记", "level": "正厅级", "location": "吉首", "system": "party", "rank": "正厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2023-01", "end": "present", "org": "湖南省政协", "title": "湖南省政协副主席", "level": "副部级", "location": "长沙", "system": "other", "rank": "副部级", "is_key_promotion": True, "notes": "2024年10月卸任湘西州委书记后专注省政协工作", "confidence": "confirmed", "source_ids": ["S001"]}
    ],
    "organizations": [],
    "relationships": [
        {"person": "刘涛", "person_id": "xiangxi_liu_tao", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "虢正贵卸任后刘涛接任", "overlap_org": "中共湘西州委", "overlap_period": "2024-10", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "陈华", "person_id": "xiangxi_chen_hua", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "搭班约1年9个月", "overlap_org": "湘西州", "overlap_period": "2023-01至2024-10", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]}
    ],
    "governance_record": [],
    "professional_profile": {
        "primary_specializations": ["地方治理", "新区开发"],
        "career_pattern": "local_ladder",
        "systems_experience": ["government", "party", "development_zone"],
        "geographic_pattern": ["宁乡", "长沙", "湘西"],
        "promotion_velocity": {"summary": "从县委书记到省部级副职约21年", "notable_fast_promotions": []}
    },
    "work_style_and_personality": {"public_style_indicators": [], "caveat": "Work style is inferred from public records."},
    "network_metrics": {},
    "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信号", "date": "", "confidence": "confirmed", "source_ids": []}],
    "source_register": [
        {"id": "S001", "title": "百度百科-虢正贵", "url": "https://baike.baidu.com/item/%E8%99%A2%E6%AD%A3%E8%B4%B5", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": ""}
    ],
    "confidence_summary": {
        "identity": "confirmed",
        "current_role": "confirmed",
        "career_completeness": "partial",
        "relationship_confidence": "high",
        "biggest_gap": "1984-2002年早期履历"
    },
    "open_questions": [
        {"priority": "low", "question": "虢正贵1984年参加工作至2002年任宁乡县委书记间的完整履历", "why_it_matters": "约18年的早期职业路径", "suggested_queries": ["虢正贵 早期 简历 1984"], "last_attempted": AS_OF}
    ]
})

print("\nAll person JSON files created.")
