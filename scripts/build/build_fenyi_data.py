"""
Build SQLite database + GEXF graph for 分宜县 (Fenyi County, under 新余市, Jiangxi).
County party secretary: 邹家洪 (Zou Jiahong) — 2021~2025
County chief: 谢淘 (Xie Tao) — 2021~present

Data sources:
  - Baidu Baike: 分宜县, 邹家洪, 谢淘, 胡瑜瑞, 黄斯文
  - thepaper.cn articles on 分宜县 leadership appointments
  - jxnews.com.cn (大江网/新余频道) leadership meeting reports
  - 分宜县人民政府网站 (fenyi.gov.cn)
  - baike.baidu.com / 中文百科全书
"""
import os
import sqlite3
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────────────────
DB_PATH = "data/database/fenyi_network.db"
GEXF_PATH = "data/graph/fenyi_network.gexf"

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# ── Hardcoded Research Data ────────────────────────────────────────────────────
# Person ID convention: fenyi_{surname_givenname}

persons = [
    # ═══ County Party Secretary (县委书记) ═══
    dict(id="fenyi_zou_jiahong", name="邹家洪", gender="男", ethnicity="汉族",
         birth="1970-04", birthplace="江西遂川",
         education="江西省委党校经济学专业在职研究生",
         party_join="1991-12", work_start="1992-08",
         current_post="（原分宜县委书记，已任新余市委常委、宣传部部长）",
         current_org="中共新余市委",
         source="baike.baidu.com; thepaper.cn/newsDetail_forward_30434821"),

    # ═══ County Chief (县长) ═══
    dict(id="fenyi_xie_tao", name="谢淘", gender="男", ethnicity="汉族",
         birth="1989-09", birthplace="江西万载",
         education="清华大学环境工程专业博士研究生",
         party_join="2008-12", work_start="2015-08",
         current_post="县委副书记、县长",
         current_org="分宜县人民政府",
         source="baike.baidu.com/item/谢淘; thepaper.cn/newsDetail_forward_13871696"),

    # ═══ Deputy Party Secretary (县委副书记) ═══
    dict(id="fenyi_zhong_yuhong", name="钟宇虹", gender="女", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="县委副书记（专职）",
         current_org="中共分宜县委",
         source="jxnews.com.cn meeting reports (2021~2024)"),

    # ═══ Standing Committee (县委常委) ═══
    dict(id="fenyi_liu_jun", name="刘军", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="县委常委、宣传部部长",
         current_org="中共分宜县委宣传部",
         source="jxnews.com.cn (分宜县委常委、宣传部长刘军到分宜五中调研 2022-02-22)"),

    dict(id="fenyi_chen_zhenggen", name="陈正根", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="县委常委、组织部部长（原任，后调整）",
         current_org="中共分宜县委",
         source="分宜县第十五届县委第一次全会选举结果 (2021-09)"),

    dict(id="fenyi_xiahou_yun", name="夏侯云", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="县委常委、常务副县长",
         current_org="分宜县人民政府",
         source="jxnews.com.cn;分宜县第十七届人大一次会议选举结果 (2021-10)"),

    dict(id="fenyi_he_yonggang", name="何勇刚", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="县委常委、县纪委书记、县监委主任",
         current_org="中共分宜县纪律检查委员会",
         source="分宜县第十七届人大一次会议选举结果 (2021-10)"),

    dict(id="fenyi_zhou_jinlin", name="周金林", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="县委常委",
         current_org="中共分宜县委",
         source="分宜县第十五届县委第一次全会选举结果 (2021-09)"),

    dict(id="fenyi_hu_min", name="胡旻", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="县委常委",
         current_org="中共分宜县委",
         source="分宜县第十五届县委第一次全会选举结果 (2021-09)"),

    dict(id="fenyi_luo_yanbing", name="罗艳兵", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="县委常委、副县长",
         current_org="分宜县人民政府",
         source="分宜县第十五届县委第一次全会选举结果;jxnews.com.cn (2021-10)"),

    dict(id="fenyi_kang_xueguang", name="康学光", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="县委常委、政法委书记",
         current_org="中共分宜县委政法委员会",
         source="jxnews.com.cn (分宜县委政法委第二次全体会议 2022-07-12)"),

    dict(id="fenyi_deng_gaoping", name="邓高萍", gender="女", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="县委常委",
         current_org="中共分宜县委",
         source="分宜县第十五届县委第一次全会选举结果 (2021-09)"),

    # ═══ Vice County Chiefs (副县长) ═══
    dict(id="fenyi_li_jianjun", name="李建军", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="副县长（兼分宜工业园区党工委书记）",
         current_org="分宜县人民政府",
         source="分宜县第十七届人大一次会议; 宜春职业技术学院座谈会报道 (2024-09)"),

    dict(id="fenyi_guo_xiaoping", name="郭小平", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="副县长",
         current_org="分宜县人民政府",
         source="分宜县第十七届人大一次会议选举结果 (2021-10)"),

    dict(id="fenyi_jiang_xiaobin", name="蒋晓斌", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="副县长、县公安局局长",
         current_org="分宜县公安局",
         source="分宜县第十七届人大一次会议选举结果 (2021-10)"),

    dict(id="fenyi_huang_huang", name="黄璜", gender="女", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="副县长",
         current_org="分宜县人民政府",
         source="分宜县第十七届人大一次会议选举结果 (2021-10)"),

    dict(id="fenyi_zhang_xiaobing", name="张小兵", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="副县长",
         current_org="分宜县人民政府",
         source="分宜县第十七届人大一次会议选举结果 (2021-10)"),

    dict(id="fenyi_huang_lei", name="黄磊", gender="女", ethnicity="汉族",
         birth="1986-05", birthplace="",
         education="在职研究生学历",
         party_join="中共党员", work_start="",
         current_post="副县长（2024年11月任命）",
         current_org="分宜县人民政府",
         source="jxnews.com.cn (2024-11-08 任命); 原渝水区良山镇党委书记"),

    # ═══ NPC & CPPCC ═══
    dict(id="fenyi_hu_yurui", name="胡瑜瑞", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="县人大常委会主任",
         current_org="分宜县人民代表大会常务委员会",
         source="baike.baidu.com; 分宜县第十七届人大一次会议选举结果 (2021-10)"),

    dict(id="fenyi_huang_siwen", name="黄斯文", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="县政协主席",
         current_org="中国人民政治协商会议分宜县委员会",
         source="baike.baidu.com; 中文百科全书"),

    # ═══ Predecessor & Historical ═══
    dict(id="fenyi_li_yixiang", name="李逸翔", gender="男", ethnicity="汉族",
         birth="1968-07", birthplace="",
         education="中央党校在职研究生学历",
         party_join="中共党员", work_start="",
         current_post="（原分宜县委书记，2015-2021年任职，后另有任用）",
         current_org="",
         source="ifeng.com 江西分宜1年2换县委书记报道; 任前公示 2015-09"),

    dict(id="fenyi_liu_qiong", name="刘琼", gender="女", ethnicity="汉族",
         birth="1967-04", birthplace="",
         education="中央党校在职研究生学历",
         party_join="中共党员", work_start="",
         current_post="（原分宜县委书记，2014-2015年任职）",
         current_org="",
         source="ifeng.com 江西分宜1年2换县委书记报道"),

    dict(id="fenyi_yao_lingshu", name="姚灵目", gender="男", ethnicity="汉族",
         birth="1965-10", birthplace="",
         education="研究生学历",
         party_join="中共党员", work_start="",
         current_post="（原分宜县委书记、县长；系江西省原副省长姚木根之弟）",
         current_org="",
         source="ifeng.com 江西分宜1年2换县委书记报道"),

    dict(id="fenyi_hu_jun", name="胡军", gender="男", ethnicity="汉族",
         birth="", birthplace="",
         education="",
         party_join="", work_start="",
         current_post="（原分宜县委副书记、县长，2014-2021年任职）",
         current_org="",
         source="ifeng.com 报道; 分宜县政府官网"),

    # ═══ New party secretary (successor) ═══
    dict(id="fenyi_zhang_tao", name="张涛", gender="男", ethnicity="汉族",
         birth="1975-10", birthplace="",
         education="在职大学",
         party_join="中共党员", work_start="",
         current_post="分宜县委书记（2025年5月接任）",
         current_org="中共分宜县委",
         source="thepaper.cn/newsDetail_forward_30891747; baike.baidu.com"),

    # ═══ Xinyu City leaders (parent city) ═══
    dict(id="xinyu_fang_xiangjun", name="方向军", gender="男", ethnicity="汉族",
         birth="1970-10", birthplace="浙江省淳安县",
         education="大学学历、工商管理硕士（MBA）/管理学硕士",
         party_join="", work_start="1996-07",
         current_post="市委书记",
         current_org="中共新余市委",
         source="build_xinyu_data.py (existing project data)"),
]

organizations = [
    # ── County-level orgs ──
    dict(id="org_fenyi_county", name="分宜县", type="行政区域", level="县级", parent="新余市", location="江西省新余市"),
    dict(id="org_fenyi_cpc", name="中共分宜县委", type="党委", level="县处级", parent="中共新余市委", location="分宜县"),
    dict(id="org_fenyi_gov", name="分宜县人民政府", type="政府", level="县处级", parent="新余市人民政府", location="分宜县"),
    dict(id="org_fenyi_discipline", name="中共分宜县纪律检查委员会", type="纪委", level="县处级", parent="新余市纪委监委", location="分宜县"),
    dict(id="org_fenyi_org_dept", name="中共分宜县委组织部", type="党委部门", level="乡科级", parent="中共分宜县委", location="分宜县"),
    dict(id="org_fenyi_propaganda", name="中共分宜县委宣传部", type="党委部门", level="乡科级", parent="中共分宜县委", location="分宜县"),
    dict(id="org_fenyi_legal", name="中共分宜县委政法委员会", type="党委部门", level="乡科级", parent="中共分宜县委", location="分宜县"),
    dict(id="org_fenyi_npc", name="分宜县人民代表大会常务委员会", type="人大", level="县处级", parent="新余市人大常委会", location="分宜县"),
    dict(id="org_fenyi_cppcc", name="中国人民政治协商会议分宜县委员会", type="政协", level="县处级", parent="新余市政协", location="分宜县"),
    dict(id="org_fenyi_police", name="分宜县公安局", type="政府", level="乡科级", parent="分宜县人民政府", location="分宜县"),
    dict(id="org_fenyi_industrial_park", name="分宜工业园区", type="开发区", level="县级", parent="分宜县人民政府", location="分宜县"),
    dict(id="org_fenyi_procuratorate", name="分宜县人民检察院", type="司法", level="县处级", parent="新余市人民检察院", location="分宜县"),
    dict(id="org_fenyi_court", name="分宜县人民法院", type="司法", level="县处级", parent="新余市中级人民法院", location="分宜县"),

    # ── Xinyu City-level orgs (parent hierarchy) ──
    dict(id="org_xinyu_cpc", name="中共新余市委", type="党委", level="地级市", parent="中共江西省委", location="新余市"),
    dict(id="org_xinyu_gov", name="新余市人民政府", type="政府", level="地级市", parent="江西省人民政府", location="新余市"),
]

positions = [
    # ── 邹家洪 (Zou Jiahong) — full career ──
    dict(person_id="fenyi_zou_jiahong", org_id="org_xinyu_cpc", title="新余市委常委、宣传部部长", start="2025-03", end="", rank="副厅级",
         note="现任"),
    dict(person_id="fenyi_zou_jiahong", org_id="org_fenyi_cpc", title="分宜县委书记", start="2021-08", end="2025-03", rank="县处级正职",
         note="2021年7月任前公示，8月3日到任；主持县委全面工作"),
    dict(person_id="fenyi_zou_jiahong", org_id="org_xinyu_gov", title="新余市渝水区委副书记、区政府党组书记、区长",
         start="2020-05", end="2021-07", rank="县处级正职", note="2020年5月任渝水区代区长，6月当选"),
    dict(person_id="fenyi_zou_jiahong", org_id="org_xinyu_gov", title="吉安市国有资产监督管理委员会主任",
         start="~2018", end="~2020", rank="正处级", note=""),
    dict(person_id="fenyi_zou_jiahong", org_id="org_xinyu_gov", title="吉安市政府办党组成员、副秘书长",
         start="~2017", end="~2018", rank="正处级", note=""),
    dict(person_id="fenyi_zou_jiahong", org_id="org_xinyu_gov", title="吉安市旅游发展委员会党组书记、主任",
         start="~2016", end="~2017", rank="正处级", note="前身为吉安市旅游局"),
    dict(person_id="fenyi_zou_jiahong", org_id="org_xinyu_gov", title="吉安市旅游局党组书记、局长",
         start="~2015", end="~2016", rank="正处级", note=""),
    dict(person_id="fenyi_zou_jiahong", org_id="org_xinyu_gov", title="永丰县委副书记（正县级）",
         start="~2014", end="~2015", rank="正处级", note=""),
    dict(person_id="fenyi_zou_jiahong", org_id="org_xinyu_gov", title="新疆克州州委副秘书长（正县级，援疆）",
         start="~2011", end="~2014", rank="正处级", note="援疆干部"),
    dict(person_id="fenyi_zou_jiahong", org_id="org_xinyu_gov", title="吉安市青原区委常委、副区长（正县级）",
         start="~2010", end="~2011", rank="正处级", note=""),
    dict(person_id="fenyi_zou_jiahong", org_id="org_xinyu_gov", title="吉安市青原区委常委、宣传部部长",
         start="~2007", end="~2010", rank="副处级", note=""),
    dict(person_id="fenyi_zou_jiahong", org_id="org_xinyu_gov", title="吉安市青原区政府副区长",
         start="~2002", end="~2007", rank="副处级", note=""),
    dict(person_id="fenyi_zou_jiahong", org_id="org_xinyu_gov", title="吉安师专英语系干部",
         start="1992-08", end="~1995", rank="", note="早期职业生涯起点"),

    # ── 谢淘 (Xie Tao) — full career ──
    dict(person_id="fenyi_xie_tao", org_id="org_fenyi_gov", title="分宜县委副书记、县长",
         start="2021-10", end="", rank="县处级正职", note="现任；2021年8月任代县长，10月当选"),
    dict(person_id="fenyi_xie_tao", org_id="org_fenyi_cpc", title="分宜县委副书记",
         start="2021-08", end="", rank="县处级正职", note="兼任"),
    dict(person_id="fenyi_xie_tao", org_id="org_xinyu_gov", title="新余市渝水区委常委、水北镇党委书记",
         start="2020-10", end="2021-07", rank="县处级副职", note=""),
    dict(person_id="fenyi_xie_tao", org_id="org_xinyu_gov", title="新余市渝水区副区长、水北镇党委书记",
         start="2019-11", end="2020-10", rank="县处级副职", note=""),
    dict(person_id="fenyi_xie_tao", org_id="org_xinyu_gov", title="新余市渝水区副区长（挂职福建省泉州市鲤城区副区长）",
         start="2018-11", end="2019-11", rank="县处级副职", note="挂职"),
    dict(person_id="fenyi_xie_tao", org_id="org_xinyu_gov", title="新余市渝水区副区长",
         start="2017-12", end="2018-11", rank="县处级副职", note="时年28岁"),
    dict(person_id="fenyi_xie_tao", org_id="org_xinyu_gov", title="仙女湖区河下镇党委副书记（挂职）、新余市委农工部主任科员",
         start="2016", end="2017-12", rank="乡科级", note="选调生基层锻炼"),
    dict(person_id="fenyi_xie_tao", org_id="org_xinyu_gov", title="新余市委农工部干部（省委组织部选调生）",
         start="2015-08", end="2016", rank="", note="江西省首批北大清华定向选调生"),

    # ── 钟宇虹 ──
    dict(person_id="fenyi_zhong_yuhong", org_id="org_fenyi_cpc", title="县委副书记（专职）",
         start="2021-09", end="", rank="县处级副职", note="现任"),

    # ── 刘军 ──
    dict(person_id="fenyi_liu_jun", org_id="org_fenyi_cpc", title="县委常委",
         start="2021-09", end="", rank="县处级副职", note="现任"),
    dict(person_id="fenyi_liu_jun", org_id="org_fenyi_propaganda", title="宣传部部长",
         start="~2021", end="", rank="县处级副职", note="现任"),

    # ── 陈正根 ──
    dict(person_id="fenyi_chen_zhenggen", org_id="org_fenyi_cpc", title="县委常委、组织部部长",
         start="2021-09", end="~2024", rank="县处级副职", note="第十五届县委常委，后可能调整"),

    # ── 夏侯云 ──
    dict(person_id="fenyi_xiahou_yun", org_id="org_fenyi_cpc", title="县委常委",
         start="2021-09", end="", rank="县处级副职", note="现任"),
    dict(person_id="fenyi_xiahou_yun", org_id="org_fenyi_gov", title="常务副县长",
         start="2021-10", end="", rank="县处级副职", note="现任"),

    # ── 何勇刚 ──
    dict(person_id="fenyi_he_yonggang", org_id="org_fenyi_cpc", title="县委常委、县纪委书记",
         start="2021-09", end="", rank="县处级副职", note="现任"),
    dict(person_id="fenyi_he_yonggang", org_id="org_fenyi_discipline", title="县纪委书记、县监委主任",
         start="2021-09", end="", rank="县处级副职", note="现任"),

    # ── 周金林 ──
    dict(person_id="fenyi_zhou_jinlin", org_id="org_fenyi_cpc", title="县委常委",
         start="2021-09", end="", rank="县处级副职", note="现任"),

    # ── 胡旻 ──
    dict(person_id="fenyi_hu_min", org_id="org_fenyi_cpc", title="县委常委",
         start="2021-09", end="", rank="县处级副职", note="现任"),

    # ── 罗艳兵 ──
    dict(person_id="fenyi_luo_yanbing", org_id="org_fenyi_cpc", title="县委常委",
         start="2021-09", end="", rank="县处级副职", note="现任"),
    dict(person_id="fenyi_luo_yanbing", org_id="org_fenyi_gov", title="副县长",
         start="2021-10", end="", rank="县处级副职", note="现任"),

    # ── 康学光 ──
    dict(person_id="fenyi_kang_xueguang", org_id="org_fenyi_cpc", title="县委常委",
         start="2021-09", end="", rank="县处级副职", note="现任"),
    dict(person_id="fenyi_kang_xueguang", org_id="org_fenyi_legal", title="政法委书记",
         start="~2022", end="", rank="县处级副职", note="现任"),

    # ── 邓高萍 ──
    dict(person_id="fenyi_deng_gaoping", org_id="org_fenyi_cpc", title="县委常委",
         start="2021-09", end="", rank="县处级副职", note="现任"),

    # ── 李建军 ──
    dict(person_id="fenyi_li_jianjun", org_id="org_fenyi_gov", title="副县长",
         start="2018-08", end="", rank="县处级副职", note="连任多届"),
    dict(person_id="fenyi_li_jianjun", org_id="org_fenyi_industrial_park", title="分宜工业园区党工委书记（兼）",
         start="~2021", end="", rank="", note="兼任"),

    # ── 郭小平 ──
    dict(person_id="fenyi_guo_xiaoping", org_id="org_fenyi_gov", title="副县长",
         start="2021-10", end="", rank="县处级副职", note="现任"),

    # ── 蒋晓斌 ──
    dict(person_id="fenyi_jiang_xiaobin", org_id="org_fenyi_gov", title="副县长",
         start="2021-10", end="", rank="县处级副职", note="现任"),
    dict(person_id="fenyi_jiang_xiaobin", org_id="org_fenyi_police", title="县公安局局长",
         start="2021-10", end="", rank="乡科级正职", note="现任"),

    # ── 黄璜 ──
    dict(person_id="fenyi_huang_huang", org_id="org_fenyi_gov", title="副县长",
         start="2021-10", end="", rank="县处级副职", note="现任"),

    # ── 张小兵 ──
    dict(person_id="fenyi_zhang_xiaobing", org_id="org_fenyi_gov", title="副县长",
         start="2021-10", end="", rank="县处级副职", note="现任"),

    # ── 黄磊 ──
    dict(person_id="fenyi_huang_lei", org_id="org_fenyi_gov", title="副县长",
         start="2024-11", end="", rank="县处级副职", note="2024年11月7日县人大常委会任命"),

    # ── 胡瑜瑞 ──
    dict(person_id="fenyi_hu_yurui", org_id="org_fenyi_npc", title="县人大常委会主任",
         start="2021-10", end="", rank="县处级正职", note="现任"),

    # ── 黄斯文 ──
    dict(person_id="fenyi_huang_siwen", org_id="org_fenyi_cppcc", title="县政协主席",
         start="~2016", end="", rank="县处级正职", note="现任"),

    # ── 李逸翔 (predecessor party secretary) ──
    dict(person_id="fenyi_li_yixiang", org_id="org_fenyi_cpc", title="分宜县委书记",
         start="2015-09", end="2021-07", rank="县处级正职", note="接替刘琼"),

    # ── 刘琼 (predecessor party secretary) ──
    dict(person_id="fenyi_liu_qiong", org_id="org_fenyi_cpc", title="分宜县委书记",
         start="2014-12", end="2015-09", rank="县处级正职", note="原县委副书记、县长升任"),
    dict(person_id="fenyi_liu_qiong", org_id="org_fenyi_gov", title="分宜县县长",
         start="~2011", end="2014-12", rank="县处级正职", note=""),

    # ── 姚灵目 (predecessor party secretary) ──
    dict(person_id="fenyi_yao_lingshu", org_id="org_fenyi_cpc", title="分宜县委书记",
         start="~2011", end="2014-12", rank="县处级正职", note="江西省原副省长姚木根之弟"),
    dict(person_id="fenyi_yao_lingshu", org_id="org_fenyi_gov", title="分宜县县长",
         start="~2007", end="~2011", rank="县处级正职", note=""),

    # ── 胡军 (predecessor county chief) ──
    dict(person_id="fenyi_hu_jun", org_id="org_fenyi_gov", title="分宜县委副书记、县长",
         start="2014-12", end="2021-07", rank="县处级正职", note=""),

    # ── 张涛 (successor party secretary) ──
    dict(person_id="fenyi_zhang_tao", org_id="org_fenyi_cpc", title="分宜县委书记、县人武部党委第一书记",
         start="2025-05", end="", rank="县处级正职", note="现任；原新余市工信局局长"),

    # ── 方向军 (Xinyu city party secretary) ──
    dict(person_id="xinyu_fang_xiangjun", org_id="org_xinyu_cpc", title="新余市委书记、新余军分区党委第一书记",
         start="2026-04", end="", rank="正厅级", note="现任"),
]

relationships = [
    # ── 邹家洪 ↔ 谢淘: 党政搭档 (2021~2025) ──
    dict(person_a="fenyi_zou_jiahong", person_b="fenyi_xie_tao",
         type="工作关系", context="邹家洪任县委书记、谢淘任县长，为党政正副手搭档（2021.08~2025.03）",
         overlap_org="分宜县", overlap_period="2021-2025"),

    # ── 邹家洪 → 李逸翔: 职位接替 ──
    dict(person_a="fenyi_zou_jiahong", person_b="fenyi_li_yixiang",
         type="职位接替", context="邹家洪接替李逸翔任分宜县委书记",
         overlap_org="中共分宜县委", overlap_period="2021"),

    # ── 邹家洪 → 张涛: 被接替 ──
    dict(person_a="fenyi_zou_jiahong", person_b="fenyi_zhang_tao",
         type="职位接替", context="邹家洪升任新余市委常委，张涛接替分宜县委书记",
         overlap_org="中共分宜县委", overlap_period="2025"),

    # ── 邹家洪 ↔ 刘琼: 前任关系 ──
    dict(person_a="fenyi_liu_qiong", person_b="fenyi_li_yixiang",
         type="职位接替", context="刘琼被李逸翔接替",
         overlap_org="中共分宜县委", overlap_period="2015"),

    # ── 姚灵目 ↔ 刘琼: 职位接替 ──
    dict(person_a="fenyi_yao_lingshu", person_b="fenyi_liu_qiong",
         type="职位接替", context="姚灵目卸任后刘琼升任书记",
         overlap_org="中共分宜县委", overlap_period="2014"),

    # ── 谢淘 ↔ 夏侯云: 政府正副手 ──
    dict(person_a="fenyi_xie_tao", person_b="fenyi_xiahou_yun",
         type="工作关系", context="谢淘县长与夏侯云常务副县长为正副手关系",
         overlap_org="分宜县人民政府", overlap_period="2021-"),

    # ── 谢淘 → 胡军: 职位接替 ──
    dict(person_a="fenyi_xie_tao", person_b="fenyi_hu_jun",
         type="职位接替", context="谢淘接替胡军任分宜县长",
         overlap_org="分宜县人民政府", overlap_period="2021"),

    # ── 邹家洪 ↔ 方向军: 上下级关系（新余市层面） ──
    dict(person_a="fenyi_zou_jiahong", person_b="xinyu_fang_xiangjun",
         type="工作关系", context="邹家洪任新余市委常委，方向军为市委书记，为上下级",
         overlap_org="中共新余市委", overlap_period="2025-"),

    # ── 谢淘 ↔ 方向军: 上下级关系 ──
    dict(person_a="fenyi_xie_tao", person_b="xinyu_fang_xiangjun",
         type="工作关系", context="谢陶任分宜县长，方向军为新余市委书记，为上下级",
         overlap_org="新余市", overlap_period="2024-"),

    # ── 邹家洪 → 渝水区任职: 谢淘也在渝水区共事 ──
    dict(person_a="fenyi_zou_jiahong", person_b="fenyi_xie_tao",
         type="同城任职", context="邹家洪2020-2021任渝水区长，谢淘2017-2021在渝水区任职，曾在同一区共事",
         overlap_org="渝水区", overlap_period="2020-2021"),

    # ── 邹家洪 ↔ 李逸翔: 同在新余市 ──
    dict(person_a="fenyi_li_yixiang", person_b="fenyi_yao_lingshu",
         type="同城任职", context="历任分宜县委书记",
         overlap_org="中共分宜县委", overlap_period="2011-2021"),
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
        if not p["current_org"] and not title.startswith("（"):  # skip shadow nodes
            return "8.0"
        if "书记" in title and "副" not in title and "副书记" not in title:
            return "20.0"
        if "县长" in title or "区长" in title:
            return "20.0"
        return "12.0"

    def person_color(p):
        title = p["current_post"]
        if "书记" in title and "副" not in title and "副书记" not in title:
            return color(220, 50, 50)  # red = top party secretary
        if "县长" in title or "区长" in title or "市长" in title:
            return color(50, 100, 220)  # blue = government lead
        if "常务" in title or "党组副书记" in title:
            return color(50, 150, 255)  # light blue = executive deputy
        if "副县长" in title or "副区长" in title or "副市长" in title:
            return color(100, 120, 255)  # lighter blue = deputy gov
        if "人大" in title or "政协" in title:
            return color(60, 180, 75)  # green = people's congress/political consult
        if "纪委" in title:
            return color(255, 165, 0)   # orange = discipline
        if "组织部" in title:
            return color(200, 100, 200)  # purple = org dept
        if "宣传" in title:
            return color(200, 150, 50)   # gold = propaganda
        if "政法" in title:
            return color(150, 100, 200)  # violet = legal affairs
        if "副" in title:
            return color(160, 130, 80)  # brown = deputy
        return color(100, 100, 100)     # grey = other

    def org_color(o):
        otype = o["type"]
        if "党委" in otype: return color(240, 120, 120)
        if "政府" in otype or "行政" in otype: return color(120, 180, 240)
        if "人大" in otype or "政协" in otype: return color(120, 220, 140)
        if "纪委" in otype: return color(255, 200, 100)
        if "司法" in otype: return color(200, 180, 220)
        if "开发区" in otype: return color(180, 220, 180)
        if "党委部门" in otype: return color(220, 180, 180)
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
        current_org = esc(p["current_org"]) if p["current_org"] else "N/A"
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
    print("=== 分宜县 (Fenyi County) Leadership Network ===")
    print("[SQLite]")
    build_sqlite()
    print("[GEXF]")
    build_gexf()
    print("Done.")
