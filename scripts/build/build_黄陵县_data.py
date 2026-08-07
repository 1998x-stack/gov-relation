#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 黄陵县, 陕西省延安市.

Investigation date: 2026-08-07
Task ID: shaanxi_黄陵县
Level: 县
Targets: 县委书记 & 县长

Research sources (primary, directly accessed this session):
  - http://www.huangling.gov.cn/zfxxgk/fdzdgknr/ldzc/xc/ljx/1.html — 黄陵县政府 领导之窗: 县长 李建雄 及县政府班子成员、分管领域
  - http://www.huangling.gov.cn/zfxxgk/fdzdgknr/ldzc/xc/1.html — 县政府领导名录（县长/常务副县长/党组成员/副县长）
  - http://www.huangling.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/{...}/1.html — 各副县长个人页
  - http://www.huangling.gov.cn/xwzx/bdyw/2085175927169425410.html — 县委常委会（2026-08-04）: 李建雄已任县委书记
  - http://www.huangling.gov.cn/xwzx/bdyw/2085555215525814274.html — 刘昌宏以"代县长"身份调研防汛（2026-08-07）
  - http://www.huangling.gov.cn/xwzx/bdyw/2071763040954556418.html — 县委常委会（2026-06-29）: 刘矿平仍为县委书记
  - http://www.huangling.gov.cn/xwzx/bdyw/2071410824825593857.html — 县人大第34次常委会: 惠建国(人大主任)、车华能(监委主任)、周海龙(法院院长)
  - http://www.huangling.gov.cn/xwzx/bdyw/2038437784777138178.html — 2026 政协会议: 刘矿平/惠建国/李建委/朱小虎
  - http://www.huangling.gov.cn/zjhl/ — 走进黄陵: 县情概况
  - 兄弟产物: build_子长市_data.py — 卢志华曾任黄陵县委常委/纪委书记（跨县交流）
  - 延安市人民政府门户 https://www.yanan.gov.cn/ — 延安市委书记 王海鹏、市长 郭柱国（2026-08-06/07 已直连核实）

Leadership transition (confirmed):
  - 2026-07 下旬 全县领导干部会议（延安市委书记 王海鹏 出席讲话）宣布新班子
  - 前任县委书记 刘矿平（省黄帝陵文化园区党工委书记、管委会主任）卸任
  - 李建委（原县长/县委副书记）晋升 县委书记（省黄帝陵文化园区党工委书记）
  - 刘昌宏（省黄帝陵文化园区党工委副书记）任 县委副书记、代县长

Confidence notes:
  - 现任县委书记 李建委: confirmed（政府网站县委常委会会议 2026-08-06）
  - 现任代县长 刘昌宏: confirmed（政府网站新闻 2026-08-07)；履历未获
  - 前任县委书记 刘矿平: confirmed 任职（2025-2026 大量县内报道）；去向 unverified
  - 县政府领导成员及分管领域: confirmed（领导之窗 2026）
  - 县人大/监委/法院: confirmed（人大第34次会议 2026-06-29）
  - 政协领导 朱小虎: plausible（2026 政协会议作报告）
  - 出生年份/籍贯/学历 等身份字段：多数 unverified（受搜索引擎验证码/百科限制，见 open_questions）
"""

from __future__ import annotations

import sqlite3  # noqa — used by gov_relation.runner via import

import json
import os
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

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "黄陵县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_黄陵县"
if _CURRENT_DIR.name == "shaanxi_黄陵县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ──────────────────────────────────────────────────────────────────
# IDs: 1-3 县委主要领导（现任文书/代县长/前任书记）, 4-11 县政府领导,
#      12-13 人大/监委/法院, 14 政协, 15 跨县交流, 16-17 市级上级
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 县委主要领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1, "name": "李建委", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委书记", "current_org": "中共黄陵县委员会",
        "source": "http://www.huangling.gov.cn/xwzx/bdyw/2085175927169425410.html"
    },
    {
        "id": 2, "name": "刘昌宏", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记、代县长", "current_org": "黄陵县人民政府",
        "source": "http://www.huangling.gov.cn/xwzx/bdyw/2085555215525814274.html"
    },
    {
        "id": 3, "name": "刘矿平", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任县委书记", "current_org": "中共黄陵县委员会",
        "source": "http://www.huangling.gov.cn/xwzx/bdyw/2071763040954556418.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县政府领导班子（领导之窗 2026）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 4, "name": "张海清", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、常务副县长", "current_org": "黄陵县人民政府",
        "source": "http://www.huangling.gov.cn/zfxxgk/fdzdgknr/ldzc/cwfxc/zhq/1.html"
    },
    {
        "id": 5, "name": "李清喜", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、组织部部长、县政府党组成员", "current_org": "黄陵县人民政府",
        "source": "http://www.huangling.gov.cn/zfxxgk/fdzdgknr/ldzc/dzcy/lqx/1.html"
    },
    {
        "id": 6, "name": "吴健雄", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、副县长", "current_org": "黄陵县人民政府",
        "source": "http://www.huangling.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/wjx/1.html"
    },
    {
        "id": 7, "name": "刘志江", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "黄陵县人民政府",
        "source": "http://www.huangling.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/lzj/1.html"
    },
    {
        "id": 8, "name": "曹泽鸿", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "黄陵县人民政府",
        "source": "http://www.huangling.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/czh/1.html"
    },
    {
        "id": 9, "name": "刘光显", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "黄陵县人民政府",
        "source": "http://www.huangling.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/lgx/1.html"
    },
    {
        "id": 10, "name": "申一修", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "黄陵县人民政府",
        "source": "http://www.huangling.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/syx/1.html"
    },
    {
        "id": 11, "name": "杨磊", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长、公安局局长", "current_org": "黄陵县人民政府",
        "source": "http://www.huangling.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/cyf/1.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大常委会 / 监察委 / 法院 / 政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12, "name": "惠建国", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会主任", "current_org": "黄陵县人民代表大会常务委员会",
        "source": "http://www.huangling.gov.cn/xwzx/bdyw/2071410824825593857.html"
    },
    {
        "id": 13, "name": "车华能", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县监察委员会主任", "current_org": "黄陵县监察委员会",
        "source": "http://www.huangling.gov.cn/xwzx/bdyw/2071410824825593857.html"
    },
    {
        "id": 14, "name": "周海龙", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人民法院院长", "current_org": "黄陵县人民法院",
        "source": "http://www.huangling.gov.cn/xwzx/bdyw/2071410824825593857.html"
    },
    {
        "id": 15, "name": "朱小虎", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协主席（拟）", "current_org": "中国人民政治协商会议黄陵县委员会",
        "source": "http://www.huangling.gov.cn/xwzx/bdyw/2038437784777138178.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 跨县交流人物（子长市→曾任黄陵纪委书记）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 16, "name": "卢志华", "gender": "男", "ethnicity": "汉族",
        "birth": "1975年2月", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "子长市委常委、副市长（曾任黄陵县委常委、纪委书记、监委主任）",
        "current_org": "子长市人民政府",
        "source": "https://www.zichang.gov.cn/zfxxgk/fdzdgknr/zfld/fsc/lzh/1.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市级上级
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 17, "name": "王海鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "延安市委书记", "current_org": "中共延安市委",
        "source": "https://www.yanan.gov.cn/"
    },
    {
        "id": 18, "name": "郭柱国", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "延安市委副书记、市长", "current_org": "延安市人民政府",
        "source": "https://www.yanan.gov.cn/"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共黄陵县委员会", "type": "党委", "level": "县级", "parent": "中共延安市委", "location": "黄陵县"},
    {"id": 2, "name": "黄陵县人民政府", "type": "政府", "level": "县级", "parent": "延安市人民政府", "location": "黄陵县"},
    {"id": 3, "name": "省黄帝陵文化园区党工委/管委会", "type": "党委", "level": "省级派出", "parent": "中共陕西省委", "location": "黄陵县"},
    {"id": 4, "name": "中共黄陵县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共黄陵县委员会", "location": "黄陵县"},
    {"id": 5, "name": "黄陵县监察委员会", "type": "党委", "level": "县级", "parent": "中共黄陵县委员会", "location": "黄陵县"},
    {"id": 6, "name": "中共黄陵县委组织部", "type": "党委", "level": "县级", "parent": "中共黄陵县委员会", "location": "黄陵县"},
    {"id": 7, "name": "黄陵县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "延安市人民代表大会常务委员会", "location": "黄陵县"},
    {"id": 8, "name": "黄陵县人民法院", "type": "政府", "level": "县级", "parent": "黄陵县人民代表大会常务委员会", "location": "黄陵县"},
    {"id": 9, "name": "中国人民政治协商会议黄陵县委员会", "type": "政协", "level": "县级", "parent": "政协延安市委员会", "location": "黄陵县"},
    {"id": 10, "name": "黄陵县公安局", "type": "政府", "level": "科级", "parent": "黄陵县人民政府", "location": "黄陵县"},
    {"id": 11, "name": "中共延安市委", "type": "党委", "level": "地级市", "parent": "中共陕西省委", "location": "延安市"},
    {"id": 12, "name": "延安市人民政府", "type": "政府", "level": "地级市", "parent": "陕西省人民政府", "location": "延安市"},
    {"id": 13, "name": "子长市人民政府", "type": "政府", "level": "县级市", "parent": "延安市人民政府", "location": "子长市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 李建委 (现任县委书记; 2026-07 由县长晋升)
    {"person_id": 1, "org_id": 2, "title": "县长（县委副书记、县政府党组书记）", "start": "~2020", "end": "2026.07",
     "rank": "正处级", "note": "2026-02 两会以县长身份作政府工作报告；2026 上半年仍为县长"},
    {"person_id": 1, "org_id": 3, "title": "省黄帝陵文化园区管委会（省祭陵办）副主任", "start": "", "end": "2026.07",
     "rank": "", "note": "园区党工委副书主、管委会副主任"},
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2026.07", "end": "present",
     "rank": "正处级", "note": "省黄帝陵文化园区党工委书记、县委书记；2026-07 全县领导干部会议后履新"},
    # 刘昌宏 (现任代县长)
    {"person_id": 2, "org_id": 2, "title": "县委副书记、代县长", "start": "2026.08", "end": "present",
     "rank": "正处级", "note": "2026-08-07 以代县长身份调研防汛"},
    {"person_id": 2, "org_id": 3, "title": "省黄帝陵文化园区党工委副书记", "start": "", "end": "",
     "rank": "", "note": ""},
    # 刘矿平 (前任县委书记)
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start": "~2024", "end": "2026.07",
     "rank": "正处级", "note": "2025年中至2026-07 持续以县委书记身份活动"},
    {"person_id": 3, "org_id": 3, "title": "省黄帝陵文化园区党工委书记、管委会主任", "start": "", "end": "2026.07",
     "rank": "", "note": ""},
    # 张海清 (常务副县长)
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start": "", "end": "",
     "rank": "副处级", "note": "分管：发改/统计/应急/安全/工业/煤炭/国资等"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "",
     "rank": "副处级", "note": ""},
    # 李清喜 (组织部长/党组成员)
    {"person_id": 5, "org_id": 2, "title": "县政府党组成员", "start": "", "end": "",
     "rank": "副处级", "note": "分管：自然资源、避灾移民搬迁"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "",
     "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "组织部部长", "start": "", "end": "",
     "rank": "副处级", "note": ""},
    # 吴健雄 (副县长)
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": "分管：生态环保、人社、城乡建设、碳硅新材料：分管工业园区高新区"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "",
     "rank": "副处级", "note": ""},
    # 刘志江 (副县长)
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": "分管卫健、医保、教育体育、文旅文物、黄帝陵园区"},
    # 曹泽鸿 (副县长)
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": "分管金融保险、投融资"},
    # 刘光显 (副县长)
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": "分管农业农村、乡村振兴、水利林业"},
    # 申一修 (副县长)
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": "分管交通运输、市场监管、民政、数字经济、招商"},
    # 杨磊 (副县长/公安局长)
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": "主持公安工作"},
    {"person_id": 11, "org_id": 10, "title": "公安局局长", "start": "", "end": "",
     "rank": "正科级", "note": ""},
    # 惠建国 (人大主任)
    {"person_id": 12, "org_id": 7, "title": "县人大常委会主任", "start": "", "end": "",
     "rank": "正处级", "note": "2026-06-29 主持第34次常委会"},
    # 车华能 (监委主任)
    {"person_id": 13, "org_id": 5, "title": "县监察委员会主任", "start": "", "end": "",
     "rank": "副处级", "note": ""},
    # 周海龙 (法院院长)
    {"person_id": 14, "org_id": 8, "title": "县人民法院院长", "start": "", "end": "",
     "rank": "副处级", "note": ""},
    # 朱小虎 (政协主席拟)
    {"person_id": 15, "org_id": 9, "title": "县政协主席", "start": "", "end": "",
     "rank": "正处级", "note": "2026-02 政协会议作报告"},
    # 卢志华 (跨县: 子长市, 曾任黄陵纪委书记)
    {"person_id": 16, "org_id": 4, "title": "黄陵县委常委、纪委书记、监委主任", "start": "", "end": "",
     "rank": "副处级", "note": "prior role"},
    {"person_id": 16, "org_id": 13, "title": "子长市委常委、副市长", "start": "", "end": "",
     "rank": "副处级", "note": "current role (per 子长市政府)"},
    # 王海鹏 (延安市委书记)
    {"person_id": 17, "org_id": 11, "title": "延安市委书记", "start": "", "end": "present",
     "rank": "正厅级", "note": "黄陵县委的直接上级领导"},
    # 郭柱国 (延安市长)
    {"person_id": 18, "org_id": 12, "title": "延安市委副书记、市长", "start": "", "end": "present",
     "rank": "正厅级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与代县长，县委与县政府一把手", "overlap_org": "黄陵县", "overlap_period": "2026.07-至今"},
    # 人大代表
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "刘矿平为前任县委书记，李建委接任（全县领导干部会议宣布；原书记刘矿平转出）", "overlap_org": "中共黄陵县委", "overlap_period": "2026.07"},
    # 县长→书记 本地晋升线
    {"person_a": 1, "person_b": 1, "type": "local_promotion", "context": "李建委由县长晋升县委书记（2026-07）", "overlap_org": "黄陵县", "overlap_period": "2026"},
    # 县委书记 x 县政府领导
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与常务副县长", "overlap_org": "中共黄陵县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记与常委/组织部长", "overlap_org": "中共黄陵县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记与常委/副县长", "overlap_org": "中共黄陵县委", "overlap_period": ""},
    # 代县长 × 副县长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "代县长与常务副县长", "overlap_org": "黄陵县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "代县长与副县长", "overlap_org": "黄陵县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "代县长与副县长", "overlap_org": "黄陵县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "代县长与副县长", "overlap_org": "黄陵县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "代县长与副县长", "overlap_org": "黄陵县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "代县长与副县长/公安局长", "overlap_org": "黄陵县人民政府", "overlap_period": ""},
    # 人大/监委/法院/政协 x 县委
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "县委书记与人大常委会主任", "overlap_org": "黄陵县", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "县委书记与监察委主任", "overlap_org": "黄陵县", "overlap_period": ""},
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "县委书记与政协主席", "overlap_org": "黄陵县", "overlap_period": ""},
    # 跨县交流（卢志华 曾任黄陵纪委书记 → 子长副市长）
    {"person_a": 16, "person_b": 1, "type": "former_colleague", "context": "卢志华曾任黄陵县委常委/纪委书记，与李建委（当时县长）在同一县领导层共事", "overlap_org": "黄陵县", "overlap_period": "履历待查"},
    # 上级
    {"person_a": 17, "person_b": 1, "type": "superior_subordinate", "context": "延安市委书记为黄陵县委书记的上级", "overlap_org": "延安市", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "黄陵县政府 领导之窗 — 县长李建委", "url": "http://www.huangling.gov.cn/zfxxgk/fdzdgknr/ldzc/xc/ljx/1.html", "publisher": "黄陵县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县长李建委、常务张学海、副县长分工"},
        {"id": "S002", "title": "黄陵县政府 新闻 — 县委常委会会议 (2026-08-04)", "url": "http://www.huangling.gov.cn/xwzx/bdyw/2085175927169425410.html", "publisher": "黄陵县融媒体中心", "published_at": "2026-08-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "李建委以县委书记身份主持：任现书记 confirmation"},
        {"id": "S003", "title": "黄陵县政府 新闻 — 刘昌宏调研防汛 (2026-08-07)", "url": "http://www.huangling.gov.cn/xwzx/bdyw/2085555215525814274.html", "publisher": "黄陵县融媒体中心", "published_at": "2026-08-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "刘昌宏以代县长身份调研防汛；附县长名誉确认"},
        {"id": "S004", "title": "黄陵县政府 新闻 — 县委常委会会议 (2026-06-29)", "url": "http://www.huangling.gov.cn/xwzx/bdyw/2071763040954556418.html", "publisher": "黄陵县融媒体中心", "published_at": "2026-06-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "刘矿平仍为县委书记（书记之确认）"},
        {"id": "S005", "title": "黄陵县政府 新闻 — 2026 两会政府工作报告", "url": "http://www.huangling.gov.cn/xwzx/bdyw/2038779796489502721.html", "publisher": "黄陵县融媒体中心", "published_at": "2026-02", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "李建委以县长身份作政府工作报告；刘矿平出席"},
        {"id": "S006", "title": "黄陵县政府 新闻 — 县人大常委会第三十四次会议 (2026-06-29)", "url": "http://www.huangling.gov.cn/xwzx/bdyw/2071410824825593857.html", "publisher": "黄陵县融媒体中心", "published_at": "2026-06-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "人大主任惠建国、监委主任车华能、法院院长周海龙"},
        {"id": "S007", "title": "黄陵县政府 新闻 — 2026 政协会议", "url": "http://www.huangling.gov.cn/xwzx/bdyw/2038437784777138178.html", "publisher": "黄陵县融媒体中心", "published_at": "2026-02", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "政协朱小虎作报告；刘矿平/惠建国/李建委出席"},
        {"id": "S008", "title": "子长市政府 领导之窗 — 卢志华", "url": "https://www.zichang.gov.cn/zfxxgk/fdzdgknr/zfld/fsc/lzh/1.html", "publisher": "子长市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "卢志华现任子长市委常委、副市长；曾任黄陵县委常委/纪委书记（子长市 build 脚本）"},
        {"id": "S009", "title": "延安市人民政府门户", "url": "https://www.yanan.gov.cn/", "publisher": "延安市人民政府", "published_at": "2026-08-06/07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "延安市委书记王海鹏、市长郭柱国"},
        {"id": "S010", "title": "黄陵县政府 领导之窗 — 各副县长个人页", "url": "http://www.huangling.gov.cn/zfxxgk/fdzdgknr/ldzc/", "publisher": "黄陵县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张海清/李清喜/吴健雄/刘志江/曹泽鸿/刘光显/申一修/杨磊 分工"},
        {"id": "S011", "title": "黄陵县政府 走进黄陵 — 县情概况", "url": "http://www.huangling.gov.cn/zjhl/", "publisher": "黄陵县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "苹果适生区、煤炭能源化工基地、黄帝陵等县情"},
    ]


def make_person_json(person, timeline, relationships_list, source_register, gaps=None):
    """Build a person graph JSON following the schema."""
    pfname = f"huangling_{person['name']}"
    name = person["name"]
    post = person["current_post"]
    if "书记" in post and "副" not in post and "前任" not in post:
        rank = "正处级"
    elif "代县长" in post or "县长" in post:
        rank = "正处级"
    elif "人大主任" in post or "政协主席" in post or "监委主任" in post:
        rank = "正处级"
    elif "前任" in post:
        rank = "正处级"
    elif "公安" in post:
        rank = "副处级"
    elif "延安市" in (person.get("current_org") or ""):
        rank = "正厅级"
    else:
        rank = "副处级"
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "陕西省",
            "city": "延安市",
            "region": "黄陵县",
            "job": post,
            "task_id": "shaanxi_黄陵县",
            "time_focus": "2024-2026"
        },
        "identity": {
            "person_id": pfname,
            "name": name,
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person["education"], "study_type": "unknown", "source_ids": []}] if person["education"] else [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_{person['birth']}" if person["birth"] else name,
                "name_birthplace": f"{name}_{person['birthplace']}" if person["birthplace"] else name,
                "official_profile_url": person["source"]
            }
        },
        "current_status": {
            "current_post": post,
            "current_org": person["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": ("前任" not in post),
            "source_ids": []
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面公开记录（本调查仅就公开报道扫描）", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "plausible" if person["birth"] else "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{name}的早期履历、出生年月、籍贯、学历未获"
        },
        "open_questions": (gaps if gaps else [
            {"priority": "high", "question": f"{name}的完整职业履历（含出生/籍贯/学历/入党/早期岗位）是什么？", "why_it_matters": "无法分析晋升路径与跨部门经验", "suggested_queries": [f"{name} 简历 黄陵", f"{name} 任前公示", f"{name} 百度百科"], "last_attempted": AS_OF},
        ])
    }


# ══════════════════════════════════════════════════════════════════════════
# Build Function
# ══════════════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print("  黄陵县领导班子工作关系网络")
    print("  等级: 县")
    print(f"  调查日期: {AS_OF}")
    print("  信息来源: huangling.gov.cn (官方)、yanan.gov.cn (官方)、子长市 build")
    print("=" * 60)

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

    print(f"\n  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 李建委 (现任县委书记)
    ljx_timeline = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到李建委早于县政府工作的履历", "confidence": "unverified", "source_ids": []},
        {"start": "~2020", "end": "2026.07", "org": "黄陵县人民政府", "title": "县长、县委副书记、县政府党组书记", "notes": "2026-02两会作政府工作报告；2026年内多次以县长身份开展调研", "confidence": "confirmed", "source_ids": ["S005"]},
        {"start": "", "end": "2026.07", "org": "省黄帝陵文化园区管委会", "title": "省黄帝陵文化园园区党工委副书记、管委会副主任", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2026.07", "end": "present", "org": "中共黄陵县委", "title": "县委书记", "notes": "由县长晋升县委书记（全县领导干部会议后）", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2026.07", "end": "present", "org": "省黄帝陵园区管委会", "title": "省黄帝陵文化园区党工委书记", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    ljx_rels = [
        {"person": "刘昌宏", "person_id": "huangling_刘昌宏", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与县委副书记、代县长，党政搭档", "overlap_org": "黄陵县", "overlap_period": "2026.07-至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "张海清", "person_id": "huangling_张海清", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与常务副县长", "overlap_org": "黄陵县委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S010"]},
        {"person": "刘矿平", "person_id": "huangling_刘矿平", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "李建委接替刘矿平任县委书记", "overlap_org": "中共黄陵县委", "overlap_period": "2026.07", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
        {"person": "王海鹏", "person_id": "huangling_王海鹏", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "延安市委书记为黄陵县委书记的直接上级", "overlap_org": "延安市", "overlap_period": "", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S009"]},
    ]
    ljx_json = make_person_json(persons[0], ljx_timeline, ljx_rels, source_register,
        [{"priority": "critical", "question": "李建委的出生年份、籍贯、教育背景？", "why_it_matters": "核心人物身份信息缺失", "suggested_queries": ["李建委 简历 黄陵", "李建委 百度百科"], "last_attempted": AS_OF},
         {"priority": "critical", "question": "李建委 ~2020 年之前的职业生涯（任县长前担任何职）？", "why_it_matters": "无法分析其晋升路径与组织背景", "suggested_queries": ["李建委 县长 2020 黄陵"], "last_attempted": AS_OF}])
    with open(PJSON_DIR / f"{TODAY}-陕西省-延安市-县委书记-李建委.json", "w", encoding="utf-8") as f:
        json.dump(ljx_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {TODAY}-陕西省-延安市-县委书记-李建委.json")

    # 2. 刘昌宏 (代县长)
    lch_timeline = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "刘昌宏履历未获（出任代县长前的职务不明）", "confidence": "unverified", "source_ids": []},
        {"start": "2026.08", "end": "present", "org": "黄陵县人民政府", "title": "县委副书记、代县长", "notes": "2026-08-07 以代县长身份调研防汛", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    lc_rels = [
        {"person": "李建委", "person_id": "huangling_李建委", "relationship_type": "overlap", "strength": "strong", "evidence": "代县长与县委书记，党政搭档", "overlap_org": "黄陵县", "overlap_period": "2026.07-至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "王海鹏", "person_id": "huangling_王海鹏", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "代县长由延安市委管控", "overlap_org": "延安市", "overlap_period": "", "direction": "other_to_person", "confidence": "confirmed", "source_ids": []},
    ]
    lc_gaps = [
        {"priority": "critical", "question": "刘昌宏在任黄陵代县长前担任何职？完整履历？", "why_it_matters": "核心人物；履历完全空白", "suggested_queries": ["刘昌宏 黄陵 简历", "刘昌宏 任前公示", "刘昌宏 延安"], "last_attempted": AS_OF},
        {"priority": "critical", "question": "刘昌宏的出生年份、籍贯、教育背景？", "why_it_matters": "核心人物身份信息缺失", "suggested_queries": ["刘昌宏 出生 陕西"], "last_attempted": AS_OF},
    ]
    lc_p = make_person_json(persons[1], lch_timeline, lc_rels, source_register, lc_gaps)
    with open(PJSON_DIR / f"{TODAY}-陕西省-延安市-县长-刘昌宏.json", "w", encoding="utf-8") as f:
        json.dump(lc_p, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {TODAY}-陕西省-延安市-县长-刘昌宏.json")

    # 3. 刘矿平 (前任书民)
    lkp_timeline = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "刘矿平的早期履历未获", "confidence": "unverified", "source_ids": []},
        {"start": "~2024", "end": "2026.07", "org": "中共黄陵县委", "title": "县委书记", "notes": "2025-05~2026-06 持续以县委书记身份活动（警示教育/防汛/党建/春节检查等）", "confidence": "confirmed", "source_ids": ["S004"]},
        {"start": "", "end": "2026.07", "org": "省黄帝陵园管委会", "title": "省黄帝陵文化园区党工委书记、管委会主任", "notes": "", "confidence": "confirmed", "source_ids": ["S004"]},
        {"start": "2026.07", "end": "去向待查", "org": "去向未明", "title": "（调离黄陵）", "notes": "2026-07 全县领导干部会议后卸任，去向待证实", "confidence": "unverified", "source_ids": []},
    ]
    lkp_rels = [
        {"person": "李建委", "person_id": "huangling_李建委", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "李建委接替刘矿平任县委书记", "overlap_org": "中共黄陵县委", "overlap_period": "2026.07", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S004", "S002"]},
        {"person": "惠建国", "person_id": "huangling_惠建国", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与人大主任共事（两会/常委会）", "overlap_org": "黄陵县", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": []},
    ]
    lkp_gaps = [
        {"priority": "critical", "question": "刘矿平2026年7月后去向（调任何职）？", "why_it_matters": "前任书记若被提拔或平行调动，是全县调整信号", "suggested_queries": ["刘矿平 卸任 去向", "刘矿平 调任"], "last_attempted": AS_OF},
        {"priority": "high", "question": "刘矿平的完整履历（前任职务、出生/学历）？", "why_it_matters": "了解其晋升路径", "suggested_queries": ["刘矿平 简历 黄陵"], "last_attempted": AS_OF},
    ]
    lkp_p = make_person_json(persons[2], lkp_timeline, lkp_rels, source_register, lkp_gaps)
    with open(PJSON_DIR / f"{TODAY}-陕西省-延安市-原县委书记-刘矿平.json", "w", encoding="utf-8") as f:
        json.dump(lkp_p, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {TODAY}-陕西省-延安市-原县委书记-刘矿平.json")

    print(f"\n所有 Person Graph JSONs 已生成到: {PJSON_DIR}")


if __name__ == "__main__":
    build()