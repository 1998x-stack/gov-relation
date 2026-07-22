#!/usr/bin/env python3
"""
北京市平谷区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Pinggu District leadership.

Data sources:
- bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/ (official leadership pages, accessed 2026-07-16)
- bjpg.gov.cn/pgqrmzf/zwxx0/jrpg/ (news articles confirming roles, accessed 2026-07-16)

Note on administrative rank: 平谷区 is a 市辖区 (district) of Beijing,
which is a 直辖市 (municipality directly under the central government).
District-level leaders in Beijing hold sub-provincial (副省级/副部级) rank
for the top positions, and bureau-director (正局级/正厅级) for others.
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "平谷区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "平谷区_network.gexf")

# ════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════

# Person ID convention: pinggu_{surname_givenname}
PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ════════════════════════════════════════════════════════════
    # 区委 — District Party Committee
    # ════════════════════════════════════════════════════════════

    # ── Top Leaders ──
    ("pinggu_di_tao", "狄涛", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委书记", "中共北京市平谷区委员会",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qw/"),

    ("pinggu_li_zhisui", "李志遂", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委副书记、区政府党组书记、区长", "北京市平谷区人民政府",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qw/"),

    # ── Deputy Party Secretary ──
    ("pinggu_ge_haibin", "葛海斌", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委副书记、兼区委党校校长", "中共北京市平谷区委党校",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qw/"),

    # ── Standing Committee Members ──
    ("pinggu_gao_lei", "高磊", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委、宣传部部长", "中共北京市平谷区委宣传部",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qw/"),

    ("pinggu_zhao_wenkan", "赵文侃", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委、区政府党组副书记、常务副区长", "北京市平谷区人民政府",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qw/"),

    ("pinggu_xie_huancheng", "颉换成", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委、区政府党组成员、副区长", "北京市平谷区人民政府",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qw/"),

    ("pinggu_zhang_shengjun", "张胜军", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委、组织部部长", "中共北京市平谷区委组织部",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qw/"),

    ("pinggu_yu_jianbo", "于建波", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委、区纪委书记，区监委主任，二级高级监察官", "中共北京市平谷区纪律检查委员会",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qw/"),

    ("pinggu_liu_kun", "刘堃", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委、统战部部长、兼区政协党组副书记", "中共北京市平谷区委统战部",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qw/"),

    ("pinggu_li_ziteng", "李子腾", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委、政法委书记", "中共北京市平谷区委政法委员会",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qw/"),

    ("pinggu_zhou_guoxiang", "周国祥", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委、武装部政治委员", "北京市平谷区人民武装部",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qw/"),

    # ════════════════════════════════════════════════════════════
    # 区政府 — District Government
    # ════════════════════════════════════════════════════════════

    ("pinggu_zang_xuemin", "臧学民", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区政府党组成员、副区长、市公安局平谷分局党委书记、局长", "北京市公安局平谷分局",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzf/"),

    ("pinggu_ma_dongmei", "马冬梅", "女", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区政府党组成员、副区长", "北京市平谷区人民政府",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzf/"),

    ("pinggu_fu_qiang", "付强", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区政府党组成员、副区长", "北京市平谷区人民政府",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzf/"),

    ("pinggu_peng_shi", "彭石", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区政府党组成员、副区长", "北京市平谷区人民政府",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzf/"),

    ("pinggu_yin_shuangfeng", "尹双凤", "女", "汉族", "未知", "未知", "未知", "未知", "未知",
     "区政府副区长（挂职）", "北京市平谷区人民政府",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzf/"),

    ("pinggu_gao_hongbin", "高宏斌", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区政府党组成员、副区长（挂职）", "北京市平谷区人民政府",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzf/"),

    # ════════════════════════════════════════════════════════════
    # 区人大 — District People's Congress
    # ════════════════════════════════════════════════════════════

    ("pinggu_liu_zhen", "刘震", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区人大常委会党组书记、主任", "北京市平谷区人民代表大会常务委员会",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qrd/"),

    ("pinggu_fu_xiangsheng", "付湘生", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区人大常委会党组副书记、副主任，兼区总工会主席", "北京市平谷区人民代表大会常务委员会",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qrd/"),

    ("pinggu_hu_baowang", "胡宝旺", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区人大常委会党组成员、副主任", "北京市平谷区人民代表大会常务委员会",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qrd/"),

    ("pinggu_ma_liwen", "马立文", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区人大常委会党组成员、副主任", "北京市平谷区人民代表大会常务委员会",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qrd/"),

    ("pinggu_shen_lijun", "沈立军", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区人大常委会党组成员、副主任", "北京市平谷区人民代表大会常务委员会",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qrd/"),

    ("pinggu_ma_yulan", "马玉兰", "女", "汉族", "未知", "未知", "未知", "未知", "未知",
     "区人大常委会副主任（不驻会）、区投资促进服务中心主任", "北京市平谷区投资促进服务中心",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qrd/"),

    # ════════════════════════════════════════════════════════════
    # 区政协 — District CPPCC
    # ════════════════════════════════════════════════════════════

    ("pinggu_zhang_xiaofeng", "张晓峰", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区政协党组书记、主席", "中国人民政治协商会议北京市平谷区委员会",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzx/"),

    ("pinggu_cui_chengli", "崔成立", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区政协党组成员、副主席", "中国人民政治协商会议北京市平谷区委员会",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzx/"),

    ("pinggu_yang_heqing", "杨河清", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区政协党组成员、副主席", "中国人民政治协商会议北京市平谷区委员会",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzx/"),

    ("pinggu_liu_pinghua", "刘平华", "男", "汉族", "未知", "未知", "未知", "民革会员", "未知",
     "区政协副主席（不驻会）、民革北京市委秘书长", "民革北京市委",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzx/"),

    ("pinggu_luo_kun", "罗焜", "男", "汉族", "未知", "未知", "未知", "九三学社社员", "未知",
     "区政协副主席（不驻会）、区卫生健康委主任", "北京市平谷区卫生健康委员会",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzx/"),

    ("pinggu_hu_huanyu", "胡桓宇", "男", "汉族", "未知", "未知", "未知", "未知", "未知",
     "区政协副主席（不驻会）、区工商联主席", "北京市平谷区工商业联合会",
     "bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzx/"),
]

# Note: 平谷区 as a Beijing district has unique rank conventions.
# The district party secretary and district mayor hold 副部级 (sub-provincial) rank.
# Standing committee members and deputy mayors hold 正局级/副局级.
ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("pinggu_party_committee", "中共北京市平谷区委员会", "党委", "副部级", "中共北京市委", "北京市平谷区"),
    ("pinggu_gov", "北京市平谷区人民政府", "政府", "副部级", "北京市人民政府", "北京市平谷区"),
    ("pinggu_discipline", "中共北京市平谷区纪律检查委员会", "纪委", "副部级", "北京市纪委", "北京市平谷区"),
    ("pinggu_party_school", "中共北京市平谷区委党校", "事业单位", "正处级", "平谷区委", "北京市平谷区"),
    ("pinggu_org_department", "中共北京市平谷区委组织部", "党委部门", "正处级", "平谷区委", "北京市平谷区"),
    ("pinggu_propaganda", "中共北京市平谷区委宣传部", "党委部门", "正处级", "平谷区委", "北京市平谷区"),
    ("pinggu_united_front", "中共北京市平谷区委统战部", "党委部门", "正处级", "平谷区委", "北京市平谷区"),
    ("pinggu_political_legal", "中共北京市平谷区委政法委员会", "党委部门", "正处级", "平谷区委", "北京市平谷区"),
    ("pinggu_armed_forces", "北京市平谷区人民武装部", "军队", "正师级", "北京卫戍区", "北京市平谷区"),
    ("pinggu_public_security", "北京市公安局平谷分局", "公安", "正处级", "北京市公安局", "北京市平谷区"),
    ("pinggu_peoples_congress", "北京市平谷区人民代表大会常务委员会", "人大", "副部级", "北京市人大常委会", "北京市平谷区"),
    ("pinggu_cppcc", "中国人民政治协商会议北京市平谷区委员会", "政协", "副部级", "北京市政协", "北京市平谷区"),
    ("pinggu_investment_promotion", "北京市平谷区投资促进服务中心", "事业单位", "正处级", "平谷区政府", "北京市平谷区"),
    ("pinggu_health_commission", "北京市平谷区卫生健康委员会", "政府组成部门", "正处级", "平谷区政府", "北京市平谷区"),
    ("pinggu_federation_industry", "北京市平谷区工商业联合会", "群团", "正处级", "平谷区委", "北京市平谷区"),
]

# Person → Organization positions
POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ── 狄涛（区委书记）──
    ("pinggu_di_tao", "pinggu_party_committee", "区委书记", "未知", "至今", "副部级", "主持区委全面工作"),

    # ── 李志遂（区长）──
    ("pinggu_li_zhisui", "pinggu_gov", "区长", "未知", "至今", "副部级", "区政府全面工作"),
    ("pinggu_li_zhisui", "pinggu_party_committee", "区委副书记", "未知", "至今", "副部级", ""),
    ("pinggu_li_zhisui", "pinggu_gov", "党组书记", "未知", "至今", "副部级", ""),

    # ── 葛海斌（区委副书记）──
    ("pinggu_ge_haibin", "pinggu_party_committee", "区委副书记", "未知", "至今", "正局级", "兼区委党校校长"),
    ("pinggu_ge_haibin", "pinggu_party_school", "校长（兼）", "未知", "至今", "正局级", ""),

    # ── 高磊（宣传部部长）──
    ("pinggu_gao_lei", "pinggu_party_committee", "区委常委", "未知", "至今", "正局级", ""),
    ("pinggu_gao_lei", "pinggu_propaganda", "宣传部部长", "未知", "至今", "正局级", ""),

    # ── 赵文侃（常务副区长）──
    ("pinggu_zhao_wenkan", "pinggu_party_committee", "区委常委", "未知", "至今", "正局级", ""),
    ("pinggu_zhao_wenkan", "pinggu_gov", "常务副区长", "未知", "至今", "正局级", "党组副书记"),

    # ── 颉换成（副区长）──
    ("pinggu_xie_huancheng", "pinggu_party_committee", "区委常委", "未知", "至今", "正局级", ""),
    ("pinggu_xie_huancheng", "pinggu_gov", "副区长", "未知", "至今", "正局级", "党组成员"),

    # ── 张胜军（组织部部长）──
    ("pinggu_zhang_shengjun", "pinggu_party_committee", "区委常委", "未知", "至今", "正局级", ""),
    ("pinggu_zhang_shengjun", "pinggu_org_department", "组织部部长", "未知", "至今", "正局级", ""),

    # ── 于建波（纪委书记）──
    ("pinggu_yu_jianbo", "pinggu_party_committee", "区委常委", "未知", "至今", "正局级", ""),
    ("pinggu_yu_jianbo", "pinggu_discipline", "区纪委书记/监委主任", "未知", "至今", "正局级", "二级高级监察官"),

    # ── 刘堃（统战部部长）──
    ("pinggu_liu_kun", "pinggu_party_committee", "区委常委", "未知", "至今", "正局级", ""),
    ("pinggu_liu_kun", "pinggu_united_front", "统战部部长", "未知", "至今", "正局级", "兼区政协党组副书记"),

    # ── 李子腾（政法委书记）──
    ("pinggu_li_ziteng", "pinggu_party_committee", "区委常委", "未知", "至今", "正局级", ""),
    ("pinggu_li_ziteng", "pinggu_political_legal", "政法委书记", "未知", "至今", "正局级", ""),

    # ── 周国祥（武装部政委）──
    ("pinggu_zhou_guoxiang", "pinggu_party_committee", "区委常委", "未知", "至今", "正师级", ""),
    ("pinggu_zhou_guoxiang", "pinggu_armed_forces", "政治委员", "未知", "至今", "正师级", ""),

    # ── 区政府副区长 ──
    ("pinggu_zang_xuemin", "pinggu_gov", "副区长", "未知", "至今", "正局级", "党组成员"),
    ("pinggu_zang_xuemin", "pinggu_public_security", "党委书记、局长", "未知", "至今", "正处级", ""),

    ("pinggu_ma_dongmei", "pinggu_gov", "副区长", "未知", "至今", "正局级", "党组成员"),

    ("pinggu_fu_qiang", "pinggu_gov", "副区长", "未知", "至今", "正局级", "党组成员"),

    ("pinggu_peng_shi", "pinggu_gov", "副区长", "未知", "至今", "正局级", "党组成员"),

    ("pinggu_yin_shuangfeng", "pinggu_gov", "副区长（挂职）", "未知", "至今", "正局级", ""),

    ("pinggu_gao_hongbin", "pinggu_gov", "副区长（挂职）", "未知", "至今", "正局级", "党组成员"),

    # ── 人大 ──
    ("pinggu_liu_zhen", "pinggu_peoples_congress", "主任", "未知", "至今", "副部级", "党组书记"),
    ("pinggu_fu_xiangsheng", "pinggu_peoples_congress", "副主任", "未知", "至今", "正局级", "党组副书记，兼区总工会主席"),
    ("pinggu_hu_baowang", "pinggu_peoples_congress", "副主任", "未知", "至今", "正局级", "党组成员"),
    ("pinggu_ma_liwen", "pinggu_peoples_congress", "副主任", "未知", "至今", "正局级", "党组成员"),
    ("pinggu_shen_lijun", "pinggu_peoples_congress", "副主任", "未知", "至今", "正局级", "党组成员"),
    ("pinggu_ma_yulan", "pinggu_peoples_congress", "副主任（不驻会）", "未知", "至今", "正局级", "区投资促进服务中心主任"),

    # ── 政协 ──
    ("pinggu_zhang_xiaofeng", "pinggu_cppcc", "主席", "未知", "至今", "副部级", "党组书记"),
    ("pinggu_cui_chengli", "pinggu_cppcc", "副主席", "未知", "至今", "正局级", "党组成员"),
    ("pinggu_yang_heqing", "pinggu_cppcc", "副主席", "未知", "至今", "正局级", "党组成员"),
    ("pinggu_liu_pinghua", "pinggu_cppcc", "副主席（不驻会）", "未知", "至今", "正局级", "民革北京市委秘书长"),
    ("pinggu_luo_kun", "pinggu_cppcc", "副主席（不驻会）", "未知", "至今", "正局级", "区卫生健康委主任"),
    ("pinggu_hu_huanyu", "pinggu_cppcc", "副主席（不驻会）", "未知", "至今", "正局级", "区工商联主席"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # Top leadership dyads
    ("pinggu_di_tao", "pinggu_li_zhisui", "superior_subordinate",
     "区委书记→区长，党政一把手搭档", "中共北京市平谷区委/平谷区政府", "至今"),

    # Party Secretary → Standing Committee
    ("pinggu_di_tao", "pinggu_ge_haibin", "superior_subordinate",
     "区委书记→区委副书记", "中共北京市平谷区委", "至今"),

    ("pinggu_di_tao", "pinggu_gao_lei", "superior_subordinate",
     "区委书记→宣传部部长", "中共北京市平谷区委", "至今"),

    ("pinggu_di_tao", "pinggu_zhao_wenkan", "superior_subordinate",
     "区委书记→常务副区长", "中共北京市平谷区委/平谷区政府", "至今"),

    ("pinggu_di_tao", "pinggu_xie_huancheng", "superior_subordinate",
     "区委书记→副区长", "中共北京市平谷区委/平谷区政府", "至今"),

    ("pinggu_di_tao", "pinggu_zhang_shengjun", "superior_subordinate",
     "区委书记→组织部部长", "中共北京市平谷区委", "至今"),

    ("pinggu_di_tao", "pinggu_yu_jianbo", "superior_subordinate",
     "区委书记→纪委书记", "中共北京市平谷区委/区纪委", "至今"),

    ("pinggu_di_tao", "pinggu_liu_kun", "superior_subordinate",
     "区委书记→统战部部长", "中共北京市平谷区委", "至今"),

    ("pinggu_di_tao", "pinggu_li_ziteng", "superior_subordinate",
     "区委书记→政法委书记", "中共北京市平谷区委", "至今"),

    ("pinggu_di_tao", "pinggu_zhou_guoxiang", "superior_subordinate",
     "区委书记→武装部政委", "中共北京市平谷区委/区人武部", "至今"),

    # District Mayor → Deputy Mayors
    ("pinggu_li_zhisui", "pinggu_zhao_wenkan", "superior_subordinate",
     "区长→常务副区长", "平谷区政府", "至今"),

    ("pinggu_li_zhisui", "pinggu_xie_huancheng", "superior_subordinate",
     "区长→副区长", "平谷区政府", "至今"),

    ("pinggu_li_zhisui", "pinggu_zang_xuemin", "superior_subordinate",
     "区长→副区长/公安分局局长", "平谷区政府/公安局平谷分局", "至今"),

    ("pinggu_li_zhisui", "pinggu_ma_dongmei", "superior_subordinate",
     "区长→副区长", "平谷区政府", "至今"),

    ("pinggu_li_zhisui", "pinggu_fu_qiang", "superior_subordinate",
     "区长→副区长", "平谷区政府", "至今"),

    ("pinggu_li_zhisui", "pinggu_peng_shi", "superior_subordinate",
     "区长→副区长", "平谷区政府", "至今"),

    # Deputy Party Secretary → Standing Committee cross-connections
    ("pinggu_ge_haibin", "pinggu_zhang_shengjun", "overlap",
     "区委副书记和组织部长，干部工作层面的密切协作", "中共北京市平谷区委", "至今"),

    ("pinggu_zhao_wenkan", "pinggu_xie_huancheng", "overlap",
     "常务副区长和副区长，区政府日常工作搭档", "平谷区政府", "至今"),

    # 于建波 (discipline) → cross-cutting oversight
    ("pinggu_yu_jianbo", "pinggu_zhang_shengjun", "overlap",
     "纪委书记和组织部长，干部监督与任用工作的交叉领域", "中共北京市平谷区委", "至今"),
]


# ════════════════════════════════════════════════════════════
# SQLITE BUILD
# ════════════════════════════════════════════════════════════

def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
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
        );
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)", pos)
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"✓ Database created: {DB_PATH}")


# ════════════════════════════════════════════════════════════
# GEXF BUILD
# ════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(name):
    """Return 'r,g,b' color string based on role."""
    for p in PERSONS:
        if p[0] == name:
            post = (p[9] or "")
            if "书记" in post and "副书记" not in post:
                return "255,50,50"  # Red for Party Secretary
            if "区长" in post or "副区长" in post or "市长" in post or "副县长" in post:
                return "50,100,255"  # Blue for government
            if "纪委" in post or "监委" in post:
                return "255,165,0"  # Orange for discipline
            return "100,100,100"  # Grey for others
    return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "党委部门": "255,200,200",
        "政府": "200,200,255",
        "政府组成部门": "200,200,255",
        "公安": "200,200,255",
        "纪委": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "军队": "200,200,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(person_id):
    leaders = {"pinggu_di_tao", "pinggu_li_zhisui"}
    return person_id in leaders

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>北京市平谷区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        post = p[9] or ""
        col = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        lines.append(f'      <node id="{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{col.split(",")[0]}" g="{col.split(",")[1]}" b="{col.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        col = org_color(otype)
        lines.append(f'      <node id="{esc(oid)}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{col.split(",")[0]}" g="{col.split(",")[1]}" b="{col.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in POSITIONS:
        eid += 1
        pid = pos[0]
        oid = pos[1]
        title = pos[2] or ""
        lines.append(f'      <edge id="{eid}" source="{esc(pid)}" target="{esc(oid)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        eid += 1
        a, b, rtype, ctx = r[0], r[1], r[3], r[4]
        lines.append(f'      <edge id="{eid}" source="{esc(a)}" target="{esc(b)}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ GEXF graph created: {GEXF_PATH}")


# ════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    build_database()
    build_gexf()

    # Summary
    print(f"\nSummary:")
    print(f"  Persons: {len(PERSONS)}")
    print(f"  Organizations: {len(ORGANIZATIONS)}")
    print(f"  Positions: {len(POSITIONS)}")
    print(f"  Relationships: {len(RELATIONSHIPS)}")
    print(f"\nGenerated files:")
    print(f"  {DB_PATH}")
    print(f"  {GEXF_PATH}")
