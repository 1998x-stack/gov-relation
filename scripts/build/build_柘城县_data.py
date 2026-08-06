#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 柘城县 (Zhecheng County), 河南省商丘市.

Investigation date: 2026-08-06
Task ID: henan_柘城县
Level: 县 (county)
Targets: 县委书记 & 县长

Research sources:
  - 河南省委组织干部任前公示 (河南日报 / 大河网 / 新华网河南) 2024-05-12, 2024-11-18, 2026-04-19
  - 澎湃新闻 / 新京报 / 腾讯新闻 — 柘城县"6.25"武术馆火灾（2021-06）书记梁辉、县长路标免职；王景宇代县长→县长→县委书记；常忠伟任代县长/县长
  - 柘城县人民政府官网 (zhecheng.gov.cn) 要闻动态
  - 河南县域经济网 (sq.henance.com) 柘城新闻 — 2025-2026 现任班子活动报道
  - 百度百科 — 吴杰（柘城县长）词条
  - 商丘市纪委监委官网 (sqlzw.gov.cn / lhlzw.gov.cn) — 柘城县纪委领导机构（监委主任徐永超）
  - 中国日报网 / 大河网 — 柘城考察、县区主要领导调整

Confidence notes:
  - 现任县委书记 邢玉富：身份与现任职务已确认（多重权威来源）；出生年月1979-06来自2024-05-12任前公示
  - 现任县长 常忠伟：2026-05起任县委副书记、代县长，2026-07已正式任县长（柘城融媒体多篇报道确认）；此前任商丘市示范区（豫商经开区）党工委副书记、管委会主任
  - 前任县长 吴杰：2025-01任柘城县长，2026-04-19公示拟任县（市、区）委书记，2026-05调任虞城县委书记（北大百度百科+虞城融媒体确认）
  - 部分常委/副处级干部出生年月与籍贯未公开，已标为 plausible / 缺口，列入 open_questions
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
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
SLUG = "柘城县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "henan_柘城县"
if _CURRENT_DIR.name == "henan_柘城县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 core (书记/县长 current), 3-9 县委领导/常委, 10-14 县政府领导,
#       15-19 人大/政协/纪委, 20+ predecessors

persons = [
    # ═══ Current core leaders ═══
    {
        "id": 1,
        "name": "邢玉富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-06",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共柘城县委员会",
        "source": "https://newpaper.dahe.cn/hnrb/html/2024-05/12/content_12_1666236.htm",
        "confidence": "confirmed",
        "notes": "2024-05-12河南省委组织部任前公示：1979年6月生，省委党校研究生，中共党员，时任鹤壁市鹤山区委副书记、区长，拟任县（市、区）委书记；2024年下半年赴柘城县任县委书记至今（2025-2026多篇官方报道确认）"
    },
    {
        "id": 2,
        "name": "常忠伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "柘城县人民政府",
        "source": "https://sq.henance.com/show-63262.html",
        "confidence": "confirmed",
        "notes": "2026-05-28柘城县政协十一届五次会议以县委副书记、代县长身份出席；2026-07-02县委常委扩大会以县委副书记、县长身份出席；此前任商丘市城乡一体化示范区（豫商经济技术开发区）党工委副书记、管委会主任（2025-11至2026-05商丘示范区报道）"
    },
    # ═══ 县委领导 / 副书记 ═══
    {
        "id": 3,
        "name": "王世伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共柘城县委员会",
        "source": "https://sq.henance.com/show-63898.html",
        "confidence": "plausible",
        "notes": "2026-05-28政协十一届五次会议、2026-07-02县委常委扩大会均以县委副书记身份出席（2026年报道）"
    },
    {
        "id": 4,
        "name": "蒋云兰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记（此前）",
        "current_org": "中共柘城县委员会",
        "source": "https://sq.henance.com/show-61536.html",
        "confidence": "plausible",
        "notes": "2025-09至2025-12多篇县委常委会/廉政会议以县委副书记身份出席；截至2026-05的报道中该职由王世伟担任（交接判断"
    },
    # ═══ 党委常委 / 纪委监委 ═══
    {
        "id": 5,
        "name": "徐永超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共柘城县纪律检查委员会",
        "source": "http://www.sqlzwj.gov.cn/",
        "confidence": "confirmed",
        "notes": "柘城县纪委监委领导机构页面：纪委书记（监委主任）徐永超，副书记梁东、王超；此前一任何永波（2021-2024县纪委书记）"
    },
    {
        "id": 6,
        "name": "冯湛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共柘城县委员会",
        "source": "https://sq.henance.com/show-63822.html",
        "confidence": "plausible",
        "notes": "2025-03校园餐调研、2026年调研报道以县委常委、县委办公室主任身份陪同/出席"
    },
    {
        "id": 7,
        "name": "李传奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "柘城县人民代表大会",
        "source": "https://sq.henance.com/show-63898.html",
        "confidence": "confirmed",
        "notes": "2026-05-28政协会议以县人大常委会党组书记出席，2026-07-02以县人大常委会主任列席县委常委会扩大会议（2026年接任）"
    },
    # ═══ 县政府领导 ═══
    {
        "id": 8,
        "name": "胡鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "柘城县人民政府",
        "source": "https://zhecheng.gov.cn/",
        "confidence": "plausible",
        "notes": "2025-09-30烈士纪念日仪式县委常委、常务副县长主持；2025-03政银合作对接会、2025-12-23县发展保障部门汇报会均以县领导出席"
    },
    {
        "id": 9,
        "name": "张琦祥",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "柘城县人民政府",
        "source": "https://sq.henance.com/show-63822.html",
        "confidence": "plausible",
        "notes": "2025-08-31县长调研生态环境保护、2026-06-25书记调研三资等报道以副县长身份陪同"
    },
    {
        "id": 10,
        "name": "郭伟超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "柘城县人民政府",
        "source": "https://sq.henance.com/show-63987.html",
        "confidence": "plausible",
        "notes": "2026-06-25三资调研、2026-07-16防汛调研以县领导陪同书记"
    },
    {
        "id": 11,
        "name": "王雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "柘城县人民政府",
        "source": "https://sq.henance.com/show-61536.html",
        "confidence": "plausible",
        "notes": "2025-03县政府常务会议副县长出席；2026-07-16防汛调研以县领导陪同"
    },
    {
        "id": 12,
        "name": "刘枫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "柘城县人民政府",
        "source": "https://sq.henance.com/show-61536.html",
        "confidence": "plausible",
        "notes": "2025-03县政府第52次常务会议出席；2025-09灭火救援演练出席"
    },
    {
        "id": 13,
        "name": "梁东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县纪委监委副书记、县监委副主任",
        "current_org": "柘城县监察委员会",
        "source": "http://www.sqlzwj.gov.cn/",
        "confidence": "confirmed",
        "notes": "柘城县纪委监委领导机构名单，监委副书记/副主任"
    },
    # ═══ 人大 / 政协 ═══
    {
        "id": 14,
        "name": "孙文涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协柘城县委员会",
        "source": "https://5g.dahe.cn/news/202205011013555",
        "confidence": "confirmed",
        "notes": "2022-04柘城县政协十一届一次会议当选主席，2026-05-28政协十一届五次会议仍为主席"
    },
    # ═══ 前任县委书记 ═══
    {
        "id": 20,
        "name": "吴杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-10",
        "birthplace": "河南省商丘市夏邑县",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "虞城县委书记（柘城县前县长）",
        "current_org": "中共虞城县委员会",
        "source": "https://baike.baidu.com/item/%E5%90%B4%E6%9D%B0/65229164",
        "confidence": "confirmed",
        "notes": "历任商丘市宁陵县委常委、县委办公室主任→柘城县委常委、常务副县长（2024-11-18公示任县长候选人）→柘城县委副书记、代县长→2025-01-25柘城县十六届人大五次会议当选县长→2026-04-19河南省委选公示拟任县（市、区）委书记→2026-05任虞城县委书记（虞城融媒体2026-05/06/07报道确认）"
    },
    {
        "id": 21,
        "name": "王景宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-10",
        "birthplace": "河南省商丘市梁园区",
        "education": "中央党校研究生（法学理论）",
        "party_join": "中共党员(送公示:1999-08)",
        "work_start": "1995-09",
        "current_post": "前任柘城县委书记",
        "current_org": "",
        "source": "https://www.bjnews.com.cn/detail/162572578414987.html",
        "confidence": "confirmed",
        "notes": "1995-09参加工作，1999-01入党，中央党校法学理论研究生；历任虞城县委组织部干部、商丘市委办公室综合科主任科员/科长/副调研员、民权县副县长、共青团商丘市委书记、夏邑县委副书记（正处级）、商丘市旅游局长、城乡一体化示范区党工委副书记/管委会主任；2021-07任柘城代县长→2021-08-18县委书记；2024年调离（公开活动减少）"
    },
    {
        "id": 22,
        "name": "梁辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记（2021年免）",
        "current_org": "",
        "source": "https://m.bjnews.com.cn/detail/162467606214299.html",
        "confidence": "confirmed",
        "notes": "曾任柘城县长、后任县委书记；2021年6月柘城县远襄镇北街武馆'6·25'重大火灾（18人死亡）被免职"
    },
    {
        "id": 23,
        "name": "路标",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-10",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员(1995-11)",
        "work_start": "1992-09",
        "current_post": "前任柘城县长（2021-06免）",
        "current_org": "",
        "source": "https://m.bjnews.com.cn/detail/162149697214299.html",
        "confidence": "confirmed",
        "notes": "1969-10生，河南大学教育系（1992毕业），历任商丘市委宣传部科长、商丘日报社纪检书记、梁园区委常委、宣传部长、商丘市统计局党组书记、局长等；2014-12起任柘城县委副书记、代县长、县长，2021-06因火灾事故被免职"
    },
    {
        "id": 24,
        "name": "余化敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任柘城县长",
        "current_org": "",
        "source": "https://cn.chinadaily.com.cn/a/202311/08/WS654b3252a310d5acd876de52.html",
        "confidence": "plausible",
        "notes": "2023-11中国日报网报道：柘城县委书记王景宇、县长余化敏率党政考察团赴永城考察；继王景宇后就任（2021-2023/2024任县长），继后由吴杰接任（时间待进一步核实）"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共柘城县委员会", "type": "党委", "level": "县", "parent": "商丘市", "location": "河南省商丘市柘城县"},
    {"id": 2, "name": "柘城县人民政府", "type": "政府", "level": "县", "parent": "商丘市", "location": "河南省商丘市柘城县"},
    {"id": 3, "name": "中共柘城县纪律检查委员会", "type": "纪委监察", "level": "县", "parent": "商丘市", "location": "河南省商丘市柘城县"},
    {"id": 4, "name": "柘城县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "商丘市", "location": "河南省商丘市柘城县"},
    {"id": 5, "name": "政协柘城县委员会", "type": "政协", "level": "县", "parent": "商丘市", "location": "河南省商丘市柘城县"},
    {"id": 6, "name": "中共鹤壁市鹤山区委员会", "type": "党委", "level": "区", "parent": "鹤壁市", "location": "河南省鹤壁市鹤山区"},
    {"id": 7, "name": "鹤壁市鹤山区人民政府", "type": "政府", "level": "区", "parent": "鹤壁市", "location": "河南省鹤壁市鹤山区"},
    {"id": 8, "name": "商丘市城乡一体化示范区（豫商经济技术开发区）", "type": "开发区", "level": "国家级/市", "parent": "商丘市", "location": "河南省商丘市"},
    {"id": 9, "name": "中共虞城县委员会", "type": "党委", "level": "县", "parent": "商丘市", "location": "河南省商丘市虞城县"},
    {"id": 10, "name": "商丘市城乡一体化示范区管委会", "type": "开发区", "level": "市", "parent": "商丘市", "location": "河南省商丘市"},
    {"id": 11, "name": "商丘市旅游局", "type": "政府部门", "level": "市", "parent": "商丘市", "location": "河南省商丘市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # Current
    {"person_id": 1, "org_id": 1, "title": "柘城县委书记", "start_date": "2024", "end_date": "present", "rank": "正处级", "note": "2024年下半年由省委选派赴任（公示2024-05-12），2026年仍在任"},
    {"person_id": 1, "org_id": 6, "title": "鹤壁市鹤山区委副书记、区长", "start_date": "2021-01", "end_date": "2024", "rank": "正处级", "note": "2021-01任鹤山区代区长，后任区长"},
    {"person_id": 2, "org_id": 2, "title": "柘城县长", "start_date": "2026-05", "end_date": "present", "rank": "正处级", "note": "2026-05以代县长出席政协会议，2026-07已任县长"},
    {"person_id": 2, "org_id": 8, "title": "商丘示范区党工委副书记、管委会主任", "start_date": "", "end_date": "2026", "rank": "正处级", "note": "2025-11至2026-05在示范区任职（豫商经开区）"},
    {"person_id": 3, "org_id": 1, "title": "柘城县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026年报道"},
    {"person_id": 4, "org_id": 1, "title": "柘城县委副书记（此前）", "start_date": "", "end_date": "2026", "rank": "正处级", "note": "2025-09至2025-12任县委副书记"},
    {"person_id": 5, "org_id": 3, "title": "县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "现纪委监委领导机构"},
    {"person_id": 6, "org_id": 1, "title": "县委常委、县委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2025-2026报道"},
    {"person_id": 7, "org_id": 4, "title": "县人大常委会主任", "start_date": "2026", "end_date": "present", "rank": "正处级", "note": "2026-05县人大常委会党组书记、2026-07主任"},
    {"person_id": 8, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2025-09主持烈士纪念日仪式"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "县纪委监委副书记、县监委副主任", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    {"person_id": 14, "org_id": 5, "title": "县政协主席", "start_date": "2022-04", "end_date": "present", "rank": "正处级", "note": "2022年政协十一届一次会当选"},
    # Predecessors
    {"person_id": 20, "org_id": 9, "title": "虞城县委书记", "start_date": "2026-05", "end_date": "present", "rank": "正处级", "note": "2026-05调任虞城县委书记"},
    {"person_id": 20, "org_id": 2, "title": "柘城县长", "start_date": "2025-01", "end_date": "2026-05", "rank": "正处级", "note": "2025-01-25县十六届人大五次会议当选"},
    {"person_id": 20, "org_id": 2, "title": "柘城县常务副县长", "start_date": "", "end_date": "2024", "rank": "副处级", "note": "2024-11任前公示（拟历任县长候选人）"},
    {"person_id": 21, "org_id": 1, "title": "柘城县委书记", "start_date": "2021-08", "end_date": "2024", "rank": "正处级", "note": "2021-08-18首次以书记身份亮相；2024年后公开活动减少"},
    {"person_id": 21, "org_id": 2, "title": "柘城县长", "start_date": "2021-07", "end_date": "2021-08", "rank": "正处级", "note": "2021-07代县长、07-18当选县长"},
    {"person_id": 21, "org_id": 10, "title": "商丘示范区管委会主任", "start_date": "2018", "end_date": "2021", "rank": "正处级", "note": "商丘市城乡一体化示范区党工委副书记/管委会主任"},
    {"person_id": 22, "org_id": 1, "title": "柘城县委书记", "start_date": "", "end_date": "2021-06", "rank": "正处级", "note": "2021-06因'6·25'火灾被免职"},
    {"person_id": 23, "org_id": 2, "title": "柘城县长", "start_date": "2014-12", "end_date": "2021-06", "rank": "正处级", "note": "代县长→县长，2021-06因火灾被免职"},
    {"person_id": 24, "org_id": 2, "title": "柘城县长", "start_date": "2021", "end_date": "2023/2024", "rank": "正处级", "note": "2023-11报道仍任县长（王景宇书任前），接任具体时间特考"},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "柘城县党政一把手搭档（2026年邢玉富任书记、常忠伟任县长）", "overlap_org": "柘城县（县委/政府）", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 20, "type": "前任继任", "context": "吴杰任柘城县长期间与邢玉富书记配合，吴杰调任虞城后常忠伟接任县长（党政班子交替）", "overlap_org": "柘城县", "overlap_period": "2024-2026"},
    {"person_a": 20, "person_b": 21, "type": "前任继任", "context": "王景宇任柘城县长/书配；吴杰后任县长，为继任吴杰的县长", "overlap_org": "柘城县", "overlap_period": "2021-2024"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记与纪委书记（全面从严治党履职）", "overlap_org": "中共柘城县委/纪委", "overlap_period": "2024-至今"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "县长与常务副县长的政府班子搭配", "overlap_org": "柘城县政府", "overlap_period": "2026-至今"},
    {"person_a": 7, "person_b": 1, "type": "共事", "context": "人大班子与县委班子（人大主任列席县委常委会）", "overlap_org": "柘城县", "overlap_period": "2026-至今"},
    {"person_a": 21, "person_b": 22, "type": "前任继任", "context": "梁辉被免职后（2021-06），王景宇接任柘城县长/书记（先后任）", "overlap_org": "柘城县", "overlap_period": "2021"},
    {"person_a": 22, "person_b": 23, "type": "前任", "context": "梁辉任书记期间，路标任县长（党政班子）", "overlap_org": "柘城县", "overlap_period": "2014-2021"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "县长与副县长分管工作", "overlap_org": "柘城县政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "县长与副县长", "overlap_org": "柘城县政府", "overlap_period": "2026-至今"},
]


# ── Person JSON writer ───────────────────────────────────────────────────────
_KNOWN_EXTRA_CAREER = {
    "邢玉富": [
        ("2000", "2004", "河南大学行政管理专业学习", "河南大学", "2000-2004"),
        ("", "", "鹤壁经济技术开发区局长", "鹤壁", "早期任鹤壁国家经济技术开发区某局领导"),
        ("2021-01", "2024", "鹤壁市鹤山区委副书记、区长（前代区长）", "鹤壁", "2021-01代区长，后任区长；2024年河南两会代表"),
    ],
    "吴杰": [
        ("", "", "商丘市宁陵县委常委、县委办公室主任", "宁陵", "百度百科称曾任宁陵县委办公室主任；亦见'民权县'交叉表述待核"),
        ("2024-11", "2024", "柘城县委常委、常务副县长（三级调研员）", "柘城", "2024-11-18任前公示拟任县长候选人"),
        ("2025-01", "2026-05", "柘城县委副书记、县长", "柘城", "2025-01-25当选"),
        ("2026-05", "present", "虞城县委书记", "虞城", "2026-04-19公示，05月履新"),
    ],
    "王景宇": [
        ("1995-09", "2021", "商丘市基层+市直（虞城组织部、商丘市委办、商圈共青团、商丘旅游、示范区）", "商丘", "区组织/旅游/示范区"),
        ("2021-07", "2021-08", "柘城代县长→县长", "柘城", "2021-07-07代县长、07-18当选县长"),
        ("2021-08", "2024", "柘城县委书记", "柘城", "2021-08-18首以书记身份亮相；2024年后活跃度下降"),
    ],
    "路标": [
        ("1992-09", "2003", "商运总公司、商丘市委宣传部（科长）", "商丘", ""),
        ("2003-09", "2009", "商丘日报社纪检、梁园区委常委兼宣传部长", "商丘", ""),
        ("2009-04", "2014-12", "商丘市委宣传部副部长兼市政府新闻办主任、市统计局局长", "商丘", ""),
        ("2014-12", "2021-06", "柘城县委副书记代县长、县长", "柘城", "2021-06因火灾免职"),
    ],
}


def _person_slug(name: str) -> str:
    return f"zhecheng_{name}"


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]

    person_positions = [p for p in positions if p["person_id"] == pid]
    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": "present" if pos.get("end_date") == "present" else (pos.get("end_date", "") or ""),
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "system": _system_hint(pos.get("title", "")),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Enrich with known external career segments
    for k, rows in _KNOWN_EXTRA_CAREER.items():
        if name == k:
            for seg in rows:
                career_timeline.append({
                    "start": seg[0] or "unknown",
                    "end": "present" if seg[1] in ("至今", "present") else (seg[1] or "unknown"),
                    "org": seg[2] or seg[1],
                    "title": "",
                    "level": "",
                    "rank": "",
                    "system": "地方",
                    "notes": seg[3] or "",
                    "confidence": "plausible",
                    "source_ids": ["S002"],
                })
    if len(career_timeline) == 0 and not person.get("birth"):
        career_timeline.append({
            "start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
            "notes": "公开资料不足，完整履历待查。", "confidence": "unverified", "source_ids": [],
        })

    # Relationships
    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        if not other:
            continue
        rels_output.append({
            "person": other["name"],
            "person_id": _person_slug(other["name"]),
            "relationship_type": "overlap" if r["type"] == "共事" else "predecessor_successor",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {"id": "S001", "title": "柘城县融媒体中心 / 河南县域经济网 / 柘城县政府网站", "url": source_url,
         "publisher": "柘城县融媒体中心 / 河南县域经济网 / 柘城县人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "2025-2026柘城县委/县人大活动报道（书记邢玉富、县长常忠伟等多篇）"},
    ]
    if name in _KNOWN_EXTRA_CAREER:
        sources.append({"id": "S002", "title": "河南省委组织部任前公示 / 媒体 / 百度百科履历", "url": source_url,
                        "publisher": "河南省委组织部 / 澎湃 / 大河网 / 百度百科", "published_at": "", "accessed_at": AS_OF,
                        "source_type": "appointment_notice", "reliability": "high",
                        "notes": "任前公示（2024-05-12、2024-11-18、2026-04-19）及综合履历"})

    # Organizations for this person
    orgs_out = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        if org and org["name"] not in [o["name"] for o in orgs_out]:
            orgs_out.append({"id": org["id"], "name": org["name"], "type": org["type"]})

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省", "city": "商丘市", "region": "柘城县",
            "job": person.get("current_post", ""), "task_id": "henan_柘城县", "time_focus": "2024-2026现任及晋升路径",
        },
        "identity": {
            "person_id": _person_slug(name),
            "name": name, "aliases": [],
            "gender": person.get("gender", ""), "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""), "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""), "work_start": person.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{name}_{person.get('birth', '')}", "name_birthplace": f"{name}_{person.get('birthplace', '')}", "official_profile_url": source_url},
        },
        "current_status": {
            "current_post": person.get("current_post", ""), "current_org": person.get("current_org", ""),
            "administrative_rank": "", "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed", "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": orgs_out,
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if name in ("邢玉富", "吴杰", "王景宇", "常忠伟") else "local_ladder",
            "systems_experience": [], "geographic_pattern": ["河南省"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [], "speech_themes": [], "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "good" if name in _KNOWN_EXTRA_CAREER else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "核心领导出生年月/籍贯/入党时间等细项缺口；州面上常委履历未核实",
        },
        "open_questions": [
            {"priority": "critical", "question": f"{name}的出生年月/籍贯/教育背景未核实（部分领导）",
             "why_it_matters": "核心身份信息，用于去重与跨区域关联分析",
             "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"], "last_attempted": AS_OF},
            {"priority": "high", "question": f"{name}的完整逐段任职履历（起止时间精确到月）",
             "why_it_matters": "关系网络分析需要精确时间线",
             "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"], "last_attempted": AS_OF},
        ],
    }
    fname = f"{TODAY}-河南省-商丘市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


def _system_hint(title: str) -> str:
    if "纪委书记" in title or "监委" in title:
        return "discipline"
    if "组织" in title:
        return "organization"
    if "宣传" in title:
        return "propaganda"
    return "地方"


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
    # Core leaders (书记、县长) + key predecessors + primary deputies
    core_ids = {1, 2, 3, 5, 20, 21, 22, 23}
    for p in persons:
        if p["id"] in core_ids:
            try:
                write_person_json(p)
            except Exception as exc:  # noqa: BLE001
                print(f"  !! person json failed for {p['name']}: {exc}")

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())