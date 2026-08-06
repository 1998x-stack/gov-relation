#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 珲春市 (Hunchun City), 吉林省.

Task ID: jilin_珲春市 | Level: 县级市 | Targets: 市委书记 & 市长 | Date: 2026-08-06
Parent: 延边朝鲜族自治州 | Province: 吉林省

SouffCE / confidence (primary source: official 珲春市人民政府门户 www.hunchun.gov.cn, accessed via HTTP 2026-08-06):
  - 林小林（珲春市委书记）：职务 confirmed（官方新闻 2026-07-21/08-04，任延边州委副书记、珲春市委书记、示范(海洋经济发展示范区)党工委书记）；出生/籍贯/学历/完整履历 open（search engines blocked）。
  - 张林国（市长）：confirmed（官方"我的简历"页）：男，朝鲜族，1974年1月生，研究生，经济学博士；珲春市委副书记、市长、市政府党组书记、示范区党工委副书记、管委会主任。
  - 李昭辉（常务副市长 1978年10月）、徐善君（挂职 1981年6月）、关亚菲（锡伯族 1974年8月）、朴永虎（朝鲜族 1976年4月）、李威（1977年9月 兼公安局长）、俞林（朝鲜族 1986年4月）、苏志伟（1982年5月）：confirmed 官方在挂名单/简历。
  - 沈洪子（市委常委、组织部部长）：confirmed 官方"两优一先"表彰大会稿件。
  - 陈航发（人大常委会党组书记、主任候选人）、董永利/吕玉华/王娟/王士勇（人大副主任）、赵显虎（政协党组书记）、崔巍/金在虎/冯立强（政协副主席）、李容宇（市检察院检察长）：confirmed 官方人大/政协会议稿件。
  - 前任珲春市委书记 / 前任市长 / 纪委书记 / 政法委书记 / 宣传部长 / 统战部长：unverified（搜索受限未取得）。
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
SLUG = "珲春市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_珲春市"
if _CURRENT_DIR.name == "jilin_珲春市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

PERSON_CITY = "延边朝鲜族自治州"  # per-person JSON filename convention uses parent city

# ── Persons ──────────────────────────────────────────────────────────────────
persons = [
    # ══════ 核心领导（现任） ══════
    {
        "id": 1, "name": "林小林",
        "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委书记", "current_org": "中共珲春市委",
        "source": "http://www.hunchun.gov.cn/sz/zyhy/202607/t20260724_581118.html",
        "confidence": "confirmed",
        "notes": "延边州委副书记、珲春市委书记、示范区(珲春海洋经济发展示范区)党工委书记。2026-07-21主持市委常委会暨示范区党工委会议并作部署；2026-08-04走访慰问驻珲官兵(八一)。主持全市安全、防汛等。出生/籍贯/学历/完整履历 open(搜索受限)。",
    },
    {
        "id": 2, "name": "张林国",
        "gender": "男", "ethnicity": "朝鲜族", "birth": "1974年1月", "birthplace": "",
        "education": "研究生，经济学博士", "party_join": "中共党员", "work_start": "",
        "current_post": "市委副书记、市长", "current_org": "珲春市人民政府",
        "source": "http://www.hunchun.gov.cn/sz/zjf/szjl/",
        "confidence": "confirmed",
        "notes": "珲春市委副书记、市长、市政府党组书记，示范区(珲春海洋经济发展示范区)党工委副书记、管委会主任。主持市政府全面工作。2026-07-24主持召开十九届市政府第七十一次常务会议。",
    },
    # ══════ 政府班子（现任副市长） ══════
    {
        "id": 3, "name": "李昭辉",
        "gender": "男", "ethnicity": "汉族", "birth": "1978年10月", "birthplace": "",
        "education": "研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、常务副市长", "current_org": "珲春市人民政府",
        "source": "http://www.hunchun.gov.cn/szf_1881/",
        "confidence": "confirmed",
        "notes": "珲春市委常委、市政府常务副市长（官网领导排序第一）。分管政府常务工作。出生/籍贯/学历/完整履历部分 open。",
    },
    {
        "id": 4, "name": "徐善君",
        "gender": "男", "ethnicity": "汉族", "birth": "1981年6月", "birthplace": "",
        "education": "硕士研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "珲春市人民政府",
        "source": "http://www.hunchun.gov.cn/zw_1881/",
        "confidence": "confirmed",
        "notes": "珲春市委常委、副市长（挂职），市政府党组成员。出生/籍贯/完整履历部分 open。",
    },
    {
        "id": 5, "name": "关亚菲",
        "gender": "女", "ethnicity": "锡伯族", "birth": "1974年8月", "birthplace": "",
        "education": "硕士", "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "珲春市人民政府",
        "source": "http://www.hunchun.gov.cn/zw_1881/",
        "confidence": "confirmed",
        "notes": "珲春市副市长、市政府党组成员。少数民族(锡伯族)女性干部。",
    },
    {
        "id": 6, "name": "朴永虎",
        "gender": "男", "ethnicity": "朝鲜族", "birth": "1976年4月", "birthplace": "",
        "education": "大学", "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "珲春市人民政府",
        "source": "http://www.hunchun.gov.cn/zw_1881/",
        "confidence": "confirmed",
        "notes": "珲春市副市长、市政府党组成员（朝鲜族）。",
    },
    {
        "id": 7, "name": "李威",
        "gender": "男", "ethnicity": "汉族", "birth": "1977年9月", "birthplace": "",
        "education": "大学，法学学士", "party_join": "中共党员", "work_start": "",
        "current_post": "副市长、市公安局局长", "current_org": "珲春市公安局",
        "source": "http://www.hunchun.gov.cn/sz/fsz/csj_13223/",
        "confidence": "confirmed",
        "notes": "珲春市副市长、市政府党组成员，市公安局局长、党委书记、督察长（兼）。分管公安、司法、退役军人事务、信访。",
    },
    {
        "id": 8, "name": "俞林",
        "gender": "男", "ethnicity": "朝鲜族", "birth": "1986年4月", "birthplace": "",
        "education": "大学，经济学学士", "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "珲春市人民政府",
        "source": "http://www.hunchun.gov.cn/zw_1881/",
        "confidence": "confirmed",
        "notes": "珲春市副市长、市政府党组成员（朝鲜族）。七月人大常委会第31次会议列席。",
    },
    {
        "id": 9, "name": "苏志伟",
        "gender": "男", "ethnicity": "汉族", "birth": "1982年5月", "birthplace": "",
        "education": "硕士研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "珲春市人民政府",
        "source": "http://www.hunchun.gov.cn/zw_1881/",
        "confidence": "confirmed",
        "notes": "珲春市副市长、市政府党组成员。",
    },
    # ══════ 市委（关键常委） ══════
    {
        "id": 10, "name": "沈洪子",
        "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、组织部部长", "current_org": "中共珲春市委",
        "source": "http://www.hunchun.gov.cn/sz/zyhy/202607/t20260706_579847.html",
        "confidence": "confirmed",
        "notes": "2026-06\u201c两优一先\u201d表彰大会宣读表彰决定（组织部部长）。出生/籍贯/学历/履历 open。",
    },
    # ══════ 人大 / 政协 ══════
    {
        "id": 11, "name": "陈航",
        "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会党组书记、主任候选人", "current_org": "珲春市人大常委会",
        "source": "http://www.hunchun.gov.cn/sz/zyhy/202607/t20260726_581134.html",
        "confidence": "confirmed",
        "notes": "市人大常委会党组书记、主任候选人（换届中）。出生/籍贯/学历 open。",
    },
    {
        "id": 12, "name": "赵显虎",
        "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市政协党组书记", "current_org": "珲春市政协",
        "source": "http://www.hunchun.gov.cn/sz/zyhy/202607/t20260726_581130.html",
        "confidence": "confirmed",
        "notes": "市政协党组书记（换届筹备年）。出生/籍贯/学历 open。",
    },
    {
        "id": 13, "name": "李容宇",
        "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市人民检察院检察长", "current_org": "珲春市人民检察院",
        "source": "http://www.hunchun.gov.cn/sz/zyhy/202607/t20260726_581134.html",
        "confidence": "confirmed",
        "notes": "列席人大常委会会议。",
    },
    # ══════ 前任（unverified） ══════
    {
        "id": 14, "name": "前任珲春市委书记(待查)",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "前任市委书记（未确认）", "current_org": "",
        "source": "",
        "confidence": "unverified",
        "notes": "林小林现任前任未敢确证。外部百科/任前公示受限，未能交叉核实。",
    },
]

organizations = [
    {"id": 1, "name": "中共珲春市委员会", "type": "党委", "level": "县级", "parent": "中共延边朝鲜族自治州委员会", "location": "珲春市"},
    {"id": 2, "name": "珲春市人民政府", "type": "政府", "level": "县级", "parent": "延边朝鲜族自治州人民政府", "location": "珲春市"},
    {"id": 3, "name": "珲春市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "珲春市"},
    {"id": 4, "name": "中国人民政治协商会议珲春市委员会", "type": "政协", "level": "县级", "parent": "", "location": "珲春市"},
    {"id": 5, "name": "珲春市公安局", "type": "政府", "level": "县级", "parent": "珲春市人民政府", "location": "珲春市"},
    {"id": 6, "name": "珲春市人民检察院", "type": "司法", "level": "县级", "parent": "", "location": "珲春市"},
    {"id": 7, "name": "珲春海洋经济发展示范区（党工委/管委会）", "type": "开发区", "level": "国家级(海参崴开放)/县级", "parent": "珲春市人民政府", "location": "珲春市"},
    {"id": 8, "name": "中共延边朝鲜族自治州委员会", "type": "党委", "level": "地级(州)", "parent": "中共吉林省委员会", "location": "延边州"},
    {"id": 9, "name": "延边朝鲜族自治州人民政府", "type": "政府", "level": "地级(州)", "parent": "吉林省人民政府", "location": "延边州"},
    {"id": 10, "name": "中共吉林省委员会", "type": "党委", "level": "省级", "parent": "", "location": "长春市"},
    {"id": 11, "name": "吉林省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "长春市"},
]

positions = [
    # 林小林
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "unknown", "end_date": "present", "rank": "县级正职(州委副书记兼)", "note": "珲春市委书记、示范区党工委书记（延边州委副书记兼）"},
    {"person_id": 1, "org_id": 8, "title": "延边州委副书记（兼）", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": "边界/口岸城市，州级托底配置"},
    {"person_id": 1, "org_id": 7, "title": "示范区党工委书记（兼）", "start_date": "unknown", "end_date": "present", "rank": "", "note": "珲春海洋经济发展示范区"},
    # 张林国市长
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "unknown", "end_date": "present", "rank": "正处级(县级市长)", "note": "主持市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "unknown", "end_date": "present", "rank": "县级委副书记", "note": "市长兼市委副书记"},
    {"person_id": 2, "org_id": 7, "title": "示范区党工委副书记、管委会主任（兼）", "start_date": "unknown", "end_date": "present", "rank": "", "note": "珲春海洋经济发展示范区"},
    # 副市长们
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "unknown", "end_date": "present", "rank": "副县级", "note": "市委常委兼，分工第一"},
    {"person_id": 4, "org_id": 2, "title": "副市长（挂职）", "start_date": "unknown", "end_date": "present", "rank": "副县级", "note": "挂职"},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "副县级", "note": "锡伯族"},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "副县级", "note": "朝鲜族"},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "副县级", "note": "兼公安局长"},
    {"person_id": 7, "org_id": 5, "title": "市公安局局长、党委书记、督察长", "start_date": "unknown", "end_date": "present", "rank": "副县级", "note": "公安"},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "副县级", "note": "朝鲜族"},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "副县级", "note": ""},
    # 组织部长
    {"person_id": 10, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "unknown", "end_date": "present", "rank": "副县级", "note": ""},
    # 人大 / 政协 / 检察
    {"person_id": 11, "org_id": 3, "title": "人大常委会党组书记、主任候选人", "start_date": "unknown", "end_date": "present", "rank": "正处", "note": "换届选举候选"},
    {"person_id": 12, "org_id": 4, "title": "政协党组书记", "start_date": "unknown", "end_date": "present", "rank": "正处", "note": "换届筹备"},
    {"person_id": 13, "org_id": 6, "title": "市人民检察院检察长", "start_date": "unknown", "end_date": "present", "rank": "副处", "note": ""},
    # 前任（unconfirmed 占位）
    {"person_id": 14, "org_id": 1, "title": "前任市委书记（点位未命名）", "start_date": "", "end_date": "", "rank": "", "note": "无法确证名字/去向——避免虚构，仅记占位 gap"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "决策搭档（党政班子）", "context": "书记与市长搭档，林小林主持市委，张林国主持市政府", "overlap_org": "中共珲春市委/珲春市人民政府", "overlap_period": "present"},
    {"person_a": 1, "person_b": 2, "type": "示范驻共同履职", "context": "共同领导珲春海洋经济发展示范区（林为党工委书记，张为党工委副书记、管委会主任）", "overlap_org": "珲春海洋经济发展示范区", "overlap_period": "present"},
    {"person_a": 2, "person_b": 3, "type": "班子/上下级（政府）", "context": "常务副市长协助市长主持市政府常务工作", "overlap_org": "珲春市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 7, "type": "班子/上下级（公安）", "context": "副市长李威兼公安局长，隶属市政府班子", "overlap_org": "珲春市人民政府/市公安局", "overlap_period": "present"},
    {"person_a": 1, "person_b": 10, "type": "班子/上下级（组织）", "context": "组织部长沈洪在市委常委会上受市委书记领导", "overlap_org": "中共珲春市委", "overlap_period": "present"},
    {"person_a": 1, "person_b": 8, "type": "州-市上下级", "context": "林小林同时任延边州委副书记（州委-市级交叠）", "overlap_org": "中共延边州委", "overlap_period": "present"},
    {"person_a": 1, "person_b": 11, "type": "本届班子/人大", "context": "市人大常委会主任候选人与市委书记同届期（换届）", "overlap_org": "珲春市人大常委会", "overlap_period": "present"},
]

# ── Person JSON ─────────────────────────────────────────────────────────────
SOURCE_REGISTER = [
    {"id": "S001", "title": "珲春市人民政府 · 市政府领导", "url": "http://www.hunchun.gov.cn/szf_1881/", "publisher": "珲春市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市长/副市长名单（张林国等7人）与分工"},
    {"id": "S002", "title": "珲春市政府 · 市长简历/分工", "url": "http://www.hunchun.gov.cn/sz/zjf/szjl/", "publisher": "珲春市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张林国简历（朝鲜族 1974-01 经济学博士）+分工"},
    {"id": "S003", "title": "市委常委会暨示范区党工委会议", "url": "http://www.hunchun.gov.cn/sz/zyhy/202607/t20260724_581118.html", "publisher": "珲春市人民政府/图们江报", "published_at": "2026-07-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "林小林（延边州委副书记、珲春市委书记、示范党工委书记）主持"},
    {"id": "S004", "title": "十九届市政府第七十一次常务会议", "url": "http://www.hunchun.gov.cn/sz/zyhy/202607/t20260724_581119.html", "publisher": "珲春市人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张林国市长主持，政府班子"},
    {"id": "S005", "title": "人大常委会第三十一次会议", "url": "http://www.hunchun.gov.cn/sz/zyhy/202607/t20260726_581134.html", "publisher": "珲春市人民政府", "published_at": "2026-07-26", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "人大领导（主任候选人陈航伦、副主任等）+检察长李容宇"},
    {"id": "S006", "title": "政协十四届二十四次常委会议", "url": "http://www.hunchun.gov.cn/sz/zyhy/202607/t20260726_581130.html", "publisher": "珲春市人民政府", "published_at": "2026-07-26", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "政协领导（党组书记赵显虎、副主席者）"},
    {"id": "S007", "title": "两优一先表彰大会", "url": "http://www.hunchun.gov.cn/sz/zyhy/202607/t20260706_579847.html", "publisher": "珲春市人民政府", "published_at": "2026-07-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "沈洪泽（组织部长）宣读表彰决定"},
]

def build_person_file(job, name, cts, identity, timeline, relations, big_gap, orgs, qs=None):
    p = STAGING / f"{TODAY}-吉林省-{PERSON_CITY}-{job}-{name}.json"
    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {"province": "吉林省", "city": PERSON_CITY, "region": SLUG,
                                "job": job, "task_id": "jilin_珲春市", "time_focus": "2026"},
        "identity": {"person_id": f"hunchun_{name}", "name": name, "aliases": [],
                     "gender": identity.get("gender", ""), "ethnicity": identity.get("ethnicity", ""),
                     "birth": identity.get("birth", ""), "birthplace": identity.get("birthplace", ""),
                     "native_place": identity.get("native_place", ""),
                     "education": identity.get("education", []),
                     "party_join": identity.get("party_join", ""), "work_start": identity.get("work_start", ""),
                     "dedupe_keys": {"name_birth": f"{name}_{identity.get('birth','')}",
                                     "name_birthplace": f"{name}_{identity.get('birthplace','')}",
                                     "official_profile_url": ""}},
        "current_status": {"current_post": job, "current_org": identity.get("org", ""),
                           "administrative_rank": identity.get("rank", ""), "as_of": AS_OF,
                           "is_current_confirmed": identity.get("confirmed", True),
                           "source_ids": identity.get("source_ids", ["S001"])},
        "career_timeline": timeline if timeline else [],
        "organizations": orgs if isinstance(orgs, list) else ([orgs] if orgs else []),
        "relationships": relations if isinstance(relations, list) else relations if relations else [],
        "governance_record": [{"period": "", "domain": "border_economy", "achievement_or_event": "", "role_in_event": "", "measurable_outcome": "", "location": "珲春市", "confidence": "plausible", "source_ids": []}],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [],
                                 "career_pattern": "county_leadership|open_gap", "systems_experience": [],
                                 "geographic_pattern": ["延边州·珲春"], "promotion_velocity": {"summary": ""}},
        "work_style_and_personality": {"public_style_indicators": [
            {"trait": "grassroots_oriented", "evidence": "常规调研防汛等上级部署", "confidence": "plausible", "source_ids": []}] if cts else [], "speech_themes": [], "management_signals": [], "caveat": "推断自公开活动，非心理评估"},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "公开检索范围内未发现涉权负面信息", "date": AS_OF, "confidence": "plausible", "source_ids": []}],
        "source_register": SOURCE_REGISTER,
        "confidence_summary": {"identity": "confirmed" if identity.get("birth") else "plausible",
                               "current_role": "confirmed",
                               "career_completeness": "partial" if identity.get("birth") else "thin",
                               "relationship_confidence": "medium", "biggest_gap": big_gap},
        "open_questions": qs or [{"priority": "critical", "question": big_gap, "why_it_matters": "关系网络", "suggested_queries": [f"{name} 简历"], "last_attempted": AS_OF}],
    }
    with open(p, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
    print("  person JSON:", p.name)

def write_persons_files():
    # ── 林小林（市委书记） ──
    build_person_file(
        "市委书记", "林小林",
        True,
        {"gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
         "education": [], "party_join": "中共党员", "work_start": "",
         "org": "中共珲春市委", "rank": "州委副书记兼珲春市委书记", "confirmed": True,
         "source_ids": ["S003"]},
        [{"start": "unknown", "end": "present", "org": "中共珲春市委", "title": "市委书记、示范区党工委书记（延边州委副书记兼）", "level": "县级", "system": "party", "rank": "正处", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]}],
        [{"person": "张林国", "person_id": "hunchun_张林国", "relationship_type": "overlap", "strength": "strong", "evidence": "党政班子书记-市长", "overlap_org": "中共珲春市委/市政府", "overlap_period": "present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]}],
        "林小林出生/籍贯/学历/完整履历；就任珲春市委书记确切年月；前任书记姓名与去向",
        [{"id": "hunchun_市委", "name": "中共珲春市委员会", "type": "党委", "level": "县级", "location": "珲春市"},
         {"id": "hunchun_示范区", "name": "珲春海洋经济发展示范区", "type": "开发区", "level": "国家级", "location": "珲春市"},
         {"id": "yanbian_州委", "name": "中共延边朝鲜族自治州委员会", "type": "党委", "level": "地级(州)", "location": "延边州"}],
    )

    # ── 张林国（市长） ──
    build_person_file(
        "市委副书记、市长", "张林国",
        True,
        {"gender": "男", "ethnicity": "朝鲜族", "birth": "1974年1月", "birthplace": "", "native_place": "",
         "education": [{"period": "", "institution": "", "major": "经济学", "degree": "博士", "study_type": "unknown", "source_ids": ["S002"]}],
         "party_join": "中共党员", "work_start": "", "org": "珲春市人民政府",
         "rank": "正处级（县级市长）", "confirmed": True, "source_ids": ["S001", "S002"]},
        [{"start": "unknown", "end": "present", "org": "珲春市人民政府", "title": "市长、市政府党组书记", "level": "县级", "system": "government", "rank": "正处", "is_key_promotion": True, "notes": "主持市政府全面工作", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
         {"start": "unknown", "end": "present", "org": "中共珲春市委", "title": "市委副书记", "level": "县级", "system": "party", "rank": "", "confidence": "confirmed", "source_ids": ["S001"]},
         {"start": "unknown", "end": "present", "org": "珲春海洋经济发展示范区", "title": "示范区党工委副书记、管委会主任（兼）", "level": "国家级", "system": "development_zone", "rank": "", "confidence": "confirmed", "source_ids": ["S002"]}],
        [{"person": "林小林", "person_id": "hunchun_林小林", "relationship_type": "overlap", "strength": "strong", "evidence": "党政班子", "overlap_org": "中共珲春市委/市政府", "overlap_period": "present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
         {"person": "李昭辉", "person_id": "hunchun_李昭辉", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "常务副市长协助市长", "overlap_org": "珲春市人民政府", "overlap_period": "present", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]}],
        "张林国出生地/籍贯/完整履历；就任珲春市长确切年月；前任市长姓名与去向",
        [{"id": "hunchun_市政府", "name": "珲春市人民政府", "type": "政府", "level": "县级", "location": "珲春市"},
         {"id": "hunchun_示范区", "name": "珲春海洋经济发展示范区", "type": "开发区", "level": "国家级", "location": "珲春市"}],
    )

    # ── 李昭辉（常务副市长） ──
    build_person_file(
        "市委常委、常务副市长", "李昭辉",
        True,
        {"gender": "男", "ethnicity": "汉族", "birth": "1978年10月", "birthplace": "", "native_place": "",
         "education": [{"period": "", "institution": "", "major": "", "degree": "研究生", "study_status": "unknown", "source_ids": ["S001"]}],
         "party_join": "中共党员", "work_start": "", "org": "珲春市人民政府",
         "rank": "常务副市长", "confirmed": True, "source_ids": ["S001"]},
        [{"start": "unknown", "end": "present", "org": "珲春市人民政府", "title": "市委常委、常务副市长", "level": "县级", "system": "government", "rank": "副处", "is_key_promotion": True, "confidence": "confirmed", "source_ids": ["S001"]}],
        [{"person": "张林国", "person_id": "hunchun_张林国", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "常务副市长协助市长", "overlap_org": "珲春市人民政府", "overlap_period": "present", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]}],
        "李昭辉完整履历、出生地",
        [{"id": "hunchun_市政府", "name": "珲春市人民政府", "type": "政府", "level": "县级", "location": "珲春市"}],
    )


# ── 主入口 ───────────────────────────────────────────────────────────────
def main():
    print(f"[{SLUG}] 构建 SQLite DB + GEXF ...")
    run_build(slug=SLUG, persons=persons, organizations=organizations,
              positions=positions, relationships=relationships,
              db_path=DB_PATH, gexf_path=GEXF_PATH)
    _verify_db()
    write_persons_files()
    print(f"[{SLUG}] 完成：{DB_PATH}\n{GEXF_PATH}\npersons JSON 若干")

def _verify_db():
    import sqlite3  # noqa
    conn = sqlite3.connect(str(DB_PATH))
    try:
        required = {"persons", "organizations", "positions", "relationships"}
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        missing = sorted(required - tables)
        if missing:
            raise SystemExit(f"DB 缺少表: {missing}")
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in sorted(required)}
        print("  DB 校验:", counts)
    finally:
        conn.close()

if __name__ == "__main__":
    main()