#!/usr/bin/env python3
"""
南昌市青山湖区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Qingshanhu District leadership.
"""

import sqlite3
import os

# ── DATA ──
# Person ID convention: qsh_{surname_givenname}

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source
    # Top leaders
    ("qsh_yang_yuxing", "杨育星", "男", "汉族", "1975年5月", "江西南昌", "研究生/工学硕士（南昌大学环境工程）", "中共党员", "1997年8月", "区委书记", "中共南昌市青山湖区委员会", "http://ncqsh.nc.gov.cn/ncqsh/qwsj/202105/40e6b23b80e34e82b5e1133c29b60592.shtml"),
    ("qsh_gong_feixia", "龚飞霞", "女", "汉族", "1980年10月", "江西南昌县", "省委党校研究生/法学学士", "中共党员", "2003年7月", "区委副书记、代区长", "南昌市青山湖区人民政府", "http://ncqsh.nc.gov.cn/ncqsh/qwfsj/202502/926ba36f6dc341aa82086e58805b4693.shtml"),
    # Standing committee (8 priority targets + role info from official bios)
    ("qsh_mao_tao", "毛涛", "男", "汉族", "1988年2月", "江西永丰", "在职研究生/公共管理硕士", "中共党员", "2010年7月", "区委常委、副区长", "南昌市青山湖区人民政府", "http://ncqsh.nc.gov.cn/ncqsh/qwcw/202003/93d4baf3c751414e9067b96db7ca0845.shtml"),
    ("qsh_yang_feng", "杨峰", "男", "汉族", "1980年10月", "江西南昌", "大学学历", "中共党员", "2003年11月", "区委常委、常务副区长", "南昌市青山湖区人民政府", "http://ncqsh.nc.gov.cn/ncqsh/qwcw/202003/463ab7f4ffde45b4a64d8ce03a256af5.shtml"),
    ("qsh_wu_qinghe", "吴庆和", "男", "汉族", "1976年1月", "江西宜黄", "全日制大学本科学历", "中共党员", "1999年7月", "区委常委、宣传部部长", "中共南昌市青山湖区委宣传部", "http://ncqsh.nc.gov.cn/ncqsh/qwcw/202410/9e25a37ed32f4f308d4e9a3cc805c6c1.shtml"),
    ("qsh_fu_lei", "付磊", "男", "汉族", "1981年10月", "江西都昌", "华中科技大学新闻学/大学学历", "中共党员", "2004年7月", "区委常委、组织部部长", "中共南昌市青山湖区委组织部", "http://ncqsh.nc.gov.cn/ncqsh/qwcw/202507/9f005bdfc13347d99727450dce541f4a.shtml"),
    ("qsh_niu_hao", "牛浩", "男", "汉族", "1983年9月", "山东邹城", "山东经济学院/管理学学士", "中共党员", "2008年6月", "区委常委、高新园区党工委书记、罗家镇党委书记", "南昌青山湖高新技术产业园区", "http://ncqsh.nc.gov.cn/ncqsh/qwcw/202307/cf447a1859d24fa48c100a4e075f3e2a.shtml"),
    ("qsh_cai_zhigang", "蔡志刚", "男", "汉族", "1974年12月", "江西南昌", "大学学历", "中共党员", "1995年12月", "区委常委、政法委书记", "中共南昌市青山湖区委政法委员会", "http://ncqsh.nc.gov.cn/ncqsh/qwcw/202003/3f422b69ed8e445796e1cdc7f8484475.shtml"),
    ("qsh_liu_wei", "刘伟", "男", "汉族", "1984年5月", "江西吉水", "大学学历/哲学学士", "中共党员", "2005年6月", "区委常委、人武部政委", "南昌市青山湖区人民武装部", "http://ncqsh.nc.gov.cn/ncqsh/qwcw/202509/a1307dc6f78b4c6895129609f3d537b9.shtml"),
    ("qsh_peng_lingqian", "彭凌迁", "男", "回族", "1988年11月", "江西南昌", "在职研究生/工商管理硕士", "中共党员", "2011年9月", "区委常委、区纪委书记、区监委主任", "中共南昌市青山湖区纪律检查委员会", "http://ncqsh.nc.gov.cn/ncqsh/qwcw/202511/e5e4d83170dd4af5aa3b5b1e1fde7871.shtml"),
    # Vice-mayors (5, non-standing committee)
    ("qsh_wang_guang", "王光", "男", "汉族", "1979年2月", "江西南昌县", "未查到", "民进会员", "未查到", "副区长（民进）", "南昌市青山湖区人民政府", "http://ncqsh.nc.gov.cn/ncqsh/ldxx/leader.shtml"),
    ("qsh_yu_wei", "余炜", "男", "汉族", "1968年11月", "江西南昌", "中央党校函授学院法律本科（南昌市人民警察学校起点）", "中共党员", "1988年", "副区长、青山湖公安分局局长", "南昌市公安局青山湖分局", "baike.baidu.com"),
    ("qsh_mao_yanbin", "毛演斌", "男", "汉族", "1974年7月", "江西南昌", "在职大学学历（南昌高等专科学校起点）", "中共党员", "1996年8月", "副区长", "南昌市青山湖区人民政府", "网易《南昌92名处级干部任前公示》2021-08-19"),
    ("qsh_peng_xiaojian", "彭小建", "男", "汉族", "1979年7月", "江西遂川", "大学/文学学士", "中共党员", "未查到", "副区长", "南昌市青山湖区人民政府", "http://ncqsh.nc.gov.cn/ncqsh/ldxx/leader.shtml"),
    ("qsh_yu_jing", "余婧", "女", "汉族", "1986年11月", "江西景德镇", "工学学士", "中共党员", "未查到", "副区长", "南昌市青山湖区人民政府", "http://ncqsh.nc.gov.cn/ncqsh/ldxx/leader.shtml"),
    # Predecessors & connections (3)
    ("qsh_yuan_yidan", "袁一旦", "男", "汉族", "1970年4月", "江西分宜", "中国地质大学(武汉)/工学学士", "2000年4月", "1992年6月", "南昌市人大常委会副主任（原区委书记）", "南昌市人大常委会", "baike.baidu.com"),
    ("qsh_ye_fei", "叶飞", "男", "汉族", "未查到", "未查到", "未查到", "中共党员", "2001年9月", "进贤县委副书记（青山湖成长干部）", "中共进贤县委员会", "baike.baidu.com"),
    ("qsh_li_songdian", "李松殿", "男", "汉族", "未查到", "未查到", "未查到", "中共党员", "未查到", "南昌市委常委/宣传部部长/新建区委书记", "中共南昌市委宣传部", "baike.baidu.com"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("qsh_party_committee", "中共南昌市青山湖区委员会", "党委", "县级", "中共南昌市委", "南昌市青山湖区"),
    ("qsh_gov", "南昌市青山湖区人民政府", "政府", "县级", "南昌市人民政府", "南昌市青山湖区"),
    ("qsh_org_department", "中共南昌市青山湖区委组织部", "党委部门", "正科级", "青山湖区委", "南昌市青山湖区"),
    ("qsh_discipline", "中共南昌市青山湖区纪律检查委员会", "纪委", "县级", "南昌市纪委", "南昌市青山湖区"),
    ("qsh_propaganda", "中共南昌市青山湖区委宣传部", "党委部门", "正科级", "青山湖区委", "南昌市青山湖区"),
    ("qsh_political_legal", "中共南昌市青山湖区委政法委员会", "党委部门", "正科级", "青山湖区委", "南昌市青山湖区"),
    ("qsh_armed_forces", "南昌市青山湖区人民武装部", "军队", "县级", "南昌警备区", "南昌市青山湖区"),
    ("qsh_high_tech_park", "南昌青山湖高新技术产业园区", "开发区", "省级", "青山湖区委/区政府", "南昌市青山湖区"),
    ("qsh_luojia_town", "青山湖区罗家镇", "乡镇", "正科级", "青山湖区委/区政府", "南昌市青山湖区罗家镇"),
    ("nanchang_npc", "南昌市人大常委会", "人大", "地厅级", "南昌市人民代表大会", "南昌市"),
    ("jinxian_county_committee", "中共进贤县委员会", "党委", "县级", "中共南昌市委", "进贤县"),
    ("anyi_county_committee", "中共安义县委员会", "党委", "县级", "中共南昌市委", "安义县"),
    ("xihu_district_committee", "中共西湖区委员会", "党委", "县级", "中共南昌市委", "南昌市西湖区"),
    ("nanchang_discipline", "中共南昌市纪律检查委员会", "纪委", "地厅级", "江西省纪委", "南昌市"),
    ("qingyunpu_daishan_st", "青云谱区岱山街道", "街道", "正科级", "青云谱区委/区政府", "南昌市青云谱区"),
    ("qingyunpu_sanjiadian_st", "青云谱区三家店街道", "街道", "正科级", "青云谱区委/区政府", "南昌市青云谱区"),
    ("anyi_discipline", "安义县纪委监委", "纪委", "县级", "安义县委/南昌市纪委", "安义县"),
    ("nanchang_transport", "南昌市交通运输局", "政府机构", "正县级", "南昌市人民政府", "南昌市"),
    ("nanchang_fgw", "南昌市发展和改革委员会", "政府机构", "正县级", "南昌市人民政府", "南昌市"),
    ("yongfeng_town", "永丰县瑶田镇", "乡镇", "正科级", "永丰县委/县政府", "永丰县"),
    ("donghu_street", "东湖区墩子塘街道", "街道", "正科级", "东湖区委/区政府", "南昌市东湖区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 杨育星 — 6 positions ═══
    ("qsh_yang_yuxing", "qsh_party_committee", "区委书记", "2026-07", "至今", "正县级", "主持区委全面工作"),
    ("qsh_yang_yuxing", "qsh_gov", "区长", "2021-10", "2026-07", "正县级", "前职"),
    ("qsh_yang_yuxing", "qsh_party_committee", "区委副书记、代区长", "2021-04", "2021-10", "正县级", "到任青山湖区"),
    ("qsh_yang_yuxing", "xihu_district_committee", "青云谱区委副书记", "~2019", "2021-04", "副县级", ""),
    ("qsh_yang_yuxing", "qsh_gov", "青云谱区委常委、副区长（常务）", "~2016", "~2019", "副县级", ""),
    ("qsh_yang_yuxing", "qsh_gov", "青云谱区委常委、组织部部长", "~2014", "~2016", "副县级", ""),

    # ═══ 龚飞霞 — 7 positions (full career) ═══
    ("qsh_gong_feixia", "qsh_party_committee", "区委副书记、代区长", "2026-07", "至今", "正县级", ""),
    ("qsh_gong_feixia", "qsh_party_committee", "区委副书记、统战部部长", "2025-02", "2026-06", "副县级", ""),
    ("qsh_gong_feixia", "anyi_discipline", "安义县委常委、县纪委书记、县监委主任", "2021-09", "2025-01", "副县级", ""),
    ("qsh_gong_feixia", "qingyunpu_sanjiadian_st", "三家店街道党工委书记", "~2020", "2020-12", "正科级", ""),
    ("qsh_gong_feixia", "qingyunpu_daishan_st", "岱山街道党工委书记", "~2015", "~2020", "正科级", ""),
    ("qsh_gong_feixia", "qingyunpu_daishan_st", "岱山街道党工委副书记、办事处主任", "~2012", "~2015", "正科级", ""),
    ("qsh_gong_feixia", "nanchang_discipline", "副科级纪检员（→正科级）", "2003-07", "~2008", "副科→正科", "南昌市纪委起步"),

    # ═══ 袁一旦 — 8 positions (full career) ═══
    ("qsh_yuan_yidan", "nanchang_npc", "市人大常委会副主任（专职）", "2026-07", "至今", "副厅级", ""),
    ("qsh_yuan_yidan", "qsh_party_committee", "区委书记（兼市人大副主任）", "2025-01", "2026-07", "正县级→副厅级", ""),
    ("qsh_yuan_yidan", "qsh_party_committee", "区委书记", "2021-04", "2025-01", "正县级", ""),
    ("qsh_yuan_yidan", "qsh_party_committee", "区委副书记、区长", "2020-04", "2021-04", "正县级", ""),
    ("qsh_yuan_yidan", "nanchang_transport", "南昌市交通运输局局长", "2019-02", "2020-04", "正县级", ""),
    ("qsh_yuan_yidan", "xihu_district_committee", "西湖区委副书记", "~2016", "2019-02", "副县级", ""),
    ("qsh_yuan_yidan", "jinxian_county_committee", "进贤县委常委、常务副县长", "~2012", "~2016", "副县级", ""),
    ("qsh_yuan_yidan", "anyi_county_committee", "安义县副县长", "2006", "~2012", "副县级", ""),

    # ═══ 叶飞 — 8 positions (full career) ═══
    ("qsh_ye_fei", "jinxian_county_committee", "进贤县委副书记", "2024-11", "至今", "副县级", ""),
    ("qsh_ye_fei", "anyi_county_committee", "安义县委副书记", "~2023", "2024-11", "副县级", ""),
    ("qsh_ye_fei", "anyi_county_committee", "安义县委常委、常务副县长", "2021-08", "~2023", "副县级", ""),
    ("qsh_ye_fei", "qsh_propaganda", "区委常委、宣传部部长", "2020-07", "2021-08", "副县级", ""),
    ("qsh_ye_fei", "qsh_gov", "副区长", "2016-10", "2017-12", "副县级", ""),
    ("qsh_ye_fei", "qsh_gov", "区政府办公室主任", "2015-02", "2016-07", "正科级", ""),
    ("qsh_ye_fei", "qsh_luojia_town", "南钢街道党工委书记", "2013-08", "2015-02", "正科级", ""),
    ("qsh_ye_fei", "qsh_luojia_town", "扬子洲镇镇长", "2011-05", "2013-08", "正科级", ""),

    # ═══ 李松殿 — 1 current position ═══
    ("qsh_li_songdian", "qsh_gov", "南昌市委常委/宣传部部长/新建区委书记", "当前", "至今", "副厅级", ""),

    # ═══ 牛浩 — 12 positions (FULL career from official bio) ═══
    ("qsh_niu_hao", "qsh_high_tech_park", "区委常委、高新园区党工委书记、罗家镇党委书记", "2025-06", "至今", "副县级", ""),
    ("qsh_niu_hao", "qsh_propaganda", "区委常委、统战部部长、高新园区党工委书记", "2024-02", "2025-06", "副县级", ""),
    ("qsh_niu_hao", "qsh_propaganda", "区委常委、统战部部长", "2023-07", "2024-02", "副县级", "从西湖区副区长调任"),
    ("qsh_niu_hao", "xihu_district_committee", "南昌市西湖区政府党组成员、副区长", "2021-08", "2023-07", "副县级", ""),
    ("qsh_niu_hao", "anyi_county_committee", "安义工业园区挂职党工委副书记、管委会副主任", "2020-06", "2021-08", "正科级", "市发改委科长期间挂职"),
    ("qsh_niu_hao", "nanchang_transport", "南昌市发改委规划科科长", "2020-10", "2021-08", "正科级", "机构改革后科室更名"),
    ("qsh_niu_hao", "nanchang_transport", "南昌市发改委规划处处长", "2019-06", "2020-10", "正科级", ""),
    ("qsh_niu_hao", "nanchang_transport", "南昌市发改委产业处处长", "2017-12", "2019-06", "正科级", ""),
    ("qsh_niu_hao", "nanchang_transport", "南昌市发改委产业处副处长(主持工作)", "2015-12", "2017-12", "副科级", ""),
    ("qsh_niu_hao", "nanchang_transport", "南昌市发改委环资处副处长", "2012-04", "2015-12", "副科级", ""),
    ("qsh_niu_hao", "nanchang_transport", "南昌市发改委工交处科员", "2008-06", "2012-04", "科员", "省发改委帮助工作2013-2014"),
    ("qsh_niu_hao", "nanchang_transport", "毕业待分配", "2007-07", "2008-06", "—", "山东经济学院毕业"),

    # ═══ 彭凌迁 — 7 positions (from official bio) ═══
    ("qsh_peng_lingqian", "qsh_discipline", "区委常委、区纪委书记、区监委主任", "现任", "至今", "副县级", "四级高级监察官"),
    ("qsh_peng_lingqian", "nanchang_discipline", "南昌市纪委市监委（工作）", "~2019", "~2025", "—", "具体职务待查"),
    ("qsh_peng_lingqian", "qsh_gov", "江西省政府办公厅（工作）", "~2017", "~2019", "—", "具体职务待查"),
    ("qsh_peng_lingqian", "qsh_high_tech_park", "江西省林业厅（工作）", "~2015", "~2017", "—", "具体职务待查"),
    ("qsh_peng_lingqian", "qsh_org_department", "南昌县委组织部（工作）", "~2013", "~2015", "—", "具体职务待查"),
    ("qsh_peng_lingqian", "qsh_luojia_town", "南昌县东新乡（工作）", "2011-09", "~2013", "—", "乡镇基层起步"),
    ("qsh_peng_lingqian", "qsh_luojia_town", "南昌大学 本科/研究生", "2007", "2011", "—", "应届毕业参加工作"),

    # ═══ 毛涛 — 12 positions (FULL career from official bio) ═══
    ("qsh_mao_tao", "qsh_gov", "区委常委、副区长", "2023-07", "至今", "副县级", "分管商务/人社/市监等"),
    ("qsh_mao_tao", "qsh_propaganda", "区委常委、统战部长,区政协党组副书记", "2021-08", "2023-07", "副县级", "从省政协下派到地方"),
    ("qsh_mao_tao", "qsh_party_committee", "江西省政协办公厅会议处副处长", "2019-03", "2021-08", "副处级", "省级机关"),
    ("qsh_mao_tao", "qsh_party_committee", "江西省政协办公厅秘书处主任科员", "2015-12", "2019-03", "主任科员", ""),
    ("qsh_mao_tao", "qsh_party_committee", "江西省政协办公厅秘书处副主任科员", "2013-02", "2015-12", "副主任科员", ""),
    ("qsh_mao_tao", "yongfeng_town", "江西省永丰县瑶田镇综治办专职副主任(借调县委办)", "2012-12", "2013-02", "—", "乡镇综治"),
    ("qsh_mao_tao", "yongfeng_town", "江西省永丰县瑶田镇政府宣传干事", "2010-06", "2012-12", "—", "乡镇宣传"),
    ("qsh_mao_tao", "yongfeng_town", "江西省永丰县潭城乡辋川村委会大学生村官", "2009-09", "2010-06", "—", "大学生村官"),
    ("qsh_mao_tao", "qsh_party_committee", "待业", "2009-06", "2009-09", "—", "黄冈师范学院毕业"),

    # ═══ 杨峰 — positions (FULL career from official bio) ═══
    ("qsh_yang_feng", "qsh_gov", "区委常委、区政府党组副书记、常务副区长", "现任", "至今", "副县级", "分管发改/财政/统计/教育等"),
    ("qsh_yang_feng", "xihu_district_committee", "青云谱区政府（工作）", "~2017", "~2025", "—", "具体职务待查"),
    ("qsh_yang_feng", "qsh_org_department", "东湖区八一桥街办（工作）", "~2015", "~2017", "—", ""),
    ("qsh_yang_feng", "qsh_org_department", "东湖区政府办（工作）", "~2013", "~2015", "—", ""),
    ("qsh_yang_feng", "qsh_propaganda", "东湖区文明办（工作）", "~2010", "~2013", "—", ""),
    ("qsh_yang_feng", "qsh_propaganda", "东湖区委宣传部（工作）", "~2006", "~2010", "—", ""),
    ("qsh_yang_feng", "qsh_luojia_town", "东湖区墩子塘街办（工作）", "2003-11", "~2006", "—", "基层起步"),

    # ═══ 吴庆和 — 7 positions (FULL career from official bio) ═══
    ("qsh_wu_qinghe", "qsh_propaganda", "区委常委、宣传部部长", "现任", "至今", "副县级", ""),
    ("qsh_wu_qinghe", "jinxian_county_committee", "进贤县委常委、宣传部部长", "~2021", "~2025", "副县级", ""),
    ("qsh_wu_qinghe", "nanchang_discipline", "南昌市委宣传部副调研员（四级调研员）", "~2017", "~2021", "副处级", ""),
    ("qsh_wu_qinghe", "nanchang_discipline", "南昌市委宣传部舆情信息处处长", "~2014", "~2017", "正科级", ""),
    ("qsh_wu_qinghe", "nanchang_discipline", "南昌市委宣传部外宣处副处长", "~2009", "~2014", "副科级", ""),
    ("qsh_wu_qinghe", "nanchang_discipline", "南昌市委宣传部科员、副主任科员", "~2003", "~2009", "科员", ""),
    ("qsh_wu_qinghe", "qsh_luojia_town", "江西宜黄二中教师", "1999-07", "~2003", "—", "教师起步"),

    # ═══ 付磊 — 5 positions (FULL career from official bio) ═══
    ("qsh_fu_lei", "qsh_org_department", "区委常委、组织部部长、区委党校校长（兼）", "现任", "至今", "副县级", ""),
    ("qsh_fu_lei", "qsh_org_department", "南昌市委办公室副主任、市档案局局长", "~2020", "~2025", "副县级", ""),
    ("qsh_fu_lei", "qsh_propaganda", "南昌市委常委会秘书", "~2017", "~2020", "正科级", ""),
    ("qsh_fu_lei", "qsh_propaganda", "南昌市委办公厅综合一处副处长", "~2012", "~2017", "副科级", ""),
    ("qsh_fu_lei", "qsh_org_department", "（南昌市委办公厅起步）", "2004-07", "~2012", "—", "华中科技大学新闻学毕业"),

    # ═══ 蔡志刚 — 18 positions (FULL career from official bio) ═══
    ("qsh_cai_zhigang", "qsh_political_legal", "区委常委、政法委书记", "2025-04", "至今", "副县级", ""),
    ("qsh_cai_zhigang", "qsh_political_legal", "区委常委", "2025-03", "2025-04", "副县级", "过渡期"),
    ("qsh_cai_zhigang", "qsh_gov", "区政府党组成员、副区长", "2021-10", "2025-03", "副县级", ""),
    ("qsh_cai_zhigang", "qsh_gov", "区政府副区长提名人选", "2021-08", "2021-10", "副县级", ""),
    ("qsh_cai_zhigang", "qsh_gov", "区财政局党组书记、局长", "2020-10", "2021-08", "正科级", ""),
    ("qsh_cai_zhigang", "qsh_gov", "区市监局党委书记、局长", "2019-02", "2020-10", "正科级", ""),
    ("qsh_cai_zhigang", "qsh_gov", "区城管委党委书记、主任、武装部第一部长", "2017-07", "2019-02", "正科级", ""),
    ("qsh_cai_zhigang", "qsh_party_committee", "待安排", "2017-05", "2017-07", "—", "机构调整过渡"),
    ("qsh_cai_zhigang", "qsh_gov", "区总工会党组副书记、常务副主席", "2016-04", "2017-05", "正科级", ""),
    ("qsh_cai_zhigang", "qsh_luojia_town", "罗家镇党委书记", "2013-12", "2016-04", "正科级", ""),
    ("qsh_cai_zhigang", "qsh_luojia_town", "罗家镇党委副书记、镇长", "2012-08", "2013-12", "正科级", ""),
    ("qsh_cai_zhigang", "qsh_luojia_town", "京东镇党委副书记、镇长", "2011-05", "2012-08", "正科级", ""),
    ("qsh_cai_zhigang", "qsh_luojia_town", "扬子洲镇党委委员、副书记", "2010-07", "2011-05", "副科级", "撤乡设镇"),
    ("qsh_cai_zhigang", "qsh_luojia_town", "扬子洲乡党委委员、副书记", "2007-06", "2010-07", "副科级", ""),
    ("qsh_cai_zhigang", "qsh_luojia_town", "罗家镇党委委员、副镇长", "2006-03", "2007-06", "副科级", ""),
    ("qsh_cai_zhigang", "qsh_luojia_town", "扬子洲乡党委委员、副乡长", "2003-09", "2006-03", "副科级", ""),
    ("qsh_cai_zhigang", "qsh_luojia_town", "扬子洲乡副乡长", "2002-06", "2003-09", "副科级", "郊区→青山湖区区划调整"),
    ("qsh_cai_zhigang", "qsh_luojia_town", "南昌市郊区扬子洲乡副乡长", "2001-12", "2002-06", "副科级", ""),
    ("qsh_cai_zhigang", "qsh_gov", "南昌市郊区交通局干部", "1995-12", "2001-12", "科员", "西北政法学院毕业"),

    # ═══ 刘伟 — 3 positions ═══
    ("qsh_liu_wei", "qsh_armed_forces", "区委常委、人武部政委", "现任", "至今", "副县级", ""),
    ("qsh_liu_wei", "qsh_armed_forces", "南昌市青山湖区政府党组成员、人武部政委", "~2025", "现任", "副县级", ""),
    ("qsh_liu_wei", "qsh_armed_forces", "南昌市东湖区人武部政委", "~2022", "~2025", "副县级", "军转干部"),

    # ═══ 余炜 — 9 positions (FULL career from official sources) ═══
    ("qsh_yu_wei", "qsh_gov", "青山湖区副区长、公安分局局长", "2021-10", "至今", "副县级", "分管公安/消防/维稳"),
    ("qsh_yu_wei", "nanchang_transport", "南昌市公安局东湖分局局长", "~2018", "2021-10", "正处级", ""),
    ("qsh_yu_wei", "anyi_county_committee", "安义县公安局局长、政委、副县长", "~2013", "~2018", "副县级", ""),
    ("qsh_yu_wei", "nanchang_transport", "南昌市公安局缉毒支队支队长", "~2010", "~2013", "正科级", ""),
    ("qsh_yu_wei", "nanchang_transport", "南昌市公安局东湖分局副局长", "~2007", "~2010", "副科级", ""),
    ("qsh_yu_wei", "nanchang_transport", "南昌市公安局刑侦支队二大队大队长", "~2003", "~2007", "副科级", ""),
    ("qsh_yu_wei", "nanchang_transport", "南昌市公安局刑侦支队案件审理科科长", "~2000", "~2003", "正科级", ""),
    ("qsh_yu_wei", "nanchang_transport", "南昌市公安局西湖分局刑侦队科员", "1988", "~2000", "科员", "南昌市人民警察学校毕业"),
    # ═══ 毛演斌 — 6 positions (FULL career from official sources) ═══
    ("qsh_mao_yanbin", "qsh_gov", "青山湖区副区长", "2021-10", "至今", "副县级", "分管城管/农业/环保/水务"),
    ("qsh_mao_yanbin", "qsh_gov", "新建区住房和城乡建设局党组书记、局长", "~2019", "2021-08", "正科级", "任前公示确认"),
    ("qsh_mao_yanbin", "qsh_gov", "新建区石埠乡党委副书记、乡长", "~2016", "~2019", "正科级", ""),
    ("qsh_mao_yanbin", "qsh_gov", "新建县乐化镇党委副书记、纪委书记", "~2010", "~2016", "副科级", ""),
    ("qsh_mao_yanbin", "qsh_gov", "新建县乐化镇团委副书记", "~2003", "~2010", "科员", "南昌高等专科学校毕业"),
    ("qsh_mao_yanbin", "qsh_gov", "新建县（现新建区）乡镇基层工作", "1996-08", "~2003", "科员", "参加工作"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period
    ("qsh_yang_yuxing", "qsh_yuan_yidan", "强关系（共事）", "区长×书记搭档约5年", "青山湖区委/区政府", "2021.04-2026.07"),
    ("qsh_gong_feixia", "qsh_yang_yuxing", "强关系（共事）", "现任班子搭档", "青山湖区委/区政府", "2026.07-至今"),
    ("qsh_gong_feixia", "qsh_yuan_yidan", "弱关系（共事）", "副书记×书记", "青山湖区委", "2025.02-2026.06"),
    ("qsh_ye_fei", "qsh_yang_yuxing", "弱关系（共事）", "宣传部长×区长", "青山湖区", "2021-2021.08"),
    ("qsh_ye_fei", "qsh_gong_feixia", "弱关系（共事）", "安义县共事", "安义县", "2021.08-2025.01"),
    ("qsh_li_songdian", "qsh_yang_yuxing", "弱关系（间接）", "前任区长", "青山湖区政府", "不同时期"),
    ("qsh_yuan_yidan", "qsh_ye_fei", "弱关系（共事）", "书记×宣传部长", "青山湖区委", "2020-2021.08"),
    ("qsh_yuan_yidan", "qsh_li_songdian", "弱关系（间接）", "安义县交集", "安义县", "~2014-2019"),
    # New: 牛浩 connections
    ("qsh_niu_hao", "qsh_yang_yuxing", "弱关系（共事）", "现任班子成员", "青山湖区委", "2023.07-至今"),
    ("qsh_niu_hao", "qsh_gong_feixia", "弱关系（共事）", "安义县共事（挂职期间）", "安义县", "2020.06-2021.08"),
    ("qsh_niu_hao", "qsh_ye_fei", "弱关系（共事）", "安义县共事", "安义县", "2020.06-2021.08"),
    # New: 彭凌迁 connections
    ("qsh_peng_lingqian", "qsh_gong_feixia", "弱关系（间接）", "纪委系统前后任（龚曾任安义县纪委书记）", "南昌市纪委系统", "不同时期"),
    # New: 毛涛 connections (from 省政协下派)
    ("qsh_mao_tao", "qsh_yang_yuxing", "弱关系（共事）", "现任班子成员", "青山湖区委", "2021.08-至今"),
    # New: 吴庆和 connections (进贤县→青山湖)
    ("qsh_wu_qinghe", "qsh_yuan_yidan", "弱关系（间接）", "袁曾在进贤任职，吴后任进贤宣传部长", "进贤县", "不同时期"),
    # New: 蔡志刚 connections (青山湖本地成长)
    ("qsh_cai_zhigang", "qsh_yuan_yidan", "弱关系（共事）", "副区长×书记", "青山湖区", "2021.10-2025.01"),
]

# ── BUILD DATABASE ──

DB_PATH = "data/database/qingshanhu_network.db"
GEXF_PATH = "data/graph/qingshanhu_network.gexf"


def create_db():
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

    # Insert persons
    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)

    # Insert organizations
    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)

    # Insert positions
    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)

    # Insert relationships
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


def generate_gexf():
    """Generate GEXF 1.3 with viz namespace using string formatting."""

    def esc(s):
        """XML-escape a string."""
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def color_for_person(post):
        """Determine (r,g,b, size) based on person's role."""
        if "区委书记" in post:
            return (255, 50, 50, 20.0)
        elif "代区长" in post or "区长" in post:
            return (50, 100, 255, 20.0)
        elif "常务副区长" in post:
            return (50, 100, 255, 16.0)
        elif "副区长" in post:
            return (50, 100, 255, 14.0)
        elif "纪委书记" in post or "监委主任" in post:
            return (255, 165, 0, 14.0)
        else:
            return (100, 100, 100, 12.0)

    def color_for_org(org_type):
        if "党委" in org_type or "纪委" in org_type:
            return (255, 200, 200, 8.0)
        elif "政府" in org_type or "政府机构" in org_type:
            return (200, 200, 255, 8.0)
        elif "开发区" in org_type:
            return (200, 255, 200, 8.0)
        elif "街道" in org_type:
            return (255, 255, 200, 8.0)
        elif "人大" in org_type:
            return (200, 255, 255, 8.0)
        elif "军队" in org_type or "公安" in org_type:
            return (200, 200, 200, 8.0)
        else:
            return (200, 200, 200, 8.0)

    lines = []

    # Header
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3"')
    lines.append('      xmlns:viz="http://gexf.net/1.3/viz"')
    lines.append('      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
    lines.append('      xsi:schemaLocation="http://gexf.net/1.3 http://gexf.net/1.3/gexf.xsd"')
    lines.append('      version="1.3">')
    lines.append('  <meta>')
    lines.append('    <creator>China-Gov-Network Investigation</creator>')
    lines.append('    <description>南昌市青山湖区领导班子工作关系网络 — 2026年7月</description>')
    lines.append('    <date>2026-07-14</date>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="type" title="Node Type" type="string"/>')
    lines.append('      <attribute id="role" title="Role" type="string"/>')
    lines.append('      <attribute id="org_type" title="Org Type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="type" title="Edge Type" type="string"/>')
    lines.append('      <attribute id="start" title="Start Date" type="string"/>')
    lines.append('      <attribute id="end" title="End Date" type="string"/>')
    lines.append('      <attribute id="rank" title="Rank" type="string"/>')
    lines.append('      <attribute id="strength" title="Strength" type="string"/>')
    lines.append('      <attribute id="context" title="Context" type="string"/>')
    lines.append('      <attribute id="overlap_org" title="Overlap Org" type="string"/>')
    lines.append('      <attribute id="overlap_period" title="Overlap Period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        label = esc(p[1])
        post = p[9] or ""
        r, g, b, sz = color_for_person(post)
        title_info = f"{esc(p[1])}\\n{esc(post)}\\n{esc(p[3])}·{esc(p[4] if p[4] else '未知')}\\n籍贯: {esc(p[5] if p[5] else '未知')}"
        lines.append(f'      <node id="{pid}" label="{label}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="person"/>')
        lines.append(f'          <attvalue for="role" value="{esc(post)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:position x="0" y="0" z="0"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        label = esc(o[1])
        tp = o[2]
        r, g, b, sz = color_for_org(tp)
        lines.append(f'      <node id="{oid}" label="{label}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="org"/>')
        lines.append(f'          <attvalue for="org_type" value="{esc(tp)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="square"/>')
        lines.append(f'        <viz:position x="0" y="0" z="0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    # work_at edges (person -> org)
    edge_id = 0
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        edge_id += 1
        lines.append(f'      <edge id="e{edge_id}" source="{pid}" target="{oid}" type="directed" label="{esc(title)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="start" value="{esc(start or "")}"/>')
        lines.append(f'          <attvalue for="end" value="{esc(end or "")}"/>')
        lines.append(f'          <attvalue for="rank" value="{esc(rank or "")}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="80" g="80" b="80" a="0.5"/>')
        lines.append('        <viz:thickness value="1.0"/>')
        lines.append('      </edge>')

    # relationship edges (person <-> person)
    for r in RELATIONSHIPS:
        a, b, typ, context, overlap_org, overlap_period = r
        edge_id += 1
        is_strong = "强关系" in typ
        cr, cg, cb = (184, 149, 62) if is_strong else (91, 139, 192)
        thickness = 2.5 if is_strong else 1.5
        lines.append(f'      <edge id="e{edge_id}" source="{a}" target="{b}" type="undirected" label="{esc(context)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="relationship"/>')
        lines.append(f'          <attvalue for="strength" value="{esc(typ)}"/>')
        lines.append(f'          <attvalue for="context" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="overlap_org" value="{esc(overlap_org)}"/>')
        lines.append(f'          <attvalue for="overlap_period" value="{esc(overlap_period)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>')
        lines.append(f'        <viz:thickness value="{thickness}"/>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
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
    print("Building 南昌市青山湖区 network data...")
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()
    print("Done.")
