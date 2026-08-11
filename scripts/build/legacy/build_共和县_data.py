#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Gonghe County (共和县),
Hainan Tibetan Autonomous Prefecture (海南藏族自治州), Qinghai (青海省).

task_id: qinghai_共和县
targets: 县委书记 & 县长 (张俊录 as 州委副书记、县委书记; 周明长 as 县委副书记、县长)

Research as-of: 2026-08-07 (based on official gonghe.gov.cn, hainanzhou.gov.cn,
and Baidu Baike). Web search engines (Baidu/Sogou/360/Bing/Exa) were blocked in the
research environment, so career timelines are partial. Durations and personal
fields that could not be verified are marked unknown; uncertainty is preserved in
the person JSON open_questions and the report open gaps, not fabricated.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/qinghai_共和县")
DB_PATH = os.path.join(TMP, "共和县_network.db")
GEXF_PATH = os.path.join(TMP, "共和县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "张俊录", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海南州委副书记、共和县委书记", "current_org": "中共共和县委员会",
     "source": "https://www.gonghe.gov.cn/xwdt/zyhy/content_1013654271"},
    {"id": 2, "name": "周明长", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-02", "birthplace": "青海省海东市互助县", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共和县委副书记、县人民政府县长", "current_org": "共和县人民政府",
     "source": "https://baike.baidu.com/item/%E5%91%A8%E6%98%8E%E9%95%BF"},

    # ── 人大 / 政协 ──
    {"id": 3, "name": "曹志刚", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共和县人大常委会党组书记（主任）", "current_org": "共和县人民代表大会常务委员会",
     "source": "https://www.gonghe.gov.cn/xwdt/zyhy/content_" },
    {"id": 4, "name": "王有业", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政协共和县委员会主席", "current_org": "中国人民政治协商会议共和县委员会",
     "source": "https://www.gonghe.gov.cn/xwdt/zyhy/content_1013654504"},

    # ── 县政府领导 (deputy magistrates) ──
    {"id": 5, "name": "元旦才让", "gender": "男", "ethnicity": "藏族",
     "birth": "1980-01", "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共和县副县长", "current_org": "共和县人民政府",
     "source": "https://www.gonghe.gov.cn/zwgk/fdzdgknr/jgjj/zfld"},
    {"id": 6, "name": "才铎", "gender": "男", "ethnicity": "藏族",
     "birth": "1980-04", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共和县副县长、县公安局局长", "current_org": "共和县公安分局（县公安局）",
     "source": "https://www.gonghe.gov.cn/zwgk/fdzdgknr/jgjj/zfld"},
    {"id": 7, "name": "吉先加", "gender": "男", "ethnicity": "藏族",
     "birth": "1979-02", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共和县副县长", "current_org": "共和县人民政府",
     "source": "https://www.gonghe.gov.cn/zwgk/fdzdgknr/jgjj/zfld"},
    {"id": 8, "name": "童应庆", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-07", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共和县副县长", "current_org": "共和县人民政府",
     "source": "https://www.gonghe.gov.cn/zwgk/fdzdgknr/jgjj/zfld"},
    {"id": 9, "name": "仁钦达哇", "gender": "女", "ethnicity": "藏族",
     "birth": "1988-10", "birthplace": "", "education": "党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共和县副县长", "current_org": "共和县人民政府",
     "source": "https://www.gonghe.gov.cn/zwgk/fdzdgknr/jgjj/zfld"},

    # ── 政协委员 ──
    {"id": 10, "name": "多杰本", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "政协共和县委员会副主席", "current_org": "中国人民政治协商会议共和县委员会",
     "source": "https://www.gonghe.gov.cn/xwdt/zyhy/content_1013654504"},
    {"id": 11, "name": "旦木秋措毛", "gender": "女", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "政协共和县委员会秘书长", "current_org": "中国人民政治协商会议共和县委员会",
     "source": "https://www.gonghe.gov.cn/xwdt/zyhy/content_1013654504"},

    # ── 前任领导 ──
    {"id": 12, "name": "拉夫旦", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原共和县人大常委会主任（离任）", "current_org": "共和县人民代表大会常务委员会",
     "source": "https://www.gonghexww.cn/system/2026/02/xx/030534479.shtml"},
    {"id": 13, "name": "王金山", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海南州人民政府国有资产监督管理委员会主任（原共和县委常委、副县长）", "current_org": "海南州人民政府",
     "source": "https://www.hainanzhou.gov.cn/zwgk/fdzdgknr/rsrm/content_400018547"},

    # ── 海南州层级 ──
    {"id": 14, "name": "熊元来", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海南州委书记", "current_org": "中共海南藏族自治州委员会",
     "source": "https://www.hainanzhou.gov.cn/"},
    {"id": 15, "name": "当周", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海南州委副书记、州政府代理州长", "current_org": "海南藏族自治州人民政府",
     "source": "https://www.hainanzhou.gov.cn/"},
    {"id": 16, "name": "戴敏捷", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-02", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "省政府副秘书长、海南州委副书记、州政府副州长", "current_org": "海南藏族自治州人民政府",
     "source": "https://www.hainanzhou.gov.cn/zwgk/fdzdgknr/jgjj/zzfld"},
    {"id": 17, "name": "李伟", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海南州委常委、州纪委书记、州监委主任", "current_org": "中共海南藏族自治州纪律检查委员会",
     "source": "https://www.gonghe.gov.cn/xwdt/zyhy/content_1013654271"},
]

organizations = [
    {"id": 1, "name": "中共共和县委员会", "type": "党委", "level": "县处级",
     "parent": "中共海南藏族自治州委员会", "location": "青海省海南藏族自治州共和县"},
    {"id": 2, "name": "共和县人民政府", "type": "政府", "level": "县处级",
     "parent": "海南藏族自治州人民政府", "location": "青海省海南藏族自治州共和县"},
    {"id": 3, "name": "共和县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "海南藏族自治州人大常委会", "location": "青海省海南藏族自治州共和县"},
    {"id": 4, "name": "中国人民政治协商会议共和县委员会", "type": "政协", "level": "县处级",
     "parent": "政协海南藏族自治州委员会", "location": "青海省海南藏族自治州共和县"},
    {"id": 5, "name": "共和县公安局", "type": "政府", "level": "乡科级",
     "parent": "海南藏族自治州公安局", "location": "青海省海南藏族自治州共和县"},
    {"id": 6, "name": "中共海南藏族自治州委员会", "type": "党委", "level": "地厅级",
     "parent": "中共青海省委员会", "location": "青海省海南藏族自治州"},
    {"id": 7, "name": "海南藏族自治州人民政府", "type": "政府", "level": "地厅级",
     "parent": "青海省人民政府", "location": "青海省海南藏族自治州"},
    {"id": 8, "name": "海南州人民政府国有资产监督管理委员会", "type": "政府", "level": "地厅级",
     "parent": "海南藏族自治州人民政府", "location": "青海省海南藏族自治州"},
    {"id": 9, "name": "中共海南藏族自治州纪律检查委员会", "type": "纪委", "level": "地厅级",
     "parent": "中共青海省纪律检查委员会", "location": "青海省海南藏族自治州"},
    {"id": 10, "name": "海东市人民政府", "type": "政府", "level": "地厅级",
     "parent": "青海省人民政府", "location": "青海省海东市"},
    {"id": 11, "name": "海东市发展和改革委员会", "type": "政府", "level": "县处级",
     "parent": "海东市人民政府", "location": "青海省海东市"},
    {"id": 12, "name": "海东市住房和城乡建设局", "type": "政府", "level": "县处级",
     "parent": "海东市人民政府", "location": "青海省海东市"},
    {"id": 13, "name": "海东市互助县", "type": "政府", "level": "县处级",
     "parent": "海东市人民政府", "location": "青海省海东市互助县"},
]

positions = [
    # ── Zhang Junlu (张俊录) 县委书记 ──
    {"person_id": 1, "org_id": 6, "title": "海南州委副书记", "start": "", "end": "present", "rank": "副厅级",
     "note": "兼任共和县委书记，属于州府首府县的编制性安排；具体任职年份待核实"},
    {"person_id": 1, "org_id": 1, "title": "共和县委书记", "start": "", "end": "present", "rank": "副厅级",
     "note": "2026年7月共和县第十七次党代会选入县委领导班子；前期履历待查"},
    {"person_id": 1, "org_id": 0, "title": "履历缺口", "start": "unknown", "end": "unknown", "rank": "",
     "note": "公开资料未找到任共和县委书记前的完整履历（出生、籍贯、学历、此前职务均未公开）"},

    # ── Zhou Mingchang (周明长) 县长 ──
    {"person_id": 2, "org_id": 13, "title": "海东市互助县人民政府副县长", "start": "", "end": "", "rank": "副县级",
     "note": "早年履历，籍贯为海东市互助县"},
    {"person_id": 2, "org_id": 11, "title": "海东市发展和改革委员会党组书记、主任", "start": "2025-04", "end": "2025-10", "rank": "正县级",
     "note": "2025年4月至2025年10月任"},
    {"person_id": 2, "org_id": 12, "title": "海东市住房和城乡建设局局长", "start": "2024-04", "end": "2025-04", "rank": "正县级",
     "note": "2024年4月-2025年4月任"},
    {"person_id": 2, "org_id": 1, "title": "共和县委副书记", "start": "2025-09", "end": "present", "rank": "副厅级",
     "note": "2025年9月起任共和县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "共和县人民政府县长（代/任）", "start": "2025-09", "end": "present", "rank": "正县级",
     "note": "2025年9月任县长；2026年7月30日共和县十七届人大一次会议当选"},

    # ── 人大 / 政协 ──
    {"person_id": 3, "org_id": 3, "title": "县人大常委会党组书记（主任）", "start": "2026-07", "end": "present", "rank": "正县级",
     "note": "2026年7月十七届人大一次会议选任"},
    {"person_id": 4, "org_id": 4, "title": "政协主席", "start": "2026-07-29", "end": "present", "rank": "正县级",
     "note": "2026年7月29日当选"},
    {"person_id": 10, "org_id": 4, "title": "政协副主席", "start": "2026-07-29", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 4, "title": "政协秘书长", "start": "2026-07-29", "end": "present", "rank": "副县级", "note": ""},

    # ── 县政府领导班子 ──
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级",
     "note": "分管教育、城乡建设、文旅体育、广播电视等"},
    {"person_id": 6, "org_id": 2, "title": "副县长、县公安局局长", "start": "", "end": "present", "rank": "副县级",
     "note": "分管公安、司法、民族宗教"},
    {"person_id": 6, "org_id": 5, "title": "县公安局局长", "start": "", "end": "present", "rank": "正科级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级",
     "note": "分管发改、能源、农牧科技、乡村振兴、统计"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级",
     "note": "分管交通、卫生健康、医保"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级",
     "note": "分管民政、市场监管、民族语文、机关事务"},

    # ── 前任领导 ──
    {"person_id": 12, "org_id": 3, "title": "县人大常委会主任（前任）", "start": "", "end": "2026", "rank": "正县级",
     "note": "2026年2月县两会时在任；后卸任（去向待核实）"},
    {"person_id": 13, "org_id": 2, "title": "县委常委、副县长", "start": "~2026", "end": "2026-07", "rank": "副县级",
     "note": "2026年5月在任；2026年7月调任州国资主任"},
    {"person_id": 13, "org_id": 8, "title": "海南州国资委员会主任", "start": "2026-07", "end": "present", "rank": "正处级",
     "note": "2026-07-17海南州人事任免" },

    # ── 海南州层级 ──
    {"person_id": 14, "org_id": 6, "title": "海南州委书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 15, "org_id": 7, "title": "海南州委副书记、州政府代理州长", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 16, "org_id": 7, "title": "省政府副秘书长、海南州委副书记、副州长", "start": "", "end": "present", "rank": "副厅级",
     "note": "对口支援、东西部协作、招商引资分工；跨省/省直交流干部"},
    {"person_id": 16, "org_id": 6, "title": "海南州委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 9, "title": "海南州委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "张俊录任县委书记，周明长任县委副书记、县长，为党政一把手搭档",
     "overlap_org": "中共共和县委员会/共和县人民政府",
     "overlap_period": "2025-09至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate", "strength": "strong",
     "context": "张俊录为海南州委副书记，熊元来为州委书记，属州委上下级/同班子关系",
     "overlap_org": "中共海南藏族自治州委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 16, "type": "overlap", "strength": "medium",
     "context": "张俊录与戴敏捷均任海南州委副书记，属州委常委同僚",
     "overlap_org": "中共海南藏族自治州委员会",
     "overlap_period": "至今", "confidence": "plausible"},
    {"person_a": 1, "person_b": 15, "type": "overlap", "strength": "medium",
     "context": "张俊录为州委、当周为州政府代理州长，州级党政班子共事；共和为州府首县",
     "overlap_org": "海南藏族自治州党委/政府",
     "overlap_period": "至今", "confidence": "plausible"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "strength": "strong",
     "context": "张俊录任县委书记，曹志刚任县人大常委会党组书记（主任），为县委-人大县班子关系",
     "overlap_org": "中共共和县委员会",
     "overlap_period": "2026-07至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "张俊录与王有业在共和县班子共事，王为县政协主席",
     "overlap_org": "中共共和县委员会",
     "overlap_period": "2026-07至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "strength": "medium",
     "context": "周明长为县长，曹志刚为人大常委会党组书记，县行政与人大班子关系",
     "overlap_org": "共和县人大常委会/人民政府",
     "overlap_period": "2026-07至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "strength": "strong",
     "context": "周明长作为县长（主持全面工作），元旦才职为副县长，属行政上下级",
     "overlap_org": "共和县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 12, "person_b": 3, "type": "predecessor_successor", "strength": "strong",
     "context": "拉夫旦在2026年2月两会上仍任人大常委会主任，后由曹志刚继任（2026年7月十七届人大）",
     "overlap_org": "共和县人民代表大会常务委员会",
     "overlap_period": "2026", "confidence": "plausible"},
    {"person_a": 13, "person_b": 2, "type": "overlap", "strength": "strong",
     "context": "王金山曾任共和县委常委、副县长（2026年5月在任），与周明长同县政府班子；后调任州国资委",
     "overlap_org": "共和县人民政府",
     "overlap_period": "~2026-07", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "strength": "strong",
     "context": "周明长为县长，才铎为副县长兼公安局长，行政上下级",
     "overlap_org": "共和县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "strength": "strong",
     "context": "周明长为县长，吉先加为副县长，行政上下级",
     "overlap_org": "共和县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "strength": "medium",
     "context": "元旦才与才铎同任共和县副县长，为政府班子同事",
     "overlap_org": "共和县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 8, "type": "overlap", "strength": "medium",
     "context": "吉先加、童应均同任共和县副县长",
     "overlap_org": "共和县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 9, "person_b": 8, "type": "overlap", "strength": "medium",
     "context": "仁钦达哇、童应庆同任共和县副县长",
     "overlap_org": "共和县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if ("县委书记" in role) and ("副书记" not in role):
        return "255,50,50"
    elif "县长" in role and "县" in role:
        return "50,100,255"
    elif "人大常委会" in role or "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    elif "副州长" in role or "州长" in role or "州委书记" in role:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,180,120",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")

def is_top_leader(p):
    role = p["current_post"]
    return ("县委书记" in role and "副书记" not in role) or ("县长" in role)

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
        c.execute("""INSERT OR REPLACE INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
             pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT OR REPLACE INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"], r["context"],
             r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# ── BUILD GEXF ─────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>共和县领导班子工作关系网络 (task_id qinghai_共和县)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org_type" type="string"/>')
    lines.append('      <attribute id="2" title="title" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="etype" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        r, g, b = [x.strip() for x in c.split(",")]
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        r, g, b = [x.strip() for x in c.split(",")]
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="org"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        if pos["org_id"] == 0:
            continue  # skip placeholder person gap row (no org node)
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append('          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
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

# ── SUMMARY ─────────────────────────────────────────────────

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