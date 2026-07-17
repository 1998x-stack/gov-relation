#!/usr/bin/env python3
"""
莲花县（萍乡市下辖县）领导班子工作关系网络 — 数据构建脚本
Builds SQLite DB + GEXF graph for Lianhua County leadership network.

Research date: 2026-07-15
Sources used:
  - px.jxnews.com.cn (大江网/萍乡头条) - primary source for leadership changes
  - thepaper.cn (澎湃新闻) - leadership roster announcements, appointment articles
  - jx.people.com.cn (人民网江西频道) - interviews and profiles (王东成, 易刚)
  - jx.news.cn (新华网江西频道) - interviews and profiles (曾衍敏, 王东成)
  - cs0799.com (萍乡城事网) - local news
  - baike.baidu.com (百度百科) - biographical data
  - baike.sogou.com (搜狗百科) - biographical data (易刚)
  - newrsc.jaas.ac.cn (江西省农科院) - official visit coverage
  - news.qq.com (腾讯新闻) - 2026 Jiangxi Two Sessions coverage
  - kknews.xyz - 2026 election results (王东成当选县长)
  - jxrd.jxnews.com.cn (江西人大新闻网) - NPC committee updates
  - zgcounty.com (中国县域) - leadership roster
  - jxzx.jxnews.com.cn (江西政协新闻网) - CPPCC updates (汤杰)
  - chinanews.com.cn (中新网) - agricultural bank meeting
  - baike.newton.com.tw - biographical reference (刘海林, 陈礼虎, 刘力亚)
"""

import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data/database/莲花县_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "data/graph/莲花县_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# PERSONS
# Format: (id, name, gender, ethnicity, birth, birthplace,
#          education, party_join, work_start, current_post, current_org, source)
# ═══════════════════════════════════════════════════════════════════════

PERSONS = [
    # ═══ Current Top Leaders (as of mid-2026) ═══

    # 县委书记 易刚（2021年8月任，仍在任）
    ("lh_yi_gang", "易刚", "男", "汉族", "1972-09", "江西芦溪",
     "省委党校研究生学历", "1995-04", "1995-07",
     "莲花县委书记", "中共莲花县委员会",
     "https://baike.sogou.com/v99695938.htm"),

    # 县委副书记、县长 王东成（2026年2月28日当选县长；此前为县委常委、县纪委书记、副县长）
    ("lh_wang_dongcheng", "王东成", "男", "汉族", "1980-02", "待查（江西）",
     "大学本科学历", "中共党员", "待查",
     "莲花县委副书记、县长", "莲花县人民政府",
     "https://kknews.xyz/55259"),

    # 县委副书记（前任县长） 曾衍敏（2021年8月-2026年2月任县长→去向待查）
    ("lh_zeng_yanmin", "曾衍敏", "男", "汉族", "1976-08", "江西铅山",
     "省委党校在职研究生学历", "中共党员", "1996-07",
     "原莲花县委副书记、县长（卸任，去向待查）", "莲花县人民政府",
     "https://m.thepaper.cn/newsDetail_forward_14014658"),

    # 县委副书记、副县长 贺延伟（民政部挂职干部，2023年10月任）
    ("lh_he_yanwei", "贺延伟", "男", "汉族", "1980-12", "山东烟台",
     "研究生学历/理学硕士", "2007-05", "2007-07",
     "莲花县委副书记、副县长（挂职）", "莲花县人民政府",
     "https://baike.baidu.com/item/%E8%B4%BA%E5%BB%B6%E4%BC%9F/63657149"),

    # ═══ Former Leaders (腐败被查) ═══

    # 县委书记（前任） 张运来（2019-2021，2023年被查，被双开）
    ("lh_zhang_yunlai", "张运来", "男", "汉族", "1966-08", "江西上栗",
     "中央党校在职大学学历", "1989-03", "1984-12",
     "原莲花县委书记（被双开）", "中共莲花县委员会",
     "https://m.bjnews.com.cn/detail/167402958314796.html"),

    # 县长（前任） 曾国祥（2019-2021年任县长）
    ("lh_zeng_guoxiang", "曾国祥", "男", "汉族", "1968-09", "江西湘东",
     "工程学硕士", "1997-11", "1992-08",
     "原莲花县委副书记、县长（2021年8月卸任）", "莲花县人民政府",
     "https://upimg.baike.so.com/doc/5369137-24861583.html"),

    # ═══ Standing Committee / 县委常委 ═══

    # 县委常委、常务副县长 陈礼虎（2024年6月辞职，转任武功山管委会）
    ("lh_chen_lihu", "陈礼虎", "男", "汉族", "1980-09", "江西上栗",
     "省委党校在职研究生学历", "中共党员", "待查",
     "武功山风景名胜区党委委员、管委会副主任（原莲花县委常委、常务副县长）", "武功山风景名胜区管委会",
     "https://www.newton.com.tw/wiki/%E9%99%B3%E7%A6%AE%E8%99%8E"),

    # 县委常委、副县长 刘力亚（曾任副县长，后任县委常委）
    ("lh_liu_liya", "刘力亚", "男", "汉族", "1984-04", "江西安源",
     "大学本科学历", "2006-09", "2005-07",
     "莲花县委常委、副县长", "莲花县人民政府",
     "https://www.newton.com.tw/wiki/%E5%8A%89%E5%8A%9B%E4%BA%9E"),

    # 县委常委、副县长（挂职） 王红宙（国家康复辅具研究中心挂职）
    ("lh_wang_hongzhou", "王红宙", "男", "汉族", "1975-09", "山西永济",
     "大学本科学历", "中共党员", "1994-09",
     "莲花县委常委、副县长（挂职）", "莲花县人民政府",
     "https://m.thepaper.cn/newsDetail_forward_14014658"),

    # ═══ County Government Deputy Heads (副县长) ═══

    # 副县长 张琼孟娜
    ("lh_zhangqiong_mengna", "张琼孟娜", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县副县长", "莲花县人民政府",
     "https://zgcounty.com/news/33720.html"),

    # 副县长 刘晓飞
    ("lh_liu_xiaofei", "刘晓飞", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县副县长", "莲花县人民政府",
     "https://zgcounty.com/news/33720.html"),

    # 副县长 文凯
    ("lh_wen_kai", "文凯", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县副县长", "莲花县人民政府",
     "https://zgcounty.com/news/33720.html"),

    # 副县长（挂职） 丁山
    ("lh_ding_shan", "丁山", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县副县长（挂职）", "莲花县人民政府",
     "https://zgcounty.com/news/33720.html"),

    # 副县长（前任→已被接替） 晏辉（2024年1月辞职）
    ("lh_yan_hui", "晏辉", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "原莲花县副县长（2024年1月辞职）", "莲花县人民政府",
     "https://px.jxnews.com.cn/system/2024/01/03/020358547.shtml"),

    # 副县长 刘海丰（2024年1月任）
    ("lh_liu_haifeng", "刘海丰", "男", "汉族", "1978-05", "待查",
     "在职大学学历", "中共党员", "待查",
     "莲花县副县长", "莲花县人民政府",
     "https://px.jxnews.com.cn/system/2024/01/03/020358547.shtml"),

    # 副县长 吴潇雯（提名人选→副县长）
    ("lh_wu_xiaowen", "吴潇雯", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县副县长", "莲花县人民政府",
     "https://zgcounty.com/news/33720.html"),

    # 副县长 汤咏锋
    ("lh_tang_yongfeng", "汤咏锋", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县副县长", "莲花县人民政府",
     "https://px.jxnews.com.cn/system/2024/11/04/020687282.shtml"),

    # 副县长（前任） 郭小彬
    ("lh_guo_xiaobin", "郭小彬", "男", "汉族", "1976-04", "江西莲花",
     "在职大专学历", "中共党员", "1995-08",
     "原莲花县副县长（曾任）", "莲花县人民政府",
     "https://www.thepaper.cn/newsDetail_forward_10711288"),

    # 副县长 戴刚（农工党，非中共）
    ("lh_dai_gang", "戴刚", "男", "汉族", "1984-06", "江西上栗",
     "在职研究生学历", "农工党党员", "2006-07",
     "莲花县副县长", "莲花县人民政府",
     "https://www.thepaper.cn/newsDetail_forward_10711288"),

    # 副县长 刘华平
    ("lh_liu_huaping", "刘华平", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县副县长", "莲花县人民政府",
     "https://baike.baidu.com/item/%E8%8E%B2%E8%8A%B1%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C/59996135"),

    # ═══ 县人大常委会 ═══

    # 县人大常委会主任 刘美兰（2023年补选）
    ("lh_liu_meilan", "刘美兰", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县人大常委会党组书记、主任", "莲花县人大常委会",
     "https://jxrd.jxnews.com.cn/system/2024/09/04/020621986.shtml"),

    # 县人大常委会副主任 李铁湘
    ("lh_li_tiexiang", "李铁湘", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县人大常委会副主任", "莲花县人大常委会",
     "https://px.jxnews.com.cn/system/2024/11/08/020692510.shtml"),

    # 县人大常委会副主任 刘正良（2026年2月补选）
    ("lh_liu_zhengliang", "刘正良", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县人大常委会副主任", "莲花县人大常委会",
     "https://kknews.xyz/55259"),

    # 县人大常委会原主任 朱白明（被查）
    ("lh_zhu_baiming", "朱白明", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "原莲花县人大常委会党组书记、主任（被查）", "莲花县人大常委会",
     "https://www.ctdsb.net/c1716_202302/1657863.html"),

    # ═══ 县政协 ═══

    # 县政协主席 汤杰（2021年接任，接替刘海林）
    ("lh_tang_jie", "汤杰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县政协党组书记、主席", "政协莲花县委员会",
     "https://jxzx.jxnews.com.cn/system/2025/07/01/020917861.shtml"),

    # 县政协原主席 刘海林（2026年被查）
    ("lh_liu_hailin", "刘海林", "男", "汉族", "1964-07", "待查",
     "在职研究生学历（中央党校）", "1985-12", "1983-08",
     "原莲花县政协党组书记、主席（被查）", "政协莲花县委员会",
     "https://www.newton.com.tw/wiki/%E5%8A%89%E6%B5%B7%E6%9E%97/7703689"),

    # 县政协副主席 朱治平
    ("lh_zhu_zhiping", "朱治平", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县政协副主席", "政协莲花县委员会",
     "https://px.jxnews.com.cn/system/2021/11/08/019443916.shtml"),

    # ═══ 县纪委监委 ═══

    # 县监委代主任 周可以（2024年6月任）
    ("lh_zhou_keyi", "周可以", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县监察委员会副主任、代理主任", "莲花县监察委员会",
     "https://px.jxnews.com.cn/system/2024/06/28/020551367.shtml"),

    # ═══ 县检察院 ═══

    # 县检察院检察长 胡晨琳（女，2026年2月补选）
    ("lh_hu_chenlin", "胡晨琳", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县人民检察院检察长", "莲花县人民检察院",
     "https://kknews.xyz/55259"),

    # ═══ 县公安局 ═══
    # 副县长兼公安局长 — 从报道中未明确确认

    # ═══ 其他重要人物 ═══

    # 县政府办公室主任、党组成员 张方清
    ("lh_zhang_fangqing", "张方清", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县政府办公室主任、党组成员", "莲花县人民政府办公室",
     "https://zgcounty.com/news/33720.html"),

    # 县纪委副书记、监委副主任 朱力
    ("lh_zhu_li", "朱力", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "莲花县纪委副书记、监委副主任", "莲花县监察委员会",
     "https://px.jxnews.com.cn/system/2021/11/18/019454361.shtml"),
]

# ═══════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# Format: (id, name, type, level, parent, location)
# ═══════════════════════════════════════════════════════════════════════

ORGANIZATIONS = [
    # 县级四套班子
    ("org_lh_county_party", "中共莲花县委员会", "党委", "县级", "中共萍乡市委", "萍乡市莲花县琴亭镇"),
    ("org_lh_county_gov", "莲花县人民政府", "政府", "县级", "萍乡市人民政府", "萍乡市莲花县琴亭镇"),
    ("org_lh_npc", "莲花县人大常委会", "人大", "县级", "萍乡市人大常委会", "萍乡市莲花县琴亭镇"),
    ("org_lh_cppcc", "政协莲花县委员会", "政协", "县级", "政协萍乡市委员会", "萍乡市莲花县琴亭镇"),

    # 纪检监察
    ("org_lh_discipline", "莲花县纪律检查委员会/监察委员会", "党委", "县级", "中共莲花县委/萍乡市纪委监委", "萍乡市莲花县琴亭镇"),

    # 政法
    ("org_lh_procuratorate", "莲花县人民检察院", "事业单位", "县级", "莲花县人民代表大会", "萍乡市莲花县琴亭镇"),
    ("org_lh_public_security", "莲花县公安局", "政府", "县级", "莲花县人民政府/萍乡市公安局", "萍乡市莲花县琴亭镇"),

    # 政府组成部门
    ("org_lh_gov_office", "莲花县人民政府办公室", "政府", "县级", "莲花县人民政府", "萍乡市莲花县琴亭镇"),

    # 上级/相关机构
    ("org_pingxiang_municipal", "萍乡市人大常委会", "人大", "地市级", "萍乡市", "萍乡市"),
    ("org_pingxiang_gov", "萍乡市人民政府", "政府", "地市级", "江西省人民政府", "萍乡市"),
    ("org_pingxiang_party", "中共萍乡市委", "党委", "地市级", "中共江西省委", "萍乡市"),
    ("org_wugongshan", "武功山风景名胜区管委会", "事业单位", "地市级", "萍乡市人民政府", "萍乡市武功山"),
    ("org_pingxiang_tech", "萍乡市科技局", "政府", "地市级", "萍乡市人民政府", "萍乡市"),
    ("org_ministry_civil_affairs", "民政部", "政府", "省部级", "国务院", "北京市"),
    ("org_national_rehab", "国家康复辅具研究中心", "事业单位", "省部级", "民政部", "北京市"),
    ("org_pingxiang_org", "萍乡市委组织部", "党委", "地市级", "中共萍乡市委", "萍乡市"),
    ("org_pingxiang_gov_office", "萍乡市委办公室", "党委", "地市级", "中共萍乡市委", "萍乡市"),
    ("org_lh_xianwei_office", "中共莲花县委办公室", "党委", "县级", "中共莲花县委", "萍乡市莲花县琴亭镇"),
    ("org_lh_party_school", "莲花县委党校/甘祖昌干部学院", "事业单位", "县级", "中共莲花县委", "萍乡市莲花县"),
    ("org_shangli_county", "上栗县人民政府", "政府", "县级", "萍乡市人民政府", "萍乡市上栗县"),
    ("org_anyuan_district", "安源区人民政府", "政府", "县级", "萍乡市人民政府", "萍乡市安源区"),
]

# ═══════════════════════════════════════════════════════════════════════
# POSITIONS (career history)
# Format: (person_id, org_id, title, start_date, end_date, rank, note)
# ═══════════════════════════════════════════════════════════════════════

POSITIONS = [
    # ── 易刚（县委书记） ──
    ("lh_yi_gang", "org_lh_county_party", "莲花县委书记", "2021-08", "至今", "正县级", "2021年8月任莲花县委书记至今"),
    ("lh_yi_gang", "org_pingxiang_municipal", "萍乡市（任前职务待查）", "待查", "2021-08", "副县级待查", "2021年8月从萍乡市调任莲花县委书记"),
    ("lh_yi_gang", "org_pingxiang_party", "萍乡市（早期职务待查）", "待查", "待查", "待查", "江西芦溪人，1972年9月生，省委党校研究生学历"),

    # ── 王东成（县长） ──
    ("lh_wang_dongcheng", "org_lh_county_gov", "莲花县委副书记、县长", "2026-02", "至今", "正县级", "2026年2月28日莲花县第十八届人大七次会议补选为县长"),
    ("lh_wang_dongcheng", "org_lh_county_gov", "莲花县人民政府副县长", "2024-06", "2026-02", "副县级", "2024年6月任副县长，同年被提名为代县长"),
    ("lh_wang_dongcheng", "org_lh_discipline", "莲花县委常委、县纪委书记、县监委主任", "2021-08", "2024-06", "副县级", "2021年8月任县委常委、纪委书记、监委主任"),
    ("lh_wang_dongcheng", "org_pingxiang_municipal", "萍乡市纪委（任前职务待查）", "待查", "2021-08", "待查", "从萍乡市纪委系统调入莲花县"),
    ("lh_wang_dongcheng", "org_pingxiang_org", "萍乡市委组织部（早期职务待查）", "待查", "待查", "待查", "1980年2月生，大学本科学历"),

    # ── 曾衍敏（前任县长） ──
    ("lh_zeng_yanmin", "org_lh_county_gov", "莲花县委副书记、县长", "2021-08", "2026-02", "正县级", "2021年8月任代县长→县长，2026年2月卸任，去向待查"),
    ("lh_zeng_yanmin", "org_lh_county_party", "莲花县委副书记", "2018-11", "2021-08", "副县级", "2018年11月至2021年8月任县委副书记"),
    ("lh_zeng_yanmin", "org_lh_county_gov", "莲花县委常委、副县长", "2016-07", "2018-11", "副县级", "2016年7月至2018年11月任常委、副县长"),
    ("lh_zeng_yanmin", "org_pingxiang_gov_office", "萍乡市委办公室副主任", "2015-08", "2016-07", "副县级", "2015年8月任萍乡市委办公室副主任"),
    ("lh_zeng_yanmin", "org_lh_discipline", "莲花县委常委、纪委书记", "2013-04", "2015-08", "副县级", "2013年4月至2015年8月任莲花县委常委、纪委书记"),
    ("lh_zeng_yanmin", "org_pingxiang_org", "萍乡市委组织部干部综合科科长", "待查", "2013-04", "正科级", "历任市委组织部副主任科员、干部一科副科长、主任科员、干部监督科科长、干部综合科科长"),
    ("lh_zeng_yanmin", "org_lh_county_gov", "莲花县副县长", "2016-09", "2018-11", "副县级", "2016年9月当选为莲花县副县长"),

    # ── 贺延伟（挂职县委副书记、副县长） ──
    ("lh_he_yanwei", "org_lh_county_gov", "莲花县委副书记、副县长（挂职）", "2023-10", "至今", "副县级", "2023年10月30日任莲花县副县长（挂职），兼任县委副书记"),
    ("lh_he_yanwei", "org_ministry_civil_affairs", "民政部区划地名司副处长兼二级调研员", "待查", "2023-10", "正处级", "民政部区划地名司主任科员、副处长兼二级调研员"),
    ("lh_he_yanwei", "org_ministry_civil_affairs", "民政部区划地名司主任科员", "待查", "待查", "主任科员", ""),
    ("lh_he_yanwei", "org_ministry_civil_affairs", "天津海关副主任科员", "待查", "待查", "副主任科员", "1980年12月生，山东烟台人，理学硕士"),

    # ── 张运来（原县委书记，被双开） ──
    ("lh_zhang_yunlai", "org_lh_county_party", "莲花县委书记", "2019-05", "2021-08", "正县级", "2019年5月至2021年8月任莲花县委书记"),
    ("lh_zhang_yunlai", "org_lh_county_gov", "莲花县委副书记、县长", "2016-07", "2019-05", "正县级", "2016年7月至2019年5月任县长（2019年1月起兼任县委书记）"),
    ("lh_zhang_yunlai", "org_lh_county_party", "莲花县委副书记、政法委书记", "2013-12", "2016-07", "正县级", "2013年12月至2016年7月任县委副书记（正县级）、政法委书记"),
    ("lh_zhang_yunlai", "org_pingxiang_gov", "萍乡市商务局党委副书记、局长", "2011-06", "2013-12", "正县级", "2011年6月至2013年12月任市商务局局长"),
    ("lh_zhang_yunlai", "org_pingxiang_gov", "萍乡市商业管理办公室党委副书记、主任", "2009-03", "2011-06", "正县级", ""),
    ("lh_zhang_yunlai", "org_shangli_county", "上栗县委常委、常务副县长", "2009-01", "2009-03", "副县级", ""),
    ("lh_zhang_yunlai", "org_shangli_county", "上栗县委常委、政法委书记", "2007-01", "2009-01", "副县级", ""),
    ("lh_zhang_yunlai", "org_shangli_county", "上栗县委常委、农工委书记", "2006-08", "2007-01", "副县级", ""),
    ("lh_zhang_yunlai", "org_shangli_county", "上栗县政府副县长", "2003-12", "2006-08", "副县级", ""),
    ("lh_zhang_yunlai", "org_pingxiang_municipal", "萍乡市人大常委会办公室二级巡视员", "2021-08", "2023-01", "副厅级", "2021年8月调任市人大，2023年1月被查"),

    # ── 曾国祥（前任县长） ──
    ("lh_zeng_guoxiang", "org_lh_county_gov", "莲花县委副书记、县长", "2019-08", "2021-08", "正县级", "2019年8月当选县长，2021年8月辞职"),

    # ── 陈礼虎（原常务副县长） ──
    ("lh_chen_lihu", "org_wugongshan", "武功山风景名胜区党委委员、管委会副主任", "2024-06", "至今", "副县级", "2024年6月调离莲花县"),
    ("lh_chen_lihu", "org_lh_county_gov", "莲花县委常委、常务副县长", "2021-09", "2024-06", "副县级", "2021年9月至2024年6月任常委、常务副县长"),

    # ── 刘力亚 ──
    ("lh_liu_liya", "org_lh_county_gov", "莲花县委常委、副县长", "待查", "至今", "副县级", "2016年9月当选副县长，后任县委常委"),

    # ── 王红宙（挂职副县长） ──
    ("lh_wang_hongzhou", "org_lh_county_gov", "莲花县委常委、副县长（挂职）", "2021-08", "至今", "副县级", "2021年8月起挂职两年（可能已续期）"),
    ("lh_wang_hongzhou", "org_national_rehab", "国家康复辅具研究中心后勤基建管理部副主任", "待查", "2021-08", "正处级", "从国家康复辅具研究中心派出挂职"),

    # ── 刘美兰（县人大常委会主任） ──
    ("lh_liu_meilan", "org_lh_npc", "莲花县人大常委会党组书记、主任", "2023-08", "至今", "正县级", "2023年8月补选为县人大常委会主任"),

    # ── 朱白明（原县人大常委会主任，被查） ──
    ("lh_zhu_baiming", "org_lh_npc", "莲花县人大常委会党组书记、主任", "2021-09", "2023-02", "正县级", "2021年9月任，2023年2月被查"),
    ("lh_zhu_baiming", "org_lh_county_party", "莲花县委常委、政法委书记", "2016-07", "2021-09", "副县级", "2016年7月至2021年8月任"),
    ("lh_zhu_baiming", "org_lh_county_gov", "莲花县政府副县长", "2011-08", "2016-07", "副县级", ""),

    # ── 汤杰（县政协主席） ──
    ("lh_tang_jie", "org_lh_cppcc", "莲花县政协党组书记、主席", "2021", "至今", "正县级", "接替刘海林任县政协主席"),

    # ── 刘海林（原县政协主席，被查） ──
    ("lh_liu_hailin", "org_lh_cppcc", "莲花县政协党组书记、主席", "2016-09", "2026-07", "正县级", "2026年7月被查，涉嫌严重违纪违法"),
    ("lh_liu_hailin", "org_lh_cppcc", "莲花县政协副主席", "2016-09", "2016-09", "副县级", "2016年9月当选政协副主席后转任主席"),

    # ── 周可以（代监委主任） ──
    ("lh_zhou_keyi", "org_lh_discipline", "莲花县监察委员会副主任、代理主任", "2024-06", "至今", "副县级", "接替王东成任监委代主任"),

    # ── 胡晨琳（县检察院检察长） ──
    ("lh_hu_chenlin", "org_lh_procuratorate", "莲花县人民检察院检察长", "2026-02", "至今", "副县级", "2026年2月28日补选"),
]

# ═══════════════════════════════════════════════════════════════════════
# RELATIONSHIPS (work overlaps, connections)
# Format: (person_a, person_b, type, context, overlap_org, overlap_period)
# ═══════════════════════════════════════════════════════════════════════

RELATIONSHIPS = [
    # ── 县委书记 ↔ 县长（党政一把手关系） ──
    ("lh_yi_gang", "lh_wang_dongcheng", "上下级", "易刚（书记）与王东成（县长）党政搭档", "中共莲花县委/莲花县人民政府", "2024-06至今"),
    ("lh_yi_gang", "lh_zeng_yanmin", "上下级", "易刚（书记）与曾衍敏（前县长）党政搭档", "中共莲花县委/莲花县人民政府", "2021-08至2026-02"),

    # ── 张运来（前书记）与搭档的关系 ──
    ("lh_zhang_yunlai", "lh_zeng_guoxiang", "上下级", "张运来（前书记）与曾国祥（前县长）党政搭档", "中共莲花县委/莲花县人民政府", "2019-08至2021-08"),

    # ── 曾衍敏与王东成的交接 ──
    ("lh_zeng_yanmin", "lh_wang_dongcheng", "交接", "王东成接替曾衍敏任县长", "莲花县人民政府", "2026-02"),

    # ── 纪委系统内部关系 ──
    ("lh_wang_dongcheng", "lh_zhou_keyi", "交接", "王东成（原监委主任）与周可以（代监委主任）交接", "莲花县纪委监委", "2024-06"),
    ("lh_wang_dongcheng", "lh_zhu_li", "上下级", "王东成（原纪委书记）与朱力（纪委副书记）同事关系", "莲花县纪委监委", "2021-08至2024-06"),

    # ── 曾衍敏与张运来的关系 ──
    ("lh_zeng_yanmin", "lh_zhang_yunlai", "同事", "曾衍敏（副书记/副县长）与张运来（书记/县长）共事", "中共莲花县委/莲花县人民政府", "2013-04至2021-08"),

    # ── 挂职干部 ──
    ("lh_he_yanwei", "lh_yi_gang", "上下级", "贺延伟（挂职副书记）向易刚（书记）汇报工作", "中共莲花县委", "2023-10至今"),
    ("lh_wang_hongzhou", "lh_yi_gang", "上下级", "王红宙（挂职副县长）在易刚领导下工作", "莲花县人民政府", "2021-08至今"),

    # ── 前任被查链条 ──
    ("lh_zhang_yunlai", "lh_zhu_baiming", "同事", "张运来（书记）与朱白明（政法委书记/人大主任）共事", "莲花县", "2013-12至2021-08"),
    ("lh_zhang_yunlai", "lh_liu_hailin", "同事", "张运来（书记）与刘海林（政协主席）共事", "莲花县", "2016-09至2021-08"),
    ("lh_zhu_baiming", "lh_liu_hailin", "同事", "朱白明（人大主任）与刘海林（政协主席）同为正县级领导", "莲花县四套班子", "2021-09至2023-02"),

    # ── 陈礼虎与王东成 ──
    ("lh_chen_lihu", "lh_wang_dongcheng", "同事", "陈礼虎（常务副县长）与王东成（时任纪委书记）共事", "莲花县", "2021-08至2024-06"),

    # ── 刘力亚长年任职 ──
    ("lh_liu_liya", "lh_yi_gang", "上下级", "刘力亚（副县长/常委）在易刚领导下工作", "莲花县人民政府", "2021-08至今"),
    ("lh_liu_liya", "lh_zeng_yanmin", "同事", "刘力亚与曾衍敏曾在县政府共事", "莲花县人民政府", "2016至2026"),
    ("lh_liu_liya", "lh_zhang_yunlai", "同事", "刘力亚与张运来曾共事", "莲花县人民政府", "2016-09至2021-08"),

    # ── 市人大层级关系 ──
    ("lh_zhang_yunlai", "org_pingxiang_municipal", "调任", "张运来2021年8月调任萍乡市人大常委会办公室", "", "2021-08至2023-01"),
]

# ═══════════════════════════════════════════════════════════════════════
# Helper functions
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(person_id):
    """Color by role: red=secretary, blue=gov leader, orange=discipline, grey=other."""
    red_ids = {"lh_yi_gang"}  # 县委书记
    blue_ids = {
        "lh_wang_dongcheng", "lh_zeng_yanmin", "lh_zeng_guoxiang",  # 县长/前县长
        "lh_chen_lihu", "lh_liu_liya", "lh_wang_hongzhou",  # 副县长
        "lh_zhangqiong_mengna", "lh_liu_xiaofei", "lh_wen_kai", "lh_ding_shan",
        "lh_yan_hui", "lh_liu_haifeng", "lh_wu_xiaowen", "lh_tang_yongfeng",
        "lh_guo_xiaobin", "lh_dai_gang", "lh_liu_huaping", "lh_he_yanwei",
    }
    orange_ids = {"lh_wang_dongcheng", "lh_zhou_keyi", "lh_zhu_li"}  # 纪委/监委—王东成曾兼
    # Note: 王东成现在是县长(blue)，但曾当过纪委书记。Let's make him blue as current role.

    if person_id in red_ids:
        return "255,50,50"
    elif person_id in blue_ids or person_id == "lh_wang_dongcheng":
        return "50,100,255"
    elif person_id in orange_ids:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
    }
    return colors.get(org_type, "200,200,200")


# ═══════════════════════════════════════════════════════════════════════
# BUILD SQLite DB
# ═══════════════════════════════════════════════════════════════════════

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
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
        );

        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

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
        );
    """)

    # Insert persons
    for p in PERSONS:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", p)

    # Insert organizations
    for o in ORGANIZATIONS:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""", o)

    # Insert positions
    for pos in POSITIONS:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?,?,?,?,?,?,?)""", pos)

    # Insert relationships
    for r in RELATIONSHIPS:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""", r)

    conn.commit()
    conn.close()
    print(f"✅ SQLite DB: {DB_PATH}")


# ═══════════════════════════════════════════════════════════════════════
# BUILD GEXF Graph
# ═══════════════════════════════════════════════════════════════════════

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []

    # Header
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Government Network Investigator</creator>')
    lines.append('    <description>莲花县（萍乡市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes: node
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="birthplace" type="string"/>')
    lines.append('      <attribute id="4" title="education" type="string"/>')
    lines.append('      <attribute id="5" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Attributes: edge
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        birth = esc(p[4])
        birthplace = esc(p[5])
        education = esc(p[6])
        role = esc(p[9] or "")
        source = esc(p[11] or "")
        c = person_color(pid)
        sz = "20.0" if pid in ("lh_yi_gang", "lh_wang_dongcheng") else "12.0"
        lines.append(f'      <node id="{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{birth}"/>')
        lines.append(f'          <attvalue for="3" value="{birthplace}"/>')
        lines.append(f'          <attvalue for="4" value="{education}"/>')
        lines.append(f'          <attvalue for="5" value="{source}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        c = org_color(otype)
        lines.append(f'      <node id="{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (positions)
    for pos in POSITIONS:
        pid = pos[0]
        oid = pos[1]
        title = pos[2]
        start = pos[3]
        end = pos[4]
        note = pos[6]
        label = f"{title} ({start}–{end})"
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(label)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person↔Person (relationships)
    for r in RELATIONSHIPS:
        if len(r) == 6:
            a, b, rtype, ctx, overlap, period = r
            # Skip if either is not a person ID (could be org ref)
            if a.startswith("org_") or b.startswith("org_"):
                continue
            label = f"{rtype}: {esc(ctx)}"
            lines.append(f'      <edge id="e{eid}" source="{a}" target="{b}" label="{label}" weight="2.0">')
            lines.append('        <attvalues>')
            lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')
            eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  莲花县领导班子工作关系网络 — 数据构建")
    print("=" * 60)
    print(f"\nPersons: {len(PERSONS)}")
    print(f"Organizations: {len(ORGANIZATIONS)}")
    print(f"Positions (career entries): {len(POSITIONS)}")
    print(f"Relationships: {len(RELATIONSHIPS)}")
    print()

    build_db()
    build_gexf()

    print(f"\n{'=' * 60}")
    print("  Done!")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"{'=' * 60}")

    # Print summary
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        count = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} records")
    conn.close()


if __name__ == "__main__":
    main()
