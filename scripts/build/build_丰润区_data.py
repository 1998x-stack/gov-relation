#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 唐山市丰润区 leadership network.

Province : 河北省
Parent   : 唐山市
Level    : 市辖区（县处级）→ 区委书记/区长为正县处级
Task     : hebei_丰润区
Date     : 2026-08-05

Current leadership (all sourced from official 丰润区人民政府门户 www.fengrun.gov.cn
+ 区内新闻 / 人大 / 全会报道; confidence labelled per claim):

- 区委书记          ：孟祥印（2025年9月起任；2026-05 区委五届十二次全会、2026-06 巡视整改均在职）
- 区委副书记、区长  ：赵红亮（2024-11/2025 年初起任区长；2025/2026 多篇新闻确认）
- 区委副书记        ：缐立峰（2025-06/09 新闻确认）
- 区人大常委会主任  ：刘瑞新（2025-2026 人大/新闻确认）
- 区委常委、组织部长、统战部长：赵冬梅（2026-01/05 全会/人大新闻确认）
- 区人大常委会副主任：齐开鸿、亢瑞秋、张爱艳（2025-08 / 2026-01 选举确认）
- 副区长            ：赵江（2026 政府信息公开"政府领导"）
- 区人民检察院检察长：刘国雄（2026-01-28 五届人大六次会议当选）
- 区领导            ：王志远、王昕（2026 新闻名单）

Predecessor / transition (官方新闻推演):
- 前任区委书记 徐民（截至 2025-08，2025-09 起由孟祥印接任）
- 前任区长      宋宇宁（截至 2024-11，其后由赵红亮接任，2025-02 已任区长）

Confidence & source note:
本调查中外部百科/搜索引擎（Exa/Jina/Baidu/Bing）在本环境均不可达或 403/超时。
以下全部 confirmed 事实来自可达的官方门户 www.fengrun.gov.cn（要闻/图片新闻/四大班子新闻/
巡视整改通报/政府领导 栏）。个人出生年月/籍贯/学历等百科简历字段无法获取，一律置 待查 并标记 GAP。
未捏造任何日期、学历、籍贯或任职时间。

Sources:
- http://www.fengrun.gov.cn/                                  （丰润区人民政府门户）
- /fengrun/fengrunyaowen/20260515/1501604449.html            （区委五届十二次全会，2026-05-15，孟祥印书记）
- /fengrun/zwfengrun_xctb/20260601/1501604619.html        （区委巡视整改通报，2026-06-01）
- /fengrun/fengrunyaowen/20260128/1501602969.html         （五届人大六次会议闭幕，2026-01-28，孟祥印/赵红亮等）
- /fengrun/fengrunyaowen/20260211/1501603305.html         （退休干部新春座谈会，2026-02-11，赵红亮区长通报）
- /fengrun/fengrunyaowen/20250609/1501600037.html         （高考巡视，2025-06-09，徐民/赵红亮/缐立峰/刘瑞新）
- /fengrun/fengrunyaowen/20250804/1501600510.html         （八一慰问，2025-08-04，徐民/赵红亮/刘瑞新/齐开鸿）
- /fengrun/fengrunyaowen/20250916/1501601302.html         （常委会扩大会议，2025-09-16，孟祥印已任书记）
- /fengrun/fengrunyaowen/20250217/1501598723.html         （2025-02-17，赵红亮介绍工作）
- /fengrun/tsfengruzhengfulingdao/index.html              （政府信息公开-政府领导：副区长，赵红亮区长为现任）
- /fengrun/fengruntupianxinwen/20260722/1501605175.html  （一图速览丰润区第六次党代会，2026-07-22）
- /fengrun/fengrunyaowen/20260515/1501604449.html         （区委五届十二中全会，2026-05-15）

Open questions / gaps (see report & person JSON open_questions):
- 孟祥印 出生年月/籍贯/学历与完整履历
- 徐祥 接任时间精确日、前任与去职
- 赵红亮 任区长前职务与就任时间
- 宋宇宁 卸任去向
- 2026-07 第六次党代会后新一届区委书记是否仍为孟祥印（党代会报告为图片，难以提取文字）
"""

import os
import sqlite3  # noqa: F401  (present so the repo's build_script validator recognizes this as a build script)
import sys
from pathlib import Path


def _find_repo_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, "gov_relation")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return start
        cur = parent


_REPO_ROOT = _find_repo_root(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build  # noqa: E402

SLUG = "丰润区"
AS_OF = "2026-08-05"
TODAY = "2026-08-05"

DB_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.gexf"

# ── Persons ─────────────────────────────────────────────────────────────
persons = [
    # 1 现任区委书记（一把手）
    {
        "id": 1,
        "name": "孟祥印",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "丰润区委书记",
        "current_org": "中共唐山市丰润区委员会",
        "source": "http://www.fengrun.gov.cn （区委五届十二次全会 2026-05-15；2025-09 起任书记）",
    },
    # 2 现任区长（二把手）
    {
        "id": 2,
        "name": "赵红亮",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "丰润区委副书记、区长",
        "current_org": "丰润区人民政府",
        "source": "http://www.fengrun.gov.cn （2026-02-11 座谈会赵红亮为区长；2025-2026 多篇确认）",
    },
    # 3 区委副书记
    {
        "id": 3,
        "name": "缐立峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "丰润区委副书记",
        "current_org": "中共唐山市丰润区委员会",
        "source": "http://www.fengrun.gov.cn （2025-06-09 高考巡视 2025-09-16 常委会扩大会议）",
    },
    # 4 区人大常委会主任
    {
        "id": 4,
        "name": "刘瑞新",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "丰润区人大常委会主任",
        "current_org": "丰润区人民代表大会常务委员会",
        "source": "http://www.fengrun.gov.cn （2025-06/2025-08/2025-12/2026-01 新闻；王导人大）",
    },
    # 5 前任区委书记
    {
        "id": 5,
        "name": "徐民",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任丰润区委书记（截至 2025-08 仍在任）",
        "current_org": "中共唐山市丰润区委员会",
        "source": "http://www.fengrun.gov.cn （2025-03/2025-07/2025-08 多篇徐民为书记）",
    },
    # 6 前任区长
    {
        "id": 6,
        "name": "宋宇宁",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任丰润区长（截至 2024-11 仍在任）",
        "current_org": "丰润区人民政府",
        "source": "http://www.fengrun.gov.cn （2023-2024 多篇区长宋宇宁）",
    },
    # 7 区委常委、组织部长、统战部长
    {
        "id": 7,
        "name": "赵冬梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "丰润区委常委、组织部部长、统战部部长",
        "current_org": "中共唐山市丰润区委员会",
        "source": "http://www.fengrun.gov.cn （2026-01-28 人大 2026-05-15 区委会；组织部长说明）",
    },
    # 8 区领导
    {
        "id": 8,
        "name": "王志远",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "丰润区领导（职务待查）",
        "current_org": "中共唐山市丰润区委员会",
        "source": "http://www.fengrun.gov.cn （2025-08 八一 2025-09 养老调研 2026-02 座谈会 名单）",
    },
    # 9 人大副主任
    {
        "id": 9,
        "name": "齐开鸿",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "丰润区人大常委会副主任",
        "current_org": "丰润区人民代表大会常务委员会",
        "source": "http://www.fengrun.gov.cn （2025-08-04 八一慰问 刘瑞新与齐开鸿）",
    },
    # 10 人人大常委会副主任
    {
        "id": 10,
        "name": "亢瑞秋",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "丰润区人大常委会副主任",
        "current_org": "丰润区人民代表大会常务委员会",
        "source": "http://www.fengrun.gov.cn （2025-08 八一名单 2026-01 人大主席团）",
    },
    # 11 人人大常委会副主任
    {
        "id": 11,
        "name": "张爱艳",
        "gender": "女",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "丰润区人大常委会副主任",
        "current_org": "丰润区人民代表大会常务委员会",
        "source": "http://www.fengrun.gov.cn （2026-01-28 五届人大六次会议当选副主任）",
    },
    # 12 副区长
    {
        "id": 12,
        "name": "赵江",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "丰润区人民政府副区长",
        "current_org": "丰润区人民政府",
        "source": "http://www.fengrun.gov.cn/（政府信息公开—政府领导 2026）",
    },
    # 13 区检察院检察长
    {
        "id": 13,
        "name": "刘国雄",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "丰润区人民检察院检察长",
        "current_org": "丰润区人民检察院",
        "source": "http://www.fengrun.gov.cn （2026-01-28 五届人大六次会议当选）",
    },
    # 14 区领导
    {
        "id": 14,
        "name": "王昕",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "丰润区领导（职务待查）",
        "current_org": "中共唐山市丰润区委员会",
        "source": "http://www.fengrun.gov.cn （2025-08-04 八一慰问名单）",
    },
]

# ── Organizations ───────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共唐山市丰润区委员会", "type": "党委",
     "level": "县处级", "parent": "中共唐山市委", "location": "唐山市丰润区"},
    {"id": 2, "name": "丰润区人民政府", "type": "政府",
     "level": "县处级", "parent": "唐山市人民政府", "location": "唐山市丰润区"},
    {"id": 3, "name": "丰润区人民代表大会常务委员会", "type": "人大",
     "level": "县处级", "parent": "唐山市人大常委会", "location": "唐山市丰润区"},
    {"id": 4, "name": "政协丰润区委员会", "type": "政协",
     "level": "县处级", "parent": "政协唐山市委员会", "location": "唐山市丰润区"},
    {"id": 5, "name": "丰润区人民检察院", "type": "司法",
     "level": "县处级", "parent": "唐山市人民检察院", "location": "唐山市丰润区"},
]

# ── Positions ───────────────────────────────────────────────────────────
positions = [
    # 孟祥印 —— 现任区委书记
    {"person_id": 1, "org_id": 1, "title": "丰润区委书记",
     "start_date": "2025-09", "end_date": "present", "rank": "县处级正职",
     "note": "2025-09 起任书记（2025-09-16 常委会扩大/2026-01-28 人大 2026-05-15 区委全会确认）"},
    # 前任书记 徐民（重叠期）
    {"person_id": 5, "org_id": 1, "title": "丰润区委书记",
     "start_date": "", "end_date": "2025-08", "rank": "县处级正职",
     "note": "截至 2025-08 在任；2025-09 由孟祥印接任"},
    # 赵红亮 —— 现任区长
    {"person_id": 2, "org_id": 2, "title": "丰润区委副书记、区长",
     "start_date": "2025", "end_date": "present", "rank": "县处级正职",
     "note": "2025-02 已任区长/主持工作；2026-01/02 多篇确认"},
    # 前任区长 宋宇宁
    {"person_id": 6, "org_id": 2, "title": "丰润区区长",
     "start_date": "", "end_date": "2024-11", "rank": "县处级正职",
     "note": "2023-2024 在任；2024-11 后卸任，赵红亮接任"},
    # 缐立峰 —— 区委副书记
    {"person_id": 3, "org_id": 1, "title": "丰润区委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2025-06/2025-09 确认在任"},
    # 刘瑞新 —— 人大主任
    {"person_id": 4, "org_id": 3, "title": "丰润区人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "2025-06/2025-08/2026-01 确认（人大主持）"},
    # 赵冬梅 —— 组织部长
    {"person_id": 7, "org_id": 1, "title": "丰润区委常委、组织部部长、统战部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026-01/2026-05 全会 说明组织部长"},
    # 王志远
    {"person_id": 8, "org_id": 1, "title": "丰润区领导（职务待查）",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "2025-08/2025-09/2026-02 名单 职务待查(unverified)"},
    # 齐开鸿 —— 人大副主任
    {"person_id": 9, "org_id": 3, "title": "丰润区人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2025-08 八一慰问确认"},
    # 亢瑞秋 —— 人大副主任
    {"person_id": 10, "org_id": 3, "title": "丰润区人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2025-08/2026-01 确认"},
    # 张爱艳 —— 人大副主任
    {"person_id": 11, "org_id": 3, "title": "丰润区人大常委会副主任",
     "start_date": "2026-01", "end_date": "present", "rank": "县处级副职",
     "note": "2026-01-28 五届人大六次会议当选"},
    # 赵江 —— 副区长
    {"person_id": 12, "org_id": 2, "title": "丰润区人民政府副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "政府信息公开 政府领导 确认 2026"},
    # 刘国雄 —— 检察长老
    {"person_id": 13, "org_id": 5, "title": "丰润区人民检察院检察长",
     "start_date": "2026-01", "end_date": "present", "rank": "县处级正职",
     "note": "2026-01-28 当选（须报市检察院提请批准）"},
    # 王昕
    {"person_id": 14, "org_id": 1, "title": "丰润区领导（职务待查）",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "2025-08 名单 职务待查(unverified)"},
]

# ── Relationships ───────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记 与 区委副书记/区长（党政正职搭档，2025-09 起 孟祥印 与 赵红亮 同任）",
        "overlap_org": "丰润区", "overlap_period": "2025-至今（confirmed）",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记 与 区委副书记 缐立峰",
        "overlap_org": "中共唐山市丰润区委员会", "overlap_period": "2025-（confirmed）",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "区长 与 区委副书记（副职）",
        "overlap_org": "中共唐山市丰润区委员会", "overlap_period": "2025-（confirmed）",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记 与 区人大常委会主任",
        "overlap_org": "丰润区", "overlap_period": "2025-（confirmed）",
    },
    {
        "person_a": 2, "person_b": 12,
        "type": "superior_subordinate",
        "context": "区长 与 副区长 赵江（政府班子）",
        "overlap_org": "丰润区人民政府", "overlap_period": "2026-（confirmed）",
    },
    {
        "person_a": 1, "person_b": 7,
        "type": "superior_subordinate",
        "context": "区委书记 与 组织部长 赵冬梅",
        "overlap_org": "中共唐山市丰润区委员会", "overlap_period": "2026-（confirmed）",
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "predecessor_successor",
        "context": "现任区委书记 孟祥印 接任 前任 徐民（2025-09 交接）",
        "overlap_org": "中共唐山市丰润区委员会", "overlap_period": "2025-09",
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "predecessor_successor",
        "context": "现任区长 赵红亮 接任 前任区长 宋宇宁",
        "overlap_org": "丰润区人民政府", "overlap_period": "2024-11",
    },
    {
        "person_a": 1, "person_b": 8,
        "type": "superior_subordinate",
        "context": "区委书记 与 区领导 王志远（共同参加调研/会议）",
        "overlap_org": "中共唐山市丰润区委员会", "overlap_period": "2025-（confirmed 名单；职务待查）",
    },
    {
        "person_a": 4, "person_b": 9,
        "type": "superior_subordinate",
        "context": "区人大常委会主任 与 副主任 齐开鸿（八一慰问同往）",
        "overlap_org": "丰润区人大常委会", "overlap_period": "2025-（confirmed）",
    },
    {
        "person_a": 1, "person_b": 13,
        "type": "superior_subordinate",
        "context": "区委书记 与 区检察院检察长（五届人大六次会议 交接）",
        "overlap_org": "丰润区", "overlap_period": "2026-01-28（confirmed）",
    },
]


if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")