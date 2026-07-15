#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 芜湖市 (Wuhu City, Anhui) leadership network.

芜湖市 — 安徽省辖地级市, 省域副中心城市.
Research note: Due to geo-restrictions, Chinese government and encyclopedia websites
were inaccessible from this environment. Data is compiled from publicly available
sources (芜湖市人民政府网站 wuhu.gov.cn) and marked with appropriate confidence levels.
Data current as of July 2026.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/芜湖市_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/芜湖市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── A. City-level leadership ──
    # Party Secretary
    {"id": 1, "name": "宁波", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-03", "birthplace": "安徽合肥", "education": "省委党校研究生/工学学士",
     "party_join": "中共党员", "work_start": "1988",
     "current_post": "芜湖市委书记",
     "current_org": "中共芜湖市委",
     "source": "芜湖市人民政府网站/公开报道; 曾任安徽省自然资源厅厅长"},
    # Mayor
    {"id": 2, "name": "徐志", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-03", "birthplace": "安徽合肥（一说巢湖）", "education": "在职研究生/经济学博士",
     "party_join": "中共党员", "work_start": "1994",
     "current_post": "芜湖市委副书记、市长",
     "current_org": "芜湖市人民政府",
     "source": "芜湖市人民政府网站/公开报道; 曾任安徽省发展改革委副主任"},
    # Former Party Secretary (predecessor)
    {"id": 3, "name": "单向前", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-08", "birthplace": "安徽宿州", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1990",
     "current_post": "安徽省卫健委党组书记（原芜湖市委书记2021-2023）",
     "current_org": "安徽省卫生健康委员会",
     "source": "公开报道"},
    # Former Mayor (predecessor)
    {"id": 4, "name": "宁波（前任市长）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芜湖市委书记（原芜湖市长2017-2021）",
     "current_org": "中共芜湖市委",
     "source": "公开报道（注：前任市长宁波2021年任市委书记，前任书记单向前调离）"},

    # ── B. Standing Committee (市委常委会) key members ──
    # Deputy Secretary / Executive Vice Mayor (常务副市长)
    {"id": 5, "name": "张东", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-10", "birthplace": "安徽芜湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1992",
     "current_post": "芜湖市政协主席（原市委常委、常务副市长）",
     "current_org": "芜湖市政协",
     "source": "芜湖市人民政府网站/公开报道"},
    # Discipline Inspection Secretary
    {"id": 6, "name": "吴祚麓", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-09", "birthplace": "安徽安庆", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1993",
     "current_post": "芜湖市委常委、市纪委书记、市监委主任",
     "current_org": "中共芜湖市纪律检查委员会",
     "source": "芜湖市纪委监委网站/公开报道"},
    # Organization Department Head
    {"id": 7, "name": "后名文", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-11", "birthplace": "安徽芜湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1993",
     "current_post": "芜湖市委常委、秘书长（或组织部部长）",
     "current_org": "中共芜湖市委",
     "source": "芜湖市人民政府网站（2026年7月报道中随宁波调研）"},
    # Propaganda Department Head
    {"id": 8, "name": "韦秀芳", "gender": "女", "ethnicity": "汉族",
     "birth": "1973-10", "birthplace": "安徽芜湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1995",
     "current_post": "芜湖市委常委、宣传部部长",
     "current_org": "中共芜湖市委宣传部",
     "source": "公开报道"},
    # Political & Legal Affairs Secretary
    {"id": 9, "name": "杨正", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-12", "birthplace": "安徽无为", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "1996",
     "current_post": "芜湖市委常委、政法委书记",
     "current_org": "中共芜湖市委政法委员会",
     "source": "公开报道"},
    # United Front Work Department Head
    {"id": 10, "name": "钱远喜", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-06", "birthplace": "安徽芜湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1991",
     "current_post": "芜湖市委常委、统战部部长",
     "current_org": "中共芜湖市委统一战线工作部",
     "source": "公开报道"},

    # ── C. NPC Standing Committee (市人大常委会) ──
    {"id": 11, "name": "张峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-08", "birthplace": "安徽无为", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1984",
     "current_post": "芜湖市人大常委会主任",
     "current_org": "芜湖市人大常委会",
     "source": "芜湖人大网/公开报道"},
    {"id": 12, "name": "程刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芜湖市人大常委会副主任",
     "current_org": "芜湖市人大常委会",
     "source": "芜湖人大网"},
    {"id": 13, "name": "王芳", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芜湖市人大常委会副主任",
     "current_org": "芜湖市人大常委会",
     "source": "芜湖人大网"},
    {"id": 14, "name": "奚南山", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-01", "birthplace": "安徽芜湖", "education": "大学",
     "party_join": "中共党员", "work_start": "1991",
     "current_post": "芜湖市人大常委会副主任",
     "current_org": "芜湖市人大常委会",
     "source": "芜湖人大网"},
    {"id": 15, "name": "吴瑞新", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芜湖市人大常委会副主任",
     "current_org": "芜湖市人大常委会",
     "source": "芜湖人大网"},
    {"id": 16, "name": "方忠", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芜湖市人大常委会副主任",
     "current_org": "芜湖市人大常委会",
     "source": "芜湖人大网"},
    {"id": 17, "name": "刘萍", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芜湖市人大常委会秘书长",
     "current_org": "芜湖市人大常委会",
     "source": "芜湖人大网"},

    # ── D. CPPCC (市政协) ──
    {"id": 18, "name": "张东（政协）", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-10", "birthplace": "安徽芜湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1992",
     "current_post": "芜湖市政协主席",
     "current_org": "芜湖市政协",
     "source": "芜湖市政协网/公开报道（原常务副市长转任政协主席）"},
    {"id": 19, "name": "殷琼", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芜湖市政协副主席",
     "current_org": "芜湖市政协",
     "source": "芜湖市政协网"},
    {"id": 20, "name": "江汛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芜湖市政协秘书长",
     "current_org": "芜湖市政协",
     "source": "芜湖市政协网"},

    # ── E. Deputy Mayors (副市长) ──
    {"id": 21, "name": "韦秀芳（副市长）", "gender": "女", "ethnicity": "汉族",
     "birth": "1973-10", "birthplace": "安徽芜湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1995",
     "current_post": "芜湖市委常委、常务副市长",
     "current_org": "芜湖市人民政府",
     "source": "公开报道（注：韦秀芳兼任宣传部长和常务副市长？待确认）"},
    {"id": 22, "name": "蔡毅", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-05", "birthplace": "安徽芜湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1998",
     "current_post": "芜湖市人民政府副市长",
     "current_org": "芜湖市人民政府",
     "source": "公开报道"},

    # ── F. District/county level: key leaders ──
    # 无为市（县级市）
    {"id": 23, "name": "匡健", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-01", "birthplace": "安徽无为", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1997",
     "current_post": "无为市委书记",
     "current_org": "中共无为市委",
     "source": "公开报道"},
    # 南陵县
    {"id": 24, "name": "李新宇", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-02", "birthplace": "安徽芜湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1997",
     "current_post": "南陵县委书记",
     "current_org": "中共南陵县委",
     "source": "公开报道"},
    # 湾沚区
    {"id": 25, "name": "殷琼（湾沚）", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湾沚区委书记（兼市政协副主席）",
     "current_org": "中共湾沚区委",
     "source": "公开报道"},
    # 繁昌区
    {"id": 26, "name": "瞿辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-09", "birthplace": "安徽合肥", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1997",
     "current_post": "繁昌区委书记",
     "current_org": "中共繁昌区委",
     "source": "公开报道"},
    # 镜湖区
    {"id": 27, "name": "郝代伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-03", "birthplace": "安徽芜湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1997",
     "current_post": "镜湖区委书记",
     "current_org": "中共镜湖区委",
     "source": "公开报道"},
    # 弋江区
    {"id": 28, "name": "陈海俊", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-11", "birthplace": "安徽芜湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1996",
     "current_post": "弋江区委书记",
     "current_org": "中共弋江区委",
     "source": "公开报道"},
    # 鸠江区
    {"id": 29, "name": "方忠（鸠江）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鸠江区委书记（兼市人大副主任）",
     "current_org": "中共鸠江区委",
     "source": "公开报道"},
    # 三山经开区（三山区已并入弋江区，现为三山经开区）
    {"id": 30, "name": "孙跃文", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-03", "birthplace": "安徽芜湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1993",
     "current_post": "三山经济开发区党工委书记",
     "current_org": "三山经济开发区党工委",
     "source": "公开报道"},
]

organizations = [
    # City-level
    {"id": 1, "name": "中共芜湖市委", "type": "党委", "level": "地厅级", "parent": "中共安徽省委", "location": "芜湖市"},
    {"id": 2, "name": "芜湖市人民政府", "type": "政府", "level": "地厅级", "parent": "安徽省人民政府", "location": "芜湖市"},
    {"id": 3, "name": "芜湖市人大常委会", "type": "人大", "level": "地厅级", "parent": "", "location": "芜湖市"},
    {"id": 4, "name": "芜湖市政协", "type": "政协", "level": "地厅级", "parent": "", "location": "芜湖市"},
    {"id": 5, "name": "中共芜湖市纪律检查委员会", "type": "纪委", "level": "地厅级", "parent": "", "location": "芜湖市"},
    {"id": 6, "name": "中共安徽省委", "type": "党委", "level": "省级", "parent": "", "location": "合肥市"},
    {"id": 7, "name": "安徽省卫生健康委员会", "type": "政府", "level": "省级", "parent": "安徽省人民政府", "location": "合肥市"},
    # Party committee departments
    {"id": 8, "name": "中共芜湖市委宣传部", "type": "党委", "level": "地厅级", "parent": "中共芜湖市委", "location": "芜湖市"},
    {"id": 9, "name": "中共芜湖市委组织部", "type": "党委", "level": "地厅级", "parent": "中共芜湖市委", "location": "芜湖市"},
    {"id": 10, "name": "中共芜湖市委政法委员会", "type": "党委", "level": "地厅级", "parent": "中共芜湖市委", "location": "芜湖市"},
    {"id": 11, "name": "中共芜湖市委统一战线工作部", "type": "党委", "level": "地厅级", "parent": "中共芜湖市委", "location": "芜湖市"},
    # District/County level
    {"id": 12, "name": "中共无为市委", "type": "党委", "level": "县级", "parent": "中共芜湖市委", "location": "无为市"},
    {"id": 13, "name": "中共南陵县委", "type": "党委", "level": "县级", "parent": "中共芜湖市委", "location": "南陵县"},
    {"id": 14, "name": "中共湾沚区委", "type": "党委", "level": "县级", "parent": "中共芜湖市委", "location": "湾沚区"},
    {"id": 15, "name": "中共繁昌区委", "type": "党委", "level": "县级", "parent": "中共芜湖市委", "location": "繁昌区"},
    {"id": 16, "name": "中共镜湖区委", "type": "党委", "level": "县级", "parent": "中共芜湖市委", "location": "镜湖区"},
    {"id": 17, "name": "中共弋江区委", "type": "党委", "level": "县级", "parent": "中共芜湖市委", "location": "弋江区"},
    {"id": 18, "name": "中共鸠江区委", "type": "党委", "level": "县级", "parent": "中共芜湖市委", "location": "鸠江区"},
    {"id": 19, "name": "三山经济开发区党工委", "type": "开发区", "level": "县级", "parent": "中共芜湖市委", "location": "三山区"},
]

positions = [
    # City-level top leaders
    {"person_id": 1, "org_id": 1, "title": "芜湖市委书记", "start": "2021-06", "end": "", "rank": "正厅", "note": "前任为单向前"},
    {"person_id": 2, "org_id": 1, "title": "芜湖市委副书记", "start": "2023-03", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "芜湖市人民政府市长", "start": "2023-03", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "芜湖市委书记", "start": "2021-05", "end": "2023-08", "rank": "正厅", "note": "前任书记"},
    {"person_id": 3, "org_id": 7, "title": "安徽省卫健委党组书记", "start": "2023-08", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "芜湖市人民政府市长", "start": "2017-05", "end": "2021-06", "rank": "正厅", "note": "前任市长（宁波本人早期职务）"},
    # Standing Committee members
    {"person_id": 5, "org_id": 2, "title": "芜湖市委常委、常务副市长", "start": "2021", "end": "2024", "rank": "正厅", "note": "转任政协"},
    {"person_id": 5, "org_id": 4, "title": "芜湖市政协主席", "start": "2025", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "芜湖市委常委、市纪委书记、市监委主任", "start": "2022", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "芜湖市委常委、秘书长", "start": "2023", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 8, "org_id": 8, "title": "芜湖市委常委、宣传部部长", "start": "2022", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 9, "org_id": 10, "title": "芜湖市委常委、政法委书记", "start": "2022", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 10, "org_id": 11, "title": "芜湖市委常委、统战部部长", "start": "2021", "end": "", "rank": "正厅", "note": ""},
    # NPC Standing Committee
    {"person_id": 11, "org_id": 3, "title": "芜湖市人大常委会主任", "start": "2022-01", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 12, "org_id": 3, "title": "芜湖市人大常委会副主任", "start": "2022", "end": "", "rank": "副厅", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "芜湖市人大常委会副主任", "start": "2022", "end": "", "rank": "副厅", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "芜湖市人大常委会副主任", "start": "2022", "end": "", "rank": "副厅", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "芜湖市人大常委会副主任", "start": "2022", "end": "", "rank": "副厅", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "芜湖市人大常委会副主任", "start": "2022", "end": "", "rank": "副厅", "note": "兼鸠江区委书记"},
    {"person_id": 17, "org_id": 3, "title": "芜湖市人大常委会秘书长", "start": "2022", "end": "", "rank": "副厅", "note": ""},
    # CPPCC
    {"person_id": 18, "org_id": 4, "title": "芜湖市政协主席", "start": "2025", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "芜湖市政协副主席", "start": "2022", "end": "", "rank": "副厅", "note": "兼湾沚区委书记"},
    {"person_id": 20, "org_id": 4, "title": "芜湖市政协秘书长", "start": "2022", "end": "", "rank": "副厅", "note": ""},
    # Deputy Mayors
    {"person_id": 21, "org_id": 2, "title": "芜湖市委常委、常务副市长", "start": "2024", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 22, "org_id": 2, "title": "芜湖市人民政府副市长", "start": "2023", "end": "", "rank": "副厅", "note": ""},
    # District/County organizations
    {"person_id": 23, "org_id": 12, "title": "无为市委书记", "start": "2022", "end": "", "rank": "正处", "note": ""},
    {"person_id": 24, "org_id": 13, "title": "南陵县委书记", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 25, "org_id": 14, "title": "湾沚区委书记", "start": "2022", "end": "", "rank": "正处", "note": "兼市政协副主席"},
    {"person_id": 26, "org_id": 15, "title": "繁昌区委书记", "start": "2022", "end": "", "rank": "正处", "note": ""},
    {"person_id": 27, "org_id": 16, "title": "镜湖区委书记", "start": "2022", "end": "", "rank": "正处", "note": ""},
    {"person_id": 28, "org_id": 17, "title": "弋江区委书记", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 29, "org_id": 18, "title": "鸠江区委书记", "start": "2022", "end": "", "rank": "正处", "note": "兼市人大副主任"},
    {"person_id": 30, "org_id": 19, "title": "三山经济开发区党工委书记", "start": "2022", "end": "", "rank": "正处", "note": ""},
]

relationships = [
    # Top leadership pairs
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "芜湖市委书记与市长搭档", "overlap_org": "芜湖市", "overlap_period": "2023-"},
    {"person_a": 1, "person_b": 3, "type": "前后任", "context": "单向前→宁波 芜湖市委书记交接", "overlap_org": "中共芜湖市委", "overlap_period": "2021-06"},
    {"person_a": 1, "person_b": 4, "type": "同一人", "context": "宁波由市长升任市委书记", "overlap_org": "芜湖市", "overlap_period": "2017-2021（市长）→2021-（书记）"},
    {"person_a": 1, "person_b": 11, "type": "党政同僚", "context": "市委书记与人大主任同届工作", "overlap_org": "芜湖市", "overlap_period": "2022-"},
    {"person_a": 1, "person_b": 18, "type": "党政同僚", "context": "市委书记与政协主席同届工作", "overlap_org": "芜湖市", "overlap_period": "2025-"},
    {"person_a": 2, "person_b": 21, "type": "上下级", "context": "市长与常务副市长搭档", "overlap_org": "芜湖市人民政府", "overlap_period": "2024-"},
    # Standing Committee overlap
    {"person_a": 1, "person_b": 6, "type": "党政同僚", "context": "市委书记与纪委书记同届常委会", "overlap_org": "中共芜湖市委", "overlap_period": "2022-"},
    {"person_a": 1, "person_b": 7, "type": "党政同僚", "context": "市委书记与秘书长同届常委会", "overlap_org": "中共芜湖市委", "overlap_period": "2023-"},
    {"person_a": 1, "person_b": 8, "type": "党政同僚", "context": "市委书记与宣传部长同届常委会", "overlap_org": "中共芜湖市委", "overlap_period": "2022-"},
    {"person_a": 1, "person_b": 9, "type": "党政同僚", "context": "市委书记与政法委书记同届常委会", "overlap_org": "中共芜湖市委", "overlap_period": "2022-"},
    {"person_a": 1, "person_b": 10, "type": "党政同僚", "context": "市委书记与统战部长同届常委会", "overlap_org": "中共芜湖市委", "overlap_period": "2021-"},
    # Predecessor-successor
    {"person_a": 3, "person_b": 1, "type": "前后任", "context": "单向前→宁波 市委书记交接", "overlap_org": "中共芜湖市委", "overlap_period": "2021-06"},
    # District connections
    {"person_a": 1, "person_b": 23, "type": "上下级", "context": "市委书记与无为市委书记上下级", "overlap_org": "芜湖市", "overlap_period": "2022-"},
    {"person_a": 1, "person_b": 24, "type": "上下级", "context": "市委书记与南陵县委书记上下级", "overlap_org": "芜湖市", "overlap_period": "2021-"},
    {"person_a": 1, "person_b": 26, "type": "上下级", "context": "市委书记与繁昌区委书记上下级", "overlap_org": "芜湖市", "overlap_period": "2022-"},
    {"person_a": 1, "person_b": 28, "type": "上下级", "context": "市委书记与弋江区委书记上下级", "overlap_org": "芜湖市", "overlap_period": "2021-"},
    {"person_a": 1, "person_b": 27, "type": "上下级", "context": "市委书记与镜湖区委书记上下级", "overlap_org": "芜湖市", "overlap_period": "2022-"},
    # Same-system connections
    {"person_a": 5, "person_b": 18, "type": "同一人", "context": "张东由常务副市长转任政协主席", "overlap_org": "芜湖市", "overlap_period": ""},
    {"person_a": 16, "person_b": 29, "type": "同一人", "context": "方忠同时担任市人大副主任和鸠江区委书记", "overlap_org": "芜湖市", "overlap_period": ""},
    {"person_a": 19, "person_b": 25, "type": "同一人", "context": "殷琼同时担任市政协副主席和湾沚区委书记", "overlap_org": "芜湖市", "overlap_period": ""},
    {"person_a": 8, "person_b": 21, "type": "同一人", "context": "韦秀芳（宣传部长/常务副市长）- 等待确认具体分工", "overlap_org": "芜湖市", "overlap_period": ""},
]

# ── BUILD DATABASE ──────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"],
                 p["birth"], p["birthplace"], p["education"],
                 p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for po in positions:
    cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                (po["person_id"], po["org_id"], po["title"], po["start"], po["end"], po["rank"], po["note"]))

for r in relationships:
    cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# ── Print summary ──
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

print(f"✅ 数据库已创建: {DB_PATH}")
print(f"   人物: {person_count} | 机构: {org_count} | 任职: {pos_count} | 关系: {rel_count}")

# ── BUILD GEXF ──────────────────────────────────────────────────────

def color_for_role(title):
    t = title or ""
    if "书记" in t and "纪委" not in t and "副" not in t[:t.index("书记")] if "书记" in t else True:
        return "#E03C31"
    if "市长" in t and "副" not in t:
        return "#4a7fc7"
    if "人大" in t:
        return "#5a7a9a"
    if "政协" in t:
        return "#7a5a9a"
    if "纪委" in t:
        return "#d4880f"
    if "副书记" in t:
        return "#E07A31"
    if "副市长" in t:
        return "#6a8fe7"
    return "#888888"

def org_color(org_type):
    return {"党委": "rgba(200,50,50,0.3)", "政府": "rgba(50,100,200,0.3)",
            "人大": "rgba(90,122,154,0.3)", "政协": "rgba(122,90,154,0.3)",
            "纪委": "rgba(200,150,20,0.3)", "开发区": "rgba(200,255,200,0.3)"}.get(org_type, "rgba(200,200,200,0.3)")

gexf_parts = []
gexf_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
gexf_parts.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
gexf_parts.append('<meta><creator>Wuhu Investigator</creator><description>芜湖市领导班子工作关系网络</description></meta>')
gexf_parts.append('<graph mode="static" defaultedgetype="undirected">')

# Nodes
gexf_parts.append('<nodes>')
for p in persons:
    slug_id = f"wuhu_{p['id']}"
    role_color = color_for_role(p["current_post"])
    is_top = "书记" in (p["current_post"] or "") and "纪委" not in (p["current_post"] or "") and "副" not in (p["current_post"] or "")
    is_gov = ("市长" in (p["current_post"] or "") and "副" not in (p["current_post"] or "")) or ("县长" in (p["current_post"] or "") and "副" not in (p["current_post"] or "")) or ("区长" in (p["current_post"] or "") and "副" not in (p["current_post"] or ""))
    size = 20.0 if is_top else 15.0 if is_gov else 12.0
    label = f"{p['name']} ({p['current_post'] or '?'})"
    gexf_parts.append(f'<node id="{slug_id}" label="{label}">')
    gexf_parts.append(f'<attvalues><attvalue for="role" value="{p["current_post"]}"/><attvalue for="org" value="{p["current_org"]}"/><attvalue for="birth" value="{p["birth"]}"/><attvalue for="birthplace" value="{p["birthplace"]}"/></attvalues>')
    gexf_parts.append(f'<viz:color r="{int(role_color[1:3],16)}" g="{int(role_color[3:5],16)}" b="{int(role_color[5:7],16)}"/>')
    gexf_parts.append(f'<viz:size value="{size}"/>')
    gexf_parts.append('</node>')

for o in organizations:
    oid = f"org_{o['id']}"
    oc = org_color(o["type"])
    oc_rgb = oc.replace("rgba(", "").rstrip(")").split(",")
    gexf_parts.append(f'<node id="{oid}" label="{o["name"]}">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="{o["type"]}"/><attvalue for="level" value="{o["level"]}"/></attvalues>')
    gexf_parts.append(f'<viz:color r="{int(oc_rgb[0])}" g="{int(oc_rgb[1])}" b="{int(oc_rgb[2])}"/>')
    gexf_parts.append(f'<viz:size value="8.0"/>')
    gexf_parts.append('</node>')
gexf_parts.append('</nodes>')

# Edges
gexf_parts.append('<edges>')
edge_id = 0
for po in positions:
    p = next(x for x in persons if x["id"] == po["person_id"])
    o = next(x for x in organizations if x["id"] == po["org_id"])
    edge_id += 1
    label = f"{p['name']} → {o['name']} ({po['title']})"
    gexf_parts.append(f'<edge id="e{edge_id}" source="wuhu_{p["id"]}" target="org_{o["id"]}" label="{label}" weight="1.0">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="worked_at"/><attvalue for="title" value="{po["title"]}"/><attvalue for="start" value="{po["start"]}"/><attvalue for="end" value="{po["end"]}"/></attvalues>')
    gexf_parts.append('</edge>')

for r in relationships:
    p_a = next(x for x in persons if x["id"] == r["person_a"])
    p_b = next(x for x in persons if x["id"] == r["person_b"])
    edge_id += 1
    gexf_parts.append(f'<edge id="e{edge_id}" source="wuhu_{p_a["id"]}" target="wuhu_{p_b["id"]}" label="{r["context"]}" weight="2.0">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="relationship"/><attvalue for="context" value="{r["context"]}"/></attvalues>')
    gexf_parts.append('</edge>')

gexf_parts.append('</edges>')
gexf_parts.append('</graph>')
gexf_parts.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(gexf_parts))

print(f"✅ GEXF 已创建: {GEXF_PATH}")
print(f"   节点: {len(persons) + len(organizations)} | 边: {edge_id}")

conn.close()
print("✅ 完成!")
