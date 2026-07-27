#!/usr/bin/env python3
"""Build script for 荔波县 (Libo County, 黔南州, 贵州省) leadership network.

Generated: 2026-07-23
Level: 县
Province: 贵州省
Parent City: 黔南布依族苗族自治州
Targets: 县委书记 & 县长

Research Note:
  The county government website (www.libo.gov.cn) was fully accessible.
  The 政务公开 > 领导之窗 page confirmed the full county party committee and
  government leadership roster. Individual biography pages were accessed for
  all县委领导 and县政府领导 members.

  Confirmed current officeholders (as of May 2026):
  - 余登利: 县委书记 (name confirmed from official县委领导 sidebar listing;
    no dedicated biography page found on the website)
  - 马登宏: 县委副书记、县人民政府县长 (full bio on official website)

  The县委领导 section includes 12 members. The县政府 section includes
  8 members. Leadership pages last updated May 2026.

  Notes on gaps:
  - 余登利 (县委书记): Name confirmed from official县委领导 sidebar, but no
    detailed biography page found. Birth year, birthplace, education, and
    career history are all unknown. Also listed in other county-level cadres.
  - 彭佐扬 (挂职副书记): Name confirmed, no biography available.
  - 吕建军 (挂职副县长): Name confirmed, no biography.
  - Previous 县委书记: Not confirmed from currently accessible pages.
  - Previous 县长: Not confirmed from currently accessible pages.

Sources:
  - https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/ (领导之窗)
  - https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5999926/ (县委领导)
  - https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld_5981819/ (县政府领导)
  - Individual bio pages for each leader (see source fields)
"""

import sqlite3
from pathlib import Path

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

PERSONS = [
    # ── Core Leaders ──
    # 县委书记 (PARTY SECRETARY) — Name confirmed from official sidebar, no detailed bio
    {
        "id": 1,
        "name": "余登利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县委书记",
        "current_org": "中共荔波县委员会",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5999926/ （县委领导页面侧栏确认姓名与职务）",
    },
    # 县长 (COUNTY MAYOR) — Confirmed from leadership page
    {
        "id": 2,
        "name": "马登宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县委副书记、县人民政府县长",
        "current_org": "荔波县人民政府",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5999926/202605/t20260519_90190191.html （官网县委领导页面）",
    },
    # ── 县委领导班子 (confirmed from official pages) ──
    {
        "id": 3,
        "name": "曾松林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县委副书记、县委政法委书记",
        "current_org": "中共荔波县委员会",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5999926/202605/t20260519_90190210.html",
    },
    {
        "id": 4,
        "name": "彭佐扬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县委副书记（挂职）",
        "current_org": "中共荔波县委员会",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5999926/202605/t20260519_90190217.html",
    },
    {
        "id": 5,
        "name": "谢义鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县委常委、县人民政府常务副县长",
        "current_org": "中共荔波县委员会 / 荔波县人民政府",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5999926/202605/t20260519_90190227.html",
    },
    {
        "id": 6,
        "name": "龙怀",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县委常委、县委统战部部长、县政协党组副书记",
        "current_org": "中共荔波县委员会",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5999926/202605/t20260519_90190231.html",
    },
    {
        "id": 7,
        "name": "娄钧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县委常委、县纪委书记、县监委主任",
        "current_org": "中共荔波县纪律检查委员会 / 荔波县监察委员会",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5999926/202605/t20260519_90190240.html",
    },
    {
        "id": 8,
        "name": "颜东梅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县委常委、县委组织部部长、县委党校校长（兼）",
        "current_org": "中共荔波县委员会",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5999926/202605/t20260519_90190244.html",
    },
    {
        "id": 9,
        "name": "胡晴",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县委常委、县委办公室主任，县直属机关工作委员会书记",
        "current_org": "中共荔波县委员会",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5999926/202605/t20260519_90190250.html",
    },
    {
        "id": 10,
        "name": "瞿双",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县委常委、县委宣传部部长、县教育工作委员会书记",
        "current_org": "中共荔波县委员会",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5999926/202605/t20260519_90190262.html",
    },
    {
        "id": 11,
        "name": "李仕富",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县委常委、副县长（提名）、荔波樟江风景名胜区管理处党组书记",
        "current_org": "中共荔波县委员会 / 荔波县人民政府",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xwld_5999926/202605/t20260519_90190265.html",
    },
    {
        "id": 12,
        "name": "吕建军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县委常委、县人民政府副县长（挂职）",
        "current_org": "中共荔波县委员会 / 荔波县人民政府",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld_5981819/202503/t20250326_87280301.html",
    },
    # ── 县政府其他领导 ──
    {
        "id": 13,
        "name": "卢小泉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县人民政府副县长",
        "current_org": "荔波县人民政府",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld_5981819/202503/t20250326_87280300.html",
    },
    {
        "id": 14,
        "name": "袁学玉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县人民政府副县长",
        "current_org": "荔波县人民政府",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld_5981819/202503/t20250326_87280299.html",
    },
    {
        "id": 15,
        "name": "王燕隆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县人民政府副县长",
        "current_org": "荔波县人民政府",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld_5981819/202503/t20250326_87280298.html",
    },
    {
        "id": 16,
        "name": "金安贵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县人民政府副县长，县公安局党委书记、局长、督察长，县委政法委员会委员",
        "current_org": "荔波县人民政府 / 荔波县公安局",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld_5981819/202604/t20260430_90090179.html",
    },
    # ── 县人大领导 ──
    {
        "id": 17,
        "name": "向宗洋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县人大常委会党组书记、主任",
        "current_org": "荔波县人民代表大会常务委员会",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xrdld/202605/t20260519_90190290.html",
    },
    # ── 县政协领导 ──
    {
        "id": 18,
        "name": "吴化明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荔波县政协党组副书记、副主席",
        "current_org": "中国人民政治协商会议荔波县委员会",
        "source": "https://www.libo.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzxld/202605/t20260519_90190270.html",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共荔波县委员会",
        "type": "党委",
        "level": "县",
        "location": "贵州省黔南布依族苗族自治州荔波县",
    },
    {
        "id": 2,
        "name": "荔波县人民政府",
        "type": "政府",
        "level": "县",
        "location": "贵州省黔南布依族苗族自治州荔波县",
    },
    {
        "id": 3,
        "name": "中共荔波县纪律检查委员会",
        "type": "纪律检查",
        "level": "县",
        "location": "贵州省黔南布依族苗族自治州荔波县",
    },
    {
        "id": 4,
        "name": "荔波县监察委员会",
        "type": "监察",
        "level": "县",
        "location": "贵州省黔南布依族苗族自治州荔波县",
    },
    {
        "id": 5,
        "name": "荔波县公安局",
        "type": "政府",
        "level": "县",
        "location": "贵州省黔南布依族苗族自治州荔波县",
    },
    {
        "id": 6,
        "name": "荔波樟江风景名胜区管理处",
        "type": "事业单位",
        "level": "县",
        "location": "贵州省黔南布依族苗族自治州荔波县",
    },
    {
        "id": 7,
        "name": "荔波县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "location": "贵州省黔南布依族苗族自治州荔波县",
    },
    {
        "id": 8,
        "name": "中国人民政治协商会议荔波县委员会",
        "type": "政协",
        "level": "县",
        "location": "贵州省黔南布依族苗族自治州荔波县",
    },
]

POSITIONS = [
    # 余登利 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "荔波县委书记", "start": "", "end": "present", "rank": "正县", "note": ""},
    # 马登宏 - 县长
    {"person_id": 2, "org_id": 1, "title": "荔波县委副书记", "start": "", "end": "present", "rank": "副县", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "荔波县人民政府县长", "start": "", "end": "present", "rank": "正县", "note": ""},
    # 曾松林
    {"person_id": 3, "org_id": 1, "title": "荔波县委副书记、县委政法委书记", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 彭佐扬（挂职）
    {"person_id": 4, "org_id": 1, "title": "荔波县委副书记（挂职）", "start": "", "end": "present", "rank": "副县", "note": "挂职"},
    # 谢义鹏
    {"person_id": 5, "org_id": 1, "title": "荔波县委常委", "start": "", "end": "present", "rank": "副县", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "荔波县人民政府常务副县长", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 龙怀
    {"person_id": 6, "org_id": 1, "title": "荔波县委常委、统战部部长", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 娄钧
    {"person_id": 7, "org_id": 1, "title": "荔波县委常委、县纪委书记", "start": "", "end": "present", "rank": "副县", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "荔波县监委主任", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 颜东梅
    {"person_id": 8, "org_id": 1, "title": "荔波县委常委、组织部部长", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 胡晴
    {"person_id": 9, "org_id": 1, "title": "荔波县委常委、县委办公室主任", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 瞿双
    {"person_id": 10, "org_id": 1, "title": "荔波县委常委、宣传部部长", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 李仕富
    {"person_id": 11, "org_id": 1, "title": "荔波县委常委", "start": "", "end": "present", "rank": "副县", "note": "提名副县长"},
    {"person_id": 11, "org_id": 2, "title": "荔波县人民政府副县长（提名）", "start": "", "end": "present", "rank": "副县", "note": "提名"},
    {"person_id": 11, "org_id": 6, "title": "荔波樟江风景名胜区管理处党组书记", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 吕建军（挂职）
    {"person_id": 12, "org_id": 1, "title": "荔波县委常委", "start": "", "end": "present", "rank": "副县", "note": "挂职"},
    {"person_id": 12, "org_id": 2, "title": "荔波县人民政府副县长（挂职）", "start": "", "end": "present", "rank": "副县", "note": "挂职"},
    # 卢小泉
    {"person_id": 13, "org_id": 2, "title": "荔波县人民政府副县长", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 袁学玉
    {"person_id": 14, "org_id": 2, "title": "荔波县人民政府副县长", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 王燕隆
    {"person_id": 15, "org_id": 2, "title": "荔波县人民政府副县长", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 金安贵
    {"person_id": 16, "org_id": 2, "title": "荔波县人民政府副县长", "start": "", "end": "present", "rank": "副县", "note": ""},
    {"person_id": 16, "org_id": 5, "title": "荔波县公安局局长、督察长", "start": "", "end": "present", "rank": "副县", "note": ""},
    # 向宗洋
    {"person_id": 17, "org_id": 7, "title": "荔波县人大常委会主任", "start": "", "end": "present", "rank": "正县", "note": ""},
    # 吴化明
    {"person_id": 18, "org_id": 8, "title": "荔波县政协副主席", "start": "", "end": "present", "rank": "副县", "note": ""},
]

RELATIONSHIPS = [
    # 余登利 ↔ 马登宏 (书记-县长搭档)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭档",
        "overlap_org": "中共荔波县委员会",
        "overlap_period": "unknown~present",
    },
    # 余登利 ↔ 曾松林 (书记-专职副书记)
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与专职副书记",
        "overlap_org": "中共荔波县委员会",
        "overlap_period": "unknown~present",
    },
    # 马登宏 ↔ 谢义鹏 (县长-常务副县长)
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县长与常务副县长",
        "overlap_org": "荔波县人民政府",
        "overlap_period": "unknown~present",
    },
    # 曾松林 ↔ 颜东梅 (政法-组织交叉)
    {
        "person_a": 3,
        "person_b": 8,
        "type": "overlap",
        "context": "县委副书记与组织部部长协同工作",
        "overlap_org": "中共荔波县委员会",
        "overlap_period": "unknown~present",
    },
    # 颜东梅 ↔ 娄钧 (组织-纪委)
    {
        "person_a": 8,
        "person_b": 7,
        "type": "overlap",
        "context": "组织部与纪委协作（干部监督）",
        "overlap_org": "中共荔波县委员会",
        "overlap_period": "unknown~present",
    },
    # 谢义鹏 ↔ 金安贵 (常务-公安)
    {
        "person_a": 5,
        "person_b": 16,
        "type": "overlap",
        "context": "常务副县长与公安局长工作关系",
        "overlap_org": "荔波县人民政府",
        "overlap_period": "unknown~present",
    },
    # 胡晴 ↔ 余登利 (办公室主任-书记)
    {
        "person_a": 9,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "县委办公室主任直接服务县委书记",
        "overlap_org": "中共荔波县委员会",
        "overlap_period": "unknown~present",
    },
    # 瞿双 ↔ 颜东梅 (宣传-教育-组织交叉)
    {
        "person_a": 10,
        "person_b": 8,
        "type": "overlap",
        "context": "宣传部部长与组织部部长同为县委常委",
        "overlap_org": "中共荔波县委员会",
        "overlap_period": "unknown~present",
    },
    # 龙怀 ↔ 娄钧 (统战-纪委交叉)
    {
        "person_a": 6,
        "person_b": 7,
        "type": "overlap",
        "context": "统战部部长与纪委书记同为县委常委",
        "overlap_org": "中共荔波县委员会",
        "overlap_period": "unknown~present",
    },
    # 马登宏 ↔ 卢小泉 (县长-副县长)
    {
        "person_a": 2,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "荔波县人民政府",
        "overlap_period": "unknown~present",
    },
    # 马登宏 ↔ 袁学玉 (县长-副县长)
    {
        "person_a": 2,
        "person_b": 14,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "荔波县人民政府",
        "overlap_period": "unknown~present",
    },
    # 马登宏 ↔ 王燕隆 (县长-副县长)
    {
        "person_a": 2,
        "person_b": 15,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "荔波县人民政府",
        "overlap_period": "unknown~present",
    },
]

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

DB_PATH = Path("data/tmp/guizhou_荔波县/荔波县_network.db")
GEXF_PATH = Path("data/tmp/guizhou_荔波县/荔波县_network.gexf")

if __name__ == "__main__":
    run_build(
        slug="荔波县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
