#!/usr/bin/env python3
"""Build script for 临夏县 — county-level government personnel network.

Data sources:
  - 临夏县人民政府网站: https://www.linxiaxian.gov.cn/
  - 临夏县人民政府办公室关于县长、副县长、党组成员工作分工的通知 (2026-06-17)
  - "文斌调研督导防汛减灾工作" news article (2026-07-19)
  - 十八届县人民政府第73次常务会议 news (2026-06-30)
  - 人事任免通知 multiple issues

As-of date: 2026-07-22
"""

import sys
from pathlib import Path

# Add project root so gov_relation is importable
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build

# ── Ensure we use the staging directory ──────────────────────────────────
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "临夏县_network.db"
GEXF_PATH = STAGING / "临夏县_network.gexf"

# ══════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════

PERSONS = [
    # ── 1. 县委书记 ──
    {
        "id": 1,
        "name": "文斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共临夏县委员会",
        "source": "https://www.linxiaxian.gov.cn/lxx/YWDT/zwyw/art/2026/art_05239d73e6c84a4d8dada1e4ae1ec069.html",
    },
    # ── 2. 县长 ──
    {
        "id": 2,
        "name": "马俊平",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "临夏县人民政府",
        "source": "https://www.linxiaxian.gov.cn/lxx/zwgk/zc/agwzlfl/LXZBF/art/2026/art_d06d96349f3b4599baa8f7782302a199.html",
    },
    # ── 3. 县委副书记 ──
    {
        "id": 3,
        "name": "马晓明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共临夏县委员会",
        "source": "https://www.linxiaxian.gov.cn/lxx/YWDT/zwyw/art/2026/art_05239d73e6c84a4d8dada1e4ae1ec069.html",
    },
    # ── 4. 常务副县长 ──
    {
        "id": 4,
        "name": "马建平",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "临夏县人民政府",
        "source": "https://www.linxiaxian.gov.cn/lxx/zwgk/zc/agwzlfl/LXZBF/art/2026/art_d06d96349f3b4599baa8f7782302a199.html",
    },
    # ── 5. 副县长 ──
    {
        "id": 5,
        "name": "郭晓伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临夏县人民政府",
        "source": "https://www.linxiaxian.gov.cn/lxx/zwgk/zc/agwzlfl/LXZBF/art/2026/art_d06d96349f3b4599baa8f7782302a199.html",
    },
    # ── 6. 副县长 ──
    {
        "id": 6,
        "name": "马锦明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临夏县人民政府",
        "source": "https://www.linxiaxian.gov.cn/lxx/zwgk/zc/agwzlfl/LXZBF/art/2026/art_d06d96349f3b4599baa8f7782302a199.html",
    },
    # ── 7. 副县长（挂职）──
    {
        "id": 7,
        "name": "慕华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "临夏县人民政府",
        "source": "https://www.linxiaxian.gov.cn/lxx/zwgk/zc/agwzlfl/LXZBF/art/2026/art_d06d96349f3b4599baa8f7782302a199.html",
    },
    # ── 8. 副县长 ──
    {
        "id": 8,
        "name": "赵国顺",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临夏县人民政府",
        "source": "https://www.linxiaxian.gov.cn/lxx/zwgk/zc/agwzlfl/LXZBF/art/2026/art_d06d96349f3b4599baa8f7782302a199.html",
    },
    # ── 9. 副县长（挂职/中央定点帮扶）──
    {
        "id": 9,
        "name": "胡诚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "临夏县人民政府",
        "source": "https://www.linxiaxian.gov.cn/lxx/zwgk/zc/agwzlfl/LXZBF/art/2026/art_d06d96349f3b4599baa8f7782302a199.html",
    },
    # ── 10. 副县长 ──
    {
        "id": 10,
        "name": "康逢芳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临夏县人民政府",
        "source": "https://www.linxiaxian.gov.cn/lxx/zwgk/zc/agwzlfl/LXZBF/art/2026/art_d06d96349f3b4599baa8f7782302a199.html",
    },
    # ── 11. 副县长 ──
    {
        "id": 11,
        "name": "戴旭东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临夏县人民政府",
        "source": "https://www.linxiaxian.gov.cn/lxx/zwgk/zc/agwzlfl/LXZBF/art/2026/art_d06d96349f3b4599baa8f7782302a199.html",
    },
    # ── 12. 副县长 ──
    {
        "id": 12,
        "name": "王喜",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临夏县人民政府",
        "source": "https://www.linxiaxian.gov.cn/lxx/zwgk/zc/agwzlfl/LXZBF/art/2026/art_d06d96349f3b4599baa8f7782302a199.html",
    },
    # ── 13. 党组成员 ──
    {
        "id": 13,
        "name": "杨士勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员",
        "current_org": "临夏县人民政府",
        "source": "https://www.linxiaxian.gov.cn/lxx/zwgk/zc/agwzlfl/LXZBF/art/2026/art_d06d96349f3b4599baa8f7782302a199.html",
    },
    # ── 14. 党组成员、办公室主任 ──
    {
        "id": 14,
        "name": "周胜平",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、办公室主任",
        "current_org": "临夏县人民政府办公室",
        "source": "https://www.linxiaxian.gov.cn/lxx/zwgk/zc/agwzlfl/LXZBF/art/2026/art_d06d96349f3b4599baa8f7782302a199.html",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共临夏县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共临夏回族自治州委员会",
        "location": "甘肃省临夏回族自治州临夏县",
    },
    {
        "id": 2,
        "name": "临夏县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "临夏回族自治州人民政府",
        "location": "甘肃省临夏回族自治州临夏县",
    },
    {
        "id": 3,
        "name": "临夏县人民政府办公室",
        "type": "政府",
        "level": "县",
        "parent": "临夏县人民政府",
        "location": "甘肃省临夏回族自治州临夏县",
    },
]

POSITIONS = [
    # 文斌
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "2026年7月新闻报道确认"},
    # 马俊平
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "兼任县长"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "负责县政府全面工作"},
    # 马晓明
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马建平
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责县政府日常事务"},
    # 郭晓伟
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责住房公积金、数字政府、政务服务"},
    # 马锦明
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责市场监管、文旅、工信、人社、商务"},
    # 慕华
    {"person_id": 7, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "东西部协作，济南高新区对口协作"},
    # 赵国顺
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责维稳、公安、司法、交通、信访"},
    # 胡诚
    {"person_id": 9, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "中央定点帮扶及招商引资"},
    # 康逢芳
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责科技、教育、卫健、医保、残疾人事业"},
    # 戴旭东
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责农业农村、乡村振兴、水利、民政"},
    # 王喜
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责住建、城市管理、生态环境"},
    # 杨士勇
    {"person_id": 13, "org_id": 2, "title": "党组成员", "start_date": "", "end_date": "present", "rank": "副县级", "note": "东西部协作"},
    # 周胜平
    {"person_id": 14, "org_id": 3, "title": "党组书记、主任", "start_date": "", "end_date": "present", "rank": "正科级", "note": "主持县政府办公室全面工作"},
]

RELATIONSHIPS = [
    # 文斌 <-> 马俊平（书记-县长搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记—县长搭档，县委常委会共事", "overlap_org": "中共临夏县委员会", "overlap_period": "现任"},
    # 文斌 <-> 马晓明（书记-专职副书记）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记—县委副书记，共同调研防汛减灾工作", "overlap_org": "中共临夏县委员会", "overlap_period": "现任"},
    # 马俊平 <-> 马建平（县长-常务副县长）
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长—常务副县长，AB岗搭档；马建平协助县长日常事务", "overlap_org": "临夏县人民政府", "overlap_period": "现任"},
    # 马俊平 <-> 马锦明（县长-副县长）
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县长—副县长，县政府班子共事", "overlap_org": "临夏县人民政府", "overlap_period": "现任"},
    # 马俊平 <-> 戴旭东（县长-副县长）
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "县长—副县长，戴旭东AB岗与马锦明互为", "overlap_org": "临夏县人民政府", "overlap_period": "现任"},
    # 马建平 <-> 王喜（AB岗）
    {"person_a": 4, "person_b": 12, "type": "overlap", "context": "互为AB岗", "overlap_org": "临夏县人民政府", "overlap_period": "现任"},
    # 马锦明 <-> 戴旭东（AB岗）
    {"person_a": 6, "person_b": 11, "type": "overlap", "context": "互为AB岗", "overlap_org": "临夏县人民政府", "overlap_period": "现任"},
    # 赵国顺 <-> 康逢芳（AB岗）
    {"person_a": 8, "person_b": 10, "type": "overlap", "context": "互为AB岗", "overlap_org": "临夏县人民政府", "overlap_period": "现任"},
    # 郭晓伟 -> 马建平（协助关系）
    {"person_a": 5, "person_b": 4, "type": "overlap", "context": "郭晓伟协助马建平工作", "overlap_org": "临夏县人民政府", "overlap_period": "现任"},
    # 慕华 -> 戴旭东（协助关系）
    {"person_a": 7, "person_b": 11, "type": "overlap", "context": "慕华协助戴旭东工作", "overlap_org": "临夏县人民政府", "overlap_period": "现任"},
    # 胡诚 -> 马锦明（协助关系）
    {"person_a": 9, "person_b": 6, "type": "overlap", "context": "胡诚协助马锦明工作", "overlap_org": "临夏县人民政府", "overlap_period": "现任"},
    # 周胜平 <-> 马建平（办公室主任-常务副县长）
    {"person_a": 14, "person_b": 4, "type": "overlap", "context": "县政府办公室主任协调县政府与各部门各乡镇、协助常务副县长", "overlap_org": "临夏县人民政府", "overlap_period": "现任"},
    # 马建平 <-> 马晓明（县委常委班子）
    {"person_a": 4, "person_b": 3, "type": "overlap", "context": "同为县委常委，县委常委会共事", "overlap_org": "中共临夏县委员会", "overlap_period": "现任"},
    # 文斌 <-> 马建平（书记-常委）
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记—县委常委/常务副县长", "overlap_org": "中共临夏县委员会", "overlap_period": "现任"},
]

# ══════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="临夏县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("✅  Build complete.")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
