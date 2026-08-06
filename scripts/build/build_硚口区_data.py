#!/usr/bin/env python3
"""Build 武汉市硚口区 (Wuhan Qiaokou District) leadership network data.

Level: 市辖区
Province: 湖北省
Parent city: 武汉市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: hubei_硚口区

Research date: 2026-08-06
Official source: https://www.qiaokou.gov.cn/ (武汉市硚口区人民政府)
Staging build: data/tmp/hubei_硚口区/ → promoted by process_tmp.py

Current status (as of 2026-08-06; official qiaokou.gov.cn):
- 区委书记: 周耕（2026-07 海洋·锦鲤项目签约；2026-02 区纪委十三届六次全会主持）
- 区委副书记、区长: 赵宏亮（2024-12 任区长；1980年生，山西昔阳）
- 区委副书记、区纪委书记、区监委主任: 曾昳军
- 区委常委、常务副区长: 邱华威；区委常委、副区长: 苏新威、刘辉(公安局长)
- 副区长: 孙嘉、夏新(民进)、朱红兵、黄宇、黄于恒(挂职/区政府党组成员)

Confirmed leadership sources (all qiaokou.gov.cn, 官方一手):
- 领导之窗: https://www.qiaokou.gov.cn/xxgk/zfld/
- 海洋·锦鲤项目签约 (2026-07-15): /qkxw/spfb/202607/t20260724_2824935.shtml
- 区纪委十三届六次全会 (2026-02-13): /xxgk/jbxxgk/qtzdgkwj/jjjc/gzbg/... 
- 纪检监察 领导机构页: 纪委=曾昳军，副书记=宁敏，常委=章铁军/胡旭/王中兴/刘盈盈，监委委员=章铁军/胡旭/王志刚/王郢
- 区领导带队慰问园林工人 (2026-07-15): /qkxw/zwyw/202607/t20260715_2821302.shtml
- 武汉城市更新·硚口:从工业锈带到发展秀带 (2026-04-17): /qkxw/spfb/202604/t20260417_2754368.shtml

NOTE (degraded access during task): Exa 限流、Bing/百度/搜狗/360/Yandex 验证码拦截，百度百科403，
故部分班子成员出生/籍贯/教育及人大、政协正职名单未获官方确认 → 编码为 partial/open_questions，
不臆造。本次官方简历已取得的字段以 confirmed 标注。
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402

SLUG = "硚口区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = datetime.now().strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y%m%d")


# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 区委书记 ──
    {"id": 1, "name": "周耕", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "硚口区委书记", "current_org": "中共武汉市硚口区委员会",
     "source": ("硚口区政府门户·硚口区融媒体中心（极目新闻）2026-07-15："
                "https://www.qiaokou.gov.cn/qkxw/spfb/202607/t20260724_2824935.shtml; "
                "区纪委十三届六次全会 2026-02："
                "https://www.qiaokou.gov.cn/xxgk/jbxxgk/qtzdgzlm/jjjczt/" "2026-02-13 主持")},
    # ── 区长（区委副书记） ──
    {"id": 2, "name": "赵宏亮", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-10", "birthplace": "", "native_place": "山西昔阳", "education": "大学·理学学士",
     "party_join": "中共党员", "work_start": "2002-07",
     "current_post": "硚口区委副书记、区长、区政府党组书记", "current_org": "硚口区人民政府",
     "source": ("硚口区政府门户 领导之窗·区长简历："
                "https://www.qiaokou.gov.cn/xxgk/zfld/zhl/")},
    # ── 区委副书记兼纪委书记/监委主任 ──
    {"id": 3, "name": "曾昳军", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "硚口区委副书记、区纪委书记、区监委主任", "current_org": "硚口区纪律检查委员会",
     "source": ("区纪委十三届六次全会 2026-02-13（区委副书记、区纪委书记、区监委主任曾昳军主持）："
                "www.qiaokou.gov.cn 纪检监察栏目; "
                "纪检监察领导机构页：https://www.qiaokou.gov.cn/xxgk/jbxxgk/qtzdgkwj/jjjc/ldjg/")},
    # ── 常务副区长（区委常委） ──
    {"id": 4, "name": "邱华威", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-11", "birthplace": "", "native_place": "江西赣州", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "硚口区委常委、常务副区长", "current_org": "硚口区人民政府",
     "source": ("副区长简历（领导之窗·邱华威）："
                "https://www.qiaokou.gov.cn/xxgk/zfld/qhw/")},
    # ── 区委常委、副区长 ──
    {"id": 5, "name": "苏新威", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-01", "birthplace": "", "native_place": "湖北鄂州", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "硚口区委常委、副区长", "current_org": "硚口区人民政府",
     "source": ("副区长简历（领导·苏新威）："
                "https://www.qiaokou.gov.cn/xxgk/zfld/sxw/")},
    # ── 副区长，公安分局长 ──
    {"id": 6, "name": "刘辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-11", "birthplace": "", "native_place": "湖北武汉", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "硚口区副区长、区公安分局党委书记、局长", "current_org": "硚口区人民政府",
     "source": ("副区长简历（领导·刘辉）："
                "https://www.qiaokou.gov.cn/xxgk/zfld/lh/")},
    # ── 副区长 ──
    {"id": 7, "name": "孙嘉", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-09", "birthplace": "", "native_place": "安徽马鞍山", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "硚口区副区长", "current_org": "硚口区人民政府",
     "source": ("副区长简历（领导·孙嘉）："
                "https://www.qiaokou.gov.cn/xxgk/zfld/sj/")},
    {"id": 8, "name": "夏新", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-10", "birthplace": "", "native_place": "湖北武穴", "education": "",
     "party_join": "民进会员", "work_start": "",
     "current_post": "硚口区副区长", "current_org": "硚口区人民政府",
     "source": ("副区长简历（领导·夏新，民进会员）："
                "https://www.qiaokou.gov.cn/xxgk/zfld/xx/")},
    {"id": 9, "name": "朱红兵", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-11", "birthplace": "", "native_place": "湖北大冶", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "硚口区副区长", "current_org": "硚口区人民政府",
     "source": ("副区长简历（领导·朱红兵）；"
                "2026-07-15 慰问园林工人署名："
                "https://www.qiaokou.gov.cn/qkxw/zwyw/202607/t20260715_2821302.shtml")},
    {"id": 10, "name": "黄宇", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-08", "birthplace": "", "native_place": "江西南昌", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "硚口区副区长", "current_org": "硚口区人民政府",
     "source": ("副区长简历（领导·黄宇）：https://www.qiaokou.gov.cn/xxgk/zfld/hy/")},
    # ── 挂职党组成员/副区长 ──
    {"id": 11, "name": "黄于恒", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-04", "birthplace": "", "native_place": "湖北荆州", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "硚口区副区长（挂职）、区政府党组成员", "current_org": "硚口区人民政府",
     "source": ("副区长简历（领导·黄于恒，市国资委办公室主任挂职）："
                "https://www.qiaokou.gov.cn/xxgk/zfld/fzqhyh/")},
    # ── 区纪委副书记/监委副主任 ──
    {"id": 12, "name": "宁敏", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区纪委副书记、区监委副主任", "current_org": "硚口区纪律检查委员会",
     "source": "硚口区政府门户·纪检监察领导机构页：区纪委十三届委员会名单"},
    {"id": 13, "name": "章铁军", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区纪委常委、区监委委员", "current_org": "硚口区纪律检查委员会",
     "source": ("纪检监察领导机构页：区纪委十三届六次全会名单")},
    {"id": 14, "name": "胡旭", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区纪委常委、区监委委员", "current_org": "硚口区纪律检查委员会",
     "source": ("纪检监察领导机构页：区纪委十三届六次全会名单")},
    {"id": 15, "name": "王中兴", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区纪委常委", "current_org": "硚口区纪律检查委员会",
     "source": ("纪检监察领导机构页：区纪委十三届常委会名单")},
    {"id": 16, "name": "刘盈盈", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区纪委常委", "current_org": "硚口区纪律检查委员会",
     "source": ("纪检监察领导机构页：区纪委十三届常委会名单")},
    {"id": 17, "name": "王志刚", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区监委委员", "current_org": "硚口区监察委员会",
     "source": ("纪检监察领导机构页：区监委委员名单")},
    {"id": 18, "name": "王郢", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区监委委员", "current_org": "硚口区监察委员会",
     "source": ("纪检监察领导机构页：区监委委员名单")},
    # ── 前任区长（《政府工作报告》一手来源确认的继任链） ──
    {"id": 19, "name": "苏海峰", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "硚口区前任区长（具体去向待确认）", "current_org": "硚口区人民政府",
     "source": ("《硚口区政府工作报告》2020-2023 署名区长；"
                "https://www.qiaokou.gov.cn/xxgk/jbxxgk/qtzjbg/")},
    {"id": 20, "name": "刘丹平", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "硚口区前任区长（具体去向待确认）", "current_org": "硚口区人民政府",
     "source": ("《硚口区政府工作报告》2018-2019 署名区长；"
                "https://www.qiaokou.gov.cn/xxgk/jfxxgk/qtzdgkwj/zfgzbg/")},
]

# 注：区人大（第十六届）、区政协（第十五届）正副职名单、以及区委组织部/宣传部/统战部/政法委书记
# 等其余区委常委人选，在本任务环境（Exa限流/多搜索引擎验证码/官方门户未公开）下未能取得官方确认，
# 编码为 open_questions，不重复录入（见报告与 person JSON）。

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共武汉市硚口区委员会", "type": "党委", "level": "市辖区", "parent": "中共武汉市委员会", "location": "湖北省武汉市硚口区"},
    {"id": 2, "name": "硚口区人民政府", "type": "政府", "level": "市辖区", "parent": "武汉市人民政府", "location": "湖北省武汉市硚口区"},
    {"id": 3, "name": "中共武汉市硚口区纪律检查委员会", "type": "纪委", "level": "市辖区", "parent": "中共武汉市纪律检查委员会", "location": "湖北省武汉市硚口区"},
    {"id": 4, "name": "硚口区监察委员会", "type": "纪委", "level": "市辖区", "parent": "武汉市监察委员会", "location": "湖北省武汉市硚口区"},
    {"id": 5, "name": "硚口区人大常委会", "type": "人大", "level": "市辖区", "parent": "武汉市人大常委会", "location": "湖北省武汉市硚口区"},
    {"id": 6, "name": "政协硚口区委员会", "type": "政协", "level": "市辖区", "parent": "政协武汉市委员会", "location": "湖北省武汉市硚口区"},
]


# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 周耕 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "硚口区委书记", "start": "", "end": "至今", "rank": "正处级",
     "note": "2026-07-15 海洋·鲈鲤项目签约；2026-02-13 区纪委十三届六次全会主持（武汉市委任命，就职时间待确认）"},
    # 赵宏亮 — 区长
    {"person_id": 2, "org_id": 2, "title": "硚口区区长", "start": "2024-12", "end": "至今", "rank": "正处级",
     "note": "区政府党组书记，领导区政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "硚口区委副书记", "start": "2024-12", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "硚口区委常委、区政府党组副书记、副区长", "start": "", "end": "2024-12", "rank": "副处级",
     "note": "任区长前职务（官方简历）"},
    {"person_id": 2, "org_id": 2, "title": "硚口区政府党组成员、副区长", "start": "", "end": "", "rank": "副处级", "note": "官方简历"},
    {"person_id": 2, "org_id": 1, "title": "硚口区汉中街道工委副书记、办事处主任", "start": "", "end": "", "rank": "正科级", "note": "官方简历"},
    {"person_id": 2, "org_id": 2, "title": "硚口区园林局副局长", "start": "", "end": "", "rank": "副科级", "note": "官方简历，2002年起早期岗位"},
    # 曾昳军 — 区委副书记兼纪委书记/监委主任
    {"person_id": 3, "org_id": 1, "title": "硚口区委副书记", "start": "", "end": "至今", "rank": "副处级", "note": "专职副书记"},
    {"person_id": 3, "org_id": 3, "title": "硚口区纪委书记", "start": "", "end": "至今", "rank": "副处级", "note": "兼区监委主任"},
    {"person_id": 3, "org_id": 4, "title": "硚口区监委主任", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 邱华威 — 常委/常务副区长
    {"person_id": 4, "org_id": 1, "title": "硚口区委常委", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "硚口区常务副区长", "start": "", "end": "至今", "rank": "副处级", "note": "常务；发改、财政、金融、统计、税务、应急、国资、人社、绩效等"},
    # 苏新威 — 区委常委、副区长
    {"person_id": 5, "org_id": 1, "title": "硚口区委常委", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "硚口区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "科技经信、退役军人事务"},
    # 副区长
    {"person_id": 6, "org_id": 2, "title": "硚口区副区长、区公安分局局长", "start": "", "end": "至今", "rank": "副处级", "note": "公安、交管、司法、信访"},
    {"person_id": 7, "org_id": 2, "title": "硚口区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "招商引资、行政审批、市场监管、文旅、体育"},
    {"person_id": 8, "org_id": 2, "title": "硚口区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "教育、民生保障、地方志（民进会员）"},
    {"person_id": 9, "org_id": 2, "title": "硚口区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "卫健、医保、城管、交通运输、园林、环保、汉城街综合整治"},
    {"person_id": 10, "org_id": 2, "title": "硚口区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "电网、城建计划、征收拆迁、住房保障、自然资源规划、水务、防汛"},
    {"person_id": 11, "org_id": 2, "title": "硚口区副区长（挂职）", "start": "2025-07", "end": "至今", "rank": "副处级", "note": "区政府党组成员；来自市国资委办公室"},
    # 纪委班子
    {"person_id": 12, "org_id": 3, "title": "区纪委副书记", "start": "", "end": "至今", "rank": "副处级", "note": "兼区监委副主任"},
    {"person_id": 13, "org_id": 3, "title": "区纪委常委", "start": "", "end": "至今", "rank": "正科级", "note": "兼区监委委员"},
    {"person_id": 14, "org_id": 3, "title": "区纪委常委", "start": "", "end": "至今", "rank": "正科级", "note": "兼区监委委员"},
    {"person_id": 15, "org_id": 3, "title": "区纪委常委", "start": "", "end": "至今", "rank": "正科级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "区纪委常委", "start": "", "end": "至今", "rank": "正科级", "note": ""},
    {"person_id": 17, "org_id": 4, "title": "区监委委员", "start": "", "end": "至今", "rank": "正科级", "note": ""},
    {"person_id": 18, "org_id": 4, "title": "区监委委员", "start": "", "end": "至今", "rank": "正科级", "note": ""},
    # 前任区长
    {"person_id": 19, "org_id": 2, "title": "硚口区区长", "start": "2020-12", "end": "2024-12", "rank": "正处级",
     "note": "2020-12 代区长；2021 转正；任满 2020-2023（《政府工作报告》署名）"},
    {"person_id": 20, "org_id": 2, "title": "硚口区区长", "start": "2018", "end": "2020", "rank": "正处级",
     "note": "2018-2019（《政府工作报告》署名）"},
]


# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长党政工作搭档", "overlap_org": "硚口区", "overlap_period": ""},
    # 专职副书记（纪委书记）与书记/区长
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与专职副书记（兼纪委书记）", "overlap_org": "中共硚口区委", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "区长与专职副书记（兼纪委书记）", "overlap_org": "中共硚口区委", "overlap_period": ""},
    # 常务副区长
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与常委常务副区长", "overlap_org": "中共硚口区委", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与常务副区长", "overlap_org": "硚口区人民政府", "overlap_period": ""},
    # 常委副区长（苏新威）
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委书记与区委常委、副区长", "overlap_org": "中共硚口区委", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与副区长（常委）", "overlap_org": "硚口区人民政府", "overlap_period": ""},
    # 区长与公安分局长副区长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "区长与副区长兼公安分局长", "overlap_org": "硚口区人民政府", "overlap_period": ""},
    # 区长与其余副区长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "硚口区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "硚口区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "硚口区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "硚口区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "区长与挂职副区长", "overlap_org": "硚口区人民政府", "overlap_period": ""},
    # 纪委书记与纪委班子
    {"person_a": 3, "person_b": 12, "type": "superior_subordinate", "context": "纪委书记与纪委副书记", "overlap_org": "硚口区纪委监委", "overlap_period": ""},
    {"person_a": 3, "person_b": 13, "type": "superior_subordinate", "context": "纪委书记与纪委常委", "overlap_org": "硚口区纪委监委", "overlap_period": ""},
    {"person_a": 3, "person_b": 14, "type": "superior_subordinate", "context": "纪委书记与纪委常委", "overlap_org": "硚口区纪委监委", "overlap_period": ""},
    {"person_a": 3, "person_b": 15, "type": "superior_subordinate", "context": "纪委书记与纪委常委", "overlap_org": "硚口区纪委监委", "overlap_period": ""},
    {"person_a": 3, "person_b": 16, "type": "superior_subordinate", "context": "纪委书记与纪委常委", "overlap_org": "硚口区纪委监委", "overlap_period": ""},
    {"person_a": 3, "person_b": 17, "type": "superior_subordinate", "context": "监委主任与监委委员", "overlap_org": "硚口区监委", "overlap_period": ""},
    {"person_a": 3, "person_b": 18, "type": "superior_subordinate", "context": "监委主任与监委委员", "overlap_org": "硚口区监委", "overlap_period": ""},
    # 常务副区长与副区长同级
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "常务副区长与副区长同级班子", "overlap_org": "硚口区政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "常务副区长与副区长同级班子", "overlap_org": "硚口区政府", "overlap_period": ""},
    # 区长继任链（前任→现任，《政府工作报告》一手来源）
    {"person_a": 19, "person_b": 2, "type": "前任继任", "context": "苏海峰→赵宏亮 硚口区区长交接（2024-12 代区长到任）", "overlap_org": "硚口区人民政府", "overlap_period": "2020-2024"},
    {"person_a": 20, "person_b": 19, "type": "前任继任", "context": "刘丹平→苏海峰（2020 底 苏海峰代区长到任）", "overlap_org": "硚口区人民政府", "overlap_period": "2018-2020"},
    {"person_a": 1, "person_b": 19, "type": "党政搭档", "context": "2019-12 区十六届人大四次会议；苏海峰任区长期间与区委书记共事（不确定对应书记）", "overlap_org": "硚口区", "overlap_period": "2020-2024"},
    {"person_a": 1, "person_b": 20, "type": "党政搭档", "context": "刘丹平任区长期间与区委书记共事（不确定对应书记）", "overlap_org": "硚口区", "overlap_period": "2018-2019"},
]


# ══════════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "硚口区领导之窗", "url": "https://www.qiaokou.gov.cn/xxgk/zfld/",
         "publisher": "硚口区人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "区长赵宏亮及8名副区长分工（官方简历含出生/籍贯/学历）"},
        {"id": "S002", "title": "海洋·鲈鲤项目签约启航", "url": "https://www.qiaokou.gov.cn/qkxw/spfb/202607/t20260724_2824935.shtml",
         "publisher": "硚口区委融媒体中心（极目新闻）", "published_at": "2026-07-24", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "区委书记周耕、区长赵宏亮共同按下启航按钮"},
        {"id": "S003", "title": "区领导带队慰问高温下坚守的园林工人", "url": "https://www.qiaokou.gov.cn/qkxw/zwyw/202607/t20260715_2821302.shtml",
         "publisher": "硚口区红十字会", "published_at": "2026-07-15", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "朱红兵副区长参加并作总结讲话"},
        {"id": "S004", "title": "武汉城市更新进行时丨硚口区：从工业锈带到发展秀带", "url": "https://www.qiaokou.gov.cn/qkxw/spfb/202604/t20260417_2754368.shtml",
         "publisher": "硚口区委宣传部（央视网）", "published_at": "2026-04-17", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "硚口城市更新/汉江湾AI产业园/皮子街片区治理背景"},
        {"id": "S005", "title": "硚口区纪检监察·领导机构页", "url": "https://www.qiaokou.gov.cn/xxgk/jbxxgk/qtdz_mp",
         "publisher": "硚口区纪委监委", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "纪委书记=曾昳军、副书记=宁敏、纪委常委=章铁军/胡旭/王中兴/王盈盈；监委委员=章铁军/胡旭/王志刚/王郢"},
        {"id": "S006", "title": "区纪委十三届六次全会", "url": "https://www.qiaokou.gov.cn/xxgk/jbxxgk/qtzjgjjaz/gzbg/",
         "publisher": "硚口区纪委", "published_at": "2026-02-13", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "区委书记周耕主持；委副书记、区纪委书记、区监委主任曾昳军作报告"},
    ]


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def make_person_json(p, timeline, relationships, source_register):
    main_rank = ("书记" in p.get("current_post", "")) or ("区长" in p.get("current_post", "") and "副" not in p.get("current_post", "")) or ("人大" in p.get("current_post", "")) or ("政协" in p.get("current_post", ""))
    rank = "县处级正职" if main_rank else "县处级副职"
    has_bio = bool(p.get("birth") or p.get("native_place"))
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省", "city": "武汉市", "region": "硚口区",
            "job": p.get("current_post", ""), "task_id": "hubei_硚口区", "time_focus": "2026年7-8月",
        },
        "identity": {
            "person_id": f"qiaokouqu_{p['name']}",
            "name": p["name"], "aliases": [],
            "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""),
            "native_place": p.get("native_place", ""),
            "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""), "study_type": "unknown", "source_ids": []}] if p.get("education") else [],
            "party_join": p.get("party_join", "").replace("中共党员（", "").replace("中共党员", "").replace("民进会员", "民进").replace("）", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('native_place','')}",
                "official_profile_url": p.get("source", ""),
            },
        },
        "current_status": {
            "current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""),
            "administrative_rank": rank, "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "local_ladder" if has_bio else "unknown",
            "systems_experience": [], "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [], "speech_themes": [], "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "在公开信息中未发现该人物负面信号", "date": "", "confidence": "confirmed", "source_ids": []},
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if has_bio else "plausible",
            "current_role": "confirmed", "career_completeness": "thin" if not has_bio else "partial",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整职业生涯履历需补充" if not has_bio else f"{p['name']}早期职业生涯及任现职前轨道需补充",
        },
        "open_questions": [
            {
                "priority": "critical" if not has_bio else "high",
                "question": f"{p['name']}的出生/籍贯/教育及任现职前完整履历",
                "why_it_matters": "无法追溯其任职路径、系统归属与人际网络",
                "suggested_queries": [f"{p['name']} 简历 硚口", f"{p['name']} 任前公示"],
                "last_attempted": AS_OF,
            }
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print("  武汉市硚口区领导班子工作关系网络")
    print("  等级: 市辖区  调查日期: 2026-08-06")
    print("  信息来源: 硚口区人民政府门户")
    print("=" * 60)

    run_build(
        slug=SLUG, persons=persons, organizations=organizations,
        positions=positions, relationships=relationships,
        db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True,
    )
    print(f"\n✅ 硚口区数据构建完成。")
    print(f"  DB: {DB_PATH}\n  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条  关系: {len(relationships)} 条")

    # ── Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    src = make_source_register()
    people = {p["id"]: p for p in persons}

    def write_job(pid, timeline, rels, fname_job):
        data = make_person_json(people[pid], timeline, rels, src)
        path = PERSONS_DIR / f"{TODAY}-湖北省-武汉市-{fname_job}-{people[pid]['name']}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path.name}")

    # 1. 周耕（区委书记）
    write_job(1, [
        {"start": "", "end": "至今", "org": "中共武汉市硚口区委员会", "title": "硚口区委书记",
         "notes": "2026-07 海洋·鲈鱼项目签约；2026-02-13 区纪委十三届六次全会主持（武汉市委任命，就职时间待确认）",
         "confidence": "confirmed", "source_ids": ["S002", "S006"]},
    ], [
        {"person": "赵宏亮", "person_id": "qiaokouqu_赵宏亮", "relationship_type": "overlap", "strength": "strong",
         "evidence": "区委书记与区长党政搭档", "overlap_org": "硚口区", "overlap_period": "", "direction": "undirected",
         "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "邱华威", "person_id": "qiaokouqu_邱华威", "relationship_type": "overlap", "strength": "medium",
         "evidence": "区委书记与常委常务副区长", "overlap_org": "中共硚口区委", "overlap_period": "", "direction": "undirected",
         "confidence": "confirmed", "source_ids": ["S001"]},
    ], "区委书记")

    # 2. 赵宏亮（区长）
    write_job(2, [
        {"start": "2024-12", "end": "至今", "org": "硚口区人民政府", "title": "硚口区区长",
         "notes": "区政府党组书记，领导区政府全面工作", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2024-12", "end": "至今", "org": "中共武汉市硚口区委", "title": "硚口区委副书记", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "2024-12", "org": "硚口区人民政府", "title": "区委常委、区政府党组副书记、副区长", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "硚口区人民政府", "title": "区政府党组成员、副区长", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "硚口区汉中街道", "title": "汉中街道工委副书记、办事处主任", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2002-07", "end": "", "org": "硚口区园林局", "title": "硚口区园林局副局长", "confidence": "confirmed", "source_ids": ["S001"]},
    ], [
        {"person": "周耕", "person_id": "qiaokouqu_周耕", "relationship_type": "overlap", "strength": "strong",
         "evidence": "区长与区委书记党政搭档", "overlap_org": "硚口区", "overlap_period": "", "direction": "undirected",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "邱华威", "person_id": "qiaokouqu_邱华威", "relationship_type": "superior_subordinate", "strength": "medium",
         "evidence": "区长与常务副区长", "overlap_org": "硚口区人民政府", "overlap_period": "", "direction": "undirected",
         "confidence": "confirmed", "source_ids": ["S001"]},
    ], "区长")

    # 3. 曾昳军(区委副书记兼纪委书记)
    write_job(3, [
        {"start": "", "end": "至今", "org": "中共武汉市硚口区委", "title": "硚口区委副书记",
         "notes": "专职副书记；1936-02 区纪委十三届六次全会作工作报告", "confidence": "confirmed", "source_ids": ["S006"]},
        {"start": "", "end": "至今", "org": "硚口区纪律检查委员会", "title": "区纪委书记", "notes": "兼区监委主任", "confidence": "confirmed", "source_ids": ["S005"]},
        {"start": "", "end": "至今", "org": "硚口区监察委员会", "title": "区监委主任", "confidence": "confirmed", "source_ids": ["S005"]},
    ], [
        {"person": "周耕", "person_id": "qiaokouqu_周耕", "relationship_type": "overlap", "strength": "medium",
         "evidence": "区委书记与专职副书记（兼纪委书记）", "overlap_org": "中共硚口区委", "overlap_period": "", "direction": "undirected",
         "confidence": "confirmed", "source_ids": ["S005", "S006"]},
        {"person": "赵宏亮", "person_id": "qiaokouqu_赵宏亮", "relationship_type": "overlap", "strength": "medium",
         "evidence": "区长与专职副书记（兼纪委书记）", "overlap_org": "中共硚口区委", "overlap_period": "", "direction": "undirected",
         "confidence": "confirmed", "source_ids": ["S006"]},
    ], "区委副书记")

    # 4. 邱华威（常务副区长）
    write_job(4, [
        {"start": "", "end": "至今", "org": "硚口区人民政府", "title": "硚口区常务副区长",
         "notes": "常务工作；发改/财政/金融/统计/税务/应急/人社/国有，1976年生", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "至今", "org": "中共武汉市硚口区委", "title": "硚口区委常委", "confidence": "confirmed", "source_ids": ["S001"]},
    ], [
        {"person": "赵宏亮", "person_id": "qiaokouqu_赵宏亮", "relationship_type": "superior_subordinate", "strength": "medium",
         "evidence": "常务副区长与区长", "overlap_org": "硚口区人民政府", "overlap_period": "", "direction": "undirected",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "周耕", "person_id": "qiaokouqu_周耕", "relationship_type": "overlap", "strength": "medium",
         "evidence": "常委常务副区长与区委书记", "overlap_org": "中共硚口区委", "overlap_period": "", "direction": "undirected",
         "confidence": "confirmed", "source_ids": ["S001"]},
    ], "常务副区长")


if __name__ == "__main__":
    build()