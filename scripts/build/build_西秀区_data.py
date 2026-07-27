#!/usr/bin/env python3
"""Build script for 西秀区 (Xixiu District, Anshun, Guizhou) leadership network.

Generated: 2026-07-23
Level: 市辖区
Province: 贵州省
Parent City: 安顺市
Targets: 区委书记 & 区长

Research Note (2026-07-23):
  Web sources for 西秀区 were partially accessible:
  - Official site www.xixiu.gov.cn: accessible (homepage, news, gov info)
  - Leadership page (/web2023/zwgk/ldzc2/): blocked by JS rendering
  - Jina Reader: timed out
  - Baidu Baike: unreachable from this environment
  - Exa: rate-limited

  Key findings via official site news articles:
  - 区委书记 朱煜 confirmed via news article "朱煜调研安全生产、未成年人保护和防溺水工作" (2026-07-17)
  - 区长 position appears VACANT as of 2026-07; 常务副区长 朱光云 "主持区人民政府全面工作"
  - Deputy District Mayors: 何玉尤, 吴凤琴, 胡雪, 黄龙, 周仪, 吕杰 (from leadership page)
  - 区委副书记 饶雪 confirmed via news article
  - 区领导 孙亮 mentioned in news article (2026-07-20)

Sources:
  - https://www.xixiu.gov.cn/ — official government website
  - https://www.xixiu.gov.cn/web2023/zwgk/ldzc2/ — leadership page (partially accessible)
  - https://www.xixiu.gov.cn/web2023/xwzx/jrxx/ — news section
"""

import sqlite3  # noqa: used by gov_relation.runner
from pathlib import Path

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
        "name": "朱煜",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安顺市委常委、西秀区委书记",
        "current_org": "中共安顺市西秀区委员会",
        "source": "新闻《朱煜调研安全生产、未成年人保护和防溺水工作》西秀区政府网 2026-07-17; 标题称【市委常委、区委书记朱煜】",
    },
    {
        "id": 2,
        "name": "【待查】西秀区区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西秀区区长（空缺，由常务副区长主持工作）",
        "current_org": "安顺市西秀区人民政府",
        "source": "西秀区政府领导之窗页面，显示区长空缺，常务副区长朱光云【主持区人民政府全面工作】",
    },
    # ── Deputy Leaders ──
    {
        "id": 3,
        "name": "饶雪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西秀区委副书记",
        "current_org": "中共安顺市西秀区委员会",
        "source": "新闻《朱煜调研安全生产、未成年人保护和防溺水工作》西秀区政府网 2026-07-17",
    },
    {
        "id": 4,
        "name": "朱光云",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西秀区委常委、常务副区长（主持区政府全面工作）",
        "current_org": "安顺市西秀区人民政府",
        "source": "西秀区政府领导之窗页面，2026-07-23",
    },
    {
        "id": 5,
        "name": "孙亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西秀区领导",
        "current_org": "中共安顺市西秀区委员会",
        "source": "新闻《西秀区黄腊乡村庚陆活动》西秀区政府网 2026-07-20",
    },
    {
        "id": 6,
        "name": "何玉尤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西秀区副区长",
        "current_org": "安顺市西秀区人民政府",
        "source": "西秀区政府领导之窗页面，2026-07-23",
    },
    {
        "id": 7,
        "name": "吴凤琴",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西秀区副区长",
        "current_org": "安顺市西秀区人民政府",
        "source": "西秀区政府领导之窗页面; 新闻《西秀区黄腊乡村庚陆活动》2026-07-20",
    },
    {
        "id": 8,
        "name": "胡雪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西秀区副区长",
        "current_org": "安顺市西秀区人民政府",
        "source": "西秀区政府领导之窗页面，2026-07-23",
    },
    {
        "id": 9,
        "name": "黄龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西秀区副区长",
        "current_org": "安顺市西秀区人民政府",
        "source": "西秀区政府领导之窗页面; 新闻《朱煜调研安全生产、未成年人保护和防溺水工作》2026-07-17",
    },
    {
        "id": 10,
        "name": "周仪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西秀区副区长",
        "current_org": "安顺市西秀区人民政府",
        "source": "西秀区政府领导之窗页面，2026-07-23",
    },
    {
        "id": 11,
        "name": "吕杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西秀区副区长",
        "current_org": "安顺市西秀区人民政府",
        "source": "西秀区政府领导之窗页面，2026-07-23",
    },
    # ── Gap: Standing Committee members ──
    {
        "id": 12,
        "name": "【待查】西秀区纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西秀区委常委、纪委书记（待查）",
        "current_org": "中共安顺市西秀区纪律检查委员会",
        "source": "GAP — 待后续通过领导之窗页面补充",
    },
    {
        "id": 13,
        "name": "【待查】西秀区委组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西秀区委常委、组织部长（待查）",
        "current_org": "中共安顺市西秀区委组织部",
        "source": "GAP — 待后续通过领导之窗页面补充",
    },
    {
        "id": 14,
        "name": "【待查】西秀区委宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西秀区委常委、宣传部长（待查）",
        "current_org": "中共安顺市西秀区委宣传部",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 15,
        "name": "【待查】西秀区委政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西秀区委常委、政法委书记（待查）",
        "current_org": "中共安顺市西秀区委政法委员会",
        "source": "GAP — 待后续补充",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共安顺市委员会", "type": "党委", "level": "地厅级", "parent": "中共贵州省委员会", "location": "安顺市"},
    {"id": 2, "name": "中共安顺市西秀区委员会", "type": "党委", "level": "正处级", "parent": "中共安顺市委员会", "location": "安顺市西秀区"},
    {"id": 3, "name": "安顺市西秀区人民政府", "type": "政府", "level": "正处级", "parent": "安顺市人民政府", "location": "安顺市西秀区"},
    {"id": 4, "name": "中共安顺市西秀区纪律检查委员会", "type": "纪委", "level": "副处级", "parent": "中共安顺市纪律检查委员会", "location": "安顺市西秀区"},
    {"id": 5, "name": "中共安顺市西秀区委组织部", "type": "党委", "level": "正科级", "parent": "中共安顺市西秀区委员会", "location": "安顺市西秀区"},
    {"id": 6, "name": "中共安顺市西秀区委宣传部", "type": "党委", "level": "正科级", "parent": "中共安顺市西秀区委员会", "location": "安顺市西秀区"},
    {"id": 7, "name": "中共安顺市西秀区委政法委员会", "type": "党委", "level": "正科级", "parent": "中共安顺市西秀区委员会", "location": "安顺市西秀区"},
]

POSITIONS = [
    # 朱煜 — 区委书记（兼市常委）
    {"person_id": 1, "org_id": 1, "title": "安顺市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼任"},
    {"person_id": 1, "org_id": 2, "title": "西秀区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # GAP — 区长（空缺）
    {"person_id": 2, "org_id": 3, "title": "西秀区区长（空缺）", "start_date": "", "end_date": "present", "rank": "正处级", "note": "空缺中，由常务副区长主持工作"},
    # 饶雪 — 区委副书记
    {"person_id": 3, "org_id": 2, "title": "西秀区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 朱光云 — 常务副区长
    {"person_id": 4, "org_id": 2, "title": "西秀区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "西秀区常务副区长（主持区政府全面工作）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区长空缺期间主持政府全面工作"},
    # 孙亮 — 区领导
    {"person_id": 5, "org_id": 2, "title": "西秀区领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    # 何玉尤 — 副区长
    {"person_id": 6, "org_id": 3, "title": "西秀区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 吴凤琴 — 副区长
    {"person_id": 7, "org_id": 3, "title": "西秀区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 胡雪 — 副区长
    {"person_id": 8, "org_id": 3, "title": "西秀区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 黄龙 — 副区长
    {"person_id": 9, "org_id": 3, "title": "西秀区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 周仪 — 副区长
    {"person_id": 10, "org_id": 3, "title": "西秀区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 吕杰 — 副区长
    {"person_id": 11, "org_id": 3, "title": "西秀区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # GAP — 纪委书记
    {"person_id": 12, "org_id": 4, "title": "西秀区纪委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 组织部长
    {"person_id": 13, "org_id": 5, "title": "西秀区委组织部长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "GAP — 姓名未知"},
    # GAP — 宣传部长
    {"person_id": 14, "org_id": 6, "title": "西秀区委宣传部长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "GAP — 姓名未知"},
    # GAP — 政法委书记
    {"person_id": 15, "org_id": 7, "title": "西秀区委政法委书记", "start_date": "", "end_date": "present", "rank": "正科级", "note": "GAP — 姓名未知"},
]

RELATIONSHIPS = [
    # 朱煜 — 党政正职搭档（空缺）
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记与区长（空缺中）", "overlap_org": "西秀区四套班子", "overlap_period": "", "source": "区政府领导之窗", "confidence": "unverified"},
    # 朱煜 — 饶雪（上下级）
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与专职副书记", "overlap_org": "西秀区委常委会", "overlap_period": "2026", "source": "新闻", "confidence": "confirmed"},
    # 朱煜 — 朱光云（上下级）
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与常务副区长", "overlap_org": "西秀区委常委会", "overlap_period": "2026", "source": "领导之窗", "confidence": "confirmed"},
    # 朱光云 — 副区长们（政府班子）
    {"person_a": 4, "person_b": 6, "type": "政府班子", "context": "常务副区长与副区长", "overlap_org": "西秀区人民政府", "overlap_period": "2026", "source": "领导之窗", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 7, "type": "政府班子", "context": "常务副区长与副区长", "overlap_org": "西秀区人民政府", "overlap_period": "2026", "source": "领导之窗", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 8, "type": "政府班子", "context": "常务副区长与副区长", "overlap_org": "西秀区人民政府", "overlap_period": "2026", "source": "领导之窗", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 9, "type": "政府班子", "context": "常务副区长与副区长", "overlap_org": "西秀区人民政府", "overlap_period": "2026", "source": "领导之窗", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 10, "type": "政府班子", "context": "常务副区长与副区长", "overlap_org": "西秀区人民政府", "overlap_period": "2026", "source": "领导之窗", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 11, "type": "政府班子", "context": "常务副区长与副区长", "overlap_org": "西秀区人民政府", "overlap_period": "2026", "source": "领导之窗", "confidence": "confirmed"},
    # 吴凤琴 — 孙亮（同事）
    {"person_a": 7, "person_b": 5, "type": "同事", "context": "共同出席黄腊乡活动", "overlap_org": "西秀区", "overlap_period": "2026-07", "source": "新闻", "confidence": "confirmed"},
    # 黄龙 — 朱煜（上下级）
    {"person_a": 9, "person_b": 1, "type": "上下级", "context": "黄龙陪同朱煜调研安全生产", "overlap_org": "西秀区委", "overlap_period": "2026-07", "source": "新闻", "confidence": "confirmed"},
    # 饶雪 — 朱煜（上下级）
    {"person_a": 3, "person_b": 1, "type": "上级", "context": "饶雪以区委副书记身份陪同朱煜调研", "overlap_org": "西秀区委", "overlap_period": "2026-07", "source": "新闻", "confidence": "confirmed"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "西秀区_network.db"
GEXF_PATH = STAGING_DIR / "西秀区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="西秀区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
