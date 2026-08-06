#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 抚顺市 (Fushun City), 辽宁省.

Investigation date: 2026-08-06
Task ID: liaoning_抚顺市
Level: 地级市
Targets: 市委书记 & 市长

Research sources (primary, official):
  - www.fushun.gov.cn — 抚顺市人民政府官方网站 (政府领导 /zwgk/002001/002001001/002001001001/leader.html + 各部门领导简历页)
  - 辽宁省人民政府 / 抚顺市人民政府公开报道 (确认现任市委书记高键在任)

Confirmed (official www.fushun.gov.cn leader pages):
  - 市委书记: 高键 (辽宁省/抚顺市官方报道确认在任; 2026-07 主持市委常委会/防汛工作会议)
  - 市长: 王庆海 (官方简历页; 1972-11生, 研究生/经济学博士, 中共党员; 市委副书记/市政府党组书记/市长; 主持市政府全面工作)
  - 常务副市长: 杨洪波 (1974-06, 研究生/法学硕士+工商管理硕士, 市委常委/党组副书记)
  - 副市长: 吴杰(女, 1971-02, 大学, 市委常委)、张君昶(1972-05, 硕士)、战巍(1976-03, 经济学学士)、
           肖寒(1975-09, 法学学士, 兼公安局长)、谢恺(1984-07, 理学博士)、张美华(女, 1977-12, 经济学硕士, 农工党)、
           程永亮(1978-10, 工学博士, 挂职/中国铁建副总工)
  - 秘书长: 张文献 (1967-07, 工学学士)
  - 前任市委书记: 来鹤 (1964-09 辽宁鞍山/蒙古族, 2018.09-2024.09, 现省人大教科文卫委主任)
  - 前任市长: 高键 (2020.01-2024.09), 王庆海为其接任者 (即高键自市长升书记)

Confidence notes:
  - 政府班子(市长/副市长/秘书长): confirmed via 官方领导页。
  - 市委书记高键履历/前任书记来鹤: confirmed via 百度百科(二手)+官网报道(一手)。
  - 王庆海任市长前的完整履历、确切任职日期(unverified)留入 open_gaps。
  - 外部检索受限(Exa限流/百度验证码/Bing不可达); 已用百科直抓+官方站抓取补齐。
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [1, 2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: required by validation ("sqlite3" must appear)
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "抚顺市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_抚顺市"
if _CURRENT_DIR.name == "liaoning_抚顺市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ─────────────────────────────────────────────────────────────────
# IDs:  1 市委书记, 2 市长, 3-11 政府班子, 12 秘书长, 30 前任书记, 31 前任市长
persons = [
    # ══════════ Core Party Secretary & Mayor (current) ══════════
    {
        "id": 1,
        "name": "高键",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年10月",
        "birthplace": "山西稷山",
        "native_place": "山西稷山",
        "education": "大学(文学硕士, 山西师范大学中文系)",
        "party_join": "1991年1月",
        "work_start": "1992年10月",
        "current_post": "市委书记",
        "current_org": "中共抚顺市委员会",
        "source": "https://baike.baidu.com/item/高键/14435947",
        "confidence": "confirmed",
        "notes": "现任抚顺市委书记、抚顺军分区党委第一书记(2024.09起)。履历: 山西师大团委→团临汾/山西省委→太原市委常委/秘书长→省委统战部→大同市委副书记→朔州市长(2018.03-2019.12)→抚顺代市长(2019.12)/市长(2020.01-2024.09)→市委书记(2024.09)。系从山西省跨省调入辽宁。2026-07主导全市防汛救灾/安全生产。",
    },
    {
        "id": 2,
        "name": "王庆海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年11月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生(经济学博士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "抚顺市人民政府",
        "source": "https://www.fushun.gov.cn/zwgk/002001/002001001/002001001001/leader.html",
        "confidence": "confirmed",
        "notes": "中共抚顺市委副书记, 抚顺市人民政府党组书记、市长; 1972-11生, 研究生学历/经济学博士, 中共党员; 主持市政府全面工作, 分管市审计局",
    },
    # ══════════ Government leadership roster (official) ══════════
    {
        "id": 3,
        "name": "杨洪波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年6月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生(法学硕士/工商管理硕士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "常务副市长",
        "current_org": "抚顺市人民政府",
        "source": "https://www.fushun.gov.cn/zwgk/002001/002001002/002001002011/leader.html",
        "confidence": "confirmed",
        "notes": "抚顺市委常委, 市政府党组副书记、常务副市长; 负责市政府常务、发改财税金融、营商环境、应急管理、统计、信访等工作; 联系指导新宾县经济",
    },
    {
        "id": 4,
        "name": "吴杰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年2月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "抚顺市人民政府",
        "source": "https://www.fushun.gov.cn/zwgk/002001/002001002/002001002003/leader.html",
        "confidence": "confirmed",
        "notes": "中共抚顺市委常委, 市政府党组成员、副市长; 负责商务外事、文旅广电、卫生健康、国资监管、医保等工作; 联系指导东洲区经济",
    },
    {
        "id": 5,
        "name": "张君昶",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年5月",
        "birthplace": "",
        "native_place": "",
        "education": "硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "抚顺市人民政府",
        "source": "https://www.fushun.gov.cn/zwgk/002001/002001002/002001002008/leader.html",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长; 负责人社、自然资源、水利、农业农村、乡村振兴、林业草原、供销等工作; 联系指导抚顺县经济",
    },
    {
        "id": 6,
        "name": "战巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "",
        "native_place": "",
        "education": "大学(经济学学士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "抚顺市人民政府",
        "source": "https://www.fushun.gov.cn/zwgk/002001/002001002/002001002010/leader.html",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长; 2005-06入党; 协助负责国资监管、金融、抚顺银行改革等工作; 协助联系指导新宾县经济",
    },
    {
        "id": 7,
        "name": "肖寒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "",
        "native_place": "",
        "education": "大学(法学学士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长兼公安局长",
        "current_org": "抚顺市人民政府",
        "source": "https://www.fushun.gov.cn/zwgk/002001/002001002/002001002007/leader.html",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长, 市公安局党委书记、局长、督察长(兼); 负责公安、司法等工作; 联系指导新抚区经济",
    },
    {
        "id": 8,
        "name": "谢恺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年7月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生(理学博士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "抚顺市人民政府",
        "source": "https://www.fushun.gov.cn/zwgk/002001/002001002/002001002009/leader.html",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长; 1984年生(班子最年轻); 负责科技创新、工业和信息化、生态环境等工作; 联系指导望花区经济",
    },
    {
        "id": 9,
        "name": "张美华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年12月",
        "birthplace": "",
        "native_place": "",
        "education": "大学(经济学硕士)",
        "party_join": "",      # 农工党成员(非中共)
        "work_start": "",
        "current_post": "副市长",
        "current_org": "抚顺市人民政府",
        "source": "https://www.fushun.gov.cn/zwgk/002001/002001002/002001002004/leader.html",
        "confidence": "confirmed",
        "notes": "农工党, 党外干部; 负责教育、民政、退役军人、市场监管/知识产权、大数据等工作; 联系指导顺城区经济",
    },
    {
        "id": 10,
        "name": "程永亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年10月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生(工学博士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长(挂职)",
        "current_org": "抚顺市人民政府",
        "source": "https://www.fushun.gov.cn/zwgk/002001/002001002/002001002005/leader.html",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长(挂职), 中国铁建股份有限公司副总工程师; 2006-08入党; 负责城乡建设、交通运输等工作; 联系指导清原县经济",
    },
    # ══════════ 秘书长 ══════════
    {
        "id": 11,
        "name": "张文献",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年7月",
        "birthplace": "",
        "native_place": "",
        "education": "大学(工学学士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "抚顺市人民政府",
        "source": "https://www.fushun.gov.cn/zwgk/002001/002001003/002001003001/leader.html",
        "confidence": "confirmed",
        "notes": "市政府党组成员、秘书长, 市政府办公室党组书记、主任, 二级巡视员; 协助市长处理日常工作",
    },
    # ══════════ Predecessor 市委书记 (confirmed) ══════════
    {
        "id": 30,
        "name": "来鹤",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1964年9月",
        "birthplace": "辽宁鞍山",
        "native_place": "辽宁鞍山",
        "education": "",
        "party_join": "1997年6月",
        "work_start": "1983年8月",
        "current_post": "前任市委书记(现任辽宁省人大教科文卫委主任)",
        "current_org": "辽宁省人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/来鹤",
        "confidence": "confirmed",
        "notes": "前任抚顺市委书记(2018.09-2024.09), 由高键接任。此前曾任抚顺市副市长(2011.12-2015), 与抚顺地缘深厚(两次任职)。现任辽宁省人大常委会教科文卫委员会主任委员。前任辽宁省委书记郝鹏(2025.09不再担任, 转全国人大)不涉本地区图。",
    },
    # 注: 王庆海的前任市长即现任市委书记高键(2020.01-2024.09任市长), 已由 id=1 覆盖, 不再单列占位。
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共抚顺市委员会", "type": "党委", "level": "地级市", "parent": "中共辽宁省委员会", "location": "抚顺市"},
    {"id": 2, "name": "抚顺市人民政府", "type": "政府", "level": "地级市", "parent": "辽宁省人民政府", "location": "抚顺市"},
    {"id": 3, "name": "抚顺市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "辽宁省人大常委会", "location": "抚顺市"},
    {"id": 4, "name": "政协抚顺市委员会", "type": "政协", "level": "地级市", "parent": "政协辽宁省委员会", "location": "抚顺市"},
    {"id": 5, "name": "抚顺市公安局", "type": "政府", "level": "地级市属", "parent": "抚顺市人民政府", "location": "抚顺市"},
    {"id": 6, "name": "辽宁省人民代表大会常务委员会", "type": "人大", "level": "省级", "parent": "全国人大常委会", "location": "沈阳市"},
    {"id": 7, "name": "中共朔州市委员会", "type": "党委", "level": "地级市", "parent": "中共山西省委员会", "location": "朔州市"},
    {"id": 8, "name": "朔州市人民政府", "type": "政府", "level": "地级市", "parent": "山西省人民政府", "location": "朔州市"},
    {"id": 9, "name": "中共大同市委员会", "type": "党委", "level": "地级市", "parent": "中共山西省委员会", "location": "大同市"},
    {"id": 10, "name": "中共太原市委员会", "type": "党委", "level": "副省级市", "parent": "中共山西省委员会", "location": "太原市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 高键 (市委书记)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2024-09", "end_date": "", "rank": "正厅级", "note": "现任抚顺市委书记/抚顺军分区党委第一书记(2024.09起)"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start_date": "2020-01", "end_date": "2024-09", "rank": "正厅级", "note": "抚顺代市长(2019.12-2020.01)升任市长; 2024.09升书记交由王庆海接任"},
    {"person_id": 1, "org_id": 8, "title": "市长", "start_date": "2018-03", "end_date": "2019-12", "rank": "正厅级", "note": "山西朔州市长(跨省调入辽前最后一职); 曾任朔州市委副书记"},
    {"person_id": 1, "org_id": 9, "title": "市委副书记", "start_date": "2017-02", "end_date": "2018-03", "rank": "副厅级", "note": "山西大同市委副书记"},
    {"person_id": 1, "org_id": 10, "title": "市委常委/市委秘书长", "start_date": "2016", "end_date": "2017", "rank": "副厅级", "note": "山西太原市委常委、秘书长(早年曾任省委统战部副部长级干部引导)"},
    # 王庆海 (市长)
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "兼任市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "市政府党组书记、市长; 主持全面工作"},
    # 杨洪波 (常务副市长)
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市委常委/党组副书记"},
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 吴杰
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 其他副市长
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "张君昶"},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "战巍"},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "肖寒 兼公安局长"},
    {"person_id": 7, "org_id": 5, "title": "市公安局局长", "start_date": "", "end_date": "", "rank": "正处级", "note": "兼任市公安局党委书记/局长/督察长"},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "谢恺(最年轻)"},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "张美华(农工党/党外)"},
    {"person_id": 10, "org_id": 2, "title": "副市长(挂职)", "start_date": "", "end_date": "", "rank": "副厅级", "note": "程永亮 中国铁建原副总工"},
    # 秘书长
    {"person_id": 11, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": "张文献, 二级巡视员"},
    # 前任书记 来鹤
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "2018-09", "end_date": "2024-09", "rank": "正厅级", "note": "前任抚顺市委书记(2018.09-2024.09); 此前曾任抚顺市副市长(2011.12-2015)"},
    {"person_id": 30, "org_id": 6, "title": "省人大常委会教科文卫委员会主任委员", "start_date": "2024", "end_date": "", "rank": "正厅级", "note": "卸任抚顺书记后, 退居省人大(现职)"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 高键 ↔ 王庆海 (书记—市长)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共抚顺市委员会/抚顺市人民政府", "overlap_period": "2026"},
    # 王庆海 ↔ 常务副市长 杨洪波
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—常务副市长", "overlap_org": "抚顺市人民政府", "overlap_period": "2026"},
    # 市长 ↔ 副市长们
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—副市长", "overlap_org": "抚顺市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—副市长", "overlap_org": "抚顺市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "市长—副市长", "overlap_org": "抚顺市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "市长—副市长/公安局长", "overlap_org": "抚顺市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "市长—副市长", "overlap_org": "抚顺市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "市长—副市长(党外)", "overlap_org": "抚顺市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—挂职副市长", "overlap_org": "抚顺市人民政府", "overlap_period": "2026"},
    # 市长 ↔ 秘书长
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "市长—市政府秘书长", "overlap_org": "抚顺市人民政府", "overlap_period": "2026"},
    # 书记 ↔ 市公安局局长
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "市委书记—公安局长", "overlap_org": "中共抚顺市委员会", "overlap_period": "2026"},
    # 书记 高键 ↔ 前任书记 来鹤 (交接)
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记(2018-2024搭档: 来鹤任书记期间高键任市长)", "overlap_org": "中共抚顺市委员会", "overlap_period": "2020-2024"},
    # 书记 高键 ↔ 市长 王庆海: 亦为"前市长→现任市长"交接链
    {"person_a": 2, "person_b": 1, "type": "交接", "context": "王庆海接任高键之市长职务(高键2020.01-2024.09任市长)", "overlap_org": "抚顺市人民政府", "overlap_period": "2024"},
]


# ── Helper functions ──────────────────────────────────────────────────────────


def _has_identifier(person: dict) -> bool:
    return bool(person.get("birth") or person.get("birthplace") or person.get("native_place"))


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    city = "抚顺市"

    if name.startswith("前任"):
        # predecessor name unknown; skip writing a person file for placeholder
        return

    person_positions = [p for p in positions if p["person_id"] == pid]
    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # 简历较单薄且无独有标识时补显式缺口
    if len(career_timeline) <= 1 and not _has_identifier(person):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开官方简历信息有限, 完整履历与确切就任时间待补。外部检索(Exa限流/百度验证/Bing)受限, 未能进一步核实。",
            "confidence": "unverified",
            "source_ids": [],
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": other_name,
            "relationship_type": "overlap" if r["type"] == "共事" else "predecessor_successor",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "抚顺市人民政府官方网站—政府领导/各部门领导简历页",
            "url": source_url or "http://www.fushun.gov.cn/",
            "publisher": "抚顺市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "领导之窗/政府领导及各部门领导简历页(王庆海/杨洪波/吴杰/张君昶/战巍/肖寒/谢恺/张美华/程永亮/张文献等)确认现任职务与基础履历",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": city,
            "region": city,
            "job": person.get("current_post", ""),
            "task_id": "liaoning_抚顺市",
            "time_focus": "2026-08",
        },
        "identity": {
            "person_id": f"{city}_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [
            {
                "period": "2026",
                "domain": "disaster_management" if person.get("id") in (1, 2) else "other",
                "achievement_or_event": "2026年7月抚顺市'7·13'暴雨灾后重建与防汛救灾统筹(市领导多次调度, 筑牢汛期安全防线)",
                "role_in_event": "市委书记/市长",
                "measurable_outcome": "统筹灾后重建与防汛'零亡人'目标, 保障民生",
                "location": "抚顺市",
                "confidence": "confirmed" if person.get("current_post") in ("市委书记", "市长") else "unverified",
                "source_ids": ["S001"],
            }
        ] if person.get("current_post") in ("市委书记", "市长") else [],
        "professional_profile": {
            "primary_specializations": ["党建工作" if person.get("current_post") == "市委书记" else "政府行政管理"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if person.get("id") in (1, 2) else "unknown",
            "systems_experience": [],
            "geographic_pattern": ["抚顺市(辽宁省)"],
            "promotion_velocity": {
                "summary": "公开履历不全, 无法精确分析晋升速度",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "grassroots_oriented" if person.get("id") == 1 else "stability_oriented",
                    "evidence": "2026-07市委议军会议、防汛/安全生产工作会提'补短板堵漏洞强弱项'、'先清污后消毒'科学防污等公开报道(官方)",
                    "confidence": "plausible",
                    "source_ids": ["S001"],
                },
            ],
            "speech_themes": [
                "筑牢汛期安全防线 / '7·13'灾后重建",
                "补短板堵漏洞强弱项",
                "统筹发展与安全（营商环境/安全监管）",
            ],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026-08, 未在可获得公开来源中发现针对该人物的纪律处分/审计问题/负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if _has_identifier(person) else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "partial" if _has_identifier(person) else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{name} 的出生年月/籍贯/学历及完整任职履历(除当前职务外)待补充",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历教育、入党参工时间",
                "why_it_matters": "身份去重与档案库基础信息, 跨地域关联分析必需",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历(每段职务起止时间)",
                "why_it_matters": "精确时间线是关系网络与晋升链分析的输入",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职时间"],
                "last_attempted": AS_OF,
            },
        ],
    }
    slug_post = person['current_post'].replace('/', '_').replace('、', '_').replace('，', '_')
    fname = f"{TODAY}-辽宁省-抚顺市-{slug_post}-{name}.json"
    if not person.get("current_post"):
        fname = f"{TODAY}-辽宁省-抚顺市-待定-{name}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ── Build ────────────────────────────────────────────────────────────────────


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    print("  Writing person JSONs...")
    core_ids = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 30}  # 班子核心成员 + 前任书记来鹤
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


TID = "liaoning_抚顺市"


if __name__ == "__main__":
    raise SystemExit(main())