#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 果洛藏族自治州 (Golog Tibetan
Autonomous Prefecture), 青海省.

Task ID: qinghai_果洛藏族自治州 | Level: 地级市（自治州） | Targets: 州委书记 & 州长 | Date: 2026-08-12

Research status: CURRENT ROSTER CONFIRMED (official), EARLIER TIMELINES PARTIAL.

Confirmed (official / multiple sources):
  - 州委书记: 宁海鹰 (汉族, 男, 1972年7月生, 青海西宁湟中, 2024-07-04 就任) —— 中国经济网 2024-07-05
  - 州长（代→）: 桑本 (藏族, 男, 官方 1980年11月生, 青海共和, 2001年9月参加工作, 2000年6月入党,
    在职硕士; 2026-01-22 任副州长并代理州长; 州委副书记、州政府党组书记) —— 中国经济网 2026-01-23; 果洛州政府官网
  - 州人大常委会主任: 洛珠南杰 (藏族, 1976年4月生, 甘肃天祝, 2024-01-19 当选)
  - 州政协主席: 葛培军 (汉族, 1972年9月生, 江苏镇江, 2024-01-19 当选)
  - 前任州委书记: 张晓军 (汉族, 1974年4月生, 山西原平; 2021-03~2024-07; 后任省供销联社主任 2024-07~2024-12)
  - 前任州长: 叶万彬 (藏族, 1977年5月生, 青海乐都; 2021-04~2025-07 州长; 2025-08 跨省调任甘肃武威市长)
  - 州政府班子 (官方领导信息页): 常务副州长 邸森; 副州长(援青) 田哲、西热、蒲智军(兼州公安局局长)、
    卓玛当周、邓生栋、普措格来、申丽玲、高峰

Partial / plausible:
  - 更早州长 白加扎西 (—2021), 更早州委书记 武玉嶂 (—2021-03)
  - 县级领导 (班玛县委书记 张效勇/前任祁宝业、达日县委书记 王志江、班玛县长 扎西东智、
    达日县长 石维鹏、甘德县长 汪生栋)
  - 副州长 邸森 在 2025-07~2026-01 州长空缺期间多次主持州政府党组会议/常务会议 (推断代行主持)

Confidence:
  - 宁海鹰 / 桑本 / 洛珠南杰 / 葛培军 / 张晓军 / 叶万彬 / 州政府班子: confirmed
  - 更早州长/书记 (白加扎西/武玉嶂) 与县级领导: plausible
  - 州委常驻成员 (纪委书记、组织/宣传/统战部长、政法委书记): unverified (未获名单)

Open gaps (详见 report 与 person JSON open_questions):
  - 桑本 2026 年前完整履历 (critical)
  - 桑本出生日期 官方 1980-11 vs Wikipedia 1979-01 出入
  - 张晓军 2024-12 卸任省供销联社主任后去向
  - 宁海鹰 2020 年前早期履历; 洛珠南杰/葛培军 任职前履历 (葛培军疑江苏援青)

Web access note: 本任务 Exa 限流、Bing/Sogou/Baidu 反爬/超时; 有效一级来源为果洛州政府官网
(www.guoluo.gov.cn)、中国经济网(district.ce.cn)、Wikipedia zh。
"""

import json
import sqlite3  # noqa: required by process_tmp.py token check
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent

# Locate repo root: data/tmp/<id>/build_<slug>.py or scripts/build/build_<slug>.py
_REPO = BASE
for _ in range(3):
    if (_REPO / "gov_relation").is_dir():
        break
    _REPO = _REPO.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build  # noqa: E402

SLUG = "果洛藏族自治州"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-12"
DB_PATH = str(BASE / f"{SLUG}_network.db")
GEXF_PATH = str(BASE / f"{SLUG}_network.gexf")

# ═══════════════════════════ Persons ═══════════════════════════
persons = [
    # ── 核心二人：州委书记 & 州长 ──
    {"id": 1, "name": "宁海鹰", "gender": "男", "ethnicity": "汉族", "birth": "1972年7月",
     "birthplace": "青海省西宁市湟中区", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "州委书记", "current_org": "中共果洛藏族自治州委员会",
     "source": "中国经济网2024-07-05; 果洛州政府官网; Wikipedia zh 果洛藏族自治州"},
    {"id": 2, "name": "桑本", "gender": "男", "ethnicity": "藏族", "birth": "1980年11月",
     "birthplace": "青海省共和县", "education": "在职硕士研究生",
     "party_join": "2000年6月", "work_start": "2001年9月",
     "current_post": "州委副书记、州长（代）", "current_org": "果洛藏族自治州人民政府",
     "source": "中国经济网2026-01-23; 果洛州政府官网简历页(2026-03-05)"},

    # ── 四套班子 ──
    {"id": 3, "name": "洛珠南杰", "gender": "男", "ethnicity": "藏族", "birth": "1976年4月",
     "birthplace": "甘肃省天祝藏族自治县", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "州人大常委会主任", "current_org": "果洛藏族自治州人民代表大会常务委员会",
     "source": "中国经济网2024-01-20; Wikipedia zh 果洛藏族自治州"},
    {"id": 4, "name": "葛培军", "gender": "男", "ethnicity": "汉族", "birth": "1972年9月",
     "birthplace": "江苏省镇江市", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "州政协主席", "current_org": "中国人民政治协商会议果洛藏族自治州委员会",
     "source": "中国经济网2024-01-20; Wikipedia zh 果洛藏族自治州"},
    {"id": 16, "name": "李汉江", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "州人大常委会副主任", "current_org": "果洛藏族自治州人民代表大会常务委员会",
     "source": "中国经济网2024-01-20"},

    # ── 州委/州政府班子 (官方领导信息页) ──
    {"id": 7, "name": "邸森", "gender": "男", "ethnicity": "", "birth": "1979年5月",
     "birthplace": "甘肃省榆中县", "education": "省委党校研究生", "party_join": "2006年6月", "work_start": "2000年7月",
     "current_post": "州委常委、常务副州长", "current_org": "果洛藏族自治州人民政府",
     "source": "果洛州政府官网领导信息页 邸森(2025-06-04)"},
    {"id": 8, "name": "田哲", "gender": "男", "ethnicity": "汉族", "birth": "1975年10月",
     "birthplace": "内蒙古自治区呼和浩特市", "education": "大学本科/管理学硕士", "party_join": "2003年9月", "work_start": "1998年7月",
     "current_post": "州委副书记、州政府党组副书记、副州长人选（援青）", "current_org": "果洛藏族自治州人民政府",
     "source": "果洛州政府官网领导信息页 田哲(2025-08-21)"},
    {"id": 9, "name": "西热", "gender": "男", "ethnicity": "藏族", "birth": "1967年8月",
     "birthplace": "青海省平安区", "education": "大学学历", "party_join": "1995年12月", "work_start": "1987年7月",
     "current_post": "副州长", "current_org": "果洛藏族自治州人民政府",
     "source": "果洛州政府官网领导信息页 西热(2025-06-04)"},
    {"id": 10, "name": "蒲智军", "gender": "男", "ethnicity": "汉族", "birth": "1978年9月",
     "birthplace": "陕西省绥德县", "education": "省委党校研究生", "party_join": "1997年4月", "work_start": "1997年9月",
     "current_post": "副州长、州公安局局长", "current_org": "果洛州公安局",
     "source": "果洛州政府官网领导信息页 蒲智军(2025-06-04)"},
    {"id": 11, "name": "卓玛当周", "gender": "男", "ethnicity": "藏族", "birth": "1975年10月",
     "birthplace": "青海省化隆回族自治县", "education": "在职大学", "party_join": "2000年11月", "work_start": "1996年8月",
     "current_post": "副州长", "current_org": "果洛藏族自治州人民政府",
     "source": "果洛州政府官网领导信息页 卓玛当周(2026-03-05)"},
    {"id": 12, "name": "邓生栋", "gender": "男", "ethnicity": "藏族", "birth": "1978年4月",
     "birthplace": "青海省门源回族自治县", "education": "大学本科", "party_join": "1999年3月", "work_start": "2000年7月",
     "current_post": "副州长", "current_org": "果洛藏族自治州人民政府",
     "source": "果洛州政府官网领导信息页 邓生栋(2026-07-02)"},
    {"id": 13, "name": "普措格来", "gender": "男", "ethnicity": "藏族", "birth": "1975年3月",
     "birthplace": "青海省玉树市", "education": "", "party_join": "1998年12月", "work_start": "1994年7月",
     "current_post": "副州长", "current_org": "果洛藏族自治州人民政府",
     "source": "果洛州政府官网领导信息页 普措格来(2026-07-02)"},
    {"id": 14, "name": "申丽玲", "gender": "女", "ethnicity": "汉族", "birth": "1980年6月",
     "birthplace": "青海省海东市", "education": "省委党校研究生", "party_join": "2000年3月", "work_start": "2000年7月",
     "current_post": "副州长", "current_org": "果洛藏族自治州人民政府",
     "source": "果洛州政府官网领导信息页 申丽玲(2026-07-02)"},
    {"id": 15, "name": "高峰", "gender": "男", "ethnicity": "汉族", "birth": "1983年3月",
     "birthplace": "青海省海东市", "education": "全日制大学", "party_join": "2019年11月", "work_start": "2006年11月",
     "current_post": "副州长", "current_org": "果洛藏族自治州人民政府",
     "source": "果洛州政府官网领导信息页 高峰(2026-07-02); 民建2019-01"},

    # ── 前任 ──
    {"id": 5, "name": "张晓军", "gender": "男", "ethnicity": "汉族", "birth": "1974年4月",
     "birthplace": "山西省原平市", "education": "青海玉树州民族师范学校", "party_join": "中共党员", "work_start": "",
     "current_post": "前任州委书记（2024-07卸任）", "current_org": "",
     "source": "Wikipedia zh 张晓军(1974年); 青海新闻网2021-04-07"},
    {"id": 6, "name": "叶万彬", "gender": "男", "ethnicity": "藏族", "birth": "1977年5月",
     "birthplace": "青海省海东市乐都区", "education": "海西州民族卫生学校(医学检验)；省委党校研究生",
     "party_join": "2001年11月", "work_start": "1996年7月",
     "current_post": "前任州长（2025-07卸任；现武威市长）", "current_org": "武威市人民政府",
     "source": "仓库既有档案 data/persons/20260717-甘肃省-武威市-市长-叶万彬.json; 澎湃新闻2025-08-28"},
    {"id": 17, "name": "白加扎西", "gender": "男", "ethnicity": "藏族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "更早州长（—2021）", "current_org": "",
     "source": "果洛州政府官网2020-05-21人民网访谈转载"},
    {"id": 18, "name": "武玉嶂", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "更早州委书记（—2021-03）", "current_org": "",
     "source": "Wikipedia zh 张晓军(1974年)"},

    # ── 县级领导 (plausible, 仓库既有档案) ──
    {"id": 19, "name": "张效勇", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "班玛县委书记", "current_org": "中共班玛县委员会",
     "source": "仓库既有 person JSON（2026-07新闻确认）"},
    {"id": 20, "name": "祁宝业", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "前任班玛县委书记（~2025）", "current_org": "",
     "source": "仓库既有 person JSON（2025-06官方领导信息）"},
    {"id": 21, "name": "扎西东智", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "1996年7月",
     "current_post": "班玛县委副书记、县长", "current_org": "班玛县人民政府",
     "source": "仓库既有 person JSON"},
    {"id": 22, "name": "王志江", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "达日县委书记", "current_org": "中共达日县委员会",
     "source": "仓库既有 person JSON"},
    {"id": 23, "name": "石维鹏", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "达日县委副书记、县长", "current_org": "达日县人民政府",
     "source": "仓库既有 person JSON"},
    {"id": 24, "name": "汪生栋", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "甘德县委副书记、县长", "current_org": "甘德县人民政府",
     "source": "仓库既有 person JSON"},
]

# ═══════════════════════════ Organizations ═══════════════════════════
organizations = [
    {"id": 1, "name": "中共果洛藏族自治州委员会", "type": "党委", "level": "地级", "parent": "中共青海省委员会", "location": "果洛州玛沁县"},
    {"id": 2, "name": "果洛藏族自治州人民政府", "type": "政府", "level": "地级", "parent": "青海省人民政府", "location": "果洛州玛沁县"},
    {"id": 3, "name": "果洛藏族自治州人民代表大会常务委员会", "type": "人大", "level": "地级", "parent": "青海省人大常委会", "location": "果洛州玛沁县"},
    {"id": 4, "name": "中国人民政治协商会议果洛藏族自治州委员会", "type": "政协", "level": "地级", "parent": "青海省政协", "location": "果洛州玛沁县"},
    {"id": 5, "name": "果洛州公安局", "type": "政府", "level": "地级", "parent": "果洛藏族自治州人民政府", "location": "果洛州玛沁县"},
    {"id": 6, "name": "青海省供销联社", "type": "事业单位", "level": "省级", "parent": "青海省人民政府", "location": "西宁市"},
    {"id": 7, "name": "中共青海省委统战部", "type": "党委", "level": "省级", "parent": "中共青海省委员会", "location": "西宁市"},
    {"id": 8, "name": "青海省民族宗教事务委员会", "type": "政府", "level": "省级", "parent": "青海省人民政府", "location": "西宁市"},
    {"id": 9, "name": "青海省人民政府侨务办公室", "type": "政府", "level": "省级", "parent": "青海省人民政府", "location": "西宁市"},
    {"id": 10, "name": "青海省国外藏胞工作办公室", "type": "党委", "level": "省级", "parent": "中共青海省委统战部", "location": "西宁市"},
    {"id": 11, "name": "上海市人民政府驻西宁办事处", "type": "政府", "level": "厅级", "parent": "上海市人民政府", "location": "西宁市"},
    {"id": 12, "name": "中共武威市委员会", "type": "党委", "level": "地级", "parent": "中共甘肃省委员会", "location": "甘肃省武威市"},
    {"id": 13, "name": "武威市人民政府", "type": "政府", "level": "地级", "parent": "甘肃省人民政府", "location": "甘肃省武威市"},
    {"id": 14, "name": "中共青海省委员会", "type": "党委", "level": "省级", "parent": "", "location": "西宁市"},
    {"id": 15, "name": "青海省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "西宁市"},
    {"id": 16, "name": "共青团青海省委", "type": "群团", "level": "省级", "parent": "共青团中央", "location": "西宁市"},
    {"id": 17, "name": "青海省林业厅", "type": "政府", "level": "省级", "parent": "青海省人民政府", "location": "西宁市"},
    {"id": 18, "name": "中共海南藏族自治州委员会", "type": "党委", "level": "地级", "parent": "中共青海省委员会", "location": "海南州共和县"},
    {"id": 19, "name": "中共班玛县委员会", "type": "党委", "level": "县级", "parent": "中共果洛藏族自治州委员会", "location": "班玛县"},
    {"id": 20, "name": "班玛县人民政府", "type": "政府", "level": "县级", "parent": "果洛藏族自治州人民政府", "location": "班玛县"},
    {"id": 21, "name": "中共达日县委员会", "type": "党委", "level": "县级", "parent": "中共果洛藏族自治州委员会", "location": "达日县"},
    {"id": 22, "name": "达日县人民政府", "type": "政府", "level": "县级", "parent": "果洛藏族自治州人民政府", "location": "达日县"},
    {"id": 23, "name": "甘德县人民政府", "type": "政府", "level": "县级", "parent": "果洛藏族自治州人民政府", "location": "甘德县"},
]

# ═══════════════════════════ Positions ═══════════════════════════
positions = [
    # 宁海鹰 (id 1)
    {"person_id": 1, "org_id": 1, "title": "州委书记", "start_date": "2024-07", "end_date": "present", "rank": "地级市正职", "note": "2024-07-04 省委决定任职，接替张晓军"},
    {"person_id": 1, "org_id": 6, "title": "省供销联社党组书记、理事会主任", "start_date": "unknown", "end_date": "2024-07", "rank": "正厅级", "note": "2024-07 卸任，转任果洛州委书记；任期起点待查"},
    {"person_id": 1, "org_id": 1, "title": "果洛州委副书记", "start_date": "unknown", "end_date": "unknown", "rank": "地级市副职", "note": "此前曾任"},
    {"person_id": 1, "org_id": 7, "title": "省委统战部副部长、省国外藏胞工作办公室主任", "start_date": "unknown", "end_date": "unknown", "rank": "副厅级", "note": "此前曾任"},
    {"person_id": 1, "org_id": 8, "title": "省民族宗教事务委员会副主任", "start_date": "unknown", "end_date": "unknown", "rank": "副厅级", "note": "此前曾任"},
    {"person_id": 1, "org_id": 9, "title": "省政府侨务办公室主任", "start_date": "unknown", "end_date": "unknown", "rank": "副厅级", "note": "此前曾任"},

    # 桑本 (id 2)
    {"person_id": 2, "org_id": 2, "title": "州长（代）", "start_date": "2026-01", "end_date": "present", "rank": "地级市正职", "note": "2026-01-22 州人大第28次会议决定代理州长"},
    {"person_id": 2, "org_id": 1, "title": "州委副书记", "start_date": "2026-01", "end_date": "present", "rank": "地级市副职", "note": "州政府党组书记"},

    # 洛珠南杰 (id 3)
    {"person_id": 3, "org_id": 3, "title": "州人大常委会主任", "start_date": "2024-01", "end_date": "present", "rank": "地级市正职", "note": "2024-01-19 十五届人大五次会议补选"},

    # 葛培军 (id 4)
    {"person_id": 4, "org_id": 4, "title": "州政协主席", "start_date": "2024-01", "end_date": "present", "rank": "地级市正职", "note": "2024-01-19 政协十四届四次会议补选"},

    # 李汉江 (id 16)
    {"person_id": 16, "org_id": 3, "title": "州人大常委会副主任", "start_date": "2024-01", "end_date": "present", "rank": "地级市副职", "note": "2024-01-19 补选"},

    # 邸森 (id 7)
    {"person_id": 7, "org_id": 2, "title": "常务副州长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": "州委常委、州政府党组副书记；2025-12 起多次主持州政府党组会议（州长空缺期间）"},
    {"person_id": 7, "org_id": 1, "title": "州委常委", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},

    # 田哲 (id 8)
    {"person_id": 8, "org_id": 2, "title": "州政府党组副书记、副州长人选（援青）", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": "援青干部"},
    {"person_id": 8, "org_id": 1, "title": "州委副书记", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 8, "org_id": 11, "title": "上海市人民政府驻西宁办事处主任", "start_date": "unknown", "end_date": "present", "rank": "厅级", "note": "现任，上海市援青干部"},

    # 副州长
    {"person_id": 9, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": "兼州公安局局长"},
    {"person_id": 10, "org_id": 5, "title": "州公安局局长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": "民建+中共党员"},

    # 张晓军 (id 5)
    {"person_id": 5, "org_id": 1, "title": "州委书记", "start_date": "2021-03", "end_date": "2024-07", "rank": "地级市正职", "note": "2024-07 卸任，与宁海鹰对调"},
    {"person_id": 5, "org_id": 6, "title": "青海省供销联社主任", "start_date": "2024-07", "end_date": "2024-12", "rank": "正厅级", "note": "2024-12 卸任后去向待查"},

    # 叶万彬 (id 6)
    {"person_id": 6, "org_id": 13, "title": "武威市委副书记、市长", "start_date": "2025-08", "end_date": "present", "rank": "正厅级", "note": "2025-08-28 选举确认；跨省调任"},
    {"person_id": 6, "org_id": 2, "title": "州长", "start_date": "2021-04", "end_date": "2025-07", "rank": "地级市正职", "note": "2021-08 正式当选；2025-07 卸任"},
    {"person_id": 6, "org_id": 1, "title": "州委副书记、州政府党组书记", "start_date": "2021-03", "end_date": "2021-04", "rank": "地级市副职", "note": ""},
    {"person_id": 6, "org_id": 18, "title": "海南州委常委、副州长", "start_date": "unknown", "end_date": "2021-03", "rank": "副厅级", "note": "其间挂职江苏无锡市副市长"},
    {"person_id": 6, "org_id": 17, "title": "青海省林业厅副厅长", "start_date": "2012-10", "end_date": "unknown", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 16, "title": "共青团青海省委工作人员至常委、工农青年部部长", "start_date": "2003-06", "end_date": "2012-10", "rank": "处级", "note": ""},

    # 更早
    {"person_id": 17, "org_id": 2, "title": "州长", "start_date": "unknown", "end_date": "2021", "rank": "地级市正职", "note": "2020年仍任州长；2021年由叶万彬接任"},
    {"person_id": 18, "org_id": 1, "title": "州委书记", "start_date": "unknown", "end_date": "2021-03", "rank": "地级市正职", "note": "2021-03 由张晓军接任"},

    # 县级
    {"person_id": 19, "org_id": 19, "title": "班玛县委书记", "start_date": "unknown", "end_date": "present", "rank": "县级正职", "note": "2026-07 新闻确认"},
    {"person_id": 20, "org_id": 19, "title": "班玛县委书记（前任）", "start_date": "unknown", "end_date": "unknown", "rank": "县级正职", "note": "~2025-06 在职"},
    {"person_id": 21, "org_id": 20, "title": "班玛县委副书记、县长", "start_date": "unknown", "end_date": "present", "rank": "县级正职", "note": ""},
    {"person_id": 22, "org_id": 21, "title": "达日县委书记", "start_date": "unknown", "end_date": "present", "rank": "县级正职", "note": ""},
    {"person_id": 23, "org_id": 22, "title": "达日县委副书记、县长", "start_date": "unknown", "end_date": "present", "rank": "县级正职", "note": ""},
    {"person_id": 24, "org_id": 23, "title": "甘德县委副书记、县长", "start_date": "unknown", "end_date": "present", "rank": "县级正职", "note": ""},
]

# ═══════════════════════════ Relationships ═══════════════════════════
relationships = [
    # 中央核心：书记-州长
    {"person_a": 1, "person_b": 2, "type": "决策搭档", "context": "现任州委书记与州长（代）党政一把/二把手搭档", "overlap_org": "中共果洛藏族自治州委员会/果洛州人民政府", "overlap_period": "2026-01至今"},
    {"person_a": 1, "person_b": 6, "type": "前任搭档", "context": "宁海鹰任州委书记期（2024-07起）与州长叶万彬（至2025-07）党政搭档", "overlap_org": "中共果洛藏族自治州委员会", "overlap_period": "2024-07至2025-07"},
    {"person_a": 2, "person_b": 6, "type": "前任-继任", "context": "桑本2026-01接任叶万彬州长职务", "overlap_org": "果洛藏族自治州人民政府", "overlap_period": "2026-01"},
    {"person_a": 6, "person_b": 17, "type": "前任-继任", "context": "叶万彬2021接替白加扎西州长", "overlap_org": "果洛藏族自治州人民政府", "overlap_period": "2021"},

    # 书记交接（对调）
    {"person_a": 1, "person_b": 5, "type": "前任-继任（对调）", "context": "宁海鹰与张晓军2024-07岗位对调（州委书记⇄省供销联社主任）", "overlap_org": "中共果洛藏族自治州委员会/青海省供销联社", "overlap_period": "2024-07"},
    {"person_a": 5, "person_b": 18, "type": "前任-继任", "context": "张晓军2021-03接替武玉嶂州委书记", "overlap_org": "中共果洛藏族自治州委员会", "overlap_period": "2021-03"},

    # 前任州长-前任书记 搭档
    {"person_a": 5, "person_b": 6, "type": "前任搭档", "context": "张晓军任州委书记（2021-03至2024-07）与州长叶万彬搭档", "overlap_org": "中共果洛藏族自治州委员会", "overlap_period": "2021-03至2024-07"},

    # 现任班子
    {"person_a": 2, "person_b": 7, "type": "上下级/班子", "context": "常务副州长邸森协助州长主持州政府日常；2025-12州长空缺期间代主持", "overlap_org": "果洛藏族自治州人民政府", "overlap_period": "2026-01至今"},
    {"person_a": 1, "person_b": 7, "type": "班子交集", "context": "邸森为州委常委、常务副州长，同属州委常委会", "overlap_org": "中共果洛藏族自治州委员会", "overlap_period": "unknown至今"},
    {"person_a": 2, "person_b": 8, "type": "班子/协作", "context": "副州长（援青）田哲兼州政府党组副书记，沪果对口支援协作", "overlap_org": "果洛藏族自治州人民政府", "overlap_period": "2026-01至今"},
    {"person_a": 1, "person_b": 8, "type": "班子交集", "context": "田哲兼州委副书记，与州委书记同属州委常委班子", "overlap_org": "中共果洛藏族自治州委员会", "overlap_period": "unknown至今"},
    {"person_a": 1, "person_b": 3, "type": "班子交集", "context": "州委书记与州人大常委会主任同属州四套班子", "overlap_org": "中共果洛藏族自治州委员会", "overlap_period": "2024-01至今"},
    {"person_a": 1, "person_b": 4, "type": "班子交集", "context": "州委书记与州政协主席同属州四套班子", "overlap_org": "中共果洛藏族自治州委员会", "overlap_period": "2024-01至今"},
    {"person_a": 2, "person_b": 3, "type": "班子交集", "context": "州长（代）与州人大常委会主任同属州四套班子", "overlap_org": "中共果洛藏族自治州委员会", "overlap_period": "2026-01至今"},
    {"person_a": 2, "person_b": 4, "type": "班子交集", "context": "州长（代）与州政协主席同属州四套班子", "overlap_org": "中共果洛藏族自治州委员会", "overlap_period": "2026-01至今"},
    {"person_a": 5, "person_b": 3, "type": "班子交集", "context": "张晓军任州委书记（至2024-07）与洛珠南杰（2024-01当选人大主任）短暂同班子", "overlap_org": "中共果洛藏族自治州委员会", "overlap_period": "2024-01至2024-07"},

    # 州长-各副州长 班子
    {"person_a": 2, "person_b": 9, "type": "班子/上下级", "context": "州长与副州长同属州政府班子", "overlap_org": "果洛藏族自治州人民政府", "overlap_period": "2026-01至今"},
    {"person_a": 2, "person_b": 10, "type": "班子/上下级", "context": "州长与副州长（兼公安局长）同属州政府班子", "overlap_org": "果洛藏族自治州人民政府", "overlap_period": "2026-01至今"},
    {"person_a": 2, "person_b": 11, "type": "班子/上下级", "context": "州长与副州长同属州政府班子", "overlap_org": "果洛藏族自治州人民政府", "overlap_period": "2026-01至今"},
    {"person_a": 2, "person_b": 12, "type": "班子/上下级", "context": "州长与副州长同属州政府班子", "overlap_org": "果洛藏族自治州人民政府", "overlap_period": "2026-01至今"},
    {"person_a": 2, "person_b": 13, "type": "班子/上下级", "context": "州长与副州长同属州政府班子", "overlap_org": "果洛藏族自治州人民政府", "overlap_period": "2026-01至今"},
    {"person_a": 2, "person_b": 14, "type": "班子/上下级", "context": "州长与副州长同属州政府班子", "overlap_org": "果洛藏族自治州人民政府", "overlap_period": "2026-01至今"},
    {"person_a": 2, "person_b": 15, "type": "班子/上下级", "context": "州长与副州长同属州政府班子", "overlap_org": "果洛藏族自治州人民政府", "overlap_period": "2026-01至今"},

    # 州—县 纵向链条
    {"person_a": 1, "person_b": 19, "type": "上下级（州-县）", "context": "州委书记与班玛县委书记纵向隶属", "overlap_org": "中共果洛藏族自治州委员会", "overlap_period": "2024-07至今"},
    {"person_a": 19, "person_b": 20, "type": "前任-继任", "context": "张效勇接替（或前任）祁宝业任班玛县委书记", "overlap_org": "中共班玛县委员会", "overlap_period": "unknown"},
    {"person_a": 2, "person_b": 21, "type": "上下级（州-县）", "context": "州长（代）与班玛县县长纵向隶属", "overlap_org": "果洛藏族自治州人民政府", "overlap_period": "2026-01至今"},
]


def main():
    print(f"[果洛藏族自治州] 构建 SQLite DB + GEXF ...")
    run_build(slug=SLUG, persons=persons, organizations=organizations,
              positions=positions, relationships=relationships,
              db_path=DB_PATH, gexf_path=GEXF_PATH)
    _verify_db()
    write_persons_files()
    print(f"[果洛藏族自治州] 完成：{DB_PATH}\n{GEXF_PATH}\npersons JSON {len(persons)} 人")


def _verify_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        required = {"persons", "organizations", "positions", "relationships"}
        missing = sorted(required - tables)
        if missing:
            raise SystemExit(f"DB 缺少表: {missing}")
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in sorted(required)}
        print(f"  DB 校验: {counts}")
    finally:
        conn.close()


# ═══════════════════════════ Person JSON ═══════════════════════════
SOURCE_REGISTER = [
    {"id": "S001", "title": "中国经济网——宁海鹰任果洛州委书记 张晓军不再担任", "url": "http://district.ce.cn/newarea/sddy/202407/05/t20240705_39060801.shtml", "publisher": "中国经济网", "published_at": "2024-07-05", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "宁海鹰1972-07；曾任果洛州委副书记、省民宗委副主任、省委统战部副部长/涉外藏胞办主任/省侨办主任、省供销联社党组书记"},
    {"id": "S002", "title": "中国经济网——桑本任果洛州代州长", "url": "http://distalk.ce.cn/newarea/sddy/202601/t20260123_2723475.shtml", "publisher": "中国经济网", "published_at": "2026-01-23", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "2026-01-22州人大第28次会议任命副州长并决定代理州长（来源：果洛人大）"},
    {"id": "S003", "title": "果洛州人民政府——领导信息 州长桑本简历", "url": "http://www.guoluo.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/sb/202603/t20260305_394157.html", "publisher": "果洛州人民政府", "published_at": "2026-03-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "桑本：男，藏族，1980年11月生，青海共和人，2001-09参加工作，2000-06入党，在职硕士，州委副书记/州政府党组书记/州长"},
    {"id": "S004", "title": "果洛州人民政府——领导信息（州政府班子）", "url": "http://www.guoluo.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/", "publisher": "果洛州人民政府", "published_at": "2026-08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "州长桑本及副州长邸森、田哲、西热、蒲智军、卓玛当周、邓生栋、普措格来、申丽玲、高峰的官方简历"},
    {"id": "S005", "title": "中国经济网——洛珠南杰当选果洛州人大常委会主任", "url": "http://district.ce.cn/newarea/sddy/202401/20/t20240120_38874257.shtml", "publisher": "中国经济网", "published_at": "2024-01-20", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "2024-01-19 洛珠南杰当选州人大主任，李汉江当选副主任"},
    {"id": "S006", "title": "中国经济网——葛培军当选果洛州政协主席", "url": "http://district.ce.cn/newarea/sddy/202401/20/t20240120_38874254.shtml", "publisher": "中国经济网", "published_at": "2024-01-20", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "2024-01-19 政协十四届四次会议补选葛培军为主席"},
    {"id": "S007", "title": "Wikipedia zh《果洛藏族自治州》", "url": "https://zh.wikipedia.org/wiki/果洛藏族自治州", "publisher": "Wikipedia", "published_at": "2026", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "现任领导表：宁海鹰(2024-07)、洛珠南杰(2024-01)、桑本(2026-01)、葛培军(2024-01)；桑本生年记1979-01与官方1980-11有出入"},
    {"id": "S008", "title": "Wikipedia zh《张晓军 (1974年)》", "url": "https://zh.wikipedia.org/wiki/张晓军_(1974年)", "publisher": "Wikipedia", "published_at": "2026", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "张晓军：1974-04，山西原平；果洛州委书记2021-03~2024-07；省供销联社主任2024-07~2024-12；前任武玉嶂"},
    {"id": "S009", "title": "仓库既有档案——叶万彬(武威市长) person JSON", "url": "file://data/persons/20260717-甘肃省-武威市-市长-叶万彬.json", "publisher": "gov-relation 仓库", "published_at": "2026-07-17", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "叶万彬：藏族，1977-05，青海乐都；果洛州长2021-04~2025-07；2025-08跨省任武威代市长→市长（澎湃新闻2025-08-28）"},
    {"id": "S010", "title": "果洛州人民政府——州政府新闻（邸森主持州政府党组会议等）", "url": "http://www.guoluo.gov.cn/zwgk/zzfhy/", "publisher": "果洛州人民政府", "published_at": "2025-12~2026-08", "accessed_at": AS_OF, "source_type": "official", "reliability": "medium", "notes": "2025-12-30州政府党组会议邸森主持；2026年党代会周宁海鹰/桑本活动动态；2020-05-21白加扎西（时任州长）访谈转载"},
]


def build_person_file(name, current_post, profile, big_gap="", qs=None):
    """Write a person JSON from a single profile dict."""
    p = BASE / f"{TODAY}-青海省-果洛藏族自治州-{current_post}-{name}.json"
    orgs = profile.get("organizations", []) or []
    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {"province": "青海省", "city": "果洛藏族自治州", "region": "果洛藏族自治州",
                                "job": current_post, "task_id": "qinghai_果洛藏族自治州", "time_focus": "2024-2026"},
        "identity": {"person_id": f"golog_{name}", "name": name,
                     "aliases": [], "gender": profile.get("gender", ""),
                     "ethnicity": profile.get("ethnicity", ""),
                     "birth": profile.get("birth", ""),
                     "birthplace": profile.get("birthplace", ""),
                     "native_place": profile.get("birthplace", ""),
                     "education": profile.get("education", []),
                     "party_join": profile.get("party_join", ""), "work_start": profile.get("work_start", ""),
                     "dedupe_keys": {"name_birth": f"golog_{name}_{profile.get('birth','')}",
                                     "name_birthplace": f"golog_{name}_{profile.get('birthplace','')}",
                                     "official_profile_url": profile.get("profile_url", "")}},
        "current_status": {"current_post": current_post, "current_org": profile.get("current_org", ""),
                           "administrative_rank": profile.get("rank", ""), "as_of": AS_OF,
                           "is_current_confirmed": profile.get("is_confirmed", True),
                           "source_ids": list(profile.get("source_ids", ["S001", "S002"]))},
        "career_timeline": profile.get("career_timeline", []),
        "organizations": orgs,
        "relationships": profile.get("relationships", []),
        "governance_record": profile.get("governance_record", []),
        "professional_profile": profile.get("professional_profile", {}),
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": profile.get("risk_signals", []),
        "source_register": SOURCE_REGISTER,
        "confidence_summary": {
            "identity": profile.get("identity_confidence", "confirmed"),
            "current_role": profile.get("current_confidence", "confirmed"),
            "career_completeness": profile.get("career_completeness", "partial"),
            "relationship_confidence": profile.get("relationship_confidence", "medium"),
            "biggest_gap": big_gap or profile.get("biggest_gap", "")},
        "open_questions": qs or [{"priority": "high", "question": big_gap or profile.get("biggest_gap", "履历未完整"),
                                  "why_it_matters": "任职网络分析",
                                  "suggested_queries": [f"{name} 简历"], "last_attempted": AS_OF}],
    }
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("  person JSON:", p.name)


def write_persons_files():
    # ── 州委书记 宁海鹰 ──
    build_person_file(
        "宁海鹰", "州委书记",
        {"gender": "男", "ethnicity": "汉族", "birth": "1972年7月", "birthplace": "青海省西宁市湟中区",
         "education": [], "party_join": "中共党员", "work_start": "",
         "current_org": "中共果洛藏族自治州委员会", "rank": "地级市正职", "profile_url": "",
         "is_confirmed": True, "source_ids": ["S001", "S007"],
         "identity_confidence": "confirmed", "current_confidence": "confirmed", "career_completeness": "partial",
         "relationships": [
             {"person": "桑本", "person_id": "golog_桑本", "relationship_type": "overlap", "strength": "strong", "evidence": "现任党政一把手搭档（书记+州长）", "overlap_org": "中共果洛州委/州政府", "overlap_period": "2026-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
             {"person": "张晓军", "person_id": "golog_张晓军", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "2024-07 职务对调：宁海鹰接任州委书记，张晓军转任省供销联社主任", "overlap_org": "中共果洛州委/青海省供销联社", "overlap_period": "2024-07", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S008"]},
             {"person": "叶万彬", "person_id": "golog_叶万彬", "relationship_type": "overlap", "strength": "strong", "evidence": "宁任州委书记（2024-07起）期间叶万彬仍任州长（至2025-07）", "overlap_org": "中共果洛州委", "overlap_period": "2024-07至2025-07", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S009"]},
             {"person": "洛珠南杰", "person_id": "golog_洛珠南杰", "relationship_type": "overlap", "strength": "medium", "evidence": "州四套班子交集", "overlap_org": "中共果洛州委员会", "overlap_period": "2024-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
             {"person": "葛培军", "person_id": "golog_葛培军", "relationship_type": "overlap", "strength": "medium", "evidence": "州四套班子交集", "overlap_org": "中共果洛州委员会", "overlap_period": "2024-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
             {"person": "田哲", "person_id": "golog_田哲", "relationship_type": "overlap", "strength": "medium", "evidence": "田哲兼州委副书记，同属州委班子", "overlap_org": "中共果洛州委", "overlap_period": "unknown至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]}],
         "organizations": [
             {"id": "golog_州委", "name": "中共果洛藏族自治州委员会", "type": "党委", "level": "地级", "location": "玛沁县"},
             {"id": "golog_州政府", "name": "果洛藏族自治州人民政府", "type": "政府", "level": "地级", "location": "玛沁县"},
             {"id": "qh_供销联社", "name": "青海省供销联社", "type": "事业单位", "level": "省级", "location": "西宁市"},
             {"id": "qh_统战部", "name": "中共青海省委统战部", "type": "党委", "level": "省级", "location": "西宁市"},
             {"id": "qh_民宗委", "name": "青海省民族宗教事务委员会", "type": "政府", "level": "省级", "location": "西宁市"}],
         "career_timeline": [
             {"start": "2024-07", "end": "present", "org": "中共果洛藏族自治州委员会", "title": "州委书记", "level": "地级市", "system": "party", "rank": "地级市正职", "is_key_promotion": True, "notes": "2024-07-04省委决定，接替张晓军", "confidence": "confirmed", "source_ids": ["S001"]},
             {"start": "unknown", "end": "2024-07", "org": "青海省供销联社", "title": "党组书记、理事会主任", "level": "省级", "system": "other", "rank": "正厅级", "is_key_promotion": True, "notes": "任期起点待查", "confidence": "confirmed", "source_ids": ["S001", "S008"]},
             {"start": "unknown", "end": "unknown", "org": "中共青海省委统战部", "title": "副部长、省国外藏胞工作办公室主任", "level": "省级", "system": "party", "rank": "副厅级", "is_key_promotion": False, "notes": "此前曾任", "confidence": "confirmed", "source_ids": ["S001"]},
             {"start": "unknown", "end": "unknown", "org": "青海省民族宗教事务委员会", "title": "副主任", "level": "省级", "system": "government", "rank": "副厅级", "is_key_promotion": False, "notes": "此前曾任", "confidence": "confirmed", "source_ids": ["S001"]},
             {"start": "unknown", "end": "unknown", "org": "青海省人民政府侨务办公室", "title": "主任", "level": "省级", "system": "government", "rank": "副厅级", "is_key_promotion": False, "notes": "此前曾任", "confidence": "confirmed", "source_ids": ["S001"]},
             {"start": "unknown", "end": "unknown", "org": "中共果洛藏族自治州委员会", "title": "州委副书记", "level": "地级市", "system": "party", "rank": "地级市副职", "is_key_promotion": False, "notes": "此前曾任（早年主政任职）", "confidence": "confirmed", "source_ids": ["S001"]},
             {"start": "unknown", "end": "unknown", "org": "履历缺口（2020年前早期岗位未获一级来源）", "title": "", "level": "", "system": "", "rank": "", "notes": "学历、入党、参加工作等出生年份外信息缺失", "confidence": "unverified", "source_ids": []}],
         "professional_profile": {"primary_specializations": ["民族宗教事务", "统战与涉藏工作", "供销系统管理", "民族地区治理"], "secondary_specializations": [],
                                  "career_pattern": "provincial_department", "systems_experience": ["party", "government", "other"],
                                  "geographic_pattern": ["西宁（省直）→ 果洛（早年州委副书记→现任州委书记）"], "promotion_velocity": {"summary": "省级统战/民族宗教系统历练后主政一州", "notable_fast_promotions": []}},
         "risk_signals": [{"type": "none_found", "description": "公开检索未发现处分/审计/舆情问题（截至" + AS_OF + "）", "date": AS_OF, "confidence": "confirmed", "source_ids": []}],
         "biggest_gap": "宁海鹰 2020 年前早期履历（学历、入党、初入仕途）"},
        qs=[
            {"priority": "high", "question": "宁海鹰 2020 年前完整履历（学历、入党时间、初入仕途岗位）？", "why_it_matters": "其省民宗委/统战部职务之前的晋升路径未明", "suggested_queries": ["宁海鹰 简历 青海", "宁海鹰 民族宗教事务委员会 副主任 任职"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "宁海鹰任青海省供销联社党组书记的确切起止时间？", "why_it_matters": "补全正厅级岗位时间线", "suggested_queries": ["宁海鹰 供销联社 主任 2022"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "宁海鹰早年任果洛州委副书记的具体年份？", "why_it_matters": "其与果洛的渊源年份", "suggested_queries": ["宁海鹰 果洛州委副书记"], "last_attempted": AS_OF}],
    )

    # ── 州长 桑本 ──
    build_person_file(
        "桑本", "州长",
        {"gender": "男", "ethnicity": "藏族", "birth": "1980年11月", "birthplace": "青海省共和县",
         "education": [{"period": "unknown", "institution": "在职硕士", "major": "", "degree": "硕士研究生", "study_type": "part_time", "source_ids": ["S003"]}],
         "party_join": "2000年6月", "work_start": "2001年9月",
         "current_org": "果洛藏族自治州人民政府", "rank": "地级市正职", "profile_url": "http://www.guoluo.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/sb/202603/t20260305_394157.html",
         "is_confirmed": True, "source_ids": ["S002", "S003"],
         "identity_confidence": "confirmed", "current_confidence": "confirmed", "career_completeness": "thin",
         "relationships": [
             {"person": "宁海鹰", "person_id": "golog_宁海鹰", "relationship_type": "overlap", "strength": "strong", "evidence": "现任党政一把手搭档（州长+州委书记）", "overlap_org": "中共果洛州委/州政府", "overlap_period": "2026-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
             {"person": "叶万彬", "person_id": "golog_叶万彬", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "2026-01 接任叶万彬州长（2025-07卸任）", "overlap_org": "果洛州人民政府", "overlap_period": "2026-01", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S009"]},
             {"person": "邸森", "person_id": "golog_邸森", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "州长与常务副州长，党组班子上下级", "overlap_org": "果洛州人民政府", "overlap_period": "2026-01至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S004"]},
             {"person": "田哲", "person_id": "golog_田哲", "relationship_type": "overlap", "strength": "medium", "evidence": "州政府班子（田哲为援青副州长），沪果协作", "overlap_org": "果洛州人民政府", "overlap_period": "2026-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]}],
         "organizations": [
             {"id": "golog_州政府", "name": "果洛藏族自治州人民政府", "type": "政府", "level": "地级", "location": "玛沁县"},
             {"id": "golog_州委", "name": "中共果洛藏族自治州委员会", "type": "党委", "level": "地级", "location": "玛沁县"}],
         "career_timeline": [
             {"start": "2026-01", "end": "present", "org": "果洛藏族自治州人民政府", "title": "州长（代理）", "level": "地级市", "system": "government", "rank": "地级市正职", "is_key_promotion": True, "notes": "2026-01-22州人大第28次会议任命副州长并决定代理州长", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
             {"start": "2026-01", "end": "present", "org": "中共果洛藏族自治州委员会", "title": "州委副书记、州政府党组书记", "level": "地级市", "system": "party", "rank": "地级市重职", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
             {"start": "unknown", "end": "2025-12", "org": "履历缺口（2026年前岗位未获公开来源）", "title": "", "level": "", "system": "", "rank": "", "notes": "2018-2018年任前岗位未知；出生地共和县（海南州），年龄1979/1980争议", "confidence": "unverified", "source_ids": []}],
         "professional_profile": {"primary_specializations": ["民族地区治理(推定)"], "secondary_specializations": [],
                                  "career_pattern": "unknown", "systems_experience": [], "geographic_pattern": ["共和（出生，海南州）→ 果洛"],
                                  "promotion_velocity": {"summary": "履历前段未知，无从评估", "notable_fast_promotions": []}},
         "risk_signals": [{"type": "none_found", "description": "公开检索未发现处分/审计/舆情问题（截至" + AS_OF + "）", "date": AS_OF, "confidence": "confirmed", "source_ids": []}],
         "biggest_gap": "桑本 2026 年前完整履历（critical）"},
        qs=[
            {"priority": "critical", "question": "桑本任果洛州长前的完整履历（2026年前岗位、晋升路径）？", "why_it_matters": "核心二人中履历信息最薄者，直接影响网络分析完整性", "suggested_queries": ["桑本 简历", "桑本 青海 县委书记", "桑本 任前公示"], "last_attempted": AS_OF},
            {"priority": "high", "question": "桑本出生日期：官方 1980-11 vs Wikipedia 1979-01 出入，以何为准？", "why_it_matters": "身份去重关键字段", "suggested_queries": ["桑本 出生 1980 1979 果洛"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "2025-07 叶万彬卸任至 2026-01 桑本到任之间，州政府由谁主持（推断常务副州长邸森）？", "why_it_matters": "人事空缺期治理线索", "suggested_queries": ["果洛州 代州长 2025"], "last_attempted": AS_OF}],
    )

    # ── 前任州委书记 张晓军 ──
    build_person_file(
        "张晓军", "前任州委书记",
        {"gender": "男", "ethnicity": "汉族", "birth": "1974年4月", "birthplace": "山西省原平市",
         "education": [{"period": "unknown", "institution": "青海玉树州民族师范学校", "major": "", "degree": "中专", "study_type": "unknown", "source_ids": ["S008"]}],
         "party_join": "中共党员", "work_start": "",
         "current_org": "", "rank": "地级市正职", "profile_url": "https://zh.wikipedia.org/wiki/张晓军_(1974年)",
         "is_confirmed": False, "source_ids": ["S008"],
         "identity_confidence": "confirmed", "current_confidence": "confirmed", "career_completeness": "thin",
         "relationships": [
             {"person": "宁海鹰", "person_id": "golog_宁海鹰", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "2024-07 职务对调：张晓军卸任州委书记转省供销联社主任，宁海鹰接任", "overlap_org": "中共果洛州委/青海省供销联社", "overlap_period": "2024-07", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S008"]},
             {"person": "叶万彬", "person_id": "golog_叶万彬", "relationship_type": "overlap", "strength": "strong", "evidence": "张晓军任州委书记期间叶万彬任州长（党政搭档）", "overlap_org": "中共果洛州委", "overlap_period": "2021-03至2024-07", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S008", "S009"]},
             {"person": "武玉嶂", "person_id": "golog_武玉嶂", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "2021-03 接任武玉嶂州委书记", "overlap_org": "中共果洛州委", "overlap_period": "2021-03", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S008"]}],
         "organizations": [
             {"id": "golog_州委", "name": "中共果洛藏族自治州委员会", "type": "党委", "level": "地级", "location": "玛沁县"},
             {"id": "qh_供销联社", "name": "青海省供销联社", "type": "事业单位", "level": "省级", "location": "西宁市"}],
         "career_timeline": [
             {"start": "2021-03", "end": "2024-07", "org": "中共果洛藏族自治州委员会", "title": "州委书记", "level": "地级市", "system": "party", "rank": "地级市正职", "is_key_promotion": True, "notes": "2024-07 卸任", "confidence": "confirmed", "source_ids": ["S001", "S008"]},
             {"start": "2024-07", "end": "2024-12", "org": "青海省供销联社", "title": "主任", "level": "省级", "system": "other", "rank": "正厅级", "is_key_promotion": False, "notes": "2024-12 卸任；之后去向待查", "confidence": "confirmed", "source_ids": ["S008"]},
             {"start": "unknown", "end": "unknown", "org": "履历缺口（2021年前早期履历及2024-12后去向）", "title": "", "level": "", "system": "", "rank": "", "notes": "玉树师范学校毕业，其余未明", "confidence": "unverified", "source_ids": []}],
         "biggest_gap": "张晓军 2024-12 卸任省供销联社主任后的去向，及 2021年前早期履历"},
        qs=[
            {"priority": "high", "question": "张晓军 2024-12 卸任青海省供销联社主任后的去向？", "why_it_matters": "前任州委书记的动态是此前提更迭线索", "suggested_queries": ["张晓军 供销联社 卸任 去向"], "last_attempted": AS_OF},
            {"priority": "high", "question": "张晓军 2021年任果洛州委书记前的早期履历？", "why_it_matters": "评估其晋升路径与省直网络", "suggested_queries": ["张晓军 简历 青海 玉树"], "last_attempted": AS_OF}],
    )

    # ── 前任州长 叶万彬 ──
    build_person_file(
        "叶万彬", "前任州长",
        {"gender": "男", "ethnicity": "藏族", "birth": "1977年5月", "birthplace": "青海省海东市乐都区",
         "education": [{"period": "1993-09--1996-07", "institution": "青海省海西州民族卫生学校", "major": "医学检验", "degree": "中专", "study_type": "full_time", "source_ids": ["S009"]}],
         "party_join": "2001年11月", "work_start": "1996年7月",
         "current_org": "武威市人民政府", "rank": "正厅级", "profile_url": "",
         "is_confirmed": False, "source_ids": ["S009"],
         "identity_confidence": "confirmed", "current_confidence": "confirmed", "career_completeness": "partial",
         "relationships": [
             {"person": "桑本", "person_id": "golog_桑本", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "桑本2026-01接任其州长职务", "overlap_org": "果洛州人民政府", "overlap_period": "2026-01", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S009"]},
             {"person": "张晓军", "person_id": "golog_张晓军", "relationship_type": "overlap", "strength": "strong", "evidence": "党政搭档（书记+州长）2021-2024", "overlap_org": "中共果洛州委", "overlap_period": "2021-03至2024-07", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S008", "S009"]},
             {"person": "宁海鹰", "person_id": "golog_宁海鹰", "relationship_type": "overlap", "strength": "strong", "evidence": "党政搭档（书记+州长）2024-2025", "overlap_org": "中共果洛州委", "overlap_period": "2024-07至2025-07", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S009"]},
             {"person": "武和谦", "person_id": "gansu_wuwei_wu_heqian_1971", "relationship_type": "overlap", "strength": "strong", "evidence": "现武威党政一把手搭档（叶任市长，武和谦任书记）——跨省后新网络", "overlap_org": "中共武威市委", "overlap_period": "2025-08至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S009"]}],
         "organizations": [
             {"id": "golog_州政府", "name": "果洛藏族自治州人民政府", "type": "政府", "level": "地级", "location": "玛沁县"},
             {"id": "wuwei_gov", "name": "武威市人民政府", "type": "政府", "level": "地级", "location": "甘肃省武威市"},
             {"id": "qh_林业厅", "name": "青海省林业厅", "type": "政府", "level": "省级", "location": "西宁市"},
             {"id": "qh_团省委", "name": "共青团青海省委", "type": "群团", "level": "省级", "location": "西宁市"}],
         "career_timeline": [
             {"start": "2021-04", "end": "2025-07", "org": "果洛藏族自治州人民政府", "title": "州长", "level": "地级市", "system": "government", "rank": "地级市正职", "is_key_promotion": True, "notes": "2021-08正式当选；2025-07卸任", "confidence": "confirmed", "source_ids": ["S009"]},
             {"start": "2025-08", "end": "present", "org": "武威市人民政府", "title": "市委副书记、市长", "level": "地级市", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "跨省调任；2025-08-28当选", "confidence": "confirmed", "source_ids": ["S009"]},
             {"start": "unknown", "end": "2021-03", "org": "中共海南藏族自治州委员会", "title": "州委常委、副州长", "level": "地级市", "system": "government", "rank": "副厅级", "is_key_promotion": False, "notes": "其间挂职江苏省无锡市副市长", "confidence": "confirmed", "source_ids": ["S009"]},
             {"start": "2012-10", "end": "unknown", "org": "青海省林业厅", "title": "副厅长、党组成员", "level": "省级", "system": "government", "rank": "副厅级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S009"]},
             {"start": "2003-06", "end": "2012-10", "org": "共青团青海省委", "title": "办公室到常委、工农青年部部长", "level": "省级", "system": "other", "rank": "处级至正处级", "is_key_promotion": True, "notes": "由团系统逐步晋升", "confidence": "confirmed", "source_ids": ["S009"]}],
         "professional_profile": {"primary_specializations": ["民族地区治理", "共青团系统", "林业管理"], "secondary_specializations": [],
                                  "career_pattern": "cross_province_rotation", "systems_experience": ["government", "party", "other"],
                                  "geographic_pattern": ["乐都→海西→西宁→海南州→果洛→甘肃武威"], "promotion_velocity": {"summary": "藏医院检验员→正厅，跨省调动罕见", "notable_fast_promotions": []}},
         "risk_signals": [{"type": "none_found", "description": "未发现公开处分/负面报道（截至" + AS_OF + "）", "date": AS_OF, "confidence": "confirmed", "source_ids": []}],
         "biggest_gap": "叶万彬团青海省委书记任期的具体起止时间与海南州任职年份"},
    )

    # ── 州人大常委会主任 洛珠南杰 ──
    build_person_file(
        "洛珠南杰", "州人大常委会主任",
        {"gender": "男", "ethnicity": "藏族", "birth": "1976年4月", "birthplace": "甘肃省天祝藏族自治县",
         "education": [], "party_join": "中共党员", "work_start": "",
         "current_org": "果洛藏族自治州人民代表大会常务委员会", "rank": "地级市正职", "profile_url": "",
         "is_confirmed": True, "source_ids": ["S005", "S007"],
         "identity_confidence": "confirmed", "current_confidence": "confirmed", "career_completeness": "thin",
         "relationships": [
             {"person": "宁海鹰", "person_id": "golog_宁海鹰", "relationship_type": "overlap", "strength": "medium", "evidence": "州四套班子交集", "overlap_org": "中共果洛州委", "overlap_period": "2024-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
             {"person": "桑本", "person_id": "golog_桑本", "relationship_type": "overlap", "strength": "medium", "evidence": "州四套班子交集", "overlap_org": "中共果洛州委", "overlap_period": "2026-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005", "S003"]}],
         "organizations": [{"id": "golog_人大", "name": "果洛藏族自治州人民代表大会常务委员会", "type": "人大", "level": "地级", "location": "玛沁县"}],
         "career_timeline": [
             {"start": "2024-01", "end": "present", "org": "果洛州人大常委会", "title": "主任", "level": "地级市", "system": "other", "rank": "地级市正职", "is_key_promotion": True, "notes": "2024-01-19十五届人大五次会议补选", "confidence": "confirmed", "source_ids": ["S005", "S007"]},
             {"start": "unknown", "end": "unknown", "org": "履历缺口（2024年前履历）", "title": "", "level": "", "system": "", "rank": "", "notes": "甘肃天祝藏族，此前履历未获来源", "confidence": "unverified", "source_ids": []}],
         "biggest_gap": "洛珠南杰 2024 年前完整履历"},
        qs=[{"priority": "high", "question": "洛珠南杰当选州人大主任前的完整履历？", "why_it_matters": "其来源（甘肃天祝藏族）预示跨省/省直背景", "suggested_queries": ["洛珠南杰 简历"], "last_attempted": AS_OF}],
    )

    # ── 州政协主席 葛培军 ──
    build_person_file(
        "葛培军", "州政协主席",
        {"gender": "男", "ethnicity": "汉族", "birth": "1972年9月", "birthplace": "江苏省镇江市",
         "education": [], "party_join": "中共党员", "work_start": "",
         "current_org": "中国人民政治协商会议果洛藏族自治州委员会", "rank": "地级市正职", "profile_url": "",
         "is_confirmed": True, "source_ids": ["S006", "S007"],
         "identity_confidence": "confirmed", "current_confidence": "confirmed", "career_completeness": "thin",
         "relationships": [
             {"person": "宁海鹰", "person_id": "golog_宁海鹰", "relationship_type": "overlap", "strength": "medium", "evidence": "州四套班子交集", "overlap_org": "中共果洛州委", "overlap_period": "2024-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
             {"person": "桑本", "person_id": "golog_桑本", "relationship_type": "overlap", "strength": "medium", "evidence": "州四套班子交集", "overlap_org": "中共果洛州委", "overlap_period": "2026-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006", "S003"]}],
         "organizations": [{"id": "golog_政协", "name": "中国人民政治协商会议果洛藏族自治州委员会", "type": "政协", "level": "地级", "location": "玛沁县"}],
         "career_timeline": [
             {"start": "2024-01", "end": "present", "org": "果洛州政协", "title": "主席", "level": "地级市", "system": "other", "rank": "地级市正职", "is_key_promotion": True, "notes": "2024-01-19政协十四届四次会议补选", "confidence": "confirmed", "source_ids": ["S006", "S007"]},
             {"start": "unknown", "end": "unknown", "org": "履历缺口（2024年前履历）", "title": "", "level": "", "system": "", "rank": "", "notes": "江苏镇江籍，疑为苏青对口支援（援青）干部；具体履历未获来源", "confidence": "unverified", "source_ids": []}],
         "biggest_gap": "葛培军 2024 年前完整履历及是否为江苏援青干部"},
        qs=[{"priority": "high", "question": "葛培军当选州政协主席前的履历？是否系江苏援青干部？", "why_it_matters": "若为援青干部则构成苏果协作人事通道", "suggested_queries": ["葛培军 简历 镇江 援青"], "last_attempted": AS_OF}],
    )


if __name__ == "__main__":
    main()
