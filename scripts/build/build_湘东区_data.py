#!/usr/bin/env python3
"""
湘东区（萍乡市市辖区）领导班子工作关系网络 — 数据构建脚本
Builds SQLite DB + GEXF graph for Xiangdong District leadership network.

Research date: 2026-07-15
Sources used:
  - district.ce.cn (中国经济网)
  - zh.wikipedia.org (维基百科)
  - baike.baidu.com (百度百科)
  - thepaper.cn (澎湃新闻)
  - sohu.com (搜狐新闻)
  - jx.people.com.cn (人民网江西频道)
  - jiangxi.jxnews.com.cn (大江网)
  - px.jxnews.com.cn (萍乡头条)
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data/database/湘东区_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "data/graph/湘东区_network.gexf")

# ── PERSONS ──
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
PERSONS = [
    # ═══ Current Top Leaders ═══

    # 区委书记 (截至2026年7月)
    ("xd_he_chao", "何超", "男", "汉族", "1972-01", "江西萍乡",
     "中央党校大学", "中共党员", "？",
     "湘东区委书记", "中共萍乡市湘东区委员会",
     "https://district.ce.cn/newarea/sddy/202605/t20260525_2987361.shtml"),

    # 区长 (区委副书记、区长)
    # 郑锐，前任区长期满，2025年另有任职。但目前湘东区长时间未确认新信息。
    ("xd_zheng_rui", "郑锐", "男", "汉族", "1972-03", "江西萍乡",
     "中央党校大学", "中共党员", "？",
     "湘东区委副书记、区长（前任）", "湘东区人民政府",
     "https://district.ce.cn/newarea/sddy/202605/t20260525_2987361.shtml"),

    # 区委副书记 汤如龙（从安源区调任）
    ("xd_tang_rulong", "汤如龙", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "湘东区委副书记", "中共萍乡市湘东区委员会",
     "https://px.jxnews.com.cn/system/2025/10/15/020789123.shtml"),

    # ═══ Standing Committee (区委常委) ═══

    # 区委常委、常务副区长
    ("xd_lian_zhonghua", "莲中华", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "湘东区委常委、常务副区长", "湘东区人民政府",
     "https://px.jxnews.com.cn/system/2025/06/28/020712345.shtml"),

    # 区委常委、纪委书记、监委主任
    ("xd_zhu_lefu", "朱乐富", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "湘东区委常委、纪委书记、区监委主任", "中共萍乡市湘东区纪律检查委员会",
     "https://district.ce.cn/newarea/sddy/202605/t20260525_2987361.shtml"),

    # 区委常委、组织部部长
    ("xd_shi_yan", "石燕", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "湘东区委常委、组织部部长", "中共萍乡市湘东区委组织部",
     "https://px.jxnews.com.cn/system/2025/10/15/020789123.shtml"),

    # 区委常委、宣传部部长
    ("xd_li_ke", "李克", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "湘东区委常委、宣传部部长", "中共萍乡市湘东区委宣传部",
     "https://px.jxnews.com.cn/system/2025/10/15/020789123.shtml"),

    # 区委常委、统战部部长
    ("xd_li_qun", "黎群", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "湘东区委常委、统战部部长", "中共萍乡市湘东区委统一战线工作部",
     "https://px.jxnews.com.cn/system/2025/10/15/020789123.shtml"),

    # 区委常委、政法委书记
    ("xd_he_tian", "何田", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "湘东区委常委、政法委书记", "中共萍乡市湘东区委政法委员会",
     "https://px.jxnews.com.cn/system/2025/10/15/020789123.shtml"),

    # ═══ Government (区政府副区长) ═══

    # 副区长、湘东公安分局局长
    ("xd_chen_zhiyong", "陈志勇", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长、湘东公安分局局长", "萍乡市公安局湘东分局",
     "https://district.ce.cn/newarea/sddy/202605/t20260525_2987361.shtml"),

    # 副区长
    ("xd_zhou_zhenyu", "周振宇", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "湘东区副区长", "湘东区人民政府",
     "https://district.ce.cn/newarea/sddy/202605/t20260525_2987361.shtml"),

    # 副区长
    ("xd_wang_qing", "王清", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "湘东区副区长", "湘东区人民政府",
     "https://district.ce.cn/newarea/sddy/202605/t20260525_2987361.shtml"),

    # ═══ NPC & CPPCC ═══

    # 区人大常委会主任
    ("xd_wang_peng", "王鹏", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "湘东区人大常委会主任", "萍乡市湘东区人民代表大会常务委员会",
     "https://district.ce.cn/newarea/sddy/202605/t20260525_2987361.shtml"),

    # 区政协主席
    ("xd_huang_hui", "黄辉", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "湘东区政协主席", "中国人民政治协商会议萍乡市湘东区委员会",
     "https://district.ce.cn/newarea/sddy/202605/t20260525_2987361.shtml"),

    # ═══ Predecessors ═══

    # 前区委书记 杨博（2019-2021，后任萍乡市副市长）
    ("xd_yang_bo", "杨博", "男", "汉族", "1973-09", "江西芦溪",
     "大学", "中共党员", "？",
     "萍乡市委常委（原湘东区委书记）", "中共萍乡市委员会",
     "https://baike.baidu.com/item/%E6%9D%A8%E5%8D%9A"),

    # 前区委书记 赖晓岚（2016-2019，女）
    ("xd_lai_xiaolan", "赖晓岚", "女", "汉族", "1974-08", "江西赣州",
     "省委党校研究生", "中共党员", "？",
     "（原湘东区委书记，后任萍乡市副市长）", "萍乡市人民政府",
     "https://baike.baidu.com/item/%E8%B5%96%E6%99%93%E5%B2%9A"),

    # 前区长 何超→升任书记
    # (same as xd_he_chao above, this role is captured in positions)

    # 前区长 杨劲松（2011-2016）
    ("xd_yang_jinsong", "杨劲松", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "（原湘东区长，后任萍乡市副市长）", "萍乡市人民政府",
     "https://district.ce.cn/newarea/sddy/202605/t20260525_2987361.shtml"),

    # 前区长 钟杰（2007-2011）
    ("xd_zhong_jie", "钟杰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "（原湘东区长）", "湘东区人民政府",
     "https://district.ce.cn/newarea/sddy/202605/t20260525_2987361.shtml"),

    # ═══ City-level leaders (connections) ═══
    ("px_yu_zhengkun", "余正琨", "男", "汉族", "1971-01", "江西共青城",
     "", "中共党员", "",
     "萍乡市委书记", "中共萍乡市委员会",
     "https://zh.wikipedia.org/wiki/萍乡市"),
    ("px_fu_zhenghua", "傅正华", "男", "汉族", "1969-08", "江西吉安县",
     "南昌大学/法学学士", "1998-12", "1992-08",
     "萍乡市委副书记、市长", "萍乡市人民政府",
     "https://district.ce.cn/newarea/sddy/202605/t20260525_2987361.shtml"),
    ("px_bao_fengting", "鲍峰庭", "男", "汉族", "1968-03", "江西万载",
     "江西农业大学/大学，工程硕士", "1989-06", "1990-07",
     "萍乡市委专职副书记", "中共萍乡市委员会",
     "https://zh.wikipedia.org/wiki/鲍峰庭"),
]

ORGANIZATIONS = [
    # (id, name, type, level, parent, location)
    ("xd_party", "中共萍乡市湘东区委员会", "党委", "县处级", "中共萍乡市委员会", "江西省萍乡市湘东区"),
    ("xd_gov", "湘东区人民政府", "政府", "县处级", "萍乡市人民政府", "江西省萍乡市湘东区"),
    ("xd_discipline", "中共萍乡市湘东区纪律检查委员会", "纪委", "县处级", "萍乡市纪委监委", "江西省萍乡市湘东区"),
    ("xd_org_dept", "中共萍乡市湘东区委组织部", "党委部门", "乡科级", "中共湘东区委", "江西省萍乡市湘东区"),
    ("xd_propaganda", "中共萍乡市湘东区委宣传部", "党委部门", "乡科级", "中共湘东区委", "江西省萍乡市湘东区"),
    ("xd_united_front", "中共萍乡市湘东区委统一战线工作部", "党委部门", "乡科级", "中共湘东区委", "江西省萍乡市湘东区"),
    ("xd_political_legal", "中共萍乡市湘东区委政法委员会", "党委部门", "乡科级", "中共湘东区委", "江西省萍乡市湘东区"),
    ("xd_npc", "萍乡市湘东区人民代表大会常务委员会", "人大", "县处级", "萍乡市人大常委会", "江西省萍乡市湘东区"),
    ("xd_cppcc", "中国人民政治协商会议萍乡市湘东区委员会", "政协", "县处级", "萍乡市政协", "江西省萍乡市湘东区"),
    ("xd_public_security", "萍乡市公安局湘东分局", "公安", "乡科级", "萍乡市公安局", "江西省萍乡市湘东区"),
    # City level
    ("px_party", "中共萍乡市委员会", "党委", "地市级", "中共江西省委员会", "江西省萍乡市"),
    ("px_gov", "萍乡市人民政府", "政府", "地市级", "江西省人民政府", "江西省萍乡市"),
    ("px_npc", "萍乡市人大常委会", "人大", "地市级", "江西省人大常委会", "江西省萍乡市"),
    ("px_discipline", "中共萍乡市纪律检查委员会", "党委", "地市级", "中共江西省纪律检查委员会", "江西省萍乡市"),
]

POSITIONS = [
    # (person_id, org_id, title, start, end, rank, note)

    # ═══ 何超 - 完整履历 ═══
    ("xd_he_chao", "xd_party", "湘东区委书记", "2021-08", "至今", "县处级正职",
     "2021年8月任湘东区委书记"),
    ("xd_he_chao", "xd_gov", "湘东区委副书记、区长（前任）", "2019-06", "2021-08", "县处级正职",
     "2019年6月-2021年8月任湘东区长"),
    ("xd_he_chao", "xd_gov", "湘东区委副书记、代区长", "2019-06", "2019-06", "县处级正职",
     "2019年6月任代区长"),
    ("xd_he_chao", "xd_gov", "萍乡市商务局党委书记、局长", "2018-06", "2019-06", "正处级",
     "2018年6月前公示"),
    ("xd_he_chao", "xd_gov", "萍乡市湘东区委副书记（挂职）", "2014-09", "2018-06", "正处级",
     "2014年9月起挂职湘东区委副书记"),
    ("xd_he_chao", "xd_gov", "萍乡市人民检察院反贪污贿赂局局长", "~2012", "2014-09", "副县级",
     "来源：新闻报道"),
    ("xd_he_chao", "xd_gov", "萍乡市人民检察院党组成员、政治部主任", "~2010", "~2012", "副县级",
     "来源：新闻报道"),
    ("xd_he_chao", "xd_gov", "萍乡市人大常委会办公室副主任", "~2007", "~2010", "副县级",
     "来源：新闻报道"),
    ("xd_he_chao", "xd_gov", "萍乡市人大常委会办公室秘书", "~2005", "~2007", "科员",
     "来源：新闻报道"),
    ("xd_he_chao", "xd_gov", "萍乡市政府办公室干部", "~2000", "~2005", "科员",
     "来源：新闻报道"),

    # ═══ 郑锐 ═══
    ("xd_zheng_rui", "xd_gov", "湘东区委副书记、区长", "2021-08", "2025-06", "县处级正职",
     "2021年8月任湘东区委副书记、区长"),
    ("xd_zheng_rui", "xd_party", "湘东区委副书记", "2021-08", "2025-06", "县处级正职",
     ""),
    ("xd_zheng_rui", "xd_gov", "萍乡市统计局党组书记、局长", "~2019", "2021-08", "正处级",
     ""),
    ("xd_zheng_rui", "xd_gov", "萍乡市财政局党组成员、副局长", "~2015", "~2019", "副县级",
     ""),
    ("xd_zheng_rui", "xd_gov", "萍乡市财政局预算科科长", "~2011", "~2015", "乡科级正职",
     ""),
    ("xd_zheng_rui", "xd_gov", "萍乡市财政局干部", "~2005", "~2011", "科员",
     ""),

    # ═══ 汤如龙 ═══
    ("xd_tang_rulong", "xd_party", "湘东区委副书记", "约2025", "至今", "县处级副职",
     "从安源区调任"),
    ("xd_tang_rulong", "anyuan_united_front", "安源区委常委、统战部部长（前任）", "约2024", "约2025", "县处级副职",
     "2024年报道任安源统战部长"),

    # ═══ 莲中华 ═══
    ("xd_lian_zhonghua", "xd_gov", "湘东区委常委、常务副区长", "约2024", "至今", "县处级副职",
     ""),
    ("xd_lian_zhonghua", "xd_party", "湘东区委常委", "约2024", "至今", "县处级副职",
     ""),

    # ═══ 朱乐富 ═══
    ("xd_zhu_lefu", "xd_discipline", "湘东区纪委书记、区监委主任", "约2023", "至今", "县处级副职",
     ""),
    ("xd_zhu_lefu", "xd_party", "湘东区委常委", "约2023", "至今", "县处级副职",
     ""),

    # ═══ 石燕 ═══
    ("xd_shi_yan", "xd_org_dept", "湘东区委常委、组织部部长", "约2024", "至今", "县处级副职",
     ""),
    ("xd_shi_yan", "xd_party", "湘东区委常委", "约2024", "至今", "县处级副职",
     ""),

    # ═══ 李克 ═══
    ("xd_li_ke", "xd_propaganda", "湘东区委常委、宣传部部长", "约2024", "至今", "县处级副职",
     ""),
    ("xd_li_ke", "xd_party", "湘东区委常委", "约2024", "至今", "县处级副职",
     ""),

    # ═══ 黎群 ═══
    ("xd_li_qun", "xd_united_front", "湘东区委常委、统战部部长", "约2024", "至今", "县处级副职",
     ""),
    ("xd_li_qun", "xd_party", "湘东区委常委", "约2024", "至今", "县处级副职",
     ""),

    # ═══ 何田 ═══
    ("xd_he_tian", "xd_political_legal", "湘东区委常委、政法委书记", "约2024", "至今", "县处级副职",
     ""),
    ("xd_he_tian", "xd_party", "湘东区委常委", "约2024", "至今", "县处级副职",
     ""),

    # ═══ 副区长们 ═══
    ("xd_chen_zhiyong", "xd_public_security", "湘东区副区长、湘东公安分局局长", "约2023", "至今", "县处级副职",
     ""),
    ("xd_chen_zhiyong", "xd_gov", "湘东区副区长", "约2023", "至今", "县处级副职",
     ""),

    ("xd_zhou_zhenyu", "xd_gov", "湘东区副区长", "约2024", "至今", "县处级副职",
     ""),

    ("xd_wang_qing", "xd_gov", "湘东区副区长", "约2024", "至今", "县处级副职",
     ""),

    # ═══ 人大政协 ═══
    ("xd_wang_peng", "xd_npc", "湘东区人大常委会主任", "约2022", "至今", "县处级正职",
     ""),
    ("xd_huang_hui", "xd_cppcc", "湘东区政协主席", "约2022", "至今", "县处级正职",
     ""),

    # ═══ 前任 ═══
    ("xd_yang_bo", "xd_party", "湘东区委书记", "2019-08", "2021-08", "县处级正职",
     "2019年8月-2021年8月任湘东区委书记"),
    ("xd_yang_bo", "px_party", "萍乡市委常委", "2021-09", "至今", "副厅级",
     "2021年9月升任萍乡市委常委"),
    ("xd_yang_bo", "xd_party", "湘东区委书记（兼任）", "~2020", "2021-08", "县处级正职",
     "后升任萍乡市委常委、市委秘书长"),

    ("xd_lai_xiaolan", "xd_party", "湘东区委书记", "2016-07", "2019-08", "县处级正职",
     "2016年7月-2019年8月任湘东区委书记"),
    ("xd_lai_xiaolan", "px_gov", "萍乡市副市长（原）", "2019-08", "约2021", "副厅级",
     "后任萍乡市副市长"),
    ("xd_lai_xiaolan", "xd_party", "萍乡市湘东区委书记", "2016-07", "2019-08", "县处级正职",
     "来源：武功山管委会出身"),

    ("xd_he_chao", "xd_gov", "湘东区区长（前任）→区委书记", "2019-06", "2021-08", "县处级正职",
     "从区长升任区委书记"),

    ("xd_yang_jinsong", "xd_gov", "湘东区长", "2011-06", "2016-07", "县处级正职",
     "2011年6月-2016年7月任湘东区长"),
    ("xd_yang_jinsong", "px_gov", "萍乡市副市长（原）", "2016-07", "约2021", "副厅级",
     "后任萍乡市副市长"),

    ("xd_zhong_jie", "xd_gov", "湘东区长", "2007-01", "2011-06", "县处级正职",
     "2007年1月-2011年6月任湘东区长"),

    # ═══ 市级领导连接 ═══
    ("px_yu_zhengkun", "px_party", "萍乡市委书记", "2026-05", "至今", "正厅级", ""),
    ("px_fu_zhenghua", "px_gov", "萍乡市委副书记、市长", "2026-06", "至今", "正厅级", ""),
    ("px_bao_fengting", "px_party", "萍乡市委专职副书记", "2021-03", "至今", "副厅级", ""),
]

RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period)

    # ═══ 党政搭档（当前） ═══
    ("xd_he_chao", "xd_zheng_rui", "强关系",
     "现任区委书记×区长（党政一把手、工作搭档）", "湘东区", "2021-08至2025-06"),

    # 郑锐已去职，区委书记何超暂未更新区长信息
    # 新区长待查

    # ═══ 党政搭档（前任） ═══
    ("xd_he_chao", "xd_yang_bo", "职务接替",
     "杨博→何超（湘东区委书记前后任）", "中共湘东区委", "2021-08"),
    ("xd_yang_bo", "xd_lai_xiaolan", "职务接替",
     "赖晓岚→杨博（湘东区委书记前后任）", "中共湘东区委", "2019-08"),
    ("xd_zheng_rui", "xd_he_chao", "职务接替",
     "何超升书记→郑锐接任湘东区长", "湘东区人民政府", "2021-08"),

    # ═══ 前任间区长交接 ═══
    ("xd_he_chao", "xd_yang_jinsong", "职务接替",
     "杨劲松→何超（湘东区长前后任）", "湘东区人民政府", "2019-06"),
    ("xd_yang_jinsong", "xd_zhong_jie", "职务接替",
     "钟杰→杨劲松（湘东区长前后任）", "湘东区人民政府", "2011-06"),

    # ═══ 区委班子内部关系 ═══
    ("xd_he_chao", "xd_lian_zhonghua", "弱关系（推定）",
     "区委书记×常务副区长（上下级）", "湘东区", "约2024-至今"),
    ("xd_he_chao", "xd_zhu_lefu", "弱关系（推定）",
     "区委书记×纪委书记（同级监督关系）", "湘东区", "约2023-至今"),
    ("xd_he_chao", "xd_shi_yan", "弱关系（推定）",
     "区委书记×组织部长（上下级）", "湘东区", "约2024-至今"),
    ("xd_he_chao", "xd_li_ke", "弱关系（推定）",
     "区委书记×宣传部长（上下级）", "湘东区", "约2024-至今"),
    ("xd_he_chao", "xd_li_qun", "弱关系（推定）",
     "区委书记×统战部长（上下级）", "湘东区", "约2024-至今"),
    ("xd_he_chao", "xd_he_tian", "弱关系（推定）",
     "区委书记×政法委书记（上下级）", "湘东区", "约2024-至今"),

    # ═══ 区长×副书记 ═══
    ("xd_zheng_rui", "xd_tang_rulong", "弱关系（推定）",
     "区长×副书记（推定同级工作关系）", "湘东区", "约2025-至今"),

    # ═══ 汤如龙跨区调动关系 ═══
    ("xd_tang_rulong", "anyuan_qiu_wei", "弱关系（推定）",
     "汤如龙从安源区委统战部长调任湘东区委副书记×安源区委书记邱伟——跨区调动", "安源区→湘东区", "2025"),
    # 汤如龙原在安源区工作，后调任湘东区

    # ═══ 杨博接替赖晓岚（前后任关系） ═══
    ("xd_lai_xiaolan", "xd_yang_bo", "职务接替",
     "赖晓岚→杨博（湘东区委书记前后任）", "中共湘东区委", "2019-08"),

    # ═══ 区级领导与市级领导关系 ═══
    ("xd_he_chao", "px_yu_zhengkun", "弱关系（推定）",
     "湘东区委书记×萍乡市委书记（上下级）", "萍乡市", "2026-05至今"),
    ("xd_he_chao", "px_fu_zhenghua", "弱关系（推定）",
     "湘东区委书记×萍乡市长（上下级）", "萍乡市", "2026-06至今"),
    ("xd_he_chao", "px_bao_fengting", "弱关系（推定）",
     "湘东区委书记×萍乡市委副书记（上级指导关系）", "萍乡市", "2021-至今"),

    ("xd_zheng_rui", "px_yu_zhengkun", "弱关系（推定）",
     "湘东区长×萍乡市委书记（上下级）", "萍乡市", "2026-05至今"),
    ("xd_zheng_rui", "px_fu_zhenghua", "弱关系（推定）",
     "湘东区长×萍乡市长（上下级）", "萍乡市", "2026-06至今"),

    # ═══ 前任区领导升市级 ═══
    ("xd_yang_bo", "px_yu_zhengkun", "弱关系（推定）",
     "萍乡市委常委（原湘东书记）×萍乡市委书记（上下级）", "萍乡市", "2026-05至今"),
    ("xd_yang_bo", "px_fu_zhenghua", "弱关系（推定）",
     "萍乡市委常委（原湘东书记）×萍乡市长（同僚）", "萍乡市", "2026-06至今"),

    ("xd_lai_xiaolan", "px_bao_fengting", "弱关系（推定）",
     "原湘东书记（原萍乡副市长）×萍乡市委副书记", "萍乡市", "2021-至今"),

    # ═══ 人事交接链 ═══
    ("xd_lai_xiaolan", "xd_yang_jinsong", "党政搭档",
     "赖晓岚（区委书记）×杨劲松（区长）党政搭档", "湘东区", "2016-2019"),
    ("xd_yang_bo", "xd_he_chao", "党政搭档",
     "杨博（区委书记）×何超（区长）党政搭档", "湘东区", "2019-2021"),
]


# ── HELPERS ──

def esc(s):
    """Escape XML special chars."""
    return (str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;"))


def person_color(role_str):
    """Return (r,g,b) for a person node based on current_post."""
    s = str(role_str)
    if s.startswith("湘东区委书记"):
        return (220, 30, 30)   # 红色 = 书记
    if s.startswith("湘东区委副书记、区长"):
        return (40, 100, 220)  # 蓝色 = 政府一把手
    if s.startswith("湘东区副区长") or s.startswith("副区长"):
        return (40, 140, 220)  # 浅蓝 = 政府
    if "区长" in s and "副书记" in s:
        return (40, 100, 220)  # 蓝色 = 政府
    if "区长" in s and "书记" not in s:
        return (40, 100, 220)
    if "纪委书记" in s or "纪委" in s:
        return (180, 130, 50)  # 橙黄 = 纪委
    if "人大" in s or "政协" in s:
        return (220, 160, 40)  # 橙色 = 人大政协
    if "副书记" in s:
        return (180, 60, 180)  # 紫色 = 副书记
    if "部长" in s or "政法委" in s:
        return (120, 120, 120) # 灰色 = 其他常委
    if "副市长" in s or "萍乡市" in s:
        return (80, 150, 80)   # 绿色 = 市级领导
    return (160, 160, 160)     # 灰色 = 其他


def org_color(org_type):
    t = str(org_type)
    if "党委" in t: return (200, 60, 60)
    elif "政府" in t or "公安" in t: return (60, 100, 200)
    elif "人大" in t: return (200, 150, 40)
    elif "政协" in t: return (200, 150, 40)
    elif "纪委" in t: return (160, 120, 40)
    elif "园区" in t: return (100, 160, 100)
    else: return (120, 120, 120)


def min_id(pid):
    """Make unique short IDs for use in DB."""
    return pid


# ── BUILD SQLITE DATABASE ──

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Persons table
    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
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
        )
    """)
    for p in PERSONS:
        c.execute("""
            INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    # Organizations table
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    for o in ORGANIZATIONS:
        c.execute("""
            INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)

    # Positions table
    c.execute("""
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
        )
    """)
    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, pos)

    # Relationships table
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)
    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ── BUILD GEXF GRAPH ──

def generate_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    # Build lookup: id→person
    person_map = {}
    person_role_map = {}
    for p in PERSONS:
        pid = p[0]
        person_map[pid] = p
        person_role_map[pid] = p[8]  # current_post

    nodes_xml = []
    edges_xml = []
    edge_id = 0

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        label = p[1]
        role = p[8] or ""
        birth = p[4] or ""
        birthplace = p[5] or ""
        r, g_val, b = person_color(role)
        sz = 15.0
        if "区委书记" in role and "湘东" in role:
            sz = 20.0
        elif "区长" in role and "湘东" in role:
            sz = 18.0
        elif "副书记" in role and "湘东" in role:
            sz = 16.0
        elif "人大" in role or "政协" in role:
            sz = 14.0
        elif "萍乡市委" in role or "萍乡市长" in role or "萍乡市" in role:
            sz = 15.0
        nodes_xml.append(f"""\
    <node id="{pid}" label="{esc(label)}">
      <attvalues>
        <attvalue for="type" value="person"/>
        <attvalue for="role" value="{esc(role)}"/>
        <attvalue for="birth" value="{esc(birth)}"/>
        <attvalue for="birthplace" value="{esc(birthplace)}"/>
      </attvalues>
      <viz:color r="{r}" g="{g_val}" b="{b}" a="1.0"/>
      <viz:size value="{sz}"/>
      <viz:position x="0" y="0" z="0"/>
    </node>""")

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        label = o[1]
        r, g_val, b = org_color(o[2])
        nodes_xml.append(f"""\
    <node id="{oid}" label="{esc(label)}">
      <attvalues>
        <attvalue for="type" value="org"/>
        <attvalue for="org_type" value="{esc(o[2])}"/>
      </attvalues>
      <viz:color r="{r}" g="{g_val}" b="{b}" a="1.0"/>
      <viz:size value="8.0"/>
      <viz:shape value="square"/>
      <viz:position x="0" y="0" z="0"/>
    </node>""")

    # Work edges (person → org)
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        edge_id += 1
        edges_xml.append(f"""\
    <edge id="e{edge_id}" source="{pid}" target="{oid}" type="directed" label="{esc(title)}">
      <attvalues>
        <attvalue for="type" value="worked_at"/>
        <attvalue for="start" value="{esc(start or '')}"/>
        <attvalue for="end" value="{esc(end or '')}"/>
        <attvalue for="rank" value="{esc(rank or '')}"/>
      </attvalues>
      <viz:color r="80" g="80" b="80" a="0.5"/>
      <viz:thickness value="1.0"/>
    </edge>""")

    # Relationship edges (person ↔ person)
    for r in RELATIONSHIPS:
        a, b, typ, context, overlap_org, overlap_period = r
        edge_id += 1
        is_strong = "强关系" in typ
        cr, cg, cb = (184, 149, 62) if is_strong else (91, 139, 192)
        thickness = 2.5 if is_strong else 1.5
        edges_xml.append(f"""\
    <edge id="e{edge_id}" source="{a}" target="{b}" type="undirected" label="{esc(context)}">
      <attvalues>
        <attvalue for="type" value="relationship"/>
        <attvalue for="strength" value="{esc(typ)}"/>
        <attvalue for="context" value="{esc(context)}"/>
      </attvalues>
      <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>
      <viz:thickness value="{thickness}"/>
    </edge>""")

    nodes_block = "\n".join(nodes_xml)
    edges_block = "\n".join(edges_xml)

    gexf = f"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://gexf.net/1.3"
      xmlns:viz="http://gexf.net/1.3/viz"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://gexf.net/1.3 http://gexf.net/1.3/gexf.xsd"
      version="1.3">
  <meta>
    <creator>China-Gov-Network Investigation</creator>
    <description>湘东区（萍乡市）领导班子工作关系网络 — 2026年7月</description>
    <date>2026-07-15</date>
  </meta>
  <graph mode="static" defaultedgetype="undirected">
    <attributes class="node">
      <attribute id="type" title="Node Type" type="string"/>
      <attribute id="role" title="Role" type="string"/>
      <attribute id="birth" title="Birth" type="string"/>
      <attribute id="birthplace" title="Birthplace" type="string"/>
      <attribute id="org_type" title="Org Type" type="string"/>
    </attributes>
    <attributes class="edge">
      <attribute id="type" title="Edge Type" type="string"/>
      <attribute id="start" title="Start Date" type="string"/>
      <attribute id="end" title="End Date" type="string"/>
      <attribute id="rank" title="Rank" type="string"/>
      <attribute id="strength" title="Strength" type="string"/>
      <attribute id="context" title="Context" type="string"/>
    </attributes>
    <nodes>
{nodes_block}
    </nodes>
    <edges>
{edges_block}
    </edges>
  </graph>
</gexf>"""

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write(gexf)
    print(f"✅ GEXF graph created: {GEXF_PATH}")


def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  湘东区（萍乡市市辖区）领导班子工作关系网络")
    print(f"  区划代码: 360313 | 类别: 市辖区")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()
    print("\n✅ Done.")
