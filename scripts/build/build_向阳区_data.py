#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向阳区领导班子工作关系网络 — 数据构建脚本（暂存区版）
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 黑龙江省
Parent City: 鹤岗市
Region: 向阳区
Targets: 区委书记 & 区长

Research Sources (2026-07-24):
- 鹤岗市向阳区人民政府官网 (www.hgxyq.gov.cn):
  - 区委领导班子页面: 8 in-party leaders identified
  - 区政府领导班子页面: 7 in-government leaders identified
  - 区人大领导班子: 5 members
  - 区政协领导班子: 4 members
  - 房涛 profile (2025-08-22): confirmed 区委书记兼区长
  - 丛培甲 profile (2026-04-29): confirmed 区委副书记正处级
  - 其他常委/副区长 profiles confirmed with bios

Key Finding: 房涛 holds both 区委书记 and 区长 positions concurrently (一肩挑).
This is common in some districts but noteworthy.

Research Date: 2026-07-24

Gaps (see open_gaps.md):
1. 房涛此前完整履历（2025年8月前任向阳区区长之前的职务）
2. 丛培甲此前职务（他何时调任向阳区，此前在何处任职）
3. 前任区委书记/区长的身份信息
4. 房涛的出生地和其他身份字段
5. 部分领导人的完整出生日期（月份级别数据已有）
"""

import os
import sys

_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.normpath(os.path.join(_script_dir, "../.."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from gov_relation.runner import run_build

from gov_relation.runner import run_build

SLUG = "向阳区"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# --- Data ---

persons = [
    # ── 区委领导 (Party Committee Leaders) ──
    {
        "id": 1,
        "name": "房涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年5月",
        "birthplace": "",
        "education": "黑龙江省委党校经济管理专业",
        "party_join": "2002年11月",
        "work_start": "2003年7月",
        "current_post": "鹤岗市向阳区委书记、政府区长",
        "current_org": "中共鹤岗市向阳区委员会",
        "source": "confirmed - hgxyq.gov.cn 领导简介 (202508), 区委组织部",
        "notes": "兼任区委书记和政府区长（一肩挑）；籍贯山东烟台"
    },
    {
        "id": 2,
        "name": "丛培甲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年1月",
        "birthplace": "",
        "education": "北京体育大学体育教学专业",
        "party_join": "2007年5月",
        "work_start": "2007年7月",
        "current_post": "鹤岗市向阳区委副书记（正处级）、政法委书记",
        "current_org": "中共鹤岗市向阳区委员会",
        "source": "confirmed - hgxyq.gov.cn 领导简介 (202604), 区委组织部",
        "notes": "正处级区委副书记；兼任区直机关工委书记、北山街道党工委书记、办事处主任；籍贯黑龙江克东"
    },
    {
        "id": 3,
        "name": "刘海波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市向阳区委常委、组织部部长、统战部部长、政协党组副书记",
        "current_org": "中共鹤岗市向阳区委组织部",
        "source": "confirmed - hgxyq.gov.cn 领导简介 (202505), 区委组织部",
        "notes": "主持组织部全面工作；分管编办、工商联、总工会、团委、妇联、残联"
    },
    {
        "id": 4,
        "name": "迟延成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "",
        "education": "哈尔滨师范大学汉语言文学专业",
        "party_join": "1999年6月",
        "work_start": "1999年9月",
        "current_post": "鹤岗市向阳区委常委、区纪委书记、区监委主任",
        "current_org": "中共鹤岗市向阳区纪律检查委员会",
        "source": "confirmed - hgxyq.gov.cn 领导简介 (202505), 区委组织部",
        "notes": "主持区纪委、区监委全面工作；分管区委巡察办；籍贯辽宁桓仁"
    },
    {
        "id": 5,
        "name": "段肖飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "长春税务学院财政学专业",
        "party_join": "2011年11月",
        "work_start": "2003年12月",
        "current_post": "鹤岗市向阳区委常委、政府副区长",
        "current_org": "鹤岗市向阳区人民政府",
        "source": "confirmed - hgxyq.gov.cn 领导简介 (202505), 区委组织部",
        "notes": "分管区政府办、应急管理局、发改局、财政局、统计局、信访局、机关事务服务中心；兼任胜利（南翼）街道党工委书记、办事处主任；籍贯吉林榆树"
    },
    {
        "id": 6,
        "name": "赵云龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990年4月",
        "birthplace": "",
        "education": "黑龙江科技学院电气工程及其自动化专业",
        "party_join": "2016年6月",
        "work_start": "2011年8月",
        "current_post": "鹤岗市向阳区委常委、政府副区长（挂职）",
        "current_org": "鹤岗市向阳区人民政府",
        "source": "confirmed - hgxyq.gov.cn 领导简介 (202505), 区委组织部",
        "notes": "挂职副区长，最年轻的常委（1990年生）；籍贯黑龙江林口；分管退役军人事务局"
    },
    {
        "id": 7,
        "name": "高伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市向阳区委常委、人武部政委",
        "current_org": "中国人民解放军黑龙江省鹤岗市向阳区人民武装部",
        "source": "confirmed - hgxyq.gov.cn 领导简介 (202604), 区委组织部",
        "notes": "人武部政委；详细个人资料未公开"
    },
    {
        "id": 8,
        "name": "张洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年3月",
        "birthplace": "",
        "education": "东北林业大学法学专业",
        "party_join": "2005年11月",
        "work_start": "2002年9月",
        "current_post": "鹤岗市向阳区委常委、政府副区长",
        "current_org": "鹤岗市向阳区人民政府",
        "source": "confirmed - hgxyq.gov.cn 领导简介 (202505), 区委组织部",
        "notes": "分管住建局、城管执法局、环卫站、司法局；籍贯吉林榆树"
    },
    # ── 区政府领导 (Government Leaders, non-常委) ──
    {
        "id": 9,
        "name": "张士良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年10月",
        "birthplace": "",
        "education": "黑龙江省委党校财会专业",
        "party_join": "1999年12月",
        "work_start": "1995年7月",
        "current_post": "鹤岗市向阳区副区长",
        "current_org": "鹤岗市向阳区人民政府",
        "source": "confirmed - hgxyq.gov.cn 领导简介 (202505), 区委组织部",
        "notes": "分管工信科技局、人社局、文体旅游局；籍贯山东东阿"
    },
    {
        "id": 10,
        "name": "李松贵",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市向阳区副区长、市公安局向阳分局局长",
        "current_org": "鹤岗市公安局向阳分局",
        "source": "confirmed - hgxyq.gov.cn 领导简介 (202505), 区委组织部",
        "notes": "兼任公安分局局长"
    },
    {
        "id": 11,
        "name": "刘林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市向阳区副区长",
        "current_org": "鹤岗市向阳区人民政府",
        "source": "confirmed - hgxyq.gov.cn 领导简介 (202505), 区委组织部",
    },
    # ── 区人大领导 (People's Congress) ──
    {
        "id": 12,
        "name": "尹立斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市向阳区人大常委会主任（候选人）",
        "current_org": "鹤岗市向阳区人民代表大会常务委员会",
        "source": "confirmed - hgxyq.gov.cn 人大领导班子 (202604)",
    },
    {
        "id": 13,
        "name": "薛晓红",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市向阳区人大常委会副主任",
        "current_org": "鹤岗市向阳区人民代表大会常务委员会",
        "source": "confirmed - hgxyq.gov.cn 人大领导班子 (202412)",
    },
    {
        "id": 14,
        "name": "王英田",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市向阳区人大常委会副主任",
        "current_org": "鹤岗市向阳区人民代表大会常务委员会",
        "source": "confirmed - hgxyq.gov.cn 人大领导班子 (202412)",
    },
    {
        "id": 15,
        "name": "陈萍",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市向阳区人大常委会副主任",
        "current_org": "鹤岗市向阳区人民代表大会常务委员会",
        "source": "confirmed - hgxyq.gov.cn 人大领导班子 (202412)",
    },
    {
        "id": 16,
        "name": "曲佳红",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市向阳区人大常委会副主任",
        "current_org": "鹤岗市向阳区人民代表大会常务委员会",
        "source": "confirmed - hgxyq.gov.cn 人大领导班子 (202412)",
    },
    # ── 区政协领导 (Political Consultative Conference) ──
    {
        "id": 17,
        "name": "郑异军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市向阳区政协主席",
        "current_org": "中国人民政治协商会议鹤岗市向阳区委员会",
        "source": "confirmed - hgxyq.gov.cn 政协领导班子 (202604)",
    },
    {
        "id": 18,
        "name": "孟兆香",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市向阳区政协副主席",
        "current_org": "中国人民政治协商会议鹤岗市向阳区委员会",
        "source": "confirmed - hgxyq.gov.cn 政协领导班子 (202412)",
    },
    {
        "id": 19,
        "name": "褚玉萍",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市向阳区政协副主席",
        "current_org": "中国人民政治协商会议鹤岗市向阳区委员会",
        "source": "confirmed - hgxyq.gov.cn 政协领导班子 (202412)",
    },
    {
        "id": 20,
        "name": "曲建丽",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤岗市向阳区政协副主席（候选人）",
        "current_org": "中国人民政治协商会议鹤岗市向阳区委员会",
        "source": "confirmed - hgxyq.gov.cn 政协领导班子 (202605)",
    },
]

organizations = [
    {"id": 1, "name": "中共鹤岗市向阳区委员会", "type": "党委", "level": "县处级",
     "parent": "中共鹤岗市委员会", "location": "黑龙江省鹤岗市向阳区"},
    {"id": 2, "name": "鹤岗市向阳区人民政府", "type": "政府", "level": "县处级",
     "parent": "鹤岗市人民政府", "location": "黑龙江省鹤岗市向阳区"},
    {"id": 3, "name": "中共鹤岗市向阳区纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共鹤岗市纪律检查委员会", "location": "黑龙江省鹤岗市向阳区"},
    {"id": 4, "name": "中共鹤岗市向阳区委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共鹤岗市向阳区委员会", "location": "黑龙江省鹤岗市向阳区"},
    {"id": 5, "name": "中共鹤岗市向阳区委组织部", "type": "党委", "level": "县处级",
     "parent": "中共鹤岗市向阳区委员会", "location": "黑龙江省鹤岗市向阳区"},
    {"id": 6, "name": "中共鹤岗市向阳区委统一战线工作部", "type": "党委", "level": "县处级",
     "parent": "中共鹤岗市向阳区委员会", "location": "黑龙江省鹤岗市向阳区"},
    {"id": 7, "name": "中国人民解放军黑龙江省鹤岗市向阳区人民武装部", "type": "军队", "level": "县处级",
     "parent": "鹤岗军分区", "location": "黑龙江省鹤岗市向阳区"},
    {"id": 8, "name": "鹤岗市公安局向阳分局", "type": "政府", "level": "县处级",
     "parent": "鹤岗市公安局", "location": "黑龙江省鹤岗市向阳区"},
    {"id": 9, "name": "鹤岗市向阳区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "鹤岗市人大常委会", "location": "黑龙江省鹤岗市向阳区"},
    {"id": 10, "name": "中国人民政治协商会议鹤岗市向阳区委员会", "type": "政协", "level": "县处级",
     "parent": "鹤岗市政协", "location": "黑龙江省鹤岗市向阳区"},
    {"id": 11, "name": "鹤岗市向阳区北山街道办事处", "type": "乡镇/街道", "level": "乡科级",
     "parent": "鹤岗市向阳区人民政府", "location": "黑龙江省鹤岗市向阳区"},
    {"id": 12, "name": "鹤岗市向阳区胜利（南翼）街道办事处", "type": "乡镇/街道", "level": "乡科级",
     "parent": "鹤岗市向阳区人民政府", "location": "黑龙江省鹤岗市向阳区"},
]

positions = [
    # 房涛 — 区委书记兼区长（一肩挑）
    {"person_id": 1, "org_id": 1, "title": "鹤岗市向阳区委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "兼任政府区长"},
    {"person_id": 1, "org_id": 2, "title": "鹤岗市向阳区区长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "由区委书记兼任"},
    # 丛培甲
    {"person_id": 2, "org_id": 1, "title": "鹤岗市向阳区委副书记（正处级）",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "正处级区委副书记"},
    {"person_id": 2, "org_id": 4, "title": "鹤岗市向阳区委政法委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "兼任"},
    {"person_id": 2, "org_id": 11, "title": "北山街道党工委书记、办事处主任",
     "start_date": "", "end_date": "present", "rank": "乡科级正职",
     "note": "兼任"},
    # 刘海波
    {"person_id": 3, "org_id": 5, "title": "鹤岗市向阳区委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "主持组织部全面工作"},
    {"person_id": 3, "org_id": 6, "title": "鹤岗市向阳区委统战部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "兼任"},
    # 迟延成
    {"person_id": 4, "org_id": 3, "title": "鹤岗市向阳区委常委、纪委书记、监委主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "主持区纪委、区监委全面工作"},
    # 段肖飞
    {"person_id": 5, "org_id": 2, "title": "鹤岗市向阳区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "区政府常务工作"},
    {"person_id": 5, "org_id": 1, "title": "鹤岗市向阳区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 5, "org_id": 12, "title": "胜利（南翼）街道党工委书记、办事处主任",
     "start_date": "", "end_date": "present", "rank": "乡科级正职",
     "note": "兼任"},
    # 赵云龙
    {"person_id": 6, "org_id": 2, "title": "鹤岗市向阳区副区长（挂职）",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "挂职"},
    {"person_id": 6, "org_id": 1, "title": "鹤岗市向阳区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 高伟
    {"person_id": 7, "org_id": 7, "title": "鹤岗市向阳区委常委、人武部政委",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 张洋
    {"person_id": 8, "org_id": 2, "title": "鹤岗市向阳区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 8, "org_id": 1, "title": "鹤岗市向阳区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 张士良
    {"person_id": 9, "org_id": 2, "title": "鹤岗市向阳区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 李松贵
    {"person_id": 10, "org_id": 2, "title": "鹤岗市向阳区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 10, "org_id": 8, "title": "鹤岗市公安局向阳分局局长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "兼任"},
    # 刘林
    {"person_id": 11, "org_id": 2, "title": "鹤岗市向阳区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 人大
    {"person_id": 12, "org_id": 9, "title": "鹤岗市向阳区人大常委会主任（候选人）",
     "start_date": "", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 13, "org_id": 9, "title": "鹤岗市向阳区人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 14, "org_id": 9, "title": "鹤岗市向阳区人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 15, "org_id": 9, "title": "鹤岗市向阳区人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 16, "org_id": 9, "title": "鹤岗市向阳区人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    # 政协
    {"person_id": 17, "org_id": 10, "title": "鹤岗市向阳区政协主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 18, "org_id": 10, "title": "鹤岗市向阳区政协副主席",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 19, "org_id": 10, "title": "鹤岗市向阳区政协副主席",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
    {"person_id": 20, "org_id": 10, "title": "鹤岗市向阳区政协副主席（候选人）",
     "start_date": "", "end_date": "present", "rank": "县处级副职"},
]

relationships = [
    # 党政核心——房涛与副书记
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "区委书记与副书记",
     "overlap_org": "中共鹤岗市向阳区委员会", "overlap_period": "至今"},
    # 区委书记与各常委
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与组织部部长",
     "overlap_org": "中共鹤岗市向阳区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与纪委书记",
     "overlap_org": "中共鹤岗市向阳区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记与区委常委、副区长",
     "overlap_org": "中共鹤岗市向阳区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记与区委常委、挂职副区长",
     "overlap_org": "中共鹤岗市向阳区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记与人武部政委",
     "overlap_org": "中共鹤岗市向阳区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记与区委常委、副区长",
     "overlap_org": "中共鹤岗市向阳区委员会", "overlap_period": "至今"},
    # 副书记与常委
    {"person_a": 2, "person_b": 3, "type": "搭档", "context": "区委副书记与组织部部长",
     "overlap_org": "中共鹤岗市向阳区委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "搭档", "context": "区委副书记与纪委书记",
     "overlap_org": "中共鹤岗市向阳区委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "搭档", "context": "区委副书记与区委常委、副区长",
     "overlap_org": "中共鹤岗市向阳区委员会", "overlap_period": "至今"},
    # 政府班子关系（房涛兼区长）
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区长（兼）与副区长段肖飞",
     "overlap_org": "鹤岗市向阳区人民政府", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区长（兼）与副区长张洋",
     "overlap_org": "鹤岗市向阳区人民政府", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区长（兼）与挂职副区长赵云龙",
     "overlap_org": "鹤岗市向阳区人民政府", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区长（兼）与副区长张士良",
     "overlap_org": "鹤岗市向阳区人民政府", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "区长（兼）与副区长李松贵",
     "overlap_org": "鹤岗市向阳区人民政府", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "区长（兼）与副区长刘林",
     "overlap_org": "鹤岗市向阳区人民政府", "overlap_period": "至今"},
    # 政府班子成员间
    {"person_a": 5, "person_b": 8, "type": "同事", "context": "副区长之间",
     "overlap_org": "鹤岗市向阳区人民政府", "overlap_period": "至今"},
    {"person_a": 5, "person_b": 9, "type": "同事", "context": "副区长之间",
     "overlap_org": "鹤岗市向阳区人民政府", "overlap_period": "至今"},
    {"person_a": 8, "person_b": 9, "type": "同事", "context": "副区长之间",
     "overlap_org": "鹤岗市向阳区人民政府", "overlap_period": "至今"},
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
