#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
曲松县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 西藏自治区
Parent City: 山南市
Region: 曲松县
Targets: 县委书记 & 县长

Research Sources:
- 曲松县人民政府官网 (www.qusong.gov.cn) — 领导之窗及新闻中心
  - 边巴次仁县长页面: http://www.qusong.gov.cn/zwgk/ldzc/202509/t20250912_155307.html
  - 次仁朗杰副县长页面: http://www.qusong.gov.cn/zwgk/ldzc/202601/t20260107_162632.html
  - 蒋建生副县长页面: http://www.qusong.gov.cn/zwgk/ldzc/202601/t20260107_162629.html
- 司刚存委书记身份确认自多处官方新闻:
  - 司刚存专题调研卫生健康领域工作 (2026-07-29): http://www.qusong.gov.cn/xwzx/qsyw/202607/t20260729_174066.html
  - 司刚存主持召开曲松县委2026年上半年"一把手"监督谈话会 (2026-07-24): http://www.qusong.gov.cn/xwzx/qsyw/202607/t20260724_173909.html
  - 司刚存在县宣传文化系统调研 (2026-07-07): http://www.qusong.gov.cn/xwzx/tpxw/202607/t20260707_172830.html
  - 司刚存深入一线调研全国文明城市创建 (2026-04-07): http://www.qusong.gov.cn/xwzx/tpxw/202604/t20260407_166828.html
- 曲松县第十五届人民代表大会公告 (2026-07-07): http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html
- 曲松县人大常委会任免名单 (2026-05-21): http://www.qusong.gov.cn/zwgk/xxgkml/202605/t20260527_170228.html
- 曲松县人大常委会任免职名单 (2026-01-06): http://www.qusong.gov.cn/zwgk/xxgkml/202601/t20260106_162495.html

Research Date: 2026-08-03

Gaps:
- 县委书记司刚存的出生年月、籍贯、学历、完整履历暂缺（未在领导之窗页面出现）
- 县政协主席姓名暂缺
- 部分县委常委（常务副县长等）的履历和分管信息暂缺
- 前任县委书记信息暂缺（未找到公开资料）
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "曲松县"

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
        "name": "司刚存",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县委书记",
        "current_org": "中共曲松县委员会",
        "source": "曲松县人民政府官网: 县委书记司刚存多次出现在官方新闻中。来源: http://www.qusong.gov.cn/xwzx/qsyw/202607/t20260729_174066.html — '县委书记司刚存专题调研卫生健康领域工作'"
    },
    {
        "id": 2,
        "name": "边巴次仁",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1983年7月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "曲松县委副书记、县长",
        "current_org": "曲松县人民政府",
        "source": "https://www.qusong.gov.cn/zwgk/ldzc/202509/t20250912_155307.html — 边巴次仁，男，藏族，1983年7月出生，中共党员，在职研究生学历。现任西藏自治区曲松县委副书记、县政府县长。"
    },
    # ════════════════════════════════════════
    # Government Deputy Leaders (县人代会选出)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "王平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县副县长",
        "current_org": "曲松县人民政府",
        "source": "http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html — 曲松县人民代表大会公告：王平为副县长"
    },
    {
        "id": 4,
        "name": "边巴",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县副县长",
        "current_org": "曲松县人民政府",
        "source": "http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html — 曲松县人民代表大会公告：边巴为副县长"
    },
    {
        "id": 5,
        "name": "次仁群培",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县副县长",
        "current_org": "曲松县人民政府",
        "source": "http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html — 曲松县人民代表大会公告"
    },
    {
        "id": 6,
        "name": "次仁朗杰",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1986年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "曲松县副县长",
        "current_org": "曲松县人民政府",
        "source": "https://www.qusong.gov.cn/zwgk/ldzc/202601/t20260107_162632.html — 次仁朗杰，男，藏族，1986年10月出生，中共党员，大学学历，现任西藏自治区曲松县副县长。负责农业农村、水利、科技、乡村振兴方面工作。"
    },
    {
        "id": 7,
        "name": "杨东林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县副县长",
        "current_org": "曲松县人民政府",
        "source": "http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html — 曲松县人民代表大会公告"
    },
    {
        "id": 8,
        "name": "苗康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县副县长",
        "current_org": "曲松县人民政府",
        "source": "http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html — 曲松县人民代表大会公告"
    },
    {
        "id": 9,
        "name": "拓永红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县副县长",
        "current_org": "曲松县人民政府",
        "source": "http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html — 曲松县人民代表大会公告"
    },
    {
        "id": 10,
        "name": "蒋建生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年11月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "曲松县副县长",
        "current_org": "曲松县人民政府",
        "source": "https://www.qusong.gov.cn/zwgk/ldzc/202601/t20260107_162629.html — 蒋建生，男，汉族，1981年11月出生，中共党员，在职大学学历，现任西藏自治区曲松县副县长。负责公安、自然资源、林业草原、矿业开发方面工作。"
    },
    # ════════════════════════════════════════
    # County Party Committee Members
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "白玛拉吉",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县委常委、宣传部部长",
        "current_org": "中共曲松县委员会",
        "source": "http://www.qusong.gov.cn/xwzx/tpxw/202604/t20260407_166828.html — '县委书记司刚存带队...县委常委、宣传部部长白玛拉吉...参加调研'"
    },
    {
        "id": 12,
        "name": "仝义鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县委常委、县委办公室主任",
        "current_org": "中共曲松县委员会",
        "source": "http://www.qusong.gov.cn/xwzx/qsyw/202607/t20260729_174066.html — '县委常委、县委办主任仝义鹏...一同调研并参加座谈'"
    },
    {
        "id": 13,
        "name": "吴配伟",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县委常委、纪委书记、监委主任",
        "current_org": "中共曲松县纪律检查委员会",
        "source": "http://www.qusong.gov.cn/xwzx/qsyw/202607/t20260724_173909.html — '县委常委、纪委书记、监委主任吴厚伟结合日常监督...点评'；以及 http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html — '选举吴配伟（侗族）为曲松县监察委员会主任'"
    },
    {
        "id": 14,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县委常委、副县长",
        "current_org": "曲松县人民政府",
        "source": "http://www.qusong.gov.cn/xwzx/qsyw/202607/t20260729_174066.html — '县委常委、副县长刘涛...一同调研并参加座谈'"
    },
    # ════════════════════════════════════════
    # County People's Congress
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "白玛次仁",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县人大常委会主任",
        "current_org": "曲松县人民代表大会常务委员会",
        "source": "http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html — '选举产生曲松县第十五届人民代表大会常务委员会主任：白玛次仁'"
    },
    {
        "id": 16,
        "name": "小边巴",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县人大常委会副主任",
        "current_org": "曲松县人民代表大会常务委员会",
        "source": "http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html"
    },
    {
        "id": 17,
        "name": "牛文现",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县人大常委会副主任",
        "current_org": "曲松县人民代表大会常务委员会",
        "source": "http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html"
    },
    {
        "id": 18,
        "name": "王慧",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县人大常委会副主任",
        "current_org": "曲松县人民代表大会常务委员会",
        "source": "http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html"
    },
    {
        "id": 19,
        "name": "边巴次仁（人大）",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县人大常委会副主任",
        "current_org": "曲松县人民代表大会常务委员会",
        "source": "http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html"
    },
    # ════════════════════════════════════════
    # Justice & Procuratorate
    # ════════════════════════════════════════
    {
        "id": 20,
        "name": "仁青白珍",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县人民法院院长",
        "current_org": "曲松县人民法院",
        "source": "http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html — '选举仁青白珍（女）为曲松县人民法院院长'"
    },
    {
        "id": 21,
        "name": "冯勇卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲松县人民检察院检察长",
        "current_org": "曲松县人民检察院",
        "source": "http://www.qusong.gov.cn/zwgk/xxgkml/202607/t20260709_173033.html — '选举冯勇卫（汉族）为曲松县人民检察院检察长'"
    },
    # ════════════════════════════════════════
    # Cross-county connections
    # ════════════════════════════════════════
    {
        "id": 22,
        "name": "次仁达瓦",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1981年5月",
        "birthplace": "西藏曲松",
        "education": "在职研究生学历",
        "party_join": "2006年6月",
        "work_start": "",
        "current_post": "桑日县委副书记、县长",
        "current_org": "桑日县人民政府",
        "source": "https://www.sangri.gov.cn/zwgk/ldzc/202506/t20250626_151958.html — 次仁达瓦，男，藏族，1981年5月出生，西藏曲松人。现任桑日县委副书记、县长。"
    },
]

organizations = [
    {"id": 1, "name": "中共曲松县委员会", "type": "党委", "level": "县处级", "parent": "中共山南市委员会", "location": "西藏山南曲松"},
    {"id": 2, "name": "曲松县人民政府", "type": "政府", "level": "县处级", "parent": "山南市人民政府", "location": "西藏山南曲松"},
    {"id": 3, "name": "曲松县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "山南市人民代表大会常务委员会", "location": "西藏山南曲松"},
    {"id": 4, "name": "政协曲松县委员会", "type": "政协", "level": "县处级", "parent": "政协山南市委员会", "location": "西藏山南曲松"},
    {"id": 5, "name": "中共曲松县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共曲松县委员会", "location": "西藏山南曲松"},
    {"id": 6, "name": "曲松县人民法院", "type": "司法机关", "level": "县处级", "parent": "", "location": "西藏山南曲松"},
    {"id": 7, "name": "曲松县人民检察院", "type": "司法机关", "level": "县处级", "parent": "", "location": "西藏山南曲松"},
    {"id": 8, "name": "桑日县人民政府", "type": "政府", "level": "县处级", "parent": "山南市人民政府", "location": "西藏山南桑日"},
]

positions = [
    # ── Party Secretary site here
    {"id": 1, "person_id": 1, "org_id": 1, "title": "曲松县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    # ── County Magistrate
    {"id": 2, "person_id": 2, "org_id": 2, "title": "曲松县委副书记、县长", "start": "", "end": "", "rank": "县处级正职", "note": "主持县人民政府全面工作"},
    # 边巴次仁 previous roles (Zhanang County)
    {"id": 31, "person_id": 2, "org_id": 1, "title": "扎囊县监察局副局长", "start": "", "end": "", "rank": "", "note": "早期职务"},
    {"id": 32, "person_id": 2, "org_id": 1, "title": "扎囊县监察局局长", "start": "", "end": "", "rank": "", "note": ""},
    {"id": 33, "person_id": 2, "org_id": 1, "title": "扎囊县纪委副书记、监察局局长", "start": "", "end": "", "rank": "", "note": ""},
    {"id": 34, "person_id": 2, "org_id": 1, "title": "扎囊县扎其乡党委书记", "start": "", "end": "", "rank": "", "note": ""},
    {"id": 35, "person_id": 2, "org_id": 1, "title": "扎囊县政协副主席", "start": "", "end": "", "rank": "", "note": ""},

    # ── Deputy County Magistrates
    {"id": 3, "person_id": 3, "org_id": 2, "title": "曲松县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 4, "person_id": 4, "org_id": 2, "title": "曲松县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 5, "person_id": 5, "org_id": 2, "title": "曲松县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 6, "person_id": 6, "org_id": 2, "title": "曲松县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任，分管农业农村、水利、乡村振兴"},
    {"id": 7, "person_id": 7, "org_id": 2, "title": "曲松县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 8, "person_id": 8, "org_id": 2, "title": "曲松县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 9, "person_id": 9, "org_id": 2, "title": "曲松县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 10, "person_id": 10, "org_id": 2, "title": "曲松县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任，负责公安、自然资源、林业草原"},
    # 蒋建生前职务
    {"id": 36, "person_id": 10, "org_id": 1, "title": "浪卡子县政府办党组书记、主任", "start": "", "end": "", "rank": "", "note": "调任曲松前职务"},

    # ── Party Committee Members
    {"id": 11, "person_id": 11, "org_id": 1, "title": "曲松县委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 12, "person_id": 12, "org_id": 1, "title": "曲松县委常委、县委办公室主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 13, "person_id": 13, "org_id": 5, "title": "曲松县委常委、纪委书记、监委主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 14, "person_id": 14, "org_id": 1, "title": "曲松县委常委、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── NPC
    {"id": 15, "person_id": 15, "org_id": 3, "title": "曲松县人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 16, "person_id": 16, "org_id": 3, "title": "曲松县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 17, "person_id": 17, "org_id": 3, "title": "曲松县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 18, "person_id": 18, "org_id": 3, "title": "曲松县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 19, "person_id": 19, "org_id": 3, "title": "曲松县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Court & Procuratorate
    {"id": 20, "person_id": 20, "org_id": 6, "title": "曲松县人民法院院长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 21, "person_id": 21, "org_id": 7, "title": "曲松县人民检察院检察长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Cross-county
    {"id": 30, "person_id": 22, "org_id": 8, "title": "桑日县委副书记、县长", "start": "", "end": "", "rank": "县处级正职", "note": "曲松籍，在桑日县任职"},
]

relationships = [
    # ── Party Secretary + County Magistrate
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "司刚存（县委书记）与边巴次仁（县长）组成党政班子",
     "overlap_org": "曲松县", "overlap_period": ""},

    # ── Party Secretary + Party Committee Members
    {"id": 2, "person_a_id": 1, "person_b_id": 11, "type": "上下级",
     "context": "司刚存（书记）与白玛拉吉（宣传部长）",
     "overlap_org": "中共曲松县委员会", "overlap_period": ""},
    {"id": 3, "person_a_id": 1, "person_b_id": 12, "type": "上下级",
     "context": "司刚存（书记）与仝义鹏（县委办主任）",
     "overlap_org": "中共曲松县委员会", "overlap_period": ""},
    {"id": 4, "person_a_id": 1, "person_b_id": 13, "type": "上下级",
     "context": "司刚存（书记）与吴配伟（纪委书记）",
     "overlap_org": "中共曲松县委员会", "overlap_period": ""},
    {"id": 5, "person_a_id": 1, "person_b_id": 14, "type": "上下级",
     "context": "司刚存（书记）与刘涛（常委、副县长）",
     "overlap_org": "中共曲松县委员会", "overlap_period": ""},

    # ── County Magistrate + Deputy County Magistrates
    {"id": 6, "person_a_id": 2, "person_b_id": 3, "type": "上下级",
     "context": "边巴次仁（县长）与王平（副县长）",
     "overlap_org": "曲松县人民政府", "overlap_period": ""},
    {"id": 7, "person_a_id": 2, "person_b_id": 4, "type": "上下级",
     "context": "边巴次仁（县长）与边巴（副县长）",
     "overlap_org": "曲松县人民政府", "overlap_period": ""},
    {"id": 8, "person_a_id": 2, "person_b_id": 5, "type": "上下级",
     "context": "边巴次仁（县长）与次仁群培（副县长）",
     "overlap_org": "曲松县人民政府", "overlap_period": ""},
    {"id": 9, "person_a_id": 2, "person_b_id": 6, "type": "上下级",
     "context": "边巴次仁（县长）与次仁朗杰（副县长）",
     "overlap_org": "曲松县人民政府", "overlap_period": ""},
    {"id": 10, "person_a_id": 2, "person_b_id": 7, "type": "上下级",
     "context": "边巴次仁（县长）与杨东林（副县长）",
     "overlap_org": "曲松县人民政府", "overlap_period": ""},
    {"id": 11, "person_a_id": 2, "person_b_id": 8, "type": "上下级",
     "context": "边巴次仁（县长）与苗康（副县长）",
     "overlap_org": "曲松县人民政府", "overlap_period": ""},
    {"id": 12, "person_a_id": 2, "person_b_id": 9, "type": "上下级",
     "context": "边巴次仁（县长）与拓永红（副县长）",
     "overlap_org": "曲松县人民政府", "overlap_period": ""},
    {"id": 13, "person_a_id": 2, "person_b_id": 10, "type": "上下级",
     "context": "边巴次仁（县长）与蒋建生（副县长）",
     "overlap_org": "曲松县人民政府", "overlap_period": ""},

    # ── Party Committee + NPC + other organs
    {"id": 14, "person_a_id": 15, "person_b_id": 16, "type": "同僚",
     "context": "白玛次仁（主任）与小边巴（副主任）",
     "overlap_org": "曲松县人民代表大会常务委员会", "overlap_period": ""},
    {"id": 15, "person_a_id": 15, "person_b_id": 17, "type": "同僚",
     "context": "白玛次仁与牛文现",
     "overlap_org": "曲松县人民代表大会常务委员会", "overlap_period": ""},
    {"id": 16, "person_a_id": 15, "person_b_id": 18, "type": "同僚",
     "context": "白玛次仁与王慧",
     "overlap_org": "曲松县人民代表大会常务委员会", "overlap_period": ""},

    # ── Cross-county: Qusong native connection
    {"id": 17, "person_a_id": 2, "person_b_id": 22, "type": "同乡",
     "context": "边巴次仁（曲松县长）与次仁达瓦（桑日县长）均为曲松籍/边巴次仁为扎囊籍，次仁达瓦为曲松籍",
     "overlap_org": "", "overlap_period": ""},
    {"id": 18, "person_a_id": 6, "person_b_id": 22, "type": "同乡",
     "context": "次仁朗杰（曲松副县长）与次仁达瓦（桑日县长），次仁朗杰曾任桑日县政府办公室副主任",
     "overlap_org": "桑日县", "overlap_period": ""},
]


# ── BUILD SQLite DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT,
    ethnicity TEXT,
    birth TEXT,
    birthplace TEXT,
    education TEXT,
    party_join TEXT,
    work_start TEXT,
    current_post TEXT,
    current_org TEXT,
    source TEXT
);

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary stats
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>曲松县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    # Color by role
    if p["id"] == 1:
        color = '#E03C31'  # red: Party Secretary
        size = 20.0
    elif p["id"] == 2:
        color = '#2980B9'  # blue: government leader (county mayor)
        size = 20.0
    elif p["id"] == 15:
        color = '#5a7a9a'  # blue-grey: NPC
        size = 16.0
    elif p["id"] == 11:
        color = '#8E44AD'  # purple: propaganda
        size = 14.0
    elif p["id"] == 13:
        color = '#E67E22'  # orange: discipline
        size = 14.0
    elif p["id"] == 22:
        color = '#2980B9'  # blue: cross-county
        size = 14.0
    elif p["id"] in [12, 14]:
        color = '#7F8C8D'  # grey: party committee members
        size = 14.0
    else:
        color = '#95A5A6'  # light grey: others
        size = 12.0

    lines.append(f'      <node id="{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="education" value="{p["education"]}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"][:100]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="44" g="62" b="80"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{r["type"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="C" value="{r["type"]}"/>')
    lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")