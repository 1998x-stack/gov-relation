"""嘉兴市领导班子关系网络 — 地级市级构建脚本。

数据来源：
- 嘉兴市人民政府网站 (jiaxing.gov.cn) 市政府领导页面 — 2026年7月确认
- 嘉兴市政府活动新闻 — 陈伟（市委书记）、许小月（市长）多次出现
- 各副市长职责分工页面已确认

数据时效：2026-07-28
"""

import sys
from pathlib import Path

# 将项目根目录加入路径
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import sqlite3  # noqa: used by run_build internally

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "嘉兴市"
STAGING_DIR = Path(__file__).parent
DB_PATH = STAGING_DIR / "嘉兴市_network.db"
GEXF_PATH = STAGING_DIR / "嘉兴市_network.gexf"

# ═══════════════════════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════════════════════
# 核心领导（一号、二号人物）
PERSONS = [
    # ── 市委书记 ──
    {
        "id": 1,
        "name": "陈伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共嘉兴市委员会",
        "source": "https://www.jiaxing.gov.cn/col/col1535565/index.html",
    },
    # ── 市委副书记、市长 ──
    {
        "id": 2,
        "name": "许小月",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "嘉兴市人民政府",
        "source": "https://www.jiaxing.gov.cn/col/col1558839/xxy/index.html",
    },
    # ── 市委常委、常务副市长 ──
    {
        "id": 3,
        "name": "颜海荣",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "嘉兴市人民政府",
        "source": "https://www.jiaxing.gov.cn/col/col1229819091/index.html",
    },
    # ── 副市长 ──
    {
        "id": 4,
        "name": "林万乐",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "嘉兴市人民政府",
        "source": "https://www.jiaxing.gov.cn/col/col1229819095/index.html",
    },
    # ── 副市长 ──
    {
        "id": 5,
        "name": "戴锋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "嘉兴市人民政府",
        "source": "https://www.jiaxing.gov.cn/col/col1229819096/index.html",
    },
    # ── 副市长 ──
    {
        "id": 6,
        "name": "周连昆",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "嘉兴市人民政府",
        "source": "https://www.jiaxing.gov.cn/col/col1558839/zlk/index.html",
    },
    # ── 副市长、市公安局局长 ──
    {
        "id": 7,
        "name": "张海燕",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "嘉兴市人民政府",
        "source": "https://www.jiaxing.gov.cn/col/col1229819097/index.html",
    },
    # ── 副市长 ──
    {
        "id": 8,
        "name": "黄亮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "嘉兴市人民政府",
        "source": "https://www.jiaxing.gov.cn/col/col1558839/hl/index.html",
    },
    # ── 秘书长 ──
    {
        "id": 9,
        "name": "朱少平",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "秘书长、二级巡视员",
        "current_org": "嘉兴市人民政府办公室",
        "source": "https://www.jiaxing.gov.cn/col/col1229819099/index.html",
    },
    # ── 市级领导（新闻报道中出现，经信局/商务局背景） ──
    {
        "id": 10,
        "name": "沈雨祥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "嘉兴市",
        "source": "https://www.jiaxing.gov.cn/col/col1558839/xxy/zyhd/art/2026/art_2a0194c6deadcfa0471b3b0ff9f8eff6.html",
    },
]

# ═══════════════════════════════════════════════════════════════
# 组织机构数据
# ═══════════════════════════════════════════════════════════════
ORGANIZATIONS = [
    # ── 党委 ──
    {
        "id": 1,
        "name": "中共嘉兴市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共浙江省委员会",
        "location": "浙江省嘉兴市",
    },
    # ── 政府 ──
    {
        "id": 2,
        "name": "嘉兴市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "浙江省人民政府",
        "location": "浙江省嘉兴市",
    },
    # ── 政府办公室 ──
    {
        "id": 3,
        "name": "嘉兴市人民政府办公室",
        "type": "政府部门",
        "level": "县处级",
        "parent": "嘉兴市人民政府",
        "location": "浙江省嘉兴市",
    },
    # ── 公安局 ──
    {
        "id": 4,
        "name": "嘉兴市公安局",
        "type": "政府部门",
        "level": "县处级",
        "parent": "嘉兴市人民政府",
        "location": "浙江省嘉兴市",
    },
    # ── 人大 ──
    {
        "id": 5,
        "name": "嘉兴市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "",
        "location": "浙江省嘉兴市",
    },
    # ── 政协 ──
    {
        "id": 6,
        "name": "中国人民政治协商会议嘉兴市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "",
        "location": "浙江省嘉兴市",
    },
]

# ═══════════════════════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════════════════════
POSITIONS = [
    # 陈伟
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "主持市委全面工作"},
    # 许小月
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "协助书记工作"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "领导市政府全面工作"},
    # 颜海荣
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "负责市政府常务工作"},
    # 林万乐
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "负责自然资源、住建、卫健等"},
    # 戴锋
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "负责经信、教育、科技、商务等"},
    # 周连昆
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 张海燕
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "市公安局局长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "主持公安局工作"},
    # 黄亮
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "负责生态环境、交通、水利、农业农村等"},
    # 朱少平
    {"person_id": 9, "org_id": 3, "title": "秘书长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "协助市长处理日常工作，二级巡视员"},
    # 沈雨祥
    {"person_id": 10, "org_id": 1, "title": "市领导", "start_date": "", "end_date": "", "rank": "", "note": "新闻报道中出席市级会议"},
]

# ═══════════════════════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════════════════════
RELATIONSHIPS = [
    # 党政正职搭档 — 陈伟 ↔ 许小月
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记与市长搭档", "overlap_org": "中共嘉兴市委员会", "overlap_period": ""},
    # 市委常委班子 — 陈伟 ↔ 颜海荣（上下级）
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "市委书记与市委常委", "overlap_org": "中共嘉兴市委员会", "overlap_period": ""},
    # 市政府班子 — 许小月与各副市长共事关系
    {"person_a": 2, "person_b": 3, "type": "党政副职", "context": "市长与常务副市长", "overlap_org": "嘉兴市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "党政副职", "context": "市长与副市长", "overlap_org": "嘉兴市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "党政副职", "context": "市长与副市长", "overlap_org": "嘉兴市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "党政副职", "context": "市长与副市长", "overlap_org": "嘉兴市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "党政副职", "context": "市长与副市长兼公安局长", "overlap_org": "嘉兴市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "党政副职", "context": "市长与副市长", "overlap_org": "嘉兴市人民政府", "overlap_period": ""},
    # 朱少平—市长 工作关联
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "市长与市政府秘书长", "overlap_org": "嘉兴市人民政府", "overlap_period": ""},
    # 张海燕（公安）- 政府与其他副市长
    {"person_a": 7, "person_b": 3, "type": "同僚", "context": "副市长之间", "overlap_org": "嘉兴市人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 4, "type": "同僚", "context": "副市长之间", "overlap_org": "嘉兴市人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 5, "type": "同僚", "context": "副市长之间", "overlap_org": "嘉兴市人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 6, "type": "同僚", "context": "副市长之间", "overlap_org": "嘉兴市人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "副市长之间", "overlap_org": "嘉兴市人民政府", "overlap_period": ""},
    # 沈雨祥 与其他市领导
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "市委会议出席", "overlap_org": "中共嘉兴市委员会", "overlap_period": ""},
]

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"✅ 嘉兴市网络构建完成")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")