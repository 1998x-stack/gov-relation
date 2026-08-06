#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database and GEXF graph for 松原市宁江区 leadership network.

Level: 市辖区
Province: 吉林省
Parent City: 松原市
Region: 宁江区
Targets: 区委书记 & 区长

Research Date: 2026-08-06 (task jilin_宁江区)
Evidence quality: guided by the china-gov-network skill; web access degraded
(Exa rate-limited, Bing/Sogou/Yandex/DuckDuckGo captcha-gated, Baidu unavailable,
r.jina.ai down). Core facts confirmed from the official 宁江区人民政府 portal
www.ningjiang.gov.cn (primary source) and 松原市人民政府 www.jlsy.gov.cn.

CONFIRMED (primary/official, as of 2025-12 ~ 2026-07):
  - 区委书记 田宇: 主持 区委常委会2026年第10次会议 (2026-06-12);
    主持 2025年度党委（党组）书记述责述廉评议会议 (2026-01);
    主持 区七届人大六次会议 (2025-12-25); 2026-06 常委会听取区八次党代会筹备意见汇报。
  - 区委副书记、区长 荀礼: 政务网《宁江区委副书记、区长荀礼简介》(2025-04-22, 主持区政府全面工作);
    主持 2026年区政府第1次常务会议 (2026-01-15)。
  - 党政班子 (述责述廉 2026-01 与 两会 2025-12-25 台前名单):
    区委书记 田宇; 区委副书记、区长 荀礼; 区委副书记 代志宇;
    区委常委 李海江、安平来、张凯波(巡察工作领导小组组长)、李识多(副组长)、李胜、
      马志英、王宁、彭东洋、关云鹏(常委、常务副区长)、孟祥虹(常委、副区长)。
  - 区人大常委会主任/党组书记 唐艳峰; 副主任 王志海、刘继东、郭英伟;
    区政协主席 王志国。区法院院长 赵景坤; 区检察院检察长 周永福; 区武装部政委 信本雷。
  - 区政府副区长 (政务网官绍): 常务 关云鹏; 王志会(公安/司法/信访/退役军人/国动办);
    甄春蕾(人社/卫健/政务/医保)、刘小丰(教育/工信/商务/开发区)、杨天宝(农业/林业/水利/乡村振兴)、
    张东起(民政/交通/机关事务/民宗)、孟祥虹(文旅/体育、协助常务)。

UNVERIFIED / open gaps (见 report/open_gaps.md 与各 person JSON open_questions):
  - 田宇、荀礼 出生、籍贯、学历、入党/参工时间，以及任区委书记/区长前完整晋升履历。
  - 各区级领导 (代志宇、唐艳峰、王志国、张凯波、关云鹏等) 完整履历。
  - 田宇/荀礼 前任 (上届区委书记、前任区长) 姓名与去向；跨县区干部交流具体任免证据。

regional: 松原市政治、经济、文化中心; 幅员面积 1313 km²; 辖 17 街道 62 社区、5 乡镇 82 行政村
以及 3 个工业园区; 总人口 60 万 (农业人口 10 万); 汉满蒙回朝等 20 余民族。
素有"粮仓、肉库、渔乡、油海"之誉 (石油/天然气/油页岩资源丰富, 吉林油田所在地)。
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

_BASE = Path(__file__).resolve().parent
while _BASE != _BASE.parent and not (_BASE / "gov_relation").is_dir():
    _BASE = _BASE.parent
sys.path.insert(0, str(_BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "宁江区"

# 入库（暂存/规范化）用 STAGING_DIR 环境变量覆盖输出目录；否则写规范化目录
_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(_STAGING, f"{SLUG}_network.gexf")
else:
    DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
    GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共松原市宁江区委员会", "type": "党委", "level": "县处级",
     "parent": "中共松原市委", "location": "吉林省松原市宁江区"},
    {"id": 2, "name": "松原市宁江区人民政府", "type": "政府", "level": "县处级",
     "parent": "松原市人民政府", "location": "吉林省松原市宁江区"},
    {"id": 3, "name": "松原市宁江区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "松原市人大常委会", "location": "吉林省松原市宁江区"},
    {"id": 4, "name": "中国人民政治协商会议松原市宁江区委员会", "type": "政协", "level": "县处级",
     "parent": "政协松原市委员会", "location": "吉林省松原市宁江区"},
    {"id": 5, "name": "松原市宁江区纪律检查委员会/宁江区监察委员会", "type": "纪委", "level": "县处级",
     "parent": "中共松原市纪委", "location": "吉林省松原市宁江区"},
    {"id": 6, "name": "中共松原市宁江区委巡察工作领导小组办公室", "type": "党委", "level": "副处级",
     "parent": "中共松原市宁江区委员会", "location": "吉林省松原市宁江区"},
    {"id": 7, "name": "松原市宁江区人民法院", "type": "政法", "level": "县处级",
     "parent": "吉林省高级人民法院", "location": "吉林省松原市宁江区"},
    {"id": 8, "name": "松原市宁江区人民检察院", "type": "政法", "level": "县处级",
     "parent": "松原市人民检察院", "location": "吉林省松原市宁江区"},
    {"id": 9, "name": "松原市宁江区人民武装部", "type": "政府", "level": "县处级",
     "parent": "松原军分区", "location": "吉林省松原市宁江区"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 田宇 — 区委书记 (confirmmed, primary)
    {"id": 1, "name": "田宇", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "松原市宁江区委书记（区委常委会主持，区八次党代会筹备中）",
     "current_org": "中共松原市宁江区委员会",
     "source": "http://www.ningjiang.gov.cn/zwgk/zwgk/202606/t20260622_574093.html"},
    # 2 — 荀礼 — 区长
    {"id": 2, "name": "荀礼", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区委副书记、区人民政府区长、区政府党组书记",
     "current_org": "松原市宁江区人民政府",
     "source": "http://www.ningjiang.gov.cn/zwgk/zfld/202504/t20250422_549202.html"},
    # 3 — 代志宇 — 区委副书记
    {"id": 3, "name": "代志宇", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区委副书记",
     "current_org": "中共松原市宁江区委员会",
     "source": "http://www.ningjiang.gov.cn/zwgk/zwgk/202601/t20260127_566192.html"},
    # 4 — 唐艳峰 — 区人大主任
    {"id": 4, "name": "唐艳峰", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区人大常委会主任、党组书记",
     "current_org": "松原市宁江区人民代表大会常务委员会",
     "source": "http://www.ningjiang.gov.cn/zwgk/zwgk/202601/t20260115_565460.html"},
    # 5 — 王志国 — 区政协主席
    {"id": 5, "name": "王志国", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区政协主席",
     "current_org": "中国人民政治协商会议松原市宁江区委员会",
     "source": "http://www.ningjiang.gov.cn/zwgk/zwgk/202512/t20251229_564375.html"},
    # 6 — 关云鹏 — 区委常委、常务副区长
    {"id": 6, "name": "关云鹏", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区委常委、常务副区长",
     "current_org": "松原市宁江区人民政府",
     "source": "http://www.ningjiang.gov.cn/zwgk/zfld/202606/t20260602_573247.html"},
    # 7 — 孟祥虹 — 区委常委、副区长
    {"id": 7, "name": "孟祥虹", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区委常委、副区长",
     "current_org": "松原市宁江区人民政府",
     "source": "http://www.ningjiang.gov.cn/zwgk/zfld/202606/t20260602_573248.html"},
    # 8 — 张凯波 — 区委常委、区委巡察工作领导小组组长
    {"id": 8, "name": "张凯波", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区委常委、区委巡察工作领导小组组长",
     "current_org": "中共松原市宁江区委员会",
     "source": "http://www.ningjiang.gov.cn/zwgk/zwgk/202604/t20260416_570804.html"},
    # 9 — 李识多 — 区委常委、巡察工作领导小组副组长
    {"id": 9, "name": "李识多", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区委常委、巡察工作领导小组副组长",
     "current_org": "中共松原市宁江区委员会",
     "source": "http://www.ningjiang.gov.cn/zwgk/zwgk/202604/t20260416_570804.html"},
    # 10 — 王志会 — 副区长（政法/公安）
    {"id": 10, "name": "王志会", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区人民政府副区长",
     "current_org": "松原市宁江区人民政府",
     "source": "http://www.ningjiang.gov.cn/zwgk/zfld/202303/t20230314_490967.html"},
    # 11 — 甄春蕾 — 副区长（人社/卫健）
    {"id": 11, "name": "甄春蕾", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区人民政府副区长",
     "current_org": "宁江区人民政府",
     "source": "http://www.ningjiang.gov.cn/zwgk/zfld/202601/t20260104_564760.html"},
    # 12 — 刘小丰 — 副区长（教育/工信/商务）
    {"id": 12, "name": "刘小丰", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区人民政府副区长",
     "current_org": "宁江区人民政府",
     "source": "http://www.ningjiang.gov.cn/zwgk/zfld/202606/t20260602_573249.html"},
    # 13 — 杨天宝 — 副区长（农业/乡村振兴）
    {"id": 13, "name": "杨天宝", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区人民政府副区长",
     "current_org": "宁江区人民政府",
     "source": "http://www.ningjiang.gov.cn/zwgk/zfld/202606/t20260602_573250.html"},
    # 14 — 张东起 — 副区长（民政/交通）
    {"id": 14, "name": "张东起", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区人民政府副区长",
     "current_org": "宁江区人民政府",
     "source": "http://www.ningjiang.gov.cn/zwgk/zfld/202606/t20260602_573251.html"},
    # 15 — 赵景坤 — 区法院院长
    {"id": 15, "name": "赵景坤", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区人民法院院长",
     "current_org": "松原市宁江区人民法院",
     "source": "http://www.ningjiang.gov.cn/zwgk/zwgk/202512/t20251229_564375.html"},
    # 16 — 周永福 — 区检察院检察长
    {"id": 16, "name": "周永福", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区人民检察院检察长",
     "current_org": "松原市宁江区人民检察院",
     "source": "http://www.ningjiang.gov.cn/zwgk/zwgk/202512/t20251229_564375.html"},
    # 17 — 信本雷 — 区武装部政委
    {"id": 17, "name": "信本雷", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁江区人民武装部政治委员",
     "current_org": "松原市宁江区人民武装部",
     "source": "http://www.ningjiang.gov.cn/zwgk/zwgk/202512/t20251229_564375.html"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 田宇 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "宁江区委书记", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "主持区委常委会(2026-06-12第10次)、2025年度述责述廉(2026-01)、区七届人大六次会议(2025-12-25)"},
    # 荀礼 — 区长
    {"person_id": 2, "org_id": 2, "title": "宁江区委副书记、区人民政府", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "主持区政府全面工作; 主持2026年区政府第1次常务会议(2026-01-15)"},
    {"person_id": 2, "org_id": 1, "title": "宁江区委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 代志宇 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "宁江区委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 唐艳峰 — 人大主任
    {"person_id": 4, "org_id": 3, "title": "宁江区人大常委会主任、党组书记", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "主持区人大常委会党组会议(2026-01-08)"},
    # 王志国 — 政协主席
    {"person_id": 5, "org_id": 4, "title": "宁江区政协主席", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": ""},
    # 关云鹏 — 区委常委/常务副区长
    {"person_id": 6, "org_id": 1, "title": "宁江区委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "宁江区常务副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "负责区政府常务工作，分管区财政局/发改局/住建局等"},
    # 孟祥虹 — 区委常委/副区长
    {"person_id": 7, "org_id": 1, "title": "宁江区委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "宁江区政府副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管文旅/体育，协助常务副区长"},
    # 张凯波 — 区委常委/巡察组长
    {"person_id": 8, "org_id": 1, "title": "宁江区委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "区委巡察工作领导小组组长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "七届区委第八轮巡察动员部署会议讲话(2026-04)"},
    # 李识多 — 区委常委/巡察副组长
    {"person_id": 9, "org_id": 1, "title": "宁江区委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "区委巡察工作领导小组副组长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 王志会 — 副区长（政法）
    {"person_id": 10, "org_id": 2, "title": "宁江区政府副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管区公安/司法/信访/退役; 双拥城创建"},
    # 甄春蕾 — 副区长（人社/卫健）
    {"person_id": 11, "org_id": 2, "title": "宁江区政府副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管人社/卫健/政务服务和数字化建设"},
    # 刘小丰 — 副区长（教育/工信）
    {"person_id": 12, "org_id": 2, "title": "宁江区政府副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管教育/工信/商务/开发区(吉林宁江经济开发区)"},
    # 杨天宝 — 副区长（农业/乡村振兴）
    {"person_id": 13, "org_id": 2, "title": "宁江区政府副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管农业农村(乡村振兴)/林业/水利/乡镇工作"},
    # 张东起 — 副区长（民政/交通）
    {"person_id": 14, "org_id": 2, "title": "宁江区政府副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "分管民政/交通/机关事务管理局"},
    # 赵景坤 — 法院院长
    {"person_id": 15, "org_id": 7, "title": "宁江区人民法院院长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 周永福 — 检察院检察长
    {"person_id": 16, "org_id": 8, "title": "宁江区人民检察院检察长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 信本雷 — 武装部政委
    {"person_id": 17, "org_id": 9, "title": "宁江区人民武装部政治委员", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 党政正职
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区政府局长（党政班一把手）宁江区党政班子", "overlap_org": "中共松原市宁江区委员会", "overlap_period": "current"},
    # 区委班子核心
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委书记与区委副书记（代志宇）党政班子核心", "overlap_org": "中共宁江区委员会", "overlap_period": "current"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "区长与区委副书记（代志宇）同届党政班子", "overlap_org": "中共宁江区委员会", "overlap_period": "current"},
    # 区委书记与常委
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "区委书记与区委常委、常务副区长", "overlap_org": "中共宁江区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "区委书记与区委常委、副区长孟祥虹", "overlap_org": "中共宁江区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "区委书记与区委常委、区委巡察工作领导小组组长", "overlap_org": "中共宁江区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "区委书记与区委常委、巡察工作领导小组副组长", "overlap_org": "中共宁江区委员会", "overlap_period": "2026"},
    # 区长与副区长
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "区长与常务副区长（政府工作日常）", "overlap_org": "宁江区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "区长与副区长（政法/公安）政府班子", "overlap_org": "宁江区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 11, "type": "overlap",
     "context": "区长与副区长（人社/卫健）政府班子", "overlap_org": "宁江区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 12, "type": "overlap",
     "context": "区长与副区长（教育/工业/开发区）政府班子", "overlap_org": "宁江区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 13, "type": "overlap",
     "context": "区长与副区长（农业/乡村振兴）政府班子", "overlap_org": "宁江区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 14, "type": "overlap",
     "context": "区长与副区长（民政/交通）政府班子", "overlap_org": "宁江区人民政府", "overlap_period": "current"},
    # 区委书记与人大/政协/政法
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与区人大主任（两会/党组成员）", "overlap_org": "宁江区", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与区政协主席（两会）", "overlap_org": "宁江区", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "区政府局长与区人大主任（政*两*工作交叉）", "overlap_org": "宁江区", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 15, "type": "overlap",
     "context": "区委书记与区法院院长（两会台前）", "overlap_org": "宁江区", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 16, "type": "overlap",
     "context": "区委书记与区检察院检察长（两会台前）", "overlap_org": "宁江区", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 17, "type": "overlap",
     "context": "区委书记与区武装部政委（两会台前）", "overlap_org": "宁江区", "overlap_period": "2025-2026"},
    # 人大与政府
    {"person_a": 4, "person_b": 6, "type": "overlap",
     "context": "区人大主任与常务副区长", "overlap_org": "宁江区", "overlap_period": "2026"},
]

if __name__ == "__main__":
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
    print(f"\nDone: {SLUG} staging build complete.")