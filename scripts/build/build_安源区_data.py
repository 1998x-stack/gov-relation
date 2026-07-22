#!/usr/bin/env python3
"""
安源区（萍乡市市辖区）领导班子工作关系网络 — 数据构建脚本
Builds SQLite DB + GEXF graph for Anyuan District leadership network.

Research date: 2026-07-15
Sources used:
  - px.jxnews.com.cn (大江网/萍乡头条)
  - thepaper.cn (澎湃新闻)
  - news.qq.com (腾讯新闻)
  - shobserver.com (上观新闻)
  - jx.people.com.cn (人民网江西频道)
  - 163.com (网易新闻)
  - cs0799.com (萍乡城事网)
  - guan.media (观媒网)
  - baike.baidu.com (百度百科)
  - district.ce.cn (中国经济网)
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data/database/安源区_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "data/graph/安源区_network.gexf")

# ── PERSONS ──
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
PERSONS = [
    # ═══ Current Top Leaders ═══

    # 区委书记 邱伟（2025年5月任）
    ("anyuan_qiu_wei", "邱伟", "男", "汉族", "1983-01", "江西信丰",
     "厦门大学/新闻学硕士", "2005-12", "2000-09",
     "安源区委书记", "中共萍乡市安源区委员会",
     "https://www.thepaper.cn/newsDetail_forward_30830428"),

    # 区委副书记、区长 汤艳红（2025年9月提名）
    ("anyuan_tang_yanhong", "汤艳红", "女", "汉族", "1979-04", "江西湘东",
     "省委党校研究生", "中共党员", "？",
     "安源区委副书记、区长", "安源区人民政府",
     "https://guan.media/news/detail_15832.html"),

    # 区委副书记 龚云华
    ("anyuan_gong_yunhua", "龚云华", "男", "汉族", "1979-02", "江西湘东",
     "在职研究生", "2001-08", "2001-03",
     "安源区委副书记", "中共萍乡市安源区委员会",
     "https://baike.so.com/doc/1157728-24992702.html"),

    # ═══ Standing Committee (区委常委) ═══

    # 区委常委、常务副区长 袁子安
    ("anyuan_yuan_zian", "袁子安", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "安源区委常委、常务副区长", "安源区人民政府",
     "https://px.jxnews.com.cn/system/2024/11/04/020687371.shtml"),

    # 区委常委、副区长、安源工业园党工委书记 黄国晖（原统战部长）
    ("anyuan_huang_guohui", "黄国晖", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "安源区委常委、副区长、安源工业园党工委书记", "安源区人民政府",
     "https://px.jxnews.com.cn/system/2024/10/22/020673459.shtml"),

    # 区委常委、宣传部部长 邬思海
    ("anyuan_wu_sihai", "邬思海", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "安源区委常委、宣传部部长", "中共萍乡市安源区委宣传部",
     "https://px.jxnews.com.cn/system/2024/11/12/020695763.shtml"),

    # 区委常委、统战部部长 汤如龙
    ("anyuan_tang_rulong", "汤如龙", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "安源区委常委、统战部部长", "中共萍乡市安源区委统一战线工作部",
     "https://www.cs0799.com/portal.php?catid=106&mod=list"),

    # 区纪委书记 叶继辉（市纪委副书记提名人选兼任）
    ("anyuan_ye_jihui", "叶继辉", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "安源区委常委、区纪委书记、区监委主任", "中共萍乡市安源区纪律检查委员会",
     "https://px.jxnews.com.cn/system/2024/07/04/020558585.shtml"),

    # ═══ Government (区政府副区长) ═══

    # 副区长、安源公安分局局长 叶方
    ("anyuan_ye_fang", "叶方", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长、安源公安分局局长", "萍乡市公安局安源分局",
     "https://px.jxnews.com.cn/system/2024/11/20/020704673.shtml"),

    # 副区长 谢晖（原安源工业园党工委书记）
    ("anyuan_xie_hui", "谢晖", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "安源区副区长", "安源区人民政府",
     "https://px.jxnews.com.cn/system/2024/10/22/020673459.shtml"),

    # 副区长 杨树
    ("anyuan_yang_shu", "杨树", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "安源区副区长", "安源区人民政府",
     "https://px.jxnews.com.cn/system/2024/11/04/020687371.shtml"),

    # 副区长 廖志群（女，农工党员）
    ("anyuan_liao_zhiqun", "廖志群", "女", "汉族", "1976-06", "待查",
     "大学", "农工党员", "待查",
     "安源区副区长", "安源区人民政府",
     "https://px.jxnews.com.cn/system/2024/01/31/020389965.shtml"),

    # 副区长 葛堃（博士）
    ("anyuan_ge_kun", "葛堃", "男", "汉族", "1986-02", "待查",
     "博士研究生", "中共党员", "待查",
     "安源区副区长", "安源区人民政府",
     "https://jiangxi.jxnews.com.cn/system/2024/11/29/020714514.shtml"),

    # 副区长 刘松（原）
    ("anyuan_liu_song", "刘松", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "安源区副区长（原）", "安源区人民政府",
     "https://px.jxnews.com.cn/system/2024/10/22/020673459.shtml"),

    # ═══ NPC & CPPCC ═══

    # 区人大常委会主任 黄卫东
    ("anyuan_huang_weidong", "黄卫东", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "安源区人大常委会主任", "萍乡市安源区人民代表大会常务委员会",
     "https://px.jxnews.com.cn/system/2024/11/12/020695763.shtml"),

    # 区政协主席（待确认姓名）
    ("anyuan_cppcc_chair", "（待确认）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "安源区政协主席", "中国人民政治协商会议萍乡市安源区委员会",
     "⚠️ 待确认"),

    # ═══ Predecessors ═══

    # 前区委书记 李水清（2021-2025，升任萍乡市人大常委会副主任）
    ("anyuan_li_shuiqing", "李水清", "男", "汉族", "1968-11", "江西莲花",
     "大学，高级工商管理硕士", "1988-05", "1988-08",
     "萍乡市人大常委会副主任（原安源区委书记）", "萍乡市人大常委会",
     "https://baike.baidu.com/item/%E6%9D%8E%E6%B0%B4%E6%B8%85/1610403"),

    # 前区委书记 康峰（2019-2021）
    ("anyuan_kang_feng", "康峰", "男", "汉族", "1967-10", "江西遂川",
     "大学/工商管理硕士", "1989-07", "1989-07",
     "（原安源区委书记、区长）", "（原安源区）",
     "https://www.newton.com.tw/wiki/%E5%BA%B7%E5%B3%B0/19903046"),

    # 前区长 邱伟 ← 升任书记
    # (same as anyuan_qiu_wei above, this role is captured in positions)

    # 前区委副书记 黎增义（前任区长）
    ("anyuan_li_zengyi", "黎增义", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "（原安源区委副书记、区长）", "（原安源区人民政府）",
     "https://px.jxnews.com.cn/system/2020/07/28/018986983.shtml"),

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
    ("anyuan_party", "中共萍乡市安源区委员会", "党委", "县处级", "中共萍乡市委员会", "江西省萍乡市安源区"),
    ("anyuan_gov", "安源区人民政府", "政府", "县处级", "萍乡市人民政府", "江西省萍乡市安源区"),
    ("anyuan_discipline", "中共萍乡市安源区纪律检查委员会", "纪委", "县处级", "萍乡市纪委监委", "江西省萍乡市安源区"),
    ("anyuan_org_dept", "中共萍乡市安源区委组织部", "党委部门", "乡科级", "中共安源区委", "江西省萍乡市安源区"),
    ("anyuan_propaganda", "中共萍乡市安源区委宣传部", "党委部门", "乡科级", "中共安源区委", "江西省萍乡市安源区"),
    ("anyuan_united_front", "中共萍乡市安源区委统一战线工作部", "党委部门", "乡科级", "中共安源区委", "江西省萍乡市安源区"),
    ("anyuan_npc", "萍乡市安源区人民代表大会常务委员会", "人大", "县处级", "萍乡市人大常委会", "江西省萍乡市安源区"),
    ("anyuan_cppcc", "中国人民政治协商会议萍乡市安源区委员会", "政协", "县处级", "萍乡市政协", "江西省萍乡市安源区"),
    ("anyuan_public_security", "萍乡市公安局安源分局", "公安", "乡科级", "萍乡市公安局", "江西省萍乡市安源区"),
    ("anyuan_industrial_park", "安源工业园", "园区", "待查", "安源区人民政府", "江西省萍乡市安源区"),
    # City level
    ("px_party", "中共萍乡市委员会", "党委", "地市级", "中共江西省委员会", "江西省萍乡市"),
    ("px_gov", "萍乡市人民政府", "政府", "地市级", "江西省人民政府", "江西省萍乡市"),
    ("px_npc", "萍乡市人大常委会", "人大", "地市级", "江西省人大常委会", "江西省萍乡市"),
]

POSITIONS = [
    # (person_id, org_id, title, start, end, rank, note)

    # ═══ 邱伟 - 完整履历 ═══
    ("anyuan_qiu_wei", "anyuan_party", "安源区委书记", "2025-05", "至今", "县处级正职",
     "2025年5月28日省委市委决定任安源区委书记"),
    ("anyuan_qiu_wei", "anyuan_gov", "安源区委副书记、区长（前任）", "2021-09", "2025-05", "县处级正职",
     "2021年9月人大正式选举为区长；2025年5月升任书记"),
    ("anyuan_qiu_wei", "anyuan_gov", "安源区代区长", "2021-08", "2021-09", "县处级正职", ""),
    ("anyuan_qiu_wei", "anyuan_party", "安源区委副书记（正县级）", "2020-11", "2021-08", "县处级正职",
     "兼任区委党校校长"),
    ("anyuan_qiu_wei", "anyuan_party", "安源区委副书记（正县级）", "2020-05", "2020-11", "县处级正职",
     "选派参加十四届省委第八轮巡视锻炼"),
    ("anyuan_qiu_wei", "anyuan_gov", "江西省减灾备灾中心主任（省应急管理厅）", "2018-12", "2020-05", "正处级",
     "2019.09-2020.01 江西省委党校第55期中青班学习"),
    ("anyuan_qiu_wei", "anyuan_gov", "江西省民政厅救灾处副处长", "约2015", "约2018", "副处级",
     "2014年任救灾处副处长"),
    ("anyuan_qiu_wei", "anyuan_gov", "江西省减灾备灾中心主任（省民政厅）", "约2014", "2018-12", "正处级", ""),
    ("anyuan_qiu_wei", "anyuan_gov", "江西省民政厅救灾处主任科员", "约2011", "约2014", "主任科员", ""),
    ("anyuan_qiu_wei", "anyuan_gov", "江西省民政厅救灾处（省减灾办）副主任科员", "约2009", "约2011", "副主任科员", ""),
    ("anyuan_qiu_wei", "anyuan_gov", "江西省民政厅救灾处（省减灾办）科员", "2008-04", "约2009", "科员",
     "2008年4月进入江西省民政厅"),
    ("anyuan_qiu_wei", "anyuan_gov", "深圳市龙岗区交通局人秘科（聘用）", "2007-07", "2008-04", "聘用",
     "厦门大学研究生毕业后"),
    ("anyuan_qiu_wei", "anyuan_gov", "厦门大学新闻传播学院新闻学硕士研究生", "2004-09", "2007-07", "学生", ""),
    ("anyuan_qiu_wei", "anyuan_gov", "江西教育学院英语专业本科", "2002-09", "2004-07", "学生", ""),
    ("anyuan_qiu_wei", "anyuan_gov", "江西省信丰县新田中学教师", "2001-09", "2004-09", "教师", ""),
    ("anyuan_qiu_wei", "anyuan_gov", "江西省信丰县新田中心小学教师", "2000-09", "2001-09", "教师", ""),
    ("anyuan_qiu_wei", "anyuan_gov", "南昌大学汉语言文学专业自考专科", "1999-10", "2001-10", "学生", ""),
    ("anyuan_qiu_wei", "anyuan_gov", "江西省龙南师范学校学习", "1997-09", "2000-07", "学生", ""),

    # ═══ 汤艳红 ═══
    ("anyuan_tang_yanhong", "anyuan_gov", "安源区委副书记、区长", "2025-09", "至今", "县处级正职",
     "2025年9月任区委副书记、提名为区长候选人"),
    ("anyuan_tang_yanhong", "anyuan_party", "安源区委副书记", "2025-09", "至今", "县处级正职", ""),
    ("anyuan_tang_yanhong", "anyuan_gov", "萍乡市新闻传媒中心（传媒集团）党委书记、主任、董事长", "2020-08", "2025-09", "正处级",
     "2020年8月任前公示"),
    ("anyuan_tang_yanhong", "anyuan_gov", "湘东区委常委、宣传部部长", "约2016", "2020-08", "副县级",
     "https://www.thepaper.cn/newsDetail_forward_30830428"),

    # ═══ 龚云华 ═══
    ("anyuan_gong_yunhua", "anyuan_party", "安源区委副书记", "约2024", "至今", "县处级副职",
     "2024年1月卸任常务副区长转副书记（按公开报道推测）"),
    ("anyuan_gong_yunhua", "anyuan_gov", "安源区委常委、常务副区长", "约2022", "2024-01", "县处级副职",
     "2024年1月辞去副区长职务"),
    ("anyuan_gong_yunhua", "anyuan_party", "莲花县委常委、常务副县长（正县级）", "2019-01", "约2022", "正县级",
     "来源：360百科"),
    ("anyuan_gong_yunhua", "anyuan_party", "莲花县委常委、宣传部部长（正县级）", "2016-08", "2019-01", "正县级", ""),
    ("anyuan_gong_yunhua", "anyuan_gov", "莲花县委常委、副县长（挂职锻炼）", "2015-08", "2016-08", "副县级",
     "江西省委统战部六处处长挂职"),
    ("anyuan_gong_yunhua", "anyuan_party", "江西省委统战部六处处长", "约2013", "2015-08", "正处级", ""),
    ("anyuan_gong_yunhua", "anyuan_party", "江西省委统战部一处副处长", "2011-07", "约2013", "副处级", ""),
    ("anyuan_gong_yunhua", "anyuan_party", "江西省委统战部一处副处长（其间）", "2009-09", "2011-07", "副处级", ""),
    ("anyuan_gong_yunhua", "anyuan_party", "江西省委统战部一处处长", "约2009", "2009-09", "正处级", ""),
    ("anyuan_gong_yunhua", "anyuan_party", "江西省委统战部一处主任科员", "2004-12", "约2009", "主任科员", ""),
    ("anyuan_gong_yunhua", "anyuan_party", "江西省委统战部一处副主任科员", "2003-09", "2004-12", "副主任科员", ""),
    ("anyuan_gong_yunhua", "anyuan_gov", "上栗县杨岐乡人民政府乡长助理", "2001-08", "2003-09", "乡长助理",
     "2001年3月参加工作"),
    ("anyuan_gong_yunhua", "anyuan_gov", "江西农业大学职师院农艺教育专业学习", "1997-09", "2001-08", "学生", ""),

    # ═══ 袁子安 ═══
    ("anyuan_yuan_zian", "anyuan_gov", "安源区委常委、常务副区长", "约2023", "至今", "县处级副职", ""),
    ("anyuan_yuan_zian", "anyuan_party", "安源区委常委", "约2023", "至今", "县处级副职", ""),

    # ═══ 黄国晖 ═══
    ("anyuan_huang_guohui", "anyuan_gov", "安源区委常委、副区长、安源工业园党工委书记", "约2024", "至今", "县处级副职", ""),
    ("anyuan_huang_guohui", "anyuan_party", "安源区委常委", "约2022", "至今", "县处级副职",
     "原任区委统战部部长、丹江街党委书记"),

    # ═══ 邬思海 ═══
    ("anyuan_wu_sihai", "anyuan_propaganda", "安源区委常委、宣传部部长", "约2024", "至今", "县处级副职", ""),
    ("anyuan_wu_sihai", "anyuan_party", "安源区委常委", "约2024", "至今", "县处级副职", ""),

    # ═══ 汤如龙 ═══
    ("anyuan_tang_rulong", "anyuan_united_front", "安源区委常委、统战部部长", "约2024", "至今", "县处级副职", ""),
    ("anyuan_tang_rulong", "anyuan_party", "安源区委常委", "约2024", "至今", "县处级副职", ""),

    # ═══ 叶继辉 ═══
    ("anyuan_ye_jihui", "anyuan_discipline", "安源区纪委书记、区监委主任", "约2024", "至今", "县处级副职",
     "市纪委副书记提名人选兼任"),
    ("anyuan_ye_jihui", "anyuan_party", "安源区委常委", "约2024", "至今", "县处级副职", ""),

    # ═══ 副区长们 ═══
    ("anyuan_ye_fang", "anyuan_public_security", "安源区副区长、安源公安分局局长", "约2023", "至今", "县处级副职", ""),
    ("anyuan_ye_fang", "anyuan_gov", "安源区副区长", "约2023", "至今", "县处级副职", ""),

    ("anyuan_xie_hui", "anyuan_gov", "安源区副区长", "约2022", "至今", "县处级副职",
     "原安源工业园党工委书记"),
    ("anyuan_xie_hui", "anyuan_industrial_park", "安源工业园党工委书记（原，兼）", "约2022", "约2024", "", ""),

    ("anyuan_yang_shu", "anyuan_gov", "安源区副区长", "约2024", "至今", "县处级副职", ""),

    ("anyuan_liao_zhiqun", "anyuan_gov", "安源区副区长", "2024-01", "至今", "县处级副职",
     "2024年1月31日区人大常委会任命，农工党员"),
    ("anyuan_liao_zhiqun", "anyuan_gov", "安源区发改委主任（原）", "约2022", "2024-01", "乡科级正职", ""),

    ("anyuan_ge_kun", "anyuan_gov", "安源区副区长", "2024-11", "至今", "县处级副职",
     "2024年11月29日区人大常委会任命，博士研究生"),

    ("anyuan_liu_song", "anyuan_gov", "安源区副区长（原）", "约2022", "约2024", "县处级副职",
     "2024年初已不再担任副区长（报道显示卸任）"),

    # ═══ 人大政协 ═══
    ("anyuan_huang_weidong", "anyuan_npc", "安源区人大常委会主任", "约2024", "至今", "县处级正职", ""),
    ("anyuan_cppcc_chair", "anyuan_cppcc", "安源区政协主席", "待查", "至今", "县处级正职", "⚠️ 待确认姓名"),

    # ═══ 前任 ═══
    ("anyuan_li_shuiqing", "anyuan_party", "安源区委书记", "2021-08", "2025-05", "县处级正职",
     "2021年8月-2025年5月任安源区委书记"),
    ("anyuan_li_shuiqing", "px_npc", "萍乡市人大常委会副主任", "2025-05", "至今", "副厅级",
     "2025年5月任前公示：拟提名为设区市人大常委会副主任"),
    ("anyuan_li_shuiqing", "anyuan_gov", "萍乡武功山风景名胜区党委书记", "2016-08", "2021-08", "副厅级", ""),
    ("anyuan_li_shuiqing", "anyuan_gov", "萍乡武功山风景名胜区管委会主任", "约2015", "2016-09", "副厅级", ""),
    ("anyuan_li_shuiqing", "anyuan_gov", "芦溪县委常委、常务副县长", "约2012", "约2015", "副县级", ""),
    ("anyuan_li_shuiqing", "anyuan_gov", "芦溪县委常委、政法委书记", "约2010", "约2012", "副县级", ""),
    ("anyuan_li_shuiqing", "anyuan_gov", "芦溪县人民政府副县长", "约2006", "约2010", "副县级", ""),
    ("anyuan_li_shuiqing", "anyuan_gov", "莲花县人民政府县长助理", "约2004", "约2006", "副县级", ""),
    ("anyuan_li_shuiqing", "anyuan_gov", "莲花县荷塘乡党委书记、人大主席", "约2002", "约2004", "乡科级", ""),
    ("anyuan_li_shuiqing", "anyuan_gov", "莲花县神泉乡党委书记、人大主席", "约1999", "约2002", "乡科级", ""),
    ("anyuan_li_shuiqing", "anyuan_gov", "莲花县荷塘乡党委副书记、乡长", "约1997", "约1999", "乡科级", ""),
    ("anyuan_li_shuiqing", "anyuan_gov", "莲花县高洲乡党委副书记、乡长", "约1995", "约1997", "乡科级", ""),
    ("anyuan_li_shuiqing", "anyuan_gov", "共青团莲花县委书记", "约1993", "约1995", "乡科级", ""),
    ("anyuan_li_shuiqing", "anyuan_gov", "共青团莲花县委副书记", "1988-08", "约1993", "副科级",
     "1988年8月参加工作"),

    ("anyuan_kang_feng", "anyuan_party", "安源区委书记", "2019-08", "2021-08", "县处级正职", ""),
    ("anyuan_kang_feng", "anyuan_gov", "安源区长", "2016-09", "2021-08", "县处级正职",
     "2019年8月起书记区长一肩挑"),
    ("anyuan_kang_feng", "anyuan_gov", "安源区委副书记、区长提名人选", "2016-08", "2016-09", "县处级正职", ""),

    ("anyuan_li_zengyi", "anyuan_gov", "安源区委副书记、区长（前任）", "2020-07", "2021-08", "县处级正职",
     "接替康峰，邱伟的前任区长"),

    # ═══ 市级领导连接 ═══
    ("px_yu_zhengkun", "px_party", "萍乡市委书记", "2026-05", "至今", "正厅级", ""),
    ("px_fu_zhenghua", "px_gov", "萍乡市委副书记、市长", "2026-06", "至今", "正厅级", ""),
    ("px_bao_fengting", "px_party", "萍乡市委专职副书记", "2021-03", "至今", "副厅级", ""),
]

RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period)

    # ═══ 党政搭档（当前） ═══
    ("anyuan_qiu_wei", "anyuan_tang_yanhong", "强关系",
     "现任区委书记×区长（党政一把手、工作搭档）", "安源区", "2025-09至今"),

    # ═══ 党政搭档（前任） ═══
    ("anyuan_qiu_wei", "anyuan_li_shuiqing", "职务接替",
     "李水清→邱伟（安源区委书记前后任）", "中共安源区委", "2025-05"),
    ("anyuan_li_shuiqing", "anyuan_kang_feng", "职务接替",
     "康峰→李水清（安源区委书记前后任）", "中共安源区委", "2021-08"),
    ("anyuan_qiu_wei", "anyuan_li_zengyi", "职务接替",
     "邱伟接替黎增义任安源区长", "安源区人民政府", "2021-09"),

    # ═══ 区长×副书记 ═══
    ("anyuan_tang_yanhong", "anyuan_gong_yunhua", "弱关系（推定）",
     "区长×副书记（推定同级工作关系）", "安源区", "2025-09至今"),

    # ═══ 区委班子内部关系 ═══
    ("anyuan_qiu_wei", "anyuan_yuan_zian", "弱关系（推定）",
     "区委书记×常务副区长（上下级）", "安源区", "2023-至今"),
    ("anyuan_qiu_wei", "anyuan_huang_guohui", "弱关系（推定）",
     "区委书记×区委常委", "安源区", "2022-至今"),
    ("anyuan_qiu_wei", "anyuan_ye_jihui", "弱关系（推定）",
     "区委书记×纪委书记（同级监督关系）", "安源区", "2024-至今"),

    # ═══ 邱伟的省厅经历联系 ═══
    # 邱伟与龚云华曾在省级层面有交集（省直机关）？
    ("anyuan_qiu_wei", "anyuan_gong_yunhua", "弱关系（推定）",
     "邱伟（省民政厅/应急管理厅）×龚云华（省委统战部）—省直机关同僚", "江西省直", "约2010-2020"),
    # 这个交集是推定的，基于两人都在省直机关工作过

    # ═══ 龚云华跨县联系 ═══
    ("anyuan_gong_yunhua", "anyuan_li_shuiqing", "弱关系（推定）",
     "龚云华（莲花县常委/副县长）×李水清（莲花县人）—同籍萍乡莲花", "莲花县", "约2015-2019"),
    # 龚云华在莲花县任职期间，李水清是莲花人且在萍乡武功山任职

    # ═══ 汤艳红湘东→安源调动 ═══
    # 汤艳红从湘东区到萍乡市再到安源区
    # 邱伟从省厅下派到安源
    ("anyuan_tang_yanhong", "anyuan_qiu_wei", "强关系",
     "市传媒中心→安源区长 × 省厅下派→书记的党政搭档", "安源区", "2025-09至今"),

    # ═══ 市级领导关系 ═══
    ("anyuan_qiu_wei", "px_yu_zhengkun", "弱关系（推定）",
     "安源区委书记×萍乡市委书记（上下级）", "萍乡市", "2026-05至今"),
    ("anyuan_qiu_wei", "px_fu_zhenghua", "弱关系（推定）",
     "安源区委书记×萍乡市长（上下级）", "萍乡市", "2026-06至今"),
    ("anyuan_qiu_wei", "px_bao_fengting", "弱关系（推定）",
     "安源区委书记×萍乡市委副书记（上级指导关系）", "萍乡市", "2021-至今"),
    ("anyuan_tang_yanhong", "px_fu_zhenghua", "弱关系（推定）",
     "安源区长×萍乡市长（上下级）", "萍乡市", "2026-06至今"),
    ("anyuan_tang_yanhong", "px_yu_zhengkun", "弱关系（推定）",
     "安源区长×萍乡市委书记（上下级）", "萍乡市", "2026-05至今"),

    # ═══ 前任领导与市级联系 ═══
    ("anyuan_li_shuiqing", "px_bao_fengting", "弱关系（推定）",
     "安源区委书记×市委副书记", "萍乡市", "2021-2025"),

    # ═══ 康峰→李水清→邱伟 交接 ═══
    ("anyuan_kang_feng", "anyuan_li_shuiqing", "职务接替",
     "康峰→李水清（区委书记交接）", "中共安源区委", "2021-08"),
    ("anyuan_li_shuiqing", "anyuan_qiu_wei", "职务接替",
     "李水清→邱伟（区委书记交接）", "中共安源区委", "2025-05"),
]

# ── HELPERS ──

def esc(s):
    """Escape XML special chars."""
    if s is None: return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(pid):
    """Determine (r,g,b) and size for a person node."""
    for p in PERSONS:
        if p[0] == pid:
            post = p[9] or ""
            if "书记" in post and "副" not in post and "纪委" not in post:
                # Party secretary → red
                return (212, 52, 46, 20.0)
            elif ("区长" in post or "市长" in post) and "副" not in post:
                # Government head → blue
                return (51, 102, 204, 20.0)
            elif "副书记" in post:
                # Deputy secretary → dark red
                return (180, 60, 50, 16.0)
            elif "常务副" in post:
                # Executive deputy → blue
                return (51, 102, 204, 16.0)
            elif "纪委书记" in post or "纪委" in post:
                # Discipline → orange
                return (204, 119, 34, 14.0)
            elif "副区长" in post or "副县长" in post:
                # Deputy gov → light blue
                return (80, 130, 200, 14.0)
            elif "人大" in post:
                # NPC → purple
                return (130, 80, 180, 14.0)
            elif "政协" in post:
                # CPPCC → green
                return (100, 160, 100, 14.0)
            else:
                return (102, 102, 102, 12.0)
    return (102, 102, 102, 12.0)

def org_color(org_type):
    colors = {
        "党委": (85, 51, 51),
        "政府": (51, 68, 85),
        "人大": (100, 80, 130),
        "政协": (80, 110, 80),
        "纪委": (130, 80, 50),
        "公安": (51, 68, 85),
        "园区": (60, 90, 110),
    }
    return colors.get(org_type, (68, 68, 68))

# ── BUILD DATABASE ──

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
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
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
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
    print(f"✅ Database created: {DB_PATH}")

# ── BUILD GEXF ──

def generate_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    nodes_xml = []
    edges_xml = []
    edge_id = 0

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        label = p[1]
        r, g, b, sz = person_color(pid)
        nodes_xml.append(f"""\
    <node id="{pid}" label="{esc(label)}">
      <attvalues>
        <attvalue for="type" value="person"/>
        <attvalue for="role" value="{esc(p[9])}"/>
        <attvalue for="birth" value="{esc(p[4])}"/>
        <attvalue for="birthplace" value="{esc(p[5])}"/>
      </attvalues>
      <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>
      <viz:size value="{sz}"/>
      <viz:position x="0" y="0" z="0"/>
    </node>""")

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        label = o[1]
        r, g, b = org_color(o[2])
        nodes_xml.append(f"""\
    <node id="{oid}" label="{esc(label)}">
      <attvalues>
        <attvalue for="type" value="org"/>
        <attvalue for="org_type" value="{esc(o[2])}"/>
      </attvalues>
      <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>
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
    <description>安源区（萍乡市）领导班子工作关系网络 — 2026年7月</description>
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
    print("  安源区（萍乡市市辖区）领导班子工作关系网络")
    print(f"  区划代码: 360302 | 类别: 市辖区")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()
    print("\n✅ Done.")
