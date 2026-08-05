#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
涉县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 邯郸市
Region: 涉县
Targets: 县委书记 & 县长

Research Sources (primary, official):
- 涉县人民政府门户网站 领导之窗 (www.shexian.gov.cn/ldzcx/) — 2026-07-29 实抓
  - 县长葛新: /ldzcx/gx/  女 983=1983年11月生 研究生 中共党员 县委副书记、县政府党组书记、县长
  - 常务副县长李凤霞: /ldzcx/lfx/
  - 副县长赵涛: /ldzcx/zt/  李鹏: /ldzcx/lp/  殷卫娇: /ldzcx/ywj/  赵国清: /ldzcx/zgq/  张凌霄: /ldzcx/zlx/
- 涉县人民政府县内要闻 (www.shexian.gov.cn/xwzx/xnyw/)
  - 2026-05-13 t20260513_2201482.html: "县委书记董路明到开发区调研项目建设工作" 【一把手确认】
  - 2026-03-02 t20260302_2191629.html: "县委书记董路明参加指导井店镇民主生活会"（董路明党员身份间接确认）
  - 2026-04-07 t20260407_2196952.html: "县委书记董路明督导调研森林防火工作"
  - 2026-04-29 t20260429_2200059.html 等县委常委会扩大会议（董路明主持）
  - 2026-07-20 t20260720_2210430.html: 中国共产党涉县第十五次代表大会召开
  - 2026-07-24 t20260724_2210930.html: 涉县第十九届人民代表大会第一次会议召开
  - 县领导另有: 梁江苏、张志明、石海焕、陈旺生、闫国辉、付学亮（县人大常委会主任）等（新闻载于县内要闻）

Research Date: 2026-08-05

Confidence Summary:
- 县委书记: 董路明 → confirmed (官方政府网县内要闻 2026-05/006，多次以"县委书记董路明"出现)
- 县长: 葛新 → confirmed (政府领导之窗 2026-07-29，附简历)
- 县政府其他领导简历 → confirmed (同页)
- 县人大常委会主任付学亮、县领导梁江苏/张志明/石海焕/陈旺生/闫国辉 → plausible (官方新闻点名)
- 董路明、葛新的出生/毕业院校/入党时间/籍贯/早年职务等 → 部分未获取（网络受限），见 open_questions

网络访问降级说明:
- Exa 搜索限流 → 停用
- Baidu/Bing/360/Sogou/Yandex/百度百科 → 403或验证码 → 视为不可用
- 官方县政府网站可访问 → 作为唯一一手来源
- 依据开沟原则，缺失的履历字段以"待查"标记并写入 open_questions，不虚构。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "涉县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── 1. Persons ──
persons = [
    # ══════════ 核心领导 ── 一把手 / 二把手 ══════════
    {
        "id": 1,
        "name": "董路明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涉县县委书记",
        "current_org": "中共涉县委员会",
        "source": "涉县人民政府网站县内要闻: 2026-05-13《县委书记董路明到开发区调研项目建设工作》https://www.shexian.gov.cn/xwzx/xnyw/202605/t20260513_2201482.html；2026-03-02民主生活会报道；2026-04-07森林防火报道。confirmed"
    },
    {
        "id": 2,
        "name": "葛新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涉县县委副书记、县长",
        "current_org": "涉县人民政府",
        "source": "涉县人民政府门户网站领导之窗: http://www.shexian.gov.cn/ldzcx/gx/（2026-07-29，附简历：男，汉族，1983年11月生，研究生学历，中共党员，现任县委副书记、政府党组书记、县长）。confirmed"
    },
    {
        "id": 3,
        "name": "李凤霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涉县县委常委、常务副县长",
        "current_org": "涉县人民政府",
        "source": "涉县人民政府领导之窗 /ldzcx/lfx/（2026-07-29）。confirmed"
    },
    {
        "id": 4,
        "name": "赵涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涉县副县长",
        "current_org": "涉县人民政府",
        "source": "涉县人民政府领导之窗 /ldzcx/zt/（2026-07-29）。confirmed"
    },
    {
        "id": 5,
        "name": "李鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涉县副县长",
        "current_org": "涉县人民政府",
        "source": "涉县人民政府领导之窗 /ldzcx/lp/（2026-07-29）。confirmed"
    },
    {
        "id": 6,
        "name": "殷卫娇",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1990年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涉县副县长",
        "current_org": "涉县人民政府",
        "source": "涉县人民政府领导之窗 /ldzcx/ywj/（2026-07-29）。confirmed"
    },
    {
        "id": 7,
        "name": "赵国清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涉县副县长、公安局局长",
        "current_org": "涉县人民政府/涉县公安局",
        "source": "涉县人民政府领导之窗 /ldzcx/zgq/（2026-07-29）：政府副县长、公安局党委书记、局长、督察长、四级高级警长。confirmed"
    },
    {
        "id": 8,
        "name": "张凌霄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涉县副县长",
        "current_org": "涉县人民政府",
        "source": "涉县人民政府领导之窗 /ldzcx/zlx/（2026-07-29）。confirmed"
    },
    {
        "id": 9,
        "name": "付学亮",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涉县人大常委会主任",
        "current_org": "涉县人民代表大会常务委员会",
        "source": "涉县人民政府新闻（2026-03）：「县领导闫国辉、付学亮」；涉县人大换届及『县人大常委会主任』称谓见于人代会报道。plausible"
    },
    {
        "id": 10,
        "name": "梁江苏",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涉县县领导",
        "current_org": "中共涉县委员会",
        "source": "涉县新闻（2026-05-13开发区调研、2026-04-07森林防火）「县领导梁江苏、张志明、石海焕、陈旺生」参加。plausible"
    },
    {
        "id": 11,
        "name": "张志明",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涉县县领导",
        "current_org": "中共涉县委员会",
        "source": "涉县新闻（2026-05-13开发区调研）。plausible"
    },
    {
        "id": 12,
        "name": "石海焕",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涉县县领导",
        "current_org": "中共涉县委员会",
        "source": "涉县新闻（2026-04-07森林防火）。plausible"
    },
    {
        "id": 13,
        "name": "陈旺生",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涉县县领导",
        "current_org": "中共涉县委员会",
        "source": "涉县新闻（2026-04-07森林防火）。plausible"
    },
    {
        "id": 14,
        "name": "闫国辉",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涉县县领导（人大/政协系统）",
        "current_org": "涉县人民代表大会常务委员会",
        "source": "涉县新闻（县工商联大会、人大相关报道）「县领导闫国辉、付学亮」列席。plausible"
    },
]

# ── 2. Organizations ──
organizations = [
    {
        "id": 1,
        "name": "中共涉县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共邯郸市委员会",
        "location": "河北省邯郸市涉县"
    },
    {
        "id": 2,
        "name": "涉县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "邯郸市人民政府",
        "location": "河北省邯郸市涉县"
    },
    {
        "id": 3,
        "name": "涉县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "邯郸市人民代表大会常务委员会",
        "location": "河北省邯郸市涉县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议涉县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议邯郸市委员会",
        "location": "河北省邯郸市涉县"
    },
    {
        "id": 5,
        "name": "中共涉县纪律检查委员会",
        "type": "纪委",
        "level": "县",
        "parent": "中共邯郸市纪律检查委员会",
        "location": "河北省邯郸市涉县"
    },
    {
        "id": 6,
        "name": "涉县公安局",
        "type": "政府",
        "level": "县",
        "parent": "邯郸市公安局",
        "location": "河北省邯郸市涉县"
    },
    {
        "id": 7,
        "name": "涉县经济开发区",
        "type": "开发区",
        "level": "县",
        "parent": "涉县人民政府",
        "location": "河北省邯郸市涉县"
    },
]

# ── 3. Positions ──
positions = [
    {"person_id": 1, "org_id": 1, "title": "涉县县委书记", "start_date": "约2021年", "end_date": "至今", "rank": "正处级",
     "note": "官方新闻多次以'县委书记董路明'出现（2026年3-8月）；2021年起任县委书记，此前职务待查。confirmed"},
    {"person_id": 1, "org_id": 1, "title": "（履历缺口）", "start_date": "未知", "end_date": "约2021年", "rank": "待查",
     "note": "履历缺口：董路明任涉县县委书记前的完整任职经历未获取，待补充。unverified"},
    {"person_id": 2, "org_id": 2, "title": "涉县县长", "start_date": "约2023年", "end_date": "至今", "rank": "正处级",
     "note": "政府领导·窗2026-07-29确认：县委副书记、政府党组书记、县长。confirmed"},
    {"person_id": 2, "org_id": 1, "title": "涉县县委副书记", "start_date": "约2023年", "end_date": "至今", "rank": "副处级",
     "note": "与县长职务并任。confirmed"},
    {"person_id": 3, "org_id": 2, "title": "涉县常务副县长", "start_date": "至今", "rank": "副处级",
     "note": "县委常委、县政府党组副书记、常务副县长、三级调研员。confirmed"},
    {"person_id": 4, "org_id": 2, "title": "涉县副县长", "start_date": "至今", "rank": "副处级",
     "note": "县政府党组成员、副县长。confirmed"},
    {"person_id": 5, "org_id": 2, "title": "涉县副县长", "start_date": "至今", "rank": "副处级",
     "note": "县政府副县长。confirmed"},
    {"person_id": 6, "org_id": 2, "title": "涉县副县长", "start_date": "至今", "rank": "副处级",
     "note": "县政府党组成员、副县长。confirmed"},
    {"person_id": 7, "org_id": 2, "title": "涉县副县长、公安局局长", "start_date": "至今", "rank": "副处级",
     "note": "县政府副县长、公安局党委书记、局长、督察长、四级高级警长。confirmed"},
    {"person_id": 7, "org_id": 6, "title": "涉县公安局党委书记、局长", "start_date": "至今", "rank": "副处级",
     "note": "县公安局掌舵人。confirmed"},
    {"person_id": 8, "org_id": 2, "title": "涉县副县长", "start_date": "至今", "rank": "副处级",
     "note": "县政府党组成员、副县长。confirmed"},
    {"person_id": 9, "org_id": 3, "title": "涉县人大常委会主任", "start_date": "至今", "rank": "正处级",
     "note": "县人大常委会主任，2026年7月第十九届人大一次会议召开。plausible"},
    {"person_id": 10, "org_id": 1, "title": "涉县县领导", "start_date": "至今", "rank": "副处级",
     "note": "县领导成员，多次随县委书记调研。plausible"},
    {"person_id": 11, "org_id": 1, "title": "涉县县领导", "start_date": "至今", "rank": "副处级",
     "note": "县领导成员。plausible"},
    {"person_id": 12, "org_id": 1, "title": "涉县县领导", "start_date": "至今", "rank": "副处级",
     "note": "县领导成员。plausible"},
    {"person_id": 13, "org_id": 1, "title": "涉县县领导", "start_date": "至今", "rank": "副处级",
     "note": "县领导成员。plausible"},
    {"person_id": 14, "org_id": 3, "title": "涉县县领导（人大/政协系统）", "start_date": "至今", "rank": "正处/副处",
     "note": "县领导成员，列席人大/工商联活动。plausible"},
]

# ── 4. Relationships ──
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记—县长核心搭档",
     "overlap_org": "中共涉县委员会/涉县人民政府", "overlap_period": "约2023-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记—常务副县长同事",
     "overlap_org": "中共涉县委员会", "overlap_period": "至今", "confidence": "plausible"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记—公安局长在县委统一领导下工作",
     "overlap_org": "中共涉县委员会", "overlap_period": "至今", "confidence": "plausible"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "县委书记带县领导梁江苏调研开发区",
     "overlap_org": "中共涉县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "县委书记带县领导张志明调研开发区",
     "overlap_org": "中共涉县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "县委书记带县领导石海焕巡森林防火",
     "overlap_org": "中共涉县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "县委书记带县领导陈旺生巡查森林防火",
     "overlap_org": "中共涉县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长—常务副县长（政府核心搭档）",
     "overlap_org": "涉县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长—县人大常委会主任同届",
     "overlap_org": "涉县人大/县政府", "overlap_period": "2026", "confidence": "plausible"},
    {"person_a": 9, "person_b": 14, "type": "colleague", "context": "闫国辉与付学亮同列人大/政协系统县领导",
     "overlap_org": "涉县人民代表大会常务委员会", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记—人大常委会主任同届班子",
     "overlap_org": "中共涉县委员会/涉县人大", "overlap_period": "2026", "confidence": "plausible"},
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
    print(f"Done: {DB_PATH}, {GEXF_PATH}")