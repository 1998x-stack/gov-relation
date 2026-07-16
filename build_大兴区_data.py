#!/usr/bin/env python3
"""
北京市大兴区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Daxing District leadership.

Data source: bjdx.gov.cn (official leadership page, accessed 2026-07-16)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "大兴区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "大兴区_network.gexf")

# ════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════

# Person ID convention: daxing_{surname_givenname}
PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source
    # ── Top leaders ──
    ("daxing_chu_junwei", "初军威", "男", "汉族", "1971年12月", "未知", "在职研究生/管理学博士", "中共党员", "未知",
     "区委书记", "中共北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qwld/717055/index.html"),
    ("daxing_liu_yang", "刘洋", "男", "汉族", "1974年3月", "未知", "中央党校研究生", "中共党员", "未知",
     "区委副书记、区长", "北京市大兴区人民政府", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qzfld/717125/index.html"),

    # ── Standing Committee (常委) ──
    ("daxing_qing_zhaoshen", "庆兆珅", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委副书记", "中共北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qwld/717046/index.html"),
    ("daxing_huang_xiaowen", "黄晓文", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委", "中共北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qwld/1456125/index.html"),
    ("daxing_guo_wenjie", "郭文杰", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委、副区长", "北京市大兴区人民政府", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qwld/725731/index.html"),
    ("daxing_zhang_bo", "张博", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委", "中共北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qwld/717034/index.html"),
    ("daxing_cai_xiaojun", "蔡小军", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委、区政协党组副书记", "中国人民政治协商会议北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qwld/717043/index.html"),
    ("daxing_bao_ru", "薄茹", "女", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委", "中共北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qwld/717049/index.html"),
    ("daxing_zhang_shuying", "张树鹰", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委", "中共北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qwld/717016/index.html"),
    ("daxing_zhou_chong", "周冲", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委、副区长", "北京市大兴区人民政府", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qwld/2313902/index.html"),
    ("daxing_zhang_guoyu", "张国宇", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委", "中共北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qwld/1859717/index.html"),

    # ── District Government Vice Heads ──
    ("daxing_yang_junling", "杨峻岭", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "副区长", "北京市大兴区人民政府", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qzfld/717082/index.html"),
    ("daxing_zhang_xiaosheng", "张晓晟", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "副区长", "北京市大兴区人民政府", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qzfld/1456215/index.html"),
    ("daxing_zhai_yang", "翟杨", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "副区长", "北京市大兴区人民政府", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qzfld/717115/index.html"),
    ("daxing_cong_weiqing", "丛威青", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "副区长", "北京市大兴区人民政府", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qzfld/717078/index.html"),
    ("daxing_wang_yiming", "王逸鸣", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "副区长", "北京市大兴区人民政府", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qzfld/2288651/index.html"),
    ("daxing_liu_qilong", "刘其龙", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "副区长", "北京市大兴区人民政府", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qzfld/2125515/index.html"),

    # ── People's Congress ──
    ("daxing_ai_li", "艾丽", "女", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区人大常委会党组书记、主任", "北京市大兴区人民代表大会常务委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qrdld/717074/index.html"),
    ("daxing_li_da", "李达", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区人大常委会副主任", "北京市大兴区人民代表大会常务委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qrdld/717059/index.html"),
    ("daxing_wang_xuejun", "王学军", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区人大常委会副主任", "北京市大兴区人民代表大会常务委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qrdld/717071/index.html"),
    ("daxing_wang_sen", "王森", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区人大常委会副主任", "北京市大兴区人民代表大会常务委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qrdld/717062/index.html"),
    ("daxing_zhou_xuefeng", "周雪峰", "未知", "未知", "未知", "未知", "未知", "未知", "未知",
     "区人大常委会副主任（不驻会）", "北京市大兴区人民代表大会常务委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qrdld/717068/index.html"),

    # ── CPPCC ──
    ("daxing_yu_xueyin", "禹学垠", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区政协党组书记、主席", "中国人民政治协商会议北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qzxld/717155/index.html"),
    ("daxing_geng_xiaomei", "耿晓梅", "女", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区政协副主席", "中国人民政治协商会议北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qzxld/717149/index.html"),
    ("daxing_feng_xiuhai", "冯秀海", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区政协副主席", "中国人民政治协商会议北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qzxld/717146/index.html"),
    ("daxing_zhuang_weihua", "庄卫华", "女", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区政协副主席", "中国人民政治协商会议北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qzxld/2291599/index.html"),
    ("daxing_liu_huixin", "刘会新", "未知", "未知", "未知", "未知", "未知", "未知", "未知",
     "区政协副主席（不驻会）", "中国人民政治协商会议北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qzxld/717137/index.html"),
    ("daxing_zhang_xuefei", "张雪飞", "未知", "未知", "未知", "未知", "未知", "未知", "未知",
     "区政协副主席（不驻会）", "中国人民政治协商会议北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qzxld/717143/index.html"),
    ("daxing_zhao_jianguo", "赵建国", "未知", "未知", "未知", "未知", "未知", "未知", "未知",
     "区政协副主席（不驻会）", "中国人民政治协商会议北京市大兴区委员会", "bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/qzxld/717140/index.html"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("daxing_party_committee", "中共北京市大兴区委员会", "党委", "正厅级（直辖市辖区）", "中共北京市委", "北京市大兴区"),
    ("daxing_gov", "北京市大兴区人民政府", "政府", "正厅级（直辖市辖区）", "北京市人民政府", "北京市大兴区"),
    ("daxing_peoples_congress", "北京市大兴区人民代表大会常务委员会", "人大", "正厅级（直辖市辖区）", "北京市人大常委会", "北京市大兴区"),
    ("daxing_cppcc", "中国人民政治协商会议北京市大兴区委员会", "政协", "正厅级（直辖市辖区）", "北京市政协", "北京市大兴区"),
    ("daxing_linjing_party_work", "中共北京市委大兴国际机场临空经济区（大兴）工作委员会", "党委", "正厅级", "中共北京市委", "北京市大兴区"),
    ("daxing_linjing_manage", "北京大兴国际机场临空经济区（大兴）管理委员会", "政府派出机构", "正厅级", "北京市人民政府", "北京市大兴区"),
    ("daxing_ftz_office", "中国（河北）自由贸易试验区大兴机场片区（北京大兴）管理委员会", "政府派出机构", "正厅级", "北京市人民政府", "北京市大兴区"),
    ("daxing_airport_prep", "北京新机场建设大兴区筹备办公室", "政府临时机构", "正厅级", "大兴区政府", "北京市大兴区"),
]

# Person → Organization positions
POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ── 初军威（区委书记）──
    ("daxing_chu_junwei", "daxing_party_committee", "区委书记", "2024-?", "至今", "正厅级", "主持区委全面工作"),
    ("daxing_chu_junwei", "daxing_linjing_party_work", "临空区党工委书记（兼）", "2024-?", "至今", "正厅级", "兼任"),

    # ── 刘洋（区长）──
    ("daxing_liu_yang", "daxing_gov", "区长", "2025-?", "至今", "正厅级", "区政府全面工作"),
    ("daxing_liu_yang", "daxing_party_committee", "区委副书记", "2025-?", "至今", "正厅级", ""),
    ("daxing_liu_yang", "daxing_linjing_party_work", "临空区党工委副书记（兼）", "2025-?", "至今", "正厅级", "兼任"),
    ("daxing_liu_yang", "daxing_linjing_manage", "临空区管委会主任（兼）", "2025-?", "至今", "正厅级", "兼任"),
    ("daxing_liu_yang", "daxing_ftz_office", "自贸区大兴机场片区管委会主任（兼）", "2025-?", "至今", "正厅级", "兼任"),
    ("daxing_liu_yang", "daxing_airport_prep", "北京新机场建设大兴区筹备办公室主任（兼）", "2025-?", "至今", "正厅级", "兼任"),

    # ── 庆兆珅（副书记）──
    ("daxing_qing_zhaoshen", "daxing_party_committee", "区委副书记", "2024-?", "至今", "正厅级", ""),

    # ── 常委兼副区长 ──
    ("daxing_guo_wenjie", "daxing_party_committee", "区委常委", "2025-?", "至今", "副厅级", ""),
    ("daxing_guo_wenjie", "daxing_gov", "副区长", "2025-?", "至今", "副厅级", "区委常委"),
    ("daxing_zhou_chong", "daxing_party_committee", "区委常委", "2024-?", "至今", "副厅级", ""),
    ("daxing_zhou_chong", "daxing_gov", "副区长", "2024-?", "至今", "副厅级", "区委常委"),

    # ── 其他常委 ──
    ("daxing_huang_xiaowen", "daxing_party_committee", "区委常委", "2025-?", "至今", "副厅级", ""),
    ("daxing_zhang_bo", "daxing_party_committee", "区委常委", "2021-?", "至今", "副厅级", ""),
    ("daxing_cai_xiaojun", "daxing_party_committee", "区委常委", "2023-?", "至今", "副厅级", "兼政协党组副书记"),
    ("daxing_cai_xiaojun", "daxing_cppcc", "政协党组副书记", "2023-?", "至今", "副厅级", "区委常委兼"),
    ("daxing_bao_ru", "daxing_party_committee", "区委常委", "2024-?", "至今", "副厅级", ""),
    ("daxing_zhang_shuying", "daxing_party_committee", "区委常委", "2025-?", "至今", "副厅级", ""),
    ("daxing_zhang_guoyu", "daxing_party_committee", "区委常委", "2026-?", "至今", "副厅级", ""),

    # ── 副区长 ──
    ("daxing_yang_junling", "daxing_gov", "副区长", "2025-?", "至今", "副厅级", ""),
    ("daxing_zhang_xiaosheng", "daxing_gov", "副区长", "2021-?", "至今", "副厅级", ""),
    ("daxing_zhai_yang", "daxing_gov", "副区长", "2021-?", "至今", "副厅级", ""),
    ("daxing_cong_weiqing", "daxing_gov", "副区长", "2026-?", "至今", "副厅级", ""),
    ("daxing_wang_yiming", "daxing_gov", "副区长", "2025-?", "至今", "副厅级", ""),
    ("daxing_liu_qilong", "daxing_gov", "副区长", "2026-?", "至今", "副厅级", ""),

    # ── 人大 ──
    ("daxing_ai_li", "daxing_peoples_congress", "主任", "2024-?", "至今", "正厅级", ""),
    ("daxing_li_da", "daxing_peoples_congress", "副主任", "2021-?", "至今", "副厅级", ""),
    ("daxing_wang_xuejun", "daxing_peoples_congress", "副主任", "2021-?", "至今", "副厅级", ""),
    ("daxing_wang_sen", "daxing_peoples_congress", "副主任", "2026-?", "至今", "副厅级", ""),
    ("daxing_zhou_xuefeng", "daxing_peoples_congress", "副主任（不驻会）", "2024-?", "至今", "副厅级", ""),

    # ── 政协 ──
    ("daxing_yu_xueyin", "daxing_cppcc", "主席", "2024-?", "至今", "正厅级", ""),
    ("daxing_geng_xiaomei", "daxing_cppcc", "副主席", "2024-?", "至今", "副厅级", ""),
    ("daxing_feng_xiuhai", "daxing_cppcc", "副主席", "2026-?", "至今", "副厅级", ""),
    ("daxing_zhuang_weihua", "daxing_cppcc", "副主席", "2026-?", "至今", "副厅级", ""),
    ("daxing_liu_huixin", "daxing_cppcc", "副主席（不驻会）", "2019-?", "至今", "副厅级", ""),
    ("daxing_zhang_xuefei", "daxing_cppcc", "副主席（不驻会）", "2021-?", "至今", "副厅级", ""),
    ("daxing_zhao_jianguo", "daxing_cppcc", "副主席（不驻会）", "2021-?", "至今", "副厅级", ""),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period
    # Top leadership dyads
    ("daxing_chu_junwei", "daxing_liu_yang", "superior_subordinate", "区委书记→区长，党政一把手搭档", "大兴区委/区政府", "2025-至今"),
    ("daxing_chu_junwei", "daxing_liu_yang", "overlap", "共同兼任临空经济区工作委员会职务", "临空区党工委", "2025-至今"),
    ("daxing_chu_junwei", "daxing_qing_zhaoshen", "superior_subordinate", "区委书记→区委副书记", "大兴区委", "2024-至今"),
    ("daxing_liu_yang", "daxing_qing_zhaoshen", "overlap", "区委副书记共事", "大兴区委", "2025-至今"),
    # Party Committee overlap
    ("daxing_chu_junwei", "daxing_guo_wenjie", "superior_subordinate", "区委书记→区委常委", "大兴区委", "2025-至今"),
    ("daxing_chu_junwei", "daxing_zhou_chong", "superior_subordinate", "区委书记→区委常委", "大兴区委", "2024-至今"),
    ("daxing_chu_junwei", "daxing_huang_xiaowen", "superior_subordinate", "区委书记→区委常委", "大兴区委", "2025-至今"),
    ("daxing_chu_junwei", "daxing_zhang_bo", "superior_subordinate", "区委书记→区委常委", "大兴区委", "2021-至今"),
    ("daxing_chu_junwei", "daxing_cai_xiaojun", "superior_subordinate", "区委书记→区委常委", "大兴区委", "2023-至今"),
    ("daxing_chu_junwei", "daxing_bao_ru", "superior_subordinate", "区委书记→区委常委", "大兴区委", "2024-至今"),
    ("daxing_chu_junwei", "daxing_zhang_shuying", "superior_subordinate", "区委书记→区委常委", "大兴区委", "2025-至今"),
    ("daxing_chu_junwei", "daxing_zhang_guoyu", "superior_subordinate", "区委书记→区委常委", "大兴区委", "2026-至今"),
    # Government overlap
    ("daxing_liu_yang", "daxing_guo_wenjie", "superior_subordinate", "区长→副区长（区委常委兼）", "大兴区政府", "2025-至今"),
    ("daxing_liu_yang", "daxing_zhou_chong", "superior_subordinate", "区长→副区长（区委常委兼）", "大兴区政府", "2024-至今"),
    ("daxing_liu_yang", "daxing_yang_junling", "superior_subordinate", "区长→副区长", "大兴区政府", "2025-至今"),
    ("daxing_liu_yang", "daxing_zhang_xiaosheng", "superior_subordinate", "区长→副区长", "大兴区政府", "2025-至今"),
    ("daxing_liu_yang", "daxing_zhai_yang", "superior_subordinate", "区长→副区长", "大兴区政府", "2025-至今"),
    ("daxing_liu_yang", "daxing_cong_weiqing", "superior_subordinate", "区长→副区长", "大兴区政府", "2026-至今"),
    ("daxing_liu_yang", "daxing_wang_yiming", "superior_subordinate", "区长→副区长", "大兴区政府", "2025-至今"),
    ("daxing_liu_yang", "daxing_liu_qilong", "superior_subordinate", "区长→副区长", "大兴区政府", "2026-至今"),
    # PCC chair - Party committee overlap
    ("daxing_yu_xueyin", "daxing_chu_junwei", "overlap", "政协主席与区委书记共事", "大兴区", "2024-至今"),
    ("daxing_ai_li", "daxing_chu_junwei", "overlap", "人大主任与区委书记共事", "大兴区", "2024-至今"),
    ("daxing_ai_li", "daxing_liu_yang", "overlap", "人大主任与区长共事", "大兴区", "2025-至今"),
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
    return "区委书记" in p[9] and "副书记" not in p[9] or ("区委副书记" in p[9] and "区长" in p[9])

def person_color(p):
    role = p[9]
    if "区委书记" in role and "副书记" not in role:
        return "255,50,50"
    if "区长" in role:
        return "50,100,255"
    return "100,100,100"

def org_color(org_type):
    t = org_type or ""
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>北京市大兴区领导班子工作关系网络</description>')
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
    print("Building 大兴区 network database...")
    build_database()
    print(f"  DB: {DB_PATH}")

    print("Building 大兴区 network graph...")
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
