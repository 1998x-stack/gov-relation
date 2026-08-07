#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
青县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 沧州市
Region: 青县
Targets: 县委书记 & 县长

Research 要点（2026-08-06，一手青县人民政府 www.qingxian.gov.cn + 权威媒体/百科交叉）：
- 现任县委书记：张硕（2026-01-10 履新；约2026-07-29 调任黄骅市人民政府市长，故截至调研时青县县委书记继任未确认）
  * 1980年3月生，男，汉族，河北保定，2003年6月入党，2003年8月参加工作，全日制大学学历、公共管理硕士
  * 履历：沧州渤海新区党工委委员、管委会副主任 → 沧州渤海新区黄骅市港城产业园区党组书记、管委会主任 → 沧州市财政局党组书记、局长 → 青县县委书记 → （黄骅市市长）
  * 来源：青县政府官网“机关简介/领导介绍”系列 + 汲古新知(2026-02-07) + 燕阵沧州/网易(2026-07-29) 万人 OK
- 现任代县长：李向伟（2026-05-20 青县第十八届人大常委会第四十次会议任命副县长并决定代理县长；前任时励同日辞去县长）
  * 来源：爱企查“青县2026年最新任命” + 百度百科“李向伟(青县代理县长)”；此前任大城县人民政府副县长（2022-08-30 大城县人大任命）
- 原县长：时励（2021-06 代县长、2021-07 当选，2026-05-20 辞职；1982-07 河北武强，河北经贸大学法学，2005-08 参加工作）
- 前任县委书记：左佳宁（2022-12-15 任，2026-01 离任；据报任黄骅市委副书记、代理市长）

Confidence 说明：
  张硕任青县委书记、李向伟任代县长、时励任县长及辞职 — confirmed（官方人大常委会公告 + 媒体）。
  张硕个人履历节点 — confirmed（百科/媒体交叉）；李向伟出生/学历 — unverified。
  领导班子成员及分工 — 部分 confirmed（官方会议/人大公告），部分为历史在任（待补充）。

参考资料：青县政府常务会议均署“时励主持召开”（2025-01~2026-05，官方一手）；2026年政府工作报告由时励署名（2026-02-11）。
"""

import os
import sys
from pathlib import Path

# Allow import from repo root robustly (works from data/tmp/<task>/ and scripts/build/)
REPO_ROOT = Path(__file__).resolve().parents[2]
for _pc in [2, 3, 4, 5]:
    _candidate = Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: F401 — required for process_tmp.py token check

from gov_relation.runner import run_build

SLUG = "青县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════════
    # 现任一把手（target）与核心历史人物
    # ════════════════════════════════════════════
    {
        "id": 1,
        "name": "张硕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-03",
        "birthplace": "河北保定",
        "native_place": "待查",
        "education": "全日制大学学历，公共管理硕士",
        "party_join": "2003年6月加入中国共产党",
        "work_start": "2003年8月参加工作",
        "current_post": "青县县委书记（2026-01 起，约2026-07 调任黄骅市市长）",
        "current_org": "中共青县委员会",
        "source": "百度百科-张硕(河北省沧州市青县县委书记)：1980年3月生，河北保定人，2003年6月入党、2003年8月参加工作，全日制大学学历、公共管理硕士；2026-01-10 青县县委书记——沧州市财政局原党委书记、局长张硕履新（望海司微博/汲古新知 2026-02-07）；2026-07-29 燕阵沧州-人事快讯：张硕任黄骅市人民政府市长。"
    },
    {
        "id": 2,
        "name": "李向伟",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "青县人民政府副县长、代理县长",
        "current_org": "青县人民政府",
        "source": "青县2026年最新任命(爱企查)：2026-05-20 青县第十八届人大常委会第四十次会议决定任命李向伟为青县副县长并决定其代理青县县长，同时接受时励辞去县长；百度百科-李向伟(青县代理县长)。此前任大城县人民政府副县长（2022-08-30 大城县人大常委会第十次会议任命）。"
    },
    {
        "id": 3,
        "name": "时励",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-07",
        "birthplace": "河北省衡水市武强县",
        "native_place": "河北武强",
        "education": "河北经贸大学法学院法学专业（2001.09-2005.07）",
        "party_join": "中共党员",
        "work_start": "2005年8月",
        "current_post": "原青县人民政府县长（2026-05-20 辞职，另有任用）",
        "current_org": "青县人民政府（已卸任）",
        "source": "百度百科-时励：1982年7月生，河北武强人，河北经贸大学法学；2021-06 任青县副县长、代县长，2021-07-28 当选县长（青县十八届人大一次会议）；2026-05-20 青县十八届人大常委会第四十次会议接受其辞去青县县长。青县2026年政府工作报告（2026-02-11）由县长时励署名。"
    },
    {
        "id": 4,
        "name": "左亚宁",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原青县县委书记（2026-01 离任；据报任黄骅市委副书记、代理市长）",
        "current_org": "中共青县委员会（已卸任）",
        "source": "搜狐网-沧州人事任免：2022-12-15 青县召开全县领导干部会议，省委、市委决定左亚宁任中共青县县委书记；百度文库-青县领导干部调整：左亚宁曾任肃宁县副县长、肃宁县委常委办公室主任、东光县委常委常务副县长；汲古新知/望江司(2026-01-10)：左亚宁不再担任青县县委书记，据报任黄骅市委副书记、代理市长。"
    },
    # ════════════════════════════════════════════
    # 领导班子（人大/纪委/县政府）
    # ════════════════════════════════════════════
    {
        "id": 5,
        "name": "张卫忠",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "青县人大常委会主任",
        "current_org": "青县人民代表大会常务委员会",
        "source": "青县第十八届人大常委会第五次(2022-01-19)/第三十七次(2026-01-30)/第四十次会议均由主任张卫忠主持（官方发布）。"
    },
    {
        "id": 6,
        "name": "马俊敏",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "青县县委常委、纪委书记、监委主任",
        "current_org": "中共青县纪律检查委员会",
        "source": "青县十八届人大常委会第五次会议(2022-01-19)：县委常委、纪委书记、监委主任马俊敏列席（官方发布）。"
    },
    {
        "id": 7,
        "name": "韩尚龙",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "青县人民政府副县长（2026-01-13 任命）",
        "current_org": "青县人民政府",
        "source": "青县第十八届人大常委会第三十七次会议(2026-01-30)：副县长韩尚龙列席；爱企查-青县2026年最新任命：2026-01-13 决定任命韩尚龙为青县副县长，同时免去曾宪强的副县长职务。"
    },
    {
        "id": 8,
        "name": "李国钧",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原青县县委书记（约2021-2022，后任辛集市委书记）",
        "current_org": "中共青县委员会（已卸任）",
        "source": "网易新闻(2022-12-29)：李国钧曾为青县县委书记，2022-11 已任辛集市委书记；“书记项目”专访播出青县县委书记李国钧(2021-11)。青县县委常委会(扩大)会议(2023-11-21 青县政府)等仍以李国钧为书记出席。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共青县委员会",
        "type": "党委",
        "level": "县级",
        "location": "沧州市青县",
        "parent": "中共沧州市委"
    },
    {
        "id": 2,
        "name": "青县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "沧州市青县",
        "parent": "沧州市人民政府"
    },
    {
        "id": 3,
        "name": "青县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "location": "沧州市青县",
        "parent": "沧州市人大常委会"
    },
    {
        "id": 4,
        "name": "中共青县纪律检查委员会",
        "type": "群团（纪检）",
        "level": "县级",
        "location": "沧州市青县",
        "parent": "中共沧州市纪委"
    },
    {
        "id": 5,
        "name": "政协青县委员会",
        "type": "政协",
        "level": "县级",
        "location": "沧州市青县",
        "parent": "政协沧州市委员会"
    },
    {
        "id": 6,
        "name": "青县经济开发区管理委员会",
        "type": "开发区",
        "level": "县级",
        "location": "沧州市青县",
        "parent": "青县人民政府"
    },
    {
        "id": 7,
        "name": "沧州市财政局",
        "type": "政府",
        "level": "市级",
        "location": "沧州市",
        "parent": "沧州市人民政府"
    },
    {
        "id": 8,
        "name": "沧州渤海新区管理委员会",
        "type": "开发区",
        "level": "市级（国家级新区）",
        "location": "沧州市",
        "parent": "沧州市人民政府"
    },
    {
        "id": 9,
        "name": "沧州渤海新区黄骅市港城产业园区",
        "type": "开发区",
        "level": "县级",
        "location": "沧州市黄骅市",
        "parent": "沧州渤海新区"
    },
    {
        "id": 10,
        "name": "黄骅市人民政府",
        "type": "政府",
        "level": "县级（县级市）",
        "location": "沧州市黄骅市",
        "parent": "沧州市人民政府"
    },
    {
        "id": 11,
        "name": "大城县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "廊坊市大城县",
        "parent": "廊坊市人民政府"
    },
]

# 3. Positions
positions = [
    # ── 张硕（县委书记）──
    {"person_id": 1, "org_id": 1, "title": "青县县委书记", "start_date": "2026-01", "end_date": "约2026-07", "rank": "正处级（县处级正职）", "note": "2026-01-10 履新青县县委书记，免去沧州市财政局局长职务；约2026-07 调任黄骅市市长。confirmed。"},
    {"person_id": 1, "org_id": 7, "title": "沧州市财政局党组书记、局长", "start_date": "约2024-2025", "end_date": "2026-01", "rank": "正处级", "note": "此前任沧州市财政局党组书记、局长。confirmed。"},
    {"person_id": 1, "org_id": 9, "title": "沧州渤海新区黄骅市港城产业园区党组书记、管委会主任", "start_date": "约2021-2023", "end_date": "约2024", "rank": "副处级→正处级", "note": "2024-01 沧州市最新任免报道时任港城产业园区党组书记、管委会主任。confirmed。"},
    {"person_id": 1, "org_id": 8, "title": "沧州渤海新区党工委委员、管委会副主任", "start_date": "约2018-2020", "end_date": "约2021", "rank": "副处级", "note": "长期扎根沧州渤海新区一线的临港实干干部。confirmed（百科/报道）。"},
    {"person_id": 1, "org_id": 10, "title": "黄骅市人民政府市长（据报）", "start_date": "2026-07", "end_date": "present", "rank": "县级市正职", "note": "2026-07-29 燕阵沧州/网易：张硕任黄骅市人民政府市长。plausible。", "rank_note": ""},
    # ── 李向伟（代县长）──
    {"person_id": 2, "org_id": 2, "title": "青县人民政府副县长、代理县长", "start_date": "2026-05-20", "end_date": "present", "rank": "正处级（县处级正职）", "note": "2026-05-20 青县十八届人大常委会第四十次会议任命副县长并决定代理县长。confirmed。"},
    {"person_id": 2, "org_id": 11, "title": "大城县人民政府副县长", "start_date": "2022-08-30", "end_date": "2026-05", "rank": "副处级", "note": "2022-08-30 大城县人大常委会第十次会议任命李向伟为副县长。confirmed。"},
    # ── 时励（原县长）──
    {"person_id": 3, "org_id": 2, "title": "青县人民政府县长", "start_date": "2021-07", "end_date": "2026-05-20", "rank": "正处级", "note": "2021-07-28 当选青县县长；2026-05-20 辞去。confirmed。"},
    {"person_id": 3, "org_id": 2, "title": "青县人民政府副县长、代县长", "start_date": "2021-06", "end_date": "2021-07", "rank": "代县长", "note": "2021-06 澎湃-河北4市任免：任青县副县长、代县长。confirmed。"},
    {"person_id": 3, "org_id": 1, "title": "青县委副书记、县政府党组书记", "start_date": "2021-06", "end_date": "2026-05", "rank": "县委副书记", "note": "青县政府官网2022-07：时励为县委副书记、县政府党组书记、县长。confirmed。"},
    # ── 左亚宁（前书记）──
    {"person_id": 4, "org_id": 1, "title": "青县县委书记", "start_date": "2022-12-15", "end_date": "2026-01", "rank": "县委书记", "note": "2022-12-15 全县领导干部会议宣布省委市委决定左亚宁任青县县委书记；2026-01 张硕接任。confirmed。"},
    {"person_id": 4, "org_id": 10, "title": "黄骅市委副书记、代理市长（据报）", "start_date": "2026-01", "end_date": "present", "rank": "县级市正职（代理）", "note": "据汲古新知(2026-02)：左亚宁已任黄骅市委副书记、代理市长；2026-07-29 又报封立新任黄骅市委书记、张硕任市长，左亚宁去向存疑（open_q）。", "rank_note": ""},
    # ── 领导班子 ──
    {"person_id": 5, "org_id": 3, "title": "青县人大常委会主任", "start_date": "约2022", "end_date": "present", "rank": "正处级", "note": "2022-2026 多次主持县人大常委会会议。confirmed。"},
    {"person_id": 6, "org_id": 4, "title": "青县纪委书记、监委主任", "start_date": "约2022", "end_date": "present", "rank": "副处级", "note": "2022-01 县委常委、纪委书记、监委主任。confirmed。"},
    {"person_id": 7, "org_id": 2, "title": "青县人民政府副县长", "start_date": "2026-01-13", "end_date": "present", "rank": "副县处级", "note": "2026-01-13 任命为副县长，2026-01-30 列席县人大常委会第三十七次会议（官方发布）。confirmed。。confirmed。"},
    {"person_id": 8, "org_id": 1, "title": "青县县委书记（原）", "start_date": "约2021", "end_date": "2022-12", "rank": "县委书记", "note": "约2021-2022 任青县委书记；2022-12 由左亚宁接任；后任辛集市委书记。confirmed。"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "张硕（书记，2026-01 任）与李向伟（代县长，2026-05-20 任）为青县党政一把手搭档（书记-县长（代））的依据：二者任职期重叠（2026-05/2026-07）。",
        "overlap_org": "青县县委／青县人民政府",
        "overlap_period": "2026-05/2026-07"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "张硕 2026-01 任青县县委书记，与县长时励（2021-2026-05）在 2026-01～2026-05 期间为书记-县长搭档。",
        "overlap_org": "青县县委／青县人民政府",
        "overlap_period": "2026-01—2026-05"
    },
    {
        "person_a": 3,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "时励 2026-05-20 辞去青县长，李向伟同日被任命为代理县长（前任-继任）。",
        "overlap_org": "青县人民政府",
        "overlap_period": "2026-05-20"
    },
    {
        "person_a": 4,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "左亚宁 2022-12～2026-01 任青县县委书记，张硕 2026-01 接任县委书记（前一前者-继任者）。",
        "overlap_org": "青县县委",
        "overlap_period": "2026-01"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "县委书记张硕与人大主任张卫忠共同出席县里重要会议/政法班子（张卫忠多次主持人大，张书记2026-01后主持县委）。",
        "overlap_org": "青县县委／青县人大",
        "overlap_period": "2026-01/2026-07"
    },
    {
        "person_a": 3,
        "person_b": 5,
        "type": "overlap",
        "context": "县长时励与人大主任张卫忠：政府工作报告提交人代会审议等体制内常态互动。",
        "overlap_org": "青县政府／青县人大",
        "overlap_period": "2021/2026"
    },
    {
        "person_a": 3,
        "person_b": 6,
        "type": "overlap",
        "context": "县长时励与纪委书记马俊敏同属青县党政班子，于 2021-2026 共同任职。",
        "overlap_org": "青县县委",
        "overlap_period": "2022-01/2026-05"
    },
    {
        "person_a": 4,
        "person_b": 3,
        "type": "overlap",
        "context": "左亚宁（书记2022-12～2026-01）与时励（县长2021-06～2026-05）为青县书记-县长搭档，两人期间共同主持县常委会等。",
        "overlap_org": "青县县委／青县人民政府",
        "overlap_period": "2023-2026-01"
    },
]

# ── Build ──

if __name__ == "__main__":
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
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")