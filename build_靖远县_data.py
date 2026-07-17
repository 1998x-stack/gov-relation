#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 靖远县 (Jingyuan County, Gansu Province).

Task: gansu_靖远县 — 县委书记 & 县长
Province: 甘肃省
Parent city: 白银市
Region: 靖远县
Level: 县
Research date: 2026-07-17
Model intent: iagent

Confirmed officeholders (as of 2026-07-17, from www.jingyuan.gov.cn):
- 县委书记/县长: 李晓清 (serves as both party secretary and county mayor)
- 县人大常委会主任: 王有儒
- 县政协主席: 曹榕 (主席候选人, July 2026 article)
- 县政协原主席: 刘丽春

县委领导 (partial from news reports):
- 马金栋 (县委常委, frequently accompanies 李晓清 on inspections)
- 曹怀睿 (县委常委, appears in 巡察工作会议)
- 马保景 (县委常委, appears in 巡察工作会议)
- 苟三海 (县领导, Feb 2026 safety inspection)
- 马斌 (县领导, 枸杞洽谈会 July 2026)
- 马娇燕 (县领导, 枸杞洽谈会)
- 陈良 (县领导, 枸杞洽谈会)
- 安清民 (县领导, 枸杞洽谈会)
- 张今朝 (县领导, 枸杞洽谈会)
- 柴立刚 (县领导, 枸杞洽谈会)
- 吴晓兰 (副县长, 人大常委会 July 2026)
- 高兴明 (县人民检察院检察长)
- 李敬珣 (副县长, 枸杞产业推介 July 2026)

人大常委会:
- 王兴弟 (县人大常委会副主任)
- 陈瑜山 (县人大常委会副主任)
- 罗爱民 (县人大常委会副主任)
- 吴晓英 (县人大常委会副主任)
- 刘兴贤 (县人大常委会副主任候选人)

Key Note: 李晓清 serves concurrently as party secretary AND county mayor — a dual role.
Previously served as 县委副书记、县长 (Feb 2026 article).
Predecessor as 县委书记 is unclear — may have succeeded 许伟民 or another official.
Predecessor as 县长 also unclear from available sources.

Sources:
- www.jingyuan.gov.cn (official website, accessed 2026-07-17)
- Baidu Baike page for 靖远县 (political leadership table, accessed 2026-07-17)
- 靖远县融媒体中心 news articles on www.jingyuan.gov.cn
"""

import sqlite3
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in SCRIPT_DIR:
    STAGING = SCRIPT_DIR
else:
    GOV_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STAGING = os.path.join(GOV_ROOT, "data", "tmp", "gansu_靖远县")
DB_PATH = os.path.join(STAGING, "靖远县_network.db")
GEXF_PATH = os.path.join(STAGING, "靖远县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

TODAY = datetime.now().strftime("%Y-%m-%d")

# ══════════════════════════════════════════════════════════════════════════
# RESEARCH DATA
# ══════════════════════════════════════════════════════════════════════════

persons = [
    # ═══ Core Leader: 县委书记/县长 ═══
    {
        "id": "jingyuan_li_xiaoqing",
        "name": "李晓清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县委书记、县长",
        "current_org": "中共靖远县委员会、靖远县人民政府",
        "source": "www.jingyuan.gov.cn (靖远要闻 2026-07-17, 2026-02-14); Baidu Baike 靖远县条目 (政治表格)",
        "notes": "李晓清同时担任县委书记和县长（一肩挑）。2026年2月以县委副书记、县长身份检查安全生产工作。2026年7月以县委书记、县委巡察工作领导小组组长身份主持会议。履历详情待查。",
        "confidence": "confirmed",
    },

    # ═══ 县人大常委会主任 ═══
    {
        "id": "jingyuan_wang_youru",
        "name": "王有儒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县人大常委会主任",
        "current_org": "靖远县人民代表大会常务委员会",
        "source": "Baidu Baike 靖远县条目 (政治表格); www.jingyuan.gov.cn (人大常委会会议 2026-07-17; 枸杞洽谈会 2026-07-12)",
        "notes": "担任县人大常委会主任，经常出席县内重要会议和活动。",
        "confidence": "confirmed",
    },

    # ═══ 县政协主席 ═══
    {
        "id": "jingyuan_cao_rong",
        "name": "曹榕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县政协党组书记、主席候选人",
        "current_org": "中国人民政治协商会议靖远县委员会",
        "source": "www.jingyuan.gov.cn (枸杞洽谈会 2026-07-12: '县政协党组书记、主席候选人曹榕主持')",
        "notes": "2026年7月以县政协党组书记、主席候选人身份主持枸杞洽谈会。前任县政协主席刘丽春（见Baidu Baike）。",
        "confidence": "confirmed",
    },

    # ═══ 原县政协主席 ═══
    {
        "id": "jingyuan_liu_lichun",
        "name": "刘丽春",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "Baidu Baike 靖远县条目 (政治表格: 县政协主席 刘丽春)",
        "notes": "Baidu Baike显示刘丽春曾任靖远县政协主席，截至2026年6月。2026年7月已由曹榕接任（或拟接任）。去向待查。",
        "confidence": "plausible",
    },

    # ═══ 县委常委/领导 ═══
    {
        "id": "jingyuan_ma_jindong",
        "name": "马金栋",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县委常委",
        "current_org": "中共靖远县委员会",
        "source": "www.jingyuan.gov.cn (多次陪同李晓清调研, 2026-02-14, 2026-07-17; 枸杞洽谈会)",
        "notes": "多次陪同县委书记李晓清外出调研（安全生产、防汛减灾等），出席枸杞洽谈会。",
        "confidence": "confirmed",
    },

    {
        "id": "jingyuan_cao_huaixuan",
        "name": "曹怀睿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县委常委",
        "current_org": "中共靖远县委员会",
        "source": "www.jingyuan.gov.cn (巡察工作会议 2026-07-17; 枸杞洽谈会 2026-07-12)",
        "notes": "出席县委巡察工作领导小组会议和枸杞洽谈会。",
        "confidence": "confirmed",
    },

    {
        "id": "jingyuan_ma_baojing",
        "name": "马保景",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县委常委",
        "current_org": "中共靖远县委员会",
        "source": "www.jingyuan.gov.cn (巡察工作会议 2026-07-17; 枸杞洽谈会 2026-07-12)",
        "notes": "出席县委巡察工作领导小组会议和枸杞洽谈会。",
        "confidence": "confirmed",
    },

    {
        "id": "jingyuan_gou_sanhai",
        "name": "苟三海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县领导",
        "current_org": "靖远县",
        "source": "www.jingyuan.gov.cn (陪同李晓清检查安全生产 2026-02-14)",
        "notes": "2026年2月陪同时任县长李晓清检查安全生产工作。",
        "confidence": "plausible",
    },

    # ═══ 县领导（从枸杞洽谈会名单） ═══
    {
        "id": "jingyuan_ma_bin",
        "name": "马斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县领导",
        "current_org": "靖远县",
        "source": "www.jingyuan.gov.cn (枸杞洽谈会 2026-07-12)",
        "notes": "出席2026年枸杞产业高质量发展暨经贸洽谈会。",
        "confidence": "plausible",
    },

    {
        "id": "jingyuan_ma_jiaoyan",
        "name": "马娇燕",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县领导",
        "current_org": "靖远县",
        "source": "www.jingyuan.gov.cn (枸杞洽谈会 2026-07-12)",
        "notes": "出席2026年枸杞产业高质量发展暨经贸洽谈会。",
        "confidence": "plausible",
    },

    {
        "id": "jingyuan_chen_liang",
        "name": "陈良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县领导",
        "current_org": "靖远县",
        "source": "www.jingyuan.gov.cn (枸杞洽谈会 2026-07-12)",
        "notes": "出席2026年枸杞产业高质量发展暨经贸洽谈会。",
        "confidence": "plausible",
    },

    {
        "id": "jingyuan_an_qingmin",
        "name": "安清民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县领导",
        "current_org": "靖远县",
        "source": "www.jingyuan.gov.cn (枸杞洽谈会 2026-07-12)",
        "notes": "出席2026年枸杞产业高质量发展暨经贸洽谈会。",
        "confidence": "plausible",
    },

    {
        "id": "jingyuan_zhang_jinzhao",
        "name": "张今朝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县领导",
        "current_org": "靖远县",
        "source": "www.jingyuan.gov.cn (枸杞洽谈会 2026-07-12)",
        "notes": "出席2026年枸杞产业高质量发展暨经贸洽谈会。",
        "confidence": "plausible",
    },

    {
        "id": "jingyuan_chai_ligang",
        "name": "柴立刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县领导",
        "current_org": "靖远县",
        "source": "www.jingyuan.gov.cn (枸杞洽谈会 2026-07-12)",
        "notes": "出席2026年枸杞产业高质量发展暨经贸洽谈会。",
        "confidence": "plausible",
    },

    # ═══ 副县长 ═══
    {
        "id": "jingyuan_li_jingxun",
        "name": "李敬珣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "靖远县副县长",
        "current_org": "靖远县人民政府",
        "source": "www.jingyuan.gov.cn (枸杞洽谈会 2026-07-12: '副县长李敬珣介绍...')",
        "notes": "在枸杞洽谈会上作靖远枸杞产业建设成果及扶持政策介绍。",
        "confidence": "confirmed",
    },

    {
        "id": "jingyuan_wu_xiaolan",
        "name": "吴晓兰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "靖远县副县长",
        "current_org": "靖远县人民政府",
        "source": "www.jingyuan.gov.cn (县人大常委会会议 2026-07-17)",
        "notes": "列席县十八届人大常委会第三十六次会议。",
        "confidence": "confirmed",
    },

    # ═══ 检察院 ═══
    {
        "id": "jingyuan_gao_xingming",
        "name": "高兴明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "靖远县人民检察院检察长",
        "current_org": "靖远县人民检察院",
        "source": "www.jingyuan.gov.cn (县人大常委会会议 2026-07-17)",
        "notes": "列席县十八届人大常委会第三十六次会议。",
        "confidence": "confirmed",
    },

    # ═══ 人大常委会副主任 ═══
    {
        "id": "jingyuan_wang_xingdi",
        "name": "王兴弟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县人大常委会副主任",
        "current_org": "靖远县人民代表大会常务委员会",
        "source": "www.jingyuan.gov.cn (人大常委会会议 2026-07-17)",
        "notes": "出席县十八届人大常委会第三十六次会议。",
        "confidence": "confirmed",
    },

    {
        "id": "jingyuan_chen_yushan",
        "name": "陈瑜山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县人大常委会副主任",
        "current_org": "靖远县人民代表大会常务委员会",
        "source": "www.jingyuan.gov.cn (人大常委会会议 2026-07-17)",
        "notes": "出席县十八届人大常委会第三十六次会议。",
        "confidence": "confirmed",
    },

    {
        "id": "jingyuan_luo_aimin",
        "name": "罗爱民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县人大常委会副主任",
        "current_org": "靖远县人民代表大会常务委员会",
        "source": "www.jingyuan.gov.cn (人大常委会会议 2026-07-17)",
        "notes": "出席县十八届人大常委会第三十六次会议。",
        "confidence": "confirmed",
    },

    {
        "id": "jingyuan_wu_xiaoying",
        "name": "吴晓英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县人大常委会副主任",
        "current_org": "靖远县人民代表大会常务委员会",
        "source": "www.jingyuan.gov.cn (人大常委会会议 2026-07-17)",
        "notes": "出席县十八届人大常委会第三十六次会议。",
        "confidence": "confirmed",
    },

    {
        "id": "jingyuan_liu_xingxian",
        "name": "刘兴贤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "靖远县人大常委会副主任候选人",
        "current_org": "靖远县人民代表大会常务委员会",
        "source": "www.jingyuan.gov.cn (人大常委会会议 2026-07-17: '县人大常委会副主任候选人刘兴贤')",
        "notes": "以县人大常委会副主任候选人身份出席会议。",
        "confidence": "confirmed",
    },
]

# ── Organizations ────────────────────────────────────────────────────────

organizations = [
    {"id": "jingyuan_county_committee", "name": "中共靖远县委员会", "type": "党委", "level": "县", "parent": "中共白银市委员会", "location": "靖远县"},
    {"id": "jingyuan_gov", "name": "靖远县人民政府", "type": "政府", "level": "县", "parent": "白银市人民政府", "location": "靖远县"},
    {"id": "jingyuan_npc", "name": "靖远县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "白银市人民代表大会常务委员会", "location": "靖远县"},
    {"id": "jingyuan_cppcc", "name": "中国人民政治协商会议靖远县委员会", "type": "政协", "level": "县", "parent": "政协白银市委员会", "location": "靖远县"},
    {"id": "jingyuan_procuratorate", "name": "靖远县人民检察院", "type": "事业单位", "level": "县", "parent": "白银市人民检察院", "location": "靖远县"},
]

# ── Positions (person_id, org_id, title, start, end, rank, note) ────────

positions = [
    # 李晓清
    ("jingyuan_li_xiaoqing", "jingyuan_county_committee", "靖远县委书记", "2026-06", "present", "正县级", "同时兼任县长"),
    ("jingyuan_li_xiaoqing", "jingyuan_gov", "靖远县委副书记、县长", "2025", "present", "正县级", "2026年2月以县长身份活动，6-7月升任县委书记"),
    # 王有儒
    ("jingyuan_wang_youru", "jingyuan_npc", "靖远县人大常委会主任", "2021", "present", "正县级", ""),
    # 曹榕
    ("jingyuan_cao_rong", "jingyuan_cppcc", "靖远县政协党组书记、主席候选人", "2026-07", "present", "正县级", "新拟任"),
    # 刘丽春
    ("jingyuan_liu_lichun", "jingyuan_cppcc", "靖远县政协主席", "2021", "2026-06", "正县级", "已离任"),
    # 县委常委
    ("jingyuan_ma_jindong", "jingyuan_county_committee", "靖远县委常委", "", "present", "副县级", ""),
    ("jingyuan_cao_huaixuan", "jingyuan_county_committee", "靖远县委常委", "", "present", "副县级", ""),
    ("jingyuan_ma_baojing", "jingyuan_county_committee", "靖远县委常委", "", "present", "副县级", ""),
    # 副县长
    ("jingyuan_li_jingxun", "jingyuan_gov", "靖远县副县长", "", "present", "副县级", ""),
    ("jingyuan_wu_xiaolan", "jingyuan_gov", "靖远县副县长", "", "present", "副县级", ""),
    # 检察院
    ("jingyuan_gao_xingming", "jingyuan_procuratorate", "靖远县人民检察院检察长", "", "present", "副县级", ""),
    # 人大副主任
    ("jingyuan_wang_xingdi", "jingyuan_npc", "靖远县人大常委会副主任", "", "present", "副县级", ""),
    ("jingyuan_chen_yushan", "jingyuan_npc", "靖远县人大常委会副主任", "", "present", "副县级", ""),
    ("jingyuan_luo_aimin", "jingyuan_npc", "靖远县人大常委会副主任", "", "present", "副县级", ""),
    ("jingyuan_wu_xiaoying", "jingyuan_npc", "靖远县人大常委会副主任", "", "present", "副县级", ""),
    ("jingyuan_liu_xingxian", "jingyuan_npc", "靖远县人大常委会副主任候选人", "2026-07", "present", "副县级", ""),
    # 县领导（具体职务待查）
    ("jingyuan_gou_sanhai", "jingyuan_gov", "靖远县领导", "", "present", "副县级", "具体职务待确认"),
    ("jingyuan_ma_bin", "jingyuan_gov", "靖远县领导", "", "present", "", "具体职务待确认"),
    ("jingyuan_ma_jiaoyan", "jingyuan_gov", "靖远县领导", "", "present", "", "具体职务待确认"),
    ("jingyuan_chen_liang", "jingyuan_gov", "靖远县领导", "", "present", "", "具体职务待确认"),
    ("jingyuan_an_qingmin", "jingyuan_gov", "靖远县领导", "", "present", "", "具体职务待确认"),
    ("jingyuan_zhang_jinzhao", "jingyuan_gov", "靖远县领导", "", "present", "", "具体职务待确认"),
    ("jingyuan_chai_ligang", "jingyuan_gov", "靖远县领导", "", "present", "", "具体职务待确认"),
]

# ── Relationships ────────────────────────────────────────────────────────

relationships = [
    # 同一班子关系
    ("jingyuan_li_xiaoqing", "jingyuan_wang_youru", "领导-人大", "confirmed", "靖远县委、人大", "2021-present", "书记与人大主任工作配合关系"),
    ("jingyuan_li_xiaoqing", "jingyuan_cao_rong", "领导-政协", "confirmed", "靖远县委、政协", "2026-07-present", "书记与政协主席候选人工作配合"),
    ("jingyuan_li_xiaoqing", "jingyuan_ma_jindong", "上下级", "confirmed", "靖远县委", "2026-present", "多次一同调研，马金栋系县委常委"),
    ("jingyuan_li_xiaoqing", "jingyuan_cao_huaixuan", "上下级", "confirmed", "靖远县委", "2026-present", "曹怀睿系县委常委，出席巡察会议"),
    ("jingyuan_li_xiaoqing", "jingyuan_ma_baojing", "上下级", "confirmed", "靖远县委", "2026-present", "马保景系县委常委，出席巡察会议"),
    ("jingyuan_li_xiaoqing", "jingyuan_li_jingxun", "上下级", "confirmed", "靖远县人民政府", "2026-present", "李敬珣系副县长"),
    ("jingyuan_li_xiaoqing", "jingyuan_wu_xiaolan", "上下级", "confirmed", "靖远县人民政府", "2026-present", "吴晓兰系副县长"),
    # 人大常委会内部
    ("jingyuan_wang_youru", "jingyuan_wang_xingdi", "上下级", "confirmed", "靖远县人大常委会", "present", "主任与副主任"),
    ("jingyuan_wang_youru", "jingyuan_chen_yushan", "上下级", "confirmed", "靖远县人大常委会", "present", "主任与副主任"),
    ("jingyuan_wang_youru", "jingyuan_luo_aimin", "上下级", "confirmed", "靖远县人大常委会", "present", "主任与副主任"),
    ("jingyuan_wang_youru", "jingyuan_wu_xiaoying", "上下级", "confirmed", "靖远县人大常委会", "present", "主任与副主任"),
    # 政协前后任
    ("jingyuan_liu_lichun", "jingyuan_cao_rong", "前后任", "plausible", "靖远县政协", "2026", "刘丽春离任后由曹榕接任"),
    # 县委原县长-书记晋升
    ("jingyuan_li_xiaoqing", "jingyuan_li_xiaoqing", "自晋升", "confirmed", "靖远县", "2026", "由县长升任县委书记（一肩挑）"),
]

# ══════════════════════════════════════════════════════════════════════════
# SQLITE DATABASE
# ══════════════════════════════════════════════════════════════════════════

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
    CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT,
        ethnicity TEXT,
        birth TEXT,
        birthplace TEXT,
        native_place TEXT,
        education TEXT,
        party_join TEXT,
        work_start TEXT,
        current_post TEXT,
        current_org TEXT,
        source TEXT,
        notes TEXT,
        confidence TEXT
    );

    CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    );

    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT NOT NULL,
        org_id TEXT NOT NULL,
        title TEXT NOT NULL,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );

    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT NOT NULL,
        person_b TEXT NOT NULL,
        type TEXT NOT NULL,
        confidence TEXT,
        overlap_org TEXT,
        overlap_period TEXT,
        evidence TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
""")

# Insert persons
for p in persons:
    cur.execute("""
        INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
            education, party_join, work_start, current_post, current_org, source, notes, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
          p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
          p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
          p.get("current_post", ""), p.get("current_org", ""),
          p.get("source", ""), p.get("notes", ""), p.get("confidence", "")))

# Insert organizations
for o in organizations:
    cur.execute("""
        INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

# Insert positions
for pos in positions:
    cur.execute("""
        INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, pos)

# Insert relationships (skip self-relationships)
for r in relationships:
    if r[0] == r[1]:
        continue
    cur.execute("""
        INSERT INTO relationships (person_a, person_b, type, confidence, overlap_org, overlap_period, evidence)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (r[0], r[1], r[2], r[3], r[4], r[5], r[6]))

conn.commit()

# ── Summary ──────────────────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"✅ Database created: {DB_PATH}")
print(f"   Persons: {person_count}, Organizations: {org_count}, Positions: {pos_count}, Relationships: {rel_count}")


# ══════════════════════════════════════════════════════════════════════════
# GEXF GRAPH
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(person_id):
    """Return 'r,g,b' for a person node based on role."""
    name_to_role = {
        "jingyuan_li_xiaoqing": "255,50,50",        # Red — 县委书记
        "jingyuan_wang_youru": "50,100,255",        # Blue — 人大主任
        "jingyuan_cao_rong": "50,100,255",          # Blue — 政协主席
        "jingyuan_liu_lichun": "100,100,100",       # Grey — 原政协主席
        "jingyuan_li_jingxun": "50,100,255",        # Blue — 副县长
        "jingyuan_wu_xiaolan": "50,100,255",        # Blue — 副县长
        "jingyuan_gao_xingming": "255,165,0",       # Orange — 检察院
    }
    return name_to_role.get(person_id, "100,100,100")

def person_size(person_id):
    """Node size based on importance."""
    big = {"jingyuan_li_xiaoqing", "jingyuan_wang_youru", "jingyuan_cao_rong"}
    return "20.0" if person_id in big else "12.0"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
    }
    return colors.get(org_type, "200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{TODAY}">')
lines.append('    <creator>OpenCode Research Agent (Sisyphus)</creator>')
lines.append('    <description>靖远县领导班子工作关系网络 — 白银市靖远县</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="confidence" type="string"/>')
lines.append('      <attribute id="2" title="period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    pid = p["id"]
    c = person_color(pid)
    sz = person_size(pid)
    role = p.get("current_post", "")
    org = p.get("current_org", "")
    lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = o["id"]
    oc = org_color(o["type"])
    lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# ── Edges: Person → Organization (worked_at) ──
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos[0]}" target="o{pos[1]}" label="{esc(pos[2])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos[5] or "")}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(pos[3] or "")}-{esc(pos[4] or "")}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# ── Edges: Person ↔ Person (relationship) ──
for r in relationships:
    if r[0] == r[1]:
        continue  # skip self
    eid += 1
    conf = r[3]
    weight = "2.0" if conf == "confirmed" else "1.5" if conf == "plausible" else "1.0"
    lines.append(f'      <edge id="e{eid}" source="p{r[0]}" target="p{r[1]}" label="{esc(r[2])}" weight="{weight}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(conf)}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r[5] or "")}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF graph created: {GEXF_PATH}")
print(f"   Edges: {eid}")
print("Done.")
