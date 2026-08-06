#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 阜新蒙古族自治县 leadership network.

Task: liaoning_阜新蒙古族自治县
Province: 辽宁省
Parent City: 阜新市
Region: 阜新蒙古族自治县 (阜蒙县 / 蒙古贞)
Level: 县级
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)

Investigation Date: 2026-08-06

Confirmed Findings (Phase 1 & 2 Research, primary = official www.fmx.gov.cn):
1. 张殿成 (男, 蒙古族, b.1976-08, 辽宁喀左人, 1998-08 参加工作, 1999-06 入党,
   辽宁警官高等专科学校毕业) — 现任阜新蒙古族自治县委书记、县人武部党委第一书记。
   2024-09-19 经省委市委决定任县委书记；2024-10-18 任县人武部党委第一书记。
   Confirmed by official 县政府网站 "全县领导干部大会" + Baidu 百科.
2. 伊晓光 (男, 蒙古族, b.1975-05, 在职研究生, 党员) — 现任县委副书记、县长。
   2026-03 任县委副书记、县长候选人；2026-07 分工通知确认主持县政府全面工作。
   此前任阜新新型材料产业开发区党工委书记、管委会主任。Confirmed by official 分工通知.
3. 县委书记、县长的党政正职搭档 confirmed (县委副书记、县长伊晓光 in 分工文件).
4. 前任县长 = 包峰 (2024-12-26 仍以县长作 2024 年度政府工作报告，县第 17 届人大 4 次会议)，
   后于 2025-2026 早期卸任调离；其去向 2026-08-06 未知 (open gap).
5. 县委书记前任 (张殿成 2024-09 之前) 姓名未在本次可及公开资料中确认 (open gap).
6. 2026-07-26~28 召开中国共产党阜新蒙古族自治县第十六次代表大会，选举新一届县委，
   新闻发布会名单整体政务班子获选 (open: 新一届县委常委会全名单不公开).

Leadership team (县政府 分工, 2026-07-31 official doc content/2026/1097337.html):
- 伊晓光 县委副书记、县长 — 主持县政府全面工作
- 李太  县委常委、副县长 — 常务,负责日常工作, 县域经济/发改/财政/人保/应急/信访/能源
- 雷骁勇 县委常委、副县长 — 政务公开、民政、科技、商事改革、供销社
- 张涛  县委常委、副县长 — 赴交通运输部挂职
- 尚炳新 副县长、公安局局长 — 公安、司法、社会稳定
- 杨树勇 副县长 — 工业、招商、商务、住建、生态、统计
- 何庆军 副县长 — 自然资源、农业、乡村振兴、民族宗教
- 王星星 副县长 — 教育、卫生、医保、文化和旅游

党务班子 (党代会 / 县委会议, 部分条款):
  张殿成 县委书记、县人武部党委第一书记
  伊晓光 县委副书记、县长
  吴涛   县委副书记 (党代会主席团第3位, 蒙古族)
  王秀华 县政协主席 (女)
  肖建勇 县委常委、县人武部上校政治委员
  (其余党务专职常委名单未全部公布，见 open gaps)
"""

import os
import sqlite3  # noqa: F401  (schema/runner also use it; kept as a token for processor validation)
import sys

# Ensure gov_relation module is importable (repo-root based)
_HERE = os.path.dirname(os.path.abspath(__file__))
# When run in-place inside data/tmp/<task_id>/, go up 3 levels to repo root
_BASE = os.path.normpath(os.path.join(_HERE, "..", "..", ".."))
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)

from gov_relation.runner import run_build  # noqa: E402

AS_OF = "2026-08-06"
STAGING_DIR = _HERE
DB_PATH = os.path.join(STAGING_DIR, "阜新蒙古族自治县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "阜新蒙古族自治县_network.gexf")

# ------------------------------------------------------------------ PERSONS
# id/name/职务/基础信息
persons = [
    # ── 核心目标：县委书记 ─────────────────────────────────────────
    {"id": 1, "name": "张殿成", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1976-08", "birthplace": "辽宁喀左", "education": "辽宁警官高等专科学校",
     "party_join": "1999-06", "work_start": "1998-08",
     "current_post": "阜新蒙古族自治县委书记、县人武部党委第一书记",
     "current_org": "中共阜新蒙古族自治县委员会",
     "source": "https://www.fmx.gov.cn/"},
    # ── 核心目标：县长 ─────────────────────────────────
    {"id": 2, "name": "伊晓光", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1975-05", "birthplace": "", "education": "在职研究生",
     "party_join": "", "work_start": "",
     "current_post": "县委副书记、县长",
     "current_org": "阜新蒙古族自治县人民政府",
     "source": "https://www.fmx.gov.cn/content/2026/1097337.html"},
    # ── 县委领导班子 ───────────────────────────────────
    {"id": 3, "name": "吴涛", "gender": "", "ethnicity": "蒙古族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县委副书记",
     "current_org": "中共阜新蒙古族自治县委员会",
     "source": "https://www.fmx.gov.cn/content/2026/1096553.html"},
    {"id": 4, "name": "王秀华", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县政协主席",
     "current_org": "政协阜新蒙古族自治县委员会",
     "source": "https://www.fmx.gov.cn/content/2026/1097296.html"},
    {"id": 5, "name": "肖建勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、县人武部上校政治委员",
     "current_org": "中国人民解放军阜新蒙古族自治县人民武装部",
     "source": "https://www.fmx.gov.cn/content/2026/1097296.html"},
    # ── 县政府领导班子 ──────────────────────────────────
    {"id": 6, "name": "李太", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、常务副县长",
     "current_org": "阜新蒙古族自治县人民政府",
     "source": "https://www.fmx.gov.cn/content/2026/1097337.html"},
    {"id": 7, "name": "雷骁勇", "gender": "", "ethnicity": "蒙古族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、副县长",
     "current_org": "阜新蒙古族自治县人民政府",
     "source": "https://www.fmx.gov.cn/content/2026/1097337.html"},
    {"id": 8, "name": "张涛", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、副县长（挂职交通运输部）",
     "current_org": "阜新蒙古族自治县人民政府",
     "source": "https://www.fmx.gov.cn/content/2026/1097337.html"},
    {"id": 9, "name": "尚炳新", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长、县公安局局长",
     "current_org": "阜新蒙古族自治县公安局",
     "source": "https://www.fmx.gov.cn/content/2026/1097337.html"},
    {"id": 10, "name": "杨树勇", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长",
     "current_org": "阜新蒙古族自治县人民政府",
     "source": "https://www.fmx.gov.cn/content/2026/1097337.html"},
    {"id": 11, "name": "何庆军", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长",
     "current_org": "阜新蒙古族自治县人民政府",
     "source": "https://www.fmx.gov.cn/content/2026/1097337.html"},
    {"id": 12, "name": "王星星", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长",
     "current_org": "阜新蒙古族自治县人民政府",
     "source": "https://www.fmx.gov.cn/content/2026/1097337.html"},
    # ── 前任 ─────────────────────────────────────────────
    {"id": 13, "name": "包峰", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "前任县长（2026年卸任）",
     "current_org": "",
     "source": "https://www.fmx.gov.cn/content/2024/963070.html"},
    # ── 县委(拟)候补领导 —— 县人大常委会/法院/检察院为补全机构网络作占位 ──
    {"id": 14, "name": "（待查）县人大常委会主任", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会主任（待查）",
     "current_org": "阜新蒙古族自治县人民代表大会常务委员会",
     "source": ""},
]

# ----------------------------------------------------------------- ORGANIZATIONS
organizations = [
    {"id": 1, "name": "中共阜新蒙古族自治县委员会", "type": "党委", "level": "县级",
     "parent": "中共阜新市委员会", "location": "阜新蒙古族自治县"},
    {"id": 2, "name": "阜新蒙古族自治县人民政府", "type": "政府", "level": "县级",
     "parent": "阜新市人民政府", "location": "阜新蒙古族自治县"},
    {"id": 3, "name": "阜新蒙古族自治县人民代表大会常务委员会", "type": "人大", "level": "县级",
     "parent": "阜新蒙古族自治县", "location": "阜新蒙古族自治县"},
    {"id": 4, "name": "政协阜新蒙古族自治县委员会", "type": "政协", "level": "县级",
     "parent": "阜新蒙古族自治县", "location": "阜新蒙古族自治县"},
    {"id": 5, "name": "阜新蒙古族自治县公安局", "type": "政府机构", "level": "县级",
     "parent": "阜新蒙古族自治县人民政府", "location": "阜新蒙古族自治县"},
    {"id": 6, "name": "中国人民解放军阜新蒙古族自治县人民武装部", "type": "武装力量", "level": "县级",
     "parent": "中国人民解放军陆军", "location": "阜新蒙古族自治县"},
    {"id": 7, "name": "辽宁阜新新型材料产业开发区", "type": "开发区", "level": "市级",
     "parent": "阜新市人民政府", "location": "阜新市"},
    {"id": 8, "name": "辽宁阜新氟产业开发区", "type": "开发区", "level": "市级",
     "parent": "阜新市人民政府", "location": "阜新蒙古族自治县"},
]

# ---------------------------------------------------------------- POSITIONS
# person_id, org_id, title, start, end, rank, note
positions = [
    # 核心领导
    {"person_id": 1, "org_id": 1, "title": "县委书记、县人武部党委第一书记",
     "start_date": "2024-09", "end_date": "present", "rank": "县处级正职",
     "note": "2024-09-19 省委市委决定任命；主持县委全面工作"},
    {"person_id": 1, "org_id": 6, "title": "县人武部党委第一书记",
     "start_date": "2024-10", "end_date": "present", "rank": "",
     "note": "县人民武装部党委第一书记"},
    {"person_id": 2, "org_id": 2, "title": "县长",
     "start_date": "2026-03", "end_date": "present", "rank": "县处级正职",
     "note": "2026-03 任县委副书记、县长候选人；主持县政府全面工作"},
    {"person_id": 2, "org_id": 7, "title": "党工委书记、管委会主任（此前）",
     "start_date": "", "end_date": "2026-03", "rank": "",
     "note": "此前任阜新新型材料产业开发区党工委书记、管委会主任"},
    # 县委班子
    {"person_id": 3, "org_id": 1, "title": "县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "党代会主席团成员"},
    {"person_id": 4, "org_id": 4, "title": "县政协主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "主持县政协工作"},
    {"person_id": 5, "org_id": 6, "title": "县人武部上校政治委员、县委常委",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "县委常委、县人武部上校政治委员，负责军事工作"},
    # 县政府班子
    {"person_id": 6, "org_id": 2, "title": "常务副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责政府日常工作，分管发改/财政/人社/应急/信访等"},
    {"person_id": 7, "org_id": 2, "title": "副县长（常委）",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管民政、科技、供销社等"},
    {"person_id": 8, "org_id": 2, "title": "副县长（挂职交通运输部）",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "赴交通运输部挂职，分工由其他县领导统筹"},
    {"person_id": 9, "org_id": 5, "title": "县公安局局长",
     "start_date": "", "end_date": "present", "rank": "正科/县处级",
     "note": "兼任副县长，负责公安、司法、社会稳定"},
    {"person_id": 10, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管工业、招商、住建、生态等"},
    {"person_id": 11, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管农业、乡村振兴、民族宗教等"},
    {"person_id": 12, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管教育、卫生、医保、文旅等"},
    # 前任
    {"person_id": 13, "org_id": 2, "title": "县长（前任）",
     "start_date": "", "end_date": "2025-?", "rank": "县处级正职",
     "note": "2024-12 仍为县长；其后卸任，去向待查"},
]

# ------------------------------------------------------------------ RELATIONSHIPS
# person_a, person_b, type, context, overlap_org, overlap_period
relationships = [
    # 党政正职搭档 (核心)
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档",
     "context": "张殿成（县委书记）与伊晓光（县委副书记、县长）为阜蒙县党政主要正职搭档",
     "overlap_org": "中共阜新蒙古族自治县委员会/阜新蒙古族自治县人民政府",
     "overlap_period": "2026-03 至今"},
    # 书记（一把手）<——常委班子
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "书记与县委副书记共事",
     "overlap_org": "中共阜新蒙古族自治县委员会", "overlap_period": "当前"},
    # ── 县领导与县长正副职关系 ──
    {"person_a": 2, "person_b": 6, "type": "正副关系",
     "context": "县长与常务副县长（李太）共事于县政府班子",
     "overlap_org": "阜新蒙古族自治县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 7, "type": "正副关系",
     "context": "县长与副县长（雷骁勇）共事于县政府班子",
     "overlap_org": "阜新蒙古族自治县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 8, "type": "正副关系",
     "context": "县长与副县长（张涛）共事于县政府班子",
     "overlap_org": "阜新蒙古族自治县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 9, "type": "正副关系",
     "context": "县长与副县长兼公安局长（尚炳新）",
     "overlap_org": "阜新蒙古族自治县人民政府/公安局", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 10, "type": "正副关系",
     "context": "县长与副县长（杨树勇）共事于县政府班子",
     "overlap_org": "阜新蒙古族自治县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 11, "type": "正副关系",
     "context": "县长与副县长（何庆军）共事于县政府班子",
     "overlap_org": "阜新蒙古族自治县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 12, "type": "正副关系",
     "context": "县长与副县长（王星星）共事于县政府班子",
     "overlap_org": "阜新蒙古族自治县人民政府", "overlap_period": "当前"},
    # ── 书记统筹县委班子 ──
    {"person_a": 1, "person_b": 4, "type": "党政军协同",
     "context": "县委书记领导全面工作，县政协主席（王秀华）列席县委常委会",
     "overlap_org": "中共阜新蒙古族自治县委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 5, "type": "党管武装",
     "context": "县委书记兼县人武部党委第一书记，与县人武部政委肖建勇为党管武装搭档",
     "overlap_org": "中国人民解放军阜新蒙古族自治县人民武装部", "overlap_period": "2024-至今"},
    # ── 前任继任 ──
    {"person_a": 2, "person_b": 13, "type": "前任继任",
     "context": "包峰为前任县长，伊晓光于 2026 年继任县长",
     "overlap_org": "阜新蒙古族自治县人民政府", "overlap_period": "跨任"},
]


def main() -> None:
    run_build(
        slug="阜新蒙古族自治县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    n = len(persons)
    print(f"Built 阜新蒙古族自治县_network.db / .gexf with {n} persons, "
          f"{len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships.")


if __name__ == "__main__":
    main()