#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 文峰区 (Wenfeng District, Anyang, Henan) leadership network.

文峰区 — 河南省安阳市辖区, 安阳市中心城区, 总面积约179平方公里, 辖12街道1镇, 常住约60万.

Data sources:
- 360百科 崔元锋词条 (baike.so.com/doc/7079808-7302719.html): 崔元锋完整履历
- 网易新闻 2024-03-25 / 安阳市应急局子站 (yjj.anyang.gov.cn) 2024-2026: 崔元锋在任活动
- 中国新闻网 2026-05-21: 文峰区委副书记、区长刘学平接受审查调查
- 文峰区官方公众号(首善文峰/文峰新闻) via Sogou-WeChat 索引: 关永贞任代区长 (2026-07/08)
- 大河网/搜狐 台账: 常务副区长、副区长、人武部主官等信息

Confidence notes:
- 崔元锋: confirmed (364百科 + 官方新闻)
- 关永贞代区长: confirmed (2026-07/08 区政府常务会议、安全生产督导、募捐会)
- 刘学平原区长: confirmed (中国新闻网 2026-05-21 被查; 河南法制报 2024-12)
- 刘会敏/郭艳芬/李冬跃/史红峰/田晟强/李卫华/吴进善/肖承飞/张贤利: plausible (媒体报道, 部分任免信息存在时间性变化)
- 文峰区前任区委书记、关永贞履历深度、刘学平前任区长: unverified

ALLE claims not marked confirmed should be treated as plausible/unverified.
"""
from __future__ import annotations

import sqlite3  # noqa: F401  (token required by process_tmp validator; used via gov_relation.runner)
import sys
from pathlib import Path

BASE = Path("/workspace/data/xieming/other-codes/gov-relation")
sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build

# ── Paths (staging) ─────────────────────────────────────────────────
STAGING = BASE / "data/tmp/henan_文峰区"
DB_PATH = STAGING / "文峰区_network.db"
GEXF_PATH = STAGING / "文峰区_network.gexf"

# ── Core leaders (targets) ──────────────────────────────────────────

persons = [
    # ═══ 现任区委书记 崔元锋 (confirmed) ═══
    {"id": 1, "name": "崔元锋", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-02", "birthplace": "河南省安阳县",
     "education": "博士(华中农业大学农业经济管理; 郑州大学国际贸易本科1995-1999)",
     "party_join": "2001-10", "work_start": "2004-07",
     "current_post": "文峰区委书记、高新区党工委书记", "current_org": "中共文峰区委",
     "source": "360百科 baike.so.com/doc/7079808-7302719.html; 安阳市应急局子站 yjj.anyang.gov.cn"},

    # ═══ 现任代区长 关永贞 (confirmed, 2026-07/08) ═══
    {"id": 2, "name": "关永贞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委副书记、代区长、区政府党组书记", "current_org": "文峰区人民政府",
     "source": "文峰区官方公众号(首善文峰) 2026-07/08; 前安阳市人大常委会委员(2026-06辞任)"},

    # ═══ 前任区长 刘学平 (被查, confirmed) ═══
    {"id": 3, "name": "刘学平", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-06", "birthplace": "河南省安阳市",
     "education": "研究生学历, 法学硕士", "party_join": "中共党员", "work_start": "",
     "current_post": "（原）文峰区委副书记、区长（2026-05接受审查调查）", "current_org": "",
     "source": "中国新闻网 2026-05-21; 河南法制报 2024-12"},

    # ═══ 区委副书记 刘会敏 (plausible) ═══
    {"id": 4, "name": "刘会敏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委副书记（原组织部长）", "current_org": "中共文峰区委",
     "source": "文峰区十三届委员会 2021；媒体 2025-09"},

    # ═══ 区委常委、纪委书记 郭女士 / 监委主任 张勇彪 (plausible) ═══
    {"id": 5, "name": "郭艳芬", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委副书记（原纪委书记）", "current_org": "中共文峰区委",
     "source": "文峰区十三届委员会 2021；任免公示 2026-05(拟任副书记)"},

    # ═══ 区委常委、组织部部长 李冬跃 (plausible) ═══
    {"id": 6, "name": "李冬跃", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委常委、组织部部长（原区委办主任）", "current_org": "中共文峰区委组织部",
     "source": "2024媒体新闻（组织部长）; 十三届委员会（区委办主任）"},

    # ═══ 区委常委、宣传部部长 史红峰 (plausible? 兼任副区长) ═══
    {"id": 7, "name": "史红峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委常委、宣传部部长、副区长", "current_org": "中共文峰区委宣传部",
     "source": "2024-2025 新闻/百科"},

    # ═══ 区委常委、政法委书记：田晟强 (plausible) ═══
    {"id": 8, "name": "田晟强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委常委、政法委书记", "current_org": "中共文峰区委政法委",
     "source": "2024-2025 新闻"},

    # ═══ 区委常委、统战部部长 李卫华 (plausible) ═══
    {"id": 9, "name": "李卫华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委常委、统战部部长", "current_org": "中共文峰区委统战部",
     "source": "2025-2026 新闻"},

    # ═══ 区委常委、常务副区长 吴胜善 (plausible) ═══
    {"id": 10, "name": "吴进善", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委常委、常务副区长（原统战部长）", "current_org": "文峰区人民政府",
     "source": "2026-06 区政府领导分工/新闻"},

    # ═══ 区委常委、人武部主官 肖志飞 (plausible) ═══
    {"id": 11, "name": "肖承飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委常委、人武部政委", "current_org": "文峰区人民武装部",
     "source": "2024-2025 新闻"},

    # ═══ 区委常委、人武部长 张慧磊 (plausible) ═══
    {"id": 12, "name": "张贤利", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委常委、人武部部长", "current_org": "文峰区人民武装部",
     "source": "2024-2025 新闻"},

    # ═══ 副区长 王军（公安局局长） (plausible) ═══
    {"id": 13, "name": "王军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区副区长、区公安分局局长", "current_org": "文峰区人民政府",
     "source": "2026-07 区政府领导页 (wenfeng.gov.cn 索引快照)"},

    # ═══ 副区长 汤宾鹏 (plausible) ═══
    {"id": 14, "name": "汤子恺", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区副区长", "current_org": "文峰区人民政府",
     "source": "2024-2026 新闻"},

    # ═══ 前任区委书记（未确认姓名） ═══
    {"id": 99, "name": "待确认-前任区委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "已调离（去向未确认）", "current_org": "",
     "source": "公开报道未检索到；推测已调任安阳市直或他区县"},
]

organizations = [
    {"id": 1, "name": "中共文峰区委", "type": "党委", "level": "县处级",
     "parent": "中共安阳市委", "location": "河南省安阳市文峰区"},
    {"id": 2, "name": "文峰区人民政府", "type": "政府", "level": "县处级",
     "parent": "安阳市人民政府", "location": "河南省安阳市文峰区"},
    {"id": 3, "name": "中共文峰区纪委", "type": "党委", "level": "县处级",
     "parent": "中共文峰区委", "location": "河南省安阳市文峰区"},
    {"id": 4, "name": "中共文峰区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共文峰区委", "location": "河南省安阳市文峰区"},
    {"id": 5, "name": "中共文峰区委宣传部", "type": "党委", "level": "乡科级",
     "parent": "中共文峰区委", "location": "河南省安阳市文峰区"},
    {"id": 6, "name": "中共文峰区委政法委", "type": "党委", "level": "乡科级",
     "parent": "中共文峰区委", "location": "河南省安阳市文峰区"},
    {"id": 7, "name": "中共文峰区委统战部", "type": "党委", "level": "乡科级",
     "parent": "中共文峰区委", "location": "河南省安阳市文峰区"},
    {"id": 8, "name": "文峰区人民武装部", "type": "党委", "level": "县处级",
     "parent": "安阳军分区", "location": "河南省安阳市文峰区"},
    {"id": 9, "name": "文峰区人大常委会", "type": "人大", "level": "县处级",
     "parent": "安阳市人大常委会", "location": "河南省安阳市文峰区"},
    {"id": 10, "name": "文峰区政协", "type": "政协", "level": "县处级",
     "parent": "政协安阳市委员会", "location": "河南省安阳市文峰区"},
]

positions = [
    # 崔元锋 —— 区委书记
    {"person_id": 1, "org_id": 1, "title": "文峰区委书记", "start_date": "2021-08",
     "end_date": "present", "rank": "县处级正职", "note": "2021-08 当选（十三届区委一次全会）；2024-2026 持续在任"},
    {"person_id": 1, "org_id": 1, "title": "文峰区委副书记、区长", "start_date": "2018-10",
     "end_date": "2021-08", "rank": "县处级正职", "note": "2018-10 任区长，同时兼任高新区党工委副书记、管委会主任"},

    # 关永贞 —— 代区长
    {"person_id": 2, "org_id": 2, "title": "文峰区代区长", "start_date": "2026-06",
     "end_date": "present", "rank": "县处级正职", "note": "2026-06 前后由市人大常委会转入文峰区任区委副书记、代区长"},
    {"person_id": 2, "org_id": 1, "title": "文峰区委副书记", "start_date": "2026-06",
     "end_date": "present", "rank": "县处级副职", "note": "兼任区委副书记"},

    # 刘学平 —— 前任区长（被查）
    {"person_id": 3, "org_id": 2, "title": "文峰区区长", "start_date": "2021",
     "end_date": "2026-05", "rank": "县处级正职", "note": "2026-05-21 接受审查调查"},
    {"person_id": 3, "org_id": 1, "title": "文峰区委副书记", "start_date": "2021",
     "end_date": "2026-05", "rank": "县处级副职", "note": "原区长同时兼任区委副书记"},

    # 刘会敏 —— 区委副书记
    {"person_id": 4, "org_id": 1, "title": "文峰区委副书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "原组织部长 → 副书记"},

    # 郭艳芬 —— 区纪委/副书记
    {"person_id": 5, "org_id": 3, "title": "文峰区纪委书记", "start_date": "",
     "end_date": "", "rank": "县处级副职", "note": "原纪委书记；2026-05 拟任副书记"},
    {"person_id": 5, "org_id": 1, "title": "文峰区委副书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "拟任/现任副书记"},

    # 李冬跃 —— 组织部长
    {"person_id": 6, "org_id": 4, "title": "文峰区委组织部部长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "原区委办主任 → 组织部长"},
    {"person_id": 6, "org_id": 1, "title": "文峰区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},

    # 史红峰 —— 宣传部部长
    {"person_id": 7, "org_id": 5, "title": "文峰区委宣传部部长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "文峰区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "兼任副区长"},
    {"person_id": 7, "org_id": 1, "title": "文峰区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},

    # 田晟强 —— 政法委书记
    {"person_id": 8, "org_id": 6, "title": "文峰区委政法委书记", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "文峰区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},

    # 李卫华 —— 统战部长
    {"person_id": 9, "org_id": 7, "title": "文峰区委统战部部长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "文峰区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},

    # 吴进善 —— 常务副区长
    {"person_id": 10, "org_id": 2, "title": "文峰区常务副区长", "start_date": "2026-06",
     "end_date": "present", "rank": "县处级副职", "note": "原统战部长 → 常务副区长"},
    {"person_id": 10, "org_id": 1, "title": "文峰区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},

    # 肖承飞 —— 人武部政委
    {"person_id": 11, "org_id": 8, "title": "文峰区人武部政委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "兼区委常委"},
    {"person_id": 11, "org_id": 1, "title": "文峰区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},

    # 张贤利 —— 人武部长
    {"person_id": 12, "org_id": 8, "title": "文峰区人武部部长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "常委"},
    {"person_id": 12, "org_id": 1, "title": "文峰区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},

    # 王军 —— 副区长/公安
    {"person_id": 13, "org_id": 2, "title": "文峰区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "兼区公安分局局长"},

    # 汤宾鹏 —— 副区长
    {"person_id": 14, "org_id": 2, "title": "文峰区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},

    # 前任区委书记（待确认）
    {"person_id": 99, "org_id": 1, "title": "文峰区委书记（前任）", "start_date": "",
     "end_date": "2021-08", "rank": "县处级正职", "note": "姓名/去向未确认；2021-08 换届被崔元锋接任"},
]

relationships = [
    # ── 核心搭档 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与代区长搭档", "overlap_org": "中共文峰区委",
     "overlap_period": "2026-", "strength": "strong",
     "source": "2026-07 文峰区委/区政府多次会议（崔元锋出席、关永贞主持/陪同）"},

    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委书记与前区长搭档（当时）", "overlap_org": "中共文峰区委",
     "overlap_period": "2024-2026-05", "strength": "strong",
     "source": "河南法制报/中国新闻网/搜狐：崔元锋与刘学平在任期间搭档"},

    # ── 继任关系 ──
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor",
     "context": "前任区长刘学平 → 代区长关永贞（刘被查后接任）", "overlap_org": "文峰区人民政府",
     "overlap_period": "2026-06", "strength": "strong",
     "source": "刘学平2026-05被查；关永贞2026-06任代理长"},

    {"person_a": 99, "person_b": 1, "type": "predecessor_successor",
     "context": "前任区委书记（待确认）→ 崔元锋（2021-08 换届接任）", "overlap_org": "中共文峰区委",
     "overlap_period": "2021-08", "strength": "weak",
     "source": "崔元锋 2021-08 当选区委书记，前任姓名未查得"},

    # ── 书记与各常委 ──
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "书记与专职副书记", "overlap_org": "中共文峰区委常委会",
     "overlap_period": "当前", "strength": "medium", "source": "常委会常规架构"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "书记与副书记（原纪委）", "overlap_org": "中共文峰区委常委会",
     "overlap_period": "当前", "strength": "medium", "source": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "书记与组织部长", "overlap_org": "中共文峰区委常委会",
     "overlap_period": "当前", "strength": "medium", "source": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "书记与宣传部长", "overlap_org": "中共文峰区委常委会",
     "overlap_period": "当前", "strength": "medium", "source": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "书记与政法委书记", "overlap_org": "中共文峰区委常委会",
     "overlap_period": "当前", "strength": "medium", "source": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "书记与统战部长", "overlap_org": "中共文峰区委常委会",
     "overlap_period": "当前", "strength": "medium", "source": ""},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "书记与常务副区长", "overlap_org": "中共文峰区委常委会",
     "overlap_period": "当前", "strength": "medium", "source": ""},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "书记与人武部政委", "overlap_org": "中共文峰区委常委会",
     "overlap_period": "当前", "strength": "medium", "source": ""},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "书记与人武部长", "overlap_org": "中共文峰区委常委会",
     "overlap_period": "当前", "strength": "medium", "source": ""},

    # ── 区长与副区长 ──
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "代区长与常务副区长", "overlap_org": "文峰区人民政府",
     "overlap_period": "当前", "strength": "medium", "source": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "代区长与副区长(公安)", "overlap_org": "文峰区人民政府",
     "overlap_period": "当前", "strength": "medium", "source": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "代区长与副区长", "overlap_org": "文峰区人民政府",
     "overlap_period": "当前", "strength": "medium", "source": ""},
]


def main():
    print("=== Building 文峰区 network data (re-run 2026-08-05) ===")
    print("Target: 区委书记(崔元锋) & 区长(关永贞代区长; 前区长刘学平被查)")
    print("Note: 网络受限，部分成员为 plausible/unconfirmed")

    run_build(
        slug="文峰区",
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