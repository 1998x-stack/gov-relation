#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 民权县 (Minquan County), 商丘市, 河南省.

Investigation date: 2026-08-06
Task ID: henan_民权县
Level: 县
Targets: 县委书记 & 县长

Research sources (confirmed):
  - 民权网 www.cnmq.com.cn (official 县委/县政府 news):
    * 2026-03-05 县委书记王静娴调研省市重点项目建设 (http://www.cnmq.com.cn/news/mqyw/44107.html)
    * 2026-02-27 中共民权县第十三届委员会常委会第154次会议 (http://www.cnmq.com.cn/news/mqyw/44101.html)
    * 2026-03-12 四大家领导开展春季义务植树 (县委书记王静娴、县长王景义) (http://www.cnmq.com.cn/news/mqyw/44125.html)
    * 2026-04-03 人大常委第36次会议 (张爱军/李晓彬/李卫政/王晓敏列席) (http://www.cnmq.com.cn/news/mqyw/44240.html)
    * 2026-05-25 县长王景义调研文旅项目 (http://www.cnmq.com.cn/news/mqyw/44466.html)
    * 2026-03-13 国土空间规划委员会 (王静娴主持, 王景义/陈鸿志等) (http://www.cnmq.com.cn/news/mqyw/44132.html)
    * 2026-01-23 常委会第151次会议 (王静娴主持) (http://www.cnmq.com.cn/news/mqyw/43881.html)
    * 2026-03-18 政府第64次常务会议 (王景义主持) (http://www.cnmq.com.cn/news/mqyw/44142.html)
    * 2026-03-25 县长王景义调度群腐整治 (http://www.cnmq.com.cn/news/mqyw/44176.html)
  - 商丘纪检监察网 sqlzw.gov.cn — 民权县纪委监委领导机构 (王晓敏任监委主任, 纪委副书记张林军/乔帅)
  - 中华网河南 2023-05-11 "王静娴任中共民权县委书记" (https://henan.china.com/news/hot/2023/0511/2530454638.html)
  - 中华网河南 2021-08-07 "王静娴同志任民权县委副书记、提名为县长候选人" (https://henan.china.com/shangqiu/info/2021/0807/2530196809.html)
  - 中华网河南 2021-09-15 "张团结当选为民权县委书记" (https://henan.china.com/shangqiu/info/2021/0915/2530206052.html)
  - 澎湃新闻 2023-10-12 "王景义当选为民权县政府县长" (https://www.thepaper.cn/newsDetail_forward_24910903)
  - 百度百科 "王景义(民权县委副书记、县长)" — 完整履历, 1978年生宁陵人 (https://baike.baidu.com/item/王景义/58147253)
  - 百度百科 "张团结(商丘市人大常委会副主任、梁园区委书记)" — 完整履历 (https://baike.baidu.com/item/张团结/19756818)
  - 央视网 2026-05-22 "河南省商丘市人大常委会副主任张团结接受纪律审查和监察调查" (https://news.cctv.com/2026/05/22/ARTIBPP6d2l1JsUmK6h7wjLw260522.shtml)
  - 河南日报 2025-02-21 专访县委书记王静娴 (https://newpaper.dahe.cn/hnrb/html/2025-02/21/content_16_1722304.htm)
  - 时代酒店网素材/官宣公示: 2023-04-28 河南省委组织部拟任公示 — 王静娴(女,1977-11生, 中央党校研究生, 文学学士; 曾任驻马店政务大数据局长/正阳县委常)
  - 中国县域 民权县政府领导分工 (王静娴县长时; 王景义常务副县长) (http://www.zgcounty.com/news/37256.html)
  - 中国县域 民权县2025年政府工作报告 (王景义县长)

Confidence notes:
  - 王静娴: confirmed as 县委书记 (2023-05-11 起, 2026年仍在任)
  - 王景峰: confirmed as 县长 (2023-10-11 当选, 2026年仍在任)
  - 张团结: confirmed as 前任县委书记, 2026-05-22 被查
  - 领导班子 roster: 由多份官方文章交叉确认
  - 部分人物出生/学历/完整履历: 未取得完整公开资料, 标记 unverified/plausible
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root: data/tmp/henan_民权县/ → data/ → repo root
SLUG = "民权县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "王静娴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-11",
        "birthplace": "",
        "education": "中央党校研究生、文学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共民权县委员会",
        "source": "Confirmed as 县委书记 since 2023-05-11 (中华网河南 2023-05-11; 河南省委组织部2023-04-28拟任公示; 民权县委常委会第150-164次会议 2026仍在任). 曾任民权县长(2021-08~2023-05), 此前任驻马店市政务服务和大数据管理局局长、正阳县委常委/宣传部部长/常务副县长."
    },
    {
        "id": 2,
        "name": "王景义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-07",
        "birthplace": "河南省商丘市宁陵县",
        "education": "党校研究生",
        "party_join": "1999-07",
        "work_start": "1996-08",
        "current_post": "县委副书记、县长",
        "current_org": "民权县人民政府",
        "source": "Confirmed via 澎湃 2023-10-12 '王景义当选为民权县政府县长'; 民权网 2026 仍为县委副书记、县长. 完整履历见百度百科: 1978-07生宁陵人, 1996参加工作, 1999入党, 党校研究生; 曾任宁陵县政府办干部/乡长、商丘市商务局副局长(援疆兵团十三师红山农场副场长)、民权县委常/常务副/代县长."
    },
    {
        "id": 3,
        "name": "张团结",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "商丘市人大常委会副主任、梁园区委书记（此前为民权县委书记）",
        "current_org": "商丘市人大常委会",
        "source": "曾任民权县委副书记(2012)、民权县长(2015.03-2021.09)、民权县委书记(2021.09-2023.05); 后任商丘市人大常委会副主任、梁园区区委书记. ⚠️2026-05-22 接受纪律审查和监察调查(央视)."
    },
    # ═══════ Leadership Roster ═══════
    {
        "id": 4,
        "name": "陈鸿志",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、政法委书记",
        "current_org": "中共民权县委员会",
        "source": "Confirmed via 民权网 2026-03-12 植树活动 (县委副书记、政法委书记陈鸿志) 及 2026-11 制冷博览会复盘会议."
    },
    {
        "id": 5,
        "name": "张爱军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "民权县人民代表大会常务委员会",
        "source": "Confirmed via 民权网 2026-04-03 人大常委第36次会议 (县人大常委会党组书记、主任张爱军)."
    },
    {
        "id": 6,
        "name": "周明河",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议民权县委员会",
        "source": "Confirmed via 民权网 2026-03-12 植树活动 (县政协主席周明河)."
    },
    {
        "id": 7,
        "name": "李卫政",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "民权县人民政府",
        "source": "Confirmed via 民权网 2026-03-18 政府第64次常务会议及人大常委会议 (身为常、常务副)."
    },
    {
        "id": 8,
        "name": "李晓彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长（2026-07前后已交棒）",
        "current_org": "中共民权县委员会",
        "source": "Confirmed via 民权网 2026-04-03 人大常委会议 (县委常委、组织部部长李晓彬). 2026-07-09 人大八次会议报道显示组织部部长为祝金伟, 推定为中期调整."
    },
    {
        "id": 9,
        "name": "王晓敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "民权县纪律检查委员会",
        "source": "Confirmed via 民权网 2026-04-03 (县委常委、县纪委书记、监委主任王晓敏) 及 商丘纪检监察网 领导机构 (监委主任:王晓敏)."
    },
    {
        "id": 10,
        "name": "毕道喜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、副县长",
        "current_org": "民权县人民政府",
        "source": "Confirmed via 中国县域 民权县政府领导分工 (民权县委常、宣传部长、县政府党组成员、副县长毕道喜)."
    },
    {
        "id": 11,
        "name": "李天桩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "民权县人民政府",
        "source": "Confirmed via 民权网 2026-03-18 政府第64次常务会议 及 分工."
    },
    {
        "id": 12,
        "name": "王玉军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县高新区管委会主任",
        "current_org": "民权县高新技术产业开发区",
        "source": "Confirmed via 民权网 政府常务会议列席 (县高新区管委会主任王玉军)."
    },
    {
        "id": 13,
        "name": "黄新峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长、政府办公室主任",
        "current_org": "民权县人民政府",
        "source": "Confirmed via 民权网 政府常务会议 (县领导黄新峰出席) 及 中国县域分工."
    },
    {
        "id": 14,
        "name": "陈进领",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、二级调研员",
        "current_org": "民权县人民政府",
        "source": "Confirmed via 民权网 政府常务会议 及 家园县域分工."
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共民权县委员会", "type": "党委", "level": "县处级", "parent": "中共商丘市委", "location": "民权县"},
    {"id": 2, "name": "民权县人民政府", "type": "政府", "level": "县处级", "parent": "商丘市人民政府", "location": "民权县"},
    {"id": 3, "name": "民权县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "商丘市人大常委会", "location": "民权县"},
    {"id": 4, "name": "中国人民政治协商会议民权县委员会", "type": "政协", "level": "县处级", "parent": "商丘市政协", "location": "民权县"},
    {"id": 5, "name": "民权县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "商丘市纪委监委", "location": "民权县"},
    {"id": 6, "name": "民权县高新技术产业开发区", "type": "开发区", "level": "县处级", "parent": "民权县人民政府", "location": "民权县"},
    {"id": 7, "name": "商丘市人大常委会", "type": "人大", "level": "地级市", "parent": "河南省人大常委会", "location": "商丘市"},
    {"id": 8, "name": "中共商丘市委", "type": "党委", "level": "地级市", "parent": "中共河南省委", "location": "商丘市"},
    {"id": 9, "name": "商丘市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "商丘市"},
    {"id": 10, "name": "中共梁园区委", "type": "党委", "level": "副厅级", "parent": "中共商丘市委", "location": "商丘市梁园区"},
]

# ── Positions (person → org with title) ────────────────────────────────────

positions = [
    # 王静娴 (id=1)
    {"person_id": 1, "org_id": 2, "title": "县长（前任）", "start_date": "~2021-08", "end_date": "2023-05", "rank": "县处级正职", "note": "2021-08-07 任县委副书记、县长候选人; 2023-06 人大会报告为县长"},
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2023-05-11", "end_date": "present", "rank": "县处级正职", "note": "Confirmed 2023-05-11 任职通知; 2026 仍主持常委会"},
    # 王景义 (id=2)
    {"person_id": 2, "org_id": 2, "title": "常务副县长（前任）", "start_date": "2021-08", "end_date": "2023-10", "rank": "县处级副职", "note": "2021-09 民权县委常委、常务副县长、县政府党组副书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2023-10-11", "end_date": "present", "rank": "县处级正职", "note": "2023-10-11 第23届人大第次会入选"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2023-10-11", "end_date": "present", "rank": "县处级副职", "note": "县长兼任"},
    # 张团结 (id=3)
    {"person_id": 3, "org_id": 2, "title": "县长（前任）", "start_date": "2015-03", "end_date": "2021-09", "rank": "县处级正职", "note": "2015-03 起任民权县长"},
    {"person_id": 3, "org_id": 1, "title": "县委书记（前任）", "start_date": "2021-09", "end_date": "2023-05", "rank": "县处级正职", "note": "2021-09-14 十三届县委一次全会当选"},
    {"person_id": 3, "org_id": 7, "title": "商丘市人大常委会副主任", "start_date": "~2023-05", "end_date": "present", "rank": "厅级", "note": "2023-05 后任; 兼任梁园区区委书记; 2026-05-22被查"},
    {"person_id": 3, "org_id": 10, "title": "梁园区区委书记", "start_date": "~2023", "end_date": "present", "rank": "副厅级", "note": "兼职"},
    # 陈鸿志 (id=4)
    {"person_id": 4, "org_id": 1, "title": "县委副书记、政法委书记", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": "Confirmed 2026"},
    # 张爱军 (id=5)
    {"person_id": 5, "org_id": 3, "title": "县人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "县处级正职", "note": "Confirmed 2026"},
    # 周明河 (id=6)
    {"person_id": 6, "org_id": 4, "title": "县政协主席", "start_date": "unknown", "end_date": "present", "rank": "县处级正职", "note": "Confirmed 2026"},
    # 李卫政 (id=7)
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "常务副县长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": "Confirmed 2026"},
    # 李晓彬 (id=8)
    {"person_id": 8, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "unknown", "end_date": "2026-07", "rank": "县处级副职", "note": "Confirmed 2026-04; 2026-07后转为祝金伟"},
    # 王晓敏 (id=9)
    {"person_id": 9, "org_id": 5, "title": "县纪委书记、监委主任", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": "Confirmed 2026"},
    # 毕道喜 (id=10)
    {"person_id": 10, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 李天桩 (id=11)
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": "Confirmed 2026"},
    # 王玉军 (id=12)
    {"person_id": 12, "org_id": 6, "title": "高新区管委会主任", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "Confirmed 2026"},
    # 黄新峰 (id=13)
    {"person_id": 13, "org_id": 2, "title": "县政府党组成员、副县长、政府办公室主任", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": "Confirmed 2026"},
    # 陈进领 (id=14)
    {"person_id": 14, "org_id": 2, "title": "县政府党组成员、二级调研员", "start_date": "unknown", "end_date": "present", "rank": "处级", "note": "Confirmed 2026"},
]

# ── Relationships ───────────────────────────────────────────────────────────

relationships = [
    # 王静娴 ↔ 王景义（党政正职搭档）
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "王静娴（县委书记）与王景义（县长）为全县党政正职搭档，共同主持县委县政府工作（多次同场出席会议，如植树活动、制冷博览会、县委会常务会）。",
        "overlap_org": "民权县",
        "overlap_period": "2023-至今"
    },
    # 王静娴 ↔ 张团结（前后任交接）
    {
        "person_a": 1, "person_b": 3,
        "type": "predecessor_successor",
        "context": "张团结 2023-05 离任民权县委书记，王静娴接任县委书记；张到商丘市人大任，2026-05-22 被查。",
        "overlap_org": "中共民权县委员会",
        "overlap_period": "2023-05"
    },
    # 王景义 ↔ 张团结（政县长 → 县长?）
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "张团结任县委书记期间（2021-2023），王景义任民权常务副县长、代县长，同一班子工作。",
        "overlap_org": "民权县",
        "overlap_period": "2021-2023"
    },
    # 王静娴 ↔ 陈鸿志
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "王静娴（县委书记）与陈鸿志（县委副书记、政法委书记）在民权县委班子共事",
        "overlap_org": "民权县",
        "overlap_period": "当前"
    },
    # 王景义 ↔ 李卫政（政府正副职）
    {
        "person_a": 2, "person_b": 7,
        "type": "superior_subordinate",
        "context": "王景义（县长）与李卫政（常务副县长）为县政府正副职搭档，共同主持政府常务会议",
        "overlap_org": "民权县人民政府",
        "overlap_period": "当前"
    },
    # 王景义 ↔ 王玉军（高新开发区领导）
    {
        "person_a": 2, "person_b": 12,
        "type": "superior_subordinate",
        "context": "王景义（县长）与王玉军（高新区管委会主任）在政府常务会议同场，高新区主任列席",
        "overlap_org": "民权县",
        "overlap_period": "当前"
    },
    # 王静娴 ↔ 张爱军（党政对接）
    {
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "王静娴（县委书记）与张爱军（县人大常委会主任）为全县核心领导，共证人大协商事项",
        "overlap_org": "民权县",
        "overlap_period": "当前"
    },
    # 王静娴 ↔ 周明河
    {
        "person_a": 1, "person_b": 6,
        "type": "overlap",
        "context": "王静娴（县委书记）与周明河（县政协主席）共同出席植树等全县性活动",
        "overlap_org": "民权县",
        "overlap_period": "当前"
    },
    # 王静娴 ↔ 王晓敏（纪检）
    {
        "person_a": 1, "person_b": 9,
        "type": "overlap",
        "context": "王静娴（县委书记）与王晓敏（县纪委书记、监委主任）为县委纪委班子",
        "overlap_org": "民权县",
        "overlap_period": "当前"
    },
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "王静娴",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "商丘市",
                "region": "民权县",
                "job": "县委书记",
                "task_id": "henan_民权县",
                "time_focus": "2021-2026"
            },
            "identity": {
                "person_id": "minquan_wang_jingxian",
                "name": "王静娴",
                "aliases": [],
                "gender": "女",
                "ethnicity": "汉族",
                "birth": "1977-11",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "中央党校",
                        "major": "",
                        "degree": "研究生",
                        "study_type": "party_school",
                        "source_ids": ["S004"]
                    }
                ],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "王静娴_197711",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共民权县委员会",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S004"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "王静娴任驻马店市政务服务和大数据管理局局长前的早期履历（出生至任正阳县委前）未公开。网络公开资料显示其曾在驻马店市正阳县任县委常、宣传部部长、常务副县长。",
                    "confidence": "unverified",
                    "source_ids": []
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "正阳县委",
                    "title": "县委常委、宣传部部长",
                    "level": "县处级副职",
                    "location": "河南省驻马店市正阳县",
                    "system": "party",
                    "rank": "副处级",
                    "is_key_promotion": False,
                    "notes": "来自任前公示 '曾任正委县委常委、宣传部部长'（驻马店）。",
                    "confidence": "plausible",
                    "source_ids": ["S004"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "正阳县人民政府",
                    "title": "县委常委、常务副县长",
                    "level": "县处级副职",
                    "location": "河南省驻马店市正阳县",
                    "system": "government",
                    "rank": "副处级",
                    "is_key_promotion": False,
                    "notes": "任前公示中 '曾在河南驻马店市正阳县委副书记、常务县长'。",
                    "confidence": "plausible",
                    "source_ids": ["S004"]
                },
                {
                    "start": "unknown",
                    "end": "2021-08",
                    "org": "驻马店市政务服务和大数据管理局",
                    "title": "局长",
                    "level": "正处级",
                    "location": "河南省驻马店市",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": False,
                    "notes": "任前公示 '曾任驻马店市政务服务和大数据管理局局长'。",
                    "confidence": "plausible",
                    "source_ids": ["S004"]
                },
                {
                    "start": "2021-08",
                    "end": "2023-05",
                    "org": "民权县人民政府",
                    "title": "县长",
                    "level": "县处级正职",
                    "location": "河南省商丘市民权县",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": False,
                    "notes": "2021-08-07 任县委副书记、县长候选人; 2023年政府工作报告以县长身份宣读。",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "start": "2023-05-11",
                    "end": "present",
                    "org": "中共民权县委员会",
                    "title": "县委书记",
                    "level": "县处级正职",
                    "location": "河南省商丘市民权县",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2023-05-11 省委/商丘市委任命; 2026年仍主持县委常委会（第150-164次）。",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"]
                }
            ],
            "organizations": [
                {"org": "驻马店市政务服务和大数据管理局", "role": "局长", "period": "~2021"},
                {"org": "民权县人民政府", "role": "县长", "period": "2021-2023"},
                {"org": "中共民权县委员会", "role": "县委书记", "period": "2023-至今"}
            ],
            "relationships": [
                {
                    "person": "王景义",
                    "person_id": "minquan_wang_jingyi",
                    "relationship_type": "overlap",
                    "strength": "strong",
                    "evidence": "王静娴（县委书记）与王景义（县长）为全县党政正职搭档，多次同场主持/出席县委常委会、政府常务会议及调研活动。",
                    "overlap_org": "民权县",
                    "overlap_period": "2023-至今",
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "person": "张团结",
                    "person_id": "minquan_zhang_tuanjie",
                    "relationship_type": "predecessor_successor",
                    "strength": "strong",
                    "evidence": "张团结2023-05离任民权县委书记，王静娴接任县委书记（前后任交接）。",
                    "overlap_org": "中共民权县委员会",
                    "overlap_period": "2023-05",
                    "direction": "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S005"]
                },
                {
                    "person": "陈鸿志",
                    "person_id": "minquan_chen_hongzhi",
                    "relationship_type": "superior_subordinate",
                    "strength": "medium",
                    "evidence": "王静娴（书记）与陈鸿志（县委副书记、政法委书记）同届县委班子。",
                    "overlap_org": "民权县",
                    "overlap_period": "当前",
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "governance_record": [
                {
                    "period": "2026-03-05",
                    "domain": "economic_development",
                    "achievement_or_event": "调研督导省市重点项目建设（同鑫制冷二期、阿斯贝拉配套产业园、宏象铝业、康拜恩电器），召开座谈会部署优化营商环境。",
                    "role_in_event": "主持调研督导",
                    "location": "民权县",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "period": "2024-08-28",
                    "domain": "industry",
                    "achievement_or_event": "推动黄河故道葡萄酒产区（民权）高质量发展调研座谈会在民权举办，强调把以葡萄酒为主的食品加工产业确立为重点扶持支柱产业。",
                    "role_in_event": "推动/致辞",
                    "location": "民权县",
                    "confidence": "plausible",
                    "source_ids": ["S006"]
                },
                {
                    "period": "2025-11-07",
                    "domain": "industry",
                    "achievement_or_event": "主持召开第八届河南·民权制冷博览会复盘会议，强调坚定信心把冷博会办好、走市场化路线、与机电商会深化合作",
                    "role_in_event": "主持",
                    "location": "民权县",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "professional_profile": {
                "primary_specializations": ["县域经济", "工业/制冷产业", "葡萄酒产业", "城市规划"],
                "secondary_specializations": ["县城治理", "生态建设"],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["河南省驻马店市", "河南省商丘市"],
                "promotion_velocity": {
                    "summary": "2021-08 从正处级（驻马店市政务服务和大数据管理局局长）转任民权县长，2023-05 升任县委书记，两年内实现县长→书记晋升，属正常组织晋升路径。",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "grassroots_oriented",
                        "evidence": "频繁深入企业车间、乡镇林带）调研重点项目建设，走访阿斯贝拉、美是食品等企业并现场督导",
                        "confidence": "plausible",
                        "source_ids": ["S001"]
                    },
                    {
                        "trait": "pragmatic",
                        "evidence": "强调树立和践行正确政绩观，不搞形式主义、不做表面文章",
                        "confidence": "plausible",
                        "source_ids": ["S001"]
                    }
                ],
                "speech_themes": ["六城一中心", "1234工作思路", "高质量发展", "政绩观"],
                "management_signals": ["亲自抓重点项目", "重视营商环境", "抓产业升级"],
                "caveat": "工作风格基于公开报道和讲话要点推断，非私人心理评估"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026-08，未发现王静娴本人的纪检处分或负面媒体。",
                    "date": AS_OF,
                    "confidence": "plausible",
                    "source_ids": []
                },
                {
                    "type": "controversy",
                    "description": "其前手民权县委书记张团结（2021-2023）2026-05-22 因接受纪律审查和监察调查被查（时任商丘市人大常委会副主任）；张团结在县长/书记任内同王静娴共事，提示民权班子历史关联风险需关注。",
                    "date": "2026-05-22",
                    "confidence": "confirmed",
                    "source_ids": ["S005"]
                }
            ],
            "source_register": [
                {"id": "S001", "title": "县委书记王静娴调研省市重点项目建设 开展树立和践行正确政绩观学习教育", "url": "http://www.cnmq.com.cn/news/mqyw/44107.html", "publisher": "民权网", "published_at": "2026-03-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认王静娴任县委书记，2026年在任"},
                {"id": "S002", "title": "中共民权县第十三届委员会常委会第151次会议召开", "url": "http://www.cnmq.com.cn/news/mqyw/43881.html", "publisher": "民权网", "published_at": "2026-01-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认王静娴主持县委常委会"},
                {"id": "S003", "title": "王静娴同志任民权县委副书记、提名为县长候选人", "url": "https://henan.china.com/shangqiu/info/2021/0807/2530196809.html", "publisher": "中华网河南", "published_at": "2021-08-07", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "确认王静娴2021-08任县长候选人"},
                {"id": "S004", "title": "'75后'的她，拟任县（市、区）委书记（河南省委组织部拟任公示）", "url": "http://www.jiudian.news3.cn/information/2023/0507/2834.html", "publisher": "时代酒店网转载", "published_at": "2023-05-07", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "medium", "notes": "省委组织部拟任公示：王静娴女1977-11生，中央党校研究生文学学士，曾任驻马店政务/正阳县委常、宣传部部长、常务副"},
                {"id": "S005", "title": "河南省商丘市人大常委会副主任张团结接受纪律审查和监察调查", "url": "https://news.cctv.com/2026/05/22/ARTIBPP6d2l1JsUmK6hWjLw260522.shtml", "publisher": "央视新闻", "published_at": "2026-05-22", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "确认张团结（民权前任书记）被查"},
                {"id": "S006", "title": "黄河故道葡萄酒产区（民权）高质量发展调研座谈会在民权成功举办", "url": "http://www.winechina.com/html/2024/08/202408319017.html", "publisher": "葡萄酒信息网", "published_at": "2024-08-01", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "确认王静娴对葡萄酒产业推动，发词提及"}
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "王静娴任驻马店市职务前的早期履历及出生地/籍贯"
            },
            "open_questions": [
                {
                    "priority": "high",
                    "question": "王静娴的出生地/籍贯及入党/参加工作时间？",
                    "why_it_matters": "核心人物完整身份信息（dedupe_key用途）",
                    "suggested_queries": ["王静娴 籍贯 民权", "王静娴 简历 出生"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "王静娴任正阳县委前（在驻马店任政务大数据局长前的）早期履历？",
                    "why_it_matters": "跨市流动来源与干部系统归属",
                    "suggested_queries": ["王静娴 驻马店 正阳 履历"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    {
        "id": 2,
        "name": "王景义",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "商丘市",
                "region": "民权县",
                "job": "县委副书记、县长",
                "task_id": "henan_民权县",
                "time_focus": "2021-2026"
            },
            "identity": {
                "name": "王景义",
                "person_id": "minquan_wang_jingyi",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1978-07",
                "birthplace": "河南省商丘市宁陵县",
                "native_place": "河南宁陵",
                "education": [
                    {
                        "period": "2005-09~2008-07",
                        "institution": "中央党校研究生院",
                        "major": "法学理论",
                        "degree": "研究生",
                        "study_type": "party_school",
                        "source_ids": ["S010"]
                    },
                    {
                        "period": "",
                        "institution": "河南省物资学校（文秘专业）",
                        "major": "文秘",
                        "degree": "中专",
                        "study_type": "full_time",
                        "source_ids": ["S010"]
                    }
                ],
                "party_join": "1999-07",
                "work_start": "1996-08",
                "dedupe_keys": {
                    "name_birth": "王景义_197807",
                    "name_birthplace": "王景义_河南宁陵",
                    "official_profile_url": "https://baike.baidu.com/item/王景义/58147253"
                }
            },
            "current_status": {
                "current_post": "县委副书记、县长",
                "current_org": "民权县人民政府",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"]
            },
            "career_timeline": [
                {
                    "start": "1992-09",
                    "end": "1996-07",
                    "org": "河南省物资学校",
                    "title": "文秘专业学习",
                    "level": "",
                    "location": "河南省",
                    "system": "education",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "1992.09-1996.07 河南省物资学校文秘专业学习",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "start": "1996-07",
                    "end": "2000-11",
                    "org": "宁陵县人民政府办公室",
                    "title": "干部",
                    "level": "科员",
                    "location": "河南省商丘市宁陵县",
                    "system": "government",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "1996.07-2000.11 宁陵县政府办干部 (1996.06-1998.06 河南财院秘书专业大专)",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "start": "2000-11",
                    "end": "2004-02",
                    "org": "宁陵县政府督查室",
                    "title": "副主任",
                    "level": "",
                    "location": "宁陵县",
                    "system": "government",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "2000.11-2004.02 督察室副主任 (河南大学汉语言文学本科)",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "start": "2004-02",
                    "end": "2007-12",
                    "org": "宁陵县人民政府办公室",
                    "title": "副主任、督查室主任",
                    "level": "",
                    "location": "宁陵县",
                    "system": "government",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "2004.02-2005.04 政府办副主任;(2002.08-2004.12党校函授法律专科)",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "start": "2007-12",
                    "end": "2010-05",
                    "org": "宁陵县刘楼乡",
                    "title": "党委副书记、乡长",
                    "level": "乡科级正职",
                    "location": "宁陵县",
                    "system": "government",
                    "rank": "正科级",
                    "is_key_promotion": False,
                    "notes": "2007.12-2010.05 刘楼乡党委副书记、乡长",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "start": "2010-05",
                    "end": "2012-11",
                    "org": "宁陵县孔集乡",
                    "title": "党委副书记、乡长",
                    "level": "乡科级正职",
                    "location": "宁陵县",
                    "system": "government",
                    "rank": "正科级",
                    "is_key_promotion": False,
                    "notes": "2010.05-2012.11 孔集乡党委副书记、乡长",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "start": "2012-11",
                    "end": "2021-02",
                    "org": "商丘市商务局",
                    "title": "党组成员、副局长",
                    "level": "",
                    "location": "商丘市",
                    "system": "government",
                    "rank": "副处级",
                    "is_key_promotion": True,
                    "notes": "2012.11-2020.10 商务局党组成员、副局长；2016.12-2020.01挂职新疆兵团十三师红旗山农场党委常委、副场长(援疆)",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "start": "2021-02",
                    "end": "2021-08",
                    "org": "商丘市商务局",
                    "title": "一级调研员",
                    "level": "",
                    "location": "商丘市",
                    "system": "government",
                    "rank": "一级调研员",
                    "is_key_promotion": False,
                    "notes": "2020.10-2021.02 三级调研员；2021.02-2021.08 二级调研员（商丘市商务局副局长）",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "start": "2021-08",
                    "end": "2023-10",
                    "org": "民权县人民政府",
                    "title": "县委常委、常务副县长（县政府党组副书记）",
                    "level": "县处级副职",
                    "location": "民权县",
                    "system": "government",
                    "rank": "副处级",
                    "is_key_promotion": True,
                    "notes": "2021-08 常务副县长候选人，2021-09 常务副县长；后任代县长",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "start": "2023-10-11",
                    "end": "present",
                    "org": "民权县人民政府",
                    "title": "县委副书记、县长",
                    "level": "县处级正职",
                    "location": "民权县",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2023-10-11 第十六届人大第四次会议当选县长",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                }
            ],
            "organizations": [
                {"org": "宁陵县政府办/乡镇", "role": "干部/乡长", "period": "1996-2012"},
                {"org": "商丘市商务局", "role": "副局长（援疆）", "period": "2012-2021"},
                {"org": "民权县人民政府", "role": "常务副县长/县长", "period": "2021-至今"}
            ],
            "relationships": [
                {
                    "person": "王静娴",
                    "person_id": "minquan_wang_jingxian",
                    "relationship_type": "overlap",
                    "strength": "strong",
                    "evidence": "王景义（县长）与王静娴（县委书记）为全县党政正职搭档",
                    "overlap_org": "民权县",
                    "overlap_period": "2023-至今",
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "governance_record": [
                {
                    "period": "2026-03-02",
                    "domain": "economic_development",
                    "achievement_or_event": "作2025年政府工作报告：2024年GDP 307.4亿元(+4.5%)，社零+6.2%增速全市第2，规上工业+7.0%；推进制冷装备产业链、铝基新材料、食品产业",
                    "role_in_event": "作政府工作报告",
                    "location": "民权县",
                    "confidence": "confirmed",
                    "source_ids": ["S004"]
                },
                {
                    "period": "2026-03-25",
                    "domain": "discipline",
                    "achievement_or_event": "调度重点领域群腐整治，赴校园餐、养老、农业领域督导",
                    "role_in_event": "调度部署",
                    "location": "民权县",
                    "confidence": "confirmed",
                    "source_ids": ["S005"]
                }
            ],
            "professional_profile": {
                "primary_specializations": ["县域经济", "农业/生态", "文旅"],
                "secondary_specializations": ["项目建设", "安全生产"],
                "career_pattern": "local_ladder",
                "systems_experience": ["government"],
                "geographic_pattern": ["宁陵县", "商丘市", "新疆兵团（援疆）", "民权县"],
                "promotion_velocity": {
                    "summary": "从基层乡镇长起步，历经商丘市直机关（商务局）和援疆，2021年转民权县常务副县长，2023年任县长。",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "pragmatic",
                        "evidence": "多次组织群腐整治，强调校园食品安全、养老服务等民生领域治理；作报告强调高质量发展",
                        "confidence": "plausible",
                        "source_ids": ["S004", "S005"]
                    }
                ],
                "speech_themes": ["高质量发展", "群腐整治"],
                "management_signals": ["重抓重点项目建设", "重视安全生产"],
                "caveat": "工作风格基于公开报道推断，非私人心理评估"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026-08，未发现王景义本人纪检或审计问题。",
                    "date": AS_OF,
                    "confidence": "plausible",
                    "source_ids": []
                }
            ],
            "source_register": [
                {"id": "S001", "title": "民权县第十六届人民政府第64次常务会议", "url": "http://www.cnmq.com.cn/news/mqyw/44142.html", "publisher": "民权网", "published_at": "2026-03-18", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认王景义为县长，主持常务会议"},
                {"id": "S002", "title": "王景义当选为民权县政府县长", "url": "https://www.thepaper.cn/newsDetail_forward_24910903", "publisher": "澎湃新闻", "published_at": "2023-10-12", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "确认王景义2023-10-11当选县长"},
                {"id": "S003", "title": "百度百科 王景义（民权县委副书记、县长）", "url": "https://baike.baidu.com/item/王景义/58147253", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "完整履历：1978-07宁陵人，1996工作；商丘商贸、援疆、民权常务副县长/县长"},
                {"id": "S004", "title": "民权县2025年政府工作报告", "url": "http://www.zgcounty.com/news/67521.html", "publisher": "中国县域", "published_at": "2025-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王景义县长作报告"},
                {"id": "S005", "title": "县委副书记、县长王景义调度重点领域群腐整治工作", "url": "http://www.cnmq.com.cn/news/mqyw/44176.html", "publisher": "民权网", "published_at": "2026-03-25", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认王景义2026-03在任县长"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "complete",
                "relationship_confidence": "high",
                "biggest_gap": "王景义出生地宁陵（已确认），县级身份相关档案详实；open questions 较少"
            },
            "open_questions": [
                {
                    "priority": "medium",
                    "question": "王景义任民权县长前是否兼县委副书记？（已按惯例推定兼任）",
                    "why_it_matters": "党政分工确认",
                    "suggested_queries": ["王景义 民权 县委副书记"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    {
        "id": 3,
        "name": "张团结",
        "job": "前任县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "商丘市",
                "region": "民权县",
                "job": "前任县委书记",
                "task_id": "henan_民权县",
                "time_focus": "2012-2026"
            },
            "identity": {
                "person_id": "minquan_zhang_tuanjie",
                "name": "张团结",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {
                        "institution": "永城师范学校",
                        "major": "",
                        "degree": "中专",
                        "study_type": "full_time",
                        "period": "1985.09-1988.07",
                        "source_ids": ["S002"]
                    }
                ],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "张团结_unknown",
                    "name_birthplace": "",
                    "official_profile_url": "https://baike.baidu.com/item/张团结/19756818"
                }
            },
            "current_status": {
                "current_post": "商丘市人大常委会副主任、梁园区委书记（被调查）",
                "current_org": "商丘市人大常委会",
                "administrative_rank": "厅级（副厅）",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "1985.09", "end": "1988.07", "org": "永城师范学校", "title": "学习", "confidence": "confirmed", "notes": "中师"},
                {"start": "1988.09", "end": "1996.03", "org": "商丘市(县级)乡镇企业局劳动服务公司", "title": "干部/办公室副主任/主任", "confidence": "confirmed", "notes": "基层起步"},
                {"start": "2008.12", "end": "2012.12", "org": "商丘经济技术开发区管委会", "title": "副主任、党委副书记（正处级）", "confidence": "confirmed", "notes": "正处级"},
                {"start": "2012.12", "end": "2015.03", "org": "中共民权县委", "title": "县委副书记", "confidence": "confirmed"},
                {"start": "2015.03", "end": "2021.09", "org": "民权县人民政府", "title": "县长", "confidence": "confirmed", "notes": "2015.09-2015.12挂职浙江衢州常山县县长助理"},
                {"start": "2021.09", "end": "2023.05", "org": "中共民权县委", "title": "县委书记", "confidence": "confirmed", "notes": "2021-09-14十三届县委一次全会当选"},
                {"start": "2023.05", "end": "present", "org": "商丘市人大常委会", "title": "市人大常委会副主任（兼梁园区区委书记）", "confidence": "confirmed", "notes": "2026-05-22 被查"},
            ],
            "organizations": [
                {"org": "中共民权县委", "role": "副书记/书记", "period": "2012-2023"},
                {"org": "民权县人民政府", "role": "县长", "period": "2015-2021"},
                {"org": "商丘市人大常委会", "role": "副主任", "period": "2023-至今"}
            ],
            "relationships": [
                {
                    "person": "王静娴",
                    "person_id": "minquan_wang_jingxian",
                    "relationship_type": "predecessor_successor",
                    "strength": "strong",
                    "evidence": "张团结 2023-05 民调任县委书记，王静娴接任",
                    "overlap_org": "中共民权县委员会",
                    "overlap_period": "2023-05",
                    "direction": "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"]
                },
                {
                    "person": "王景义",
                    "person_id": "minquan_wang_jingyi",
                    "relationship_type": "overlap",
                    "strength": "medium",
                    "evidence": "张团结任县委书记期间（2021-2023）王景义任民权常务副县长、代县长",
                    "overlap_org": "民权县",
                    "overlap_period": "2021-2023",
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": []
                }
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["商丘市", "民权县"],
                "promotion_velocity": {"summary": "长期在商丘与民权基层，2012年后县处级，2023年升厅级（市人大副主任）。", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "受调查后公开形象有限"},
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "disciplinary_action",
                    "description": "2026-05-22 张团结（商丘市人大常委会副主任、梁园区区委书记）接受纪律审查和监察调查。作为民权县前县委书（2021-09~2023-05任书记；2015-2021任县长），其被查可能波及民权县领导班子与用人环节，需重点关注民权班子历史关联风险。",
                    "date": "2026-05-22",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "source_register": [
                {"id": "S001", "title": "河南省商丘市人大常委会副主任张团结接受纪律审查和监察调查", "url": "https://news.cctv.com/2026/05/22/ARTIBPP6d2l1JsUmK6hWjLw260522.shtml", "publisher": "央视新闻", "published_at": "2026-05-22", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "被查通报"},
                {"id": "S002", "title": "百度百科 张团结（商丘市人大常委会副主任、梁园区委书记）", "url": "https://baike.baidu.com/item/张团结/19756818", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "2012任民权县委副书记、2015-2021县长、2021-2023县委书记、后任商丘市人大副主任兼梁园区区委书记"}
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "high",
                "biggest_gap": "出生年/籍贯/学历（除永城师范）未完全确认；被查具体情节未公开"
            },
            "open_questions": [
                {
                    "priority": "high",
                    "question": "张团结被查的具体所指（受贿、用人等）及对民权班子的影响？",
                    "why_it_matters": "民权县班子高风险关联",
                    "suggested_queries": ["张团结 被查 民权 案件"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
]

# ─────────────────────────────────────────────────────────────────────────
# Runner
# ─────────────────────────────────────────────────────────────────────────

def main():
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

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

    # Write person JSON files
    for pf in person_files_data:
        person_name = pf["name"]
        job = pf["job"]
        filename = f"{TODAY}-河南省-商丘市-{job}-{person_name}.json"
        filepath = PERSONS_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filepath}")

    print(f"\nDone. Build complete for {SLUG}.")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")


if __name__ == "__main__":
    main()