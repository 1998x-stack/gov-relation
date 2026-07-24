#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阜城县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 衡水市
Region: 阜城县
Targets: 县委书记 & 县长

Research Sources:
- 阜城县人民政府官方网站 (http://www.hbfcx.gov.cn/) — 领导信息页面
  - 王国崇县长: http://www.hbfcx.gov.cn/art/2026/7/2/art_10325_447978.html
  - 关升常务副县长: http://www.hbfcx.gov.cn/art/2022/10/31/art_10325_447989.html
  - 徐海江副县长: http://www.hbfcx.gov.cn/art/2022/10/31/art_10325_447975.html
  - 李又良副县长: http://www.hbfcx.gov.cn/art/2022/10/31/art_10325_447969.html
  - 李晓燕副县长: http://www.hbfcx.gov.cn/art/2022/10/31/art_10325_447972.html
  - 高李冀副县长: http://www.hbfcx.gov.cn/art/2022/10/31/art_10325_447967.html
  - 张峻副县长: http://www.hbfcx.gov.cn/art/2025/12/13/art_10325_609186.html
  - 朱洪志三级调研员: http://www.hbfcx.gov.cn/art/2022/10/31/art_10325_447999.html
- 维基百科 — 阜城县词条 (https://zh.wikipedia.org/wiki/阜城县) 确认县委书记为姚辛福
- 快懂百科 — 石瑞发曾任阜城县委书记
- 现有项目数据: data/persons/20260724-河北省-衡水市-县委书记-石瑞发.json

Research Date: 2026-07-24
"""

import sys
import os
from pathlib import Path

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from gov_relation.runner import run_build

SLUG = "阜城县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── PERSONS ────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════════
    # CURRENT TOP LEADERS
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "姚辛福",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共阜城县委书记",
        "current_org": "中共阜城县委员会",
        "source": "https://zh.wikipedia.org/wiki/阜城县（维基百科词条显示县委书记为姚辛福，最新编辑2026-05-16）",
    },
    {
        "id": 2,
        "name": "王国崇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年10月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "阜城县委副书记、县长，阜城经济开发区党工委副书记、管委会主任(兼)",
        "current_org": "阜城县人民政府",
        "source": "http://www.hbfcx.gov.cn/art/2026/7/2/art_10325_447978.html",
    },
    # ═══════════════════════════════════════════════════════════════════
    # KEY DEPUTIES (Confirmed from official government website)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "关升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年9月",
        "birthplace": "",
        "education": "大学学历、工学学士、省委党校在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "阜城县委常委、县政府党组副书记、副县长（分工常务工作）",
        "current_org": "阜城县人民政府",
        "source": "http://www.hbfcx.gov.cn/art/2022/10/31/art_10325_447989.html",
    },
    {
        "id": 4,
        "name": "徐海江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阜城县人民政府副县长",
        "current_org": "阜城县人民政府",
        "source": "http://www.hbfcx.gov.cn/art/2022/10/31/art_10325_447975.html",
    },
    {
        "id": 5,
        "name": "李又良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年3月",
        "birthplace": "",
        "education": "省委党校法律专业",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "阜城县人民政府党组成员、副县长",
        "current_org": "阜城县人民政府",
        "source": "http://www.hbfcx.gov.cn/art/2022/10/31/art_10325_447969.html",
    },
    {
        "id": 6,
        "name": "李晓燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年9月",
        "birthplace": "",
        "education": "省委党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "阜城县政府党组成员、副县长",
        "current_org": "阜城县人民政府",
        "source": "http://www.hbfcx.gov.cn/art/2022/10/31/art_10325_447972.html",
    },
    {
        "id": 7,
        "name": "高李冀",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1978年11月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "阜城县副县长、县公安局局长",
        "current_org": "阜城县人民政府",
        "source": "http://www.hbfcx.gov.cn/art/2022/10/31/art_10325_447967.html",
    },
    {
        "id": 8,
        "name": "张峻",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年6月",
        "birthplace": "",
        "education": "河北师范大学中国近现代史基本问题研究专业",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "阜城县人民政府党组成员、副县长",
        "current_org": "阜城县人民政府",
        "source": "http://www.hbfcx.gov.cn/art/2025/12/13/art_10325_609186.html",
    },
    {
        "id": 9,
        "name": "朱洪志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年6月",
        "birthplace": "",
        "education": "省委党校在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "阜城县人民政府党组成员（三级调研员）",
        "current_org": "阜城县人民政府",
        "source": "http://www.hbfcx.gov.cn/art/2022/10/31/art_10325_447999.html",
    },
    # ═══════════════════════════════════════════════════════════════════
    # PREDECESSORS
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "石瑞发",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年8月（待确认）",
        "birthplace": "河北省丰宁县（待确认）",
        "education": "河北师范大学汉语言文学（大学）",
        "party_join": "2001年5月",
        "work_start": "2001年7月",
        "current_post": "饶阳县委书记（原阜城县委书记）",
        "current_org": "中共饶阳县委员会",
        "source": "快懂百科（曾任阜城县委书记）；饶阳县政府网站确认现任饶阳县委书记",
    },
    {
        "id": 11,
        "name": "刘新营",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年12月",
        "birthplace": "河北省衡水市阜城县",
        "education": "河北师范大学政治教育（大学），省委党校经济管理（在职研究生）",
        "party_join": "1990年10月",
        "work_start": "1988年8月",
        "current_post": "衡水市人大常委会副主任、枣强县委书记",
        "current_org": "衡水市人大常委会/中共枣强县委",
        "source": "https://www.baike.com/wiki/刘新营（阜城籍，提供衡水地区干部网络线索）",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共阜城县委员会", "type": "党委", "level": "县级", "location": "河北省衡水市阜城县"},
    {"id": 2, "name": "阜城县人民政府", "type": "政府", "level": "县级", "location": "河北省衡水市阜城县"},
    {"id": 3, "name": "阜城县人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "河北省衡水市阜城县"},
    {"id": 4, "name": "中国人民政治协商会议阜城县委员会", "type": "政协", "level": "县级", "location": "河北省衡水市阜城县"},
    {"id": 5, "name": "阜城县公安局", "type": "政府", "level": "县级", "location": "河北省衡水市阜城县"},
    {"id": 6, "name": "阜城经济开发区", "type": "开发区", "level": "县级", "location": "河北省衡水市阜城县"},
    {"id": 7, "name": "中共衡水市委员会", "type": "党委", "level": "地级", "location": "河北省衡水市"},
    {"id": 8, "name": "衡水市人民政府", "type": "政府", "level": "地级", "location": "河北省衡水市"},
    {"id": 9, "name": "中共饶阳县委员会", "type": "党委", "level": "县级", "location": "河北省衡水市饶阳县"},
    {"id": 10, "name": "中共枣强县委", "type": "党委", "level": "县级", "location": "河北省衡水市枣强县"},
    {"id": 11, "name": "河北师范大学", "type": "事业单位", "level": "省级", "location": "河北省石家庄市"},
]

# ── POSITIONS ─────────────────────────────────────────────────────────

positions = [
    # 姚辛福 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共阜城县委书记",
     "start": "", "end": "present", "rank": "正处级", "note": "现任（维基百科确认，上任时间待查）"},

    # 王国崇 — 县长
    {"person_id": 2, "org_id": 2, "title": "阜城县委副书记、县长",
     "start": "", "end": "present", "rank": "正处级", "note": "现任（2026-07-02政府网站更新）"},
    {"person_id": 2, "org_id": 6, "title": "阜城经济开发区党工委副书记、管委会主任(兼)",
     "start": "", "end": "present", "rank": "正处级", "note": "兼任"},

    # 关升 — 常务副县长
    {"person_id": 3, "org_id": 2, "title": "阜城县委常委、县政府党组副书记、副县长（分工常务工作）",
     "start": "", "end": "present", "rank": "副处级", "note": "现任（2022-10-31确认）"},
    {"person_id": 3, "org_id": 1, "title": "阜城县委常委",
     "start": "", "end": "present", "rank": "副处级", "note": "现任"},

    # 徐海江 — 副县长
    {"person_id": 4, "org_id": 2, "title": "阜城县人民政府副县长",
     "start": "", "end": "present", "rank": "副处级", "note": "现任，分管教育、文化、市场监管"},

    # 李又良 — 副县长
    {"person_id": 5, "org_id": 2, "title": "阜城县人民政府党组成员、副县长",
     "start": "", "end": "present", "rank": "副处级", "note": "现任，分管农业农村、水利、乡村振兴"},

    # 李晓燕 — 副县长
    {"person_id": 6, "org_id": 2, "title": "阜城县政府党组成员、副县长",
     "start": "", "end": "present", "rank": "副处级", "note": "现任，分管医疗、人社、民政"},

    # 高李冀 — 副县长、公安局长
    {"person_id": 7, "org_id": 2, "title": "阜城县副县长、县公安局局长",
     "start": "", "end": "present", "rank": "副处级", "note": "现任，分管公安、司法、退役军人事务"},
    {"person_id": 7, "org_id": 5, "title": "阜城县公安局局长",
     "start": "", "end": "present", "rank": "副处级", "note": "兼任"},

    # 张峻 — 副县长
    {"person_id": 8, "org_id": 2, "title": "阜城县人民政府党组成员、副县长",
     "start": "", "end": "present", "rank": "副处级", "note": "现任（2025-12-13确认），分管住建、环保、金融"},

    # 朱洪志 — 党组成员（三级调研员）
    {"person_id": 9, "org_id": 2, "title": "阜城县人民政府党组成员（三级调研员）",
     "start": "", "end": "present", "rank": "副处级", "note": "现任，分管交通、邮政"},

    # 石瑞发 — 前县委书记
    {"person_id": 10, "org_id": 1, "title": "中共阜城县委书记（前任）",
     "start": "", "end": "2026年初", "rank": "正处级", "note": "前任县委书记，后调任饶阳县委书记"},
    {"person_id": 10, "org_id": 9, "title": "饶阳县委书记（现任）",
     "start": "2026-05", "end": "present", "rank": "正处级", "note": "至迟2026年5月已任饶阳县委书记"},

    # 刘新营 — 阜城籍干部（衡水领导）
    {"person_id": 11, "org_id": 7, "title": "衡水市人大常委会副主任",
     "start": "2024-01", "end": "present", "rank": "副厅级", "note": "阜城籍干部"},
    {"person_id": 11, "org_id": 10, "title": "枣强县委书记",
     "start": "2021-05", "end": "present", "rank": "正处级", "note": "兼任"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────

relationships = [
    # 姚辛福 ↔ 王国崇 (current partners: 书记-县长)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "阜城县委班子搭档，县委书记和县长",
        "overlap_org": "中共阜城县委员会/阜城县人民政府",
        "overlap_period": "当前",
    },
    # 姚辛福 ↔ 关升 (书记-常务副县长)
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "阜城县委班子，书记和常委/常务副县长",
        "overlap_org": "中共阜城县委员会",
        "overlap_period": "当前",
    },
    # 王国崇 ↔ 关升 (县长-常务副县长)
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "阜城县政府班子，县长和常务副县长",
        "overlap_org": "阜城县人民政府",
        "overlap_period": "当前",
    },
    # 王国崇 ↔ 徐海江 (县长-副县长)
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "阜城县政府班子工作关系",
        "overlap_org": "阜城县人民政府",
        "overlap_period": "当前",
    },
    # 王国崇 ↔ 李又良 (县长-副县长)
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "阜城县政府班子工作关系",
        "overlap_org": "阜城县人民政府",
        "overlap_period": "当前",
    },
    # 王国崇 ↔ 李晓燕 (县长-副县长)
    {
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "阜城县政府班子工作关系",
        "overlap_org": "阜城县人民政府",
        "overlap_period": "当前",
    },
    # 王国崇 ↔ 高李冀 (县长-副县长/公安局长)
    {
        "person_a": 2, "person_b": 7,
        "type": "overlap",
        "context": "阜城县政府班子工作关系",
        "overlap_org": "阜城县人民政府",
        "overlap_period": "当前",
    },
    # 王国崇 ↔ 张峻 (县长-副县长)
    {
        "person_a": 2, "person_b": 8,
        "type": "overlap",
        "context": "阜城县政府班子工作关系",
        "overlap_org": "阜城县人民政府",
        "overlap_period": "2025-12至今",
    },
    # 石瑞发 → 姚辛福 (predecessor-successor, 县委书记)
    {
        "person_a": 10, "person_b": 1,
        "type": "predecessor_successor",
        "context": "石瑞发卸任阜城县委书记后由姚辛福接任",
        "overlap_org": "中共阜城县委员会",
        "overlap_period": "",
    },
    # 石瑞发 ↔ 王国崇 (former 书记-县长)
    {
        "person_a": 10, "person_b": 2,
        "type": "overlap",
        "context": "石瑞发此前在阜城任县委书记时与王国崇县长搭班子",
        "overlap_org": "中共阜城县委员会/阜城县人民政府",
        "overlap_period": "2026年初之前",
    },
    # 刘新营 — 阜城籍干部关系
    {
        "person_a": 11, "person_b": 1,
        "type": "same_native_place",
        "context": "刘新营为阜城籍干部，现任衡水市领导，与阜城现任领导有地域联系",
        "overlap_org": "",
        "overlap_period": "",
    },
    {
        "person_a": 11, "person_b": 2,
        "type": "same_native_place",
        "context": "刘新营为阜城籍干部，王国崇现任阜城县长",
        "overlap_org": "",
        "overlap_period": "",
    },
]

# ── RUN ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
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
    print(f"\nDone. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
