#!/usr/bin/env python3
"""内蒙古自治区省级领导班子工作关系网络生成脚本.

基于内蒙古自治区人民政府门户 (www.nmg.gov.cn) 领导简介与 2026-07-31 区党委
十一届十二次全会公报、百度百科公开人物履历、新华社职务调整新闻等，构建
内蒙古自治区党委、政府、人大、政协主要领导及前任领导的 SQLite 数据库与
GEXF 关系图。

数据时间锚点：截至 2026-08-06（模拟环境日期）
核心任职信息以官方门户/新华社/百度百科为 confirmed 依据；个人早期履历细节
以官方/主流媒体公开来源确认；无法确认的现任岗位列于 report/open_gaps.md。

来源：
- 内蒙古自治区人民政府门户 www.nmg.gov.cn（主席/副主席「领导信息」简介，
  2026-07-31 全会公报确认党委书记王伟中、组织部长李东旭）, 2026-08 访问
- 百度百科人物词条（王伟中/包钢/孙绍骋/王莉霞），2026-08 访问
- 中国维基百科（包钢等，引新华社/中国经济网），2026-08 访问
- 新华社 2025-09-30《内蒙古自治区党委主要负责同志职务调整》
"""

from __future__ import annotations

import sqlite3  # SQLite 标准库（经由 gov_relation.runner 落库）

import sys
from pathlib import Path

# 项目根目录（向上寻找包含 gov_relation/ 的仓库根，兼容 data/tmp/<task>/, scripts/build/, 仓库根 三种位置）
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = next((p for p in _HERE.parents if (p / "gov_relation").is_dir()), _HERE)
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build

SLUG = "内蒙古自治区"
DB_PATH = _HERE / "内蒙古自治区_network.db"
GEXF_PATH = _HERE / "内蒙古自治区_network.gexf"

# ── Persons ───────────────────────────────────────────────────────────────
PERSONS = [
    # 1 现任自治区党委书记
    {
        "id": 1,
        "name": "王伟中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962-03",
        "birthplace": "山西朔州",
        "education": "清华大学水利工程系水资源工程专业本科；清华大学管理科学与工程专业研究生、管理学博士",
        "party_join": "1983-10",
        "work_start": "1987-04",
        "current_post": "内蒙古自治区党委书记",
        "current_org": "中国共产党内蒙古自治区委员会",
        "source": "https://baike.baidu.com/item/王伟中",
    },
    # 2 现任自治区主席
    {
        "id": 2,
        "name": "包钢",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1969-05",
        "birthplace": "辽宁阜新",
        "education": "内蒙古大学经济系国民经济管理专业学士；内蒙古党校研究生（公共管理）；清华经管学院EMBA",
        "party_join": "1988-12",
        "work_start": "1991-07",
        "current_post": "内蒙古自治区主席",
        "current_org": "内蒙古自治区人民政府",
        "source": "https://zh.wikipedia.org/zh-cn/包钢_(政治人物)",
    },
    # 3 现任常务副主席（党委常委）
    {
        "id": 3,
        "name": "黄志强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-06",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "内蒙古自治区常务副主席",
        "current_org": "内蒙古自治区人民政府",
        "source": "https://www.nmg.gov.cn/zwgk/zzqzf/hzq/",
    },
    # 4 现任党委常委、组织部部长
    {
        "id": 4,
        "name": "李东旭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "内蒙古自治区党委常委、组织部部长",
        "current_org": "中国共产党内蒙古自治区委员会",
        "source": "https://www.nmg.gov.cn/zwyw/tpxw/202607/t20260731_2935986.html",
    },
    # 5 办公厅副主席（公安厅厅长）郑光照
    {
        "id": 5,
        "name": "郑光照",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-09",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "内蒙古自治区副主席、公安厅厅长",
        "current_org": "内蒙古自治区人民政府",
        "source": "https://www.nmg.gov.cn/zwgk/zzqzf/zgz/",
    },
    # 6 副主席 奇巴图
    {
        "id": 6,
        "name": "奇巴图",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1971-09",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "内蒙古自治区副主席",
        "current_org": "内蒙古自治区人民政府",
        "source": "https://www.nmg.gov.cn/zwgk/zzqzf/qbt/",
    },
    # 7 前党委书记（2022-2025，2026-01 被查）
    {
        "id": 7,
        "name": "孙绍骋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1960-07",
        "birthplace": "山东海阳",
        "education": "山东大学中文系本科；北京大学国际关系学院在职研究生、法学博士",
        "party_join": "1986-05",
        "work_start": "1984-07",
        "current_post": "（前内蒙古自治区党委书记，2026-01-29 接受纪律审查和监察调查）",
        "current_org": "",
        "source": "https://baike.baidu.com/item/孙绍骋",
    },
    # 8 前主席（2021-2025，2025-08 被查、2026-02 双开）
    {
        "id": 8,
        "name": "王莉霞",
        "gender": "女",
        "ethnicity": "蒙古族",
        "birth": "1964-06",
        "birthplace": "辽宁建平",
        "education": "辽宁大学计划统计专业本科；陕西财经学院统计学硕士；厦门大学经济学博士",
        "party_join": "1992-12",
        "work_start": "1985-09",
        "current_post": "（前内蒙古自治区主席，2026-02-12 双开，2026-06 提起公诉）",
        "current_org": "",
        "source": "https://baike.baidu.com/item/王莉霞",
    },
    # 9 政协主席
    {
        "id": 9,
        "name": "张延昆",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "内蒙古自治区政协主席",
        "current_org": "中国人民政治协商会议内蒙古自治区委员会",
        "source": "https://www.nmg.gov.cn/zwgk/zzqzf/",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党内蒙古自治区委员会", "type": "党委", "level": "省级", "parent": "", "location": "内蒙古自治区呼和浩特市"},
    {"id": 2, "name": "内蒙古自治区人民政府", "type": "政府", "level": "省级", "parent": "", "location": "内蒙古自治区呼和浩特市"},
    {"id": 3, "name": "中国共产党内蒙古自治区委员会组织部", "type": "党委", "level": "省级", "parent": "中国共产党内蒙古自治区委员会", "location": "内蒙古自治区呼和浩特市"},
    {"id": 4, "name": "内蒙古自治区公安厅", "type": "政府", "level": "副省级", "parent": "内蒙古自治区人民政府", "location": "内蒙古自治区呼和浩特市"},
    {"id": 5, "name": "内蒙古自治区人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "内蒙古自治区呼和浩特市"},
    {"id": 6, "name": "中国人民政治协商会议内蒙古自治区委员会", "type": "政协", "level": "省级", "parent": "", "location": "内蒙古自治区呼和浩特市"},
]

# ── Positions ─────────────────────────────────────────────────────────────
POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "内蒙古自治区党委书记", "start_date": "2025-09", "end_date": "present", "rank": "正省级", "note": "2025-09 中共中央决定任党委书记；2025-10-18 当选区人大常委会主任；此前任广东省委副书记、省长"},
    {"person_id": 2, "org_id": 2, "title": "内蒙古自治区主席", "start_date": "2025-10", "end_date": "present", "rank": "正省级", "note": "2025-09 任党委副书记、政府党组书记，2025-10-18 当选主席；此前任区党委常委、呼和浩特市委书记"},
    {"person_id": 3, "org_id": 2, "title": "自治区常务副主席", "start_date": "2023", "end_date": "present", "rank": "副省级", "note": "二十届中央候补委员、区党委常委，分管发改/财税/金融等"},
    {"person_id": 4, "org_id": 3, "title": "自治区党委常委、组织部部长", "start_date": "2026", "end_date": "present", "rank": "副省级", "note": "十一届十二次全会主持《决议》说明；履历细节未公开"},
    {"person_id": 5, "org_id": 4, "title": "自治区副主席、公安厅厅长", "start_date": "2023", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "自治区副主席", "start_date": "2021", "end_date": "present", "rank": "副省级", "note": "兼红十字会会长"},
    {"person_id": 7, "org_id": 1, "title": "内蒙古自治区党委书记（前任）", "start_date": "2022-04", "end_date": "2025-09", "rank": "正省级", "note": "2026-01-29 接受纪律审查和监察调查"},
    {"person_id": 8, "org_id": 2, "title": "内蒙古自治区主席（前任）", "start_date": "2021-09", "end_date": "2025-09", "rank": "正省级", "note": "2025-08-22 被查；2026-02-12 双开；2026-06 提起公诉"},
    {"person_id": 9, "org_id": 6, "title": "自治区政协主席", "start_date": "2023", "end_date": "present", "rank": "正省级", "note": ""},
]

# ── Relationships (person <-> person) ─────────────────────────────────────
RELATIONSHIPS = [
    # 王伟中 — 包钢（现任党政一把手搭档）
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "王伟中2025-09任内蒙古党委书记后与主席包钢组成党政一把手搭档", "overlap_org": "内蒙古自治区", "overlap_period": "2025-09至今"},
    # 王伟中 — 前党委书记 孙绍骋（前任后任）
    {"person_a": 1, "person_b": 7, "type": "前任后任", "context": "王伟中2025-09 接任内蒙古党委书记（接替因违纪违法被查的孙绍骋）", "overlap_org": "中国共产党内蒙古自治区委员会", "overlap_period": "2025-09"},
    # 包钢 — 前主席 王莉霞（主席继任链 / 前任后任）
    {"person_a": 2, "person_b": 8, "type": "前任后任", "context": "王莉霞2025-09 卸任内蒙古主席，包钢2025-10继任", "overlap_org": "内蒙古自治区人民政府", "overlap_period": "2025-09至2025-10"},
    # 包钢 — 前书记孙绍骋（共事）
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "孙绍骋任党委书记期间（2022-2025）包钢任区副主席/党委常委、呼和浩特书记", "overlap_org": "内蒙古自治区", "overlap_period": "2022-2025"},
    # 王伟中 — 组织部长 李东旭（上下级）
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "党委书记与党委常委、组织部部长同属自治区党委常委会", "overlap_org": "中国共产党内蒙古自治区委员会", "overlap_period": "present"},
    # 包钢 — 常务副主席 黄志强（上下级 / 政府班子）
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "主席与常务副主席同属自治区政府班子", "overlap_org": "内蒙古自治区人民政府", "overlap_period": "present"},
    # 王莉霞 — 孙绍骋（前任党政一把手，双双被查）
    {"person_a": 8, "person_b": 7, "type": "共事", "context": "孙绍骋任书记期间，王莉霞任主席（2022-2025），二人先后被查", "overlap_org": "内蒙古自治区", "overlap_period": "2022-2025"},
    # 王伟中 — 政协主席张延昆（省委与政协班子协作）
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "党委书记与政协主席同属省级领导层", "overlap_org": "内蒙古自治区", "overlap_period": "2025-09至今"},
]


# ── Main ──────────────────────────────────────────────────────────────────
def main():
    print(f"Building Inner Mongolia (内蒙古自治区) provincial leadership network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print()
    print("Summary:")
    print(f"  Persons:        {len(PERSONS)}")
    print(f"  Organizations:  {len(ORGANIZATIONS)}")
    print(f"  Positions:      {len(POSITIONS)}")
    print(f"  Relationships:  {len(RELATIONSHIPS)}")
    print()

    for p in [DB_PATH, GEXF_PATH]:
        if p.exists():
            print(f"  OK {p.name} ({p.stat().st_size / 1024:.1f} KB)")
        else:
            print(f"  MISSING {p.name}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()