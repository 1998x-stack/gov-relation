#!/usr/bin/env python3
"""
民乐县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

民乐县 — 甘肃省张掖市下辖县，位于祁连山北麓，河西走廊中段，张掖市东南部。

数据来源:
- 民乐县人民政府官方网站 (www.gsml.gov.cn)
- 百度百科/百度搜索
- 新闻报道（张掖市人民政府网、澎湃新闻、新浪新闻等）
- 任前公示信息（甘肃组工网）

注意: 部分履历信息基于公开资料汇总整理，标记了置信度级别。
"""

import json
import os
import sqlite3
from datetime import datetime

# ── 路径 ──────────────────────────────────────────────
BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_民乐县")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "民乐县_network.db")
GEXF_PATH = os.path.join(STAGING, "民乐县_network.gexf")

# ── 数据 ──────────────────────────────────────────────

# 1. 人员
persons = [
    # === 核心领导（目标人物）===
    # 县委书记
    {
        "id": "p01",
        "name": "张鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "甘肃甘州",
        "native_place": "甘肃甘州",
        "education": "省委党校研究生学历",
        "party_join": "中共党员（1995年7月加入）",
        "work_start": "1990年代?",
        "current_post": "民乐县委书记、县人武部党委第一书记",
        "current_org": "中共民乐县委员会",
        "source": "百度百科、民乐县人民政府官网、甘肃组工网",
        "person_id": "minle_zhang_peng"
    },
    # 县长
    {
        "id": "p02",
        "name": "张晓龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "甘肃敦煌",
        "native_place": "甘肃敦煌",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "2000年?",
        "current_post": "民乐县委副书记、县人民政府县长",
        "current_org": "民乐县人民政府",
        "source": "民乐县人民政府官网、百度百科、汲古新知",
        "person_id": "minle_zhang_xiaolong"
    },
    # === 县委副书记 ===
    {
        "id": "p03",
        "name": "许治建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年4月",
        "birthplace": "甘肃高台",
        "native_place": "甘肃高台",
        "education": "自考大学学历",
        "party_join": "中共党员",
        "work_start": "2000年?",
        "current_post": "民乐县委副书记",
        "current_org": "中共民乐县委员会",
        "source": "百度百科、民乐县人民政府官网",
        "person_id": "minle_xu_zhijian"
    },
    # 副书记（还有一位范文成）
    {
        "id": "p04",
        "name": "范文成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "民乐县委副书记",
        "current_org": "中共民乐县委员会",
        "source": "政协民乐县第十届委员会第四次会议报道",
        "person_id": "minle_fan_wencheng"
    },
    # === 常务副县长 ===
    {
        "id": "p05",
        "name": "李培福",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "民乐县委常委、常务副县长",
        "current_org": "民乐县人民政府",
        "source": "民乐县人民政府官网",
        "person_id": "minle_li_peifu"
    },
    # === 县委常委 ===
    {
        "id": "p06",
        "name": "卢芋辰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "民乐县委常委（具体职务待确认）",
        "current_org": "中共民乐县委员会",
        "source": "民乐县人民政府官网",
        "person_id": "minle_lu_yuchen"
    },
    {
        "id": "p07",
        "name": "付强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "民乐县委常委（具体职务待确认）",
        "current_org": "中共民乐县委员会",
        "source": "民乐县人民政府官网",
        "person_id": "minle_fu_qiang"
    },
    {
        "id": "p08",
        "name": "展兴华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "民乐县委常委（具体职务待确认）",
        "current_org": "中共民乐县委员会",
        "source": "民乐县人民政府官网",
        "person_id": "minle_zhan_xinghua"
    },
    {
        "id": "p09",
        "name": "高峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "民乐县委常委、武装部部长",
        "current_org": "民乐县人民武装部",
        "source": "民乐县人民政府官网",
        "person_id": "minle_gao_feng"
    },
    {
        "id": "p10",
        "name": "王金刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "民乐县委常委（具体职务待确认）",
        "current_org": "中共民乐县委员会",
        "source": "百度百科、民乐县人民政府官网",
        "person_id": "minle_wang_jingang"
    },
    {
        "id": "p11",
        "name": "陈朝贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "民乐县委常委、副县长",
        "current_org": "民乐县人民政府",
        "source": "民乐县人民政府官网",
        "person_id": "minle_chen_chaogui"
    },
    # === 人大主任 ===
    {
        "id": "p12",
        "name": "张自新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年4月",
        "birthplace": "甘肃民乐",
        "native_place": "甘肃民乐",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "民乐县人大常委会党组书记、主任",
        "current_org": "民乐县人大常委会",
        "source": "百度百科、民乐县人民政府官网",
        "person_id": "minle_zhang_zixin"
    },
    # === 政协主席 ===
    {
        "id": "p13",
        "name": "杨瑗芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "民乐县政协主席",
        "current_org": "政协民乐县委员会",
        "source": "民乐县新闻报道",
        "person_id": "minle_yang_yuanfang"
    },
    # === 前任县委书记（被查）===
    {
        "id": "p14",
        "name": "李作明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "甘肃定西",
        "native_place": "甘肃定西",
        "education": "在职研究生学历",
        "party_join": "中共党员（1995年7月加入）",
        "work_start": "1994年8月",
        "current_post": "原民乐县委书记（2024年5月被查）",
        "current_org": "",
        "source": "澎湃新闻、新浪新闻、甘肃省纪委监委通报",
        "person_id": "minle_li_zuoming"
    },
    # === 前任县长 ===
    {
        "id": "p15",
        "name": "牛益民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年9月",
        "birthplace": "甘肃张掖",
        "native_place": "河南洛阳",
        "education": "大学学历、农学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原民乐县长（2019-2023年任职）",
        "current_org": "",
        "source": "甘肃组工网任前公示",
        "person_id": "minle_niu_yimin"
    },
    # === 副县长（其他）===
    {
        "id": "p16",
        "name": "钟波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "民乐县副县长",
        "current_org": "民乐县人民政府",
        "source": "民乐县人民政府官网",
        "person_id": "minle_zhong_bo"
    },
    {
        "id": "p17",
        "name": "魏燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "民乐县副县长",
        "current_org": "民乐县人民政府",
        "source": "民乐县人民政府官网",
        "person_id": "minle_wei_yan"
    },
]

# 2. 组织
organizations = [
    {"id": "o01", "name": "中共民乐县委员会", "type": "党委", "level": "县处级", "parent": "中共张掖市委员会", "location": "民乐县"},
    {"id": "o02", "name": "民乐县人民政府", "type": "政府", "level": "县处级", "parent": "张掖市人民政府", "location": "民乐县"},
    {"id": "o03", "name": "民乐县人大常委会", "type": "人大", "level": "县处级", "parent": "民乐县", "location": "民乐县"},
    {"id": "o04", "name": "政协民乐县委员会", "type": "政协", "level": "县处级", "parent": "民乐县", "location": "民乐县"},
    {"id": "o05", "name": "中共民乐县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共民乐县委员会", "location": "民乐县"},
    {"id": "o06", "name": "民乐县人民武装部", "type": "事业单位", "level": "县处级", "parent": "民乐县", "location": "民乐县"},
    {"id": "o07", "name": "中共甘州区委员会", "type": "党委", "level": "县处级", "parent": "中共张掖市委员会", "location": "甘州区"},
    {"id": "o08", "name": "甘州区人民政府", "type": "政府", "level": "县处级", "parent": "张掖市人民政府", "location": "甘州区"},
    {"id": "o09", "name": "中共临泽县委员会", "type": "党委", "level": "县处级", "parent": "中共张掖市委员会", "location": "临泽县"},
    {"id": "o10", "name": "临泽县人民政府", "type": "政府", "level": "县处级", "parent": "张掖市人民政府", "location": "临泽县"},
    {"id": "o11", "name": "中共岷县委员会", "type": "党委", "level": "县处级", "parent": "中共定西市委员会", "location": "岷县"},
    {"id": "o12", "name": "中共临洮县委员会", "type": "党委", "level": "县处级", "parent": "中共定西市委员会", "location": "临洮县"},
    {"id": "o13", "name": "张掖市人民政府办公室", "type": "政府", "level": "县处级", "parent": "张掖市人民政府", "location": "甘州区"},
    {"id": "o14", "name": "民乐工业园区", "type": "开发区", "level": "县处级", "parent": "民乐县人民政府", "location": "民乐县"},
    {"id": "o15", "name": "民乐县丰乐镇", "type": "乡镇/街道", "level": "乡科级", "parent": "民乐县", "location": "丰乐镇"},
    {"id": "o16", "name": "民乐县六坝镇", "type": "乡镇/街道", "level": "乡科级", "parent": "民乐县", "location": "六坝镇"},
    {"id": "o17", "name": "民乐县洪水镇", "type": "乡镇/街道", "level": "乡科级", "parent": "民乐县", "location": "洪水镇"},
]

# 3. 任职
positions = [
    # 张鹏 - 县委书记
    {"person_id": "p01", "org_id": "o01", "title": "民乐县委书记", "start": "2024年8月", "end": "至今", "rank": "正县级", "note": "2024年8月任民乐县委书记；2026年6月拟提名为市（州）政府副市（州）长人选"},
    {"person_id": "p01", "org_id": "o10", "title": "临泽县委副书记、县长", "start": "约2019年", "end": "2024年8月", "rank": "正县级", "note": "此前任临泽县长"},
    {"person_id": "p01", "org_id": "o07", "title": "甘州区委常委、政法委书记", "start": "约2016年", "end": "约2019年", "rank": "副县级", "note": ""},
    {"person_id": "p01", "org_id": "o08", "title": "甘州区副区长", "start": "约2011年", "end": "约2016年", "rank": "副县级", "note": ""},
    {"person_id": "p01", "org_id": "o07", "title": "甘州区发改委主任", "start": "约2010年", "end": "约2011年", "rank": "正科级", "note": "曾任甘州区发展和改革委员会主任"},
    # 张鹏早期在甘州区乡镇
    {"person_id": "p01", "org_id": "o07", "title": "甘州区上秦镇党委书记", "start": "约2006年", "end": "约2010年", "rank": "正科级", "note": "曾任上秦镇党委书记"},
    {"person_id": "p01", "org_id": "o07", "title": "甘州区上秦镇镇长", "start": "约2004年", "end": "约2006年", "rank": "副科级", "note": ""},
    {"person_id": "p01", "org_id": "o07", "title": "甘州区梁家墩镇副镇长", "start": "约2001年", "end": "约2004年", "rank": "副科级", "note": ""},
    {"person_id": "p01", "org_id": "o07", "title": "甘州区三闸乡副乡长", "start": "约1998年", "end": "约2001年", "rank": "副科级", "note": "三闸乡副乡长"},
    # 张晓龙 - 县长
    {"person_id": "p02", "org_id": "o02", "title": "民乐县委副书记、县长", "start": "2023年9月", "end": "至今", "rank": "正县级", "note": "2023年9月任县长候选人，后正式当选"},
    {"person_id": "p02", "org_id": "o08", "title": "甘州区委常委、常务副区长", "start": "2023年3月", "end": "2023年9月", "rank": "副县级", "note": ""},
    {"person_id": "p02", "org_id": "o13", "title": "张掖市政府办公室副主任", "start": "约2019年", "end": "2023年3月", "rank": "副县级", "note": ""},
    {"person_id": "p02", "org_id": "o13", "title": "张掖市政府办公室秘书四科科长", "start": "约2012年", "end": "约2019年", "rank": "正科级", "note": ""},
    {"person_id": "p02", "org_id": "o13", "title": "张掖市政府办公室干部", "start": "约2005年", "end": "约2012年", "rank": "科级", "note": ""},
    # 许治建 - 副书记
    {"person_id": "p03", "org_id": "o01", "title": "民乐县委副书记", "start": "约2024年", "end": "至今", "rank": "副县级", "note": "来自高台县"},
    {"person_id": "p03", "org_id": "o01", "title": "民乐县委常委", "start": "约2023年", "end": "约2024年", "rank": "副县级", "note": ""},
    # 范文成 - 副书记
    {"person_id": "p04", "org_id": "o01", "title": "民乐县委副书记", "start": "未知", "end": "至今", "rank": "副县级", "note": ""},
    # 李培福 - 常务副县长
    {"person_id": "p05", "org_id": "o02", "title": "民乐县委常委、常务副县长", "start": "未知", "end": "至今", "rank": "副县级", "note": ""},
    # 卢芋辰 - 县委常委
    {"person_id": "p06", "org_id": "o01", "title": "民乐县委常委", "start": "未知", "end": "至今", "rank": "副县级", "note": "女，1979年10月出生"},
    # 付强 - 县委常委
    {"person_id": "p07", "org_id": "o01", "title": "民乐县委常委", "start": "未知", "end": "至今", "rank": "副县级", "note": "1980年1月出生，省委党校研究生学历"},
    # 展兴华 - 县委常委
    {"person_id": "p08", "org_id": "o01", "title": "民乐县委常委", "start": "未知", "end": "至今", "rank": "副县级", "note": "1973年12月出生"},
    # 高峰 - 人武部长
    {"person_id": "p09", "org_id": "o06", "title": "民乐县委常委、武装部部长", "start": "未知", "end": "至今", "rank": "副县级", "note": "1978年9月出生"},
    # 王金刚 - 县委常委
    {"person_id": "p10", "org_id": "o01", "title": "民乐县委常委", "start": "未知", "end": "至今", "rank": "副县级", "note": ""},
    # 陈朝贵 - 副县长
    {"person_id": "p11", "org_id": "o02", "title": "民乐县委常委、副县长", "start": "未知", "end": "至今", "rank": "副县级", "note": ""},
    # 张自新 - 人大主任
    {"person_id": "p12", "org_id": "o03", "title": "民乐县人大常委会党组书记、主任", "start": "2025年1月", "end": "至今", "rank": "正县级", "note": "2025年1月补选为县人大常委会主任"},
    # 杨瑗芳 - 政协主席
    {"person_id": "p13", "org_id": "o04", "title": "民乐县政协主席", "start": "未知", "end": "至今", "rank": "正县级", "note": ""},
    # 李作明 - 前任书记（被查）
    {"person_id": "p14", "org_id": "o01", "title": "民乐县委书记", "start": "约2020年", "end": "2024年5月", "rank": "正县级", "note": "2024年5月被甘肃省纪委监委审查调查"},
    {"person_id": "p14", "org_id": "o12", "title": "临洮县委常委、副县长", "start": "2009年11月", "end": "约2011年", "rank": "副县级", "note": "兼任县城投公司董事长"},
    {"person_id": "p14", "org_id": "o12", "title": "临洮县委常委、政法委书记", "start": "2006年11月", "end": "2009年11月", "rank": "副县级", "note": ""},
    {"person_id": "p14", "org_id": "o11", "title": "岷县副县长", "start": "2004年", "end": "2006年11月", "rank": "副县级", "note": ""},
    {"person_id": "p14", "org_id": "o11", "title": "岷县西江镇党委书记", "start": "约2002年", "end": "2004年", "rank": "正科级", "note": ""},
    {"person_id": "p14", "org_id": "o11", "title": "岷县西江镇党委副书记、镇长", "start": "2000年2月", "end": "约2002年", "rank": "正科级", "note": ""},
    {"person_id": "p14", "org_id": "o11", "title": "岷县茶埠乡党委副书记", "start": "1998年3月", "end": "2000年2月", "rank": "副科级", "note": ""},
    {"person_id": "p14", "org_id": "o11", "title": "岷县茶埠乡副乡长", "start": "1996年12月", "end": "1998年3月", "rank": "副科级", "note": ""},
    {"person_id": "p14", "org_id": "o11", "title": "岷县茶埠乡干部", "start": "1994年8月", "end": "1996年12月", "rank": "办事员", "note": ""},
    # 牛益民 - 前任县长
    {"person_id": "p15", "org_id": "o02", "title": "民乐县县长", "start": "2019年", "end": "2023年9月", "rank": "正县级", "note": "2019年1月公示拟提名为县长候选人，2023年9月由张晓龙接替"},
    {"person_id": "p15", "org_id": "o01", "title": "民乐县委副书记（正县级）", "start": "2015年6月", "end": "2019年", "rank": "正县级", "note": "2015年6月任中共民乐县委委员、常委、副书记（正县级）"},
    # 钟波 - 副县长
    {"person_id": "p16", "org_id": "o02", "title": "民乐县副县长", "start": "未知", "end": "至今", "rank": "副县级", "note": ""},
    # 魏燕 - 副县长
    {"person_id": "p17", "org_id": "o02", "title": "民乐县副县长", "start": "未知", "end": "至今", "rank": "副县级", "note": ""},
]

# 4. 关系
relationships = [
    # 张鹏 & 张晓龙 — 党政主要领导关系
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "2023年9月起分别任县委书记和县长，党政主要领导搭档关系",
     "overlap_org": "民乐县", "overlap_period": "2024年8月至今", "direction": "undirected"},
    # 张鹏 & 李作明 — 前后任书记
    {"person_a": "p01", "person_b": "p14", "type": "predecessor_successor", "context": "李作明被查后，张鹏接任民乐县委书记",
     "overlap_org": "中共民乐县委员会", "overlap_period": "2024年", "direction": "person_to_other"},
    # 张晓龙 & 牛益民 — 前后任县长
    {"person_a": "p02", "person_b": "p15", "type": "predecessor_successor", "context": "牛益民后，张晓龙接任民乐县长",
     "overlap_org": "民乐县人民政府", "overlap_period": "2023年", "direction": "person_to_other"},
    # 张鹏 & 张晓龙 — 曾在甘州区共事
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "张鹏曾任甘州区委常委、政法委书记、副区长；张晓龙曾任甘州区委常委、常务副区长，两人可能在甘州区有交集",
     "overlap_org": "甘州区", "overlap_period": "约2016-2023年", "direction": "undirected"},
    # 张鹏 & 牛益民 — 前后任关系（张鹏接替李作明，牛益民是前任县长）
    {"person_a": "p01", "person_b": "p15", "type": "overlap", "context": "张鹏任书记时牛益民已离任，无直接共事",
     "overlap_org": "民乐县", "overlap_period": "2024年", "direction": "undirected"},
    # 李作明 & 牛益民 — 曾搭班
    {"person_a": "p14", "person_b": "p15", "type": "overlap", "context": "李作明任书记期间，牛益民任县长，党政主要领导搭档",
     "overlap_org": "民乐县", "overlap_period": "约2020-2023年", "direction": "undirected"},
    # 张鹏 & 许治建 — 上下级
    {"person_a": "p01", "person_b": "p03", "type": "superior_subordinate", "context": "许治建任县委副书记，张鹏为书记",
     "overlap_org": "中共民乐县委员会", "overlap_period": "约2024年至今", "direction": "person_to_other"},
    # 张晓龙 & 李培福 — 上下级
    {"person_a": "p02", "person_b": "p05", "type": "superior_subordinate", "context": "李培福任常务副县长，协助县长张晓龙工作",
     "overlap_org": "民乐县人民政府", "overlap_period": "至今", "direction": "person_to_other"},
    # 李作明 — 定西系统出身（与岷县、临洮连接）
    {"person_a": "p14", "person_b": "p15", "type": "same_system", "context": "李作明（定西岷县出身）与牛益民（张掖本地干部）不同系统背景",
     "overlap_org": "", "overlap_period": "", "direction": "undirected"},
]

# ── SQLite 构建 ────────────────────────────────────────

def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
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
        )
    """)
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            direction TEXT
        )
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", (
            int(p["id"][1:]), p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], p["education"],
            p["party_join"], p["work_start"],
            p["current_post"], p["current_org"], p["source"]
        ))
    for o in organizations:
        cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            int(o["id"][1:]), o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))
    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)""", (
            int(pos["person_id"][1:]), int(pos["org_id"][1:]),
            pos["title"], pos["start"], pos["end"],
            pos["rank"], pos["note"]
        ))
    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, direction) VALUES (?,?,?,?,?,?,?)""", (
            int(r["person_a"][1:]), int(r["person_b"][1:]),
            r["type"], r["context"], r["overlap_org"],
            r["overlap_period"], r["direction"]
        ))

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ── GEXF 构建 ──────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string by role."""
    post = p["current_post"]
    if "县委书记" in post or "书记" in post and "副" not in post:
        return "255,50,50"
    elif "县长" in post:
        return "50,100,255"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    elif "人大" in post:
        return "200,255,255"
    elif "政协" in post:
        return "255,240,200"
    else:
        return "100,100,100"

def is_top_leader(p):
    return p["id"] in ("p01", "p02")

def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "default": "200,200,200",
    }
    return colors.get(t, colors["default"])

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>民乐县领导班子工作关系网络 — 民乐县位于甘肃省张掖市</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        oid = o["id"]
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person -> organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{pos["person_id"]}" target="{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person <-> person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")


# ── 主入口 ─────────────────────────────────────────────

if __name__ == "__main__":
    build_database()
    build_gexf()
    print("🎉 Done! Database and GEXF graph for 民乐县 are ready.")
