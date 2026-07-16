#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 泾县 (Jing County) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/泾县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/泾县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretaries & Government Leaders ──
    {"id": 1, "name": "俞志刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-08", "birthplace": "安徽宁国", "education": "省委党校研究生",
     "party_join": "1998-01", "work_start": "1994-09",
     "current_post": "中共泾县县委书记", "current_org": "中共泾县委员会",
     "source": "https://www.ahjx.gov.cn/News/show/1709038.html"},
    {"id": 2, "name": "李中厚", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-08", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县县委副书记、县政府党组书记、县长", "current_org": "泾县人民政府",
     "source": "https://www.ahjx.gov.cn/SiteLeader/showList/217/5.html"},
    {"id": 3, "name": "施怀中", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-10", "birthplace": "安徽宣州", "education": "省委党校研究生",
     "party_join": "2000-01", "work_start": "1991-06",
     "current_post": "", "current_org": "",
     "source": "https://www.ahjx.gov.cn/News/show/1624820.html"},
    {"id": 4, "name": "许立勋", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-12", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "郎溪县委书记", "current_org": "中共郎溪县委员会",
     "source": "https://www.ahjx.gov.cn/OpennessContent/show/2293927.html"},
    {"id": 5, "name": "孙广东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/%E6%B3%BE%E5%8E%BF"},

    # ── Current County Government Leaders ──
    {"id": 6, "name": "常浩", "gender": "女", "ethnicity": "汉族",
     "birth": "1984-10", "birthplace": "", "education": "在职研究生/公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县县委常委、常务副县长", "current_org": "泾县人民政府",
     "source": "https://www.ahjx.gov.cn/SiteLeader/showList/196/5.html"},
    {"id": 7, "name": "胡晨", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县县委常委、副县长", "current_org": "泾县人民政府",
     "source": "https://www.ahjx.gov.cn/SiteLeader/showList/15/5.html"},
    {"id": 8, "name": "束剑", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县人民政府副县长", "current_org": "泾县人民政府",
     "source": "https://www.ahjx.gov.cn/SiteLeader/showList/15/5.html"},
    {"id": 9, "name": "卢勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-02", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县人民政府副县长", "current_org": "泾县人民政府",
     "source": "https://www.ahjx.gov.cn/SiteLeader/showList/166/5.html"},
    {"id": 10, "name": "黄凰", "gender": "女", "ethnicity": "汉族",
     "birth": "1980-12", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县人民政府副县长", "current_org": "泾县人民政府",
     "source": "https://www.ahjx.gov.cn/SiteLeader/showList/164/5.html"},
    {"id": 11, "name": "苏志刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-12", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县人民政府副县长、县公安局局长", "current_org": "泾县人民政府",
     "source": "https://www.ahjx.gov.cn/SiteLeader/showList/142/5.html"},
    {"id": 12, "name": "程禹柏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县人民政府副县长", "current_org": "泾县人民政府",
     "source": "https://www.ahjx.gov.cn/SiteLeader/showList/15/5.html"},
    {"id": 13, "name": "李廷春", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县人民政府副县长（挂职）", "current_org": "泾县人民政府",
     "source": "https://www.ahjx.gov.cn/SiteLeader/showList/15/5.html"},
    {"id": 14, "name": "徐伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县人民政府副县长", "current_org": "泾县人民政府",
     "source": "https://www.ahjx.gov.cn/SiteLeader/showList/145/5.html"},

    # ── Party Committee Standing Members ──
    {"id": 15, "name": "王勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县县委副书记", "current_org": "中共泾县委员会",
     "source": "https://www.ahjx.gov.cn/News/show/1696819.html"},
    {"id": 16, "name": "芮立军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县县委常委、纪委书记、监委主任", "current_org": "中共泾县纪律检查委员会",
     "source": "https://www.ahjx.gov.cn/News/show/1699221.html"},
    {"id": 17, "name": "余良", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县县委常委、组织部部长", "current_org": "中共泾县委员会",
     "source": "https://www.ahjx.gov.cn/News/show/1696819.html"},
    {"id": 18, "name": "姚瑶", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县县委常委、宣传部部长", "current_org": "中共泾县委员会",
     "source": "https://www.ahjx.gov.cn/News/show/1708910.html"},
    {"id": 19, "name": "舒军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县县委常委、政法委书记", "current_org": "中共泾县委员会",
     "source": "https://www.ahjx.gov.cn/Jczwgk/show/3515576.html"},
    {"id": 20, "name": "陈发贵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县县委常委、统战部部长、县委办主任", "current_org": "中共泾县委员会",
     "source": "https://www.ahjx.gov.cn/News/show/1708099.html"},
    {"id": 21, "name": "陆勤超", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县县委常委、人武部政委", "current_org": "泾县人武部",
     "source": "https://www.ahjx.gov.cn/News/show/1699221.html"},

    # ── Other Key County Leaders ──
    {"id": 22, "name": "詹善清", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县人大常委会主任", "current_org": "泾县人民代表大会常务委员会",
     "source": "https://www.ahjx.gov.cn/News/show/1694676.html"},
    {"id": 23, "name": "吴胜华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县人大常委会党组书记", "current_org": "泾县人民代表大会常务委员会",
     "source": "https://www.ahjx.gov.cn/News/show/1699221.html"},
    {"id": 24, "name": "涂顺", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泾县政协主席", "current_org": "中国人民政治协商会议泾县委员会",
     "source": "https://www.ahjx.gov.cn/News/show/1650083.html"},
]

organizations = [
    {"id": 1, "name": "中共泾县委员会", "type": "党委", "level": "县", "parent": "宣城市", "location": "泾县"},
    {"id": 2, "name": "泾县人民政府", "type": "政府", "level": "县", "parent": "宣城市", "location": "泾县"},
    {"id": 3, "name": "中共泾县纪律检查委员会", "type": "党委", "level": "县", "parent": "泾县", "location": "泾县"},
    {"id": 4, "name": "泾县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "泾县", "location": "泾县"},
    {"id": 5, "name": "中国人民政治协商会议泾县委员会", "type": "政协", "level": "县", "parent": "泾县", "location": "泾县"},
    {"id": 6, "name": "泾县人武部", "type": "党委", "level": "县", "parent": "泾县", "location": "泾县"},
    {"id": 7, "name": "宣城市生态环境局", "type": "政府", "level": "市", "parent": "宣城市", "location": "宣城市"},
    {"id": 8, "name": "郎溪县人民政府", "type": "政府", "level": "县", "parent": "宣城市", "location": "郎溪县"},
    {"id": 9, "name": "安徽省民政厅", "type": "政府", "level": "省", "parent": "安徽省", "location": "合肥市"},
    {"id": 10, "name": "中共郎溪县委员会", "type": "党委", "level": "县", "parent": "宣城市", "location": "郎溪县"},
    {"id": 11, "name": "中共宣州区委", "type": "党委", "level": "县", "parent": "宣城市", "location": "宣州区"},
    {"id": 12, "name": "宣州区人民政府", "type": "政府", "level": "县", "parent": "宣城市", "location": "宣州区"},
    {"id": 13, "name": "中共宁国市委", "type": "党委", "level": "县(市)", "parent": "宣城市", "location": "宁国市"},
    {"id": 14, "name": "宁国市人民政府", "type": "政府", "level": "县(市)", "parent": "宣城市", "location": "宁国市"},
    {"id": 15, "name": "中共旌德县委", "type": "党委", "level": "县", "parent": "宣城市", "location": "旌德县"},
    {"id": 16, "name": "旌德县人民政府", "type": "政府", "level": "县", "parent": "宣城市", "location": "旌德县"},
    {"id": 17, "name": "宣城市委宣传部", "type": "党委", "level": "市", "parent": "宣城市", "location": "宣城市"},
    {"id": 18, "name": "宣城市委组织部", "type": "党委", "level": "市", "parent": "宣城市", "location": "宣城市"},
    {"id": 19, "name": "宣城市财政局", "type": "政府", "level": "市", "parent": "宣城市", "location": "宣城市"},
    {"id": 20, "name": "宣城市总工会", "type": "群团", "level": "市", "parent": "宣城市", "location": "宣城市"},
    {"id": 21, "name": "宣城市公安局", "type": "政府", "level": "市", "parent": "宣城市", "location": "宣城市"},
]

positions = [
    # ── 俞志刚 ──
    {"person_id": 1, "org_id": 1, "title": "中共泾县县委书记",
     "start": "2025-08", "end": "present", "rank": "正处级",
     "note": "2025年8月由宣州区委书记调任泾县县委书记"},
    {"person_id": 1, "org_id": 11, "title": "中共宣州区委书记",
     "start": "2024", "end": "2025-08", "rank": "正处级",
     "note": "曾任宣州区委书记"},
    {"person_id": 1, "org_id": 11, "title": "宣州区委副书记、区长",
     "start": "", "end": "2024", "rank": "正处级",
     "note": "俞志刚此前有宣州区区长、宁国市委常委等工作经历"},
    {"person_id": 1, "org_id": 13, "title": "宁国市委常委",
     "start": "2014", "end": "", "rank": "副处级",
     "note": "2014.03起任宁国市委常委、市委秘书长等职；曾负责援疆工作"},

    # ── 李中厚 ──
    {"person_id": 2, "org_id": 2, "title": "泾县县委副书记、县政府党组书记、代县长/县长",
     "start": "2026-06", "end": "present", "rank": "正处级",
     "note": "2026年6月起任泾县县委副书记、代县长，后任县长"},
    {"person_id": 2, "org_id": 9, "title": "省民政厅人事教育处处长",
     "start": "", "end": "", "rank": "正处级",
     "note": "曾任省民政厅办公室副主任、人事教育处副处长、处长"},
    {"person_id": 2, "org_id": 8, "title": "郎溪县委常委、副县长（挂职）",
     "start": "", "end": "", "rank": "挂职",
     "note": "在省民政厅工作期间挂职郎溪县"},
    {"person_id": 2, "org_id": 10, "title": "郎溪县委副书记（正县级）、新发镇党委书记",
     "start": "", "end": "", "rank": "正处级",
     "note": "挂职结束后留任郎溪县委副书记"},

    # ── 施怀中 ──
    {"person_id": 3, "org_id": 1, "title": "中共泾县县委书记",
     "start": "2021-12", "end": "2025-08", "rank": "正处级",
     "note": "2021年12月起任县委书记"},
    {"person_id": 3, "org_id": 2, "title": "泾县县委副书记、县政府党组书记、县长",
     "start": "2019-03", "end": "2021-12", "rank": "正处级",
     "note": "2019年3月起任代理县长，5月当选县长"},
    {"person_id": 3, "org_id": 7, "title": "宣城市生态环境局局长、党组书记",
     "start": "2019-01", "end": "2019-03", "rank": "正处级",
     "note": "机构改革后任生态环境局局长"},
    {"person_id": 3, "org_id": 7, "title": "宣城市环保局局长、党组书记",
     "start": "2016-03", "end": "2019-01", "rank": "正处级",
     "note": "任宣城市环保局局长"},
    {"person_id": 3, "org_id": 19, "title": "宣城市财政局副局长、党组副书记（正县级）",
     "start": "2013-10", "end": "2016-03", "rank": "正处级",
     "note": "由广德县委常委、常务副县长调任"},
    {"person_id": 3, "org_id": 13, "title": "广德县委常委、县政府常务副县长",
     "start": "2011-09", "end": "2013-10", "rank": "副处级",
     "note": "此前曾任广德县委常委、纪委书记"},
    {"person_id": 3, "org_id": 15, "title": "旌德县委常委、纪委书记",
     "start": "2006-06", "end": "2009-02", "rank": "副处级",
     "note": "此前曾任旌德县副县长"},
    {"person_id": 3, "org_id": 16, "title": "旌德县人民政府副县长",
     "start": "2004-11", "end": "2006-06", "rank": "副处级",
     "note": "由郎溪县地税局局长升任"},

    # ── 许立勋 ──
    {"person_id": 4, "org_id": 2, "title": "泾县县委副书记、县政府党组书记、县长",
     "start": "2021-12", "end": "2026-05", "rank": "正处级",
     "note": "2021年12月提名为县长候选人"},
    {"person_id": 4, "org_id": 10, "title": "郎溪县委书记",
     "start": "2026-05", "end": "present", "rank": "正处级",
     "note": "2026年5月调任郎溪县委书记"},
    {"person_id": 4, "org_id": 17, "title": "宣城市委宣传部常务副部长、市政府新闻办主任（兼）",
     "start": "", "end": "", "rank": "正处级",
     "note": "此前任宣城市委宣传部副部长"},
    {"person_id": 4, "org_id": 13, "title": "宁国市委常委、政法委书记",
     "start": "", "end": "", "rank": "副处级",
     "note": "曾任宁国市委常委、政法委书记、群众工作部部长"},
    {"person_id": 4, "org_id": 14, "title": "宁国市政府党组成员、副市长",
     "start": "", "end": "", "rank": "副处级",
     "note": "曾任宁国市副市长，后入常"},
    {"person_id": 4, "org_id": 20, "title": "宣城市总工会党组成员、副主席",
     "start": "", "end": "", "rank": "副处级",
     "note": ""},
    {"person_id": 4, "org_id": 15, "title": "旌德县俞村镇（乡）党委书记、人大主席",
     "start": "", "end": "", "rank": "正科级",
     "note": "此前曾任旌德县团县委副书记、书记，俞村乡乡长"},

    # ── 常浩 ──
    {"person_id": 6, "org_id": 2, "title": "泾县县委常委、常务副县长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "负责政府常务工作"},
    {"person_id": 6, "org_id": 1, "title": "泾县县委常委、组织部部长、统战部部长",
     "start": "", "end": "", "rank": "副处级",
     "note": "曾任泾县组织部长兼统战部长"},
    {"person_id": 6, "org_id": 18, "title": "宣城市委组织部办公室主任（一级主任科员）",
     "start": "", "end": "", "rank": "正科级",
     "note": "长期在市委组织部工作"},

    # ── 苏志刚 ──
    {"person_id": 11, "org_id": 2, "title": "泾县人民政府副县长、党组成员",
     "start": "", "end": "present", "rank": "副处级",
     "note": "分管公安、司法、信访等"},
    {"person_id": 11, "org_id": 21, "title": "宣城市公安局宣州分局党委副书记、政委",
     "start": "", "end": "", "rank": "正科级",
     "note": "此前任宣州分局副局长、政委等职"},

    # ── 卢勇 ──
    {"person_id": 9, "org_id": 2, "title": "泾县人民政府副县长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "曾任宣城市经信委办公室主任"},

    # ── 黄凰 ──
    {"person_id": 10, "org_id": 2, "title": "泾县人民政府副县长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "曾任泾县文旅局局长"},
]

relationships = [
    # ── Predecessor-Successor ──
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "俞志刚接替施怀中任泾县县委书记", "overlap_org": "中共泾县委员会",
     "overlap_period": "2025-08"},
    {"person_a": 4, "person_b": 2, "type": "predecessor_successor",
     "context": "许立勋调任郎溪县委书记后，李中厚接任泾县县长",
     "overlap_org": "泾县人民政府", "overlap_period": "2026-06"},
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor",
     "context": "施怀中任县委书记时，许立勋任县长（搭档关系）",
     "overlap_org": "泾县", "overlap_period": "2021-12至2025-08"},

    # ── County Committee Team Overlaps ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "俞志刚（县委书记）与李中厚（县长）为当前党政正职搭档",
     "overlap_org": "泾县", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "俞志刚与常浩在泾县县委班子共事", "overlap_org": "中共泾县委员会",
     "overlap_period": "2025-08至今"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "俞志刚与胡晨在泾县县委班子共事", "overlap_org": "中共泾县委员会",
     "overlap_period": "2025-08至今"},
    {"person_a": 1, "person_b": 15, "type": "overlap",
     "context": "俞志刚与王勇（县委副书记）在泾县县委班子共事",
     "overlap_org": "中共泾县委员会", "overlap_period": "2025-08至今"},
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "李中厚与常浩在县政府班子搭档", "overlap_org": "泾县人民政府",
     "overlap_period": "2026-06至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "李中厚与胡晨在县政府班子搭档", "overlap_org": "泾县人民政府",
     "overlap_period": "2026-06至今"},

    # ── Same-System Connections ──
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "施怀中（县委书记）与许立勋（县长）搭档约3年8个月",
     "overlap_org": "泾县", "overlap_period": "2021-12至2025-08"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "俞志刚任县委书记时，许立勋任县长，共事约9个月",
     "overlap_org": "泾县", "overlap_period": "2025-08至2026-05"},
    {"person_a": 3, "person_b": 19, "type": "same_system",
     "context": "施怀中曾在旌德县、广德县任县委常委、纪委书记，与政法系统关联",
     "overlap_org": "旌德/广德", "overlap_period": "2006-2011"},

    # ── 俞志刚与宣州/宁国系统 ──
    {"person_a": 1, "person_b": 3, "type": "cross_county_rotation",
     "context": "俞志刚曾长期在宁国市工作，施怀中曾在广德县工作，均属宣城市系统",
     "overlap_org": "宣城市", "overlap_period": ""},

    # ── 许立勋与宁国系统 ──
    {"person_a": 4, "person_b": 1, "type": "same_system",
     "context": "许立勋与俞志刚均在宁国市有过任职经历（不同时期）",
     "overlap_org": "宁国市", "overlap_period": ""},

    # ── 施怀中与环保/财政系统 ──
    {"person_a": 3, "person_b": 6, "type": "same_system",
     "context": "施怀中（曾任宣城市财政/环保局长）与常浩（曾任宣城市委组织部）同属宣城市直系统",
     "overlap_org": "宣城市直单位", "overlap_period": ""},
]


# ── BUILD DATABASE ────────────────────────────────────────────────

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p["gender"], p["ethnicity"],
                     p["birth"], p["birthplace"], p["education"],
                     p["party_join"], p["work_start"],
                     p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                       VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"],
                     pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"],
                     r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")


# ── BUILD GEXF ─────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p.get("current_post", "")
    if "县委书记" in post:
        return "255,50,50"
    elif "县长" in post or "副县长" in post or "常务副县长" in post:
        return "50,100,255"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    elif "政法委" in post:
        return "200,100,50"
    elif "宣传部" in post or "组织部" in post or "统战部" in post:
        return "180,100,200"
    elif "人大" in post:
        return "50,180,180"
    elif "政协" in post:
        return "180,180,50"
    else:
        return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    elif "群团" in t:
        return "255,220,255"
    else:
        return "200,200,200"

def is_top_leader(p):
    post = p.get("current_post", "")
    return "县委书记" in post or ("县长" in post and "副县长" not in post and "常务" not in post)

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>泾县（安徽省宣城市）领导班子工作关系网络 - 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="birthplace" type="string"/>')
    lines.append('      <attribute id="4" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        eid = f"p{p['id']}"
        lines.append(f'      <node id="{eid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birthplace"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        eid = f"o{o['id']}"
        lines.append(f'      <node id="{eid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="4" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid_counter = [0]
    lines.append('    <edges>')

    # Person→Organization (worked_at)
    for pos in positions:
        eid_counter[0] += 1
        lines.append(f'      <edge id="e{eid_counter[0]}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])} - {esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationship)
    for r in relationships:
        eid_counter[0] += 1
        weight = "2.0"
        lines.append(f'      <edge id="e{eid_counter[0]}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")


# ── MAIN ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    build_db()
    build_gexf()
    print("Done.")
