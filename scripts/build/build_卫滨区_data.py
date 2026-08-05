#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 卫滨区, 新乡市, 河南省.

Level: 市辖区
Province: 河南省
Parent city: 新乡市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: henan_卫滨区

Research date: 2026-08-05
Official source: http://www.wbq.gov.cn/ (卫滨区人民政府)

Current status (as of 2026-08-05):
- 区委书记: 邓国永  (自 2026-04-28 起, 全区领导干部会议宣布)
- 区长: 王西忠     (此前任区委副书记, 2026 年年中接任区长)

Key sources:
- 卫滨区召开全区领导干部会议 (2026-04-29): 邓国永任区委书记, 李海潮不再担任
  → http://www.wbq.gov.cn/xwzx/xwzx/1280811.html
- 卫滨区人民政府"领导之窗" (2026 更新): 王西忠(区长)、张华(常务副区长)、陈鹏飞、李成国、张凤琴、李帅军、桑明磊
- 卫滨区十五届人大常委会第三十一次会议 (2025-12-29): 钱伟(纪委书记)、向卫群(政协副主席/财政局长)、王倩(法院院长)、李新领(检察长)
- 卫滨区十五届人大常委会第三十七次会议 (2026-06-29): 王西忠正式当选程序推进 (区人代会第八次会议)
- 2025年度党委书记抓基层党建述职评议会议 (2026-02-26): 李海潮(时任副市长兼区委书记)、魏海晓(区长)、王西忠(区委副书记)、钱伟、张胜利、周伟、于智、荆会云、冀大旭、向卫群

Predecessors:
- 区委书记前任: 李海潮 (2021-2026, 五年, 升任新乡市副市长)
- 区长前任: 魏海晓 (任职至 2026 年约 6 月)

Confirmed relationship evidence / work-network:
- 邓国永(书记) × 王西忠(区长): 现任区委-政府一把手搭班子
- 邓国永 ↔ 李海潮: 区委书记 交接 (李海潮→邓国永)
- 王西忠 ↔ 魏海晓: 区长 交接 (王西忠接任魏海晓)
- 赵俊芳(区人大常委会主任) 曾任 区委常委、组织部长 (区内晋升路径)

Note on confidence: 任职时间和任期等按官方新闻确认; 个人出生年月/学历来自政府领导之窗页面;
出生地、早期履历等未公开处标为 uncertain / 缺。
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "卫滨区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-05"
TODAY = "20260805"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 邓国永 — 区委书记
    {
        "id": 1,
        "name": "邓国永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共新乡市卫滨区委员会",
        "source": "http://www.wbq.gov.cn/xwzx/xwzx/1280811.html — 卫滨区召开全区领导干部会议 (2026-04-29) 宣布邓国永任区委书记",
    },

    # 2. 王西忠 — 区委副书记、区长
    {
        "id": 2,
        "name": "王西忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-11",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "卫滨区人民政府",
        "source": "http://www.wbq.gov.cn/zfxxgk/ldzc/index.html — 区政府领导之窗 王西忠简历; 新闻: 区长王西忠到先进制造业开发区调研 (2026-07-06)",
    },

    # 3. 张华 — 区委常委、区政府党组副书记、常务副区长
    {
        "id": 3,
        "name": "张华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-03",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区政府党组副书记、副区长（常务）",
        "current_org": "卫滨区人民政府",
        "source": "http://www.wbq.gov.cn/zfxxgk/ldzc/index.html — 卫滨区政府领导之窗 张华简历",
    },

    # 4. 陈鹏飞 — 区委常委、副区长
    {
        "id": 4,
        "name": "陈鹏飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989-08",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "卫滨区人民政府",
        "source": "http://www.wbq.gov.cn/zfxxgk/ldzc/index.html — 卫滨区政府领导之窗 陈鹏飞简历",
    },

    # 5. 李成国 — 副区长、市公安局卫滨分局局长
    {
        "id": 5,
        "name": "李成国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、新乡市公安局卫滨分局局长",
        "current_org": "卫滨区人民政府",
        "source": "http://www.wbq.gov.cn/zfxxgk/ldzc/index.html — 卫滨区政府领导之窗 李成国简历",
    },

    # 6. 张凤琴 — 副区长
    {
        "id": 6,
        "name": "张凤琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975-03",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "卫滨区人民政府",
        "source": "http://www.wbq.gov.cn/zfxxgk/ldzc/index.html — 卫滨区政府领导之窗 张凤琴简历",
    },

    # 7. 李帅军 — 副区长、区自由路街道党工委书记
    {
        "id": 7,
        "name": "李帅军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-07",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、自由路街道党工委书记",
        "current_org": "卫滨区人民政府",
        "source": "http://www.wbq.gov.cn/zfxxgk/ldzc/index.html — 卫滨区政府领导之窗 李帅军简历",
    },

    # 8. 桑明磊 — 副区长
    {
        "id": 8,
        "name": "桑明磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-03",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "卫滨区人民政府",
        "source": "http://www.wbq.gov.cn/zfxxgk/ldzc/index.html — 卫滨区政府领导之窗 桑明磊简历",
    },

    # 9. 钱伟 — 区委常委、区纪委书记、区监委主任
    {
        "id": 9,
        "name": "钱伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共新乡市卫滨区纪律检查委员会",
        "source": "http://www.wbq.gov.cn/xwzx/xwzx/1280430.html — 区人大常委会第三十一次会议 (2025-12-29) 列席名单",
    },

    # 10. 丁福友 — 区委常委、政法委书记
    {
        "id": 10,
        "name": "丁福友",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共新乡市卫滨区委员会",
        "source": "http://www.wbq.gov.cn/ — 区委常委、政法委书记丁福友出席区级会议新闻",
    },

    # 11. 赵俊芳 — 区人大常委会主任（原区委常委、组织部部长）
    {
        "id": 11,
        "name": "赵俊芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "新乡市卫滨区人民代表大会常务委员会",
        "source": "http://www.wbq.gov.cn/xwzx/xwzx/1291041.html — 十五届人大常委会第三十七次会议 (2026-06-29) 主持人",
    },

    # 12. 向卫群 — 区政协副主席、区财政局局长
    {
        "id": 12,
        "name": "向卫群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席、区财政局局长",
        "current_org": "中国人民政治协商会议新乡市卫滨区委员会",
        "source": "http://www.wbq.gov.cn/xwzx/xwzx/1280430.html — 区人大常委会第三十一次会议列席名单 (2025-12-29)",
    },

    # 13. 王倩 — 区人民法院院长
    {
        "id": 13,
        "name": "王倩",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民法院院长",
        "current_org": "新乡市卫滨区人民法院",
        "source": "http://www.wbq.gov.cn/xwzx/xwzx/1280430.html — 区人大常委会第三十一次会议列席名单 (2025-12-29)",
    },

    # 14. 李新领 — 区人民检察院检察长
    {
        "id": 14,
        "name": "李新领",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民检察院检察长",
        "current_org": "新乡市卫滨区人民检察院",
        "source": "http://www.wbq.gov.cn/xwzx/xwzx/1280430.html — 区人大常委会第三十一次会议列席名单 (2025-12-29)",
    },

    # 15. 李海潮 — 前任区委书记（2021-2026, 现新乡市政府副市长）
    {
        "id": 15,
        "name": "李海潮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新乡市人民政府副市长（前任卫滨区委书记, 2026-04 起）",
        "current_org": "新乡市人民政府",
        "source": "http://www.wbq.gov.cn/xwzx/xwzx/1280811.html — 全区领导干部会议, 李海潮以市政府副市长身份主持会议并卸任",
    },

# 16. 魏海晓 — 前任区长
    {
        "id": 16,
        "name": "魏海晓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区长（魏海晓, 任职至 2026 年/年中, 去向待查）",
        "current_org": "卫滨区人民政府",
        "source": "http://www.wbq.gov.cn/ — 区长魏海晓系列调研新闻 (2025-2026); 后由王西忠接任",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共新乡市卫滨区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共新乡市委员会",
        "location": "河南省新乡市卫滨区",
    },
    {
        "id": 2,
        "name": "卫滨区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "新乡市人民政府",
        "location": "河南省新乡市卫滨区",
    },
    {
        "id": 3,
        "name": "中共新乡市卫滨区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "新乡市纪委监委",
        "location": "河南省新乡市卫滨区",
    },
    {
        "id": 4,
        "name": "新乡市公安局卫滨公安分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "新乡市公安局",
        "location": "河南省新乡市卫滨区",
    },
    {
        "id": 5,
        "name": "卫滨区自由路街道党工委",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共新乡市卫滨区委员会",
        "location": "河南省新乡市卫滨区",
    },
    {
        "id": 6,
        "name": "新乡市卫滨区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "新乡市人大常委会",
        "location": "河南省新乡市卫滨区",
    },
    {
        "id": 7,
        "name": "中国人民政治协商会议新乡市卫滨区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协新乡市委员会",
        "location": "河南省新乡市卫滨区",
    },
    {
        "id": 8,
        "name": "新乡市卫滨区人民法院",
        "type": "司法",
        "level": "县处级",
        "parent": "新乡市中级人民法院",
        "location": "河南省新乡市卫滨区",
    },
    {
        "id": 9,
        "name": "新乡市卫滨区人民检察院",
        "type": "司法",
        "level": "县处级",
        "parent": "新乡市人民检察院",
        "location": "河南省新乡市卫滨区",
    },
    {
        "id": 10,
        "name": "新乡市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "河南省人民政府",
        "location": "河南省新乡市",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 邓国永 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-04", "end_date": "", "rank": "县处级正职", "note": "自2026-04-28全区领导干部会议任命"},
    # 王西忠 — 区委副书记、区长
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "此前任区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "2026年接任"},
    # 张华 — 区委常委、常务副区长
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "区政府党组副书记、副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "常务副区长"},
    # 陈鹏飞 — 区委常委、副区长
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 李成国 — 副区长、公安分局局长
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "兼任公安分局长"},
    {"person_id": 5, "org_id": 4, "title": "新乡市公安局卫滨分局局长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    # 张凤琴 — 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "党外干部"},
    # 李帅军 — 副区长、自由路街道党工委书记
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "自由路街道党工委书记", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    # 桑明磊 — 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 钱伟 — 区委常委、纪委书记
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 3, "title": "区纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 丁福友 — 区委常委、政法委书记
    {"person_id": 10, "org_id": 1, "title": "区委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 赵俊芳 — 区人大常委会主任
    {"person_id": 11, "org_id": 6, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "曾任区委常委、组织部长"},
    # 向卫群 — 区政协副主席、财政局长
    {"person_id": 12, "org_id": 7, "title": "区政协副主席", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "兼财政局长"},
    {"person_id": 12, "org_id": 2, "title": "区财政局局长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    # 王倩 — 法院院长
    {"person_id": 13, "org_id": 8, "title": "区人民法院院长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 李新领 — 检察院检察长
    {"person_id": 14, "org_id": 9, "title": "区人民检察院检察长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 李海潮 — 前任区委书记(升任副市长)
    {"person_id": 15, "org_id": 1, "title": "区委书记", "start_date": "2021-11", "end_date": "2026-04", "rank": "县处级正职", "note": "2021-2026, 后升任新乡市副市长"},
    {"person_id": 15, "org_id": 10, "title": "新乡市人民政府副市长", "start_date": "2026-04", "end_date": "", "rank": "地级市副职", "note": "2026-04 起担任"},
    # 魏海晓 — 前任区长
    {"person_id": 16, "org_id": 2, "title": "区长", "start_date": "", "end_date": "2026", "rank": "县处级正职", "note": "前任区长, 去向待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 邓国永 ↔ 王西忠（现任书记-区长搭班子, confirmed）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "邓国永任区委书记、王西忠任区长——现任区委-政府一把手搭班子", "overlap_org": "中共新乡市卫滨区委员会/卫滨区人民政府", "overlap_period": "2026-04至今"},
    # 邓国永 ↔ 张华（书记-常务副区长）
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "邓国永书记领导区委全面工作, 张华任区委常委、常务副区长", "overlap_org": "中共新乡市卫滨区委员会", "overlap_period": "2026-04至今"},
    # 邓国永 ↔ 陈鹏飞（书记-常委副区长）
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "邓国永书记领导区委全面工作, 陈鹏飞任区委常委、副区长", "overlap_org": "中共新乡市卫滨区委员会", "overlap_period": "2026-04至今"},
    # 王西忠 ↔ 张华（区长-常务副区长工作搭档）
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "王西忠区长主持区政府全面工作, 张华常务副区长协助", "overlap_org": "卫滨区人民政府", "overlap_period": "2026年至今"},
    # 王西忠 ↔ 陈鹏飞（区长-副区长工作搭档）
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "王西忠区长领导区政府, 陈鹏飞任副区长", "overlap_org": "卫滨区人民政府", "overlap_period": "2026年至今"},
    # 邓国永 ↔ 李海潮（前任书记交接, predecessor_successor）
    {"person_a": 1, "person_b": 15, "type": "predecessor_successor", "context": "邓国永接任李海潮为卫滨区委书记(2026-04), 李海潮升任新乡市副市长", "overlap_org": "中共新乡市卫滨区委员会", "overlap_period": "2026-04交接"},
    # 王西忠 ↔ 魏海晓（前任区长交接, predecessor_successor）
    {"person_a": 2, "person_b": 16, "type": "predecessor_successor", "context": "王西忠接任魏海晓为区长", "overlap_org": "卫滨区人民政府", "overlap_period": "2026年交接"},
    # 邓国永 ↔ 钱伟（书记-纪委书记）
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "邓国永任区委书记, 钱伟任区委常委、纪委书记、监委主任", "overlap_org": "中共新乡市卫滨区委员会/区纪委", "overlap_period": "2026年至今"},
    # 王西忠 ↔ 钱伟（区长-纪委书记）
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "王西忠任区长, 钱伟任区纪委书记", "overlap_org": "中共新乡市卫滨区委员会", "overlap_period": "2026年至今"},
    # 邓国永 ↔ 丁福友（书记-政法委书记）
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "邓国永任区委书记, 丁福友任区委常委、政法委书记", "overlap_org": "中共新乡市卫滨区委员会", "overlap_period": "2026年至今"},
    # 张华 ↔ 陈鹏飞（同为政府副职）
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "张华常务副区长与陈鹏飞常委副区长同为区政府班子成员", "overlap_org": "卫滨区人民政府", "overlap_period": "2026年至今"},
    # 邓国永 ↔ 赵俊芳（书记-人大主任）
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "邓国永任区委书记, 赵俊芳任区人大常委会主任", "overlap_org": "新乡市卫滨区人民代表大会常务委员会", "overlap_period": "2026年至今"},
    # 李海潮 ↔ 赵俊芳（区委班子成员晋升路径）
    {"person_a": 15, "person_b": 11, "type": "overlap", "context": "李海潮任区委书记期间, 赵俊芳曾任区委常委、组织部部长并晋升人大主任", "overlap_org": "中共新乡市卫滨区委员会", "overlap_period": "2021-2026"},
    # 向卫群（全区领导多机构）— 与书记常委班子关系
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "邓国永任区委书记, 向卫群任区政协副主席、财政局长", "overlap_org": "中国人民政治协商会议新乡市卫滨区委员会", "overlap_period": "2026年至今"},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict) -> None:
    """Write a single person's graph JSON."""
    pid = person["id"]
    name = person["name"]
    # Determine job abbreviation for filename (核心 2 人 + 关键 副职)
    job_map = {
        1: "区委书记",
        2: "区长",
        3: "常务副区长",
        4: "常委副区长",
        5: "副区长兼公安局长",
        6: "副区长",
        7: "街办副区长",
        8: "副区长",
        9: "纪委书记",
        10: "政法委书记",
        11: "人大主任",
        12: "政协副主席",
        13: "法院院长",
        14: "检察长",
        15: "前区委书记",
        16: "前区长",
    }
    job = job_map.get(pid, "常委")

    filename = f"{TODAY}-河南省-新乡市-{job}-{name}.json"
    filepath = PERSONS_DIR / filename

    rels_out = []
    for r in relationships:
        other_id = None
        direction = "undirected"
        if r["person_a"] == pid:
            other_id = r["person_b"]
            direction = "person_to_other"
        elif r["person_b"] == pid:
            other_id = r["person_a"]
            direction = "other_to_person"

        if other_id is not None:
            other_person = next((p for p in persons if p["id"] == other_id), None)
            if other_person:
                rels_out.append({
                    "person": other_person["name"],
                    "person_id": f"weibin_{other_person['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] in ("overlap", "predecessor_successor", "superior_subordinate") else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": direction,
                    "confidence": "confirmed" if r["type"] == "overlap" else "plausible",
                })

    positions_out = []
    for pos in positions:
        if pos["person_id"] == pid:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            positions_out.append({
                "start": pos["start_date"] or "unknown",
                "end": pos["end_date"] or "present",
                "org": org["name"] if org else "",
                "title": pos["title"],
                "level": pos["rank"],
                "location": "河南省新乡市卫滨区",
                "system": "party" if org and ("区委" in org["name"] or "纪委" in org["name"] or "党工委" in org["name"]) else ("government" if org and ("人民政府" in org["name"] or "公安" in org["name"]) else ("judicial" if org and ("法院" in org["name"] or "检察院" in org["name"]) else "government")),
                "rank": pos["rank"],
                "is_key_promotion": False,
                "notes": pos["note"],
                "confidence": "confirmed" if pos.get("start_date") else "plausible",
                "source_ids": ["S001"],
            })

    person_json = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "新乡市",
            "region": "卫滨区",
            "job": job,
            "task_id": "henan_卫滨区",
            "time_focus": "2026-04至今 (邓国永书记上任以来)",
        },
        "identity": {
            "person_id": f"weibin_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", "汉族"),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{
                "period": "",
                "institution": person.get("education", ""),
                "major": "",
                "degree": person.get("education", ""),
                "study_type": "unknown",
                "source_ids": ["S001"],
            }] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": f"http://www.wbq.gov.cn/zfxxgk/ldzc/index.html",
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级正职" if pid in (1, 2, 11) else ("地级市正职" if pid == 15 else "县处级副职"),
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": positions_out,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_out,
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
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "卫滨区人民政府 — 政府领导之窗",
                "url": "http://www.wbq.gov.cn/zfxxgk/ldzc/index.html",
                "publisher": "卫滨区人民政府",
                "published_at": "2026",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "官方政府领导/领导之窗页面, 列出区长、副区长及其简历",
            },
            {
                "id": "S002",
                "title": "卫滨区召开全区领导干部会议",
                "url": "http://www.wbq.gov.cn/xwzx/xwzx/1280811.html",
                "publisher": "卫滨区人民政府",
                "published_at": "2026-04-29",
                "accessed_at": AS_OF,
                "source_type": "appointment_notice",
                "reliability": "high",
                "notes": "宣布邓国永任区委书记, 李海潮卸任并已任新乡市副市长",
            },
            {
                "id": "S003",
                "title": "卫滨区十五届人大常委会第三十七次会议召开",
                "url": "http://www.wbq.gov.cn/xwzx/xwzx/1291041.html",
                "publisher": "卫滨区人民政府",
                "published_at": "2026-06-29",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "赵俊芳任区人大主任, 筹备区人代会第八次会议选举",
            },
            {
                "id": "S004",
                "title": "卫滨区十五届人大常委会第三十一次会议召开",
                "url": "http://www.wbq.gov.cn/xwzx/xwzx/1280430.html",
                "publisher": "卫滨区人民政府",
                "published_at": "2025-12-29",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认钱伟(纪委书记)、冀大旭(副区长)、王倩(法院)、李新领(检察院)名单",
            },
            {
                "id": "S005",
                "title": "2025年度党委(党组)书记抓基层党建述职评议会议",
                "url": "http://www.wbq.gov.cn/xwzx/xwzx/1280625.html",
                "publisher": "卫滨区人民政府",
                "published_at": "2026-02-26",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "时任副市长、区委书记李海潮主持, 列明 王西忠、钱伟 等区领导班子名单",
            },
            {
                "id": "S006",
                "title": "区长王西忠到先进制造业开发区调研",
                "url": "http://www.wbq.gov.cn/xwzx/xwzx/1292169.html",
                "publisher": "卫滨区人民政府",
                "published_at": "2026-07-06",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认王西忠现任区长",
            },
        ],
        "confidence_summary": {
            "identity": "plausible" if person.get("birth") else "unverified",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": f"缺少{name}的详细履历（早期职业生涯、教育背景、出生地、政治面貌发展时间线）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的详细职业履历（历任职务、调动时间线）",
                "why_it_matters": "无法了解其晋升路径、系统经验和来源地区, 难以判断其关系网络和职业背景",
                "suggested_queries": [f"{name} 简历", f"{name} 任职经历", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的出生地和出生年月",
                "why_it_matters": "出生信息是人员去重和同乡关系判断的重要依据",
                "suggested_queries": [f"{name} 出生", f"{name} 籍贯"],
                "last_attempted": AS_OF,
            },
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} network data...")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()

    # Write person JSON files for core leaders
    print("Person JSONs:")
    for p in persons:
        write_person_json(p)

    print()

    # Build database and GEXF
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

    # Verify output
    print()
    print("Verification:")
    db_size = DB_PATH.stat().st_size if DB_PATH.exists() else 0
    gexf_size = GEXF_PATH.stat().st_size if GEXF_PATH.exists() else 0
    print(f"  {SLUG}_network.db: {db_size} bytes")
    print(f"  {SLUG}_network.gexf: {gexf_size} bytes")

    # Count person JSONs
    json_count = len(list(PERSONS_DIR.glob(f"{TODAY}-*.json")))
    print(f"  Person JSONs: {json_count}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()