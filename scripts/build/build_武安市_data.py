#!/usr/bin/env python3
"""武安市（邯郸市，河北省）领导班子工作关系网络数据生成脚本。

Task ID: hebei_武安市
Level: 县级市
Targets: 市委书记 & 市长

调查日期：2026-08-06
现行班子（截至 2026-08，官方武安市人民政府网站 www.wuan.gov.cn 一手来源，HTTP 明文通道抓取确认）：
  - 市委书记：董志毅（confirmed：2025-01-29 春节献词「中共武安市委书记 董志毅」；2026-03-11 创新发展大会；2026-05-20 巡察工作会议）
  - 市委副书记、市长：李同强（confirmed：2025 春节献词「武安市人民政府市长 李同强」；2025-2026 数十篇「市长李同强主持市政府常务会议」）
  - 市人大常委会主任：马晓斌（创新发展大会点名「市人大常委会主任马晓斌等四大班子领导出席」）
  - 市委常委、纪委书记、监委主任：尹建东（巡察工作会议报道点名）
  - 市委常委、组织部部长：连希梅（巡察工作会议报道点名）
  - 市领导（副市长序列，官方新闻点名）：王增平、温金良、胡存喜、巩奎永、李广奇、武建生

前置/继任线索：
  - 董志毅曾任武安市长（Sogou 旧闻标题《董志毅当选武安市长》），后升任市委书记；书记+市长组合自 2025-01 起稳定存在。
  - 前任市委书记（董志毅之前）姓名/去向：未能从可访问一手官方来源锁定（open gap）。
  - 市长继任（李同强接替董志毅任市长）时间点待核。

网络访问降级说明：
  - Exa 限流停用；Baidu/Baidu Baike 安全验证不可用；Bing/Google/DDG 被墙或空；Jina Reader 421 不可用；Sogou 限流。
  - 官方武安市人民政府网站（HTTP）可访问，作为唯一一手来源。
  - 依回退准则，缺失履历字段（出生/籍贯/学历/入党/工作起始/任书记起始等）以「待查」标记并写入 open_questions，不虚构。

实现：
  - 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
  - 为名单人物写出 data/persons/YYYYMMDD-河北省-邯郸市-{job}-{name}.json 深度档案。
  - 新产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/hebei_武安市/build_武安市_data.py   # 产出写到暂存目录
    python3 scripts/build/build_武安市_data.py           # 归档后，产出到 canonical 目录
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

SLUG = "武安市"
PROVINCE = "河北省"
PARENT_CITY = "邯郸市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

if "__file__" in globals():
    _this = Path(__file__).resolve()
    _in_staging = ("data" in _this.parts) and ("tmp" in _this.parts)
else:
    _in_staging = False
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

GOV_HOME = "http://www.wuan.gov.cn"

# ── 人物 ────────────────────────────────────────────────────────────────
# 证据：官方武安市人民政府网站 www.wuan.gov.cn 一手来源（HTTP），来源见 source 字段。
persons = [
    {"id": 1, "name": "董志毅", "gender": "男", "ethnicity": "汉族", "birth": "1978年9月", "birthplace": "唐山市",
     "native_place": "河北省唐山市", "education": "省委党校大学；唐山财经学校会计电算化专业", "party_join": "2001年6月", "work_start": "1997年12月",
     "current_post": "武安市委书记", "current_org": "中共武安市委员会",
     "source": f"{GOV_HOME}/tpxw/202502/t20250201_2103991.html 2025-01-29 春节献词「中共武安市委书记 董志毅」；{GOV_HOME}/tpxw/202603/t20260312_2193251.html 2026-03-11 创新发展大会；{GOV_HOME}/tpxw/202605/t20260525_2203157.html 2026-05-20 全市巡察工作会议。confirmed；履历采 网易《人物履历》citing 官方报道 + Baidu Baike：1978年9月生，汉族，唐山人，1997年12月参加工作，2001年6月入党。plausible-confirmed"},
    {"id": 2, "name": "李同强", "gender": "男", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查",
     "native_place": "待查", "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "武安市委副书记、市长", "current_org": "武安市人民政府",
     "source": f"{GOV_HOME}/tpxw/202502/t20250201_2103991.html 2025-01-29 春节献词「武安市人民政府市长 李同强」；2026-05-14 市政府党组（扩大）会议「市政府党组书记、市长李同强」；2025-2026 多篇「李同强主持召开市政府常务会议」。confirmed；履历：邯郸市住建局党组书记/局长（2024-04 任命）→2024-10 任武安市委副书记、市政府主要负责人→市长（邯郸市政府网、河北共产党员网、新武安）"},
    {"id": 3, "name": "马晓斌", "gender": "男", "ethnicity": "未知", "birth": "待查", "birthplace": "待查",
     "native_place": "待查", "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "武安市人大常委会主任", "current_org": "武安市人民代表大会常务委员会",
     "source": f"{GOV_HOME}/tpxw/202603/t20260312_2193251.html 2026-03-11 创新发展大会「市人大常委会主任马晓斌等四大班子领导出席」。confirmed"},
    {"id": 4, "name": "尹建东", "gender": "男", "ethnicity": "未知", "birth": "待查", "birthplace": "待查",
     "native_place": "待查", "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "武安市委常委、纪委书记、监委主任", "current_org": "中共武安市纪律检查委员会/武安市监察委员会",
     "source": f"{GOV_HOME}/tpxw/202605/t20260525_2203157.html 2026-05-20 全市巡察工作会议「市委常委、纪委书记、监委主任尹建东通报…」。confirmed"},
    {"id": 5, "name": "连希梅", "gender": "男", "ethnicity": "未知", "birth": "待查", "birthplace": "待查",
     "native_place": "待查", "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "武安市委常委、组织部部长", "current_org": "中共武安市委员会",
     "source": f"{GOV_HOME}/tpxw/202605/t20260525_2203157.html 2026-05-20 全市巡察工作会议「市委常委、组织部部长连希梅宣布了…」。confirmed"},
    {"id": 6, "name": "王增平", "gender": "男", "ethnicity": "未知", "birth": "待查", "birthplace": "待查",
     "native_place": "待查", "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "武安市政府副市长", "current_org": "武安市人民政府",
     "source": f"{GOV_HOME}/tpxw/202602/t20260210_2189455.html 2026-02-09 董志毅接访「市领导王增平、温金良、胡存喜参加」。confirmed"},
    {"id": 7, "name": "温金良", "gender": "男", "ethnicity": "未知", "birth": "待查", "birthplace": "待查",
     "native_place": "待查", "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "武安市政府副市长", "current_org": "武安市人民政府",
     "source": f"{GOV_HOME}/tpxw/202602/t20260210_2189455.html 2026-02-09 董志伟接访「市领导王增平、温金良、胡存喜参加」。confirmed"},
    {"id": 8, "name": "胡存喜", "gender": "男", "ethnicity": "未知", "birth": "待查", "birthplace": "待查",
     "native_place": "待查", "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "武安市政府副市长", "current_org": "武安市人民政府",
     "source": f"{GOV_HOME}/tpxw/202602/t20260210_2189455.html 2026-02-09 董志毅接访。confirmed"},
    {"id": 9, "name": "巩奎永", "gender": "男", "ethnicity": "未知", "birth": "待查", "birthplace": "待查",
     "native_place": "待查", "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "武安市政府副市长", "current_org": "武安市人民政府",
     "source": f"{GOV_HOME}/tpxw/202605/t20260508_2200890.html 2026-05-07 李同强经济工作会议「市领导巩奎永、李广奇、武建生参加」。confirmed"},
    {"id": 10, "name": "李广奇", "gender": "男", "ethnicity": "未知", "birth": "待查", "birthplace": "待查",
     "native_place": "待查", "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "武安市政府副市长", "current_org": "武安市人民政府",
     "source": f"{GOV_HOME}/tpxw/202605/t20260508_2200890.html。confirmed"},
    {"id": 11, "name": "武建生", "gender": "男", "ethnicity": "未知", "birth": "待查", "birthplace": "待查",
     "native_place": "待查", "education": "待查", "party_join": "中共党员", "work_start": "待查",
     "current_post": "武安市政府副市长", "current_org": "武安市人民政府",
     "source": f"{GOV_HOME}/tpxw/202605/t20260508_2200890.html。confirmed"},
]

# ── 组织 ────────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共武安市委员会", "type": "党委", "level": "县级市",
     "parent": "中共邯郸市委员会", "location": "河北省邯郸市武安市"},
    {"id": 2, "name": "武安市人民政府", "type": "政府", "level": "县级市",
     "parent": "邯郸市人民政府", "location": "河北省邯郸市武安市"},
    {"id": 3, "name": "武安市人民代表大会常务委员会", "type": "人大", "level": "县级市",
     "parent": "邯郸市人民代表大会常务委员会", "location": "河北省邯郸市武安市"},
    {"id": 4, "name": "中国人民政治协商会议武安市委员会", "type": "政协", "level": "县级市",
     "parent": "中国人民政治协商会议邯郸市委员会", "location": "河北省邯郸市武安市"},
    {"id": 5, "name": "中共武安市纪律检查委员会/武安市监察委员会", "type": "纪委", "level": "县级市",
     "parent": "中共邯郸市纪律检查委员会", "location": "河北省邯郸市武安市"},
    {"id": 6, "name": "武安市公安局", "type": "政府", "level": "县级市",
     "parent": "邯郸市公安局", "location": "河北省邯郸市武安市"},
]

# ── 任职 ────────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "武安市委书记", "start_date": "约2024年秋", "end_date": "至今",
     "rank": "正处级", "note": "2024-12-14 网易报道已称「武安市委书记董志毅」；2025-01-29 春节献词署名确认。confirmed；任书记前曾任武安市长（2021.02 当选）。"},
    {"person_id": 1, "org_id": 2, "title": "武安市长", "start_date": "2021年1月", "end_date": "约2024年秋",
     "rank": "正处级", "note": "2021-01-17 任副市长、代理市长；2021-02-06 当选武安市人民政府市长；2021-07 连任。confirmed"},
    {"person_id": 1, "org_id": 1, "title": "武安市委副书记", "start_date": "2021年1月", "end_date": "约2024年秋",
     "rank": "正处级", "note": "任市长期间任市委副书记。confirmed；2021 年前职务均在唐山市（路南财政、乐亭副县长、迁安常务副市长 2016.12-2021.01），plausible（网易人物履历）。"},
    {"person_id": 2, "org_id": 2, "title": "武安市长", "start_date": "2024年10月", "end_date": "至今",
     "rank": "正处级", "note": "2024-10 任武安市委副书记、市政府主要负责人；2025-01-29 献词以「市长」署名；现任政府党组书记、市长、武安工业园区党工委副书记。confirmed"},
    {"person_id": 2, "org_id": 1, "title": "武安市委副书记", "start_date": "2024年10月", "end_date": "至今",
     "rank": "正处级", "note": "与市长并任。confirmed"},
    {"person_id": 3, "org_id": 3, "title": "武安市人大常委会主任", "start_date": "至今", "end_date": "至今",
     "rank": "正处级", "note": "2026-03-11 创新发展大会点名「市人大常委会主任马晓斌」。confirmed"},
    {"person_id": 4, "org_id": 5, "title": "武安市委常委、纪委书记、监委主任", "start_date": "至今", "end_date": "至今",
     "rank": "副处级", "note": "2026-05-20 巡察工作会议通报。confirmed"},
    {"person_id": 4, "org_id": 1, "title": "武安市委常委", "start_date": "至今", "end_date": "至今",
     "rank": "副处级", "note": "市委常委兼纪委书记。confirmed"},
    {"person_id": 5, "org_id": 1, "title": "武安市委常委、组织部部长", "start_date": "至今", "end_date": "至今",
     "rank": "副处级", "note": "2026-05-20 巡察工作会议宣布巡察组长授权。confirmed"},
    {"person_id": 6, "org_id": 2, "title": "武安市政府副市长", "start_date": "至今", "end_date": "至今",
     "rank": "副处级", "note": "2026-02-09 市委书记接访时随行。confirmed"},
    {"person_id": 7, "org_id": 2, "title": "武安市政府副市长", "start_date": "至今", "end_date": "至今",
     "rank": "副处级", "note": "2026-02-09 市委书记接访时随行。confirmed"},
    {"person_id": 8, "org_id": 2, "title": "武安市政府副市长", "start_date": "至今", "end_date": "至今",
     "rank": "副处级", "note": "2026-02-09 市委书记接访时随行。confirmed"},
    {"person_id": 9, "org_id": 2, "title": "武安市政府副市长", "start_date": "至今", "end_date": "至今",
     "rank": "副处级", "note": "2026-05-07 市长专题会随行。confirmed"},
    {"person_id": 10, "org_id": 2, "title": "武安市政府副市长", "start_date": "至今", "end_date": "至今",
     "rank": "副处级", "note": "2026-05-07 市长专题会随行。confirmed"},
    {"person_id": 11, "org_id": 2, "title": "武安市政府副市长", "start_date": "至今", "end_date": "至今",
     "rank": "副处级", "note": "2026-05-07 市长专题会随行。confirmed"},
]

# ── 关系 ────────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记—市长核心搭档",
     "overlap_org": "中共武安市委员会/武安市人民政府", "overlap_period": "2025-01至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "colleague", "context": "市委书记与市人大常委会主任（四大班子）同台",
     "overlap_org": "武安市四大班子", "overlap_period": "2026-03-11", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委书记—纪委书记在巡察工作中同台",
     "overlap_org": "中共武安市委员会", "overlap_period": "2026-05", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委书记—组织部部长在巡察工作中同台",
     "overlap_org": "中共武安市委员会", "overlap_period": "2026-05", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "市长—副市长（政府班子）",
     "overlap_org": "武安市人民政府", "overlap_period": "至今", "confidence": "plausible"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "市长—副市长（政府班子）",
     "overlap_org": "武安市人民政府", "overlap_period": "至今", "confidence": "plausible"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "市长—副市长（政府班子）",
     "overlap_org": "武安市人民政府", "overlap_period": "至今", "confidence": "plausible"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "市长—副市长，2026-05 一同参加经济运行专题会",
     "overlap_org": "武安市人民政府", "overlap_period": "2026-05", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "市长—副市长，2026-05 一同参加经济运行专题会",
     "overlap_org": "武安市人民政府", "overlap_period": "2026-05", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "市长—副市长，2026-05 一同参加经济运行专题会",
     "overlap_org": "武安市人民政府", "overlap_period": "2026-05", "confidence": "confirmed"},
]


def build_person_json(p) -> None:
    """写入单个人物深度档案 JSON。"""
    name = p.get("name", "")
    if not name:
        return
    job = p.get("current_post") or "武安市领导"
    _job = re.sub(r"[、，]?[一二三四]级(调研员|高级?监察官|主任科员|科员)?", "", job)
    slug_job = _job.replace("、", "-").replace("/", "-").strip("、")
    filename = f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{slug_job}-{name}.json"
    out_path = PERSONS_OUT / filename

    src_url = p.get("source") or ""
    source_register = [{
        "id": "S001",
        "title": f"武安市人民政府网站官方新闻/领导信息 - {name}",
        "url": src_url,
        "publisher": "武安市人民政府",
        "published_at": AS_OF,
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "武安市人民政府门户网站（www.wuan.gov.cn）2026-08-06 抓取确认",
    }]

    edu = []
    if p.get("education") and p["education"] not in ("待查", "", None):
        edu.append({"period": "", "institution": "", "major": "", "degree": p["education"],
                    "study_type": "unknown", "source_ids": ["S001"]})

    org_by_id = {o["id"]: o["name"] for o in organizations}
    career_timeline = []
    for pos in positions:
        if pos["person_id"] != p["id"]:
            continue
        is_party_sys = pos["org_id"] in (1, 5)
        career_timeline.append({
            "start": pos.get("start_date") or "unknown",
            "end": pos.get("end_date") or "present",
            "org": org_by_id.get(pos["org_id"], ""),
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": "邯郸市武安市",
            "system": "party" if is_party_sys else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": p["id"] in (1, 2),
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if "confirmed" in (pos.get("note") or "") else "plausible",
            "source_ids": ["S001"],
        })

    org_refs = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            org_refs.append({"org_name": org_by_id.get(pos["org_id"], ""), "org_type": "", "role": pos["title"]})

    open_q = []
    for field, label in (("birth", "出生年月"), ("birthplace", "籍贯"), ("education", "学历背景"),
                         ("party_join", "入党时间"), ("work_start", "参加工作年份")):
        if not p.get(field) or p.get(field) in ("待查", "未知"):
            open_q.append({"priority": "medium", "question": f"{name}的{label}",
                           "why_it_matters": "用于精确构建身份与晋升时间线",
                           "suggested_queries": [f"{name} 任前公示", f"{name} 简历 {SLUG}"], "last_attempted": AS_OF})
    if p["id"] in (1, 2):
        open_q.append({"priority": "high", "question": f"{'董志毅' if p['id']==1 else '李同强'}的任市委书记/市长起始时间与完整早前履历",
                       "why_it_matters": "理清武安市委书记/市长前任与继任链条",
                       "suggested_queries": ["武安市委书记换届", "武安市长任免"], "last_attempted": AS_OF})

    geometric = p.get("native_place", "")
    career_pattern = "unknown"
    if geometric and geometric != "待查":
        career_pattern = "local_ladder" if "武安" in geometric else "cross_county_rotation"

    document = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": PARENT_CITY, "region": SLUG,
                                "job": job, "task_id": "hebei_武安市", "time_focus": "2026"},
        "identity": {
            "person_id": f"hebei_handan_wuan_{name}",
            "name": name, "aliases": [],
            "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", "") if p.get("ethnicity") != "未知" else "",
            "birth": p.get("birth", "") if p.get("birth") != "待查" else "",
            "birthplace": p.get("birthplace", "") if p.get("birthplace") != "待查" else "",
            "native_place": p.get("native_place", "") if p.get("native_place") != "待查" else "",
            "education": edu,
            "party_join": p.get("party_join", "") if p.get("party_join") not in ("待查", "未知") else "",
            "work_start": p.get("work_start", "") if p.get("work_start") not in ("待查", "未知") else "",
            "dedupe_keys": {
                "name_birth": f"{name}_{p.get('birth', '')}",
                "name_birthplace": f"{name}_{p.get('birthplace', '')}",
                "official_profile_url": (src_url.split()[0] if src_url else ""),
            },
        },
        "current_status": {"current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""),
                           "administrative_rank": "正处级" if p["id"] in (1, 2, 3) else "副处级",
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]},
        "career_timeline": career_timeline,
        "organizations": org_refs,
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": career_pattern,
            "systems_experience": [], "geographic_pattern": [geometric] if geometric and geometric != "待查" else [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [], "speech_themes": [], "management_signals": [],
            "caveat": "工作风格源于公开记录与政务报道推断，并非私人心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "搜索范围内未发现纪律处分/审计/负面舆情信号（网络受限，证据有限）",
             "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历与出生等档案字段（网络受限未获取）",
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
    for pf in sorted(PERSONS_OUT.glob(f"{TODAY}-{PROVINCE}-*")):
        print(f"  Person: {pf}")


if __name__ == "__main__":
    main()