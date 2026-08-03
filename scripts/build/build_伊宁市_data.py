#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 伊宁市 (Yining City) leadership network.

Data sources (all official from yining.gov.cn):
- 领导信息 page: https://www.yining.gov.cn/yining/ldxx/ldlist.shtml (accessed 2026-08-03)
- Individual leader profile pages with detailed bios

Confidence levels:
- confirmed = official government source
- plausible = cross-referenced news reports/indirect evidence
- unverified = insufficient corroboration

NOTE: 市委书记 (Party Secretary) name is currently unknown — web search tools degraded.
This is a high-priority gap documented in open_gaps.md.
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

_script_path = Path(__file__).resolve()
_repo_root = _script_path.parents[3]
sys.path.insert(0, str(_repo_root))

# ── METADATA ────────────────────────────────────────────────────────────────

SLUG = "伊宁市"
TODAY = "2026-08-03"

# ── PATHS ───────────────────────────────────────────────────────────────────

STAGING_DIR = _repo_root / "data/tmp/xinjiang_伊宁市"
DB_PATH = STAGING_DIR / "伊宁市_network.db"
GEXF_PATH = STAGING_DIR / "伊宁市_network.gexf"

# ═════════════════════════════════════════════════════════════════════════════
# PERSONS
# ═════════════════════════════════════════════════════════════════════════════

persons = [
    # ── Mayor ────────────────────────────────────────────────────────────
    {
        "id": 1,
        "name": "哈米提·阿克木",
        "gender": "男",
        "ethnicity": "维吾尔族",
        "birth": "1969年3月",
        "birthplace": "新疆伊宁县",
        "education": "区委党校研究生学历，工学学士（新疆工学院电气工程系工业电气自动化专业）",
        "party_join": "1997年6月",
        "work_start": "1992年11月",
        "current_post": "市委副书记、政府党组书记、市长",
        "current_org": "伊宁市人民政府",
        "source": "https://www.yining.gov.cn/yining/ldxx/202204/e15c9268ac274502ba52d0f64a20fe5c.shtml",
    },
    # ── 常务副市长 ────────────────────────────────────────────────────────
    {
        "id": 2,
        "name": "马华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "清华大学公共管理硕士（2022），南昌大学工学学士（2010）",
        "party_join": "中共党员",
        "work_start": "2010年11月",
        "current_post": "市委常委、统战部部长、常务副市长",
        "current_org": "伊宁市人民政府",
        "source": "https://www.yining.gov.cn/yining/ldxx/202204/3597907fedbc40ed9e201fa7dbbf828f.shtml",
    },
    # ── 副市长（援疆） ───────────────────────────────────────────────────
    {
        "id": 3,
        "name": "汤中原",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年8月",
        "birthplace": "江苏南京",
        "education": "南京师范大学汉语言文学专业",
        "party_join": "2001年3月",
        "work_start": "1998年8月",
        "current_post": "市委常委、副市长（援疆）",
        "current_org": "伊宁市人民政府",
        "source": "https://www.yining.gov.cn/yining/ldxx/202204/6bc5753edafc4605b1591ab69187d39d.shtml",
    },
    # ── 副市长 ───────────────────────────────────────────────────────────
    {
        "id": 4,
        "name": "夏地曼·乌鲁木齐拜",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "1984年7月",
        "birthplace": "新疆伊宁市",
        "education": "武汉理工大学管理学院市场营销专业，管理学学士（2008）",
        "party_join": "2013年6月",
        "work_start": "2009年1月",
        "current_post": "副市长",
        "current_org": "伊宁市人民政府",
        "source": "https://www.yining.gov.cn/yining/ldxx/202312/8b6f8ecb4c994b0ebf0886533f68fed3.shtml",
    },
    # ── 副市长 ───────────────────────────────────────────────────────────
    {
        "id": 5,
        "name": "地丽努尔·塔西",
        "gender": "女",
        "ethnicity": "维吾尔族",
        "birth": "1986年8月",
        "birthplace": "新疆巩留县",
        "education": "新疆大学科学技术学院市场营销专业（2009）",
        "party_join": "2010年9月",
        "work_start": "2009年8月",
        "current_post": "副市长",
        "current_org": "伊宁市人民政府",
        "source": "https://www.yining.gov.cn/yining/ldxx/202204/1eb3a93a92854821b153bf4a22ac14d3.shtml",
    },
    # ── 副市长、公安局长 ─────────────────────────────────────────────────
    {
        "id": 6,
        "name": "邢科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年11月",
        "birthplace": "甘肃定西",
        "education": "新疆师范大学地理科学与旅游管理专业本科（2007）",
        "party_join": "2012年6月",
        "work_start": "2009年6月",
        "current_post": "副市长、市公安局党委书记、局长、督察长",
        "current_org": "伊宁市人民政府",
        "source": "https://www.yining.gov.cn/yining/ldxx/202204/b48aa80dfbfe4150892f184cfee60fa2.shtml",
    },
    # ── 市委书记（待查） ──────────────────────────────────────────────────
    {
        "id": 7,
        "name": "待查（市委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共伊宁市委员会",
        "source": "",
    },
]

# ═════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ═════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共伊宁市委员会", "type": "党委", "level": "县级",
     "parent": "中共伊犁哈萨克自治州委员会", "location": "伊宁市"},
    {"id": 2, "name": "伊宁市人民政府", "type": "政府", "level": "县级",
     "parent": "伊犁哈萨克自治州人民政府", "location": "伊宁市"},
    {"id": 3, "name": "中共伊犁哈萨克自治州委员会", "type": "党委", "level": "地厅级",
     "parent": "中国共产党新疆维吾尔自治区委员会", "location": "伊宁市"},
    {"id": 4, "name": "伊犁哈萨克自治州人民政府", "type": "政府", "level": "地厅级",
     "parent": "新疆维吾尔自治区人民政府", "location": "伊宁市"},
    {"id": 5, "name": "伊宁市公安局", "type": "政法机关", "level": "县级",
     "parent": "伊宁市人民政府", "location": "伊宁市"},
    {"id": 6, "name": "中共伊宁县委员会", "type": "党委", "level": "县级",
     "parent": "中共伊犁哈萨克自治州委员会", "location": "伊宁县"},
    {"id": 7, "name": "伊宁县人大常委会", "type": "人大", "level": "县级",
     "parent": "伊宁县", "location": "伊宁县"},
    {"id": 8, "name": "巩留县委", "type": "党委", "level": "县级",
     "parent": "中共伊犁哈萨克自治州委员会", "location": "巩留县"},
    {"id": 9, "name": "尼勒克县委", "type": "党委", "level": "县级",
     "parent": "中共伊犁哈萨克自治州委员会", "location": "尼勒克县"},
    {"id": 10, "name": "霍城县委", "type": "党委", "level": "县级",
     "parent": "中共伊犁哈萨克自治州委员会", "location": "霍城县"},
]

# ═════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ═════════════════════════════════════════════════════════════════════════════

positions = [
    # ── 哈米提·阿克木 (person 1) ─────────────────────────────────────────
    {"person_id": 1, "org_id": 2, "title": "新疆工学院电气工程系工业电气自动化专业学习",
     "start_date": "1987.09", "end_date": "1992.07", "rank": "工学学士", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "毕业待分配",
     "start_date": "1992.07", "end_date": "1992.11", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "新疆第九汽车运输公司技术员",
     "start_date": "1992.11", "end_date": "1994.04", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "伊宁县第一中学教师",
     "start_date": "1994.04", "end_date": "1994.07", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "伊宁县委办秘书",
     "start_date": "1994.07", "end_date": "1998.04", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "伊宁县英塔木乡科技副乡长",
     "start_date": "1998.04", "end_date": "1998.11", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "伊宁县团委协助工作",
     "start_date": "1998.11", "end_date": "1999.04", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "伊宁县委文明办副主任",
     "start_date": "1999.04", "end_date": "2001.06", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "伊宁县团委副书记（主持工作）",
     "start_date": "2001.06", "end_date": "2003.03", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "伊宁县胡地亚于孜乡党委副书记",
     "start_date": "2003.03", "end_date": "2004.01", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "伊宁县英塔木乡党委委员、乡长候选人",
     "start_date": "2004.01", "end_date": "2004.05", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "伊宁县英塔木乡党委委员、乡长",
     "start_date": "2004.05", "end_date": "2007.07", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "伊宁县萨木于孜乡党委书记",
     "start_date": "2007.07", "end_date": "2010.10", "rank": "", "note": "期间读在职研究生"},
    {"person_id": 1, "org_id": 6, "title": "伊宁县萨木于孜乡党委书记（副县级待遇）",
     "start_date": "2010.10", "end_date": "2012.01", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "巩留县委常委",
     "start_date": "2012.01", "end_date": "2016.07", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "伊宁县人大常委会主任候选人、党组书记",
     "start_date": "2016.07", "end_date": "2016.09", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "伊宁县人大党组书记、主任",
     "start_date": "2016.09", "end_date": "2017.11", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 3, "title": "伊犁州党委组织部副部长",
     "start_date": "2017.11", "end_date": "2021.12", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "伊宁市委副书记、政府党组书记、市长",
     "start_date": "2021.12", "end_date": "至今", "rank": "", "note": ""},

    # ── 马华 (person 2) ──────────────────────────────────────────────────
    {"person_id": 2, "org_id": 2, "title": "南昌大学机电工程学院机械设计制造及其自动化专业学习",
     "start_date": "2006.09", "end_date": "2010.06", "rank": "本科", "note": "辅修工商管理2008-2009"},
    {"person_id": 2, "org_id": 2, "title": "北京金一文化发展有限公司渠道专员",
     "start_date": "2010.11", "end_date": "2011.07", "rank": "", "note": "企业工作"},
    {"person_id": 2, "org_id": 2, "title": "伊宁市萨依布依街道办事处党工委秘书",
     "start_date": "2011.08", "end_date": "2012.12", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "伊宁市塔什科瑞克乡党建办干部（借调市委办）",
     "start_date": "2012.12", "end_date": "2014.11", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "伊宁市委办公室秘书",
     "start_date": "2014.11", "end_date": "2017.06", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "伊宁市委办公室副主任",
     "start_date": "2017.06", "end_date": "2019.05", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "伊宁市英也尔镇党委副书记（主持工作）",
     "start_date": "2019.05", "end_date": "2019.07", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "伊宁市英也尔镇党委书记",
     "start_date": "2019.07", "end_date": "2021.07", "rank": "", "note": "期间获清华MPA"},
    {"person_id": 2, "org_id": 2, "title": "伊宁市投资促进中心筹备组负责人",
     "start_date": "2021.07", "end_date": "2022.02", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "伊宁市住建局党组书记、副局长",
     "start_date": "2022.02", "end_date": "2022.08", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "伊宁市托格拉克乡党委书记",
     "start_date": "2022.08", "end_date": "2023.05", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "伊宁市委常委、统战部部长、政协党组副书记",
     "start_date": "2023.05", "end_date": "2025.04", "rank": "", "note": "挂职南京建邺区2024.10-2025.01"},
    {"person_id": 2, "org_id": 2, "title": "伊宁市委常委、统战部部长、常务副市长人选",
     "start_date": "2025.04", "end_date": "至今", "rank": "", "note": ""},

    # ── 汤中原 (person 3) ────────────────────────────────────────────────
    {"person_id": 3, "org_id": 2, "title": "江苏省南京市六合区工作",
     "start_date": "2000.08", "end_date": "2023.03", "rank": "", "note": "23年南京地方工作经历"},
    {"person_id": 3, "org_id": 2, "title": "伊宁市委常委、副市长（援疆）",
     "start_date": "2023.04", "end_date": "至今", "rank": "", "note": "江苏援疆干部"},

    # ── 夏地曼·乌鲁木齐拜 (person 4) ────────────────────────────────────
    {"person_id": 4, "org_id": 2, "title": "武汉理工大学管理学院市场营销专业学习",
     "start_date": "2004.09", "end_date": "2008.06", "rank": "管理学学士", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "待业",
     "start_date": "2008.06", "end_date": "2009.01", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "伊犁州烟草专卖局（公司）霍城分局客户经理",
     "start_date": "2009.01", "end_date": "2011.01", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 9, "title": "尼勒克县纪委监察局执法监察室干部",
     "start_date": "2011.01", "end_date": "2013.02", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 9, "title": "尼勒克县胡吉尔台乡副乡长",
     "start_date": "2013.02", "end_date": "2017.09", "rank": "", "note": "挂职乌鲁木齐社区副主任2015-2016"},
    {"person_id": 4, "org_id": 9, "title": "尼勒克县乌赞镇党委副书记、纪委书记",
     "start_date": "2017.09", "end_date": "2020.09", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 9, "title": "尼勒克县加哈乌拉斯台乡党委副书记、乡长",
     "start_date": "2020.09", "end_date": "2023.09", "rank": "一级主任科员", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "伊宁市人民政府党组成员、副市长",
     "start_date": "2023.09", "end_date": "至今", "rank": "", "note": ""},

    # ── 地丽努尔·塔西 (person 5) ─────────────────────────────────────────
    {"person_id": 5, "org_id": 2, "title": "新疆大学科学技术学院市场营销专业学习",
     "start_date": "2005.09", "end_date": "2009.07", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "待业",
     "start_date": "2009.07", "end_date": "2009.08", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "共青团伊宁市委员会大学生西部计划志愿者",
     "start_date": "2009.08", "end_date": "2010.10", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "伊宁市潘津乡人民政府纪检干事/出纳/专职副书记",
     "start_date": "2010.10", "end_date": "2016.03", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "伊宁市巴彦岱镇副镇长/党委委员/纪委书记",
     "start_date": "2016.03", "end_date": "2020.10", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "伊宁市宁远路街道筹备/达达木图镇镇长",
     "start_date": "2020.10", "end_date": "2024.10", "rank": "一级主任科员", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "伊宁市人民政府副市长",
     "start_date": "2024.10", "end_date": "至今", "rank": "", "note": ""},

    # ── 邢科 (person 6) ──────────────────────────────────────────────────
    {"person_id": 6, "org_id": 2, "title": "新疆师范大学旅游管理专业学习",
     "start_date": "2003.09", "end_date": "2007.07", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "伊宁市待业",
     "start_date": "2007.07", "end_date": "2009.06", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "伊宁县公安局派出所民警/所长/国保大队教导员",
     "start_date": "2009.06", "end_date": "2023.09", "rank": "", "note": "逐步晋升至一级警长"},
    {"person_id": 6, "org_id": 10, "title": "霍城县公安局党委书记、局长",
     "start_date": "2023.09", "end_date": "2025.12", "rank": "四级高级警长", "note": "霍城县委政法委副书记"},
    {"person_id": 6, "org_id": 5, "title": "伊宁市政府党组成员、副市长、公安局党委书记、局长",
     "start_date": "2025.12", "end_date": "至今", "rank": "四级高级警长", "note": "2026年1月正式任命"},

    # ── 市委书记 placeholder ──────────────────────────────────────────────
    {"person_id": 7, "org_id": 1, "title": "市委书记",
     "start_date": "", "end_date": "", "rank": "", "note": "待查 — 公开资料未找到姓名和履历"},
]

# ═════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ═════════════════════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "市长与常务副市长，伊宁市政府班子",
     "overlap_org": "伊宁市人民政府", "overlap_period": "2025.04至今"},
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "市长与援疆副市长",
     "overlap_org": "伊宁市人民政府", "overlap_period": "2023.04至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "市长与副市长",
     "overlap_org": "伊宁市人民政府", "overlap_period": "2023.09至今"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "市长与副市长",
     "overlap_org": "伊宁市人民政府", "overlap_period": "2024.10至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "市长与副市长兼公安局局长",
     "overlap_org": "伊宁市人民政府", "overlap_period": "2026.01至今"},
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "常务副市长与副市长，政府班子",
     "overlap_org": "伊宁市人民政府", "overlap_period": "2025.04至今"},
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "副市长，政府班子",
     "overlap_org": "伊宁市人民政府", "overlap_period": "2024.10至今"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "同届市委常委",
     "overlap_org": "中共伊宁市委员会", "overlap_period": "2025.04至今"},
    {"person_a": 2, "person_b": 5, "type": "predecessor_successor",
     "context": "马华曾任托格拉克乡党委书记（2022-2023）；地丽努尔曾任达达木图镇镇长（2021-2024）",
     "overlap_org": "伊宁市乡镇系统", "overlap_period": "2020-2023"},
    {"person_a": 6, "person_b": 5, "type": "overlap",
     "context": "副市长，政府班子",
     "overlap_org": "伊宁市人民政府", "overlap_period": "2026.01至今"},
]

# ═════════════════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县级市")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 伊宁市人民政府网站 (yining.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
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
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    conn.commit()

    # ── Insert persons ──
    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace",
              "education", "party_join", "work_start", "current_post",
              "current_org", "source"]
    for p in persons:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(
            f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?'] * len(cols_p))})",
            vals,
        )

    # ── Insert organizations ──
    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(
            f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?'] * len(cols_o))})",
            vals,
        )

    # ── Insert positions ──
    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date",
                "rank", "note"]
    for pos in positions:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(
            f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?'] * len(cols_pos))})",
            vals,
        )

    # ── Insert relationships ──
    cols_r = ["person_a", "person_b", "type", "context", "overlap_org",
              "overlap_period"]
    for r in relationships:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(
            f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?'] * len(cols_r))})",
            vals,
        )

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──
    print("\n--- 构建 GEXF 图文件 ---")

    def esc(s):
        if s is None:
            return ""
        return (str(s).replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))

    def person_color(post):
        if "市委书记" in post and "副书记" not in post:
            return ("255,50,50", 20.0)
        elif "市长" in post and "副" not in post:
            return ("50,100,255", 20.0)
        elif "常务" in post or "副市长" in post:
            return ("50,100,255", 15.0)
        elif "常委" in post:
            return ("100,100,255", 15.0)
        else:
            return ("100,100,100", 12.0)

    def org_color_vals(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "政法机关": ("200,200,200"),
            "人大": ("200,255,255"),
        }.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        c_vals = c.split(",")
        lines.append(f'        <viz:color r="{c_vals[0]}" g="{c_vals[1]}" b="{c_vals[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color_vals(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    for pos in positions:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{pos["person_id"]}" '
            f'target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">'
        )
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{r["person_a"]}" '
            f'target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">'
        )
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(str(GEXF_PATH), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    run_build()