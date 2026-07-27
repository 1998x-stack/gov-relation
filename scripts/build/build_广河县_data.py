#!/usr/bin/env python3
"""Build script for 广河县 — county-level government personnel network.

Data sources:
  - 广河县人民政府网站: https://www.ghx.gov.cn/
  - 县政府领导分工页面: https://www.ghx.gov.cn/ghx/zwgk/fdzdgknr/jgjj/ZFGZJG/
  - 县委常委会会议新闻 (2026-07-12): https://www.ghx.gov.cn/ghx/ywdt/szyw/art/2026/art_3a70da2855224950b2e0d14ea243fa68.html
  - 陈启智到城关镇调研 (2026-06-23): https://www.ghx.gov.cn/ghx/ywdt/zwdt/art/2026/art_4c0066065d0d448ca4546b5cac2eb5fb.html
  - 陈启智暗访检查防汛备汛 (2026-07-10): https://www.ghx.gov.cn/ghx/ywdt/zwdt/art/2026/art_76546a17947b41f49a6eef536fd246e7.html
  - 防汛备汛工作视频调度会 (2026-07-09): https://www.ghx.gov.cn/ghx/ywdt/szyw/art/2026/art_f605c2689610449c9385cd5661b834e3.html
  - 广河县举办第九期高质量发展大讲堂 (2026-07-10): https://www.ghx.gov.cn/ghx/ywdt/szyw/art/2026/art_2936efbf9dfa4db1ba39f46845cf71a3.html

As-of date: 2026-07-22
"""

import sqlite3
import sys
from pathlib import Path

# Add project root so gov_relation is importable
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build

# ── Ensure we use the staging directory ──────────────────────────────────
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "广河县_network.db"
GEXF_PATH = STAGING / "广河县_network.gexf"

# ══════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════

PERSONS = [
    # ── 1. 县委书记 ──
    {
        "id": 1,
        "name": "陈启智",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共广河县委员会",
        "source": "https://www.ghx.gov.cn/ghx/ywdt/szyw/art/2026/art_3a70da2855224950b2e0d14ea243fa68.html",
    },
    # ── 2. 县人大主任 ──
    {
        "id": 2,
        "name": "马学良",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "广河县人民代表大会常务委员会",
        "source": "https://www.ghx.gov.cn/ghx/ywdt/szyw/art/2026/art_f605c2689610449c9385cd5661b834e3.html",
    },
    # ── 3. 县政协主席 ──
    {
        "id": 3,
        "name": "马海俊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组书记、主席",
        "current_org": "政协广河县委员会",
        "source": "https://www.ghx.gov.cn/ghx/ywdt/szyw/art/2026/art_f605c2689610449c9385cd5661b834e3.html",
    },
    # ── 4. 县委副书记（待确认，可能刘永东） ──
    {
        "id": 4,
        "name": "刘永东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委领导",
        "current_org": "中共广河县委员会",
        "source": "https://www.ghx.gov.cn/ghx/ywdt/szyw/art/2026/art_f605c2689610449c9385cd5661b834e3.html",
    },
    # ── 5. 常务副县长 ──
    {
        "id": 5,
        "name": "郭斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1991年3月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "广河县人民政府",
        "source": "https://www.ghx.gov.cn/ghx/zwgk/fdzdgknr/jgjj/ZFGZJG/",
    },
    # ── 6. 县委常委、副县长（中央定点帮扶） ──
    {
        "id": 6,
        "name": "向霄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年9月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "广河县人民政府",
        "source": "https://www.ghx.gov.cn/ghx/zwgk/fdzdgknr/jgjj/ZFGZJG/",
    },
    # ── 7. 县委常委、副县长（东西部协作） ──
    {
        "id": 7,
        "name": "李荣金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年5月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "广河县人民政府",
        "source": "https://www.ghx.gov.cn/ghx/zwgk/fdzdgknr/jgjj/ZFGZJG/",
    },
    # ── 8. 县委常委、副县长（国有企业管理） ──
    {
        "id": 8,
        "name": "祁东明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年3月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "广河县人民政府",
        "source": "https://www.ghx.gov.cn/ghx/zwgk/fdzdgknr/jgjj/ZFGZJG/",
    },
    # ── 9. 县委常委、副县长（农业农村） ──
    {
        "id": 9,
        "name": "马全忠",
        "gender": "男",
        "ethnicity": "东乡族",
        "birth": "1976年9月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "广河县人民政府",
        "source": "https://www.ghx.gov.cn/ghx/zwgk/fdzdgknr/jgjj/ZFGZJG/",
    },
    # ── 10. 县委常委、组织部部长 ──
    {
        "id": 10,
        "name": "陕玺",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共广河县委员会",
        "source": "https://www.ghx.gov.cn/ghx/ywdt/zwdt/art/2026/art_4c0066065d0d448ca4546b5cac2eb5fb.html",
    },
    # ── 11. 副县长、公安局局长 ──
    {
        "id": 11,
        "name": "潘学江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年3月",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "广河县人民政府",
        "source": "https://www.ghx.gov.cn/ghx/zwgk/fdzdgknr/jgjj/ZFGZJG/",
    },
    # ── 12. 副县长（交通运输、工业） ──
    {
        "id": 12,
        "name": "李昉昕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年8月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "广河县人民政府",
        "source": "https://www.ghx.gov.cn/ghx/zwgk/fdzdgknr/jgjj/ZFGZJG/",
    },
    # ── 13. 副县长（卫生健康） ──
    {
        "id": 13,
        "name": "张丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1990年4月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "广河县人民政府",
        "source": "https://www.ghx.gov.cn/ghx/zwgk/fdzdgknr/jgjj/ZFGZJG/",
    },
    # ── 14. 副县长（生态环境、住建） ──
    {
        "id": 14,
        "name": "冶鹏",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1979年4月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "广河县人民政府",
        "source": "https://www.ghx.gov.cn/ghx/zwgk/fdzdgknr/jgjj/ZFGZJG/",
    },
    # ── 15. 县领导（出席大讲堂活动） ──
    {
        "id": 15,
        "name": "马绍鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "广河县",
        "source": "https://www.ghx.gov.cn/ghx/ywdt/szyw/art/2026/art_2936efbf9dfa4db1ba39f46845cf71a3.html",
    },
    # ── 16. 县领导（出席大讲堂活动） ──
    {
        "id": 16,
        "name": "马魁",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "广河县",
        "source": "https://www.ghx.gov.cn/ghx/ywdt/szyw/art/2026/art_2936efbf9dfa4db1ba39f46845cf71a3.html",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共广河县委员会", "type": "党委", "level": "县级", "parent": "中共临夏回族自治州委员会", "location": "广河县"},
    {"id": 2, "name": "广河县人民政府", "type": "政府", "level": "县级", "parent": "临夏回族自治州人民政府", "location": "广河县"},
    {"id": 3, "name": "广河县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "临夏回族自治州人民代表大会常务委员会", "location": "广河县"},
    {"id": 4, "name": "政协广河县委员会", "type": "政协", "level": "县级", "parent": "政协临夏回族自治州委员会", "location": "广河县"},
    {"id": 5, "name": "广河县公安局", "type": "政府", "level": "科级", "parent": "广河县人民政府", "location": "广河县"},
    {"id": 6, "name": "中共广河县委组织部", "type": "党委", "level": "科级", "parent": "中共广河县委员会", "location": "广河县"},
]

POSITIONS = [
    # 陈启智
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 马学良
    {"person_id": 2, "org_id": 3, "title": "县人大常委会党组书记、主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 马海俊
    {"person_id": 3, "org_id": 4, "title": "县政协党组书记、主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 刘永东
    {"person_id": 4, "org_id": 1, "title": "县委领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待确认，出现在县领导名单中"},
    # 郭斌
    {"person_id": 5, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责县政府日常事务"},
    # 向霄
    {"person_id": 6, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "中央单位定点帮扶"},
    # 李荣金
    {"person_id": 7, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "东西部协作"},
    # 祁东明
    {"person_id": 8, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "国有企业管理"},
    # 马全忠
    {"person_id": 9, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "农业农村"},
    # 陕玺
    {"person_id": 10, "org_id": 6, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 陕玺 also in 县委
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 潘学江
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "公安"},
    {"person_id": 11, "org_id": 5, "title": "县公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "三级高级警长"},
    # 李昉昕
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "交通运输、工业"},
    # 张丽
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "卫生健康"},
    # 冶鹏
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "生态环境、住建"},
]

RELATIONSHIPS = [
    # 陈启智 <-> 郭斌 (书记—常务副县长上下级)
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记—常务副县长", "overlap_org": "广河县", "overlap_period": "2026"},
    # 陈启智 <-> 马全忠 (书记—副县长上下级)
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记—副县长", "overlap_org": "广河县", "overlap_period": "2026"},
    # 陈启智 <-> 陕玺 (书记—组织部长)
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "县委书记—组织部部长", "overlap_org": "中共广河县委员会", "overlap_period": "2026"},
    # 马全忠 <-> 陕玺 (一同参加调研)
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "一同陪同县委书记调研城关镇", "overlap_org": "广河县", "overlap_period": "2026-06"},
    # 郭斌 <-> 马全忠 (共同参加防汛调度会)
    {"person_a": 5, "person_b": 9, "type": "overlap", "context": "一同参加全县防汛备汛视频调度会", "overlap_org": "广河县人民政府", "overlap_period": "2026-07"},
    # 马学良 <-> 马海俊 (人大主任—政协主席)
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "人大主任和政协主席共同参加防汛调度会", "overlap_org": "广河县", "overlap_period": "2026-07"},
    # 陈启智 <-> 马学良
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记和人大主任共同参加防汛调度会", "overlap_org": "广河县", "overlap_period": "2026-07"},
    # 陈启智 <-> 马海俊
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记和政协主席共同参加防汛调度会", "overlap_org": "广河县", "overlap_period": "2026-07"},
    # 陈启智 <-> 刘永东
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "在县委常委会共事", "overlap_org": "中共广河县委员会", "overlap_period": "2026"},
    # 郭斌 <-> 向霄 (常务副县长—副县长)
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "县政府班子成员", "overlap_org": "广河县人民政府", "overlap_period": "2026"},
    # 郭斌 <-> 李昉昕
    {"person_a": 5, "person_b": 12, "type": "overlap", "context": "县政府班子成员", "overlap_org": "广河县人民政府", "overlap_period": "2026"},
]

# ══════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="广河县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done. Files created:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
