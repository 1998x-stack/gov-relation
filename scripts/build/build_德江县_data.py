#!/usr/bin/env python3
"""Build script for 德江县 (Dejiang County, Tongren, Guizhou) leadership network.

Generated: 2026-07-23
Level: 县
Province: 贵州省
Parent City: 铜仁市
Targets: 县委书记 & 县长

Research Note (2026-07-23):
  Web sources were partially accessible:
  - Official site www.dejiang.gov.cn: accessible (homepage, news, leadership activities)
  - Leadership page: no dedicated /zwgk/ldzc/ page found (404)
  - Jina Reader: timed out
  - Exa: rate-limited
  - Bing/Baidu: traffic blocked for Chinese gov content queries

  Key findings via official site news ("今日德江" and general news columns):
  - 县委书记: 徐再高 — confirmed as top leader via multiple articles (调研社区治理,
    调研中考备考, 调研粮食生产, 走访慰问驻德部队, 率队赴浙江开展招商引资考察)
  - 县长: 敖华 — confirmed as 县委副书记、县长 via multiple articles (主持县政府会议,
    讲授思政课, 调研督导重点工作, 开展"六·一"慰问)
  - Additional confirmed leaders from 走访慰问 article that lists all four top positions:
    - 钱刚 — 县人大常委会主任
    - 李兵 — 县政协主席
    - 王刚祥 — 县领导 (likely 常务副县长 or 县委副书记)

  News articles from which leadership was confirmed (as displayed on website):
  - "徐再高敖华钱刚李兵王刚祥等县领导率队开展春节走访慰问活动并检查市场..."
  - "徐再高敖华调研义务教育优质均衡发展工作"
  - "徐再高调研中考备考和职业教育工作"
  - "敖华主持召开县政府党组（扩大）会议和常务会议"
  - "徐再高到城区调研社区治理和物业服务工作"
  - "徐再高深入乡镇调研粮食生产、产业发展、基层治理等重点工作"
  - "徐再高敖华率县四家班子走访慰问财税金融系统和企业干部职工"
  - "王刚祥带队赴浙江、上海、青岛招商考察"
  - "县委书记徐再高：立足"一心五城"谱写德江新篇"
  - "敖华在全县领导干部学习贯彻党的二十届四中全会精神专题轮训班上作专题..."
  - "徐再高李兵王刚祥等县领导开展高考巡考工作"
"""

import sqlite3  # noqa: used by gov_relation.runner
import sys
from pathlib import Path

# Ensure project root is on sys.path so gov_relation module can be imported
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "徐再高",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "德江县委书记",
        "current_org": "中共德江县委员会",
        "source": "德江县政府网 领导活动新闻 2026-07-23(首页); 《徐再高到城区调研社区治理和物业服务工作》; 《徐再高调研中考备考和职业教育工作》; 《徐再高深入乡镇调研粮食生产、产业发展、基层治理等重点工作》",
    },
    {
        "id": 2,
        "name": "敖华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "德江县委副书记、县长",
        "current_org": "德江县人民政府",
        "source": "德江县政府网 领导活动新闻 2026-07-23(首页); 《县政府召开党组（扩大）会议和常务会议》; 《敖华在全县领导干部学习贯彻党的二十届四中全会精神专题轮训班上作专题...》; 《敖华调研督导当前重点工作》",
    },
    {
        "id": 3,
        "name": "钱刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "德江县人大常委会主任",
        "current_org": "德江县人大常委会",
        "source": "德江县政府网 新闻《徐再高敖华钱刚李兵王刚祥等县领导率队开展春节走访慰问活动》",
    },
    {
        "id": 4,
        "name": "李兵",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "德江县政协主席",
        "current_org": "政协德江县委员会",
        "source": "德江县政府网 新闻《徐再高敖华钱刚李兵王刚祥等县领导率队开展春节走访慰问活动》; 《徐再高李兵王刚祥等县领导开展高考巡考工作》",
    },
    {
        "id": 5,
        "name": "王刚祥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "德江县领导（推测：常务副县长或县委副书记）",
        "current_org": "德江县人民政府",
        "source": "德江县政府网 新闻《王刚祥督导检查企业安全生产工作》; 《王刚祥带队赴浙江、上海、青岛招商考察》; 《徐再高敖华钱刚李兵王刚祥等县领导率队开展春节走访慰问活动》",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共德江县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共铜仁市委员会",
        "location": "贵州省铜仁市德江县",
    },
    {
        "id": 2,
        "name": "德江县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "铜仁市人民政府",
        "location": "贵州省铜仁市德江县",
    },
    {
        "id": 3,
        "name": "德江县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "铜仁市人大常委会",
        "location": "贵州省铜仁市德江县",
    },
    {
        "id": 4,
        "name": "政协德江县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协铜仁市委员会",
        "location": "贵州省铜仁市德江县",
    },
]

POSITIONS = [
    # 徐再高 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "德江县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "current as of 2026-07; exact appointment date unknown"},
    # 敖华 — 县长（兼县委副书记）
    {"person_id": 2, "org_id": 1, "title": "德江县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "concurrent with 县长 role"},
    {"person_id": 2, "org_id": 2, "title": "德江县县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "current as of 2026-07; exact appointment date unknown"},
    # 钱刚 — 人大主任
    {"person_id": 3, "org_id": 3, "title": "德江县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": "current as of 2026-07"},
    # 李兵 — 政协主席
    {"person_id": 4, "org_id": 4, "title": "德江县政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": "current as of 2026-07"},
    # 王刚祥 — 县领导
    {"person_id": 5, "org_id": 2, "title": "德江县领导（推测：常务副县长或县委副书记）", "start_date": "", "end_date": "present", "rank": "副县级或正县级", "note": "current as of 2026-07; exact title not confirmed"},
]

RELATIONSHIPS = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记—县长搭班子",
        "overlap_org": "中共德江县委员会/德江县人民政府",
        "overlap_period": "current（截至2026-07）",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "县委—人大 班子共事",
        "overlap_org": "德江县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "县委—政协 班子共事",
        "overlap_org": "德江县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委—政府领导 班子共事",
        "overlap_org": "德江县党政领导班子",
        "overlap_period": "current（截至2026-07）",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "政府—人大 班子共事",
        "overlap_org": "德江县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "政府—政协 班子共事",
        "overlap_org": "德江县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "政府班子共事",
        "overlap_org": "德江县人民政府",
        "overlap_period": "current（截至2026-07）",
    },
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "人大—政协 班子共事",
        "overlap_org": "德江县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
    {
        "person_a": 3, "person_b": 5,
        "type": "overlap",
        "context": "人大—政府 班子共事",
        "overlap_org": "德江县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
    {
        "person_a": 4, "person_b": 5,
        "type": "overlap",
        "context": "政协—政府 班子共事",
        "overlap_org": "德江县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
]

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

SLUG = "德江县"

TMP_DIR = Path(__file__).resolve().parent
DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

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

print(f"Done: {DB_PATH}, {GEXF_PATH}")
