#!/usr/bin/env python3
"""科尔沁区（通辽市，内蒙古自治区）领导班子工作关系网络数据生成脚本。

Task ID: inner_mongolia_科尔沁区
Province: 内蒙古自治区
Parent city: 通辽市
Level: 市辖区
Targets: 区委书记 & 区长
调查日期：2026-08-06

现任班子（截至 2026-08，科尔沁区人民政府官网 www.keerqin.gov.cn 政府领导/领导活动 页确认）：
  - 区委书记：薛宏国（男，汉族，1978年7月生，1996年8月参加工作，1999年6月入党，
            内蒙古煤炭工业学校 采煤工程专业；2024年4月由通辽市财政局局长转任，一级调研员）
            — 官网“领导活动”2026-02-13 原文点名 + 百度百科
  - 区委副书记、区长：金树国（男，蒙古族，1980年8月生，内蒙古扎鲁特旗，内蒙古大学法律专业，
            2003年1月参加工作，2012年11月入党；科尔沁区委副书记、区政府党组书记、区长，
            科尔沁工业园区党工委书记、管委会主任）
            — 官网“政府领导”页（区长：金树国）+ 2026《政府工作报告》
  - 常务副区长：孟凡辉（回族8/1983 区委常委、政府党组副书记）<男人汉族 1983-08>
  - 副区长：白巴根那（蒙古族 1971-05）、张博（1985-11）、牟德军（兼公安分局长，1975-10/1973-10）、
            布大为（兼区工信局长，1980-03）、张志勇（1985-02）、孙国红（女 1984-02）
  - 前任区委书记：徐天鹏（男，汉族，1975-09生；约2021/2022—2024年初在任；
            2024-01-04 被内蒙古自治区纪委监委通报接受审查调查[落马]）
  - 前任区长：康晓东（2023年科尔沁区十七届人大二次会议作《政府工作报告》，在任）

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 新产物第一优先级写入本脚本所在暂存目录（data/tmp/<task>/），再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/inner_mongolia_科尔沁区/build_科尔沁区_data.py   # 产出写到暂存目录
    python3 scripts/build/build_科尔沁区_data.py                     # 归档后运行，产出到 canonical 目录
"""

import sys
from datetime import datetime
from pathlib import Path

if "__file__" in globals():
    _here = Path(__file__).resolve()
    _candidate = _here.parent
    while True:
        if (_candidate / "gov_relation").is_dir():
            break
        _parent = _candidate.parent
        if _parent == _candidate:
            _candidate = Path.cwd()
            break
        _candidate = _parent
else:
    _candidate = Path.cwd()
REPO_ROOT = _candidate
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.log import get_logger  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402
from gov_relation.runner import run_build  # noqa: E402

logger = get_logger(__name__)

SLUG = "科尔沁区"
PROVINCE = "内蒙古自治区"
PARENT_CITY = "通辽市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

if "__file__" in globals():
    _this = Path(__file__).resolve()
    _in_staging = ("data" in _this.parts) and ("tmp" in _this.parts)
else:
    _in_staging = False
# 暂存运行（data/tmp/<task>/）→ 产物写到该暂存目录；canonical 运行 → 写到 data/database|graph
if _in_staging:
    OUT_DIR = Path(__file__).resolve().parent
    GEXF_OUT = OUT_DIR
else:
    OUT_DIR = DATABASE_DIR
    GEXF_OUT = GRAPH_DIR
DB_PATH = OUT_DIR / f"{SLUG}_network.db"
GEXF_PATH = GEXF_OUT / f"{SLUG}_network.gexf"

# ── Persons ─────────────────────────────────────────────────────────
# 字段: id, name, gender, ethnicity, birth, birthplace, education, party_join,
#        work_start, current_post, current_org, source
persons = [
    dict(
        id=1, name="薛宏国", gender="男", ethnicity="汉族", birth="1978年7月", birthplace="",
        education="内蒙古煤炭工业学校 采煤工程专业", party_join="1999年6月", work_start="1996年8月",
        current_post="科尔沁区委书记、一级调研员", current_org="中共通辽市科尔沁区委员会",
        source="科尔沁区人民政府官网领导活动 2026-02 / 百度百科",
    ),
    dict(
        id=2, name="金树国", gender="男", ethnicity="蒙古族", birth="1980年8月", birthplace="内蒙古扎鲁特旗",
        education="内蒙古大学 法律专业", party_join="2012年11月", work_start="2003年1月",
        current_post="科尔沁区委副书记、区政府党组书记、区长，科尔沁工业园区党工委书记、管委会主任",
        current_org="科尔沁区人民政府",
        source="科尔沁区人民政府官网 政府领导 / 2026年政府工作报告",
    ),
    dict(
        id=3, name="孟凡辉", gender="男", ethnicity="汉族", birth="1983年8月", birthplace="",
        education="大学", party_join="2008年6月", work_start="",
        current_post="区委常委、区政府党组副书记、常务副区长", current_org="科尔沁区人民政府",
        source="科尔沁区人民政府官网 政府领导",
    ),
    dict(
        id=4, name="白巴根那", gender="男", ethnicity="蒙古族", birth="1971年5月", birthplace="内蒙古科左中旗",
        education="大学（在职研究生）", party_join="1992年7月", work_start="1990年9月",
        current_post="区委常委、副区长", current_org="科尔沁区人民政府",
        source="科尔沁区人民政府官网 政府领导",
    ),
    dict(
        id=5, name="张博", gender="男", ethnicity="汉族", birth="1985年11月", birthplace="北京",
        education="大学", party_join="2008年6月", work_start="2005年9月",
        current_post="区委常委、副区长", current_org="科尔沁区人民政府",
        source="科尔沁区人民政府官网 政府领导",
    ),
    dict(
        id=6, name="牟德军", gender="男", ethnicity="汉族", birth="1973年10月", birthplace="内蒙古通辽市开鲁县",
        education="大学", party_join="1999年9月", work_start="1993年9月",
        current_post="副区长、通辽市公安局科尔沁分局党委书记、局长", current_org="通辽市公安局科尔沁区分局",
        source="科尔沁区人民政府官网 政府领导",
    ),
    dict(
        id=7, name="布大为", gender="男", ethnicity="汉族", birth="1980年3月", birthplace="山东阳谷",
        education="大学", party_join="2001年6月", work_start="2003年6月",
        current_post="副区长、科尔沁区工业和信息化局局长", current_org="科尔沁区人民政府",
        source="科尔沁区人民政府官网 政府领导",
    ),
    dict(
        id=8, name="张志勇", gender="男", ethnicity="汉族", birth="1985年2月", birthplace="内蒙古库伦旗",
        education="大学", party_join="2008年10月", work_start="2010年8月",
        current_post="副区长", current_org="科尔沁区人民政府",
        source="科尔沁区人民政府官网 政府领导",
    ),
    dict(
        id=9, name="孙国红", gender="女", ethnicity="汉族", birth="1984年2月", birthplace="山东宁津",
        education="大学", party_join="2005年11月", work_start="2007年10月",
        current_post="副区长", current_org="科尔沁区人民政府",
        source="科尔沁区人民政府官网 政府领导",
    ),
    # 区委班子其他关键领导（常委）
    dict(
        id=10, name="李永刚", gender="男", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="区委常委、纪委书记、监委主任", current_org="中共通辽市科尔沁区纪律检查委员会",
        source="通辽市政府/科尔沁区新闻 2024-12",
    ),
    dict(
        id=11, name="赵晓英", gender="女", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="区委常委、组织部部长", current_org="中共通辽市科尔沁区委员会组织部",
        source="科尔沁区官网新闻 2025",
    ),
    dict(
        id=12, name="梁威", gender="", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="区委常委、宣传部部长", current_org="中共通辽市科尔沁区委员会宣传部",
        source="科尔沁区民族团结报道（发改委/科尔沁区政府）",
    ),
    dict(
        id=13, name="刘晓辉", gender="", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="区委常委、统战部部长", current_org="中共通辽市科尔沁区委员会统战部",
        source="科尔沁区民族团结报道",
    ),
    dict(
        id=14, name="李洪玮", gender="男", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="区委常委、区委办公室主任", current_org="科尔沁区委办公室",
        source="科尔沁区官网新闻 2025",
    ),
    # 前任（干部更替主线）
    dict(
        id=15, name="徐天鹏", gender="男", ethnicity="汉族", birth="1975年9月", birthplace="",
        education="", party_join="", work_start="",
        current_post="曾任科尔沁区委书记（被查）", current_org="中共通辽市科尔沁区委员会",
        source="内蒙古自治区纪委监委通报 2024-01-04 / 央广网",
    ),
    dict(
        id=16, name="康晓东", gender="", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="曾任科尔沁区长", current_org="科尔沁区人民政府",
        source="科尔沁区2023年《政府工作报告》署名（区十七届人大二次会议）",
    ),
    # 区人大 / 区政协
    dict(
        id=17, name="张延峰", gender="", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="科尔沁区人大常委会主任（截至2024-07）", current_org="科尔沁区人大常委会",
        source="科尔沁区第十七届人大常委会第二十次会议 2024-07-31",
    ),
    dict(
        id=18, name="齐志军", gender="", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="科尔沁区政协主席", current_org="科尔沁区政协",
        source="科尔沁区政协十五届一次会议 2022-01 / 通辽政协网 2025-08",
    ),
]

# ── Organizations ─────────────────────────────────────────────────────
organizations = [
    dict(id=1, name="中共通辽市科尔沁区委员会", type="党委", level="市辖区", parent="中共通辽市委员会", location="内蒙古通辽市科尔沁区"),
    dict(id=2, name="科尔沁区人民政府", type="政府", level="市辖区", parent="通辽市人民政府", location="内蒙古通辽市科尔沁区"),
    dict(id=3, name="科尔沁区人大常委会", type="人大", level="市辖区", parent="通辽市人大常委会", location="内蒙古通辽市科尔沁区"),
    dict(id=4, name="科尔沁区政协", type="政协", level="市辖区", parent="通辽市政协", location="内蒙古通辽市科尔沁区"),
    dict(id=5, name="中共通辽市科尔沁区纪律检查委员会", type="纪委", level="市辖区", parent="通辽市纪律检查委员会", location="内蒙古通辽市科尔沁区"),
    dict(id=6, name="通辽市公安局科尔沁区分局", type="政府", level="市辖区", parent="通辽市公安局", location="内蒙古通辽市科尔沁区"),
    dict(id=7, name="科尔沁区工业和信息化局", type="政府", level="区级", parent="科尔沁区人民政府", location="内蒙古通辽市科尔沁区"),
    dict(id=8, name="科尔沁区委办公室", type="党委", level="市辖区", parent="中共通辽市科尔沁区委员会", location="内蒙古通辽市科尔沁区"),
    dict(id=9, name="科尔沁工业园区党工委", type="党委", level="市辖区", parent="中共通辽市科尔沁区委员会", location="内蒙古通辽市科尔沁区"),
]

# ── Positions ─────────────────────────────────────────────────────────
positions = [
    dict(person_id=1, org_id=1, title="科尔沁区委书记", start_date="2024-04", end_date="present", rank="正处级（一级调研员）", note="由通辽市财政局局长转任"),
    dict(person_id=2, org_id=1, title="区委副书记", start_date="", end_date="present", rank="正处级", note=""),
    dict(person_id=2, org_id=2, title="科尔沁区长", start_date="", end_date="present", rank="正处级", note="兼任科尔沁工业园区党工委书记、管委会主任"),
    dict(person_id=3, org_id=2, title="常务副区长", start_date="", end_date="present", rank="副处级", note=""),
    dict(person_id=4, org_id=2, title="副区长", start_date="", end_date="present", rank="副处级", note=""),
    dict(person_id=5, org_id=2, title="副区长", start_date="", end_date="present", rank="副处级", note=""),
    dict(person_id=6, org_id=6, title="区公安分局局长（兼副区长）", start_date="", end_date="present", rank="副处级", note=""),
    dict(person_id=6, org_id=2, title="副区长", start_date="", end_date="present", rank="副处级", note=""),
    dict(person_id=7, org_id=2, title="副区长、区工信局局长", start_date="", end_date="present", rank="副处级", note=""),
    dict(person_id=8, org_id=2, title="副区长", start_date="", end_date="present", rank="副处级", note=""),
    dict(person_id=9, org_id=2, title="副区长", start_date="", end_date="present", rank="副处级", note=""),
    dict(person_id=10, org_id=5, title="区纪委书记、监委主任", start_date="", end_date="present", rank="副处级", note=""),
    dict(person_id=11, org_id=1, title="区委常委、组织部部长", start_date="", end_date="present", rank="副处级", note=""),
    dict(person_id=12, org_id=1, title="区委常委、宣传部部长", start_date="", end_date="present", rank="副处级", note=""),
    dict(person_id=13, org_id=1, title="区委常委、统战部部长", start_date="", end_date="present", rank="副处级", note=""),
    dict(person_id=14, org_id=8, title="区委办公室主任、区委常委", start_date="", end_date="present", rank="副处级", note=""),
    dict(person_id=15, org_id=1, title="科尔沁区委书记（曾任）", start_date="2021", end_date="2024", rank="正处级", note="2024年被查免职"),
    dict(person_id=16, org_id=2, title="科尔沁区长（曾任）", start_date="", end_date="2023", rank="正处级", note=""),
    dict(person_id=17, org_id=3, title="区人大常委会主任", start_date="", end_date="present", rank="正处级", note=""),
    dict(person_id=18, org_id=4, title="区政协主席", start_date="", end_date="present", rank="正处级", note=""),
]

# ── Relationships ─────────────────────────────────────────────────────
relationships = [
    dict(person_a=1, person_b=2, type="overlap", context="科尔沁区委书记—区长 搭档", overlap_org="科尔沁区", overlap_period="2025-present"),
    dict(person_a=1, person_b=15, type="predecessor_successor", context="科尔沁区委书记 继任/前任（前任被查落马）", overlap_org="中共通辽市科尔沁区委员会", overlap_period="2021-2024→2024-今"),
    dict(person_a=2, person_b=16, type="predecessor_successor", context="科尔沁区区长 继任/前任", overlap_org="科尔沁区人民政府", overlap_period="→2023"),
    dict(person_a=2, person_b=3, type="superior_subordinate", context="区长—常务副区长", overlap_org="科尔沁区人民政府", overlap_period="present"),
    dict(person_a=2, person_b=4, type="superior_subordinate", context="区长—副区长", overlap_org="科尔沁区人民政府", overlap_period="present"),
    dict(person_a=2, person_b=5, type="superior_subordinate", context="区长—副区长", overlap_org="科尔沁区人民政府", overlap_period="present"),
    dict(person_a=2, person_b=6, type="superior_subordinate", context="区长—公安局长（副区长）", overlap_org="科尔沁区人民政府", overlap_period="present"),
    dict(person_a=2, person_b=7, type="superior_subordinate", context="区长—副区长", overlap_org="科尔沁区人民政府", overlap_period="present"),
    dict(person_a=2, person_b=8, type="superior_subordinate", context="区长—副区长", overlap_org="科尔沁区人民政府", overlap_period="present"),
    dict(person_a=2, person_b=9, type="superior_subordinate", context="区长—副区长", overlap_org="科尔沁区人民政府", overlap_period="present"),
    dict(person_a=1, person_b=17, type="overlap", context="区委书记—区人大主任", overlap_org="科尔沁区四套班子", overlap_period="present"),
    dict(person_a=1, person_b=18, type="overlap", context="区委书记—区政协主席", overlap_org="科尔沁区四套班子", overlap_period="present"),
]


def build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络 (通辽市 · 内蒙古自治区)")
    print(f"  调查日期: {AS_OF}")
    print(f"  产出目录: {OUT_DIR}")
    print("=" * 60)
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )
    import sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    n_p = conn.execute("SELECT count(*) FROM persons").fetchone()[0]
    n_o = conn.execute("SELECT count(*) FROM organizations").fetchone()[0]
    n_pos = conn.execute("SELECT count(*) FROM positions").fetchone()[0]
    n_rel = conn.execute("SELECT count(*) FROM relationships").fetchone()[0]
    conn.close()
    print(f"  DB 校验: persons={n_p}, orgs={n_o}, positions={n_pos}, relationships={n_rel}")
    print(f"\n完成。产物：\n  DB:   {DB_PATH}\n  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    build()