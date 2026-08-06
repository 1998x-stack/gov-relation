#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 长岭县, 松原市, 吉林省.

Level: 县
Province: 吉林省
Parent city: 松原市
Targets: 县委书记 (Party Secretary: 许炳权), 县长 (Mayor: 谭秀权)
Task ID: jilin_长岭县

Research date: 2026-08-06
Official source: http://www.jlcl.gov.cn/ (长岭县人民政府官网)
                + 县融媒体中心新闻 + 政府领导页 (zwgk/xld)

Current status (as of 2026-08-06, verified via 长岭县人民政府官网 政府领导页 + 官方要闻):
- 县委书记: 许炳权 (男，汉族，中共党员；2025年中接替刘英武任长岭县委书记；截至2026年7月主持县委常委会)
- 县委副书记、县长: 谭秀权 (男，汉族，中共党员，1970年7月生；曾任前郭县委办科员→共青团前郭县委副书记→前郭乡镇主政→前郭县副县长→前郭县委常委/统战部长→松原市商务局党组书记、局长；2021.07任长岭县委副书记、代县长，2021.11任县长)
- 前县委书记: 刘国印? (待核实) —— 确认: 刘英武 (2022-06至2025-03任县委书记，2025年离任；去向待查)
- 县委副书记: 李胜 (2026-07 主持"两优一先"表彰大会)

Leadership roster (official 政府领导页 + 县融媒体中心新闻):
- 县长: 谭秀权
- 县委常委、副县长(常务): 赵连敏 (1974.9，大学学历；长岭本地干部，历任县府办/县委办主任，2024.12起任委员、副县长)
- 副县长: 侯立兵 (1970.9；长岭本地，从小学教师→县民政局→县委办→乡镇书记→2021副县长)
- 副县长: 杜国锋 (1977.2；从扶余县乡镇到吉林扶余洪泛湿地省级自然保护区管理局党组书记、局长(副处)；2024.10 长岭副县长)
- 副县长: 于松巍 (从东北师大到市发改委人，2021-11长岭县政协副主席→2024-07长岭副县长)
- 副县长、县公安局局长: 张大为 (1978.9；松原公安交警→2022-09长岭副县长、公安局长)
- 副县长: 张宝峰 (1973.8；长岭公安→信访局长→政府办主任→2025-04长岭副县长)
- 县人大常委会党组书记: 吕雪萍 (2026-05~07 期由县政协党组书记履新人大)  / 县人大常委会主任: 谷青山 (2026-01在任)
- 县政协党组书记: 杨维国 (2026-07)；县政协主席: 吕雪萍 (2026-01)

Predecessor chain (县委书记):
- 许炳权 (2025- 至 present)
- 刘英武 (2022-06至2025-03)
- (更早: 陈德明等, 待查)

Predecessor chain (县长):
- 谭秀权 (2021-07 代 / 2021-11 县长 至今)
- (谭秀权之前县长待查)

Confidence notes:
  许炳权/谭秀权 身份与在任均为 confirmed (官方县官网文章 + 政府领导页 2026).
  政府班子 roster 及各人完整履历为官方政府领导页一手数据 confirmed.
  刘英武为前任县委书记 confirmed (2022-06至2025-03 官方要闻); 其卸任去向与 许炳权 到任精确日期 partial/unverified.
  许炳权 完整履历/籍贯/出生/到任前职务 多为 plausibble/unverified, 已标注于 each JSON open_questions.
  党政群团 (人大/政协/纪委/宣传)成员 role 与 在任 多为 reported via 官方要闻 (吕雪萍/杨维国/李胜/谷青山).
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Locate repo root robustly across staging vs canonical locations.
REPO_ROOT = Path(__file__).resolve().parents[2]
for _pc in (2, 3, 4, 5):
    _candidate = Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "长岭县"
TASK_ID = "jilin_长岭县"

# DB/GEXF + person JSONs always land in the task staging dir.
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / TASK_ID
if _CURRENT_DIR.name == TASK_ID:
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING

AS_OF = "2026-08-06"
TODAY = "20260806"

_PID = "changling"  # person-id prefix for graph dedup across investigations

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── Core: 县委书记 ──
    {
        "id": 1,
        "name": "许炳权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共长岭县委员会",
        "source": "http://www.jlcl.gov.cn/ywdt/zwdt/202607/t20260707_575091.html",
    },
    # ── Core: 县委副书记、县长 ──
    {
        "id": 2,
        "name": "谭秀权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年7月",
        "birthplace": "吉林省松原市前郭县(前郭县成长)",
        "education": "硕士研究生(吉林省委党校法学)",
        "party_join": "中共党员",
        "work_start": "1990年8月",
        "current_post": "县委副书记、县长",
        "current_org": "长岭县人民政府",
        "source": "http://www.jlcl.gov.cn/zwgk/xld/bch_28132/",
    },
    # ── 县委副书记 ──
    {
        "id": 3,
        "name": "李胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "current_post": "县委副书记",
        "current_org": "中共长岭县委员会",
        "source": "http://www.jlcl.gov.cn/ywdt/clyw/202607/t20260707_575087.html",
    },
    # ── 县政府班子: 常务副县长 / 副县长 ──
    {"id": 4, "name": "赵连敏", "gender": "男", "ethnicity": "汉族", "birth": "1974年9月",
     "birthplace": "吉林省松原市长岭县", "education": "大学", "current_post": "县委常委、常务副县长",
     "current_org": "长岭县人民政府", "source": "http://www.jlcl.gov.cn/zwgk/xld/zlm/"},
    {"id": 5, "name": "侯立兵", "gender": "男", "ethnicity": "汉族", "birth": "1970年9月",
     "birthplace": "吉林省松原市长岭县", "education": "大学/自考东北师大汉语言文学", "current_post": "副县长",
     "current_org": "长岭县人民政府", "source": "http://www.jlcl.gov.cn/zwgk/xld/hlbb/"},
    {"id": 6, "name": "杜国锋", "gender": "男", "ethnicity": "汉族", "birth": "1977年2月",
     "birthplace": "吉林省松原市扶余市", "education": "研究生(吉林省委党校经管)", "current_post": "副县长",
     "current_org": "长岭县人民政府", "source": "http://www.jlcl.gov.cn/zwgk/xld/dgf/"},
    {"id": 7, "name": "于松巍", "gender": "男", "ethnicity": "汉族", "birth": "1980年代",
     "birthplace": "", "education": "本科(东北师大环境科学)", "current_post": "副县长",
     "current_org": "长岭县人民政府", "source": "http://www.jlcl.gov.cn/zwgk/xld/dsw/"},
    {"id": 8, "name": "张大为", "gender": "男", "ethnicity": "汉族", "birth": "1978年9月",
     "birthplace": "吉林省松原市", "education": "本科(吉林大学法律自考/公安高专)", "current_post": "副县长、县公安局局长",
     "current_org": "长岭县公安局", "source": "http://www.jlcl.gov.cn/zwgk/xld/zdwfxz/"},
    {"id": 9, "name": "张宝峰", "gender": "男", "ethnicity": "汉族", "birth": "1973年8月",
     "birthplace": "吉林省松原市长岭县", "education": "大学", "current_post": "副县长、县政府办主任",
     "current_org": "长岭县人民政府", "source": "http://www.jlcl.gov.cn/zwgk/xld/fxzzbf/"},

    # ── 人大 / 政协 ──
    {"id": 10, "name": "谷青山", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "current_post": "县人大常委会主任(2026-01在任)", "current_org": "长岭县人大常委会",
     "source": "http://www.jlcl.gov.cn/y/zwdt 2026-01 县委经济工作会议"},
    {"id": 11, "name": "吕雪萍", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "current_post": "县人大常委会党组书记(原县政协主席)", "current_org": "长岭县人大常委会",
     "source": "http://www.jlcl.gov.cn/y/clyw/202607/t20260707_575087.html"},
    {"id": 12, "name": "杨维国", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "current_post": "县政协党组书记", "current_org": "政协长岭县委员会",
     "source": "http://www.jlcl.gov.cn/y/clyw/202607/t20260707_575087.html"},

    # ── 前任 ──
    {"id": 13, "name": "刘英武", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "current_post": "曾任长岭县委书记(2022-2025)", "current_org": "",
     "source": "http://www.jlcl.gov.cn/ywdt/zwdt/202303/t20230327_547834.html"},
    {"id": 14, "name": "张亚昕", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "current_post": "长岭县领导(原/现任, 参与活动)", "current_org": "",
     "source": "http://www.jlcl.gov.cn/ywdt/zwdt/202607/t20260707_575091.html"},
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共长岭县委员会", "type": "党委", "level": "县处级",
     "parent": "中共松原市委员会", "location": "吉林省松原市长岭县"},
    {"id": 2, "name": "长岭县人民政府", "type": "政府", "level": "县处级",
     "parent": "松原市人民政府", "location": "吉林省松原市长岭县"},
    {"id": 3, "name": "长岭县人大常委会", "type": "人大", "level": "县处级",
     "parent": "松原市人大常委会", "location": "吉林省松原市长岭县"},
    {"id": 4, "name": "政协长岭县委员会", "type": "政协", "level": "县处级",
     "parent": "政协松原市委员会", "location": "吉林省松原市长岭县"},
    {"id": 5, "name": "长岭县公安局", "type": "政府", "level": "乡科级",
     "parent": "长岭县人民政府", "location": "吉林省松原市长岭县"},
    {"id": 6, "name": "中共前郭县委办公室", "type": "党委", "level": "县处级",
     "parent": "中共前郭县委", "location": "吉林省松原市前郭县"},
    {"id": 7, "name": "松原市商务局", "type": "政府", "level": "地级市局",
     "parent": "松原市人民政府", "location": "吉林省松原市"},
    {"id": 8, "name": "前郭县人民政府", "type": "政府", "level": "县处级",
     "parent": "松原市人民政府", "location": "吉林省松原市前郭县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 许炳权_县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "约2025年中", "end": "present",
     "rank": "正处级", "note": "接替刘英武; 2026年主导县委常委会, 2026-07 仍为县委书记 (官方要闻)"},
    # 谭秀权_县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "2021年11月", "end": "present",
     "rank": "正处级", "note": "主持县政府全面工作, 分管县审计局"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2021年7月", "end": "present",
     "rank": "副处级", "note": "县委副书记、县长"},
    {"person_id": 2, "org_id": 2, "title": "代县长、副县长", "start": "2021年7月", "end": "2021年11月",
     "rank": "正处级", "note": "2021.07-2021.11任长岭县委副书记、县政府副县长、代县长"},
    {"person_id": 2, "org_id": 7, "title": "松原市商务局党组书记、局长", "start": "2020年9月", "end": "2021年7月",
     "rank": "正处级", "note": "松原市商务局党组副书记、副局长2019.09-2020.09; 2020.09任党组书记、局长"},
    {"person_id": 2, "org_id": 7, "title": "松原市商务局党组副书记、副局长", "start": "2019年9月", "end": "2020年9月",
     "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "前郭县委常委、统战部长", "start": "2016年8月", "end": "2019年9月",
     "rank": "副处级", "note": "2019.03起兼任前郭县政府党组成员"},
    {"person_id": 2, "org_id": 8, "title": "前郭县政府副县长", "start": "2012年11月", "end": "2016年8月",
     "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "前郭县郭尔罗斯工业集中区党工委书记、管委会主任", "start": "2009年8月", "end": "2012年11月",
     "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "前郭县王府站镇党委书记、人大主席", "start": "2005年10月", "end": "2009年8月",
     "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "前郭县招商局局长", "start": "2003年11月", "end": "2005年10月",
     "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "前郭县乌兰图嘎镇党委书记、人大主席", "start": "2003年2月", "end": "2003年11月",
     "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "前郭县达里巴乡党委书记、人大主席", "start": "1999年4月", "end": "2003年2月",
     "rank": "正科级", "note": "其间参加新加坡南洋理工培训班"},
    {"person_id": 2, "org_id": 8, "title": "共青团前郭县委副书记", "start": "1994年9月", "end": "1999年4月",
     "rank": "副科级", "note": "其间吉林省委党校经济管理专业本科"},
    {"person_id": 2, "org_id": 6, "title": "中共前郭县委办公室科员", "start": "1990年8月", "end": "1994年9月",
     "rank": "科员", "note": "起步职"},
    # 李胜_县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "2026-07 主持'两优一先'表彰大会"},
    # 赵连敏_常务副县长
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start": "2024年11月", "end": "present",
     "rank": "副处级", "note": "协助县长分管发改、工信、商务、招商、自然资源、开发区等"},
    {"person_id": 4, "org_id": 1, "title": "县委常委、县委办公室主任", "start": "2023年8月", "end": "2024年12月",
     "rank": "副处级", "note": "2023.08-2024.11 县委办主任; 2022.05-2023.08 县委办主任"},
    # 侯立兵
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "2021年9月", "end": "present",
     "rank": "副处级", "note": "分管农业农村、乡村振兴、林业、水利等"},
    # 杜国锋
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "2024年10月", "end": "present",
     "rank": "副处级", "note": "2024-10 长岭县政府副县长人选(履新)"},
    # 于松巍
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "2024年7月", "end": "present",
     "rank": "副处级", "note": "2024.07由长岭县政协副主席转任副县长"},
    # 张大为
    {"person_id": 8, "org_id": 5, "title": "副县长、公安局党委书记、局长", "start": "2022年9月", "end": "present",
     "rank": "副处级", "note": "兼任县公安局局长"},
    # 张宝峰
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "2025年4月", "end": "present",
     "rank": "副处级", "note": "2025.04-长岭县副县长并兼县政府办主任"},
    # 谷青山 / 吕雪萍 / 杨维国
    {"person_id": 10, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "2026年(在任2026-01)",
     "rank": "正处级", "note": "2026-01县委经济工作会议出席"},
    {"person_id": 11, "org_id": 3, "title": "县人大常委会党组书记", "start": "2026年(约5-6月)", "end": "present",
     "rank": "正处级", "note": "原县政协主席履新人大党组书记 2026-07 报道"},
    {"person_id": 11, "org_id": 4, "title": "县政协主席", "start": "", "end": "2026年(初在任)",
     "rank": "正处级", "note": "2026-01 县政协主席"},
    {"person_id": 12, "org_id": 4, "title": "县政协党组书记", "start": "2026年", "end": "present",
     "rank": "正处级", "note": "2026-07 报道"},
    # 刘英武_前任县委书记
    {"person_id": 13, "org_id": 1, "title": "县委书记", "start": "2022年", "end": "2025年3月",
     "rank": "正处级", "note": "2022-06至2025-03 官方要闻可考在任"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 许炳权 ↔ 谭秀权 (党政一把手 2026)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县委副书记、县长，党政主要领导班子成员",
     "overlap_org": "中共长岭县委员会/长岭县人民政府", "overlap_period": "2025年中-2026"},
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县委副书记、县长；县委县政府正副两套班子主要搭档",
     "overlap_org": "中共长岭县委员会", "overlap_period": "2025年中-2026"},
    # 许炳权 ↔ 刘英武 (前任书记交接)
    {"person_a": 1, "person_b": 13, "type": "predecessor_successor",
     "context": "许炳权接替刘英武任长岭县委书记",
     "overlap_org": "中共长岭县委员会", "overlap_period": "2025年交接"},
    # 谭秀权 ↔ 刘英武 (前任书记任期内的县长)
    {"person_a": 2, "person_b": 13, "type": "overlap",
     "context": "刘英武任县委书记期间谭秀权任县长(前党政班子)",
     "overlap_org": "中共长岭县委员会/长岭县人民政府", "overlap_period": "2022-2025"},
    # 谭秀权 ↔ 各副县长 (县府班子)
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与常务副县长工作搭档", "overlap_org": "长岭县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "县长与副县长工作搭档", "overlap_org": "长岭县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "县长与副县长工作搭档", "overlap_org": "长岭县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "县长与副县长工作搭档", "overlap_org": "长岭县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "县长与副县长、公安局长工作搭档", "overlap_org": "长岭县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "县长与副县长工作搭档", "overlap_org": "长岭县人民政府", "overlap_period": "截至2026-08"},
    # 常务副县长 ↔ 各副 (县府班子同僚)
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "县政府领导班子同事",
     "overlap_org": "长岭县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "县政府领导班子同事",
     "overlap_org": "长岭县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "县政府领导班子同事",
     "overlap_org": "长岭县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "县政府领导班子同事",
     "overlap_org": "长岭县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "县政府领导班子同事",
     "overlap_org": "长岭县人民政府", "overlap_period": "截至2026-08"},
    # 人大 / 政协 交接 (吕雪萍: 政协主席→人大党组书记; 杨维国→政协)
    {"person_a": 11, "person_b": 12, "type": "predecessor_successor",
     "context": "杨维国接替吕月萍出任县政协(党组书记)工作",
     "overlap_org": "政协长岭县委员会", "overlap_period": "2026年交接"},
    {"person_a": 10, "person_b": 11, "type": "predecessor_successor",
     "context": "吕月萍(人大党组书记)接替谷青山挑大族人大常委会工作",
     "overlap_org": "长岭县人大常委会", "overlap_period": "2026年交接"},
    # 县委副书记李胜
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委副书记工作搭档", "overlap_org": "中共长岭县委员会", "overlap_period": "截至2026-07"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "县委副书记同在县委班子", "overlap_org": "中共长岭县委员会", "overlap_period": "截至2026-07"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS: source register + person JSON
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "长岭县人民政府官网-政府领导-县长谭秀权",
         "url": "http://www.jlcl.gov.cn/zwgk/xld/bch_28132/", "publisher": "长岭县人民政府",
         "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "谭秀权：男,汉族,中共党员,1970年7月生; 完整履历 (前郭县委办→共青团前郭→前郭乡镇→前郭副县长→松原商务局→2021-07长岭代县长,2021-11县长)"},
        {"id": "S002", "title": "长岭县人民政府官网·政府领导页(班子清单)",
         "url": "http://www.jlcl.gov.cn/zwgk/", "publisher": "长岭县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "县长谭秀权、常务副县长赵连敏、副县长侯立兵/杜国锋/于松巍/张大为/张宝峰"},
        {"id": "S003", "title": "许炳权开展'七一'走访慰问活动",
         "url": "http://www.jlcl.gov.cn/ywdt/zwdt/202607/t20260707_575091.html", "publisher": "长岭县融媒体中心",
         "published_at": "2026-06-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "'县委书记许炳权走访慰问…'; 张亚昕参加活动"},
        {"id": "S004", "title": "县委常委会召开会议",
         "url": "http://www.jlcl.gov.cn/ywdt/zyhy/202607/t20260707_575095.html", "publisher": "长岭县融媒体中心",
         "published_at": "2026-06-27", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "'县委书记许炳权主持召开2026年第11次县委常委会会议'"},
        {"id": "S005", "title": "谭秀权调研春耕生产等重点工作",
         "url": "http://www.jlcl.gov.cn/ywdt/clyw/202605/t20260506_571842.html", "publisher": "长岭县融媒体中心",
         "published_at": "2026-05-02", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "'县委副书记、县长谭秀权' 开展调研"},
        {"id": "S006", "title": "许炳权 谭秀权到长岭经济开发区调研",
         "url": "http://www.jlcl.gov.cn/ywdt/clyw/202603/t20260312_568899.html", "publisher": "长岭县融媒体中心",
         "published_at": "2026-03-12", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "'县委书记许炳权,县委副书记、县长谭秀权' 共同调研"},
        {"id": "S007", "title": "县委经济工作会议召开",
         "url": "http://www.jlcl.gov.cn/ywdt/clyw/202602/t20260211_567847.html", "publisher": "长岭县融媒体中心",
         "published_at": "2026-01-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "'县委书记许炳权…县委副书记、县长谭秀权…县人大常委会主任谷青山、县政协主席吕雪萍出席'; 确认2026-01人大主任谷青山、政协主席吕雪萍"},
        {"id": "S008", "title": "长岭县'两优一先'表彰大会召开",
         "url": "http://www.jlcl.gov.cn/ywdt/clyw/202607/t20260707_575087.html", "publisher": "长岭县融媒体中心",
         "published_at": "2026-07-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "'县委书记许炳权…县人大常委会党组书记吕雪萍、县政协党组书记杨维国出席; 县委副书记李胜主持' ; 确认2026-07人大党组书记吕雪萍、政协党组书记杨维国"},
        {"id": "S009", "title": "长岭县政府2025年第15次常务会议",
         "url": "http://www.jlcl.gov.cn/ywdt/clyw/202601/t20260112_565275.html", "publisher": "长岭县融媒体中心",
         "published_at": "2025-12-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "'县委副书记、县长谭秀权主持召开…赵连敏、刘爽、侯立兵、杜国锋、于庆巍、张宝峰参加会议' ; 确认政府班子"},
        {"id": "S010", "title": "刘英武会见刘忠新一行",
         "url": "http://www.jlcl.gov.cn/ywdt/zwdt/202503/t20250327_547834.html", "publisher": "长岭县融媒体中心",
         "published_at": "2025-03-27", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "'县委书记刘英武' 最后一次可考公开活动 (2025-03); 之前22-06起即有"},
        {"id": "S011", "title": "刘英武调研城市建设工作",
         "url": "http://www.jlcl.gov.cn/ywdt/clyw/202408/t20240823_533741.html", "publisher": "长岭县融媒体中心",
         "published_at": "2024-08-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "'县委书记刘英武…邹立辉、张亚昕、赵连敏,张大为参加检查'; 确认前任书记及部分县领导"},
        {"id": "S012", "title": "长岭县政仿调研全县乡镇街道综合行政执法情况",
         "url": "http://www.jlcl.gov.cn/ywdt/clyw/202406/t20240620_529245.html", "publisher": "长岭县融媒体中心",
         "published_at": "2024-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "medium",
         "notes": ""},
        {"id": "S013", "title": "长岭县人民政府关于李勇等同志职务任免的通知(2025-12)",
         "url": "http://xxgk.jlcl.gov.cn/clxrmzf/clmzfbgs/gkml_19224/202512/t20251215_563548.html",
         "publisher": "长岭县人民政府", "published_at": "2025-12-15", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "长政干任〔2025〕5号 人事任免 (李勇等同志调动)"},
        {"id": "S014", "title": "赵连敏 简历",
         "url": "http://www.jlcl.gov.cn/zwgk/xld/zlm/", "publisher": "长岭县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "赵连敏男汉族1974.9大学; 长岭本地/县委办/县府办成长,2024-11起常委副县长"},
        {"id": "S015", "title": "杜国锋 简历",
         "url": "http://www.jlcl.gov.cn/zwgk/xld/dgf/", "publisher": "长岭县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "杜国锋男汉族1977.2; 扶余乡镇→扶余洪泛湿地自然保护局长→2024-10长岭副县长"},
        {"id": "S016", "title": "于松巍 简历",
         "url": "http://www.jlcl.gov.cn/zwgk/xld/dsw/", "publisher": "长岭县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "东北师大→松原市发改委→2021长岭县政协副主席→2024-07长岭副县长"},
    ]


def generate_person_json(job: str, name: str) -> dict:
    pid = f"{_PID}_{name}"
    base = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "吉林省", "city": "松原市", "region": "长岭县",
                                "job": job, "task_id": "jilin_长岭县", "time_focus": "2023–2026"},
        "current_status": {"current_org": "", "administrative_rank": "正处级", "as_of": AS_OF,
                           "is_current_confirmed": True, "source_ids": ["S001"]},
        "organizations": [
            {"org_id": 1, "name": "中共长岭县委员会", "type": "党委", "level": "县处级",
             "location": "吉林省松原市长岭县"},
            {"org_id": 2, "name": "长岭县人民政府", "type": "政府", "level": "县处级",
             "location": "吉林省松原市长岭县"},
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [],
                                 "career_pattern": "cross_county_rotation", "systems_experience": [],
                                 "geographic_pattern": ["松原市"],
                                 "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [],
                                       "management_signals": [],
                                       "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": make_source_register(),
        "open_questions": [],
    }
    base["identity"] = {}
    base["career_timeline"] = []

    if name == "许炳权":
        base["identity"] = {
            "person_id": pid, "name": "许炳权", "aliases": [], "gender": "男",
            "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "",
            "education": [], "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "许炳权_", "name_birthplace": "许炳权_",
                            "official_profile_url": ""},
        }
        base["current_status"]["current_post"] = "县委书记"
        base["current_status"]["current_org"] = "中共长岭县委员会"
        base["current_status"]["source_ids"] = ["S003", "S004", "S006"]
        base["career_timeline"] = [
            {"start": "unknown", "end": "2025年", "org": "", "title": "许炳权任县委书记前职务",
             "level": "", "location": "", "system": "party", "rank": "",
             "is_key_promotion": False, "notes": "公开资料不足，未还原到任前履历 (可能为松原市直或松原其他县区交流干部)", "confidence": "unverified",
             "source_ids": []},
            {"start": "2025年中", "end": "present", "org": "中共长岭县委员会", "title": "县委书记",
             "level": "正处级", "location": "吉林省松原市长岭县", "system": "party", "rank": "正处级",
             "is_key_promotion": True, "notes": "接替刘英武; 2026-01起主持县委常委会/党代会大会; 2026-07仍在任", "confidence": "confirmed",
             "source_ids": ["S003", "S004", "S006"]},
        ]
        base["relationships"] = [
            {"person": "谭秀权", "person_id": f"{_PID}_谭秀权", "relationship_type": "overlap",
             "strength": "strong", "evidence": "县委书记与县长党政主要搭档(2025-2026)",
             "overlap_org": "中共长岭县委员会/长岭县人民政府", "overlap_period": "2025年中-2026",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
            {"person": "刘英武", "person_id": f"{_PID}_刘英武", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "许炳权接替刘英武任县委书记",
             "overlap_org": "中共长岭县委员会", "overlap_period": "2025交接", "direction": "undirected",
             "confidence": "plausible", "source_ids": ["S010"]},
        ]
        base["governance_record"] = [
            {"period": "2026年6月", "domain": "public_security",
             "achievement_or_event": "主持召开县委常委会研究防汛抗旱、东西部协作与粮食安全部署, 提出主动权思想抓防汛",
             "role_in_event": "县委书记", "measurable_outcome": "",
             "location": "长岭县", "confidence": "confirmed", "source_ids": ["S004"]},
        ]
        base["professional_profile"]["career_pattern"] = "cross_county_rotation"
        base["professional_profile"]["geographic_pattern"] = ["松原市"]
        base["professional_profile"]["primary_specializations"] = ["党的建设", "县域治理"]
        base["confidence_summary"] = {
            "identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "许炳权的出生/籍贯/毕业院校、到任前职务与履历、精确到任时间节点"}
        base["open_questions"] = [
            {"priority": "critical", "question": "许炳权任长岭县委书记前的完整履历与职务？",
             "why_it_matters": "还原核心一把手履历", "suggested_queries": ["许炳权 简历 长岭", "许炳权 任前公示"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": "许炳权何时由何职位接任长岭县委书记？(任前公示/精确时间)",
             "why_it_matters": "精确交接时间与任命机制",
             "suggested_queries": ["许炳权 长岭县委书记 任命", "刘英武 卸任 长岭县委书记"], "last_attempted": AS_OF},
            {"priority": "high", "question": "许炳权的出生日期、籍贯、毕业院校？",
             "why_it_matters": "身份去重与完整档案", "suggested_queries": ["许炳权 简历"], "last_attempted": AS_OF},
        ]
        return base

    # ── 谭秀权 (县长) ──
    base["identity"] = {
        "person_id": pid, "name": "谭秀权", "aliases": [], "gender": "男", "ethnicity": "汉族",
        "birth": "1970年7月", "birthplace": "吉林省松原市(前郭县成长)", "native_place": "",
        "education": [{"period": "2003-2006", "institution": "吉林省委党校", "major": "法学", "degree": "硕士",
                       "study_type": "party_school", "source_ids": ["S001"]}],
        "party_join": "中共党员", "work_start": "1990年8月",
        "dedupe_keys": {"name_birth": "谭秀权_197007", "name_birthplace": "谭秀权_吉林",
                        "official_profile_url": "http://www.jlcl.gov.cn/zwgk/xld/bch_28132/"},
    }
    base["current_status"]["current_post"] = "县长"
    base["current_status"]["current_org"] = "长岭县人民政府"
    base["current_status"]["source_ids"] = ["S001", "S005"]
    tls = [
        ("1990年8月", "1994年9月", "中共前郭县委办公室", "科员", "confirmed", "S001"),
        ("1994年9月", "1999年4月", "共青团前郭县委", "副书记(其间党校经管本科)", "confirmed", "S001"),
        ("1999年4月", "2003年2月", "前郭县达里巴乡", "党委书记、人大主席", "confirmed", "S001"),
        ("2003年2月", "2003年11月", "前郭县乌兰图嘎镇", "党委书记、人大主席", "confirmed", "S001"),
        ("2003年11月", "2005年10月", "前郭县招商局", "局长", "confirmed", "S001"),
        ("2005年10月", "2009年8月", "前郭县王府站镇", "党委书记、人大主席(法学硕士)", "confirmed", "S001"),
        ("2009年8月", "2012年11月", "前郭县郭尔罗斯工业集中区", "党工委书记、管委会主任", "confirmed", "S001"),
        ("2012年11月", "2016年8月", "前郭县人民政府", "副县长", "confirmed", "S001"),
        ("2016年8月", "2019年9月", "中共前郭县委", "常委、统战部长(2019.03起兼县政府党组成员)", "confirmed", "S001"),
        ("2019年9月", "2020年9月", "松原市商务局", "党组副书记、副局长", "confirmed", "S001"),
        ("2020年9月", "2021年7月", "松原市商务局", "党组书记、局长", "confirmed", "S001"),
        ("2021年7月", "2021年11月", "长岭县人民政府", "县委副书记、副县长、代县长", "confirmed", "S001"),
        ("2021年11月", "present", "长岭县人民政府", "县委副书记、县长", "confirmed", "S001"),
    ]
    base["career_timeline"] = [
        {"start": s, "end": e, "org": o, "title": t, "level": "", "location": "吉林省松原市",
         "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": c,
         "source_ids": [sid]} for s, e, o, t, c, sid in tls
    ]
    base["career_timeline"][-1]["is_key_promotion"] = True
    base["relationships"] = [
        {"person": "许炳权", "person_id": f"{_PID}_许炳权", "relationship_type": "overlap",
         "strength": "strong", "evidence": "县长与县委书记党政主要搭档(2025-2026)",
         "overlap_org": "中共长岭县委员会/长岭县人民政府", "overlap_period": "2025年中-2026",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005", "S006"]},
    ]
    base["governance_record"] = [
        {"period": "2026年5月", "domain": "rural_revitalization",
         "achievement_or_event": "调研春耕生产、生态环境保护、道路交通安全、项目建设等重点工作,实地督查元素项目建设和污水处理厂等",
         "role_in_event": "县长", "measurable_outcome": "部署春耕气象服务、规范污水处理厂施工、加快建设工程", "location": "长岭县",
         "confidence": "confirmed", "source_ids": ["S005"]},
    ]
    base["professional_profile"]["career_pattern"] = "local_ladder"
    base["professional_profile"]["geographic_pattern"] = ["松原市(前郭→长岭)"]
    base["professional_profile"]["systems_experience"] = ["government", "party", "organization"]
    base["professional_profile"]["primary_specializations"] = ["县域治理", "商务/经贸"]
    base["professional_profile"]["promotion_velocity"]["summary"] = "从基层县办/乡镇/县级县域主管到松原市直部门再到县域把县 (县长), 稳步型晋升"
    base["confidence_summary"] = {
        "identity": "confirmed", "current_role": "confirmed", "career_completeness": "complete",
        "relationship_confidence": "high",
        "biggest_gap": "谭秀权出生年月具体日/籍贯乡镇; 出生地与1968年吉省地背景; 共产相关信息未列入详细public"}
    base["open_questions"] = [
        {"priority": "medium", "question": "谭秀权的前郭县成长背景、出生籍贯具体乡镇？",
         "why_it_matters": "完整身份档案", "suggested_queries": ["谭秀权 籍贯 出生"], "last_attempted": AS_OF},
        {"priority": "low", "question": "谭秀权在2021-07代县长前的过渡 (前县长是谁、去向)？",
         "why_it_matters": "还原前任县长流动", "suggested_queries": ["长岭县 前任县长 2021"], "last_attempted": AS_OF},
    ]
    return base


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import os
    # remove stale outputs before each run
    for p in (DB_PATH, GEXF_PATH):
        if p.exists():
            try:
                p.unlink()
            except OSError:
                pass

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
    for job, name in [("县委书记", "许炳权"), ("县长", "谭秀权")]:
        data = generate_person_json(job, name)
        fname = f"{TODAY}-吉林省-松原市-{job}-{name}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Wrote {fpath}")

    print(f"\nDone. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs in: {PERSONS_DIR}")