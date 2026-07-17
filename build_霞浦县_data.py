#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 霞浦县 (Xiapu County, Ningde, Fujian).

Task: fujian_霞浦县 — 县委书记 & 县长
Province: 福建省
City: 宁德市
Region: 霞浦县
Level: 县
Research date: 2026-07-17

Confirmed officeholders (as of 2026-07-17):
- 县委书记: 罗义春 (born 1975, male, Han, Fujian Fu'an, university + law master)
- 代县长: 蔡晶晶 (born 1982.11, female, Han, provincial party school graduate)
- 县委副书记: 伍银多 (born 1990.08, male, Han, Hubei Nanzhang, PKU PhD)

县委常委会 confirmed members:
罗义春(书记), 蔡晶晶(副书记/代县长), 伍银多(专职副书记), 吴国友(常务副县长),
蔡松根, 崔向新(政法委), 耿世谷(组织部), 雷雯(宣传部), 陈旭(原纪委书记, 现人大主任)

县政府领导班子:
蔡晶晶(代县长), 吴国友(常务副县长), 陆鸣(副县长), 张建勤(副县长/公安局长),
雷宇(副县长, 畲族, 外派挂职), 郑信旋(副县长), 陈义蜜(副县长), 陈广昱(副县长)

Sources:
- www.xiapu.gov.cn (official government leadership pages)
- www.xiapu.gov.cn/zwgk/ldzc/ (领导之窗 individual pages)
- News articles on xiapu.gov.cn
- zh.wikipedia.org (predecessor chain data)

Confidence: Current leadership confirmed from official xiapu.gov.cn sources.
Career details mostly limited — full career histories are not available on the official site.
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
    STAGING = os.path.join(GOV_ROOT, "data", "tmp", "fujian_霞浦县")
DB_PATH = os.path.join(STAGING, "霞浦县_network.db")
GEXF_PATH = os.path.join(STAGING, "霞浦县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 县委书记 — 罗义春
    {
        "id": "xiapu_luo_yichun",
        "name": "罗义春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年",
        "birthplace": "福建福安",
        "native_place": "福建福安",
        "education": "大学（兰州大学）、法律硕士（厦门大学）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县委书记",
        "current_org": "中共霞浦县委员会",
        "source": "xiapu.gov.cn (领导之窗/新闻报道), zh.wikipedia.org",
        "notes": "2026年4月由县长升任县委书记。曾任宁德市纪委常委、市委巡察办主任、东侨经济技术开发区管委会主任、霞浦县县长等职。",
        "confidence": "confirmed",
    },

    # 代县长 — 蔡晶晶
    {
        "id": "xiapu_cai_jingjing",
        "name": "蔡晶晶",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年11月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县委副书记、代县长",
        "current_org": "霞浦县人民政府",
        "source": "xiapu.gov.cn/zwgk/ldzc/cjj/",
        "notes": "2026年7月4日任代县长。曾任屏南县委副书记、古田县委常委/宣传部部长、福鼎市磻溪镇镇长。"
             "主持县政府全面工作。完整履历待补充（出生地、早期经历不详）。",
        "confidence": "confirmed",
    },

    # 县委专职副书记 — 伍银多
    {
        "id": "xiapu_wu_yinduo",
        "name": "伍银多",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990年8月",
        "birthplace": "湖北南漳",
        "native_place": "湖北南漳",
        "education": "管理学博士（北京大学，本硕博连读）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县委副书记",
        "current_org": "中共霞浦县委员会",
        "source": "百度百科、新闻报道",
        "notes": "1990年出生，北京大学管理学博士（本硕博连读）。曾任宁德市蕉城区副区长、古田县委常委/常务副县长，"
             "霞浦县委常委/常务副县长。2023年起任霞浦县委副书记。",
        "confidence": "confirmed",
    },

    # 常务副县长 — 吴国友
    {
        "id": "xiapu_wu_guoyou",
        "name": "吴国友",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年4月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历、工学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县委常委、常务副县长",
        "current_org": "霞浦县人民政府",
        "source": "xiapu.gov.cn/zwgk/ldzc/wuguoyou/",
        "notes": "负责县政府常务工作。分管发改、财政、统计、国资、金融、工信、应急管理等工作。"
             "协助县长联系审计工作。联系县人大、纪委监委等。",
        "confidence": "confirmed",
    },

    # ══════════════ Other Party Standing Committee ══════════════

    # 蔡松根 — 县委常委
    {
        "id": "xiapu_cai_songgen",
        "name": "蔡松根",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县委常委、副县长",
        "current_org": "中共霞浦县委员会",
        "source": "xiapu.gov.cn 新闻报道 (2026-05-20 一季度工作会议)",
        "notes": "通报一季度建筑业情况。具体职务：县委常委、副县长。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 崔向新 — 政法委书记
    {
        "id": "xiapu_cui_xiangxin",
        "name": "崔向新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县委常委、政法委书记",
        "current_org": "中共霞浦县委员会政法委员会",
        "source": "新闻报道 (府院联席会议 2025年7月)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 耿世谷 — 组织部部长（至2025年2月）
    {
        "id": "xiapu_geng_shigu",
        "name": "耿世谷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县委常委、组织部部长",
        "current_org": "中共霞浦县委员会组织部",
        "source": "xiapu.gov.cn (人民政府职务任免通知)",
        "notes": "曾任县委党校校长。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 雷雯 — 宣传部部长
    {
        "id": "xiapu_lei_wen",
        "name": "雷雯",
        "gender": "女",
        "ethnicity": "畲族",
        "birth": "1986年6月",
        "birthplace": "福建蕉城金涵",
        "native_place": "福建蕉城",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "2008年7月",
        "current_post": "霞浦县委常委、宣传部部长",
        "current_org": "中共霞浦县委员会宣传部",
        "source": "上观新闻、新闻媒体",
        "notes": "1986年6月出生。2008年7月参加工作。曾任蕉城区九都镇副镇长。2024年9月任现职。",
        "confidence": "confirmed",
    },

    # ══════════════ County Government ══════════════

    # 陆鸣 — 副县长
    {
        "id": "xiapu_lu_ming",
        "name": "陆鸣",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年7月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "农工党员",
        "work_start": "",
        "current_post": "霞浦县副县长",
        "current_org": "霞浦县人民政府",
        "source": "xiapu.gov.cn/zwgk/ldzc/lm/",
        "notes": "农工党员（非中共）。负责教育、卫健、民政、市监、人社、医保、退役军人、妇儿、残疾人等工作。",
        "confidence": "confirmed",
    },

    # 张建勤 — 副县长/公安局长
    {
        "id": "xiapu_zhang_jianqin",
        "name": "张建勤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年4月",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县副县长、县公安局局长",
        "current_org": "霞浦县公安局",
        "source": "xiapu.gov.cn/zwgk/ldzc/ll/",
        "notes": "兼任县公安局党委书记、局长、督察长、县打私办主任、县委政法委副书记。"
             "负责公安、司法、信访、民兵预备役等工作。2024年任现职。",
        "confidence": "confirmed",
    },

    # 雷宇 — 副县长（畲族，外派挂职）
    {
        "id": "xiapu_lei_yu",
        "name": "雷宇",
        "gender": "男",
        "ethnicity": "畲族",
        "birth": "1984年9月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县副县长",
        "current_org": "霞浦县人民政府",
        "source": "xiapu.gov.cn/zwgk/ldzc/ly/",
        "notes": "外派挂职（分工标注为'外派挂职'）。县政府党组成员。",
        "confidence": "confirmed",
    },

    # 郑信旋 — 副县长
    {
        "id": "xiapu_zheng_xinxuan",
        "name": "郑信旋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年10月",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县副县长",
        "current_org": "霞浦县人民政府",
        "source": "xiapu.gov.cn/zwgk/ldzc/zxx/",
        "notes": "县政府党组成员。负责交通、文旅、体育、商务、口岸等工作。",
        "confidence": "confirmed",
    },

    # 陈义蜜 — 副县长
    {
        "id": "xiapu_chen_yimi",
        "name": "陈义蜜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年5月",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县副县长",
        "current_org": "霞浦县人民政府",
        "source": "xiapu.gov.cn/zwgk/ldzc/chenyimi/",
        "notes": "县政府党组成员。负责林业、自然资源、住建、城管、城市建设投资开发等工作。",
        "confidence": "confirmed",
    },

    # 陈广昱 — 副县长
    {
        "id": "xiapu_chen_guangyu",
        "name": "陈广昱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年10月",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县副县长",
        "current_org": "霞浦县人民政府",
        "source": "xiapu.gov.cn/zwgk/ldzc/chenguangyi/",
        "notes": "县政府党组成员。负责农业农村和乡村振兴、海洋渔业、水利、生态环境、民族宗教等工作。",
        "confidence": "confirmed",
    },

    # ══════════════ County People's Congress ══════════════

    # 陈旭 — 人大主任（原纪委书记转任）
    {
        "id": "xiapu_chen_xu",
        "name": "陈旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年6月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县人大常委会党组书记、主任",
        "current_org": "霞浦县人大常委会",
        "source": "xiapu.gov.cn 新闻报道、鲁网（任前公示）",
        "notes": "原任霞浦县委常委、县纪委书记、县监委主任。2024年12月拟任县人大政协正职。",
        "confidence": "confirmed",
    },

    # ══════════════ County Political Consultative Conference ══════════════

    # 陈文颂 — 政协主席
    {
        "id": "xiapu_chen_wensong",
        "name": "陈文颂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年8月",
        "birthplace": "福建霞浦",
        "native_place": "福建霞浦",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县政协主席",
        "current_org": "霞浦县政协",
        "source": "百度百科、新闻媒体",
        "notes": "霞浦本地人。曾任海岛乡乡长、下浒镇党委书记、县委办主任、副县长、县委常委/统战部长。"
             "2024年12月当选政协主席。",
        "confidence": "confirmed",
    },

    # ══════════════ Predecessors ══════════════

    # 郭文胜 — 前任县委书记
    {
        "id": "xiapu_guo_wensheng",
        "name": "郭文胜",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1968年3月",
        "birthplace": "福建福安",
        "native_place": "福建福州（生于福安）",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已卸任霞浦县委书记",
        "current_org": "",
        "source": "zh.wikipedia.org、新闻媒体",
        "notes": "2019年3月至2026年4月任霞浦县委书记。曾任蕉城区区长。2026年5月卸任，新职待确认。",
        "confidence": "confirmed",
    },

    # 王斌 — 前前任县委书记（落马）
    {
        "id": "xiapu_wang_bin",
        "name": "王斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年",
        "birthplace": "福建寿宁",
        "native_place": "福建寿宁",
        "education": "",
        "party_join": "中共党员（已被开除党籍）",
        "work_start": "",
        "current_post": "已被开除党籍、公职",
        "current_org": "",
        "source": "zh.wikipedia.org",
        "notes": "2014年7月至2019年2月任霞浦县委书记。因严重违纪违法被开除党籍、公职。"
             "此前曾任霞浦县县长。",
        "confidence": "confirmed",
    },

    # 郭元杰 — 县领导（出现在新闻报道中）
    {
        "id": "xiapu_guo_yuanjie",
        "name": "郭元杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "霞浦县领导",
        "current_org": "霞浦县人民政府",
        "source": "xiapu.gov.cn 新闻报道 (2026-07-10)",
        "notes": "出现在'罗义春开展四下基层活动'报道中，以'县领导'身份陪同调研。具体职务待确认。",
        "confidence": "plausible",
    },
]

organizations = [
    {"id": "cpc_xiapu", "name": "中共霞浦县委员会", "type": "党委", "level": "县", "parent": "中共宁德市委员会", "location": "福建省宁德市霞浦县"},
    {"id": "gov_xiapu", "name": "霞浦县人民政府", "type": "政府", "level": "县", "parent": "宁德市人民政府", "location": "福建省宁德市霞浦县"},
    {"id": "npc_xiapu", "name": "霞浦县人大常委会", "type": "人大", "level": "县", "parent": "", "location": "福建省宁德市霞浦县"},
    {"id": "cppcc_xiapu", "name": "霞浦县政协", "type": "政协", "level": "县", "parent": "", "location": "福建省宁德市霞浦县"},
    {"id": "dis_xiapu", "name": "中共霞浦县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共宁德市纪律检查委员会", "location": "福建省宁德市霞浦县"},
    {"id": "org_xiapu", "name": "中共霞浦县委员会组织部", "type": "党委", "level": "县", "parent": "中共霞浦县委员会", "location": "福建省宁德市霞浦县"},
    {"id": "prop_xiapu", "name": "中共霞浦县委员会宣传部", "type": "党委", "level": "县", "parent": "中共霞浦县委员会", "location": "福建省宁德市霞浦县"},
    {"id": "polit_xiapu", "name": "中共霞浦县委员会政法委员会", "type": "党委", "level": "县", "parent": "中共霞浦县委员会", "location": "福建省宁德市霞浦县"},
    {"id": "psb_xiapu", "name": "霞浦县公安局", "type": "政府", "level": "县", "parent": "霞浦县人民政府", "location": "福建省宁德市霞浦县"},
]


positions = [
    # 罗义春
    {"person_id": "xiapu_luo_yichun", "org_id": "cpc_xiapu", "title": "霞浦县委书记", "start": "2026-04", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "xiapu_luo_yichun", "org_id": "gov_xiapu", "title": "霞浦县长（前任）", "start": "2021-06", "end": "2026-04", "rank": "正处级", "note": "此前曾任县长，后升任县委书记"},
    # 蔡晶晶
    {"person_id": "xiapu_cai_jingjing", "org_id": "cpc_xiapu", "title": "霞浦县委副书记", "start": "2026-07", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiapu_cai_jingjing", "org_id": "gov_xiapu", "title": "霞浦县代县长", "start": "2026-07", "end": "present", "rank": "正处级", "note": "县政府党组书记"},
    # 伍银多
    {"person_id": "xiapu_wu_yinduo", "org_id": "cpc_xiapu", "title": "霞浦县委副书记", "start": "2023", "end": "present", "rank": "副处级", "note": "专职副书记"},
    # 吴国友
    {"person_id": "xiapu_wu_guoyou", "org_id": "cpc_xiapu", "title": "霞浦县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiapu_wu_guoyou", "org_id": "gov_xiapu", "title": "霞浦县常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组副书记"},
    # 蔡松根
    {"person_id": "xiapu_cai_songgen", "org_id": "cpc_xiapu", "title": "霞浦县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiapu_cai_songgen", "org_id": "gov_xiapu", "title": "霞浦县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 崔向新
    {"person_id": "xiapu_cui_xiangxin", "org_id": "cpc_xiapu", "title": "霞浦县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiapu_cui_xiangxin", "org_id": "polit_xiapu", "title": "霞浦县委政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 耿世谷
    {"person_id": "xiapu_geng_shigu", "org_id": "cpc_xiapu", "title": "霞浦县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiapu_geng_shigu", "org_id": "org_xiapu", "title": "霞浦县委组织部部长", "start": "", "end": "present", "rank": "副处级", "note": "曾任县委党校校长"},
    # 雷雯
    {"person_id": "xiapu_lei_wen", "org_id": "cpc_xiapu", "title": "霞浦县委常委", "start": "2024-09", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiapu_lei_wen", "org_id": "prop_xiapu", "title": "霞浦县委宣传部部长", "start": "2024-09", "end": "present", "rank": "副处级", "note": ""},
    # 陆鸣
    {"person_id": "xiapu_lu_ming", "org_id": "gov_xiapu", "title": "霞浦县副县长", "start": "", "end": "present", "rank": "副处级", "note": "农工党员"},
    # 张建勤
    {"person_id": "xiapu_zhang_jianqin", "org_id": "gov_xiapu", "title": "霞浦县副县长", "start": "2024", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiapu_zhang_jianqin", "org_id": "psb_xiapu", "title": "霞浦县公安局局长", "start": "2024", "end": "present", "rank": "副处级", "note": "党委书记、督察长、县打私办主任"},
    # 雷宇
    {"person_id": "xiapu_lei_yu", "org_id": "gov_xiapu", "title": "霞浦县副县长（外派挂职）", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员，外派挂职"},
    # 郑信旋
    {"person_id": "xiapu_zheng_xinxuan", "org_id": "gov_xiapu", "title": "霞浦县副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    # 陈义蜜
    {"person_id": "xiapu_chen_yimi", "org_id": "gov_xiapu", "title": "霞浦县副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    # 陈广昱
    {"person_id": "xiapu_chen_guangyu", "org_id": "gov_xiapu", "title": "霞浦县副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    # 陈旭
    {"person_id": "xiapu_chen_xu", "org_id": "npc_xiapu", "title": "霞浦县人大常委会主任", "start": "2025", "end": "present", "rank": "正处级", "note": "党组书记"},
    {"person_id": "xiapu_chen_xu", "org_id": "cpc_xiapu", "title": "霞浦县委常委、县纪委书记（前任）", "start": "", "end": "2024-12", "rank": "副处级", "note": "原任纪委书记、监委主任"},
    {"person_id": "xiapu_chen_xu", "org_id": "dis_xiapu", "title": "霞浦县纪委书记、监委主任（前任）", "start": "", "end": "2024-12", "rank": "副处级", "note": ""},
    # 陈文颂
    {"person_id": "xiapu_chen_wensong", "org_id": "cppcc_xiapu", "title": "霞浦县政协主席", "start": "2024-12", "end": "present", "rank": "正处级", "note": ""},
    # 郭文胜（前任书记）
    {"person_id": "xiapu_guo_wensheng", "org_id": "cpc_xiapu", "title": "霞浦县委书记（前任）", "start": "2019-03", "end": "2026-04", "rank": "正处级", "note": ""},
    # 王斌（前前任书记）
    {"person_id": "xiapu_wang_bin", "org_id": "cpc_xiapu", "title": "霞浦县委书记（前前任）", "start": "2014-07", "end": "2019-02", "rank": "正处级", "note": "被开除党籍、公职"},
    {"person_id": "xiapu_wang_bin", "org_id": "gov_xiapu", "title": "霞浦县长（前任）", "start": "2011", "end": "2014-07", "rank": "正处级", "note": "后升任县委书记"},
    # 郭元杰
    {"person_id": "xiapu_guo_yuanjie", "org_id": "gov_xiapu", "title": "霞浦县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
]


# ── Relationship edges ──────────────────────────────────────────────────

relationships = [
    # 罗义春 ↔ 蔡晶晶 (书记↔代县长，党政一把手搭档)
    {"person_a": "xiapu_luo_yichun", "person_b": "xiapu_cai_jingjing",
     "type": "superior_subordinate", "strength": "strong",
     "context": "党政一把手搭档，罗义春主持县委全面工作，蔡晶晶主持县政府全面工作",
     "overlap_org": "中共霞浦县委员会/霞浦县人民政府",
     "overlap_period": "2026年7月起", "confidence": "confirmed"},

    # 罗义春 ↔ 伍银多 (书记↔专职副书记)
    {"person_a": "xiapu_luo_yichun", "person_b": "xiapu_wu_yinduo",
     "type": "superior_subordinate", "strength": "strong",
     "context": "伍银多协助罗义春抓党的建设工作",
     "overlap_org": "中共霞浦县委员会",
     "overlap_period": "2023年起", "confidence": "confirmed"},

    # 蔡晶晶 ↔ 吴国友 (代县长↔常务副县长)
    {"person_a": "xiapu_cai_jingjing", "person_b": "xiapu_wu_guoyou",
     "type": "superior_subordinate", "strength": "strong",
     "context": "吴国友协助蔡晶晶负责县政府常务工作",
     "overlap_org": "霞浦县人民政府",
     "overlap_period": "2026年7月起", "confidence": "confirmed"},

    # 罗义春 ↔ 吴国友 (书记↔常务副县长)
    {"person_a": "xiapu_luo_yichun", "person_b": "xiapu_wu_guoyou",
     "type": "superior_subordinate", "strength": "strong",
     "context": "吴国友多次陪同罗义春调研（2026年7月防汛检查等）",
     "overlap_org": "中共霞浦县委员会/霞浦县人民政府",
     "overlap_period": "当前", "confidence": "confirmed"},

    # 罗义春 ↔ 陈旭 (原书记↔原纪委书记)
    {"person_a": "xiapu_luo_yichun", "person_b": "xiapu_chen_xu",
     "type": "overlap", "strength": "strong",
     "context": "陈旭原为县委常委、纪委书记，与罗义春在县委常委会共事。后转任人大主任。",
     "overlap_org": "中共霞浦县委员会",
     "overlap_period": "", "confidence": "confirmed"},

    # 郭文胜 ↔ 罗义春 (前任书记↔现任书记，predecessor_successor)
    {"person_a": "xiapu_guo_wensheng", "person_b": "xiapu_luo_yichun",
     "type": "predecessor_successor", "strength": "strong",
     "context": "郭文胜2019-2026任县委书记，罗义春2021-2026任县长（搭档），后接任书记",
     "overlap_org": "中共霞浦县委员会/霞浦县人民政府",
     "overlap_period": "2021-2026", "confidence": "confirmed"},

    # 王斌 ↔ 郭文胜 (前前任书记↔前任书记)
    {"person_a": "xiapu_wang_bin", "person_b": "xiapu_guo_wensheng",
     "type": "predecessor_successor", "strength": "strong",
     "context": "王斌2019年2月被开除党籍后，郭文胜2019年3月接任县委书记",
     "overlap_org": "中共霞浦县委员会",
     "overlap_period": "2019（交接）", "confidence": "confirmed"},

    # 陈旭 ↔ 陈文颂 (纪委书记转人大主任，统战部长转政协主席)
    {"person_a": "xiapu_chen_xu", "person_b": "xiapu_chen_wensong",
     "type": "overlap", "strength": "medium",
     "context": "2024年12月同时期分别转任人大主任和政协主席",
     "overlap_org": "中共霞浦县委员会/霞浦县人大/霞浦县政协",
     "overlap_period": "2024年起", "confidence": "confirmed"},

    # 雷雯 ↔ 蔡晶晶 (宣传部长↔代县长)
    {"person_a": "xiapu_lei_wen", "person_b": "xiapu_cai_jingjing",
     "type": "overlap", "strength": "medium",
     "context": "均为女性县领导，同在县委常委会",
     "overlap_org": "中共霞浦县委员会",
     "overlap_period": "2026年起", "confidence": "plausible"},
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
    lines.append('    <description>霞浦县领导班子工作关系网络 — 中共霞浦县委员会、霞浦县人民政府、县人大、县政协</description>')
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
        sz = "20.0" if is_top_leader(p) else ("8.0" if p["id"].startswith("xiapu_guo_") or p["id"].startswith("xiapu_wang_") else "12.0")
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
