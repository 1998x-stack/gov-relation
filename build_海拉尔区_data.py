#!/usr/bin/env python3
"""海拉尔区（呼伦贝尔市，内蒙古自治区）领导班子工作关系网络数据生成脚本。

Task ID: inner_mongolia_海拉尔区
Province: 内蒙古自治区
Parent city: 呼伦贝尔市
Level: 市辖区
Targets: 区委书记 & 区长
调查日期：2026-08-06

现任班子（截至 2026-08-06，海拉尔区人民政府网 www.hailar.gov.cn 领导之窗确认）：
  - 区委书记：杨杰（男，汉族，1972年1月出生，中国科学院大学研究生学历，理学博士，
            高级农艺师，中共党员；兼任呼伦贝尔市人大常委会副主任——2026-06 起以
            「市人大常委会副主任、区委书记」身份出现） — 官方领导之窗 /Leader/show/17/53.html
  - 区委副书记、区长提名人选：于文成（男，蒙古族，1986年5月出生，研究生学历，中共党员；
            区人民政府党组书记，主持区政府全面工作、分管审计局；为区长现任提名人选；
            前任区长待查明） — /Leader/show/15/1079.html
  - 区委副书记、政法委书记：杜海娇（女，满族，1982年5月，研究生，中共党员）
  - 区委常委、纪委书记、监委主任：刘红芝（女，汉族，1972年1月，大学/管理学学士）
  - 区委常委、常务副区长：白春梅（女，蒙古族，1973年12月，大学）
  - 区委常委、宣传部长：曹大庆（男，汉族，1975年10月，内蒙古工业大学本科/工学学士）
  - 区委常委、组织部长：史奎梧（男，汉族，1978年1月，大学）
  - 区委常委、区委办主任：文进民（男，蒙古族，1971年3月，大学）
  - 区委常委、副区长：乔建华（男，汉族，1988年4月，大学农学学士）
  - 区委常委、统战部长：吕芳涛（男，汉族，1982年7月，呼伦贝尔学院/文学学士）
  - 区委常委、人武部政委：向治华
  - 区人大常委会主任：宝林（男，蒙古族，1967年7月，内蒙古党校研究生）
  - 区政府副区长：孟繁星（男，汉，1973年12月，二级高级警长，兼公安分局长）、
    谢子明（男，汉，1976年5月，大学）、于安（男，蒙古族，1982年4月，吉林松原，
    哈尔滨师范大学思政）、李沣源
  - 区政协主席：李艳英（女，汉族，1969年9月，研究生工学硕士）

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 新产物第一优先级写入本脚本所在暂存目录（data/tmp/<task>/），再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/inner_mongolia_海拉尔区/build_海拉尔区_data.py   # 产出写到暂存目录
    python3 scripts/build/build_海拉尔区_data.py                        # 归档后运行，产出到 canonical 目录
"""

import sys
from contextlib import closing
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

SLUG = "海拉尔区"
PROVINCE = "内蒙古自治区"
PARENT_CITY = "呼伦贝尔市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

if "__file__" in globals():
    _this = Path(__file__).resolve()
    _in_staging = ("data" in _this.parts) and ("tmp" in _this.parts)
else:
    _in_staging = False
# 暂存运行（data/tmp/<任务>/）→ 产物写到该暂存目录；canonical 运行 → 写到 data/database|graph
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
        id=1, name="杨杰", gender="男", ethnicity="汉族", birth="1972年1月", birthplace="",
        education="中国科学院大学研究生学历、理学博士；高级农艺师", party_join="中共党员（入党年月未公开）", work_start="",
        current_post="呼伦贝尔市人大常委会副主任、海拉尔区委书记",
        current_org="中共呼伦贝尔市海拉尔区委员会",
        source="海拉尔区人民政府网领导之窗（2026-08）/ News 区委常委会第178次会议（2026-08-05）/ News 2026-06-22 调研报道",
    ),
    dict(
        id=2, name="于文成", gender="男", ethnicity="蒙古族", birth="1986年5月", birthplace="",
        education="研究生学历", party_join="", work_start="",
        current_post="海拉尔区委副书记、区政府区长提名人选、党组书记",
        current_org="呼伦贝尔市海拉尔区人民政府",
        source="海拉尔区人民政府领导之窗于文成（2026-08-06）",
    ),
    dict(
        id=3, name="杜海娇", gender="女", ethnicity="满族", birth="1982年5月", birthplace="",
        education="研究生", party_join="", work_start="",
        current_post="海拉尔区委副书记、政法委书记", current_org="中共呼伦贝尔市海拉尔区委员会",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=4, name="刘红芝", gender="女", ethnicity="汉族", birth="1972年1月", birthplace="",
        education="大学、管理学学士", party_join="", work_start="",
        current_post="海拉尔区委常委、纪委书记、监委主任", current_org="中共呼伦贝尔市海拉尔区纪律检查委员会",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=5, name="白春梅", gender="女", ethnicity="蒙古族", birth="1973年12月", birthplace="",
        education="大学", party_join="", work_start="",
        current_post="海拉尔区委常委、区政府副区长（常务）", current_org="呼伦贝尔市海拉尔区人民政府",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=6, name="曹大庆", gender="男", ethnicity="汉族", birth="1975年10月", birthplace="",
        education="内蒙古工业大学本科、工学学士", party_join="", work_start="",
        current_post="海拉尔区委常委、宣传部部长", current_org="中共呼伦贝尔市海拉尔区委员会",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=7, name="史奎梧", gender="男", ethnicity="汉族", birth="1978年1月", birthplace="",
        education="大学", party_join="", work_start="",
        current_post="海拉尔区委常委、组织部部长", current_org="中共呼伦贝尔市海拉尔区委员会",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=8, name="文进民", gender="男", ethnicity="蒙古族", birth="1971年3月", birthplace="",
        education="大学", party_join="", work_start="",
        current_post="海拉尔区委常委、区委办公室主任", current_org="中共呼伦贝尔市海拉尔区委员会",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=9, name="乔建华", gender="男", ethnicity="汉族", birth="1988年4月", birthplace="",
        education="大学、农学学士", party_join="", work_start="",
        current_post="海拉尔区委常委、区政府副区长（分管三农、乡村振兴、招商）", current_org="呼伦贝尔市海拉尔区人民政府",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=10, name="吕芳涛", gender="男", ethnicity="汉族", birth="1982年7月", birthplace="",
        education="呼伦贝尔学院、文学学士", party_join="", work_start="",
        current_post="海拉尔区委常委、统战部部长", current_org="中共呼伦贝尔市海拉尔区委员会",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=11, name="向治华", gender="男", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="海拉尔区委常委、人民武装部政治委员", current_org="呼伦贝尔市海拉尔区人民武装部",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=12, name="宝林", gender="男", ethnicity="蒙古族", birth="1967年7月", birthplace="",
        education="内蒙古党校研究生", party_join="", work_start="",
        current_post="海拉尔区人大常委会党组书记、主任", current_org="呼伦贝尔市海拉尔区人大常委会",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=13, name="孟繁星", gender="男", ethnicity="汉族", birth="1973年12月", birthplace="",
        education="大学、二级高级警长", party_join="", work_start="",
        current_post="海拉尔区政府副区长兼呼伦贝尔市公安局海拉尔分局局长", current_org="呼伦贝尔市公安局海拉尔分局",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=14, name="谢子明", gender="男", ethnicity="汉族", birth="1976年5月", birthplace="",
        education="大学", party_join="", work_start="",
        current_post="海拉尔区政府副区长（分管住建、城管、自然资源）", current_org="呼伦贝尔市海拉尔区人民政府",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=15, name="于安", gender="男", ethnicity="蒙古族", birth="1982年4月", birthplace="吉林松原",
        education="哈尔滨师范大学思想政治教育专业", party_join="2004年4月", work_start="2005年7月",
        current_post="海拉尔区政府副区长（分管教育、卫健、商务）", current_org="呼伦贝尔市海拉尔区人民政府",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=16, name="李沣源", gender="男", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="海拉尔区政府副区长", current_org="呼伦贝尔市海拉尔区人民政府",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=17, name="李艳英", gender="女", ethnicity="汉族", birth="1969年9月", birthplace="",
        education="研究生、工学硕士", party_join="", work_start="",
        current_post="海拉尔区政协主席、党组书记", current_org="政协呼伦贝尔市海拉尔区委员会",
        source="海拉尔区人民政府网领导之窗（2026-08）",
    ),
    dict(
        id=18, name="于民", gender="", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="海拉尔区区长（前任，已于2026年卸任）", current_org="呼伦贝尔市海拉尔区人民政府",
        source="海拉尔区2026年政府工作报告（十六届人大六次会议2026-01-30由区长于民作报告）确认前任区长",
    ),
    dict(
        id=19, name="杨国宏", gender="", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="海拉尔区委书记（前任，2019年在任，~2021年卸任）", current_org="中共呼伦贝尔市海拉尔区委员会",
        source="海拉尔区政务网新闻：2019-10-18 区委杨国宏书记、2019-07-26 杨国宏带队调研（官方新闻）确认其为前任区委书记",
    ),
]

# ── Organizations ─────────────────────────────────────────────────────
organizations = [
    dict(id=1, name="中共呼伦贝尔市海拉尔区委员会", type="党委", level="市辖区", parent="中共呼伦贝尔市委员会", location="内蒙古呼伦贝尔市海拉尔区"),
    dict(id=2, name="呼伦贝尔市海拉尔区人民政府", type="政府", level="市辖区", parent="呼伦贝尔市人民政府", location="内蒙古呼伦贝尔市海拉尔区"),
    dict(id=3, name="呼伦贝尔市海拉尔区人大常委会", type="人大", level="市辖区", parent="呼伦贝尔市人大常委会", location="内蒙古呼伦贝尔市海拉尔区"),
    dict(id=4, name="政协呼伦贝尔市海拉尔区委员会", type="政协", level="市辖区", parent="政协呼伦贝尔市委员会", location="内蒙古呼伦贝尔市海拉尔区"),
    dict(id=5, name="中共呼伦贝尔市海拉尔区纪律检查委员会", type="纪委", level="市辖区", parent="中共呼伦贝尔市纪律检查委员会", location="内蒙古呼伦贝尔市海拉尔区"),
    dict(id=6, name="呼伦贝尔市人大常委会", type="人大", level="地级市", parent="内蒙古自治区人大常委会", location="内蒙古呼伦贝尔市"),
    dict(id=7, name="呼伦贝尔市公安局海拉尔分局", type="政府", level="市辖区", parent="呼伦贝尔市公安局", location="内蒙古呼伦贝尔市海拉尔区"),
    dict(id=8, name="呼伦贝尔市海拉尔区人民武装部", type="政府", level="市辖区", parent="呼伦贝尔军分区", location="内蒙古呼伦贝尔市海拉尔区"),
]

# ── Positions ─────────────────────────────────────────────────────────
positions = [
    dict(person_id=1, org_id=1, title="海拉尔区委书记", start_date="（在任，截至2026-08）", end_date="present", rank="正处级", note="主持区委全面工作；兼任呼伦贝尔市人大常委会副主任"),
    dict(person_id=1, org_id=6, title="呼伦贝尔市人大常委会副主任", start_date="（2026-06前已任职）", end_date="present", rank="副厅级", note="以『市人大常委会副主任、区委书记』身份参会调研"),
    dict(person_id=2, org_id=2, title="海拉尔区政府区长提名人选（拟任区长）", start_date="（2026年）", end_date="present", rank="正处级", note="区政府党组书记，主持区政府全面工作、分管审计局"),
    dict(person_id=2, org_id=1, title="海拉尔区委副书记", start_date="（2026年）", end_date="present", rank="正处级", note="党政班子二把手"),
    dict(person_id=3, org_id=1, title="区委副书记、政法委书记", start_date="（在任）", end_date="present", rank="副处级", note="协助区委书记负责党建、政法信访维稳"),
    dict(person_id=4, org_id=5, title="区纪委书记、监委主任", start_date="（在任）", end_date="present", rank="副处级", note=""),
    dict(person_id=5, org_id=2, title="区委常委、区政府常务副区长", start_date="（在任）", end_date="present", rank="副处级", note="协助区长并分管发改/财税/金融/审计/国资/应急等"),
    dict(person_id=6, org_id=1, title="区委宣传部部长", start_date="（在任）", end_date="present", rank="副处级", note=""),
    dict(person_id=7, org_id=1, title="区委组织部部长", start_date="（在任）", end_date="present", rank="副处级", note="兼任区委老干部局局长、公务员局局长"),
    dict(person_id=8, org_id=1, title="区委办公室主任", start_date="（在任）", end_date="present", rank="副处级", note=""),
    dict(person_id=9, org_id=2, title="区政府副区长", start_date="（在任）", end_date="present", rank="副处级", note="分管水利/农村经济/乡村振兴/招商引资"),
    dict(person_id=10, org_id=1, title="区委统战部部长", start_date="（在任）", end_date="present", rank="副处级", note=""),
    dict(person_id=11, org_id=8, title="区人武部政治委员", start_date="（在任）", end_date="present", rank="副处级（军）", note=""),
    dict(person_id=12, org_id=3, title="区人大常委会主任", start_date="（在任）", end_date="present", rank="正处级", note="区人大常委会党组书记"),
    dict(person_id=13, org_id=7, title="区政府副区长兼公安分局长", start_date="（在任）", end_date="present", rank="副处级", note="呼伦贝尔市公安局海拉尔分局党委书记、局长，二级高级警长"),
    dict(person_id=14, org_id=2, title="区政府副区长", start_date="（在任）", end_date="present", rank="副处级", note="分管住建、城管、自然资源、征收安置"),
    dict(person_id=15, org_id=2, title="区政府副区长", start_date="（在任）", end_date="present", rank="副处级", note="分管教育、卫生健康、商务口岸"),
    dict(person_id=16, org_id=2, title="区政府副区长", start_date="（在任）", end_date="present", rank="副处级", note=""),
    dict(person_id=17, org_id=4, title="区政协主席", start_date="（在任）", end_date="present", rank="正处级", note="区政协党组书记"),
    dict(person_id=19, org_id=1, title="海拉尔区委书记（前任）", start_date="（2019年在任）", end_date="（~2021卸任）", rank="正处级", note="前任区委书记杨国宏，2019-10仍主持海区工作；~2021由杨杰接任"),
    dict(person_id=18, org_id=2, title="区区长（前任）", start_date="（至少2026-01-30在任）", end_date="（2026年春卸任）", rank="正处级", note="前任区长于民，2026-01-30 十六届人大六次会议作政府工作报告"),
]

# ── Relationships ─────────────────────────────────────────────────────
relationships = [
    dict(person_a=1, person_b=2, type="overlap", context="海拉尔区委书记—区长（提名人选）党政正职搭档，同出席区委常委会178次会议（2026-08-05）", overlap_org="中共呼伦贝尔市海拉尔区委员会/海拉尔区人民政府", overlap_period="2026"),
    dict(person_a=1, person_b=3, type="superior_subordinate", context="区委书记—专职副书记（杜海娇协助书记负责党建）", overlap_org="中共呼伦贝尔市海拉尔区委员会", overlap_period="在任"),
    dict(person_a=1, person_b=6, type="superior_subordinate", context="区委书记—区委常委、宣传部长（区委班子）", overlap_org="中共呼伦贝尔市海拉尔区委员会", overlap_period="在任"),
    dict(person_a=1, person_b=7, type="superior_subordinate", context="区委书记—组织部长（区委班子）", overlap_org="中共呼伦贝尔市海拉尔区委员会", overlap_period="在任"),
    dict(person_a=1, person_b=5, type="superior_subordinate", context="区委书记—常务副区长（区委常委、政府班子）", overlap_org="中共呼伦贝尔市海拉尔区委员会", overlap_period="在任"),
    dict(person_a=2, person_b=5, type="superior_subordinate", context="区长（提名人）—常务副区长白春梅（协助区长负责政府常务）", overlap_org="呼伦贝尔市海拉尔区人民政府", overlap_period="在任"),
    dict(person_a=2, person_b=9, type="superior_subordinate", context="区长（提名人）—副区长乔建华（政府班子）", overlap_org="呼伦贝尔市海拉尔区人民政府", overlap_period="在任"),
    dict(person_a=2, person_b=14, type="superior_subordinate", context="区长（提名人）—副区长谢子明（政府班子）", overlap_org="呼伦贝尔市海拉尔区人民政府", overlap_period="在任"),
    dict(person_a=2, person_b=15, type="superior_subordinate", context="区长（提名人）—副区长于安（政府班子）", overlap_org="呼伦贝尔市海拉尔区人民政府", overlap_period="在任"),
    dict(person_a=2, person_b=13, type="superior_subordinate", context="区长（提名人）—副区长孟繁星（兼公安局长）", overlap_org="呼伦贝尔市公安局海拉尔分局", overlap_period="在任"),
    dict(person_a=1, person_b=12, type="overlap", context="区委书记—区人大主任（四套班子正职会）", overlap_org="呼伦贝尔市海拉尔区人大常委会", overlap_period="在任"),
    dict(person_a=1, person_b=17, type="overlap", context="区委书记—区政协主席（四套班子正职会）", overlap_org="政协呼伦贝尔市海拉尔区委员会", overlap_period="在任"),
    dict(person_a=2, person_b=12, type="overlap", context="区长（提名人）—区人大主任（人大任命程序）", overlap_org="呼伦贝尔市海拉尔区人大常委会", overlap_period="2026"),
    dict(person_a=4, person_b=1, type="superior_subordinate", context="区纪委书记—区委书记（纪委受区委领导）", overlap_org="中共呼伦贝尔市海拉尔区委员会", overlap_period="在任"),
    dict(person_a=1, person_b=19, type="predecessor_successor", context="杨杰（~2021）接任前任区委书记杨国宏（2019年在任）", overlap_org="中共呼伦贝尔市海拉尔区委员会", overlap_period="~2021"),
    dict(person_a=2, person_b=18, type="predecessor_successor", context="于文成（区长提名人选）接任前任区长于民（2026-01-30 于民仍作政府工作报告，2026年春由于文成接任）", overlap_org="呼伦贝尔市海拉尔区人民政府", overlap_period="2026"),
]


def build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络 (呼伦贝尔市 · 内蒙古自治区)")
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
    with closing(sqlite3.connect(str(DB_PATH))) as conn:
        n_p = conn.execute("SELECT count(*) FROM persons").fetchone()[0]
        n_o = conn.execute("SELECT count(*) FROM organizations").fetchone()[0]
        n_pos = conn.execute("SELECT count(*) FROM positions").fetchone()[0]
        n_rel = conn.execute("SELECT count(*) FROM relationships").fetchone()[0]
    print(f"  DB 校验: persons={n_p}, orgs={n_o}, positions={n_pos}, relationships={n_rel}")
    print(f"\n完成。产物：\n  DB:   {DB_PATH}\n  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    build()