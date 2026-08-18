#!/usr/bin/env python3
"""
乾县跨县干部交流网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

研究范围：乾县（陕西省咸阳市下辖县）与周边县区的干部交流网络
研究日期：2026-07-25
任务ID: shaanxi_乾县_cross_county

数据来源：
  - Wikipedia (en.wikipedia.org) — Shangguan Jiqing, Xu Xinrong 等人物详情
  - 乾县政府网站 (www.snqianxian.gov.cn) — 领导之窗
  - 咸阳市人民政府 (www.xianyang.gov.cn)
  - 礼泉县/永寿县/泾阳县 政府网站
  - 本项目已有 build_乾县_data.py 等脚本采集数据

关键发现：
  - 上官吉庆（乾县人）：乾县县委书记(1999-2002)→咸阳副市长→宝鸡市长/书记→西安市市长（已落马）
  - 徐新荣（乾县人）：秦都区委书记(2000-2004)→咸阳市委副书记→渭南市长/书记→延安市委书记→陕西省政协主席
  - 闫兴斌（现任乾县县委书记，1971年生）：前任乾县县长后升任县委书记
  - 焦志鹏：闫兴斌前任乾县县委书记，后调任咸阳市
  - 冷劲松（现任咸阳市委书记）：原咸阳市市长后升任，管辖乾县
"""
import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

USING_RUNNER = False
try:
    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
    USING_RUNNER = True
except ImportError:
    pass

SLUG = "乾县跨县交流"
DATE = "2026-07-25"

# ===== 人物数据 =====
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, confidence)
persons = [
    # --- 乾县现任领导（含跨县经历） ---
    (1, "闫兴斌", "男", "汉族", "1971年9月", "", "研究生学历", "中共党员", "",
     "县委书记", "中共乾县县委",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/yxb/", "confirmed"),
    (2, "段志华", "男", "汉族", "1974年4月", "", "研究生学历", "中共党员", "",
     "县委副书记、县长", "乾县人民政府",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/dzha/", "confirmed"),
    (3, "刘春锋", "男", "汉族", "", "", "", "中共党员", "",
     "县委副书记", "中共乾县县委",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/", "confirmed"),
    (4, "吴元操", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、组织部部长", "中共乾县县委组织部",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/", "confirmed"),
    (5, "孙佳佳", "男", "汉族", "1986年2月", "", "研究生学历，工学硕士", "中共党员", "",
     "县委常委、常务副县长", "乾县人民政府",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zfld/sjj/", "confirmed"),

    # --- 乾县历任主要领导（跨县/调出） ---
    (6, "上官吉庆", "男", "汉族", "1963年3月", "乾县", "陕西商业专科学校", "中共党员", "1980年8月",
     "（已落马）", "（原西安市市长）",
     "https://en.wikipedia.org/wiki/Shangguan_Jiqing", "confirmed"),
    (7, "徐新荣", "男", "汉族", "1962年4月", "乾县", "中央党校研究生", "中共党员", "1983年8月",
     "陕西省政协主席（正省级）", "中国人民政治协商会议陕西省委员会",
     "https://en.wikipedia.org/wiki/Xu_Xinrong", "confirmed"),
    (8, "焦志鹏", "男", "汉族", "", "", "", "中共党员", "",
     "（原乾县县委书记，已调任）", "",
     "https://www.snqianxian.gov.cn/", "plausible"),

    # --- 邻近县区主要领导班子（用于建立跨县联系） ---
    # 礼泉县
    (9, "姚俊峰", "男", "汉族", "", "", "", "中共党员", "",
     "县委书记", "中共礼泉县委",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (10, "吴云锋", "男", "汉族", "", "", "", "中共党员", "",
     "县委副书记、县长", "礼泉县人民政府",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    # 永寿县
    (11, "杨孟珠", "男", "汉族", "", "", "", "中共党员", "",
     "县委书记", "中共永寿县委员会",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/ymz/", "confirmed"),
    (12, "闫启东", "男", "汉族", "", "", "", "中共党员", "",
     "县委副书记、县长", "永寿县人民政府",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/", "confirmed"),
    # 泾阳县
    (13, "郝瑞耀", "男", "汉族", "1984年8月", "", "研究生学历", "中共党员", "",
     "县委书记", "中共泾阳县委员会",
     "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xw/hry/", "confirmed"),
    (14, "王洲", "男", "汉族", "1976年9月", "", "中央党校大学学历", "中共党员", "",
     "县委副书记、县长", "泾阳县人民政府",
     "https://www.snjingyang.gov.cn/zfxxgk/fdzdgknr/ldzc/xw/wz/", "confirmed"),
    # 咸阳市领导
    (15, "冷劲松", "男", "汉族", "", "", "", "中共党员", "",
     "市委书记", "中共咸阳市委员会",
     "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260715_2101330.html", "confirmed"),
    (16, "贾珉亮", "男", "汉族", "", "", "", "中共党员", "",
     "市长", "咸阳市人民政府",
     "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260724_2103540.html", "confirmed"),
    (17, "夏晓中", "男", "汉族", "", "", "", "中共党员", "",
     "（原咸阳市委书记）", "",
     "https://www.xianyang.gov.cn/", "plausible"),
    # 陕西省领导
    (18, "赵一德", "男", "汉族", "1965年2月", "浙江温岭", "浙江省委党校研究生", "中共党员", "1983年8月",
     "陕西省委书记", "中共陕西省委员会",
     "https://en.wikipedia.org/wiki/Zhao_Yide", "confirmed"),
    (19, "赵刚", "男", "汉族", "1968年6月", "辽宁新民", "北京理工大学学士", "中共党员", "1993年4月",
     "陕西省省长", "陕西省人民政府",
     "https://en.wikipedia.org/wiki/Zhao_Gang_(born_1968)", "confirmed"),
]

# ===== 组织数据 =====
# (id, name, type, level, parent, location)
organizations = [
    # 乾县
    (1, "中共乾县县委", "党委", "县处级", "中共咸阳市委", "陕西省咸阳市乾县"),
    (2, "乾县人民政府", "政府", "县处级", "咸阳市人民政府", "陕西省咸阳市乾县"),
    (3, "中共乾县县委组织部", "党委部门", "正科级", "中共乾县县委", "陕西省咸阳市乾县"),
    # 邻近县区
    (4, "中共礼泉县委", "党委", "县处级", "中共咸阳市委", "陕西省咸阳市礼泉县"),
    (5, "礼泉县人民政府", "政府", "县处级", "咸阳市人民政府", "陕西省咸阳市礼泉县"),
    (6, "中共永寿县委员会", "党委", "县处级", "中共咸阳市委", "陕西省咸阳市永寿县"),
    (7, "永寿县人民政府", "政府", "县处级", "咸阳市人民政府", "陕西省咸阳市永寿县"),
    (8, "中共泾阳县委员会", "党委", "县处级", "中共咸阳市委", "陕西省咸阳市泾阳县"),
    (9, "泾阳县人民政府", "政府", "县处级", "咸阳市人民政府", "陕西省咸阳市泾阳县"),
    # 咸阳市
    (10, "中共咸阳市委员会", "党委", "地级市", "中共陕西省委员会", "陕西省咸阳市"),
    (11, "咸阳市人民政府", "政府", "地级市", "陕西省人民政府", "陕西省咸阳市"),
    # 陕西省
    (12, "中共陕西省委员会", "党委", "省级", "中共中央", "陕西省西安市"),
    (13, "陕西省人民政府", "政府", "省级", "国务院", "陕西省西安市"),
    (14, "中国人民政治协商会议陕西省委员会", "政协", "省级", "全国政协", "陕西省西安市"),
    # 乾县外调人员曾任组织
    (15, "西安市人民政府", "政府", "副省级", "陕西省人民政府", "陕西省西安市"),
    (16, "宝鸡市人民政府", "政府", "地级市", "陕西省人民政府", "陕西省宝鸡市"),
    (17, "渭南市人民政府", "政府", "地级市", "陕西省人民政府", "陕西省渭南市"),
    (18, "中共渭南市委员会", "党委", "地级市", "中共陕西省委员会", "陕西省渭南市"),
    (19, "中共延安市委员会", "党委", "地级市", "中共陕西省委员会", "陕西省延安市"),
    (20, "中共咸阳市秦都区委员会", "党委", "县处级", "中共咸阳市委", "陕西省咸阳市秦都区"),
    (21, "旬邑县人民政府", "政府", "县处级", "咸阳市人民政府", "陕西省咸阳市旬邑县"),
    (22, "咸阳市财政局", "政府部门", "县处级", "咸阳市人民政府", "陕西省咸阳市"),
]

# ===== 任职数据 =====
positions = [
    # --- 乾县现任领导任职 ---
    (1, 1, 1, "县委书记", "未知", "至今", "正县级", "闫兴斌曾任乾县县长后升任县委书记"),
    (1, 1, 2, "县长", "未知", "至今", "正县级", "此前曾任乾县县长"),
    (2, 2, 2, "县长", "未知", "至今", "正县级", "段志华现任乾县县长"),
    (3, 3, 1, "县委副书记", "未知", "至今", "副县级", "专职副书记"),
    (4, 4, 3, "县委常委、组织部部长", "未知", "至今", "副县级", ""),
    (5, 5, 2, "县委常委、常务副县长", "未知", "至今", "副县级", "孙佳佳1986年生"),

    # --- 上官吉庆跨县任职轨迹（乾县人，在乾县曾任县委书记后调出） ---
    (6, 6, 1, "县委书记", "1999年10月", "2002年12月", "正县级", "乾县县委书记"),
    (6, 6, 11, "副市长", "2004年4月", "2004年11月", "副厅级", "咸阳市副市长"),
    (6, 6, 13, "副厅长", "2004年11月", "2008年8月", "副厅级", "陕西省财政厅副厅长"),
    (6, 6, 16, "副市长→市长→市委书记", "2008年8月", "2015年10月", "正厅级", "宝鸡市副市长/市长/市委书记"),
    (6, 6, 15, "西安市市长", "2016年2月", "2018年11月", "副省级", "西安市市长（已落马）"),

    # --- 徐新荣跨县任职轨迹（乾县人，从秦都区起步） ---
    (7, 7, 20, "区委书记", "2000年6月", "2004年3月", "副厅级", "咸阳市秦都区委书记"),
    (7, 7, 10, "市委副书记", "2004年3月", "2006年（约）", "副厅级", "咸阳市委副书记"),
    (7, 7, 17, "市长", "2008年2月", "2013年2月", "正厅级", "渭南市市长"),
    (7, 7, 18, "市委书记", "2013年2月", "2015年6月", "正厅级", "渭南市委书记"),
    (7, 7, 19, "市委书记", "2015年6月", "2021年1月", "正厅级", "延安市委书记"),
    (7, 7, 14, "主席", "2022年1月", "至今", "正省级", "陕西省政协主席"),

    # --- 焦志鹏（闫兴斌前任乾县县委书记） ---
    (8, 8, 1, "县委书记", "未知", "（已调任）", "正县级", "前任乾县县委书记，后调往咸阳市"),
    (8, 8, 21, "县长", "未知", "未知", "正县级", "此前曾任旬邑县县长"),

    # --- 邻近县区现任领导 ---
    (9, 9, 4, "县委书记", "未知", "至今", "正县级", "礼泉县委书记"),
    (10, 10, 5, "县长", "未知", "至今", "正县级", "礼泉县县长"),
    (11, 11, 6, "县委书记", "未知", "至今", "正县级", "永寿县委书记"),
    (12, 12, 7, "县长", "未知", "至今", "正县级", "永寿县县长"),
    (13, 13, 8, "县委书记", "未知", "至今", "正县级", "泾阳县委书记"),
    (14, 14, 9, "县长", "未知", "至今", "正县级", "泾阳县县长"),

    # --- 咸阳市领导 ---
    (15, 15, 10, "市委书记", "未知", "至今", "正厅级", "原咸阳市市长升任"),
    (15, 15, 11, "市长", "未知", "至今", "正厅级", "此前任咸阳市市长"),
    (16, 16, 11, "市长", "未知", "至今", "正厅级", "接冷劲松任市长"),

    # --- 陕西省领导 ---
    (18, 18, 12, "省委书记", "2022年11月", "至今", "正省级", "陕西省委书记"),
    (19, 19, 13, "省长", "2022年12月", "至今", "正省级", "陕西省省长"),
]

# ===== 关系数据 =====
# (id, person_a, person_b, type, context, overlap_org, overlap_period, confidence)
relationships = [
    # 乾县内部关系
    (1, 1, 2, "搭档", "闫兴斌（县委书记）与段志华（县长）——当前党政一把手", "中共乾县县委/乾县人民政府", "至今", "confirmed"),
    (1, 1, 3, "上下级", "县委书记与专职副书记刘春锋", "中共乾县县委", "至今", "confirmed"),

    # 跨县调任关系
    (2, 6, 18, "同乡", "上官吉庆与徐新荣均为乾县人，先后从乾县调往咸阳市和更高岗位", "（籍贯相同）", "同代官员", "confirmed"),
    (3, 8, 1, "接班", "焦志鹏（前任乾县县委书记）→闫兴斌（接任县委书记）", "中共乾县县委", "（交接期）", "plausible"),
    (4, 8, 21, "跨县", "焦志鹏此前曾任旬邑县县长，后调任乾县县委书记", "旬邑县→乾县", "（调任时）", "plausible"),

    # 乾县⟷咸阳市关系
    (5, 1, 15, "上下级", "闫兴斌（乾县县委书记）受冷劲松（咸阳市委书记）领导", "中共咸阳市委/乾县县委", "至今", "confirmed"),
    (6, 2, 16, "上下级", "段志华（乾县县长）受贾珉亮（咸阳市市长）领导", "咸阳市人民政府/乾县人民政府", "至今", "confirmed"),

    # 邻近县区关系
    (7, 1, 9, "同级别", "闫兴斌（乾县县委书记）与姚俊峰（礼泉县委书记）为邻县同僚", "（不同县区）", "同时期", "confirmed"),
    (8, 1, 11, "同级别", "闫兴斌（乾县县委书记）与杨孟珠（永寿县委书记）为邻县同僚", "（不同县区）", "同时期", "confirmed"),
    (9, 1, 13, "同级别", "闫兴斌（乾县县委书记）与郝瑞耀（泾阳县委书记）为邻县同僚", "（不同县区）", "同时期", "confirmed"),

    # 咸阳市⟷乾县以及咸阳内部提拔
    (10, 15, 16, "接班", "冷劲松（原市长）升任市委书记，贾珉亮接任市长", "咸阳市人民政府", "2026年", "confirmed"),
    (11, 17, 15, "接班", "夏晓中（前任市委书记）→冷劲松（接任市委书记）", "中共咸阳市委员会", "2026年（推测）", "plausible"),
]

# ===== 生成函数 =====
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(pid, post):
    if "书记" in post and ("县委" in post or "省委" in post or "市委" in post or "区委" in post):
        return "255,50,50"
    if "县长" in post or "区长" in post or "市长" in post and "副" not in post[:2]:
        return "50,100,255"
    if "省长" in post or "主席" in post and "政协" in post:
        return "200,50,200"
    if "副书记" in post or "副市长" in post or "副县长" in post:
        return "100,150,255"
    return "100,100,100"

def is_top_leader(post):
    return "书记" in post or "县长" in post and "副" not in post[:2] or "市长" in post and "副" not in post[:2]

def build_sqlite(db_path):
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT,
            confidence TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)
    c.executemany("INSERT OR REPLACE INTO persons(id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source,confidence) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", persons)
    c.executemany("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)", organizations)
    c.executemany("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)", positions)
    c.executemany("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?,?)", relationships)
    conn.commit()
    conn.close()
    print(f"  SQLite 数据库已生成: {db_path}")
    print(f"    - {len(persons)} 人物")
    print(f"    - {len(organizations)} 组织")
    print(f"    - {len(positions)} 任职记录")
    print(f"    - {len(relationships)} 关系记录")

def build_gexf(gexf_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{DATE}">')
    lines.append('    <creator>OpenCode Gov-Relation Agent</creator>')
    lines.append(f'    <description>乾县跨县干部交流网络 - {DATE}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="county" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        pid, name, gender, ethnicity, birth, birthplace, edu, party, work, post, org, source, conf = p
        c = person_color(pid, post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(birthplace or "乾县" if pid <= 8 else "")}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - organizations
    for o in organizations:
        oid, oname, otype, olevel, oparent, oloc = o
        color_map = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "党委部门": "255,210,210",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "政府部门": "220,220,255",
        }
        oc = color_map.get(otype, "200,200,200")
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="square"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    for pos in positions:
        pos_id, pid, oid, title, start, end, rank, note = pos
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for rel in relationships:
        rid, pa, pb, rtype, context, overlap_org, overlap_period, conf = rel
        eid += 1
        w = "2.0" if "搭档" in rtype or "接班" in rtype or "上下级" in rtype else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(context)}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF 图文件已生成: {gexf_path}")
    print(f"    - {len(persons)} 个人物节点 + {len(organizations)} 个组织节点")
    print(f"    - {len(positions)} 条任职边 + {len(relationships)} 条关系边")


if __name__ == "__main__":
    staging = Path(__file__).parent.resolve()
    db_path = staging / "乾县跨县交流_network.db"
    gexf_path = staging / "乾县跨县交流_network.gexf"

    print(f"========== 构建 {SLUG} 数据 ==========")
    print(f"日期: {DATE}")

    build_sqlite(db_path)
    build_gexf(gexf_path)

    print(f"\n========== 构建完成 ==========")
    print(f"数据库: {db_path} ({db_path.stat().st_size} bytes)")
    print(f"GEXF:   {gexf_path} ({gexf_path.stat().st_size} bytes)")
