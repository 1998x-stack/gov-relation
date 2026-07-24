#!/usr/bin/env python3
"""Build 顺平县 leadership network: SQLite DB + GEXF graph.

Research date: 2026-07-24
Task ID: hebei_顺平县
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure gov_relation is importable
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug ─────────────────────────────────────────────────────────────────
SLUG = "顺平县"
TASK_DIR = Path(__file__).parent.resolve()

# ── Persons ──────────────────────────────────────────────────────────────
# ID mapping: 1-99 for persons, 100+ for organizations

persons = [
    # === Core leaders ===
    {
        "id": 1,
        "name": "吴鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "湖南省衡阳市",
        "education": "湘潭大学建筑工程专业本科；东南大学防灾减灾工程及防护工程博士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共顺平县委",
        "source": "https://www.163.com/dy/article/JIO4K2PS0525EN38.html",
    },
    {
        "id": 2,
        "name": "刘玉辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县长（已调任满城区委书记）",
        "current_org": "顺平县人民政府（已离任）",
        "source": "https://www.hbxyjjw.com/rsrm/5451.html; https://heb.hebccw.cn/system/2021/06/04/100685288.shtml",
    },
    {
        "id": 3,
        "name": "陈志强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县委书记（2021.5-2024.11）",
        "current_org": "中共顺平县委（已离任）",
        "source": "https://m.thepaper.cn/baijiahao_12742962; https://www.163.com/dy/article/GFLP9P9O0524CFN0.html",
    },
    {
        "id": 4,
        "name": "单有高",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县委书记（2021年前）",
        "current_org": "中共顺平县委（已离任）",
        "source": "https://m.thepaper.cn/baijiahao_12742962",
    },
    {
        "id": 5,
        "name": "邓艳学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县长（2021.5前离任）",
        "current_org": "顺平县人民政府（已离任）",
        "source": "https://heb.hebccw.cn/system/2021/06/04/100685288.shtml",
    },
    # === Leadership roster (2025河长名单) ===
    {
        "id": 6,
        "name": "王敏",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县委副书记",
        "current_org": "中共顺平县委",
        "source": "http://shunping.gov.cn/col/1660634096582/2025/06/09/1749431967992.html",
    },
    {
        "id": 7,
        "name": "王玉新",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部长、统战部长",
        "current_org": "中共顺平县委",
        "source": "http://shunping.gov.cn/col/1660634096582/2025/06/09/1749431967992.html",
    },
    {
        "id": 8,
        "name": "祝恒",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县委办主任",
        "current_org": "中共顺平县委",
        "source": "http://shunping.gov.cn/col/1660634096582/2025/06/09/1749431967992.html",
    },
    {
        "id": 9,
        "name": "尤磊",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部长",
        "current_org": "中共顺平县委",
        "source": "http://shunping.gov.cn/col/1660634096582/2025/06/09/1749431967992.html",
    },
    {
        "id": 10,
        "name": "张要松",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、经济开发区党工委副书记、管委会常务副主任",
        "current_org": "顺平经济开发区",
        "source": "http://shunping.gov.cn/col/1660634096582/2025/06/09/1749431967992.html",
    },
    {
        "id": 11,
        "name": "张伟一",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、人武部政委",
        "current_org": "顺平县人武部",
        "source": "http://shunping.gov.cn/col/1660634096582/2025/06/09/1749431967992.html",
    },
    {
        "id": 12,
        "name": "李刚",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共顺平县委政法委",
        "source": "http://shunping.gov.cn/col/1660634096582/2025/06/09/1749431967992.html",
    },
    {
        "id": 13,
        "name": "张建龙",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "顺平县人民政府",
        "source": "http://shunping.gov.cn/col/1660634096582/2025/06/09/1749431967992.html",
    },
    {
        "id": 14,
        "name": "张新培",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "顺平县人民政府",
        "source": "http://shunping.gov.cn/col/1660634096582/2025/06/09/1749431967992.html",
    },
    {
        "id": 15,
        "name": "康建良",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长、公安局长",
        "current_org": "顺平县人民政府/县公安局",
        "source": "http://shunping.gov.cn/col/1660634096582/2025/06/09/1749431967992.html",
    },
    {
        "id": 16,
        "name": "赵昱璇",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "顺平县人民政府",
        "source": "http://shunping.gov.cn/col/1660634096582/2025/06/09/1749431967992.html",
    },
    # === 2021 era leaders (from 2021换届) ===
    {
        "id": 17,
        "name": "李素娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县委副书记（2021届）",
        "current_org": "中共顺平县委（已离任）",
        "source": "https://www.163.com/dy/article/GFLP9P9O0524CFN0.html",
    },
    {
        "id": 18,
        "name": "张天亚",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县委常委、副县长（2021届）",
        "current_org": "顺平县人民政府（已离任）",
        "source": "https://m.thepaper.cn/newsDetail_forward_13850451",
    },
    {
        "id": 19,
        "name": "汪源",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县委常委、县纪委书记、县监委主任",
        "current_org": "顺平县纪委监委",
        "source": "https://m.thepaper.cn/newsDetail_forward_13850451",
    },
    {
        "id": 20,
        "name": "侯英武",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原副县长（2021届）",
        "current_org": "顺平县人民政府（已离任）",
        "source": "https://m.thepaper.cn/newsDetail_forward_13850451",
    },
    {
        "id": 21,
        "name": "王伯健",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原副县长、公安局长（2021届）",
        "current_org": "顺平县人民政府（已离任）",
        "source": "https://m.thepaper.cn/newsDetail_forward_13850451",
    },
    {
        "id": 22,
        "name": "孙慧霄",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县委常委、政法委书记（2021届）",
        "current_org": "中共顺平县委（已离任）",
        "source": "https://m.thepaper.cn/newsDetail_forward_13850451",
    },
    # 2024-era additional names
    {
        "id": 23,
        "name": "焦文昭",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县委常委、管委会副主任（2024届）",
        "current_org": "顺平经济开发区",
        "source": "http://www.shunping.gov.cn/col/1660634096582/2024/06/12/1718158388151.html",
    },
    {
        "id": 24,
        "name": "李大伟",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县委常委、人武部部长（2024届）",
        "current_org": "顺平县人武部（已离任）",
        "source": "http://www.shunping.gov.cn/col/1660634096582/2024/06/12/1718158388151.html",
    },
    {
        "id": 25,
        "name": "常彦龙",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "顺平县人民政府",
        "source": "http://www.shunping.gov.cn/",
    },
]

# ── Organizations ────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共顺平县委", "type": "党委", "level": "县", "parent": "中共保定市委", "location": "河北省保定市顺平县"},
    {"id": 2, "name": "顺平县人民政府", "type": "政府", "level": "县", "parent": "保定市人民政府", "location": "河北省保定市顺平县"},
    {"id": 3, "name": "顺平县公安局", "type": "政府", "level": "县", "parent": "顺平县人民政府", "location": "河北省保定市顺平县"},
    {"id": 4, "name": "顺平县人武部", "type": "政府", "level": "县", "parent": "保定军分区", "location": "河北省保定市顺平县"},
    {"id": 5, "name": "顺平经济开发区", "type": "开发区", "level": "省级", "parent": "顺平县人民政府", "location": "河北省保定市顺平县"},
    {"id": 6, "name": "顺平县纪委监委", "type": "党委", "level": "县", "parent": "中共顺平县委", "location": "河北省保定市顺平县"},
    {"id": 7, "name": "中共顺平县委政法委", "type": "党委", "level": "县", "parent": "中共顺平县委", "location": "河北省保定市顺平县"},
]

# ── Positions ────────────────────────────────────────────────────────────

positions = [
    # 吴鹏
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2024-11", "end_date": "", "rank": "正处级", "note": "2024年11月任顺平县委书记"},
    # 刘玉辉
    {"person_id": 2, "org_id": 7, "title": "县委常委、政法委书记", "start_date": "", "end_date": "2021-05", "rank": "副处级", "note": "曾任顺平县委常委、政法委书记"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2021-05", "end_date": "2021-07", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "副县长、代县长", "start_date": "2021-05", "end_date": "2021-07", "rank": "正处级", "note": "2021年5月任代县长"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2021-07", "end_date": "2026-03", "rank": "正处级", "note": "2021年7月当选县长，后调任满城区委书记"},
    # 陈志强
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start_date": "2021-05", "end_date": "2024-11", "rank": "正处级", "note": "2021年5月从单有高处接任县委书记，2024年11月由吴鹏接替"},
    # 单有高
    {"person_id": 4, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "2021-05", "rank": "正处级", "note": "2021年5月离任"},
    # 邓艳学
    {"person_id": 5, "org_id": 2, "title": "县长", "start_date": "", "end_date": "2021-05", "rank": "正处级", "note": "2021年5月辞职"},
    # 王敏
    {"person_id": 6, "org_id": 1, "title": "县委常委、县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025年在任"},
    # 王玉新
    {"person_id": 7, "org_id": 1, "title": "县委常委、组织部长、统战部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025年在任"},
    # 祝恒
    {"person_id": 8, "org_id": 1, "title": "县委常委、县委办主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025年在任"},
    # 尤磊
    {"person_id": 9, "org_id": 1, "title": "县委常委、宣传部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025年在任"},
    # 张要松
    {"person_id": 10, "org_id": 5, "title": "县委常委、经济开发区党工委副书记、管委会常务副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025年在任"},
    # 张伟一
    {"person_id": 11, "org_id": 4, "title": "县委常委、人武部政委", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025年在任"},
    # 李刚
    {"person_id": 12, "org_id": 7, "title": "县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025年在任"},
    # 张建龙
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "2021-07", "end_date": "", "rank": "副处级", "note": "2021年7月当选副县长，2025年仍在任"},
    # 张新培
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "2021-07", "end_date": "", "rank": "副处级", "note": "2021年7月当选副县长，2025年仍在任"},
    # 康建良
    {"person_id": 15, "org_id": 2, "title": "副县长、公安局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025年在任"},
    {"person_id": 15, "org_id": 3, "title": "公安局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 赵昱璇
    {"person_id": 16, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025年在任"},
    # 李素娜
    {"person_id": 17, "org_id": 1, "title": "县委副书记", "start_date": "2021-07", "end_date": "", "rank": "副处级", "note": "2021年7月当选县委副书记"},
    # 张天亚
    {"person_id": 18, "org_id": 2, "title": "县委常委、副县长", "start_date": "2021-07", "end_date": "", "rank": "副处级", "note": "2021年7月当选"},
    # 汪源
    {"person_id": 19, "org_id": 6, "title": "县委常委、县纪委书记、县监委主任", "start_date": "2021-07", "end_date": "", "rank": "副处级", "note": "2021年7月当选"},
    # 侯英武
    {"person_id": 20, "org_id": 2, "title": "副县长", "start_date": "2021-07", "end_date": "", "rank": "副处级", "note": "2021年7月当选副县长"},
    # 王伯健
    {"person_id": 21, "org_id": 2, "title": "副县长、公安局长", "start_date": "2021-07", "end_date": "", "rank": "副处级", "note": "2021年7月当选副县长、公安局长"},
    {"person_id": 21, "org_id": 3, "title": "公安局长", "start_date": "2021-07", "end_date": "", "rank": "副处级", "note": ""},
    # 孙慧霄
    {"person_id": 22, "org_id": 7, "title": "县委常委、政法委书记", "start_date": "2021-07", "end_date": "", "rank": "副处级", "note": "2021年7月当选"},
    # 焦文昭
    {"person_id": 23, "org_id": 5, "title": "县委常委、管委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "2024年在任"},
    # 李大伟
    {"person_id": 24, "org_id": 4, "title": "县委常委、人武部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2024年在任"},
    # 常彦龙
    {"person_id": 25, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026年在任（顺平县政府官网县长之窗显示）"},
]

# ── Relationships ────────────────────────────────────────────────────────

relationships = [
    # 吴鹏 — 刘玉辉（书记—县长搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与县长工作搭档", "overlap_org": "顺平县", "overlap_period": "2024-11 至 2026-03"},
    # 陈志强 — 刘玉辉（书记—县长搭档）
    {"person_a": 3, "person_b": 2, "type": "overlap", "context": "县委书记与县长工作搭档", "overlap_org": "顺平县", "overlap_period": "2021-05 至 2024-11"},
    # 单有高 → 陈志强（书记交接）
    {"person_a": 4, "person_b": 3, "type": "predecessor_successor", "context": "顺平县委书记前后任", "overlap_org": "中共顺平县委", "overlap_period": "2021-05"},
    # 陈志强 → 吴鹏（书记交接）
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "顺平县委书记前后任", "overlap_org": "中共顺平县委", "overlap_period": "2024-11"},
    # 邓艳学 → 刘玉辉（县长交接）
    {"person_a": 5, "person_b": 2, "type": "predecessor_successor", "context": "顺平县县长前后任", "overlap_org": "顺平县人民政府", "overlap_period": "2021-05"},
    # 吴鹏 — 王敏（书记—副书记）
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与县委副书记", "overlap_org": "中共顺平县委", "overlap_period": "2024-11 至今"},
    # 吴鹏 — 李刚（书记—政法委书记）
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "县委书记与政法委书记", "overlap_org": "中共顺平县委", "overlap_period": "2024-11 至今"},
    # 吴鹏 — 张建龙（书记—副县长）
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "县委书记与副县长", "overlap_org": "顺平县", "overlap_period": "2024-11 至今"},
    # 陈志强 — 李素娜（书记—副书记）
    {"person_a": 3, "person_b": 17, "type": "superior_subordinate", "context": "县委书记与县委副书记", "overlap_org": "中共顺平县委", "overlap_period": "2021-05 至 2024-11"},
    # 陈志强 — 刘玉辉 — 张天亚（县委常委会）
    {"person_a": 3, "person_b": 18, "type": "overlap", "context": "县委常委会共事", "overlap_org": "中共顺平县委", "overlap_period": "2021-07 至 2024-11"},
    # 陈志强 — 汪源（书记—纪委书记）
    {"person_a": 3, "person_b": 19, "type": "superior_subordinate", "context": "县委书记与纪委书记", "overlap_org": "中共顺平县委", "overlap_period": "2021-07 至 2024-11"},
]

# ── Build ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    db_path = TASK_DIR / "顺平县_network.db"
    gexf_path = TASK_DIR / "顺平县_network.gexf"

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"\nDone. Files created:")
    print(f"  DB:   {db_path}")
    print(f"  GEXF: {gexf_path}")
