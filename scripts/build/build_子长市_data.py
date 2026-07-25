#!/usr/bin/env python3
"""Build 子长市 leadership network — SQLite DB + GEXF graph."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Output paths ──────────────────────────────────────────────────────────────
DB_PATH = DATABASE_DIR / "子长市_network.db"
GEXF_PATH = GRAPH_DIR / "子长市_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
PERSONS = [
    # ── Top leaders ──
    {
        "id": 1,
        "name": "王诚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共子长市委员会",
        "source": "子长市人民政府官网新闻 (2026-07-22); 子长市本地要闻 (2026-07-17)",
    },
    {
        "id": 2,
        "name": "高晓斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-10",
        "birthplace": "陕西神木",
        "education": "研究生",
        "party_join": "2002-12",
        "work_start": "1998-10",
        "current_post": "市委副书记、市长",
        "current_org": "子长市人民政府",
        "source": "https://www.zichang.gov.cn/zfxxgk/fdzdgknr/zfld/sc/cyj/1.html",
    },
    # ── Government Leaders ──
    {
        "id": 3,
        "name": "李茂胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-03",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "子长市人民政府",
        "source": "https://www.zichang.gov.cn/zfxxgk/fdzdgknr/zfld/fsc/lms/1.html",
    },
    {
        "id": 4,
        "name": "卢志华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-02",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "子长市人民政府",
        "source": "https://www.zichang.gov.cn/zfxxgk/fdzdgknr/zfld/fsc/lzh/1.html",
    },
    {
        "id": 5,
        "name": "余博龙",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1984-05",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长（挂职）",
        "current_org": "子长市人民政府",
        "source": "https://www.zichang.gov.cn/zfxxgk/fdzdgknr/zfld/fsc/ybl/1.html",
    },
    {
        "id": 6,
        "name": "任碧辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-09",
        "birthplace": "",
        "education": "在职研究生，经济管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "子长市人民政府",
        "source": "https://www.zichang.gov.cn/zfxxgk/fdzdgknr/zfld/fsc/rbh/1.html",
    },
    {
        "id": 7,
        "name": "李涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-01",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长、公安局局长",
        "current_org": "子长市公安局",
        "source": "https://www.zichang.gov.cn/zfxxgk/fdzdgknr/zfld/fsc/lt/1.html",
    },
    {
        "id": 8,
        "name": "刘建强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-11",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "子长市人民政府",
        "source": "https://www.zichang.gov.cn/zfxxgk/fdzdgknr/zfld/fsc/ljq/1.html",
    },
    {
        "id": 9,
        "name": "赵雁鸿",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973-08",
        "birthplace": "",
        "education": "研究生，经济管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "子长市人民政府",
        "source": "https://www.zichang.gov.cn/zfxxgk/fdzdgknr/zfld/fsc/zyh/1.html",
    },
    {
        "id": 10,
        "name": "陈伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-05",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长（挂职）",
        "current_org": "子长市人民政府",
        "source": "https://www.zichang.gov.cn/zfxxgk/fdzdgknr/zfld/fsc/cw/1.html",
    },
    # ── Standing Committee members (non-government) ──
    # Note: Party committee other than government cross-post members are not on gov site.
    # Typical county party standing committee includes: secretary, deputy secretary/mayor,
    # discipline secretary, organization head, propaganda head, united front head,
    # political-legal affairs head, and a few others.
    # The ones not yet covered above are marked as "待查" pending deeper research.
    {
        "id": 11,
        "name": "待查（纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、纪委书记、监委主任",
        "current_org": "中共子长市纪律检查委员会",
        "source": "未找到公开简历；需进一步搜索",
    },
    {
        "id": 12,
        "name": "待查（组织部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共子长市委组织部",
        "source": "未找到公开简历；需进一步搜索",
    },
    {
        "id": 13,
        "name": "待查（宣传部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共子长市委宣传部",
        "source": "未找到公开简历；需进一步搜索",
    },
    {
        "id": 14,
        "name": "待查（政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共子长市委政法委",
        "source": "未找到公开简历；需进一步搜索",
    },
    {
        "id": 15,
        "name": "待查（统战部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共子长市委统战部",
        "source": "未找到公开简历；需进一步搜索",
    },
    # ── Legislature & Consultative ──
    {
        "id": 16,
        "name": "待查（人大主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "子长市人大常委会",
        "source": "未找到公开简历；需进一步搜索",
    },
    {
        "id": 17,
        "name": "待查（政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "政协子长市委员会",
        "source": "未找到公开简历；需进一步搜索",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中共子长市委员会", "type": "党委", "level": "县级", "location": "陕西省延安市子长市"},
    {"id": 2, "name": "子长市人民政府", "type": "政府", "level": "县级", "location": "陕西省延安市子长市"},
    {"id": 3, "name": "中共子长市纪律检查委员会", "type": "党委", "level": "县级", "location": "陕西省延安市子长市"},
    {"id": 4, "name": "子长市监察委员会", "type": "党委", "level": "县级", "location": "陕西省延安市子长市"},
    {"id": 5, "name": "中共子长市委组织部", "type": "党委", "level": "县级", "location": "陕西省延安市子长市"},
    {"id": 6, "name": "中共子长市委宣传部", "type": "党委", "level": "县级", "location": "陕西省延安市子长市"},
    {"id": 7, "name": "中共子长市委政法委", "type": "党委", "level": "县级", "location": "陕西省延安市子长市"},
    {"id": 8, "name": "中共子长市委统战部", "type": "党委", "level": "县级", "location": "陕西省延安市子长市"},
    {"id": 9, "name": "子长市公安局", "type": "政府", "level": "县级", "location": "陕西省延安市子长市"},
    {"id": 10, "name": "子长市人大常委会", "type": "人大", "level": "县级", "location": "陕西省延安市子长市"},
    {"id": 11, "name": "政协子长市委员会", "type": "政协", "level": "县级", "location": "陕西省延安市子长市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
POSITIONS = [
    # 王诚 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正县级", "note": "current as of 2026-07"},
    # 高晓斌 — 市长
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "", "end": "present", "rank": "正县级", "note": "current as of 2026-07; last updated 2025-05-16"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "", "rank": "", "note": "prior to becoming mayor; was 子长市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "市政府党组书记", "start": "", "end": "present", "rank": "", "note": ""},
    # 高晓斌 earlier career
    {"person_id": 2, "org_id": 1, "title": "共青团延安市委书记、市青联主席", "start": "", "end": "", "rank": "", "note": "团市委时期"},
    {"person_id": 2, "org_id": 1, "title": "共青团延安市委办公室主任、副书记", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "共青团延安市委直属单位委员会书记、办公室主任", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "延安市财政局预算科副科长", "start": "", "end": "", "rank": "", "note": "earliest known position"},
    # 李茂胜 — 常务副市长
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start": "", "end": "present", "rank": "副县级", "note": "also 市政府党组副书记"},
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    # 李茂胜 previous roles
    {"person_id": 3, "org_id": 2, "title": "副县长/副市长", "start": "", "end": "", "rank": "", "note": "prior县级市副市长"},
    {"person_id": 3, "org_id": 1, "title": "乡镇党委书记", "start": "", "end": "", "rank": "", "note": "乡镇党委书记"},
    {"person_id": 3, "org_id": 2, "title": "县政府组成部门局长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "乡镇镇长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "乡镇人大主席", "start": "", "end": "", "rank": "", "note": ""},
    # 卢志华 — 市委常委、副市长
    {"person_id": 4, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "黄陵县委常委、纪委书记、监委主任", "start": "", "end": "", "rank": "", "note": "prior role"},
    {"person_id": 4, "org_id": 1, "title": "宝塔区委常委、统战部部长", "start": "", "end": "", "rank": "", "note": "prior role"},
    {"person_id": 4, "org_id": 1, "title": "中共普兰县委常委、副县长（援藏挂职）", "start": "", "end": "", "rank": "", "note": "陕西省委组织部选派援藏"},
    {"person_id": 4, "org_id": 1, "title": "宝塔区委常委", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "宝塔区桥沟镇主要领导", "start": "", "end": "", "rank": "", "note": "担任镇长/书记"},
    {"person_id": 4, "org_id": 2, "title": "宝塔区甘谷驿镇主要领导", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "宝塔区梁村乡主要领导", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "宝塔区委办公室机要秘书、副主任", "start": "", "end": "", "rank": "", "note": "early career"},
    # 余博龙 — 市委常委、副市长（挂职）
    {"person_id": 5, "org_id": 2, "title": "副市长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "挂职"},
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 9, "title": "国家矿山安全监察局政策法规和科技装备司发展规划处处长", "start": "", "end": "", "rank": "正处级", "note": "prior role in central government"},
    {"person_id": 5, "org_id": 9, "title": "煤炭科学技术研究院有限公司装备分院副院长", "start": "", "end": "", "rank": "", "note": "prior role"},
    # 任碧辉 — 副市长
    {"person_id": 6, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "工业园区管委会主任", "start": "", "end": "", "rank": "", "note": "prior role"},
    {"person_id": 6, "org_id": 1, "title": "乡镇党委书记", "start": "", "end": "", "rank": "", "note": "prior乡镇书记"},
    {"person_id": 6, "org_id": 2, "title": "乡镇镇长", "start": "", "end": "", "rank": "", "note": "prior乡镇长"},
    # 李涛 — 副市长、公安局长
    {"person_id": 7, "org_id": 9, "title": "公安局党委书记、局长、督察长", "start": "", "end": "present", "rank": "副县级", "note": "三级高级警长"},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 7, "org_id": 9, "title": "延安市公安局治安管理支队支队长", "start": "", "end": "", "rank": "副县级", "note": "prior role"},
    {"person_id": 7, "org_id": 9, "title": "延安市公安局治安管理支队副支队长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 7, "org_id": 9, "title": "延安市公安局治安管理支队内务大队大队长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 7, "org_id": 9, "title": "宝塔分局信息中心主任", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 7, "org_id": 9, "title": "宝塔分局临镇派出所所长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 7, "org_id": 9, "title": "宝塔分局万花派出所所长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 7, "org_id": 9, "title": "宝塔分局治安大队民警", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 7, "org_id": 9, "title": "延长县公安局黑家堡派出所治安警、副所长", "start": "", "end": "", "rank": "", "note": "earliest known role"},
    # 刘建强 — 副市长
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "市政府组成部门四级调研员", "start": "", "end": "", "rank": "", "note": "prior role"},
    {"person_id": 8, "org_id": 2, "title": "市政府组成部门科长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "市政府组成部门副科长", "start": "", "end": "", "rank": "", "note": ""},
    # 赵雁鸿 — 副市长
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副县级", "note": "无党派"},
    {"person_id": 9, "org_id": 11, "title": "延川县政协副主席", "start": "", "end": "", "rank": "", "note": "prior role"},
    {"person_id": 9, "org_id": 5, "title": "延川县工商联合会主席", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "延川县会计结算中心主任", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "延川县采购中心主任", "start": "", "end": "", "rank": "", "note": ""},
    # 陈伟 — 副市长（挂职）
    {"person_id": 10, "org_id": 2, "title": "副市长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "建设银行延安分行高级客户经理、党委组织部部长、办公室副主任", "start": "", "end": "", "rank": "", "note": "prior roles in bank"},
    {"person_id": 10, "org_id": 9, "title": "建设银行延安南桥支行高级客户经理、行长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "建设银行延安分行营运管理部高级客户经理、总经理", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "建设银行黄陵县支行党支部书记、高级客户经理、行长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "建设银行店头煤炭专业支行副行长、党支部书记、行长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "建设银行延安分行营业部河庄坪办事处主任", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "建设银行延安分行人事教育科员工", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "建设银行延安分行延川县支行股长", "start": "", "end": "", "rank": "", "note": "earliest known role"},
    # 待查（纪委书记）
    {"person_id": 11, "org_id": 3, "title": "纪委书记、监委主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    # 待查（组织部长）
    {"person_id": 12, "org_id": 5, "title": "组织部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    # 待查（宣传部长）
    {"person_id": 13, "org_id": 6, "title": "宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    # 待查（政法委书记）
    {"person_id": 14, "org_id": 7, "title": "政法委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    # 待查（统战部长）
    {"person_id": 15, "org_id": 8, "title": "统战部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "", "note": ""},
    # 待查（人大主任）
    {"person_id": 16, "org_id": 10, "title": "市人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # 待查（政协主席）
    {"person_id": 17, "org_id": 11, "title": "市政协主席", "start": "", "end": "present", "rank": "正县级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
# Leadership team overlaps
RELATIONSHIPS = [
    # Core top-2
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记—市长搭档", "overlap_org": "中共子长市委员会/子长市人民政府", "overlap_period": "至今"},
    # 王诚 — 市委常委 (government cross-posts)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记—常务副市长", "overlap_org": "中共子长市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委书记—市委常委、副市长", "overlap_org": "中共子长市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "市委书记—市委常委、副市长（挂职）", "overlap_org": "中共子长市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "市委书记—纪委书记", "overlap_org": "中共子长市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "市委书记—组织部长", "overlap_org": "中共子长市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "市委书记—宣传部长", "overlap_org": "中共子长市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "市委书记—政法委书记", "overlap_org": "中共子长市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "市委书记—统战部长", "overlap_org": "中共子长市委员会", "overlap_period": "至今"},
    # 高晓斌 — 政府班子
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "市长—常务副市长", "overlap_org": "子长市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "市长—副市长", "overlap_org": "子长市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "市长—副市长（挂职）", "overlap_org": "子长市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "市长—副市长", "overlap_org": "子长市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "市长—副市长、公安局长", "overlap_org": "子长市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "市长—副市长", "overlap_org": "子长市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "市长—副市长", "overlap_org": "子长市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "市长—副市长（挂职）", "overlap_org": "子长市人民政府", "overlap_period": "至今"},
    # 卢志华 & 李涛 — 曾在宝塔区共事
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "两人曾在延安市宝塔区不同岗位任职（卢志华在区委办和乡镇，李涛在宝塔分局派出所），时间可能有重叠", "overlap_org": "延安市宝塔区", "overlap_period": ""},
    # 李茂胜 & 任碧辉 — 均有乡镇党委书记经历
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "两人均有乡镇党委书记经历，曾同级别任乡镇主要领导", "overlap_org": "", "overlap_period": ""},
    # 高晓斌 earlier — 团市委系统与赵雁鸿 不直接相关
    # 人大/政协 — 系统内关系
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "市委书记—人大主任", "overlap_org": "子长市", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "市委书记—政协主席", "overlap_org": "子长市", "overlap_period": "至今"},
]


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    run_build(
        slug="子长市领导班子关系图",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )


if __name__ == "__main__":
    main()
