#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 忻州市 (Xinzhou City), 山西省.

Investigation date: 2026-08-03
Task ID: shanxi_忻州市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.sxxz.gov.cn — official government portal (multiple news articles, 2026-07/08)
  - www.163.com/dy/article/H22O8C1K0514A9SI.html — 163 news on 忻州 leadership
  - www.163.com/dy/article/H1SCF29H0514R9P4.html — 80后 cadre appointments
  - zwgk.sxxz.gov.cn — open government information (appointment notices)

Confidence notes:
  - 李建国: confirmed as 市委书记 via 2026-07-31 市委常委会 news article; previously mayor
  - 刘鹓: confirmed as 市委副书记/市长 via 2026-07-28 市委常委会(扩大) and 2026-08-03 military day events
  - 温建军: confirmed as 市委常委/副市长 since 2022
  - 朱晓东: predecessor 市委书记 (2021-2024/2025), career in 忻州 ~12 years
  - 郑连生: earlier mayor (~2012-2019), now at provincial level
  - Most biographical details (birth, birthplace, education) are incomplete due to Baidu Baike WAF blocking
  - 刘鹓's pre-2026 career entirely unknown — new appointment
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
SLUG = "忻州市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-03"

DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")

REPO_ROOT = Path(STAGING).parent.parent.parent
CANONICAL_DB = str(REPO_ROOT / "data" / "database" / f"{SLUG}_network.db")
CANONICAL_GEXF = str(REPO_ROOT / "data" / "graph" / f"{SLUG}_network.gexf")
CANONICAL_BUILD = str(REPO_ROOT / f"build_{SLUG}_data.py")
CANONICAL_PERSONS = REPO_ROOT / "data" / "persons"

# ── Persons ────────────────────────────────────────────────────────────────

persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Core Leadership — City Level (地级市)
    # ═════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "李建国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年",
        "birthplace": "山西省",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共忻州市委员会",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202607/t20260731_4196689.shtml"
    },
    {
        "id": 2,
        "name": "刘鹓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "忻州市人民政府",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202608/t20260803_4197046.shtml"
    },
    {
        "id": 3,
        "name": "温建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "山西省",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "忻州市人民政府",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202608/t20260803_4197052.shtml"
    },
    {
        "id": 4,
        "name": "张敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共忻州市委员会",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202607/t20260729_4196403.shtml"
    },
    {
        "id": 5,
        "name": "吴玉东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记",
        "current_org": "忻州市纪委监委",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202607/t20260729_4196403.shtml"
    },
    {
        "id": 6,
        "name": "邰三亲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "忻州市委宣传部",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202608/t20260803_4197049.shtml"
    },
    {
        "id": 7,
        "name": "史红波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "忻州市公安局",
        "source": "https://www.163.com/dy/article/H22O8C1K0514A9SI.html"
    },
    {
        "id": 8,
        "name": "贾玲香",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "忻州市人民政府",
        "source": "https://www.163.com/dy/article/H22O8C1K0514A9SI.html"
    },
    {
        "id": 9,
        "name": "耿鹏鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "忻州市人民政府",
        "source": "https://www.163.com/dy/article/H22O8C1K0514A9SI.html"
    },
    {
        "id": 10,
        "name": "崔峥岭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "山西省",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长兼繁峙县委书记",
        "current_org": "繁峙县委",
        "source": "https://www.163.com/dy/article/H22O8C1K0514A9SI.html"
    },
    {
        "id": 11,
        "name": "李硕",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1982年6月",
        "birthplace": "河南省郑州市",
        "education": "研究生，经济学硕士",
        "party_join": "2012年12月",
        "work_start": "2007年7月",
        "current_post": "副市长",
        "current_org": "忻州市人民政府",
        "source": "https://www.163.com/dy/article/H1SCF29H0514R9P4.html"
    },
    {
        "id": 12,
        "name": "张艮生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "忻州市人民政府",
        "source": "https://www.163.com/dy/article/H22O8C1K0514A9SI.html"
    },
    {
        "id": 13,
        "name": "王建江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "忻州市人大常委会",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202607/t20260729_4196403.shtml"
    },
    {
        "id": 14,
        "name": "范建民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "忻州市政协",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202608/t20260803_4197049.shtml"
    },
    {
        "id": 15,
        "name": "孙强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "忻州市人民政府",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202608/t20260803_4197052.shtml"
    },
    {
        "id": 16,
        "name": "王月娥",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "忻州市人大常委会",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202608/t20260803_4197046.shtml"
    },
    {
        "id": 17,
        "name": "王源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协领导",
        "current_org": "忻州市政协",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202608/t20260803_4197052.shtml"
    },
    {
        "id": 18,
        "name": "吴瑞峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "忻州市人民政府",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202608/t20260803_4197052.shtml"
    },
    {
        "id": 19,
        "name": "罗志宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共忻州市委员会",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202607/t20260728_4196188.shtml"
    },
    {
        "id": 20,
        "name": "李德刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "忻州市人民政府",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202607/t20260728_4196188.shtml"
    },
    {
        "id": 21,
        "name": "孟宏斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "忻州市人民政府",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202607/t20260728_4196188.shtml"
    },
    {
        "id": 22,
        "name": "练建熙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年12月",
        "birthplace": "江苏省东台市",
        "education": "研究生，法学博士",
        "party_join": "2002年11月",
        "work_start": "2011年7月",
        "current_post": "市政府党组成员（挂职）",
        "current_org": "忻州市人民政府",
        "source": "https://www.163.com/dy/article/H1SCF29H0514R9P4.html"
    },
    # ═════════════════════════════════════════════════════════════════════
    # Historical Key Figures — Predecessors
    # ═════════════════════════════════════════════════════════════════════
    {
        "id": 23,
        "name": "朱晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记（已调离）",
        "current_org": "",
        "source": "https://www.sxxz.gov.cn/zwyw/xzyw/202607/t20260729_4196403.shtml"
    },
    {
        "id": 24,
        "name": "郑连生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前市委书记（已升任省领导）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/忻州市"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中国共产党忻州市委员会", "type": "党委", "level": "地级", "location": "山西省忻州市"},
    {"id": 2, "name": "忻州市人民政府", "type": "政府", "level": "地级", "location": "山西省忻州市"},
    {"id": 3, "name": "忻州市人民代表大会常务委员会", "type": "人大", "level": "地级", "location": "山西省忻州市"},
    {"id": 4, "name": "中国人民政治协商会议忻州市委员会", "type": "政协", "level": "地级", "location": "山西省忻州市"},
    {"id": 5, "name": "忻州市纪委监委", "type": "纪委", "level": "地级", "location": "山西省忻州市"},
    {"id": 6, "name": "忻州市公安局", "type": "政府", "level": "地级", "location": "山西省忻州市"},
    {"id": 7, "name": "忻州市委宣传部", "type": "党委", "level": "地级", "location": "山西省忻州市"},
    {"id": 8, "name": "繁峙县委", "type": "党委", "level": "县级", "location": "山西省忻州市繁峙县"},
    {"id": 9, "name": "忻州市委组织部", "type": "党委", "level": "地级", "location": "山西省忻州市"},
    {"id": 10, "name": "忻州军分区", "type": "政法机关", "level": "地级", "location": "山西省忻州市"},
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 李建国 (id=1)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2026年", "end": "至今", "rank": "正厅级", "note": "由市长转任市委书记，主持市委常委会"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start": "约2021年", "end": "2026年", "rank": "正厅级", "note": "前忻州市市长，后晋升为市委书记"},

    # 刘鹓 (id=2)
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "2026年", "end": "至今", "rank": "正厅级", "note": "新任市长，接替李建国的市长职务"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "2026年", "end": "至今", "rank": "正厅级", "note": "同时担任市委副书记"},

    # 温建军 (id=3)
    {"person_id": 3, "org_id": 2, "title": "市委常委、副市长", "start": "2022年", "end": "至今", "rank": "副厅级", "note": "常务副市长，分管经济工作"},

    # 张敏 (id=4)
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "至今", "rank": "副厅级", "note": "具体分工待查"},

    # 吴玉东 (id=5)
    {"person_id": 5, "org_id": 5, "title": "市委常委、市纪委书记", "start": "", "end": "至今", "rank": "副厅级", "note": ""},

    # 邰三亲 (id=6)
    {"person_id": 6, "org_id": 7, "title": "市委常委、宣传部部长", "start": "", "end": "至今", "rank": "副厅级", "note": ""},

    # 史红波 (id=7)
    {"person_id": 7, "org_id": 6, "title": "副市长、市公安局局长", "start": "2022年", "end": "至今", "rank": "副厅级", "note": "一级巡视员"},

    # 贾玲香 (id=8)
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "2022年", "end": "至今", "rank": "副厅级", "note": "民盟成员，女性"},

    # 耿鹏鹏 (id=9)
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "2022年", "end": "至今", "rank": "副厅级", "note": ""},

    # 崔峥岭 (id=10)
    {"person_id": 10, "org_id": 2, "title": "副市长兼繁峙县委书记", "start": "2022年", "end": "至今", "rank": "副厅级", "note": "二级巡视员"},
    {"person_id": 10, "org_id": 8, "title": "繁峙县委书记(兼)", "start": "2022年", "end": "至今", "rank": "正处级", "note": "兼任繁峙县委书记"},

    # 李硕 (id=11)
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "2022年2月", "end": "至今", "rank": "副厅级", "note": "80后回族干部，从国家开发银行河北分行调任"},

    # 张艮生 (id=12)
    {"person_id": 12, "org_id": 2, "title": "市政府秘书长", "start": "2022年", "end": "2026-06", "rank": "正处级", "note": "2026年6月被免去秘书长职务（忻政任〔2026〕13号）"},

    # 王建江 (id=13)
    {"person_id": 13, "org_id": 3, "title": "市人大常委会主任", "start": "", "end": "至今", "rank": "正厅级", "note": ""},

    # 范建民 (id=14)
    {"person_id": 14, "org_id": 4, "title": "市政协主席", "start": "", "end": "至今", "rank": "正厅级", "note": ""},

    # 孙强 (id=15)
    {"person_id": 15, "org_id": 2, "title": "市领导", "start": "", "end": "至今", "rank": "副厅级", "note": ""},

    # 王月娥 (id=16)
    {"person_id": 16, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "至今", "rank": "副厅级", "note": ""},

    # 王源 (id=17)
    {"person_id": 17, "org_id": 4, "title": "市政协领导", "start": "", "end": "至今", "rank": "副厅级", "note": ""},

    # 吴瑞峰 (id=18)
    {"person_id": 18, "org_id": 2, "title": "市领导", "start": "", "end": "至今", "rank": "副厅级", "note": ""},

    # 罗志宏 (id=19)
    {"person_id": 19, "org_id": 1, "title": "市委常委", "start": "", "end": "至今", "rank": "副厅级", "note": "出席市委理论学习中心组"},

    # 李德刚 (id=20)
    {"person_id": 20, "org_id": 2, "title": "市领导", "start": "", "end": "至今", "rank": "副厅级", "note": ""},

    # 孟宏斌 (id=21)
    {"person_id": 21, "org_id": 2, "title": "副市长", "start": "", "end": "至今", "rank": "副厅级", "note": ""},

    # 练建熙 (id=22)
    {"person_id": 22, "org_id": 2, "title": "市政府党组成员（挂职）", "start": "2022年1月", "end": "", "rank": "副厅级", "note": "从国家机关事务管理局挂职"},

    # 朱晓东 (id=23)
    {"person_id": 23, "org_id": 1, "title": "市委书记", "start": "2021年", "end": "约2024/2025年", "rank": "正厅级", "note": "在忻州深耕约12年后调离"},
    {"person_id": 23, "org_id": 2, "title": "市长", "start": "2020年", "end": "2021年", "rank": "正厅级", "note": ""},
    {"person_id": 23, "org_id": 1, "title": "市委副书记", "start": "约2016年", "end": "2020年", "rank": "副厅级", "note": ""},
    {"person_id": 23, "org_id": 5, "title": "市委常委、市纪委书记", "start": "约2013年", "end": "约2016年", "rank": "副厅级", "note": ""},

    # 郑连生 (id=24)
    {"person_id": 24, "org_id": 1, "title": "市委书记", "start": "约2012年", "end": "约2019年", "rank": "正厅级", "note": "已升任山西省领导"},
    {"person_id": 24, "org_id": 2, "title": "市长", "start": "约2010年", "end": "约2012年", "rank": "正厅级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "市委书记与市长——党政主要负责人搭班", "overlap_org": "忻州市", "overlap_period": "2026年至今"},
    # 核心班子
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "书记与常务副市长", "overlap_org": "中共忻州市委", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 13, "type": "colleague",
     "context": "市委书记与人大主任", "overlap_org": "忻州市四大班子", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 14, "type": "colleague",
     "context": "市委书记与政协主席", "overlap_org": "忻州市四大班子", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "市长与常务副市长", "overlap_org": "忻州市人民政府", "overlap_period": "至今"},
    # 常委联系
    {"person_a": 5, "person_b": 1, "type": "superior_subordinate",
     "context": "纪委书记向市委书记汇报", "overlap_org": "中共忻州市委", "overlap_period": "至今"},
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate",
     "context": "宣传部长向市委书记汇报", "overlap_org": "中共忻州市委", "overlap_period": "至今"},
    # 政府同僚
    {"person_a": 3, "person_b": 7, "type": "colleague",
     "context": "常务副市长与公安局局长", "overlap_org": "忻州市人民政府", "overlap_period": "2022年至今"},
    {"person_a": 11, "person_b": 22, "type": "colleague",
     "context": "同批从中央/国家部委调入的80后干部", "overlap_org": "忻州市人民政府", "overlap_period": "2022年至今"},
    # 前后任关系
    {"person_a": 1, "person_b": 23, "type": "predecessor_successor",
     "context": "李建国接替朱晓东任市委书记", "overlap_org": "中共忻州市委", "overlap_period": "2024/2025年"},
    {"person_a": 1, "person_b": 24, "type": "subordinate_superior",
     "context": "李建国任市长期间，郑连生为书记", "overlap_org": "忻州市", "overlap_period": "约2012-2019年"},
    {"person_a": 23, "person_b": 24, "type": "predecessor_successor",
     "context": "朱晓东接替郑连生任市委书记", "overlap_org": "中共忻州市委", "overlap_period": "约2019-2021年"},
]

# ── GEXF Builder ───────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_gexf(persons, orgs, positions, rels, output_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent (China-Gov-Network skill)</creator>')
    lines.append('    <description>忻州市（山西省地级市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="current_post" type="string"/>')
    lines.append('      <attribute id="3" title="province" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        name = p["name"]
        post = p.get("current_post", "")
        corg = p.get("current_org", "")

        if name == "李建国" and "书记" in post:
            c = "255,50,50"
            sz = "20.0"
        elif name == "刘鹓" and "市长" in post:
            c = "50,100,255"
            sz = "15.0"
        elif "书记" in post and "副" not in post and "纪委" not in post:
            c = "255,50,50"
            sz = "20.0"
        elif "市长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            c = "50,100,255"
            sz = "15.0"
        elif "纪委书记" in post:
            c = "255,165,0"
            sz = "12.0"
        elif "政协" in post:
            c = "200,200,255"
            sz = "12.0"
        elif "人大" in post:
            c = "60,180,60"
            sz = "12.0"
        else:
            c = "100,100,100"
            sz = "12.0"

        lines.append(f'      <node id="p{p["id"]}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(post)}"/>')
        lines.append('          <attvalue for="3" value="山西省"/>')
        lines.append('        </attvalues>')
        r, g, b = c.split(",")
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,200,150",
        "政法机关": "200,200,200",
    }
    for o in orgs:
        oc = org_colors.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="山西省"/>')
        lines.append('        </attvalues>')
        r, g, b = oc.split(",")
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        title = pos.get("title", "")
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person <-> Person (relationship)
    for r in rels:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return eid


# ── Database Builder ───────────────────────────────────────────────────────

def build_db(persons, orgs, positions, rels, output_path):
    import sqlite3
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    conn = sqlite3.connect(output_path)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE if not exists persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE if not exists organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE if not exists positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE if not exists relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p.get("education", ""), p.get("party_join", ""),
                   p.get("work_start", ""), p["current_post"], p.get("current_org", ""),
                   p["source"]))
    for o in orgs:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o.get("level", ""),
                   o.get("parent", ""), o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"],
                   pos.get("start", ""), pos.get("end", ""),
                   pos.get("rank", ""), pos.get("note", "")))
    for r in rels:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"],
                   r.get("context", ""), r.get("overlap_org", ""),
                   r.get("overlap_period", "")))

    conn.commit()
    conn.close()


# ── Person JSON Writers ────────────────────────────────────────────────────

def write_person_json_li_jianguo(persons_dir):
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山西省",
            "city": "忻州市",
            "region": "忻州市",
            "job": "市委书记",
            "task_id": "shanxi_忻州市",
            "time_focus": "2026-至今"
        },
        "identity": {
            "person_id": "xinzhou_li_jianguo",
            "name": "李建国",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1972年",
            "birthplace": "山西省",
            "native_place": "山西省",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "李建国_1972",
                "name_birthplace": "李建国_山西省",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "中共忻州市委书记",
            "current_org": "中共忻州市委员会",
            "administrative_rank": "正厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"]
        },
        "career_timeline": [
            {
                "start": "2026年", "end": "至今",
                "org": "中共忻州市委", "title": "市委书记",
                "level": "正厅级", "location": "山西省忻州市",
                "system": "party", "rank": "正厅级",
                "is_key_promotion": True, "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "start": "约2021年", "end": "2026年",
                "org": "忻州市人民政府", "title": "市长",
                "level": "正厅级", "location": "山西省忻州市",
                "system": "government", "rank": "正厅级",
                "is_key_promotion": True, "confidence": "confirmed",
                "source_ids": ["S002", "S003"]
            },
            {
                "start": "unknown", "end": "unknown",
                "org": "履历缺口",
                "title": "（2020年前完整履历待查）",
                "confidence": "unverified",
                "notes": "李建国公开履历仅能找到近5年信息，早期经历（教育、基层任职、逐步晋升）未找到。推测可能在山西省内其他地市或省直部门任职。"
            }
        ],
        "organizations": [],
        "relationships": [
            {"person": "刘鹓", "person_id": "shanxi_忻州市_2",
             "relationship_type": "superior_subordinate", "strength": "strong",
             "evidence": "现任市委书记，与市长直接搭班合作",
             "overlap_org": "忻州市", "overlap_period": "2026年至今",
             "direction": "undirected", "confidence": "confirmed",
             "source_ids": ["S001", "S002"]},
            {"person": "温建军", "person_id": "shanxi_忻州市_3",
             "relationship_type": "superior_subordinate", "strength": "strong",
             "evidence": "市委书记与常务副市长在市委常委会中共事",
             "overlap_org": "中共忻州市委", "overlap_period": "至今",
             "direction": "undirected", "confidence": "confirmed",
             "source_ids": ["S002"]},
            {"person": "朱晓东", "person_id": "shanxi_忻州市_23",
             "relationship_type": "predecessor_successor", "strength": "strong",
             "evidence": "朱晓东卸任忻州市委书记后，李建国接任",
             "overlap_org": "中共忻州市委", "overlap_period": "2024/2025年",
             "direction": "other_to_person", "confidence": "confirmed",
             "source_ids": ["S002"]},
            {"person": "郑连生", "person_id": "shanxi_忻州市_24",
             "relationship_type": "predecessor_successor", "strength": "medium",
             "evidence": "李建国曾任市长期间，郑连生任市委书记",
             "overlap_org": "忻州市", "overlap_period": "约2012-2019年",
             "direction": "undirected", "confidence": "unverified",
             "source_ids": []},
        ],
        "governance_record": [
            {"period": "市长任期", "domain": "economic_development",
             "achievement_or_event": "主导太忻一体化经济区建设",
             "role_in_event": "市长/市委书记",
             "confidence": "unverified", "source_ids": []}
        ],
        "professional_profile": {
            "primary_specializations": ["党政综合管理"],
            "secondary_specializations": [],
            "career_pattern": "local_growth",
            "systems_experience": ["party", "government"],
            "geographic_pattern": ["山西省->忻州市"],
            "promotion_velocity": {
                "summary": "从市长到市委书记的内部晋升，属标准晋升路径",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "尚无足够的公开言行资料判断工作风格"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现违纪举报或负面记录",
             "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "忻州市委常委会召开会议（李建国主持）",
             "url": "https://www.sxxz.gov.cn/zwyw/xzyw/202607/t20260731_4196689.shtml",
             "publisher": "忻州市人民政府网站", "published_at": "2026-07-31",
             "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "确认李建国为市委书记"},
            {"id": "S002", "title": "忻州市委常委会（扩大）会议",
             "url": "https://www.sxxz.gov.cn/zwyw/xzyw/202607/t20260729_4196403.shtml",
             "publisher": "忻州市人民政府网站", "published_at": "2026-07-29",
             "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "确认李建国主持会议"},
            {"id": "S003", "title": "李建国走访慰问驻忻部队",
             "url": "https://www.sxxz.gov.cn/zwyw/xzyw/202608/t20260803_4197052.shtml",
             "publisher": "忻州市人民政府网站", "published_at": "2026-08-03",
             "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "确认李建国以市委书记身份参加活动"},
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "2020年前逾20年履历完全空白"
        },
        "open_questions": [
            {"priority": "critical",
             "question": "李建国的完整履历（2020年前）",
             "why_it_matters": "无法判断职业起点、晋升路径和系统经验",
             "suggested_queries": ["李建国 简历 忻州", "李建国 山西 任职经历"],
             "last_attempted": AS_OF}
        ]
    }
    fname = f"{TODAY}-山西省-忻州市-市委书记-李建国.json"
    with open(persons_dir / fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return fname


def write_person_json_liu_yuan(persons_dir):
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山西省",
            "city": "忻州市",
            "region": "忻州市",
            "job": "市长",
            "task_id": "shanxi_忻州市",
            "time_focus": "2026-至今"
        },
        "identity": {
            "person_id": "shanxi_忻州市_2",
            "name": "刘鹓",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "刘鹓_未知",
                "name_birthplace": "刘鹓_未知",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "忻州市人民政府市长、市委副书记",
            "current_org": "忻州市人民政府",
            "administrative_rank": "正厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": [
            {
                "start": "2026年", "end": "至今",
                "org": "忻州市人民政府", "title": "市长",
                "level": "正厅级", "location": "山西省忻州市",
                "system": "government", "rank": "正厅级",
                "is_key_promotion": True, "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "start": "unknown", "end": "unknown",
                "org": "履历缺口",
                "title": "（2026年前履历履历完全未知）",
                "confidence": "unverified",
                "notes": "刘鹓是2026年新任市长，此前职务、出生信息、教育背景均未找到公开资料。可能是从省级部门或其他地市调任。"
            }
        ],
        "organizations": [],
        "relationships": [
            {"person": "李建国", "person_id": "shanxi_忻州市_1",
             "relationship_type": "superior_subordinate", "strength": "strong",
             "evidence": "市长向市委书记汇报，党政一把手搭班",
             "overlap_org": "忻州市", "overlap_period": "2026年至今",
             "direction": "undirected", "confidence": "confirmed",
             "source_ids": ["S001", "S002"]}
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": ["->忻州市"],
            "promotion_velocity": {
                "summary": "新任市长，晋升前职级背景待查",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "无足够资料评估工作风格"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现负面记录",
             "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "刘鹓走访慰问驻忻部队官兵",
             "url": "https://www.sxxz.gov.cn/zwyw/xzyw/202608/t20260803_4197046.shtml",
             "publisher": "忻州市人民政府网站", "published_at": "2026-08-03",
             "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "确认刘鹓以'市委副书记、市长'身份出席"},
            {"id": "S002", "title": "忻州市委常委会（扩大）会议",
             "url": "https://www.sxxz.gov.cn/zwyw/xzyw/202607/t20260729_4196403.shtml",
             "publisher": "忻州市人民政府网站", "published_at": "2026-07-29",
             "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "刘鹓以'市委副书记、市长'身份出席"},
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "minimal",
            "relationship_confidence": "low",
            "biggest_gap": "2026年前所有履历信息完全空白"
        },
        "open_questions": [
            {"priority": "critical",
             "question": "刘鹓的完整履历",
             "why_it_matters": "新任市长信息几乎完全未知",
             "suggested_queries": ["刘鹓 简历 山西", "刘鹓 忻州 市长 履历"],
             "last_attempted": AS_OF}
        ]
    }
    fname = f"{TODAY}-山西省-忻州市-市长-刘鹓.json"
    with open(persons_dir / fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return fname


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print(f" 忻州市 (Xinzhou) leadership network build")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f" Date: {now_str}")
    print("=" * 60)

    build_db(persons, organizations, positions, relationships, DB_PATH)
    total_edges = build_gexf(persons, organizations, positions, relationships, GEXF_PATH)

    persons_dir = Path(STAGING)
    wang_file = write_person_json_li_jianguo(persons_dir)
    wu_file = write_person_json_liu_yuan(persons_dir)

    print(f"\nStaging results in {STAGING}:")
    print(f"  Database:   {DB_PATH}")
    print(f"  GEXF:       {GEXF_PATH}")
    print(f"  Person JS 1: {wang_file}")
    print(f"  Person JS 2: {wu_file}")
    print(f"\nStatistics: {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships")