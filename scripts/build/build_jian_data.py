"""
Build SQLite database + GEXF graph for 吉安市 (Ji'an City) leadership network.
Focus: 市委书记 严允, 市长（空缺）, predecessor 罗文江 & 王亚联
调查日期: 2026-07-14
"""
import os
import sqlite3

# ── Paths ──────────────────────────────────────────────────────────────────────
DB_PATH = "data/database/jian_network.db"
GEXF_PATH = "data/graph/jian_network.gexf"

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# ── Hardcoded Research Data ────────────────────────────────────────────────────
# Sources: zh.wikipedia.org/wiki/吉安市; baike.baidu.com/item/严允; baike.baidu.com/item/罗文江 etc.

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Current leadership (from jian.gov.cn official site)
    # ══════════════════════════════════════════════════════════════════════
    # ── 市委书记 ──
    dict(id="jian_yan_yun", name="严允", gender="男", ethnicity="汉族",
         birth="1972-11", birthplace="江西石城", education="南昌大学中文系汉语言文学专业（大学学历）",
         party_join="1993-11", work_start="1994-07", current_post="吉安市委书记",
         current_org="中共吉安市委",
         source="baike.baidu.com/item/严允; jian.gov.cn/news-list-yanyun.html"),
    # ── 市长空缺 ── (since 2026年1月王亚联离任)
    # ── 市委副书记 ──
    dict(id="jian_wu_yanling", name="吴艳玲", gender="女", ethnicity="汉族",
         birth="1975-06", birthplace="", education="中央党校大学",
         party_join="中共党员", work_start="", current_post="吉安市委副书记",
         current_org="中共吉安市委",
         source="jian.gov.cn/news-list-wuyanling.html"),
    # ── 市委常委/常务副市长 ──
    dict(id="jian_wang_dasheng", name="王大胜", gender="男", ethnicity="汉族",
         birth="1969-11", birthplace="", education="中央党校大学",
         party_join="中共党员", work_start="", current_post="吉安市委常委、市政府党组副书记、副市长",
         current_org="吉安市人民政府",
         source="jian.gov.cn/news-list-wangdasheng.html"),
    # ── 市委常委/市纪委书记 ──
    dict(id="jian_chen_dingyu", name="陈定宇", gender="男", ethnicity="汉族",
         birth="1972-05", birthplace="", education="省委党校研究生",
         party_join="中共党员", work_start="", current_post="吉安市委常委、市纪委书记、市监委主任",
         current_org="中共吉安市纪委",
         source="jian.gov.cn/news-list-chendingyu.html"),
    # ── 市委常委/政法委书记 ──
    dict(id="jian_peng_xuekai", name="彭学凯", gender="男", ethnicity="汉族",
         birth="1966-04", birthplace="", education="中央党校研究生",
         party_join="中共党员", work_start="", current_post="吉安市委常委、政法委书记",
         current_org="中共吉安市委政法委",
         source="jian.gov.cn/news-list-pengxuekai.html"),
    # ── 市委常委/统战部长 ──
    dict(id="jian_liu_zhibin", name="刘志斌", gender="男", ethnicity="汉族",
         birth="1971-11", birthplace="", education="中央党校研究生",
         party_join="中共党员", work_start="", current_post="吉安市委常委、统战部部长",
         current_org="中共吉安市委统战部",
         source="jian.gov.cn/news-list-liuqzhigbinv.html"),
    # ── 市委常委/组织部长 ──
    dict(id="jian_gong_pingqiu", name="龚平秋", gender="男", ethnicity="汉族",
         birth="1970-06", birthplace="", education="省委党校研究生",
         party_join="中共党员", work_start="", current_post="吉安市委常委、组织部部长",
         current_org="中共吉安市委组织部",
         source="jian.gov.cn/news-list-gongpingqiu.html"),
    # ── 市委常委/军分区政委 ──
    dict(id="jian_chen_lizhong", name="陈李忠", gender="男", ethnicity="汉族",
         birth="1969-11", birthplace="", education="在职大学",
         party_join="中共党员", work_start="", current_post="吉安市委常委、吉安军分区政治委员",
         current_org="吉安军分区",
         source="jian.gov.cn/news-list-chenlizhong.html"),
    # ── 副市长团队 ──
    dict(id="jian_chen_qingshou", name="陈庆寿", gender="男", ethnicity="汉族",
         birth="1974-09", birthplace="", education="大学",
         party_join="中共党员", work_start="", current_post="吉安市副市长",
         current_org="吉安市人民政府",
         source="jian.gov.cn"),
    dict(id="jian_zhou_mi", name="周密", gender="女", ethnicity="汉族",
         birth="1967-10", birthplace="", education="大学",
         party_join="九三学社社员", work_start="", current_post="吉安市副市长",
         current_org="吉安市人民政府",
         source="jian.gov.cn"),
    dict(id="jian_liao_dongsheng", name="廖东生", gender="男", ethnicity="汉族",
         birth="1969-10", birthplace="", education="在职大学",
         party_join="中共党员", work_start="", current_post="吉安市副市长、井冈山管理局党工委书记",
         current_org="吉安市人民政府",
         source="jian.gov.cn"),
    dict(id="jian_zeng_jiaxin", name="曾家新", gender="男", ethnicity="汉族",
         birth="1977-06", birthplace="", education="省委党校研究生",
         party_join="中共党员", work_start="", current_post="吉安市副市长、市公安局局长",
         current_org="吉安市人民政府",
         source="jian.gov.cn"),
    dict(id="jian_lin_hao", name="林皓", gender="男", ethnicity="壮族",
         birth="1982-09", birthplace="", education="研究生",
         party_join="中共党员", work_start="", current_post="吉安市副市长（挂职）",
         current_org="吉安市人民政府",
         source="jian.gov.cn"),
    dict(id="jian_liu_yeqiu", name="刘烨球", gender="男", ethnicity="汉族",
         birth="1969-09", birthplace="", education="大学",
         party_join="中共党员", work_start="", current_post="吉安市人民政府秘书长",
         current_org="吉安市人民政府",
         source="jian.gov.cn"),
    # ── 人大领导 ──
    dict(id="jian_liao_hong", name="廖宏", gender="男", ethnicity="汉族",
         birth="1968-07", birthplace="重庆荣昌", education="大学学历",
         party_join="中共党员", work_start="", current_post="吉安市人大常委会主任",
         current_org="吉安市人大常委会",
         source="jasrd.gov.cn; zh.wikipedia.org/wiki/吉安市"),
    # ── 政协领导 ──
    dict(id="jian_xiao_yulan", name="肖玉兰", gender="女", ethnicity="汉族",
         birth="1966-07", birthplace="江西万安", education="省委党校研究生",
         party_join="中共党员", work_start="", current_post="吉安市政协主席",
         current_org="吉安市政协",
         source="zh.wikipedia.org/wiki/吉安市"),
    # ══════════════════════════════════════════════════════════════════════
    # Previous leadership (predecessors)
    # ══════════════════════════════════════════════════════════════════════
    dict(id="jian_luo_wenjiang", name="罗文江", gender="男", ethnicity="汉族",
         birth="1968-03", birthplace="江西德安", education="中央党校大学学历",
         party_join="中共党员", work_start="", current_post="（原吉安市委书记，2026年4月离任）",
         current_org="",
         source="zh.wikipedia.org/wiki/吉安市; jian.gov.cn"),
    dict(id="jian_wang_yalian", name="王亚联", gender="男", ethnicity="汉族",
         birth="1972-09", birthplace="江西九江", education="大学学历，公共管理硕士",
         party_join="中共党员", work_start="", current_post="（原吉安市市长，2026年1月离任）",
         current_org="",
         source="zh.wikipedia.org/wiki/吉安市"),
    dict(id="jian_wang_shaoxuan", name="王少玄", gender="男", ethnicity="汉族",
         birth="1967-10", birthplace="江西临川", education="省委党校研究生",
         party_join="中共党员", work_start="", current_post="江西省人大常委会副主任",
         current_org="江西省人大常委会",
         source="zh.wikipedia.org/wiki/王少玄"),
    dict(id="jian_hu_shizhong", name="胡世忠", gender="男", ethnicity="汉族",
         birth="1963-12", birthplace="江西武宁", education="研究生学历，工学硕士",
         party_join="中共党员", work_start="", current_post="江西省人大常委会副主任",
         current_org="江西省人大常委会",
         source="zh.wikipedia.org/wiki/胡世忠"),
    # ── Historical leaders ──────────────────────────────────────────────
    dict(id="jian_wang_ping", name="王萍", gender="女", ethnicity="汉族",
         birth="1962-05", birthplace="江西南昌", education="大学学历",
         party_join="中共党员", work_start="", current_post="（原吉安市委书记/市长，已退休）",
         current_org="",
         source="zh.wikipedia.org/wiki/王萍"),
    dict(id="jian_zhou_meng", name="周萌", gender="男", ethnicity="汉族",
         birth="1957-08", birthplace="江西丰城", education="中央党校大学",
         party_join="中共党员", work_start="", current_post="（原吉安市委书记/市长，已退休）",
         current_org="",
         source="zh.wikipedia.org/wiki/周萌"),
    # ── Cross-city connections (漆海云: 宜春→吉安→抚州) ─────────────
    dict(id="jian_qi_haiyun", name="漆海云", gender="男", ethnicity="汉族",
         birth="1970-06", birthplace="江西丰城", education="",
         party_join="中共党员", work_start="", current_post="（原吉安市委常委、副市长，已调抚州）",
         current_org="",
         source="pengpai news"),
]

organizations = [
    dict(id="org_jian_city", name="吉安市", type="行政区域", level="地级市", parent="江西省", location="江西省"),
    dict(id="org_jian_cpc", name="中共吉安市委", type="党委", level="地级市", parent="中共江西省委", location="吉安市"),
    dict(id="org_jian_gov", name="吉安市人民政府", type="政府", level="地级市", parent="吉安市", location="吉安市"),
    dict(id="org_jian_npc", name="吉安市人大常委会", type="人大", level="地级市", parent="吉安市", location="吉安市"),
    dict(id="org_jian_cppcc", name="吉安市政协", type="政协", level="地级市", parent="吉安市", location="吉安市"),
    dict(id="org_jian_discipline", name="中共吉安市纪委/监委", type="纪委", level="地级市", parent="中共吉安市委", location="吉安市"),
    dict(id="org_jian_politics_law", name="中共吉安市委政法委", type="党委", level="地级市", parent="中共吉安市委", location="吉安市"),
    dict(id="org_jian_org_dept", name="中共吉安市委组织部", type="党委", level="地级市", parent="中共吉安市委", location="吉安市"),
    dict(id="org_jian_united_front", name="中共吉安市委统战部", type="党委", level="地级市", parent="中共吉安市委", location="吉安市"),
    dict(id="org_jian_garrison", name="吉安军分区", type="军队", level="地级市", parent="江西省军区", location="吉安市"),
    dict(id="org_jian_police", name="吉安市公安局", type="政府", level="地级市部门", parent="吉安市人民政府", location="吉安市"),
    dict(id="org_jinggangshan_admin", name="井冈山管理局", type="事业单位", level="地级市", parent="吉安市", location="井冈山市"),
    dict(id="org_jiangxi_cpc", name="中共江西省委", type="党委", level="省级", parent="中共中央", location="南昌市"),
    dict(id="org_jiangxi_gov", name="江西省人民政府", type="政府", level="省级", parent="江西省", location="南昌市"),
    dict(id="org_jiangxi_npc", name="江西省人大常委会", type="人大", level="省级", parent="江西省", location="南昌市"),
    # 严允's previous orgs
    dict(id="org_jx_transport", name="江西省交通运输厅", type="政府", level="省级部门", parent="江西省人民政府", location="南昌市"),
    dict(id="org_jx_highway", name="江西省公路管理局", type="事业单位", level="省级", parent="江西省交通运输厅", location="南昌市"),
    dict(id="org_jx_port", name="江西省港航管理局", type="事业单位", level="省级", parent="江西省交通运输厅", location="南昌市"),
    dict(id="org_pingxiang_cpc", name="中共萍乡市委", type="党委", level="地级市", parent="中共江西省委", location="萍乡市"),
    dict(id="org_nanchang_cpc", name="中共南昌市委", type="党委", level="地级市", parent="中共江西省委", location="南昌市"),
    dict(id="org_yichun_cpc", name="中共宜春市委", type="党委", level="地级市", parent="中共江西省委", location="宜春市"),
    dict(id="org_yichun_gov", name="宜春市人民政府", type="政府", level="地级市", parent="宜春市", location="宜春市"),
    # 罗文江's previous orgs
    dict(id="org_jx_finance", name="江西省金融控股集团", type="事业单位", level="省级", parent="江西省人民政府", location="南昌市"),
    dict(id="org_ruichang_cpc", name="中共瑞昌市委", type="党委", level="县级市", parent="中共九江市委", location="瑞昌市"),
    dict(id="org_jiujiang_gov", name="九江市人民政府", type="政府", level="地级市", parent="九江市", location="九江市"),
    # 王亚联's previous orgs
    dict(id="org_jx_dev", name="江西省发展和改革委员会", type="政府", level="省级部门", parent="江西省人民政府", location="南昌市"),
    dict(id="org_jx_data", name="江西省大数据中心", type="事业单位", level="省级", parent="江西省人民政府", location="南昌市"),
    dict(id="org_jx_party_school", name="中共江西省委党校", type="事业单位", level="省级", parent="中共江西省委", location="南昌市"),
    # 漆海云's orgs
    dict(id="org_fuzhou_cpc", name="中共抚州市委", type="党委", level="地级市", parent="中共江西省委", location="抚州市"),
    dict(id="org_fuzhou_gov", name="抚州市人民政府", type="政府", level="地级市", parent="抚州市", location="抚州市"),
    # Unknown
    dict(id="org_unknown", name="（待查）", type="其他", level="未知", parent="", location="未知"),
]

positions = [
    # ── 严允 (Yan Yun) — 完整履历（来源：百度百科）─────────────────────
    # 教育
    dict(person_id="jian_yan_yun", org_id="org_unknown", title="南昌大学中文系汉语言文学专业学生",
         start="1990-09", end="1994-07", rank="", note="大学学历"),
    # 早期：省公路管理局
    dict(person_id="jian_yan_yun", org_id="org_jx_highway", title="江西省公路管理局宣传处干部",
         start="1994-07", end="2001-07", rank="科员", note="期间：1995.12-1997.08 320国道改建行政处干部"),
    dict(person_id="jian_yan_yun", org_id="org_jx_highway", title="江西省公路管理局宣传处副处长（正科级）",
         start="2001-07", end="2001-08", rank="正科级", note=""),
    # 省交通厅
    dict(person_id="jian_yan_yun", org_id="org_jx_transport", title="江西省交通厅办公室干部",
         start="2001-08", end="2002-08", rank="正科级", note=""),
    dict(person_id="jian_yan_yun", org_id="org_jx_transport", title="江西省交通厅办公室主任科员",
         start="2002-08", end="2004-03", rank="主任科员", note=""),
    dict(person_id="jian_yan_yun", org_id="org_jx_transport", title="江西省交通厅党办主任科员",
         start="2004-03", end="2004-12", rank="主任科员", note=""),
    dict(person_id="jian_yan_yun", org_id="org_jx_transport", title="江西省交通厅政策法规处副处长",
         start="2004-12", end="2006-10", rank="副处级", note=""),
    dict(person_id="jian_yan_yun", org_id="org_jx_transport", title="江西省交通厅党委办公室副主任、直属机关党委副书记",
         start="2006-10", end="2007-12", rank="副处级", note=""),
    dict(person_id="jian_yan_yun", org_id="org_jx_transport", title="江西省交通厅党委办公室主任、直属机关党委专职副书记",
         start="2007-12", end="2009-11", rank="正处级", note=""),
    dict(person_id="jian_yan_yun", org_id="org_jx_transport", title="江西省交通运输厅党委办公室主任、直属机关党委专职副书记",
         start="2009-11", end="2011-01", rank="正处级", note="期间：2010.03-2010.06江西省委党校第36期中青班学习"),
    # 省港航管理局
    dict(person_id="jian_yan_yun", org_id="org_jx_port", title="江西省港航管理局党委书记（副厅级）",
         start="2011-01", end="2017-09", rank="副厅级", note="期间：2013.03-2013.06江西省委省政府信访局接访处锻炼"),
    # 省交通运输厅
    dict(person_id="jian_yan_yun", org_id="org_jx_transport", title="江西省交通运输厅党委委员、副厅长",
         start="2017-09", end="2019-02", rank="副厅级", note=""),
    # 萍乡市委常委、组织部部长
    dict(person_id="jian_yan_yun", org_id="org_pingxiang_cpc", title="萍乡市委常委、组织部部长",
         start="2019-02", end="2020-06", rank="副厅级", note=""),
    # 南昌市委副书记
    dict(person_id="jian_yan_yun", org_id="org_nanchang_cpc", title="南昌市委副书记",
         start="2020-06", end="2021-02", rank="副厅级", note=""),
    # 宜春市长
    dict(person_id="jian_yan_yun", org_id="org_yichun_gov", title="宜春市委副书记、市政府党组书记、代市长",
         start="2021-02", end="2021-03", rank="正厅级", note=""),
    dict(person_id="jian_yan_yun", org_id="org_yichun_gov", title="宜春市委副书记、市长",
         start="2021-03", end="2023-08", rank="正厅级", note=""),
    # 宜春市委书记
    dict(person_id="jian_yan_yun", org_id="org_yichun_cpc", title="宜春市委书记、宜春军分区党委第一书记",
         start="2023-08", end="2026-04", rank="正厅级", note=""),
    # 吉安市委书记（现任）
    dict(person_id="jian_yan_yun", org_id="org_jian_cpc", title="吉安市委书记",
         start="2026-04", end="", rank="正厅级", note="现任；第十四届全国人大代表"),

    # ── 罗文江 (Luo Wenjiang) — 前任市委书记 ─────────────────────
    dict(person_id="jian_luo_wenjiang", org_id="org_jiujiang_gov", title="九江市人民政府副市长",
         start="~2015", end="~2019", rank="副厅级", note="具体起止年月待精确化"),
    dict(person_id="jian_luo_wenjiang", org_id="org_ruichang_cpc", title="瑞昌市委书记",
         start="~2019", end="~2020", rank="正处级", note=""),
    dict(person_id="jian_luo_wenjiang", org_id="org_jx_finance", title="江西省委金融工委副书记、省金融控股集团董事长",
         start="~2020", end="2021-04", rank="正厅级", note=""),
    dict(person_id="jian_luo_wenjiang", org_id="org_jian_gov", title="吉安市委副书记、市长",
         start="2021-04", end="2023-08", rank="正厅级", note=""),
    dict(person_id="jian_luo_wenjiang", org_id="org_jian_cpc", title="吉安市委书记",
         start="2023-08", end="2026-04", rank="正厅级", note="2026年4月离任"),

    # ── 王亚联 (Wang Yalian) — 前任市长 ────────────────────────────
    dict(person_id="jian_wang_yalian", org_id="org_jx_dev", title="江西省发展和改革委员会副主任",
         start="~2019", end="~2021", rank="副厅级", note=""),
    dict(person_id="jian_wang_yalian", org_id="org_jx_data", title="江西省大数据中心主任",
         start="~2021", end="2023-08", rank="正厅级", note=""),
    dict(person_id="jian_wang_yalian", org_id="org_jx_party_school", title="江西省委党校副校长",
         start="~2023", end="2023-08", rank="正厅级", note=""),
    dict(person_id="jian_wang_yalian", org_id="org_jian_gov", title="吉安市委副书记、市长",
         start="2023-08", end="2026-01", rank="正厅级", note="2026年1月离任"),

    # ── 王少玄 (Wang Shaoxuan) — 前任市委书记 ──────────────────────
    dict(person_id="jian_wang_shaoxuan", org_id="org_jian_gov", title="吉安市委副书记、市长",
         start="2015-02", end="2021-04", rank="正厅级", note=""),
    dict(person_id="jian_wang_shaoxuan", org_id="org_jian_cpc", title="吉安市委书记",
         start="2021-03", end="2023-08", rank="正厅级", note=""),

    # ── 胡世忠 (Hu Shizhong) — 前任市委书记 ──────────────────────────
    dict(person_id="jian_hu_shizhong", org_id="org_jian_gov", title="吉安市委副书记、市长",
         start="2011-09", end="2015-02", rank="正厅级", note=""),
    dict(person_id="jian_hu_shizhong", org_id="org_jian_cpc", title="吉安市委书记",
         start="2016-09", end="2021-03", rank="正厅级", note=""),
    dict(person_id="jian_hu_shizhong", org_id="org_jiangxi_npc", title="江西省人大常委会副主任",
         start="2021-03", end="", rank="副省级", note="现任"),

    # ── 吴艳玲 (Wu Yanling) 市委副书记 ───────────────────────────────
    dict(person_id="jian_wu_yanling", org_id="org_jian_cpc", title="吉安市委副书记",
         start="~2022-11", end="", rank="副厅级", note="现任；协助书记处理市委日常工作"),

    # ── 王大胜 (Wang Dasheng) 常务副市长 ─────────────────────────
    dict(person_id="jian_wang_dasheng", org_id="org_jian_cpc", title="吉安市委常委",
         start="~2022-11", end="", rank="副厅级", note="现任"),
    dict(person_id="jian_wang_dasheng", org_id="org_jian_gov", title="吉安市委常委、市政府党组副书记、副市长（常务）",
         start="~2022-11", end="", rank="副厅级", note="现任；协助市长负责市政府常务工作"),

    # ── 陈定宇 (Chen Dingyu) 纪委书记 ───────────────────────────────
    dict(person_id="jian_chen_dingyu", org_id="org_jian_cpc", title="吉安市委常委、市纪委书记",
         start="~2022", end="", rank="副厅级", note="现任"),
    dict(person_id="jian_chen_dingyu", org_id="org_jian_discipline", title="吉安市监委主任",
         start="~2022", end="", rank="副厅级", note="现任"),

    # ── 彭学凯 (Peng Xuekai) 政法委书记 ──────────────────────────────
    dict(person_id="jian_peng_xuekai", org_id="org_jian_cpc", title="吉安市委常委、政法委书记",
         start="~2022", end="", rank="副厅级", note="现任"),

    # ── 刘志斌 (Liu Zhibin) 统战部长 ─────────────────────────────────
    dict(person_id="jian_liu_zhibin", org_id="org_jian_cpc", title="吉安市委常委、统战部部长",
         start="~2022", end="", rank="副厅级", note="现任"),

    # ── 龚平秋 (Gong Pingqiu) 组织部长 ─────────────────────────────
    dict(person_id="jian_gong_pingqiu", org_id="org_jian_cpc", title="吉安市委常委、组织部部长",
         start="~2025-10", end="", rank="副厅级", note="现任；2025年10月加入常委"),

    # ── 陈李忠 (Chen Lizhong) 军分区政委 ────────────────────────────
    dict(person_id="jian_chen_lizhong", org_id="org_jian_cpc", title="吉安市委常委",
         start="~2020", end="", rank="副厅级", note="现任"),
    dict(person_id="jian_chen_lizhong", org_id="org_jian_garrison", title="吉安军分区政治委员",
         start="~2020", end="", rank="副厅级", note="现任"),

    # ── 陈庆寿 (Chen Qingshou) 副市长 ───────────────────────────────
    dict(person_id="jian_chen_qingshou", org_id="org_jian_gov", title="吉安市副市长",
         start="~2022", end="", rank="副厅级", note="现任；分管民政、退役军人、农业农村等"),

    # ── 周密 (Zhou Mi) 副市长（九三学社） ────────────────────────────
    dict(person_id="jian_zhou_mi", org_id="org_jian_gov", title="吉安市副市长",
         start="~2022", end="", rank="副厅级", note="现任；九三学社；分管教育体育、卫生健康等"),

    # ── 廖东生 (Liao Dongsheng) 副市长 ─────────────────────────────
    dict(person_id="jian_liao_dongsheng", org_id="org_jian_gov", title="吉安市副市长",
         start="~2022", end="", rank="副厅级", note="现任；兼井冈山管理局党工委书记"),
    dict(person_id="jian_liao_dongsheng", org_id="org_jinggangshan_admin", title="井冈山管理局党工委书记",
         start="~2022", end="", rank="副厅级", note="现任"),

    # ── 曾家新 (Zeng Jiaxin) 副市长/公安局长 ──────────────────────
    dict(person_id="jian_zeng_jiaxin", org_id="org_jian_gov", title="吉安市副市长",
         start="~2025-01", end="", rank="副厅级", note="现任"),
    dict(person_id="jian_zeng_jiaxin", org_id="org_jian_police", title="吉安市公安局党委书记、局长",
         start="~2025-01", end="", rank="正处级", note="现任"),

    # ── 林皓 (Lin Hao) 挂职副市长 ──────────────────────────────────
    dict(person_id="jian_lin_hao", org_id="org_jian_gov", title="吉安市副市长（挂职）",
         start="~2026-07", end="", rank="副厅级", note="现任；挂职干部"),

    # ── 刘烨球 (Liu Yeqiu) 市政府秘书长 ───────────────────────────
    dict(person_id="jian_liu_yeqiu", org_id="org_jian_gov", title="吉安市人民政府秘书长",
         start="~2022", end="", rank="正处级", note="现任"),

    # ── 廖宏 (Liao Hong) 人大常委会主任 ──────────────────────────────
    dict(person_id="jian_liao_hong", org_id="org_jian_npc", title="吉安市人大常委会主任",
         start="2021-10", end="", rank="正厅级", note="现任"),

    # ── 肖玉兰 (Xiao Yulan) 政协主席 ───────────────────────────────────
    dict(person_id="jian_xiao_yulan", org_id="org_jian_cppcc", title="吉安市政协主席",
         start="2025-01", end="", rank="正厅级", note="现任"),

    # ── 漆海云 (Qi Haiyun) 跨市交流 ──────────────────────────────────
    dict(person_id="jian_qi_haiyun", org_id="org_jian_gov", title="吉安市委常委、副市长",
         start="~2021-09", end="~2023-10", rank="副厅级", note="从宜春调吉安"),
    dict(person_id="jian_qi_haiyun", org_id="org_fuzhou_gov", title="抚州市委常委、常务副市长",
         start="~2023-10", end="~2025-07", rank="副厅级", note="从吉安调抚州"),
    dict(person_id="jian_qi_haiyun", org_id="org_fuzhou_cpc", title="抚州市委副书记",
         start="~2025-07", end="", rank="副厅级", note="现任"),

    # ── 王萍 (Wang Ping) 历史书记/市长 ─────────────────────────────────
    dict(person_id="jian_wang_ping", org_id="org_jian_gov", title="吉安市市长",
         start="2009-01", end="2011-09", rank="正厅级", note=""),
    dict(person_id="jian_wang_ping", org_id="org_jian_cpc", title="吉安市委书记",
         start="2011-08", end="2016-09", rank="正厅级", note=""),

    # ── 周萌 (Zhou Meng) 历史书记/市长 ─────────────────────────────────
    dict(person_id="jian_zhou_meng", org_id="org_jian_gov", title="吉安市市长",
         start="2006-10", end="2008-04", rank="正厅级", note=""),
    dict(person_id="jian_zhou_meng", org_id="org_jian_cpc", title="吉安市委书记",
         start="2008-03", end="2011-08", rank="正厅级", note=""),
]

relationships = [
    # ── 严允 → 罗文江: 接替市委书记 ───────────────────────────────
    dict(person_a="jian_yan_yun", person_b="jian_luo_wenjiang",
         type="职位接替", context="严允接替罗文江任吉安市委书记",
         overlap_org="中共吉安市委", overlap_period="2026-04"),
    # ── 严允 ↔ 罗文江: 宜春-吉安跨市交流 ──────────────────────────
    dict(person_a="jian_yan_yun", person_b="jian_luo_wenjiang",
         type="间接关系", context="严允曾任宜春市长/书记，罗文江曾任九江副市长，均为赣西干部交流圈成员",
         overlap_org="赣西地区干部圈", overlap_period=""),
    # ── 罗文江 → 王亚联: 市长-书记搭班 ────────────────────────────
    dict(person_a="jian_luo_wenjiang", person_b="jian_wang_yalian",
         type="工作关系", context="罗文江任市委书记，王亚联任市长，为党政正副手关系",
         overlap_org="吉安市", overlap_period="2023-08—2026-01"),
    # ── 罗文江 → 王少玄: 接替市委书记 ────────────────────────────
    dict(person_a="jian_luo_wenjiang", person_b="jian_wang_shaoxuan",
         type="职位接替", context="罗文江接替王少玄任吉安市委书记",
         overlap_org="中共吉安市委", overlap_period="2023-08"),
    # ── 王亚联 → 罗文江: 接替市长 ──────────────────────────────────
    dict(person_a="jian_wang_yalian", person_b="jian_luo_wenjiang",
         type="职位接替", context="王亚联接替罗文江任吉安市市长",
         overlap_org="吉安市人民政府", overlap_period="2023-08"),
    # ── 王少玄 → 胡世忠: 接替市委书记 ─────────────────────────────
    dict(person_a="jian_wang_shaoxuan", person_b="jian_hu_shizhong",
         type="职位接替", context="王少玄接替胡世忠任吉安市委书记",
         overlap_org="中共吉安市委", overlap_period="2021-03"),
    # ── 胡世忠 → 王少玄: 市长接替 ─────────────────────────────
    dict(person_a="jian_hu_shizhong", person_b="jian_wang_shaoxuan",
         type="职位接替", context="胡世忠升任省人大副主任后，王少玄由市长转任吉安市委书记",
         overlap_org="中共吉安市委", overlap_period="2021-03"),
    # ── 王少玄 → 胡世忠: 市长接替 ─────────────────────────────
    dict(person_a="jian_wang_shaoxuan", person_b="jian_hu_shizhong",
         type="职位接替", context="王少玄接替胡世忠任吉安市市长",
         overlap_org="吉安市人民政府", overlap_period="2015-02"),
    # ── 王萍 → 周萌: 接替市委书记 ────────────────────────────────
    dict(person_a="jian_wang_ping", person_b="jian_zhou_meng",
         type="职位接替", context="王萍接替周萌任吉安市委书记",
         overlap_org="中共吉安市委", overlap_period="2011-08"),
    # ── 严允 ↔ 廖宏: 四套班子关系 ──────────────────────────────────
    dict(person_a="jian_yan_yun", person_b="jian_liao_hong",
         type="工作关系", context="严允任市委书记，廖宏任市人大常委会主任，为四套班子关系",
         overlap_org="吉安市", overlap_period="2026-04-"),
    # ── 严允 ↔ 肖玉兰: 四套班子关系 ────────────────────────────────
    dict(person_a="jian_yan_yun", person_b="jian_xiao_yulan",
         type="工作关系", context="严允任市委书记，肖玉兰任市政协主席，为四套班子关系",
         overlap_org="吉安市", overlap_period="2026-04-"),
    # ── 王亚联 ↔ 肖玉兰: 搭班关系 ──────────────────────────────────
    dict(person_a="jian_wang_yalian", person_b="jian_xiao_yulan",
         type="工作关系", context="王亚联任市长期间，肖玉兰由市委副书记转任政协主席",
         overlap_org="吉安市", overlap_period="2023-08—2026-01"),
    # ── 严允的跨市连接：萍乡→南昌→宜春→吉安 ──────────────────────
    dict(person_a="jian_yan_yun", person_b="jian_luo_wenjiang",
         type="间接关系", context="严允（萍乡、南昌、宜春背景）与罗文江（九江/瑞昌背景），分属赣西和赣北干部圈，需进一步确认交集",
         overlap_org="", overlap_period=""),
    # ── 严允 ↔ 吴艳玲: 党政正副手 ────────────────────────────────────
    dict(person_a="jian_yan_yun", person_b="jian_wu_yanling",
         type="工作关系", context="严允任市委书记，吴艳玲任市委副书记，为党政正副手关系",
         overlap_org="中共吉安市委", overlap_period="2026-04-"),
    # ── 严允 ↔ 王大胜: 市委书记-常务副市长 ───────────────────────────
    dict(person_a="jian_yan_yun", person_b="jian_wang_dasheng",
         type="工作关系", context="严允任市委书记，王大胜任常务副市长，为党政工作关系",
         overlap_org="吉安市", overlap_period="2026-04-"),
    # ── 严允 ↔ 陈定宇: 党委书记-纪委书记 ────────────────────────────
    dict(person_a="jian_yan_yun", person_b="jian_chen_dingyu",
         type="工作关系", context="严允任市委书记，陈定宇任市纪委书记，为同级党委-纪委关系",
         overlap_org="中共吉安市委", overlap_period="2026-04-"),
    # ── 严允 ↔ 彭学凯: 党委书记-政法委书记 ──────────────────────────
    dict(person_a="jian_yan_yun", person_b="jian_peng_xuekai",
         type="工作关系", context="严允任市委书记，彭学凯任政法委书记，为工作关系",
         overlap_org="中共吉安市委", overlap_period="2026-04-"),
    # ── 漆海云: 宜春→吉安→抚州 跨市交流 ──────────────────────────
    dict(person_a="jian_qi_haiyun", person_b="jian_yan_yun",
         type="间接关系", context="漆海云（宜春→吉安→抚州）与严允（宜春→吉安）均有宜春-吉安跨市交流背景",
         overlap_org="宜春-吉安干部走廊", overlap_period=""),
    # ── 漆海云 ↔ 罗文江: 曾在吉安同班子 ────────────────────────────
    dict(person_a="jian_qi_haiyun", person_b="jian_luo_wenjiang",
         type="工作关系", context="漆海云任吉安市委常委、副市长期间，罗文江任市委书记",
         overlap_org="吉安市", overlap_period="2023-08—2023-10"),
]

# ── Build SQLite ─────────────────────────────────────────────────────────────────
def build_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
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
        CREATE INDEX IF NOT EXISTS idx_person_name ON persons(name);
        CREATE INDEX IF NOT EXISTS idx_org_name ON organizations(name);
        CREATE INDEX IF NOT EXISTS idx_pos_person ON positions(person_id);
        CREATE INDEX IF NOT EXISTS idx_pos_org ON positions(org_id);
    """)
    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES(:id,:name,:gender,:ethnicity,:birth,:birthplace,:education,:party_join,:work_start,:current_post,:current_org,:source)", p)
    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES(:id,:name,:type,:level,:parent,:location)", o)
    for p in positions:
        c.execute("INSERT OR REPLACE INTO positions(person_id,org_id,title,start,end,rank,note) VALUES(:person_id,:org_id,:title,:start,:end,:rank,:note)", p)
    for r in relationships:
        c.execute("INSERT OR REPLACE INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period) VALUES(:person_a,:person_b,:type,:context,:overlap_org,:overlap_period)", r)
    conn.commit()
    for tbl in ["persons","organizations","positions","relationships"]:
        cnt = c.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        print(f"  {tbl}: {cnt}")
    conn.close()

# ── Build GEXF ───────────────────────────────────────────────────────────────────
def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    def color(r, g, b):
        return f'<viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>'

    def node_size(p):
        title = p["current_post"]
        if p["current_org"] == "" and not title.startswith("（原"):
            return "8.0"
        if "书记" in title and "副" not in title and "副书记" not in title:
            return "20.0"
        if "市长" in title and "副" not in title:
            return "20.0"
        return "12.0"

    def person_color(p):
        title = p["current_post"]
        if "书记" in title and "副" not in title and "副书记" not in title:
            return color(220, 50, 50)  # red = top party secretary
        if "市长" in title and "副" not in title:
            return color(50, 100, 220)  # blue = government lead
        if "常务" in title or "党组副书记" in title:
            return color(50, 150, 255)  # light blue = executive deputy
        if "副市长" in title:
            return color(100, 120, 255)  # lighter blue = deputy gov
        if "人大" in title:
            return color(60, 180, 75)  # green = people's congress
        if "政协" in title:
            return color(60, 180, 75)  # green = political consult
        if "纪委" in title:
            return color(255, 165, 0)   # orange = discipline
        if "副" in title:
            return color(160, 130, 80)  # brown = deputy
        return color(100, 100, 100)     # grey = other

    def org_color(o):
        otype = o["type"]
        if "党委" in otype: return color(240, 120, 120)
        if "政府" in otype or "行政" in otype: return color(120, 180, 240)
        if "人大" in otype or "政协" in otype: return color(120, 220, 140)
        if "事业单位" in otype: return color(200, 200, 200)
        return color(180, 180, 180)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append("<graph mode=\"static\" defaultedgetype=\"undirected\">")

    # Attributes
    lines.append("""<attributes class="node">
        <attribute id="type" title="type" type="string"/>
        <attribute id="birth" title="birth" type="string"/>
        <attribute id="birthplace" title="birthplace" type="string"/>
        <attribute id="current_post" title="current_post" type="string"/>
        <attribute id="entity_type" title="entity_type" type="string"/>
        <attribute id="level" title="level" type="string"/>
    </attributes>
    <attributes class="edge">
        <attribute id="type" title="type" type="string"/>
        <attribute id="start" title="start" type="string"/>
        <attribute id="end" title="end" type="string"/>
        <attribute id="context" title="context" type="string"/>
    </attributes>""")

    # Nodes
    lines.append("<nodes>")
    for p in persons:
        sz = node_size(p)
        c = person_color(p)
        lines.append(f"""<node id="{esc(p['id'])}" label="{esc(p['name'])}">
        {c}
        <viz:size value="{sz}"/>
        <attvalues>
            <attvalue for="type" value="person"/>
            <attvalue for="birth" value="{esc(p['birth'])}"/>
            <attvalue for="birthplace" value="{esc(p['birthplace'])}"/>
            <attvalue for="current_post" value="{esc(p['current_post'])}"/>
            <attvalue for="entity_type" value="person"/>
            <attvalue for="level" value=""/>
        </attvalues>
    </node>""")
    for o in organizations:
        c = org_color(o)
        lines.append(f"""<node id="{esc(o['id'])}" label="{esc(o['name'])}">
        {c}
        <viz:size value="8.0"/>
        <attvalues>
            <attvalue for="type" value="organization"/>
            <attvalue for="birth" value=""/>
            <attvalue for="birthplace" value=""/>
            <attvalue for="current_post" value=""/>
            <attvalue for="entity_type" value="org"/>
            <attvalue for="level" value="{esc(o['level'])}"/>
        </attvalues>
    </node>""")
    lines.append("</nodes>")

    # Edges
    lines.append("<edges>")
    edge_id = 0
    for pos in positions:
        edge_id += 1
        start = esc(pos.get("start", ""))
        end = esc(pos.get("end", ""))
        note = esc(pos.get("note", ""))
        lines.append(f"""<edge id="{edge_id}" source="{esc(pos['person_id'])}" target="{esc(pos['org_id'])}" weight="1.0">
        <attvalues>
            <attvalue for="type" value="worked_at"/>
            <attvalue for="start" value="{start}"/>
            <attvalue for="end" value="{end}"/>
            <attvalue for="context" value="{esc(pos['title'])}. {note}"/>
        </attvalues>
    </edge>""")
    for rel in relationships:
        edge_id += 1
        ctx = esc(rel.get("context", ""))
        period = esc(rel.get("overlap_period", ""))
        w = "2.0" if rel["type"] in ("工作关系", "职位接替") else "1.0"
        lines.append(f"""<edge id="{edge_id}" source="{esc(rel['person_a'])}" target="{esc(rel['person_b'])}" weight="{w}">
        <attvalues>
            <attvalue for="type" value="{esc(rel['type'])}"/>
            <attvalue for="start" value=""/>
            <attvalue for="end" value=""/>
            <attvalue for="context" value="{ctx} ({period})"/>
        </attvalues>
    </edge>""")
    lines.append("</edges>")
    lines.append("</graph></gexf>")

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {edge_id} edges written")

# ── Main ─────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== 吉安市 (Ji'an) Leadership Network ===")
    print("[SQLite]")
    build_sqlite()
    print("[GEXF]")
    build_gexf()
    print("Done.")
