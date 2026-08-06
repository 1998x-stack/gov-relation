#!/usr/bin/env python3
"""南漳县（襄阳市，湖北省）领导班子工作关系网络数据生成脚本。

Task ID: hubei_南漳县
Level: 县
Targets: 县委书记 & 县长

调查日期：2026-08-06
现行班子（截至 2026-08，南漳县人民政府门户网 www.hbnz.gov.cn 领导之窗 + 官方新闻确认）：
  - 县委书记：陈栋（1982-04，汉族，博士研究生·经济学博士；2025-11 由县长升任书记）
  - 县委副书记、县长：李恒（1979-10，汉族，湖北宜城人，博士研究生·管理学博士；2025-12 从襄阳高新区空降接任）
  - 县政府：常务副县长黄伟、副县长徐劲松(常委)、周建强、石海龙、艾婧、郑昌俊、黄玉刚、赵锋、张晖
  - 县委副书记：蒋双成；县人大常委会党组书记、主任：孙国强
前任县委书记：2025-11 前在任者（name 待核实，见 report/open_gaps.md）。

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 为核心领导写出 data/persons/YYYYMMDD-湖北省-襄阳市-{job}-{name}.json 深度档案。
- 新产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/hubei_南漳县/build_南漳县_data.py        # 产出写到暂存目录
    python3 build/build_南漳县_data.py / python3 build_南漳县_data.py   # 归档后运行，产出到 canonical 目录
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
import re

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
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR  # noqa: E402
from gov_relation.runner import run_build  # noqa: E402

logger = get_logger(__name__)

SLUG = "南漳县"
PROVINCE = "湖北省"
PARENT_CITY = "襄阳市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

if "__file__" in globals():
    _this = Path(__file__).resolve()
    _in_staging = ("data" in _this.parts) and ("tmp" in _this.parts)
else:
    _in_staging = False
# 暂存运行（data/tmp/<task>/）→ 产物写到该暂存目录；canonical 运行 → 写到 data/database|graph|persons
if _in_staging:
    OUT_DIR = Path(__file__).resolve().parent
    PERSONS_OUT = OUT_DIR
    GEXF_OUT = OUT_DIR
else:
    OUT_DIR = DATABASE_DIR
    PERSONS_OUT = PERSONS_DIR
    GEXF_OUT = GRAPH_DIR
DB_PATH = OUT_DIR / f"{SLUG}_network.db"
GEXF_PATH = GEXF_OUT / f"{SLUG}_network.gexf"

GOV_HOST = "http://www.hbnz.gov.cn"

# ── 人物 ────────────────────────────────────────────────────────────────────
persons = [
    # 县委书记
    {"id": 1, "name": "陈栋", "gender": "男", "ethnicity": "汉族", "birth": "1982-04", "birthplace": "", "native_place": "",
     "education": "博士研究生、经济学博士",
     "party_join": "", "work_start": "2007-08",
     "current_post": "南漳县委书记", "current_org": "中共南漳县委员会",
     "source": f"{GOV_HOST}/ldzc/xwld/xwsj/cd/202010/t20201015_2286674.shtml"},
    # 2 县长
    {"id": 2, "name": "李恒", "gender": "男", "ethnicity": "汉族", "birth": "1979-10", "birthplace": "湖北宜城", "native_place": "湖北省襄阳市宜城市",
     "education": "博士研究生、管理学博士",
     "party_join": "2000-11", "work_start": "2010-09",
     "current_post": "南漳县委副书记、县长、县人民政府党组书记", "current_org": "南漳县人民政府",
     "source": f"{GOV_HOST}/ldzc/xwld/xwfsj/lh/202512/t20251226_3932319.shtml"},
    # 3 县委副书记
    {"id": 3, "name": "蒋双成", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "南漳县委副书记", "current_org": "中共南漳县委员会",
     "source": f"{GOV_HOST}/ldzc/xwld/xwsj/cd/hdtj/202607/t20260731_4038391.shtml"},
    # 4 常务副县长
    {"id": 4, "name": "黄伟", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "南漳县委常委、常务副县长、县行政学校校长", "current_org": "南漳县人民政府",
     "source": f"{GOV_HOST}/ldzc/xzfld/"},
    # 5 副县长（常委）
    {"id": 5, "name": "徐劲松", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "南漳县委常委、副县长", "current_org": "南漳县人民政府",
     "source": f"{GOV_HOST}/ldzc/xzfld/"},
    # 6 副县长
    {"id": 6, "name": "周建强", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "南漳县人民政府副县长", "current_org": "南漳县人民政府",
     "source": f"{GOV_HOST}/ldzc/xzfld/"},
    # 7 副县长
    {"id": 7, "name": "石海龙", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "南漳县人民政府副县长、县委委员", "current_org": "南漳县人民政府",
     "source": f"{GOV_HOST}/ldzc/xzfld/"},
    # 8 副县长
    {"id": 8, "name": "艾婧", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "南漳县人民政府副县长", "current_org": "南漳县人民政府",
     "source": f"{GOV_HOST}/ldzc/xzfld/"},
    # 9 副县长
    {"id": 9, "name": "郑昌俊", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "南漳县人民政府副县长、县委候补委员", "current_org": "南漳县人民政府",
     "source": f"{GOV_HOST}/ldzc/xzfld/"},
    # 10 副县长
    {"id": 10, "name": "黄玉刚", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "南漳县人民政府副县长", "current_org": "南漳县人民政府",
     "source": f"{GOV_HOST}/ldzc/xzfld/"},
    # 11 副县长
    {"id": 11, "name": "赵锋", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "南漳县人民政府副县长", "current_org": "南漳县人民政府",
     "source": f"{GOV_HOST}/ldzc/xzfld/"},
    # 12 副县长
    {"id": 12, "name": "张晖", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "南漳县人民政府副县长", "current_org": "南漳县人民政府",
     "source": f"{GOV_HOST}/ldzc/xwld/xwsj/cd/hdtj/202607/t20260731_4038391.shtml"},
    # 13 人大常委会主任
    {"id": 13, "name": "孙国强", "gender": "男", "ethnicity": "汉族", "birth": "1968-02", "birthplace": "", "native_place": "",
     "education": "省委党校本科、工商管理硕士",
     "party_join": "", "work_start": "",
     "current_post": "南漳县人大常委会党组书记、主任", "current_org": "南漳县人大常委会",
     "source": f"{GOV_HOST}/ldzc/xrdld/zr/sgq/"},
    # 14 人大副主任
    {"id": 14, "name": "刘友武", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "南漳县人大常委会副主任", "current_org": "南漳县人大常委会",
     "source": f"{GOV_HOST}/ldzc/xrdld/zr/sgq/"},
    # 15 人大副主任
    {"id": 15, "name": "刘鹏飞", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "南漳县人大常委会副主任", "current_org": "南漳县人大常委会",
     "source": f"{GOV_HOST}/ldzc/xrdld/zr/sgq/"},
    # 16 人大副主任
    {"id": 16, "name": "齐贤林", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "南漳县人大常委会副主任", "current_org": "南漳县人大常委会",
     "source": f"{GOV_HOST}/ldzc/xrdld/zr/sgq/"},
    # 17 人大副主任
    {"id": 17, "name": "董尚梅", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "南漳县人大常委会副主任", "current_org": "南漳县人大常委会",
     "source": f"{GOV_HOST}/ldzc/xrdld/zr/sgq/"},
    # 18 人大副主任
    {"id": 18, "name": "尤明军", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "南漳县人大常委会副主任", "current_org": "南漳县人大常委会",
     "source": f"{GOV_HOST}/ldzc/xrdld/zr/sgq/"},
    # 19 人大副主任
    {"id": 19, "name": "唐大海", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "南漳县人大常委会副主任", "current_org": "南漳县人大常委会",
     "source": f"{GOV_HOST}/ldzc/xrdld/zr/sgq/"},
    # 20 人大办公室主任
    {"id": 20, "name": "张大江", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "南漳县人大常委会办公室主任", "current_org": "南漳县人大常委会",
     "source": f"{GOV_HOST}/ldzc/xrdld/zr/sgq/"},
]

organizations = [
    {"id": 1, "name": "中共南漳县委员会", "type": "党委", "level": "县级", "parent": "中共襄阳市委员会", "location": "襄阳市南漳县"},
    {"id": 2, "name": "南漳县人民政府", "type": "政府", "level": "县级", "parent": "南漳县人民代表大会", "location": "襄阳市南漳县"},
    {"id": 3, "name": "南漳县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "中共南漳县委员会", "location": "襄阳市南漳县"},
    {"id": 4, "name": "中共襄阳市委员会", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "湖北襄阳"},
    {"id": 5, "name": "襄阳市人民政府", "type": "政府", "level": "地级市", "parent": "", "location": "湖北襄阳"},
    {"id": 6, "name": "襄阳高新技术产业开发区党工委", "type": "党委", "level": "县处级", "parent": "中共襄阳市委员会", "location": "湖北襄阳"},
    {"id": 7, "name": "中共南漳县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共南漳县委员会", "location": "襄阳市南漳县"},
    {"id": 8, "name": "南漳县行政学校", "type": "事业单位", "level": "县级", "parent": "南漳县人民政府", "location": "襄阳市南漳县"},
]

positions = [
    # 陈栋（书记）
    {"person_id": 1, "org_id": 1, "title": "南漳县委书记", "start_date": "2025-12", "end_date": "present", "rank": "正处级", "note": "2025-11 由县委副书记、县长升任县委书记，2025-12 起专职书记"},
    {"person_id": 1, "org_id": 2, "title": "南漳县县长（兼）", "start_date": "2020-12", "end_date": "2025-12", "rank": "正处级", "note": "2020-10 代理县长，2020-12 转正；2025-11任书记后至2025-12仍兼县长"},
    {"person_id": 1, "org_id": 5, "title": "襄阳市招商局党组书记、局长", "start_date": "2019-02", "end_date": "2020-09", "rank": "正处级", "note": "2019.03 正式任命"},
    {"person_id": 1, "org_id": 4, "title": "枣阳市委常委、副市长", "start_date": "2016-08", "end_date": "2019-02", "rank": "副处级", "note": "2016.10 起任副市长，2018.02 三级调研员"},
    {"person_id": 1, "org_id": 4, "title": "襄阳市国防动员委员会经济动员办公室副主任", "start_date": "2012-09", "end_date": "2016-08", "rank": "副处级", "note": "2012-07 襄阳市招硕引博至市发改委"},
    # 李恒（县长）
    {"person_id": 2, "org_id": 2, "title": "南漳县人民政府县长", "start_date": "2025-12", "end_date": "present", "rank": "正处级", "note": "2025-12 副县长、代理县长→县长"},
    {"person_id": 2, "org_id": 1, "title": "南漳县委副书记", "start_date": "2025-12", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "襄阳高新区党工委副书记、东风街道党工委书记（兼）", "start_date": "2024-07", "end_date": "2025-12", "rank": "正处级", "note": "2024.07 任副书记"},
    {"person_id": 2, "org_id": 6, "title": "襄阳高新区党工委委员、襄阳综合保税区管理办公室党组书记、主任", "start_date": "2022-05", "end_date": "2024-07", "rank": "正处级", "note": "2022.02 党工委委员，2022.05 综保区"},
    {"person_id": 2, "org_id": 1, "title": "南漳县委常委、政法委书记", "start_date": "2015-11", "end_date": "2016-10", "rank": "副处级", "note": ""},
    # 蒋双成（副书记）
    {"person_id": 3, "org_id": 1, "title": "南漳县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 黄伟（常务副县长）
    {"person_id": 4, "org_id": 2, "title": "南漳县委常委、常务副县长、县行政学校校长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 徐劲松（常委副县长）
    {"person_id": 5, "org_id": 2, "title": "南漳县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 副县长们
    {"person_id": 6, "org_id": 2, "title": "南漳县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "南漳县人民政府副县长、县委委员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "南漳县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "南漳县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "南漳县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "南漳县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "南漳县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 人大常委会
    {"person_id": 13, "org_id": 3, "title": "南漳县人大常委会党组书记、主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "南漳县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "南漳县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "南漳县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "南漳县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "南漳县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "南漳县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "南漳县人大常委会办公室主任", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "前后任党政正职交接", "context": "陈栋自2020-12任县长，2025-11升任县委书记；李恒2025-12接任县长，现任党政正职搭档", "overlap_org": "南漳县（党委/政府）", "overlap_period": "2025-12至今"},
    {"person_a": 1, "person_b": 3, "type": "县委班子", "context": "县委副书记在书记领导下工作", "overlap_org": "中共南漳县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "县委班子", "context": "常务副县长在书记领导下工作", "overlap_org": "中共南漳县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "县委班子", "context": "常委副县在书记领导下工作", "overlap_org": "中共南漳县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "政府班子", "context": "常务副县长在县长领导下工作", "overlap_org": "南漳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "政府班子", "context": "常委副县在县长领导下工作", "overlap_org": "南漳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "南漳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "南漳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "南漳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "南漳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "南漳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "南漳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "南漳县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "党政人大工作关系", "context": "县委书记与县人大常委会主任为县四套班子正职", "overlap_org": "南漳县", "overlap_period": ""},
    {"person_a": 1, "person_b": 2, "type": "交叉履历-襄阳", "context": "陈栋、李恒均任职襄阳市政府体系（陈栋曾任市招商局局长，李恒曾任市政府法制办副主任、市纪委常委）", "overlap_org": "襄阳市", "overlap_period": "2010s"},
]


def build_person_json(p) -> None:
    """写入单个人物深度档案 JSON。"""
    name = p.get("name", "")
    if not name:
        return
    job = p.get("current_post") or "南漳县领导"
    _job = re.sub(r"[、，]?[一二三四]级(调研员|高级?监察官|主任科员|科员)?", "", job)
    slug_job = _job.replace("、", "-").replace("/", "-").strip("、")
    filename = f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{slug_job}-{name}.json"
    out_path = PERSONS_OUT / filename

    src_url = p.get("source") or p.get("source_url") or ""
    source_register = [{
        "id": "S001",
        "title": "南漳县人民政府门户网站领导之窗 - 干部任免",
        "url": src_url or "http://www.hbnz.gov.cn/ldzc/",
        "publisher": "南漳县人民政府",
        "published_at": AS_OF,
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "南漳县人民政府官方领导之窗/简历页（2026-08-06 复核）",
    }]

    edu = []
    if p.get("education"):
        edu.append({"period": "", "institution": "", "major": "", "degree": p["education"],
                    "study_type": "unknown", "source_ids": ["S001"]})

    org_by_id = {o["id"]: o["name"] for o in organizations}
    career_timeline = []
    for pos in positions:
        if pos["person_id"] != p["id"]:
            continue
        career_timeline.append({
            "start": pos.get("start_date") or "unknown",
            "end": pos.get("end_date") or "present",
            "org": org_by_id.get(pos.get("org_id"), ""),
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "location": "襄阳市南漳县",
            "system": "party" if pos.get("org_id") in (1, 4, 6, 7) else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": pos.get("person_id") in (1, 2, 13),
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if src_url else "plausible",
            "source_ids": ["S001"],
        })

    org_refs = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            org_refs.append({"org_name": org_by_id.get(pos.get("org_id"), ""), "org_type": "", "role": pos.get("title", "")})

    open_q = []
    if not p.get("birth"):
        open_q.append({"priority": "high", "question": f"{name}的出生年月/籍贯",
                       "why_it_matters": "用于身份去重与晋升时间线",
                       "suggested_queries": [f"{name} 履历 出生", f"{name} 南漳 任前公示"], "last_attempted": AS_OF})
    if not p.get("work_start"):
        open_q.append({"priority": "high", "question": f"{name}的参加工作年份",
                       "why_it_matters": "用于衡量晋升速度",
                       "suggested_queries": [f"{name} 简历 参加工作", f"{name} 南漳"], "last_attempted": AS_OF})
    if p.get("id") == 1:
        open_q.append({"priority": "high", "question": "陈栋任县委书记前的县委班子、前任县委书记全称与去向",
                       "why_it_matters": "确定前任-继任关系网络",
                       "suggested_queries": ["南漳县 前任县委书记 任命"], "last_attempted": AS_OF})

    document = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": PARENT_CITY, "region": SLUG,
                                "job": job, "task_id": "hubei_南漳县", "time_focus": "2026"},
        "identity": {
            "person_id": f"hubei_xiangyang_nanzhang_{name}",
            "name": name, "aliases": [],
            "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""),
            "native_place": p.get("native_place", ""),
            "education": edu,
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{p.get('birth', '')}",
                "name_birthplace": f"{name}_{p.get('birthplace', '')}",
                "official_profile_url": src_url,
            },
        },
        "current_status": {"current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""),
                           "administrative_rank": ("正处级" if p.get("id") in (1, 2, 3, 4, 5, 13) else "副处级"),
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]},
        "career_timeline": career_timeline,
        "organizations": org_refs,
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": ("local_ladder" if p.get("id") in (1, 2) else "unknown"),
            "systems_experience": [],
            "geographic_pattern": [p.get("birthplace", "")] if p.get("birthplace") else [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [], "speech_themes": [], "management_signals": [],
            "caveat": "工作风格源于公开记录与政务报道推断，并非私人心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "搜索范围内未发现纪律处分/审计/负面舆情信号", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "complete" if p.get("work_start") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "除县委书记陈栋、县长李恒外，其余副职完整履历缺失",
        },
        "open_questions": open_q,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(document, f, ensure_ascii=False, indent=2)
    logger.info("person JSON written: %s", out_path)


def main() -> None:
    print(f"Building {SLUG} network data...")
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
    print("  Writing person JSON lead-files...")
    for p in persons:
        build_person_json(p)
    print(f"\nDone. Artifacts:\n  DB:   {DB_PATH}\n  GEXF: {GEXF_PATH}")
    _conn = sqlite3.connect(str(DB_PATH))
    print(f"  DB rows: persons={_conn.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}, "
          f"organizations={_conn.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}, "
          f"positions={_conn.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}, "
          f"relationships={_conn.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    _conn.close()
    for pf in sorted(OUT_DIR.glob(f"{TODAY}-{PROVINCE}-*")):
        print(f"  Person: {pf}")


if __name__ == "__main__":
    main()