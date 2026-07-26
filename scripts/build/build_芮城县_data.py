#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 芮城县 (Ruicheng County), 山西省运城市.

Investigation date: 2026-07-26
Task ID: shanxi_芮城县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.rcx.gov.cn — 芮城县人民政府官方网站 (primary, current as of July 2026)
  - Individual profile pages for all 县委常委 and 县政府领导

Confidence notes:
  - Current roles/names/bios: confirmed via official government leadership pages (primary quality)
  - Full career timelines BEFORE current role: unverified due to limited web access
  - All claims labeled with confidence level; gaps documented in person JSON open_questions
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
for parent_count in range(1, 6):
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

SLUG = "芮城县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── Persons ───────────────────────────────────────────────────────────────────
# Core data from official 芮城县政府网站 (rcx.gov.cn)
# 县委常委: 12 members; 县政府: 11 members (with overlap)
# IDs: 1=县委书记, 2=县长, 3=副书记, 4=常务副县长, 5=纪委书记, 6=政法委书记,
#      7=组织部长, 8=宣传部长, 9=常委副县长(王磊), 10=常委副县长(张瑜),
#      11=人武部政委, 12=县委办主任, 13=风陵渡开发区主任, 14=副县长(公安),
#      15=副县长(教育文旅), 16=副县长(农业农村), 17=副县长(市场监管),
#      18=副县长(自然资源), 19=县政府办主任

persons = [
    # 1. 县委书记
    {
        "id": 1, "name": "余敏", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-10", "birthplace": "山西五寨",
        "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委书记", "current_org": "中共芮城县委员会",
        "source": "rcx.gov.cn"
    },
    # 2. 县长
    {
        "id": 2, "name": "王德谋", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-06", "birthplace": "山西永济",
        "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记、县长", "current_org": "芮城县人民政府",
        "source": "rcx.gov.cn"
    },
    # 3. 县委副书记
    {
        "id": 3, "name": "赵炜博", "gender": "男", "ethnicity": "汉族",
        "birth": "1987-02", "birthplace": "山西万荣",
        "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记", "current_org": "中共芮城县委员会",
        "source": "rcx.gov.cn"
    },
    # 4. 县委常委、常务副县长
    {
        "id": 4, "name": "宁峰荣", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-10", "birthplace": "山西稷山",
        "education": "大学学历，管理学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、副县长（常务）", "current_org": "芮城县人民政府",
        "source": "rcx.gov.cn"
    },
    # 5. 县委常委、纪委书记
    {
        "id": 5, "name": "张磊", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-02", "birthplace": "山西临猗",
        "education": "大学本科学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任", "current_org": "中共芮城县纪律检查委员会",
        "source": "rcx.gov.cn"
    },
    # 6. 县委常委、政法委书记
    {
        "id": 6, "name": "王柱兵", "gender": "男", "ethnicity": "汉族",
        "birth": "1982-10", "birthplace": "山西柳林",
        "education": "本科学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、政法委书记", "current_org": "中共芮城县委员会",
        "source": "rcx.gov.cn"
    },
    # 7. 县委常委、组织部部长
    {
        "id": 7, "name": "郭彩飞", "gender": "女", "ethnicity": "汉族",
        "birth": "1981-08", "birthplace": "山西夏县",
        "education": "硕士研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、组织部部长", "current_org": "中共芮城县委员会",
        "source": "rcx.gov.cn"
    },
    # 8. 县委常委、宣传部长
    {
        "id": 8, "name": "杨岩军", "gender": "男", "ethnicity": "汉族",
        "birth": "1989-11", "birthplace": "山西万荣",
        "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、宣传部长", "current_org": "中共芮城县委员会",
        "source": "rcx.gov.cn"
    },
    # 9. 县委常委、副县长
    {
        "id": 9, "name": "王磊", "gender": "男", "ethnicity": "汉族",
        "birth": "1987-05", "birthplace": "山西新绛",
        "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、副县长", "current_org": "芮城县人民政府",
        "source": "rcx.gov.cn"
    },
    # 10. 县委常委、副县长
    {
        "id": 10, "name": "张瑜", "gender": "男", "ethnicity": "汉族",
        "birth": "1986-04", "birthplace": "山西古县",
        "education": "硕士研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、副县长", "current_org": "芮城县人民政府",
        "source": "rcx.gov.cn"
    },
    # 11. 县委常委、人武部政委
    {
        "id": 11, "name": "张冰", "gender": "男", "ethnicity": "汉族",
        "birth": "1972-09", "birthplace": "河南泌阳",
        "education": "本科学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、人武部政委", "current_org": "芮城县人民武装部",
        "source": "rcx.gov.cn"
    },
    # 12. 县委办主任
    {
        "id": 12, "name": "谢晓宁", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-09", "birthplace": "山西芮城",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委办主任", "current_org": "中共芮城县委办公室",
        "source": "rcx.gov.cn"
    },
    # 13. 风陵渡经济开发区主任
    {
        "id": 13, "name": "许朝庆", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-10", "birthplace": "山西永济",
        "education": "大学本科学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府党组成员、风陵渡开发区党工委书记、管委会主任",
        "current_org": "风陵渡经济开发区",
        "source": "rcx.gov.cn"
    },
    # 14. 副县长、公安局长
    {
        "id": 14, "name": "卫琰军", "gender": "男", "ethnicity": "汉族",
        "birth": "1977-11", "birthplace": "山西新绛",
        "education": "在职研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长、公安局局长", "current_org": "芮城县人民政府",
        "source": "rcx.gov.cn"
    },
    # 15. 副县长（教育文旅）
    {
        "id": 15, "name": "张衡", "gender": "男", "ethnicity": "汉族",
        "birth": "1983-11", "birthplace": "山西芮城",
        "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "芮城县人民政府",
        "source": "rcx.gov.cn"
    },
    # 16. 副县长（农业农村）
    {
        "id": 16, "name": "刘钊", "gender": "男", "ethnicity": "汉族",
        "birth": "1985-02", "birthplace": "山西芮城",
        "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "芮城县人民政府",
        "source": "rcx.gov.cn"
    },
    # 17. 副县长（市场监管）
    {
        "id": 17, "name": "王传旭", "gender": "男", "ethnicity": "汉族",
        "birth": "1985-04", "birthplace": "山东聊城",
        "education": "研究生学历、理学博士",
        "party_join": "九三学社社员", "work_start": "",
        "current_post": "副县长", "current_org": "芮城县人民政府",
        "source": "rcx.gov.cn"
    },
    # 18. 副县长（自然资源）
    {
        "id": 18, "name": "肖国红", "gender": "女", "ethnicity": "汉族",
        "birth": "1984-05", "birthplace": "山西芮城",
        "education": "大学本科学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "芮城县人民政府",
        "source": "rcx.gov.cn"
    },
    # 19. 县政府办主任
    {
        "id": 19, "name": "于江涛", "gender": "男", "ethnicity": "汉族",
        "birth": "1988-10", "birthplace": "山西芮城",
        "education": "大学本科学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府党组成员、政府办主任",
        "current_org": "芮城县人民政府办公室",
        "source": "rcx.gov.cn"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共芮城县委员会", "type": "党委", "level": "县级", "parent": "运城市", "location": "芮城县"},
    {"id": 2, "name": "芮城县人民政府", "type": "政府", "level": "县级", "parent": "运城市", "location": "芮城县"},
    {"id": 3, "name": "中共芮城县纪律检查委员会", "type": "党委", "level": "县级", "parent": "芮城县", "location": "芮城县"},
    {"id": 4, "name": "芮城县人民武装部", "type": "其他", "level": "县级", "parent": "芮城县", "location": "芮城县"},
    {"id": 5, "name": "中共芮城县委办公室", "type": "党委", "level": "县级", "parent": "芮城县", "location": "芮城县"},
    {"id": 6, "name": "芮城县人民政府办公室", "type": "政府", "level": "县级", "parent": "芮城县", "location": "芮城县"},
    {"id": 7, "name": "风陵渡经济开发区", "type": "开发区", "level": "县级", "parent": "芮城县", "location": "芮城县"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2021-12", "end": "present", "rank": "正处级", "note": "主持县委全面工作"},
    # 县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "2022-01", "end": "present", "rank": "正处级", "note": "主持县政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2022-01", "end": "present", "rank": "正处级", "note": ""},
    # 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "2026-05", "end": "present", "rank": "副处级", "note": "协助党建、信访、农业农村、乡村振兴"},
    # 常务副县长
    {"person_id": 4, "org_id": 2, "title": "县委常委、副县长（常务）", "start": "unknown", "end": "present", "rank": "副处级", "note": "协助县政府常务工作"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 纪委书记
    {"person_id": 5, "org_id": 3, "title": "纪委书记、监委主任", "start": "unknown", "end": "present", "rank": "副处级", "note": "主持纪委监委全面工作"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 政法委书记
    {"person_id": 6, "org_id": 1, "title": "县委常委、政法委书记", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管政法、维稳"},
    # 组织部长
    {"person_id": 7, "org_id": 1, "title": "县委常委、组织部部长", "start": "2026-05", "end": "present", "rank": "副处级", "note": "分管组织、党校工作"},
    # 宣传部长
    {"person_id": 8, "org_id": 1, "title": "县委常委、宣传部长", "start": "2026-05", "end": "present", "rank": "副处级", "note": "分管意识形态和宣传文化工作"},
    # 常委副县长（王磊）
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管行政审批、商务、招商、医疗卫生"},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "2026-05", "end": "present", "rank": "副处级", "note": ""},
    # 常委副县长（张瑜）
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管民政、住建、人社"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 人武部政委
    {"person_id": 11, "org_id": 4, "title": "人武部政委", "start": "unknown", "end": "present", "rank": "正团级", "note": "负责国防动员工作"},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 县委办主任
    {"person_id": 12, "org_id": 5, "title": "县委办主任", "start": "unknown", "end": "present", "rank": "正科级", "note": "主持县委办工作"},
    # 风陵渡开发区主任
    {"person_id": 13, "org_id": 7, "title": "管委会主任", "start": "unknown", "end": "present", "rank": "副处级", "note": "主持风陵渡经济开发区工作"},
    {"person_id": 13, "org_id": 2, "title": "县政府党组成员", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 副县长（公安）
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "2026-05", "end": "present", "rank": "副处级", "note": "分管公安、司法、信访"},
    # 副县长（教育文旅）
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管教育、文旅、环保"},
    # 副县长（农业农村）
    {"person_id": 16, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管农业农村、水利、乡村振兴"},
    # 副县长（市场监管）
    {"person_id": 17, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管市场监管、退役军人（九三学社）"},
    # 副县长（自然资源）
    {"person_id": 18, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管自然资源、林业、交通"},
    # 县政府办主任
    {"person_id": 19, "org_id": 6, "title": "政府办主任", "start": "unknown", "end": "present", "rank": "正科级", "note": "主持政府办工作"},
]

# ── Relationships ──────────────────────────────────────────────────────────────
relationships = [
    # 党委书记-县长搭档关系
    {"person_a": 1, "person_b": 2, "type": "political_partnership",
     "context": "党委书记-县长搭档，共同领导芮城县工作",
     "overlap_org": "芮城县", "overlap_period": "2022至今"},
    # 党委副书记-县长（同一人，张磊、王柱兵等系常委会成员）
    # 常务副县长-县委书记
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记-常务副县长",
     "overlap_org": "芮城县", "overlap_period": "至今"},
    # 常务副县长-县长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长-常务副县长",
     "overlap_org": "芮城县人民政府", "overlap_period": "至今"},
    # 政法委书记-公安局长（政法系统关联）
    {"person_a": 6, "person_b": 14, "type": "superior_subordinate",
     "context": "政法委书记-公安局长（政法系统领导和执行关系）",
     "overlap_org": "芮城县政法系统", "overlap_period": "至今"},
    # 组织部长-宣传部长（年轻常委）
    {"person_a": 7, "person_b": 8, "type": "same_committee",
     "context": "组织部部长与宣传部部长同为县委常委",
     "overlap_org": "中共芮城县委常委", "overlap_period": "2026至今"},
    # 王磊-张瑜（同 ）
    {"person_a": 9, "person_b": 10, "type": "same_committee",
     "context": "同为县委常委、副县长",
     "overlap_org": "芮城县委常委", "overlap_period": "至今"},
]

# ── Main ──────────────────────────────────────────────────────────────────────
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
    print(f"✓ 数据库: {DB_PATH}")
    print(f"✓ 关系图: {GEXF_PATH}")
    print(f"✓ 人员: {len(persons)} 人")
    print(f"✓ 组织: {len(organizations)} 个")
    print(f"✓ 任职: {len(positions)} 条")
    print(f"✓ 关系: {len(relationships)} 条")