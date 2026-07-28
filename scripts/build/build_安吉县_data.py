#!/usr/bin/env python3
"""Build script for 安吉县 (Anji County) government personnel network."""

import sqlite3
from datetime import date
from pathlib import Path

SLUG = "安吉县"
TODAY = date.today().isoformat()

BASE = Path(__file__).resolve().parents[2]
DB_PATH = BASE / "data" / "database" / f"{SLUG}_network.db"
GEXF_PATH = BASE / "data" / "graph" / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────

persons = [
    # ── Party Secretary (县委书记) ──
    {
        "id": 1, "name": "宁云", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-08", "birthplace": "待查", "education": "在职大学",
        "party_join": "待查", "work_start": "待查",
        "current_post": "县委书记",
        "current_org": "中共安吉县委员会",
        "source": "https://www.anji.gov.cn/col/col1229211800/index.html",
    },
    # ── County Mayor (县长兼县委副书记) ──
    {
        "id": 2, "name": "杨斌", "gender": "男", "ethnicity": "汉族",
        "birth": "1985-09", "birthplace": "待查", "education": "大学",
        "party_join": "中共党员", "work_start": "待查",
        "current_post": "县委副书记、县长",
        "current_org": "安吉县人民政府",
        "source": "https://www.anji.gov.cn/col/col1229614952/index.html",
    },
    # ── Deputy Secretary + Executive Deputy Mayor (县委副书记、常务副县长) ──
    {
        "id": 3, "name": "黄枫", "gender": "男", "ethnicity": "汉族",
        "birth": "1981-08", "birthplace": "待查", "education": "硕士研究生",
        "party_join": "中共党员", "work_start": "待查",
        "current_post": "县委副书记、常务副县长",
        "current_org": "中共安吉县委员会 / 安吉县人民政府",
        "source": "https://www.anji.gov.cn/col/col1229614953/index.html",
    },
    # ── Discipline Inspection Secretary (纪委书记) ──
    {
        "id": 4, "name": "王宗明", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-03", "birthplace": "待查", "education": "大学",
        "party_join": "中共党员", "work_start": "待查",
        "current_post": "县委常委、纪委书记、县监委主任",
        "current_org": "中共安吉县纪律检查委员会",
        "source": "https://www.anji.gov.cn/col/col1229614949/index.html",
    },
    # ── Organization Department Head (组织部长) ──
    {
        "id": 5, "name": "彭琳", "gender": "女", "ethnicity": "汉族",
        "birth": "1986-02", "birthplace": "待查", "education": "大学",
        "party_join": "中共党员", "work_start": "待查",
        "current_post": "县委常委、组织部部长、县委党校校长",
        "current_org": "中共安吉县委组织部",
        "source": "https://www.anji.gov.cn/col/col1229787270/index.html",
    },
    # ── Standing Committee / Deputy Mayor (县委常委、副县长) ──
    {
        "id": 6, "name": "徐伟", "gender": "男", "ethnicity": "汉族",
        "birth": "1972-12", "birthplace": "待查", "education": "中央党校大学",
        "party_join": "中共党员", "work_start": "待查",
        "current_post": "县委常委、副县长",
        "current_org": "安吉县人民政府",
        "source": "https://www.anji.gov.cn/col/col1229856400/index.html",
    },
    # ── Propaganda Secretary (宣传部长) ──
    {
        "id": 7, "name": "沈小波", "gender": "男", "ethnicity": "汉族",
        "birth": "1985-04", "birthplace": "待查", "education": "省委党校研究生",
        "party_join": "中共党员", "work_start": "待查",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共安吉县委宣传部",
        "source": "https://www.anji.gov.cn/col/col1229787269/index.html",
    },
    # ── Standing Committee / Dev Zone Secretary (县委常委、经开区党工委书记) ──
    {
        "id": 8, "name": "高安兵", "gender": "男", "ethnicity": "汉族",
        "birth": "1974-11", "birthplace": "待查", "education": "在职大学",
        "party_join": "中共党员", "work_start": "待查",
        "current_post": "县委常委、经开区党工委书记",
        "current_org": "浙江安吉经济开发区党工委",
        "source": "https://www.anji.gov.cn/col/col1229614951/index.html",
    },
    # ── Standing Committee / Aid work in progress (县委常委，援派金川县) ──
    {
        "id": 9, "name": "谢春伟", "gender": "男", "ethnicity": "汉族",
        "birth": "1981-01", "birthplace": "待查", "education": "大学",
        "party_join": "中共党员", "work_start": "待查",
        "current_post": "县委常委（援派金川县）",
        "current_org": "中共安吉县委员会（援派金川县）",
        "source": "https://www.anji.gov.cn/col/col1229856401/index.html",
    },
    # ── Standing Committee / Tianhuangping Town Party Secretary ──
    {
        "id": 10, "name": "吴博文", "gender": "男", "ethnicity": "汉族",
        "birth": "1991-10", "birthplace": "待查", "education": "硕士研究生",
        "party_join": "中共党员", "work_start": "待查",
        "current_post": "县委常委、天荒坪镇党委书记",
        "current_org": "安吉县天荒坪镇党委",
        "source": "https://www.anji.gov.cn/col/col1229211797/wbw/index.html",
    },
    # ── Standing Committee / Armed Forces (县委常委、人武部政委) ──
    {
        "id": 11, "name": "王卫国", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-02", "birthplace": "陕西合阳", "education": "大学",
        "party_join": "2001-03", "work_start": "1998-09",
        "current_post": "县委常委、人武部政委",
        "current_org": "安吉县人民武装部",
        "source": "https://www.anji.gov.cn/col/col1229614950/index.html",
    },
    # ── Deputy Mayor (副县长) ──
    {
        "id": 12, "name": "管永丰", "gender": "男", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "待查", "work_start": "待查",
        "current_post": "副县长",
        "current_org": "安吉县人民政府",
        "source": "https://www.anji.gov.cn/col/col1229211873/index.html",
    },
    {
        "id": 13, "name": "夏中金", "gender": "男", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "待查", "work_start": "待查",
        "current_post": "副县长",
        "current_org": "安吉县人民政府",
        "source": "https://www.anji.gov.cn/col/col1229787767/index.html",
    },
    {
        "id": 14, "name": "王爱国", "gender": "男", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "待查", "work_start": "待查",
        "current_post": "副县长、公安局局长",
        "current_org": "安吉县人民政府 / 安吉县公安局",
        "source": "https://www.anji.gov.cn/col/col1229787766/index.html",
    },
    {
        "id": 15, "name": "章毅", "gender": "男", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "待查", "work_start": "待查",
        "current_post": "副县长",
        "current_org": "安吉县人民政府",
        "source": "https://www.anji.gov.cn/col/col1229819087/index.html",
    },
    {
        "id": 16, "name": "沈斌", "gender": "男", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "待查", "work_start": "待查",
        "current_post": "副县长",
        "current_org": "安吉县人民政府",
        "source": "https://www.anji.gov.cn/col/col1229829432/index.html",
    },
    {
        "id": 17, "name": "徐晟", "gender": "男", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "待查", "work_start": "待查",
        "current_post": "副县长",
        "current_org": "安吉县人民政府",
        "source": "https://www.anji.gov.cn/col/col1229866052/index.html",
    },
    {
        "id": 18, "name": "艾杰", "gender": "男", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "待查", "work_start": "待查",
        "current_post": "副县长",
        "current_org": "安吉县人民政府",
        "source": "https://www.anji.gov.cn/col/col1229211798/index.html",
    },
    {
        "id": 19, "name": "肖家青", "gender": "男", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "待查", "work_start": "待查",
        "current_post": "县政府党组成员",
        "current_org": "安吉县人民政府",
        "source": "https://www.anji.gov.cn/col/col1229614954/index.html",
    },
    # ── NPC Chair (人大主任) ──
    {
        "id": 20, "name": "何晓红", "gender": "女", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "待查", "work_start": "待查",
        "current_post": "县人大常委会主任",
        "current_org": "安吉县人大常委会",
        "source": "https://www.anji.gov.cn/col/col1229211479/art/2026/art_cb67548f76614de3b87ae94db7cdafda.html",
    },
    # ── CPPCC Chair (政协主席) ──
    {
        "id": 21, "name": "何承明", "gender": "男", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "待查", "work_start": "待查",
        "current_post": "县政协主席",
        "current_org": "安吉县政协",
        "source": "https://www.anji.gov.cn/col/col1229211479/art/2026/art_ba6f3eb0610043c3bfe90eda8ce797f4.html",
    },
    # ── Court President (法院院长) ──
    {
        "id": 22, "name": "费思杰", "gender": "男", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "待查", "work_start": "待查",
        "current_post": "县法院院长",
        "current_org": "安吉县人民法院",
        "source": "https://www.anji.gov.cn/col/col1229211479/art/2026/art_9de2e9540fc34b2481c1f4e7f9a18185.html",
    },
    # ── Procuratorate (检察院检察长) ──
    {
        "id": 23, "name": "张帆", "gender": "男", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "待查", "work_start": "待查",
        "current_post": "县检察院检察长",
        "current_org": "安吉县人民检察院",
        "source": "https://www.anji.gov.cn/col/col1229211479/art/2026/art_6bb4c8b0fb3a4a1e944a7cbbac499f34.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共安吉县委员会", "type": "党委", "level": "县", "parent": "中共湖州市委", "location": "安吉县"},
    {"id": 2, "name": "安吉县人民政府", "type": "政府", "level": "县", "parent": "湖州市人民政府", "location": "安吉县"},
    {"id": 3, "name": "中共安吉县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共安吉县委员会", "location": "安吉县"},
    {"id": 4, "name": "中共安吉县委组织部", "type": "党委", "level": "县", "parent": "中共安吉县委员会", "location": "安吉县"},
    {"id": 5, "name": "中共安吉县委宣传部", "type": "党委", "level": "县", "parent": "中共安吉县委员会", "location": "安吉县"},
    {"id": 6, "name": "浙江安吉经济开发区党工委", "type": "党委", "level": "县", "parent": "中共安吉县委员会", "location": "安吉县"},
    {"id": 7, "name": "安吉县公安局", "type": "政府", "level": "县", "parent": "安吉县人民政府", "location": "安吉县"},
    {"id": 8, "name": "安吉县天荒坪镇党委", "type": "党委", "level": "乡镇", "parent": "中共安吉县委员会", "location": "安吉县天荒坪镇"},
    {"id": 9, "name": "安吉县人民武装部", "type": "政府", "level": "县", "parent": "湖州军分区", "location": "安吉县"},
    {"id": 10, "name": "安吉县人大常委会", "type": "人大", "level": "县", "parent": "安吉县", "location": "安吉县"},
    {"id": 11, "name": "安吉县政协", "type": "政协", "level": "县", "parent": "安吉县", "location": "安吉县"},
    {"id": 12, "name": "安吉县人民法院", "type": "政法机关", "level": "县", "parent": "安吉县", "location": "安吉县"},
    {"id": 13, "name": "安吉县人民检察院", "type": "政法机关", "level": "县", "parent": "安吉县", "location": "安吉县"},
]

# ── Positions ────────────────────────────────────────────────────────────

positions = [
    # Party committee leaders
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "待查", "end_date": "", "rank": "正县级", "note": "主持县委全面工作"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "兼任县长"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "专职副书记,兼任常务副县长"},
    {"person_id": 4, "org_id": 1, "title": "县委常委、纪委书记", "start_date": "待查", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "兼任县委党校校长"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "兼任副县长"},
    {"person_id": 7, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "兼任经开区党工委书记"},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "援派四川省金川县"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "兼任天荒坪镇党委书记"},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "兼任人武部政委"},
    # Government leaders
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "待查", "end_date": "", "rank": "正县级", "note": "领导县政府全面工作"},
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "负责县政府常务工作"},
    {"person_id": 6, "org_id": 2, "title": "县委常委、副县长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "负责住建、交通、城管、教育、卫健"},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "负责工业、金融、文旅、生态"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "负责招商引资、临港经济"},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "兼任公安局长"},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "负责两山科技城、长合区"},
    {"person_id": 16, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "负责民政、人社、医保、退役军人"},
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "负责民政、退役军人、外事"},
    {"person_id": 18, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "协助常务副县长"},
    {"person_id": 19, "org_id": 2, "title": "县政府党组成员", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "负责农业农村、林业、水利"},
    # Other organs
    {"person_id": 14, "org_id": 7, "title": "县公安局局长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "天荒坪镇党委书记", "start_date": "待查", "end_date": "", "rank": "正科级", "note": "县委常委兼任"},
    {"person_id": 11, "org_id": 9, "title": "县人武部政委", "start_date": "待查", "end_date": "", "rank": "正团级", "note": "县委常委兼任"},
    {"person_id": 4, "org_id": 3, "title": "县监委主任", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "纪委书记兼任"},
    {"person_id": 5, "org_id": 4, "title": "县委组织部部长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "兼任县委党校校长"},
    {"person_id": 7, "org_id": 5, "title": "县委宣传部部长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "经开区党工委书记", "start_date": "待查", "end_date": "", "rank": "副县级", "note": "县委常委兼任"},
    {"person_id": 20, "org_id": 10, "title": "县人大常委会主任", "start_date": "待查", "end_date": "", "rank": "正县级", "note": ""},
    {"person_id": 21, "org_id": 11, "title": "县政协主席", "start_date": "待查", "end_date": "", "rank": "正县级", "note": ""},
    {"person_id": 22, "org_id": 12, "title": "县法院院长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 23, "org_id": 13, "title": "县检察院检察长", "start_date": "待查", "end_date": "", "rank": "副县级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────

relationships = [
    # Leadership team working relationships (同班子)
    {"person_a": 1, "person_b": 2, "type": "领导关系", "context": "县委书记与县长搭档", "overlap_org": "中共安吉县委员会/安吉县人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 3, "type": "领导关系", "context": "县委书记与专职副书记/常务副县长搭档", "overlap_org": "中共安吉县委员会", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 3, "type": "领导关系", "context": "县长与常务副县长搭档", "overlap_org": "安吉县人民政府", "overlap_period": "当前"},
    {"person_a": 3, "person_b": 4, "type": "领导关系", "context": "副书记与纪委书记同班子", "overlap_org": "中共安吉县委员会常委会", "overlap_period": "当前"},
    {"person_a": 3, "person_b": 5, "type": "领导关系", "context": "副书记与组织部长同班子", "overlap_org": "中共安吉县委员会常委会", "overlap_period": "当前"},
    {"person_a": 3, "person_b": 6, "type": "领导关系", "context": "常务副县长与县委常委、副县长同政府班子", "overlap_org": "安吉县人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 20, "type": "领导关系", "context": "县委书记与人大主任分工协作", "overlap_org": "安吉县领导层", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 21, "type": "领导关系", "context": "县委书记与政协主席分工协作", "overlap_org": "安吉县领导层", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 7, "type": "领导关系", "context": "县委书记与宣传部长上下级", "overlap_org": "中共安吉县委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 8, "type": "领导关系", "context": "县委书记与经开区书记上下级", "overlap_org": "中共安吉县委员会", "overlap_period": "当前"},
    {"person_a": 5, "person_b": 10, "type": "干管关系", "context": "组织部长和县委常委（最年轻常委）", "overlap_org": "中共安吉县委员会常委会", "overlap_period": "当前"},
    {"person_a": 4, "person_b": 5, "type": "同班子", "context": "纪委书记与组织部长同班子", "overlap_org": "中共安吉县委员会常委会", "overlap_period": "当前"},
    # Police-chief relationship
    {"person_a": 14, "person_b": 3, "type": "领导关系", "context": "公安局长向常务副县长汇报", "overlap_org": "安吉县人民政府", "overlap_period": "当前"},
    {"person_a": 14, "person_b": 22, "type": "协作关系", "context": "公安与法院在政法委系统协作", "overlap_org": "安吉县政法系统", "overlap_period": "当前"},
    {"person_a": 14, "person_b": 23, "type": "协作关系", "context": "公安与检察院在政法委系统协作", "overlap_org": "安吉县政法系统", "overlap_period": "当前"},
    {"person_a": 22, "person_b": 23, "type": "协作关系", "context": "法检两长协作", "overlap_org": "安吉县政法系统", "overlap_period": "当前"},
    # Organization department relations
    {"person_a": 5, "person_b": 10, "type": "人事关系", "context": "组织部长管理最年轻常委的干部任用", "overlap_org": "中共安吉县委组织部/天荒坪镇", "overlap_period": "当前"},
]

# ══════════════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
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
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
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
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
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
    print(f"  信息来源: 安吉县人民政府网站 (anji.gov.cn)")
    print("=" * 60)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Persons
    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    # Organizations
    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    # Positions
    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c,"") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    # Relationships
    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c,"") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "县委书记" in post and "副书记" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post and "副书记" in post:
            return ("50,120,255", 20.0)
        elif "副书记" in post and "常务" in post:
            return ("150,80,80", 18.0)
        elif "副书记" in post:
            return ("150,100,100", 15.0)
        elif "常务" in post:
            return ("80,80,200", 15.0)
        elif "纪委书记" in post:
            return ("200,150,50", 14.0)
        elif "组织部长" in post:
            return ("50,180,120", 14.0)
        elif "副县长" in post or "常委" in post:
            return ("100,100,255", 12.0)
        elif "人大主任" in post:
            return ("200,255,200", 15.0)
        elif "政协主席" in post:
            return ("200,200,100", 15.0)
        elif "法院" in post or "检察" in post:
            return ("180,180,180", 12.0)
        else:
            return ("100,100,100", 10.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,200"),
            "政协": ("200,200,200"),
            "政法机关": ("220,220,180"),
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
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
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
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    run_build()
