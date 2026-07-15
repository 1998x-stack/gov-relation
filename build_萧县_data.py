#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 萧县 (Xiao County, Suzhou, Anhui).

Task: anhui_萧县 — 县委书记 & 县长
Province: 安徽省
City: 宿州市
Region: 萧县
Level: 县
Research date: 2026-07-15

Confirmed officeholders (as of 2026-07-15):
- 县委书记: 罗圣权 (born 1973.05, male, Han, graduate)
- 县长: 周瑜 (born 1987.06, male, Han, graduate)
- 县委专职副书记: 孙鹏 (born 1985.03, male, Han, graduate)
- 常务副县长: 侯传宇 (born 1980.10, male, Han, graduate)

县委常委会 (11 members):
罗圣权, 周瑜, 孙鹏, 侯传宇, 仇索, 马晓勇, 刘帅, 李世静, 魏舰艇, 马阳阳, 王莉

Sources:
- www.ahxx.gov.cn/zwgk/ldzc/ (official leadership page)
- ahxx.gov.cn individual profile pages

Confidence: Current leadership confirmed from ahxx.gov.cn official 领导之窗 page.
Career details limited — only identity-level data. Full career histories not
available on the official site (only birth year/s, gender, ethnicity, education, party status).
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Check if running from repo root or from staging
GOV_ROOT = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == "data" else SCRIPT_DIR
if "data/tmp" in SCRIPT_DIR:
    STAGING = SCRIPT_DIR
else:
    STAGING = os.path.join(GOV_ROOT, "data", "tmp", "anhui_萧县")
DB_PATH = os.path.join(STAGING, "萧县_network.db")
GEXF_PATH = os.path.join(STAGING, "萧县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 县委书记 — 罗圣权
    {
        "id": "xiaoxian_luo_shengquan",
        "name": "罗圣权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年5月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "萧县县委书记",
        "current_org": "中共萧县委员会",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "主持县委全面工作。1973年5月出生，中共党员，研究生学历。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 县长 — 周瑜
    {
        "id": "xiaoxian_zhou_yu",
        "name": "周瑜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年6月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "萧县县长",
        "current_org": "萧县人民政府",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "主持县政府全面工作。1987年6月出生，中共党员，研究生学历。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 县委专职副书记 — 孙鹏
    {
        "id": "xiaoxian_sun_peng",
        "name": "孙鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年3月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "萧县县委副书记、县委党校校长",
        "current_org": "中共萧县委员会",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "协助罗圣权同志抓党的建设工作，负责党的农村工作、群团工作、巡视整改、基层减负和督查考核工作。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 常务副县长 — 侯传宇
    {
        "id": "xiaoxian_hou_chuanyu",
        "name": "侯传宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年10月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "萧县县委常委、常务副县长",
        "current_org": "萧县人民政府",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "负责县政府常务工作。分管发改、财政、金融、应急、统计、商务等。完整履历待补充。",
        "confidence": "confirmed",
    },

    # ══════════════ Other Party Standing Committee ══════════════

    # 仇索 — 县委常委、副县长
    {
        "id": "xiaoxian_qiu_suo",
        "name": "仇索",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "萧县县委常委、副县长",
        "current_org": "萧县人民政府",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "分管工信、招商、园区、教育体育等。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 马晓勇 — 县人武部上校政委
    {
        "id": "xiaoxian_ma_xiaoyong",
        "name": "马晓勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年6月",
        "birthplace": "",
        "native_place": "",
        "education": "大学(MPA)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "萧县县委常委、县人武部上校政治委员",
        "current_org": "萧县人民武装部",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 刘帅 — 县纪委书记/监委主任
    {
        "id": "xiaoxian_liu_shuai",
        "name": "刘帅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年10月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "萧县县委常委、县纪委书记、县监委主任",
        "current_org": "中共萧县纪律检查委员会",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 李世静 — 组织部部长
    {
        "id": "xiaoxian_li_shijing",
        "name": "李世静",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年6月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "萧县县委常委、组织部部长",
        "current_org": "中共萧县委员会组织部",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 魏舰艇 — 统战部部长/县委办主任
    {
        "id": "xiaoxian_wei_jianting",
        "name": "魏舰艇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年5月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "萧县县委常委、统战部部长、县委办公室主任",
        "current_org": "中共萧县委员会",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 马阳阳 — 宣传部部长
    {
        "id": "xiaoxian_ma_yangyang",
        "name": "马阳阳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986年1月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "萧县县委常委、宣传部部长",
        "current_org": "中共萧县委员会宣传部",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # 王莉 — 政法委书记
    {
        "id": "xiaoxian_wang_li",
        "name": "王莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年8月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "萧县县委常委、政法委书记、凤城街道党工委书记",
        "current_org": "中共萧县委员会政法委员会",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "完整履历待补充。",
        "confidence": "confirmed",
    },

    # ══════════════ County Government ══════════════

    # 王静 — 副县长（挂职）
    {
        "id": "xiaoxian_wang_jing",
        "name": "王静",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萧县副县长人选（挂职二年）",
        "current_org": "萧县人民政府",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "挂职副县长人选，2026年7月仍在挂职期。",
        "confidence": "confirmed",
    },

    # 吴群 — 副县长
    {
        "id": "xiaoxian_wu_qun",
        "name": "吴群",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萧县副县长",
        "current_org": "萧县人民政府",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "",
        "confidence": "confirmed",
    },

    # 张鹏 — 副县长/公安局长
    {
        "id": "xiaoxian_zhang_peng",
        "name": "张鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萧县副县长、县公安局党委书记、局长、督察长",
        "current_org": "萧县公安局",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "四级高级警长。",
        "confidence": "confirmed",
    },

    # 王威 — 副县长（挂职）
    {
        "id": "xiaoxian_wang_wei",
        "name": "王威",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萧县副县长（挂职二年）",
        "current_org": "萧县人民政府",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "挂职副县长，2026年7月仍在挂职期。",
        "confidence": "confirmed",
    },

    # 刘圣军 — 副县长
    {
        "id": "xiaoxian_liu_shengjun",
        "name": "刘圣军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萧县副县长",
        "current_org": "萧县人民政府",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "",
        "confidence": "confirmed",
    },

    # ══════════════ County People's Congress ══════════════

    # 朱永亮 — 人大主任
    {
        "id": "xiaoxian_zhu_yongliang",
        "name": "朱永亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年6月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "萧县人大常委会党组书记、主任",
        "current_org": "萧县人大常委会",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "",
        "confidence": "confirmed",
    },

    # 蒋曦 — 人大副主任
    {
        "id": "xiaoxian_jiang_xi",
        "name": "蒋曦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萧县人大常委会副主任",
        "current_org": "萧县人大常委会",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "",
        "confidence": "confirmed",
    },

    # 丁勤华 — 人大副主任
    {
        "id": "xiaoxian_ding_qinhua",
        "name": "丁勤华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萧县人大常委会副主任",
        "current_org": "萧县人大常委会",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "",
        "confidence": "confirmed",
    },

    # 刘杰 — 人大副主任
    {
        "id": "xiaoxian_liu_jie",
        "name": "刘杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萧县人大常委会副主任",
        "current_org": "萧县人大常委会",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "",
        "confidence": "confirmed",
    },

    # ══════════════ County Political Consultative Conference ══════════════

    # 杨洪军 — 政协主席
    {
        "id": "xiaoxian_yang_hongjun",
        "name": "杨洪军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年6月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "萧县政协党组书记、主席",
        "current_org": "萧县政协",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "",
        "confidence": "confirmed",
    },

    # 肖民 — 政协副主席
    {
        "id": "xiaoxian_xiao_min",
        "name": "肖民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萧县政协党组副书记、副主席",
        "current_org": "萧县政协",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "",
        "confidence": "confirmed",
    },

    # 张艳 — 政协副主席
    {
        "id": "xiaoxian_zhang_yan",
        "name": "张艳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萧县政协副主席",
        "current_org": "萧县政协",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "",
        "confidence": "confirmed",
    },

    # 郑玉锦 — 政协副主席
    {
        "id": "xiaoxian_zheng_yujin",
        "name": "郑玉锦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萧县政协副主席",
        "current_org": "萧县政协",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "",
        "confidence": "confirmed",
    },

    # 张跃 — 政协副主席
    {
        "id": "xiaoxian_zhang_yue",
        "name": "张跃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萧县政协党组成员、副主席",
        "current_org": "萧县政协",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "",
        "confidence": "confirmed",
    },

    # 郑峰 — 政协副主席（兼工商联）
    {
        "id": "xiaoxian_zheng_feng",
        "name": "郑峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萧县政协副主席、县工商联主席",
        "current_org": "萧县政协",
        "source": "www.ahxx.gov.cn (领导之窗, 2026-07-15)",
        "notes": "",
        "confidence": "confirmed",
    },
]


organizations = [
    {"id": "cpc_xiaoxian", "name": "中共萧县委员会", "type": "党委", "level": "县", "parent": "中共宿州市委员会", "location": "安徽省宿州市萧县"},
    {"id": "gov_xiaoxian", "name": "萧县人民政府", "type": "政府", "level": "县", "parent": "宿州市人民政府", "location": "安徽省宿州市萧县"},
    {"id": "npc_xiaoxian", "name": "萧县人大常委会", "type": "人大", "level": "县", "parent": "", "location": "安徽省宿州市萧县"},
    {"id": "cppcc_xiaoxian", "name": "萧县政协", "type": "政协", "level": "县", "parent": "", "location": "安徽省宿州市萧县"},
    {"id": "dis_xiaoxian", "name": "中共萧县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共宿州市纪律检查委员会", "location": "安徽省宿州市萧县"},
    {"id": "org_xiaoxian", "name": "中共萧县委员会组织部", "type": "党委", "level": "县", "parent": "中共萧县委员会", "location": "安徽省宿州市萧县"},
    {"id": "prop_xiaoxian", "name": "中共萧县委员会宣传部", "type": "党委", "level": "县", "parent": "中共萧县委员会", "location": "安徽省宿州市萧县"},
    {"id": "united_xiaoxian", "name": "中共萧县委员会统战部", "type": "党委", "level": "县", "parent": "中共萧县委员会", "location": "安徽省宿州市萧县"},
    {"id": "polit_xiaoxian", "name": "中共萧县委员会政法委员会", "type": "党委", "level": "县", "parent": "中共萧县委员会", "location": "安徽省宿州市萧县"},
    {"id": "mil_xiaoxian", "name": "萧县人民武装部", "type": "事业单位", "level": "县", "parent": "", "location": "安徽省宿州市萧县"},
    {"id": "psb_xiaoxian", "name": "萧县公安局", "type": "政府", "level": "县", "parent": "萧县人民政府", "location": "安徽省宿州市萧县"},
    {"id": "party_school_xiaoxian", "name": "中共萧县县委党校", "type": "事业单位", "level": "县", "parent": "中共萧县委员会", "location": "安徽省宿州市萧县"},
    {"id": "sub_xiaoxian_fengcheng", "name": "萧县凤城街道党工委", "type": "乡镇/街道", "level": "乡镇", "parent": "中共萧县委员会", "location": "安徽省宿州市萧县凤城街道"},
]


positions = [
    # 罗圣权
    {"person_id": "xiaoxian_luo_shengquan", "org_id": "cpc_xiaoxian", "title": "萧县县委书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 周瑜
    {"person_id": "xiaoxian_zhou_yu", "org_id": "gov_xiaoxian", "title": "萧县县长", "start": "", "end": "present", "rank": "正处级", "note": "同时兼任县委副书记、县政府党组书记"},
    {"person_id": "xiaoxian_zhou_yu", "org_id": "cpc_xiaoxian", "title": "萧县县委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 孙鹏
    {"person_id": "xiaoxian_sun_peng", "org_id": "cpc_xiaoxian", "title": "萧县县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "专职副书记"},
    {"person_id": "xiaoxian_sun_peng", "org_id": "party_school_xiaoxian", "title": "萧县县委党校校长", "start": "", "end": "present", "rank": "副处级", "note": "兼任"},
    # 侯传宇
    {"person_id": "xiaoxian_hou_chuanyu", "org_id": "cpc_xiaoxian", "title": "萧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_hou_chuanyu", "org_id": "gov_xiaoxian", "title": "萧县常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组副书记"},
    # 仇索
    {"person_id": "xiaoxian_qiu_suo", "org_id": "cpc_xiaoxian", "title": "萧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_qiu_suo", "org_id": "gov_xiaoxian", "title": "萧县副县长", "start": "", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    # 马晓勇
    {"person_id": "xiaoxian_ma_xiaoyong", "org_id": "cpc_xiaoxian", "title": "萧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_ma_xiaoyong", "org_id": "mil_xiaoxian", "title": "萧县人武部上校政治委员", "start": "", "end": "present", "rank": "副师级/上校", "note": ""},
    # 刘帅
    {"person_id": "xiaoxian_liu_shuai", "org_id": "cpc_xiaoxian", "title": "萧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_liu_shuai", "org_id": "dis_xiaoxian", "title": "萧县纪委书记、县监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 李世静
    {"person_id": "xiaoxian_li_shijing", "org_id": "cpc_xiaoxian", "title": "萧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_li_shijing", "org_id": "org_xiaoxian", "title": "萧县县委组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 魏舰艇
    {"person_id": "xiaoxian_wei_jianting", "org_id": "cpc_xiaoxian", "title": "萧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_wei_jianting", "org_id": "united_xiaoxian", "title": "萧县县委统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_wei_jianting", "org_id": "cpc_xiaoxian", "title": "萧县县委办公室主任", "start": "", "end": "present", "rank": "副处级", "note": "兼任"},
    # 马阳阳
    {"person_id": "xiaoxian_ma_yangyang", "org_id": "cpc_xiaoxian", "title": "萧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_ma_yangyang", "org_id": "prop_xiaoxian", "title": "萧县县委宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王莉
    {"person_id": "xiaoxian_wang_li", "org_id": "cpc_xiaoxian", "title": "萧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_wang_li", "org_id": "polit_xiaoxian", "title": "萧县县委政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_wang_li", "org_id": "sub_xiaoxian_fengcheng", "title": "萧县凤城街道党工委书记", "start": "", "end": "present", "rank": "正科级", "note": "兼任"},

    # Government
    {"person_id": "xiaoxian_wang_jing", "org_id": "gov_xiaoxian", "title": "萧县副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "挂职二年"},
    {"person_id": "xiaoxian_wu_qun", "org_id": "gov_xiaoxian", "title": "萧县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_zhang_peng", "org_id": "gov_xiaoxian", "title": "萧县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_zhang_peng", "org_id": "psb_xiaoxian", "title": "萧县公安局党委书记、局长、督察长", "start": "", "end": "present", "rank": "副处级", "note": "四级高级警长"},
    {"person_id": "xiaoxian_wang_wei", "org_id": "gov_xiaoxian", "title": "萧县副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "挂职二年"},
    {"person_id": "xiaoxian_liu_shengjun", "org_id": "gov_xiaoxian", "title": "萧县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # NPC
    {"person_id": "xiaoxian_zhu_yongliang", "org_id": "npc_xiaoxian", "title": "萧县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "党组书记"},
    {"person_id": "xiaoxian_jiang_xi", "org_id": "npc_xiaoxian", "title": "萧县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_ding_qinhua", "org_id": "npc_xiaoxian", "title": "萧县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_liu_jie", "org_id": "npc_xiaoxian", "title": "萧县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # CPPCC
    {"person_id": "xiaoxian_yang_hongjun", "org_id": "cppcc_xiaoxian", "title": "萧县政协主席", "start": "", "end": "present", "rank": "正处级", "note": "党组书记"},
    {"person_id": "xiaoxian_xiao_min", "org_id": "cppcc_xiaoxian", "title": "萧县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": "党组副书记"},
    {"person_id": "xiaoxian_zhang_yan", "org_id": "cppcc_xiaoxian", "title": "萧县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_zheng_yujin", "org_id": "cppcc_xiaoxian", "title": "萧县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "xiaoxian_zhang_yue", "org_id": "cppcc_xiaoxian", "title": "萧县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": "党组成员"},
    {"person_id": "xiaoxian_zheng_feng", "org_id": "cppcc_xiaoxian", "title": "萧县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": "兼县工商联主席"},
]


# ── Relationship edges ──────────────────────────────────────────────────

relationships = [
    # 罗圣权 ↔ 周瑜 (县委书记↔县长, 党政一把手搭档)
    {"person_a": "xiaoxian_luo_shengquan", "person_b": "xiaoxian_zhou_yu",
     "type": "superior_subordinate", "strength": "strong",
     "context": "党政一把手搭档，罗圣权主持县委全面工作，周瑜主持县政府全面工作",
     "overlap_org": "中共萧县委员会/萧县人民政府",
     "overlap_period": "当前", "confidence": "confirmed"},

    # 罗圣权 ↔ 孙鹏 (书记↔专职副书记)
    {"person_a": "xiaoxian_luo_shengquan", "person_b": "xiaoxian_sun_peng",
     "type": "superior_subordinate", "strength": "strong",
     "context": "孙鹏协助罗圣权抓党的建设工作",
     "overlap_org": "中共萧县委员会",
     "overlap_period": "当前", "confidence": "confirmed"},

    # 周瑜 ↔ 侯传宇 (县长↔常务副县长)
    {"person_a": "xiaoxian_zhou_yu", "person_b": "xiaoxian_hou_chuanyu",
     "type": "superior_subordinate", "strength": "strong",
     "context": "侯传宇协助周瑜负责县政府常务工作",
     "overlap_org": "萧县人民政府",
     "overlap_period": "当前", "confidence": "confirmed"},

    # 罗圣权 ↔ 刘帅 (书记↔纪委书记)
    {"person_a": "xiaoxian_luo_shengquan", "person_b": "xiaoxian_liu_shuai",
     "type": "superior_subordinate", "strength": "strong",
     "context": "刘帅在县委领导下负责全县纪检监察工作",
     "overlap_org": "中共萧县委员会",
     "overlap_period": "当前", "confidence": "confirmed"},

    # 罗圣权 ↔ 李世静 (书记↔组织部长)
    {"person_a": "xiaoxian_luo_shengquan", "person_b": "xiaoxian_li_shijing",
     "type": "superior_subordinate", "strength": "strong",
     "context": "李世静负责县委组织部工作，在书记领导下负责干部工作",
     "overlap_org": "中共萧县委员会",
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
    lines.append('    <description>萧县领导班子工作关系网络 — 中共萧县委员会、萧县人民政府、县人大、县政协</description>')
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
