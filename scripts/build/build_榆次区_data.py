#!/usr/bin/env python3
"""Build 榆次区 (Yuci District) personnel network database + GEXF graph."""

import sqlite3
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))

DB_PATH = os.path.join(PROJECT_ROOT, "data/database/榆次区_network.db")
GEXF_PATH = os.path.join(PROJECT_ROOT, "data/graph/榆次区_network.gexf")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

# ========== DATA ==========

persons = [
    # === Core Leaders ===
    {"id": "yuci_zhang_yingjie", "name": "张英杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1970年3月", "birthplace": "山西省平遥县",
     "education": "中央党校研究生学历",
     "party_join": "1991年9月", "work_start": "1990年7月",
     "current_post": "晋中市人大常委会副主任、区委书记", "current_org": "中共榆次区委员会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/qwld/content_12940"},
    {"id": "yuci_du_jianzhong", "name": "杜建中", "gender": "男", "ethnicity": "汉族",
     "birth": "1973年10月", "birthplace": "",
     "education": "工商管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、区长", "current_org": "榆次区人民政府",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/qwld/content_42112"},
    # === Key Deputies ===
    {"id": "yuci_li_tao", "name": "李涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年9月", "birthplace": "",
     "education": "中央党校大学学历，农业推广硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、政法委书记", "current_org": "中共榆次区委员会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/qwld/content_45726"},
    {"id": "yuci_wang_yanlong", "name": "王艳龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年1月", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区委办主任", "current_org": "中共榆次区委员会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/qwld/content_35150"},
    {"id": "yuci_zhang_xiaoguang", "name": "张晓光", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年9月", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区政府副区长", "current_org": "榆次区人民政府",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/qwld/content_35144"},
    {"id": "yuci_cui_yanjie", "name": "崔宴杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年1月", "birthplace": "",
     "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、宣传部部长", "current_org": "中共榆次区委宣传部",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/qwld/content_12469"},
    {"id": "yuci_tian_weijie", "name": "田伟杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1981年2月", "birthplace": "",
     "education": "大学本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、组织部部长、区委党校校长", "current_org": "中共榆次区委组织部",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/qwld/content_45727"},
    {"id": "yuci_li_mingdao", "name": "李明道", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年4月", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、纪委书记、提名监委主任", "current_org": "榆次区纪律检查委员会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/qwld/content_45728"},
    {"id": "yuci_chen_ming", "name": "陈明", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年6月", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区人武部政委", "current_org": "榆次区人民武装部",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/qwld/content_8768"},
    # === Government Deputy Mayors ===
    {"id": "yuci_zhang_zhonglin", "name": "张中林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政府副区长、区公安分局局长", "current_org": "榆次区公安分局",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/zfld/content_39518"},
    {"id": "yuci_du_xiaoyu", "name": "杜晓宇", "gender": "女", "ethnicity": "汉族",
     "birth": "1983年12月", "birthplace": "山西省和顺县",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "区政府副区长", "current_org": "榆次区人民政府",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/zfld/content_35143"},
    {"id": "yuci_ma_hong", "name": "马宏", "gender": "男", "ethnicity": "汉族",
     "birth": "1974年5月", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政府副区长", "current_org": "榆次区人民政府",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/zfld/content_13540"},
    {"id": "yuci_sun_wentao", "name": "孙文韬", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年3月", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政府副区长", "current_org": "榆次区人民政府",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/zfld/content_35140"},
    {"id": "yuci_yang_linjie", "name": "杨林杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年5月", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政府副区长", "current_org": "榆次区人民政府",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/zfld/content_35142"},
    {"id": "yuci_qi_tao", "name": "齐涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政府办公室主任", "current_org": "榆次区人民政府",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/zfld/content_13793"},
    # === People's Congress ===
    {"id": "yuci_li_pengfei", "name": "李鹏飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会党组书记、主任", "current_org": "榆次区人大常委会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/rdld/content_10407"},
    {"id": "yuci_fan_yaoming", "name": "范耀明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会党组副书记、副主任", "current_org": "榆次区人大常委会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/rdld/content_13536"},
    {"id": "yuci_zhang_qun", "name": "张群", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会副主任", "current_org": "榆次区人大常委会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/rdld/content_13537"},
    {"id": "yuci_guo_qiang", "name": "郭强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会党组成员、副主任", "current_org": "榆次区人大常委会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/rdld/content_13542"},
    {"id": "yuci_fu_haihui", "name": "付海挥", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会党组成员、副主任", "current_org": "榆次区人大常委会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/rdld/content_37844"},
    {"id": "yuci_zhang_yonggang", "name": "张永刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大办公室主任", "current_org": "榆次区人大常委会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/rdld/content_13846"},
    # === CPPCC ===
    {"id": "yuci_xing_rubiao", "name": "邢如彪", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政协主席", "current_org": "政协榆次区委员会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/zxld/content_8764"},
    {"id": "yuci_zhang_pingping", "name": "张平平", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "区政协副主席", "current_org": "政协榆次区委员会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/zxld/content_13545"},
    {"id": "yuci_liu_jiangang", "name": "刘建刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "区政协副主席、市政协常委、民建市委副主委", "current_org": "政协榆次区委员会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/zxld/content_13543"},
    {"id": "yuci_cui_haibin", "name": "崔海宾", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政协副主席", "current_org": "政协榆次区委员会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/zxld/content_36558"},
    {"id": "yuci_kang_xiaoyuan", "name": "康晓渊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政协副主席", "current_org": "政协榆次区委员会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/zxld/content_42434"},
    {"id": "yuci_li_yuan", "name": "李源", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政协秘书长、办公室主任", "current_org": "政协榆次区委员会",
     "source": "https://www.yuci.gov.cn/zwgk/fdzdgknr/ldzc/zxld/content_36559"},
]

organizations = [
    {"id": "yuci_party_committee", "name": "中共榆次区委员会", "type": "party", "level": "county", "parent": "晋中市委", "location": "山西省晋中市榆次区"},
    {"id": "yuci_gov", "name": "榆次区人民政府", "type": "government", "level": "county", "parent": "晋中市政府", "location": "山西省晋中市榆次区"},
    {"id": "yuci_discipline", "name": "榆次区纪律检查委员会", "type": "discipline", "level": "county", "parent": "晋中市纪委监委", "location": "山西省晋中市榆次区"},
    {"id": "yuci_org_dept", "name": "中共榆次区委组织部", "type": "party_dept", "level": "county", "parent": "榆次区委", "location": "山西省晋中市榆次区"},
    {"id": "yuci_propaganda_dept", "name": "中共榆次区委宣传部", "type": "party_dept", "level": "county", "parent": "榆次区委", "location": "山西省晋中市榆次区"},
    {"id": "yuci_office", "name": "中共榆次区委办公室", "type": "party_dept", "level": "county", "parent": "榆次区委", "location": "山西省晋中市榆次区"},
    {"id": "yuci_political_legal", "name": "中共榆次区委政法委员会", "type": "party_dept", "level": "county", "parent": "榆次区委", "location": "山西省晋中市榆次区"},
    {"id": "yuci_military_dept", "name": "榆次区人民武装部", "type": "government", "level": "county", "parent": "榆次区委", "location": "山西省晋中市榆次区"},
    {"id": "yuci_public_security", "name": "榆次区公安分局", "type": "government", "level": "county", "parent": "榆次区政府", "location": "山西省晋中市榆次区"},
    {"id": "yuci_congress", "name": "榆次区人大常委会", "type": "congress", "level": "county", "parent": "榆次区", "location": "山西省晋中市榆次区"},
    {"id": "yuci_cppcc", "name": "政协榆次区委员会", "type": "cppcc", "level": "county", "parent": "榆次区", "location": "山西省晋中市榆次区"},
    {"id": "jinzhong_congress", "name": "晋中市人大常委会", "type": "congress", "level": "prefecture", "parent": "晋中市", "location": "山西省晋中市"},
    {"id": "jinzhong_party_committee", "name": "中共晋中市委员会", "type": "party", "level": "prefecture", "parent": "山西省委", "location": "山西省晋中市"},
    {"id": "jinzhong_gov", "name": "晋中市人民政府", "type": "government", "level": "prefecture", "parent": "山西省政府", "location": "山西省晋中市"},
    {"id": "xixian_party_committee", "name": "中共昔阳县委员会", "type": "party", "level": "county", "parent": "晋中市委", "location": "山西省晋中市昔阳县"},
]

positions = [
    # 张英杰
    {"person_id": "yuci_zhang_yingjie", "org_id": "yuci_party_committee", "title": "区委书记", "start": "2021", "end": "", "rank": "副厅级", "note": "现任，兼晋中市人大常委会副主任"},
    {"person_id": "yuci_zhang_yingjie", "org_id": "jinzhong_congress", "title": "晋中市人大常委会副主任", "start": "2022", "end": "", "rank": "副厅级", "note": "现任"},
    {"person_id": "yuci_zhang_yingjie", "org_id": "xixian_party_committee", "title": "昔阳县委书记", "start": "2016", "end": "2021", "rank": "正处级", "note": ""},
    # 杜建中
    {"person_id": "yuci_du_jianzhong", "org_id": "yuci_party_committee", "title": "区委副书记", "start": "2026-01", "end": "", "rank": "正处级", "note": "现任"},
    {"person_id": "yuci_du_jianzhong", "org_id": "yuci_gov", "title": "区长", "start": "2026-01", "end": "", "rank": "正处级", "note": "现任"},
    # 李涛
    {"person_id": "yuci_li_tao", "org_id": "yuci_party_committee", "title": "区委副书记、政法委书记", "start": "2026-07", "end": "", "rank": "副处级", "note": "现任"},
    {"person_id": "yuci_li_tao", "org_id": "yuci_political_legal", "title": "政法委书记", "start": "2026-07", "end": "", "rank": "副处级", "note": "现任"},
    # 王艳龙
    {"person_id": "yuci_wang_yanlong", "org_id": "yuci_party_committee", "title": "区委常委、区委办主任", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    {"person_id": "yuci_wang_yanlong", "org_id": "yuci_office", "title": "区委办公室主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 张晓光
    {"person_id": "yuci_zhang_xiaoguang", "org_id": "yuci_party_committee", "title": "区委常委", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    {"person_id": "yuci_zhang_xiaoguang", "org_id": "yuci_gov", "title": "区政府副区长（常务）", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 崔宴杰
    {"person_id": "yuci_cui_yanjie", "org_id": "yuci_party_committee", "title": "区委常委、宣传部部长", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    {"person_id": "yuci_cui_yanjie", "org_id": "yuci_propaganda_dept", "title": "宣传部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 田伟杰
    {"person_id": "yuci_tian_weijie", "org_id": "yuci_party_committee", "title": "区委常委、组织部部长", "start": "2026-07", "end": "", "rank": "副处级", "note": "现任"},
    {"person_id": "yuci_tian_weijie", "org_id": "yuci_org_dept", "title": "组织部部长、区委党校校长", "start": "2026-07", "end": "", "rank": "副处级", "note": ""},
    # 李明道
    {"person_id": "yuci_li_mingdao", "org_id": "yuci_party_committee", "title": "区委常委、纪委书记", "start": "2026-07", "end": "", "rank": "副处级", "note": "现任，提名监委主任"},
    {"person_id": "yuci_li_mingdao", "org_id": "yuci_discipline", "title": "纪委书记、提名监委主任", "start": "2026-07", "end": "", "rank": "副处级", "note": ""},
    # 陈明
    {"person_id": "yuci_chen_ming", "org_id": "yuci_party_committee", "title": "区委常委", "start": "", "end": "", "rank": "副处级", "note": "现任"},
    {"person_id": "yuci_chen_ming", "org_id": "yuci_military_dept", "title": "区人武部政委", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 张中林
    {"person_id": "yuci_zhang_zhonglin", "org_id": "yuci_gov", "title": "区政府副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "yuci_zhang_zhonglin", "org_id": "yuci_public_security", "title": "区公安分局局长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 杜晓宇
    {"person_id": "yuci_du_xiaoyu", "org_id": "yuci_gov", "title": "区政府副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 马宏
    {"person_id": "yuci_ma_hong", "org_id": "yuci_gov", "title": "区政府副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 孙文韬
    {"person_id": "yuci_sun_wentao", "org_id": "yuci_gov", "title": "区政府副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 杨林杰
    {"person_id": "yuci_yang_linjie", "org_id": "yuci_gov", "title": "区政府副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 齐涛
    {"person_id": "yuci_qi_tao", "org_id": "yuci_gov", "title": "区政府办公室主任", "start": "", "end": "", "rank": "正科级", "note": ""},
    # 李鹏飞
    {"person_id": "yuci_li_pengfei", "org_id": "yuci_congress", "title": "区人大常委会主任", "start": "", "end": "", "rank": "正处级", "note": ""},
    # 范耀明
    {"person_id": "yuci_fan_yaoming", "org_id": "yuci_congress", "title": "区人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 张群
    {"person_id": "yuci_zhang_qun", "org_id": "yuci_congress", "title": "区人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 郭强
    {"person_id": "yuci_guo_qiang", "org_id": "yuci_congress", "title": "区人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 付海挥
    {"person_id": "yuci_fu_haihui", "org_id": "yuci_congress", "title": "区人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 邢如彪
    {"person_id": "yuci_xing_rubiao", "org_id": "yuci_cppcc", "title": "区政协主席", "start": "", "end": "", "rank": "正处级", "note": ""},
    # 张平平
    {"person_id": "yuci_zhang_pingping", "org_id": "yuci_cppcc", "title": "区政协副主席", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 刘建刚
    {"person_id": "yuci_liu_jiangang", "org_id": "yuci_cppcc", "title": "区政协副主席", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 崔海宾
    {"person_id": "yuci_cui_haibin", "org_id": "yuci_cppcc", "title": "区政协副主席", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 康晓渊
    {"person_id": "yuci_kang_xiaoyuan", "org_id": "yuci_cppcc", "title": "区政协副主席", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 李源
    {"person_id": "yuci_li_yuan", "org_id": "yuci_cppcc", "title": "区政协秘书长、办公室主任", "start": "", "end": "", "rank": "正科级", "note": ""},
]

relationships = [
    # 张英杰 ↔ 杜建中 (党政搭档)
    {"person_a": "yuci_zhang_yingjie", "person_b": "yuci_du_jianzhong", "type": "superior_subordinate",
     "context": "区委书记与区长党政搭档", "overlap_org": "中共榆次区委员会/榆次区人民政府",
     "overlap_period": "2026-01至今", "strength": "strong", "confidence": "confirmed"},
    # 张英杰 ↔ 李涛 (top leader + deputy secretary)
    {"person_a": "yuci_zhang_yingjie", "person_b": "yuci_li_tao", "type": "superior_subordinate",
     "context": "区委书记与副书记/政法委书记", "overlap_org": "中共榆次区委员会",
     "overlap_period": "2026-07至今", "strength": "strong", "confidence": "confirmed"},
    # 张英杰 ↔ 张晓光 (区委书记 + standing committee member / deputy mayor)
    {"person_a": "yuci_zhang_yingjie", "person_b": "yuci_zhang_xiaoguang", "type": "superior_subordinate",
     "context": "区委书记与区委常委、常务副区长", "overlap_org": "中共榆次区委员会/榆次区人民政府",
     "overlap_period": "2025-02至今", "strength": "strong", "confidence": "confirmed"},
    # 杜建中 ↔ 张晓光 (mayor + deputy mayor)
    {"person_a": "yuci_du_jianzhong", "person_b": "yuci_zhang_xiaoguang", "type": "superior_subordinate",
     "context": "区长与常务副区长", "overlap_org": "榆次区人民政府",
     "overlap_period": "2026-01至今", "strength": "strong", "confidence": "confirmed"},
    # 张英杰 ↔ 李明道 (区委书记 + 纪委书记)
    {"person_a": "yuci_zhang_yingjie", "person_b": "yuci_li_mingdao", "type": "superior_subordinate",
     "context": "区委书记与纪委书记", "overlap_org": "中共榆次区委员会",
     "overlap_period": "2026-07至今", "strength": "strong", "confidence": "confirmed"},
    # 张英杰 ↔ 田伟杰 (区委书记 + 组织部长)
    {"person_a": "yuci_zhang_yingjie", "person_b": "yuci_tian_weijie", "type": "superior_subordinate",
     "context": "区委书记与组织部部长", "overlap_org": "中共榆次区委员会",
     "overlap_period": "2026-07至今", "strength": "strong", "confidence": "confirmed"},
    # 张英杰 ↔ 王艳龙 (区委书记 + 区委办主任)
    {"person_a": "yuci_zhang_yingjie", "person_b": "yuci_wang_yanlong", "type": "superior_subordinate",
     "context": "区委书记与区委办主任", "overlap_org": "中共榆次区委员会",
     "overlap_period": "2025-02至今", "strength": "strong", "confidence": "confirmed"},
    # 杜建中 ↔ 副区长们 (区长 + 各位副区长)
    {"person_a": "yuci_du_jianzhong", "person_b": "yuci_zhang_zhonglin", "type": "superior_subordinate",
     "context": "区长与副区长/公安分局局长", "overlap_org": "榆次区人民政府",
     "overlap_period": "2026-01至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "yuci_du_jianzhong", "person_b": "yuci_du_xiaoyu", "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "榆次区人民政府",
     "overlap_period": "2026-01至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "yuci_du_jianzhong", "person_b": "yuci_ma_hong", "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "榆次区人民政府",
     "overlap_period": "2026-01至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "yuci_du_jianzhong", "person_b": "yuci_sun_wentao", "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "榆次区人民政府",
     "overlap_period": "2026-01至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "yuci_du_jianzhong", "person_b": "yuci_yang_linjie", "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "榆次区人民政府",
     "overlap_period": "2026-01至今", "strength": "medium", "confidence": "confirmed"},
    # 杜建中 ↔ 李涛 (区长 + 区委副书记/政法委书记)
    {"person_a": "yuci_du_jianzhong", "person_b": "yuci_li_tao", "type": "overlap",
     "context": "区长与区委副书记共事", "overlap_org": "中共榆次区委员会",
     "overlap_period": "2026-07至今", "strength": "strong", "confidence": "confirmed"},
]


# ========== BUILD SQLite ==========
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript('''
    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    );
    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    );
    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
''')

# Insert persons
person_id_map = {}
for i, p in enumerate(persons, 1):
    cur.execute('''INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (i, p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
                 p["education"], p["party_join"], p["work_start"], p["current_post"],
                 p["current_org"], p["source"]))
    person_id_map[p["id"]] = i

org_id_map = {}
for i, o in enumerate(organizations, 1):
    cur.execute('''INSERT INTO organizations (id, name, type, level, parent, location)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (i, o["name"], o["type"], o["level"], o["parent"], o["location"]))
    org_id_map[o["id"]] = i

for pos in positions:
    pid = person_id_map.get(pos["person_id"])
    oid = org_id_map.get(pos["org_id"])
    if pid and oid:
        cur.execute('''INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (pid, oid, pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    pa = person_id_map.get(r["person_a"])
    pb = person_id_map.get(r["person_b"])
    if pa and pb:
        cur.execute('''INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                       VALUES (?, ?, ?, ?, ?, ?)''',
                    (pa, pb, r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()

print(f"  榆次区 DB: {DB_PATH}")
print(f"     Persons: {len(persons)}")
print(f"     Organizations: {len(organizations)}")
print(f"     Positions: {len(positions)}")
print(f"     Relationships: {len(relationships)}")

# ========== BUILD GEXF ==========
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if "书记" in role and "区委书记" in role or "区委书记" in role:
        return "255,50,50"
    if "区长" in role or "县长" in role:
        return "50,100,255"
    if "纪委书记" in role or "监委" in role:
        return "255,165,0"
    if "副书记" in role:
        return "200,50,50"
    return "100,100,100"

def is_top_leader(p):
    return p["id"] in ("yuci_zhang_yingjie", "yuci_du_jianzhong")

def org_color(org):
    t = org["type"]
    if t == "party" or t == "party_dept":
        return "255,200,200"
    if t == "government":
        return "200,200,255"
    if t == "discipline":
        return "255,220,200"
    if t == "congress":
        return "200,255,255"
    if t == "cppcc":
        return "255,240,200"
    return "200,200,200"

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>榆次区领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="start" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Organization nodes
for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="org"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges — person ↔ organization (worked_at)
lines.append('    <edges>')
edge_id = 0
for pos in positions:
    pid = person_id_map.get(pos["person_id"])
    oid = org_id_map.get(pos["org_id"])
    if pid and oid:
        lines.append(f'      <edge id="e{edge_id}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        edge_id += 1

# Edges — person ↔ person (relationship)
for r in relationships:
    pa = person_id_map.get(r["person_a"])
    pb = person_id_map.get(r["person_b"])
    if pa and pb:
        w = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="e{edge_id}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue type="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"   GEXF: {GEXF_PATH}")
print(f"   Edges: {edge_id}")
print("Done.")