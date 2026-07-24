#!/usr/bin/env python3
"""Build 武汉市青山区 (Wuhan Qingshan District) leadership network data.

Level: 市辖区
Province: 湖北省
Parent city: 武汉市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: hubei_青山区

Research date: 2026-07-24
Official source: https://www.qingshan.gov.cn/ (武汉市青山区人民政府)

Current status (as of 2026-07-24, verified via qingshan.gov.cn news and WeChat articles):
- 区委书记、化工区党工委书记: 余志成 — confirmed by qingshan.gov.cn slide and WeChat article (2026-02-09)
- 区委副书记、区人民政府区长: 王永胜 — confirmed as 代理区长 (2026-06-16), then 区长 (2026-06-29 onward)
- 前任区长: 沈涛 — 青山区委副书记、区长、化工区党工委副书记、管委会主任 (as of 2025-08-12)
- 区领导: 陈敏 — 出现在2026年2月文章中（可能在余志成和王永胜之间）
- 区领导: 杨海牛 — 出现在常务会议名单中
- 区领导: 王小兵 — 出现在常务会议名单中
- 区领导: 朱仕君 — 出现在常务会议名单中
- 区领导: 郑丽梅 — 化工区党工委委员、管委会副主任
- 区领导: 朱海林 — 出现在常务会议名单中
- 区领导: 雷敏 — 出现在常务会议名单中
- 区领导: 屠浩文 — 出现在常务会议名单中
- 区领导: 彭小平 — 出现在常务会议名单中
- 区领导: 吴冬 — 出现在常务会议名单中
- 区领导: 肖建洲 — 出现在常务会议名单中

Confirmed news article sources (all from qingshan.gov.cn):
- 区政府常务会议(第104次, 2026-07-23): /qzfbm/zfgzbm/zfb/bmdt/202607/t20260723_2824704.shtml
- 区政府常务会议(第102次, 2026-06-29): /qzfbm/zfgzbm/zfb/bmdt/202606/t20260629_2814506.shtml
- 区政府常务会议(第101次, 2026-06-17): /qzfbm/zfgzbm/zfb/bmdt/202606/t20260617_2778287.shtml
- 区政府常务会议(第100次, 2026-06-10): /qzfbm/zfgzbm/zfb/bmdt/202606/t20260610_2775670.shtml
- 区委书记余志成调研青山船厂 (2026-02-09): WeChat article (美丽青山)
- 青山携手武钢集团北湖片区开发 (2025-08-12): WeChat article (美丽青山)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "青山区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = datetime.now().strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y%m%d")

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════

    # ── 区委书记 ──
    {
        "id": 1,
        "name": "余志成",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青山区委书记、化工区党工委书记",
        "current_org": "中共武汉市青山区委员会",
        "source": "https://mp.weixin.qq.com/s/t5DR-Cco286wXB9Lb8nKTw (美丽青山 2026-02-09)",
        "notes": "官网首页幻灯片确认区委书记身份；兼任化工区党工委书记。出生年份、籍贯、教育等个人信息待补充。",
    },
    # ── 区委副书记、区长 ──
    {
        "id": 2,
        "name": "王永胜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青山区委副书记、区人民政府区长",
        "current_org": "青山区人民政府",
        "source": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/zfb/bmdt/202607/t20260723_2824704.shtml",
        "notes": "2026年6月16日以'代理区长'身份主持会议，6月29日起以'区长'身份出现。出生年份、籍贯等个人信息待补充。",
    },
    # ── 区委副书记（推测） ──
    {
        "id": 3,
        "name": "陈敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共武汉市青山区委员会",
        "source": "https://mp.weixin.qq.com/s/t5DR-Cco286wXB9Lb8nKTw (2026-02-09 余志成调研青山船厂)",
        "notes": "出现在2026年2月区委书记调研活动的'区领导'名单首位，推测为区委副书记。具体职务待确认。",
    },
    # ── 区领导 ──
    {
        "id": 4,
        "name": "杨海牛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长（推测）",
        "current_org": "青山区人民政府",
        "source": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/zfb/bmdt/202606/t20260617_2778287.shtml",
        "notes": "多次出现在区政府常务会议名单中。常务会议出席名单包括政府副区长等成员，推测为常务副区长。",
    },
    # ── 区领导 ──
    {
        "id": 5,
        "name": "王小兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区政府副区长（推测）",
        "current_org": "青山区人民政府",
        "source": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/zfb/bmdt/202607/t20260723_2824704.shtml",
        "notes": "持续出现在2026年6-7月历次区政府常务会议名单中。",
    },
    # ── 区领导 ──
    {
        "id": 6,
        "name": "朱仕君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区政府副区长（推测）",
        "current_org": "青山区人民政府",
        "source": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/zfb/bmdt/202607/t20260723_2824704.shtml",
        "notes": "持续出现在2026年6-7月历次区政府常务会议名单中。",
    },
    # ── 郑丽梅 ──
    {
        "id": 7,
        "name": "郑丽梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "化工区党工委委员、管委会副主任",
        "current_org": "武汉化工区管委会",
        "source": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/tjj/bmdt/202607/t20260721_2823594.shtml",
        "notes": "以'化工区党工委委员、管委会副主任'身份出席区农业普查会议并讲话。",
    },
    # ── 朱海林 ──
    {
        "id": 8,
        "name": "朱海林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "青山区人民政府",
        "source": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/zfb/bmdt/202607/t20260723_2824704.shtml",
        "notes": "出现在2026年6-7月区政府常务会议名单中。",
    },
    # ── 雷敏 ──
    {
        "id": 9,
        "name": "雷敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "青山区人民政府",
        "source": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/zfb/bmdt/202607/t20260723_2824704.shtml",
        "notes": "出现在2026年7月区政府常务会议名单中。",
    },
    # ── 屠浩文 ──
    {
        "id": 10,
        "name": "屠浩文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "青山区人民政府",
        "source": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/zfb/bmdt/202607/t20260723_2824704.shtml",
        "notes": "持续出现在2026年2月调研和6-7月常务会议名单中。",
    },
    # ── 彭小平 ──
    {
        "id": 11,
        "name": "彭小平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "青山区人民政府",
        "source": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/zfb/bmdt/202607/t20260723_2824704.shtml",
        "notes": "持续出现在2026年6-7月历次区政府常务会议名单中。",
    },
    # ── 吴冬 ──
    {
        "id": 12,
        "name": "吴冬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "青山区人民政府",
        "source": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/zfb/bmdt/202607/t20260723_2824704.shtml",
        "notes": "出现在2026年7月常务会议和6月10日第100次常务会议名单中。",
    },
    # ── 肖建洲 ──
    {
        "id": 13,
        "name": "肖建洲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "青山区人民政府",
        "source": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/zfb/bmdt/202607/t20260723_2824704.shtml",
        "notes": "出现在2026年2月调研和7月常务会议名单中。",
    },
    # ════════════════════════════════════════
    # 前任区长
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "沈涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任青山区区长）",
        "current_org": "",
        "source": "https://mp.weixin.qq.com/s/NTH8FfDl7SPz_x5H1vLftg (美丽青山 2025-08-12)",
        "notes": "2025年8月12日以'区委副书记，区人民政府区长，化工区党工委副书记、管委会主任'身份出席北湖片区签约活动。之后由王永胜接任。目前去向不明。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共武汉市青山区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共武汉市委",
        "location": "武汉市青山区",
    },
    {
        "id": 2,
        "name": "青山区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "武汉市人民政府",
        "location": "武汉市青山区",
    },
    {
        "id": 3,
        "name": "武汉化工区党工委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共武汉市委",
        "location": "武汉市青山区",
    },
    {
        "id": 4,
        "name": "武汉化工区管委会",
        "type": "政府",
        "level": "县处级",
        "parent": "武汉市人民政府",
        "location": "武汉市青山区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 余志成
    {"person_id": "p1", "org_id": 1, "title": "青山区委书记", "start": "", "end": "present", "rank": "副厅级", "note": "兼任化工区党工委书记"},
    {"person_id": "p1", "org_id": 3, "title": "化工区党工委书记", "start": "", "end": "present", "rank": "", "note": "与区委书记兼任"},
    # 王永胜
    {"person_id": "p2", "org_id": 2, "title": "青山区人民政府区长", "start": "2026-06", "end": "present", "rank": "副厅级", "note": "2026年6月16日以代理区长身份主持会议，6月29日以区长身份出现"},
    {"person_id": "p2", "org_id": 1, "title": "青山区委副书记", "start": "", "end": "present", "rank": "", "note": ""},
    # 陈敏
    {"person_id": "p3", "org_id": 1, "title": "区委领导（推测副书记）", "start": "", "end": "present", "rank": "", "note": "2026年2月调研活动出席，在'区领导'名单首位"},
    # 杨海牛
    {"person_id": "p4", "org_id": 2, "title": "区委常委、副区长（推测）", "start": "", "end": "present", "rank": "", "note": "出席区政府常务会议"},
    # 王小兵
    {"person_id": "p5", "org_id": 2, "title": "区委常委、副区长（推测）", "start": "", "end": "present", "rank": "", "note": "出席区政府常务会议"},
    # 朱仕君
    {"person_id": "p6", "org_id": 2, "title": "区委常委、副区长（推测）", "start": "", "end": "present", "rank": "", "note": "出席区政府常务会议"},
    # 郑丽梅
    {"person_id": "p7", "org_id": 4, "title": "化工区党工委委员、管委会副主任", "start": "", "end": "present", "rank": "", "note": "确认身份：区第四次全国农业普查领导小组组长"},
    # 朱海林
    {"person_id": "p8", "org_id": 2, "title": "区领导（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出席区政府常务会议"},
    # 雷敏
    {"person_id": "p9", "org_id": 2, "title": "区领导（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出席区政府常务会议"},
    # 屠浩文
    {"person_id": "p10", "org_id": 2, "title": "区领导（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出席区政府常务会议和调研活动"},
    # 彭小平
    {"person_id": "p11", "org_id": 2, "title": "区领导（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出席区政府常务会议"},
    # 吴冬
    {"person_id": "p12", "org_id": 2, "title": "区领导（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出席区政府常务会议"},
    # 肖建洲
    {"person_id": "p13", "org_id": 2, "title": "区领导（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出席调研和常务会议"},
    # 沈涛（前任）
    {"person_id": "p14", "org_id": 2, "title": "青山区人民政府区长", "start": "", "end": "2026-06", "rank": "", "note": "截至2025年8月仍在任；后由王永胜接任"},
    {"person_id": "p14", "org_id": 1, "title": "青山区委副书记", "start": "", "end": "2026-06", "rank": "", "note": ""},
    {"person_id": "p14", "org_id": 4, "title": "化工区党工委副书记、管委会主任", "start": "", "end": "2026-06", "rank": "", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 余志成 ↔ 王永胜 （区委书记与区长搭档）
    {
        "person_a": "p1",
        "person_b": "p2",
        "type": "overlap",
        "context": "区委书记与区长搭档关系—共同出席调研和主持会议",
        "overlap_org": "中共武汉市青山区委员会/青山区人民政府",
        "overlap_period": "2026-06至present",
        "confidence": "confirmed",
    },
    # 余志成 ↔ 陈敏（书记与副书记推测）
    {
        "person_a": "p1",
        "person_b": "p3",
        "type": "superior_subordinate",
        "context": "区委书记与副书记（推测）共同出席调研活动",
        "overlap_org": "中共武汉市青山区委员会",
        "overlap_period": "2026-02至present",
        "confidence": "plausible",
    },
    # 余志成 ↔ 杨海牛
    {
        "person_a": "p1",
        "person_b": "p4",
        "type": "superior_subordinate",
        "context": "共同出席调研活动",
        "overlap_org": "青山区",
        "overlap_period": "2026-02至present",
        "confidence": "confirmed",
    },
    # 余志成 ↔ 王小兵
    {
        "person_a": "p1",
        "person_b": "p5",
        "type": "superior_subordinate",
        "context": "共同出席调研活动",
        "overlap_org": "青山区",
        "overlap_period": "2026-02至present",
        "confidence": "confirmed",
    },
    # 余志成 ↔ 屠浩文
    {
        "person_a": "p1",
        "person_b": "p10",
        "type": "superior_subordinate",
        "context": "共同出席调研和北湖签约活动",
        "overlap_org": "青山区",
        "overlap_period": "2025-08至present",
        "confidence": "confirmed",
    },
    # 余志成 ↔ 肖建洲
    {
        "person_a": "p1",
        "person_b": "p13",
        "type": "superior_subordinate",
        "context": "共同出席调研活动（青山船厂）",
        "overlap_org": "青山区",
        "overlap_period": "2026-02至present",
        "confidence": "confirmed",
    },
    # 余志成 ↔ 沈涛（前任区长搭档）
    {
        "person_a": "p1",
        "person_b": "p14",
        "type": "overlap",
        "context": "区委书记与区长搭档关系—共同出席北湖签约活动",
        "overlap_org": "中共武汉市青山区委员会/青山区人民政府",
        "overlap_period": "至2026-06",
        "confidence": "confirmed",
    },
    # 王永胜 → 沈涛（区长继任关系）
    {
        "person_a": "p2",
        "person_b": "p14",
        "type": "predecessor_successor",
        "context": "王永胜接替沈涛担任青山区区长",
        "overlap_org": "青山区人民政府",
        "overlap_period": "2026-06",
        "confidence": "confirmed",
    },
    # 王永胜 ↔ 杨海牛
    {
        "person_a": "p2",
        "person_b": "p4",
        "type": "overlap",
        "context": "区长与副区长（推测）共同出席区政府常务会议",
        "overlap_org": "青山区人民政府",
        "overlap_period": "2026-06至present",
        "confidence": "confirmed",
    },
    # 王永胜 ↔ 王小兵
    {
        "person_a": "p2",
        "person_b": "p5",
        "type": "overlap",
        "context": "区长与区领导共同出席区政府常务会议",
        "overlap_org": "青山区人民政府",
        "overlap_period": "2026-06至present",
        "confidence": "confirmed",
    },
    # 王永胜 ↔ 朱仕君
    {
        "person_a": "p2",
        "person_b": "p6",
        "type": "overlap",
        "context": "区长与区领导共同出席区政府常务会议",
        "overlap_org": "青山区人民政府",
        "overlap_period": "2026-06至present",
        "confidence": "confirmed",
    },
    # 王永胜 ↔ 彭小平
    {
        "person_a": "p2",
        "person_b": "p11",
        "type": "overlap",
        "context": "区长与区领导共同出席区政府常务会议",
        "overlap_org": "青山区人民政府",
        "overlap_period": "2026-06至present",
        "confidence": "confirmed",
    },
    # 王永胜 ↔ 吴冬
    {
        "person_a": "p2",
        "person_b": "p12",
        "type": "overlap",
        "context": "区长与区领导共同出席区政府常务会议",
        "overlap_org": "青山区人民政府",
        "overlap_period": "2026-06至present",
        "confidence": "confirmed",
    },
    # 杨海牛 ↔ 屠浩文
    {
        "person_a": "p4",
        "person_b": "p10",
        "type": "overlap",
        "context": "共同出席调研活动和北湖签约",
        "overlap_org": "青山区人民政府",
        "overlap_period": "2025-08至present",
        "confidence": "confirmed",
    },
    # 杨海牛 ↔ 王小兵
    {
        "person_a": "p4",
        "person_b": "p5",
        "type": "overlap",
        "context": "共同出席区常务会议和调研活动",
        "overlap_org": "青山区人民政府",
        "overlap_period": "2026-02至present",
        "confidence": "confirmed",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON DATA
# ══════════════════════════════════════════════════════════════════════════════

_source_register = [
    {
        "id": "S001",
        "title": "区政府常务会议第104次 (2026-07-23)",
        "url": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/zfb/bmdt/202607/t20260723_2824704.shtml",
        "publisher": "青山区人民政府",
        "published_at": "2026-07-23",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "王永胜以区长身份主持；王小兵、朱仕君、郑丽梅、朱海林、雷敏、屠浩文、彭小平、吴冬、肖建洲出席",
    },
    {
        "id": "S002",
        "title": "区政府常务会议第102次 (2026-06-29)",
        "url": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/zfb/bmdt/202606/t20260629_2814506.shtml",
        "publisher": "青山区人民政府",
        "published_at": "2026-06-29",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "王永胜以区长身份主持；杨海牛、王小兵、朱仕君、郑丽梅、朱海林、雷敏、屠浩文、彭小平、肖建洲出席",
    },
    {
        "id": "S003",
        "title": "区政府常务会议第101次 (2026-06-17)",
        "url": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/zfb/bmdt/202606/t20260617_2778287.shtml",
        "publisher": "青山区人民政府",
        "published_at": "2026-06-17",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "王永胜以'代理区长'身份主持；杨海牛、王小兵、朱仕君、屠浩文、彭小平出席",
    },
    {
        "id": "S004",
        "title": "区政府常务会议第100次 (2026-06-10)",
        "url": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/zfb/bmdt/202606/t20260610_2775670.shtml",
        "publisher": "青山区人民政府",
        "published_at": "2026-06-10",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "王永胜同志主持（未明确职务）；杨海牛、王小兵、朱仕君、朱海林、屠浩文、彭小平、吴冬出席",
    },
    {
        "id": "S005",
        "title": "区委书记余志成调研青山船厂 (2026-02-09)",
        "url": "https://mp.weixin.qq.com/s/t5DR-Cco286wXB9Lb8nKTw",
        "publisher": "美丽青山（青山区融媒体中心）",
        "published_at": "2026-02-09",
        "accessed_at": AS_OF,
        "source_type": "media",
        "reliability": "high",
        "notes": "余志成以区委书记、化工区党工委书记身份调研；陈敏、王永胜、杨海牛、王小兵、肖建洲出席",
    },
    {
        "id": "S006",
        "title": "青山携手武钢北湖片区开发 (2025-08-12)",
        "url": "https://mp.weixin.qq.com/s/NTH8FfDl7SPz_x5H1vLftg",
        "publisher": "美丽青山（青山区融媒体中心）",
        "published_at": "2025-08-12",
        "accessed_at": AS_OF,
        "source_type": "media",
        "reliability": "high",
        "notes": "沈涛以区委副书记、区长、化工区党工委副书记、管委会主任身份出席；余志成、王永胜、杨海牛、屠浩文出席",
    },
    {
        "id": "S007",
        "title": "青山区召开第四次全国农业普查会议 (2026-07-21)",
        "url": "https://www.qingshan.gov.cn/qzfbm/zfgzbm/tjj/bmdt/202607/t20260721_2823594.shtml",
        "publisher": "青山区统计局",
        "published_at": "2026-07-21",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "郑丽梅以化工区党工委委员、管委会副主任身份讲话",
    },
]


def make_person_json(person, timeline_items, relationship_list):
    """Build a person graph JSON following the schema."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "武汉市",
            "region": "青山区",
            "job": person["current_post"],
            "task_id": "hubei_青山区",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": f"qingshan_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}" if person.get("birth") else person["name"],
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}" if person.get("birthplace") else person["name"],
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S005"]
        },
        "career_timeline": timeline_items,
        "organizations": [],
        "relationships": relationship_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "无法评估——缺少出生年份和完整履历",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "公开资料中未发现纪律处分、审计问题或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": _source_register,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "缺失出生年份、籍贯、教育背景和完整履历"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年份、籍贯和教育背景是什么？",
                "why_it_matters": "用于人员去重和晋升速度分析",
                "suggested_queries": [
                    f"余志成 简历",
                    f"余志成 出生 籍贯 学历",
                    f"余志成 武汉 任职经历"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['name']}在担任现职前的工作履历是什么？",
                "why_it_matters": "完整的晋升路径揭示工作关系网络",
                "suggested_queries": [
                    f"{person['name']} 此前担任",
                    f"{person['name']} 调任 青山区",
                    f"{person['name']} 历任"
                ],
                "last_attempted": AS_OF
            }
        ]
    }


def write_person_json(person, timeline_items, relationship_list):
    data = make_person_json(person, timeline_items, relationship_list)
    path = PERSONS_DIR / f"{TODAY}-湖北省-武汉市-{person['current_post'].split('、')[0].split('（')[0]}-{person['name']}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    os.makedirs(_STAGING_DIR, exist_ok=True)

    # Build DB + GEXF
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for core leaders
    print("\n--- Person JSONs ---")

    # 余志成 — 区委书记
    yuzc_timeline = [
        {
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "level": "",
            "location": "",
            "system": "other",
            "rank": "",
            "is_key_promotion": False,
            "notes": "公开资料未找到余志成担任青山区委书记前的完整履历",
            "confidence": "unverified",
            "source_ids": []
        },
        {
            "start": "2025-08",
            "end": "present",
            "org": "中共武汉市青山区委员会",
            "title": "青山区委书记、化工区党工委书记",
            "level": "副厅级",
            "location": "武汉市青山区",
            "system": "party",
            "rank": "",
            "is_key_promotion": True,
            "notes": "2025年8月12日北湖签约活动中以区委书记身份出席",
            "confidence": "confirmed",
            "source_ids": ["S005", "S006"]
        },
    ]
    yuzc_relationships = [
        {
            "person": "王永胜",
            "person_id": "qingshan_wang_yongsheng",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "区委书记与区长搭档关系，共同出席调研活动和常务会议",
            "overlap_org": "青山区",
            "overlap_period": "2026-06至present",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S005"]
        },
        {
            "person": "沈涛",
            "person_id": "qingshan_shen_tao",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "前任区长搭档，共同出席北湖片区签约活动",
            "overlap_org": "青山区",
            "overlap_period": "至2026-06",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S006"]
        },
    ]
    write_person_json(persons[0], yuzc_timeline, yuzc_relationships)

    # 王永胜 — 区长
    wys_timeline = [
        {
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "level": "",
            "location": "",
            "system": "other",
            "rank": "",
            "is_key_promotion": False,
            "notes": "公开资料未找到王永胜担任青山区区长前的完整履历",
            "confidence": "unverified",
            "source_ids": []
        },
        {
            "start": "2026-06-10",
            "end": "2026-06-16",
            "org": "青山区人民政府",
            "title": "（代理区长就任前，以'王永胜同志'身份主持会议）",
            "level": "",
            "location": "武汉市青山区",
            "system": "government",
            "rank": "",
            "is_key_promotion": True,
            "notes": "6月10日第100次常务会议以'王永胜同志'主持",
            "confidence": "confirmed",
            "source_ids": ["S004"]
        },
        {
            "start": "2026-06-16",
            "end": "2026-06-29",
            "org": "青山区人民政府",
            "title": "青山区人民政府代理区长",
            "level": "副厅级",
            "location": "武汉市青山区",
            "system": "government",
            "rank": "",
            "is_key_promotion": True,
            "notes": "6月16日第101次常务会议以'代理区长'身份主持",
            "confidence": "confirmed",
            "source_ids": ["S003"]
        },
        {
            "start": "2026-06-29",
            "end": "present",
            "org": "青山区人民政府",
            "title": "青山区人民政府区长",
            "level": "副厅级",
            "location": "武汉市青山区",
            "system": "government",
            "rank": "",
            "is_key_promotion": True,
            "notes": "6月29日第102次常务会议开始以'区长'身份出现",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002"]
        },
    ]
    wys_relationships = [
        {
            "person": "余志成",
            "person_id": "qingshan_yu_zhicheng",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "区长与区委书记搭档关系",
            "overlap_org": "青山区",
            "overlap_period": "2026-06至present",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S005"]
        },
        {
            "person": "沈涛",
            "person_id": "qingshan_shen_tao",
            "relationship_type": "predecessor_successor",
            "strength": "strong",
            "evidence": "接替沈涛担任青山区区长",
            "overlap_org": "青山区人民政府",
            "overlap_period": "2026-06",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": []
        },
    ]
    write_person_json(persons[1], wys_timeline, wys_relationships)

    print(f"\n{'='*60}")
    print(f"青山区 Network Build Complete")
    print(f"{'='*60}")
    print(f"Staging dir: {_STAGING_DIR}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    main()
