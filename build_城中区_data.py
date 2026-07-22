#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Chengzhong District (城中区), Liuzhou, Guangxi."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangxi_城中区")
DB_PATH = os.path.join(TMP, "城中区_network.db")
GEXF_PATH = os.path.join(TMP, "城中区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "宋军", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-06", "birthplace": "广西融安", "education": "在职大学学历",
     "party_join": "1998-12", "work_start": "1993-07",
     "current_post": "柳州市城中区委书记", "current_org": "中共柳州市城中区委员会",
     "source": "https://baike.baidu.com/item/%E5%AE%8B%E5%86%9B/57281422"},
    {"id": 2, "name": "莫慧明", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-04", "birthplace": "广西柳城", "education": "在职大学学历",
     "party_join": "2008-04", "work_start": "2004-01",
     "current_post": "柳州市城中区政府党组书记、代理区长", "current_org": "柳州市城中区人民政府",
     "source": "https://baike.baidu.com/item/%E8%8E%AB%E6%85%A7%E6%98%8E/57616052"},

    # ── Predecessor Leaders ──
    {"id": 3, "name": "周水祥", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-06", "birthplace": "江西湖口", "education": "研究生/法律硕士（清华大学）",
     "party_join": "2005-11", "work_start": "2011-07",
     "current_post": "柳州市柳北区委书记（原城中区区长）", "current_org": "中共柳州市柳北区委员会",
     "source": "https://baike.baidu.com/item/%E5%91%A8%E6%B0%B4%E7%A5%A5/31661385"},
    {"id": 4, "name": "刘杰华", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-05", "birthplace": "辽宁北票", "education": "在职研究生/工商管理学硕士",
     "party_join": "2002-12", "work_start": "2003-07",
     "current_post": "原城中区区长（~2024年离任）", "current_org": "",
     "source": "https://www.chengzhong.gov.cn"},

    # ── Standing Committee Members ──
    {"id": 5, "name": "王琦", "gender": "女", "ethnicity": "汉族",
     "birth": "1979-12", "birthplace": "江西新余", "education": "在职研究生/理学硕士",
     "party_join": "2003-10", "work_start": "2000-11",
     "current_post": "城中区委副书记", "current_org": "中共柳州市城中区委员会",
     "source": "https://www.chengzhong.gov.cn"},
    {"id": 6, "name": "栗庆耀", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-10", "birthplace": "陕西旬阳", "education": "研究生学历",
     "party_join": "2007-06", "work_start": "2008-04",
     "current_post": "城中区委常委、常务副区长", "current_org": "柳州市城中区人民政府",
     "source": "https://www.chengzhong.gov.cn"},
    {"id": 7, "name": "魏莉", "gender": "女", "ethnicity": "汉族",
     "birth": "1978-06", "birthplace": "陕西宝鸡", "education": "广西大学本科学历",
     "party_join": "2001-12", "work_start": "2003-03",
     "current_post": "城中区委常委、纪委书记", "current_org": "中共柳州市城中区纪律检查委员会",
     "source": "https://www.chengzhong.gov.cn"},
    {"id": 8, "name": "周伟平", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-02", "birthplace": "湖南祁东", "education": "研究生/法学硕士（湖南大学）",
     "party_join": "", "work_start": "",
     "current_post": "城中区委常委（原常务副区长）", "current_org": "中共柳州市城中区委员会",
     "source": "https://www.chengzhong.gov.cn"},
    {"id": 9, "name": "刘长河", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "城中区委常委、政法委书记", "current_org": "中共柳州市城中区委员会",
     "source": "https://www.chengzhong.gov.cn"},
    {"id": 10, "name": "佟德军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "城中区委常委、统战部部长", "current_org": "中共柳州市城中区委员会",
     "source": "https://www.chengzhong.gov.cn"},
    {"id": 11, "name": "覃卢露", "gender": "女", "ethnicity": "壮族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "城中区委常委、宣传部部长", "current_org": "中共柳州市城中区委员会",
     "source": "https://www.chengzhong.gov.cn"},
    {"id": 12, "name": "王佳富", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "城中区委常委、区委办主任", "current_org": "中共柳州市城中区委员会",
     "source": "https://www.chengzhong.gov.cn"},
    {"id": 13, "name": "杨志海", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "城中区委常委、人武部", "current_org": "柳州市城中区人民武装部",
     "source": "https://www.chengzhong.gov.cn"},

    # ── Deputy District Chiefs (副区长) ──
    {"id": 14, "name": "占平", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-09", "birthplace": "湖北浠水", "education": "武汉科技大学城市建设学院",
     "party_join": "2004-11", "work_start": "2002-07",
     "current_post": "城中区副区长", "current_org": "柳州市城中区人民政府",
     "source": "https://www.chengzhong.gov.cn"},
    {"id": 15, "name": "韦文学", "gender": "男", "ethnicity": "壮族",
     "birth": "", "birthplace": "广西融安", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "城中区副区长", "current_org": "柳州市城中区人民政府",
     "source": "https://www.chengzhong.gov.cn"},
    {"id": 16, "name": "李敏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "城中区副区长", "current_org": "柳州市城中区人民政府",
     "source": "https://www.chengzhong.gov.cn"},
    {"id": 17, "name": "亓树思", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "山东临沂", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "城中区副区长", "current_org": "柳州市城中区人民政府",
     "source": "https://www.chengzhong.gov.cn"},
    {"id": 18, "name": "储云", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-01", "birthplace": "江苏扬州", "education": "西安交通大学电机专业/工学学士",
     "party_join": "1990-06", "work_start": "1990-07",
     "current_post": "城中区副区长、公安分局局长", "current_org": "柳州市公安局城中分局",
     "source": "https://www.chengzhong.gov.cn"},
    {"id": 19, "name": "唐宏虎", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "城中区政府党组成员", "current_org": "柳州市城中区人民政府",
     "source": "https://www.chengzhong.gov.cn"},
    {"id": 20, "name": "张光禄", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "城中区政府党组成员", "current_org": "柳州市城中区人民政府",
     "source": "https://www.chengzhong.gov.cn"},
]

organizations = [
    {"id": 1, "name": "中共柳州市城中区委员会", "type": "党委", "level": "县处级", "parent": "中共柳州市委员会",
     "location": "广西柳州市城中区"},
    {"id": 2, "name": "柳州市城中区人民政府", "type": "政府", "level": "县处级", "parent": "柳州市人民政府",
     "location": "广西柳州市城中区"},
    {"id": 3, "name": "中共柳州市城中区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共柳州市纪律检查委员会",
     "location": "广西柳州市城中区"},
    {"id": 4, "name": "柳州市公安局城中分局", "type": "政府", "level": "乡科级", "parent": "柳州市公安局",
     "location": "广西柳州市城中区"},
    {"id": 5, "name": "柳州市城中区人民武装部", "type": "政府", "level": "县处级", "parent": "柳州军分区",
     "location": "广西柳州市城中区"},
    {"id": 6, "name": "中共柳州市委组织部", "type": "党委", "level": "地厅级", "parent": "中共柳州市委员会",
     "location": "广西柳州市"},
    {"id": 7, "name": "柳州市发展和改革委员会", "type": "政府", "level": "县处级", "parent": "柳州市人民政府",
     "location": "广西柳州市"},
    {"id": 8, "name": "柳州市人民政府办公室", "type": "政府", "level": "县处级", "parent": "柳州市人民政府",
     "location": "广西柳州市"},
    {"id": 9, "name": "融安县人民政府", "type": "政府", "level": "县处级", "parent": "柳州市人民政府",
     "location": "广西柳州市融安县"},
    {"id": 10, "name": "融安县长安镇", "type": "乡镇/街道", "level": "乡科级", "parent": "融安县人民政府",
     "location": "广西柳州市融安县"},
    {"id": 11, "name": "中共融水县委", "type": "党委", "level": "县处级", "parent": "中共柳州市委员会",
     "location": "广西柳州市融水县"},
    {"id": 12, "name": "柳州市鱼峰区人民政府", "type": "政府", "level": "县处级", "parent": "柳州市人民政府",
     "location": "广西柳州市鱼峰区"},
    {"id": 13, "name": "北海市商务局", "type": "政府", "level": "县处级", "parent": "北海市人民政府",
     "location": "广西北海市"},
    {"id": 14, "name": "合浦县人民政府", "type": "政府", "level": "县处级", "parent": "北海市人民政府",
     "location": "广西北海市合浦县"},
    {"id": 15, "name": "中共北海市委组织部", "type": "党委", "level": "地厅级", "parent": "中共北海市委员会",
     "location": "广西北海市"},
    {"id": 16, "name": "柳州市自然资源和规划局", "type": "政府", "level": "县处级", "parent": "柳州市人民政府",
     "location": "广西柳州市"},
    {"id": 17, "name": "广西壮族自治区审计厅", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府",
     "location": "广西南宁市"},
    {"id": 18, "name": "中共柳州市城中区人大常委会", "type": "人大", "level": "县处级", "parent": "柳州市人大常委会",
     "location": "广西柳州市城中区"},
    {"id": 19, "name": "柳州市城中区政协", "type": "政协", "level": "县处级", "parent": "柳州市政协",
     "location": "广西柳州市城中区"},
    {"id": 20, "name": "中共柳州市柳北区委员会", "type": "党委", "level": "县处级", "parent": "中共柳州市委员会",
     "location": "广西柳州市柳北区"},
]

positions = [
    # ── Song Jun's Career (宋军) ──
    {"person_id": 1, "org_id": 10, "title": "融安县长安镇党委书记", "start": "", "end": "", "rank": "", "note": "早期职务"},
    {"person_id": 1, "org_id": 11, "title": "融水县委常委、组织部部长", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "融安县委常委、常务副县长", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "柳州市委组织部副部长", "start": "", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "柳州市委组织部分管日常工作的副部长（正处长级）", "start": "", "end": "2021-06", "rank": "正县级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "柳州市城中区委书记", "start": "2021-06", "end": "present", "rank": "副厅级", "note": "2021年6月公示拟任县区党委书记"},

    # ── Mo Huiming's Career (莫慧明) ──
    {"person_id": 2, "org_id": 7, "title": "柳州市发展和改革委员会办公室主任、一级主任科员", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "鱼峰区人民政府副区长、党组成员", "start": "", "end": "2024-07", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "融安县人民政府副县长", "start": "2024-07", "end": "2026-07", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "城中区政府党组书记、代理区长", "start": "2026-07-14", "end": "present", "rank": "正县级", "note": "2026年7月14日区人大常委会决定代理区长"},

    # ── Zhou Shuixiang's Career (周水祥) ──
    {"person_id": 3, "org_id": 15, "title": "北海市委组织部（选调生）", "start": "2011-07", "end": "", "rank": "", "note": "清华大学选调生"},
    {"person_id": 3, "org_id": 14, "title": "合浦县委常委、常务副县长、县委办主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 13, "title": "北海市商务局局长、党组书记", "start": "", "end": "2024-07", "rank": "正县级", "note": "兼市口岸办主任、贸促会会长"},
    {"person_id": 3, "org_id": 2, "title": "城中区委副书记、代区长", "start": "2024-07", "end": "2024-09", "rank": "正县级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "城中区委副书记、区长", "start": "2024-09-13", "end": "2026-06", "rank": "正县级", "note": "2024年9月13日城中区十三届人大五次会议当选"},
    {"person_id": 3, "org_id": 20, "title": "柳北区委书记", "start": "2026-06", "end": "present", "rank": "副厅级", "note": "2026年6月任前公示"},

    # ── Liu Jehua's Career (刘杰华) ──
    {"person_id": 4, "org_id": 2, "title": "城中区区长", "start": "", "end": "2024-07", "rank": "正县级", "note": "前任区长"},

    # ── Wang Qi (王琦) ──
    {"person_id": 5, "org_id": 1, "title": "城中区委常委、组织部部长", "start": "", "end": "c.2021", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "城中区委副书记", "start": "c.2021-06", "end": "present", "rank": "副县级", "note": "2021年6月任前公示拟任县区党委副书记"},

    # ── Li Qingyao (栗庆耀) ──
    {"person_id": 6, "org_id": 8, "title": "柳州市人民政府办公室基础设施科科长", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "柳州市人民政府副秘书长", "start": "", "end": "2024-12", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "城中区委常委、区人民政府党组副书记、副区长（常务）", "start": "2024-12", "end": "present", "rank": "副县级", "note": ""},

    # ── Wei Li (魏莉) ──
    {"person_id": 7, "org_id": 3, "title": "城中区委常委、纪委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # ── Zhou Weiping (周伟平) ──
    {"person_id": 8, "org_id": 17, "title": "广西审计厅办公室副主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "城中区副区长（挂职2年）", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "城中区委常委、副区长（分管常务工作）", "start": "2022-07", "end": "2024-12", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "城中区委常委", "start": "2024-12", "end": "present", "rank": "副县级", "note": "角色调整"},

    # ── Liu Changhe (刘长河) ──
    {"person_id": 9, "org_id": 1, "title": "城中区委常委、政法委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # ── Tong Dejun (佟德军) ──
    {"person_id": 10, "org_id": 1, "title": "城中区委常委、统战部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # ── Qin Lulu (覃卢露) ──
    {"person_id": 11, "org_id": 1, "title": "城中区委常委、宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # ── Wang Jiafu (王佳富) ──
    {"person_id": 12, "org_id": 1, "title": "城中区委常委、区委办主任", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # ── Yang Zhihai (杨志海) ──
    {"person_id": 13, "org_id": 5, "title": "城中区委常委、人武部", "start": "", "end": "present", "rank": "", "note": ""},

    # ── Zhan Ping (占平) ──
    {"person_id": 14, "org_id": 8, "title": "柳州市人民政府办公室第二秘书科干部", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "城中区副区长", "start": "2021-11-03", "end": "present", "rank": "副县级", "note": ""},

    # ── Wei Wenxue (韦文学) ──
    {"person_id": 15, "org_id": 2, "title": "城中区副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # ── Li Min (李敏) ──
    {"person_id": 16, "org_id": 2, "title": "城中区副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # ── Qi Shusi (亓树思) ──
    {"person_id": 17, "org_id": 16, "title": "柳州市自然资源和规划局", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "城中区副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # ── Chu Yun (储云) ──
    {"person_id": 18, "org_id": 4, "title": "城中区副区长、公安分局局长", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # ── Tang Honghu (唐宏虎) ──
    {"person_id": 19, "org_id": 2, "title": "城中区政府党组成员", "start": "", "end": "present", "rank": "", "note": ""},

    # ── Zhang Guanglu (张光禄) ──
    {"person_id": 20, "org_id": 2, "title": "城中区政府党组成员", "start": "", "end": "present", "rank": "", "note": ""},
]

relationships = [
    # ── 书记 × 区长 ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "宋军作为区委书记，莫慧明作为代理区长，是新党政一把手搭档",
     "overlap_org": "中共柳州市城中区委员会/柳州市城中区人民政府",
     "overlap_period": "2026-07至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "strength": "strong",
     "context": "宋军与周水祥在城中区党政一把手搭档（2024-2026）",
     "overlap_org": "中共柳州市城中区委员会/柳州市城中区人民政府",
     "overlap_period": "2024-2026", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor", "strength": "strong",
     "context": "周水祥调任柳北区委书记后，莫慧明接任代理区长",
     "overlap_org": "柳州市城中区人民政府",
     "overlap_period": "2026-07", "confidence": "confirmed"},

    # ── 书记 × 常委 ──
    {"person_a": 1, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "宋军与王琦在城中区委共事，王琦任区委副书记",
     "overlap_org": "中共柳州市城中区委员会",
     "overlap_period": "2021-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "strength": "strong",
     "context": "宋军与魏莉在城中区委共事，魏莉任纪委书记",
     "overlap_org": "中共柳州市城中区委员会",
     "overlap_period": "2021-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "strength": "strong",
     "context": "宋军与刘长河在城中区委共事，刘长河任政法委书记",
     "overlap_org": "中共柳州市城中区委员会",
     "overlap_period": "2021-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "strength": "strong",
     "context": "宋军与佟德军在城中区委共事，佟德军任统战部部长",
     "overlap_org": "中共柳州市城中区委员会",
     "overlap_period": "2021-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "strength": "strong",
     "context": "宋军与覃卢露在城中区委共事，覃卢露任宣传部部长",
     "overlap_org": "中共柳州市城中区委员会",
     "overlap_period": "2021-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "strength": "strong",
     "context": "宋军与王佳富在城中区委共事，王佳富任区委办主任",
     "overlap_org": "中共柳州市城中区委员会",
     "overlap_period": "2021-至今", "confidence": "confirmed"},

    # ── 区长 × 常委/副区长 ──
    {"person_a": 3, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "周水祥与王琦在城中区党政班子共事",
     "overlap_org": "中共柳州市城中区委员会/柳州市城中区人民政府",
     "overlap_period": "2024-2026", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 14, "type": "overlap", "strength": "medium",
     "context": "周水祥与占平在城中区政府班子共事",
     "overlap_org": "柳州市城中区人民政府",
     "overlap_period": "2024-2026", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "strength": "medium",
     "context": "周水祥与栗庆耀在城中区政府班子共事，栗庆耀任常务副区长",
     "overlap_org": "柳州市城中区人民政府",
     "overlap_period": "2024-2026", "confidence": "confirmed"},

    # ── 常务副区长交接 ──
    {"person_a": 8, "person_b": 6, "type": "predecessor_successor", "strength": "strong",
     "context": "周伟平与栗庆耀的常务副区长交接",
     "overlap_org": "柳州市城中区人民政府",
     "overlap_period": "2024-12", "confidence": "confirmed"},

    # ── 融安县共事经历（宋军与莫慧明间接关联） ──
    {"person_a": 1, "person_b": 2, "type": "same_system", "strength": "medium",
     "context": "宋军曾任融安县委常委、常务副县长；莫慧明曾任融安县副县长——二人在融安县有先后任职的间接关联",
     "overlap_org": "融安县人民政府",
     "overlap_period": "宋军: ?-2021; 莫慧明: 2024-2026", "confidence": "plausible"},

    # ── 跨区调动 ──
    {"person_a": 14, "person_b": 17, "type": "overlap", "strength": "weak",
     "context": "占平（从市政府办调来）、亓树思（从市自然资源局调来）均有市级机关工作背景",
     "overlap_org": "柳州市直机关",
     "overlap_period": "", "confidence": "plausible"},
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if "区委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "区长" in role and "副书记" in role:
        return "50,100,255"
    elif "区长" in role:
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")

def is_top_leader(p):
    role = p["current_post"]
    return "区委书记" in role or ("区长" in role and "副书记" in role)

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>城中区领导班子工作关系网络 - 广西柳州市城中区</description>')
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
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
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
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")

# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
