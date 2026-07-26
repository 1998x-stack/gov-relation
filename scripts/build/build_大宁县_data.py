#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 大宁县, 临汾市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_大宁县
Level: 县
Targets: 县委书记 & 县长

Current Status (as of 2026-07-26):
  - 县委书记: 翟纪亭 (confirmed — government site + Baidu Baike)
  - 县长: 宋建伟 (confirmed — government site + Baidu Baike; succeeded 王志华 in May 2026)

Research notes:
  - 大宁县政府官网 (http://www.daning.gov.cn/) — accessible, confirmed names
  - 百度百科 — accessible, confirmed career histories for core figures
  - Baidu search — partially accessible via direct URL
  - Google/Bing/Jina Reader/Exa — all blocked or timed out
  - Wikipedia — no political data for this small county
"""

from __future__ import annotations

import json
import os
import sqlite3  # noqa: used by gov_relation.runner internally
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _ in range(10):
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    REPO_ROOT = REPO_ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "大宁县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_大宁县"
if _CURRENT_DIR.name == "shanxi_大宁县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — CONFIRMED
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "翟纪亭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-11",
        "birthplace": "山西芮城",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "大宁县委书记",
        "current_org": "中国共产党大宁县委员会",
        "source": "http://www.daning.gov.cn/ — 政府网站新闻; 百度百科; 网易新闻2025-11-15",
        "confidence": "confirmed",
        "notes": "2025年11月14日任大宁县委书记。曾任平陆县委副书记、县长。2017年获全国对口支援新疆先进个人。山西省第十四届人大代表。"
    },
    {
        "id": 2,
        "name": "宋建伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-02",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_post": "",
        "current_post": "大宁县委副书记、县长",
        "current_org": "大宁县人民政府",
        "source": "百度百科(宋建伟-大宁县代县长); 大宁县政府网站2026-07新闻; 汲古新知2026-05-21",
        "confidence": "confirmed",
        "notes": "2026年5月20日任大宁县委副书记，提名为县长候选人。曾任临汾市住房和城乡建设局党组成员、副局长。2026年5月任代县长，7月以县长身份活动。接替王志华。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Key Deputies — CONFIRMED NAMES, partial biographical data
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "任臻",
        "gender": "男",
        "ethnicity": "",
        "birth": "1976-02",
        "birthplace": "山西夏县",
        "education": "大学",
        "party_join": "2000-06",
        "work_post": "1995-08",
        "current_post": "大宁县委副书记、统战部部长",
        "current_org": "中国共产党大宁县委员会",
        "source": "百度百科; 搜狐新闻; 黄河新闻网",
        "confidence": "confirmed",
        "notes": "1995年8月参加工作，2000年6月入党。大学学历。山西夏县人。负责县委统战工作。"
    },
    {
        "id": 4,
        "name": "贺晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-08",
        "birthplace": "",
        "education": "省委党校研究生",
        "current_post": "大宁县人大常委会主任、县委常委、政法委书记",
        "current_org": "大宁县人民代表大会常务委员会",
        "source": "百度百科; 2025年3月任职报道",
        "confidence": "confirmed",
        "notes": "2025年3月任大宁县人大常委会主任。三级调研员。兼任县委常委、政法委书记。"
    },
    {
        "id": 5,
        "name": "李剑书",
        "gender": "男",
        "ethnicity": "",
        "birth": "1988-08",
        "birthplace": "",
        "education": "研究生，教育学硕士",
        "current_contact": "",
        "current_post": "县委常委、副县长",
        "current_org": "大宁县人民政府",
        "source": "2024年1月9日任命; 52保德网2024-02-18; 县政府网站",
        "confidence": "confirmed",
        "notes": "1988年8月生，研究生学历，教育学硕士，中共党员。2024年1月任副县长，现任县委常委、副县长。分管人社局、教科局（科技工作）、民政局、退役军人事务局，联系市生态环境局大宁分局。"
    },
    {
        "id": 6,
        "name": "王婧",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "current_post": "县委常委、宣传部部长、政府党组成员",
        "current_org": "中国共产党大宁县委员会宣传部",
        "source": "百度百科; 黄河新闻网2025-05-15; 大宁县党务工作会议",
        "confidence": "confirmed",
        "notes": "详细履历（出生年月、具体任职历程）未在公开资料中列出。负责全县宣传思想文化工作。"
    },
    {
        "id": 7,
        "name": "李博",
        "gender": "",
        "ethnicity": "汉",
        "birth": "1981-06",
        "birthplace": "",
        "education": "大学",
        "current_post": "县委常委、组织部部长、党校校长",
        "current_org": "中国共产党大宁县委员会组织部",
        "source": "搜狐网2024-07-02; 临汾市委组织部公示",
        "confidence": "confirmed",
        "notes": "1981年6月生，大学学历，中共党员。2024年6月任大宁县委常委、组织部长、党校校长。此前任临汾市委组织部干部一科（干部队伍规划科）科长、四级调研员。接替宗燕军（调任蒲县）。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县政府领导班子 — CONFIRMED from government site
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 8,
        "name": "张鹏华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "current_post": "大宁副县长",
        "current_org": "大宁县人民政府",
        "source": "县政府网站（5天前 - 2026年7月）",
        "confidence": "confirmed",
        "notes": "县政府副县长。详细履历待查。"
    },
    {
        "id": 9,
        "name": "冯华平",
        "current_post": "大宁县政府副县长",
        "current_org": "大宁县人民政府",
        "source": "县政府网站; 大宁县政府新闻2026-01-12",
        "confidence": "confirmed",
        "notes": "具体分工：陪同翟纪亭、王志华调研疾控中心工作。"
    },
    {
        "id": 10,
        "name": "温晓敏",
        "current_post": "大宁县政府副县长",
        "current_org": "大宁县人民政府",
        "source": "县政府网站",
        "confidence": "confirmed",
        "notes": "详细履历待查。"
    },
    {
        "id": 11,
        "name": "曹峰",
        "gender": "",
        "current_post": "大宁副县长、公安局党委书记、局长",
        "current_org": "大宁县公安局",
        "source": "县政府网站; 山西晚报2026-02-06（大宁县公安局务虚会）",
        "confidence": "confirmed",
        "notes": "兼任县公安局局长。2026年2月主持公安局务虚会。此前历任不详。"
    },
    {
        "id": 12,
        "name": "胡玲玲",
        "current_post": "大宁县政府副县长",
        "current_org": "大宁县人民政府",
        "source": "县政府网站",
        "confidence": "confirmed",
    },
    {
        "id": 13,
        "name": "李小虎",
        "current_post": "大宁县政府副县长",
        "current_org": "大宁县人民政府",
        "source": "县政府网站",
        "confidence": "confirmed",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Additional deputy-level leaders from news articles
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 14,
        "name": "李栋",
        "current_post": "大宁县副县长",
        "current_org": "大宁县人民政府",
        "source": "山西新闻网2025-04; 县政府常务会议2025-04-21",
        "confidence": "confirmed",
        "notes": "2025年4月以副县长身份参加曲峨镇调研。"
    },
    {
        "id": 15,
        "name": "任秀红",
        "current_post": "大宁县副县长",
        "current_org": "大宁县人民政府",
        "source": "县政府常务会议2025-04-21",
        "confidence": "confirmed",
    },
    {
        "id": 16,
        "name": "苏争鸣",
        "current_post": "大宁县副县长",
        "current_org": "大宁县人民政府",
        "source": "县政府常务会议2025-04-21; 光明书屋揭牌仪式2026-07",
        "confidence": "confirmed",
        "notes": "参与光明书屋项目建设。"
    },
    {
        "id": 17,
        "name": "吴虹",
        "current_post": "大宁县政协副主席、县财政局局长",
        "current_org": "大宁县政协",
        "source": "县政府常务会议2025-04-21",
        "confidence": "confirmed",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessor Figures
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 101,
        "name": "王晓斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-07",
        "birthplace": "山西省临汾市尧都区",
        "education": "大学（武汉大学中文系）",
        "party_join": "1994-05",
        "work_post": "1991-09",
        "current_post": "阳泉市委常委、统战部部长、市政协党组副书记",
        "current_org": "中共阳泉市委统战部",
        "source": "百度百科; 搜狐新闻2025-08-14（拟任市委常委公示）",
        "confidence": "confirmed",
        "notes": "2021年3月任大宁县委书记。2025年8月拟任市委常委，后任阳泉市委常委、统战部长。接替王金龙。"
    },
    {
        "id": 102,
        "name": "王志华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-10",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "current_post": "不再担任大宁县县长（去向未确认）",
        "current_org": "",
        "source": "百度百科; 网易2023-04-01; 汲古新知2026-05",
        "confidence": "confirmed",
        "notes": "1970年10月生，大学本科学历。2022年4月任大宁副县长、代县长 → 2023年3月当选县长。2026年5月被宋建伟接替。去向目前未确认。"
    },
    {
        "id": 103,
        "name": "王金龙",
        "current_post": "前大宁县县委书记（更早前任）",
        "current_org": "",
        "source": "网易2021-03-20（王晓斌接替王金龙）",
        "confidence": "confirmed",
        "notes": "2021年3月前担任大宁县委书记，由王晓斌接替。更早细节待查。"
    },
    {
        "id": 104,
        "name": "宗燕军",
        "current_post": "蒲县县委常委、组织部长（此前大宁县组织部长）",
        "current_org": "蒲县县委组织部",
        "source": "搜狐2024-07-02; 汲古新知2024-06-27",
        "confidence": "confirmed",
        "notes": "原大宁县委常委、组织部长，2024年6月调任蒲县。李博接替。"
    },
]

# Fill in missing fields for consistency
for p in persons:
    p.setdefault("gender", "")
    p.setdefault("ethnicity", "")
    p.setdefault("birth", "")
    p.setdefault("birthplace", "")
    p.setdefault("education", "")
    p.setdefault("party_join", "")
    p.setdefault("work_post", "")
    p.setdefault("notes", "")

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中国共产党大宁县委员会",           "type": "党委", "level": "县级", "parent": "中共临汾市委员会", "location": "山西省临汾市大宁县"},
    {"id": 2, "name": "大宁县人民政府",                   "type": "政府", "level": "县级", "parent": "临汾市人民政府", "location": "山西省临汾市大宁县"},
    {"id": 3, "name": "大宁县人民代表大会常务委员会",     "type": "人大", "level": "县级", "parent": "临汾市人大常委会", "location": "山西省临汾市大宁县"},
    {"id": 4, "name": "大宁县政协",                       "type": "政协", "level": "县级", "parent": "政协临汾市委员会", "location": "山西省临汾市大宁县"},
    {"id": 5, "name": "中国共产党大宁县纪律检查委员会",   "type": "纪委", "level": "县级", "parent": "中共临汾市纪律检查委员会", "location": "山西省临汾市大宁县"},
    {"id": 6, "name": "中共大宁县委组织部",               "type": "党委", "level": "县级", "parent": "中共临汾市委组织部", "location": "山西省临汾市大宁县"},
    {"id": 7, "name": "中共大宁县委宣传部",               "type": "党委", "level": "县级", "parent": "中共临汾市委宣传部", "location": "山西省临汾市大宁县"},
    {"id": 8, "name": "中共大宁县委政法委员会",           "type": "党委", "level": "县级", "parent": "中共临汾市委政法委员会", "location": "山西省临汾市大宁县"},
    {"id": 9, "name": "大宁县委统战部",                   "type": "党委", "level": "县级", "parent": "中共临汾市委统战部", "location": "山西省临汾市大宁县"},
    {"id": 10, "name": "大宁县公安局",                    "type": "政府", "level": "县级", "parent": "临汾市公安局", "location": "山西省临汾市大宁县"},
    {"id": 11, "name": "大宁县财政局",                    "type": "政府", "level": "县级", "parent": "临汾市财政局", "location": "山西省临汾市大宁县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # Current leadership
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2025-11-14", "end_date": "至今", "rank": "正处级", "note": "2025年11月14日任大宁县委书记。此前任平陆县委副书记、县长。"},
    {"person_id": 2, "org_id": 2, "title": "县长（代县长→县长）", "start_date": "2026-05-20", "end_date": "至今", "rank": "正处级", "note": "2026年5月20日任县委副书记、提名为县长候选人。此前任临汾市住建局副局长。"},
    # Key standing committee
    {"person_id": 3, "org_id": 1, "title": "县委副书记、统战部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "1976年2月生，山西夏县人。大学学历。"},
    {"person_id": 4, "org_id": 3, "title": "县人大常委会主任", "start_date": "2025-03", "end_date": "至今", "rank": "正处级", "note": "兼任县委常委、政法委书记。"},
    {"person_id": 5, "org_id": 2, "title": "县委常委、副县长", "start_date": "2024-01", "end_date": "至今", "rank": "副处级", "note": "1988年8月生，研究生学历，教育学硕士。"},
    {"person_id": 6, "org_id": 7, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "兼政府党组成员。详细公开履历有限。"},
    {"person_id": 7, "org_id": 6, "title": "县委常委、组织部部长、党校校长", "start_date": "2024-06", "end_date": "至今", "rank": "副处级", "note": "1981年6月生。之前任临汾市委组织部干部一科科长。"},
    # 县政府领导班子
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 10, "title": "副县长、公安局党委书记、局长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长（此前任职）", "start_date": "", "end_date": "2025", "rank": "副处级", "note": "2025年仍在任，当前名单中未出现，可能已调整。"},
    {"person_id": 15, "org_id": 2, "title": "副县长（此前任职）", "start_date": "", "end_date": "2025", "rank": "副处级", "note": "2025年仍在任。"},
    # 其他重要职位
    {"person_id": 16, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 4, "title": "县政协副主席兼县财政局局长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # Predecessors
    {"person_id": 101, "org_id": 1, "title": "原县委书记", "start_date": "2021-03", "end_date": "2025-11", "rank": "正处级", "note": "2021年3月-2025年11月任大宁县委书记。现任阳泉市委常委、统战部部长。"},
    {"person_id": 102, "org_id": 2, "title": "原县长", "start_date": "2022-04", "end_date": "2026-05", "rank": "正处级", "note": "2022年4月任代县长 → 2023年3月正式当选。2026年5月卸任。"},
    {"person_id": 103, "org_id": 1, "title": "前县委书记", "start_date": "", "end_date": "2021-03", "rank": "正处级", "note": "2021年3月前担任大宁县委书记"},
    {"person_id": 104, "org_id": 6, "title": "原组织部部长", "start_date": "", "end_date": "2024-06", "rank": "副处级", "note": "调任蒲县县委常委、组织部部长。"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # Core leadership: party secretary ↔ mayor (structural partnership)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "翟纪亭（县委书）与宋建伟（县长）党政搭档关系", "overlap_org": "大宁县", "overlap_period": "2026-05至今"},
    {"person_a": 1, "person_b": 102, "type": "后任与前任", "context": "翟纪亭接替王晓斌任大宁县委书记", "overlap_org": "中国共产党大宁县委员会", "overlap_period": "2025-11"},
    {"person_a": 2, "person_b": 102, "type": "后任与前任", "context": "宋建伟接替王志华任大宁县县长", "overlap_org": "大宁县人民政府", "overlap_period": "2026-05"},
    {"person_a": 101, "person_b": 103, "type": "后任与前任", "context": "王晓斌接替王金龙任大宁县委书记", "overlap_org": "大宁县县委", "overlap_period": "2021-03"},
    # Predecessor → successor chain
    {"person_a": 103, "person_b": 101, "type": "前任与后任", "context": "王金龙离任后王晓斌接任县委书记", "overlap_org": "中国共产党大宁县委员会", "overlap_period": "2021-03"},
    {"person_a": 101, "person_b": 1, "type": "前任与后任", "context": "王晓斌升任阳泉市委常委后翟纪亭接任", "overlap_org": "中国共产党大宁县委员会", "overlap_period": "2025-11"},
    # Standing committee working relationships
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与县委副书记（统战部长）", "overlap_org": "大宁县县委", "overlap_period": "2025-11至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记与政法委书记/人大主任", "overlap_org": "大宁县常委分红会", "overlap_period": "2025-11至今"},
    {"person_a": 1, "person_b": 6, "type": "同事", "context": "县委常委班子共事", "overlap_org": "大宁县县委常委会", "overlap_period": "2025-11至今"},
    {"person_a": 1, "person_b": 7, "type": "同事", "context": "县委常委班子共事", "overlap_org": "大宁县县委常委会", "overlap_period": "2025-11至今"},
    {"person_a": 2, "person_b": 3, "type": "同事", "context": "县长与县委副书记", "overlap_org": "大宁县", "overlap_period": "2026-05至今"},
    {"person_a": 2, "person_b": 5, "type": "同事", "context": "县长与常务副县长", "overlap_org": "大宁县人民政府", "overlap_period": "2026-05至今"},
    # Gov team relationships
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长与副县长张鹏华", "overlap_org": "大宁县人民政府", "overlap_period": "2026-05至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长与副县长冯华平", "overlap_org": "大宁县人民政府", "overlap_period": "2026-05至今"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "县长与副县长/公安局长曹峰", "overlap_org": "大宁县人民政府"},
    # Position handoffs
    {"person_a": 7, "person_b": 104, "type": "前后任", "context": "李博接替宗燕军任组织部长", "overlap_org": "中共大宁县委组织部", "overlap_period": "2024-06"},
    # Cross-county / cross-region connections
    {"person_a": 1, "person_b": 101, "type": "跨县关联", "context": "翟纪亭（平陆县长→大宁书记）与王晓斌（大宁书记→阳泉市委常委）先后在大宁任职", "overlap_org": "大宁县委员会", "overlap_period": "2025-11"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════


def _get_person_open_questions(person: dict) -> list[dict]:
    """Generate open questions for a person record."""
    name = person["name"]
    pid = person["id"]
    questions = [
        {
            "priority": "critical",
            "question": f"宋建伟（大宁县县长）的完整履历——尤其是任临汾市住建局副局长之前的经历",
            "why_it_matters": "核心人物履历仍不完整",
            "suggested_queries": [f"宋建伟 简历 临汾 住建局", "宋建伟 公示"],
            "last_attempted": AS_OF,
        },
    ]
    if name == "翟纪亭" and pid == 1:
        questions.append({
            "priority": "high",
            "question": "翟纪亭在芮城县的详细任职时间（乡镇任职各时间段）",
            "why_it_matters": "丰富核心人物早期履历",
            "suggested_queries": ["翟纪亭 芮城县 大王镇 党委副书记"],
        })
    return questions


def _make_person_id(name: str, birth: str = "") -> str:
    clean = name.replace(" ", "").replace("　", "")
    birth_part = f"_{birth.replace('-', '').replace('月', '')}" if birth else ""
    return f"daning_{clean}{birth_part}"


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file."""
    pid = person["id"]
    name = person["name"]

    person_positions = [p for p in positions if p["person_id"] == pid]
    orgs_lookup = {o["id"]: o for o in organizations}

    career_timeline = []
    for pos in sorted(person_positions, key=lambda x: x.get("start_date", "")):
        org = orgs_lookup.get(pos["org_id"])
        career_timeline.append({
            "start": pos.get("start_date", ""),
            "end": pos.get("end_date", ""),
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "location": org["location"] if org else "",
            "system": "party" if org and "中共" in org["name"] else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": pid in (1, 2),
            "notes": pos.get("note", ""),
            "confidence": person.get("confidence", "plausible"),
            "source_ids": ["S001"],
        })

    person_rels = [
        r for r in relationships if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": _make_person_id(other_name),
            "relationship_type": r.get("type", "overlap"),
            "strength": "strong" if r.get("type") in ("党政搭档", "前后任") else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": person.get("confidence", "plausible"),
            "source_ids": ["S001"],
        })

    sources = [
        {
            "id": "S001",
            "title": "大宁县人民政府门户网站",
            "url": "http://www.daning.gov.cn/",
            "publisher": "大宁县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "大宁县政府官网首页及新闻页面，可确认县委书记翟纪亭和县长宋建伟的公开活动。",
        },
        {
            "id": "S002",
            "title": "翟纪亭-百度百科",
            "url": "https://baike.baidu.com/item/翟纪亭",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "百度百科提供了翟纪亭的详细履历信息。",
        },
        {
            "id": "S003",
            "title": "宋建伟-百度百科",
            "url": "https://baike.baidu.com/item/宋建伟",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "百度百科提供了宋建伟的基本信息。",
        },
    ]

    current_post = person.get("current_post", "")
    current_org_val = person.get("current_org", "")
    is_core = pid in (1, 2)
    admin_rank = (
        "正处级" if is_core or "正处级" in str(current_post) or "书记" in str(current_post) or "县长" in str(current_post)
        else "副处级"
    )
    # 人大主任 is also 正处级
    if "人大主任" in str(current_post) or "政协主席" in str(current_post):
        admin_rank = "正处级"

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山西省",
            "city": "临汾市",
            "region": "大宁县",
            "job": current_post,
            "task_id": "shanxi_大宁县",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": _make_person_id(name, person.get("birth", "")),
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown"}] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": current_post,
            "current_org": current_org_val,
            "administrative_rank": admin_rank,
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["党政管理"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if "芮城" in str(person.get("birthplace", "")) else "cross_county_rotation" if pid in (1, 2) else "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格为从公开记录、讲话和政务行动的推断，非心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "current_role": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "high" if pid in (1, 2, 101, 102) else "medium",
            "biggest_gap": f"{name}早期履历细节" if not person.get("work_start") else "履历中的具体时间节点",
        },
        "open_questions": _get_person_open_questions(person),
    }

    # Build filename
    safe_post = str(current_post).replace('/', '_').replace('（', '(').replace('）', ')')
    fname = f"{TODAY}-山西省-临汾市-{safe_post}-{name}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Write person JSONs for core targets + key deputies
    print("  Writing person JSONs...")
    core_ids = {1, 2, 3, 4, 5, 6, 7, 101, 102}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())