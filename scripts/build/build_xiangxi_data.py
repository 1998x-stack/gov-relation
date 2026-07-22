"""
Build 湘西土家族苗族自治州 (Xiangxi Tujia-Miao Autonomous Prefecture)
Personnel Network Database + GEXF Graph

Data sourced from Wikipedia (Chinese) - July 2026
All URLs cited below.

Coverage:
- Prefecture level: 州委书记, 州长, 前任州委书记
- 8 counties/cities: 吉首市, 泸溪县, 凤凰县, 花垣县, 保靖县, 古丈县, 永顺县, 龙山县
- 16 county/city positions (县委书记/市委书记 + 县长/市长)
"""

import sqlite3
import os

DB_PATH = "data/database/xiangxi_network.db"
GEXF_PATH = "data/graph/xiangxi_network.gexf"

# ──────────────────────────────────────────────
# RAW DATA
# ──────────────────────────────────────────────

# --- Organizations ---
organizations = [
    # Prefecture level
    {"id": "xiangxi_zhouwei", "name": "中共湘西土家族苗族自治州委员会", "type": "prefecture_party", "level": "prefecture", "parent": "hunan_province", "location": "吉首市"},
    {"id": "xiangxi_zhouzhengfu", "name": "湘西土家族苗族自治州人民政府", "type": "prefecture_gov", "level": "prefecture", "parent": "hunan_province", "location": "吉首市"},
    {"id": "xiangxi_rd", "name": "湘西土家族苗族自治州人大常委会", "type": "prefecture_npc", "level": "prefecture", "parent": "hunan_province", "location": "吉首市"},
    {"id": "xiangxi_zx", "name": "政协湘西土家族苗族自治州委员会", "type": "prefecture_ccppcc", "level": "prefecture", "parent": "hunan_province", "location": "吉首市"},

    # County/ City level
    {"id": "jishou_shiwei", "name": "中共吉首市委员会", "type": "county_party", "level": "county", "parent": "xiangxi_zhouwei", "location": "吉首市"},
    {"id": "jishou_shizhengfu", "name": "吉首市人民政府", "type": "county_gov", "level": "county", "parent": "xiangxi_zhouzhengfu", "location": "吉首市"},
    {"id": "luxi_xianwei", "name": "中共泸溪县委员会", "type": "county_party", "level": "county", "parent": "xiangxi_zhouwei", "location": "泸溪县"},
    {"id": "luxi_xianzhengfu", "name": "泸溪县人民政府", "type": "county_gov", "level": "county", "parent": "xiangxi_zhouzhengfu", "location": "泸溪县"},
    {"id": "fenghuang_xianwei", "name": "中共凤凰县委员会", "type": "county_party", "level": "county", "parent": "xiangxi_zhouwei", "location": "凤凰县"},
    {"id": "fenghuang_xianzhengfu", "name": "凤凰县人民政府", "type": "county_gov", "level": "county", "parent": "xiangxi_zhouzhengfu", "location": "凤凰县"},
    {"id": "huayuan_xianwei", "name": "中共花垣县委员会", "type": "county_party", "level": "county", "parent": "xiangxi_zhouwei", "location": "花垣县"},
    {"id": "huayuan_xianzhengfu", "name": "花垣县人民政府", "type": "county_gov", "level": "county", "parent": "xiangxi_zhouzhengfu", "location": "花垣县"},
    {"id": "baojing_xianwei", "name": "中共保靖县委员会", "type": "county_party", "level": "county", "parent": "xiangxi_zhouwei", "location": "保靖县"},
    {"id": "baojing_xianzhengfu", "name": "保靖县人民政府", "type": "county_gov", "level": "county", "parent": "xiangxi_zhouzhengfu", "location": "保靖县"},
    {"id": "guzhang_xianwei", "name": "中共古丈县委员会", "type": "county_party", "level": "county", "parent": "xiangxi_zhouwei", "location": "古丈县"},
    {"id": "guzhang_xianzhengfu", "name": "古丈县人民政府", "type": "county_gov", "level": "county", "parent": "xiangxi_zhouzhengfu", "location": "古丈县"},
    {"id": "yongshun_xianwei", "name": "中共永顺县委员会", "type": "county_party", "level": "county", "parent": "xiangxi_zhouwei", "location": "永顺县"},
    {"id": "yongshun_xianzhengfu", "name": "永顺县人民政府", "type": "county_gov", "level": "county", "parent": "xiangxi_zhouzhengfu", "location": "永顺县"},
    {"id": "longshan_xianwei", "name": "中共龙山县委员会", "type": "county_party", "level": "county", "parent": "xiangxi_zhouwei", "location": "龙山县"},
    {"id": "longshan_xianzhengfu", "name": "龙山县人民政府", "type": "county_gov", "level": "county", "parent": "xiangxi_zhouzhengfu", "location": "龙山县"},
]

# --- Persons ---
persons = [
    # Prefecture level
    {"id": "xiangxi_liu_tao", "name": "刘涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1971年6月", "birthplace": "河南省方城县",
     "education": "研究生（河南大学中国现代文学硕士）",
     "party_join": "1996年11月", "work_start": "1997年7月",
     "current_post": "湘西州委书记", "current_org": "中共湘西土家族苗族自治州委员会",
     "source": "https://zh.wikipedia.org/wiki/刘涛_(1971年)"},

    {"id": "xiangxi_shang_shenglong", "name": "尚生龙", "gender": "男", "ethnicity": "土家族",
     "birth": "1972年5月", "birthplace": "湖南省桑植县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "湘西州州长（代理）", "current_org": "湘西土家族苗族自治州人民政府",
     "source": "https://zh.wikipedia.org/wiki/湘西土家族苗族自治州"},

    {"id": "xiangxi_guo_zhenggui", "name": "虢正贵", "gender": "男", "ethnicity": "汉族",
     "birth": "1964年9月", "birthplace": "湖南省长沙市望城区",
     "education": "大专（长沙基础大学物理专业）",
     "party_join": "1984年6月", "work_start": "1984年7月",
     "current_post": "湖南省政协副主席", "current_org": "湖南省政协",
     "source": "https://zh.wikipedia.org/wiki/虢正贵"},

    {"id": "xiangxi_chen_hua", "name": "陈华", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "前任州长（另有任用）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/湘西土家族苗族自治州"},

    {"id": "xiangxi_gong_minghan", "name": "龚明汉", "gender": "男", "ethnicity": "汉族",
     "birth": "1964年9月", "birthplace": "湖南省张家界市永定区",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "州人大常委会主任", "current_org": "湘西土家族苗族自治州人大常委会",
     "source": "https://zh.wikipedia.org/wiki/湘西土家族苗族自治州"},

    {"id": "xiangxi_xiang_bangwei", "name": "向邦伟", "gender": "男", "ethnicity": "土家族",
     "birth": "1969年3月", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "州政协主席", "current_org": "政协湘西土家族苗族自治州委员会",
     "source": "https://zh.wikipedia.org/wiki/湘西土家族苗族自治州"},

    # Jishou City
    {"id": "jishou_zhou_lizhi", "name": "周立志", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年5月", "birthplace": "湖南省永州市",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "吉首市委书记", "current_org": "中共吉首市委员会",
     "source": "https://zh.wikipedia.org/wiki/吉首市"},

    {"id": "jishou_fu_jiasheng", "name": "符家盛", "gender": "男", "ethnicity": "苗族",
     "birth": "1973年4月", "birthplace": "湖南省龙山县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "吉首市市长", "current_org": "吉首市人民政府",
     "source": "https://zh.wikipedia.org/wiki/吉首市"},

    # Luxi County
    {"id": "luxi_peng_wuxue", "name": "彭武学", "gender": "男", "ethnicity": "土家族",
     "birth": "1971年5月", "birthplace": "湖南省永顺县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "泸溪县委书记", "current_org": "中共泸溪县委员会",
     "source": "https://zh.wikipedia.org/wiki/泸溪县"},

    {"id": "luxi_fu_jiabo", "name": "符家波", "gender": "男", "ethnicity": "苗族",
     "birth": "1979年5月", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "泸溪县县长", "current_org": "泸溪县人民政府",
     "source": "https://zh.wikipedia.org/wiki/泸溪县"},

    # Fenghuang County
    {"id": "fenghuang_mao_jia", "name": "毛家", "gender": "男", "ethnicity": "土家族",
     "birth": "1973年10月", "birthplace": "湖南省永顺县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "凤凰县委书记", "current_org": "中共凤凰县委员会",
     "source": "https://zh.wikipedia.org/wiki/凤凰县"},

    {"id": "fenghuang_fan_zhongqing", "name": "樊忠清", "gender": "男", "ethnicity": "苗族",
     "birth": "1975年10月", "birthplace": "湖南省花垣县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "凤凰县县长", "current_org": "凤凰县人民政府",
     "source": "https://zh.wikipedia.org/wiki/凤凰县"},

    # Huayuan County
    {"id": "huayuan_wang_jinghai", "name": "王京海", "gender": "男", "ethnicity": "土家族",
     "birth": "1975年9月", "birthplace": "湖南省慈利县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "花垣县委书记兼县长", "current_org": "中共花垣县委员会",
     "source": "https://zh.wikipedia.org/wiki/花垣县"},

    # Baojing County
    {"id": "baojing_zhou_jianwu", "name": "周建武", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年11月", "birthplace": "湖南省涟源市",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "保靖县委书记", "current_org": "中共保靖县委员会",
     "source": "https://zh.wikipedia.org/wiki/保靖县"},

    {"id": "baojing_guo_yingxiang", "name": "郭应湘", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年6月", "birthplace": "湖南省桂东县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "保靖县县长", "current_org": "保靖县人民政府",
     "source": "https://zh.wikipedia.org/wiki/保靖县"},

    # Guzhang County
    {"id": "guzhang_teng_zhaohui", "name": "滕朝辉", "gender": "男", "ethnicity": "土家族",
     "birth": "1974年10月", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古丈县委书记", "current_org": "中共古丈县委员会",
     "source": "https://zh.wikipedia.org/wiki/古丈县"},

    {"id": "guzhang_chen_jianxin", "name": "陈建新", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年6月", "birthplace": "湖南省衡东县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古丈县县长", "current_org": "古丈县人民政府",
     "source": "https://zh.wikipedia.org/wiki/古丈县"},

    # Yongshun County
    {"id": "yongshun_xiang_jiamao", "name": "向加茂", "gender": "男", "ethnicity": "苗族",
     "birth": "1973年2月", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "永顺县委书记兼县长", "current_org": "中共永顺县委员会",
     "source": "https://zh.wikipedia.org/wiki/永顺县"},

    # Longshan County
    {"id": "longshan_shi_rongfen", "name": "时荣芬", "gender": "女", "ethnicity": "苗族",
     "birth": "1976年12月", "birthplace": "湖南省花垣县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "龙山县县委书记", "current_org": "中共龙山县委员会",
     "source": "https://zh.wikipedia.org/wiki/龙山县"},

    {"id": "longshan_zhou_shengyi", "name": "周胜益", "gender": "男", "ethnicity": "苗族",
     "birth": "1972年9月", "birthplace": "湖南省保靖县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "龙山县县长", "current_org": "龙山县人民政府",
     "source": "https://zh.wikipedia.org/wiki/龙山县"},
]

# --- Positions (person -> org) ---
positions = [
    # Prefecture level
    {"person_id": "xiangxi_liu_tao", "org_id": "xiangxi_zhouwei", "title": "州委书记", "start": "2024年10月", "end": "", "rank": "正厅级"},
    {"person_id": "xiangxi_shang_shenglong", "org_id": "xiangxi_zhouzhengfu", "title": "州长（代理）", "start": "2026年6月", "end": "", "rank": "正厅级"},
    {"person_id": "xiangxi_guo_zhenggui", "org_id": "xiangxi_zhouwei", "title": "前任州委书记", "start": "2021年3月", "end": "2024年10月", "rank": "正厅级"},
    {"person_id": "xiangxi_gong_minghan", "org_id": "xiangxi_rd", "title": "州人大常委会主任", "start": "2021年1月", "end": "", "rank": "正厅级"},
    {"person_id": "xiangxi_xiang_bangwei", "org_id": "xiangxi_zx", "title": "州政协主席", "start": "2026年2月", "end": "", "rank": "正厅级"},

    # Jishou
    {"person_id": "jishou_zhou_lizhi", "org_id": "jishou_shiwei", "title": "市委书记", "start": "2023年10月", "end": "", "rank": "正处级"},
    {"person_id": "jishou_fu_jiasheng", "org_id": "jishou_shizhengfu", "title": "市长", "start": "2020年4月", "end": "", "rank": "正处级"},

    # Luxi
    {"person_id": "luxi_peng_wuxue", "org_id": "luxi_xianwei", "title": "县委书记", "start": "2021年6月", "end": "", "rank": "正处级"},
    {"person_id": "luxi_fu_jiabo", "org_id": "luxi_xianzhengfu", "title": "县长", "start": "2023年11月", "end": "", "rank": "正处级"},

    # Fenghuang
    {"person_id": "fenghuang_mao_jia", "org_id": "fenghuang_xianwei", "title": "县委书记", "start": "2022年1月", "end": "", "rank": "正处级"},
    {"person_id": "fenghuang_fan_zhongqing", "org_id": "fenghuang_xianzhengfu", "title": "县长", "start": "2022年3月", "end": "", "rank": "正处级"},

    # Huayuan
    {"person_id": "huayuan_wang_jinghai", "org_id": "huayuan_xianwei", "title": "县委书记", "start": "2025年2月", "end": "", "rank": "正处级"},
    {"person_id": "huayuan_wang_jinghai", "org_id": "huayuan_xianzhengfu", "title": "县长", "start": "2022年3月", "end": "", "rank": "正处级"},

    # Baojing
    {"person_id": "baojing_zhou_jianwu", "org_id": "baojing_xianwei", "title": "县委书记", "start": "2024年6月", "end": "", "rank": "正处级"},
    {"person_id": "baojing_guo_yingxiang", "org_id": "baojing_xianzhengfu", "title": "县长", "start": "2024年7月", "end": "", "rank": "正处级"},

    # Guzhang
    {"person_id": "guzhang_teng_zhaohui", "org_id": "guzhang_xianwei", "title": "县委书记", "start": "2023年12月", "end": "", "rank": "正处级"},
    {"person_id": "guzhang_chen_jianxin", "org_id": "guzhang_xianzhengfu", "title": "县长", "start": "2024年7月", "end": "", "rank": "正处级"},

    # Yongshun
    {"person_id": "yongshun_xiang_jiamao", "org_id": "yongshun_xianwei", "title": "县委书记", "start": "2025年2月", "end": "", "rank": "正处级"},
    {"person_id": "yongshun_xiang_jiamao", "org_id": "yongshun_xianzhengfu", "title": "县长", "start": "2021年10月", "end": "", "rank": "正处级"},

    # Longshan
    {"person_id": "longshan_shi_rongfen", "org_id": "longshan_xianwei", "title": "县委书记", "start": "2022年1月", "end": "", "rank": "正处级"},
    {"person_id": "longshan_zhou_shengyi", "org_id": "longshan_xianzhengfu", "title": "县长", "start": "2022年3月", "end": "", "rank": "正处级"},
]

# --- Relationships (person -> person) ---
relationships = [
    # 虢正贵 -> 刘涛 (successor)
    {"person_a": "xiangxi_guo_zhenggui", "person_b": "xiangxi_liu_tao",
     "type": "successor", "context": "虢正贵2024年10月卸任后刘涛接任湘西州委书记",
     "overlap_org": "xiangxi_zhouwei", "overlap_period": "2024年10月"},

    # 刘涛 -> 尚生龙 (party secretary - governor)
    {"person_a": "xiangxi_liu_tao", "person_b": "xiangxi_shang_shenglong",
     "type": "colleague", "context": "刘涛（州委书记）与尚生龙（代州长）搭班",
     "overlap_org": "xiangxi_zhouwei", "overlap_period": "2026年6月起"},

    # 周立志(吉首书记) <-> 符家盛(吉首市长)
    {"person_a": "jishou_zhou_lizhi", "person_b": "jishou_fu_jiasheng",
     "type": "colleague", "context": "周立志（吉首市委书记）与符家盛（吉首市长）搭班",
     "overlap_org": "jishou_shiwei", "overlap_period": "2023年10月起"},

    # 彭武学(泸溪书记) <-> 符家波(泸溪县长)
    {"person_a": "luxi_peng_wuxue", "person_b": "luxi_fu_jiabo",
     "type": "colleague", "context": "彭武学（泸溪县委书记）与符家波（泸溪县长）搭班",
     "overlap_org": "luxi_xianwei", "overlap_period": "2023年11月起"},

    # 毛家(凤凰书记) <-> 樊忠清(凤凰县长)
    {"person_a": "fenghuang_mao_jia", "person_b": "fenghuang_fan_zhongqing",
     "type": "colleague", "context": "毛家（凤凰县委书记）与樊忠清（凤凰县长）搭班",
     "overlap_org": "fenghuang_xianwei", "overlap_period": "2022年3月起"},

    # 周建武(保靖书记) <-> 郭应湘(保靖县长)
    {"person_a": "baojing_zhou_jianwu", "person_b": "baojing_guo_yingxiang",
     "type": "colleague", "context": "周建武（保靖县委书记）与郭应湘（保靖县长）搭班",
     "overlap_org": "baojing_xianwei", "overlap_period": "2024年7月起"},

    # 滕朝辉(古丈书记) <-> 陈建新(古丈县长)
    {"person_a": "guzhang_teng_zhaohui", "person_b": "guzhang_chen_jianxin",
     "type": "colleague", "context": "滕朝辉（古丈县委书记）与陈建新（古丈县长）搭班",
     "overlap_org": "guzhang_xianwei", "overlap_period": "2024年7月起"},

    # 时荣芬(龙山书记) <-> 周胜益(龙山县长)
    {"person_a": "longshan_shi_rongfen", "person_b": "longshan_zhou_shengyi",
     "type": "colleague", "context": "时荣芬（龙山县委书记）与周胜益（龙山县县长）搭班",
     "overlap_org": "longshan_xianwei", "overlap_period": "2022年3月起"},

    # Cross-county connections: Same birthplace connections
    {"person_a": "xiangxi_guo_zhenggui", "person_b": "xiangxi_liu_tao",
     "type": "cross_province", "context": "虢正贵（湖南本土）→ 刘涛（河南跨省调任），湘西州委书记首次外省调入",
     "overlap_org": "", "overlap_period": "2024年"},
]


# ──────────────────────────────────────────────
# BUILD SQLite DATABASE
# ──────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
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
    person_id TEXT,
    org_id TEXT,
    title TEXT,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a TEXT,
    person_b TEXT,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for org in organizations:
    c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
              (org["id"], org["name"], org["type"], org["level"], org["parent"], org["location"]))

for p in persons:
    c.execute("INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
               p["education"], p["party_join"], p["work_start"],
               p["current_post"], p["current_org"], p["source"]))

for pos in positions:
    c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank) VALUES (?,?,?,?,?,?)",
              (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"]))

for r in relationships:
    c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
              (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()

print(f"✅ SQLite DB created: {DB_PATH}")


# ──────────────────────────────────────────────
# BUILD GEXF GRAPH
# ──────────────────────────────────────────────

def role_color(pid):
    """Determine node color by role."""
    for p in persons:
        if p["id"] == pid:
            post = p["current_post"]
            if "书记" in post and "州" in p.get("current_org", ""):
                return "#E03C31"  # red - party secretary (prefecture)
            elif "书记" in post and ("县委" in p.get("current_org", "") or "市委" in p.get("current_org", "")):
                return "#E03C31"  # red - county/city party secretary
            elif "州长" in post or "县长" in post or "市长" in post:
                return "#2563EB"  # blue - government leader
            elif "主任" in post:
                return "#F59E0B"  # orange - NPC
            elif "主席" in post:
                return "#8B5CF6"  # purple - CPPCC
            else:
                return "#6B7280"  # grey - other
    return "#6B7280"

def org_color(org_type):
    if "party" in org_type:
        return "#E03C31"
    elif "gov" in org_type:
        return "#2563EB"
    elif "npc" in org_type:
        return "#F59E0B"
    elif "ccppcc" in org_type:
        return "#8B5CF6"
    return "#6B7280"

def node_size(pid):
    for p in persons:
        if p["id"] == pid:
            post = p["current_post"]
            if "州委书记" in post or "州长" in post:
                return 20.0
            elif "书记" in post or "县长" in post or "市长" in post:
                return 14.0
            elif "主任" in post or "主席" in post:
                return 12.0
            else:
                return 10.0
    return 10.0

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append('  <meta>')
lines.append('    <creator>gov-relation investigator</creator>')
lines.append('    <description>湘西土家族苗族自治州领导班子工作关系网络</description>')
lines.append('    <date>2026-07-14</date>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# --- Attributes ---
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="role" title="Role" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# --- Nodes: Persons ---
lines.append('    <nodes>')
for p in persons:
    c = role_color(p["id"])
    sz = node_size(p["id"])
    lines.append(f'      <node id="{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="role" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(c[1:3],16)}" g="{int(c[3:5],16)}" b="{int(c[5:7],16)}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'        <viz:shape value="disc"/>')
    lines.append(f'      </node>')

# --- Nodes: Organizations ---
for o in organizations:
    c = org_color(o["type"])
    lines.append(f'      <node id="{o["id"]}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="role" value="{o["type"]}"/>')
    lines.append(f'          <attvalue for="current_post" value=""/>')
    lines.append(f'          <attvalue for="source" value=""/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(c[1:3],16)}" g="{int(c[3:5],16)}" b="{int(c[5:7],16)}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'        <viz:shape value="square"/>')
    lines.append(f'      </node>')

lines.append('    </nodes>')

# --- Edges ---
lines.append('    <edges>')
edge_id = 0

# Person -> Organization (worked_at)
for pos in positions:
    edge_id += 1
    lines.append(f'      <edge id="e{edge_id}" source="{pos["person_id"]}" target="{pos["org_id"]}" type="directed">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{pos["title"]} ({pos["start"]}~{pos["end"] or "今"})"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"]}~{pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="180" g="180" b="180"/>')
    lines.append(f'        <viz:thickness value="1.0"/>')
    lines.append(f'      </edge>')

# Person <-> Person (relationship)
for r in relationships:
    edge_id += 1
    lines.append(f'      <edge id="e{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
    lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    if r["type"] in ("colleague",):
        lines.append(f'        <viz:color r="201" g="169" b="78"/>')
        lines.append(f'        <viz:thickness value="2.5"/>')
    else:
        lines.append(f'        <viz:color r="100" g="150" b="255"/>')
        lines.append(f'        <viz:thickness value="1.5"/>')
    lines.append(f'      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF graph created: {GEXF_PATH}")

# ──────────────────────────────────────────────
# STATS
# ──────────────────────────────────────────────
print()
print("📊 Summary Statistics:")
print(f"   Persons: {len(persons)}")
print(f"   Organizations: {len(organizations)}")
print(f"   Positions (appointments): {len(positions)}")
print(f"   Relationships (person↔person): {len(relationships)}")
print(f"   Edges total: {len(positions) + len(relationships)}")
print()
print("   Persons by role:")
for p in persons:
    print(f"     - {p['name']}: {p['current_post']} ({p['birth']})")
