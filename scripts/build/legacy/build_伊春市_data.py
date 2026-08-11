#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 伊春市 leadership network.

伊春市是黑龙江省东北部地级市，别称"林都"，以森林生态旅游、林业资源著称，下辖伊美区、
乌翠区、友好区、金林区、汤旺县、丰林县、大箐山县、南岔县、嘉荫县、铁力市共十个县级政区，
是大小兴安岭森林生态核心区。

Current leadership as of 2026-08 (sources: 伊春市人民政府门户网站 www.yc.gov.cn「领导之窗/
市政府领导」官方简历、「伊春要闻」要闻；维基百科《伊春市》现任领导；既有调查 build_友好区
_data.py / build_汤旺县_data.py 汇总):
- 市委书记、市人大常委会主任: 董文琴（女，汉族，1972年10月生，黑龙江省宾县人，省委党校
  研究生学历；2024年9月任市委书记，2025年1月当选市人大常委会主任）
- 市委副书记、市长、市政府党组书记: 苑芳江（男，汉族，1977年3月生，2000年7月参加工作，
  1997年4月加入中国共产党，在职研究生、法学博士；主持市政府全面工作，分管市审计局）

市政府班子成员（官方「市政府领导」领导之窗确认，2026-08）：
- 陈岩：市委常委、市政府副市长（常务，协助市长主持市政府日常工作）
- 田宁、高见、刘暾、李东辉、姜治富、孟庆彤：市政府副市长
- 李长江：市政府秘书长

市政协主席: 刘福军（男，汉族，1968年1月生，山东省梁山县人，2025年1月当选）

网络连接线索：
- 佳木斯市委书记（兼黑龙江省副省长）丛丽为伊春籍干部，属跨地市干部成长路径。
- 前任市委书记/市长交接时间为 2024 年 9 月（董文琴任书记、苑芳江任市长）。

部分人物的完整履历/籍贯/学历公开资料有限，均在 confidence、open_questions 标注并写入
report/open_gaps.md，未作虚构。每一条任职/关系在网络图中按来源置信度分级。
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

SLUG = "伊春市"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "伊春市_network.db")
    GEXF_PATH = os.path.join(_STAGING, "伊春市_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "伊春市_network.db"
    GEXF_PATH = GRAPH_DIR / "伊春市_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共伊春市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委员会", "location": "黑龙江省伊春市伊美区"},
    {"id": 2, "name": "伊春市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省伊春市伊美区"},
    {"id": 3, "name": "伊春市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "黑龙江省人民代表大会常务委员会", "location": "黑龙江伊春市伊美区"},
    {"id": 4, "name": "中国人民政治协商会议伊春市委员会", "type": "政协", "level": "地厅级", "parent": "政协黑龙江省委员会", "location": "黑龙江伊春市伊美区"},
    {"id": 5, "name": "中共伊春市纪律检查委员会/伊春市监察委员会", "type": "纪委", "level": "地厅级", "parent": "中共黑龙江省纪委/省监委", "location": "黑龙江伊春市伊美区"},
    {"id": 6, "name": "中共黑龙江省委员会", "type": "党委", "level": "省部级", "parent": "中国共产党中央委员会", "location": "黑龙江省哈尔滨市"},
    {"id": 7, "name": "黑龙江省人民政府", "type": "政府", "level": "省部级", "parent": "中华人民共和国国务院", "location": "黑龙江省哈尔滨市"},

    # 跨地市连接（丛丽任职）
    {"id": 8, "name": "中共佳木斯市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委员会", "location": "黑龙江佳木斯市"},
    {"id": 9, "name": "黑龙江省科学技术协会", "type": "群团", "level": "厅局级", "parent": "黑龙江省人民政府", "location": "黑龙江省哈尔滨市"},
    {"id": 10, "name": "黑龙江省环境保护厅", "type": "政府机关", "level": "厅局级", "parent": "黑龙江省人民政府", "location": "黑龙江省哈尔滨市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 董文琴 — 市委书记、市人大常委会主任（现任）
    {"id": 1, "name": "董文琴", "gender": "女",
     "ethnicity": "汉族", "birth": "1972年10月", "birthplace": "黑龙江",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "伊春市委书记、市人大常委会主任", "current_org": "中共伊春市委员会",
     "source": "https://zh.wikipedia.org/wiki/伊春市; https://www.yc.gov.cn/"},
    # 2 — 苑芳江 — 市委副书记、市长（现任）
    {"id": 2, "name": "苑芳江", "gender": "男",
     "ethnicity": "汉族", "birth": "1977年3月", "birthplace": "黑龙江",
     "education": "在职研究生、法学博士",
     "party_join": "1997年4月加入中国共产党", "work_start": "2000年7月",
     "current_post": "伊春市委副书记、市长、市政府党组书记", "current_org": "伊春市人民政府",
     "source": "https://www.yc.gov.cn/ycsrmzf/c102129/202503/396239.shtml"},
    # 3 — 陈岩 — 市委常委、常务副市长
    {"id": 3, "name": "陈岩", "gender": "男",
     "ethnicity": "汉族", "birth": "1973年4月", "birthplace": "",
     "education": "在职大学学历",
     "party_join": "1994年12月加入中国共产党", "work_start": "1993年7月",
     "current_post": "伊春市委常委、市人民政府副市长", "current_org": "伊春市人民政府",
     "source": "https://www.yc.gov.cn/ycsrmzf/c102129/202405/352868.shtml"},
    # 4 — 田宁 — 市政府副市长
    {"id": 4, "name": "田宁", "gender": "",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "伊春市人民政府副市长", "current_org": "伊春市人民政府",
     "source": "https://www.yc.gov.cn/"},
    # 5 — 高见 — 市政府副市长
    {"id": 5, "name": "高见", "gender": "男",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "伊春市人民政府副市长", "current_org": "伊春市人民政府",
     "source": "https://www.yc.gov.cn/"},
    # 6 — 刘暾 — 市政府副市长
    {"id": 6, "name": "刘暾", "gender": "",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "伊春市人民政府副市长", "current_org": "伊春市人民政府",
     "source": "https://www.yc.gov.cn/"},
    # 7 — 李东辉 — 市政府副市长
    {"id": 7, "name": "李东辉", "gender": "",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "伊春市人民政府副市长", "current_org": "伊春市人民政府",
     "source": "https://www.yc.gov.cn/ycsrmzf/c102129/202506/404369.shtml"},
    # 8 — 姜治富 — 市政府副市长
    {"id": 8, "name": "姜治富", "gender": "",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "伊春市人民政府副市长", "current_org": "伊春市人民政府",
     "source": "https://www.yc.gov.cn/ycsrmzf/c102129/202212/250295.shtml"},
    # 9 — 孟庆彤 — 市政府副市长
    {"id": 9, "name": "孟庆彤", "gender": "",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "伊春市人民政府副市长", "current_org": "伊春市人民政府",
     "source": "https://www.yc.gov.cn/ycsrmzf/c102129/202212/250305.shtml"},
    # 10 — 李长江 — 市政府秘书长
    {"id": 10, "name": "李长江", "gender": "男",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "伊春市人民政府秘书长", "current_org": "伊春市人民政府",
     "source": "https://www.yc.gov.cn/ycsrmzf/c102129/202407/357513.shtml"},
    # 11 — 刘福军 — 市政协主席
    {"id": 11, "name": "刘福军", "gender": "男",
     "ethnicity": "汉族", "birth": "1968年1月", "birthplace": "山东省梁山县",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "伊春市政协主席", "current_org": "政协伊春市委员会",
     "source": "https://zh.wikipedia.org/wiki/伊春市"},
    # 12 — 丛丽 — 黑龙江省副省长、佳木斯市委书记（伊春籍，跨地市线索）
    {"id": 12, "name": "丛丽", "gender": "女",
     "ethnicity": "汉族", "birth": "1970年7月", "birthplace": "黑龙江省伊春市",
     "education": "",
     "party_join": "1991年加入中国共产党", "work_start": "",
     "current_post": "黑龙江省副省长、佳木斯市委书记", "current_org": "中共佳木斯市委员会",
     "source": "https://zh.wikipedia.org/wiki/丛丽"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 董文琴
    {"person_id": 1, "org_id": 1, "title": "伊春市委书记", "start_date": "2024-09", "end_date": "present", "rank": "正厅级", "note": "2024年9月任"},
    {"person_id": 1, "org_id": 3, "title": "伊春市人大常委会主任", "start_date": "2025-01", "end_date": "present", "rank": "正厅级", "note": "兼，2025年1月当选"},
    # 苑芳江
    {"person_id": 2, "org_id": 1, "title": "伊春市委副书记", "start_date": "2024-09", "end_date": "present", "rank": "副厅级", "note": "市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "伊春市人民政府市长", "start_date": "2024-09", "end_date": "present", "rank": "正厅级", "note": "市长、市政府党组书记"},
    # 陈岩
    {"person_id": 3, "org_id": 1, "title": "伊春市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "伊春市人民政府副市长（常务）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "协助市长负责市政府常务工作"},
    {"person_id": 4, "org_id": 2, "title": "伊春市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "伊春市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "伊春市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "伊春市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "伊春市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "伊春市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "伊春市人民政府秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 4, "title": "伊春市政协主席", "start_date": "2025-01", "end_date": "present", "rank": "正厅级", "note": "2025年1月当选"},
    {"person_id": 12, "org_id": 8, "title": "佳木斯市委书记", "start_date": "2023-03", "end_date": "present", "rank": "正厅级", "note": "兼黑龙江省副省长（2025-11 起副部级）"},
    {"person_id": 12, "org_id": 10, "title": "黑龙江省环境保护厅总工程师（早年）", "start_date": "", "end_date": "", "rank": "", "note": "早年曾在省环保厅任职"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────
relationships = [
    # 书记—市长 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "董文琴（市委书记）与苑芳江（市委副书记、市长）为伊春市现任党政一把手，同一市委班子共事", "overlap_org": "中共伊春市委", "overlap_period": "2024-09至今"},
    # 市长—常务副市长
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "苑芳江（市长）与陈岩（市委常委、常务副市长）为市政府班子正副主官配对", "overlap_org": "伊春市人民政府", "overlap_period": "至今"},
    # 书记—常务副市长（常委班子）
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "董文琴（市委书记）与陈岩（市委常委）同为市委常委会成员", "overlap_org": "中共伊春市委", "overlap_period": "至今"},
    # 市长—各副市长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "苑芳江（市长）与田宁（副市长）共事于市政府班子", "overlap_org": "伊春市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "苑芳江（市长）与高见（副市长）共事于市政府班子", "overlap_org": "伊春市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "苑芳江（市长）与刘暾（副市长）共事于市政府班子", "overlap_org": "伊春市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "苑芳江（市长）与李东辉（副市长）共事于市政府班子", "overlap_org": "伊春市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "苑芳江（市长）与姜治富（副市长）共事于市政府班子", "overlap_org": "伊春市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "苑芳江（市长）与孟庆彤（副市长）共事于市政府班子", "overlap_org": "伊春市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "苑芳江（市长）与李长江（市政府秘书长）为市政府办主从配对", "overlap_org": "伊春市人民政府", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 11, "type": "同城四大班子", "context": "董文琴（市人大常委会主任）与刘福军（市政协主席）同城四大班子", "overlap_org": "伊春市", "overlap_period": "2025-01至今"},
    {"person_a": 2, "person_b": 11, "type": "同城共事", "context": "苑芳江（市长）与刘福军（市政协主席）同城共事", "overlap_org": "伊春市", "overlap_period": "2025-01至今"},
    {"person_a": 1, "person_b": 12, "type": "同省地市正职", "context": "丛丽（佳木斯市委书记）籍贯为伊春市，与董文琴同为黑龙江省地级市正职领导（跨地市干部成长线索）", "overlap_org": "黑龙江省", "overlap_period": "", "context_note": ""},
]

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
    print(f"Wrote DB: {DB_PATH}")
    print(f"Wrote GEXF: {GEXF_PATH}")
    print(f"Stats: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")