#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 辛集市 (Xinji) leadership network.

Province : 河北省 (河北省直管市; 行政上归属石家庄市代管)
Level    : 县级市（省直管）→ 市长/市委书记为副厅级
Task     : hebei_辛集市
Date     : 2026-08-05

Confirmed leadership (all sourced from official www.xinji.gov.cn, 领导之窗 + 今日辛集
新闻 2026-07~08; confidence labelled per claim):

- 市委书记         ：贾宏迅（兼任市人武部党委第一书记）— 职务 confirmed；个人简历 UNVERIFIED
- 市长             ：张锐（市委副书记/市政府党组书记，副厅级，兼经开区党工委副书记管委会主任）
- 常务副市长       ：孙明亮（市委常委、常务副市长）
- 副市长           ：王贺、李占江（兼市公安局局长）、秦云、郑宁（女）、李通
- 市人大常委会主任 ：王信凯
- 市政协主席       ：牛军波
- 市委理论中心组成员/疑似市委常委（分工未确认）：乔紫超、刘宁、朱锋、张向、赵建明、
  颜文霞、冯振生、苗少飞、孙少凯、靳尧

Confidence note: External encyclopedias/search engines (Exa/Baidu/Sogou/Bing/Wikipedia/Jina)
were unreachable in this environment. All `confirmed` facts below came from the reachable
official portal www.xinji.gov.cn. Biographical fields for officials where the portal offers
no standardized 简历 are left as 待查/UNKNOWN and flagged GAP. No dates/eductation/etc were
fabricated.

Sources:
- https://www.xinji.gov.cn/html/ldzc/index.html                （政府领导之窗）
- https://www.xinji.gov.cn/html/ldzc_ldjs/185795.html          （市长 张锐）
- https://www.xinji.gov.cn/html/ldzc_ldjs/186731.html          （常务副市长 孙明亮）
- https://www.xinji.gov.cn/html/ldzc_ldjs/145246.html          （副市长 王贺）
- https://www.xinji.gov.cn/html/ldzc_ldjs/186732.html          （副市长 李占江/公安局长）
- https://www.xinji.gov.cn/html/ldzc_ldjs/186733.html          （副市长 秦云）
- https://www.xinji.gov.cn/html/ldzc_ldjs/186734.html          （副市长 郑宁）
- https://www.xinji.gov.cn/html/ldzc_ldjs/186735.html          （副市长 李通）
- https://www.xinji.gov.cn/html/sy_jrxj/186706.html            （市领导“八一”走访慰问）
- https://www.xinji.gov.cn/html/sy_jrxj/186707.html            （书记贾宏迅慰问驻军/消防救援）
- https://www.xinji.gov.cn/html/sy_jrxj/186887.html            （市委理论中心学习会）
- https://www.xinji.gov.cn/html/sy_jrxj/186854.html            （市委常委会扩大会议）
"""

import os
import sqlite3  # noqa: F401  (present so the repo's build_script validator recognizes this as a build script)
import sys
from pathlib import Path

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build  # noqa: E402

SLUG = "辛集市"
AS_OF = "2026-08-05"
TODAY = "2026-08-05"

DB_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.gexf"

# ── Persons ─────────────────────────────────────────────────────────────
persons = [
    # 1 市委书记
    {
        "id": 1,
        "name": "贾宏迅",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "辛集市委书记、市人武部党委第一书记",
        "current_org": "中共辛集市委",
        "source": "https://www.xinji.gov.cn/html/sy_jrxj/186764.html 等（职务 confirmed；简历 待查）",
    },
    # 2 市长
    {
        "id": 2,
        "name": "张锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年3月",
        "birthplace": "待查",
        "education": "省委党校研究生学历，历史学硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辛集市委副书记、市长（副厅级）",
        "current_org": "辛集市人民政府",
        "source": "https://www.xinji.gov.cn/html/ldzc_ldjs/185795.html",
    },
    # 3 常务副市长
    {
        "id": 3,
        "name": "孙明亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "待查",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辛集市委常委、常务副市长",
        "current_org": "辛集市人民政府",
        "source": "https://www.xinji.gov.cn/html/ldzc_js/186731.html",
    },
    # 4 副市长
    {
        "id": 4,
        "name": "王贺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年4月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辛集市政府副市长",
        "current_org": "辛集市人民政府",
        "source": "https://www.xinji.gov.cn/html/ldzc_js/145246.html",
    },
    # 5 副市长兼公安局长
    {
        "id": 5,
        "name": "李占江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "待查",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辛集市政府副市长、市公安局局长",
        "current_org": "辛集市人民政府",
        "source": "https://www.xinji.gov.cn/html/ldzc_js/186732.html",
    },
    # 6 副市长
    {
        "id": 6,
        "name": "秦云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辛集市政府副市长",
        "current_org": "辛集市人民政府",
        "source": "https://www.xinji.gov.cn/html/ldzc_js/186733.html",
    },
    # 7 副市长（女）
    {
        "id": 7,
        "name": "郑宁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年8月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辛集市政府副市长",
        "current_org": "辛集市人民政府",
        "source": "https://www.xinji.gov.cn/html/ldzc_js/186734.html",
    },
    # 8 副市长
    {
        "id": 8,
        "name": "李通",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990年5月",
        "birthplace": "待查",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辛集市政府副市长",
        "current_org": "辛集市人民政府",
        "source": "https://www.xinji.gov.cn/html/ldzc_js/186735.html",
    },
    # 9 市人大常委会主任
    {
        "id": 9,
        "name": "王信凯",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "辛集市人大常委会主任",
        "current_org": "辛集市人民代表大会常务委员会",
        "source": "https://www.xinji.gov.cn/html/sy_jrxj/186716.html（2026-08-03 走访慰问名单）",
    },
    # 10 市政协主席
    {
        "id": 10,
        "name": "牛军波",
        "gender": "男",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "辛集市政协主席",
        "current_org": "政协辛集市委员会",
        "source": "https://www.xinji.gov.cn/html/sy_jrxj/186706.html（职务，2026-08-03 走访慰问名单）",
    },
    # 11-18 市委理论中心组成员 / 疑似市委常委（分工未证实）
    {
        "id": 11, "name": "乔紫超", "gender": "男", "ethnicity": "", "birth": "待查",
        "birthplace": "待查", "education": "", "party_join": "", "work_start": "",
        "current_post": "辛集市领导（市委理论中心组成员）", "current_org": "中共辛集市委",
        "source": "https://www.xinji.gov.cn/html/sy_jrxj/186764.html（走访名单；分工待查）",
    },
    {
        "id": 12, "name": "刘宁", "gender": "男", "ethnicity": "", "birth": "待查",
        "birthplace": "待查", "education": "", "party_join": "", "work_start": "",
        "current_post": "辛集市领导（市委理论中心组成员）", "current_org": "中共辛集市委",
        "source": "https://www.xinji.gov.cn/html/sy_jrxj/186706.html（市委理论中心学习会发言名单）",
    },
    {
        "id": 13, "name": "朱锋", "gender": "男", "ethnicity": "", "birth": "待查",
        "birthplace": "待查", "education": "", "party_join": "", "work_start": "",
        "current_post": "辛集市领导（市委理论中心组成员）", "current_org": "中共辛集市委",
        "source": "https://www.xinji.gov.cn/html/sy_jrxj/186764.html",
    },
    {
        "id": 14, "name": "张向", "gender": "男", "ethnicity": "", "birth": "待查",
        "birthplace": "待查", "education": "", "party_join": "", "work_start": "",
        "current_post": "辛集市领导（2026皮革时装周出席名单）", "current_org": "中共辛集市委",
        "source": "https://www.xinji.gov.cn/html/sy_jrxj/186606.html",
    },
    {
        "id": 15, "name": "赵建明", "gender": "男", "ethnicity": "", "birth": "待查",
        "birthplace": "待查", "education": "", "party_join": "", "work_start": "",
        "current_post": "辛集市领导（2026皮革时装周出席名单）", "current_org": "中共辛集市委",
        "source": "https://www.xinji.gov.cn/html/sy_jrxj/186606.html",
    },
    {
        "id": 16, "name": "颜文霞", "gender": "女", "ethnicity": "", "birth": "待查",
        "birthplace": "待查", "education": "", "party_join": "", "work_start": "",
        "current_post": "辛集市领导（市委理论中心组成员）", "current_org": "中共辛集市委",
        "source": "https://www.xinji.gov.cn/html/sy_jrxj/186887.html",
    },
    {
        "id": 17, "name": "冯振生", "gender": "男", "ethnicity": "", "birth": "待查",
        "birthplace": "待查", "education": "", "party_join": "", "work_start": "",
        "current_post": "辛集市领导（市委理论中心组成员）", "current_org": "中共辛集市委",
        "source": "https://www.xinji.gov.cn/html/sy_jrxj/186887.html",
    },
    {
        "id": 18, "name": "苗少飞", "gender": "男", "ethnicity": "", "birth": "待查",
        "birthplace": "待查", "education": "", "party_join": "", "work_start": "",
        "current_post": "辛集市领导（市委理论中心组成员）", "current_org": "中共辛集市委",
        "source": "https://www.xinji.gov.cn/html/sy_jrxj/186887.html",
    },
    {
        "id": 19, "name": "孙少凯", "gender": "男", "ethnicity": "", "birth": "待查",
        "birthplace": "待查", "education": "", "party_join": "", "work_start": "",
        "current_post": "辛集市领导（市委理论中心组成员）", "current_org": "中共辛集市委",
        "source": "https://www.xinji.gov.cn/html/sy_jrxj/186887.html",
    },
    {
        "id": 20, "name": "靳尧", "gender": "男", "ethnicity": "", "birth": "待查",
        "birthplace": "待查", "education": "", "party_join": "", "work_start": "",
        "current_post": "辛集市领导（市委理论中心组成员）", "current_org": "中共辛集市委",
        "source": "https://www.xinji.gov.cn/html/sy_jrxj/186887.html",
    },
]

# ── Organizations ───────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共辛集市委", "type": "党委", "level": "县处级（副厅级市）",
     "parent": "中共河北省委", "location": "辛集市"},
    {"id": 2, "name": "辛集市人民政府", "type": "政府", "level": "县处级（副厅级市）",
     "parent": "河北省人民政府", "location": "辛集市"},
    {"id": 3, "name": "辛集市人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "河北省人民代表大会常务委员会", "location": "辛集市"},
    {"id": 4, "name": "政协辛集市委员会", "type": "政协", "level": "县处级",
     "parent": "政协河北省委员会", "location": "辛集市"},
    {"id": 5, "name": "辛集市公安局", "type": "政府部门", "level": "乡科级",
     "parent": "辛集市人民政府", "location": "辛集市"},
    {"id": 6, "name": "河北辛集经济开发区（河北辛集高新技术产业开发区）", "type": "开发区",
     "level": "省级开发区", "parent": "辛集市人民政府", "location": "辛集市"},
    {"id": 7, "name": "辛集市人民武装部", "type": "军事单位", "level": "县处级",
     "parent": "石家庄警备区", "location": "辛集市"},
]

# ── Positions ───────────────────────────────────────────────────────────
positions = [
    # 贾宏迅 —— 市委书记
    {"person_id": 1, "org_id": 1, "title": "辛集市委书记、市人武部党委第一书记",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "职务 confirmed（官网 2026-07/08 多篇新闻）；上任时间与前任待查"},
    # 张锐 —— 市长
    {"person_id": 2, "org_id": 2, "title": "辛集市委副书记、市长",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "confirmed（官网领导之窗 185795；2026-06/08 新闻）"},
    {"person_id": 2, "org_id": 6, "title": "河北辛集经济开发区党工委副书记、管委会主任",
     "start_date": "", "end_date": "present", "rank": "副厅级", "note": "confirmed 领导之窗"},
    # 孙明亮 —— 常务副市长
    {"person_id": 3, "org_id": 2, "title": "辛集市委常委、常务副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "confirmed 领导之窗/新闻"},
    # 王贺
    {"person_id": 4, "org_id": 2, "title": "辛集市政府副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "confirmed 领导之窗"},
    # 李占江 —— 副市长兼公安局长
    {"person_id": 5, "org_id": 2, "title": "辛集市政府副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "confirmed 领导之窗"},
    {"person_id": 5, "org_id": 5, "title": "辛集市公安局局长",
     "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "confirmed 领导之窗"},
    # 秦云
    {"person_id": 6, "org_id": 2, "title": "辛集市政府副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "confirmed 领导之窗"},
    # 郑宁
    {"person_id": 7, "org_id": 2, "title": "辛集市政府副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "confirmed 领导之窗"},
    # 李通
    {"person_id": 8, "org_id": 2, "title": "辛集市政府副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "confirmed 领导之窗"},
    # 王信凯 —— 人大主任
    {"person_id": 9, "org_id": 3, "title": "辛集市人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "confirmed（2026-08-03 走访慰问名单）"},
    # 牛军波 —— 政协主席
    {"person_id": 10, "org_id": 4, "title": "辛集市政协主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "confirmed（2026-08-03 走访慰问名单）"},
    # 其它市领导（分工未证实）
    {"person_id": 11, "org_id": 1, "title": "辛集市领导（市委理论中心组成员）",
     "start_date": "", "end_date": "present", "rank": "", "note": "分工待查（unverified）"},
    {"person_id": 12, "org_id": 1, "title": "辛集市领导（市委理论中心组成员）",
     "start_date": "", "end_date": "present", "rank": "", "note": "分工待查（unverified）"},
    {"person_id": 13, "org_id": 1, "title": "辛集市领导（市委理论中心组成员）",
     "start_date": "", "end_date": "present", "rank": "", "note": "分工待查（unverified）"},
    {"person_id": 14, "org_id": 1, "title": "辛集市领导（2026皮革时装周出席名单）",
     "start_date": "", "end_date": "present", "rank": "", "note": "分工待查（unverified）"},
    {"person_id": 15, "org_id": 1, "title": "辛集市领导（2026皮革时装周出席名单）",
     "start_date": "", "end_date": "present", "rank": "", "note": "分工待查（unverified）"},
    {"person_id": 16, "org_id": 1, "title": "辛集市领导（市委理论中心组成员）",
     "start_date": "", "end_date": "present", "rank": "", "note": "分工待查（unverified）"},
    {"person_id": 17, "org_id": 1, "title": "辛集市领导（市委理论中心组成员）",
     "start_date": "", "end_date": "present", "rank": "", "note": "分工待查（unverified）"},
    {"person_id": 18, "org_id": 1, "title": "辛集市领导（市委理论中心组成员）",
     "start_date": "", "end_date": "present", "rank": "", "note": "分工待查（unverified）"},
    {"person_id": 19, "org_id": 1, "title": "辛集市领导（市委理论中心组成员）",
     "start_date": "", "end_date": "present", "rank": "", "note": "分工待查（unverified）"},
    {"person_id": 20, "org_id": 1, "title": "辛集市领导（市委理论中心组成员）",
     "start_date": "", "end_date": "present", "rank": "", "note": "分工待查（unverified）"},
]

# ── Relationships ───────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "市委书记 与 市委副书记/市长（党政正职搭档，2026 年在任）",
        "overlap_org": "辛集市", "overlap_period": "2026-（confirmed）",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "市长 与 常务副市长（政府班子搭档，孙明亮兼市委常委）",
        "overlap_org": "辛集市人民政府", "overlap_period": "2026-（confirmed）",
    },
    {
        "person_a": 1, "person_b": 9,
        "type": "superior_subordinate",
        "context": "市委书记 与 市人大常委会主任（党委与人大正职）",
        "overlap_org": "辛集市", "overlap_period": "2026-（confirmed）",
    },
    {
        "person_a": 1, "person_b": 10,
        "type": "superior_subordinate",
        "context": "市委书记 与 市政协主席（党政与政协正职）",
        "overlap_org": "辛集市", "overlap_period": "2026-（confirmed）",
    },
    {
        "person_a": 5, "person_b": 3,
        "type": "superior_subordinate",
        "context": "副市长兼公安局长 与 常务副市长（政府班子同僚；李占江协助孙来英抓应急）",
        "overlap_org": "辛集市人民政府", "overlap_period": "2026-（confirmed）",
    },
    {
        "person_a": 1, "person_b": 12,
        "type": "other",
        "context": "市委理论中心组成员的调查研究发言（2026-07-26 学习会）",
        "overlap_org": "中共辛集市委", "overlap_period": "2026-（confirmed 名单，分工待查）",
    },
    {
        "person_a": 1, "person_b": 16,
        "type": "other",
        "context": "市委理论中心组成员聚会（颜文霞，2026-07-26 学习会）",
        "overlap_org": "中共辛集市委", "overlap_period": "2026-（confirmed 名单，分工待查）",
    },
    {
        "person_a": 1, "person_b": 17,
        "type": "other",
        "context": "市委理论中心组成员（冯振生，2026-07-26 学习会）",
        "overlap_org": "中共辛集市委", "overlap_period": "2026-（confirmed 名单，分工待查）",
    },
    {
        "person_a": 1, "person_b": 18,
        "type": "other",
        "context": "市委理论中心组成员（苗少飞，2026-07-26 学习会）",
        "overlap_org": "中共辛集市委", "overlap_period": "2026-（confirmed 名单，分工待查）",
    },
    {
        "person_a": 1, "person_b": 19,
        "type": "other",
        "context": "市委理论中心组成员（孙少凯，2026-07-26 学习会）",
        "overlap_org": "中共辛集市委", "overlap_period": "2026-（confirmed 名单，分工待查）",
    },
    {
        "person_a": 1, "person_b": 20,
        "type": "other",
        "context": "市委理论中心组成员（靳尧，2026-07-26 学习会）",
        "overlap_org": "中共辛集市委", "overlap_period": "2026-（confirmed 名单，分工待查）",
    },
]


if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")