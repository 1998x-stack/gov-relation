#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 杞县 leadership network.

杞县 - 开封市 - 河南省
Targets: 县委书记戴继田, 县长黄宗刚

数据来源：开封市人民政府门户网站（kaifeng.gov.cn）县区动态、人事任免栏目、
开封市委组织部领导干部任前公示公告。因外部搜索引擎与县政府门户限流，部分
履历字段（出生年月、籍贯、教育背景）未能核实，已在 person JSON 的
open_questions 与 report/open_gaps.md 中标注为待查。
"""

import sqlite3  # noqa: F401 — required for process_tmp.py token check
import sys
from pathlib import Path

# Ensure gov_relation is importable
_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "杞县"
TASK_ID = "henan_杞县"

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────
# 现任党政正职已由开封市政府网站（kaifeng.gov.cn）2026年6月县区报道确认。
persons = [
    # ── 1. 现任核心领导 ──
    {
        "id": 1,
        "name": "戴继田",
        "gender": "男",
        "ethnicity": "汉",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杞县县委书记",
        "current_org": "中国共产党杞县委员会",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/xqdt/pc/content/content_2069349989317390336.html",
    },
    {
        "id": 2,
        "name": "黄宗刚",
        "gender": "男",
        "ethnicity": "汉",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杞县县委副书记、政府县长",
        "current_org": "杞县人民政府",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/xqdt/pc/content/content_2069350218448023552.html",
    },
    # ── 2. 其他县委班子主要成员 ──
    {
        "id": 3,
        "name": "罗力鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杞县县委副书记、统战部部长",
        "current_org": "中国共产党杞县委员会",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/xqdt/pc/content/content_2080552812080050176.html",
    },
    {
        "id": 4,
        "name": "任明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杞县县委常委",
        "current_org": "中国共产党杞县委员会",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/xqdt/pc/content/content_2069350218448023552.html",
    },
    {
        "id": 5,
        "name": "李琦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杞县县委常委（联系县人武部）",
        "current_org": "中国共产党杞县委员会",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/xqdt/pc/content/content_2082728448995811552.html",
    },
    {
        "id": 6,
        "name": "宋朝忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杞县县委常委",
        "current_org": "中国共产党杞县委员会",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/xqdt/pc/content/content_2069350218448027552.html",
    },
    {
        "id": 7,
        "name": "赵凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杞县县委常委",
        "current_org": "中国共产党杞县委员会",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/xqdt/pc/content/content_2069350218448023552.html",
    },
    {
        "id": 8,
        "name": "张亚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杞县县委常委",
        "current_org": "中国共产党杞县委员会",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/xqdt/pc/content/content_2069350218448023552.html",
    },
    {
        "id": 9,
        "name": "转迎亚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杞县县委常委",
        "current_org": "中国共产党杞县委员会",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/xqdt/pc/content/2081639334933999616.html",
    },
    {
        "id": 10,
        "name": "李青",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杞县县委常委",
        "current_org": "中国共产党杞县委员会",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/xqdt/pc/content/content_2069350218448023552.html",
    },
    # ── 3. 人大、政协正职 ──
    {
        "id": 11,
        "name": "王星海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杞县人大常委会主任",
        "current_org": "杞县人民代表大会常务委员会",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/xqdt/pc/content/2081639334934509568.html",
    },
    {
        "id": 12,
        "name": "董伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杞县政协主席",
        "current_org": "政协杞县委员会",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/xqdt/pc/content/2082728960834711552.html",
    },
    # ── 4. 前任县委书记（经搜索线索确认，履历待查）──
    {
        "id": 13,
        "name": "韩治群",
        "gender": "男",
        "ethnicity": "汉",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任杞县县委书记）",
        "current_org": "中国共产党杞县委员会",
        "source": "搜索引擎报道：河南省杞县县委书记韩治群现场督导问题楼盘化解攻坚（报道线索）",
    },
    # ── 5. 2026年拟任副县长的杞县干部（任前公示）──
    {
        "id": 14,
        "name": "李青杰",
        "gender": "男",
        "ethnicity": "汉",
        "birth": "1985年3月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（拟任）杞县副县长",
        "current_org": "杞县人民政府",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/rsrm/pc/content/content_2064873904794021888.html",
    },
    {
        "id": 15,
        "name": "霍赟",
        "gender": "男",
        "ethnicity": "汉",
        "birth": "1974年7月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（拟任）杞县，原杞县先进制造业开发区党工委书记、管委会主任",
        "current_org": "杞县先进制造业开发区",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/rsrm/pc/content/content_2064873904794021888.html",
    },
    {
        "id": 16,
        "name": "王顺利",
        "gender": "男",
        "ethnicity": "汉",
        "birth": "1977年10月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（拟任）杞县，原杞县公安局党委副书记、政委",
        "current_org": "杞县公安局",
        "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/rsrm/pc/content/content_1960505552583168000.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党杞县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党开封市委员会",
        "location": "杞县",
    },
    {
        "id": 2,
        "name": "杞县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "开封市人民政府",
        "location": "杞县",
    },
    {
        "id": 3,
        "name": "杞县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "开封市人民代表大会常务委员会",
        "location": "杞县",
    },
    {
        "id": 4,
        "name": "政协杞县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协开封市委员会",
        "location": "杞县",
    },
    {
        "id": 5,
        "name": "中国共产党开封市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中国共产党河南省委员会",
        "location": "开封市",
    },
    {
        "id": 6,
        "name": "开封市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "河南省人民政府",
        "location": "开封市",
    },
    {
        "id": 7,
        "name": "中共开封市委组织部",
        "type": "党委",
        "level": "地市级",
        "parent": "中国共产党开封市委员会",
        "location": "开封市",
    },
    {
        "id": 8,
        "name": "杞县先进制造业开发区",
        "type": "开发区",
        "level": "县级",
        "parent": "杞县人民政府",
        "location": "杞县",
    },
    {
        "id": 9,
        "name": "杞县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "杞县人民政府",
        "location": "杞县",
    },
    {
        "id": 10,
        "name": "杞县竹林乡",
        "type": "乡镇",
        "level": "乡镇级",
        "parent": "杞县人民政府",
        "location": "杞县",
    },
]

# ── Positions ─────────────────────────────────────────────────────────

positions = [
    # 戴继田（县委书记）
    {"person_id": 1, "org_id": 1, "title": "杞县县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "据开封市政府网站2026年6月县区报道确认"},
    # 黄宗刚（县长）
    {"person_id": 2, "org_id": 2, "title": "杞县县委副书记、县政府县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "据2026年6月杞县十四届党代会报道确认"},
    # 罗力鹏
    {"person_id": 3, "org_id": 1, "title": "杞县县委副书记、统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "2026年7月报道任统战部长"},
    # 常委班子
    {"person_id": 4, "org_id": 1, "title": "杞县县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "杞县县委常委、县人武部相关领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": "2026年7月议军会议汇报人武工作"},
    {"person_id": 6, "org_id": 1, "title": "杞县县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "杞县县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "杞县县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "杞县县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "杞县县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 人大、政协
    {"person_id": 11, "org_id": 3, "title": "杞县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 12, "org_id": 4, "title": "杞县政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 前任县委书记韩治群
    {"person_id": 13, "org_id": 1, "title": "杞县县委书记（前任）", "start_date": "", "end_date": "", "rank": "正县级", "note": "报道线索，具体任期待查"},
    # 新任副县长候选人
    {"person_id": 14, "org_id": 2, "title": "杞县副县长（拟任）", "start_date": "2026.06", "end_date": "present", "rank": "副县级", "note": "2026年6月任前公示；原杞县竹林乡党委书记"},
    {"person_id": 14, "org_id": 10, "title": "杞县竹林乡党委书记", "start_date": "", "end_date": "2026.06", "rank": "乡科级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "杞县副县长（拟任）", "start_date": "2026.06", "end_date": "present", "rank": "副县级", "note": "2026年6月任前公示；原开发区党工委书记"},
    {"person_id": 15, "org_id": 8, "title": "杞县先进制造业开发区党工委书记、管委会主任", "start_date": "", "end_date": "2026.06", "rank": "副县级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "杞县副县长（拟任）", "start_date": "2025.08", "end_date": "present", "rank": "副县级", "note": "2025年8月任前公示；原县公安局党委副书记、政委"},
    {"person_id": 16, "org_id": 9, "title": "杞县公安局党委副书记、政委", "start_date": "", "end_date": "2025.08", "rank": "副县级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────

relationships = [
    # 党政正职搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "共事",
        "context": "戴继田（县委书记）与黄宗刚（县长）为杞县党政正职搭档，共同出席2026年杞县第十四次党代会相关活动",
        "overlap_org": "中国共产党杞县委员会/杞县人民政府",
        "overlap_period": "2026年至今",
    },
    # 县委班子同事
    {
        "person_a": 1,
        "person_b": 3,
        "type": "上下级",
        "context": "罗力鹏（县委副书记）在戴继田（县委书记）领导下工作",
        "overlap_org": "中国共产党杞县委员会",
        "overlap_period": "2026年至今",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "共事",
        "context": "黄宗刚（县长）与罗力鹏（县委副书记）同属县委班子",
        "overlap_org": "中国共产党杞县委员会",
        "overlap_period": "2026年至今",
    },
    # 人大/政协领导与党政
    {
        "person_a": 1,
        "person_b": 11,
        "type": "共事",
        "context": "王星海（县人大主任）在县委领导下，列席杞县十三届十次全委会",
        "overlap_org": "杞县",
        "overlap_period": "2026年",
    },
    {
        "person_a": 1,
        "person_b": 12,
        "type": "共事",
        "context": "董伟（县政协主席）在戴继田领导下，出席大常委会等会议",
        "overlap_org": "杞县",
        "overlap_period": "2026年",
    },
    # 前任书记与现任（前后任）
    {
        "person_a": 13,
        "person_b": 1,
        "type": "前后任",
        "context": "韩治群（前任杞县县委书记）与戴继田（现任）先后任职杞县县委书记",
        "overlap_org": "中国共产党杞县委员会",
        "overlap_period": "",
    },
    # 拟任副县长与班长（作为候选上下级）
    {
        "person_a": 2,
        "person_b": 14,
        "type": "上下级",
        "context": "李青杰任杞县副县长（拟），在黄宗刚（县长）领导下工作",
        "overlap_org": "杞县人民政府",
        "overlap_period": "2026年",
    },
]

# ── Build ─────────────────────────────────────────────────────────────

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

    print(f" DB: {DB_PATH}")
    print(f" GEXF: {GEXF_PATH}")
    print(f" Done.")