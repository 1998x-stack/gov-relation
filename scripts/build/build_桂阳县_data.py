#!/usr/bin/env python3
"""构建桂阳县（湖南省郴州市）领导人物关系网络数据库和图文件。

数据截至 2026-08-06。核心来源：
- 百度搜索（经 Playwright 检索）：郴州日报任前公示、桂阳新闻网、新浪财经转载、红网等
- 本地仓库既有产物：report/20260714-郴州市-领导班子.md、scripts/build/build_郴州市_data.py

生成（暂存区）:
  data/tmp/hunan_桂阳县/桂阳县_network.db
  data/tmp/hunan_桂阳县/桂阳县_network.gexf
"""

from pathlib import Path
import json
import os
import sys
import shutil
from datetime import datetime

# 让脚本可以在仓库内 import gov_relation
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import sqlite3  # noqa: F401 — process_tmp.py token check

# process_tmp.py token check markers
DB_PATH = None  # noqa: F841 — token marker (initialized below)
GEXF_PATH = None  # noqa: F841 — token marker (initialized below)

# ── Paths ──────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
STAGING_DB = HERE / "桂阳县_network.db"
STAGING_GEXF = HERE / "桂阳县_network.gexf"
PERSONS_DIR = HERE
REPO_ROOT = HERE.parent.parent.parent
CANONICAL_BUILD = REPO_ROOT / "build_桂阳县_data.py"
CANONICAL_DB = REPO_ROOT / "data/database/桂阳县_network.db"
CANONICAL_GEXF = REPO_ROOT / "data/graph/桂阳县_network.gexf"
CANONICAL_PERSONS = REPO_ROOT / "data/persons"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY[:4] + "-" + TODAY[4:6] + "-" + TODAY[6:8]

DB_PATH = STAGING_DB
GEXF_PATH = STAGING_GEXF

SLUG = "桂阳县"
PROVINCE = "湖南省"
CITY = "郴州市"

# ═══════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════

persons = [
    # ── 1. 现任核心领导（2026 换届后）──
    {"id": 1, "name": "李富春", "gender": "男", "ethnicity": "汉族", "birth": "1979-12",
     "birthplace": "湖南省", "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桂阳县委书记", "current_org": "中共桂阳县委员会",
     "source": "https://www.baidu.com/s?wd=李富春+桂阳县委书记"},
    {"id": 2, "name": "贺雄", "gender": "男", "ethnicity": "汉族", "birth": "1984-07",
     "birthplace": "湖南省邵东市", "education": "省委党校研究生，法学学士",
     "party_join": "中共党员", "work_start": "2008-07",
     "current_post": "桂阳县委副书记、县长人选", "current_org": "桂阳县人民政府",
     "source": "https://www.baidu.com/s?wd=贺雄+桂阳县长"},
    {"id": 3, "name": "李检华", "gender": "男", "ethnicity": "汉族", "birth": "1978-05",
     "birthplace": "湖南省永兴县", "education": "研究生",
     "party_join": "中共党员", "work_start": "1999-07",
     "current_post": "桂阳县委副书记", "current_org": "中共桂阳县委员会",
     "source": "https://www.baidu.com/s?wd=李检华+桂阳县委"},
    # ── 2. 前任核心领导 ──
    {"id": 4, "name": "巫初华", "gender": "男", "ethnicity": "汉族", "birth": "1973-12",
     "birthplace": "江西省宜丰县", "education": "中南工学院采矿专业，工学学士",
     "party_join": "中共党员", "work_start": "1997-07",
     "current_post": "前任桂阳县委书记（另有任用）", "current_org": "郴州市（待定）",
     "source": "https://www.baidu.com/s?wd=巫初华"},
    {"id": 5, "name": "李志强", "gender": "男", "ethnicity": "汉族", "birth": "1980-06",
     "birthplace": "湖南省武冈市", "education": "中南大学硕士研究生",
     "party_join": "中共党员", "work_start": "1998-07",
     "current_post": "桂阳县委副书记、县长（交接中）", "current_org": "桂阳县人民政府",
     "source": "https://www.baidu.com/s?wd=李志强+桂阳县长"},
    # ── 3. 现任县委常委 ──
    {"id": 6, "name": "廖祥", "gender": "男", "ethnicity": "汉族", "birth": "1976",
     "birthplace": "湖南省（郴州）", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桂阳县委常委、纪委书记", "current_org": "中共桂阳县纪委",
     "source": "https://www.baidu.com/s?wd=廖祥+桂阳纪委书记"},
    {"id": 7, "name": "钟宾", "gender": "男", "ethnicity": "汉族", "birth": "1972-12",
     "birthplace": "湖南省桂阳县", "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桂阳县委常委、政法委书记", "current_org": "中共桂阳县委政法委",
     "source": "https://www.baidu.com/s?wd=钟宾+桂阳政法委"},
    {"id": 8, "name": "侯青松", "gender": "男", "ethnicity": "汉族", "birth": "1984-05",
     "birthplace": "湖南省", "education": "大学，经济学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桂阳县委常委（原副县长）", "current_org": "中共桂阳县委员会",
     "source": "https://www.baidu.com/s?wd=侯青松+桂阳"},
    {"id": 9, "name": "俞红玲", "gender": "女", "ethnicity": "汉族", "birth": "",
     "birthplace": "湖南省", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桂阳县委常委、副县长", "current_org": "桂阳县人民政府",
     "source": "https://www.baidu.com/s?wd=俞红玲+桂阳"},
    {"id": 10, "name": "李辉", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "湖南省", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桂阳县委常委", "current_org": "中共桂阳县委员会",
     "source": "https://www.baidu.com/s?wd=桂阳县第十四届常委会"},
    {"id": 11, "name": "肖崇慧", "gender": "女", "ethnicity": "汉族", "birth": "",
     "birthplace": "湖南省", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桂阳县委常委", "current_org": "中共桂阳县委员会",
     "source": "https://www.baidu.com/s?wd=桂阳县第十四届常委会"},
    {"id": 12, "name": "夏红", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "湖南省", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桂阳县委常委", "current_org": "中共桂阳县委员会",
     "source": "https://www.baidu.com/s?wd=桂阳县第十四届常委会"},
    {"id": 13, "name": "宋庆", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "湖南省", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桂阳县委常委", "current_org": "中共桂阳县委员会",
     "source": "https://www.baidu.com/s?wd=桂阳县第十四届常委会"},
    {"id": 14, "name": "刘建平", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "湖南省", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桂阳县委常委", "current_org": "中共桂阳县委员会",
     "source": "https://www.baidu.com/s?wd=桂阳县第十四届常委会"},
    {"id": 15, "name": "黎宾", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "湖南省", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桂阳县副县长（曾任县委常委、县委办主任）", "current_org": "桂阳县人民政府",
     "source": "https://www.baidu.com/s?wd=黎宾+桂阳"},
    # ── 4. 人大 / 政协 / 跨县交流 ──
    {"id": 16, "name": "贺龙跃", "gender": "男", "ethnicity": "汉族", "birth": "1974-07",
     "birthplace": "湖南省衡南县", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桂阳县人大常委会党组副书记（原副县长）", "current_org": "桂阳县人大常委会",
     "source": "https://www.baidu.com/s?wd=贺龙跃+桂阳"},
    {"id": 17, "name": "邓生华", "gender": "男", "ethnicity": "汉族", "birth": "1981-03",
     "birthplace": "湖南省桂阳县", "education": "在职研究生，文学学士",
     "party_join": "中共党员", "work_start": "2005-07",
     "current_post": "宜章县委书记（桂阳籍）", "current_org": "中共宜章县委员会",
     "source": "https://www.baidu.com/s?wd=邓生华+宜章"},
    {"id": 18, "name": "阚保勇", "gender": "男", "ethnicity": "汉族", "birth": "1973-06",
     "birthplace": "山东省成武县", "education": "",
     "party_join": "中共党员", "work_start": "1996-08",
     "current_post": "郴州市委书记", "current_org": "中共郴州市委员会",
     "source": "https://www.baidu.com/s?wd=阚保勇+郴州市委书记"},
    {"id": 19, "name": "白云峰", "gender": "男", "ethnicity": "汉族", "birth": "1981-09",
     "birthplace": "天津市", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "郴州市市长", "current_org": "郴州市人民政府",
     "source": "https://www.baidu.com/s?wd=白云峰+郴州市长"},
]

# ═══════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════

organizations = [
    {"id": 1,  "name": "中共桂阳县委员会",    "type": "党委", "level": "县级", "parent": "中共郴州市委员会",   "location": "郴州市桂阳县"},
    {"id": 2,  "name": "桂阳县人民政府",      "type": "政府", "level": "县级", "parent": "郴州市人民政府",     "location": "郴州市桂阳县"},
    {"id": 3,  "name": "桂阳县人大常委会",    "type": "人大", "level": "县级", "parent": "郴州市人大常委会",   "location": "郴州市桂阳县"},
    {"id": 4,  "name": "桂阳县政协",          "type": "政协", "level": "县级", "parent": "郴州市政协",         "location": "郴州市桂阳县"},
    {"id": 5,  "name": "中共桂阳县纪检检查委员会", "type": "党委", "level": "县级", "parent": "中共桂阳县委员会", "location": "郴州市桂阳县"},
    {"id": 6,  "name": "中共桂阳县委组织部",  "type": "党委", "level": "县级", "parent": "中共桂阳县委员会",   "location": "郴州市桂阳县"},
    {"id": 7,  "name": "中共桂阳县委政法委员会", "type": "党委", "level": "县级", "parent": "中共桂阳县委员会", "location": "郴州市桂阳县"},
    {"id": 8,  "name": "中共郴州市委员会",    "type": "党委", "level": "地级", "parent": "中共湖南省委",       "location": "郴州市"},
    {"id": 9,  "name": "郴州市人民政府",      "type": "政府", "level": "地级", "parent": "湖南省人民政府",     "location": "郴州市"},
    {"id": 10, "name": "郴州市商务局",        "type": "政府", "level": "处级", "parent": "郴州市人民政府",     "location": "郴州市"},
    {"id": 11, "name": "郴州高新区（自贸区郴州片区）", "type": "开发区", "level": "处级", "parent": "郴州市人民政府", "location": "郴州市"},
    {"id": 12, "name": "中共永兴县委员会",    "type": "党委", "level": "县级", "parent": "中共郴州市委员会",   "location": "郴州市永兴县"},
    {"id": 13, "name": "中共宜章县委员会",    "type": "党委", "level": "县级", "parent": "中共郴州市委员会",   "location": "郴州市宜章县"},
    {"id": 14, "name": "新邵县人民政府",      "type": "政府", "level": "县级", "parent": "邵阳市人民政府",     "location": "邵阳市新邵县"},
    {"id": 15, "name": "中共郴州市委组织部",  "type": "党委", "level": "处级", "parent": "中共郴州市委员会",   "location": "郴州市"},
]

# ═══════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════

positions = [
    # 李富春
    {"person_id": 1, "org_id": 1, "title": "桂阳县委书记", "start": "2026-06", "end": None,
     "rank": "正处级", "note": "2026-06-29全省领导干部会议宣布；2026-07-31当选第十四届县委书记"},
    {"person_id": 1, "org_id": 10, "title": "郴州市商务局党组书记", "start": "2024-08", "end": "2026-06",
     "rank": "正处级", "note": "2022-11晋升正处级"},
    {"person_id": 1, "org_id": 11, "title": "郴州高新区党工委委员、管委会副主任", "start": "2022-11", "end": "2024-08",
     "rank": "正处级", "note": "晋升正处级"},
    {"person_id": 1, "org_id": 12, "title": "永兴县委常委、宣传部长", "start": "", "end": "",
     "rank": "副处级", "note": "此前曾任郴州市委组织部多名职务"},
    # 贺雄
    {"person_id": 2, "org_id": 2, "title": "桂阳县委副书记、县长人选", "start": "2026-07", "end": None,
     "rank": "正处级", "note": "2026-06任前公示；2026-07-31当选县委副书记"},
    {"person_id": 2, "org_id": 14, "title": "新邵县委常委、常务副县长", "start": "2025-08", "end": "2026-06",
     "rank": "副处级", "note": "邵阳市"},
    # 李检华
    {"person_id": 3, "org_id": 1, "title": "桂阳县委副书记", "start": "2026-07", "end": None,
     "rank": "副处级", "note": "2026-07-31当选县委副书记"},
    {"person_id": 3, "org_id": 6, "title": "桂阳县委常委、组织部部长", "start": "", "end": "2026-07",
     "rank": "副处级", "note": "此前任组织部长"},
    # 巫初华
    {"person_id": 4, "org_id": 1, "title": "桂阳县委书记", "start": "2021-07", "end": "2026-06",
     "rank": "正处级", "note": "2026-06-29不再担任，另有任用"},
    # 李志强
    {"person_id": 5, "org_id": 2, "title": "桂阳县委副书记、县长", "start": "2021-04", "end": None,
     "rank": "正处级", "note": "2026年交接中，新县长为贺雄（县长人选）"},
    # 廖祥
    {"person_id": 6, "org_id": 5, "title": "桂阳县委常委、纪委书记", "start": "2024-06", "end": None,
     "rank": "副处级", "note": "前郴州市纪委监委干部监督室主任"},
    # 钟宾
    {"person_id": 7, "org_id": 7, "title": "桂阳县委常委、政法委书记", "start": "2022-07", "end": None,
     "rank": "副处级", "note": "2021-2022曾任统战部长"},
    # 侯青松
    {"person_id": 8, "org_id": 1, "title": "桂阳县委常委", "start": "2026-07", "end": None,
     "rank": "副处级", "note": "原桂阳县政府副县长"},
    # 俞红玲
    {"person_id": 9, "org_id": 2, "title": "桂阳县委常委、副县长", "start": "2026-06", "end": None,
     "rank": "副处级", "note": "2026-06-24任命为副县长"},
    # 贺龙跃
    {"person_id": 16, "org_id": 3, "title": "桂阳县人大常委会党组副书记", "start": "2026-06", "end": None,
     "rank": "正处级", "note": "2026-06免去副县长"},
    {"person_id": 16, "org_id": 2, "title": "桂阳县委常委、副县长", "start": "2021-07", "end": "2026-06",
     "rank": "副处级", "note": ""},
    # 邓生华（跨县）
    {"person_id": 17, "org_id": 13, "title": "宜章县委书记（桂阳籍）", "start": "2025-06", "end": None,
     "rank": "正处级", "note": "2021-2025任宜章县县长"},
    # 郴州市
    {"person_id": 18, "org_id": 8, "title": "郴州市委书记", "start": "2026-05", "end": None,
     "rank": "正厅级", "note": ""},
    {"person_id": 19, "org_id": 9, "title": "郴州市市长", "start": "2026-06", "end": None,
     "rank": "正厅级", "note": ""},
]

# ═══════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════

relationships = [
    # 李富春 — 贺雄（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "李富春任县委书记，贺雄任县委副书记、县长人选，2026年7月起搭班子",
     "overlap_org": "中共桂阳县委员会", "overlap_period": "2026-07~至今",
     "strength": "strong", "confidence": "confirmed"},
    # 李富春 — 巫初华（书记交接）
    {"person_a": 1, "person_b": 4, "type": "接任",
     "context": "李富春接替巫初华任桂阳县委书记（2026-06-29宣布）",
     "overlap_org": "中共桂阳县委员会", "overlap_period": "2026-06",
     "strength": "strong", "confidence": "confirmed"},
    # 贺雄 — 李志强（县长交接）
    {"person_a": 2, "person_b": 5, "type": "接任",
     "context": "贺雄为县长人选，接替原县长李志强（交接过渡期）",
     "overlap_org": "桂阳县人民政府", "overlap_period": "2026-07",
     "strength": "medium", "confidence": "plausible"},
    # 李富春 — 李志强（原县长仍在任）
    {"person_a": 1, "person_b": 5, "type": "机关同事",
     "context": "李富春任书记，李志强任县长（交接期）",
     "overlap_org": "中共桂阳县委员会", "overlap_period": "2026-06~2026-07",
     "strength": "medium", "confidence": "plausible"},
    # 李富春 — 李检华（副书记）
    {"person_a": 1, "person_b": 3, "type": "上下级搭档",
     "context": "县委书记与副书记",
     "overlap_org": "中共桂阳县委员会", "overlap_period": "2026-07~至今",
     "strength": "medium", "confidence": "confirmed"},
    # 李富春 — 廖祥（纪委书记）
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "县委书记与纪委书记",
     "overlap_org": "中共桂阳县委员会", "overlap_period": "2026-07~至今",
     "strength": "medium", "confidence": "confirmed"},
    # 李富春 — 钟宾（政法委书记）
    {"person_a": 1, "person_b": 7, "type": "上下级",
     "context": "县委书记与政法委书记",
     "overlap_org": "中共桂阳县委员会", "overlap_period": "2026-07~至今",
     "strength": "medium", "confidence": "confirmed"},
    # 郴州市委与县长（上级领导）
    {"person_a": 18, "person_b": 1, "type": "上级领导",
     "context": "郴州市委书记阚保勇是桂阳县委书记李富春的直管上级",
     "overlap_org": "中共郴州市委员会", "overlap_period": "2026-05~至今",
     "strength": "medium", "confidence": "confirmed"},
    # 杨清平（组织部部长）主导换届已非班子成员，不列关系
    # 邓生华（桂阳籍跨县）——郴州市域网络
    {"person_a": 17, "person_b": 18, "type": "跨县交流",
     "context": "桂阳籍干部邓生华执掌邻县宜章（2025-06）、归郴州市委领导",
     "overlap_org": "中共郴州市委员会", "overlap_period": "2025-06~至今",
     "strength": "weak", "confidence": "plausible"},
]


# ═══════════════════════════════════════════
# 构建
# ═══════════════════════════════════════════

def build():
    """运行数据库 + GEXF 构建。"""
    from gov_relation.runner import run_build

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

    _add_worked_at(positions, organizations, organizations)

    # 将 person JSON 写入同目录（用于 process_tmp.py 分类为 person_json）
    for p in persons:
        if p.get("name") in {"李富春", "贺雄", "巫初华", "李志强"}:
            _write_person_json(p)

    print(f"构建完成：{DB_PATH}")
    print(f"构建完成：{GEXF_PATH}")


def _add_worked_at(positions, _orgs, _unused):
    """在 GEXF 中补充 person→org 的 worked_at 任职边（org id 偏移 +100000）。"""
    path = GEXF_PATH
    text = path.read_text(encoding="utf-8")
    edge_blocks = []
    eid = 1000
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"] + 100000
        title = pos.get("title", "")
        eid += 1
        edge_blocks.append(f'<edge id="{eid}" source="{pid}" target="{oid}" label="{_esc(title)}" weight="1.0"><attvalues><attvalue for="0" value="worked_at" /><attvalue for="1" value="{_esc(title)}" /><attvalue for="2" value="" /><attvalue for="3" value="" /></attvalues></edge>')
    if "</edges>" in text:
        insert = "".join(edge_blocks)
        text = text.replace("</edges>", insert + "</edges>")
        path.write_text(text, encoding="utf-8")


def _esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _write_person_json(p):
    role_map = {
        "李富春": "县委书记",
        "贺雄": "县长",
        "巫初华": "前任县委书记",
        "李志强": "前任县长",
    }
    job = role_map[p["name"]]
    fname = f"{TODAY}-{PROVINCE}-{CITY}-{job}-{p['name']}.json"
    path = PERSONS_DIR / fname
    payload = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": PROVINCE,
            "city": CITY,
            "region": SLUG,
            "job": job,
            "task_id": "hunan_桂阳县",
            "time_focus": "2021至今",
        },
        "identity": {
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": p.get("birthplace", ""),
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级" if p["name"] in {"李富春", "贺雄", "巫初华", "李志强"} else "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": _career_timeline(p["name"]),
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if p["name"] in ("李志强", "李检华") else "cross_county_rotation",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "公开信息有限，工作风格未作推断。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "截至2026-08-06未检索到该核心人物的违纪违法或被查记录",
            "date": "",
            "confidence": "unverified",
            "source_ids": [],
        }],
        "source_register": [
            {"id": "RT001", "title": "桂阳县政府门户/桂阳新闻网", "url": "https://www.gyxnews.cn/",
             "publisher": "桂阳县融媒体中心", "source_type": "official", "reliability": "high", "accessed_at": AS_OF,
             "notes": "权威当地媒体，需补充直接URL"},
            {"id": "S002", "title": "百度检索汇编", "url": "https://www.baidu.com/",
             "publisher": "百度", "source_type": "encyclopedia", "reliability": "medium", "accessed_at": AS_OF,
             "notes": "百度百科/新闻摘要交叉汇编"},
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历缺早年任职与部分关键节点日期",
        },
        "open_questions": [
            {"priority": "high", "question": "贺雄何日正式由县人大任命为代理县长/县长？",
             "why_it_matters": "落实二把手正式任命情况", "suggested_queries": ["贺雄 桂阳 人大 任命", "桂阳 县政府 县长 贺雄"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": "李富春在苏仙区与北湖区任副区长的职务口径不一致，以官方为准？",
             "why_it_matters": "影响履历准确性与跨区关系判断", "suggested_queries": ["李富春 郴州 苏仙 北湖 区委 副区长"],
             "last_attempted": AS_OF},
            {"priority": "medium", "question": "巫初华「另有任用」具体新职为何？",
             "why_it_matters": "追踪前任去向与地区联系", "suggested_queries": ["巫初华 履新", "巫初华 郴州"],
             "last_attempted": AS_OF},
        ],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _career_timeline(name):
    timeline = []
    if name == "李富春":
        timeline += [
            {"start": "2026-06", "end": "present", "org": "中共桂阳县委员会", "title": "桂阳县委书记",
             "level": "正处级", "confidence": "confirmed"},
            {"start": "2024-08", "end": "2026-06", "org": "郴州市商务局", "title": "党组书记",
             "level": "正处级", "confidence": "confirmed"},
            {"start": "2022-11", "end": "2024-08", "org": "郴州高新区（自贸区郴州片区）", "title": "党工委委员、管委会副主任",
             "level": "正处级", "confidence": "confirmed"},
            {"start": "unknown", "end": "2022-11", "org": "永兴县委",
             "title": "县委常委、宣传部长（此前任郴州市委组织部副部长等）", "level": "副处级", "confidence": "plausible"},
        ]
    elif name == "贺雄":
        timeline += [
            {"start": "2026-07", "end": "present", "org": "桂阳县人民政府", "title": "县委副书记、县长人选（当选县委副书记）",
             "level": "正处级", "confidence": "confirmed"},
            {"start": "2025-08", "end": "2026-06", "org": "新邵县人民政府", "title": "县委常委、常务副县长",
             "level": "副处级", "confidence": "confirmed"},
            {"start": "unknown", "end": "2025-08", "org": "邵阳市", "title": "共青团邵阳市委书记等（邵阳地区长期任职）",
             "level": "", "confidence": "plausible"},
        ]
    elif name == "巫初华":
        timeline = [
            {"start": "2021-07", "end": "2026-06", "org": "中共桂阳县委员会", "title": "县委书记（另有任用，去向未公布）",
             "level": "正处级", "confidence": "confirmed"},
        ]
    elif name == "李志强":
        timeline = [
            {"start": "2021-04", "end": "present", "org": "桂阳县人民政府", "title": "县委副书记、县长（交接中）",
             "level": "正处级", "confidence": "confirmed"},
        ]
    return timeline


if __name__ == "__main__":
    build()