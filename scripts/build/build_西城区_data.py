#!/usr/bin/env python3
"""
北京市西城区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Xicheng District leadership.

Data source: bjxch.gov.cn (official leadership page, accessed 2026-07-15)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "西城区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "西城区_network.gexf")

# ════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════

# Person ID convention: xicheng_{surname_givenname}
PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source
    # ── Top leaders ──
    ("xicheng_liu_dongwei", "刘东伟", "男", "汉族", "1972年8月", "未知", "在职研究生", "中共党员", "未知",
     "区委书记", "中共北京市西城区委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_zhi_haijie", "郅海杰", "男", "汉族", "1972年11月", "未知", "在职研究生", "中共党员", "未知",
     "区委副书记、区长", "北京市西城区人民政府", "bjxch.gov.cn/xxgk/ldzc.html"),

    # ── Standing Committee ──
    ("xicheng_cai_bing", "蔡兵", "男", "汉族", "1977年5月", "未知", "研究生", "中共党员", "未知",
     "区委副书记、区委党校校长", "中共北京市西城区委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_wu_bin", "吴斌", "男", "汉族", "1971年8月", "未知", "在职大学", "中共党员", "未知",
     "区委常委、区纪委书记、区监委主任", "中共北京市西城区纪律检查委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_liu_meiying", "刘梅英", "女", "汉族", "1978年2月", "未知", "在职研究生", "中共党员", "未知",
     "区委常委、常务副区长、金融街党工委书记", "北京市西城区人民政府", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_zhang_xiaojia", "张晓家", "男", "汉族", "1974年10月", "未知", "在职研究生", "中共党员", "未知",
     "区委常委、宣传部部长", "中共北京市西城区委宣传部", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_wang_bo", "王波", "男", "汉族", "1979年9月", "未知", "研究生", "中共党员", "未知",
     "区委常委、副区长", "北京市西城区人民政府", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_jiang_lan", "江岚", "女", "汉族", "1975年6月", "未知", "在职研究生", "中共党员", "未知",
     "区委常委、统战部部长、区政协党组副书记", "中共北京市西城区委统战部", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_liu_zhi", "刘峙", "男", "汉族", "1974年8月", "未知", "在职大学", "中共党员", "未知",
     "区委常委、区武装部部长", "北京市西城区人民武装部", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_yu_jiaming", "于家明", "男", "汉族", "1983年10月", "未知", "研究生", "中共党员", "未知",
     "区委常委、组织部部长", "中共北京市西城区委组织部", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_gao_yunfei", "高云飞", "男", "汉族", "1974年1月", "未知", "研究生", "中共党员", "未知",
     "区委常委、政法委书记", "中共北京市西城区委政法委员会", "bjxch.gov.cn/xxgk/ldzc.html"),

    # ── District Government Vice Heads ──
    ("xicheng_song_mei", "宋玫", "女", "汉族", "1971年9月", "未知", "大学", "农工党党员", "未知",
     "副区长", "北京市西城区人民政府", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_zhu_haibin", "朱海斌", "男", "汉族", "1976年6月", "未知", "研究生", "中共党员", "未知",
     "副区长", "北京市西城区人民政府", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_li_jianxi", "李健希", "男", "汉族", "1983年7月", "未知", "在职研究生", "中共党员", "未知",
     "副区长", "北京市西城区人民政府", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_fan_yang", "樊阳", "男", "汉族", "1978年12月", "未知", "研究生", "中共党员", "未知",
     "副区长、公安分局局长", "北京市公安局西城分局", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_bing_hao", "邴浩", "男", "汉族", "1984年9月", "未知", "研究生", "中共党员", "未知",
     "副区长", "北京市西城区人民政府", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_guo_jie", "郭洁", "女", "汉族", "1976年6月", "未知", "在职研究生", "中共党员", "未知",
     "副区长（挂职）", "北京市西城区人民政府", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_du_hongyue", "杜洪悦", "女", "汉族", "1977年10月", "未知", "在职研究生", "中共党员", "未知",
     "副区长", "北京市西城区人民政府", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_hong_yingzi", "洪英子", "女", "朝鲜族", "1975年4月", "未知", "在职研究生", "中共党员", "未知",
     "副区长（挂职）", "北京市西城区人民政府", "bjxch.gov.cn/xxgk/ldzc.html"),

    # ── People's Congress ──
    ("xicheng_cheng_changhong", "程昌宏", "男", "汉族", "1969年2月", "未知", "研究生/工学硕士", "中共党员", "未知",
     "区人大常委会党组书记、主任", "北京市西城区人民代表大会常务委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_xu_xiaohong", "许晓红", "女", "汉族", "1966年10月", "未知", "市委党校大学", "中共党员", "未知",
     "区人大常委会党组副书记、副主任", "北京市西城区人民代表大会常务委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_li_hua", "李华", "男", "汉族", "1967年5月", "未知", "中央党校研究生", "中共党员", "未知",
     "区人大常委会党组成员、副主任", "北京市西城区人民代表大会常务委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_wang_xiaonong", "王效农", "男", "汉族", "1970年11月", "未知", "大学", "中共党员", "未知",
     "区人大常委会党组成员、副主任", "北京市西城区人民代表大会常务委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_zhang_ding", "张丁", "男", "汉族", "1968年9月", "未知", "市委党校大学", "中共党员", "未知",
     "区人大常委会党组成员、副主任", "北京市西城区人民代表大会常务委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_yuan_li", "袁利", "女", "汉族", "1969年1月", "未知", "中央党校研究生", "中共党员", "未知",
     "区人大常委会党组成员、副主任", "北京市西城区人民代表大会常务委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_li_cheng", "李程", "女", "汉族", "1969年6月", "未知", "大学/公共管理硕士", "中共党员", "未知",
     "区人大常委会党组成员、副主任", "北京市西城区人民代表大会常务委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_wang_zhe", "王喆", "男", "汉族", "1978年11月", "未知", "在职研究生/法学博士", "民盟盟员", "未知",
     "区人大常委会副主任（不驻会）", "北京市西城区人民代表大会常务委员会", "bjxch.gov.cn/xxgk/ldzc.html"),

    # ── CPPCC ──
    ("xicheng_liu_guoqiang", "刘国强", "男", "汉族", "1970年3月", "未知", "中央党校研究生", "中共党员", "未知",
     "区政协党组书记、主席", "中国人民政治协商会议北京市西城区委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_peng_xiuying", "彭秀颖", "女", "汉族", "1967年4月", "未知", "在职研究生", "中共党员", "未知",
     "区政协党组副书记、副主席", "中国人民政治协商会议北京市西城区委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_tu_yunguo", "涂云国", "女", "汉族", "1968年7月", "未知", "在职研究生", "中共党员", "未知",
     "区政协党组成员、副主席", "中国人民政治协商会议北京市西城区委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_chen_xin", "陈新", "男", "汉族", "1967年3月", "未知", "大学", "中共党员", "未知",
     "区政协党组成员、副主席", "中国人民政治协商会议北京市西城区委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_yang_qiu", "杨秋", "女", "汉族", "1968年2月", "未知", "大学", "民进会员", "未知",
     "区政协副主席（不驻会）", "中国人民政治协商会议北京市西城区委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_guan_zhenpeng", "关振鹏", "男", "汉族", "1969年5月", "未知", "大学", "致公党党员", "未知",
     "区政协副主席（不驻会）", "中国人民政治协商会议北京市西城区委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_wang_jinglan", "王景兰", "女", "汉族", "1969年2月", "未知", "在职研究生", "九三学社社员", "未知",
     "区政协副主席（不驻会）", "中国人民政治协商会议北京市西城区委员会", "bjxch.gov.cn/xxgk/ldzc.html"),
    ("xicheng_guo_hailong", "郭海龙", "男", "汉族", "1971年5月", "未知", "大学", "中共党员", "未知",
     "区政协党组成员、秘书长", "中国人民政治协商会议北京市西城区委员会", "bjxch.gov.cn/xxgk/ldzc.html"),

    # ── Predecessors ──
    ("xicheng_sun_jun", "孙硕", "男", "汉族", "1974年11月", "未知", "研究生/经济学博士", "中共党员", "未知",
     "前区委书记（现任北京市副市长）", "北京市人民政府（已离任）", "known_public_record"),
    ("xicheng_liu_yuebo", "刘月波", "未知", "未知", "未知", "未知", "未知", "未知", "未知",
     "前区长", "西城区（已离任）", "bjxch.gov.cn"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("xicheng_party_committee", "中共北京市西城区委员会", "党委", "地厅级（副省级城市下辖区为副厅级，直辖市辖区为正厅级）", "中共北京市委", "北京市西城区"),
    ("xicheng_gov", "北京市西城区人民政府", "政府", "正厅级", "北京市人民政府", "北京市西城区"),
    ("xicheng_discipline", "中共北京市西城区纪律检查委员会", "纪委", "正厅级", "北京市纪委", "北京市西城区"),
    ("xicheng_org_department", "中共北京市西城区委组织部", "党委部门", "正处级", "西城区委", "北京市西城区"),
    ("xicheng_propaganda", "中共北京市西城区委宣传部", "党委部门", "正处级", "西城区委", "北京市西城区"),
    ("xicheng_united_front", "中共北京市西城区委统战部", "党委部门", "正处级", "西城区委", "北京市西城区"),
    ("xicheng_political_legal", "中共北京市西城区委政法委员会", "党委部门", "正处级", "西城区委", "北京市西城区"),
    ("xicheng_armed_forces", "北京市西城区人民武装部", "军队", "正师级", "北京卫戍区", "北京市西城区"),
    ("xicheng_party_school", "中共北京市西城区委党校", "事业单位", "正处级", "西城区委", "北京市西城区"),
    ("xicheng_public_security", "北京市公安局西城分局", "公安", "正处级", "北京市公安局", "北京市西城区"),
    ("xicheng_financial_street", "北京金融街党工委", "党委", "正处级", "西城区委", "北京市西城区"),
    ("xicheng_peoples_congress", "北京市西城区人民代表大会常务委员会", "人大", "正厅级", "北京市人大常委会", "北京市西城区"),
    ("xicheng_cppcc", "中国人民政治协商会议北京市西城区委员会", "政协", "正厅级", "北京市政协", "北京市西城区"),
]

# Person → Organization positions
POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ── 刘东伟（区委书记）──
    ("xicheng_liu_dongwei", "xicheng_party_committee", "区委书记", "2023-12", "至今", "正厅级", "主持区委全面工作"),
    ("xicheng_liu_dongwei", "xicheng_gov", "区长", "2020-07", "2023-12", "正厅级", "前任区长职务"),
    # 刘东伟此前曾在北京市委办公厅、北京市工作

    # ── 郅海杰（区长）──
    ("xicheng_zhi_haijie", "xicheng_gov", "区长", "2025-01", "至今", "正厅级", "区政府全面工作"),
    ("xicheng_zhi_haijie", "xicheng_gov", "代区长", "2024-12", "2025-01", "正厅级", "过渡期"),
    # 郅海杰此前曾任北京市委相关工作

    # ── 蔡兵（副书记）──
    ("xicheng_cai_bing", "xicheng_party_committee", "区委副书记", "2025-?", "至今", "正厅级", "兼任党校校长"),
    ("xicheng_cai_bing", "xicheng_party_school", "区委党校校长", "2025-?", "至今", "正厅级", "兼任"),

    # ── 吴斌（纪委书记）──
    ("xicheng_wu_bin", "xicheng_discipline", "区纪委书记/监委主任", "2025-?", "至今", "正厅级", "二级高级监察官"),

    # ── 刘梅英（常务副区长）──
    ("xicheng_liu_meiying", "xicheng_gov", "常务副区长", "2025-?", "至今", "副厅级", "区委常委、党组副书记"),
    ("xicheng_liu_meiying", "xicheng_financial_street", "金融街党工委书记", "2025-?", "至今", "兼任", ""),

    # ── 张晓家（宣传部部长）──
    ("xicheng_zhang_xiaojia", "xicheng_propaganda", "宣传部部长", "2023-?", "至今", "副厅级", ""),

    # ── 王波（副区长）──
    ("xicheng_wang_bo", "xicheng_gov", "副区长", "2021-?", "至今", "副厅级", "区委常委"),

    # ── 江岚（统战部部长）──
    ("xicheng_jiang_lan", "xicheng_united_front", "统战部部长", "2023-?", "至今", "副厅级", ""),

    # ── 刘峙（武装部部长）──
    ("xicheng_liu_zhi", "xicheng_armed_forces", "武装部部长", "2021-?", "至今", "副师级", ""),

    # ── 于家明（组织部部长）──
    ("xicheng_yu_jiaming", "xicheng_org_department", "组织部部长", "2023-?", "至今", "副厅级", ""),

    # ── 高云飞（政法委书记）──
    ("xicheng_gao_yunfei", "xicheng_political_legal", "政法委书记", "2025-?", "至今", "副厅级", ""),

    # ── 区政府副区长 ──
    ("xicheng_song_mei", "xicheng_gov", "副区长", "2021-?", "至今", "副厅级", "农工党"),
    ("xicheng_zhu_haibin", "xicheng_gov", "副区长", "2022-?", "至今", "副厅级", ""),
    ("xicheng_li_jianxi", "xicheng_gov", "副区长", "2023-?", "至今", "副厅级", ""),
    ("xicheng_fan_yang", "xicheng_gov", "副区长", "2025-?", "至今", "副厅级", "兼任公安分局局长"),
    ("xicheng_fan_yang", "xicheng_public_security", "公安分局局长", "2025-?", "至今", "正处级", ""),
    ("xicheng_bing_hao", "xicheng_gov", "副区长", "2023-?", "至今", "副厅级", ""),
    ("xicheng_guo_jie", "xicheng_gov", "副区长（挂职）", "2025-?", "至今", "副厅级", ""),
    ("xicheng_du_hongyue", "xicheng_gov", "副区长", "2025-?", "至今", "副厅级", ""),
    ("xicheng_hong_yingzi", "xicheng_gov", "副区长（挂职）", "2026-?", "至今", "副厅级", ""),

    # ── 人大 ──
    ("xicheng_cheng_changhong", "xicheng_peoples_congress", "主任", "2021-?", "至今", "正厅级", ""),
    ("xicheng_xu_xiaohong", "xicheng_peoples_congress", "副主任", "2021-?", "至今", "副厅级", ""),
    ("xicheng_li_hua", "xicheng_peoples_congress", "副主任", "2021-?", "至今", "副厅级", ""),
    ("xicheng_wang_xiaonong", "xicheng_peoples_congress", "副主任", "2021-?", "至今", "副厅级", ""),
    ("xicheng_zhang_ding", "xicheng_peoples_congress", "副主任", "2024-?", "至今", "副厅级", ""),
    ("xicheng_yuan_li", "xicheng_peoples_congress", "副主任", "2024-?", "至今", "副厅级", ""),
    ("xicheng_li_cheng", "xicheng_peoples_congress", "副主任", "2024-?", "至今", "副厅级", ""),
    ("xicheng_wang_zhe", "xicheng_peoples_congress", "副主任（不驻会）", "2024-?", "至今", "副厅级", ""),

    # ── 政协 ──
    ("xicheng_liu_guoqiang", "xicheng_cppcc", "主席", "2024-?", "至今", "正厅级", ""),
    ("xicheng_peng_xiuying", "xicheng_cppcc", "副主席", "2021-?", "至今", "副厅级", ""),
    ("xicheng_tu_yunguo", "xicheng_cppcc", "副主席", "2024-?", "至今", "副厅级", ""),
    ("xicheng_chen_xin", "xicheng_cppcc", "副主席", "2021-?", "至今", "副厅级", ""),
    ("xicheng_yang_qiu", "xicheng_cppcc", "副主席（不驻会）", "2021-?", "至今", "副厅级", ""),
    ("xicheng_guan_zhenpeng", "xicheng_cppcc", "副主席（不驻会）", "2021-?", "至今", "副厅级", ""),
    ("xicheng_wang_jinglan", "xicheng_cppcc", "副主席（不驻会）", "2024-?", "至今", "副厅级", ""),
    ("xicheng_guo_hailong", "xicheng_cppcc", "秘书长", "2021-?", "至今", "正处级", ""),

    # ── 孙硕（前任区委书记）──
    ("xicheng_sun_jun", "xicheng_party_committee", "区委书记", "2021-07", "2023-12", "正厅级", "后升任北京市副市长"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period
    # Top leadership dyads
    ("xicheng_liu_dongwei", "xicheng_zhi_haijie", "predecessor_successor", "前任区长→现任区长（区委书记调任后）", "西城区政府", "2020-2023"),
    ("xicheng_liu_dongwei", "xicheng_zhi_haijie", "superior_subordinate", "区委书记→区长，党政一把手搭档", "西城区委/区政府", "2025-至今"),
    ("xicheng_liu_dongwei", "xicheng_sun_jun", "predecessor_successor", "接替孙硕任区委书记", "西城区委", "2023-12"),
    ("xicheng_zhi_haijie", "xicheng_liu_meiying", "superior_subordinate", "区长→常务副区长", "西城区政府", "2025-至今"),
]


# ════════════════════════════════════════════════════════════
# SQLITE BUILD
# ════════════════════════════════════════════════════════════

def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)", pos)
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()


# ════════════════════════════════════════════════════════════
# GEXF BUILD
# ════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def is_top_leader(p):
    return "区委书记" in p[9] or ("区委副书记" in p[9] and "区长" in p[9]) or "区长" in p[9]

def person_color(p):
    role = p[9]
    if "区委书记" in role and "副书记" not in role:
        return "255,50,50"
    if "区长" in role:
        return "50,100,255"
    if "纪委书记" in role or "监委" in role:
        return "255,165,0"
    return "100,100,100"

def org_color(org_type):
    t = org_type or ""
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    return "200,200,200"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>北京市西城区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        name = esc(p[1])
        role = esc(p[9])
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{pid}" label="{name}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append('        </attvalues>')
        cs = c.split(",")
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in ORGANIZATIONS:
        oid = o[0]
        name = esc(o[1])
        otype = esc(o[2] or "")
        c = org_color(otype)
        lines.append(f'      <node id="{oid}" label="{name}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="2" value="{otype}"/>')
        lines.append('        </attvalues>')
        cs = c.split(",")
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in POSITIONS:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{pos[0]}" target="{pos[1]}" label="{esc(pos[2])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos[5] or "")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in RELATIONSHIPS:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{r[0]}" target="{r[1]}" label="{esc(r[3])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r[3])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════

def main():
    print("Building 西城区 network database...")
    build_database()
    print(f"  DB: {DB_PATH}")

    print("Building 西城区 network graph...")
    build_gexf()
    print(f"  GEXF: {GEXF_PATH}")

    # Summary stats
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    print()
    print("Summary:")
    for table in ["persons", "organizations", "positions", "relationships"]:
        count = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count}")
    conn.close()
    print()
    print("Done.")


if __name__ == "__main__":
    main()
