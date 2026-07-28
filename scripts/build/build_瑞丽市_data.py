#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 瑞丽市 leadership network.

调查日期: 2026-07-28
信息来源: 瑞丽市人民政府网站 (rl.gov.cn) 官方领导简介页面
调查级别: 县级市 (德宏傣族景颇族自治州)
"""

import json
import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "瑞丽市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "瑞丽市_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "瑞丽市"

# ── SOURCE REGISTER ────────────────────────────────────────────────
SOURCES = {
    "S001": {
        "id": "S001",
        "title": "温洋 — 瑞丽市人民政府领导简介",
        "url": "https://www.rl.gov.cn/Web/_F0_0_5PQWNCSD0689567207CF4A9D88.htm",
        "publisher": "瑞丽市人民政府",
        "accessed_at": "2026-07-28",
        "source_type": "official",
    },
    "S002": {
        "id": "S002",
        "title": "段如科 — 瑞丽市人民政府领导简介",
        "url": "https://www.rl.gov.cn/Web/_F0_0_6KLF700T6029EF2C45484CDB88.htm",
        "publisher": "瑞丽市人民政府",
        "accessed_at": "2026-07-28",
        "source_type": "official",
    },
    "S003": {
        "id": "S003",
        "title": "徐帅 — 瑞丽市人民政府领导简介",
        "url": "https://www.rl.gov.cn/Web/_F0_0_60B7UDFZ814B878574084E85B9.htm",
        "publisher": "瑞丽市人民政府",
        "accessed_at": "2026-07-28",
        "source_type": "official",
    },
    "S004": {
        "id": "S004",
        "title": "樊欣荣 — 瑞丽市人民政府领导简介",
        "url": "https://www.rl.gov.cn/Web/_F0_0_6KLF6TYX0DBA8CFDDE8C4D7E9F.htm",
        "publisher": "瑞丽市人民政府",
        "accessed_at": "2026-07-28",
        "source_type": "official",
    },
    "S005": {
        "id": "S005",
        "title": "寸宝得 — 瑞丽市人民政府领导简介",
        "url": "https://www.rl.gov.cn/Web/_F0_0_58G2MY39E232B1261C3B403681.htm",
        "publisher": "瑞丽市人民政府",
        "accessed_at": "2026-07-28",
        "source_type": "official",
    },
    "S006": {
        "id": "S006",
        "title": "喊顺 — 瑞丽市人民政府领导简介",
        "url": "https://www.rl.gov.cn/Web/_F0_0_5A88XFY9A5A14B08941C421691.htm",
        "publisher": "瑞丽市人民政府",
        "accessed_at": "2026-07-28",
        "source_type": "official",
    },
    "S007": {
        "id": "S007",
        "title": "彭涛 — 瑞丽市人民政府领导简介",
        "url": "https://www.rl.gov.cn/Web/_F0_0_6LZFUQ53A1AFE214B4344ADF96.htm",
        "publisher": "瑞丽市人民政府",
        "accessed_at": "2026-07-28",
        "source_type": "official",
    },
    "S008": {
        "id": "S008",
        "title": "中共瑞丽市委十四届一次全会 — 瑞丽市人民政府",
        "url": "https://www.rl.gov.cn/Web/_F0_0_6N3C8SXB4FAD488434E04E23A5.htm",
        "publisher": "瑞丽市融媒体中心",
        "accessed_at": "2026-07-28",
        "source_type": "official",
    },
    "S009": {
        "id": "S009",
        "title": "瑞丽市人民政府市长列表",
        "url": "https://www.rl.gov.cn/Web/_M31_4QWU1NV518B4429ABE394586B3_1.htm",
        "publisher": "瑞丽市人民政府",
        "accessed_at": "2026-07-28",
        "source_type": "official",
    },
    "S010": {
        "id": "S010",
        "title": "市委议军会 — 瑞丽市人民政府",
        "url": "https://www.rl.gov.cn/Web/_F0_0_6N6BZF7M971742AA6989499BAF.htm",
        "publisher": "瑞丽市融媒体中心",
        "accessed_at": "2026-07-28",
        "source_type": "official",
    },
    "S011": {
        "id": "S011",
        "title": "寸待纯调研市纪委监委 — 瑞丽市人民政府",
        "url": "https://www.rl.gov.cn/Web/_F0_0_6N4QLWO9B6B1A7F1354942AA9C.htm",
        "publisher": "瑞丽市融媒体中心",
        "accessed_at": "2026-07-28",
        "source_type": "official",
    },
    "S012": {
        "id": "S012",
        "title": "瑞丽市第十四次党代会开幕 — 瑞丽市人民政府",
        "url": "https://www.rl.gov.cn/Web/_F0_0_6N5S1DX4E2F5E1219A1944C3B2D.htm",
        "publisher": "瑞丽市融媒体中心",
        "accessed_at": "2026-07-28",
        "source_type": "official",
    },
    "S013": {
        "id": "S013",
        "title": "毛晓任瑞丽市委书记 — 网易/新华社",
        "url": "https://www.163.com/dy/article/GITNLFV70552DNJF.html",
        "publisher": "网易新闻",
        "accessed_at": "2026-07-28",
        "source_type": "media",
    },
}

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 市委领导 (Party Committee)
    # ═══════════════════════════════
    {
        "id": 1,
        "name": "寸待纯",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德宏州委常委、瑞丽市委书记、市人武部党委第一书记",
        "current_org": "中共瑞丽市委员会",
        "source": "rl.gov.cn 新闻 (S008, S010, S011)",
    },
    {
        "id": 2,
        "name": "温洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-10",
        "birthplace": "",
        "education": "在职硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市委副书记、市长",
        "current_org": "瑞丽市人民政府",
        "source": "rl.gov.cn 领导简介 (S001)",
    },
    {
        "id": 3,
        "name": "夏辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市委副书记",
        "current_org": "中共瑞丽市委员会",
        "source": "rl.gov.cn (S008, S010)",
    },
    {
        "id": 4,
        "name": "段如科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-11",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市委常委、常务副市长",
        "current_org": "瑞丽市人民政府",
        "source": "rl.gov.cn 领导简介 (S002)",
    },
    {
        "id": 5,
        "name": "王敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市委常委",
        "current_org": "中共瑞丽市委员会",
        "source": "rl.gov.cn (S008)",
    },
    {
        "id": 6,
        "name": "王泽升",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市委常委",
        "current_org": "中共瑞丽市委员会",
        "source": "rl.gov.cn (S008, S010, S011)",
    },
    {
        "id": 7,
        "name": "李倩颖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市委常委",
        "current_org": "中共瑞丽市委员会",
        "source": "rl.gov.cn (S008, S010)",
    },
    {
        "id": 8,
        "name": "陈刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市委常委、市纪委书记",
        "current_org": "中共瑞丽市纪律检查委员会",
        "source": "rl.gov.cn (S008, S011)",
    },
    {
        "id": 9,
        "name": "阳艳武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市委常委、市人武部政委",
        "current_org": "瑞丽市人民武装部",
        "source": "rl.gov.cn (S008, S010)",
    },
    {
        "id": 10,
        "name": "线智林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市委常委",
        "current_org": "中共瑞丽市委员会",
        "source": "rl.gov.cn (S008, S010, S011)",
    },
    {
        "id": 11,
        "name": "蒋辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市委常委",
        "current_org": "中共瑞丽市委员会",
        "source": "rl.gov.cn (S008, S010)",
    },
    # ═══════════════════════════════
    # 市政府领导 (Government)
    # ═══════════════════════════════
    {
        "id": 12,
        "name": "徐帅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-10",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市委常委、副市长（挂职二年）",
        "current_org": "瑞丽市人民政府",
        "source": "rl.gov.cn 领导简介 (S003)",
    },
    {
        "id": 13,
        "name": "樊欣荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-03",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市副市长、公安局长",
        "current_org": "瑞丽市人民政府",
        "source": "rl.gov.cn 领导简介 (S004)",
    },
    {
        "id": 14,
        "name": "寸宝得",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-05",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "民盟盟员",
        "work_start": "",
        "current_post": "瑞丽市副市长",
        "current_org": "瑞丽市人民政府",
        "source": "rl.gov.cn 领导简介 (S005)",
    },
    {
        "id": 15,
        "name": "喊顺",
        "gender": "女",
        "ethnicity": "傣族",
        "birth": "1980-08",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市副市长",
        "current_org": "瑞丽市人民政府",
        "source": "rl.gov.cn 领导简介 (S006)",
    },
    {
        "id": 16,
        "name": "彭涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-09",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市副市长",
        "current_org": "瑞丽市人民政府",
        "source": "rl.gov.cn 领导简介 (S007)",
    },
    # ═══════════════════════════════
    # Predecessors (前任)
    # ═══════════════════════════════
    {
        "id": 17,
        "name": "毛晓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-07",
        "birthplace": "云南腾冲（生于梁河县）",
        "education": "中央党校函授法律本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任瑞丽市委书记(2021.09-~2023)",
        "current_org": "",
        "source": "网易/新华社 (S013)",
    },
    {
        "id": 18,
        "name": "翟玉龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-06",
        "birthplace": "安徽芜湖",
        "education": "在职博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任瑞丽市委书记(2021.04-2021.09)",
        "current_org": "",
        "source": "媒体报道 (S013相关)",
    },
    {
        "id": 19,
        "name": "龚云尊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任瑞丽市委书记(至2021.04，因疫情被撤职)",
        "current_org": "",
        "source": "网易新闻 (S013)",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    # Party / Government
    {"id": 1, "name": "中共瑞丽市委员会", "type": "党委", "level": "县级", "parent": "中共德宏州委员会", "location": "瑞丽市"},
    {"id": 2, "name": "瑞丽市人民政府", "type": "政府", "level": "县级", "parent": "德宏傣族景颇族自治州人民政府", "location": "瑞丽市"},
    {"id": 3, "name": "中共瑞丽市纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共德宏州纪律检查委员会", "location": "瑞丽市"},
    {"id": 4, "name": "瑞丽市人民武装部", "type": "政府", "level": "县级", "parent": "德宏军分区", "location": "瑞丽市"},
    # 派出机构 / 功能区
    {"id": 5, "name": "自贸试验区德宏片区管委会", "type": "政府", "level": "县级", "parent": "德宏州人民政府", "location": "瑞丽市"},
    {"id": 6, "name": "瑞丽国家重点开发开放试验区管委会", "type": "政府", "level": "县级", "parent": "云南省人民政府", "location": "瑞丽市"},
    {"id": 7, "name": "瑞丽产业园区管委会", "type": "政府", "level": "县级", "parent": "瑞丽市人民政府", "location": "瑞丽市"},
    {"id": 8, "name": "瑞丽边境经济合作区管委会", "type": "政府", "level": "县级", "parent": "瑞丽市人民政府", "location": "瑞丽市"},
    {"id": 9, "name": "畹町边境经济合作区管委会", "type": "政府", "level": "县级", "parent": "瑞丽市人民政府", "location": "瑞丽市"},
    # 公安
    {"id": 10, "name": "瑞丽市公安局", "type": "政府", "level": "县级", "parent": "瑞丽市人民政府", "location": "瑞丽市"},
]

# ── POSITIONS ─────────────────────────────────────────────────────
positions = [
    # 寸待纯 (id=1)
    {"person_id": 1, "org_id": 1, "title": "德宏州委常委（兼）", "start": "", "end": "present", "rank": "副厅级", "note": "州委常委兼任瑞丽市委书记"},
    {"person_id": 1, "org_id": 1, "title": "瑞丽市委书记", "start": "", "end": "present", "rank": "正处级", "note": "2026年6月26日十四届一次全会当选"},
    {"person_id": 1, "org_id": 4, "title": "市人武部党委第一书记", "start": "", "end": "present", "rank": "", "note": "2026年7月兼任"},
    # 温洋 (id=2)
    {"person_id": 2, "org_id": 1, "title": "瑞丽市委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "瑞丽市长", "start": "", "end": "present", "rank": "正处级", "note": "市政府党组书记"},
    {"person_id": 2, "org_id": 5, "title": "自贸试验区德宏片区管委会主任", "start": "", "end": "present", "rank": "", "note": "兼工委副书记"},
    {"person_id": 2, "org_id": 6, "title": "瑞丽试验区管委会副主任", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "瑞丽产业园区管委会主任", "start": "", "end": "present", "rank": "", "note": "兼工委副书记"},
    {"person_id": 2, "org_id": 8, "title": "瑞丽边境经济合作区管委会主任", "start": "", "end": "present", "rank": "", "note": "兼工委副书记"},
    {"person_id": 2, "org_id": 9, "title": "畹町边境经济合作区管委会主任", "start": "", "end": "present", "rank": "", "note": "兼工委副书记"},
    # 夏辉 (id=3)
    {"person_id": 3, "org_id": 1, "title": "瑞丽市委副书记", "start": "", "end": "present", "rank": "副处级", "note": "2026年6月十四届一次全会当选副书记"},
    # 段如科 (id=4)
    {"person_id": 4, "org_id": 1, "title": "瑞丽市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "瑞丽常务副市长", "start": "", "end": "present", "rank": "副处级", "note": "党组副书记"},
    # 王敏 (id=5)
    {"person_id": 5, "org_id": 1, "title": "瑞丽市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王泽升 (id=6)
    {"person_id": 6, "org_id": 1, "title": "瑞丽市委常委", "start": "", "end": "present", "rank": "副处级", "note": "多次出席市级活动"},
    # 李倩颖 (id=7)
    {"person_id": 7, "org_id": 1, "title": "瑞丽市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 陈刚 (id=8)
    {"person_id": 8, "org_id": 1, "title": "瑞丽市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 3, "title": "市纪委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 阳艳武 (id=9)
    {"person_id": 9, "org_id": 1, "title": "瑞丽市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 4, "title": "市人武部政委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 线智林 (id=10)
    {"person_id": 10, "org_id": 1, "title": "瑞丽市委常委", "start": "", "end": "present", "rank": "副处级", "note": "出席纪委、议军会等活动"},
    # 蒋辉 (id=11)
    {"person_id": 11, "org_id": 1, "title": "瑞丽市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 徐帅 (id=12)
    {"person_id": 12, "org_id": 1, "title": "瑞丽市委常委", "start": "", "end": "present", "rank": "副处级", "note": "挂职"},
    {"person_id": 12, "org_id": 2, "title": "瑞丽市副市长 (挂职)", "start": "", "end": "present", "rank": "副处级", "note": "挂职二年"},
    # 樊欣荣 (id=13)
    {"person_id": 13, "org_id": 2, "title": "瑞丽市副市长", "start": "", "end": "present", "rank": "副处级", "note": "党组成员"},
    {"person_id": 13, "org_id": 10, "title": "瑞丽市公安局局长", "start": "", "end": "present", "rank": "副处级", "note": "党委书记、督察长"},
    # 寸宝得 (id=14)
    {"person_id": 14, "org_id": 2, "title": "瑞丽市副市长", "start": "", "end": "present", "rank": "副处级", "note": "非中共党员"},
    # 喊顺 (id=15)
    {"person_id": 15, "org_id": 2, "title": "瑞丽市副市长", "start": "", "end": "present", "rank": "副处级", "note": "党组成员"},
    # 彭涛 (id=16)
    {"person_id": 16, "org_id": 2, "title": "瑞丽市副市长", "start": "", "end": "present", "rank": "副处级", "note": "党组成员"},
    # 毛晓 (id=17)
    {"person_id": 17, "org_id": 1, "title": "瑞丽市委书记", "start": "2021-09", "end": "~2023", "rank": "正处级", "note": "前任"},
    # 翟玉龙 (id=18)
    {"person_id": 18, "org_id": 1, "title": "瑞丽市委书记", "start": "2021-04", "end": "2021-09", "rank": "正处级", "note": "前任"},
    # 龚云尊 (id=19)
    {"person_id": 19, "org_id": 1, "title": "瑞丽市委书记", "start": "~2019", "end": "2021-04", "rank": "正处级", "note": "前任，因疫情被撤职"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────
relationships = [
    # 市委常委会核心关系
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长搭班", "overlap_org": "中共瑞丽市委员会", "overlap_period": "现阶段"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与专职副书记共事", "overlap_org": "中共瑞丽市委员会", "overlap_period": "现阶段"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "市委书记调研市纪委监委", "overlap_org": "中共瑞丽市委员会", "overlap_period": "现阶段"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "市委议军会，市委书记与人武部政委", "overlap_org": "瑞丽市人民武装部", "overlap_period": "现阶段"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "市长与常务副市长", "overlap_org": "瑞丽市人民政府", "overlap_period": "现阶段"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "瑞丽市人民政府", "overlap_period": "现阶段"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长与分管公安的副市长", "overlap_org": "瑞丽市人民政府", "overlap_period": "现阶段"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "瑞丽市人民政府", "overlap_period": "现阶段"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "瑞丽市人民政府", "overlap_period": "现阶段"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "瑞丽市人民政府", "overlap_period": "现阶段"},
    # 常委之间（同为市委常委）
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同为瑞丽市委常委", "overlap_org": "中共瑞丽市委员会", "overlap_period": "现阶段"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "同为瑞丽市委常委", "overlap_org": "中共瑞丽市委员会", "overlap_period": "现阶段"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "同为瑞丽市委常委", "overlap_org": "中共瑞丽市委员会", "overlap_period": "现阶段"},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "同为瑞丽市委常委", "overlap_org": "中共瑞丽市委员会", "overlap_period": "现阶段"},
    {"person_a": 3, "person_b": 10, "type": "overlap", "context": "同为瑞丽市委常委", "overlap_org": "中共瑞丽市委员会", "overlap_period": "现阶段"},
    {"person_a": 3, "person_b": 11, "type": "overlap", "context": "同为瑞丽市委常委", "overlap_org": "中共瑞丽市委员会", "overlap_period": "现阶段"},
    # 前任-继任关系 (Predecessor-Successor)
    {"person_a": 19, "person_b": 18, "type": "predecessor_successor", "context": "龚云尊被撤职后翟玉龙接任瑞丽市委书记", "overlap_org": "中共瑞丽市委员会", "overlap_period": "2021.04"},
    {"person_a": 18, "person_b": 17, "type": "predecessor_successor", "context": "翟玉龙后毛晓接任瑞丽市委书记", "overlap_org": "中共瑞丽市委员会", "overlap_period": "2021.09"},
    {"person_a": 17, "person_b": 1, "type": "predecessor_successor", "context": "毛晓后寸待纯接任瑞丽市委书记", "overlap_org": "中共瑞丽市委员会", "overlap_period": "~2023"},
]

# ── BUILD ──────────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(pid):
    # Party Secretary: red
    if pid == 1:
        return "255,50,50"
    # Government head (mayor): blue
    if pid == 2:
        return "50,100,255"
    # Discipline Inspection: orange
    if pid == 8:
        return "255,165,0"
    # Predecessors: grey
    if pid in (17, 18, 19):
        return "160,160,160"
    # Default: grey
    return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(pid):
    return pid in (1, 2)  # 市委书记, 市长


if __name__ == "__main__":
    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

    # Write to staging
    db_path = DB_PATH
    gexf_path = GEXF_PATH

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    # ── Person JSON files ─────────────────────────────────────────
    for p in persons:
        if not p["name"] or p["name"] == "":
            continue
        # Build person JSON (simplified version for build pipeline)
        person_data = {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "云南省",
                "city": "德宏傣族景颇族自治州",
                "region": "瑞丽市",
                "job": p.get("current_post", ""),
                "task_id": "yunnan_瑞丽市",
                "time_focus": "2025-2026",
            },
            "identity": {
                "person_id": f"ruili_{p['name']}",
                "name": p["name"],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "education": p.get("education", ""),
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "as_of": "2026-07-28",
                "is_current_confirmed": not p["name"] in ("毛晓", "迟玉龙", "龚云尊"),
            },
            "career_timeline": [],
            "organizations": [],
            "relationships": [],
            "governance_record": [],
            "professional_profile": {},
            "work_style_and_personality": {},
            "network_metrics": {},
            "risk_and_integrity_signals": [],
            "source_register": [],
            "confidence_summary": {},
            "open_questions": [],
        }

        # Add career timeline from positions
        timeline = []
        for pos in positions:
            if pos["person_id"] == p["id"]:
                org_name = ""
                for o in organizations:
                    if o["id"] == pos["org_id"]:
                        org_name = o["name"]
                        break
                timeline.append({
                    "start": pos.get("start", ""),
                    "end": pos.get("end", ""),
                    "org": org_name,
                    "title": pos.get("title", ""),
                    "rank": pos.get("rank", ""),
                    "notes": pos.get("note", ""),
                    "confidence": "confirmed",
                    "source_ids": [],
                })
        person_data["career_timeline"] = timeline

        # Add relationships
        rels = []
        for rel in relationships:
            other_id = None
            direction = "other_to_person"
            if rel["person_a"] == p["id"]:
                other_id = rel["person_b"]
                direction = "person_to_other"
            elif rel["person_b"] == p["id"]:
                other_id = rel["person_a"]
                direction = "other_to_person"
            if other_id:
                other_name = ""
                for op in persons:
                    if op["id"] == other_id:
                        other_name = op["name"]
                        break
                rels.append({
                    "person": other_name,
                    "relationship_type": rel.get("type", ""),
                    "strength": "strong",
                    "evidence": rel.get("context", ""),
                    "overlap_org": rel.get("overlap_org", ""),
                    "overlap_period": rel.get("overlap_period", ""),
                    "direction": direction,
                    "confidence": "confirmed",
                })
        person_data["relationships"] = rels

        # Source register
        source_register = [v for v in SOURCES.values()]
        person_data["source_register"] = source_register

        # Confidence summary
        has_full_bio = bool(p.get("birth") and p.get("education"))
        person_data["confidence_summary"] = {
            "identity": "confirmed" if p["name"] else "unverified",
            "current_role": "confirmed" if p.get("current_post") else "unverified",
            "career_completeness": "complete" if has_full_bio else ("partial" if p.get("birth") else "thin"),
            "biggest_gap": "入职前履历完全未知" if not p.get("work_start") else "",
        }

        # Open questions
        questions = []
        if not p.get("birth"):
            questions.append({
                "priority": "critical" if p["id"] in (1, 2) else "high",
                "question": f"{p['name']}的出生日期",
                "why_it_matters": "身份核验与去重",
                "suggested_queries": [f"{p['name']} 出生"],
                "last_attempted": "2026-07-28",
            })
        if not p.get("birthplace"):
            questions.append({
                "priority": "critical" if p["id"] in (1, 2) else "high",
                "question": f"{p['name']}的籍贯/出生地",
                "why_it_matters": "地缘关系分析",
                "suggested_queries": [f"{p['name']} 籍贯"],
                "last_attempted": "2026-07-28",
            })
        if not p.get("work_start"):
            questions.append({
                "priority": "high",
                "question": f"{p['name']}的入职/从政起始时间",
                "why_it_matters": "完整的职业生涯年表",
                "suggested_queries": [f"{p['name']} 工作简历"],
                "last_attempted": "2026-07-28",
            })
        if p["id"] == 1:
            questions.append({
                "priority": "critical",
                "question": "寸待纯的完整履历 — 接任瑞丽市委书记前的全部职业生涯",
                "why_it_matters": "核心人物履历完全空白",
                "suggested_queries": ["寸待纯 简历 德宏", "寸待纯 此前 任职", "寸待纯 出身"],
                "last_attempted": "2026-07-28",
            })
        if p["id"] == 2:
            questions.append({
                "priority": "critical",
                "question": "温洋2024年任瑞丽市长前的约20年履历（1983年出生约2005年毕业至今）",
                "why_it_matters": "二把手历年去留空，无法判断其调任轨迹",
                "suggested_queries": ["温洋 德宏 简历", "温洋 原任"],
                "last_attempted": "2026-07-28",
            })
        person_data["open_questions"] = questions

        # Save
        # Build a clean job slug
        post = p.get("current_post", "")
        pid = p.get("id", 0)
        if pid == 1:
            job_slug = "市委书记"
        elif pid == 2:
            job_slug = "市长"
        elif pid == 4:
            job_slug = "常务副市长"
        elif pid == 8:
            job_slug = "纪委书记"
        elif pid == 12:
            job_slug = "副市长"
        elif pid == 13:
            job_slug = "副市长"
        elif pid == 14:
            job_slug = "副市长"
        elif pid == 15:
            job_slug = "副市长"
        elif pid == 16:
            job_slug = "副市长"
        elif pid == 3:
            job_slug = "市委副书记"
        elif pid == 9:
            job_slug = "市委常委"
        elif pid in (5, 6, 7, 10, 11):
            job_slug = "市委常委"
        elif pid == 17:
            job_slug = "市委书记"
        elif pid == 18:
            job_slug = "市委书记"
        elif pid == 19:
            job_slug = "市委书记"
        else:
            job_slug = "其他"

        filename = f"{TODAY}-云南省-德宏傣族景颇族自治州-{job_slug}-{p['name']}.json"
        filepath = os.path.join(PERSONS_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(person_data, f, ensure_ascii=False, indent=2)
        print(f"  Wrote {filepath}")

    print(f"\nDone. SQLite: {db_path} | GEXF: {gexf_path}")
    print(f"Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")