#!/usr/bin/env python3
"""
北京市朝阳区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Chaoyang District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 北京市
Targets: 区委书记 & 区长

Sources:
- bjchy.gov.cn/affair/lingdbz/ (official leadership pages, accessed 2026-07-16)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "朝阳区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "朝阳区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ── 区委班子（9人） ──
    ("chaoyang_wu_xiaojie", "吴小杰", "男", "汉族", "1970年12月", "待查",
     "在职研究生/工学学士/工商管理硕士", "中共党员", "待查",
     "区委书记", "中共北京市朝阳区委员会",
     "bjchy.gov.cn/affair/lingdbz/qwld/qwsj/"),

    ("chaoyang_nie_jieying", "聂杰英", "女", "汉族", "1972年7月", "待查",
     "在职研究生/经济学博士", "中共党员", "待查",
     "区委副书记、区长", "北京市朝阳区人民政府",
     "bjchy.gov.cn/affair/lingdbz/qwld/qwfsj/"),

    ("chaoyang_zhao_lingyun", "赵凌云", "女", "汉族", "1971年8月", "待查",
     "市委党校研究生/工学学士", "中共党员", "待查",
     "区委常委、纪委书记、监委主任", "中共北京市朝阳区纪律检查委员会",
     "bjchy.gov.cn/affair/lingdbz/qwld/qwcw/"),

    ("chaoyang_zhao_haidong", "赵海东", "男", "汉族", "1976年3月", "待查",
     "在职研究生/经济学学士/公共管理硕士/管理学硕士", "中共党员", "待查",
     "区委常委、常务副区长", "北京市朝阳区人民政府",
     "bjchy.gov.cn/affair/lingdbz/qwld/qwcw/"),

    ("chaoyang_feng_zhiming", "冯志明", "男", "汉族", "1974年6月", "待查",
     "在职研究生/工学学士/公共管理硕士/法学博士/管理学博士", "中共党员", "待查",
     "区委常委、宣传部部长", "中共北京市朝阳区委宣传部",
     "bjchy.gov.cn/affair/lingdbz/qwld/qwcw/"),

    ("chaoyang_han_xue", "韩雪", "女", "汉族", "1974年11月", "待查",
     "大学/法学学士/公共管理硕士", "中共党员", "待查",
     "区委常委、统战部部长", "中共北京市朝阳区委统战部",
     "bjchy.gov.cn/affair/lingdbz/qwld/qwcw/"),

    ("chaoyang_chen_dapeng", "陈大鹏", "男", "汉族", "1974年8月", "待查",
     "研究生/工学硕士", "中共党员", "待查",
     "区委常委、政法委书记", "中共北京市朝阳区委政法委员会",
     "bjchy.gov.cn/affair/lingdbz/qwld/qwcw/"),

    ("chaoyang_ren_chao", "任超", "男", "汉族", "1974年8月", "待查",
     "研究生/工学硕士", "中共党员", "待查",
     "区委常委、组织部部长", "中共北京市朝阳区委组织部",
     "bjchy.gov.cn/affair/lingdbz/qwld/qwcw/"),

    ("chaoyang_li_fuze", "刘福泽", "男", "满族", "1980年5月", "待查",
     "在职研究生/法学学士/公共管理硕士/管理学博士", "中共党员", "待查",
     "区委常委、副区长", "北京市朝阳区人民政府",
     "bjchy.gov.cn/affair/lingdbz/qwld/qwcw/"),

    ("chaoyang_li_xiaobo", "李晓波", "男", "汉族", "1979年10月", "待查",
     "研究生/军事学硕士", "中共党员", "待查",
     "区委常委、武装部部长", "北京市朝阳区人民武装部",
     "bjchy.gov.cn/affair/lingdbz/qwld/qwcw/"),

    # ── 副区长（除常委外） ──
    ("chaoyang_yin_yuan", "尹圆", "女", "汉族", "1979年4月", "待查",
     "研究生/工学学士/法律硕士", "致公党", "待查",
     "副区长", "北京市朝阳区人民政府",
     "bjchy.gov.cn/affair/lingdbz/qzfld/fqz/"),

    ("chaoyang_bi_bo", "毕波", "男", "汉族", "1970年1月", "待查",
     "市委党校研究生", "中共党员", "待查",
     "副区长、区公安分局局长", "北京市公安局朝阳分局",
     "bjchy.gov.cn/affair/lingdbz/qzfld/fqz/"),

    ("chaoyang_chen_dai", "陈黛", "女", "汉族", "1982年9月", "待查",
     "在职研究生/管理学博士", "中共党员", "待查",
     "副区长", "北京市朝阳区人民政府",
     "bjchy.gov.cn/affair/lingdbz/qzfld/fqz/"),

    ("chaoyang_lou_yixiang", "娄毅翔", "男", "汉族", "1976年3月", "待查",
     "研究生/经济学硕士", "中共党员", "待查",
     "副区长", "北京市朝阳区人民政府",
     "bjchy.gov.cn/affair/lingdbz/qzfld/fqz/"),

    ("chaoyang_hao_baogang", "郝宝刚", "男", "汉族", "1973年12月", "待查",
     "研究生/农学硕士", "中共党员", "待查",
     "副区长", "北京市朝阳区人民政府",
     "bjchy.gov.cn/affair/lingdbz/qzfld/fqz/"),

    ("chaoyang_pan_zejun", "潘泽君", "男", "汉族", "1977年6月", "待查",
     "大学/文学学士/经济学硕士", "中共党员", "待查",
     "副区长（挂职）", "北京市朝阳区人民政府",
     "bjchy.gov.cn/affair/lingdbz/qzfld/fqz/"),

    ("chaoyang_wu_fengwu", "吴凤武", "男", "汉族", "1976年1月", "待查",
     "在职研究生/经济学博士", "中共党员", "待查",
     "副区长（挂职）", "北京市朝阳区人民政府",
     "bjchy.gov.cn/affair/lingdbz/qzfld/fqz/"),

    # ── 人大 ──
    ("chaoyang_wang_xu", "王旭", "男", "汉族", "1969年3月", "待查",
     "市委党校研究生", "中共党员", "待查",
     "区人大常委会主任", "北京市朝阳区人民代表大会常务委员会",
     "bjchy.gov.cn/affair/lingdbz/qrdld/qrdzr/"),

    ("chaoyang_zhang_kebin", "张克斌", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会副主任", "北京市朝阳区人民代表大会常务委员会",
     "bjchy.gov.cn/affair/lingdbz/qrdld/qrdfzr/"),

    ("chaoyang_bao_yuefeng", "宝月凤", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会副主任", "北京市朝阳区人民代表大会常务委员会",
     "bjchy.gov.cn/affair/lingdbz/qrdld/qrdfzr/"),

    ("chaoyang_xu_jianing", "许嘉宁", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会副主任", "北京市朝阳区人民代表大会常务委员会",
     "bjchy.gov.cn/affair/lingdbz/qrdld/qrdfzr/"),

    ("chaoyang_bi_zhongwei", "毕重伟", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会副主任", "北京市朝阳区人民代表大会常务委员会",
     "bjchy.gov.cn/affair/lingdbz/qrdld/qrdfzr/"),

    ("chaoyang_ye_qing", "叶青", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会副主任", "北京市朝阳区人民代表大会常务委员会",
     "bjchy.gov.cn/affair/lingdbz/qrdld/qrdfzr/"),

    # ── 政协 ──
    ("chaoyang_li_guohong", "李国红", "女", "汉族", "1968年9月", "待查",
     "在职研究生/法学硕士", "中共党员", "待查",
     "区政协主席", "中国人民政治协商会议北京市朝阳区委员会",
     "bjchy.gov.cn/affair/lingdbz/qzxld/qzxzx/"),

    ("chaoyang_zhang_yan", "张岩", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协副主席", "中国人民政治协商会议北京市朝阳区委员会",
     "bjchy.gov.cn/affair/lingdbz/qzxld/qzxfzx/"),

    ("chaoyang_li_liang", "李靓", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协副主席", "中国人民政治协商会议北京市朝阳区委员会",
     "bjchy.gov.cn/affair/lingdbz/qzxld/qzxfzx/"),

    ("chaoyang_lian_wensheng", "连文胜", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协副主席", "中国人民政治协商会议北京市朝阳区委员会",
     "bjchy.gov.cn/affair/lingdbz/qzxld/qzxfzx/"),

    ("chaoyang_wang_dongyan", "王冬岩", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协副主席", "中国人民政治协商会议北京市朝阳区委员会",
     "bjchy.gov.cn/affair/lingdbz/qzxld/qzxfzx/"),

    ("chaoyang_wang_qiang", "王强", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协副主席", "中国人民政治协商会议北京市朝阳区委员会",
     "bjchy.gov.cn/affair/lingdbz/qzxld/qzxfzx/"),

    ("chaoyang_liu_cunzhi", "刘存志", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协副主席", "中国人民政治协商会议北京市朝阳区委员会",
     "bjchy.gov.cn/affair/lingdbz/qzxld/qzxfzx/"),

    # ── 前主要领导（已知从公开资料）──
    ("chaoyang_wen_xian", "文献", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前区委书记", "已离任",
     "media:thepaper.cn;baike.baidu.com"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("cy_party_committee", "中共北京市朝阳区委员会", "党委", "地厅级", "中共北京市委", "北京市朝阳区"),
    ("cy_gov", "北京市朝阳区人民政府", "政府", "地厅级", "北京市人民政府", "北京市朝阳区"),
    ("cy_org_department", "中共北京市朝阳区委组织部", "党委部门", "正处级", "朝阳区委", "北京市朝阳区"),
    ("cy_discipline", "中共北京市朝阳区纪律检查委员会", "纪委", "地厅级", "北京市纪委监委", "北京市朝阳区"),
    ("cy_propaganda", "中共北京市朝阳区委宣传部", "党委部门", "正处级", "朝阳区委", "北京市朝阳区"),
    ("cy_united_front", "中共北京市朝阳区委统战部", "党委部门", "正处级", "朝阳区委", "北京市朝阳区"),
    ("cy_political_legal", "中共北京市朝阳区委政法委员会", "党委部门", "正处级", "朝阳区委", "北京市朝阳区"),
    ("cy_party_school", "中共北京市朝阳区委党校", "党委部门", "正处级", "朝阳区委", "北京市朝阳区"),
    ("cy_public_security", "北京市公安局朝阳分局", "公安", "正处级", "北京市公安局", "北京市朝阳区"),
    ("cy_armed_forces", "北京市朝阳区人民武装部", "武装", "正处级", "北京卫戍区", "北京市朝阳区"),
    ("cy_peoples_congress", "北京市朝阳区人民代表大会常务委员会", "人大", "地厅级", "北京市人大常委会", "北京市朝阳区"),
    ("cy_cppcc", "中国人民政治协商会议北京市朝阳区委员会", "政协", "地厅级", "北京市政协", "北京市朝阳区"),
    ("cy_business_zone", "北京商务中心区管委会", "开发区", "正处级", "北京市朝阳区人民政府", "北京市朝阳区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 吴小杰 — 区委书记 ═══
    ("chaoyang_wu_xiaojie", "cy_party_committee", "区委书记", "2022-11", "至今", "正厅级", "主持区委全面工作，官方页面发布日期2022-11-22"),
    # 履历缺口
    ("chaoyang_wu_xiaojie", "cy_org_department", "履历缺口（2022年前约30年职业生涯）", "1992", "2022-11", "未知", "公开资料未记载2022年前具体任职经历"),

    # ═══ 聂杰英 — 区长 ═══
    ("chaoyang_nie_jieying", "cy_gov", "区长", "2025-06", "至今", "正厅级", "区政府党组书记，2025-06-28官方页面发布"),
    ("chaoyang_nie_jieying", "cy_party_committee", "区委副书记", "2025-06", "至今", "正厅级", "兼任"),
    # 履历缺口
    ("chaoyang_nie_jieying", "cy_org_department", "履历缺口（2025年前约30年职业生涯）", "1994", "2025-06", "未知", "公开资料仅记载基本信息，缺任职经历"),

    # ═══ 赵凌云 — 纪委书记 ═══
    ("chaoyang_zhao_lingyun", "cy_discipline", "区委常委、纪委书记、监委主任", "待查", "至今", "副厅级", "纪检监察系统"),
    ("chaoyang_zhao_lingyun", "cy_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),

    # ═══ 赵海东 — 常务副区长 ═══
    ("chaoyang_zhao_haidong", "cy_gov", "常务副区长", "待查", "至今", "副厅级", "区政府党组副书记"),
    ("chaoyang_zhao_haidong", "cy_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),
    ("chaoyang_zhao_haidong", "cy_business_zone", "市委商务中心区工委书记（兼）", "待查", "至今", "副厅级", "兼任"),

    # ═══ 冯志明 — 宣传部长 ═══
    ("chaoyang_feng_zhiming", "cy_propaganda", "区委常委、宣传部部长", "待查", "至今", "副厅级", ""),
    ("chaoyang_feng_zhiming", "cy_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),

    # ═══ 韩雪 — 统战部长 ═══
    ("chaoyang_han_xue", "cy_united_front", "区委常委、统战部部长", "待查", "至今", "副厅级", "兼区政协党组副书记、区社会主义学院院长"),
    ("chaoyang_han_xue", "cy_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),

    # ═══ 陈大鹏 — 政法委书记 ═══
    ("chaoyang_chen_dapeng", "cy_political_legal", "区委常委、政法委书记", "待查", "至今", "副厅级", ""),
    ("chaoyang_chen_dapeng", "cy_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),

    # ═══ 任超 — 组织部长 ═══
    ("chaoyang_ren_chao", "cy_org_department", "区委常委、组织部部长", "待查", "至今", "副厅级", ""),
    ("chaoyang_ren_chao", "cy_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),

    # ═══ 刘福泽 — 副区长（常委） ═══
    ("chaoyang_li_fuze", "cy_gov", "区委常委、副区长", "待查", "至今", "副厅级", "区政府党组成员"),
    ("chaoyang_li_fuze", "cy_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),

    # ═══ 李晓波 — 武装部长 ═══
    ("chaoyang_li_xiaobo", "cy_armed_forces", "区委常委、武装部部长", "待查", "至今", "副厅级", ""),
    ("chaoyang_li_xiaobo", "cy_party_committee", "区委常委", "待查", "至今", "副厅级", "入常"),

    # ═══ 副区长们 ═══
    ("chaoyang_yin_yuan", "cy_gov", "副区长", "待查", "至今", "副厅级", "致公党，分管生态环境/人社/教育/文旅/体育"),
    ("chaoyang_bi_bo", "cy_gov", "副区长、区公安分局局长", "待查", "至今", "副厅级", "区政府党组成员/分管公安/司法/交通"),
    ("chaoyang_bi_bo", "cy_public_security", "公安分局党委书记、局长", "待查", "至今", "正处级", "兼区委政法委副书记"),
    ("chaoyang_chen_dai", "cy_gov", "副区长", "待查", "至今", "副厅级", "区政府党组成员/分管政务服务/卫健/医保/信访"),
    ("chaoyang_lou_yixiang", "cy_gov", "副区长", "待查", "至今", "副厅级", "区政府党组成员/分管科技/市场监管/民政/街道"),
    ("chaoyang_hao_baogang", "cy_gov", "副区长", "待查", "至今", "副厅级", "区政府党组成员/分管农业农村/水务/园林绿化"),
    ("chaoyang_pan_zejun", "cy_gov", "副区长（挂职）", "待查", "至今", "副厅级", "协助刘福泽分管城管/住建/规划"),
    ("chaoyang_wu_fengwu", "cy_gov", "副区长（挂职）", "待查", "至今", "副厅级", "协助赵海东分管发改/国资/财政/金融"),

    # ═══ 人大 ═══
    ("chaoyang_wang_xu", "cy_peoples_congress", "区人大常委会党组书记、主任", "待查", "至今", "正厅级", ""),
    ("chaoyang_zhang_kebin", "cy_peoples_congress", "区人大常委会副主任", "待查", "至今", "副厅级", ""),
    ("chaoyang_bao_yuefeng", "cy_peoples_congress", "区人大常委会副主任", "待查", "至今", "副厅级", ""),
    ("chaoyang_xu_jianing", "cy_peoples_congress", "区人大常委会副主任", "待查", "至今", "副厅级", ""),
    ("chaoyang_bi_zhongwei", "cy_peoples_congress", "区人大常委会副主任", "待查", "至今", "副厅级", ""),
    ("chaoyang_ye_qing", "cy_peoples_congress", "区人大常委会副主任", "待查", "至今", "副厅级", ""),

    # ═══ 政协 ═══
    ("chaoyang_li_guohong", "cy_cppcc", "区政协党组书记、主席", "待查", "至今", "正厅级", ""),
    ("chaoyang_zhang_yan", "cy_cppcc", "区政协副主席", "待查", "至今", "副厅级", ""),
    ("chaoyang_li_liang", "cy_cppcc", "区政协副主席", "待查", "至今", "副厅级", ""),
    ("chaoyang_lian_wensheng", "cy_cppcc", "区政协副主席", "待查", "至今", "副厅级", ""),
    ("chaoyang_wang_dongyan", "cy_cppcc", "区政协副主席", "待查", "至今", "副厅级", ""),
    ("chaoyang_wang_qiang", "cy_cppcc", "区政协副主席", "待查", "至今", "副厅级", ""),
    ("chaoyang_liu_cunzhi", "cy_cppcc", "区政协副主席", "待查", "至今", "副厅级", ""),

    # ═══ 前主要领导 ═══
    ("chaoyang_wen_xian", "cy_party_committee", "区委书记（前任）", "2019", "2022-11", "正厅级", "文献，前任区委书记"),
]

# ── RELATIONSHIPS ──
# person_a, person_b, type, context, overlap_org, overlap_period

RELATIONSHIPS = [
    # 吴小杰 ↔ 聂杰英 — 党政正职搭档
    ("chaoyang_wu_xiaojie", "chaoyang_nie_jieying", "superior_subordinate",
     "区委书记与区长党政正职搭档",
     "中共北京市朝阳区委员会/朝阳区人民政府", "2025-06至今"),

    # 吴小杰 ↔ 赵凌云 — 书记-纪委书记
    ("chaoyang_wu_xiaojie", "chaoyang_zhao_lingyun", "superior_subordinate",
     "区委书记与纪委书记（从严治党主体责任）",
     "中共北京市朝阳区委员会", "待查至今"),

    # 吴小杰 ↔ 赵海东 — 书记-常务副区长
    ("chaoyang_wu_xiaojie", "chaoyang_zhao_haidong", "superior_subordinate",
     "区委书记与常务副区长",
     "中共北京市朝阳区委员会", "待查至今"),

    # 聂杰英 ↔ 赵海东 — 区长-常务副区长
    ("chaoyang_nie_jieying", "chaoyang_zhao_haidong", "superior_subordinate",
     "区长与常务副区长（区政府日常运作）",
     "北京市朝阳区人民政府", "2025-06至今"),

    # 吴小杰 ↔ 任超 — 书记-组织部长
    ("chaoyang_wu_xiaojie", "chaoyang_ren_chao", "superior_subordinate",
     "区委书记与组织部部长（干部管理）",
     "中共北京市朝阳区委员会", "待查至今"),

    # 吴小杰 ↔ 陈大鹏 — 书记-政法委书记
    ("chaoyang_wu_xiaojie", "chaoyang_chen_dapeng", "superior_subordinate",
     "区委书记与政法委书记",
     "中共北京市朝阳区委员会", "待查至今"),

    # 吴小杰 ↔ 冯志明 — 书记-宣传部长
    ("chaoyang_wu_xiaojie", "chaoyang_feng_zhiming", "superior_subordinate",
     "区委书记与宣传部部长",
     "中共北京市朝阳区委员会", "待查至今"),

    # 吴小杰 ↔ 韩雪 — 书记-统战部长
    ("chaoyang_wu_xiaojie", "chaoyang_han_xue", "superior_subordinate",
     "区委书记与统战部部长",
     "中共北京市朝阳区委员会", "待查至今"),

    # 吴小杰 ↔ 刘福泽 — 书记-常委副区长
    ("chaoyang_wu_xiaojie", "chaoyang_li_fuze", "superior_subordinate",
     "区委书记与常委副区长",
     "中共北京市朝阳区委员会", "待查至今"),

    # 聂杰英 ↔ 刘福泽 — 区长-副区长
    ("chaoyang_nie_jieying", "chaoyang_li_fuze", "superior_subordinate",
     "区长与副区长",
     "北京市朝阳区人民政府", "2025-06至今"),

    # 聂杰英 ↔ 毕波 — 区长-公安分局长
    ("chaoyang_nie_jieying", "chaoyang_bi_bo", "superior_subordinate",
     "区长与公安分局局长（安全稳定）",
     "北京市朝阳区人民政府", "2025-06至今"),

    # 陈大鹏 ↔ 毕波 — 政法委书记-公安分局长
    ("chaoyang_chen_dapeng", "chaoyang_bi_bo", "overlap",
     "政法委书记与公安分局局长的政法系统协作",
     "中共北京市朝阳区委政法委员会", "待查至今"),

    # 赵凌云 ↔ 任超 — 纪委书记-组织部长
    ("chaoyang_zhao_lingyun", "chaoyang_ren_chao", "overlap",
     "纪委与组织部在干部监督方面的协作",
     "中共北京市朝阳区委员会", "待查至今"),

    # 赵海东 ↔ 吴凤武 — 常务副区长-挂职副区长
    ("chaoyang_zhao_haidong", "chaoyang_wu_fengwu", "superior_subordinate",
     "常务副区长与挂职副区长的工作协助关系",
     "北京市朝阳区人民政府", "待查至今"),

    # 刘福泽 ↔ 潘泽君 — 副区长-挂职副区长
    ("chaoyang_li_fuze", "chaoyang_pan_zejun", "superior_subordinate",
     "副区长与挂职副区长的工作协助关系",
     "北京市朝阳区人民政府", "待查至今"),

    # 吴小杰 ↔ 文献 — 前后任区委书记
    ("chaoyang_wu_xiaojie", "chaoyang_wen_xian", "predecessor_successor",
     "吴小杰接替文献任朝阳区委书记",
     "中共北京市朝阳区委员会", "2022-11"),
]


# ════════════════════════════════════════════
# DATABASE BUILDER
# ════════════════════════════════════════════

def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons(
        id TEXT PRIMARY KEY,
        name TEXT,
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
    )""")

    c.execute("""CREATE TABLE organizations(
        id TEXT PRIMARY KEY,
        name TEXT,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    )""")

    c.execute("""CREATE TABLE positions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT,
        org_id TEXT,
        title TEXT,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT
    )""")

    c.execute("""CREATE TABLE relationships(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT,
        person_b TEXT,
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT
    )""")

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")


# ════════════════════════════════════════════
# GEXF BUILDER
# ════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(post):
    if "书记" in post and "副" not in post and "副书记" not in post:
        return "255,50,50"
    if "区长" in post and "副" not in post:
        return "50,100,255"
    if "副书记" in post:
        return "255,100,100"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    if "常务副" in post:
        return "50,130,255"
    if "副区长" in post:
        return "100,130,255"
    if "部长" in post or "统战" in post or "组织" in post:
        return "180,100,200"
    if "政法委" in post:
        return "200,150,50"
    if "武装部" in post:
        return "150,150,50"
    if "主任" in post or "人大" in post:
        return "200,255,255"
    if "政协" in post or "主席" in post:
        return "255,240,200"
    if "前" in post:
        return "150,150,150"
    return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "党委部门": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "公安": "200,200,255",
        "武装": "150,150,50",
        "开发区": "200,255,200",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(post):
    post_clean = post.strip()
    if post_clean == "区委书记":
        return True
    if "区长" in post_clean and "副" not in post_clean:
        return True
    return False

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>北京市朝阳区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role_or_type" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="edge_type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid, name, gender, eth, birth, bp, edu, party, work, post, org, src = p
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        if "副书记" in post and "区委副书记" in post:
            sz = "15.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        parts = c.split(",")
        lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid, name, otype, level, parent, loc = o
        c = org_color(otype)
        lines.append(f'      <node id="o{oid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(parent)}"/>')
        lines.append('        </attvalues>')
        parts = c.split(",")
        lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in RELATIONSHIPS:
        pa, pb, rtype, context, overlap_org, overlap_period = r
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] GEXF created: {GEXF_PATH}")


# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    create_database()
    create_gexf()
    print("[DONE] Build complete.")
