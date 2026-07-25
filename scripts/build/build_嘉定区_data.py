#!/usr/bin/env python3
"""嘉定区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区(直辖市)
调查日期: 2026-07-25
信息来源:
  - 上海市嘉定区人民政府网站 (www.jiading.gov.cn)
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Find project root: walk up looking for gov_relation/
PROJECT_ROOT = HERE
for _ in range(10):
    if (PROJECT_ROOT / "gov_relation").is_dir():
        break
    PROJECT_ROOT = PROJECT_ROOT.parent
else:
    PROJECT_ROOT = HERE.parents[2]  # fallback

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "嘉定区"
TODAY = "2026-07-25"

STAGING = HERE
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# Canonical destinations (always relative to project root)
CANONICAL_DB = PROJECT_ROOT / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = PROJECT_ROOT / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = PROJECT_ROOT / "scripts" / "build" / f"build_{SLUG}_data.py"
CANONICAL_ROOT_BUILD = PROJECT_ROOT / f"build_{SLUG}_data.py"

# ── Persons ──────────────────────────────────────────────────────────────────
# ID ranges: 1xxx = party committee, 2xxx = government, 3xxx = congress,
#            4xxx = cppcc, 5xxx = judiciary

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 区委领导班子
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 肖文高 — 区委书记
    {
        "id": 1001,
        "name": "肖文高",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1975年7月",
        "birthplace": "",
        "education": "大学，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区委书记",
        "current_org": "中共上海市嘉定区委员会",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_37",
    },
    # 2. 高香 — 区委副书记、区长
    {
        "id": 1002,
        "name": "高香",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969年12月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区委副书记、区长",
        "current_org": "上海市嘉定区人民政府",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_18",
    },
    # 3. 吴杰 — 区委副书记
    {
        "id": 1003,
        "name": "吴杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年5月",
        "birthplace": "",
        "education": "大学，工学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区委副书记、区一级巡视员",
        "current_org": "中共上海市嘉定区委员会",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_908245",
    },
    # 4. 冯捷 — 区委常委、区纪委书记
    {
        "id": 1004,
        "name": "冯捷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年6月",
        "birthplace": "",
        "education": "大学，经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区委常委、区纪委书记、区监委主任、区一级巡视员",
        "current_org": "中共上海市嘉定区纪律检查委员会",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_733116",
    },
    # 5. 姚卫华 — 区委常委、组织部部长
    {
        "id": 1005,
        "name": "姚卫华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年8月",
        "birthplace": "",
        "education": "中央党校研究生，经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区委常委、组织部部长、区委党校校长、区行政学院院长、区一级巡视员",
        "current_org": "中共上海市嘉定区委员会组织部",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_339394",
    },
    # 6. 朱效洁 — 区委常委、副区长
    {
        "id": 1006,
        "name": "朱效洁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年4月",
        "birthplace": "",
        "education": "在职研究生，工学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区委常委、副区长、区政府党组成员",
        "current_org": "上海市嘉定区人民政府",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_720364",
    },
    # 7. 罗博 — 区委常委、宣传部部长
    {
        "id": 1007,
        "name": "罗博",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "嘉定区委常委、宣传部部长",
        "current_org": "中共上海市嘉定区委员会宣传部",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_971071",
    },
    # 8. 唐晓林 — 区委常委、统战部部长
    {
        "id": 1008,
        "name": "唐晓林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年5月",
        "birthplace": "",
        "education": "在职研究生，理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区委常委、统战部部长",
        "current_org": "中共上海市嘉定区委员会统战部",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_45",
    },
    # 9. 卞唯敏 — 区委常委、政法委书记
    {
        "id": 1009,
        "name": "卞唯敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年2月",
        "birthplace": "",
        "education": "市委党校研究生，文学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区委常委、政法委书记",
        "current_org": "中共上海市嘉定区委员会政法委员会",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_339399",
    },
    # 10. 彭春林 — 区委常委、人武部政委
    {
        "id": 1010,
        "name": "彭春林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "嘉定区委常委、人武部政委",
        "current_org": "上海市嘉定区人民武装部",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_838920",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 区政府领导 (除兼任常委的)
    # ═══════════════════════════════════════════════════════════════════════
    # 11. 姚少杰 — 副区长
    {
        "id": 2001,
        "name": "姚少杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年9月",
        "birthplace": "",
        "education": "大学，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区副区长、区政府党组成员，公安嘉定分局局长",
        "current_org": "上海市嘉定区人民政府",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_963632",
    },
    # 12. 季倩倩 — 副区长
    {
        "id": 2002,
        "name": "季倩倩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年7月",
        "birthplace": "",
        "education": "研究生，工学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区副区长、区政府党组成员",
        "current_org": "上海市嘉定区人民政府",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_845489",
    },
    # 13. 丁炯炯 — 副区长
    {
        "id": 2003,
        "name": "丁炯炯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年7月",
        "birthplace": "",
        "education": "大学，法律硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区副区长、区政府党组成员",
        "current_org": "上海市嘉定区人民政府",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_852554",
    },
    # 14. 汤东英 — 副区长
    {
        "id": 2004,
        "name": "汤东英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "",
        "education": "大学，工学学士",
        "party_join": "九三学社",
        "work_start": "",
        "current_post": "嘉定区副区长",
        "current_org": "上海市嘉定区人民政府",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_841678",
    },
    # 15. 刘嘉峰 — 副区长
    {
        "id": 2005,
        "name": "刘嘉峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年7月",
        "birthplace": "",
        "education": "大学，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区副区长、区政府党组成员",
        "current_org": "上海市嘉定区人民政府",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_950810",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 区人大常委会
    # ═══════════════════════════════════════════════════════════════════════
    # 16. 连正华 — 主任
    {
        "id": 3001,
        "name": "连正华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年4月",
        "birthplace": "",
        "education": "中央党校研究生，高级管理人员工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区人大常委会主任、党组书记",
        "current_org": "嘉定区人民代表大会常务委员会",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_52",
    },
    # 17. 王建新 — 副主任
    {
        "id": 3002,
        "name": "王建新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年7月",
        "birthplace": "",
        "education": "市委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区人大常委会副主任、党组成员，区总工会主席",
        "current_org": "嘉定区人民代表大会常务委员会",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_339416",
    },
    # 18. 刘骏 — 副主任
    {
        "id": 3003,
        "name": "刘骏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年5月",
        "birthplace": "",
        "education": "在职研究生，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区人大常委会副主任、党组成员",
        "current_org": "嘉定区人民代表大会常务委员会",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_144481",
    },
    # 19. 陆强 — 副主任
    {
        "id": 3004,
        "name": "陆强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年12月",
        "birthplace": "",
        "education": "大学，经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区人大常委会副主任、党组成员",
        "current_org": "嘉定区人民代表大会常务委员会",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_43",
    },
    # 20. 张伟东 — 副主任
    {
        "id": 3005,
        "name": "张伟东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年10月",
        "birthplace": "",
        "education": "市委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区人大常委会副主任、党组成员",
        "current_org": "嘉定区人民代表大会常务委员会",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_870117",
    },
    # 21. 陈小鸿 — 副主任
    {
        "id": 3006,
        "name": "陈小鸿",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1961年8月",
        "birthplace": "",
        "education": "在职研究生，工学博士",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "嘉定区人大常委会副主任（不驻会），同济大学教授",
        "current_org": "嘉定区人民代表大会常务委员会",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_355080",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 区政协
    # ═══════════════════════════════════════════════════════════════════════
    # 22. 杨莉 — 主席
    {
        "id": 4001,
        "name": "杨莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1965年11月",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区政协主席、党组书记",
        "current_org": "中国人民政治协商会议上海市嘉定区委员会",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_49",
    },
    # 23. 乐跃明 — 副主席
    {
        "id": 4002,
        "name": "乐跃明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年2月",
        "birthplace": "",
        "education": "大学，文学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区政协副主席、党组成员",
        "current_org": "中国人民政治协商会议上海市嘉定区委员会",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_144477",
    },
    # 24. 徐锋 — 副主席
    {
        "id": 4003,
        "name": "徐锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年3月",
        "birthplace": "",
        "education": "大学，管理学硕士",
        "party_join": "农工党",
        "work_start": "",
        "current_post": "嘉定区政协副主席（不驻会），农工党嘉定区主委",
        "current_org": "中国人民政治协商会议上海市嘉定区委员会",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_7",
    },
    # 25. 周芳珍 — 副主席
    {
        "id": 4004,
        "name": "周芳珍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "",
        "education": "研究生，工学硕士",
        "party_join": "民盟",
        "work_start": "",
        "current_post": "嘉定区政协副主席（不驻会），民盟嘉定区主委、区规划资源局局长",
        "current_org": "中国人民政治协商会议上海市嘉定区委员会",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_36",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 区法院 & 区检察院
    # ═══════════════════════════════════════════════════════════════════════
    # 26. 毛译宇 — 法院院长
    {
        "id": 5001,
        "name": "毛译宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年12月",
        "birthplace": "",
        "education": "大学，法律硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区人民法院院长、党组书记",
        "current_org": "上海市嘉定区人民法院",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_741000",
    },
    # 27. 葛建军 — 检察院检察长
    {
        "id": 5002,
        "name": "葛建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年11月",
        "birthplace": "",
        "education": "在职大学，法律硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "嘉定区人民检察院检察长、党组书记",
        "current_org": "上海市嘉定区人民检察院",
        "source": "https://www.jiading.gov.cn/zwpd/ldzc/content_339430",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共上海市嘉定区委员会",
        "type": "党委",
        "level": "市辖区(直辖市)",
        "parent": "中共上海市委员会",
        "location": "上海市嘉定区",
    },
    {
        "id": 2,
        "name": "上海市嘉定区人民政府",
        "type": "政府",
        "level": "市辖区(直辖市)",
        "parent": "上海市人民政府",
        "location": "上海市嘉定区",
    },
    {
        "id": 3,
        "name": "嘉定区人民代表大会常务委员会",
        "type": "人大",
        "level": "市辖区(直辖市)",
        "parent": "上海市人民代表大会常务委员会",
        "location": "上海市嘉定区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议上海市嘉定区委员会",
        "type": "政协",
        "level": "市辖区(直辖市)",
        "parent": "中国人民政治协商会议上海市委员会",
        "location": "上海市嘉定区",
    },
    {
        "id": 5,
        "name": "中共上海市嘉定区纪律检查委员会",
        "type": "纪委",
        "level": "市辖区(直辖市)",
        "parent": "中共上海市纪律检查委员会",
        "location": "上海市嘉定区",
    },
    {
        "id": 6,
        "name": "上海市嘉定区人民法院",
        "type": "司法机关",
        "level": "市辖区(直辖市)",
        "parent": "上海市高级人民法院",
        "location": "上海市嘉定区",
    },
    {
        "id": 7,
        "name": "上海市嘉定区人民检察院",
        "type": "司法机关",
        "level": "市辖区(直辖市)",
        "parent": "上海市人民检察院",
        "location": "上海市嘉定区",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # Party Committee
    {"person_id": 1001, "org_id": 1, "title": "嘉定区委书记", "start_date": "", "end_date": "present", "rank": "正局级", "note": "2026年7月在任"},
    {"person_id": 1002, "org_id": 1, "title": "嘉定区委副书记", "start_date": "", "end_date": "present", "rank": "正局级", "note": "兼任区长"},
    {"person_id": 1003, "org_id": 1, "title": "嘉定区委副书记", "start_date": "", "end_date": "present", "rank": "副局级", "note": "区一级巡视员"},
    {"person_id": 1004, "org_id": 5, "title": "嘉定区委常委、区纪委书记", "start_date": "", "end_date": "present", "rank": "副局级", "note": "兼区监委主任，区一级巡视员"},
    {"person_id": 1005, "org_id": 1, "title": "嘉定区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副局级", "note": "兼区委党校校长，区一级巡视员"},
    {"person_id": 1006, "org_id": 2, "title": "嘉定区委常委、副区长", "start_date": "", "end_date": "present", "rank": "副局级", "note": "常务副区长，分管发改财政税务"},
    {"person_id": 1007, "org_id": 1, "title": "嘉定区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    {"person_id": 1008, "org_id": 1, "title": "嘉定区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    {"person_id": 1009, "org_id": 1, "title": "嘉定区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    {"person_id": 1010, "org_id": 1, "title": "嘉定区委常委、人武部政委", "start_date": "", "end_date": "present", "rank": "副局级", "note": ""},
    # Government
    {"person_id": 1002, "org_id": 2, "title": "嘉定区长", "start_date": "", "end_date": "present", "rank": "正局级", "note": "区政府党组书记"},
    {"person_id": 1006, "org_id": 2, "title": "嘉定区副区长（常务）", "start_date": "", "end_date": "present", "rank": "副局级", "note": "区政府党组成员"},
    {"person_id": 2001, "org_id": 2, "title": "嘉定区副区长", "start_date": "", "end_date": "present", "rank": "副局级", "note": "兼公安分局局长"},
    {"person_id": 2002, "org_id": 2, "title": "嘉定区副区长", "start_date": "", "end_date": "present", "rank": "副局级", "note": "分管城建交通"},
    {"person_id": 2003, "org_id": 2, "title": "嘉定区副区长", "start_date": "", "end_date": "present", "rank": "副局级", "note": "分管农业农村人社"},
    {"person_id": 2004, "org_id": 2, "title": "嘉定区副区长", "start_date": "", "end_date": "present", "rank": "副局级", "note": "分管教育卫健文旅，九三学社"},
    {"person_id": 2005, "org_id": 2, "title": "嘉定区副区长", "start_date": "", "end_date": "present", "rank": "副局级", "note": "分管商务数据信访"},
    # People's Congress
    {"person_id": 3001, "org_id": 3, "title": "嘉定区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正局级", "note": "党组书记"},
    {"person_id": 3002, "org_id": 3, "title": "嘉定区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副局级", "note": "党组成员，兼区总工会主席"},
    {"person_id": 3003, "org_id": 3, "title": "嘉定区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副局级", "note": "党组成员"},
    {"person_id": 3004, "org_id": 3, "title": "嘉定区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副局级", "note": "党组成员"},
    {"person_id": 3005, "org_id": 3, "title": "嘉定区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副局级", "note": "党组成员"},
    {"person_id": 3006, "org_id": 3, "title": "嘉定区人大常委会副主任（不驻会）", "start_date": "", "end_date": "present", "rank": "副局级", "note": "无党派，同济大学教授"},
    # CPPCC
    {"person_id": 4001, "org_id": 4, "title": "嘉定区政协主席", "start_date": "", "end_date": "present", "rank": "正局级", "note": "党组书记"},
    {"person_id": 4002, "org_id": 4, "title": "嘉定区政协副主席", "start_date": "", "end_date": "present", "rank": "副局级", "note": "党组成员"},
    {"person_id": 4003, "org_id": 4, "title": "嘉定区政协副主席（不驻会）", "start_date": "", "end_date": "present", "rank": "副局级", "note": "农工党"},
    {"person_id": 4004, "org_id": 4, "title": "嘉定区政协副主席（不驻会）", "start_date": "", "end_date": "present", "rank": "副局级", "note": "民盟"},
    # Judiciary
    {"person_id": 5001, "org_id": 6, "title": "嘉定区人民法院院长", "start_date": "", "end_date": "present", "rank": "副局级", "note": "党组书记"},
    {"person_id": 5002, "org_id": 7, "title": "嘉定区人民检察院检察长", "start_date": "", "end_date": "present", "rank": "副局级", "note": "党组书记"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # Top leadership partnership
    {"person_a": 1001, "person_b": 1002, "type": "superior_subordinate", "context": "区委书记—区长搭班子", "overlap_org": "嘉定区", "overlap_period": "present"},
    {"person_a": 1001, "person_b": 1003, "type": "superior_subordinate", "context": "区委书记—区委副书记", "overlap_org": "区委常委会", "overlap_period": "present"},
    {"person_a": 1002, "person_b": 1003, "type": "colleague", "context": "区委副书记同事关系", "overlap_org": "区委常委会", "overlap_period": "present"},
    # Standing committee collegial relationships
    {"person_a": 1001, "person_b": 1004, "type": "superior_subordinate", "context": "区委书记—纪委书记", "overlap_org": "区委常委会", "overlap_period": "present"},
    {"person_a": 1001, "person_b": 1005, "type": "superior_subordinate", "context": "区委书记—组织部长", "overlap_org": "区委常委会", "overlap_period": "present"},
    {"person_a": 1001, "person_b": 1006, "type": "superior_subordinate", "context": "区委书记—常务副区长", "overlap_org": "区委常委会", "overlap_period": "present"},
    {"person_a": 1001, "person_b": 1007, "type": "superior_subordinate", "context": "区委书记—宣传部长", "overlap_org": "区委常委会", "overlap_period": "present"},
    {"person_a": 1001, "person_b": 1008, "type": "superior_subordinate", "context": "区委书记—统战部长", "overlap_org": "区委常委会", "overlap_period": "present"},
    {"person_a": 1001, "person_b": 1009, "type": "superior_subordinate", "context": "区委书记—政法委书记", "overlap_org": "区委常委会", "overlap_period": "present"},
    {"person_a": 1001, "person_b": 1010, "type": "superior_subordinate", "context": "区委书记—人武部政委", "overlap_org": "区委常委会", "overlap_period": "present"},
    # Government team
    {"person_a": 1002, "person_b": 1006, "type": "superior_subordinate", "context": "区长—常务副区长", "overlap_org": "区政府", "overlap_period": "present"},
    {"person_a": 1002, "person_b": 2001, "type": "superior_subordinate", "context": "区长—副区长（公安）", "overlap_org": "区政府", "overlap_period": "present"},
    {"person_a": 1002, "person_b": 2002, "type": "superior_subordinate", "context": "区长—副区长（城建）", "overlap_org": "区政府", "overlap_period": "present"},
    {"person_a": 1002, "person_b": 2003, "type": "superior_subordinate", "context": "区长—副区长（农业）", "overlap_org": "区政府", "overlap_period": "present"},
    {"person_a": 1002, "person_b": 2004, "type": "superior_subordinate", "context": "区长—副区长（文教）", "overlap_org": "区政府", "overlap_period": "present"},
    {"person_a": 1002, "person_b": 2005, "type": "superior_subordinate", "context": "区长—副区长（商务）", "overlap_org": "区政府", "overlap_period": "present"},
]


def main() -> None:
    print(f"\n{'='*60}")
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区(直辖市)")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 嘉定区人民政府网站 (jiading.gov.cn)")
    print(f"{'='*60}")

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

    # If writing to staging, also refresh canonical copies
    for dst in [CANONICAL_DB, CANONICAL_GEXF]:
        if dst.exists():
            dst.unlink()
    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)

    print(f"\n{'='*60}")
    print(f"  嘉定区 数据构建完成")
    print(f"  DB:   {DB_PATH} -> {CANONICAL_DB}")
    print(f"  GEXF: {GEXF_PATH} -> {CANONICAL_GEXF}")
    print(f"  Persons:     {len(persons)}")
    print(f"  Orgs:        {len(organizations)}")
    print(f"  Positions:   {len(positions)}")
    print(f"  Relations:   {len(relationships)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
