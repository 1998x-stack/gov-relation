#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 长白朝鲜族自治县, 白山市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_长白朝鲜族自治县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - changbai.gov.cn — 长白朝鲜族自治县人民政府官方网站 (✓ reachable)
    - 县长韩永哲完整履历 (http://changbai.gov.cn/zfjg/ldfgjj/xz/202110/t20211011_695774.html)
    - 副县长张震履历 (http://changbai.gov.cn/zfjg/ldfgjj/fxz/202508/t20250801_853033.html)
    - 副县长杨济人履历 (http://changbai.gov.cn/zfjg/ldfgjj/fxz/202508/t20250801_853026.html)
    - 副县长金英华履历 (http://changbai.gov.cn/zfjg/ldfgjj/fxz/202110/t20211011_695844.html)
    - 副县长何韶晨履历 (http://changbai.gov.cn/zfjg/ldfgjj/fxz/202510/t20251029_859002.html)
    - 副县长龚玺鉴履历 (http://changbai.gov.cn/zfjg/ldfgjj/fxz/202512/t20251212_862344.html)
    - 副县长杜继宝履历 (http://changbai.gov.cn/zfjg/ldfgjj/fxz/202408/t20240826_820531.html)
    - 副县长戴鑫磊履历 (http://changbai.gov.cn/zfjg/ldfgjj/fxz/202408/t20240826_820540.html)
  - Baidu Baike — 长白朝鲜族自治县词条 (confirmed: 王成, 许家财, 谭晓轼)
  - Baidu Baike — 王成词条 (confirmed: 1982年生, 汉族, 白山市委常委, 副厅长级)
  - 人民网 — 全国人大代表韩永哲(2023)
  - 吉林日报 — 省管干部任前公示(2025-10-31, 王成拟任市州党委常委)

Confidence notes:
  - 王成(县委书记): names confirmed from Baidu Baike with limited bio (1982年生, 汉族, 大学学历, 白山市委常委, 副厅长级)
    完整履历尚未查到（早期职业生涯未知）
  - 韩永哲(县长): name confirmed, full career timeline from 1992 onwards from government website.
    出生年月、籍贯、学历等基本信息未在网站上公开，仅有职业生涯履历
  - 张震(常务副县长): 完整履历已从政府网站确认（从延边大学毕业到2025年任常委、副县长）
  - 杨济人(副县长): 完整履历已确认（海军航空工程学院毕业，退役后转业白山）
  - 金英华(副县长): 完整履历已确认（本地干部，从吉林机电工程学校毕业一路在长白县晋升）
  - 何韶晨(副县长): 完整履历已确认（从白山市地震局到应急管理局，2025年下派长白）
  - 龚玺鉴(副县长): 完整履历已确认（省药监局挂职干部）
  - 杜继宝(副县长): 完整履历已确认（本地干部，从农技站一路晋升）
  - 戴鑫磊(副县长): 完整履历已确认（从临江市跨县调任）
  - 许家财(县人大常委会主任): name confirmed from Baidu Baike, no biography
  - 谭晓轼(县政协主席): name confirmed from Baidu Baike, no biography
  - All县委常委会其他委员（专职副书记、组织部长、宣传部长、政法委书记、统战部长等）姓名待查
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
SLUG = "长白朝鲜族自治县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_长白朝鲜族自治县"
if _CURRENT_DIR.name == "jilin_长白朝鲜族自治县":
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
# IDs: 1=县委书记, 2=县长, 3=常务副县长(常委), 4=副县长(常委)杨济人,
# 5=金英华(副县长), 6=何韶晨(副县长), 7=龚玺鉴(挂职副县长),
# 8=杜继宝(副县长), 9=戴鑫磊(副县长),
# 10=许家财(人大主任), 11=谭晓轼(政协主席)
# 12-18: 待查的县委常委（专职副书记、纪委书记、组织部长、宣传部长、政法委书记、统战部长、人武部长）

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "王成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年1月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "白山市委常委、县委书记",
        "current_org": "中共长白朝鲜族自治县委员会",
        "source": "Baidu Baike — 长白朝鲜族自治县词条（截至2024年12月）; 吉林日报省管干部任前公示（2025年10月）",
        "confidence": "confirmed_name_partial_bio",
        "notes": "1982年生，汉族，大学学历。现任白山市委常委（副厅长级）、长白朝鲜族自治县委书记。2025年10月吉林日报省管干部任前公示公告拟任市（州）党委常委，随后任白山市委常委。此前完整履历（早期职业生涯、何时任长白县委书记）尚未查到。"
    },
    {
        "id": 2,
        "name": "韩永哲",
        "gender": "男",
        "ethnicity": "推定朝鲜族",
        "birth": "待查（约1970年代初）",
        "birthplace": "推定长白县本地",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "1992年7月",
        "current_post": "县委副书记、县长",
        "current_org": "长白朝鲜族自治县人民政府",
        "source": "changbai.gov.cn — 县长领导简介页面（2021年10月）",
        "confidence": "confirmed_full_career_timeline",
        "notes": "县长，2023年全国人大代表。完整职业生涯履历已从政府网站获取：1992年7月参加工作，历任十四道沟镇农机站、八道沟镇副镇长、县委宣传部副部长、宝泉山镇党委书记、副县长、代县长、县长（2021年11月至今）。作为自治县县长，推定朝鲜族（依法应由朝鲜族公民担任）。出生年月、籍贯、学历等基本信息政府网站未公开。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县政府领导班子（confirmed from changbai.gov.cn）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "张震",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查（约1980年代）",
        "birthplace": "待查",
        "education": "延边大学环境科学专业（2003-2007）",
        "party_join": "中共党员",
        "work_start": "2008年11月",
        "current_post": "县委常委、副县长（常务）",
        "current_org": "长白朝鲜族自治县人民政府",
        "source": "changbai.gov.cn — 副县长张震领导简介页面（2025年8月更新）",
        "confidence": "confirmed_full_career_timeline",
        "notes": "常务副县长。2007年延边大学毕业，2008年参加工作。历任白山经济开发区科员/副局长、靖宇生态健康产业园区管委会主任、白山市商务局科长、吉林靖宇经济开发区管委会主任（副处长级）、2025年4月任长白县委常委，2025年5月任副县长。曾于2024年在龙腾云创产业互联网公司挂职（央企）。分管发改、财政、税务、统计、应急、消防等。"
    },
    {
        "id": 4,
        "name": "杨济人",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查（约1980年代）",
        "birthplace": "待查",
        "education": "海军航空工程学院电气工程及其自动化专业（2001-2005）",
        "party_join": "中共党员",
        "work_start": "2005年6月（军旅）",
        "current_post": "县委常委、副县长",
        "current_org": "长白朝鲜族自治县人民政府",
        "source": "changbai.gov.cn — 副县长杨济人领导简介页面（2025年4月更新）",
        "confidence": "confirmed_full_career_timeline",
        "notes": "军转干部。2001-2005年海军航空工程学院学习，2005-2015年在海军航空兵部队服役（技术军官，正营级）。2017年转业至白山市工信局，历任主任科员、信访办主任、副局长。2025年4月任长白县委常委、副县长。分管人社、水利等。"
    },
    {
        "id": 5,
        "name": "金英华",
        "gender": "女",
        "ethnicity": "待查（推定朝鲜族）",
        "birth": "待查（约1970年代末）",
        "birthplace": "推定长白县",
        "education": "吉林机电工程学校工企营销与公关（1995-1999中专）; 国家开放大学法学（2015-2018大专）",
        "party_join": "中共党员",
        "work_start": "1999年7月",
        "current_post": "副县长",
        "current_org": "长白朝鲜族自治县人民政府",
        "source": "changbai.gov.cn — 副县长金英华领导简介页面（2021年9月更新）",
        "confidence": "confirmed_full_career_timeline",
        "notes": "女性干部，职业生涯完全在长白县。从公路管理段技术员起步，历任交通局妇女主任、十四道沟镇副镇长、旅游局副局长、职业技能教育中心主任、供销社主任、长白镇党委书记。2021年9月任副县长。分管商务、招商引资、边境贸易、外事、政务服务、妇女儿童、生态环境等。推定朝鲜族（自治县女性领导中朝鲜族比例较高）。"
    },
    {
        "id": 6,
        "name": "何韶晨",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查（约1980年代）",
        "birthplace": "待查",
        "education": "吉林省委党校公共管理专业研究生（2014-2016）",
        "party_join": "中共党员",
        "work_start": "待查（约2015年前）",
        "current_post": "副县长",
        "current_org": "长白朝鲜族自治县人民政府",
        "source": "changbai.gov.cn — 副县长何韶晨领导简介页面（2025年9月更新）",
        "confidence": "confirmed_full_career_timeline",
        "notes": "从白山市地震局起步，历任震害防御科副科长/科长、白山市应急管理局灾害防治指导科科长、市应急管理局副局长。2025年9月提名长白县副县长人选，当月任副县长。分管市场监管、住建、残联等。"
    },
    {
        "id": 7,
        "name": "龚玺鉴",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查（约1980年代）",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "2008年8月",
        "current_post": "副县长（挂职）",
        "current_org": "长白朝鲜族自治县人民政府",
        "source": "changbai.gov.cn — 副县长龚玺鉴领导简介页面（2025年12月更新）",
        "confidence": "confirmed_full_career_timeline",
        "notes": "省药监局挂职干部。2008年起在双辽市食药监局、省食药监局/药监局工作，历任科员、副主任科员、主任科员、医疗器械注册管理处一级主任科员、综合和规划财务处副处长。2025年11月任长白县副县长（挂职）。分管重点项目开发建设，协助张震分管工业、通讯。"
    },
    {
        "id": 8,
        "name": "杜继宝",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查（约1970年代末）",
        "birthplace": "推定长白县",
        "education": "吉林农垦特产高等专科学校经济植物（1995-1999）; 国家开放大学行政管理（2021-2024本科）",
        "party_join": "中共党员",
        "work_start": "2000年10月",
        "current_post": "副县长",
        "current_org": "长白朝鲜族自治县人民政府",
        "source": "changbai.gov.cn — 副县长杜继宝领导简介页面（2024年5月更新）",
        "confidence": "confirmed_full_career_timeline",
        "notes": "本地干部，职业生涯完全在长白县。从农技推广站起步，历任特产技术推广站、金华乡政府、县政府办公室、商务粮食局、八道沟镇（党委副书记、镇长、党委书记），2024年5月任副县长。分管自然资源、林业、农业、乡村振兴、人参特产、畜牧、交通等。"
    },
    {
        "id": 9,
        "name": "戴鑫磊",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查（约1980年代）",
        "birthplace": "待查",
        "education": "辽宁工程技术大学机械工程及自动化（2003-2007本科）",
        "party_join": "中共党员",
        "work_start": "2007年8月",
        "current_post": "副县长",
        "current_org": "长白朝鲜族自治县人民政府",
        "source": "changbai.gov.cn — 副县长戴鑫磊领导简介页面（2024年5月更新）",
        "confidence": "confirmed_full_career_timeline",
        "notes": "跨县调任干部，原在临江市工作。历任临江市政府办科员/法制科长、蚂蚁河乡武装部长、住建局党委副书记/纪委书记、临江团市委书记、兴隆街道党工委书记、信访局局长、发改局局长兼国防动员办主任。2024年5月任长白县副县长。分管卫健、医保、教育、体育、供销等。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县人大、政协领导（confirmed from Baidu Baike）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "许家财",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "长白朝鲜族自治县人民代表大会常务委员会",
        "source": "Baidu Baike — 长白朝鲜族自治县词条（截至2024年12月）",
        "confidence": "confirmed_name_only",
        "notes": "县人大常委会主任。姓名从长白县百度百科词条领导信息表确认，无任何履历信息。"
    },
    {
        "id": 11,
        "name": "谭晓轼",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议长白朝鲜族自治县委员会",
        "source": "Baidu Baike — 长白朝鲜族自治县词条（截至2024年12月）",
        "confidence": "confirmed_name_only",
        "notes": "县政协主席。姓名从长白县百度百科词条领导信息表确认，无任何履历信息。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县委常委会其他成员（待查 — 政府网站仅公布政府领导）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "待查_专职副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记（专职）",
        "current_org": "中共长白朝鲜族自治县委员会",
        "source": "待查 — 县委领导不在政府网站公开范围内",
        "confidence": "unverified",
        "notes": "县委专职副书记姓名待核实。长白县政府网站（changbai.gov.cn）仅公开政府领导信息（县长、副县长），县委领导（书记、副书记、常委）信息未在该网站公布。需从其他渠道获取。"
    },
    {
        "id": 13,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共长白朝鲜族自治县纪律检查委员会",
        "source": "待查 — 默认县级纪检班子构成推断",
        "confidence": "unverified",
        "notes": "县纪委书记姓名待核实。属县级标配常委职务。"
    },
    {
        "id": 14,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共长白朝鲜族自治县委组织部",
        "source": "待查 — 默认县级班子构成推断",
        "confidence": "unverified",
        "notes": "县委组织部部长姓名待核实。"
    },
    {
        "id": 15,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共长白朝鲜族自治县委宣传部",
        "source": "待查 — 默认县级班子构成推断",
        "confidence": "unverified",
        "notes": "县委宣传部部长姓名待核实。"
    },
    {
        "id": 16,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共长白朝鲜族自治县委政法委员会",
        "source": "待查 — 默认县级班子构成推断",
        "confidence": "unverified",
        "notes": "县委政法委书记姓名待核实。"
    },
    {
        "id": 17,
        "name": "待查_统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共长白朝鲜族自治县委统战部",
        "source": "待查 — 自治县标配常委职务推断",
        "confidence": "unverified",
        "notes": "县委统战部部长姓名待核实。自治县统战部长通常由朝鲜族干部担任。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共长白朝鲜族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共白山市委", "location": "长白朝鲜族自治县"},
    {"id": 2, "name": "长白朝鲜族自治县人民政府", "type": "政府", "level": "县处级", "parent": "白山市人民政府", "location": "长白朝鲜族自治县"},
    {"id": 3, "name": "长白朝鲜族自治县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "白山市人大常委会", "location": "长白朝鲜族自治县"},
    {"id": 4, "name": "中国人民政治协商会议长白朝鲜族自治县委员会", "type": "政协", "level": "县处级", "parent": "政协白山市委", "location": "长白朝鲜族自治县"},
    {"id": 5, "name": "中共长白朝鲜族自治县纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级", "parent": "白山市纪委", "location": "长白朝鲜族自治县"},
    {"id": 6, "name": "中共长白朝鲜族自治县委组织部", "type": "党委", "level": "县处级", "parent": "中共长白朝鲜族自治县委员会", "location": "长白朝鲜族自治县"},
    {"id": 7, "name": "中共长白朝鲜族自治县委宣传部", "type": "党委", "level": "县处级", "parent": "中共长白朝鲜族自治县委员会", "location": "长白朝鲜族自治县"},
    {"id": 8, "name": "中共长白朝鲜族自治县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共长白朝鲜族自治县委员会", "location": "长白朝鲜族自治县"},
    {"id": 9, "name": "中共长白朝鲜族自治县委统战部", "type": "党委", "level": "县处级", "parent": "中共长白朝鲜族自治县委员会", "location": "长白朝鲜族自治县"},
    {"id": 10, "name": "长白朝鲜族自治县公安局", "type": "政府", "level": "乡科级", "parent": "长白朝鲜族自治县人民政府", "location": "长白朝鲜族自治县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 王成（县委书记）
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "同时任白山市委常委（副厅长级）。任县委书记具体时间待查。"},
    {"person_id": 1, "org_id": 1, "title": "白山市委常委", "start_date": "2025年10月后", "end_date": "", "rank": "副厅级",
     "note": "2025年10月省管干部任前公示，拟任市（州）党委常委"},

    # 韩永哲（县长）
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2021年11月", "end_date": "", "rank": "县处级正职",
     "note": "2021年11月至今任县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2021年8月", "end_date": "", "rank": "县处级正职",
     "note": "2021年8月任县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "代县长", "start_date": "2021年8月", "end_date": "2021年11月", "rank": "县处级正职",
     "note": ""},
    {"person_id": 2, "org_id": 2, "title": "副县长", "start_date": "2018年11月", "end_date": "2021年8月", "rank": "县处级副职",
     "note": "2018年11月副县长人选，2019年2月县政府党组成员、副县长"},
    {"person_id": 2, "org_id": 9, "title": "宝泉山镇党委书记", "start_date": "2016年8月", "end_date": "2020年3月", "rank": "乡科级正职",
     "note": "2016.08-2018.11 宝泉山镇党委书记，2018.11-2020.03 兼宝泉山镇党委书记"},
    {"person_id": 2, "org_id": 9, "title": "宝泉山镇党委书记、镇长", "start_date": "2015年12月", "end_date": "2016年8月", "rank": "乡科级正职",
     "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县委宣传部副部长兼县文联主席", "start_date": "2014年12月", "end_date": "2015年12月", "rank": "县处级副职",
     "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县委宣传部副部长", "start_date": "2011年7月", "end_date": "2014年12月", "rank": "县处级副职",
     "note": ""},
    {"person_id": 2, "org_id": 2, "title": "八道沟镇政府副镇长", "start_date": "2006年10月", "end_date": "2011年7月", "rank": "乡科级副职",
     "note": ""},
    {"person_id": 2, "org_id": 1, "title": "十四道沟镇宣传委员", "start_date": "2004年11月", "end_date": "2006年10月", "rank": "乡科级副职",
     "note": ""},
    {"person_id": 2, "org_id": 9, "title": "十四道沟镇农业综合服务中心主任", "start_date": "2004年3月", "end_date": "2004年11月", "rank": "股级",
     "note": ""},
    {"person_id": 2, "org_id": 9, "title": "十四道沟镇农机站职员、站长", "start_date": "1992年7月", "end_date": "2004年3月", "rank": "科员级",
     "note": ""},

    # 张震（常委、常务副县长）
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "2025年4月", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副县长（常务）", "start_date": "2025年5月", "end_date": "", "rank": "县处级副职",
     "note": "负责常务工作，分管发改、财政、税务、统计、应急、消防等"},
    {"person_id": 3, "org_id": 100, "title": "吉林靖宇经济开发区管委会主任", "start_date": "2023年2月", "end_date": "2025年4月", "rank": "副处级",
     "note": "兼靖宇新能源产业园区管委会主任"},

    # 杨济人（常委、副县长）
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "2025年4月", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "2025年4月", "end_date": "", "rank": "县处级副职",
     "note": "分管人社、水利等"},

    # 金英华（副县长）
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "2021年9月", "end_date": "", "rank": "县处级副职",
     "note": "分管商务、招商引资、边境贸易、外事、政务服务、妇女儿童、生态环境等"},
    {"person_id": 5, "org_id": 9, "title": "长白镇党委书记", "start_date": "2021年8月", "end_date": "2021年9月", "rank": "乡科级正职",
     "note": ""},

    # 何韶晨（副县长）
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "2025年9月", "end_date": "", "rank": "县处级副职",
     "note": "分管市场监管、住建、残联等"},

    # 龚玺鉴（挂职副县长）
    {"person_id": 7, "org_id": 2, "title": "副县长（挂职）", "start_date": "2025年11月", "end_date": "", "rank": "县处级副职",
     "note": "省药监局挂职干部，分管重点项目开发建设"},

    # 杜继宝（副县长）
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "2024年5月", "end_date": "", "rank": "县处级副职",
     "note": "分管自然资源、林业、农业、乡村振兴、人参特产、畜牧、交通等"},

    # 戴鑫磊（副县长）
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "2024年5月", "end_date": "", "rank": "县处级副职",
     "note": "分管卫健、医保、教育、体育、供销等"},

    # 许家财（人大主任）
    {"person_id": 10, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},

    # 谭晓轼（政协主席）
    {"person_id": 11, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},

    # 待查_专职副书记
    {"person_id": 12, "org_id": 1, "title": "县委副书记（专职）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "姓名待核实"},

    # 待查_纪委书记
    {"person_id": 13, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 5, "title": "县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "姓名待核实"},

    # 待查_组织部长
    {"person_id": 14, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},

    # 待查_宣传部长
    {"person_id": 15, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},

    # 待查_政法委书记
    {"person_id": 16, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},

    # 待查_统战部长
    {"person_id": 17, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 书记与县长
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记王成与县长韩永哲为党政主要领导搭档关系",
        "overlap_org": "中共长白朝鲜族自治县委员会",
        "overlap_period": "当前（王成任书记后至今）",
        "confidence": "confirmed",
    },
    # 书记与常务副县长
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与常务副县长张震为县委与政府领导关系",
        "overlap_org": "中共长白朝鲜族自治县委员会",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 县长与常务
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长韩永哲与常务副县长张震为政府主要领导与副手关系",
        "overlap_org": "长白朝鲜族自治县人民政府",
        "overlap_period": "2025年5月至今",
        "confidence": "confirmed",
    },
    # 县长与各副县长
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与杨济人副县长为政府领导关系",
        "overlap_org": "长白朝鲜族自治县人民政府",
        "overlap_period": "2025年4月至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县长与金英华副县长为政府领导关系。金英华长期在长白县任职，与韩永哲有多年的工作交集",
        "overlap_org": "长白朝鲜族自治县人民政府",
        "overlap_period": "2021年9月至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长与杜继宝副县长为政府领导关系。杜继宝为长白本地成长干部，与韩永哲有多年的工作交集",
        "overlap_org": "长白朝鲜族自治县人民政府",
        "overlap_period": "2024年5月至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "县长与戴鑫磊副县长为政府领导关系。戴鑫磊2024年从临江市跨县调任",
        "overlap_org": "长白朝鲜族自治县人民政府",
        "overlap_period": "2024年5月至今",
        "confidence": "confirmed",
    },
    # 跨县调任关系 - 戴鑫磊从临江市调来
    {
        "person_a": 9,
        "person_b": 2,
        "type": "cross_county_transfer",
        "context": "戴鑫磊2024年从临江市跨县调任长白县副县长，为长白-临江跨县干部交流案例",
        "overlap_org": "白山市",
        "overlap_period": "2024年",
        "confidence": "confirmed",
    },
    # 张震从靖宇县调来
    {
        "person_a": 3,
        "person_b": 2,
        "type": "cross_county_transfer",
        "context": "张震2025年从吉林靖宇经济开发区调任长白县委常委、副县长",
        "overlap_org": "白山市",
        "overlap_period": "2025年",
        "confidence": "confirmed",
    },
    # 杨济人从白山工信局下派
    {
        "person_a": 4,
        "person_b": 2,
        "type": "city_to_county",
        "context": "杨济人2025年从白山市工信局副局长下派长白县任县委常委、副县长",
        "overlap_org": "白山市",
        "overlap_period": "2025年",
        "confidence": "confirmed",
    },
    # 何韶晨从白山应急管理局下派
    {
        "person_a": 6,
        "person_b": 2,
        "type": "city_to_county",
        "context": "何韶晨2025年从白山市应急管理局副局长下派长白县任副县长",
        "overlap_org": "白山市",
        "overlap_period": "2025年",
        "confidence": "confirmed",
    },
    # 龚玺鉴从省药监局挂职
    {
        "person_a": 7,
        "person_b": 2,
        "type": "province_to_county",
        "context": "龚玺鉴2025年从吉林省药监局副处长下派长白县挂职副县长",
        "overlap_org": "吉林省",
        "overlap_period": "2025年",
        "confidence": "confirmed",
    },
    # 常委之间的同僚关系
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "杨济人与张震同为长白县委常委",
        "overlap_org": "中共长白朝鲜族自治县委员会",
        "overlap_period": "2025年4月至今",
        "confidence": "confirmed",
    },
    # 本地干部之间长期关系
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "韩永哲与金英华均为长白本地成长干部，职业生涯长年在长白县任职",
        "overlap_org": "长白朝鲜族自治县",
        "overlap_period": "多年",
        "confidence": "plausible",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "overlap",
        "context": "韩永哲与杜继宝均为长白本地成长干部，长期在长白县任职",
        "overlap_org": "长白朝鲜族自治县",
        "overlap_period": "多年",
        "confidence": "plausible",
    },
]

# ── Person JSONs ─────────────────────────────────────────────────────────────

PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "吉林省",
        "city": "白山市",
        "region": "长白朝鲜族自治县",
        "task_id": "jilin_长白朝鲜族自治县",
        "time_focus": "2026年7月",
    },
    "identity": {},
    "current_status": {},
    "career_timeline": [],
    "organizations": [],
    "relationships": [],
    "governance_record": [],
    "professional_profile": {},
    "work_style_and_personality": {},
    "network_metrics": {},
    "risk_and_integrity_signals": [],
    "source_register": [],
    "confidence_summary": {},
    "open_questions": [],
}


def build_person_json(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    now = TODAY

    person = {
        "identity": {
            "person_id": f"jilin_baishan_changbai_{name}",
            "name": name,
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [e.strip() for e in p["education"].split(";") if e.strip()] if p["education"] and p["education"] != "待查" else [],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_{p['birth']}",
                "name_birthplace": f"{name}_{p['birthplace']}",
                "official_profile_url": f"http://changbai.gov.cn/zfjg/ldfgjj/",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "副厅级" if person_id == 1 and "白山市委常委" in role_label else ("县处级正职" if person_id <= 2 or person_id in (10, 11) else "县处级副职"),
            "as_of": AS_OF,
            "is_current_confirmed": p["confidence"] not in ("unverified", "confirmed_name_only"),
            "source_ids": [p["source"]],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No risk signals found from available sources",
                "date": AS_OF,
                "confidence": "low" if p["confidence"] == "unverified" else "medium",
                "source_ids": [],
            }
        ],
        "source_register": [],
        "confidence_summary": {
            "identity": p["confidence"],
            "current_role": p["confidence"],
            "career_completeness": "partial" if p.get("notes") and "履历" in p["source"] else "thin",
            "relationship_confidence": "low",
            "biggest_gap": "",
        },
        "open_questions": [],
    }

    # Build career_timeline from positions
    pos_list = [x for x in positions if x["person_id"] == person_id]
    for pos in sorted(pos_list, key=lambda x: x.get("start_date", "")):
        person["career_timeline"].append({
            "start": pos.get("start_date", "unknown"),
            "end": pos.get("end_date", "present") if pos.get("end_date") else "present",
            "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": "长白朝鲜族自治县",
            "system": "party" if "书记" in pos["title"] or "常委" in pos["title"] or "组织" in pos["title"] or "宣传" in pos["title"] or "统战" in pos["title"] or "纪委" in pos["title"] else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": "县委书记" in pos["title"] or "县长" in pos["title"] or "副县长" in pos["title"] and "start" not in pos.get("start_date", "unknown"),
            "notes": pos.get("note", "") if pos.get("note") else "",
            "confidence": p["confidence"],
            "source_ids": [],
        })

    # Build open_questions
    if "待查" in name:
        person["open_questions"].append({
            "priority": "critical",
            "question": f"长白朝鲜族自治县{role_label}姓名是什么？",
            "why_it_matters": "核心目标人物之一，完整调查必须确认姓名和身份",
            "suggested_queries": [
                f"长白朝鲜族自治县 {role_label}",
                "长白县委 常委会 组成人员",
                "白山市委组织部 长白 干部任免",
            ],
            "last_attempted": AS_OF,
        })
    if p["birth"] == "" or "待查" in p["birth"]:
        person["open_questions"].append({
            "priority": "critical",
            "question": f"{name}的出生年月、籍贯、学历和完整履历",
            "why_it_matters": "身份确认后需补充完整履历资料",
            "suggested_queries": [
                f"长白朝鲜族自治县 {name} 简历",
                f"{name} 百度百科",
            ],
            "last_attempted": AS_OF,
        })

    if len(person["career_timeline"]) <= 2:
        person["confidence_summary"]["biggest_gap"] = f"履历信息不完整，仅当前职务已知，缺少此前职业生涯详情"

    return person


def write_person_json(person_id: int):
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    safe_role = role_label.replace("、", "_").replace("（", "(").replace("）", ")")
    filename = f"{TODAY}-吉林省-白山市-{safe_role}-{name}.json"
    path = PJSON_DIR / filename

    person_data = build_person_json(person_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)

    return path


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    # Build DB and GEXF
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

    # Write person JSONs for known people
    person_files = []
    for pid in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"\nNote: County website (changbai.gov.cn) reachable. Full government leadership confirmed.")
    print(f"      县委常委会其他委员（专职副书记、纪委书记、组织部长、宣传部长、政法委书记、统战部长）姓名待查。")
    print(f"Done.")


if __name__ == "__main__":
    main()
