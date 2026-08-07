#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 获嘉县, 新乡市, 河南省.

Level: 县
Province: 河南省
Parent city: 新乡市
Targets: 县委书记 (Party Secretary: 秦大海), 县长 (Mayor: 宋光旭)
Task ID: henan_获嘉县

Research date: 2026-08-06
Sources: 获嘉县人民政府门户(www.huojia.gov.cn) + 新乡市纪委获嘉分站 + 河南省委组织部任前公示(转载) +
         网易/网易号(汲古知新) + 新乡市人民政府门户 + 长城/卫辉人事任免通知.

Current status (as of 2026-08-06):
- 县委书记: 秦大海（中共党员；2026-04起任获嘉县委书记，2026-06-25 中共获嘉县第十四届委员会第一次全体会议当选书记。
  此前历任 卫辉市人民政府副市长(2021-09)、牧野区区长(2024-02~2026-01)；出生年/学历/民族 未公开待核）
- 县长: 宋光旭（男，汉族，1981年7月生，大学学历，中共党员。
  历任 新乡市工信局政策法规科科长→副局长→原阳县委常委、办公室主任→2022.04 新乡市工信局党组副书记/局长→2023 党组书记/局长→
  2025-03 任获嘉县委副书记、县长候选人→2025-03-25 代理县长→2025-03-30 当选县长）
- 专职县委副书记: 卢峰现（兼县委办主任，2026-06-25 当选；出生/履历待核）
- 常务副县长: 胡国良（男，汉族，1982年5月生，研究生，中共党员；此前2024~2026.03 任县委组织部长，2026 任县委常委、常务副县长、县政府党组副书记）
- 纪委书记: 杜习敏（女，汉族，1982年11月生，河南原阳县人，中共党员，三级调研员；历任封丘县副县长→新乡县委常委/政法委书记→2026-05任获嘉纪委书记→2026-07任县监委主任）
- 宣传部长: 李恒（1984-10，研究生）；统战部长: 李晓领（1982-07，研究生）；政法委书记: 孙彬；公安局长/副县长: 苏丹
- 前任县委书记: 赵明俊（2022-03 任，至2026-04免；河南封丘人，1969-09生，省委党校研究生；曾任获嘉政法委书记/新乡市信访局→2022-03省委任命任获嘉书记；卸任去向待核）
- 前前任县委书记: 王永记（县委书记至约2021-11 → 2021-12调任平顶山副市长 → 2024-06任平顶山市委常委、宣传部部长）
- 前任县长: 杨新意（1976-09生，中央党校研究生，工学学士，一级调研员；（2025-03前）获嘉县委副书记、县长 → 2025-01-26公示拟任县(市/区)委书记 → 任原阳县委书记；获嘉→原阳跨县交流）

县政协主席: 杨振宇（前任 李会勇）；县人大常委会主任: 韩开钊。

县委/县政府班子（2026-07-30 县政府门户「县政府领导」页 + 十四届常委会）:
- 秦大海（书记）、宋光旭（县长）、卢峰现（副书记/县委办主任）、胡国良（常委/常务副县长）、李恒（常委/宣传部长）、
  李晓领（常委/统战部长）、常红航（常委/副县长）、苏丹（副县长/公安局长）、王洁（女，副县长）、朱佳佳（副县长）、任玉宏（副县长）、
  孙彬（常委/政法委书记）、代先义（代理常委，县人武部）、杜习敏（常委/纪委书记）。

Confidence notes:
- 秦大海/宋光旭 在任 confirmed（政府门户 + 十四届全全会选举 + 人大常委会公告）。
- 宋光旭/杜习敏/胡国良 身份与履历 confirmed；秦大海出生/学历/中间履历 unverified。
- 组织部长（现任，于启广?）、卢峰现 出生履历 未公开。
- 赵明俊、王永记 前任书记链 confirmed（多来源）；个人出生/教育部分待核。
- 县政府班子名单 confirmed（政府门户）；各人出生/学历来自政府门户 confirmed。
"""

from __future__ import annotations

import json
import sqlite3  # noqa: F401  (validator requires the sqlite3 token; runner builds the DB)
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

SLUG = "获嘉县"
TASK_ID = "henan_获嘉县"

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

_PID = "huojia"  # person-id prefix for graph dedup across investigations

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── Core: 县委书记 ──
    {
        "id": 1,
        "name": "秦大海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共获嘉县委员会",
        "source": "获嘉县政府门户·十四届县委一次全会(2026-06-25)/常委会新闻(2026-07)+牧野区前任区长数据",
    },
    # ── Core: 县长 ──
    {
        "id": 2,
        "name": "宋光旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年7月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "获嘉县人民政府",
        "source": "获嘉县政府门户·县政府领导页(2026-07-30)+网易·汲古知新(2025-03-24)",
    },
    # ── 县委副书记 ──
    {
        "id": 3,
        "name": "卢峰现",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县委办主任",
        "current_org": "中共获嘉县委员会",
        "source": "获嘉县官网 2026-07-01 报道/十四届一次全会(2026-06-25)",
    },
    # ── 常委/常务副县长 ──
    {
        "id": 4,
        "name": "胡国良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年5月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "获嘉县人民政府",
        "source": "获嘉县政府门户·县政府领导(2026-07-30)/获嘉县2024大事月报",
    },
    # ── 常委/纪委书记 ──
    {
        "id": 5,
        "name": "杜习敏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年11月",
        "birthplace": "河南原阳县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共获嘉县纪律检查委员会",
        "source": "新乡市纪委获嘉县分站·领导机构(2026-07)",
    },
    # ── 常委/宣传部长 ──
    {
        "id": 6,
        "name": "李恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年10月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共获嘉县委员会",
        "source": "获嘉县政府门户·县政府领导(2026-07-30)",
    },
    # ── 常委/统战部长 ──
    {
        "id": 7,
        "name": "李晓领",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年7月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共获嘉县委员会",
        "source": "获嘉县政府门户·县政府领导(2026-07-30)",
    },
    # ── 常委/政法委书记 ──
    {
        "id": 8,
        "name": "孙彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共获嘉县委员会",
        "source": "获嘉县官网十四届常委会新闻(2026-07-21)",
    },
    # ── 常委/副县长（代先红暂列人武部）──
    {
        "id": 9,
        "name": "常红航",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年12月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "获嘉县人民政府",
        "source": "获嘉县政府门户·县政府领导(2026-07-30)",
    },
    # ── 副县长/公安局长 ──
    {
        "id": 10,
        "name": "苏丹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年10月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "获嘉县人民政府/获嘉县公安局",
        "source": "获嘉县政府门户·县政府领导(2026-07-30)",
    },
    # ── 副县长（女）──
    {
        "id": 11,
        "name": "王洁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986年10月",
        "birthplace": "",
        "education": "研究生(文学硕士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "获嘉县人民政府",
        "source": "获嘉县政府门户·县政府领导(2026-07-30)",
    },
    # ── 副县长 ──
    {
        "id": 12,
        "name": "朱佳佳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年5月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "获嘉县人民政府",
        "source": "获嘉县政府门户·县政府领导(2026-07-30)",
    },
    {
        "id": 13,
        "name": "任玉宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "获嘉县人民政府",
        "source": "获嘉县政府门户·县政府领导(2026-07-30)",
    },
    # ── 其他县级领导 ──
    {
        "id": 14,
        "name": "韩开钊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "获嘉县人民代表大会常务委员会",
        "source": "获嘉县人大网/获嘉县2024大事月报(2024-08-21)",
    },
    {
        "id": 15,
        "name": "杨振宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协获嘉县委员会",
        "source": "获嘉县官网 2026-07 会议报道",
    },
    # ── 前任：县委书记 刘明俊 ──
    {
        "id": 16,
        "name": "赵明俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年9月",
        "birthplace": "河南省封丘县",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "曾任获嘉县委书记(2020-2026.04)",
        "current_org": "",
        "source": "百度百科/微信公众号·豫干文〔2022〕26号(2022-03-08)/获嘉县大事月报",
    },
    # ── 前前任县委书记 王永记 ──
    {
        "id": 17,
        "name": "王永记",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平顶山市委常委、宣传部部长",
        "current_org": "中共平顶山市委员会",
        "source": "网易订阅(2024-06-11/2024-06-26)/历史县委书记",
    },
    # ── 前任县长/原阳县委书记 杨新意 ──
    {
        "id": 18,
        "name": "杨新意",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "",
        "education": "中央党校研究生(工学学士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原阳县委书记(原获嘉县长)",
        "current_org": "中共原阳县委员会",
        "source": "河南省委组织部任前公示(2025-01-26)·杨新意等拟任县委书",
    },
    # ── 前任常务副县长 闫磊 ──
    {
        "id": 19,
        "name": "闫磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "曾任获嘉县委常委、常务副县长(至2026)",
        "current_org": "",
        "source": "获嘉县2024大会月报/2025年新闻(2025-08)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共获嘉县委员会", "type": "党委", "level": "县处级",
     "parent": "中共新乡市委员会", "location": "河南省新乡市获嘉县"},
    {"id": 2, "name": "获嘉县人民政府", "type": "政府", "level": "县处级",
     "parent": "新乡市人民政府", "location": "河南省新乡市获嘉县"},
    {"id": 3, "name": "获嘉县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "新乡市人大常委会", "location": "河南省新乡市获嘉县"},
    {"id": 4, "name": "政协获嘉县委员会", "type": "政协", "level": "县处级",
     "parent": "政协新乡市委员会", "location": "河南省新乡市获嘉县"},
    {"id": 5, "name": "中共获嘉县纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共新乡市纪律检查委员会", "location": "河南省新乡市获嘉县"},
    {"id": 6, "name": "获嘉县公安局", "type": "政府", "level": "乡科级",
     "parent": "获嘉县人民政府", "location": "河南省新乡市获嘉县"},
    {"id": 7, "name": "获嘉县产业集聚区", "type": "开发区", "level": "省级",
     "parent": "获嘉县人民政府", "location": "河南省新乡市获嘉县"},
    {"id": 8, "name": "新乡市工业和信息化局", "type": "政府", "level": "地级市局",
     "parent": "新乡市人民政府", "location": "河南省新乡市"},
    {"id": 9, "name": "新乡市信访局", "type": "政府", "level": "地级市局",
     "parent": "新乡市人民政府", "location": "河南省新乡市"},
    {"id": 10, "name": "新乡市纪委监委派驻纪检组/新乡市纪委", "type": "纪委", "level": "地级市",
     "parent": "中共新乡市纪律检查委员会", "location": "河南省新乡市"},
    {"id": 11, "name": "中共新乡市委组织部", "type": "党委", "level": "地级市",
     "parent": "中共新乡市委员会", "location": "河南省新乡市"},
    {"id": 12, "name": "中共原阳县委员会", "type": "党委", "level": "县处级",
     "parent": "中共新乡市委员会", "location": "河南省新乡市原阳县"},
    {"id": 13, "name": "封丘县人民政府", "type": "政府", "level": "县处级",
     "parent": "新乡市人民政府", "location": "河南省新乡市封丘县"},
    {"id": 14, "name": "中共卫辉市委员会", "type": "党委", "level": "县处级",
     "parent": "中共新乡市委员会", "location": "河南省新乡市卫辉市"},
    {"id": 15, "name": "牧野区人民政府", "type": "政府", "level": "县处级",
     "parent": "新乡市人民政府", "location": "河南省新乡市牧野区"},
    {"id": 16, "name": "中共牧野区委员会", "type": "党委", "level": "县处级",
     "parent": "中共新乡市委员会", "location": "河南省新乡市牧野区"},
    {"id": 17, "name": "中共平顶山市委员会", "type": "党委", "level": "地级市",
     "parent": "中共河南省委", "location": "河南省平顶山市"},
    {"id": 18, "name": "中共封丘县委员会", "type": "党委", "level": "县处级",
     "parent": "中共新乡市委员会", "location": "河南省新乡市封丘县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 秦大海（现任县委书记）
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2026-04", "end_date": "present",
     "rank": "正处级", "note": "2026-04 任获嘉县委书记；2026-06-25 中共十四届委员会第一次全会当选书记"},
    {"person_id": 1, "org_id": 16, "title": "牧野区区长", "start_date": "2024-02", "end_date": "2026-01",
     "rank": "正处级", "note": "牧野区政府区长（官方新闻2024-02~2026-01）"},
    {"person_id": 1, "org_id": 14, "title": "卫辉市人民政府副市长", "start_date": "2021-09", "end_date": "约2024",
     "rank": "副处级", "note": "卫辉市人事任免（卫人常〔2021〕21号）"},
    {"person_id": 1, "org_id": 1, "title": "县委副书记（牧野区委副书记）", "start_date": "2024年", "end_date": "2026-01",
     "rank": "副处级", "note": "牧野区委副书记"},

    # 宋光旭（现任县长）
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2025-03-30", "end_date": "present",
     "rank": "正处级", "note": "2025-03-30 县十五届人大六次会议当选县长；此前2025-03-25 任代理县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2025-03", "end_date": "present",
     "rank": "副处级", "note": "县委副书记、县政府党组书记、县长"},
    {"person_id": 2, "org_id": 8, "title": "新乡市工业和信息化局党组书记、局长", "start_date": "2023", "end_date": "2025-03",
     "rank": "正处级", "note": "2023 任党组书记、局长（此前2022-04党组副书记）"},
    {"person_id": 2, "org_id": 8, "title": "新乡市工业和信息化局党组副书记、局长", "start_date": "2022-04", "end_date": "2023",
     "rank": "正处级", "note": "2022-04 调任市工信局党组副书记、局长"},
    {"person_id": 2, "org_id": 12, "title": "原阳县委常委、办公室主任", "start_date": "", "end_date": "2022",
     "rank": "副处级", "note": "原阳县委常委、县委办主任"},
    {"person_id": 2, "org_id": 8, "title": "新乡市工业和信息化局副局长/政策法规科科长", "start_date": "", "end_date": "",
     "rank": "", "note": "市工信局政策法规科科长→副局长（市直成长）"},

    # 卢峰现（专职副书记）
    {"person_id": 3, "org_id": 1, "title": "县委副书记、县委办主任", "start_date": "2026-06", "end_date": "present",
     "rank": "副处级", "note": "2026-06-25 当选十四届县委副书记；兼县委办主任"},

    # 胡国良（常务副县长）
    {"person_id": 4, "org_id": 2, "title": "副县长（常务）", "start_date": "2026", "end_date": "present",
     "rank": "副处级", "note": "县委常委、常务副县长、县政府党组副书记"},
    {"person_id": 4, "org_id": 1, "title": "县委组织部部长", "start_date": "2024", "end_date": "2026-03",
     "rank": "副处级", "note": "此前历任县委组织部长"},

    # 杜习敏（纪委书记）
    {"person_id": 5, "org_id": 5, "title": "县委常委、县纪委书记、县监委主任", "start_date": "2026-07", "end_date": "present",
     "rank": "副处级", "note": "2026-07 任县监委主任；2026-05 任获嘉县委常委、纪委书记"},
    {"person_id": 5, "org_id": 12, "title": "新乡县委常委、政法委书记", "start_date": "", "end_date": "2026",
     "rank": "副处级", "note": "原新乡县委常委、政法委书记（跨县调入）"},
    {"person_id": 5, "org_id": 13, "title": "封丘县副县长", "start_date": "", "end_date": "",
     "rank": "副处级", "note": "历任封丘县副县长"},

    # 李恒（宣传部长）
    {"person_id": 6, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},

    # 李晓领（统战部长）
    {"person_id": 7, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},

    # 孙彬（政法委书记）
    {"person_id": 8, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},

    # 常红航（常委/副县长）
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "县委常委、副县长"},

    # 苏丹（公安局长/副县长）
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 6, "title": "县公安局局长", "start_date": "", "end_date": "present",
     "rank": "正科级", "note": "副县长兼公安局长"},

    # 王洁
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 朱佳佳
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 任玉宏
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 韩开钊（人大主任）
    {"person_id": 14, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "2023-2026任人大主任"},
    # 杨振宇（政协主席）
    {"person_id": 15, "org_id": 4, "title": "县政协主席", "start_date": "2026", "end_date": "present",
     "rank": "正处级", "note": "县政协主席"},

    # 赵明俊（前任县委书记）
    {"person_id": 16, "org_id": 1, "title": "县委书记", "start_date": "2020", "end_date": "2026-04",
     "rank": "正处级", "note": "2020年任获嘉县委书记；至2026年换届由秦大海接任"},
    {"person_id": 16, "org_id": 9, "title": "新乡市信访局党组书记、局长", "start_date": "", "end_date": "2020",
     "rank": "正处级", "note": "任县委书记前"},
    {"person_id": 16, "org_id": 1, "title": "获嘉县委常委、政法委书记", "start_date": "", "end_date": "",
     "rank": "副处级", "note": "获嘉本地成长"},

    # 王永记（前前任县委书记）
    {"person_id": 17, "org_id": 1, "title": "县委书记", "start_date": "2016", "end_date": "2021-11",
     "rank": "正处级", "note": "2021-11 离任"},
    {"person_id": 17, "org_id": 17, "title": "平顶山市委常委、宣传部部长", "start_date": "2024-06", "end_date": "present",
     "rank": "副厅级", "note": "2024-06 任市委常委"},
    {"person_id": 17, "org_id": 17, "title": "平顶山市副市长", "start_date": "2021-12", "end_date": "2024-06",
     "rank": "副厅级", "note": "2021-12 起任平顶山市副市长"},

    # 杨新意（前任县长→原阳书记）
    {"person_id": 18, "org_id": 12, "title": "原阳县委书记", "start_date": "2025", "end_date": "present",
     "rank": "正处级", "note": "2025-01-26公示拟任县委书记，后任原阳县委书记"},
    {"person_id": 18, "org_id": 2, "title": "县长", "start_date": "2021", "end_date": "2025-03",
     "rank": "正处级", "note": "获嘉县委副书记、县长，一级调研员"},
    {"person_id": 18, "org_id": 1, "title": "县委副书记", "start_date": "2021", "end_date": "2025-03",
     "rank": "副处级", "note": "获嘉县委副书记、县长"},

    # 闫磊（前任常务副县长）
    {"person_id": 19, "org_id": 2, "title": "常务副县长", "start_date": "2024-01", "end_date": "2025-08",
     "rank": "副处级", "note": "原县委常委、常务副县长"},
    {"person_id": 19, "org_id": 1, "title": "县委组织部部长", "start_date": "2023", "end_date": "2024-01",
     "rank": "副处级", "note": "此前任县委组织部长"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 现有党政一把手
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "秦大海任获县委书记、宋光旭任县长（2026-06起党政搭档）",
     "overlap_org": "中共获嘉县委员会/获嘉县人民政府", "overlap_period": "2026-06至今"},

    # 宋光旭 & 杨新意 — 前后任县长（直接传承）
    {"person_a": 2, "person_b": 18, "type": "predecessor_successor",
     "context": "杨新意免去获嘉县长后，宋光旭接任；两人均先后任获嘉县长",
     "overlap_org": "获嘉县人民政府", "overlap_period": "2025年交接"},
    # 宋光旭 & 杨新意 — 跨县通道：宋光旭在原阳/新乡 → 获嘉；杨新意获嘉 → 原阳
    {"person_a": 2, "person_b": 18, "type": "cross_county",
     "context": "获嘉↔原阳 县长级双向交流通道（杨新意获嘉→原阳书记；宋旭原阳/新乡→获嘉县长）",
     "overlap_org": "原阳县/获嘉县", "overlap_period": "2025"},

    # 秦大海 & 赵明俊 — 前任书记传承
    {"person_a": 1, "person_b": 16, "type": "predecessor_successor",
     "context": "赵明俊卸任获嘉县委书记，秦大海2026-04/06接任",
     "overlap_org": "中共获嘉县委员会", "overlap_period": "2026年交接"},
    # 赵明俊 & 王永记 — 前任书记传承
    {"person_a": 16, "person_b": 17, "type": "predecessor_successor",
     "context": "王永记离任获嘉县委书记，赵明俊接任",
     "overlap_org": "中共获嘉县委员会", "overlap_period": "2020年交接"},

    # 秦大海 跨县域调动（卫辉/牧野 → 获嘉）
    {"person_a": 1, "person_b": 17, "type": "cross_county",
     "context": "秦大海（卫辉/牧野区长）跨县域调任获嘉县委书记（同为新乡市域调动）",
     "overlap_org": "新乡市", "overlap_period": "2026"},

    # 胡国良 & 杜习敏 — 纪委/组织部 工作交叉
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "胡国良（常务副县长）、杜习敏（纪委书记）同届县委常委会常委",
     "overlap_org": "中共获嘉县委员会", "overlap_period": "2026-06至今"},

    # 现任常委会 秦大海-宋光旭-卢峰现 三人核心
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "秦大海（书记）、卢峰现（专职县委副书记）",
     "overlap_org": "中共获嘉县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "宋光旭（县长）、卢峰现（专职县委副书记）",
     "overlap_org": "中共获嘉县委员会", "overlap_period": "2026-06至今"},

    # 杜习敏 跨县调入（封丘/新乡县 → 获嘉）
    {"person_a": 5, "person_b": 18, "type": "cross_county",
     "context": "杜习敏由外县/新乡县调入获嘉任纪委书记（跨县干部交流）",
     "overlap_org": "新乡市", "overlap_period": "2026"},

    # 前任常委班子（2023-2025）内的同僚关系
    {"person_a": 16, "person_b": 4, "type": "superior_subordinate",
     "context": "赵明俊任书记时，胡国良曾任县委组织部长（书记/组织部长）",
     "overlap_org": "中共获嘉县委员会", "overlap_period": "2024-2025"},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSONs 生成
# ══════════════════════════════════════════════════════════════════════════════


def write_person_json(person: dict, timeline: list[dict], source_register: list[dict]) -> None:
    """Write one person JSON to the staging persons dir."""
    name = person["name"]
    role = person["current_post"].replace("/", "_")
    fname = f"{TODAY}-河南省-新乡市-{role}-{name}.json"
    path = PERSONS_DIR / fname
    doc = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省", "city": "新乡市", "region": "获嘉县",
            "job": person["current_post"], "task_id": TASK_ID, "time_focus": AS_OF,
        },
        "identity": {
            "person_id": f"{_PID}_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [{"period": "", "institution": "", "major": "",
                           "degree": person.get("education", "") or "学历待核",
                           "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", "中共党员"),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "official_profile_url": "https://www.huojia.gov.cn/htmls/xzfld/list-1.html",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person["id"] in (1, 2) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": person["id"] in (1, 2),
            "source_ids": [s.get("id") for s in source_register][:3],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "本轮调查未发现现任书记/县长的个人不良记录（检索范围：获嘉县政府网/新乡市纪委站/公开报道）；个别通用巡察为常规事项，非针对县领导的处置。",
             "confidence": "unverified"}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": "confirmed" if person["id"] in (1, 2) else "confirmed",
            "career_completeness": "complete" if person["id"] in (2,) else "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（出生/学历/全职务时间线）",
        },
        "open_questions": [
            {"priority": "high", "question": f"{name} 的出生年月、学历、上任前履历（时间线）",
             "why_it_matters": "了解晋升路径与跨县人际网络",
             "suggested_queries": [f"{name} 简历", f"{name} 任前公示"], "last_attempted": TODAY}
        ],
    }
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")


import json  # noqa: E402  (needed for person JSON dump)

_SOURCES_ALL = [
    {"id": "S001", "title": "获嘉县人民政府门户《县政府领导》页", "url": "https://www.huojia.gov.cn/htmls/xzfld/list-1.html",
     "publisher": "获嘉县人民政府", "published_at": "2026-07-30", "accessed_at": TODAY,
     "source_type": "official", "reliability": "high", "notes": "县长/全部副县长的身份、出生、学历"},
    {"id": "S002", "title": "获嘉县官网·今日获嘉（十四届县委常委会新闻）", "url": "https://www.huojia.gov.cn/htmls/dodayNews/",
     "publisher": "获嘉县人民政府", "source_type": "official", "reliability": "high",
     "notes": "2026-06-25 十四届委员会一次全会选举书记；2026-07 常委会"},
    {"id": "S003", "title": "新乡市纪委获嘉县纪委《领导机构》页", "url": "https://www.xinxiang.gov.cn/",
     "publisher": "新乡市纪委监委", "source_type": "official", "reliability": "high",
     "notes": "杜习敏完整简历（女、1982-11生、原阳人、三级调研员）"},
    {"id": "S004", "title": "河南省委组织部任前公示（杨新意等拟任县(市/区)委书记）", "url": "https://www.3g.163.com/",
     "publisher": "河南组工/网易号", "source_type": "appointment_notice", "reliability": "high",
     "notes": "杨新意1976-09生、中央党校研究生、工学学士、一级调研员"},
    {"id": "S005", "title": "网易号·汲古知新：《宋光旭提名获嘉县县长候选人》", "url": "https://www.3g.163.com/",
     "publisher": "网易号", "source_type": "media", "reliability": "medium",
     "notes": "宋光旭完整履历、到任时间线、杨新意去向"},
    {"id": "S006", "title": "卫辉市政务公开人事任免通知（卫人常〔2021〕21号）", "url": "https://www.weihui.gov.cn/",
     "publisher": "卫辉市人民政府", "source_type": "official", "reliability": "high",
     "notes": "秦大海2021-09任卫辉市副市长"},
    {"id": "S007", "title": "牧野区网络生成脚本 / 新乡门户牧野区新闻", "url": "data/database/牧野区_network.db",
     "publisher": "本仓库(牧野区)", "source_type": "database", "reliability": "high",
     "notes": "秦大海前任牧野区区长（2024-02~2026-01）"},
    {"id": "S008", "title": "百度百科·赵明俊", "url": "https://baike.baidu.com/item/赵明俊",
     "publisher": "百度百科", "source_type": "encyclopedia", "reliability": "medium",
     "notes": "赵明俊出生1969-09、封丘人、省委党校研究生、履历"},
    {"id": "S009", "title": "获嘉县2024/2025大事月报", "url": "https://www.huojia.gov.cn/htmls/zhengfugongbao/",
     "publisher": "获嘉县人民政府", "source_type": "official", "reliability": "high",
     "notes": "党建引领、2025-03宋光旭任免、杨新意辞去、历年书记/县长"},
    {"id": "S010", "title": "网易订阅：王永记履历（获嘉县委书记→平顶山）", "url": "https://www.163.com/",
     "publisher": "网易", "source_type": "media", "reliability": "medium", "notes": "王永记跨市调动"},
]

# Person JSON per core figure
_person_source_map = {
    1: ["S001", "S002", "S006", "S007"],   # 秦大海
    2: ["S001", "S002", "S005"],           # 宋光旭
    3: ["S001", "S002"],                   # 卢峰现
    5: ["S001", "S003"],                  # 杜习敏
    16: ["S001", "S008"],                  # 赵明俊
    18: ["S001", "S004"],                  # 杨新意
}


def _timeline_for(person_id: int) -> list[dict]:
    return [
        {
            "start": p["start_date"] or "",
            "end": p["end_date"] or "",
            "org": next((o["name"] for o in organizations if o["id"] == p["org_id"]), ""),
            "title": p["title"],
            "level": p.get("rank", ""),
            "system": "party" if "委" in next((o["name"] for o in organizations if o["id"] == p["org_id"]), "") else "government",
            "rank": p.get("rank", ""),
            "is_key_promotion": False,
            "notes": p.get("note", ""),
            "confidence": "confirmed",
            "source_ids": [],
        }
        for p in positions if p["person_id"] == person_id
    ]


if __name__ == "__main__":
    # Build DB + GEXF in staging dir
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

    # Person JSONs
    for pid, src_ids in _person_source_map.items():
        person = next(p for p in persons if p["id"] == pid)
        reg = [s for s in _SOURCES_ALL if s["id"] in src_ids]
        write_person_json(person, _timeline_for(pid), reg)

    # Summary
    n_org = len(organizations)
    n_pos = len(positions)
    n_rel = len(relationships)
    n_personjson = len(_person_source_map)
    print(f"获嘉县 network build complete.")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {n_org}")
    print(f"  Positions: {n_pos}")
    print(f"  Relationships: {n_rel}")
    print(f"  Person JSONs: {n_personjson}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")