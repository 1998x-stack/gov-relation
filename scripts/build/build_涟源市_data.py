#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 涟源市 (Lianyuan), 湖南省.

Investigation date: 2026-08-06
Task ID: hunan_涟源市
Province: 湖南省
Parent city: 娄底市
Level: 县级市
Targets: 市委书记 & 市长

Key finding: 涟源市第十四次党代会于 2026-07-28/30 召开, 产生新一届市委领导班子.
            原市长 邓伟谋 于 2026-05 末/06 初离任, 市委副书记、代理市长 伍鹤群 接任
            (2026-06-16 起主持市政府第11次常务会议). 官方"领导之窗"标注伍鹤群为"代市长",
            尚未经市人大正式选举转正.

Research sources (官方, accessed 2026-08-06):
  - https://www.lianyuan.gov.cn/lianyuan/zwgk/0030301/zwgk_leader_list.shtml  (市委领导 - 现任名单)
  - https://www.lianyuan.gov.cn/lianyuan/zwgk/0030303/zwgk_leader_list.shtml  (市政府领导)
  - https://www.lianyuan.gov.cn/lianyuan/zwgk/0030304/zwgk_leader_list.shtml  (市政协领导)
  - 各领导详情页 (领导之窗"个人简历"一行 + 分工)
  - 涟源市政府"政务要闻": 第十四次党代会(2026-07-28/30), 伍鹤辉 建军节走访/防讯抗旱/第13次常务会(2026-07-30), 段晓秋 经济运行调度会(2026-07-24)
  - 项目娄底市 build (2026-07-24) data/database/娄底市_network.db 提供前任/市人大/政协基线

Confidence notes:
  - 现任职务: confirmed via 官方领导之窗 + 政务要闻
  - 身份字段(出生/籍贯/学历): confirmed via 官方简历一行
  - 完整历届履历(前职/日期): 官方领导之窗仅提供一行简介, 未发布完整职务履历
      => 记为 open_gaps; 段晓秋由衡山县调入(2025-03, 父项目娄底 build), 邓伟谋任市长至2026-05-22(常务会)
  - Exa 限流, Bing/Jina/百度 受阻, 依赖官方站直接抓取
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402

import sqlite3  # noqa: F401  (DB output is SQLite, produced via gov_relation.runner)

# ── Metadata ────────────────────────────────────────────────────────────────
SLUG = "涟源市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Paths ────────────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_涟源市"
if _CURRENT_DIR.name == "hunan_涟源市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# Consolidated official source URLs (行政之窗 领导之窗)
ORG_OFFICIAL = "https://www.lianyuan.gov.cn"
SRC_DUAN = "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030301/201612/7588874534ff4c05b94d231660f01ce7.shtml"
SRC_WU = "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030301/201801/8087bd5facb74c16b899179f92074f11.shtml"
SRC_ZHOU = "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030301/201709/c65361aa88c840228760b9bbfade0ff4.shtml"
SRC_LIST_SW = "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030301/zwgk_leader_list.shtml"
SRC_LIST_ZW = "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030303/zwgk_leader_list.shtml"
SRC_LOB = "data/database/娄底市_network.db (project build 2026-07-24)"

# ├─ Persons ────────────────────────────────────────────────────────────────
# ID 分层: 1-10 现任市委常委/核心; 20-24 市政府副职; 30 人大主任; 40 政协主席; 90 前任干部
persons = [
    # ── 核心领导 (targets) ───────────────────────────────────────────────
    {
        "id": 1, "name": "段晓赛", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-12", "birthplace": "湖南省耒阳市", "education": "研究生学历",
        "party_join": "", "work_start": "",
        "current_post": "市委书记", "current_org": "中共涟源市委",
        "source": SRC_DUAN, "confidence": "confirmed",
        "notes": "2025-03 由衡阳市衡山县跨市调任涟源市委书记(兼娄底高新区党工委书记). 官方简历: 男,汉,研究生学历,湖南耒阳人,1975-12生,党员.",
    },
    {
        "id": 2, "name": "伍鹤群", "gender": "男", "ethnicity": "汉族",
        "birth": "1980-10", "birthplace": "湖南省新化县", "education": "本科学历",
        "party_join": "", "work_start": "",
        "current_post": "市委副书记、代市长", "current_org": "中共涟源市委/涟源市人民政府",
        "source": SRC_WU, "confidence": "confirmed",
        "notes": "2026-05月末~06初任市委副书记、代市长, 接替邓伟谋; 2026-06-16起主持市政府常务(党组)会议(第11次). 官方简历: 男,汉,本科,湖南新化人,1980-10生,党员.",
    },
    {
        "id": 3, "name": "周杨", "gender": "男", "ethnicity": "汉族",
        "birth": "1990-05", "birthplace": "湖北省罗田县", "education": "研究生学历(管理学博士)",
        "party_join": "", "work_start": "",
        "current_post": "市委副书记、市委统战部部长、市委党校校长", "current_org": "中共涟源市委",
        "source": SRC_ZHOU, "confidence": "confirmed",
        "notes": "第二副书记; 1990-05生, 湖北罗田人, 管理学博士; 分工:协(书记处理日常党务/统战).",
    },
    # ── 市委常委会其余 ──────────────────────────────────────────────────
    {
        "id": 4, "name": "谢聪", "gender": "女", "ethnicity": "汉族",
        "birth": "1978-01", "birthplace": "湖南省涟源市", "education": "研究生学历",
        "party_join": "", "work_start": "",
        "current_post": "市委常委、常务副市长", "current_org": "中共涟源市委/涟源市人民政府",
        "source": SRC_LIST_SW, "confidence": "confirmed",
        "notes": "常务副市长; 1978-01生, 湖南涟源人, 研究生学历.",
    },
    {
        "id": 5, "name": "易专", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-03", "birthplace": "湖南省涟源市", "education": "本科学历",
        "party_join": "", "work_start": "",
        "current_post": "市委常委、市委办公室主任", "current_org": "中共涟源市委",
        "source": "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030301/201609/dbbb9064dea246399d82f8295fe004e3.shtml",
        "confidence": "confirmed",
        "notes": "市委办主任; 1975-03生, 涟源人.",
    },
    {
        "id": 6, "name": "彭余辉", "gender": "女", "ethnicity": "汉族",
        "birth": "1983-04", "birthplace": "湖南省娄星区", "education": "研究生学历",
        "party_join": "", "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任", "current_org": "中共涟源市委/涟源市监察委",
        "source": "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030301/201801/f86d761fbaac49e09208842ed3988f4.shtml",
        "confidence": "confirmed",
        "notes": "纪委书记/监委主任; 1983-04生, 湖南娄星人.",
    },
    {
        "id": 7, "name": "周新科", "gender": "男", "ethnicity": "汉族",
        "birth": "1981-03", "birthplace": "湖南省涟源市", "education": "本科学历",
        "party_join": "", "work_start": "",
        "current_post": "市委常委、宣传部部长", "current_org": "中共涟源市委",
        "source": "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030301/201801/84242a96d37d4fa6b366cc5e95bcf615.shtml",
        "confidence": "confirmed",
        "notes": "宣传部长; 1981-03生, 涟源人.",
    },
    {
        "id": 8, "name": "黄和平", "gender": "男", "ethnicity": "汉族",
        "birth": "1980-06", "birthplace": "湖南省湘乡市", "education": "大专学历",
        "party_join": "", "work_start": "",
        "current_post": "市委常委、政法委书记、副市长", "current_org": "中共涟源市委/涟源市人民政府",
        "source": "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030301/201612/65a146e8f19d4da4b1f9df7f7b2858.shtml",
        "confidence": "confirmed",
        "notes": "常年政法委书记兼副市长; 1980-06生, 湘乡人, 大专学历.",
    },
    {
        "id": 9, "name": "王昆", "gender": "男", "ethnicity": "汉族",
        "birth": "1985-11", "birthplace": "湖南省新化县", "education": "大学学历",
        "party_join": "", "work_start": "",
        "current_post": "市委常委、市委组织部部长", "current_org": "中共涟源市委",
        "source": "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030301/201912/15df563f1a044253bf368a94b3f8c291.shtml",
        "confidence": "confirmed",
        "notes": "组织部长; 1985-11生, 新化人.",
    },
    {
        "id": 10, "name": "曾志文", "gender": "男", "ethnicity": "汉族",
        "birth": "1985-03", "birthplace": "湖南省新化县", "education": "研究生学历",
        "party_join": "", "work_start": "",
        "current_post": "市委常委、副市长候选人", "current_org": "中共涟源市委/涟源市人民政府",
        "source": "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030301/201912/466e86ee79593c9dc1e7102d298ee.shtml",
        "confidence": "confirmed",
        "notes": "常委、副市长候选人提名人选(待人大任命); 1985-03生, 新化人.",
    },
    # ── 其他市政府副职 ──────────────────────────────────────────────────
    {
        "id": 20, "name": "佘威", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-12", "birthplace": "湖南省双峰县", "education": "大专学历",
        "party_join": "", "work_start": "",
        "current_post": "市政府党组成员、副市长、市公安局局长", "current_org": "涟源市人民政府/涟源市公安局",
        "source": "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030303/201801/464fd315db4441215ba03ed5c0fb97c29.shtml",
        "confidence": "confirmed",
        "notes": "公安局长/副市长; 1978-12生, 双峰人.",
    },
    {
        "id": 21, "name": "肖鸿杰", "gender": "男", "ethnicity": "汉族",
        "birth": "1987-02", "birthplace": "湖南省娄底市", "education": "本科学历",
        "party_join": "", "work_start": "",
        "current_post": "市政府党组成员、副市长", "current_org": "涟源市人民政府",
        "source": "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030303/201801/c84fb3e37524211a24a51b1a75162e37e.shtml",
        "confidence": "confirmed",
        "notes": "副市长; 1987-02生, 娄底人.",
    },
    {
        "id": 22, "name": "郭慕升", "gender": "男", "ethnicity": "汉族",
        "birth": "1986-01", "birthplace": "湖南省涟源市", "education": "研究生学历",
        "party_join": "", "work_start": "",
        "current_post": "市政府党组成员、副市长", "current_org": "涟源市人民政府",
        "source": "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030303/201801/9394f0429e074622a472b6a42c9f615.shtml",
        "confidence": "confirmed",
        "notes": "副市长; 1986-01生, 涟源人.",
    },
    # ── 人大 / 政协 ──────────────────────────────────────────────────────
    {
        "id": 30, "name": "梁育清", "gender": "女", "ethnicity": "汉族",
        "birth": "1967-11", "birthplace": "湖南省涟源市", "education": "本科学历",
        "party_join": "", "work_start": "",
        "current_post": "市人大常委会主任、党组书记", "current_org": "涟源市人大常委会",
        "source": "https://www.lianyuan.gov.cn/lianyuan/zwgk/00303011/201703/48c3a00f35e74cb3bbe09d274b004faa.shtml",
        "confidence": "confirmed",
        "notes": "人大主任(自2021); 1967-11生, 涟源人, 女.",
    },
    {
        "id": 31, "name": "周惠军", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-03", "birthplace": "湖南省娄底市", "education": "本科学历",
        "party_join": "", "work_start": "",
        "current_post": "市政协主席、党组书记", "current_org": "涟源市政协",
        "source": "https://www.lianyuan.gov.cn/lianyuan/zwgk/0030304/201905/41796b37138c4aa3aaa6d25c2ef415f.shtml",
        "confidence": "confirmed",
        "notes": "政协主席(自2021-10); 1971-03生, 娄底人.",
    },
    # ── 前任干部 ─────────────────────────────────────────────────────────
    {
        "id": 50, "name": "邓伟谋", "gender": "男", "ethnicity": "汉族",
        "birth": "1976", "birthplace": "湖南省双峰县", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "前任市长", "current_org": "（离任）",
        "source": SRC_LIST_ZW, "confidence": "confirmed",
        "notes": "历任涟源市长/原市长; 2021-07任市长; 2026-05-22主持市政府第10次常务会议后离任; 去向上待查; 双峰人.",
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共涟源市委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "涟源市"},
    {"id": 2, "name": "涟源市人民政府", "type": "政府", "level": "县级", "parent": "", "location": "涟源市"},
    {"id": 3, "name": "涟源市人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "涟源市"},
    {"id": 4, "name": "涟源市政协", "type": "政协", "level": "县级", "parent": "", "location": "涟源市"},
    {"id": 5, "name": "涟源市公安局", "type": "政府", "level": "县级", "parent": "涟源市人民政府", "location": "涟源市"},
    {"id": 6, "name": "娄底高新区党工委", "type": "党委", "level": "省级园区", "parent": "中共娄底市委", "location": "涟源市"},
    {"id": 7, "name": "中共娄底市委", "type": "党委", "level": "地级", "parent": "中共湖南省委", "location": "娄底市"},
    {"id": 8, "name": "中共衡山县委", "type": "党委", "level": "县级", "parent": "中共衡阳市委", "location": "衡山县（衡阳市）"},
    {"id": 9, "name": "中共新化县委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "新化县"},
    {"id": 10, "name": "中共双峰县委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "双峰县"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 段晓赛 (书记)
    {"person_id": 1, "org_id": 1, "title": "涟源市委书记", "start_date": "2025-03", "end_date": "", "rank": "副厅级",
     "note": "2025-03 由衡山县(衡阳市)跨市调入; 兼娄底高新区党工委书记"},
    {"person_id": 1, "org_id": 8, "title": "衡山县委书记(前任)", "start_date": "", "end_date": "2025-03", "rank": "正处级",
     "note": "2025-03 离任转涟源; 具体到任年月待查"},
    # 伍鹤群 (代市长)
    {"person_id": 2, "org_id": 1, "title": "涟源市委副书记", "start_date": "2026-05", "end_date": "", "rank": "副厅级",
     "note": "2026-05末~06初任市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "涟源市代理市长", "start_date": "2026-06", "end_date": "", "rank": "正处级(代)",
     "note": "2026-06-16起主持市政府常务会议(第11次)"},
    # 周杨 (第二副书记)
    {"person_id": 3, "org_id": 1, "title": "涟源市委副书记、统战部部长、市委党校校长", "start_date": "", "end_date": "",
     "rank": "副厅级", "note": ""},
    # 常委会
    {"person_id": 4, "org_id": 1, "title": "涟源市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "党组副书记"},
    {"person_id": 4, "org_id": 2, "title": "涟源市常务副市长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "涟源市委常委、市委办公室主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "涟源市委常委、市纪委书记、市监委主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "涟源市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "涟源市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "涟源市副市长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "涟源市委常委、市委组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "涟源市委常委", "start_date": "2026-07", "end_date": "", "rank": "副厅级", "note": "副市长提名人"},
    {"person_id": 10, "org_id": 2, "title": "涟源市副市长候选人提名人选", "start_date": "2026-07", "end_date": "", "rank": "正处级", "note": ""},
    # 市政府
    {"person_id": 20, "org_id": 2, "title": "涟源市副市长、市公安局局长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "涟源市副市长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 22, "org_id": 2, "title": "涟源市副市长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 人大/政协
    {"person_id": 30, "org_id": 3, "title": "涟源市人大常委会主任、党组书记", "start_date": "2021", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 31, "org_id": 4, "title": "涟源市政协主席、党组书记", "start_date": "2021-10", "end_date": "", "rank": "正处级", "note": ""},
    # 前任市长 邓伟谋
    {"person_id": 50, "org_id": 2, "title": "涟源市市长", "start_date": "2021-07", "end_date": "2026-05", "rank": "正处级",
     "note": "2021-07由代市长转正; 2026-05-22仍主持第10次常务会; 后离任(去向待查)"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 党政搭班
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "段晓赛(书记)与伍鹤群(代市长)党政搭档搭班", "overlap_org": "中共涟源市委/涟源市人民政府",
     "overlap_period": "2026"},
    {"person_a": 1, "person_b": 3, "type": "colleague",
     "context": "段晓赛(书记)与周杨(副书记/统战)同为市委班子", "overlap_org": "中共涟源市委", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 3, "type": "colleague",
     "context": "伍鹤群(代市长)与周杨(副书记/统战)同为市委班子", "overlap_org": "中共涟源市委", "overlap_period": "2026"},
    # 市长继任
    {"person_a": 50, "person_b": 2, "type": "succession",
     "context": "邓伟谋(原市长)离任, 伍鹤群接任代市长(2026-06)", "overlap_org": "涟源市人民政府",
     "overlap_period": "2026-06"},
    # 段晓秋跨市调任（外来干部）
    {"person_a": 1, "person_b": 8, "type": "cross_region",
     "context": "段晓秋由衡阳市衡山县跨市调任涟源市委书记(2025-03)", "overlap_org": "衡山县→涟源市",
     "overlap_period": "2025-03"},
    # 常委会内部交叉
    {"person_a": 4, "person_b": 2, "type": "colleague",
     "context": "谢聪(常务副市长)协助代市长伍鹤群主持工作", "overlap_org": "涟源市人民政府",
     "overlap_period": "2026"},
    # 同乡 (新化籍)
    {"person_a": 2, "person_b": 9, "type": "hometown",
     "context": "伍鹤群(新化人)与王昆(新化人)同乡", "overlap_org": "新化县", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "hometown",
     "context": "伍鹤群(新化人)与曾志文(新化人)同乡", "overlap_org": "新化县", "overlap_period": ""},
    # 涟源本地
    {"person_a": 4, "person_b": 5, "type": "hometown",
     "context": "谢聪(涟源人)与易专(涟源人)同乡", "overlap_org": "涟源市", "overlap_period": ""},
    # 前任市长与双峰系
    {"person_a": 50, "person_b": 20, "type": "hometown",
     "context": "邓伟谋(双峰人)与佘威(双峰人)同乡", "overlap_org": "双峰县", "overlap_period": ""},
    # 人大/政协
    {"person_a": 1, "person_b": 30, "type": "colleague",
     "context": "段晓赛(书记)与梁育清(人大主任)共事", "overlap_org": "涟源市", "overlap_period": "2025-"},
    {"person_a": 1, "person_b": 31, "type": "colleague",
     "context": "段晓赛(书记)与周惠军(政协主席)共事", "overlap_org": "涟源市", "overlap_period": "2025-"},
]


# ── Person JSON writer ───────────────────────────────────────────────────────
def write_person_json(person: dict) -> None:
    pid = person["id"]
    name = person["name"]
    slug_id = f"lianyuan_{name}"

    career_timeline = []
    for pos in positions:
        if pos["person_id"] != pid:
            continue
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
            "source_ids": ["S001"],
        })

    if len(career_timeline) <= 1:
        career_timeline.append({
            "start": "unknown", "end": "unknown", "org": "履历缺口",
            "title": "", "notes": "公开资料不足, 完整历届/前职履历待查.",
            "confidence": "unverified", "source_ids": [],
        })

    rels_output = []
    for r in relationships:
        if r["person_a"] != pid and r["person_b"] != pid:
            continue
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rel_map = {
            "colleague": ("overlap", "strong"),
            "succession": ("predecessor_successor", "strong"),
            "cross_region": ("other", "medium"),
            "hometown": ("same_native_place", "weak"),
            "subordinate": ("superior_subordinate", "strong"),
        }
        rtype, strength = rel_map.get(r["type"], ("overlap", "medium"))
        rels_output.append({
            "person": other_name,
            "person_id": f"lianyuan_{other_name}",
            "relationship_type": rtype,
            "strength": strength,
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if r["type"] in ("colleague", "succession") else "plausible",
        })

    identity = {
        "person_id": slug_id,
        "name": name,
        "aliases": [],
        "gender": person.get("gender", ""),
        "ethnicity": person.get("ethnicity", ""),
        "birth": person.get("birth", ""),
        "birthplace": person.get("birthplace", ""),
        "native_place": person.get("birthplace", ""),
        "education": [{"institution": person.get("education", ""), "major": "",
                       "degree": person.get("education", ""), "study_type": "unknown", "source_ids": []}
                      ] if person.get("education") else [],
        "party_join": person.get("party_join", ""),
        "work_start": person.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{name}_{person.get('birth','')}",
            "name_birthplace": f"{name}_{person.get('birthplace','')}",
            "official_profile_url": person.get("source", ""),
        },
    }

    current_status = {
        "current_post": person.get("current_post", ""),
        "current_org": person.get("current_org", ""),
        "administrative_rank": next(
            (p["rank"] for p in positions
             if p["person_id"] == pid and (p.get("title", "").find("书记") >= 0 or p["person_id"] == pid and p.get("rank"))),
            ""),
        "as_of": AS_OF,
        "is_current_confirmed": person.get("confidence") == "confirmed",
    }

    open_questions = []
    if not person.get("work_start") or not person.get("party_join"):
        open_questions.append({
            "priority": "high",
            "question": f"{name} 入党时间/参加工作时间及完整前期履历(出生/入党/工作起点/各职历)",
            "why_it_matters": "官方领导之窗仅一行简历, 未发布完整履历; 精确时间线对关系网络分析关键",
            "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 涟源 履历"],
            "last_attempted": AS_OF,
        })

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖南省", "city": "娄底市", "region": "涟源市",
            "job": person.get("current_post", ""),
            "task_id": "hunan_涟源市", "time_focus": "2026-05 至 2026-08",
        },
        "identity": identity,
        "current_status": current_status,
        "career_timeline": career_timeline,
        "organizations": [
            {"name": o["name"], "type": o["type"], "level": o["level"], "location": o["location"]}
            for o in organizations
            if o["id"] in {p["org_id"] for p in positions if p["person_id"] == pid}
        ],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": (
                "cross_county_rotation" if pid == 1 else
                "local_ladder" if pid == 2 else "local_ladder"),
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
        "source_register": [
            {"id": "S001", "title": person.get("source", ""), "url": person.get("source", ""),
             "publisher": "涟源市人民政府 领导之窗 / 项目数据", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S002", "title": SRC_LIST_SW, "url": SRC_LIST_SW,
             "publisher": "涟源市人民政府 市政府领导之窗", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "市政府领导名单"},
        ],
        "confidence_summary": {
            "identity": person.get("confidence", "unverified"),
            "current_role": "confirmed",
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历(前职/具体日期)" if person.get("birth") else "身份细节",
        },
        "open_questions": open_questions,
    }

    job = person.get("current_post", "").split("、")[0].replace("提名人选", "").replace("（挂职）", "")
    if person["id"] in (1, 2):
        job = "市委书记" if person["id"] == 1 else "市长"
    fname = STAGING / f"{TODAY}-湖南省-娄底市-{job}-{name}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"    wrote {fname.name}")


# ── Build ────────────────────────────────────────────────────────────────────
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
    core_ids = {1, 2, 50}  # 书记/代市长/前任市长
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())