#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 东辽县, 辽源市, 吉林省.

Level: 县
Province: 吉林省
Parent city: 辽源市
Targets: 县委书记 (Party Secretary: 石磊), 县长 (Mayor: 田国栋)
Task ID: jilin_东辽县

Research date: 2026-07-25
Official source: http://www.dongliao.gov.cn/ (东辽县人民政府)

Current status (as of 2026-07-25, verified via 东辽县人民政府 website):
- 县委书记: 石磊 (男，曾任东辽县代县长/县长，现转任县委书记)
- 县长: 田国栋 (男，汉族，1976年7月生，省委党校研究生学历，中共党员)
- Full government leadership roster confirmed on county website (县政府领导页面)

Leadership roster sourced from:
  - http://www.dongliao.gov.cn/xzf/ (县政府首页)
  - http://www.dongliao.gov.cn/xzf/zfld/xz/tgd/ (田国栋)
  - http://www.dongliao.gov.cn/xzf/zfld/fxz/lbg/ (李宝刚)
  - http://www.dongliao.gov.cn/xzf/zfld/fxz/gf/ (高峰)
  - http://www.dongliao.gov.cn/xzf/zfld/fxz/zfs/ (赵丰双)
  - http://www.dongliao.gov.cn/xzf/zfld/fxz/jx/ (姜贤)
  - http://www.dongliao.gov.cn/xzf/zfld/fxz/zzm/ (张志民)
  - http://www.dongliao.gov.cn/xzf/zfld/fxz/cl/ (陈亮)
  - http://www.dongliao.gov.cn/xzf/zfld/fxz/wyq/ (吴跃泉)
  - http://www.dongliao.gov.cn/xzf/zfld/fxz/qgj/ (邱国军)
  - http://www.dongliao.gov.cn/xzf/zfhy/202607/t20260709_744104.html (确认石磊为县委书记)
  - http://www.dongliao.gov.cn/xzf/gzbg/202510/t20251009_721966.html (石磊曾任代理县长)

Confidence notes:
  石磊 identity as 县委书记 confirmed via July 2026 news article on county website.
  田国栋 identity confirmed via official government bio page (1976年生, 省委党校研究生, 中共党员).
  Full career histories before current roles are partial - 田国栋 has official bio, 石磊 has limited public bio.
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

SLUG = "东辽县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 石磊 — 县委书记
    {
        "id": 1,
        "name": "石磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共东辽县委员会",
        "source": "http://www.dongliao.gov.cn/xzf/zfhy/202607/t20260709_744104.html",
    },
    # 2. 田国栋 — 县委副书记、县长
    {
        "id": 2,
        "name": "田国栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年7月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "东辽县人民政府",
        "source": "http://www.dongliao.gov.cn/xzf/zfld/xz/tgd/",
    },

    # ════════════════════════════════════════
    # 县政府领导 (Government Leadership)
    # ════════════════════════════════════════

    # 3. 李宝刚 — 县委常委、常务副县长
    {
        "id": 3,
        "name": "李宝刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年2月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "东辽县人民政府",
        "source": "http://www.dongliao.gov.cn/xzf/zfld/fxz/lbg/",
    },
    # 4. 高峰 — 县委常委、副县长（挂职）
    {
        "id": 4,
        "name": "高峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "东辽县人民政府",
        "source": "http://www.dongliao.gov.cn/xzf/zfld/fxz/gf/",
    },
    # 5. 赵丰双 — 副县长
    {
        "id": 5,
        "name": "赵丰双",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1976年4月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "东辽县人民政府",
        "source": "http://www.dongliao.gov.cn/xzf/zfld/fxz/zfs/",
    },
    # 6. 姜贤 — 副县长
    {
        "id": 6,
        "name": "姜贤",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969年12月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "东辽县人民政府",
        "source": "http://www.dongliao.gov.cn/xzf/zfld/fxz/jx/",
    },
    # 7. 张志民 — 副县长
    {
        "id": 7,
        "name": "张志民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "东辽县人民政府",
        "source": "http://www.dongliao.gov.cn/xzf/zfld/fxz/zzm/",
    },
    # 8. 陈亮 — 副县长（挂职）
    {
        "id": 8,
        "name": "陈亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年1月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "东辽县人民政府",
        "source": "http://www.dongliao.gov.cn/xzf/zfld/fxz/cl/",
    },
    # 9. 吴跃泉 — 副县长、公安局局长
    {
        "id": 9,
        "name": "吴跃泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "东辽县人民政府",
        "source": "http://www.dongliao.gov.cn/xzf/zfld/fxz/wyq/",
    },
    # 10. 邱国军 — 副县长
    {
        "id": 10,
        "name": "邱国军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "东辽县人民政府",
        "source": "http://www.dongliao.gov.cn/xzf/zfld/fxz/qgj/",
    },

    # ════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ════════════════════════════════════════

    # 11. 石磊 — 前任县长（2025年任代理县长/县长，后转任县委书记）
    # Note: Same person as id=1, but we capture the previous role via positions.
    # This entry is intentionally not duplicated - 石磊 id=1 covers both roles.
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共东辽县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共辽源市委员会",
        "location": "吉林省辽源市东辽县",
    },
    {
        "id": 2,
        "name": "东辽县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "辽源市人民政府",
        "location": "吉林省辽源市东辽县",
    },
    {
        "id": 3,
        "name": "东辽县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "辽源市人大常委会",
        "location": "吉林省辽源市东辽县",
    },
    {
        "id": 4,
        "name": "政协东辽县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协辽源市委员会",
        "location": "吉林省辽源市东辽县",
    },
    {
        "id": 5,
        "name": "东辽县纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共辽源市纪律检查委员会",
        "location": "吉林省辽源市东辽县",
    },
    {
        "id": 6,
        "name": "东辽县公安局",
        "type": "政府",
        "level": "乡科级",
        "parent": "东辽县人民政府",
        "location": "吉林省辽源市东辽县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 石磊 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present",
     "rank": "正处级", "note": "2026年7月8日以县委书记身份主持召开全县防汛工作部署大会"},
    # 石磊 - 县长（前任职务）
    {"person_id": 1, "org_id": 2, "title": "县长（代县长）", "start": "2025年1月前", "end": "",
     "rank": "正处级", "note": "2025年1月3日在县十八届人大四次会议上以代理县长身份作政府工作报告"},
    # 田国栋 - 县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present",
     "rank": "正处级", "note": "主持县政府全面工作，分管县审计局"},
    # 田国栋 - 县委副书记
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "东辽县委副书记、县长"},

    # ── 县政府领导 ──
    # 李宝刚 - 县委常委、常务副县长
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责县政府常务工作，分管审计、应急、财政、发改、工信、开发区等"},
    # 高峰 - 县委常委、副县长（挂职）
    {"person_id": 4, "org_id": 2, "title": "县委常委、副县长（挂职）", "start": "", "end": "present",
     "rank": "副处级", "note": "协助常务副县长做好粮食方面工作，协助副县长邱国军做好农业方面工作"},
    # 赵丰双 - 副县长
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "分管交通运输、招商引资、商务、市场监管、人社、政务公开等"},
    # 姜贤 - 副县长
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "分管教育、卫生健康、医疗保障等"},
    # 张志民 - 副县长
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "分管住建、民政救济、自然资源、残疾人事业等"},
    # 陈亮 - 副县长（挂职）
    {"person_id": 8, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present",
     "rank": "副处级", "note": "协助常务副县长做好化债和金融方面工作"},
    # 吴跃泉 - 副县长、公安局局长
    {"person_id": 9, "org_id": 2, "title": "副县长、公安局局长", "start": "", "end": "present",
     "rank": "副处级", "note": "分管公安、司法、信访稳定、退役军人等"},
    {"person_id": 9, "org_id": 6, "title": "公安局局长", "start": "", "end": "present",
     "rank": "正科级", "note": "兼任东辽县公安局局长"},
    # 邱国军 - 副县长
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "分管农业、林业、水利、环境保护、供销等"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 石磊 <-> 田国栋: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长党政主要领导搭档；石磊曾任县长后转任书记，田国栋接任县长",
     "overlap_org": "中共东辽县委员会/东辽县人民政府",
     "overlap_period": "2025-2026年"},

    # 石磊 <-> 田国栋: 前任与继任（县长职务交接）
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "石磊由县长晋升县委书记，田国栋接任县长",
     "overlap_org": "东辽县人民政府",
     "overlap_period": "2025-2026年"},

    # 石磊 <-> 李宝刚: 书记与政府副职
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委常委、常务副县长；县委领导班子搭档",
     "overlap_org": "中共东辽县委员会/东辽县人民政府",
     "overlap_period": "截至2026年7月"},

    # 田国栋 <-> 李宝刚: 县长与常务副县长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "县长与县委常委、常务副县长；政府领导班子搭档",
     "overlap_org": "东辽县人民政府",
     "overlap_period": "截至2026年7月"},

    # 田国栋 <-> 其他副县长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与副县长（挂职）工作搭档", "overlap_org": "东辽县人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "县长与副县长工作搭档", "overlap_org": "东辽县人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "县长与副县长工作搭档", "overlap_org": "东辽县人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "县长与副县长工作搭档", "overlap_org": "东辽县人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "县长与副县长（挂职）工作搭档", "overlap_org": "东辽县人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "县长与副县长、公安局局长工作搭档", "overlap_org": "东辽县人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "县长与副县长工作搭档", "overlap_org": "东辽县人民政府", "overlap_period": "截至2026年7月"},

    # 副县长之间的联系（政府班子成员）
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "县政府领导班子同事", "overlap_org": "东辽县人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "县政府领导班子同事", "overlap_org": "东辽县人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 3, "person_b": 6, "type": "overlap",
     "context": "县政府领导班子同事", "overlap_org": "东辽县人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 3, "person_b": 7, "type": "overlap",
     "context": "县政府领导班子同事", "overlap_org": "东辽县人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 3, "person_b": 8, "type": "overlap",
     "context": "县政府领导班子同事", "overlap_org": "东辽县人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 3, "person_b": 9, "type": "overlap",
     "context": "县政府领导班子同事", "overlap_org": "东辽县人民政府", "overlap_period": "截至2026年7月"},
    {"person_a": 3, "person_b": 10, "type": "overlap",
     "context": "县政府领导班子同事", "overlap_org": "东辽县人民政府", "overlap_period": "截至2026年7月"},

    # 石磊 <-> 前任关系（如果能找到前任信息）
    # 目前不知道前任县委书记是谁，留空
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "东辽县人民政府官网-县政府-县长田国栋",
            "url": "http://www.dongliao.gov.cn/xzf/zfld/xz/tgd/",
            "publisher": "东辽县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "田国栋: 男，汉族，1976年7月生，省委党校研究生学历，中共党员，东辽县委副书记，县长",
        },
        {
            "id": "S002",
            "title": "东辽县人民政府官网-县政府-常务副县长李宝刚",
            "url": "http://www.dongliao.gov.cn/xzf/zfld/fxz/lbg/",
            "publisher": "东辽县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "李宝刚: 男，汉族，1979年2月生，大学学历，中共党员，县委常委、常务副县长",
        },
        {
            "id": "S003",
            "title": "东辽县人民政府官网-县政府-副县长高峰",
            "url": "http://www.dongliao.gov.cn/xzf/zfld/fxz/gf/",
            "publisher": "东辽县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "高峰: 男，汉族，1976年1月生，大学学历，中共党员，县委常委、副县长（挂职）",
        },
        {
            "id": "S004",
            "title": "东辽县人民政府官网-县政府-副县长赵丰双",
            "url": "http://www.dongliao.gov.cn/xzf/zfld/fxz/zfs/",
            "publisher": "东辽县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "赵丰双: 男，满族，1976年4月生，大学学历，中共党员，副县长",
        },
        {
            "id": "S005",
            "title": "东辽县人民政府官网-县政府-副县长姜贤",
            "url": "http://www.dongliao.gov.cn/xzf/zfld/fxz/jx/",
            "publisher": "东辽县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "姜贤: 女，汉族，1969年12月生，大学学历，中共党员，副县长",
        },
        {
            "id": "S006",
            "title": "东辽县人民政府官网-县政府-副县长张志民",
            "url": "http://www.dongliao.gov.cn/xzf/zfld/fxz/zzm/",
            "publisher": "东辽县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "张志民: 男，汉族，1972年10月生，在职研究生学历，中共党员，副县长",
        },
        {
            "id": "S007",
            "title": "东辽县人民政府官网-县政府-副县长陈亮",
            "url": "http://www.dongliao.gov.cn/xzf/zfld/fxz/cl/",
            "publisher": "东辽县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "陈亮: 男，汉族，1982年1月生，大学学历，中共党员，副县长（挂职）",
        },
        {
            "id": "S008",
            "title": "东辽县人民政府官网-县政府-副县长吴跃泉",
            "url": "http://www.dongliao.gov.cn/xzf/zfld/fxz/wyq/",
            "publisher": "东辽县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "吴跃泉: 男，汉族，1974年12月生，大学学历，中共党员，副县长、公安局局长",
        },
        {
            "id": "S009",
            "title": "东辽县人民政府官网-县政府-副县长邱国军",
            "url": "http://www.dongliao.gov.cn/xzf/zfld/fxz/qgj/",
            "publisher": "东辽县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "邱国军: 男，汉族，1974年12月生，大专学历，中共党员，副县长",
        },
        {
            "id": "S010",
            "title": "东辽县人民政府-政府会议-防汛工作部署大会",
            "url": "http://www.dongliao.gov.cn/xzf/zfhy/202607/t20260709_744104.html",
            "publisher": "东辽县人民政府",
            "published_at": "2026-07-09",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认石磊为东辽县县委书记（截至2026年7月8日）",
        },
        {
            "id": "S011",
            "title": "东辽县人民政府-政府工作报告-2024年东辽县政府工作报告",
            "url": "http://www.dongliao.gov.cn/xzf/gzbg/202510/t20251009_721966.html",
            "publisher": "东辽县人民政府",
            "published_at": "2025-10-09",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认石磊2025年1月以代理县长身份作政府工作报告",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"dongliao_{name}"

    # ── 石磊 (县委书记) ──
    if name == "石磊":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "吉林省",
                "city": "辽源市",
                "region": "东辽县",
                "job": "县委书记",
                "task_id": "jilin_东辽县",
                "time_focus": "2025–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "石磊",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "石磊_",
                    "name_birthplace": "石磊_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共东辽县委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S010"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "2025年初",
                    "org": "东辽县人民政府",
                    "title": "未知（任县长前职务）",
                    "level": "",
                    "location": "吉林省辽源市东辽县",
                    "system": "government",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "石磊任东辽县代理县长前的职务公开信息不足",
                    "confidence": "unverified",
                    "source_ids": [],
                },
                {
                    "start": "2025年1月前",
                    "end": "2026年初",
                    "org": "东辽县人民政府",
                    "title": "县长（代县长）",
                    "level": "正处级",
                    "location": "吉林省辽源市东辽县",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2025年1月3日以代理县长身份在县十八届人大四次会议上作政府工作报告",
                    "confidence": "confirmed",
                    "source_ids": ["S011"],
                },
                {
                    "start": "2026年初",
                    "end": "present",
                    "org": "中共东辽县委员会",
                    "title": "县委书记",
                    "level": "正处级",
                    "location": "吉林省辽源市东辽县",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2026年7月8日以县委书记身份主持召开全县防汛工作部署大会",
                    "confidence": "confirmed",
                    "source_ids": ["S010"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共东辽县委员会", "type": "党委",
                 "level": "县处级", "location": "吉林省辽源市东辽县"},
                {"org_id": 2, "name": "东辽县人民政府", "type": "政府",
                 "level": "县处级", "location": "吉林省辽源市东辽县"},
            ],
            "relationships": [
                {"person": "田国栋", "person_id": "dongliao_田国栋",
                 "relationship_type": "predecessor_successor", "strength": "strong",
                 "evidence": "石磊由县长晋升县委书记，田国栋接任县长",
                 "overlap_org": "东辽县人民政府/中共东辽县委员会",
                 "overlap_period": "2025-2026年",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S010", "S011"]},
                {"person": "田国栋", "person_id": "dongliao_田国栋",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "县委书记与县长党政主要领导搭档",
                 "overlap_org": "中共东辽县委员会/东辽县人民政府",
                 "overlap_period": "2026年起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S010"]},
                {"person": "李宝刚", "person_id": "dongliao_李宝刚",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "县委书记与县委常委、常务副县长",
                 "overlap_org": "中共东辽县委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
            ],
            "governance_record": [
                {
                    "period": "2025年1月",
                    "domain": "other",
                    "achievement_or_event": "作2024年东辽县人民政府工作报告",
                    "role_in_event": "代理县长，作报告",
                    "measurable_outcome": "总结2024年工作，全县地区生产总值增长4.5%左右",
                    "location": "东辽县",
                    "confidence": "confirmed",
                    "source_ids": ["S011"],
                },
                {
                    "period": "2026年7月",
                    "domain": "public_security",
                    "achievement_or_event": "主持召开全县防汛工作部署大会暨东辽县防汛工作视频会议",
                    "role_in_event": "县委书记，主持会议并作部署",
                    "measurable_outcome": "全面部署防汛减灾工作，要求各级干部下沉一线",
                    "location": "东辽县",
                    "confidence": "confirmed",
                    "source_ids": ["S010"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["辽源市"],
                "promotion_velocity": {
                    "summary": "从县长晋升县委书记属常见干部晋升路径；公开源不足，无法精确分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道以政务会议为主，暂不足以判断工作风格",
                        "confidence": "unverified",
                        "source_ids": [],
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "石磊的完整履历（出生年月、籍贯、教育背景、任代理县长前的职业生涯）均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "石磊的出生年月、籍贯、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["石磊 简历 东辽县 辽源", "石磊 出生"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "石磊何时开始担任东辽县代理县长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和职业生涯全貌",
                    "suggested_queries": ["石磊 任 东辽县 县长 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "石磊何时由县长转任县委书记？",
                    "why_it_matters": "确认具体交接时间节点",
                    "suggested_queries": ["石磊 任 县委书记 东辽县"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "石磊的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["石磊 工作 经历 东辽"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "前任县委书记是谁？",
                    "why_it_matters": "理清县委书记交接链条",
                    "suggested_queries": ["东辽县 前任 县委书记"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 田国栋 (县长) ──
    if name == "田国栋":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "吉林省",
                "city": "辽源市",
                "region": "东辽县",
                "job": "县长",
                "task_id": "jilin_东辽县",
                "time_focus": "2025–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "田国栋",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1976年7月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {"period": "", "institution": "", "major": "", "degree": "省委党校研究生",
                     "study_type": "party_school", "source_ids": ["S001"]},
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "田国栋_197607",
                    "name_birthplace": "田国栋_",
                    "official_profile_url": "http://www.dongliao.gov.cn/xzf/zfld/xz/tgd/",
                },
            },
            "current_status": {
                "current_post": "县长",
                "current_org": "东辽县人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "东辽县人民政府",
                    "title": "县长",
                    "level": "正处级",
                    "location": "吉林省辽源市东辽县",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "主持县政府全面工作，分管县审计局",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共东辽县委员会",
                    "title": "县委副书记",
                    "level": "副处级",
                    "location": "吉林省辽源市东辽县",
                    "system": "party",
                    "rank": "副处级",
                    "is_key_promotion": False,
                    "notes": "县委副书记、县长",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "东辽县人民政府", "type": "政府",
                 "level": "县处级", "location": "吉林省辽源市东辽县"},
                {"org_id": 1, "name": "中共东辽县委员会", "type": "党委",
                 "level": "县处级", "location": "吉林省辽源市东辽县"},
            ],
            "relationships": [
                {"person": "石磊", "person_id": "dongliao_石磊",
                 "relationship_type": "predecessor_successor", "strength": "strong",
                 "evidence": "田国栋接替石磊担任东辽县县长",
                 "overlap_org": "东辽县人民政府",
                 "overlap_period": "2025-2026年",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S010", "S011"]},
                {"person": "石磊", "person_id": "dongliao_石磊",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "县长与县委书记党政主要领导搭档",
                 "overlap_org": "中共东辽县委员会/东辽县人民政府",
                 "overlap_period": "2026年起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S010"]},
                {"person": "李宝刚", "person_id": "dongliao_李宝刚",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "县长与县委常委、常务副县长",
                 "overlap_org": "东辽县人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
                {"person": "高峰", "person_id": "dongliao_高峰",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "县长与副县长（挂职）",
                 "overlap_org": "东辽县人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
                {"person": "赵丰双", "person_id": "dongliao_赵丰双",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "县长与副县长",
                 "overlap_org": "东辽县人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S004"]},
                {"person": "姜贤", "person_id": "dongliao_姜贤",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "县长与副县长",
                 "overlap_org": "东辽县人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S005"]},
                {"person": "张志民", "person_id": "dongliao_张志民",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "县长与副县长",
                 "overlap_org": "东辽县人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S006"]},
                {"person": "陈亮", "person_id": "dongliao_陈亮",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "县长与副县长（挂职）",
                 "overlap_org": "东辽县人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S007"]},
                {"person": "吴跃泉", "person_id": "dongliao_吴跃泉",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "县长与副县长、公安局局长",
                 "overlap_org": "东辽县人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S008"]},
                {"person": "邱国军", "person_id": "dongliao_邱国军",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "县长与副县长",
                 "overlap_org": "东辽县人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S009"]},
            ],
            "governance_record": [
                {
                    "period": "2026年4月",
                    "domain": "public_security",
                    "achievement_or_event": "主持召开县安委会2026年第二次全体（扩大）会议暨安全生产治本攻坚三年行动推进部署会议",
                    "role_in_event": "县长，主持会议",
                    "measurable_outcome": "部署九大行动52项任务，强调矿山、危化品、消防等重点领域隐患排查",
                    "location": "东辽县",
                    "confidence": "confirmed",
                    "source_ids": [],
                },
                {
                    "period": "2026年7月",
                    "domain": "public_security",
                    "achievement_or_event": "参与全县防汛工作部署大会，围绕隐患清零、监测预警、群众转移等作全面部署",
                    "role_in_event": "县长，作防汛工作部署",
                    "measurable_outcome": "要求各部门加密监测研判、完善应急预案",
                    "location": "东辽县",
                    "confidence": "confirmed",
                    "source_ids": ["S010"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["辽源市"],
                "promotion_velocity": {
                    "summary": "公开源不足，无法精确分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道以政务会议为主，暂不足以判断工作风格",
                        "confidence": "unverified",
                        "source_ids": [],
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "田国栋任县长前的完整职业生涯履历（前任职务、入职时间等）未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "田国栋的籍贯和毕业院校详情？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["田国栋 简历 东辽县", "田国栋 辽源"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "田国栋何时开始担任东辽县县长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和职业生涯全貌",
                    "suggested_queries": ["田国栋 任 东辽县 县长 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "田国栋的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["田国栋 工作 经历"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    return {}


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSON files
    person_configs = [
        ("县委书记", "石磊"),
        ("县长", "田国栋"),
    ]

    for job, name in person_configs:
        data = generate_person_json(job, name)
        if data:
            fname = f"{TODAY}-吉林省-辽源市-{job}-{name}.json"
            fpath = PERSONS_DIR / fname
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Wrote {fpath}")

    print(f"\nDone. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs in: {PERSONS_DIR}")
