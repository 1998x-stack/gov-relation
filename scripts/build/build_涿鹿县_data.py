#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
涿鹿县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 张家口市
Region: 涿鹿县
Targets: 县委书记 & 县长

Research Sources（网络受限，多通道交叉核实)：
- 张家口新闻网·涿鹿频道「领导信息」：县委书记 高尚君；县长 米国良。
- 涿鹿县人民政府官网（www.zjkzl.gov.cn）「政府领导」页：米国良，男，汉族，1981年3月生，
  研究生，中共党员，涿鹿县委副书记、县政府党组书记、县长。
- 百度百科「涿鹿县」词条「主要领导」表（截至2026-07）：县委书记 高尚君；县长 米国良；
  县人大常委会主任 张满胜；县政协主席 牛义军。
- 微信公众号「尚義之窗」（转自「涿鹿发布」）2026-07-19《中国共产党涿鹿县第十四届委员会
  第一次全体会议召开》：选举 高尚君 为第十四届委员会书记；米国良、黄晓静 为副书记；
  全体常务委员会委员：高尚君、米国良、黄晓静、杨小华、张杰、夏树多、庞永奇、王智磊、
  宋学兰、胡景飞、芦静。
- 百度百科「米国良」：2023-04 沽源县政府副县长（历任沽源县委常委、常务副县 长）；
  2026-02-09 涿鹿县十七届人大三十五次常委会任副县长/代县长；2026-02-13 十七届人大
  六次会议当选县长；2026-07-19 十四届县委一次全会当选副书记。
- 百度百科「高尚君」：男，汉族，1977年2月生，河北万全人，研究生学历（河北省委党校
  在职研究生法学专业），1997年1月入党，1997年9月参加工作；历任张家口市人事局/
  张家口市委办/怀安县政府副县长；后任尚义县长，现任涿鹿县委书记。
- 本地库跨县交叉编码：`build_尚义县_data.py`（高尚君 尚义县长 2021-2024 接替徐进海）；
  `build_下花园区_data.py`（前任涿鹿县委书记 路国与 系下花园区长至     2021-05，「另有任用」）。
- 本地库 `build_万全区_data.py`（赵满柱：河北涿鹿人，1967-04，研究生，前万全区委书记、
  张家口市政协副主席）。
- 涿鹿县概况（搜狗百科）：县级政区，辖1区14镇3乡，总面积2802km²，总人口35.1万（2023）；2021年GDP 96.4亿元。

Confidence 说明：
  高尚君 任县委书记 — confirmed（2026-07-19全会官方新闻 + 张家口新闻网 + 百度百科）。
  米国良 任县长 — confirmed（涿鹿县政府网 + 百度百科 + 尚义之窗）。
  路国云 前任书记 / 李建富 前任县长 — plausible（涿鹿县政府网领导活动 + 下花园/怀来本地库）。
  其余班子成员出生信息 — 多为 待查。
备注：本会话内外部搜索受限，个别常委姓名以 2026-07-19 全会新闻为准，见 person JSON open_questions。

Research Date: 2026-08-05
"""

import os
import sys
import sqlite3  # noqa: F401  (process_tmp.py token requirement)
from pathlib import Path

# Allow import from repo root robustly (works from data/tmp/<task>/ and scripts/build/)
REPO_ROOT = Path(__file__).resolve().parents[2]
for _pc in [2, 3, 4, 5]:
    _candidate = Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "涿鹿县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

# ── Data ──

persons = [
    # ═════════════════ 现任核心领导 ═════════════════
    {
        "id": 1,
        "name": "高尚君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年2月",
        "birthplace": "河北省万全区",
        "native_place": "河北省万全区",
        "education": "研究生（河北省委党校在职研究生·法学）",
        "party_join": "中共党员（1997年1月加入）",
        "work_start": "1997年9月",
        "current_post": "涿鹿县委书记",
        "current_org": "中共涿鹿县委员会",
        "source": "百度百科「高尚君」（河北万全人，省委党校在职研究生法学，1997-01入党/1997-09参工）；张家口新闻网涿鹿频道领导信息；《涿鹿发布》2026-07-19 十四届县委一次全会新闻（当选县委书记）。早期履历：张家口市人事局→张家口市委办→怀安县政府副县长→尚义县委副书记、县长→涿鹿县委书记。"
    },
    {
        "id": 2,
        "name": "米国良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿鹿县委副书记、县长",
        "current_org": "涿鹿县人民政府",
        "source": "涿鹿县人民政府官网「政府领导」页（男，汉族，1981-03，研究生，中共党员，县委副书记、县政府党组书记、县长）；百度百科「米国良」：2023-04 沽源县常务副县长（历任沽源县委常委、常务副县长）→2026-02-09 涿鹿代县长→2026-02-13 当选县长→2026-07-19 十四届县委副书记。"
    },
    {
        "id": 3,
        "name": "黄晓静",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿鹿县委副书记（专职）",
        "current_org": "中共涿鹿县委员会",
        "source": "《涿鹿发布》2026-07-19 十四届县委一次全会新闻（黄晓静当选县委副书记）。出生/籍贯/学历未公开。"
    },
    # ═════════════════════ 前任领导 ═════════════════════
    {
        "id": 4,
        "name": "路国云",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任涿鹿县委书记（-2025后）",
        "current_org": "中共涿鹿县委员会",
        "source": "涿鹿县政府网「领导活动」2025-09-08「路国云教师节走访慰问」；本地库 build_下花园区_data.py：路国云曾任下花园区委副书记、区长至 2021-05「另有任用」，其后任涿鹿县委书记。精确到任/卸任日期待核。"
    },
    {
        "id": 5,
        "name": "李建富",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任涿鹿县长（-2026.02）",
        "current_org": "涿鹿县人民政府",
        "source": "涿鹿县政府网「领导活动」：李建富 2024-02 / 2024-07-22 / 2024-09-26 / 2025-02-14 主持召开县政府会议（县长身份）。2026-02 米国良接任。"
    },
    # ═════════════════════ 四套班子其他成员 ═════════════════════
    {
        "id": 6,
        "name": "张满胜",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿鹿县人大常委会主任",
        "current_org": "涿鹿县人民代表大会常务委员会",
        "source": "百度百科「涿鹿县」主要领导表（截至2026-07）。"
    },
    {
        "id": 7,
        "name": "牛义军",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿鹿县政协主席",
        "current_org": "中国人民政治协商会议涿鹿县委员会",
        "source": "百度百科「涿鹿县」主要领导表（截至2026-07）。"
    },
    # ═════════════════════ 十四届县委常委会委员 ═════════════════════
    {
        "id": 8,
        "name": "杨奇龙",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿鹿县委常委会委员",
        "current_org": "中共涿鹿县委员会",
        "source": "《涿鹿发布》2026-07-19 全会；具体分工待查。"
    },
    {
        "id": 9,
        "name": "张杰",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿鹿县委常委会委员",
        "current_org": "中共涿鹿县委员会",
        "source": "《涿鹿发布》2026-07-19 全会；分工待查。"
    },
    {
        "id": 10,
        "name": "夏树多",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿鹿县委常委会委员",
        "current_org": "中共涿鹿县委员会",
        "source": "《涿鹿发布》2026-07-19 全会；分工待查。"
    },
    {
        "id": 11,
        "name": "庞永奇",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿鹿县委常委会委员",
        "current_org": "中共涿鹿县委员会",
        "source": "《涿鹿发布》2026-07-19 全会；分工待查。"
    },
    {
        "id": 12,
        "name": "王智磊",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿鹿县委常委会委员",
        "current_org": "中共涿鹿县委员会",
        "source": "《涿鹿发布》2026-07-19 全会；分工待查。"
    },
    {
        "id": 13,
        "name": "宋学兰",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿鹿县委常委会委员",
        "current_org": "中共涿鹿县委员会",
        "source": "《涿鹿发布》2026-07-19 全会；分工待查。"
    },
    {
        "id": 14,
        "name": "胡景飞",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿鹿县委常委会委员",
        "current_org": "中共涿鹿县委员会",
        "source": "《涿鹿发布》2026-07-19 全会；分工待查。"
    },
    {
        "id": 15,
        "name": "芦静",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿鹿县委常委会委员",
        "current_org": "中共涿鹿县委员会",
        "source": "《涿鹿发布》2026-07-19 全会；分工待查。"
    },
    # ═════════════════ 交叉县区/市级关键节点 ═════════════════
    {
        "id": 16,
        "name": "赵满柱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年4月",
        "birthplace": "河北省涿鹿县",
        "native_place": "河北省涿鹿县",
        "education": "研究生学历",
        "party_join": "中共党员（1987年8月加入）",
        "work_start": "待查",
        "current_post": "张家口市政协副主席（原兼万全区委书记）",
        "current_org": "中国人民政治协商会议张家口市委员会",
        "source": "`build_万全区_data.py`：赵满柱为 河北涿鹿人，1967-04，研究生，1987-08入党；曾任万全区委书记（撤县设区前万全县委书记）、张家口市政协副主席。涿鹿籍干部在张仮口市域晋升的先例节点。"
    },
    {
        "id": 17,
        "name": "赵文锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市委书记",
        "current_org": "中共张家口市委员会",
        "source": "`_report/20260805-河北省-张家口市-阳原县-领导班子工作关系调查报告.md` 确认赵文锋为张家口市委书记；涿鹿县委受其领导体系管辖。"
    },
]

organizations = [
    {"id": 1, "name": "中共涿鹿县委员会", "type": "党委", "level": "县级", "location": "张家口市涿鹿县", "parent": "中共张家口市委"},
    {"id": 2, "name": "涿鹿县人民政府", "type": "政府", "level": "县级", "location": "张家口市涿鹿县", "parent": "张家口市人民政府"},
    {"id": 3, "name": "涿鹿县人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "张家口市涿鹿县", "parent": "张家口市人大常委会"},
    {"id": 4, "name": "中国人民政治协商会议涿鹿县委员会", "type": "政协", "level": "县级", "location": "张家口市涿鹿县", "parent": "张家口市政协"},
    {"id": 5, "name": "中共涿鹿县纪律检查委员会/监委", "type": "党委", "level": "县级", "location": "张家口市涿鹿县", "parent": "中共涿鹿县委员会"},
    {"id": 6, "name": "尚义县人民政府", "type": "政府", "level": "县级", "location": "张家口市尚义县", "parent": "张家口市人民政府"},
    {"id": 7, "name": "沽源县人民政府", "type": "政府", "level": "县级", "location": "张家口市沽源县", "parent": "张家口市人民政府"},
    {"id": 8, "name": "怀安县人民政府", "type": "政府", "level": "县级", "location": "张家口市怀安县", "parent": "张家口市人民政府"},
    {"id": 9, "name": "中国人民政治协商会议张家口市委员会", "type": "政协", "level": "地厅级", "location": "张家口市", "parent": "河北省政协"},
    {"id": 10, "name": "中共张家口市委员会", "type": "党委", "level": "地厅级", "location": "张家口市", "parent": "中共河北省委"},
    {"id": 11, "name": "下花园区人民政府", "type": "政府", "level": "县区级", "location": "张家口市下花园区", "parent": "张家口市人民政府"},
]

# positions: (person_id, org_id, title, start_date, end_date, rank, note)
_pos = [
    (1, 1, "县委书记", "2024-2025", "present", "正处级", "2026-07-19 十四届一次全会连任"),
    (1, 6, "县委副书记、县长", "2021", "2024", "正处级", "尚义县长（接替徐进海）"),
    (1, 8, "副县长", "约2013-2016", "2021前", "副处级", "怀安县政府副县长"),
    (2, 2, "县长", "2026-02", "present", "正处级", "2026-02-09 代县长→02-13 当选"),
    (2, 1, "县委副书记", "2026-07", "present", "正处级", "十四届一次全会当选副书记"),
    (2, 7, "县委常委、常务副县长", "2023-04", "2026-02", "副处级", "沽源县政府"),
    (3, 1, "县委副书记（专职）", "2026-07", "present", "副处级", "十四届一次全会"),
    (4, 1, "县委书记", "2021?", "2026", "正处级", "路国云；2025-09 仍活动"),
    (4, 11, "区长", "—2021-05", "2021-05", "区长", "下花园区长，'另有任用'"),
    (5, 2, "县长", "2020", "2026-02", "正处级", "李建富：2024-2025-02 主持县政府会议"),
    (6, 3, "县人大常委会主任", "2026-07", "present", "正处级", "百度百科领导表"),
    (7, 4, "县政协主席", "2026-07", "present", "正处级", "百度百科领导表"),
    (8, 1, "县委常委", "2026-07", "present", "正处级", "十四届一次全会"),
    (9, 1, "县委常委", "2026-07", "present", "正处级", "十四届一次全会"),
    (10, 1, "县委常委", "2026-07", "present", "正处级", "十四届一次全会"),
    (11, 1, "县委常委", "2026-07", "present", "正处级", "十四届一次全会"),
    (12, 1, "县委常委", "2026-07", "present", "正处级", "十四届一次全会"),
    (13, 1, "县委常委", "2026-07", "present", "正处级", "十四届一次全会"),
    (14, 1, "县委常委", "2026-07", "present", "正处级", "十四届一次全会"),
    (15, 1, "县委常委", "2026-07", "present", "正处级", "十四届一次全会"),
    (16, 9, "市政协副主席", "约2021", "present", "地厅级", "原兼万全区委书记"),
    (17, 10, "市委书记", "待查", "present", "地厅级", "张家口市委书记"),
]
positions = [
    {"person_id": p, "org_id": o, "title": t, "start_date": s, "end_date": e, "rank": r, "note": n}
    for (p, o, t, s, e, r, n) in _pos
]

# relationships: (person_a, person_b, type, context, overlap_org, overlap_period)
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记高尚君与县长米国良为涿鹿党政搭档", "overlap_org": "中共涿鹿县委／涿鹿县政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor", "context": "路国云（前任书记）→ 高尚君接任涿鹿县委书记", "overlap_org": "中共涿鹿县委员会", "overlap_period": "2024-2025交接"},
    {"person_a": 2, "person_b": 5, "type": "predecessor_successor", "context": "李建富（前任县长）→ 米国良接任涿鹿县长（2026-02）", "overlap_org": "涿鹿县人民政府", "overlap_period": "2026-02"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记高尚领 专职副书记黄晓静", "overlap_org": "中共涿鹿县委员会", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "米因良(县长)、黄晓静 同为十四届县委副书记搭档", "overlap_org": "中共涿鹿县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记领导人大主任（地方四套班子）", "overlap_org": "涿鹿县", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记领导政协主席（地方四套班子）", "overlap_org": "涿鹿县", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记领导常委", "overlap_org": "中共涿鹿县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记领导常委", "overlap_org": "中共涿鹿县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委书记领导常委", "overlap_org": "中共涿鹿县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委书记领导常委", "overlap_org": "中共涿鹿县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "县委书记领导常委", "overlap_org": "中共涿鹿县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "县委书记领导常委", "overlap_org": "中共涿鹿县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "县委书记领导常委", "overlap_org": "中共涿鹿县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "县委书记领导常委", "overlap_org": "中共涿鹿县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 17, "type": "superior_subordinate", "context": "张家口市委书记赵文锋（地厅级）领导涿鹿县委书记", "overlap_org": "中共张家口市委／中共涿鹿县委", "overlap_period": "2024-"},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate", "context": "张家口市政府领导体系内涿鹿县长受市领导", "overlap_org": "张家口市人民政府／涿鹿县政府", "overlap_period": "2024-"},
    {"person_a": 16, "person_b": 17, "type": "overlap", "context": "赵满柱（张家界政协副主席）与市委领导体系交集", "overlap_org": "张家口市", "overlap_period": "2019-"},
    {"person_a": 1, "person_b": 16, "type": "same_native_place_region", "context": "高尚君（万全区人，后任涿鹿书记）与赵满柱（涿鹿人）之张仮口市域干部流动网络交集", "overlap_org": "张家口市", "overlap_period": "-", "note": "赵满柱为涿鹿籍（本地人）出身的市域晋升先例"},
]

# ── Build ──
run_build(
    slug=SLUG,
    persons=persons,
    organizations=organizations,
    positions=positions,
    relationships=relationships,
    db_path=DB_PATH,
    gexf_path=GEXF_PATH,
)

print("\n=== 涿鹿县 network build complete ===")
print(f"persons: {len(persons)}  orgs: {len(organizations)}  positions: {len(positions)}  relationships: {len(relationships)}")
print(f"DB:   {DB_PATH}")
print(f"GEXF: {GEXF_PATH}")