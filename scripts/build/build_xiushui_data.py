#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Xiushui County (修水县) leadership network.

修水县 is located in the northwest of Jiangxi Province, under Jiujiang City.
It is the largest county (by area) in Jiangxi, bordering Hunan and Hubei provinces.
"""
import os, sqlite3
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "data/database/xiushui_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/xiushui_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
# ID convention: xiushui_{pinyin_name}

persons = [
    # ── Current & Recent Party Secretaries ──
    {"id":"xiushui_liu_jie","name":"刘婕","gender":"女","ethnicity":"汉族",
     "birth":"1978-09","birthplace":"浙江温州","education":"省委党校研究生",
     "party_join":"1999-11","work_start":"2001-07",
     "current_post":"中共修水县委书记","current_org":"中共修水县委员会",
     "source":"https://www.xiushui.gov.cn (2026年7月政务资讯); 新浪财经 https://finance.sina.com.cn 2026年5月任前公示"},
    {"id":"xiushui_zheng_qinghua","name":"郑庆华","gender":"男","ethnicity":"汉族",
     "birth":"1970-10","birthplace":"江西庐山(原星子县)","education":"省委党校研究生",
     "party_join":"中共党员","work_start":"1992-08",
     "current_post":"九江市人大常委会党组成员、副主任","current_org":"九江市人大常委会",
     "source":"https://baike.baidu.com (微博人物志); 九江人大信息网 2026-01"},
    {"id":"xiushui_sun_zhaohui","name":"孙朝辉","gender":"男","ethnicity":"汉族",
     "birth":"1974-12","birthplace":"江西都昌","education":"江西农业大学/农业推广硕士",
     "party_join":"中共党员","work_start":"1998-10",
     "current_post":"九江市人大常委会党组成员、副主任(原九江市委副书记)","current_org":"九江市人大常委会",
     "source":"https://www.thepaper.cn 澎湃新闻 2021-03; 新浪网 2020-05"},
    {"id":"xiushui_zhang_lin","name":"张林","gender":"男","ethnicity":"汉族",
     "birth":"1965-03","birthplace":"江西武宁","education":"大专",
     "party_join":"中共党员","work_start":"1987-07",
     "current_post":"九江市政协党组成员、副主席","current_org":"政协九江市委员会",
     "source":"https://www.thepaper.cn 澎湃新闻 2021-08; 新浪网 https://k.sina.com.cn 2021-08"},

    # ── Current & Recent County Mayors ──
    {"id":"xiushui_liu_mingshou","name":"刘名寿","gender":"男","ethnicity":"汉族",
     "birth":"1982-03","birthplace":"","education":"在职研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委副书记、县政府代县长","current_org":"修水县人民政府",
     "source":"https://www.xiushui.gov.cn (2026年7月); 九江经济技术开发区官网 https://www.jj.gov.cn 2025-12"},

    # ── Standing Committee (县委常委) ──
    {"id":"xiushui_leng_fenhua","name":"冷芬华","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委常委、政法委书记","current_org":"中共修水县委员会",
     "source":"https://www.xiushui.gov.cn; 修水县政府门户网站"},
    {"id":"xiushui_zhu_qiusheng","name":"朱秋生","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委常委、县政府常务副县长","current_org":"修水县人民政府",
     "source":"https://www.xiushui.gov.cn (PDF《修水县人民政府办公室文件》) 2025"},
    {"id":"xiushui_lu_haiming","name":"卢海明","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委常委、宣传部部长","current_org":"中共修水县委员会",
     "source":"https://www.xiushui.gov.cn; 微信公众平台 2025-06"},
    {"id":"xiushui_zhou_qunfeng","name":"周群峰","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委常委","current_org":"中共修水县委员会",
     "source":"https://www.xiushui.gov.cn"},
    {"id":"xiushui_miao_ketai","name":"缪可太","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委常委、县工业园区党工委书记","current_org":"中共修水县委员会",
     "source":"https://www.xiushui.gov.cn 2025-12; 微信公众平台 2025-12"},
    {"id":"xiushui_ruan_guoming","name":"阮国明","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委常委、县政府副县长","current_org":"修水县人民政府",
     "source":"https://www.xiushui.gov.cn"},
    {"id":"xiushui_fan_xuegang","name":"樊雪刚","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委常委","current_org":"中共修水县委员会",
     "source":"https://www.xiushui.gov.cn 2025-08"},
    {"id":"xiushui_zhou_jinghua","name":"周经华","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委常委、县纪委书记、县监委代理主任","current_org":"中共修水县纪律检查委员会",
     "source":"https://www.xiushui.gov.cn; 修水县纪委县监委网站 2026-01-15"},
    {"id":"xiushui_qiu_xiuhua","name":"丘秀华","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委常委、人武部部长","current_org":"修水县人民武装部",
     "source":"https://www.xiushui.gov.cn (百度百科-中国共产党修水县委员会)"},
    {"id":"xiushui_lu_liheng","name":"卢礼衡","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委常委、县政府副县长","current_org":"修水县人民政府",
     "source":"https://www.xiushui.gov.cn 2026-07"},

    # ── Former Standing Committee Members (2021) ──
    {"id":"xiushui_ma_wenqing","name":"马文卿","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委副书记(原)","current_org":"",
     "source":"https://www.xiushui.gov.cn; 新浪网 2021-09"},
    {"id":"xiushui_liu_xueping","name":"刘雪萍","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委常委(原)","current_org":"",
     "source":"https://www.xiushui.gov.cn; 新浪网 2021-09"},
    {"id":"xiushui_liu_wei","name":"刘伟","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委常委(原)","current_org":"",
     "source":"https://www.xiushui.gov.cn"},
    {"id":"xiushui_dong_guoxiang","name":"董国祥","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委常委(原)","current_org":"",
     "source":"https://www.xiushui.gov.cn"},
    {"id":"xiushui_zha_mingyang","name":"查明杨","gender":"男","ethnicity":"汉族",
     "birth":"1984-10","birthplace":"江西共青城","education":"省委党校研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"九江经济技术开发区党工委委员(原修水县委常委、组织部部长)","current_org":"九江经济技术开发区",
     "source":"https://baike.baidu.com/item/%E6%9F%A5%E6%98%8E%E6%9D%A8"},
    {"id":"xiushui_huang_sen","name":"黄森","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县委常委(原)","current_org":"",
     "source":"https://www.xiushui.gov.cn; 人民资讯 2021-09"},
    {"id":"xiushui_xin_jianbo","name":"辛建波","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"修水县委副书记、县政府副县长(挂职)","current_org":"修水县人民政府",
     "source":"https://www.xiushui.gov.cn; 修水县第十七届人大六次会议 2026-03"},

    # ── NPC & CPPCC Leaders ──
    {"id":"xiushui_yuan_guanyun","name":"袁观云","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县人大常委会主任","current_org":"修水县人民代表大会常务委员会",
     "source":"https://www.xiushui.gov.cn 2026-03"},
    {"id":"xiushui_wang_weihua","name":"王位华","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"修水县政协主席","current_org":"政协修水县委员会",
     "source":"https://www.xiushui.gov.cn"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":"org_xs_party","name":"中共修水县委员会","type":"党委","level":"县处级","parent":"中共九江市委员会","location":"江西省九江市修水县"},
    {"id":"org_xs_gov","name":"修水县人民政府","type":"政府","level":"县处级","parent":"九江市人民政府","location":"江西省九江市修水县"},
    {"id":"org_xs_discipline","name":"中共修水县纪律检查委员会","type":"纪委","level":"县处级","parent":"中共九江市纪律检查委员会","location":"江西省九江市修水县"},
    {"id":"org_xs_military","name":"修水县人民武装部","type":"军事","level":"县处级","parent":"","location":"江西省九江市修水县"},
    {"id":"org_xs_npc","name":"修水县人民代表大会常务委员会","type":"人大","level":"县处级","parent":"九江市人大常委会","location":"江西省九江市修水县"},
    {"id":"org_xs_cppcc","name":"政协修水县委员会","type":"政协","level":"县处级","parent":"政协九江市委员会","location":"江西省九江市修水县"},
    {"id":"org_xs_industrial_park","name":"修水(九江)工业园管委会","type":"开发区","level":"县处级","parent":"修水县人民政府","location":"江西省九江市修水县"},

    # Higher-level
    {"id":"org_jj_npc","name":"九江市人大常委会","type":"人大","level":"地市级","parent":"江西省人大常委会","location":"江西省九江市"},
    {"id":"org_jj_cppcc","name":"政协九江市委员会","type":"政协","level":"地市级","parent":"政协江西省委员会","location":"江西省九江市"},
    {"id":"org_jj_ete_park","name":"九江经济技术开发区","type":"开发区","level":"国家级","parent":"九江市人民政府","location":"江西省九江市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 刘婕 (Liu Jie) career ──
    {"person_id":"xiushui_liu_jie","org_id":"org_xs_party","title":"中共修水县委书记","start":"2026-05","end":"","rank":"县处级正职","note":"2026年5月任前公示，现任"},
    {"person_id":"xiushui_liu_jie","org_id":"org_xs_gov","title":"修水县人民政府县长","start":"2021-10","end":"2026-05","rank":"县处级正职","note":"2021.08代县长，2021.10正式当选"},
    {"person_id":"xiushui_liu_jie","org_id":"org_xs_gov","title":"修水县人民政府代县长","start":"2021-08","end":"2021-10","rank":"县处级正职","note":""},
    # 刘婕 earlier: 瑞昌市湓城街道办事处副主任科员, 九江市委组织部副科级/正科级组织员,
    # 牯岭镇镇长/党委书记, 省经济作物实验站副站长, 庐山管理局发改委
    # (incomplete dates from public sources)

    # ── 郑庆华 (Zheng Qinghua) career ──
    {"person_id":"xiushui_zheng_qinghua","org_id":"org_jj_npc","title":"九江市人大常委会党组成员、副主任","start":"2026-01","end":"","rank":"副厅级","note":"2026年1月当选"},
    {"person_id":"xiushui_zheng_qinghua","org_id":"org_xs_party","title":"中共修水县委书记","start":"2021-08","end":"2026-07","rank":"县处级正职","note":"主持县委全面工作，2021.08-2026.07"},
    {"person_id":"xiushui_zheng_qinghua","org_id":"org_xs_gov","title":"庐山西海风景名胜区党委副书记、管委会主任","start":"2019-07","end":"2021-08","rank":"县处级正职","note":""},
    {"person_id":"xiushui_zheng_qinghua","org_id":"org_xs_party","title":"武宁县委副书记、县委党校校长","start":"2016-12","end":"2019-07","rank":"县处级副职","note":""},
    # 郑庆华 earlier: 星子县 - 共青园林处 - 九江市园林处 - 武宁副县长
    # Known: 1992.08 星子县隘口中学教师 → 星子县 → 共青开放开发区 → 九江市园林处 → 武宁
    # (exact positions and dates before 2016 are incomplete)

    # ── 孙朝辉 (Sun Zhaohui) career ──
    {"person_id":"xiushui_sun_zhaohui","org_id":"org_jj_npc","title":"九江市人大常委会党组成员、副主任","start":"2020-01","end":"","rank":"副厅级","note":"兼任修水县委书记至2021.08"},
    {"person_id":"xiushui_sun_zhaohui","org_id":"org_xs_party","title":"中共修水县委书记","start":"2014-01","end":"2021-08","rank":"县处级正职","note":"同时任九江市委副书记(2021.03起)"},
    {"person_id":"xiushui_sun_zhaohui","org_id":"org_xs_gov","title":"修水县人民政府县长","start":"2011-09","end":"2014-01","rank":"县处级正职","note":"2011.06代县长"},
    {"person_id":"xiushui_sun_zhaohui","org_id":"org_xs_party","title":"修水县委副书记、县政府党组书记","start":"2011-06","end":"2011-09","rank":"县处级副职","note":""},
    {"person_id":"xiushui_sun_zhaohui","org_id":"org_xs_party","title":"九江县委副书记","start":"2008-08","end":"2011-06","rank":"县处级副职","note":""},
    {"person_id":"xiushui_sun_zhaohui","org_id":"org_xs_gov","title":"九江县委常委、县政府常务副县长","start":"2006-05","end":"2008-08","rank":"县处级副职","note":"2007.12获农大农业推广硕士"},
    {"person_id":"xiushui_sun_zhaohui","org_id":"org_xs_gov","title":"都昌县大沙镇党委书记","start":"2003-03","end":"2006-05","rank":"正科级","note":""},
    {"person_id":"xiushui_sun_zhaohui","org_id":"org_xs_gov","title":"都昌县七角乡副乡长","start":"2001-05","end":"2003-03","rank":"副科级","note":"2000.07副乡长候选人"},
    {"person_id":"xiushui_sun_zhaohui","org_id":"org_xs_gov","title":"都昌县农业局经作站技术员","start":"1998-10","end":"2001-05","rank":"","note":"江西农大园艺专业1994.09-1998.07"},

    # ── 张林 (Zhang Lin) career ──
    {"person_id":"xiushui_zhang_lin","org_id":"org_jj_cppcc","title":"九江市政协党组成员、副主席","start":"2021-08","end":"","rank":"副厅级","note":""},
    {"person_id":"xiushui_zhang_lin","org_id":"org_xs_gov","title":"修水县人民政府县长","start":"2014-01","end":"2021-08","rank":"县处级正职","note":"接替孙朝辉升书记后的空缺"},
    {"person_id":"xiushui_zhang_lin","org_id":"org_xs_gov","title":"修水县人民政府代县长","start":"2013","end":"2014-01","rank":"县处级正职","note":""},
    # 张林 earlier: 武宁县罗坪乡→横路乡→县委办→武宁副县长→永修/武宁常务→修水代县长
    # (long career path, see his detailed resume from thepaper.cn)

    # ── 刘名寿 (Liu Mingshou) ──
    {"person_id":"xiushui_liu_mingshou","org_id":"org_xs_gov","title":"修水县委副书记、县政府代县长","start":"2026-07","end":"","rank":"县处级正职","note":"2026年7月任代县长"},
    {"person_id":"xiushui_liu_mingshou","org_id":"org_jj_ete_park","title":"九江经济技术开发区党工委委员、管委会副主任","start":"","end":"2026-07","rank":"县处级副职","note":"此前职务"},

    # ── Current Standing Committee positions ──
    {"person_id":"xiushui_leng_fenhua","org_id":"org_xs_party","title":"修水县委常委、政法委书记","start":"","end":"","rank":"县处级副职","note":"现任"},
    {"person_id":"xiushui_zhu_qiusheng","org_id":"org_xs_gov","title":"修水县委常委、县政府常务副县长","start":"","end":"","rank":"县处级副职","note":"现任"},
    {"person_id":"xiushui_lu_haiming","org_id":"org_xs_party","title":"修水县委常委、宣传部部长","start":"","end":"","rank":"县处级副职","note":"现任"},
    {"person_id":"xiushui_zhou_qunfeng","org_id":"org_xs_party","title":"修水县委常委","start":"","end":"","rank":"县处级副职","note":"现任"},
    {"person_id":"xiushui_miao_ketai","org_id":"org_xs_industrial_park","title":"修水县委常委、县工业园区党工委书记","start":"","end":"","rank":"县处级副职","note":"现任"},
    {"person_id":"xiushui_ruan_guoming","org_id":"org_xs_gov","title":"修水县委常委、县政府副县长","start":"","end":"","rank":"县处级副职","note":"现任"},
    {"person_id":"xiushui_fan_xuegang","org_id":"org_xs_party","title":"修水县委常委","start":"","end":"","rank":"县处级副职","note":"现任"},
    {"person_id":"xiushui_zhou_jinghua","org_id":"org_xs_discipline","title":"修水县委常委、县纪委书记、县监委代理主任","start":"","end":"","rank":"县处级副职","note":"现任"},
    {"person_id":"xiushui_qiu_xiuhua","org_id":"org_xs_military","title":"修水县委常委、县人武部部长","start":"","end":"","rank":"县处级副职","note":"现任"},
    {"person_id":"xiushui_lu_liheng","org_id":"org_xs_gov","title":"修水县委常委、县政府副县长","start":"","end":"","rank":"县处级副职","note":"现任"},

    # ── Former Standing Committee positions ──
    {"person_id":"xiushui_ma_wenqing","org_id":"org_xs_party","title":"修水县委副书记","start":"2021-09","end":"","rank":"县处级副职","note":"2021年当选，届中调整"},
    {"person_id":"xiushui_liu_xueping","org_id":"org_xs_party","title":"修水县委常委","start":"2021-09","end":"","rank":"县处级副职","note":"2021年当选"},
    {"person_id":"xiushui_liu_wei","org_id":"org_xs_party","title":"修水县委常委","start":"2021-09","end":"","rank":"县处级副职","note":"2021年当选"},
    {"person_id":"xiushui_dong_guoxiang","org_id":"org_xs_party","title":"修水县委常委","start":"2021-09","end":"","rank":"县处级副职","note":"2021年当选"},
    {"person_id":"xiushui_zha_mingyang","org_id":"org_xs_party","title":"修水县委常委、组织部部长","start":"2021-09","end":"2025","rank":"县处级副职","note":"后兼工业园党工委书记；2025年调离"},
    {"person_id":"xiushui_zha_mingyang","org_id":"org_xs_industrial_park","title":"修水县委常委、工业园党工委书记","start":"2022","end":"2025","rank":"县处级副职","note":"兼任"},
    {"person_id":"xiushui_zha_mingyang","org_id":"org_jj_ete_park","title":"九江经济技术开发区党工委委员","start":"2025","end":"","rank":"县处级副职","note":"调任"},
    {"person_id":"xiushui_huang_sen","org_id":"org_xs_party","title":"修水县委常委","start":"2021-09","end":"","rank":"县处级副职","note":"2021年当选"},
    {"person_id":"xiushui_xin_jianbo","org_id":"org_xs_gov","title":"修水县委副书记、县政府副县长(挂职)","start":"","end":"","rank":"县处级副职","note":"挂职"},

    # ── NPC & CPPCC ──
    {"person_id":"xiushui_yuan_guanyun","org_id":"org_xs_npc","title":"修水县人大常委会主任","start":"2021","end":"","rank":"县处级正职","note":"现任"},
    {"person_id":"xiushui_wang_weihua","org_id":"org_xs_cppcc","title":"修水县政协主席","start":"2021","end":"","rank":"县处级正职","note":"现任"},

    # ── 郑庆华 earlier career (fragmentary) ──
    # Known: 星子县隘口中学教师(1992.08) → 星子县 → 共青开放开发区 → 九江市园林处
    # → 武宁县 → 武宁县委副书记(2016.12) → 庐山西海(2019.07) → 修水(2021.08)
    {"person_id":"xiushui_zheng_qinghua","org_id":"org_xs_gov","title":"武宁县人民政府副县长(前职)","start":"","end":"2016-12","rank":"县处级副职","note":"此前在九江市园林处、共青开放开发区、星子县工作"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── Party Secretary Succession Chain ──
    {"person_a":"xiushui_liu_jie","person_b":"xiushui_zheng_qinghua",
     "type":"前后任","context":"刘婕(2026.05接任书记) → 郑庆华(2021.08-2026.07书记)，刘婕原为县长升任书记",
     "overlap_org":"中共修水县委员会","overlap_period":"2026-05"},
    {"person_a":"xiushui_zheng_qinghua","person_b":"xiushui_sun_zhaohui",
     "type":"前后任","context":"郑庆华(2021.08接任书记) → 孙朝辉(2014-2021书记，升九江市委副书记)",
     "overlap_org":"中共修水县委员会","overlap_period":"2021-08"},

    # ── County Mayor Succession Chain ──
    {"person_a":"xiushui_liu_mingshou","person_b":"xiushui_liu_jie",
     "type":"前后任","context":"刘名寿(2026.07代县长) → 刘婕(2021-2026县长，升书记)",
     "overlap_org":"修水县人民政府","overlap_period":"2026-07"},
    {"person_a":"xiushui_liu_jie","person_b":"xiushui_zhang_lin",
     "type":"前后任","context":"刘婕(2021.08接任县长) → 张林(2014-2021县长，调九江政协)",
     "overlap_org":"修水县人民政府","overlap_period":"2021-08"},
    {"person_a":"xiushui_zhang_lin","person_b":"xiushui_sun_zhaohui",
     "type":"前后任","context":"张林(2014接任县长) → 孙朝辉(2011-2014县长，升书记)",
     "overlap_org":"修水县人民政府","overlap_period":"2014-01"},

    # ── 党政搭档 (Party Secretary - County Mayor pairs) ──
    {"person_a":"xiushui_liu_jie","person_b":"xiushui_liu_mingshou",
     "type":"党政搭档","context":"刘婕(县委书记)与刘名寿(代县长)为2026年7月起党政一把手",
     "overlap_org":"修水县","overlap_period":"2026-07至今"},
    {"person_a":"xiushui_zheng_qinghua","person_b":"xiushui_liu_jie",
     "type":"党政搭档","context":"郑庆华(县委书记)与刘婕(县长)搭班子，2021.08-2026.05",
     "overlap_org":"修水县","overlap_period":"2021-08至2026-05"},
    {"person_a":"xiushui_sun_zhaohui","person_b":"xiushui_zhang_lin",
     "type":"党政搭档","context":"孙朝辉(县委书记)与张林(县长)搭班子，2014-2021",
     "overlap_org":"修水县","overlap_period":"2014-2021"},

    # ── 孙朝辉↔郑庆华: 都昌/星子-庐山地域网络 ──
    {"person_a":"xiushui_sun_zhaohui","person_b":"xiushui_zheng_qinghua",
     "type":"地域关联","context":"孙朝辉(都昌人)与郑庆华(庐山人)，分属九江不同县域，先后任修水书记",
     "overlap_org":"中共修水县委员会","overlap_period":"不重叠"},

    # ── 刘婕跨省籍贯 ──
    {"person_a":"xiushui_liu_jie","person_b":"xiushui_zheng_qinghua",
     "type":"工作关系","context":"刘婕(浙江温州人)与郑庆华(江西庐山人)，刘婕系少数非江西籍的修水主官之一",
     "overlap_org":"修水县","overlap_period":"2021-2026"},

    # ── 现任常委同僚关系 ──
    {"person_a":"xiushui_leng_fenhua","person_b":"xiushui_zhu_qiusheng",
     "type":"同僚","context":"冷芬华(政法委书记)与朱秋生(常务副县长)均为县委常委",
     "overlap_org":"中共修水县委员会","overlap_period":""},
    {"person_a":"xiushui_lu_haiming","person_b":"xiushui_zhou_jinghua",
     "type":"同僚","context":"卢海明(宣传部长)与周经华(纪委书记)均为县委常委",
     "overlap_org":"中共修水县委员会","overlap_period":""},
    {"person_a":"xiushui_miao_ketai","person_b":"xiushui_ruan_guoming",
     "type":"同僚","context":"缪可太(工业园书记)与阮国明(副县长)均为县委常委",
     "overlap_org":"中共修水县委员会","overlap_period":""},

    # ── 人大/政协与党政关系 ──
    {"person_a":"xiushui_yuan_guanyun","person_b":"xiushui_liu_jie",
     "type":"工作关系","context":"袁观云(人大主任)与刘婕(书记)为县四套班子关系",
     "overlap_org":"修水县","overlap_period":"2021至今"},
    {"person_a":"xiushui_wang_weihua","person_b":"xiushui_zheng_qinghua",
     "type":"工作关系","context":"王位华(政协主席)与郑庆华(前书记)曾为县四套班子关系",
     "overlap_org":"修水县","overlap_period":"2021-2026"},

    # ── 跨县/跨市交流 ──
    {"person_a":"xiushui_zha_mingyang","person_b":"xiushui_liu_mingshou",
     "type":"跨系统调动","context":"查明杨(修水前组织部长→九江经开区)与刘名寿(九江经开区→修水代县长)，两人均为经开区-修水双向交流的案例",
     "overlap_org":"九江经济技术开发区","overlap_period":""},
    {"person_a":"xiushui_zheng_qinghua","person_b":"xiushui_sun_zhaohui",
     "type":"跨地域路径","context":"郑庆华(武宁→庐山西海→修水)与孙朝辉(都昌→九江→修水)代表了九江两条不同的县域干部成长路径",
     "overlap_org":"","overlap_period":""},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
    work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
    parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id TEXT, org_id TEXT, title TEXT, start TEXT,
    end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a TEXT, person_b TEXT, type TEXT, context TEXT,
    overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
CREATE INDEX IF NOT EXISTS idx_pos_person ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_org ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")

for p in persons:
    c.execute("INSERT OR REPLACE INTO persons(id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations(id,name,type,level,parent,location) VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions(person_id,org_id,title,start,end,rank,note) VALUES(?,?,?,?,?,?,?)",
              (pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period) VALUES(?,?,?,?,?,?)",
              (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
conn.commit()

counts = {}
for tbl in ["persons","organizations","positions","relationships"]:
    counts[tbl] = c.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t,n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF
# =========================================================================
def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(post):
    p = post or ""
    # Party Secretary (top) - Red
    if "县委书记" in p and "副" not in p:
        return "230,50,50"
    # Government leader (县长) - Blue
    if "县长" in p and "副" not in p:
        return "50,100,230"
    # County mayor (代县长) - Blue
    if "代县长" in p:
        return "50,100,230"
    # Deputy county mayor - Lighter blue
    if "副县长" in p:
        return "80,140,230"
    # Discipline inspection - Orange
    if "纪委书记" in p:
        return "255,165,0"
    # NPC - Light blue
    if "人大" in p:
        return "180,200,255"
    # CPPCC - Purple
    if "政协" in p:
        return "200,180,255"
    # Former/previous - Grey
    if "原" in p or "挂职" in p:
        return "150,150,150"
    return "120,120,120"

def org_color(otype):
    return {"党委":"255,200,200","政府":"200,200,255","纪委":"255,220,200","人大":"200,230,255",
            "政协":"230,200,255","军事":"200,255,200","开发区":"200,255,200"}.get(otype,"200,200,200")

today = datetime.now().strftime("%Y-%m-%d")
lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>修水县领导班子工作关系网络 — {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
for aid,atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","education"),("4","current_post"),("5","entity_type")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid,atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    c_ = person_color(p.get("current_post","")).split(",")
    is_top = ("县委书记" in p.get("current_post","") and "副" not in p.get("current_post","")) or \
             ("县长" in p.get("current_post","") and "副" not in p.get("current_post","")) or \
             ("代县长" in p.get("current_post",""))
    sz = "20.0" if is_top else "12.0"
    lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("education","")),("4",p.get("current_post","")),("5","person")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c_[0]}" g="{c_[1]}" b="{c_[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: Organizations
for o in organizations:
    c_ = org_color(o.get("type","")).split(",")
    lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4",""),("5","organization")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c_[0]}" g="{c_[1]}" b="{c_[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0

# person→organization (worked_at)
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f,v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# person↔person (relationships)
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

tn = len(persons) + len(organizations)
te = len(positions) + len(relationships)
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone!")
