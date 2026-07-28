#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 扎囊县 (Zhanang County), 山南市, 西藏自治区.

Current officeholders as of 2026-07:
  - Party Secretary (县委书记): 鲁绪超 (confirmed from 2026-07 11th Party Congress article)
  - County Mayor (县长): 索朗格桑 (confirmed from 2025-09 and 2026-07 articles)
  - Predecessor (县委书记): 唐勇 (as of 2025-09, before 鲁绪超)

Sources:
  - https://www.zhanang.gov.cn/xwzx/znyw/202607/t20260709_173194.html (11th Party Congress)
  - https://www.zhanang.gov.cn/xwzx/znyw/202509/t20250915_155347.html (2025 festival article)
  - https://www.zhanang.gov.cn/xwzx/znyw/202509/t20250923_155645.html (2025 employment article)
  - https://www.shannan.gov.cn/xwzx/ldhd/202607/t20260717_173695.html (Li Fuzhong inspection)

Web access note: Exa rate-limited, Baidu 403, Jina timed out, some government subpages
inaccessible. Core leader names are confirmed from official county website (zhanang.gov.cn),
but full biographical details (birth, birthplace, education, career timelines before current
role) remain unverified.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

TODAY = "2026-07-28"
STAGING = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/tmp/xizang_扎囊县")
os.makedirs(STAGING, exist_ok=True)
DB_PATH = os.path.join(STAGING, "扎囊县_network.db")
GEXF_PATH = os.path.join(STAGING, "扎囊县_network.gexf")

# =========================================================================
# PERSONS
# Confidence labels: confirmed=official source, plausible=credible media,
#                    unverified=insufficient evidence
# =========================================================================
persons = [
    # ── Current top leadership ──
    {
        "id": 1,
        "name": "鲁绪超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委书记",
        "current_org": "中共扎囊县委员会",
        "source": "Confirmed: 扎囊县第十一次党代会主席团常务委员会委员名单, zhanang.gov.cn (2026-07-09)"
    },
    {
        "id": 2,
        "name": "索朗格桑",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委副书记、政府县长",
        "current_org": "扎囊县人民政府",
        "source": "Confirmed: presided over 11th Party Congress (zhanang.gov.cn 2026-07-09); 2025 festival article named as 县委副书记、政府县长"
    },
    # ── Standing Committee members (from 11th Party Congress presidium) ──
    {
        "id": 3,
        "name": "洛桑平措",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委常委",
        "current_org": "中共扎囊县委员会",
        "source": "11th Party Congress presidium standing committee member (zhanang.gov.cn 2026-07-09)"
    },
    {
        "id": 4,
        "name": "冯义洲",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "湖南（援藏干部）",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委常务副书记、常务副县长、株洲市第十一批援藏工作队领队",
        "current_org": "中共扎囊县委员会",
        "source": "Confirmed: 2025 employment article as 县委常务副书记、常务副县长、株洲市第十一批援藏工作队领队 (zhanang.gov.cn 2025-09-23); also on 11th Party Congress presidium"
    },
    {
        "id": 5,
        "name": "李建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委常委",
        "current_org": "中共扎囊县委员会",
        "source": "11th Party Congress presidium standing committee list (zhanang.gov.cn 2026-07-09)"
    },
    {
        "id": 6,
        "name": "洛琼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委常委",
        "current_org": "中共扎囊县委员会",
        "source": "11th Party Congress presidium standing committee list (zhanang.gov.cn 2026-07-09)"
    },
    {
        "id": 7,
        "name": "郝磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委常委",
        "current_org": "中共扎囊县委员会",
        "source": "11th Party Congress presidium standing committee list (zhanang.gov.cn 2026-07-09)"
    },
    {
        "id": 8,
        "name": "次旺加布",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委常委",
        "current_org": "中共扎囊县委员会",
        "source": "11th Party Congress presidium standing committee list (zhanang.gov.cn 2026-07-09)"
    },
    {
        "id": 9,
        "name": "谭福强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委常委",
        "current_org": "中共扎囊县委员会",
        "source": "11th Party Congress presidium standing committee list (zhanang.gov.cn 2026-07-09)"
    },
    {
        "id": 10,
        "name": "闫辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委常委",
        "current_org": "中共扎囊县委员会",
        "source": "11th Party Congress presidium standing committee list (zhanang.gov.cn 2026-07-09)"
    },
    {
        "id": 11,
        "name": "张华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委常委、政府副县长",
        "current_org": "扎囊县人民政府",
        "source": "Confirmed: 2025 employment article as 县委常委、政府副县长 (zhanang.gov.cn 2025-09-23); also on 11th Congress presidium"
    },
    {
        "id": 12,
        "name": "拉珍",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委常委",
        "current_org": "中共扎囊县委员会",
        "source": "11th Party Congress presidium standing committee list (zhanang.gov.cn 2026-07-09)"
    },
    {
        "id": 13,
        "name": "陈亚林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委常委",
        "current_org": "中共扎囊县委员会",
        "source": "11th Party Congress presidium standing committee list (zhanang.gov.cn 2026-07-09)"
    },
    {
        "id": 14,
        "name": "胡学民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委常委",
        "current_org": "中共扎囊县委员会",
        "source": "11th Party Congress presidium standing committee list (zhanang.gov.cn 2026-07-09)"
    },
    {
        "id": 15,
        "name": "普布桑珠",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "扎囊县委常委",
        "current_org": "中共扎囊县委员会",
        "source": "11th Party Congress presidium standing committee list (zhanang.gov.cn 2026-07-09)"
    },
    # ── Predecessor ──
    {
        "id": 16,
        "name": "唐勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原扎囊县委书记（2025年在任，2026年离任）",
        "current_org": "",
        "source": "Confirmed as 扎囊县委书记 in 2025 festival article (zhanang.gov.cn 2025-09-15). Succeeded by 鲁绪超 sometime between late 2025 and mid-2026."
    },
    # ── Shannan city leadership (relevant for cross-reference) ──
    {
        "id": 17,
        "name": "李富忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山南市委书记",
        "current_org": "中共山南市委员会",
        "source": "Shannan.gov.cn leadership activity page (2026-07-17 article)"
    },
    {
        "id": 18,
        "name": "桑珠次仁",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山南市委副书记、市长",
        "current_org": "山南市人民政府",
        "source": "Shannan.gov.cn leadership activity page (2026-07-14)"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共扎囊县委员会", "type": "党委", "level": "县级", "parent": "中共山南市委员会", "location": "西藏山南市扎囊县"},
    {"id": 2, "name": "扎囊县人民政府", "type": "政府", "level": "县级", "parent": "山南市人民政府", "location": "西藏山南市扎囊县"},
    {"id": 3, "name": "中共扎囊县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共扎囊县委员会", "location": "西藏山南市扎囊县"},
    {"id": 4, "name": "扎囊县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "西藏山南市扎囊县"},
    {"id": 5, "name": "政协扎囊县委员会", "type": "政协", "level": "县级", "parent": "", "location": "西藏山南市扎囊县"},
    {"id": 6, "name": "中共扎囊县委员会组织部", "type": "党委", "level": "县级", "parent": "中共扎囊县委员会", "location": "西藏山南市扎囊县"},
    {"id": 7, "name": "扎塘镇", "type": "乡镇/街道", "level": "乡级", "parent": "扎囊县", "location": "扎囊县扎塘镇"},
    {"id": 8, "name": "桑耶镇", "type": "乡镇/街道", "level": "乡级", "parent": "扎囊县", "location": "扎囊县桑耶镇"},
    {"id": 9, "name": "扎其乡", "type": "乡镇/街道", "level": "乡级", "parent": "扎囊县", "location": "扎囊县扎其乡"},
    {"id": 10, "name": "阿扎乡", "type": "乡镇/街道", "level": "乡级", "parent": "扎囊县", "location": "扎囊县阿扎乡"},
    {"id": 11, "name": "吉汝乡", "type": "乡镇/街道", "level": "乡级", "parent": "扎囊县", "location": "扎囊县吉汝乡"},
    {"id": 12, "name": "株洲市第十一批援藏工作队", "type": "群团", "level": "县级", "parent": "湖南省株洲市", "location": "西藏山南市扎囊县"},
    {"id": 13, "name": "中共山南市委员会", "type": "党委", "level": "地级", "parent": "中共西藏自治区委员会", "location": "西藏山南市乃东区"},
    {"id": 14, "name": "山南市人民政府", "type": "政府", "level": "地级", "parent": "西藏自治区人民政府", "location": "西藏山南市乃东区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 鲁绪超
    {"person_id": 1, "org_id": 1, "title": "扎囊县委书记", "start_date": "2026", "end_date": "present", "rank": "正县级", "note": "2026年7月已就任（主持十一届党代会）"},
    # 索朗格桑
    {"person_id": 2, "org_id": 2, "title": "扎囊县县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "2025年9月已在任"},
    {"person_id": 2, "org_id": 1, "title": "扎囊县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": "县委副书记、政府县长"},
    # 洛桑平措
    {"person_id": 3, "org_id": 1, "title": "扎囊县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "排名第三"},
    # 冯义洲
    {"person_id": 4, "org_id": 1, "title": "扎囊县委常务副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": "株洲援藏干部"},
    {"person_id": 4, "org_id": 2, "title": "扎囊县常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 12, "title": "株洲市第十一批援藏工作队领队", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 李建
    {"person_id": 5, "org_id": 1, "title": "扎囊县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 洛琼
    {"person_id": 6, "org_id": 1, "title": "扎囊县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 郝磊
    {"person_id": 7, "org_id": 1, "title": "扎囊县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 次旺加布
    {"person_id": 8, "org_id": 1, "title": "扎囊县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 谭福强
    {"person_id": 9, "org_id": 1, "title": "扎囊县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 闫辉
    {"person_id": 10, "org_id": 1, "title": "扎囊县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 张华
    {"person_id": 11, "org_id": 1, "title": "扎囊县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "扎囊县副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "县委常委、政府副县长"},
    # 拉珍
    {"person_id": 12, "org_id": 1, "title": "扎囊县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 陈亚林
    {"person_id": 13, "org_id": 1, "title": "扎囊县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 胡学民
    {"person_id": 14, "org_id": 1, "title": "扎囊县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 普布桑珠
    {"person_id": 15, "org_id": 1, "title": "扎囊县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 唐勇 (predecessor)
    {"person_id": 16, "org_id": 1, "title": "扎囊县委书记", "start_date": "2025之前", "end_date": "2026", "rank": "正县级", "note": "2025年9月仍在任，2026年7月已由鲁绪超接任"},
    # 李富忠
    {"person_id": 17, "org_id": 13, "title": "山南市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 桑珠次仁
    {"person_id": 18, "org_id": 14, "title": "山南市市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 鲁绪超 ←→ 索朗格桑 (县委班子搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "扎囊县委书记与县长工作搭档", "overlap_org": "中共扎囊县委员会/扎囊县人民政府", "overlap_period": "2026-"},
    # 鲁绪超 ←→ 冯义洲 (常委班子)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委正副书记工作关系", "overlap_org": "中共扎囊县委员会", "overlap_period": "2026-"},
    # 鲁绪超 ←→ 唐勇 (前后任)
    {"person_a": 1, "person_b": 16, "type": "predecessor_successor", "context": "唐勇前任扎囊县委书记，鲁绪超接任", "overlap_org": "中共扎囊县委员会", "overlap_period": "2025-2026交接"},
    # 索朗格桑 ←→ 冯义洲 (县长与常务副县长)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长与常务副县长工作关系", "overlap_org": "扎囊县人民政府", "overlap_period": ""},
    # 索朗格桑 ←→ 唐勇 (前后任)
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "在唐勇任书记时县长已为索朗格桑", "overlap_org": "扎囊县", "overlap_period": "2025"},
    # 李富忠 ←→ 鲁绪超 (上下级)
    {"person_a": 17, "person_b": 1, "type": "superior_subordinate", "context": "山南市委书记与扎囊县委书记上下级", "overlap_org": "山南市/扎囊县", "overlap_period": "2026-"},
    # 桑珠次仁 ←→ 索朗格桑 (上下级)
    {"person_a": 18, "person_b": 2, "type": "superior_subordinate", "context": "山南市长与扎囊县长上下级", "overlap_org": "山南市/扎囊县", "overlap_period": ""},
    # 李富忠 → 扎囊县领导班子 (2026-07-17现场调研)
    {"person_a": 17, "person_b": 1, "type": "reported_association", "context": "李富忠2026-07-16赴扎囊县调研", "overlap_org": "扎囊县", "overlap_period": "2026-07-16"},
    {"person_a": 17, "person_b": 2, "type": "reported_association", "context": "李富忠在扎囊县吉汝乡调研", "overlap_org": "扎囊县", "overlap_period": "2026-07-16"},
]

if __name__ == "__main__":
    run_build(
        slug="扎囊县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done! DB:", DB_PATH)
    print("Done! GEXF:", GEXF_PATH)
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")