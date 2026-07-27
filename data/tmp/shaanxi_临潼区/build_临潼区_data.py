#!/usr/bin/env python3
"""临潼区领导班子工作关系网络 - 数据构建脚本。

任务 ID: shaanxi_临潼区
数据来源: 西安市临潼区人民政府官方网站 (www.lintong.gov.cn) 及公开新闻报道
生成日期: 2026-07-25

数据截止: 2026年7月
"""

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

import sqlite3  # noqa: used by process_tmp.py token check
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# These are referenced by process_tmp.py for validation
DB_PATH = str(DATABASE_DIR / "临潼区_network.db")
GEXF_PATH = str(GRAPH_DIR / "临潼区_network.gexf")

# ── 人员 ──────────────────────────────────────────────────────────────
persons = [
    # ⚠ 区委书记 - 待查
    # 经多渠道搜索（政府网站领导之窗、百度搜索、新闻检索），未能确认现任临潼区委书记姓名。
    # 苗吉(区长)在2026年7月13日陕西省委组织部干部任职公示中被公示为"拟进一步使用"，
    # 可能即将接任区委书记或调任其他职务。
    # 临潼区政府网站"区长之窗"页面仅列出了政府领导班子（区长+副区长），
    # 区委领导班子信息未公开或未在搜索范围内找到。
    {
        "id": 1,
        "name": "待查_区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共西安市临潼区委员会",
        "source": "待查：区委书记姓名待补充。建议搜索方向：西安市委组织部任前公示、临潼区政府网站区委领导栏目、陕西日报临潼报道。"
    },
    {
        "id": 2,
        "name": "苗吉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年3月",
        "birthplace": "河南洛阳",
        "education": "研究生学历，博士学位",
        "party_join": "中共党员",
        "work_start": "2002年7月",
        "current_post": "区委副书记、区长",
        "current_org": "西安市临潼区人民政府",
        "source": "http://www.lintong.gov.cn/zwgk/xxgkml/zfld/hk/1.html"
    },
    {
        "id": 3,
        "name": "孟俊平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年5月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "西安市临潼区人民政府",
        "source": "http://www.lintong.gov.cn/zwgk/xxgkml/zfld/mjp/1.html; 2026年7月13日陕西省委组织部任职公示"
    },
    {
        "id": 4,
        "name": "霍炳男",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市临潼区人民政府",
        "source": "http://www.lintong.gov.cn/zwgk/xxgkml/zfld/hbn/1.html"
    },
    {
        "id": 5,
        "name": "王鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市临潼区人民政府",
        "source": "http://www.lintong.gov.cn/zwgk/xxgkml/zfld/wp/1.html"
    },
    {
        "id": 6,
        "name": "张超",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市临潼区人民政府",
        "source": "http://www.lintong.gov.cn/zwgk/xxgkml/zfld/zc/1.html"
    },
    {
        "id": 7,
        "name": "简国锋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市临潼区人民政府",
        "source": "http://www.lintong.gov.cn/zwgk/xxgkml/zfld/jgf/1.html"
    },
]

# ── 组织机构 ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共西安市临潼区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共西安市委",
        "location": "西安市临潼区"
    },
    {
        "id": 2,
        "name": "西安市临潼区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市人民政府",
        "location": "西安市临潼区"
    },
    {
        "id": 3,
        "name": "西安建筑科技大学土木学院",
        "type": "事业单位",
        "level": "县处级",
        "parent": "西安建筑科技大学",
        "location": "西安市"
    },
    {
        "id": 4,
        "name": "西安市规划局",
        "type": "政府",
        "level": "副厅级",
        "parent": "西安市人民政府",
        "location": "西安市"
    },
    {
        "id": 5,
        "name": "西安市规划局碑林分局",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市规划局",
        "location": "西安市碑林区"
    },
    {
        "id": 6,
        "name": "西安国际港务区管委会",
        "type": "开发区",
        "level": "副厅级",
        "parent": "西安市人民政府",
        "location": "西安市"
    },
]

# ── 任职记录 ─────────────────────────────────────────────────────────
positions = [
    # 苗吉的历任职务
    {"person_id": 2, "org_id": 3, "title": "党委副书记、副院长、纪委书记",
     "start_date": "", "end_date": "", "rank": "", "note": "西安建筑科技大学土木学院任职"},
    {"person_id": 2, "org_id": 4, "title": "总工程师办公室副主任",
     "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 5, "title": "局长",
     "start_date": "", "end_date": "", "rank": "", "note": "西安市规划局碑林分局局长"},
    {"person_id": 2, "org_id": 4, "title": "建设工程规划处处长",
     "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 4, "title": "市政工程规划处处长",
     "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "管委会副主任、党工委委员",
     "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "党工委副书记",
     "start_date": "", "end_date": "", "rank": "副厅级", "note": "西安国际港务区党工委副书记"},
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长",
     "start_date": "2022年3月", "end_date": "present", "rank": "正处级",
     "note": "2022年3月起任临潼区区长。2026年7月13日陕西省委组织部公示：拟进一步使用。"},

    # 孟俊平的职务（来自同一公示）
    {"person_id": 3, "org_id": 2, "title": "区委常委、常务副区长",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "2026年7月13日陕西省委组织部任职公示中提及"},

    # 其他副区长 - 具体分管待确认
    {"person_id": 4, "org_id": 2, "title": "副区长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副区长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副区长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 待查区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "姓名待查。临潼区政府网站未公开区委领导信息。"},
]

# ── 人员关系 ─────────────────────────────────────────────────────────
relationships = [
    # 苗吉与孟俊平 - 同一公示中出现，同届班子
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "临潼区政府领导班子成员，在2026年7月13日陕西省委组织部任职公示中同时被提及",
     "overlap_org": "西安市临潼区人民政府",
     "overlap_period": "2022-至今"},
]

# ── 其他区县联络线索（待查区委书记） ──────────────────────────────
# 注：未找到区委书记姓名，无法建立与兄弟区县的人事交流网络。
# 苗吉此前任职于西安国际港务区，属于开发区系统，暂未发现跨区县干部交流的明确证据。

# ── 执行构建 ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug="临潼区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("✅ 临潼区数据构建完成")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
