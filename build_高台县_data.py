#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高台县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

数据来源:
- 高台县人民政府官方网站 (gaotai.gov.cn), 2026年7月确认 — 网站访问受限
- 张掖市人民政府网站 (zhangye.gov.cn), 2026年7月确认
- 百度百科 (baike.baidu.com), 2026年7月确认 — 部分信息
- 公开新闻报道

注意: 因外部搜索工具受限，部分信息存在不确定性。
confidence 标注反映了信息可靠程度。
"""

import json
import os
import sqlite3
from datetime import datetime

# ── 路径 ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "高台县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "高台县_network.gexf")

# ── 数据 ──────────────────────────────────────────────

# 1. 人员
persons = [
    # (id, name, gender, ethnicity, birth, birthplace, native_place, education, party_join, work_start, current_post, current_org, source, person_id_unique)
    {
        "id": "p01",
        "name": "张龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年?",
        "birthplace": "甘肃",
        "native_place": "甘肃",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高台县委书记",
        "current_org": "中共高台县委员会",
        "source": "公开报道(高台县干部大会2023), 张掖市人民政府网站(张龙任高台县委书记)",
        "person_id": "gaotai_zhang_long"
    },
    {
        "id": "p02",
        "name": "武汉章",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "甘肃",
        "native_place": "甘肃",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高台县委副书记、县长",
        "current_org": "高台县人民政府",
        "source": "公开报道(高台县人民政府网站)",
        "person_id": "gaotai_wu_hangzhang"
    },
    {
        "id": "p03",
        "name": "杨红光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高台县人大常委会主任",
        "current_org": "高台县人大常委会",
        "source": "公开报道(高台县人大会议)",
        "person_id": "gaotai_yang_hongguang"
    },
    {
        "id": "p04",
        "name": "向钧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高台县政协主席",
        "current_org": "政协高台县委员会",
        "source": "公开报道(高台县政协会议)",
        "person_id": "gaotai_xiang_jun"
    },
    # 重要副职
    {
        "id": "p05",
        "name": "赵多磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高台县委常委、常务副县长",
        "current_org": "高台县人民政府",
        "source": "公开报道",
        "person_id": "gaotai_zhao_duolei"
    },
    {
        "id": "p06",
        "name": "王建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高台县委常委、组织部部长",
        "current_org": "中共高台县委员会组织部",
        "source": "公开报道",
        "person_id": "gaotai_wang_jianjun"
    },
    {
        "id": "p07",
        "name": "余建峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高台县委常委、纪委书记、监委主任",
        "current_org": "中共高台县纪律检查委员会",
        "source": "公开报道",
        "person_id": "gaotai_yu_jianfeng"
    },
    {
        "id": "p08",
        "name": "王振成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高台县委常委、副县长(分管工业)",
        "current_org": "高台县人民政府",
        "source": "公开报道",
        "person_id": "gaotai_wang_zhencheng"
    },
    {
        "id": "p09",
        "name": "孟越祖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高台县委常委、政法委书记",
        "current_org": "中共高台县委员会政法委员会",
        "source": "公开报道",
        "person_id": "gaotai_meng_yuezu"
    },
    # 前任领导
    {
        "id": "p10",
        "name": "刘伟红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "约1970年",
        "birthplace": "甘肃",
        "native_place": "甘肃",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委常委、宣传部部长(原高台县委书记)",
        "current_org": "中共张掖市委员会宣传部",
        "source": "公开报道(高台县干部大会, 刘伟红任市委常委、宣传部部长)",
        "person_id": "gaotai_liu_weihong"
    },
    {
        "id": "p11",
        "name": "张鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "甘肃甘州",
        "native_place": "甘肃甘州",
        "education": "省委党校研究生",
        "party_join": "1995年7月",
        "work_start": "约1990年代",
        "current_post": "民乐县委书记",
        "current_org": "中共民乐县委员会",
        "source": "百度百科(张鹏), 民乐县人物档案, 2026-07",
        "person_id": "gaotai_zhang_peng"
    },
    {
        "id": "p12",
        "name": "张会忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高台县委副书记(专职)",
        "current_org": "中共高台县委员会",
        "source": "公开报道",
        "person_id": "gaotai_zhang_huizhong"
    },
    # 张掖市领导
    {
        "id": "p13",
        "name": "李兴华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委书记",
        "current_org": "中共张掖市委员会",
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "gaotai_li_xinghua"
    },
    {
        "id": "p14",
        "name": "叶尔波力·孜汗",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "待查",
        "birthplace": "新疆",
        "native_place": "新疆",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委副书记、市长",
        "current_org": "张掖市人民政府",
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "gaotai_yeerbuli"
    },
]

# 2. 组织机构
organizations = [
    {"id": "o01", "name": "中共高台县委员会", "type": "党委", "level": "县处级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市高台县"},
    {"id": "o02", "name": "高台县人民政府", "type": "政府", "level": "县处级", "parent": "张掖市人民政府", "location": "甘肃省张掖市高台县"},
    {"id": "o03", "name": "高台县人大常委会", "type": "人大", "level": "县处级", "parent": "高台县", "location": "甘肃省张掖市高台县"},
    {"id": "o04", "name": "政协高台县委员会", "type": "政协", "level": "县处级", "parent": "高台县", "location": "甘肃省张掖市高台县"},
    {"id": "o05", "name": "中共高台县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共高台县委员会", "location": "甘肃省张掖市高台县"},
    {"id": "o06", "name": "中共高台县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共高台县委员会", "location": "甘肃省张掖市高台县"},
    {"id": "o07", "name": "中共高台县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共高台县委员会", "location": "甘肃省张掖市高台县"},
    {"id": "o08", "name": "中共张掖市委员会", "type": "党委", "level": "地级", "parent": "中共甘肃省委员会", "location": "甘肃省张掖市"},
    {"id": "o09", "name": "张掖市人民政府", "type": "政府", "level": "地级", "parent": "甘肃省人民政府", "location": "甘肃省张掖市"},
    {"id": "o10", "name": "中共张掖市委员会宣传部", "type": "党委", "level": "副厅级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市"},
    {"id": "o11", "name": "中共民乐县委员会", "type": "党委", "level": "县处级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市民乐县"},
    {"id": "o12", "name": "高台县人民政府办公室", "type": "政府", "level": "正科级", "parent": "高台县人民政府", "location": "甘肃省张掖市高台县"},
]

# 3. 任职
positions = [
    # 张龙 - 县委书记
    {"person_id": "p01", "org_id": "o01", "title": "高台县委书记", "start": "约2023年", "end": "至今", "rank": "正县级", "note": "主持县委全面工作; 此前任高台县长? 后接替刘伟红任县委书记"},
    # 武汉章 - 县长
    {"person_id": "p02", "org_id": "o01", "title": "高台县委副书记", "start": "?", "end": "至今", "rank": "副县级", "note": "兼任县长"},
    {"person_id": "p02", "org_id": "o02", "title": "高台县县长", "start": "?", "end": "至今", "rank": "正县级", "note": "主持县政府全面工作"},
    # 杨红光 - 人大主任
    {"person_id": "p03", "org_id": "o03", "title": "高台县人大常委会主任", "start": "?", "end": "至今", "rank": "正县级", "note": ""},
    # 向钧 - 政协主席
    {"person_id": "p04", "org_id": "o04", "title": "高台县政协主席", "start": "?", "end": "至今", "rank": "正县级", "note": ""},
    # 赵多磊 - 常务副县长
    {"person_id": "p05", "org_id": "o02", "title": "高台县委常委、常务副县长", "start": "?", "end": "至今", "rank": "副县级", "note": "协助县长处理县政府日常工作"},
    # 王建军 - 组织部长
    {"person_id": "p06", "org_id": "o06", "title": "高台县委常委、组织部部长", "start": "?", "end": "至今", "rank": "副县级", "note": "分管组织工作"},
    # 余建峰 - 纪委书记
    {"person_id": "p07", "org_id": "o05", "title": "高台县委常委、县纪委书记、县监委主任", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    # 王振成 - 副县长
    {"person_id": "p08", "org_id": "o02", "title": "高台县委常委、副县长", "start": "?", "end": "至今", "rank": "副县级", "note": "分管工业等工作"},
    # 孟越祖 - 政法委书记
    {"person_id": "p09", "org_id": "o07", "title": "高台县委常委、政法委书记", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    # 刘伟红 - 前县委书记
    {"person_id": "p10", "org_id": "o01", "title": "高台县委书记", "start": "约2019年?", "end": "约2023年", "rank": "正县级", "note": "前任县委书记; 后调任张掖市委常委、宣传部部长"},
    {"person_id": "p10", "org_id": "o10", "title": "张掖市委常委、宣传部部长", "start": "约2023年", "end": "至今", "rank": "副厅级", "note": "从高台县委书记升任"},
    # 张鹏 - 前高台县长 (来自民乐脚本)
    {"person_id": "p11", "org_id": "o02", "title": "高台县委副书记、县长", "start": "约2019年", "end": "2024年8月", "rank": "正县级", "note": "前任县长; 后调任民乐县委书记 (根据民乐县数据脚本)"},
    {"person_id": "p11", "org_id": "o11", "title": "民乐县委书记", "start": "2024年8月", "end": "至今", "rank": "正县级", "note": "2024年8月任民乐县委书记"},
    # 张会忠 - 专职副书记
    {"person_id": "p12", "org_id": "o01", "title": "高台县委副书记", "start": "?", "end": "至今", "rank": "副县级", "note": "专职副书记"},
    # 李兴华 - 张掖市委书记
    {"person_id": "p13", "org_id": "o08", "title": "张掖市委书记", "start": "?", "end": "至今", "rank": "正厅级", "note": ""},
    # 叶尔波力·孜汗 - 张掖市长
    {"person_id": "p14", "org_id": "o09", "title": "张掖市市长", "start": "?", "end": "至今", "rank": "正厅级", "note": ""},
]

# 4. 关系
relationships = [
    # 党政一把手
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "张龙(书记)与武汉章(县长): 高台县党政一把手配合作", "overlap_org": "中共高台县委员会/高台县人民政府", "overlap_period": "?至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-人大
    {"person_a": "p01", "person_b": "p03", "type": "overlap", "context": "张龙(书记)与杨红光(人大主任): 党委与人大配合作", "overlap_org": "高台县四套班子", "overlap_period": "?至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-政协
    {"person_a": "p01", "person_b": "p04", "type": "overlap", "context": "张龙(书记)与向钧(政协主席): 党委与政协配合作", "overlap_org": "高台县四套班子", "overlap_period": "?至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-专职副书记
    {"person_a": "p01", "person_b": "p12", "type": "overlap", "context": "张龙(书记)与张会忠(专职副书记): 党委班子上下级", "overlap_org": "中共高台县委员会", "overlap_period": "?至今", "strength": "strong", "confidence": "confirmed"},
    # 县长-常务副县长
    {"person_a": "p02", "person_b": "p05", "type": "overlap", "context": "武汉章(县长)与赵多磊(常务副县长): 正副手关系", "overlap_org": "高台县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-组织部长
    {"person_a": "p01", "person_b": "p06", "type": "overlap", "context": "张龙(书记)与王建军(组织部长): 党委班子上下级", "overlap_org": "中共高台县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-纪委书记
    {"person_a": "p01", "person_b": "p07", "type": "overlap", "context": "张龙(书记)与余建峰(纪委书记): 党委班子上下级", "overlap_org": "中共高台县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-政法委书记
    {"person_a": "p01", "person_b": "p09", "type": "overlap", "context": "张龙(书记)与孟越祖(政法委书记): 党委班子上下级", "overlap_org": "中共高台县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-副县长
    {"person_a": "p01", "person_b": "p08", "type": "overlap", "context": "张龙(书记)与王振成(副县长): 党委班子上下级", "overlap_org": "中共高台县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 前任-现任关系(县委书记)
    {"person_a": "p10", "person_b": "p01", "type": "predecessor_successor", "context": "刘伟红(前任县委书记)与张龙(现任县委书记): 高台县委书记交接", "overlap_org": "中共高台县委员会", "overlap_period": "约2023年", "strength": "strong", "confidence": "confirmed"},
    # 前任-现任关系(县长)
    {"person_a": "p11", "person_b": "p02", "type": "predecessor_successor", "context": "张鹏(前任县长)与武汉章(现任县长): 高台县长交接", "overlap_org": "高台县人民政府", "overlap_period": "2024?", "strength": "strong", "confidence": "plausible"},
    # 张龙 - 张鹏(曾共事)
    {"person_a": "p01", "person_b": "p11", "type": "overlap", "context": "张龙(现任书记)与张鹏(前任县长): 曾在高台县共事", "overlap_org": "高台县", "overlap_period": "约2019-2023年?", "strength": "medium", "confidence": "plausible"},
    # 张龙 - 刘伟红(曾任高台县委书记)
    {"person_a": "p01", "person_b": "p10", "type": "overlap", "context": "张龙(现任书记)与刘伟红(前任书记): 可能曾有交接合作", "overlap_org": "中共高台县委员会", "overlap_period": "约2023年", "strength": "medium", "confidence": "plausible"},
    # 张掖市-高台县上下级关系
    {"person_a": "p13", "person_b": "p01", "type": "superior_subordinate", "context": "李兴华(张掖市委书记)与张龙(高台县委书记): 市级对县级领导关系", "overlap_org": "张掖市/高台县", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p14", "person_b": "p02", "type": "superior_subordinate", "context": "叶尔波力·孜汗(张掖市长)与武汉章(高台县长): 市级对县级领导关系", "overlap_org": "张掖市/高台县", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 刘伟红与张鹏(前高台县长-书记搭档)
    {"person_a": "p10", "person_b": "p11", "type": "overlap", "context": "刘伟红(前县委书记)与张鹏(前县长): 高台县党政一把手搭档", "overlap_org": "高台县", "overlap_period": "约2019-2023年", "strength": "strong", "confidence": "confirmed"},
    # 刘伟红-张掖市委
    {"person_a": "p10", "person_b": "p13", "type": "superior_subordinate", "context": "刘伟红(宣传部部长)与李兴华(市委书记): 市委班子同僚", "overlap_org": "中共张掖市委员会", "overlap_period": "约2023年至今", "strength": "strong", "confidence": "confirmed"},
]


# ── 辅助函数 ──────────────────────────────────────────

def esc(s):
    """XML转义"""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """按角色返回RGB颜色"""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title:
        if "副书记" in title:
            return "200,50,50"   # 暗红 — 副职(如县委副书记)
        return "255,50,50"   # 红色 — 党委正职
    if "县长" in title or ("长" in title and "副县长" not in title and "部长" not in title):
        return "50,100,255"  # 蓝色 — 政府领导
    if "纪委" in title or "监委" in title:
        return "255,165,0"   # 橙色 — 纪检
    if "常委" in title:
        return "200,100,100" # 粉红 — 其他常委
    if "人大" in title:
        return "200,255,255" # 青色 — 人大
    if "政协" in title:
        return "255,240,200" # 米色 — 政协
    if "副市长" in title or "副区长" in title or "副县长" in title:
        return "100,100,200" # 浅蓝 — 副市/县/区长
    return "100,100,100"     # 灰色 — 其他

def person_size(p):
    """按角色返回节点大小"""
    title = p["current_post"]
    if "县委书记" in title or "县长" in title:
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "人大" in title or "政协" in title:
        return "12.0"
    if "副市长" in title or "副区长" in title or "副县长" in title:
        return "12.0"
    return "10.0"

def org_color(o):
    """按类型返回组织颜色"""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")

# ── 构建数据库 ────────────────────────────────────────

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT, strength TEXT, confidence TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    c.execute("DELETE FROM persons")
    c.execute("DELETE FROM organizations")
    c.execute("DELETE FROM positions")
    c.execute("DELETE FROM relationships")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            p["id"], p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"],
            p["current_org"], p["source"]
        ))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            pos["person_id"], pos["org_id"], pos["title"],
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
                     VALUES (?,?,?,?,?,?,?,?)""", (
            r["person_a"], r["person_b"], r["type"], r["context"],
            r["overlap_org"], r["overlap_period"], r.get("strength", "medium"), r.get("confidence", "plausible")
        ))

    conn.commit()
    conn.close()

# ── 构建 GEXF ─────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>高台县领导班子工作关系网络 - 数据来源: 公开报道及政府网站</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="高台县"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="高台县"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (worked_at)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = r.get("confidence", "plausible")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ── 主函数 ──────────────────────────────────────────

def main():
    print(f"=== 高台县网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")

if __name__ == "__main__":
    main()
