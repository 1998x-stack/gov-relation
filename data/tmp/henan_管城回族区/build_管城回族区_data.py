#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 管城回族区 leadership network.

管城回族区 - 郑州市 - 河南省
Targets: 区委书记刘利, 区长马东亮
"""

import sys
from pathlib import Path

# Ensure gov_relation is importable
_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import REPO_ROOT

SLUG = "管城回族区"
TASK_ID = "henan_管城回族区"

# ── Data ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "刘利",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "管城回族区委书记",
        "current_org": "中共郑州市管城回族区委员会",
        "source": "https://www.guancheng.gov.cn/gczw/10171154.jhtml",
    },
    {
        "id": 2,
        "name": "马东亮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "管城回族区委副书记、区政府区长",
        "current_org": "管城回族区人民政府",
        "source": "https://public.guancheng.gov.cn/D13X/1428660.jhtml",
    },
    # ── Government Leaders ──
    {
        "id": 3,
        "name": "李晓雷",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "管城回族区人民政府",
        "source": "https://public.guancheng.gov.cn/D13X/1438164.jhtml",
    },
    {
        "id": 4,
        "name": "张朝辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区政府党组成员、副区长",
        "current_org": "管城回族区人民政府",
        "source": "https://public.guancheng.gov.cn/D13X/1428611.jhtml",
    },
    {
        "id": 5,
        "name": "栗英",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长、管城公安分局局长",
        "current_org": "管城回族区人民政府",
        "source": "https://public.guancheng.gov.cn/D13X/7866922.jhtml",
    },
    {
        "id": 6,
        "name": "索琰琰",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "管城回族区人民政府",
        "source": "https://public.guancheng.gov.cn/D13X/10105664.jhtml",
    },
    {
        "id": 7,
        "name": "王子慧",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "管城回族区人民政府",
        "source": "https://public.guancheng.gov.cn/D13X/10064553.jhtml",
    },
    {
        "id": 8,
        "name": "李静",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "管城回族区人民政府",
        "source": "https://public.guancheng.gov.cn/D13X/5598952.jhtml",
    },
    # ── Party Leaders ──
    {
        "id": 9,
        "name": "关江娜",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "中共郑州市管城回族区委员会",
        "source": "https://www.guancheng.gov.cn/gczw/10171154.jhtml",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共郑州市管城回族区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共郑州市委员会",
        "location": "郑州市管城回族区",
    },
    {
        "id": 2,
        "name": "管城回族区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "郑州市人民政府",
        "location": "郑州市管城回族区",
    },
]

positions = [
    # 刘利
    {"person_id": 1, "org_id": 1, "title": "管城回族区委书记",
     "start_date": "", "end_date": "present", "rank": "正县处级",
     "note": "主持区委全面工作；2026年7月仍在任"},
    # 马东亮
    {"person_id": 2, "org_id": 2, "title": "管城回族区委副书记、区政府区长",
     "start_date": "", "end_date": "present", "rank": "正县处级",
     "note": "主持区政府全面工作；负责审计方面工作"},
    # 李晓雷
    {"person_id": 3, "org_id": 2, "title": "区委常委、常务副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": "主持区政府常务工作"},
    # 张朝辉
    {"person_id": 4, "org_id": 2, "title": "区委常委、区政府党组成员、副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": "负责工业发展、科技创新、对外开放、招商引资、商务、市场监管、食品安全、政务服务等"},
    # 栗英
    {"person_id": 5, "org_id": 2, "title": "副区长、管城公安分局局长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": "负责公安、司法、信访稳定等；二级高级警长"},
    # 索琰琰
    {"person_id": 6, "org_id": 2, "title": "区政府党组成员、副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": "负责民族宗教、民政、人力资源和社会保障、农业农村发展、生态水系、乡村振兴、生态环保等"},
    # 王子慧
    {"person_id": 7, "org_id": 2, "title": "区政府党组成员、副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": "负责自然资源和规划、城乡建设、住房保障、城市更新、城市管理、园林绿化等"},
    # 李静
    {"person_id": 8, "org_id": 2, "title": "副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": "负责教育、文化旅游、体育、文物、卫生健康、医疗保障等"},
    # 关江娜
    {"person_id": 9, "org_id": 1, "title": "区领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "陪同区委书记调研安全生产"},
]

relationships = [
    # 刘利 <-> 马东亮 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "区委书记与区长的党政工作搭档",
     "overlap_org": "管城回族区", "overlap_period": ""},
    # 刘利 <-> 张朝辉 (上下级)
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "区委书记与区委常委副区长；张朝辉陪同刘利调研安全生产",
     "overlap_org": "中共管城回族区委/区政府", "overlap_period": ""},
    # 刘利 <-> 关江娜 (上下级)
    {"person_a": 1, "person_b": 9, "type": "上下级",
     "context": "区委书记与区领导；关江娜陪同刘利调研安全生产",
     "overlap_org": "中共管城回族区委", "overlap_period": ""},
    # 马东亮 <-> 李晓雷 (区长-常务副区长)
    {"person_a": 2, "person_b": 3, "type": "上下级",
     "context": "区长与常务副区长的政府工作搭档",
     "overlap_org": "管城回族区人民政府", "overlap_period": ""},
    # 马东亮 <-> 张朝辉 (区长-副区长)
    {"person_a": 2, "person_b": 4, "type": "上下级",
     "context": "区长与区委常委副区长的政府工作搭档",
     "overlap_org": "管城回族区人民政府", "overlap_period": ""},
    # 马东亮 <-> 栗英 (区长-副区长/公安局长)
    {"person_a": 2, "person_b": 5, "type": "上下级",
     "context": "区长与副区长工作搭档",
     "overlap_org": "管城回族区人民政府", "overlap_period": ""},
    # 马东亮 <-> 索琰琰
    {"person_a": 2, "person_b": 6, "type": "上下级",
     "context": "区长与副区长工作搭档",
     "overlap_org": "管城回族区人民政府", "overlap_period": ""},
    # 马东亮 <-> 王子慧
    {"person_a": 2, "person_b": 7, "type": "上下级",
     "context": "区长与副区长工作搭档",
     "overlap_org": "管城回族区人民政府", "overlap_period": ""},
    # 马东亮 <-> 李静
    {"person_a": 2, "person_b": 8, "type": "上下级",
     "context": "区长与副区长工作搭档",
     "overlap_org": "管城回族区人民政府", "overlap_period": ""},
    # 李晓雷 <-> 张朝辉 (同为区委常委)
    {"person_a": 3, "person_b": 4, "type": "共事",
     "context": "同为区委常委，区政府领导班子成员",
     "overlap_org": "中共管城回族区委/区政府", "overlap_period": ""},
]


# ── Run Build ────────────────────────────────────────────────────────

if __name__ == "__main__":
    tmp_dir = REPO_ROOT / "data/tmp" / TASK_ID
    tmp_dir.mkdir(parents=True, exist_ok=True)

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=tmp_dir / f"{SLUG}_network.db",
        gexf_path=tmp_dir / f"{SLUG}_network.gexf",
        overwrite=True,
    )
    print(f"Build complete. Artifacts in {tmp_dir}/")
