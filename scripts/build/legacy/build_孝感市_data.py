#!/usr/bin/env python3
"""Build script for 孝感市 (Xiaogan) cadre leadership network.

Task: hubei_孝感市 — targets 市委书记 & 市长 (prefecture-level city, 湖北省).
As-of date: 2026-08-06.

Key sources (official 孝感市人民政府门户 https://www.xiaogan.gov.cn/, 领导之窗, fetched 2026-08-06):
- 市委书记：胡玖明 (1969-09, 大学学历、高级管理人员工商管理硕士)
- 市委副书记/市长：林中麟 (1974-09, 大学学历、公共管理硕士)
- 市委副书记(正厅长级)：王云清 (1978-01)
- 市委常委：张淼(统战→组织), 贺卫东(统战部长), 曾凡笋(军分区司令员), 黄建军(政法委书记), 赵志国(纪委书记/监委主任)
- 市人大主任：吴丕华 (1969-09)
- 市政府副市长：石必成、潘晓洁(农工党)、童巍(公AN局长)、徐长斌、朱罡
- 市政协主席：刘振军
Official 领导之窗 URLs (slug map recorded in checkpoint_01_research.md).

CONFIDENCE NOTES
- 现任市委书记=胡玖明、市长=林中麟 (confirmed: 官方领导之窗 2026-08-06; 领导活动日历高频报道)
- 前任市长吴庆华已离职,现任为林中麟 (confirmed: 官方领导之窗现任为林中麟; 首页旧 HTML 占位仍为吴庆华[wqh]系过期注释)
- 各核心人物出生年月/学历来自官方领导之窗简历 (高置信)
- 胡玖明/林中麟详细早年履历、前任市委书记人姓名及去向 = 待核 (见 person JSON open_questions / report open_gaps)
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
SLUG = "孝感市"

TMP = Path(__file__).resolve().parent
DB_PATH = TMP / "孝感市_network.db"
GEXF_PATH = TMP / "孝感市_network.gexf"

persons = [
    # ── 现任 党委 (市委) ──
    {
        "id": 10,
        "name": "胡玖明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-09",
        "birthplace": "",
        "education": "大学学历、高级管理人员工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孝感市委书记",
        "current_org": "中共孝感市委员会",
        "source": "https://www.xiaogan.gov.cn/ld/swld/swsj/hjm/",
    },
    {
        "id": 11,
        "name": "林中麟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-09",
        "birthplace": "",
        "education": "大学学历、公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孝感市委副书记、市长",
        "current_org": "孝感市人民政府",
        "source": "https://www.xiaogan.gov.cn/ld/szfld/sc/lzl/",
    },
    {
        "id": 12,
        "name": "王云清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-01",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孝感市委副书记",
        "current_org": "中共孝感市委员会",
        "source": "https://www.xiaogan.gov.cn/ld/swld/swfsj/wyq/",
    },
    {
        "id": 13,
        "name": "张淼",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975-09",
        "birthplace": "",
        "education": "大学学历、经济学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孝感市委常委、组织部部长",
        "current_org": "中共孝感市委员会",
        "source": "https://www.xiaogan.gov.cn/ld/swld/swcw/zm/",
    },
    {
        "id": 14,
        "name": "贺卫东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-01",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孝感市委常委、统战部部长",
        "current_org": "中共孝感市委员会",
        "source": "https://www.xiaogan.gov.cn/ld/swld/swcw/hwd/",
    },
    {
        "id": 15,
        "name": "曾凡笋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-06",
        "birthplace": "",
        "education": "在职研究生、法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孝感市委常委、孝感军分区司令员",
        "current_org": "孝感军分区",
        "source": "https://www.xiaogan.gov.cn/ld/swld/swcw/zfs/",
    },
    {
        "id": 16,
        "name": "黄建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-05",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孝感市委常委、政法委书记",
        "current_org": "中共孝感市委员会",
        "source": "https://www.xiaogan.gov.cn/ld/swld/swcw/hjj/",
    },
    {
        "id": 17,
        "name": "赵志国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-09",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孝感市委常委、市纪委书记、市监委主任",
        "current_org": "中共孝感市纪律检查委员会",
        "source": "https://www.xiaogan.gov.cn/ld/swld/swcw/zzg/",
    },
    # ── 市人大 ──
    {
        "id": 20,
        "name": "吴丕华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-09",
        "birthplace": "",
        "education": "在职大学、法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孝感市人大常委会主任",
        "current_org": "孝感市人民代表大会常务委员会",
        "source": "https://www.xiaogan.gov.cn/ld/srdld/zr/wph/",
    },
    # ── 市政府 (副市长) ──
    {
        "id": 21,
        "name": "石必成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-07",
        "birthplace": "",
        "education": "大学学历、公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孝感市人民政府副市长",
        "current_org": "孝感市人民政府",
        "source": "https://www.xiaogan.gov.cn/ld/szfld/fsc/sbc/",
    },
    {
        "id": 22,
        "name": "潘晓洁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980-12",
        "birthplace": "",
        "education": "博士研究生、理学博士",
        "party_join": "中国农工民主党",
        "work_start": "",
        "current_post": "孝感市人民政府副市长",
        "current_org": "孝感市人民政府",
        "source": "https://www.xiaogan.gov.cn/ld/szfld/fsc/pxj/",
    },
    {
        "id": 23,
        "name": "童巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-10",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孝感市人民政府副市长、市公安局局长",
        "current_org": "孝感市人民政府",
        "source": "https://www.xiaogan.gov.cn/ld/szfld/fsc/tw/",
    },
    {
        "id": 24,
        "name": "徐长斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-12",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孝感市人民政府副市长",
        "current_org": "孝感市人民政府",
        "source": "https://www.xiaogan.gov.cn/ld/szfld/fsc/xzb/",
    },
    {
        "id": 25,
        "name": "朱江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-08",
        "birthplace": "",
        "education": "大学学历、管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孝感市人民政府副市长",
        "current_org": "孝感市人民政府",
        "source": "https://www.xiaogan.gov.cn/ld/szfld/fsc/zj/",
    },
    # ── 市政协 ──
    {
        "id": 26,
        "name": "刘振军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-11",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "孝感市政协主席",
        "current_org": "政协孝感市委员会",
        "source": "https://www.xiaogan.gov.cn/ld/szxld/zx/lzj/",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共孝感市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党湖北省委员会",
        "location": "孝感市",
    },
    {
        "id": 2,
        "name": "孝感市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "湖北省人民政府",
        "location": "孝感市",
    },
    {
        "id": 3,
        "name": "孝感市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "中共孝感市委员会",
        "location": "孝感市",
    },
    {
        "id": 4,
        "name": "政协孝感市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "中共孝感市委员会",
        "location": "孝感市",
    },
    {
        "id": 5,
        "name": "中共孝感市纪律检查委员会",
        "type": "纪委",
        "level": "地级市",
        "parent": "中共孝感市委员会",
        "location": "孝感市",
    },
    {
        "id": 6,
        "name": "孝感军分区",
        "type": "军事",
        "level": "地级市",
        "parent": "湖北省军区",
        "location": "孝感市",
    },
    {
        "id": 7,
        "name": "中国共产党湖北省委员会",
        "type": "党委",
        "level": "省级",
        "parent": "",
        "location": "武汉市",
    },
    {
        "id": 8,
        "name": "湖北省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "武汉市",
    },
]

positions = [
    # ── 市委书记 ──
    {"person_id": 10, "org_id": 1, "title": "孝感市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "现任; 具体任职日期待核"},
    # ── 市长 ──
    {"person_id": 11, "org_id": 2, "title": "孝感市委副书记、市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "市政府党组书记; 主持市政府全面工作"},
    {"person_id": 11, "org_id": 1, "title": "孝感市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼任市委副书记"},
    # ── 市委副书记 ──
    {"person_id": 12, "org_id": 1, "title": "孝感市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "正厅长级"},
    # ── 市委常委 ──
    {"person_id": 13, "org_id": 1, "title": "孝感市委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "孝感市委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "市政协党组副书记"},
    {"person_id": 15, "org_id": 1, "title": "孝感市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "孝感军分区大校司令员"},
    {"person_id": 16, "org_id": 1, "title": "孝感市委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 5, "title": "孝感市纪委书记、市监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "市委常委、二级高级监察官"},
    # ── 市人大 ──
    {"person_id": 20, "org_id": 3, "title": "孝感市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "党组书记"},
    # ── 市政府班子 ──
    {"person_id": 21, "org_id": 2, "title": "孝感市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 22, "org_id": 2, "title": "孝感市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "农工党中央委员"},
    {"person_id": 23, "org_id": 2, "title": "孝感市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼市公安局局长/党委政法委副书记"},
    {"person_id": 24, "org_id": 2, "title": "孝感市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 25, "org_id": 2, "title": "孝感市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # ── 市政协 ──
    {"person_id": 26, "org_id": 4, "title": "孝感市政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "党组书记"},
]

relationships = [
    # 党政一把手搭档
    {"person_a": 10, "person_b": 11, "type": "党政搭档",
     "context": "胡玖明（市委书记）与林中麟（市委副书记、市长）组成孝感市党政一把手搭档",
     "overlap_org": "中共孝感市委员会/孝感市人民政府", "overlap_period": "2026至今"},
    # 市委班子核心交集 (常委会共事)
    {"person_a": 10, "person_b": 12, "type": "superior_subordinate",
     "context": "市委书记胡玖明与市委副书记王云清同属市委常委会",
     "overlap_org": "中共孝感市委员会", "overlap_period": "2026"},
    {"person_a": 10, "person_b": 13, "type": "superior_subordinate",
     "context": "市委书记与市委常委、组织部长张淼在市委常委会共事",
     "overlap_org": "中共孝感市委员会", "overlap_period": "2026"},
    {"person_a": 10, "person_b": 14, "type": "superior_subordinate",
     "context": "市委书记与市委常委、统战部长贺卫东在市委常委会共事",
     "overlap_org": "中共孝感市委员会", "overlap_period": "2026"},
    {"person_a": 10, "person_b": 16, "type": "superior_subordinate",
     "context": "市委书记胡玖明与市委常委、政法委书记黄建军同属市委常委会",
     "overlap_org": "中共孝感市委员会", "overlap_period": "2026"},
    {"person_a": 10, "person_b": 17, "type": "superior_subordinate",
     "context": "市委书记胡玖明与纪委书记赵志国同属市委常委会",
     "overlap_org": "中共孝感市委员会", "overlap_period": "2026"},
    # 市长与市政府班子
    {"person_a": 11, "person_b": 21, "type": "superior_subordinate",
     "context": "市长林中麟与副市长石必成在市政府班子共事",
     "overlap_org": "孝感市人民政府", "overlap_period": "2026"},
    {"person_a": 11, "person_b": 23, "type": "superior_subordinate",
     "context": "市长林中麟与副市长童巍（兼公安局长）在市政府班子共事",
     "overlap_org": "孝感市人民政府", "overlap_period": "2026"},
    {"person_a": 11, "person_b": 24, "type": "superior_subordinate",
     "context": "市长林中麟与副市长徐长斌在市政府班子共事",
     "overlap_org": "孝感市人民政府", "overlap_period": "2026"},
    {"person_a": 11, "person_b": 25, "type": "superior_subordinate",
     "context": "市长林中麟与副市长朱江在市政府班子共事",
     "overlap_org": "孝感市人民政府", "overlap_period": "2026"},
    # 人大/政协
    {"person_a": 20, "person_b": 10, "type": "same_system",
     "context": "市人大常委会主任吴丕华与市委书记同受市委统一领导",
     "overlap_org": "中国共产党孝感市委员会", "overlap_period": "2026"},
    {"person_a": 26, "person_b": 10, "type": "same_system",
     "context": "市政协主席刘振军与市委书记同受市委统一领导",
     "overlap_org": "中国共产党孝感市委员会", "overlap_period": "2026"},
    # 前任市长继任链 (待核)
    {"person_a": 11, "person_b": 30, "type": "predecessor_successor",
     "context": "林中麟接任前任孝感市长（继任链; 前任吴庆华已离任，具体交接日期待核）",
     "overlap_org": "孝感市人民政府", "overlap_period": ""},
    # 省级统一领导关系
    {"person_a": 10, "person_b": 26, "type": "same_system",
     "context": "市级领导班子成员均受湖北省委领导",
     "overlap_org": "中国共产党湖北省委员会", "overlap_period": ""},
]

# 前任市长 (placeholder; 待核)
persons.append({
    "id": 30,
    "name": "吴庆华",
    "gender": "男",
    "ethnicity": "",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "中共党员",
    "work_start": "",
    "current_post": "前任孝感市长（已离任）",
    "current_org": "孝感市人民政府",
    "source": "https://www.xiaogan.gov.cn/ld/szfld/sc/wqh/",
})
positions.append({"person_id": 30, "org_id": 2, "title": "前任孝感市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任; 具体任期待核"})

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