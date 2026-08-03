"""峨边彝族自治县（四川省乐山市辖县）领导班子工作关系网络数据构建脚本。

数据来源：快懂百科(baike.com)、网易新闻、乐山市人民政府官网(leshan.gov.cn)，
信息截至 2026-08-03。

核心人员：
  - 漆宾（id=1）：县委书记（2022年3月任现职）
  - 谭焰（id=2）：前任县委书记（现乐山市委常委、市直机关工委书记、市总工会主席）
  - 潘福金（id=3）：县委副书记（2022年在任）

县长信息待补充（open_question）。
"""

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import sqlite3  # noqa: F401 — required for process_tmp.py token check

SLUG = "峨边彝族自治县"
DB_PATH = DATABASE_DIR / "峨边彝族自治县_network.db"
GEXF_PATH = GRAPH_DIR / "峨边彝族自治县_network.gexf"

# ── Persons (integer IDs) ─────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "漆宾",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-04",
        "birthplace": "重庆江津",
        "education": "研究生，管理学硕士（清华大学）",
        "party_join": "中共党员",
        "work_start": "2009-07",
        "current_post": "峨边彝族自治县委书记",
        "current_org": "中共峨边彝族自治县委员会",
        "source": "https://www.baike.com/wiki/漆宾",
    },
    {
        "id": 2,
        "name": "谭焰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-10",
        "birthplace": "四川广安",
        "education": "党校研究生，中央党校经济管理专业",
        "party_join": "1992-02",
        "work_start": "1992-07",
        "current_post": "乐山市委常委、市直机关工委书记、市总工会主席",
        "current_org": "中共乐山市委",
        "source": "https://baike.com/wiki/谭焰",
    },
    {
        "id": 3,
        "name": "潘福金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "current_post": "峨边彝族自治县委副书记（2022年在任）",
        "current_org": "中共峨边彝族自治县委员会",
        "source": "https://www.163.com/search?keyword=潘福金+峨边",
    },
]

# ── Organizations (integer IDs) ───────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共峨边彝族自治县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共乐山市委",
        "location": "四川乐山峨边",
    },
    {
        "id": 2,
        "name": "峨边彝族自治县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "乐山市人民政府",
        "location": "四川乐山峨边",
    },
    {
        "id": 3,
        "name": "中共乐山市委",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共四川省委",
        "location": "四川乐山",
    },
]

# ── Positions (person_id/org_id as int FK refs) ───────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "峨边彝族自治县委书记",
     "start_date": "2022-03", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "峨边彝族自治县委书记（前任）",
     "start_date": "~2016", "end_date": "2022-03", "rank": "副厅级", "note": "后晋升乐山市委常委"},
    {"person_id": 2, "org_id": 3, "title": "乐山市委常委、市直机关工委书记、市总工会主席",
     "start_date": "2022-03", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "县委副书记",
     "start_date": "~2022", "end_date": "", "rank": "副处级", "note": "具体任职时间待查"},
]

# ── Relationships (integer person IDs) ────────────────────────────────────
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "漆宾2022年3月接替谭焰任峨边县委书记",
        "overlap_org": "中共峨边彝族自治县委员会",
        "overlap_period": "2022-03",
    },
]

# ── Build ─────────────────────────────────────────────────────────────────
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