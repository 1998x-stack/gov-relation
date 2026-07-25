#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 山西省领导班子 (Shanxi Province Leadership Network).
Investigation date: 2026-07-25

Current 山西省委书记: 唐登杰 (Tang Dengjie, since 2023.10)
Current 山西省省长: 卢东亮 (Lu Dongliang, since 2025.06)
"""

import os
import sqlite3
import sys
from pathlib import Path

# Add repo root to path
_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))
os.chdir(str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

DB_PATH = DATABASE_DIR / "山西省_network.db"
GEXF_PATH = GRAPH_DIR / "山西省_network.gexf"

# ═══════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════

persons = [
    # ── 唐登杰 - 山西省委书记 (Party Secretary) ──
    {"id": 1, "name": "唐登杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1964-06", "birthplace": "上海", "education": "同济大学机械工程系毕业，大学学历",
     "party_join": "中共党员", "work_start": "1985-07",
     "current_post": "山西省委书记、省人大常委会主任", "current_org": "中共山西省委",
     "source": "https://en.wikipedia.org/wiki/Tang_Dengjie"},

    # ── 卢东亮 - 山西省省长 (Governor) ──
    {"id": 2, "name": "卢东亮", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-12", "birthplace": "辽宁康平", "education": "北方工业大学会计专业毕业",
     "party_join": "1993-05", "work_start": "1995-08",
     "current_post": "山西省委副书记、省长", "current_org": "山西省人民政府",
     "source": "https://en.wikipedia.org/wiki/Lu_Dongliang"},

    # ── 蓝佛安 - 前任省委书记 (2022.12-2023.09)，现任财政部部长 ──
    {"id": 3, "name": "蓝佛安", "gender": "男", "ethnicity": "汉族",
     "birth": "1962-06", "birthplace": "广东惠东", "education": "湖北财经学院（现中南财经政法大学）财政专业毕业",
     "party_join": "中共党员", "work_start": "1985-08",
     "current_post": "财政部部长、党组书记", "current_org": "财政部",
     "source": "https://en.wikipedia.org/wiki/Lan_Fo%27an"},

    # ── 金湘军 - 前任省长 (2022.12-2025.04，后被调查) ──
    {"id": 4, "name": "金湘军", "gender": "男", "ethnicity": "汉族",
     "birth": "1964-07", "birthplace": "湖南江华", "education": "成都电讯工程学院（现电子科技大学）计算机软件专业毕业，华中科技大学管理学博士",
     "party_join": "中共党员（2025年开除）", "work_start": "1990-07",
     "current_post": "", "current_org": "",
     "source": "https://en.wikipedia.org/wiki/Jin_Xiangjun"},

    # ── 林武 - 前任省委书记 (2021.06-2022.12)，现任山东省委书记 ──
    {"id": 5, "name": "林武", "gender": "男", "ethnicity": "汉族",
     "birth": "1962-02", "birthplace": "福建闽侯", "education": "江西冶金学院（现江西理工大学）毕业",
     "party_join": "中共党员", "work_start": "1982-08",
     "current_post": "山东省委书记", "current_org": "中共山东省委",
     "source": "https://baike.baidu.com/item/%E6%9E%97%E6%AD%A6"},

    # ── 楼阳生 - 前任省委书记 (2019.11-2021.06)，前任河南省委书记 ──
    {"id": 6, "name": "楼阳生", "gender": "男", "ethnicity": "汉族",
     "birth": "1959-10", "birthplace": "浙江浦江", "education": "浙江师范大学数学系毕业，浙江大学工商管理硕士",
     "party_join": "中共党员", "work_start": "1976-08",
     "current_post": "", "current_org": "",
     "source": "https://en.wikipedia.org/wiki/Lou_Yangsheng"},

    # ── 李小鹏 - 前任省长 (2013.01-2016.08) ──
    {"id": 7, "name": "李小鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "1959-06", "birthplace": "四川成都", "education": "华北电力学院发电厂及电力系统专业毕业",
     "party_join": "中共党员", "work_start": "1975-08",
     "current_post": "交通运输部部长", "current_org": "交通运输部",
     "source": "https://en.wikipedia.org/wiki/Li_Xiaopeng"},

    # ── 张春林 - 省政协主席 ──
    {"id": 8, "name": "张春林", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-02", "birthplace": "四川德阳", "education": "八一农学院（现新疆农业大学）农业机械化专业毕业",
     "party_join": "1986-01", "work_start": "1986-07",
     "current_post": "山西省政协主席、党组书记", "current_org": "山西省政协",
     "source": "https://en.wikipedia.org/wiki/Zhang_Chunlin"},

    # ── 省委专职副书记（张春林前任，待确认当前人选）─ placeholder ──
    # 当前省委专职副书记空缺或由张春林转政协后新人接任

    # ── 王拥军 - 省纪委书记 ──
    {"id": 9, "name": "王拥军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "山西省委常委、省纪委书记、省监委主任", "current_org": "中共山西省纪律检查委员会",
     "source": "https://baike.baidu.com/item/%E7%8E%8B%E6%8B%A5%E5%86%9B"},

    # ── 省委组织部部长（待确认） ──
    {"id": 10, "name": "山西省委组织部部长", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "山西省委常委、组织部部长", "current_org": "中共山西省委组织部",
     "source": ""},

    # ── 省委宣传部部长（待确认） ──
    {"id": 11, "name": "山西省委宣传部部长", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "山西省委常委、宣传部部长", "current_org": "中共山西省委宣传部",
     "source": ""},

    # ── 省委统战部部长（待确认） ──
    {"id": 12, "name": "山西省委统战部部长", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "山西省委常委、统战部部长", "current_org": "中共山西省委统战部",
     "source": ""},

    # ── 省委政法委书记（待确认） ──
    {"id": 13, "name": "山西省委政法委书记", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "山西省委常委、政法委书记", "current_org": "中共山西省委政法委",
     "source": ""},

    # ── 省委秘书长（待确认） ──
    {"id": 14, "name": "山西省委秘书长", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "山西省委常委、秘书长", "current_org": "中共山西省委办公厅",
     "source": ""},

    # ── 太原市委书记（一般由省委常委兼任） ──
    {"id": 15, "name": "太原市委书记", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "山西省委常委、太原市委书记", "current_org": "中共太原市委",
     "source": ""},

    # ── 省军区司令员（省委常委兼任） ──
    {"id": 16, "name": "山西省军区司令员", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "山西省委常委、省军区司令员", "current_org": "山西省军区",
     "source": ""},

    # ── 卢东亮前任去路──
    # 金湘军已经列为id=4，这里不再重复

    # ── 常务副省长（待确认） ──
    {"id": 17, "name": "山西省常务副省长", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "山西省委常委、常务副省长", "current_org": "山西省人民政府",
     "source": ""},
]

organizations = [
    {"id": 1, "name": "中共山西省委", "type": "党委", "level": "省级", "parent": "", "location": "太原"},
    {"id": 2, "name": "山西省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "太原"},
    {"id": 3, "name": "中共山西省纪律检查委员会", "type": "纪委", "level": "省级", "parent": "中共山西省委", "location": "太原"},
    {"id": 4, "name": "中共山西省委组织部", "type": "党委部门", "level": "省级", "parent": "中共山西省委", "location": "太原"},
    {"id": 5, "name": "中共山西省委宣传部", "type": "党委部门", "level": "省级", "parent": "中共山西省委", "location": "太原"},
    {"id": 6, "name": "中共山西省委统战部", "type": "党委部门", "level": "省级", "parent": "中共山西省委", "location": "太原"},
    {"id": 7, "name": "中共山西省委政法委", "type": "党委部门", "level": "省级", "parent": "中共山西省委", "location": "太原"},
    {"id": 8, "name": "中共山西省委办公厅", "type": "党委部门", "level": "省级", "parent": "中共山西省委", "location": "太原"},
    {"id": 9, "name": "中共太原市委", "type": "党委", "level": "副省级", "parent": "中共山西省委", "location": "太原"},
    {"id": 10, "name": "山西省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "太原"},
    {"id": 11, "name": "山西省政协", "type": "政协", "level": "省级", "parent": "", "location": "太原"},
    {"id": 12, "name": "山西省军区", "type": "军队", "level": "省级", "parent": "", "location": "太原"},
    {"id": 13, "name": "财政部", "type": "政府", "level": "中央", "parent": "", "location": "北京"},
    {"id": 14, "name": "交通运输部", "type": "政府", "level": "中央", "parent": "", "location": "北京"},
    {"id": 15, "name": "中共山东省委", "type": "党委", "level": "省级", "parent": "", "location": "济南"},
    {"id": 16, "name": "中国铝业集团有限公司", "type": "国企", "level": "中央", "parent": "", "location": "北京"},
]

positions = [
    # 唐登杰
    {"person_id": 1, "org_id": 1, "title": "山西省委书记", "start_date": "2023-10", "end_date": "present", "rank": "正省级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "山西省人大常委会主任", "start_date": "2023-10", "end_date": "present", "rank": "正省级", "note": "由省委书记兼任"},
    # 唐登杰前任经历
    {"person_id": 1, "org_id": 13, "title": "民政部部长", "start_date": "2022-02", "end_date": "2023-12", "rank": "正省级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "国家发展和改革委员会副主任（正部长级）", "start_date": "2020-07", "end_date": "2022-02", "rank": "正省级", "note": "分管固定资产投资等"},
    {"person_id": 1, "org_id": 1, "title": "福建省省长", "start_date": "2018-01", "end_date": "2020-07", "rank": "正省级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "工业和信息化部副部长、国家航天局局长", "start_date": "2017-05", "end_date": "2017-12", "rank": "副省级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "中国兵器装备集团公司董事长、党组书记", "start_date": "2013-02", "end_date": "2017-05", "rank": "正部级央企", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "上海市副市长", "start_date": "2003-02", "end_date": "2011-04", "rank": "副省级", "note": "最年轻的上海市副市长"},
    {"person_id": 1, "org_id": 1, "title": "上海电气集团董事长", "start_date": "2001", "end_date": "2003-02", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "上海汽车工业（集团）总公司副总裁", "start_date": "1998", "end_date": "2001", "rank": "正厅级", "note": ""},

    # 卢东亮
    {"person_id": 2, "org_id": 2, "title": "山西省省长", "start_date": "2025-06", "end_date": "present", "rank": "正省级", "note": "2025年6月任代省长，后当选省长"},
    {"person_id": 2, "org_id": 1, "title": "山西省委副书记", "start_date": "2025-05", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "山西省副省长", "start_date": "2024-12", "end_date": "2025-06", "rank": "副省级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "大同市委书记", "start_date": "2021-11", "end_date": "2024-12", "rank": "副省级", "note": "省委常委兼任"},
    {"person_id": 2, "org_id": 1, "title": "山西省委常委", "start_date": "2021-10", "end_date": "present", "rank": "副省级", "note": "2021年10月入列省委常委"},
    {"person_id": 2, "org_id": 2, "title": "山西省副省长", "start_date": "2020-05", "end_date": "2021-10", "rank": "副省级", "note": ""},
    {"person_id": 2, "org_id": 16, "title": "中国铝业集团有限公司董事长、党组书记", "start_date": "2019-02", "end_date": "2020-05", "rank": "正部级央企", "note": ""},
    {"person_id": 2, "org_id": 16, "title": "中国铝业集团有限公司副总经理", "start_date": "2016-04", "end_date": "2019-02", "rank": "副部级央企", "note": ""},

    # 蓝佛安
    {"person_id": 3, "org_id": 1, "title": "山西省委书记", "start_date": "2022-12", "end_date": "2023-09", "rank": "正省级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "山西省省长", "start_date": "2021-06", "end_date": "2022-12", "rank": "正省级", "note": ""},
    {"person_id": 3, "org_id": 13, "title": "财政部部长、党组书记", "start_date": "2023-10", "end_date": "present", "rank": "正省级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "海南省委常委、省纪委书记", "start_date": "2017-03", "end_date": "2021-04", "rank": "副省级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "广东省副省长", "start_date": "2016-01", "end_date": "2017-03", "rank": "副省级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "韶关市委书记", "start_date": "2015-03", "end_date": "2016-01", "rank": "正厅级", "note": ""},

    # 金湘军
    {"person_id": 4, "org_id": 2, "title": "山西省省长", "start_date": "2022-12", "end_date": "2025-04", "rank": "正省级", "note": "2025年4月被调查，10月被开除党籍和公职"},
    {"person_id": 4, "org_id": 1, "title": "天津市委副书记", "start_date": "2022-03", "end_date": "2022-12", "rank": "副省级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "天津市委常委、秘书长", "start_date": "2021-01", "end_date": "2022-03", "rank": "副省级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "天津市副市长", "start_date": "2018-01", "end_date": "2022-03", "rank": "副省级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "防城港市委书记", "start_date": "2014-01", "end_date": "2018-01", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "玉林市委书记", "start_date": "2009-02", "end_date": "2014-01", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "玉林市市长", "start_date": "2003-05", "end_date": "2009-02", "rank": "正厅级", "note": ""},

    # 林武
    {"person_id": 5, "org_id": 1, "title": "山西省委书记", "start_date": "2021-06", "end_date": "2022-12", "rank": "正省级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "山西省省长", "start_date": "2019-12", "end_date": "2021-06", "rank": "正省级", "note": ""},
    {"person_id": 5, "org_id": 15, "title": "山东省委书记", "start_date": "2022-12", "end_date": "present", "rank": "正省级", "note": ""},

    # 楼阳生
    {"person_id": 6, "org_id": 1, "title": "山西省委书记", "start_date": "2019-11", "end_date": "2021-06", "rank": "正省级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "山西省省长", "start_date": "2016-08", "end_date": "2019-11", "rank": "正省级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "山西省委副书记", "start_date": "2014-06", "end_date": "2016-08", "rank": "副省级", "note": ""},

    # 李小鹏
    {"person_id": 7, "org_id": 2, "title": "山西省省长", "start_date": "2013-01", "end_date": "2016-08", "rank": "正省级", "note": ""},
    {"person_id": 7, "org_id": 14, "title": "交通运输部部长", "start_date": "2016-09", "end_date": "present", "rank": "正省级", "note": ""},

    # 张春林
    {"person_id": 8, "org_id": 11, "title": "山西省政协主席", "start_date": "2025-01", "end_date": "present", "rank": "正省级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "山西省委副书记", "start_date": "2023-11", "end_date": "2025-01", "rank": "副省级", "note": "专职副书记"},
    {"person_id": 8, "org_id": 1, "title": "新疆维吾尔自治区党委副书记", "start_date": "2021-04", "end_date": "2023-11", "rank": "副省级", "note": "兼任宣传部部长"},
    {"person_id": 8, "org_id": 1, "title": "新疆维吾尔自治区常务副主席", "start_date": "2018-01", "end_date": "2021-04", "rank": "副省级", "note": ""},

    # 王拥军
    {"person_id": 9, "org_id": 3, "title": "山西省纪委书记、省监委主任", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},

    # 省委常委各部门（占位）
    {"person_id": 10, "org_id": 4, "title": "山西省委组织部部长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 11, "org_id": 5, "title": "山西省委宣传部部长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 12, "org_id": 6, "title": "山西省委统战部部长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 13, "org_id": 7, "title": "山西省委政法委书记", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 14, "org_id": 8, "title": "山西省委秘书长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 15, "org_id": 9, "title": "太原市委书记", "start_date": "", "end_date": "present", "rank": "副省级", "note": "省委常委兼任"},
    {"person_id": 16, "org_id": 12, "title": "山西省军区司令员", "start_date": "", "end_date": "present", "rank": "副省级", "note": "省委常委兼任"},
    {"person_id": 17, "org_id": 2, "title": "山西省常务副省长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
]

relationships = [
    # 唐登杰 — 卢东亮（省委书记—省长搭班）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "省委书记—省长搭班", "overlap_org": "山西省", "overlap_period": "2025-06至今"},
    # 唐登杰 — 蓝佛安（前任继任）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "接替蓝佛安任山西省委书记", "overlap_org": "中共山西省委", "overlap_period": "2023-10"},
    # 蓝佛安 — 林武（前任继任）
    {"person_a": 3, "person_b": 5, "type": "predecessor_successor", "context": "接替林武任山西省委书记", "overlap_org": "中共山西省委", "overlap_period": "2022-12"},
    # 蓝佛安 — 林武（前省长—前书记搭班）
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "前任省长—前任省委书记搭班", "overlap_org": "山西省", "overlap_period": "2021-06至2022-12"},
    # 林武 — 楼阳生（前任继任）
    {"person_a": 5, "person_b": 6, "type": "predecessor_successor", "context": "接替楼阳生任山西省委书记", "overlap_org": "中共山西省委", "overlap_period": "2021-06"},
    # 林武 — 楼阳生（前省长—前书记搭班）
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "前任省长—前任省委书记搭班", "overlap_org": "山西省", "overlap_period": "2019-12至2021-06"},
    # 楼阳生 — 李小鹏（前任继任/省长交接）
    {"person_a": 6, "person_b": 7, "type": "predecessor_successor", "context": "接替李小鹏任山西省省长", "overlap_org": "山西省人民政府", "overlap_period": "2016-08"},
    # 蓝佛安 — 金湘军（前任书记—前任省长搭班）
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "前任省委书记—前任省长搭班", "overlap_org": "山西省", "overlap_period": "2022-12至2023-09"},
    # 唐登杰 — 金湘军（前任书记—前任省长搭班）
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "现任省委书记—前任省长搭班", "overlap_org": "山西省", "overlap_period": "2023-10至2025-04"},
    # 卢东亮 — 金湘军（现任省长—前任省长）
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor", "context": "接替金湘军任山西省省长", "overlap_org": "山西省人民政府", "overlap_period": "2025-06"},
    # 卢东亮 — 张春林（省委副书记—省政协主席）
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "现任省委副书记（后任省长）与前任专职副书记搭班", "overlap_org": "中共山西省委", "overlap_period": "2023-11至2025-01"},
    # 唐登杰 — 张春林（省委书记—专职副书记/政协主席）
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "省委书记—省委副书记/省政协主席", "overlap_org": "中共山西省委", "overlap_period": "2023-11至今"},
    # 唐登杰 — 王拥军（上下级）
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "省委书记—省纪委书记", "overlap_org": "中共山西省委", "overlap_period": "2023-10至今"},
]

# ═══════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="山西省",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done: 山西省 network built.")
