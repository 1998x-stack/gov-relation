#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 黄石港区 (Huangshigang District, 黄石市, 湖北省) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/黄石港区_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/黄石港区_network.gexf")

# ── DATA ────────────────────────────────────────────────────────────────────

persons = [
    # ── District Party Committee Leaders ──
    {"id": 1, "name": "冯雨", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区委书记", "current_org": "中共黄石港区委员会",
     "source": "https://www.huangshigang.gov.cn/jjhsg/202607/t20260720_1344412.html"},
    {"id": 2, "name": "李冠男", "gender": "男", "ethnicity": "汉族",
     "birth": "1987-01", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区委副书记、代理区长", "current_org": "黄石港区人民政府",
     "source": "https://www.huangshigang.gov.cn/zwpd/fdzdgknr/ldzc/202108/t20210820_827346.html"},
    {"id": 3, "name": "刘辉", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区委常委、组织部部长", "current_org": "中共黄石港区委员会",
     "source": "https://www.huangshigang.gov.cn/jjhsg/202607/t20260702_1339508.html"},
    {"id": 4, "name": "彭华云", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区委常委、纪委书记、监委主任", "current_org": "中共黄石港区纪律检查委员会",
     "source": "https://www.huangshigang.gov.cn/jjhsg/202606/t20260612_1334915.html"},
    {"id": 5, "name": "黄方", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区委常委、统战部部长", "current_org": "中共黄石港区委员会",
     "source": "https://www.huangshigang.gov.cn/jjhsg/202606/t20260610_1334357.html"},

    # ── District Government Leaders ──
    {"id": 6, "name": "凡后美", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-04", "birthplace": "", "education": "大学学历、农学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区副区长", "current_org": "黄石港区人民政府",
     "source": "https://www.huangshigang.gov.cn/zwpd/fdzdgknr/ldzc/202108/t20210809_822520.html"},
    {"id": 7, "name": "柳长文", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-03", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区副区长", "current_org": "黄石港区人民政府",
     "source": "https://www.huangshigang.gov.cn/zwpd/fdzdgknr/ldzc/202008/t20200831_685026.html"},
    {"id": 8, "name": "秦志刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-05", "birthplace": "", "education": "",
     "party_join": "民建会员", "work_start": "",
     "current_post": "黄石港区副区长", "current_org": "黄石港区人民政府",
     "source": "https://www.huangshigang.gov.cn/zwpd/fdzdgknr/ldzc/202110/t20211014_842971.html"},
    {"id": 9, "name": "周邦松", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-01", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区副区长", "current_org": "黄石港区人民政府",
     "source": "https://www.huangshigang.gov.cn/zwpd/fdzdgknr/ldzc/202201/t20220110_869958.html"},
    {"id": 10, "name": "崔岩", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-10", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区副区长", "current_org": "黄石港区人民政府",
     "source": "https://www.huangshigang.gov.cn/zwpd/fdzdgknr/ldzc/202408/t20240828_1145901.html"},
    {"id": 11, "name": "马思远", "gender": "男", "ethnicity": "汉族",
     "birth": "1994-08", "birthplace": "", "education": "工学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区政府党组成员（挂职）、工业园区党工委副书记", "current_org": "黄石港区人民政府",
     "source": "https://www.huangshigang.gov.cn/zwpd/fdzdgknr/ldzc/202408/t20240828_1145891.html"},

    # ── District People's Congress & Political Consultative Conference ──
    {"id": 12, "name": "陆英", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区人大常委会党组书记、主任", "current_org": "黄石港区人民代表大会常务委员会",
     "source": "https://www.huangshigang.gov.cn/jjhsg/202607/t20260702_1339508.html"},
    {"id": 13, "name": "彭建佳", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "黄石港区人大常委会副主任", "current_org": "黄石港区人民代表大会常务委员会",
     "source": "https://www.huangshigang.gov.cn/zwpd/fdzdgknr/rsxx/202412/t20241230_1179405.html"},
    {"id": 14, "name": "黄铮", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区政协党组书记、主席", "current_org": "中国人民政治协商会议黄石港区委员会",
     "source": "https://www.huangshigang.gov.cn/jjhsg/202607/t20260720_1344412.html"},
    {"id": 15, "name": "叶宇", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "黄石港区人民法院院长", "current_org": "黄石港区人民法院",
     "source": "https://www.huangshigang.gov.cn/zwpd/fdzdgknr/rsxx/202412/t20241230_1179407.html"},

    # ── Other District Leaders (identified in news, exact posts TBD) ──
    {"id": 16, "name": "朱兴国", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区领导", "current_org": "中共黄石港区委员会",
     "source": "https://www.huangshigang.gov.cn/jjhsg/202606/t20260612_1334915.html"},
    {"id": 17, "name": "余正江", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区领导", "current_org": "中共黄石港区委员会",
     "source": "https://www.huangshigang.gov.cn/jjhsg/202606/t20260610_1334357.html"},
    {"id": 18, "name": "鞠成伟", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区领导", "current_org": "中共黄石港区委员会",
     "source": "https://www.huangshigang.gov.cn/jjhsg/202606/t20260610_1334357.html"},
    {"id": 19, "name": "方英明", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄石港区领导", "current_org": "中共黄石港区委员会",
     "source": "https://www.huangshigang.gov.cn/jjhsg/202606/t20260610_1334357.html"},

    # ── Predecessors ──
    {"id": 20, "name": "王永桂", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原黄石港区副区长（已免）", "current_org": "",
     "source": "https://www.huangshigang.gov.cn/zwpd/fdzdgknr/rsxx/"},
    {"id": 21, "name": "严华", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原黄石港区副区长（已辞职）", "current_org": "",
     "source": "https://www.huangshigang.gov.cn/zwpd/fdzdgknr/rsxx/"},
    {"id": 22, "name": "宁海", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原黄石港区副区长（已调离）", "current_org": "",
     "source": "https://www.huangshigang.gov.cn/zwpd/fdzdgknr/rsxx/"},
    {"id": 23, "name": "徐新勇", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原黄石港区副区长（已调离）", "current_org": "",
     "source": "https://www.huangshigang.gov.cn/zwpd/fdzdgknr/rsxx/"},
]

organizations = [
    {"id": 1, "name": "中共黄石港区委员会", "type": "党委", "level": "县级", "parent": "中共黄石市委员会", "location": "黄石港区"},
    {"id": 2, "name": "黄石港区人民政府", "type": "政府", "level": "县级", "parent": "黄石市人民政府", "location": "黄石港区"},
    {"id": 3, "name": "中共黄石港区纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共黄石市纪律检查委员会", "location": "黄石港区"},
    {"id": 4, "name": "黄石港区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "黄石市人民代表大会常务委员会", "location": "黄石港区"},
    {"id": 5, "name": "中国人民政治协商会议黄石港区委员会", "type": "政协", "level": "县级", "parent": "中国人民政治协商会议黄石市委员会", "location": "黄石港区"},
    {"id": 6, "name": "黄石港区人民法院", "type": "事业单位", "level": "县级", "parent": "黄石市中级人民法院", "location": "黄石港区"},
    {"id": 7, "name": "黄石港区人民检察院", "type": "事业单位", "level": "县级", "parent": "黄石市人民检察院", "location": "黄石港区"},
    {"id": 8, "name": "湖北黄石港工业园区（江北管理区）", "type": "开发区", "level": "县级", "parent": "黄石港区人民政府", "location": "黄石港区"},
    {"id": 9, "name": "中共阳新县委员会", "type": "党委", "level": "县级", "parent": "中共黄石市委员会", "location": "阳新县"},
    {"id": 10, "name": "阳新县人民政府", "type": "政府", "level": "县级", "parent": "黄石市人民政府", "location": "阳新县"},
]

positions = [
    # 冯雨
    {"person_id": 1, "org_id": 1, "title": "黄石港区委书记",
     "start": "2024-12", "end": "present", "rank": "正县级", "note": "此前曾兼任区长至2026年5月"},
    {"person_id": 1, "org_id": 2, "title": "黄石港区区长（原兼任）",
     "start": "", "end": "2026-05", "rank": "正县级", "note": "已卸任区长，保留区委书记"},

    # 李冠男
    {"person_id": 2, "org_id": 2, "title": "黄石港区副区长、代理区长",
     "start": "2026-06", "end": "present", "rank": "正县级", "note": "2026年6月12日区人大常委会任命"},
    {"person_id": 2, "org_id": 1, "title": "黄石港区委副书记",
     "start": "2026-06", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "阳新县委副书记",
     "start": "", "end": "2026-05", "rank": "副县级", "note": "调任黄石港区前任阳新县委副书记"},

    # 刘辉
    {"person_id": 3, "org_id": 1, "title": "黄石港区委常委、组织部部长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 彭华云
    {"person_id": 4, "org_id": 3, "title": "黄石港区委常委、纪委书记、监委主任",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "黄石港区委常委",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 黄方
    {"person_id": 5, "org_id": 1, "title": "黄石港区委常委、统战部部长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 凡后美
    {"person_id": 6, "org_id": 2, "title": "黄石港区副区长",
     "start": "2025-10", "end": "present", "rank": "副县级", "note": "2025年10月29日任命，接替严华"},
    {"person_id": 6, "org_id": 2, "title": "黄石港区政府党组成员",
     "start": "2025-10", "end": "present", "rank": "副县级", "note": ""},

    # 柳长文
    {"person_id": 7, "org_id": 2, "title": "黄石港区副区长",
     "start": "2025-04", "end": "present", "rank": "副县级", "note": "2025年4月任命"},
    {"person_id": 7, "org_id": 2, "title": "黄石港区政府党组成员",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 秦志刚
    {"person_id": 8, "org_id": 2, "title": "黄石港区副区长",
     "start": "", "end": "present", "rank": "副县级", "note": "民建会员，非中共党员"},

    # 周邦松
    {"person_id": 9, "org_id": 2, "title": "黄石港区副区长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "黄石港区政府党组成员",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 崔岩
    {"person_id": 10, "org_id": 2, "title": "黄石港区副区长",
     "start": "2024-08", "end": "present", "rank": "副县级", "note": "2024年8月任命"},
    {"person_id": 10, "org_id": 2, "title": "黄石港区政府党组成员",
     "start": "2024-08", "end": "present", "rank": "副县级", "note": ""},

    # 马思远
    {"person_id": 11, "org_id": 8, "title": "湖北黄石港工业园区党工委副书记、副主任（挂职）",
     "start": "2024-08", "end": "present", "rank": "挂职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "黄石港区政府党组成员（挂职）",
     "start": "2024-08", "end": "present", "rank": "挂职", "note": ""},

    # 陆英
    {"person_id": 12, "org_id": 4, "title": "黄石港区人大常委会党组书记、主任",
     "start": "", "end": "present", "rank": "正县级", "note": ""},

    # 彭建佳
    {"person_id": 13, "org_id": 4, "title": "黄石港区人大常委会副主任",
     "start": "2024-12", "end": "present", "rank": "副县级", "note": "2024年12月27日选举"},

    # 黄铮
    {"person_id": 14, "org_id": 5, "title": "黄石港区政协党组书记、主席",
     "start": "", "end": "present", "rank": "正县级", "note": ""},

    # 叶宇
    {"person_id": 15, "org_id": 6, "title": "黄石港区人民法院院长",
     "start": "2024-12", "end": "present", "rank": "副县级", "note": "2024年12月27日选举"},

    # 王永桂（前任副区长，已免）
    {"person_id": 20, "org_id": 2, "title": "黄石港区副区长",
     "start": "", "end": "2026-06", "rank": "副县级", "note": "2026年6月12日免职"},

    # 严华（前任副区长，已辞职）
    {"person_id": 21, "org_id": 2, "title": "黄石港区副区长",
     "start": "", "end": "2025-10", "rank": "副县级", "note": "2025年10月辞职"},

    # 宁海（前任副区长，已调离）
    {"person_id": 22, "org_id": 2, "title": "黄石港区副区长",
     "start": "", "end": "2025-04", "rank": "副县级", "note": "2025年4月因工作变动调离"},

    # 徐新勇（前任副区长，已调离）
    {"person_id": 23, "org_id": 2, "title": "黄石港区副区长",
     "start": "", "end": "2025-06", "rank": "副县级", "note": "2025年6月调离"},
]

relationships = [
    # 上下级关系
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "冯雨为区委书记，李冠男为区委副书记、代理区长，直接上下级",
     "overlap_org": "中共黄石港区委员会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "冯雨为区委书记，刘辉为区委常委、组织部部长",
     "overlap_org": "中共黄石港区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "冯雨为区委书记，彭华云为区委常委、纪委书记",
     "overlap_org": "中共黄石港区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "冯雨为区委书记，黄方为区委常委、统战部部长",
     "overlap_org": "中共黄石港区委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "李冠男（代理区长）与凡后美（副区长）政府上下级",
     "overlap_org": "黄石港区人民政府", "overlap_period": "2025-10至今"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "李冠男（代理区长）与柳长文（副区长）政府上下级",
     "overlap_org": "黄石港区人民政府", "overlap_period": "2025-04至今"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "李冠男（代理区长）与秦志刚（副区长）政府上下级",
     "overlap_org": "黄石港区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "李冠男（代理区长）与周邦松（副区长）政府上下级",
     "overlap_org": "黄石港区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "李冠男（代理区长）与崔岩（副区长）政府上下级",
     "overlap_org": "黄石港区人民政府", "overlap_period": "2024-08至今"},

    # 跨区调任关系
    {"person_a": 2, "person_b": 0, "type": "predecessor_successor",
     "context": "李冠男从阳新县委副书记调任黄石港区代理区长——跨县区交流",
     "overlap_org": "阳新县→黄石港区", "overlap_period": "2026-06"},

    # 前任-继任关系
    {"person_a": 20, "person_b": 2, "type": "predecessor_successor",
     "context": "王永桂免职后李冠男任代理区长",
     "overlap_org": "黄石港区人民政府", "overlap_period": "2026-06"},
    {"person_a": 21, "person_b": 6, "type": "predecessor_successor",
     "context": "严华辞职后凡后美接任副区长",
     "overlap_org": "黄石港区人民政府", "overlap_period": "2025-10"},
    {"person_a": 22, "person_b": 7, "type": "predecessor_successor",
     "context": "宁海调离后柳长文任副区长（时间接近）",
     "overlap_org": "黄石港区人民政府", "overlap_period": "2025-04"},
    {"person_a": 23, "person_b": 10, "type": "predecessor_successor",
     "context": "徐新勇调离后崔岩任副区长（时间接近）",
     "overlap_org": "黄石港区人民政府", "overlap_period": "2024-08"},

    # 同部门同级关系
    {"person_a": 6, "person_b": 7, "type": "overlap",
     "context": "同为副区长",
     "overlap_org": "黄石港区人民政府", "overlap_period": "2025-10至今"},
    {"person_a": 6, "person_b": 8, "type": "overlap",
     "context": "同为副区长",
     "overlap_org": "黄石港区人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 9, "type": "overlap",
     "context": "同为副区长",
     "overlap_org": "黄石港区人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 10, "type": "overlap",
     "context": "同为副区长",
     "overlap_org": "黄石港区人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "同为区委常委班子成员",
     "overlap_org": "中共黄石港区委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "同为区委常委班子成员",
     "overlap_org": "中共黄石港区委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "同为区委常委班子成员",
     "overlap_org": "中共黄石港区委员会", "overlap_period": ""},
]

# ── BUILD FUNCTIONS ─────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
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
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    conn.commit()

def person_color(p):
    """Return GEXF color string based on person's role."""
    post = p.get("current_post", "")
    if "区委书记" in post:
        return "255,50,50"
    elif any(x in post for x in ["区长", "代理区长"]):
        return "50,100,255"
    elif "纪委书记" in post:
        return "255,165,0"
    elif any(x in post for x in ["副区长", "政府党组成员"]):
        return "50,100,255"
    elif "人大" in post:
        return "200,255,255"
    elif "政协" in post:
        return "255,240,200"
    elif "法院" in post:
        return "220,220,220"
    else:
        return "100,100,100"

def is_top_leader(p):
    post = p.get("current_post", "")
    return ("区委书记" in post) or ("区长" in post) or ("代理区长" in post)

def build_gexf(persons_list, orgs_list, positions_list, relationships_list):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>黄石港区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="post" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - Persons
    lines.append('    <nodes>')
    for p in persons_list:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("12.0" if "领导" not in p.get("current_post", "") or "常委" in p.get("current_post", "") else "12.0")
        if p.get("id", 0) >= 20:  # predecessors
            sz = "10.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - Organizations
    for o in orgs_list:
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="200" g="200" b="200"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person -> organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions_list:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start", ""))} - {esc(pos.get("end", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person <-> person
    for r in relationships_list:
        if r["person_b"] == 0:
            continue  # skip placeholder
        eid += 1
        w = "2.0" if r["type"] in ("superior_subordinate", "predecessor_successor") else "1.5"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    return "\n".join(lines)

# ── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print(f"Building database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    for p in persons:
        conn.execute(
            "INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p.get("current_post", ""), p.get("current_org", ""), p.get("source", ""))
        )

    # Insert organizations
    for o in organizations:
        conn.execute(
            "INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    # Insert positions
    for pos in positions:
        conn.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", ""),
             pos.get("rank", ""), pos.get("note", ""))
        )

    # Insert relationships
    for r in relationships:
        if r["person_b"] == 0:
            continue
        conn.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""))
        )

    conn.commit()
    conn.close()

    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len([r for r in relationships if r['person_b'] != 0])}")

    # Build GEXF
    print(f"\nBuilding GEXF: {GEXF_PATH}")
    gexf_content = build_gexf(persons, organizations, positions, relationships)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write(gexf_content)
    print("  Done.")

    # Summary table
    print("\n── Key Personnel ──")
    for p in persons:
        if p["id"] <= 19 and is_top_leader(p):
            print(f"  {p['name']} — {p['current_post']} ({p.get('birth', '?')})")
    print("\n── Standing Committee (confirmed) ──")
    for p in persons:
        if p["id"] <= 5:
            print(f"  {p['name']} — {p['current_post']}")
    print("\n── Vice District Chiefs ──")
    for p in persons:
        if 6 <= p["id"] <= 11:
            print(f"  {p['name']} — {p['current_post']} ({p.get('birth', '?')})")
    print("\n── Congress & Political Consultative ──")
    for p in persons:
        if 12 <= p["id"] <= 15:
            print(f"  {p['name']} — {p['current_post']}")

if __name__ == "__main__":
    main()
