#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
凯里市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县级市
Province: 贵州省
Parent City: 黔东南苗族侗族自治州
Region: 凯里市
Task: guizhou_凯里市
Targets: 市委书记 & 市长

当前在任 (as of 2026-08-05, 依据 kaili.gov.cn 官方网站确认):
- 市委书记: 谭夔 (州委常委、市委书记; 主持市委常委会/半年经济工作会, 推动景区治理/乡村振兴/项目建设)
- 市委副书记、市长: 杨波 (侗族, 1978-03, 研究生, 党员; 市政府全面工作, 分管财政/审计/粮食)
- 市委副书记: 叶树根、田珍灶
- 市人大常委会主任: 李文禹
- 市政协主席: 王凤贵
- 市委常委、市人武部上校政委: 梁红波
- 市政府常务副市长: 刘鹏 (汉族, 1984-05, 大学, 党员; 市委常委/常务副市长/党组副书记)
- 市政府副市长: 龙安平(苗族1971)、蒋云生(苗族1978)、杨寰(苗族1981)、彭诗美(女侗族1977)、顾启明(苗族1979,兼公安局局长)、欧亚君(1976,2025-09新任)
- 前任市委书记: 王镇义 (→黔南州委副书记→被查; 依据既有镇远调研)
- 上级: 州委书记李建, 州委副书记/州长杨光杰
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
TASK_ID = "guizhou_凯里市"
SLUG = "凯里市"
AS_OF = "2026-08-05"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = BASE

# =========================================================================
# 1. SOURCE REGISTER
# =========================================================================
source_register = [
    {"id": "S001", "title": "凯里市人民政府门户网站 —— 首页/时政要闻（领导活动）",
     "url": "https://www.kaili.gov.cn/", "publisher": "凯里市人民政府", "published_at": "2026-08",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
     "notes": "确认谭夔（州委常委、市委书记）、杨波（市委副书记、市长）等领导活动"},
    {"id": "S002", "title": "凯里市人民政府 —— 谭夔到下司镇、黔东南高新区调研景区运营管理及项目建设工作（2026-08-03）",
     "url": "http://www.kaili.gov.cn/xwzx/jdtxw/202608/t20260803_90685543.html",
     "publisher": "时政凯里/凯里市人民政府", "published_at": "2026-08-03", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "首段点名'州委常委、市委书记谭夔'；政务要点：景区精细化管理、大抓产业/项目/招商/市场主体、黔东南高新区新能源项目建设"},
    {"id": "S003", "title": "凯里市人民政府 —— 谭夔到雨海镇调研（2026-07-30）",
     "url": "http://www.kaili.gov.cn/xwzx/jdtxw/202607/t20260730_90674629.html",
     "publisher": "时政凯里/凯里市人民政府", "published_at": "2026-07-30", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "农村集体'三资'管理、防溺水、G653雨海至凯里公路改扩建项目建设调研"},
    {"id": "S004", "title": "凯里市人民政府 —— 全市半年经济工作会暨市委财经委员会2026年第2次会议（2026-07-31）",
     "url": "http://www.kaili.gov.cn/xwzx/jdtxw/202607/t20260731_90679371.html",
     "publisher": "时政凯里/凯里市人民政府", "published_at": "2026-07-31", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "谭夔主持并讲话；杨波代表市委市政府安排下半年经济工作；出席另有：市人大主任李文禹、市政协主席王凤贵、市委副书记叶树根、田珍灶"},
    {"id": "S005", "title": "凯里市人民政府 —— 市领导开展'八一'走访慰问活动（2026-08-03）",
     "url": "http://www.kaili.gov.cn/xwzx/jdtxw/202608/t20260803_90685546.html",
     "publisher": "时政凯里/凯里市人民政府", "published_at": "2026-08-03", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认：谭夔（书记）、杨波（市长）、李文禹（人大主任）、王凤祥（政协主席）、梁红波（市委常委/市人武部上校政委）、顾启明（副市长/市公安局局长）"},
    {"id": "S006", "title": "凯里市人民政府 —— 凯里市第十届人民政府第151次常务会（2026-08-05）",
     "url": "http://www.kaili.gov.cn/ztzl/klsrmzfcwhy/202608/t20260805_90696620.html",
     "publisher": "凯里市人民政府", "published_at": "2026-08-05", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "市委副书记、市长杨波主持"},
    {"id": "S007", "title": "凯里市人民政府 —— 领导之窗/市长专栏",
     "url": "http://www.kaili.gov.cn/zwgk/ldzc/sz/", "publisher": "凯里市人民政府", "published_at": "2026-08",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
     "notes": "杨波简历：男、侗族、1978-03、中共党员、研究生学历；现任中共贵州省凯里市委副书记，市人民政府市长、党组书记"},
    {"id": "S008", "title": "凯里市人民政府 —— 领导之窗/常务副市长专栏",
     "url": "http://www.kaili.gov.cn/zwgk/ldzc/cwfsz/202501/t20250122_86663380.html",
     "publisher": "凯里市人民政府", "published_at": "2024-01", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "刘鹏简历：汉族、1984-05、大学、党员；中共凯里市委常委、常务副市长、党组副书记"},
    {"id": "S009", "title": "凯里市人民政府 —— 领导之窗/副市长专栏（龙安平）",
     "url": "http://www.kaili.gov.cn/zwgk/ldzc/fsz/202501/t20250122_86663393.html",
     "publisher": "凯里市人民政府", "published_at": "2020-11", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "龙安平：男、苗族、1971-11、大学、党员；市委常委、副市长（农业/水务/供销/林业）"},
    {"id": "S010", "title": "凯里市人民政府 —— 领导之窗/副市长专栏（蒋云生）",
     "url": "http://www.kaili.gov.cn/zwgk/ldzc/fsz/202501/t20250122_86663405.html",
     "publisher": "凯里市人民政府", "published_at": "2020-11", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "蒋云生：男、苗族、1978-10、大学、党员；副市长（交通/教育/市场监管）"},
    {"id": "S011", "title": "凯里市人民政府 —— 领导之窗/副市长专栏（杨寰）",
     "url": "http://www.kaili.gov.cn/zwgk/ldzc/fsz/202506/t20250623_88175526.html",
     "publisher": "凯里市人民政府", "published_at": "2025-06", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "杨寰：男、苗族、1981-10、大学；副市长（商务/工信/科技/招商，协助刘鹏统计/人社）"},
    {"id": "S012", "title": "凯里市人民政府 —— 领导之窗/副市长专栏（彭诗美）",
     "url": "http://www.kaili.gov.cn/zwgk/ldzc/fsz/202501/t20250122_86663409.html",
     "publisher": "凯里市人民政府", "published_at": "2021-12", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "彭诗美：女、侗族、1977-06、大学、党员；副市长（文旅/卫健/医保/民政）"},
    {"id": "S013", "title": "凯里市人民政府 —— 领导之窗/副市长专栏（顾启明）",
     "url": "http://www.kaili.gov.cn/zwgk/ldzc/fsz/202501/t20250122_86663413.html",
     "publisher": "凯里市人民政府", "published_at": "2024-01", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "顾启明：男、苗族、1979-09、大学、党员；副市长/市委政法委委员/市公安局党委书记、局长、督察长（公安/司法/信访）"},
    {"id": "S014", "title": "凯里市人民政府 —— 领导之窗/副市长专栏（欧亚君）",
     "url": "http://www.kaili.gov.cn/zwgk/ldzc/fsz/202509/t20250903_88560576.html",
     "publisher": "凯里市人民政府", "published_at": "2025-09", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "欧亚君：男、1976-10、大学、党员；2025-09 新任副市长（自然资源/住建/城管/生态环境）"},
    {"id": "S015", "title": "本地既有调研 —— 黔东南州/镇远县 report 与 build",
     "url": "report/20260805-贵州省-黔东南苗族侗族自治州-镇远县-领导班子工作关系网络调查报告.md",
     "publisher": "本地仓库", "published_at": "2026-08", "accessed_at": AS_OF,
     "source_type": "inferred", "reliability": "medium",
     "notes": "前任凯里市委书记王镇义（镇远出身→麻江→凯里→黔南州委副书记→被查）；州领导名单含谭夔；州委书记李建、州长杨光杰"},
]

# =========================================================================
# 2. PERSONS
# =========================================================================
persons = [
    # ── 核心领导：市委书记 ──
    {"id": 1, "name": "谭夔", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共凯里市委书记（兼黔东南州委常委）", "current_org": "中共凯里市委员会",
     "source": "S002"},

    # ── 核心领导：市长 ──
    {"id": 2, "name": "杨波", "gender": "男", "ethnicity": "侗族",
     "birth": "1978-03", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凯里市委副书记、市人民政府市长", "current_org": "凯里市人民政府",
     "source": "S007"},

    # ── 市委副书记 ──
    {"id": 3, "name": "叶树根", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凯里市委副书记", "current_org": "中共凯里市委员会",
     "source": "S004"},
    {"id": 4, "name": "田珍灶", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凯里市委副书记", "current_org": "中共凯里市委员会",
     "source": "S004"},

    # ── 市人大 / 市政协 ──
    {"id": 5, "name": "李文禹", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凯里市人大常委会主任", "current_org": "凯里市人民代表大会常务委员会",
     "source": "S005"},
    {"id": 6, "name": "王凤贵", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凯里市政协主席", "current_org": "中国人民政治协商会议凯里市委员会",
     "source": "S005"},

    # ── 市政府班子 ──
    {"id": 7, "name": "刘鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-05", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凯里市人民政府常务副市长（市委常委）", "current_org": "凯里市人民政府",
     "source": "S008"},
    {"id": 8, "name": "龙安平", "gender": "男", "ethnicity": "苗族",
     "birth": "1971-11", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凯里市人民政府副市长（市委常委）", "current_org": "凯里市人民政府",
     "source": "S009"},
    {"id": 9, "name": "蒋云生", "gender": "男", "ethnicity": "苗族",
     "birth": "1978-10", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凯里市人民政府副市长", "current_org": "凯里市人民政府",
     "source": "S010"},
    {"id": 10, "name": "杨寰", "gender": "男", "ethnicity": "苗族",
     "birth": "1981-10", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "凯里市人民政府副市长", "current_org": "凯里市人民政府",
     "source": "S011"},
    {"id": 11, "name": "彭诗美", "gender": "女", "ethnicity": "侗族",
     "birth": "1977-06", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凯里市人民政府副市长", "current_org": "凯里市人民政府",
     "source": "S012"},
    {"id": 12, "name": "顾启明", "gender": "男", "ethnicity": "苗族",
     "birth": "1979-09", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凯里市人民政府副市长、市公安局局长", "current_org": "凯里市人民政府",
     "source": "S013"},
    {"id": 13, "name": "欧亚君", "gender": "男", "ethnicity": "",
     "birth": "1976-10", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凯里市人民政府副市长", "current_org": "凯里市人民政府",
     "source": "S014"},

    # ── 市委其他 ──
    {"id": 14, "name": "梁红波", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凯里市委常委、市人武部上校政委", "current_org": "中国人民解放军凯里市人民武装部",
     "source": "S005"},

    # ── 前任/上级（供网络分析） ──
    {"id": 15, "name": "王镇义", "gender": "男", "ethnicity": "侗族",
     "birth": "", "birthplace": "贵州省镇远县", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黔南州委副书记（原凯里市委书记，已被查）", "current_org": "中共黔南州委员会",
     "source": "S015"},
]

# =========================================================================
# 3. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共凯里市委员会", "type": "党委", "level": "县级",
     "parent": "中共黔东南苗族侗族自治州委员会", "location": "贵州省黔东南州凯里市"},
    {"id": 2, "name": "凯里市人民政府", "type": "政府", "level": "县级",
     "parent": "黔东南苗族侗族自治州人民政府", "location": "贵州省黔东南州凯里市"},
    {"id": 3, "name": "凯里市人民代表大会常务委员会", "type": "人大", "level": "县级",
     "parent": "黔东南苗族侗族自治州人民代表大会常务委员会", "location": "贵州省黔东南州凯里市"},
    {"id": 4, "name": "中国人民政治协商会议凯里市委员会", "type": "政协", "level": "县级",
     "parent": "", "location": "贵州省黔东南州凯里市"},
    {"id": 5, "name": "中共凯里市纪律检查委员会", "type": "纪委", "level": "县级",
     "parent": "中共黔东南苗族侗族自治州纪律检查委员会", "location": "贵州省黔东南州凯里市"},
    {"id": 6, "name": "凯里市公安局", "type": "政府", "level": "正科级",
     "parent": "凯里市人民政府 / 黔东南州公安局", "location": "贵州省黔东南州凯里市"},
    {"id": 7, "name": "凯里市人民武装部", "type": "党委", "level": "县级",
     "parent": "中国人民解放军凯里市人民武装部", "location": "贵州省黔东南州凯里市"},
    {"id": 8, "name": "黔东南高新技术产业开发区", "type": "开发区", "level": "县级",
     "parent": "凯里市人民政府", "location": "贵州省黔东南州凯里市"},
    {"id": 9, "name": "中共黔东南苗族侗族自治州委员会", "type": "党委", "level": "地级",
     "parent": "中共贵州省委员会", "location": "贵州省黔东南州凯里市"},
    {"id": 10, "name": "黔东南苗族侗族自治州人民政府", "type": "政府", "level": "地级",
     "parent": "贵州省人民政府", "location": "贵州省黔东南州凯里市"},
    {"id": 11, "name": "中共黔南州委员会", "type": "党委", "level": "地级",
     "parent": "中共贵州省委员会", "location": "贵州省黔南州"},
]

# =========================================================================
# 4. POSITIONS
# =========================================================================
positions = [
    # ── 谭夔 ──
    {"person_id": 1, "org_id": 1, "title": "中共凯里市委书记",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任；州委常委、市委书记；主持市委常委会/半年经济工作会"},
    {"person_id": 1, "org_id": 9, "title": "黔东南州委常委",
     "start_date": "", "end_date": "", "rank": "州级副职/市委常委", "note": "兼州委常委；参与州70周年州庆筹备等"},
    # ── 杨波 ──
    {"person_id": 2, "org_id": 1, "title": "凯里市委副书记",
     "start_date": "", "end_date": "", "rank": "县级副职", "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "凯里市人民政府市长（党组书记）",
     "start_date": "", "end_date": "", "rank": "县级正职", "note": "现任，领导市政府全面工作，分管财政/审计/粮食；兼市国防动员委员会主任"},
    # ── 叶树根 / 田珍灶 ──
    {"person_id": 3, "org_id": 1, "title": "凯里市委副书记", "start_date": "", "end_date": "", "rank": "县级副职", "note": "现任"},
    {"person_id": 4, "org_id": 1, "title": "凯里市委副书记", "start_date": "", "end_date": "", "rank": "县级副职", "note": "现任"},
    # ── 李文禹、王凤贵 ──
    {"person_id": 5, "org_id": 3, "title": "凯里市人大常委会主任", "start_date": "", "end_date": "", "rank": "县级正职", "note": "现任"},
    {"person_id": 6, "org_id": 4, "title": "凯里市政协主席", "start_date": "", "end_date": "", "rank": "县级正职", "note": "现任"},
    # ── 刘鹏 ──
    {"person_id": 7, "org_id": 1, "title": "凯里市委常委", "start_date": "", "end_date": "", "rank": "县级副职", "note": "现任"},
    {"person_id": 7, "org_id": 2, "title": "凯里市人民政府常务副市长（党组副书记）", "start_date": "", "end_date": "", "rank": "县级副职", "note": "现任；协助市长分管财政/审计"},
    # ── 龙安平 ──
    {"person_id": 8, "org_id": 1, "title": "凯里市委常委", "start_date": "", "end_date": "", "rank": "县级副职", "note": "现任"},
    {"person_id": 8, "org_id": 2, "title": "凯里市人民政府副市长", "start_date": "", "end_date": "", "rank": "县级副职", "note": "现在：农业农村/水务/供销/林业"},
    # ── 蒋云生 ──
    {"person_id": 9, "org_id": 2, "title": "凯里市人民政府副市长", "start_date": "", "end_date": "", "rank": "县级副职", "note": "现任：交通运输/教育/市场监管"},
    # ── 杨寰 ──
    {"person_id": 10, "org_id": 2, "title": "凯里市人民政府副市长", "start_date": "", "end_date": "", "rank": "县级副职", "note": "现任：商务/工信/科技/招商，协助刘鹏分管统计/人社"},
    # ── 彭诗美 ──
    {"person_id": 11, "org_id": 2, "title": "凯里市人民政府副市长", "start_date": "", "end_date": "", "rank": "县级副职", "note": "现任：文旅/卫生/医保/民政/民宗"},
    # ── 顾启明 ──
    {"person_id": 12, "org_id": 2, "title": "凯里市人民政府副市长", "start_date": "", "end_date": "", "rank": "县级副职", "note": "现任"},
    {"person_id": 12, "org_id": 6, "title": "凯里市公安局党委书记、局长", "start_date": "", "end_date": "", "rank": "正科级", "note": "现任；市委政法委委员"},
    # ── 欧亚君 ──
    {"person_id": 13, "org_id": 2, "title": "凯里市人民政府副市长", "start_date": "", "end_date": "", "rank": "县级副职", "note": "2025-09 新任；自然资源/住建/城管/生态环境"},
    # ── 梁红波 ──
    {"person_id": 14, "org_id": 1, "title": "凯里市委常委", "start_date": "", "end_date": "", "rank": "县级副职", "note": "现任"},
    {"person_id": 14, "org_id": 7, "title": "凯里市人武部上校政委", "start_date": "", "end_date": "", "rank": "正科级", "note": "现任"},
    # ── 王镇义（前任） ──
    {"person_id": 15, "org_id": 1, "title": "前任凯里市委书记（黔东南州委常委兼任）", "start_date": "", "end_date": "", "rank": "县级正职", "note": "前期任；离任后调黔南州委副书记，后被查了"},
    {"person_id": 15, "org_id": 11, "title": "黔南州委副书记", "start_date": "", "end_date": "", "rank": "州级副职", "note": "被查（既有调研）"},
]

# =========================================================================
# 5. RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 党政主要领导 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "谭夔（市委书记）与杨波（市委副书记、市长）构成书记-市长搭档",
     "overlap_org": "中共凯里市委员会 / 凯里市人民政府", "overlap_period": "2026"},
    # ── 书记与市委副书记 ──
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "谭夔与市委副书记叶树根在市委班子共事",
     "overlap_org": "中共凯里市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "谭夔与市委副书记田珍灶在市委班子共事",
     "overlap_org": "中共凯里市委员会", "overlap_period": "2026"},
    # ── 书记/市长与人大、政协 ──
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "谭夔（书记）与李文禹（人大常委会主任）同属凯里市四大班子领导的领导干部",
     "overlap_org": "凯里市四大班子", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "杨波（市长）与李文禹（人大常委会主任）同属四大班子领导，'八一'慰问同台",
     "overlap_org": "凯里市四大班子", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "谭夔（书记）与王凤贵（政协主席）同属凯里市四大班子领导",
     "overlap_org": "凯里市四大班子", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "杨波（市长）与王凤贵（政协主席）同属凯里市四大班子领导，半年经济工作会议出席",
     "overlap_org": "凯里市四大班子", "overlap_period": "2026"},
    # ── 市长与市政府班子 ──
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "杨波（市长）与常务副市长刘鹏在市政府班子共事，刘鹏协助其分管财政/审计",
     "overlap_org": "凯里市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "overlap",
     "context": "杨波（市长）与副市长龙安平在市政府班子共事",
     "overlap_org": "凯里市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "overlap",
     "context": "杨波（市长）与副市长蒋云生在市政府班子共事",
     "overlap_org": "凯里市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "杨波（市长）与副市长杨寰在市政府班子共事",
     "overlap_org": "凯里市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 11, "type": "overlap",
     "context": "杨波（市长）与副市长彭诗美在市政府班子共事",
     "overlap_org": "凯里市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 12, "type": "overlap",
     "context": "杨波（市长）与副市长兼公安局长顾启明在市政府班子共事",
     "overlap_org": "凯里市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 13, "type": "overlap",
     "context": "杨波（市长）与副市长欧亚君在市政府班子共事",
     "overlap_org": "凯里市人民政府", "overlap_period": "2026"},
    # ── 书记与政府班子 ──
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "谭夔（书记）与常务副市长刘鹏在县级领导层共事",
     "overlap_org": "凯里市", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 14, "type": "overlap",
     "context": "谭夔（书记）与市委常委、人武部政委梁红波在市委班子共事",
     "overlap_org": "中共凯里市委员会", "overlap_period": "2026"},
    # ── 书记-前任链（交接） ──
    {"person_a": 1, "person_b": 15, "type": "predecessor_successor",
     "context": "谭夔接任王镇义曾担任的凯里市委书记之职（王镇义此前任凯里市委书记），构成职务交接",
     "overlap_org": "中共凯里市委员会", "overlap_period": ""},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build():
    os.makedirs(BASE, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"kaili_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "255,50,50"
        if "市长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "50,100,255"
        if "纪委书记" in post:
            return "255,165,0"
        if "副" in post or "副书记" in post:
            return "100,150,220"
        if "主任" in post and "副" not in post:
            return "60,180,60"
        if "政协" in post:
            return "180,160,80"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post) or \
               ("市长" in post and "副" not in post and "人大" not in post and "政协" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "square"
        if "市长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "circle"
        if "纪委书记" in post or "纪委" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "纪委": "255,200,150",
            "开发区": "200,255,200",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>凯里市领导班子工作关系网络（基于凯里市人民政府门户网站）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person Graph JSONs ──
    now = AS_OF.replace("-", "")

    def make_person_json(p, timeline, relationships_list):
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "贵州省",
                "city": "黔东南苗族侗族自治州",
                "region": "凯里市",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年8月"
            },
            "identity": {
                "person_id": f"kaili_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
                ] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县级正职" if is_top_leader(p.get("current_post", "")) else "县级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": [p.get("source", "")]
            },
            "career_timeline": [],
            "organizations": [],
            "relationships": relationships_list,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "confirmed" if p.get("birth") else "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": ""
            },
            "open_questions": []
        }

    # 谭夔 Person JSON
    tan_timeline = [
        {"start": "", "end": "present", "org": "中共凯里市委员会", "title": "中共凯里市委书记（兼黔东南州委常委）",
         "notes": "现任；2026年7-8月主持市委常委会、全市半年经济工作会议；推动景区精细化管理、产业升级、乡村振兴、项目建设",
         "confidence": "confirmed", "source_ids": ["S002", "S003", "S004"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "谭夔任凯里市委书记前/委任时的出生年、民族、教育背景、完整任职路径未在本次调查中取得（网络搜索受限：Baidu 百科 403、Exa 限流、r.jina.ai 不可达）",
         "confidence": "unverified", "source_ids": []},
    ]
    t_rels = [
        {"person": "杨波", "person_id": "kaili_杨波", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "谭夔（市委书记）与杨波（市委副书记、市长）构成书记-市长搭档",
         "overlap_org": "凯里市委员会/凯里市人民政府", "overlap_period": "2026",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "王镇义", "person_id": "kaili_王镇义", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "谭夔接任王镇义担任过的凯里市委书记职位",
         "overlap_org": "中共凯里市委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "plausible", "source_ids": ["S015"]},
    ]
    tan_json = make_person_json(persons[0], [], [])
    tan_json["relationships"] = t_rels
    tan_json["career_timeline"] = tan_timeline
    tan_json["governance_record"] = [
        {"period": "2026", "domain": "economic_development", "achievement_or_event": "推动产业升级与招商引资（新能源、大中小项目）",
         "role_in_event": "主持全市半年经济工作会并强产业/项目/招商", "location": "凯里市", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
        {"period": "2026", "domain": "rural_revitalization", "achievement_or_event": "赴农村集体'三资'管理、种植业发展调研",
         "role_in_event": "实地调研提要求", "location": "凯里市旁海镇", "confidence": "confirmed", "source_ids": ["S003"]},
        {"period": "2026", "domain": "urban_construction", "achievement_or_event": "景区精细化管理、G653项目推进",
         "role_in_event": "调研并强景区优化", "location": "凯里市下司镇/黔东南高新区", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    tan_json["work_style_and_personality"]["public_style_indicators"] = [
        {"trait": "grassroots_oriented", "evidence": "频繁深入乡镇、高新区、景区一线调研", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"trait": "pragmatic", "evidence": "强调抓投资、招大项目、大抓农民增收的落地式政务语言", "confidence": "plausible", "source_ids": ["S004"]},
    ]
    tan_json["open_questions"] = [
        {"priority": "critical", "question": "谭夔的完整职业生涯履历（出生年、民族、籍贯、教育背景、任凯里市委书记前任职）",
         "why_it_matters": "无法追溯其晋升路径与系统经历（组织/纪检/州机关），影响对'州委常委兼市委书记'安排动因的分析",
         "suggested_queries": ["谭夔 简历 凯里", "谭夔 任前公示", "谭夔 黔东南州委常委 履历"], "last_attempted": AS_OF}
    ]
    tan_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-黔东南苗族侗族自治州-市委书记-谭夔.json")
    with open(tan_path, "w", encoding="utf-8") as f:
        json.dump(tan_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {tan_path}")

    # 杨波 Person JSON
    yb_timeline = [
        {"start": "", "end": "present", "org": "凯里市人民政府", "title": "中共凯里市委副书记、市人民政府市长",
         "notes": "现任；领导市政府全面工作，负责财政/审计/粮食；兼市国防动员委员会主任；姓名党建组书记",
         "confidence": "confirmed", "source_ids": ["S006", "S007"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "杨波任凯里市长前的完整任职何时到任、此前历任职务未在本次取得",
         "confidence": "unverified", "source_ids": []},
    ]
    yb_rels = [
        {"person": "谭夔", "person_id": "kaili_谭夔", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "杨波（市长）与谭夔（市委书记）构成书记-市长搭档",
         "overlap_org": "凯里市委员会/凯里市人民政府", "overlap_period": "2026",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004", "S006"]},
        {"person": "刘鹏", "person_id": "kaili_刘鹏", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "杨波（市长）与常务副市长刘鹏在市政府班子共事，刘鹏协助其分管财政/审计",
         "overlap_org": "凯里市人民政府", "overlap_period": "2026",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S008"]},
        {"person": "顾启明", "person_id": "kaili_顾启明", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "杨波（市长）与副市长兼公安局长顾启明在市政府班子共事，且同岗八一慰问",
         "overlap_org": "凯里市人民政府", "overlap_period": "2026",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
    ]
    yb_json = make_person_json(persons[1], [], [])
    yb_json["career_timeline"] = yb_timeline
    yb_json["relationships"] = yb_rels
    yb_json["governance_record"] = [
        {"period": "2026", "domain": "public_security", "achievement_or_event": "国防动员/民兵、防汛、项目建设督导",
         "role_in_event": "市长兼国防动员委员会主任", "location": "凯里市", "confidence": "confirmed", "source_ids": ["S006"]},
        {"period": "2026", "domain": "economic_development", "achievement_or_event": "代表市委市政府安排下半年经济工作",
         "role_in_event": "分管财政/审计/粮食", "location": "凯里市", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    yb_json["open_questions"] = [
        {"priority": "high", "question": "杨波何年何月起任凯里市长，此前历任职务、籍贯/毕业院校",
         "why_it_matters": "推测其地方履历与晋升速度", "suggested_queries": ["杨波 凯里市长 简历 学历 任前公示"],
         "last_attempted": AS_OF},
    ]
    yb_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-黔东南苗族侗族自治州-市长-杨波.json")
    with open(yb_path, "w", encoding="utf-8") as f:
        json.dump(yb_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {yb_path}")

    print("\nDone. All artifacts generated in staging directory.")


if __name__ == "__main__":
    build()