#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 武邑县 (Wuyi County) leadership network.

武邑县 is a county under 衡水市 (Hengshui), 河北省 (Hebei).
Current leadership as of 2026-07 per wyx.hengshui.gov.cn news articles.

Research sources:
- wyx.hengshui.gov.cn (武邑县人民政府网站): official news articles from 2026
- Sogou web search for previous leadership names

Research limitations:
- Exa search was rate-limited during this investigation.
- Baidu Baike returned 403 errors.
- Sogou search returned captcha after initial results.
- Biographical details for most figures limited to what appears in news articles.
- No full career timelines available from public web search.
"""

import sqlite3
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from gov_relation.runner import run_build

SLUG = "武邑县"
TASK_DIR = Path(__file__).parent.resolve()

DB_PATH = TASK_DIR / "武邑县_network.db"
GEXF_PATH = TASK_DIR / "武邑县_network.gexf"

# ── PERSONS ────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════════
    # CURRENT TOP LEADERS (confirmed from wyx.hengshui.gov.cn news, as of 2026-07)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "文健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共武邑县委书记",
        "current_org": "中共武邑县委员会",
        "source": "http://wyx.hengshui.gov.cn/art/2026/5/20/art_199_625646.html",
    },
    {
        "id": 2,
        "name": "李啸鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武邑县人民政府县长",
        "current_org": "武邑县人民政府",
        "source": "http://wyx.hengshui.gov.cn/art/2026/5/20/art_199_625646.html",
    },
    {
        "id": 3,
        "name": "刘威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共武邑县委副书记",
        "current_org": "中共武邑县委员会",
        "source": "http://wyx.hengshui.gov.cn/art/2026/5/20/art_199_625646.html",
    },

    # ═══════════════════════════════════════════════════════════════════
    # KEY DEPUTIES (confirmed from official news articles)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "王伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武邑县委常委、县委办公室主任",
        "current_org": "中共武邑县委员会",
        "source": "http://wyx.hengshui.gov.cn/art/2026/3/24/art_199_620195.html",
    },
    {
        "id": 5,
        "name": "李瑞祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武邑县人民政府副县长",
        "current_org": "武邑县人民政府",
        "source": "http://wyx.hengshui.gov.cn/art/2026/5/6/art_199_624094.html",
    },
    {
        "id": 6,
        "name": "侯会然",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武邑县领导",
        "current_org": "中共武邑县委员会",
        "source": "http://wyx.hengshui.gov.cn/art/2026/5/20/art_199_625646.html",
    },
    {
        "id": 7,
        "name": "冯晓光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武邑县领导",
        "current_org": "中共武邑县委员会",
        "source": "http://wyx.hengshui.gov.cn/art/2026/5/20/art_199_625646.html",
    },

    # ═══════════════════════════════════════════════════════════════════
    # 人大 & 政协 LEADERS
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 8,
        "name": "张百芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武邑县人大常委会主任",
        "current_org": "武邑县人民代表大会常务委员会",
        "source": "http://wyx.hengshui.gov.cn/art/2026/5/20/art_199_625646.html",
    },
    {
        "id": 9,
        "name": "赵磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武邑县政协主席",
        "current_org": "中国人民政治协商会议武邑县委员会",
        "source": "http://wyx.hengshui.gov.cn/art/2026/5/20/art_199_625646.html",
    },
    {
        "id": 10,
        "name": "张金雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武邑县人大常委会副主任",
        "current_org": "武邑县人民代表大会常务委员会",
        "source": "http://wyx.hengshui.gov.cn/art/2026/5/6/art_199_624094.html",
    },
    {
        "id": 11,
        "name": "谷世英",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武邑县人大常委会副主任",
        "current_org": "武邑县人民代表大会常务委员会",
        "source": "http://wyx.hengshui.gov.cn/art/2026/5/6/art_199_624094.html",
    },
    {
        "id": 12,
        "name": "常红根",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武邑县人大常委会副主任",
        "current_org": "武邑县人民代表大会常务委员会",
        "source": "http://wyx.hengshui.gov.cn/art/2026/5/6/art_199_624094.html",
    },

    # ═══════════════════════════════════════════════════════════════════
    # JUDICIARY
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 13,
        "name": "袁明辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武邑县人民检察院检察长",
        "current_org": "武邑县人民检察院",
        "source": "http://wyx.hengshui.gov.cn/art/2026/5/6/art_199_624094.html",
    },
    {
        "id": 14,
        "name": "刘茹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武邑县人民法院院长",
        "current_org": "武邑县人民法院",
        "source": "http://wyx.hengshui.gov.cn/art/2026/3/24/art_199_620195.html",
    },

    # ═══════════════════════════════════════════════════════════════════
    # PREDECESSORS
    # ═══════════════════════════════════════════════════════════════════
    # 耿伟平 — predecessor 县委书记 (succeeded by 文健)
    {
        "id": 15,
        "name": "耿伟平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任武邑县委书记）",
        "current_org": "",
        "source": "Sogou web search - 武邑县现任领导班子",
    },
    # 刘勇 — predecessor 县委书记 before 耿伟平
    {
        "id": 16,
        "name": "刘勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任武邑县委书记）",
        "current_org": "",
        "source": "Sogou web search - 武邑县委书记刘勇",
    },
    # 王桂冰 — predecessor 县长 (succeeded by 李啸鹏)
    {
        "id": 17,
        "name": "王桂冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任武邑县县长）",
        "current_org": "",
        "source": "Sogou web search - 王桂冰 武邑县长",
    },
    # 王成宗 — predecessor 县长 before 王桂冰
    {
        "id": 18,
        "name": "王成宗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任武邑县县长）",
        "current_org": "",
        "source": "Sogou web search - 武邑县县长任命",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共武邑县委员会", "type": "党委", "level": "县级", "location": "河北省衡水市武邑县"},
    {"id": 2, "name": "武邑县人民政府", "type": "政府", "level": "县级", "location": "河北省衡水市武邑县"},
    {"id": 3, "name": "武邑县人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "河北省衡水市武邑县"},
    {"id": 4, "name": "中国人民政治协商会议武邑县委员会", "type": "政协", "level": "县级", "location": "河北省衡水市武邑县"},
    {"id": 5, "name": "武邑县人民法院", "type": "事业单位", "level": "县级", "location": "河北省衡水市武邑县"},
    {"id": 6, "name": "武邑县人民检察院", "type": "事业单位", "level": "县级", "location": "河北省衡水市武邑县"},
    {"id": 7, "name": "中共衡水市委员会", "type": "党委", "level": "地级", "location": "河北省衡水市"},
    {"id": 8, "name": "衡水市人民政府", "type": "政府", "level": "地级", "location": "河北省衡水市"},
]

# ── POSITIONS ─────────────────────────────────────────────────────────

positions = [
    # 文健 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共武邑县委书记",
     "start": "", "end": "present", "rank": "正处级", "note": "现任（2026年3月-7月多次在新闻报道中出现）"},

    # 李啸鹏 — 县长
    {"person_id": 2, "org_id": 2, "title": "武邑县人民政府县长",
     "start": "", "end": "present", "rank": "正处级", "note": "现任（2026年5月20日县委理论学习中心组会议中出现）"},

    # 刘威 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "中共武邑县委副书记",
     "start": "", "end": "present", "rank": "副处级", "note": "现任"},

    # 王伟 — 县委常委、县委办公室主任
    {"person_id": 4, "org_id": 1, "title": "武邑县委常委、县委办公室主任",
     "start": "", "end": "present", "rank": "副处级", "note": "现任"},

    # 李瑞祥 — 副县长
    {"person_id": 5, "org_id": 2, "title": "武邑县人民政府副县长",
     "start": "", "end": "present", "rank": "副处级", "note": "现任"},

    # 侯会然 — 县领导
    {"person_id": 6, "org_id": 1, "title": "武邑县领导",
     "start": "", "end": "present", "rank": "副处级", "note": "现任，具体职务待确认"},

    # 冯晓光 — 县领导
    {"person_id": 7, "org_id": 1, "title": "武邑县领导",
     "start": "", "end": "present", "rank": "副处级", "note": "现任，具体职务待确认"},

    # 张百芳 — 人大主任
    {"person_id": 8, "org_id": 3, "title": "武邑县人大常委会主任",
     "start": "", "end": "present", "rank": "正处级", "note": "现任"},

    # 赵磊 — 政协主席
    {"person_id": 9, "org_id": 4, "title": "武邑县政协主席",
     "start": "", "end": "present", "rank": "正处级", "note": "现任"},

    # 张金雷 — 人大副主任
    {"person_id": 10, "org_id": 3, "title": "武邑县人大常委会副主任",
     "start": "", "end": "present", "rank": "副处级", "note": "现任"},

    # 谷世英 — 人大副主任
    {"person_id": 11, "org_id": 3, "title": "武邑县人大常委会副主任",
     "start": "", "end": "present", "rank": "副处级", "note": "现任"},

    # 常红根 — 人大副主任
    {"person_id": 12, "org_id": 3, "title": "武邑县人大常委会副主任",
     "start": "", "end": "present", "rank": "副处级", "note": "现任"},

    # 袁明辉 — 检察院检察长
    {"person_id": 13, "org_id": 6, "title": "武邑县人民检察院检察长",
     "start": "", "end": "present", "rank": "副处级", "note": "现任"},

    # 刘茹 — 法院院长
    {"person_id": 14, "org_id": 5, "title": "武邑县人民法院院长",
     "start": "", "end": "present", "rank": "副处级", "note": "现任"},

    # 耿伟平 — 前县委书记
    {"person_id": 15, "org_id": 1, "title": "中共武邑县委书记（前任）",
     "start": "", "end": "", "rank": "正处级", "note": "前任县委书记，后由文健接任"},

    # 刘勇 — 前前县委书记
    {"person_id": 16, "org_id": 1, "title": "中共武邑县委书记（前任）",
     "start": "", "end": "", "rank": "正处级", "note": "前任县委书记，后由耿伟平接任"},

    # 王桂冰 — 前县长
    {"person_id": 17, "org_id": 2, "title": "武邑县人民政府县长（前任）",
     "start": "", "end": "", "rank": "正处级", "note": "前任县长，后由李啸鹏接任"},

    # 王成宗 — 前前县长
    {"person_id": 18, "org_id": 2, "title": "武邑县人民政府县长（前任）",
     "start": "", "end": "", "rank": "正处级", "note": "前任县长，后由王桂冰接任"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────

relationships = [
    # 文健 ↔ 李啸鹏 (current partners in same county committee)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "武邑县委班子搭档，书记和县长",
        "overlap_org": "中共武邑县委员会/武邑县人民政府",
        "overlap_period": "2025/2026-至今",
    },
    # 文健 ↔ 刘威 (书记-副书记)
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "武邑县委班子，书记和副书记",
        "overlap_org": "中共武邑县委员会",
        "overlap_period": "2025/2026-至今",
    },
    # 文健 ↔ 王伟 (书记-县委办主任)
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "武邑县委班子，上下级关系",
        "overlap_org": "中共武邑县委员会",
        "overlap_period": "2025/2026-至今",
    },
    # 李啸鹏 ↔ 李瑞祥 (县长-副县长)
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "武邑县政府班子，县长和副县长",
        "overlap_org": "武邑县人民政府",
        "overlap_period": "2025/2026-至今",
    },
    # 文健 ↔ 张百芳 (县委-人大)
    {
        "person_a": 1, "person_b": 8,
        "type": "overlap",
        "context": "武邑县四套班子，县委书记和人大主任",
        "overlap_org": "中共武邑县委员会/武邑县人大",
        "overlap_period": "2025/2026-至今",
    },
    # 文健 ↔ 赵磊 (县委-政协)
    {
        "person_a": 1, "person_b": 9,
        "type": "overlap",
        "context": "武邑县四套班子，县委书记和政协主席",
        "overlap_org": "中共武邑县委员会/武邑县政协",
        "overlap_period": "2025/2026-至今",
    },
    # 耿伟平 → 文健 (predecessor-successor, 县委书记)
    {
        "person_a": 15, "person_b": 1,
        "type": "predecessor_successor",
        "context": "耿伟平卸任武邑县委书记后由文健接任",
        "overlap_org": "中共武邑县委员会",
        "overlap_period": "",
    },
    # 刘勇 → 耿伟平 (predecessor-successor, 县委书记)
    {
        "person_a": 16, "person_b": 15,
        "type": "predecessor_successor",
        "context": "刘勇卸任武邑县委书记后由耿伟平接任",
        "overlap_org": "中共武邑县委员会",
        "overlap_period": "",
    },
    # 王桂冰 → 李啸鹏 (predecessor-successor, 县长)
    {
        "person_a": 17, "person_b": 2,
        "type": "predecessor_successor",
        "context": "王桂冰卸任武邑县长后由李啸鹏接任",
        "overlap_org": "武邑县人民政府",
        "overlap_period": "",
    },
    # 王成宗 → 王桂冰 (predecessor-successor, 县长)
    {
        "person_a": 18, "person_b": 17,
        "type": "predecessor_successor",
        "context": "王成宗卸任武邑县长后由王桂冰接任",
        "overlap_org": "武邑县人民政府",
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
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )
    print(f"\nDone. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
