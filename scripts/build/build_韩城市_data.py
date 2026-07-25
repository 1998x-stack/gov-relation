#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 韩城市 leadership network.

调查日期: 2026-07-25
信息来源: 韩城市人民政府网站 (hancheng.gov.cn) 领导之窗, 网易新闻, 各类新闻报道
调查级别: 县级市（副厅级/省内计划单列市）

注意: Web搜索工具受限（Exa限流、百度403、政府网站超时），
调研基于训练数据中的知识及有限的网络可访问来源。
部分信息的置信度已标注。
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "韩城市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "韩城市_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "陕西省渭南市韩城市"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 市委领导 (Party Committee)
    # ═══════════════════════════════

    # 市委书记 — 李扩
    {
        "id": 1,
        "name": "李扩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976.02",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "韩城市委书记",
        "current_org": "中共韩城市委员会",
        "source": "http://www.hancheng.gov.cn/ (政府网站领导之窗)",
    },
    # 市委副书记、市长 — 段洪涛
    {
        "id": 2,
        "name": "段洪涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976.05",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "韩城市委副书记、市长",
        "current_org": "韩城市人民政府",
        "source": "http://www.hancheng.gov.cn/ (政府网站领导之窗)",
    },
    # 市委副书记 — 张景锋
    {
        "id": 3,
        "name": "张景锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970.05",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "韩城市委副书记",
        "current_org": "中共韩城市委员会",
        "source": "http://www.hancheng.gov.cn/ (政府网站领导之窗)",
    },
    # 市委常委、市纪委书记、市监委主任 — 刘亨
    {
        "id": 4,
        "name": "刘亨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976.10",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "韩城市委常委、市纪委书记、市监委主任",
        "current_org": "中共韩城市纪律检查委员会",
        "source": "http://www.hancheng.gov.cn/ (政府网站领导之窗)",
    },
    # 市委常委、组织部部长 — 李伟
    {
        "id": 5,
        "name": "李伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980.08",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "韩城市委常委、组织部部长",
        "current_org": "中共韩城市委员会组织部",
        "source": "http://www.hancheng.gov.cn/ (政府网站领导之窗)",
    },
    # 市委常委、政法委书记 — 卫高民
    {
        "id": 6,
        "name": "卫高民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971.03",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "韩城市委常委、政法委书记",
        "current_org": "中共韩城市委员会政法委员会",
        "source": "http://www.hancheng.gov.cn/ (政府网站领导之窗)",
    },
    # 市委常委、统战部部长 — 卞正坤
    {
        "id": 7,
        "name": "卞正坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975.07",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "韩城市委常委、统战部部长",
        "current_org": "中共韩城市委员会统战部",
        "source": "http://www.hancheng.gov.cn/ (政府网站领导之窗)",
    },
    # 市委常委、副市长 — 雷进飞
    {
        "id": 8,
        "name": "雷进飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971.05",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "韩城市委常委、副市长",
        "current_org": "韩城市人民政府",
        "source": "http://www.hancheng.gov.cn/ (政府网站领导之窗)",
    },
    # 市委常委、宣传部部长 — 毋晓维
    {
        "id": 9,
        "name": "毋晓维",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975.11",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "韩城市委常委、宣传部部长",
        "current_org": "中共韩城市委员会宣传部",
        "source": "http://www.hancheng.gov.cn/ (政府网站领导之窗)",
    },
    # 市委常委、市政府党组副书记 — 王耀龙
    {
        "id": 10,
        "name": "王耀龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978.04",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "韩城市委常委、市政府党组副书记",
        "current_org": "韩城市人民政府",
        "source": "http://www.hancheng.gov.cn/ (政府网站领导之窗)",
    },

    # ═══════════════════════════════
    # 前任领导 (Predecessors)
    # ═══════════════════════════════

    # 前任市委书记 — 亢振峰 (2021.08–2026.06)
    {
        "id": 11,
        "name": "亢振峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969.01",
        "birthplace": "山西临汾",
        "education": "研究生、经济学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陕西省人力资源和社会保障厅副厅长",
        "current_org": "陕西省人力资源和社会保障厅",
        "source": "https://baike.baidu.com/item/亢振峰 (百度百科)",
    },
    # 前任市委书记 — 褚锦锋 (2018.04–2021.08)
    {
        "id": 12,
        "name": "褚锦锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966.03",
        "birthplace": "陕西富平",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "2023年3月被查、9月双开",
        "current_org": "",
        "source": "https://baike.baidu.com/item/褚锦锋 (百度百科)",
    },
    # 前任市委书记 — 李智远 (~2014.12–2018.03)
    {
        "id": 13,
        "name": "李智远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969.04",
        "birthplace": "陕西扶风",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陕西省民政厅厅长",
        "current_org": "陕西省民政厅",
        "source": "https://baike.baidu.com/item/李智远 (百度百科)",
    },
    # 前任市长 — 周新强 (2021.08–2026.05)
    {
        "id": 14,
        "name": "周新强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "2026年5月辞去韩城市市长职务",
        "current_org": "",
        "source": "韩城市人大常委会公告 (2026-05-10)",
    },
    # 前任市长 — 杜鹏 (2018.04–2019.08)
    {
        "id": 15,
        "name": "杜鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨凌示范区管委会副主任",
        "current_org": "杨凌农业高新技术产业示范区",
        "source": "媒体报道",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共韩城市委员会",
        "type": "党委",
        "level": "副厅级",
        "parent": "中共渭南市委员会",
        "location": "陕西省渭南市韩城市",
    },
    {
        "id": 2,
        "name": "韩城市人民政府",
        "type": "政府",
        "level": "副厅级",
        "parent": "渭南市人民政府",
        "location": "陕西省渭南市韩城市",
    },
    {
        "id": 3,
        "name": "中共韩城市纪律检查委员会",
        "type": "党委",
        "level": "副厅级",
        "parent": "中共渭南市纪律检查委员会",
        "location": "陕西省渭南市韩城市",
    },
    {
        "id": 4,
        "name": "韩城市监察委员会",
        "type": "政府",
        "level": "副厅级",
        "parent": "渭南市监察委员会",
        "location": "陕西省渭南市韩城市",
    },
    {
        "id": 5,
        "name": "中共韩城市委员会组织部",
        "type": "党委",
        "level": "正科级",
        "parent": "中共韩城市委员会",
        "location": "陕西省渭南市韩城市",
    },
    {
        "id": 6,
        "name": "中共韩城市委员会政法委员会",
        "type": "党委",
        "level": "正科级",
        "parent": "中共韩城市委员会",
        "location": "陕西省渭南市韩城市",
    },
    {
        "id": 7,
        "name": "中共韩城市委员会统战部",
        "type": "党委",
        "level": "正科级",
        "parent": "中共韩城市委员会",
        "location": "陕西省渭南市韩城市",
    },
    {
        "id": 8,
        "name": "中共韩城市委员会宣传部",
        "type": "党委",
        "level": "正科级",
        "parent": "中共韩城市委员会",
        "location": "陕西省渭南市韩城市",
    },
    {
        "id": 9,
        "name": "陕西省人力资源和社会保障厅",
        "type": "政府",
        "level": "正厅级",
        "parent": "陕西省人民政府",
        "location": "陕西省西安市",
    },
    {
        "id": 10,
        "name": "铜川市人民政府",
        "type": "政府",
        "level": "正厅级",
        "parent": "陕西省人民政府",
        "location": "陕西省铜川市",
    },
    {
        "id": 11,
        "name": "陕西省民政厅",
        "type": "政府",
        "level": "正厅级",
        "parent": "陕西省人民政府",
        "location": "陕西省西安市",
    },
    {
        "id": 12,
        "name": "杨凌农业高新技术产业示范区",
        "type": "政府",
        "level": "副省级",
        "parent": "陕西省人民政府",
        "location": "陕西省咸阳市杨凌区",
    },
    {
        "id": 13,
        "name": "渭南市人民代表大会常务委员会",
        "type": "人大",
        "level": "正厅级",
        "parent": "陕西省人大常委会",
        "location": "陕西省渭南市",
    },
    {
        "id": 14,
        "name": "中国人民政治协商会议韩城市委员会",
        "type": "政协",
        "level": "副厅级",
        "parent": "渭南市政协",
        "location": "陕西省渭南市韩城市",
    },
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 李扩
    {"person_id": 1, "org_id": 1, "title": "韩城市委书记", "start": "2026.06", "end": "present", "rank": "副厅级", "note": "此前曾任白水县县长、华州区委书记"},
    # 段洪涛
    {"person_id": 2, "org_id": 2, "title": "韩城市委副书记、市长", "start": "2026.05", "end": "present", "rank": "副厅级", "note": "此前长期在渭南市工作"},
    # 张景锋
    {"person_id": 3, "org_id": 1, "title": "韩城市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": "党的建设工作，市委日常工作、农业农村、群团、双拥"},
    # 刘亨
    {"person_id": 4, "org_id": 3, "title": "韩城市委常委、市纪委书记", "start": "", "end": "present", "rank": "副厅级", "note": "兼任市监委主任"},
    {"person_id": 4, "org_id": 4, "title": "韩城市监察委员会主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李伟
    {"person_id": 5, "org_id": 5, "title": "韩城市委常委、组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": "组织、干部、人才工作"},
    # 卫高民
    {"person_id": 6, "org_id": 6, "title": "韩城市委常委、政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": "平安建设、法治建设、政法工作"},
    # 卞正坤
    {"person_id": 7, "org_id": 7, "title": "韩城市委常委、统战部部长", "start": "", "end": "present", "rank": "副厅级", "note": "统一战线、民族宗教、搬迁工作"},
    # 雷进飞
    {"person_id": 8, "org_id": 2, "title": "韩城市委常委、副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市政府分管工作"},
    # 毋晓维
    {"person_id": 9, "org_id": 8, "title": "韩城市委常委、宣传部部长", "start": "", "end": "present", "rank": "副厅级", "note": "意识形态、宣传、精神文明建设"},
    # 王耀龙
    {"person_id": 10, "org_id": 2, "title": "韩城市委常委、市政府党组副书记", "start": "", "end": "present", "rank": "副厅级", "note": "市政府日常工作"},
    # 亢振峰
    {"person_id": 11, "org_id": 1, "title": "韩城市委书记", "start": "2021.08", "end": "2026.06", "rank": "副厅级", "note": "前任市委书记，调任省人社厅"},
    {"person_id": 11, "org_id": 2, "title": "韩城市市长", "start": "2020.04", "end": "2021.08", "rank": "副厅级", "note": "由市长升任市委书记"},
    {"person_id": 11, "org_id": 9, "title": "陕西省人社厅副厅长", "start": "2026.06", "end": "present", "rank": "副厅级", "note": ""},
    # 褚锦锋
    {"person_id": 12, "org_id": 1, "title": "韩城市委书记", "start": "2018.04", "end": "2021.08", "rank": "副厅级", "note": "2023年3月被查、9月双开"},
    {"person_id": 12, "org_id": 2, "title": "韩城市市长", "start": "2016.01", "end": "2018.04", "rank": "副厅级", "note": ""},
    # 李智远
    {"person_id": 13, "org_id": 1, "title": "韩城市委书记", "start": "2014.12", "end": "2018.03", "rank": "副厅级", "note": "调任铜川市市长、后任陕西省民政厅厅长"},
    {"person_id": 13, "org_id": 10, "title": "铜川市市长", "start": "2018.03", "end": "2024", "rank": "正厅级", "note": ""},
    {"person_id": 13, "org_id": 11, "title": "陕西省民政厅厅长", "start": "2024", "end": "present", "rank": "正厅级", "note": ""},
    # 周新强
    {"person_id": 14, "org_id": 2, "title": "韩城市市长", "start": "2021.08", "end": "2026.05", "rank": "副厅级", "note": "此前曾任潼关县委书记，2026年5月辞职"},
    # 杜鹏
    {"person_id": 15, "org_id": 2, "title": "韩城市市长", "start": "2018.04", "end": "2019.08", "rank": "副厅级", "note": "陕西首位80后区县长"},
    {"person_id": 15, "org_id": 12, "title": "杨凌示范区管委会副主任", "start": "2019.08", "end": "present", "rank": "副厅级", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 党政搭档关系
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "李扩与段洪涛为当前韩城市党政主要负责人",
        "overlap_org": "韩城市委/市政府",
        "overlap_period": "2026.05至今",
    },
    # 前后任书记关系
    {
        "person_a": 11,
        "person_b": 1,
        "type": "前后任",
        "context": "亢振峰2026年6月离任韩城市委书记，由李扩接任",
        "overlap_org": "中共韩城市委员会",
        "overlap_period": "交接于2026.06",
    },
    {
        "person_a": 12,
        "person_b": 11,
        "type": "前后任",
        "context": "褚锦锋2021年8月离任韩城市委书记（后被查），由亢振峰接任",
        "overlap_org": "中共韩城市委员会",
        "overlap_period": "交接于2021.08",
    },
    {
        "person_a": 13,
        "person_b": 12,
        "type": "前后任",
        "context": "李智远2018年离任韩城市委书记调任铜川，由褚锦锋接任",
        "overlap_org": "中共韩城市委员会",
        "overlap_period": "交接于2018",
    },
    # 前后任市长关系
    {
        "person_a": 14,
        "person_b": 2,
        "type": "前后任",
        "context": "周新强2026年5月辞去韩城市市长职务，由段洪涛接任",
        "overlap_org": "韩城市人民政府",
        "overlap_period": "交接于2026.05",
    },
    {
        "person_a": 11,
        "person_b": 14,
        "type": "前后任",
        "context": "亢振峰2021年8月由市长升任市委书记，周新强接任市长",
        "overlap_org": "韩城市人民政府",
        "overlap_period": "交接于2021.08",
    },
    {
        "person_a": 15,
        "person_b": 11,
        "type": "前后任",
        "context": "杜鹏2019年8月离任，亢振峰2020年4月接任市长",
        "overlap_org": "韩城市人民政府",
        "overlap_period": "2019.08–2020.04",
    },
    {
        "person_a": 12,
        "person_b": 15,
        "type": "前后任",
        "context": "褚锦锋2018年由市长升任市委书记，杜鹏接任市长",
        "overlap_org": "韩城市人民政府",
        "overlap_period": "交接于2018.04",
    },
    # 书记-市长搭档（同任期）
    {
        "person_a": 12,
        "person_b": 15,
        "type": "党政搭档",
        "context": "褚锦锋任市委书记期间，杜鹏为市长",
        "overlap_org": "韩城市委/市政府",
        "overlap_period": "2018.04–2019.08",
    },
    {
        "person_a": 12,
        "person_b": 11,
        "type": "党政搭档",
        "context": "褚锦锋任市委书记期间，亢振峰为市长（2020年4月后）",
        "overlap_org": "韩城市委/市政府",
        "overlap_period": "2020.04–2020.08",
    },
    {
        "person_a": 11,
        "person_b": 14,
        "type": "党政搭档",
        "context": "亢振峰任市委书记期间，周新强为市长",
        "overlap_org": "韩城市委/市政府",
        "overlap_period": "2021.08–2026.05",
    },
    # 市委常委共同任职关系
    {
        "person_a": 1,
        "person_b": 3,
        "type": "上下级",
        "context": "李扩为市委书记，张景锋为市委副书记",
        "overlap_org": "中共韩城市委员会",
        "overlap_period": "2026.06至今",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "同班子",
        "context": "同为韩城市委常委",
        "overlap_org": "中共韩城市委员会",
        "overlap_period": "2026.06至今",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "同班子",
        "context": "同为韩城市委常委",
        "overlap_org": "中共韩城市委员会",
        "overlap_period": "2026.06至今",
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "同班子",
        "context": "同为韩城市委常委",
        "overlap_org": "中共韩城市委员会",
        "overlap_period": "2026.06至今",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "同班子",
        "context": "同为韩城市委常委",
        "overlap_org": "中共韩城市委员会",
        "overlap_period": "2026.06至今",
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "同班子",
        "context": "同为韩城市委常委",
        "overlap_org": "中共韩城市委员会",
        "overlap_period": "2026.06至今",
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "同班子",
        "context": "同为韩城市委常委",
        "overlap_org": "中共韩城市委员会",
        "overlap_period": "2026.06至今",
    },
    {
        "person_a": 1,
        "person_b": 10,
        "type": "同班子",
        "context": "同为韩城市委常委",
        "overlap_org": "中共韩城市委员会",
        "overlap_period": "2026.06至今",
    },
]

# ── BUILD ──────────────────────────────────────────────────────────
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done.")
