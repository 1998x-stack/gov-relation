#!/usr/bin/env python3
"""
镇原县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Zhenyuan County leadership network.

Level: 县
Province: 甘肃省
Parent city: 庆阳市
Region: 镇原县
Targets: 县委书记 & 县长

Research Sources:
- www.gszy.gov.cn (镇原县人民政府官网 领导之窗, accessed 2026-07-22)
- 镇原县新闻中心 (www.gszy.gov.cn/xwzx/zyyw, accessed 2026-07-22)
- 庆阳市领导网络 (已有研究数据)

Confirmed officeholders (as of 2026-07-22, from www.gszy.gov.cn):
- 县委书记: 罗睿
- 县委副书记、县政府党组书记、县长: 夏成
- 县委副书记: 黄沐
- 县委常委、县政府党组副书记、常务副县长: 左宗琛
- 县委常委、县纪委书记、县监察委员会主任: 张彦宏
- 县委常委、县委组织部部长: 梁钧洲
- 县委常委、宣传部部长: 杨俊杰
- 县委常委、县委政法委书记，县公安局党委书记、局长: 王涛
- 县委常委、人民武装部上校部长: 程世平
- 县委常委、县政府党组成员、副县长: 张海东
- 县委常委、县政府党组成员、副县长: 杨海
- 县人大常委会党组书记、主任: 巨文程
- 县人大常委会党组副书记、副主任、县总工会主席: 路军莲

Research Date: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "镇原县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "镇原县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── DATA ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": "p01",
        "name": "罗睿",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "镇原县委书记",
        "current_org": "中共镇原县委员会",
        "source": "www.gszy.gov.cn (领导之窗); 镇原新闻2026-07-01(罗睿主持县委常委会会议)",
        "person_id": "zhenyuan_luo_rui"
    },
    {
        "id": "p02",
        "name": "夏成",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "镇原县委副书记、县政府党组书记、县长",
        "current_org": "镇原县人民政府",
        "source": "www.gszy.gov.cn (领导之窗); 镇原新闻2026-07-22(夏成主持召开县规委会)",
        "person_id": "zhenyuan_xia_cheng"
    },
    # ════════════════════════════════════════
    # Deputy Leaders (县委班子 + 县政府)
    # ════════════════════════════════════════
    {
        "id": "p03",
        "name": "黄沐",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "镇原县委副书记",
        "current_org": "中共镇原县委员会",
        "source": "www.gszy.gov.cn (领导之窗)",
        "person_id": "zhenyuan_huang_mu"
    },
    {
        "id": "p04",
        "name": "左宗琛",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "镇原县委常委、县政府党组副书记、常务副县长",
        "current_org": "镇原县人民政府",
        "source": "www.gszy.gov.cn (领导之窗)",
        "person_id": "zhenyuan_zuo_zongchen"
    },
    {
        "id": "p05",
        "name": "张彦宏",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "镇原县委常委、县纪委书记、县监察委员会主任",
        "current_org": "中共镇原县纪律检查委员会",
        "source": "www.gszy.gov.cn (领导之窗)",
        "person_id": "zhenyuan_zhang_yanhong"
    },
    {
        "id": "p06",
        "name": "梁钧洲",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "镇原县委常委、县委组织部部长",
        "current_org": "中共镇原县委员会组织部",
        "source": "www.gszy.gov.cn (领导之窗)",
        "person_id": "zhenyuan_liang_junzhou"
    },
    {
        "id": "p07",
        "name": "杨俊杰",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "镇原县委常委、宣传部部长",
        "current_org": "中共镇原县委员会宣传部",
        "source": "www.gszy.gov.cn (领导之窗)",
        "person_id": "zhenyuan_yang_junjie"
    },
    {
        "id": "p08",
        "name": "王涛",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "镇原县委常委、县委政法委书记, 县公安局党委书记、局长",
        "current_org": "中共镇原县委员会政法委员会",
        "source": "www.gszy.gov.cn (领导之窗)",
        "person_id": "zhenyuan_wang_tao"
    },
    {
        "id": "p09",
        "name": "程世平",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "镇原县委常委、人民武装部上校部长",
        "current_org": "镇原县人民武装部",
        "source": "www.gszy.gov.cn (领导之窗)",
        "person_id": "zhenyuan_cheng_shiping"
    },
    {
        "id": "p10",
        "name": "张海东",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "镇原县委常委、县政府党组成员、副县长",
        "current_org": "镇原县人民政府",
        "source": "www.gszy.gov.cn (领导之窗)",
        "person_id": "zhenyuan_zhang_haidong"
    },
    {
        "id": "p11",
        "name": "杨海",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "镇原县委常委、县政府党组成员、副县长",
        "current_org": "镇原县人民政府",
        "source": "www.gszy.gov.cn (领导之窗)",
        "person_id": "zhenyuan_yang_hai"
    },
    # ════════════════════════════════════════
    # 人大 (People's Congress)
    # ════════════════════════════════════════
    {
        "id": "p12",
        "name": "巨文程",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "镇原县人大常委会党组书记、主任",
        "current_org": "镇原县人民代表大会常务委员会",
        "source": "www.gszy.gov.cn (领导之窗)",
        "person_id": "zhenyuan_ju_wencheng"
    },
    {
        "id": "p13",
        "name": "路军莲",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "镇原县人大常委会党组副书记、副主任、县总工会主席",
        "current_org": "镇原县人民代表大会常务委员会",
        "source": "www.gszy.gov.cn (领导之窗)",
        "person_id": "zhenyuan_lu_junlian"
    },
    # ════════════════════════════════════════
    # Predecessors (placeholder)
    # ════════════════════════════════════════
    {
        "id": "p14",
        "name": "罗睿（前任待确认）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（镇原县前任县委书记）",
        "current_org": "待查",
        "source": "待查 — 需后续搜索罗睿前任信息",
        "person_id": "zhenyuan_predecessor_secretary"
    },
    {
        "id": "p15",
        "name": "夏成（前任待确认）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（镇原县前任县长）",
        "current_org": "待查",
        "source": "待查 — 需后续搜索夏成前任信息",
        "person_id": "zhenyuan_predecessor_mayor"
    },
]

# 2. Organizations
organizations = [
    {"id": "o01", "name": "中共镇原县委员会", "type": "党委", "level": "县处级", "parent": "中共庆阳市委员会", "location": "甘肃省庆阳市镇原县城关镇"},
    {"id": "o02", "name": "镇原县人民政府", "type": "政府", "level": "县处级", "parent": "庆阳市人民政府", "location": "甘肃省庆阳市镇原县城关镇"},
    {"id": "o03", "name": "镇原县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "镇原县", "location": "甘肃省庆阳市镇原县城关镇"},
    {"id": "o04", "name": "中国人民政治协商会议镇原县委员会", "type": "政协", "level": "县处级", "parent": "镇原县", "location": "甘肃省庆阳市镇原县城关镇"},
    {"id": "o05", "name": "中共镇原县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共镇原县委员会", "location": "甘肃省庆阳市镇原县城关镇"},
    {"id": "o06", "name": "中共镇原县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共镇原县委员会", "location": "甘肃省庆阳市镇原县城关镇"},
    {"id": "o07", "name": "中共镇原县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共镇原县委员会", "location": "甘肃省庆阳市镇原县城关镇"},
    {"id": "o08", "name": "中共镇原县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共镇原县委员会", "location": "甘肃省庆阳市镇原县城关镇"},
    {"id": "o09", "name": "镇原县公安局", "type": "政府", "level": "县处级", "parent": "镇原县人民政府", "location": "甘肃省庆阳市镇原县城关镇"},
    {"id": "o10", "name": "镇原县人民武装部", "type": "事业单位", "level": "县处级", "parent": "庆阳军分区", "location": "甘肃省庆阳市镇原县城关镇"},
    {"id": "o11", "name": "中共庆阳市委员会", "type": "党委", "level": "地厅级", "parent": "中共甘肃省委员会", "location": "甘肃省庆阳市西峰区"},
    {"id": "o12", "name": "庆阳市人民政府", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府", "location": "甘肃省庆阳市西峰区"},
]

# 3. Positions
positions = [
    # 罗睿 (p01)
    {"person_id": "p01", "org_id": "o01", "title": "镇原县委书记", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持县委全面工作。2026年7月1日、7月14日主持县委常委会会议；2026年7月委托暗访防汛工作。当前在任。"},
    # 夏成 (p02)
    {"person_id": "p02", "org_id": "o02", "title": "镇原县人民政府县长", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持县政府全面工作。2026年7月22日主持召开县国土空间规划委员会第二次会议。2026年7月督查调研常态化帮扶、防汛减灾等工作。"},
    {"person_id": "p02", "org_id": "o01", "title": "镇原县委副书记", "start": "待查", "end": "至今", "rank": "副处级", "note": "兼任县政府党组书记"},
    # 黄沐 (p03)
    {"person_id": "p03", "org_id": "o01", "title": "镇原县委副书记", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委专职副书记"},
    # 左宗琛 (p04)
    {"person_id": "p04", "org_id": "o02", "title": "镇原县委常委、常务副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县政府党组副书记，协助县长处理县政府日常工作"},
    {"person_id": "p04", "org_id": "o01", "title": "镇原县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委会成员"},
    # 张彦宏 (p05)
    {"person_id": "p05", "org_id": "o05", "title": "镇原县纪委书记、县监委主任", "start": "待查", "end": "至今", "rank": "副处级", "note": "主持县纪委监委全面工作"},
    {"person_id": "p05", "org_id": "o01", "title": "镇原县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 梁钧洲 (p06)
    {"person_id": "p06", "org_id": "o06", "title": "镇原县委常委、组织部部长", "start": "待查", "end": "至今", "rank": "副处级", "note": "主持县委组织部全面工作"},
    {"person_id": "p06", "org_id": "o01", "title": "镇原县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 杨俊杰 (p07)
    {"person_id": "p07", "org_id": "o07", "title": "镇原县委常委、宣传部部长", "start": "待查", "end": "至今", "rank": "副处级", "note": "主持县委宣传部全面工作"},
    {"person_id": "p07", "org_id": "o01", "title": "镇原县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 王涛 (p08)
    {"person_id": "p08", "org_id": "o08", "title": "镇原县委常委、政法委书记", "start": "待查", "end": "至今", "rank": "副处级", "note": "主持县委政法委全面工作"},
    {"person_id": "p08", "org_id": "o09", "title": "镇原县公安局党委书记、局长", "start": "待查", "end": "至今", "rank": "副处级", "note": "兼任县公安局局长"},
    {"person_id": "p08", "org_id": "o01", "title": "镇原县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 程世平 (p09)
    {"person_id": "p09", "org_id": "o10", "title": "镇原县人武部上校部长", "start": "待查", "end": "至今", "rank": "副处级", "note": "人武部部长"},
    {"person_id": "p09", "org_id": "o01", "title": "镇原县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 张海东 (p10)
    {"person_id": "p10", "org_id": "o02", "title": "镇原县委常委、副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": "p10", "org_id": "o01", "title": "镇原县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 杨海 (p11)
    {"person_id": "p11", "org_id": "o02", "title": "镇原县委常委、副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": "p11", "org_id": "o01", "title": "镇原县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 巨文程 (p12)
    {"person_id": "p12", "org_id": "o03", "title": "镇原县人大常委会主任", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持县人大常委会全面工作"},
    # 路军莲 (p13)
    {"person_id": "p13", "org_id": "o03", "title": "镇原县人大常委会副主任", "start": "待查", "end": "至今", "rank": "副处级", "note": "党组副书记、县总工会主席"},
    # 前任书记占位 (p14)
    {"person_id": "p14", "org_id": "o01", "title": "镇原县前任县委书记", "start": "待查", "end": "待查", "rank": "正处级", "note": "罗睿的前任 — 待识别"},
    # 前任县长占位 (p15)
    {"person_id": "p15", "org_id": "o02", "title": "镇原县前任县长", "start": "待查", "end": "待查", "rank": "正处级", "note": "夏成的前任 — 待识别"},
]

# 4. Relationships
relationships = [
    # 现任班子核心关系
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "罗睿(书记)与夏成(县长): 镇原县党政一把手配合", "overlap_org": "中共镇原县委员会/镇原县人民政府", "overlap_period": "当前在任", "strength": "strong", "confidence": "confirmed"},
    # 书记-副书记
    {"person_a": "p01", "person_b": "p03", "type": "overlap", "context": "罗睿(书记)与黄沐(副书记): 县委书记与专职副书记工作配合", "overlap_org": "中共镇原县委员会", "overlap_period": "当前在任", "strength": "strong", "confidence": "confirmed"},
    # 县长-常务副县长
    {"person_a": "p02", "person_b": "p04", "type": "overlap", "context": "夏成(县长)与左宗琛(常务副县长): 县政府正副职配合", "overlap_org": "镇原县人民政府", "overlap_period": "当前在任", "strength": "strong", "confidence": "confirmed"},
    # 县委常委会成员关系
    {"person_a": "p01", "person_b": "p04", "type": "overlap", "context": "罗睿(书记)与左宗琛(常委、常务副县长): 县委常委会共事", "overlap_org": "中共镇原县委员会", "overlap_period": "当前在任", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p05", "type": "overlap", "context": "罗睿(书记)与张彦宏(纪委书记): 县委常委会共事", "overlap_org": "中共镇原县委员会", "overlap_period": "当前在任", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p06", "type": "overlap", "context": "罗睿(书记)与梁钧洲(组织部长): 县委常委会共事", "overlap_org": "中共镇原县委员会", "overlap_period": "当前在任", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p07", "type": "overlap", "context": "罗睿(书记)与杨俊杰(宣传部长): 县委常委会共事", "overlap_org": "中共镇原县委员会", "overlap_period": "当前在任", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p08", "type": "overlap", "context": "罗睿(书记)与王涛(政法委书记): 县委常委会共事", "overlap_org": "中共镇原县委员会", "overlap_period": "当前在任", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p10", "type": "overlap", "context": "罗睿(书记)与张海东(副县长): 县委常委会共事", "overlap_org": "中共镇原县委员会", "overlap_period": "当前在任", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p11", "type": "overlap", "context": "罗睿(书记)与杨海(副县长): 县委常委会共事", "overlap_org": "中共镇原县委员会", "overlap_period": "当前在任", "strength": "medium", "confidence": "confirmed"},
    # 人大-县委关系
    {"person_a": "p01", "person_b": "p12", "type": "overlap", "context": "罗睿(书记)与巨文程(人大主任): 县委-人大配合", "overlap_org": "镇原县", "overlap_period": "当前在任", "strength": "medium", "confidence": "confirmed"},
    # 上级领导关系 — 庆阳市领导
    {"person_a": "p01", "person_b": "p02", "type": "same_system", "context": "镇原县受庆阳市领导管理", "overlap_org": "庆阳市/镇原县", "overlap_period": "当前", "strength": "medium", "confidence": "confirmed"},
]

# ── Helper Functions ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return RGB color string based on current_post."""
    title = p["current_post"]
    if "县委书记" in title or ("书记" in title and "纪委" not in title and "人大" not in title and "政协" not in title):
        return "255,50,50"    # Red — Party Secretary
    if "县长" in title and ("副书记" in title or "党组书记" in title):
        return "50,100,255"   # Blue — County Mayor
    if "县长" in title:
        return "50,100,255"   # Blue — Government head
    if "纪委" in title or "监委" in title:
        return "255,165,0"    # Orange — Discipline
    if "副书记" in title:
        return "200,50,50"    # Dark red — Deputy Secretary
    if "常委" in title and "副县长" in title:
        return "100,100,200"  # Light blue — Deputy Mayor (常委+副县长)
    if "常委" in title:
        return "200,100,100"  # Pink — Other Standing Committee
    if "副县长" in title:
        return "100,100,200"  # Light blue — Deputy Mayor
    if "人大" in title and "主任" in title:
        return "200,255,255"  # Cyan — People's Congress
    if "人大" in title:
        return "200,255,255"  # Cyan — People's Congress
    if "政协" in title:
        return "255,240,200"  # Cream — CPPCC
    return "100,100,100"      # Grey — Other

def person_size(p):
    """Return node size based on role."""
    title = p["current_post"]
    if "县委书记" in title or "人大主任" in title or "政协主席" in title:
        return "20.0"
    if "县长" in title and ("副书记" in title or "党组书记" in title):
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副县长" in title:
        return "12.0"
    if "人大" in title or "政协" in title:
        return "12.0"
    return "10.0"

def org_color(o):
    """Return RGB color string based on org type."""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "事业单位": "220,220,220",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")

# ── Build Database ──

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
        overlap_org TEXT, overlap_period TEXT,
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
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (
            r["person_a"], r["person_b"], r["type"], r["context"],
            r["overlap_org"], r["overlap_period"]
        ))

    conn.commit()
    conn.close()

# ── Build GEXF ──

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>镇原县领导班子工作关系网络 - 数据来源: 镇原县人民政府官网(www.gszy.gov.cn)及公开报道</description>')
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
        lines.append('          <attvalue for="3" value="镇原县"/>')
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
        lines.append('          <attvalue for="3" value="镇原县"/>')
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

# ── Main ──

def main():
    print(f"=== 镇原县网络数据构建 ===")
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
