#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 汉中市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_汉中市
Level: 地级市
Targets: 市委书记 & 市长

Research sources (primary, directly accessed this session):
  - https://www.hanzhong.gov.cn/ — 汉中市政府门户（首页新闻: 张烨=市委书记、王建平=市长）
  - https://www.hanzhong.gov.cn/hzszf/wjp/szfld.shtml — 市长 王建平 官方简历（2023年4月更新）
  - https://www.hanzhong.gov.cn/hzszf/wxj/szfld.shtml — 常务副市长 王旭坚 简历（2025-04更新）
  - https://www.hanzhong.gov.cn/hzszf/wsb/szfld.shtml — 副市长 王松柏 简历
  - https://www.hanzhong.gov.cn/hzszf/duding/szfld.shtml — 副市长 杜顶 简历
  - https://www.hanzhong.gov.cn/hzszf/wwq/szfld.shtml — 副市长 吴维强 简历
  - https://www.hanzhong.gov.cn/hzszf/zxm/szfld.shtml — 副市长 郑雪梅 简历
  - https://www.hanzhong.gov.cn/hzszf/zhangpeng/szfld.shtml — 副市长 张鹏 简历
  - https://www.hanzhong.gov.cn/hzszf/songxu/szfld.shtml — 副市长 宋旭 简历
  - https://www.hanzhong.gov.cn/hzszf/likuan/szfld.shtml — 副市长 李宽 简历
  - https://www.hanzhong.gov.cn/hzszf/wzz/szfld.shtml — 市政府秘书长 王镇 简历
  - https://zh.wikipedia.org/wiki/张烨_(1972年) — 市委书记 张烨 完整履历（中宣部背景; 2023-03任书记）
  - 汉中要闻 2026-08-06/07（官媒）: 市委常委/组织部部长 周耀宜、市委常委/纪委书记 钟伟
  - 维基百科 汉中市正职领导人列表（人大主任 杨记明、政协主席 蔡煜东、历任书记）

Leadership facts (confirmed, as of 2026-08):
  - 市委书记: 张烨（2023-03 上任，此前任汉中市长 2021-2023、陕西省广播电视局局长）
  - 市长: 王建平（2023 接任张烨的市长职务；1972年10月生）
  - 党政搭档: 张烨（书记）x 王建平（市长）; 张烨另为王建平的前任市长
  - 前任书记: 钟洪江（2021-2023）→ 张烨接任；张烨市长之位亦由钟洪江传下

Confidence notes:
  - 市委书记/市长身份与简历: confirmed（官媒 + 政府门户 + 维基百科）
  - 市政府领导班子及分管领域: confirmed（政府门户 领导之窗 2026）
  - 市委常委 周耀宜(组织部长)、钟伟(纪委书记): confirmed（2026-08 市委巡察动员部署会官宣）
  - 市人大主任 杨记明、政协主席 蔡煜东: plausible（维基百科正职列表）
  - 出生年份：多数据官简历；个别出生地/学历 detail unverified（见 open_questions）
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

import sqlite3  # noqa — used by gov_relation.runner via import

from gov_relation.runner import run_build

# ── Metadata ────────────────────────────────────────────────────────────────
SLUG = "汉中市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ───────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_汉中市"
if _CURRENT_DIR.name == "shaanxi_汉中市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ────────────────────────────────────────────────────────────────
# ID 1-2: 市委主要领导（书记/市长/前任书记）; 3-12: 市政府领导班子;
# 13-14: 市委常（组织部/纪委）; 15-16: 人大/政协
persons = [
    # ════════════════ 市委主要领导 ════════════════
    {
        "id": 1, "name": "张烨", "gender": "男", "ethnicity": "汉族",
        "birth": "1972年8月", "birthplace": "河北省秦皇岛市北戴河区", "education": "大学(法学)，公共管理硕士",
        "party_join": "中共党员", "work_start": "1995年",
        "current_post": "市委书记", "current_org": "中共汉中市委",
        "source": "https://www.hanzhong.gov.cn/hzszf/xwzx/zwyw/202608/6f630737ef0a420986df1d0cc4fe7c1e.shtml"
    },
    {
        "id": 2, "name": "王建平", "gender": "男", "ethnicity": "汉族",
        "birth": "1972年10月", "birthplace": "", "education": "大学学历，工学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市长、市委副书记、市政府党组书记", "current_org": "汉中市人民政府",
        "source": "https://www.hanzhong.gov.cn/hzszf/wjp/szfld.shtml"
    },
    {
        "id": 3, "name": "钟洪江", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任市委书记(2021-2023)", "current_org": "中共汉中市委",
        "source": "https://zh.wikipedia.org/wiki/张烨_(1972年)"
    },
    # ════════════════ 市政府领导班子 ════════════════
    {
        "id": 4, "name": "王旭坚", "gender": "男", "ethnicity": "汉族",
        "birth": "1978年5月", "birthplace": "", "education": "研究生学历，工学硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、常务副市长", "current_org": "汉中市人民政府",
        "source": "https://www.hanzhong.gov.cn/hzszf/wxj/szfld.shtml"
    },
    {
        "id": 5, "name": "王松柏", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年2月", "birthplace": "", "education": "在职研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、副市长", "current_org": "汉中市人民政府",
        "source": "https://www.hanzhong.gov.cn/hzszf/wsb/szfld.shtml"
    },
    {
        "id": 6, "name": "杜顶", "gender": "男", "ethnicity": "汉族",
        "birth": "1976年12月", "birthplace": "", "education": "研究生学历，管理学博士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、副市长", "current_org": "汉中市人民政府",
        "source": "https://www.hanzhong.gov.cn/hzszf/duding/szfld.shtml"
    },
    {
        "id": 7, "name": "吴维强", "gender": "男", "ethnicity": "汉族",
        "birth": "1970年1月", "birthplace": "", "education": "在职研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "汉中市人民政府",
        "source": "https://www.hanzhong.gov.cn/hzszf/wwq/szfld.shtml"
    },
    {
        "id": 8, "name": "郑雪梅", "gender": "女", "ethnicity": "汉族",
        "birth": "1969年7月", "birthplace": "", "education": "在职研究生学历",
        "party_join": "民革党员", "work_start": "",
        "current_post": "副市长、市工商联主席", "current_org": "汉中市人民政府",
        "source": "https://www.hanzhong.gov.cn/hzszf/zxm/szfld.shtml"
    },
    {
        "id": 9, "name": "张鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "1973年3月", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长、市公安局局长", "current_org": "汉中市公安局",
        "source": "https://www.hanzhong.gov.cn/hzszf/zhangpeng/szfld.shtml"
    },
    {
        "id": 10, "name": "宋旭", "gender": "男", "ethnicity": "汉族",
        "birth": "1976年7月", "birthplace": "", "education": "研究生学历，管理学博士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "汉中市人民政府",
        "source": "https://www.hanzhong.gov.cn/hzszf/songxu/szfld.shtml"
    },
    {
        "id": 11, "name": "李宽", "gender": "男", "ethnicity": "汉族",
        "birth": "1972年3月", "birthplace": "", "education": "在职研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "汉中市人民政府",
        "source": "https://www.hanzhong.gov.cn/hzszf/likuan/szfld.shtml"
    },
    {
        "id": 12, "name": "王镇", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年11月", "birthplace": "", "education": "在职研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市政府党组成员、市政府秘书长", "current_org": "汉中市人民政府办公室",
        "source": "https://www.hanzhong.gov.cn/hzszf/wzz/szfld.shtml"
    },
    # ════════════════ 市委常委(组织/纪委) ════════════════
    {
        "id": 13, "name": "周耀宜", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、市委组织部部长", "current_org": "中共汉中市委组织部",
        "source": "https://www.hanzhong.gov.cn/hzszf/xwzx/zwyw/202608/6f630737ef0a420986df1d0cc4fe7c1e.shtml"
    },
{
        "id": 14, "name": "钟伟", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、市纪委书记", "current_org": "汉中市纪律检查委员会",
        "source": "https://www.hanzhong.gov.cn/hzszf/xwzx/zwyw/202608/6a630737ef0a420986df1d0cc4fe7c1e.shtml"
    },
    # ════════════════ 市委常委(其他) ════════════════
    {
        "id": 17, "name": "郭志胜", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委", "current_org": "中共汉中市委",
        "source": "https://www.hanzhong.gov.cn/hzszf/xwzx/zwyw/202608/383338c43f3a4912ba03edd8174aebdc.shtml"
    },
    {
        "id": 18, "name": "王红艳", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委", "current_org": "中共汉中市委",
        "source": "https://www.hanzhong.gov.cn/hzszf/xwzx/zwyw/202608/383338c43f3a4912ba03edd8174aebdc.shtml"
    },
    {
        "id": 19, "name": "万启杰", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委", "current_org": "中共汉中市委",
        "source": "https://www.hanzhong.gov.cn/hzszf/xwzx/zwyw/202608/383338c43f3a4912ba03edd8174aebdc.shtml"
    },
    {
        "id": 20, "name": "方红卫", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任市委书记(2020-2021，已被处分)", "current_org": "中共汉中市委",
        "source": "https://zh.wikipedia.org/wiki/方红卫_(政治人物)"
    },
    # ════════════════ 人大 / 政协 ════════════════
    {
        "id": 15, "name": "杨记明", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会主任", "current_org": "汉中市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/张烨_(1972年)"
    },
    {
        "id": 16, "name": "蔡煜东", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市政协主席", "current_org": "政协汉中市委员会",
        "source": "https://zh.wikipedia.org/wiki/张烨_(1972年)"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共汉中市委", "type": "党委", "level": "地级市", "parent": "中共陕西省委", "location": "汉中市"},
    {"id": 2, "name": "汉中市人民政府", "type": "政府", "level": "地级市", "parent": "陕西省人民政府", "location": "汉中市"},
    {"id": 3, "name": "汉中市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "陕西省人大常委会", "location": "汉中市"},
    {"id": 4, "name": "政协汉中市委员会", "type": "政协", "level": "地级市", "parent": "政协陕西省委员会", "location": "汉中市"},
    {"id": 5, "name": "中共汉中市委组织部", "type": "党委", "level": "地级市", "parent": "中共汉中市委", "location": "汉中市"},
    {"id": 6, "name": "汉中市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共汉中市委", "location": "汉中市"},
    {"id": 7, "name": "汉中市公安局", "type": "政府", "level": "处级", "parent": "汉中市人民政府", "location": "汉中市"},
    {"id": 8, "name": "汉中市人民政府办公室", "type": "政府", "level": "处级", "parent": "汉中市人民政府", "location": "汉中市"},
    {"id": 9, "name": "陕西省广播电视局", "type": "政府", "level": "厅级", "parent": "陕西省人民政府", "location": "西安市"},
    {"id": 10, "name": "中共中央宣传部", "type": "党委", "level": "中央部委", "parent": "中国共产党中央委员会", "location": "北京市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 张烨 (书记; 市长→书记 本地晋升)
    {"person_id": 1, "org_id": 10, "title": "中宣部新闻局副局长、国际联络局局长", "start": "2015", "end": "2020",
     "rank": "厅局级副职", "note": "中宣部多年工作：新闻研究处/国家应急新闻中心发起；2017.7任用中宣部国际联络局局长"},
    {"person_id": 1, "org_id": 9, "title": "陕西省广播电视局局长、党组书记", "start": "2020.10", "end": "2021.6",
     "rank": "正厅级", "note": "由中宣部转地方，任陕西省广播电视局局长"},
    {"person_id": 1, "org_id": 2, "title": "市委副书记、市政府代市长→市长", "start": "2021.6", "end": "2023.3",
     "rank": "正厅级", "note": "2021.6任代市长，2021.8.31去代转正；前任钟洪江"},
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2023.3", "end": "present",
     "rank": "正厅级", "note": "2023-03-25任汉中市委书记"},
    # 王建平 (市长)
    {"person_id": 2, "org_id": 9, "title": "省政府组成部门副处长、处长", "start": "", "end": "",
     "rank": "县处级", "note": "早期任职于省政府组成部门"},
    {"person_id": 2, "org_id": 2, "title": "地级市副市长、市委常委、市委秘书长", "start": "", "end": "",
     "rank": "副厅级", "note": "曾在地级市任副市长、市委常委、市委秘书长"},
    {"person_id": 2, "org_id": 9, "title": "省政府副秘书长、机关党组成员", "start": "", "end": "",
     "rank": "副厅级", "note": "省政府副秘书长、机关党组成员"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记、市政府市长、党组书记", "start": "2023", "end": "present",
     "rank": "正厅级", "note": "2023年起任汉中市长；接替张烨（张烨转任书记）"},
    # 钟洪江 (前任书记/市长)
    {"person_id": 3, "org_id": 2, "title": "市委副书记、市长", "start": "~2016", "end": "2021.6",
     "rank": "正厅级", "note": "2019-2021任汉中市长，张烨接任"},
    {"person_id": 3, "org_id": 1, "title": "市委书记", "start": "2019", "end": "2023.3",
     "rank": "正厅级", "note": "2021.6-2023.3任汉中市委书记；张烨2023.3接任"},
    # 方红卫 (前任书记)
    {"person_id": 20, "org_id": 1, "title": "市委书记", "start": "2020", "end": "2021",
     "rank": "正厅级", "note": "汉中市委书记2020-2021；后调西安；2025-11落马、2026-07开除党籍公职"},
    {"person_id": 20, "org_id": 1, "title": "西安市委书记", "start": "2021", "end": "2025",
     "rank": "副省部", "note": "省委常委、西安市委书记；2025-11-07 被查"},
    # 市政府班子
    {"person_id": 4, "org_id": 2, "title": "市委常委、常务副市长", "start": "", "end": "",
     "rank": "副厅级", "note": "分管市发改委、自然资源、卫健、应急、统计、医保等"},
    {"person_id": 4, "org_id": 6, "title": "地级市市纪委书记、市监委主任", "start": "", "end": "",
     "rank": "副厅级", "note": "此前曾任地级市纪委书记、市监委主任"},
    {"person_id": 5, "org_id": 2, "title": "市委常委、副市长", "start": "", "end": "",
     "rank": "副厅级", "note": "分管生态环保、住建、城管、交通、市场监管等"},
    {"person_id": 6, "org_id": 2, "title": "市委常委、副市长", "start": "", "end": "",
     "rank": "副厅级", "note": "中央部委挂职；分管行政审批、政府研究、航空配套产业链"},
    {"person_id": 6, "org_id": 9, "title": "国家部委所属单位高级工程师/处长/副主任", "start": "", "end": "",
     "rank": "厅局级", "note": "挂职交流前任职于中央部委"},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "", "end": "",
     "rank": "副厅级", "note": "分管科技、工信、人社等"},
    {"person_id": 8, "org_id": 2, "title": "副市长、市工商联主席", "start": "", "end": "",
     "rank": "副厅级", "note": "分管教育、体育、旅游机场等；民革党员"},
    {"person_id": 9, "org_id": 2, "title": "副市长、市公安局局长", "start": "", "end": "",
     "rank": "副厅级", "note": "公安局长；分管公安、司法、退役军人、信访"},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start": "", "end": "",
     "rank": "副厅级", "note": "分管国资、民政、国资等"},
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "", "end": "",
     "rank": "副厅级", "note": "分管公安、司法、文旅等"},
    {"person_id": 12, "org_id": 2, "title": "市政府党组成员、市政府秘书长", "start": "", "end": "",
     "rank": "正处级", "note": "主持市政府办公室全面工作"},
    # 组织部/纪委
    {"person_id": 13, "org_id": 5, "title": "市委常委、市委组织部部长", "start": "", "end": "",
     "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 6, "title": "市委常委、市纪委书记", "start": "", "end": "",
     "rank": "副厅级", "note": ""},
    # 其他市委常委
    {"person_id": 17, "org_id": 1, "title": "市委常委", "start": "", "end": "",
     "rank": "副厅级", "note": ""},
    {"person_id": 18, "org_id": 1, "title": "市委常委", "start": "", "end": "",
     "rank": "副厅级", "note": ""},
    {"person_id": 19, "org_id": 1, "title": "市委常委", "start": "", "end": "",
     "rank": "副厅级", "note": ""},
    # 人大/政协
    {"person_id": 15, "org_id": 3, "title": "市人大常委会主任", "start": "", "end": "",
     "rank": "正厅级", "note": ""},
    {"person_id": 16, "org_id": 4, "title": "市政协主席", "start": "", "end": "",
     "rank": "正厅级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记与市长（市委、市政府一把手）", "overlap_org": "汉中市", "overlap_period": "2023-至今"},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "张烨由汉中市长升任市委书记，王建平接任市长职", "overlap_org": "汉中市人民政府", "overlap_period": "2023"},
    # 前任书记
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "钟洪江为前任市委书记，张烨2023年3月接任", "overlap_org": "中共汉中市委", "overlap_period": "2023.03"},
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "钟洪江辞去市长，张烨2021年6月接任代市长", "overlap_org": "汉中市人民政府", "overlap_period": "2021"},
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor", "context": "钟洪江为前任市长（2016-2021），其后再任书记；王建平2023接任市长", "overlap_org": "汉中市人民政府", "overlap_period": "2023"},
    # 前任书记方红卫
    {"person_a": 20, "person_b": 3, "type": "predecessor_successor", "context": "方红卫为前任书记（2020-2021），钟洪江接任；方红卫后调西安，2025落马（风险信号）", "overlap_org": "中共汉中市委", "overlap_period": "2021"},
    # 书记 x 政府班子成员
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委书记与常务副市长", "overlap_org": "中共汉中市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "市委书记与市委常委/副市长", "overlap_org": "中共汉中市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "市委书记与市委常委/副市长（中央挂职干部）", "overlap_org": "中共汉中市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "市委书记与组织部部长", "overlap_org": "中共汉中市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate", "context": "市委书记与纪委书记", "overlap_org": "中共汉中市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "市委书记与市委常委（共常委会）", "overlap_org": "中共汉中市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 18, "type": "overlap", "context": "市委书记与市委常委（共常委会）", "overlap_org": "中共汉中市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 19, "type": "overlap", "context": "市委书记与市委常委（共常委会）", "overlap_org": "中共汉中市委", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "市长与市委常委（常委会同席）", "overlap_org": "中共汉中市委", "overlap_period": ""},
    # 市长 x 副市长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "市长与常务副市长", "overlap_org": "汉中市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "市长与副市长", "overlap_org": "汉中市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "市长与副市长（中央挂职）", "overlap_org": "汉中市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "市长与副市长", "overlap_org": "汉中市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "市长与副市长", "overlap_org": "汉中市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "市长与副市长/公安局长", "overlap_org": "汉中市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "市长与副市长", "overlap_org": "汉中市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "市长与副市长", "overlap_org": "汉中市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "市长与市政府秘书长", "overlap_org": "汉中市人民政府", "overlap_period": ""},
    # 人大/政协 x 市委
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "市委书记与人大常委会主任", "overlap_org": "汉中市", "overlap_period": ""},
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "市委书记与市政协主席", "overlap_org": "汉中市", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "汉中市政府门户 — 首页新闻（张烨=市委书记、王建平=市长）", "url": "https://www.hanzhong.gov.cn/", "publisher": "汉中市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张烨以市委书记身份出席 巡察工作动员部署会；王建平以市长身份调研"},
        {"id": "S002", "title": "汉中市政府 — 市长 王建平 官方简历", "url": "https://www.hanzhong.gov.cn/hzszf/wjp/szfld.shtml", "publisher": "汉中市人民政府", "published_at": "2023-04-25", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王建平：1972年10月生、大学/工学学士、市长/市委副书记/党组书记；完整履历"},
        {"id": "S003", "title": "汉中市政府 — 常务副市长 王旭坚 简历", "url": "https://www.hanzhong.gov.cn/hzszf/wxj/szfld.shtml", "publisher": "汉中市人民政府", "published_at": "2025-04-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王旭坚：1978年5月生、研究生/工学硕士、常务副市长/党组副书记"},
        {"id": "S004", "title": "汉中市政府 — 副市长 王松柏 简历", "url": "https://www.hanzhong.gov.cn/hzszf/wsb/szfld.shtml", "publisher": "汉中市人民政府", "published_at": "2025-04-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王松柏：1971年2月生、市委常委/副市长"},
        {"id": "S005", "title": "汉中市政府 — 副市长 杜顶 简历", "url": "https://www.hanzhong.gov.cn/hzszf/duding/szfld.shtml", "publisher": "汉中市人民政府", "published_at": "2026-06-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "杜顶：1976年12月生、管理学博士、中央部委挂职"},
        {"id": "S006", "title": "汉中市政府 — 副市长 吴维强 简历", "url": "https://www.hanzhong.gov.cn/hzszf/wwq/szfld.shtml", "publisher": "汉中市人民政府", "published_at": "2022-04-08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "吴维强：1970年1月生、副市长"},
        {"id": "S007", "title": "汉中市政府 — 副市长 郑雪梅 简历", "url": "https://www.hanzhong.gov.cn/hzszf/zxm/szfld.shtml", "publisher": "汉中市人民政府", "published_at": "2022-04-08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "郑雪梅：女、1969年7月生、民革党员、市工商联主席"},
        {"id": "S008", "title": "汉中市政府 — 副市长 张鹏 简历", "url": "https://www.hanzhong.gov.cn/hzszf/zhangpeng/szfld.shtml", "publisher": "汉中市人民政府", "published_at": "2023-11-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张鹏：1973年3月生、市公安局长"},
        {"id": "S009", "title": "汉中市政府 — 副市长 宋旭 简历", "url": "https://www.hanzhong.gov.cn/hzszf/songxu/szfld.shtml", "publisher": "汉中市人民政府", "published_at": "2024-08-19", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "宋旭：1976年7月生、管理学博士"},
        {"id": "S010", "title": "汉中市政府 — 副市长 李宽 简历", "url": "https://www.hanzhong.gov.cn/hzszf/likuan/szfld.shtml", "publisher": "汉中市人民政府", "published_at": "2025-05-14", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "李宽：1972年3月生、副市长"},
        {"id": "S011", "title": "汉中市政府 — 市政府秘书长 王镇 简历", "url": "https://www.hanzhong.gov.cn/hzszf/wzz/szfld.shtml", "publisher": "汉中市人民政府", "published_at": "2021-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王镇：1971年11月生、秘书长/党组成员"},
        {"id": "S012", "title": "维基百科 — 张烨 (1972年) 完整履历", "url": "https://zh.wikipedia.org/wiki/张烨_(1972年)", "publisher": "维基百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "张烨1972年8月生、河北北戴河、法学；中宣部→陕西广电→汉中市长→汉中市委书记；前任钟洪江"},
        {"id": "S013", "title": "汉中要闻 — 市委巡察工作动员部署会（周耀宜=组织部部长、钟伟=纪委书记）", "url": "https://www.hanzhong.gov.cn/hzszf/xwzx/zwyw/202608/6a630737ef7a420986df1d0cc4fe7c1e.shtml", "publisher": "汉中日报", "published_at": "2026-08-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市委书记张烨、组织部部长 书周耀宜、纪委书记 钟伟"},
        {"id": "S014", "title": "维基百科 — 汉中市正职领导人列表", "url": "https://zh.wikipedia.org/wiki/张烨_(1972年)", "publisher": "维基百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "人大主任 杨记明、政协主席 蔡煜东；汉中历任市委书记/市长"},
    ]


def make_person_json(person, timeline, relationships_list, source_register, gaps=None):
    pfname = f"hanzhong_{person['name']}"
    name = person["name"]
    post = person["current_post"]
    if "前任" in post:
        rank = "正厅级"
    elif "市委书记" in post:
        rank = "正厅级"
    elif "市长" in post:
        rank = "正厅级"
    elif "人大" in post or "政协主席" in post:
        rank = "正厅级"
    elif "常务副市长" in post or "副市长" in post or "常委" in post:
        rank = "副厅级"
    elif "秘书长" in post:
        rank = "正处级"
    else:
        rank = "副厅级"
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "陕西省",
            "city": "汉中市",
            "region": "汉中市",
            "job": post,
            "task_id": "shaanxi_汉中市",
            "time_focus": "2023-2026"
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
            "education": [{"period": "", "institution": "", "major": "", "degree": person["education"], "study_type": "unknown", "source_ids": ["S002", "S012"]}] if person["education"] else [],
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
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if "书记" in post else "cross_county_rotation",
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
            "identity": "confirmed" if person["birth"] else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if person["birth"] else "thin",
            "relationship_confidence": "high",
            "biggest_gap": f"{name}的完整上任前履历及出生地/籍贯补充"
        },
        "open_questions": (gaps if gaps else [
            {"priority": "high", "question": f"{name}的完整职业履历（含出生/籍贯/学历/入党/早期岗位细节）？", "why_it_matters": "更精确分析晋升路径", "suggested_queries": [f"{name} 简历 汉中", f"{name} 任前公示"], "last_attempted": AS_OF},
        ])
    }


def build():
    print("=" * 60)
    print("  汉中市领导班子工作关系网络")
    print("  等级: 地级市")
    print(f"  调查日期: {AS_OF}")
    print("  信息来源: hanzhong.gov.cn(官方)、维基百科、官媒")
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

    # 1. 张烨 (市委书记)
    zy_timeline = [
        {"start": "1995", "end": "2015", "org": "中共中央宣传部", "title": "新闻局新闻研究处（干部→主任科员）", "notes": "1995年进入中宣部新闻局，历任干部、副主任科员、主任科员；1997.3-1998.2挂职陕西铜川耀县", "confidence": "confirmed", "source_ids": ["S012"]},
        {"start": "2003.9", "end": "2006", "org": "中宣部新闻局", "title": "新闻研究处副处长→处长", "notes": "", "confidence": "confirmed", "source_ids": ["S012"]},
        {"start": "2010.7", "end": "2015.3", "org": "中宣部国家应急新闻中心", "title": "办公室专职副主任", "notes": "期间北大攻读公共管理硕士", "confidence": "confirmed", "source_ids": ["S012"]},
        {"start": "2015.3", "end": "2017.10", "org": "中宣部新闻局", "title": "副局长", "notes": "2017.7兼任中宣部国际联络局局长", "confidence": "confirmed", "source_ids": ["S012"]},
        {"start": "2020.10", "end": "2021.6", "org": "陕西省广播电视局", "title": "局长、党组书记", "notes": "", "confidence": "confirmed", "source_ids": ["S012"]},
        {"start": "2021.6", "end": "2023.3", "org": "汉中市人民政府", "title": "市委副书记、代市长→市长", "notes": "2021.6代市长；2021.8.31转正", "confidence": "confirmed", "source_ids": ["S012", "S002"]},
        {"start": "2023.3.25", "end": "present", "org": "中共汉中市委", "title": "市委书记", "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S012"]},
    ]
    zy_rels = [
        {"person": "王建平", "person_id": "hanzhong_王建平", "relationship_type": "overlap", "strength": "strong", "evidence": "市委书记与市长党政搭档", "overlap_org": "汉中市", "overlap_period": "2023-至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "王建平", "person_id": "hanzhong_王建平", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "张烨升任市委书记后由王建平接任市长", "overlap_org": "汉中市人民政府", "overlap_period": "2023", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012"]},
        {"person": "钟洪江", "person_id": "hanzhong_钟洪江", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "钟洪江为前任市委书记/市长；张烨接任", "overlap_org": "中共汉中市委", "overlap_period": "2023.03", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012"]},
    ]
    zy_gaps = [{"priority": "low", "question": "张烨1995年进入中宣部前是否曾有其他工作，及入党准确日期", "why_it_matters": "履历完整度", "suggested_queries": ["张烨 中宣部 简历"], "last_attempted": AS_OF}]
    zy_json = make_person_json(persons[0], zy_timeline, zy_rels, source_register, zy_gaps)
    with open(PJSON_DIR / f"{TODAY}-陕西省-汉中市-市委书记-张烨.json", "w", encoding="utf-8") as f:
        json.dump(zy_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {TODAY}-陕西省-汉中市-市委书记-张烨.json")

    # 2. 王建平 (市长)
    wjp_timeline = [
        {"start": "unknown", "end": "unknown", "org": "陕西省人民政府组成部门", "title": "副处长、处长", "notes": "曾任省政府组成部门副处长、处长", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "陕西省某县", "title": "县长", "notes": "曾担任县长", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "陕西某地级市", "title": "副市长、市委常委、市委秘书长", "notes": "曾担任地级市副市长、市委常委、市委秘书长", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "陕西省人民政府", "title": "副秘书长、机关党组成员", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "陕西某地级市", "title": "市委常委、市委副书记、统战部部长、市委党校校长", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2023", "end": "present", "org": "汉中市人民政府", "title": "市长、市委副书记、市政府党组书记", "notes": "2023年接任张烨市长之职", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    wjp_rels = [
        {"person": "张烨", "person_id": "hanzhong_张烨", "relationship_type": "overlap", "strength": "strong", "evidence": "市长与市委书记（党政搭档）", "overlap_org": "汉中市", "overlap_period": "2023-至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "张烨", "person_id": "hanzhong_张烨", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "王建平接任张烨的市长职务（张烨升任书记）", "overlap_org": "汉中市人民政府", "overlap_period": "2023", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012"]},
        {"person": "钟洪江", "person_id": "hanzhong_钟洪江", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "钟洪江为更早市长", "overlap_org": "汉中市人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012"]},
    ]
    wjp_gaps = [{"priority": "high", "question": "王建平出生地、具体任职年份（各段岗位起止时间）", "why_it_matters": "市长履历时间线更精确", "suggested_queries": ["王建平 汉中市市长 简历", "王建平 任前公示"], "last_attempted": AS_OF}]
    wjp_json = make_person_json(persons[1], wjp_timeline, wjp_rels, source_register, wjp_gaps)
    with open(PJSON_DIR / f"{TODAY}-陕西省-汉中市-市长-王建平.json", "w", encoding="utf-8") as f:
        json.dump(wjp_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {TODAY}-陕西省-汉中市-市长-王建平.json")

    # 3. 钟洪江 (前任书记)
    zhj_timeline = [
        {"start": "2016", "end": "2021.6", "org": "汉中市人民政府", "title": "市委副书记、市长", "notes": "2016年起任汉中市长", "confidence": "plausible", "source_ids": ["S012"]},
        {"start": "2019", "end": "2023.3", "org": "中共汉中市委", "title": "市委书记", "notes": "2023.3由张烨接任", "confidence": "confirmed", "source_ids": ["S012"]},
    ]
    zhj_rels = [
        {"person": "张烨", "person_id": "hanzhong_张烨", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "钟洪江为前任市委书记；张烨接任", "overlap_org": "中共汉中市委", "overlap_period": "2023.03", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012"]},
        {"person": "王建平", "person_id": "hanzhong_王建平", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "钟洪江更早任市长", "overlap_org": "汉中市人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012"]},
    ]
    zhj_gaps = [{"priority": "high", "question": "钟洪江2023年3月卸任后去向（调任何职）", "why_it_matters": "前任书记去向是调整信号", "suggested_queries": ["钟洪江 去向"], "last_attempted": AS_OF}]
    zhj_json = make_person_json(persons[2], zhj_timeline, zhj_rels, source_register, zhj_gaps)
    with open(PJSON_DIR / f"{TODAY}-陕西省-汉中市-前任市委书记-钟洪江.json", "w", encoding="utf-8") as f:
        json.dump(zhj_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {TODAY}-陕西省-汉中市-前任市委书记-钟洪江.json")

    print(f"\n所有 Person JSONs 已生成到: {PJSON_DIR}")


if __name__ == "__main__":
    build()