#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 湛河区 (Zhanhe District, Pingdingshan, Henan) leadership network.

湛河区 — 河南省平顶山市辖区, 平顶山市中心城区之一, 总面积约240平方公里,
辖1个乡、5个街道, 常住人口约29万.

Data sources:
- 湛河区人民政府门户网站 (www.zhq.gov.cn) — official news articles and leadership reports
- 第七次党代会报道 (2026-06-22/24) — new leadership election
- 区委六届十二次全会报道 (2026-06-17) — standing committee roster
- 区六届人大六次会议报道 (2026-02-26) — government and people's congress leadership
- 区政协六届五次会议报道 (2026-02-27) — political consultative conference leadership

Confidence notes:
- Current roles: confirmed (official source, as of 2026-07)
- Identity data (birth, birthplace, education) for most figures: partially known from news mentions
- Career timelines beyond current role: limited; gaps marked as unverified
- Baidu Baike (accessed via limited fetch) confirmed top 4 leaders but blocked for personal bio pages
"""

import sys
import os
from pathlib import Path

# Add project root to path
BASE = Path("/workspace/data/xieming/other-codes/gov-relation")
sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build

# ── Paths ────────────────────────────────────────────────────────────

STAGING = BASE / "data/tmp/henan_湛河区"
DB_PATH = STAGING / "湛河区_network.db"
GEXF_PATH = STAGING / "湛河区_network.gexf"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════
    # Core Leaders (Targets)
    # ══════════════════════════════════════════════════════════════════

    # 1. 区委书记 陈斌
    {"id": 1, "name": "陈斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区委书记", "current_org": "中共湛河区委",
     "source": "zhq.gov.cn — 七次党代会开幕报道 (2026-06-23); 两优一先表彰大会报道 (2026-06-30)"},

    # 2. 区委副书记、区长 马培翼
    {"id": 2, "name": "马培翼", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区委副书记、区长", "current_org": "湛河区人民政府",
     "source": "zhq.gov.cn — 六届人大六次会议 (2026-02-26); 两优一先表彰大会报道 (2026-06-30); Baidu Baike (2025-07)"},

    # ══════════════════════════════════════════════════════════════════
    # Party Committee Leaders
    # ══════════════════════════════════════════════════════════════════

    # 3. 区委副书记 王伟
    {"id": 3, "name": "王伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区委副书记", "current_org": "中共湛河区委",
     "source": "zhq.gov.cn — 两优一先表彰大会 (2026-06-30); 区委六届十二次全会 (2026-06-17)"},

    # 4. 区委常委、常务副区长(推测) 马小帅
    {"id": 4, "name": "马小帅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区委常委、常务副区长（推测）", "current_org": "中共湛河区委",
     "source": "zhq.gov.cn — 区委六届十二次全会主席台名单; 安全生产暨社会稳定工作会议 (2026-04-08); 防汛备汛工作会议 (2026-04-08)"},

    # 5. 区委常委、区委办公室主任 袁景涛
    {"id": 5, "name": "袁景涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区委常委、区委办公室主任", "current_org": "中共湛河区委办公室",
     "source": "zhq.gov.cn — 区委六届十二次全会主席台名单; 春季学期主体班报道 (2026-03)"},

    # 6. 区委常委 马斌
    {"id": 6, "name": "马斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区委常委", "current_org": "中共湛河区委",
     "source": "zhq.gov.cn — 区委六届十二次全会主席台名单; 看望党代会代表 (2026-06-22)"},

    # 7. 区委常委、区纪委书记 蔺泓光
    {"id": 7, "name": "蔺泓光", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区委常委、区纪委书记", "current_org": "中共湛河区纪委",
     "source": "zhq.gov.cn — 七次党代会开幕 (2026-06-23, 代表六届纪委作报告); 看望党代会代表 (2026-06-22)"},

    # 8. 区委常委、组织部部长 郭志钢
    {"id": 8, "name": "郭志钢", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区委常委、组织部部长", "current_org": "中共湛河区委组织部",
     "source": "zhq.gov.cn — 正确政绩观学习教育座谈会 (2026-06-09, 组织部长身份); 区委六届十二次全会主席台名单"},

    # 9. 区委常委 李永浩
    {"id": 9, "name": "李永浩", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区委常委", "current_org": "中共湛河区委",
     "source": "zhq.gov.cn — 区委六届十二次全会主席台名单; 安全生产会议; 看望代表名单"},

    # 10. 区委常委 付亚鹏
    {"id": 10, "name": "付亚鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区委常委", "current_org": "中共湛河区委",
     "source": "zhq.gov.cn — 区委六届十二次全会主席台名单; 看望代表名单"},

    # 11. 区委常委 王佳涵
    {"id": 11, "name": "王佳涵", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区委常委", "current_org": "中共湛河区委",
     "source": "zhq.gov.cn — 区委六届十二次全会主席台名单; 看望代表名单"},

    # 12. 区委常委、统战部部长 李烨鸿
    {"id": 12, "name": "李烨鸿", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区委常委、统战部部长", "current_org": "中共湛河区委统战部",
     "source": "zhq.gov.cn — 政协六届五次会议开幕报道 (2026-02-27, 统战部长列名); 政协闭幕报道"},

    # ══════════════════════════════════════════════════════════════════
    # Government Leaders (from official news)
    # ══════════════════════════════════════════════════════════════════

    # 13. 副区长(推测排列第一) 赵亚锋
    {"id": 13, "name": "赵亚锋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区副区长", "current_org": "湛河区人民政府",
     "source": "zhq.gov.cn — 安全生产会议名单; 六届人大六次会议报道"},

    # 14. 副区长级领导 于红可
    {"id": 14, "name": "于红可", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区区领导（副区长级）", "current_org": "湛河区人民政府",
     "source": "zhq.gov.cn — 安全生产会议名单; 防汛备汛会议名单"},

    # 15. 副区长级领导 张晓春
    {"id": 15, "name": "张晓春", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区区领导（副区长级）", "current_org": "湛河区人民政府",
     "source": "zhq.gov.cn — 安全生产会议名单; 防汛备汛会议名单"},

    # ══════════════════════════════════════════════════════════════════
    # People's Congress (from 六届人大六次会议)
    # ══════════════════════════════════════════════════════════════════

    # 16. 区人大常委会主任 褚正宾
    {"id": 16, "name": "褚正宾", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区人大常委会主任", "current_org": "湛河区人大常委会",
     "source": "zhq.gov.cn — 区六届人大六次会议 (2026-02-26, 主席台前排就座并主持); Baidu Baike (2025-07)"},

    # 17. 区人大常委会副主任 王要红
    {"id": 17, "name": "王要红", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区人大常委会副主任", "current_org": "湛河区人大常委会",
     "source": "zhq.gov.cn — 六届人大六次会议主席台前排名单"},

    # 18. 区人大常委会副主任 龚永强
    {"id": 18, "name": "龚永强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区人大常委会副主任", "current_org": "湛河区人大常委会",
     "source": "zhq.gov.cn — 六届人大六次会议主席台前排名单"},

    # 19. 区人大常委会副主任 周学军
    {"id": 19, "name": "周学军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区人大常委会副主任", "current_org": "湛河区人大常委会",
     "source": "zhq.gov.cn — 六届人大六次会议主席台前排名单"},

    # 20. 区人大常委会副主任 王韦弦
    {"id": 20, "name": "王韦弦", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区人大常委会副主任", "current_org": "湛河区人大常委会",
     "source": "zhq.gov.cn — 六届人大六次会议主席台前排名单"},

    # ══════════════════════════════════════════════════════════════════
    # Political Consultative Conference (from 政协六届五次会议)
    # ══════════════════════════════════════════════════════════════════

    # 21. 区政协主席 宋本旺
    {"id": 21, "name": "宋本旺", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "湛河区政协主席", "current_org": "政协湛河区委员会",
     "source": "zhq.gov.cn — 政协六届五次会议 (2026-02-27); Baidu Baike (2025-07)"},

    # 22. 区政协副主席 马喜彬
    {"id": 22, "name": "马喜彬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "湛河区政协副主席", "current_org": "政协湛河区委员会",
     "source": "zhq.gov.cn — 政协六届五次会议报道"},

    # 23. 区政协副主席 吕晓丽
    {"id": 23, "name": "吕晓丽", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "湛河区政协副主席", "current_org": "政协湛河区委员会",
     "source": "zhq.gov.cn — 政协六届五次会议报道"},

    # 24. 区政协副主席 楚辉锋
    {"id": 24, "name": "楚辉锋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "湛河区政协副主席", "current_org": "政协湛河区委员会",
     "source": "zhq.gov.cn — 政协六届五次会议报道"},

    # 25. 区政协副主席 孟丽
    {"id": 25, "name": "孟丽", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "湛河区政协副主席", "current_org": "政协湛河区委员会",
     "source": "zhq.gov.cn — 政协六届五次会议报道"},
]

organizations = [
    {"id": 1, "name": "中共湛河区委", "type": "党委", "level": "县处级",
     "parent": "中共平顶山市委", "location": "河南省平顶山市湛河区"},
    {"id": 2, "name": "湛河区人民政府", "type": "政府", "level": "县处级",
     "parent": "平顶山市人民政府", "location": "河南省平顶山市湛河区"},
    {"id": 3, "name": "中共湛河区纪委", "type": "党委", "level": "县处级",
     "parent": "中共湛河区委", "location": "河南省平顶山市湛河区"},
    {"id": 4, "name": "中共湛河区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共湛河区委", "location": "河南省平顶山市湛河区"},
    {"id": 5, "name": "中共湛河区委办公室", "type": "党委", "level": "乡科级",
     "parent": "中共湛河区委", "location": "河南省平顶山市湛河区"},
    {"id": 6, "name": "中共湛河区委统战部", "type": "党委", "level": "乡科级",
     "parent": "中共湛河区委", "location": "河南省平顶山市湛河区"},
    {"id": 7, "name": "湛河区人大常委会", "type": "人大", "level": "县处级",
     "parent": "平顶山市人大常委会", "location": "河南省平顶山市湛河区"},
    {"id": 8, "name": "政协湛河区委员会", "type": "政协", "level": "县处级",
     "parent": "政协平顶山市委员会", "location": "河南省平顶山市湛河区"},
]

positions = [
    # ── 陈斌 (区委书记) ──
    {"person_id": 1, "org_id": 1, "title": "湛河区委书记", "start": "",
     "end": "present", "rank": "县处级正职", "note": "从区长升任书记；2026年主持区委六届十二次全会、七次党代会、两优一先表彰大会"},

    # ── 马培翼 (区长) ──
    {"person_id": 2, "org_id": 2, "title": "湛河区区长", "start": "",
     "end": "present", "rank": "县处级正职", "note": "2026年2月人大会议上作政府工作报告；兼任区委副书记；Baidu Baike 标为'代理区长'"},
    {"person_id": 2, "org_id": 1, "title": "湛河区委副书记", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 王伟 (区委副书记) ──
    {"person_id": 3, "org_id": 1, "title": "湛河区委副书记", "start": "",
     "end": "present", "rank": "县处级副职", "note": "两优一先大会宣读表彰决定"},

    # ── 马小帅 (区委常委、推测常务副区长) ──
    {"person_id": 4, "org_id": 1, "title": "湛河区委常委", "start": "",
     "end": "present", "rank": "县处级副职", "note": "经常出席政府工作会议"},
    {"person_id": 4, "org_id": 2, "title": "常务副区长（推测）", "start": "",
     "end": "present", "rank": "县处级副职", "note": "在政府领导中排列第一，推测为常务副区长"},

    # ── 袁景涛 (区委办主任) ──
    {"person_id": 5, "org_id": 1, "title": "湛河区委常委", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "区委办公室主任", "start": "",
     "end": "present", "rank": "乡科级正职", "note": ""},

    # ── 马斌 (区委常委) ──
    {"person_id": 6, "org_id": 1, "title": "湛河区委常委", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 蔺泓光 (纪委书记) ──
    {"person_id": 7, "org_id": 3, "title": "湛河区纪委书记", "start": "",
     "end": "present", "rank": "县处级副职", "note": "代表六届纪委在七次党代会作报告"},
    {"person_id": 7, "org_id": 1, "title": "湛河区委常委", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 郭志钢 (组织部长) ──
    {"person_id": 8, "org_id": 1, "title": "湛河区委常委", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 4, "title": "区委组织部部长", "start": "",
     "end": "present", "rank": "乡科级正职", "note": "正确政绩观学习教育座谈会以组织部长身份讲话"},

    # ── 李永浩 (区委常委) ──
    {"person_id": 9, "org_id": 1, "title": "湛河区委常委", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 付亚鹏 (区委常委) ──
    {"person_id": 10, "org_id": 1, "title": "湛河区委常委", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 王佳涵 (区委常委) ──
    {"person_id": 11, "org_id": 1, "title": "湛河区委常委", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 李烨鸿 (统战部长) ──
    {"person_id": 12, "org_id": 1, "title": "湛河区委常委", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 6, "title": "区委统战部部长", "start": "",
     "end": "present", "rank": "乡科级正职", "note": "区政协党组副书记"},

    # ── 赵亚锋 (副区长) ──
    {"person_id": 13, "org_id": 2, "title": "湛河区副区长", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 于红可 (区领导) ──
    {"person_id": 14, "org_id": 2, "title": "湛河区副区长级领导", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 张晓春 (区领导) ──
    {"person_id": 15, "org_id": 2, "title": "湛河区副区长级领导", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 褚正宾 (人大主任) ──
    {"person_id": 16, "org_id": 7, "title": "区人大常委会主任", "start": "",
     "end": "present", "rank": "县处级正职", "note": "主持六届人大六次会议"},

    # ── 王要红 (人大副主任) ──
    {"person_id": 17, "org_id": 7, "title": "区人大常委会副主任", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 龚永强 (人大副主任) ──
    {"person_id": 18, "org_id": 7, "title": "区人大常委会副主任", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 周学军 (人大副主任) ──
    {"person_id": 19, "org_id": 7, "title": "区人大常委会副主任", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 王韦弦 (人大副主任) ──
    {"person_id": 20, "org_id": 7, "title": "区人大常委会副主任", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 宋本旺 (政协主席) ──
    {"person_id": 21, "org_id": 8, "title": "区政协主席", "start": "",
     "end": "present", "rank": "县处级正职", "note": ""},

    # ── 马喜彬 (政协副主席) ──
    {"person_id": 22, "org_id": 8, "title": "区政协副主席", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 吕晓丽 (政协副主席) ──
    {"person_id": 23, "org_id": 8, "title": "区政协副主席", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 楚辉锋 (政协副主席) ──
    {"person_id": 24, "org_id": 8, "title": "区政协副主席", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},

    # ── 孟丽 (政协副主席) ──
    {"person_id": 25, "org_id": 8, "title": "区政协副主席", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},
]

relationships = [
    # ── 区委班子核心 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政搭档", "overlap_org": "中共湛河区委",
     "overlap_period": "", "strength": "strong",
     "source": "zhq.gov.cn — 区委六届十二次全会; 两优一先; 人大会议"},
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委书记与专职副书记", "overlap_org": "中共湛河区委",
     "overlap_period": "", "strength": "strong",
     "source": "zhq.gov.cn — 两优一先; 区委全会"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "区长与区委副书记（均为副书记）", "overlap_org": "中共湛河区委常委会",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 区委全会; 两优一先"},

    # ── 区委常委之间的工作关系 ──
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "区委书记与纪委书记", "overlap_org": "中共湛河区委常委会",
     "overlap_period": "", "strength": "strong",
     "source": "zhq.gov.cn — 七次党代会; 看望代表名单"},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "区委书记与组织部部长", "overlap_org": "中共湛河区委常委会",
     "overlap_period": "", "strength": "strong",
     "source": "zhq.gov.cn — 区委全会; 政绩观座谈会"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与常务副区长（推测）", "overlap_org": "中共湛河区委常委会",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 区委全会主席台名单"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与区委办主任", "overlap_org": "中共湛河区委/区委办",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 区委全会主席台名单; 主体班报道"},
    {"person_a": 1, "person_b": 12, "type": "overlap",
     "context": "区委书记与统战部长", "overlap_org": "中共湛河区委常委会",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 政协会议报道"},

    # ── 区委常委之间的同事关系 ──
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "区委常委同事", "overlap_org": "中共湛河区委常委会",
     "overlap_period": "", "strength": "weak",
     "source": "zhq.gov.cn — 区委全会主席台名单"},
    {"person_a": 4, "person_b": 6, "type": "overlap",
     "context": "区委常委同事", "overlap_org": "中共湛河区委常委会",
     "overlap_period": "", "strength": "weak",
     "source": "zhq.gov.cn — 区委全会主席台名单"},
    {"person_a": 4, "person_b": 9, "type": "overlap",
     "context": "区委常委同事", "overlap_org": "中共湛河区委常委会",
     "overlap_period": "", "strength": "weak",
     "source": "zhq.gov.cn — 区委全会主席台名单"},

    # ── 政府班子关系 ──
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与常务副区长（推测）", "overlap_org": "湛河区人民政府",
     "overlap_period": "", "strength": "strong",
     "source": "zhq.gov.cn — 安全生产会议; 区政府工作会议"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "湛河区人民政府",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 安全生产会议"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "区长与区政府领导", "overlap_org": "湛河区人民政府",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 安全生产会议; 防汛会议"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "区长与区政府领导", "overlap_org": "湛河区人民政府",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 安全生产会议; 防汛会议"},
    {"person_a": 4, "person_b": 13, "type": "overlap",
     "context": "常务副区长与副区长（政府班子成员）", "overlap_org": "湛河区人民政府",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 各类政府工作会议"},

    # ── 人大关系 ──
    {"person_a": 16, "person_b": 17, "type": "overlap",
     "context": "人大主任与副主任", "overlap_org": "湛河区人大常委会",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 六届人大六次会议"},
    {"person_a": 16, "person_b": 18, "type": "overlap",
     "context": "人大主任与副主任", "overlap_org": "湛河区人大常委会",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 六届人大六次会议"},
    {"person_a": 16, "person_b": 19, "type": "overlap",
     "context": "人大主任与副主任", "overlap_org": "湛河区人大常委会",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 六届人大六次会议"},
    {"person_a": 16, "person_b": 20, "type": "overlap",
     "context": "人大主任与副主任", "overlap_org": "湛河区人大常委会",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 六届人大六次会议"},

    # ── 政协关系 ──
    {"person_a": 21, "person_b": 22, "type": "overlap",
     "context": "政协主席与副主席", "overlap_org": "政协湛河区委员会",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 政协六届五次会议"},
    {"person_a": 21, "person_b": 23, "type": "overlap",
     "context": "政协主席与副主席", "overlap_org": "政协湛河区委员会",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 政协六届五次会议"},
    {"person_a": 21, "person_b": 24, "type": "overlap",
     "context": "政协主席与副主席", "overlap_org": "政协湛河区委员会",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 政协六届五次会议"},
    {"person_a": 21, "person_b": 25, "type": "overlap",
     "context": "政协主席与副主席", "overlap_org": "政协湛河区委员会",
     "overlap_period": "", "strength": "medium",
     "source": "zhq.gov.cn — 政协六届五次会议"},
]


def main():
    print(f"=== Building 湛河区 network data ===")
    print(f"Target: 区委书记 & 区长")
    print(f"Date: 2026-07-24")

    run_build(
        slug="湛河区",
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
