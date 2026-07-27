#!/usr/bin/env python3
"""郑州市中原区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区
调查日期: 2026-07-24
信息来源: 中原区人民政府网站 (zhongyuan.gov.cn, public.zhongyuan.gov.cn)
         中国共产党郑州市中原区第十三次代表大会新闻报道
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "中原区"
TODAY = "2026-07-24"
STAGING = Path(__file__).resolve().parent

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee, 2xxx = government

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 李晓雷 — 区委书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1001,
        "name": "李晓雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中原区委书记",
        "current_org": "中共郑州市中原区委员会",
        "source": "https://www.zhongyuan.gov.cn/zyyw/10153657.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 邓英文 — 区委副书记、区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "邓英文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年11月",
        "birthplace": "",
        "education": "研究生，公共管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "中原区委副书记、区政府区长、党组书记",
        "current_org": "中原区人民政府",
        "source": "https://public.zhongyuan.gov.cn/D13X/1698860.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 马素华 — 区委副书记（推定）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1003,
        "name": "马素华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中原区委副书记（推定）",
        "current_org": "中共郑州市中原区委员会",
        "source": "https://www.zhongyuan.gov.cn/zyyw/10118551.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. 房玉雯 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1004,
        "name": "房玉雯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中原区委常委",
        "current_org": "中共郑州市中原区委员会",
        "source": "https://www.zhongyuan.gov.cn/zyyw/10118551.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 5. 冯乐 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1005,
        "name": "冯乐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中原区委常委",
        "current_org": "中共郑州市中原区委员会",
        "source": "https://www.zhongyuan.gov.cn/zyyw/10118551.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 6. 周伟杰 — 区委常委、常务副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1006,
        "name": "周伟杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年11月",
        "birthplace": "",
        "education": "研究生，应用社会学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "中原区委常委、区政府副区长、党组副书记",
        "current_org": "中原区人民政府",
        "source": "https://public.zhongyuan.gov.cn/D13X/6064529.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 7. 武学德 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1007,
        "name": "武学德",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中原区委常委",
        "current_org": "中共郑州市中原区委员会",
        "source": "https://www.zhongyuan.gov.cn/zyyw/10118551.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 8. 郭学远 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1008,
        "name": "郭学远",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中原区委常委",
        "current_org": "中共郑州市中原区委员会",
        "source": "https://www.zhongyuan.gov.cn/zyyw/10118551.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 9. 李鑫 — 区委常委、副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1009,
        "name": "李鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年3月",
        "birthplace": "",
        "education": "研究生，工商管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "中原区委常委、区政府副区长、党组成员",
        "current_org": "中原区人民政府",
        "source": "https://public.zhongyuan.gov.cn/D13X/9214991.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 10. 孔健 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1010,
        "name": "孔健",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中原区委常委",
        "current_org": "中共郑州市中原区委员会",
        "source": "https://www.zhongyuan.gov.cn/zyyw/10118551.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 11. 刘超 — 区委常委、区委办主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1011,
        "name": "刘超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中原区委常委、区委办公室主任",
        "current_org": "中共郑州市中原区委员会",
        "source": "https://www.zhongyuan.gov.cn/zyyw/10128972.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 12. 李智 — 副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2001,
        "name": "李智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年7月",
        "birthplace": "",
        "education": "研究生，工学博士",
        "party_join": "",
        "work_start": "",
        "current_post": "中原区政府副区长、党组成员",
        "current_org": "中原区人民政府",
        "source": "https://public.zhongyuan.gov.cn/D13X/10136093.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 13. 李嵘 — 副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2002,
        "name": "李嵘",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年4月",
        "birthplace": "",
        "education": "研究生，工商管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "中原区政府副区长、党组成员",
        "current_org": "中原区人民政府",
        "source": "https://public.zhongyuan.gov.cn/D13X/9972102.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 14. 张毅 — 副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2003,
        "name": "张毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年9月",
        "birthplace": "",
        "education": "研究生，工学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "中原区政府副区长",
        "current_org": "中原区人民政府",
        "source": "https://public.zhongyuan.gov.cn/D13X/9947609.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 15. 薛晓军 — 前任区委领导（主席台就座）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 3001,
        "name": "薛晓军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（前任中原区领导）",
        "current_org": "",
        "source": "https://www.zhongyuan.gov.cn/zyyw/10118551.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 16. 王义民 — 前任区委领导（主席台就座）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 3002,
        "name": "王义民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（前任中原区领导）",
        "current_org": "",
        "source": "https://www.zhongyuan.gov.cn/zyyw/10118551.jhtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 17. 李献民 — 前任区委领导（主席台就座）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 3003,
        "name": "李献民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（前任中原区领导）",
        "current_org": "",
        "source": "https://www.zhongyuan.gov.cn/zyyw/10118551.jhtml",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共郑州市中原区委员会", "type": "党委", "level": "县处级", "parent": "中共郑州市委", "location": "郑州市中原区"},
    {"id": 2, "name": "中原区人民政府", "type": "政府", "level": "县处级", "parent": "郑州市人民政府", "location": "郑州市中原区"},
    {"id": 3, "name": "中原区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共郑州市中原区委员会", "location": "郑州市中原区"},
    {"id": 4, "name": "中原区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "郑州市中原区"},
    {"id": 5, "name": "中原区政协", "type": "政协", "level": "县处级", "parent": "", "location": "郑州市中原区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 李晓雷
    {"person_id": 1001, "org_id": 1, "title": "中原区委书记", "start_date": "", "end_date": "", "rank": "正县处级", "note": "主持区委全面工作"},
    # 邓英文
    {"person_id": 1002, "org_id": 1, "title": "中原区委副书记", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    {"person_id": 1002, "org_id": 2, "title": "中原区区长、党组书记", "start_date": "", "end_date": "", "rank": "正县处级", "note": "主持区政府全面工作"},
    # 马素华
    {"person_id": 1003, "org_id": 1, "title": "中原区委副书记（推定）", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 房玉雯
    {"person_id": 1004, "org_id": 1, "title": "中原区委常委", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 冯乐
    {"person_id": 1005, "org_id": 1, "title": "中原区委常委", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 周伟杰
    {"person_id": 1006, "org_id": 1, "title": "中原区委常委", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    {"person_id": 1006, "org_id": 2, "title": "常务副区长、党组副书记", "start_date": "", "end_date": "", "rank": "副县处级", "note": "负责区政府常务工作"},
    # 武学德
    {"person_id": 1007, "org_id": 1, "title": "中原区委常委", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 郭学远
    {"person_id": 1008, "org_id": 1, "title": "中原区委常委", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 李鑫
    {"person_id": 1009, "org_id": 1, "title": "中原区委常委", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    {"person_id": 1009, "org_id": 2, "title": "副区长、党组成员", "start_date": "", "end_date": "", "rank": "副县处级", "note": "负责应急、安全生产、卫健、文旅等"},
    # 孔健
    {"person_id": 1010, "org_id": 1, "title": "中原区委常委", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 刘超
    {"person_id": 1011, "org_id": 1, "title": "中原区委常委、区委办公室主任", "start_date": "", "end_date": "", "rank": "副县处级", "note": ""},
    # 李智
    {"person_id": 2001, "org_id": 2, "title": "副区长、党组成员", "start_date": "", "end_date": "", "rank": "副县处级", "note": "负责工业、科技、招商、商务等"},
    # 李嵘
    {"person_id": 2002, "org_id": 2, "title": "副区长、党组成员", "start_date": "", "end_date": "", "rank": "副县处级", "note": "负责教育、城建、住房保障等"},
    # 张毅
    {"person_id": 2003, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副县处级", "note": "负责金融领域工作"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 李晓雷 ↔ 邓英文: 党政一把手搭档
    {"person_a": 1001, "person_b": 1002, "type": "overlap", "context": "区委书记与区长党政工作搭档", "overlap_org": "中原区", "overlap_period": ""},
    # 李晓雷 ↔ 马素华: 书记与副书记
    {"person_a": 1001, "person_b": 1003, "type": "overlap", "context": "区委书记与区委副书记工作搭档", "overlap_org": "中共中原区委", "overlap_period": ""},
    # 邓英文 ↔ 马素华: 区长与副书记
    {"person_a": 1002, "person_b": 1003, "type": "overlap", "context": "区长与区委副书记工作搭档", "overlap_org": "中原区", "overlap_period": ""},
    # 李晓雷 ↔ 周伟杰: 书记与常务副区长
    {"person_a": 1001, "person_b": 1006, "type": "overlap", "context": "区委书记与常务副区长工作搭档", "overlap_org": "中共中原区委/区政府", "overlap_period": ""},
    # 邓英文 ↔ 周伟杰: 区长与常务副区长
    {"person_a": 1002, "person_b": 1006, "type": "overlap", "context": "区长与常务副区长工作搭档", "overlap_org": "中原区政府", "overlap_period": ""},
    # 李晓雷 ↔ 李鑫: 书记与区委常委副区长
    {"person_a": 1001, "person_b": 1009, "type": "overlap", "context": "区委书记与区委常委副区长工作搭档", "overlap_org": "中共中原区委/区政府", "overlap_period": ""},
    # 邓英文 ↔ 李鑫: 区长与副区长（陪同调研）
    {"person_a": 1002, "person_b": 1009, "type": "overlap", "context": "区长调研时由李鑫陪同，工作搭档", "overlap_org": "中原区政府", "overlap_period": ""},
    # 李晓雷 ↔ 刘超: 书记与区委办主任
    {"person_a": 1001, "person_b": 1011, "type": "overlap", "context": "区委书记与区委办公室主任工作关系（慰问党员时刘超参加）", "overlap_org": "中共中原区委", "overlap_period": ""},
    # 邓英文 ↔ 李智: 区长与副区长
    {"person_a": 1002, "person_b": 2001, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "中原区政府", "overlap_period": ""},
    # 邓英文 ↔ 李嵘: 区长与副区长
    {"person_a": 1002, "person_b": 2002, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "中原区政府", "overlap_period": ""},
    # 邓英文 ↔ 张毅: 区长与副区长
    {"person_a": 1002, "person_b": 2003, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "中原区政府", "overlap_period": ""},
    # 周伟杰 ↔ 李鑫: 两位副区长
    {"person_a": 1006, "person_b": 1009, "type": "overlap", "context": "常务副区长与副区长工作搭档", "overlap_org": "中原区政府", "overlap_period": ""},
    # 李晓雷 ↔ 薛晓军: 前任领导
    {"person_a": 1001, "person_b": 3001, "type": "predecessor_successor", "context": "薛晓军为前任区领导，在十三次党代会上主席台就座", "overlap_org": "中共中原区委", "overlap_period": ""},
    # 邓英文 ↔ 房玉雯: 区委委员
    {"person_a": 1002, "person_b": 1004, "type": "overlap", "context": "区委副书记与区委常委工作搭档", "overlap_org": "中共中原区委", "overlap_period": ""},
    # 李晓雷 ↔ 冯乐: 书记与常委
    {"person_a": 1001, "person_b": 1005, "type": "overlap", "context": "区委书记与区委常委工作搭档", "overlap_org": "中共中原区委", "overlap_period": ""},
    # 李晓雷 ↔ 武学德: 书记与常委
    {"person_a": 1001, "person_b": 1007, "type": "overlap", "context": "区委书记与区委常委工作搭档", "overlap_org": "中共中原区委", "overlap_period": ""},
    # 李晓雷 ↔ 郭学远: 书记与常委
    {"person_a": 1001, "person_b": 1008, "type": "overlap", "context": "区委书记与区委常委工作搭档", "overlap_org": "中共中原区委", "overlap_period": ""},
    # 李晓雷 ↔ 孔健: 书记与常委
    {"person_a": 1001, "person_b": 1010, "type": "overlap", "context": "区委书记与区委常委工作搭档", "overlap_org": "中共中原区委", "overlap_period": ""},
]


# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON helpers
# ═══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "中原区政府网站-领导信息-邓英文", "url": "https://public.zhongyuan.gov.cn/D13X/1698860.jhtml", "publisher": "中原区人民政府", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "邓英文官方简历"},
        {"id": "S002", "title": "中原区政府网站-领导信息-周伟杰", "url": "https://public.zhongyuan.gov.cn/D13X/6064529.jhtml", "publisher": "中原区人民政府", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "周伟杰官方简历"},
        {"id": "S003", "title": "中原区政府网站-领导信息-李鑫", "url": "https://public.zhongyuan.gov.cn/D13X/9214991.jhtml", "publisher": "中原区人民政府", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "李鑫官方简历"},
        {"id": "S004", "title": "中原区政府网站-领导信息-李智", "url": "https://public.zhongyuan.gov.cn/D13X/10136093.jhtml", "publisher": "中原区人民政府", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "李智官方简历"},
        {"id": "S005", "title": "中原区政府网站-领导信息-李嵘", "url": "https://public.zhongyuan.gov.cn/D13X/9972102.jhtml", "publisher": "中原区人民政府", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "李嵘官方简历"},
        {"id": "S006", "title": "中原区政府网站-领导信息-张毅", "url": "https://public.zhongyuan.gov.cn/D13X/9947609.jhtml", "publisher": "中原区人民政府", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "张毅官方简历"},
        {"id": "S007", "title": "中原区第十三次党代会开幕报道", "url": "https://www.zhongyuan.gov.cn/zyyw/10118551.jhtml", "publisher": "中原区人民政府", "published_at": "2026-06-23", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "确认区委常委会组成人员名单"},
        {"id": "S008", "title": "中原区第十三次党代会闭幕报道", "url": "https://www.zhongyuan.gov.cn/zyyw/10122885.jhtml", "publisher": "中原区人民政府", "published_at": "2026-06-25", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "选举产生新一届区委"},
        {"id": "S009", "title": "李晓雷调研安全生产报道", "url": "https://www.zhongyuan.gov.cn/zyyw/10153657.jhtml", "publisher": "中原区人民政府", "published_at": "2026-07-14", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "确认李晓雷为区委书记"},
        {"id": "S010", "title": "邓英文调研安全生产报道", "url": "https://www.zhongyuan.gov.cn/zyyw/10155693.jhtml", "publisher": "中原区人民政府", "published_at": "2026-07-14", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "确认邓英文为区长、李鑫陪同"},
        {"id": "S011", "title": "李晓雷慰问老党员报道", "url": "https://www.zhongyuan.gov.cn/zyyw/10128972.jhtml", "publisher": "中原区人民政府", "published_at": "2026-06-30", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "确认刘超为区委常委、区委办主任"},
    ]


def make_person_json(person, timeline, rels, source_register):
    """Create a person graph JSON following the person_graph_json.md schema."""
    today_short = TODAY.replace("-", "")
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "郑州市",
            "region": "中原区",
            "job": person["current_post"],
            "task_id": "henan_中原区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"zhongyuanqu_{person['name']}",
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
            "administrative_rank": "正县处级" if person["id"] == 1001 or person["id"] == 1002 else "副县处级",
            "as_of": TODAY,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S007", "S008"]
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
        "risk_and_integrity_signals": [],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "详细履历（早期职业经历、教育背景、政治面貌时间等）尚未获取"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（早期职业经历、教育背景、入党时间、历任职务及起止时间）",
                "why_it_matters": "核心领导的履历是关系网络分析的基础",
                "suggested_queries": [f"{person['name']} 简历 中原区"],
                "last_attempted": TODAY
            }
        ]
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  郑州市中原区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-24（首次调查）")
    print("  信息来源: 中原区政府网站 + 第十三次党代会报道")
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
    print(f"\n✅ 中原区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 李晓雷 (区委书记)
    li_timeline = [
        {"start": "", "end": "", "org": "中共郑州市中原区委员会", "title": "中原区委书记", "notes": "主持区委全面工作；2026年6月23日第十三次党代会作工作报告并连任", "confidence": "confirmed", "source_ids": ["S007", "S009"]},
    ]
    li_relationships = [
        {"person": "邓英文", "person_id": "zhongyuanqu_邓英文", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记与区长党政工作搭档，共同主持第十三次党代会", "overlap_org": "中原区", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007"]},
        {"person": "马素华", "person_id": "zhongyuanqu_马素华", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记与区委副书记工作搭档", "overlap_org": "中共中原区委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007"]},
        {"person": "周伟杰", "person_id": "zhongyuanqu_周伟杰", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记与常务副区长工作搭档", "overlap_org": "中共中原区委/区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007"]},
        {"person": "李鑫", "person_id": "zhongyuanqu_李鑫", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记与区委常委副区长工作搭档", "overlap_org": "中共中原区委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007"]},
        {"person": "刘超", "person_id": "zhongyuanqu_刘超", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记与区委办公室主任工作关系，陪同慰问党员", "overlap_org": "中共中原区委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S011"]},
    ]
    li_json = make_person_json(persons[0], li_timeline, li_relationships, source_register)
    li_path = STAGING / f"{TODAY}-河南省-郑州市-区委书记-李晓雷.json"
    with open(li_path, "w", encoding="utf-8") as f:
        json.dump(li_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {li_path.name}")

    # 2. 邓英文 (区长)
    deng_timeline = [
        {"start": "", "end": "", "org": "中原区人民政府", "title": "中原区区长、党组书记", "notes": "主持区政府全面工作；同时任区委副书记", "confidence": "confirmed", "source_ids": ["S001", "S007", "S010"]},
    ]
    deng_relationships = [
        {"person": "李晓雷", "person_id": "zhongyuanqu_李晓雷", "relationship_type": "overlap", "strength": "strong", "evidence": "区长与区委书记党政工作搭档", "overlap_org": "中原区", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007"]},
        {"person": "周伟杰", "person_id": "zhongyuanqu_周伟杰", "relationship_type": "overlap", "strength": "strong", "evidence": "区长与常务副区长工作搭档", "overlap_org": "中原区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "李鑫", "person_id": "zhongyuanqu_李鑫", "relationship_type": "overlap", "strength": "strong", "evidence": "区长调研安全生产时由区委常委、副区长李鑫陪同", "overlap_org": "中原区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S010"]},
    ]
    deng_json = make_person_json(persons[1], deng_timeline, deng_relationships, source_register)
    deng_path = STAGING / f"{TODAY}-河南省-郑州市-区长-邓英文.json"
    with open(deng_path, "w", encoding="utf-8") as f:
        json.dump(deng_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {deng_path.name}")

    # 3. 周伟杰 (常务副区长)
    zhou_timeline = [
        {"start": "", "end": "", "org": "中原区人民政府", "title": "常务副区长、党组副书记", "notes": "区委常委；负责区政府常务工作、经济运行、发展改革、统计、财税金融等", "confidence": "confirmed", "source_ids": ["S002", "S007"]},
    ]
    zhou_relationships = [
        {"person": "李晓雷", "person_id": "zhongyuanqu_李晓雷", "relationship_type": "overlap", "strength": "strong", "evidence": "常务副区长与区委书记工作关系", "overlap_org": "中共中原区委/区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007"]},
        {"person": "邓英文", "person_id": "zhongyuanqu_邓英文", "relationship_type": "overlap", "strength": "strong", "evidence": "区长与常务副区长工作搭档", "overlap_org": "中原区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    zhou_json = make_person_json(persons[5], zhou_timeline, zhou_relationships, source_register)
    zhou_path = STAGING / f"{TODAY}-河南省-郑州市-常务副区长-周伟杰.json"
    with open(zhou_path, "w", encoding="utf-8") as f:
        json.dump(zhou_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zhou_path.name}")

    # 4. 李鑫 (区委常委、副区长)
    li_xin_timeline = [
        {"start": "", "end": "", "org": "中原区人民政府", "title": "副区长、党组成员", "notes": "区委常委；负责应急管理、安全生产、消防救援、卫健、文旅等", "confidence": "confirmed", "source_ids": ["S003", "S010"]},
    ]
    li_xin_relationships = [
        {"person": "李晓雷", "person_id": "zhongyuanqu_李晓雷", "relationship_type": "overlap", "strength": "strong", "evidence": "区委常委与区委书记工作关系", "overlap_org": "中共中原区委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007"]},
        {"person": "邓英文", "person_id": "zhongyuanqu_邓英文", "relationship_type": "overlap", "strength": "strong", "evidence": "陪同区长调研安全生产", "overlap_org": "中原区政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S010"]},
    ]
    li_xin_json = make_person_json(persons[8], li_xin_timeline, li_xin_relationships, source_register)
    li_xin_path = STAGING / f"{TODAY}-河南省-郑州市-副区长-李鑫.json"
    with open(li_xin_path, "w", encoding="utf-8") as f:
        json.dump(li_xin_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {li_xin_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {STAGING}")


if __name__ == "__main__":
    main()
