#!/usr/bin/env python3
"""Build 壤塘县 (Rangtang County, Aba Prefecture, Sichuan) network data.

Data source: 壤塘县人民政府 official website (https://www.rangtang.gov.cn)
Accessed: 2026-07-28

Note: 县委书记 position is NOT LISTED on the official leadership page as of 2026-07-28.
This is flagged as a critical gap. The county mayor (罗先全 县委副书记/县长) is the
highest-ranked person listed.
"""

from __future__ import annotations

import sys
import json
from pathlib import Path

# ── Path setup ──────────────────────────────────────────────────────────
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Scoping ──────────────────────────────────────────────────────────────
SLUG = "壤塘县"
PROVINCE = "四川省"
PARENT_CITY = "阿坝藏族羌族自治州"
LEVEL = "县"
TODAY = "2026-07-28"

# ========================================================================
# PERSONS
# ========================================================================

persons = [
    # ── 县委 (Party Committee) ──
    {
        "id": 1,
        "name": "罗先全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-12",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "中共壤塘县委副书记、壤塘县人民政府县长",
        "current_org": "壤塘县人民政府",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100066/202309/c305beb386ce43a69f40547fcc251c12.shtml",
    },
    {
        "id": 2,
        "name": "阿旺",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1976-07",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "中共壤塘县委副书记",
        "current_org": "中共壤塘县委",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100066/202410/87090bfdbebc4181921830a86381d880.shtml",
    },
    {
        "id": 3,
        "name": "邓南新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-09",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "中共壤塘县委副书记",
        "current_org": "中共壤塘县委",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100066/201904/23e67ca40a9e43a389659e87a4b30361.shtml",
    },
    {
        "id": 4,
        "name": "李远",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1984-11",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "中共壤塘县委副书记（挂职）",
        "current_org": "中共壤塘县委",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100066/202409/9436965e9a624199b7013233415f1fa8.shtml",
    },
    {
        "id": 5,
        "name": "董宗梁",
        "gender": "男",
        "ethnicity": "羌族",
        "birth": "1978-06",
        "birthplace": "四川理县",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "中共壤塘县委常委、壤塘县人民政府常务副县长",
        "current_org": "壤塘县人民政府",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100066/201904/d12c8a356717450daaff572baca592d5.shtml",
    },
    {
        "id": 6,
        "name": "赵春勇",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1981-12",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "中共壤塘县委常委、统战部长、县总工会主席",
        "current_org": "中共壤塘县委统战部",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100066/202111/ebfbb1c4e34e44239e24e56e5c666a33.shtml",
    },
    {
        "id": 7,
        "name": "康术元",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1980-09",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "中共壤塘县委常委、政法委书记",
        "current_org": "中共壤塘县委政法委",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100066/202010/e11ec2bda16847ad93787a3b21740e8e.shtml",
    },
    {
        "id": 8,
        "name": "袁航导",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1979-10",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "中共壤塘县委常委、县纪委书记、县监察委员会主任",
        "current_org": "中共壤塘县纪律检查委员会",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100066/202402/c56106f880b94d50939845512cb5ba6f.shtml",
    },
    {
        "id": 9,
        "name": "陈永霖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-01",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "中共壤塘县委常委、壤塘县人民政府副县长（挂职）",
        "current_org": "壤塘县人民政府",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100066/202412/473e9ae661b04a88add1374ffcc14d87.shtml",
    },
    {
        "id": 10,
        "name": "朵强",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1978-12",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "中共壤塘县委常委、壤塘县人民政府副县长",
        "current_org": "壤塘县人民政府",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100066/202411/15181f32a401464983a0d839e34d1140.shtml",
    },
    {
        "id": 11,
        "name": "马晓波",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1983-03",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "中共壤塘县委常委、县委办公室主任",
        "current_org": "中共壤塘县委办公室",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100066/202412/6b207c945e684f2584dc00ccd2b74d.shtml",
    },
    {
        "id": 12,
        "name": "旦措",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "1985-08",
        "birthplace": "四川马尔康",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "中共壤塘县委常委、宣传部部长",
        "current_org": "中共壤塘县委宣传部",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100066/202412/0594b99a4ea04fd3b02fcf57cf162ceb.shtml",
    },
    {
        "id": 13,
        "name": "吕勇",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1978-04",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "中共壤塘县委常委、组织部部长",
        "current_org": "中共壤塘县委组织部",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100066/202111/6e4024bf234e42d8bfe7bccb310cb483.shtml",
    },
    {
        "id": 14,
        "name": "张翼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-08",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "中共壤塘县委常委、壤塘县人民政府副县长（挂职）",
        "current_org": "壤塘县人民政府",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100066/202309/938ac1df7cce465f93e29a143ba8760c.shtml",
    },
    # ── 县政府 (County Government - Deputy Mayors) ──
    {
        "id": 15,
        "name": "王基",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1976-07",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "壤塘县人民政府副县长",
        "current_org": "壤塘县人民政府",
        "source": "https://www.rangtang.gov.cn/xtxrrmzf/c100414/202111/ce6f0b15e7d74987aa351c95fddf544e.shtml",
    },
    {
        "id": 16,
        "name": "王辅川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-12",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "壤塘县人民政府副县长",
        "current_org": "壤塘县人民政府",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100414/202111/c5afb167af12799b8605c4c875b80.shtml",
    },
    {
        "id": 17,
        "name": "李昌祥",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1979-04",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "壤塘县人民政府副县长、县公安局局长",
        "current_org": "壤塘县公安局",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100414/202405/3983b291772e93560eb054c42aa551195.shtml",
    },
    {
        "id": 18,
        "name": "克让措",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "1979-10",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "壤塘县人民政府副县长",
        "current_org": "壤塘县人民政府",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100414/202111/3de670895037a2693520a3c9b885e5.shtml",
    },
    {
        "id": 19,
        "name": "杨勇",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1982-04",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "壤塘县人民政府副县长",
        "current_org": "壤塘县人民政府",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/100414/202111/cc8a64ccd1c24e90a75468d5dbe7bd2f.shtml",
    },
    # ── 人大 (People's Congress) ──
    {
        "id": 20,
        "name": "刘木滚",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1967-07",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "壤塘县人大常委会主任",
        "current_org": "壤塘县人大常委会",
        "source": "https://www.rangtang.gov.cn/xtxrmrf/100072/201904/6bf54a3aa4e44f87301386ce0e596b.shtml",
    },
    # ── 政协 (CPPCC) ──
    {
        "id": 21,
        "name": "张万贵",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1973-10",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "政协壤塘县委员会主席",
        "current_org": "政协壤塘县委员会",
        "source": "https://www.rangtang.gov.cn/xtxrmzf/c100442/201904/7b734ce5939a43d8ae9684e123b00f.shtml",
    },
]

# ================================================================
# 2. ORGANIZATIONS
# ================================================================

organizations = [
    {"id": 1, "name": "中共壤塘县委", "type": "党委", "level": "县级", "parent": PARENT_CITY, "location": "壤塘县"},
    {"id": 2, "name": "壤塘县人民政府", "type": "政府", "level": "县级", "parent": PARENT_CITY, "location": "壤塘县"},
    {"id": 3, "name": "中共壤塘县纪律检查委员会", "type": "党委", "level": "县级", "parent": PARENT_CITY, "location": "壤塘县"},
    {"id": 4, "name": "中共壤塘县委统战部", "type": "党委", "level": "县级", "parent": PARENT_CITY, "location": "壤塘县"},
    {"id": 5, "name": "中共壤塘县委政法委", "type": "党委", "level": "县级", "parent": PARENT_CITY, "location": "壤塘县"},
    {"id": 6, "name": "中共壤塘县委宣传部", "type": "党委", "level": "县级", "parent": PARENT_CITY, "location": "壤塘县"},
    {"id": 7, "name": "中共壤塘县委组织部", "type": "党委", "level": "县级", "parent": PARENT_CITY, "location": "壤塘县"},
    {"id": 8, "name": "中共壤塘县委办公室", "type": "党委", "level": "县级", "parent": PARENT_CITY, "location": "壤塘县"},
    {"id": 9, "name": "壤塘县人大常委会", "type": "人大", "level": "县级", "parent": PARENT_CITY, "location": "壤塘县"},
    {"id": 10, "name": "政协壤塘县委员会", "type": "政协", "level": "县级", "parent": PARENT_CITY, "location": "壤塘县"},
    {"id": 11, "name": "壤塘县公安局", "type": "政府", "level": "县级", "parent": PARENT_CITY, "location": "壤塘县"},
]

# ============================================================
# 3. POSITIONS
# ============================================================
positions = [
    # 罗先全
    {"person_id": 1, "org_id": 1, "title": "中共壤塘县委副书记", "start_date": "", "end_date": "present", "rank": "副县级"},
    {"person_id": 1, "org_id": 2, "title": "壤塘县人民政府县长", "start_date": "", "end_date": "present", "rank": "正县级"},
    # 阿旺
    {"person_id": 2, "org_id": 1, "title": "中共壤塘县委副书记", "start_date": "", "end_date": "present", "rank": "副县级"},
    # 邓南新
    {"person_id": 3, "org_id": 1, "title": "中共壤塘县委副书记", "start_date": "", "end_date": "present", "rank": "副县级"},
    # 李远（挂职）
    {"person_id": 4, "org_id": 1, "title": "中共壤塘县委副书记（挂职）", "start_date": "", "end_date": "present", "rank": "副县级"},
    # 董宗梁
    {"person_id": 5, "org_id": 1, "title": "中共壤塘县委常委", "start_date": "", "end_date": "present", "rank": "副县级"},
    {"person_id": 5, "org_id": 2, "title": "壤塘县人民政府常务副县长", "start_date": "", "end_date": "present", "rank": "副县级"},
    # 赵春勇
    {"person_id": 6, "org_id": 1, "title": "中共壤塘县委常委", "start_date": "", "end_date": "present", "rank": "副县级"},
    {"person_id": 6, "org_id": 4, "title": "统战部长、县总工会主席", "start_date": "", "end_date": "present", "rank": ""},
    # 康术元
    {"person_id": 7, "org_id": 1, "title": "中共壤塘县委常委", "start_date": "", "end_date": "present", "rank": "副县级"},
    {"person_id": 7, "org_id": 5, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": ""},
    # 袁航导
    {"person_id": 8, "org_id": 1, "title": "中共壤塘县委常委", "start_date": "", "end_date": "present", "rank": "副县级"},
    {"person_id": 8, "org_id": 3, "title": "县纪委书记、县监委主任", "start_date": "", "end_date": "present", "rank": ""},
    # 陈永霖（挂职）
    {"person_id": 9, "org_id": 1, "title": "中共壤塘县委常委（挂职）", "start_date": "", "end_date": "present", "rank": "副县级"},
    {"person_id": 9, "org_id": 2, "title": "壤塘县人民政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": ""},
    # 朵强
    {"person_id": 10, "org_id": 1, "title": "中共壤塘县委常委", "start_date": "", "end_date": "present", "rank": "副县级"},
    {"person_id": 10, "org_id": 2, "title": "壤塘县人民政府副县长", "start_date": "", "end_date": "present", "rank": ""},
    # 马晓波
    {"person_id": 11, "org_id": 1, "title": "中共壤塘县委常委", "start_date": "", "end_date": "present", "rank": "副县级"},
    {"person_id": 11, "org_id": 8, "title": "县委办公室主任", "start_date": "", "end_date": "present", "rank": ""},
    # 旦措
    {"person_id": 12, "org_id": 1, "title": "中共壤塘县委常委", "start_date": "", "end_date": "present", "rank": "副县级"},
    {"person_id": 12, "org_id": 6, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": ""},
    # 吕勇
    {"person_id": 13, "org_id": 1, "title": "中共壤塘县委常委", "start_date": "", "end_date": "present", "rank": "副县级"},
    {"person_id": 13, "org_id": 7, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": ""},
    # 张翼（挂职）
    {"person_id": 14, "org_id": 1, "title": "中共壤塘县委常委（挂职）", "start_date": "", "end_date": "present", "rank": "副县级"},
    {"person_id": 14, "org_id": 2, "title": "壤塘县人民政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": ""},
    # 王基
    {"person_id": 15, "org_id": 2, "title": "壤塘县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副县级"},
    # 王辅川
    {"person_id": 16, "org_id": 2, "title": "壤塘县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副县级"},
    # 李昌祥
    {"person_id": 17, "org_id": 2, "title": "壤塘县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副县级"},
    {"person_id": 17, "org_id": 11, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": ""},
    # 克让措
    {"person_id": 18, "org_id": 2, "title": "壤塘县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副县级"},
    # 杨勇
    {"person_id": 19, "org_id": 2, "title": "壤塘县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副县级"},
    # 刘木滚
    {"person_id": 20, "org_id": 9, "title": "壤塘县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级"},
    # 张万贵
    {"person_id": 21, "org_id": 10, "title": "政协壤塘县委员会主席", "start_date": "", "end_date": "present", "rank": "正县级"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================

# All county committee members work together in the same county leadership,
# they overlap in 中共壤塘县委
relationships = [
    # 罗先全 and 董宗梁 — 县长 + 常务副县长 overlap
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县长与常务副县长工作关系",
     "overlap_org": "壤塘县人民政府", "overlap_period": "present"},

    # 罗先全 and 阿旺 — 县委副书记同僚
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委副书记同僚，县长与维稳副书记",
     "overlap_org": "中共壤塘县委", "overlap_period": "present"},

    # 罗先全 and 邓南新 — 县委副书记同僚
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委副书记同僚，县长与党建副书记",
     "overlap_org": "中共壤塘县委", "overlap_period": "present"},

    # 邓南新 and 董宗梁 — 党建副书记 + 常务副县长，工作紧密
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "县委副书记与常务副县长协同抓经济",
     "overlap_org": "中共壤塘县委", "overlap_period": "present"},

    # 县委常委会成员之间
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "县委常委员会同事，统战与政法",
     "overlap_org": "中共壤塘县常委会", "overlap_period": "present"},
    {"person_a": 8, "person_b": 13, "type": "overlap", "context": "纪委与组织部 — 干部监督与管理工作配合",
     "overlap_org": "中共壤塘县常委会", "overlap_period": "present"},
    {"person_a": 12, "person_b": 13, "type": "overlap", "context": "宣传与组织部 — 县委宣传与干部管理配合",
     "overlap_org": "中共壤塘县常委会", "overlap_period": "present"},

    # 董宗梁 + 副县长们
    {"person_a": 5, "person_b": 15, "type": "overlap", "context": "常务副县长与副县长 — 政府班子同僚",
     "overlap_org": "壤塘县人民政府", "overlap_period": "present"},
    {"person_a": 5, "person_b": 16, "type": "overlap", "context": "常务副县长与副县长 — 政府班子同僚",
     "overlap_org": "壤塘县人民政府", "overlap_period": "present"},
    {"person_a": 5, "person_b": 17, "type": "overlap", "context": "常务副县长与副县长 — 政府班子同僚",
     "overlap_org": "壤塘县人民政府", "overlap_period": "present"},

    # 挂职副书记与挂职副县长 — 帮扶线
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "挂职副书记与挂职副县长 — 对口帮扶线",
     "overlap_org": "中共壤塘县委", "overlap_period": "present"},

    # 人大与政协
    {"person_a": 20, "person_b": 21, "type": "overlap", "context": "人大主任与政协主席 — 两会系统配合",
     "overlap_org": "壤塘县", "overlap_period": "present"},
]

# ============================================================
# 5. RUN BUILD
# ============================================================

STAGING = REPO / "data" / "tmp" / "sichuan_壤塘县"

def main() -> None:
    db_path = STAGING / f"{SLUG}_network.db"
    gexf_path = STAGING / f"{SLUG}_network.gexf"

    print(f"Building database: {db_path}")
    print(f"Building GEXF: {gexf_path}")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    # Verify
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    cur = conn.execute("SELECT COUNT(*) FROM persons")
    print(f"  Persons in DB: {cur.fetchone()[0]}")
    cur = conn.execute("SELECT COUNT(*) FROM organizations")
    print(f"  Orgs in DB: {cur.fetchone()[0]}")
    cur = conn.execute("SELECT COUNT(*) FROM positions")
    print(f"  Positions in DB: {cur.fetchone()[0]}")
    cur = conn.execute("SELECT COUNT(*) FROM relationships")
    print(f"  Relationships in DB: {cur.fetchone()[0]}")
    conn.close()

    # Verify GEXF exists and has content
    import os
    gexf_size = os.path.getsize(gexf_path)
    print(f"  GEXF size: {gexf_size} bytes")
    print("Done!")


if __name__ == "__main__":
    main()