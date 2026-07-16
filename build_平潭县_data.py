#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 平潭县 (Pingtan County, Fuzhou, Fujian).

Task: fujian_平潭县 — 县委书记 & 县长
Province: 福建省
City: 福州市
Region: 平潭县
Level: 县
Research date: 2026-07-16

Key structural note: 平潭综合实验区与平潭县实行"区县合一"体制。
实验区党工委书记兼平潭县委书记, 实验区管委会主任兼平潭县长。

Confirmed officeholders (as of 2026-07-16):
- 县委书记: 赖军 (实验区党工委书记兼, 2021年8月起任)
- 县长: 黄建波 (实验区管委会主任兼, 2021年8月起任)

Sources:
- 平潭综合实验区党工委管委会门户网站领导之窗 (pingtan.gov.cn)
- 人民网 — 赖军/黄建波2021年8月任命报道
- 平潭网 (ptnet.cn) — 2026年新闻确认在任
- 福州新闻网 — 2026年管委会会议报道
- 百度百科 — 赖军词条, 陈善光词条, 张兆民词条, 何杰民词条, 方良栋词条, 陈训明词条
- 中文维基百科 — 赖军, 陈善光, 张兆民
- 平潭综合实验区管委会官网 — 领导分工页面
- 中国日报网 — 黄建波2025年全国两会采访

Confidence: Current leadership confirmed from multiple official/news sources.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING = SCRIPT_DIR
DB_PATH = os.path.join(STAGING, "平潭县_network.db")
GEXF_PATH = os.path.join(STAGING, "平潭县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 县委书记 / 实验区党工委书记 — 赖军
    {
        "id": "pingtan_lai_jun",
        "name": "赖军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年1月",
        "birthplace": "重庆云阳",
        "native_place": "重庆云阳",
        "education": "公共管理硕士",
        "party_join": "1995年5月",
        "work_start": "1990年8月",
        "current_post": "平潭综合实验区党工委书记、平潭县委书记",
        "current_org": "中共平潭综合实验区工作委员会 / 中共平潭县委员会",
        "source": "中文维基百科（赖军词条）; 人民网（2021-08-07任命报道）; 平潭网（2026-01-01经济工作会议报道）",
        "notes": "1990年厦门大学海洋生物学专业毕业。历任：共青团福建省委副书记（2003）、共青团福建省委书记（2011.09）、莆田市委副书记（2015.02）、福建省民政厅厅长（2016.09）、福建省水利厅党组书记兼厅长（2018.03）、平潭综合实验区党工委书记兼平潭县委书记（2021.08-今）。",
        "confidence": "confirmed",
    },

    # 县长 / 实验区管委会主任 — 黄建波
    {
        "id": "pingtan_huang_jianbo",
        "name": "黄建波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年8月",
        "birthplace": "福建",
        "native_place": "福建",
        "education": "在职研究生，工学博士",
        "party_join": "中共党员",
        "work_start": "1993年8月",
        "current_post": "平潭综合实验区党工委副书记、管委会主任、平潭县县长",
        "current_org": "平潭综合实验区管委会 / 平潭县人民政府",
        "source": "平潭综合实验区管委会官网领导简介; 人民网（2021-08-07任命报道）; 福州新闻网（2026-02-04管委会全体会议报道）; 中国日报网（2025-03-11两会采访）",
        "notes": "历任：厦门大学基建处副处长、共青团福建省委常委、福建省青联副主席、三明市三元区委书记（2011）、三明市台商投资区党工委书记（2016）、福建省工信厅副厅长、福建省大数据管理局局长、平潭综合实验区管委会主任兼平潭县县长（2021.08-今）。",
        "confidence": "confirmed",
    },

    # ══════════════ Key Deputy Leaders ══════════════

    # 县委副书记 / 实验区党工委副书记 — 文学林
    {
        "id": "pingtan_wen_xuelin",
        "name": "文学林",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1975年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "工商管理硕士",
        "party_join": "中共党员",
        "work_start": "1996年8月",
        "current_post": "平潭综合实验区党工委副书记、省政协平潭工委主任（兼平潭县政协主席）",
        "current_org": "中共平潭综合实验区工作委员会",
        "source": "平潭综合实验区管委会官网领导之窗（文学林页面）",
        "notes": "2024年7月起任党工委副书记。分工：协助书记抓党的建设工作，负责党群工作（组织人事、机构编制、统战、民族宗教）、自贸试验与深化改革工作、对台工作、农村工作、基层治理。此前为吴礼源（2023年7月调任福建省能源石化集团, 2026年7月被查）。",
        "confidence": "plausible",
    },

    # 纪委书记 — 黄惠元
    {
        "id": "pingtan_huang_huiyuan",
        "name": "黄惠元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年3月",
        "birthplace": "福建",
        "native_place": "福建",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1989年8月",
        "current_post": "平潭综合实验区党工委委员、纪工委书记、监察工委主任（兼平潭县纪委书记、监委主任）",
        "current_org": "中共平潭综合实验区纪工委 / 平潭县纪委",
        "source": "平潭综合实验区管委会官网领导之窗（黄惠元页面）",
        "notes": "负责纪律检查、监察工作，分管巡察工作。",
        "confidence": "plausible",
    },

    # 管委会副主任 / 副县长 — 何杰民
    {
        "id": "pingtan_he_jiemin",
        "name": "何杰民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年7月",
        "birthplace": "福建永泰",
        "native_place": "福建永泰",
        "education": "大学，文学硕士",
        "party_join": "1993年5月",
        "work_start": "1993年8月",
        "current_post": "平潭综合实验区党工委委员、管委会副主任（兼平潭县副县长）",
        "current_org": "平潭综合实验区管委会 / 平潭县人民政府",
        "source": "百度百科（何杰民词条）; 平潭综合实验区管委会官网领导之窗",
        "notes": "福建师范大学中文系毕业。历任：福州师范高等专科学校教师→福州团市委副书记→福州团市委书记→长乐市委副书记→仓山区区长（2012-2014）→罗源县委书记（2014-2020）→福州新区管委会副主任、长乐区委书记（2020-2022年9月）→平潭综合实验区党工委委员、管委会副主任（2022年9月-今）。跨县域经历：永泰（出生地）→福州→长乐→罗源→长乐→平潭。",
        "confidence": "confirmed",
    },

    # 管委会副主任 / 副县长 — 陈训明
    {
        "id": "pingtan_chen_xunming",
        "name": "陈训明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年2月",
        "birthplace": "福建福清",
        "native_place": "福建福清",
        "education": "在职博士，管理学博士",
        "party_join": "1996年",
        "work_start": "1997年8月",
        "current_post": "平潭综合实验区党工委委员、管委会副主任（兼平潭县副县长）",
        "current_org": "平潭综合实验区管委会 / 平潭县人民政府",
        "source": "百度百科（陈训明词条）; 平潭综合实验区管委会官网领导之窗",
        "notes": "福建师范大学中文系毕业。历任：福建师范大学团委→共青团福建省委办公室、学校部、统战部→宣传部副部长→福建青年杂志社社长→省团委少年部部长、常委、办公室主任→省团委副书记→平潭综合实验区管委会副主任（2021年5月）→党工委委员、管委会副主任（2023年3月-今）。福建福清人（福清与平潭相邻）。",
        "confidence": "confirmed",
    },

    # 管委会副主任 — 方良栋
    {
        "id": "pingtan_fang_liangdong",
        "name": "方良栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年6月",
        "birthplace": "福建平潭",
        "native_place": "福建平潭",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "1991年8月",
        "current_post": "平潭综合实验区党工委委员、管委会副主任（兼平潭县副县长）",
        "current_org": "平潭综合实验区管委会 / 平潭县人民政府",
        "source": "百度百科（方良栋词条）; 平潭综合实验区管委会官网领导之窗",
        "notes": "平潭本地成长干部。历任：平潭县人大办秘书、副主任→澳前镇人大主席、苏澳镇党委书记→平潭县副县长、综合执法局局长→综合执法局党组书记、局长→海坛片区管理局党委书记、局长→平潭综合实验区管委会副主任（2022年7月）→党工委委员（2025年5月-今）。",
        "confidence": "confirmed",
    },

    # 党工委委员 — 潘新雅
    {
        "id": "pingtan_pan_xinya",
        "name": "潘新雅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年12月",
        "birthplace": "福建永春",
        "native_place": "福建永春",
        "education": "大学，高级工程师",
        "party_join": "中共党员",
        "work_start": "1991年8月",
        "current_post": "平潭综合实验区党工委委员",
        "current_org": "中共平潭综合实验区工作委员会",
        "source": "平潭综合实验区管委会官网领导之窗（潘新雅页面）",
        "notes": "高级工程师。历任：永春县建委→永春县交通局副局长→泉州市丰泽区西湖旅游建设管理处主任→泉州市交通运输委员会党组书记、主任→平潭交建局党组书记、局长（2018年9月）→平潭综合实验区党工委委员（2023年3月-今）。分工：国防动员、交通运输、住建、共青团、妇联、办公室工作。",
        "confidence": "plausible",
    },

    # 管委会副主任 — 孙树群
    {
        "id": "pingtan_sun_shuqun",
        "name": "孙树群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年8月",
        "birthplace": "福建宁化",
        "native_place": "福建宁化",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "1992年8月",
        "current_post": "平潭综合实验区管委会副主任（兼平潭县副县长）",
        "current_org": "平潭综合实验区管委会 / 平潭县人民政府",
        "source": "平潭综合实验区管委会官网领导之窗（孙树群页面）; 人民网",
        "notes": "历任：平潭环境与国土资源局副局长（主持工作）→局长→苏平片区管理局党委书记、局长、苏平镇党委书记、镇长→区检察院二级巡视员→党工委管委会办公室二级巡视员→管委会副主任（2025年3月任，试用期一年）。分工：政府投资项目建设、资源生态（自然资源、环保、征地、海洋、城乡规划）。",
        "confidence": "plausible",
    },

    # ══════════════ Predecessors ══════════════

    # 前任县委书记 / 实验区党工委书记 — 陈善光
    {
        "id": "pingtan_chen_shanguang",
        "name": "陈善光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年7月",
        "birthplace": "福建连江",
        "native_place": "福建连江",
        "education": "省委党校研究生",
        "party_join": "1985年",
        "work_start": "1982年8月",
        "current_post": "福建省人大常委会社会委员会主任委员（已离任平潭）",
        "current_org": "福建省人大常委会",
        "source": "中文维基百科（陈善光词条）; 百度百科（陈善光词条）",
        "notes": "历任：福建省纪委办公厅主任→福建省纪委常委、省监察厅副厅长→福建省纪委副书记、省监察厅厅长、省监委副主任→平潭综合实验区党工委书记兼平潭县委书记（2018.07-2021.08）→福建省人大常委会社会委员会主任委员（2022.01-今）。连江人，连江县与平潭均属福州。",
        "confidence": "confirmed",
    },

    # 前任县委书记 / 实验区党工委书记 — 张兆民
    {
        "id": "pingtan_zhang_zhaomin",
        "name": "张兆民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962年3月",
        "birthplace": "福建邵武",
        "native_place": "福建邵武",
        "education": "省委党校大学",
        "party_join": "1984年12月",
        "work_start": "1981年8月",
        "current_post": "福建省政协副主席（2026年1月已届满离任）",
        "current_org": "福建省政协",
        "source": "中文维基百科（张兆民词条）; 百度百科（张兆民词条）",
        "notes": "历任：南平市委常委、副市长→龙岩市代市长、市长→福建省交通运输厅党组书记、厅长→平潭综合实验区党工委书记兼平潭县委书记（2015.12-2018.07）→福建省政协副主席（2018.01-2026.01）。",
        "confidence": "confirmed",
    },

    # 前任县委书记 / 实验区党工委书记 — 龚清概
    {
        "id": "pingtan_gong_qinggai",
        "name": "龚清概",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1958年6月",
        "birthplace": "福建石狮",
        "native_place": "福建石狮",
        "education": "在职大学",
        "party_join": "1980年10月",
        "work_start": "1978年10月",
        "current_post": "无（已落马）",
        "current_org": "",
        "source": "中文维基百科; 中央纪委国家监委网站",
        "notes": "平潭综合实验区首任党工委书记/管委会主任（2009-2013）。历任：晋江市市长、晋江市委书记→泉州市委副书记→福建省政府副秘书长、省台办主任→平潭综合实验区党工委书记、管委会主任→福建省副省长（2013）→中央台办、国台办副主任（2014）。2016年被调查。",
        "confidence": "confirmed",
    },

    # 前任实验区管委会主任 / 县长相关 — 林文耀
    {
        "id": "pingtan_lin_wenyao",
        "name": "林文耀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年",
        "birthplace": "福建",
        "native_place": "福建",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "1984年8月",
        "current_post": "已离任",
        "current_org": "",
        "source": "中文维基百科; 新闻搜索",
        "notes": "历任：福建省政府办公厅副主任→福建省卫生厅副厅长→平潭综合实验区管委会主任兼平潭县长（2017-2021）→离任。",
        "confidence": "plausible",
    },

    # ══════════════ Cross-County Connection Figures ══════════════

    # 吴礼源 — 前任党工委副书记（2023年调出, 2026年被查）
    {
        "id": "pingtan_wu_liyuan",
        "name": "吴礼源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年",
        "birthplace": "福建",
        "native_place": "福建",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1995年8月",
        "current_post": "无（被调查）",
        "current_org": "",
        "source": "新闻搜索",
        "notes": "平潭综合实验区原党工委副书记（前任文学林的前任）。2023年7月调任福建省能源石化集团。2026年7月因涉嫌严重违纪违法被调查。",
        "confidence": "plausible",
    },
]

organizations = [
    # ══════════════ Party Organizations ══════════════
    {
        "id": "pingtan_party_committee",
        "name": "中共平潭县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共福州市委员会",
        "location": "福建省福州市平潭县",
        "notes": "与平潭综合实验区党工委合署办公（区县合一）",
    },
    {
        "id": "pingtan_exp_zone_party",
        "name": "中共福建省委平潭综合实验区工作委员会",
        "type": "党委",
        "level": "副厅级",
        "parent": "中共福建省委员会",
        "location": "福建省福州市平潭县",
        "notes": "省级派出机构，与平潭县委合署办公",
    },

    # ══════════════ Government Organizations ══════════════
    {
        "id": "pingtan_gov",
        "name": "平潭县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "福州市人民政府",
        "location": "福建省福州市平潭县",
    },
    {
        "id": "pingtan_exp_zone_admin",
        "name": "平潭综合实验区管理委员会",
        "type": "政府",
        "level": "副厅级",
        "parent": "福建省人民政府",
        "location": "福建省福州市平潭县",
        "notes": "省级派出机构，与平潭县人民政府合署办公",
    },

    # ══════════════ Discipline Inspection ══════════════
    {
        "id": "pingtan_discipline",
        "name": "平潭县纪律检查委员会 / 平潭县监察委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共平潭县委员会",
        "location": "福建省福州市平潭县",
        "notes": "与实验区纪工委/监察工委合署办公",
    },
    {
        "id": "pingtan_exp_zone_discipline",
        "name": "平潭综合实验区纪工委 / 监察工委",
        "type": "党委",
        "level": "副厅级",
        "parent": "中共福建省委平潭综合实验区工作委员会",
        "location": "福建省福州市平潭县",
    },

    # ══════════════ People's Congress / Political Consultative ══════════════
    {
        "id": "pingtan_npc",
        "name": "平潭县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "平潭县人民代表大会",
        "location": "福建省福州市平潭县",
    },
    {
        "id": "pingtan_cppcc",
        "name": "政协平潭县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协福州市委员会",
        "location": "福建省福州市平潭县",
    },

    # ══════════════ Sub-district / Townships ══════════════
    {
        "id": "pingtan_haitan",
        "name": "平潭县海坛片区管理局",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "平潭县人民政府",
        "location": "福建省福州市平潭县",
    },
    {
        "id": "pingtan_suping",
        "name": "平潭县苏平片区管理局",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "平潭县人民政府",
        "location": "福建省福州市平潭县",
    },
]

positions = [
    # ── 赖军 ──
    {"person_id": "pingtan_lai_jun", "org_id": "pingtan_exp_zone_party", "title": "平潭综合实验区党工委书记", "start": "2021-08", "end": "present", "rank": "正厅级", "note": "省委决定"},
    {"person_id": "pingtan_lai_jun", "org_id": "pingtan_party_committee", "title": "平潭县委书记（兼）", "start": "2021-08", "end": "present", "rank": "正厅级（兼）", "note": "区县合一体制下兼任"},
    {"person_id": "pingtan_lai_jun", "org_id": "", "title": "福建省水利厅党组书记、厅长", "start": "2018-03", "end": "2021-08", "rank": "正厅级", "note": "前一职务"},
    {"person_id": "pingtan_lai_jun", "org_id": "", "title": "福建省民政厅党组书记、厅长", "start": "2016-09", "end": "2018-03", "rank": "正厅级"},
    {"person_id": "pingtan_lai_jun", "org_id": "", "title": "莆田市委副书记", "start": "2015-02", "end": "2016-09", "rank": "副厅级"},
    {"person_id": "pingtan_lai_jun", "org_id": "", "title": "共青团福建省委书记", "start": "2011-09", "end": "2015-02", "rank": "正厅级"},
    {"person_id": "pingtan_lai_jun", "org_id": "", "title": "共青团福建省委副书记", "start": "2003", "end": "2011-09", "rank": "副厅级"},

    # ── 黄建波 ──
    {"person_id": "pingtan_huang_jianbo", "org_id": "pingtan_exp_zone_admin", "title": "平潭综合实验区管委会主任", "start": "2021-08", "end": "present", "rank": "正厅级", "note": "省委决定"},
    {"person_id": "pingtan_huang_jianbo", "org_id": "pingtan_exp_zone_party", "title": "平潭综合实验区党工委副书记", "start": "2021-08", "end": "present", "rank": "副厅级"},
    {"person_id": "pingtan_huang_jianbo", "org_id": "pingtan_gov", "title": "平潭县县长（兼）", "start": "2021-08", "end": "present", "rank": "正处级（兼）", "note": "区县合一体制下兼任"},
    {"person_id": "pingtan_huang_jianbo", "org_id": "", "title": "福建省大数据管理局局长", "start": "2018", "end": "2021-08", "rank": "副厅级"},
    {"person_id": "pingtan_huang_jianbo", "org_id": "", "title": "福建省工信厅副厅长", "start": "2016", "end": "2018", "rank": "副厅级"},
    {"person_id": "pingtan_huang_jianbo", "org_id": "", "title": "三明市台商投资区党工委书记", "start": "2016", "end": "2016", "rank": "副厅级"},
    {"person_id": "pingtan_huang_jianbo", "org_id": "", "title": "三明市三元区委书记", "start": "2011", "end": "2016", "rank": "正处级"},
    {"person_id": "pingtan_huang_jianbo", "org_id": "", "title": "福建省青联副主席", "start": "2005", "end": "2011", "rank": "副厅级"},
    {"person_id": "pingtan_huang_jianbo", "org_id": "", "title": "共青团福建省委常委", "start": "2002", "end": "2011", "rank": "正处级"},

    # ── 文学林 ──
    {"person_id": "pingtan_wen_xuelin", "org_id": "pingtan_exp_zone_party", "title": "平潭综合实验区党工委副书记", "start": "2024-07", "end": "present", "rank": "副厅级"},
    {"person_id": "pingtan_wen_xuelin", "org_id": "pingtan_cppcc", "title": "省政协平潭工委主任（兼）", "start": "2024-07", "end": "present", "rank": "副厅级"},
    {"person_id": "pingtan_wen_xuelin", "org_id": "pingtan_party_committee", "title": "平阳县委副书记（分管党群）", "start": "2024-07", "end": "present", "rank": "正处级（兼）"},

    # ── 黄惠元 ──
    {"person_id": "pingtan_huang_huiyuan", "org_id": "pingtan_exp_zone_discipline", "title": "平潭综合实验区纪工委书记、监察工委主任", "start": "unknown", "end": "present", "rank": "副厅级"},
    {"person_id": "pingtan_huang_huiyuan", "org_id": "pingtan_discipline", "title": "平潭县纪委书记、监委主任（兼）", "start": "unknown", "end": "present", "rank": "正处级（兼）"},

    # ── 何杰民 ──
    {"person_id": "pingtan_he_jiemin", "org_id": "pingtan_exp_zone_admin", "title": "平潭综合实验区管委会副主任", "start": "2022-09", "end": "present", "rank": "副厅级"},
    {"person_id": "pingtan_he_jiemin", "org_id": "pingtan_gov", "title": "平潭县副县长（兼）", "start": "2022-09", "end": "present", "rank": "副处级（兼）"},
    {"person_id": "pingtan_he_jiemin", "org_id": "", "title": "福州新区管委会副主任、长乐区委书记", "start": "2020", "end": "2022-09", "rank": "副厅级"},
    {"person_id": "pingtan_he_jiemin", "org_id": "", "title": "罗源县委书记", "start": "2014", "end": "2020", "rank": "正处级"},
    {"person_id": "pingtan_he_jiemin", "org_id": "", "title": "福州市仓山区区长", "start": "2012", "end": "2014", "rank": "正处级"},
    {"person_id": "pingtan_he_jiemin", "org_id": "", "title": "长乐市委副书记", "start": "2009", "end": "2012", "rank": "副处级"},

    # ── 陈训明 ──
    {"person_id": "pingtan_chen_xunming", "org_id": "pingtan_exp_zone_party", "title": "平潭综合实验区党工委委员", "start": "2023-03", "end": "present", "rank": "副厅级"},
    {"person_id": "pingtan_chen_xunming", "org_id": "pingtan_exp_zone_admin", "title": "平潭综合实验区管委会副主任", "start": "2021-05", "end": "present", "rank": "副厅级"},
    {"person_id": "pingtan_chen_xunming", "org_id": "pingtan_gov", "title": "平潭县副县长（兼）", "start": "2021-05", "end": "present", "rank": "副处级（兼）"},
    {"person_id": "pingtan_chen_xunming", "org_id": "", "title": "共青团福建省委副书记", "start": "2015", "end": "2021-05", "rank": "副厅级"},

    # ── 方良栋 ──
    {"person_id": "pingtan_fang_liangdong", "org_id": "pingtan_exp_zone_party", "title": "平潭综合实验区党工委委员", "start": "2025-05", "end": "present", "rank": "副厅级"},
    {"person_id": "pingtan_fang_liangdong", "org_id": "pingtan_exp_zone_admin", "title": "平潭综合实验区管委会副主任", "start": "2022-07", "end": "present", "rank": "副厅级"},
    {"person_id": "pingtan_fang_liangdong", "org_id": "pingtan_gov", "title": "平潭县副县长（兼）", "start": "2016", "end": "2022-07", "rank": "副处级"},
    {"person_id": "pingtan_fang_liangdong", "org_id": "pingtan_haitan", "title": "海坛片区管理局党委书记、局长", "start": "2019", "end": "2022-07", "rank": "正处级"},

    # ── 潘新雅 ──
    {"person_id": "pingtan_pan_xinya", "org_id": "pingtan_exp_zone_party", "title": "平潭综合实验区党工委委员", "start": "2023-03", "end": "present", "rank": "副厅级"},

    # ── 孙树群 ──
    {"person_id": "pingtan_sun_shuqun", "org_id": "pingtan_exp_zone_admin", "title": "平潭综合实验区管委会副主任", "start": "2025-03", "end": "present", "rank": "副厅级", "note": "试用期一年"},
    {"person_id": "pingtan_sun_shuqun", "org_id": "pingtan_gov", "title": "平潭县副县长（兼）", "start": "2025-03", "end": "present", "rank": "副处级（兼）"},
    {"person_id": "pingtan_sun_shuqun", "org_id": "pingtan_suping", "title": "苏平片区管理局党委书记、局长", "start": "2021", "end": "2025-03", "rank": "正处级"},

    # ── 陈善光 ──
    {"person_id": "pingtan_chen_shanguang", "org_id": "pingtan_exp_zone_party", "title": "平潭综合实验区党工委书记", "start": "2018-07", "end": "2021-08", "rank": "正厅级"},
    {"person_id": "pingtan_chen_shanguang", "org_id": "pingtan_party_committee", "title": "平潭县委书记（兼）", "start": "2018-07", "end": "2021-08", "rank": "正厅级（兼）"},

    # ── 张兆民 ──
    {"person_id": "pingtan_zhang_zhaomin", "org_id": "pingtan_exp_zone_party", "title": "平潭综合实验区党工委书记", "start": "2015-12", "end": "2018-07", "rank": "正厅级"},
    {"person_id": "pingtan_zhang_zhaomin", "org_id": "pingtan_party_committee", "title": "平潭县委书记（兼）", "start": "2016-06", "end": "2018-07", "rank": "正厅级（兼）"},

    # ── 龚清概 ──
    {"person_id": "pingtan_gong_qinggai", "org_id": "", "title": "平潭综合实验区党工委书记、管委会主任", "start": "2009-07", "end": "2013", "rank": "正厅级"},

    # ── 林文耀 ──
    {"person_id": "pingtan_lin_wenyao", "org_id": "pingtan_exp_zone_admin", "title": "平潭综合实验区管委会主任", "start": "2017", "end": "2021", "rank": "正厅级"},
    {"person_id": "pingtan_lin_wenyao", "org_id": "pingtan_gov", "title": "平潭县县长（兼）", "start": "2017", "end": "2021", "rank": "正处级（兼）"},
]

relationships = [
    # ── 赖军 ↔ 黄建波: 区县合一搭档 ──
    {"person_a": "pingtan_lai_jun", "person_b": "pingtan_huang_jianbo", "type": "overlap", "context": "平潭综合实验区党政一把手搭档（书记+主任/县长）", "overlap_org": "平潭综合实验区党工委/管委会/平潭县委县政府", "overlap_period": "2021-08至今", "strength": "strong", "confidence": "confirmed"},

    # ── 赖军 ↔ 陈善光: 前后任书记 ──
    {"person_a": "pingtan_lai_jun", "person_b": "pingtan_chen_shanguang", "type": "predecessor_successor", "context": "平潭综合实验区党工委书记前后任", "overlap_org": "平潭综合实验区党工委", "overlap_period": "交接2021年8月", "strength": "medium", "confidence": "confirmed"},

    # ── 陈善光 ↔ 张兆民: 前后任书记 ──
    {"person_a": "pingtan_chen_shanguang", "person_b": "pingtan_zhang_zhaomin", "type": "predecessor_successor", "context": "平潭综合实验区党工委书记前后任", "overlap_org": "平潭综合实验区党工委", "overlap_period": "交接2018年7月", "strength": "medium", "confidence": "confirmed"},

    # ── 张兆民 ↔ 龚清概: 前后任书记 ──
    {"person_a": "pingtan_zhang_zhaomin", "person_b": "pingtan_gong_qinggai", "type": "predecessor_successor", "context": "平潭综合实验区党工委书记前后任", "overlap_org": "平潭综合实验区党工委", "overlap_period": "交接2015年12月", "strength": "medium", "confidence": "confirmed"},

    # ── 黄建波 ↔ 林文耀: 前后任主任 ──
    {"person_a": "pingtan_huang_jianbo", "person_b": "pingtan_lin_wenyao", "type": "predecessor_successor", "context": "平潭综合实验区管委会主任前后任", "overlap_org": "平潭综合实验区管委会", "overlap_period": "交接2021年8月", "strength": "medium", "confidence": "plausible"},

    # ── 赖军 ↔ 文学林: 上下级（书记+副书记）─
    {"person_a": "pingtan_lai_jun", "person_b": "pingtan_wen_xuelin", "type": "superior_subordinate", "context": "平潭综合实验区党工委书记与副书记", "overlap_org": "平潭综合实验区党工委", "overlap_period": "2024年7月至今", "strength": "strong", "confidence": "confirmed"},

    # ── 黄建波 ↔ 文学林: 上下级 ──
    {"person_a": "pingtan_huang_jianbo", "person_b": "pingtan_wen_xuelin", "type": "overlap", "context": "平潭综合实验区党工委副书记与管委会主任", "overlap_org": "平潭综合实验区党工委/管委会", "overlap_period": "2024年7月至今", "strength": "strong", "confidence": "confirmed"},

    # ── 赖军 ↔ 黄惠元: 上下级（书记+纪委书记）─
    {"person_a": "pingtan_lai_jun", "person_b": "pingtan_huang_huiyuan", "type": "superior_subordinate", "context": "平潭综合实验区党工委书记与纪工委书记", "overlap_org": "平潭综合实验区党工委", "overlap_period": "2021年8月至今", "strength": "strong", "confidence": "confirmed"},

    # ── 何杰民 ↔ 陈训明: 同为管委会副主任（同级同事）─
    {"person_a": "pingtan_he_jiemin", "person_b": "pingtan_chen_xunming", "type": "overlap", "context": "平潭综合实验区管委会副主任同事", "overlap_org": "平潭综合实验区管委会", "overlap_period": "2022年9月至今", "strength": "strong", "confidence": "confirmed"},

    # ── 何杰民 ↔ 方良栋: 同为管委会副主任 ──
    {"person_a": "pingtan_he_jiemin", "person_b": "pingtan_fang_liangdong", "type": "overlap", "context": "平潭综合实验区管委会副主任同事", "overlap_org": "平潭综合实验区管委会", "overlap_period": "2022年9月至今", "strength": "strong", "confidence": "confirmed"},

    # ── 陈训明 ↔ 方良栋: 同为管委会副主任 ──
    {"person_a": "pingtan_chen_xunming", "person_b": "pingtan_fang_liangdong", "type": "overlap", "context": "平潭综合实验区管委会副主任同事", "overlap_org": "平潭综合实验区管委会", "overlap_period": "2022年7月至今", "strength": "strong", "confidence": "confirmed"},

    # ── 何杰民 ↔ 黄建波: 上下级 ──
    {"person_a": "pingtan_he_jiemin", "person_b": "pingtan_huang_jianbo", "type": "superior_subordinate", "context": "平潭综合实验区管委会主任与副主任", "overlap_org": "平潭综合实验区管委会", "overlap_period": "2022年9月至今", "strength": "strong", "confidence": "confirmed"},

    # ── 方良栋 ↔ 黄建波: 上下级 ──
    {"person_a": "pingtan_fang_liangdong", "person_b": "pingtan_huang_jianbo", "type": "superior_subordinate", "context": "平潭综合实验区管委会主任与副主任", "overlap_org": "平潭综合实验区管委会", "overlap_period": "2022年7月至今", "strength": "strong", "confidence": "confirmed"},

    # ── 陈训明 ↔ 黄建波: 上下级 ──
    {"person_a": "pingtan_chen_xunming", "person_b": "pingtan_huang_jianbo", "type": "superior_subordinate", "context": "平潭综合实验区管委会主任与副主任", "overlap_org": "平潭综合实验区管委会", "overlap_period": "2021年5月至今", "strength": "strong", "confidence": "confirmed"},

    # ── 文学林 ↔ 吴礼源: 前后任副书记 ──
    {"person_a": "pingtan_wen_xuelin", "person_b": "pingtan_wu_liyuan", "type": "predecessor_successor", "context": "平潭综合实验区党工委副书记前后任", "overlap_org": "平潭综合实验区党工委", "overlap_period": "交接2024年7月", "strength": "medium", "confidence": "plausible"},

    # ── 何杰民 ↔ 赖军: 上下级（书记+委员）─
    {"person_a": "pingtan_he_jiemin", "person_b": "pingtan_lai_jun", "type": "superior_subordinate", "context": "平潭综合实验区党工委书记与委员", "overlap_org": "平潭综合实验区党工委", "overlap_period": "2022年9月至今", "strength": "strong", "confidence": "confirmed"},

    # ── 陈训明 ↔ 赖军: 上下级（书记+委员）─
    {"person_a": "pingtan_chen_xunming", "person_b": "pingtan_lai_jun", "type": "superior_subordinate", "context": "平潭综合实验区党工委书记与委员", "overlap_org": "平潭综合实验区党工委", "overlap_period": "2023年3月至今", "strength": "strong", "confidence": "confirmed"},

    # ── 潘新雅 ↔ 赖军: 上下级（书记+委员）─
    {"person_a": "pingtan_pan_xinya", "person_b": "pingtan_lai_jun", "type": "superior_subordinate", "context": "平潭综合实验区党工委书记与委员", "overlap_org": "平潭综合实验区党工委", "overlap_period": "2023年3月至今", "strength": "strong", "confidence": "confirmed"},

    # ── 方良栋 ↔ 赖军: 上下级（书记+委员）─
    {"person_a": "pingtan_fang_liangdong", "person_b": "pingtan_lai_jun", "type": "superior_subordinate", "context": "平潭综合实验区党工委书记与委员", "overlap_org": "平潭综合实验区党工委", "overlap_period": "2025年5月至今", "strength": "strong", "confidence": "confirmed"},

    # ── 孙树群 ↔ 黄建波: 上下级 ──
    {"person_a": "pingtan_sun_shuqun", "person_b": "pingtan_huang_jianbo", "type": "superior_subordinate", "context": "平潭综合实验区管委会主任与副主任", "overlap_org": "平潭综合实验区管委会", "overlap_period": "2025年3月至今", "strength": "strong", "confidence": "confirmed"},
]


# ── build SQLite database ─────────────────────────────────────────────

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
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
    )""")

    c.execute("""CREATE TABLE organizations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT,
        notes TEXT
    )""")

    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT,
        org_id TEXT,
        title TEXT,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")

    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT,
        person_b TEXT,
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT,
        strength TEXT,
        confidence TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["native_place"], p["education"],
                   p["party_join"], p["work_start"], p["current_post"],
                   p["current_org"], p["source"], p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"],
                   o["location"], o.get("notes", "")))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)""",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos.get("note", "")))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence) VALUES (?,?,?,?,?,?,?,?)""",
                  (r["person_a"], r["person_b"], r["type"], r["context"],
                   r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    size = os.path.getsize(DB_PATH)
    print(f"✅ SQLite DB created: {DB_PATH} ({size} bytes)")


# ── build GEXF graph ──────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    if "书记" in p["current_post"] and "纪委" not in p["current_post"]:
        return "255,50,50"  # Red for party secretary
    elif "县长" in p["current_post"] or "主任" in p["current_post"]:
        return "50,100,255"  # Blue for government head
    elif "纪委" in p["current_post"]:
        return "255,165,0"  # Orange for discipline
    elif "副书记" in p["current_post"]:
        return "255,50,50"  # Red for deputy secretary (party)
    else:
        return "100,100,100"  # Grey for others

def person_size(p):
    top_keywords = ["书记", "县长", "主任"]
    if p["id"] in ["pingtan_lai_jun", "pingtan_huang_jianbo"]:
        return "20.0"
    return "12.0"

def org_color(o):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "乡镇/街道": "255,255,200",
    }
    return colors.get(o["type"], "200,200,200")

def org_size(o):
    return "8.0"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode china-gov-network Research Agent</creator>')
    lines.append('    <description>平潭县（福建省福州市）领导班子工作关系网络 — 区县合一体制</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="location" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes: Persons ──
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        role = p["current_post"]
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # ── Nodes: Organizations ──
    for o in organizations:
        c = org_color(o)
        sz = org_size(o)
        lines.append(f'      <node id="{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("location",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── Edges: person→organization (worked_at) ──
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        if not pos["org_id"]:
            continue
        eid += 1
        title = pos["title"]
        rank = pos.get("rank", "")
        lines.append(f'      <edge id="e{eid}" source="{pos["person_id"]}" target="{pos["org_id"]}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["start"])} - {esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # ── Edges: person↔person (relationship) ──
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["context"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{r["confidence"]}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    size = os.path.getsize(GEXF_PATH)
    print(f"✅ GEXF graph created: {GEXF_PATH} ({size} bytes)")


# ── main ───────────────────────────────────────────────────────────────

def main():
    print(f"=== Building 平潭县 Network Data ===")
    print(f"Date: {TODAY}")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print()
    build_db()
    build_gexf()
    print()
    print("=== Done ===")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    main()
