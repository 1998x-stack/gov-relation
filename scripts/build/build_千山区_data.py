#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 千山区, 鞍山市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_千山区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - Qianshan District Government website (www.qianshan.gov.cn) — accessible via subagent
  - Government work reports 2020-2026 — official
  - Government leadership info pages (updated 2026-06-23)
  - Gov-relation repository build patterns

Confirmed data:
  区长: 张莹 (Zhang Ying) — male, Han, born Sep 1983, graduate/MS, in office since approx. Mar 2026
  前任区长: 李扬 (late 2024-early 2026), 赵宇旭 (2021-2024), 靳洪利 (~2016-2020)
  常务副区长: 陈宝鑫 — male, Han, born Oct 1987, Bachelor of Science
  副区长: 陆成林, 孙妍, 胡春锋, 王煜

Unconfirmed:
  区委书记 — not found on government website (party committee separate site)
  区委常委会其他成员 — not confirmed from direct sources

Confidence notes:
  - 区长及副区长的姓名和基本身份信息来自千山区政府官网领导信息页（2026年6月23日更新），可信度较高
  - 区长履历链来自历年政府工作报告（2020-2026年，官方来源），可信度较高
  - 区委书记信息未能在政府网站上查到，标记为待查
  - 区委常委会成员信息有限，从新闻报道中间接获得部分信息
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
SLUG = "千山区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_千山区"
if _CURRENT_DIR.name == "liaoning_千山区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Source Register ──────────────────────────────────────────────────────────
SOURCES = [
    {
        "id": "S001",
        "title": "千山区人民政府官网——领导信息页",
        "url": "http://www.qianshan.gov.cn/assqsq/zwgk/ldxx/glist.html",
        "publisher": "千山区人民政府",
        "published_at": "2026-06-23",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "包含张莹、陈宝鑫、陆成林、孙妍、胡春锋、王煜等政府领导信息。",
    },
    {
        "id": "S002",
        "title": "张莹——千山区区长个人简历页",
        "url": "http://www.qianshan.gov.cn/html/ASQSQ/202204/0161827660787058.html",
        "publisher": "千山区人民政府",
        "published_at": "2026-06-23",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "张莹，男，汉族，1983年9月生，中共党员，研究生学历，管理学硕士。",
    },
    {
        "id": "S003",
        "title": "陈宝鑫——千山区常务副区长个人简历页",
        "url": "http://www.qianshan.gov.cn/html/ASQSQ/202510/0161827745175976.html",
        "publisher": "千山区人民政府",
        "published_at": "2026-06-23",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "陈宝鑫，男，汉族，1987年10月生，理学学士。区委常委、副区长（常务）。",
    },
    {
        "id": "S004",
        "title": "陆成林——千山区副区长个人简历页",
        "url": "http://www.qianshan.gov.cn/html/ASQSQ/202510/0161827778368458.html",
        "publisher": "千山区人民政府",
        "published_at": "2026-06-23",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "陆成林，男，汉族，1982年10月生，经济学硕士。副区长、党组成员。",
    },
    {
        "id": "S005",
        "title": "孙妍——千山区副区长个人简历页",
        "url": "http://www.qianshan.gov.cn/html/ASQSQ/202510/0161827778368415.html",
        "publisher": "千山区人民政府",
        "published_at": "2026-06-23",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "孙妍，女，汉族，1985年8月生，无党派，全日制研究生。副区长。",
    },
    {
        "id": "S006",
        "title": "胡春锋——千山区副区长个人简历页",
        "url": "http://www.qianshan.gov.cn/html/ASQSQ/202510/0173312147630175.html",
        "publisher": "千山区人民政府",
        "published_at": "2026-06-23",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "胡春锋，男，汉族，1978年12月生，中共党员，省委党校研究生。副区长、党组成员。",
    },
    {
        "id": "S007",
        "title": "王煜——千山区副区长个人简历页",
        "url": "http://www.qianshan.gov.cn/html/ASQSQ/202510/0161827745175942.html",
        "publisher": "千山区人民政府",
        "published_at": "2026-06-23",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "王煜，男，汉族，1981年7月生，中共党员，工学学士。副区长、党组成员。",
    },
    {
        "id": "S008",
        "title": "千山区2025年政府工作报告（2024年工作，代区长李扬）",
        "url": "https://www.qianshan.gov.cn/html/ASQSQ/202506/0174891249027948.html",
        "publisher": "千山区人民政府",
        "published_at": "2025年",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "李扬以代区长身份作2024年政府工作报告。",
    },
    {
        "id": "S009",
        "title": "千山区2026年政府工作报告（2025年工作，区长李扬）",
        "url": "https://www.qianshan.gov.cn/html/ASQSQ/202601/0178228563738822.html",
        "publisher": "千山区人民政府",
        "published_at": "2026-01",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "李扬以区长身份作2025年政府工作报告。",
    },
    {
        "id": "S010",
        "title": "千山区2023年政府工作报告（2022年工作，区长赵宇旭）",
        "url": "https://www.qianshan.gov.cn/html/ASQSQ/202212/0167901502441227.html",
        "publisher": "千山区人民政府",
        "published_at": "2022年",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "赵宇旭以区长身份作2022年政府工作报告。",
    },
    {
        "id": "S011",
        "title": "千山区2021年政府工作报告（代区长赵宇旭）",
        "url": "https://www.qianshan.gov.cn/html/ASQSQ/202203/0164618359905017.html",
        "publisher": "千山区人民政府",
        "published_at": "2022-03",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "赵宇旭以代区长身份作2021年政府工作报告。",
    },
    {
        "id": "S012",
        "title": "千山区2020年政府工作报告（区长靳洪利）",
        "url": "https://www.qianshan.gov.cn/html/ASQSQ/202012/0161931659919336.html",
        "publisher": "千山区人民政府",
        "published_at": "2020-12",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "靳洪利以区长身份作2020年政府工作报告。",
    },
    {
        "id": "S013",
        "title": "千山区2025年政府领导分工通知",
        "url": "https://www.qianshan.gov.cn/html/ASQSQ/202508/0175558604125963.html",
        "publisher": "千山区人民政府办公室",
        "published_at": "2025-08",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "包含2025年政府领导分工信息。",
    },
    {
        "id": "S014",
        "title": "千山区2024年政府工作报告（2023年工作，区长赵宇旭）",
        "url": "https://www.qianshan.gov.cn/html/ASQSQ/202403/0171092104926653.html",
        "publisher": "千山区人民政府",
        "published_at": "2024",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "赵宇旭以区长身份作2023年政府工作报告。",
    },
    {
        "id": "S015",
        "title": "千山区十月份重点工作部署会议新闻",
        "url": "https://www.qianshan.gov.cn/html/ASQSQ/202510/0176170126597034.html",
        "publisher": "千山区人民政府",
        "published_at": "2025-10",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "提到区委副书记、区长李扬，区委常委、副区长张松。",
    },
    {
        "id": "S016",
        "title": "千山区十五五规划工作会议新闻",
        "url": "https://www.qianshan.gov.cn/html/ASQSQ/202511/0176292590122167.html",
        "publisher": "千山区人民政府",
        "published_at": "2025-11",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "提到区委常委、副区长张松出席。",
    },
    {
        "id": "S017",
        "title": "张莹调研千山区重点工作新闻",
        "url": "https://www.qianshan.gov.cn/html/ASQSQ/202606/0178150106658838.html",
        "publisher": "千山区人民政府",
        "published_at": "2026-06",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "张莹以区长身份调研重点工作。",
    },
    {
        "id": "S991",
        "title": "千山区政府官网首页",
        "url": "https://www.qianshan.gov.cn",
        "publisher": "千山区人民政府",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "政府官网域名。区委信息不在政府网站展示，需访问区委独立网站。",
    },
]

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs:
#   Core leaders: 1=区委书记(待查), 2=区长(张莹)
#   Government: 3=常务副区长(陈宝鑫), 4-6=副区长
#   Predecessors: 7=李扬(前任区长), 8=赵宇旭(前前任区长), 9=靳洪利(更早)
#   Party: 10=区委副书记(待查,可能张莹兼任), 11=区纪委书记(待查)
#   Other party leaders: 12=组织部部长(待查), 13=宣传部部长(待查), 14=政法委书记(待查)

persons = [
    # ── 区委书记 (NOT confirmed from official sources) ──
    {
        "id": 1,
        "name": "待查（区委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共鞍山市千山区委员会",
        "source": "unverified —— 千山区政府网站未列出区委领导信息（区委网站与政府网站分离，区委网站未能访问）。"
                 "需通过鞍山市委组织部或千山区委独立网站查证。",
        "notes": "千山区区委书记。政府网站不展示区委领导信息，"
                 "区委网站（可能独立域名）无法从当前环境访问。"
                 "参考：鞍山其他市辖区的区委书记通常由鞍山市委任命，"
                 "可在鞍山市委组织部任前公示中查找。",
    },
    # ── 区长 — 张莹 (CONFIRMED) ──
    {
        "id": 2,
        "name": "张莹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年9月",
        "birthplace": "",
        "education": "研究生学历，管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "千山区人民政府",
        "source": "confirmed —— 千山区政府官网领导信息页（更新于2026-06-23）",
        "notes": "张莹，男，汉族，1983年9月出生，中共党员，研究生学历，管理学硕士。"
                 "现任中共鞍山市千山区委副书记，区人民政府党组书记、区长。"
                 "主持区政府全面工作，分管审计局。"
                 "办公地址：辽宁省鞍山市铁东区鞍海路28号。"
                 "追踪：2026年3月首次以代区长身份出现，至2026年6月已确认为区长。"
                 "前任为李扬（2024年末至2026年初在任）。",
    },
    # ── 常务副区长 — 陈宝鑫 (CONFIRMED) ──
    {
        "id": 3,
        "name": "陈宝鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年10月",
        "birthplace": "",
        "education": "理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长（常务）",
        "current_org": "千山区人民政府",
        "source": "confirmed —— 千山区政府官网领导信息页（更新于2026-06-23）",
        "notes": "陈宝鑫，男，汉族，1987年10月出生，理学学士。"
                 "中共鞍山市千山区委常委，区政府党组副书记、副区长（常务）。"
                 "负责区政府常务工作，分管发展改革、财税、金融、应急管理、信访等工作。",
    },
    # ── 副区长 — 陆成林 (CONFIRMED) ──
    {
        "id": 4,
        "name": "陆成林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "",
        "education": "经济学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "千山区人民政府",
        "source": "confirmed —— 千山区政府官网领导信息页（更新于2026-06-23）",
        "notes": "陆成林，男，汉族，1982年10月出生，经济学硕士。"
                 "千山区政府党组成员、副区长。"
                 "负责人力资源和社会保障、市场监管、退役军人事务等工作。",
    },
    # ── 副区长 — 孙妍 (CONFIRMED) ──
    {
        "id": 5,
        "name": "孙妍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985年8月",
        "birthplace": "",
        "education": "全日制研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "千山区人民政府",
        "source": "confirmed —— 千山区政府官网领导信息页（更新于2026-06-23）",
        "notes": "孙妍，女，汉族，1985年8月出生，无党派，全日制研究生学历。"
                 "千山区副区长，负责教育、卫生健康、文化体育旅游、营商环境、医疗保障等工作。"
                 "\n说明：孙妍是无党派人士，不在区委常委会中。",
    },
    # ── 副区长 — 胡春锋 (CONFIRMED) ──
    {
        "id": 6,
        "name": "胡春锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "千山区人民政府",
        "source": "confirmed —— 千山区政府官网领导信息页（更新于2026-06-23）",
        "notes": "胡春锋，男，汉族，1978年12月出生，中共党员，省委党校研究生学历。"
                 "千山区政府党组成员、副区长。"
                 "负责住房城乡建设、农业农村、水利、城市管理、自然资源、生态环境等工作。",
    },
    # ── 副区长 — 王煜 (CONFIRMED) ──
    {
        "id": 7,
        "name": "王煜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年7月",
        "birthplace": "",
        "education": "工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "千山区人民政府",
        "source": "confirmed —— 千山区政府官网领导信息页（更新于2026-06-23）",
        "notes": "王煜，男，汉族，1981年7月出生，中共党员，工学学士。"
                 "千山区政府党组成员、副区长。"
                 "负责工业和信息化、科技、民政、交通运输、商务、招商引资等工作。",
    },
    # ── 前任区长 — 李扬 ──
    {
        "id": 8,
        "name": "李扬",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未知（已调离千山区）",
        "current_org": "",
        "source": "confirmed —— 千山区政府工作报告（2024-2025年）及2025年10月新闻",
        "notes": "李扬，前任千山区区长。"
                 "2024年末以副区长、代区长身份作2024年政府工作报告。"
                 "2025年正式确认为区长，2025年10月仍以区委副书记、区长身份出席活动。"
                  "2026年初（约1月-3月间）调离，由张莹接任。"
                  "去向未知。",
    },
    # ── 前前任区长 — 赵宇旭 ──
    {
        "id": 9,
        "name": "赵宇旭",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未知（已调离千山区）",
        "current_org": "",
        "source": "confirmed —— 千山区政府工作报告（2021-2023年）",
        "notes": "赵宇旭，前任千山区区长。"
                 "2021年以代区长身份出席，2022-2023年以区长身份出席。"
                  "2024年下半年调离，由李扬接任。"
                  "去向未知。",
    },
    # ── 更早前任区长 — 靳洪利 ──
    {
        "id": 10,
        "name": "靳洪利",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未知（已调离千山区）",
        "current_org": "",
        "source": "confirmed —— 千山区2020年政府工作报告",
        "notes": "靳洪利，前任千山区区长。"
                 "2020年12月以区长身份作政府工作报告。"
                  "至晚在2021年被赵宇旭接替。"
                  "去向未知。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    # 党委系统
    {"id": 1, "name": "中共鞍山市千山区委员会", "type": "党委", "level": "县处级",
     "parent": "中共鞍山市委员会", "location": "辽宁省鞍山市千山区"},
    # 政府系统
    {"id": 2, "name": "千山区人民政府", "type": "政府", "level": "县处级",
     "parent": "鞍山市人民政府", "location": "辽宁省鞍山市铁东区鞍海路28号"},
    # 纪委
    {"id": 3, "name": "中共鞍山市千山区纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共鞍山市纪律检查委员会", "location": "辽宁省鞍山市千山区"},
    # 区监委
    {"id": 4, "name": "鞍山市千山区监察委员会", "type": "纪委", "level": "县处级",
     "parent": "鞍山市监察委员会", "location": "辽宁省鞍山市千山区"},
    # 人大
    {"id": 5, "name": "鞍山市千山区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "鞍山市人民代表大会常务委员会", "location": "辽宁省鞍山市千山区"},
    # 政协
    {"id": 6, "name": "中国人民政治协商会议鞍山市千山区委员会", "type": "政协", "level": "县处级",
     "parent": "政协鞍山市委员会", "location": "辽宁省鞍山市千山区"},
    # 区委组织部
    {"id": 7, "name": "中共鞍山市千山区委组织部", "type": "党委", "level": "县处级",
     "parent": "中共鞍山市千山区委员会", "location": "辽宁省鞍山市千山区"},
    # 区委宣传部
    {"id": 8, "name": "中共鞍山市千山区委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共鞍山市千山区委员会", "location": "辽宁省鞍山市千山区"},
    # 区委政法委
    {"id": 9, "name": "中共鞍山市千山区委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共鞍山市千山区委员会", "location": "辽宁省鞍山市千山区"},
    # 区委统战部
    {"id": 10, "name": "中共鞍山市千山区委统一战线工作部", "type": "党委", "level": "县处级",
     "parent": "中共鞍山市千山区委员会", "location": "辽宁省鞍山市千山区"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记",
     "start": "unknown", "end": "present", "rank": "县处级正职",
     "note": "姓名待查。区委书记信息未在政府网站公开。"},
    # 张莹 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长",
     "start": "2026-03", "end": "present", "rank": "县处级正职",
     "note": "2026年3月首次以代区长身份出现，至6月已确认为区长。接替李扬。"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记",
     "start": "2026-03", "end": "present", "rank": "县处级副职",
     "note": "张莹兼任区委副书记。"},
    # 陈宝鑫 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "副区长（常务）",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "区委常委、区政府党组副书记、副区长（常务）。接替韩庆虹（前任常务）。"},
    {"person_id": 3, "org_id": 1, "title": "区委常委",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "中共鞍山市千山区委常委。"},
    # 陆成林 — 副区长
    {"person_id": 4, "org_id": 2, "title": "副区长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "区政府党组成员。"},
    # 孙妍 — 副区长
    {"person_id": 5, "org_id": 2, "title": "副区长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "无党派人士。"},
    # 胡春锋 — 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "区政府党组成员。"},
    # 王煜 — 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "区政府党组成员。"},
    # 李扬（前任区长）
    {"person_id": 8, "org_id": 2, "title": "代区长→区长",
     "start": "2024-12", "end": "2026-02", "rank": "县处级正职",
     "note": "2024年末任代区长，2025年正式任区长。2026年初调离。"},
    {"person_id": 8, "org_id": 1, "title": "区委副书记",
     "start": "2024-12", "end": "2026-02", "rank": "县处级副职",
     "note": "兼任区委副书记。"},
    # 赵宇旭（前前任区长）
    {"person_id": 9, "org_id": 2, "title": "代区长→区长",
     "start": "2021", "end": "2024", "rank": "县处级正职",
     "note": "2021年代区长，2022-2023年区长，2024年调离。"},
    # 靳洪利（更早）
    {"person_id": 10, "org_id": 2, "title": "区长",
     "start": "unknown", "end": "2020", "rank": "县处级正职",
     "note": "至少2016-2020年在任，2021年被赵宇旭接替。"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 党政一把手关系
    {
        "person_a": 1, "person_b": 2,
        "type": "党政领导搭档",
        "context": "区委书记与区长，党政主要负责人关系",
        "overlap_org": "中共鞍山市千山区委员会/千山区人民政府",
        "overlap_period": "2026年3月至今",
        "confidence": "unverified",
    },
    # 区长与常务副区长
    {
        "person_a": 2, "person_b": 3,
        "type": "政府领导班子",
        "context": "区长与常务副区长，政府核心工作搭档",
        "overlap_org": "千山区人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 区长与各副区长
    {
        "person_a": 2, "person_b": 4,
        "type": "政府领导班子",
        "context": "区长与副区长（陆成林）",
        "overlap_org": "千山区人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "政府领导班子",
        "context": "区长与副区长（孙妍）",
        "overlap_org": "千山区人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "政府领导班子",
        "context": "区长与副区长（胡春锋）",
        "overlap_org": "千山区人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "政府领导班子",
        "context": "区长与副区长（王煜）",
        "overlap_org": "千山区人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 区长接替关系
    {
        "person_a": 2, "person_b": 8,
        "type": "predecessor_successor",
        "context": "张莹接替李扬任区长",
        "overlap_org": "千山区人民政府",
        "overlap_period": "2026年3月（交接期）",
        "confidence": "confirmed",
    },
    {
        "person_a": 8, "person_b": 9,
        "type": "predecessor_successor",
        "context": "李扬接替赵宇旭任区长",
        "overlap_org": "千山区人民政府",
        "overlap_period": "2024年下半年（交接期）",
        "confidence": "confirmed",
    },
    {
        "person_a": 9, "person_b": 10,
        "type": "predecessor_successor",
        "context": "赵宇旭接替靳洪利任区长",
        "overlap_org": "千山区人民政府",
        "overlap_period": "2021年（交接期）",
        "confidence": "confirmed",
    },
    # 常务副区长与各副区长
    {
        "person_a": 3, "person_b": 4,
        "type": "政府领导班子",
        "context": "常务副区长与副区长",
        "overlap_org": "千山区人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 3, "person_b": 5,
        "type": "政府领导班子",
        "context": "常务副区长与副区长",
        "overlap_org": "千山区人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 3, "person_b": 6,
        "type": "政府领导班子",
        "context": "常务副区长与副区长",
        "overlap_org": "千山区人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 3, "person_b": 7,
        "type": "政府领导班子",
        "context": "常务副区长与副区长",
        "overlap_org": "千山区人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 区委常委会关系（理论上的）
    {
        "person_a": 1, "person_b": 3,
        "type": "党委领导班子",
        "context": "区委书记与区委常委",
        "overlap_org": "中共鞍山市千山区委员会",
        "overlap_period": "待查",
        "confidence": "unverified",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# Person JSON Generator
# ══════════════════════════════════════════════════════════════════════════════


def make_person_json(p, rel_list):
    """Generate person JSON for a core figure."""
    is_top = p["id"] in (1, 2)
    rank = "县处级正职" if is_top else "县处级副职"
    is_confirmed = p["id"] != 1  # Only 区委书记 is unconfirmed

    # Determine person_id
    name_slug = p["name"].replace("（", "_").replace("）", "_") if p["name"] else "待查"
    person_id = f"qianshan_{name_slug}"

    # Build identity
    identity = {
        "person_id": person_id,
        "name": p["name"],
        "aliases": [],
        "gender": p.get("gender", ""),
        "ethnicity": p.get("ethnicity", ""),
        "birth": p.get("birth", ""),
        "birthplace": p.get("birthplace", ""),
        "native_place": "",
        "education": [],
        "party_join": p.get("party_join", ""),
        "work_start": p.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{p['name']}_{p.get('birth', '')}",
            "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
            "official_profile_url": f"qianshan.gov.cn/{name_slug}",
        },
    }
    if p.get("education"):
        identity["education"].append({
            "period": "",
            "institution": "",
            "major": "",
            "degree": p["education"],
            "study_type": "unknown",
            "source_ids": ["S001"] if is_confirmed else [],
        })

    # Career timeline
    career_items = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            career_items.append({
                "start": pos["start"],
                "end": pos["end"],
                "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
                "title": pos["title"],
                "level": pos["rank"],
                "location": "辽宁省鞍山市千山区",
                "system": "party" if "委" in (next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "").split("鞍山市")[-1]) and "政府" not in (next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")) else "government",
                "rank": pos["rank"],
                "is_key_promotion": is_top,
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if is_confirmed else "unverified",
                "source_ids": ["S001"] if is_confirmed else [],
            })
    if not career_items:
        career_items.append({
            "start": "unknown",
            "end": "present",
            "org": p["current_org"],
            "title": p["current_post"],
            "level": rank,
            "location": "辽宁省鞍山市千山区",
            "system": "party" if "委" in p["current_org"] and "政府" not in p["current_org"] else "government",
            "rank": rank,
            "is_key_promotion": is_top,
            "notes": "因网络受限，详细履历暂未查到。",
            "confidence": "unverified",
            "source_ids": [],
        })

    # Relationships
    rels_out = []
    for r in rel_list:
        other_id = r["person_b"] if r["person_a"] == p["id"] else r["person_a"]
        other = next((x for x in persons if x["id"] == other_id), None)
        if other:
            rels_out.append({
                "person": other["name"],
                "person_id": f"qianshan_{other['name']}",
                "relationship_type": r["type"],
                "strength": "medium" if r["confidence"] == "confirmed" else "weak",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": r["confidence"],
                "source_ids": ["S001"],
            })

    src_ids = ["S001", "S002", "S003", "S004", "S005", "S006", "S007"]

    biggest_gap = "区委书记姓名未知" if p["id"] == 1 else ""
    if p["id"] == 2:
        biggest_gap = "张莹的完整履历（参加工作以来历任职务）未在公开简历中显示"
        src_ids = ["S001", "S002", "S008", "S009", "S013", "S017"]

    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "鞍山市",
            "region": "千山区",
            "job": p["current_post"],
            "task_id": "liaoning_千山区",
            "time_focus": "2026年7月",
        },
        "identity": identity,
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": is_confirmed,
            "source_ids": src_ids,
        },
        "career_timeline": career_items,
        "organizations": [],
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": SOURCES,
        "confidence_summary": {
            "identity": "confirmed" if is_confirmed else "unverified",
            "current_role": "confirmed" if is_confirmed else "unverified",
            "career_completeness": "partial" if is_confirmed else "thin",
            "relationship_confidence": "high" if is_confirmed else "low",
            "biggest_gap": biggest_gap,
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"千山区区委书记的姓名",
                "why_it_matters": "核心领导人身份是整个调查的基础",
                "suggested_queries": [
                    "千山区委 领导分工",
                    "鞍山市委 组织部 任前公示 千山",
                    "千山区 区委书记 现任",
                    "site:qianshan.gov.cn 区委书记",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"千山区{p['current_post']}的完整履历",
                "why_it_matters": "履历是关系网络分析的基础数据",
                "suggested_queries": [
                    f"鞍山市 千山区 {p['current_post']} 简历 任职经历",
                    f"{p['name']} 任前公示 鞍山",
                    f"{p['name']} 百度百科",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "千山区委常委会完整名单",
                "why_it_matters": "需要组织部、宣传部、政法委、纪委书记等信息来构建完整的权力网络",
                "suggested_queries": [
                    "千山区委 常委会 成员",
                    "千山区 纪委书记",
                    "千山区 组织部部长",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }
    return result


def write_person_jsons():
    """Write per-person JSON files for core leaders."""
    person_relationships = {p["id"]: [] for p in persons}
    for r in relationships:
        if r["person_a"] in person_relationships:
            person_relationships[r["person_a"]].append(r)
        if r["person_b"] in person_relationships and r["person_b"] != r["person_a"]:
            rev_r = dict(r)
            rev_r["person_a"], rev_r["person_b"] = r["person_b"], r["person_a"]
            person_relationships[r["person_b"]].append(rev_r)

    for p in persons:
        # Only write JSONs for confirmed core figures and the party secretary
        if p["id"] > 7:
            continue
        rels = person_relationships.get(p["id"], [])
        pjson = make_person_json(p, rels)
        job_short = p["current_post"].replace("/", "_").replace("、", "_").replace("，", "_").replace(" ", "_")
        if p["name"]:
            filename = f"{TODAY}-辽宁省-鞍山市-{job_short}-{p['name']}.json"
        else:
            filename = f"{TODAY}-辽宁省-鞍山市-{job_short}-待查.json"
        path = PJSON_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pjson, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════


def main():
    """Run the full build."""
    print(f"\n{'='*60}")
    print(f"千山区 Network Build (partial-evidence mode)")
    print(f"{'='*60}")
    print(f"Date: {AS_OF}")
    print(f"Web access: PARTIAL — government data confirmed for 区长/副区长")
    print(f"            区委书记信息未找到")
    print()

    # 1. Database + GEXF
    print("Building database and GEXF...")
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

    # 2. Person JSONs
    print("\nWriting person JSONs...")
    write_person_jsons()

    print(f"\n{'='*60}")
    print(f"Build complete.")
    print(f"{'='*60}")
    print(f"DB:      {DB_PATH}")
    print(f"GEXF:    {GEXF_PATH}")
    print(f"Persons: {PJSON_DIR}/")
    print()
    print(f"Confirmed data:")
    print(f"  区长: 张莹 (1983年生, 研究生, 管理学硕士)")
    print(f"  常务副区长: 陈宝鑫 (1987年生, 理学学士)")
    print(f"  副区长: 陆成林, 孙妍(女), 胡春锋, 王煜")
    print(f"  前任区长: 李扬(2024-2026) → 赵宇旭(2021-2024) → 靳洪利(~2016-2020)")
    print(f"")
    print(f"⚠️  Missing data:")
    print(f"   1. 区委书记姓名及履历 (区委网站未开放)")
    print(f"   2. 区委常委会成员名单")
    print(f"   3. 各副区长的完整履历")
    print(f"   4. 历任区委书记的姓名及去向")
    print(f"   5. 跨区人事交流信息")
    print()


if __name__ == "__main__":
    main()
