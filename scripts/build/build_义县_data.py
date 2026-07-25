#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 义县 (Yixian County), 锦州市, 辽宁省.

Level: 县
Province: 辽宁省
Parent city: 锦州市
Targets: 县委书记 (Party Secretary: 尤源), 县长 (County Mayor: 张健)
Task ID: liaoning_义县

Research date: 2026-07-25
Official source: http://www.lnyx.gov.cn/ (义县人民政府)

Current status (as of 2026-07-25, confirmed via 义县人民政府 website):
- 县委书记: 尤源 (2026年6月27日以县委书记身份在"两优一先"表彰大会上讲话)
- 县长: 张健 (县政府党组书记、县长; 兼任锦州七里河经济开发区党工委副书记、管委会主任)
- 县人大常委会党组书记、主任候选人: 梁铮 (原常务副县长)
- 县政协党组书记、主席候选人: 金海
- 前任县委书记: 待查 (尤源的接任时间未知)
- 前任县长: 待查 (张健的接任时间未知)

Leadership roster confirmed via:
- http://www.lnyx.gov.cn/ (义县人民政府官网)
- http://www.lnyx.gov.cn/ldzc/xz.htm (县长页面)
- http://www.lnyx.gov.cn/ldzc/fxz.htm (副县长页面)
- http://www.lnyx.gov.cn/info/1038/26709.htm ("两优一先"表彰大会 — 确认县委书记尤源)
- http://www.lnyx.gov.cn/info/1038/26715.htm (走访慰问 — 尤源带队)
- http://www.lnyx.gov.cn/info/1203/25916.htm (义政办发〔2026〕1号 — 县政府领导班子分工)

Confidence notes:
   尤源身份作为县委书记被"两优一先"表彰大会文章确认。
   张健身份作为县长被政府官网和新闻报道确认。
   政府领导班子成员信息来自义政办发〔2026〕1号及政府网站领导之窗。
   县委常委名单不完全——公开源仅显示部分成员。
   尤源、张健等人的完整履历（出生年月、籍贯、教育背景等）未公开。
   Web search tools (Exa, Baidu, Jina Reader) 该任务中受到限速或超时。
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "义县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 尤源 — 县委书记
    {
        "id": 1,
        "name": "尤源",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中国共产党义县委员会",
        "source": "http://www.lnyx.gov.cn/info/1038/26709.htm (2026年6月27日'两优一先'表彰大会: 县委书记尤源出席会议并讲话)",
    },
    # 2. 张健 — 县委副书记、县长
    {
        "id": 2,
        "name": "张健",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "义县人民政府",
        "source": "http://www.lnyx.gov.cn/ldzc/xz.htm (县政府官网领导之窗: 张健 县长)",
    },

    # ════════════════════════════════════════
    # 县人大常委会/政协领导
    # ════════════════════════════════════════

    # 3. 梁铮 — 县人大常委会党组书记、主任候选人 (原常务副县长)
    {
        "id": 3,
        "name": "梁铮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任候选人",
        "current_org": "义县人民代表大会常务委员会",
        "source": "http://www.lnyx.gov.cn/info/1038/26709.htm (2026年6月27日: 县人大常委会党组书记、主任候选人梁铮出席'两优一先'表彰大会)",
    },
    # 4. 金海 — 县政协党组书记、主席候选人
    {
        "id": 4,
        "name": "金海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组书记、主席候选人",
        "current_org": "政协义县委员会",
        "source": "http://www.lnyx.gov.cn/info/1038/26709.htm (2026年6月27日: 县政协党组书记、主席候选人金海出席'两优一先'表彰大会)",
    },

    # ════════════════════════════════════════
    # 县委常委及其他县级领导
    # ════════════════════════════════════════

    # 5. 苗齐 — 县委常委
    {
        "id": 5,
        "name": "苗齐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中国共产党义县委员会",
        "source": "http://www.lnyx.gov.cn/info/1038/26709.htm (2026年6月27日: 县领导苗齐参加'两优一先'表彰大会)",
    },
    # 6. 迟晓君 — 县委常委、副县长（常务）
    {
        "id": 6,
        "name": "迟晓君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长（常务）",
        "current_org": "义县人民政府",
        "source": "http://www.lnyx.gov.cn/ldzc/fxz.htm (县政府官网: 迟晓君 副县长 负责常务工作)",
    },
    # 7. 赵宇飞 — 县委常委/县领导
    {
        "id": 7,
        "name": "赵宇飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中国共产党义县委员会",
        "source": "http://www.lnyx.gov.cn/info/1038/26770.htm (2026年7月20日: 县领导赵宇飞参加博爱助学活动)",
    },
    # 8. 韩一 — 县委常委/县领导
    {
        "id": 8,
        "name": "韩一",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中国共产党义县委员会",
        "source": "http://www.lnyx.gov.cn/info/1038/26709.htm (2026年6月27日: 县领导韩一参加'两优一先'表彰大会)",
    },
    # 9. 张小江 — 县委常委/县领导
    {
        "id": 9,
        "name": "张小江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中国共产党义县委员会",
        "source": "http://www.lnyx.gov.cn/info/1038/26709.htm (2026年6月27日: 县领导张小江参加'两优一先'表彰大会)",
    },
    # 10. 赵光明 — 县委常委/县领导
    {
        "id": 10,
        "name": "赵光明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中国共产党义县委员会",
        "source": "http://www.lnyx.gov.cn/info/1038/26709.htm (2026年6月27日: 县领导赵光明参加'两优一先'表彰大会)",
    },
    # 11. 钱伟 — 县委常委/县领导
    {
        "id": 11,
        "name": "钱伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中国共产党义县委员会",
        "source": "http://www.lnyx.gov.cn/info/1038/26709.htm (2026年6月27日: 县领导钱伟参加'两优一先'表彰大会)",
    },
    # 12. 金晓明 — 县领导
    {
        "id": 12,
        "name": "金晓明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中国共产党义县委员会",
        "source": "http://www.lnyx.gov.cn/info/1038/26715.htm (2026年7月1日: 县领导金晓明参加走访慰问活动)",
    },

    # ════════════════════════════════════════
    # 县政府副县长团队
    # ════════════════════════════════════════

    # 13. 刘亮 — 副县长 (2026年7月政府官网在任)
    {
        "id": 13,
        "name": "刘亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "义县人民政府",
        "source": "http://www.lnyx.gov.cn/ldzc/fxz.htm (县政府官网: 刘亮 副县长 负责住建/综合执法等)",
    },
    # 14. 王惟 — 副县长
    {
        "id": 14,
        "name": "王惟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "义县人民政府",
        "source": "http://www.lnyx.gov.cn/ldzc/fxz.htm (县政府官网: 王惟 副县长 负责文旅/教育/卫健等)",
    },
    # 15. 高伟 — 副县长
    {
        "id": 15,
        "name": "高伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "义县人民政府",
        "source": "http://www.lnyx.gov.cn/ldzc/fxz.htm (县政府官网: 高伟 副县长 负责水利/农业/乡村振兴等)",
    },
    # 16. 张柯 — 副县长、县公安局党委书记/局长
    {
        "id": 16,
        "name": "张柯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "义县人民政府",
        "source": "http://www.lnyx.gov.cn/ldzc/fxz.htm (县政府官网: 张柯 副县长,县公安局党委书记、局长)",
    },
    # 17. 单玉斌 — 副县长
    {
        "id": 17,
        "name": "单玉斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "义县人民政府",
        "source": "http://www.lnyx.gov.cn/ldzc/fxz.htm (县政府官网: 单玉斌 副县长 负责金融/打非等)",
    },
    # 18. 任国锋 — 副县长
    {
        "id": 18,
        "name": "任国锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "义县人民政府",
        "source": "http://www.lnyx.gov.cn/ldzc/fxz.htm (县政府官网: 任国锋 副县长 负责自然资源/交通/市场监管等)",
    },
    # 19. 滕林 — 县政府党组成员，锦州七里河经济开发区党工委副书记、管委会常务副主任
    {
        "id": 19,
        "name": "滕林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、开发区常务副主任",
        "current_org": "锦州七里河经济开发区",
        "source": "http://www.lnyx.gov.cn/info/1203/25916.htm (义政办发〔2026〕1号区政府分工通知)",
    },
    # 20. 洪尚铁 — 代管县政府办公室工作
    {
        "id": 20,
        "name": "洪尚铁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府办公室（代管）",
        "current_org": "义县人民政府办公室",
        "source": "http://www.lnyx.gov.cn/info/1203/25916.htm (义政办发〔2026〕1号: 洪尚铁代管政府办工作)",
    },
    # 21. 胡伟 — 原副县长(2026年1月分工通知中在任，7月官网已变更为刘亮)
    {
        "id": 21,
        "name": "胡伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原副县长",
        "current_org": "义县人民政府（已离任）",
        "source": "http://www.lnyx.gov.cn/info/1203/25916.htm (义政办发〔2026〕1号: 胡伟 副县长; 2026年7月官网已显示由刘亮接替)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中国共产党义县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共锦州市委员会",
        "location": "辽宁省锦州市义县",
    },
    {
        "id": 2,
        "name": "义县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "锦州市人民政府",
        "location": "辽宁省锦州市义县",
    },
    {
        "id": 3,
        "name": "义县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "锦州市人民代表大会常务委员会",
        "location": "辽宁省锦州市义县",
    },
    {
        "id": 4,
        "name": "政协义县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协锦州市委员会",
        "location": "辽宁省锦州市义县",
    },
    {
        "id": 5,
        "name": "义县纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共锦州市纪律检查委员会",
        "location": "辽宁省锦州市义县",
    },
    {
        "id": 6,
        "name": "义县公安局",
        "type": "政府",
        "level": "乡科级",
        "parent": "义县人民政府",
        "location": "辽宁省锦州市义县",
    },
    {
        "id": 7,
        "name": "锦州七里河经济开发区",
        "type": "开发区",
        "level": "省级开发区",
        "parent": "义县人民政府",
        "location": "辽宁省锦州市义县七里河镇",
    },
    {
        "id": 8,
        "name": "义县人民政府办公室",
        "type": "政府",
        "level": "乡科级",
        "parent": "义县人民政府",
        "location": "辽宁省锦州市义县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 尤源 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present",
     "rank": "正处级", "note": "2026年6月27日以县委书记身份在'两优一先'表彰大会上讲话; 具体任命时间未知"},
    # 张健 - 县委副书记、县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present",
     "rank": "正处级", "note": "县政府党组书记、县长; 兼任锦州七里河经济开发区党工委副书记、管委会主任; 2026年7月公开报道确认"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present",
     "rank": "正处级", "note": "县委副书记、县长"},
    {"person_id": 2, "org_id": 7, "title": "开发区党工委副书记、管委会主任", "start": "", "end": "present",
     "rank": "正处级", "note": "兼任锦州七里河经济开发区党工委副书记、管委会主任"},

    # ── 人大/政协 ──
    # 梁铮 - 县人大常委会党组书记、主任候选人
    {"person_id": 3, "org_id": 3, "title": "县人大常委会党组书记、主任候选人", "start": "2026年", "end": "present",
     "rank": "正处级", "note": "原常务副县长转任县人大常委会; 2026年6月以该身份出席'两优一先'表彰大会"},
    # 金海 - 县政协党组书记、主席候选人
    {"person_id": 4, "org_id": 4, "title": "县政协党组书记、主席候选人", "start": "2026年", "end": "present",
     "rank": "正处级", "note": "2026年6月以该身份出席'两优一先'表彰大会"},

    # ── 县委常委及县领导 ──
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present",
     "rank": "副处级", "note": "具体分工未知"},
    # 迟晓君 - 县委常委、副县长（常务）
    {"person_id": 6, "org_id": 2, "title": "副县长（常务）", "start": "2026年", "end": "present",
     "rank": "副处级", "note": "负责县政府常务工作; 发展改革/财税/人社/应急管理等; 协助张健分管审计局"},
    {"person_id": 7, "org_id": 1, "title": "县领导", "start": "", "end": "present",
     "rank": "副处级", "note": "参与博爱助学活动; 具体职务待确认"},
    {"person_id": 8, "org_id": 1, "title": "县领导", "start": "", "end": "present",
     "rank": "副处级", "note": "参加'两优一先'表彰大会; 具体职务待确认"},
    {"person_id": 9, "org_id": 1, "title": "县领导", "start": "", "end": "present",
     "rank": "副处级", "note": "参加'两优一先'表彰大会; 具体职务待确认"},
    {"person_id": 10, "org_id": 1, "title": "县领导", "start": "", "end": "present",
     "rank": "副处级", "note": "参加'两优一先'表彰大会; 具体职务待确认"},
    {"person_id": 11, "org_id": 1, "title": "县领导", "start": "", "end": "present",
     "rank": "副处级", "note": "参加'两优一先'表彰大会; 具体职务待确认"},
    {"person_id": 12, "org_id": 1, "title": "县领导", "start": "", "end": "present",
     "rank": "副处级", "note": "参加走访慰问活动; 具体职务待确认"},

    # ── 副县长团队 ──
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "2026年", "end": "present",
     "rank": "副处级", "note": "负责住建/综合执法/营商环境/退役军人事务等; 接替胡伟岗位"},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责文旅/广电/体育/教育/卫健/残疾人保障等"},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责水利/防洪抗旱/农业农村/乡村振兴/生态环境等"},
    {"person_id": 16, "org_id": 2, "title": "副县长、县公安局局长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责公安/司法等工作; 县公安局党委书记、局长"},
    {"person_id": 16, "org_id": 6, "title": "县公安局党委书记、局长", "start": "", "end": "present",
     "rank": "乡科级", "note": "兼任县公安局党委书记、局长"},
    {"person_id": 17, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责打击非法集资/金融/石油/通讯/烟草等"},
    {"person_id": 18, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责自然资源/林草/交通/市场监管等"},
    {"person_id": 19, "org_id": 7, "title": "开发区党工委副书记、管委会常务副主任", "start": "", "end": "present",
     "rank": "副处级", "note": "负责开发区日常工作及工信/商务/招商引资等"},
    {"person_id": 20, "org_id": 8, "title": "县政府办公室（代管）", "start": "", "end": "present",
     "rank": "乡科级", "note": "代管县政府办公室工作"},

    # ── 原副县长（离任）──
    {"person_id": 21, "org_id": 2, "title": "副县长", "start": "", "end": "2026年初",
     "rank": "副处级", "note": "2026年1月分工通知中仍在任; 2026年7月政府官网已由刘亮接替"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 尤源 <-> 张健: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长党政主要领导搭档",
     "overlap_org": "中国共产党义县委员会/义县人民政府",
     "overlap_period": "2026年"},

    # 尤源 <-> 梁铮: 县委领导与人大常委会
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "同为县级领导出席'两优一先'表彰大会",
     "overlap_org": "中国共产党义县委员会",
     "overlap_period": "2026年"},

    # 尤源 <-> 金海: 县委领导与政协
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "同为县级领导出席'两优一先'表彰大会",
     "overlap_org": "中国共产党义县委员会",
     "overlap_period": "2026年"},

    # 张健 <-> 迟晓君: 县长与常务副县长
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "县长与常务副县长行政工作搭档",
     "overlap_org": "义县人民政府",
     "overlap_period": "2026年"},

    # 张健 <-> 梁铮（原常务副县长）:
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "原县长与常务副县长行政搭档（梁铮转任人大前）",
     "overlap_org": "义县人民政府",
     "overlap_period": "2025-2026年"},

    # 张健 <-> 高伟: 县长与副县长
    {"person_a": 2, "person_b": 15, "type": "overlap",
     "context": "县长与分管水利/农业的副县长",
     "overlap_org": "义县人民政府",
     "overlap_period": "2026年"},

    # 张健 <-> 张柯: 县长与公安局长
    {"person_a": 2, "person_b": 16, "type": "overlap",
     "context": "县长与分管公安的副县长、县公安局局长",
     "overlap_org": "义县人民政府",
     "overlap_period": "2026年"},

    # 张健 <-> 赵宇飞: 县领导出席同一活动
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "共同出席博爱助学活动",
     "overlap_org": "中国共产党义县委员会",
     "overlap_period": "2026年7月"},

    # 胡伟 <-> 刘亮: 前任与继任（副县长岗位）
    {"person_a": 21, "person_b": 13, "type": "predecessor_successor",
     "context": "刘亮接替胡伟的副县长岗位（住建/综合执法等领域）",
     "overlap_org": "义县人民政府",
     "overlap_period": "2026年初"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "义县人民政府官网 - 两优一先表彰大会",
            "url": "http://www.lnyx.gov.cn/info/1038/26709.htm",
            "publisher": "义县人民政府",
            "published_at": "2026-06-29",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "县委书记尤源出席会议并讲话; 确认尤源为县委书记、张健为县长、梁铮为人大党组书记、金海为政协党组书记",
        },
        {
            "id": "S002",
            "title": "义县人民政府官网 - 领导之窗（县长）",
            "url": "http://www.lnyx.gov.cn/ldzc/xz.htm",
            "publisher": "义县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认张健为县长",
        },
        {
            "id": "S003",
            "title": "义县人民政府官网 - 领导之窗（副县长）",
            "url": "http://www.lnyx.gov.cn/ldzc/fxz.htm",
            "publisher": "义县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认迟晓君（常务）、刘亮、王惟、高伟、张柯（公安局长）、单玉斌、任国锋为副县长",
        },
        {
            "id": "S004",
            "title": "义县人民政府办公室关于调整县政府领导班子成员工作分工的通知",
            "url": "http://www.lnyx.gov.cn/info/1203/25916.htm",
            "publisher": "义县人民政府办公室",
            "published_at": "2026-01-28",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "义政办发〔2026〕1号; 确认张健为县长、梁铮为常务副县长（后转任人大）、滕林/胡伟/王惟/高伟/张柯/单玉斌/任国锋/洪尚铁的职务分工",
        },
        {
            "id": "S005",
            "title": "义县人民政府官网 - 县领导走访慰问老党员和困难党员",
            "url": "http://www.lnyx.gov.cn/info/1038/26715.htm",
            "publisher": "义县人民政府",
            "published_at": "2026-07-01",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认尤源、张健、梁铮、金海、苗齐、迟晓君、刘亮、赵宇飞、金晓明、韩一、张小江、赵光明、钱伟等县级领导名单",
        },
        {
            "id": "S006",
            "title": "义县人民政府官网 - 博爱助学活动",
            "url": "http://www.lnyx.gov.cn/info/1038/26770.htm",
            "publisher": "义县人民政府",
            "published_at": "2026-07-20",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "县委副书记、县长张健参加活动; 县领导赵宇飞参加活动",
        },
        {
            "id": "S007",
            "title": "义县人民政府官网 - 防汛工作会议",
            "url": "http://www.lnyx.gov.cn/info/1038/26733.htm",
            "publisher": "义县人民政府",
            "published_at": "2026-07-05",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "县委副书记、县长张健讲话; 高伟参加",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"yixian_{name}"

    # ── 尤源 (县委书记) ──
    if name == "尤源":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省",
                "city": "锦州市",
                "region": "义县",
                "job": "县委书记",
                "task_id": "liaoning_义县",
                "time_focus": "2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "尤源",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "尤源_",
                    "name_birthplace": "尤源_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中国共产党义县委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中国共产党义县委员会",
                    "title": "县委书记",
                    "level": "正处级",
                    "location": "辽宁省锦州市义县",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2026年6月27日以县委书记身份在'两优一先'表彰大会上讲话; 何时就任及此前职务未知",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中国共产党义县委员会", "type": "党委",
                 "level": "县处级", "location": "辽宁省锦州市义县"},
            ],
            "relationships": [
                {"person": "张健", "person_id": "yixian_张健",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "县委书记与县长党政主要领导搭档",
                 "overlap_org": "中国共产党义县委员会/义县人民政府",
                 "overlap_period": "2026年",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002", "S005"]},
                {"person": "梁铮", "person_id": "yixian_梁铮",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "同为县级领导出席'两优一先'表彰大会",
                 "overlap_org": "中国共产党义县委员会",
                 "overlap_period": "2026年",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S005"]},
                {"person": "金海", "person_id": "yixian_金海",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "同为县级领导出席'两优一先'表彰大会",
                 "overlap_org": "中国共产党义县委员会",
                 "overlap_period": "2026年",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S005"]},
            ],
            "governance_record": [
                {
                    "period": "2026年6月",
                    "domain": "governance",
                    "achievement_or_event": "主持召开义县'两优一先'表彰大会并发表讲话",
                    "role_in_event": "县委书记，主持会议",
                    "measurable_outcome": "表彰全县优秀共产党员、优秀党务工作者和先进基层党组织",
                    "location": "锦州市义县",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道有限，不足以判断工作风格",
                        "confidence": "unverified",
                        "source_ids": ["S001"],
                    }
                ],
                "speech_themes": [
                    "筑牢信仰之基",
                    "永葆绝对忠诚的政治本色",
                    "坚定拥护'两个确立'、坚决做到'两个维护'",
                    "厚植为民情怀",
                    "涵养清风正气",
                ],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "minimal",
                "relationship_confidence": "medium",
                "biggest_gap": "尤源的完整履历（出生年月、籍贯、性别、教育背景、任县委书记前的职业生涯）完全未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "尤源的出生年月、籍贯、性别、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["尤源 简历 义县", "尤源 出生", "尤源 百度百科", "锦州 尤源"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "尤源何时开始担任义县县委书记？此前担任什么职务？",
                    "why_it_matters": "理清其职业生涯路径和任命时间",
                    "suggested_queries": ["尤源 任义县县委书记", "义县 县委书记 任免 2025", "义县 书记 尤源 任职"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "尤源的完整职业生涯履历？",
                    "why_it_matters": "评估其专业背景和职业发展路径",
                    "suggested_queries": ["尤源 工作经历", "尤源 此前职务"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "义县前任县委书记是谁？由谁接替尤源之前担任县委书记？",
                    "why_it_matters": "构建领导人继任链条",
                    "suggested_queries": ["义县 前县委书记", "义县 前任书记", "锦州 义县 书记 任免"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 张健 (县长) ──
    if name == "张健":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省",
                "city": "锦州市",
                "region": "义县",
                "job": "县长",
                "task_id": "liaoning_义县",
                "time_focus": "2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "张健",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "张健_",
                    "name_birthplace": "张健_",
                    "official_profile_url": "http://www.lnyx.gov.cn/ldzc/xz.htm",
                },
            },
            "current_status": {
                "current_post": "县长",
                "current_org": "义县人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "义县人民政府",
                    "title": "县长",
                    "level": "正处级",
                    "location": "辽宁省锦州市义县",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "县政府党组书记、县长; 兼任锦州七里河经济开发区党工委副书记、管委会主任; 主持县政府全面工作",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002", "S004"],
                },
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中国共产党义县委员会",
                    "title": "县委副书记",
                    "level": "正处级",
                    "location": "辽宁省锦州市义县",
                    "system": "party",
                    "rank": "正处级",
                    "notes": "兼任县委副书记",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S006"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "义县人民政府", "type": "政府",
                 "level": "县处级", "location": "辽宁省锦州市义县"},
                {"org_id": 1, "name": "中国共产党义县委员会", "type": "党委",
                 "level": "县处级", "location": "辽宁省锦州市义县"},
                {"org_id": 7, "name": "锦州七里河经济开发区", "type": "开发区",
                 "level": "省级开发区", "location": "辽宁省锦州市义县七里河镇"},
            ],
            "relationships": [
                {"person": "尤源", "person_id": "yixian_尤源",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "县长与县委书记党政主要领导搭档",
                 "overlap_org": "中国共产党义县委员会/义县人民政府",
                 "overlap_period": "2026年",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002", "S005"]},
                {"person": "迟晓君", "person_id": "yixian_迟晓君",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "县长与常务副县长行政工作搭档",
                 "overlap_org": "义县人民政府",
                 "overlap_period": "2026年",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003", "S004"]},
                {"person": "梁铮", "person_id": "yixian_梁铮",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "原县长与常务副县长搭档（梁铮转任人大前）",
                 "overlap_org": "义县人民政府",
                 "overlap_period": "2025-2026年",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S004", "S005"]},
            ],
            "governance_record": [
                {
                    "period": "2026年7月",
                    "domain": "education",
                    "achievement_or_event": "参加锦州博爱助学项目助学金发放仪式并讲话",
                    "role_in_event": "县长，致辞",
                    "measurable_outcome": "发放助学金11.8万元，帮扶118名困难学生",
                    "location": "锦州市义县",
                    "confidence": "confirmed",
                    "source_ids": ["S006"],
                },
                {
                    "period": "2026年6月",
                    "domain": "governance",
                    "achievement_or_event": "主持义县'两优一先'表彰大会",
                    "role_in_event": "县长，主持会议",
                    "measurable_outcome": "表彰全县先进基层党组织和个人",
                    "location": "锦州市义县",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
                {
                    "period": "2026年7月",
                    "domain": "disaster_prevention",
                    "achievement_or_event": "主持召开防汛工作会议",
                    "role_in_event": "县长，讲话部署",
                    "measurable_outcome": "部署全县防汛工作",
                    "location": "锦州市义县",
                    "confidence": "confirmed",
                    "source_ids": ["S007"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道有限，不足以判断工作风格",
                        "confidence": "unverified",
                        "source_ids": ["S001"],
                    }
                ],
                "speech_themes": [
                    "统筹发展和安全",
                    "压实责任守底线",
                ],
                "management_signals": [
                    {
                        "signal": "实地督导",
                        "evidence": "防汛工作部署要求'靠前指挥'",
                        "confidence": "plausible",
                        "source_ids": ["S007"],
                    }
                ],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "minimal",
                "relationship_confidence": "medium",
                "biggest_gap": "张健的完整履历（出生年月、籍贯、性别、教育背景、任县长前的职业生涯）完全未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "张健的出生年月、籍贯、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["张健 简历 义县", "张健 出生", "张健 百度百科", "锦州 张健 县长"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "张健何时开始担任义县县长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和职业生涯全貌",
                    "suggested_queries": ["张健 任义县县长", "义县 县长 任职公示", "张健 代县长"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "张健的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["张健 工作经历", "张健 此前职务 锦州"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    return {}


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSON files
    person_configs = [
        ("县委书记", "尤源"),
        ("县长", "张健"),
    ]

    for job, name in person_configs:
        data = generate_person_json(job, name)
        if data:
            fname = f"{TODAY}-辽宁省-锦州市-{job}-{name}.json"
            fpath = PERSONS_DIR / fname
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Wrote {fpath}")

    print(f"\nDone. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs in: {PERSONS_DIR}")
