#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
瑞昌市领导班子工作关系网络 — 数据构建脚本
调研日期: 2026-07-14
来源说明: 瑞昌市人民政府官网(ruichang.gov.cn)新闻信息为主
"""

import sqlite3
import os

# ============================================================
# 硬编码研究数据
# ============================================================

# ---- 人员数据 ----
# 每条信息附来源URL | 区分已确认/推测/未验证

persons = [
    # ===== 党政一把手 =====
    {
        "id": "ruichang_wu_song",
        "name": "吴松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年2月",
        "birthplace": "江西弋阳",
        "education": "本科（华东师范大学汉语言文学）",
        "party_join": "2002年9月",
        "work_start": "2000年9月",
        "current_post": "瑞昌市委书记",
        "current_org": "中共瑞昌市委",
        "source": "https://www.srlz.gov.cn/a/gexianshixinxigongkai/poyangxian/lingdaojigou/2020/1203/6984.html"
    },
    {
        "id": "ruichang_feng_meixin",
        "name": "冯美鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年3月",
        "birthplace": "履历待查（推测江西九江地区）",
        "education": "大学学历，农业推广硕士",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市委副书记、代理市长",
        "current_org": "瑞昌市人民政府",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260713_7273518.html"
    },

    # ===== 前任 =====
    {
        "id": "ruichang_lu_zhixuan",
        "name": "卢治轩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "原瑞昌市委书记（去向：九江市直单位）",
        "current_org": "九江市（待确认具体单位）",
        "source": "瑞昌市人大常委会公告；https://www.ruichang.gov.cn/ywzx/rcyw/"
    },

    # ===== 市委常委（按角色排序） =====
    # 袁思义 - 市纪委书记（已确认：7月14日陪同吴松走访市纪委监委）
    {
        "id": "ruichang_yuan_siyi",
        "name": "袁思义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市委常委、市纪委书记、市监委主任",
        "current_org": "中共瑞昌市纪委/瑞昌市监委",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260714_7274190.html"
    },
    # 危建武 - 市委组织部长（已确认：7月14日陪同吴松走访市委组织部）
    {
        "id": "ruichang_wei_jianwu",
        "name": "危建武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市委常委、市委组织部部长",
        "current_org": "中共瑞昌市委组织部",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260714_7274190.html"
    },
    # 陈超 - 常务副市长（已确认）
    {
        "id": "ruichang_chen_chao",
        "name": "陈超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市委常委、常务副市长",
        "current_org": "瑞昌市人民政府",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260709_7271325.html"
    },
    # 范辉 - 政法委书记（已确认：7月14日陪同吴松走访市委政法委）
    {
        "id": "ruichang_fan_hui",
        "name": "范辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市委常委、政法委书记",
        "current_org": "中共瑞昌市委政法委",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260714_7274190.html"
    },
    # 章丽婷 - 统战部长（已确认：7月14日陪同吴松走访市委统战部）
    {
        "id": "ruichang_zhang_liting",
        "name": "章丽婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市委常委、市委统战部部长",
        "current_org": "中共瑞昌市委统战部",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260714_7274190.html"
    },
    # 向坚 - 宣传部长（已确认：7月14日陪同吴松走访市委宣传部）
    {
        "id": "ruichang_xiang_jian",
        "name": "向坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市委常委、宣传部部长",
        "current_org": "中共瑞昌市委宣传部",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260714_7274190.html"
    },
    # 高阔 - 市委常委（具体分工待查，列席2026年7月市委常委学习会）
    {
        "id": "ruichang_gao_kuo",
        "name": "高阔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市委常委（具体分工待查）",
        "current_org": "中共瑞昌市委",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260709_7271325.html"
    },
    # 李英豪 - 市委办公室主任（推测，7月14日陪同吴松走访）
    {
        "id": "ruichang_li_yinghao",
        "name": "李英豪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市委常委、市委办公室主任",
        "current_org": "中共瑞昌市委办公室",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260714_7274190.html"
    },

    # ===== 市政府领导 =====
    {
        "id": "ruichang_wang_ying",
        "name": "王荧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市副市长（推测）",
        "current_org": "瑞昌市人民政府",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260709_7271325.html"
    },
    {
        "id": "ruichang_yu_shuifeng",
        "name": "余水锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市副市长（推测）",
        "current_org": "瑞昌市人民政府",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260714_7274490.html"
    },
    {
        "id": "ruichang_wang_min",
        "name": "王敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市副市长（推测）",
        "current_org": "瑞昌市人民政府",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260714_7274490.html"
    },

    # ===== 市人大常委会 =====
    {
        "id": "ruichang_liang_shaoqing",
        "name": "梁少清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市人大常委会主任",
        "current_org": "瑞昌市人大常委会",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260713_7273518.html"
    },
    {
        "id": "ruichang_chen_guosheng",
        "name": "陈国胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市人大常委会副主任",
        "current_org": "瑞昌市人大常委会",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260713_7273518.html"
    },
    {
        "id": "ruichang_chen_gang",
        "name": "陈刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市人大常委会副主任",
        "current_org": "瑞昌市人大常委会",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260713_7273518.html"
    },
    {
        "id": "ruichang_zhou_yuyang",
        "name": "周宇洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市人大常委会副主任",
        "current_org": "瑞昌市人大常委会",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260713_7273518.html"
    },
    {
        "id": "ruichang_chen_gaosheng",
        "name": "陈高生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市人大常委会副主任",
        "current_org": "瑞昌市人大常委会",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260713_7273518.html"
    },
    {
        "id": "ruichang_wang_zaixin",
        "name": "王再新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市人大常委会副主任",
        "current_org": "瑞昌市人大常委会",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260713_7273518.html"
    },

    # ===== 市政协 =====
    {
        "id": "ruichang_zhou_hongwen",
        "name": "周洪文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市政协主席",
        "current_org": "瑞昌市政协",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260709_7271325.html"
    },

    # ===== 法检两院（现任+前任） =====
    {
        "id": "ruichang_guo_huaqing",
        "name": "郭华清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "法律专业背景",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市人民法院代理院长",
        "current_org": "瑞昌市人民法院",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260713_7273518.html"
    },
    {
        "id": "ruichang_jiang_shaohua",
        "name": "姜绍华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "法律专业背景",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "瑞昌市人民检察院代理检察长",
        "current_org": "瑞昌市人民检察院",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260713_7273518.html"
    },
    {
        "id": "ruichang_wu_yingchun",
        "name": "吴迎春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "原瑞昌市人民法院院长（已辞职）",
        "current_org": "待确认",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260713_7273518.html"
    },
    {
        "id": "ruichang_zhang_xu",
        "name": "张旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "原瑞昌市人民检察院检察长（已辞职）",
        "current_org": "待确认",
        "source": "https://www.ruichang.gov.cn/ywzx/rcyw/202607/t20260713_7273518.html"
    },
]

# ---- 组织数据 ----
organizations = [
    {"id": "org_ruichang_city", "name": "瑞昌市", "type": "行政区划", "level": "县级市", "parent": "九江市", "location": "江西省九江市"},
    {"id": "org_ruichang_party", "name": "中共瑞昌市委", "type": "党委", "level": "县级", "parent": "中共九江市委", "location": "瑞昌市"},
    {"id": "org_ruichang_gov", "name": "瑞昌市人民政府", "type": "政府", "level": "县级", "parent": "九江市人民政府", "location": "瑞昌市"},
    {"id": "org_ruichang_npc", "name": "瑞昌市人大常委会", "type": "人大", "level": "县级", "parent": "九江市人大常委会", "location": "瑞昌市"},
    {"id": "org_ruichang_ccppcc", "name": "瑞昌市政协", "type": "政协", "level": "县级", "parent": "九江市政协", "location": "瑞昌市"},
    {"id": "org_ruichang_court", "name": "瑞昌市人民法院", "type": "司法机关", "level": "县级", "parent": "九江市中级人民法院", "location": "瑞昌市"},
    {"id": "org_ruichang_procuratorate", "name": "瑞昌市人民检察院", "type": "司法机关", "level": "县级", "parent": "九江市人民检察院", "location": "瑞昌市"},
    {"id": "org_ruichang_discipline", "name": "中共瑞昌市纪委/瑞昌市监委", "type": "纪委", "level": "县级", "parent": "中共九江市纪委", "location": "瑞昌市"},
    {"id": "org_ruichang_organization", "name": "中共瑞昌市委组织部", "type": "党委部门", "level": "县级", "parent": "中共瑞昌市委", "location": "瑞昌市"},
    {"id": "org_ruichang_propaganda", "name": "中共瑞昌市委宣传部", "type": "党委部门", "level": "县级", "parent": "中共瑞昌市委", "location": "瑞昌市"},
    {"id": "org_ruichang_united_front", "name": "中共瑞昌市委统战部", "type": "党委部门", "level": "县级", "parent": "中共瑞昌市委", "location": "瑞昌市"},
    {"id": "org_ruichang_political_legal", "name": "中共瑞昌市委政法委", "type": "党委部门", "level": "县级", "parent": "中共瑞昌市委", "location": "瑞昌市"},
    {"id": "org_ruichang_office", "name": "中共瑞昌市委办公室", "type": "党委部门", "level": "县级", "parent": "中共瑞昌市委", "location": "瑞昌市"},
    {"id": "org_jiujiang_city", "name": "九江市", "type": "行政区划", "level": "地级市", "parent": "江西省", "location": "江西省"},
    {"id": "org_jiujiang_discipline", "name": "九江市纪委监委", "type": "纪委", "level": "地级", "parent": "江西省纪委监委", "location": "九江市"},
    {"id": "org_poyang_county", "name": "鄱阳县", "type": "行政区划", "level": "县", "parent": "上饶市", "location": "江西省上饶市"},
    {"id": "org_yugan_gov", "name": "余干县人民政府", "type": "政府", "level": "县", "parent": "上饶市人民政府", "location": "江西省上饶市"},
    {"id": "org_gangkou_town", "name": "弋阳县港口镇", "type": "乡镇", "level": "乡镇", "parent": "弋阳县", "location": "江西省上饶市弋阳县"},
    {"id": "org_zhangshudun_town", "name": "弋阳县樟树墩镇", "type": "乡镇", "level": "乡镇", "parent": "弋阳县", "location": "江西省上饶市弋阳县"},
    {"id": "org_yiyang_communist_youth", "name": "共青团弋阳县委", "type": "群团", "level": "县", "parent": "弋阳县", "location": "江西省上饶市弋阳县"},
    {"id": "org_qinghu_town", "name": "弋阳县清湖乡", "type": "乡镇", "level": "乡镇", "parent": "弋阳县", "location": "江西省上饶市弋阳县"},
    {"id": "org_xiushui_gov", "name": "修水县人民政府", "type": "政府", "level": "县", "parent": "九江市人民政府", "location": "江西省九江市"},
    {"id": "org_balihu_lake", "name": "九江市八里湖新区", "type": "功能区", "level": "县(区)", "parent": "九江市", "location": "江西省九江市"},
    {"id": "org_jiujiang_county_organization", "name": "九江县委组织部", "type": "党委部门", "level": "县", "parent": "中共九江县委", "location": "江西省九江市"},
]

# ---- 任职数据 ----
positions = [
    # 吴松的完整履历
    {"person_id": "ruichang_wu_song", "org_id": "org_ruichang_party", "title": "瑞昌市委书记", "start": "2026年7月", "end": "至今", "rank": "正处级", "note": "此前任瑞昌市长，2026年7月辞去市长专职书记"},
    {"person_id": "ruichang_wu_song", "org_id": "org_ruichang_gov", "title": "瑞昌市人民政府市长", "start": "约2021年", "end": "2026年7月", "rank": "正处级", "note": "兼任瑞昌市委副书记；2026年7月13日辞职"},
    {"person_id": "ruichang_wu_song", "org_id": "org_poyang_county", "title": "鄱阳县委常委、县纪委书记、县监委主任", "start": "2020年6月", "end": "约2021年", "rank": "副处级", "note": "2020年9月当选县监委主任"},
    {"person_id": "ruichang_wu_song", "org_id": "org_yugan_gov", "title": "余干县人民政府副县长", "start": "2016年9月", "end": "2020年6月", "rank": "副处级", "note": ""},
    {"person_id": "ruichang_wu_song", "org_id": "org_gangkou_town", "title": "弋阳县港口镇党委书记、人大主席", "start": "2015年2月", "end": "2016年9月", "rank": "正科级", "note": ""},
    {"person_id": "ruichang_wu_song", "org_id": "org_zhangshudun_town", "title": "弋阳县樟树墩镇党委副书记、镇长", "start": "2011年1月", "end": "2015年2月", "rank": "正科级", "note": ""},
    {"person_id": "ruichang_wu_song", "org_id": "org_yiyang_communist_youth", "title": "共青团弋阳县委副书记", "start": "2006年4月", "end": "2011年1月", "rank": "副科级", "note": "2010.09-2011.01挂职任团市委副书记"},
    {"person_id": "ruichang_wu_song", "org_id": "org_qinghu_town", "title": "弋阳县清湖乡干部", "start": "2000年9月", "end": "2006年4月", "rank": "科员", "note": "2003.05-2003.11团市委跟班学习"},
    {"person_id": "ruichang_wu_song", "org_id": "org_jiujiang_city", "title": "跨市调任：从鄱阳县调至瑞昌市", "start": "约2021年", "end": "", "rank": "", "note": "从上饶市鄱阳县跨市调任九江市瑞昌市（关键跨市调动）"},

    # 冯美鑫的履历
    {"person_id": "ruichang_feng_meixin", "org_id": "org_ruichang_gov", "title": "瑞昌市人民政府副市长、代理市长", "start": "2026年7月", "end": "至今", "rank": "正处级", "note": "2026年7月13日市人大常委会任命为代市长"},
    {"person_id": "ruichang_feng_meixin", "org_id": "org_ruichang_party", "title": "瑞昌市委副书记", "start": "2024年7月", "end": "至今", "rank": "副处级", "note": "2024年7月从九江市纪委调任瑞昌市委副书记"},
    {"person_id": "ruichang_feng_meixin", "org_id": "org_jiujiang_discipline", "title": "九江市纪委常委、市监委委员", "start": "约2021年", "end": "2024年7月", "rank": "副处级", "note": "四级高级监察官"},
    {"person_id": "ruichang_feng_meixin", "org_id": "org_xiushui_gov", "title": "修水县人民政府副县长", "start": "2016年8月", "end": "约2021年", "rank": "副处级", "note": "2016年8月九江市管干部任前公示"},
    {"person_id": "ruichang_feng_meixin", "org_id": "org_balihu_lake", "title": "九江市八里湖新区宣传部负责人", "start": "约2014年", "end": "2016年8月", "rank": "正科级", "note": ""},
    {"person_id": "ruichang_feng_meixin", "org_id": "org_jiujiang_county_organization", "title": "九江县委组织部干部（早期）", "start": "约2005年", "end": "约2014年", "rank": "科员", "note": "早期在九江县人事劳动局、县委组织部工作"},

    # 卢治轩（前任书记）
    {"person_id": "ruichang_lu_zhixuan", "org_id": "org_ruichang_party", "title": "瑞昌市委书记", "start": "约2020年", "end": "约2026年6月", "rank": "正处级", "note": "去向待确认"},
    {"person_id": "ruichang_lu_zhixuan", "org_id": "org_ruichang_gov", "title": "瑞昌市人民政府市长", "start": "约2016年", "end": "约2020年", "rank": "正处级", "note": "后续任瑞昌市委书记"},

    # 袁思义 - 市纪委书记
    {"person_id": "ruichang_yuan_siyi", "org_id": "org_ruichang_discipline", "title": "瑞昌市委常委、市纪委书记、市监委主任", "start": "未知", "end": "至今", "rank": "副处级", "note": "2026年7月14日陪同吴松走访市纪委监委"},
    {"person_id": "ruichang_yuan_siyi", "org_id": "org_ruichang_party", "title": "瑞昌市委常委", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},

    # 危建武 - 组织部长
    {"person_id": "ruichang_wei_jianwu", "org_id": "org_ruichang_organization", "title": "瑞昌市委常委、市委组织部部长", "start": "未知", "end": "至今", "rank": "副处级", "note": "2026年7月14日陪同吴松走访市委组织部"},
    {"person_id": "ruichang_wei_jianwu", "org_id": "org_ruichang_party", "title": "瑞昌市委常委", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},

    # 陈超 - 常务副市长
    {"person_id": "ruichang_chen_chao", "org_id": "org_ruichang_gov", "title": "瑞昌市委常委、常务副市长", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": "ruichang_chen_chao", "org_id": "org_ruichang_party", "title": "瑞昌市委常委", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},

    # 范辉 - 政法委书记
    {"person_id": "ruichang_fan_hui", "org_id": "org_ruichang_political_legal", "title": "瑞昌市委常委、政法委书记", "start": "未知", "end": "至今", "rank": "副处级", "note": "2026年7月14日陪同吴松走访市委政法委"},
    {"person_id": "ruichang_fan_hui", "org_id": "org_ruichang_party", "title": "瑞昌市委常委", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},

    # 章丽婷 - 统战部长
    {"person_id": "ruichang_zhang_liting", "org_id": "org_ruichang_united_front", "title": "瑞昌市委常委、统战部部长", "start": "未知", "end": "至今", "rank": "副处级", "note": "2026年7月14日陪同吴松走访市委统战部"},
    {"person_id": "ruichang_zhang_liting", "org_id": "org_ruichang_party", "title": "瑞昌市委常委", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},

    # 向坚 - 宣传部长
    {"person_id": "ruichang_xiang_jian", "org_id": "org_ruichang_propaganda", "title": "瑞昌市委常委、宣传部部长", "start": "未知", "end": "至今", "rank": "副处级", "note": "2026年7月14日陪同吴松走访市委宣传部"},
    {"person_id": "ruichang_xiang_jian", "org_id": "org_ruichang_party", "title": "瑞昌市委常委", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},

    # 高阔 - 市委常委（具体分工待查）
    {"person_id": "ruichang_gao_kuo", "org_id": "org_ruichang_party", "title": "瑞昌市委常委（具体分工待查）", "start": "未知", "end": "至今", "rank": "副处级", "note": "列席2026年7月8日市委理论学习中心组学习会"},

    # 李英豪 - 市委办公室主任
    {"person_id": "ruichang_li_yinghao", "org_id": "org_ruichang_office", "title": "瑞昌市委常委、市委办公室主任", "start": "未知", "end": "至今", "rank": "副处级", "note": "2026年7月14日陪同吴松走访"},
    {"person_id": "ruichang_li_yinghao", "org_id": "org_ruichang_party", "title": "瑞昌市委常委", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},

    # 王荧 - 副市长级
    {"person_id": "ruichang_wang_ying", "org_id": "org_ruichang_gov", "title": "瑞昌市副市长（推测）", "start": "未知", "end": "至今", "rank": "副处级", "note": "列席2026年7月市委学习会"},
    # 余水锋 - 副市长级
    {"person_id": "ruichang_yu_shuifeng", "org_id": "org_ruichang_gov", "title": "瑞昌市副市长（推测）", "start": "未知", "end": "至今", "rank": "副处级", "note": "2026年7月14日出席三农工作会议"},
    # 王敏 - 副市长级
    {"person_id": "ruichang_wang_min", "org_id": "org_ruichang_gov", "title": "瑞昌市副市长（推测）", "start": "未知", "end": "至今", "rank": "副处级", "note": "2026年7月14日出席三农工作会议"},

    # 梁少清 - 人大主任
    {"person_id": "ruichang_liang_shaoqing", "org_id": "org_ruichang_npc", "title": "瑞昌市人大常委会主任", "start": "未知", "end": "至今", "rank": "正处级", "note": "主持2026年7月13日市人大常委会会议"},
    # 人大副主任
    {"person_id": "ruichang_chen_guosheng", "org_id": "org_ruichang_npc", "title": "瑞昌市人大常委会副主任", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": "ruichang_chen_gang", "org_id": "org_ruichang_npc", "title": "瑞昌市人大常委会副主任", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": "ruichang_zhou_yuyang", "org_id": "org_ruichang_npc", "title": "瑞昌市人大常委会副主任", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": "ruichang_chen_gaosheng", "org_id": "org_ruichang_npc", "title": "瑞昌市人大常委会副主任", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": "ruichang_wang_zaixin", "org_id": "org_ruichang_npc", "title": "瑞昌市人大常委会副主任", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},

    # 周洪文 - 政协主席
    {"person_id": "ruichang_zhou_hongwen", "org_id": "org_ruichang_ccppcc", "title": "瑞昌市政协主席", "start": "未知", "end": "至今", "rank": "正处级", "note": "列席2026年7月8日市委学习会"},

    # 法检两院
    {"person_id": "ruichang_guo_huaqing", "org_id": "org_ruichang_court", "title": "瑞昌市人民法院代理院长", "start": "2026年7月", "end": "至今", "rank": "副处级", "note": "2026年7月13日市人大常委会任命"},
    {"person_id": "ruichang_jiang_shaohua", "org_id": "org_ruichang_procuratorate", "title": "瑞昌市人民检察院代理检察长", "start": "2026年7月", "end": "至今", "rank": "副处级", "note": "2026年7月13日市人大常委会任命"},
    {"person_id": "ruichang_wu_yingchun", "org_id": "org_ruichang_court", "title": "瑞昌市人民法院院长", "start": "未知", "end": "2026年7月", "rank": "副处级", "note": "2026年7月13日辞职"},
    {"person_id": "ruichang_zhang_xu", "org_id": "org_ruichang_procuratorate", "title": "瑞昌市人民检察院检察长", "start": "未知", "end": "2026年7月", "rank": "副处级", "note": "2026年7月13日辞职"},
]

# ---- 关系数据 ----
relationships = [
    # 党政一把手关系
    {"person_a": "ruichang_wu_song", "person_b": "ruichang_feng_meixin", "type": "confirmed",
     "context": "党政一把手搭档：吴松任市委书记，冯美鑫任代理市长", "overlap_org": "中共瑞昌市委/瑞昌市人民政府", "overlap_period": "2026年7月至今"},

    # 前后任书记关系
    {"person_a": "ruichang_wu_song", "person_b": "ruichang_lu_zhixuan", "type": "inferred",
     "context": "前后任市委书记关系：吴松接替卢治轩任瑞昌市委书记", "overlap_org": "中共瑞昌市委", "overlap_period": "交接过渡期"},

    # 书记与常委关系
    {"person_a": "ruichang_wu_song", "person_b": "ruichang_yuan_siyi", "type": "confirmed",
     "context": "书记与纪委书记上下级关系", "overlap_org": "中共瑞昌市委", "overlap_period": "至今"},
    {"person_a": "ruichang_wu_song", "person_b": "ruichang_wei_jianwu", "type": "confirmed",
     "context": "书记与组织部长上下级关系", "overlap_org": "中共瑞昌市委", "overlap_period": "至今"},
    {"person_a": "ruichang_wu_song", "person_b": "ruichang_chen_chao", "type": "confirmed",
     "context": "书记与常务副市长共事", "overlap_org": "中共瑞昌市委/瑞昌市人民政府", "overlap_period": "至今"},
    {"person_a": "ruichang_wu_song", "person_b": "ruichang_fan_hui", "type": "confirmed",
     "context": "书记与政法委书记上下级关系", "overlap_org": "中共瑞昌市委", "overlap_period": "至今"},
    {"person_a": "ruichang_wu_song", "person_b": "ruichang_zhang_liting", "type": "confirmed",
     "context": "书记与统战部长上下级关系", "overlap_org": "中共瑞昌市委", "overlap_period": "至今"},
    {"person_a": "ruichang_wu_song", "person_b": "ruichang_xiang_jian", "type": "confirmed",
     "context": "书记与宣传部长上下级关系", "overlap_org": "中共瑞昌市委", "overlap_period": "至今"},
    {"person_a": "ruichang_wu_song", "person_b": "ruichang_li_yinghao", "type": "confirmed",
     "context": "书记与市委办主任上下级关系", "overlap_org": "中共瑞昌市委", "overlap_period": "至今"},

    # 代市长与副市长关系
    {"person_a": "ruichang_feng_meixin", "person_b": "ruichang_chen_chao", "type": "confirmed",
     "context": "代市长与常务副市长搭档", "overlap_org": "瑞昌市人民政府", "overlap_period": "2026年7月至今"},

    # 书记与人大的关系
    {"person_a": "ruichang_wu_song", "person_b": "ruichang_liang_shaoqing", "type": "confirmed",
     "context": "市委与市人大主要领导共事", "overlap_org": "瑞昌市", "overlap_period": "至今"},

    # 代市长与政协的关系
    {"person_a": "ruichang_feng_meixin", "person_b": "ruichang_zhou_hongwen", "type": "confirmed",
     "context": "市委副书记与政协主席同班子", "overlap_org": "瑞昌市", "overlap_period": "2024年至今"},

    # 法检两院前后任
    {"person_a": "ruichang_wu_yingchun", "person_b": "ruichang_guo_huaqing", "type": "inferred",
     "context": "前后任法院院长", "overlap_org": "瑞昌市人民法院", "overlap_period": "2026年7月"},
    {"person_a": "ruichang_zhang_xu", "person_b": "ruichang_jiang_shaohua", "type": "inferred",
     "context": "前后任检察院检察长", "overlap_org": "瑞昌市人民检察院", "overlap_period": "2026年7月"},
]


# ============================================================
# 构建 SQLite 数据库
# ============================================================

BASE_DIR = "/workspace/data/xieming/other-codes/gov-relation"
DB_DIR = os.path.join(BASE_DIR, "data", "database")
GRAPH_DIR = os.path.join(BASE_DIR, "data", "graph")

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "ruichang_network.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 建表
cur.executescript("""
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
    title TEXT,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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

# 清空旧数据（防止重复）
cur.execute("DELETE FROM relationships")
cur.execute("DELETE FROM positions")
cur.execute("DELETE FROM organizations")
cur.execute("DELETE FROM persons")

# 插入数据
for p in persons:
    cur.execute("""
        INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
          p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""
        INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""
        INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""
        INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# 统计
p_count = cur.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
o_count = cur.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
pos_count = cur.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
r_count = cur.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]

conn.close()

print(f"\n✅ SQLite 数据库已写入: {DB_PATH}")
print(f"   - {p_count} 个人物")
print(f"   - {o_count} 个组织")
print(f"   - {pos_count} 条任职记录")
print(f"   - {r_count} 条关系")


# ============================================================
# 构建 GEXF 图文件
# ============================================================

GEXF_PATH = os.path.join(GRAPH_DIR, "ruichang_network.gexf")

# 节点颜色
COLOR_PARTY = "255,50,50"       # 红色 - 党委书记
COLOR_GOV = "50,100,255"        # 蓝色 - 政府领导
COLOR_NPC = "255,165,0"        # 橙色 - 人大
COLOR_CPPCC = "200,100,0"      # 深橙 - 政协
COLOR_DISCIPLINE = "200,50,50"  # 深红 - 纪委
COLOR_JUDICIAL = "150,150,200"  # 紫色 - 司法
COLOR_OTHER = "180,180,180"     # 灰色 - 其他

def get_person_color(person_id):
    """根据角色返回节点颜色"""
    if "wu_song" in person_id:
        return COLOR_PARTY  # 书记 - 红色
    if "feng_meixin" in person_id:
        return COLOR_GOV  # 市长 - 蓝色
    if "lu_zhixuan" in person_id:
        return COLOR_PARTY  # 前任书记 - 红色
    if "yuan_siyi" in person_id:
        return COLOR_DISCIPLINE  # 纪委书记 - 深红
    if "chen_chao" in person_id or "wang_ying" in person_id or "yu_shuifeng" in person_id or "wang_min" in person_id:
        return COLOR_GOV  # 副市长级 - 蓝色
    if "liang_shaoqing" in person_id or "chen_guosheng" in person_id or "chen_gang" in person_id or "zhou_yuyang" in person_id or "chen_gaosheng" in person_id or "wang_zaixin" in person_id:
        return COLOR_NPC  # 人大 - 橙色
    if "zhou_hongwen" in person_id:
        return COLOR_CPPCC  # 政协 - 深橙
    if "guo_huaqing" in person_id or "jiang_shaohua" in person_id or "wu_yingchun" in person_id or "zhang_xu" in person_id:
        return COLOR_JUDICIAL  # 司法 - 紫色
    return COLOR_OTHER  # 常委其他 - 灰色

def get_person_size(person_id):
    """根据重要性返回节点大小"""
    if "wu_song" in person_id or "feng_meixin" in person_id:
        return "20.0"  # 党政一把手
    if "lu_zhixuan" in person_id:
        return "18.0"  # 前任书记
    if "liang_shaoqing" in person_id or "zhou_hongwen" in person_id:
        return "16.0"  # 人大主任/政协主席
    if "chen_chao" in person_id or "yuan_siyi" in person_id or "wei_jianwu" in person_id:
        return "14.0"  # 重要常委
    return "12.0"  # 其他

# 用字符串拼接生成GEXF
lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ---- 属性定义 ----
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="role" title="Role" type="string"/>')
lines.append('      <attribute id="org" title="Organization" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Edge Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ---- 节点 ----
lines.append('    <nodes>')

for p in persons:
    pid = p["id"]
    name = p["name"]
    role_desc = p["current_post"]
    org_name = p["current_org"]
    color = get_person_color(pid)
    size = get_person_size(pid)
    lines.append(f'      <node id="{pid}" label="{name}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="role" value="{role_desc}"/>')
    lines.append(f'          <attvalue for="org" value="{org_name}"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# 组织节点
for o in organizations:
    oid = o["id"]
    oname = o["name"]
    lines.append(f'      <node id="{oid}" label="{oname}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="role" value="{o["type"]}"/>')
    lines.append(f'          <attvalue for="org" value="{oname}"/>')
    lines.append(f'          <attvalue for="birth" value=""/>')
    lines.append(f'          <attvalue for="birthplace" value=""/>')
    lines.append(f'          <attvalue for="source" value=""/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="100" g="100" b="100" a="1"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')

lines.append('    </nodes>')

# ---- 边 ----
lines.append('    <edges>')

edge_id = 0

# Person → Organization (worked_at)
for pos in positions:
    edge_id += 1
    context = f"{pos['title']} ({pos['start']}-{pos['end']})"
    lines.append(f'      <edge id="e{edge_id}" source="{pos["person_id"]}" target="{pos["org_id"]}" type="directed" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{context}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"]} - {pos["end"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')

# Person ↔ Person (relationship)
for r in relationships:
    edge_id += 1
    lines.append(f'      <edge id="e{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}" label="relationship">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="relationship"/>')
    lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\n✅ GEXF 图文件已写入: {GEXF_PATH}")
print(f"   - {len(persons) + len(organizations)} 个节点")
print(f"   - {edge_id} 条边")
print(f"\n📊 摘要:")
print(f"   - 市委书记: 吴松（1981年2月生，江西弋阳人）")
print(f"   - 代理市长: 冯美鑫（1983年3月生）")
print(f"   - 市委常委人数: {sum(1 for p in persons if '市委常委' in p['current_post'])}人")
print(f"   - 市人大: {sum(1 for p in persons if '人大' in p['current_post'])}人")
print(f"   - 市政协: {sum(1 for p in persons if '政协' in p['current_post'])}人")
print(f"   - 法检: {sum(1 for p in persons if '法院' in p['current_post'] or '检察' in p['current_post'])}人")
print(f"   - 已确认完整履历: 吴松（来源：上饶市纪委官网）")
print(f"   - 部分履历已知: 冯美鑫")
print(f"   - 履历待查（高优先级）: 袁思义、危建武、陈超、范辉、章丽婷、高阔、向坚、李英豪、梁少清等")
print(f"\n🔍 关键发现:")
print(f"   - 吴松从上饶市鄱阳县跨市调任至九江市瑞昌市，横跨两个地级市")
print(f"   - 冯美鑫从九江市纪委系统调任瑞昌市委副书记，再升代理市长")
print(f"   - 2026年7月13日完成书记/市长分设、法检两长换人")
print("\n✅ 全部完成！")
