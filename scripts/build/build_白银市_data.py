#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 白银市 (Baiyin City, Gansu Province).

Task: gansu_白银市 — 市委书记 & 市长
Province: 甘肃省
Parent city: (none, prefecture-level)
Region: 白银市
Level: 地级市
Research date: 2026-07-17

Confirmed officeholders (as of 2026-07-17, from www.baiyin.gov.cn 领导之窗):
- 市委书记: 刘凯 (born 1983.07, male, Han, PhD, from Henan)
- 市长: 张延保 (born 1966.09, male, Tibetan, master's degree)
- 市委副书记/宣传部部长: 朱利民 (born 1971.02, female, Han)
- 常务副市长: 葛永宏 (born 1975.09, male, Han)
- 市纪委书记/监委主任: 董兆生 (born 1976.08, male, Han)

市委常委会 (11 members confirmed):
刘凯, 张延保, 朱利民, 葛永宏, 董兆生, 王彬, 乔振华, 丁肃静, 胡建伟, 潘新

Key Note: 刘凯 took office as 市委书记 in Jan 2026, succeeding 杨建武.
刘凯 is the youngest prefectural-level party secretary in China (born 1983).
Previously served as Mayor of 嘉峪关市 (2021-2026).

张延保 is a Tibetan cadre with long service in Gansu. Career details limited on gov site.

Sources:
- www.baiyin.gov.cn/ldzc/ (official leadership page, accessed 2026-07-17)
- zh.wikipedia.org/wiki/刘凯_(1983年) (verified career timeline)
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
    GOV_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STAGING = os.path.join(GOV_ROOT, "data", "tmp", "gansu_白银市")
DB_PATH = os.path.join(STAGING, "白银市_network.db")
GEXF_PATH = os.path.join(STAGING, "白银市_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 市委书记 — 刘凯 (born 1983, youngest prefectural party secretary in China)
    {
        "id": "baiyin_liu_kai",
        "name": "刘凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年7月",
        "birthplace": "河南省焦作市",
        "native_place": "河南省濮阳市",
        "education": "研究生（哲学博士，北京大学）",
        "party_join": "2002年6月",
        "work_start": "2010年7月",
        "current_post": "白银市委书记",
        "current_org": "中共白银市委员会",
        "source": "www.baiyin.gov.cn (领导之窗); zh.wikipedia.org/wiki/刘凯_(1983年)",
        "notes": "1983年7月生，河南焦作人（祖籍濮阳）。2002年保送北京大学哲学系，2006年学士，2010年博士。曾任北京大学学生会主席、全国学联主席、全国青联副主席。2010年留校任北大团委副书记，后任北京朝阳区团委书记。2011年赴甘肃，历任灵台县长、灵台县委书记、平凉市委常委、嘉峪关市长。2026年1月任白银市委书记，为全国最年轻地级市市委书记。",
        "confidence": "confirmed",
    },

    # 市长 — 张延保
    {
        "id": "baiyin_zhang_yanbao",
        "name": "张延保",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1966年9月",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生（法学硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市委副书记、市长",
        "current_org": "白银市人民政府",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1966年9月出生，藏族，在职研究生学历，法学硕士，中共党员。现任白银市委副书记、市政府市长、党组书记。领导市政府全面工作。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 市委副书记、宣传部部长 — 朱利民
    {
        "id": "baiyin_zhu_limin",
        "name": "朱利民",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年2月",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学（历史学学士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市委副书记、宣传部部长",
        "current_org": "中共白银市委员会宣传部",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1971年2月出生，汉族，在职大学学历，历史学学士，中共党员。现任白银市委副书记、宣传部部长，市新时代文明实践中心办公室主任，市委教育工作委员会书记（兼）。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 常务副市长 — 葛永宏
    {
        "id": "baiyin_ge_yonghong",
        "name": "葛永宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学（公共管理硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市委常委、常务副市长",
        "current_org": "白银市人民政府",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1975年9月出生，在职大学学历，公共管理硕士，中共党员。现任白银市委常委，市政府（常务）副市长、党组副书记。负责市政府常务工作，分管发改、财政、国资、税务、金融、自然资源、应急、统计等。",
        "confidence": "confirmed",
    },

    # 市纪委书记/监委主任 — 董兆生
    {
        "id": "baiyin_dong_zhaosheng",
        "name": "董兆生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年8月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市委常委、市纪委书记、市监委主任",
        "current_org": "中共白银市纪律检查委员会",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1976年8月出生，大学学历，中共党员。现任白银市委常委、市纪委书记、市监委主任、二级高级监察官。完整履历待补充。",
        "confidence": "confirmed",
    },

    # ══════════════ Other Party Standing Committee ══════════════

    # 王彬 — 市委常委、白银有色集团党委书记、董事长
    {
        "id": "baiyin_wang_bin",
        "name": "王彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年6月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市委常委、白银有色集团股份有限公司党委书记、董事长",
        "current_org": "白银有色集团股份有限公司",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1974年6月出生，省委党校研究生学历，思想政治工作研究员，中共党员。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 乔振华 — 市委常委、政法委书记
    {
        "id": "baiyin_qiao_zhenhua",
        "name": "乔振华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年7月",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学（法学学士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市委常委、政法委书记",
        "current_org": "中共白银市委员会政法委员会",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1973年7月出生，在职大学学历，法学学士，中共党员。现任白银市委常委、政法委书记，市委全面依法治市委员会办公室主任（兼）。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 丁肃静 — 市委常委、组织部部长
    {
        "id": "baiyin_ding_sujing",
        "name": "丁肃静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "",
        "native_place": "",
        "education": "大学（法学学士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市委常委、组织部部长",
        "current_org": "中共白银市委员会组织部",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1978年1月出生，大学学历，法学学士，中共党员。现任白银市委常委、组织部部长，市委党校（市行政学院、甘肃会宁干部学院）校长（院长）（兼）。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 胡建伟 — 市委常委、秘书长
    {
        "id": "baiyin_hu_jianwei",
        "name": "胡建伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年3月",
        "birthplace": "",
        "native_place": "",
        "education": "大学（公共管理硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市委常委、秘书长",
        "current_org": "中共白银市委员会",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1969年3月出生，大学学历，公共管理硕士，中共党员。现任白银市委常委、秘书长，市委改革办主任（兼），市委直属机关工委书记（兼），市委国安办主任（兼）。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 潘新 — 市委常委、统战部部长、副市长
    {
        "id": "baiyin_pan_xin",
        "name": "潘新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年4月",
        "birthplace": "",
        "native_place": "",
        "education": "大学（农业推广硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市委常委、统战部部长，市政府党组成员",
        "current_org": "中共白银市委员会统战部",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1981年4月出生，大学学历，农业推广硕士，中共党员。现任白银市委常委、统战部部长，市政府党组成员，市政协党组副书记（兼）。分工负责民政、水利、农业农村、乡村振兴、气象、供销等。完整履历待补充。",
        "confidence": "confirmed",
    },

    # ══════════════ Deputy Mayors ══════════════

    # 刘湖泉 — 副市长
    {
        "id": "baiyin_liu_huquan",
        "name": "刘湖泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年10月",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生（工商管理硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市副市长",
        "current_org": "白银市人民政府",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1980年10月生，在职研究生学历，工商管理硕士。现任白银市政府副市长、党组成员，白银高新区党工委第一书记（兼）。负责兰白自创区、科技、工信、生态环境、商务等工作。",
        "confidence": "confirmed",
    },

    # 丁富强 — 副市长（民盟）
    {
        "id": "baiyin_ding_fuqiang",
        "name": "丁富强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学",
        "party_join": "民盟盟员",
        "work_start": "",
        "current_post": "白银市副市长",
        "current_org": "白银市人民政府",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1974年10月生，在职大学，民盟盟员。负责社保、住建、交通、残疾人等工作。",
        "confidence": "confirmed",
    },

    # 亓述伟 — 副市长（民革）
    {
        "id": "baiyin_qi_shuwei",
        "name": "亓述伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生（法学硕士）",
        "party_join": "民革党员",
        "work_start": "",
        "current_post": "白银市副市长",
        "current_org": "白银市人民政府",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1976年3月生，研究生学历，法学硕士，民革党员。负责司法、地震等工作。",
        "confidence": "confirmed",
    },

    # 王娟 — 副市长
    {
        "id": "baiyin_wang_juan",
        "name": "王娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年12月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生（文学硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市副市长",
        "current_org": "白银市人民政府",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1980年12月出生，研究生学历，文学硕士，中共党员。负责教育、文广旅、卫生健康、医保、市场监管、体育等工作。",
        "confidence": "confirmed",
    },

    # 许伟民 — 副市长兼会宁县委书记
    {
        "id": "baiyin_xu_weimin",
        "name": "许伟民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年6月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生（工程硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市副市长、会宁县委书记",
        "current_org": "中共会宁县委员会",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1984年6月出生，研究生学历，工程硕士，中共党员。现任白银市政府副市长、党组成员，会宁县委书记。负责会宁县委全面工作。",
        "confidence": "confirmed",
    },

    # 康岸桥 — 副市长人选、公安局局长
    {
        "id": "baiyin_kang_anqiao",
        "name": "康岸桥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年7月",
        "birthplace": "",
        "native_place": "",
        "education": "大学（理学学士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市副市长人选、市公安局局长",
        "current_org": "白银市人民政府",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1971年7月生，大学学历，理学学士，中共党员。现任白银市政府党组成员、副市长人选，市公安局党委书记、局长、督察长（兼）人选，市委政法委副书记（兼）。负责民族宗教、公安、退役军人事务、信访等工作。",
        "confidence": "confirmed",
    },

    # ══════════════ Municipal Government Secretary ══════════════

    # 忽建强 — 市政府秘书长
    {
        "id": "baiyin_hu_jianqiang",
        "name": "忽建强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "",
        "native_place": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市政府秘书长",
        "current_org": "白银市人民政府",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1975年10月出生，中央党校研究生学历，中共党员。现任市政府党组成员、秘书长，市政府办公室党组书记。协助市长处理市政府日常工作。",
        "confidence": "confirmed",
    },

    # ══════════════ NPC (人大) ══════════════

    # 惠强 — 人大主任
    {
        "id": "baiyin_hui_qiang",
        "name": "惠强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年4月",
        "birthplace": "",
        "native_place": "",
        "education": "大学（法学硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市人大常委会主任",
        "current_org": "白银市人大常委会",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1970年4月出生，大学学历，法学硕士，中共党员。现任白银市人大常委会主任、党组书记。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 郝平英 — 人大副主任
    {
        "id": "baiyin_hao_pingying",
        "name": "郝平英",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "白银市人大常委会副主任",
        "current_org": "白银市人大常委会",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 任文贵 — 人大副主任
    {
        "id": "baiyin_ren_wengui",
        "name": "任文贵",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "白银市人大常委会副主任",
        "current_org": "白银市人大常委会",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 马世斌 — 人大副主任
    {
        "id": "baiyin_ma_shibin",
        "name": "马世斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "白银市人大常委会副主任",
        "current_org": "白银市人大常委会",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 何艳君 — 人大副主任
    {
        "id": "baiyin_he_yanjun",
        "name": "何艳君",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "白银市人大常委会副主任",
        "current_org": "白银市人大常委会",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 任辉 — 人大秘书长
    {
        "id": "baiyin_ren_hui",
        "name": "任辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "白银市人大常委会秘书长",
        "current_org": "白银市人大常委会",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # ══════════════ CPPCC (政协) ══════════════

    # 杜健棠 — 政协主席
    {
        "id": "baiyin_du_jiantang",
        "name": "杜健棠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年11月",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生（工商管理硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白银市政协主席",
        "current_org": "白银市政协",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "1970年11月出生，在职研究生学历，工商管理硕士，中共党员。现任白银市政协主席、党组书记。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 潘新 — 政协党组副书记（兼）
    # (Duplicate role — already listed as person)

    # 杨永强 — 政协党组副书记、副主席
    {
        "id": "baiyin_yang_yongqiang",
        "name": "杨永强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "白银市政协党组副书记、副主席",
        "current_org": "白银市政协",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 杨志平 — 政协副主席
    {
        "id": "baiyin_yang_zhiping",
        "name": "杨志平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "白银市政协副主席",
        "current_org": "白银市政协",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 傅学兴 — 政协副主席
    {
        "id": "baiyin_fu_xuexing",
        "name": "傅学兴",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "白银市政协副主席",
        "current_org": "白银市政协",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 杨永胜 — 政协副主席
    {
        "id": "baiyin_yang_yongsheng",
        "name": "杨永胜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "白银市政协副主席",
        "current_org": "白银市政协",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 李呈萍 — 政协副主席
    {
        "id": "baiyin_li_chengping",
        "name": "李呈萍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "白银市政协副主席",
        "current_org": "白银市政协",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 史文娟 — 政协副主席
    {
        "id": "baiyin_shi_wenjuan",
        "name": "史文娟",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "白银市政协副主席",
        "current_org": "白银市政协",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 魏列海 — 政协秘书长
    {
        "id": "baiyin_wei_liehai",
        "name": "魏列海",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "白银市政协秘书长",
        "current_org": "白银市政协",
        "source": "www.baiyin.gov.cn (领导之窗)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },
]

organizations = [
    # Party committee
    {"id": "cpc_baiyin", "name": "中共白银市委员会", "type": "党委", "level": "地级市", "parent": "中共甘肃省委员会", "location": "甘肃省白银市"},
    # Government
    {"id": "gov_baiyin", "name": "白银市人民政府", "type": "政府", "level": "地级市", "parent": "甘肃省人民政府", "location": "甘肃省白银市"},
    # Discipline inspection
    {"id": "dis_baiyin", "name": "中共白银市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共白银市委员会", "location": "甘肃省白银市"},
    # Organization
    {"id": "org_baiyin", "name": "中共白银市委员会组织部", "type": "党委", "level": "地级市", "parent": "中共白银市委员会", "location": "甘肃省白银市"},
    # Propaganda
    {"id": "prop_baiyin", "name": "中共白银市委员会宣传部", "type": "党委", "level": "地级市", "parent": "中共白银市委员会", "location": "甘肃省白银市"},
    # United front
    {"id": "united_baiyin", "name": "中共白银市委员会统战部", "type": "党委", "level": "地级市", "parent": "中共白银市委员会", "location": "甘肃省白银市"},
    # Political-legal
    {"id": "polit_baiyin", "name": "中共白银市委员会政法委员会", "type": "党委", "level": "地级市", "parent": "中共白银市委员会", "location": "甘肃省白银市"},
    # SOE
    {"id": "soe_baiyin_nonferrous", "name": "白银有色集团股份有限公司", "type": "政府", "level": "地级市", "parent": "", "location": "甘肃省白银市"},
    # NPC
    {"id": "npc_baiyin", "name": "白银市人大常委会", "type": "人大", "level": "地级市", "parent": "", "location": "甘肃省白银市"},
    # CPPCC
    {"id": "cppcc_baiyin", "name": "白银市政协", "type": "政协", "level": "地级市", "parent": "", "location": "甘肃省白银市"},
    # Public security bureau
    {"id": "psb_baiyin", "name": "白银市公安局", "type": "政府", "level": "地级市", "parent": "白银市人民政府", "location": "甘肃省白银市"},
    # Party school
    {"id": "party_school_baiyin", "name": "中共白银市委党校（市行政学院、甘肃会宁干部学院）", "type": "事业单位", "level": "地级市", "parent": "中共白银市委员会", "location": "甘肃省白银市"},
    # Hi-tech zone
    {"id": "hitech_baiyin", "name": "白银高新技术产业开发区", "type": "开发区", "level": "地级市", "parent": "白银市人民政府", "location": "甘肃省白银市"},
    # Huining county committee
    {"id": "cpc_huining", "name": "中共会宁县委员会", "type": "党委", "level": "县", "parent": "中共白银市委员会", "location": "甘肃省白银市会宁县"},
]

positions = [
    # 刘凯
    {"person_id": "baiyin_liu_kai", "org_id": "cpc_baiyin", "title": "白银市委书记", "start": "2026年1月", "end": "present", "rank": "正厅级", "note": "全国最年轻地级市市委书记"},

    # 张延保
    {"person_id": "baiyin_zhang_yanbao", "org_id": "gov_baiyin", "title": "白银市市长", "start": "", "end": "present", "rank": "正厅级", "note": "市政府党组书记"},
    {"person_id": "baiyin_zhang_yanbao", "org_id": "cpc_baiyin", "title": "白银市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},

    # 朱利民
    {"person_id": "baiyin_zhu_limin", "org_id": "cpc_baiyin", "title": "白银市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_zhu_limin", "org_id": "prop_baiyin", "title": "白银市委宣传部部长", "start": "", "end": "present", "rank": "副厅级", "note": "兼任"},

    # 葛永宏
    {"person_id": "baiyin_ge_yonghong", "org_id": "cpc_baiyin", "title": "白银市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_ge_yonghong", "org_id": "gov_baiyin", "title": "白银市常务副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市政府党组副书记"},

    # 董兆生
    {"person_id": "baiyin_dong_zhaosheng", "org_id": "cpc_baiyin", "title": "白银市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_dong_zhaosheng", "org_id": "dis_baiyin", "title": "白银市纪委书记、市监委主任", "start": "", "end": "present", "rank": "副厅级", "note": "二级高级监察官"},

    # 王彬
    {"person_id": "baiyin_wang_bin", "org_id": "cpc_baiyin", "title": "白银市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_wang_bin", "org_id": "soe_baiyin_nonferrous", "title": "白银有色集团党委书记、董事长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # 乔振华
    {"person_id": "baiyin_qiao_zhenhua", "org_id": "cpc_baiyin", "title": "白银市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_qiao_zhenhua", "org_id": "polit_baiyin", "title": "白银市委政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # 丁肃静
    {"person_id": "baiyin_ding_sujing", "org_id": "cpc_baiyin", "title": "白银市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_ding_sujing", "org_id": "org_baiyin", "title": "白银市委组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_ding_sujing", "org_id": "party_school_baiyin", "title": "市委党校校长（兼）", "start": "", "end": "present", "rank": "副厅级", "note": "兼任"},

    # 胡建伟
    {"person_id": "baiyin_hu_jianwei", "org_id": "cpc_baiyin", "title": "白银市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_hu_jianwei", "org_id": "cpc_baiyin", "title": "白银市委秘书长", "start": "", "end": "present", "rank": "副厅级", "note": "兼任"},

    # 潘新
    {"person_id": "baiyin_pan_xin", "org_id": "cpc_baiyin", "title": "白银市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_pan_xin", "org_id": "united_baiyin", "title": "白银市委统战部部长", "start": "", "end": "present", "rank": "副厅级", "note": "兼任"},
    {"person_id": "baiyin_pan_xin", "org_id": "gov_baiyin", "title": "白银市副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市政府党组成员"},
    {"person_id": "baiyin_pan_xin", "org_id": "cppcc_baiyin", "title": "市政协党组副书记（兼）", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # 刘湖泉
    {"person_id": "baiyin_liu_huquan", "org_id": "gov_baiyin", "title": "白银市副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市政府党组成员"},
    {"person_id": "baiyin_liu_huquan", "org_id": "hitech_baiyin", "title": "白银高新区党工委第一书记（兼）", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # 丁富强
    {"person_id": "baiyin_ding_fuqiang", "org_id": "gov_baiyin", "title": "白银市副市长", "start": "", "end": "present", "rank": "副厅级", "note": "民盟盟员"},

    # 亓述伟
    {"person_id": "baiyin_qi_shuwei", "org_id": "gov_baiyin", "title": "白银市副市长", "start": "", "end": "present", "rank": "副厅级", "note": "民革党员"},

    # 王娟
    {"person_id": "baiyin_wang_juan", "org_id": "gov_baiyin", "title": "白银市副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市政府党组成员"},

    # 许伟民
    {"person_id": "baiyin_xu_weimin", "org_id": "gov_baiyin", "title": "白银市副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市政府党组成员"},
    {"person_id": "baiyin_xu_weimin", "org_id": "cpc_huining", "title": "会宁县委书记", "start": "", "end": "present", "rank": "正处级", "note": "兼任"},

    # 康岸桥
    {"person_id": "baiyin_kang_anqiao", "org_id": "gov_baiyin", "title": "白银市副市长人选", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_kang_anqiao", "org_id": "psb_baiyin", "title": "白银市公安局局长", "start": "", "end": "present", "rank": "副厅级", "note": "兼督察长"},

    # 忽建强
    {"person_id": "baiyin_hu_jianqiang", "org_id": "gov_baiyin", "title": "白银市政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": "市政府党组成员"},

    # NPC
    {"person_id": "baiyin_hui_qiang", "org_id": "npc_baiyin", "title": "白银市人大常委会主任", "start": "", "end": "present", "rank": "正厅级", "note": "党组书记"},
    {"person_id": "baiyin_hao_pingying", "org_id": "npc_baiyin", "title": "白银市人大常委会副主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_ren_wengui", "org_id": "npc_baiyin", "title": "白银市人大常委会副主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_ma_shibin", "org_id": "npc_baiyin", "title": "白银市人大常委会副主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_he_yanjun", "org_id": "npc_baiyin", "title": "白银市人大常委会副主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_ren_hui", "org_id": "npc_baiyin", "title": "白银市人大常委会秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # CPPCC
    {"person_id": "baiyin_du_jiantang", "org_id": "cppcc_baiyin", "title": "白银市政协主席", "start": "", "end": "present", "rank": "正厅级", "note": "党组书记"},
    {"person_id": "baiyin_yang_yongqiang", "org_id": "cppcc_baiyin", "title": "白银市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": "党组副书记"},
    {"person_id": "baiyin_yang_zhiping", "org_id": "cppcc_baiyin", "title": "白银市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_fu_xuexing", "org_id": "cppcc_baiyin", "title": "白银市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_yang_yongsheng", "org_id": "cppcc_baiyin", "title": "白银市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_li_chengping", "org_id": "cppcc_baiyin", "title": "白银市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_shi_wenjuan", "org_id": "cppcc_baiyin", "title": "白银市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "baiyin_wei_liehai", "org_id": "cppcc_baiyin", "title": "白银市政协秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

# ── Relationship edges ──────────────────────────────────────────────────
relationships = [
    # 刘凯 ↔ 张延保 (党委书记↔市长, 党政一把手搭档)
    {"person_a": "baiyin_liu_kai", "person_b": "baiyin_zhang_yanbao",
     "type": "superior_subordinate", "strength": "strong",
     "context": "党政一把手搭档，刘凯主持市委全面工作，张延保主持市政府全面工作",
     "overlap_org": "中共白银市委员会/白银市人民政府",
     "overlap_period": "2026年1月至今", "confidence": "confirmed"},

    # 刘凯 ↔ 朱利民 (书记↔专职副书记)
    {"person_a": "baiyin_liu_kai", "person_b": "baiyin_zhu_limin",
     "type": "superior_subordinate", "strength": "strong",
     "context": "朱利民协助刘凯抓党的建设工作，同时分管宣传",
     "overlap_org": "中共白银市委员会",
     "overlap_period": "当前", "confidence": "confirmed"},

    # 刘凯 ↔ 葛永宏 (书记↔常委)
    {"person_a": "baiyin_liu_kai", "person_b": "baiyin_ge_yonghong",
     "type": "superior_subordinate", "strength": "strong",
     "context": "葛永宏为市委常委、常务副市长，在刘凯领导下负责市政府常务工作",
     "overlap_org": "中共白银市委员会/白银市人民政府",
     "overlap_period": "当前", "confidence": "confirmed"},

    # 刘凯 ↔ 董兆生 (书记↔纪委书记)
    {"person_a": "baiyin_liu_kai", "person_b": "baiyin_dong_zhaosheng",
     "type": "superior_subordinate", "strength": "strong",
     "context": "董兆生在市委领导下负责全市纪检监察工作",
     "overlap_org": "中共白银市委员会",
     "overlap_period": "当前", "confidence": "confirmed"},

    # 刘凯 ↔ 丁肃静 (书记↔组织部长)
    {"person_a": "baiyin_liu_kai", "person_b": "baiyin_ding_sujing",
     "type": "superior_subordinate", "strength": "strong",
     "context": "丁肃静负责市委组织部工作，在书记领导下负责干部任用工作",
     "overlap_org": "中共白银市委员会",
     "overlap_period": "当前", "confidence": "confirmed"},

    # 张延保 ↔ 葛永宏 (市长↔常务副市长)
    {"person_a": "baiyin_zhang_yanbao", "person_b": "baiyin_ge_yonghong",
     "type": "superior_subordinate", "strength": "strong",
     "context": "葛永宏协助张延保负责市政府常务工作，分管发改、财政、金融等核心部门",
     "overlap_org": "白银市人民政府",
     "overlap_period": "当前", "confidence": "confirmed"},

    # 刘凯 ↔ 王彬 (书记↔企业领导常委)
    {"person_a": "baiyin_liu_kai", "person_b": "baiyin_wang_bin",
     "type": "superior_subordinate", "strength": "medium",
     "context": "王彬作为白银有色集团负责人兼任市委常委，属于企地合作安排",
     "overlap_org": "中共白银市委员会",
     "overlap_period": "当前", "confidence": "confirmed"},

    # 刘凯 ↔ 乔振华 (书记↔政法委书记)
    {"person_a": "baiyin_liu_kai", "person_b": "baiyin_qiao_zhenhua",
     "type": "superior_subordinate", "strength": "strong",
     "context": "乔振华负责全市政法工作，在书记领导下维护社会稳定",
     "overlap_org": "中共白银市委员会",
     "overlap_period": "当前", "confidence": "confirmed"},

    # 刘凯 ↔ 胡建伟 (书记↔秘书长)
    {"person_a": "baiyin_liu_kai", "person_b": "baiyin_hu_jianwei",
     "type": "superior_subordinate", "strength": "strong",
     "context": "胡建伟作为市委秘书长负责市委日常运转，直接服务于刘凯",
     "overlap_org": "中共白银市委员会",
     "overlap_period": "当前", "confidence": "confirmed"},
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
    if "市委书记" in current:
        return "255,50,50"
    if "市长" in current or "副市长" in current or "常务副" in current:
        return "50,100,255"
    if "纪委书记" in current or "监委" in current:
        return "255,165,0"
    return "100,100,100"


def is_top_leader(p):
    current = p.get("current_post", "")
    return "市委书记" in current or "市长" in current


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
    if "开发区" in t:
        return "200,255,200"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>白银市领导班子工作关系网络 — 中共白银市委员会、白银市人民政府、市人大、市政协</description>')
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
