#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 河北省张家口市下花园区 leadership network.

Province : 河北省
Parent   : 张家口市
Level    : 市辖区（正处级）→ 区委书记/区长为正处级
Task     : hebei_下花园区
Date     : 2026-08-05
Region   : 下花园区（辖4乡：花园乡、辛庄子乡、定方水乡、段家堡乡；2街道：城镇街道、煤矿街道；
           13社区 46村；总面积315km²；约7万人口；政府门户 www.zjkxhy.gov.cn）

当前领导班子（下花园区人民政府官网 政府领导页 + 跨来源公开报道；每项置信度见注释）：

- 区委书记  ：顾蕾（男；2021-05-23 张家口市下花园区领导干部会议 由 市委组织部 宣布接任，
               前任王小军卸任另有任用；顾蕾此前曾任 河北地矿地质六队 党委书记；
               截至2026-08 未发现其继任者，仍为现任 区委书记——公开渠道未见其出生年/学历等个人履历）
- 区委副书记、区长：王江平（男，汉族，1981年12月，2004-09 参加工作，中共党员，研究生学历，
               东北大学公共管理专业硕士，下花园区委副书记、区政府区长，河北张家口下花园经开区
               党工委副书记、管委会主任(兼)；官网政府领导页 2026-07-29）
- 常务副区长：高文阳（男，蒙古族，1983-08，2006-07 参加工作，中共党员，区委常委，河北农业大学农业推广硕士）
- 副区长    ：杨海龙（男，汉族，1980-03）、冯云楠（女，1981-02）、梅雪峰、李强、顾飞
- 区委常委、组织部长：刘云峰（2023 新闻报道引述）
- 区检察院检察长：史富贤（女）（2026-07-31 张家口市第十五届人大常委会第四十九次会议 批准任命）

前任链（河北新闻网 任前公示/领导干部会议 + 张家口新闻）：
- 区委书记：王小军（至2021-05；卸任后 另有任用，后任 张家口市人大常委会副主任）
- 区长链：胡荣（2019-2020）→ 路国云（至2021-05；卸任 另有任用）→ 韩俊峰（2021-05 任区委副书记，后任区长，2022 河北日报 访谈）→ 王江平（今）

Open questions / gaps（详见 report/ 与 person JSON open_questions；不虚构）：
1. 顾蕾 出生年/籍贯/学历/入党年 与 任下花园区委书记前的完整履历（已知系 河北地质六队 党委书记）
2. 王江平 任区长前的完整任职序列（公开渠道仅述 研究生/东北大学硕士，缺历年岗位序列）
3. 现任副区长 梅雪峰 / 李强 / 顾飞 个人信息与履历
4. 现任区委常委会完整名单（专职副书记/纪委书记/宣传 / 政法）与人大/政协主席
5. 韩俊峰 卸任区长后的去向；路国云（前任区长）2021 后的去向
6. 现任 区人大常委会主任 / 区政协主席（2021 换届后）
"""

import sqlite3  # noqa: F401  (token that process_tmp.py requires to recognize a build script)
import sys
from pathlib import Path


def _find_repo_root(start):
    import os
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, "gov_relation")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return start
        cur = parent


_REPO_ROOT = _find_repo_root(Path(__file__).resolve().parent)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build  # noqa: E402

SLUG = "下花园区"
AS_OF = "2026-08-05"

DB_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.gexf"

# ── Persons ─────────────────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "顾蕾",
        "gender": "男",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "下花园区委书记",
        "current_org": "中共张家口市下花园区委员会",
        "source": "河北新闻网《张家口下花园区召开领导干部会议 顾蕾任区委书记》（2021-05-23 任前公示）；此前任 河北地矿地质六队 党委书记（2020 报道）",
    },
    {
        "id": 2,
        "name": "王江平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年12月",
        "birthplace": "待查",
        "education": "研究生学历（东北大学公共管理专业硕士）",
        "party_join": "中共党员",
        "work_start": "2004年9月",
        "current_post": "下花园区委副书记、区长，河北张家口下花园经开区党工委副书记、管委会主任（兼）",
        "current_org": "下花园区人民政府",
        "source": "下花园区人民政府官网·政府领导页（官方，2026-07-29）",
    },
    {
        "id": 3,
        "name": "高文阳",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1983年8月",
        "birthplace": "待查",
        "education": "研究生学历（河北农业大学农业推广硕士）",
        "party_join": "中共党员",
        "work_start": "2006年7月",
        "current_post": "下花园区委常委、常务副区长",
        "current_org": "下花园区人民政府",
        "source": "下花园区人民政府官网·政府领导页（官方）",
    },
    {
        "id": 4,
        "name": "杨海龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年3月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2005年8月",
        "current_post": "副区长",
        "current_org": "下花园区人民政府",
        "source": "下花园区人民政府官网·政府领导页（官方）",
    },
    {
        "id": 5,
        "name": "冯云楠",
        "gender": "女",
        "ethnicity": "汉族（推测）",
        "birth": "1981年2月",
        "birthplace": "待查",
        "education": "燕山大学文法学院公共管理硕士",
        "party_join": "中共党员（2003年6月）",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "下花园区人民政府",
        "source": "下花园区人民政府官网·政府领导页（官方）",
    },
    {
        "id": 6,
        "name": "梅雪峰",
        "gender": "男（推测）",
        "ethnicity": "未知",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员（推测）",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "下花园区人民政府",
        "source": "下花园区人民政府官网·政府领导页（官方名单）",
    },
    {
        "id": 7,
        "name": "李强",
        "gender": "男（推测）",
        "ethnicity": "未知",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员（推测）",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "下花园区人民政府",
        "source": "下花园区人民政府官网·政府领导页（官方名单）",
    },
    {
        "id": 8,
        "name": "顾飞",
        "gender": "男（推测）",
        "ethnicity": "未知",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员（推测）",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "下花园区人民政府",
        "source": "下花园区人民政府官网·政府领导页（官方名单）",
    },
    {
        "id": 9,
        "name": "刘云峰",
        "gender": "男（推测）",
        "ethnicity": "未知",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "下花园区委常委、组织部部长",
        "current_org": "中共张家口市下花园区委组织部",
        "source": "河北新闻网 公开报道（2023 以其 区委常委、组织部长 身份引述）",
    },
    {
        "id": 10,
        "name": "史富贤",
        "gender": "女",
        "ethnicity": "未知",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张家口市下花园区人民检察院检察长",
        "current_org": "下花园区人民检察院",
        "source": "张家口新闻网·市人大 任免名单（2026-08-02，2026-07-31 人大四十九次会议 批准任命）",
    },
    {
        "id": 11,
        "name": "王小军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任下花园区委书记（至2021-05）；现任 张家口市人大常委会副主任",
        "current_org": "张家口市人大常委会",
        "source": "河北新闻网《领导干部会议 顾蕾任区委书记》(2021-05-23) + 张家口新闻网 市人大 主席团名单（2023-01）",
    },
    {
        "id": 12,
        "name": "路国云",
        "gender": "男",
        "ethnicity": "未知",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任下花园区委副书记、区长（至2021-05；去向待查）",
        "current_org": "",
        "source": "河北新闻网 2021-05-23 领导干部会议（路国云不再担任区委副书记、常委、委员兼区长，另有任用）",
    },
    {
        "id": 13,
        "name": "韩俊峰",
        "gender": "男",
        "ethnicity": "未知",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任下花园区长（2021-05 任区委副书记；约2022 任区长；去向待查）",
        "current_org": "",
        "source": "河北新闻网 领导干部会议 2021-05-23 + 河北日报《解放思想……访下花园区区长韩俊峰》(2022)",
    },
    {
        "id": 14,
        "name": "胡荣",
        "gender": "男",
        "ethnicity": "未知",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任下花园区长（2019-2020）",
        "current_org": "",
        "source": "河北新闻网 2020 报道（下花园区区长胡荣）",
    },
]

# ── Organizations ────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共张家口市下花园区委员会", "type": "党委",
     "level": "区（正处级）", "parent": "中共张家口市委", "location": "张家口市下花园区"},
    {"id": 2, "name": "下花园区人民政府", "type": "政府",
     "level": "区（正处级）", "parent": "张家口市人民政府", "location": "张家口市下花园区"},
    {"id": 3, "name": "河北张家口下花园经济开发区", "type": "开发区",
     "level": "省级经开区", "parent": "张家口市人民政府", "location": "张家口市下花园区"},
    {"id": 4, "name": "中共张家口市委组织部", "type": "党委",
     "level": "市级", "parent": "中共张家口市委", "location": "张家口市"},
    {"id": 5, "name": "河北地矿地质六队", "type": "事业单位",
     "level": "地质类单位", "parent": "河北省地矿系统", "location": "河北省"},
    {"id": 6, "name": "下花园区人民检察院", "type": "检察院",
     "level": "区级", "parent": "张家口市人民检察院", "location": "张家口市下花园区"},
    {"id": 7, "name": "张家口市人大常委会", "type": "人大",
     "level": "市级", "parent": "河北省人大", "location": "张家口市"},
    {"id": 8, "name": "中共张家口市下花园区委组织部", "type": "党委",
     "level": "区级部门", "parent": "中共张家口市下花园区委", "location": "张家口市下花园区"},
]

# ── Positions ────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "下花园区委书记",
     "start_date": "2021-05", "end_date": "present", "rank": "区（正处级）",
     "note": "2021-05-23 领导干部会议宣布任下花园区委委员、常委、书记；接任王小军；未发现后续继任者，仍为现任"},
    {"person_id": 1, "org_id": 5, "title": "河北地矿地质六队党委书记",
     "start_date": "", "end_date": "2021", "rank": "地质类单位",
     "note": "任下花园区委书记前曾任河北地矿地质六队党委书记（2020 报道）；具体年月待查"},

    {"person_id": 2, "org_id": 2, "title": "下花园区委副书记、区长",
     "start_date": "约2025", "end_date": "present", "rank": "区（正处级）",
     "note": "官网 2026-07-29 审核简历；任区长/区委副书记；接续韩俊峰；具体到任年份待查"},
    {"person_id": 2, "org_id": 3, "title": "下花园经开区党工委副书记、管委会主任（兼）",
     "start_date": "约2025", "end_date": "present", "rank": "经开区（兼）",
     "note": "下花园经开区主要负责人（官网政府领导页 兼）"},

    {"person_id": 3, "org_id": 2, "title": "下花园区委常委、常务副区长",
     "start_date": "", "end_date": "present", "rank": "区（副处级）", "note": "官网政府领导页"},
    {"person_id": 4, "org_id": 2, "title": "下花园区副区长",
     "start_date": "", "end_date": "present", "rank": "区（副处级）", "note": "官网政府领导页"},
    {"person_id": 5, "org_id": 2, "title": "下花园区副区长",
     "start_date": "", "end_date": "present", "rank": "区（副处级）", "note": "官网政府领导页"},
    {"person_id": 6, "org_id": 2, "title": "下花园区副区长",
     "start_date": "", "end_date": "present", "rank": "区（副处级）", "note": "官网政府领导页名单"},
    {"person_id": 7, "org_id": 2, "title": "下花园区副区长",
     "start_date": "", "end_date": "present", "rank": "区（副处级）", "note": "官网政府领导页名单"},
    {"person_id": 8, "org_id": 2, "title": "下花园区副区长",
     "start_date": "", "end_date": "present", "rank": "区（副处级）", "note": "官网政府领导页名单"},
    {"person_id": 9, "org_id": 8, "title": "下花园区委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "区（副处级）", "note": "河北新闻网 2023 引述"},
    {"person_id": 10, "org_id": 6, "title": "下花园区人民检察院检察长",
     "start_date": "2026-07", "end_date": "present", "rank": "区（副处级）",
     "note": "2026-07-31 张家口市人大四十九次会议 批准任命"},

    {"person_id": 11, "org_id": 1, "title": "前任下花园区委书记",
     "start_date": "2017-?", "end_date": "2021-05", "rank": "区（正处级）", "note": "至2021-05 卸任，另有任用"},
    {"person_id": 11, "org_id": 7, "title": "张家口市人大常委会副主任",
     "start_date": "约2021/2022", "end_date": "present", "rank": "市（副厅级）",
     "note": "卸任区委书记后转市人大常委会（2023-01 市人大主席团名单列名）"},

    {"person_id": 12, "org_id": 2, "title": "前任下花园区委副书记、区长",
     "start_date": "", "end_date": "2021-05", "rank": "区（正处级）",
     "note": "2021-05-23 不再担任区委副书记/常委/区长，另有任用"},
    {"person_id": 13, "org_id": 2, "title": "前任下花园区长",
     "start_date": "约2022", "end_date": "约2024", "rank": "区（正处级）",
     "note": "2021-05 任区委副书记，约2022 任区长（河北日报访谈）；后卸任，去向待查"},
    {"person_id": 14, "org_id": 2, "title": "前任下花园区长",
     "start_date": "2019", "end_date": "2020", "rank": "区（正处级）",
     "note": "2019-2020 任下花园区长（新闻）"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "搭档",
     "context": "现任区委书记 顾蕾 与 区长 王江平（区委副书记）为下花园区委、区政府正职搭档",
     "overlap_org": "下花园区委、区政府", "overlap_period": "约2021-2026"},
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor",
     "context": "顾蕾2021-05 接续 王小军 任下花园区委书记（王小军卸任另有任用）",
     "overlap_org": "中共下花园区委", "overlap_period": "2021-05"},
    {"person_a": 11, "person_b": 7, "type": "promotion_chain",
     "context": "王小军 卸任区委书记后转任 张家口市人大常委会副主任", "overlap_org": "", "overlap_period": "2021-"},
    {"person_a": 2, "person_b": 13, "type": "predecessor_successor",
     "context": "王江平 接续 韩俊峰 任下花园区长（约2024-2025）",
     "overlap_org": "下花园区人民政府", "overlap_period": "约2024-2025"},
    {"person_a": 13, "person_b": 1, "type": "同事",
     "context": "韩俊峰 2021-05 任区委副书记 时，顾蕾 任区委书记，二人区委班子共事",
     "overlap_org": "下花园区委", "overlap_period": "2021-"},
    {"person_a": 13, "person_b": 12, "type": "predecessor_successor",
     "context": "韩俊峰（区委副书记）接续 路国云（区长）任区长链（同年班子）",
     "overlap_org": "下花园区委、区政府", "overlap_period": "2021"},
    {"person_a": 3, "person_b": 2, "type": "colleague_overlap",
     "context": "高文阳（常务副区长）与 王江平（区长）为区政府班子搭档",
     "overlap_org": "下花园区人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 4, "type": "colleague_overlap",
     "context": "杨海龙（副区长）与 王江平（区长）同班子", "overlap_org": "下花园区人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 5, "type": "colleague_overlap",
     "context": "冯云楠（副区长）与 王江平（区长）同班子", "overlap_org": "下花园区人民政府", "overlap_period": "现任"},
]


def main():
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("=== 下花园区 network build complete ===")
    print(f"  DB  : {DB_PATH}  (persons={len(persons)}, orgs={len(organizations)}, "
          f"positions={len(positions)}, rels={len(relationships)})")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()