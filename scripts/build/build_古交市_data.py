#!/usr/bin/env python3
"""
古交市领导班子工作关系网络 — 数据构建脚本
调查日期: 2026-07-26
信息来源: 公开新闻报道、古交市人民政府门户网站 (www.gujiao.gov.cn)
"""

import sqlite3
import os
from datetime import datetime

SLUG = "古交市"
TODAY = "2026-07-26"
AS_OF = "2026-07-26"
PROVINCE = "山西省"
CITY = "太原市"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR.endswith("scripts/build"):
    REPO_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
elif "data/tmp" in BASE_DIR:
    parts = BASE_DIR.split(os.sep)
    try:
        tmp_idx = parts.index("tmp")
        REPO_ROOT = os.sep.join(parts[:tmp_idx - 1])
    except ValueError:
        REPO_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
else:
    REPO_ROOT = BASE_DIR
DB_PATH = os.path.join(REPO_ROOT, "data", "database", f"{SLUG}_network.db")
GEXF_PATH = os.path.join(REPO_ROOT, "data", "graph", f"{SLUG}_network.gexf")

# =========================================================================
# Research Data
# =========================================================================

# 古交市 — 太原市下辖的县级市
# 截至 2026-07-26 的领导班子数据
# 注意：由于公开网络检索受限，部分信息为 plausible 等级，详见 open_questions

persons = [
    # ── 1. 市委书记 ──
    {
        "id": 1,
        "name": "李卫雁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共古交市委",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn); 太原市委组织部任前公示",
        "notes": "古交市委书记。曾任古交市市长。完整履历（出生、教育、早期任职等）待查。"
    },
    # ── 2. 市长 ──
    {
        "id": 2,
        "name": "张麒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "古交市人民政府",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn)",
        "notes": "古交市委副书记、市长。曾任古交市委常委、副市长等职务。完整履历待查。"
    },
    # ── 3. 市委副书记 ──
    {
        "id": 3,
        "name": "邢武晓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共古交市委",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn)",
        "notes": "古交市委副书记。协助市委书记处理市委日常工作。"
    },
    # ── 4. 市委常委、副市长（常务） ──
    {
        "id": 4,
        "name": "杜国名",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长（常务）",
        "current_org": "中共古交市委、古交市人民政府",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn)",
        "notes": "常务副市长，负责市政府日常工作。"
    },
    # ── 5. 市委常委、纪委书记、监委主任 ──
    {
        "id": 5,
        "name": "陈铮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共古吉市纪律检查委员会、古交市监察委员会",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn)",
        "notes": "负责纪检监察工作。"
    },
    # ── 6. 市委常委、组织部部长 ──
    {
        "id": 6,
        "name": "李永强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共古交市委组织部",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn)",
        "notes": "负责组织人事工作。"
    },
    # ── 7. 市委常委、政法委书记 ──
    {
        "id": 7,
        "name": "周飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共古交市委政法委",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn)",
        "notes": "负责政法工作。"
    },
    # ── 8. 市委常委、宣传部部长 ──
    {
        "id": 8,
        "name": "崔燕波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共古交市委宣传部",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn)",
        "notes": "负责宣传思想文化工作。"
    },
    # ── 9. 市委常委、统战部部长 ──
    {
        "id": 9,
        "name": "张秀玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共古交市委统战部",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn)",
        "notes": "负责统一战线工作。"
    },
    # ── 10. 市委常委、人武部政委 ──
    {
        "id": 10,
        "name": "许军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市人武部政委",
        "current_org": "古交市人民武装部",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn)",
        "notes": "负责武装工作。"
    },
    # ── 11. 副市长（排名第一） ──
    {
        "id": 11,
        "name": "王勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "古交市人民政府",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn)",
        "notes": "分管领域待查。"
    },
    # ── 12. 副市长 ──
    {
        "id": 12,
        "name": "闫文光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "古交市人民政府",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn)",
        "notes": "分管领域待查。"
    },
    # ── 13. 副市长、市公安局局长 ──
    {
        "id": 13,
        "name": "王治国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "古交市公安局",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn)",
        "notes": "主管公安、司法等工作。"
    },
    # ── 14. 市人大主任 ──
    {
        "id": 14,
        "name": "张刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会党组书记、主任",
        "current_org": "古交市人大常委会",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn)",
        "notes": "负责市人大常委会全面工作。"
    },
    # ── 15. 市政协主席 ──
    {
        "id": 15,
        "name": "李宏刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协党组书记、主席",
        "current_org": "古交市政协",
        "source": "古交市人民政府门户网站 (www.gujiao.gov.cn)",
        "notes": "负责市政协全面工作。"
    },
    # ── 16. 前任市委书记 ──
    {
        "id": 16,
        "name": "翟永清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共古交市委(已离任)",
        "source": "公开新闻报道",
        "notes": "曾任古交市委书记。后调任太原市领导职务（具体去向待查）。"
    },
    # ── 17. 前任市委书记 ──
    {
        "id": 17,
        "name": "贾慕权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共古交市委(已离任)",
        "source": "公开新闻报道",
        "notes": "曾任古交市委书记。后调任太原市卫生健康委员会主任等职务。"
    },
    # ── 18. 前任市长 ──
    {
        "id": 18,
        "name": "刘锦春",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年3月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "古交市人民政府(已离任)",
        "source": "公开新闻报道",
        "notes": "曾任古交市市长。后任太原市尖草坪区委书记。"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共古交市委",
        "type": "党委",
        "level": "县级市",
        "parent": "中共太原市委",
        "location": "山西省太原市古交市"
    },
    {
        "id": 2,
        "name": "古交市人民政府",
        "type": "政府",
        "level": "县级市",
        "parent": "太原市人民政府",
        "location": "山西省太原市古交市"
    },
    {
        "id": 3,
        "name": "中共古交市纪律检查委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共古交市委",
        "location": "山西省太原市古交市"
    },
    {
        "id": 4,
        "name": "古交市监察委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "古交市人民政府",
        "location": "山西省太原市古交市"
    },
    {
        "id": 5,
        "name": "中共古交市委组织部",
        "type": "党委",
        "level": "县级市",
        "parent": "中共古交市委",
        "location": "山西省太原市古交市"
    },
    {
        "id": 6,
        "name": "中共古交市委政法委",
        "type": "党委",
        "level": "县级市",
        "parent": "中共古交市委",
        "location": "山西省太原市古交市"
    },
    {
        "id": 7,
        "name": "中共古交市委宣传部",
        "type": "党委",
        "level": "县级市",
        "parent": "中共古交市委",
        "location": "山西省太原市古交市"
    },
    {
        "id": 8,
        "name": "中共古交市委统战部",
        "type": "党委",
        "level": "县级市",
        "parent": "中共古交市委",
        "location": "山西省太原市古交市"
    },
    {
        "id": 9,
        "name": "古交市人民武装部",
        "type": "党委",
        "level": "县级市",
        "parent": "太原警备区",
        "location": "山西省太原市古交市"
    },
    {
        "id": 10,
        "name": "古交市公安局",
        "type": "政府",
        "level": "县级市",
        "parent": "古交市人民政府",
        "location": "山西省太原市古交市"
    },
    {
        "id": 11,
        "name": "古交市人大常委会",
        "type": "人大",
        "level": "县级市",
        "parent": "太原市人大常委会",
        "location": "山西省太原市古交市"
    },
    {
        "id": 12,
        "name": "古交市政协",
        "type": "政协",
        "level": "县级市",
        "parent": "太原市政协",
        "location": "山西省太原市古交市"
    },
]

positions = [
    # 李卫雁
    {"person_id": "p1", "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正处级", "note": "现任古交市委书记"},
    {"person_id": "p1", "org_id": 2, "title": "市长", "start": "", "end": "", "rank": "正处级", "note": "曾任古交市市长，后接任市委书记"},
    # 张麒
    {"person_id": "p2", "org_id": 2, "title": "市长", "start": "", "end": "present", "rank": "正处级", "note": "现任古交市委副书记、市长"},
    {"person_id": "p2", "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p2", "org_id": 2, "title": "市委常委、副市长", "start": "", "end": "", "rank": "副处级", "note": "曾任古交市委常委、副市长"},
    # 邢武晓
    {"person_id": "p3", "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "", "note": ""},
    # 杜国名
    {"person_id": "p4", "org_id": 2, "title": "市委常委、副市长（常务）", "start": "", "end": "present", "rank": "", "note": "负责市政府日常工作"},
    # 陈铮
    {"person_id": "p5", "org_id": 3, "title": "市委常委、市纪委书记", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": "p5", "org_id": 4, "title": "市监委主任", "start": "", "end": "present", "rank": "", "note": ""},
    # 李永强
    {"person_id": "p6", "org_id": 5, "title": "市委常委、组织部部长", "start": "", "end": "present", "rank": "", "note": ""},
    # 周飞
    {"person_id": "p7", "org_id": 6, "title": "市委常委、政法委书记", "start": "", "end": "present", "rank": "", "note": ""},
    # 崔燕波
    {"person_id": "p8", "org_id": 7, "title": "市委常委、宣传部部长", "start": "", "end": "present", "rank": "", "note": ""},
    # 张秀玲
    {"person_id": "p9", "org_id": 8, "title": "市委常委、统战部部长", "start": "", "end": "present", "rank": "", "note": ""},
    # 许军
    {"person_id": "p10", "org_id": 9, "title": "市委常委、市人武部政委", "start": "", "end": "present", "rank": "", "note": ""},
    # 王勇
    {"person_id": "p11", "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "", "note": ""},
    # 闫文光
    {"person_id": "p12", "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "", "note": ""},
    # 王治国
    {"person_id": "p13", "org_id": 10, "title": "副市长、市公安局局长", "start": "", "end": "present", "rank": "", "note": ""},
    # 张刚
    {"person_id": "p14", "org_id": 11, "title": "市人大常委会主任", "start": "", "end": "present", "rank": "", "note": ""},
    # 李宏刚
    {"person_id": "p15", "org_id": 12, "title": "市政协主席", "start": "", "end": "present", "rank": "", "note": ""},
    # 翟永清
    {"person_id": "p16", "org_id": 1, "title": "市委书记", "start": "", "end": "", "rank": "正处级", "note": "前任古交市委书记"},
    # 贾慕权
    {"person_id": "p17", "org_id": 1, "title": "市委书记", "start": "", "end": "", "rank": "正处级", "note": "前任古交市委书记"},
    # 刘锦春
    {"person_id": "p18", "org_id": 2, "title": "市长", "start": "", "end": "", "rank": "正处级", "note": "前任古交市长，现任尖草坪区委书记"},
]

relationships = [
    # 李卫雁 — 张麒 (党政一把手)
    {"person_a": "p1", "person_b": "p2", "type": "overlap", "context": "市委书记与市长党政一把手搭档", "overlap_org": "古交市", "overlap_period": "至今", "confidence": "confirmed"},
    # 李卫雁 — 邢武晓 (正副书记)
    {"person_a": "p1", "person_b": "p3", "type": "overlap", "context": "市委书记与市委副书记", "overlap_org": "中共古交市委", "overlap_period": "至今", "confidence": "confirmed"},
    # 张麒 — 杜国名 (市长与常务副市长)
    {"person_a": "p2", "person_b": "p4", "type": "overlap", "context": "市长与常务副市长工作搭档", "overlap_org": "古交市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 李卫雁 — 刘锦春 (predecessor-successor 市长)
    {"person_a": "p1", "person_b": "p18", "type": "predecessor_successor", "context": "李卫雁接替刘锦春任古交市长", "overlap_org": "古交市人民政府", "overlap_period": "", "confidence": "confirmed"},
    # 李卫雁 — 翟永清 (predecessor-successor 市委书记)
    {"person_a": "p1", "person_b": "p16", "type": "predecessor_successor", "context": "李卫雁接替翟永清任古交市委书记", "overlap_org": "中共古交市委", "overlap_period": "", "confidence": "plausible"},
    # 翟永清 — 贾慕权 (predecessor-successor 市委书记)
    {"person_a": "p16", "person_b": "p17", "type": "predecessor_successor", "context": "贾慕权后翟永清接任古交市委书记", "overlap_org": "中共古交市委", "overlap_period": "", "confidence": "plausible"},
    # 李卫雁 — 全部市委常委 (市委班子成员)
    {"person_a": "p1", "person_b": "p4", "type": "overlap", "context": "市委书记与常务副市长", "overlap_org": "中共古交市委", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p5", "type": "overlap", "context": "市委书记与市纪委书记", "overlap_org": "中共古交市委", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p6", "type": "overlap", "context": "市委书记与组织部部长", "overlap_org": "中共古交市委", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p7", "type": "overlap", "context": "市委书记与政法委书记", "overlap_org": "中共古交市委", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p8", "type": "overlap", "context": "市委书记与宣传部部长", "overlap_org": "中共古交市委", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p9", "type": "overlap", "context": "市委书记与统战部部长", "overlap_org": "中共古交市委", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p10", "type": "overlap", "context": "市委书记与人武部政委", "overlap_org": "中共古交市委", "overlap_period": "至今", "confidence": "confirmed"},
    # 张麒 — 副市长们
    {"person_a": "p2", "person_b": "p11", "type": "overlap", "context": "市长与副市长工作关系", "overlap_org": "古交市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": "p2", "person_b": "p12", "type": "overlap", "context": "市长与副市长工作关系", "overlap_org": "古交市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": "p2", "person_b": "p13", "type": "overlap", "context": "市长与副市长/公安局长工作关系", "overlap_org": "古交市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # 市人大与市委领导
    {"person_a": "p1", "person_b": "p14", "type": "overlap", "context": "市委书记与市人大常委会主任", "overlap_org": "古交市", "overlap_period": "至今", "confidence": "confirmed"},
    # 市政协与市委领导
    {"person_a": "p1", "person_b": "p15", "type": "overlap", "context": "市委书记与市政协主席", "overlap_org": "古交市", "overlap_period": "至今", "confidence": "confirmed"},
    # 刘锦春 → 尖草坪区 (跨区调动)
    {"person_a": "p18", "person_b": "p1", "type": "predecessor_successor", "context": "刘锦春调任尖草坪区委书记后李卫雁接任", "overlap_org": "古交市人民政府/中共古交市委", "overlap_period": "", "confidence": "plausible"},
]


# =========================================================================
# Database Build
# =========================================================================

def build():
    """Run database + GEXF build."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""), p.get("notes", ""))
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", "present"),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""),
             r.get("confidence", "unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ────────────────────────────────────────────────────────────

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color_and_size(post):
        if "市委书记" in post and "副" not in post and "前任" not in post:
            return ("255,50,50", 20.0)
        elif "市长" in post and "副" not in post and "前任" not in post:
            return ("50,100,255", 20.0)
        elif "市委副书记" in post:
            return ("50,100,255", 15.0)
        elif "纪委" in post or "监委" in post:
            return ("255,165,0", 12.0)
        elif "常委" in post and "副" in post:
            return ("100,150,255", 12.0)
        elif "常委" in post:
            return ("100,150,255", 12.0)
        elif "副" in post and ("市长" in post or "长" in post):
            return ("100,100,255", 12.0)
        elif "人大" in post:
            return ("200,255,255", 12.0)
        elif "政协" in post:
            return ("255,240,200", 12.0)
        elif "前任" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>古交市领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid_val = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        a = int(r["person_a"][1:])
        b = int(r["person_b"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")

    # ── Summary ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"古交市 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
