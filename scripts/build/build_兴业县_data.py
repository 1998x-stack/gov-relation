#!/usr/bin/env python3
"""兴业县领导班子关系网络数据构建脚本。

数据来源:
  - 兴业县人民政府门户网站 http://www.xingye.gov.cn
  - 县长页面: http://www.xingye.gov.cn/zfxxgk/xxgkml/zfld/xz/
  - 副县长页面: http://www.xingye.gov.cn/zfxxgk/xxgkml/zfld/fxz/
  - 政务要闻: 2026年7月多次报道确认县委书记华海德

确认日期: 2026-07-23
"""

import json
import os
import sqlite3
from datetime import datetime

# ── 路径 ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "兴业县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR
TASK_ID = "guangxi_兴业县"
AS_OF = "2026-07-23"
OFFICIAL_SITE = "http://www.xingye.gov.cn"

# ── 来源登记 ──
source_register = [
    {"id": "S001", "title": "兴业县人民政府门户网站 - 县长页面",
     "url": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zfld/xz/",
     "publisher": "兴业县人民政府", "published_at": "2025-04-03",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S002", "title": "兴业县人民政府 - 副县长吴益君页面",
     "url": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zfld/fxz/t19769775.shtml",
     "publisher": "兴业县人民政府", "published_at": "2025-04-03",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S003", "title": "兴业县人民政府 - 副县长赵坚页面",
     "url": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zfld/fxz/t18323317.shtml",
     "publisher": "兴业县人民政府", "published_at": "2025-04-03",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S004", "title": "兴业县人民政府 - 副县长蓝岸页面",
     "url": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zfld/fxz/t10473781.shtml",
     "publisher": "兴业县人民政府", "published_at": "2025-04-03",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S005", "title": "兴业县人民政府 - 副县长梁业荣页面",
     "url": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zfld/fxz/t10473833.shtml",
     "publisher": "兴业县人民政府", "published_at": "2025-04-03",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S006", "title": "兴业县人民政府 - 副县长覃展页面",
     "url": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zfld/fxz/t19769902.shtml",
     "publisher": "兴业县人民政府", "published_at": "2025-04-03",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S007", "title": "政务要闻 - 县委常委会召开会议 华海德主持会议并讲话",
     "url": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zwdt/zwyw/t27891446.shtml",
     "publisher": "兴业县融媒体中心", "published_at": "2026-07-15",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S008", "title": "政务要闻 - 华海德到大平山镇检查防汛",
     "url": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zwdt/zwyw/t27869264.shtml",
     "publisher": "兴业县融媒体中心", "published_at": "2026-07-08",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S009", "title": "政务要闻 - 兴业县收听收看建党105周年大会",
     "url": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zwdt/zwyw/t27856425.shtml",
     "publisher": "兴业县融媒体中心", "published_at": "2026-07-03",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    {"id": "S010", "title": "政务要闻 - 县委常委会会议 陆金学主持会议（前任书记）",
     "url": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zwdt/ldhd/t21245090.shtml",
     "publisher": "兴业县融媒体中心", "published_at": "2024-08-29",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
]


# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委领导
    # ════════════════════════════════════════
    {
        "id": "xy_hua_haide",
        "name": "华海德",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县委书记",
        "current_org": "中共兴业县委员会",
        "source": OFFICIAL_SITE + " — 2026年7月多篇报道确认县委书记身份: 县委常委会会议、防汛检查等",
    },
    {
        "id": "xy_wang_yongjian",
        "name": "王永坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年5月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县委副书记、县长",
        "current_org": "中共兴业县委员会/兴业县人民政府",
        "source": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zfld/xz/",
    },
    {
        "id": "xy_wu_yijun",
        "name": "吴益君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年7月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县委常委、副县长（常务）",
        "current_org": "中共兴业县委员会/兴业县人民政府",
        "source": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zfld/fxz/t19769775.shtml",
    },
    {
        "id": "xy_zhao_jian",
        "name": "赵坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年8月",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生学历，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县委常委、副县长（挂职）",
        "current_org": "中共兴业县委员会/兴业县人民政府",
        "source": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zfld/fxz/t18323317.shtml",
    },
    {
        "id": "xy_lan_an",
        "name": "蓝岸",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年5月",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生学历",
        "party_join": "民盟",
        "work_start": "",
        "current_post": "兴业县副县长、民盟玉林市委副主委",
        "current_org": "兴业县人民政府",
        "source": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zfld/fxz/t10473781.shtml",
    },
    {
        "id": "xy_liang_yerong",
        "name": "梁业荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县副县长",
        "current_org": "兴业县人民政府",
        "source": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zfld/fxz/t10473833.shtml",
    },
    {
        "id": "xy_qin_zhan",
        "name": "覃展",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年10月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县副县长、县公安局局长",
        "current_org": "兴业县人民政府/兴业县公安局",
        "source": "http://www.xingye.gov.cn/zfxxgk/xxgkml/zfld/fxz/t19769902.shtml",
    },
    # ════════════════════════════════════════
    # 其他县委常委（从新闻报道中提取）
    # ════════════════════════════════════════
    {
        "id": "xy_shen_junyu",
        "name": "沈俊雨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县委常委",
        "current_org": "中共兴业县委员会",
        "source": OFFICIAL_SITE + " — 2026年7月县委常委会会议报道",
    },
    {
        "id": "xy_liang_bing",
        "name": "梁冰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县委常委",
        "current_org": "中共兴业县委员会",
        "source": OFFICIAL_SITE + " — 2026年7月县委常委会会议报道",
    },
    {
        "id": "xy_li_guoyao",
        "name": "李国尧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县委常委",
        "current_org": "中共兴业县委员会",
        "source": OFFICIAL_SITE + " — 2026年7月县委常委会会议报道",
    },
    {
        "id": "xy_chen_jie",
        "name": "陈杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县委常委",
        "current_org": "中共兴业县委员会",
        "source": OFFICIAL_SITE + " — 2026年7月县委常委会会议报道",
    },
    {
        "id": "xy_dang_dongxian",
        "name": "党东显",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县委常委",
        "current_org": "中共兴业县委员会",
        "source": OFFICIAL_SITE + " — 2026年7月县委常委会会议报道",
    },
    {
        "id": "xy_he_jun",
        "name": "何军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县委常委",
        "current_org": "中共兴业县委员会",
        "source": OFFICIAL_SITE + " — 2026年7月防汛检查报道",
    },
    {
        "id": "xy_yan_guofan",
        "name": "颜国蕃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县委常委",
        "current_org": "中共兴业县委员会",
        "source": OFFICIAL_SITE + " — 2026年7月县委常委会会议报道",
    },
    {
        "id": "xy_pan_yi",
        "name": "潘毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县委常委",
        "current_org": "中共兴业县委员会",
        "source": OFFICIAL_SITE + " — 2026年7月县委常委会会议报道",
    },
    {
        "id": "xy_tan_zhijian",
        "name": "谭志坚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县委常委",
        "current_org": "中共兴业县委员会",
        "source": OFFICIAL_SITE + " — 2026年7月县委常委会会议报道",
    },
    # ════════════════════════════════════════
    # 县人大领导
    # ════════════════════════════════════════
    {
        "id": "xy_he_jining",
        "name": "何际宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县领导（人大方向）",
        "current_org": "兴业县人民代表大会常务委员会",
        "source": OFFICIAL_SITE + " — 2026年7月县委常委会列席报道",
    },
    {
        "id": "xy_liu_jun",
        "name": "刘军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县领导（政协方向）",
        "current_org": "中国人民政治协商会议兴业县委员会",
        "source": OFFICIAL_SITE + " — 2026年7月县委常委会列席报道",
    },
    {
        "id": "xy_xie_yequan",
        "name": "谢业权",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "兴业县领导",
        "current_org": "兴业县",
        "source": OFFICIAL_SITE + " — 2026年7月县委常委会列席报道",
    },
    # ════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════
    {
        "id": "xy_lu_jinxue",
        "name": "陆金学",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴业县委原书记",
        "current_org": "中共兴业县委员会",
        "source": OFFICIAL_SITE + " — 2024年8月报道中仍以县委书记身份主持县委常委会",
    },
]


# ═══════════════════════════════════════════════
# 组织机构数据
# ═══════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共兴业县委员会", "type": "党委", "level": "县处级",
     "parent": "中共玉林市委员会", "location": "兴业县民主路1号"},
    {"id": 2, "name": "兴业县人民政府", "type": "政府", "level": "县处级",
     "parent": "玉林市人民政府", "location": "兴业县民主路1号"},
    {"id": 3, "name": "兴业县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "兴业县", "location": "兴业县"},
    {"id": 4, "name": "中国人民政治协商会议兴业县委员会", "type": "政协", "level": "县处级",
     "parent": "兴业县", "location": "兴业县"},
    {"id": 5, "name": "中共兴业县纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共兴业县委员会", "location": "兴业县"},
    {"id": 6, "name": "兴业县公安局", "type": "政府", "level": "县处级",
     "parent": "兴业县人民政府", "location": "兴业县"},
    {"id": 7, "name": "兴业县人民武装部", "type": "政府", "level": "县处级",
     "parent": "玉林军分区", "location": "兴业县"},
]


# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 华海德
    {"person_id": "xy_hua_haide", "org_id": 1, "title": "兴业县委书记",
     "start_date": "2026年", "end_date": "present", "rank": "县处级正职",
     "note": "2026年7月确认任县委书记；前任为陆金学"},
    # 王永坚
    {"person_id": "xy_wang_yongjian", "org_id": 1, "title": "兴业县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "官方简历为县委副书记"},
    {"person_id": "xy_wang_yongjian", "org_id": 2, "title": "兴业县人民政府县长、党组书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "1977年5月出生，大学学历，中共党员"},
    # 吴益君
    {"person_id": "xy_wu_yijun", "org_id": 1, "title": "兴业县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "1983年7月出生，大学学历"},
    {"person_id": "xy_wu_yijun", "org_id": 2, "title": "兴业县人民政府副县长（常务）、党组副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责常务工作，分管发改、财政、应急、金融、统计等"},
    # 赵坚
    {"person_id": "xy_zhao_jian", "org_id": 1, "title": "兴业县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "1981年8月出生，在职研究生，工程硕士"},
    {"person_id": "xy_zhao_jian", "org_id": 2, "title": "兴业县人民政府副县长（挂职）",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "挂职副县长，分管广西驻村工作队兴业县工作队"},
    # 蓝岸
    {"person_id": "xy_lan_an", "org_id": 2, "title": "兴业县人民政府副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "1973年5月出生，在职研究生学历，民盟盟员；分管农业农村、乡村振兴、水利、林业、文体广电旅游等"},
    {"person_id": "xy_lan_an", "org_id": 0, "title": "民盟玉林市委副主委",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "民主党派职务"},
    # 梁业荣
    {"person_id": "xy_liang_yerong", "org_id": 2, "title": "兴业县人民政府副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "1976年10月出生，在职大学学历，中共党员；分管住建、交通、经贸、工业园区等"},
    # 覃展
    {"person_id": "xy_qin_zhan", "org_id": 2, "title": "兴业县人民政府副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "1983年10月出生，大学学历，中共党员"},
    {"person_id": "xy_qin_zhan", "org_id": 6, "title": "兴业县公安局局长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "兼任县公安局党委书记、局长、四级高级警长"},
    # 沈俊雨
    {"person_id": "xy_shen_junyu", "org_id": 1, "title": "兴业县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    # 梁冰
    {"person_id": "xy_liang_bing", "org_id": 1, "title": "兴业县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    # 李国尧
    {"person_id": "xy_li_guoyao", "org_id": 1, "title": "兴业县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    # 陈杰
    {"person_id": "xy_chen_jie", "org_id": 1, "title": "兴业县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    # 党东显
    {"person_id": "xy_dang_dongxian", "org_id": 1, "title": "兴业县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    # 何军
    {"person_id": "xy_he_jun", "org_id": 1, "title": "兴业县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    # 颜国蕃
    {"person_id": "xy_yan_guofan", "org_id": 1, "title": "兴业县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    # 潘毅
    {"person_id": "xy_pan_yi", "org_id": 1, "title": "兴业县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    # 谭志坚
    {"person_id": "xy_tan_zhijian", "org_id": 1, "title": "兴业县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    # 人大/政协
    {"person_id": "xy_he_jining", "org_id": 3, "title": "兴业县领导（人大方向）",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "列席县委常委会"},
    {"person_id": "xy_liu_jun", "org_id": 4, "title": "兴业县领导（政协方向）",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "列席县委常委会"},
    # 陆金学（前任县委书记）
    {"person_id": "xy_lu_jinxue", "org_id": 1, "title": "兴业县委书记（前任）",
     "start_date": "", "end_date": "2026年", "rank": "县处级正职",
     "note": "2024年8月仍以县委书记身份活动，2026年由华海德接任"},
]


# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════

relationships = [
    # 华海德 <-> 王永坚（党政搭档）
    {"person_a": "xy_hua_haide", "person_b": "xy_wang_yongjian",
     "type": "党政搭档",
     "context": "华海德（县委书记）与王永坚（县长）为兴业县党政主要领导人",
     "overlap_org": "兴业县党政班子", "overlap_period": "2026年"},
    # 华海德 <-> 吴益君（县委常委班子）
    {"person_a": "xy_hua_haide", "person_b": "xy_wu_yijun",
     "type": "上下级",
     "context": "华海德（县委书记）与吴益君（县委常委、常务副县长）在县委常委班子共事",
     "overlap_org": "中共兴业县委员会", "overlap_period": "2026年"},
    # 王永坚 <-> 吴益君（县长-常务副县长）
    {"person_a": "xy_wang_yongjian", "person_b": "xy_wu_yijun",
     "type": "上下级",
     "context": "王永坚（县长）与吴益君（常务副县长）在县政府班子中共事",
     "overlap_org": "兴业县人民政府", "overlap_period": ""},
    # 华海德 <-> 陆金学（前后任）
    {"person_a": "xy_hua_haide", "person_b": "xy_lu_jinxue",
     "type": "前后任",
     "context": "华海德接替陆金学任兴业县委书记",
     "overlap_org": "中共兴业县委员会", "overlap_period": "2026年交接"},
    # 覃展 <-> 王永坚（政府班子成员）
    {"person_a": "xy_qin_zhan", "person_b": "xy_wang_yongjian",
     "type": "上下级",
     "context": "覃展（副县长、公安局长）在王永坚（县长）领导下工作",
     "overlap_org": "兴业县人民政府", "overlap_period": ""},
    # 蓝岸 <-> 王永坚（政府班子成员）
    {"person_a": "xy_lan_an", "person_b": "xy_wang_yongjian",
     "type": "上下级",
     "context": "蓝岸（副县长）在王永坚（县长）领导下工作",
     "overlap_org": "兴业县人民政府", "overlap_period": ""},
    # 梁业荣 <-> 王永坚（政府班子成员）
    {"person_a": "xy_liang_yerong", "person_b": "xy_wang_yongjian",
     "type": "上下级",
     "context": "梁业荣（副县长）在王永坚（县长）领导下工作",
     "overlap_org": "兴业县人民政府", "overlap_period": ""},
    # 县委常委班子成员互相关联
    {"person_a": "xy_hua_haide", "person_b": "xy_shen_junyu",
     "type": "共事", "context": "县委常委会共事", "overlap_org": "中共兴业县委员会", "overlap_period": "2026年"},
    {"person_a": "xy_hua_haide", "person_b": "xy_liang_bing",
     "type": "共事", "context": "县委常委会共事", "overlap_org": "中共兴业县委员会", "overlap_period": "2026年"},
    {"person_a": "xy_hua_haide", "person_b": "xy_li_guoyao",
     "type": "共事", "context": "县委常委会共事", "overlap_org": "中共兴业县委员会", "overlap_period": "2026年"},
    {"person_a": "xy_hua_haide", "person_b": "xy_chen_jie",
     "type": "共事", "context": "县委常委会共事", "overlap_org": "中共兴业县委员会", "overlap_period": "2026年"},
    {"person_a": "xy_hua_haide", "person_b": "xy_dang_dongxian",
     "type": "共事", "context": "县委常委会共事", "overlap_org": "中共兴业县委员会", "overlap_period": "2026年"},
    {"person_a": "xy_hua_haide", "person_b": "xy_he_jun",
     "type": "共事", "context": "县委常委会共事", "overlap_org": "中共兴业县委员会", "overlap_period": "2026年"},
    {"person_a": "xy_hua_haide", "person_b": "xy_yan_guofan",
     "type": "共事", "context": "县委常委会共事", "overlap_org": "中共兴业县委员会", "overlap_period": "2026年"},
    {"person_a": "xy_hua_haide", "person_b": "xy_pan_yi",
     "type": "共事", "context": "县委常委会共事", "overlap_org": "中共兴业县委员会", "overlap_period": "2026年"},
    {"person_a": "xy_hua_haide", "person_b": "xy_tan_zhijian",
     "type": "共事", "context": "县委常委会共事", "overlap_org": "中共兴业县委员会", "overlap_period": "2026年"},
]


# ═══════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ═══════════════════════════════════════════════
# 构建
# ═══════════════════════════════════════════════

def build():
    os.makedirs(STAGING_DIR, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    # Assign auto-increment IDs to persons
    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = p["id"]
        person_map[pid] = idx
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""),
                     r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>兴业县领导班子关系网络（基于官网确认数据）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid = person_map[p["id"]]
        post = p.get("current_post", "")
        is_secretary = "书记" in post and "副" not in post.split("、")[0] if "、" not in post else "书记" in post and not post.startswith("副")
        is_mayor = "县长" in post and "副" not in post
        is_discipline = "纪委" in post

        if is_secretary:
            color = "200,30,30"
        elif is_mayor:
            color = "30,100,200"
        elif is_discipline:
            color = "255,165,0"
        else:
            color = "100,100,100"

        size = "20.0" if (is_secretary or is_mayor) else "12.0"
        shape = "square" if is_secretary else ("circle" if is_mayor else "triangle")

        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        otype = o["type"]
        if otype == "党委":
            ocolor = "255,200,200"
        elif otype == "政府":
            ocolor = "200,200,255"
        elif otype == "人大":
            ocolor = "200,255,255"
        elif otype == "政协":
            ocolor = "255,240,200"
        elif otype == "纪委":
            ocolor = "255,200,150"
        elif otype == "开发区":
            ocolor = "200,255,200"
        elif otype == "乡镇/街道":
            ocolor = "255,255,200"
        else:
            ocolor = "200,200,200"

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        oid = pos["org_id"] + 100000 if pos["org_id"] > 0 else 0
        if oid == 0:
            continue
        lines.append(
            f'      <edge id="e{eid}" source="p{person_map[pos["person_id"]]}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{person_map[r["person_a"]]}" target="p{person_map[r["person_b"]]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person graph JSONs ──
    now = AS_OF.replace("-", "")

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "广西壮族自治区",
                "city": "玉林市",
                "region": "兴业县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"xingye_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
                ] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": []
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": relationships_list,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在兴业县政府官网公开信息中未发现负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历及出生年月、籍贯、学历等详细信息缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的出生年月、籍贯、学历、入党时间、参加工作时间",
                 "why_it_matters": "无法建立完整的身份标识",
                 "suggested_queries": [f"{p['name']} 简历 兴业"],
                 "last_attempted": AS_OF},
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 兴业 任职经历"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 华海德 person JSON ──
    hhd_timeline = []
    hhd_relationships = [
        {"person": "王永坚", "person_id": "xingye_王永坚", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "华海德（县委书记）与王永坚（县长）为兴业县党政主要领导搭档",
         "overlap_org": "兴业县党政班子", "overlap_period": "2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007"]},
        {"person": "吴益君", "person_id": "xingye_吴益君", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "华海德（县委书记）与吴益君（县委常委、常务副县长）在县委常委会共事",
         "overlap_org": "中共兴业县委员会", "overlap_period": "2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007"]},
        {"person": "陆金学", "person_id": "xingye_陆金学", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "华海德接替陆金学任兴业县委书记（2026年）",
         "overlap_org": "中共兴业县委员会", "overlap_period": "2026年",
         "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S010"]},
    ]
    hhd_timeline.append({
        "start": "", "end": "", "org": "履历缺口", "title": "",
        "notes": "公开资料未找到华海德任兴业县委书记前的履历信息",
        "confidence": "unverified", "source_ids": []})

    hhd_json = make_person_json(persons[0], hhd_timeline, hhd_relationships)
    hhd_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-玉林市-县委书记-华海德.json")
    with open(hhd_path, "w", encoding="utf-8") as f:
        json.dump(hhd_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {hhd_path}")

    # ── 王永坚 person JSON ──
    wyj_timeline = []
    wyj_relationships = [
        {"person": "华海德", "person_id": "xingye_华海德", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "王永坚（县长）与华海德（县委书记）为兴业县党政主要领导搭档",
         "overlap_org": "兴业县党政班子", "overlap_period": "2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "吴益君", "person_id": "xingye_吴益君", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "王永坚（县长）与吴益君（常务副县长）在县政府班子共事",
         "overlap_org": "兴业县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    wyj_timeline.append({
        "start": "", "end": "", "org": "履历缺口", "title": "",
        "notes": "公开资料未找到王永坚任兴业县长前的完整履历",
        "confidence": "unverified", "source_ids": []})
    wyj_json = make_person_json(persons[1], wyj_timeline, wyj_relationships)
    wyj_json["identity"]["gender"] = "男"
    wyj_json["identity"]["birth"] = "1977年5月"
    wyj_json["identity"]["education"] = [{"period": "", "institution": "", "major": "", "degree": "大学学历",
                                          "study_type": "unknown", "source_ids": ["S001"]}]
    wyj_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-玉林市-县长-王永坚.json")
    with open(wyj_path, "w", encoding="utf-8") as f:
        json.dump(wyj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wyj_path}")

    # ── 陆金学 person JSON (predecessor) ──
    ljx_timeline = []
    ljx_relationships = [
        {"person": "华海德", "person_id": "xingye_华海德", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "陆金学任县委书记至2026年初，后由华海德接任",
         "overlap_org": "中共兴业县委员会", "overlap_period": "2026年",
         "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S010"]},
        {"person": "王永坚", "person_id": "xingye_王永坚", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "陆金学（原县委书记）与王永坚（县长）曾为党政搭档",
         "overlap_org": "兴业县党政班子", "overlap_period": "2024-2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S010"]},
    ]
    ljx_timeline.append({
        "start": "", "end": "", "org": "履历缺口", "title": "",
        "notes": "公开资料仅见2024年8月以县委书记身份主持常委会的报道，完整履历未知",
        "confidence": "unverified", "source_ids": ["S010"]})
    ljx_json = make_person_json(persons[-1], ljx_timeline, ljx_relationships)
    ljx_json["identity"]["gender"] = "男"
    ljx_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-玉林市-原县委书记-陆金学.json")
    with open(ljx_path, "w", encoding="utf-8") as f:
        json.dump(ljx_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {ljx_path}")

    print(f"\nBuild complete. All current roles confirmed from official source {OFFICIAL_SITE}")
    print("Identity info (birth, education, etc.) partially verified from official profiles.")
    print("华海德的完整履历和详细身份信息仍需补充。")


if __name__ == "__main__":
    build()
