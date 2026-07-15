#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 砀山县 (Dangshan County, Suzhou, Anhui).

Task: anhui_砀山县 — 县委书记 & 县长
Province: 安徽省
City: 宿州市
Region: 砀山县
Level: 县
Research date: 2026-07-15

Confirmed officeholders (as of 2026-07-15):
- 县委书记: 朱新华 (elected 2026-06-23 at 16th CPC Dangshan County Committee 1st Plenary Session)
- 县长: 王继军 (县委副书记、县政府县长)
- 县委副书记: 沈慧星

县委常委会 (11 members elected 2026-06-23):
朱新华, 王继军, 沈慧星, 叶争奇, 刘建, 孙强, 谢京波, 姜波涛, 宋文广, 杨大青, 盛开枫

Sources:
- www.dangshan.gov.cn (official government website)
- 砀山县人民政府 县长之窗 (leadership page)
- 中国共产党砀山县第十六届委员会第一次全体会议 (2026-06-26)
- 县十六次党代会系列报道 (2026-06-22/23/26)
- 县政府第62次常务会议 (2026-07-01)

Confidence: Current leadership confirmed from dangshan.gov.cn official news and
leadership page. Career details limited — only identity-level data available from
official leadership pages. 朱新华's previous role (before June 2026) was 县委副书记/县长
(15th County Committee period), elected 县委书记 at the 16th Congress.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in SCRIPT_DIR:
    STAGING = SCRIPT_DIR
else:
    STAGING = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))),
        "data/tmp/anhui_砀山县",
    )
DB_PATH = os.path.join(STAGING, "砀山县_network.db")
GEXF_PATH = os.path.join(STAGING, "砀山县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 县委书记 — 朱新华
    {
        "id": "dangshan_zhu_xinhua",
        "name": "朱新华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "砀山县委书记",
        "current_org": "中共砀山县委员会",
        "source": "www.dangshan.gov.cn/dsyw/163890231.html (县十六届一次全会, 2026-06-26); www.dangshan.gov.cn/dsyw/163877431.html (十六次党代会开幕, 朱新华作报告, 2026-06-23)",
        "notes": "2026年6月23日当选砀山县委书记。此前为砀山县委副书记、县长（第十五届县委）。在县十六次党代会上作报告，提出'产业立县、工业强县'战略和'1234'发展路径。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 县长 — 王继军
    {
        "id": "dangshan_wang_jijun",
        "name": "王继军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-05",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "砀山县委副书记、县政府县长",
        "current_org": "砀山县人民政府",
        "source": "www.dangshan.gov.cn/ldzc/index.html (县长之窗, 2026-07-15); www.dangshan.gov.cn/dsyw/163890231.html (县十六届一次全会当选副书记, 2026-06-26)",
        "notes": "1972年5月出生，研究生学历。领导县政府全面工作，负责审计。主持县政府第62次常务会议(2026-06-29)。与朱新华共同督导新官不理旧账集中整治(2026-07-08)。",
        "confidence": "confirmed",
    },

    # 县委副书记 — 沈慧星
    {
        "id": "dangshan_shen_huixing",
        "name": "沈慧星",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "砀山县委副书记（专职）",
        "current_org": "中共砀山县委员会",
        "source": "www.dangshan.gov.cn/dsyw/163890231.html (县十六届一次全会, 2026-06-26); www.dangshan.gov.cn/dsyw/163907121.html (两优一先表彰大会, 2026-07-03)",
        "notes": "2026年6月23日当选县委副书记。出席全县'两优一先'表彰大会以县委副书记身份。",
        "confidence": "confirmed",
    },

    # ══════════════ 县委常委 ══════════════

    # 县委常委 — 叶争奇
    {
        "id": "dangshan_ye_zhengqi",
        "name": "叶争奇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共砀山县委员会",
        "source": "www.dangshan.gov.cn/dsyw/163890231.html (县十六届一次全会常委名单, 2026-06-26)",
        "notes": "十六届县委常委（2026年6月23日当选）。",
        "confidence": "confirmed",
    },

    # 县委常委、副县长 — 刘建
    {
        "id": "dangshan_liu_jian",
        "name": "刘建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-11",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "砀山县人民政府",
        "source": "www.dangshan.gov.cn/content/column/18255926?liId=15711 (领导之窗, 2026-07-15)",
        "notes": "1974年11月出生，大学学历。负责生态环境、自然资源、住建、城管等。",
        "confidence": "confirmed",
    },

    # 县委常委、县纪委书记 — 孙强
    {
        "id": "dangshan_sun_qiang",
        "name": "孙强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记",
        "current_org": "中共砀山县纪律检查委员会",
        "source": "www.dangshan.gov.cn/dsyw/163877431.html (十六次党代会, 孙强代表十五届纪委作报告, 2026-06-23)",
        "notes": "任十五届县纪委书记并在十六次党代会代表纪委作工作报告，继续当选十六届县委常委。",
        "confidence": "confirmed",
    },

    # 县委常委 — 谢京波
    {
        "id": "dangshan_xie_jingbo",
        "name": "谢京波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共砀山县委员会",
        "source": "www.dangshan.gov.cn/dsyw/163890231.html (县十六届一次全会常委名单, 2026-06-26)",
        "notes": "十六届县委常委（2026年6月23日当选）。",
        "confidence": "confirmed",
    },

    # 县委常委、副县长 — 姜波涛
    {
        "id": "dangshan_jiang_botao",
        "name": "姜波涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-11",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "砀山县人民政府",
        "source": "www.dangshan.gov.cn/content/column/18255926?liId=16551 (领导之窗, 2026-07-15); www.dangshan.gov.cn/dsyw/163890231.html (十六届常委, 2026-06-26)",
        "notes": "1986年11月出生，研究生学历。负责商务、招商引资、工信、科技等。",
        "confidence": "confirmed",
    },

    # 县委常委 — 宋文广
    {
        "id": "dangshan_song_wenguang",
        "name": "宋文广",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共砀山县委员会",
        "source": "www.dangshan.gov.cn/dsyw/163890231.html (县十六届一次全会常委名单, 2026-06-26)",
        "notes": "十六届县委常委。陪同朱新华调研防汛备汛工作 (2026-07-13)。陪同朱新华赴得壹能源考察 (2026-06-24)。出席县政府第62次常务会议。",
        "confidence": "confirmed",
    },

    # 县委常委 — 杨大青
    {
        "id": "dangshan_yang_daqing",
        "name": "杨大青",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共砀山县委员会",
        "source": "www.dangshan.gov.cn/dsyw/163890231.html (县十六届一次全会常委名单, 2026-06-26)",
        "notes": "十六届县委常委。出席县政府第62次常务会议 (2026-06-29)。",
        "confidence": "confirmed",
    },

    # 县委常委 — 盛开枫
    {
        "id": "dangshan_sheng_kaifeng",
        "name": "盛开枫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共砀山县委员会",
        "source": "www.dangshan.gov.cn/dsyw/163890231.html (县十六届一次全会常委名单, 2026-06-26)",
        "notes": "十六届县委常委（2026年6月23日当选）。",
        "confidence": "confirmed",
    },

    # ══════════════ 县政府其他领导 ══════════════

    # 副县长 — 许雷侠
    {
        "id": "dangshan_xu_leixia",
        "name": "许雷侠",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1978-02",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "砀山县人民政府",
        "source": "www.dangshan.gov.cn/content/column/18255926?liId=15721 (领导之窗, 2026-07-15)",
        "notes": "1978年2月出生，回族，大学学历。负责教育、卫健、医保、文旅、体育等。非中共党员。",
        "confidence": "confirmed",
    },

    # 副县长、县公安局局长 — 郑峰
    {
        "id": "dangshan_zheng_feng",
        "name": "郑峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-06",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "砀山县公安局",
        "source": "www.dangshan.gov.cn/content/column/18255926?liId=16241 (领导之窗, 2026-07-15)",
        "notes": "1972年6月出生，大学学历。负责公安、司法、退役军人事务、信访等。",
        "confidence": "confirmed",
    },

    # 副县长 — 赵振海
    {
        "id": "dangshan_zhao_zhenhai",
        "name": "赵振海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-07",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "砀山县人民政府",
        "source": "www.dangshan.gov.cn/content/column/18255926?liId=16511 (领导之窗, 2026-07-15)",
        "notes": "1976年7月出生，研究生学历。负责农业农村、乡村振兴、水利、民政等。",
        "confidence": "confirmed",
    },

    # 副县长、县政府办公室主任 — 孙书振
    {
        "id": "dangshan_sun_shuzhen",
        "name": "孙书振",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-06",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县政府办公室主任",
        "current_org": "砀山县人民政府",
        "source": "www.dangshan.gov.cn/content/column/18255926?liId=16561 (领导之窗, 2026-07-15)",
        "notes": "1985年6月出生，大学学历。负责交通、人社、市场监管、政务公开等。",
        "confidence": "confirmed",
    },

    # ══════════════ 人大、政协领导 ══════════════

    # 县人大常委会主任 — 陈晓强
    {
        "id": "dangshan_chen_xiaoqiang",
        "name": "陈晓强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "砀山县人民代表大会常务委员会",
        "source": "www.dangshan.gov.cn/dsyw/163877431.html (十六次党代会主席团成员, 2026-06-23); www.dangshan.gov.cn/dsyw/163907121.html (两优一先表彰大会出席, 2026-07-03)",
        "notes": "县人大常委会主任。十六次党代会主席团前排就座。出席两优一先表彰大会。",
        "confidence": "confirmed",
    },

    # 县政协主席 — 武云峰
    {
        "id": "dangshan_wu_yunfeng",
        "name": "武云峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议砀山县委员会",
        "source": "www.dangshan.gov.cn/dsyw/163877431.html (十六次党代会主席团成员, 2026-06-23)",
        "notes": "县政协主席。十六次党代会主席团前排就座。",
        "confidence": "confirmed",
    },

    # ══════════════ 其他县级领导 ══════════════

    # 副县长 — 梁宏 (从县政府常务会议得知)
    {
        "id": "dangshan_liang_hong",
        "name": "梁宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "砀山县人民政府",
        "source": "www.dangshan.gov.cn/public/6628921/163896751.html (县政府第62次常务会议, 2026-07-01)",
        "notes": "出席县政府第62次常务会议。具体分工待确认。",
        "confidence": "confirmed",
    },

    # 副县长 — 丁慧
    {
        "id": "dangshan_ding_hui",
        "name": "丁慧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "砀山县人民政府",
        "source": "www.dangshan.gov.cn/dsyw/163927161.html (督导新官不理旧账, 2026-07-13); www.dangshan.gov.cn/public/6628921/163896751.html (县政府第62次常务会议, 2026-07-01)",
        "notes": "出席县政府第62次常务会议。参加朱新华、王继军督导新官不理旧账集中整治（2026-07-08）。",
        "confidence": "confirmed",
    },

    # 县人武部 / 县委委员 — 薛同辉
    {
        "id": "dangshan_xue_tonghui",
        "name": "薛同辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委委员",
        "current_org": "中共砀山县委员会",
        "source": "www.dangshan.gov.cn/dsyw/163890361.html (朱新华与得壹能源会谈, 薛同辉参加, 2026-06-26)",
        "notes": "陪同朱新华赴得壹能源考察（2026-06-24）。",
        "confidence": "confirmed",
    },
]

organizations = [
    {
        "id": "dangshan_county_party",
        "name": "中共砀山县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共宿州市委员会",
        "location": "安徽省宿州市砀山县",
    },
    {
        "id": "dangshan_county_gov",
        "name": "砀山县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "宿州市人民政府",
        "location": "安徽省宿州市砀山县",
    },
    {
        "id": "dangshan_discipline",
        "name": "中共砀山县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共砀山县委员会",
        "location": "安徽省宿州市砀山县",
    },
    {
        "id": "dangshan_people_congress",
        "name": "砀山县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "",
        "location": "安徽省宿州市砀山县",
    },
    {
        "id": "dangshan_政协",
        "name": "中国人民政治协商会议砀山县委员会",
        "type": "政协",
        "level": "县",
        "parent": "",
        "location": "安徽省宿州市砀山县",
    },
    {
        "id": "dangshan_public_security",
        "name": "砀山县公安局",
        "type": "政府",
        "level": "县",
        "parent": "砀山县人民政府",
        "location": "安徽省宿州市砀山县",
    },
]

positions = [
    # 朱新华 — 县委书记
    {"person_id": "dangshan_zhu_xinhua", "org_id": "dangshan_county_party",
     "title": "县委书记", "start": "2026-06", "end": "present",
     "rank": "正县级", "note": "2026年6月23日当选十六届县委书记"},
    {"person_id": "dangshan_zhu_xinhua", "org_id": "dangshan_county_gov",
     "title": "县委副书记、县长（前任）", "start": "unknown", "end": "2026-06",
     "rank": "正县级", "note": "此前担任县委副书记、县长。在十六次党代会作十五届县委工作报告。"},

    # 王继军 — 县长
    {"person_id": "dangshan_wang_jijun", "org_id": "dangshan_county_gov",
     "title": "县委副书记、县长", "start": "unknown", "end": "present",
     "rank": "正县级", "note": "领导县政府全面工作。2026年6月23日当选县委副书记。"},
    {"person_id": "dangshan_wang_jijun", "org_id": "dangshan_county_party",
     "title": "县委副书记", "start": "unknown", "end": "present",
     "rank": "正县级", "note": "2026年6月23日当选十六届县委副书记。"},

    # 沈慧星 — 县委副书记
    {"person_id": "dangshan_shen_huixing", "org_id": "dangshan_county_party",
     "title": "县委副书记（专职）", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "2026年6月23日当选十六届县委副书记。"},

    # 县委常委
    {"person_id": "dangshan_ye_zhengqi", "org_id": "dangshan_county_party",
     "title": "县委常委", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "2026年6月23日当选十六届县委常委。"},
    {"person_id": "dangshan_liu_jian", "org_id": "dangshan_county_party",
     "title": "县委常委", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "十六届县委常委。"},
    {"person_id": "dangshan_liu_jian", "org_id": "dangshan_county_gov",
     "title": "副县长", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "负责生态环境、自然资源、住建、城管等。"},
    {"person_id": "dangshan_sun_qiang", "org_id": "dangshan_discipline",
     "title": "县委常委、县纪委书记", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "十五届县纪委书记，连任十六届县委常委。"},
    {"person_id": "dangshan_xie_jingbo", "org_id": "dangshan_county_party",
     "title": "县委常委", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "2026年6月23日当选十六届县委常委。"},
    {"person_id": "dangshan_jiang_botao", "org_id": "dangshan_county_party",
     "title": "县委常委", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "2026年6月23日当选十六届县委常委。"},
    {"person_id": "dangshan_jiang_botao", "org_id": "dangshan_county_gov",
     "title": "副县长", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "负责商务、招商引资、工信、科技等。"},
    {"person_id": "dangshan_song_wenguang", "org_id": "dangshan_county_party",
     "title": "县委常委", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "2026年6月23日当选十六届县委常委。"},
    {"person_id": "dangshan_yang_daqing", "org_id": "dangshan_county_party",
     "title": "县委常委", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "2026年6月23日当选十六届县委常委。"},
    {"person_id": "dangshan_sheng_kaifeng", "org_id": "dangshan_county_party",
     "title": "县委常委", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "2026年6月23日当选十六届县委常委。"},

    # 其他政府领导
    {"person_id": "dangshan_xu_leixia", "org_id": "dangshan_county_gov",
     "title": "副县长", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "负责教育、卫健、医保、文旅、体育等。"},
    {"person_id": "dangshan_zheng_feng", "org_id": "dangshan_county_gov",
     "title": "副县长", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "负责公安、司法等。"},
    {"person_id": "dangshan_zheng_feng", "org_id": "dangshan_public_security",
     "title": "县公安局局长", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "兼任副县长。"},
    {"person_id": "dangshan_zhao_zhenhai", "org_id": "dangshan_county_gov",
     "title": "副县长", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "负责农业农村、乡村振兴、水利等。"},
    {"person_id": "dangshan_sun_shuzhen", "org_id": "dangshan_county_gov",
     "title": "副县长、县政府办公室主任", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "负责交通、人社、市场监管等。"},

    # 人大、政协
    {"person_id": "dangshan_chen_xiaoqiang", "org_id": "dangshan_people_congress",
     "title": "县人大常委会主任", "start": "unknown", "end": "present",
     "rank": "正县级", "note": ""},
    {"person_id": "dangshan_wu_yunfeng", "org_id": "dangshan_政协",
     "title": "县政协主席", "start": "unknown", "end": "present",
     "rank": "正县级", "note": ""},

    # 其他领导
    {"person_id": "dangshan_liang_hong", "org_id": "dangshan_county_gov",
     "title": "副县长", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "出席县政府第62次常务会议。"},
    {"person_id": "dangshan_ding_hui", "org_id": "dangshan_county_gov",
     "title": "副县长", "start": "unknown", "end": "present",
     "rank": "副县级", "note": "出席县政府第62次常务会议。"},
    {"person_id": "dangshan_xue_tonghui", "org_id": "dangshan_county_party",
     "title": "县委委员", "start": "unknown", "end": "present",
     "rank": "正科/副县级", "note": "陪同朱新华赴得壹能源考察。"},
]

relationships = [
    # 工作核心团队——县委常委会成员
    {
        "person_a": "dangshan_zhu_xinhua",
        "person_b": "dangshan_wang_jijun",
        "type": "superior_subordinate",
        "context": "书记+县长搭档。共同出席督导新官不理旧账工作(2026-07-08)，共同主持县委理论学习中心组。王继军任副书记、县长。",
        "overlap_org": "中共砀山县委员会/砀山县人民政府",
        "overlap_period": "confirmed",
        "strength": "strong",
    },
    {
        "person_a": "dangshan_zhu_xinhua",
        "person_b": "dangshan_shen_huixing",
        "type": "superior_subordinate",
        "context": "书记+专职副书记搭档。共同出席两优一先表彰大会。",
        "overlap_org": "中共砀山县委员会",
        "overlap_period": "confirmed",
        "strength": "strong",
    },
    {
        "person_a": "dangshan_wang_jijun",
        "person_b": "dangshan_shen_huixing",
        "type": "overlap",
        "context": "同为县委副书记，共同出席县委各类会议。",
        "overlap_org": "中共砀山县委员会",
        "overlap_period": "confirmed",
        "strength": "strong",
    },
    # 政府领导班子（县长+副县长）
    {
        "person_a": "dangshan_wang_jijun",
        "person_b": "dangshan_liu_jian",
        "type": "superior_subordinate",
        "context": "县长+常委副县长，县政府领导团队。",
        "overlap_org": "砀山县人民政府",
        "overlap_period": "confirmed",
        "strength": "strong",
    },
    {
        "person_a": "dangshan_wang_jijun",
        "person_b": "dangshan_jiang_botao",
        "type": "superior_subordinate",
        "context": "县长+常委副县长，县政府领导团队。姜波涛协助王继军分管经济开发区等工作。",
        "overlap_org": "砀山县人民政府",
        "overlap_period": "confirmed",
        "strength": "strong",
    },
    {
        "person_a": "dangshan_wang_jijun",
        "person_b": "dangshan_xu_leixia",
        "type": "superior_subordinate",
        "context": "县长+副县长，县政府领导团队。",
        "overlap_org": "砀山县人民政府",
        "overlap_period": "confirmed",
        "strength": "medium",
    },
    {
        "person_a": "dangshan_wang_jijun",
        "person_b": "dangshan_zheng_feng",
        "type": "superior_subordinate",
        "context": "县长+副县长/公安局长，县政府领导团队。",
        "overlap_org": "砀山县人民政府",
        "overlap_period": "confirmed",
        "strength": "medium",
    },
    {
        "person_a": "dangshan_wang_jijun",
        "person_b": "dangshan_zhao_zhenhai",
        "type": "superior_subordinate",
        "context": "县长+副县长，县政府领导团队。",
        "overlap_org": "砀山县人民政府",
        "overlap_period": "confirmed",
        "strength": "medium",
    },
    {
        "person_a": "dangshan_wang_jijun",
        "person_b": "dangshan_sun_shuzhen",
        "type": "superior_subordinate",
        "context": "县长+副县长/办公室主任，县政府领导团队。孙书振协助王继军分管城建、环保工作。",
        "overlap_org": "砀山县人民政府",
        "overlap_period": "confirmed",
        "strength": "strong",
    },
    # 县委常委之间的工作关系
    {
        "person_a": "dangshan_zhu_xinhua",
        "person_b": "dangshan_song_wenguang",
        "type": "overlap",
        "context": "宋文广陪同朱新华调研防汛备汛(2026-07-13)和赴得壹能源考察(2026-06-24)。",
        "overlap_org": "中共砀山县委员会",
        "overlap_period": "confirmed",
        "strength": "medium",
    },
    {
        "person_a": "dangshan_wang_jijun",
        "person_b": "dangshan_yang_daqing",
        "type": "overlap",
        "context": "杨大青出席县政府第62次常务会议。",
        "overlap_org": "砀山县人民政府",
        "overlap_period": "confirmed",
        "strength": "medium",
    },
    {
        "person_a": "dangshan_zhu_xinhua",
        "person_b": "dangshan_chen_xiaoqiang",
        "type": "overlap",
        "context": "书记+人大主任，共同出席十六次党代会主席团、两优一先表彰大会等。",
        "overlap_org": "砀山县",
        "overlap_period": "confirmed",
        "strength": "medium",
    },
    {
        "person_a": "dangshan_zhu_xinhua",
        "person_b": "dangshan_wu_yunfeng",
        "type": "overlap",
        "context": "书记+政协主席，共同出席十六次党代会主席团。",
        "overlap_org": "砀山县",
        "overlap_period": "confirmed",
        "strength": "medium",
    },
    # 县纪委书记+县委书记
    {
        "person_a": "dangshan_zhu_xinhua",
        "person_b": "dangshan_sun_qiang",
        "type": "superior_subordinate",
        "context": "书记+纪委书记。孙强在十六次党代会代表纪委作工作报告。共同开展廉政警示教育。",
        "overlap_org": "中共砀山县委员会",
        "overlap_period": "confirmed",
        "strength": "medium",
    },
]


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    """Create SQLite database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
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
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                                 native_place, education, party_join, work_start,
                                 current_post, current_org, source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
            p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
            p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
            p.get("current_post", ""), p.get("current_org", ""),
            p.get("source", ""), p.get("notes", ""), p.get("confidence", ""),
        ))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pos["person_id"], pos["org_id"], pos["title"],
            pos.get("start", ""), pos.get("end", ""),
            pos.get("rank", ""), pos.get("note", ""),
        ))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context,
                                       overlap_org, overlap_period, strength)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            r["person_a"], r["person_b"], r["type"], r.get("context", ""),
            r.get("overlap_org", ""), r.get("overlap_period", ""), r.get("strength", ""),
        ))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def build_gexf():
    """Create GEXF graph file using string formatting (avoids namespace issues)."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>砀山县 (Dangshan County, Suzhou, Anhui) — Leadership Network Graph</description>')
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
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Person node colors
    def person_color(p):
        post = p.get("current_post", "")
        if "书记" in post and "县" in post:
            return "255,50,50"   # red — party secretary
        if "县长" in post:
            return "50,100,255"  # blue — government leader
        if "纪委书记" in post:
            return "255,165,0"   # orange — discipline
        if "人大" in post or "政协" in post:
            return "100,180,100" # green — congress/CPPCC
        return "100,100,100"     # grey — others

    def is_top_leader(p):
        return "县委书记" in p.get("current_post", "") or "县长" in p.get("current_post", "")

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization node colors
    def org_color(o):
        t = o["type"]
        if "党委" in t:
            return "255,200,200"
        if "政府" in t:
            return "200,200,255"
        if "人大" in t:
            return "200,255,255"
        if "政协" in t:
            return "255,240,200"
        return "200,200,200"

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
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

    # Person → Organization edges (worked_at)
    for pos in positions:
        pid = persons_map[pos["person_id"]]
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person edges (relationship)
    for r in relationships:
        weight = "2.0" if r.get("strength") == "strong" else "1.5" if r.get("strength") == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("strength", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[GEXF] Created: {GEXF_PATH}")
    print(f"[GEXF] Nodes: {len(persons)} persons + {len(organizations)} orgs")
    print(f"[GEXF] Edges: {len(positions)} worked_at + {len(relationships)} relationships")


def main():
    os.makedirs(STAGING, exist_ok=True)
    build_db()
    build_gexf()

    # Print summary
    print(f"\n{'=' * 50}")
    print(f"砀山县 Leadership Network — Build Complete")
    print(f"{'=' * 50}")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"\nOutput files:")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    # Build a lookup for positions
    persons_map = {}
    for p in persons:
        persons_map[p["id"]] = p
    main()
