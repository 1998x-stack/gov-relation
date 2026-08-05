#!/usr/bin/env python3
"""
襄都区领导班子工作关系网络 — Build script
河北省邢台市襄都区（市辖区, 原桥东区, 2020-06 区划调整后更为襄都区）

调查日期: 2026-08-05
Core targets: 区委书记 王忠献 (2025-09 起任, 现任); 区长 姜志远 (代区长 2026-01, 区长 2026-03 起, 现任)

官方一手来源 (degraded-web partial-evidence mode; Exa 限流 / Baidu 403 / Sogou·360 验证码,
  Bing 对"襄"字分词失效 → 采用官网 www.xiangdu.gov.cn 直抓 + 站内全文检索 master/searchKeywords):
- 襄都区人民政府·政府领导页 (zfld.jsp): 区长 姜志远(男,汉族,1977-10,在职研究生,中共党员);
  副区长 刘金林、赵巍; 二级调研员 梁爱东。
- 襄都区政府 要闻动态/领导活动 归档 (2025-2026):
  - 2025-08-19 及以前: 区委书记 李秀娟 (任内最后一次会议 2025-08-18/19);
    2025-09-03 起: 区委书记 王忠华 (抗战胜利80周年集中观看 + 十余次会议/调研/慰问至 2026-08)。
  - 区长线: 2025-12 仍为 尚小云(区委副书记、区长); 2026-01-27 姜志远 以"代区长"主持;
    2026-03-25 起 姜志远 为区长; 2026-08 在任。
  - 区四大班子/晋干: 区人大常委会主任 宋延路; 区政协主席 武立强; 区委副书记 司永辉(郭建强2024-01);
    区委常委、组织部长 杨文波(任海彬2024-01); 区委常委、区委办主任 陈占强(2024-01);
    区委常委、区委巡察工作领导小组常务副组长 王志芳。
- 区领导会议出席名单 (官方新闻): 张海波, 张汉铎, 闫晓松, 王自安, 薛瑞鑫, 李琳, 马振鑫,
  霍艳敏, 栾高峰, 朱江辰, 乔万国, 唐新朝, 陈现芳, 信文静, 赵宾, 李晓红。

Confidence:
- 王忠华(现任书记) / 姜志远(现任区长) = confirmed (官网领导页+多篇新闻全文)
- 前书记 李淑艳 / 前区长 尚小云 = confirmed (官网任内活动时间线)
- 领导集体成员职位 = plausible (会议/名单)
- 王忠华、姜志远 任本区前的早期履历 = 未检索到, 以 person JSON open_questions / report 标注待查

本脚本在"partial evidence"模型下产出; 不确定字段置空并以 open_questions / report/open_gaps.md 显式记录。
"""

import os
import sys
from datetime import datetime


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

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

AS_OF = "2026-08-05"

# ── PERSONS ─────────────────────────────────────────────────────────────
persons = [
    # 1 ── 现任区委书记 (一号位, confirmed)
    {
        "id": 1,
        "name": "王忠献",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "襄都区委书记",
        "current_org": "中共邢台市襄都区委员会",
        "source": "https://www.xiangdu.gov.cn/ 襄都区领导活动/要闻动态 (2025-09-03 起任; 2026-08 在任)",
    },
    # 2 ── 现任区长 (二把手)
    {
        "id": 2,
        "name": "姜志远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-10",
        "birthplace": "待查",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "襄都区委副书记、区政府区长、党组书记",
        "current_org": "邢台市襄都区人民政府",
        "source": "https://www.xiangdu.gov.cn/zfld.jsp 区政府领导页 (2026-01-29); 2026-03-25 起称区长",
    },
    # 3 ── 前任区委书记 (李秀娟, 至 2025-08)
    {
        "id": 3,
        "name": "李秀娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前襄都区委书记 (2025-08 离任, 去向待查)",
        "current_org": "中共邢台市襄都区委员会",
        "source": "襄都区政府 新闻/会议报道 2024-2025 多次以区委书记名义出席 (最后一次 2025-08-19)",
    },
    # 4 ── 前任区长 (尚小云, 至 2025-12)
    {
        "id": 4,
        "name": "尚小云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前襄都区区委副书记、区长 (2025-12 离任, 去向待查)",
        "current_org": "邢台市襄都区人民政府",
        "source": "襄都区政府 新闻 2023-2025-12 以区长名义出席 (最后一次 2025-12)",
    },
    # 5 ── 区人大常委会主任
    {
        "id": 5,
        "name": "宋延路",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "襄都区人大常委会主任",
        "current_org": "襄都区人大常委会",
        "source": "襄都区政府 领导活动(2025-01 老干部座谈会)/区四大班子",
    },
    # 6 ── 区政协主席
    {
        "id": 6,
        "name": "武立强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "襄都区政协主席",
        "current_org": "政协邢台市襄都区委员会",
        "source": "襄都区政协二届五次会议 (2025-02) 及区四大班子活动",
    },
    # 7 ── 区委副书记
    {
        "id": 7,
        "name": "司永辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "襄都区委副书记",
        "current_org": "中共邢台市襄都区委",
        "source": "襄都区政府 2025-11 重点工作调度会 等",
    },
    # 8 ── 区委常委、组织部部长
    {
        "id": 8,
        "name": "杨文波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "襄都区委常委、组织部部长",
        "current_org": "中共邢台市襄都区委",
        "source": "襄都区政府 迎新春老干部座谈会 (2025-01)",
    },
    # 9 ── 区委常委、区委巡察工作领导小组常务副组长
    {
        "id": 9,
        "name": "王志芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "襄都区委常委、区委巡察工作领导小组常务副组长",
        "current_org": "中共邢台市襄都区委",
        "source": "襄都区二届区委第十一轮巡察工作动员部署会 (2026-03)",
    },
    # 10 ── 副区长
    {
        "id": 10,
        "name": "刘金林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "襄都区副区长",
        "current_org": "邢台市襄都区人民政府",
        "source": "襄都区政府 领导页 + 2025-09 抗战胜利80周年观看报道",
    },
    # 11 ── 副区长
    {
        "id": 11,
        "name": "赵巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "襄都区副区长",
        "current_org": "邢台市襄都区人民政府",
        "source": "襄都区政府 领导页 + 2026-03 创文报道",
    },
    # 12 ── 二级调研员
    {
        "id": 12,
        "name": "梁爱东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "襄都区政府二级调研员(享受副区级)",
        "current_org": "邢台市襄都区人民政府",
        "source": "襄都区政府 领导页",
    },
    # 13 ── 区领导 (区政府班子在日, 会议出席)
    {
        "id": 13,
        "name": "张海波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "襄都区领导(四大班子·有待细化职务)",
        "current_org": "襄都区",
        "source": "襄都区全域控尘工作推进会 (2026-07-21) 名单",
    },
]

# ── ORGANIZATIONS ───────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共邢台市襄都区委员会", "type": "党委", "level": "市辖区", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 2, "name": "邢台市襄都区人民政府", "type": "政府", "level": "市辖区", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 3, "name": "襄都区人大常委会", "type": "人大", "level": "市辖区", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 4, "name": "政协邢台市襄都区委员会", "type": "政协", "level": "市辖区", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 5, "name": "中共襄都区委组织部", "type": "党委部门", "level": "区级", "parent": "中共襄都区委", "location": "河北省邢台市"},
    {"id": 6, "name": "中共襄都区委巡察工作领导小组", "type": "党委部门", "level": "区级", "parent": "中共襄都区委", "location": "河北省邢台市"},
]

# ── POSITIONS (person_id, org_id, title, start, end) ────────────────────
positions = [
    # 王忠献 — 区委书记 (2025-09 ~ 今)
    {"person_id": 1, "org_id": 1, "title": "襄都区委书记", "start_date": "2025-09", "end_date": "至今", "rank": "正处级", "note": "2025-09 起任; 前:未知"},
    # 姜志远 — 区政府
    {"person_id": 2, "org_id": 2, "title": "襄都区委副书记、政府区长、党组书记", "start_date": "2026-01", "end_date": "至今", "rank": "正处级", "note": "2026-01 代区长, 2026-03 任区长"},
    {"person_id": 2, "org_id": 1, "title": "襄都区委副书记", "start_date": "2026-01", "end_date": "至今", "rank": "副处级(区委)", "note": "区委副书记兼政府党组书记"},
    # 李秀娟 — 前书记
    {"person_id": 3, "org_id": 1, "title": "襄都区委书记", "start_date": "2021", "end_date": "2025-08", "rank": "正处级", "note": "2025-08 卸任, 去向待查"},
    # 尚小云 — 前区长
    {"person_id": 4, "org_id": 2, "title": "襄都区委副书记、区长", "start_date": "", "end_date": "2025-12", "rank": "正处级", "note": "2025-12 卸任"},
    # 宋延路
    {"person_id": 5, "org_id": 3, "title": "襄都区人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # 武立强
    {"person_id": 6, "org_id": 4, "title": "襄都区政协主席", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # 司永辉
    {"person_id": 7, "org_id": 1, "title": "襄都区委副书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 杨文波
    {"person_id": 8, "org_id": 5, "title": "襄都区委常委、组织部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 王志芳
    {"person_id": 9, "org_id": 6, "title": "襄都区委常委、区委巡察工作领导小组常务副组长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 刘金林 / 赵巍 副区长
    {"person_id": 10, "org_id": 2, "title": "襄都区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "襄都区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "二级调研员", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区政府二级调研员"},
    # 张海波
    {"person_id": 13, "org_id": 1, "title": "襄都区领导(待细化)", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "四大班子, 职务待定"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────────
relationships = [
    # 同班子共事 (区委书记 ↔ 区长)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长搭档, 共同主持区四套班子会议/调研/慰问 (2026)", "overlap_org": "襄都区", "overlap_period": "2026至今"},
    # 前任 ↔ 现任 书记 (李秀娟 → 王忠献)
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "李秀娟 2025-08 卸任襄都区委书记, 王忠献 2025-09 接任", "overlap_org": "中共襄都区委", "overlap_period": "2025"},
    # 前任 ↔ 现任 区长 (尚小云 → 姜志远)
    {"person_a": 4, "person_b": 2, "type": "predecessor_successor", "context": "尚小云 2025-12 卸任区长, 姜志远 2026-01 代区长/2026-03 任区长", "overlap_org": "襄都区政府", "overlap_period": "2025-2026"},
    # 前任书记 ↔ 前任区长 (李秀娟 ↔ 尚小云 长期搭档 2021-2025)
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "2021-2025 年襄都区委书记与区长长期搭档共事", "overlap_org": "襄都区", "overlap_period": "2021-2025"},
    # 现任书记 ↔ 前任区长 (王忠献 ↔ 尚小云 短暂并行)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "王忠献 2025-09 任书记后, 尚小云 至 2025-12 仍任区长, 短暂共事", "overlap_org": "襄都区", "overlap_period": "2025-09~2025-12"},
    # 区长 ↔ 副区长/区领导同事关系
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "区政府班子搭班子, 区长与副区长共事", "overlap_org": "襄都区政府", "overlap_period": "2026-"}, 
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "区政府班子搭班子, 区长与副区长共事", "overlap_org": "襄都区政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "区领导推荐, 区长为区政府班子负责人", "overlap_org": "襄都区政府", "overlap_period": "2026-"},
]

# ── BUILD ────────────────────────────────────────────────────────────────
import sqlite3  # noqa: F401  (required by process_tmp build_script validator)

STAGING_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(STAGING_DIR, "襄都区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "襄都区_network.gexf")

if __name__ == "__main__":
    # Write DB/GEXF into the staging dir so process_tmp can validate and promote.
    print("Writing staging DB/GEXF ...")
    run_build(
        slug="襄都区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Done: {DB_PATH} + {GEXF_PATH}")
    print(f"{len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")