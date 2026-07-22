#!/usr/bin/env python3
"""
酒泉市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

数据来源:
- 酒泉市人民政府官方网站及相关报道, 2026年7月确认
- 百度百科 (王立奇、贾志升)
- 维基百科 (酒泉市、中国共产党酒泉市委员会)
- 任前公示 (甘肃组工网)
- 新闻报道 (中国经济网, 澎湃新闻, 中国甘肃网, 每日甘肃网等)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── 路径 ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING_DIR = SCRIPT_DIR
DB_PATH = os.path.join(STAGING_DIR, "酒泉市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "酒泉市_network.gexf")

# ── 数据 ──────────────────────────────────────────────

# 1. 人员
persons = [
    # (id, name, gender, ethnicity, birth, birthplace, native_place, education, party_join, work_start, current_post, current_org, source, person_id_unique)
    # ── 当前主要领导人 ──
    {
        "id": "p01",
        "name": "王立奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年12月",
        "birthplace": "辽宁北票",
        "native_place": "辽宁北票",
        "education": "研究生/工学硕士(清华大学管理科学与工程专业)",
        "party_join": "中共党员",
        "work_start": "2003年9月",
        "current_post": "酒泉市委书记",
        "current_org": "中共酒泉市委员会",
        "source": "百度百科, 维基百科, 人民网, 每日甘肃网2026-03",
        "person_id": "jiuquan_wang_liqi"
    },
    {
        "id": "p02",
        "name": "贾志升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年7月",
        "birthplace": "甘肃镇原",
        "native_place": "甘肃镇原",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "1996年11月",
        "current_post": "酒泉市委副书记、市政府党组书记、市长",
        "current_org": "酒泉市人民政府",
        "source": "百度百科, 澎湃新闻, 中国经济网, 中国甘肃网",
        "person_id": "jiuquan_jia_zhisheng"
    },
    # ── 市委常委 ──
    {
        "id": "p03",
        "name": "赵峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "酒泉市委常委、市政府党组副书记、常务副市长",
        "current_org": "酒泉市人民政府",
        "source": "酒泉市领导班子公开信息, 2025年酒泉市人大会议报道",
        "person_id": "jiuquan_zhao_feng"
    },
    {
        "id": "p04",
        "name": "崔福祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年5月",
        "birthplace": "甘肃泾川",
        "native_place": "甘肃泾川",
        "education": "省委党校研究生/文学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "酒泉市人大常委会主任",
        "current_org": "酒泉市人民代表大会常务委员会",
        "source": "中国经济网2026-01, 人民网, 酒泉市第五届人大第六次会议",
        "person_id": "jiuquan_cui_fuxiang"
    },
    {
        "id": "p05",
        "name": "王海明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年5月",
        "birthplace": "山西中阳",
        "native_place": "山西中阳",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "1988年7月",
        "current_post": "酒泉市政协党组书记、主席",
        "current_org": "中国人民政治协商会议酒泉市委员会",
        "source": "澎湃新闻2022-12, 百度百科, 中国甘肃网",
        "person_id": "jiuquan_wang_haiming"
    },
    {
        "id": "p06",
        "name": "义战鹰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学/公共管理硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "酒泉市委常委、宣传部部长",
        "current_org": "中共酒泉市委员会宣传部",
        "source": "酒泉市第五届委员会常委名单, 中国经济网2021-12",
        "person_id": "jiuquan_yi_zhanying"
    },
    {
        "id": "p07",
        "name": "徐志强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学/法律硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "酒泉市委常委、政法委书记",
        "current_org": "中共酒泉市委员会政法委员会",
        "source": "酒泉市第五届委员会常委名单, 中国经济网2021-12",
        "person_id": "jiuquan_xu_zhiqiang"
    },
    {
        "id": "p08",
        "name": "何正军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生/文学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "酒泉市人大常委会副主任",
        "current_org": "酒泉市人民代表大会常务委员会",
        "source": "酒泉市第五届委员会常委名单, 中国经济网, 中国甘肃网2026-01",
        "person_id": "jiuquan_he_zhengjun"
    },
    {
        "id": "p09",
        "name": "李生潜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "酒泉市委常委、市政府党组成员、肃州区委书记",
        "current_org": "中共肃州区委员会",
        "source": "酒泉市领导班子公开信息, 酒泉市委组织部任前公示",
        "person_id": "jiuquan_li_shengqian"
    },
    {
        "id": "p10",
        "name": "石峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "酒泉市委常委、市政府党组成员、副市长",
        "current_org": "酒泉市人民政府",
        "source": "酒泉市人民政府官网, 中国经济网",
        "person_id": "jiuquan_shi_feng"
    },
    # ── 其他市政府领导 ──
    {
        "id": "p11",
        "name": "庞柒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "酒泉市委常委、副市长(挂职)",
        "current_org": "酒泉市人民政府",
        "source": "酒泉市人民政府官网, 中国经济网2022-07",
        "person_id": "jiuquan_pang_qi"
    },
    {
        "id": "p12",
        "name": "张跃峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "酒泉市人民政府副市长",
        "current_org": "酒泉市人民政府",
        "source": "中国甘肃网, 酒泉市人大常委会2025-12",
        "person_id": "jiuquan_zhang_yuefeng"
    },
    {
        "id": "p13",
        "name": "陶涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学/农业推广硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "酒泉市人民政府副市长",
        "current_org": "酒泉市人民政府",
        "source": "中国经济网2026-01, 酒泉市第五届人大第六次会议",
        "person_id": "jiuquan_tao_tao"
    },
    {
        "id": "p14",
        "name": "王立扬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "酒泉市人民政府副市长",
        "current_org": "酒泉市人民政府",
        "source": "中国甘肃网2026-06-30, 酒泉市人大常委会",
        "person_id": "jiuquan_wang_liyang"
    },
    {
        "id": "p15",
        "name": "张力",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学/农业推广硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "酒泉市监察委员会主任",
        "current_org": "酒泉市监察委员会",
        "source": "中国经济网2026-01, 酒泉市第五届人大第六次会议",
        "person_id": "jiuquan_zhang_li"
    },
    # ── 前任主要领导 ──
    {
        "id": "p16",
        "name": "唐培宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年3月",
        "birthplace": "甘肃民勤",
        "native_place": "甘肃民勤",
        "education": "大学/公共管理硕士(兰州大学)",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平凉市委书记",
        "current_org": "中共平凉市委员会",
        "source": "甘肃组工网, 澎湃新闻, 中国经济网, 新京报",
        "person_id": "jiuquan_tang_peihong"
    },
    {
        "id": "p17",
        "name": "吴仰东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "另有任用(原酒泉市委书记)",
        "current_org": "待查",
        "source": "新京报, 维基百科, 西部门户网",
        "person_id": "jiuquan_wu_yangdong"
    },
    {
        "id": "p18",
        "name": "张安疆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原酒泉市市长",
        "current_org": "待查",
        "source": "维基百科",
        "person_id": "jiuquan_zhang_anjiang"
    },
    # ── 县区主要领导（下辖县市区委书记） ──
    {
        "id": "p19",
        "name": "石琳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生/工商管理硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "酒泉市委常委、敦煌市委书记",
        "current_org": "中共敦煌市委员会",
        "source": "酒泉市第五届委员会常委名单, 中国经济网2021-12",
        "person_id": "jiuquan_shi_lin"
    },
]

# 2. 组织机构
organizations = [
    {"id": "o01", "name": "中共酒泉市委员会", "type": "党委", "level": "地级", "parent": "中共甘肃省委员会", "location": "甘肃省酒泉市"},
    {"id": "o02", "name": "酒泉市人民政府", "type": "政府", "level": "地级", "parent": "甘肃省人民政府", "location": "甘肃省酒泉市"},
    {"id": "o03", "name": "酒泉市人民代表大会常务委员会", "type": "人大", "level": "地级", "parent": "酒泉市", "location": "甘肃省酒泉市"},
    {"id": "o04", "name": "中国人民政治协商会议酒泉市委员会", "type": "政协", "level": "地级", "parent": "酒泉市", "location": "甘肃省酒泉市"},
    {"id": "o05", "name": "中共酒泉市委员会宣传部", "type": "党委", "level": "地级", "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市"},
    {"id": "o06", "name": "中共酒泉市委员会政法委员会", "type": "党委", "level": "地级", "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市"},
    {"id": "o07", "name": "中共肃州区委员会", "type": "党委", "level": "县处级", "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市肃州区"},
    {"id": "o08", "name": "中共敦煌市委员会", "type": "党委", "level": "县处级", "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市敦煌市"},
    {"id": "o09", "name": "酒泉市监察委员会", "type": "党委", "level": "地级", "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市"},
    {"id": "o10", "name": "中共平凉市委员会", "type": "党委", "level": "地级", "parent": "中共甘肃省委员会", "location": "甘肃省平凉市"},
    {"id": "o11", "name": "甘肃省交通运输厅", "type": "政府", "level": "省级", "parent": "甘肃省人民政府", "location": "甘肃省兰州市"},
    {"id": "o12", "name": "庆阳市人民政府", "type": "政府", "level": "地级", "parent": "甘肃省人民政府", "location": "甘肃省庆阳市"},
    {"id": "o13", "name": "白银市人民政府", "type": "政府", "level": "地级", "parent": "甘肃省人民政府", "location": "甘肃省白银市"},
    {"id": "o14", "name": "中共白银市委政法委员会", "type": "党委", "level": "地级", "parent": "中共白银市委员会", "location": "甘肃省白银市"},
    {"id": "o15", "name": "张掖市人民政府", "type": "政府", "level": "地级", "parent": "甘肃省人民政府", "location": "甘肃省张掖市"},
    {"id": "o16", "name": "中共张掖市委员会组织部", "type": "党委", "level": "地级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市"},
    {"id": "o17", "name": "甘肃省委组织部", "type": "党委", "level": "省级", "parent": "中共甘肃省委员会", "location": "甘肃省兰州市"},
    {"id": "o18", "name": "中共酒泉市委员会组织部", "type": "党委", "level": "地级", "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市"},
    {"id": "o19", "name": "酒泉军分区", "type": "事业单位", "level": "地级", "parent": "甘肃省军区", "location": "甘肃省酒泉市"},
]

# 3. 任职
positions = [
    # 王立奇 (p01)
    {"person_id": "p01", "org_id": "o01", "title": "酒泉市委书记", "start": "2021-07", "end": "至今", "rank": "正厅级", "note": "主持市委全面工作"},
    {"person_id": "p01", "org_id": "o02", "title": "酒泉市人民政府市长(前任)", "start": "2020-01", "end": "2021-07", "rank": "正厅级", "note": "曾任市长"},
    {"person_id": "p01", "org_id": "o01", "title": "酒泉市委副书记", "start": "2019-12", "end": "2021-07", "rank": "副厅级", "note": "赴酒泉任职起始岗位"},
    # 贾志升 (p02)
    {"person_id": "p02", "org_id": "o01", "title": "酒泉市委副书记", "start": "2025-09", "end": "至今", "rank": "副厅级", "note": "兼任市长"},
    {"person_id": "p02", "org_id": "o02", "title": "酒泉市人民政府市长", "start": "2025-10", "end": "至今", "rank": "正厅级", "note": "2025年10月当选"},
    {"person_id": "p02", "org_id": "o14", "title": "白银市委常委、政法委书记", "start": "2023-09", "end": "2025-09", "rank": "副厅级", "note": "前职"},
    {"person_id": "p02", "org_id": "o13", "title": "白银市人民政府副市长", "start": "2021-09", "end": "2023-09", "rank": "副厅级", "note": "前职"},
    {"person_id": "p02", "org_id": "o12", "title": "庆阳市农业农村局局长", "start": "2019-02", "end": "2020-04", "rank": "正处级", "note": "前职"},
    {"person_id": "p02", "org_id": "o12", "title": "正宁县委书记", "start": "2020-04", "end": "2021-08", "rank": "正处级", "note": "前职"},
    # 赵峰 (p03)
    {"person_id": "p03", "org_id": "o02", "title": "酒泉市委常委、常务副市长", "start": "?", "end": "至今", "rank": "副厅级", "note": "负责市政府常务工作"},
    # 崔福祥 (p04)
    {"person_id": "p04", "org_id": "o03", "title": "酒泉市人大常委会主任", "start": "2026-01", "end": "至今", "rank": "正厅级", "note": ""},
    {"person_id": "p04", "org_id": "o01", "title": "酒泉市委常委、市纪委书记、市监委主任(前任)", "start": "2021-12?", "end": "2026-01", "rank": "副厅级", "note": "前职"},
    # 王海明 (p05)
    {"person_id": "p05", "org_id": "o04", "title": "酒泉市政协主席", "start": "2022-12", "end": "至今", "rank": "正厅级", "note": ""},
    # 义战鹰 (p06)
    {"person_id": "p06", "org_id": "o05", "title": "酒泉市委宣传部部长", "start": "2021-12?", "end": "至今", "rank": "副厅级", "note": ""},
    # 徐志强 (p07)
    {"person_id": "p07", "org_id": "o06", "title": "酒泉市委政法委书记", "start": "2021-12?", "end": "至今", "rank": "副厅级", "note": ""},
    # 何正军 (p08)
    {"person_id": "p08", "org_id": "o03", "title": "酒泉市人大常委会副主任", "start": "2025-10", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p08", "org_id": "o01", "title": "酒泉市委常委、肃州区委书记(前任)", "start": "2021-12?", "end": "2025-10", "rank": "副厅级", "note": "前职"},
    # 李生潜 (p09)
    {"person_id": "p09", "org_id": "o07", "title": "肃州区委书记", "start": "?", "end": "至今", "rank": "副厅级", "note": "兼任市委常委"},
    # 石峰 (p10)
    {"person_id": "p10", "org_id": "o02", "title": "酒泉市副市长", "start": "2022-11?", "end": "至今", "rank": "副厅级", "note": "兼任市委常委"},
    # 庞柒 (p11)
    {"person_id": "p11", "org_id": "o02", "title": "酒泉市副市长(挂职)", "start": "2022-07", "end": "至今", "rank": "副厅级", "note": "挂职"},
    # 张跃峰 (p12)
    {"person_id": "p12", "org_id": "o02", "title": "酒泉市副市长", "start": "2025-12", "end": "至今", "rank": "副厅级", "note": ""},
    # 陶涛 (p13)
    {"person_id": "p13", "org_id": "o02", "title": "酒泉市副市长", "start": "2026-01", "end": "至今", "rank": "副厅级", "note": "原阿克塞县委书记"},
    # 王立扬 (p14)
    {"person_id": "p14", "org_id": "o02", "title": "酒泉市副市长", "start": "2026-06", "end": "至今", "rank": "副厅级", "note": ""},
    # 张力 (p15)
    {"person_id": "p15", "org_id": "o09", "title": "酒泉市监察委员会主任", "start": "2026-01", "end": "至今", "rank": "副厅级", "note": "原张掖市副市长"},
    # 唐培宏 (p16)
    {"person_id": "p16", "org_id": "o10", "title": "平凉市委书记", "start": "2025-09", "end": "至今", "rank": "正厅级", "note": ""},
    {"person_id": "p16", "org_id": "o02", "title": "酒泉市人民政府市长(前任)", "start": "2021-12", "end": "2025-09", "rank": "正厅级", "note": "前任市长"},
    {"person_id": "p16", "org_id": "o01", "title": "酒泉市委副书记", "start": "2018-08", "end": "2025-09", "rank": "副厅级", "note": "原副书记"},
    {"person_id": "p16", "org_id": "o16", "title": "张掖市委常委、组织部部长", "start": "2014", "end": "2018-08", "rank": "副厅级", "note": "前职"},
    {"person_id": "p16", "org_id": "o17", "title": "甘肃省委组织部办公室主任", "start": "?", "end": "2014", "rank": "正处级", "note": "前职"},
    # 吴仰东 (p17)
    {"person_id": "p17", "org_id": "o01", "title": "酒泉市委书记(前任)", "start": "2018-01", "end": "2021-07", "rank": "正厅级", "note": "前任"},
    # 张安疆 (p18)
    {"person_id": "p18", "org_id": "o02", "title": "酒泉市人民政府市长(前任)", "start": "2018-01", "end": "2019-12", "rank": "正厅级", "note": "前任"},
    # 石琳 (p19)
    {"person_id": "p19", "org_id": "o08", "title": "敦煌市委书记", "start": "?", "end": "至今", "rank": "副厅级", "note": "兼任市委常委"},
]

# 4. 关系
relationships = [
    # 现任班子内部关系
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "王立奇(书记)与贾志升(市长): 党政一把手配合", "overlap_org": "中共酒泉市委员会/酒泉市人民政府", "overlap_period": "2025-09至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p03", "type": "overlap", "context": "王立奇(书记)与赵峰(常务副市长): 上下级关系", "overlap_org": "中共酒泉市委员会/酒泉市人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p03", "type": "overlap", "context": "贾志升(市长)与赵峰(常务副市长): 正副手关系", "overlap_org": "酒泉市人民政府", "overlap_period": "2025-09至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p06", "type": "overlap", "context": "王立奇(书记)与义战鹰(宣传部长): 上下级关系", "overlap_org": "中共酒泉市委员会", "overlap_period": "2021至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p07", "type": "overlap", "context": "王立奇(书记)与徐志强(政法委书记): 上下级关系", "overlap_org": "中共酒泉市委员会", "overlap_period": "2021至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p19", "type": "overlap", "context": "王立奇(书记)与石琳(敦煌市委书记): 上下级关系", "overlap_org": "中共酒泉市委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 前任-现任关系
    {"person_a": "p01", "person_b": "p17", "type": "predecessor_successor", "context": "王立奇接替吴仰东任酒泉市委书记", "overlap_org": "中共酒泉市委员会", "overlap_period": "2021-07", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p16", "type": "predecessor_successor", "context": "贾志升接替唐培宏任酒泉市市长", "overlap_org": "酒泉市人民政府", "overlap_period": "2025-09/10", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p16", "person_b": "p18", "type": "predecessor_successor", "context": "唐培宏接替张安疆任酒泉市市长", "overlap_org": "酒泉市人民政府", "overlap_period": "2019-12/2021-12", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p18", "type": "predecessor_successor", "context": "王立奇接替张安疆任酒泉市市长", "overlap_org": "酒泉市人民政府", "overlap_period": "2019-12/2020-01", "strength": "strong", "confidence": "confirmed"},
    # 前任之间的工作关系
    {"person_a": "p17", "person_b": "p18", "type": "overlap", "context": "吴仰东(书记)与张安疆(市长): 原党政一把手配合", "overlap_org": "中共酒泉市委员会/酒泉市人民政府", "overlap_period": "2018-2019", "strength": "strong", "confidence": "confirmed"},
    # 跨市交流关系
    {"person_a": "p16", "person_b": "p02", "type": "same_system", "context": "唐培宏(平凉书记)与贾志升(酒泉市长): 白银-酒泉-平凉干部流动线", "overlap_org": "甘肃省干部交流体系", "overlap_period": "", "strength": "medium", "confidence": "plausible"},
    {"person_a": "p16", "person_b": "p17", "type": "same_system", "context": "唐培宏任平凉市委书记, 吴仰东曾任酒泉市委书记: 酒泉-平凉干部轮换", "overlap_org": "甘肃省干部交流体系", "overlap_period": "", "strength": "medium", "confidence": "plausible"},
    # 贾志升跨市职业生涯
    {"person_a": "p02", "person_b": "p16", "type": "same_system", "context": "贾志升从白银到酒泉任市长, 唐培宏从酒泉到平凉任书记: 交叉调动", "overlap_org": "甘肃省干部交流体系", "overlap_period": "2025", "strength": "medium", "confidence": "plausible"},
    # 人大/政协团队
    {"person_a": "p04", "person_b": "p08", "type": "overlap", "context": "崔福祥(人大主任)与何正军(人大副主任): 人大班子配合", "overlap_org": "酒泉市人大常委会", "overlap_period": "2026-01至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p04", "type": "overlap", "context": "王立奇(书记)与崔福祥(原纪委书记、现人大主任): 长期配合", "overlap_org": "中共酒泉市委员会", "overlap_period": "2021-2026", "strength": "strong", "confidence": "confirmed"},
    # 新调任副市长
    {"person_a": "p15", "person_b": "p02", "type": "overlap", "context": "张力(监委主任)与贾志升(市长): 新任监察-政府配合作", "overlap_org": "酒泉市", "overlap_period": "2026-01至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p13", "person_b": "p12", "type": "overlap", "context": "陶涛(副市长)与张跃峰(副市长): 同期新任副市长", "overlap_org": "酒泉市人民政府", "overlap_period": "2025-12/2026-01", "strength": "medium", "confidence": "confirmed"},
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
    if "书记" in title and "纪委" not in title and "统战" not in title and "人大" not in title:
        return "255,50,50"   # 红色 — 党委正职
    if "市长" in title and ("副书记" in title or "党组书记" in title):
        return "50,100,255"  # 蓝色 — 政府正职
    if "市长" in title or ("副市长" in title and "常委" not in title):
        return "50,100,255"  # 蓝色 — 政府正职/副职
    if "纪委" in title or "监委" in title or "监察" in title:
        return "255,165,0"   # 橙色 — 纪检
    if "副书记" in title:
        return "200,50,50"   # 暗红 — 副书记
    if "常委" in title:
        return "200,100,100" # 粉红 — 其他常委
    if "副市长" in title or "副市长" in title:
        return "100,100,200" # 浅蓝 — 副市长
    if "人大" in title:
        return "200,255,255" # 青色 — 人大
    if "政协" in title:
        return "255,240,200" # 奶油色 — 政协
    return "100,100,100"     # 灰色 — 其他

def person_size(p):
    """按角色返回节点大小"""
    title = p["current_post"]
    if "市委书记" in title or "人大主任" in title or "政协主席" in title:
        return "20.0"
    if "市长" in title and ("副书记" in title or "党组书记" in title):
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副市长" in title:
        return "12.0"
    if "人大" in title or "政协" in title:
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
    lines.append('    <description>酒泉市领导班子工作关系网络 - 数据来源: 酒泉市人民政府官网及公开报道</description>')
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
        lines.append('          <attvalue for="3" value="酒泉市"/>')
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
        lines.append('          <attvalue for="3" value="酒泉市"/>')
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
    print(f"=== 酒泉市网络数据构建 ===")
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
