#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 红谷滩区 leadership network."""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/honggutan_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/honggutan_network.gexf")

# ── PERSONS ──
persons = [
    # Current 区委
    {"id":1,"name":"陈奕蒙","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"红谷滩区委书记","current_org":"中共南昌市红谷滩区委员会","source":"https://hgt.nc.gov.cn/hgtqrmzf/jryw/202607/31b55b5b280a42c49ca7e534d0b9d24e.shtml"},
    {"id":2,"name":"李婷","gender":"女","ethnicity":"汉族","birth":"1976-11","birthplace":"江西南昌","education":"在职研究生学历（省委党校）","party_join":"","work_start":"","current_post":"红谷滩区委副书记、区长","current_org":"南昌市红谷滩区人民政府","source":"https://hgt.nc.gov.cn/hgtqrmzf/qzfld/202506/373e5fdc220e4a4aa1eb42d59373fe84.shtml"},
    {"id":3,"name":"万晓娟","gender":"女","ethnicity":"汉族","birth":"1982-10","birthplace":"江西南昌","education":"省委党校法学在职研究生/云南大学软件工程硕士","party_join":"2002-11","work_start":"2003-07","current_post":"红谷滩区委副书记","current_org":"中共南昌市红谷滩区委员会","source":"https://hgt.nc.gov.cn"},
    {"id":4,"name":"江龙","gender":"男","ethnicity":"汉族","birth":"1981-09","birthplace":"江西都昌","education":"博士研究生","party_join":"","work_start":"","current_post":"红谷滩区委常委、常务副区长","current_org":"南昌市红谷滩区人民政府","source":"https://hgt.nc.gov.cn/hgtqrmzf/qzfld/bmxxgk_list.shtml"},
    {"id":5,"name":"胡军","gender":"男","ethnicity":"汉族","birth":"1974-10","birthplace":"江西南昌","education":"在职研究生/公共管理硕士","party_join":"2005-11","work_start":"","current_post":"红谷滩区委常委、组织部部长","current_org":"中共南昌市红谷滩区委员会","source":"https://hgt.nc.gov.cn"},
    {"id":6,"name":"陈敏","gender":"男","ethnicity":"汉族","birth":"1977-03","birthplace":"江西上高","education":"在职研究生","party_join":"1998-11","work_start":"2000-08","current_post":"红谷滩区委常委、统战部部长","current_org":"中共南昌市红谷滩区委员会","source":"https://hgt.nc.gov.cn"},
    {"id":7,"name":"唐武","gender":"男","ethnicity":"汉族","birth":"1970-03","birthplace":"江西南昌","education":"本科","party_join":"","work_start":"1991-07","current_post":"红谷滩区委常委、政法委书记","current_org":"中共南昌市红谷滩区委员会","source":"https://hgt.nc.gov.cn"},
    {"id":8,"name":"徐军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"红谷滩区委常委、纪委书记、监委主任","current_org":"中共南昌市红谷滩区纪律检查委员会","source":"https://hgt.nc.gov.cn"},
    {"id":9,"name":"黄小明","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"红谷滩区委常委、人武部上校部长","current_org":"南昌市红谷滩区人民武装部","source":"https://hgt.nc.gov.cn"},
    {"id":10,"name":"周晓东","gender":"男","ethnicity":"汉族","birth":"1985-11","birthplace":"","education":"大学","party_join":"","work_start":"","current_post":"红谷滩区委常委、宣传部部长","current_org":"中共南昌市红谷滩区委员会","source":"https://hgt.nc.gov.cn"},
    {"id":11,"name":"周结华","gender":"男","ethnicity":"汉族","birth":"1983-01","birthplace":"江西万年","education":"研究生/工学博士","party_join":"","work_start":"","current_post":"红谷滩区委常委、副区长","current_org":"南昌市红谷滩区人民政府","source":"https://hgt.nc.gov.cn"},
    {"id":12,"name":"朱志翔","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"红谷滩区副区长","current_org":"南昌市红谷滩区人民政府","source":"https://hgt.nc.gov.cn/hgtqrmzf/qzfld/bmxxgk_list.shtml"},
    {"id":13,"name":"张莲波","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"红谷滩区副区长","current_org":"南昌市红谷滩区人民政府","source":"https://hgt.nc.gov.cn/hgtqrmzf/qzfld/bmxxgk_list.shtml"},
    {"id":14,"name":"熊飞","gender":"男","ethnicity":"汉族","birth":"1975-09","birthplace":"江西新建","education":"南昌大学MBA/在职研究生","party_join":"","work_start":"","current_post":"红谷滩区副区长","current_org":"南昌市红谷滩区人民政府","source":"https://hgt.nc.gov.cn/hgtqrmzf/qzfld/bmxxgk_list.shtml"},
    {"id":15,"name":"陈羽","gender":"女","ethnicity":"汉族","birth":"1982-12","birthplace":"","education":"大学","party_join":"民建会员（非中共党员）","work_start":"","current_post":"红谷滩区副区长","current_org":"南昌市红谷滩区人民政府","source":"https://hgt.nc.gov.cn/hgtqrmzf/qzfld/bmxxgk_list.shtml"},
    {"id":16,"name":"徐辉","gender":"男","ethnicity":"汉族","birth":"1983-11","birthplace":"","education":"研究生","party_join":"","work_start":"","current_post":"红谷滩区副区长","current_org":"南昌市红谷滩区人民政府","source":"https://hgt.nc.gov.cn/hgtqrmzf/qzfld/bmxxgk_list.shtml"},
    # Predecessors
    {"id":17,"name":"刘光荣","gender":"男","ethnicity":"汉族","birth":"1972-11","birthplace":"江西南昌县","education":"大学/哲学学士","party_join":"1995-04","work_start":"1995-12","current_post":"东湖区委书记","current_org":"中共南昌市东湖区委员会","source":"https://dhq.nc.gov.cn/dhqrmzf/qwld/202502/05326f5c302b432192d95b75837b694b.shtml"},
    {"id":18,"name":"涂晓晖","gender":"男","ethnicity":"汉族","birth":"1976-05","birthplace":"","education":"大学/公共管理硕士","party_join":"","work_start":"","current_post":"（原红谷滩区委书记，去向待查）","current_org":"","source":"https://baike.baidu.com/item/%E6%B6%82%E6%99%93%E6%99%96"},
    {"id":19,"name":"吴江辉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"（原红谷滩区委书记，去向待查）","current_org":"","source":"https://news.sina.com.cn/c/2021-07-24/doc-ikqcfnca6365908.shtml"},
    # Cross-district connections
    {"id":20,"name":"王成久","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"新建区委副书记、区长","current_org":"南昌市新建区人民政府","source":"https://news.sina.com.cn/c/2021-07-24/doc-ikqcfnca6365908.shtml"},
    {"id":21,"name":"周亮","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"（原红谷滩区委书记，2024年8月被查）","current_org":"","source":"https://news.sina.com.cn"},
    {"id":22,"name":"邓之武","gender":"男","ethnicity":"汉族","birth":"","birthplace":"江西万年","education":"","party_join":"","work_start":"","current_post":"东湖区委副书记、代区长","current_org":"南昌市东湖区人民政府","source":"https://dhq.nc.gov.cn/dhqrmzf/rsrm/202607/debeb85666a34617bab6e21af9d66e95.shtml"},
    # 红谷滩新区时期管委会主任（历史）
    {"id":23,"name":"卢晓健","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"（原南昌市政协副主席）","current_org":"南昌市政协","source":""},
    {"id":24,"name":"宋铀","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"（原南昌市副市长）","current_org":"南昌市人民政府","source":""},
]

# ── ORGANIZATIONS ──
organizations = [
    {"id":1,"name":"中共南昌市红谷滩区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市红谷滩区"},
    {"id":2,"name":"南昌市红谷滩区人民政府","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市红谷滩区"},
    {"id":3,"name":"中共南昌市红谷滩区纪律检查委员会","type":"党委","level":"区级","parent":"南昌市纪律检查委员会","location":"江西省南昌市红谷滩区"},
    {"id":4,"name":"南昌市红谷滩区人民武装部","type":"政府","level":"区级","parent":"南昌警备区","location":"江西省南昌市红谷滩区"},
    {"id":5,"name":"中共南昌市东湖区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市东湖区"},
    {"id":6,"name":"南昌市东湖区人民政府","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市东湖区"},
    {"id":7,"name":"中共南昌市委员会","type":"党委","level":"市级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":8,"name":"南昌市人民政府","type":"政府","level":"市级","parent":"","location":"江西省南昌市"},
    {"id":9,"name":"南昌市财政局","type":"政府","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":10,"name":"南昌市人民政府驻深圳办事处","type":"政府","level":"市级","parent":"南昌市人民政府","location":"广东省深圳市"},
    {"id":11,"name":"南昌市人民政府驻广东办事处","type":"政府","level":"市级","parent":"南昌市人民政府","location":"广东省广州市"},
    {"id":12,"name":"南昌市新建区人民政府","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市新建区"},
    {"id":13,"name":"红谷滩新区管委会","type":"开发区","level":"副厅级","parent":"南昌市人民政府","location":"江西省南昌市红谷滩区"},
    {"id":14,"name":"南昌市国资委","type":"政府","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":15,"name":"南昌市政协","type":"政协","level":"市级","parent":"","location":"江西省南昌市"},
    {"id":16,"name":"南昌市委组织部","type":"党委","level":"市级","parent":"中共南昌市委员会","location":"江西省南昌市"},
    {"id":17,"name":"中共青云谱区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市青云谱区"},
    {"id":18,"name":"南昌市西湖区人民政府","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市西湖区"},
    {"id":19,"name":"南昌市红谷滩城投集团","type":"国企","level":"区级","parent":"红谷滩区人民政府","location":"江西省南昌市红谷滩区"},
]

# ── POSITIONS ──
positions = [
    # 陈奕蒙(1) — current 区委书记
    {"id":1,"person_id":1,"org_id":12,"title":"新建区委书记","start":"~2021","end":"2026-06","rank":"副厅级","note":"前任新建区委书记"},
    {"id":2,"person_id":1,"org_id":1,"title":"红谷滩区委书记","start":"2026-07","end":"","rank":"副厅级","note":"2026年7月南昌六县区联动调整上任"},
    # 李婷(2) — current 区长
    {"id":3,"person_id":2,"org_id":6,"title":"东湖区委常委、副区长","start":"~2021","end":"~2024","rank":"副处级","note":"在东湖区担任副区长、常委"},
    {"id":4,"person_id":2,"org_id":10,"title":"南昌市政府驻深圳办事处主任","start":"~2024","end":"~2025","rank":"正处级","note":""},
    {"id":5,"person_id":2,"org_id":11,"title":"南昌市政府驻广东办事处党组书记、主任","start":"~2024","end":"2025-05","rank":"正处级","note":"同时兼任"},
    {"id":6,"person_id":2,"org_id":2,"title":"红谷滩区委副书记、代区长→区长","start":"2025-05","end":"","rank":"正处级","note":"2025.05代区长，2025.08.15正式当选区长"},
    # 万晓娟(3) — 区委副书记
    {"id":7,"person_id":3,"org_id":16,"title":"南昌市委组织部办公室主任→部务委员","start":"~2013","end":"~2021","rank":"副处级","note":""},
    {"id":8,"person_id":3,"org_id":13,"title":"红谷滩新区工委委员、管委会副主任","start":"~2021","end":"~2023","rank":"副处级","note":"新区时期"},
    {"id":9,"person_id":3,"org_id":1,"title":"红谷滩区委副书记","start":"~2021","end":"","rank":"副处级","note":"兼任区委党校校长"},
    # 江龙(4) — 常务副区长
    {"id":10,"person_id":4,"org_id":2,"title":"红谷滩区副区长→常务副区长","start":"2023-02","end":"","rank":"副处级","note":"2023.02任命副区长，后任区委常委、常务副区长"},
    # 胡军(5) — 组织部部长
    {"id":11,"person_id":5,"org_id":1,"title":"红谷滩区委常委、组织部部长","start":"","end":"","rank":"副处级","note":""},
    # 陈敏(6) — 统战部
    {"id":12,"person_id":6,"org_id":1,"title":"红谷滩区委常委、统战部部长","start":"","end":"","rank":"副处级","note":""},
    # 唐武(7) — 政法委
    {"id":13,"person_id":7,"org_id":1,"title":"红谷滩区委常委、政法委书记","start":"","end":"","rank":"副处级","note":""},
    # 徐军(8) — 纪委书记
    {"id":14,"person_id":8,"org_id":3,"title":"红谷滩区委常委、纪委书记、监委主任","start":"2024-06","end":"","rank":"副处级","note":"2024.06到任，2025.01补选监委主任"},
    # 周晓东(10) — 宣传部
    {"id":15,"person_id":10,"org_id":1,"title":"红谷滩区委常委、宣传部部长","start":"2024-12","end":"","rank":"副处级","note":"此前任南昌市教育局总督学"},
    # 周结华(11) — 常委副区长
    {"id":16,"person_id":11,"org_id":2,"title":"红谷滩区委常委、副区长","start":"2025-01","end":"","rank":"副处级","note":"2025.01补选"},
    # 熊飞(14) — 副区长
    {"id":17,"person_id":14,"org_id":19,"title":"红谷滩城投集团董事长","start":"~2018","end":"~2021","rank":"区属国企","note":""},
    {"id":18,"person_id":14,"org_id":2,"title":"红谷滩区副区长","start":"~2021","end":"","rank":"副处级","note":"从城投集团转政府任职"},
    # 陈羽(15) — 副区长
    {"id":19,"person_id":15,"org_id":2,"title":"红谷滩区副区长","start":"~2023-07","end":"","rank":"副处级","note":"民建成员，南昌市发改委规划法规科科长升任"},
    # 徐辉(16) — 副区长
    {"id":20,"person_id":16,"org_id":2,"title":"红谷滩区副区长","start":"~2023-12","end":"","rank":"副处级","note":""},
    # 刘光荣(17) — 前任区长
    {"id":21,"person_id":17,"org_id":2,"title":"红谷滩区委副书记、区长","start":"~2020-06","end":"2025-05","rank":"正处级","note":"红谷滩区首任区长，任职约5年"},
    {"id":22,"person_id":17,"org_id":5,"title":"东湖区委书记","start":"2025-02","end":"","rank":"正处级","note":"2025年调任东湖区委书记"},
    # 涂晓晖(18) — 前任书记
    {"id":23,"person_id":18,"org_id":9,"title":"南昌市财政局局长","start":"~2020","end":"2023-06","rank":"正处级","note":""},
    {"id":24,"person_id":18,"org_id":1,"title":"红谷滩区委书记","start":"2023-06","end":"~2026-06","rank":"副厅级","note":"接替吴江辉任红谷滩区委书记"},
    # 吴江辉(19) — 前任书记
    {"id":25,"person_id":19,"org_id":17,"title":"青云谱区委副书记、区长","start":"~2016","end":"~2021-07","rank":"正处级","note":"青云谱区长"},
    {"id":26,"person_id":19,"org_id":1,"title":"红谷滩区委书记","start":"2021-08","end":"2023-06","rank":"副厅级","note":"接替周亮任红谷滩区委书记"},
    # 邓之武(22) — 东湖代区长
    {"id":27,"person_id":22,"org_id":6,"title":"东湖区委副书记、代区长","start":"~2026-07","end":"","rank":"正处级","note":"接替刘光荣调离后空缺"},
    # 卢晓健(23) — 新区时期
    {"id":28,"person_id":23,"org_id":13,"title":"红谷滩新区管委会主任","start":"~2007","end":"~2011","rank":"副厅级","note":"新区时期早期负责人"},
    # 宋铀(24) — 新区时期
    {"id":29,"person_id":24,"org_id":13,"title":"红谷滩新区管委会主任","start":"~2016","end":"2020","rank":"副厅级","note":"新区最后一位主任，设区后任南昌市副市长"},
]

# ── RELATIONSHIPS ──
relationships = [
    # 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"陈奕蒙（区委书记）与李婷（区长）为红谷滩区党政一把手","overlap_org":"红谷滩区","overlap_period":"2026-07至今"},
    # 职务接替 - 书记
    {"id":2,"person_a":18,"person_b":1,"type":"职务接替","context":"涂晓晖（原书记）→ 陈奕蒙任红谷滩区委书记","overlap_org":"红谷滩区委","overlap_period":"不重叠（前后任）"},
    {"id":3,"person_a":19,"person_b":18,"type":"职务接替","context":"吴江辉（原书记）→ 涂晓晖任红谷滩区委书记","overlap_org":"红谷滩区委","overlap_period":"不重叠（前后任）"},
    {"id":4,"person_a":21,"person_b":19,"type":"职务接替","context":"周亮（原书记）→ 吴江辉任红谷滩区委书记（周亮2024年8月被查）","overlap_org":"红谷滩区委","overlap_period":"不重叠（前后任）"},
    # 职务接替 - 区长
    {"id":5,"person_a":17,"person_b":2,"type":"职务接替","context":"刘光荣（原区长）→ 李婷任红谷滩区长","overlap_org":"红谷滩区政府","overlap_period":"不重叠（前后任）"},
    # 跨区联系：刘光荣（红谷滩→东湖）
    {"id":6,"person_a":17,"person_b":22,"type":"党政搭档","context":"刘光荣（东湖区委书记）与邓之武（东湖代区长）为东湖区党政搭档","overlap_org":"东湖区","overlap_period":"~2026-07至今"},
    # 跨区联系：李婷（东湖→红谷滩）
    {"id":7,"person_a":2,"person_b":22,"type":"东湖同事","context":"李婷（原东湖副区长）与邓之武（东湖代区长）均在东湖区政府任职","overlap_org":"东湖区政府","overlap_period":"~2021-~2024"},
    # 跨区联系：吴江辉（青云谱→红谷滩）
    {"id":8,"person_a":19,"person_b":17,"type":"红谷滩搭档","context":"吴江辉（红谷滩区委书记）与刘光荣（红谷滩区长）曾为红谷滩区党政一把手搭档","overlap_org":"红谷滩区","overlap_period":"2021-2023"},
    # 跨区联系：涂晓晖（财政局→红谷滩）
    {"id":9,"person_a":18,"person_b":17,"type":"红谷滩搭档","context":"涂晓晖（红谷滩区委书记）与刘光荣（红谷滩区长）曾为红谷滩区党政搭档","overlap_org":"红谷滩区","overlap_period":"2023-2025"},
    # 跨区联系：陈奕蒙（新建→红谷滩）
    {"id":10,"person_a":1,"person_b":20,"type":"新建同事","context":"陈奕蒙（原新建区委书记）与王成久（新建区长）曾在新建区党政搭档","overlap_org":"新建区","overlap_period":"~2021-2026"},
    # 万晓娟与市委组织部联系
    {"id":11,"person_a":3,"person_b":7,"type":"组织系统同事","context":"万晓娟（红谷滩区委副书记）曾在市委组织部工作多年","overlap_org":"市委组织部","overlap_period":"~2013-~2021"},
    # 熊飞与红谷滩城投
    {"id":12,"person_a":14,"person_b":2,"type":"政府国企流转","context":"熊飞从红谷滩城投集团董事长转任区副区长，系国企→政府转岗","overlap_org":"红谷滩区","overlap_period":"~2021-至今"},
]

# ── BUILD SQLITE ──
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT);
CREATE TABLE IF NOT EXISTS organizations (id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT);
CREATE TABLE IF NOT EXISTS positions (id INTEGER PRIMARY KEY,person_id INTEGER,org_id INTEGER,title TEXT,start TEXT,"end" TEXT,rank TEXT,note TEXT,FOREIGN KEY(person_id) REFERENCES persons(id),FOREIGN KEY(org_id) REFERENCES organizations(id));
CREATE TABLE IF NOT EXISTS relationships (id INTEGER PRIMARY KEY,person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT,FOREIGN KEY(person_a) REFERENCES persons(id),FOREIGN KEY(person_b) REFERENCES persons(id));
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")
for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
conn.commit()

counts = {}
for t in ["persons","organizations","positions","relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t,n in counts.items():
    print(f"  {t}: {n} records")

# ── BUILD GEXF ──
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "区委书记" in post: return "255,50,50"
    elif "区长" in post or "副区长" in post or "代区长" in post: return "50,100,255"
    elif "纪委书记" in post or "监委" in post: return "255,165,0"
    elif "政法委" in post: return "150,100,200"
    elif "宣传部" in post: return "100,200,150"
    elif "组织部" in post: return "200,150,100"
    elif "统战部" in post: return "200,100,150"
    elif "人武部" in post: return "100,150,100"
    return "100,100,100"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200","群团":"255,220,255","事业单位":"220,220,220","开发区":"200,255,200","国企":"255,255,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>红谷滩区领导班子工作关系网络 — 2026年7月14日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid,atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post"),("4","entity_type"),("5","level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid,atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c = pcolor(p.get("current_post",""))
    sz = "20.0" if "书记" in p.get("current_post","") and "区委" in p.get("current_post","") else ("20.0" if p["id"] in [2] else "12.0")
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f,v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('      </attvalue>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('      </attvalue>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

tn = len(persons) + len(organizations)
te = len(positions) + len(relationships)
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone!")
