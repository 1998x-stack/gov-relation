#!/usr/bin/env python3
"""漳县 (定西市, 甘肃省) 领导班子工作关系网络数据构建脚本

数据来源: 漳县人民政府官方网站 http://www.zhangxian.gov.cn
页面: 县委领导(col/col719), 县政府领导(col/col721), 县人大领导(col/col720), 县政协领导(col/col722)
      任前公示(art/718)等, 访问日期: 2026-07-22
"""

import os
import sqlite3
from datetime import datetime

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "漳县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "漳县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据 (来源: zhangxian.gov.cn 领导之窗, 2026-07-22)
# ═══════════════════════════════════════════════

persons = [
    # === 县委领导 (col/col719) ===
    {
        "id": "zhangxian_wang_yawei",
        "name": "王亚伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-12",
        "birthplace": "",
        "native_place": "",
        "education": "中央党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "漳县县委书记",
        "current_org": "中共漳县委员会",
        "source": "http://www.zhangxian.gov.cn/col/col9670/index.html",
    },
    {
        "id": "zhangxian_li_qingpeng",
        "name": "李青鹏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974-05",
        "birthplace": "",
        "native_place": "",
        "education": "中央党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "漳县县委副书记、县长",
        "current_org": "中共漳县委员会/漳县人民政府",
        "source": "http://www.zhangxian.gov.cn/col/col9671/index.html; http://www.zhangxian.gov.cn/col/col9688/index.html",
    },
    {
        "id": "zhangxian_wang_xiaojun",
        "name": "王小军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-12",
        "birthplace": "",
        "native_place": "",
        "education": "本科",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共漳县纪律检查委员会/漳县监察委员会",
        "source": "http://www.zhangxian.gov.cn/col/col9674/index.html",
    },
    {
        "id": "zhangxian_zhang_jiang",
        "name": "张江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共漳县委员会组织部",
        "source": "http://www.zhangxian.gov.cn/col/col9679/index.html",
    },
    {
        "id": "zhangxian_wang_jianfu",
        "name": "王建府",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-11",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共漳县委员会政法委员会",
        "source": "http://www.zhangxian.gov.cn/col/col15500/index.html",
    },
    {
        "id": "zhangxian_zhang_kuan",
        "name": "张宽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县人武部部长",
        "current_org": "漳县人民武装部",
        "source": "http://www.zhangxian.gov.cn/col/col9675/index.html",
    },
    {
        "id": "zhangxian_xu_yagang",
        "name": "徐亚纲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府副县长（挂职）",
        "current_org": "漳县人民政府",
        "source": "http://www.zhangxian.gov.cn/col/col12067/index.html",
    },
    {
        "id": "zhangxian_yang_hui",
        "name": "杨慧",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府副县长（挂职）",
        "current_org": "漳县人民政府",
        "source": "http://www.zhangxian.gov.cn/col/col19802/index.html",
    },
    {
        "id": "zhangxian_li_ying",
        "name": "李颖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共漳县委员会宣传部",
        "source": "http://www.zhangxian.gov.cn/col/col15501/index.html",
    },
    {
        "id": "zhangxian_xie_jiangchao",
        "name": "解江超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府副县长候选人（挂职）",
        "current_org": "漳县人民政府",
        "source": "http://www.zhangxian.gov.cn/col/col15343/index.html",
    },
    {
        "id": "zhangxian_li_zhengwen",
        "name": "李正文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-04",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共漳县委员会统战部",
        "source": "http://www.zhangxian.gov.cn/col/col9676/index.html",
    },
    {
        "id": "zhangxian_zhu_jichang",
        "name": "朱继昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-04",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府副县长",
        "current_org": "漳县人民政府",
        "source": "http://www.zhangxian.gov.cn/col/col9672/index.html",
    },
    # === 县政府副县长 (col/col721) 非县委常委 ===
    {
        "id": "zhangxian_guo_yuanhong",
        "name": "郭元红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府副县长",
        "current_org": "漳县人民政府",
        "source": "http://www.zhangxian.gov.cn/col/col15518/index.html",
    },
    {
        "id": "zhangxian_wei_junmin",
        "name": "魏军民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府副县长",
        "current_org": "漳县人民政府",
        "source": "http://www.zhangxian.gov.cn/col/col15508/index.html",
    },
    {
        "id": "zhangxian_xu_bin",
        "name": "徐斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "漳县人民政府",
        "source": "http://www.zhangxian.gov.cn/col/col19244/index.html",
    },
    {
        "id": "zhangxian_zhang_pengfei",
        "name": "张鹏飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-04",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长、县公安局局长",
        "current_org": "漳县人民政府/漳县公安局",
        "source": "http://www.zhangxian.gov.cn/col/col15520/index.html",
    },
    {
        "id": "zhangxian_gou_ruibin",
        "name": "苟睿斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-01",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "漳县人民政府",
        "source": "http://www.zhangxian.gov.cn/col/col20440/index.html",
    },
    {
        "id": "zhangxian_zhang_jianxin",
        "name": "张建新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-10",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "漳县人民政府",
        "source": "http://www.zhangxian.gov.cn/col/col12004/index.html",
    },
    # === 县人大领导 (col/col720) ===
    {
        "id": "zhangxian_pei_kongrong",
        "name": "裴孔荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-04",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "漳县人民代表大会常务委员会",
        "source": "http://www.zhangxian.gov.cn/col/col9683/index.html",
    },
    {
        "id": "zhangxian_zhang_xiaojun",
        "name": "张小军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "漳县人民代表大会常务委员会",
        "source": "http://www.zhangxian.gov.cn/col/col15982/index.html",
    },
    {
        "id": "zhangxian_wang_xiaofang",
        "name": "王小芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "漳县人民代表大会常务委员会",
        "source": "http://www.zhangxian.gov.cn/col/col12283/index.html",
    },
    {
        "id": "zhangxian_jiang_jinxi",
        "name": "蒋金喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "漳县人民代表大会常务委员会",
        "source": "http://www.zhangxian.gov.cn/col/col9687/index.html",
    },
    {
        "id": "zhangxian_zhao_yongjun",
        "name": "赵永军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "漳县人民代表大会常务委员会",
        "source": "http://www.zhangxian.gov.cn/col/col9685/index.html",
    },
    # === 县政协领导 (col/col722) ===
    {
        "id": "zhangxian_liu_zhilan",
        "name": "刘芝兰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971-07",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协漳县委员会",
        "source": "http://www.zhangxian.gov.cn/col/col9696/index.html",
    },
    {
        "id": "zhangxian_luo_hongming",
        "name": "骆宏明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协漳县委员会",
        "source": "http://www.zhangxian.gov.cn/col/col9698/index.html",
    },
    {
        "id": "zhangxian_xu_ming",
        "name": "徐明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协漳县委员会",
        "source": "http://www.zhangxian.gov.cn/col/col19806/index.html",
    },
    {
        "id": "zhangxian_zhao_xiaozhuo",
        "name": "赵小卓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协漳县委员会",
        "source": "http://www.zhangxian.gov.cn/col/col12284/index.html",
    },
    {
        "id": "zhangxian_tian_ainong",
        "name": "田爱农",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协漳县委员会",
        "source": "http://www.zhangxian.gov.cn/col/col9697/index.html",
    },
]

# ═══════════════════════════════════════════════
# 组织机构数据
# ═══════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共漳县委员会", "type": "党委", "level": "县处级", "parent": "中共定西市委员会", "location": "甘肃省定西市漳县"},
    {"id": 2, "name": "漳县人民政府", "type": "政府", "level": "县处级", "parent": "定西市人民政府", "location": "甘肃省定西市漳县"},
    {"id": 3, "name": "中共漳县纪律检查委员会/漳县监察委员会", "type": "党委", "level": "县处级", "parent": "中共定西市纪律检查委员会", "location": "甘肃省定西市漳县"},
    {"id": 4, "name": "中共漳县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共漳县委员会", "location": "甘肃省定西市漳县"},
    {"id": 5, "name": "中共漳县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共漳县委员会", "location": "甘肃省定西市漳县"},
    {"id": 6, "name": "漳县人民武装部", "type": "政府", "level": "县处级", "parent": "定西军分区", "location": "甘肃省定西市漳县"},
    {"id": 7, "name": "中共漳县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共漳县委员会", "location": "甘肃省定西市漳县"},
    {"id": 8, "name": "中共漳县委员会统战部", "type": "党委", "level": "县处级", "parent": "中共漳县委员会", "location": "甘肃省定西市漳县"},
    {"id": 9, "name": "漳县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "定西市人民代表大会常务委员会", "location": "甘肃省定西市漳县"},
    {"id": 10, "name": "政协漳县委员会", "type": "政协", "level": "县处级", "parent": "政协定西市委员会", "location": "甘肃省定西市漳县"},
    {"id": 11, "name": "漳县公安局", "type": "政府", "level": "县处级", "parent": "漳县人民政府/定西市公安局", "location": "甘肃省定西市漳县"},
    {"id": 12, "name": "定西市商务局", "type": "政府", "level": "地厅级", "parent": "定西市人民政府", "location": "甘肃省定西市"},
    {"id": 13, "name": "中共定西市委员会", "type": "党委", "level": "地厅级", "parent": "中共甘肃省委员会", "location": "甘肃省定西市"},
    {"id": 14, "name": "定西市人民政府", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府", "location": "甘肃省定西市"},
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # === 王亚伟 — 县委书记 ===
    {"person_id": "zhangxian_wang_yawei", "org_id": 1, "title": "漳县县委书记", "start": "2024", "end": "present", "rank": "正处级", "note": "1974年生, 中央党校大学学历"},
    # === 李青鹏 — 县长 ===
    {"person_id": "zhangxian_li_qingpeng", "org_id": 1, "title": "漳县县委副书记", "start": "2024-12", "end": "present", "rank": "正处级", "note": "2024年11月任前公示, 拟提名为县长候选人"},
    {"person_id": "zhangxian_li_qingpeng", "org_id": 2, "title": "漳县县长", "start": "2024-12", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "zhangxian_li_qingpeng", "org_id": 12, "title": "定西市商务局党组书记、局长", "start": "", "end": "2024-11", "rank": "正处级", "note": "任前公示显示此前职务"},
    # === 王小军 — 纪委书记 ===
    {"person_id": "zhangxian_wang_xiaojun", "org_id": 3, "title": "县委常委、县纪委书记、县监委主任", "start": "", "end": "present", "rank": "副处级", "note": "1981年生, 四级高级监察官"},
    # === 张江 — 组织部长 ===
    {"person_id": "zhangxian_zhang_jiang", "org_id": 4, "title": "县委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # === 王建府 — 政法委书记 ===
    {"person_id": "zhangxian_wang_jianfu", "org_id": 5, "title": "县委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": "1979年生, 在职大学学历"},
    # === 张宽 — 人武部长 ===
    {"person_id": "zhangxian_zhang_kuan", "org_id": 6, "title": "县委常委、县人武部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # === 徐亚纲 — 挂职副县长 ===
    {"person_id": "zhangxian_xu_yagang", "org_id": 2, "title": "县委常委、县政府副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "挂职"},
    # === 杨慧 — 挂职副县长 ===
    {"person_id": "zhangxian_yang_hui", "org_id": 2, "title": "县委常委、县政府副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "挂职"},
    # === 李颖 — 宣传部长 ===
    {"person_id": "zhangxian_li_ying", "org_id": 7, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": "1983年生"},
    # === 解江超 — 挂职副县长候选人 ===
    {"person_id": "zhangxian_xie_jiangchao", "org_id": 2, "title": "县委常委、县政府副县长候选人（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "挂职"},
    # === 李正文 — 统战部长 ===
    {"person_id": "zhangxian_li_zhengwen", "org_id": 8, "title": "县委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": "1979年生"},
    # === 朱继昌 — 副县长 ===
    {"person_id": "zhangxian_zhu_jichang", "org_id": 2, "title": "县委常委、县政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "1978年生"},
    # === 郭元红 — 副县长 ===
    {"person_id": "zhangxian_guo_yuanhong", "org_id": 2, "title": "县委常委、县政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # === 魏军民 — 副县长 ===
    {"person_id": "zhangxian_wei_junmin", "org_id": 2, "title": "县委常委、县政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # === 徐斌 — 副县长 ===
    {"person_id": "zhangxian_xu_bin", "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # === 张鹏飞 — 副县长/公安局长 ===
    {"person_id": "zhangxian_zhang_pengfei", "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "1977年生, 兼任县公安局局长"},
    {"person_id": "zhangxian_zhang_pengfei", "org_id": 11, "title": "县公安局党委书记、局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # === 苟睿斌 — 副县长 ===
    {"person_id": "zhangxian_gou_ruibin", "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "1984年生"},
    # === 张建新 — 副县长 ===
    {"person_id": "zhangxian_zhang_jianxin", "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "1985年生"},
    # === 人大 ===
    {"person_id": "zhangxian_pei_kongrong", "org_id": 9, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "1972年生"},
    {"person_id": "zhangxian_zhang_xiaojun", "org_id": 9, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "zhangxian_wang_xiaofang", "org_id": 9, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "zhangxian_jiang_jinxi", "org_id": 9, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "zhangxian_zhao_yongjun", "org_id": 9, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # === 政协 ===
    {"person_id": "zhangxian_liu_zhilan", "org_id": 10, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": "1971年生"},
    {"person_id": "zhangxian_luo_hongming", "org_id": 10, "title": "县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "zhangxian_xu_ming", "org_id": 10, "title": "县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "zhangxian_zhao_xiaozhuo", "org_id": 10, "title": "县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "zhangxian_tian_ainong", "org_id": 10, "title": "县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════

relationships = [
    # 王亚伟 - 李青鹏: 书记-县长搭班
    {"person_a": "zhangxian_wang_yawei", "person_b": "zhangxian_li_qingpeng",
     "type": "superior_subordinate", "context": "县委书记-县长搭班工作关系",
     "overlap_org": "中共漳县委员会/漳县人民政府", "overlap_period": "2024-2026", "confidence": "confirmed"},
    # 王亚伟 - 王小军: 书记-纪委书记
    {"person_a": "zhangxian_wang_yawei", "person_b": "zhangxian_wang_xiaojun",
     "type": "superior_subordinate", "context": "县委书记-纪委书记监督与被监督关系",
     "overlap_org": "中共漳县委员会", "overlap_period": "", "confidence": "confirmed"},
    # 王亚伟 - 张江: 书记-组织部长
    {"person_a": "zhangxian_wang_yawei", "person_b": "zhangxian_zhang_jiang",
     "type": "superior_subordinate", "context": "县委书记-组织部长干部选拔任用关系",
     "overlap_org": "中共漳县委员会", "overlap_period": "", "confidence": "confirmed"},
    # 王亚伟 - 李颖: 书记-宣传部长
    {"person_a": "zhangxian_wang_yawei", "person_b": "zhangxian_li_ying",
     "type": "superior_subordinate", "context": "县委书记-宣传部长意识形态工作关系",
     "overlap_org": "中共漳县委员会", "overlap_period": "", "confidence": "confirmed"},
    # 王亚伟 - 王建府: 书记-政法委书记
    {"person_a": "zhangxian_wang_yawei", "person_b": "zhangxian_wang_jianfu",
     "type": "superior_subordinate", "context": "县委书记-政法委书记政法工作关系",
     "overlap_org": "中共漳县委员会", "overlap_period": "", "confidence": "confirmed"},
    # 王亚伟 - 李正文: 书记-统战部长
    {"person_a": "zhangxian_wang_yawei", "person_b": "zhangxian_li_zhengwen",
     "type": "superior_subordinate", "context": "县委书记-统战部长统战工作关系",
     "overlap_org": "中共漳县委员会", "overlap_period": "", "confidence": "confirmed"},
    # 李青鹏 - 朱继昌: 县长-副县长
    {"person_a": "zhangxian_li_qingpeng", "person_b": "zhangxian_zhu_jichang",
     "type": "superior_subordinate", "context": "县长-分管农业副县长工作关系",
     "overlap_org": "漳县人民政府", "overlap_period": "", "confidence": "confirmed"},
    # 李青鹏 - 张鹏飞: 县长-公安局长
    {"person_a": "zhangxian_li_qingpeng", "person_b": "zhangxian_zhang_pengfei",
     "type": "superior_subordinate", "context": "县长-分管公安副县长工作关系",
     "overlap_org": "漳县人民政府", "overlap_period": "", "confidence": "confirmed"},
    # 李青鹏 - 裴孔荣: 县长-人大主任
    {"person_a": "zhangxian_li_qingpeng", "person_b": "zhangxian_pei_kongrong",
     "type": "overlap", "context": "县政府-县人大监督与协作关系",
     "overlap_org": "漳县", "overlap_period": "", "confidence": "confirmed"},
    # 李青鹏 - 刘芝兰: 县长-政协主席
    {"person_a": "zhangxian_li_qingpeng", "person_b": "zhangxian_liu_zhilan",
     "type": "overlap", "context": "县政府-县政协协商民主关系",
     "overlap_org": "漳县", "overlap_period": "", "confidence": "confirmed"},
    # 王亚伟 - 裴孔荣: 书记-人大主任
    {"person_a": "zhangxian_wang_yawei", "person_b": "zhangxian_pei_kongrong",
     "type": "overlap", "context": "县委-县人大领导协作关系",
     "overlap_org": "漳县", "overlap_period": "", "confidence": "confirmed"},
    # 王亚伟 - 刘芝兰: 书记-政协主席
    {"person_a": "zhangxian_wang_yawei", "person_b": "zhangxian_liu_zhilan",
     "type": "overlap", "context": "县委-县政协领导协作关系",
     "overlap_org": "漳县", "overlap_period": "", "confidence": "confirmed"},
    # 李青鹏 - 郭元红: 县长-副县长
    {"person_a": "zhangxian_li_qingpeng", "person_b": "zhangxian_guo_yuanhong",
     "type": "superior_subordinate", "context": "县长-县委常委副县长工作关系",
     "overlap_org": "漳县人民政府", "overlap_period": "", "confidence": "confirmed"},
    # 李青鹏 - 魏军民: 县长-副县长
    {"person_a": "zhangxian_li_qingpeng", "person_b": "zhangxian_wei_junmin",
     "type": "superior_subordinate", "context": "县长-县委常委副县长工作关系",
     "overlap_org": "漳县人民政府", "overlap_period": "", "confidence": "confirmed"},
    # 纪委-县委 关联
    {"person_a": "zhangxian_wang_xiaojun", "person_b": "zhangxian_wang_yawei",
     "type": "superior_subordinate", "context": "纪委书记受县委和上级纪委双重领导",
     "overlap_org": "中共漳县委员会", "overlap_period": "", "confidence": "confirmed"},
    # 政法委-公安 关联
    {"person_a": "zhangxian_wang_jianfu", "person_b": "zhangxian_zhang_pengfei",
     "type": "overlap", "context": "政法委书记-公安局长政法系统协作关系",
     "overlap_org": "漳县政法系统", "overlap_period": "", "confidence": "confirmed"},
]


# ═══════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title and "人大" not in title and "政协" not in title and "副书记" not in title:
        return "255,50,50"     # Red — Party Secretary
    if "县长" in title and "副" not in title:
        return "50,100,255"    # Blue — Government head
    if "副书记" in title:
        return "200,50,50"     # Dark red — Deputy Secretary (includes县长)
    if "纪委" in title or "监委" in title:
        return "255,165,0"     # Orange — Discipline
    if "人大" in title:
        return "200,255,255"   # Cyan — PC
    if "政协" in title:
        return "255,240,200"   # Cream — PCC
    if "副" in title:
        return "100,100,200"   # Light blue — Deputy
    return "100,100,100"


def person_size(p):
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "人大" not in title and "政协" not in title and "副书记" not in title:
        return "20.0"
    if "县长" in title and "副" not in title:
        return "20.0"
    if "副书记" in title or "主任" in title or "主席" in title:
        return "14.0"
    if "常委" in title:
        return "12.0"
    if "副" in title:
        return "10.0"
    return "8.0"


def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


# ── Build Database ──

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS persons")
    c.execute("DROP TABLE IF EXISTS organizations")
    c.execute("DROP TABLE IF EXISTS positions")
    c.execute("DROP TABLE IF EXISTS relationships")

    c.execute("""CREATE TABLE persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id INTEGER, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", (
            p["id"], p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], p["education"],
            p["party_join"], p["work_start"], p["current_post"],
            p["current_org"], p["source"]
        ))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            pos["person_id"], pos["org_id"], pos["title"],
            pos["start"], pos["end"], pos["rank"], pos.get("note", "")
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (
            r["person_a"], r["person_b"], r["type"], r["context"],
            r["overlap_org"], r["overlap_period"]
        ))

    conn.commit()
    conn.close()


# ── Build GEXF ──

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>漳县领导班子工作关系网络 - 数据来源: 漳县人民政府官网</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="定西市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="定西市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (worked_at)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = r.get("confidence", "confirmed")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── Main ──

def main():
    print(f"=== 漳县网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")


if __name__ == "__main__":
    main()
