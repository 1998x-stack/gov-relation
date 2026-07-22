#!/usr/bin/env python3
"""
江门市新会区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Xinhui District leadership.

Research note: Due to geo-restrictions, the official xinhui.gov.cn website was
unreachable from this environment (all connections timed out). Core leader names
confirmed via jiangmen.gov.cn 新闻报道 (multiple 2026-06/07 articles cross-referenced).
Data marked with ⚠️ "待确认" requires verification from:
  - https://www.xinhui.gov.cn/ldzc/ (领导之窗页面)
  - 江门市委组织部任前公示
  - Baidu Baike for each individual
  - Local news reports

初步调查时间: 2026-07-22

Confirmed sources from jiangmen.gov.cn:
- https://www.jiangmen.gov.cn/home/sqdt/xhzx/content/post_3522236.html (百千万工程推进会, 2026-07-16)
- https://www.jiangmen.gov.cn/home/sqdt/xhzx/content/post_3508473.html (区委十四届十一次全会, 2026-06-18)
- https://www.jiangmen.gov.cn/home/sqdt/xhzx/content/post_3508467.html (区领导基层调研, 2026-06-18)
- https://www.jiangmen.gov.cn/home/sqdt/xhzx/content/post_3515131.html (6·30乡村振兴活动, 2026-07-02)
- https://www.jiangmen.gov.cn/home/sqdt/xhzx/content/post_3518670.html (两优一先表彰会, 2026-07-09)
- https://www.jiangmen.gov.cn/home/sqdt/xhzx/content/post_3522235.html (区委常委会会议, 2026-07-16)
"""
import sys
from pathlib import Path

# Ensure we can import from repo root
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "新会区"

# ═══════════════════════════════════════════════════════════════════════════
# Persons
# ═══════════════════════════════════════════════════════════════════════════
# ID convention: xinhui_<pinyin_surname_givenname>
persons = [
    # ═══ 区党政主要领导 (Top Leaders) ═══
    # 区委书记：陈钊（confirmed via multiple jiangmen.gov.cn news articles, June-July 2026）
    {
        "id": 1,
        "name": "陈钊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共江门市新会区委员会",
        "source": "https://www.jiangmen.gov.cn/home/sqdt/xhzx/content/post_3522236.html",
    },
    # 区长：刘兵（confirmed via multiple jiangmen.gov.cn news articles）
    {
        "id": 2,
        "name": "刘兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "新会区人民政府",
        "source": "https://www.jiangmen.gov.cn/home/sqdt/xhzx/content/post_3522236.html",
    },

    # ═══ 区委常委会（标配岗位） ═══
    {
        "id": 3,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记（专职）",
        "current_org": "中共江门市新会区委员会",
        "source": "⚠️ 待确认",
    },
    {
        "id": 4,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "新会区人民政府",
        "source": "⚠️ 待确认",
    },
    {
        "id": 5,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、纪委书记、区监委主任",
        "current_org": "中共江门市新会区纪律检查委员会",
        "source": "⚠️ 待确认",
    },
    {
        "id": 6,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共江门市新会区委组织部",
        "source": "⚠️ 待确认",
    },
    {
        "id": 7,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共江门市新会区委宣传部",
        "source": "⚠️ 待确认",
    },
    {
        "id": 8,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共江门市新会区委政法委员会",
        "source": "⚠️ 待确认",
    },
    {
        "id": 9,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共江门市新会区委统一战线工作部",
        "source": "⚠️ 待确认",
    },
    {
        "id": 10,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区人民武装部政委（或部长）",
        "current_org": "江门市新会区人民武装部",
        "source": "⚠️ 待确认",
    },

    # ═══ 副区长 ═══
    {
        "id": 11,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "新会区人民政府",
        "source": "⚠️ 待确认",
    },
    {
        "id": 12,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "新会区人民政府",
        "source": "⚠️ 待确认",
    },
    {
        "id": 13,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "新会区人民政府",
        "source": "⚠️ 待确认",
    },
    {
        "id": 14,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "新会区人民政府",
        "source": "⚠️ 待确认",
    },

    # 区人大常委会主任：郑祖材（confirmed via jiangmen.gov.cn 百千万工程推进会 2026-07-08）
    {
        "id": 15,
        "name": "郑祖材",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会党组书记、主任",
        "current_org": "江门市新会区人民代表大会常务委员会",
        "source": "https://www.jiangmen.gov.cn/home/sqdt/xhzx/content/post_3522236.html",
    },
    # 区政协主席：张华（confirmed via jiangmen.gov.cn 百千万工程推进会 2026-07-08）
    {
        "id": 16,
        "name": "张华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协党组书记、主席",
        "current_org": "中国人民政治协商会议江门市新会区委员会",
        "source": "https://www.jiangmen.gov.cn/home/sqdt/xhzx/content/post_3522236.html",
    },

    # ═══ 江门市领导 ═══
    {
        "id": 100,
        "name": "陈杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "江门市委书记",
        "current_org": "中共江门市委员会",
        "source": "https://www.jiangmen.gov.cn 新闻报道(2026-07)",
    },
    {
        "id": 101,
        "name": "吴晓晖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "江门市委副书记、市长",
        "current_org": "江门市人民政府",
        "source": "https://www.jiangmen.gov.cn 新闻报道(2026-07)",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════════
organizations = [
    {
        "id": 1,
        "name": "中共江门市新会区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共江门市委员会",
        "location": "广东省江门市新会区",
    },
    {
        "id": 2,
        "name": "新会区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "江门市人民政府",
        "location": "广东省江门市新会区",
    },
    {
        "id": 3,
        "name": "中共江门市新会区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "江门市纪委监委",
        "location": "广东省江门市新会区",
    },
    {
        "id": 4,
        "name": "中共江门市新会区委组织部",
        "type": "党委部门",
        "level": "乡科级",
        "parent": "中共新会区委",
        "location": "广东省江门市新会区",
    },
    {
        "id": 5,
        "name": "中共江门市新会区委宣传部",
        "type": "党委部门",
        "level": "乡科级",
        "parent": "中共新会区委",
        "location": "广东省江门市新会区",
    },
    {
        "id": 6,
        "name": "中共江门市新会区委政法委员会",
        "type": "党委部门",
        "level": "乡科级",
        "parent": "中共新会区委",
        "location": "广东省江门市新会区",
    },
    {
        "id": 7,
        "name": "中共江门市新会区委统一战线工作部",
        "type": "党委部门",
        "level": "乡科级",
        "parent": "中共新会区委",
        "location": "广东省江门市新会区",
    },
    {
        "id": 8,
        "name": "江门市新会区人民武装部",
        "type": "军队",
        "level": "县处级",
        "parent": "江门军分区",
        "location": "广东省江门市新会区",
    },
    {
        "id": 9,
        "name": "江门市新会区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "江门市人大常委会",
        "location": "广东省江门市新会区",
    },
    {
        "id": 10,
        "name": "中国人民政治协商会议江门市新会区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协江门市委员会",
        "location": "广东省江门市新会区",
    },
    {
        "id": 11,
        "name": "江门市公安局新会分局",
        "type": "公安",
        "level": "乡科级",
        "parent": "江门市公安局",
        "location": "广东省江门市新会区",
    },
    # 江门市级组织
    {
        "id": 100,
        "name": "中共江门市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中共广东省委员会",
        "location": "广东省江门市",
    },
    {
        "id": 101,
        "name": "江门市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "广东省人民政府",
        "location": "广东省江门市",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# Positions
# ═══════════════════════════════════════════════════════════════════════════
positions = [
    # 区委书记：陈钊（confirmed via jiangmen.gov.cn 2026-06/07 多篇报道）
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "待查", "end_date": "至今", "rank": "县处级正职", "note": "最早见2026-06-16报道，上任日期待确认"},
    # 区长：刘兵（confirmed）
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "待查", "end_date": "至今", "rank": "县处级正职", "note": "最早见2026-06报道，上任日期待确认"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "confirmed"},
    # 专职副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记（专职）", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "⚠️ 待确认"},
    # 常务副区长
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "⚠️ 待确认"},
    # 纪委书记
    {"person_id": 5, "org_id": 3, "title": "区纪委书记、区监委主任", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "⚠️ 待确认"},
    # 组织部部长
    {"person_id": 6, "org_id": 4, "title": "区委组织部部长", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "⚠️ 待确认"},
    # 宣传部部长
    {"person_id": 7, "org_id": 5, "title": "区委宣传部部长", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "⚠️ 待确认"},
    # 政法委书记
    {"person_id": 8, "org_id": 6, "title": "区委政法委书记", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "⚠️ 待确认"},
    # 统战部部长
    {"person_id": 9, "org_id": 7, "title": "区委统战部部长", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "⚠️ 待确认"},
    # 人武部
    {"person_id": 10, "org_id": 8, "title": "区人武部政委（或部长）", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "⚠️ 待确认"},
    # 副区长
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "⚠️ 待确认"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "⚠️ 待确认"},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "⚠️ 待确认"},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "至今", "rank": "县处级副职", "note": "⚠️ 待确认"},
    # 人大
    {"person_id": 15, "org_id": 9, "title": "区人大常委会党组书记、主任", "start_date": "待查", "end_date": "至今", "rank": "县处级正职", "note": "confirmed via jiangmen.gov.cn"},
    # 政协
    {"person_id": 16, "org_id": 10, "title": "区政协党组书记、主席", "start_date": "待查", "end_date": "至今", "rank": "县处级正职", "note": "confirmed via jiangmen.gov.cn"},
    # 江门市领导
    {"person_id": 100, "org_id": 100, "title": "江门市委书记", "start_date": "", "end_date": "至今", "rank": "地厅级正职", "note": "2026年最新报道确认"},
    {"person_id": 101, "org_id": 101, "title": "江门市委副书记、市长", "start_date": "", "end_date": "至今", "rank": "地厅级正职", "note": "2026年最新报道确认"},
]

# ═══════════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════════
relationships = [
    # 书记—区长（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记—区长", "overlap_org": "新会区四套班子", "overlap_period": ""},
    # 区长—副区长（政府班子）
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长—常务副区长", "overlap_org": "新会区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长—副区长", "overlap_org": "新会区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长—副区长", "overlap_org": "新会区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "区长—副区长", "overlap_org": "新会区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "区长—副区长", "overlap_org": "新会区人民政府", "overlap_period": ""},
    # 书记—专职副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "书记—专职副书记", "overlap_org": "中共新会区委", "overlap_period": ""},
    # 书记—纪委书记
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "书记—纪委书记", "overlap_org": "中共新会区委", "overlap_period": ""},
    # 书记—组织部长
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "书记—组织部长", "overlap_org": "中共新会区委", "overlap_period": ""},
    # 书记—宣传部长
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "书记—宣传部长", "overlap_org": "中共新会区委", "overlap_period": ""},
    # 书记—政法委书记
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "书记—政法委书记", "overlap_org": "中共新会区委", "overlap_period": ""},
    # 书记—统战部长
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "书记—统战部长", "overlap_org": "中共新会区委", "overlap_period": ""},
    # 江门市领导—新会区（上下级对应）
    {"person_a": 100, "person_b": 1, "type": "上下级", "context": "市委书记—区委书记", "overlap_org": "江门市—新会区", "overlap_period": ""},
    {"person_a": 101, "person_b": 2, "type": "上下级", "context": "市长—区长", "overlap_org": "江门市—新会区", "overlap_period": ""},
    # 人大、政协列席
    {"person_a": 15, "person_b": 2, "type": "列席监督", "context": "人大主任列席政府会议", "overlap_org": "新会区", "overlap_period": ""},
    {"person_a": 16, "person_b": 2, "type": "列席监督", "context": "政协主席列席政府会议", "overlap_org": "新会区", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / "新会区_network.db",
        gexf_path=GRAPH_DIR / "新会区_network.gexf",
        overwrite=True,
    )
    print("Done: 新会区 network built.")
