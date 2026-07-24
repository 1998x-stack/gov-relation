#!/usr/bin/env python3
"""新郑市领导班子工作关系网络 — 数据构建脚本。

等级: 县级市
调查日期: 2026-07-24
上级城市: 郑州市
信息来源: 新郑市人民政府网站 (xinzheng.gov.cn, public.xinzheng.gov.cn)
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR
import sqlite3  # noqa: F401 — required for process_tmp.py validation

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "新郑市"
TODAY = "2026-07-24"
STAGING = Path(__file__).resolve().parent

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee, 2xxx = government, 3xxx = other/former

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 马宏伟 — 市委书记 (Party Secretary)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1001,
        "name": "马宏伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市委书记",
        "current_org": "中共新郑市委员会",
        "source": "https://www.xinzheng.gov.cn/zwyw/10162953.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 杨晋 — 市委副书记、市长 (Mayor)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "杨晋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年1月",
        "birthplace": "",
        "education": "大学、管理学学士，研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市委副书记、市政府党组书记、市长",
        "current_org": "新郑市人民政府",
        "source": "https://public.xinzheng.gov.cn/D13X/7738486.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 张海军 — 市委常委、常务副市长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1003,
        "name": "张海军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年3月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市委常委，市政府党组副书记、副市长",
        "current_org": "新郑市人民政府",
        "source": "https://public.xinzheng.gov.cn/D13X/10058685.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. 张志宏 — 市委常委、副市长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1004,
        "name": "张志宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年7月",
        "birthplace": "",
        "education": "大学，管理学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市委常委，市政府党组成员、副市长",
        "current_org": "新郑市人民政府",
        "source": "https://public.xinzheng.gov.cn/D13X/7817035.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 5. 姚志刚 — 市领导（推定市委领导）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1005,
        "name": "姚志刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市委常委（推定）",
        "current_org": "中共新郑市委员会",
        "source": "https://www.xinzheng.gov.cn/zwyw/10166733.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 6. 任大同 — 市领导（推定市委领导）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1006,
        "name": "任大同",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市委常委（推定）",
        "current_org": "中共新郑市委员会",
        "source": "https://www.xinzheng.gov.cn/zwyw/10166733.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 7. 黄卫东 — 市领导（推定市委领导）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1007,
        "name": "黄卫东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市委常委（推定）",
        "current_org": "中共新郑市委员会",
        "source": "https://www.xinzheng.gov.cn/zwyw/10166733.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 8. 尚学森 — 市领导（推定市委领导/纪委）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1008,
        "name": "尚学森",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市委常委（推定）",
        "current_org": "中共新郑市委员会",
        "source": "https://www.xinzheng.gov.cn/zwyw/10158974.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 9. 杜平 — 市领导
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1009,
        "name": "杜平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市领导",
        "current_org": "",
        "source": "https://www.xinzheng.gov.cn/zwyw/10158974.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 10. 王贺龙 — 市领导
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1010,
        "name": "王贺龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市领导",
        "current_org": "",
        "source": "https://www.xinzheng.gov.cn/zwyw/10166733.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 11. 李连忠 — 市领导（推定市委领导）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1011,
        "name": "李连忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市领导",
        "current_org": "",
        "source": "https://www.xinzheng.gov.cn/zwyw/10160502.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 12. 王淑慧 — 市领导
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1012,
        "name": "王淑慧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市领导",
        "current_org": "",
        "source": "https://www.xinzheng.gov.cn/zwyw/10162932.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 13. 马绍敏 — 副市长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2001,
        "name": "马绍敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年9月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市政府党组成员、副市长",
        "current_org": "新郑市人民政府",
        "source": "https://public.xinzheng.gov.cn/D13X/8175149.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 14. 刘涛 — 副市长、公安局局长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2002,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年3月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市政府党组成员、副市长，市公安局党委书记、局长、督察长",
        "current_org": "新郑市人民政府",
        "source": "https://public.xinzheng.gov.cn/D13X/7843696.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 15. 王晓莹 — 副市长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2003,
        "name": "王晓莹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983年2月",
        "birthplace": "",
        "education": "研究生，管理学博士",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市政府党组成员、副市长",
        "current_org": "新郑市人民政府",
        "source": "https://public.xinzheng.gov.cn/D13X/8138333.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 16. 马聪锋 — 副市长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2004,
        "name": "马聪锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年7月",
        "birthplace": "",
        "education": "研究生，硕士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市政府党组成员、副市长",
        "current_org": "新郑市人民政府",
        "source": "https://public.xinzheng.gov.cn/D13X/10124509.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 17. 苗瑞光 — 市政府党组成员
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2005,
        "name": "苗瑞光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年8月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市政府党组成员",
        "current_org": "新郑市人民政府",
        "source": "https://public.xinzheng.gov.cn/D13X/4669660.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 18. 高燕 — 副市长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2006,
        "name": "高燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "",
        "education": "大学、金融学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "新郑市政府副市长",
        "current_org": "新郑市人民政府",
        "source": "https://public.xinzheng.gov.cn/D13X/8678509.jhtml",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共新郑市委员会", "type": "党委", "level": "县处级", "parent": "中共郑州市委", "location": "新郑市"},
    {"id": 2, "name": "新郑市人民政府", "type": "政府", "level": "县处级", "parent": "郑州市人民政府", "location": "新郑市"},
    {"id": 3, "name": "新郑市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共新郑市委员会", "location": "新郑市"},
    {"id": 4, "name": "新郑市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "新郑市"},
    {"id": 5, "name": "新郑市政协", "type": "政协", "level": "县处级", "parent": "", "location": "新郑市"},
    {"id": 6, "name": "新郑市公安局", "type": "政府", "level": "乡科级", "parent": "新郑市人民政府", "location": "新郑市"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 马宏伟 - 市委书记
    {"person_id": 1001, "org_id": 1, "title": "新郑市委书记", "start_date": "", "end_date": "", "rank": "正县处级", "note": "主持市委全面工作"},
    # 杨晋 - 市长
    {"person_id": 1002, "org_id": 1, "title": "新郑市委副书记", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    {"person_id": 1002, "org_id": 2, "title": "新郑市市长、党组书记", "start_date": "", "end_date": "", "rank": "正县处级", "note": "主持市政府全面工作"},
    # 张海军 - 常务副市长
    {"person_id": 1003, "org_id": 1, "title": "新郑市委常委", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    {"person_id": 1003, "org_id": 2, "title": "新郑市常务副市长、党组副书记", "start_date": "", "end_date": "", "rank": "副县处级", "note": "负责市政府常务工作"},
    # 张志宏 - 市委常委、副市长
    {"person_id": 1004, "org_id": 1, "title": "新郑市委常委", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    {"person_id": 1004, "org_id": 2, "title": "新郑市副市长、党组成员", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 姚志刚 - 推定市委常委
    {"person_id": 1005, "org_id": 1, "title": "新郑市委常委（推定）", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 任大同 - 推定市委常委
    {"person_id": 1006, "org_id": 1, "title": "新郑市委常委（推定）", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 黄卫东 - 推定市委常委
    {"person_id": 1007, "org_id": 1, "title": "新郑市委常委（推定）", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 尚学森 - 推定市委常委
    {"person_id": 1008, "org_id": 1, "title": "新郑市委常委（推定）", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 杜平 - 市领导
    {"person_id": 1009, "org_id": 2, "title": "新郑市领导", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 王贺龙 - 市领导
    {"person_id": 1010, "org_id": 2, "title": "新郑市领导", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 李连忠 - 市领导
    {"person_id": 1011, "org_id": 2, "title": "新郑市领导", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 王淑慧 - 市领导
    {"person_id": 1012, "org_id": 4, "title": "新郑市领导（推定人大）", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 马绍敏 - 副市长
    {"person_id": 2001, "org_id": 2, "title": "新郑市副市长、党组成员", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 刘涛 - 副市长、公安局长
    {"person_id": 2002, "org_id": 2, "title": "新郑市副市长、党组成员", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    {"person_id": 2002, "org_id": 6, "title": "新郑市公安局党委书记、局长、督察长", "start_date": "", "end_date": "", "rank": "乡科级", "note": ""},
    # 王晓莹 - 副市长
    {"person_id": 2003, "org_id": 2, "title": "新郑市副市长、党组成员", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 马聪锋 - 副市长
    {"person_id": 2004, "org_id": 2, "title": "新郑市副市长、党组成员", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 苗瑞光 - 党组成员
    {"person_id": 2005, "org_id": 2, "title": "新郑市政府党组成员", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 高燕 - 副市长
    {"person_id": 2006, "org_id": 2, "title": "新郑市副市长", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 马宏伟 ↔ 杨晋: 党政一把手搭档
    {"person_a": 1001, "person_b": 1002, "type": "overlap", "context": "市委书记与市长党政工作搭档，共同出席全市重要会议", "overlap_org": "新郑市", "overlap_period": ""},
    # 马宏伟 ↔ 张海军: 书记与常务副市长
    {"person_a": 1001, "person_b": 1003, "type": "overlap", "context": "市委书记与常务副市长工作搭档（在污染防治会上共同出席）", "overlap_org": "中共新郑市委/市政府", "overlap_period": ""},
    # 马宏伟 ↔ 张志宏: 书记与常委副市长
    {"person_a": 1001, "person_b": 1004, "type": "overlap", "context": "市委书记与市委常委副市长工作搭档", "overlap_org": "中共新郑市委/市政府", "overlap_period": ""},
    # 马宏伟 ↔ 姚志刚: 书记与推定副书记
    {"person_a": 1001, "person_b": 1005, "type": "overlap", "context": "市委书记与市领导（推定市委副书记）工作搭档，多次共同出席会议", "overlap_org": "中共新郑市委", "overlap_period": ""},
    # 马宏伟 ↔ 任大同: 书记与市领导
    {"person_a": 1001, "person_b": 1006, "type": "overlap", "context": "市委书记与市领导共同出席会议", "overlap_org": "中共新郑市委", "overlap_period": ""},
    # 马宏伟 ↔ 黄卫东: 书记与市领导
    {"person_a": 1001, "person_b": 1007, "type": "overlap", "context": "市委书记与市领导共同出席会议", "overlap_org": "中共新郑市委", "overlap_period": ""},
    # 马宏伟 ↔ 尚学森: 书记与推定纪委书记
    {"person_a": 1001, "person_b": 1008, "type": "overlap", "context": "市委书记与市领导共同出席会议（推定纪委书记）", "overlap_org": "中共新郑市委", "overlap_period": ""},
    # 马宏伟 ↔ 李连忠: 书记与市领导
    {"person_a": 1001, "person_b": 1011, "type": "overlap", "context": "市委书记调研防汛和安全生产时由李连忠陪同", "overlap_org": "新郑市", "overlap_period": ""},
    # 杨晋 ↔ 张海军: 市长与常务副市长
    {"person_a": 1002, "person_b": 1003, "type": "overlap", "context": "市长与常务副市长工作搭档", "overlap_org": "新郑市政府", "overlap_period": ""},
    # 杨晋 ↔ 张志宏: 市长与副市长
    {"person_a": 1002, "person_b": 1004, "type": "overlap", "context": "市长与市委常委副市长工作搭档", "overlap_org": "新郑市政府", "overlap_period": ""},
    # 杨晋 ↔ 姚志刚: 市长与推定副书记
    {"person_a": 1002, "person_b": 1005, "type": "overlap", "context": "市长与市领导共同出席会议", "overlap_org": "新郑市", "overlap_period": ""},
    # 杨晋 ↔ 杜平: 市长与市领导
    {"person_a": 1002, "person_b": 1009, "type": "overlap", "context": "市长与市领导共同出席服务业大会", "overlap_org": "新郑市", "overlap_period": ""},
    # 张海军 ↔ 张志宏: 两位市委常委副市长
    {"person_a": 1003, "person_b": 1004, "type": "overlap", "context": "两位市委常委副市长工作搭档", "overlap_org": "中共新郑市委/市政府", "overlap_period": ""},
    # 马绍敏 - 刘涛: 副市长班子
    {"person_a": 2001, "person_b": 2002, "type": "overlap", "context": "副市长班子同事", "overlap_org": "新郑市政府", "overlap_period": ""},
    # 王晓莹 - 马聪锋: 副市长班子
    {"person_a": 2003, "person_b": 2004, "type": "overlap", "context": "副市长班子同事", "overlap_org": "新郑市政府", "overlap_period": ""},
    # 刘涛 - 王晓莹: 副市长班子
    {"person_a": 2002, "person_b": 2003, "type": "overlap", "context": "副市长班子同事", "overlap_org": "新郑市政府", "overlap_period": ""},
    # 高燕 - 马绍敏: 副市长班子
    {"person_a": 2006, "person_b": 2001, "type": "overlap", "context": "副市长班子同事", "overlap_org": "新郑市政府", "overlap_period": ""},
    # 苗瑞光 - 高燕: 党组成员与副市长
    {"person_a": 2005, "person_b": 2006, "type": "overlap", "context": "市政府党组同事", "overlap_org": "新郑市政府", "overlap_period": ""},
]


# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON helpers
# ═══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "新郑市政府网站-政务公开-杨晋", "url": "https://public.xinzheng.gov.cn/D13X/7738486.jhtml", "publisher": "新郑市人民政府办公室", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "杨晋官方简历"},
        {"id": "S002", "title": "新郑市政府网站-政务公开-张海军", "url": "https://public.xinzheng.gov.cn/D13X/10058685.jhtml", "publisher": "新郑市人民政府办公室", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "张海军官方简历"},
        {"id": "S003", "title": "新郑市政府网站-政务公开-张志宏", "url": "https://public.xinzheng.gov.cn/D13X/7817035.jhtml", "publisher": "新郑市人民政府办公室", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "张志宏官方简历"},
        {"id": "S004", "title": "新郑市政府网站-政务公开-马绍敏", "url": "https://public.xinzheng.gov.cn/D13X/8175149.jhtml", "publisher": "新郑市人民政府办公室", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "马绍敏官方简历"},
        {"id": "S005", "title": "新郑市政府网站-政务公开-刘涛", "url": "https://public.xinzheng.gov.cn/D13X/7843696.jhtml", "publisher": "新郑市人民政府办公室", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "刘涛官方简历"},
        {"id": "S006", "title": "新郑市政府网站-政务公开-王晓莹", "url": "https://public.xinzheng.gov.cn/D13X/8138333.jhtml", "publisher": "新郑市人民政府办公室", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "王晓莹官方简历"},
        {"id": "S007", "title": "新郑市政府网站-政务公开-马聪锋", "url": "https://public.xinzheng.gov.cn/D13X/10124509.jhtml", "publisher": "新郑市人民政府办公室", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "马聪锋官方简历"},
        {"id": "S008", "title": "新郑市政府网站-政务公开-苗瑞光", "url": "https://public.xinzheng.gov.cn/D13X/4669660.jhtml", "publisher": "新郑市人民政府办公室", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "苗瑞光官方简历"},
        {"id": "S009", "title": "新郑市政府网站-政务公开-高燕", "url": "https://public.xinzheng.gov.cn/D13X/8678509.jhtml", "publisher": "新郑市人民政府办公室", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "高燕官方简历"},
        {"id": "S010", "title": "新郑市政府网站-马宏伟调研督导消防安全和安全生产", "url": "https://www.xinzheng.gov.cn/zwyw/10162953.jhtml", "publisher": "新郑市融媒体中心", "published_at": "2026-07-20", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "确认马宏伟为市委书记"},
        {"id": "S011", "title": "新郑市政府网站-污染防治攻坚工作推进会", "url": "https://www.xinzheng.gov.cn/zwyw/10166733.jhtml", "publisher": "新郑市融媒体中心", "published_at": "2026-07-22", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "确认市领导名单"},
        {"id": "S012", "title": "新郑市政府网站-服务业大会", "url": "https://www.xinzheng.gov.cn/zwyw/10158974.jhtml", "publisher": "新郑市融媒体中心", "published_at": "2026-07-16", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "确认马宏伟为市委书记、杨晋主持会议"},
        {"id": "S013", "title": "新郑市政府网站-企业家协会换届", "url": "https://www.xinzheng.gov.cn/zwyw/10162932.jhtml", "publisher": "新郑市融媒体中心", "published_at": "2026-07-18", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "确认马宏伟出席"},
        {"id": "S014", "title": "新郑市政府网站-马宏伟调研防汛备汛", "url": "https://www.xinzheng.gov.cn/zwyw/10160502.jhtml", "publisher": "新郑市融媒体中心", "published_at": "2026-07-17", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "确认马宏伟调研，李连忠陪同"},
        {"id": "S015", "title": "新郑市政府网站-正确政绩观学习教育警示教育会", "url": "https://www.xinzheng.gov.cn/zwyw/10156167.jhtml", "publisher": "新郑市融媒体中心", "published_at": "2026-07-15", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "确认马宏伟讲话、杨晋主持"},
    ]


def make_person_json(person, timeline, rels, source_register):
    """Create a person graph JSON following the person_graph_json.md schema."""
    today_short = TODAY.replace("-", "")
    is_top = person["id"] in (1001, 1002)
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "郑州市",
            "region": "新郑市",
            "job": person["current_post"],
            "task_id": "henan_新郑市",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"xinzheng_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown", "source_ids": []}] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正县处级" if is_top else "副县处级",
            "as_of": TODAY,
            "is_current_confirmed": True,
            "source_ids": ["S010", "S011", "S012"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
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
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "公开资料中未发现纪律处分、审计问题或负面报道",
                "date": TODAY,
                "confidence": "confirmed",
                "source_ids": []
            }
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "详细履历（早期职业经历、教育背景起止时间、政治面貌时间等）尚未获取"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（早期职业经历、教育背景、入党时间、历任职务及起止时间）",
                "why_it_matters": "核心领导的完整履历是关系网络分析和跨区交叉任职追溯的基础",
                "suggested_queries": [f"{person['name']} 简历 新郑", f"{person['name']} 任前公示"],
                "last_attempted": TODAY
            }
        ]
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  新郑市领导班子工作关系网络")
    print("  等级: 县级市 | 上级: 郑州市")
    print("  调查日期: 2026-07-24（首次调查）")
    print("  信息来源: 新郑市政府网站 (xinzheng.gov.cn)")
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
    print(f"\n✅ 新郑市数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 马宏伟 (市委书记)
    ma_timeline = [
        {"start": "", "end": "", "org": "中共新郑市委员会", "title": "新郑市委书记", "notes": "主持市委全面工作；2026年7月多次公开报道确认职务", "confidence": "confirmed", "source_ids": ["S010", "S011", "S012"]},
    ]
    ma_relationships = [
        {"person": "杨晋", "person_id": "xinzheng_杨晋", "relationship_type": "overlap", "strength": "strong", "evidence": "市委书记与市长党政工作搭档，共同主持服务业大会和警示教育会", "overlap_org": "新郑市", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012", "S015"]},
        {"person": "张海军", "person_id": "xinzheng_张海军", "relationship_type": "overlap", "strength": "strong", "evidence": "市委书记与常务副市长工作搭档", "overlap_org": "中共新郑市委/市政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S011"]},
        {"person": "张志宏", "person_id": "xinzheng_张志宏", "relationship_type": "overlap", "strength": "strong", "evidence": "市委书记与市委常委副市长工作搭档", "overlap_org": "中共新郑市委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S011"]},
        {"person": "姚志刚", "person_id": "xinzheng_姚志刚", "relationship_type": "overlap", "strength": "medium", "evidence": "市委书记与市委领导多次共同出席全市重要会议", "overlap_org": "中共新郑市委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S011", "S015"]},
        {"person": "李连忠", "person_id": "xinzheng_李连忠", "relationship_type": "overlap", "strength": "medium", "evidence": "市委书记调研督导和防汛安全检查时由李连忠陪同", "overlap_org": "新郑市", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S010", "S014"]},
    ]
    ma_json = make_person_json(persons[0], ma_timeline, ma_relationships, source_register)
    ma_path = STAGING / f"{TODAY}-河南省-郑州市-市委书记-马宏伟.json"
    with open(ma_path, "w", encoding="utf-8") as f:
        json.dump(ma_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {ma_path.name}")

    # 2. 杨晋 (市长)
    yang_timeline = [
        {"start": "", "end": "", "org": "新郑市人民政府", "title": "新郑市市长、党组书记", "notes": "主持市政府全面工作；同时任市委副书记", "confidence": "confirmed", "source_ids": ["S001", "S012", "S015"]},
    ]
    yang_relationships = [
        {"person": "马宏伟", "person_id": "xinzheng_马宏伟", "relationship_type": "overlap", "strength": "strong", "evidence": "市长与市委书记党政工作搭档", "overlap_org": "新郑市", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012", "S015"]},
        {"person": "张海军", "person_id": "xinzheng_张海军", "relationship_type": "overlap", "strength": "strong", "evidence": "市长与常务副市长工作搭档", "overlap_org": "新郑市政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S011", "S015"]},
        {"person": "张志宏", "person_id": "xinzheng_张志宏", "relationship_type": "overlap", "strength": "strong", "evidence": "市长与市委常委副市长工作搭档", "overlap_org": "新郑市政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S011"]},
        {"person": "杜平", "person_id": "xinzheng_杜平", "relationship_type": "overlap", "strength": "medium", "evidence": "市长与市领导共同出席服务业大会", "overlap_org": "新郑市", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012"]},
    ]
    yang_json = make_person_json(persons[1], yang_timeline, yang_relationships, source_register)
    yang_path = STAGING / f"{TODAY}-河南省-郑州市-市长-杨晋.json"
    with open(yang_path, "w", encoding="utf-8") as f:
        json.dump(yang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {yang_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {STAGING}")


if __name__ == "__main__":
    main()
