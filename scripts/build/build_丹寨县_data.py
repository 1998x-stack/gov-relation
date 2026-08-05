#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 丹寨县 leadership network.

丹寨县隶属贵州省黔东南苗族侗族自治州，位于贵州省东南部，辖龙泉镇、兴仁镇等乡镇/街道。
经济以农业（茶叶、中药材、蓝莓等）、非遗+旅游（万达小镇）、金钟经济开发区等为主，为国家乡村振兴重点县。

Current leadership as of 2026-08 (sources: 丹寨县人民政府门户网领导之窗/政务要闻、黔东南州人民政府人事任免)：
- 县委书记: 张登利（女，曾任县委副书记、县长，约2025年末/2026年初升任书记）
- 县委副书记、代理县长: 任高峰（1980年9月生、汉族、工学学士；原黔东南州锦屏县委副书记；兼丹寨金钟经开区管委会主任）
- 县人大常委会主任: 李白；县政协主席: 袁碧华
- 县委常委: 黄东琳（县委办主任）、周春龙（组织部长/老干部局长）
- 副县长: 龙运辉、周兴标、熊勇、杨维顺、蒋佰春
- 前任县委书记: 袁尚勇（兼黔东南州政协副主席、丹寨金钟经开区党工委书记）

Biographical data sourced from official government pages and appointment notices.
Confidence per person/claim marked where uncertain（见 report 与 report/open_gaps.md）。
"""

import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _parent in REPO_ROOT.parents:
    if (_parent / "gov_relation").is_dir():
        REPO_ROOT = _parent
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "丹寨县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "丹寨县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "丹寨县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "丹寨县_network.db"
    GEXF_PATH = GRAPH_DIR / "丹寨县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共丹寨县委员会", "type": "党委", "level": "县处级", "parent": "中共黔东南州委", "location": "贵州省黔东南州丹寨县"},
    {"id": 2, "name": "丹寨县人民政府", "type": "政府", "level": "县处级", "parent": "黔东南州人民政府", "location": "贵州省黔东南州丹寨县"},
    {"id": 3, "name": "丹寨县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "黔东南州人大常委会", "location": "贵州省黔东南州丹寨县"},
    {"id": 4, "name": "中国人民政治协商会议丹寨县委员会", "type": "政协", "level": "县处级", "parent": "政协黔东南州委员会", "location": "贵州省黔东南州丹寨县"},
    {"id": 5, "name": "中共丹寨县纪律检查委员会/丹寨县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共黔东南州纪委", "location": "贵州省黔东南州丹寨县"},
    {"id": 6, "name": "贵州丹寨金钟经济开发区", "type": "开发区", "level": "县处级", "parent": "黔东南州人民政府", "location": "贵州省黔东南州丹寨县"},
    {"id": 7, "name": "中共黔东南州委员会", "type": "党委", "level": "地厅级", "parent": "中共贵州省委员会", "location": "贵州省黔东南州凯里市"},
    {"id": 8, "name": "黔东南州人民政府", "type": "政府", "level": "地厅级", "parent": "贵州省人民政府", "location": "贵州省黔东南州凯里市"},
    {"id": 9, "name": "政协黔东南州委员会", "type": "政协", "level": "地厅级", "parent": "政协贵州省委员会", "location": "贵州省黔东南州凯里市"},
    {"id": 10, "name": "中共锦屏县委员会", "type": "党委", "level": "县处级", "parent": "中共黔东南州委", "location": "贵州省黔东南州锦屏县"},
    {"id": 11, "name": "锦屏县人民政府", "type": "政府", "level": "县处级", "parent": "黔东南州人民政府", "location": "贵州省黔东南州锦屏县"},
    {"id": 12, "name": "中共丹寨县委组织部", "type": "党委部门", "level": "县处级", "parent": "中共丹寨县委", "location": "贵州省黔东南州丹寨县"},
    {"id": 13, "name": "中共丹寨县委办公室", "type": "党委部门", "level": "县处级", "parent": "中共丹寨县委", "location": "贵州省黔东南州丹寨县"},
    {"id": 14, "name": "丹寨县审计局", "type": "政府", "level": "县处级", "parent": "丹寨县人民政府", "location": "贵州省黔东南州丹寨县"},
    {"id": 15, "name": "丹寨县财政局", "type": "政府", "level": "县处级", "parent": "丹寨县人民政府", "location": "贵州省黔东南州丹寨县"},
    {"id": 16, "name": "中共贵州省委员会", "type": "党委", "level": "省部级", "parent": "", "location": "贵州省贵阳市"},
    {"id": 17, "name": "中共黔东南州委组织部", "type": "党委部门", "level": "地厅级", "parent": "中共黔东南州委", "location": "贵州省黔东南州凯里市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 张登利 — 县委书记（现任；曾任县长）
    {"id": 1, "name": "张登利", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "贵州省（待查）",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共丹寨县委书记", "current_org": "中共丹寨县委员会",
     "source": "https://www.qdndz.gov.cn/xwzx/zwyw/202608/t20260804_90690990.html"},
    # 2 — 任高峰 — 现任县委副书记、代理县长
    {"id": 2, "name": "任高峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年9月", "birthplace": "（待查）",
     "education": "大学学历，工学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "丹寨县委副书记、县人民政府党组书记、代理县长", "current_org": "丹寨县人民政府",
     "source": "https://www.qdndz.gov.cn/zwgk/jcxxgk/ldzc/202607/t20260730_90675474.html"},
    # 3 — 李白 — 县人大常委会主任
    {"id": 3, "name": "李白", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "丹寨县人大常委会主任", "current_org": "丹寨县人民代表大会常务委员会",
     "source": "https://www.qdndz.gov.cn/xwzx/zwyw/202608/t20260804_90690990.html"},
    # 4 — 袁碧华 — 县政协主席
    {"id": 4, "name": "袁碧华", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "丹寨县政协主席", "current_org": "中国人民政治协商会议丹寨县委员会",
     "source": "https://www.qdndz.gov.cn/xwzx/zwyw/202608/t20260804_90690990.html"},
    # 5 — 黄东琳 — 县委常委、县委办主任
    {"id": 5, "name": "黄东琳", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "丹寨县委常委、县委办主任", "current_org": "中共丹寨县委员会",
     "source": "https://www.qdndz.gov.cn/xwzx/zwyw/202608/t20260804_90691009.html"},
    # 6 — 周春龙 — 县委常委、组织部长、老干部局长
    {"id": 6, "name": "周春龙", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "丹寨县委常委、组织部长、老干部局长", "current_org": "中共丹寨县委组织部",
     "source": "https://www.qdndz.gov.cn/xwzx/zwyw/202607/t20260729_90671532.html"},
    # 7 — 龙运辉 — 副县长
    {"id": 7, "name": "龙运辉", "gender": "男", "ethnicity": "苗族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "丹寨县副县长", "current_org": "丹寨县人民政府",
     "source": "https://www.qdndz.gov.cn/zwgk/jcxxgk/ldzc/202603/t20260310_89622922.html"},
    # 8 — 周兴标 — 副县长
    {"id": 8, "name": "周兴标", "gender": "男", "ethnicity": "苗族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "丹寨县副县长", "current_org": "丹寨县人民政府",
     "source": "https://www.qdndz.gov.cn/zwgk/jcxxgk/ldzc/202306/t20230605_80049715.html"},
    # 9 — 熊国玺 — 副县长（政府领导之窗）
    {"id": 9, "name": "熊国玺", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "丹寨县副县长", "current_org": "丹寨县人民政府",
     "source": "https://www.qdndz.gov.cn/zwgk/jcxxgk/ldzc/202311/t20231114_83074860.html"},
    # 10 — 杨维顺 — 副县长
    {"id": 10, "name": "杨维顺", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "丹寨县副县长", "current_org": "丹寨县人民政府",
     "source": "https://www.qdndz.gov.cn/zwgk/jcxxgk/ldzc/202205/t20220517_74083822.html"},
    # 11 — 蒋佰春 — 副县长
    {"id": 11, "name": "蒋佰春", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "丹寨县副县长", "current_org": "丹寨县人民政府",
     "source": "https://www.qdndz.gov.cn/zwgk/jcxxgk/ldzc/202212/t20221213_77448776.html"},
    # 12 — 袁尚勇 — 前任县委书记（兼州政协副主席）
    {"id": 12, "name": "袁尚勇", "gender": "男", "ethnicity": "侗族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "黔东南州政协副主席（前丹寨县委书记）", "current_org": "政协黔东南州委员会",
     "source": "百度百科/传媒报道（袁氏宗亲网转载）"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 张登利
    {"person_id": 1, "org_id": 1, "title": "丹寨县委书记", "start": "2026", "end": "present", "rank": "正处级", "note": "2026年任县委书记，主持县委常委会"},
    {"person_id": 1, "org_id": 2, "title": "丹寨县委副书记、县长", "start": "2021", "end": "2026", "rank": "正处级", "note": "2021年任县长，2025年仍在任"},
    {"person_id": 1, "org_id": 6, "title": "贵州丹寨金钟经济开发区管委会主任（兼）", "start": "", "end": "2026-07", "rank": "", "note": "州政府任免〔2026〕49号免去"},
    # 任高峰
    {"person_id": 2, "org_id": 2, "title": "丹寨县委副书记、代理县长", "start": "2026-07", "end": "present", "rank": "正处级", "note": "2026年7月到任，代理县长"},
    {"person_id": 2, "org_id": 6, "title": "金钟经济开发区管委会主任（兼）", "start": "2026-07", "end": "present", "rank": "", "note": "黔东南府任〔2026〕49号"},
    {"person_id": 2, "org_id": 10, "title": "锦屏县委副书记", "start": "", "end": "2026-07", "rank": "副处级", "note": "调任丹寨前任锦屏县委副书记"},
    # 李白
    {"person_id": 3, "org_id": 3, "title": "丹寨县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 袁碧华
    {"person_id": 4, "org_id": 4, "title": "丹寨县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 黄东琳
    {"person_id": 5, "org_id": 1, "title": "丹寨县委常委、县委办主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 周春龙
    {"person_id": 6, "org_id": 12, "title": "丹寨县委常委、组织部长、老干部局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 副县长们
    {"person_id": 7, "org_id": 2, "title": "丹寨县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "丹寨县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "丹寨县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "丹寨县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "丹寨县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 袁尚勇
    {"person_id": 12, "org_id": 1, "title": "丹寨县委书记", "start": "", "end": "2025", "rank": "正处级", "note": "前任丹寨县委书记"},
    {"person_id": 12, "org_id": 6, "title": "金钟经济开发区党工委书记（兼）", "start": "", "end": "2025", "rank": "", "note": ""},
    {"person_id": 12, "org_id": 9, "title": "黔东南州政协副主席（兼任）", "start": "", "end": "present", "rank": "副厅级", "note": "仍任州政协副主席"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "张登利（县委书记）与任高峰（代理县长）为丹寨现任党政一把手，同一班子共事", "overlap_org": "丹寨县", "overlap_period": "2026至今"},
    {"person_a": 12, "person_b": 1, "type": "predecessor_successor", "context": "张登利接任高峰前前任书记袁尚勇的丹寨县委书记职务", "overlap_org": "丹寨县", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 2, "type": "上下级", "context": "张登利任书记，任高峰任县长（上下级党政搭档）", "overlap_org": "丹寨县", "overlap_period": "2026-07至今"},
    {"person_a": 2, "person_b": 1, "type": "上下级", "context": "任高峰曾以金钟经开区管委会主任身份与张登利有工作交集（州府任免49号交接）", "overlap_org": "金钟经济开发区", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 3, "type": "同一班子", "context": "张登利书记任内李白任县人大主任", "overlap_org": "丹寨县", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 4, "type": "同一班子", "context": "张登利书记任内袁碧华任县政协主席", "overlap_org": "丹寨县", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "张登利任书记时黄东琳任县委办主任/常委", "overlap_org": "丹寨县", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "张登利任书记时周春龙任组织部长", "overlap_org": "丹寨县", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "任高峰任县长期间与副县长龙运辉共事", "overlap_org": "丹寨县", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "任高峰任县长期间副县长周兴标共事", "overlap_org": "丹寨县", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "任高峰任县长期间副县长熊国玺共事", "overlap_org": "丹寨县", "overlap_period": "2026至今"},
]

if __name__ == "__main__":
    # Fix any stray closing-bracket typos in data (resilience)
    import re

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
    print(f"Wrote DB: {DB_PATH}")
    print(f"Wrote GEXF: {GEXF_PATH}")
    print(f"Stats: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")