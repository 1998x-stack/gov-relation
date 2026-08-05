#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 黄平县 (Huangping County), 黔东南苗族侗族自治州, 贵州省.

Level: 县
Province: 贵州省
Parent city: 黔东南苗族侗族自治州
Targets: 县委书记 & 县长
Task ID: guizhou_黄平县
Investigation date: 2026-08-05

Research sources (primary: 黄平县人民政府门户 www.qdnhp.gov.cn):
  - 领导之窗: https://www.qdnhp.gov.cn/xxgk/zdxxgk/ldzc_5983168/
      + 万政/田奇/洪加朗/张雪宾/舒烈跃/刘锷/曾玲/张东海 profiles (birth, ethnicity, education, 分工)
  - 领导活动 (官方县委常委会报道): https://www.qdnhp.gov.cn/xwzx/ldhd/
      + 2026-07-29: "县委书记王思红主持会议" (t20260730_90675246.html) — 王思红=县委书记, 万政=县委副书记/县长,
        向国强=人大主任, 杨冰=政协主席, 蒲桂蓉=县委副书记
      + 2026-07-20: "县委书记王思红主持" (t20260721_90644962.html)
      + 2026-07-10: "州人大常委会副主任、县委书记肖高峰主持" (t20260713_90613418.html) — 前任书记肖高峰,
        曹振宇 县委副书记
  - 新闻 archive: 万政 (县长, 主持县政府党组会/常务会/调研); 杨满英 (前任县长, 此前主持县政府)
      + 杨满英 (县领导慰问/人大/政协); 张海洋 (副县) 等

Confidence notes:
  - 王思红 (县委书记): confirmed via 官方 07-20/07-29 县委常委会报道. 前任肖高峰截至 2026-07-10 仍在任
    ("州人大常委会副主任、县委书记"), 交接窗口为 2026-07-13 后、07-20 前. 王思红任书记前职务、出生年月、
    籍贯、教育背景未从一手来源取得（网络受限）—— open gap.
  - 万政 (县委副书记/县政府党组成员/县长): confirmed via 官方领导之窗 bio (男/苗族/1985-08/大学·工学学士/
    中共党员) + 县委常委会与会名单. 任县长前职务路径未取得 —— open gap.
  - 县政府班子 (田奇 常务/洪加朗/张雪宾/舒烈跃/刘锷/曾妮/张东海): confirmed via 官方领导之窗 (出生/学历/分工).
  - 前任县长杨满英: 新闻报道 (主持县政府常务会议) + 副职资料, 去向(州总工会) 未同时用手一源交叉 — open gap.
  - 肖高峰: 州人大常委会副主任、县委书记（2025-2026），卸任去向待查.
  - 四套班子: 向国强(人大主任)、杨冰(政协主席)、蒲桂蓉/曹振宇(县委副书记) 经 07 县委常委会出席名单确认.
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "黄平县"
TODAY = datetime.now().strftime("%Y%m%d")

# DB + GEXF written into the current directory (staging when run from data/tmp)
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ 县委主要领导（一把手／二把手）═══════
    {
        "id": 1,
        "name": "王思红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共黄平县委书记",
        "current_org": "中共黄平县委",
        "source": "https://www.qdnhp.gov.cn/xwzx/ldhd/202607/t20260730_90675246.html; https://www.qdnhp.gov.cn/xwzx/ldhd/202607/t20260721_90644962.html"
    },
    {
        "id": 2,
        "name": "万政",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1985年8月",
        "birthplace": "",
        "education": "大学学历、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共黄平县委副书记、县人民政府县长",
        "current_org": "黄平县人民政府",
        "source": "https://www.qdnhp.gov.cn/xxgk/zdxxgk/ldzc_5983168/202601/t20260109_89283691.html"
    },
    # ═══════ 县委副书记 ═══════
    {
        "id": 3,
        "name": "蒲桂蓉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共黄平县委副书记",
        "current_org": "中共黄平县委",
        "source": "https://www.qdnhp.gov.cn/xwzx/ldhd/202607/t20260730_90675246.html"
    },
    {
        "id": 4,
        "name": "曹振宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共黄平县委副书记",
        "current_org": "中共黄平县委",
        "source": "https://www.qdnhp.gov.cn/xwzx/ldhd/202607/t20260713_90613418.html"
    },
    # ═══════ 县政府领导（常务/副县长）═══════
    {
        "id": 5,
        "name": "田奇",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1985年9月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄平县委常委、县人民政府常务副县长",
        "current_org": "黄平县人民政府",
        "source": "https://www.qdnhp.gov.cn/xxgk/zdxxgk/ldzc_5983168/202507/t20250702_88222052.html"
    },
    {
        "id": 6,
        "name": "洪加朗",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1980年7月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄平县委常委、县人民政府副县长",
        "current_org": "黄平县人民政府",
        "source": "https://www.qdnhp.gov.cn/xxgk/zdxxgk/ldzc_5983168/202505/t20250508_87681679.html"
    },
    {
        "id": 7,
        "name": "张雪宾",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄平县人民政府党组成员、副县长",
        "current_org": "黄平县人民政府",
        "source": "https://www.qdnhp.gov.cn/xxgk/zdxxgk/ldzc_5983168/202505/t20250508_87681678.html"
    },
    {
        "id": 8,
        "name": "舒烈跃",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1975年10月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄平县人民政府党组成员、副县长、县公安局党委书记、局长",
        "current_org": "黄平县公安局",
        "source": "https://www.qdnhp.gov.cn/xxgk/zdxxgk/ldzc_5983168/202505/t20250508_87681646.html"
    },
    {
        "id": 9,
        "name": "刘锷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年10月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄平县人民政府党组成员、副县长",
        "current_org": "黄平县人民政府",
        "source": "https://www.qdnhp.gov.cn/xxgk/zdxxgk/ldzc_5983168/202512/t20251208_89024595.html"
    },
    {
        "id": 10,
        "name": "曾玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年3月",
        "birthplace": "",
        "education": "大学文学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄平县人民政府党组成员、副县长、新州镇党委书记",
        "current_org": "黄平县人民政府",
        "source": "https://www.qdnhp.gov.cn/xxgk/zdxxgk/ldzc_5983168/202607/t20260731_90684198.html"
    },
    {
        "id": 11,
        "name": "张东海",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1990年6月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄平县人民政府党组成员、副县长",
        "current_org": "黄平县人民政府",
        "source": "https://www.qdnhp.gov.cn/xxgk/zdxxgk/ldzc_5983168/202607/t20260731_90684205.html"
    },
    # ═══════ 县人大 / 政协 ═══════
    {
        "id": 12,
        "name": "向国强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄平县人大常委会主任",
        "current_org": "黄平县人大常委会",
        "source": "https://www.qdnhp.gov.cn/xwzx/ldhd/202607/t20260730_90675246.html"
    },
    {
        "id": 13,
        "name": "杨冰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政协黄平县委员会主席",
        "current_org": "政协黄平县委员会",
        "source": "https://www.qdnhp.gov.cn/xwzx/ldhd/202607/t20260730_90675246.html"
    },
    # ═══════ 前任书记 ═══════
    {
        "id": 14,
        "name": "肖高峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任黄平县委书记（州人大常委会副主任兼；2026-07 前卸任，去向待查）",
        "current_org": "中共黄平县委",
        "source": "https://www.qdnhp.gov.cn/xwzx/ldhd/202607/t20260713_90613418.html"
    },
    # ═══════ 前任县长 ═══════
    {
        "id": 15,
        "name": "杨满英",
        "gender": "女",
        "ethnicity": "侗族",
        "birth": "1977年1月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任黄平县长（2026 年前在任；去向待查）",
        "current_org": "黄平县人民政府",
        "source": "https://www.qdnhp.gov.cn/xwzx/ldhd/"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共黄平县委", "type": "党委", "level": "县级", "parent": "中共黔东南州委", "location": "黔东南州黄平县"},
    {"id": 2, "name": "黄平县人民政府", "type": "政府", "level": "县级", "parent": "黔东南州人民政府", "location": "黔东南州黄平县"},
    {"id": 3, "name": "黄平县公安局", "type": "政府", "level": "县级", "parent": "黄平县人民政府", "location": "黔东南州黄平县"},
    {"id": 4, "name": "黄平县人大常委会", "type": "人大", "level": "县级", "parent": "黔东南州人大常委会", "location": "黔东南州黄平县"},
    {"id": 5, "name": "政协黄平县委员会", "type": "政协", "level": "县级", "parent": "政协黔东南州委员会", "location": "黔东南州黄平县"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 王思红 — 县委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共黄平县委书记", "start": "2026-07(约)", "end": "present", "rank": "正处级",
     "note": "主持县委全面工作。经官方 2026-07-20、07-29 县委常委会报道确认在任。前任书记肖高峰 2026-07-10 仍在任，交接窗口为 2026-07-13 后、07-20 前。"},
    # 万政 — 县长
    {"id": 2, "person_id": 2, "org_id": 1, "title": "中共黄平县委副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "兼任县委副书记。2026-07 县委常委会出席名单在列。"},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "黄平县人民政府县长", "start": "", "end": "present", "rank": "正处级",
     "note": "主持县人民政府全面工作，负责财政、审计、粮食方面工作；分管县财政局、县审计局。多次以县长身份调研、出席县委常委会。"},
    # 县委副书记
    {"id": 4, "person_id": 3, "org_id": 1, "title": "黄平县委副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "协助县委书记抓党的建设等工作。2026-07-29 县委常委会出席名单在列。"},
    {"id": 5, "person_id": 4, "org_id": 1, "title": "黄平县委副书记", "start": "", "end": "", "rank": "副处级",
     "note": "2026-07-10（肖高峰主持）县委常委会出席名单在列；是否仍在任待查。"},
    # 县政府领导
    {"id": 6, "person_id": 5, "org_id": 2, "title": "黄平县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责县政府常务工作；县委常委会成员。负责财政、发改、金融、应急等工作（主管领域见官方领导之窗分工）。"},
    {"id": 7, "person_id": 6, "org_id": 2, "title": "黄平县委常委、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责农业、水务、林业、乡村振兴、易地搬迁、脱贫成果巩固等（官方领导之窗分工）。"},
    {"id": 8, "person_id": 6, "org_id": 1, "title": "黄平县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": "县委常委会成员。"},
    {"id": 9, "person_id": 7, "org_id": 2, "title": "黄平县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责民政、人力资源、社会保障、文旅、体育、广电、残疾人事业等。"},
    {"id": 10, "person_id": 8, "org_id": 2, "title": "黄平县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责公安、国安、司法、退役军人事务、维护稳定、信访、禁毒等；主持县公安局全面工作。"},
    {"id": 11, "person_id": 8, "org_id": 3, "title": "黄平县公安局党委书记、局长、督查长", "start": "", "end": "present", "rank": "副处级",
     "note": "主持县公安局全面工作。"},
    {"id": 12, "person_id": 9, "org_id": 2, "title": "黄平县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责工业和信息化、商务、民营经济、市场监管、招商引资、营商环境、政务服务、驻外联络等。"},
    {"id": 13, "person_id": 10, "org_id": 2, "title": "黄平县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责教育、民族宗教、卫生健康、医疗保障、大健康、工会、妇女儿童等。兼任新州镇党委书记。"},
    {"id": 14, "person_id": 10, "org_id": 1, "title": "新州镇党委书记（兼）", "start": "", "end": "present", "rank": "兼",
     "note": "现任副县长、新州镇党委书记（官方领导之窗）。"},
    {"id": 15, "person_id": 11, "org_id": 2, "title": "黄平县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "黄平县副县长（分工待核，领导之窗 2026-07 上线）。"},
    # 四套班子
    {"id": 16, "person_id": 12, "org_id": 4, "title": "黄平县人大常委会主任", "start": "", "end": "present", "rank": "正处级",
     "note": "2026-07-29 出席县委常委会扩大会议。"},
    {"id": 17, "person_id": 13, "org_id": 5, "title": "政协黄平县委员会主席", "start": "", "end": "present", "rank": "正处级",
     "note": "2026-07-29 出席县委常委会扩大会议。"},
    # 前任书记
    {"id": 18, "person_id": 14, "org_id": 1, "title": "前任中共黄平县委书记", "start": "（任职起止待查）", "end": "2026-07（卸任）", "rank": "正处级",
     "note": "州人大常委会副主任、县委书记；2026-07-10 仍主持县委常委会，2026-07-20 前由王思红接任。卸任后去向待查。"},
    # 前任县长
    {"id": 19, "person_id": 15, "org_id": 2, "title": "前任黄平县人民政府县长", "start": "（任职起止待查）", "end": "2026（卸任）", "rank": "正处级",
     "note": "曾任黄平县县长，新闻报道多次主持县政府党组会议、常务会议；2026 年为万政接替，卸任去向待查。"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记责王思红与县长万政党政正职搭档，共同主持县委常委会、县委县政府联席会议（2026-07 接手）。", "overlap_org": "中共黄平县委／黄平县政府", "overlap_period": "2026-07"},
    {"id": 2, "person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记领导县委副书记蒲桂蓉，2026-07-29 县委常委会同台出席。", "overlap_org": "中共黄平县委", "overlap_period": "2026-07"},
    {"id": 3, "person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记领导县委副书记曹振宇（2026-07-10 肖高峰时代同台出席）。", "overlap_org": "中共黄平县委", "overlap_period": "2026-07"},
    {"id": 4, "person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记领导常务副县长田奇（县委常委会成员，共同出席县委常委会）。", "overlap_org": "中共黄平县委／县政府", "overlap_period": "2026-07"},
    {"id": 5, "person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记领导县委常委、副县长洪加朗（县委常委会成员）。", "overlap_org": "中共黄平县委／县政府", "overlap_period": "2026-07"},
    {"id": 6, "person_a": 1, "person_b": 12, "type": "同级协作", "context": "县委书记与县人大常委会主任向国强同台出席县委常委会扩大会议。", "overlap_org": "黄平县四套班子", "overlap_period": "2026-07"},
    {"id": 7, "person_a": 1, "person_b": 13, "type": "同级协作", "context": "县委书记与县政协主席杨冰同台出席县委常委会扩大会议。", "overlap_org": "黄平县四套班子", "overlap_period": "2026-07"},
    {"id": 8, "person_a": 2, "person_b": 5, "type": "上下级", "context": "县长领导常务副县长田奇（协助县长抓财政、发改、应急等）。", "overlap_org": "黄平县人民政府", "overlap_period": "2026"},
    {"id": 9, "person_a": 2, "person_b": 6, "type": "上下级", "context": "县长与副县长洪加朗同属县政府班子，共同出席县政府会议。", "overlap_org": "黄平县人民政府", "overlap_period": "2026"},
    {"id": 10, "person_a": 2, "person_b": 8, "type": "上下级", "context": "县长领导副县长、公安局长舒烈跃（政府班子成员）。", "overlap_org": "黄平县人民政府／县公安局", "overlap_period": "2026"},
    {"id": 11, "person_a": 1, "person_b": 14, "type": "前继-后继", "context": "王思红中继肖高峰任黄平县委书记。肖高峰 2026-07-10 仍在任（主持县委常委会），2026-07-20 前卸任由王思红接任。", "overlap_org": "中共黄平县委", "overlap_period": "2026"},
    {"id": 12, "person_a": 14, "person_b": 2, "type": "上下级", "context": "前任县委书记肖高峰与县长万政在 2026-07-10 县委常委会同台（肖主持）。", "overlap_org": "中共黄平县委／县政府", "overlap_period": "2026-07"},
    {"id": 13, "person_a": 2, "person_b": 15, "type": "前继-后继", "context": "万政继任黄平县县长。前任县长杨满英（此前主持县政府），2026 年由万政接任。", "overlap_org": "黄平县人民政府", "overlap_period": "2026"},
    {"id": 14, "person_a": 14, "person_b": 3, "type": "上下级", "context": "前任县委书记肖高峰与县委副书记蒲桂蓉同台出席（2026-07-10）。", "overlap_org": "中共黄平县委", "overlap_period": "2026-07"},
]

# ── SQLite Build ───────────────────────────────────────────────────────────
if DB_PATH.exists():
    DB_PATH.unlink()

conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()
conn.executescript("""
    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '',
        birth TEXT DEFAULT '',
        birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '',
        party_join TEXT DEFAULT '',
        work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '',
        current_org TEXT DEFAULT '',
        source TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT DEFAULT '',
        level TEXT DEFAULT '',
        parent TEXT DEFAULT '',
        location TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        start TEXT DEFAULT '',
        end TEXT DEFAULT '',
        rank TEXT DEFAULT '',
        note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );

    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY,
        person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL,
        type TEXT DEFAULT '',
        context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
""")

for p in persons:
    cur.execute(
        "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
         p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
    )
for o in organizations:
    cur.execute(
        "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
    )
for pos in positions:
    cur.execute(
        "INSERT INTO positions (id, person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (pos["id"], pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"])
    )
for r in relationships:
    cur.execute(
        "INSERT INTO relationships (id, person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (r["id"], r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
    )
conn.commit()

# ── GEXF Generation ────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def is_party_secretary(post):
    # 现任县委书记 (not 副书记/前任/政协)
    return ("县委书记" in post) and ("县委副书记" not in post) and ("前任" not in post) and ("人民政协" not in post)

def is_gov_leader(post):
    # 现任县长 (not 副县长/前任; allow "县委副书记、县人民政府县长")
    return ("县长" in post) and ("副县长" not in post) and ("前任" not in post) \
        and ("县委副书记" not in post or "人民政府县长" in post)

def person_color(p):
    post = p.get("current_post", "") or ""
    if is_party_secretary(post):
        return "255,50,50"
    elif is_gov_leader(post):
        return "50,100,255"
    elif "常务副县长" in post:
        return "50,120,255"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    elif "副县长" in post:
        return "50,150,255"
    elif "副书记" in post:
        return "255,120,60"
    return "100,100,100"

def org_color(o):
    t = o.get("type", "") or ""
    if "党委" in t:
        return "255,200,200"
    elif "纪委" in t:
        return "255,220,180"
    elif "政府" in t:
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    return "200,200,200"

def is_top_leader(p):
    post = p.get("current_post", "") or ""
    return is_party_secretary(post) or is_gov_leader(post)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Research Agent - gov-relation</creator>')
lines.append('    <description>黄平县领导班子工作关系网络 - 贵州省黔东南苗族侗族自治州</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="organization" type="string"/>')
lines.append('    </attributes>')

lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", "") or "")}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", "") or "")}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o.get("type", "") or "")}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o.get("level", "") or "")}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

conn.close()

# ── Summary ────────────────────────────────────────────────────────────────
print(f"黄平县 network build complete.")
print(f"  Database:        {DB_PATH} ({DB_PATH.stat().st_size / 1024:.1f} KB)")
print(f"  GEXF:            {GEXF_PATH} ({GEXF_PATH.stat().st_size / 1024:.1f} KB)")
print(f"  Persons:         {len(persons)}")
print(f"  Organizations:   {len(organizations)}")
print(f"  Positions:       {len(positions)}")
print(f"  Relationships:   {len(relationships)}")
print()
print("Confidence notes:")
print("  - 王思红 (县委书记): confirmed via official 2026-07-20/29 县委常委会报道; earlier career empty (gap)")
print("  - 万政 (县长):      confirmed via official 领导之窗 bio + 县委常委会")
print("  - 班子成员:         confirmed via official 领导之窗 / 县委常委会新闻")
print("  - 前任书记肖高峰/前任县长杨满英交接窗口 confirmed; 履历与去向为 open gap")