#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 景泰县 (Jingtai County, Gansu Province).

Task: gansu_景泰县 — 县委书记 & 县长
Province: 甘肃省
Parent city: 白银市
Region: 景泰县
Level: 县
Research date: 2026-07-17
Model intent: iagent

Confirmed officeholders (as of 2026-07-17, from www.jingtai.gov.cn 领导之窗):
- 县委书记: 刘定顺 (born 1973.04, male, Han, university degree, from Gansu)
- 县长: 李学雄 (born 1980.09, male, Han, university degree)
- 县委副书记: 许立龙 (born 1981.08, male, Han, university degree)
- 县委常委、常务副县长: 吴爱民 (born 1979.11, male, Han, university degree)

县委常委会 (12 members confirmed from www.jingtai.gov.cn/ldzc/):
刘定顺, 李学雄, 许立龙, 王晓燕, 张亚兵, 刘中朝,
吴爱民, 张雷, 罗卓, 狄国亮, 冯锡国, 张庆懿

Key Note: 刘定顺 assumed office as 县委书记 (date not specified, appears to be
relatively recent — his profile was published in 2026 on the gov site).
Predecessor unknown from available sources (potential predecessor: 薛丞忠).

李学雄 serves as 县委副书记、县长 (confirmed since at least 2023 profile on gov site).

Sources:
- www.jingtai.gov.cn/ldzc/ (official leadership page, accessed 2026-07-17)
- www.jingtai.gov.cn (news articles from 2026-07)
"""

import json
import os
import sqlite3
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in SCRIPT_DIR:
    STAGING = SCRIPT_DIR
else:
    GOV_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STAGING = os.path.join(GOV_ROOT, "data", "tmp", "gansu_景泰县")
DB_PATH = os.path.join(STAGING, "景泰县_network.db")
GEXF_PATH = os.path.join(STAGING, "景泰县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

TODAY = datetime.now().strftime("%Y-%m-%d")

# ══════════════════════════════════════════════════════════════════════════
# RESEARCH DATA
# ══════════════════════════════════════════════════════════════════════════

persons = [
    # ═══ Core Leader: 县委书记 ═══
    {
        "id": "jingtai_liu_dingshun",
        "name": "刘定顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年4月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县委书记",
        "current_org": "中共景泰县委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县委书记 刘定顺, accessed 2026-07-17)",
        "notes": "1973年4月出生，大学学历。2026年已以县委书记身份主持县委常委会、调研文旅等。履历详情待查。前任县委书记信息待核实。",
        "confidence": "confirmed",
    },

    # ═══ Core Leader: 县长 ═══
    {
        "id": "jingtai_li_xuexiong",
        "name": "李学雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年9月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县委副书记、县长",
        "current_org": "景泰县人民政府",
        "source": "www.jingtai.gov.cn (领导之窗: 县委副书记、县长 李学雄; 政府页, accessed 2026-07-17)",
        "notes": "1980年9月出生，大学学历。主持县政府全面工作。分管审计局。2023年领导之窗页面已存在，说明至少在2023年已在任。",
        "confidence": "confirmed",
    },

    # ═══ 县委副书记 ═══
    {
        "id": "jingtai_xu_lilong",
        "name": "许立龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年8月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县委副书记",
        "current_org": "中共景泰县委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县委副书记 许立龙, accessed 2026-07-17)",
        "notes": "1981年8月出生，大学学历。多次陪同书记调研文旅、参加党建会议。",
        "confidence": "confirmed",
    },

    # ═══ 县委常委/宣传部部长 ═══
    {
        "id": "jingtai_wang_xiaoyan",
        "name": "王晓燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县委常委、县委宣传部部长",
        "current_org": "中共景泰县委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县委常委、宣传部部长 王晓燕, accessed 2026-07-17)",
        "notes": "县委常委、宣传部部长。2023年已有领导之窗页面。",
        "confidence": "confirmed",
    },

    # ═══ 县委常委/纪委书记 ═══
    {
        "id": "jingtai_zhang_yabing",
        "name": "张亚兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县委常委、县纪委书记",
        "current_org": "中共景泰县纪律检查委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县委常委、县纪委书记 张亚兵, accessed 2026-07-17)",
        "notes": "县委常委、县纪委书记。出席县委理论中心组学习会。",
        "confidence": "confirmed",
    },

    # ═══ 县委常委/政法委书记 ═══
    {
        "id": "jingtai_liu_zhongchao",
        "name": "刘中朝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县委常委、县委政法委书记",
        "current_org": "中共景泰县委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县委常委、政法委书记 刘中朝, accessed 2026-07-17)",
        "notes": "县委常委、政法委书记。出席县委理论学习中心组会议。",
        "confidence": "confirmed",
    },

    # ═══ 县委常委/常务副县长 ═══
    {
        "id": "jingtai_wu_aimin",
        "name": "吴爱民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年11月",
        "birthplace": "",
        "native_place": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县委常委、常务副县长",
        "current_org": "景泰县人民政府",
        "source": "www.jingtai.gov.cn (领导之窗: 县委常委、常务副县长 吴爱民, accessed 2026-07-17)",
        "notes": "1979年11月出生，大学本科学历。负责县政府常务工作。分管发改、财政、住建、应急、人社等。",
        "confidence": "confirmed",
    },

    # ═══ 县委常委/副县长 ═══
    {
        "id": "jingtai_zhang_lei",
        "name": "张雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县委常委、副县长",
        "current_org": "景泰县人民政府",
        "source": "www.jingtai.gov.cn (领导之窗: 县委常委、副县长 张雷, accessed 2026-07-17)",
        "notes": "县委常委、副县长。2024年领导之窗页面。",
        "confidence": "confirmed",
    },

    # ═══ 县委常委/人武部政委 ═══
    {
        "id": "jingtai_luo_zhuo",
        "name": "罗卓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县委常委、县人民武装部上校政治委员",
        "current_org": "景泰县人民武装部",
        "source": "www.jingtai.gov.cn (领导之窗: 县委常委、县人武部上校政治委员 罗卓, accessed 2026-07-17)",
        "notes": "县委常委、人武部政委。2023年已有领导之窗页面。",
        "confidence": "confirmed",
    },

    # ═══ 县委常委/组织部部长 ═══
    {
        "id": "jingtai_di_guoliang",
        "name": "狄国亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县委常委、县委组织部部长",
        "current_org": "中共景泰县委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县委常委、组织部部长 狄国亮, accessed 2026-07-17)",
        "notes": "县委常委、组织部部长。出席县委理论学习中心组会议和群众身边不正之风整治会议。",
        "confidence": "confirmed",
    },

    # ═══ 县委常委/副县长（冯锡国） ═══
    {
        "id": "jingtai_feng_xiguo",
        "name": "冯锡国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县委常委、副县长",
        "current_org": "景泰县人民政府",
        "source": "www.jingtai.gov.cn (领导之窗: 县委常委、副县长 冯锡国, accessed 2026-07-17)",
        "notes": "2026年新晋县委常委、副县长。出席县四班子赴省景电水资源利用中心走访活动。",
        "confidence": "confirmed",
    },

    # ═══ 县委常委/统战部部长 ═══
    {
        "id": "jingtai_zhang_qingyi",
        "name": "张庆懿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县委常委、县委统战部部长",
        "current_org": "中共景泰县委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县委常委、统战部部长 张庆懿, accessed 2026-07-17)",
        "notes": "县委常委、统战部部长。出席县委理论学习中心组会议。",
        "confidence": "confirmed",
    },

    # ═══ 副县长（非常委） ═══
    {
        "id": "jingtai_zhang_xuening",
        "name": "张学宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县副县长、县公安局局长",
        "current_org": "景泰县人民政府、景泰县公安局",
        "source": "www.jingtai.gov.cn (领导之窗: 副县长、县公安局局长 张学宁, accessed 2026-07-17)",
        "notes": "副县长兼公安局长。2023年已有领导之窗页面。",
        "confidence": "confirmed",
    },

    {
        "id": "jingtai_shi_fukun",
        "name": "石福琨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县副县长",
        "current_org": "景泰县人民政府",
        "source": "www.jingtai.gov.cn (领导之窗: 副县长 石福琨, accessed 2026-07-17)",
        "notes": "副县长。2023年已有领导之窗页面。",
        "confidence": "confirmed",
    },

    {
        "id": "jingtai_zhou_baofeng",
        "name": "周宝峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县副县长",
        "current_org": "景泰县人民政府",
        "source": "www.jingtai.gov.cn (领导之窗: 副县长 周宝峰, accessed 2026-07-17)",
        "notes": "副县长。2023年已有领导之窗页面。",
        "confidence": "confirmed",
    },

    {
        "id": "jingtai_zhang_ying",
        "name": "张颖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县副县长",
        "current_org": "景泰县人民政府",
        "source": "www.jingtai.gov.cn (领导之窗: 副县长 张颖, accessed 2026-07-17)",
        "notes": "女，副县长。陪同刘定顺调研文旅产业。2023年已有领导之窗页面。",
        "confidence": "confirmed",
    },

    # ═══ 县人大 ═══
    {
        "id": "jingtai_xu_kelin",
        "name": "许可林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年11月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县人大常委会党组书记、主任",
        "current_org": "景泰县人民代表大会常务委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县人大常委会主任 许可林, accessed 2026-07-17)",
        "notes": "1969年11月出生，研究生学历。县人大常委会主任。",
        "confidence": "confirmed",
    },

    {
        "id": "jingtai_li_junbiao",
        "name": "李俊标",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县人大常委会党组副书记、副主任",
        "current_org": "景泰县人民代表大会常务委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县人大常委会副主任 李俊标, accessed 2026-07-17)",
        "notes": "县人大常委会党组副书记、副主任。",
        "confidence": "confirmed",
    },

    {
        "id": "jingtai_hao_guohua",
        "name": "郝国华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县人大常委会党组成员、副主任",
        "current_org": "景泰县人民代表大会常务委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县人大常委会副主任 郝国华, accessed 2026-07-17)",
        "notes": "县人大常委会副主任。",
        "confidence": "confirmed",
    },

    {
        "id": "jingtai_li_zike",
        "name": "李自科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县人大常委会党组成员、副主任",
        "current_org": "景泰县人民代表大会常务委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县人大常委会副主任 李自科, accessed 2026-07-17)",
        "notes": "县人大常委会副主任。2025年领导之窗页面。",
        "confidence": "confirmed",
    },

    # ═══ 县政协 ═══
    {
        "id": "jingtai_wang_tao",
        "name": "王涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年7月",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县政协党组书记、主席",
        "current_org": "中国人民政治协商会议景泰县委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县政协主席 王涛, accessed 2026-07-17)",
        "notes": "1971年7月出生，在职大学学历。",
        "confidence": "confirmed",
    },

    {
        "id": "jingtai_zhang_cuimei",
        "name": "张翠梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县政协副主席",
        "current_org": "中国人民政治协商会议景泰县委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县政协副主席 张翠梅, accessed 2026-07-17)",
        "notes": "县政协副主席。",
        "confidence": "confirmed",
    },

    {
        "id": "jingtai_an_fangqiang",
        "name": "安方强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县政协党组成员、副主席",
        "current_org": "中国人民政治协商会议景泰县委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县政协副主席 安方强, accessed 2026-07-17)",
        "notes": "县政协副主席。",
        "confidence": "confirmed",
    },

    {
        "id": "jingtai_xu_dong",
        "name": "徐东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "景泰县政协党组成员、副主席",
        "current_org": "中国人民政治协商会议景泰县委员会",
        "source": "www.jingtai.gov.cn (领导之窗: 县政协副主席 徐东, accessed 2026-07-17)",
        "notes": "县政协副主席。",
        "confidence": "confirmed",
    },
]

# ── Organizations ────────────────────────────────────────────────────────

organizations = [
    {"id": "jingtai_county_committee", "name": "中共景泰县委员会", "type": "党委", "level": "县", "parent": "中共白银市委员会", "location": "景泰县"},
    {"id": "jingtai_gov", "name": "景泰县人民政府", "type": "政府", "level": "县", "parent": "白银市人民政府", "location": "景泰县"},
    {"id": "jingtai_discipline", "name": "中共景泰县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共白银市纪律检查委员会", "location": "景泰县"},
    {"id": "jingtai_npc", "name": "景泰县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "白银市人民代表大会常务委员会", "location": "景泰县"},
    {"id": "jingtai_cppcc", "name": "中国人民政治协商会议景泰县委员会", "type": "政协", "level": "县", "parent": "政协白银市委员会", "location": "景泰县"},
    {"id": "jingtai_public_security", "name": "景泰县公安局", "type": "政府", "level": "县", "parent": "白银市公安局", "location": "景泰县"},
    {"id": "jingtai_military", "name": "景泰县人民武装部", "type": "事业单位", "level": "县", "parent": "白银军分区", "location": "景泰县"},
]

# ── Positions (person_id, org_id, title, start, end, rank, note) ────────

positions = [
    # 刘定顺
    ("jingtai_liu_dingshun", "jingtai_county_committee", "景泰县委书记", "2026", "present", "正县级", "2026年以县委书记身份主持工作"),
    # 李学雄
    ("jingtai_li_xuexiong", "jingtai_county_committee", "景泰县委副书记", "2023", "present", "副县级", "至少在2023年已任副书记"),
    ("jingtai_li_xuexiong", "jingtai_gov", "景泰县县长", "2023", "present", "正县级", "主持县政府全面工作"),
    # 许立龙
    ("jingtai_xu_lilong", "jingtai_county_committee", "景泰县委副书记", "2026", "present", "副县级", "2026年新设副书记岗位"),
    # 王晓燕
    ("jingtai_wang_xiaoyan", "jingtai_county_committee", "景泰县委常委、宣传部部长", "2023", "present", "副县级", ""),
    # 张亚兵
    ("jingtai_zhang_yabing", "jingtai_discipline", "景泰县委常委、县纪委书记", "2023", "present", "副县级", ""),
    # 刘中朝
    ("jingtai_liu_zhongchao", "jingtai_county_committee", "景泰县委常委、政法委书记", "2023", "present", "副县级", ""),
    # 吴爱民
    ("jingtai_wu_aimin", "jingtai_gov", "景泰县委常委、常务副县长", "2023", "present", "副县级", "负责县政府常务工作"),
    # 张雷
    ("jingtai_zhang_lei", "jingtai_gov", "景泰县委常委、副县长", "2024", "present", "副县级", ""),
    # 罗卓
    ("jingtai_luo_zhuo", "jingtai_military", "景泰县委常委、县人武部上校政委", "2023", "present", "副县级", ""),
    # 狄国亮
    ("jingtai_di_guoliang", "jingtai_county_committee", "景泰县委常委、组织部部长", "2023", "present", "副县级", ""),
    # 冯锡国
    ("jingtai_feng_xiguo", "jingtai_gov", "景泰县委常委、副县长", "2026", "present", "副县级", "2026年新晋县委常委"),
    # 张庆懿
    ("jingtai_zhang_qingyi", "jingtai_county_committee", "景泰县委常委、统战部部长", "2023", "present", "副县级", ""),
    # 张学宁
    ("jingtai_zhang_xuening", "jingtai_public_security", "景泰县副县长、县公安局局长", "2023", "present", "副县级", ""),
    # 石福琨
    ("jingtai_shi_fukun", "jingtai_gov", "景泰县副县长", "2023", "present", "副县级", ""),
    # 周宝峰
    ("jingtai_zhou_baofeng", "jingtai_gov", "景泰县副县长", "2023", "present", "副县级", ""),
    # 张颖
    ("jingtai_zhang_ying", "jingtai_gov", "景泰县副县长", "2023", "present", "副县级", ""),
    # 人大
    ("jingtai_xu_kelin", "jingtai_npc", "景泰县人大常委会党组书记、主任", "2025", "present", "正县级", ""),
    ("jingtai_li_junbiao", "jingtai_npc", "景泰县人大常委会党组副书记、副主任", "2023", "present", "副县级", ""),
    ("jingtai_hao_guohua", "jingtai_npc", "景泰县人大常委会党组成员、副主任", "2023", "present", "副县级", ""),
    ("jingtai_li_zike", "jingtai_npc", "景泰县人大常委会党组成员、副主任", "2025", "present", "副县级", ""),
    # 政协
    ("jingtai_wang_tao", "jingtai_cppcc", "景泰县政协党组书记、主席", "2023", "present", "正县级", ""),
    ("jingtai_zhang_cuimei", "jingtai_cppcc", "景泰县政协副主席", "2023", "present", "副县级", ""),
    ("jingtai_an_fangqiang", "jingtai_cppcc", "景泰县政协党组成员、副主席", "2023", "present", "副县级", ""),
    ("jingtai_xu_dong", "jingtai_cppcc", "景泰县政协党组成员、副主席", "2023", "present", "副县级", ""),
]

# ── Relationships ────────────────────────────────────────────────────────

relationships = [
    # 书记-县长
    ("jingtai_liu_dingshun", "jingtai_li_xuexiong", "党政一把手", "confirmed", "中共景泰县委员会、景泰县人民政府", "2026-present", "刘定顺任书记，李学雄任县长，为党政主要领导搭配关系"),
    # 书记-副书记
    ("jingtai_liu_dingshun", "jingtai_xu_lilong", "上下级", "confirmed", "中共景泰县委员会", "2026-present", "许立龙为县委副书记，多次陪同刘定顺调研"),
    # 书记-县委常委（领导班子）
    ("jingtai_liu_dingshun", "jingtai_wang_xiaoyan", "上下级", "confirmed", "中共景泰县委员会", "2023-present", "王晓燕系县委常委、宣传部部长"),
    ("jingtai_liu_dingshun", "jingtai_zhang_yabing", "上下级", "confirmed", "中共景泰县委员会", "2023-present", "张亚兵系县委常委、纪委书记"),
    ("jingtai_liu_dingshun", "jingtai_liu_zhongchao", "上下级", "confirmed", "中共景泰县委员会", "2023-present", "刘中朝系县委常委、政法委书记"),
    ("jingtai_liu_dingshun", "jingtai_wu_aimin", "上下级", "confirmed", "中共景泰县委员会", "2023-present", "吴爱民系县委常委、常务副县长"),
    ("jingtai_liu_dingshun", "jingtai_di_guoliang", "上下级", "confirmed", "中共景泰县委员会", "2023-present", "狄国亮系县委常委、组织部部长"),
    ("jingtai_liu_dingshun", "jingtai_feng_xiguo", "上下级", "confirmed", "中共景泰县委员会", "2026-present", "冯锡国系县委常委、副县长"),
    ("jingtai_liu_dingshun", "jingtai_zhang_qingyi", "上下级", "confirmed", "中共景泰县委员会", "2023-present", "张庆懿系县委常委、统战部部长"),
    # 县长-副县长
    ("jingtai_li_xuexiong", "jingtai_wu_aimin", "上下级", "confirmed", "景泰县人民政府", "2023-present", "吴爱民系常务副县长，协助县长工作"),
    ("jingtai_li_xuexiong", "jingtai_zhang_lei", "上下级", "confirmed", "景泰县人民政府", "2024-present", "张雷系副县长"),
    ("jingtai_li_xuexiong", "jingtai_zhang_xuening", "上下级", "confirmed", "景泰县人民政府", "2023-present", "张学宁系副县长兼公安局长"),
    ("jingtai_li_xuexiong", "jingtai_shi_fukun", "上下级", "confirmed", "景泰县人民政府", "2023-present", "石福琨系副县长"),
    ("jingtai_li_xuexiong", "jingtai_zhou_baofeng", "上下级", "confirmed", "景泰县人民政府", "2023-present", "周宝峰系副县长"),
    ("jingtai_li_xuexiong", "jingtai_zhang_ying", "上下级", "confirmed", "景泰县人民政府", "2023-present", "张颖系副县长"),
    # 四套班子关系 - 书记-人大主任
    ("jingtai_liu_dingshun", "jingtai_xu_kelin", "党政-人大", "confirmed", "景泰县", "2025-present", "书记与人大主任工作关系"),
    # 四套班子关系 - 书记-政协主席
    ("jingtai_liu_dingshun", "jingtai_wang_tao", "党政-政协", "confirmed", "景泰县", "2023-present", "书记与政协主席工作关系"),
    # 人大内部
    ("jingtai_xu_kelin", "jingtai_li_junbiao", "上下级", "confirmed", "景泰县人大常委会", "2025-present", "主任与副主任"),
    ("jingtai_xu_kelin", "jingtai_hao_guohua", "上下级", "confirmed", "景泰县人大常委会", "2025-present", "主任与副主任"),
    ("jingtai_xu_kelin", "jingtai_li_zike", "上下级", "confirmed", "景泰县人大常委会", "2025-present", "主任与副主任"),
    # 政协内部
    ("jingtai_wang_tao", "jingtai_zhang_cuimei", "上下级", "confirmed", "景泰县政协", "2023-present", "主席与副主席"),
    ("jingtai_wang_tao", "jingtai_an_fangqiang", "上下级", "confirmed", "景泰县政协", "2023-present", "主席与副主席"),
    ("jingtai_wang_tao", "jingtai_xu_dong", "上下级", "confirmed", "景泰县政协", "2023-present", "主席与副主席"),
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

# Insert relationships
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
        "jingtai_liu_dingshun": "255,50,50",        # Red — 县委书记
        "jingtai_li_xuexiong": "50,100,255",        # Blue — 县长
        "jingtai_xu_lilong": "100,100,100",         # Grey — 副书记
        "jingtai_wu_aimin": "50,100,255",           # Blue — 常务副县长
        "jingtai_xu_kelin": "50,100,255",           # Blue — 人大主任
        "jingtai_wang_tao": "50,100,255",           # Blue — 政协主席
        "jingtai_zhang_yabing": "255,165,0",        # Orange — 纪委书记
        "jingtai_zhang_xuening": "50,100,255",      # Blue — 副县长/公安局长
        "jingtai_shi_fukun": "50,100,255",          # Blue — 副县长
        "jingtai_zhou_baofeng": "50,100,255",       # Blue — 副县长
        "jingtai_zhang_ying": "50,100,255",         # Blue — 副县长
    }
    return name_to_role.get(person_id, "100,100,100")

def person_size(person_id):
    """Node size based on importance."""
    big = {"jingtai_liu_dingshun", "jingtai_li_xuexiong", "jingtai_xu_kelin", "jingtai_wang_tao"}
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
lines.append('    <description>景泰县领导班子工作关系网络 — 白银市景泰县</description>')
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
        continue
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
