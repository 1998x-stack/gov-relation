#!/usr/bin/env python3
"""Build script for 雷山县 (Leishan County, 黔东南苗族侗族自治州, 贵州省) leadership network.

Generated: 2026-08-05
Level: 县
Province: 贵州省
Parent City: 黔东南苗族侗族自治州
Targets: 县委书记 & 县长

Research Note (as-of 2026-08):
  The county government website (www.leishan.gov.cn) was fully accessible. The
  领导之窗 page confirmed the full county government roster with detailed
  biographies for 县长 黎琨 and 副县长 (刘玉林/张建明/彭城/石小妹). The
  county party committee leadership (县委领导班子) was confirmed from official
  leader-activity news & 县委常委会会议 articles on the same domain (Jan-Aug 2026).

  Confirmed leadership:
  - 县委书记 潘黔昆 (在任, 多次主持县委常委会/读书班, 2026年1-8月)
  - 县委副书记、县长 黎琨 (1987年6月生, 布依族, 研究生/工程硕士, 中共党员)
  - 县委副书记 敖德玉;  县委副书记、县委组织部部长、县委党校校长 陈序云;  县委副书记 陈尔鲲
  - 县人大常委会主任 罗祖新;  县政协主席 石虎
  - 副县长: 刘玉林(常务), 张建明, 彭城(兼公安局长), 卫红星, 石小妹
  - 县委常委、县委办主任 吴江辉; 县领导 王先贵, 龙剑, 杨胜荣, 陈明府

  Notes on gaps:
  - 潘黔昆 (县委书记): 身份 confirmed from multiple official news articles (2026),
    but no standalone biography page was found on the government website. Birth year,
    birthplace, education, and career history are unknown (履历待查).
  - 前任县委书记: 未在全国可访问来源中确认 (外网搜索受限: Exa限流/Baidu403/Jina不可达).
  - 陈序云角色变化: 2026年初为 县委常委、县委组织部部长, 2026年年中升任 县委副书记。

Sources:
  - https://www.leishan.gov.cn/zwgk/ldzc/ (领导之窗 — confirmed government leaders)
  - https://www.leishan.gov.cn/xwzx/ldhd/ (领导活动/新闻 — confirmed 县委领导班子)
"""

import sys
from pathlib import Path

# Locate repo root robustly regardless of where this script sits
_here = Path(__file__).resolve().parent
_REPO = next((p for p in (_here,) + tuple(_here.parents)
              if (p / "gov_relation").is_dir()), _here)
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leader 1: 县委书记 (PARTY SECRETARY) ──
{
        "id": 1,
        "name": "潘黔昆",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1974年4月",
        "birthplace": "贵州凯里",
        "education": "省委党校在职研究生学历",
        "party_join": "中共党员（1997年6月）",
        "work_start": "1994年8月",
        "current_post": "雷山县委书记、县人武部党委第一书记",
        "current_org": "中共雷山县委员会",
        "source": "https://www.leishan.gov.cn/xwzx/ldhd/202608/t20260803_90689975.html（官方新闻确认在任；履历见百度百科词条）",
    },
    # ── Core Leader 2: 县长 (COUNTY MAYOR) ──
    {
        "id": 2,
        "name": "黎琨",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1987年6月",
        "birthplace": "",
        "education": "研究生学历（工程硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "雷山县委副书记、县人民政府县长",
        "current_org": "雷山县人民政府",
        "source": "https://www.leishan.gov.cn/zwgk/ldzc/202508/t20250826_88519267.html （官网领导之窗确认简历）",
    },
    # ── 县委副书记 (专职) ──
    {
        "id": 3,
        "name": "敖德玉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "雷山县委副书记",
        "current_org": "中共雷山县委员会",
        "source": "https://www.leishan.gov.cn/xwzx/ldhd/202603/t20260323_89897535.html （县委常委会述责述廉会议确认）",
    },
    {
        "id": 4,
        "name": "陈序云",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "雷山县委副书记、县委组织部部长、县委党校校长",
        "current_org": "中共雷山县委员会",
        "source": "https://www.leishan.gov.cn/xwzx/ldhd/202607/t20260713_90613628.html （官方新闻确认，7月10日县委工作会议）",
    },
    {
        "id": 5,
        "name": "陈尔鲲",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "雷山县委副书记",
        "current_org": "中共雷山县委员会",
        "source": "https://www.leishan.gov.cn/xwzx/ldhd/202607/t20260713_90613628.html （官方新闻确认，7月10日县委工作会议）",
    },
    # ── 县委常委 ──
    {
        "id": 6,
        "name": "吴江辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "雷山县委常委、县委办公室主任",
        "current_org": "中共雷山县委员会",
        "source": "https://www.leishan.gov.cn/xwzx/ldhd/202602/t20260214_89547716.html （官方新闻确认，春节慰问）",
    },
    {
        "id": 7,
        "name": "刘玉林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2008年7月",
        "current_post": "雷山县委常委、县人民政府常务副县长",
        "current_org": "雷山县人民政府",
        "source": "https://www.leishan.gov.cn/zwgk/ldzc/202505/t20250527_87927537.html （官网领导之窗确认简历）",
    },
    # ── 县政府领导班子 (confirmed from 领导之窗) ──
    {
        "id": 8,
        "name": "张建明",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1982年6月",
        "birthplace": "",
        "education": "省委党校大学学历（法律专业）",
        "party_join": "中共党员",
        "work_start": "2005年12月",
        "current_post": "雷山县人民政府党组成员、副县长",
        "current_org": "雷山县人民政府",
        "source": "https://www.leishan.gov.cn/zwgk/ldzc/202112/t20211217_75780769.html （官网领导之窗确认简历）",
    },
    {
        "id": 9,
        "name": "彭城",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1985年3月",
        "birthplace": "贵州锦屏人",
        "education": "",
        "party_join": "中共党员",
        "work_start": "2007年6月",
        "current_post": "雷山县人民政府党组成员、副县长，县公安局党委书记、局长、督察长",
        "current_org": "雷山县人民政府",
        "source": "https://www.leishan.gov.cn/zwgk/ldzc/202406/t20240605_84728336.html （官网领导之窗确认简历）",
    },
    {
        "id": 10,
        "name": "卫红星",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "雷山县人民政府副县长",
        "current_org": "雷山县人民政府",
        "source": "https://www.leishan.gov.cn/xwzx/ldhd/202607/t20260713_90613628.html （官方新闻确认，7月10日县委工作会议）",
    },
    {
        "id": 11,
        "name": "石小妹",
        "gender": "女",
        "ethnicity": "苗族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "雷山县人民政府副县长",
        "current_org": "雷山县人民政府",
        "source": "https://www.leishan.gov.cn/xwzx/ldhd/202607/t20260731_90683458.html （官方新闻确认）",
    },
    # ── 人大 / 政协 ──
    {
        "id": 12,
        "name": "罗祖新",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "雷山县人大常委会主任",
        "current_org": "雷山县人大常委会",
        "source": "https://www.leishan.gov.cn/xwzx/ldhd/202603/t20260323_89897535.html （县委常委会述责述廉会议确认）",
    },
    {
        "id": 13,
        "name": "石虎",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "雷山县政协主席",
        "current_org": "雷山县政协",
        "source": "https://www.leishan.gov.cn/xwzx/ldhd/202607/t20260728_90667981.html （县委常委会新闻确认）",
    },
    # ── 县领导 (其他, from news) ──
    {
        "id": 14,
        "name": "王先贵",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "雷山县领导",
        "current_org": "中共雷山县委员会",
        "source": "https://www.leishan.gov.cn/xwzx/ldhd/202608/t20260803_90689975.html （官方新闻确认，八一建军节调研）",
    },
    {
        "id": 15,
        "name": "龙剑",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "雷山县领导",
        "current_org": "中共雷山县委员会",
        "source": "https://www.leishan.gov.cn/xwzx/ldhd/202602/t20260214_89547716.html （官方新闻确认，春节慰问）",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共雷山县委员会", "type": "党委", "level": "县级", "parent": "中共黔东南州委员会", "location": "贵州省黔东南州雷山县"},
    {"id": 2, "name": "雷山县人民政府", "type": "政府", "level": "县级", "parent": "黔东南州人民政府", "location": "贵州省黔东南州雷山县"},
    {"id": 3, "name": "雷山县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "黔东南州人大常委会", "location": "贵州省黔东南州雷山县"},
    {"id": 4, "name": "中国人民政治协商会议雷山县委员会", "type": "政协", "level": "县级", "parent": "黔东南州政协", "location": "贵州省黔东南州雷山县"},
    {"id": 5, "name": "中共雷山县委组织部", "type": "党委", "level": "县级", "parent": "中共雷山县委员会", "location": "贵州省黔东南州雷山县"},
    {"id": 6, "name": "中共雷山县委办公室", "type": "党委", "level": "县级", "parent": "中共雷山县委员会", "location": "贵州省黔东南州雷山县"},
    {"id": 7, "name": "雷山县公安局", "type": "政府", "level": "正科级", "parent": "雷山县人民政府", "location": "贵州省黔东南州雷山县"},
    {"id": 8, "name": "中共雷山县委党校", "type": "党委", "level": "县级", "parent": "中共雷山县委员会", "location": "贵州省黔东南州雷山县"},
]

POSITIONS = [
    # 县委
    {"person_id": 1, "org_id": 1, "title": "雷山县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026年1-8月多次以县委书记身份主持县委常委会会议"},
    {"person_id": 2, "org_id": 1, "title": "雷山县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼县长"},
    {"person_id": 3, "org_id": 1, "title": "雷山县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026年3月主持政法会议"},
    {"person_id": 4, "org_id": 1, "title": "雷山县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼县委组织部部长、县委党校校长"},
    {"person_id": 4, "org_id": 5, "title": "雷山县委组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼县委党校校长"},
    {"person_id": 4, "org_id": 8, "title": "雷山县委党校校长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "雷山县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "雷山县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "雷山县委办公室主任", "start_date": "", "end_date": "present", "rank": "正科级", "note": "兼县委常委"},
    {"person_id": 7, "org_id": 1, "title": "雷山县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼常务副县长"},
    # 政府
    {"person_id": 2, "org_id": 2, "title": "雷山县人民政府县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "领导政府全面工作，负责财政、审计、粮食"},
    {"person_id": 7, "org_id": 2, "title": "雷山县人民政府常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责发展改革、财税金融、人社等领域"},
    {"person_id": 8, "org_id": 2, "title": "雷山县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责工业、住建、生态、交通、供销"},
    {"person_id": 9, "org_id": 2, "title": "雷山县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责公安、司法、退役军人、信访"},
    {"person_id": 9, "org_id": 7, "title": "雷山县公安局局长、党委书记", "start_date": "", "end_date": "present", "rank": "正科级", "note": "兼县委政法委委员、副县长"},
    {"person_id": 10, "org_id": 2, "title": "雷山县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "雷山县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026年7月30日调研政务服务"},
    # 人大 / 政协
    {"person_id": 12, "org_id": 3, "title": "雷山县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 13, "org_id": 4, "title": "雷山县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

RELATIONSHIPS = [
    # 县委核心：书记与县长
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政搭档", "overlap_org": "中共雷山县委员会", "overlap_period": "2026"},
    # 书记与专职副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与专职副书记", "overlap_org": "中共雷山县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与副书记、组织部长同框调研", "overlap_org": "中共雷山县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与专职副书记", "overlap_org": "中共雷山县委员会", "overlap_period": "2026"},
    # 书记与人大 / 政协 / 常委
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "县四大班子同框", "overlap_org": "中共雷山县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "县四大班子同框", "overlap_org": "中共雷山县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与县委办主任（随行调研）", "overlap_org": "中共雷山县委员会", "overlap_period": "2026"},
    # 县长与副县长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "雷山县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与副县长（1月4日同赴丹江镇调研）", "overlap_org": "雷山县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长/公安局长", "overlap_org": "雷山县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "雷山县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "雷山县人民政府", "overlap_period": "2026"},
]

# fmt: on
# ═══════════════════════════════════════════════════


def build(db_path, gexf_path):
    """Build the 雷山县 leadership network."""
    from gov_relation.runner import run_build as _run_build
    _run_build(
        slug="雷山县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=db_path,
        gexf_path=gexf_path,
    )


if __name__ == "__main__":
    import sqlite3
    DB_PATH = Path(__file__).parent / "雷山县_network.db"
    GEXF_PATH = Path(__file__).parent / "雷山县_network.gexf"
    build(DB_PATH, GEXF_PATH)
    with sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True) as conn:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        assert {"persons", "organizations", "positions", "relationships"} <= tables
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in ("persons", "organizations", "positions", "relationships")}
    print(f"✅ 雷山县 network built successfully.")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   counts: {counts}")