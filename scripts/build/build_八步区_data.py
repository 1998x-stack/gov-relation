#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database and GEXF graph for 贺州市八步区 leadership network.

Level: 市辖区
Province: 广西壮族自治区
Parent City: 贺州市
Region: 八步区
Targets: 区委书记 & 区长

Research Date: 2026-08-06 (task guangxi_八步区)
Evidence quality: guided by the china-gov-network skill; web access degraded
(Exa rate-limited, Baidu/Bing/so.com/360/搜狗 captcha-gated, r.jina.ai down,
babu.gov.cn DNS blocked). Core facts confirmed from the official 八步区人民政府
portal www.gxbabu.gov.cn (primary source).

CONFIRMED (primary/official, as of 2026-08):
  - 区委书记 马鹏翔: 区人武部党委第一书记任职大会 2026-06-12;
    区委常委会主持 2026-07-24 / 07-30; 中国共产党贺州市八步区第六次代表大会作区委工作报告 2026-08-01。
  - 马鹏翔 此前为 区长/区政府党组书记 (2026-03-19 政府工作报告; 2026-06-24 仍"区委书记、区长"
    主持第86次常务会)。进入 第六次党代会(2026-08-01开幕) 换届过渡期。
  - 六次党代会大会执行主席/主席台前排: 马鹏翔、高宾(主持大会)、陈宏乾、李季桦、张楠、
    梁键、陈晓、乐学斌、陈家坛、张洪波、陈振攀。
  - 区委常委、区人武部上校政委 张洪波; 副区长、市公安局八步分局局长 龙绍聪。
  - 区人大常委会主任 莫华钧 (2026-03 五届人大六次会议主持); 人大领导 龙立忠、吴慧、
    黄晓波、李海珍。
  - 前任区委书记/党委领导 雷少华 (2025 活跃; 去向待查)。

UNVERIFIED / open gaps (见 report/open_gaps.md 与各 person JSON open_questions):
  - 第六次党代会后新任正式区长的最终确认; 高宾具体职务分工与完整履历。
  - 马鹏翔/高宾 的出生、籍贯、学历、入党/参工时间以及任区委书记前的完整履历。
  - 前任书记雷少华 的下一步去向。

regional: 面积 3666.65 km2 (~31.2% of 贺州), 户籍人口 77.95万 (~78万 各族), 辖 12 镇 1 瑶族乡
3 街道办事处, 185 个建制村, 23 个社区居委会。前身 贺县/贺州市(县级)。
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

# 向上查找仓库根目录（兼容暂存目录 data/tmp/<task>/ 与规范化 scripts/build/ 两种位置）
BASE = Path(__file__).resolve()
for _ in range(6):
    if (BASE / "gov_relation").is_dir() and (BASE / "gov_relation" / "runner.py").is_file():
        break
    BASE = BASE.parent
sys.path.insert(0, str(BASE))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "八步区"

# 入库（暂存/规范化）用 STAGING_DIR 环境变量覆盖输出目录；否则写规范化目录
_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(_STAGING, f"{SLUG}_network.gexf")
else:
    DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
    GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共贺州市八步区委员会", "type": "党委", "level": "县处级",
     "parent": "中共贺州市委", "location": "广西壮族自治区贺州市八步区"},
    {"id": 2, "name": "贺州市八步区人民政府", "type": "政府", "level": "县处级",
     "parent": "贺州市人民政府", "location": "广西壮族自治区贺州市八步区"},
    {"id": 3, "name": "贺州市八步区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "贺州市人大常委会", "location": "广西壮族自治区贺州市八步区"},
    {"id": 4, "name": "中国人民政治协商会议贺州市八步区委员会", "type": "政协", "level": "县处级",
     "parent": "政协贺州市委员会", "location": "广西壮族自治区贺州市八步区"},
    {"id": 5, "name": "贺州市八步区纪律检查委员会/八步区监察委员会", "type": "纪委", "level": "县处级",
     "parent": "中共贺州市纪委", "location": "广西壮族自治区贺州市八步区"},
    {"id": 6, "name": "贺州市八步区人民武装部", "type": "政府", "level": "县处级",
     "parent": "贺州军分区", "location": "广西壮族自治区贺州市八步区"},
    {"id": 7, "name": "贺州市公安局八步分局", "type": "政府", "level": "县处级",
     "parent": "贺州市公安局", "location": "广西壮族自治区贺州市八步区"},
    # 跨县区节点
    {"id": 8, "name": "中共钟山县委员会", "type": "党委", "level": "县处级",
     "parent": "中共贺州市委", "location": "广西壮族自治区贺州市钟山县"},
    {"id": 9, "name": "中共昭平县委员会", "type": "党委", "level": "县处级",
     "parent": "中共贺州市委", "location": "广西壮族自治区贺州市昭平县"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 马鹏翔 — 区委书记（原区长，换届过渡期亦任区长）
    {"id": 1, "name": "马鹏翔", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "八步区委书记（第六次党代会换届过渡期兼任区长）",
     "current_org": "中共贺州市八步区委员会",
     "source": "http://www.gxbabu.gov.cn/zwgknrgl_44979/ldhd/t27806125.shtml"},
    # 2 — 高宾 — 区委副书记/区长候选人（六次党代会大会主持）
    {"id": 2, "name": "高宾", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "八步区（第六次党代会大会执行主席/主持人，区委副书记领衔班子）",
        "current_org": "中共贺州市八步区委员会",
        "source": "http://www.gxbabu.gov.cn/zwgknrgl_44979/szyw/t27973533.shtml"},
    # 3 — 张洪波 — 区委常委、人武部政委
    {"id": 3, "name": "张洪波", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "八步区委常委、区人民武装部上校政治委员",
        "current_org": "贺州市八步区人民武装部",
        "source": "http://www.gxbabu.gov.cn/zwgknrgl_44979/ldhd/t27806125.shtml"},
    # 4 — 龙绍聪 — 副区长、区公安局局长
    {"id": 4, "name": "龙绍聪", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "八步区副区长、市公安局八步分局局长",
        "current_org": "贺州市公安局八步分局",
        "source": "http://www.gxbabu.gov.cn/zwgknrgl_44979/szyw/t27973533.shtml"},
    # 5 — 莫华钧 — 区人大常委会主任
    {"id": 5, "name": "莫华钧", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "八步区人大常委会主任（党组书记）",
        "current_org": "贺州市八步区人民代表大会常务委员会",
        "source": "http://www.gxbabu.gov.cn/zwgknrgl_44979/szyw/t27375847.shtml"},
    # 6 — 雷少华 — 前任区委书记
    {"id": 6, "name": "雷少华", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "（曾任八步区委书记，2025 活跃）",
        "current_org": "中共八步区委员会",
        "source": "http://www.gxbabu.gov.cn/szyw 时政要闻 2025 年活动记录"},
    # 7 — 陈信东 — 前八步区 20 年干部，现钟山县长（跨县区）
    {"id": 7, "name": "陈信东", "gender": "男", "ethnicity": "汉族", "birth": "1978年1月",
        "birthplace": "广西贺州", "education": "桂林理工大学在职研究生（工程硕士），桂林工学院高分子材料与工程本科",
        "party_join": "2005年4月加入中国共产党", "work_start": "2002年11月参加工作",
        "current_post": "钟山县委副书记、县长",
        "current_org": "钟山县人民政府",
        "source": "scripts/build/build_钟山县_data.py (本地库)"},
    # 8 — 陈宏乾 — 六次党代会执行主席（区委领导）
    {"id": 8, "name": "陈宏乾", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "八步区区委领导（第六次党代会执行主席）",
        "current_org": "中共八步区委员会",
        "source": "http://www.gxbabu.gov.cn/zwgknrgl_44979/szyw/t27973533.shtml"},
    # 9 — 龙立忠/李院珍 等区人大领导（六次人大主席团）
    {"id": 9, "name": "龙立忠", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "八步区人大常委会领导",
        "current_org": "贺州市八步区人民代表大会常务委员会",
        "source": "http://www.gxbabu.gov.cn/zwgknrgl_44979/szyw/t27375847.shtml"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 马鹏翔 — 区委书记（+过渡期区长）
    {"person_id": 1, "org_id": 1, "title": "八步区委书记", "start_date": "2026-06", "end_date": "present",
     "rank": "正处级", "note": "兼任区人民武装部党委第一书记（2026-06-12任职大会）"},
    {"person_id": 1, "org_id": 2, "title": "八步区长、区政府党组书记", "start_date": "", "end_date": "2026-06过渡",
     "rank": "正处级", "note": "2026-03-19 政府工作报告; 2026-06-24 第86次常务会仍以区长主持"},
    # 高宾 — 区委副书记（候选人）/六届党代会主持
    {"person_id": 2, "org_id": 1, "title": "八步区委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "第六次党代会大会主持（2026-08-01）"},
    # 张洪波 — 区委常委/人武部
    {"person_id": 3, "org_id": 1, "title": "八步区委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "区人民武装部上校政治委员", "start_date": "", "end_date": "present",
     "rank": "", "note": ""},
    # 龙聪 — 副区长/公安局长
    {"person_id": 4, "org_id": 2, "title": "八步区副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 7, "title": "市公安局八步分局局长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "市管干部"},
    # 莫华钧 — 人大主任
    {"person_id": 5, "org_id": 3, "title": "八步区人大常委会主任", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "2026-03 五届人大六次会议大会执行主席"},
    # 雷少华 — 前任书记
    {"person_id": 6, "org_id": 1, "title": "八步区委书记", "start_date": "", "end_date": "2026",
     "rank": "正处级", "note": "前任区委书记；去向待核"},
    # 陈信东 — 钟山县长（八步成长）
    {"person_id": 7, "org_id": 8, "title": "钟山县委副书记、县长", "start_date": "2024-07", "end_date": "present",
     "rank": "正处级", "note": "此前在八步区工作约 20 年"},
    {"person_id": 7, "org_id": 1, "title": "八步区委常委、区委办公室主任", "start_date": "2020-10", "end_date": "2021-07",
     "rank": "副处级", "note": "本地库来源（build_钟山县_data.py）"},
    # 陈宏乾 — 区委领导
    {"person_id": 8, "org_id": 1, "title": "八步区委领导（常委）", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "第六次党代会执行主席"},
    # 龙立忠 — 区人大领导
    {"person_id": 9, "org_id": 3, "title": "八步区人大常委会副主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "2026-03 人大主席团"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 党政正职
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区委副书记（六代会大会主持）党政班子", "overlap_org": "中共八步区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 6, "type": "predecessor_successor",
     "context": "马鹏翔接任雷少华担任区委书记（推测，去向待核）", "overlap_org": "中共八步区委员会", "overlap_period": "2026"},
    # 区委班子
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委书记与区委常委、人武部政委", "overlap_org": "中共八步区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "区委书记与陈宏乾（六次党代会执行主席）", "overlap_org": "中共八步区委员会", "overlap_period": "2026"},
    # 区长与公安
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区长与副区长、公安局长 共事", "overlap_org": "八步区人民政府", "overlap_period": "2025-2026"},
    # 人大
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与区人大主任，两会交叉", "overlap_org": "八步区", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "区委副书记（两会）与区人大主任", "overlap_org": "八步区", "overlap_period": "2026"},
    # 跨县区调动
    {"person_a": 7, "person_b": 1, "type": "overlap",
     "context": "陈信东与马鹏翔同出八步区（陈信东八步区 20 年干部，后调钟山任县长）",
     "overlap_org": "八步区", "overlap_period": "2015-2021"},
    {"person_a": 7, "person_b": 2, "type": "overlap",
     "context": "钟山县长与八步区委，贺州市域跨县区干部交流", "overlap_org": "贺州市", "overlap_period": "2024"},
]

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
    print(f"\nDone: {SLUG} staging build complete.")