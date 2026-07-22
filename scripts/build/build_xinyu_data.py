"""
Build SQLite database + GEXF graph for 新余市 (Xinyu City) leadership network.
"""
import os
import sqlite3

# ── Paths ──────────────────────────────────────────────────────────────────────
DB_PATH = "data/database/xinyu_network.db"
GEXF_PATH = "data/graph/xinyu_network.gexf"

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# ── Hardcoded Research Data ────────────────────────────────────────────────────

persons = [
    # ── Current leadership ──────────────────────────────────────────────
    dict(id="xinyu_fang_xiangjun", name="方向军", gender="男", ethnicity="汉族",
         birth="1970-10", birthplace="浙江省淳安县", education="大学学历、工商管理硕士（MBA）/管理学硕士",
         party_join="", work_start="1996-07", current_post="市委书记",
         current_org="中共新余市委",
         source="sogou.com搜索快照; zh.wikipedia.org/wiki/新余市"),
    dict(id="xinyu_liao_liangsheng", name="廖良生", gender="男", ethnicity="汉族",
         birth="1975-09", birthplace="江西石城", education="在职大学学历，工商管理硕士",
         party_join="1997-08", work_start="1993-07", current_post="常务副市长",
         current_org="新余市人民政府", source="xinyu.gov.cn; baike.baidu.com"),
    dict(id="xinyu_chen_wenhua", name="陈文华", gender="女", ethnicity="汉族",
         birth="1968-03", birthplace="未知", education="在职研究生学历，法学博士",
         party_join="民盟盟员", work_start="", current_post="副市长",
         current_org="新余市人民政府", source="xinyu.gov.cn"),
    dict(id="xinyu_shu_yongzhong", name="舒永忠", gender="男", ethnicity="汉族",
         birth="1969-02", birthplace="未知", education="大学学历，经济学学士",
         party_join="中共党员", work_start="", current_post="副市长",
         current_org="新余市人民政府", source="xinyu.gov.cn"),
    dict(id="xinyu_he_lihua", name="贺利华", gender="男", ethnicity="汉族",
         birth="1967-06", birthplace="未知", education="在职大学学历，工商管理硕士",
         party_join="中共党员", work_start="", current_post="副市长",
         current_org="新余市人民政府", source="xinyu.gov.cn"),
    dict(id="xinyu_xiao_qiugen", name="肖秋根", gender="男", ethnicity="汉族",
         birth="1968-10", birthplace="未知", education="在职大学学历",
         party_join="中共党员", work_start="", current_post="副市长",
         current_org="新余市人民政府", source="xinyu.gov.cn"),
    dict(id="xinyu_li_zhidan", name="李之旦", gender="男", ethnicity="汉族",
         birth="1975-08", birthplace="未知", education="大学学历，法学学士",
         party_join="中共党员", work_start="", current_post="副市长、市公安局局长",
         current_org="新余市人民政府", source="xinyu.gov.cn"),
    dict(id="xinyu_fu_qiang", name="傅强", gender="男", ethnicity="汉族",
         birth="未知", birthplace="未知", education="未知",
         party_join="中共党员", work_start="", current_post="市政府秘书长",
         current_org="新余市人民政府", source="xinyu.gov.cn"),
    # ── Predecessors ────────────────────────────────────────────────────────
    dict(id="xinyu_xu_hong", name="徐鸿", gender="男", ethnicity="汉族",
         birth="1968-08", birthplace="江西上饶", education="博士研究生",
         party_join="中共党员", work_start="", current_post="（被撤职）",
         current_org="", source="zh.wikipedia.org/wiki/新余市"),
    dict(id="xinyu_zheng_guangquan", name="郑光泉", gender="男", ethnicity="汉族",
         birth="1967-08", birthplace="江西上饶", education="省委党校研究生",
         party_join="中共党员", work_start="", current_post="（原市委书记，已离任）",
         current_org="", source="zh.wikipedia.org/wiki/郑光泉"),
    # ── Key historical leaders ──────────────────────────────────────────────
    dict(id="xinyu_zhang_zhiping", name="张智萍", gender="女", ethnicity="汉族",
         birth="1967-11", birthplace="湖南邵阳", education="未知",
         party_join="中共党员", work_start="", current_post="市人大常委会主任",
         current_org="新余市人大常委会", source="zh.wikipedia.org/wiki/张智萍"),
    dict(id="xinyu_you_ying", name="犹㼆", gender="男", ethnicity="土家族",
         birth="1973-11", birthplace="贵州余庆", education="中央党校研究生",
         party_join="中共党员", work_start="", current_post="江西省商务厅厅长",
         current_org="江西省商务厅", source="zh.wikipedia.org/wiki/犹㼆"),
    dict(id="xinyu_dong_xiaojian", name="董晓健", gender="男", ethnicity="汉族",
         birth="1962-10", birthplace="江西浮梁", education="研究生学历",
         party_join="中共党员", work_start="", current_post="（原市长）",
         current_org="", source="zh.wikipedia.org/wiki/董晓健"),
    dict(id="xinyu_liu_jie", name="刘捷", gender="男", ethnicity="汉族",
         birth="1970-01", birthplace="江苏丹阳", education="工学博士",
         party_join="中共党员", work_start="1992-08", current_post="浙江省委副书记",
         current_org="中共浙江省委", source="zh.wikipedia.org/wiki/刘捷"),
    # ── Cross-city connections ────────────────────────────────────────────
    dict(id="xinyu_wu_fukang", name="伍复康", gender="男", ethnicity="汉族",
         birth="未知", birthplace="未知", education="未知",
         party_join="中共党员", work_start="", current_post="新余学院党委书记",
         current_org="新余学院", source="现有项目数据(南昌县报告)"),
]

organizations = [
    dict(id="org_xinyu_city", name="新余市", type="行政区域", level="地级市", parent="江西省", location="江西省"),
    dict(id="org_xinyu_cpc", name="中共新余市委", type="党委", level="地级市", parent="中共江西省委", location="新余市"),
    dict(id="org_xinyu_gov", name="新余市人民政府", type="政府", level="地级市", parent="新余市", location="新余市"),
    dict(id="org_xinyu_npc", name="新余市人大常委会", type="人大", level="地级市", parent="新余市", location="新余市"),
    dict(id="org_xinyu_cppcc", name="新余市政协", type="政协", level="地级市", parent="新余市", location="新余市"),
    dict(id="org_xinyu_police", name="新余市公安局", type="政府", level="地级市部门", parent="新余市人民政府", location="新余市"),
    dict(id="org_xinyu_college", name="新余学院", type="事业单位", level="地级市", parent="新余市", location="新余市"),
    dict(id="org_jiangxi_stats", name="江西省统计局", type="政府", level="省级", parent="江西省人民政府", location="南昌市"),
    dict(id="org_jiangxi_env", name="江西省生态环境厅", type="政府", level="省级", parent="江西省人民政府", location="南昌市"),
    dict(id="org_jiangxi_commerce", name="江西省商务厅", type="政府", level="省级", parent="江西省人民政府", location="南昌市"),
    dict(id="org_jiangxi_tech", name="江西省科技厅", type="政府", level="省级", parent="江西省人民政府", location="南昌市"),
    dict(id="org_jiangxi_cpc", name="中共江西省委", type="党委", level="省级", parent="中共中央", location="南昌市"),
    dict(id="org_jiangxi_province", name="江西省人民政府", type="政府", level="省级", parent="江西省", location="南昌市"),
    dict(id="org_zhejiang_cpc", name="中共浙江省委", type="党委", level="省级", parent="中共中央", location="杭州市"),
    dict(id="org_unknown", name="（待查）", type="其他", level="未知", parent="", location="未知"),
]

positions = [
    # ── 方向军 (Fang Xiangjun) ── 完整履历（2026-07-14深挖新增早期职务）───────
    # 以下为新增的早期职务（经搜狗快照数据确认职务序列，具体起止月份待精确化）
    dict(person_id="xinyu_fang_xiangjun", org_id="org_unknown", title="上饶市信州区科技副区长（挂职）", start="~2000s?", end="~2000s?", rank="副处级?",
         note="早期挂职经历，具体起止年月待查"),
    dict(person_id="xinyu_fang_xiangjun", org_id="org_jiangxi_commerce", title="江西省对外贸易经济合作厅外经贸发展处副处长",
         start="~2000s?", end="~2009?", rank="副处级", note="商务厅前身，2009年机构合并前"),
    dict(person_id="xinyu_fang_xiangjun", org_id="org_jiangxi_commerce", title="江西省商务厅对外贸易处副处长",
         start="~2009?", end="~2010s?", rank="副处级", note="机构合并后"),
    dict(person_id="xinyu_fang_xiangjun", org_id="org_jiangxi_commerce", title="江西省商务厅直属机关党委专职副书记兼直属机关纪委书记",
         start="~2010s?", end="~2010s?", rank="正处级?", note="党内职务"),
    dict(person_id="xinyu_fang_xiangjun", org_id="org_jiangxi_commerce", title="江西省商务厅对外经济合作处处长",
         start="~2010s?", end="~2010s?", rank="正处级", note=""),
    dict(person_id="xinyu_fang_xiangjun", org_id="org_jiangxi_commerce", title="江西省商务厅对外投资和经济合作处处长",
         start="~2010s?", end="~2010s?", rank="正处级", note=""),
    dict(person_id="xinyu_fang_xiangjun", org_id="org_jiangxi_commerce", title="江西省商务厅办公室(宣传处)主任(处长)",
         start="~2010s?", end="~2020?", rank="正处级", note=""),
    dict(person_id="xinyu_fang_xiangjun", org_id="org_jiangxi_commerce", title="江西省商务厅副厅长",
         start="~2020?", end="~2021?", rank="副厅级", note=""),
    dict(person_id="xinyu_fang_xiangjun", org_id="org_jiangxi_cpc", title="江西省委副秘书长",
         start="~2021?", end="~2023?", rank="副厅级", note="搜狗快照显示"2021..."暗示2021年上任"),
    dict(person_id="xinyu_fang_xiangjun", org_id="org_jiangxi_stats", title="江西省统计局党组书记、局长", start="~2023", end="2024-08", rank="正厅级", note=""),
    dict(person_id="xinyu_fang_xiangjun", org_id="org_xinyu_gov", title="新余市委副书记、市长", start="2024-08", end="2026-04", rank="正厅级", note="2024年9月29日正式当选"),
    dict(person_id="xinyu_fang_xiangjun", org_id="org_xinyu_cpc", title="新余市委书记、新余军分区党委第一书记", start="2026-04", end="", rank="正厅级", note="现任"),

    # ── 廖良生 (Liao Liangsheng) ───────────────────────────────────────
    dict(person_id="xinyu_liao_liangsheng", org_id="org_xinyu_cpc", title="新余市委常委", start="~2025", end="", rank="副厅级", note="现任"),
    dict(person_id="xinyu_liao_liangsheng", org_id="org_xinyu_gov", title="新余市常务副市长、党组副书记", start="~2025", end="", rank="副厅级", note="现任"),

    # ── 陈文华 ───────────────────────────────────────────────────────────
    dict(person_id="xinyu_chen_wenhua", org_id="org_xinyu_gov", title="新余市副市长", start="~2021", end="", rank="副厅级", note="现任；民盟盟员"),

    # ── 舒永忠 ───────────────────────────────────────────────────────────
    dict(person_id="xinyu_shu_yongzhong", org_id="org_xinyu_gov", title="新余市副市长", start="~2021", end="", rank="副厅级", note="现任；兼高新区党工委书记"),

    # ── 贺利华 ───────────────────────────────────────────────────────────
    dict(person_id="xinyu_he_lihua", org_id="org_xinyu_gov", title="新余市副市长", start="~2021", end="", rank="副厅级", note="现任"),

    # ── 肖秋根 ───────────────────────────────────────────────────────────
    dict(person_id="xinyu_xiao_qiugen", org_id="org_xinyu_gov", title="新余市副市长", start="~2021", end="", rank="副厅级", note="现任"),

    # ── 李之旦 ───────────────────────────────────────────────────────────
    dict(person_id="xinyu_li_zhidan", org_id="org_xinyu_gov", title="新余市副市长", start="2025-09", end="", rank="副厅级", note="现任"),
    dict(person_id="xinyu_li_zhidan", org_id="org_xinyu_police", title="新余市公安局局长", start="2025-09", end="", rank="正处级", note="现任"),

    # ── 傅强 ─────────────────────────────────────────────────────────────
    dict(person_id="xinyu_fu_qiang", org_id="org_xinyu_gov", title="新余市政府秘书长", start="~2021", end="", rank="正处级", note="现任"),

    # ── 徐鸿 (Xu Hong - predecessor mayor) ───────────────────────────
    dict(person_id="xinyu_xu_hong", org_id="org_xinyu_gov", title="新余市委副书记、市长", start="2021-04", end="2024-07", rank="正厅级", note="因1·24火灾被撤职"),

    # ── 郑光泉 (Zheng Guangquan - predecessor party secretary) ─────────
    dict(person_id="xinyu_zheng_guangquan", org_id="org_jiangxi_env", title="江西省生态环境厅党组书记", start="~2021", end="2023-07", rank="正厅级", note=""),
    dict(person_id="xinyu_zheng_guangquan", org_id="org_xinyu_cpc", title="新余市委书记", start="2023-07", end="2026-04", rank="正厅级", note=""),

    # ── 张智萍 (Zhang Zhiping) ─────────────────────────────────────
    dict(person_id="xinyu_zhang_zhiping", org_id="org_xinyu_npc", title="新余市人大常委会主任", start="2024", end="", rank="正厅级", note="现任"),

    # ── 犹㼆 (You Ying) ───────────────────────────────────────────
    dict(person_id="xinyu_you_ying", org_id="org_xinyu_gov", title="新余市市长", start="2018", end="2021", rank="正厅级", note=""),
    dict(person_id="xinyu_you_ying", org_id="org_jiangxi_tech", title="江西省科技厅厅长", start="2021", end="~2023", rank="正厅级", note=""),
    dict(person_id="xinyu_you_ying", org_id="org_jiangxi_commerce", title="江西省商务厅厅长", start="~2023", end="", rank="正厅级", note="现任"),

    # ── 董晓健 (Dong Xiaojian) ─────────────────────────────────────
    dict(person_id="xinyu_dong_xiaojian", org_id="org_xinyu_gov", title="新余市市长", start="2015", end="2018", rank="正厅级", note=""),

    # ── 刘捷 (Liu Jie) ────────────────────────────────────────────
    dict(person_id="xinyu_liu_jie", org_id="org_xinyu_cpc", title="新余市委书记", start="2013", end="2016", rank="正厅级", note=""),
    dict(person_id="xinyu_liu_jie", org_id="org_zhejiang_cpc", title="浙江省委副书记", start="~2023", end="", rank="副省级", note="现任"),

    # ── 伍复康 (Wu Fukang) ──────────────────────────────────────────
    dict(person_id="xinyu_wu_fukang", org_id="org_xinyu_college", title="新余学院党委书记", start="~2023", end="", rank="正厅级(?)", note="现任；与南昌县委书记贾彧超为团省委同期"),
]

relationships = [
    # ── 方向军 ↔ 廖良生: 市政府正副手 ───────────────────────────────
    dict(person_a="xinyu_fang_xiangjun", person_b="xinyu_liao_liangsheng",
         type="工作关系", context="方向军任市长/市委书记期间，廖良生任常务副市长，为正副手关系",
         overlap_org="新余市人民政府", overlap_period="2025-"),
    # ── 方向军 → 徐鸿: 接替市长职位 ────────────────────────────────
    dict(person_a="xinyu_fang_xiangjun", person_b="xinyu_xu_hong",
         type="职位接替", context="方向军接替因火灾撤职的徐鸿任新余市长",
         overlap_org="新余市人民政府", overlap_period="2024"),
    # ── 方向军 → 郑光泉: 接替市委书记职位 ────────────────────────────
    dict(person_a="xinyu_fang_xiangjun", person_b="xinyu_zheng_guangquan",
         type="职位接替", context="方向军由市长升任市委书记，接替郑光泉",
         overlap_org="中共新余市委", overlap_period="2026"),
    # ── 徐鸿 ← 1·24火灾问责 │ 郑光泉受处分 ────────────────────────────
    dict(person_a="xinyu_xu_hong", person_b="xinyu_zheng_guangquan",
         type="同案问责", context="均因新余1·24特别重大火灾事故受处分",
         overlap_org="新余市委/市政府", overlap_period="2024"),
    # ── 犹㼆 → 徐鸿: 接替市长职位 ──────────────────────────────────
    dict(person_a="xinyu_you_ying", person_b="xinyu_xu_hong",
         type="职位接替", context="犹㼆调省厅后由徐鸿接任市长",
         overlap_org="新余市人民政府", overlap_period="2021"),
    # ── 张智萍: 三城循环 ──新余→宜春→吉安→新余────────────────────
    dict(person_a="xinyu_zhang_zhiping", person_b="xinyu_fang_xiangjun",
         type="工作关系", context="张智萍任人大主任，方向军任市委书记，为四套班子关系",
         overlap_org="新余市", overlap_period="2024-"),
    # ── 伍复康 ↔ 贾彧超(南昌县) 团省委连接 ──────────────────────────
    # This links to nanchang county investigation;贾彧超 is in nanchang_data.py
    dict(person_a="xinyu_wu_fukang", person_b="xinyu_fang_xiangjun",
         type="间接关系", context="伍复康(新余学院书记)与贾彧超(南昌县委书记)为团省委同期，可作为新余-南昌交流通道",
         overlap_org="", overlap_period=""),
]

# ── Build SQLite ─────────────────────────────────────────────────────────────────
def build_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT, org_id TEXT, title TEXT, start TEXT,
            end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT, person_b TEXT, type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
        CREATE INDEX IF NOT EXISTS idx_person_name ON persons(name);
        CREATE INDEX IF NOT EXISTS idx_org_name ON organizations(name);
        CREATE INDEX IF NOT EXISTS idx_pos_person ON positions(person_id);
        CREATE INDEX IF NOT EXISTS idx_pos_org ON positions(org_id);
    """)
    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES(:id,:name,:gender,:ethnicity,:birth,:birthplace,:education,:party_join,:work_start,:current_post,:current_org,:source)", p)
    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES(:id,:name,:type,:level,:parent,:location)", o)
    for p in positions:
        c.execute("INSERT OR REPLACE INTO positions(person_id,org_id,title,start,end,rank,note) VALUES(:person_id,:org_id,:title,:start,:end,:rank,:note)", p)
    for r in relationships:
        c.execute("INSERT OR REPLACE INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period) VALUES(:person_a,:person_b,:type,:context,:overlap_org,:overlap_period)", r)
    conn.commit()
    for tbl in ["persons","organizations","positions","relationships"]:
        cnt = c.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        print(f"  {tbl}: {cnt}")
    conn.close()

# ── Build GEXF ───────────────────────────────────────────────────────────────────
def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    def color(r, g, b):
        return f'<viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>'

    def node_size(p):
        title = p["current_post"]
        if p["current_org"] == "" and not title.startswith("（原"):  # skip shadow nodes
            return "8.0"
        if "书记" in title and "副" not in title and "副书记" not in title:
            return "20.0"
        return "12.0"

    def person_color(p):
        title = p["current_post"]
        if "书记" in title and "副" not in title and "副书记" not in title:
            return color(220, 50, 50)  # red = top party secretary
        if "市长" in title or "区长" in title or "县长" in title:
            return color(50, 100, 220)  # blue = government lead
        if "常务" in title or "党组副书记" in title:
            return color(50, 150, 255)  # light blue = executive deputy
        if "副市长" in title or "副区长" in title or "副县长" in title:
            return color(100, 120, 255)  # lighter blue = deputy gov
        if "人大" in title or "政协" in title:
            return color(60, 180, 75)  # green = people's congress/political consult
        if "纪委" in title:
            return color(255, 165, 0)   # orange = discipline
        if "组织部" in title:
            return color(200, 100, 200)  # purple = org dept
        if "副" in title:
            return color(160, 130, 80)  # brown = deputy
        return color(100, 100, 100)     # grey = other

    def org_color(o):
        otype = o["type"]
        if "党委" in otype: return color(240, 120, 120)
        if "政府" in otype or "行政" in otype: return color(120, 180, 240)
        if "人大" in otype or "政协" in otype: return color(120, 220, 140)
        if "事业单位" in otype: return color(200, 200, 200)
        return color(180, 180, 180)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append("<graph mode=\"static\" defaultedgetype=\"undirected\">")

    # Attributes
    lines.append("""<attributes class="node">
        <attribute id="type" title="type" type="string"/>
        <attribute id="birth" title="birth" type="string"/>
        <attribute id="birthplace" title="birthplace" type="string"/>
        <attribute id="current_post" title="current_post" type="string"/>
        <attribute id="entity_type" title="entity_type" type="string"/>
        <attribute id="level" title="level" type="string"/>
    </attributes>
    <attributes class="edge">
        <attribute id="type" title="type" type="string"/>
        <attribute id="start" title="start" type="string"/>
        <attribute id="end" title="end" type="string"/>
        <attribute id="context" title="context" type="string"/>
    </attributes>""")

    # Nodes
    lines.append("<nodes>")
    for p in persons:
        sz = node_size(p)
        c = person_color(p)
        current_org = esc(p["current_org"]) if p["current_org"] else "N/A"
        lines.append(f"""<node id="{esc(p['id'])}" label="{esc(p['name'])}">
        {c}
        <viz:size value="{sz}"/>
        <attvalues>
            <attvalue for="type" value="person"/>
            <attvalue for="birth" value="{esc(p['birth'])}"/>
            <attvalue for="birthplace" value="{esc(p['birthplace'])}"/>
            <attvalue for="current_post" value="{esc(p['current_post'])}"/>
            <attvalue for="entity_type" value="person"/>
            <attvalue for="level" value=""/>
        </attvalues>
    </node>""")
    for o in organizations:
        c = org_color(o)
        lines.append(f"""<node id="{esc(o['id'])}" label="{esc(o['name'])}">
        {c}
        <viz:size value="8.0"/>
        <attvalues>
            <attvalue for="type" value="organization"/>
            <attvalue for="birth" value=""/>
            <attvalue for="birthplace" value=""/>
            <attvalue for="current_post" value=""/>
            <attvalue for="entity_type" value="org"/>
            <attvalue for="level" value="{esc(o['level'])}"/>
        </attvalues>
    </node>""")
    lines.append("</nodes>")

    # Edges
    lines.append("<edges>")
    edge_id = 0
    for pos in positions:
        edge_id += 1
        start = esc(pos.get("start", ""))
        end = esc(pos.get("end", ""))
        note = esc(pos.get("note", ""))
        lines.append(f"""<edge id="{edge_id}" source="{esc(pos['person_id'])}" target="{esc(pos['org_id'])}" weight="1.0">
        <attvalues>
            <attvalue for="type" value="worked_at"/>
            <attvalue for="start" value="{start}"/>
            <attvalue for="end" value="{end}"/>
            <attvalue for="context" value="{esc(pos['title'])}. {note}"/>
        </attvalues>
    </edge>""")
    for rel in relationships:
        edge_id += 1
        ctx = esc(rel.get("context", ""))
        period = esc(rel.get("overlap_period", ""))
        # Strong (confirmed) vs weak (indirect/inferred)
        w = "2.0" if rel["type"] in ("工作关系", "职位接替") else "1.0"
        lines.append(f"""<edge id="{edge_id}" source="{esc(rel['person_a'])}" target="{esc(rel['person_b'])}" weight="{w}">
        <attvalues>
            <attvalue for="type" value="{esc(rel['type'])}"/>
            <attvalue for="start" value=""/>
            <attvalue for="end" value=""/>
            <attvalue for="context" value="{ctx} ({period})"/>
        </attvalues>
    </edge>""")
    lines.append("</edges>")
    lines.append("</graph></gexf>")

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {edge_id} edges written")

# ── Main ─────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== 新余市 Leadership Network ===")
    print("[SQLite]")
    build_sqlite()
    print("[GEXF]")
    build_gexf()
    print("Done.")
