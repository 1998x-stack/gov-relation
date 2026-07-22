#!/usr/bin/env python3
"""通渭县 (定西市, 甘肃省) 领导班子工作关系网络数据构建脚本

数据来源: 通渭县人民政府官网 http://www.tongwei.gov.cn
页面: 通渭要闻 (col/col2038), 头条推荐 (col/col6784) 等新闻报道
访问日期: 2026-07-22
"""

import os
import sqlite3
from datetime import datetime

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "通渭县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "通渭县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据 (来源: tongwei.gov.cn 新闻报道, 2026-07-22)
# ═══════════════════════════════════════════════

persons = [
    # === 县委领导 ===
    {
        "id": "tongwei_shao_peng",
        "name": "邵鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "通渭县委书记",
        "current_org": "中共通渭县委员会",
        "source": "http://www.tongwei.gov.cn/art/2026/7/1/art_2038_1901232.html; http://www.tongwei.gov.cn/art/2026/7/8/art_2038_1902296.html",
    },
    {
        "id": "tongwei_zhu_jie",
        "name": "朱杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共通渭县委员会",
        "source": "http://www.tongwei.gov.cn/art/2026/6/25/art_2038_1900348.html; http://www.tongwei.gov.cn/art/2026/6/5/art_2038_1897797.html; http://www.tongwei.gov.cn/art/2026/7/14/art_2038_1903130.html",
    },
    {
        "id": "tongwei_chen_wenxin",
        "name": "陈文鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共通渭县纪律检查委员会/通渭县监察委员会",
        "source": "http://www.tongwei.gov.cn/art/2026/6/30/art_2038_1901176.html",
    },
    {
        "id": "tongwei_liu_zhijun",
        "name": "刘治军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "通渭县人民政府",
        "source": "http://www.tongwei.gov.cn/art/2026/7/3/art_2038_1901886.html; http://www.tongwei.gov.cn/art/2026/7/2/art_2038_1901467.html",
    },
    {
        "id": "tongwei_li_yuwei",
        "name": "李育伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共通渭县委员会宣传部",
        "source": "http://www.tongwei.gov.cn/art/2026/6/25/art_2038_1900188.html",
    },
    {
        "id": "tongwei_gong_weilong",
        "name": "龚维龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共通渭县委员会政法委员会",
        "source": "http://www.tongwei.gov.cn/art/2026/7/3/art_2038_1901889.html; http://www.tongwei.gov.cn/art/2026/7/2/art_2038_1901467.html",
    },
    {
        "id": "tongwei_zhang_hong",
        "name": "张红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共通渭县委员会",
        "source": "http://www.tongwei.gov.cn/art/2026/7/8/art_2038_1902296.html; http://www.tongwei.gov.cn/art/2026/6/30/art_2038_1901176.html",
    },
    {
        "id": "tongwei_wu_bin",
        "name": "吴彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共通渭县委员会",
        "source": "http://www.tongwei.gov.cn/art/2026/7/8/art_2038_1902296.html; http://www.tongwei.gov.cn/art/2026/6/25/art_2038_1900348.html",
    },
    {
        "id": "tongwei_he_yanjun",
        "name": "何艳君",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共通渭县委员会",
        "source": "http://www.tongwei.gov.cn/art/2026/7/8/art_2038_1902296.html; http://www.tongwei.gov.cn/art/2026/6/30/art_2038_1901176.html",
    },
    {
        "id": "tongwei_bao_xi",
        "name": "包玺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "通渭县人民政府",
        "source": "http://www.tongwei.gov.cn/art/2026/7/8/art_2038_1902296.html; http://www.tongwei.gov.cn/art/2026/7/3/art_2038_1901886.html",
    },
    {
        "id": "tongwei_yue_chen",
        "name": "岳晨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共通渭县委员会",
        "source": "http://www.tongwei.gov.cn/art/2026/7/8/art_2038_1902296.html",
    },
    {
        "id": "tongwei_wang_jiangtao",
        "name": "王江涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共通渭县委员会",
        "source": "http://www.tongwei.gov.cn/art/2026/6/30/art_2038_1901176.html; http://www.tongwei.gov.cn/art/2026/6/16/art_2038_1899044.html",
    },
    # === 县政府副县长（非县委常委）===
    {
        "id": "tongwei_zhang_xinxia",
        "name": "张新霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "通渭县人民政府",
        "source": "http://www.tongwei.gov.cn/art/2026/6/25/art_2038_1900281.html",
    },
    # === 县人大领导 ===
    {
        "id": "tongwei_zhao_hui",
        "name": "赵晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "通渭县人民代表大会常务委员会",
        "source": "http://www.tongwei.gov.cn/art/2026/7/1/art_2038_1901463.html; http://www.tongwei.gov.cn/art/2026/7/8/art_2038_1902296.html",
    },
    # === 县政协领导 ===
    {
        "id": "tongwei_zhu_yongqing",
        "name": "朱永庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协通渭县委员会",
        "source": "http://www.tongwei.gov.cn/art/2026/7/3/art_2038_1901769.html; http://www.tongwei.gov.cn/art/2026/7/8/art_2038_1902296.html",
    },
    {
        "id": "tongwei_chen_yaohui",
        "name": "陈耀辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协通渭县委员会",
        "source": "http://www.tongwei.gov.cn/art/2026/6/25/art_2038_1900188.html",
    },
    # === 其他领导 ===
    {
        "id": "tongwei_wang_dingwen",
        "name": "王定文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长候选人",
        "current_org": "通渭县人民政府",
        "source": "http://www.tongwei.gov.cn/art/2026/7/3/art_2038_1901886.html",
    },
    {
        "id": "tongwei_li_jinxiong",
        "name": "李金雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长/会议主持",
        "current_org": "通渭县人民政府",
        "source": "http://www.tongwei.gov.cn/art/2026/6/25/art_2038_1900348.html",
    },
]

# ═══════════════════════════════════════════════
# 组织机构数据
# ═══════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共通渭县委员会", "type": "党委", "level": "县处级", "parent": "中共定西市委员会", "location": "甘肃省定西市通渭县"},
    {"id": 2, "name": "通渭县人民政府", "type": "政府", "level": "县处级", "parent": "定西市人民政府", "location": "甘肃省定西市通渭县"},
    {"id": 3, "name": "中共通渭县纪律检查委员会/通渭县监察委员会", "type": "党委", "level": "县处级", "parent": "中共定西市纪律检查委员会", "location": "甘肃省定西市通渭县"},
    {"id": 4, "name": "中共通渭县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共通渭县委员会", "location": "甘肃省定西市通渭县"},
    {"id": 5, "name": "中共通渭县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共通渭县委员会", "location": "甘肃省定西市通渭县"},
    {"id": 6, "name": "通渭县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "定西市人民代表大会常务委员会", "location": "甘肃省定西市通渭县"},
    {"id": 7, "name": "政协通渭县委员会", "type": "政协", "level": "县处级", "parent": "政协定西市委员会", "location": "甘肃省定西市通渭县"},
    {"id": 8, "name": "中共定西市委员会", "type": "党委", "level": "地厅级", "parent": "中共甘肃省委员会", "location": "甘肃省定西市"},
    {"id": 9, "name": "定西市人民政府", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府", "location": "甘肃省定西市"},
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 邵鹏 — 县委书记
    {"person_id": "tongwei_shao_peng", "org_id": 1, "title": "通渭县委书记", "start": "", "end": "present", "rank": "正处级", "note": "2026年7月多篇新闻报道证实现任职务"},
    # 朱杰 — 县委副书记
    {"person_id": "tongwei_zhu_jie", "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "2026年6-7月多篇新闻报道以县委副书记身份出席会议"},
    # 陈文鑫 — 纪委书记
    {"person_id": "tongwei_chen_wenxin", "org_id": 3, "title": "县委常委、县纪委书记、县监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘治军 — 常务副县长
    {"person_id": "tongwei_liu_zhijun", "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "县国土空间规划委员会副主任"},
    # 李育伟 — 宣传部长
    {"person_id": "tongwei_li_yuwei", "org_id": 4, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 龚维龙 — 政法委书记
    {"person_id": "tongwei_gong_weilong", "org_id": 5, "title": "县委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张红 — 县委常委
    {"person_id": "tongwei_zhang_hong", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待查"},
    # 吴彬 — 县委常委
    {"person_id": "tongwei_wu_bin", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待查"},
    # 何艳君 — 县委常委
    {"person_id": "tongwei_he_yanjun", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待查"},
    # 包玺 — 副县长
    {"person_id": "tongwei_bao_xi", "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 岳晨 — 县委常委
    {"person_id": "tongwei_yue_chen", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待查"},
    # 王江涛 — 县委常委
    {"person_id": "tongwei_wang_jiangtao", "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "宣读县委表彰决定"},
    # 张新霞 — 副县长
    {"person_id": "tongwei_zhang_xinxia", "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 赵晖 — 人大主任
    {"person_id": "tongwei_zhao_hui", "org_id": 6, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 朱永庆 — 政协主席
    {"person_id": "tongwei_zhu_yongqing", "org_id": 7, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 陈耀辉 — 政协副主席
    {"person_id": "tongwei_chen_yaohui", "org_id": 7, "title": "县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王定文 — 副县长候选人
    {"person_id": "tongwei_wang_dingwen", "org_id": 2, "title": "县政府副县长候选人", "start": "", "end": "present", "rank": "副处级", "note": "出席国土空间规划委员会"},
    # 李金雄
    {"person_id": "tongwei_li_jinxiong", "org_id": 2, "title": "副县长/主持", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════

relationships = [
    # 邵鹏 - 朱杰: 书记-副书记搭班
    {"person_a": "tongwei_shao_peng", "person_b": "tongwei_zhu_jie",
     "type": "superior_subordinate", "context": "县委书记-县委副书记工作关系",
     "overlap_org": "中共通渭县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    # 邵鹏 - 陈文鑫: 书记-纪委书记
    {"person_a": "tongwei_shao_peng", "person_b": "tongwei_chen_wenxin",
     "type": "superior_subordinate", "context": "县委书记-纪委书记监督与被监督关系",
     "overlap_org": "中共通渭县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    # 邵鹏 - 刘治军: 书记-常务副县长
    {"person_a": "tongwei_shao_peng", "person_b": "tongwei_liu_zhijun",
     "type": "superior_subordinate", "context": "县委书记-常务副县长工作关系",
     "overlap_org": "中共通渭县委员会/通渭县人民政府", "overlap_period": "2026", "confidence": "confirmed"},
    # 邵鹏 - 李育伟: 书记-宣传部长
    {"person_a": "tongwei_shao_peng", "person_b": "tongwei_li_yuwei",
     "type": "superior_subordinate", "context": "县委书记-宣传部长意识形态工作关系",
     "overlap_org": "中共通渭县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    # 邵鹏 - 龚维龙: 书记-政法委书记
    {"person_a": "tongwei_shao_peng", "person_b": "tongwei_gong_weilong",
     "type": "superior_subordinate", "context": "县委书记-政法委书记关系，共同调研城市建设",
     "overlap_org": "中共通渭县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    # 邵鹏 - 包玺: 书记-副县长
    {"person_a": "tongwei_shao_peng", "person_b": "tongwei_bao_xi",
     "type": "superior_subordinate", "context": "县委书记-副县长关系",
     "overlap_org": "中共通渭县委员会/通渭县人民政府", "overlap_period": "2026", "confidence": "confirmed"},
    # 邵鹏 - 赵晖: 书记-人大主任
    {"person_a": "tongwei_shao_peng", "person_b": "tongwei_zhao_hui",
     "type": "overlap", "context": "县委书记-人大主任领导协作关系",
     "overlap_org": "通渭县", "overlap_period": "2026", "confidence": "confirmed"},
    # 邵鹏 - 朱永庆: 书记-政协主席
    {"person_a": "tongwei_shao_peng", "person_b": "tongwei_zhu_yongqing",
     "type": "overlap", "context": "县委书记-政协主席领导协作关系",
     "overlap_org": "通渭县", "overlap_period": "2026", "confidence": "confirmed"},
    # 邵鹏 - 王江涛: 书记-县委常委
    {"person_a": "tongwei_shao_peng", "person_b": "tongwei_wang_jiangtao",
     "type": "superior_subordinate", "context": "县委书记-县委常委工作关系",
     "overlap_org": "中共通渭县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    # 邵鹏 - 张红: 书记-县委常委
    {"person_a": "tongwei_shao_peng", "person_b": "tongwei_zhang_hong",
     "type": "superior_subordinate", "context": "县委书记-县委常委工作关系",
     "overlap_org": "中共通渭县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    # 邵鹏 - 吴彬: 书记-县委常委
    {"person_a": "tongwei_shao_peng", "person_b": "tongwei_wu_bin",
     "type": "superior_subordinate", "context": "县委书记-县委常委工作关系",
     "overlap_org": "中共通渭县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    # 邵鹏 - 何艳君: 书记-县委常委
    {"person_a": "tongwei_shao_peng", "person_b": "tongwei_he_yanjun",
     "type": "superior_subordinate", "context": "县委书记-县委常委工作关系",
     "overlap_org": "中共通渭县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    # 邵鹏 - 岳晨: 书记-县委常委
    {"person_a": "tongwei_shao_peng", "person_b": "tongwei_yue_chen",
     "type": "superior_subordinate", "context": "县委书记-县委常委工作关系",
     "overlap_org": "中共通渭县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    # 朱杰 - 吴彬: 副书记-县委常委
    {"person_a": "tongwei_zhu_jie", "person_b": "tongwei_wu_bin",
     "type": "overlap", "context": "县委副书记-县委常委，共同出席国评省考反馈问题整改推进会",
     "overlap_org": "中共通渭县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    # 朱杰 - 李金雄: 副书记-副县长
    {"person_a": "tongwei_zhu_jie", "person_b": "tongwei_li_jinxiong",
     "type": "superior_subordinate", "context": "县委副书记-副县长关系",
     "overlap_org": "中共通渭县委员会/通渭县人民政府", "overlap_period": "2026", "confidence": "confirmed"},
    # 刘治军 - 龚维龙: 共同调研城市建设
    {"person_a": "tongwei_liu_zhijun", "person_b": "tongwei_gong_weilong",
     "type": "overlap", "context": "常务副县长-政法委书记共同陪同县委书记调研",
     "overlap_org": "通渭县人民政府", "overlap_period": "2026", "confidence": "confirmed"},
    # 刘治军 - 包玺: 副县长同僚
    {"person_a": "tongwei_liu_zhijun", "person_b": "tongwei_bao_xi",
     "type": "overlap", "context": "常务副县长-县委常委副县长，共同出席国土规划委员会",
     "overlap_org": "通渭县人民政府", "overlap_period": "2026", "confidence": "confirmed"},
    # 陈文鑫 - 李育伟: 纪委书记-宣传部长
    {"person_a": "tongwei_chen_wenxin", "person_b": "tongwei_li_yuwei",
     "type": "overlap", "context": "纪委书记-宣传部长，共同出席廉洁文化主题书画展",
     "overlap_org": "中共通渭县委员会", "overlap_period": "2026", "confidence": "confirmed"},
    # 李育伟 - 包玺: 宣传部长-副县长
    {"person_a": "tongwei_li_yuwei", "person_b": "tongwei_bao_xi",
     "type": "overlap", "context": "宣传部长-副县长，共同出席廉洁文化主题书画展",
     "overlap_org": "", "overlap_period": "2026", "confidence": "confirmed"},
    # 包玺 - 陈耀辉: 副县长-政协副主席
    {"person_a": "tongwei_bao_xi", "person_b": "tongwei_chen_yaohui",
     "type": "overlap", "context": "副县长-政协副主席，共同出席篮球争霸赛开幕式",
     "overlap_org": "", "overlap_period": "2026", "confidence": "confirmed"},
    # 赵晖 - 朱永庆: 人大主任-政协主席
    {"person_a": "tongwei_zhao_hui", "person_b": "tongwei_zhu_yongqing",
     "type": "overlap", "context": "人大主任-政协主席，定期列席县委常委会",
     "overlap_org": "通渭县", "overlap_period": "2026", "confidence": "confirmed"},
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
    if "副书记" in title:
        return "200,50,50"     # Dark red — Deputy Secretary
    if "县长" in title and "副" not in title:
        return "50,100,255"    # Blue — Government head
    if "纪委" in title or "监委" in title:
        return "255,165,0"     # Orange — Discipline
    if "人大" in title:
        return "200,255,255"   # Cyan — PC
    if "政协" in title:
        return "255,240,200"   # Cream — PCC
    if "副" in title or "常务" in title:
        return "100,100,200"   # Light blue — Deputy
    if "常委" in title:
        return "100,100,100"   # Grey — Standing Committee member
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
    lines.append('    <description>通渭县领导班子工作关系网络 - 数据来源: 通渭县人民政府官网新闻报道</description>')
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
    print(f"=== 通渭县网络数据构建 ===")
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
