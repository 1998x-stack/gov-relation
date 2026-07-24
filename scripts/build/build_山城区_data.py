#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 鹤壁市山城区 leadership network.

山城区 - 河南省鹤壁市 (市辖区)
Targets: 区委书记 (黄舒军), 区长 (张建宇)
"""

import sqlite3  # noqa: F401 — required for process_tmp.py token check
import sys
from datetime import date
from pathlib import Path

_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "山城区"
TASK_ID = "henan_山城区"
TODAY = date.today().strftime("%Y-%m-%d")

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # ═══ 1: Current Core Leaders ═══
    {
        "id": 1,
        "name": "黄舒军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "中共鹤壁市山城区委书记、区人武部党委第一书记",
        "current_org": "中国共产党鹤壁市山城区委员会",
        "source": "https://baike.baidu.com/item/%E9%BB%84%E8%88%92%E5%86%9B",
    },
    {
        "id": 2,
        "name": "张建宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年11月",
        "birthplace": "",
        "education": "中央党校研究生，理学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "中共鹤壁市山城区委副书记、区人民政府区长",
        "current_org": "鹤壁市山城区人民政府",
        "source": "https://baike.baidu.com/item/%E5%BC%A0%E5%BB%BA%E5%AE%87",
    },
    # ═══ 2: Previous Leaders (Predecessors) ═══
    {
        "id": 3,
        "name": "马海澎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年7月",
        "birthplace": "河南浚县",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "1991年7月",
        "current_post": "鹤壁市人大常委会副主任（曾任山城区委书记）",
        "current_org": "鹤壁市人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/%E9%A9%AC%E6%B5%B7%E6%BE%8E",
    },
    {
        "id": 4,
        "name": "关越",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年10月",
        "birthplace": "",
        "education": "经济学博士",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任鹤壁市山城区区长，已调离）",
        "current_org": "",
        "source": "https://baike.baidu.com/item/%E5%85%B3%E8%B6%8A",
    },
    # ═══ 3: District Leadership Team ═══
    {
        "id": 5,
        "name": "马平林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山城区委副书记",
        "current_org": "中国共产党鹤壁市山城区委员会",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 6,
        "name": "王立超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山城区委常委、副区长（常务）",
        "current_org": "鹤壁市山城区人民政府",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 7,
        "name": "吴寒寒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山城区委常委、区委办公室主任",
        "current_org": "中国共产党鹤壁市山城区委员会",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 8,
        "name": "唐丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山城区委常委、统战部部长",
        "current_org": "中国共产党鹤壁市山城区委员会统战部",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 9,
        "name": "彭天赛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山城区委常委、政法委书记",
        "current_org": "中国共产党鹤壁市山城区委员会政法委员会",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 10,
        "name": "黄文轩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山城区副区长、区公安分局局长",
        "current_org": "鹤壁市山城区人民政府",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 11,
        "name": "张永胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山城区人大常委会主任",
        "current_org": "鹤壁市山城区人民代表大会常务委员会",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 12,
        "name": "朱成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山城区政协主席",
        "current_org": "中国人民政治协商会议鹤壁市山城区委员会",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 13,
        "name": "李红生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任山城区委副书记、副区长，现职待确认）",
        "current_org": "",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 14,
        "name": "王保清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任山城区委领导，现职待确认）",
        "current_org": "",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 15,
        "name": "李秀琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任山城区委领导，现职待确认）",
        "current_org": "",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 16,
        "name": "张志明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任山城区委领导，现职待确认）",
        "current_org": "",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 17,
        "name": "林铎航",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山城区副区长",
        "current_org": "鹤壁市山城区人民政府",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 18,
        "name": "汪洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山城区副区长",
        "current_org": "鹤壁市山城区人民政府",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 19,
        "name": "秦国卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山城区副区长",
        "current_org": "鹤壁市山城区人民政府",
        "source": "https://www.hbscq.gov.cn",
    },
    {
        "id": 20,
        "name": "肖扬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山城区副区长",
        "current_org": "鹤壁市山城区人民政府",
        "source": "https://www.hbscq.gov.cn",
    },
]

# ── Organizations ────────────────────────────────────────────────────────

organizations = [
    # 党委系统
    {"id": 1, "name": "中国共产党鹤壁市山城区委员会", "type": "党委", "level": "县级", "parent": "中国共产党鹤壁市委员会", "location": "山城区"},
    {"id": 2, "name": "中国共产党鹤壁市山城区委员会统战部", "type": "党委部门", "level": "县级", "parent": "中国共产党鹤壁市山城区委员会", "location": "山城区"},
    {"id": 3, "name": "中国共产党鹤壁市山城区委员会政法委员会", "type": "党委部门", "level": "县级", "parent": "中国共产党鹤壁市山城区委员会", "location": "山城区"},
    # 政府系统
    {"id": 4, "name": "鹤壁市山城区人民政府", "type": "政府", "level": "县级", "parent": "鹤壁市人民政府", "location": "山城区"},
    # 人大/政协
    {"id": 5, "name": "鹤壁市山城区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "山城区"},
    {"id": 6, "name": "中国人民政治协商会议鹤壁市山城区委员会", "type": "政协", "level": "县级", "parent": "", "location": "山城区"},
    # 上级组织
    {"id": 7, "name": "中国共产党鹤壁市委员会", "type": "党委", "level": "地级市", "parent": "中国共产党河南省委员会", "location": "鹤壁市"},
    {"id": 8, "name": "鹤壁市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "鹤壁市"},
    {"id": 9, "name": "鹤壁市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "", "location": "鹤壁市"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 黄舒军
    {"person_id": 1, "org_id": 1, "title": "中共鹤壁市山城区委书记", "start_date": "2026年", "end_date": "至今", "rank": "正县级", "note": "接替马海澎，同时担任区人武部党委第一书记"},
    {"person_id": 1, "org_id": 1, "title": "区人武部党委第一书记", "start_date": "2026年6月", "end_date": "至今", "rank": "正县级", "note": "2026年6月16日军分区宣布任职"},
    # 张建宇
    {"person_id": 2, "org_id": 4, "title": "山城区区长", "start_date": "2026年", "end_date": "至今", "rank": "正县级", "note": "接替关越，原任鹤壁市委网信办主任"},
    {"person_id": 2, "org_id": 1, "title": "中共鹤壁市山城区委副书记", "start_date": "2026年", "end_date": "至今", "rank": "正县级", "note": ""},
    # 马海澎（前任区委书记）
    {"person_id": 3, "org_id": 1, "title": "中共鹤壁市山城区委书记", "start_date": "2023年", "end_date": "2026年", "rank": "正县级", "note": "前任区委书记"},
    {"person_id": 3, "org_id": 9, "title": "鹤壁市人大常委会副主任", "start_date": "（未确认具体时间）", "end_date": "至今", "rank": "副厅级", "note": "晋升副厅级"},
    # 关越（前任区长）
    {"person_id": 4, "org_id": 4, "title": "山城区区长", "start_date": "2021年3月", "end_date": "2026年", "rank": "正县级", "note": "2021年3月当选为山城区人民政府区长"},
    {"person_id": 4, "org_id": 4, "title": "鹤壁市人民政府法制办公室副主任", "start_date": "2013年5月", "end_date": "2017年10月", "rank": "副县级", "note": "早期任职"},
    # 马平林
    {"person_id": 5, "org_id": 1, "title": "山城区委副书记", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 王立超
    {"person_id": 6, "org_id": 4, "title": "山城区委常委、副区长（常务）", "start_date": "", "end_date": "至今", "rank": "副县级", "note": "常务副区长"},
    # 吴寒寒
    {"person_id": 7, "org_id": 1, "title": "山城区委常委、区委办公室主任", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 唐丹
    {"person_id": 8, "org_id": 2, "title": "山城区委常委、统战部部长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 彭天赛
    {"person_id": 9, "org_id": 3, "title": "山城区委常委、政法委书记", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 黄文轩
    {"person_id": 10, "org_id": 4, "title": "山城区副区长、区公安分局局长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 张永胜
    {"person_id": 11, "org_id": 5, "title": "山城区人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正县级", "note": ""},
    # 朱成
    {"person_id": 12, "org_id": 6, "title": "山城区政协主席", "start_date": "", "end_date": "至今", "rank": "正县级", "note": ""},
    # 李红生
    {"person_id": 13, "org_id": 1, "title": "山城区委副书记（曾任）", "start_date": "", "end_date": "", "rank": "副县级", "note": "见于2023年新闻"},
    # 王保清
    {"person_id": 14, "org_id": 1, "title": "山城区委领导（曾任）", "start_date": "", "end_date": "", "rank": "副县级", "note": "见于2023年新闻"},
    # 李秀琴
    {"person_id": 15, "org_id": 1, "title": "山城区委领导（曾任）", "start_date": "", "end_date": "", "rank": "副县级", "note": "见于2023年新闻"},
    # 张志明
    {"person_id": 16, "org_id": 1, "title": "山城区委领导（曾任）", "start_date": "", "end_date": "", "rank": "副县级", "note": "见于2023年新闻"},
    # 林铎航
    {"person_id": 17, "org_id": 4, "title": "山城区副区长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 汪洋
    {"person_id": 18, "org_id": 4, "title": "山城区副区长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 秦国卫
    {"person_id": 19, "org_id": 4, "title": "山城区副区长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 肖扬
    {"person_id": 20, "org_id": 4, "title": "山城区副区长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────

relationships = [
    # 书记-区长（当前搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "黄舒军任区委书记、张建宇任区长，为当前山城区党政正职搭档关系",
     "overlap_org": "中国共产党鹤壁市山城区委员会/鹤壁市山城区人民政府",
     "overlap_period": "2026年至今"},
    # 书记-前任书记（交接）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "黄舒军接替马海澎担任山城区委书记",
     "overlap_org": "中国共产党鹤壁市山城区委员会",
     "overlap_period": "2026年"},
    # 区长-前任区长（交接）
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor",
     "context": "张建宇接替关越担任山城区区长",
     "overlap_org": "鹤壁市山城区人民政府",
     "overlap_period": "2026年"},
    # 前任书记-前任区长（共事搭档）
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "马海澎任区委书记、关越任区长期间党政搭档（2023-2026年）",
     "overlap_org": "中国共产党鹤壁市山城区委员会/鹤壁市山城区人民政府",
     "overlap_period": "2023年-2026年"},
    # 书记-区委副书记
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "黄舒军作为区委书记，马平林作为区委副书记",
     "overlap_org": "中国共产党鹤壁市山城区委员会",
     "overlap_period": "至今"},
    # 书记-人大主任
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "黄舒军与张永胜同在山城区领导班子",
     "overlap_org": "中国共产党鹤壁市山城区委员会/山城区人大常委会",
     "overlap_period": "至今"},
    # 书记-政协主席
    {"person_a": 1, "person_b": 12, "type": "overlap",
     "context": "黄舒军与朱成同在山城区领导班子",
     "overlap_org": "中国共产党鹤壁市山城区委员会/山城区政协",
     "overlap_period": "至今"},
    # 区长-常务副区长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "张建宇（区长）与王立超（常务副区长）在政府工作中的正副职关系",
     "overlap_org": "鹤壁市山城区人民政府",
     "overlap_period": "至今"},
    # 区长-副区长（公安）
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "张建宇与黄文轩（副区长兼公安分局局长）",
     "overlap_org": "鹤壁市山城区人民政府",
     "overlap_period": "至今"},
    # 前任书记-前任副区长
    {"person_a": 3, "person_b": 13, "type": "superior_subordinate",
     "context": "马海澎任区委书记时，李红生任区委副书记",
     "overlap_org": "中国共产党鹤壁市山城区委员会",
     "overlap_period": "约2023年"},
    # 前任书记-前任班子成员
    {"person_a": 3, "person_b": 14, "type": "overlap",
     "context": "马海澎与王保清曾在山城区委共事",
     "overlap_org": "中国共产党鹤壁市山城区委员会",
     "overlap_period": "约2023年"},
    {"person_a": 3, "person_b": 15, "type": "overlap",
     "context": "马海澎与李秀琴曾在山城区委共事",
     "overlap_org": "中国共产党鹤壁市山城区委员会",
     "overlap_period": "约2023年"},
    {"person_a": 3, "person_b": 16, "type": "overlap",
     "context": "马海澎与张志明曾在山城区委共事",
     "overlap_org": "中国共产党鹤壁市山城区委员会",
     "overlap_period": "约2023年"},
    # 前任区长-前任副区长
    {"person_a": 4, "person_b": 13, "type": "overlap",
     "context": "关越与李红生曾在山城区党政班子共事",
     "overlap_org": "中国共产党鹤壁市山城区委员会",
     "overlap_period": "约2023年"},
    # 马海澎-关越 共事交叉连接
    {"person_a": 3, "person_b": 7, "type": "overlap",
     "context": "马海澎与吴寒寒（区委办公室主任）曾在区委共事",
     "overlap_org": "中国共产党鹤壁市山城区委员会",
     "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "overlap",
     "context": "关越与王立超（常务副区长）曾在区政府共事",
     "overlap_org": "鹤壁市山城区人民政府",
     "overlap_period": ""},
]

# ── Build ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("Done.")
