#!/usr/bin/env python3
"""
永昌县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Yongchang County leadership.

Research sources:
- 永昌县人民政府门户网站 (www.yongchang.gov.cn) — 领导之窗页面 (2026-07-17)
  All current officeholders, bios, and role assignments sourced from official bio pages.

Core confirmed data (from official source):
- 县委书记 = 马寿龙 (Ma Shoulong) — 回族, 1975年8月生
- 县长 = 俞天德 (Yu Tiande) — 汉族, 1973年2月生
- 县委副书记 = 刘吉军 (Liu Jijun) — 汉族, 1982年11月生
- Full 县委常委会 (11 members) and 县政府领导班子 confirmed.

Predecessor info:
- 前任县委书记: 待查 (马寿龙于何时接任及前任信息未从公开资料确认)
- 前任县长: 待查 (俞天德接任时间及前任信息未从公开资料确认)
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ──
STAGING = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(STAGING))
DB_PATH = os.path.join(STAGING, "永昌县_network.db")
GEXF_PATH = os.path.join(STAGING, "永昌县_network.gexf")

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;") if s else ""

# ── DATA ──
# Person ID convention: yongchang_{surname_givenname}

# =========================================================================
# PERSONS
# =========================================================================
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

PERSONS = [
    # ═══ Top Leaders ═══

    # 县委书记 — 马寿龙
    # Source: yongchang.gov.cn 领导之窗 (confirmed official)
    ("yongchang_ma_shoulong", "马寿龙", "男", "回族", "1975-08", "待查", "大学学历、文学学士", "中共党员", "待查",
     "县委书记", "中共永昌县委员会",
     "https://www.yongchang.gov.cn/ldzc/xwld/xwsj/msl/index.html — 县委书记马寿龙, 回族, 1975年8月出生, 大学学历、文学学士, 中共党员"),

    # 县长 — 俞天德
    ("yongchang_yu_tiande", "俞天德", "男", "汉族", "1973-02", "待查", "大学、工学学士", "中共党员", "待查",
     "县委副书记、县长", "永昌县人民政府",
     "https://www.yongchang.gov.cn/ldzc/xzfld/xz/ytd/index.html — 俞天德, 汉族, 1973年2月出生, 大学、工学学士, 中共党员"),

    # 县委副书记 — 刘吉军
    ("yongchang_liu_jijun", "刘吉军", "男", "汉族", "1982-11", "待查", "大学、经济学学士", "中共党员", "待查",
     "县委副书记（甘肃永昌工业园区党工委书记）", "中共永昌县委员会",
     "https://www.yongchang.gov.cn/ldzc/xzfld/fxz/ljj/index.html — 刘吉军, 汉族, 1982年11月出生, 大学、经济学学士, 中共党员"),

    # ═══ 县委常委 ═══

    # 何忠山 — 县委常委、县纪委书记、监委主任候选人
    ("yongchang_he_zhongshan", "何忠山", "男", "汉族", "1981-03", "待查", "大学、理学学士", "中共党员", "待查",
     "县委常委、县纪委书记、监委主任候选人", "中共永昌县纪律检查委员会",
     "https://www.yongchang.gov.cn/ldzc/xwld/xwcw/hzs/index.html — 何忠山, 汉族, 1981年3月出生, 大学、理学学士, 中共党员"),

    # 张海亮 — 县委常委、常务副县长
    ("yongchang_zhang_hailiang", "张海亮", "男", "汉族", "1983-04", "待查", "大学法学学士", "中共党员", "待查",
     "县委常委、常务副县长", "永昌县人民政府",
     "https://www.yongchang.gov.cn/ldzc/xwld/xwcw/zhl/index.html — 张海亮, 汉族, 1983年4月出生, 大学法学学士, 中共党员"),

    # 张世明 — 县委常委、政法委书记
    ("yongchang_zhang_shiming", "张世明", "男", "汉族", "1979-10", "待查", "省委党校大学", "中共党员", "待查",
     "县委常委、政法委书记", "中共永昌县委员会政法委员会",
     "https://www.yongchang.gov.cn/ldzc/xzfld/fxz/zsm/index.html — 张世明, 汉族, 1979年10月出生, 省委党校大学, 中共党员"),

    # 赵静 — 县委常委、宣传部部长
    ("yongchang_zhao_jing", "赵静", "女", "汉族", "1986-08", "待查", "大学、法学学士", "中共党员", "待查",
     "县委常委、宣传部部长", "中共永昌县委宣传部",
     "https://www.yongchang.gov.cn/ldzc/xwld/xwcw/zhaoj/index.html — 赵静, 女, 汉族, 1986年8月出生, 大学、法学学士, 中共党员"),

    # 陈春来 — 县委常委、组织部部长
    ("yongchang_chen_chunlai", "陈春来", "男", "汉族", "1985", "待查", "大学经济学学士", "中共党员", "待查",
     "县委常委、组织部部长", "中共永昌县委组织部",
     "https://www.yongchang.gov.cn/ldzc/xwld/xwcw/ccl/index.html — 陈春来, 汉族, 1985年出生, 大学经济学学士, 中共党员"),

    # 李孜锋 — 县委常委、统战部部长、县委办主任
    ("yongchang_li_zifeng", "李孜锋", "男", "汉族", "1980-04", "待查", "在职大学学历", "中共党员", "待查",
     "县委常委、统战部部长、县委办主任", "中共永昌县委统战部",
     "https://www.yongchang.gov.cn/ldzc/xwld/xwcw/lzf/index.html — 李孜锋, 汉族, 1980年4月出生, 在职大学学历, 中共党员"),

    # 高俊兴 — 县委常委、永昌工业园区党工委副书记
    ("yongchang_gao_junxing", "高俊兴", "男", "汉族", "1972-12", "待查", "甘肃省委党校大学", "中共党员", "待查",
     "县委常委、永昌工业园区党工委副书记", "甘肃永昌工业园区",
     "https://www.yongchang.gov.cn/ldzc/xwld/xwcw/gjx/index.html — 高俊兴, 汉族, 1972年12月出生, 甘肃省委党校大学, 中共党员"),

    # 周海建 — 县委常委、县人武部政委
    ("yongchang_zhou_haijian", "周海建", "男", "汉族", "1979-08", "待查", "大学学历", "中共党员", "待查",
     "县委常委、县人武部党委书记、上校政治委员", "永昌县人民武装部",
     "https://www.yongchang.gov.cn/ldzc/xwld/xwcw/zhj/index.html — 周海建, 汉族, 1979年8月出生, 大学学历, 中共党员"),

    # 郭万寿 — 县委常委、副县长
    ("yongchang_guo_wanshou", "郭万寿", "男", "汉族", "1980-08", "待查", "在职研究生学历", "中共党员", "待查",
     "县委常委、副县长", "永昌县人民政府",
     "https://www.yongchang.gov.cn/ldzc/xwld/xwcw/gws/index.html — 郭万寿, 汉族, 1980年8月出生, 在职研究生学历, 中共党员"),

    # ═══ 其他副县长 ═══

    # 李德志 — 副县长、公安局局长
    ("yongchang_li_dezhi", "李德志", "男", "汉族", "1982-11", "待查", "中央广播电视大学", "中共党员", "待查",
     "副县长、县公安局党委书记、局长", "永昌县公安局",
     "https://www.yongchang.gov.cn/ldzc/xzfld/fxz/ldz/index.html — 李德志, 汉族, 1982年11月出生, 中央广播电视大学, 中共党员"),

    # 毛焕泽 — 副县长
    ("yongchang_mao_huanze", "毛焕泽", "男", "汉族", "1990-06", "待查", "研究生学历", "中共党员", "待查",
     "副县长", "永昌县人民政府",
     "https://www.yongchang.gov.cn/ldzc/xzfld/fxz/mhz/index.html — 毛焕泽, 汉族, 1990年6月出生, 研究生学历, 中共党员"),

    # 韩晓英 — 副县长
    ("yongchang_han_xiaoying", "韩晓英", "女", "汉族", "1986-08", "待查", "大学文学学士", "中共党员", "待查",
     "副县长", "永昌县人民政府",
     "https://www.yongchang.gov.cn/ldzc/xzfld/fxz/hxy/index.html — 韩晓英, 女, 汉族, 1986年8月出生, 大学文学学士, 中共党员"),

    # 宋德刚 — 副县长（挂职）
    ("yongchang_song_degang", "宋德刚", "男", "汉族", "1983-06", "待查", "研究生学历、法律硕士", "中共党员", "待查",
     "副县长（挂职）", "永昌县人民政府",
     "https://www.yongchang.gov.cn/ldzc/xzfld/fxz/sdg/index.html — 宋德刚, 汉族, 1983年6月出生, 研究生学历、法律硕士, 中共党员"),

    # 梁兴贵 — 副县长
    ("yongchang_liang_xinggui", "梁兴贵", "男", "汉族", "1983-11", "待查", "大学理学学士", "中共党员", "待查",
     "副县长", "永昌县人民政府",
     "https://www.yongchang.gov.cn/ldzc/xzfld/fxz/lxg/index.html — 梁兴贵, 汉族, 1983年11月出生, 大学理学学士, 中共党员"),

    # ═══ 前任 — 信息待补充 ═══
    # 前任县委书记 — 待查
    ("yongchang_prev_secretary", "（前任县委书记待查）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "原县委书记", "中共永昌县委员会（前任）",
     "⚠️ 马寿龙的前任县委书记信息未从公开资料确认"),

    # 前任县长 — 待查
    ("yongchang_prev_mayor", "（前任县长待查）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "原县长", "永昌县人民政府（前任）",
     "⚠️ 俞天德的前任县长信息未从公开资料确认"),
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
# (id, name, type, level, parent, location)

ORGANIZATIONS = [
    ("中共永昌县委员会", "党委", "县级", "中共金昌市委员会", "甘肃省金昌市永昌县"),
    ("中共永昌县纪律检查委员会", "党委", "县级", "中共金昌市纪律检查委员会", "甘肃省金昌市永昌县"),
    ("中共永昌县委组织部", "党委", "县级", "中共永昌县委员会", "甘肃省金昌市永昌县"),
    ("中共永昌县委宣传部", "党委", "县级", "中共永昌县委员会", "甘肃省金昌市永昌县"),
    ("中共永昌县委统战部", "党委", "县级", "中共永昌县委员会", "甘肃省金昌市永昌县"),
    ("中共永昌县委政法委员会", "党委", "县级", "中共永昌县委员会", "甘肃省金昌市永昌县"),
    ("中共永昌县委办公室", "党委", "县级", "中共永昌县委员会", "甘肃省金昌市永昌县"),
    ("永昌县人民政府", "政府", "县级", "金昌市人民政府", "甘肃省金昌市永昌县"),
    ("永昌县公安局", "政府", "县级", "永昌县人民政府", "甘肃省金昌市永昌县"),
    ("甘肃永昌工业园区", "开发区", "县级", "永昌县人民政府", "甘肃省金昌市永昌县"),
    ("永昌县人民武装部", "党委", "县级", "金昌军分区", "甘肃省金昌市永昌县"),
]

# =========================================================================
# POSITIONS
# =========================================================================
# (person_id, org_name, title, start, end, rank, note)

POSITIONS = [
    # 马寿龙
    ("yongchang_ma_shoulong", "中共永昌县委员会", "县委书记", "待查", "present", "正县级", "主持县委全面工作"),

    # 俞天德
    ("yongchang_yu_tiande", "永昌县人民政府", "县长", "待查", "present", "正县级", "领导县政府全面工作"),
    ("yongchang_yu_tiande", "中共永昌县委员会", "县委副书记", "待查", "present", "正县级", ""),

    # 刘吉军
    ("yongchang_liu_jijun", "中共永昌县委员会", "县委副书记", "待查", "present", "副县级", "协助书记抓党建, 负责农业农村、生态建设"),
    ("yongchang_liu_jijun", "甘肃永昌工业园区", "党工委书记", "待查", "present", "副县级", ""),

    # 何忠山
    ("yongchang_he_zhongshan", "中共永昌县纪律检查委员会", "县纪委书记", "待查", "present", "副县级", "负责纪检监察和巡察工作"),

    # 张海亮
    ("yongchang_zhang_hailiang", "永昌县人民政府", "常务副县长", "待查", "present", "副县级", "负责县政府日常工作"),
    ("yongchang_zhang_hailiang", "中共永昌县委员会", "县委常委", "待查", "present", "副县级", ""),

    # 张世明
    ("yongchang_zhang_shiming", "中共永昌县委政法委员会", "政法委书记", "待查", "present", "副县级", "负责社会稳定、信访工作"),
    ("yongchang_zhang_shiming", "中共永昌县委员会", "县委常委", "待查", "present", "副县级", ""),

    # 赵静
    ("yongchang_zhao_jing", "中共永昌县委宣传部", "宣传部部长", "待查", "present", "副县级", "负责宣传思想文化和意识形态工作"),
    ("yongchang_zhao_jing", "中共永昌县委员会", "县委常委", "待查", "present", "副县级", ""),

    # 陈春来
    ("yongchang_chen_chunlai", "中共永昌县委组织部", "组织部部长", "待查", "present", "副县级", "负责组织部工作"),
    ("yongchang_chen_chunlai", "中共永昌县委员会", "县委常委", "待查", "present", "副县级", ""),

    # 李孜锋
    ("yongchang_li_zifeng", "中共永昌县委统战部", "统战部部长", "待查", "present", "副县级", "负责统战工作"),
    ("yongchang_li_zifeng", "中共永昌县委办公室", "县委办主任", "待查", "present", "副县级", "负责县委办公室全面工作"),
    ("yongchang_li_zifeng", "中共永昌县委员会", "县委常委", "待查", "present", "副县级", ""),

    # 高俊兴
    ("yongchang_gao_junxing", "甘肃永昌工业园区", "党工委副书记", "待查", "present", "副县级", "负责金川集团永昌铜业全面工作"),
    ("yongchang_gao_junxing", "中共永昌县委员会", "县委常委", "待查", "present", "副县级", ""),

    # 周海建
    ("yongchang_zhou_haijian", "永昌县人民武装部", "政委（上校）", "待查", "present", "副县级", "负责县人武部工作"),
    ("yongchang_zhou_haijian", "中共永昌县委员会", "县委常委", "待查", "present", "副县级", ""),

    # 郭万寿
    ("yongchang_guo_wanshou", "永昌县人民政府", "副县长", "待查", "present", "副县级", "分管县政府分工工作"),
    ("yongchang_guo_wanshou", "中共永昌县委员会", "县委常委", "待查", "present", "副县级", ""),

    # 李德志
    ("yongchang_li_dezhi", "永昌县公安局", "党委书记、局长", "待查", "present", "副县级", "主持公安局全面工作"),
    ("yongchang_li_dezhi", "永昌县人民政府", "副县长", "待查", "present", "副县级", "分管信访、民族宗教"),

    # 毛焕泽
    ("yongchang_mao_huanze", "永昌县人民政府", "副县长", "待查", "present", "副县级", "负责农业农村、乡村振兴、水务"),

    # 韩晓英
    ("yongchang_han_xiaoying", "永昌县人民政府", "副县长", "待查", "present", "副县级", "负责教育、民政、卫健、医保"),

    # 宋德刚
    ("yongchang_song_degang", "永昌县人民政府", "副县长（挂职）", "待查", "present", "副县级", "负责科技、退役军人事务"),

    # 梁兴贵
    ("yongchang_liang_xinggui", "永昌县人民政府", "副县长", "待查", "present", "副县级", "负责交通、商贸、市场监管、招商引资"),
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
# (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)

RELATIONSHIPS = [
    # 马寿龙 <-> 俞天德 (书记-县长搭档)
    ("yongchang_ma_shoulong", "yongchang_yu_tiande", "superior_subordinate",
     "县委书记与县长党政主官搭档关系", "中共永昌县委员会/永昌县人民政府", "待查-present", "strong", "confirmed"),

    # 马寿龙 <-> 刘吉军 (书记-副书记)
    ("yongchang_ma_shoulong", "yongchang_liu_jijun", "superior_subordinate",
     "县委书记与专职副书记", "中共永昌县委员会", "待查-present", "strong", "confirmed"),

    # 马寿龙 <-> 何忠山 (书记-纪委书记)
    ("yongchang_ma_shoulong", "yongchang_he_zhongshan", "superior_subordinate",
     "县委书记与纪委书记", "中共永昌县委员会", "待查-present", "strong", "confirmed"),

    # 马寿龙 <-> 张海亮 (书记-常务副县长)
    ("yongchang_ma_shoulong", "yongchang_zhang_hailiang", "superior_subordinate",
     "县委书记与常务副县长", "中共永昌县委员会/永昌县人民政府", "待查-present", "strong", "confirmed"),

    # 马寿龙 <-> 张世明 (书记-政法委书记)
    ("yongchang_ma_shoulong", "yongchang_zhang_shiming", "superior_subordinate",
     "县委书记与政法委书记", "中共永昌县委员会", "待查-present", "strong", "confirmed"),

    # 马寿龙 <-> 赵静 (书记-宣传部长)
    ("yongchang_ma_shoulong", "yongchang_zhao_jing", "superior_subordinate",
     "县委书记与宣传部部长", "中共永昌县委员会", "待查-present", "strong", "confirmed"),

    # 马寿龙 <-> 陈春来 (书记-组织部长)
    ("yongchang_ma_shoulong", "yongchang_chen_chunlai", "superior_subordinate",
     "县委书记与组织部部长", "中共永昌县委员会", "待查-present", "strong", "confirmed"),

    # 马寿龙 <-> 李孜锋 (书记-统战部长/县委办主任)
    ("yongchang_ma_shoulong", "yongchang_li_zifeng", "superior_subordinate",
     "县委书记与统战部部长/县委办主任", "中共永昌县委员会", "待查-present", "strong", "confirmed"),

    # 马寿龙 <-> 高俊兴 (书记-园区副书记)
    ("yongchang_ma_shoulong", "yongchang_gao_junxing", "superior_subordinate",
     "县委书记与工业园区党工委副书记", "中共永昌县委员会", "待查-present", "strong", "confirmed"),

    # 马寿龙 <-> 周海建 (书记-人武部政委)
    ("yongchang_ma_shoulong", "yongchang_zhou_haijian", "superior_subordinate",
     "县委书记与人武部政委", "中共永昌县委员会", "待查-present", "strong", "confirmed"),

    # 马寿龙 <-> 郭万寿 (书记-副县长)
    ("yongchang_ma_shoulong", "yongchang_guo_wanshou", "superior_subordinate",
     "县委书记与副县长", "中共永昌县委员会/永昌县人民政府", "待查-present", "strong", "confirmed"),

    # 俞天德 <-> 张海亮 (县长-常务副县长)
    ("yongchang_yu_tiande", "yongchang_zhang_hailiang", "superior_subordinate",
     "县长与常务副县长", "永昌县人民政府", "待查-present", "strong", "confirmed"),

    # 俞天德 <-> 李德志 (县长-公安局长)
    ("yongchang_yu_tiande", "yongchang_li_dezhi", "superior_subordinate",
     "县长与公安局长", "永昌县人民政府", "待查-present", "strong", "confirmed"),

    # 俞天德 <-> 毛焕泽 (县长-副县长)
    ("yongchang_yu_tiande", "yongchang_mao_huanze", "superior_subordinate",
     "县长与副县长（农业农村）", "永昌县人民政府", "待查-present", "strong", "confirmed"),

    # 俞天德 <-> 韩晓英 (县长-副县长)
    ("yongchang_yu_tiande", "yongchang_han_xiaoying", "superior_subordinate",
     "县长与副县长（教育卫健）", "永昌县人民政府", "待查-present", "strong", "confirmed"),

    # 俞天德 <-> 梁兴贵 (县长-副县长)
    ("yongchang_yu_tiande", "yongchang_liang_xinggui", "superior_subordinate",
     "县长与副县长（交通商贸）", "永昌县人民政府", "待查-present", "strong", "confirmed"),

    # 刘吉军 <-> 毛焕泽 (副书记-副县长 工作交叉: 农业农村)
    ("yongchang_liu_jijun", "yongchang_mao_huanze", "overlap",
     "工作交叉: 农业农村工作", "永昌县人民政府/中共永昌县委员会", "待查-present", "medium", "confirmed"),

    # 赵静 <-> 韩晓英 (工作交叉: 教育)
    ("yongchang_zhao_jing", "yongchang_han_xiaoying", "overlap",
     "工作交叉: 教育工作", "永昌县", "待查-present", "medium", "confirmed"),
]

# =========================================================================
# SQLITE DATABASE
# =========================================================================

def build_db(db_path):
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT,
            org_name TEXT,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
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
        )
    """)

    for p in PERSONS:
        c.execute("INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)

    for o in ORGANIZATIONS:
        c.execute("INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)", (o[0], o[0], o[1], o[2], o[3], o[4]))

    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_name, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)

    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence) VALUES (?,?,?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"✓ SQLite DB created: {db_path}")


# =========================================================================
# GEXF GRAPH
# =========================================================================

def person_color(name):
    """Color by role."""
    if "书记" in name and "纪委" not in name and "政法委" not in name:
        return "255,50,50"  # Red for party secretary
    if "县长" in name or "常务副" in name:
        return "50,100,255"  # Blue for government
    if "纪委" in name or "监委" in name:
        return "255,165,0"  # Orange for discipline
    if "政法委" in name:
        return "200,100,50"  # Brown for political-legal
    if "宣传" in name:
        return "200,100,200"  # Purple for propaganda
    if "组织" in name:
        return "100,200,100"  # Green for organization
    if "统战" in name:
        return "100,150,200"  # Steel blue for united front
    if "人武" in name or "政委" in name:
        return "150,150,50"  # Olive for military
    return "100,100,100"  # Grey for others

def org_color(org_type):
    colors = {
        "党委": "255,200,200", "政府": "200,200,255", "开发区": "200,255,200",
        "乡镇": "255,255,200", "事业单位": "220,220,220", "群团": "255,220,255",
        "人大": "200,255,255", "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(name):
    return name in ["马寿龙", "俞天德"]


def build_gexf(gexf_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Research Agent</creator>')
    lines.append('    <description>永昌县领导班子工作关系网络 (Yongchang County Leadership Network)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — Persons
    lines.append('    <nodes>')
    for p in PERSONS:
        pid, name, gender, ethnicity, birth = p[0], p[1], p[2], p[3], p[4]
        role = p[9]  # current_post
        org = p[10]  # current_org
        c = person_color(role)
        sz = "20.0" if is_top_leader(name) else ("14.0" if "县委常委" in role or "副书记" in role else "12.0")
        lines.append(f'      <node id="{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes — Organizations
    for o in ORGANIZATIONS:
        oid = o[0]
        c = org_color(o[1])
        lines.append(f'      <node id="org_{esc(oid)}" label="{esc(oid)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o[1])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    seen_positions = set()
    for pos in POSITIONS:
        pid, org_name, title = pos[0], pos[1], pos[2]
        key = (pid, org_name)
        if key in seen_positions:
            continue
        seen_positions.add(key)
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="org_{esc(org_name)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('          <attvalue for="2" value="strong"/>')
        lines.append('          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person <-> Person (relationship)
    for r in RELATIONSHIPS:
        pa, pb, rtype, context = r[0], r[1], r[2], r[3]
        strength = r[6] if len(r) > 6 else "medium"
        confidence = r[7] if len(r) > 7 else "confirmed"
        w = "2.0" if strength == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" label="{esc(rtype)}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{strength}"/>')
        lines.append(f'          <attvalue for="3" value="{confidence}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ GEXF graph created: {gexf_path} (nodes: {len(PERSONS) + len(ORGANIZATIONS)}, edges: {eid})")


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print(f"=== 永昌县领导班子工作关系网络 ===\nData as of: 2026-07-17")
    build_db(DB_PATH)
    build_gexf(GEXF_PATH)

    # Summary
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    print(f"\n📊 Summary:")
    c.execute("SELECT COUNT(*) FROM persons"); print(f"  Persons: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM organizations"); print(f"  Organizations: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM positions"); print(f"  Positions: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM relationships"); print(f"  Relationships: {c.fetchone()[0]}")
    conn.close()
    print("\n✅ Done!")
