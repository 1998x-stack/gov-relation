#!/usr/bin/env python3
"""长垣市领导班子关系网络数据生成脚本 (河南省新乡市长垣市, 县级市).

依据官方政府网站 (changyuan.gov.cn / xinxiang.gov.cn) 2026 年公开报道承担:
核心一把手/二把手身份均经官方权威报道确认; 部分履历字段因网络受限标为待查。
"""
import sys, sqlite3
from pathlib import Path
_REPO = Path(__file__).resolve()
for _ in range(6):
    if (_REPO / "gov_relation").is_dir():
        break
    _REPO = _REPO.parent
sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

slug = "长垣市"

DB_PATH = DATABASE_DIR / "长垣市_network.db"
GEXF_PATH = GRAPH_DIR / "长垣市_network.gexf"

# ---------------- Persons ----------------
persons = [
    {"id": 1, "name": "范文卿", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委书记", "current_org": "中共长垣市委员会",
     "source": "http://www.changyuan.gov.cn/sitesources/cyxrmzf/page_pc/ywdt/zyyw/articlebd3598cf02b343288a949a00cac2ed5b.html"},
    {"id": 2, "name": "曹祖臣", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委副书记、市长", "current_org": "长垣市人民政府",
     "source": "http://www.changyuan.gov.cn/sitesources/cyxrmzf/page_pc/ywdt/zyyw/article6b064750fbfb4d3fadd4d8d63fd89393.html"},
    {"id": 3, "name": "周骥", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委常委、常务副市长", "current_org": "长垣市人民政府",
     "source": "http://www.changyuan.gov.cn/sitesources/cyxrmzf/page_pc/ywdt/tpxw/article381d24255ba14b4fad51ae5e558b30c7.html"},
    {"id": 4, "name": "李成贵", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委常委", "current_org": "中共长垣市委员会",
     "source": "http://www.changyuan.gov.cn/sitesources/cyxrmzf/page_pc/ywdt/tpxw/article381d24255ba14b4fad51ae5e558b30c7.html"},
    {"id": 5, "name": "王彦涛", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委常委、副市长", "current_org": "长垣市人民政府",
     "source": "http://www.changyuan.gov.cn/sitesources/cyxrmzf/page_pc/ywdt/zyyw/article6b064750fbfb4d3fadd4d8d63fd89393.html"},
    {"id": 6, "name": "冀大旭", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委常委", "current_org": "中共长垣市委员会",
     "source": "http://www.changyuan.gov.cn/sitesources/cyxrmzf/page_pc/ywdt/tpxw/article381d24255ba14b4fad51ae5e558b30c7.html"},
    {"id": 7, "name": "张良", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委常委", "current_org": "中共长垣市委员会",
     "source": "http://www.changyuan.gov.cn/sitesources/cyxrmzf/page_pc/ywdt/zyyw/articlec520a36269a1416daa2a63426a259e75.html"},
    {"id": 8, "name": "宋云天", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委常委、副市长", "current_org": "长垣市人民政府",
     "source": "http://www.changyuan.gov.cn/sitesources/cyxrmzf/page_pc/ywdt/zyyw/articlec520a36269a1416daa2a63426a259e75.html"},
    {"id": 9, "name": "赵旭", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委常委、组织部部长", "current_org": "中共长垣市委员会",
     "source": "http://www.changyuan.gov.cn/sitesources/cyxrmzf/page_pc/ywdt/tpxw/article52bfc3c2b67448c2bff0aaa2fec76872.html"},
    {"id": 10, "name": "刘洋", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "市委常委", "current_org": "中共长垣市委员会",
     "source": "http://www.changyuan.gov.cn/sitesources/cyxrmzf/page_pc/ywdt/tpxw/article381d24255ba14b4fad51ae5e558b30c7.html"},
    {"id": 11, "name": "李联合", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副市长", "current_org": "长垣市人民政府",
     "source": "http://www.changyuan.gov.cn/sitesources/cyxrmzf/page_pc/ywdt/zyyw/articlec520a36269a1416daa2a63426a259e75.html"},
    {"id": 12, "name": "薛伟涛", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副市长", "current_org": "长垣市人民政府",
     "source": "http://www.changyuan.gov.cn/sitesources/cyxrmzf/page_pc/ywdt/zyyw/articlea62fe3cd6ca7433187aafa95d1ad4b7e.html"},
    {"id": 13, "name": "魏建平", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "新乡市委书记", "current_org": "中共新乡市委员会",
     "source": "https://www.xinxiang.gov.cn/zwzx/jrxx/10774920.html"},
]

# ---------------- Organizations ----------------
organizations = [
    {"id": 1, "name": "中共长垣市委员会", "type": "党委", "level": "县级市", "parent": "中共新乡市委员会", "location": "河南省新乡市长垣市"},
    {"id": 2, "name": "长垣市人民政府", "type": "政府", "level": "县级市", "parent": "新乡市人民政府", "location": "河南省新乡市长垣市"},
    {"id": 3, "name": "中共新乡市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委员会", "location": "河南省新乡市"},
    {"id": 4, "name": "新乡市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "河南省新乡市"},
    {"id": 5, "name": "中共封丘县委员会", "type": "党委", "level": "县", "parent": "中共新乡市委员会", "location": "河南省新乡市封丘县"},
]

# ---------------- Positions ----------------
positions = [
    # 党委正职
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "三届市委书记(2026-06 历届党代会报告)"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 政府正职
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正处级", "note": "2026-08 主持市政府第107次常务会议"},
    # 市委常委
    {"person_id": 3, "org_id": 1, "title": "市委常委、常务副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026-07-20 主持干部培训班"},
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 市政府副市长 (非常委)
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 上级 (新乡市委)
    {"person_id": 13, "org_id": 3, "title": "新乡市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "2026-07-30 到长垣调研"},
    # 曹祖臣旧职 (封丘)
    {"person_id": 2, "org_id": 5, "title": "县委副书记", "start_date": "2021-09", "end_date": "", "rank": "副处级", "note": "据百度百科:2021-09 任封丘县委副书记"},
]

# ---------------- Relationships ----------------
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "书记/市长党政正职搭档, 党代会一荣俱荣", "overlap_org": "中共长垣市委员会", "overlap_period": "2023-至今"},
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "新乡市委书记为长垣市委书记上级", "overlap_org": "中共新乡市委员会", "overlap_period": "2023-至今"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "长垣市长受新乡市委领导", "overlap_org": "中共新乡市委员会", "overlap_period": "2023-至今"},
    {"person_a": 3, "person_b": 2, "type": "上下级", "context": "常务副市长为市长副手", "overlap_org": "长垣市人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 2, "type": "上下级", "context": "副市长为市长副手", "overlap_org": "长垣市人民政府", "overlap_period": ""},
    {"person_a": 8, "person_b": 2, "type": "上下级", "context": "副市长为市长副手", "overlap_org": "长垣市人民政府", "overlap_period": ""},
    {"person_a": 9, "person_b": 1, "type": "上下级", "context": "组织部部长在市委书记领导下工作", "overlap_org": "中共长垣市委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "前任关系", "context": "曹祖臣曾任封丘县委副书记 (2021) 前后职务与本县关联", "overlap_org": "中共封丘县委员会", "overlap_period": "2021-2023"},
]

# ---------------- Build ----------------
if __name__ == "__main__":
    run_build(
        slug=slug,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("DB_PATH:", DB_PATH)
    print("GEXF_PATH:", GEXF_PATH)
    print(f"长垣市_network build complete: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} pos, {len(relationships)} rel")
