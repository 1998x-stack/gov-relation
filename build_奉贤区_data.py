#!/usr/bin/env python3
"""奉贤区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区(直辖市)
调查日期: 2026-07-25
信息来源:
  - 上海市奉贤区人民政府网站 (www.fengxian.gov.cn) 政务要闻
  - 奉贤区融媒体中心官方报道

Confirmed current leaders (2026年7月):
  - 区委书记: 刘平 (confirmed from government news, 2026-07-22)
  - 区委副书记、区长: 王益群 (confirmed from government news, 2026-07-21)
  - 其他区委常委: 依据公开报道
  - 前任区委书记: 袁泉 (截至2025年9月)

Open questions (see open_questions in person JSONs):
  - 刘平的完整履历 (前任职位、教育背景、出生年月)
  - 王益群的完整履历 (前任职位、教育背景、出生年月)
  - 部分非常委副区长的详细分工
  - 区人大、政协全部领导班子
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Find project root: walk up looking for gov_relation/
PROJECT_ROOT = HERE
for _ in range(10):
    if (PROJECT_ROOT / "gov_relation").is_dir():
        break
    PROJECT_ROOT = PROJECT_ROOT.parent
else:
    PROJECT_ROOT = HERE.parents[2]  # fallback

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "奉贤区"
TODAY = "2026-07-25"

STAGING = HERE
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# Canonical destinations (always relative to project root)
CANONICAL_DB = PROJECT_ROOT / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = PROJECT_ROOT / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = PROJECT_ROOT / "scripts" / "build" / f"build_{SLUG}_data.py"
CANONICAL_ROOT_BUILD = PROJECT_ROOT / f"build_{SLUG}_data.py"

# ── Persons ──────────────────────────────────────────────────────────────────
# ID ranges: 1xxx = party committee, 2xxx = government, 3xxx = congress,
#            4xxx = cppcc, 5xxx = judiciary, 6xxx = predecessor

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 区委领导班子
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 刘平 — 区委书记
    {
        "id": 1001,
        "name": "刘平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区委书记",
        "current_org": "中共上海市奉贤区委员会",
        "source": "https://www.fengxian.gov.cn/zwyw/20260723/110440.html",
    },
    # 2. 王益群 — 区委副书记、区长
    {
        "id": 1002,
        "name": "王益群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区委副书记、区长",
        "current_org": "上海市奉贤区人民政府",
        "source": "https://www.fengxian.gov.cn/zwyw/20260721/110348.html",
    },
    # 3. 唐晓腾 — 区委副书记
    {
        "id": 1003,
        "name": "唐晓腾",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区委副书记",
        "current_org": "中共上海市奉贤区委员会",
        "source": "https://www.fengxian.gov.cn/zwyw/20260722/110384.html",
    },
    # 4. 陈学哲 — 区委常委
    {
        "id": 1004,
        "name": "陈学哲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区委常委",
        "current_org": "中共上海市奉贤区委员会",
        "source": "https://www.fengxian.gov.cn/zwyw/20260317/104315.html",
    },
    # 5. 王洪青 — 区委常委
    {
        "id": 1005,
        "name": "王洪青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区委常委",
        "current_org": "中共上海市奉贤区委员会",
        "source": "https://www.fengxian.gov.cn/zwyw/20260317/104315.html",
    },
    # 6. 俞林伟 — 区委常委
    {
        "id": 1006,
        "name": "俞林伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区委常委",
        "current_org": "中共上海市奉贤区委员会",
        "source": "https://www.fengxian.gov.cn/zwyw/20260317/104315.html",
    },
    # 7. 刘伟 — 区委常委、副区长
    {
        "id": 1007,
        "name": "刘伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区委常委、副区长",
        "current_org": "上海市奉贤区人民政府",
        "source": "https://www.fengxian.gov.cn/zwyw/20260719/110269.html",
    },
    # 8. 胡煜昂 — 区委常委、组织部部长、党校校长
    {
        "id": 1008,
        "name": "胡煜昂",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区委常委、组织部部长，区委党校校长",
        "current_org": "中共上海市奉贤区委组织部",
        "source": "https://www.fengxian.gov.cn/zwyw/20260529/107795.html",
    },
    # 9. 李锐 — 区委常委、统战部部长
    {
        "id": 1009,
        "name": "李锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区委常委、统战部部长",
        "current_org": "中共上海市奉贤区委统战部",
        "source": "https://www.fengxian.gov.cn/zwyw/20260719/110269.html",
    },
    # 10. 吕将 — 区委常委
    {
        "id": 1010,
        "name": "吕将",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区委常委",
        "current_org": "中共上海市奉贤区委员会",
        "source": "https://www.fengxian.gov.cn/zwyw/20260317/104315.html",
    },
    # 11. 胡伟龙 — 区委常委
    {
        "id": 1011,
        "name": "胡伟龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区委常委",
        "current_org": "中共上海市奉贤区委员会",
        "source": "https://www.fengxian.gov.cn/zwyw/20260317/104315.html",
    },

    # ═══════════════════════════════════════════════════════════════════════
    # 区政府领导班子（非常委副区长）
    # ═══════════════════════════════════════════════════════════════════════
    # 12. 陈钺 — 副区长
    {
        "id": 2001,
        "name": "陈钺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区人民政府副区长",
        "current_org": "上海市奉贤区人民政府",
        "source": "https://www.fengxian.gov.cn/zwyw/20260717/110127.html",
    },
    # 13. 王淳 — 副区长
    {
        "id": 2002,
        "name": "王淳",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "奉贤区人民政府副区长",
        "current_org": "上海市奉贤区人民政府",
        "source": "https://www.fengxian.gov.cn/zwyw/20260701/109327.html",
    },
    # 14. 李嘉宁 — 副区长
    {
        "id": 2003,
        "name": "李嘉宁",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "奉贤区人民政府副区长",
        "current_org": "上海市奉贤区人民政府",
        "source": "https://www.fengxian.gov.cn/zwyw/20260717/110127.html",
    },
    # 15. 李慧 — 副区长
    {
        "id": 2004,
        "name": "李慧",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "奉贤区人民政府副区长",
        "current_org": "上海市奉贤区人民政府",
        "source": "https://www.fengxian.gov.cn/zwyw/20260717/110127.html",
    },
    # 16. 唐雄威 — 副区长
    {
        "id": 2005,
        "name": "唐雄威",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "奉贤区人民政府副区长",
        "current_org": "上海市奉贤区人民政府",
        "source": "https://www.fengxian.gov.cn/zwyw/20260717/110127.html",
    },
    # 17. 卓雅 — 副区长
    {
        "id": 2006,
        "name": "卓雅",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "奉贤区人民政府副区长",
        "current_org": "上海市奉贤区人民政府",
        "source": "https://www.fengxian.gov.cn/zwyw/20260717/110127.html",
    },
    # 18. 陆建新 — 原副区长/区领导
    {
        "id": 2007,
        "name": "陆建新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区人民政府副区长",
        "current_org": "上海市奉贤区人民政府",
        "source": "https://www.fengxian.gov.cn/zwyw/20260723/110435.html",
    },

    # ═══════════════════════════════════════════════════════════════════════
    # 区人大领导班子
    # ═══════════════════════════════════════════════════════════════════════
    # 19. 张权权 — 人大常委会党组书记
    {
        "id": 3001,
        "name": "张权权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区人大常委会党组书记",
        "current_org": "上海市奉贤区人大常委会",
        "source": "https://www.fengxian.gov.cn/zwyw/20260723/110435.html",
    },
    # 20. 张培荣 — 原人大常委会主任
    {
        "id": 3002,
        "name": "张培荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.fengxian.gov.cn/zwyw/20260317/104315.html",
    },

    # ═══════════════════════════════════════════════════════════════════════
    # 区政协领导班子
    # ═══════════════════════════════════════════════════════════════════════
    # 21. 陈勇章 — 政协主席
    {
        "id": 4001,
        "name": "陈勇章",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区政协主席、党组书记",
        "current_org": "政协上海市奉贤区委员会",
        "source": "https://www.fengxian.gov.cn/zwyw/20260317/104315.html",
    },

    # ═══════════════════════════════════════════════════════════════════════
    # 区法院、检察院
    # ═══════════════════════════════════════════════════════════════════════
    # 22. 韩峰 — 法院院长
    {
        "id": 5001,
        "name": "韩峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区人民法院院长、党组书记",
        "current_org": "上海市奉贤区人民法院",
        "source": "https://www.fengxian.gov.cn/zwyw/20260714/9dc2055ace454ebda001b9ff413ecde4.html",
    },
    # 23. 韩孔林 — 检察院领导
    {
        "id": 5002,
        "name": "韩孔林",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "奉贤区人民检察院领导",
        "current_org": "上海市奉贤区人民检察院",
        "source": "https://www.fengxian.gov.cn/zwyw/20260723/110435.html",
    },

    # ═══════════════════════════════════════════════════════════════════════
    # 前任领导
    # ═══════════════════════════════════════════════════════════════════════
    # 24. 袁泉 — 前任区委书记
    {
        "id": 6001,
        "name": "袁泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.fengxian.gov.cn/zwyw/20250921/96025.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共上海市奉贤区委员会", "type": "党委", "level": "市辖区"},
    {"id": 2, "name": "上海市奉贤区人民政府", "type": "政府", "level": "市辖区"},
    {"id": 3, "name": "上海市奉贤区人大常委会", "type": "人大", "level": "市辖区"},
    {"id": 4, "name": "政协上海市奉贤区委员会", "type": "政协", "level": "市辖区"},
    {"id": 5, "name": "上海市奉贤区人民法院", "type": "其他", "level": "市辖区"},
    {"id": 6, "name": "上海市奉贤区人民检察院", "type": "其他", "level": "市辖区"},
    {"id": 7, "name": "中共上海市奉贤区委组织部", "type": "党委", "level": "市辖区"},
    {"id": 8, "name": "中共上海市奉贤区委统战部", "type": "党委", "level": "市辖区"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 刘平 — 区委书记
    {"person_id": 1001, "org_id": 1, "title": "奉贤区委书记", "start": "2025-2026", "end": "present", "rank": "", "note": "区委全面工作"},
    {"person_id": 1001, "org_id": 1, "title": "奉贤区委书记", "start": "2026-03", "end": "present", "rank": "", "note": "最早见于2026年3月17日新闻报道"},

    # 王益群 — 区长
    {"person_id": 1002, "org_id": 2, "title": "奉贤区委副书记、区长", "start": "", "end": "present", "rank": "", "note": "区政府全面工作"},
    {"person_id": 1002, "org_id": 2, "title": "奉贤区区长", "start": "2025-09", "end": "present", "rank": "", "note": "最早见于2025年9月新闻报道"},

    # 唐晓腾 — 区委副书记
    {"person_id": 1003, "org_id": 1, "title": "奉贤区委副书记", "start": "", "end": "present", "rank": "", "note": ""},

    # 陈学哲 — 区委常委
    {"person_id": 1004, "org_id": 1, "title": "奉贤区委常委", "start": "", "end": "present", "rank": "", "note": ""},

    # 王洪青 — 区委常委
    {"person_id": 1005, "org_id": 1, "title": "奉贤区委常委", "start": "", "end": "present", "rank": "", "note": ""},

    # 俞林伟 — 区委常委
    {"person_id": 1006, "org_id": 1, "title": "奉贤区委常委", "start": "", "end": "present", "rank": "", "note": ""},

    # 刘伟 — 常委副区长
    {"person_id": 1007, "org_id": 2, "title": "奉贤区委常委、副区长", "start": "", "end": "present", "rank": "", "note": ""},

    # 胡煜昂 — 组织部长
    {"person_id": 1008, "org_id": 7, "title": "奉贤区委常委、组织部部长、区委党校校长", "start": "", "end": "present", "rank": "", "note": ""},

    # 李锐 — 统战部长
    {"person_id": 1009, "org_id": 8, "title": "奉贤区委常委、统战部部长", "start": "", "end": "present", "rank": "", "note": ""},

    # 吕将 — 区委常委
    {"person_id": 1010, "org_id": 1, "title": "奉贤区委常委", "start": "", "end": "present", "rank": "", "note": ""},

    # 胡伟龙 — 区委常委
    {"person_id": 1011, "org_id": 1, "title": "奉贤区委常委", "start": "", "end": "present", "rank": "", "note": ""},

    # 陈钺 — 副区长
    {"person_id": 2001, "org_id": 2, "title": "奉贤区副区长", "start": "", "end": "present", "rank": "", "note": ""},

    # 王淳 — 副区长
    {"person_id": 2002, "org_id": 2, "title": "奉贤区副区长", "start": "", "end": "present", "rank": "", "note": ""},

    # 李嘉宁 — 副区长
    {"person_id": 2003, "org_id": 2, "title": "奉贤区副区长", "start": "", "end": "present", "rank": "", "note": ""},

    # 李慧 — 副区长
    {"person_id": 2004, "org_id": 2, "title": "奉贤区副区长", "start": "", "end": "present", "rank": "", "note": ""},

    # 唐雄威 — 副区长
    {"person_id": 2005, "org_id": 2, "title": "奉贤区副区长", "start": "", "end": "present", "rank": "", "note": ""},

    # 卓雅 — 副区长
    {"person_id": 2006, "org_id": 2, "title": "奉贤区副区长", "start": "", "end": "present", "rank": "", "note": ""},

    # 陆建新 — 副区长
    {"person_id": 2007, "org_id": 2, "title": "奉贤区副区长", "start": "", "end": "present", "rank": "", "note": ""},

    # 张权权 — 人大党组书记
    {"person_id": 3001, "org_id": 3, "title": "奉贤区人大常委会党组书记", "start": "2026", "end": "present", "rank": "", "note": "2026年7月报道"}, # 待补选

    # 张培荣 — 原人大主任
    {"person_id": 3002, "org_id": 3, "title": "奉贤区人大常委会主任、党组书记", "start": "", "end": "2026", "rank": "", "note": "截至2026年3月仍在任"},

    # 陈勇章 — 政协主席
    {"person_id": 4001, "org_id": 4, "title": "奉贤区政协主席、党组书记", "start": "", "end": "present", "rank": "", "note": ""},

    # 韩峰 — 法院院长
    {"person_id": 5001, "org_id": 5, "title": "奉贤区人民法院院长、党组书记", "start": "", "end": "present", "rank": "", "note": ""},

    # 韩孔林 — 检察院领导
    {"person_id": 5002, "org_id": 6, "title": "奉贤区人民检察院领导", "start": "", "end": "present", "rank": "", "note": ""},

    # 前任领导
    {"person_id": 6001, "org_id": 1, "title": "奉贤区委书记", "start": "", "end": "2025-2026", "rank": "", "note": "袁泉，刘平前任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 班子成员关系 — 同一届区委常委会
    {"person_a": 1001, "person_b": 1002, "type": "overlap", "strength": "strong",
     "context": "区委书记与区长搭档", "overlap_org": "中共上海市奉贤区委员会", "overlap_period": "2025/2026-至今"},
    {"person_a": 1001, "person_b": 1003, "type": "overlap", "strength": "strong",
     "context": "区委书记与区委副书记在同一常委会", "overlap_org": "中共上海市奉贤区委员会", "overlap_period": "至今"},
    {"person_a": 1002, "person_b": 1003, "type": "overlap", "strength": "strong",
     "context": "区长与区委副书记在同一常委会", "overlap_org": "中共上海市奉贤区委员会", "overlap_period": "至今"},
    {"person_a": 1001, "person_b": 1007, "type": "overlap", "strength": "strong",
     "context": "区委书记与常委副区长在区委常委会共事", "overlap_org": "中共上海市奉贤区委员会", "overlap_period": "至今"},
    {"person_a": 1001, "person_b": 1008, "type": "overlap", "strength": "strong",
     "context": "区委书记与组织部长在区委常委会共事", "overlap_org": "中共上海市奉贤区委员会", "overlap_period": "至今"},
    {"person_a": 1001, "person_b": 1009, "type": "overlap", "strength": "strong",
     "context": "区委书记与统战部长在区委常委会共事", "overlap_org": "中共上海市奉贤区委员会", "overlap_period": "至今"},
    {"person_a": 1001, "person_b": 1004, "type": "overlap", "strength": "strong",
     "context": "区委书记与区委常委在同一常委会", "overlap_org": "中共上海市奉贤区委员会", "overlap_period": "至今"},
    {"person_a": 1001, "person_b": 1005, "type": "overlap", "strength": "strong",
     "context": "区委书记与区委常委在同一常委会", "overlap_org": "中共上海市奉贤区委员会", "overlap_period": "至今"},
    {"person_a": 1001, "person_b": 1006, "type": "overlap", "strength": "strong",
     "context": "区委书记与区委常委在同一常委会", "overlap_org": "中共上海市奉贤区委员会", "overlap_period": "至今"},
    {"person_a": 1001, "person_b": 1010, "type": "overlap", "strength": "strong",
     "context": "区委书记与区委常委在同一常委会", "overlap_org": "中共上海市奉贤区委员会", "overlap_period": "至今"},
    {"person_a": 1001, "person_b": 1011, "type": "overlap", "strength": "strong",
     "context": "区委书记与区委常委在同一常委会", "overlap_org": "中共上海市奉贤区委员会", "overlap_period": "至今"},

    # 前任关系
    {"person_a": 6001, "person_b": 1001, "type": "predecessor_successor", "strength": "strong",
     "context": "袁泉为前任奉贤区委书记，刘平接任", "overlap_org": "中共上海市奉贤区委员会", "overlap_period": "2025-2026"},

    # 区政府班子成员关系
    {"person_a": 1002, "person_b": 2001, "type": "overlap", "strength": "strong",
     "context": "区长与副区长在同一政府共事", "overlap_org": "上海市奉贤区人民政府", "overlap_period": "至今"},
    {"person_a": 1002, "person_b": 2002, "type": "overlap", "strength": "strong",
     "context": "区长与副区长在同一政府共事", "overlap_org": "上海市奉贤区人民政府", "overlap_period": "至今"},
    {"person_a": 1002, "person_b": 2003, "type": "overlap", "strength": "strong",
     "context": "区长与副区长在同一政府共事", "overlap_org": "上海市奉贤区人民政府", "overlap_period": "至今"},
    {"person_a": 1002, "person_b": 2004, "type": "overlap", "strength": "strong",
     "context": "区长与副区长在同一政府共事", "overlap_org": "上海市奉贤区人民政府", "overlap_period": "至今"},
    {"person_a": 1002, "person_b": 2005, "type": "overlap", "strength": "strong",
     "context": "区长与副区长在同一政府共事", "overlap_org": "上海市奉贤区人民政府", "overlap_period": "至今"},
    {"person_a": 1002, "person_b": 2006, "type": "overlap", "strength": "strong",
     "context": "区长与副区长在同一政府共事", "overlap_org": "上海市奉贤区人民政府", "overlap_period": "至今"},
    {"person_a": 1002, "person_b": 2007, "type": "overlap", "strength": "strong",
     "context": "区长与副区长在同一政府共事", "overlap_org": "上海市奉贤区人民政府", "overlap_period": "至今"},
]

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"=== 奉贤区领导班子工作关系网络 ===")
    print(f"调查日期: {TODAY}")
    print(f"人员: {len(persons)}")
    print(f"机构: {len(organizations)}")
    print(f"任职: {len(positions)}")
    print(f"关系: {len(relationships)}")
    print()

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\n数据库: {DB_PATH}")
    print(f"图谱:   {GEXF_PATH}")

    # Copy to canonical locations if running from staging
    import shutil
    if STAGING != HERE.parents[2]:
        for src, dst in [
            (DB_PATH, CANONICAL_DB),
            (GEXF_PATH, CANONICAL_GEXF),
            (HERE / f"build_{SLUG}_data.py", CANONICAL_BUILD),
            (HERE / f"build_{SLUG}_data.py", CANONICAL_ROOT_BUILD),
        ]:
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                print(f"已复制: {src} -> {dst}")
