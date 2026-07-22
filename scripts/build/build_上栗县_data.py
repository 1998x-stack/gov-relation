#!/usr/bin/env python3
"""
上栗县（萍乡市下辖县）领导班子工作关系网络 — 数据构建脚本
Builds SQLite DB + GEXF graph for Shangli County leadership network.

Research date: 2026-07-15
Sources used:
  - baike.baidu.com (百度百科) - 利军简历
  - px.jxnews.com.cn (大江网/萍乡头条) - leadership changes, 副县长任命
  - jx.people.com.cn (人民网江西频道) - 李志猛人物专访
  - jx.news.cn (新华网江西频道) - 李志猛人物专访
  - jxrd.jxnews.com.cn (江西人大新闻网) - 人大代表进站履职
  - www.cs0799.com (萍乡城事网) - 县委常委会会议
  - www.newton.com.tw (中文百科) - 李昌清、肖妮娜简历
  - ruclaw.com (法律界) - 领导班子名单
  - m.jxnews.com.cn (手机江西网) - 县长任免
  - www.jendow.com.tw - 县委常委名单
  - sohu.com - 县委常委名单
  - hotelaah.com - 历任县委书记/县长
  - www.baike.com (快懂百科) - 肖妮娜升迁
  - china.huanqiu.com / thepaper.cn (澎湃新闻) - 利军简历
"""

import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data/database/上栗县_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "data/graph/上栗县_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# PERSONS
# Format: (id, name, gender, ethnicity, birth, birthplace,
#          education, party_join, work_start, current_post, current_org, source)
# ═══════════════════════════════════════════════════════════════════════

PERSONS = [
    # ═══ Current Top Leaders (as of mid-2026) ═══

    # 县委书记 利军（2021年8月任，仍在任）
    ("sl_li_jun", "利军", "男", "汉族", "1969-09", "江西安源",
     "江西省委党校在职研究生学历", "1995-03", "1990-08",
     "上栗县委书记", "中共上栗县委员会",
     "https://baike.baidu.com/item/%E5%88%A9%E5%86%9B/17575376"),

    # 县委副书记、县长 李志猛（2021年8月任代县长，后当选县长，仍在任）
    ("sl_li_zhimeng", "李志猛", "男", "汉族", "1982-09", "江西湘东",
     "大学学历", "2004-07", "2004-08",
     "上栗县委副书记、县长", "上栗县人民政府",
     "https://jx.people.com.cn/n2/2025/0119/c186330-41113428.html"),

    # ═══ Former Secretaries ═══

    # 前任县委书记 肖妮娜（2016年7月-2021年8月任；后升任上饶市委常委、组织部部长）
    ("sl_xiao_nina", "肖妮娜", "女", "汉族", "1975-02", "江西湘东",
     "江西省委党校在职研究生学历", "1999-10", "1992-08",
     "上饶市委常委、组织部部长（原上栗县委书记）", "中共上饶市委组织部",
     "https://www.baike.com/wikiid/7294781911548641315"),

    # 更前任县委书记 严荣华（-2016年7月任；后转任萍乡市人大内务司法委员会主任委员）
    ("sl_yan_ronghua", "严荣华", "男", "汉族", "1961-05", "江西莲花",
     "中央党校在职大学文化", "中共党员", "待查",
     "萍乡市人大内务司法委员会原主任委员（原上栗县委书记）", "萍乡市人民代表大会",
     "https://www.jendow.com.tw/wiki/%E5%9A%B4%E6%A6%AE%E8%8F%AF"),

    # ═══ Former County Mayors ═══

    # 前任县长 彭文华（肖妮娜搭档，任职至约2016年7月）
    ("sl_peng_wenhua", "彭文华", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "原上栗县县长（2015年前后在任）", "上栗县人民政府",
     "https://baike.so.com/doc/6665040-6878868.html"),

    # ═══ Current Standing Committee / 县委常委 as of 2024-2026 ═══

    # 县委副书记、常务副县长 李昌清（常委→常务副县长）
    ("sl_li_changqing", "李昌清", "男", "汉族", "1976-01", "江西上栗",
     "在职大学学历", "1999-03", "1995-10",
     "上栗县委副书记、常务副县长", "上栗县人民政府",
     "https://www.newton.com.tw/wiki/%E6%9D%8E%E6%98%8C%E6%B8%85/20227377"),

    # 县委副书记 李夙颖（曾任副书记）
    ("sl_li_suying", "李夙颖", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县委副书记", "中共上栗县委员会",
     "http://www.cs0799.com/portal.php?aid=88910&mod=view"),

    # 县委常委、县纪委书记、县监委主任 叶润锋
    ("sl_ye_runfeng", "叶润锋", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县委常委、县纪委书记、县监委主任", "上栗县纪委监委",
     "https://px.jxnews.com.cn/system/2022/09/09/019772983.shtml"),

    # 县委常委、统战部部长 陈忠林
    ("sl_chen_zhonglin", "陈忠林", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县委常委、统战部部长", "中共上栗县委统战部",
     "http://www.cs0799.com/portal.php?aid=88910&mod=view"),

    # 县委常委、政法委书记 王均洪
    ("sl_wang_junhong", "王均洪", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县委常委、政法委书记", "中共上栗县委政法委",
     "https://ecywang.com/pic/%e6%b1%9f%e8%a5%bf%e4%b8%8a%e6%a0%97%e5%8e%bf%e5%a7%94%e4%b9%a6%e8%ae%b0/"),

    # 县委常委 漆宇晴
    ("sl_qi_yuqing", "漆宇晴", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县委常委", "中共上栗县委员会",
     "http://www.cs0799.com/portal.php?aid=99193&mod=view"),

    # 县委常委 易军
    ("sl_yi_jun", "易军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县委常委", "中共上栗县委员会",
     "http://www.cs0799.com/portal.php?aid=99193&mod=view"),

    # 县委常委 卢政武
    ("sl_lu_zhengwu", "卢政武", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县委常委", "中共上栗县委员会",
     "https://px.jxnews.com.cn/system/2024/10/15/020665028.shtml"),

    # 原县委常委 易冬梅（女，县委宣传部部长、曾任职务）
    ("sl_yi_dongmei", "易冬梅", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县委常委（曾任）", "中共上栗县委员会",
     "https://www.jendow.com.tw/wiki/%E4%B8%8A%E6%A0%97%E7%B8%A3"),

    # 原县委常委 肖根铭
    ("sl_xiao_genming", "肖根铭", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县委常委（曾任）", "中共上栗县委员会",
     "https://www.jendow.com.tw/wiki/%E4%B8%8A%E6%A0%97%E7%B8%A3"),

    # 原县委常委 廖宇波
    ("sl_liao_yubo", "廖宇波", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县委常委（曾任）", "中共上栗县委员会",
     "https://www.jendow.com.tw/wiki/%E4%B8%8A%E6%A0%97%E7%B8%A3"),

    # 原县委常委 张达彪（曾任常务副县长）
    ("sl_zhang_dabiao", "张达彪", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "原上栗县委常委、常务副县长", "上栗县人民政府",
     "https://www.jendow.com.tw/wiki/%E4%B8%8A%E6%A0%97%E7%B8%A3"),

    # 原县委常委 熊渊
    ("sl_xiong_yuan", "熊渊", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县委常委（曾任）", "中共上栗县委员会",
     "https://www.jendow.com.tw/wiki/%E4%B8%8A%E6%A0%97%E7%B8%A3"),

    # 原县委常委 魏逵
    ("sl_wei_kui", "魏逵", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县委常委（曾任）", "中共上栗县委员会",
     "https://www.jendow.com.tw/wiki/%E4%B8%8A%E6%A0%97%E7%B8%A3"),

    # 原县委常委 宋崇信
    ("sl_song_chongxin", "宋崇信", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县委常委（曾任）", "中共上栗县委员会",
     "https://www.jendow.com.tw/wiki/%E4%B8%8A%E6%A0%97%E7%B8%A3"),

    # ═══ Current County Government Deputy Heads (副县长 as of 2024-2025) ═══

    # 副县长 王登辉（2024年6月任）
    ("sl_wang_denghui", "王登辉", "男", "汉族", "1985-05", "待查",
     "博士研究生", "中共党员", "待查",
     "上栗县副县长", "上栗县人民政府",
     "https://px.jxnews.com.cn/system/2024/06/18/020539383.shtml"),

    # 副县长 王均礼（2024年6月任）
    ("sl_wang_junli", "王均礼", "男", "汉族", "1979-06", "待查",
     "中央党校在职大学", "中共党员", "待查",
     "上栗县副县长", "上栗县人民政府",
     "https://px.jxnews.com.cn/system/2024/06/18/020539383.shtml"),

    # 副县长 罗俊湘（2024年12月任）
    ("sl_luo_junxiang", "罗俊湘", "男", "汉族", "1979-06", "待查",
     "在职研究生", "中共党员", "待查",
     "上栗县副县长", "上栗县人民政府",
     "https://px.jxnews.com.cn/system/2024/12/28/020743901.shtml"),

    # 副县长 程慧平（2024年12月任）
    ("sl_cheng_huiping", "程慧平", "男", "汉族", "1984-08", "待查",
     "博士研究生", "中共党员", "待查",
     "上栗县副县长", "上栗县人民政府",
     "https://px.jxnews.com.cn/system/2024/12/28/020743901.shtml"),

    # 副县长 吴菊芳（女，2021年1月任）
    ("sl_wu_jufang", "吴菊芳", "女", "汉族", "1983-09", "江西安源",
     "大学学历", "中共党员", "2006-08",
     "上栗县副县长", "上栗县人民政府",
     "https://px.jxnews.com.cn/system/2021/01/23/019170531.shtml"),

    # 副县长 陈强（民盟，2021年1月任）
    ("sl_chen_qiang", "陈强", "男", "汉族", "1984-11", "江西安源",
     "大学学历", "民盟盟员", "2007-09",
     "上栗县副县长", "上栗县人民政府",
     "https://px.jxnews.com.cn/system/2021/01/23/019170531.shtml"),

    # 副县长 何宏寓（政府党组成员）
    ("sl_he_hongyu", "何宏寓", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县人民政府党组成员、副县长", "上栗县人民政府",
     "http://www.pxsxsy.com/m/article.php?id=24788"),

    # 原副县长 曾育平（挂职，2021年1月至2024年12月任，已辞职）
    ("sl_zeng_yuping", "曾育平", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "原上栗县副县长（挂职，2024年12月辞职）", "上栗县人民政府",
     "https://px.jxnews.com.cn/system/2024/12/28/020743901.shtml"),

    # 原副县长 徐琦（已辞职，2024年12月）
    ("sl_xu_qi", "徐琦", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "原上栗县副县长（2024年12月辞职）", "上栗县人民政府",
     "https://px.jxnews.com.cn/system/2024/12/28/020743901.shtml"),

    # 原副县长 严鹏程（2024年6月辞职）
    ("sl_yan_pengcheng", "严鹏程", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "原上栗县副县长（2024年6月辞职）", "上栗县人民政府",
     "https://px.jxnews.com.cn/system/2024/06/18/020539383.shtml"),

    # 原副县长 温卫兵（2024年6月辞职）
    ("sl_wen_weibing", "温卫兵", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "原上栗县副县长（2024年6月辞职）", "上栗县人民政府",
     "https://px.jxnews.com.cn/system/2024/06/18/020539383.shtml"),

    # 原副县长 尹绍萍（曾任副县长）
    ("sl_yin_shaoping", "尹绍萍", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "原上栗县副县长", "上栗县人民政府",
     "https://www.cs0799.com/portal.php?aid=99193&mod=view"),

    # ═══ 县人大常委会 ═══

    # 县人大常委会主任 王纯（2020年5月当选）
    ("sl_wang_chun", "王纯", "男", "汉族", "1965-06", "待查",
     "待查", "中共党员", "待查",
     "上栗县人大常委会党组书记、主任", "上栗县人大常委会",
     "https://px.jxnews.com.cn/system/2020/05/27/018907020.shtml"),

    # 县人大常委会副主任 易冬梅（曾任县委常委、后任人大副主任）
    ("sl_yi_dongmei_npc", "易冬梅", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县人大常委会副主任", "上栗县人大常委会",
     "http://www.pxsxsy.com/m/article.php?id=25205"),

    # 县人大常委会副主任 杨庆康
    ("sl_yang_qingkang", "杨庆康", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县人大常委会副主任", "上栗县人大常委会",
     "http://www.pxsxsy.com/m/article.php?id=25205"),

    # 县人大常委会副主任 李频
    ("sl_li_pin", "李频", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县人大常委会副主任", "上栗县人大常委会",
     "http://www.pxsxsy.com/m/article.php?id=25205"),

    # 县人大常委会副主任 黄贤海
    ("sl_huang_xianhai", "黄贤海", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县人大常委会副主任", "上栗县人大常委会",
     "http://www.pxsxsy.com/m/article.php?id=25205"),

    # 县人大常委会副主任 李永林
    ("sl_li_yonglin", "李永林", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县人大常委会副主任", "上栗县人大常委会",
     "http://www.pxsxsy.com/m/article.php?id=25205"),

    # 县人大常委会副主任 黄绍良
    ("sl_huang_shaoliang", "黄绍良", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县人大常委会副主任", "上栗县人大常委会",
     "http://www.pxsxsy.com/m/article.php?id=25205"),

    # ═══ 县政协 ═══

    # 县政协主席 关翠屏（任职多年）
    ("sl_guan_cuiping", "关翠屏", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县政协党组书记、主席", "政协上栗县委员会",
     "https://px.jxnews.com.cn/system/2023/02/21/019955839.shtml"),

    # 县政协副主席 况德萍
    ("sl_kuang_deping", "况德萍", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县政协副主席", "政协上栗县委员会",
     "https://px.jxnews.com.cn/system/2021/09/23/019402892.shtml"),

    # 县政协副主席 王涛
    ("sl_wang_tao", "王涛", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县政协副主席", "政协上栗县委员会",
     "https://px.jxnews.com.cn/system/2021/09/23/019402892.shtml"),

    # 县政协副主席 陈新发
    ("sl_chen_xinfa", "陈新发", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "上栗县政协党组成员、副主席", "政协上栗县委员会",
     "https://px.jxnews.com.cn/system/2023/02/22/019957577.shtml"),

    # ═══ 其他重要人物 ═══

    # 原人大主任 兰先湖（2015年前后在任）
    ("sl_lan_xianhu", "兰先湖", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "原上栗县人大常委会主任", "上栗县人大常委会",
     "https://baike.so.com/doc/6665040-6878868.html"),
]

# ═══════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# Format: (id, name, type, level, parent, location)
# ═══════════════════════════════════════════════════════════════════════

ORGANIZATIONS = [
    # 县级四套班子
    ("org_sl_county_party", "中共上栗县委员会", "党委", "县级", "中共萍乡市委", "萍乡市上栗县上栗镇"),
    ("org_sl_county_gov", "上栗县人民政府", "政府", "县级", "萍乡市人民政府", "萍乡市上栗县上栗镇"),
    ("org_sl_npc", "上栗县人大常委会", "人大", "县级", "萍乡市人大常委会", "萍乡市上栗县上栗镇"),
    ("org_sl_cppcc", "政协上栗县委员会", "政协", "县级", "政协萍乡市委员会", "萍乡市上栗县上栗镇"),

    # 纪检监察
    ("org_sl_discipline", "上栗县纪律检查委员会/监察委员会", "党委", "县级", "中共上栗县委/萍乡市纪委监委", "萍乡市上栗县上栗镇"),

    # 党委部门
    ("org_sl_united_front", "中共上栗县委统战部", "党委", "县级", "中共上栗县委", "萍乡市上栗县上栗镇"),
    ("org_sl_political_legal", "中共上栗县委政法委", "党委", "县级", "中共上栗县委", "萍乡市上栗县上栗镇"),

    # 上级机构
    ("org_pingxiang_party", "中共萍乡市委", "党委", "地市级", "中共江西省委", "萍乡市"),
    ("org_pingxiang_gov", "萍乡市人民政府", "政府", "地市级", "江西省人民政府", "萍乡市"),
    ("org_pingxiang_npc", "萍乡市人大常委会", "人大", "地市级", "", "萍乡市"),
    ("org_pingxiang_cppcc", "政协萍乡市委员会", "政协", "地市级", "", "萍乡市"),
    ("org_pingxiang_discipline", "萍乡市纪委监委", "党委", "地市级", "中共萍乡市委", "萍乡市"),

    # 其他关联机构
    ("org_shangrao_party_org", "中共上饶市委组织部", "党委", "地市级", "中共上饶市委", "上饶市"),
    ("org_pingxiang_economic_dev", "萍乡经济技术开发区", "政府", "地市级", "萍乡市人民政府", "萍乡市"),
    ("org_wugongshan", "武功山风景名胜区", "事业单位", "地市级", "萍乡市人民政府", "萍乡市武功山"),
    ("org_anyuan_district", "安源区人民政府", "政府", "县级", "萍乡市人民政府", "萍乡市安源区"),
    ("org_xiangdong_district", "湘东区人民政府", "政府", "县级", "萍乡市人民政府", "萍乡市湘东区"),
    ("org_pingxiang_gov_office", "萍乡市人民政府办公室", "政府", "地市级", "萍乡市人民政府", "萍乡市"),
]

# ═══════════════════════════════════════════════════════════════════════
# POSITIONS (career history)
# Format: (person_id, org_id, title, start_date, end_date, rank, note)
# ═══════════════════════════════════════════════════════════════════════

POSITIONS = [
    # ── 利军（县委书记） ──
    ("sl_li_jun", "org_sl_county_party", "上栗县委书记", "2021-08", "至今", "正县级", "2021年8月任上栗县委书记至今"),
    ("sl_li_jun", "org_sl_county_gov", "上栗县委副书记、县长", "2016-09", "2021-08", "正县级", "2016年9月当选县长，2021年8月辞任"),
    ("sl_li_jun", "org_sl_county_gov", "上栗县委副书记、代县长", "2016-08", "2016-09", "正县级", "2016年8月任代县长"),
    ("sl_li_jun", "org_sl_county_party", "上栗县委副书记", "2016-07", "2016-08", "副县级", "2016年7月任上栗县委副书记"),
    ("sl_li_jun", "org_pingxiang_economic_dev", "萍乡经济技术开发区党委委员、管委会副主任", "待查", "2016-07", "副县级", "任上栗县委副书记前任职"),
    ("sl_li_jun", "org_anyuan_district", "萍乡市安源区（早期职务待查）", "待查", "待查", "待查", "1969年9月生，江西安源人"),

    # ── 李志猛（县长） ──
    ("sl_li_zhimeng", "org_sl_county_gov", "上栗县委副书记、县长", "2021-09", "至今", "正县级", "2021年9月当选县长"),
    ("sl_li_zhimeng", "org_sl_county_gov", "上栗县代县长", "2021-08", "2021-09", "正县级", "2021年8月8日任命为代县长"),
    ("sl_li_zhimeng", "org_sl_county_party", "上栗县委副书记（正县级）", "2019-06", "2021-08", "正县级", "2019年6月任上栗县委副书记"),
    ("sl_li_zhimeng", "org_pingxiang_gov_office", "萍乡市委副秘书长、政研室主任", "待查", "2019-06", "正县级", "任上栗县委副书记前任职"),
    ("sl_li_zhimeng", "org_pingxiang_gov_office", "萍乡市委办副主任", "待查", "待查", "副县级", ""),
    ("sl_li_zhimeng", "org_pingxiang_gov_office", "共青团萍乡市委副书记", "待查", "待查", "副县级", ""),
    ("sl_li_zhimeng", "org_pingxiang_gov_office", "萍乡市委办公室调研科科长", "待查", "待查", "正科级", ""),
    ("sl_li_zhimeng", "org_pingxiang_gov_office", "萍乡市委组织部科长", "待查", "待查", "正科级", ""),
    ("sl_li_zhimeng", "org_anyuan_district", "萍乡市安源区五陂镇镇长助理", "2004-08", "待查", "科员级", "2004年8月参加工作，起点职务"),
    ("sl_li_zhimeng", "org_sl_county_party", "上栗县委副书记（正县级）", "2019-06", "2021-08", "正县级", "2019年6月12日陪同观摩团报道显示已任职"),

    # ── 肖妮娜（前任县委书记） ──
    ("sl_xiao_nina", "org_shangrao_party_org", "上饶市委常委、组织部部长", "2021-08", "至今", "副厅级", "2021年8月后升任"),
    ("sl_xiao_nina", "org_sl_county_party", "上栗县委书记", "2016-07", "2021-08", "正县级", "2016年7月28日上任，至2021年8月"),
    ("sl_xiao_nina", "org_wugongshan", "萍乡武功山风景名胜区党委书记/市政府副秘书长", "2015-01", "2016-07", "正县级", "任武功山党委书记兼市政府副秘书长"),
    ("sl_xiao_nina", "org_wugongshan", "武功山风景名胜区党委委员、管委会副主任（正县级）", "待查", "2015-01", "正县级", ""),
    ("sl_xiao_nina", "org_pingxiang_gov_office", "萍乡市妇联副主席", "待查", "待查", "副县级", ""),
    ("sl_xiao_nina", "org_xiangdong_district", "湘东区广寒寨乡党委副书记、乡长", "待查", "待查", "正科级", ""),
    ("sl_xiao_nina", "org_xiangdong_district", "湘东区白竺乡党委副书记、乡长", "待查", "待查", "正科级", ""),
    ("sl_xiao_nina", "org_xiangdong_district", "湘东区工会副主席", "待查", "待查", "副科级", "1975年2月生，江西湘东人"),

    # ── 严荣华（更前任县委书记） ──
    ("sl_yan_ronghua", "org_pingxiang_npc", "萍乡市人大内务司法委员会主任委员", "2016-10", "待查", "正县级", "2016年10月任"),
    ("sl_yan_ronghua", "org_sl_county_party", "上栗县委书记", "待查", "2016-07", "正县级", "2016年7月28日离任"),
    ("sl_yan_ronghua", "org_sl_county_gov", "上栗县县长（曾任）", "待查", "待查", "正县级", "1961年5月生，江西莲花人"),

    # ── 彭文华（前任县长） ──
    ("sl_peng_wenhua", "org_sl_county_gov", "上栗县县长", "待查", "~2016-07", "正县级", "2015年前后在任，2016年7月由利军接替"),
    ("sl_peng_wenhua", "org_sl_county_party", "上栗县委副书记", "待查", "待查", "副县级", ""),

    # ── 李昌清（县委副书记、常务副县长） ──
    ("sl_li_changqing", "org_sl_county_gov", "上栗县委副书记、常务副县长", "2021", "至今", "副县级", "2021年任县委副书记、常务副县长"),
    ("sl_li_changqing", "org_sl_county_gov", "上栗县委常委、副县长", "2020-08", "2021", "副县级", "2020年8月任副县长"),
    ("sl_li_changqing", "org_sl_united_front", "上栗县委常委、统战部部长兼民宗局长", "2019-12", "2020-08", "副县级", "兼县民宗局局长"),
    ("sl_li_changqing", "org_sl_united_front", "上栗县委常委、统战部部长兼产业园党工委书记", "2017-08", "2019-12", "副县级", "兼县产业园党工委书记"),
    ("sl_li_changqing", "org_sl_county_party", "上栗县委常委", "2016-11", "2017-08", "副县级", "2016年11月任县委常委"),
    ("sl_li_changqing", "org_pingxiang_party", "萍乡市援疆干部（新疆克州阿克陶县委组织部副部长）", "待查", "待查", "副县级", "援疆工作经历"),
    ("sl_li_changqing", "org_sl_county_party", "上栗县委组织部部务会成员", "待查", "待查", "正科级", "早期职务"),
    ("sl_li_changqing", "org_sl_county_party", "上栗县委常委", "2016-11", "至今", "副县级", "1976年1月生，江西上栗人"),

    # ── 李夙颖（县委副书记） ──
    ("sl_li_suying", "org_sl_county_party", "上栗县委副书记", "待查", "至今", "副县级", "分管农业、农村等工作"),

    # ── 叶润锋（县纪委书记） ──
    ("sl_ye_runfeng", "org_sl_discipline", "上栗县委常委、县纪委书记、县监委主任", "2021", "至今", "副县级", ""),
    ("sl_ye_runfeng", "org_sl_discipline", "上栗县委巡察工作领导小组组长", "2021", "至今", "副县级", "兼任"),

    # ── 陈忠林（统战部部长） ──
    ("sl_chen_zhonglin", "org_sl_united_front", "上栗县委常委、统战部部长", "待查", "至今", "副县级", ""),

    # ── 王均洪（政法委书记） ──
    ("sl_wang_junhong", "org_sl_political_legal", "上栗县委常委、政法委书记", "待查", "至今", "副县级", ""),

    # ── 张达彪（原常务副县长） ──
    ("sl_zhang_dabiao", "org_sl_county_gov", "上栗县委常委、常务副县长", "~2016", "2020-08", "副县级", "2020年8月免去副县长职务"),

    # ── 王纯（县人大常委会主任） ──
    ("sl_wang_chun", "org_sl_npc", "上栗县人大常委会党组书记、主任", "2020-05", "至今", "正县级", "2020年5月当选"),
    ("sl_wang_chun", "org_pingxiang_economic_dev", "萍乡经济技术开发区党工委委员、管委会副主任（正县级）", "待查", "2020-05", "正县级", "1965年6月生"),

    # ── 关翠屏（县政协主席） ──
    ("sl_guan_cuiping", "org_sl_cppcc", "上栗县政协党组书记、主席", "2016", "至今", "正县级", "自2016年起任政协主席"),

    # ── 吴菊芳（副县长） ──
    ("sl_wu_jufang", "org_sl_county_gov", "上栗县副县长", "2021-01", "至今", "副县级", "2021年1月22日任命"),
    ("sl_wu_jufang", "org_xiangdong_district", "湘东区麻山镇党委书记、麻山生态新区主任", "待查", "2021-01", "正科级", ""),
    ("sl_wu_jufang", "org_xiangdong_district", "湘东区广寒寨乡党委书记", "待查", "待查", "正科级", ""),
    ("sl_wu_jufang", "org_xiangdong_district", "共青团湘东区委书记", "待查", "待查", "正科级", ""),
    ("sl_wu_jufang", "org_xiangdong_district", "湘东区下埠镇镇长助理", "2006-08", "待查", "科员级", "1983年9月生，江西安源人"),

    # ── 陈强（副县长，民盟） ──
    ("sl_chen_qiang", "org_sl_county_gov", "上栗县副县长", "2021-01", "至今", "副县级", "2021年1月22日任命"),
    ("sl_chen_qiang", "org_pingxiang_gov", "萍乡市人社局就业促进和失业保险科科长", "待查", "2021-01", "正科级", "1984年11月生，江西安源人"),
    ("sl_chen_qiang", "org_xiangdong_district", "湘东区白竺乡副乡长", "待查", "待查", "副科级", ""),

    # ── 王登辉（副县长，2024年6月任） ──
    ("sl_wang_denghui", "org_sl_county_gov", "上栗县副县长", "2024-06", "至今", "副县级", "2024年6月18日任命，博士研究生"),
    ("sl_wang_junli", "org_sl_county_gov", "上栗县副县长", "2024-06", "至今", "副县级", "2024年6月18日任命"),
    ("sl_luo_junxiang", "org_sl_county_gov", "上栗县副县长", "2024-12", "至今", "副县级", "2024年12月28日任命"),
    ("sl_cheng_huiping", "org_sl_county_gov", "上栗县副县长", "2024-12", "至今", "副县级", "2024年12月28日任命，博士研究生"),

    # ── 曾育平（原副县长，挂职） ──
    ("sl_zeng_yuping", "org_sl_county_gov", "上栗县副县长（挂职）", "2020-09", "2024-12", "副县级", "2024年12月28日辞职"),
    ("sl_xu_qi", "org_sl_county_gov", "上栗县副县长", "待查", "2024-12", "副县级", "2024年12月28日辞职"),
    ("sl_yan_pengcheng", "org_sl_county_gov", "上栗县副县长", "待查", "2024-06", "副县级", "2024年6月18日辞职"),
    ("sl_wen_weibing", "org_sl_county_gov", "上栗县副县长", "待查", "2024-06", "副县级", "2024年6月18日辞职"),
]

# ═══════════════════════════════════════════════════════════════════════
# RELATIONSHIPS (work overlaps, connections)
# Format: (person_a, person_b, type, context, overlap_org, overlap_period)
# ═══════════════════════════════════════════════════════════════════════

RELATIONSHIPS = [
    # ── 县委书记 ↔ 县长（党政一把手） ──
    ("sl_li_jun", "sl_li_zhimeng", "上下级", "利军（书记）与李志猛（县长）党政搭档", "上栗县委/上栗县政府", "2021-08至今"),

    # ── 利军与肖妮娜（前后任书记） ──
    ("sl_li_jun", "sl_xiao_nina", "交接", "利军接替肖妮娜任上栗县委书记", "中共上栗县委", "2021-08"),

    # ── 肖妮娜与利军（书记+县长搭档） ──
    ("sl_xiao_nina", "sl_li_jun", "上下级", "肖妮娜（书记）与利军（县长）党政搭档", "上栗县委/上栗县政府", "2016-09至2021-08"),

    # ── 利军与李志猛（前后任县长） ──
    ("sl_li_jun", "sl_li_zhimeng", "交接", "李志猛接替利军任县长", "上栗县政府", "2021-08"),

    # ── 肖妮娜与严荣华（前后任书记） ──
    ("sl_xiao_nina", "sl_yan_ronghua", "交接", "肖妮娜接替严荣华任上栗县委书记", "中共上栗县委", "2016-07"),

    # ── 利军与彭文华（前后任县长） ──
    ("sl_li_jun", "sl_peng_wenhua", "交接", "利军接替彭文华任上栗县县长", "上栗县政府", "2016-07"),

    # ── 李志猛与李昌清（县委正副书记） ──
    ("sl_li_zhimeng", "sl_li_changqing", "同事", "李志猛（县长/副书记）与李昌清（副书记/常务副县长）在县政府共事", "上栗县政府", "2021至今"),

    # ── 李志猛与李夙颖（县委副书记同事） ──
    ("sl_li_zhimeng", "sl_li_suying", "同事", "李志猛与李夙颖同为县委副书记", "中共上栗县委", "待查至今"),

    # ── 县委常委间关系 ──
    ("sl_li_changqing", "sl_ye_runfeng", "同事", "李昌清（常务副县长）与叶润锋（纪委书记）同为县委常委", "上栗县委常委班子", "2021至今"),
    ("sl_li_changqing", "sl_chen_zhonglin", "同事", "李昌清与陈忠林（统战部长）同为县委常委", "上栗县委常委班子", "待查至今"),
    ("sl_li_changqing", "sl_wang_junhong", "同事", "李昌清与王均洪（政法委书记）同为县委常委", "上栗县委常委班子", "待查至今"),
    ("sl_li_changqing", "sl_qi_yuqing", "同事", "李昌清与漆宇晴同为县委常委", "上栗县委常委班子", "待查至今"),
    ("sl_li_changqing", "sl_yi_jun", "同事", "李昌清与易军同为县委常委", "上栗县委常委班子", "待查至今"),
    ("sl_li_changqing", "sl_lu_zhengwu", "同事", "李昌清与卢政武同为县委常委", "上栗县委常委班子", "2024至今"),

    # ── 张达彪与李昌清交接 ──
    ("sl_zhang_dabiao", "sl_li_changqing", "交接", "李昌清接替张达彪任副县长", "上栗县政府", "2020-08"),

    # ── 四套班子领导关系 ──
    ("sl_li_jun", "sl_wang_chun", "同事", "利军（书记）与王纯（人大主任）同在四套班子", "上栗县四套班子", "2020至今"),
    ("sl_li_jun", "sl_guan_cuiping", "同事", "利军（书记）与关翠屏（政协主席）同在四套班子", "上栗县四套班子", "2021至今"),
    ("sl_li_zhimeng", "sl_wang_chun", "同事", "李志猛（县长）与王纯（人大主任）同在四套班子", "上栗县四套班子", "2021至今"),
    ("sl_li_zhimeng", "sl_guan_cuiping", "同事", "李志猛（县长）与关翠屏（政协主席）同在四套班子", "上栗县四套班子", "2021至今"),

    # ── 肖妮娜与关翠屏（多年搭班） ──
    ("sl_xiao_nina", "sl_guan_cuiping", "同事", "肖妮娜（书记）与关翠屏（政协主席）搭班多年", "上栗县四套班子", "2016-07至2021-08"),

    # ── 原领导班子（2016年） ──
    ("sl_yan_ronghua", "sl_peng_wenhua", "上下级", "严荣华（书记）与彭文华（县长）党政搭档", "上栗县委/上栗县政府", "~2016"),

    # ── 副县长同事关系 ──
    ("sl_wu_jufang", "sl_chen_qiang", "同事", "吴菊芳与陈强同于2021年1月获任副县长", "上栗县政府", "2021至今"),
    ("sl_wang_denghui", "sl_wang_junli", "同事", "王登辉与王均礼同于2024年6月获任副县长", "上栗县政府", "2024-06至今"),
    ("sl_luo_junxiang", "sl_cheng_huiping", "同事", "罗俊湘与程慧平同于2024年12月获任副县长", "上栗县政府", "2024-12至今"),
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
    """Color by role: red=secretary, blue=gov leader, orange=other."""
    red_ids = {"sl_li_jun"}  # 县委书记
    blue_ids = {
        "sl_li_zhimeng", "sl_peng_wenhua",  # 县长/前县长
        "sl_li_changqing", "sl_wang_denghui", "sl_wang_junli",
        "sl_luo_junxiang", "sl_cheng_huiping", "sl_wu_jufang",
        "sl_chen_qiang", "sl_he_hongyu", "sl_zeng_yuping",
        "sl_xu_qi", "sl_yan_pengcheng", "sl_wen_weibing",
        "sl_yin_shaoping", "sl_zhang_dabiao",
    }
    if person_id in red_ids:
        return "255,50,50"
    elif person_id in blue_ids:
        return "50,100,255"
    else:
        return "255,165,0"  # orange for other roles

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

    for p in PERSONS:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", p)

    for o in ORGANIZATIONS:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""", o)

    for pos in POSITIONS:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?,?,?,?,?,?,?)""", pos)

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

    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Government Network Investigator</creator>')
    lines.append('    <description>上栗县（萍乡市）领导班子工作关系网络</description>')
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
        sz = "20.0" if pid in ("sl_li_jun", "sl_li_zhimeng") else "12.0"
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
    print("  上栗县领导班子工作关系网络 — 数据构建")
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
