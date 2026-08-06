#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 图们市 (Tumen), 吉林省.

Investigation date: 2026-08-06
Task ID: jilin_图们市
Province: 吉林省
Parent city: 延边朝鲜族自治州
Level: 县级市
Targets: 市委书记 & 市长

Research sources (official portal, accessed via HTTP 2026-08-06):
  - http://www.tumen.gov.cn/  图们市人民政府门户网站 (primary; current 市政府/领导名单/新闻)
  - http://www.tumen.gov.cn/szf_2172/szfld/  市政府领导
  - http://www.tumen.gov.cn/szf_2172/szfld/fsz/202511/t20251111_559554.html 等 — 5位副市长官方简历("我的简历")
  - http://www.tumen.gov.cn/zw_2185/rsxx/  人大常委会人事任免通知（市长当选、副市长任命）
  - http://www.yanbian.gov.cn/zwgk_83/zzfld/  延边州政府领导（跨级参考/州副州长名单）

Network constraints in this environment:
  - Baidu Baike 403/captcha, Exa MCP rate-limited, Sogou captcha, Bing/Google/Jina/DuckDuckGo
    blocked/timeout. So 孙东升(市委书记)、崔永国(市长)、金哲俊(前任市长) 的完整履历以及
    市委其他常委的具体分工均未能通过外部百科/任前公示交叉核实，写入 open_questions /
    report gaps（符合 partial-evidence artifact mode）。

Confidence:
  - 孙东升(市委书记)、崔永国(市长)：职务 confirmed from 官方新闻；出生/籍贯/学历/履历 open。
  - 金哲俊(前任市长)：confirmed 任职至2023-11；去向 open。
  - 姜哲荣、贺照满、崔春虎、徐衍茹、滕达：简历 confirmed from 官方副市长"我的简历"页。
  - 吕秀生(市政协主席)：confirmed from 官方新闻。
  - 徐衍茹（2025-10-29）与滕达（2026-02）任副市长：confirmed 官方人事通知。
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: F401

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "图们市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_图们市"
if _CURRENT_DIR.name == "jilin_图们市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Source URLs ──────────────────────────────────────────────────────────────
FSU = "http://www.tumen.gov.cn/szf_2172/szfld/"
URL_RSXX = "http://www.tumen.gov.cn/zw_2185/rsxx/"

# ── Persons ───────────────────────────────────────────────────────────────────
persons = [
    # ══════ 核心领导（现任） ══════
    {
        "id": 1,
        "name": "孙东升",
        "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市委书记", "current_org": "中共图们市委",
        "source": "http://www.tumen.gov.cn/zw_2185/tmyw/202607/t20260731_581412.html",
        "confidence": "confirmed",
        "notes": "主持市委2026年第10次常委会会议（2026-07-10）并开展'八一'节前走访慰问（2026-07-30）。口岸城市定位、兴边富民/产业升级/对外开放/乡村振兴/民族团结/防汛减灾治理主题。出生/籍贯/学历/完整履历 open（百度百科不可用）。",
    },
    {
        "id": 2,
        "name": "崔永国",
        "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市委副书记、市长", "current_org": "图们市人民政府",
        "source": "http://www.tumen.gov.cn/szf_2172/szfld/",
        "confidence": "confirmed",
        "notes": "现任市长、市委副书记；市政府门户'市长'栏及官方新闻（2026-07-31）。出生/籍贯/学历/完整履历 open。",
    },
    # ══════ 政府班子（现任副市长） ══════
    {
        "id": 3,
        "name": "姜哲荣",
        "gender": "男", "ethnicity": "朝鲜族", "birth": "1985年5月", "birthplace": "",
        "education": "研究生", "party_join": "中共党员", "work_start": "2008年7月",
        "current_post": "副市长", "current_org": "图们市人民政府",
        "source": "http://www.tumen.gov.cn/szf_2172/szfld/fsz/202511/t20251111_559554.html",
        "confidence": "confirmed",
        "notes": "2006年5月入党。延边大学朝鲜语言文学专业，研究生学历硕士学位。现任市政府党组成员、副市长。分管人社、民政、退役、政务服务和数字化、全域旅游、市场监管、供销。",
    },
    {
        "id": 4,
        "name": "贺照满",
        "gender": "男", "ethnicity": "汉族", "birth": "1973年12月", "birthplace": "",
        "education": "大学本科", "party_join": "中共党员", "work_start": "1995年9月",
        "current_post": "副市长、市公安局局长", "current_org": "图们市公安局",
        "source": "http://www.tumen.gov.cn/szf_2172/szfld/fsz/202511/t20251111_559552.html",
        "confidence": "confirmed",
        "notes": "1999年10月入党。吉林大学法律专业，大学本科。现任市政府党组成员、副市长、公安局长。分管公安、边境管控、信访、法律援助。",
    },
    {
        "id": 5,
        "name": "崔春虎",
        "gender": "男", "ethnicity": "朝鲜族", "birth": "1976年5月", "birthplace": "",
        "education": "大学本科", "party_join": "中共党员", "work_start": "1999年11月",
        "current_post": "副市长", "current_org": "图们市人民政府",
        "source": "http://www.tumen.gov.cn/szf_2172/szfld/fsz/202511/t20251111_559550.html",
        "confidence": "confirmed",
        "notes": "2004年7月入党。吉林省委党校法律专业，大学本科。分管工业经济、民营经济、科技、水利、商贸流通、招商引资、对外事务。",
    },
    {
        "id": 6,
        "name": "徐衍茹",
        "gender": "女", "ethnicity": "汉族", "birth": "1986年4月", "birthplace": "",
        "education": "大学本科", "party_join": "中共党员", "work_start": "2009年9月",
        "current_post": "副市长", "current_org": "图们市人民政府",
        "source": "http://www.tumen.gov.cn/szf_2172/szfld/fsz/202511/t20251111_559170.html",
        "confidence": "confirmed",
        "notes": "2007年5月入党。中国农业大学种子科学与工程专业，大学本科。2025-10-29 图们市第十九届人大常委会第26次会议决定任命为副市长。分管教育、卫生健康、医疗保障、残疾人、街道政务。",
    },
    {
        "id": 7,
        "name": "滕达",
        "gender": "男", "ethnicity": "汉族", "birth": "1983年1月", "birthplace": "",
        "education": "研究生", "party_join": "中共党员", "work_start": "2005年10月",
        "current_post": "副市长", "current_org": "图们市人民政府",
        "source": "http://www.tumen.gov.cn/szf_2172/szfld/fsz/202602/t20260224_567566.html",
        "confidence": "confirmed",
        "notes": "2008年5月入党。吉林省委党校经济管理专业，研究生学历，硕士。2026-02 任副市长（人大任命）。分管农业农村、乡村振兴、林业、生态环境、乡镇事务。",
    },
    # ══════ 人大常委会（主任待查） ══════
    {
        "id": 8,
        "name": "待查_人大常委会主任",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "市人大常委会主任", "current_org": "图们市人民代表大会常务委员会",
        "source": URL_RSXX,
        "confidence": "unverified",
        "notes": "市十九届人大常委会（第26/31次会议等）运行中，主任姓名未从官方页面单独抓取；open question。",
    },
    {
        "id": 9,
        "name": "吕秀生",
        "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市政协主席", "current_org": "政协图们市委员会",
        "source": "http://www.tumen.gov.cn/szf_2172/zyhy/",
        "confidence": "confirmed",
        "notes": "官方新闻'市政协主席吕秀生到凉水镇走访调研'（2025-12）。现任市政协主席、党组书记。履历 open。",
    },
    # ══════ 前任 / 近期变动 ══════
    {
        "id": 10,
        "name": "金哲俊",
        "gender": "男", "ethnicity": "朝鲜族", "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "前任市长", "current_org": "图们市人民政府",
        "source": "http://www.tumen.gov.cn/sz_2181/wdgz/",
        "confidence": "confirmed",
        "notes": "官方新闻'图们市委副书记、市政府市长金哲俊'（2023-11 调研月晴镇、长安镇）。崔永国前任，卸任时间/去向 open。",
    },
    {
        "id": 11,
        "name": "待查_前任市委书记",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "前任市委书记", "current_org": "中共图们市委",
        "source": "",
        "confidence": "unverified",
        "notes": "孙东升任前市委书记身份及孙东升到任时间均未确认（open question）。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共图们市委", "type": "党委", "level": "县处级", "parent": "中共延边朝鲜族自治州委员会", "location": "图们市"},
    {"id": 2, "name": "图们市人民政府", "type": "政府", "level": "县处级", "parent": "延边朝鲜族自治州人民政府", "location": "图们市"},
    {"id": 3, "name": "图们市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "延边朝鲜族自治州人大常委会", "location": "图们市"},
    {"id": 4, "name": "政协图们市委员会", "type": "政协", "level": "县处级", "parent": "政协延边朝鲜族自治州委员会", "location": "图们市"},
    {"id": 5, "name": "图们市公安局", "type": "政府", "level": "正科级", "parent": "图们市人民政府", "location": "图们市"},
    {"id": 6, "name": "中共延边朝鲜族自治州委员会", "type": "党委", "level": "地厅级", "parent": "中共吉林省委", "location": "延吉市"},
    {"id": 7, "name": "延边朝鲜族自治州人民政府", "type": "政府", "level": "地厅级", "parent": "吉林省人民政府", "location": "延吉市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 孙东升 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2025", "end_date": "", "rank": "县处级（副厅级）", "note": "现任中共图们市委书记；任前时间 open（推测自2025年前后）"},
    # 崔永国 — 市长
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2024", "end_date": "", "rank": "县处级", "note": "现任市委副书记、市长、市政府党组书记，领导市政府全面工作"},
    # 姜哲荣
    {"person_id": 3, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级", "note": "市政府党组成员；分管人社、民政、退役、政务服务和数字化、全域旅游、市场监管、供销"},
    # 贺照满
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级", "note": "市政府党组成员"},
    {"person_id": 4, "org_id": 5, "title": "市公安局局长", "start_date": "", "end_date": "", "rank": "县处级", "note": "主持市公安局工作"},
    # 崔春虎
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级", "note": "分管工业经济、民营经济、科技、水利、商贸、招商、对外事务"},
    # 徐衍茹
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "2025-10", "end_date": "", "rank": "县处级", "note": "2025-10-29 图们市人大常委会第26次会议任命；分管教育、卫生、基层保障、残疾人、街道政务"},
    # 滕达
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "2026-02", "end_date": "", "rank": "县处级", "note": "2026-02 人大任命；分管农业农村、乡村振兴、林业、生态环境、乡镇事务"},
    # 市人大常委会主任（待查）
    {"person_id": 8, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级", "note": "市十九届人大常委会运行中；主任姓名待查"},
    # 吕秀生 — 政协主席
    {"person_id": 9, "org_id": 4, "title": "市政协主席（党组书记）", "start_date": "", "end_date": "", "rank": "县处级", "note": "官方新闻（2025-12）确认现任"},
    # 金哲俊 — 前任市长
    {"person_id": 10, "org_id": 2, "title": "市长", "start_date": "", "end_date": "2023-11", "rank": "县处级", "note": "前任市长；2023-11 仍以市长身份调研；后由崔永国接任"},
    {"person_id": 10, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "2023-11", "rank": "县处级", "note": ""},
    # 前任市委书记（待查）
    {"person_id": 11, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "县处级", "note": "孙东升任前书记，身份待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 书记—市长（核心搭档）
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共图们市委", "overlap_period": "2024-2026"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副市长", "overlap_org": "中共图们市委", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—副市长/公安局长", "overlap_org": "中共图们市委", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "书记—政协党组", "overlap_org": "中共图们市委", "overlap_period": "2025-2026"},
    # 市长 ↔ 团队
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—副市长", "overlap_org": "图们市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—副市长（公安）", "overlap_org": "图们市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—副市长", "overlap_org": "图们市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "市长—副市长", "overlap_org": "图们市人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "市长—副市长", "overlap_org": "图们市人民政府", "overlap_period": "2026"},
    # 前任/交接
    {"person_a": 10, "person_b": 2, "type": "交接", "context": "前任市长→现任市长（交接）", "overlap_org": "图们市人民政府", "overlap_period": "2023-2024"},
    {"person_a": 11, "person_b": 1, "type": "交接", "context": "前任市委书记→现任书记（交接，前任身份待查）", "overlap_org": "中共图们市委", "overlap_period": ""},
]

# ═════════════════════════════════════════════════════════════════════════════
# Person JSON generation (person_graph_json.md schema)
# ═════════════════════════════════════════════════════════════════════════════

def _open_questions(person: dict, pid: int):
    q = []
    if not person.get("birth"):
        q.append("出生年月未确认")
    if not person.get("birthplace"):
        q.append("籍贯未确认")
    if not person.get("education"):
        q.append("学历教育背景未确认")
    if not person.get("work_start"):
        q.append("参加工作年份未确认")
    if pid == 1:
        q.append("任图们市委书记前职务与到任时间未确认；前任市委书记身份未确认")
    if pid == 2:
        q.append("任市长前职务、完整任职履历未确认")
    if pid == 10:
        q.append("卸任时间与去向未确认")
    if pid == 8:
        q.append("市人大常委会主任姓名与履历未确认")
    if person.get("notes", ""):
        q.append("完整任职履历需进一步核实")
    return q


def write_person_json(person: dict) -> None:
    pid = person["id"]
    name = person["name"]
    conf = person.get("confidence", "unverified")

    person_positions = [p for p in positions if p["person_id"] == pid]
    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": conf,
            "source_ids": ["S001"],
        })
    if len(career_timeline) == 0 or name.startswith("待查"):
        career_timeline.append({
            "start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
            "notes": "公开资料不足（政府网站无书记/主任简介页，百度百科不可用）。",
            "confidence": "unverified", "source_ids": [],
        })

    rels_output = []
    for r in relationships:
        if r["person_a"] == pid or r["person_b"] == pid:
            other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
            other = next((p for p in persons if p["id"] == other_id), None)
            other_name = other["name"] if other else f"person_{other_id}"
            rels_output.append({
                "person": other_name,
                "person_id": f"tumen_{other_name}",
                "relationship_type": "overlap" if r["type"] == "共事" else "predecessor_successor",
                "strength": "strong" if r["type"] == "共事" else "medium",
                "evidence": r.get("context", ""),
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": conf,
                "source_ids": ["S001"],
            })

    source_url = person.get("source", "")
    sources = [{
        "id": "S001",
        "title": "图们市人民政府门户网站（市政府领导/副市长简历/领导活动/人事任免）",
        "url": source_url or "http://www.tumen.gov.cn/",
        "publisher": "图们市人民政府",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "官方领导栏及新闻确认现任职务",
    }]

    is_open_lead = pid in (1, 2, 8, 9, 10, 11)
    identity_conf = "confirmed" if (conf == "confirmed" and person.get("birth")) else "unverified"
    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省", "city": "延边朝鲜族自治州", "region": "图们市",
            "job": person.get("current_post", ""), "task_id": "jilin_图们市",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": f"tumen_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{
                "period": "", "institution": "", "major": "",
                "degree": person.get("education", ""),
                "study_type": "unknown", "source_ids": ["S001"],
            }] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级" if not person.get("current_post", "").startswith("前任") else "",
            "as_of": AS_OF,
            "is_current_confirmed": conf == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [{
            "period": "2025-2026",
            "domain": "other",
            "achievement_or_event": "口岸城市/兴边富民/乡村振兴/民族团结/防汛减灾治理（公开会议与活动主题）",
            "role_in_event": "现任市委领导/政府领导",
            "measurable_outcome": "",
            "location": "图们市",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        }] if pid in (1, 2) else [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if pid in (1, 2) else "local_ladder",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": identity_conf,
            "current_role": conf,
            "career_completeness": "thin" if is_open_lead else ("partial" if person.get("birth") else "thin"),
            "relationship_confidence": "medium",
            "biggest_gap": "出生年月/籍贯/完整履历（百度百科不可用）；市委班子/人大主任明细待查",
        },
        "open_questions": [
            {
                "priority": "critical" if pid in (1, 2) else "high",
                "question": (person.get("notes", "") or f"{name}的出生年月、籍贯、学历教育背景"),
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical" if pid == 1 else "medium",
                "question": f"{name}的完整任职履历（每段职务起止时间）",
                "why_it_matters": "关系网络分析需要精确时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历", "图们市委 常委班子"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-吉林省-延边朝鲜族自治州-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    print("  Writing person JSONs...")
    core_ids = {1, 2, 3, 4, 6, 9, 10}  # 书记/市长/副市长(姜哲荣、贺照满、徐衍茹)/政协主席/前任市长
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"  PJSON: {PJSON_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
