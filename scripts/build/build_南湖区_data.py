"""南湖区领导班子关系网络 — 构建脚本。

数据来源：
- 嘉兴市南湖区人民政府网站 (nanhu.gov.cn) — 2026年7-8月确认
- 南湖区具身智能生态建设推进会新闻 (2026-08-03) — 陈群伟、王志军、徐刚、陈裕
- 区委书记陈群伟进人大代表联络站新闻 (2026-07-21) — 陈群伟
- 区政府常务会议第63次新闻 (2026-07-20) — 王志军、王存乡、郁新喜、傅政霖、蒋伟、郑卓洲
- 街道行政区划调整动员会新闻 (2026-07-09) — 陈群伟、王志军、吴健、武曜云、斯科
- 台风"巴威"防御调度新闻 (2026-07-10) — 王志军 陈光振
- 南湖区－若尔盖县对口工作联席会议新闻 (2026-06-25) — 王志军 陈光振
- 百度百科 — 陈群伟（嘉兴南湖区委书记）、邵潘锋（前任书记→衢州市副市长）
- 维基百科 — 南湖区历史概况

数据时效：2026-08-03
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import sqlite3  # noqa: used by run_build internally

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

STAGING_DIR = Path(__file__).parent
SLUG = "南湖区"
DB_PATH = STAGING_DIR / "南湖区_network.db"
GEXF_PATH = STAGING_DIR / "南湖区_network.gexf"

# ═══════════════════════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════════════════════
PERSONS = [
    # ── 区委书记 ──
    {
        "id": 1,
        "name": "陈群伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976.11",
        "birthplace": "浙江嘉兴",
        "education": "大学本科，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共嘉兴市南湖区委员会",
        "source": "http://www.nanhu.gov.cn/col/col1570682/art/2026/art_c28d09e345cab4c31575122fbf207b77.html",
    },
    # ── 区委副书记、区长 ──
    {
        "id": 2,
        "name": "王志军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978.09",
        "birthplace": "浙江台州",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1999.08",
        "current_post": "区委副书记、区长",
        "current_org": "南湖区人民政府",
        "source": "http://www.nanhu.gov.cn/col/col1570682/art/2026/art_5caea3a923a4f362dd713e2f5589ee42.html",
    },
    # ── 副区长 ──
    {
        "id": 3,
        "name": "徐刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "南湖区人民政府",
        "source": "http://www.nanhu.gov.cn/col/col1570682/art/2026/art_0de64a2b2e45f2c0d162cd847a989c74.html",
    },
    # ── 副区长 ──
    {
        "id": 4,
        "name": "王存乡",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "南湖区人民政府",
        "source": "http://www.nanhu.gov.cn/col/col1570682/art/2026/art_5caea3a923a4f362dd713e2f5589ee42.html",
    },
    # ── 副区长 ──
    {
        "id": 5,
        "name": "郁新喜",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "南湖区人民政府",
        "source": "http://www.nanhu.gov.cn/col/col1570682/art/2026/art_5caea3a923a4f362dd713e2f5589ee42.html",
    },
    # ── 副区长 ──
    {
        "id": 6,
        "name": "傅政霖",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "南湖区人民政府",
        "source": "http://www.nanhu.gov.cn/col/col1570682/art/2026/art_5caea3a923a4f362dd713e2f5589ee42.html",
    },
    # ── 副区长 ──
    {
        "id": 7,
        "name": "蒋伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "南湖区人民政府",
        "source": "http://www.nanhu.gov.cn/col/col1570682/art/2026/art_5caea3a923a4f362dd713e2f5589ee42.html",
    },
    # ── 副区长 ──
    {
        "id": 8,
        "name": "郑卓洲",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "南湖区人民政府",
        "source": "http://www.nanhu.gov.cn/col/col1570682/art/2026/art_5caea3a923a4f362dd713e2f5589ee42.html",
    },
    # ── 区委接待（行政区划调整工作） ──
    {
        "id": 9,
        "name": "陈光振",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共嘉兴市南湖区委员会",
        "source": "http://www.nanhu.gov.cn/col/col1570682/art/2026/art_ce511efa772d0b9f2db5d9d2c5833a57.html",
    },
    # ── 区领导（区政协主席） ──
    {
        "id": 10,
        "name": "武曜云",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议嘉兴市南湖区委员会",
        "source": "http://www.nanhu.gov.cn/col/col1570682/art/2026/art_304ea4363ef4197f85cb37205a4dac1e.html",
    },
    # ── 区人大常委会主任 ──
    {
        "id": 11,
        "name": "吴健",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "嘉兴市南湖区人民代表大会常务委员会",
        "source": "http://www.nanhu.gov.cn/col/col1570682/art/2026/art_304ea4363ef4387f85cb37205a4dac1e.html",
    },
    # ── 区领导（区纪律检查委员会） ──
    {
        "id": 12,
        "name": "斯科",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共嘉兴市南湖区委员会",
        "source": "http://www.nanhu.gov.cn/col/col1570682/art/2026/art_304ea4363ef7197f85cb37205a4dac1e.html",
    },
    # ── 副区长（区领导） ──
    {
        "id": 13,
        "name": "陈裕",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共嘉兴市南湖区委员会",
        "source": "http://www.nanhu.gov.cn/col/col1570682/art/2026/art_0de64a2b2e45bbf9a300ee68d46b24.html",
    },
    # ── 前任区委书记（2021.11-2025.01） ──
    {
        "id": 14,
        "name": "邵潘锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977.04",
        "birthplace": "浙江永嘉",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1999.08",
        "current_post": "衢州市副市长",
        "current_org": "衢州市人民政府",
        "source": "https://baike.baidu.com/item/%E9%82%B5%E6%BD%98%E9%94%8B/63272896",
    },
]

# ═══════════════════════════════════════════════════════════════
# 组织机构数据
# ═══════════════════════════════════════════════════════════════
ORGANIZATIONS = [
    # ── 区委 ──
    {
        "id": 1,
        "name": "中共嘉兴市南湖区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共嘉兴市委员会",
        "location": "浙江省嘉兴市南湖区",
    },
    # ── 区政府 ──
    {
        "id": 2,
        "name": "南湖区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "嘉兴市人民政府",
        "location": "浙江省嘉兴市南湖区",
    },
    # ── 区人大 ──
    {
        "id": 3,
        "name": "嘉兴市南湖区人民代表大会",
        "type": "人大",
        "level": "县处级",
        "parent": "",
        "location": "浙江省嘉兴市南湖区",
    },
    # ── 区政协 ──
    {
        "id": 4,
        "name": "中国人民政治协商会议嘉兴市南湖区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "",
        "location": "浙江省嘉兴市南湖区",
    },
    # ── 衢州市政府（前任书记现任职） ──
    {
        "id": 5,
        "name": "衢州市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "浙江省人民政府",
        "location": "浙江省衢州市",
    },
]

# ═══════════════════════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════════════════════
POSITIONS = [
    # 陈群伟 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2025.01", "end_date": "", "rank": "副厅级", "note": "主持区委全面工作，据新闻报道2025年起任职"},
    # 王志军 — 区长
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "协助书记处置"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "领导区政府全面工作"},
    # 徐刚 — 常务副区长
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 王存乡 — 副区长
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 郁新喜 — 副区长
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 傅政霖 — 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 蒋伟 — 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 郑卓洲 — 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 陈光振 — 区委常委
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 武曜云 — 区政协主席
    {"person_id": 10, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 吴健 — 区人大常委会主任
    {"person_id": 11, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 斯科 — 区委常委
    {"person_id": 12, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 陈裕 — 区委常委
    {"person_id": 13, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 邵潘锋 — 前任区委书记
    {"person_id": 14, "org_id": 1, "title": "区委书记", "start_date": "2021.11", "end_date": "2025.01", "rank": "副厅级", "note": "赴衢州市任副市长"},
    {"person_id": 14, "org_id": 5, "title": "副市长", "start_date": "2025.01", "end_date": "", "rank": "副厅级", "note": "分管教育、卫生健康等工作"},
]

# ═══════════════════════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════════════════════
RELATIONSHIPS = [
    # 党政正职搭档 — 陈群伟 ↔ 王志军
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记与区长区政搭档", "overlap_org": "中共嘉兴市南湖区委员会", "overlap_period": "2025至今"},
    # 前任与现任
    {"person_a": 14, "person_b": 1, "type": "前任继任", "context": "邵潘锋接任南湖区委书记（2021-2025），陈群伟继任（2025至今）", "overlap_org": "中共嘉兴市南湖区委员会", "overlap_period": ""},
    # 陈群伟与各区委常委
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与区委常委/常务副区长", "overlap_org": "中共嘉兴市南湖区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记与区委常委", "overlap_org": "中共嘉兴市南湖区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "区委书记与区委常委", "overlap_org": "中共嘉兴市南湖区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "区委书记与区委常委", "overlap_org": "中共嘉兴市南湖区委员会", "overlap_period": ""},
    # 区长与副区长
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "区长与常务副区长", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "党政副职", "context": "区长与副区长", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "党政副职", "context": "区长与副区长", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "党政副职", "context": "区长与副区长", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "党政副职", "context": "区长与副区长", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "党政副职", "context": "区长与副区长", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    # 人大与区委
    {"person_a": 1, "person_b": 11, "type": "党政协调", "context": "区委书记与区人大主任", "overlap_org": "南湖区", "overlap_period": ""},
    # 政协与区委
    {"person_a": 1, "person_b": 10, "type": "党政协调", "context": "区委书记与区政协主席", "overlap_org": "南湖区", "overlap_period": ""},
    # 区长与前任书记
    {"person_a": 14, "person_b": 2, "type": "前任继任", "context": "前任区委书记对区长任务", "overlap_org": "中共嘉兴市南湖区委员会", "overlap_period": ""},
    # 副区长之间
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "副区长之间", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "副区长之间", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "同僚", "context": "副区长之间", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 8, "type": "同僚", "context": "副区长之间", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "副区长之间", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "副区长之间", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "副区长之间", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "副区长之间", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "副区长之间", "overlap_org": "南湖区人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "副区长之间", "overlap_org": "南湖区人民政府", "overlap_period": ""},
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
    print(f"      南湖区网络构建完成")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")