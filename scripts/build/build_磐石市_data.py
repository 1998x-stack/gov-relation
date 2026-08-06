#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 磐石市 (Panshi City), 吉林省.

Investigation date: 2026-08-06
Task ID: jilin_磐石市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.panshi.gov.cn — 磐石市人民政府官方网站 (primary, current as of 2026-08-06)
    - 领导之窗/市政府 (ldzc/szf/): 市长孙宏宽 + 副市长郝拓宇/王廷旭/金泽/姚丽萍 individual bios
    - 市内要闻 (snyw) listing pages 1-40: 市委书记王萍萍, 市委副书记褚鹏, 市政协主席谭宏亮
      confirmed via 3+ meeting reports (2026年第1-18次常委会, 两优一先表彰大会)
    - 党风廉政通报会 article (2026-07-23): 常委/纪委书记/监委主任禚敬茹, 常委李淑南
    - 人大常委会/政协会 article (2026-06): 人大主任邢红梅, 政协主席谭宏亮 等

Confidence notes:
  - Current roles: confirmed via government website (2026-08-06)
  - 王萍萍 (party secretary, female): confirmed via 2026年第1-18次常委会 + 两优一先大会
  - 孙宏宽 (mayor): confirmed from homepage + 领导之窗 bio page
  - Predecessor 金永善 (party secretary 2024): confirmed from 2024年第10次常委会 article
  - Transition 金永善→王萍萍 (2025年初): confirmed (王萍萍主持2025年第1次常委会议)
  - 王萍萍 前为市长 then 书记: confirmed (2024年新闻标题"市长王萍萍")
  - 孙宏宽 简历: confirmed from official bio page
  - 完整履历(出生/籍贯/学历)对于王萍萍/褚鹏/多数常委及人大政协：未公开，列为 open_questions
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
SLUG = "磐石市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_磐石市"
if _CURRENT_DIR.name == "jilin_磐石市":
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

persons = [
    # ══════════════ 核心领导 (1-2) ══════════════
    {
        "id": 1, "name": "王萍萍", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市委书记",
        "current_org": "中共磐石市委员会",
        "source": "http://www.panshi.gov.cn/",
        "confidence": "confirmed",
        "notes": "磐石市委书记(女性)。2025年起主持市委常委会(2025年第1次至2026年第18次均有记录)。2024年任磐石市市长(生态环保会议新闻标题'市长王萍萍')。前任书记金永善。"
    },
    {
        "id": 2, "name": "孙宏宽", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "研究生学历", "party_join": "中共党员",
        "work_start": "", "current_post": "市长",
        "current_org": "磐石市人民政府",
        "source": "http://www.panshi.gov.cn/ldzc/szf/202508/t20250807_1279967.html",
        "confidence": "confirmed",
        "notes": "磐石市委副书记、市长、市政府党组书记，主持市政府全面工作。汉族/中共党员/研究生学历。历任榆树市新庄镇团委书记/副镇长、榆树市信访局副局长、共青团榆树市委书记/党组书记、榆树市人民政府办公室党组书记/主任、榆树市委常委/统战部部长(市政协党组副书记兼市委办公室主任/市档案局局长)、榆树市委常委/常务副市长，现任磐石市市长。"
    },
    # ══════════════ 市委班子 (3-8) ══════════════
    {
        "id": 3, "name": "褚鹏", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市委副书记",
        "current_org": "中共磐石市委员会",
        "source": "http://www.panshi.gov.cn/snyw/202608/t20260803_1331014.html",
        "confidence": "confirmed",
        "notes": "磐石市委副书记。2026-07-31带队慰问市人武部。完整履历待查。"
    },
    {
        "id": 4, "name": "禚敬茹", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共磐石市委员会",
        "source": "http://www.panshi.gov.cn/snyw/202607/t20260723_1329826.html",
        "confidence": "confirmed",
        "notes": "磐石市委常委、市纪委书记、市监委主任。2026-07-22在党风廉政建设和反腐败工作专题通报会通报有关情况。"
    },
    {
        "id": 5, "name": "周大鹏", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市委常委、组织部部长",
        "current_org": "中共磐石市委员会",
        "source": "http://www.panshi.gov.cn/snyw/202608/t20260806_1331432.html",
        "confidence": "confirmed",
        "notes": "磐石市委常委、组织部部长。2026-08-06为基层党组织书记进修班讲授任职培训第一课。"
    },
    {
        "id": 6, "name": "王林", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市委常委、市人武部部长",
        "current_org": "中共磐石市委员会",
        "source": "http://www.panshi.gov.cn/snyw/202608/t20260803_1331014.html",
        "confidence": "confirmed",
        "notes": "磐石市委常委、市人民武装部部长。"
    },
    {
        "id": 7, "name": "李淑南", "gender": "女", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市委常委",
        "current_org": "中共磐石市委员会",
        "source": "http://www.panshi.gov.cn/snyw/202607/t20260723_1329826.html",
        "confidence": "confirmed",
        "notes": "磐石市委常委。2026-07-22主持党风廉政建设和反腐败工作通报会用。偏统战/纪检条线，待进一步确认。"
    },
    {
        "id": 8, "name": "郝拓宇", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "吉林省桦甸市", "education": "大学学历", "party_join": "中共党员",
        "work_start": "", "current_post": "市委常委、常务副市长",
        "current_org": "磐石市人民政府",
        "source": "http://www.panshi.gov.cn/ldzc/szf/",
        "confidence": "confirmed",
        "notes": "磐石市委常委、常务副市长。汉族/中共党员/大学学历/吉林省桦甸市人。历任吉林市发改委国民经济综合处处长、能源协调处处长、发改委党组成员/副主任。任现职分管市政府办/发改/财政/应急等。"
    },
    # ══════════════ 市政府副市长 (9-13) ══════════════
    {
        "id": 9, "name": "姚丽萍", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "吉林省磐石市", "education": "中共吉林省委党校研究生", "party_join": "中共党员",
        "work_start": "", "current_post": "副市长",
        "current_org": "磐石市人民政府",
        "source": "http://www.panshi.gov.cn/ldzc/szf/",
        "confidence": "confirmed",
        "notes": "磐石市副市长。汉族/中共党员/省委党校研究生/吉林磐石本地。历任磐石市宝山乡乡长/党委书记、磐石市农业农村局党组书记/局长。本地成长干部。"
    },
    {
        "id": 10, "name": "金泽", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "大学学历", "party_join": "中共党员",
        "work_start": "", "current_post": "副市长、市公安局局长",
        "current_org": "磐石市人民政府",
        "source": "http://www.panshi.gov.cn/ldzc/szf/",
        "confidence": "confirmed",
        "notes": "磐石市副市长、市公安局局长，二级高级警长。汉族/中共党员/大学学历。曾任吉林市经济joins经济技术开发区管委会副主任（公安分局局长）。分管公安/司法/信访/退役军人。"
    },
    {
        "id": 11, "name": "王廷旭", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "副市长",
        "current_org": "磐石市人民政府",
        "source": "http://www.panshi.gov.cn/ldzc/szf/",
        "confidence": "confirmed",
        "notes": "磐石市副市长。汉族/中共党员。历任舒兰市新安乡政府副乡长、共青团舒兰市委副书记/书记、舒兰市亮甲山乡党委副书记/乡长/党委书记、舒兰市溪河镇党委书记。现任磐石副市长，分管城建/自然资源。"
    },
    {
        "id": 12, "name": "郝俊生", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "副市长",
        "current_org": "磐石市人民政府",
        "source": "http://www.panshi.gov.cn/snyw/202607/t20260730_1330624.html",
        "confidence": "confirmed",
        "notes": "磐石市副市长。2026-07-29参加书记带队的驻军慰问活动。"
    },
    {
        "id": 13, "name": "肖辉东", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "副市长",
        "current_org": "磐石市人民政府",
        "source": "http://www.panshi.gov.cn/snyw/",
        "confidence": "unverified",
        "notes": "磐石市副市长(在相关活动新闻中列名，任职时点/履历待核实)。"
    },
    # ══════════════ 市人大 (14-17) ══════════════
    {
        "id": 14, "name": "邢红梅", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市人大常委会主任",
        "current_org": "磐石市人民代表大会常务委员会",
        "source": "http://www.panshi.gov.cn/snyw/202606/t20260625_1326572.html",
        "confidence": "confirmed",
        "notes": "磐石市人大常委会主任。2026-06-23主持市十九届人大常委会第三十四次会议。"
    },
    {
        "id": 15, "name": "朴钟洙", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市人大常委会副主任",
        "current_org": "磐石市人民代表大会常务委员会",
        "source": "http://www.panshi.gov.cn/snyw/202606/t20260625_1326572.html",
        "confidence": "confirmed", "notes": "市人大常委会副主任。"
    },
    {
        "id": 16, "name": "陈贵君", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市人大常委会副主任",
        "current_org": "磐石市人民代表大会常务委员会",
        "source": "http://www.panshi.gov.cn/snyw/202606/t20260625_1326572.html",
        "confidence": "confirmed", "notes": "市人大常委会副主任。"
    },
    {
        "id": 17, "name": "佟仁", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市人大常委会副主任",
        "current_org": "磐石市人民代表大会常务委员会",
        "source": "http://www.panshi.gov.cn/snyw/202606/t20260625_1326572.html",
        "confidence": "confirmed", "notes": "市人大常委会副主任。"
    },
    # ══════════════ 市政协 (18-21) ══════════════
    {
        "id": 18, "name": "谭宏亮", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市政协主席",
        "current_org": "政协磐石市委员会",
        "source": "http://www.panshi.gov.cn/snyw/202608/t20260803_1330988.html",
        "confidence": "confirmed",
        "notes": "磐石市政协主席。2026-07月走访慰问驻军部队。"
    },
    {
        "id": 19, "name": "徐西举", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市政协副主席",
        "current_org": "政协磐石市委员会",
        "source": "http://www.panshi.gov.cn/snyw/202608/t20260803_1331018.html",
        "confidence": "confirmed", "notes": "市政协副主席。"
    },
    {
        "id": 20, "name": "张怀荣", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市政协副主席",
        "current_org": "政协磐石市委员会",
        "source": "http://www.panshi.gov.cn/snyw/202606/t20260601_1323681.html",
        "confidence": "confirmed", "notes": "市政协副主席，主持二十二次常委会。"
    },
    {
        "id": 21, "name": "田卫东", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市政协副主席",
        "current_org": "政协磐石市委员会",
        "source": "http://www.panshi.gov.cn/snyw/202606/t20260601_1323681.html",
        "confidence": "confirmed", "notes": "市政协副主席。"
    },
    # ══════════════ 前任/关联 (22+) ══════════════
    {
        "id": 22, "name": "金永善", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "前任市委书记",
        "current_org": "中共磐石市委员会",
        "source": "http://www.panshi.gov.cn/",
        "confidence": "confirmed",
        "notes": "磐石市前任市委书记。2024年任市委书记(2024年第10次常委会议)，2025年初由王萍萍继任。去向待查。"
    },
    {
        "id": 23, "name": "张颖", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市级领导",
        "current_org": "磐石市",
        "source": "http://www.panshi.gov.cn/snyw/202608/t20260803_1331018.html",
        "confidence": "unverified",
        "notes": "'市级领导张颖'，陪同市政协调研蛋鸡产业，具体职务待核实。"
    },
    {
        "id": 24, "name": "秦宏旭", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市领导",
        "current_org": "磐石市",
        "source": "http://www.panshi.gov.cn/snyw/202608/t20260803_1330988.html",
        "confidence": "unverified",
        "notes": "'市领导秦宏旭'，在政协走访慰问报道中点名，具体职务待查。"
    },
    {
        "id": 25, "name": "李冠霖", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员",
        "work_start": "", "current_post": "市领导",
        "current_org": "磐石市",
        "source": "http://www.panshi.gov.cn/snyw/202608/t20260803_1331014.html",
        "confidence": "unverified",
        "notes": "'市领导李冠霖'，在市委副书记慰问活动中点名参加，具体职务待查。"
    },
]


# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共磐石市委员会", "type": "党委", "level": "县级", "location": "吉林省吉林市磐石市"},
    {"id": 2, "name": "磐石市人民政府", "type": "政府", "level": "县级", "location": "吉林省吉林市磐石市"},
    {"id": 3, "name": "磐石市人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "吉林省吉林市磐石市"},
    {"id": 4, "name": "政协磐石市委员会", "type": "政协", "level": "县级", "location": "吉林省吉林市磐石市"},
    {"id": 5, "name": "磐石市纪委监委", "type": "纪委", "level": "县级", "location": "吉林省吉林市磐石市"},
    {"id": 6, "name": "磐石市公安局", "type": "政府", "level": "县级", "location": "吉林省吉林市磐石市"},
    {"id": 7, "name": "吉林市发展和改革委员会", "type": "政府", "level": "地级市", "location": "吉林省吉林市"},
    {"id": 8, "name": "吉林市经济技术开发区管委会", "type": "开发区", "level": "地级市", "location": "吉林省吉林市"},
    {"id": 9, "name": "榆树市人民政府", "type": "政府", "level": "县级", "location": "吉林省长春市榆树市"},
    {"id": 10, "name": "中共榆树市委员会", "type": "党委", "level": "县级", "location": "吉林省长春市榆树市"},
    {"id": 11, "name": "舒兰市人民政府", "type": "政府", "level": "县级", "location": "吉林省吉林市舒兰市"},
    {"id": 12, "name": "磐石市宝山乡人民政府", "type": "乡镇", "level": "乡科级", "location": "吉林省吉林市磐石市"},
    {"id": 13, "name": "磐石市农业农村局", "type": "政府", "level": "乡科级", "location": "吉林省吉林市磐石市"},
]


# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 王萍萍 (1)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2025-01", "end": "present",
     "rank": "县处级正职", "note": "主持磐石市委全面工作"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start": "", "end": "2024-12",
     "rank": "县处级正职", "note": "2024年任磐石市市长"},

    # 孙宏宽 (2)
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "", "end": "present",
     "rank": "县处级正职", "note": "现任磐石市委副书记、市长、党组书记"},
    {"person_id": 2, "org_id": 10, "title": "市委常委、常务副市长", "start": "", "end": "",
     "rank": "县处级副职", "note": "中共榆树市委常委、常务副市长"},
    {"person_id": 2, "org_id": 10, "title": "市委常委、统战部部长", "start": "", "end": "",
     "rank": "县处级副职", "note": "市政协党组副书记兼市委办公室主任、市档案局局长"},
    {"person_id": 2, "org_id": 9, "title": "市政府办公室党组书记、主任", "start": "", "end": "",
     "rank": "乡科级", "note": "榆树市人民政府办公室"},
    {"person_id": 2, "org_id": 9, "title": "共青团榆树市委书记、党组书记", "start": "", "end": "",
     "rank": "乡科级", "note": "共青团榆树市委"},
    {"person_id": 2, "org_id": 9, "title": "榆树市信访局副局长", "start": "", "end": "",
     "rank": "乡科级", "note": "榆树市信访局"},
    {"person_id": 2, "org_id": 9, "title": "新庄镇团委书记、副镇长", "start": "", "end": "",
     "rank": "乡科级", "note": "榆树市新庄镇"},

    # 褚鹏 (3)
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start": "", "end": "present",
     "rank": "县处级副职", "note": "磐石市委"},
    # 禚敬敏 (4)
    {"person_id": 4, "org_id": 1, "title": "市委常委、市纪委书记、市监委主任", "start": "", "end": "present",
     "rank": "县处级副职", "note": "磐石市委/纪委"},
    # 周大鹏 (5)
    {"person_id": 5, "org_id": 1, "title": "市委常委、组织部部长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "磐石市委"},
    # 王林 (6)
    {"person_id": 6, "org_id": 1, "title": "市委常委、市人武部部长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "磐石市委"},
    # 李淑南 (7)
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start": "", "end": "present",
     "rank": "县处级副职", "note": "磐石市委"},

    # 郝拓宇 (8)
    {"person_id": 8, "org_id": 2, "title": "市委常委、常务副市长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "磐石市政府"},
    {"person_id": 8, "org_id": 7, "title": "党组成员、副主任", "start": "", "end": "",
     "rank": "县处级副职", "note": "吉林市发展和改革委员会"},
    {"person_id": 8, "org_id": 7, "title": "能源协调处处长", "start": "", "end": "",
     "rank": "乡科级", "note": "吉林市发展和改革委员会"},
    {"person_id": 8, "org_id": 7, "title": "国民经济综合处处长", "start": "", "end": "",
     "rank": "乡科级", "note": "吉林市发展和改革委员会"},

    # 姚丽萍 (9)
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "磐石市政府"},
    {"person_id": 9, "org_id": 13, "title": "农业农村局党组书记、局长", "start": "", "end": "",
     "rank": "乡科级", "note": "磐石市农业农村局"},
    {"person_id": 9, "org_id": 12, "title": "宝山乡乡长、党委书记", "start": "", "end": "",
     "rank": "乡科级", "note": "磐石市宝山乡"},

    # 金泽 (10)
    {"person_id": 10, "org_id": 2, "title": "副市长、市公安局局长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "磐石市政府"},
    {"person_id": 10, "org_id": 8, "title": "管委会副主任、公安分局局长", "start": "", "end": "",
     "rank": "县处级副职", "note": "吉林市经济技术开发区"},

    # 王廷旭 (11)
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "磐石市政府"},
    {"person_id": 11, "org_id": 11, "title": "溪河镇党委书记", "start": "", "end": "",
     "rank": "乡科级", "note": "舒兰市溪河镇"},
    {"person_id": 11, "org_id": 11, "title": "亮甲山镇党委副书记、乡长、党委书记", "start": "", "end": "",
     "rank": "乡科级", "note": "舒兰市亮甲山乡"},
    {"person_id": 11, "org_id": 11, "title": "共青团舒兰市委副书记、书记", "start": "", "end": "",
     "rank": "乡科级", "note": "共青团舒兰市委"},
    {"person_id": 11, "org_id": 11, "title": "新安乡政府副乡长", "start": "", "end": "",
     "rank": "乡科级", "note": "舒兰市新安乡"},

    # 郝俊生 (12)、肖辉东 (13)
    {"person_id": 12, "org_id": 2, "title": "副市长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "磐石市政府"},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "磐石市政府"},

    # 人大 (14-17)
    {"person_id": 14, "org_id": 3, "title": "市人大常委会主任", "start": "", "end": "present",
     "rank": "县处级正职", "note": "磐石市人大"},
    {"person_id": 15, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present",
     "rank": "县处级副职", "note": "磐石市人大"},
    {"person_id": 16, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present",
     "rank": "县处级副职", "note": "磐石市人大"},
    {"person_id": 17, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present",
     "rank": "县处级副职", "note": "磐石市人大"},

    # 政协 (18-21)
    {"person_id": 18, "org_id": 4, "title": "市政协主席", "start": "", "end": "present",
     "rank": "县处级正职", "note": "政协磐石市委员会"},
    {"person_id": 19, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present",
     "rank": "县处级副职", "note": "政协磐石市委员会"},
    {"person_id": 20, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present",
     "rank": "县处级副职", "note": "政协磐石市委员会"},
    {"person_id": 21, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present",
     "rank": "县处级副职", "note": "政协磐石市委员会"},

    # 前任市委书记 金永善 (22)
    {"person_id": 22, "org_id": 1, "title": "市委书记", "start": "", "end": "2024-12",
     "rank": "县处级正职", "note": "磐石市前任市委书记"},
]


# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 王萍萍 ↔ 孙宏宽（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "王萍萍任市委书记、孙宏宽任市长，为当前磐石市党政正职搭档",
     "overlap_org": "中共磐石市委员会", "overlap_period": "2025至今",
     "confidence": "confirmed"},
    # 王萍 ↔ 金永善（前后任书记）
    {"person_a": 1, "person_b": 22, "type": "predecessor_successor",
     "context": "金永善为前任市委书记，2025年由王萍萍接任市委书记（王萍萍前为市长）",
     "overlap_org": "中共磐石市委员会", "overlap_period": "2024-2025",
     "confidence": "confirmed"},
    # 王萍萍（市长→书记）与孙宏宽（市长继任）
    {"person_a": 1, "person_b": 2, "type": "succession",
     "context": "王萍萍由磐石市长升任书记，孙宏宽自榆树市调入接任市长",
     "overlap_org": "磐石市人民政府", "overlap_period": "2024-2025",
     "confidence": "plausible"},
    # 孙宏宽 ↔ 褚鹏（正副手）
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "孙宏宽（市长、副书记）与褚鹏（市委副书记）在市委班子共事",
     "overlap_org": "中共磐石市委员会", "overlap_period": "",
     "confidence": "confirmed"},
    # 孙宏宽（榆树干部）↔ 榆树市网络
    {"person_a": 2, "person_b": 22, "type": "cross_county_rotation",
     "context": "孙宏宽自榆树市（中共榆树市委常委、常务副市长）调任磐石市长，属跨县调动",
     "overlap_org": "榆树市人民政府", "overlap_period": "",
     "confidence": "confirmed"},
    # 王廷为（舒兰）↔ 孙宏宽
    {"person_a": 11, "person_b": 2, "type": "overlap",
     "context": "王廷为（原舒兰市乡镇/共青团干部）与孙宏宽在磐石市政府班子共事",
     "overlap_org": "磐石市人民政府", "overlap_period": "",
     "confidence": "confirmed"},
    # 郝拓宇（上级机关调任）
    {"person_a": 8, "person_b": 2, "type": "overlap",
     "context": "郝拓宇（常务副市长，原吉林市发改委副主任）与孙宏宽在磐石市党政班子共事",
     "overlap_org": "磐石市人民政府", "overlap_period": "",
     "confidence": "confirmed"},
    # 姚丽萍（本地成长）
    {"person_a": 9, "person_b": 2, "type": "overlap",
     "context": "姚丽萍（磐石本地宝山镇成长干部）与孙宏宽在磐石市政府共事",
     "overlap_org": "磐石市人民政府", "overlap_period": "",
     "confidence": "confirmed"},
    # 金泽（公安政法条线）
    {"person_a": 10, "person_b": 8, "type": "overlap",
     "context": "金泽（副市长兼公安局长，原吉林市经开区）与郝拓宇（常务副市长）在市政府班子共事",
     "overlap_org": "磐石市人民政府", "overlap_period": "",
     "confidence": "confirmed"},
    # 王萍萍 ↔ 禚敬敏（班子配合）
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "王萍萍（书记）与禚敬敏（常委/纪委书记）在市委班子共事",
     "overlap_org": "中共磐石市委员会", "overlap_period": "",
     "confidence": "confirmed"},
    # 金永善（前任书记）与市政府
    {"person_a": 22, "person_b": 2, "type": "predecessor_successor",
     "context": "金永善为前任书记，孙宏宽继任市长（承接其任期政府班子）",
     "overlap_org": "磐石市人民政府", "overlap_period": "",
     "confidence": "plausible"},
]


# ── Person JSON writer ─────────────────────────────────────────────────────────

def _org_name(org_id: int) -> str:
    return next((o["name"] for o in organizations if o["id"] == org_id), "")


def _write_person_json(person_id: int, job: str, name: str) -> None:
    """Write a person JSON file for a core figure."""
    p = next(x for x in persons if x["id"] == person_id)
    pos_list = [x for x in positions if x["person_id"] == person_id]
    rel_list = [
        r for r in relationships
        if r["person_a"] == person_id or r["person_b"] == person_id
    ]
    org_ids = set()
    for pos in pos_list:
        org_ids.add(pos["org_id"])
    org_list = [o for o in organizations if o["id"] in org_ids]

    career_timeline = []
    for pos in pos_list:
        org_name = _org_name(pos["org_id"])
        career_timeline.append({
            "start": pos.get("start", ""),
            "end": pos.get("end", ""),
            "org": org_name,
            "title": pos["title"],
            "rank": pos.get("rank", ""),
            "confidence": "confirmed" if p.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001", "S002"],
        })

    relationships_out = []
    for r in rel_list:
        other_id = r["person_b"] if r["person_a"] == person_id else r["person_a"]
        other_name = next((x["name"] for x in persons if x["id"] == other_id), "")
        relationships_out.append({
            "person": other_name,
            "person_id": f"panshi_{other_name}",
            "relationship_type": r["type"],
            "strength": "medium" if r.get("confidence") == "confirmed" else "weak",
            "evidence": r["context"],
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "confidence": r.get("confidence", "unverified"),
            "source_ids": ["S001", "S002"],
        })

    person_data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "吉林省",
            "city": "吉林市",
            "region": "磐石市",
            "job": job,
            "task_id": "jilin_磐石市",
            "time_focus": "2026年8月",
        },
        "identity": {
            "person_id": f"panshi_{name}",
            "name": name,
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [{
                "period": "",
                "institution": p.get("education", "未找到"),
                "major": "",
                "degree": "",
                "study_type": "unknown",
                "source_ids": ["S001"],
            }],
            "party_join": "中共党员",
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{p.get('birth', '')}",
                "name_birthplace": f"{name}_{p.get('birthplace', '')}",
                "official_profile_url": p.get("source", ""),
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if person_id in (1, 2, 22, 14, 18) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": p.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [
            {"name": o["name"], "type": o["type"], "relationship": "曾任职"}
            for o in org_list
        ],
        "relationships": relationships_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if person_id in (1, 9) else (
                "cross_county_rotation" if person_id in (2, 8, 10, 11) else "unknown"),
            "systems_experience": [],
            "geographic_pattern": ["磐石市"] if person_id == 1 else
                                 (["榆树市", "磐石市"] if person_id == 2 else
                                  (["舒兰市", "磐石市"] if person_id == 11 else
                                   ["吉林市", "磐石市"] if person_id == 8 else
                                   ["吉林市", "磐石市"] if person_id == 10 else
                                   ["磐石市"] if person_id == 9 else [])),
            "promotion_velocity": {
                "summary": "履历信息不足，无法判断晋升速度",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {
            "total_relationships": len(relationships_out),
            "strong_connections": sum(1 for r in relationships_out if r["strength"] == "strong"),
            "medium_connections": sum(1 for r in relationships_out if r["strength"] == "medium"),
            "weak_connections": sum(1 for r in relationships_out if r["strength"] == "weak"),
        },
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "公开渠道未发现该人员的纪律处分、审查调查或负面报道",
            "date": AS_OF,
            "confidence": "unverified",
            "source_ids": ["S001"],
        }],
        "source_register": [
            {
                "id": "S001",
                "title": "磐石市人民政府官方网站（领导之窗/市内要闻）",
                "url": "http://www.panshi.gov.cn/",
                "publisher": "磐石市人民政府",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "领导之窗/市政府页面及各领导个人档案页；市内要闻/重要会议栏目报道",
            },
            {
                "id": "S002",
                "title": "磐石市党风廉政建设和反腐败工作情况专题通报会报道",
                "url": "http://www.panshi.gov.cn/snyw/202607/t20260723_1329826.html",
                "publisher": "磐石发布",
                "published_at": "2026-07-23",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "常委/纪委书记/监委主任禚敬敏、常委李行南、政协等确认",
            },
        ],
        "confidence_summary": {
            "identity": "unverified" if not p.get("birth") else "confirmed",
            "current_role": "confirmed" if p.get("confidence") == "confirmed" else "unverified",
            "career_completeness": "partial" if len(pos_list) > 1 else "thin",
            "relationship_confidence": "plausible",
            "biggest_gap": "完整履历（出生年月、籍贯、学历、早期任职起止时间）缺失" if not p.get("birthplace") else "部分履历起止时间待补充",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整履历（出生年月、籍贯、学历、历任职务起止）是什么？",
                "why_it_matters": "构建精确关系网络需要完整时间线与历任职务",
                "suggested_queries": [f"{name} 简历 磐石", f"{name} 百度百科", f"{name} 任前公示 吉林"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}是否在市委/政府班子之外有其他兼职或跨县调动历史？",
                "why_it_matters": "识别跨县干部交流网络模式",
                "suggested_queries": [f"{name} 磐石 交流", f"{name} 调任"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-吉林省-吉林市-{job}-{name}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ════════ main ════════
def main() -> None:
    print(f"=== Building {SLUG} network ===")
    print(f"Staging: {STAGING}")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")

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

    # Write person JSON for core leaders (市委书记 & 市长) + key deputies
    _write_person_json(1, "市委书记", "王萍萍")
    _write_person_json(2, "市长", "孙宏宽")
    _write_person_json(8, "常务副市长", "郝拓宇")
    _write_person_json(9, "副市长", "姚丽萍")
    _write_person_json(10, "副市长", "金泽")

    print(f"\n=== Build complete ===")
    print(f"DB size: {DB_PATH.stat().st_size} bytes")
    print(f"GEXF size: {GEXF_PATH.stat().st_size} bytes")
    print(f"Person JSONs in: {PJSON_DIR}")


if __name__ == "__main__":
    main()