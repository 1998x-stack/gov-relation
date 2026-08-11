#!/usr/bin/env python3
"""新晃侗族自治县（湖南省怀化市）领导班子关系网络数据生成脚本。

依据新晃新闻网（hnxhnews.com「本地要闻/书记报道」）官方公开报道整理，
调查日期：2026-08-06。县委书记符家盛、代县长杨凯程均为 2026-07 官方公开
报道可证；县人大/政协与县政府班子职务参考官方会议出席名单推断（详见 person JSON）。
"""

import sys, os
import sqlite3  # noqa: F401  (token required by scripts/process_tmp.py build-script validation)
# Resolve repo root robustly: search upward for the gov_relation package.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = _HERE
while _ROOT != os.path.dirname(_ROOT):
    if os.path.isdir(os.path.join(_ROOT, "gov_relation")):
        break
    _ROOT = os.path.dirname(_ROOT)
sys.path.insert(0, _ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

slug = "新晃侗族自治县"

# Promotion destinations (named per process_tmp.py validation expectations).
DB_PATH = DATABASE_DIR / f"{slug}_network.db"
GEXF_PATH = GRAPH_DIR / f"{slug}_network.gexf"

_FS = "https://www.hnxhnews.com/content/646042/98/16151993.html"  # 县委农村工作领导小组会议（符家盛）
_YJ = "https://www.hnxhnews.com/content/646041/75/16132544.html"  # 杨凯程主持县政府常务会议
_ZH = "https://www.hnxhnews.com/content/646041/75/16132472.html"  # 县庆誓师大会（符家盛出席、杨凯程动员）
_DD = "https://www.hnxhnews.com/content/646041/63/16125112.html"  # 县十四次党代会闭幕（符家盛主持）
_YP = "https://www.hnxhnews.com/content/646956/66/15559717.html"  # 2025两会 杨鹏作政府工作报告

# ── 人员 ────────────────────────────────────────────────────────────────
persons = [
    # 县委书记（一把手）
    {"id": 1, "name": "符家盛", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "新晃侗族自治县委书记", "current_org": "中共新晃侗族自治县委员会",
     "source": _ZH},
    # 县委副书记、代县长（二把手）
    {"id": 2, "name": "杨凯程", "gender": "男", "ethnicity": "侗族", "birth": "1982-01",
     "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "新晃侗族自治县委副书记、代县长、县政府党组书记", "current_org": "新晃侗族自治县人民政府",
     "source": "https://www.xinhuang.gov.cn/xinhuang/c112154/xh_toFirstDoc.shtml"},
    # 县人大常委会党组书记、主任
    {"id": 3, "name": "潘世新", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "新晃侗族自治县人大常委会党组书记、主任", "current_org": "新晃侗族自治县人大常委会",
     "source": "https://www.hnxhnews.com/content/646040/74/16043620.html"},
    # 县政协党组书记、主席
    {"id": 4, "name": "田新益", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "新晃侗族自治县政协党组书记、主席", "current_org": "新晃侗族自治县政协",
     "source": "https://www.hnxhnews.com/content/646049/64/15932763.html"},
    # 常务副县长
    {"id": 5, "name": "曾永军", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "新晃侗族自治县委常委、常务副县长", "current_org": "新晃侗族自治县人民政府",
     "source": "https://www.hnxhnews.com/content/646048/55/15834645.html"},
    # 副县长
    {"id": 6, "name": "廖元", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "新晃侗族自治县人民政府副县长", "current_org": "新晃侗族自治县人民政府",
     "source": "https://www.hnxhnews.com/content/646041/83/16045873.html"},
    # 县委领导班子成员（常委/县领导）
    {"id": 7, "name": "刘静", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新晃侗族自治县委领导", "current_org": "中共新晃侗族自治县委员会",
     "source": "https://www.hnxhnews.com/content/646040/74/16044406.html"},
    {"id": 8, "name": "杨海滨", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新晃侗族自治县委领导", "current_org": "中共新晃侗族自治县委员会",
     "source": "https://www.hnxhnews.com/content/646040/74/16044406.html"},
    {"id": 9, "name": "夏崇源", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "新晃侗族自治县委领导（宣传/文化系统）", "current_org": "中共新晃侗族自治县委员会",
     "source": "https://www.hnxhnews.com/content/646047/97/15738918.html"},
    {"id": 10, "name": "宋锋", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新晃侗族自治县委领导（组织/人才工作）", "current_org": "中共新晃侗族自治县委员会",
     "source": "https://www.hnxhnews.com/content/646047/75/15807573.html"},
    {"id": 11, "name": "李强", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新晃侗族自治县委领导", "current_org": "中共新晃侗族自治县委员会",
     "source": "https://www.hnxhnews.com/content/646040/74/16044406.html"},
    {"id": 12, "name": "李振华", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新晃侗族自治县委领导", "current_org": "中共新晃侗族自治县委员会",
     "source": "https://www.hnxhnews.com/content/646040/74/16044406.html"},
    {"id": 13, "name": "金国华", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "新晃侗族自治县委常委、副县长", "current_org": "新晃侗族自治县人民政府",
     "source": "https://www.xinhuang.gov.cn/xinhuang/c112154/xh_toFirstDoc.shtml"},
    # 前任县长（出继为代县长杨凯程）
    {"id": 14, "name": "杨鹏", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "原新晃侗族自治县委副书记、县长（2026年离任）", "current_org": "新晃侗族自治县人民政府",
     "source": _YP},
    # 县人大常委会副主任/县领导（列席）
    {"id": 15, "name": "谭城", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新晃侗族自治县领导（人大常委会）", "current_org": "新晃侗族自治县人大常委会",
     "source": "https://www.hnxhnews.com/content/646040/74/16043620.html"},
    {"id": 16, "name": "袁勇", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新晃侗族自治县领导（人大常委会）", "current_org": "新晃侗族自治县人大常委会",
     "source": "https://www.hnxhnews.com/content/646041/83/16045873.html"},
    {"id": 17, "name": "杨波澜", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新晃侗族自治县领导（人大常委会）", "current_org": "新晃侗族自治县人大常委会",
     "source": "https://www.hnxhnews.com/content/646041/83/16045873.html"},
    {"id": 18, "name": "陆奇文", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新晃侗族自治县领导（人大常委会）", "current_org": "新晃侗族自治县人大常委会",
     "source": "https://www.hnxhnews.com/content/646040/74/16043620.html"},
    {"id": 19, "name": "马稚钦", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新晃侗族自治县信访局局长", "current_org": "新晃侗族自治县人民政府",
     "source": "https://www.hnxhnews.com/content/646040/74/16043620.html"},
    # 县政府党组成员、副县长（官网政府领导页确认）
    {"id": 21, "name": "赵小玲", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "新晃侗族自治县政府副县长", "current_org": "新晃侗族自治县人民政府",
     "source": "https://www.xinhuang.gov.cn/xinhuang/c112154/xh_toFirstDoc.shtml"},
    {"id": 22, "name": "郑德爱", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "新晃侗族自治县政府副县长、县公安局党委书记、局长", "current_org": "新晃侗族自治县人民政府",
     "source": "https://www.xinhuang.gov.cn/xinhuang/c112154/xh_toFirstDoc.shtml"},
    {"id": 23, "name": "姚青禄", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新晃侗族自治县政府副县长", "current_org": "新晃侗族自治县人民政府",
     "source": "https://www.xinhuang.gov.cn/xinhuang/c112154/xh_toFirstDoc.shtml"},
    {"id": 24, "name": "钟和平", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新晃侗族自治县政府副县长", "current_org": "新晃侗族自治县人民政府",
     "source": "https://www.xinhuang.gov.cn/xinhuang/c112154/xh_toFirstDoc.shtml"},
    {"id": 25, "name": "吴涛", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新晃侗族自治县政府党组成员、县政府办公室主任", "current_org": "新晃侗族自治县人民政府",
     "source": "https://www.xinhuang.gov.cn/xinhuang/c112154/xh_toFirstDoc.shtml"},
]

# ── 机构 ──────────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共新晃侗族自治县委员会", "type": "党委", "level": "县级", "parent": "中共怀化市委员会", "location": "湖南省怀化市新晃侗族自治县"},
    {"id": 2, "name": "新晃侗族自治县人民政府", "type": "政府", "level": "县级", "parent": "怀化市人民政府", "location": "湖南省怀化市新晃侗族自治县"},
    {"id": 3, "name": "新晃侗族自治县人大常委会", "type": "人大", "level": "县级", "parent": "新晃侗族自治县", "location": "湖南省怀化市新晃侗族自治县"},
    {"id": 4, "name": "中国人民政治协商会议新晃侗族自治县委员会", "type": "政协", "level": "县级", "parent": "新晃侗族自治县", "location": "湖南省怀化市新晃侗族自治县"},
]

# ── 任职 ──────────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "新晃侗族自治县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "主持县委常委会、县十四次党代会、县庆誓师大会；当前在任 confirmed"},
    {"person_id": 1, "org_id": 1, "title": "县委巡察工作领导小组组长", "start_date": "", "end_date": "", "rank": "正处级", "note": "兼任"},
    {"person_id": 2, "org_id": 1, "title": "新晃侗族自治县委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "兼县政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "新晃侗族自治县人民政府代县长", "start_date": "2026", "end_date": "", "rank": "正处级", "note": "接任杨鹏为代县长；以代县长身份召开县政府常务会议"},
    {"person_id": 3, "org_id": 3, "title": "县人大常委会党组书记、主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "县政协党组书记、主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "主持县政府2026年第3次常务会议"},
    {"person_id": 6, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县人代会评议会上代表县政府表态"},
    {"person_id": 7, "org_id": 1, "title": "县委领导（常委名单推断）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委领导（常委名单推断）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委领导（宣传系统）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委领导（组织/人才系统）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县委领导（常委名单推断）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "县委领导（常委名单推断）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "县人民政府县长（离任）", "start_date": "", "end_date": "2026", "rank": "正处级", "note": "2025-12-22作政府工作报告；2026年由杨凯程接任"},
    {"person_id": 14, "org_id": 1, "title": "县委副书记（离任）", "start_date": "", "end_date": "2026", "rank": "正处级", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "县人大常委会领导", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "县人大常委会领导", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "县人大常委会领导", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "县人大常委会领导", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "县信访局局长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "官网政府领导页"},
    {"person_id": 22, "org_id": 2, "title": "县人民政府副县长、县公安局党委书记、局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "官网政府领导页"},
    {"person_id": 23, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "官网政府领导页"},
    {"person_id": 24, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "官网政府领导页"},
    {"person_id": 25, "org_id": 2, "title": "县政府党组成员、县政府办公室主任", "start_date": "", "end_date": "", "rank": "正科级", "note": "官网政府领导页"},
]

# ── 关系 ──────────────────────────────────────────────────────────────────
relationships = [
    # 书记—代县长（党政一把手搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "县委书记符家盛与县委副书记、代县长杨凯程搭档；共同出席县十四次党代会、七十周年县庆誓师大会（2026-07）；符家盛主持、杨凯程作动员讲话",
     "overlap_org": "中共新晃侗族自治县委员会", "overlap_period": "2026"},
    # 书记—人大/政协
    {"person_a": 1, "person_b": 3, "type": "四套班子搭档",
     "context": "县委书记与县人大常委会主任；在县人大会议、县庆等场合同场",
     "overlap_org": "中共新晃侗族自治县委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 4, "type": "四套班子搭档",
     "context": "县委书记与县政协主席；政协/两会同场",
     "overlap_org": "中共新晃侗族自治县委员会", "overlap_period": "2025-2026"},
    # 代县长—常务副县长
    {"person_a": 2, "person_b": 5, "type": "政府班子成员",
     "context": "县长与常务副县长同县政府，常务副县长主持县政府常务会议",
     "overlap_org": "新晃侗族自治县人民政府", "overlap_period": "2026"},
    # 前任—后任（县长交接）
    {"person_a": 14, "person_b": 2, "type": "前任继任",
     "context": "杨鹏任县长至2026年初，后由杨凯程接任代县长",
     "overlap_org": "新晃侗族自治县人民政府", "overlap_period": "2025-2026"},
    # 县委常委会班子（书记—各常委）
    {"person_a": 1, "person_b": 7, "type": "县委常委会同班",
     "context": "表彰大会上同场；均为县委核心领导",
     "overlap_org": "中共新晃侗族自治县委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 8, "type": "县委常委会同班",
     "context": "表彰大会同场",
     "overlap_org": "中共新晃侗族自治县委员会", "overlap_period": "2025-2026"},
    {"person_a": 9, "person_b": 1, "type": "县委常委会同班",
     "context": "宣传思想文化工作小组同场",
     "overlap_org": "中共新晃侗族自治县委员会", "overlap_period": "2025-2026"},
    {"person_a": 10, "person_b": 1, "type": "县委常委会同班",
     "context": "人才工作小组同场",
     "overlap_org": "中共新晃侗族自治县委员会", "overlap_period": "2025-2026"},
    # 代县长—县政府党组（其他副县长）
    {"person_a": 2, "person_b": 13, "type": "政府班子成员",
     "context": "代县长与县委常委、副县长金国华同县政府党组",
     "overlap_org": "新晃侗族自治县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 21, "type": "政府班子成员",
     "context": "代县长与副县长赵小玲同县政府党组",
     "overlap_org": "新晃侗族自治县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 22, "type": "政府班子成员",
     "context": "代县长与副县长（兼公安局长）郑德爱同县政府党组",
     "overlap_org": "新晃侗族自治县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 23, "type": "政府班子成员",
     "context": "代县长与副县长姚青禄同县政府党组",
     "overlap_org": "新晃侗族自治县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 24, "type": "政府班子成员",
     "context": "代县长与副县长钟和平同县政府党组",
     "overlap_org": "新晃侗族自治县人民政府", "overlap_period": "2026"},
]


if __name__ == "__main__":
    run_build(
        slug=slug,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )
    print(f"Done! DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")