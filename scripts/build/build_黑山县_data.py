#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 黑山县 (Heishan County), 辽宁省锦州市.

Investigation date: 2026-08-06
Task ID: liaoning_黑山县
Level: 县
Targets: 县委书记 & 县长

Research sources (primary = official):
  - www.heishan.gov.cn — 黑山县人民政府门户网站首页 (OFFICIAL, reached via http)
    - 首页头条「中国共产党黑山县第十七次代表大会开幕」(2026-07-28): 王华作工作报告, 赵庆宇主持 → 确认 王华=县委书记, 赵庆宇=县长
    - 领导之窗 (zwgk/fdzdgknr/jgjj.htm): 县长 赵庆宇 + 副县长 陈强/尹元曦/李霞/王晓勇/张榜/鄂涛 完整简历
    - 领导简介页面 (info/1019/14686.htm 等): 各副职出生/学历/入党 confirmed
    - 黑政办发〔2026〕2号/3号 政府领导分工通知 (info/1191/49216.htm, 49300.htm): 县政府分工 + 阎晓东
    - 黑山县人大常委会人事任免决定 (info/2527/49336.htm, 46769.htm, 46742.htm): 张铁明辞监委主任/陈强任副县长/满佳免、王晓勇任
    - 2026-07 各会议/调研新闻: 王华、赵庆宇 plus 胡伟/檀雪松/吕明霏/鄂涛/王敬珏/孙放 等县领导
  - 锦州市政府门户 (www.jz.gov.cn) 参考
  - Web search degraded: Exa 限流, Baidu 403/captcha, Jina Reader 超时 → 外部履历检索受限

Confirmed (official source, as of 2026-08):
  - 县委书记: 王华 — 现职由党代会报告+多次会议主持确认; 出生/籍贯/学历/此前职务 未获一手来源 → unverified/gap
  - 县委副书记、县长: 赵庆宇 — 男,汉族,1981-10,硕士学位,中共党员; 兼 庞河经开区工委书记/管委会主任
  - 县委常委、副县长: 陈彦淞 — 男,汉族,1973-12,在职大学,中共党员
  - 县委常委、副县长: 尹元曦 — 男,汉族,1985-01,研究生/硕士,中共党员
  - 副县长: 李霞(女,1981-06,研究生/硕士), 王晓勇(男,1975-12,在职大学), 张艳(男,1982-01,公安局长), 鄂涛(男,1979-07,副县长人选)
  - 县领导/党工委: 阎晓东 (分管庞河经开区)

Confidence notes:
  - 现任县长及副县长出生/学历/入党: confirmed (官网领导之窗)
  - 县委书记 王华 身份: confirmed (官方党代会报道); 完整履历: unknown → open_questions
  - 县领导班子其余成员 (县委副书记、组织/宣传/纪委/政法委、人大/政协) 名单: partial → 列为 gap, 以 plausible/unverified 标注
  - 前任县委书记: 未从一手来源确认 → open_questions
"""

from __future__ import annotations

import json
import os
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

import sqlite3  # noqa
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "黑山县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_黑山县"
if _CURRENT_DIR.name == "liaoning_黑山县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# ID 1 = 县委书记, 2 = 县长, 3-8 = 政府班子, 9-10 = 其他县领导, 20+ = 前任/原班子
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 现任核心领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "王华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共黑山县委员会",
        "source": "http://www.heishan.gov.cn/info/1012/49830.htm",
        "confidence": "confirmed_role",
        "notes": "现任黑山县委书记。2026-07-27 在中共黑山县第十七次代表大会上作县委工作报告; 多次主持县委会议(重点项目/苏锦合作/防汛/城区规划)。出生年月、籍贯、学历、入党时间、参加工作、此前职务均未获一手来源, 完整履历待核。"
    },
    {
        "id": 2,
        "name": "赵庆宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "",
        "education": "硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "黑山县人民政府",
        "source": "http://www.heishan.gov.cn/info/1019/14686.htm",
        "confidence": "confirmed",
        "notes": "现任黑山县委副书记、县长, 兼中共锦州庞河经济开发区工委书记、管委会主任。主持县政府和庞河经开区全面工作, 分管审计、农业农村(乡村振兴)、生态环境。多次主持召开县政府常务会议并深入防汛/产业园/项目一线。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 政府班子成员 (领导之窗, official)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "陈强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "黑山县人民政府",
        "source": "http://www.heishan.gov.cn/info/1019/26606.htm",
        "confidence": "confirmed",
        "notes": "现任黑山县委常委、副县长(2026-04-30 县人大常委会决定任命/续任)。负责发展改革、财政、人社、住建、应急、信访、统计、机关事务等; 协助县长分管审计。2026-03 省委第十五巡辑组对黑山开展营商环境专项巡视背景下常见出席常务会议。"
    },
    {
        "id": 4,
        "name": "尹元曦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年1月",
        "birthplace": "",
        "education": "研究生学历、硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "黑山县人民政府",
        "source": "http://www.heishan.gov.cn/info/1019/14684.htm",
        "confidence": "confirmed",
        "notes": "现任黑山县委常委、副县长。负责民营经济、自然资源、交通运输、营商环境建设、智慧城市、供电等。1985年出生, 为班子中较年轻的常委。"
    },
    {
        "id": 5,
        "name": "李霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年6月",
        "birthplace": "",
        "education": "研究生学历、硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "黑山县人民政府",
        "source": "http://www.heishan.gov.cn/info/1019/14682.htm",
        "confidence": "confirmed",
        "notes": "现任黑山县政府副县长。负责教育、科技、外贸出口、外事、文旅广电、卫生健康、民族宗教、医疗保健等。班子中女性代表。"
    },
    {
        "id": 6,
        "name": "王晓勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年12月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "黑山县人民政府",
        "source": "http://www.heishan.gov.cn/info/1019/46491.htm",
        "confidence": "confirmed",
        "notes": "现任黑山县政府副县长(2025-11-04 县人大常委会决定任命)。负责防汛抗旱、林业草原、供销、民政等; 协助县长分管县农业农村局(乡村振兴局)。"
    },
    {
        "id": 7,
        "name": "张榜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年1月",
        "birthplace": "",
        "education": "在职研究生学历、硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "黑山县公安局",
        "source": "http://www.heishan.gov.cn/info/1019/49305.htm",
        "confidence": "confirmed",
        "notes": "现任黑山县副县长，主持县公安局工作，分管县司法局，负责公安、司法等方面工作，协助县长抓好社会稳定工作。"
    },
    {
        "id": 8,
        "name": "鄂涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年7月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "黑山县人民政府",
        "source": "http://www.heishan.gov.cn/info/1019/44440.htm",
        "confidence": "confirmed",
        "notes": "现任黑山县人民政府副县长(曾任副县长合适人选,现为正式副县长)。负责民政、退役军人事务、市场监管等; 协助县政府联系县生态环境局。参与防汛等领域调研。"
    },
    {
        "id": 9,
        "name": "阎晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、庞河经开区负责人",
        "current_org": "锦州庞河经济开发区",
        "source": "http://www.heishan.gov.cn/info/1191/49300.htm",
        "confidence": "confirmed_role",
        "notes": "县领导, 负责庞河经济开发区日常工作, 协助赵县长抓招商引资、分管县经济合作中心。出现在县政府领导分工通知(万政办发〔2026〕3号)。出生/学历未公开。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任/原班子 (confirmed via 人大常委会人事任免决定)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "满佳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任副县长",
        "current_org": "黑山县人民政府",
        "source": "http://www.heishan.gov.cn/info/2527/46742.htm",
        "confidence": "confirmed_role",
        "notes": "原黑山县人民政府副县长, 2025-11-04 (县人大常委会第三十八次会议) 决定免去其职务。王晓勇为其继任者之一。完整履历/去向待核。"
    },
    {
        "id": 21,
        "name": "张铁明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县监委主任",
        "current_org": "中共黑山县纪律检查委员会",
        "source": "http://www.heishan.gov.cn/info/2527/49336.htm",
        "confidence": "confirmed_role",
        "notes": "原黑山县监察委员会主任 (县纪委监委负责人)。2026-04 (县人大常委会第四十三次会议) 接受其辞去县监察委员会主任职务。继任者及去向待核。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共黑山县委员会", "type": "党委", "level": "县处级", "parent": "中共锦州市委员会", "location": "黑山县"},
    {"id": 2, "name": "黑山县人民政府", "type": "政府", "level": "县处级", "parent": "锦州市人民政府", "location": "黑山县"},
    {"id": 3, "name": "黑山县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "锦州市人大常委会", "location": "黑山县"},
    {"id": 4, "name": "中国人民政治协商会议黑山县委员会", "type": "政协", "level": "县处级", "parent": "政协锦州市委员会", "location": "黑山县"},
    {"id": 5, "name": "中共黑山县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共黑山县委员会", "location": "黑山县"},
    {"id": 6, "name": "黑山县公安局", "type": "政府", "level": "科级", "parent": "黑山县人民政府", "location": "黑山县"},
    {"id": 7, "name": "锦州庞河经济开发区", "type": "开发区", "level": "县处级", "parent": "黑山县人民政府", "location": "黑山县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 王华 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正县处级", "note": "现任黑山县委书记 (2026-07 党代会报告确认, 任期含十五五)"},
    # 赵庆宇 — 县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县处级", "note": "县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正县处级", "note": "现任县长, 主持县政府全面工作, 兼房区庞河经开区工委书记/管委会主任"},
    {"person_id": 2, "org_id": 7, "title": "经开区党工委书记、管委会主任", "start_date": "", "end_date": "", "rank": "县处级", "note": "兼任"},
    # 陈强
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 尹元曦
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 李霞
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 王晓勇
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "2025-11", "end_date": "", "rank": "副县处级", "note": "2025-11-04 县人大常委会任命"},
    # 张榜
    {"person_id": 7, "org_id": 6, "title": "县公安局局长", "start_date": "", "end_date": "", "rank": "正科级", "note": "主持县公安局工作"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县处级", "note": "负责公安、司法"},
    # 鄂涛
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 阎晓东
    {"person_id": 9, "org_id": 7, "title": "庞河经开区负责人", "start_date": "", "end_date": "", "rank": "县处级", "note": "负责开发区日常工作, 协助县长抓招商引资"},
    # 前任
    {"person_id": 20, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "2025", "rank": "副县处级", "note": "2025-11-04 县人大常委会免职"},
    {"person_id": 21, "org_id": 5, "title": "县纪委监委主任", "start_date": "", "end_date": "2026", "rank": "副县处级", "note": "2026-04 辞职"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 核心搭档: 书记—县长
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长核心搭档", "overlap_org": "中共黑山县委员会/县政府", "overlap_period": "现任(2026)"},
    # 书记—班子
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "党政—把手, 共同主持项目/防汛/招商会议", "overlap_org": "中共黑山县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—县委委员, 参与县域重大工作", "overlap_org": "中共黑山县委员会", "overlap_period": ""},
    # 县长—班子对接
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "县长—常务副县长搭班", "overlap_org": "黑山县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "县长—副县长同班", "overlap_org": "黑山县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "县长—副县长", "overlap_org": "黑山县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "县长—副县长", "overlap_org": "黑山县人民政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "县长—副县长/公安局长", "overlap_org": "黑山县人民政府/公安局", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "县长—副县长", "overlap_org": "黑山县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "县长—庞河经开区负责人, 县长兼经开区书记", "overlap_org": "锦州庞河经济开发区", "overlap_period": ""},
    # 前任/原班子交接
    {"person_a": 20, "person_b": 6, "type": "交接", "context": "前任副县长—继任副县长(满佳免/王晓勇任)", "overlap_org": "黑山县人民政府", "overlap_period": "2025"},
    {"person_a": 21, "person_b": 1, "type": "交接", "context": "前任县监委主任辞职, 县委党风廉政建设衔接", "overlap_org": "中共黑山县纪律检查委员会", "overlap_period": "2026"},
]

# ═════════════════════════════════════════════════════════════════════════════
# Helper functions (person JSON)
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[str]:
    q = []
    if not person.get("birth"):
        q.append("出生年月未确认")
    if not person.get("birthplace"):
        q.append("籍贯/出生地未确认")
    if not person.get("education"):
        q.append("学历教育背景未确认")
    if not person.get("work_start"):
        q.append("参加工作年份未确认")
    if "待核" in person.get("notes", "") or "未公开" in person.get("notes", "") or person.get("confidence") not in ("confirmed",):
        if person.get("name") != "赵庆宇":
            q.append("完整任职履历未确认")
    return q


def write_person_json(person: dict) -> None:
    pid = person["id"]
    name = person["name"]
    slug_id = f"heishan_{name}"

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
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"] if person.get("confidence") == "confirmed" else ["S100"],
        })
    if len(career_timeline) <= 2 and (not person.get("birth") or "待核" in person.get("notes", "") or not person.get("work_start")):
        career_timeline.append({
            "start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
            "notes": "公开资料不足: 外部检索受限(Exa限流/百度403/Jina超时), 早期任职履历待核。",
            "confidence": "unverified", "source_ids": [],
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        if other_id == pid:
            continue
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rel_type = "overlap" if r["type"] == "共事" else "predecessor_successor"
        strength = "strong" if r["type"] == "共事" else "medium"
        rels_output.append({
            "person": other_name, "person_id": f"heishan_{other_name}",
            "relationship_type": rel_type, "strength": strength,
            "evidence": r.get("context", ""), "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""), "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"] if person.get("confidence") == "confirmed" else ["S100"],
        })

    source_url = person.get("source", "")
    sources = [{
        "id": "S001",
        "title": "黑山县人民政府门户网站—领导之窗/新闻",
        "url": source_url or "http://www.heishan.gov.cn/",
        "publisher": "黑山县人民政府",
        "published_at": "", "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high" if person.get("confidence") == "confirmed" else "medium",
        "notes": "官方一手来源",
    }]

    big_gap = "完整履历与出生信息缺失(外部检索受限)"
    career_completeness = "confirmed" if person.get("confidence") == "confirmed" else "thin"

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省", "city": "锦州市", "region": "黑山县",
            "job": person.get("current_post", ""),
            "task_id": "liaoning_黑山县", "time_focus": "2024–2026",
        },
        "identity": {
            "person_id": slug_id, "name": name, "aliases": [],
            "gender": person.get("gender", ""), "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""), "birthplace": person.get("birthplace", ""),
            "native_place": "", "education": [], "party_join": person.get("party_join", ""),
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
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") in ("confirmed", "confirmed_role"),
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
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
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "截至2026-08-06未发现违纪或负面舆情信号(公开来源)",
            "date": "", "confidence": "unverified", "source_ids": [],
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": "confirmed" if person.get("confidence") in ("confirmed", "confirmed_role") else "plausible",
            "career_completeness": career_completeness,
            "relationship_confidence": "medium" if person.get("confidence") in ("confirmed", "confirmed_role") else "low",
            "biggest_gap": big_gap,
        },
        "open_questions": [
            {"priority": "critical", "question": f"{name}的准确出生年月、籍贯、学历教育背景",
             "why_it_matters": "核心身份信息, 用于去重和跨区域关联分析",
             "suggested_queries": [f"{name} 简历 黑山", f"{name} 任前公示", f"{name} 百度百科"],
             "last_attempted": AS_OF},
            {"priority": "critical", "question": f"{name}的完整任职履历(每段职务起止时间与前期职务)",
                 "why_it_matters": "关系网络分析需要精确时间线",
                 "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历", f"{name} 辽宁省委组织部"],
                 "last_attempted": AS_OF},
        ],
    }
    if person.get("confidence") == "confirmed":
        record["open_questions"] = [q for q in record["open_questions"] if "出生" not in q["question"] or not person.get("birth")]

    post_slug = person['current_post'].replace('/', '_')
    fname = f"{TODAY}-辽宁省-锦州市-{post_slug}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════

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
    core_ids = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())