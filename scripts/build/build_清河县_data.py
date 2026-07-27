#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 清河县 leadership network.

Level: 县
Province: 河北省
Parent city: 邢台市
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
Task ID: hebei_清河县

Research date: 2026-07-23
Official site: https://www.qinghexian.gov.cn/

Current status (as of 2026-07-23):
- 县委书记: 樊振宇 — confirmed by official news (2026-07-18)
- 县长: 刘志诚 — confirmed by 2026 government work report (2026-01-27)
- 县委副书记: 常振刚 — confirmed by multiple 2026 news articles
- 常务副县长: 鞠占稳 (男, 汉族, 1976-09, 广宗县人, 中央党校研究生)
- 纪委书记: 杨文卓 (男, 汉族, 1974-03, 南和县人)
- 组织部长: 王旭 — confirmed by 2026 news
- 常委/办公室主任: 张海斌 — confirmed by 2026 news
- 5 deputy county mayors: 安铭(兼公安局长), 郭兵, 王晓磊, 王其良, 尚瑞
- Predecessor 县委书记: 张剑 (last seen 2025-11-10)
- Predecessor chain (县长): 韩恺(2018代~2021) → 郭卫欣(~2021) → 闫恒卓(~2021~2025) → 刘志诚(~2025-)
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "清河县"
TASK_ID = "hebei_清河县"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

AS_OF = "2026-07-23"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 县领导 Core Leaders (1-10) ──
    {
        "id": 1,
        "name": "樊振宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共清河县委",
        "source": "https://www.qinghexian.gov.cn/news/12023.cshtml",
    },
    {
        "id": 2,
        "name": "刘志诚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "清河县人民政府",
        "source": "https://www.qinghexian.gov.cn/news/11964.cshtml",
    },
    # ── 县委副书记 ──
    {
        "id": 4,
        "name": "常振刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共清河县委",
        "source": "https://www.qinghexian.gov.cn/",
    },
    # ── 常务副县长 ──
    {
        "id": 3,
        "name": "鞠占稳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-09",
        "birthplace": "河北省邢台市广宗县",
        "education": "中央党校研究生",
        "party_join": "1998-12",
        "work_start": "1995-09",
        "current_post": "常务副县长",
        "current_org": "清河县人民政府",
        "source": "https://www.qinghexian.gov.cn/news/7923.cshtml",
    },
    # ── 纪委书记 ──
    {
        "id": 5,
        "name": "杨文卓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-03",
        "birthplace": "河北省邢台市南和县",
        "education": "中央党校大学",
        "party_join": "1995-05",
        "work_start": "1994-08",
        "current_post": "纪委书记",
        "current_org": "中共清河县纪委",
        "source": "https://baike.baidu.com/item/%E6%9D%A8%E6%96%87%E5%8D%93/58372533",
    },
    # ── 组织部长 ──
    {
        "id": 6,
        "name": "王旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "组织部长",
        "current_org": "中共清河县委组织部",
        "source": "https://www.qinghexian.gov.cn/news/11954.cshtml",
    },
    # ── 常委/办公室主任 ──
    {
        "id": 7,
        "name": "张海斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、办公室主任",
        "current_org": "中共清河县委",
        "source": "https://www.qinghexian.gov.cn/",
    },
    # ── 副县长 (11-15) ──
    {
        "id": 11,
        "name": "安铭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-12",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、公安局长",
        "current_org": "清河县人民政府",
        "source": "https://www.qinghexian.gov.cn/ldml/",
    },
    {
        "id": 12,
        "name": "郭兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "清河县人民政府",
        "source": "https://www.qinghexian.gov.cn/ldml/",
    },
    {
        "id": 13,
        "name": "王晓磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "清河县人民政府",
        "source": "https://www.qinghexian.gov.cn/ldml/",
    },
    {
        "id": 14,
        "name": "王其良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "清河县人民政府",
        "source": "https://www.qinghexian.gov.cn/ldml/",
    },
    {
        "id": 15,
        "name": "尚瑞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "清河县人民政府",
        "source": "https://www.qinghexian.gov.cn/ldml/",
    },
    # ── 前县委书记 Predecessor ──
    {
        "id": 30,
        "name": "张剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前县委书记（待查去向）",
        "current_org": "（待查）",
        "source": "https://www.qinghexian.gov.cn/news/11596.cshtml",
    },
    # ── 前县长 Predecessors (21-23) ──
    {
        "id": 21,
        "name": "闫恒卓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前县长",
        "current_org": "（待查离任后去向）",
        "source": "https://www.qinghexian.gov.cn/news/10977.cshtml",
    },
    {
        "id": 22,
        "name": "郭卫欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前县长",
        "current_org": "（待查离任后去向）",
        "source": "https://www.qinghexian.gov.cn/news/7650.cshtml",
    },
    {
        "id": 23,
        "name": "韩恺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前县长",
        "current_org": "（待查离任后去向）",
        "source": "https://www.qinghexian.gov.cn/news/4964.cshtml",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共清河县委",
        "type": "党委",
        "level": "县级",
        "parent": "邢台市委",
        "location": "邢台市清河县",
    },
    {
        "id": 2,
        "name": "清河县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "邢台市人民政府",
        "location": "邢台市清河县",
    },
    {
        "id": 3,
        "name": "中共清河县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "邢台市纪委",
        "location": "邢台市清河县",
    },
    {
        "id": 4,
        "name": "中共清河县委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共清河县委",
        "location": "邢台市清河县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # Current leaders
    {
        "person_id": 1,
        "org_id": 1,
        "title": "县委书记",
        "start_date": "~2025-12",
        "end_date": "",
        "rank": "正处级",
        "note": "前任张剑2025-11-10最后一次以县委书记出现；樊振宇2026-01-04首次以县委书记出现",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "县长",
        "start_date": "2025-09（代）",
        "end_date": "",
        "rank": "正处级",
        "note": "2025-09-25首次以代县长出现；2026-01-27正式县长作政府工作报告",
    },
    {
        "person_id": 4,
        "org_id": 1,
        "title": "县委副书记",
        "start_date": "",
        "end_date": "",
        "rank": "副处级",
        "note": "2026年多次新闻报道确认",
    },
    {
        "person_id": 3,
        "org_id": 2,
        "title": "常务副县长",
        "start_date": "2021-07",
        "end_date": "",
        "rank": "副处级",
        "note": "县委常委，分管常务工作，协助县长负责审计",
    },
    {
        "person_id": 5,
        "org_id": 3,
        "title": "纪委书记、监委代理主任",
        "start_date": "2022-03",
        "end_date": "",
        "rank": "副处级",
        "note": "县委常委，2022-02起任县委常委、纪委书记",
    },
    {
        "person_id": 6,
        "org_id": 4,
        "title": "组织部长",
        "start_date": "",
        "end_date": "",
        "rank": "副处级",
        "note": "县委常委，2026-03新闻确认",
    },
    {
        "person_id": 7,
        "org_id": 1,
        "title": "县委常委、办公室主任",
        "start_date": "",
        "end_date": "",
        "rank": "副处级",
        "note": "2026年新闻报道确认",
    },
    # Deputy county mayors
    {
        "person_id": 11,
        "org_id": 2,
        "title": "副县长、公安局长",
        "start_date": "2023-12",
        "end_date": "",
        "rank": "副处级",
        "note": "兼任县公安局局长",
    },
    {
        "person_id": 12,
        "org_id": 2,
        "title": "副县长",
        "start_date": "",
        "end_date": "",
        "rank": "副处级",
        "note": "",
    },
    {
        "person_id": 13,
        "org_id": 2,
        "title": "副县长",
        "start_date": "",
        "end_date": "",
        "rank": "副处级",
        "note": "",
    },
    {
        "person_id": 14,
        "org_id": 2,
        "title": "副县长",
        "start_date": "",
        "end_date": "",
        "rank": "副处级",
        "note": "",
    },
    {
        "person_id": 15,
        "org_id": 2,
        "title": "副县长",
        "start_date": "",
        "end_date": "",
        "rank": "副处级",
        "note": "",
    },
    # Predecessor chain
    {
        "person_id": 30,
        "org_id": 1,
        "title": "县委书记",
        "start_date": "",
        "end_date": "~2025-12",
        "rank": "正处级",
        "note": "2025-11-10仍以县委书记身份出现，其后由樊振宇接任",
    },
    {
        "person_id": 21,
        "org_id": 2,
        "title": "县长",
        "start_date": "~2021",
        "end_date": "~2025-08",
        "rank": "正处级",
        "note": "连续4年作政府工作报告（2022-2025年），2025-08-13最后一次出现",
    },
    {
        "person_id": 22,
        "org_id": 2,
        "title": "县长",
        "start_date": "~2021",
        "end_date": "~2021",
        "rank": "正处级",
        "note": "2021-02-06作2020年政府工作报告",
    },
    {
        "person_id": 23,
        "org_id": 2,
        "title": "县长",
        "start_date": "2018（代）",
        "end_date": "~2021",
        "rank": "正处级",
        "note": "2020-01-18正式县长作2019年报告",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # Predecessor-successor (县委书记)
    {
        "person_a": 30,
        "person_b": 1,
        "type": "predecessor-successor",
        "context": "县委书记交接",
        "overlap_org": "中共清河县委",
        "overlap_period": "~2025-12",
    },
    # Predecessor-successor (县长 chain)
    {
        "person_a": 23,
        "person_b": 22,
        "type": "predecessor-successor",
        "context": "县长交接",
        "overlap_org": "清河县人民政府",
        "overlap_period": "~2021",
    },
    {
        "person_a": 22,
        "person_b": 21,
        "type": "predecessor-successor",
        "context": "县长交接",
        "overlap_org": "清河县人民政府",
        "overlap_period": "~2021/2022",
    },
    {
        "person_a": 21,
        "person_b": 2,
        "type": "predecessor-successor",
        "context": "县长交接",
        "overlap_org": "清河县人民政府",
        "overlap_period": "~2025",
    },
    # 县委-县政府
    {
        "person_a": 1,
        "person_b": 2,
        "type": "party-gov",
        "context": "党政搭档",
        "overlap_org": "清河县",
        "overlap_period": AS_OF,
    },
    # 书记-副书记
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior-subordinate",
        "context": "书记与副书记工作关系",
        "overlap_org": "中共清河县委",
        "overlap_period": AS_OF,
    },
    # 书记-常务副县长
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior-subordinate",
        "context": "县委与常务副县长",
        "overlap_org": "中共清河县委/清河县人民政府",
        "overlap_period": AS_OF,
    },
    # 书记-纪委书记
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior-subordinate",
        "context": "县委与纪委",
        "overlap_org": "中共清河县委",
        "overlap_period": AS_OF,
    },
    # 书记-组织部长
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior-subordinate",
        "context": "县委与组织部",
        "overlap_org": "中共清河县委",
        "overlap_period": AS_OF,
    },
    # 县长-常务副县长
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior-subordinate",
        "context": "县长与常务副县长工作关系，协助审计",
        "overlap_org": "清河县人民政府",
        "overlap_period": "~2025至今",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    TMP_DIR.mkdir(parents=True, exist_ok=True)

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

    import sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    pc = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    oc = conn.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
    conn.close()

    print(f"\n{SLUG} v2 data written to {TMP_DIR}")
    print(f"  DB:   {DB_PATH} ({pc} persons, {oc} orgs)")
    print(f"  GEXF: {GEXF_PATH}")
    print()
    print(f"Current leadership (2026):")
    print(f"  县委书记: 樊振宇 (since ~2025-12, predecessor: 张剑)")
    print(f"  县长: 刘志诚 (1976-09 代→2026-01 正式, predecessor: 闫恒卓)")
    print(f"  县委副书记: 常振刚")
    print(f"  常务副县长: 鞠占稳 (1976-09, 广宗人, 中央党校研究生)")
    print(f"  纪委书记: 杨文卓 (1974-03, 南和人)")
    print(f"  组织部长: 王旭")
    print(f"  常委/办公室主任: 张海斌")
    print(f"  副县长兼公安局长: 安铭 (1971-12)")
    print(f"  副县长: 郭兵, 王晓磊, 王其良, 尚瑞")
    print()
    print(f"Confirmed successor chain (县长): 韩恺 → 郭卫欣 → 闫恒卓 → 刘志诚")
    print(f"Confirmed successor chain (书记): 张剑 → 樊振宇")
    print()
    print("Gaps remaining:")
    print("  1. 樊振宇, 刘志诚, 常振刚, 王旭, 张海斌, 张剑 — 完整履历")
    print("  2. 闫恒卓, 郭卫欣, 韩恺, 张剑 — 离任后去向")
    print("  3. 5位副县长(郭兵, 王晓磊, 王其良, 尚瑞) — 个人简历与分管领域")
    print("  4. 政法委书记, 宣传部长, 统战部长 — 姓名未知")
    print("  5. 跨县干部交流模式")
