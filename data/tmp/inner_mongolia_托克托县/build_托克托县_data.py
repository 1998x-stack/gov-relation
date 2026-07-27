#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 托克托县 leadership network.

托克托县隶属内蒙古自治区呼和浩特市。

Current leadership (as of 2026-07-25 — web access degraded; verified from pre-cutoff knowledge):
- 县委书记: 王冬生 (confirmed up to mid-2025, status as of 2026 TBC)
- 县长: 高正 (confirmed up to mid-2025, status as of 2026 TBC)

⚠ NOTE: Web access was unavailable during research (Exa rate-limited, all HTTP
requests timed out). Leadership data is based on pre-cutoff knowledge and requires
verification against current official sources. All biographical details beyond
basic identity are marked with appropriate confidence levels.

Key sources to verify:
- http://www.tuoketuo.gov.cn/zhengwu/ldzc/ (托克托县政府领导之窗)
- https://baike.baidu.com/item/王冬生 (for secretary's resume)
- https://baike.baidu.com/item/高正 (for mayor's resume)
- 呼和浩特市/内蒙古自治区官网任前公示
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "托克托县"
DB_PATH = DATABASE_DIR / "托克托县_network.db"
GEXF_PATH = GRAPH_DIR / "托克托县_network.gexf"

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共托克托县委员会", "type": "党委", "level": "县处级", "parent": "中共呼和浩特市委", "location": "内蒙古自治区呼和浩特市托克托县"},
    {"id": 2, "name": "托克托县人民政府", "type": "政府", "level": "县处级", "parent": "呼和浩特市人民政府", "location": "内蒙古自治区呼和浩特市托克托县"},
    {"id": 3, "name": "托克托县人大常委会", "type": "人大", "level": "县处级", "parent": "呼和浩特市人大常委会", "location": "内蒙古自治区呼和浩特市托克托县"},
    {"id": 4, "name": "托克托县政协", "type": "政协", "level": "县处级", "parent": "呼和浩特市政协", "location": "内蒙古自治区呼和浩特市托克托县"},
    {"id": 5, "name": "中共托克托县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共呼和浩特市纪委", "location": "内蒙古自治区呼和浩特市托克托县"},
    {"id": 6, "name": "中共托克托县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共托克托县委员会", "location": "内蒙古自治区呼和浩特市托克托县"},
    {"id": 7, "name": "中共托克托县委组织部", "type": "党委", "level": "县处级", "parent": "中共托克托县委员会", "location": "内蒙古自治区呼和浩特市托克托县"},
    {"id": 8, "name": "中共托克托县委宣传部", "type": "党委", "level": "县处级", "parent": "中共托克托县委员会", "location": "内蒙古自治区呼和浩特市托克托县"},
    {"id": 9, "name": "中共托克托县委统战部", "type": "党委", "level": "县处级", "parent": "中共托克托县委员会", "location": "内蒙古自治区呼和浩特市托克托县"},
    {"id": 10, "name": "托克托县人民武装部", "type": "事业单位", "level": "县处级", "parent": "呼和浩特警备区", "location": "内蒙古自治区呼和浩特市托克托县"},
    {"id": 11, "name": "托克托县公安局", "type": "政府", "level": "县处级", "parent": "托克托县人民政府", "location": "内蒙古自治区呼和浩特市托克托县"},
    {"id": 12, "name": "托克托县人民法院", "type": "事业单位", "level": "县处级", "parent": "呼和浩特市中级人民法院", "location": "内蒙古自治区呼和浩特市托克托县"},
    {"id": 13, "name": "托克托县人民检察院", "type": "事业单位", "level": "县处级", "parent": "呼和浩特市人民检察院", "location": "内蒙古自治区呼和浩特市托克托县"},
    {"id": 14, "name": "呼和浩特托克托工业园区", "type": "开发区", "level": "县处级", "parent": "托克托县人民政府", "location": "内蒙古自治区呼和浩特市托克托县"},
    {"id": 15, "name": "中共托克托县委办公室", "type": "党委", "level": "县处级", "parent": "中共托克托县委员会", "location": "内蒙古自治区呼和浩特市托克托县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ═══ 县委领导 ═══

    # 1 — 王冬生 — 县委书记
    {"id": 1, "name": "王冬生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "托克托县委书记", "current_org": "中共托克托县委员会",
     "source": "已知信息—需通过网络核实确认"},
    # 2 — 高正 — 县长
    {"id": 2, "name": "高正", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "托克托县委副书记、县政府党组书记、县长", "current_org": "托克托县人民政府",
     "source": "已知信息—需通过网络核实确认"},
    # 3 — 专职副书记（人选待核实）
    {"id": 3, "name": "（专职副书记待核实）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "托克托县委副书记（专职）", "current_org": "中共托克托县委员会",
     "source": "待查—需通过政府网站领导之窗核实"},
    # 4 — 常务副县长（人选待核实）
    {"id": 4, "name": "（常务副县长待核实）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "托克托县委常委、常务副县长", "current_org": "托克托县人民政府",
     "source": "待查—需通过政府网站领导之窗核实"},
    # 5 — 纪委书记（人选待核实）
    {"id": 5, "name": "（纪委书记待核实）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "托克托县委常委、纪委书记、监委主任", "current_org": "中共托克托县纪律检查委员会",
     "source": "待查—需通过政府网站领导之窗核实"},
    # 6 — 组织部长（人选待核实）
    {"id": 6, "name": "（组织部长待核实）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "托克托县委常委、组织部部长", "current_org": "中共托克托县委组织部",
     "source": "待查—需通过政府网站领导之窗核实"},
    # 7 — 宣传部长（人选待核实）
    {"id": 7, "name": "（宣传部长待核实）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "托克托县委常委、宣传部部长", "current_org": "中共托克托县委宣传部",
     "source": "待查—需通过政府网站领导之窗核实"},
    # 8 — 统战部长（人选待核实）
    {"id": 8, "name": "（统战部长待核实）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "托克托县委常委、统战部部长", "current_org": "中共托克托县委统战部",
     "source": "待查—需通过政府网站领导之窗核实"},
    # 9 — 政法委书记（人选待核实）
    {"id": 9, "name": "（政法委书记待核实）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "托克托县委常委、政法委书记", "current_org": "中共托克托县委政法委员会",
     "source": "待查—需通过政府网站领导之窗核实"},
    # 10 — 人武部长（人选待核实）
    {"id": 10, "name": "（人武部长待核实）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "托克托县委常委、人武部部长", "current_org": "托克托县人民武装部",
     "source": "待查—需通过政府网站领导之窗核实"},
    # 11 — 县委办主任（人选待核实）
    {"id": 11, "name": "（县委办主任待核实）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "托克托县委常委、县委办主任", "current_org": "中共托克托县委办公室",
     "source": "待查—需通过政府网站领导之窗核实"},

    # ═══ 人大、政协领导 ═══

    # 12 — 人大主任（人选待核实）
    {"id": 12, "name": "（人大主任待核实）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "托克托县人大常委会主任", "current_org": "托克托县人大常委会",
     "source": "待查—需通过政府网站核实"},
    # 13 — 政协主席（人选待核实）
    {"id": 13, "name": "（政协主席待核实）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "托克托县政协主席", "current_org": "托克托县政协",
     "source": "待查—需通过政府网站核实"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 王冬生
    {"person_id": 1, "org_id": 1, "title": "托克托县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县委全面工作"},

    # 高正
    {"person_id": 2, "org_id": 1, "title": "托克托县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "托克托县政府党组书记、县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县政府全面工作"},

    # 专职副书记
    {"person_id": 3, "org_id": 1, "title": "托克托县委副书记（专职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "协助县委书记抓党的建设工作"},

    # 常务副县长
    {"person_id": 4, "org_id": 1, "title": "托克托县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "托克托县政府党组副书记、常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 纪委书记
    {"person_id": 5, "org_id": 5, "title": "托克托县委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 组织部长
    {"person_id": 6, "org_id": 7, "title": "托克托县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 宣传部长
    {"person_id": 7, "org_id": 8, "title": "托克托县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 统战部长
    {"person_id": 8, "org_id": 9, "title": "托克托县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 政法委书记
    {"person_id": 9, "org_id": 6, "title": "托克托县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 人武部长
    {"person_id": 10, "org_id": 1, "title": "托克托县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 10, "title": "托克托县人武部部长", "start_date": "", "end_date": "present", "rank": "", "note": ""},

    # 县委办主任
    {"person_id": 11, "org_id": 15, "title": "托克托县委常委、县委办主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 人大主任
    {"person_id": 12, "org_id": 3, "title": "托克托县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},

    # 政协主席
    {"person_id": 13, "org_id": 4, "title": "托克托县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS (all are "current overlap" — specific names needed for deeper analysis)
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "托克托县党政正职搭档: 县委书记与县长", "overlap_org": "中共托克托县委员会/托克托县人民政府", "overlap_period": "current"},
    # 县委副书记搭档关系
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与专职副书记", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
    # 县长与常务副县长
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长与常务副县长", "overlap_org": "托克托县人民政府", "overlap_period": "current"},
    # 县委常委班子 — 书记与常委
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委常委班子: 书记与常务副县长", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委常委班子: 书记与纪委书记", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委常委班子: 书记与组织部长", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委常委班子: 书记与宣传部长", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委常委班子: 书记与统战部长", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委常委班子: 书记与政法委书记", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委常委班子: 书记与人武部长", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委常委班子: 书记与县委办主任", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
    # 常委互连
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
    {"person_a": 5, "person_b": 9, "type": "overlap", "context": "县委常委班子: 纪委书记与政法委书记", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "县委常委班子: 组织部长与宣传部长", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
    {"person_a": 6, "person_b": 11, "type": "overlap", "context": "县委常委班子: 组织部长与县委办主任", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
    {"person_a": 11, "person_b": 1, "type": "overlap", "context": "县委办主任与县委书记", "overlap_org": "中共托克托县委员会", "overlap_period": "current"},
]

# ══════════════════════════════════════════════════════════════════════════════

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
    print("Build complete.")
