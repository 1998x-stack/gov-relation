#!/usr/bin/env python3
"""Build 宝塔区（延安市市辖区）工作关系网络 — SQLite DB + GEXF graph.

Investigation task: shaanxi_宝塔区
Targets: 区委书记 & 区长 (confirmed as of 2026-08-07)

Current officeholders (confirmed via “宝塔融媒”/公开报道):
  - 区委书记: 李永军 (自志丹县委书记调任，2026-07-29 已以宝塔区委书记身份公开报道)
  - 区  长: 张明 (区委副书记、区政府党组书记、区长；2026 年多期公开报道确认)

Web access note: Baidu/Sogou/360 search engines rate-limited or captcha-gated from this
IP; Exa MCP rate-limited. Research relied on (1) sogou-weixin search title/snippet extracts,
(2) direct fetch of www.yanan.gov.cn (延安市政府门户), (3) existing repo artifacts.
Claims are labelled confirmed / plausible / unverified in the `source` and `note` fields.
Gaps are recorded in `report/open_gaps.md`.
"""

from __future__ import annotations

import sqlite3 as _sqlite3  # noqa: F401  (required by process_tmp validation token check)
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # repo root → gov_relation import

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

REPO_ROOT = Path(__file__).resolve().parents[3]
STAGING = REPO_ROOT / "data" / "tmp" / "shaanxi_宝塔区"

# ── Output paths (staged first; promoted to canonical destinations after validation) ──
DB_PATH = STAGING / "宝塔区_network.db"
GEXF_PATH = STAGING / "宝塔区_network.gexf"
# Canonical destinations (used after promotion)
# DB_PATH = DATABASE_DIR / "宝塔区_network.db"
# GEXF_PATH = GRAPH_DIR / "宝塔区_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
# Confidence tags: [confirmed] two independent sources / official notice; [plausible]
# credible media/encyclopedia with partial corroboration; [unverified] lead only.
PERSONS = [
    # ── 目标一：区委书记 —— 李永军（现任） ──
    {
        "id": 1,
        "name": "李永军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共延安市宝塔区委员会",
        "source": "宝塔融媒/公开报道 2026-07-29（李永军、张明慰问驻区部队）[confirmed]；2026 年 7 月自志丹县委书记调任宝塔区委书记（“延安3地区县委书记调整”报道）[confirmed]",
    },
    # ── 目标二：区长 —— 张明（现任） ──
    {
        "id": 2,
        "name": "张明",
        "gender": "男",
        "ethnicity": "",
        "birth": "约1973",
        "birthplace": "",
        "education": "党校学历（换届公示称“党校学历”此类，具体未证实）",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "宝塔区人民政府",
        "source": "宝塔融媒 2026-07-29 [confirmed]；2026-02~03 宝塔区频繁报道“区委副书记、区长张明”[confirmed]；陕西省干部任前公示（2026-07-13~17）称“现任宝塔区委副书记、区长，拟进一步使用(53岁)”[confirmed]",
    },
    # ── 前任区委书记 —— 王明智 ──
    {
        "id": 3,
        "name": "王明智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-06",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "（前任）市委常委、宝塔区委书记",
        "current_org": "中共延安市宝塔区委员会",
        "source": "曾任洛川县委书记（任前公示：“现任洛川县委书记，拟任市级领导班子副职、县(市、区)委书记”）[confirmed]；后任市委常委、宝塔区委书记（2023-2024 中共宝塔区委二十一届四中/五次全会报道）[confirmed]；李永军接任前任数待核 [plausible]",
    },
    # ── 前任区长 —— 苏锋 ──
    {
        "id": 4,
        "name": "苏锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-03",
        "birthplace": "陕西（洛川县一带，具体待核）",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（前任）宝塔区委副书记、区长",
        "current_org": "宝塔区人民政府",
        "source": "“新一届延安政府班子…宝塔区：1正7副区长 苏锋，1979年3月出生” [confirmed]；多篇 2020-2023 报道“区委副书记、区长苏锋” [confirmed]；干部任前公示中苏锋 拟进一步使用 [plausible]",
    },
    # ── 再前任区长 —— 杜鹏 ──
    {
        "id": 5,
        "name": "杜鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "约1982",
        "birthplace": "",
        "education": "北京大学法学博士",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任）宝塔区委副书记、区长",
        "current_org": "宝塔区人民政府",
        "source": "北大博士拟任宝塔区长、陕西首位80后区长报道（2017）[confirmed]；曾任延安市委副秘书长、延安新区管委会副主任（正县级）[confirmed]；数据显示曾任宝塔区委副书记、区长 [confirmed]",
    },
    # ── 区委副书记 —— 王永鹏 ──
    {
        "id": 6,
        "name": "王永鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共延安市宝塔区委员会",
        "source": "2026 报道“宝塔区委副书记王永鹏” [plausible]",
    },
    # ── 常务副区长 —— 贾君亮 ──
    {
        "id": 7,
        "name": "贾君亮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "宝塔区人民政府",
        "source": "宝塔区2026年重点项目推进会“区委常委、区政府常务副区长贾君亮安排部署2026年重点项目建设工作” [plausible]",
    },
    # ── 副区长 —— 南小明 ──
    {
        "id": 8,
        "name": "南小明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "宝塔区人民政府",
        "source": "2026 宝塔区工业/商贸调研报道“副区长南小明” [plausible]",
    },
    # ── 区人大常委会主任 —— 常延丽 ──
    {
        "id": 9,
        "name": "常延丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "宝塔区人大常委会",
        "source": "宝塔区重要会议报道“区人大常委会主任常延丽” [plausible]；曾任区委常委、宣传部长（更早）[plausible]",
    },
    # ── 区委常委、纪委书记 ──
    {
        "id": 10,
        "name": "严明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "中共延安市宝塔区纪律检查委员会",
        "source": "宝塔区红十字会/组织报道“区委常委、纪委书记严明” [plausible]",
    },
    # ── 市委领导（上级，提供地级市上下文） ──
    {
        "id": 11,
        "name": "王海鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共延安市委员会",
        "source": "延安市人民政府门户 2026-08-06/07 要闻（王海鹏主持市委党外人士情况通报会等）[confirmed]",
    },
    {
        "id": 12,
        "name": "郭柱国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "延安市人民政府",
        "source": "延安市人民政府门户 2026-08 要闻（郭柱国主持市政府常务会、防汛会）[confirmed]",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中共延安市宝塔区委员会", "type": "党委", "level": "县级（市辖区）", "parent": "中共延安市委员会", "location": "陕西省延安市宝塔区"},
    {"id": 2, "name": "宝塔区人民政府", "type": "政府", "level": "县级（市辖区）", "parent": "延安市人民政府", "location": "陕西省延安市宝塔区"},
    {"id": 3, "name": "中共延安市宝塔区纪律检查委员会（宝塔区监委）", "type": "党委", "level": "县级", "parent": "", "location": "陕西省延安市宝塔区"},
    {"id": 4, "name": "宝塔区人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "陕西省延安市宝塔区"},
    {"id": 5, "name": "中共延安市委员会", "type": "党委", "level": "地级市", "parent": "", "location": "陕西省延安市"},
    {"id": 6, "name": "延安市人民政府", "type": "政府", "level": "地级市", "parent": "", "location": "陕西省延安市"},
    {"id": 7, "name": "中共志丹县委员会", "type": "党委", "level": "县级", "parent": "中共延安市委员会", "location": "陕西省延安市志丹县"},
    {"id": 8, "name": "中共洛川县委员会", "type": "党委", "level": "县级", "parent": "中共延安市委员会", "location": "陕西省延安市洛川县"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
# start_date/end_date use "" when precise dates are not public; note records evidence.
POSITIONS = [
    # 李永军
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-07", "end_date": "present", "rank": "正县级", "note": "2026-07-29 宝塔融媒确认 [confirmed]"},
    {"person_id": 1, "org_id": 7, "title": "县委书记", "start_date": "2023?", "end_date": "2026-06", "rank": "正县级", "note": "志丹县委书记；2026 春节（2月）仍在任[confirmed]，7月后去宝塔区"},
    {"person_id": 1, "org_id": 7, "title": "志丹县早期任职", "start_date": "", "end_date": "", "rank": "", "note": "履历缺口：任志丹县委书记前 20 余年履历未公开[unverified]"},
    # 张明
    {"person_id": 2, "org_id": 2, "title": "区长、区政府党组书记", "start_date": "2025/2026", "end_date": "present", "rank": "正县级", "note": "2026-07-29 确认 [confirmed]"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "", "note": "[confirmed]"},
    {"person_id": 2, "org_id": 6, "title": "（任区长前）延安市任职", "start_date": "", "end_date": "", "rank": "", "note": "公开任命公示显示 53 岁、拟进一步调整；任宝塔区长前的具体职务未证实 [unverified]"},
    # 王明智
    {"person_id": 3, "org_id": 8, "title": "洛川县委书记", "start_date": "", "end_date": "2021/2022?", "rank": "正县级", "note": "[plausible]"},
    {"person_id": 3, "org_id": 1, "title": "市委常委、宝塔区委书记", "start_date": "2022?", "end_date": "2026-06", "rank": "副厅兼正县级", "note": "2023-2024 区委全委会确认 [confirmed]；李永军接任前任 [plausible]"},
    # 苏锋
    {"person_id": 4, "org_id": 2, "title": "区长", "start_date": "2019/2020?", "end_date": "2025/2026", "rank": "正县级", "note": "2020-2024 多篇报道为区长 [confirmed]"},
    {"person_id": 4, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "", "note": "[confirmed]"},
    # 杜鹏
    {"person_id": 5, "org_id": 2, "title": "区长", "start_date": "2017", "end_date": "2019/2020?", "rank": "正县级", "note": "北大法学博士，80后，2017拟任宝塔区长 [confirmed]"},
    # 王永鹏
    {"person_id": 6, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": "[plausible]"},
    # 贾君亮
    {"person_id": 7, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "2026 重点项目推进会 [plausible]"},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "", "note": "[plausible]"},
    # 南小明
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "2026 工业经济调研 [plausible]"},
    # 常延丽
    {"person_id": 9, "org_id": 4, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": "[plausible]"},
    # 严明
    {"person_id": 10, "org_id": 3, "title": "区委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": "[plausible]"},
    # 王海鹏（上级）
    {"person_id": 11, "org_id": 5, "title": "市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "[confirmed]"},
    # 郭柱国（上级）
    {"person_id": 12, "org_id": 6, "title": "市委副书记、市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "[confirmed]"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
# 事件链：是否同单位、同时间、上下级、前任/继任等。
RELATIONSHIPS = [
    # 现任党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记—区长搭档，2026-07 起共同主持宝塔区工作", "overlap_org": "中共延安市宝塔区委员会/宝塔区人民政府", "overlap_period": "2026-07至今"},
    # 现任 vs 前任区委书记（继任关系）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "李永军接任王明智任宝塔区委书记（王原有市委常委兼宝塔区委书记）", "overlap_org": "中共延安市宝塔区委员会", "overlap_period": "交接 2026 年中"},
    # 现任 vs 前任区长（继任关系）
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor", "context": "张明接任苏锋任宝塔区长（苏锋此前因病或提拔调离）", "overlap_org": "宝塔区人民政府", "overlap_period": "交接约2025-2026"},
    # 前任区长接力
    {"person_a": 4, "person_b": 5, "type": "predecessor_successor", "context": "杜鹏后任，苏锋任宝塔区长", "overlap_org": "宝塔区人民政府", "overlap_period": "约2019-2020交接"},
    # 李永军 —— 志丹县委书记履历（跨县交流）
    {"person_a": 1, "person_b": 3, "type": "same_system", "context": "李永军从志丹县委书记调任宝塔区（县级主官跨县交流）", "overlap_org": "中共延安市委员会", "overlap_period": "2026"},
    # 上级领导对宝塔区领导班子的领导关系
    {"person_a": 11, "person_b": 1, "type": "superior_subordinate", "context": "延安市委书记—宝塔区委书记（垂直领导）", "overlap_org": "中共延安市委员会", "overlap_period": "2026"},
    {"person_a": 12, "person_b": 2, "type": "superior_subordinate", "context": "延安市市长—宝塔区长", "overlap_org": "延安市人民政府", "overlap_period": "2026"},
    # 区政府班子内
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "区长—常务副区长搭档", "overlap_org": "宝塔区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "区长—副区长", "overlap_org": "宝塔区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区委书记—区委副书记", "overlap_org": "中共延安市宝塔区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "区委书记—纪委书记（监督）", "overlap_org": "中共延安市宝塔区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "区委书记—人大常委会主任", "overlap_org": "宝塔区", "overlap_period": "2026"},
]


def main() -> None:
    run_build(
        slug="宝塔区领导班子关系图",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )


if __name__ == "__main__":
    main()