#!/usr/bin/env python3
"""Build script for 万山区 (Wanshan District, Tongren, Guizhou) leadership network.

Generated: 2026-07-23
Level: 市辖区
Province: 贵州省
Parent City: 铜仁市
Targets: 区委书记 & 区长

Research Note:
  The district government website (www.trws.gov.cn) was accessible via direct HTTP.
  The 领导之窗 page confirmed all 11区委 leaders and 6区政府 leaders by name, role,
  demographic info, and work division (分工). Both core targets (刘浩 & 陈松) were
  found with complete biographies.

  Web search via Exa was rate-limited. All research was done via direct HTTP access
  to the district government website.

Sources:
  - http://www.trws.gov.cn/zwgk/ldzc/qwld1/ (区委领导 listing with detailed profiles)
  - http://www.trws.gov.cn/zwgk/ldzc/zfld1/ (政府领导 listing with detailed profiles)
  - http://www.trws.gov.cn/ (万山区人民政府 — news articles)
"""

import sqlite3  # noqa: used by gov_relation.runner
from pathlib import Path

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    # 区委书记 (PARTY SECRETARY) — CONFIRMED
    {
        "id": 1,
        "name": "刘浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年11月",
        "birthplace": "",
        "education": "研究生学历，博士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "万山区委书记，贵州万山经开区党工委书记",
        "current_org": "中共铜仁市万山区委员会",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/qwld1/202503/t20250327_87284462.html （官网确认简历）",
    },
    # 区长 (DISTRICT MAYOR) — CONFIRMED
    {
        "id": 2,
        "name": "陈松",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "在职法律硕士学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "万山区委副书记、区长、区政府党组书记，贵州万山经开区党工委副书记、管委会主任",
        "current_org": "铜仁市万山区人民政府",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/zfld1/202503/t20250327_87284460.html （官网确认简历）",
    },
    # ── 区委领导 (District Party Committee Leaders) ──
    # 区委副书记（挂职）
    {
        "id": 3,
        "name": "周建国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "万山区委副书记（挂职）",
        "current_org": "中共铜仁市万山区委员会",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/qwld1/202509/t20250903_88562883.html （官网确认）",
    },
    # 常务副区长（区委常委）
    {
        "id": 4,
        "name": "黄睿",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1981年7月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "万山区委常委、区政府常务副区长",
        "current_org": "铜仁市万山区人民政府",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/qwld1/202503/t20250327_87284458.html （官网确认简历）",
    },
    # 组织部部长
    {
        "id": 5,
        "name": "杨旭",
        "gender": "男",
        "ethnicity": "",
        "birth": "1983年9月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "万山区委常委、区委组织部部长、党校校长",
        "current_org": "中共铜仁市万山区委员会",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/qwld1/202503/t20250327_87284457.html （官网确认简历）",
    },
    # 区委常委、副区长
    {
        "id": 6,
        "name": "张曲",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1977年9月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "万山区委常委、区人民政府副区长",
        "current_org": "铜仁市万山区人民政府",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/qwld1/202503/t20250327_87284454.html （官网确认简历）",
    },
    # 人武部政委
    {
        "id": 7,
        "name": "田儒乾",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1978年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "万山区委常委、人武部政委",
        "current_org": "铜仁市万山区人民武装部",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/qwld1/202506/t20250630_88210867.html （官网确认简历）",
    },
    # 纪委书记
    {
        "id": 8,
        "name": "陈莉",
        "gender": "女",
        "ethnicity": "苗族",
        "birth": "1980年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "铜仁市监委委员，万山区委常委、纪委书记、监委主任",
        "current_org": "中共铜仁市万山区纪律检查委员会",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/qwld1/202605/t20260528_90223447.html （官网确认简历）",
    },
    # 政法委书记
    {
        "id": 9,
        "name": "王苏州",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1976年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "万山区委常委、区委政法委书记",
        "current_org": "中共铜仁市万山区委员会",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/qwld1/202607/t20260710_90607273.html （官网确认简历）",
    },
    # 经开区党工委副书记
    {
        "id": 10,
        "name": "杨光金",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1980年9月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "万山区委常委，贵州万山经开区党工委副书记、管委会副主任",
        "current_org": "贵州万山经济开发区",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/qwld1/202512/t20251226_89090411.html （官网确认简历）",
    },
    # 宣传部长、统战部长
    {
        "id": 11,
        "name": "杨胜荃",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1979年4月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "万山区委常委、宣传部部长、统战部部长",
        "current_org": "中共铜仁市万山区委员会",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/qwld1/202601/t20260122_89323900.html （官网确认简历）",
    },
    # ── 区政府领导 (District Government Leaders, non-常委) ──
    # 副区长（致公党）
    {
        "id": 12,
        "name": "罗雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "",
        "education": "本科学历，学士学位",
        "party_join": "致公党党员",
        "work_start": "",
        "current_post": "万山区人民政府副区长",
        "current_org": "铜仁市万山区人民政府",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/zfld1/202506/t20250630_88210366.html （官网确认简历）",
    },
    # 副区长（侗族）
    {
        "id": 13,
        "name": "姚斌",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "",
        "birthplace": "",
        "education": "在职本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "万山区人民政府副区长",
        "current_org": "铜仁市万山区人民政府",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/zfld1/202503/t20250327_87284467.html （官网确认简历）",
    },
    # 副区长（农工党）
    {
        "id": 14,
        "name": "谭铄斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中国农工民主党党员",
        "work_start": "",
        "current_post": "万山区人民政府副区长",
        "current_org": "铜仁市万山区人民政府",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/zfld1/202503/t20250327_87284466.html （官网确认简历）",
    },
    # 副区长、公安局局长
    {
        "id": 15,
        "name": "陈勇",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1985年9月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "万山区人民政府副区长、市公安局万山分局党委书记、局长",
        "current_org": "铜仁市公安局万山分局",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/zfld1/202606/t20260611_90515581.html （官网确认简历）",
    },
    # 副区长、财政局长
    {
        "id": 16,
        "name": "杨琪云",
        "gender": "女",
        "ethnicity": "侗族",
        "birth": "1976年7月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "万山区人民政府党组成员、副区长，区财政局党组书记、局长",
        "current_org": "铜仁市万山区人民政府",
        "source": "http://www.trws.gov.cn/zwgk/ldzc/zfld1/202503/t20250327_87284472.html （官网确认简历）",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共铜仁市万山区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜仁市委员会",
        "location": "贵州省铜仁市万山区",
    },
    {
        "id": 2,
        "name": "铜仁市万山区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "铜仁市人民政府",
        "location": "贵州省铜仁市万山区",
    },
    {
        "id": 3,
        "name": "铜仁市万山区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "铜仁市人大常委会",
        "location": "贵州省铜仁市万山区",
    },
    {
        "id": 4,
        "name": "铜仁市万山区政协委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "铜仁市政协",
        "location": "贵州省铜仁市万山区",
    },
    {
        "id": 5,
        "name": "中共铜仁市万山区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜仁市纪律检查委员会",
        "location": "贵州省铜仁市万山区",
    },
    {
        "id": 6,
        "name": "贵州万山经济开发区",
        "type": "开发区",
        "level": "县处级",
        "parent": "铜仁市人民政府",
        "location": "贵州省铜仁市万山区",
    },
    {
        "id": 7,
        "name": "铜仁市万山区人民武装部",
        "type": "事业单位",
        "level": "县处级",
        "parent": "铜仁军分区",
        "location": "贵州省铜仁市万山区",
    },
    {
        "id": 8,
        "name": "铜仁市公安局万山分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "铜仁市公安局",
        "location": "贵州省铜仁市万山区",
    },
]

POSITIONS = [
    # 刘浩 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "未知", "end": "现任", "rank": "县处级正职", "note": "1981年11月生，汉族，研究生学历，博士学位"},
    {"person_id": 1, "org_id": 6, "title": "贵州万山经开区党工委书记", "start": "未知", "end": "现任", "rank": "县处级正职", "note": "兼任"},
    # 陈松 — 区长
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "区政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "未知", "end": "现任", "rank": "县处级正职", "note": "1980年8月生，苗族，在职法律硕士学历"},
    {"person_id": 2, "org_id": 6, "title": "经开区党工委副书记、管委会主任", "start": "未知", "end": "现任", "rank": "县处级正职", "note": "兼任"},
    # 周建国 — 区委副书记（挂职）
    {"person_id": 3, "org_id": 1, "title": "区委副书记（挂职）", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "1973年12月生，汉族，在职大学学历，挂职"},
    # 黄睿 — 常务副区长
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "1981年7月生，土家族"},
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "协助区长分管财政、审计、粮食"},
    # 杨旭 — 组织部长
    {"person_id": 5, "org_id": 1, "title": "区委常委、组织部部长、党校校长", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "1983年9月生"},
    # 张曲 — 区委常委、副区长
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "1977年9月生，侗族，在职大学学历"},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "分管城市经济、住建、自然资源等"},
    # 田儒乾 — 人武部政委
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "1978年9月生，土家族，大学学历"},
    {"person_id": 7, "org_id": 7, "title": "人武部政委", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    # 陈莉 — 纪委书记
    {"person_id": 8, "org_id": 5, "title": "纪委书记、监委主任", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "女，1980年6月生，苗族，大学学历。铜仁市监委委员兼"},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    # 王苏州 — 政法委书记
    {"person_id": 9, "org_id": 1, "title": "区委常委、政法委书记", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "1976年11月生，土家族，大学学历"},
    # 杨光金 — 经开区
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "1980年9月生，侗族"},
    {"person_id": 10, "org_id": 6, "title": "经开区党工委副书记、管委会副主任", "start": "未知", "end": "现任", "rank": "县处级副职", "note": ""},
    # 杨胜荃 — 宣传部长、统战部长
    {"person_id": 11, "org_id": 1, "title": "区委常委、宣传部部长、统战部部长", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "女，1979年4月生，土家族，在职大学学历"},
    # 罗雷 — 副区长（致公党）
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "1975年10月生，汉族，本科学历，致公党党员"},
    # 姚斌 — 副区长
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "侗族，在职本科学历。分管农业农村、乡村振兴、交通运输等"},
    # 谭铄斌 — 副区长（农工党）
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "1980年12月生，汉族，大学学历，农工党党员"},
    # 陈勇 — 副区长、公安局长
    {"person_id": 15, "org_id": 2, "title": "副区长", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "1985年9月生，苗族，在职大学学历"},
    {"person_id": 15, "org_id": 8, "title": "公安分局党委书记、局长", "start": "未知", "end": "现任", "rank": "乡科级正职", "note": "兼任"},
    # 杨琪云 — 副区长、财政局长
    {"person_id": 16, "org_id": 2, "title": "副区长", "start": "未知", "end": "现任", "rank": "县处级副职", "note": "女，1976年7月生，侗族，大学学历"},
    {"person_id": 16, "org_id": 2, "title": "区财政局党组书记、局长", "start": "未知", "end": "现任", "rank": "乡科级正职", "note": "兼任"},
]

RELATIONSHIPS = [
    # 区委书记 ↔ 区长（核心搭档）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长搭档关系",
        "overlap_org": "中共铜仁市万山区委员会",
        "overlap_period": "现任",
    },
    # 陈松（区长）→ 黄睿（常务副区长）
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区长与常务副区长（协助分管财政、审计、粮食）",
        "overlap_org": "铜仁市万山区人民政府",
        "overlap_period": "现任",
    },
    # 陈松（区长）→ 张曲（副区长）
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "铜仁市万山区人民政府",
        "overlap_period": "现任",
    },
    # 陈松（区长）→ 罗雷（副区长）
    {
        "person_a": 2,
        "person_b": 12,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "铜仁市万山区人民政府",
        "overlap_period": "现任",
    },
    # 陈松（区长）→ 姚斌（副区长）
    {
        "person_a": 2,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "区长与副区长（分管农业农村、乡村振兴）",
        "overlap_org": "铜仁市万山区人民政府",
        "overlap_period": "现任",
    },
    # 陈松（区长）→ 谭铄斌（副区长）
    {
        "person_a": 2,
        "person_b": 14,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "铜仁市万山区人民政府",
        "overlap_period": "现任",
    },
    # 陈松（区长）→ 陈勇（副区长、公安局长）
    {
        "person_a": 2,
        "person_b": 15,
        "type": "superior_subordinate",
        "context": "区长与副区长、公安局长",
        "overlap_org": "铜仁市万山区人民政府",
        "overlap_period": "现任",
    },
    # 陈松（区长）→ 杨琪云（副区长、财政局长）
    {
        "person_a": 2,
        "person_b": 16,
        "type": "superior_subordinate",
        "context": "区长与副区长、财政局长",
        "overlap_org": "铜仁市万山区人民政府",
        "overlap_period": "现任",
    },
    # 刘浩（区委书记）→ 陈莉（纪委书记）
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "区委书记与纪委书记",
        "overlap_org": "中共铜仁市万山区委员会",
        "overlap_period": "现任",
    },
    # 刘浩（区委书记）→ 杨旭（组织部长）
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区委书记与组织部部长",
        "overlap_org": "中共铜仁市万山区委员会",
        "overlap_period": "现任",
    },
    # 杨旭（组织部长）←→ 杨胜荃（宣传/统战部长）同级
    {
        "person_a": 5,
        "person_b": 11,
        "type": "overlap",
        "context": "区委常委同级（组织部长与宣传/统战部长）",
        "overlap_org": "中共铜仁市万山区委员会",
        "overlap_period": "现任",
    },
    # 杨光金（经开区副书记）↔ 刘浩（经开区党工委书记）
    {
        "person_a": 1,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "经开区党工委书记与副书记",
        "overlap_org": "贵州万山经济开发区",
        "overlap_period": "现任",
    },
    # 杨光金（经开区副书记）↔ 陈松（经开区管委会主任）
    {
        "person_a": 2,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "经开区管委会主任与副主任",
        "overlap_org": "贵州万山经济开发区",
        "overlap_period": "现任",
    },
    # 王苏州（政法委书记）↔ 陈勇（公安局长）政法系统
    {
        "person_a": 9,
        "person_b": 15,
        "type": "superior_subordinate",
        "context": "政法委书记与公安局长（政法系统领导关系）",
        "overlap_org": "中共铜仁市万山区委员会",
        "overlap_period": "现任",
    },
]

DB_PATH = Path("data/tmp/guizhou_万山区") / "万山区_network.db"
GEXF_PATH = Path("data/tmp/guizhou_万山区") / "万山区_network.gexf"


def main():
    run_build(
        slug="万山区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Done.")


if __name__ == "__main__":
    main()
