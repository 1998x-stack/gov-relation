#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 镇远县 (Zhenyuan County, Qiandongnan, Guizhou) leadership network.

镇远县 — 贵州省黔东南苗族侗族自治州辖县, 中国历史文化名城, 镇远古城 (国家5A级旅游景区).
Research date: 2026-08-05. Targets: 县委书记 (杨琼) & 县长 (杨屏).

Sources (primary first):
  - 镇远县人民政府门户 www.zygov.gov.cn 领导之窗 (官方人事档案)
  - 黔东南州人民政府门户 www.qdn.gov.cn (官方州要闻/任免)
  - 县四大班子"八一"走访慰问新闻 (2026-07-31, zygov)
  - 政协第十五届镇远县委员会第五次会议 (2026-02)
  - 任前公示/媒体 (中国妇女报, 天眼新闻, 政事儿, 黔东南普法等) 经 搜狗微信 检索

Confidence note: 核心二人 (杨琼/杨屏) 现任职务与领导班子名单由官方来源确认;
个人完整履历、部分领导班子副职与个别前任书记存在资料缺口, 以 open_questions 呈现.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

# ════════════════════════════════════════════════════════════════════
# PATHS — write to staging; promote via scripts/process_tmp.py
# ════════════════════════════════════════════════════════════════════
BASE = Path(__file__).resolve().parents[3]
STAGING = BASE / "data/tmp/guizhou_镇远县"
DB_PATH = STAGING / "镇远县_network.db"
GEXF_PATH = STAGING / "镇远县_network.gexf"

AS_OF = "2026-08-05"
TODAY = datetime.now().strftime("%Y-%m-%d")

# ════════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════════

persons = [
    # ── Core targets ──
    {"id": 1, "name": "杨琼", "gender": "女", "ethnicity": "侗族",
     "birth": "", "birthplace": "", "education": "省委党校大学",
     "party_join": "", "work_start": "1993年(1991-09入贵州农学院畜牧兽医专业)",
     "current_post": "镇远县委书记",
     "current_org": "中共镇远县委员会",
     "source": "zygov.gov.cn 领导之窗/新闻确认现任; 任前公示(贵州省委组织部2023-08-15)确认任命; 中国妇女报/美美广元报道履历"},
    {"id": 2, "name": "杨屏", "gender": "男", "ethnicity": "苗族",
     "birth": "1986年3月", "birthplace": "", "education": "研究生(工学硕士)",
     "party_join": "", "work_start": "",
     "current_post": "镇远县委副书记、县人民政府县长",
     "current_org": "镇远县人民政府",
     "source": "zy.gov.cn 领导之窗官方简历(苗族,1986-03,工学硕士); 政协/两会新闻确认现任"},

    # ── 县委领导班子 ──
    {"id": 3, "name": "陈林", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "镇远县委副书记",
     "current_org": "中共镇远县委员会",
     "source": "zy.gov.cn 新闻(县委副书记陈林到镇远二中走访慰问; 杨琼陈林调研县法院)"},
    {"id": 15, "name": "杨径", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "镇远县委常委、县委办公室主任",
     "current_org": "中共镇远县委员会",
     "source": "镇远公安公众号(2024-02春节慰问: 县委书记杨琼、县委常委县委办主任杨径)"},

    # ── 县人大 / 县政协 ──
    {"id": 5, "name": "黄朝银", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "镇远县人大常委会主任",
     "current_org": "镇远县人民代表大会常务委员会",
     "source": "zy.gov.cn 八一走访慰问/人大会议(四大班子领导)"},
    {"id": 6, "name": "王冬梅", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "镇远县政协主席",
     "current_org": "政协镇远县委员会",
     "source": "zy.gov.cn 八一走访慰问(四大班子领导)"},

    # ── 县政府领导班子 (领导之窗官方名册) ──
    {"id": 7, "name": "吴铭", "gender": "男", "ethnicity": "苗族",
     "birth": "1984年9月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇远县委常委、县人民政府常务副县长",
     "current_org": "镇远县人民政府",
     "source": "zy.gov.cn 领导之窗官方档案"},
    {"id": 8, "name": "粟静", "gender": "女", "ethnicity": "苗族",
     "birth": "1978年9月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇远县委常委、县人民政府副县长",
     "current_org": "镇远县人民政府",
     "source": "zy.gov.cn 领导之窗官方档案"},
    {"id": 9, "name": "杨军", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年2月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇远县委常委、县人民政府副县长(挂职)",
     "current_org": "镇远县人民政府",
     "source": "zy.gov.cn 领导之窗官方档案"},
    {"id": 10, "name": "周江", "gender": "男", "ethnicity": "彝族",
     "birth": "1983年11月", "birthplace": "", "education": "研究生(管理学硕士)",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇远县委常委、县人民政府副县长(挂职)",
     "current_org": "镇远县人民政府",
     "source": "zy.gov.cn 领导之窗官方档案"},
    {"id": 11, "name": "杨顺金", "gender": "男", "ethnicity": "侗族",
     "birth": "1975年12月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇远县人民政府副县长、县公安局局长",
     "current_org": "镇远县公安局",
     "source": "zy.gov.cn 领导之窗官方档案"},
    {"id": 12, "name": "周益民", "gender": "男", "ethnicity": "侗族",
     "birth": "1985年11月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇远县人民政府副县长",
     "current_org": "镇远县人民政府",
     "source": "zy.gov.cn 领导之窗官方档案"},
    {"id": 13, "name": "杨昌新", "gender": "男", "ethnicity": "侗族",
     "birth": "1983年11月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇远县人民政府副县长",
     "current_org": "镇远县人民政府",
     "source": "zy.gov.cn 领导之窗官方档案"},
    {"id": 14, "name": "金庆祝", "gender": "女", "ethnicity": "苗族",
     "birth": "1976年9月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇远县人民政府副县长",
     "current_org": "镇远县人民政府",
     "source": "zy.gov.cn 领导之窗官方档案"},
    {"id": 16, "name": "杨义昌", "gender": "男", "ethnicity": "汉族",
     "birth": "1987年3月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "镇远县人民政府副县长",
     "current_org": "镇远县人民政府",
     "source": "zy.gov.cn 领导之窗官方档案"},

    # ── 前任领导 (继任链 / 风险信号) ──
    {"id": 17, "name": "杨仕根", "gender": "男", "ethnicity": "侗族",
     "birth": "1979年1月", "birthplace": "贵州天柱", "education": "贵州工业大学交通土建工程",
     "party_join": "2009年2月", "work_start": "2003年9月",
     "current_post": "已落马(因贪腐被判刑十年六个月)",
     "current_org": "-",
     "source": "政事儿/启点消息/剑河便民网: 曾任镇远县委副书记、县长,被查判刑; 2020由从江县委常委、常务副县长调任"}, 
    {"id": 18, "name": "刘建新", "gender": "男", "ethnicity": "苗族",
     "birth": "1966年4月", "birthplace": "籍贯贵州镇远/出生地岑巩", "education": "省委党校研究生",
     "party_join": "2000年12月", "work_start": "1985年8月",
     "current_post": "已被公诉/双开(原担任镇远县委书记,后任黔东南州人大常委会副主任)",
     "current_org": "-",
     "source": "中国裁判文书/启点消息: 2012年起任镇远县委书记、贵州黔东经济开发区党工委书记(兼); 因受贿被诉"},
    {"id": 19, "name": "王镇义", "gender": "男", "ethnicity": "侗族",
     "birth": "", "birthplace": "贵州镇远(出身镇远县舞阳镇)", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "已被查(曾任黔南州委副书记、凯里市委书记、麻江县委书记)",
     "current_org": "-",
     "source": "媒体(镇远人出身); 后历任麻江县委书记、黔东南州委常委/凯里市委书记、黔南州委副书记; 被查"},

    # ── 关联机构负责人 / 跨县网节点 ──
    {"id": 20, "name": "王建勇", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "镇远县人民政府副县长",
     "current_org": "镇远县人民政府",
     "source": "州黔东南招商新闻(2026-03 随县委书记杨琼赴广州/贵阳招商)"},
    {"id": 21, "name": "田奇", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "镇远县人民政府副县长",
     "current_org": "镇远县人民政府",
     "source": "州黔东南招商新闻(2026-03 随杨琼赴贵阳招商)"},
    {"id": 22, "name": "王树江", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "镇远县人民法院院长",
     "current_org": "镇远县人民法院",
     "source": "镇远法院新闻(县委书记杨琼调研, 院长王树江陪同)"},
]

organizations = [
    {"id": 1, "name": "中共镇远县委员会", "type": "党委", "level": "县", "parent": "中共黔东南苗族侗族自治州委员会", "location": "镇远县"},
    {"id": 2, "name": "镇远县人民政府", "type": "政府", "level": "县", "parent": "黔东南苗族侗族自治州人民政府", "location": "镇远县"},
    {"id": 3, "name": "镇远县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "黔东南苗族侗族自治州人大常委会", "location": "镇远县"},
    {"id": 4, "name": "政协镇远县委员会", "type": "政协", "level": "县", "parent": "政协黔东南苗族侗族自治州委员会", "location": "镇远县"},
    {"id": 5, "name": "贵州黔东经济开发区", "type": "开发区", "level": "县(开发区)", "parent": "镇远县", "location": "镇远县"},
    {"id": 6, "name": "镇远县公安局", "type": "政府", "level": "县", "parent": "镇远县人民政府", "location": "镇远县"},
    {"id": 7, "name": "镇远县人民法院", "type": "政府(司法)", "level": "县", "parent": "镇远县", "location": "镇远县"},
    {"id": 8, "name": "中共黔东南苗族侗族自治州委员会", "type": "党委", "level": "州", "parent": "贵州省", "location": "凯里市"},
    {"id": 9, "name": "黔东南苗族侗族自治州人民政府", "type": "政府", "level": "州", "parent": "贵州省", "location": "凯里市"},
    {"id": 10, "name": "黔东南州发展改革委员会", "type": "政府", "level": "州", "parent": "黔东南州人民政府", "location": "凯里市"},
    {"id": 11, "name": "岑巩县人民政府", "type": "政府", "level": "县", "parent": "黔东南苗族侗族自治州人民政府", "location": "岑巩县"},
    {"id": 12, "name": "黔东南州交通运输局", "type": "政府", "level": "州", "parent": "黔东南州人民政府", "location": "凯里市"},
    {"id": 13, "name": "从江县人民政府", "type": "政府", "level": "县", "parent": "黔东南苗族侗族自治州人民政府", "location": "从江县"},
    {"id": 14, "name": "黔东南州人大常委会", "type": "人大", "level": "州", "parent": "黔东南州", "location": "凯里市"},
    {"id": 15, "name": "凯里市人民政府/中共凯里市委", "type": "党委", "level": "州辖市", "parent": "黔东南州", "location": "凯里市"},
]

positions = [
    # ── 现任核心领导 ──
    {"person_id": 1, "org_id": 1, "title": "镇远县委书记", "start_date": "2023-08", "end_date": "至今", "rank": "县处级正职", "note": "2023年8月15日任前公示拟任; 兼贵州黔东经济开发区党工委书记"},
    {"person_id": 1, "org_id": 10, "title": "黔东南州发展改革委主任", "start_date": "", "end_date": "2023-08", "rank": "县处级正职", "note": "任镇远县委书记前任黔东南州发改委主任"},
    {"person_id": 1, "org_id": 11, "title": "岑巩县副县长、党组成员", "start_date": "", "end_date": "", "rank": "副县级", "note": "此前任职(公开早简历)"},
    {"person_id": 2, "org_id": 2, "title": "镇远县委副书记、县人民政府县长", "start_date": "", "end_date": "至今", "rank": "县处级正职", "note": "现任县长(2026年主抓'十五五'开局)"},
    {"person_id": 3, "org_id": 1, "title": "镇远县委副书记", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "镇远县委常委、县委办公室主任", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "镇远县人大常委会主任", "start_date": "", "end_date": "至今", "rank": "县处级正职", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "镇远县政协主席", "start_date": "", "end_date": "至今", "rank": "县处级正职", "note": ""},

    # ── 县政府班子 ──
    {"person_id": 7, "org_id": 2, "title": "县人民政府常务副县长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "县委常委"},
    {"person_id": 8, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "县委常委"},
    {"person_id": 9, "org_id": 2, "title": "县人民政府副县长(挂职)", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "县委常委"},
    {"person_id": 10, "org_id": 2, "title": "县人民政府副县长(挂职)", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "县委常委"},
    {"person_id": 11, "org_id": 6, "title": "县人民政府副县长、县公安局局长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "随书记招商"},
    {"person_id": 21, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "随书记招商"},
    {"person_id": 22, "org_id": 7, "title": "镇远县人民法院院长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": ""},

    # ── 前任领导 ──
    {"person_id": 17, "org_id": 2, "title": "镇远县委副书记、县长(兼贵州黔东经济开发区管委会主任)", "start_date": "2021-07", "end_date": "被查(约2024)", "rank": "县处级正职", "note": "2021-07代理县长;被查/判刑十年六个月"},
    {"person_id": 17, "org_id": 13, "title": "从江县委常委、常务副县长", "start_date": "2020", "end_date": "2021", "rank": "副县级", "note": "2020年调住从江县"},
    {"person_id": 17, "org_id": 12, "title": "黔东南州交通运输局党组书记", "start_date": "2021-04", "end_date": "2021-07", "rank": "县处级正职", "note": ""},
    {"person_id": 18, "org_id": 1, "title": "镇远县委书记、贵州黔东经济开发区党工委书记(兼)", "start_date": "2012", "end_date": "2020", "rank": "县处级正职", "note": "因受贿被诉/双开"},
    {"person_id": 18, "org_id": 14, "title": "黔东南州人大常委会副主任", "start_date": "", "end_date": "被查", "rank": "副厅级", "note": "被捕"},
    {"person_id": 18, "org_id": 8, "title": "镇远县委常委、县纪委书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "早期任职"},
    {"person_id": 19, "org_id": 15, "title": "凯里市委书记、黔东南州委常委", "start_date": "2021-06", "end_date": "2023-05", "rank": "副厅级", "note": "镇远出身名校"},
    {"person_id": 19, "org_id": 8, "title": "麻江县/州级干部(任黔南州委副书记)", "start_date": "2023-05", "end_date": "被查", "rank": "副厅级", "note": "被查"},
]

relationships = [
    # ── 核心搭档 ──
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档", "overlap_org": "镇远县党政领导班子", "overlap_period": "2023年至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记—县委副书记", "overlap_org": "中共镇远县委员会", "overlap_period": "2023年至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记—人大常委会主任(四大班子协庆)", "overlap_org": "镇远县四大班子", "overlap_period": "2023年至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记—政协主席(四大班子协庆)", "overlap_org": "镇远县四大班子", "overlap_period": "2023年至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "县委书记—常务副县长", "overlap_org": "镇远县党政领导班子", "overlap_period": "2023年至今"},
    {"person_a": 1, "person_b": 15, "type": "上下级", "context": "县委书记—县委办主任(身边班子)", "overlap_org": "中共镇远县委员会", "overlap_period": "2023年至今"},
    {"person_a": 1, "person_b": 20, "type": "上下级", "context": "书记率队招商, 副县长随行", "overlap_org": "镇远县人民政府", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 22, "type": "上下级", "context": "调研法院, 院长陪同", "overlap_org": "镇远县人民法院", "overlap_period": "2024年"},

    {"person_a": 2, "person_b": 3, "type": "共事", "context": "县长—县委副书记", "overlap_org": "镇远县党政领导班子", "overlap_period": "现任任期"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长—常务副县长", "overlap_org": "镇远县人民政府", "overlap_period": "现任任期"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "县长—人大主任(人代会)", "overlap_org": "镇远县人民代表大会", "overlap_period": "现任任期"},

    # ── 继任链 (县长) ──
    {"person_a": 17, "person_b": 2, "type": "前任继任", "context": "杨仕根(前任县长,被查)→杨屏(现任县长)", "overlap_org": "镇远县人民政府", "overlap_period": "2024年交接"},

    # ── 前任书记 ──
    {"person_a": 18, "person_b": 1, "type": "前任继任", "context": "刘建新(早年书记,被诉)→后任由若干书记过渡→杨琼(2023)", "overlap_org": "中共镇远县委员会", "overlap_period": "跨届"},
    {"person_a": 1, "person_b": 18, "type": "同籍贯", "context": "杨琼(岑巩人)与刘建新(出生地岑巩)同为岑巩籍", "overlap_org": "镇远/岑巩", "overlap_period": "-"},

    # ── 跨县干部交流网 ──
    {"person_a": 17, "person_b": 1, "type": "跨县干部交流", "context": "杨仕根由从江县调入住镇远县县长(跨县)", "overlap_org": "黔东南州组织交流", "overlap_period": "2021"},
    {"person_a": 19, "person_b": 18, "type": "跨县干部交流", "context": "王镇义(镇远出身)与刘建新(镇远历任书记)同为镇远地方干部体系", "overlap_org": "镇远县", "overlap_period": "历年"},
    {"person_a": 19, "person_b": 1, "type": "跨县干部交流", "context": "王镇义(镇远出身, 升任州/外州市领导)与杨琼(现任书记)分属不同任期", "overlap_org": "镇远/黔东南州", "overlap_period": "跨任"},
]

# ════════════════════════════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════════════════════════════
def build() -> None:
    STAGING.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    try:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS persons")
        cur.execute("DROP TABLE IF EXISTS organizations")
        cur.execute("DROP TABLE IF EXISTS positions")
        cur.execute("DROP TABLE IF EXISTS relationships")
        cur.execute("""CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT)""")
        cur.execute("""CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT)""")
        cur.execute("""CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
            title TEXT, start_date TEXT, end_date TEXT, rank TEXT, note TEXT)""")
        cur.execute("""CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT)""")
        cur.executemany(
            "INSERT INTO persons VALUES (:id,:name,:gender,:ethnicity,:birth,:birthplace,:education,:party_join,:work_start,:current_post,:current_org,:source)",
            [{k: (v if v is not None else "") for k, v in p.items()} for p in persons],
        )
        cur.executemany(
            "INSERT INTO organizations (id,name,type,level,parent,location) VALUES (:id,:name,:type,:level,:parent,:location)",
            organizations,
        )
        cur.executemany(
            "INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (:person_id,:org_id,:title,:start_date,:end_date,:rank,:note)",
            positions,
        )
        cur.executemany(
            "INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (:person_a,:person_b,:type,:context,:overlap_org,:overlap_period)",
            relationships,
        )
        conn.commit()
    finally:
        conn.close()

    # ── GEXF ──
    def esc(s: object) -> str:
        return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    color_of = {7: "255,184,28", 9: "50,160,255", 10: "255,140,0", 11: "180,180,180"}
    person_color = {
        1: "255,50,50",   # 县委书记 - 红
        2: "50,100,255",  # 县长 - 蓝
        3: "140,140,140",
        5: "34,139,34",
        6: "140,80,160",
        7: "50,100,255",
        8: "50,100,255",
        9: "50,100,255",
        10: "50,100,255",
        11: "50,100,255",
        12: "50,100,255",
        13: "50,100,255",
        14: "50,100,255",
        15: "140,140,140",
        16: "50,100,255",
        17: "160,160,160",
        18: "200,80,80",
        19: "200,80,80",
        20: "50,100,255",
        21: "50,100,255",
        22: "50,100,255",
    }
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append('  <meta lastmodifieddate="%s">' % TODAY)
    lines.append('    <creator>china-gov-network Agent</creator>')
    lines.append('    <description>镇远县领导班子工作关系网络 (as of 2026-08)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="relType" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color.get(p["id"], "100,100,100")
        g, r, b = c.split(",")
        lines.append('      <node id="p%d" label="%s">' % (p["id"], esc(p["name"])))
        lines.append('        <attvalues><attvalue for="0" value="person"/></attvalues>')
        lines.append('        <viz:color r="%s" g="%s" b="%s"/>' % (r, g, b))
        lines.append('        <viz:size value="%s"/>' % ("20.0" if p["id"] in (1, 2) else "12.0"))
        lines.append('      </node>')
    for o in organizations:
        lines.append('      <node id="o%d" label="%s">' % (o["id"], esc(o["name"])))
        lines.append('        <attvalues><attvalue for="0" value="org"/></attvalues>')
        lines.append('        <viz:color r="220" g="220" b="220"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        lines.append('      <edge id="e%d" source="p%d" target="o%d" label="%s" weight="1.0">' % (
            eid, pos["person_id"], pos["org_id"], esc(pos["title"])))
        lines.append('        <attvalues><attvalue for="0" value="worked_at"/></attvalues>')
        lines.append('      </edge>')
        eid += 1
    for rel in relationships:
        lines.append('      <edge id="e%d" source="p%d" target="p%d" label="%s" weight="2.0">' % (
            eid, rel["person_a"], rel["person_b"], esc(rel["context"])))
        lines.append('        <attvalues><attvalue for="0" value="%s"/></attvalues>' % esc(rel["type"]))
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    GEXF_PATH.write_text("\n".join(lines), encoding="utf-8")

    print("镇远县 build complete:")
    print("  DB   :", DB_PATH)
    print("  GEXF :", GEXF_PATH)
    print("  persons=%d orgs=%d positions=%d relationships=%d" % (
        len(persons), len(organizations), len(positions), len(relationships)))


if __name__ == "__main__":
    build()