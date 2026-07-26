#!/usr/bin/env python3
"""Build 娄烦县 leadership network (2026-07-26)."""

import os
import sys
import sqlite3
from pathlib import Path

DB_PATH = os.environ.get("DB_PATH", "")
GEXF_PATH = os.environ.get("GEXF_PATH", "")
STAGING = os.environ.get("STAGING_DIR", "")

if not DB_PATH:
    if STAGING:
        DB_PATH = str(Path(STAGING) / "娄烦县_network.db")
    else:
        DB_PATH = str(Path(__file__).resolve().parents[3] / "data" / "database" / "娄烦县_network.db")

if not GEXF_PATH:
    if STAGING:
        GEXF_PATH = str(Path(STAGING) / "娄烦县_network.gexf")
    else:
        GEXF_PATH = str(Path(__file__).resolve().parents[3] / "data" / "graph" / "娄烦县_network.gexf")

_repo_root = Path(__file__).resolve().parents[3]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from gov_relation.runner import run_build

SLUG = "娄烦县"

PERSONS = [
    # 1-3: 县委主要领导
    {"id":1,"name":"李文权","gender":"男","ethnicity":"汉族","birth":"1968.09","birthplace":"山西怀仁","education":"大学/工商管理硕士","party_join":"1992.06","work_start":"1990.07","current_post":"太原市人大常委会副主任、县委书记","current_org":"中共娄烦县委员会",
     "source":"https://www.sxlf.gov.cn/ywdt/20260716/30309547.html"},
    {"id":2,"name":"景博","gender":"男","ethnicity":"汉族","birth":"1989.11","birthplace":"山西永济","education":"太原理工大学硕士研究生","party_join":"2009.05","work_start":"2014.07","current_post":"县委副书记、县长","current_org":"娄烦县人民政府",
     "source":"https://www.sxlf.gov.cn/ldzc.html"},
    {"id":3,"name":"秦晓东","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委副书记、政法委书记、县委办主任","current_org":"中共娄烦县委员会",
     "source":"https://www.sxlf.gov.cn/ywdt/20260716/30309548.html"},
    # 4-11: 县委常委
    {"id":4,"name":"庞娟","gender":"女","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委常委、常务副县长","current_org":"娄烦县人民政府",
     "source":"https://www.sxlf.gov.cn/ldzc.html"},
    {"id":5,"name":"高林","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委常委、副县长","current_org":"娄烦县人民政府",
     "source":"https://www.sxlf.gov.cn/ldzc.html"},
    {"id":6,"name":"武鹏","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委常委","current_org":"中共娄烦县委员会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":7,"name":"杨剑","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委常委","current_org":"中共娄烦县委员会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":8,"name":"张文彬","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委常委、纪委书记、监委主任","current_org":"中共娄烦县纪律检查委员会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":9,"name":"李学斌","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委常委","current_org":"中共娄烦县委员会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":10,"name":"管宁","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委常委","current_org":"中共娄烦县委员会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":11,"name":"关晋钢","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委常委","current_org":"中共娄烦县委员会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    # 12-16: 县政府其他领导
    {"id":12,"name":"马建玉","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"娄烦县人民政府",
     "source":"https://www.sxlf.gov.cn/ldzc.html"},
    {"id":13,"name":"孙俊","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"娄烦县人民政府",
     "source":"https://www.sxlf.gov.cn/ldzc.html"},
    {"id":14,"name":"武进文","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"娄烦县人民政府",
     "source":"https://www.sxlf.gov.cn/ldzc.html"},
    {"id":15,"name":"白洁皓","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县政府党组成员（挂职）","current_org":"娄烦县人民政府",
     "source":"https://www.sxlf.gov.cn/ldzc.html"},
    # 16-20: 人大
    {"id":16,"name":"朱永军","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县人大常委会主任","current_org":"娄烦县人大常委会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":17,"name":"马存海","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县人大常委会副主任","current_org":"娄烦县人大常委会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":18,"name":"侯尚德","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县人大常委会副主任","current_org":"娄烦县人大常委会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":19,"name":"雷爱婵","gender":"女","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县人大常委会副主任","current_org":"娄烦县人大常委会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":20,"name":"王丽军","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县人大常委会副主任","current_org":"娄烦县人大常委会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    # 21-26: 政协
    {"id":21,"name":"曹晓冬","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县政协主席","current_org":"政协娄烦县委员会",
     "source":"https://www.sxlf.gov.cn/ywdt/20260716/30309548.html"},
    {"id":22,"name":"强建生","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县政协副主席","current_org":"政协娄烦县委员会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":23,"name":"张晓芳","gender":"女","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县政协副主席","current_org":"政协娄烦县委员会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":24,"name":"苏效忠","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县政协副主席","current_org":"政协娄烦县委员会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":25,"name":"李晨","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县政协副主席","current_org":"政协娄烦县委员会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":26,"name":"刘志君","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县政协副主席","current_org":"政协娄烦县委员会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    # 27-29: 法检两院、人武部
    {"id":27,"name":"田志凯","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县人民法院院长","current_org":"娄烦县人民法院",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":28,"name":"马峰","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县人民检察院检察长","current_org":"娄烦县人民检察院",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    {"id":29,"name":"肖桂峰","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县人武部部长","current_org":"娄烦县人民武装部",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
    # 30-33: 前任领导
    {"id":30,"name":"李树忠","gender":"男","ethnicity":"汉族","birth":"1968.06","birthplace":"山西太原晋源区","education":"中共中央党校","party_join":"1994.08","work_start":"","current_post":"（原县委书记，2024.03被查）","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E6%A0%91%E5%BF%A0"},
    {"id":31,"name":"薛东晓","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"（原县委书记，2023.06被查）","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E6%A0%91%E5%BF%A0"},
    {"id":32,"name":"张磊","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"（原县长，李树忠前任）","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E6%A0%91%E5%BF%A0"},
    {"id":33,"name":"马兰红","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县人大常委会副主任","current_org":"娄烦县人大常委会",
     "source":"https://www.sxlf.gov.cn/ywdt/20251231/30275157.html"},
]

O = [
    {"id":1,"name":"中共娄烦县委员会","type":"党委","level":"县处级","parent":"中共太原市委","location":"娄烦县"},
    {"id":2,"name":"娄烦县人民政府","type":"政府","level":"县处级","parent":"太原市人民政府","location":"娄烦县"},
    {"id":3,"name":"中共娄烦县纪律检查委员会","type":"纪委","level":"县处级","parent":"中共太原市纪委","location":"娄烦县"},
    {"id":4,"name":"娄烦县人大常委会","type":"人大","level":"县处级","parent":"太原市人大常委会","location":"娄烦县"},
    {"id":5,"name":"政协娄烦县委员会","type":"政协","level":"县处级","parent":"政协太原市委员会","location":"娄烦县"},
    {"id":6,"name":"娄烦县人民法院","type":"司法机关","level":"","parent":"太原市中级人民法院","location":"娄烦县"},
    {"id":7,"name":"娄烦县人民检察院","type":"司法机关","level":"","parent":"太原市人民检察院","location":"娄烦县"},
    {"id":8,"name":"娄烦县人民武装部","type":"军事","level":"","parent":"太原警备区","location":"娄烦县"},
    {"id":9,"name":"太原市人大常委会","type":"人大","level":"地厅级","parent":"山西省人大常委会","location":"太原市"},
]

POSITIONS = [
    # 李文权
    {"person_id":1,"org_id":1,"title":"县委书记","start_date":"2024.04","end_date":"","rank":"副厅级","note":"兼任，同时任太原市人大常委会副主任"},
    {"person_id":1,"org_id":9,"title":"市人大常委会副主任","start_date":"2022","end_date":"","rank":"副厅级","note":"2022年当选市人大常委会副主任"},
    # 景博
    {"person_id":2,"org_id":2,"title":"县长","start_date":"2021.02","end_date":"","rank":"正处级","note":"接替李树忠"},
    {"person_id":2,"org_id":1,"title":"县委副书记","start_date":"","end_date":"","rank":"副处级","note":""},
    # 秦晓东
    {"person_id":3,"org_id":1,"title":"县委副书记、政法委书记、县委办主任","start_date":"","end_date":"","rank":"副处级","note":""},
    # 县政府领导
    {"person_id":4,"org_id":2,"title":"常务副县长","start_date":"","end_date":"","rank":"副处级","note":"兼县委常委；分管发改、能源、工业、财税、金融、统计、审计等"},
    {"person_id":5,"org_id":2,"title":"副县长","start_date":"","end_date":"","rank":"副处级","note":"兼县委常委；分管安全生产、应急、消防、住建、交通等"},
    {"person_id":12,"org_id":2,"title":"副县长","start_date":"","end_date":"","rank":"副处级","note":"分管农业农村、水务、乡村振兴等"},
    {"person_id":13,"org_id":2,"title":"副县长","start_date":"","end_date":"","rank":"副处级","note":"分管综合执法、市场监管、规划自然资源、融媒体等"},
    {"person_id":14,"org_id":2,"title":"副县长","start_date":"2026.02","end_date":"","rank":"副处级","note":"分管公安、司法、信访；2026年2月到任"},
    {"person_id":15,"org_id":2,"title":"县政府党组成员（挂职）","start_date":"2026.01","end_date":"","rank":"","note":"分管文旅、文物"},
    # 人大
    {"person_id":16,"org_id":4,"title":"县人大常委会主任","start_date":"","end_date":"","rank":"正处级","note":""},
    {"person_id":17,"org_id":4,"title":"县人大常委会副主任","start_date":"","end_date":"","rank":"副处级","note":""},
    {"person_id":18,"org_id":4,"title":"县人大常委会副主任","start_date":"","end_date":"","rank":"副处级","note":""},
    {"person_id":19,"org_id":4,"title":"县人大常委会副主任","start_date":"","end_date":"","rank":"副处级","note":""},
    {"person_id":20,"org_id":4,"title":"县人大常委会副主任","start_date":"","end_date":"","rank":"副处级","note":""},
    {"person_id":33,"org_id":4,"title":"县人大常委会副主任","start_date":"","end_date":"","rank":"副处级","note":""},
    # 政协
    {"person_id":21,"org_id":5,"title":"县政协主席","start_date":"","end_date":"","rank":"正处级","note":""},
    {"person_id":22,"org_id":5,"title":"县政协副主席","start_date":"","end_date":"","rank":"副处级","note":""},
    {"person_id":23,"org_id":5,"title":"县政协副主席","start_date":"","end_date":"","rank":"副处级","note":""},
    {"person_id":24,"org_id":5,"title":"县政协副主席","start_date":"","end_date":"","rank":"副处级","note":""},
    {"person_id":25,"org_id":5,"title":"县政协副主席","start_date":"","end_date":"","rank":"副处级","note":""},
    {"person_id":26,"org_id":5,"title":"县政协副主席","start_date":"","end_date":"","rank":"副处级","note":""},
    # 法检、人武部
    {"person_id":27,"org_id":6,"title":"院长","start_date":"","end_date":"","rank":"","note":""},
    {"person_id":28,"org_id":7,"title":"检察长","start_date":"","end_date":"","rank":"","note":""},
    {"person_id":29,"org_id":8,"title":"部长","start_date":"","end_date":"","rank":"","note":""},
    # 前任县委书记
    {"person_id":30,"org_id":1,"title":"县委书记","start_date":"2021.02","end_date":"2024.03","rank":"正处级","note":"被查落马"},
    {"person_id":30,"org_id":2,"title":"县长","start_date":"2016.08","end_date":"2021.02","rank":"正处级","note":"2015.11为代县长"},
    {"person_id":31,"org_id":1,"title":"县委书记","start_date":"约2011","end_date":"约2021.02","rank":"正处级","note":"被查落马；长期在娄烦任职"},
    {"person_id":32,"org_id":2,"title":"县长","start_date":"","end_date":"2015.11","rank":"正处级","note":"李树忠前任"},
]

RELS = [
    # 县委书记-县长传承链
    {"person_a":31,"person_b":30,"type":"前后任","context":"薛东晓→李树忠：娄烦县委书记前后任（约2021年交接）","overlap_org":"中共娄烦县委","overlap_period":"约2011-2024","confidence":"confirmed","strength":"strong"},
    {"person_a":30,"person_b":1,"type":"前后任","context":"李树忠→李文权：娄烦县委书记前后任（李树忠被查，2024年4月李文权紧急接任）","overlap_org":"中共娄烦县委","overlap_period":"2021-2024","confidence":"confirmed","strength":"strong"},
    # 县长传承链
    {"person_a":32,"person_b":30,"type":"前后任","context":"张磊→李树忠：娄烦县长前后任（2015年11月交接）","overlap_org":"娄烦县人民政府","overlap_period":"","confidence":"confirmed","strength":"strong"},
    {"person_a":30,"person_b":2,"type":"前后任","context":"李树忠→景博：娄烦县长前后任（2021年李树忠升任书记、景博接任县长）","overlap_org":"娄烦县人民政府","overlap_period":"2016-2021","confidence":"confirmed","strength":"strong"},
    # 搭班关系
    {"person_a":31,"person_b":30,"type":"上下级","context":"薛东晓任书记、李树忠任县长期间搭班（2016-2021）","overlap_org":"娄烦县","overlap_period":"2016-2021","confidence":"confirmed","strength":"strong"},
    # 县级同班关系
    {"person_a":1,"person_b":2,"type":"上下级","context":"李文权任书记、景博任县长搭班（2024.04至今）","overlap_org":"娄烦县","overlap_period":"2024-至今","confidence":"confirmed","strength":"strong"},
    {"person_a":1,"person_b":3,"type":"上下级","context":"李文权任书记、秦晓东任副书记/政法委书记","overlap_org":"中共娄烦县委","overlap_period":"","confidence":"confirmed","strength":"strong"},
    {"person_a":2,"person_b":3,"type":"搭班","context":"景博任县长、秦晓东任副书记","overlap_org":"娄烦县","overlap_period":"","confidence":"confirmed","strength":"strong"},
    {"person_a":2,"person_b":4,"type":"上下级","context":"景博任县长、庞娟任常务副县长","overlap_org":"娄烦县人民政府","overlap_period":"","confidence":"confirmed","strength":"strong"},
]

# ── Run Build ──────────────────────────────────────────────────────────
STAGING = os.environ.get("STAGING_DIR")
if STAGING:
    db_path = os.path.join(STAGING, f"{SLUG}_network.db")
    gexf_path = os.path.join(STAGING, f"{SLUG}_network.gexf")
else:
    db_path = str(DATABASE_DIR / f"{SLUG}_network.db")
    gexf_path = str(GRAPH_DIR / f"{SLUG}_network.gexf")

run_build(
    slug=SLUG,
    persons=PERSONS,
    organizations=O,
    positions=POSITIONS,
    relationships=RELS,
    db_path=db_path,
    gexf_path=gexf_path,
)
