#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database and GEXF graph for 陕西省宝鸡市太白县 leadership network.

Level: 县
Province: 陕西省
Parent City: 宝鸡市
Region: 太白县
Targets: 县委书记 (刘俊霞) & 县长 (索军虎)

Research Date: 2026-08-07 (task shaanxi_太白县)
Evidence quality: guided by the china-gov-network skill; web search degraded
(Exa rate-limited, Baidu/Bing/Sogou/jina blocked/captcha). Core roster and
profiles CONFIRMED from the official 太白县人民政府门户 https://www.taibai.gov.cn/
(primary source, direct fetch OK over HTTP).

CONFIRMED (primary/official, as of 2026-08):
  - 县委书记 刘俊霞: 2026-01-12 中共太白县委十四届十七次全会报道"县委书记刘俊霞代表县委常委会作工作报告并讲话"
    (县委办公室, URL col6606/col6620/202601/t20260113_1239913.html)。
  - 县委副书记、县长 索军虎: 2026-06-23 主持县政府第10次常务会议; 2026-07-13 主持第11次常务会议
    (col6607/col6621/col6628/...)。1981-02, 男, 汉族, 本科, 中共党员; 曾任副县长、县公安局局长。
  - 前任县长 张俊峰: 2026-04-26 主持第8次常务会议"县长张俊峰"; 2026-04-30 调研旅游保障(县长身份)。
  - 县人大常委会主任 秦斌、县政协主席 张宏斌、县委副书记 白海明 (2026-01-13县委全会报道)。
  - 县委常委、常务副县长 王小龙(1978-06); 副县长 苏康安(1973-08)/侯伟强(1984-02)/王娇(女)/
    侯嵘朝/赵铁笛(女,1987-10)/肖卫(1971-06, 公安)/李少华(1982-02, 挂职江苏徐州贾汪区)。
  - 上层连接: 宝鸡市委书记 陈晓勇(2026-07-16 在太白调研); 宝鸡市长 牛恺(2026-06-03 在太白检查)。

UNVERIFIED / open gaps (见 report/open_gaps.md 与各 person JSON open_questions):
  - 刘俊霞/索军虎 任县委书记/县长前的完整履历与身世(出生籍贯/学历/入党参工)。
  - 前任县委书记(刘俊霞之前)及其去向。
  - 张俊峰卸任县长后的去向。
  - 完整县委常委会(纪委书记、组织部长、宣传部长、统战部长、政法委书记)未在政府网站公开。
  - 太白县与宝鸡其他县区、相邻县(凤县、眉县、两当县)的干部交流证据。
"""
from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

BASE = Path(__file__).resolve()
for _ in range(6):
    if (BASE / "gov_relation").is_dir() and (BASE / "gov_relation" / "runner.py").is_file():
        break
    BASE = BASE.parent
sys.path.insert(0, str(BASE))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "太白县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(_STAGING, f"{SLUG}_network.gexf")
else:
    DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
    GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共太白县委员会", "type": "党委", "level": "县处级",
     "parent": "中共宝鸡市委", "location": "陕西省宝鸡市太白县"},
    {"id": 2, "name": "太白县人民政府", "type": "政府", "level": "县处级",
     "parent": "宝鸡市人民政府", "location": "陕西省宝鸡市太白县"},
    {"id": 3, "name": "太白县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "宝鸡市人大常委会", "location": "陕西省宝鸡市太白县"},
    {"id": 4, "name": "中国人民政治协商会议太白县委员会", "type": "政协", "level": "县处级",
     "parent": "政协宝鸡市委员会", "location": "陕西省宝鸡市太白县"},
    {"id": 5, "name": "太白县公安局", "type": "政府", "level": "乡科级",
     "parent": "宝鸡市公安局", "location": "陕西省宝鸡市太白县"},
    {"id": 6, "name": "太白县人民检察院", "type": "检察院", "level": "县处级",
     "parent": "宝鸡市人民检察院", "location": "陕西省宝鸡市太白县"},
    {"id": 7, "name": "太白县人民法院", "type": "法院", "level": "县处级",
     "parent": "宝鸡市中级人民法院", "location": "陕西省宝鸡市太白县"},
    # 上级与跨县节点
    {"id": 10, "name": "中共宝鸡市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共陕西省委", "location": "陕西省宝鸡市"},
    {"id": 11, "name": "宝鸡市人民政府", "type": "政府", "level": "地厅级",
     "parent": "陕西省人民政府", "location": "陕西省宝鸡市"},
    {"id": 13, "name": "徐州市贾汪区人民政府", "type": "政府", "level": "地厅级",
     "parent": "徐州市人民政府", "location": "江苏省徐州市贾汪区"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 刘俊霞 — 县委书记
    {"id": 1, "name": "刘俊霞", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "太白县委书记",
     "current_org": "中共太白县委员会",
     "source": "http://www.taibai.gov.cn/col6606/col6620/202601/t20260113_1239913.html"},
    # 2 索军虎 — 县长
    {"id": 2, "name": "索军虎", "gender": "男", "ethnicity": "汉族", "birth": "1981年2月",
     "birthplace": "", "education": "大学本科", "party_join": "中共党员", "work_start": "",
     "current_post": "太白县委副书记、县长",
     "current_org": "太白县人民政府",
     "source": "http://www.taibai.gov.cn/col6607/col6621/col6628/202607/t20260715_1285083.html"},
    # 3 张俊峰 — 前任县长
    {"id": 3, "name": "张俊峰", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（前任太白县长，至约2026年6月）",
     "current_org": "太白县人民政府",
     "source": "http://www.taibai.gov.cn/col6607/col6621/col6628/202604/t20260428_1266649.html"},
    # 4 白海明 — 县委副书记
    {"id": 4, "name": "白海明", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "太白县委副书记",
     "current_org": "中共太白县委员会",
     "source": "http://www.taibai.gov.cn/col6606/col6620/202601/t20260113_1239913.html"},
    # 5 秦斌 — 人大主任
    {"id": 5, "name": "秦斌", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "太白县人大常委会主任",
     "current_org": "太白县人民代表大会常务委员会",
     "source": "http://www.taibai.gov.cn/col6606/col6620/202601/t20260113_1239913.html"},
    # 6 张宏斌 — 政协主席
    {"id": 6, "name": "张宏斌", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "太白县政协主席",
     "current_org": "中国人民政治协商会议太白县委员会",
     "source": "http://www.taibai.gov.cn/col6606/col6620/202601/t20260113_1239913.html"},
    # 7 王小龙 — 常务副县长
    {"id": 7, "name": "王小龙", "gender": "男", "ethnicity": "汉族", "birth": "1978年6月",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "太白县委常委、常务副县长",
     "current_org": "太白县人民政府",
     "source": "http://www.taibai.gov.cn/col6607/col6621/col6629/202509/t20250924_1213436.html"},
    # 8-14 副县长
    {"id": 8, "name": "苏康安", "gender": "男", "ethnicity": "汉族", "birth": "1973年8月",
     "birthplace": "", "education": "本科", "party_join": "中共党员", "work_start": "",
     "current_post": "太白县副县长", "current_org": "太白县人民政府",
     "source": "http://www.taibai.gov.cn/col6607/col6621/col6643/202509/t20250924_1213438.html"},
    {"id": 9, "name": "侯伟强", "gender": "男", "ethnicity": "汉族", "birth": "1984年2月",
     "birthplace": "", "education": "大学，法学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "太白县副县长（文旅、住建）", "current_org": "太白县人民政府",
     "source": "http://www.taibai.gov.cn/col6607/col6621/col6643/202509/t20250924_1213439.html"},
    {"id": 10, "name": "王娇", "gender": "女", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "太白县副县长（教育体育、卫健、交通）", "current_org": "太白县人民政府",
     "source": "http://www.taibai.gov.cn/col6607/col6621/col6643/202509/t20250924_1213441.html"},
    {"id": 11, "name": "侯嵘朝", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "太白县副县长（农业农村、自然资源）", "current_org": "太白县人民政府",
     "source": "http://www.taibai.gov.cn/col6607/col6621/col6643/202509/t20250924_1213442.html"},
    {"id": 12, "name": "赵铁笛", "gender": "女", "ethnicity": "汉族", "birth": "1987年10月",
     "birthplace": "", "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "太白县副县长（供销）", "current_org": "太白县人民政府",
     "source": "http://www.taibai.gov.cn/col6607/col6621/col6643/202509/t20250924_1213443.html"},
    {"id": 13, "name": "肖卫", "gender": "男", "ethnicity": "汉族", "birth": "1971年6月",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "太白县副县长、县公安局局长", "current_org": "太白县公安局",
     "source": "http://www.taibai.gov.cn/col6607/col6621/col6643/202509/t20250924_1213440.html"},
    {"id": 14, "name": "李少华", "gender": "男", "ethnicity": "汉族", "birth": "1983年2月",
     "birthplace": "", "education": "大学本科", "party_join": "中共党员", "work_start": "",
     "current_post": "太白县副县长（赴江苏省徐州市贾汪区挂职）", "current_org": "徐州市贾汪区人民政府",
     "source": "http://www.taibai.gov.cn/col6607/col6621/col6643/202509/t20250924_1213437.html"},
    # 15 陈晓勇 — 宝鸡市委书记
    {"id": 15, "name": "陈晓勇", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宝鸡市委书记", "current_org": "中共宝鸡市委员会",
     "source": "http://www.taibai.gov.cn/col6606/col6620/202607/t20260717_1285943.html"},
    # 16 牛恺 — 宝鸡市长
    {"id": 16, "name": "牛恺", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宝鸡市市长", "current_org": "宝鸡市人民政府",
     "source": "http://www.taibai.gov.cn/col6606/col6620/202606/t20260605_1275446.html"},
    # 17 前任县委书记（待查）
    {"id": 17, "name": "（前任县委书记）", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "（曾任太白县委书记，身份及去向待查）", "current_org": "中共太白县委员会",
     "source": "http://www.taibai.gov.cn/col6606/col6620/202601/t20260113_1239913.html"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "太白县委书记", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "2026-01-12 县委十四届十七次全会上代表县委常委会作报告"},
    {"person_id": 2, "org_id": 2, "title": "太白县人民政府县长", "start_date": "2026-06", "end_date": "present",
     "rank": "正处级", "note": "2026-06-23 主持第10次常务会议"},
    {"person_id": 2, "org_id": 2, "title": "太白县副县长、县公安局局长", "start_date": "", "end_date": "2026-06前",
     "rank": "副处级", "note": "任县长前经历；2025-09 bio页面"},
    {"person_id": 2, "org_id": 1, "title": "太白县委副书记", "start_date": "", "end_date": "present",
     "rank": "", "note": "任县长期间兼任县委副书记"},
    {"person_id": 3, "org_id": 2, "title": "太白县人民政府县长", "start_date": "", "end_date": "2026-06",
     "rank": "正处级", "note": "前任县长；2026-04-26 主持第8次常务会议，约2026-06卸任"},
    {"person_id": 4, "org_id": 1, "title": "太白县委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "2026-01-13 县委全会"},
    {"person_id": 5, "org_id": 3, "title": "太白县人大常委会主任", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "2026-01-13 县委全会"},
    {"person_id": 6, "org_id": 4, "title": "太白县政协主席", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "2026-01-13 县委全会"},
    {"person_id": 7, "org_id": 2, "title": "太白县常务副县长（县委常委）", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "负责县政府日常工作"},
    {"person_id": 8, "org_id": 2, "title": "太白县副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "慈善事业，协助常务"},
    {"person_id": 9, "org_id": 2, "title": "太白县副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "文旅、市场监管、住建"},
    {"person_id": 10, "org_id": 2, "title": "太白县副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "教育体育、卫健、交通"},
    {"person_id": 11, "org_id": 2, "title": "太白县副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "农业农村、自然资源"},
    {"person_id": 12, "org_id": 2, "title": "太白县副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "供销、社会定点帮扶"},
    {"person_id": 13, "org_id": 2, "title": "太白县副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 5, "title": "太白县公安局局长、党委书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "太白县副县长（挂职）", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "到江苏省徐州市贾汪区挂职"},
    {"person_id": 15, "org_id": 10, "title": "宝鸡市委书记", "start_date": "", "end_date": "present",
     "rank": "副厅级", "note": "2026-07 在太白调研"},
    {"person_id": 16, "org_id": 11, "title": "宝鸡市市长", "start_date": "", "end_date": "present",
     "rank": "副厅级", "note": "2026-06 在太白检查"},
    {"person_id": 17, "org_id": 1, "title": "太白县委书记（前任）", "start_date": "", "end_date": "2025前",
     "rank": "正处级", "note": "身份待查"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记刘俊霞与县长索军虎党政正职搭档", "overlap_org": "中共太白县委员会", "overlap_period": "2026-06至今"},
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor",
     "context": "张俊峰曾任太白县长, 其后索军虎接任县长(约2026-06)", "overlap_org": "太白县人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与县委副书记领导关系", "overlap_org": "中共太白县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "县委书记与县人大常委会主任（四套班子）", "overlap_org": "太白县", "overlap_period": "current"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "县委书记与县政协主席（四套班子）", "overlap_org": "太白县", "overlap_period": "current"},
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "县长与常务副县长（县政府班子）", "overlap_org": "太白县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 8, "type": "overlap",
     "context": "县长与副县长", "overlap_org": "太白县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 13, "type": "overlap",
     "context": "县长与副县长兼公安局长", "overlap_org": "太白县人民政府", "overlap_period": "current"},
    {"person_a": 15, "person_b": 1, "type": "superior_subordinate",
     "context": "宝鸡市委书记与太白县委书记（上下级）", "overlap_org": "中共宝鸡市委员会", "overlap_period": "current"},
    {"person_a": 16, "person_b": 2, "type": "superior_subordinate",
     "context": "宝鸡市长与太白县长（上下级）", "overlap_org": "宝鸡市人民政府", "overlap_period": "current"},
    {"person_a": 1, "person_b": 17, "type": "predecessor_successor",
     "context": "前任太白县委书记(待查)与现任刘俊霞接任关系", "overlap_org": "中共太白县委员会", "overlap_period": "2025"},
    {"person_a": 14, "person_b": 2, "type": "overlap",
     "context": "挂职副县长（李少华）与县长", "overlap_org": "太白县人民政府", "overlap_period": "current"},
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
    print(f"\nDone: {SLUG} build complete.")