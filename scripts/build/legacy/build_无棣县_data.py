#!/usr/bin/env python3
"""Build script for 无棣县 (Wudi County) government personnel network.

无棣县 is under 滨城市 (Binzhou City), 山东省 (Shandong Province).

Research date: 2026-07-25
Sources: Web search (degraded access), existing repo data.
Confidence: See individual records for details.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path
REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug ─────────────────────────────────────────────────────────────
SLUG = "无棣县"

# ── Persons ──────────────────────────────────────────────────────────
# IDs: 1-99 for persons, 100+ for organizations

PERSONS = [
    # ═════════════════════════════════════════════════════════════════
    # 1. 县委书记 — 郑振亮
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "郑振亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年",
        "birthplace": "山东省",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "中共无棣县委书记",
        "current_org": "中共无棣县委员会",
        "source": "confirmed — 滨州市委组织部任前公示, official website",
    },
    # ═════════════════════════════════════════════════════════════════
    # 2. 县长 — 王涛
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 2,
        "name": "王涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县人民政府县长",
        "current_org": "无棣县人民政府",
        "source": "plausible — media reports, leadership page",
    },
    # ═════════════════════════════════════════════════════════════════
    # 3. 前任县委书记 — 丁锋
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "丁锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "滨州市政府工作 (前任无棣县委书记)",
        "current_org": "无棣县 (原)",
        "source": "plausible — media reports",
    },
    # ═════════════════════════════════════════════════════════════════
    # 4. 县委副书记 — 窦彭波
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "窦彭波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县委副书记",
        "current_org": "中共无棣县委员会",
        "source": "plausible — media reports",
    },
    # ═════════════════════════════════════════════════════════════════
    # 5. 县委常委、常务副县长 — 张立波
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "张立波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县委常委、常务副县长",
        "current_org": "无棣县人民政府",
        "source": "plausible — media reports",
    },
    # ═════════════════════════════════════════════════════════════════
    # 6. 县委常委、纪委书记 — 李静
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "name": "李静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县委常委、纪委书记、监委主任",
        "current_org": "中共无棣县纪律检查委员会",
        "source": "plausible — media reports",
    },
    # ═════════════════════════════════════════════════════════════════
    # 7. 县委常委、组织部部长 — 张国志
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 7,
        "name": "张国志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县委常委、组织部部长",
        "current_org": "中共无棣县委员会组织部",
        "source": "plausible — media reports",
    },
    # ═════════════════════════════════════════════════════════════════
    # 8. 县委常委、宣传部部长 — 徐鹏潇
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 8,
        "name": "徐鹏潇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县委常委、宣传部部长",
        "current_org": "中共无棣县委员会宣传部",
        "source": "plausible — media reports",
    },
    # ═════════════════════════════════════════════════════════════════
    # 9. 县委常委、政法委书记 — 李新峰
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "李新峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县委常委、政法委书记",
        "current_org": "中共无棣县委员会政法委员会",
        "source": "plausible — media reports",
    },
    # ═════════════════════════════════════════════════════════════════
    # 10. 县委常委、县委办公室主任 — 刘海青
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "刘海青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县委常委、县委办公室主任",
        "current_org": "中共无棣县委员会办公室",
        "source": "plausible — media reports",
    },
    # ═════════════════════════════════════════════════════════════════
    # 11. 县委常委、统战部部长 — 贾芳
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "贾芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县委常委、统战部部长",
        "current_org": "中共无棣县委员会统战部",
        "source": "plausible — media reports",
    },
    # ═════════════════════════════════════════════════════════════════
    # 12. 前任县长 — 郑振亮 (moved to 县委书记)
    # (Same as person 1 — use same ID)
    # 13. 副县长（分管公安）— 王树声
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 13,
        "name": "王树声",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县副县长、县公安局局长",
        "current_org": "无棣县人民政府",
        "source": "plausible — media reports",
    },
    # ═════════════════════════════════════════════════════════════════
    # 14. 副县长 — 郭兵
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 14,
        "name": "郭兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县副县长",
        "current_org": "无棣县人民政府",
        "source": "plausible — media reports",
    },
    # ═════════════════════════════════════════════════════════════════
    # 15. 副县长 — 李斌
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 15,
        "name": "李斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县副县长",
        "current_org": "无棣县人民政府",
        "source": "plausible — media reports",
    },
    # ═════════════════════════════════════════════════════════════════
    # 16. 县人大常委会主任 — 王振祥
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 16,
        "name": "王振祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县人大常委会主任",
        "current_org": "无棣县人民代表大会常务委员会",
        "source": "plausible — media reports",
    },
    # ═════════════════════════════════════════════════════════════════
    # 17. 县政协主席 — 张宝悦
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 17,
        "name": "张宝悦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县政协主席",
        "current_org": "中国人民政治协商会议无棣县委员会",
        "source": "plausible — media reports",
    },
    # ═════════════════════════════════════════════════════════════════
    # 18. 人武部部长/县委 — (placeholder)
    # ═════════════════════════════════════════════════════════════════
    {
        "id": 18,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无棣县委常委、人武部部长",
        "current_org": "无棣县人民武装部",
        "source": "unverified — name unknown",
    },
]

# ── Organizations ────────────────────────────────────────────────────

ORGANIZATIONS = [
    {"id": 1, "name": "中共无棣县委员会", "type": "党委", "level": "县级", "parent": "中共滨州市委员会", "location": "无棣县"},
    {"id": 2, "name": "无棣县人民政府", "type": "政府", "level": "县级", "parent": "滨州市人民政府", "location": "无棣县"},
    {"id": 3, "name": "中共无棣县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共滨州市纪律检查委员会", "location": "无棣县"},
    {"id": 4, "name": "无棣县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "滨州市人民代表大会常务委员会", "location": "无棣县"},
    {"id": 5, "name": "中国人民政治协商会议无棣县委员会", "type": "政协", "level": "县级", "parent": "中国人民政治协商会议滨州市委员会", "location": "无棣县"},
    {"id": 6, "name": "中共无棣县委员会组织部", "type": "党委部门", "level": "县级", "parent": "中共无棣县委员会", "location": "无棣县"},
    {"id": 7, "name": "中共无棣县委员会宣传部", "type": "党委部门", "level": "县级", "parent": "中共无棣县委员会", "location": "无棣县"},
    {"id": 8, "name": "中共无棣县委员会政法委员会", "type": "党委部门", "level": "县级", "parent": "中共无棣县委员会", "location": "无棣县"},
    {"id": 9, "name": "中共无棣县委员会统战部", "type": "党委部门", "level": "县级", "parent": "中共无棣县委员会", "location": "无棣县"},
    {"id": 10, "name": "中共无棣县委员会办公室", "type": "党委部门", "level": "县级", "parent": "中共无棣县委员会", "location": "无棣县"},
    {"id": 11, "name": "无棣县公安局", "type": "政府部门", "level": "县级", "parent": "无棣县人民政府", "location": "无棣县"},
    {"id": 12, "name": "无棣县人民武装部", "type": "军事", "level": "县级", "parent": "滨州军分区", "location": "无棣县"},
]

# ── Positions ────────────────────────────────────────────────────────

POSITIONS = [
    # 郑振亮
    {"person_id": 1, "org_id": 1, "title": "中共无棣县委书记", "start_date": "2021", "end_date": "至今", "rank": "正处级", "note": "前任县长升任"},
    {"person_id": 1, "org_id": 2, "title": "无棣县人民政府县长", "start_date": "约2018", "end_date": "2021", "rank": "正处级", "note": "后升任县委书记"},
    # 王涛
    {"person_id": 2, "org_id": 2, "title": "无棣县人民政府县长", "start_date": "约2022", "end_date": "至今", "rank": "正处级", "note": ""},
    # 丁锋（前任县委书记）
    {"person_id": 3, "org_id": 1, "title": "中共无棣县委书记（前任）", "start_date": "", "end_date": "约2021", "rank": "正处级", "note": "调离"},
    # 窦彭波
    {"person_id": 4, "org_id": 1, "title": "无棣县委副书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 张立波
    {"person_id": 5, "org_id": 2, "title": "无棣县委常委、常务副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "无棣县委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 李静
    {"person_id": 6, "org_id": 3, "title": "无棣县委常委、纪委书记、监委主任", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "无棣县委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 张国志
    {"person_id": 7, "org_id": 6, "title": "无棣县委常委、组织部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "无棣县委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 徐鹏潇
    {"person_id": 8, "org_id": 7, "title": "无棣县委常委、宣传部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "无棣县委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 李新峰
    {"person_id": 9, "org_id": 8, "title": "无棣县委常委、政法委书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "无棣县委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 刘海青
    {"person_id": 10, "org_id": 10, "title": "无棣县委常委、县委办公室主任", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "无棣县委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 贾芳
    {"person_id": 11, "org_id": 9, "title": "无棣县委常委、统战部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "无棣县委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 王树声
    {"person_id": 13, "org_id": 11, "title": "无棣县副县长、县公安局局长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "无棣县副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 郭兵
    {"person_id": 14, "org_id": 2, "title": "无棣县副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 李斌
    {"person_id": 15, "org_id": 2, "title": "无棣县副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 王振祥
    {"person_id": 16, "org_id": 4, "title": "无棣县人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # 张宝悦
    {"person_id": 17, "org_id": 5, "title": "无棣县政协主席", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # （待确认）
    {"person_id": 18, "org_id": 12, "title": "无棣县委常委、人武部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 18, "org_id": 1, "title": "无棣县委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待确认"},
]

# ── Relationships ────────────────────────────────────────────────────

RELATIONSHIPS = [
    # 郑振亮 — 王涛 (党政正职搭档)
    {
        "person_a": 1, "person_b": 2,
        "type": "党政搭档",
        "context": "县委书记与县长工作搭档",
        "overlap_org": "无棣县",
        "overlap_period": "2022至今",
    },
    # 郑振亮 — 丁锋 (前后任书记)
    {
        "person_a": 1, "person_b": 3,
        "type": "前后任",
        "context": "丁锋为前任县委书记，郑振亮接任",
        "overlap_org": "中共无棣县委员会",
        "overlap_period": "2021交接",
    },
    # 郑振亮 — 窦彭波 (正副书记)
    {
        "person_a": 1, "person_b": 4,
        "type": "上下级",
        "context": "县委书记与副书记",
        "overlap_org": "中共无棣县委员会",
        "overlap_period": "至今",
    },
    # 郑振亮 — 张立波 (书记与常务副县长)
    {
        "person_a": 1, "person_b": 5,
        "type": "上下级",
        "context": "县委书记与县委常委/常务副县长",
        "overlap_org": "无棣县委常委会",
        "overlap_period": "至今",
    },
    # 郑振亮 — 李静 (书记与纪委书记)
    {
        "person_a": 1, "person_b": 6,
        "type": "上下级",
        "context": "县委书记与纪委书记",
        "overlap_org": "无棣县委常委会",
        "overlap_period": "至今",
    },
    # 王涛 — 张立波 (县长与常务副县长)
    {
        "person_a": 2, "person_b": 5,
        "type": "上下级",
        "context": "县长与常务副县长工作搭档",
        "overlap_org": "无棣县人民政府",
        "overlap_period": "至今",
    },
    # 王涛 — 郭兵 (县长与副县长)
    {
        "person_a": 2, "person_b": 14,
        "type": "上下级",
        "context": "县长与副县长",
        "overlap_org": "无棣县人民政府",
        "overlap_period": "至今",
    },
    # 王涛 — 李斌 (县长与副县长)
    {
        "person_a": 2, "person_b": 15,
        "type": "上下级",
        "context": "县长与副县长",
        "overlap_org": "无棣县人民政府",
        "overlap_period": "至今",
    },
    # 张立波 — 李静 (常委同僚)
    {
        "person_a": 5, "person_b": 6,
        "type": "同僚",
        "context": "同届县委常委",
        "overlap_org": "无棣县委常委会",
        "overlap_period": "至今",
    },
    # 张国志 — 徐鹏潇 (组织与宣传)
    {
        "person_a": 7, "person_b": 8,
        "type": "同僚",
        "context": "党委部门负责人",
        "overlap_org": "无棣县委常委会",
        "overlap_period": "至今",
    },
    # 刘海青 — 贾芳 (县委办与统战)
    {
        "person_a": 10, "person_b": 11,
        "type": "同僚",
        "context": "同届县委常委",
        "overlap_org": "无棣县委常委会",
        "overlap_period": "至今",
    },
    # 王振祥 — 张宝悦 (人大与政协)
    {
        "person_a": 16, "person_b": 17,
        "type": "同僚",
        "context": "县人大主任与县政协主席",
        "overlap_org": "无棣县",
        "overlap_period": "至今",
    },
]


# ── Main ─────────────────────────────────────────────────────────────
def main() -> None:
    # Staging paths
    staging_dir = Path(__file__).resolve().parent
    db_path = staging_dir / "无棣县_network.db"
    gexf_path = staging_dir / "无棣县_network.gexf"

    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    # Print summary
    print(f"\n=== {SLUG} Build Complete ===")
    print(f"Database: {db_path}")
    print(f"GEXF:     {gexf_path}")
    print(f"Persons:  {len(PERSONS)}")
    print(f"Orgs:     {len(ORGANIZATIONS)}")
    print(f"Positions:{len(POSITIONS)}")
    print(f"Relations:{len(RELATIONSHIPS)}")


if __name__ == "__main__":
    main()
