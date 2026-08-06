#!/usr/bin/env python3
"""东胜区（鄂尔多斯市，内蒙古自治区）领导班子工作关系网络数据生成脚本。

Task ID: inner_mongolia_东胜区
Province: 内蒙古自治区
Parent city: 鄂尔多斯市
Level: 市辖区
Targets: 区委书记 & 区长
调查日期：2026-08-06

现任班子（截至 2026-08，官网 www.ds.gov.cn 领导活动/党代会报道确认）：
  - 区委书记：高屹东（男，汉族，1973年6月生，大学学历、公共管理硕士，中共党员，1995年8月参加工作；
            现任鄂尔多斯高新技术产业开发区党工委书记、东胜区委书记；2026年7月底区第十次党代会
            当选第十届区委书记） — 来源：鄂尔多斯高新区官网领导成员页（2026-05）+ ds.gov.cn 2026-07-31 区委十届一次全会
  - 区委副书记、区长：韩涛（男，汉族，1982年5月生，内蒙古大学法学、公共管理硕士，2000年10月入党，
            2005年参加工作；2021-06-23 任区委副书记、代区长，2021-07-09 人大常委会任命代区长；
            后正式任区长；东胜经济开发区管委会 → 市委办公厅 → 团市委 → 大路煤化工基地党工委书记）
            — 东胜区人民政府网简历（2026-04）+ 百度百科 + 澎湃新闻/鄂尔多斯日报（2021-06-23）
  - 区人大常委会主任：冀平（区人大常委会党组书记、主任） — ds.gov.cn 2026-08-05 书记专题会确认
  - 区政协主席（候选人）：阿拉腾敖日格乐（区政协党组书记、主席候选人） — ds.gov.cn 2026-08-05 确认
  - 区纪委书记：吕向利（2026-07-30 区第十届纪委一次全会当选；副书记 毛燕君、颉鹏程）
  - 前任区长：刘凤云（2021-06-23 免去东胜区委副书记、区长；现任鄂尔多斯市委常委、副市长）
  - 区政协主席（此前）：韩耀庭
  - 区委常委、区政府副区长（常务方向）：杜继宽、张建功；区政府副区长：张兵（兼公安局长）、保积锴 等

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 新产物第一优先级写入本脚本所在暂存目录（data/tmp/<task>/），再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/inner_mongolia_东胜区/build_东胜区_data.py   # 产出写到暂存目录
    python3 scripts/build/build_东胜区_data.py                     # 归档后运行，产出到 canonical 目录
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

SLUG = "东胜区"
PROVINCE = "内蒙古自治区"
PARENT_CITY = "鄂尔多斯市"
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
        id=1, name="高屹东", gender="男", ethnicity="汉族", birth="1973年6月", birthplace="",
        education="大学学历、公共管理硕士(MPA)", party_join="中共党员（入党年月未公开）", work_start="1995年8月",
        current_post="东胜区委书记、鄂尔多斯高新技术产业开发区党工委书记",
        current_org="中共鄂尔多斯市东胜区委员会",
        source="鄂尔多斯高新区官网领导成员页（2026-05-27）/ ds.gov.cn 区委十届一次全会（2026-07-31）",
    ),
    dict(
        id=2, name="韩涛", gender="男", ethnicity="汉族", birth="1982年5月", birthplace="内蒙古自治区",
        education="内蒙古大学法学、公共管理硕士(MPA)", party_join="2000年10月", work_start="2005年7月",
        current_post="东胜区委副书记、区长、区政府党组书记",
        current_org="鄂尔多斯市东胜区人民政府",
        source="东胜区人民政府网简历（2026-04）/ 澎湃新闻、鄂尔多斯日报（2021-06-23）",
    ),
    dict(
        id=3, name="冀平", gender="男", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="东胜区人大常委会党组书记、主任", current_org="鄂尔多斯市东胜区人大常委会",
        source="ds.gov.cn 东胜区委书记专题会（2026-08-05）/ 区四大班子慰问（2026-07-31）",
    ),
    dict(
        id=4, name="阿拉腾敖日格乐", gender="男", ethnicity="蒙古族", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="东胜区政协党组书记、主席候选人", current_org="政协鄂尔多斯市东胜区委员会",
        source="ds.gov.cn 东胜区委书记专题会（2026-08-05）/ 区四大班子慰问（2026-07-31）",
    ),
    dict(
        id=5, name="吕向利", gender="男", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="东胜区委常委、区纪委书记、区监委主任", current_org="中共鄂尔多斯市东胜区纪律检查委员会",
        source="东胜区政府网东胜区纪委十届一次全会（2026-07-30）",
    ),
    dict(
        id=6, name="刘凤云", gender="男", ethnicity="汉族", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="东胜区长（前任）→ 现任鄂尔多斯市委常委、副市长", current_org="鄂尔多斯市人民政府",
        source="鄂尔多斯市政府任免报道（2026-07）/ 澎湃新闻、鄂尔多斯日报（2021-06-23）",
    ),
    dict(
        id=7, name="韩耀庭", gender="男", ethnicity="", birth="", birthplace="",
        education="", party_join="", work_start="",
        current_post="东胜区政协主席（前）", current_org="政协鄂尔多斯市东胜区委员会",
        source="东胜区政协/人大报道（2023卷2025）",
    ),
    dict(
        id=8, name="杜继宽", gender="男", ethnicity="汉族", birth="1979年10月", birthplace="",
        education="研究生学历，党员（2004-06）", party_join="2004年6月", work_start="2001年7月",
        current_post="东胜区委常委、区政府副区长（常务）", current_org="鄂尔多斯市东胜区人民政府",
        source="东胜区人民政府官网 领导之窗 履职信息（2026-06）",
    ),
    dict(
        id=9, name="张建功", gender="男", ethnicity="汉族", birth="1975年9月", birthplace="鄂尔多斯市东胜区",
        education="", party_join="", work_start="1998年8月",
        current_post="东胜区委常委、区政府副区长", current_org="鄂尔多斯市东胜区人民政府",
        source="东胜区人民政府官网 领导之窗 履职信息（2026-04）",
    ),
    dict(
        id=10, name="保积锴", gender="男", ethnicity="汉族", birth="1990年1月", birthplace="",
        education="研究生学历", party_join="2010年11月", work_start="2012年6月",
        current_post="东胜区人民政府副区长", current_org="鄂尔多斯市东胜区人民政府",
        source="东胜区人民政府官网 领导之窗 履职信息（2026-06）",
    ),
]

# ── Organizations ─────────────────────────────────────────────────────
organizations = [
    dict(id=1, name="中共鄂尔多斯市东胜区委员会", type="党委", level="市辖区", parent="中共鄂尔多斯市委员会", location="内蒙古鄂尔多斯市东胜区"),
    dict(id=2, name="鄂尔多斯市东胜区人民政府", type="政府", level="市辖区", parent="鄂尔多斯市人民政府", location="内蒙古鄂尔多斯市东胜区"),
    dict(id=3, name="鄂尔多斯市东胜区人大常委会", type="人大", level="市辖区", parent="鄂尔多斯市人大常委会", location="内蒙古鄂尔多斯市东胜区"),
    dict(id=4, name="政协鄂尔多斯市东胜区委员会", type="政协", level="市辖区", parent="鄂尔多斯市政协", location="内蒙古鄂尔多斯市东胜区"),
    dict(id=5, name="中共鄂尔多斯市东胜区纪律检查委员会", type="纪委", level="市辖区", parent="中共鄂尔多斯市纪律检查委员会", location="内蒙古鄂尔多斯市东胜区"),
    dict(id=6, name="鄂尔多斯高新技术产业开发区党工委", type="党委", level="市级开发区", parent="中共鄂尔多斯市委员会", location="内蒙古鄂尔多斯市东胜区"),
    dict(id=7, name="鄂尔多斯大路煤化工集团党工委", type="党委", level="市级园区", parent="中共鄂尔多斯市委员会", location="内蒙古鄂尔多斯市准格尔旗"),
    dict(id=8, name="共青团鄂尔多斯市委员会", type="群团", level="市级", parent="共青团内蒙古自治区委员会", location="内蒙古鄂尔多斯市"),
    dict(id=9, name="鄂尔多斯市人民政府", type="政府", level="地级市", parent="内蒙古自治区人民政府", location="内蒙古鄂尔多斯市"),
    dict(id=10, name="东胜经济开发区管委会", type="开发区", level="市辖区", parent="鄂尔多斯市人民政府", location="内蒙古鄂尔多斯市东胜区"),
]

# ── Positions ─────────────────────────────────────────────────────────
positions = [
    dict(person_id=1, org_id=1, title="东胜区委书记", start_date="（在任，2026-07-30 东胜区十次党代会当选）", end_date="present", rank="正处级", note="兼任鄂尔多斯高新技术产业开发区党工委书记"),
    dict(person_id=1, org_id=6, title="鄂尔多斯高新技术产业开发区党工委书记", start_date="（截至2026-05）", end_date="present", rank="正处级", note="主持高新区党工委全面工作"),
    dict(person_id=2, org_id=2, title="东胜区长", start_date="2021-07-09", end_date="present", rank="正处级", note="2021-06-23 任区委副书记、区长候选人；2021-07-09 人大常委会决定代区长"),
    dict(person_id=2, org_id=1, title="区委副书记", start_date="2021-06-23", end_date="present", rank="正处级", note="2021-06-23 干部大会宣布"),
    dict(person_id=2, org_id=7, title="鄂尔多斯大路煤化工集团党工委书记", start_date="2018-02", end_date="2021-06", rank="正处级", note="任东胜区长前之职（百科归集）"),
    dict(person_id=2, org_id=8, title="共青团鄂尔多斯市委员会书记", start_date="~2015", end_date="2018", rank="正处级", note="百科归集；王高祥2019接任团市委书记"),
    dict(person_id=2, org_id=10, title="东胜经济开发区管委会工作（后入鄂尔多斯市委办公厅）", start_date="2005-07", end_date="~2006", rank="", note="百科归集，早期经历"),
    dict(person_id=3, org_id=3, title="区人大常委会主任", start_date="（在任）", end_date="present", rank="正处级", note="区人大常委会党组书记"),
    dict(person_id=4, org_id=4, title="区政协主席（候选人）", start_date="2026", end_date="present", rank="正处级", note="区政协党组书记"),
    dict(person_id=5, org_id=5, title="区纪委书记、区监委主任", start_date="2026-07-30", end_date="present", rank="副处级", note="区第十届纪委全委会当选"),
    dict(person_id=6, org_id=9, title="鄂尔多斯市政府副市长", start_date="（在任）", end_date="present", rank="副厅级", note="曾任东胜区长 2026-07 市政府常务会议到会"),
    dict(person_id=6, org_id=2, title="东胜区长（前任）", start_date="", end_date="2021-06-23", rank="正处级", note="2021-06-23 免去东胜区长"),
    dict(person_id=7, org_id=4, title="区政协主席（前任）", start_date="", end_date="~2025", rank="正处级", note="换届卸任"),
    dict(person_id=8, org_id=2, title="区委常委、区政府副区长（常务）", start_date="（在任）", end_date="present", rank="副处级", note="分管发改、财政、金融、应急、协助区长工作；官方未书“常务”二字，按其职分推断"),
    dict(person_id=9, org_id=2, title="区委常委、区政府副区长", start_date="（在任）", end_date="present", rank="副处级", note="分管城建、人事、国资、规划等"),
    dict(person_id=10, org_id=2, title="区政府副区长", start_date="（在任）", end_date="present", rank="副处级", note="分管乡村振兴、农牧、民政等"),
]

# ── Relationships ─────────────────────────────────────────────────────
relationships = [
    dict(person_a=1, person_b=2, type="overlap", context="东胜区委书记—区长 党政正职搭档", overlap_org="中共鄂尔多斯市东胜区委员会 / 东胜区人民政府", overlap_period="2021至今"),
    dict(person_a=1, person_b=3, type="overlap", context="区委书记—区人大常委会主任", overlap_org="东胜区四大班子", overlap_period="在任"),
    dict(person_a=1, person_b=4, type="overlap", context="区委书记—区政协主席（候选人）", overlap_org="东胜区四大班子", overlap_period="2026"),
    dict(person_a=2, person_b=3, type="overlap", context="区长—区人大主任（任命程序）", overlap_org="东胜区人大常委会", overlap_period="2021至今"),
    dict(person_a=2, person_b=6, type="predecessor_successor", context="东胜区长 前任/新继任（刘凤云2021-06-23免，韩涛接）", overlap_org="东胜区人民政府", overlap_period="2021-06"),
    dict(person_a=1, person_b=6, type="overlap", context="高屹东任区委书记时刘凤云为当时区长", overlap_org="东胜区", overlap_period="~2021"),
    dict(person_a=5, person_b=1, type="superior_subordinate", context="区纪委书记—区委书记（纪委受区委领导）", overlap_org="中共鄂尔多斯东胜区委员会", overlap_period="2026-07至今"),
    dict(person_a=8, person_b=1, type="superior_subordinate", context="区委常委、常务副区长—区委书记（区委班子）", overlap_org="中共鄂尔多斯东胜区委员会", overlap_period="在任"),
    dict(person_a=8, person_b=2, type="superior_subordinate", context="常务副区长—区长（政府班子中枢）", overlap_org="东胜区人民政府", overlap_period="在任"),
    dict(person_a=9, person_b=2, type="superior_subordinate", context="区委常委、副区长—区长（政府班子）", overlap_org="东胜区人民政府", overlap_period="在任"),
    dict(person_a=10, person_b=2, type="superior_subordinate", context="副区长—区长（政府班子）", overlap_org="东胜区人民政府", overlap_period="在任"),
    dict(person_a=4, person_b=7, type="predecessor_successor", context="区政协主席接任（阿拉腾敖日格乐接韩耀庭）", overlap_org="政协鄂尔多斯东胜区委员会", overlap_period="~2026"),
    dict(person_a=2, person_b=7, type="overlap", context="区长—区政协主席（四大班子会）", overlap_org="东胜区政协", overlap_period="~2026"),
]


def build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络 (鄂尔多斯市 · 内蒙古自治区)")
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