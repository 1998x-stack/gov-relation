#!/usr/bin/env python3
"""Build script for 岑巩县 (Cengong County, 黔东南州, 贵州省) leadership network.

Generated: 2026-07-23
Level: 县
Province: 贵州省
Parent City: 黔东南苗族侗族自治州
Targets: 县委书记 & 县长

Research Note:
  The county government website (www.qdncg.gov.cn) was fully accessible.
  The 领导之窗 page confirmed the full county government roster with detailed
  biographies and work divisions. Party committee leadership (县委领导班子)
  was confirmed from news articles on the same domain (June-July 2026).

  Notes on gaps:
  - 冉超 (县委书记): Confirmed name from multiple official sources, but no
    detailed biography page was found. Birth year, birthplace, education,
    and career history are all unknown.
  - 何洪道 (宣传部部长、统战部部长): Name confirmed, no biography available.
  - 龙杰 (组织部部长): Name confirmed, no biography available.
  - 李兴旺、刘有祥、李建 (县委副书记): Names confirmed, roles confirmed,
    but no detailed career histories available.
  - Previous 县委书记 (杨伟): Name from prior reports, after being
    investigated/removed. Exact fate unknown.
  - Previous 县长 (吴昌盛): Name from prior reports, replacement by 王思红
    around Jan 2022. Exact whereabouts unknown.

Sources:
  - https://www.qdncg.gov.cn/zwgk/ldzc/ (领导之窗 — confirmed all 10 government leaders)
  - https://www.qdncg.gov.cn/ (news articles confirming 县委 leadership)
"""

import sqlite3  # noqa
from pathlib import Path

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    # 县委书记 (PARTY SECRETARY) — Name confirmed, no detailed bio
    {
        "id": 1,
        "name": "冉超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "岑巩县委书记",
        "current_org": "中共岑巩县委员会",
        "source": "https://www.qdncg.gov.cn/xwzx/zwyw/202607/t20260702_90577435.html （官方新闻确认姓名）",
    },
    # 县长 (COUNTY MAYOR) — Confirmed from leadership page
    {
        "id": 2,
        "name": "王思红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "岑巩县委副书记、县人民政府党组书记、县长",
        "current_org": "岑巩县人民政府",
        "source": "https://www.qdncg.gov.cn/zwgk/ldzc/202201/t20220112_85100714.html （官网领导之窗确认简历）",
    },
    # ── 县委领导班子 (names confirmed from news articles) ──
    {
        "id": 3,
        "name": "李兴旺",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "岑巩县委副书记、思旸镇党委书记",
        "current_org": "中共岑巩县委员会",
        "source": "https://www.qdncg.gov.cn/xwzx/rdtj/202607/t20260703_90586039.html （官方新闻）",
    },
    {
        "id": 4,
        "name": "刘有祥",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "岑巩县委副书记",
        "current_org": "中共岑巩县委员会",
        "source": "https://www.qdncg.gov.cn/xwzx/zwyw/202607/t20260702_90577435.html （官方新闻）",
    },
    {
        "id": 5,
        "name": "李建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "岑巩县委副书记",
        "current_org": "中共岑巩县委员会",
        "source": "https://www.qdncg.gov.cn/xwzx/rdtj/202607/t20260715_90621243.html （官方新闻）",
    },
    {
        "id": 6,
        "name": "葛银",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1982年10月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "岑巩县委常委、县人民政府副县长（常务）",
        "current_org": "岑巩县人民政府",
        "source": "https://www.qdncg.gov.cn/zwgk/ldzc/202509/t20250905_88569520.html （官网领导之窗确认简历）",
    },
    {
        "id": 7,
        "name": "何洪道",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "岑巩县委常委、宣传部部长、统战部部长",
        "current_org": "中共岑巩县委宣传部",
        "source": "https://www.qdncg.gov.cn/xwzx/zwyw/202606/t20260624_90549827.html （官方新闻确认）",
    },
    {
        "id": 8,
        "name": "龙杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "岑巩县委常委、组织部部长",
        "current_org": "中共岑巩县委组织部",
        "source": "https://www.qdncg.gov.cn/xwzx/rdtj/202607/t20260703_90586039.html （官方新闻确认）",
    },
    {
        "id": 9,
        "name": "洪加久",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1982年9月",
        "birthplace": "",
        "education": "工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "岑巩县委常委、县人民政府党组成员、副县长",
        "current_org": "岑巩县人民政府",
        "source": "https://www.qdncg.gov.cn/zwgk/ldzc/202404/t20240428_85100740.html （官网领导之窗确认简历）",
    },
    {
        "id": 10,
        "name": "何伟棠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年7月",
        "birthplace": "",
        "education": "工商管理专业硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "岑巩县委委员、常委、县人民政府党组成员、副县长（挂职）",
        "current_org": "岑巩县人民政府",
        "source": "https://www.qdncg.gov.cn/zwgk/ldzc/202404/t20240430_85100742.html （官网领导之窗确认简历）",
    },
    # ── 县政府领导班子 (其余成员) ──
    {
        "id": 11,
        "name": "姚茂勋",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1974年6月",
        "birthplace": "",
        "education": "省委党校大学学历",
        "party_join": "农工党党员",
        "work_start": "",
        "current_post": "岑巩县人民政府副县长",
        "current_org": "岑巩县人民政府",
        "source": "https://www.qdncg.gov.cn/zwgk/ldzc/202011/t20201116_85100716.html （官网领导之窗确认简历）",
    },
    {
        "id": 12,
        "name": "吴述涛",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1974年4月",
        "birthplace": "",
        "education": "农学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "岑巩县人民政府党组成员、副县长",
        "current_org": "岑巩县人民政府",
        "source": "https://www.qdncg.gov.cn/zwgk/ldzc/202111/t20211103_85100737.html （官网领导之窗确认简历）",
    },
    {
        "id": 13,
        "name": "高俊发",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1973年12月",
        "birthplace": "",
        "education": "省委党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "岑巩县人民政府党组成员、副县长",
        "current_org": "岑巩县人民政府",
        "source": "https://www.qdncg.gov.cn/zwgk/ldzc/202201/t20220107_85100738.html （官网领导之窗确认简历）",
    },
    {
        "id": 14,
        "name": "罗国泮",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1978年10月",
        "birthplace": "",
        "education": "大学本科工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "岑巩县人民政府党组成员、副县长",
        "current_org": "岑巩县人民政府",
        "source": "https://www.qdncg.gov.cn/zwgk/ldzc/202404/t20240429_85100741.html （官网领导之窗确认简历）",
    },
    {
        "id": 15,
        "name": "张治藩",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1982年9月",
        "birthplace": "",
        "education": "在职工程硕士学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "岑巩县人民政府党组成员、副县长，县公安局党委书记、局长",
        "current_org": "岑巩县人民政府",
        "source": "https://www.qdncg.gov.cn/zwgk/ldzc/202309/t20230913_85100739.html （官网领导之窗确认简历）",
    },
    {
        "id": 16,
        "name": "吴金隆",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1988年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "岑巩县人民政府党组成员、机关党组书记、办公室主任",
        "current_org": "岑巩县人民政府办公室",
        "source": "https://www.qdncg.gov.cn/zwgk/ldzc/202512/t20251215_89043838.html （官网领导之窗确认简历）",
    },
    # ── 人大、政协 ──
    {
        "id": 17,
        "name": "刘文辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "岑巩县人大常委会主任",
        "current_org": "岑巩县人大常委会",
        "source": "https://www.qdncg.gov.cn/xwzx/zwyw/202607/t20260702_90577435.html （官方新闻确认）",
    },
    {
        "id": 18,
        "name": "杨和",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "岑巩县政协主席",
        "current_org": "政协岑巩县委员会",
        "source": "https://www.qdncg.gov.cn/xwzx/zwyw/202607/t20260702_90577435.html （官方新闻确认）",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共岑巩县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共黔东南苗族侗族自治州委员会",
        "location": "贵州省黔东南州岑巩县",
    },
    {
        "id": 2,
        "name": "岑巩县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "黔东南苗族侗族自治州人民政府",
        "location": "贵州省黔东南州岑巩县",
    },
    {
        "id": 3,
        "name": "岑巩县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "黔东南州人大常委会",
        "location": "贵州省黔东南州岑巩县",
    },
    {
        "id": 4,
        "name": "政协岑巩县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协黔东南州委员会",
        "location": "贵州省黔东南州岑巩县",
    },
    {
        "id": 5,
        "name": "中共岑巩县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共岑巩县委员会",
        "location": "贵州省黔东南州岑巩县",
    },
    {
        "id": 6,
        "name": "中共岑巩县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共岑巩县委员会",
        "location": "贵州省黔东南州岑巩县",
    },
    {
        "id": 7,
        "name": "岑巩县人民政府办公室",
        "type": "政府",
        "level": "乡科级",
        "parent": "岑巩县人民政府",
        "location": "贵州省黔东南州岑巩县",
    },
    {
        "id": 8,
        "name": "岑巩县公安局",
        "type": "政府",
        "level": "乡科级",
        "parent": "岑巩县人民政府",
        "location": "贵州省黔东南州岑巩县",
    },
    {
        "id": 9,
        "name": "思旸镇党委",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共岑巩县委员会",
        "location": "贵州省黔东南州岑巩县思旸镇",
    },
]

POSITIONS = [
    # 冉超 — 县委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "岑巩县委书记",
        "start": "未知",
        "end": "现任",
        "rank": "县处级正职",
        "note": "姓名通过官方新闻确认（2026年6-7月多次报道），出生年份、性别、民族、履历待查",
    },
    # 王思红 — 县长
    {
        "person_id": 2,
        "org_id": 1,
        "title": "岑巩县委副书记",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "岑巩县人民政府党组书记、县长",
        "start": "大约2022年1月",
        "end": "现任",
        "rank": "县处级正职",
        "note": "1980年11月生，女，汉族，省委党校研究生学历，中共党员",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "岑巩经济开发区党工委副书记、管委会主任",
        "start": "未知",
        "end": "现任",
        "rank": "",
        "note": "兼任",
    },
    # 李兴旺 — 县委副书记
    {
        "person_id": 3,
        "org_id": 1,
        "title": "岑巩县委副书记",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "兼思旸镇党委书记",
    },
    {
        "person_id": 3,
        "org_id": 9,
        "title": "思旸镇党委书记（兼）",
        "start": "未知",
        "end": "现任",
        "rank": "乡科级正职",
        "note": "",
    },
    # 刘有祥 — 县委副书记
    {
        "person_id": 4,
        "org_id": 1,
        "title": "岑巩县委副书记",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    # 李建 — 县委副书记
    {
        "person_id": 5,
        "org_id": 1,
        "title": "岑巩县委副书记",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "参与中央单位定点帮扶工作",
    },
    # 葛银 — 常务副县长
    {
        "person_id": 6,
        "org_id": 1,
        "title": "岑巩县委常委",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 6,
        "org_id": 2,
        "title": "岑巩县人民政府副县长（常务）",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "负责常务工作, 1982年10月生，苗族，本科学历",
    },
    # 何洪道 — 宣传部部长、统战部部长
    {
        "person_id": 7,
        "org_id": 1,
        "title": "岑巩县委常委",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 7,
        "org_id": 5,
        "title": "岑巩县委宣传部部长、县委统战部部长",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    # 龙杰 — 组织部部长
    {
        "person_id": 8,
        "org_id": 1,
        "title": "岑巩县委常委",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 8,
        "org_id": 6,
        "title": "岑巩县委组织部部长",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    # 洪加久 — 县委常委、副县长
    {
        "person_id": 9,
        "org_id": 1,
        "title": "岑巩县委常委",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 9,
        "org_id": 2,
        "title": "岑巩县人民政府副县长",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "1982年9月生，土家族，工学学士，负责工业、招商等",
    },
    # 何伟棠 — 挂职副县长
    {
        "person_id": 10,
        "org_id": 1,
        "title": "岑巩县委常委（挂职）",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 10,
        "org_id": 2,
        "title": "岑巩县人民政府副县长（挂职）",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "1975年7月生，汉族，工商管理硕士，协助乡村振兴和招商",
    },
    # 姚茂勋 — 副县长
    {
        "person_id": 11,
        "org_id": 2,
        "title": "岑巩县人民政府副县长",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "1974年6月生，侗族，省委党校大学，农工党党员，负责住建、水务、卫健等",
    },
    # 吴述涛 — 副县长
    {
        "person_id": 12,
        "org_id": 2,
        "title": "岑巩县人民政府副县长",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "1974年4月生，侗族，农学学士，中共党员，负责农业农村、乡村振兴等",
    },
    # 高俊发 — 副县长
    {
        "person_id": 13,
        "org_id": 2,
        "title": "岑巩县人民政府副县长",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "1973年12月生，侗族，省委党校大学，中共党员，负责民政、文旅、交通等",
    },
    # 罗国泮 — 副县长
    {
        "person_id": 14,
        "org_id": 2,
        "title": "岑巩县人民政府副县长",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "1978年10月生，侗族，工学学士，中共党员，负责教育、人社、市场监管等",
    },
    # 张治藩 — 副县长、公安局长
    {
        "person_id": 15,
        "org_id": 2,
        "title": "岑巩县人民政府副县长",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 15,
        "org_id": 8,
        "title": "岑巩县公安局党委书记、局长",
        "start": "未知",
        "end": "现任",
        "rank": "乡科级正职",
        "note": "1982年9月生，侗族，在职工程硕士，中共党员",
    },
    # 吴金隆 — 政府办主任
    {
        "person_id": 16,
        "org_id": 2,
        "title": "岑巩县人民政府党组成员",
        "start": "未知",
        "end": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 16,
        "org_id": 7,
        "title": "岑巩县人民政府办公室主任",
        "start": "未知",
        "end": "现任",
        "rank": "乡科级正职",
        "note": "1988年12月生，苗族，大学学历，中共党员",
    },
    # 刘文辉 — 人大主任
    {
        "person_id": 17,
        "org_id": 3,
        "title": "岑巩县人大常委会主任",
        "start": "未知",
        "end": "现任",
        "rank": "县处级正职",
        "note": "",
    },
    # 杨和 — 政协主席
    {
        "person_id": 18,
        "org_id": 4,
        "title": "岑巩县政协主席",
        "start": "未知",
        "end": "现任",
        "rank": "县处级正职",
        "note": "",
    },
]

RELATIONSHIPS = [
    # 冉超 (书记) ↔ 王思红 (县长) — 党政一把手搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长党政搭档",
        "overlap_org": "中共岑巩县委员会",
        "overlap_period": "现任",
    },
    # 冉超 (书记) ↔ 三名副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记（李兴旺兼思旸镇党委书记）",
        "overlap_org": "中共岑巩县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记刘有祥",
        "overlap_org": "中共岑巩县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记李建",
        "overlap_org": "中共岑巩县委员会",
        "overlap_period": "现任",
    },
    # 冉超 (书记) ↔ 常委成员
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委、常务副县长葛银",
        "overlap_org": "中共岑巩县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委、宣传部部长何洪道",
        "overlap_org": "中共岑巩县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委、组织部部长龙杰",
        "overlap_org": "中共岑巩县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委、副县长洪加久",
        "overlap_org": "中共岑巩县委员会",
        "overlap_period": "现任",
    },
    # 王思红 (县长) ↔ 副县长们
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县长与常务副县长葛银（协助县长负责财政、审计）",
        "overlap_org": "岑巩县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "县长与副县长洪加久",
        "overlap_org": "岑巩县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "县长与副县长姚茂勋",
        "overlap_org": "岑巩县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 12,
        "type": "superior_subordinate",
        "context": "县长与副县长吴述涛",
        "overlap_org": "岑巩县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "县长与副县长高俊发",
        "overlap_org": "岑巩县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 14,
        "type": "superior_subordinate",
        "context": "县长与副县长罗国泮",
        "overlap_org": "岑巩县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 15,
        "type": "superior_subordinate",
        "context": "县长与副县长、公安局长张治藩",
        "overlap_org": "岑巩县人民政府",
        "overlap_period": "现任",
    },
]

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "岑巩县_network.db"
GEXF_PATH = STAGING_DIR / "岑巩县_network.gexf"


def main():
    run_build(
        slug="岑巩县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Persons: {len(PERSONS)}")
    print(f"Organizations: {len(ORGANIZATIONS)}")
    print(f"Positions: {len(POSITIONS)}")
    print(f"Relationships: {len(RELATIONSHIPS)}")
    print("Done.")


if __name__ == "__main__":
    main()
