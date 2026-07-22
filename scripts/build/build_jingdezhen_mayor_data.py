#!/usr/bin/env python3
"""
景德镇市市长（市长空缺）— 领导班子工作关系网络数据库 + GEXF 图谱构建脚本
调查日期: 2026-07-14
"""

import sqlite3
import os
import textwrap

# ── 数据定义 ─────────────────────────────────────────────────────────────

PERSONS = [
    # ── 1. 主要领导 ──
    {
        "id": "jdz_chen_kelong",
        "name": "陈克龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-12",
        "birthplace": "未公开",
        "education": "研究生/工学硕士",
        "party_join": "未公开",
        "work_start": "未公开",
        "current_post": "景德镇市委书记",
        "current_org": "中共景德镇市委员会",
        "source": "中国经济网(2026-04-27); district.ce.cn"
    },
    {
        "id": "jdz_xue_qiang",
        "name": "薛强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-03",
        "birthplace": "江西安远",
        "education": "省委党校研究生/工商管理硕士",
        "party_join": "1997-04",
        "work_start": "1997-07",
        "current_post": "景德镇市委常委、常务副市长、市政府党组副书记",
        "current_org": "景德镇市人民政府",
        "source": "澎湃新闻; jdz.gov.cn"
    },
    {
        "id": "jdz_hu_xuemei",
        "name": "胡雪梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1967-08",
        "birthplace": "未公开（推测江西籍）",
        "education": "未公开",
        "party_join": "未公开",
        "work_start": "未公开",
        "current_post": "（传闻：江西省广播电视局局长，待确认）",
        "current_org": "（待确认）",
        "source": "中国经济网(2024-09-03); 人民网"
    },
    {
        "id": "jdz_liu_feng",
        "name": "刘锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964-08",
        "birthplace": "湖南衡阳",
        "education": "上饶师范专科学校中文系",
        "party_join": "1985-12",
        "work_start": "1982-08",
        "current_post": "（2025年1月被免职）",
        "current_org": "（原江西省人大财经委副主任委员）",
        "source": "人民网江西频道(2021-03-22); Wikipedia 刘锋(1964年)"
    },
    {
        "id": "jdz_yan_ganhui",
        "name": "颜赣辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962-02",
        "birthplace": "江西崇仁",
        "education": "江西财经学院计划统计系工业统计专业",
        "party_join": "（2021年2月开除党籍）",
        "work_start": "1982-08",
        "current_post": "（2021年被判刑11年）",
        "current_org": "（原宜春市委书记）",
        "source": "Wikipedia 颜赣辉"
    },
    # ── 2. 副市长团队 ──
    {
        "id": "jdz_zou_yongsheng",
        "name": "邹永胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-12",
        "birthplace": "江西吉安",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1993-07",
        "current_post": "（原景德镇副市长兼公安局长，2026年初已升任省公安厅副厅长）",
        "current_org": "江西省公安厅",
        "source": "jdz.gov.cn; 江西省公安厅官网"
    },
    {
        "id": "jdz_wei_ji",
        "name": "魏冀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-11",
        "birthplace": "未公开",
        "education": "文学博士",
        "party_join": "中共党员",
        "work_start": "未公开",
        "current_post": "景德镇市副市长（挂职）、党组成员",
        "current_org": "景德镇市人民政府",
        "source": "jdz.gov.cn; 文旅部任职信息"
    },
    {
        "id": "jdz_jiang_minqiang",
        "name": "江民强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-09",
        "birthplace": "未公开",
        "education": "未公开",
        "party_join": "无党派",
        "work_start": "未公开",
        "current_post": "景德镇市副市长、市工商联主席",
        "current_org": "景德镇市人民政府",
        "source": "jdz.gov.cn"
    },
    {
        "id": "jdz_luo_wenjun",
        "name": "罗文军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-04",
        "birthplace": "未公开",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "未公开",
        "current_post": "景德镇市副市长、党组成员、高新区党工委书记",
        "current_org": "景德镇市人民政府",
        "source": "jdz.gov.cn"
    },
    {
        "id": "jdz_xu_hui",
        "name": "徐辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-03",
        "birthplace": "未公开",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "未公开",
        "current_post": "景德镇市副市长、党组成员",
        "current_org": "景德镇市人民政府",
        "source": "jdz.gov.cn"
    },
    {
        "id": "jdz_gao_xiaoyun",
        "name": "高晓云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-05",
        "birthplace": "未公开",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "未公开",
        "current_post": "景德镇市副市长、党组成员",
        "current_org": "景德镇市人民政府",
        "source": "jdz.gov.cn"
    },
    {
        "id": "jdz_huang_lian",
        "name": "黄练",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-12",
        "birthplace": "未公开",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "未公开",
        "current_post": "景德镇市副市长、党组成员、市公安局局长",
        "current_org": "景德镇市人民政府",
        "source": "jdz.gov.cn"
    },
    # ── 3. 其他机构领导 ──
    {
        "id": "jdz_huang_jianping",
        "name": "黄建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-05",
        "birthplace": "未公开",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "未公开",
        "current_post": "景德镇市政府秘书长、党组成员",
        "current_org": "景德镇市人民政府",
        "source": "jdz.gov.cn"
    },
    {
        "id": "jdz_yan_hua",
        "name": "鄢华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未公开",
        "birthplace": "未公开",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "未公开",
        "current_post": "景德镇市人大常委会主任",
        "current_org": "景德镇市人大常委会",
        "source": "中国经济网(2026-01-24); 鹰潭市纪委原书记调任"
    },
    {
        "id": "yingtan_yan_hua",  # same person, cross-city reference
        "name": "鄢华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未公开",
        "birthplace": "未公开",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "未公开",
        "current_post": "（原鹰潭市委常委、市纪委书记）",
        "current_org": "中共鹰潭市纪律检查委员会",
        "source": "district.ce.cn"
    },
    {
        "id": "jdz_zhong_zhiSheng",
        "name": "钟志生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-06",
        "birthplace": "江西分宜",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "未公开",
        "current_post": "（原景德镇市委书记→省直机关）",
        "current_org": "（已调任）",
        "source": "Wikipedia 景德镇市; 公开资料"
    },
]

ORGANIZATIONS = [
    {"id": "jdz_municipal_gov", "name": "景德镇市人民政府", "type": "地方政府", "level": "地级市", "parent": "江西省人民政府", "location": "江西省景德镇市"},
    {"id": "jdz_cpc_committee", "name": "中共景德镇市委员会", "type": "党委", "level": "地级市", "parent": "中共江西省委", "location": "江西省景德镇市"},
    {"id": "jdz_npc_standing", "name": "景德镇市人大常委会", "type": "人大", "level": "地级市", "parent": "江西省人大常委会", "location": "江西省景德镇市"},
    {"id": "miit_planning", "name": "工业和信息化部规划司", "type": "中央部委司局", "level": "正司级", "parent": "工业和信息化部", "location": "北京市"},
    {"id": "miit_equipment", "name": "工业和信息化部装备工业一司", "type": "中央部委司局", "level": "正司级", "parent": "工业和信息化部", "location": "北京市"},
    {"id": "miit_raw_materials", "name": "工业和信息化部原材料工业司", "type": "中央部委司局", "level": "正司级", "parent": "工业和信息化部", "location": "北京市"},
    {"id": "ganzhou_municipal", "name": "赣州市人民政府", "type": "地方政府", "level": "地级市", "parent": "江西省人民政府", "location": "江西省赣州市"},
    {"id": "quannan_cpc", "name": "中共全南县委", "type": "党委", "level": "县级", "parent": "中共赣州市委", "location": "江西省赣州市全南县"},
    {"id": "longnan_cpc", "name": "中共龙南县委", "type": "党委", "level": "县级", "parent": "中共赣州市委", "location": "江西省赣州市龙南市"},
    {"id": "fuzhou_municipal", "name": "抚州市人民政府", "type": "地方政府", "level": "地级市", "parent": "江西省人民政府", "location": "江西省抚州市"},
    {"id": "shangrao_cpc", "name": "中共上饶市委", "type": "党委", "level": "地级市", "parent": "中共江西省委", "location": "江西省上饶市"},
    {"id": "yingtan_cpc_discipline", "name": "中共鹰潭市纪律检查委员会", "type": "纪委", "level": "地级市", "parent": "中共江西省纪委", "location": "江西省鹰潭市"},
    {"id": "jdz_public_security", "name": "景德镇市公安局", "type": "政府部门", "level": "县级", "parent": "景德镇市人民政府", "location": "江西省景德镇市"},
    {"id": "jdz_high_tech_zone", "name": "景德镇高新技术产业开发区管委会", "type": "开发区管委会", "level": "国家级高新区", "parent": "景德镇市人民政府", "location": "江西省景德镇市"},
    {"id": "jiangxi_gov", "name": "江西省人民政府", "type": "地方政府", "level": "省级", "parent": "", "location": "江西省南昌市"},
    {"id": "jiangxi_cpc", "name": "中共江西省委", "type": "党委", "level": "省级", "parent": "", "location": "江西省南昌市"},
]

POSITIONS = [
    # ── 陈克龙 ──
    {"person": "jdz_chen_kelong", "org": "miit_planning", "title": "工业和信息化部规划司投资计划处处长", "start": "~2010",
     "end": "2017-12", "rank": "正处级", "note": "早期在工信部工作"},
    {"person": "jdz_chen_kelong", "org": "miit_planning", "title": "工业和信息化部规划司副司长", "start": "2017-12",
     "end": "2019-12", "rank": "副司级", "note": ""},
    {"person": "jdz_chen_kelong", "org": "miit_equipment", "title": "工业和信息化部装备工业一司副司长", "start": "2020",
     "end": "2021", "rank": "副司级", "note": "平调"},
    {"person": "jdz_chen_kelong", "org": "miit_raw_materials", "title": "工业和信息化部原材料工业司司长（稀土办公室主任）", "start": "2021",
     "end": "2023-05", "rank": "正司级", "note": "晋升正司级"},
    {"person": "jdz_chen_kelong", "org": "miit_planning", "title": "工业和信息化部规划司司长", "start": "2023-05",
     "end": "2024-10", "rank": "正司级", "note": "回到规划司任一把手"},
    {"person": "jdz_chen_kelong", "org": "jdz_municipal_gov",
     "title": "景德镇市委副书记、市政府党组书记、代市长", "start": "2024-10",
     "end": "2025-01", "rank": "正厅级", "note": "央地交流空降"},
    {"person": "jdz_chen_kelong", "org": "jdz_municipal_gov", "title": "景德镇市人民政府市长", "start": "2025-01",
     "end": "2026-05", "rank": "正厅级", "note": "2025年1月人大正式当选；2026年5月辞去市长职务"},
    {"person": "jdz_chen_kelong", "org": "jdz_cpc_committee", "title": "景德镇市委书记", "start": "2026-04",
     "end": None, "rank": "正厅级", "note": "2026年4月25日省委任命"},
    # ── 薛强 ──
    {"person": "jdz_xue_qiang", "org": "ganzhou_municipal",
     "title": "赣州市国际经济技术合作公司业务员、办公室副主任", "start": "1997-07",
     "end": "1999-04", "rank": "科员", "note": ""},
    {"person": "jdz_xue_qiang", "org": "ganzhou_municipal", "title": "大余县计划委员会科员", "start": "1999-04",
     "end": "2001-08", "rank": "科员", "note": ""},
    {"person": "jdz_xue_qiang", "org": "ganzhou_municipal", "title": "大余县计委副主任", "start": "2001-08",
     "end": "2003-06", "rank": "副科级", "note": "期间2000.04-2003.06借调赣州市计委/项目办"},
    {"person": "jdz_xue_qiang", "org": "ganzhou_municipal", "title": "赣州市项目办公室副主任", "start": "2003-06",
     "end": "2004", "rank": "正科级", "note": ""},
    {"person": "jdz_xue_qiang", "org": "ganzhou_municipal", "title": "赣州市发改委办公室主任", "start": "2008-04",
     "end": "2009-07", "rank": "正科级", "note": "2004-2008年在市发改委系统内有4年职务空缺"},
    {"person": "jdz_xue_qiang", "org": "ganzhou_municipal", "title": "赣州开发区发展规划局局长", "start": "2009-07",
     "end": "2011-05", "rank": "副处级", "note": ""},
    {"person": "jdz_xue_qiang", "org": "quannan_cpc", "title": "全南县委书记、县人大常委会主任", "start": "2011-05",
     "end": "2013-09", "rank": "正处级", "note": "首次主政一县"},
    {"person": "jdz_xue_qiang", "org": "longnan_cpc", "title": "龙南县委书记、龙南经济技术开发区党工委书记", "start": "2013-09",
     "end": "2016-08", "rank": "副厅级", "note": "晋升副厅；2015.03-2016.01挂职环保部规划财务司副司长"},
    {"person": "jdz_xue_qiang", "org": "ganzhou_municipal",
     "title": "赣南苏区振兴发展工作办公室主任", "start": "2016-08",
     "end": "2021-09", "rank": "副厅级", "note": ""},
    {"person": "jdz_xue_qiang", "org": "fuzhou_municipal", "title": "抚州市人民政府副市长", "start": "2021-09",
     "end": "2024-10", "rank": "副厅级", "note": ""},
    {"person": "jdz_xue_qiang", "org": "jdz_municipal_gov",
     "title": "景德镇市委常委、市政府党组副书记、常务副市长", "start": "2024-11",
     "end": None, "rank": "副厅级", "note": "2024年11月13日市人大常委会任命；市长空缺期间主持日常工作"},
    # ── 胡雪梅 ──
    {"person": "jdz_hu_xuemei", "org": "ganzhou_municipal",
     "title": "赣州市委常委、市政府副市长、党组副书记",
     "start": "~2018", "end": "2021-05", "rank": "副厅级", "note": "早期在赣州市工作"},
    {"person": "jdz_hu_xuemei", "org": "jdz_municipal_gov", "title": "景德镇市委副书记、市长", "start": "2021-05",
     "end": "2024-09", "rank": "正厅级", "note": ""},
    {"person": "jdz_hu_xuemei", "org": "jdz_cpc_committee", "title": "景德镇市委书记", "start": "2024-09",
     "end": "2026-04", "rank": "正厅级", "note": ""},
    # ── 刘锋 ──
    {"person": "jdz_liu_feng", "org": "shangrao_cpc", "title": "上饶师范专科学校中文系学习", "start": "1979-09",
     "end": "1982-07", "rank": "学生", "note": ""},
    {"person": "jdz_liu_feng", "org": "shangrao_cpc", "title": "上饶地区商业局干部", "start": "1982-08",
     "end": "1983-11", "rank": "科员", "note": ""},
    {"person": "jdz_liu_feng", "org": "shangrao_cpc", "title": "上饶地委办公室干部→政研室经济科副科长→科长", "start": "1983-11",
     "end": "1997-03", "rank": "正科级", "note": ""},
    {"person": "jdz_liu_feng", "org": "shangrao_cpc", "title": "余干县委常委、组织部部长", "start": "1997-11",
     "end": "2001-05", "rank": "副处级", "note": ""},
    {"person": "jdz_liu_feng", "org": "shangrao_cpc", "title": "上饶市委副秘书长、政研室主任", "start": "2001-05",
     "end": "2005-07", "rank": "正处级", "note": ""},
    {"person": "jdz_liu_feng", "org": "shangrao_cpc", "title": "鄱阳县委副书记、县长→县委书记", "start": "2005-07",
     "end": "2011-05", "rank": "正处级", "note": ""},
    {"person": "jdz_liu_feng", "org": "shangrao_cpc", "title": "玉山县委书记", "start": "2011-05",
     "end": "2013-07", "rank": "正处级", "note": ""},
    {"person": "jdz_liu_feng", "org": "shangrao_cpc", "title": "上饶市副市长（兼玉山县委书记）→市委常委、上饶经开区党工委书记", "start": "2013-07",
     "end": "2016-09", "rank": "副厅级", "note": ""},
    {"person": "jdz_liu_feng", "org": "jdz_municipal_gov", "title": "景德镇市委常委、副市长", "start": "2016-09",
     "end": "2017-08", "rank": "副厅级", "note": "跨市调任景德镇"},
    {"person": "jdz_liu_feng", "org": "jdz_municipal_gov", "title": "景德镇市委副书记（兼副市长）", "start": "2017-09",
     "end": "2018-11", "rank": "副厅级", "note": ""},
    {"person": "jdz_liu_feng", "org": "jdz_municipal_gov", "title": "景德镇市委副书记、代市长→市长", "start": "2018-11",
     "end": "2021-03", "rank": "正厅级", "note": "2019年1月正式当选市长"},
    {"person": "jdz_liu_feng", "org": "jdz_cpc_committee", "title": "景德镇市委书记", "start": "2021-03",
     "end": "2024-09", "rank": "正厅级", "note": ""},
    {"person": "jdz_liu_feng", "org": "jiangxi_gov", "title": "江西省人大财经委副主任委员", "start": "2024-09",
     "end": "2025-01", "rank": "正厅级", "note": "退居二线；2025年1月被免职（原因未公开）"},
    # ── 颜赣辉 ──
    {"person": "jdz_yan_ganhui", "org": "jdz_municipal_gov", "title": "景德镇市市长", "start": "2013-09",
     "end": "2016-04", "rank": "正厅级", "note": ""},
    {"person": "jdz_yan_ganhui", "org": "shangrao_cpc", "title": "上饶市市长", "start": "2016-04",
     "end": "2017-06", "rank": "正厅级", "note": ""},
    {"person": "jdz_yan_ganhui", "org": "jiangxi_cpc", "title": "宜春市委书记", "start": "2017-06",
     "end": "2020-06", "rank": "正厅级", "note": "2020年6月被免职调查；2021年判刑11年"},
    # ── 副市长团队 ──
    {"person": "jdz_zou_yongsheng", "org": "jdz_municipal_gov",
     "title": "景德镇市副市长、党组成员、市公安局局长", "start": "2019-12",
     "end": "2026-01", "rank": "副厅级", "note": "2026年初调省公安厅"},
    {"person": "jdz_zou_yongsheng", "org": "jiangxi_gov", "title": "江西省公安厅党委委员、副厅长", "start": "2026-01",
     "end": None, "rank": "副厅级", "note": "升职调离景德镇"},
    {"person": "jdz_wei_ji", "org": "jdz_municipal_gov", "title": "景德镇市副市长（挂职）、党组成员", "start": "2025-11",
     "end": None, "rank": "副厅级", "note": "原文旅部财务司副司长挂职；负责文旅"},
    {"person": "jdz_jiang_minqiang", "org": "jdz_municipal_gov", "title": "景德镇市副市长、市工商联主席", "start": "~2021",
     "end": None, "rank": "副厅级", "note": "无党派人士"},
    {"person": "jdz_luo_wenjun", "org": "jdz_municipal_gov",
     "title": "景德镇市副市长、党组成员、高新区党工委书记", "start": "~2021",
     "end": None, "rank": "副厅级", "note": "兼高新区党工委书记"},
    {"person": "jdz_xu_hui", "org": "jdz_municipal_gov", "title": "景德镇市副市长、党组成员", "start": "~2022",
     "end": None, "rank": "副厅级", "note": "负责住建、城管、教育等"},
    {"person": "jdz_gao_xiaoyun", "org": "jdz_municipal_gov", "title": "景德镇市副市长、党组成员", "start": "~2022",
     "end": None, "rank": "副厅级", "note": "负责工业、交通、高新区等"},
    {"person": "jdz_huang_lian", "org": "jdz_municipal_gov",
     "title": "景德镇市副市长、党组成员、市公安局局长", "start": "2026-06",
     "end": None, "rank": "副厅级", "note": "接替邹永胜的新任公安局长"},
    {"person": "jdz_huang_lian", "org": "jdz_public_security", "title": "景德镇市公安局局长", "start": "2026-06",
     "end": None, "rank": "副县级", "note": ""},
    {"person": "jdz_huang_jianping", "org": "jdz_municipal_gov", "title": "景德镇市政府秘书长、党组成员", "start": "~2022",
     "end": None, "rank": "正处级", "note": ""},
    # ── 其他机构 ──
    {"person": "jdz_yan_hua", "org": "jdz_npc_standing", "title": "景德镇市人大常委会主任", "start": "2026-01",
     "end": None, "rank": "正厅级", "note": "从鹰潭调任"},
    {"person": "yingtan_yan_hua", "org": "yingtan_cpc_discipline", "title": "鹰潭市委常委、市纪委书记、市监委主任", "start": "~2021",
     "end": "2025-12", "rank": "副厅级", "note": ""},
    {"person": "jdz_zhong_zhiSheng", "org": "jdz_cpc_committee", "title": "景德镇市委书记", "start": "2015",
     "end": "2021-03", "rank": "正厅级", "note": "前任市委书记，后调省直"},
]

RELATIONSHIPS = [
    # 工作交集：陈克龙与薛强同时被任命
    {"person_a": "jdz_chen_kelong", "person_b": "jdz_xue_qiang", "type": "强关系",
     "context": "同日（2024.11.13）被景德镇市人大常委会任命为副市长（陈为代市长，薛为常务副市长），属同一批次调配的新班子",
     "overlap_org": "景德镇市人民政府", "overlap_period": "2024.11至今"},

    # 工作交集：刘锋与胡雪梅交接
    {"person_a": "jdz_liu_feng", "person_b": "jdz_hu_xuemei", "type": "强关系",
     "context": "刘锋2021.3接任市委书记时，胡雪梅已任市长（2021.5起），二人搭档领导景德镇约3年",
     "overlap_org": "景德镇市四套班子", "overlap_period": "2021.05-2024.09"},

    # 工作交集：胡雪梅与陈克龙交接
    {"person_a": "jdz_hu_xuemei", "person_b": "jdz_chen_kelong", "type": "强关系",
     "context": "胡雪梅为书记时陈克龙任市长（2024.10-2026.04），先后搭档约18个月后陈接任书记",
     "overlap_org": "景德镇市四套班子", "overlap_period": "2024.10-2026.04"},

    # 工作交集：颜赣辉与刘锋同为景德镇市长
    {"person_a": "jdz_yan_ganhui", "person_b": "jdz_liu_feng", "type": "弱关系",
     "context": "先后任景德镇市长（颜2013-2016，刘2018-2021），刘锋到景德镇时颜已调离上饶",
     "overlap_org": "景德镇市人民政府", "overlap_period": "无直接共事"},

    # 工作交集：薛强与邹永胜
    {"person_a": "jdz_xue_qiang", "person_b": "jdz_zou_yongsheng", "type": "弱关系",
     "context": "薛强2024年底到任时邹永胜已在景德镇任副市长兼公安局长，共同工作约1年",
     "overlap_org": "景德镇市人民政府", "overlap_period": "2024.11-2026.01"},

    # 跨市交流：鄢华从鹰潭调任景德镇
    {"person_a": "jdz_yan_hua", "person_b": "yingtan_yan_hua", "type": "强关系",
     "context": "同一人（鄢华），从鹰潭市委常委、市纪委书记调任景德镇市人大常委会主任",
     "overlap_org": "跨市流动", "overlap_period": "2026.01调任"},

    # 跨市交流：刘锋从景德镇调任省人大
    {"person_a": "jdz_liu_feng", "person_b": "jdz_chen_kelong", "type": "弱关系",
     "context": "刘锋从市委书记退居二线（省人大财经委）为陈克龙接任腾出空间",
     "overlap_org": "景德镇市", "overlap_period": "2024.09交接"},

    # 景德镇与鹰潭跨市交流通道
    {"person_a": "jdz_zhong_zhiSheng", "person_b": "jdz_yan_hua", "type": "弱关系",
     "context": "钟志生（鹰潭市长→景德镇书记）与鄢华（鹰潭纪委书记→景德镇人大主任），同属鹰潭→景德镇交流通道",
     "overlap_org": "跨市流动（鹰潭→景德镇）", "overlap_period": "2015-2026（跨时段）"},
]


# ── 构建脚本 ─────────────────────────────────────────────────────────────

def build_database(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT REFERENCES persons(id),
            org_id TEXT REFERENCES organizations(id),
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT REFERENCES persons(id),
            person_b TEXT REFERENCES persons(id),
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT
        );
    """)

    for p in PERSONS:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in ORGANIZATIONS:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in POSITIONS:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person"], pos["org"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in RELATIONSHIPS:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()


def build_gexf(gexf_path):
    """Build GEXF 1.3 with viz namespace using string formatting."""

    # Node colors
    colors = {
        "party_secretary": (220, 50, 47),   # red (red)
        "gov_leader": (51, 122, 183),        # blue
        "discipline": (240, 150, 50),        # orange
        "other_gov": (100, 100, 100),        # grey
        "organization": (80, 80, 80),        # dark grey
        "central_gov": (60, 130, 60),        # green for central ministry
        "province": (90, 90, 150),           # purple for provincial
    }

    def person_color(person):
        if "书记" in (person.get("current_post") or "") and "陈克龙" in person["name"]:
            return colors["party_secretary"]
        if "颜赣辉" in person["name"]:
            return colors["discipline"]
        if "市长" in (person.get("current_post") or "") or "常务副" in (person.get("current_post") or ""):
            return colors["gov_leader"]
        if "副市" in (person.get("current_post") or ""):
            return colors["gov_leader"]
        if "纪委" in (person.get("current_post") or ""):
            return colors["discipline"]
        return colors["other_gov"]

    def org_color(org):
        if "中央" in org["type"] or "工信" in org["name"]:
            return colors["central_gov"]
        if "省级" == org["level"]:
            return colors["province"]
        return colors["organization"]

    def person_size(person):
        top_leaders = {"jdz_chen_kelong", "jdz_hu_xuemei", "jdz_liu_feng", "jdz_xue_qiang", "jdz_yan_ganhui"}
        if person["id"] in top_leaders:
            return 20.0
        return 12.0

    # Collect IDs
    person_ids = {p["id"] for p in PERSONS}
    org_ids = {o["id"] for o in ORGANIZATIONS}

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="type" title="Type" type="string"/>')
    lines.append('      <attribute id="role" title="Role" type="string"/>')
    lines.append('      <attribute id="birth" title="Birth" type="string"/>')
    lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
    lines.append('      <attribute id="education" title="Education" type="string"/>')
    lines.append('      <attribute id="source" title="Source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="type" title="Type" type="string"/>')
    lines.append('      <attribute id="context" title="Context" type="string"/>')
    lines.append('      <attribute id="start" title="Start" type="string"/>')
    lines.append('      <attribute id="end" title="End" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        c = person_color(p)
        sz = person_size(p)
        role = "person"
        if "书记" in (p.get("current_post") or "") and "纪委" not in (p.get("current_post") or ""):
            role = "party_secretary"
        elif "市" in (p.get("current_post") or "") and "副" not in (p.get("current_post") or ""):
            role = "gov_leader"
        elif "副" in (p.get("current_post") or ""):
            role = "deputy"
        elif "纪委" in (p.get("current_post") or ""):
            role = "discipline"

        lines.append(f'      <node id="{p["id"]}" label="{p["name"]}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="person"/>')
        lines.append(f'          <attvalue for="role" value="{role}"/>')
        lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
        lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
        lines.append(f'          <attvalue for="education" value="{p["education"]}"/>')
        lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}" a="1"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'      </node>')
    for o in ORGANIZATIONS:
        c = org_color(o)
        lines.append(f'      <node id="{o["id"]}" label="{o["name"]}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="organization"/>')
        lines.append(f'          <attvalue for="role" value="{o["type"]}"/>')
        lines.append(f'          <attvalue for="birth" value=""/>')
        lines.append(f'          <attvalue for="birthplace" value="{o["location"]}"/>')
        lines.append(f'          <attvalue for="education" value=""/>')
        lines.append(f'          <attvalue for="source" value=""/>')
        lines.append(f'        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}" a="1"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="square"/>')
        lines.append(f'      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    edge_idx = 0

    # Person → Organization (worked_at)
    for pos in POSITIONS:
        if pos["person"] not in person_ids or pos["org"] not in org_ids:
            continue
        edge_idx += 1
        lines.append(f'      <edge id="e{edge_idx}" source="{pos["person"]}" target="{pos["org"]}" weight="1.5">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
        lines.append(f'          <attvalue for="start" value="{pos["start"] or ""}"/>')
        lines.append(f'          <attvalue for="end" value="{pos["end"] or ""}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'        <viz:color r="180" g="180" b="180" a="0.6"/>')
        lines.append(f'        <viz:thickness value="1.0"/>')
        lines.append(f'      </edge>')

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        if r["person_a"] not in person_ids or r["person_b"] not in person_ids:
            continue
        edge_idx += 1
        is_strong = "强关系" in r["type"]
        weight = 4.0 if is_strong else 2.0
        color = (201, 169, 78) if is_strong else (100, 150, 200)
        lines.append(f'      <edge id="e{edge_idx}" source="{r["person_a"]}" target="{r["person_b"]}" weight="{weight}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="relationship"/>')
        lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
        lines.append(f'          <attvalue for="start" value="{r["overlap_period"]}"/>')
        lines.append(f'          <attvalue for="end" value=""/>')
        lines.append(f'        </attvalues>')
        lines.append(f'        <viz:color r="{color[0]}" g="{color[1]}" b="{color[2]}" a="0.8"/>')
        lines.append(f'        <viz:thickness value="{2.0 if is_strong else 0.8}"/>')
        lines.append(f'      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def print_summary(db_path, gexf_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    print(f"{'='*60}")
    print(f"  景德镇市市长（市长空缺）— 领导班子工作关系网络")
    print(f"  调查日期: 2026-07-14")
    print(f"{'='*60}")

    n_people = c.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    n_orgs = c.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
    n_pos = c.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
    n_rel = c.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
    print(f"\n  📊 统计")
    print(f"  人物: {n_people} 人")
    print(f"  机构: {n_orgs} 个")
    print(f"  任职: {n_pos} 条")
    print(f"  关系: {n_rel} 条")
    print()

    print(f"  📁 文件")
    print(f"  数据库: {os.path.abspath(db_path)}")
    print(f"  GEXF:   {os.path.abspath(gexf_path)}")

    # List mayor succession
    print(f"\n  📋 市长任职链（颜赣辉 → 刘锋 → 胡雪梅 → 陈克龙 → [空缺]）")
    print(f"  颜赣辉 (2013-2016) → 🔴 2020年被查，判刑11年")
    print(f"  梅亦  (2016-2018) → 调省医保局")
    print(f"  刘锋  (2018-2021任市长→2021-2024任书记) → 2025年1月被免职")
    print(f"  胡雪梅 (2021-2024任市长→2024-2026任书记) → 调省广播电视局（待确认）")
    print(f"  陈克龙 (2024-2026任市长→2026.4任书记) → 💡央地交流干部")
    print(f"  🔴 市长职位现在空缺（截至2026年7月14日）")
    print()

    conn.close()


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")

    db_path = os.path.join(data_dir, "database", "jingdezhen_mayor.db")
    gexf_path = os.path.join(data_dir, "graph", "jingdezhen_mayor.gexf")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    os.makedirs(os.path.dirname(gexf_path), exist_ok=True)

    build_database(db_path)
    build_gexf(gexf_path)
    print_summary(db_path, gexf_path)
