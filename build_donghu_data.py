#!/usr/bin/env python3
"""
南昌市东湖区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Donghu District leadership.
"""

import sqlite3
import os

# ── DATA ──
# Person ID convention: donghu_{surname_givenname}

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source
    # Top leaders
    ("donghu_liu_guangrong", "刘光荣", "男", "汉族", "1972年11月", "江西南昌县", "大学/哲学学士", "1995年4月", "1995年12月", "区委书记", "中共南昌市东湖区委员会", "dhq.nc.gov.cn/official"),
    ("donghu_deng_zhiwu", "邓之武", "男", "汉族", "1976年2月", "江西万年", "管理学硕士", "1995年12月", "1998年8月", "区委副书记、代区长", "南昌市东湖区人民政府", "dhq.nc.gov.cn/official"),
    # Standing committee — UPDATED with detailed findings
    ("donghu_wei_jixin", "魏维新", "男", "汉族", "1978年4月", "江西南昌", "省委党校研究生/法学学士", "2000年5月", "2000年7月", "区委常委、组织部部长", "中共南昌市东湖区委组织部", "baike.baidu.com"),
    ("donghu_shao_yinglan", "邵应兰", "女", "汉族", "1978年4月", "江西抚州", "大学/公共管理硕士", "2005年4月", "2003年10月", "区委常委、区纪委书记、区监委主任", "中共南昌市东湖区纪律检查委员会", "baike.baidu.com"),
    ("donghu_xiong_guangyi", "熊广义", "男", "汉族", "1982年1月", "江西南昌", "大学/文学学士", "不详", "不详", "区委常委、常务副区长", "南昌市东湖区人民政府", "dhq.nc.gov.cn/official"),
    ("donghu_jiang_rensheng", "江人生", "男", "汉族", "1975年9月", "江西鄱阳", "本科", "不详", "不详", "区委常委、人武部部长", "南昌市东湖区人民武装部", "dhq.nc.gov.cn/official"),
    ("donghu_tu_hongwei", "涂宏伟", "男", "汉族", "1980年5月", "江西南昌", "本科", "中共党员", "不详", "区委常委、宣传部部长", "中共南昌市东湖区委宣传部", "dhq.nc.gov.cn/official"),
    ("donghu_xiong_guohai", "熊国海", "男", "汉族", "1977年11月", "江西南昌", "大学/工学学士", "中共党员", "1999年9月", "区委常委、政法委书记", "中共南昌市东湖区委政法委员会", "dhq.nc.gov.cn+police"),
    # Vice mayors — UPDATED
    ("donghu_rao_xueyu", "饶雪宇", "女", "汉族", "1970年4月", "江西南昌", "研究生", "九三学社", "不详", "副区长", "南昌市东湖区人民政府", "dhq.nc.gov.cn/official"),
    ("donghu_xu_qiang", "许强", "男", "汉族", "1979年12月", "江西南昌", "本科", "中共党员", "不详", "副区长", "南昌市东湖区人民政府", "dhq.nc.gov.cn/official"),
    ("donghu_yao_le", "姚乐", "男", "汉族", "1983年6月", "江西南昌", "大学", "中共党员", "2006年7月", "副区长", "南昌市东湖区人民政府", "dhq.nc.gov.cn/official"),
    ("donghu_jiang_shan", "江珊", "女", "汉族", "1983年11月", "江西黎川", "大学", "中共党员", "不详", "副区长", "南昌市东湖区人民政府", "dhq.nc.gov.cn/official"),
    ("donghu_xiong_hua", "熊华", "男", "汉族", "1973年1月", "江西南昌", "法学学士", "中共党员", "不详", "副区长、东湖公安分局局长", "南昌市公安局东湖分局", "dhq.nc.gov.cn/official"),
    # Predecessors
    ("donghu_hu_junfeng", "胡俊峰", "男", "汉族", "1977年12月", "江西南昌", "省委党校研究生/工程硕士", "1998年12月", "2000年8月", "前区长（去向待查）", "东湖区（已离任）", "dhq.nc.gov.cn/official"),
    ("donghu_deng_yunsheng", "邓云生", "男", "未知", "未知", "未知", "未知", "未知", "未知", "前专职副书记（去向待查）", "东湖区（已离任）", "news/2021.09"),
    # Key connections from existing research
    ("jinxian_xu_jiang", "徐强", "男", "汉族", "1974年11月", "江西南昌县", "未知", "未知", "未知", "新建区委书记（前进贤县委书记）", "中共南昌市新建区委员会", "existing_project"),
    ("nanchang_jia_yuchao", "贾彧超", "男", "汉族", "1976年9月", "湖北襄阳", "未知", "未知", "未知", "南昌县委书记", "中共南昌县委员会", "existing_project"),
    # Early career connections for 邓之武
    ("donghu_deng_early_orgs", "省蚕桑茶叶研究所/市外经贸委/市投促局", "未知", "未知", "未知", "未知", "未知", "未知", "未知", "邓之武1998-2019年任职单位", "多个单位", "baike"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("donghu_party_committee", "中共南昌市东湖区委员会", "党委", "县级", "中共南昌市委", "南昌市东湖区"),
    ("donghu_gov", "南昌市东湖区人民政府", "政府", "县级", "南昌市人民政府", "南昌市东湖区"),
    ("donghu_org_department", "中共南昌市东湖区委组织部", "党委部门", "正科级", "东湖区委", "南昌市东湖区"),
    ("donghu_discipline", "中共南昌市东湖区纪律检查委员会", "纪委", "县级", "南昌市纪委", "南昌市东湖区"),
    ("donghu_propaganda", "中共南昌市东湖区委宣传部", "党委部门", "正科级", "东湖区委", "南昌市东湖区"),
    ("donghu_political_legal", "中共南昌市东湖区委政法委员会", "党委部门", "正科级", "东湖区委", "南昌市东湖区"),
    ("donghu_armed_forces", "南昌市东湖区人民武装部", "军队", "县级", "南昌警备区", "南昌市东湖区"),
    ("donghu_public_security", "南昌市公安局东湖分局", "公安", "正科级", "南昌市公安局", "南昌市东湖区"),
    ("donghu_peoples_congress", "南昌市东湖区人民代表大会常务委员会", "人大", "县级", "南昌市人大常委会", "南昌市东湖区"),
    ("donghu_cppcc", "中国人民政治协商会议南昌市东湖区委员会", "政协", "县级", "南昌市政协", "南昌市东湖区"),
    # Related orgs from cross-district
    ("nanchang_county_committee", "中共南昌县委员会", "党委", "县级", "中共南昌市委", "南昌县"),
    ("jinxian_county_gov", "进贤县人民政府", "政府", "县级", "南昌市人民政府", "进贤县"),
    ("jinxian_county_committee", "中共进贤县委员会", "党委", "县级", "中共南昌市委", "进贤县"),
    ("nanchang_investment", "南昌市投资促进局", "政府机构", "正县级", "南昌市人民政府", "南昌市"),
    ("nanchang_foreign_trade", "南昌市外经贸委", "政府机构", "正县级", "南昌市人民政府", "南昌市"),
    ("honggutan_gov", "红谷滩区人民政府", "政府", "县级", "南昌市人民政府", "南昌市红谷滩区"),
    ("sedriculture_research", "江西省蚕桑茶叶研究所", "事业单位", "正处级", "江西省农业厅", "南昌县"),
    ("nanchang_university", "浙江农业大学（现浙江大学）", "学校", "大学", "教育部", "浙江杭州"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note
    # 刘光荣
    ("donghu_liu_guangrong", "donghu_party_committee", "区委书记", "2025-02", "至今", "正县级", "主持区委全面工作"),
    ("donghu_liu_guangrong", "honggutan_gov", "红谷滩区长", "~2021", "2025-02", "正县级", "前职"),
    ("donghu_liu_guangrong", "nanchang_county_committee", "南昌县任职（21年）", "1995", "~2021", "未知", "具体职务序列完全空缺"),
    # 邓之武
    ("donghu_deng_zhiwu", "donghu_party_committee", "区委副书记", "2026-07", "至今", "正县级", "兼任代区长"),
    ("donghu_deng_zhiwu", "donghu_gov", "代区长", "2026-07-07", "至今", "正县级", "负责区政府全面工作"),
    ("donghu_deng_zhiwu", "nanchang_county_committee", "县委副书记", "2025-01", "2026-07", "正县级", "前职"),
    ("donghu_deng_zhiwu", "jinxian_county_gov", "常务副县长", "2023-02", "2025-01", "副县级", "进贤县委常委/县政府党组副书记"),
    ("donghu_deng_zhiwu", "jinxian_county_committee", "县委常委/组织部部长", "2019-06", "2023-02", "副县级", "组织部长"),
    ("donghu_deng_zhiwu", "nanchang_investment", "副局长", "2015-09", "2019-06", "副县级", "南昌市投资促进局副局长"),
    ("donghu_deng_zhiwu", "nanchang_foreign_trade", "处长", "~2010", "2015-09", "正科→副处", "投资促进处处长"),
    ("donghu_deng_zhiwu", "nanchang_foreign_trade", "区域合作处副处长", "2002-05", "~2010", "副科→正科", "外经贸委"),
    ("donghu_deng_zhiwu", "sedriculture_research", "工作（推测）", "1998-08", "2002-05", "未知", "约3年9个月空白"),
    ("donghu_deng_zhiwu", "nanchang_university", "茶学系学生", "1994-09", "1998-07", "本科", "浙江农业大学茶学系"),
    # 熊广义
    ("donghu_xiong_guangyi", "donghu_gov", "常务副区长", "2023", "至今", "副县级", "区委常委/党组副书记"),
    ("donghu_xiong_guangyi", "donghu_propaganda", "宣传部部长（区委常委）", "2021-09", "2023", "副县级", "曾任"),
    ("donghu_xiong_guangyi", "donghu_propaganda", "宣传部（副部长等）", "~2015", "2021-09", "未知", "具体职务待查"),
    ("donghu_xiong_guangyi", "donghu_propaganda", "东湖区文明办", "~2018", "2021", "未知", "兼任"),
    # ═══ 魏维新 — 完整履历 ═══
    ("donghu_wei_jixin", "donghu_org_department", "组织部部长（区委常委）", "2021-09", "至今", "副县级", "现任"),
    ("donghu_wei_jixin", "jinxian_county_committee", "县委常委、组织部部长", "2016-07", "2021-08", "副县级", "兼县非公经济组织和社会组织工委书记"),
    ("donghu_wei_jixin", "donghu_party_committee", "市委组织部干部综合处处长", "2012-02", "2016-07", "正科", "南昌市委组织部13年"),
    ("donghu_wei_jixin", "donghu_party_committee", "市委组织部干部二处副处长", "2008-12", "2012-02", "副科/正科", "南昌市委组织部"),
    ("donghu_wei_jixin", "donghu_party_committee", "市委组织部干部综合处副主任科员", "2005-12", "2008-12", "副科", "南昌市委组织部"),
    ("donghu_wei_jixin", "donghu_party_committee", "市委组织部干部综合处科员", "2003-02", "2005-12", "科员", "南昌市委组织部"),
    ("donghu_wei_jixin", "donghu_party_committee", "南昌县蒋巷镇政府科员（市选拔生）", "2000-07", "2003-02", "科员", "基层选拔培养"),
    # ═══ 邵应兰 — 完整履历 ═══
    ("donghu_shao_yinglan", "donghu_discipline", "区纪委书记/监委主任", "2021-09", "至今", "副县级", "现任"),
    ("donghu_shao_yinglan", "donghu_party_committee", "区委常委", "2021-09", "至今", "副县级", "当选第十三届区委常委"),
    ("donghu_shao_yinglan", "donghu_org_department", "县委常委、宣传部部长", "2019-06", "2021-08", "副县级", "安义县（首次下派地方）"),
    ("donghu_shao_yinglan", "donghu_discipline", "南昌市纪委党风政风监督室副主任", "2014-07", "2019-06", "正科", "市级纪委16年"),
    ("donghu_shao_yinglan", "donghu_discipline", "南昌市纪委调研宣传室副主任", "2013-05", "2014-07", "副科→正科", "市级纪委"),
    ("donghu_shao_yinglan", "donghu_discipline", "南昌市纪委科员→副科→正科级纪检员", "2003-10", "2013-05", "科员→正科", "市级纪委"),
    # ═══ 熊国海 — 完整履历 ═══
    ("donghu_xiong_guohai", "donghu_political_legal", "政法委书记（区委常委）", "2025-02", "至今", "副县级", "首任从公安系统转入的政法委书记"),
    ("donghu_xiong_guohai", "donghu_public_security", "南昌市公安局反恐支队支队长", "2023-01", "2025-02", "正科/副县", "公安系统"),
    ("donghu_xiong_guohai", "donghu_public_security", "南昌市公安局刑侦支队副支队长", "~2016", "2023-01", "正科", "全国刑侦专家/二级英模"),
    ("donghu_xiong_guohai", "donghu_public_security", "南昌市公安局刑侦支队民警/中队长/大队长", "1999-09", "~2016", "民警→科级", "从警17年逐步晋升"),
    # ═══ 涂宏伟 — 部分还原 ═══
    ("donghu_tu_hongwei", "donghu_propaganda", "宣传部部长（区委常委）", "~2023", "至今", "副县级", "接替熊广义"),
    ("donghu_tu_hongwei", "donghu_gov", "副区长", "2021-01", "~2023", "副县级", "分管城管/城建/卫健"),
    ("donghu_tu_hongwei", "donghu_gov", "2021年前东湖区任职", "~2000", "~2021-01", "未知", "2021年前具体职务空白"),
    # ═══ 江人生 ═══
    ("donghu_jiang_rensheng", "donghu_armed_forces", "人武部部长（区委常委）", "2022-07", "至今", "副县级", "现任"),
    # ═══ 熊华 ═══
    ("donghu_xiong_hua", "donghu_public_security", "东湖公安分局局长", "2025-07", "至今", "正科/副县", "兼副区长"),
    ("donghu_xiong_hua", "donghu_gov", "副区长（兼）", "2025-07", "至今", "副县级", "兼公安分局长"),
    # ═══ 胡俊峰 ═══
    ("donghu_hu_junfeng", "donghu_gov", "区长", "2021-03", "2026-07", "正县级", "前任区长"),
    ("donghu_hu_junfeng", "donghu_party_committee", "区委副书记（兼）", "2021-03", "2026-07", "正县级", "兼任"),
    ("donghu_hu_junfeng", "donghu_gov", "代区长", "2021-03-08", "2021-03-12", "正县级", "过渡期"),
    # 胡俊峰 - 2019年前完全未知
    # ═══ 邓云生 ═══
    ("donghu_deng_yunsheng", "donghu_party_committee", "专职副书记", "2021-09", "~2023", "副县级", "最后出现在2023年新闻"),
    # ═══ 饶雪宇 ═══
    ("donghu_rao_xueyu", "donghu_gov", "副区长", "~2021", "至今", "副县级", "九三学社，无党派"),
    # ═══ 许强 — 部分还原 ═══
    ("donghu_xu_qiang", "donghu_gov", "副区长", "~2021", "至今", "副县级", "分管住建/城建/交通"),
    ("donghu_xu_qiang", "donghu_org_department", "豫章街道党工委书记", "~2019", "~2021", "正科", "东湖区"),
    ("donghu_xu_qiang", "donghu_org_department", "扬农管理处党工委书记", "~2014", "~2019", "正科", "东湖区（青山湖→东湖跨区）"),
    ("donghu_xu_qiang", "donghu_org_department", "青山湖区任职", "~2000", "~2014", "科员→科级", "青山湖区教体局/政协办/塘山镇"),
    # ═══ 姚乐 ═══
    ("donghu_yao_le", "donghu_gov", "副区长", "~2021", "至今", "副县级", "中共党员"),
    # 姚乐 2006-2021年15年完全空白
    # ═══ 江珊 ═══
    ("donghu_jiang_shan", "donghu_gov", "副区长", "2023-10", "至今", "副县级", "黎川籍/西湖区街道出身"),
    ("donghu_jiang_shan", "donghu_org_department", "西湖区南浦街道党工委书记", "~2021", "2023-10", "正科", "西湖区系马桩街办→南浦街道"),
    ("donghu_jiang_shan", "donghu_org_department", "西湖区系马桩街办主任/副书记", "~2018", "~2021", "副科→正科", "南昌市西湖区"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period
    # Strong relationships (confirmed co-workers)
    ("donghu_deng_zhiwu", "donghu_liu_guangrong", "强关系", "现任党政搭档", "东湖区", "2026-07至今"),
    ("donghu_deng_zhiwu", "jinxian_xu_jiang", "强关系", "进贤县同班子约3年", "进贤县", "2021-2024"),
    ("donghu_hu_junfeng", "donghu_liu_guangrong", "强关系", "党政搭档约1.5年", "东湖区", "2025-02至2026-07"),
    ("donghu_xiong_guangyi", "donghu_tu_hongwei", "强关系", "前后任宣传部部长", "东湖区委宣传部", "2021-2023"),
    ("donghu_deng_zhiwu", "donghu_hu_junfeng", "强关系", "职务接替（前后任区长）", "东湖区", "2026-07"),
    ("donghu_deng_zhiwu", "nanchang_jia_yuchao", "强关系", "南昌县直接上下级", "南昌县", "2025-01至2026-07"),
    # Weak relationships (indirect connections)
    ("donghu_deng_zhiwu", "donghu_xiong_guangyi", "弱关系", "现任班子共事", "东湖区", "2026-07至今"),
    ("donghu_deng_zhiwu", "donghu_wei_jixin", "弱关系", "现任班子共事", "东湖区", "2026-07至今"),
    ("donghu_deng_zhiwu", "donghu_shao_yinglan", "弱关系", "现任班子共事", "东湖区", "2026-07至今"),
    ("donghu_deng_zhiwu", "donghu_jiang_rensheng", "弱关系", "现任班子共事", "东湖区", "2026-07至今"),
    ("donghu_deng_zhiwu", "donghu_xiong_guohai", "弱关系", "现任班子共事", "东湖区", "2026-07至今"),
    # 邵应兰-江珊 connection
    ("donghu_shao_yinglan", "donghu_jiang_shan", "弱关系", "同籍贯（抚州）共事于东湖区班子", "东湖区", "2023-10至今"),
    # Cross-district connections
    ("donghu_liu_guangrong", "nanchang_jia_yuchao", "弱关系", "南昌县系前后辈", "南昌县", "1995-2021"),
    ("jinxian_xu_jiang", "donghu_hu_junfeng", "弱关系", "南昌市县级干部网络", "南昌市", "2021-2026"),
    # NEW — discovered connections
    ("donghu_wei_jixin", "donghu_deng_zhiwu", "强关系", "进贤县同班子约5年", "进贤县", "2016-2021"),
    ("donghu_wei_jixin", "nanchang_jia_yuchao", "弱关系", "市委组织部→南昌县系", "南昌市委组织部", "2003-2016"),
    ("donghu_xiong_guohai", "donghu_xiong_hua", "弱关系", "公安系统前后辈", "南昌公安系统", "1999-2025"),
]

# ── BUILD DATABASE ──

DB_PATH = "data/database/donghu_network.db"
GEXF_PATH = "data/graph/donghu_network.gexf"


def create_db():
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
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)

    # Insert organizations
    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)

    # Insert positions
    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)

    # Insert relationships
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


def generate_gexf():
    """Generate GEXF 1.3 with viz namespace using string formatting."""
    
    # Color scheme
    node_colors = {
        # Roles -> (r,g,b) for party, gov, discipline, other
        "party": (212, 52, 46),      # red
        "gov_leader": (51, 102, 204),  # blue
        "gov_deputy": (80, 130, 200),  # lighter blue
        "discipline": (204, 119, 34),  # orange
        "other": (102, 102, 102),      # grey
        "org_party": (85, 51, 51),     # dark red
        "org_gov": (51, 68, 85),       # dark blue
        "org_other": (68, 68, 68),     # dark grey
    }

    def color_for_person(pid):
        """Determine node color based on person's role."""
        for p in PERSONS:
            if p[0] == pid:
                post = p[9] or ""
                if "书记" in post and "区委" in post:
                    return "party", 20.0
                elif "代区长" in post or "区长" in post:
                    return "gov_leader", 20.0
                elif "常务副区长" in post:
                    return "gov_leader", 16.0
                elif "副区长" in post or "副县长" in post:
                    return "gov_deputy", 14.0
                elif "纪委书记" in post:
                    return "discipline", 14.0
                else:
                    return "other", 12.0
        return "other", 12.0

    def color_for_org(oid):
        for o in ORGANIZATIONS:
            if o[0] == oid:
                tp = o[2]
                if "党委" in tp:
                    return "org_party", 8.0
                elif "政府" in tp or "公安" in tp:
                    return "org_gov", 8.0
                else:
                    return "org_other", 8.0
        return "org_other", 8.0

    # Build XML parts
    nodes_xml = []
    edges_xml = []

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        label = p[1]
        g, sz = color_for_person(pid)
        r, gb, b = node_colors[g]
        title = f"{p[1]}\\n{p[9]}\\n{p[3]}·{p[4] if p[4] else '未知'}\\n籍贯: {p[5] if p[5] else '未知'}"
        nodes_xml.append(f"""\
    <node id="{pid}" label="{label}">
      <attvalues>
        <attvalue for="type" value="person"/>
        <attvalue for="role" value="{p[9]}"/>
      </attvalues>
      <viz:color r="{r}" g="{gb}" b="{b}" a="1.0"/>
      <viz:size value="{sz}"/>
      <viz:position x="0" y="0" z="0"/>
    </node>""")

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        label = o[1]
        g, sz = color_for_org(oid)
        r, gb, b = node_colors[g]
        nodes_xml.append(f"""\
    <node id="{oid}" label="{label}">
      <attvalues>
        <attvalue for="type" value="org"/>
        <attvalue for="org_type" value="{o[2]}"/>
      </attvalues>
      <viz:color r="{r}" g="{gb}" b="{b}" a="1.0"/>
      <viz:size value="{sz}"/>
      <viz:shape value="square"/>
      <viz:position x="0" y="0" z="0"/>
    </node>""")

    # work_at edges (person -> org)
    edge_id = 0
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        label = f"{title} ({start}-{end or '至今'})"
        edge_id += 1
        edges_xml.append(f"""\
    <edge id="e{edge_id}" source="{pid}" target="{oid}" type="directed" label="{title}">
      <attvalues>
        <attvalue for="type" value="worked_at"/>
        <attvalue for="start" value="{start or ''}"/>
        <attvalue for="end" value="{end or ''}"/>
        <attvalue for="rank" value="{rank or ''}"/>
      </attvalues>
      <viz:color r="80" g="80" b="80" a="0.5"/>
      <viz:thickness value="1.0"/>
    </edge>""")

    # relationship edges (person <-> person)
    for r in RELATIONSHIPS:
        a, b, typ, context, overlap_org, overlap_period = r
        edge_id += 1
        is_strong = typ == "强关系"
        cr, cg, cb = (184, 149, 62) if is_strong else (91, 139, 192)
        thickness = 2.5 if is_strong else 1.5
        edges_xml.append(f"""\
    <edge id="e{edge_id}" source="{a}" target="{b}" type="undirected" label="{context}">
      <attvalues>
        <attvalue for="type" value="relationship"/>
        <attvalue for="strength" value="{typ}"/>
        <attvalue for="context" value="{context}"/>
        <attvalue for="overlap_org" value="{overlap_org}"/>
        <attvalue for="overlap_period" value="{overlap_period}"/>
      </attvalues>
      <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>
      <viz:thickness value="{thickness}"/>
    </edge>""")

    nodes_block = "\n".join(nodes_xml)
    edges_block = "\n".join(edges_xml)

    gexf = f"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://gexf.net/1.3"
      xmlns:viz="http://gexf.net/1.3/viz"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://gexf.net/1.3 http://gexf.net/1.3/gexf.xsd"
      version="1.3">
  <meta>
    <creator>China-Gov-Network Investigation</creator>
    <description>南昌市东湖区领导班子工作关系网络 — 2026年7月</description>
    <date>2026-07-14</date>
  </meta>
  <graph mode="static" defaultedgetype="undirected">
    <attributes class="node">
      <attribute id="type" title="Node Type" type="string"/>
      <attribute id="role" title="Role" type="string"/>
      <attribute id="org_type" title="Org Type" type="string"/>
    </attributes>
    <attributes class="edge">
      <attribute id="type" title="Edge Type" type="string"/>
      <attribute id="start" title="Start Date" type="string"/>
      <attribute id="end" title="End Date" type="string"/>
      <attribute id="rank" title="Rank" type="string"/>
      <attribute id="strength" title="Strength" type="string"/>
      <attribute id="context" title="Context" type="string"/>
      <attribute id="overlap_org" title="Overlap Org" type="string"/>
      <attribute id="overlap_period" title="Overlap Period" type="string"/>
    </attributes>
    <nodes>
{nodes_block}
    </nodes>
    <edges>
{edges_block}
    </edges>
  </graph>
</gexf>"""

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write(gexf)
    print(f"✅ GEXF graph created: {GEXF_PATH}")


def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
    conn.close()


if __name__ == "__main__":
    print("Building 南昌市东湖区 network data...")
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()
    print("Done.")
