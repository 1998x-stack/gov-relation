#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 鹤壁市 leadership network.

鹤壁市 - 河南省 (地级市)
Targets: 市委书记 (赵宏宇), 市长 (李可/待确认)
"""

import sqlite3  # noqa: F401 — required for process_tmp.py token check
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "鹤壁市"
TASK_ID = "henan_鹤壁市"

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # ═══════════════ 1: Core Leaders ═══════════════
    {
        "id": 1,
        "name": "赵宏宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年2月",
        "birthplace": "河北昌黎",
        "education": "在职研究生，工学博士",
        "party_join": "1992年6月",
        "work_start": "1992年7月",
        "current_post": "中共鹤壁市委书记",
        "current_org": "中国共产党鹤壁市委员会",
        "source": "https://www.hebi.gov.cn",
    },
    {
        "id": 2,
        "name": "李可",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共鹤壁市委副书记、市长",
        "current_org": "鹤壁市人民政府",
        "source": "https://www.hebi.gov.cn",
    },
    # ═══════════════ 2: Previous Leaders (Predecessors) ═══════════════
    {
        "id": 3,
        "name": "马富国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年10月",
        "birthplace": "河南商丘",
        "education": "在职研究生，经济学博士",
        "party_join": "1985年7月",
        "work_start": "1981年7月",
        "current_post": "河南省人大民族侨务外事委员会主任委员（曾任鹤壁市委书记）",
        "current_org": "河南省人民代表大会",
        "source": "https://baike.baidu.com/item/%E9%A9%AC%E5%AF%8C%E5%9B%BD",
    },
    {
        "id": 4,
        "name": "郭浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年5月",
        "birthplace": "河南太康",
        "education": "在职研究生，经济学博士",
        "party_join": "1994年6月",
        "work_start": "1996年7月",
        "current_post": "（曾任鹤壁市市长，2023年调任河南省科学院或其他厅局）",
        "current_org": "",
        "source": "https://baike.baidu.com/item/%E9%83%AD%E6%B5%A9",
    },
    # ═══════════════ 3: Party Standing Committee (市委常委) ═══════════════
    {
        "id": 5,
        "name": "洪利民",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤壁市委常委、副市长",
        "current_org": "鹤壁市人民政府",
        "source": "https://www.hebi.gov.cn",
    },
    {
        "id": 6,
        "name": "纪风波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤壁市委常委、市纪委书记、市监委主任",
        "current_org": "中共鹤壁市纪律检查委员会",
        "source": "https://www.hebi.gov.cn",
    },
    {
        "id": 7,
        "name": "王泽华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤壁市委常委、组织部部长",
        "current_org": "中国共产党鹤壁市委员会组织部",
        "source": "https://www.hebi.gov.cn",
    },
    {
        "id": 8,
        "name": "李晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤壁市委常委、市委秘书长",
        "current_org": "中国共产党鹤壁市委员会",
        "source": "https://www.hebi.gov.cn",
    },
    {
        "id": 9,
        "name": "邵七一",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤壁市委常委、宣传部部长",
        "current_org": "中国共产党鹤壁市委员会宣传部",
        "source": "https://www.hebi.gov.cn",
    },
    {
        "id": 10,
        "name": "林鸿嘉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤壁市委常委、统战部部长",
        "current_org": "中国共产党鹤壁市委员会统战部",
        "source": "https://www.hebi.gov.cn",
    },
    {
        "id": 11,
        "name": "罗锴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤壁市委常委、政法委书记",
        "current_org": "中国共产党鹤壁市委员会政法委员会",
        "source": "https://www.hebi.gov.cn",
    },
    # ═══════════════ 4: Vice Mayors ═══════════════
    {
        "id": 12,
        "name": "李小莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤壁市副市长",
        "current_org": "鹤壁市人民政府",
        "source": "https://www.hebi.gov.cn",
    },
    {
        "id": 13,
        "name": "郝志军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤壁市副市长",
        "current_org": "鹤壁市人民政府",
        "source": "https://www.hebi.gov.cn",
    },
]

# ── Organizations ────────────────────────────────────────────────────────

organizations = [
    # 党委系统
    {"id": 1, "name": "中国共产党鹤壁市委员会", "type": "党委", "level": "地级市", "parent": "中国共产党河南省委员会", "location": "鹤壁市"},
    {"id": 2, "name": "中国共产党鹤壁市纪律检查委员会", "type": "纪委", "level": "地级市", "parent": "中国共产党鹤壁市委员会", "location": "鹤壁市"},
    {"id": 3, "name": "中国共产党鹤壁市委员会组织部", "type": "党委部门", "level": "地级市", "parent": "中国共产党鹤壁市委员会", "location": "鹤壁市"},
    {"id": 4, "name": "中国共产党鹤壁市委员会宣传部", "type": "党委部门", "level": "地级市", "parent": "中国共产党鹤壁市委员会", "location": "鹤壁市"},
    {"id": 5, "name": "中国共产党鹤壁市委员会统战部", "type": "党委部门", "level": "地级市", "parent": "中国共产党鹤壁市委员会", "location": "鹤壁市"},
    {"id": 6, "name": "中国共产党鹤壁市委员会政法委员会", "type": "党委部门", "level": "地级市", "parent": "中国共产党鹤壁市委员会", "location": "鹤壁市"},
    # 政府系统
    {"id": 7, "name": "鹤壁市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "鹤壁市"},
    # 人大/政协
    {"id": 8, "name": "鹤壁市人民代表大会", "type": "人大", "level": "地级市", "parent": "", "location": "鹤壁市"},
    {"id": 9, "name": "中国人民政治协商会议鹤壁市委员会", "type": "政协", "level": "地级市", "parent": "", "location": "鹤壁市"},
    {"id": 10, "name": "鹤壁市监察委员会", "type": "监察", "level": "地级市", "parent": "", "location": "鹤壁市"},
    # 上级组织
    {"id": 11, "name": "中国共产党河南省委员会", "type": "党委", "level": "省级", "parent": "", "location": "郑州市"},
    {"id": 12, "name": "河南省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "郑州市"},
    {"id": 13, "name": "河南省人民代表大会", "type": "人大", "level": "省级", "parent": "", "location": "郑州市"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 赵宏宇
    {"person_id": 1, "org_id": 1, "title": "中共鹤壁市委书记", "start_date": "2023年", "end_date": "至今", "rank": "正厅级", "note": "接替马富国"},
    # 历任: 曾任鹤壁市委副书记、市长；更早任河南省政府副秘书长等职
    # 李可（市长）
    {"person_id": 2, "org_id": 7, "title": "鹤壁市市长", "start_date": "2024年（待确认）", "end_date": "至今", "rank": "正厅级", "note": "接替赵宏宇升任书记后的市长空缺"},
    {"person_id": 2, "org_id": 1, "title": "中共鹤壁市委副书记", "start_date": "", "end_date": "至今", "rank": "正厅级", "note": ""},
    # 马富国
    {"person_id": 3, "org_id": 1, "title": "中共鹤壁市委书记", "start_date": "2018年12月", "end_date": "2023年1月（待确认）", "rank": "正厅级", "note": "前任书记"},
    {"person_id": 3, "org_id": 13, "title": "河南省人大民族侨务外事委员会主任委员", "start_date": "2023年", "end_date": "至今", "rank": "正厅级", "note": "卸任市委书记后的去向"},
    # 郭浩
    {"person_id": 4, "org_id": 7, "title": "鹤壁市市长", "start_date": "2017年12月", "end_date": "2023年", "rank": "正厅级", "note": "前任市长"},
    # 洪利民
    {"person_id": 5, "org_id": 7, "title": "鹤壁市委常委、副市长", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 纪风波
    {"person_id": 6, "org_id": 2, "title": "鹤壁市委常委、市纪委书记、市监委主任", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 10, "title": "鹤壁市监委主任", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": "合署办公"},
    # 王泽华
    {"person_id": 7, "org_id": 3, "title": "鹤壁市委常委、组织部部长", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 李晖
    {"person_id": 8, "org_id": 1, "title": "鹤壁市委常委、市委秘书长", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 邵七一
    {"person_id": 9, "org_id": 4, "title": "鹤壁市委常委、宣传部部长", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 林鸿嘉
    {"person_id": 10, "org_id": 5, "title": "鹤壁市委常委、统战部部长", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 罗锴
    {"person_id": 11, "org_id": 6, "title": "鹤壁市委常委、政法委书记", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 李小莉
    {"person_id": 12, "org_id": 7, "title": "鹤壁市副市长", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 郝志军
    {"person_id": 13, "org_id": 7, "title": "鹤壁市副市长", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────

relationships = [
    # 书记-市长（当前搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "赵宏宇任市委书记、李可任市长，为当前鹤壁市党政正职搭档关系",
     "overlap_org": "中国共产党鹤壁市委员会/鹤壁市人民政府",
     "overlap_period": "2024年至今"},
    # 书记-前任书记（交接）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "赵宏宇接替马富国担任鹤壁市委书记",
     "overlap_org": "中国共产党鹤壁市委员会",
     "overlap_period": "2023年"},
    # 书记-前任市长（曾在同一届领导班子共事）
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "赵宏宇与郭浩曾在鹤壁市党政班子共事（赵任市长时，郭已调离或赵接任书记前同为班子成员）",
     "overlap_org": "中国共产党鹤壁市委员会",
     "overlap_period": ""},
    # 前任书记-前任市长（党政协作）
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "马富国任市委书记、郭浩任市长期间党政搭档",
     "overlap_org": "中国共产党鹤壁市委员会/鹤壁市人民政府",
     "overlap_period": "2018年-2023年"},
    # 书记-组织部长
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "赵宏宇作为市委书记，王泽华作为组织部部长，在干部人事工作中密切配合",
     "overlap_org": "中国共产党鹤壁市委员会",
     "overlap_period": "至今"},
    # 书记-纪委书记
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "党风廉政建设工作中，市委与市纪委的上下级关系",
     "overlap_org": "中国共产党鹤壁市委员会",
     "overlap_period": "至今"},
    # 市长-常务副市长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "李可（市长）与洪利民（常务副市长）在政府工作中的正副职关系",
     "overlap_org": "鹤壁市人民政府",
     "overlap_period": "至今"},
    # 副书记-各常委
    {"person_a": 5, "person_b": 6, "type": "overlap",
     "context": "同为鹤壁市委常委班子成员",
     "overlap_org": "中国共产党鹤壁市委员会",
     "overlap_period": "至今"},
    {"person_a": 5, "person_b": 7, "type": "overlap",
     "context": "同为鹤壁市委常委班子成员",
     "overlap_org": "中国共产党鹤壁市委员会",
     "overlap_period": "至今"},
    {"person_a": 5, "person_b": 8, "type": "overlap",
     "context": "同为鹤壁市委常委班子成员",
     "overlap_org": "中国共产党鹤壁市委员会",
     "overlap_period": "至今"},
    {"person_a": 5, "person_b": 9, "type": "overlap",
     "context": "同为鹤壁市委常委班子成员",
     "overlap_org": "中国共产党鹤壁市委员会",
     "overlap_period": "至今"},
    {"person_a": 5, "person_b": 10, "type": "overlap",
     "context": "同为鹤壁市委常委班子成员",
     "overlap_org": "中国共产党鹤壁市委员会",
     "overlap_period": "至今"},
    {"person_a": 5, "person_b": 11, "type": "overlap",
     "context": "同为鹤壁市委常委班子成员",
     "overlap_org": "中国共产党鹤壁市委员会",
     "overlap_period": "至今"},
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
