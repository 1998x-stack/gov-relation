#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 同心县 (Tongxin County), 吴忠市, 宁夏回族自治区.

Task ID: ningxia_同心县
Level: 县
Targets: 县委书记 (一把手) & 县长 (二把手)

Investigation date: 2026-08-07

Research confidence notes:
  - Current (2026) leadership roster confirmed via 同心县人民政府官网 领导之窗
    (https://www.tongxin.gov.cn/zwgk/ldzc/) — primary official source.
  - 县委书记 陈华, 县长 虎玉宝 confirmed current as of 2026 (陈华 appointed 2024-12-31;
    虎玉宝 elected 2025-01-07).
  - Career timelines for county-level leaders are thin; only basic bio + confirmed
    appointment anchors available for most. Marked with confidence levels.
  - Predecessor/successor moves confirmed via 宁夏区委组织部任前公示 + official announcements.
  - Some ethnicity/education fields for minority-roster deputies are unverified; flagged.
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Allow import when run from repository root or staging dir
_here = Path(__file__).resolve().parent
# Support both staging (data/tmp/<task>/build_X_data.py) and canonical (repo root) locations
for _ancestor in (Path(__file__).resolve(), *_here.parents):
    if (_ancestor / "gov_relation").is_dir():
        sys.path.insert(0, str(_ancestor))
        break

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

TODAY = datetime.now().strftime("%Y-%m-%d")
AS_OF = "2026-08-07"
SLUG = "同心县"
PROVINCE = "宁夏回族自治区"
PARENT_CITY = "吴忠市"
LEVEL = "县"

# Staging paths (this script lives in data/tmp/...; use its own dir)
TMP = Path(__file__).parent.resolve()
DB_PATH = TMP / f"{SLUG}_network.db"
GEXF_PATH = TMP / f"{SLUG}_network.gexf"

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共同心县委员会", "type": "党委", "level": "县", "parent": "吴忠市委", "location": "宁夏同心县"},
    {"id": 2, "name": "同心县人民政府", "type": "政府", "level": "县", "parent": "吴忠市人民政府", "location": "宁夏同心县"},
    {"id": 3, "name": "同心县人大常委会", "type": "人大", "level": "县", "parent": "吴忠市人大", "location": "宁夏同心县"},
    {"id": 4, "name": "中国人民政治协商会议同心县委员会", "type": "政协", "level": "县", "parent": "吴忠市政协", "location": "宁夏同心县"},
    {"id": 5, "name": "同心县纪律检查委员会/监委", "type": "纪委", "level": "县", "parent": "吴忠市纪委监委", "location": "宁夏同心县"},
    {"id": 6, "name": "同心县委组织部", "type": "党委部门", "level": "县", "parent": "中共同心县委员会", "location": "宁夏同心县"},
    {"id": 7, "name": "同心县委宣传部", "type": "党委部门", "level": "县", "parent": "中共同心县委员会", "location": "宁夏同心县"},
    {"id": 8, "name": "同心县委统战部", "type": "党委部门", "level": "县", "parent": "中共同心县委员会", "location": "宁夏同心县"},
    {"id": 9, "name": "同心县委政法委", "type": "党委部门", "level": "县", "parent": "中共同心县委员会", "location": "宁夏同心县"},
    {"id": 10, "name": "同心县公安局", "type": "政府部门", "level": "县", "parent": "同心县人民政府", "location": "宁夏同心县"},
    {"id": 11, "name": "同心县人民武装部", "type": "政府部门", "level": "县", "parent": "同心县人民政府", "location": "宁夏同心县"},
    {"id": 12, "name": "宁夏回族自治区财政厅", "type": "省级部门", "level": "省直", "parent": "宁夏回族自治区人民政府", "location": "宁夏银川市"},
    {"id": 13, "name": "宁同县韦州镇", "type": "乡镇", "level": "乡镇", "parent": "同心县", "location": "宁夏同心县"},
    {"id": 14, "name": "吴忠金积工业园区", "type": "开发区", "level": "市园区", "parent": "吴忠市", "location": "宁夏吴忠市"},
    {"id": 15, "name": "宁夏回族自治区发展和改革委员会", "type": "省级部门", "level": "省直", "parent": "宁夏回族自治区人民政府", "location": "宁夏银川市"},
    {"id": 16, "name": "盐池县人民政府", "type": "政府", "level": "县", "parent": "吴忠市人民政府", "location": "宁夏盐池县"},
    {"id": 17, "name": "吴忠市商务和投资促进局", "type": "市级部门", "level": "市", "parent": "吴忠市人民政府", "location": "宁夏吴忠市"},
    {"id": 18, "name": "同心县委办公室", "type": "党委部门", "level": "县", "parent": "中共同心县委员会", "location": "宁夏同心县"},
]

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 core leaders, 3-5 predecessors, 6+ current 班子 members
persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership — 县委书记 & 县长
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "陈华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-08",
        "birthplace": "宁夏盐池",
        "education": "大学（在职大学）",
        "party_join": "中共党员（2000-03）",
        "work_start": "2000-09",
        "current_post": "同心县委书记",
        "current_org": "中共同心县委员会",
        "source": "同心县政府领导之窗; 宁夏区委组织部任前公示(2024年第17号)",
    },
    {
        "id": 2,
        "name": "虎玉宝",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1980-07",
        "birthplace": "",
        "education": "研究生（有公示显示大学）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同心县委副书记、县长",
        "current_org": "同心县人民政府",
        "source": "同心县政府领导之窗; 宁夏区委组织部任前公示(2024年第14号)",
    },
    # Predecessors
    {
        "id": 3,
        "name": "王汉武",
        "gender": "男",
        "ethnicity": "白族",
        "birth": "1974-11",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宁夏回族自治区发展和改革委员会党组书记、主任（原同心县委书记）",
        "current_org": "宁夏回族自治区发展和改革委员会",
        "source": "宁夏区委组织部任前公示(2024年第17号); 新京报",
    },
    {
        "id": 4,
        "name": "杨春燕",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1972-08",
        "birthplace": "",
        "education": "宁夏党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "吴忠市委常委、宣传部部长（原同心县县长）",
        "current_org": "吴忠市委",
        "source": "宁夏区委组织部任前公示(2024年第13号); 吴忠市政府领导之窗",
    },
    # 县委常务班子 (current)
    {
        "id": 5,
        "name": "高耀祖",
        "gender": "男",
        "ethnicity": "回族*",
        "birth": "1980-06",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同心县委副书记、政法委书记",
        "current_org": "同心县委政法委",
        "source": "同心县政府领导之窗",
    },
    {
        "id": 6,
        "name": "张庆",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983-10",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同心县委副书记（挂职）",
        "current_org": "中共同心县委员会",
        "source": "同心县政府领导之窗",
    },
    {
        "id": 7,
        "name": "林俊杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-09",
        "birthplace": "",
        "education": "大学本科（江西财经大学）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同心县委副书记、副县长（挂职）",
        "current_org": "同心县人民政府",
        "source": "同心县政府领导之窗",
    },
    {
        "id": 8,
        "name": "伊红德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-02",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同心县纪委书记、监委主任",
        "current_org": "同心县纪律检查委员会",
        "source": "同心县政府领导之窗",
    },
    {
        "id": 9,
        "name": "刘飞林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-02",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同心县委组织部长、党校校长",
        "current_org": "同心县委组织部",
        "source": "同心县政府领导之窗",
    },
    {
        "id": 10,
        "name": "张彤彤",
        "gender": "女",
        "ethnicity": "回族*",
        "birth": "1992-10",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同心县委宣传部长",
        "current_org": "同心县委宣传部",
        "source": "同心县政府领导之窗",
    },
    {
        "id": 11,
        "name": "马银山",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1978-11",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同心县委统战部长、县政协党组副书记",
        "current_org": "同心县委统战部",
        "source": "同心县政府领导之窗",
    },
    {
        "id": 12,
        "name": "张金成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-04",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同心县委常委、常务副县长",
        "current_org": "同心县人民政府",
        "source": "同心县政府领导之窗; 吴忠市商务局领导简历",
    },
    {
        "id": 13,
        "name": "杨海龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-12",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同心县委常委、人武部政委",
        "current_org": "同心县人民武装部",
        "source": "同心县政府领导之窗",
    },
    # 人大 / 政协
    {
        "id": 14,
        "name": "洪建群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-04",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同心县人大常委会主任",
        "current_org": "同心县人大常委会",
        "source": "同心县政府领导之窗",
    },
    {
        "id": 15,
        "name": "马俊文",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1968-06",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同心县政协主席",
        "current_org": "同心县政协",
        "source": "同心县政府领导之窗",
    },
    # 政府副县长
    {
        "id": 16,
        "name": "柳军红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-10",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同心县副县长、公安局局长",
        "current_org": "同心县公安局",
        "source": "同心县政府领导之窗",
    },
    {
        "id": 17,
        "name": "朱志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-11",
        "birthplace": "",
        "education": "大学（九三学社）",
        "party_join": "",
        "work_start": "",
        "current_post": "同心县副县长",
        "current_org": "同心县人民政府",
        "source": "同心县政府领导之窗",
    },
    {
        "id": 18,
        "name": "丁瑞民",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1987-07",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同心县副县长（福建挂职）",
        "current_org": "同心县人民政府",
        "source": "同心县政府领导之窗",
    },
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 县委
    {"person_id": 1, "org_id": 1, "title": "同心县委书记", "start_date": "2024-12", "end_date": "present", "rank": "县处级正职", "note": "2024年12月31日全县领导干部大会宣布"},
    {"person_id": 2, "org_id": 1, "title": "同心县委副书记", "start_date": "2024-12", "end_date": "present", "rank": "县处级正职", "note": "2024年12月18日任"},
    {"person_id": 2, "org_id": 2, "title": "同心县人民政府县长", "start_date": "2025-01", "end_date": "present", "rank": "县处级正职", "note": "2025年1月7日县十九届人大四次会议当选"},
    {"person_id": 5, "org_id": 9, "title": "同心县委副书记、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "同心县委副书记（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "同心县委副书记、副县长（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "福建援宁挂职"},
    {"person_id": 8, "org_id": 5, "title": "同心县委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "同心县委常委、组织部长、党校校长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 7, "title": "同心县委常委、宣传部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 8, "title": "同心县委常委、统战部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼县政协党组副书记"},
    {"person_id": 12, "org_id": 2, "title": "同心县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 11, "title": "同心县委常委、人武部政委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "同心县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 15, "org_id": 4, "title": "同心县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 16, "org_id": 10, "title": "同心县副县长、公安局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "同心县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "九三学社成员"},
    {"person_id": 18, "org_id": 2, "title": "同心县副县长（福建挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "闽宁协作挂职"},
    # 前任职务
    {"person_id": 3, "org_id": 1, "title": "同心县委书记（前任）", "start_date": "2022-01", "end_date": "2024-12", "rank": "县处级正职", "note": "2024年12月31日卸任"},
    {"person_id": 3, "org_id": 15, "title": "宁夏回族自治区发展和改革委员会主任", "start_date": "2025-01", "end_date": "present", "rank": "厅级正职", "note": "2024年第17号公示拟任区直单位正厅级"},
    {"person_id": 4, "org_id": 2, "title": "同心县人民政府县长（前任）", "start_date": "2021", "end_date": "2024-12", "rank": "县处级正职", "note": "2024年12月18日卸任"},
    {"person_id": 4, "org_id": 1, "title": "吴忠市委常委、宣传部部长", "start_date": "2024-12", "end_date": "present", "rank": "地市副职", "note": "2024年第13号公示"},
    {"person_id": 2, "org_id": 12, "title": "宁夏自治区财政厅预算处处长", "start_date": "", "end_date": "2024-12", "rank": "处级正职", "note": "任前公示确认"},
    {"person_id": 12, "org_id": 17, "title": "吴忠市商务和投资促进局副局长", "start_date": "", "end_date": "2026", "rank": "处级副职", "note": "调任同心前任职"},
    # 陈华早期履历
    {"person_id": 1, "org_id": 16, "title": "盐池县住房和城乡建设局局长", "start_date": "", "end_date": "", "rank": "科级/乡科级", "note": "早期履历（顺序,无精确日期）"},
    {"person_id": 1, "org_id": 16, "title": "盐池县大水坑镇党委书记", "start_date": "", "end_date": "", "rank": "乡科级", "note": "早期履历"},
    {"person_id": 1, "org_id": 13, "title": "同心县委常委、韦州镇党委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "早期履历"},
    {"person_id": 1, "org_id": 14, "title": "吴忠金积工业园区党工委副书记、管委会主任", "start_date": "", "end_date": "2024-12", "rank": "县处级正职", "note": "任县委书记前"},
]

# ── Relationships (person ↔ person) ───────────────────────────────────────────
relationships = [
    # 书记 ↔ 县长 搭班
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县长搭班工作", "overlap_org": "同心县领导班子", "overlap_period": "2024-12 至今"},
    # 前任—现任 书记
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "王汉武→陈华 县委书记接任", "overlap_org": "中共同心县委", "overlap_period": "2024-12"},
    # 前任—现任 县长
    {"person_a": 4, "person_b": 2, "type": "predecessor_successor", "context": "杨春燕→虎玉宝 县长接任", "overlap_org": "同心县人民政府", "overlap_period": "2024-12"},
    # 县委书记 ↔ 各常委
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记—专职副书记", "overlap_org": "同心县委", "overlap_period": "2025 至今"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记—纪委书记", "overlap_org": "同心县委", "overlap_period": "2025 至今"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记—组织部长（干部任命）", "overlap_org": "同心县委", "overlap_period": "2025 至今"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "县委书记—人大主任 四套班子共事", "overlap_org": "同心县四套班子", "overlap_period": "2025 至今"},
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "县委书记—政协主席 四套班子共事", "overlap_org": "同心县四套班子", "overlap_period": "2025 至今"},
    # 县长 ↔ 常务/副县长
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长—常务副县长", "overlap_org": "同心县人民政府", "overlap_period": "2025 至今"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "县长—副县长/公安局长", "overlap_org": "同心县人民政府", "overlap_period": "2025 至今"},
    # 跨县交流
    {"person_a": 1, "person_b": 12, "type": "same_system", "context": "陈华(盐池→同心)与张金成(吴忠市商务局→同心)先后调入同心县", "overlap_org": "同心县领导班子", "overlap_period": "2025 至今"},
    {"person_a": 3, "person_b": 1, "type": "promotion_chain", "context": "王汉武区发改委→同心书记→区直部门；陈华接任书记", "overlap_org": "宁夏自治区党委干部管理", "overlap_period": "2024-12"},
]

# ── Build ─────────────────────────────────────────────────────────────────────

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
    print(f"Build complete. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")
    conn = sqlite3.connect(str(DB_PATH))
    try:
        for table in ("persons", "organizations", "positions", "relationships"):
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table}: {count}")
    finally:
        conn.close()