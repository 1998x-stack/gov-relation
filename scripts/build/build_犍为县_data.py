#!/usr/bin/env python3
"""犍为县领导班子工作关系网络 — 数据构建脚本

Research sources:
- 犍为县人民政府官网 (www.qianwei.gov.cn)
- 乐山市人民政府官网 (www.leshan.gov.cn)
- 犍为县政协十一届六次会议开幕新闻 (2026-01-28)
- 犍为县"两优一先"表彰大会新闻 (2026-06-30)
"""

import sys
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "犍为县"
STAGING_DIR = Path(__file__).parent

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # 县委书记（兼乐山市副市长）
    {
        "id": 1,
        "name": "徐岳泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-02",
        "birthplace": "",
        "education": "党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "乐山市副市长、犍为县委书记",
        "current_org": "中共犍为县委员会",
        "source": "https://www.leshan.gov.cn/lsswszf/fsz/810541026099269.html",
    },
    # 县长
    {
        "id": 2,
        "name": "贾东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-11",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "犍为县委副书记、县长",
        "current_org": "犍为县人民政府",
        "source": "http://www.qianwei.gov.cn/qwx/leaderStp/leader_index.shtml",
    },
    # 县委副书记
    {
        "id": 3,
        "name": "干世伦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "犍为县委副书记",
        "current_org": "中共犍为县委员会",
        "source": "http://www.qianwei.gov.cn/qwx/jrqw/202606/856cb2595c4546fcafb67f7d4ecc5d79.shtml",
    },
    # 常务副县长
    {
        "id": 4,
        "name": "罗卉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981-06",
        "birthplace": "",
        "education": "党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "犍为县委常委、常务副县长",
        "current_org": "犍为县人民政府",
        "source": "http://www.qianwei.gov.cn/qwx/leaderWyb/leader_index.shtml",
    },
    # 副县长(挂职)
    {
        "id": 5,
        "name": "王勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-01",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "犍为县委常委、副县长（挂职）",
        "current_org": "犍为县人民政府",
        "source": "http://www.qianwei.gov.cn/qwx/wys/leader_index.shtml",
    },
    # 副县长(挂职)
    {
        "id": 6,
        "name": "匡怡蒙",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1989-05",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "犍为县委常委、副县长（挂职）",
        "current_org": "犍为县人民政府",
        "source": "http://www.qianwei.gov.cn/qwx/leaderKym/leader_index.shtml",
    },
    # 副县长（公安）
    {
        "id": 7,
        "name": "张勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-10",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "犍为县政府副县长、党组成员",
        "current_org": "犍为县人民政府",
        "source": "http://www.qianwei.gov.cn/qwx/leaderWj/leader_index.shtml",
    },
    # 副县长（无党派）
    {
        "id": 8,
        "name": "周锐",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-05",
        "birthplace": "",
        "education": "在职大学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "犍为县政府副县长",
        "current_org": "犍为县人民政府",
        "source": "http://www.qianwei.gov.cn/qwx/leaderFm/leader_index.shtml",
    },
    # 副县长
    {
        "id": 9,
        "name": "刘红英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976-08",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "犍为县政府副县长、党组成员",
        "current_org": "犍为县人民政府",
        "source": "http://www.qianwei.gov.cn/qwx/lhy/leader_index.shtml",
    },
    # 副县长
    {
        "id": 10,
        "name": "李佳驹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990-07",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "犍为县政府副县长、党组成员",
        "current_org": "犍为县人民政府",
        "source": "http://www.qianwei.gov.cn/qwx/leaderLjj/leader_index.shtml",
    },
    # 副县长
    {
        "id": 11,
        "name": "刘超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-09",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "犍为县政府副县长、党组成员",
        "current_org": "犍为县人民政府",
        "source": "http://www.qianwei.gov.cn/qwx/leaderLC/leader_index.shtml",
    },
    # 县政府党组成员、办公室主任
    {
        "id": 12,
        "name": "朱文权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-11",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "犍为县政府党组成员、办公室主任",
        "current_org": "犍为县人民政府",
        "source": "http://www.qianwei.gov.cn/qwx/leaderZc/leader_index.shtml",
    },
    # 县人大常委会主任
    {
        "id": 13,
        "name": "缪骏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "犍为县人大常委会主任",
        "current_org": "犍为县人大常委会",
        "source": "http://www.qianwei.gov.cn/qwx/jrqw/202601/3f58803f7262463faf049caf6d7b4664.shtml",
    },
    # 县政协主席
    {
        "id": 14,
        "name": "冯柏清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "犍为县政协主席",
        "current_org": "政协犍为县委员会",
        "source": "http://www.qianwei.gov.cn/qwx/jrqw/202601/3f58803f7262463faf049cafbaf7b4664.shtml",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共犍为县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共乐山市委",
        "location": "犍为县",
    },
    {
        "id": 2,
        "name": "犍为县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "乐山市人民政府",
        "location": "犍为县",
    },
    {
        "id": 3,
        "name": "犍为县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "乐山市人大常委会",
        "location": "犍为县",
    },
    {
        "id": 4,
        "name": "政协犍为县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协乐山市委员会",
        "location": "犍为县",
    },
    {
        "id": 5,
        "name": "乐山市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "四川省人民政府",
        "location": "乐山市",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 徐岳泉 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "犍为县委书记", "start": "", "end": "", "rank": "正处级", "note": "兼乐山市副市长"},
    {"person_id": 1, "org_id": 5, "title": "乐山市副市长", "start": "", "end": "", "rank": "副厅级", "note": "兼任犍为县委书记"},
    # 贾东 — 县长
    {"person_id": 2, "org_id": 1, "title": "犍为县委副书记", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "犍为县县长", "start": "", "end": "", "rank": "正处级", "note": "县政府党组书记"},
    # 干世伦 — 县委专职副书记
    {"person_id": 3, "org_id": 1, "title": "犍为县委副书记", "start": "", "end": "", "rank": "副处级", "note": "专职副书记"},
    # 罗卉 — 常务副县长
    {"person_id": 4, "org_id": 1, "title": "犍为县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "犍为县常务副县长", "start": "", "end": "", "rank": "副处级", "note": "县政府党组副书记"},
    # 王勇 — 挂职副县长
    {"person_id": 5, "org_id": 1, "title": "犍为县委常委", "start": "", "end": "", "rank": "副处级", "note": "挂职"},
    {"person_id": 5, "org_id": 2, "title": "犍为县副县长（挂职）", "start": "", "end": "", "rank": "副处级", "note": "挂职"},
    # 匡怡蒙 — 挂职副县长
    {"person_id": 6, "org_id": 1, "title": "犍为县委常委", "start": "", "end": "", "rank": "副处级", "note": "挂职"},
    {"person_id": 6, "org_id": 2, "title": "犍为县副县长（挂职）", "start": "", "end": "", "rank": "副处级", "note": "挂职"},
    # 其他副县长
    {"person_id": 7, "org_id": 2, "title": "犍为县副县长", "start": "", "end": "", "rank": "副处级", "note": "党组成员，分管公安"},
    {"person_id": 8, "org_id": 2, "title": "犍为县副县长", "start": "", "end": "", "rank": "副处级", "note": "无党派"},
    {"person_id": 9, "org_id": 2, "title": "犍为县副县长", "start": "", "end": "", "rank": "副处级", "note": "党组成员"},
    {"person_id": 10, "org_id": 2, "title": "犍为县副县长", "start": "", "end": "", "rank": "副处级", "note": "党组成员"},
    {"person_id": 11, "org_id": 2, "title": "犍为县副县长", "start": "", "end": "", "rank": "副处级", "note": "党组成员"},
    # 县政府办主任
    {"person_id": 12, "org_id": 2, "title": "犍为县政府党组成员、办公室主任", "start": "", "end": "", "rank": "正科级", "note": ""},
    # 县人大主任
    {"person_id": 13, "org_id": 3, "title": "犍为县人大常委会主任", "start": "", "end": "", "rank": "正处级", "note": ""},
    # 县政协主席
    {"person_id": 14, "org_id": 4, "title": "犍为县政协主席", "start": "", "end": "", "rank": "正处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 党政搭：徐岳泉 — 贾东
    {"person_a": 1, "person_b": 2, "type": "党政搭", "context": "县委书记—县长党政搭档", "overlap_org": "中共犍为县委/县政府", "overlap_period": ""},
    # 书记 — 专职副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记—县委专职副书记", "overlap_org": "中共犍为县委", "overlap_period": ""},
    # 县长 — 专职副书记
    {"person_a": 2, "person_b": 3, "type": "党政搭", "context": "县长—县委专职副书记", "overlap_org": "县委常委会", "overlap_period": ""},
    # 县长 — 常务副县长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长—常务副县长", "overlap_org": "犍为县政府", "overlap_period": ""},
    # 书记 — 常务副县长(常委)
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记—县委常委/常务副县长", "overlap_org": "县委常委会", "overlap_period": ""},
    # 书记 — 挂职常委(王勇)
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记—挂职常委", "overlap_org": "县委常委会", "overlap_period": ""},
    # 书记 — 挂职常委(匡怡蒙)
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记—挂职常委", "overlap_org": "县委常委会", "overlap_period": ""},
    # 人大主任 — 书记
    {"person_a": 1, "person_b": 13, "type": "同级协作", "context": "县委书记—县人大主任", "overlap_org": "县四大班子", "overlap_period": ""},
    # 政协主席 — 书记
    {"person_a": 1, "person_b": 14, "type": "同级协作", "context": "县委书记—县政协主席", "overlap_org": "县四大班子", "overlap_period": ""},
    # 县长 — 人大主任
    {"person_a": 2, "person_b": 13, "type": "同级协作", "context": "县长—县人大主任", "overlap_org": "县四大班子", "overlap_period": ""},
    # 县长 — 政协主席
    {"person_a": 2, "person_b": 14, "type": "同级协作", "context": "县长—县政协主席", "overlap_org": "县四大班子", "overlap_period": ""},
    # 常务副县长 — 各副县长
    {"person_a": 4, "person_b": 7, "type": "上下级", "context": "常务副县长—副县长", "overlap_org": "县政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 8, "type": "上下级", "context": "常务副县长—副县长", "overlap_org": "县政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 9, "type": "上下级", "context": "常务副县长—副县长", "overlap_org": "县政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 10, "type": "上下级", "context": "常务副县长—副县长", "overlap_org": "县政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 11, "type": "上下级", "context": "常务副县长—副县长", "overlap_org": "县政府", "overlap_period": ""},
]

# process_tmp validation tokens
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
import sqlite3

# ── Execute ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    db_path = DB_PATH
    gexf_path = GEXF_PATH

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )
    print(f"\n✅ Build complete: {SLUG}")
    print(f"   DB:   {db_path}")
    print(f"   GEXF: {gexf_path}")