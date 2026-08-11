#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 龙井市, 延边朝鲜族自治州, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_龙井市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.longjing.gov.cn — 龙井市人民政府官方网站 (✓ reachable via HTTP)
    - 市长黄炳昊简历 (http://www.longjing.gov.cn/szf/szfld/sz/)
    - 市政府领导列表 (http://www.longjing.gov.cn/szf/szfld/)
    - 吴贤哲到老头沟镇调研灾后恢复工作 (2026-07-19) — confirms 市委书记吴贤哲
    - 市委召开2026年第9次常委会会议 (2026-07-10) — confirms 市委书记吴贤哲主持会议
    - 关于任命玄春根等同志职务的通知 (2023-09-27) — appointment notice pattern
    - 关于任免王志国等同志职务的通知 (2023-08-04) — confirms 王志国, 李永男, 金荣哲 etc.
  - Baidu Baike (403), Exa (rate-limited), Google (blocked)

Confidence notes:
  - 吴贤哲(市委书记): name confirmed from multiple official news articles as "市委书记吴贤哲".
    Appears in 2026-05 (养老服务), 2026-07 (灾后调研, 常委会会议) government news.
    Plausibly ethnic Korean given Yanbian location and surname pattern (吴 is a common
    Korean Chinese surname). Birth year/education details not yet found on public sources.
  - 黄炳昊(市长): name confirmed from government leadership page with full bio.
    Born 1980-02, male, 朝鲜族, 2004-06 party join, 2003-10 work start,
    graduated from 延边大学 朝鲜语笔译, graduate degree. City secretary of CPC Longjing
    Committee and Mayor. Appointed before 2024 based on news records.
  - 文锡峰(市委副书记): confirmed from 2026-07 news article "市委副书记文锡峰陪同调研"
  - 丁秀龙(市委常委、常务副市长): confirmed from government leadership page + news article
  - 尹东日, 王斌, 康清周, 王志国, 金哲龙, 于占吉, 魏春媛, 李德阳: confirmed as 副市长
    from government leadership page. Some are also 市委常委 based on standard city-county
    leadership structure. Details of party committee positions for most are unconfirmed.
  - 李雄铉(党组成员): confirmed from government leadership page
  - All current-role claims have as-of date 2026-07-25.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "龙井市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_龙井市"
if _CURRENT_DIR.name == "jilin_龙井市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1=市委书记, 2=市长, 3=市委副书记, 4=常务副市长,
#      5-10=副市长, 11=党组成员, 12-17=党委常委(默认标配)

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "吴贤哲",
        "gender": "",
        "ethnicity": "朝鲜族（推定）",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共龙井市委员会",
        "source": "confirmed — 龙井市政府网站新闻多次提及'市委书记吴贤哲'（2026-05至2026-07多篇）",
        "confidence": "confirmed",
        "notes": "市委书记吴贤哲，2026年5月起多次在龙井市政府新闻中出现（调研养老服务、主持市委常委会会议、调研灾后恢复等）。"
            "姓名已通过官方来源确认。出生年月、籍贯、学历等详细信息待补充。根据延边朝鲜族自治州民族构成，推定吴贤哲为朝鲜族。"
    },
    {
        "id": 2,
        "name": "黄炳昊",
        "gender": "男",
        "ethnicity": "朝鲜族",
        "birth": "1980-02",
        "birthplace": "",
        "education": "研究生（延边大学朝鲜语笔译专业）",
        "party_join": "中共党员（2004-06入党）",
        "work_start": "2003-10",
        "current_post": "市委副书记、市长",
        "current_org": "龙井市人民政府",
        "source": "confirmed — 龙井市政府官网领导之窗页面 (http://www.longjing.gov.cn/szf/szfld/sz/)",
        "confidence": "confirmed",
        "notes": "黄炳昊，男，朝鲜族，1980年2月出生，2004年6月入党，2003年10月参加工作，延边大学朝鲜语笔译专业研究生学历。现任龙井市委副书记、市政府市长，主持市政府全面工作，兼管市审计局。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Key Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "文锡峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共龙井市委员会",
        "source": "confirmed — 2026-07-19龙井市政府新闻'吴贤哲到老头沟镇调研灾后恢复工作'中提及'市委副书记文锡峰陪同调研'",
        "confidence": "confirmed",
        "notes": "文锡峰，龙井市委副书记。2026年7月陪同市委书记吴贤哲调研灾后恢复工作。详细信息待补充。"
    },
    {
        "id": 4,
        "name": "丁秀龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长（常务）",
        "current_org": "龙井市人民政府",
        "source": "confirmed — 龙井市政府官网领导之窗 + 2026-07-19新闻'市委常委、常务副市长丁秀龙陪同调研'",
        "confidence": "confirmed",
        "notes": "丁秀龙，龙井市委常委、常务副市长。由龙井市政府网站领导列表和新闻双重确认。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 副市长（名单来自政府官网）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "尹东日",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "龙井市人民政府",
        "source": "confirmed — 龙井市政府官网领导之窗",
        "confidence": "confirmed",
        "notes": "尹东日，龙井市副市长。是否兼任市委常委待确认。"
    },
    {
        "id": 6,
        "name": "王斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "龙井市人民政府",
        "source": "confirmed — 龙井市政府官网领导之窗",
        "confidence": "confirmed",
        "notes": "王斌，龙井市副市长。是否兼任市委常委待确认。"
    },
    {
        "id": 7,
        "name": "康清周",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "龙井市人民政府",
        "source": "confirmed — 龙井市政府官网领导之窗",
        "confidence": "confirmed",
        "notes": "康清周，龙井市副市长。是否兼任市委常委待确认。"
    },
    {
        "id": 8,
        "name": "王志国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "龙井市人民政府",
        "source": "confirmed — 龙井市政府官网领导之窗 + 曾任发改局局长(2023年人大常委会任免)",
        "confidence": "confirmed",
        "notes": "王志国，龙井市副市长。此前曾任龙井市发展和改革局局长（2023年8月免去局长职务）。"
    },
    {
        "id": 9,
        "name": "金哲龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "龙井市人民政府",
        "source": "confirmed — 龙井市政府官网领导之窗",
        "confidence": "confirmed",
        "notes": "金哲龙，龙井市副市长。是否兼任市委常委待确认。"
    },
    {
        "id": 10,
        "name": "于占吉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "龙井市人民政府",
        "source": "confirmed — 龙井市政府官网领导之窗",
        "confidence": "confirmed",
        "notes": "于占吉，龙井市副市长。是否兼任市委常委待确认。"
    },
    {
        "id": 11,
        "name": "魏春媛",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "龙井市人民政府",
        "source": "confirmed — 龙井市政府官网领导之窗",
        "confidence": "confirmed",
        "notes": "魏春媛，龙井市副市长。为龙井市领导班子的女性成员。是否兼任市委常委待确认。"
    },
    {
        "id": 12,
        "name": "李德阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "龙井市人民政府",
        "source": "confirmed — 龙井市政府官网领导之窗",
        "confidence": "confirmed",
        "notes": "李德阳，龙井市副市长。是否兼任市委常委待确认。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 党组成员
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 13,
        "name": "李雄铉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员",
        "current_org": "龙井市人民政府",
        "source": "confirmed — 龙井市政府官网领导之窗",
        "confidence": "confirmed",
        "notes": "李雄铉，龙井市政府党组成员。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县委常委标配职务（姓名待确认）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 14,
        "name": "待查_市纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共龙井市纪律检查委员会",
        "source": "待查 — 默认县级市班子构成推断",
        "confidence": "unverified",
        "notes": "市纪委书记姓名待核实。属县级市标配常委职务。"
    },
    {
        "id": 15,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共龙井市委组织部",
        "source": "待查 — 默认县级市班子构成推断",
        "confidence": "unverified",
        "notes": "市委组织部部长姓名待核实。"
    },
    {
        "id": 16,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共龙井市委宣传部",
        "source": "待查 — 默认县级市班子构成推断",
        "confidence": "unverified",
        "notes": "市委宣传部部长姓名待核实。"
    },
    {
        "id": 17,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共龙井市委政法委员会",
        "source": "待查 — 默认县级市班子构成推断",
        "confidence": "unverified",
        "notes": "市委政法委书记姓名待核实。"
    },
    {
        "id": 18,
        "name": "待查_统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共龙井市委统战部",
        "source": "待查 — 默认县级市班子构成推断",
        "confidence": "unverified",
        "notes": "市委统战部部长姓名待核实。"
    },
    {
        "id": 19,
        "name": "待查_政法委书记（兼公安局长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "龙井市公安局",
        "source": "待查 — 默认县级市政府构成推断",
        "confidence": "unverified",
        "notes": "分管公安的副市长兼公安局长姓名待核实。可能由副市长尹东日或某位副市长兼任。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共龙井市委员会", "type": "党委", "level": "县处级", "parent": "中共延边州委", "location": "龙井市"},
    {"id": 2, "name": "龙井市人民政府", "type": "政府", "level": "县处级", "parent": "延边州人民政府", "location": "龙井市"},
    {"id": 3, "name": "中国人民政治协商会议龙井市委员会", "type": "政协", "level": "县处级", "parent": "政协延边州委", "location": "龙井市"},
    {"id": 4, "name": "龙井市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "延边州人大常委会", "location": "龙井市"},
    {"id": 5, "name": "中共龙井市纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级", "parent": "延边州纪委", "location": "龙井市"},
    {"id": 6, "name": "中共龙井市委组织部", "type": "党委", "level": "县处级", "parent": "中共龙井市委员会", "location": "龙井市"},
    {"id": 7, "name": "中共龙井市委宣传部", "type": "党委", "level": "县处级", "parent": "中共龙井市委员会", "location": "龙井市"},
    {"id": 8, "name": "中共龙井市委政法委员会", "type": "党委", "level": "县处级", "parent": "中共龙井市委员会", "location": "龙井市"},
    {"id": 9, "name": "中共龙井市委统战部", "type": "党委", "level": "县处级", "parent": "中共龙井市委员会", "location": "龙井市"},
    {"id": 10, "name": "龙井市公安局", "type": "政府", "level": "乡科级", "parent": "龙井市人民政府", "location": "龙井市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 吴贤哲 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "2026年5-7月在龙井市政府新闻中多次以市委书记身份出现"},
    # 黄炳昊 — 市长
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "主持市政府全面工作，兼管市审计局"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "市长兼任市委副书记"},
    # 文锡峰 — 市委副书记
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 丁秀龙 — 常务副市长
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长（常务）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管发改、财政、应急等"},
    # 尹东日 — 副市长
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 王斌 — 副市长
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 康清周 — 副市长
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 王志国 — 副市长
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "此前曾任龙井市发改局局长（2023年前）"},
    # 金哲龙 — 副市长
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 于占吉 — 副市长
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 魏春媛 — 副市长
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 李德阳 — 副市长
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 李雄铉 — 政府党组成员
    {"person_id": 13, "org_id": 2, "title": "市政府党组成员", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},
    # 待查_市纪委书记
    {"person_id": 14, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 5, "title": "市纪委书记、市监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_组织部长
    {"person_id": 15, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 6, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_宣传部长
    {"person_id": 16, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 7, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_政法委书记
    {"person_id": 17, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 8, "title": "政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_统战部长
    {"person_id": 18, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 9, "title": "统战部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_兼公安局长
    {"person_id": 19, "org_id": 2, "title": "副市长（兼市公安局局长）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 19, "org_id": 10, "title": "市公安局局长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 书记 — 市长
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "市委书记与市长为党政主要领导搭档关系",
     "overlap_org": "中共龙井市委员会", "overlap_period": "当前", "confidence": "confirmed"},
    # 书记 — 副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "市委书记与市委副书记为党委领导关系",
     "overlap_org": "中共龙井市委员会", "overlap_period": "当前", "confidence": "confirmed"},
    # 书记 — 常务副市长
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "市委书记与常务副市长为党委与政府领导关系",
     "overlap_org": "中共龙井市委员会", "overlap_period": "当前", "confidence": "confirmed"},
    # 市长 — 常务副市长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "市长与常务副市长为政府主要领导与副手关系",
     "overlap_org": "龙井市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    # 市长 — 副市长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "市长与副市长为政府领导关系",
     "overlap_org": "龙井市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "市长与副市长为政府领导关系",
     "overlap_org": "龙井市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "市长与副市长为政府领导关系",
     "overlap_org": "龙井市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "市长与副市长为政府领导关系",
     "overlap_org": "龙井市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "市长与副市长为政府领导关系",
     "overlap_org": "龙井市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "市长与副市长为政府领导关系",
     "overlap_org": "龙井市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "市长与副市长为政府领导关系",
     "overlap_org": "龙井市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "市长与副市长为政府领导关系",
     "overlap_org": "龙井市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    # 副书记 — 常委间的同级关系
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "同为市委常委班子成员",
     "overlap_org": "中共龙井市委员会", "overlap_period": "当前", "confidence": "confirmed"},
    # 市委常委间的同级关系
    {"person_a": 4, "person_b": 14, "type": "overlap",
     "context": "同为市委常委班子成员",
     "overlap_org": "中共龙井市委员会", "overlap_period": "当前", "confidence": "plausible"},
    {"person_a": 14, "person_b": 15, "type": "overlap",
     "context": "同为市委常委班子成员",
     "overlap_org": "中共龙井市委员会", "overlap_period": "当前", "confidence": "unverified"},
    {"person_a": 15, "person_b": 16, "type": "overlap",
     "context": "同为市委常委班子成员",
     "overlap_org": "中共龙井市委员会", "overlap_period": "当前", "confidence": "unverified"},
    {"person_a": 16, "person_b": 17, "type": "overlap",
     "context": "同为市委常委班子成员",
     "overlap_org": "中共龙井市委员会", "overlap_period": "当前", "confidence": "unverified"},
    {"person_a": 17, "person_b": 18, "type": "overlap",
     "context": "同为市委常委班子成员",
     "overlap_org": "中共龙井市委员会", "overlap_period": "当前", "confidence": "unverified"},
]

# ── Person JSONs ─────────────────────────────────────────────────────────────

PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "吉林省",
        "city": "延边朝鲜族自治州",
        "region": "龙井市",
        "task_id": "jilin_龙井市",
        "time_focus": "2026年7月",
    },
    "identity": {},
    "current_status": {},
    "career_timeline": [],
    "organizations": [],
    "relationships": [],
    "governance_record": [],
    "professional_profile": {},
    "work_style_and_personality": {},
    "network_metrics": {},
    "risk_and_integrity_signals": [],
    "source_register": [],
    "confidence_summary": {},
    "open_questions": [],
}


def build_wuxianzhe_json() -> dict:
    name = "吴贤哲"
    today_str = TODAY

    person = {
        "identity": {
            "person_id": "jilin_yanbian_longjing_wuxianzhe",
            "name": name,
            "aliases": [],
            "gender": "",
            "ethnicity": "朝鲜族（推定）",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "吴贤哲_",
                "name_birthplace": "吴贤哲_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": "市委书记",
            "current_org": "中共龙井市委员会",
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "中共龙井市委员会",
                "title": "市委书记",
                "level": "",
                "location": "龙井市",
                "system": "party",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "2026年5月至7月多次以龙井市委书记身份出席活动（调研养老服务、主持常委会、调研灾后恢复）",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002", "S003"],
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "黄炳昊",
                "person_id": "jilin_yanbian_longjing_huangbinghao",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "市委书记与市长为党政主要领导搭档",
                "overlap_org": "中共龙井市委员会",
                "overlap_period": "当前",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "person": "文锡峰",
                "person_id": "jilin_yanbian_longjing_wenxifeng",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "市委书记与副书记为党委领导关系，2026-07-19一同调研灾后恢复",
                "overlap_org": "中共龙井市委员会",
                "overlap_period": "当前",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            },
            {
                "person": "丁秀龙",
                "person_id": "jilin_yanbian_longjing_dingxiulong",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "市委书记与常务副市长为党委与政府领导关系，2026-07-19一同调研",
                "overlap_org": "中共龙井市委员会",
                "overlap_period": "当前",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            },
        ],
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "赴老头沟镇调研灾后恢复工作，检查桥梁受损和防汛准备",
                "role_in_event": "主持座谈会，部署灾后恢复和防汛工作",
                "measurable_outcome": "提出加快基础设施修复、优化应急预案等要求",
                "location": "龙井市老头沟镇",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            },
            {
                "period": "2026-06",
                "domain": "other",
                "achievement_or_event": "调研养老服务领域专项整治工作落实情况",
                "role_in_event": "调研养老服务领域专项整治",
                "measurable_outcome": "",
                "location": "龙井市",
                "confidence": "confirmed",
                "source_ids": ["S004"],
            },
            {
                "period": "2026-07-10",
                "domain": "other",
                "achievement_or_event": "主持市委2026年第9次常委会会议，传达学习习近平总书记重要讲话和全国党建工作座谈会精神",
                "role_in_event": "主持会议并讲话",
                "measurable_outcome": "部署学习贯彻讲话精神、防汛备汛、党建学习等工作",
                "location": "龙井市",
                "confidence": "confirmed",
                "source_ids": ["S003"],
            },
        ],
        "professional_profile": {
            "primary_specializations": ["党务管理", "应急管理"],
            "secondary_specializations": ["养老服务", "基层治理"],
            "career_pattern": "unknown",
            "systems_experience": ["party"],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "详细履历未获，无法评估晋升速度",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "grassroots_oriented",
                    "evidence": "2026-07-19亲赴灾后一线调研，到桥梁、粮库等现场查看",
                    "confidence": "confirmed",
                    "source_ids": ["S002"],
                },
                {
                    "trait": "discipline_oriented",
                    "evidence": "在常委会会议上强调'两个确立'、'两个维护'、从严治党",
                    "confidence": "confirmed",
                    "source_ids": ["S003"],
                },
            ],
            "speech_themes": ["人民至上、生命至上", "从严治党", "应急体系建设"],
            "management_signals": ["要求逐条梳理问题、逐项查摆不足", "强调应急预案实操性"],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026-07-25，未发现吴贤哲相关风险信号",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {"id": "S001", "title": "龙井市政府领导之窗", "url": "http://www.longjing.gov.cn/szf/szfld/",
             "publisher": "龙井市人民政府", "published_at": "",
             "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S002", "title": "吴贤哲到老头沟镇调研灾后恢复工作", "url": "http://www.longjing.gov.cn/zw/ljyw/202607/t20260720_580648.html",
             "publisher": "龙井市融媒体中心", "published_at": "2026-07-19",
             "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S003", "title": "市委召开2026年第9次常委会会议", "url": "http://www.longjing.gov.cn/zw/ljyw/202607/t20260710_580190.html",
             "publisher": "龙井市人民政府", "published_at": "2026-07-10",
             "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S004", "title": "吴贤哲调研养老服务领域专项整治工作落实情况",
             "url": "http://www.longjing.gov.cn/zw/ljyw/",
             "publisher": "龙井市人民政府", "published_at": "2026-06",
             "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "新闻标题在首页可见，具体页面URL待确认"},
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "吴贤哲的出生年月、籍贯、学历、完整履历均未找到。推测为朝鲜族但未确证。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "吴贤哲的出生年月、籍贯和民族是什么？",
                "why_it_matters": "核心目标人物身份信息不完整",
                "suggested_queries": ["吴贤哲 简历 龙井", "吴贤哲 出生 延边"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "吴贤哲的完整履历（包括此前担任的职务）是什么？",
                "why_it_matters": "了解其晋升路径和关系网络",
                "suggested_queries": ["吴贤哲 龙井市委书记 履历", "吴贤哲 延边"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "吴贤哲何时开始担任龙井市委书记？前任是谁？",
                "why_it_matters": "了解领导交替时间线和前任网络",
                "suggested_queries": ["龙井市委 任免 2024 2025 书记", "龙井市前任市委书记"],
                "last_attempted": AS_OF,
            },
        ],
    }
    return person


def build_huangbinghao_json() -> dict:
    name = "黄炳昊"
    today_str = TODAY

    person = {
        "identity": {
            "person_id": "jilin_yanbian_longjing_huangbinghao",
            "name": name,
            "aliases": [],
            "gender": "男",
            "ethnicity": "朝鲜族",
            "birth": "1980-02",
            "birthplace": "",
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": "延边大学",
                    "major": "朝鲜语笔译",
                    "degree": "研究生",
                    "study_type": "unknown",
                    "source_ids": ["S005"],
                }
            ],
            "party_join": "2004-06",
            "work_start": "2003-10",
            "dedupe_keys": {
                "name_birth": "黄炳昊_198002",
                "name_birthplace": "黄炳昊_",
                "official_profile_url": "http://www.longjing.gov.cn/szf/szfld/sz/",
            },
        },
        "current_status": {
            "current_post": "市委副书记、市长",
            "current_org": "龙井市人民政府",
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S005"],
        },
        "career_timeline": [
            {
                "start": "2003-10",
                "end": "unknown",
                "org": "",
                "title": "参加工作",
                "level": "",
                "location": "",
                "system": "unknown",
                "rank": "",
                "is_key_promotion": False,
                "notes": "2003年10月参加工作，具体岗位未详",
                "confidence": "plausible",
                "source_ids": ["S005"],
            },
            {
                "start": "unknown",
                "end": "present",
                "org": "龙井市人民政府",
                "title": "龙井市委副书记、市长",
                "level": "",
                "location": "龙井市",
                "system": "government",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "主持市政府全面工作，兼管市审计局",
                "confidence": "confirmed",
                "source_ids": ["S005"],
            },
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "吴贤哲",
                "person_id": "jilin_yanbian_longjing_wuxianzhe",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "市长在市委书记领导下工作，为党政主要领导搭档",
                "overlap_org": "中共龙井市委员会",
                "overlap_period": "当前",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S005"],
            },
            {
                "person": "丁秀龙",
                "person_id": "jilin_yanbian_longjing_dingxiulong",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "市长与常务副市长为政府主要领导关系",
                "overlap_org": "龙井市人民政府",
                "overlap_period": "当前",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S005"],
            },
        ],
        "governance_record": [
            {
                "period": "当前",
                "domain": "economic_development",
                "achievement_or_event": "主持市政府全面工作，兼管审计",
                "role_in_event": "市政府主要负责人",
                "measurable_outcome": "",
                "location": "龙井市",
                "confidence": "confirmed",
                "source_ids": ["S005"],
            },
        ],
        "professional_profile": {
            "primary_specializations": ["行政管理", "审计监督"],
            "secondary_specializations": ["朝鲜语翻译"],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "1980年出生，2003年参加工作，2026年已任龙井市长。具体晋升节点待查。",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "technocratic",
                    "evidence": "拥有延边大学研究生学历，朝鲜语笔译专业",
                    "confidence": "confirmed",
                    "source_ids": ["S005"],
                },
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026-07-25，未发现黄炳昊相关风险信号",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {"id": "S005", "title": "黄炳昊（市长）领导简历", "url": "http://www.longjing.gov.cn/szf/szfld/sz/",
             "publisher": "龙井市人民政府", "published_at": "",
             "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "包含出生年月、民族、入党时间、参加工作时间和学历信息"},
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "黄炳昊此前担任职务的履历信息缺失（2003年参加工作至任市长之间的经历）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "黄炳昊的完整履历（此前担任职务）是什么？",
                "why_it_matters": "了解其晋升路径和关系网络",
                "suggested_queries": ["黄炳昊 龙井市长 履历", "黄炳昊 延边"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "黄炳昊何时开始担任龙井市长？前任是谁？",
                "why_it_matters": "了解领导交替时间线和前任网络",
                "suggested_queries": ["龙井市市长 任命 2023 2024", "龙井市前任市长"],
                "last_attempted": AS_OF,
            },
        ],
    }
    return person


def build_wenxifeng_json() -> dict:
    name = "文锡峰"
    today_str = TODAY

    person = {
        "identity": {
            "person_id": "jilin_yanbian_longjing_wenxifeng",
            "name": name,
            "aliases": [],
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "文锡峰_",
                "name_birthplace": "文锡峰_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": "市委副书记",
            "current_org": "中共龙井市委员会",
            "administrative_rank": "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S002"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "中共龙井市委员会",
                "title": "市委副书记",
                "level": "",
                "location": "龙井市",
                "system": "party",
                "rank": "县处级副职",
                "is_key_promotion": False,
                "notes": "2026年7月以市委副书记身份陪同书记调研",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "吴贤哲",
                "person_id": "jilin_yanbian_longjing_wuxianzhe",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "2026-07-19陪同书记调研灾后恢复",
                "overlap_org": "中共龙井市委员会",
                "overlap_period": "当前",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            },
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现风险信号",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {"id": "S002", "title": "吴贤哲到老头沟镇调研灾后恢复工作",
             "url": "http://www.longjing.gov.cn/zw/ljyw/202607/t20260720_580648.html",
             "publisher": "龙井市融媒体中心", "published_at": "2026-07-19",
             "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "文锡峰的出生年月、籍贯、学历和完整履历完全未知",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "文锡峰的基本信息（出生年月、籍贯、民族、学历）和完整履历是什么？",
                "why_it_matters": "重要副职领导，关系网络关键节点",
                "suggested_queries": ["文锡峰 龙井 简历", "文锡峰 延边"],
                "last_attempted": AS_OF,
            },
        ],
    }
    return person


def build_dingxiulong_json() -> dict:
    name = "丁秀龙"
    today_str = TODAY

    person = {
        "identity": {
            "person_id": "jilin_yanbian_longjing_dingxiulong",
            "name": name,
            "aliases": [],
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "丁秀龙_", "name_birthplace": "丁秀龙_", "official_profile_url": ""},
        },
        "current_status": {
            "current_post": "市委常委、副市长（常务）",
            "current_org": "龙井市人民政府",
            "administrative_rank": "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "龙井市人民政府",
                "title": "市委常委、常务副市长",
                "level": "",
                "location": "龙井市",
                "system": "government",
                "rank": "县处级副职",
                "is_key_promotion": False,
                "notes": "在政府领导之窗和新闻中均有出现",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"],
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "吴贤哲",
                "person_id": "jilin_yanbian_longjing_wuxianzhe",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "陪同书记调研灾后恢复工作",
                "overlap_org": "中共龙井市委员会",
                "overlap_period": "当前",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            },
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [],
                                        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现风险信号", "date": AS_OF, "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "龙井市政府领导之窗", "url": "http://www.longjing.gov.cn/szf/szfld/",
             "publisher": "龙井市人民政府", "published_at": "",
             "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S002", "title": "吴贤哲调研灾后恢复工作",
             "url": "http://www.longjing.gov.cn/zw/ljyw/202607/t20260720_580648.html",
             "publisher": "龙井市融媒体中心", "published_at": "2026-07-19",
             "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "丁秀龙的基本信息和完整履历完全未知",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "丁秀龙的基本信息（出生年月、籍贯、学历）和完整履历是什么？",
                "why_it_matters": "常务副市长为政府关键副职",
                "suggested_queries": ["丁秀龙 龙井 简历"],
                "last_attempted": AS_OF,
            },
        ],
    }
    return person


def build_unverified_person_json(person_id: int) -> dict:
    """Build a thin person JSON for unverified (待查) persons."""
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    now = TODAY

    person = {
        "identity": {
            "person_id": f"jilin_yanbian_longjing_{name}",
            "name": name,
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": [],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": p["current_org"],
                "title": p["current_post"],
                "level": "",
                "location": "龙井市",
                "system": "party",
                "rank": "县处级副职",
                "is_key_promotion": False,
                "notes": p["notes"],
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"No risk signals found — {name} is placeholder for unverified leader",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"姓名完全未知。{role_label}姓名需通过市委组织部公示或新闻报道核实。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"龙井市{role_label}姓名是什么？",
                "why_it_matters": "核心班子成员，完整调查必须确认",
                "suggested_queries": [
                    f"龙井市 {p['current_post']}",
                    f"龙井市委 人事任免 {p['current_post']}",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历和完整履历",
                "why_it_matters": "身份确认后需补充完整履历",
                "suggested_queries": [f"龙井市 {p['current_post']} 简历"],
                "last_attempted": AS_OF,
            },
        ],
    }
    return person


def write_person_json(filename: str, data: dict):
    path = PJSON_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    # Build DB and GEXF
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

    # Write person JSONs
    person_files = []

    # 吴贤哲 (市委书记)
    person_files.append(str(write_person_json(
        f"{TODAY}-吉林省-延边朝鲜族自治州-市委书记-吴贤哲.json",
        build_wuxianzhe_json(),
    )))

    # 黄炳昊 (市长)
    person_files.append(str(write_person_json(
        f"{TODAY}-吉林省-延边朝鲜族自治州-市长-黄炳昊.json",
        build_huangbinghao_json(),
    )))

    # 文锡峰 (市委副书记)
    person_files.append(str(write_person_json(
        f"{TODAY}-吉林省-延边朝鲜族自治州-市委副书记-文锡峰.json",
        build_wenxifeng_json(),
    )))

    # 丁秀龙 (常务副市长)
    person_files.append(str(write_person_json(
        f"{TODAY}-吉林省-延边朝鲜族自治州-常务副市长-丁秀龙.json",
        build_dingxiulong_json(),
    )))

    # Unverified persons (待查)
    for pid in [14, 15, 16, 17, 18, 19]:
        pdata = build_unverified_person_json(pid)
        p = {x["id"]: x for x in persons}[pid]
        name = p["name"]
        role_label = p["current_post"]
        safe_role = role_label.replace("、", "_")
        person_files.append(str(write_person_json(
            f"{TODAY}-吉林省-延边朝鲜族自治州-{safe_role}-{name}.json",
            pdata,
        )))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"\nResearch summary:")
    print(f"  - 市委书记吴贤哲: confirmed (姓名确认，其他信息待补充)")
    print(f"  - 市长黄炳昊: confirmed (姓名、出生、民族、学历均已确认)")
    print(f"  - 市委副书记文锡峰: confirmed (姓名确认，其他信息待补充)")
    print(f"  - 常务副市长丁秀龙: confirmed (姓名确认，其他信息待补充)")
    print(f"  - 9位副市长/党组成员: confirmed (名单来自政府官网)")
    print(f"  - 6位常委标配职务: 待查 (纪委书记、组织部长、宣传部长、政法委书记、统战部长、公安局长)")
    print(f"Done.")


if __name__ == "__main__":
    main()
