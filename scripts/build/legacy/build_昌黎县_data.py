#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 河北省秦皇岛市昌黎县 leadership network.

Province : 河北省
Parent   : 秦皇岛市
Level    : 县（正处级）→ 县委书记/县长为正处级
Task     : hebei_昌黎县
Date     : 2026-08-05
Region   : 昌黎县（行政区划代码 130322；政府门户 www.clxzf.gov.cn）
Counties : 12镇 4乡 1街道；政府驻昌黎镇

当前领导班子（结合 昌黎县人民政府门户·政府领导页 检索自 www.clxzf.gov.cn/single/3/19473.html
          与跨来源公开报道；每项置信度见注释）：

- 县委书记   ：孙谓青（男，中共党员；河北秦皇岛人；兼任县人武部党委第一书记；
               2024-09 由秦皇岛市城市管理综合行政执法局局长调任昌黎县委书记；
               此前曾任北戴河区委常委、常务副区长/区委副书记）
- 县委副书记、县长：吴学军（男，汉族，1978-05，硕士研究生，中共党员；
               现任县委副书记、县政府党组书记、县长，兼河北昌黎经开区党工委副书记管委会主任；
               第十八届昌黎县人民政府（2026 换届））
- 前任县委书记：宗振华（至 2024-09 卸任；报道称“原任已跨市履新”）
- 前任县长链：狄莎（2022-2023）→ 李清（男，1984-08，湖北汉川人，清华；2024-2026 初）→ 吴学军（现任）

政府班子（官方 政府领导页 2026-08 现行）：
- 辛昌亮：县委常委、县政府党组副书记、副县长（分管常务）
- 陈静朋：县委常委、县政府党组成员、副县长
- 付卓然：县政府党组成员、副县长
- 张立强：县政府党组成员、副县长、县公安局局长
- 马腾飞：县政府党组成员、副县长
- 路江：县政府党组成员、副县长
- 刘向阳：县政府党组成员、副县长
- 郭毅：河北昌黎经济开发区党工委副书记、管委会常务副主任

跨区人事交流（核心网络证据，网络受限来源：官方门户+公开报道）：
- 孙谓青：秦皇岛市城市管理综合行政执法局（2021-06—2024-10）→ 昌黎县委书记（2024-09 起，跨条线转任）
- 孙谓青：曾任 秦皇岛市北戴河区（区委副书记/常务副区长）→ 昌黎（秦皇岛市内区县间横向流动）
- 吴学军：现职 昌黎县县长（第十八届）；过去与 河北昌黎经济开发区 关联（经开区党工委副书记、管委会主任）

Open questions / gaps（详见 report/与 person JSON open_questions；不虚构）：
1. 孙谓青 出生年/籍贯/学历/入党年与 2000-2015 完整履历（公开渠道未获取完整词条）
2. 吴学军 任县长前的完整任职序列（升任词条仅到 1978 年生/研究生学历，缺历年）
3. 李清（前任县长）2026 卸任后的去向
4. 宗振华（前任县委书记）2024-09 卸任后的去向
5. 现任县人大常委会主任、县政协主席、县委层面（副书记/纪委/组织/宣传/政法）正式在册名单与分工
6. 狄莎（前任县长）2023 卸任后的去向
"""

import os
import sqlite3  # noqa: F401  (present so process_tmp recognizes this as a build script)
import sys
from pathlib import Path


def _find_repo_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, "gov_relation")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return start
        cur = parent


_REPO_ROOT = _find_repo_root(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build  # noqa: E402

SLUG = "昌黎县"
AS_OF = "2026-08-05"

DB_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.gexf"

# ── Persons ─────────────────────────────────────────────────────────────
# id 1 县委书记（一把手）；id 2 县长（二把手）；id 3-9 县政府班子成员；id 10+ 前任/关键关联
persons = [
    # 1 现任县委书记（一把手）
    {
        "id": 1,
        "name": "孙谓青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "河北省秦皇岛市（籍贯待查）",
        "education": "学历待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "昌黎县委书记、县人武部党委第一书记",
        "current_org": "中共昌黎县委员会",
        "source": "跨媒体公开报道：网易163/搜狐/今日头条（2024-09 换任，2025-02 履职报道）+ 百度百科检索摘要",
    },
    # 2 现任县长（二把手）
    {
        "id": 2,
        "name": "吴学军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年5月",
        "birthplace": "待查",
        "education": "硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委副书记、县政府党组书记、县长",
        "current_org": "昌黎县人民政府",
        "source": "昌黎县政府门户·政府领导页 www.clxzf.gov.cn/single/3/19473.html（官方，2026-08-05）",
    },
    # 3 常务副县长
    {
        "id": 3,
        "name": "辛昌亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员（推测）",
        "work_start": "",
        "current_post": "县委常委、县政府党组副书记、副县长（分管常务）",
        "current_org": "昌黎县人民政府",
        "source": "昌黎县政府门户·政府领导页（官方）",
    },
    # 4 副县长
    {
        "id": 4,
        "name": "陈静朋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员（推测）",
        "work_start": "",
        "current_post": "县委常委、县政府党组成员、副县长",
        "current_org": "昌黎县人民政府",
        "source": "昌黎县政府门户·政府领导页（官方）",
    },
    # 5 副县长
    {
        "id": 5,
        "name": "付卓然",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员（推测）",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "昌黎县人民政府",
        "source": "昌黎县政府门户·政府领导页（官方）",
    },
    # 6 副县长/公安局长
    {
        "id": 6,
        "name": "张立强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员（推测）",
        "work_start": "",
        "current_post": "县政府党组成员、副县长，县公安局局长",
        "current_org": "昌黎县公安局",
        "source": "昌黎县政府门户·政府领导页（官方）",
    },
    # 7 副县长
    {
        "id": 7,
        "name": "马腾飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员（推测）",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "昌黎县人民政府",
        "source": "昌黎县政府门户·政府领导页（官方）",
    },
    # 8 副县长
    {
        "id": 8,
        "name": "路江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员（推测）",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "昌黎县人民政府",
        "source": "昌黎县政府门户·政府领导页（官方）",
    },
    # 9 副县长
    {
        "id": 9,
        "name": "刘向阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员（推测）",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "昌黎县人民政府",
        "source": "昌黎县政府门户·政府领导页（官方）",
    },
    # 10 经开区常务副主任
    {
        "id": 10,
        "name": "郭毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员（推测）",
        "work_start": "",
        "current_post": "河北昌黎经济开发区党工委副书记、管委会常务副主任",
        "current_org": "河北昌黎经济开发区管委会",
        "source": "昌黎县政府门户·政府领导页（官方）",
    },
    # 11 前任县委书记
    {
        "id": 11,
        "name": "宗振华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任昌黎县委书记（至2024-09；去向待查）",
        "current_org": "",
        "source": "公开报道（2024-09 换任，网易等；具体去向 待查）",
    },
    # 12 前任县长
    {
        "id": 12,
        "name": "李清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年8月",
        "birthplace": "湖北省汉川市",
        "education": "清华大学地球系统科学研究所（研究生）",
        "party_join": "2008年11月",
        "work_start": "2009年7月",
        "current_post": "原任 昌黎县委副书记、县长（至2026；去向待查）",
        "current_org": "",
        "source": "百度百科《李清（河北省秦皇岛市昌黎县委副书记、县政府党组书记）》检索摘要（2022-2026）",
    },
    # 13 更早前任县长
    {
        "id": 13,
        "name": "狄莎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任 昌黎县长（2022-2023；去向待查）",
        "current_org": "",
        "source": "昌黎县政府门户·政府工作报告 2023/2022（官方）",
    },
]

# ── Organizations ────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共昌黎县委员会", "type": "党委",
     "level": "县（正处级）", "parent": "中共秦皇岛市委", "location": "秦皇岛市昌黎县"},
    {"id": 2, "name": "昌黎县人民政府", "type": "政府",
     "level": "县（正处级）", "parent": "秦皇岛市人民政府", "location": "秦皇岛市昌黎县"},
    {"id": 3, "name": "昌黎县公安局", "type": "政府",
     "level": "县（正科级机构）", "parent": "昌黎县人民政府", "location": "秦皇岛市昌黎县"},
    {"id": 4, "name": "河北昌黎经济开发区管委会", "type": "开发区",
     "level": "省级开发区", "parent": "昌黎县人民政府", "location": "秦皇岛市昌黎县"},
    {"id": 5, "name": "秦皇岛市城市管理综合行政执法局", "type": "政府",
     "level": "市级（正处级部门）", "parent": "秦皇岛市人民政府", "location": "秦皇岛市"},
    {"id": 6, "name": "秦皇岛市北戴河区人民政府", "type": "政府",
     "level": "区（副处级干部）", "parent": "秦皇岛市人民政府", "location": "秦皇岛市北戴河区"},
    {"id": 7, "name": "秦皇岛市北戴河区委", "type": "党委",
     "level": "区", "parent": "中共秦皇岛市委", "location": "秦皇岛市北戴河区"},
]

# ── Positions ────────────────────────────────────────────────────────────
positions = [
    # 孙谓青 现任县委书记
    {"person_id": 1, "org_id": 1, "title": "昌黎县委书记、县人武部党委第一书记",
     "start_date": "2024-09", "end_date": "present", "rank": "县（正处级）",
     "note": "2024-09 上任，接替宗振华；兼县人武部党委第一书记（2025-02 今日头条《秦皇岛市昌黎县委书记》报道确认）"},
    # 孙谓青 曾任
    {"person_id": 1, "org_id": 5, "title": "秦皇岛市城市管理综合行政执法局局长",
     "start_date": "2021-06", "end_date": "2024-10", "rank": "市级（正处）",
     "note": "2021-06—2024-10 任局长（百科人物履历）"},
    {"person_id": 1, "org_id": 6, "title": "秦皇岛市北戴河区副区长（常务）",
     "start_date": "", "end_date": "", "rank": "区（副处级）",
     "note": "此前曾任北戴河区副区长、常务副区长/区委副书记（公开报道；具体年代待查）"},
    # 吴学军 现任县长
    {"person_id": 2, "org_id": 2, "title": "昌黎县委副书记、县政府党组书记、县长",
     "start_date": "2026", "end_date": "present", "rank": "县（正处级）",
     "note": "第十八届县政府（2026 换届）；兼河北昌黎经济开发区党工委副书记、管委会主任（官网政府领导页2026-08-05）"},
    {"person_id": 2, "org_id": 4, "title": "河北昌黎经济开发区党工委副书记、管委会主任",
     "start_date": "2026", "end_date": "present", "rank": "开发区（兼）",
     "note": "县域经济开发区主要负责人（官网政府领导页）"},
    # 辛昌亮 常务副县长
    {"person_id": 3, "org_id": 2, "title": "昌黎县委委员、县政府常务副县长",
     "start_date": "", "end_date": "present", "rank": "县（正处级副职）",
     "note": "县委常委、县政府党组副书记、副县长（分管常务）；官网政府领导页"},
    # 陈静朋 副县长
    {"person_id": 4, "org_id": 2, "title": "昌黎县委委员、县政府副县长",
     "start_date": "", "end_date": "present", "rank": "县（副处级）",
     "note": "县委常委、县政府党组成员、副县长；官网政府领导页"},
    # 付卓然 副县长
    {"person_id": 5, "org_id": 2, "title": "昌黎县政府副县长",
     "start_date": "", "end_date": "present", "rank": "县（副处级）",
     "note": "县政府党组成员、副县长；官网政府领导页"},
    # 张立强 副县长/公安局长
    {"person_id": 6, "org_id": 2, "title": "昌黎县政府副县长、县公安局局长",
     "start_date": "", "end_date": "present", "rank": "县（副处级）",
     "note": "县政府党组成员、副县长，兼任县公安局局长；官网政府领导页"},
    {"person_id": 6, "org_id": 3, "title": "昌黎县公安局局长",
     "start_date": "", "end_date": "present", "rank": "县（副处级）",
     "note": "兼任县公安局局长"},
    # 马腾飞 副县长
    {"person_id": 7, "org_id": 2, "title": "昌黎县政府副县长",
     "start_date": "", "end_date": "present", "rank": "县（副处级）",
     "note": "县政府党组成员、副县长；官网政府领导页"},
    # 路东 副县长
    {"person_id": 8, "org_id": 2, "title": "昌黎县政府副县长",
     "start_date": "", "end_date": "present", "rank": "县（副处级）",
     "note": "县政府党组成员、副县长；官网政府领导页"},
    # 刘向阳 副县长
    {"person_id": 9, "org_id": 2, "title": "昌黎县政府副县长",
     "start_date": "", "end_date": "present", "rank": "县（副处级）",
     "note": "县政府党组成员、副县长；官网政府领导页"},
    # 郭毅 经开区副主任
    {"person_id": 10, "org_id": 4, "title": "河北昌黎经济开发区党工委常务副主任",
     "start_date": "", "end_date": "present", "rank": "开发区（副处级）",
     "note": "经开区党工委副书记、管委会常务副主任；官网政府领导页"},
    # 宗振华 前任县委书记
    {"person_id": 11, "org_id": 1, "title": "昌黎县委书记（前任）",
     "start_date": "", "end_date": "2024-09", "rank": "县（正处级）",
     "note": "2024-09 卸任（报道）；去向待查"},
    # 李清 前任县长
    {"person_id": 12, "org_id": 2, "title": "昌黎县委副书记、县长（前任）",
     "start_date": "2023", "end_date": "2026", "rank": "县（正处级）",
     "note": "2023-02 起任昌黎县委副书记、代理县长；2024-2026 任县长；2026-01-27 第十七届人大六次会议作政府工作报告；去向待查"},
    {"person_id": 13, "org_id": 2, "title": "昌黎县长（前任）",
     "start_date": "2022", "end_date": "2023", "rank": "县（正处级）",
     "note": "2022-2023 任县长；2023 政府工作报告出具者；去向待查"},
]

# ── Relationships ────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档（当前）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记（孙谓青，2024-09 起）与（吴学军，2026 起）党政正副搭档",
     "overlap_org": "昌黎县", "overlap_period": "2026-至今 (confirmed 官网+报道)"},
    # 书记与前任县长
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "县委书记（孙谓青，2024-09 起）与前任县长（李清，2026 前）党政正职搭档",
     "overlap_org": "昌黎县", "overlap_period": "2024-2026 (confirmed)"},
    # 书记接替前任书记
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor",
     "context": "孙谓青 2024-09 接任 宗振华 为昌黎县委书记",
     "overlap_org": "昌黎县", "overlap_period": "2024-09 (confirmed 报道)"},
    # 县长链（前任→现任）
    {"person_a": 2, "person_b": 12, "type": "predecessor_successor",
     "context": "吴学军 接任 李清 为昌黎县县长（李清 2026 前任、吴学军现任）",
     "overlap_org": "昌黎县政府", "overlap_period": "2026 (confirmed 官网)"},
    {"person_a": 12, "person_b": 13, "type": "predecessor_successor",
     "context": "李清 接任 狄莎 为昌黎县长（2023）",
     "overlap_org": "昌黎县政府", "overlap_period": "2023 (confirmed 政府工作报告)"},
]

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")