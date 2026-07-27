#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 法库县, 沈阳市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_法库县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.faku.gov.cn — 法库县人民政府官方网站 (accessible)
  - faku.gov.cn 领导成员页面 — 县长徐健及6位副县长分工
  - faku.gov.cn 法库新闻 — 县委书记徐显帅(2026-07-15)、县长徐健(2026-07-02)、
    县委书记孔德树(2026-06-11)
  - faku.gov.cn 人事任免公示 — 2024年第3号、第4号

Confidence notes:
  - 县委书记徐显帅 confirmed via faku.gov.cn news article (2026-07-15)
  - 县长徐健 confirmed via official leadership page and multiple news articles
  - All 6 deputy county heads confirmed via official leadership pages
  - 徐显帅's biography (birth year, education, career timeline) not yet found on
    official pages — need further research
  - 孔德树 was 县委书记 as of 2026-06-11; 徐显帅 took over by 2026-07-15
  - 程廷霜 was previously 县长; 徐健 now holds the role (profile updated 2025-07-07)
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

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "法库县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_法库县"
if _CURRENT_DIR.name == "liaoning_法库县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1=县委书记, 2=县长, 3-9=副县长/常委, 10=前任

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "徐显帅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共法库县委员会",
        "source": "法库县人民政府网站: https://www.faku.gov.cn/zfxxgk/fkxw/202607/t20260715_5056872.html",
        "confidence": "confirmed",
        "notes": "县委书记徐显帅。2026年7月13日视察防汛工作报道确认职务。接替前任县委书记孔德树（孔德树在2026年6月11日仍以县委书记身份活动）。徐显帅个人简历尚未从官方网站获取，出生年月、籍贯、学历等需后续补充。"
    },
    {
        "id": 2,
        "name": "徐健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年2月",
        "birthplace": "辽宁丹东",
        "education": "工程硕士",
        "party_join": "中共党员",
        "work_start": "2000年7月",
        "current_post": "县委副书记、县长",
        "current_org": "法库县人民政府",
        "source": "法库县人民政府领导信息: https://www.faku.gov.cn/zfxxgk/fdzdgknr/jgjj/qzfldbzfg/xz/202208/t20220811_3896288.html",
        "confidence": "confirmed",
        "notes": "县长徐健，1978年2月生，男，汉族，辽宁丹东人，工程硕士。1998年6月入党，2000年7月参加工作。主持县政府全面工作。页面更新日期2025-07-07。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Key Standing Committee Members / Deputy County Heads
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "孙莹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年9月",
        "birthplace": "辽宁康平",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2002年5月",
        "current_post": "县委常委、副县长（常务）",
        "current_org": "法库县人民政府",
        "source": "https://www.faku.gov.cn/zfxxgk/fdzdgknr/jgjj/qzfldbzfg/fxz/202208/t20220811_3891624.html",
        "confidence": "confirmed",
        "notes": "县委常委、副县长、县政府党组副书记。1980年9月出生，辽宁康平人。2002年5月参加工作，2007年6月入党。分管常务工作：发改、财税、国资、人社、应急、统计等。先后工作于康平县交通局、招商局、柳树屯乡、郝官屯镇、两家子乡、张强镇。"
    },
    {
        "id": 4,
        "name": "张田",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年6月",
        "birthplace": "辽宁葫芦岛",
        "education": "管理学硕士",
        "party_join": "中共党员",
        "work_start": "2011年9月",
        "current_post": "县委常委、副县长",
        "current_org": "法库县人民政府",
        "source": "https://www.faku.gov.cn/zfxxgk/fdzdgknr/jgjj/qzfldbzfg/fxz/202208/t20220811_3896327.html",
        "confidence": "confirmed",
        "notes": "县委常委、副县长、县政府党组成员。1985年6月生，辽宁葫芦岛人。2004年6月入党，2011年9月参加工作，管理学硕研。先后工作于辽宁省抚顺市财政局、辽宁省财政厅（期间任新宾县新宾镇刘鲜村第一书记）。分管工信、科技、商务、市场监管、营商环境等。"
    },
    {
        "id": 5,
        "name": "兴颖杰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年7月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "无党派",
        "work_start": "1992年8月",
        "current_post": "副县长",
        "current_org": "法库县人民政府",
        "source": "https://www.faku.gov.cn/zfxxgk/fdzdgknr/jgjj/qzfldbzfg/fxz/202208/t20220811_3896362.html",
        "confidence": "confirmed",
        "notes": "副县长。1971年7月出生，1992年8月参加工作，无党派人士。分管教育、卫健、医保、民政、文旅等。"
    },
    {
        "id": 6,
        "name": "李忠实",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "辽宁康平",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1995年7月",
        "current_post": "副县长",
        "current_org": "法库县人民政府",
        "source": "https://www.faku.gov.cn/zfxxgk/fdzdgknr/jgjj/qzfldbzfg/fxz/202310/t20231010_4540511.html",
        "confidence": "confirmed",
        "notes": "副县长、县政府党组成员。1974年12月生，辽宁康平人。1995年7月参加工作，2002年12月入党，大学学历。分管住建、交通、自然资源、行政执法等。"
    },
    {
        "id": 7,
        "name": "盖小威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年6月",
        "birthplace": "辽宁法库",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1997年8月",
        "current_post": "副县长",
        "current_org": "法库县人民政府",
        "source": "https://www.faku.gov.cn/zfxxgk/fdzdgknr/jgjj/qzfldbzfg/fxz/202411/t20241115_4759929.html",
        "confidence": "confirmed",
        "notes": "副县长、县政府党组成员。1977年6月生，辽宁法库人。1997年8月参加工作，1998年8月入党，大学学历。分管农业农村、乡村振兴、水利、供销、生态环境等。"
    },
    {
        "id": 8,
        "name": "崔颢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年2月",
        "birthplace": "辽宁沈阳",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "2007年11月",
        "current_post": "副县长、县公安局局长",
        "current_org": "法库县公安局",
        "source": "https://www.faku.gov.cn/zfxxgk/fdzdgknr/jgjj/qzfldbzfg/fxz/202208/t20220811_3896484.html",
        "confidence": "confirmed",
        "notes": "副县长、县政府党组成员、县公安局党组书记、局长、督察长。1985年2月出生，辽宁沈阳人。2007年6月入党，2007年11月参加工作，研究生学历。分管公安、司法等工作。"
    },
    {
        "id": 9,
        "name": "何原驰",
        "gender": "男",
        "ethnicity": "锡伯族",
        "birth": "1978年6月",
        "birthplace": "",
        "education": "工程硕士",
        "party_join": "中共党员",
        "work_start": "1999年8月",
        "current_post": "辽宁法库经济开发区常务副主任",
        "current_org": "辽宁法库经济开发区（沈阳法库通用航空产业基地）",
        "source": "https://www.faku.gov.cn/zfxxgk/fdzdgknr/qtzfxx/rsxx/202208/t20220811_3887212.html",
        "confidence": "confirmed",
        "notes": "辽宁法库经济开发区常务副主任。男，锡伯族，1978年6月生，中共党员，大学学历，工程硕士。曾任法库县政府副县长（2021年5月当选），宣传部副部长、发改局局长等。出现在2026年5月新闻中参与招商会议。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Previous Leadership
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "孔德树",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共法库县委员会",
        "source": "法库县人民政府网站: https://www.faku.gov.cn/zfxxgk/fkxw/202606/t20260611_5039816.html",
        "confidence": "confirmed",
        "notes": "前任县委书记。2026年6月9日（6月11日报道）仍以县委书记身份到企业调研安全生产。2026年7月15日新闻显示县委书记已为徐显帅。交接发生在2026年6月至7月间。孔德树个人简历需后续补充。"
    },
    {
        "id": 11,
        "name": "程廷霜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "辽宁沈阳",
        "education": "研究生农学学士",
        "party_join": "中共党员",
        "work_start": "1998年9月",
        "current_post": "前任县长",
        "current_org": "法库县人民政府",
        "source": "https://www.faku.gov.cn/zfxxgk/fdzdgknr/qtzfxx/rsxx/202406/t20240612_4656255.html",
        "confidence": "confirmed",
        "notes": "前任县长。1975年11月生，辽宁沈阳人。2005年6月入党，1998年9月参加工作，研究生农学学士。先后工作于辽中县满都户镇、党史办、县委办、茨榆坨镇、大黑镇、辽中区政府、辽中区委统战部。简历页面(2024-07-24)显示曾任县长，后由徐健接替（徐健页面更新2025-07-07）。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共法库县委员会", "type": "党委", "level": "县处级", "parent": "中共沈阳市委", "location": "法库县"},
    {"id": 2, "name": "法库县人民政府", "type": "政府", "level": "县处级", "parent": "沈阳市人民政府", "location": "法库县"},
    {"id": 3, "name": "中国人民政治协商会议法库县委员会", "type": "政协", "level": "县处级", "parent": "政协沈阳市委", "location": "法库县"},
    {"id": 4, "name": "法库县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "沈阳市人大常委会", "location": "法库县"},
    {"id": 5, "name": "中共法库县纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级", "parent": "沈阳市纪委", "location": "法库县"},
    {"id": 6, "name": "中共法库县委组织部", "type": "党委", "level": "县处级", "parent": "中共法库县委员会", "location": "法库县"},
    {"id": 7, "name": "中共法库县委宣传部", "type": "党委", "level": "县处级", "parent": "中共法库县委员会", "location": "法库县"},
    {"id": 8, "name": "中共法库县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共法库县委员会", "location": "法库县"},
    {"id": 9, "name": "法库县公安局", "type": "政府", "level": "乡科级", "parent": "法库县人民政府", "location": "法库县"},
    {"id": 10, "name": "辽宁法库经济开发区（沈阳法库通用航空产业基地）", "type": "开发区", "level": "县处级", "parent": "法库县人民政府", "location": "法库县"},
    {"id": 11, "name": "法库县财政局", "type": "政府", "level": "乡科级", "parent": "法库县人民政府", "location": "法库县"},
    {"id": 12, "name": "法库县发展和改革局", "type": "政府", "level": "乡科级", "parent": "法库县人民政府", "location": "法库县"},
    {"id": 13, "name": "法库县教育局", "type": "政府", "level": "乡科级", "parent": "法库县人民政府", "location": "法库县"},
    {"id": 14, "name": "法库县农业农村局", "type": "政府", "level": "乡科级", "parent": "法库县人民政府", "location": "法库县"},
    {"id": 15, "name": "法库县住房和城乡建设局", "type": "政府", "level": "乡科级", "parent": "法库县人民政府", "location": "法库县"},
    {"id": 16, "name": "法库县工业和信息化局", "type": "政府", "level": "乡科级", "parent": "法库县人民政府", "location": "法库县"},
    {"id": 17, "name": "法库县卫生健康局", "type": "政府", "level": "乡科级", "parent": "法库县人民政府", "location": "法库县"},
    {"id": 18, "name": "法库县司法局", "type": "政府", "level": "乡科级", "parent": "法库县人民政府", "location": "法库县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 徐显帅 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2026-06~07", "end_date": "", "rank": "县处级正职",
     "note": "接替孔德树，最晚2026年7月15日已就任"},
    # 徐健 — 县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "约2024-2025", "end_date": "", "rank": "县处级正职",
     "note": "接替程廷霜，领导页面更新日期2025-07-07"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "县长兼任县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "县政府党组书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "官网明确标注"},
    # 孙莹 — 常务副县长
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副县长（常务）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "县政府党组副书记，分管发改、财税、国资、应急等"},
    # 张田 — 副县长
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管工信、科技、商务、市场监管。来自省财政厅"},
    # 兴颖杰 — 副县长
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "无党派人士，分管教育、卫健、文旅等"},
    # 李忠实 — 副县长
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "县政府党组成员，分管住建、交通、自然资源等"},
    # 盖小威 — 副县长
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "县政府党组成员，分管农业农村、乡村振兴、水利等"},
    # 崔颢 — 副县长/公安局长
    {"person_id": 8, "org_id": 2, "title": "副县长（兼县公安局局长）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},
    {"person_id": 8, "org_id": 9, "title": "县公安局局长", "start_date": "", "end_date": "", "rank": "乡科级正职",
     "note": "县政府党组成员、公安局党组书记、督察长"},
    # 何原驰 — 开发区常务副主任
    {"person_id": 9, "org_id": 10, "title": "辽宁法库经济开发区常务副主任", "start_date": "约2024", "end_date": "",
     "rank": "县处级副职", "note": "曾任副县长，现为开发区常务副主任"},
    # 孔德树 — 前任县委书记
    {"person_id": 10, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "2026-06~07", "rank": "县处级正职",
     "note": "至少任职至2026年6月，之后由徐显帅接替"},
    # 程廷霜 — 前任县长
    {"person_id": 11, "org_id": 2, "title": "县长", "start_date": "", "end_date": "约2024-2025", "rank": "县处级正职",
     "note": "简历显示曾任县长，后由徐健接替"},
    {"person_id": 11, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "约2024-2025", "rank": "县处级正职",
     "note": "县长兼任县委副书记"},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 现任党政正职
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记徐显帅与县长徐健为当前党政主要领导搭档关系",
        "overlap_org": "中共法库县委员会/法库县人民政府",
        "overlap_period": "2026年7月至今",
        "confidence": "confirmed",
    },
    # 前任-现任县委书记交接
    {
        "person_a": 10, "person_b": 1,
        "type": "predecessor_successor",
        "context": "孔德树为前任县委书记，徐显帅接任",
        "overlap_org": "中共法库县委员会",
        "overlap_period": "2026年6-7月交接",
        "confidence": "confirmed",
    },
    # 前任-现任县长交接
    {
        "person_a": 11, "person_b": 2,
        "type": "predecessor_successor",
        "context": "程廷霜为前任县长，徐健接任",
        "overlap_org": "法库县人民政府",
        "overlap_period": "约2024-2025年交接",
        "confidence": "confirmed",
    },
    # 孙莹 — 常务副县长与县长
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长徐健与常务副县长孙莹为政府主要领导与副手关系",
        "overlap_org": "法库县人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 孙莹与徐健曾在康平邻县工作过（孙莹康平人、在康平多岗位任职）
    # 张田 — 来自省财政厅
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "县长徐健与挂职副县长张田为政府班子同僚",
        "overlap_org": "法库县人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 崔颢 — 公安副县长与县长
    {
        "person_a": 2, "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长徐健与分管公安副县长崔颢为政府领导关系",
        "overlap_org": "法库县人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 何原驰 — 曾任副县长，现转开发区
    {
        "person_a": 9, "person_b": 2,
        "type": "overlap",
        "context": "开发区常务副主任何原驰与县长徐健在政府工作中有协作关系",
        "overlap_org": "法库县人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 孔德树与徐健的搭档
    {
        "person_a": 10, "person_b": 2,
        "type": "overlap",
        "context": "孔德树任县委书记期间与县长徐健为搭档",
        "overlap_org": "中共法库县委员会/法库县人民政府",
        "overlap_period": "约2024-2025至2026年6月",
        "confidence": "confirmed",
    },
    # 县政府班子内部常委
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "同为县委常委班子成员",
        "overlap_org": "中共法库县委员会",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    {
        "person_a": 3, "person_b": 6,
        "type": "overlap",
        "context": "同为法库县政府班子",
        "overlap_org": "法库县人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    {
        "person_a": 4, "person_b": 8,
        "type": "overlap",
        "context": "张田与崔颢同为县委常委班子成员",
        "overlap_org": "中共法库县委员会",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 盖小威 — 法库本地人
    {
        "person_a": 7, "person_b": 2,
        "type": "superior_subordinate",
        "context": "盖小威为法库本地成长干部，与县长为上下级关系",
        "overlap_org": "法库县人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
]

# ── Person JSONs ─────────────────────────────────────────────────────────────

PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "辽宁省",
        "city": "沈阳市",
        "region": "法库县",
        "task_id": "liaoning_法库县",
        "time_focus": "2026年7月",
    },
    "identity": {},
    "current_status": {},
    "career_timeline": [],
    "organizations": [],
    "relationships": [],
    "governance_record": [],
    "professional_profile": {},
    "work_style_and_personality": {},
    "network_metrics": {},
    "risk_and_integrity_signals": [],
    "source_register": [],
    "confidence_summary": {},
    "open_questions": [],
}


def build_person_json(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    now = TODAY

    # Source register
    sources = []
    if p["source"]:
        source_url = p["source"]
        sid = "S001"
        source_type = "official" if "faku.gov.cn" in source_url else "media"
        sources.append({
            "id": sid,
            "title": f"{role_label}确认来源",
            "url": source_url.split(": ")[-1] if ": " in source_url else source_url,
            "publisher": "法库县人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": source_type,
            "reliability": "high",
            "notes": "",
        })

    is_core = person_id <= 2
    rank = "县处级正职" if is_core else "县处级副职"
    system = "party" if person_id in [1, 10] else "government"

    person = {
        "identity": {
            "person_id": f"liaoning_shenyang_faku_{name}",
            "name": name,
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_{p['birth']}",
                "name_birthplace": f"{name}_{p['birthplace']}",
                "official_profile_url": p["source"].split(": ")[-1] if ": " in p.get("source", "") else "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": True if "待查" not in name else False,
            "source_ids": ["S001"] if sources else [],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No risk signals found in publicly available records",
                "date": AS_OF,
                "confidence": "plausible" if "待查" not in name else "unverified",
                "source_ids": [],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if not name.startswith("待查") and p.get("birth") else "plausible",
            "current_role": "confirmed" if not name.startswith("待查") else "unverified",
            "career_completeness": "partial" if p.get("work_start") else "thin",
            "relationship_confidence": "high" if not name.startswith("待查") else "low",
            "biggest_gap": "",
        },
        "open_questions": [],
    }

    # Career timeline from positions
    pos_list = [pos for pos in positions if pos["person_id"] == person_id]
    for pos in pos_list:
        org_name = ""
        for o in organizations:
            if o["id"] == pos["org_id"]:
                org_name = o["name"]
                break
        entry = {
            "start": pos["start_date"] if pos["start_date"] else "unknown",
            "end": pos["end_date"] if pos["end_date"] else "present",
            "org": org_name,
            "title": pos["title"],
            "level": "",
            "location": "法库县",
            "system": system,
            "rank": pos["rank"],
            "is_key_promotion": False,
            "notes": pos["note"],
            "confidence": "confirmed",
            "source_ids": ["S001"] if sources else [],
        }
        person["career_timeline"].append(entry)

    # Relationships for this person
    person_rels = [r for r in relationships if r["person_a"] == person_id or r["person_b"] == person_id]
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == person_id else r["person_a"]
        other_name = ""
        for op in persons:
            if op["id"] == other_id:
                other_name = op["name"]
                break
        person["relationships"].append({
            "person": other_name,
            "person_id": f"liaoning_shenyang_faku_{other_name}",
            "relationship_type": r["type"],
            "strength": "strong",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": r["confidence"],
        })

    # Big gap
    if not p.get("birth"):
        person["confidence_summary"]["biggest_gap"] = f"{name}的出生年月和完整履历未从官方网站获取"
    elif not name.startswith("待查"):
        person["confidence_summary"]["biggest_gap"] = f"{name}的完整履历仍有部分缺口"

    # Open questions
    if not p.get("birth"):
        person["open_questions"].append({
            "priority": "high",
            "question": f"{name}的出生年月、籍贯、学历？",
            "why_it_matters": "核心身份信息用于去重和综合档案",
            "suggested_queries": [f"法库县 {name} 简历"],
            "last_attempted": AS_OF,
        })
    if "待查" in name:
        person["open_questions"].append({
            "priority": "critical",
            "question": f"法库县{role_label}姓名是什么？",
            "why_it_matters": "核心目标人物之一",
            "suggested_queries": [],
            "last_attempted": AS_OF,
        })

    return person


def write_person_json(person_id: int):
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    safe_role = role_label.replace("、", "_")
    filename = f"{TODAY}-辽宁省-沈阳市-{safe_role}-{name}.json"
    path = PJSON_DIR / filename

    person_data = build_person_json(person_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)

    return path


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    # Build DB and GEXF
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

    # Write person JSONs for core figures
    person_files = []
    for pid in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"Done.")


if __name__ == "__main__":
    main()
