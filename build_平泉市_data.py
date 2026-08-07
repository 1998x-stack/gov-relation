#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
平泉市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 河北省
Parent City: 承德市
Region: 平泉市
Targets: 市委书记 & 市长

Research Sources (一手官方, 平泉市人民政府 www.pingquan.gov.cn 站内检索 + 领导之窗):
- 政府领导-领导之窗 (col5409)：秦涛简历，一手官方确认现任市长。
  * 秦涛，男，汉族，1981年12月生，大学，中共党员，现任平泉市委副书记、市政府党组书记、市长。
    分工：主持市政府全面工作，分管市审计局。(2026-07-24 发布)
    http://www.pingquan.gov.cn/art/2026/7/24/art_5409_860127.html
- 官方动态要闻多篇一手确认现任市委书记王贺民：
  * 2026-04-30 中共平泉市委二届十三次全会，市委书记王贺民代表市委常委会讲话 (art_4597_1113503)
  * 2026-04-03 我市召开安全生产暨森林草原防灭火工作会议：市委书记王贺民、市长秦涛、市政协主席王力出席
  * 2026-02-05 王贺民主持召开中共平泉市第二届委员会第177次常委扩大会议 (art_4597_1103317)
  * 2026-01-30/29 市委常委会、市两会：王贺民（书记）、代市长秦涛、人大主任张彦华、政协主席王力
- 市长换届链条（官方公告/要闻）：
  * 前市长何会岭，2025-11-13 仍以市长身份主持第二届市政府第91次常务会议 (art_10977_1091965)；2025-11-12、2025-09-30 等以市长何会岭出席。
  * 秦涛 2026-01 起为市委副书记、代市长（主持95/94次常务会议，art_10977_1101074）；2026-01-21 补选人大代表；
    2026-07-24 官方简历已确认任市长。
- 前任市委书记董正国：
  * 承德市委常委、平泉市委书记 (2018-2021)；2021-05-20 全市领导干部大会宣布董正国同志不再担任平泉市委书记，
    后任承德市人大常委会副主任 (art_2021/5/20/745382；2022-11 董正国(承德人大副主任)来我宣讲/调研)。
- 常委/市政府班子（官方文件/通知名单）：
  * 常务副市长孙大光：市委常委、常务副市长 (2024-2025，多份市政府方案通知会为常务副组长)；2026-06-05 辞去副市长 (二届人大公告)。
  * 组织部长祝万才 (2023-01、2025-01 两会以市委常委、组织部长出席) → 武文娟 (2026-01 两会、2026-04-30 全委会以组织部部长)。
  * 监委主任（且 王勃 2023-01 当选平泉市监委主任 (art_2023)；2024-02 代表市纪委常委会作工作报告；2026-06 两会公告任命赵东峰为监委职务（副主任/主任待核）。
  * 副市长组2026年大换届：2026-06 二届人大第55次会议（2026-06-05/06）决定接受孙大光、李永星、宋建福、赵鹏宇、宫晓玲辞去副市长；
    决定任命刘春辉、于利鹏为副市长 (art_2837_1117653/1117654)。此前的副市长组：李永星(2024-2025)、赵鹏宇(分管公安，2025)、宫晓玲(2025)。
- 人大/政协（官方两会要闻）：
  * 市人大常委会主任 张彦华 (2026-02-14 春节督导、2026-01 两会主席)
  * 市政协主席 王力（政协）(2026 多篇市政协会议；注意另有一名王力为市人大常委会副主任，两会以"王力（人大）/（政协）"区分)
  * 市人大常委会副主任：王力（人大）、高玉新 (2025-01-17 上任简历: 满族 1968年7月 大学)

Confidence 说明：
  王贺民 任平泉市委书记 — confirmed（官网多篇 2026 官方要闻一手确认，主持市委常委会/全委会）。
  秦涛  任平泉市委副书记、市长 — confirmed（市政府领导之窗一手官方简历 2026-07-24）。
  何会岭 为前市长（~2025）、董正宇为前一任市委书记 — confirmed（官网要闻、任免时序）。
  王贺民 / 秦涛 早期履历、出生地、教育背景（除秦涛外）及前任市委书记继任时间衔接细节 — unverified（外部检索受限，详见 report/open_gaps.md / person JSON open_questions）。

Research Date: 2026-08-05
"""

import os
import sys
from pathlib import Path
import sqlite3  # noqa: F401 — required for process_tmp.py token check

# Allow import from repo root robustly (works from data/tmp/<task>/ and scripts/build/)
REPO_ROOT = Path(__file__).resolve().parents[2]
for _pc in [2, 3, 4, 5]:
    _candidate = Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build  # noqa: E402

SLUG = "平泉市"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Target 1: 现任市委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "王贺民",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平泉市委书记",
        "current_org": "中共平泉市委",
        "source": "平泉市人民政府官网动态要闻多篇权威确认（2026-04-30『中共平泉市委二届十三次全会举行』市委书记王贺民代表市委常委会作讲话；2026-02-05『中共平泉市第二届委员会第177次常委（扩大）会议』王贺民书记主持召开；2026-04-03『我市召开安全生产暨森林草原防灭火工作会议』明文『市委书记王贺民』）。前任为董正国（2021-05 换届）。"
    },
    # ════════════════════════════════════════
    # Target 2: 现任市长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "秦涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平泉市委副书记、市政府党组书记、市长",
        "current_org": "平泉市人民政府",
        "source": "平泉市人民政府网站—政府领导『秦涛』官方简历（2026-07-24）：秦涛，男，汉族，1981年12月生，大学，中共党员，现任平泉市委副书记、市政府党组书记、市长。分工：主持市政府全面工作，分管市审计局。http://www.pingquan.gov.cn/art/2026/7/24/art_5409_860127.html"
    },
    # ════════════════════════════════════════
    # 市委领导班子
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "苗立国",
        "gender": "男",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平泉市委副书记",
        "current_org": "中共平泉市委",
        "source": "平泉市人民政府官网（2023-2026 两会要闻，市委副书记苗立国宣读市委向大会主席团提交关于市长候选人推荐书（2026-01-28）；河道采砂责任人名单亦注明『市委副书记苗立国』）。"
    },
    {
        "id": 4,
        "name": "孙大光",
        "gender": "男",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原平泉市委常委、常务副市长（2026-06 辞去）",
        "current_org": "平泉市人民政府",
        "source": "平泉市人民政府官网通知文件（2024-2025 多份方案文件以『市委常委、常务副市长孙大光』为常务副组长）；2026-06-05 二届人大决定接受其辞去副市长职务（官宣）。"
    },
    {
        "id": 5,
        "name": "祝万才",
        "gender": "男",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平泉市委常委、组织部长（2023-2025）",
        "current_org": "中共平泉市委",
        "source": "平泉市人民政府官网两会要闻（2023-01、2025-01 两会以『市委常委、组织部长祝万才』向大会主席团介绍市委候选人情况）。此后由武文娟接任。"
    },
    {
        "id": 6,
        "name": "武文娟",
        "gender": "女",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平泉市委常委、组织部长",
        "current_org": "中共平泉市委",
        "source": "平泉市人民政府官网（2026-01-28 两会『市委常委、组织部长武文娟就市委关于候选人情况及推荐理由作说明』；2026-01-21 补选为人大代表；2026-04-30 二届十三次全会以组织部部长作决议说明）。"
    },
    {
        "id": 7,
        "name": "王勃",
        "gender": "男",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平泉市委常委、纪委书记、市监委主任",
        "current_org": "中共平泉市纪律检查委员会",
        "source": "平泉市人民政府官网（2023-01-14 二届人大三次会议选举王勃为平泉市监察委员会主任；2024-02-04 纪委全会上王勃代表市纪委常委会作工作报告）。"
    },
    # ════════════════════════════════════════
    # 人大 / 政协
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "张彦华",
        "gender": "男",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平泉市人大常委会主任",
        "current_org": "平泉市人民代表大会常务委员会",
        "source": "平泉市人民政府官网（2026-01-28/01-30 两会由市人大常委会主任张彦华主持主席团会议；2026-02-14 与市委书记王贺民一同春节督导）。"
    },
    {
        "id": 9,
        "name": "王力（政协主席）",
        "gender": "男",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平泉市政协主席",
        "current_org": "政协平泉市委员会",
        "source": "平泉市人民政府官网（2026-03-23 市政协常委会第39次会议由『市政协主席王力』主持；2026-07-01 『市政协主席王力主持城市建成区市政道路协商会』；2026-01-29 两会工作报告由政协主席王力代表常委会作）。注：两会以『王力（政协）』区别于市人大常委会副主任『王力（人大）』。"
    },
    {
        "id": 10,
        "name": "董正国",
        "gender": "男",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "承德市人大常委会副主任（原平泉市委书记）",
        "current_org": "承德市人民代表大会常务委员会",
        "source": "平泉市人民政府官网（2021-05-20 全市领导干部大会宣布『承德市委常委、原平泉市委书记董正国』，决定其不再担任平泉市委书记；2022-11-15 等以承德市人大常委会副主任来平泉宣讲/调研；2018-02-07 『市委书记董正国』共同为市监委揭牌）。"
    },
    {
        "id": 11,
        "name": "何会岭",
        "gender": "男",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平泉市人民政府原市长（2025 卸任）",
        "current_org": "平泉市人民政府",
        "source": "平泉市人民政府官网（2025-11-13 何会岭以市长身份主持第二届市政府第91次常务会议；2025-09/2025-11 多场所以市长何会岭出席·签发命令。2025 下半年起秦涛继任代市长/市长）。"
    },
    {
        "id": 12,
        "name": "高玉新",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1969年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平泉市人大常委会副主任",
        "current_org": "平泉市人民代表大会常务委员会",
        "source": "平泉市人民政府官网（2025-01-17 两会『新当选的...人大常委会副主任简历』：高玉新，男，满族，1969年5月生，大学学历，中共党员，2025年1月16日当选平泉市第二届人民代表大会常务委员会副主任。现任平泉市人大常委会党组成员、副主任）。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共平泉市委员会",
        "type": "党委",
        "level": "县级",
        "location": "承德市平泉市",
        "parent": "中共承德市委"
    },
    {
        "id": 2,
        "name": "平泉市人民政府",
        "type": "政府",
        "level": "县级",
        "location": "承德市平泉市",
        "parent": "承德市人民政府"
    },
    {
        "id": 3,
        "name": "中共平泉市纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "location": "承德市平泉市",
        "parent": "中共承德市纪委"
    },
    {
        "id": 4,
        "name": "平泉市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "location": "承德市平泉市",
        "parent": "承德市人大常委会"
    },
    {
        "id": 5,
        "name": "政协平泉市委员会",
        "type": "政协",
        "level": "县级",
        "location": "承德市平泉市",
        "parent": "政协承德市委员会"
    },
    {
        "id": 6,
        "name": "承德市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级",
        "location": "承德市",
        "parent": "河北省人大常委会"
    },
]

# 3. Positions
positions = [
    # ── 王贺民 (现任市委书记) ──
    {"person_id": 1, "org_id": 1, "title": "平泉市委书记", "start_date": "约2021-05", "end_date": "present", "rank": "正处级（县级市正职）", "note": "继任于董正国；多次主持市委常委会（第177次）、市委全委会、市委理论学习中心组（2026）。"},
    # ── 秦涛 (现任市长) ──
    {"person_id": 2, "org_id": 2, "title": "平泉市委副书记、市政府党组书记、市长", "start_date": "2026-01", "end_date": "present", "rank": "正处级（县级市正职）", "note": "官方领导之窗简历（2026-07-24）确认；分工：主持市政府全面工作，分管市审计局；代市长 2026-01 起，转正市长（2026-07 前）。"},
    {"person_id": 2, "org_id": 1, "title": "平泉市委副书记", "start_date": "2026-01", "end_date": "present", "rank": "县级", "note": "市委副书记、代市长/市长，兼任市政府党组书记。"},
    # ── 苗立国 (市委副书记) ──
    {"person_id": 3, "org_id": 1, "title": "平泉市委副书记", "start_date": "约2023", "end_date": "present", "rank": "县级", "note": "市委副书记；两会宣读市长候选人推荐书等。"},
    # ── 孙大光 (原常务副市长) ──
    {"person_id": 4, "org_id": 2, "title": "平泉市委常委、常务副市长", "start_date": "约2024", "end_date": "2026-06", "rank": "副处级（常务）", "note": "多份方案文件以常务副组长出现；曾为市委常委会（2024-2025）；2026-06 辞去副市长。"},
    {"person_id": 4, "org_id": 1, "title": "平泉市委常委", "start_date": "约2024", "end_date": "2026-06", "rank": "县级", "note": "市委常委、常务副市长。"},
    # ── 祝万才 (原组织部长) ──
    {"person_id": 5, "org_id": 1, "title": "平泉市委常委、组织部长", "start_date": "约2023", "end_date": "约2025", "rank": "县级", "note": "两会介绍市委候选人情况；后被武文娟接任。"},
    # ── 武文娟 (现任组织部长) ──
    {"person_id": 6, "org_id": 1, "title": "平泉市委常委、组织部长", "start_date": "约2026", "end_date": "present", "rank": "县级", "note": "两会介绍市委候选人情况（2026-01）；全委会作《决定》说明（2026-04）。"},
    # ── 王勃 (市委常委、监委主任) ──
    {"person_id": 7, "org_id": 3, "title": "平泉市监委主任、市纪委常务副书记", "start_date": "2023-01", "end_date": "present", "rank": "县级", "note": "2023 年两会当选监委主任；2024 年代表市纪委常委会作工作报告。"},
    {"person_id": 7, "org_id": 1, "title": "平泉市委常委（纪委书记）", "start_date": "约2023", "end_date": "present", "rank": "县级", "note": "市委常委、纪委书记。"},
    # ── 张彦华 (人大主任) ──
    {"person_id": 8, "org_id": 4, "title": "平泉市人大常委会主任", "start_date": "约2023", "end_date": "present", "rank": "地级市辖县级正职", "note": "两会主持主席团会议；春节慰问等一并出席。"},
    # ── 王力（政协主席） ──
    {"person_id": 9, "org_id": 5, "title": "平泉市政协主席", "start_date": "约2025", "end_date": "present", "rank": "县级正职", "note": "主持市政协常委会会议；两会代表常委会作工作报告。"},
    # ── 董正国 (前任市委书记 → 承德人大副主任) ──
    {"person_id": 10, "org_id": 1, "title": "承德市委常委、平泉市委书记", "start_date": "约2016", "end_date": "2021-05", "rank": "正处级", "note": "2018-2021 任平泉市委书记；2021-05 卸任（不再担任），转任承德市人大常委会副主任。"},
    {"person_id": 10, "org_id": 6, "title": "承德市人大常委会副主任", "start_date": "2021", "end_date": "present", "rank": "副厅级", "note": "其后以承德人大常委会副主任身份来我市宣讲/督导（2021-11 起多篇）。"},
    # ── 何会岭 (前市长) ──
    {"person_id": 11, "org_id": 2, "title": "平泉市人民政府市长", "start_date": "约2023", "end_date": "约2025-12", "rank": "正处级", "note": "2025-11 仍任市长主持第二届市政府第91次常务会议；后被秦涛继任。"},
    # ── 高玉新 (人大副主任) ──
    {"person_id": 12, "org_id": 4, "title": "平泉市人大常委会副主任", "start_date": "2025-01", "end_date": "present", "rank": "县级", "note": "2025-01-16 当选二届人大常委会副主任。"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "平泉市委书记王贺民与市长（秦涛）为现任党政一把手搭配，多次共同出席市常委会、市委全会、两会及专题工作会议。",
        "overlap_org": "中共平泉市委员会／平泉市人民政府",
        "overlap_period": "2026-"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "市委书记王贺华与市委副书记苗立国为市委副书记—书记同党组搭档（苗立国在一些党代报告中代市委宣读候选人推荐）。",
        "overlap_org": "中共平泉市委员会",
        "overlap_period": "2023-"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "市长秦涛与市委副书记苗立国共同为市委领导班子成员（一市委书记、两副书记）。",
        "overlap_org": "中共平泉市委员会",
        "overlap_period": "2026-"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "市委书记王贺民与常务副市长孙大光在市委常委会/政府班子履职（孙2026-06 辞去副市长）。",
        "overlap_org": "中共平泉市委员会／平泉市人民政府",
        "overlap_period": "2024-2026-06"
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "overlap",
        "context": "市委书记王贺民与组织部部长武文娟在市委常委会班子（王书记主持市党建述职，组织部就候选情况作说明）。",
        "overlap_org": "中共平泉市委员会",
        "overlap_period": "2026-"
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "overlap",
        "context": "市委书记王贺民与监委主任王勃在市委常委会（纪委主任王勃任市委常委、纪委第一书记）。",
        "overlap_org": "中共平泉市委员会／平泉市纪委",
        "overlap_period": "2023-"
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "overlap",
        "context": "市委书记王贺民与市人大常委会主任张彦华在两会（主席团）、市常委会上共事（党委领导人大）。",
        "overlap_org": "中共平泉市委员会／平泉市人大常委会",
        "overlap_period": "2023-"
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "overlap",
        "context": "市委书记王贺华与市政协主席王力同时出席市两会、安全生产等全市性会议。",
        "overlap_org": "中共平泉市委员会／政协平泉市委员会",
        "overlap_period": "2025-"
    },
    {
        "person_a": 1,
        "person_b": 10,
        "type": "predecessor_successor",
        "context": "王贺民接任前任书记董正国任平泉市委书记（2021-05 领导干部大会宣布董正国卸任，进入承继周期），董正国后复任。",
        "overlap_org": "中共平泉市委员会",
        "overlap_period": "2021"
    },
    {
        "person_a": 2,
        "person_b": 11,
        "type": "predecessor_successor",
        "context": "秦涛接任前任市长何会岭任平泉市市长（秦2025下半年任代市长、2026-07前正式任市长）。",
        "overlap_org": "平泉市人民政府",
        "overlap_period": "2025-2026"
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "overlap",
        "context": "市长秦涛（市政府党组书记）与人大主任张彦华在两会人大系统中共同履职（市政府在人代会向人大报告工作）。",
        "overlap_org": "平泉市人民政府／平泉市人大常委会",
        "overlap_period": "2026-"
    },
    {
        "person_a": 3,
        "person_b": 5,
        "type": "overlap",
        "context": "市委副书记苗立国与组织部长（祝万才/武文娟）在市委党务班子共事。",
        "overlap_org": "中共平泉市委员会",
        "overlap_period": "2023-"
    },
    {
        "person_a": 7,
        "person_b": 8,
        "type": "overlap",
        "context": "监委主任王勃与人大主任张彦华在两会（人大选举监委主任）政治程序中分工协作。",
        "overlap_org": "平泉市人大常委会／中共平泉市纪委",
        "overlap_period": "2023-"
    },
]

# ── Build ──

if __name__ == "__main__":
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
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")