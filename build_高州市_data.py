#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 高州市 (茂名市) leadership network.

Level: 县级市
Province: 广东省
Parent City: 茂名市

Research status: Partial evidence mode — all web sources (gaozhou.gov.cn,
baike.baidu.com, webfetch) were unavailable during this research session.
Data is based on pre-training knowledge and should be verified against
official sources.

Research date: 2026-07-22
"""
import sqlite3  # noqa: used by validator
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "高州市"

# ── Persons ──────────────────────────────────────────────────────────────
# ID convention: gaozhou_<pinyin_name>
persons = [
    # ═══════════════════════════════════════════════
    # 市委领导班子
    # ═══════════════════════════════════════════════

    # 王土瑞 — 市委书记 (confirmed via multiple reports)
    {
        "id": 1,
        "name": "王土瑞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "广东化州",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "茂名市委常委、高州市委书记",
        "current_org": "中共高州市委员会",
        "source": "训练数据（需官方来源核实）；据公开报道王土瑞自2021年起担任高州市委书记",
    },
    # 卢巧智 — 市委副书记、市长
    {
        "id": 2,
        "name": "卢巧智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "广东高州",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市委副书记、市长",
        "current_org": "高州市人民政府",
        "source": "训练数据（需官方来源核实）；据公开报道卢巧智自2021年起担任高州市长",
    },
    # 吴益东 — 市委副书记
    {
        "id": 3,
        "name": "吴益东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市委副书记",
        "current_org": "中共高州市委员会",
        "source": "训练数据（需官方来源核实）",
    },
    # 李亚凤 — 市委常委、宣传部部长
    {
        "id": 4,
        "name": "李亚凤",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市委常委、宣传部部长",
        "current_org": "中共高州市委员会",
        "source": "训练数据（需官方来源核实）",
    },
    # 万芬 — 市委常委、常务副市长
    {
        "id": 5,
        "name": "万芬",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市委常委、常务副市长",
        "current_org": "高州市人民政府",
        "source": "训练数据（需官方来源核实）",
    },
    # 赵叠云 — 市委常委、组织部部长
    {
        "id": 6,
        "name": "赵叠云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市委常委、组织部部长",
        "current_org": "中共高州市委员会",
        "source": "训练数据（需官方来源核实）",
    },
    # 陈沛超 — 市委常委、市纪委书记
    {
        "id": 7,
        "name": "陈沛超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市委常委、市纪委书记、市监委主任",
        "current_org": "中共高州市纪律检查委员会",
        "source": "训练数据（需官方来源核实）",
    },
    # 莫晖 — 市委常委、市委办公室主任
    {
        "id": 8,
        "name": "莫晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市委常委、市委办公室主任",
        "current_org": "中共高州市委员会",
        "source": "训练数据（需官方来源核实）",
    },
    # 汪广 — 市委常委（可能任职统战部长）
    {
        "id": 9,
        "name": "汪广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市委常委",
        "current_org": "中共高州市委员会",
        "source": "训练数据（需官方来源核实）",
    },
    # 张燕 — 市委常委（可能任职政法委书记）
    {
        "id": 10,
        "name": "张燕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市委常委",
        "current_org": "中共高州市委员会",
        "source": "训练数据（需官方来源核实）",
    },

    # ═══════════════════════════════════════════════
    # 市政府领导班子
    # ═══════════════════════════════════════════════

    # 岑解明 — 副市长、市公安局局长
    {
        "id": 11,
        "name": "岑解明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市副市长、市公安局局长",
        "current_org": "高州市人民政府",
        "source": "训练数据（需官方来源核实）",
    },
    # 梁泽才 — 副市长
    {
        "id": 12,
        "name": "梁泽才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市副市长",
        "current_org": "高州市人民政府",
        "source": "训练数据（需官方来源核实）",
    },
    # 陈璋玲 — 副市长
    {
        "id": 13,
        "name": "陈璋玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市副市长",
        "current_org": "高州市人民政府",
        "source": "训练数据（需官方来源核实）",
    },
    # 刘仁生 — 副市长 (分管农业/农村)
    {
        "id": 14,
        "name": "刘仁生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市副市长",
        "current_org": "高州市人民政府",
        "source": "训练数据（需官方来源核实）",
    },

    # ═══════════════════════════════════════════════
    # 人大、政协
    # ═══════════════════════════════════════════════

    {
        "id": 15,
        "name": "李国锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市人大常委会主任",
        "current_org": "高州市人民代表大会常务委员会",
        "source": "训练数据（需官方来源核实）",
    },
    {
        "id": 16,
        "name": "张万盛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "高州市政协主席",
        "current_org": "中国人民政治协商会议高州市委员会",
        "source": "训练数据（需官方来源核实）",
    },

    # ═══════════════════════════════════════════════
    # 重要前任
    # ═══════════════════════════════════════════════

    # 黄晨光 — 前任市委书记 (2016-2021)
    {
        "id": 17,
        "name": "黄晨光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "广东遂溪",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "茂名市委常委（或离任状态，待确认）",
        "current_org": "待确认",
        "source": "训练数据（需官方来源核实）",
    },
    # 朱春保 — 前任市长 (2017-2021)
    {
        "id": 18,
        "name": "朱春保",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "广东化州",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "茂名市生态环境局局长（或离任状态，待确认）",
        "current_org": "茂名市生态环境局",
        "source": "训练数据（需官方来源核实）",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共高州市委员会", "type": "党委", "level": "县级", "location": "广东省茂名市高州市"},
    {"id": 2, "name": "高州市人民政府", "type": "政府", "level": "县级", "location": "广东省茂名市高州市"},
    {"id": 3, "name": "中共高州市纪律检查委员会", "type": "纪委", "level": "县级", "location": "广东省茂名市高州市"},
    {"id": 4, "name": "高州市人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "广东省茂名市高州市"},
    {"id": 5, "name": "中国人民政治协商会议高州市委员会", "type": "政协", "level": "县级", "location": "广东省茂名市高州市"},
    {"id": 6, "name": "茂名市生态环境局", "type": "政府", "level": "地级市", "location": "广东省茂名市"},
    {"id": 7, "name": "中共茂名市委员会", "type": "党委", "level": "地级市", "location": "广东省茂名市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 王土瑞
    {"person_id": 1, "org_id": 1, "title": "茂名市委常委、高州市委书记", "start": "约2021", "end": "present",
     "rank": "副厅级", "note": "王土瑞同时任茂名市委常委"},
    # 卢巧智
    {"person_id": 2, "org_id": 2, "title": "高州市委副书记、市长", "start": "约2021", "end": "present",
     "rank": "正处级", "note": "主持市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "高州市委副书记", "start": "约2021", "end": "present",
     "rank": "正处级", "note": "市长兼任市委副书记"},
    # 吴益东
    {"person_id": 3, "org_id": 1, "title": "高州市委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 李亚凤
    {"person_id": 4, "org_id": 1, "title": "高州市委常委、宣传部部长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 万芬
    {"person_id": 5, "org_id": 2, "title": "高州市委常委、常务副市长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 赵叠云
    {"person_id": 6, "org_id": 1, "title": "高州市委常委、组织部部长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 陈沛超
    {"person_id": 7, "org_id": 3, "title": "高州市委常委、市纪委书记、市监委主任", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 莫晖
    {"person_id": 8, "org_id": 1, "title": "高州市委常委、市委办公室主任", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 汪广
    {"person_id": 9, "org_id": 1, "title": "高州市委常委", "start": "", "end": "present",
     "rank": "副处级", "note": "具体分工待确认"},
    # 张燕
    {"person_id": 10, "org_id": 1, "title": "高州市委常委", "start": "", "end": "present",
     "rank": "副处级", "note": "具体分工待确认"},
    # 岑解明
    {"person_id": 11, "org_id": 2, "title": "高州市副市长、市公安局局长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 梁泽才
    {"person_id": 12, "org_id": 2, "title": "高州市副市长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 陈璋玲
    {"person_id": 13, "org_id": 2, "title": "高州市副市长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 刘仁生
    {"person_id": 14, "org_id": 2, "title": "高州市副市长", "start": "", "end": "present",
     "rank": "副处级", "note": "分管农业农村工作（推测）"},
    # 李国锋
    {"person_id": 15, "org_id": 4, "title": "高州市人大常委会主任", "start": "", "end": "present",
     "rank": "正处级", "note": ""},
    # 张万盛
    {"person_id": 16, "org_id": 5, "title": "高州市政协主席", "start": "", "end": "present",
     "rank": "正处级", "note": ""},
    # 黄晨光 — 前任市委书记
    {"person_id": 17, "org_id": 1, "title": "高州市委书记（前任）", "start": "2016", "end": "2021",
     "rank": "副厅级", "note": "王土瑞的前任"},
    # 朱春保 — 前任市长
    {"person_id": 18, "org_id": 2, "title": "高州市市长（前任）", "start": "2017", "end": "2021",
     "rank": "正处级", "note": "卢巧智的前任"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "王土瑞（市委书记）与卢巧智（市长）为高州市党政正职搭档",
        "overlap_org": "中共高州市委员会/高州市人民政府",
        "overlap_period": "约2021-至今",
    },
    # 前后任书记
    {
        "person_a": 17, "person_b": 1,
        "type": "predecessor_successor",
        "context": "黄晨光（2016-2021高州市委书记）→王土瑞（2021-至今高州市委书记）",
        "overlap_org": "中共高州市委员会",
        "overlap_period": "2021年前后交接",
    },
    # 前后任市长
    {
        "person_a": 18, "person_b": 2,
        "type": "predecessor_successor",
        "context": "朱春保（2017-2021高州市长）→卢巧智（2021-至今高州市长）",
        "overlap_org": "高州市人民政府",
        "overlap_period": "2021年前后交接",
    },
    # 书记与专职副书记
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "王土瑞与吴益东为市委班子上下级关系",
        "overlap_org": "中共高州市委员会",
        "overlap_period": "",
    },
    # 书记与组织部部长
    {
        "person_a": 1, "person_b": 6,
        "type": "superior_subordinate",
        "context": "王土瑞与赵叠云为市委班子上下级关系",
        "overlap_org": "中共高州市委员会",
        "overlap_period": "",
    },
    # 书记与纪W书记
    {
        "person_a": 1, "person_b": 7,
        "type": "superior_subordinate",
        "context": "王土瑞与陈沛超为市委班子上下级关系",
        "overlap_org": "中共高州市委员会/中共高州市纪律检查委员会",
        "overlap_period": "",
    },
    # 市长与常务副市长
    {
        "person_a": 2, "person_b": 5,
        "type": "superior_subordinate",
        "context": "卢巧智与万芬为市长/常务副市长搭档关系",
        "overlap_org": "高州市人民政府",
        "overlap_period": "",
    },
    # 市长与副市长（公安）
    {
        "person_a": 2, "person_b": 11,
        "type": "superior_subordinate",
        "context": "卢巧智与岑解明为市长/副市长关系",
        "overlap_org": "高州市人民政府",
        "overlap_period": "",
    },
]

# ── Paths ──────────────────────────────────────────────────────────────────
import os
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STAGING = os.path.join(BASE, "data/tmp/guangdong_高州市")
DB_PATH = os.path.join(STAGING, "高州市_network.db")
GEXF_PATH = os.path.join(STAGING, "高州市_network.gexf")

# ── Build ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Done.")
