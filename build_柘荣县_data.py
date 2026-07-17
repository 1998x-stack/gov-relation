#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 柘荣县 (Zherong County, Ningde, Fujian).

Task: fujian_柘荣县 — 县委书记 & 县长
Province: 福建省
City: 宁德市
Region: 柘荣县
Level: 县
Research date: 2026-07-17

Confirmed officeholders (as of 2026-07-17):
- 县委书记: 詹少铃 (born 1979.12, male, Han, Fujian Fu'an, university/教育学学士)
- 代县长: 邹渊 (born 1987.08, male, Han, Zhejiang Tonglu, Tsinghua PhD)
- 前县长: 宋振 (born 1989.01, male, Han, Anhui Taihe, Tsinghua PhD, left Jul 2026)
- 前县委书记: 张晓容 (born 1975, male, Han, Fujian Ninghua, now at 福建省公安厅)

县委常委会 (partially confirmed from news reports):
詹少铃(书记), 邹渊(副书记/代县长), 刘晓兵, 袁济光, 郭萌, 吴茂鸿, 韦莉

Sources:
- baike.baidu.com (詹少铃)
- zh.wikipedia.org (宋振, 柘荣县)
- 观八闽 / thepaper.cn (詹少铃任柘荣县委书记)
- 长安街知事 (党帅 career path)
- 柘荣县人大决议 (宋振离职, 邹渊任代县长)
- Ningde city government announcements

Confidence: Core leadership confirmed from encyclopedia/official sources.
Career details for deputies are limited — full career histories not found.
Marked gaps explicitly.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GOV_ROOT = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == "data" else SCRIPT_DIR
if "data/tmp" in SCRIPT_DIR:
    STAGING = SCRIPT_DIR
else:
    STAGING = os.path.join(GOV_ROOT, "data", "tmp", "fujian_柘荣县")
DB_PATH = os.path.join(STAGING, "柘荣县_network.db")
GEXF_PATH = os.path.join(STAGING, "柘荣县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 县委书记 — 詹少铃
    {
        "id": "zherong_zhan_shaoling",
        "name": "詹少铃",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年12月",
        "birthplace": "福建福安",
        "native_place": "福建福安",
        "education": "大学学历、教育学学士",
        "party_join": "1999年6月",
        "work_start": "2000年8月",
        "current_post": "柘荣县委书记",
        "current_org": "中共柘荣县委员会",
        "source": "baike.baidu.com/item/詹少铃, 观八闽 (thepaper.cn)",
        "notes": "2025年10月任柘荣县委书记。曾任宁德市委办公室综合一科科长、宁德市委办公室副主任、"
             "宁德市委改革办常务副主任、宁德市政府党组成员/秘书长/办公室党组书记。"
             "2025年11月起兼任县人武部党委第一书记。",
        "confidence": "confirmed",
    },

    # 代县长 — 邹渊
    {
        "id": "zherong_zou_yuan",
        "name": "邹渊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年8月",
        "birthplace": "浙江桐庐",
        "native_place": "浙江桐庐",
        "education": "清华大学理学博士（物理系）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "柘荣县委副书记、代县长",
        "current_org": "柘荣县人民政府",
        "source": "百度百科/鲁网, 新闻报道",
        "notes": "2026年7月由周宁县委常委、常务副县长调任柘荣代县长。清华大学物理系博士，"
             "2014年作为福建省引进生挂职寿宁县。曾任周宁县委常委、常务副县长。"
             "前任宋振已离任，去向待查。",
        "confidence": "confirmed",
    },

    # 前县长 — 宋振 (2021-2026.07)
    {
        "id": "zherong_song_zhen",
        "name": "宋振",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年1月",
        "birthplace": "安徽太和",
        "native_place": "安徽太和",
        "education": "清华大学微电子系工学博士（直博）",
        "party_join": "2008年",
        "work_start": "2015年",
        "current_post": "柘荣县前县长(已离任)",
        "current_org": "",
        "source": "zh.wikipedia.org/wiki/宋振, 柘荣县人大决议",
        "notes": "2021年12月至2026年7月任柘荣县长。2006年华中科技大学电子系本科，"
             "2008年入党，2010年清华大学微电子系直博。2015年福建省引进聘任为柘荣县科技副县长(挂职)。"
             "2017年起任柘荣县委常委/统战部部长/东源乡党委书记。2019年升任柘荣县常务副县长。"
             "2021年5月公示拟任县党政正职，2021年12月当选县长。2026年7月离任，去向待查。",
        "confidence": "confirmed",
    },

    # 前县委书记 — 张晓容 (2021-2025)
    {
        "id": "zherong_zhang_xiaorong",
        "name": "张晓容",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年3月",
        "birthplace": "福建宁化",
        "native_place": "福建宁化",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福建省公安厅党委委员、政治部主任",
        "current_org": "福建省公安厅",
        "source": "观八闽 (thepaper.cn), 柘荣县政府网",
        "notes": "2021年6月至2025年9月任柘荣县委书记。2025年9月调任福建省公安厅党委委员、政治部主任。"
             "福州公安系统出身。完整履历待补充。",
        "confidence": "confirmed",
    },

    # ══════════════ Tsinghua/PKU PhD引进生网络 ══════════════

    # 党帅 — 从柘荣科技副县长起步的清华博士
    {
        "id": "zherong_dang_shuai",
        "name": "党帅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年",
        "birthplace": "山东潍坊",
        "native_place": "山东潍坊",
        "education": "清华大学博士（航天航空学院）",
        "party_join": "中共党员",
        "work_start": "2012年",
        "current_post": "宁德市副市长",
        "current_org": "宁德市人民政府",
        "source": "百度百科, 长安街知事, 人民网",
        "notes": "清华大学博士。2012年任柘荣县科技副县长(挂职)，后任柘荣县委常委、宣传部部长。"
             "2015年11月任共青团宁德市委书记。2016年6月任古田县委副书记、代县长、县长。"
             "2021年任屏南县委书记。后升任宁德市副市长。柘荣→宁德市直→古田→屏南→宁德市的典型跨县成长路径。",
        "confidence": "confirmed",
    },

    # 雷祖铃 — 前柘荣县长
    {
        "id": "zherong_lei_zuling",
        "name": "雷祖铃",
        "gender": "男",
        "ethnicity": "畲族",
        "birth": "1968年",
        "birthplace": "福建福安",
        "native_place": "福建福安",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东侨经济技术开发区党工委书记",
        "current_org": "东侨经济技术开发区",
        "source": "新闻报道",
        "notes": "曾任柘荣县长（至2021年），后任东侨经济技术开发区党工委书记。"
             "宋振的前任。畲族，福安人（与詹少铃同乡）。",
        "confidence": "confirmed",
    },

    # 李睿华 — 北大博士引进生
    {
        "id": "zherong_li_ruihua",
        "name": "李睿华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990年",
        "birthplace": "新疆哈密",
        "native_place": "新疆哈密",
        "education": "北京大学理学博士",
        "party_join": "中共党员",
        "work_start": "2019年",
        "current_post": "宁德市政府办公室副主任",
        "current_org": "宁德市人民政府办公室",
        "source": "观八闽, 新闻报道",
        "notes": "1990年出生。北京大学理学博士（2019年福建省引进生）。"
             "曾任柘荣县科技副县长、英山乡党委书记。2024年8月至2026年6月期间调任宁德市政府办公室副主任。",
        "confidence": "confirmed",
    },

    # ══════════════ Other County Leaders (partial) ══════════════

    # 刘晓兵 — 县领导
    {
        "id": "zherong_liu_xiaobing",
        "name": "刘晓兵",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "柘荣县领导",
        "current_org": "柘荣县人民政府",
        "source": "新闻报道 (柘荣县委农村工作会议等)",
        "notes": "出现在柘荣县近期新闻报道中。具体职务待确认。",
        "confidence": "plausible",
    },

    # 袁济光 — 县领导
    {
        "id": "zherong_yuan_jiguang",
        "name": "袁济光",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "柘荣县领导",
        "current_org": "柘荣县人民政府",
        "source": "新闻报道",
        "notes": "出现在柘荣县新闻报道中。具体职务待确认。",
        "confidence": "plausible",
    },

    # 郭萌 — 县领导
    {
        "id": "zherong_guo_meng",
        "name": "郭萌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "柘荣县领导",
        "current_org": "柘荣县人民政府",
        "source": "新闻报道",
        "notes": "出现在柘荣县新闻报道中。具体职务待确认。",
        "confidence": "plausible",
    },

    # 吴茂鸿 — 县领导
    {
        "id": "zherong_wu_maohong",
        "name": "吴茂鸿",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "柘荣县领导",
        "current_org": "柘荣县人民政府",
        "source": "新闻报道",
        "notes": "出现在柘荣县新闻报道中。具体职务待确认。",
        "confidence": "plausible",
    },

    # 韦莉 — 县领导
    {
        "id": "zherong_wei_li",
        "name": "韦莉",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "柘荣县领导",
        "current_org": "柘荣县人民政府",
        "source": "新闻报道",
        "notes": "出现在柘荣县新闻报道中。具体职务待确认。",
        "confidence": "plausible",
    },

    # ══════════════ Predecessors (earlier) ══════════════

    # 郭宋玉 — 更早的县委书记
    {
        "id": "zherong_guo_songyu",
        "name": "郭宋玉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "福建寿宁",
        "native_place": "福建寿宁",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "新闻报道片段",
        "notes": "曾任柘荣县委书记（在张晓容之前）。去向待查。",
        "confidence": "unverified",
    },
]

organizations = [
    {"id": "cpc_zherong", "name": "中共柘荣县委员会", "type": "党委", "level": "县", "parent": "中共宁德市委员会", "location": "福建省宁德市柘荣县"},
    {"id": "gov_zherong", "name": "柘荣县人民政府", "type": "政府", "level": "县", "parent": "宁德市人民政府", "location": "福建省宁德市柘荣县"},
    {"id": "npc_zherong", "name": "柘荣县人大常委会", "type": "人大", "level": "县", "parent": "", "location": "福建省宁德市柘荣县"},
    {"id": "cppcc_zherong", "name": "柘荣县政协", "type": "政协", "level": "县", "parent": "", "location": "福建省宁德市柘荣县"},
    {"id": "dis_zherong", "name": "中共柘荣县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共宁德市纪律检查委员会", "location": "福建省宁德市柘荣县"},
    {"id": "org_zherong", "name": "中共柘荣县委员会组织部", "type": "党委", "level": "县", "parent": "中共柘荣县委员会", "location": "福建省宁德市柘荣县"},
    {"id": "prop_zherong", "name": "中共柘荣县委员会宣传部", "type": "党委", "level": "县", "parent": "中共柘荣县委员会", "location": "福建省宁德市柘荣县"},
    {"id": "polit_zherong", "name": "中共柘荣县委员会政法委员会", "type": "党委", "level": "县", "parent": "中共柘荣县委员会", "location": "福建省宁德市柘荣县"},
    {"id": "psb_zherong", "name": "柘荣县公安局", "type": "政府", "level": "县", "parent": "柘荣县人民政府", "location": "福建省宁德市柘荣县"},
    {"id": "mili_zherong", "name": "柘荣县人武部", "type": "政府", "level": "县", "parent": "", "location": "福建省宁德市柘荣县"},
    {"id": "gov_ningde", "name": "宁德市人民政府", "type": "政府", "level": "地级", "parent": "福建省人民政府", "location": "福建省宁德市"},
    {"id": "cpc_ningde", "name": "中共宁德市委员会", "type": "党委", "level": "地级", "parent": "中共福建省委员会", "location": "福建省宁德市"},
    {"id": "gov_fujian", "name": "福建省公安厅", "type": "政府", "level": "省级", "parent": "福建省人民政府", "location": "福建省福州市"},
    {"id": "cpc_zhouning", "name": "中共周宁县委员会", "type": "党委", "level": "县", "parent": "中共宁德市委员会", "location": "福建省宁德市周宁县"},
    {"id": "gov_zhouning", "name": "周宁县人民政府", "type": "政府", "level": "县", "parent": "宁德市人民政府", "location": "福建省宁德市周宁县"},
    {"id": "cpc_gutian", "name": "中共古田县委员会", "type": "党委", "level": "县", "parent": "中共宁德市委员会", "location": "福建省宁德市古田县"},
    {"id": "gov_gutian", "name": "古田县人民政府", "type": "政府", "level": "县", "parent": "宁德市人民政府", "location": "福建省宁德市古田县"},
    {"id": "cpc_pingnan", "name": "中共屏南县委员会", "type": "党委", "level": "县", "parent": "中共宁德市委员会", "location": "福建省宁德市屏南县"},
    {"id": "gov_pingnan", "name": "屏南县人民政府", "type": "政府", "level": "县", "parent": "宁德市人民政府", "location": "福建省宁德市屏南县"},
    {"id": "dongqiao_dev", "name": "东侨经济技术开发区", "type": "开发区", "level": "地级", "parent": "宁德市人民政府", "location": "福建省宁德市"},
    {"id": "cpc_shouning", "name": "中共寿宁县委员会", "type": "党委", "level": "县", "parent": "中共宁德市委员会", "location": "福建省宁德市寿宁县"},
]

positions = [
    # 詹少铃
    {"person_id": "zherong_zhan_shaoling", "org_id": "cpc_zherong", "title": "柘荣县委书记", "start": "2025-10", "end": "present", "rank": "正处级", "note": "兼任县人武部党委第一书记"},
    {"person_id": "zherong_zhan_shaoling", "org_id": "mili_zherong", "title": "柘荣县人武部党委第一书记", "start": "2025-11", "end": "present", "rank": "", "note": ""},
    {"person_id": "zherong_zhan_shaoling", "org_id": "gov_ningde", "title": "宁德市政府党组成员/秘书长/办公室党组书记", "start": "", "end": "2025-10", "rank": "正处级", "note": "2025年10月31日被免去"},
    {"person_id": "zherong_zhan_shaoling", "org_id": "cpc_ningde", "title": "宁德市委办公室副主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "zherong_zhan_shaoling", "org_id": "cpc_ningde", "title": "宁德市委改革办常务副主任", "start": "", "end": "", "rank": "正处级", "note": ""},
    # 邹渊
    {"person_id": "zherong_zou_yuan", "org_id": "cpc_zherong", "title": "柘荣县委副书记", "start": "2026-07", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "zherong_zou_yuan", "org_id": "gov_zherong", "title": "柘荣县代县长", "start": "2026-07", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "zherong_zou_yuan", "org_id": "cpc_zhouning", "title": "周宁县委常委、常务副县长", "start": "", "end": "2026-07", "rank": "副处级", "note": ""},
    {"person_id": "zherong_zou_yuan", "org_id": "gov_zhouning", "title": "周宁县常务副县长", "start": "", "end": "2026-07", "rank": "副处级", "note": ""},
    {"person_id": "zherong_zou_yuan", "org_id": "cpc_shouning", "title": "寿宁县挂职（引进生）", "start": "2014", "end": "", "rank": "", "note": "清华大学博士引进生挂职"},
    # 宋振
    {"person_id": "zherong_song_zhen", "org_id": "gov_zherong", "title": "柘荣县长", "start": "2021-12", "end": "2026-07", "rank": "正处级", "note": ""},
    {"person_id": "zherong_song_zhen", "org_id": "cpc_zherong", "title": "柘荣县委副书记", "start": "2021-12", "end": "2026-07", "rank": "副处级", "note": ""},
    {"person_id": "zherong_song_zhen", "org_id": "gov_zherong", "title": "柘荣县科技副县长（挂职）", "start": "2015", "end": "2017", "rank": "副处级", "note": "福建省引进，清华大学博士"},
    {"person_id": "zherong_song_zhen", "org_id": "cpc_zherong", "title": "柘荣县委常委、统战部部长", "start": "2017", "end": "2019", "rank": "副处级", "note": "兼任东源乡党委书记"},
    {"person_id": "zherong_song_zhen", "org_id": "gov_zherong", "title": "柘荣县常务副县长", "start": "2019", "end": "2021-12", "rank": "副处级", "note": ""},
    # 张晓容
    {"person_id": "zherong_zhang_xiaorong", "org_id": "cpc_zherong", "title": "柘荣县委书记", "start": "2021-06", "end": "2025-09", "rank": "正处级", "note": ""},
    {"person_id": "zherong_zhang_xiaorong", "org_id": "gov_fujian", "title": "福建省公安厅党委委员、政治部主任", "start": "2025-09", "end": "present", "rank": "副厅级", "note": ""},
    # 党帅
    {"person_id": "zherong_dang_shuai", "org_id": "gov_zherong", "title": "柘荣县科技副县长（挂职）", "start": "2012", "end": "2015", "rank": "副处级", "note": "清华大学博士引进生"},
    {"person_id": "zherong_dang_shuai", "org_id": "cpc_zherong", "title": "柘荣县委常委、宣传部部长", "start": "2014", "end": "2015-11", "rank": "副处级", "note": ""},
    {"person_id": "zherong_dang_shuai", "org_id": "cpc_ningde", "title": "共青团宁德市委书记", "start": "2015-11", "end": "2016-06", "rank": "正处级", "note": ""},
    {"person_id": "zherong_dang_shuai", "org_id": "gov_gutian", "title": "古田县委副书记、代县长、县长", "start": "2016-06", "end": "2021", "rank": "正处级", "note": ""},
    {"person_id": "zherong_dang_shuai", "org_id": "cpc_pingnan", "title": "屏南县委书记", "start": "2021", "end": "2025", "rank": "正处级", "note": ""},
    {"person_id": "zherong_dang_shuai", "org_id": "gov_ningde", "title": "宁德市副市长", "start": "2025", "end": "present", "rank": "副厅级", "note": ""},
    # 雷祖铃
    {"person_id": "zherong_lei_zuling", "org_id": "gov_zherong", "title": "柘荣县长", "start": "", "end": "2021", "rank": "正处级", "note": "宋振的前任"},
    {"person_id": "zherong_lei_zuling", "org_id": "dongqiao_dev", "title": "东侨经济技术开发区党工委书记", "start": "2021", "end": "present", "rank": "正处级", "note": ""},
    # 李睿华
    {"person_id": "zherong_li_ruihua", "org_id": "gov_zherong", "title": "柘荣县科技副县长", "start": "2019", "end": "2024", "rank": "副处级", "note": "北京大学博士引进生"},
    {"person_id": "zherong_li_ruihua", "org_id": "gov_zherong", "title": "柘荣县英山乡党委书记（兼任）", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": "zherong_li_ruihua", "org_id": "gov_ningde", "title": "宁德市政府办公室副主任", "start": "2024", "end": "present", "rank": "副处级", "note": ""},
    # Other county leaders (partial)
    {"person_id": "zherong_liu_xiaobing", "org_id": "gov_zherong", "title": "柘荣县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": "zherong_yuan_jiguang", "org_id": "gov_zherong", "title": "柘荣县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": "zherong_guo_meng", "org_id": "gov_zherong", "title": "柘荣县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": "zherong_wu_maohong", "org_id": "gov_zherong", "title": "柘荣县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": "zherong_wei_li", "org_id": "gov_zherong", "title": "柘荣县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    # 郭宋玉
    {"person_id": "zherong_guo_songyu", "org_id": "cpc_zherong", "title": "柘荣县委书记（前任前任）", "start": "", "end": "", "rank": "正处级", "note": "在张晓容之前任书记，时间和去向待查"},
]


# ── Relationship edges ──────────────────────────────────────────────────

relationships = [
    # 詹少铃 ↔ 邹渊 (书记↔代县长，党政一把手搭档)
    {"person_a": "zherong_zhan_shaoling", "person_b": "zherong_zou_yuan",
     "type": "superior_subordinate", "strength": "strong",
     "context": "党政一把手搭档，詹少铃主持县委全面工作，邹渊主持县政府全面工作",
     "overlap_org": "中共柘荣县委员会/柘荣县人民政府",
     "overlap_period": "2026年7月起", "confidence": "confirmed"},

    # 詹少铃 ↔ 宋振 (书记↔前县长，短暂共事)
    {"person_a": "zherong_zhan_shaoling", "person_b": "zherong_song_zhen",
     "type": "superior_subordinate", "strength": "strong",
     "context": "詹少铃2025年10月任书记，宋振至2026年7月任县长，共事约9个月",
     "overlap_org": "中共柘荣县委员会/柘荣县人民政府",
     "overlap_period": "2025.10-2026.07", "confidence": "confirmed"},

    # 张晓容 ↔ 詹少铃 (前任书记↔现任书记)
    {"person_a": "zherong_zhang_xiaorong", "person_b": "zherong_zhan_shaoling",
     "type": "predecessor_successor", "strength": "strong",
     "context": "张晓容2021-2025任县委书记后调省公安厅，詹少铃2025年10月接任",
     "overlap_org": "中共柘荣县委员会",
     "overlap_period": "2025年10月交接", "confidence": "confirmed"},

    # 张晓容 ↔ 宋振 (前任书记↔前县长，2021-2025搭档)
    {"person_a": "zherong_zhang_xiaorong", "person_b": "zherong_song_zhen",
     "type": "superior_subordinate", "strength": "strong",
     "context": "张晓容任书记期间，宋振任县长，党政一把手搭档近4年",
     "overlap_org": "中共柘荣县委员会/柘荣县人民政府",
     "overlap_period": "2021.12-2025.09", "confidence": "confirmed"},

    # 宋振 ↔ 党帅 (清华师兄弟，柘荣模式)
    {"person_a": "zherong_song_zhen", "person_b": "zherong_dang_shuai",
     "type": "same_school", "strength": "medium",
     "context": "均为清华大学博士引进生，均以柘荣科技副县长为起点，职业路径高度相似",
     "overlap_org": "清华大学/柘荣县",
     "overlap_period": "2015-2026", "confidence": "plausible"},

    # 党帅 ↔ 李睿华 (引进生前后辈)
    {"person_a": "zherong_dang_shuai", "person_b": "zherong_li_ruihua",
     "type": "same_system", "strength": "medium",
     "context": "党帅(清华2012引进)、李睿华(北大2019引进)，均任柘荣科技副县长后调宁德市直",
     "overlap_org": "柘荣县/宁德市人民政府",
     "overlap_period": "2019年起", "confidence": "plausible"},

    # 雷祖铃 ↔ 宋振 (前任县长↔继任县长)
    {"person_a": "zherong_lei_zuling", "person_b": "zherong_song_zhen",
     "type": "predecessor_successor", "strength": "strong",
     "context": "雷祖铃为宋振前任柘荣县长，后调东侨开发区",
     "overlap_org": "柘荣县人民政府",
     "overlap_period": "2021年交接", "confidence": "confirmed"},

    # 雷祖铃 ↔ 詹少铃 (福安同乡)
    {"person_a": "zherong_lei_zuling", "person_b": "zherong_zhan_shaoling",
     "type": "same_native_place", "strength": "weak",
     "context": "均为福建福安人",
     "overlap_org": "",
     "overlap_period": "", "confidence": "plausible"},

    # 邹渊 ↔ 党帅 (清华引进生前后辈)
    {"person_a": "zherong_zou_yuan", "person_b": "zherong_dang_shuai",
     "type": "same_school", "strength": "medium",
     "context": "均为清华大学博士引进生，邹渊2014年、党帅2012年分别在不同县挂职",
     "overlap_org": "清华大学",
     "overlap_period": "2014年起", "confidence": "plausible"},
]


# ── BUILD ────────────────────────────────────────────────────────────

def build():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, native_place TEXT,
            education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT,
            notes TEXT, confidence TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT, org_id TEXT,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT, person_b TEXT,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, native_place,
             education, party_join, work_start,
             current_post, current_org, source,
             notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p.get("birthplace", ""), p.get("native_place", ""),
             p["education"], p["party_join"], p.get("work_start", ""),
             p["current_post"], p["current_org"], p["source"],
             p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for rel in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period,
             strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (rel["person_a"], rel["person_b"], rel["type"],
             rel["context"], rel["overlap_org"], rel["overlap_period"],
             rel["strength"], rel["confidence"]))

    conn.commit()
    conn.close()
    print(f"[DB] Wrote {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    current = p.get("current_post", "")
    if "县委书记" in current:
        return "255,50,50"
    if "县长" in current or "副县长" in current or "常务副" in current:
        return "50,100,255"
    if "纪委书记" in current or "监委" in current:
        return "255,165,0"
    return "100,100,100"


def is_top_leader(p):
    current = p.get("current_post", "")
    return "县委书记" in current or "县长" in current


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "开发区" in t:
        return "200,255,200"
    if "乡镇" in t:
        return "255,255,200"
    if "事业单位" in t:
        return "220,220,220"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>柘荣县领导班子工作关系网络 — 中共柘荣县委员会、柘荣县人民政府及关联组织</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org_type" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="title" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 1
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    for rel in relationships:
        w = "2.0" if rel.get("strength") == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(rel["person_a"])}" target="{esc(rel["person_b"])}" label="{esc(rel["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("strength",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Wrote {GEXF_PATH}")


if __name__ == "__main__":
    build()
    build_gexf()

    # Summary
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
