#!/usr/bin/env python3
"""Build 泸西县 (Luxi County) 领导班子工作关系网络.

云南省红河哈尼族彝族自治州泸西县.
数据来源: 泸西县人民政府网站 (hhlx.gov.cn), 百度百科, 百度搜索.
调查日期: 2026-07-28.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "泸西县"
TODAY = "2026-07-28"
PROVINCE = "云南省"
CITY = "红河哈尼族彝族自治州"
TASK = "yunnan_泸西县"

# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    # -- 县委常委 --
    {
        "id": 1,
        "name": "夏明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年4月",
        "birthplace": "",
        "education": "省委党校大学学历",
        "party_join": "中共党员",
        "work_start": "1995年8月",
        "current_post": "县委书记",
        "current_org": "中共泸西县委",
        "source": "百度百科; 泸西县第十五届党代会(2026-06-27)",
    },
    {
        "id": 2,
        "name": "邓飚雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年3月",
        "birthplace": "云南蒙自",
        "education": "大学学历",
        "party_join": "1997年5月",
        "work_start": "1997年8月",
        "current_post": "县委副书记、县长",
        "current_org": "泸西县人民政府",
        "source": "https://www.hhlx.gov.cn/zfxxgk/fdzdgknr/zfld.htm",
    },
    {
        "id": 3,
        "name": "曾云梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2004年3月",
        "current_post": "县委副书记",
        "current_org": "中共泸西县委",
        "source": "百度搜索; 泸西县第十五届党代会(2026-06-27)",
    },
    {
        "id": 4,
        "name": "李俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共泸西县委",
        "source": "泸西县第十五届党代会执行主席名单(2026-06-27)",
    },
    {
        "id": 5,
        "name": "段立青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共泸西县委",
        "source": "泸西县第十五届党代会执行主席名单(2026-06-27)",
    },
    {
        "id": 6,
        "name": "普李芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共泸西县委",
        "source": "泸西县第十五届党代会执行主席名单(2026-06-27)",
    },
    {
        "id": 7,
        "name": "燕斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "云南泸西",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "泸西县人民政府",
        "source": "https://www.hhlx.gov.cn/zfxxgk/fdzdgknr/zfld.htm",
    },
    {
        "id": 8,
        "name": "李戈",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共泸西县委",
        "source": "泸西县第十五届党代会执行主席名单(2026-06-27)",
    },
    {
        "id": 9,
        "name": "宋国清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共泸西县委",
        "source": "泸西县第十五届党代会执行主席名单(2026-06-27)",
    },
    {
        "id": 10,
        "name": "张超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共泸西县委",
        "source": "泸西县第十五届党代会执行主席名单(2026-06-27)",
    },
    {
        "id": 11,
        "name": "马继东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共泸西县委",
        "source": "泸西县第十五届党代会执行主席名单(2026-06-27)",
    },
    {
        "id": 12,
        "name": "段泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共泸西县委",
        "source": "泸西县第十五届党代会执行主席名单(2026-06-27)",
    },
    {
        "id": 13,
        "name": "佟婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共泸西县委",
        "source": "泸西县第十五届党代会执行主席名单(2026-06-27)",
    },
    # ── 县政府领导(非县委常委) ──
    {
        "id": 14,
        "name": "朱进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长(挂职)",
        "current_org": "泸西县人民政府",
        "source": "https://www.hhlx.gov.cn/zfxxgk/fdzdgknr/zfld.htm",
    },
    {
        "id": 15,
        "name": "殷丽萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "云南泸西",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "泸西县人民政府",
        "source": "https://www.hhlx.gov.cn/zfxxgk/fdzdgknr/zfld.htm",
    },
    {
        "id": 16,
        "name": "李杨",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "云南昆明",
        "education": "",
        "party_join": "致公党",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "泸西县人民政府",
        "source": "https://www.hhlx.gov.cn/zfxxgk/fdzdgknr/zfld.htm",
    },
    {
        "id": 17,
        "name": "杨晓磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "云南泸西",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "泸西县人民政府",
        "source": "https://www.hhlx.gov.cn/zfxxgk/fdzdgknr/zfld.htm",
    },
    {
        "id": 18,
        "name": "全威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1993年",
        "birthplace": "云南墨江",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "泸西县人民政府",
        "source": "https://www.hhlx.gov.cn/zfxxgk/fdzdgknr/zfld.htm",
    },
    {
        "id": 19,
        "name": "朱林军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "云南石屏",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "泸西县公安局",
        "source": "https://www.hhlx.gov.cn/zfxxgk/fdzdgknr/zfld.htm",
    },
    {
        "id": 20,
        "name": "曹何华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长(挂职)",
        "current_org": "泸西县人民政府",
        "source": "https://www.hhlx.gov.cn/zfxxgk/fdzdgknr/zfld.htm",
    },
    {
        "id": 21,
        "name": "王家林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原县委书记（被调查）",
        "current_org": "",
        "source": "网易新闻报道(2021); 2021年接受纪律审查和监察调查",
    },
    {
        "id": 22,
        "name": "莫伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原县长",
        "current_org": "",
        "source": "媒体报道,与王家林同时期任职",
    },
]

# ── Organizations ────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共泸西县委", "type": "党委", "level": "县", "parent": "中共红河州委", "location": "泸西县"},
    {"id": 2, "name": "泸西县人民政府", "type": "政府", "level": "县", "parent": "红河州人民政府", "location": "泸西县"},
    {"id": 3, "name": "泸西县人大常委会", "type": "人大", "level": "县", "parent": "", "location": "泸西县"},
    {"id": 4, "name": "泸西县政协", "type": "政协", "level": "县", "parent": "", "location": "泸西县"},
    {"id": 5, "name": "泸西县纪委监委", "type": "党委", "level": "县", "parent": "", "location": "泸西县"},
    {"id": 6, "name": "泸西县公安局", "type": "政府", "level": "县", "parent": "泸西县人民政府", "location": "泸西县"},
    {"id": 7, "name": "红河州应急管理局", "type": "政府", "level": "州", "parent": "红河州人民政府", "location": "蒙自市"},
    {"id": 8, "name": "红河州安监局", "type": "政府", "level": "州", "parent": "红河州人民政府", "location": "蒙自市"},
    {"id": 9, "name": "个旧市人民政府", "type": "政府", "level": "县", "parent": "红河州人民政府", "location": "个旧市"},
    {"id": 10, "name": "红河州人民政府办公室", "type": "政府", "level": "州", "parent": "", "location": "蒙自市"},
    {"id": 11, "name": "中共个旧市委", "type": "党委", "level": "县", "parent": "中共红河州委", "location": "个旧市"},
]

# ── Positions ────────────────────────────────────────────────────────────
positions = [
    # 夏明
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2021", "end": "至今", "rank": "正处", "note": "2026年6月27日再次当选"},
    {"person_id": 1, "org_id": 7, "title": "红河州应急管理局局长", "start": "2019-01", "end": "2021-04", "rank": "正处", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "红河州安监局局长", "start": "2018-02", "end": "2019-01", "rank": "正处", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "红河州政府应急办专职副主任", "start": "", "end": "2018-02", "rank": "副处", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "红河州政府办秘书八科副科长、科长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "个旧市政府法制办副主任、市政府办副主任", "start": "", "end": "", "rank": "", "note": "早期履历"},
    {"person_id": 1, "org_id": 1, "title": "县委副书记", "start": "", "end": "", "rank": "副处", "note": "履历缺口，待查具体时间"},

    # 邓飚雷
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "", "end": "至今", "rank": "正处", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县人民政府党组书记", "start": "", "end": "至今", "rank": "", "note": ""},

    # 曾云梅
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "2024", "end": "至今", "rank": "副处", "note": "2024年6月公示拟任县委副书记"},
    {"person_id": 3, "org_id": 1, "title": "县委常委、组织部部长", "start": "", "end": "2024", "rank": "副处", "note": ""},

    # 燕斌
    {"person_id": 7, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "至今", "rank": "副处", "note": ""},

    # 朱林军
    {"person_id": 19, "org_id": 6, "title": "副县长、县公安局局长", "start": "", "end": "至今", "rank": "副处", "note": ""},

    # 朱进
    {"person_id": 14, "org_id": 2, "title": "县委常委、副县长(挂职)", "start": "", "end": "至今", "rank": "副处", "note": ""},

    # 殷丽萍
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处", "note": ""},
    # 李杨
    {"person_id": 16, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处", "note": ""},
    # 杨晓磊
    {"person_id": 17, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处", "note": ""},
    # 全威
    {"person_id": 18, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处", "note": ""},
    # 曹何华
    {"person_id": 20, "org_id": 2, "title": "副县长(挂职)", "start": "", "end": "至今", "rank": "副处", "note": ""},

    # 王家林 (前任书记)
    {"person_id": 21, "org_id": 1, "title": "县委书记", "start": "", "end": "2021", "rank": "正处", "note": "2021年接受调查"},
    # 莫伟 (前任县长)
    {"person_id": 22, "org_id": 2, "title": "县长", "start": "", "end": "2021", "rank": "正处", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭档", "overlap_org": "中共泸西县委/泸西县人民政府", "overlap_period": "2021-至今"},
    {"person_a": 3, "person_b": 1, "type": "superior_subordinate", "context": "县委副书记配合书记工作", "overlap_org": "中共泸西县委", "overlap_period": "2024-至今"},
    {"person_a": 7, "person_b": 1, "type": "superior_subordinate", "context": "常务副县长在县委领导下工作", "overlap_org": "中共泸西县委", "overlap_period": ""},
    {"person_a": 7, "person_b": 2, "type": "superior_subordinate", "context": "常务副县长协助县长工作", "overlap_org": "泸西县人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "县委副书记与常务副县长同为县委常委", "overlap_org": "中共泸西县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 21, "type": "predecessor_successor", "context": "夏明接替王家林任县委书记", "overlap_org": "中共泸西县委", "overlap_period": "2021"},
    {"person_a": 2, "person_b": 22, "type": "predecessor_successor", "context": "邓飚雷接替莫伟任县长", "overlap_org": "泸西县人民政府", "overlap_period": "2021"},
]

# ── Run ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    staging = Path(__file__).resolve().parent
    db_path = staging / f"{SLUG}_network.db"
    gexf_path = staging / f"{SLUG}_network.gexf"

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
    )
    print(f"✓ Database: {db_path}")
    print(f"✓ GEXF: {gexf_path}")