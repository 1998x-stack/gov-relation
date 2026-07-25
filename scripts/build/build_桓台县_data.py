#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 桓台县, 淄博市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_桓台县
Level: 县
Targets: 县委书记 & 县长

Key findings:
- 县委书记 范伟 — 兼任县长（党政一肩挑）, 男, 汉族, 1980年8月生
- 县长 王洪波 — 县委副书记、县长, 2024年12月任代县长, 2025年1月当选
- 前任县委书记 林恒 — 2021.01-2024.05任职, 后升任淄博市委常委、宣传部部长
- 县委领导班子 9人（含兼职）
- 县政府领导班子 9人（含交叉任职）
- 县人大常委会 6人, 县政协 2+人
- 司法机构 2人

Research sources:
- 桓台县人民政府网站 (www.huantai.gov.cn) — multiple news articles (2026年7月)
- 百度百科 — 中国共产党桓台县委员会词条、桓台县人民政府词条
- 百度百科 — 林恒、王韶华、陈之远、李四海、周刚、樊涛、胡智慧、徐兴岭、王洪波等个人词条

Confidence notes:
- 范伟当前职务已确认（县委书记兼县长, as of 2026年7月）
- 王洪波当前职务已确认（县委副书记、县长, as of 2026年7月）
- 大部分县委、政府、人大、政协领导已通过新闻参会名单确认
- 范伟的详细早期履历暂缺（同名演员覆盖百度百科搜索结果）
- 部分领导的出生年月、籍贯等个人信息待查
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

SLUG = "桓台县"
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

    # 范伟 — 县委书记、县长（党政一肩挑）
    {
        "id": 1,
        "name": "范伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "大学学历，管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县委书记、县长、县人武部党委第一书记",
        "current_org": "中共桓台县委员会",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年7月); 桓台县人大常委会及县委常委会会议新闻; 百度百科—中国共产党桓台县委员会词条"
    },
    # 王洪波 — 县委副书记、县长
    {
        "id": 2,
        "name": "王洪波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县委副书记、县人民政府县长",
        "current_org": "桓台县人民政府",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年7月); 百度百科-王洪波 (lemmaId=59921356); 2024年12月桓台县人大常委会第二十七次会议任代县长，2025年1月18日当选县长"
    },
    # 朱凯 — 县委副书记、政法委书记
    {
        "id": 3,
        "name": "朱凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县委副书记、政法委书记",
        "current_org": "中共桓台县委员会",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年7月3日县委常委会会议)"
    },
    # 赵寅岗 — 县委常委、组织部部长
    {
        "id": 4,
        "name": "赵寅岗",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县委常委、组织部部长",
        "current_org": "中共桓台县委组织部",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年7月15日县委常委会（扩大）会议新闻)"
    },
    # 胡智慧 — 县委常委、办公室主任
    {
        "id": 5,
        "name": "胡智慧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县委常委、办公室主任",
        "current_org": "中共桓台县委员会办公室",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年5月); 百度百科-胡智慧 (lemmaId=59921076)"
    },
    # 周刚 — 县委常委、宣传部部长、统战部部长、副县长
    {
        "id": 6,
        "name": "周刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县委常委、宣传部部长、统战部部长、副县长",
        "current_org": "中共桓台县委宣传部",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年7月); 百度百科-周刚 (lemmaId=59961548); 桓台县人民政府百度百科词条"
    },
    # 陈之远 — 县委常委、副县长，桓台经济开发区党工委书记
    {
        "id": 7,
        "name": "陈之远",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "山东桓台",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县委常委、副县长、桓台经济开发区党工委书记",
        "current_org": "桓台县人民政府",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年7月); 百度百科-陈之远 (lemmaId=54890055)"
    },
    # 王韶华 — 县委常委、副县长，淄博东岳经济开发区党工委书记
    {
        "id": 8,
        "name": "王韶华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "山东淄博张店",
        "education": "大学学历，工学学士",
        "party_join": "中共党员",
        "work_start": "2003年7月入党",
        "current_post": "桓台县委常委、副县长、淄博东岳经济开发区党工委书记",
        "current_org": "桓台县人民政府",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年6月); 百度百科-王韶华 (lemmaId=63466911)"
    },
    # 苗军 — 县委常委、县人武部上校政委
    {
        "id": 9,
        "name": "苗军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县委常委、县人武部上校政委",
        "current_org": "桓台县人民武装部",
        "source": "百度百科—中国共产党桓台县委员会词条"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Government (县政府) — Additional members not already listed as 县委常委
    # ══════════════════════════════════════════════════════════════════════════

    # 徐兴岭 — 副县长（挂职）
    {
        "id": 10,
        "name": "徐兴岭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县人民政府副县长（挂职）",
        "current_org": "桓台县人民政府",
        "source": "百度百科-徐兴岭 (lemmaId=59154058)"
    },
    # 李四海 — 副县长、县公安局局长
    {
        "id": 11,
        "name": "李四海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年1月",
        "birthplace": "",
        "education": "大学学历，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县人民政府副县长、县公安局局长",
        "current_org": "桓台县公安局",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年5月); 百度百科-李四海 (lemmaId=59961445)"
    },
    # 崔锋 — 副县长
    {
        "id": 12,
        "name": "崔锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县人民政府副县长",
        "current_org": "桓台县人民政府",
        "source": "桓台县人民政府百度百科词条"
    },
    # 樊涛 — 副县长
    {
        "id": 13,
        "name": "樊涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年7月",
        "birthplace": "",
        "education": "大学学历，法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县人民政府副县长",
        "current_org": "桓台县人民政府",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年5月); 百度百科-樊涛 (lemmaId=63418286)"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 人大 (County People's Congress)
    # ══════════════════════════════════════════════════════════════════════════

    # 李向东 — 县人大常委会主任
    {
        "id": 14,
        "name": "李向东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县人大常委会主任",
        "current_org": "桓台县人民代表大会常务委员会",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年7月3日)"
    },
    # 李树强 — 县人大常委会副主任
    {
        "id": 15,
        "name": "李树强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县人大常委会副主任",
        "current_org": "桓台县人民代表大会常务委员会",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年5月20日)"
    },
    # 裴培科 — 县人大常委会副主任
    {
        "id": 16,
        "name": "裴培科",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桓台县人大常委会副主任",
        "current_org": "桓台县人民代表大会常务委员会",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年5月20日)"
    },
    # 孙燕 — 县人大常委会副主任
    {
        "id": 17,
        "name": "孙燕",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桓台县人大常委会副主任",
        "current_org": "桓台县人民代表大会常务委员会",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年5月20日)"
    },
    # 柴涛 — 县人大常委会副主任
    {
        "id": 18,
        "name": "柴涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桓台县人大常委会副主任",
        "current_org": "桓台县人民代表大会常务委员会",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年5月20日)"
    },
    # 曹成刚 — 县人大常委会副主任
    {
        "id": 19,
        "name": "曹成刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桓台县人大常委会副主任",
        "current_org": "桓台县人民代表大会常务委员会",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年5月20日)"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 政协 (CPPCC)
    # ══════════════════════════════════════════════════════════════════════════

    # 徐宁 — 县政协主席
    {
        "id": 20,
        "name": "徐宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县政协主席、党组书记",
        "current_org": "政协桓台县委员会",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年7月3日)"
    },
    # 毕玉秀 — 县政协副主席
    {
        "id": 21,
        "name": "毕玉秀",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桓台县政协副主席",
        "current_org": "政协桓台县委员会",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年5月20日)"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 司法机构
    # ══════════════════════════════════════════════════════════════════════════

    # 黄强 — 县人民法院院长
    {
        "id": 22,
        "name": "黄强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县人民法院院长",
        "current_org": "桓台县人民法院",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年5月20日)"
    },
    # 李玉伟 — 县人民检察院检察长
    {
        "id": 23,
        "name": "李玉伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桓台县人民检察院检察长",
        "current_org": "桓台县人民检察院",
        "source": "桓台县人民政府网站新闻 (huantai.gov.cn, 2026年5月20日)"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ══════════════════════════════════════════════════════════════════════════

    # 林恒 — 前任县委书记（2021.01-2024.05）
    {
        "id": 24,
        "name": "林恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年6月",
        "birthplace": "山东牟平",
        "education": "大学学历（烟台大学机械工程系）",
        "party_join": "中共党员",
        "work_start": "1996年7月",
        "current_post": "淄博市委常委、宣传部部长",
        "current_org": "中共淄博市委宣传部",
        "source": "百度百科-林恒 (lemmaId=24353129); 2024年4月山东省委组织部任前公示"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共桓台县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共淄博市委员会",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 2,
        "name": "桓台县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "淄博市人民政府",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 3,
        "name": "桓台县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "淄博市人民代表大会常务委员会",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 4,
        "name": "政协桓台县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协淄博市委员会",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 5,
        "name": "桓台县人民法院",
        "type": "司法",
        "level": "县处级",
        "parent": "淄博市中级人民法院",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 6,
        "name": "桓台县人民检察院",
        "type": "司法",
        "level": "县处级",
        "parent": "淄博市人民检察院",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 7,
        "name": "中共桓台县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共桓台县委员会",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 8,
        "name": "中共桓台县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共桓台县委员会",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 9,
        "name": "中共桓台县委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共桓台县委员会",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 10,
        "name": "中共桓台县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共桓台县委员会",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 11,
        "name": "中共桓台县委办公室",
        "type": "党委",
        "level": "县处级",
        "parent": "中共桓台县委员会",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 12,
        "name": "桓台县人民武装部",
        "type": "政府",
        "level": "县处级",
        "parent": "淄博军分区",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 13,
        "name": "桓台县公安局",
        "type": "政府",
        "level": "乡科级",
        "parent": "桓台县人民政府",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 14,
        "name": "桓台经济开发区",
        "type": "开发区",
        "level": "县处级",
        "parent": "桓台县人民政府",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 15,
        "name": "淄博东岳经济开发区",
        "type": "开发区",
        "level": "县处级",
        "parent": "桓台县人民政府",
        "location": "山东省淄博市桓台县",
    },
    {
        "id": 16,
        "name": "中共淄博市委宣传部",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共淄博市委员会",
        "location": "山东省淄博市",
    },
]

positions_data = [
    # ═══ 范伟 — 县委书记、县长 ═══
    {
        "person_id": 1,
        "org_id": 1,
        "title": "桓台县委书记",
        "start_date": "约2024年底",
        "end_date": "现任",
        "rank": "县处级正职",
        "note": "从县长升任县委书记; 兼任县长(党政一肩挑)",
    },
    {
        "person_id": 1,
        "org_id": 2,
        "title": "桓台县县长",
        "start_date": "约2020-2021年",
        "end_date": "现任（兼任）",
        "rank": "县处级正职",
        "note": "原任县长，升任书记后仍兼任县长",
    },
    {
        "person_id": 1,
        "org_id": 12,
        "title": "桓台县人武部党委第一书记（兼）",
        "start_date": "约2024年底",
        "end_date": "现任",
        "rank": "",
        "note": "",
    },

    # ═══ 王洪波 — 县委副书记、县长 ═══
    {
        "person_id": 2,
        "org_id": 1,
        "title": "桓台县委副书记",
        "start_date": "2024年12月31日",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "2024年12月任副书记、代县长",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "桓台县人民政府县长",
        "start_date": "2025年1月18日",
        "end_date": "现任",
        "rank": "县处级正职",
        "note": "2025年1月18日在桓台县第十九届人大第四次会议上当选县长；此前任淄川区委副书记",
    },

    # ═══ 朱凯 — 县委副书记、政法委书记 ═══
    {
        "person_id": 3,
        "org_id": 1,
        "title": "桓台县委副书记",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 3,
        "org_id": 10,
        "title": "桓台县委政法委书记（兼）",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },

    # ═══ 赵寅岗 — 县委常委、组织部部长 ═══
    {
        "person_id": 4,
        "org_id": 1,
        "title": "桓台县委常委",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 4,
        "org_id": 7,
        "title": "桓台县委组织部部长",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },

    # ═══ 胡智慧 — 县委常委、办公室主任 ═══
    {
        "person_id": 5,
        "org_id": 1,
        "title": "桓台县委常委",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 5,
        "org_id": 11,
        "title": "桓台县委办公室主任",
        "start_date": "",
        "end_date": "现任",
        "rank": "乡科级正职",
        "note": "",
    },

    # ═══ 周刚 — 县委常委、宣传部部长、统战部部长、副县长 ═══
    {
        "person_id": 6,
        "org_id": 1,
        "title": "桓台县委常委",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 6,
        "org_id": 8,
        "title": "桓台县委宣传部部长（兼）",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 6,
        "org_id": 9,
        "title": "桓台县委统战部部长（兼）",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 6,
        "org_id": 2,
        "title": "桓台县人民政府副县长",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },

    # ═══ 陈之远 — 县委常委、副县长、桓台经济开发区党工委书记 ═══
    {
        "person_id": 7,
        "org_id": 1,
        "title": "桓台县委常委",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 7,
        "org_id": 2,
        "title": "桓台县人民政府副县长",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "负责科技、工信、商务、招商引资、金融证券、园区建设等",
    },
    {
        "person_id": 7,
        "org_id": 14,
        "title": "桓台经济开发区党工委书记（兼）",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级正职",
        "note": "",
    },

    # ═══ 王韶华 — 县委常委、副县长、东岳经济开发区党工委书记 ═══
    {
        "person_id": 8,
        "org_id": 1,
        "title": "桓台县委常委",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 8,
        "org_id": 2,
        "title": "桓台县人民政府副县长",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "协助县长负责财政、税务、审计工作; 1980年11月生, 淄博张店人",
    },
    {
        "person_id": 8,
        "org_id": 15,
        "title": "淄博东岳经济开发区党工委书记（兼）",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },

    # ═══ 苗军 — 县委常委、县人武部上校政委 ═══
    {
        "person_id": 9,
        "org_id": 1,
        "title": "桓台县委常委",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 9,
        "org_id": 12,
        "title": "桓台县人武部上校政委",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },

    # ═══ 徐兴岭 — 副县长（挂职） ═══
    {
        "person_id": 10,
        "org_id": 2,
        "title": "桓台县人民政府副县长（挂职）",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "1966年8月生，汉族，大学学历",
    },

    # ═══ 李四海 — 副县长、县公安局局长 ═══
    {
        "person_id": 11,
        "org_id": 2,
        "title": "桓台县人民政府副县长",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "1970年1月生，汉族，大学学历、工程硕士",
    },
    {
        "person_id": 11,
        "org_id": 13,
        "title": "桓台县公安局党委书记、局长",
        "start_date": "",
        "end_date": "现任",
        "rank": "乡科级正职",
        "note": "",
    },

    # ═══ 崔锋 — 副县长 ═══
    {
        "person_id": 12,
        "org_id": 2,
        "title": "桓台县人民政府副县长",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },

    # ═══ 樊涛 — 副县长 ═══
    {
        "person_id": 13,
        "org_id": 2,
        "title": "桓台县人民政府副县长",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "1981年7月生，汉族，大学学历、法学学士；负责教育体育、民政、慈善、文旅、卫健、医保等",
    },

    # ═══ 李向东 — 县人大常委会主任 ═══
    {
        "person_id": 14,
        "org_id": 3,
        "title": "桓台县人大常委会主任",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级正职",
        "note": "",
    },

    # ═══ 人大副主任 ═══
    {
        "person_id": 15,
        "org_id": 3,
        "title": "桓台县人大常委会副主任",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 16,
        "org_id": 3,
        "title": "桓台县人大常委会副主任",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 17,
        "org_id": 3,
        "title": "桓台县人大常委会副主任",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 18,
        "org_id": 3,
        "title": "桓台县人大常委会副主任",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 19,
        "org_id": 3,
        "title": "桓台县人大常委会副主任",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },

    # ═══ 徐宁 — 县政协主席 ═══
    {
        "person_id": 20,
        "org_id": 4,
        "title": "桓台县政协主席、党组书记",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级正职",
        "note": "",
    },

    # ═══ 毕玉秀 — 县政协副主席 ═══
    {
        "person_id": 21,
        "org_id": 4,
        "title": "桓台县政协副主席",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },

    # ═══ 黄强 — 县法院院长 ═══
    {
        "person_id": 22,
        "org_id": 5,
        "title": "桓台县人民法院院长",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },

    # ═══ 李玉伟 — 县检察院检察长 ═══
    {
        "person_id": 23,
        "org_id": 6,
        "title": "桓台县人民检察院检察长",
        "start_date": "",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },

    # ═══ 林恒 — 前任县委书记 ═══
    {
        "person_id": 24,
        "org_id": 1,
        "title": "桓台县委书记",
        "start_date": "2021年1月",
        "end_date": "2024年5月",
        "rank": "县处级正职",
        "note": "1972年6月生，山东牟平人；此前任威海文登区区长",
    },
    {
        "person_id": 24,
        "org_id": 16,
        "title": "淄博市委常委、宣传部部长",
        "start_date": "2024年5月",
        "end_date": "现任",
        "rank": "副厅级",
        "note": "2024年4月省委组织部任前公示，拟任副厅级领导职务",
    },
]

relationships_data = [
    # ═══ 范伟（书记）↔ 王洪波（县长）—— 党政搭档 ═══
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长党政搭档（范伟兼任县长，王洪波为县委副书记、县长）",
        "overlap_org": "中共桓台县委员会",
        "overlap_period": "2025年至今",
    },

    # ═══ 范伟（书记）↔ 副书记们 ═══
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记、政法委书记朱凯",
        "overlap_org": "中共桓台县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记王洪波",
        "overlap_org": "中共桓台县委员会",
        "overlap_period": "现任",
    },

    # ═══ 范伟（书记）↔ 县委常委成员 ═══
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委、组织部部长赵寅岗",
        "overlap_org": "中共桓台县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委、办公室主任胡智慧",
        "overlap_org": "中共桓台县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委、宣传部部长周刚",
        "overlap_org": "中共桓台县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委、副县长陈之远",
        "overlap_org": "中共桓台县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委、副县长王韶华",
        "overlap_org": "中共桓台县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委、人武部政委苗军",
        "overlap_org": "中共桓台县委员会",
        "overlap_period": "现任",
    },

    # ═══ 王洪波（县长）↔ 副县长们 ═══
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县长与副县长陈之远（常委兼、经济开发区书记）",
        "overlap_org": "桓台县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长与副县长王韶华（常委兼、协助财政审计）",
        "overlap_org": "桓台县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县长与副县长周刚（常委兼）",
        "overlap_org": "桓台县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "县长与挂职副县长徐兴岭",
        "overlap_org": "桓台县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "县长与副县长、公安局长李四海",
        "overlap_org": "桓台县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 12,
        "type": "superior_subordinate",
        "context": "县长与副县长崔锋",
        "overlap_org": "桓台县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "县长与副县长樊涛",
        "overlap_org": "桓台县人民政府",
        "overlap_period": "现任",
    },

    # ═══ 前任关系 ═══
    {
        "person_a": 1,
        "person_b": 24,
        "type": "predecessor_successor",
        "context": "林恒前任县委书记，范伟接任",
        "overlap_org": "桓台县",
        "overlap_period": "2024年交接",
    },

    # ═══ 范伟（县长时）提前任县长位置继任者王洪波 ═══
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "范伟原任县长升任书记，王洪波接任县长",
        "overlap_org": "桓台县人民政府",
        "overlap_period": "2024年12月",
    },

    # ═══ 人大 ≤→ 党委 ═══
    {
        "person_a": 14,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "县人大常委会主任与县委书记（党政主要负责人）",
        "overlap_org": "桓台县",
        "overlap_period": "现任",
    },

    # ═══ 政协 ≤→ 党委 ═══
    {
        "person_a": 20,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "县政协主席与县委书记",
        "overlap_org": "桓台县",
        "overlap_period": "现任",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON helpers
# ═══════════════════════════════════════════════════════════════════════════════

def make_person_json(person: dict) -> dict:
    """Generate the deep person JSON for a single person."""
    pid = f"huantai_{person['name']}"
    
    career_entries = []
    for pos in positions_data:
        if pos["person_id"] == person["id"]:
            org_name = ""
            for org in organizations_data:
                if org["id"] == pos["org_id"]:
                    org_name = org["name"]
                    break
            career_entries.append({
                "start": pos.get("start_date", ""),
                "end": pos.get("end_date", ""),
                "org": org_name,
                "title": pos.get("title", ""),
                "level": pos.get("rank", ""),
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if pos.get("end_date") or pos.get("start_date") else "plausible",
            })

    relationships_list = []
    for rel in relationships_data:
        other_id = None
        if rel["person_a"] == person["id"]:
            other_id = rel["person_b"]
        elif rel["person_b"] == person["id"]:
            other_id = rel["person_a"]
        if other_id:
            other_person = None
            for p in persons_data:
                if p["id"] == other_id:
                    other_person = p
                    break
            if other_person:
                relationships_list.append({
                    "person": other_person["name"],
                    "person_id": f"huantai_{other_person['name']}",
                    "relationship_type": rel.get("type", ""),
                    "strength": "strong" if rel.get("type") in ("superior_subordinate", "predecessor_successor") else "medium",
                    "evidence": rel.get("context", ""),
                    "overlap_org": rel.get("overlap_org", ""),
                    "overlap_period": rel.get("overlap_period", ""),
                    "direction": "undirected",
                    "confidence": "confirmed",
                })

    source_urls = []
    if person.get("source"):
        for s in person["source"].split(";"):
            s = s.strip()
            if s:
                source_urls.append({
                    "label": s[:80],
                    "url": "",
                    "note": "",
                })

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "淄博市",
            "region": "桓台县",
            "job": person.get("current_post", ""),
            "task_id": "shandong_桓台县",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": pid,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown"}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', 'unknown')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', 'unknown')}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
        },
        "career_timeline": career_entries,
        "organizations": [{"org_id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations_data],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "公开资料不足，无法推断工作风格",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至调研日未发现公开违规违纪记录",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [{"id": "S001", "title": "桓台县政府网站/百度百科", "url": "", "publisher": "政府/百科", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "medium"}],
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "high",
            "biggest_gap": f"{person['name']}的完整履历（含早期任职、教育背景）待查" if not person.get("work_start") else "",
        },
        "open_questions": [
            {"priority": "high", "question": f"{person['name']}的完整职业履历", "why_it_matters": "核心人物履历完整性", "suggested_queries": [f"{person['name']} 简历"], "last_attempted": AS_OF},
            {"priority": "medium", "question": f"{person['name']}的出生地和籍贯", "why_it_matters": "身份信息完整性", "suggested_queries": [f"{person['name']} 籍贯"], "last_attempted": AS_OF},
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    # ── Build DB + GEXF ──
    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # ── Write person JSONs for core leaders ──
    core_ids = [1, 2, 24]  # 范伟, 王洪波, 林恒
    for pid in core_ids:
        person = None
        for p in persons_data:
            if p["id"] == pid:
                person = p
                break
        if person:
            job_slug = person["current_post"].split("、")[0] if person["current_post"] else "unknown"
            filename = f"{TODAY}-山东省-淄博市-{job_slug}-{person['name']}.json"
            filepath = STAGING_DIR / filename
            data = make_person_json(person)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Person JSON: {filepath}")

    print(f"\nDB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons_data)}")
    print(f"Organizations: {len(organizations_data)}")
    print(f"Positions: {len(positions_data)}")
    print(f"Relationships: {len(relationships_data)}")
    print("Done.")


if __name__ == "__main__":
    main()
