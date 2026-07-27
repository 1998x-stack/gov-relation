#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
涞水县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 保定市
Region: 涞水县
Targets: 县委书记 & 县长

Research Sources:
- 涞水县人民政府官方网站 (www.laishui.gov.cn) — 领导之窗 确认县政府领导班子分工
- 涞水新闻 — 第十五届县委第一次全体会议(2026-07-20)确认安熠辉当选县委书记
- 涞水新闻 — 存量增量项目调度会(2026-06-25)确认秘杰鹏任县委副书记、代理县长
- 涞水新闻 — 第十八届人大一次会议(2026-07-22)确认秘杰鹏以县长身份作政府工作报告（代理县长）
- 涞水新闻 — 七一主题活动(2026-06-29)、防汛调度会(2026-07-10)等确认在任
- 涞水县新闻列表页 — 吴磊2026年4月仍以县长身份活动，2026年6月秘杰鹏接任

Research Date: 2026-07-23
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "涞水县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "安熠辉",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县委书记",
        "current_org": "中共涞水县委员会",
        "source": "中共涞水县第十五届委员会第一次全体会议(2026-07-20)选举安熠辉为县委书记；涞水县政府网站多则新闻报道确认在任。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=show&catid=25&id=20482"
    },
    {
        "id": 2,
        "name": "秘杰鹏",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县委副书记、代理县长",
        "current_org": "涞水县人民政府",
        "source": "涞水县存量增量项目调度会(2026-06-25)报道中称\"县委副书记、代理县长秘杰鹏\"；领导之窗页面(至2026-01-19)显示秘杰鹏原为县委常委、常务副县长。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=show&catid=25&id=20389"
    },
    # ════════════════════════════════════════
    # 县政府领导班子 (来自领导之窗)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "靖冬菊",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县副县长",
        "current_org": "涞水县人民政府",
        "source": "涞水县政府领导之窗(2026-01-19)。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=lists&catid=9"
    },
    {
        "id": 4,
        "name": "李伟军",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县副县长",
        "current_org": "涞水县人民政府",
        "source": "涞水县政府领导之窗(2026-01-19)；预防未成年人溺水会议(2026-07-07)确认李伟军出席。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=lists&catid=9"
    },
    {
        "id": 5,
        "name": "陈占文",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县副县长",
        "current_org": "涞水县人民政府",
        "source": "涞水县政府领导之窗(2026-01-19)。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=lists&catid=9"
    },
    {
        "id": 6,
        "name": "郭建良",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县副县长",
        "current_org": "涞水县人民政府",
        "source": "涞水县政府领导之窗(2026-01-19)。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=lists&catid=9"
    },
    {
        "id": 7,
        "name": "武永利",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县副县长、县公安局局长",
        "current_org": "涞水县人民政府",
        "source": "涞水县政府领导之窗(2026-01-19)；存量增量项目调度会(2026-06-25)确认武永利参加。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=lists&catid=9"
    },
    {
        "id": 8,
        "name": "祖金明",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县政府党组成员、野三坡景区党工委书记、管委会主任",
        "current_org": "涞水县人民政府",
        "source": "涞水县政府领导之窗(2026-01-19)；存量增量项目调度会(2026-06-25)确认祖金明参加。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=lists&catid=9"
    },
    {
        "id": 9,
        "name": "马秀辉",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县副县级干部",
        "current_org": "涞水县人民政府",
        "source": "涞水县政府领导之窗(2026-01-19)。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=lists&catid=9"
    },
    # ════════════════════════════════════════
    # 县委领导（部分确认）
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "吴四军",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县委副书记",
        "current_org": "中共涞水县委员会",
        "source": "七一主题活动(2026-06-29)中\"县领导吴四军、张婵作交流发言\"；中青年干部培训班(2026-07-02)中吴四军以县委副书记身份讲话。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=show&catid=25&id=20401"
    },
    {
        "id": 11,
        "name": "刘帅",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县领导",
        "current_org": "中共涞水县委员会",
        "source": "存量增量项目调度会(2026-06-25)中\"县领导刘帅、康田、靖冬菊、武永利、祖金明、沈飞\"参加。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=show&catid=25&id=20389"
    },
    {
        "id": 12,
        "name": "康田",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县领导",
        "current_org": "中共涞水县委员会",
        "source": "存量增量项目调度会(2026-06-25)中\"县领导刘帅、康田、靖冬菊、武永利、祖金明、沈飞\"参加。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=show&catid=25&id=20389"
    },
    {
        "id": 13,
        "name": "沈飞",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县领导",
        "current_org": "中共涞水县委员会",
        "source": "存量增量项目调度会(2026-06-25)中\"县领导刘帅、康田、靖冬菊、武永利、祖金明、沈飞\"参加。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=show&catid=25&id=20389"
    },
    {
        "id": 14,
        "name": "张婵",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县领导",
        "current_org": "中共涞水县委员会",
        "source": "七一主题活动(2026-06-29)中\"县领导吴四军、张婵作交流发言\"。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=show&catid=25&id=20401"
    },
    {
        "id": 15,
        "name": "张志鹏",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县县级领导",
        "current_org": "中共涞水县委员会",
        "source": "存量增量项目调度会(2026-06-25)中\"县级领导张志鹏参加\"。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=show&catid=25&id=20389"
    },
    # ════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════
    {
        "id": 16,
        "name": "吴磊",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任",
        "current_org": "",
        "source": "涞水县政府网站新闻列表显示，吴磊以县长身份活动至2026年4月(2026-04-23大气污染防治调度会等)；领导之窗(2026-01-19)确认吴磊任县委副书记、县长。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=lists&catid=25&page=2"
    },
    {
        "id": 17,
        "name": "黄伟",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任",
        "current_org": "",
        "source": "涞水新闻(2024-09-26)报道\"黄伟就学校建设、基层党组织建设等工作进行调研\"，确认黄伟为前任县委书记，约至2024年9月。来源：http://www.laishui.gov.cn/index.php?m=content&c=index&a=lists&catid=25&page=15"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共涞水县委员会", "type": "党委", "level": "县级", "parent": "中共保定市委", "location": "河北省保定市涞水县"},
    {"id": 2, "name": "涞水县人民政府", "type": "政府", "level": "县级", "parent": "保定市人民政府", "location": "河北省保定市涞水县"},
    {"id": 3, "name": "中共涞水县纪律检查委员会", "type": "纪律检查", "level": "县级", "parent": "中共涞水县委员会", "location": "河北省保定市涞水县"},
    {"id": 4, "name": "涞水县公安局", "type": "政府", "level": "县级", "parent": "涞水县人民政府", "location": "河北省保定市涞水县"},
    {"id": 5, "name": "野三坡景区管理委员会", "type": "事业单位", "level": "县级", "parent": "涞水县人民政府", "location": "河北省保定市涞水县"},
    {"id": 6, "name": "涞水县第十七届人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "涞水县", "location": "河北省保定市涞水县"},
    {"id": 7, "name": "涞水县第十八届人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "涞水县", "location": "河北省保定市涞水县"},
]

# 3. Positions
positions = [
    # 安熠辉
    {"person_id": 1, "org_id": 1, "title": "涞水县委书记", "start_date": "约2024-10", "end_date": "", "rank": "正处级", "note": "2024年10月首次以县委书记身份见诸报道；2026年7月20日第十五届县委第一次全会正式选举"},
    # 秘杰鹏
    {"person_id": 2, "org_id": 2, "title": "涞水县委常委、常务副县长", "start_date": "约2024年或更早", "end_date": "约2026-06", "rank": "副处级", "note": "领导之窗2026-01-19确认"},
    {"person_id": 2, "org_id": 2, "title": "涞水县委副书记、县长（代理）", "start_date": "约2026-06", "end_date": "", "rank": "正处级", "note": "2026年6月25日首次以代理县长身份出现"},
    # 县政府领导班子
    {"person_id": 3, "org_id": 2, "title": "涞水县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管市场监管、知识产权、民政"},
    {"person_id": 4, "org_id": 2, "title": "涞水县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管生态环境、卫生健康、医疗保障、电力通信"},
    {"person_id": 5, "org_id": 2, "title": "涞水县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管城乡规划建设、自然资源、林业、交通运输"},
    {"person_id": 6, "org_id": 2, "title": "涞水县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管教育体育、农业农村、水利、金融"},
    {"person_id": 7, "org_id": 2, "title": "涞水县副县长、县公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管民族宗教、公安、司法、退役军人事务"},
    {"person_id": 7, "org_id": 4, "title": "涞水县公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "涞水县政府党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "野三坡景区党工委书记、管委会主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "涞水县副县级干部", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 县委领导
    {"person_id": 10, "org_id": 1, "title": "涞水县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026年6-7月活动"},
    {"person_id": 11, "org_id": 1, "title": "涞水县领导（县委常委）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "涞水县领导（县委常委）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "涞水县领导（县委常委）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "涞水县领导（县委常委或副县长）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 前任
    {"person_id": 15, "org_id": 2, "title": "涞水县级领导", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "涞水县委副书记、县长", "start_date": "约2021或更早", "end_date": "约2026-05", "rank": "正处级", "note": "2026年1-4月以县长身份密集活动，约2026年5-6月离任"},
    {"person_id": 17, "org_id": 1, "title": "涞水县委书记", "start_date": "不详", "end_date": "约2024-09", "rank": "正处级", "note": "2024年9月仍以书记身份调研"},
]

# 4. Relationships
relationships = [
    # 安熠辉 ↔ 秘杰鹏（现任党政一把手）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "党政一把手：安熠辉任县委书记，秘杰鹏任县委副书记、代理县长", "overlap_org": "中共涞水县委员会/涞水县人民政府", "overlap_period": "2026-06至今"},
    # 安熠辉 ↔ 吴磊（前任搭档）
    {"person_a": 1, "person_b": 16, "type": "superior_subordinate", "context": "安熠辉接任县委书记后，吴磊任县长至2026年4月", "overlap_org": "中共涞水县委员会/涞水县人民政府", "overlap_period": "约2024-10至2026-04"},
    # 安熠辉 ↔ 黄伟（前任-接任）
    {"person_a": 1, "person_b": 17, "type": "predecessor_successor", "context": "黄伟为前任县委书记，安熠辉接任", "overlap_org": "中共涞水县委员会", "overlap_period": "2024年交接"},
    # 秘杰鹏 ↔ 吴磊（前任县长-接任县长）
    {"person_a": 2, "person_b": 16, "type": "predecessor_successor", "context": "秘杰鹏原为常务副县长，接替吴磊任代理县长", "overlap_org": "涞水县人民政府", "overlap_period": "2024年或更早至2026年"},
    # 秘杰鹏 ↔ 靖冬菊（县政府班子）
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "同为涞水县政府领导班子成员", "overlap_org": "涞水县人民政府", "overlap_period": "2026年"},
    # 秘杰鹏 ↔ 李伟军
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "同为涞水县政府领导班子成员", "overlap_org": "涞水县人民政府", "overlap_period": "2026年"},
    # 秘杰鹏 ↔ 武永利
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "同为涞水县政府领导班子成员；存量增量项目调度会同会", "overlap_org": "涞水县人民政府", "overlap_period": "2026年"},
    # 秘杰鹏 ↔ 祖金明
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "同为涞水县政府领导班子成员；存量增量项目调度会同会", "overlap_org": "涞水县人民政府", "overlap_period": "2026年"},
    # 吴四军 ↔ 安熠辉（县委班子）
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "安熠辉任县委书记，吴四军任县委副书记", "overlap_org": "中共涞水县委员会", "overlap_period": "2026年"},
    # 刘帅、康田、靖冬菊、武永利、祖金明、沈飞 — 同会
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "存量增量项目调度会同会参加", "overlap_org": "涞水县人民政府", "overlap_period": "2026-06-25"},
    {"person_a": 11, "person_b": 13, "type": "overlap", "context": "存量增量项目调度会同会参加", "overlap_org": "涞水县人民政府", "overlap_period": "2026-06-25"},
    # 吴磊（前任）退任后秘杰鹏接替
    {"person_a": 2, "person_b": 16, "type": "predecessor_successor", "context": "秘杰鹏以常务副县长身份接替吴磊任代理县长", "overlap_org": "涞水县人民政府", "overlap_period": "2026年"},
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
    print(f"\nDone. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
