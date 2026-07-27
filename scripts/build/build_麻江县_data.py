#!/usr/bin/env python3
"""Build script for 麻江县 (Majiang County, 黔东南州, 贵州省) leadership network.

Generated: 2026-07-23
Level: 县
Province: 贵州省
Parent City: 黔东南苗族侗族自治州
Targets: 县委书记 & 县长

Research Note:
  The county government website (www.majiang.gov.cn) was fully accessible. The
  领导之窗 page confirmed the full county government roster with detailed
  biographies and work divisions for 7 government leaders (县长 + 6 副县长).
  Party committee leadership (县委领导班子) was confirmed from news articles
  on the same domain (June-July 2026).

  Notes on gaps:
  - 唐光宏 (县委书记): Name confirmed from multiple official news articles
    (June-July 2026), but no standalone biography page was found on the
    government website. Birth year, birthplace, education, and career history
    are partially known from media reports.
  - 梅松明、敬小川 (县委副书记): Names confirmed from news articles, no
    detailed biographies available.
  - 前任县委书记 和 前任县长: Not found with available search tools.

Sources:
  - https://www.majiang.gov.cn/zwgk/ldzc/ (领导之窗 — confirmed all 7 government leaders)
  - https://www.majiang.gov.cn/xwzx/ywjj/ (news articles confirming 县委 leadership)
"""

import sqlite3
from pathlib import Path
from datetime import datetime

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders: 县委书记 (PARTY SECRETARY) ──
    {
        "id": 1,
        "name": "唐光宏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "麻江县委书记",
        "current_org": "中共麻江县委员会",
        "source": "https://www.majiang.gov.cn/xwzx/ywjj/202607/t20260721_90647122.html （官方新闻确认）",
    },
    # ── Core Leaders: 县长 (COUNTY MAYOR) ──
    {
        "id": 2,
        "name": "卢天成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年8月",
        "birthplace": "",
        "education": "大学(管理学学士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "麻江县委副书记、县人民政府县长、党组书记",
        "current_org": "麻江县人民政府",
        "source": "https://www.majiang.gov.cn/zwgk/ldzc/202410/t20241029_85997321.html （官网领导之窗确认简历）",
    },
    # ── 县委副书记 (confirmed from news) ──
    {
        "id": 3,
        "name": "梅松明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "麻江县委副书记",
        "current_org": "中共麻江县委员会",
        "source": "https://www.majiang.gov.cn/xwzx/ywjj/202606/t20260623_90548413.html （官方新闻确认）",
    },
    {
        "id": 4,
        "name": "敬小川",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "麻江县委副书记",
        "current_org": "中共麻江县委员会",
        "source": "https://www.majiang.gov.cn/xwzx/ywjj/202606/t20260623_90548413.html （官方新闻确认）",
    },
    # ── 县政府领导班子 (confirmed from 领导之窗) ──
    # 县委常委、副县长
    {
        "id": 5,
        "name": "罗辉坤",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1986年6月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "麻江县委常委、县人民政府副县长、党组成员",
        "current_org": "麻江县人民政府",
        "source": "https://www.majiang.gov.cn/zwgk/ldzc/202110/t20211011_83558462.html （官网领导之窗确认简历）",
    },
    # 县委常委、副县长（挂职）
    {
        "id": 6,
        "name": "陈建明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "麻江县委常委、县人民政府副县长、党组成员（挂职）",
        "current_org": "麻江县人民政府",
        "source": "https://www.majiang.gov.cn/zwgk/ldzc/202404/t20240425_84355389.html （官网领导之窗确认简历）",
    },
    # 县委常委、副县长（挂职）
    {
        "id": 7,
        "name": "吴峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年7月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "麻江县委常委、县人民政府副县长、党组成员（挂职）",
        "current_org": "麻江县人民政府",
        "source": "https://www.majiang.gov.cn/zwgk/ldzc/202512/t20251228_89095469.html （官网领导之窗确认简历）",
    },
    # 副县长
    {
        "id": 8,
        "name": "杨秀智",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "麻江县人民政府副县长、党组成员",
        "current_org": "麻江县人民政府",
        "source": "https://www.majiang.gov.cn/zwgk/ldzc/202106/t20210625_83558463.html （官网领导之窗确认简历）",
    },
    # 副县长
    {
        "id": 9,
        "name": "邱毅江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年3月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "麻江县人民政府副县长、党组成员",
        "current_org": "麻江县人民政府",
        "source": "https://www.majiang.gov.cn/zwgk/ldzc/202309/t20230915_83558466.html （官网领导之窗确认简历）",
    },
    # 副县长、公安局长
    {
        "id": 10,
        "name": "胡晓锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年2月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "麻江县人民政府副县长、党组成员，县公安局局长、党委书记",
        "current_org": "麻江县人民政府",
        "source": "https://www.majiang.gov.cn/zwgk/ldzc/202404/t20240425_84355518.html （官网领导之窗确认简历）",
    },
    # 副县长
    {
        "id": 11,
        "name": "李兰萍",
        "gender": "女",
        "ethnicity": "彝族",
        "birth": "1985年10月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "麻江县人民政府副县长",
        "current_org": "麻江县人民政府",
        "source": "https://www.majiang.gov.cn/zwgk/ldzc/202405/t20240531_84714021.html （官网领导之窗确认简历）",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共麻江县委员会", "type": "党委", "level": "县级", "parent": "中共黔东南州委员会", "location": "贵州省黔东南州麻江县"},
    {"id": 2, "name": "麻江县人民政府", "type": "政府", "level": "县级", "parent": "黔东南州人民政府", "location": "贵州省黔东南州麻江县"},
    {"id": 3, "name": "麻江县公安局", "type": "政府", "level": "正科级", "parent": "麻江县人民政府", "location": "贵州省黔东南州麻江县"},
]

POSITIONS = [
    # 县委
    {"person_id": 1, "org_id": 1, "title": "麻江县委书记", "start": "", "end": "present", "rank": "正处级", "note": "confirmed from multiple news articles (2026)"},
    {"person_id": 2, "org_id": 1, "title": "麻江县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "麻江县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "麻江县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "麻江县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "麻江县委常委", "start": "", "end": "present", "rank": "副处级", "note": "挂职"},
    {"person_id": 7, "org_id": 1, "title": "麻江县委常委", "start": "", "end": "present", "rank": "副处级", "note": "挂职"},
    # 政府
    {"person_id": 2, "org_id": 2, "title": "麻江县人民政府县长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "麻江县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "麻江县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "挂职"},
    {"person_id": 7, "org_id": 2, "title": "麻江县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "挂职"},
    {"person_id": 8, "org_id": 2, "title": "麻江县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "麻江县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "麻江县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "麻江县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 公安局
    {"person_id": 10, "org_id": 3, "title": "麻江县公安局局长、党委书记", "start": "", "end": "present", "rank": "正科级", "note": "兼副县长"},
]

RELATIONSHIPS = [
    # 县委核心：书记与副书记
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭档", "overlap_org": "中共麻江县委员会", "overlap_period": "2024-2026"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与专职副书记", "overlap_org": "中共麻江县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与专职副书记", "overlap_org": "中共麻江县委员会", "overlap_period": "2026"},
    # 政府班子：县长与副县长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与常务/副县长", "overlap_org": "麻江县人民政府", "overlap_period": "2024-2026"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "麻江县人民政府", "overlap_period": "2024-2026"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "麻江县人民政府", "overlap_period": "2024-2026"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长/公安局长", "overlap_org": "麻江县人民政府", "overlap_period": "2024-2026"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "麻江县人民政府", "overlap_period": "2024-2026"},
    # 县委常委关系
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "同为县委常委、副县长", "overlap_org": "麻江县人民政府", "overlap_period": "2024-2026"},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "同为县委常委、副县长", "overlap_org": "麻江县人民政府", "overlap_period": "2024-2026"},
    # 挂职副县长与南京农业大学
    {"person_a": 7, "person_b": 6, "type": "overlap", "context": "均为挂职副县长（南农大挂职与东西部协作）", "overlap_org": "麻江县人民政府", "overlap_period": "2024-2026"},
]

# fmt: on
# ═══════════════════════════════════════════════════
# 县领导分工摘要（用于备注）
# ═══════════════════════════════════════════════════
LEADER_DUTIES = {
    "罗辉坤": "住建、交通、林业、自然资源、环保、邮政管理",
    "陈建明": "东西部协作、招商引资（挂职）",
    "吴峰": "南农大定点帮扶、农业农村（挂职）",
    "杨秀智": "农业、水务、乡村振兴、供销、蓝莓、蔬菜、烤烟",
    "邱毅江": "民政、工信、商务、科技、招商引资、市场监管、酸汤产业",
    "胡晓锋": "公安、国安、司法、退役军人、民族宗教",
    "李兰萍": "教育、文化、旅游、体育、卫生健康、医疗保障",
}


def build(db_path, gexf_path):
    """Build the 麻江县 leadership network."""
    run_build(
        slug="麻江县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=db_path,
        gexf_path=gexf_path,
    )


if __name__ == "__main__":
    import sys

    staging = Path(__file__).parent
    DB_PATH = staging / "麻江县_network.db"
    GEXF_PATH = staging / "麻江县_network.gexf"
    build(DB_PATH, GEXF_PATH)
    print(f"✅ 麻江县 network built successfully.")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
