#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 黔西市 (Qianxi City), 毕节市, 贵州省.

Level: 县级市
Province: 贵州省
Parent city: 毕节市
Targets: 市委书记 & 市长
Task ID: guizhou_黔西市
Investigation date: 2026-08-05

Research sources (official 黔西市人民政府门户网 www.gzqianxi.gov.cn):
  - 政府领导·张治国简历: https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/202207/t20220705_75403292.html
  - 政府领导·尚金海:   https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/202408/t20240813_85382497.html
  - 政府领导·罗卫:     https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/202207/t20220705_75403301.html
  - 政府领导·廖帮贵:   https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/202408/t20240816_85396903.html
  - 政府领导·罗坤:     https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/202207/t20220705_75403300.html
  - 政府领导·张达春:   https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/202512/t20251229_89097676.html
  - 政府领导·丁润朋:   https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/202408/t20240815_85391728.html
  - 政务公开·政府领导栏: https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/

  - 市委常委会（扩大）会议 2026-07-17: https://www.gzqianxi.gov.cn/xxfb/qxyw2022/202607/t20260717_90635071.html
      (市委书记陈华主持人; 市委副书记、市长张治国出席)
  - 市委常委会（扩大）会议 2026-06-29: https://www.gzqianxi.gov.cn/xxfb/qxyw2022/202606/t20260629_90565325.html
  - 民建中央到黔西开展专题调研 2026-07-24: https://www.gzqianxi.gov.cn/xxfb/qxyw2022/202607/t20260724_90656793.html
  - 张治国主持召开市政府党组会议及市政府常务会议 2026-07-08: https://www.gzqianxi.gov.cn/zwgk2022/zwhy/dej/202607/t20260708_90596694.html
  - 黔西市第二届人民政府常务会议 (第124-126次) 2026-06-24: https://www.gzqianxi.gov.cn/zwgk2022/zwhy/dej/202606/t20260624_90550917.html
  - 前任市长朱宇翔 主持第二届政府常务会议(2022): https://www.gzqianxi.gov.cn/zwgk2022/zwhy/dej/202304/t20230404_78885855.html

Confidence notes:
  - 市委书记 陈华: confirmed (现任, 主持市委常委会讲话 at 2+ official 市委常委会 news 2026-06/07).
    Full biography (birth, education, prior posts) NOT found on public portal — open gap.
  - 市长 张治国: confirmed via official 领导之窗 bio page (1978-12, 汉族, 大学, 中共党员) + multiple news.
  - 市政府 6 名副市长: all confirmed via official 领导之窗 bio pages (bios with birth/ethnicity/education).
  - 前任市长 朱宇翔: confirmed via 2022-2023 政府常务会议记录; successor 张治国.
  - 李守跃/熊强 (市委副书记), 蒙敏 (人大主任), 余刚跃 (政协主席), 丁现利 (统战部长): confirmed via official 市委常委会/调研 news.
  - 前任市委书记、朱宇翔去向: NOT found (search engines degraded) — open gap.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "黔西市"
TODAY = datetime.now().strftime("%Y%m%d")

# DB + GEXF written into the current directory (staging when run from data/tmp)
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ 市委主要领导（一把手／二把手）═══════
    {
        "id": 1,
        "name": "陈华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共黔西市委书记",
        "current_org": "中共黔西市委",
        "source": "https://www.gzqianxi.gov.cn/xxfb/qxyw2022/202607/t20260717_90635071.html; https://www.gzqianxi.gov.cn/xxfb/qxyw2022/202606/t20260629_90565323.html"
    },
    {
        "id": 2,
        "name": "张治国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔西市委副书记、市人民政府市长、党组书记；贵州黔西经济开发区管委会主任（兼）",
        "current_org": "黔西市人民政府",
        "source": "https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/202207/t20220705_75403292.html"
    },
    # ═══════ 市委副书记 ═══════
    {
        "id": 3,
        "name": "李守跃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔西市委副书记",
        "current_org": "中共黔西市委",
        "source": "https://www.gzqianxi.gov.cn/xxfb/qxyw2022/202607/t20260717_90635071.html"
    },
    {
        "id": 4,
        "name": "熊强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔西市委副书记",
        "current_org": "中共黔西市委",
        "source": "https://www.gzqianxi.gov.cn/xxfb/qxyw2022/202607/t20260717_90635071.html"
    },
    # ═══════ 市政府领导班子 ═══════
    {
        "id": 5,
        "name": "尚金海",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1985年10月",
        "birthplace": "",
        "education": "大学文化",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔西市委常委、副市长（分管常务工作）",
        "current_org": "黔西市人民政府",
        "source": "https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/202408/t20240813_85382497.html"
    },
    {
        "id": 6,
        "name": "罗卫",
        "gender": "女",
        "ethnicity": "彝族",
        "birth": "1982年07月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔西市委常委、副市长",
        "current_org": "黔西市人民政府",
        "source": "https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/202207/t20220705_75403301.html"
    },
    {
        "id": 7,
        "name": "廖帮贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔西市人民政府副市长",
        "current_org": "黔西市人民政府",
        "source": "https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/202408/t20240816_85396903.html"
    },
    {
        "id": 8,
        "name": "罗坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年07月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中国民主同盟盟员",
        "work_start": "",
        "current_post": "黔西市人民政府副市长",
        "current_org": "黔西市人民政府",
        "source": "https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/202207/t20220705_75403300.html"
    },
    {
        "id": 9,
        "name": "张达春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年5月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔西市人民政府党组成员、副市长，市公安局党委书记、局长",
        "current_org": "黔西市公安局",
        "source": "https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/202512/t20251229_89097676.html"
    },
    {
        "id": 10,
        "name": "丁润朋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年8月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔西市人民政府副市长",
        "current_org": "黔西市人民政府",
        "source": "https://www.gzqianxi.gov.cn/zwgk2022/zwgk_zfld/202408/t20240815_85391728.html"
    },
    # ═══════ 四套班子 ═══════
    {
        "id": 11,
        "name": "蒙敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔西市人大常委会主任",
        "current_org": "黔西市人大常委会",
        "source": "https://www.gzqianxi.gov.cn/xxfb/qxyw2022/202607/t20260717_90635071.html"
    },
    {
        "id": 12,
        "name": "余刚跃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政协黔西市委员会主席",
        "current_org": "政协黔西市委员会",
        "source": "https://www.gzqianxi.gov.cn/xxfb/qxyw2022/202607/t20260717_90635071.html; https://www.gzqianxi.gov.cn/xxfb/qxyw2022/202607/t20260724_90656793.html"
    },
    {
        "id": 13,
        "name": "丁现利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔西市委常委、市委统战部部长",
        "current_org": "中共黔西市委",
        "source": "https://www.gzqianxi.gov.cn/xxfb/qxyw2022/202607/t20260724_90656793.html"
    },
    # ═══════ 前任市长 ═══════
    {
        "id": 14,
        "name": "朱宇翔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔西市原市委副书记、市长",
        "current_org": "黔西市人民政府",
        "source": "https://www.gzqianxi.gov.cn/zwgk2022/zwhy/dej/202304/t20230404_78885855.html"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共黔西市委", "type": "党委", "level": "县级", "parent": "中共毕节市委", "location": "毕节市黔西市"},
    {"id": 2, "name": "黔西市人民政府", "type": "政府", "level": "县级", "parent": "毕节市人民政府", "location": "毕节市黔西市"},
    {"id": 3, "name": "黔西市公安局", "type": "政府", "level": "县级", "parent": "黔西市人民政府", "location": "毕节市黔西市"},
    {"id": 4, "name": "黔西市人大常委会", "type": "人大", "level": "县级", "parent": "毕节市人大常委会", "location": "毕节市黔西市"},
    {"id": 5, "name": "政协黔西市委员会", "type": "政协", "level": "县级", "parent": "政协毕节市委员会", "location": "毕节市黔西市"},
    {"id": 6, "name": "中共黔西市委统战部", "type": "党委", "level": "县级", "parent": "中共黔西市委", "location": "毕节市黔西市"},
    {"id": 7, "name": "贵州黔西经济开发区", "type": "开发区", "level": "县级", "parent": "黔西市人民政府", "location": "毕节市黔西市"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 陈华 — 市委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共黔西市委书记", "start": "", "end": "present", "rank": "正处级",
     "note": "主持市委全面工作。2026年6月26日、7月17日两次主持召开市委常委会（扩大）会议，传达学习中央、省和毕节市精神，研究部署城市更新、民生信访、防溺水、东西部协作及党建等工作。"},
    # 张治国 — 市长
    {"id": 2, "person_id": 2, "org_id": 1, "title": "黔西市委副书记、市人民政府党组书记", "start": "", "end": "present", "rank": "正处级",
     "note": "兼任市政府党组书记，主持市政府党组会议及市政府常务会议（2026-07-08）。"},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "黔西市人民政府市长", "start": "", "end": "present", "rank": "正处级",
     "note": "领导市政府全面工作，负责审计、粮食方面工作，分管市审计局。"},
    {"id": 4, "person_id": 2, "org_id": 7, "title": "贵州黔西经济开发区管委会主任（兼）", "start": "", "end": "present", "rank": "兼",
     "note": "兼任经开区管委会主任，统筹园区开发建设。"},
    # 市委副书记
    {"id": 5, "person_id": 3, "org_id": 1, "title": "黔西市委副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "2026年6/7月市委常委会出席名单列为市委副书记。"},
    {"id": 6, "person_id": 4, "org_id": 1, "title": "黔西市委副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "2026年6/7月市委常委会出席名单列为市委副书记。"},
    # 市政府领导班子
    {"id": 7, "person_id": 5, "org_id": 2, "title": "黔西市委常委、副市长（分管常务工作）", "start": "", "end": "present", "rank": "副处级",
     "note": "负责市政府常务工作及发改、财政、统计、应急、国资、税务金融等，协助市长分管审计、粮食。"},
    {"id": 8, "person_id": 6, "org_id": 2, "title": "黔西市委常委、副市长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责教育、卫生健康、医疗保障、民族宗教、文史等。"},
    {"id": 9, "person_id": 7, "org_id": 2, "title": "黔西市人民政府副市长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责能源、煤矿安全生产、电力建设，分管市能源局。"},
    {"id": 10, "person_id": 8, "org_id": 2, "title": "黔西市人民政府副市长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责自然资源、住建、征地拆迁、城市管理、生态环保，主抓新型城镇化。"},
    {"id": 11, "person_id": 9, "org_id": 2, "title": "黔西市人民政府党组成员、副市长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责公安、国安、司法、退役军人事务，主持市公安局全面工作。"},
    {"id": 12, "person_id": 9, "org_id": 3, "title": "黔西市公安局党委书记、局长", "start": "", "end": "present", "rank": "副处级",
     "note": "主持市公安局全面工作。"},
    {"id": 13, "person_id": 10, "org_id": 2, "title": "黔西市人民政府副市长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责工业、商贸、交通、市场监管、招商引资、文体广电旅游，主抓新型工业化和旅游产业化。"},
    # 四套班子
    {"id": 14, "person_id": 11, "org_id": 4, "title": "黔西市人大常委会主任", "start": "", "end": "present", "rank": "正处级",
     "note": "2026年7月市委常委会出席。"},
    {"id": 15, "person_id": 12, "org_id": 5, "title": "政协黔西市委员会主席", "start": "", "end": "present", "rank": "正处级",
     "note": "2026年7月市委常委会及民建中央调研陪同出席。"},
    {"id": 16, "person_id": 13, "org_id": 6, "title": "黔西市委常委、统战部部长", "start": "", "end": "present", "rank": "副处级",
     "note": "2026-07-22 民建中央调研陪同领导之一。"},
    # 前任市长
    {"id": 17, "person_id": 14, "org_id": 2, "title": "黔西市原市委副书记、市人民政府市长", "start": "", "end": "2023年前后", "rank": "正处级",
     "note": "2022年在任期间多次主持召开市第二届人民政府常务会议；后由张治国接任市长（其去向待查）。"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "市委书记陈华与市长张治国党政正职搭档，多次共同出席市委常委会（2026-06-26、07-17），陈华主持并讲话、张治国出席。",
     "overlap_org": "中共黔西市委/黔西市人民政府", "overlap_period": "2026"},
    {"id": 2, "person_a": 1, "person_b": 3, "type": "上下级",
     "context": "市委书记领导市委副书记李守跃，同台出席市委常委会。", "overlap_org": "中共黔西市委", "overlap_period": "2026"},
    {"id": 3, "person_a": 1, "person_b": 4, "type": "上下级",
     "context": "市委书记领导市委副书记熊強（同台出席市委常委会）。", "overlap_org": "中共黔西市委", "overlap_period": "2026"},
    {"id": 4, "person_a": 1, "person_b": 5, "type": "上下级",
     "context": "市委书记领导市委常委、常务副市长尚金海（市政府班子属市委领导）。", "overlap_org": "中共黔西市委/黔西市政府", "overlap_period": "2026"},
    {"id": 5, "person_a": 1, "person_b": 13, "type": "上下级",
     "context": "市委书记领导市委常委、统战部长丁现利。", "overlap_org": "中共黔西市委", "overlap_period": "2026"},
    {"id": 6, "person_a": 1, "person_b": 11, "type": "同级协作",
     "context": "市委书记与市人大常委会主任蒙敏同台出席市委常委会。", "overlap_org": "黔西市四套班子", "overlap_period": "2026"},
    {"id": 7, "person_a": 1, "person_b": 12, "type": "同级协作",
     "context": "市委书记与市政协主席余刚跃同台出席市委常委会及民建中央调研接待。", "overlap_org": "黔西市四套班子", "overlap_period": "2026"},
    {"id": 8, "person_a": 2, "person_b": 5, "type": "上下级",
     "context": "市长领导常务副市长尚金宝（协助市长分管审计、粮食，负责常务口）。", "overlap_org": "黔西市人民政府", "overlap_period": "2026"},
    {"id": 9, "person_a": 2, "person_b": 6, "type": "上下级",
     "context": "市长领导副市长罗卫（分管教育卫生文旅口）。", "overlap_org": "黔西市人民政府", "overlap_period": "2026"},
    {"id": 10, "person_a": 2, "person_b": 7, "type": "上下级",
     "context": "市长领导副市长廖帮贵（能源口）。", "overlap_org": "黔西市人民政府", "overlap_period": "2026"},
    {"id": 11, "person_a": 2, "person_b": 8, "type": "上下级",
     "context": "市长领导副市长罗坤（住建、自然资源口）。", "overlap_org": "黔西市人民政府", "overlap_period": "2026"},
    {"id": 12, "person_a": 2, "person_b": 9, "type": "上下级",
     "context": "市长领导副市长、公安局长张达春（公安、司法口）。", "overlap_org": "黔西市人民政府/公安局", "overlap_period": "2026"},
    {"id": 13, "person_a": 2, "person_b": 10, "type": "上下级",
     "context": "市长领导副市长丁润朋，丁润朋协助张治国联系贵州黔西经开区工作。", "overlap_org": "黔西市人民政府", "overlap_period": "2026"},
    {"id": 14, "person_a": 2, "person_b": 14, "type": "前任后继",
     "context": "朱宇翔曾任黔西市长，张治国接任市长（党政交接）。", "overlap_org": "黔西市人民政府", "overlap_period": "2022-2023"},
    {"id": 15, "person_a": 12, "person_b": 13, "type": "同级协作",
     "context": "市政协主席余刚跃与统战部长丁现利害同于民建中央黔西调研时陪同。", "overlap_org": "黔西统一战线/市政协", "overlap_period": "2026-07"},
]

# ── SQLite Build ───────────────────────────────────────────────────────────
conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()
conn.executescript("""
    DROP TABLE IF EXISTS relationships;
    DROP TABLE IF EXISTS positions;
    DROP TABLE IF EXISTS organizations;
    DROP TABLE IF EXISTS persons;

    CREATE TABLE persons (
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

    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT DEFAULT '',
        level TEXT DEFAULT '',
        parent TEXT DEFAULT '',
        location TEXT DEFAULT ''
    );

    CREATE TABLE positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        start TEXT DEFAULT '',
        end TEXT DEFAULT '',
        rank TEXT DEFAULT '',
        note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );

    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY,
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

for p in persons:
    cur.execute(
        "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
         p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
    )
for o in organizations:
    cur.execute(
        "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
    )
for pos in positions:
    cur.execute(
        "INSERT INTO positions (id, person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (pos["id"], pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"])
    )
for r in relationships:
    cur.execute(
        "INSERT INTO relationships (id, person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (r["id"], r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
    )
conn.commit()

# ── GEXF Generation ────────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' for person node color by role."""
    cur_post = p.get("current_post", "")
    if "书记" in cur_post and "市委" in cur_post:
        return "255,50,50"      # 红：市委书记
    if "市长" in cur_post:
        return "50,100,255"     # 蓝：政府正职
    if "副市长" in cur_post or "政府" in cur_post:
        return "50,100,255"     # 蓝：政府领导
    if "统战" in cur_post:
        return "255,165,0"      # 橙：统战/纪律口
    return "100,100,100"        # 灰：其他


def org_color(o):
    """Return node color for organization node by type."""
    t = o.get("type", "")
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "开发区":
        return "200,255,200"
    if t == "人大":
        return "200,255,255"
    if t == "政协":
        return "255,240,200"
    return "200,200,200"


def is_top_leader(p):
    return p.get("id") in (1, 2)  # 市委书记 and 市长

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{TODAY}">')
lines.append('    <creator>Claude Research Agent</creator>')
lines.append(f'    <description>{esc(SLUG + " 领导班子工作关系网络（市委书记 & 市长调查）")}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="current_post" type="string"/>')
lines.append('      <attribute id="2" title="current_org" type="string"/>')
lines.append('    </attributes>')

lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

conn.close()

# ── Summary ────────────────────────────────────────────────────────────────
print(f"黔西市 network build complete.")
print(f"  Database:        {DB_PATH} ({DB_PATH.stat().st_size / 1024:.1f} KB)")
print(f"  GEXF:            {GEXF_PATH} ({GEXF_PATH.stat().st_size / 1024:.1f} KB)")
print(f"  Persons:         {len(persons)}")
print(f"  Organizations:   {len(organizations)}")
print(f"  Positions:       {len(positions)}")
print(f"  Relationships:   {len(relationships)}")
print()
print("Confidence notes:")
print("  - 陈华 (市委书记): confirmed via official 市委常委会 news; full bio/gap")
print("  - 张治国 (市长):     confirmed via official 领导之窗 bio + news")
print("  - 前任市长朱宇翔、市委副书记、人大/政协主任: confirmed via official news")