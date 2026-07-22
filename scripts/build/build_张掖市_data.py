#!/usr/bin/env python3
"""
张掖市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

数据来源:
- 张掖市人民政府官方网站 (www.zhangye.gov.cn), 2026年7月确认
- 百度百科/百度搜索 (多渠道交叉验证)
- 任前公示 (甘肃组工网)
- 新闻报道 (中国经济网, 网易, thepaper.cn 等)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── 路径 ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING_DIR = SCRIPT_DIR  # 脚本在暂存目录内
DB_PATH = os.path.join(STAGING_DIR, "张掖市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "张掖市_network.gexf")

# ── 数据 ──────────────────────────────────────────────

# 1. 人员
persons = [
    # (id, name, gender, ethnicity, birth, birthplace, native_place, education, party_join, work_start, current_post, current_org, source, person_id_unique)
    {
        "id": "p01",
        "name": "李兴华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委书记",
        "current_org": "中共张掖市委员会",
        "source": "张掖市人民政府官网(zhangye.gov.cn), 2026-07",
        "person_id": "zhangye_li_xinghua"
    },
    {
        "id": "p02",
        "name": "叶尔波力·孜汗",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "1973年5月",
        "birthplace": "新疆阿勒泰地区",
        "native_place": "新疆阿勒泰",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1996年9月",
        "current_post": "张掖市委副书记、市政府党组书记、市长",
        "current_org": "张掖市人民政府",
        "source": "张掖市人民政府官网, 百度百科, 新闻报道",
        "person_id": "zhangye_yeerboli_zihan"
    },
    {
        "id": "p03",
        "name": "李泽文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年7月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生/工程硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委副书记、政法委书记",
        "current_org": "中共张掖市委员会",
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "zhangye_li_zewen"
    },
    {
        "id": "p04",
        "name": "景国诚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生/法学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委常委、市纪委书记、市监委主任",
        "current_org": "中共张掖市纪律检查委员会",
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "zhangye_jing_guocheng"
    },
    {
        "id": "p05",
        "name": "张永刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年12月",
        "birthplace": "甘肃甘谷",
        "native_place": "甘肃甘谷",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1992年7月",
        "current_post": "张掖市委常委、常务副市长",
        "current_org": "张掖市人民政府",
        "source": "张掖市人民政府官网, 百度百科, 新闻报道",
        "person_id": "zhangye_zhang_yonggang"
    },
    {
        "id": "p06",
        "name": "杨宪辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生/医学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委常委、市委秘书长",
        "current_org": "中共张掖市委员会",
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "zhangye_yang_xianhui"
    },
    {
        "id": "p07",
        "name": "李毓刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生/法律硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委常委、组织部部长",
        "current_org": "中共张掖市委员会组织部",
        "source": "张掖市人民政府官网, 百度百科, 2026-07",
        "person_id": "zhangye_li_yugang"
    },
    {
        "id": "p08",
        "name": "王韶华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委常委、副市长、宣传部部长",
        "current_org": "中共张掖市委员会宣传部",
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "zhangye_wang_shaohua"
    },
    {
        "id": "p09",
        "name": "李锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委常委、甘州区委书记",
        "current_org": "中共甘州区委员会",
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "zhangye_li_rui"
    },
    {
        "id": "p10",
        "name": "芦建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委常委、张掖军分区司令员",
        "current_org": "张掖军分区",
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "zhangye_lu_jianping"
    },
    {
        "id": "p11",
        "name": "白冰",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1977年7月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生/正高级工程师",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委常委、副市长",
        "current_org": "张掖市人民政府",
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "zhangye_bai_bing"
    },
    {
        "id": "p12",
        "name": "武冰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委常委、统战部部长",
        "current_org": "中共张掖市委员会统战部",
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "zhangye_wu_bing"
    },
    {
        "id": "p13",
        "name": "娄金华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "农工党",
        "work_start": "待查",
        "current_post": "张掖市副市长",
        "current_org": "张掖市人民政府",
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "zhangye_lou_jinhua"
    },
    {
        "id": "p14",
        "name": "安宏亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市副市长、市公安局局长",
        "current_org": "张掖市公安局",
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "zhangye_an_hongliang"
    },
    {
        "id": "p15",
        "name": "陆思东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学/公共管理硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市副市长",
        "current_org": "张掖市人民政府",
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "zhangye_lu_sidong"
    },
    {
        "id": "p16",
        "name": "杨育林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年7月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "函授大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市政府秘书长",
        "current_org": "张掖市人民政府",
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "zhangye_yang_yulin"
    },
    # 前任领导
    {
        "id": "p17",
        "name": "卢小亨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年1月",
        "birthplace": "甘肃通渭",
        "native_place": "甘肃通渭",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1993年6月",
        "current_post": "甘肃省交通运输厅厅长",
        "current_org": "甘肃省交通运输厅",
        "source": "任前公示, 新闻报道, 百度百科",
        "person_id": "zhangye_lu_xiaoheng"
    },
    {
        "id": "p18",
        "name": "赵立香",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "河北滦南",
        "native_place": "河北滦南",
        "education": "大学/公共管理硕士",
        "party_join": "中共党员",
        "work_start": "1997年7月",
        "current_post": "兰州理工大学党委书记",
        "current_org": "兰州理工大学",
        "source": "任前公示, 新闻报道, 百度百科",
        "person_id": "zhangye_zhao_lixiang"
    },
    {
        "id": "p19",
        "name": "杨维俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962年9月",
        "birthplace": "甘肃静宁",
        "native_place": "甘肃静宁",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1982年7月",
        "current_post": "甘肃省人大法制委员会主任委员",
        "current_org": "甘肃省人民代表大会",
        "source": "新闻报道, 百度百科",
        "person_id": "zhangye_yang_weijun"
    },
    {
        "id": "p20",
        "name": "谢又生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年10月",
        "birthplace": "甘肃华亭",
        "native_place": "甘肃华亭",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1989年7月",
        "current_post": "甘肃省司法厅厅长",
        "current_org": "甘肃省司法厅",
        "source": "新闻报道, 百度百科",
        "person_id": "zhangye_xie_yousheng"
    },
]

# 2. 组织机构
organizations = [
    {"id": "o01", "name": "中共张掖市委员会", "type": "党委", "level": "地级", "parent": "中共甘肃省委员会", "location": "甘肃省张掖市"},
    {"id": "o02", "name": "张掖市人民政府", "type": "政府", "level": "地级", "parent": "甘肃省人民政府", "location": "甘肃省张掖市"},
    {"id": "o03", "name": "中共张掖市纪律检查委员会", "type": "党委", "level": "地级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市"},
    {"id": "o04", "name": "中共张掖市委员会组织部", "type": "党委", "level": "地级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市"},
    {"id": "o05", "name": "中共张掖市委员会宣传部", "type": "党委", "level": "地级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市"},
    {"id": "o06", "name": "中共张掖市委员会统战部", "type": "党委", "level": "地级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市"},
    {"id": "o07", "name": "中共张掖市委员会政法委员会", "type": "党委", "level": "地级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市"},
    {"id": "o08", "name": "中共甘州区委员会", "type": "党委", "level": "县处级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市甘州区"},
    {"id": "o09", "name": "张掖军分区", "type": "事业单位", "level": "地级", "parent": "甘肃省军区", "location": "甘肃省张掖市"},
    {"id": "o10", "name": "张掖市公安局", "type": "政府", "level": "地级", "parent": "张掖市人民政府", "location": "甘肃省张掖市"},
    {"id": "o11", "name": "甘肃省交通运输厅", "type": "政府", "level": "省级", "parent": "甘肃省人民政府", "location": "甘肃省兰州市"},
    {"id": "o12", "name": "兰州理工大学", "type": "事业单位", "level": "省级", "parent": "甘肃省人民政府", "location": "甘肃省兰州市"},
    {"id": "o13", "name": "甘肃省人民代表大会", "type": "人大", "level": "省级", "parent": "甘肃省", "location": "甘肃省兰州市"},
    {"id": "o14", "name": "甘肃省司法厅", "type": "政府", "level": "省级", "parent": "甘肃省人民政府", "location": "甘肃省兰州市"},
    {"id": "o15", "name": "张掖市政协", "type": "政协", "level": "地级", "parent": "张掖市", "location": "甘肃省张掖市"},
    {"id": "o16", "name": "张掖市人大常委会", "type": "人大", "level": "地级", "parent": "张掖市", "location": "甘肃省张掖市"},
    {"id": "o17", "name": "中共张掖市委员会办公室", "type": "党委", "level": "地级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市"},
]

# 3. 任职
positions = [
    # 李兴华
    {"person_id": "p01", "org_id": "o01", "title": "张掖市委书记", "start": "2025?", "end": "至今", "rank": "正厅级", "note": "主持市委全面工作, 来源于zhangye.gov.cn 2026-07"},
    # 叶尔波力·孜汗
    {"person_id": "p02", "org_id": "o01", "title": "张掖市委副书记", "start": "2024?", "end": "至今", "rank": "副厅级", "note": "兼任市长"},
    {"person_id": "p02", "org_id": "o02", "title": "张掖市市长", "start": "2024?", "end": "至今", "rank": "正厅级", "note": "主持市政府全面工作"},
    # 李泽文
    {"person_id": "p03", "org_id": "o01", "title": "张掖市委副书记", "start": "2025?", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p03", "org_id": "o07", "title": "张掖市委政法委书记", "start": "2025?", "end": "至今", "rank": "副厅级", "note": "兼任"},
    # 景国诚
    {"person_id": "p04", "org_id": "o03", "title": "张掖市纪委书记、市监委主任", "start": "?", "end": "至今", "rank": "副厅级", "note": "二级高级监察官"},
    # 张永刚
    {"person_id": "p05", "org_id": "o02", "title": "张掖市常务副市长", "start": "2024?", "end": "至今", "rank": "副厅级", "note": "从陇南市委常委、组织部部长调任"},
    # 杨宪辉
    {"person_id": "p06", "org_id": "o17", "title": "张掖市委秘书长", "start": "?", "end": "至今", "rank": "副厅级", "note": ""},
    # 李毓刚
    {"person_id": "p07", "org_id": "o04", "title": "张掖市委组织部部长", "start": "2024?", "end": "至今", "rank": "副厅级", "note": "兼任市委党校校长; 从省民政厅纪检组长调任"},
    # 王韶华
    {"person_id": "p08", "org_id": "o05", "title": "张掖市委宣传部部长", "start": "?", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p08", "org_id": "o02", "title": "张掖市副市长", "start": "?", "end": "至今", "rank": "副厅级", "note": "兼任"},
    # 李锐
    {"person_id": "p09", "org_id": "o08", "title": "甘州区委书记", "start": "?", "end": "至今", "rank": "副厅级", "note": "兼任市委常委"},
    # 芦建平
    {"person_id": "p10", "org_id": "o09", "title": "张掖军分区司令员", "start": "?", "end": "至今", "rank": "副厅级", "note": "兼任市委常委"},
    # 白冰
    {"person_id": "p11", "org_id": "o02", "title": "张掖市副市长", "start": "?", "end": "至今", "rank": "副厅级", "note": "分管科技、商贸、大数据"},
    # 武冰
    {"person_id": "p12", "org_id": "o06", "title": "张掖市委统战部部长", "start": "2026?", "end": "至今", "rank": "副厅级", "note": ""},
    # 娄金华
    {"person_id": "p13", "org_id": "o02", "title": "张掖市副市长", "start": "?", "end": "至今", "rank": "副厅级", "note": "分管教育、卫健、文旅; 农工党"},
    # 安宏亮
    {"person_id": "p14", "org_id": "o02", "title": "张掖市副市长", "start": "?", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p14", "org_id": "o10", "title": "张掖市公安局局长", "start": "?", "end": "至今", "rank": "副厅级", "note": "兼任"},
    # 陆思东
    {"person_id": "p15", "org_id": "o02", "title": "张掖市副市长", "start": "?", "end": "至今", "rank": "副厅级", "note": "分管工信、交通、国资"},
    # 杨育林
    {"person_id": "p16", "org_id": "o17", "title": "张掖市政府秘书长", "start": "?", "end": "至今", "rank": "正处级", "note": ""},
    # 前任: 卢小亨
    {"person_id": "p17", "org_id": "o01", "title": "张掖市委书记", "start": "2021-07", "end": "2024/2025", "rank": "正厅级", "note": "前任; 后调任甘肃省交通运输厅厅长"},
    {"person_id": "p17", "org_id": "o11", "title": "甘肃省交通运输厅厅长", "start": "2025?", "end": "至今", "rank": "正厅级", "note": ""},
    # 前任: 赵立香
    {"person_id": "p18", "org_id": "o02", "title": "张掖市市长", "start": "2021-08", "end": "2024?", "rank": "正厅级", "note": "前任; 后调任兰州理工大学党委书记"},
    {"person_id": "p18", "org_id": "o12", "title": "兰州理工大学党委书记", "start": "2024?", "end": "至今", "rank": "正厅级", "note": ""},
    # 前任: 杨维俊
    {"person_id": "p19", "org_id": "o01", "title": "张掖市委书记", "start": "2017", "end": "2021-07", "rank": "正厅级", "note": "前任; 后调任省人大"},
    {"person_id": "p19", "org_id": "o13", "title": "甘肃省人大法制委员会主任委员", "start": "2021-07", "end": "至今", "rank": "正厅级", "note": ""},
    # 前任: 谢又生
    {"person_id": "p20", "org_id": "o02", "title": "张掖市市长", "start": "2018", "end": "2021-07", "rank": "正厅级", "note": "前任; 后调任省司法厅"},
    {"person_id": "p20", "org_id": "o14", "title": "甘肃省司法厅厅长", "start": "2021-07", "end": "至今", "rank": "正厅级", "note": ""},
]

# 4. 关系
relationships = [
    # 现任班子内部关系
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "李兴华(书记)与叶尔波力·孜汗(市长): 党政一把手配合作", "overlap_org": "中共张掖市委员会/张掖市人民政府", "overlap_period": "2025?至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p03", "type": "overlap", "context": "李兴华(书记)与李泽文(副书记/政法委书记): 上下级关系", "overlap_org": "中共张掖市委员会", "overlap_period": "2025?至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p04", "type": "overlap", "context": "李兴华(书记)与景国诚(纪委书记): 上下级关系", "overlap_org": "中共张掖市委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p05", "type": "overlap", "context": "李兴华(书记)与张永刚(常务副市长): 上下级关系", "overlap_org": "中共张掖市委员会/张掖市人民政府", "overlap_period": "2024?至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p05", "type": "overlap", "context": "叶尔波力·孜汗(市长)与张永刚(常务副市长): 正副手关系", "overlap_org": "张掖市人民政府", "overlap_period": "2024?至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p03", "type": "overlap", "context": "叶尔波力·孜汗(市长)与李泽文(副书记): 同为市委副书记", "overlap_org": "中共张掖市委员会", "overlap_period": "2025?至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p05", "person_b": "p07", "type": "overlap", "context": "张永刚(前陇南组织部长)与李毓刚(现张掖组织部长): 同为组织系统干部", "overlap_org": "组织系统", "overlap_period": "", "strength": "medium", "confidence": "plausible"},
    # 前任-现任关系
    {"person_a": "p01", "person_b": "p17", "type": "predecessor_successor", "context": "李兴华接替卢小亨任张掖市委书记", "overlap_org": "中共张掖市委员会", "overlap_period": "2024/2025", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p18", "type": "predecessor_successor", "context": "叶尔波力·孜汗接替赵立香任张掖市市长", "overlap_org": "张掖市人民政府", "overlap_period": "2024", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p17", "person_b": "p19", "type": "predecessor_successor", "context": "卢小亨接替杨维俊任张掖市委书记", "overlap_org": "中共张掖市委员会", "overlap_period": "2021-07", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p18", "person_b": "p20", "type": "predecessor_successor", "context": "赵立香接替谢又生任张掖市市长", "overlap_org": "张掖市人民政府", "overlap_period": "2021-08", "strength": "strong", "confidence": "confirmed"},
    # 前任之间的工作关系
    {"person_a": "p17", "person_b": "p18", "type": "overlap", "context": "卢小亨(书记)与赵立香(市长): 原党政一把手配合作", "overlap_org": "中共张掖市委员会/张掖市人民政府", "overlap_period": "2021-2024", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p19", "person_b": "p20", "type": "overlap", "context": "杨维俊(书记)与谢又生(市长): 原党政一把手配合作", "overlap_org": "中共张掖市委员会/张掖市人民政府", "overlap_period": "2018-2021", "strength": "strong", "confidence": "confirmed"},
    # 跨市交流关系 (模式: 陇东→陇西)
    {"person_a": "p17", "person_b": "p19", "type": "same_system", "context": "卢小亨与杨维俊先后从陇东地级市长调任张掖市委书记, 体现东西干部交流模式", "overlap_org": "甘肃省干部交流体系", "overlap_period": "", "strength": "medium", "confidence": "plausible"},
    # 省直—地方旋转门
    {"person_a": "p20", "person_b": "p17", "type": "same_system", "context": "谢又生(省司法厅)→卢小亨(省交通厅): 张掖主要领导离任后均任省直部门正职", "overlap_org": "甘肃省政府系统", "overlap_period": "", "strength": "medium", "confidence": "plausible"},
]

# ── 辅助函数 ──────────────────────────────────────────

def esc(s):
    """XML转义"""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """按角色返回RGB颜色"""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title:
        return "255,50,50"   # 红色 — 党委正职
    if "市长" in title or ("副市长" in title and "常委" not in title):
        return "50,100,255"  # 蓝色 — 政府领导
    if "纪委" in title or "监委" in title:
        return "255,165,0"   # 橙色 — 纪检
    if "副书记" in title:
        return "200,50,50"   # 暗红 — 副职
    if "常委" in title:
        return "200,100,100" # 粉红 — 其他常委
    if "副市长" in title:
        return "100,100,200" # 浅蓝 — 副市长
    return "100,100,100"     # 灰色 — 其他

def person_size(p):
    """按角色返回节点大小"""
    title = p["current_post"]
    if "市委书记" in title and "纪委" not in title:
        return "20.0"
    if "市长" in title and ("副书记" in title or "党组书记" in title):
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副市长" in title:
        return "12.0"
    return "10.0"

def org_color(o):
    """按类型返回组织颜色"""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "事业单位": "220,220,220",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")

# ── 构建数据库 ────────────────────────────────────────

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    c.execute("DELETE FROM persons")
    c.execute("DELETE FROM organizations")
    c.execute("DELETE FROM positions")
    c.execute("DELETE FROM relationships")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            p["id"], p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], p["native_place"], p["education"],
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
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (
            r["person_a"], r["person_b"], r["type"], r["context"],
            r["overlap_org"], r["overlap_period"]
        ))

    conn.commit()
    conn.close()

# ── 构建 GEXF ─────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>张掖市领导班子工作关系网络 - 数据来源: 张掖市人民政府官网及公开报道</description>')
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
        lines.append('          <attvalue for="3" value="张掖市"/>')
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
        lines.append('          <attvalue for="3" value="张掖市"/>')
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
        conf = r.get("confidence", "plausible")
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

# ── 主函数 ──────────────────────────────────────────

def main():
    print(f"=== 张掖市网络数据构建 ===")
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
