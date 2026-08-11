#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 殷都区 (Yindu District, Anyang, Henan) leadership network.

殷都区 — 河南省安阳市辖区, 安阳市中心城区之一, 总面积约687平方公里,
辖8个镇、5个乡、7个街道, 常住人口约70万.
殷都区以殷墟闻名, 辖区内拥有世界文化遗产殷墟.

Data sources:
- 殷都区人民政府门户网站 (www.yindu.gov.cn):
  - 区政府领导页 (2025-10-16): 确认区长郭向工及5位副区长
  - 区政府领导分工通知 (2025-12-22): 确认常务副区长臧华伟
  - 郭向工简历页: 男, 汉族, 1973年1月出生, 研究生学历, 中共党员
  - 各副区长简历页
- 区政府会议新闻 (2026-07-08): 郭向工以区委副书记、区长身份主持会议

Confidence notes:
- 区长郭向工: confirmed (official profile page, multiple news articles 2024-2026)
- 常务副区长臧华伟: confirmed (official leadership分工通知)
- 副区长列表: confirmed (official leadership page)
- 区委书记姓名: unverified (government website only lists government leaders, not party leaders;
  区委书记领导信息不在殷都区人民政府网站"政府领导"栏目)
- 区委常委会其他成员: unknown (no accessible source)
- Career timelines for most leaders: partial (only basic identity info available)
- ALL claims not marked "confirmed" should be treated as unverified
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

BASE = Path("/workspace/data/xieming/other-codes/gov-relation")
sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build

# ── Paths ────────────────────────────────────────────────────────────

STAGING = BASE / "data/tmp/henan_殷都区"
DB_PATH = STAGING / "殷都区_network.db"
GEXF_PATH = STAGING / "殷都区_network.gexf"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════
    # Core Leaders (Targets)
    # ══════════════════════════════════════════════════════════════════

    # 区委书记 — 姓名未确认
    # note: 殷都区人民政府网站"政府领导"栏目仅公示区政府领导(区长、副区长),
    # 区委书记信息不在该栏目公示. 需通过安阳市委组织部任前公示或殷都区委网站获取.
    {"id": 1, "name": "待确认-殷都区委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区委书记（待确认）", "current_org": "中共殷都区委",
     "source": "殷都区人民政府网站未列出区委书记信息; 公开检索受限"},

    # 区长 郭向工
    # Source: 殷都区人民政府网站区长简历页 (2025-10-16)
    #         殷都区政府第108次党组（扩大）会议 (2026-07-08)
    {"id": 2, "name": "郭向工", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-01", "birthplace": "",
     "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区委副书记、区长", "current_org": "殷都区人民政府",
     "source": "https://www.yindu.gov.cn/zfxxgk/qzfld/ — 区长页; https://www.yindu.gov.cn/2022/07-19/2461517.html — 简历"},

    # ══════════════════════════════════════════════════════════════════
    # Deputy Leaders (Confirmed from official site)
    # ══════════════════════════════════════════════════════════════════

    # 常务副区长 臧华伟
    # Source: 区政府领导分工调整通知 (2025-12-22发布, 2024-11-21印发)
    {"id": 3, "name": "臧华伟", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区委常委、常务副区长", "current_org": "殷都区人民政府",
     "source": "殷都区人民政府办公室关于调整区政府领导分工的通知 (2025-12-22)"},

    # 副区长 刘艳菊 (区委常委、宣传部长)
    # Source: 简历页 https://www.yindu.gov.cn/2022/05-27/2387996.html
    {"id": 4, "name": "刘艳菊", "gender": "女", "ethnicity": "汉族",
     "birth": "1973-07", "birthplace": "",
     "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区委常委、宣传部长、副区长", "current_org": "殷都区人民政府",
     "source": "https://www.yindu.gov.cn/2022/05-27/2387996.html — 简历"},

    # 副区长 何静峰
    # Source: 区政府领导分工通知
    {"id": 5, "name": "何静峰", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "殷都区副区长", "current_org": "殷都区人民政府",
     "source": "殷都区人民政府办公室关于调整区政府领导分工的通知 (2025-12-22)"},

    # 副区长 徐海峰 (殷都公安分局局长)
    # Source: 简历页 https://www.yindu.gov.cn/2022/07-19/2461520.html
    {"id": 6, "name": "徐海峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-04", "birthplace": "",
     "education": "大学本科", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区副区长、殷都公安分局局长", "current_org": "殷都区人民政府",
     "source": "https://www.yindu.gov.cn/2022/07-19/2461520.html — 简历"},

    # 副区长 陈科
    # Source: 简历页 https://www.yindu.gov.cn/2022/07-19/2461519.html
    {"id": 7, "name": "陈科", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-07", "birthplace": "",
     "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区副区长", "current_org": "殷都区人民政府",
     "source": "https://www.yindu.gov.cn/2022/07-19/2461519.html — 简历"},

    # 副区长 张新峰
    # Source: 简历页 https://www.yindu.gov.cn/2025/03-26/3486987.html
    {"id": 8, "name": "张新峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-11", "birthplace": "",
     "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区副区长", "current_org": "殷都区人民政府",
     "source": "https://www.yindu.gov.cn/2025/03-26/3486987.html — 简历"},

    # 副区长 陈瑾 (农工党员, 非中共党员)
    # Source: 简历页 https://www.yindu.gov.cn/2025/04-17/3491671.html
    {"id": 9, "name": "陈瑾", "gender": "女", "ethnicity": "汉族",
     "birth": "1979-01", "birthplace": "",
     "education": "研究生", "party_join": "", "work_start": "",
     "current_post": "殷都区副区长", "current_org": "殷都区人民政府",
     "source": "https://www.yindu.gov.cn/2025/04-17/3491671.html — 简历"},

    # 副区长 路炎
    # Source: 简历页 https://www.yindu.gov.cn/2026/03-16/3635592.html
    {"id": 10, "name": "路炎", "gender": "男", "ethnicity": "汉族",
     "birth": "1988-04", "birthplace": "",
     "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区副区长", "current_org": "殷都区人民政府",
     "source": "https://www.yindu.gov.cn/2026/03-16/3635592.html — 简历"},

    # 区政府党组成员、办公室主任 毛学文
    # Source: 区政府领导分工通知
    {"id": 11, "name": "毛学文", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区政府党组成员、办公室主任", "current_org": "殷都区人民政府办公室",
     "source": "殷都区人民政府办公室关于调整区政府领导分工的通知 (2025-12-22)"},

    # ══════════════════════════════════════════════════════════════════
    # Key Standing Committee Members (推测 - Party leadership structure)
    # ══════════════════════════════════════════════════════════════════

    # 区委专职副书记 — 待确认 (possibly not 郭向工, as he is the government head)
    {"id": 12, "name": "待确认-殷都区委专职副书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区委副书记（推测）", "current_org": "中共殷都区委",
     "source": "区委常规设有专职副书记; 姓名未公开"},

    # 区纪委书记 — 待确认
    {"id": 13, "name": "待确认-区纪委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区委常委、区纪委书记（推测）", "current_org": "中共殷都区纪委",
     "source": "区委常规设有纪委书记; 姓名未公开"},

    # 区委组织部部长 — 待确认
    {"id": 14, "name": "待确认-区委组织部部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区委常委、组织部部长（推测）", "current_org": "中共殷都区委组织部",
     "source": "区委常规设有组织部长; 姓名未公开"},

    # 区委政法委书记 — 待确认
    {"id": 15, "name": "待确认-区委政法委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区委常委、政法委书记（推测）", "current_org": "中共殷都区委政法委",
     "source": "区委常规设有政法委书记; 姓名未公开"},

    # 人武部主官 — 待确认
    {"id": 16, "name": "待确认-人武部主官", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区委常委、人武部主官（推测）", "current_org": "殷都区人民武装部",
     "source": "区委常规设有人武部主官兼任常委; 姓名未公开"},

    # 区委统战部部长 — 待确认
    {"id": 17, "name": "待确认-区委统战部部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "殷都区委常委、统战部部长（推测）", "current_org": "中共殷都区委统战部",
     "source": "区委常规设有统战部长; 姓名未公开"},
]

organizations = [
    {"id": 1, "name": "中共殷都区委", "type": "党委", "level": "县处级",
     "parent": "中共安阳市委", "location": "河南省安阳市殷都区"},
    {"id": 2, "name": "殷都区人民政府", "type": "政府", "level": "县处级",
     "parent": "安阳市人民政府", "location": "河南省安阳市殷都区"},
    {"id": 3, "name": "中共殷都区纪委", "type": "党委", "level": "县处级",
     "parent": "中共殷都区委", "location": "河南省安阳市殷都区"},
    {"id": 4, "name": "中共殷都区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共殷都区委", "location": "河南省安阳市殷都区"},
    {"id": 5, "name": "中共殷都区委宣传部", "type": "党委", "level": "乡科级",
     "parent": "中共殷都区委", "location": "河南省安阳市殷都区"},
    {"id": 6, "name": "中共殷都区委政法委", "type": "党委", "level": "乡科级",
     "parent": "中共殷都区委", "location": "河南省安阳市殷都区"},
    {"id": 7, "name": "中共殷都区委统战部", "type": "党委", "level": "乡科级",
     "parent": "中共殷都区委", "location": "河南省安阳市殷都区"},
    {"id": 8, "name": "殷都区人民武装部", "type": "党委", "level": "县处级",
     "parent": "安阳军分区", "location": "河南省安阳市殷都区"},
    {"id": 9, "name": "殷都区人大常委会", "type": "人大", "level": "县处级",
     "parent": "安阳市人大常委会", "location": "河南省安阳市殷都区"},
    {"id": 10, "name": "殷都区政协", "type": "政协", "level": "县处级",
     "parent": "政协安阳市委员会", "location": "河南省安阳市殷都区"},
    {"id": 11, "name": "殷都区人民政府办公室", "type": "政府", "level": "乡科级",
     "parent": "殷都区人民政府", "location": "河南省安阳市殷都区"},
    {"id": 12, "name": "安阳市公安局殷都分局", "type": "政府", "level": "乡科级",
     "parent": "安阳市公安局", "location": "河南省安阳市殷都区"},
]

positions = [
    # ── 区委书记 (待确认) ──
    {"person_id": 1, "org_id": 1, "title": "殷都区委书记", "start_date": "",
     "end_date": "present", "rank": "县处级正职", "note": "姓名待确认; 区委书记领导信息不在区政府网站公示"},

    # ── 郭向工 — 区长兼区委副书记 ──
    {"person_id": 2, "org_id": 2, "title": "殷都区区长", "start_date": "",
     "end_date": "present", "rank": "县处级正职", "note": "主持区政府全面工作; 最新确认: 2026年7月"},
    {"person_id": 2, "org_id": 1, "title": "殷都区委副书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "兼任区委副书记"},

    # ── 臧华伟 — 常务副区长 ──
    {"person_id": 3, "org_id": 1, "title": "殷都区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "殷都区常务副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "负责区政府日常事务、发改、财政等工作"},

    # ── 刘艳菊 — 宣传部长、副区长 ──
    {"person_id": 4, "org_id": 1, "title": "殷都区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 5, "title": "殷都区委宣传部部长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "殷都区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "分管水利、农业、乡村振兴等工作"},

    # ── 何静峰 — 副区长 ──
    {"person_id": 5, "org_id": 2, "title": "殷都区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "分管文化、旅游、教育、民政、卫健等工作"},

    # ── 徐海峰 — 副区长、公安分局局长 ──
    {"person_id": 6, "org_id": 2, "title": "殷都区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 12, "title": "殷都公安分局局长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "主持殷都公安分局全面工作"},

    # ── 陈科 — 副区长 ──
    {"person_id": 7, "org_id": 2, "title": "殷都区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "分管工业、城建、交通、招商等工作"},

    # ── 张新峰 — 副区长 ──
    {"person_id": 8, "org_id": 2, "title": "殷都区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "分管领域待进一步确认"},

    # ── 陈瑾 — 副区长 ──
    {"person_id": 9, "org_id": 2, "title": "殷都区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "农工党员; 分管领域待进一步确认"},

    # ── 路炎 — 副区长 ──
    {"person_id": 10, "org_id": 2, "title": "殷都区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "1988年出生; 年轻副区长; 分管领域待进一步确认"},

    # ── 毛学文 — 政府党组成员、办公室主任 ──
    {"person_id": 11, "org_id": 11, "title": "殷都区政府办公室主任", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "殷都区政府党组成员", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},

    # ── 专职副书记 (待确认) ──
    {"person_id": 12, "org_id": 1, "title": "殷都区委副书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # ── 纪委书记 (待确认) ──
    {"person_id": 13, "org_id": 1, "title": "殷都区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "殷都区纪委书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # ── 组织部长 (待确认) ──
    {"person_id": 14, "org_id": 1, "title": "殷都区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 4, "title": "殷都区委组织部部长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "姓名待确认"},

    # ── 政法委书记 (待确认) ──
    {"person_id": 15, "org_id": 1, "title": "殷都区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 6, "title": "殷都区委政法委书记", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "姓名待确认"},

    # ── 人武部主官 (待确认) ──
    {"person_id": 16, "org_id": 1, "title": "殷都区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 8, "title": "殷都区人武部主官", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # ── 统战部长 (待确认) ──
    {"person_id": 17, "org_id": 1, "title": "殷都区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 7, "title": "殷都区委统战部部长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "姓名待确认"},
]

relationships = [
    # ── 区委书记与区长 — 党政一把手 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长搭档", "overlap_org": "中共殷都区委",
     "overlap_period": "当前", "strength": "strong",
     "source": "推测: 区级领导班子常规分工"},

    # ── 区长与常务副区长 ──
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "区长与常务副区长", "overlap_org": "殷都区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "source": "区政府领导分工通知 (2025-12-22)"},

    # ── 区长与副区长 ──
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与分管副区长", "overlap_org": "殷都区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "source": "区政府领导分工通知"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与分管副区长", "overlap_org": "殷都区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "source": "区政府领导分工通知"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与分管副区长", "overlap_org": "殷都区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "source": "区政府领导分工通知"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与分管副区长", "overlap_org": "殷都区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "source": "区政府领导分工通知"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与分管副区长", "overlap_org": "殷都区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "source": "区政府领导分工通知"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "区长与分管副区长", "overlap_org": "殷都区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "source": "区政府领导分工通知"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "区长与分管副区长", "overlap_org": "殷都区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "source": "区政府领导分工通知"},

    # ── 区委书记与区委常委 ──
    {"person_a": 1, "person_b": 12, "type": "overlap",
     "context": "区委书记与专职副书记", "overlap_org": "中共殷都区委常委会",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 区委常规设置"},
    {"person_a": 1, "person_b": 13, "type": "overlap",
     "context": "区委书记与纪委书记", "overlap_org": "中共殷都区委常委会",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 区委常规设置"},
    {"person_a": 1, "person_b": 14, "type": "overlap",
     "context": "区委书记与组织部长", "overlap_org": "中共殷都区委常委会",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 区委常规设置"},
    {"person_a": 1, "person_b": 15, "type": "overlap",
     "context": "区委书记与政法委书记", "overlap_org": "中共殷都区委常委会",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 区委常规设置"},

    # ── 刘艳菊兼任区委常委、宣传部长 ──
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与宣传部部长", "overlap_org": "中共殷都区委常委会",
     "overlap_period": "当前", "strength": "medium",
     "source": "刘艳菊简历证实为区委常委、宣传部长"},
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "常务副区长与宣传部部长同为区委常委", "overlap_org": "中共殷都区委常委会",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 区委常委会同僚"},

    # ── 臧华伟与刘艳菊同为区委常委 ──
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "同届区委常委会成员", "overlap_org": "中共殷都区委常委会",
     "overlap_period": "当前", "strength": "medium",
     "source": "两人均被确认为殷都区委常委"},

    # ── 徐海峰与陈科、张新峰 ──
    {"person_a": 6, "person_b": 7, "type": "overlap",
     "context": "同为副区长", "overlap_org": "殷都区人民政府",
     "overlap_period": "当前", "strength": "medium",
     "source": "区政府领导班子"},
    {"person_a": 6, "person_b": 8, "type": "overlap",
     "context": "同为副区长", "overlap_org": "殷都区人民政府",
     "overlap_period": "当前", "strength": "medium",
     "source": "区政府领导班子"},
    {"person_a": 7, "person_b": 8, "type": "overlap",
     "context": "同为副区长", "overlap_org": "殷都区人民政府",
     "overlap_period": "当前", "strength": "medium",
     "source": "区政府领导班子"},
]


def main():
    print("=== Building 殷都区 network data ===")
    print(f"Target: 区委书记 & 区长")
    print(f"区长郭向工: confirmed")
    print(f"区委书记姓名: unverified (殷都区政府网站未公示区委书记信息)")
    print(f"副区长名单: confirmed (7位副区长/党组成员来自官网)")

    run_build(
        slug="殷都区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Summary
    print(f"\n=== Summary ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"\nDB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("=== Done ===")


if __name__ == "__main__":
    main()
