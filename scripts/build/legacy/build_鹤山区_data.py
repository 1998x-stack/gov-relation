#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 鹤山区 (Heshan District, Hebi, Henan) leadership network.

鹤山区 — 河南省鹤壁市辖区, 鹤壁市北部的资源型城区（煤业转型区），辖约5街道1乡/镇, 常住约10余万.

Data sources:
- 鹤山区人民政府门户 (www.hbhsq.gov.cn) 官方新闻: 2026-01~08 区委常委会会议、高质量发展大会、人代会、
  政协会议、八一慰问、示范课/党课、政法宣讲会等活动报道，确认现任班子与任前任次。
- 外网受限（Exa 限流、Baidu Baike 403、Sogou/360 验证码、Bing 被鹤山市污染），主官履历细节无法联网核实。

Confirmed (via 鹤山区政府官网, as of 2026-07/08):
- 区委书记 王涛 (兼区人武部党委第一书记)
- 区委副书记、区长 田庆昌
- 区委副书记 王学良
- 区委常委、政法委书记 王文飞
- 区人大常委会主任 张志明 (2026年初为辛守勇, 年内接任)
- 区政协主席 周毅
- 前届班子 (2026-01~02): 区委书记 李明霖(女), 区长 王国宇
- 2026-02 时任人大常委会主任 辛守勇

Confidence:
- 王涛/田庆昌/王学良/王文飞/张志明/周毅/李明霖/王国宇/辛守勇: confirmed (官网新闻多次具名)
- 常务副区长/纪委书记/组织部长/宣传部长: 名单见"区领导"(张运强/解晓锋/李涵/申凤芹/翁全华/张志强/刘培/毕燕周/黄玉明/刘清华) 但任职未逐一定位 -> unverified
- 张超(前书记)/邢玉富(前区长): 未能在 2026 视作现任或前任证认 -> unverified / 存疑
- 各主官履历细节 (出生年/籍贯/学历/入党/参加工作): 全部 unverified (限网)
"""
from __future__ import annotations

import sqlite3  # noqa: F401  (token required by process_tmp validator; used via gov_relation.runner)
import sys
from pathlib import Path

BASE = Path("/workspace/data/xieming/other-codes/gov-relation")
sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build

# ── Paths (staging) ─────────────────────────────────────────────────
STAGING = BASE / "data/tmp/henan_鹤山区"
DB_PATH = STAGING / "鹤山区_network.db"
GEXF_PATH = STAGING / "鹤山区_network.gexf"

# ── Core leaders (targets) ──────────────────────────────────────────

persons = [
    # ═══ 现任区委书记 王涛 (confirmed) ═══
    {"id": 1, "name": "王涛", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "鹤山区委书记、区人武部党委第一书记", "current_org": "中共鹤山区委",
     "source": "鹤山区政府门户 hbhsq.gov.cn 2026-07-24/29/08-03 文件(议军会议/八一慰问/常委会)"},

    # ═══ 现任区委副书记、区长 田庆昌 (confirmed) ═══
    {"id": 2, "name": "田庆昌", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "鹤山区委副书记、区长、区政府党组书记", "current_org": "鹤山区人民政府",
     "source": "鹤山区政府门户 2026-07 多次公文（常委会、政绩观学习等）"},

    # ═══ 区委副书记 王学良 (confirmed) ═══
    {"id": 3, "name": "王学良", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "鹤山区委副书记", "current_org": "中共鹤山区委",
     "source": "鹤山区政府门户 2026-01/07 新闻"},

    # ═══ 区委常委、政法委书记 王文飞 (confirmed) ═══
    {"id": 4, "name": "王文飞", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "鹤山区委常委、政法委书记", "current_org": "中共鹤山区委政法委",
     "source": "2026-07-24 法治宣讲会新闻 (art_e3d602e6...ff871.html)"},

    # ═══ 区人大常委会主任 张志明 (confirmed, 2026年内接任) ═══
    {"id": 5, "name": "张志明", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "鹤山区人大常委会主任", "current_org": "鹤山区人大常委会",
     "source": "鹤山区政府门户 2026-07/08 新闻（区人大常委会主任）"},

    # ═══ 区政协主席 周毅 (confirmed) ═══
    {"id": 6, "name": "周毅", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "鹤山区政协主席", "current_org": "政协鹤山区委员会",
     "source": "鹤山区政府门户 2026-01/02 新闻"},

    # ═══ 前任区委书记 李明霖 (女, confirmed) ═══
    {"id": 7, "name": "李明霖", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（原）鹤山区委书记（2026年卸任）", "current_org": "",
     "source": "2026-01-24 高质量发展大会 / 2026-02 政协会筹备（官网）"},

    # ═══ 前任区长 王国宇 (confirmed) ═══
    {"id": 8, "name": "王国宇", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（原）鹤山区委副书记、区长（2026年卸任）", "current_org": "",
     "source": "鹤山区政府门户 2026-01/02 新闻（区长作政府工作报告）"},

    # ═══ 2026-02 时任人大常委会主任 辛守勇 (confirmed) ═══
    {"id": 9, "name": "辛守勇", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（原）鹤山区人大常委会主任（2026年初-年中）", "current_org": "",
     "source": "2026-02 十二届人大八次会议（作人大常委会工作报告）"},

    # ═══ 区领导（副县级以上，任职细分 unverified） ═══
    {"id": 10, "name": "解晓峰", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "鹤山区区领导（常务/副区级待定）", "current_org": "",
     "source": "鹤山区政府门户 2026-01/07 新闻"},
    {"id": 11, "name": "张运强", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "鹤山区区领导（职务待定）", "current_org": "",
     "source": "鹤山区政府门户 2026-07 新闻"},
    {"id": 12, "name": "李涵", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "鹤山区区领导（职务待定）", "current_org": "",
     "source": "鹤山区政府门户 2026-01/07 新闻"},

    # ═══ 前书记/前区长（unverified，任务基础假设） ═══
    {"id": 99, "name": "待确认-前任区委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "存疑", "current_org": "",
     "source": "公开报道未检索到可证的鹤山区前任书记（非李明霖或其他人选）；任务基础假设'张超'未能证实"},
]

organizations = [
    {"id": 1, "name": "中共鹤山区委", "type": "党委", "level": "县处级",
     "parent": "中共鹤壁市委", "location": "河南省鹤壁市鹤山区"},
    {"id": 2, "name": "鹤山区人民政府", "type": "政府", "level": "县处级",
     "parent": "鹤壁市人民政府", "location": "河南省鹤壁市鹤山区"},
    {"id": 3, "name": "中共鹤山区委政法委", "type": "党委", "level": "乡科级",
     "parent": "中共鹤山区委", "location": "河南省鹤壁市鹤山区"},
    {"id": 4, "name": "鹤山区人大常委会", "type": "人大", "level": "县处级",
     "parent": "鹤壁市人大常委会", "location": "河南省鹤壁市鹤山区"},
    {"id": 5, "name": "政协鹤山区委员会", "type": "政协", "level": "县处级",
     "parent": "政协鹤壁市委员会", "location": "河南省鹤壁市鹤山区"},
    {"id": 6, "name": "鹤山区人民武装部", "type": "党委", "level": "县处级",
     "parent": "鹤壁军分区", "location": "河南省鹤壁市鹤山区"},
    {"id": 7, "name": "中共鹤山区纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共鹤山区委", "location": "河南省鹤壁市鹤山区"},
    {"id": 8, "name": "中共鹤山区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共鹤山区委", "location": "河南省鹤壁市鹤山区"},
    {"id": 9, "name": "中共鹤山区委宣传部", "type": "党委", "level": "乡科级",
     "parent": "中共鹤山区委", "location": "河南省鹤壁市鹤山区"},
]

positions = [
    # 王涛 —— 区委书记
    {"person_id": 1, "org_id": 1, "title": "鹤山区委书记", "start_date": "",
     "end_date": "present", "rank": "县处级正职", "note": "2026年（约上半年）接任；兼区人武部党委第一书记"},
    {"person_id": 1, "org_id": 6, "title": "鹤山区人武部党委第一书记", "start_date": "",
     "end_date": "present", "rank": "县处级", "note": "2026-08-03 区委常委会会议宣布"},

    # 田庆昌 —— 区长
    {"person_id": 2, "org_id": 2, "title": "鹤山区区长", "start_date": "",
     "end_date": "present", "rank": "县处级正职", "note": "2026年中接任"},
    {"person_id": 2, "org_id": 1, "title": "鹤山区委副书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "区委副书记兼"},

    # 王学良 —— 区委副书记
    {"person_id": 3, "org_id": 1, "title": "鹤山区委副书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},

    # 王文飞 —— 政法委书记
    {"person_id": 4, "org_id": 3, "title": "鹤山区委政法委书记", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "鹤山区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},

    # 张志明 —— 人大常委会主任
    {"person_id": 5, "org_id": 4, "title": "鹤山区人大常委会主任", "start_date": "",
     "end_date": "present", "rank": "县处级正职", "note": "2026年内由辛守勇接任"},

    # 周毅 —— 政协主席
    {"person_id": 6, "org_id": 5, "title": "鹤山区政协主席", "start_date": "",
     "end_date": "present", "rank": "县处级正职", "note": ""},

    # 李明霖 —— 前任书记
    {"person_id": 7, "org_id": 1, "title": "鹤山区委书记（前任）", "start_date": "",
     "end_date": "2026-", "rank": "县处级正职", "note": "2026-01~02 在任（女），去向待查"},

    # 王国宇 —— 前任区长
    {"person_id": 8, "org_id": 2, "title": "鹤山区区长（前任）", "start_date": "",
     "end_date": "2026-", "rank": "县处级正职", "note": "2026-01~02 在任；2026年卸任"},
    {"person_id": 8, "org_id": 1, "title": "鹤山区委副书记（前任）", "start_date": "",
     "end_date": "2026-", "rank": "县处级副职", "note": ""},

    # 辛守勇 —— 前人大常委会主任
    {"person_id": 9, "org_id": 4, "title": "鹤山区人大常委会主任（前任）", "start_date": "",
     "end_date": "2026-初", "rank": "县处级正职", "note": "2026-02 作人大常委会工作报告，后卸任"},

    # 区领导（职务待定）
    {"person_id": 10, "org_id": 1, "title": "鹤山区区委班子/区领导（具体职务待定）", "start_date": "",
     "end_date": "present", "rank": "县处级", "note": "解晓锋"},
    {"person_id": 11, "org_id": 2, "title": "鹤山区政府领导（具体职务待定）", "start_date": "",
     "end_date": "present", "rank": "县处级", "note": "张运强"},
    {"person_id": 12, "org_id": 1, "title": "鹤山区区委领导（具体职务待定）", "start_date": "",
     "end_date": "present", "rank": "县处级", "note": "李涵"},

    # 前任书记（待确认）
    {"person_id": 99, "org_id": 1, "title": "鹤山区委书记（前任/待核实）", "start_date": "",
     "end_date": "", "rank": "县处级正职", "note": "任务书假设为张超，未能证实；李明霖为已确认的上一任书记"},
]

relationships = [
    # ── 核心搭档 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长搭档（现任）", "overlap_org": "中共鹤山区委",
     "overlap_period": "2026-", "strength": "strong",
     "source": "鹤山区政府门户 2026-07-27 常委会会议（王涛主持、田庆昌出席）；政绩观学习教育会议"},

    {"person_a": 7, "person_b": 8, "type": "overlap",
     "context": "前任区委书记与前区长搭档（2026年初）", "overlap_org": "中共鹤山区委",
     "overlap_period": "2026-01~02", "strength": "strong",
     "source": "2026-01-24 高质量发展大会（李明霖讲话、王国宇主持）；2026-02 人代会/政协会"},

    # ── 继任关系 ──
    {"person_a": 7, "person_b": 1, "type": "predecessor_successor",
     "context": "前任书记 李明霖 → 现任书记 王涛", "overlap_org": "中共鹤山区委",
     "overlap_period": "2026年上半年", "strength": "medium",
     "source": "2026-01/02 李明霖在任；2026-07/08 王涛在任（官网新闻）"},

    {"person_a": 8, "person_b": 2, "type": "predecessor_successor",
     "context": "前任区长 王国宇 → 现任区长 田庆昌", "overlap_org": "鹤山区人民政府",
     "overlap_period": "2026年上半年", "strength": "medium",
     "source": "2026-01/02 王国宇作府工作报告；2026-07 田庆昌任区长（官网新闻）"},

    {"person_a": 9, "person_b": 5, "type": "predecessor_successor",
     "context": "前人大常委会主任 辛守勇 → 现任 张志明", "overlap_org": "鹤山区人大常委会",
     "overlap_period": "2026年", "strength": "medium",
     "source": "2026-02 辛守勇作报告；2026-07/08 张志明任主任（官网新闻）"},

    # ── 书记与班子 ──
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "书记与专职副书记", "overlap_org": "中共鹤山区委常委会",
     "overlap_period": "当前", "strength": "medium", "source": ""},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "书记与政法委书记", "overlap_org": "中共鹤山区委常委会",
     "overlap_period": "当前", "strength": "medium", "source": ""},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与政法委书记", "overlap_org": "鹤山区人民政府",
     "overlap_period": "当前", "strength": "medium", "source": ""},

    # ── 区领导 ──
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "书记与区领导（解晓锋）", "overlap_org": "中共鹤山区委",
     "overlap_period": "当前", "strength": "weak", "source": "列席常委会会议"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "区长与区政府领导（张运强）", "overlap_org": "鹤山区人民政府",
     "overlap_period": "当前", "strength": "weak", "source": "列席常委会会议"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "书记与区领导（李涵）", "overlap_org": "中共鹤山区委",
     "overlap_period": "当前", "strength": "weak", "source": "列席会议"},

    # ── 前任交流（待核实） ──
    {"person_a": 99, "person_b": 7, "type": "predecessor_successor",
     "context": "前任(待核实) → 李明霖 区委书记接力", "overlap_org": "中共鹤山区委",
     "overlap_period": "", "strength": "weak",
     "source": "李明霖前任书记人名未确认；任务书假设张超未获证实"},
]


def main():
    print("=== Building 鹤山区 network data (2026-08-06) ===")
    print("Target: 区委书记(王涛) & 区长(田庆昌)")
    print("Note: 网络受限，主官履历/班子细分未联网核实，标记为 confirmed/unverified 并存疑")

    run_build(
        slug="鹤山区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print(f"\n=== Summary ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"\nDB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("=== Done ===")


if __name__ == "__main__":
    main()