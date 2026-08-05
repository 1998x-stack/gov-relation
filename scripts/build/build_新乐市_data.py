#!/usr/bin/env python3
"""
新乐市领导班子工作关系网络 — Build script
河北省石家庄市新乐市（县级市）

官方来源（新乐市人民政府 www.xinle.gov.cn）确认：
- 2026-07-28 新乐要闻「市委常委会召开会议 卢占军主持并讲话」: 市委书记卢占军
- 2026-07-27 新乐要闻「市委理论学习中心组召开学习会」: 市委书记卢占军主持；张桂英、牛世超、杨建哲、吴晋发言
- 2026-08-02 新乐要闻「卢占军走访慰问驻新部队官兵」: 卢占军（书记军地慰问）
- 2026-02-03 市七届人大常委会四十二次会议 / 市政府第118次常务会议: 市委副书记、市长葛利强
- 2026-05-08 市委常委会扩大会议: 市委书记李明政（前任书记，2026-05/06 由卢占军接任）
- 2026-05-16 市七届人大常委会第42次会议: 人大主任甄剑峰、副主任丁纬国/史战英/赵洪波；市委常委、常务副市长魏春光
- 市长之窗（2026-05-27 更新）: 市长葛利强；常务副市长杜威世；常委副市长李洪田；副市长李丽霞/祁建立/李金永/康勇/王艳；四级调研员马红永；党组成员(挂职)董玲缓

Leadership succession (官方会议纪录):
- 卢占军: 约2026年5-6月 接任李明君为新乐市委书记（2026-05 仍在任书记为李明君；2026-07 起以卢占军为书记）
- 葛利强: 2026年（至迟2026-02）任市委副书记、市长至今

Research date: 2026-08-05
"""

import os
import sqlite3
import sys


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

AS_OF = "2026-08-05"

# ── PERSONS ──
persons = [
    # ── 市委书记 (Party Secretary) ──
    {
        "id": 1,
        "name": "卢占军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新乐市委书记",
        "current_org": "中共新乐市委员会",
        "source": "http://www.xinle.gov.cn/columns/ddfcf040-ee42-4e8d-acdc-a8cb9bc0a886/202607/28/955c3b83-7013-4ca7-afe7-1af73f37671f.html",
    },
    # ── 市长 (Mayor) ──
    {
        "id": 2,
        "name": "葛利强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新乐市委副书记、市长",
        "current_org": "新乐市人民政府",
        "source": "https://www.xinle.gov.cn/columns/88a78b9e-b6c9-411a-b267-527c19245218/202604/24/7555dde8-f447-417e-9d8f-c559efaeb5fd.html",
    },
    # ── 常务副市长 ──
    {
        "id": 3,
        "name": "杜威世",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "新乐市人民政府",
        "source": "http://www.xinle.gov.cn/columns/a551cc60-e824-4540-ad7b-4933f4648a3c/202602/28/ca0f4fc0-de59-4130-b991-0dce649b508c.html",
    },
    # ── 市委常委、副市长 ──
    {
        "id": 4,
        "name": "李浩田",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "新乐市人民政府",
        "source": "http://www.xinle.gov.cn/columns/a551cc60-e824-4540-ad7b-4933f4648a3c/202003/17/165b9374-d355-499b-854c-f2a50f5e0964.html",
    },
    # ── 副市长 ──
    {
        "id": 5,
        "name": "李丽霞",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "新乐市人民政府",
        "source": "http://www.xinle.gov.cn/columns/a551cc60-e824-4540-ad7b-4933f4648a3c/202003/17/c390ef87-6af7-450a-acdd-9e41d0536cbe.html",
    },
    {
        "id": 6,
        "name": "祁建立",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "新乐市人民政府",
        "source": "http://www.xinle.gov.cn/columns/a551cc60-e824-4540-ad7b-4933f4648a3c/202003/17/978f7f15-31a9-4ed0-8f11-c103ddf36078.html",
    },
    {
        "id": 7,
        "name": "李金永",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "新乐市人民政府",
        "source": "http://www.xinle.gov.cn/columns/a551cc60-e824-4540-ad7b-4933f4648a3c/202106/10/6442737a-b4fc-4501-85e4-9e32ceb1cce6.html",
    },
    {
        "id": 8,
        "name": "康勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "新乐市人民政府",
        "source": "http://www.xinle.gov.cn/columns/a551cc60-e824-4540-ad7b-4933f4648a3c/202501/02/7e2dc3ae-9275-4b14-9279-bdcfd97e5e74.html",
    },
    {
        "id": 9,
        "name": "王艳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "新乐市人民政府",
        "source": "http://www.xinle.gov.cn/columns/a551cc60-e824-4540-ad7b-4933f4648a3c/202501/02/f2ed7aab-ee5c-4d7d-8ccc-ac22844ac054.html",
    },
    # ── 人大主任 ──
    {
        "id": 10,
        "name": "甄剑峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "新乐市人大常委会",
        "source": "http://www.xinle.gov.cn/columns/88a78b9e-b6c9-411a-b267-527c19245218/202605/26/d05e3c49-1bd4-4dfe-9f26-69b3f1c6555f.html",
    },
    # ── 前任市委书记 ──
    {
        "id": 11,
        "name": "李明政",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-01",
        "birthplace": "河北泊头",
        "education": "河北科技师范学院机械电子系",
        "party_join": "2002-05",
        "work_start": "2003-08",
        "current_post": "衡水市委常委、组织部部长（前任新乐市委书记）",
        "current_org": "中共衡水市委",
        "source": "http://www.xinle.gov.cn/columns/88a78b9e-b6c9-411a-b267-527c19245218/202605/26/072c9032-eead-4bfe-ae15-bf943a1be66e.html",
    },
    # ── 市委理论学习中心组发言成员（市委常委会成员风向） ──
    {
        "id": 12,
        "name": "魏春光",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原市委常委、常务副市长",
        "current_org": "新乐市人民政府",
        "source": "http://www.xinle.gov.cn/columns/88a78b9e-b6c9-411a-b267-527c19245218/202605/26/d05e3c49-1bd4-4dfe-9f26-69b3f1c6555f.html",
    },
    # ── 前任市长（宫世友） ──
    {
        "id": 13,
        "name": "宫世友",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任新乐市长（2025-03卸任）",
        "current_org": "卸任/去向待查",
        "source": "http://www.xinle.gov.cn/columns/ddfcf040-ee42-4e8d-acdc-a8cb9bc0a886/index.html",
    },
    # ── 市委副书记 ──
    {
        "id": 14,
        "name": "张桂英",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新乐市委副书记",
        "current_org": "中共新乐市委员会",
        "source": "http://www.xinle.gov.cn/columns/ddfcf040-ee42-4e8d-acdc-a8cb9bc0a886/202607/28/fdd400e4-0bdd-4e99-a168-dd59c4788910.html",
    },
    {
        "id": 15,
        "name": "郄静",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新乐市委副书记",
        "current_org": "中共新乐市委员会",
        "source": "http://www.xinle.gov.cn/columns/88a78b9e-b6c9-411a-b267-2c1c6b0572e6e.html",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共新乐市委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共石家庄市委员会",
        "location": "河北省石家庄市新乐市",
    },
    {
        "id": 2,
        "name": "新乐市人民政府",
        "type": "政府",
        "level": "县级市",
        "parent": "石家庄市人民政府",
        "location": "河北省石家庄市新乐市",
    },
    {
        "id": 3,
        "name": "新乐市人大常委会",
        "type": "人大",
        "level": "县级市",
        "parent": "新乐市",
        "location": "河北省石家庄市新乐市",
    },
    {
        "id": 4,
        "name": "政协新乐市委员会",
        "type": "政协",
        "level": "县级市",
        "parent": "新乐市",
        "location": "河北省石家庄市新乐市",
    },
    {
        "id": 5,
        "name": "赞皇县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "石家庄市人民政府",
        "location": "河北省石家庄市赞皇县",
    },
    {
        "id": 6,
        "name": "中共平山县委",
        "type": "党委",
        "level": "县",
        "parent": "中共石家庄市委",
        "location": "河北省石家庄市平山县",
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 卢占军 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "新乐市委书记",
     "start_date": "2026-07-23", "end_date": "present",
     "rank": "正处级", "note": "2026-07-23由赞皇县委副书记/县长调任新乐市委书记（跨县交流）；2026-07-27在任（市委常委会报道）"},
    {"person_id": 1, "org_id": 5, "title": "赞皇县委副书记、县长（此前）",
     "start_date": "2022-05", "end_date": "2026-07",
     "rank": "正处级", "note": "2022-05代理、2022-06当选赞皇县委副书记/县长（百度百科）；2026-07调新乐"},
    {"person_id": 1, "org_id": 6, "title": "平山县委副书记（此前）",
     "start_date": "2021-07", "end_date": "2022-05",
     "rank": "副处级/正处级", "note": "2021-07-20平山县委十一届一中全会当选县委副书记；此前任平山县委常委、政法委书记、西柏坡经济开发区党工委副书记/管委会副主任（百度百科）"},
    # 葛利强 — 市委副书记、市长
    {"person_id": 2, "org_id": 1, "title": "新乐市委副书记",
     "start_date": "2025-03", "end_date": "present",
     "rank": "正处级", "note": "市长兼任市委副书记（2026-02-03市政府第118次常务会以市委副书记、市长身份主持）"},
    {"person_id": 2, "org_id": 2, "title": "新乐市人民政府市长",
     "start_date": "2025-03-30", "end_date": "present",
     "rank": "正处级", "note": "2025-03-25代理、2025-03-30在新乐市七届人大六次会议上当选市长；2026-02-03主持市政府第118次常务会"},
    {"person_id": 2, "org_id": 2, "title": "新乐市人民政府副市长（此前）",
     "start_date": "2023-07", "end_date": "2025-03",
     "rank": "副处级", "note": "2023-07任新乐市副市长，后升任代理市长/市长（百度百科）"},
    # 杜威世 — 常务副市长
    {"person_id": 3, "org_id": 2, "title": "新乐市常务副市长",
     "start_date": "2026?", "end_date": "present",
     "rank": "副处级", "note": "市长之窗2026-05-27更新；负责市政府常务工作"},
    # 李浩田 — 市委常委会、副市长
    {"person_id": 4, "org_id": 2, "title": "新乐市副市长",
     "start_date": "2026?", "end_date": "present",
     "rank": "副处级", "note": "市长之窗列明；协助杜威海同志负责生态"},
    # 副市长
    {"person_id": 5, "org_id": 2, "title": "新乐市副市长",
     "start_date": "2026?", "end_date": "present", "rank": "副处级", "note": "负责科技工信/市场监管/退役军人"},
    {"person_id": 6, "org_id": 2, "title": "新乐市副市长",
     "start_date": "2026?", "end_date": "present", "rank": "副处级", "note": "负责公安/司法/民宗"},
    {"person_id": 7, "org_id": 2, "title": "新乐市副市长",
     "start_date": "2026?", "end_date": "present", "rank": "副处级", "note": "负责农业农村/水利/民政"},
    {"person_id": 8, "org_id": 2, "title": "新乐市副市长",
     "start_date": "2026?", "end_date": "present", "rank": "副处级", "note": "负责教育/卫生/文旅"},
    {"person_id": 9, "org_id": 2, "title": "新乐市副市长",
     "start_date": "2026?", "end_date": "present", "rank": "副处级", "note": "负责自然资源/住建/城管"},
    # 甄剑峰 — 人大主任
    {"person_id": 10, "org_id": 3, "title": "市人大常委会主任",
     "start_date": "2026?", "end_date": "present", "rank": "正处级", "note": "2026-05-16市七届人大常委会第42次会议出席"},
    # 李明政 — 前任市委书记
    {"person_id": 11, "org_id": 1, "title": "新乐市委书记（前任）",
     "start_date": "2021-05", "end_date": "2026-07",
     "rank": "正处级", "note": "2021-05-19任新乐市委书记；2026-05-08仍主持市委常委会扩大会议；后卢占军接任。此前任新乐市长（2020-01起）"},
    {"person_id": 11, "org_id": 1, "title": "衡水市委常委、组织部部长（现任）",
     "start_date": "2026-07", "end_date": "present",
     "rank": "副厅级", "note": "跨市履新至衡水市委（2026-07），由新乐市委书记转任（百度百科）"},
    # 宫世友 — 前任市长
    {"person_id": 13, "org_id": 2, "title": "新乐市人民政府市长（前任）",
     "start_date": "2021-07", "end_date": "2025-03",
     "rank": "正处级", "note": "2021-07当选新乐市长；2025-03辞职，由葛利强代理/接任"},
    # 张桂英 — 市委副书记
    {"person_id": 14, "org_id": 1, "title": "新乐市委副书记",
     "start_date": "2026?", "end_date": "present",
     "rank": "副处级/正处级", "note": "2026-07-30以市委副书记身份出席（河北美术学院校地合作）"},
    # 郄静 — 市委副书记
    {"person_id": 15, "org_id": 1, "title": "新乐市委副书记",
     "start_date": "2026?", "end_date": "present",
     "rank": "副处级/正处级", "note": "2026-05-07市委十一届十一次全会未书记作说明"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 卢占军 ↔ 葛利强 — 党政搭档（书记/市长）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "新乐市委书记与市长党政搭档（2026年在任）",
     "overlap_org": "市委/市政府", "overlap_period": "2026-present"},
    # 李明政 → 卢占军 — 前任书记继任
    {"person_a": 11, "person_b": 1, "type": "predecessor_successor",
     "context": "李明政(前任新乐书记)→卢占军接任（2026年7月交接）",
     "overlap_org": "中共新乐市委员会", "overlap_period": "2025-2026"},
    # 宫世友 → 葛利强 — 前任市长继任
    {"person_a": 13, "person_b": 2, "type": "predecessor_successor",
     "context": "宫世友(前任新乐市长)→葛利强代理并当选接任（2025-03）",
     "overlap_org": "新乐市人民政府", "overlap_period": "2025"},
    # 卢占军 — 跨县交流（平山→赞皇→新乐）
    {"person_a": 1, "person_b": 2, "type": "other",
     "context": "卢占军在石家庄域内跨县调动（平山县委副书记→赞皇县长→新乐市委书记）与葛利强（市委组织部→新乐）.",
     "overlap_org": "石家庄市辖县区", "overlap_period": "2021-2026"},
    # 葛利强 ↔ 李浩田 — 市政府班子
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "市政府领导班子（市长/常务副市长/副市长）",
     "overlap_org": "新乐市人民政府", "overlap_period": "2026-present"},
    # 葛利强 ↔ 杜威世 — 市长/常务副
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "葛利强协调常务副市长分工（协助分管审计）",
     "overlap_org": "新乐市人民政府", "overlap_period": "2026-present"},
    # 卢占军 ↔ 张桂英 — 书记/副书记
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate",
     "context": "市委书记与市委副书记班子成员",
     "overlap_org": "中共新乐市委员会", "overlap_period": "2026-present"},
]

# =========================================================================
# 5. BUILD
# =========================================================================
if __name__ == "__main__":
    STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(STAGING_DIR, "新乐市_network.db")
    GEXF_PATH = os.path.join(STAGING_DIR, "新乐市_network.gexf")

    run_build(
        slug="新乐市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("Build complete.")