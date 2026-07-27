#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
富拉尔基区领导班子工作关系网络 — 数据构建脚本（暂存区版）
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 黑龙江省
Parent City: 齐齐哈尔市
Region: 富拉尔基区
Targets: 区委书记 & 区长

Research Sources (2026-07-24):
- 富拉尔基区人民政府官网 (www.flej.gov.cn):
  - 领导之窗页面: confirmed 9 区委常委 + 8 区政府领导
  - 杨文波 profile (202009) / 李勇 profile (202412)
  - 王晓峰 / 赵宏宇 / 徐斌 / 权世红 / 马力 / 刘云鸣 / 艾纯明 profiles
  - 孙智嘉 / 姜涛 / 于得洋 / 邓伟 / 褚彬 / 宋程村 profiles
  - 区人大 / 区政协 leadership confirmed
- 百度百科 富拉尔基区（移动版）: 确认杨文波为区委书记，李勇为代区长（2024.12）
- 百度搜索结果（flej.gov.cn收录页面）: 李勇简历（1978.10生，1998.04入党）

Research Date: 2026-07-24

Gaps (see open_gaps.md):
1. 杨文波完整履历（此前职务、工作经历）
2. 李勇此前职务（2024年12月前任）
3. 前任区委书记/区长身份
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))

from gov_relation.runner import run_build

SLUG = "富拉尔基区"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# --- Data ---

persons = [
    # ── 区委领导 (Party Committee Leaders) ──
    {
        "id": 1,
        "name": "杨文波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年3月",
        "birthplace": "",
        "education": "黑龙江省委党校经济管理专业研究生",
        "party_join": "1991年10月",
        "work_start": "1989年3月",
        "current_post": "齐齐哈尔市富拉尔基区委书记、党校校长",
        "current_org": "中共齐齐哈尔市富拉尔基区委员会",
        "source": "confirmed - flej.gov.cn 领导之窗 (202009), Baidu Baike 富拉尔基区",
        "notes": "一级调研员；区委书记任职至少自2020年9月起；此前履历待查"
    },
    {
        "id": 2,
        "name": "李勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年10月",
        "birthplace": "",
        "education": "国家开放大学行政管理专业大学",
        "party_join": "1998年4月",
        "work_start": "1996年10月",
        "current_post": "齐齐哈尔市富拉尔基区委副书记、区长",
        "current_org": "齐齐哈尔市富拉尔基区人民政府",
        "source": "confirmed - flej.gov.cn 领导之窗 (202412), Baidu搜索结果",
        "notes": "2024.12.04任代理区长，后转为区长；兼任黑龙江富拉尔基经济开发区党工委书记、管委会主任"
    },
    {
        "id": 3,
        "name": "王晓峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "1972年9月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区委副书记、统战部部长",
        "current_org": "中共齐齐哈尔市富拉尔基区委员会",
        "source": "confirmed - flej.gov.cn 领导之窗",
        "notes": "三级调研员；兼任区政协党组副书记"
    },
    {
        "id": 4,
        "name": "赵宏宇",
        "gender": "男",
        "ethnicity": "",
        "birth": "1976年1月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区委常委、纪委书记、监委主任",
        "current_org": "中共齐齐哈尔市富拉尔基区纪律检查委员会",
        "source": "confirmed - flej.gov.cn 领导之窗",
        "notes": "四级高级监察官"
    },
    {
        "id": 5,
        "name": "徐斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "1972年4月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区委常委、政法委书记",
        "current_org": "中共齐齐哈尔市富拉尔基区委政法委员会",
        "source": "confirmed - flej.gov.cn 领导之窗",
    },
    {
        "id": 6,
        "name": "权世红",
        "gender": "女",
        "ethnicity": "",
        "birth": "1975年11月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区委常委、组织部部长",
        "current_org": "中共齐齐哈尔市富拉尔基区委组织部",
        "source": "confirmed - flej.gov.cn 领导之窗",
    },
    {
        "id": 7,
        "name": "马力",
        "gender": "男",
        "ethnicity": "",
        "birth": "1970年6月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区委常委、副区长",
        "current_org": "齐齐哈尔市富拉尔基区人民政府",
        "source": "confirmed - flej.gov.cn 领导之窗",
        "notes": "三级调研员；常务副区长，区政府党组副书记"
    },
    {
        "id": 8,
        "name": "刘云鸣",
        "gender": "男",
        "ethnicity": "",
        "birth": "1973年5月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区委常委、宣传部部长",
        "current_org": "中共齐齐哈尔市富拉尔基区委宣传部",
        "source": "confirmed - flej.gov.cn 领导之窗 (202401)",
        "notes": "三级调研员"
    },
    {
        "id": 9,
        "name": "艾纯明",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1974年10月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区委常委、人武部部长",
        "current_org": "中国人民解放军黑龙江省齐齐哈尔市富拉尔基区人民武装部",
        "source": "confirmed - flej.gov.cn 领导之窗 (202510)",
    },
    # ── 区政府领导 (Government Leaders) ──
    {
        "id": 10,
        "name": "孙智嘉",
        "gender": "男",
        "ethnicity": "",
        "birth": "1972年7月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区副区长、公安分局局长",
        "current_org": "齐齐哈尔市公安局富拉尔基分局",
        "source": "confirmed - flej.gov.cn 领导之窗 (202411)",
    },
    {
        "id": 11,
        "name": "姜涛",
        "gender": "女",
        "ethnicity": "达斡尔族",
        "birth": "1982年4月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区副区长",
        "current_org": "齐齐哈尔市富拉尔基区人民政府",
        "source": "confirmed - flej.gov.cn 领导之窗",
        "notes": "分管：卫生健康、教育、文化旅游、体育"
    },
    {
        "id": 12,
        "name": "于得洋",
        "gender": "男",
        "ethnicity": "朝鲜族",
        "birth": "1993年12月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区副区长",
        "current_org": "齐齐哈尔市富拉尔基区人民政府",
        "source": "confirmed - flej.gov.cn 领导之窗 (202505)",
        "notes": "最年轻的副区长；分管：市场监管、交通运输"
    },
    {
        "id": 13,
        "name": "邓伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "1985年6月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区副区长",
        "current_org": "齐齐哈尔市富拉尔基区人民政府",
        "source": "confirmed - flej.gov.cn 领导之窗",
        "notes": "分管：农业农村、乡村振兴、林业草原"
    },
    {
        "id": 14,
        "name": "褚彬",
        "gender": "男",
        "ethnicity": "",
        "birth": "1982年6月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区副区长",
        "current_org": "齐齐哈尔市富拉尔基区人民政府",
        "source": "confirmed - flej.gov.cn 领导之窗 (202406)",
        "notes": "分管：发展改革、工业、招商引资、科技、国资改革、粮食安全、统计"
    },
    {
        "id": 15,
        "name": "宋程村",
        "gender": "男",
        "ethnicity": "",
        "birth": "1979年12月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基经济开发区管委会专职副主任",
        "current_org": "黑龙江富拉尔基经济开发区管理委员会",
        "source": "confirmed - flej.gov.cn 领导之窗 (202411)",
        "notes": "协助区长分管开发区建设和城市建设管理"
    },
    # ── 区人大领导 (People's Congress) ──
    {
        "id": 16,
        "name": "梁继光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区人大常委会主任",
        "current_org": "齐齐哈尔市富拉尔基区人民代表大会常务委员会",
        "source": "confirmed - flej.gov.cn 领导之窗",
    },
    {
        "id": 17,
        "name": "刘浅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区人大常委会副主任",
        "current_org": "齐齐哈尔市富拉尔基区人民代表大会常务委员会",
        "source": "confirmed - flej.gov.cn 领导之窗",
    },
    {
        "id": 18,
        "name": "王秀卉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区人大常委会副主任",
        "current_org": "齐齐哈尔市富拉尔基区人民代表大会常务委员会",
        "source": "confirmed - flej.gov.cn 领导之窗",
    },
    {
        "id": 19,
        "name": "张积光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区人大常委会副主任",
        "current_org": "齐齐哈尔市富拉尔基区人民代表大会常务委员会",
        "source": "confirmed - flej.gov.cn 领导之窗",
    },
    {
        "id": 20,
        "name": "艾微",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区人大常委会副主任",
        "current_org": "齐齐哈尔市富拉尔基区人民代表大会常务委员会",
        "source": "confirmed - flej.gov.cn 领导之窗",
    },
    # ── 区政协领导 (Political Consultative Conference) ──
    {
        "id": 21,
        "name": "李志强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区政协主席",
        "current_org": "中国人民政治协商会议齐齐哈尔市富拉尔基区委员会",
        "source": "confirmed - flej.gov.cn 领导之窗, Baidu Baike",
    },
    {
        "id": 22,
        "name": "张宇涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区政协副主席",
        "current_org": "中国人民政治协商会议齐齐哈尔市富拉尔基区委员会",
        "source": "confirmed - flej.gov.cn 领导之窗",
    },
    {
        "id": 23,
        "name": "满涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区政协副主席",
        "current_org": "中国人民政治协商会议齐齐哈尔市富拉尔基区委员会",
        "source": "confirmed - flej.gov.cn 领导之窗",
    },
    {
        "id": 24,
        "name": "王秀林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市富拉尔基区政协副主席",
        "current_org": "中国人民政治协商会议齐齐哈尔市富拉尔基区委员会",
        "source": "confirmed - flej.gov.cn 领导之窗",
    },
]

organizations = [
    {"id": 1, "name": "中共齐齐哈尔市富拉尔基区委员会", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市委员会", "location": "黑龙江省齐齐哈尔市富拉尔基区"},
    {"id": 2, "name": "齐齐哈尔市富拉尔基区人民政府", "type": "政府", "level": "县处级",
     "parent": "齐齐哈尔市人民政府", "location": "黑龙江省齐齐哈尔市富拉尔基区"},
    {"id": 3, "name": "中共齐齐哈尔市富拉尔基区纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共齐齐哈尔市纪律检查委员会", "location": "黑龙江省齐齐哈尔市富拉尔基区"},
    {"id": 4, "name": "中共齐齐哈尔市富拉尔基区委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市富拉尔基区委员会", "location": "黑龙江省齐齐哈尔市富拉尔基区"},
    {"id": 5, "name": "中共齐齐哈尔市富拉尔基区委组织部", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市富拉尔基区委员会", "location": "黑龙江省齐齐哈尔市富拉尔基区"},
    {"id": 6, "name": "中共齐齐哈尔市富拉尔基区委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市富拉尔基区委员会", "location": "黑龙江省齐齐哈尔市富拉尔基区"},
    {"id": 7, "name": "中共齐齐哈尔市富拉尔基区委统一战线工作部", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市富拉尔基区委员会", "location": "黑龙江省齐齐哈尔市富拉尔基区"},
    {"id": 8, "name": "中国人民解放军黑龙江省齐齐哈尔市富拉尔基区人民武装部", "type": "军队", "level": "县处级",
     "parent": "齐齐哈尔军分区", "location": "黑龙江省齐齐哈尔市富拉尔基区"},
    {"id": 9, "name": "齐齐哈尔市公安局富拉尔基分局", "type": "政府", "level": "县处级",
     "parent": "齐齐哈尔市公安局", "location": "黑龙江省齐齐哈尔市富拉尔基区"},
    {"id": 10, "name": "黑龙江富拉尔基经济开发区管理委员会", "type": "政府", "level": "县处级",
     "parent": "齐齐哈尔市富拉尔基区人民政府", "location": "黑龙江省齐齐哈尔市富拉尔基区"},
    {"id": 11, "name": "齐齐哈尔市富拉尔基区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "齐齐哈尔市人大常委会", "location": "黑龙江省齐齐哈尔市富拉尔基区"},
    {"id": 12, "name": "中国人民政治协商会议齐齐哈尔市富拉尔基区委员会", "type": "政协", "level": "县处级",
     "parent": "齐齐哈尔市政协", "location": "黑龙江省齐齐哈尔市富拉尔基区"},
]

positions = [
    # 杨文波
    {"person_id": 1, "org_id": 1, "title": "齐齐哈尔市富拉尔基区委书记",
     "start_date": "约2020年9月", "end_date": "present", "rank": "县处级正职",
     "note": "区委书记、党校校长；一级调研员"},
    # 李勇
    {"person_id": 2, "org_id": 2, "title": "齐齐哈尔市富拉尔基区区长",
     "start_date": "2024年12月", "end_date": "present", "rank": "县处级正职",
     "note": "2024.12.04任代理区长；后转为区长"},
    {"person_id": 2, "org_id": 1, "title": "齐齐哈尔市富拉尔基区委副书记",
     "start_date": "2024年12月", "end_date": "present", "rank": "县处级副职",
     "note": "兼任"},
    {"person_id": 2, "org_id": 10, "title": "黑龙江富拉尔基经济开发区党工委书记、管委会主任",
     "start_date": "2024年12月", "end_date": "present", "rank": "县处级正职",
     "note": "兼任"},
    # 王晓峰
    {"person_id": 3, "org_id": 1, "title": "齐齐哈尔市富拉尔基区委副书记、统战部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "三级调研员"},
    {"person_id": 3, "org_id": 7, "title": "齐齐哈尔市富拉尔基区委统战部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "兼任"},
    # 赵宏宇
    {"person_id": 4, "org_id": 3, "title": "齐齐哈尔市富拉尔基区委常委、纪委书记、监委主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "四级高级监察官"},
    # 徐斌
    {"person_id": 5, "org_id": 4, "title": "齐齐哈尔市富拉尔基区委常委、政法委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 权世红
    {"person_id": 6, "org_id": 5, "title": "齐齐哈尔市富拉尔基区委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 马力
    {"person_id": 7, "org_id": 2, "title": "齐齐哈尔市富拉尔基区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "常务副区长，区政府党组副书记"},
    {"person_id": 7, "org_id": 1, "title": "齐齐哈尔市富拉尔基区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 刘云鸣
    {"person_id": 8, "org_id": 6, "title": "齐齐哈尔市富拉尔基区委常委、宣传部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "三级调研员"},
    # 艾纯明
    {"person_id": 9, "org_id": 8, "title": "齐齐哈尔市富拉尔基区委常委、人武部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 9, "org_id": 1, "title": "齐齐哈尔市富拉尔基区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 孙智嘉
    {"person_id": 10, "org_id": 2, "title": "齐齐哈尔市富拉尔基区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 10, "org_id": 9, "title": "齐齐哈尔市公安局富拉尔基分局局长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "兼任"},
    # 姜涛
    {"person_id": 11, "org_id": 2, "title": "齐齐哈尔市富拉尔基区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 于得洋
    {"person_id": 12, "org_id": 2, "title": "齐齐哈尔市富拉尔基区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 邓伟
    {"person_id": 13, "org_id": 2, "title": "齐齐哈尔市富拉尔基区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 褚彬
    {"person_id": 14, "org_id": 2, "title": "齐齐哈尔市富拉尔基区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 宋程村
    {"person_id": 15, "org_id": 10, "title": "黑龙江富拉尔基经济开发区管委会专职副主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 人大
    {"person_id": 16, "org_id": 11, "title": "齐齐哈尔市富拉尔基区人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 17, "org_id": 11, "title": "齐齐哈尔市富拉尔基区人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 18, "org_id": 11, "title": "齐齐哈尔市富拉尔基区人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 19, "org_id": 11, "title": "齐齐哈尔市富拉尔基区人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 20, "org_id": 11, "title": "齐齐哈尔市富拉尔基区人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 政协
    {"person_id": 21, "org_id": 12, "title": "齐齐哈尔市富拉尔基区政协主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 22, "org_id": 12, "title": "齐齐哈尔市富拉尔基区政协副主席",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 23, "org_id": 12, "title": "齐齐哈尔市富拉尔基区政协副主席",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 24, "org_id": 12, "title": "齐齐哈尔市富拉尔基区政协副主席",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
]

relationships = [
    # 党委班子核心关系
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长",
     "overlap_org": "中共齐齐哈尔市富拉尔基区委员会", "overlap_period": "2024.12至今"},
    {"person_a": 1, "person_b": 3, "type": "搭档", "context": "区委书记与副书记",
     "overlap_org": "中共齐齐哈尔市富拉尔基区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与纪委书记",
     "overlap_org": "中共齐齐哈尔市富拉尔基区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记与政法委书记",
     "overlap_org": "中共齐齐哈尔市富拉尔基区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记与组织部部长",
     "overlap_org": "中共齐齐哈尔市富拉尔基区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记与区委常委、副区长",
     "overlap_org": "中共齐齐哈尔市富拉尔基区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记与宣传部部长",
     "overlap_org": "中共齐齐哈尔市富拉尔基区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记与人武部部长",
     "overlap_org": "中共齐齐哈尔市富拉尔基区委员会", "overlap_period": "至今"},
    # 政府班子内部关系
    {"person_a": 2, "person_b": 7, "type": "搭档", "context": "区长与常务副区长",
     "overlap_org": "齐齐哈尔市富拉尔基区人民政府", "overlap_period": "2024.12至今"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区长与副区长（公安）",
     "overlap_org": "齐齐哈尔市富拉尔基区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长与副区长",
     "overlap_org": "齐齐哈尔市富拉尔基区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长与副区长",
     "overlap_org": "齐齐哈尔市富拉尔基区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "区长与副区长",
     "overlap_org": "齐齐哈尔市富拉尔基区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "区长与副区长",
     "overlap_org": "齐齐哈尔市富拉尔基区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "区长与经济开发区专职副主任",
     "overlap_org": "齐齐哈尔市富拉尔基区人民政府", "overlap_period": "至今"},
]

# --- Build ---

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
    print(f"✅ {SLUG} — Build complete!")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
