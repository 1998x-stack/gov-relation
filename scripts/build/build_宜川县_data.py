#!/usr/bin/env python3
"""Build 宜川县 leadership network — SQLite DB + GEXF graph."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, TMP_DIR

# ── Output paths (staging for validation, then promoted) ─────────────────────
_STAGING = TMP_DIR / "shaanxi_宜川县"
DB_PATH = _STAGING / "宜川县_network.db"
GEXF_PATH = _STAGING / "宜川县_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
PERSONS = [
    # ── Top leaders ──
    {
        "id": 1,
        "name": "高勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共宜川县委员会",
        "source": "https://www.ycx.gov.cn/xwzx/bdyw/2075381599494684673.html | 刘小军→左怀理(2014-2022)→高勇(2022底至今)",
    },
    {
        "id": 2,
        "name": "李岗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-04",
        "birthplace": "陕西延长",
        "education": "在职研究生学历，哲学硕士",
        "party_join": "2000-06",
        "work_start": "1997-07",
        "current_post": "县委副书记、县长",
        "current_org": "宜川县人民政府",
        "source": "https://www.ycx.gov.cn/zfxxgk/fdzdgknr/ldzc/xc/lg/1.html",
    },
    # ── Party Standing Committee Members ──
    {
        "id": 3,
        "name": "惠藏锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记（专职）",
        "current_org": "中共宜川县委员会",
        "source": "https://www.ycx.gov.cn/xwzx/bdyw/2075381599494684673.html",
    },
    {
        "id": 4,
        "name": "魏建文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-09",
        "birthplace": "陕西甘泉",
        "education": "在职研究生学历，文学硕士",
        "party_join": "1999-06",
        "work_start": "2003-07",
        "current_post": "县委常委、常务副县长",
        "current_org": "宜川县人民政府",
        "source": "https://www.ycx.gov.cn/zfxxgk/fdzdgknr/ldzc/cwfxc/wjw/1.html",
    },
    {
        "id": 5,
        "name": "杨彦辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共宜川县委员会",
        "source": "https://www.ycx.gov.cn/xwzx/bdyw/2075381599494684673.html",
    },
    {
        "id": 6,
        "name": "王小斗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共宜川县纪律检查委员会",
        "source": "https://www.ycx.gov.cn/ 宜川县纪委全会报道 (2024-2026)",
    },
    {
        "id": 7,
        "name": "李晓妮",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970-10",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "宜川县人民政府",
        "source": "https://www.ycx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/lxn/1.html",
    },
    # ── Deputy County Mayors ──
    {
        "id": 8,
        "name": "禹罡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-01",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宜川县人民政府",
        "source": "https://www.ycx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/yg/1.html",
    },
    {
        "id": 9,
        "name": "朱学文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-01",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宜川县人民政府",
        "source": "https://www.ycx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/zxw/1.html",
    },
    {
        "id": 10,
        "name": "李峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-04",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宜川县人民政府",
        "source": "https://www.ycx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/lf/1.html",
    },
    {
        "id": 11,
        "name": "张延成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "本科",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "宜川县人民政府",
        "source": "https://www.ycx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/zyc/1.html",
    },
    # ── Hukou Management Area ──
    {
        "id": 12,
        "name": "阮杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "宜川县人民政府",
        "source": "https://www.ycx.gov.cn/xwzx/bdyw/2075381599494684673.html | 苏陕协作无锡新吴区挂职干部",
    },
    # ── Predecessors ──
    {
        "id": 13,
        "name": "左怀理",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-03",
        "birthplace": "陕西甘泉",
        "education": "在职研究生学历",
        "party_join": "1986-12",
        "work_start": "1983-07",
        "current_post": "陕西省水利厅一级巡视员",
        "current_org": "陕西省水利厅",
        "source": "https://www.ycx.gov.cn/ (前任县委书记) | 陕西省水利厅官网",
    },
    {
        "id": 14,
        "name": "薛延飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-",
        "birthplace": "陕西米脂",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "洛川县人民政府",
        "source": "https://www.ycx.gov.cn/xwzx/bdyw/ (前任宜川县长) | 洛川县政府网",
    },
    {
        "id": 15,
        "name": "任建新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "历史资料 (前任宜川县长约2016-2021)",
    },
    {
        "id": 16,
        "name": "姚靖江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "陕西绥德",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "历史资料 (宜川县委书记约2007-2011，后升延安市委常委、秘书长)",
    },
    {
        "id": 17,
        "name": "冯继红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "历史资料 (宜川县委书记约2004-2007，后任延安市副市长、市人大主任)",
    },
    # ── Legislature & Consultative ──
    {
        "id": 18,
        "name": "程小卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "宜川县人大常委会",
        "source": "https://www.ycx.gov.cn/xwzx/bdyw/2039149857819615233.html",
    },
    {
        "id": 19,
        "name": "陈志胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协宜川县委员会",
        "source": "https://www.ycx.gov.cn/xwzx/bdyw/2039149857819615233.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中共宜川县委员会", "type": "党委", "level": "县级", "parent": "中共延安市委员会", "location": "宜川县"},
    {"id": 2, "name": "宜川县人民政府", "type": "政府", "level": "县级", "parent": "延安市人民政府", "location": "宜川县"},
    {"id": 3, "name": "中共宜川县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共宜川县委员会", "location": "宜川县"},
    {"id": 4, "name": "中共宜川县委组织部", "type": "党委", "level": "县级", "parent": "中共宜川县委员会", "location": "宜川县"},
    {"id": 5, "name": "宜川县公安局", "type": "政府", "level": "县级", "parent": "宜川县人民政府", "location": "宜川县"},
    {"id": 6, "name": "宜川县人大常委会", "type": "人大", "level": "县级", "parent": "延安市人大常委会", "location": "宜川县"},
    {"id": 7, "name": "政协宜川县委员会", "type": "政协", "level": "县级", "parent": "政协延安市委员会", "location": "宜川县"},
    {"id": 8, "name": "陕西省水利厅", "type": "政府", "level": "省级", "parent": "陕西省人民政府", "location": "西安市"},
    {"id": 9, "name": "洛川县人民政府", "type": "政府", "level": "县级", "parent": "延安市人民政府", "location": "洛川县"},
    {"id": 10, "name": "延安市人民政府", "type": "政府", "level": "地市级", "parent": "陕西省人民政府", "location": "延安市"},
    {"id": 11, "name": "中共延安市委组织部", "type": "党委", "level": "地市级", "parent": "中共延安市委员会", "location": "延安市"},
    {"id": 12, "name": "中共延安市委员会", "type": "党委", "level": "地市级", "parent": "中共陕西省委员会", "location": "延安市"},
    {"id": 13, "name": "延安市卫生健康委员会", "type": "政府", "level": "地市级", "parent": "延安市人民政府", "location": "延安市"},
    {"id": 14, "name": "志丹县人民政府", "type": "政府", "level": "县级", "parent": "延安市人民政府", "location": "志丹县"},
    {"id": 15, "name": "甘泉县人民政府", "type": "政府", "level": "县级", "parent": "延安市人民政府", "location": "甘泉县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
POSITIONS = [
    # 高勇 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "约2022年底", "end_date": "", "rank": "正处级", "note": "接替左怀理"},
    # 李岗 — 县长
    {"person_id": 2, "org_id": 11, "title": "市委组织部副科长", "start_date": "", "end_date": "", "rank": "副科级", "note": "延安市委组织部成长"},
    {"person_id": 2, "org_id": 11, "title": "市委组织部科长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "约2025年底", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start_date": "约2025年底/2026年初", "end_date": "", "rank": "正处级", "note": "现任"},
    # 惠藏锋 — 专职副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记（专职）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 魏建文 — 常务副县长
    {"person_id": 4, "org_id": 11, "title": "市委组织部副主任科员", "start_date": "", "end_date": "", "rank": "副科级", "note": ""},
    {"person_id": 4, "org_id": 11, "title": "市委组织部副科长", "start_date": "", "end_date": "", "rank": "副科级", "note": ""},
    {"person_id": 4, "org_id": 11, "title": "市委组织部正科级组织员", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 4, "org_id": 11, "title": "市委组织部科长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "约2026年初", "rank": "副处级", "note": "前任组织部长"},
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "2026年初", "end_date": "", "rank": "副处级", "note": "现任"},
    # 杨彦辉 — 组织部长
    {"person_id": 5, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "约2026年", "end_date": "", "rank": "副处级", "note": "接替魏建文"},
    # 王小斗 — 纪委书记
    {"person_id": 6, "org_id": 1, "title": "县委常委、纪委书记", "start_date": "至少2024年", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "县监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 李晓妮 — 常委副县长
    {"person_id": 7, "org_id": 15, "title": "乡镇副镇长", "start_date": "", "end_date": "", "rank": "", "note": "早期乡镇经历"},
    {"person_id": 7, "org_id": 15, "title": "民政局副局长", "start_date": "", "end_date": "", "rank": "", "note": "甘泉县"},
    {"person_id": 7, "org_id": 15, "title": "乡镇镇长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 13, "title": "市计生局/卫健委副局长、副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "现任"},
    # 禹罡 — 副县长
    {"person_id": 8, "org_id": 10, "title": "市产业调查队科员", "start_date": "", "end_date": "", "rank": "", "note": "延安市统计局系统成长"},
    {"person_id": 8, "org_id": 10, "title": "市统计局副科长、科长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "现任"},
    # 朱学文 — 副县长
    {"person_id": 9, "org_id": 2, "title": "乡镇长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "乡镇党委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "现任"},
    # 李峰 — 副县长
    {"person_id": 10, "org_id": 2, "title": "乡镇人大主席", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "乡镇长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "乡镇党委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "现任"},
    # 张延成 — 副县长/公安局长
    {"person_id": 11, "org_id": 14, "title": "志丹县副县长、公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 5, "title": "宜川县副县长、公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "现任"},
    # 阮杰 — 挂职副县长
    {"person_id": 12, "org_id": 2, "title": "县委常委、副县长（挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "无锡新吴区挂职干部"},
    # 左怀理 — 前任县委书记
    {"person_id": 13, "org_id": 15, "title": "甘泉县农业局/县委办/团委/乡党委书记", "start_date": "", "end_date": "", "rank": "", "note": "早期甘泉县经历"},
    {"person_id": 13, "org_id": 1, "title": "甘泉县委常委、办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "甘泉县"},
    {"person_id": 13, "org_id": 2, "title": "黄龙县副县长/常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "黄龙县"},
    {"person_id": 13, "org_id": 1, "title": "延川县委副书记", "start_date": "", "end_date": "2012", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "宜川县委副书记、县长", "start_date": "2012", "end_date": "2014", "rank": "正处级", "note": "左怀理任宜川县长"},
    {"person_id": 13, "org_id": 1, "title": "宜川县委书记", "start_date": "2014", "end_date": "2022", "rank": "正处级", "note": "左怀理任宜川县委书记"},
    {"person_id": 13, "org_id": 8, "title": "陕西省水利建设工程中心党委书记", "start_date": "2023", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 8, "title": "陕西省水利厅一级巡视员、新闻发言人", "start_date": "", "end_date": "", "rank": "副厅级", "note": "当前职务"},
    # 薛延飞 — 前任县长
    {"person_id": 14, "org_id": 2, "title": "宜川县委常委、常务副县长", "start_date": "", "end_date": "约2021", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "宜川县委副书记、县长", "start_date": "约2021", "end_date": "2025底", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 9, "title": "洛川县委副书记、县长", "start_date": "2025", "end_date": "", "rank": "正处级", "note": "现任"},
    # 程小卫 — 人大主任
    {"person_id": 18, "org_id": 6, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 陈志胜 — 政协主席
    {"person_id": 19, "org_id": 7, "title": "县政协主席", "start_date": "2025-10", "end_date": "", "rank": "正处级", "note": "2025年10月当选"},
]

# ── Relationships ────────────────────────────────────────────────────────────
RELATIONSHIPS = [
    # 高勇 ↔ 李岗 — 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长党政正职搭档", "overlap_org": "中共宜川县委员会/宜川县人民政府", "overlap_period": "2026-"},
    # 高勇 ↔ 惠藏锋 — 书记—副书记搭档
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记—专职副书记搭档", "overlap_org": "中共宜川县委员会", "overlap_period": ""},
    # 高勇 ↔ 魏建文 — 书记—常委
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "县委书记—常务副县长上下级", "overlap_org": "中共宜川县委员会", "overlap_period": ""},
    # 李岗 ↔ 魏建文 — 县长—常务副县长搭档
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "县长—常务副县长搭档", "overlap_org": "宜川县人民政府", "overlap_period": "2026-"},
    # 李岗 ↔ 薛延飞 — 前后任县长
    {"person_a": 2, "person_b": 14, "type": "前后任", "context": "薛延飞→李岗接任宜川县长", "overlap_org": "宜川县人民政府", "overlap_period": "2025底交接"},
    # 魏建文 ↔ 杨彦辉 — 前后任组织部长
    {"person_a": 4, "person_b": 5, "type": "前后任", "context": "魏建文→杨彦辉接任组织部长", "overlap_org": "中共宜川县委组织部", "overlap_period": "2026"},
    # 高勇 ↔ 左怀理 — 前后任县委书记
    {"person_a": 1, "person_b": 13, "type": "前后任", "context": "左怀理→高勇接任宜川县委书记", "overlap_org": "中共宜川县委员会", "overlap_period": "约2022底"},
    # 左怀理 ↔ 薛延飞 — 书记—县长搭档（前）
    {"person_a": 13, "person_b": 14, "type": "共事", "context": "左怀理任县委书记、薛延飞任县长时期搭档", "overlap_org": "中共宜川县委员会/宜川县人民政府", "overlap_period": "约2021-2022"},
    # 左怀理 → 陕西省水利厅 — 升迁路径
    {"person_a": 13, "person_b": 13, "type": "升迁", "context": "左怀理由宜川县委书记升任省水利厅副厅级", "overlap_org": "", "overlap_period": "2023"},
    # 李岗 — 延安市委组织部系统（与魏建文同出组织系统）
    {"person_a": 2, "person_b": 4, "type": "同系统", "context": "李岗与魏建文均有延安市委组织部工作经历", "overlap_org": "中共延安市委组织部", "overlap_period": ""},
    # 薛延飞 → 洛川县 — 跨县调动
    {"person_a": 14, "person_b": 14, "type": "跨县调动", "context": "薛延飞从宜川县长调任洛川县长", "overlap_org": "", "overlap_period": "2025"},
    # 张延成 ← 志丹县 — 跨县调动
    {"person_a": 11, "person_b": 11, "type": "跨县调动", "context": "张延成从志丹县公安局长调任宜川", "overlap_org": "", "overlap_period": ""},
    # 李晓妮 — 市卫健委经历
    {"person_a": 7, "person_b": 7, "type": "跨系统调动", "context": "李晓妮从县委统战部长→市卫健委→副县长", "overlap_org": "", "overlap_period": ""},
    # 姚靖江 ↔ 冯继红 — 前后任县委书记
    {"person_a": 16, "person_b": 17, "type": "前后任", "context": "冯继红→姚靖江接任宜川县委书记", "overlap_org": "中共宜川县委员会", "overlap_period": "约2007"},
    # 高勇 — 姚靖江、冯继红属于不同时期的县委书记（间接继承）
    {"person_a": 1, "person_b": 13, "type": "接班链", "context": "冯继红→姚靖江→刘小军→左怀理→高勇的县委书记传承链", "overlap_org": "中共宜川县委员会", "overlap_period": "2004-2026"},
]


# ── Main ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="宜川县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
