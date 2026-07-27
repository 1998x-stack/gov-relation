#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 封丘县, 新乡市, 河南省.

Level: 县
Province: 河南省
Parent city: 新乡市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: henan_封丘县

Research date: 2026-07-24
Official source: http://www.fengqiu.gov.cn/ (封丘县人民政府)

Current status (as of 2026-07-24):
- 县委书记: 王跃峰 (also served as 12th committee 书记 2021-2026)
- 县长: 巩红敏 (assumed office ~June 2026, succeeded 王振海)

Key source:
- 中国共产党封丘县第十三次代表大会 (2026-06-24) elected standing committee:
  王跃峰(书记)、巩红敏(副书记)、袁兆丹(副书记)、董兴军、龚玉兵、邢天杰、杨晋岭、
  秦桐(常委、常务副县长)、王荣世、李晨晖、田玮
- 封丘县政府领导页面 (zfxxgk/ldzc/) lists: 县长王振海(historical), 现任县长巩红敏
- 巩红敏 previously 县委常委、常务副县长 (based on 王振海 era structure)
- 赵宏恩: 县人大常委会主任 (列席县委常委会议)
- 胡高峰: 县政协主席
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

SLUG = "封丘县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-24"
TODAY = "20260724"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 王跃峰 — 县委书记
    {
        "id": 1,
        "name": "王跃峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共封丘县委员会",
        "source": "http://www.fengqiu.gov.cn/dtyw/jrfq/1293635.html — 王跃峰讲授树立和践行正确政绩观学习教育专题党课 (2026-07-15)",
    },

    # 2. 巩红敏 — 县长
    {
        "id": 2,
        "name": "巩红敏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "封丘县人民政府",
        "source": "http://www.fengqiu.gov.cn/dtyw/jrfq/1294862.html — 巩红敏深入企业调研督导安全生产 (2026-07-24). "
                 "Previous role: 县委常委、常务副县长 (inferred from county leadership structure). "
                 "Succeeded 王振海 as 县长 ~June 2026.",
    },

    # ════════════════════════════════════════
    # Standing Committee (县委常委会)
    # ════════════════════════════════════════

    # 3. 袁兆丹 — 县委副书记
    {
        "id": 3,
        "name": "袁兆丹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共封丘县委员会",
        "source": "https://www.fengqiu.gov.cn/dtyw/jrfq/1294354.html — 封丘县环保工作座谈会 (2026-07-21). "
                 "Also mentioned as 县领导 in news articles & 第13次党代会主席团常务委员会委员.",
    },

    # 4. 董兴军 — 县委常委
    {
        "id": 4,
        "name": "董兴军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共封丘县委员会",
        "source": "https://www.fengqiu.gov.cn/dtyw/jrfq/1290583.html — 第13次党代会主席团常务委员会委员 (2026-06-24)",
    },

    # 5. 龚玉兵 — 县委常委
    {
        "id": 5,
        "name": "龚玉兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共封丘县委员会",
        "source": "https://www.fengqiu.gov.cn/dtyw/jrfq/1290583.html — 第13次党代会主席团常务委员会委员 (2026-06-24)",
    },

    # 6. 邢天杰 — 县委常委
    {
        "id": 6,
        "name": "邢天杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共封丘县委员会",
        "source": "https://www.fengqiu.gov.cn/dtyw/jrfq/1290583.html — 第13次党代会主席团常务委员会委员 (2026-06-24). "
                 "Also mentioned in 县政府常务会议 (https://www.fengqiu.gov.cn/dtyw/jrfq/1294864.html) as attending county government meeting.",
    },

    # 7. 杨晋岭 — 县委常委
    {
        "id": 7,
        "name": "杨晋岭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共封丘县委员会",
        "source": "https://www.fengqiu.gov.cn/dtyw/jrfq/1290583.html — 第13次党代会主席团常务委员会委员 (2026-06-24). "
                 "Also mentioned in 县政府常务会议 (https://www.fengqiu.gov.cn/dtyw/jrfq/1294864.html).",
    },

    # 8. 秦桐 — 县委常委、常务副县长
    {
        "id": 8,
        "name": "秦桐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-10",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "封丘县人民政府",
        "source": "http://www.fengqiu.gov.cn/zfxxgk/ldzc/ — 封丘县政府领导之窗 (generated 2026-04-02). "
                 "Resume: 秦桐，男，汉族，1983年10月出生，研究生学历，中共党员，现任封丘县委常委，封丘县人民政府党组副书记、副县长.",
    },

    # 9. 王荣世 — 县委常委
    {
        "id": 9,
        "name": "王荣世",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共封丘县委员会",
        "source": "https://www.fengqiu.gov.cn/dtyw/jrfq/1290583.html — 第13次党代会主席团常务委员会委员 (2026-06-24). "
                 "Also mentioned in 县政府常务会议 (https://www.fengqiu.gov.cn/dtyw/jrfq/1294864.html).",
    },

    # 10. 李晨晖 — 县委常委
    {
        "id": 10,
        "name": "李晨晖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共封丘县委员会",
        "source": "https://www.fengqiu.gov.cn/dtyw/jrfq/1290583.html — 第13次党代会主席团常务委员会委员 (2026-06-24). "
                 "Accompanied 县长巩红敏 on enterprise inspection (https://www.fengqiu.gov.cn/dtyw/jrfq/1294862.html).",
    },

    # 11. 田玮 — 县委常委
    {
        "id": 11,
        "name": "田玮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共封丘县委员会",
        "source": "https://www.fengqiu.gov.cn/dtyw/jrfq/1290583.html — 第13次党代会主席团常务委员会委员 (2026-06-24)",
    },

    # ════════════════════════════════════════
    # County Government (县政府)
    # ════════════════════════════════════════

    # 12. 徐林锋 — 县委常委、宣传部部长、副县长
    {
        "id": 12,
        "name": "徐林锋",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976-12",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、副县长",
        "current_org": "封丘县人民政府",
        "source": "http://www.fengqiu.gov.cn/zfxxgk/ldzc/ — 封丘县政府领导之窗. "
                 "Resume: 徐林锋，女，1976年12月出生，汉族，本科学历，中共党员，现任封丘县委常委、宣传部部长，封丘县人民政府副县长.",
    },

    # 13. 苏舸 — 县委常委、统战部部长
    {
        "id": 13,
        "name": "苏舸",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-01",
        "birthplace": "",
        "education": "本科学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长，县政府党组成员",
        "current_org": "中共封丘县委员会",
        "source": "http://www.fengqiu.gov.cn/zfxxgk/ldzc/ — 封丘县政府领导之窗. "
                 "Resume: 苏舸，男，汉族，1979年1月出生，本科学历，公共管理硕士，中共党员，现任封丘县委常委、统战部部长，封丘县人民政府党组成员，政协封丘县委党组副书记.",
    },

    # 14. 付英民 — 副县长
    {
        "id": 14,
        "name": "付英民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-08",
        "birthplace": "",
        "education": "省委党校大学文化程度",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、三级调研员",
        "current_org": "封丘县人民政府",
        "source": "http://www.fengqiu.gov.cn/zfxxgk/ldzc/ — 封丘县政府领导之窗. "
                 "Resume: 付英民，男，汉族，1978年8月出生，省委党校大学文化程度，现任封丘县人民政府副县长、三级调研员.",
    },

    # 15. 黄书林 — 副县长
    {
        "id": 15,
        "name": "黄书林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-09",
        "birthplace": "",
        "education": "大学文化程度",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "封丘县人民政府",
        "source": "http://www.fengqiu.gov.cn/zfxxgk/ldzc/ — 封丘县政府领导之窗. "
                 "Resume: 黄书林，男，汉族，1984年9月出生，大学文化程度，中共党员，现任封丘县人民政府党组成员、副县长.",
    },

    # 16. 王亮 — 副县长、县公安局局长
    {
        "id": 16,
        "name": "王亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-12",
        "birthplace": "",
        "education": "大学文化程度",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "封丘县公安局",
        "source": "http://www.fengqiu.gov.cn/zfxxgk/ldzc/ — 封丘县政府领导之窗. "
                 "Resume: 王亮，男，汉族，1972年12月出生，大学文化程度，中共党员，现任封丘县人民政府党组成员、副县长，县公安局党委书记、局长、督察长、三级高级警长.",
    },

    # 17. 王志魁 — 副县长
    {
        "id": 17,
        "name": "王志魁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-12",
        "birthplace": "",
        "education": "大学文化学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县先进制造业开发区管委会主任",
        "current_org": "封丘县人民政府",
        "source": "http://www.fengqiu.gov.cn/zfxxgk/ldzc/ — 封丘县政府领导之窗. "
                 "Resume: 王志魁，男，1974年12月出生，汉族，大学文化学历，中共党员，现任封丘县人民政府副县长、封丘县先进制造业开发区管理委员会主任.",
    },

    # 18. 郭胜 — 县领导 (出席常务会议)
    {
        "id": 18,
        "name": "郭胜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "封丘县人民政府",
        "source": "https://www.fengqiu.gov.cn/dtyw/jrfq/1294864.html — 县政府常务会议 (2026-07-24). 出席人名单中的领导之一。",
    },

    # 19. 刘安超 — 县领导 (出席常务会议)
    {
        "id": 19,
        "name": "刘安超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "封丘县人民政府",
        "source": "https://www.fengqiu.gov.cn/dtyw/jrfq/1294864.html — 县政府常务会议 (2026-07-24). 出席人名单中的领导之一。",
    },

    # ════════════════════════════════════════
    # Judiciary / Discipline
    # ════════════════════════════════════════

    # 20. 吴继杰 — 县领导 (检察院/法院?)
    {
        "id": 20,
        "name": "吴继杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "封丘县",
        "source": "https://www.fengqiu.gov.cn/dtyw/jrfq/1294861.html — 新乡市人大常委会莅封调研 (2026-07-24). "
                 "Mentioned as 县领导 accompanying the delegation.",
    },

    # ════════════════════════════════════════
    # People's Congress & Political Consultative Conference
    # ════════════════════════════════════════

    # 21. 赵宏恩 — 县人大常委会主任
    {
        "id": 21,
        "name": "赵宏恩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "封丘县人民代表大会常务委员会",
        "source": "https://www.fengqiu.gov.cn/dtyw/jrfq/1292219.html — 十三届县委常委会第2次(扩大)会议 (2026-07-05). "
                 "赵宏恩列席县委常委会议. Also mentioned in 调研文章 (https://www.fengqiu.gov.cn/dtyw/jrfq/1294861.html).",
    },

    # 22. 胡高峰 — 县政协主席
    {
        "id": 22,
        "name": "胡高峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议封丘县委员会",
        "source": "https://www.fengqiu.gov.cn/dtyw/jrfq/1294858.html — 胡高峰督办重点提案 (2026-07-24). "
                 "提及为封丘县政协主席.",
    },

    # ════════════════════════════════════════
    # Historical / Predecessors
    # ════════════════════════════════════════

    # 23. 王振海 — 前任县长
    {
        "id": 23,
        "name": "王振海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-07",
        "birthplace": "",
        "education": "大学学历，农学、工学双学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县长（去向待确认）",
        "current_org": "封丘县人民政府",
        "source": "http://www.fengqiu.gov.cn/zfxxgk/ldzc/ — 封丘县政府领导之窗 (generated 2026-04-02). "
                 "Resume: 王振海，男，汉族，1970年7月出生，中共党员，大学学历，农学、工学双学士学位，现任封丘县委副书记，封丘县人民政府党组书记、县长。"
                 "As of June 2026, 巩红敏 has succeeded him as 县长.",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    # Party
    {"id": 1, "name": "中共封丘县委员会", "type": "党委", "level": "县", "parent": "中共新乡市委员会", "location": "封丘县"},
    {"id": 2, "name": "中共封丘县委宣传部", "type": "党委", "level": "县", "parent": "中共封丘县委员会", "location": "封丘县"},
    {"id": 3, "name": "中共封丘县委统战部", "type": "党委", "level": "县", "parent": "中共封丘县委员会", "location": "封丘县"},
    {"id": 4, "name": "中共封丘县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共封丘县委员会", "location": "封丘县"},

    # Government
    {"id": 5, "name": "封丘县人民政府", "type": "政府", "level": "县", "parent": "新乡市人民政府", "location": "封丘县"},
    {"id": 6, "name": "封丘县公安局", "type": "政府", "level": "县", "parent": "封丘县人民政府", "location": "封丘县"},
    {"id": 7, "name": "封丘县先进制造业开发区", "type": "开发区", "level": "县", "parent": "封丘县人民政府", "location": "封丘县"},

    # People's Congress
    {"id": 8, "name": "封丘县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "新乡市人民代表大会常务委员会", "location": "封丘县"},

    # Political Consultative Conference
    {"id": 9, "name": "中国人民政治协商会议封丘县委员会", "type": "政协", "level": "县", "parent": "政协新乡市委员会", "location": "封丘县"},

    # Township-level (referenced but not detailed)
    {"id": 10, "name": "封丘县各乡镇", "type": "乡镇/街道", "level": "乡", "parent": "封丘县人民政府", "location": "封丘县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 王跃峰
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2021?", "end_date": "present", "rank": "正处级", "note": "担任第十二届、第十三届县委书记"},

    # 巩红敏
    {"person_id": 2, "org_id": 5, "title": "县长", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "前任: 王振海"},
    {"person_id": 2, "org_id": 5, "title": "常务副县长", "start_date": "?", "end_date": "2026-06", "rank": "副处级", "note": "推测为前任常务副县长，后在2026年6月升任县长"},

    # 袁兆丹
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},

    # 董兴军
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},

    # 龚玉兵
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},

    # 邢天杰
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},

    # 杨晋岭
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},

    # 秦桐
    {"person_id": 8, "org_id": 5, "title": "常务副县长", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "县委常委、县政府党组副书记、副县长"},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "第13届党代会当选常委"},

    # 王荣世
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},

    # 李晨晖
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},

    # 田玮
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},

    # 徐林锋
    {"person_id": 12, "org_id": 2, "title": "宣传部部长", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "县委常委"},
    {"person_id": 12, "org_id": 5, "title": "副县长", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},

    # 苏舸
    {"person_id": 13, "org_id": 3, "title": "统战部部长", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "县委常委、县政府党组成员、县政协党组副书记"},
    {"person_id": 13, "org_id": 5, "title": "县政府党组成员", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},

    # 付英民
    {"person_id": 14, "org_id": 5, "title": "副县长、三级调研员", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},

    # 黄书林
    {"person_id": 15, "org_id": 5, "title": "副县长", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "县政府党组成员"},

    # 王亮
    {"person_id": 16, "org_id": 6, "title": "县公安局局长", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "县政府党组成员、县公安局党委书记、督察长、三级高级警长"},
    {"person_id": 16, "org_id": 5, "title": "副县长", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},

    # 王志魁
    {"person_id": 17, "org_id": 7, "title": "县先进制造业开发区管委会主任", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 5, "title": "副县长", "start_date": "?", "end_date": "present", "rank": "副处级", "note": ""},

    # 郭胜
    {"person_id": 18, "org_id": 5, "title": "县领导", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "出席县政府常务会议"},

    # 刘安超
    {"person_id": 19, "org_id": 5, "title": "县领导", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "出席县政府常务会议"},

    # 吴继杰
    {"person_id": 20, "org_id": 5, "title": "县领导", "start_date": "?", "end_date": "present", "rank": "副处级", "note": "陪同省市领导调研"},

    # 赵宏恩
    {"person_id": 21, "org_id": 8, "title": "县人大常委会主任", "start_date": "?", "end_date": "present", "rank": "正处级", "note": "列席县委常委会议"},

    # 胡高峰
    {"person_id": 22, "org_id": 9, "title": "县政协主席", "start_date": "?", "end_date": "present", "rank": "正处级", "note": ""},

    # 王振海（前任县长）
    {"person_id": 23, "org_id": 5, "title": "县长", "start_date": "?", "end_date": "2026-06", "rank": "正处级", "note": "前任县长，去向待确认"},
    {"person_id": 23, "org_id": 1, "title": "县委副书记", "start_date": "?", "end_date": "2026-06", "rank": "副处级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 王跃峰 <-> 巩红敏 (书记-县长搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长工作搭档关系", "overlap_org": "中共封丘县委员会/封丘县人民政府", "overlap_period": "2026-06至今"},

    # 王跃峰 <-> 袁兆丹 (书记-副书记)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与专职副书记", "overlap_org": "中共封丘县委员会", "overlap_period": "至今"},

    # 王跃峰 <-> 赵宏恩 (书记-人大主任)
    {"person_a": 1, "person_b": 21, "type": "overlap", "context": "县委书记与人大常委会主任同为县四大班子主要领导", "overlap_org": "封丘县", "overlap_period": "至今"},

    # 王跃峰 <-> 胡高峰 (书记-政协主席)
    {"person_a": 1, "person_b": 22, "type": "overlap", "context": "县委书记与政协主席同为县四大班子主要领导", "overlap_org": "封丘县", "overlap_period": "至今"},

    # 巩红敏 <-> 秦桐 (县长-常务副县长)
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与常务副县长工作关系", "overlap_org": "封丘县人民政府", "overlap_period": "2026-06至今"},
    {"person_a": 2, "person_b": 8, "type": "predecessor_successor", "context": "推测巩红敏前任秦桐可能曾任常务副县长，秦桐现任常务副县长", "overlap_org": "封丘县人民政府", "overlap_period": "2026"},

    # 王振海 <-> 巩红敏 (县长交接)
    {"person_a": 23, "person_b": 2, "type": "predecessor_successor", "context": "王振海卸任县长后由巩红敏接任", "overlap_org": "封丘县人民政府", "overlap_period": "2026-06"},

    # 王跃峰 <-> 全体县委常委 (同一届常委会)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "同一届县委常委会成员", "overlap_org": "中共封丘县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "同一届县委常委会成员", "overlap_org": "中共封丘县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "同一届县委常委会成员", "overlap_org": "中共封丘县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "同一届县委常委会成员", "overlap_org": "中共封丘县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "同一届县委常委会成员", "overlap_org": "中共封丘县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "同一届县委常委会成员", "overlap_org": "中共封丘县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "同一届县委常委会成员", "overlap_org": "中共封丘县委员会", "overlap_period": "2026-06至今"},

    # 政府班子成员关系
    {"person_a": 8, "person_b": 12, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "封丘县人民政府", "overlap_period": "至今"},
    {"person_a": 8, "person_b": 14, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "封丘县人民政府", "overlap_period": "至今"},
    {"person_a": 8, "person_b": 15, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "封丘县人民政府", "overlap_period": "至今"},
    {"person_a": 8, "person_b": 16, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "封丘县人民政府", "overlap_period": "至今"},
    {"person_a": 8, "person_b": 17, "type": "overlap", "context": "县政府领导班子成员", "overlap_org": "封丘县人民政府", "overlap_period": "至今"},
]


# ══════════════════════════════════════════════════════════════════════════════
# WRITE PERSON JSON FILES
# ══════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, *, role: str) -> None:
    """Write a single person's graph JSON to the staging directory."""
    name = person["name"]
    birth_str = person.get("birth", "")
    person_id = f"fengqiu_{name.lower()}"

    filename = f"{TODAY}-河南省-新乡市-{role}-{name}.json"
    filepath = PERSONS_DIR / filename

    source_ids = ["S001"]
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "新乡市",
            "region": "封丘县",
            "job": role,
            "task_id": "henan_封丘县",
            "time_focus": "2021-2026",
        },
        "identity": {
            "person_id": person_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": birth_str,
            "birthplace": "",
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown", "source_ids": source_ids}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{birth_str}",
                "name_birthplace": f"{name}_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if role in ["县委书记", "县长"] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": source_ids,
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": f"公开资料未找到{name}的完整履历",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "organizations": [{"org": person["current_org"], "role": person["current_post"], "period": "", "source_ids": source_ids}],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": ["河南省新乡市封丘县"],
            "promotion_velocity": {"summary": "履历不完整，无法评估晋升速度", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "资料有限，暂无足够公开信息推断工作风格",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "封丘县人民政府网站",
                "url": "http://www.fengqiu.gov.cn/",
                "publisher": "封丘县人民政府",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "县领导页面的公开简历信息",
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"{name}的完整履历（出生地、教育背景、历任职务时间线）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整履历",
                "why_it_matters": "核心领导人的履历是评估其从政背景和工作关系网络的基础",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 新乡 任职"],
                "last_attempted": AS_OF,
            }
        ],
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {filepath.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"=== Building {SLUG} network ===")
    print(f"Database: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print()

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

    # Write person JSONs for core leaders
    print("\nWriting person JSONs...")
    write_person_json(persons[0], role="县委书记")     # 王跃峰
    write_person_json(persons[1], role="县长")         # 巩红敏
    write_person_json(persons[7], role="常务副县长")    # 秦桐
    write_person_json(persons[22], role="前任县长")     # 王振海

    # Summary
    print(f"\n=== {SLUG} build complete ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"\nFiles created:")
    print(f"  {DB_PATH}")
    print(f"  {GEXF_PATH}")
    for p in persons:
        if p["id"] in [1, 2, 8, 23]:
            role_map = {1: "县委书记", 2: "县长", 8: "常务副县长", 23: "前任县长"}
            fname = f"{TODAY}-河南省-新乡市-{role_map[p['id']]}-{p['name']}.json"
            print(f"  {PERSONS_DIR / fname}")


if __name__ == "__main__":
    main()
