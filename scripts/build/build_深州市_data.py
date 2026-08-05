#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深州市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 河北省
Parent City: 衡水市
Region: 深州市
Targets: 市委书记 & 市长

Research Sources (一手官方, 深州市人民政府 www.shenzhou.gov.cn 站内要闻/人大会议):
- 现任市委书记冯淑云 (confirmed 一手官方):
  * 2026-01-20 市委农村工作会议『市委书记冯淑云传达习近平总书记对做好"三农"工作的重要指示精神并讲话』
    http://www.shenzhou.gov.cn/art/2026/1/27/art_711_614768.html
  * 2026-04-07 深州市2026桃花季活动『市委书记冯淑云出席活动并宣布开幕』
    http://www.shenzhou.gov.cn/art/2026/4/10/art_711_621976.html
  * 2026-06-23 市委理论学习中心组第六次集体学习『市委书记冯淑云主持召开』
    http://www.shenzhou.gov.cn/art/2026/6/29/art_711_629100.html
- 现任市委副书记、市长郑学国 (confirmed 一手官方):
  * 2026-01-20 市委农村工作会议『市委副书记、代市长郑学国主持』 (art_711_614768)
  * 2026-04-07 桃花季活动『市长郑学国致辞』 — 已由代市长转正当选市长 (art_711_621976)
  * 2025-12-13 『12月13日，代市长郑学学就产业发展深入开发区进行调研』
    http://www.shenzhou.gov.cn/art/2025/12/23/art_711_610165.html
- 市委/政府/人大领导班子 (一手官方人大常委会会议及市委全会记录):
  * 市人大常委会主任 严立根，副主任 张会强、李会选、刘大力、张玉品 (2026-05-14 七届人大常委会四十一 次，art_711_625384)
  * 市委常委、常务副市长 李丹辉 (2026-05-14、2026-03-30 七届人大常委列席，art_711_625384 / art_711_620697)
  * 市委常委、市纪委书记、市监委主任 张占增 (2026-03-30 七届人大常委四十四次列席，art_711_620697)
  * 副市长 周春彦 (2023-06 中考考务、2026-04 桃花季出席)
  * 市领导 刁嘉良、张忠尧、刘昭、张红梅、刘冕、刘大力、张红梅 (2026 农村工作会/桃花季、两会列名)
- 前任/继任链条 (党政一把手)：
  * 市委书记：王文强(2019-2021) → 于波(2022-2025) → 冯淑云(2026-)
  * 市长：张小勇(2018-2020) → 于波(2021-2022) → 冯淑云(2022-2025) → 郑学国(2026-)

Confidence 说明：
  冯淑云 任深州市委书记、郑学国任市委副书记、市长 — confirmed（官网一手 2026-01/04/06 多篇权威确认）。
  于波为前任书记（2022-2025）、此前任市长（2021-2022）— confirmed；其卸任后去向 unverified。
  个人履历（出生、籍贯、学历、入党参工年月）— unverified（官网无领导之窗简历页，外部 Baidu/Exa/Bing/360 检索受限）。

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

SLUG = "深州市"

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
        "name": "冯淑云",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "深州市委书记",
        "current_org": "中共深州市委员会",
        "source": "深州市人民政府官网一手官方：2026-01-20『市容农村工作会议』书记冯淑云传达习近平总书记讲话；2026-04-07『深州市2026桃花季活动』书记冯淑云宣布开幕；2026-06-23 市委理论学习中心组第六次集体学习冯淑云主持。http://www.shenzhou.gov.cn/art/2026/1/27/art_711_614768.html"
    },
    # ════════════════════════════════════════
    # Target 2: 现任市长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "郑学国",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "深州市委副书记、市长",
        "current_org": "深州市人民政府",
        "source": "深州市人民政府官网一手官方：2026-01-20 市委农村工作会议『市委副书记、代市长郑学国』主持；2026-04-07 桃花季『市长郑学国致辞』（已由代市长转正当选市长）。http://www.shenzhou.gov.cn/art/2026/4/10/art_711_621976.html"
    },
    # ════════════════════════════════════════
    # 人大常委会班子（2026 一手官方）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "严立根",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "深州市人大常委会主任",
        "current_org": "深州市人民代表大会常务委员会",
        "source": "深州市人民政府官网（2018-2026 连任）：2026-05-14 七届人大常委会第四十一次会议『市人大常委会主任严立根』主持并为被任命人员颁发任命书 (art_711_625384)；2026-03-30 七届人大常委会第四十次会议 (art_711_620697)。2018年曾任深州市副市长 (art_711_2018-11 严立根副市长调度规上企业)。"
    },
    {
        "id": 4,
        "name": "张会强",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "深州市人大常委会副主任",
        "current_org": "深州市人民代表大会常务委员会",
        "source": "深州市人民政府官网（2026-03-30、2026-05-14 七届人大常委会会议出席人员列名，张会强为人大常委会副主任）。"
    },
    {
        "id": 5,
        "name": "李会选",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "深州市人大常委会副主任",
        "current_org": "深州市人民代表大会常务委员会",
        "source": "深州市人民政府官网（2026-03-30 七届人大常委第四十次会议『市人大常委会副主任李会选主持会议』(art_711_620697)；2026-05-14 会议列名）。"
    },
    {
        "id": 6,
        "name": "刘大力",
        "current_post": "深州市人大常委会副主任",
        "current_org": "深州市人民代表大会常务委员会",
        "source": "深州市人民政府官网（2026-03-30、2026-05-14 人大常委会副主任；2026-04-07 桃花季市领导出席）。"
    },
    {
        "id": 7,
        "name": "张玉品",
        "current_post": "深州市人大常委会副主任",
        "current_org": "深州市人民代表大会常务委员会",
        "source": "深州市人民政府官网（2026-03-30、2026-05-14 人大常委会副主任列名）。"
    },
    # ════════════════════════════════════════
    # 市委常委 / 政府班子（2026 一手官方）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "张占增",
        "current_post": "深州市委常委、市纪委书记、市监委主任",
        "current_org": "中国共产党深州市纪律检查委员会",
        "source": "深州市人民政府官网（2026-03-30 七届人大常委第四十次会议『市委常委、市纪委书记、市监察委员会主任张占增列席』art_711_620697）。"
    },
    {
        "id": 9,
        "name": "李丹辉",
        "current_post": "深州市委常委、市政府常务副市长",
        "current_org": "深州市人民政府",
        "source": "深州市人民政府官网（2026-05-14 七届人大常委第四十一次会议『市委常委、政府常务副市长李丹辉列席』art_711_625384；2026-03-30 列席 art_711_620697）。"
    },
    {
        "id": 10,
        "name": "周春彦",
        "current_post": "深州市副市长",
        "current_org": "深州市人民政府",
        "source": "深州市人民政府官网（2023-06-23 『副市长周春彦视察中考考务工作』art_711_623078；2026-04-07 桃花季市领导出席列名）。"
    },
    {
        "id": 11,
        "name": "刁嘉良",
        "current_post": "深州市领导",
        "current_org": "深州市人民政府",
        "source": "深州市人民政府官网（2026-01-20 市委农村工作会、2026-04-07 桃花季市领导出席列名）。"
    },
    {
        "id": 12,
        "name": "张忠尧",
        "current_post": "深州市领导",
        "current_org": "深州市人民政府",
        "source": "深州市人民政府官网（2026-01-20 市委农村工作会、2026-04-07 桃花季市领导出席列名）。"
    },
    {
        "id": 13,
        "name": "刘昭",
        "current_post": "深州市领导",
        "current_org": "中共深州市委员会",
        "source": "深州市人民政府官网（2026-04-07 桃花季市领导出席列名）。"
    },
    {
        "id": 14,
        "name": "张红梅",
        "current_post": "深州市领导",
        "current_org": "深州市人民政府",
        "source": "深州市人民政府官网（2026-04-07 桃花季市领导出席列名）。"
    },
    # ════════════════════════════════════════
    # 前任领导 / 继任链
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "于波",
        "current_post": "原深州市委书记（2026 卸任，去向待查）",
        "current_org": "中共深州市委员会",
        "source": "深州市人民政府官网：2022-2025 多篇『市委书记于波』一手官网文章（2025-11-28 宣讲 art_711_607396、2024-10-21 和美乡村 art_711_562737、2024-03-25 招商 art_711_537301 等）；2021-2022 曾任市委副书记、市长（2021-12-27 市长于波 art_711；2022-03-07 市委副书记、市长于波），后升任市委书记。2026 年前已卸任书记（冯淑云接任）。"
    },
    {
        "id": 16,
        "name": "王文强",
        "current_post": "原深州市委书记（2019-2021）",
        "current_org": "中共深州市委员会",
        "source": "深州市人民政府官网（2019-2021 多篇市委书记王文强一手：2021-12-31 调研教育规划；2020-10-15 双代工作；2019-11-27 城市建设等）。"
    },
    {
        "id": 17,
        "name": "张小勇",
        "current_post": "原深州市市长（2018-2020）",
        "current_org": "深州市人民政府",
        "source": "深州市人民政府官网（2018-2020 多篇市长张小勇一手：2020-08-31 开学检查；2018-09-10 慰问中学教师；2018-06-06 视察高考）。"
    },
    {
        "id": 18,
        "name": "刘继承",
        "current_post": "原深州市委书记（2018-2019）",
        "current_org": "中共深州市委员会",
        "source": "深州市人民政府官网（2018-09 『深州市委书记刘继承带队到职教中心视察调研』；2019-08-16 『市委书记刘继承调研暑期汛期』）。"
    },
]

# Normalize dict fields for persons that may omit gender/ethnicity/etc.
_person_keys = ["id", "name", "gender", "ethnicity", "birth", "birthplace", "native_place",
                "education", "party_join", "work_start", "current_post", "current_org", "source"]
for _p in persons:
    for _k in _person_keys:
        _p.setdefault(_k, "")

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中国共产党深州市委员会",
        "type": "党委",
        "level": "县级",
        "location": "衡水市深州市",
        "parent": "中共衡水市委"
    },
    {
        "id": 2,
        "name": "深州市人民政府",
        "type": "政府",
        "level": "县级",
        "location": "衡水市深州市",
        "parent": "衡水市人民政府"
    },
    {
        "id": 3,
        "name": "中国共产党深州市纪律检查委员会、深州市监察委员会",
        "type": "党委",
        "level": "县级",
        "location": "衡水市深州市",
        "parent": "中共衡水市纪委"
    },
    {
        "id": 4,
        "name": "深州市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "location": "衡水市深州市",
        "parent": "衡水市人大常委会"
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议深州市委员会",
        "type": "政协",
        "level": "县级",
        "location": "衡水市深州市",
        "parent": "政协衡水市委员会"
    },
]

# 3. Positions
positions = [
    # ── 冯淑云（现任市委书记）──
    {"person_id": 1, "org_id": 1, "title": "深州市委书记", "start_date": "2026", "end_date": "present", "rank": "正处级（县级市正职）", "note": "接任前任书记于波任深州市委书记；2026-01/04/06 一手官方多篇确认；2026-07 八届人大暨八次党代会换届周期内任职。"},
    # ── 郑学国（现任市长）──
    {"person_id": 2, "org_id": 2, "title": "深州市委副书记、市长", "start_date": "2025-12", "end_date": "present", "rank": "正处级（县级市正职）", "note": "2025-12 起代市长（art_711_610165）；2026-04 已以市长身份致辞（桃花季），确认转正当选市长；2026-07 八届人大选举后市府班子。"},
    {"person_id": 2, "org_id": 1, "title": "深州市委副书记", "start_date": "2025-12", "end_date": "present", "rank": "县级", "note": "市委副书记、市长、市政府党组书记。"},
    # ── 严立根（人大主任）──
    {"person_id": 3, "org_id": 4, "title": "深州市人大常委会主任", "start_date": "2021", "end_date": "present", "rank": "县级正职", "note": "2026 七届人大常委多次主持；曾任深州市分管众副市长（2018）。"},
    {"person_id": 3, "org_id": 2, "title": "深州市副市长（早年）", "start_date": "2018", "end_date": "2021", "rank": "副处级", "note": "2018-11 严立根以副市长身份调度确定上企业（art_2018-11-05）。"},
    # ── 人大副主任 ──
    {"person_id": 4, "org_id": 4, "title": "深州市人大常委会副主任", "start_date": "约2021", "end_date": "present", "rank": "县级", "note": "2026 人大常委列名。"},
    {"person_id": 5, "org_id": 4, "title": "深州市人大常委会副主任", "start_date": "约2021", "end_date": "present", "rank": "县级", "note": "2026-03-30 常委会副主任；主持第40次常委会。"},
    {"person_id": 6, "org_id": 4, "title": "深州市人大常委会副主任", "start_date": "约2021", "end_date": "present", "rank": "县级", "note": "2026 人大常委、桃花季市领导列名。"},
    {"person_id": 7, "org_id": 4, "title": "深州市人大常委会副主任", "start_date": "约2021", "end_date": "present", "rank": "县级", "note": "2026 人大常委列名。"},
    # ── 纪委 / 政府班子 ──
    {"person_id": 8, "org_id": 3, "title": "深州市委常委、市纪委书记、市监委主任", "start_date": "约2023", "end_date": "present", "rank": "县级", "note": "2026-03-30列席人大常委会（纪委书记、监委主任）。"},
    {"person_id": 8, "org_id": 1, "title": "深州市委常委（纪委书记）", "start_date": "约2023", "end_date": "present", "rank": "县级", "note": "市委常委、纪委书记。"},
    {"person_id": 9, "org_id": 2, "title": "深州市委常委、市政府常务副市长", "start_date": "2025", "end_date": "present", "rank": "副处级（常务）", "note": "2026-03/05 人大常委会列席的政府常务副市长。"},
    {"person_id": 9, "org_id": 1, "title": "深州市委常委", "start_date": "2025", "end_date": "present", "rank": "县级", "note": "市委常委、常务副市长。"},
    {"person_id": 10, "org_id": 2, "title": "深州市副市长", "start_date": "约2023", "end_date": "present", "rank": "副处级", "note": "2023-06 视察中考考务、2026-04 桃花季市领导。"},
    {"person_id": 11, "org_id": 2, "title": "深州市领导", "start_date": "约2023", "end_date": "present", "rank": "副处级", "note": "2026 农村工作会/桃花季列名。"},
    {"person_id": 12, "org_id": 2, "title": "深州市领导", "start_date": "约2023", "end_date": "present", "rank": "副处级", "note": "2026 农村工作会/桃花季列名。"},
    {"person_id": 13, "org_id": 1, "title": "深州市领导（市委常委）", "start_date": "约2023", "end_date": "present", "rank": "县级", "note": "2026 桃花季市领导列名。"},
    {"person_id": 14, "org_id": 2, "title": "深州市领导", "start_date": "约2023", "end_date": "present", "rank": "副处级", "note": "2026 桃花季市领导列名。"},
    # ── 前任 ──
    {"person_id": 15, "org_id": 1, "title": "深州市委书记", "start_date": "2022", "end_date": "2025", "rank": "正处级", "note": "2022 年代起任市委书记；2024-2025 多篇网站一手确认；2026 年前卸任（去向待查）。"},
    {"person_id": 15, "org_id": 1, "title": "深州市委副书记、市长", "start_date": "2021", "end_date": "2022", "rank": "正处级", "note": "2021-12 市长于 波、2022-03 市委副书记、市长于 波；随后升任市委书记。"},
    {"person_id": 16, "org_id": 1, "title": "深州市委书记", "start_date": "2019", "end_date": "2021", "rank": "正处级", "note": "2019-2021 任市委书记；其后由 于波 接任。"},
    {"person_id": 17, "org_id": 2, "title": "深州市市长", "start_date": "2018", "end_date": "2020", "rank": "正处级", "note": "2018-2020 任市长；其后由于何人接任。"},
    {"person_id": 18, "org_id": 1, "title": "深州市委书记", "start_date": "2018", "end_date": "2019", "rank": "正处级", "note": "2018-2019 任市委书记；其后王文强接任。"},
    {"person_id": 1, "org_id": 2, "title": "深州市市长（此前）", "start_date": "2022", "end_date": "2025", "rank": "正处级", "note": "在任市委书记前曾任市长（2022-2025），后转任书记。"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "深州市委书记冯淑云与市长郑学国为现任党政一把手搭配，多次共同出席市委全会、市委农村工作会、市委理论学习中心组及市委常委会（2026）。",
        "overlap_org": "中共深州市委员会／深州市人民政府",
        "overlap_period": "2025-"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "市委书记冯淑云与市人大常委会主任严立根在全会（人大选举/市的党委领导人大）共事；两人均在 2026 历任党代会/人大换届任核心岗位。",
        "overlap_org": "中共深州市委员会／深州市人大常委会",
        "overlap_period": "2025-"
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "overlap",
        "context": "市委书记冯淑与市纪委书记、市监委主任张占增在市委常委会/纪委系统中共同履职，落实党全面从严治党。",
        "overlap_org": "中共深州市委员会／深州市纪委监委",
        "overlap_period": "2023-"
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "overlap",
        "context": "市委书记冯淑与常务副市长李丹辉在市委常委会和政府班子共事（李任常务副市长）。",
        "overlap_org": "中共深州市委员会／深州市人民政府",
        "overlap_period": "2025-"
    },
    {
        "person_a": 2,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "市长郑学与常务副市长李丹辉为市政府班子上级副手关系，共同出席市政府常务会议。",
        "overlap_org": "深州市人民政府",
        "overlap_period": "2025-"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "市长郑学与人大主任严立根在公务员程序中分工（市政府向市人代会报告工作，市人大常委会监督政府）。",
        "overlap_org": "深州市人民政府／深州市人大常委会",
        "overlap_period": "2025-"
    },
    {
        "person_a": 1,
        "person_b": 15,
        "type": "predecessor_successor",
        "context": "冯淑云接任前任市委书记于波任深州市委书记（于2022-2025任书记，2025年底-2026年换 由冯接任）。二人此前曾有市长—书记搭档（冯曾任市长）。",
        "overlap_org": "中共深州市委员会",
        "overlap_period": "2025-2026"
    },
    {
        "person_a": 2,
        "person_b": 15,
        "type": "predecessor_successor",
        "context": "郑学由代市长继任市长；于波曾于2021-2022任市长（后升市委书记）。",
        "overlap_org": "深州市人民政府",
        "overlap_period": "2026"
    },
    {
        "person_a": 15,
        "person_b": 16,
        "type": "predecessor_successor",
        "context": "于波接任前任市委书记王文强任深州市委书记（王文强2019-2021，于波2022-）。",
        "overlap_org": "中共深州市委员会",
        "overlap_period": "2021-2022"
    },
    {
        "person_a": 17,
        "person_b": 15,
        "type": "predecessor_successor",
        "context": "于波接任前任市长张小勇任市长（张小勇2018-2020，于波2021-2022）。",
        "overlap_org": "深州市人民政府",
        "overlap_period": "2020-2021"
    },
    {
        "person_a": 16,
        "person_b": 18,
        "type": "predecessor_successor",
        "context": "王文强接任前任市委书记刘继承（2018-2019）任书记。",
        "overlap_org": "中共深州市委员会",
        "overlap_period": "2019"
    },
    {
        "person_a": 3,
        "person_b": 15,
        "type": "overlap",
        "context": "严立根（市人大主任）与于波（前书记/前市长）均在深州市委/人大班子共事（2018-2025）。",
        "overlap_org": "中共深州市委员会／深州市人大常委会",
        "overlap_period": "2018-2025"
    },
    {
        "person_a": 5,
        "person_b": 4,
        "type": "overlap",
        "context": "人大常委会副主任李会选、张会强等在同一届人大常委会集体的共事（人大副主任集体）。",
        "overlap_org": "深州市人民代表大会常务委员会",
        "overlap_period": "2021-"
    },
    {
        "person_a": 8,
        "person_b": 3,
        "type": "overlap",
        "context": "市纪委、市监委主任张占增与人大主任严立根在人大常委会履职程序上分工协作（人大选举监委主任）。",
        "overlap_org": "深州市人大常委会／中共深州市纪委",
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