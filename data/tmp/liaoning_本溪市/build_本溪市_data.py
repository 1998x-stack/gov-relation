#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 本溪市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_本溪市
Level: 地级市
Targets: 市委书记 & 市长

Research status: WEB ACCESS DEGRADED
  - Exa API rate-limited (free tier exhausted)
  - Baidu: 403 captcha block (all entries unavailable)
  - 本溪市人民政府门户网站 (www.benxi.gov.cn): accessible
  - News articles from benxi.gov.cn: primary source for leadership names and activities
  - Baidu Baike/360百科: unavailable due to captcha

Current officeholders (as of 2026-07-25):
  - 市委书记: 王永威 (confirmed via multiple benxi.gov.cn news articles, 2026-07-17 through 2026-07-20)
  - 市委副书记、市长: 郭志强 (confirmed via official government leadership page and news articles)
  - 市人大常委会主任: 何庆伟 (confirmed via news article 2026-07-20)
  - 市政协主席: 高巍 (confirmed via news article 2026-07-20)
  - 市委常委、组织部部长: 曹春光 (confirmed via news article 2026-07-20)

市政府领导班子 (from www.benxi.gov.cn/ld):
  - 市长: 郭志强
  - 副市长: 吕雪峰, 殷俊, 栾奎杰, 张继承, 李众, 王之成
  - 秘书长: 潘政宗

Additional leaders mentioned in news (2026-07-18 招商座谈会):
  - 胡桂涛, 刘佳, 初晓光, 曹春光, 殷俊, 刘明刚, 董培峥, 邴忠友, 栾奎杰, 李众, 李春, 张维利

Note on web access:
  - Baidu Baike entries for 王永威 and 郭志强 were inaccessible (403 captcha)
  - Full career history details are limited to what is published on the official government site
  - Person JSON files reflect partial evidence with explicit gaps
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

import sqlite3
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "本溪市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ── 市委书记 ──
    {
        "id": 1,
        "name": "王永威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中国共产党本溪市委员会",
        "source": "https://www.benxi.gov.cn (2026年7月多篇政务要闻确认)",
    },
    # ── 市委副书记、市长 ──
    {
        "id": 2,
        "name": "郭志强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "本溪市人民政府",
        "source": "https://www.benxi.gov.cn/ld 政府领导页面",
    },
    # ── 市人大常委会主任 ──
    {
        "id": 3,
        "name": "何庆伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "本溪市人大常委会",
        "source": "https://www.benxi.gov.cn/xw/zwyw/content_665330 (2026-07-20 校友返乡行报道)",
    },
    # ── 市政协主席 ──
    {
        "id": 4,
        "name": "高巍",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "政协本溪市委员会",
        "source": "https://www.benxi.gov.cn/xw/zwyw/content_665330 (2026-07-20 校友返乡行报道)",
    },
    # ── 市委常委、组织部部长 ──
    {
        "id": 5,
        "name": "曹春光",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中国共产党本溪市委员会组织部",
        "source": "https://www.benxi.gov.cn/xw/zwyw/content_665330 (2026-07-20 校友返乡行报道)",
    },
    # ── 副市长 ──
    {
        "id": 6,
        "name": "吕雪峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "本溪市人民政府",
        "source": "https://www.benxi.gov.cn/ld",
    },
    # ── 副市长 ──
    {
        "id": 7,
        "name": "殷俊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "本溪市人民政府",
        "source": "https://www.benxi.gov.cn/ld",
    },
    # ── 副市长 ──
    {
        "id": 8,
        "name": "栾奎杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "本溪市人民政府",
        "source": "https://www.benxi.gov.cn/ld",
    },
    # ── 副市长 ──
    {
        "id": 9,
        "name": "张继承",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "本溪市人民政府",
        "source": "https://www.benxi.gov.cn/ld",
    },
    # ── 副市长 ──
    {
        "id": 10,
        "name": "李众",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "本溪市人民政府",
        "source": "https://www.benxi.gov.cn/ld",
    },
    # ── 副市长 ──
    {
        "id": 11,
        "name": "王之成",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "本溪市人民政府",
        "source": "https://www.benxi.gov.cn/ld",
    },
    # ── 市政府秘书长 ──
    {
        "id": 12,
        "name": "潘政宗",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "本溪市人民政府办公室",
        "source": "https://www.benxi.gov.cn/ld",
    },
    # ── 市委常委（其他，从招商座谈会报道中确认）─
    {
        "id": 13,
        "name": "胡桂涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中国共产党本溪市委员会",
        "source": "https://www.benxi.gov.cn/xw/zwyw/content_665278 (2026-07-18 招商座谈会报道)",
    },
    {
        "id": 14,
        "name": "刘佳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中国共产党本溪市委员会",
        "source": "https://www.benxi.gov.cn/xw/zwyw/content_665278 (2026-07-18 招商座谈会报道)",
    },
    {
        "id": 15,
        "name": "初晓光",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中国共产党本溪市委员会",
        "source": "https://www.benxi.gov.cn/xw/zwyw/content_665278 (2026-07-18 招商座谈会报道)",
    },
    # ── 其他市领导 ──
    {
        "id": 16,
        "name": "刘明刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "本溪市",
        "source": "https://www.benxi.gov.cn/xw/zwyw/content_665278 (2026-07-18 招商座谈会报道)",
    },
    {
        "id": 17,
        "name": "董培峥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "本溪市",
        "source": "https://www.benxi.gov.cn/xw/zwyw/content_665278 (2026-07-18 招商座谈会报道)",
    },
    {
        "id": 18,
        "name": "邴忠友",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "本溪市",
        "source": "https://www.benxi.gov.cn/xw/zwyw/content_665278 (2026-07-18 招商座谈会报道)",
    },
    {
        "id": 19,
        "name": "李春",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "本溪市",
        "source": "https://www.benxi.gov.cn/xw/zwyw/content_665278 (2026-07-18 招商座谈会报道)",
    },
    {
        "id": 20,
        "name": "张维利",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "本溪市",
        "source": "https://www.benxi.gov.cn/xw/zwyw/content_665278 (2026-07-18 招商座谈会报道)",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中国共产党本溪市委员会", "type": "党委", "level": "地级市", "parent": "中国共产党辽宁省委员会", "location": "本溪市"},
    {"id": 2, "name": "本溪市人民政府", "type": "政府", "level": "地级市", "parent": "辽宁省人民政府", "location": "本溪市"},
    {"id": 3, "name": "本溪市人大常委会", "type": "人大", "level": "地级市", "parent": "辽宁省人大常委会", "location": "本溪市"},
    {"id": 4, "name": "政协本溪市委员会", "type": "政协", "level": "地级市", "parent": "政协辽宁省委员会", "location": "本溪市"},
    {"id": 5, "name": "中国共产党本溪市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共辽宁省纪律检查委员会", "location": "本溪市"},
    {"id": 6, "name": "中国共产党本溪市委员会组织部", "type": "党委", "level": "地级市", "parent": "中共辽宁省委组织部", "location": "本溪市"},
    {"id": 7, "name": "本溪市人民政府办公室", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 8, "name": "本溪市发展和改革委员会", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 9, "name": "本溪市教育局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 10, "name": "本溪市工业和信息化局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 11, "name": "本溪市公安局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 12, "name": "本溪市财政局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 13, "name": "本溪市人力资源和社会保障局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 14, "name": "本溪市自然资源局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 15, "name": "本溪市生态环境局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 16, "name": "本溪市住房和城乡建设局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 17, "name": "本溪市交通运输局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 18, "name": "本溪市水务局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 19, "name": "本溪市农业农村局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 20, "name": "本溪市商务局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 21, "name": "本溪市文化旅游和广播电视局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 22, "name": "本溪市卫生健康委员会", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 23, "name": "本溪市应急管理局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 24, "name": "本溪市审计局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 25, "name": "本溪市市场监督管理局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 26, "name": "本溪市统计局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 27, "name": "本溪市林业和草原局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 28, "name": "本溪高新技术产业开发区管理委员会", "type": "开发区", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
    {"id": 29, "name": "本溪市数据和政务服务局", "type": "政府", "level": "地级市", "parent": "本溪市人民政府", "location": "本溪市"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 王永威 - 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正厅级", "note": "中共本溪市委书记"},
    # 郭志强 - 市委副书记、市长
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "", "end": "present", "rank": "正厅级", "note": "本溪市人民政府党组书记、市长"},
    # 何庆伟 - 市人大常委会主任
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    # 高巍 - 市政协主席
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    # 曹春光 - 市委常委、组织部部长
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": "市委常委兼任组织部部长"},
    # 吕雪峰 - 副市长
    {"person_id": 6, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 殷俊 - 副市长
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 栾奎杰 - 副市长
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 张继承 - 副市长
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李众 - 副市长
    {"person_id": 10, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 王之成 - 副市长
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 潘政宗 - 市政府秘书长
    {"person_id": 12, "org_id": 7, "title": "市政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 胡桂涛 - 市委常委
    {"person_id": 13, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 刘佳 - 市委常委
    {"person_id": 14, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 初晓光 - 市委常委
    {"person_id": 15, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 刘明刚 - 市领导
    {"person_id": 16, "org_id": 2, "title": "市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待查"},
    # 董培峥 - 市领导
    {"person_id": 17, "org_id": 2, "title": "市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待查"},
    # 邴忠友 - 市领导
    {"person_id": 18, "org_id": 2, "title": "市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待查"},
    # 李春 - 市领导
    {"person_id": 19, "org_id": 2, "title": "市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待查"},
    # 张维利 - 市领导
    {"person_id": 20, "org_id": 2, "title": "市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待查"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 王永威 <-> 郭志强 - 党政主要负责人搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "市委书记与市长搭档，共同主持市委常委会、出席重大活动（2026年7月多场会议共同出席）",
     "overlap_org": "中国共产党本溪市委员会/本溪市人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 王永威 <-> 何庆伟 - 市委与市人大
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "市委理论学习中心组学习会、校友返乡行等活动中共同出席",
     "overlap_org": "本溪市",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 王永威 <-> 高巍 - 市委与市政协
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "校友返乡行、创业大会等活动中共同出席",
     "overlap_org": "本溪市",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 郭志强 <-> 何庆伟
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "市委理论学习中心组学习会共同出席",
     "overlap_org": "本溪市",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 郭志强 <-> 高巍
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "校友返乡行招商座谈会共同出席",
     "overlap_org": "本溪市",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 郭志强 <-> 潘政宗 - 市长与秘书长
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "市政府秘书长陪同市长调研（2026-07-16 矿业工业项目调研报道中确认）",
     "overlap_org": "本溪市人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 王永威 <-> 曹春光 - 书记与组织部长
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "校友返乡行大会中曹春光以市委常委、组织部部长身份主持会议",
     "overlap_org": "中国共产党本溪市委员会",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 王永威 <-> 胡桂涛 - 书记与常委
    {"person_a": 1, "person_b": 13, "type": "overlap",
     "context": "同为市委常委班子成员",
     "overlap_org": "中国共产党本溪市委员会",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 王永威 <-> 刘佳 - 书记与常委
    {"person_a": 1, "person_b": 14, "type": "overlap",
     "context": "同为市委常委班子成员",
     "overlap_org": "中国共产党本溪市委员会",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 王永威 <-> 初晓光 - 书记与常委
    {"person_a": 1, "person_b": 15, "type": "overlap",
     "context": "同为市委常委班子成员",
     "overlap_org": "中国共产党本溪市委员会",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 郭志强 <-> 栾奎杰 - 市长与副市长
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "市长与副市长，市政府领导班子成员",
     "overlap_org": "本溪市人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 郭志强 <-> 李众 - 市长与副市长
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "市长与副市长，市政府领导班子成员",
     "overlap_org": "本溪市人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 郭志强 <-> 殷俊 - 市长与副市长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "市长与副市长，市政府领导班子成员；同时出席校友返乡行座谈会",
     "overlap_org": "本溪市人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 郭志强 <-> 吕雪峰 - 市长与副市长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "市长与副市长，市政府领导班子成员",
     "overlap_org": "本溪市人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 郭志强 <-> 张继承 - 市长与副市长
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "市长与副市长，市政府领导班子成员",
     "overlap_org": "本溪市人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 郭志强 <-> 王之成 - 市长与副市长
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "市长与副市长，市政府领导班子成员",
     "overlap_org": "本溪市人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
]

# ── Build ─────────────────────────────────────────────────────────────────────

def main():
    print(f"Building {SLUG} network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    # Write person JSONs
    write_person_jsons()

    print(f"\nDone! Output files:")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    person_dir = _CURRENT_DIR / "persons"
    if person_dir.exists():
        for f in sorted(person_dir.iterdir()):
            print(f"  JSON:  {f}")


def write_person_jsons():
    """Write person graph JSON for each core figure."""
    person_dir = _CURRENT_DIR / "persons"
    person_dir.mkdir(parents=True, exist_ok=True)

    # ── 王永威 ──
    wyw = {
        "schema_version": "1.0",
        "generated_at": "2026-07-25",
        "investigation_scope": {
            "province": "辽宁省",
            "city": "本溪市",
            "region": "本溪市",
            "job": "市委书记",
            "task_id": "liaoning_本溪市",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "benxi_wang_yongwei",
            "name": "王永威",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族（推测，待确认）",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "王永威_unknown",
                "name_birthplace": "王永威_unknown",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "市委书记",
            "current_org": "中国共产党本溪市委员会",
            "administrative_rank": "正厅级",
            "as_of": "2026-07-25",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "中国共产党本溪市委员会",
                "title": "市委书记",
                "level": "正厅级",
                "location": "本溪市",
                "system": "party",
                "rank": "正厅级",
                "is_key_promotion": True,
                "notes": "2026年7月多篇官方报道确认王永威以市委书记身份出席活动",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002", "S003"]
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到王永威到任本溪市委书记的具体时间及此前履历。Baidu Baike因403验证码无法访问。",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {"org": "中国共产党本溪市委员会", "role": "市委书记", "period": "至今", "source_ids": ["S001"]}
        ],
        "relationships": [
            {"person": "郭志强", "person_id": "benxi_guo_zhiqiang",
             "relationship_type": "superior_subordinate",
             "strength": "strong",
             "evidence": "党政主要负责人搭档关系，共同主持市委常委会和重大活动",
             "overlap_org": "本溪市",
             "overlap_period": "2026-至今",
             "direction": "person_to_other",
             "confidence": "confirmed"},
            {"person": "何庆伟", "person_id": "benxi_he_qingwei",
             "relationship_type": "overlap",
             "strength": "medium",
             "evidence": "市委理论学习中心组学习会、校友返乡行等活动共同出席",
             "overlap_org": "本溪市",
             "overlap_period": "2026-至今",
             "direction": "undirected",
             "confidence": "confirmed"},
            {"person": "高巍", "person_id": "benxi_gao_wei",
             "relationship_type": "overlap",
             "strength": "medium",
             "evidence": "校友返乡行、创业大会等活动中共同出席",
             "overlap_org": "本溪市",
             "overlap_period": "2026-至今",
             "direction": "undirected",
             "confidence": "confirmed"},
            {"person": "曹春光", "person_id": "benxi_cao_chunguang",
             "relationship_type": "superior_subordinate",
             "strength": "medium",
             "evidence": "曹春光以市委常委、组织部部长身份出席并主持会议",
             "overlap_org": "中国共产党本溪市委员会",
             "overlap_period": "2026-至今",
             "direction": "person_to_other",
             "confidence": "confirmed"}
        ],
        "governance_record": [
            {
                "period": "2026",
                "domain": "economic_development",
                "achievement_or_event": "提出'4816'特色产业体系和8个产业集群、16条产业链建设",
                "role_in_event": "主导",
                "measurable_outcome": "",
                "location": "本溪市",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "period": "2026年5月",
                "domain": "economic_development",
                "achievement_or_event": "主持本溪市2026年创业大会，提出'创造创新创优创业'精神和'四全'（全域、全业、全员、全龄）创业格局",
                "role_in_event": "主导",
                "measurable_outcome": "",
                "location": "本溪市",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            },
            {
                "period": "2026年7月",
                "domain": "economic_development",
                "achievement_or_event": "主持本溪校友返乡行暨招商选资大会，推动校友经济",
                "role_in_event": "主导",
                "measurable_outcome": "",
                "location": "本溪市",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party"],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "履历待查", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "reform_oriented",
                    "evidence": "提出'创造创新创优创业'精神，强调创新驱动和产业转型",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                },
                {
                    "trait": "pragmatic",
                    "evidence": "在讲话中强调'吃透党中央精神及省委要求前提下开展工作'，'用长期思维谋划实施可持续发展的优质项目'",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "speech_themes": ["创新驱动", "产业转型", "生态立市", "工业强市", "文旅兴市", "校友经济"],
            "management_signals": [],
            "caveat": "工作风格来源于公开报道中的讲话内容，不是私人心理评估。"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月25日，在官方报道中未发现王永威涉违纪违法或负面舆情信息",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "本溪校友返乡行暨招商选资大会举行",
                "url": "https://www.benxi.gov.cn/xw/zwyw/content_665330",
                "publisher": "本溪市人民政府门户网站",
                "published_at": "2026-07-20",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认王永威为市委书记，出席讲话"
            },
            {
                "id": "S002",
                "title": "本溪市2026年创业大会举行",
                "url": "https://www.benxi.gov.cn/xw/zwyw/content_662791",
                "publisher": "本溪市人民政府门户网站",
                "published_at": "2026-05-29",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认王永威出席创业大会并发表讲话"
            },
            {
                "id": "S003",
                "title": "市委理论学习中心组举行集中学习会",
                "url": "https://www.benxi.gov.cn/xw/zwyw/content_665334",
                "publisher": "本溪市人民政府门户网站",
                "published_at": "2026-07-20",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "王永威主持会议"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "王永威的完整履历（出生年月、籍贯、教育背景、到任前职务）全部缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "王永威的出生年月、籍贯、教育背景？",
                "why_it_matters": "基本信息缺失，影响身份确认和去重",
                "suggested_queries": ["王永威 简历", "王永威 出生", "王永威 百度百科"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "critical",
                "question": "王永威何时到任本溪市委书记？此前担任什么职务？",
                "why_it_matters": "了解其晋升路径和来源，判断其政治网络",
                "suggested_queries": ["王永威 任本溪市委书记", "王永威 此前 担任"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "high",
                "question": "王永威的完整职业生涯时间线？",
                "why_it_matters": "全面了解其工作经历和政绩",
                "suggested_queries": ["王永威 任职经历"],
                "last_attempted": "2026-07-25"
            }
        ]
    }

    # ── 郭志强 ──
    gzq = {
        "schema_version": "1.0",
        "generated_at": "2026-07-25",
        "investigation_scope": {
            "province": "辽宁省",
            "city": "本溪市",
            "region": "本溪市",
            "job": "市长",
            "task_id": "liaoning_本溪市",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "benxi_guo_zhiqiang",
            "name": "郭志强",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1973年8月",
            "birthplace": "",
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": "（大学学历，具体院校未公开）",
                    "major": "",
                    "degree": "大学学历",
                    "study_type": "unknown",
                    "source_ids": ["S004"]
                }
            ],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "郭志强_1973年8月",
                "name_birthplace": "郭志强_unknown",
                "official_profile_url": "https://www.benxi.gov.cn/ld"
            }
        },
        "current_status": {
            "current_post": "市委副书记、市长",
            "current_org": "本溪市人民政府",
            "administrative_rank": "正厅级",
            "as_of": "2026-07-25",
            "is_current_confirmed": True,
            "source_ids": ["S004", "S005"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "本溪市人民政府",
                "title": "市委副书记、市长",
                "level": "正厅级",
                "location": "本溪市",
                "system": "government",
                "rank": "正厅级",
                "is_key_promotion": True,
                "notes": "主持市政府全面工作，2026年7月主持第111次常务会议",
                "confidence": "confirmed",
                "source_ids": ["S004", "S005"]
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料仅显示郭志强1973年8月生、大学学历、中共党员。到任本溪市长前完整履历缺失。Baidu Baike因403验证码无法访问。",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {"org": "中国共产党本溪市委员会", "role": "市委副书记", "period": "至今", "source_ids": ["S004"]},
            {"org": "本溪市人民政府", "role": "市长", "period": "至今", "source_ids": ["S004"]}
        ],
        "relationships": [
            {"person": "王永威", "person_id": "benxi_wang_yongwei",
             "relationship_type": "superior_subordinate",
             "strength": "strong",
             "evidence": "党政主要负责人搭档关系",
             "overlap_org": "本溪市",
             "overlap_period": "2026-至今",
             "direction": "other_to_person",
             "confidence": "confirmed"},
            {"person": "潘政宗", "person_id": "benxi_pan_zhengzong",
             "relationship_type": "superior_subordinate",
             "strength": "medium",
             "evidence": "市政府秘书长陪同市长调研",
             "overlap_org": "本溪市人民政府",
             "overlap_period": "2026-至今",
             "direction": "person_to_other",
             "confidence": "confirmed"},
            {"person": "何庆伟", "person_id": "benxi_he_qingwei",
             "relationship_type": "overlap",
             "strength": "medium",
             "evidence": "市委理论学习中心组学习会共同出席",
             "overlap_org": "本溪市",
             "overlap_period": "2026-至今",
             "direction": "undirected",
             "confidence": "confirmed"},
            {"person": "高巍", "person_id": "benxi_gao_wei",
             "relationship_type": "overlap",
             "strength": "medium",
             "evidence": "校友返乡行招商座谈会共同出席",
             "overlap_org": "本溪市",
             "overlap_period": "2026-至今",
             "direction": "undirected",
             "confidence": "confirmed"}
        ],
        "governance_record": [
            {
                "period": "2026年7月",
                "domain": "economic_development",
                "achievement_or_event": "调研推进矿业、工业重点项目，现场办公协调解决具体问题",
                "role_in_event": "主导",
                "measurable_outcome": "实地调研思山岭铁矿、太子河抽水蓄能电站等重大项目",
                "location": "本溪市",
                "confidence": "confirmed",
                "source_ids": ["S005"]
            },
            {
                "period": "2026年7月",
                "domain": "public_security",
                "achievement_or_event": "主持召开全市防汛工作会议并现场督导检查防汛备汛工作",
                "role_in_event": "主导",
                "measurable_outcome": "",
                "location": "本溪市",
                "confidence": "confirmed",
                "source_ids": ["S004"]
            },
            {
                "period": "2026年7月",
                "domain": "other",
                "achievement_or_event": "主持市政府第111次常务会议，部署防汛救灾、项目推进等工作",
                "role_in_event": "主导",
                "measurable_outcome": "",
                "location": "本溪市",
                "confidence": "confirmed",
                "source_ids": ["S004"]
            }
        ],
        "professional_profile": {
            "primary_specializations": ["经济管理", "项目建设"],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "履历不完整，无法判断晋升速度",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "grassroots_oriented",
                    "evidence": "深入井下-1060米生产一线调研矿山安全，现场办公解决项目问题",
                    "confidence": "confirmed",
                    "source_ids": ["S005"]
                },
                {
                    "trait": "pragmatic",
                    "evidence": "强调'项目为王'理念，要求'下沉一线精准服务'",
                    "confidence": "confirmed",
                    "source_ids": ["S005"]
                }
            ],
            "speech_themes": ["项目为王", "智能化绿色化融合化", "安全底线", "服务企业"],
            "management_signals": ["现场办公", "实地调研"],
            "caveat": "工作风格来源于公开报道中的行动和讲话，不是私人心理评估。"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月25日，在官方报道中未发现郭志强涉违纪违法或负面舆情信息",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S004",
                "title": "本溪市人民政府领导页面",
                "url": "https://www.benxi.gov.cn/ld",
                "publisher": "本溪市人民政府门户网站",
                "published_at": "2026",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认郭志强为市长，提供基本信息"
            },
            {
                "id": "S005",
                "title": "郭志强调研推进矿业、工业重点项目加快建设",
                "url": "https://www.benxi.gov.cn/xw/zwyw/content_665232",
                "publisher": "本溪市人民政府门户网站",
                "published_at": "2026-07-16",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认郭志强调研活动和工作风格"
            }
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "郭志强完整履历缺失，仅知基础信息"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "郭志强到任本溪市长时间及此前职务？",
                "why_it_matters": "了解其晋升路径和政治网络",
                "suggested_queries": ["郭志强 任本溪市长", "郭志强 此前 担任"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "critical",
                "question": "郭志强的籍贯、出生地？",
                "why_it_matters": "完整身份信息",
                "suggested_queries": ["郭志强 本溪 出生"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "high",
                "question": "郭志强的教育背景（大学名称、专业）？",
                "why_it_matters": "了解其专业素养背景",
                "suggested_queries": ["郭志强 学历"],
                "last_attempted": "2026-07-25"
            }
        ]
    }

    # Write files
    for fname, data in [
        (f"{TODAY}-辽宁省-本溪市-市委书记-王永威.json", wyw),
        (f"{TODAY}-辽宁省-本溪市-市长-郭志强.json", gzq),
    ]:
        path = person_dir / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path}")


if __name__ == "__main__":
    main()
