#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 乐平市 (Leping, Jiangxi) leadership network.

归口地区: 江西省景德镇市代管县级市
"""

import sqlite3
import os
from datetime import date

DB_DIR = "data/database"
GRAPH_DIR = "data/graph"
DB_PATH = os.path.join(DB_DIR, "乐平市_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, "乐平市_network.gexf")
TODAY = "2026-07-15"

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════
# DATA — hardcoded research data
# ═══════════════════════════════════════════════════════════════════════════

persons = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ── 市委领导 ──
    ("leping_lin_weichun", "林卫春", "男", "汉族", "1975-02", "江西浮梁", "大学/工程硕士",
     "2002-03", "1994-08",
     "景德镇市委常委、乐平市委书记", "中共景德镇市委/中共乐平市委",
     "https://baike.so.com/doc/5034256-5260735.html"),

    ("leping_wu_yan", "吴艳", "男", "汉族", "1974-07", "江西鄱阳", "大学",
     "2003-06", "1997-07",
     "乐平市委副书记、市长", "乐平市人民政府",
     "https://baike.so.com/doc/6926502-32424748.html"),

    ("leping_xie_qiuhua", "谢秋华", "男", "汉族", "", "江西（推测）", "",
     "", "",
     "乐平市委副书记", "中共乐平市委",
     "https://www.thepaper.cn/newsDetail_forward_14312498"),

    # ── 市委常委 ──
    ("leping_wang_lizhen", "王枥珍", "女", "汉族", "", "", "",
     "", "",
     "乐平市委常委、组织部部长", "中共乐平市委组织部",
     "https://jxjdz.jxnews.com.cn/system/2024/12/08/020722768.shtml"),

    ("leping_zou_guoliang", "邹国良", "男", "汉族", "1976-12", "江西乐平", "中央党校大学",
     "中共党员", "",
     "乐平市委常委、宣传部部长（兼市工信局党组书记、局长）", "中共乐平市委宣传部",
     "https://www.newton.com.tw/wiki/%E9%84%92%E5%9C%8B%E8%89%AF/19875050"),

    ("leping_zhou_jun", "周军", "男", "汉族", "", "", "",
     "", "",
     "乐平市委常委、人武部政治委员", "乐平市人武部",
     "https://www.thepaper.cn/newsDetail_forward_14312498"),

    ("leping_cheng_mingbo", "程明波", "男", "汉族", "1975-06", "", "中央党校大学",
     "中共党员", "",
     "乐平市委常委、政法委书记", "中共乐平市委政法委",
     "https://www.newton.com.tw/wiki/%E7%A8%8B%E6%98%8E%E6%B3%A2/7527346"),

    ("leping_han_wei", "韩伟", "男", "汉族", "1967-02", "江西乐平", "本科",
     "1994-10", "1985-03",
     "乐平市委常委（负责农业和农村工作）", "中共乐平市委",
     "https://baike.baidu.com/item/%E9%9F%A9%E4%BC%9F/56185078"),

    ("leping_liu_xuefei", "刘学飞", "男", "汉族", "1983-11", "安徽亳州", "大学",
     "2003-11", "2006-07",
     "乐平市委常委、市纪委书记、市监委主任", "中共乐平市纪委/乐平市监委",
     "https://baike.baidu.com/item/%E5%88%98%E5%AD%A6%E9%A3%9E/22775733"),

    ("leping_ding_wei", "丁巍", "女", "汉族", "1978-10", "江西万年", "大学本科",
     "2000-08", "1997-08",
     "乐平市委常委、常务副市长（2024年3月被查）", "乐平市人民政府",
     "https://www.nbd.com.cn/articles/2024-03-21/3289507.html"),

    ("leping_dong_bin", "董斌", "男", "汉族", "", "", "",
     "", "",
     "乐平市委常委、统战部部长, 市政协党组副书记", "中共乐平市委统战部",
     "http://tzb.jdzol.com/html/jczx/lptz/4902.html"),

    ("leping_huang_cheng", "黄城", "男", "汉族", "", "", "",
     "", "",
     "乐平市委常委、副市长, 临港镇党委书记", "乐平市人民政府",
     "https://www.thepaper.cn/newsDetail_forward_15092494"),

    ("leping_wang_wei", "汪维", "男", "汉族", "1983-10", "江西浮梁", "在职本科",
     "2003-02", "2000-12",
     "乐平市委常委、副市长", "乐平市人民政府",
     "https://www.newton.com.tw/wiki/%E6%B1%AA%E7%B6%AD/58260943"),

    ("leping_dai_rong", "戴戎", "男", "汉族", "1988-04", "江西泰和", "全日制大学",
     "2012-08", "2009-08",
     "乐平市委常委、统战部部长", "中共乐平市委统战部",
     "https://www.newton.com.tw/wiki/%E6%88%B4%E6%88%8E/63006988"),

    # ── 政府副市长（非常委） ──
    ("leping_li_xiaobin", "李晓滨", "男", "汉族", "", "", "",
     "", "",
     "乐平市副市长", "乐平市人民政府",
     "https://www.thepaper.cn/newsDetail_forward_15092494"),

    ("leping_zhu_liuying", "朱柳英", "女", "汉族", "", "", "",
     "", "",
     "乐平市副市长（分管卫健、教育）", "乐平市人民政府",
     "https://www.thepaper.cn/newsDetail_forward_15092494"),

    ("leping_peng_jianhe", "彭建和", "男", "汉族", "", "", "",
     "", "",
     "乐平市副市长", "乐平市人民政府",
     "https://www.thepaper.cn/newsDetail_forward_15092494"),

    ("leping_xu_tingjia", "徐庭家", "男", "汉族", "", "", "",
     "", "",
     "乐平市副市长", "乐平市人民政府",
     "https://www.thepaper.cn/newsDetail_forward_15092494"),

    ("leping_ye_chuanhong", "叶传红", "男", "汉族", "", "", "",
     "", "",
     "乐平市副市长、市公安局局长", "乐平市人民政府/乐平市公安局",
     "https://www.qipei.rexun.cn/guonei/2023/0511/1749.html"),

    ("leping_zhou_hao", "周浩", "男", "汉族", "", "", "",
     "", "",
     "乐平市副市长", "乐平市人民政府",
     "http://www.zgcounty.com/news/33531.html"),

    ("leping_liu_hu", "刘虎", "男", "汉族", "", "", "",
     "", "",
     "乐平市副市长", "乐平市人民政府",
     "http://www.zgcounty.com/news/33531.html"),

    # ── 人大、政协领导 ──
    ("leping_liu_wenping", "刘文平", "男", "汉族", "1967-12", "江西都昌", "大学",
     "1991-12", "1988-12",
     "乐平市人大常委会党组书记、主任（2024年9月被查）", "乐平市人大常委会",
     "https://news.qq.com/rain/a/20240918A07AEY00"),

    ("leping_pan_saixin", "潘赛新", "男", "汉族", "", "", "",
     "", "",
     "乐平市政协主席", "乐平市政协",
     "http://www.lpzx.gov.cn/news/zhengxieyaowen/243615457AG2.asp"),

    ("leping_li_ping", "黎萍", "女", "汉族", "1970-10", "江西鄱阳", "中央党校大学",
     "民盟盟员", "1991-09",
     "乐平市政协副主席", "乐平市政协",
     "https://www.newton.com.tw/wiki/%E9%BB%8E%E8%90%8D/56210033"),

    # ── 前任领导 ──
    ("leping_yu_xiaoping", "俞小平", "男", "汉族", "", "江西（推测）", "",
     "", "",
     "景德镇市政协党组书记、主席（乐平前市委书记）", "景德镇市政协",
     "https://baike.so.com/doc/6600190-24409521.html"),

    ("leping_xu_hui", "徐辉", "男", "汉族", "", "", "",
     "", "",
     "景德镇市副市长（乐平前市长，2016-2019任）", "景德镇市人民政府",
     "https://baike.so.com/doc/6185978-32403703.html"),

    ("leping_gao_xiang", "高翔", "男", "汉族", "", "", "",
     "", "",
     "景德镇国家陶瓷文化传承创新试验区管委会专职副主任（乐平前市长，2019-2021任）", "景德镇国家陶瓷文化传承创新试验区管委会",
     "https://baike.so.com/doc/1939757-32406044.html"),

    ("leping_liu_shengqing", "刘圣卿", "男", "汉族", "1964-01", "江西乐平", "在职大学",
     "1983-06", "1981-11",
     "乐平市人大常委会原主任（2020年被查）", "（已落马）",
     "https://m.jxnews.com.cn/jx/system/2020/03/08/018796883.shtml"),
]

organizations = [
    # (id, name, type, level, parent, location)
    ("org_leping_city", "乐平市", "行政区划", "县级市", "景德镇市", "江西省景德镇市"),
    ("org_leping_committee", "中共乐平市委", "党委", "县级", "景德镇市委", "江西省景德镇市乐平市"),
    ("org_leping_gov", "乐平市人民政府", "政府", "县级", "景德镇市政府", "江西省景德镇市乐平市"),
    ("org_leping_discipline", "中共乐平市纪委/乐平市监委", "纪委/监委", "县级", "景德镇市纪委", "江西省景德镇市乐平市"),
    ("org_leping_organization", "中共乐平市委组织部", "党委部门", "正科", "乐平市委", "江西省景德镇市乐平市"),
    ("org_leping_propaganda", "中共乐平市委宣传部", "党委部门", "正科", "乐平市委", "江西省景德镇市乐平市"),
    ("org_leping_united_front", "中共乐平市委统战部", "党委部门", "正科", "乐平市委", "江西省景德镇市乐平市"),
    ("org_leping_politics_legal", "中共乐平市委政法委", "党委部门", "正科", "乐平市委", "江西省景德镇市乐平市"),
    ("org_leping_military", "乐平市人武部", "军事", "正团级", "景德镇军分区", "江西省景德镇市乐平市"),
    ("org_leping_npc", "乐平市人大常委会", "人大", "县级", "景德镇市人大常委会", "江西省景德镇市乐平市"),
    ("org_leping_cppcc", "乐平市政协", "政协", "县级", "景德镇市政协", "江西省景德镇市乐平市"),
    ("org_leping_public_security", "乐平市公安局", "政府部门", "正科", "乐平市政府", "江西省景德镇市乐平市"),
    ("org_jingdezhen_committee", "中共景德镇市委", "党委", "地级", "中共江西省委", "江西省景德镇市"),
    ("org_jingdezhen_gov", "景德镇市人民政府", "政府", "地级", "江西省人民政府", "江西省景德镇市"),
    ("org_jingdezhen_cppcc", "景德镇市政协", "政协", "地级", "江西省政协", "江西省景德镇市"),
    ("org_jingdezhen_ceramic_park", "景德镇国家陶瓷文化传承创新试验区管委会", "管委会", "副厅级", "景德镇市政府", "江西省景德镇市"),
]

positions = [
    # (id, person_id, org_id, title, start, end, rank, note)

    # ── 林卫春 ──
    ("pos_lin_01", "leping_lin_weichun", "org_leping_city", "景德镇市委常委、乐平市委书记", "2021-09", "", "副厅级",
     "2021年9月当选景德镇市委常委；2021年8月任乐平市委书记"),
    ("pos_lin_02", "leping_lin_weichun", "org_leping_committee", "乐平市委书记", "2021-08", "2021-09", "正处级", "2021年8月-9月未兼景德镇市委常委期间"),
    ("pos_lin_03", "leping_lin_weichun", "org_leping_committee", "乐平市委委员、常委、书记（2021年8月1日到任）", "2021-08", "", "正处级", ""),
    ("pos_lin_04", "leping_lin_weichun", "org_leping_committee", "（2010.04-2011.05挂职）乐平市委副书记", "2010-04", "2011-05", "正处级（挂职）", "挂职期间实际任景德镇市委副秘书长、办公室主任"),

    # ── 林卫春——珠山区经历 ──
    ("pos_lin_05", "leping_lin_weichun", "org_jingdezhen_committee", "景德镇市委常委", "2021-09", "", "副厅级", ""),
    ("pos_lin_06", "leping_lin_weichun", "org_leping_city", "珠山区委书记（2016.07-2021.07）", "2016-07", "2021-07", "正处级", "任乐平市委书记前任珠山区委书记"),
    ("pos_lin_old_01", "leping_lin_weichun", "org_jingdezhen_gov", "景德镇市珠山区委副书记、区长", "2011-06", "2016-07", "正处级", ""),
    ("pos_lin_old_02", "leping_lin_weichun", "org_jingdezhen_committee", "景德镇市委副秘书长、办公室主任", "2009-04", "2011-06", "正处级", ""),
    ("pos_lin_old_03", "leping_lin_weichun", "org_jingdezhen_committee", "景德镇市委办公室副主任", "2007-02", "2009-04", "副处级", ""),
    ("pos_lin_old_04", "leping_lin_weichun", "org_jingdezhen_committee", "景德镇市委办公室督查室主任", "2005-12", "2007-02", "正科级", ""),
    ("pos_lin_old_05", "leping_lin_weichun", "org_jingdezhen_gov", "景德镇市政府办公室综合调研科科长", "2002-12", "2005-12", "正科级", ""),
    ("pos_lin_old_06", "leping_lin_weichun", "org_jingdezhen_gov", "景德镇市政府办公室副主任科员", "2000-12", "2002-12", "副科级", ""),
    ("pos_lin_old_07", "leping_lin_weichun", "org_jingdezhen_gov", "景德镇市政府办公室科员", "1997-02", "2000-12", "科员", "其间:1997.04-2002.12南昌大学自考汉语言文学"),
    ("pos_lin_old_08", "leping_lin_weichun", "org_jingdezhen_gov", "景德镇市第六中学教师", "1994-08", "1997-02", "教师", ""),
    # 2004.03-2008.07 景德镇陶瓷学院学习，获工程硕士学位（兼任职务期间）

    # ── 吴艳 ──
    ("pos_wu_01", "leping_wu_yan", "org_leping_gov", "乐平市委副书记、市政府市长", "2021-08", "", "正处级", ""),
    ("pos_wu_old_01", "leping_wu_yan", "org_jingdezhen_gov", "景德镇高新技术产业开发区党工委副书记、管委会副主任", "2021-05", "2021-08", "正处级", ""),
    ("pos_wu_old_02", "leping_wu_yan", "org_jingdezhen_gov", "景德镇高新技术产业开发区党工委副书记", "2021-03", "2021-05", "正处级", ""),
    ("pos_wu_old_03", "leping_wu_yan", "org_jingdezhen_gov", "景德镇市昌江区委副书记", "2016-08", "2021-03", "副处级", ""),
    ("pos_wu_old_04", "leping_wu_yan", "org_jingdezhen_gov", "景德镇市国资委党委副书记、副主任", "2014-07", "2016-08", "副处级", ""),
    ("pos_wu_old_05", "leping_wu_yan", "org_jingdezhen_gov", "景德镇高新区财政局局长(副县级)", "2013-01", "2014-07", "副处级", ""),
    ("pos_wu_old_06", "leping_wu_yan", "org_jingdezhen_gov", "景德镇高新区财政局局长", "2008-11", "2013-01", "正科级", ""),
    ("pos_wu_old_07", "leping_wu_yan", "org_jingdezhen_gov", "景德镇高新区经济发展局局长、财政局副局长", "2008-01", "2008-11", "正科级", ""),
    ("pos_wu_old_08", "leping_wu_yan", "org_jingdezhen_gov", "景德镇高新区财政局副局长", "2004-09", "2008-01", "副科级", ""),
    ("pos_wu_old_09", "leping_wu_yan", "org_jingdezhen_gov", "景德镇高新区财政局工作", "2004-07", "2004-09", "科员", ""),
    ("pos_wu_old_10", "leping_wu_yan", "org_jingdezhen_gov", "浮梁县财政局预算股工作", "1997-07", "2004-07", "科员", ""),

    # ── 谢秋华 ──
    ("pos_xie_01", "leping_xie_qiuhua", "org_leping_committee", "乐平市委副书记", "2021-08", "", "副处级", ""),
    # 谢秋华履历不完整——需要进一步调查

    # ── 王枥珍 ──
    ("pos_wanglz_01", "leping_wang_lizhen", "org_leping_organization", "乐平市委常委、组织部部长", "2021-08", "", "副处级", ""),
    # 王枥珍履历不完整——需要进一步调查

    # ── 邹国良 ──
    ("pos_zou_01", "leping_zou_guoliang", "org_leping_propaganda", "乐平市委常委、宣传部部长", "2021-08", "", "副处级",
     "同时任市工信局党组书记、局长"),
    # 邹国良履历不完整（另有乐平洪岩镇党委书记经历）

    # ── 周军 ──
    ("pos_zhouj_01", "leping_zhou_jun", "org_leping_military", "乐平市委常委、人武部政治委员", "2021-08", "", "副处级（军队转业）", ""),

    # ── 程明波 ──
    ("pos_chengmb_01", "leping_cheng_mingbo", "org_leping_politics_legal", "乐平市委常委、政法委书记", "2021-08", "", "副处级", ""),
    # 程明波曾任乐平洪岩镇党委书记

    # ── 韩伟 ──
    ("pos_han_01", "leping_han_wei", "org_leping_committee", "乐平市委常委", "2021-08", "", "副处级", "负责农业农村工作"),
    ("pos_han_old_01", "leping_han_wei", "org_leping_gov", "乐平市政府党组成员、副市长", "2016-08", "2021-08", "副处级", ""),
    ("pos_han_old_02", "leping_han_wei", "org_leping_city", "乐平市双田镇党委书记", "2010-12", "2016-08", "正科级", ""),
    ("pos_han_old_03", "leping_han_wei", "org_leping_city", "乐平市双田镇党委副书记、镇长", "2007-02", "2010-12", "正科级", ""),
    ("pos_han_old_04", "leping_han_wei", "org_leping_city", "乐平市洎阳街道党工委副书记", "2003-04", "2007-02", "副科级", ""),
    ("pos_han_old_05", "leping_han_wei", "org_leping_city", "乐平市洎阳街道办事处党工委委员、常务副主任", "2002-12", "2003-04", "副科级", ""),
    ("pos_han_old_06", "leping_han_wei", "org_leping_city", "乐平市洎阳街道办事处副主任", "2001-12", "2002-12", "副科级", ""),
    ("pos_han_old_07", "leping_han_wei", "org_leping_city", "乐平市镇桥镇科技副镇长", "1999-01", "2001-12", "副科级", ""),
    ("pos_han_old_08", "leping_han_wei", "org_leping_city", "乐平市乐港镇工作", "1985-03", "1999-01", "科员", ""),

    # ── 刘学飞 ──
    ("pos_liuxf_01", "leping_liu_xuefei", "org_leping_discipline", "乐平市委常委、市纪委书记、市监委主任", "2021-08", "", "副处级", ""),
    # 刘学飞履历不完整——安徽亳州人，之前在景德镇工作

    # ── 丁巍（已落马） ──
    ("pos_dingw_01", "leping_ding_wei", "org_leping_gov", "乐平市委常委、常务副市长", "2021-08", "2024-03", "副处级", "2024年3月主动向组织交代问题"),
    ("pos_dingw_old_01", "leping_ding_wei", "org_leping_city", "乐平市涌山镇党委书记、四级调研员", "", "2021-08", "正科级", ""),
    ("pos_dingw_old_02", "leping_ding_wei", "org_leping_city", "乐平市塔前镇党委书记", "", "", "正科级", ""),
    ("pos_dingw_old_03", "leping_ding_wei", "org_leping_city", "乐平市塔前镇党委副书记、镇长", "", "", "正科级", ""),
    ("pos_dingw_old_04", "leping_ding_wei", "org_leping_city", "乐平市委、市政府信访局副局长", "", "", "副科级", ""),
    ("pos_dingw_old_05", "leping_ding_wei", "org_leping_city", "乐平市委、市政府信访局科室主任", "", "", "科员", ""),

    # ── 董斌 ──
    ("pos_dongb_01", "leping_dong_bin", "org_leping_united_front", "乐平市委常委、统战部部长, 市政协党组副书记", "2021-08", "", "副处级", ""),

    # ── 黄城 ──
    ("pos_huangc_01", "leping_huang_cheng", "org_leping_gov", "乐平市委常委、副市长, 临港镇党委书记", "2021-08", "", "副处级", ""),

    # ── 汪维 ──
    ("pos_wangw_01", "leping_wang_wei", "org_leping_gov", "乐平市委常委、副市长", "2024-06", "", "副处级", "调任乐平前任昌江区副区长"),
    ("pos_wangw_old_01", "leping_wang_wei", "org_jingdezhen_gov", "昌江区政府副区长", "", "2024-06", "副处级", ""),

    # ── 戴戎 ──
    ("pos_dair_01", "leping_dai_rong", "org_leping_united_front", "乐平市委常委、统战部部长", "2023-05", "", "副处级", "接替董斌（董斌调任其他岗）"),
    ("pos_dair_old_01", "leping_dai_rong", "org_jingdezhen_gov", "景德镇市人社局事业单位人事管理科科长", "", "2023-05", "正科级", ""),
    ("pos_dair_old_02", "leping_dai_rong", "org_jingdezhen_gov", "景德镇市公安局经侦支队科员", "2011-11", "2015-05", "科员", ""),
    ("pos_dair_old_03", "leping_dai_rong", "org_jingdezhen_gov", "景德镇市公安局昌江分局科员", "2009-08", "2011-11", "科员", ""),

    # ── 政府副市长 ──
    ("pos_lixb_01", "leping_li_xiaobin", "org_leping_gov", "乐平市副市长", "2021-10", "", "副处级", ""),
    ("pos_zhuly_01", "leping_zhu_liuying", "org_leping_gov", "乐平市副市长", "2021-10", "", "副处级", "分管卫健、教育等"),
    ("pos_pengjh_01", "leping_peng_jianhe", "org_leping_gov", "乐平市副市长", "2021-10", "", "副处级", ""),
    ("pos_xutj_01", "leping_xu_tingjia", "org_leping_gov", "乐平市副市长", "2021-10", "", "副处级", ""),
    ("pos_tych_01", "leping_ye_chuanhong", "org_leping_gov", "乐平市副市长、市公安局局长", "2023-05", "", "副处级", "接替童勇"),
    ("pos_zh_01", "leping_zhou_hao", "org_leping_gov", "乐平市副市长", "", "", "副处级", ""),
    ("pos_lh_01", "leping_liu_hu", "org_leping_gov", "乐平市副市长", "", "", "副处级", ""),

    # ── 人大 ──
    ("pos_liuwp_01", "leping_liu_wenping", "org_leping_npc", "乐平市人大常委会党组书记、主任", "", "2024-09", "正处级", "2024年9月主动投案被查"),
    ("pos_liuwp_old_01", "leping_liu_wenping", "org_jingdezhen_gov", "景德镇市财政局/生态环境局工作", "", "", "", "浮梁县也有任职经历"),

    # ── 政协 ──
    ("pos_pansx_01", "leping_pan_saixin", "org_leping_cppcc", "乐平市政协主席", "", "", "正处级", ""),
    ("pos_lip_01", "leping_li_ping", "org_leping_cppcc", "乐平市政协副主席", "2020-05", "", "副处级", "民盟盟员"),

    # ── 俞小平（前任市委书记） ──
    ("pos_yuxp_01", "leping_yu_xiaoping", "org_jingdezhen_cppcc", "景德镇市政协党组书记、主席", "2021-09", "", "正厅级", ""),
    ("pos_yuxp_02", "leping_yu_xiaoping", "org_leping_committee", "景德镇市委常委、乐平市委书记", "2016-07", "2021-07", "副厅级", ""),

    # ── 徐辉（前市长） ──
    ("pos_xuh_01", "leping_xu_hui", "org_jingdezhen_gov", "景德镇市政府党组成员、副市长", "2021-11", "", "副厅级", ""),
    ("pos_xuh_02", "leping_xu_hui", "org_leping_gov", "乐平市委副书记、市长", "2016-08", "2019-02", "正处级", ""),

    # ── 高翔（前市长） ──
    ("pos_gaox_01", "leping_gao_xiang", "org_jingdezhen_ceramic_park", "景德镇国家陶瓷文化传承创新试验区管委会专职副主任", "2022-04", "", "副厅级", ""),
    ("pos_gaox_02", "leping_gao_xiang", "org_leping_gov", "乐平市委副书记、市长", "2019-03", "2021-07", "正处级", ""),

    # ── 刘圣卿（前人大主任，已落马） ──
    ("pos_liushq_01", "leping_liu_shengqing", "org_leping_npc", "乐平市人大常委会党组书记、主任", "2019-03", "2019-12", "正处级", "2019年12月被查"),
    ("pos_liushq_old_01", "leping_liu_shengqing", "org_leping_committee", "乐平市委副书记", "2016-08", "2019-01", "副处级", ""),
    ("pos_liushq_old_02", "leping_liu_shengqing", "org_leping_gov", "乐平市委常委、常务副市长", "2014-12", "2016-08", "副处级", ""),
]

relationships = [
    # (id, person_a, person_b, type, context, overlap_org, overlap_period)

    # 林卫春 ↔ 吴艳（一把手+二把手）
    ("rel_001", "leping_lin_weichun", "leping_wu_yan", "工作搭档",
     "林卫春（市委书记）与吴艳（市长）为党政正职搭档关系，2021年8月换届后搭档至今",
     "中共乐平市委/乐平市人民政府", "2021-08 至今"),

    # 林卫春 ↔ 俞小平（前后任）
    ("rel_002", "leping_lin_weichun", "leping_yu_xiaoping", "前后任",
     "俞小平2016.07-2021.07任乐平市委书记，林卫春2021.08接任",
     "中共乐平市委", "2016-07—2021-07（间接）"),

    # 俞小平 ↔ 徐辉（前搭档）
    ("rel_003", "leping_yu_xiaoping", "leping_xu_hui", "工作搭档",
     "俞小平任乐平市委书记期间（2016-2021），徐辉任乐平市长（2016-2019）",
     "中共乐平市委/乐平市人民政府", "2016-08—2019-02"),

    # 徐辉 ↔ 高翔（前后任市长）
    ("rel_004", "leping_xu_hui", "leping_gao_xiang", "前后任",
     "徐辉调任后高翔接任乐平市长",
     "乐平市人民政府", "2019-03（交接）"),

    # 高翔 ↔ 吴艳（前后任市长）
    ("rel_005", "leping_gao_xiang", "leping_wu_yan", "前后任",
     "高翔2021年7月卸任乐平市长，吴艳2021年8月接任",
     "乐平市人民政府", "2021-07—2021-08"),

    # 林卫春 ↔ 林卫春挂职（自己与乐平的早期交集）
    ("rel_006", "leping_lin_weichun", "leping_lin_weichun", "自我关联（挂职）",
     "林卫春2010-2011年在乐平挂职副书记，为后来任书记埋下伏笔",
     "中共乐平市委", "2010-04—2011-05"),

    # 韩伟 ↔ 丁巍（市政府同事）
    ("rel_007", "leping_han_wei", "leping_ding_wei", "同僚",
     "韩伟与丁巍同为乐平市副市长（2016-2021期间有重叠）",
     "乐平市人民政府", "2016-08—2021-08"),

    # 丁巍 ↔ 刘圣卿（落马链条——常务副市长→常务副市长关联）
    ("rel_008", "leping_ding_wei", "leping_liu_shengqing", "前后任",
     "刘圣卿2014-2016任乐平常务副市长；丁巍2021-2024任同一职务，两人均落马",
     "乐平市人民政府", "（先后任常务副市长）"),

    # 刘圣卿 ↔ 刘文平（人大前后任，均落马）
    ("rel_009", "leping_liu_shengqing", "leping_liu_wenping", "前后任",
     "刘圣卿2019年任人大主任（同年被查），刘文平接任人大主任（2024年被查），均落马",
     "乐平市人大常委会", "2019-2024（先后任）"),

    # 吴艳 ↔ 高翔（政府工作衔接）
    ("rel_010", "leping_wu_yan", "leping_gao_xiang", "同事（昌江区）",
     "吴艳2016-2021任昌江区委副书记；高翔2021年9月起任珠山区委书记，两人在景德镇市辖区工作",
     "景德镇市辖区", "2016-2021"),

    # 韩伟 ↔ 林卫春（下级与上级）
    ("rel_011", "leping_han_wei", "leping_lin_weichun", "上下级",
     "韩伟为乐平市委常委，林卫春为市委书记",
     "中共乐平市委", "2021-08 至今"),

    # 谢秋华 ↔ 吴艳（副书记与市长）
    ("rel_012", "leping_xie_qiuhua", "leping_wu_yan", "同僚",
     "谢秋华为市委副书记，吴艳为市委副书记、市长，两人同为副书记",
     "中共乐平市委", "2021-08 至今"),

    # 王枥珍 ↔ 谢秋华（组织+群团）
    ("rel_013", "leping_wang_lizhen", "leping_xie_qiuhua", "同僚",
     "谢秋华与王枥珍共同出席青年工作联席会议",
     "中共乐平市委", "2022-12"),

    # 戴戎 ↔ 林卫春（统战调研）
    ("rel_014", "leping_dai_rong", "leping_lin_weichun", "上下级",
     "林卫春（当时任景德镇统战部长）赴乐平调研统战，戴戎（乐平统战部长）陪同",
     "统战系统", "2024-10"),
]


# ═══════════════════════════════════════════════════════════════════════════
# BUILD SQLITE
# ═══════════════════════════════════════════════════════════════════════════

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
PRAGMA foreign_keys = ON;

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
    id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL,
    org_id TEXT NOT NULL,
    title TEXT,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id TEXT PRIMARY KEY,
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

for p in persons:
    c.execute("""INSERT OR REPLACE INTO persons
        (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", p)

for o in organizations:
    c.execute("""INSERT OR REPLACE INTO organizations
        (id, name, type, level, parent, location)
        VALUES (?,?,?,?,?,?)""", o)

for pos in positions:
    c.execute("""INSERT OR REPLACE INTO positions
        (id, person_id, org_id, title, start, end, rank, note)
        VALUES (?,?,?,?,?,?,?,?)""", pos)

for r in relationships:
    c.execute("""INSERT OR REPLACE INTO relationships
        (id, person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?,?,?,?,?,?,?)""", r)

conn.commit()

# Stats
person_count = c.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
org_count = c.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
pos_count = c.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
rel_count = c.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]

conn.close()

print(f"✅ SQLite DB: {DB_PATH}")
print(f"   Persons: {person_count}, Orgs: {org_count}, Positions: {pos_count}, Relationships: {rel_count}")


# ═══════════════════════════════════════════════════════════════════════════
# BUILD GEXF (string concat — safe with xmlns:viz)
# ═══════════════════════════════════════════════════════════════════════════

def color_for_person(pid):
    """Return viz color based on role."""
    if "lin_weichun" in pid:
        return "#CC0000"   # red = party secretary
    if "wu_yan" in pid:
        return "#0044CC"   # blue = government leader
    if "ding_wei" in pid or "liu_wenping" in pid or "liu_shengqing" in pid:
        return "#FF8800"   # orange = discipline/fallen
    return "#777777"       # grey = other

def size_for_person(pid):
    if "lin_weichun" in pid or "wu_yan" in pid:
        return "20.0"
    if any(x in pid for x in ["xie_qiuhua", "wang_lizhen", "han_wei",
                                "liu_xuefei", "ding_wei", "wang_wei",
                                "dong_bin", "dai_rong", "huang_cheng",
                                "zou_guoliang", "zhou_jun", "cheng_mingbo",
                                "yu_xiaoping", "gao_xiang", "xu_hui",
                                "li_wenping", "pan_saixin"]):
        return "14.0"
    return "10.0"

def org_color(otype):
    m = {"党委": "#AA2222", "政府": "#2244AA", "人大": "#226622",
         "政协": "#662266", "纪委": "#CC6600", "军事": "#446644",
         "管委会": "#228888"}
    for k, v in m.items():
        if k in otype:
            return v
    return "#888888"


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append('  <graph defaultedgetype="undirected" mode="static">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="kind" title="Kind" type="string"/>')
lines.append('      <attribute id="role" title="Role" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    pid, name, gender, ethnicity, birth, birthplace = p[0], p[1], p[2], p[3], p[4], p[5]
    role = "secretary" if "lin_weichun" in pid else \
           "gov_leader" if "wu_yan" in pid else \
           "discipline" if any(x in pid for x in ["ding_wei", "liu_wenping", "liu_shengqing"]) else \
           "other"
    sz = size_for_person(pid)
    clr = color_for_person(pid)
    lines.append(f'      <node id="{pid}" label="{name}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="kind" value="person"/>')
    lines.append(f'          <attvalue for="role" value="{role}"/>')
    lines.append(f'          <attvalue for="birth" value="{birth}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{birthplace}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(clr[1:3],16)}" g="{int(clr[3:5],16)}" b="{int(clr[5:7],16)}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid, oname, otype = o[0], o[1], o[2]
    oc = org_color(otype)
    lines.append(f'      <node id="{oid}" label="{oname}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="kind" value="organization"/>')
    lines.append(f'          <attvalue for="role" value="{otype}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(oc[1:3],16)}" g="{int(oc[3:5],16)}" b="{int(oc[5:7],16)}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')

lines.append('    </nodes>')

# ── Edges: Positions (person → org) ──
lines.append('    <edges>')
edge_id = 0
for pos in positions:
    pos_id, pid, oid, title = pos[0], pos[1], pos[2], pos[3]
    lines.append(f'      <edge id="e{edge_id}" source="{pid}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{title}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# ── Edges: Relationships (person ↔ person) ──
for r in relationships:
    rid, pa, pb, rtype, ctx, oo, op = r[0], r[1], r[2], r[3], r[4], r[5], r[6]
    if pa == pb:
        continue  # skip self-loops
    lines.append(f'      <edge id="e{edge_id}" source="{pa}" target="{pb}" label="{rtype}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="relationship"/>')
    lines.append(f'          <attvalue for="context" value="{ctx}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

person_nodes = len(persons)
org_nodes = len(organizations)
total_edges = edge_id
print(f"✅ GEXF graph: {GEXF_PATH}")
print(f"   Person nodes: {person_nodes}, Org nodes: {org_nodes}, Total edges: {total_edges}")
print("")
print("═══ Summary ═══")
print(f"Database: {DB_PATH}")
print(f"Graph:    {GEXF_PATH}")
print(f"Total records — Persons: {person_count}, Organizations: {org_count}, Positions: {pos_count}, Relationships: {rel_count}")
