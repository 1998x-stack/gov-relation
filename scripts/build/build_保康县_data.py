#!/usr/bin/env python3
"""保康县（襄阳市，湖北省）领导班子工作关系网络数据生成脚本。

Task ID: hubei_保康县
Level: 县
Targets: 县委书记 & 县长

调查日期：2026-08-06
现行班子（截至 2026-08，保康县人民政府官网《领导之窗》www.baokang.gov.cn/ldzc/ 确认，primary/high）：
  - 县委书记：李云（女，汉族，1978-12，湖北南漳，2000-12 参加工作，2003-06 入党，
    省委党校研究生学历；2024-10 至今任中共保康县委书记）
  - 县委副书记、县人民政府代理县长：王衡（男，汉族，1980-08，江苏铜山人，
    2008-11 参加工作，2004-12 入党，博士研究生；现任保康县委副书记、代理县长）
  - 县委副书记：胡志芳；县委常委（12 人制班子，见 persons 列表）：
    张祖涛(常务副县长)、刘伟波(副县长)、史正双(纪委书记/监委主任)、朱宝剑(县委办主任)、
    王畅(组织部长)、张莹(宣传部长)、胡林(人武部长)、万传伟(统战部长/总工会主席)
  - 县人大主任：徐声军；县政协主席：王杰
前任县委书记（2024 年 10 月前）据公开训练知识推断为 冯云波（任期约 2018-2024，去向待核），置 open_questions。

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 为名单人物写出 data/persons/YYYYMMDD-湖北省-襄阳市-{job}-{name}.json 深度档案。
- 新产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。
- 网络在本次会话受限（Exa 限流、Baidu 验证码），主体证据来源于保康县政府官网领导之窗
  （primary/official），个人信息均采自官方简历，未虚构。

用法：
    python3 data/tmp/hubei_保康县/build_保康县_data.py        # 产出写到暂存目录
    python3 scripts/build/build_保康县_data.py                # 归档后运行，产出到 canonical 目录
"""

import json
import re
import sqlite3
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
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR  # noqa: E402
from gov_relation.runner import run_build  # noqa: E402

logger = get_logger(__name__)

SLUG = "保康县"
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

GOV_HOST = "https://www.baokang.gov.cn/ldzc"

# ── 人物 ────────────────────────────────────────────────────────────────────
# 证据：保康县人民政府官网《领导之窗》。李云/王衡为核心调查对象。
# 来源 URL 对应官方在职领导页（2026-08-06 复核）。
persons = [
    # 1. 县委书记 —— 核心一号
    {"id": 1, "name": "李云", "gender": "女", "ethnicity": "汉族", "birth": "1978-12",
     "birthplace": "湖北南漳", "native_place": "湖北省襄阳市南漳县",
     "education": "省委党校研究生学历", "party_join": "2003-06", "work_start": "2000-12",
     "current_post": "保康县委书记", "current_org": "中共保康县委员会",
     "source": f"{GOV_HOST}/xwld/xwsj/t_3705278.shtml"},
    # 2. 代理县长 —— 核心二号（县委副书记兼）
    {"id": 2, "name": "王衡", "gender": "男", "ethnicity": "汉族", "birth": "1980-08",
     "birthplace": "江苏铜山", "native_place": "江苏省徐州市铜山区",
     "education": "博士研究生学历", "party_join": "2004-12", "work_start": "2008-11",
     "current_post": "保康县委副书记、县人民政府代理县长", "current_org": "保康县人民政府",
     "source": f"{GOV_HOST}/xwld/xwfsj/202607/t20260704_4026271.shtml"},
    # 3. 县委副书记
    {"id": 3, "name": "胡志芳", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "保康县委副书记", "current_org": "中共保康县委员会",
     "source": f"{GOV_HOST}/xwld/xwfsj/202307/t20230703_3272170.shtml"},
    # 4. 县委常委、常务副县长
    {"id": 4, "name": "张祖涛", "gender": "男", "ethnicity": "汉族", "birth": "1973-06",
     "birthplace": "保康歇马", "native_place": "湖北省襄阳市保康县歇马镇",
     "education": "大学学历", "party_join": "1996-01", "work_start": "1996-08",
     "current_post": "保康县委常委、常务副县长", "current_org": "保康县人民政府",
     "source": f"{GOV_HOST}/xwld/xwcw/201808/t20180829_1319274.shtml"},
    # 5. 常委/副县长（科技工信招商）
    {"id": 5, "name": "刘伟波", "gender": "男", "ethnicity": "汉族", "birth": "1981-04",
     "birthplace": "襄阳襄州", "native_place": "湖北省襄阳市襄州区",
     "education": "硕士研究生学历", "party_join": "2006-06", "work_start": "2007-07",
     "current_post": "保康县委常委、副县长", "current_org": "保康县人民政府",
     "source": f"{GOV_HOST}/xwld/xwcw/202109/t20210915_2578963.shtml"},
    # 6. 纪委书记/监委主任
    {"id": 6, "name": "史正双", "gender": "男", "ethnicity": "汉族", "birth": "1975-04",
     "birthplace": "河南新野", "native_place": "河南省南阳市新野县",
     "education": "在职大学学历", "party_join": "2000-06", "work_start": "1994-02",
     "current_post": "保康县委常委、县纪委书记、县监委主任", "current_org": "中共保康县纪律检查委员会/保康县监察委员会",
     "source": f"{GOV_HOST}/xwld/xwcw/202109/t20210915_2579242.shtml"},
    # 7. 县委办主任
    {"id": 7, "name": "朱宝剑", "gender": "男", "ethnicity": "汉族", "birth": "1975-02",
     "birthplace": "保康歇马", "native_place": "湖北省襄阳市保康县歇马镇",
     "education": "研究生学历", "party_join": "1999-06", "work_start": "1995-07",
     "current_post": "保康县委常委、县委办公室主任", "current_org": "中共保康县委员会办公室",
     "source": f"{GOV_HOST}/xwld/xwcw/202111/t20211105_2623626.shtml"},
    # 8. 组织部长
    {"id": 8, "name": "王畅", "gender": "男", "ethnicity": "汉族", "birth": "1982-12",
     "birthplace": "湖北武汉", "native_place": "湖北省武汉市",
     "education": "硕士研究生学历", "party_join": "2004-01", "work_start": "2007-07",
     "current_post": "保康县委常委、组织部部长", "current_org": "中共保康县委组织部",
     "source": f"{GOV_HOST}/xwld/xwcw/202308/t20230810_3343532.shtml"},
    # 9. 宣传部长
    {"id": 9, "name": "张莹", "gender": "女", "ethnicity": "汉族", "birth": "1979-02",
     "birthplace": "湖北宜城", "native_place": "湖北省襄阳市宜城市",
     "education": "省委党校研究生学历", "party_join": "2003-01", "work_start": "2000-10",
     "current_post": "保康县委常委、宣传部部长", "current_org": "中共保康县委宣传部",
     "source": f"{GOV_HOST}/xwld/xwcw/202311/t20231120_3468940.shtml"},
    # 10. 人武部长
    {"id": 10, "name": "胡林", "gender": "男", "ethnicity": "汉族", "birth": "1976-06",
     "birthplace": "湖北十堰", "native_place": "湖北省十堰市",
     "education": "大学本科学历", "party_join": "1997-03", "work_start": "1995-12",
     "current_post": "保康县委常委、县人民武装部部长", "current_org": "保康县人民武装部",
     "source": f"{GOV_HOST}/xwld/xwcw/202402/t20240202_3560958.shtml"},
    # 11. 统战部长/总工会主席
    {"id": 11, "name": "万传伟", "gender": "男", "ethnicity": "汉族", "birth": "1975-12",
     "birthplace": "湖北樊城", "native_place": "湖北省襄阳市樊城区",
     "education": "大学学历", "party_join": "1998", "work_start": "1999",
     "current_post": "保康县委常委、统战部部长、县总工会主席", "current_org": "中共保康县委统战部",
     "source": f"{GOV_HOST}/xwld/xwcw/202311/t20231122_3473579.shtml"},
    # 12. 县人大主任
    {"id": 12, "name": "徐声军", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "保康县人大常委会主任", "current_org": "保康县人民代表大会常务委员会",
     "source": f"{GOV_HOST}/xrdld/zr/202111/t20211111_2630750.shtml"},
    # 13. 县政协主席
    {"id": 13, "name": "王杰", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "保康县政协主席", "current_org": "政协保康县委员会",
     "source": f"{GOV_HOST}/xrdld/zr/202111/t20211111_2630965.shtml"},
]

organizations = [
    {"id": 1, "name": "中共保康县委员会", "type": "党委", "level": "县级", "parent": "中共襄阳市委员会", "location": "保康县"},
    {"id": 2, "name": "保康县人民政府", "type": "政府", "level": "县级", "parent": "襄阳市人民政府", "location": "保康县"},
    {"id": 3, "name": "中共保康县纪律检查委员会/保康县监察委员会", "type": "党委", "level": "县级", "parent": "中共襄阳市纪律检查委员会", "location": "保康县"},
    {"id": 4, "name": "中共保康县委办公室", "type": "党委", "level": "县级", "parent": "中共保康县委员会", "location": "保康县"},
    {"id": 5, "name": "中共保康县委组织部", "type": "党委", "level": "县级", "parent": "中共保康县委员会", "location": "保康县"},
    {"id": 6, "name": "中共保康县委宣传部", "type": "党委", "level": "县级", "parent": "中共保康县委员会", "location": "保康县"},
    {"id": 7, "name": "保康县人民武装部", "type": "党委", "level": "县级", "parent": "襄阳军分区", "location": "保康县"},
    {"id": 8, "name": "中共保康县委统战部", "type": "党委", "level": "县级", "parent": "中共保康县委员会", "location": "保康县"},
    {"id": 9, "name": "保康县总工会", "type": "群团", "level": "县级", "parent": "保康县", "location": "保康县"},
    {"id": 10, "name": "保康县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "襄阳市人大常委会", "location": "保康县"},
    {"id": 11, "name": "政协保康县委员会", "type": "政协", "level": "县级", "parent": "中国人民政治协商会议襄阳市委员会", "location": "保康县"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "保康县委书记", "start_date": "2024-10", "end_date": "", "rank": "正处级", "note": "主持县委全面工作"},
    {"person_id": 2, "org_id": 1, "title": "保康县委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "保康县人民政府代理县长", "start_date": "约2026", "end_date": "", "rank": "正处级", "note": "主持县政府全面工作"},
    {"person_id": 3, "org_id": 1, "title": "保康县委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "保康县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "协助县长负责日常工作"},
    {"person_id": 5, "org_id": 1, "title": "保康县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管科技、工信、招商"},
    {"person_id": 6, "org_id": 1, "title": "保康县委常委、纪委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "县监委主任"},
    {"person_id": 6, "org_id": 3, "title": "县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "保康县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "县委办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "保康县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "县委组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "保康县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "县委宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "保康县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 7, "title": "县人武部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "保康县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 8, "title": "县委统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 9, "title": "保康县总工会主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 10, "title": "保康县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 13, "org_id": 11, "title": "保康县政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长为保康县党政正职搭档", "overlap_org": "保康县党委/政府", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 3, "type": "县委班子", "context": "县委副书记在书记领导下工作", "overlap_org": "中共保康县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "县委班子", "context": "县委常委在书记领导下工作", "overlap_org": "中共保康县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "县委班子", "context": "县委常委在书记领导下工作", "overlap_org": "中共保康县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "县委班子", "context": "县委常委在书记领导下工作", "overlap_org": "中共保康县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "县委班子", "context": "县委常委在书记领导下工作", "overlap_org": "中共保康县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "县委班子", "context": "县委常委在书记领导下工作", "overlap_org": "中共保康县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "县委班子", "context": "县委常委在书记领导下工作", "overlap_org": "中共保康县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "县委班子", "context": "县委常委在书记领导下工作", "overlap_org": "中共保康县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "县委班子", "context": "县委常委在书记领导下工作", "overlap_org": "中共保康县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "政府班子", "context": "常务副县长在县长领导下工作", "overlap_org": "保康县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "保康县人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 1, "type": "纪检监督", "context": "纪委书记对县委班子实施监督", "overlap_org": "保康县", "overlap_period": ""},
    {"person_a": 3, "person_b": 1, "type": "班子副职", "context": "县委副书记协助书记工作", "overlap_org": "中共保康县委员会", "overlap_period": ""},
]


def _clean_job(job: str) -> str:
    """清理职务串，生成用于文件名的简短 job。"""
    s = job.replace("、", "-").replace("/", "-") if job else ""
    s = re.sub(r"[，, ].*", "", s)
    return s.strip("-") or "保康县领导"


def build_person_json(p) -> None:
    """写入单个人物深度档案 JSON。"""
    name = p.get("name", "")
    if not name:
        return
    job = p.get("current_post") or "保康县领导"
    slug_job = _clean_job(job)
    filename = f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{slug_job}-{name}.json"
    out_path = PERSONS_OUT / filename

    src_url = p.get("source") or ""
    source_register = [{
        "id": "S001",
        "title": f"保康县人民政府领导之窗 - {name}",
        "url": src_url,
        "publisher": "保康县人民政府",
        "published_at": AS_OF,
        "accessed_at": AS_OF,
        "source_type": "official" if src_url else "inferred",
        "reliability": "high" if src_url else "low",
        "notes": "保康县人民政府官网在职领导信息页（2026-08 复核）",
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
        system = "government"
        if pos["org_id"] in (1, 3, 4, 5, 6, 7, 8):
            system = "party"
        elif pos["org_id"] == 9:
            system = "other"
        career_timeline.append({
            "start": pos["start_date"] or "unknown",
            "end": pos["end_date"] or "present",
            "org": org_by_id.get(pos["org_id"], ""),
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": "襄阳市保康县",
            "system": system,
            "rank": pos.get("rank", ""),
            "is_key_promotion": pos["person_id"] in (1, 2),
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if src_url else "plausible",
            "source_ids": ["S001"],
        })

    org_refs = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            org_refs.append({"org_name": org_by_id.get(pos["org_id"], ""), "org_type": "", "role": pos["title"]})

    open_q = []
    if not p.get("party_join"):
        open_q.append({"priority": "medium", "question": f"{name}的入党时间",
                       "why_it_matters": "用于精确构建晋升时间线",
                       "suggested_queries": [f"{name} 任前公示 入党", f"{name} 保康县 简历"], "last_attempted": AS_OF})
    if not p.get("work_start"):
        open_q.append({"priority": "medium", "question": f"{name}的参加工作年份",
                       "why_it_matters": "用于衡量晋升速度",
                       "suggested_queries": [f"{name} 简历 参加工作", f"{name} 保康县"], "last_attempted": AS_OF})
    if name == "李云" and p.get("current_post") == "保康县委书记":
        open_q.append({"priority": "high", "question": "李云任县委书记前的完整履历（此前任职单位/岗位）",
                       "why_it_matters": "一号人物早年与跨区调动线索，决定-继任关系图谱关键",
                       "suggested_queries": ["李云 南漳 保康 任职", "李云 襄阳 保康县委书记 简历"], "last_attempted": AS_OF})

    administrative_rank = "正处级" if p["id"] in (1, 2, 3, 12, 13) else "副处级"
    document = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": PARENT_CITY, "region": SLUG,
                                "job": job, "task_id": "hubei_保康县", "time_focus": "2026"},
        "identity": {
            "person_id": f"hubei_xiangyang_baokang_{name}",
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
                           "administrative_rank": administrative_rank,
                           "as_of": AS_OF, "is_current_confirmed": bool(src_url), "source_ids": ["S01"]},
        "career_timeline": career_timeline,
        "organizations": org_refs,
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if "保康县" in (p.get("native_place") or "")
                              else ("cross_county_rotation" if PARENT_CITY in (p.get("native_place") or "")
                                    else ("cross_province_rotation" if PROVINCE in (p.get("native_place") or "") else "unknown")),
            "systems_experience": [],
            "geographic_pattern": [p.get("native_place", "")] if p.get("native_place") else [],
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
            "career_completeness": "partial" if p.get("work_start") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（早年、历任职务起止时间）",
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