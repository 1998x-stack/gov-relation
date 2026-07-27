#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 左云县 leadership."""
import sqlite3, os

SLUG = "左云县"
TODAY = "2026-07-26"
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "database", "zuoyun_network.db")
GEXF_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "graph", "zuoyun_network.gexf")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

# ══════════════════════════════════════════════════════════════════════
# DATA — sourced from zuoyun.gov.cn (左云县人民政府官方网站)
# ══════════════════════════════════════════════════════════════════════

# ID convention: zuoyun_{surname_givenname}

persons = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
    ("zuoyun_luo_shibin",    "罗士彬", "男", "汉族", "", "", "", "", "", "县委书记", "中共左云县委",
     "http://www.zuoyun.gov.cn/zyxrmzfz/index.shtml"),
    ("zuoyun_yu_haibin",     "于海滨", "男", "汉族", "", "", "", "", "", "原县长（已离任）", "左云县人民政府",
     "http://www.zuoyun.gov.cn/zyxrmzfz/szf/zfld.shtml"),
    ("zuoyun_cao_yongtao",   "曹永涛", "男", "汉族", "1978-07", "", "大学", "", "", "县委常委、县政府党组副书记、副县长（常务）", "左云县人民政府",
     "http://www.zuoyun.gov.cn/zyxrmzfz/FQZHY/szfld.shtml"),
    ("zuoyun_xi_zhijun",     "席志俊", "男", "汉族", "1976-12", "", "大学", "", "", "县委常委、县政府党组成员、副县长", "左云县人民政府",
     "http://www.zuoyun.gov.cn/zyxrmzfz/hgh/szfld.shtml"),
    ("zuoyun_jin_junhua",    "金俊华", "男", "汉族", "1970-06", "", "大学本科", "", "", "副县长、县公安局党委书记、局长", "左云县人民政府",
     "http://www.zuoyun.gov.cn/zyxrmzfz/jjh/szfld.shtml"),
    ("zuoyun_gao_peng",      "高鹏",   "男", "汉族", "1977-05", "", "大学", "", "", "副县长", "左云县人民政府",
     "http://www.zuoyun.gov.cn/zyxrmzfz/gaopeng/szfld.shtml"),
    ("zuoyun_zhang_zhihong", "张志宏", "男", "汉族", "1979-10", "", "大学，在职研究生", "", "", "副县长", "左云县人民政府",
     "http://www.zuoyun.gov.cn/zyxrmzfz/lxy/szfld.shtml"),
    ("zuoyun_zhang_xiaomei", "张晓梅", "女", "汉族", "1976-05", "", "大学本科", "", "", "副县长", "左云县人民政府",
     "http://www.zuoyun.gov.cn/zyxrmzfz/wzc/szfld.shtml"),
    ("zuoyun_li_wei",        "李伟",   "男", "汉族", "1984-12", "", "大学本科", "", "", "副县长", "左云县人民政府",
     "http://www.zuoyun.gov.cn/zyxrmzfz/liwei/szfld.shtml"),
    ("zuoyun_huang_shanyuan","黄山园", "男", "汉族", "1985-12", "", "硕士研究生", "", "", "副县长（挂职）", "左云县人民政府",
     "http://www.zuoyun.gov.cn/zyxrmzfz/huansy/szfld.shtml"),
    ("zuoyun_wang_junyun",   "王俊云", "男", "汉族", "1973-12", "", "大专", "", "", "县政府党组成员、左云经开区党工委副书记、管委会主任", "左云经济技术开发区",
     "http://www.zuoyun.gov.cn/zyxrmzfz/qbw/szfld.shtml"),
]

# Additional leaders identified from news articles
# From: 县委常委会会议 (2026-07-10): 高晶、何长青、崔发、王俊云、杜红梅、席志俊、张健、吴宇杰、王光射
# From: 县安委会会议 (2026-07-15): 金俊华、高鹏、张志宏、张晓梅、黄山园、李福

organizations = [
    # (id, name, type, level, parent, location)
    ("zuoyun_psc",  "中共左云县委", "党委", "县级", "中共大同市委", "左云县"),
    ("zuoyun_gov",  "左云县人民政府", "政府", "县级", "大同市人民政府", "左云县"),
    ("zuoyun_ez",   "左云经济技术开发区", "开发区", "县级", "左云县人民政府", "左云县"),
    ("zuoyun_psb",  "左云县公安局", "政府机构", "县级", "左云县人民政府", "左云县"),
]

positions = [
    # (person_id, org_id, title, start_date, end_date, rank, note)
    ("zuoyun_luo_shibin", "zuoyun_psc", "县委书记", "", "", "正处级", "县委常委会会议主持"),
    ("zuoyun_yu_haibin", "zuoyun_gov", "原县长（已离任）", "", "", "正处级", "网站链接已注释掉，个人页面404"),
    ("zuoyun_cao_yongtao", "zuoyun_gov", "副县长（常务）", "", "", "副处级", "县政府党组副书记、县委常委。分管：县政府办公室、发改工信和科技商务局、应急管理局、统计局等"),
    ("zuoyun_xi_zhijun", "zuoyun_gov", "副县长", "", "", "副处级", "县委常委、县政府党组成员。分管：农业农村和水务局、乡村振兴、环保等"),
    ("zuoyun_jin_junhua", "zuoyun_gov", "副县长", "", "", "副处级", "县公安局党委书记、局长。分管：公安、司法、信访"),
    ("zuoyun_gao_peng", "zuoyun_gov", "副县长", "", "", "副处级", "分管：规划和自然资源、教育体育、文化旅游、广播电视、文物保护"),
    ("zuoyun_zhang_zhihong", "zuoyun_gov", "副县长", "", "", "副处级", "分管：财政税务、民政人社、医疗保障、退役军人"),
    ("zuoyun_zhang_xiaomei", "zuoyun_gov", "副县长", "", "", "副处级", "分管：卫生健康、市场监管、优化营商环境"),
    ("zuoyun_li_wei", "zuoyun_gov", "副县长", "", "", "副处级", "分管：住房和城乡建设、交通运输、搬迁安置"),
    ("zuoyun_huang_shanyuan", "zuoyun_gov", "副县长（挂职）", "", "", "副处级", "挂职干部。原单位：山西省供销合作社联合社财务处副处长。协助曹永涛"),
    ("zuoyun_wang_junyun", "zuoyun_ez", "经开区管委会主任", "", "", "副处级", "县政府党组成员。分管：招商引资"),
]

relationships = [
    # (person_a, person_b, type, context, overlap_org, overlap_period)
    ("zuoyun_luo_shibin", "zuoyun_cao_yongtao", "党政搭档", "县委书记与常务副县长", "中共左云县委/左云县人民政府", "至今"),
    ("zuoyun_luo_shibin", "zuoyun_xi_zhijun", "党政交叉任职", "县委书记与县委常委/副县长", "中共左云县委", "至今"),
    ("zuoyun_cao_yongtao", "zuoyun_xi_zhijun", "同级同事", "两名县委常委", "中共左云县委", "至今"),
    ("zuoyun_cao_yongtao", "zuoyun_huang_shanyuan", "协助关系", "常务副县长与挂职副县长（协助对象）", "左云县人民政府", "至今"),
    ("zuoyun_jin_junhua", "zuoyun_gao_peng", "同级同事", "副县长之间", "左云县人民政府", "至今"),
    ("zuoyun_jin_junhua", "zuoyun_zhang_zhihong", "同级同事", "副县长之间", "左云县人民政府", "至今"),
    ("zuoyun_jin_junhua", "zuoyun_zhang_xiaomei", "同级同事", "副县长之间", "左云县人民政府", "至今"),
    ("zuoyun_jin_junhua", "zuoyun_li_wei", "同级同事", "副县长之间", "左云县人民政府", "至今"),
    ("zuoyun_jin_junhua", "zuoyun_gao_peng", "会议同场", "县安委会会议同场", "左云县人民政府", "2026-07-15"),
    ("zuoyun_jin_junhua", "zuoyun_zhang_zhihong", "会议同场", "县安委会会议同场", "左云县人民政府", "2026-07-15"),
    ("zuoyun_jin_junhua", "zuoyun_zhang_xiaomei", "会议同场", "县安委会会议同场", "左云县人民政府", "2026-07-15"),
    ("zuoyun_jin_junhua", "zuoyun_huang_shanyuan", "会议同场", "县安委会会议同场", "左云县人民政府", "2026-07-15"),
    ("zuoyun_gao_peng", "zuoyun_zhang_zhihong", "会议同场", "县安委会会议同场", "左云县人民政府", "2026-07-15"),
    ("zuoyun_gao_peng", "zuoyun_zhang_xiaomei", "会议同场", "县安委会会议同场", "左云县人民政府", "2026-07-15"),
    ("zuoyun_gao_peng", "zuoyun_huang_shanyuan", "会议同场", "县安委会会议同场", "左云县人民政府", "2026-07-15"),
    ("zuoyun_zhang_zhihong", "zuoyun_zhang_xiaomei", "会议同场", "县安委会会议同场", "左云县人民政府", "2026-07-15"),
    ("zuoyun_zhang_zhihong", "zuoyun_huang_shanyuan", "会议同场", "县安委会会议同场", "左云县人民政府", "2026-07-15"),
    ("zuoyun_zhang_xiaomei", "zuoyun_huang_shanyuan", "会议同场", "县安委会会议同场", "左云县人民政府", "2026-07-15"),
    ("zuoyun_wang_junyun", "zuoyun_cao_yongtao", "上下级", "经开区主任与常务副县长（政府党组）", "左云县人民政府", "至今"),
]

# ══════════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ══════════════════════════════════════════════════════════════════════

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
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
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
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
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    conn.commit()

def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 左云县人民政府网站 (zuoyun.gov.cn) 及新闻报道")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        conn.execute(f"INSERT OR REPLACE INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", p)

    # Insert organizations
    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        conn.execute(f"INSERT OR REPLACE INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", o)

    # Insert positions
    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", pos)

    # Insert relationships
    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", r)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "县委书记" in post:
            return ("255,50,50", 20.0)
        elif "县长" in post:
            return ("50,100,255", 20.0)
        elif "常务" in post:
            return ("50,100,255", 15.0)
        elif "副县长" in post and "挂职" not in post:
            return ("100,100,255", 12.0)
        elif "挂职" in post:
            return ("100,200,100", 12.0)
        elif "经开区" in post:
            return ("255,180,100", 12.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "开发区": ("255,230,180"),
            "政府机构": ("200,200,255"),
        }.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    for p in persons:
        c, sz = person_color(p[9])  # current_post at index 9
        lines.append(f'      <node id="p{p[0]}" label="{esc(p[1])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p[9])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p[10])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p[4])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p[11])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o[2])  # type at index 2
        cr, cg, cb = [int(x) for x in c.split(",")]
        lines.append(f'      <node id="o{o[0]}" label="{esc(o[1])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos[0]}" target="o{pos[1]}" label="{esc(pos[2])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos[6])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r[0]}" target="p{r[1]}" label="{esc(r[2])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r[2])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r[3])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r[4])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r[5])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")

if __name__ == "__main__":
    run_build()
