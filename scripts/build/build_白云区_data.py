#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 贵阳市白云区 leadership network.

Data sources:
- www.gzbaiyun.gov.cn (official government website)
- 领导之窗 (leadership window)
- Official leadership roster page

Information currency: 2026-07 (current as of July 2026)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "白云区"
DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────
# ID convention: sequential numeric IDs
persons = [
    # ── 区委领导班子 (District Party Committee) ──
    {
        "id": 1, "name": "步岚", "gender": "女", "ethnicity": "汉族",
        "birth": "1975", "birthplace": "河南鄢陵", "education": "研究生",
        "party_join": "", "work_start": "",
        "current_post": "贵阳市政协副主席、区委书记、白云经开区党工委书记",
        "current_org": "中共贵阳市白云区委员会",
        "source": "https://www.gzbaiyun.gov.cn/xwz/zwgk_5748401/",
    },
    {
        "id": 2, "name": "唐樾", "gender": "男", "ethnicity": "苗族",
        "birth": "1976", "birthplace": "贵州修文", "education": "大学",
        "party_join": "", "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "贵阳市白云区人民政府",
        "source": "https://www.gzbaiyun.gov.cn/xwz/zwgk_5748401/",
    },
    {
        "id": 3, "name": "陈俊", "gender": "男", "ethnicity": "汉族",
        "birth": "1983", "birthplace": "湖北石首", "education": "研究生",
        "party_join": "", "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "贵阳市白云区人民政府",
        "source": "https://www.gzbaiyun.gov.cn/xwz/zwgk_5748401/",
    },
    {
        "id": 4, "name": "周亮", "gender": "男", "ethnicity": "汉族",
        "birth": "1971", "birthplace": "湖南湘乡", "education": "大学",
        "party_join": "", "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "贵阳市白云区人民政府",
        "source": "https://www.gzbaiyun.gov.cn/xwz/zwgk_5748401/",
    },
    {
        "id": 5, "name": "谭德光", "gender": "男", "ethnicity": "汉族",
        "birth": "1984", "birthplace": "河南新蔡", "education": "大学",
        "party_join": "", "work_start": "",
        "current_post": "区委常委、副区长（挂职）",
        "current_org": "贵阳市白云区人民政府",
        "source": "https://www.gzbaiyun.gov.cn/xwz/zwgk_5748401/",
    },
    {
        "id": 6, "name": "刘咏松", "gender": "男", "ethnicity": "汉族",
        "birth": "1973", "birthplace": "贵州惠水", "education": "大学",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "贵阳市白云区人民政府",
        "source": "https://www.gzbaiyun.gov.cn/xwz/zwgk_5748401/",
    },
    {
        "id": 7, "name": "赵雪", "gender": "女", "ethnicity": "汉族",
        "birth": "1974", "birthplace": "贵州贵阳", "education": "大学",
        "party_join": "", "work_start": "",
        "current_post": "副区长",
        "current_org": "贵阳市白云区人民政府",
        "source": "https://www.gzbaiyun.gov.cn/xwz/zwgk_5748401/",
    },
    {
        "id": 8, "name": "陈安", "gender": "男", "ethnicity": "汉族",
        "birth": "1974", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长、区公安分局局长",
        "current_org": "贵阳市公安局白云分局",
        "source": "https://www.gzbaiyun.gov.cn/xwz/zwgk_5748401/",
    },
    {
        "id": 9, "name": "鄢皓", "gender": "男", "ethnicity": "汉族",
        "birth": "1988", "birthplace": "贵州贵阳", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长、麦架镇党委书记",
        "current_org": "贵阳市白云区人民政府、中共白云区麦架镇委员会",
        "source": "https://www.gzbaiyun.gov.cn/xwz/zwgk_5748401/",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共贵阳市白云区委员会", "type": "党委", "level": "县处级", "parent": "中共贵阳市委", "location": "贵阳市白云区"},
    {"id": 2, "name": "贵阳市白云区人民政府", "type": "政府", "level": "县处级", "parent": "贵阳市人民政府", "location": "贵阳市白云区"},
    {"id": 3, "name": "贵阳市政协", "type": "政协", "level": "地厅级", "parent": "贵州省政协", "location": "贵阳市"},
    {"id": 4, "name": "白云经济开发区党工委", "type": "开发区", "level": "县处级", "parent": "中共贵阳市委", "location": "贵阳市白云区"},
    {"id": 5, "name": "贵阳市公安局白云分局", "type": "政府", "level": "乡科级", "parent": "贵阳市公安局", "location": "贵阳市白云区"},
    {"id": 6, "name": "中共白云区麦架镇委员会", "type": "乡镇/街道", "level": "乡科级", "parent": "中共贵阳市白云区委员会", "location": "贵阳市白云区麦架镇"},
    {"id": 7, "name": "贵阳市白云区人大常委会", "type": "人大", "level": "县处级", "parent": "贵阳市人大常委会", "location": "贵阳市白云区"},
]

# ── Positions ─────────────────────────────────────────────────────────────
positions = [
    # 步岚
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "副厅级（高配）", "note": "兼贵阳市政协副主席、白云经开区党工委书记"},
    {"person_id": 1, "org_id": 3, "title": "贵阳市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 4, "title": "白云经开区党工委书记", "start": "", "end": "present", "rank": "", "note": ""},
    # 唐樾
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "县处级", "note": "区委副书记"},
    # 陈俊
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start": "", "end": "present", "rank": "县处级", "note": "区委常委"},
    # 周亮
    {"person_id": 4, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级", "note": "区委常委"},
    # 谭德光
    {"person_id": 5, "org_id": 2, "title": "副区长（挂职）", "start": "", "end": "present", "rank": "县处级", "note": "区委常委；挂职干部"},
    # 刘咏松
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 赵雪
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 陈安
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级", "note": "2026年7月任命"},
    {"person_id": 8, "org_id": 5, "title": "公安分局局长", "start": "", "end": "present", "rank": "乡科级", "note": ""},
    # 鄢皓
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "麦架镇党委书记", "start": "", "end": "present", "rank": "乡科级", "note": "兼"},
]

# ── Relationships ─────────────────────────────────────────────────────────
relationships = [
    # 步岚 <-> 唐樾：党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长党政正职搭档", "overlap_org": "中共贵阳市白云区委员会/白云区人民政府", "overlap_period": ""},
    # 步岚 <-> 陈俊：上下级
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与常务副区长", "overlap_org": "中共贵阳市白云区委员会", "overlap_period": ""},
    # 步岚 <-> 周亮：上下级
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与区委常委、副区长", "overlap_org": "中共贵阳市白云区委员会", "overlap_period": ""},
    # 唐樾 <-> 陈俊：上下级（区长与常务副区长）
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "区长与常务副区长", "overlap_org": "贵阳市白云区人民政府", "overlap_period": ""},
    # 唐樾 <-> 各副区长：上下级
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "贵阳市白云区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与挂职副区长", "overlap_org": "贵阳市白云区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "贵阳市白云区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "贵阳市白云区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "贵阳市白云区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "贵阳市白云区人民政府", "overlap_period": ""},
    # 步岚 <-> 唐樾：区委书记与区长搭档关系（confirmed）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长党政正职搭档", "overlap_org": "贵阳市白云区", "overlap_period": ""},
    # 陈俊 <-> 鄢皓：同为区委常委
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "同为区委常委", "overlap_org": "中共贵阳市白云区委员会", "overlap_period": ""},
    # 周亮 <-> 谭德光：同为区委常委
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "同为区委常委", "overlap_org": "中共贵阳市白云区委员会", "overlap_period": ""},
]

# ── Build ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sqlite3
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
