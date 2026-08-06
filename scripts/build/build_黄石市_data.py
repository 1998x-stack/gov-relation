#!/usr/bin/env python3
"""Build script for 黄石市 (Huangshi) cadre leadership network.

Task: hubei_黄石市 — targets 市委书记 & 市长 (prefecture-level city, 湖北省).
As-of date: 2026-08-06.

Key sources:
- 黄石市人民政府门户 https://www.huangshi.gov.cn/ (official; current roster via 黄石要闻/人大/政协 news 2026-07-30~08-06)
- 黄石日报 (source of the news items) — names: 吴之凌(市长)、刘润长(副书记)、俞远汉(人大主任)、何运平(政协主席)、副市长 黄志勇/徐丹娅/晏勇、市政府秘书长 邓斌
- 市委书记 identity: 郄英才 (appointed 2021-06; background research agent) — see CONFIDENCE NOTES.

CONFIDENCE NOTES
- 吴之凌 = 现任黄石市长/市委副书记 (confirmed: official portal 2026-07-30 主持市政府第116次常务会议; 2026-07-31 双拥/安全生产会议)
- 刘润长 = 现任市委副书记、市政府党组副书记 (confirmed: 2026-07-31)
- 俞远汉 = 现任市人大常委会党组书记、主任 (confirmed: 2026-07-30)
- 何运平 = 现任市政协党组书记、主席 (confirmed: 2026-07-30)
- 黄志勇、徐丹娅、晏勇 = 副市长; 邓斌 = 市政府秘书长 (confirmed: 2026-07-31)
- 郄英才 = 现任黄石市委书记 (appointed 2021-06) — 待最终外源确认; 具体任免日期及此前任职去向 = OPEN 待核
- 前任黄石市委书记(郄英才之前)身份及去向 = OPEN 待核
- 各核心人物出生日期、籍贯、教育、任免精确日期大多待核 (见 person JSON open_questions)
"""

import sqlite3
import sys
from pathlib import Path

# Locate repo root (holds gov_relation/) robustly across staging/scripts/build/root locations.
_root = Path(__file__).resolve()
while not (_root / "gov_relation").is_dir() and _root != _root.parent:
    _root = _root.parent
sys.path.insert(0, str(_root))

from gov_relation.runner import run_build

AS_OF = "2026-08-06"
SLUG = "黄石市"

TMP = Path(__file__).resolve().parent
DB_PATH = TMP / "黄石市_network.db"
GEXF_PATH = TMP / "黄石市_network.gexf"

persons = [
    # ── 现任 党委 ──
    {
        "id": 10,
        "name": "郄英才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄石市委书记",
        "current_org": "中共黄石市委员会",
        "source": "http://hb.china.com.cn/2025-02/19/content_43031742.htm",
    },
    {
        "id": 11,
        "name": "吴之凌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄石市委副书记、市长",
        "current_org": "黄石市人民政府",
        "source": "https://www.huangshi.gov.cn/xwdt/hsyw/202607/t20260730_1346796.html",
    },
    {
        "id": 12,
        "name": "刘润长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄石市委副书记、常务副市长",
        "current_org": "黄石市人民政府",
        "source": "https://www.huangshi.gov.cn/xwdt/hsyw/202607/t20260731_1347178.html",
    },
    {
        "id": 21,
        "name": "李文波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄石市委常委、政法委书记",
        "current_org": "中共黄石市委员会",
        "source": "http://hb.china.com.cn/2025-02/17/content_42955963.html",
    },
    {
        "id": 22,
        "name": "郭宝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄石市副市长",
        "current_org": "黄石市人民政府",
        "source": "https://www.huangshi.gov.cn/",
    },
    {
        "id": 23,
        "name": "严荣勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄石市人大常委会秘书长",
        "current_org": "黄石市人大常委会",
        "source": "https://www.huangshi.gov.cn/xwdt/hsyw/202607/t20260730_1346797.html",
    },
    {
        "id": 24,
        "name": "闫树",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄石市政府党组成员",
        "current_org": "黄石市人民政府",
        "source": "https://www.huangshi.gov.cn/",
    },
    # ── 现任 市人大 ──
    {
        "id": 13,
        "name": "俞远汉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄石市人大常委会党组书记、主任",
        "current_org": "黄石市人大常委会",
        "source": "https://www.huangshi.gov.cn/xwdt/hsyw/202607/t20260730_1346797.html",
    },
    # ── 现任 政协 ──
    {
        "id": 14,
        "name": "何运平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄石市政协党组书记、主席",
        "current_org": "政协黄石市委员会",
        "source": "https://www.huangshi.gov.cn/xwdt/hsyw/202607/t20260730_1346799.html",
    },
    {
        "id": 15,
        "name": "汪岚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄石市政协党组副书记、副主席",
        "current_org": "政协黄石市委员会",
        "source": "https://www.huangshi.gov.cn/xwdt/hsyw/202607/t20260730_1346799.html",
    },
    # ── 现任 市政府 班子 ──
    {
        "id": 16,
        "name": "黄志勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄石市副市长",
        "current_org": "黄石市人民政府",
        "source": "https://www.huangshi.gov.cn/xwdt/hsyw/202607/t20260731_1347183.html",
    },
    {
        "id": 17,
        "name": "徐丹娅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄石市副市长",
        "current_org": "黄石市人民政府",
        "source": "https://www.huangshi.gov.cn/xwdt/hsyw/202607/t20260731_1347178.html",
    },
    {
        "id": 18,
        "name": "晏勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄石市副市长",
        "current_org": "黄石市人民政府",
        "source": "https://www.huangshi.gov.cn/xwdt/hsyw/202607/t20260731_1347183.html",
    },
    {
        "id": 19,
        "name": "邓斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄石市政府秘书长",
        "current_org": "黄石市人民政府",
        "source": "https://www.huangshi.gov.cn/xwdt/hsyw/202607/t20260731_1347178.html",
    },
    # ── 前任 ──
    {
        "id": 20,
        "name": "（前任市委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任黄石市委书记",
        "current_org": "中共黄石市委员会",
        "source": "",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共黄石市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党湖北省委员会",
        "location": "黄石市",
    },
    {
        "id": 2,
        "name": "黄石市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "湖北省人民政府",
        "location": "黄石市",
    },
    {
        "id": 3,
        "name": "黄石市人大常委会",
        "type": "人大",
        "level": "地级市",
        "parent": "中国共产党黄石市委员会",
        "location": "黄石市",
    },
    {
        "id": 4,
        "name": "政协黄石市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "中国共产党黄石市委员会",
        "location": "黄石市",
    },
    {
        "id": 5,
        "name": "中国共产党湖北省委员会",
        "type": "党委",
        "level": "省级",
        "parent": "",
        "location": "武汉市",
    },
    {
        "id": 6,
        "name": "湖北省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "武汉市",
    },
]

positions = [
    # ── 市委书记 ──
    {"person_id": 10, "org_id": 1, "title": "黄石市委书记", "start_date": "2021", "end_date": "present", "rank": "正厅级", "note": "现任; 具体任命日期待核"},
    # ── 市长 ──
    {"person_id": 11, "org_id": 2, "title": "黄石市委副书记、市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "现任; 2026-07主持市政府常务会议"},
    {"person_id": 11, "org_id": 1, "title": "黄石市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼任市委副书记"},
    # ── 副书记/常务副市长 ──
    {"person_id": 12, "org_id": 1, "title": "黄石市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼任市政府党组副书记"},
    {"person_id": 12, "org_id": 2, "title": "黄石市常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "副市长(常务) 请注意系政府序列"},
    # ── 市委常委/政法委书记 ──
    {"person_id": 21, "org_id": 1, "title": "黄石市委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "2025-02报道确认"},
    # ── 政府党组成员 ──
    {"person_id": 24, "org_id": 2, "title": "黄石市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # ── 人大 ──
    {"person_id": 13, "org_id": 3, "title": "黄石市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "党组书记"},
    # ── 政协 ──
    {"person_id": 14, "org_id": 4, "title": "黄石市政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "党组书记"},
    {"person_id": 15, "org_id": 4, "title": "黄石市政协副主席", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "党组副书记"},
    # ── 市政府班子 ──
    {"person_id": 16, "org_id": 2, "title": "黄石市副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "黄石市副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "黄石市副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 22, "org_id": 2, "title": "黄石市副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 24, "org_id": 2, "title": "黄石市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 23, "org_id": 3, "title": "黄石市人大常委会秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "黄石市政府秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # ── 前任市委书记 ──
    {"person_id": 20, "org_id": 1, "title": "黄石市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任; 具体身份/去向待核"},
]

relationships = [
    # 党政一把手搭档
    {"person_a": 10, "person_b": 11, "type": "党政搭档",
     "context": "郄英才（市委书记）与吴之凌（市委副书记、市长）组成黄石市党政一把手搭档",
     "overlap_org": "中共黄石市委员会/黄石市人民政府", "overlap_period": "2026至今"},
    # 副书记与市长共事
    {"person_a": 11, "person_b": 12, "type": "superior_subordinate",
     "context": "吴之凌（市长）与刘润长（市委副书记、市政府党组副书记）在市政府班子共事",
     "overlap_org": "中共黄石市委员会/黄石市人民政府", "overlap_period": "2026至今"},
    # 书记与人大/政协
    {"person_a": 10, "person_b": 13, "type": "superior_subordinate",
     "context": "黄石市委书记与市人大常委会主任俞远汉同属市级领导班子",
     "overlap_org": "中共黄石市委员会/黄石市人大常委会", "overlap_period": "2026"},
    {"person_a": 10, "person_b": 14, "type": "superior_subordinate",
     "context": "黄石市委书记与市政协主席何运平同属市级领导班子",
     "overlap_org": "中共黄石市委员会/政协黄石市委员会", "overlap_period": "2026"},
    # 市政府班子内部
    {"person_a": 11, "person_b": 16, "type": "superior_subordinate",
     "context": "市长吴之凌与副市长黄志勇在市政府班子共事",
     "overlap_org": "黄石市人民政府", "overlap_period": "2026"},
    {"person_a": 11, "person_b": 17, "type": "superior_subordinate",
     "context": "市长吴之凌与副市长徐丹娅在市政府班子共事",
     "overlap_org": "黄石市人民政府", "overlap_period": "2026"},
    {"person_a": 11, "person_b": 18, "type": "superior_subordinate",
     "context": "市长吴之凌与副市长晏勇在市政府班子共事",
     "overlap_org": "黄石市人民政府", "overlap_period": "2026"},
    {"person_a": 11, "person_b": 22, "type": "superior_subordinate",
     "context": "市长吴之凌与副市长郭宝在市政府班子共事",
     "overlap_org": "黄石市人民政府", "overlap_period": "2026"},
    {"person_a": 11, "person_b": 24, "type": "superior_subordinate",
     "context": "市长吴之凌与市政府党组成员闫树在市政府班子共事",
     "overlap_org": "黄石市人民政府", "overlap_period": "2026"},
    {"person_a": 10, "person_b": 21, "type": "superior_subordinate",
     "context": "市委书记郄英才与市委常委、政法委书记李文波同属市委常委会",
     "overlap_org": "中共黄石市委员会", "overlap_period": "2025-2026"},
    {"person_a": 10, "person_b": 12, "type": "superior_subordinate",
     "context": "市委书记与市委副书记刘润长在市委常委会共事",
     "overlap_org": "中共黄石市委员会", "overlap_period": "2026"},
    {"person_a": 13, "person_b": 23, "type": "superior_subordinate",
     "context": "市人大常委会主任俞远汉与其秘书长严荣勇共事",
     "overlap_org": "黄石市人大常委会", "overlap_period": "2026"},
    # 书记继任链
    {"person_a": 10, "person_b": 20, "type": "predecessor_successor",
     "context": "郄英才接任前任黄石市委书记（继任链，具体前任身份待核）",
     "overlap_org": "中共黄石市委员会", "overlap_period": "2021"},
    # 省级关系
    {"person_a": 10, "person_b": 13, "type": "same_system",
     "context": "市级领导班子成员均受湖北省委/黄石市委统一领导",
     "overlap_org": "中国共产党湖北省委员会", "overlap_period": ""},
]

if __name__ == "__main__":
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
    conn = sqlite3.connect(str(DB_PATH))
    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("persons", "organizations", "positions", "relationships")}
    conn.close()
    print(f"Built {DB_PATH} and {GEXF_PATH}")
    print(f"persons={len(persons)} orgs={len(organizations)} positions={len(positions)} relationships={len(relationships)}")
    print("DB counts:", counts)