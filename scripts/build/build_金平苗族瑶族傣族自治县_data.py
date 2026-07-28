#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 金平苗族瑶族傣族自治县 leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/金平苗族瑶族傣族自治县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/金平苗族瑶族傣族自治县_network.gexf")

# ── DATA ── (same as canonical version)
persons = [
    {"id": 1, "name": "张猛", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "中共金平苗族瑶族傣族自治县委书记", "current_org": "中共金平苗族瑶族傣族自治县委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 2, "name": "田红梅", "gender": "女", "ethnicity": "傣族", "birth": "1974-09", "birthplace": "云南金平", "education": "省委党校研究生", "party_join": "中共党员", "work_start": "", "current_post": "金平苗族瑶族傣族自治县人民政府县长", "current_org": "金平苗族瑶族傣族自治县人民政府", "source": "https://www.hhjp.gov.cn/info/52521/20651.htm"},
    {"id": 3, "name": "苏庆劼", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "中共金平县委副书记", "current_org": "中共金平苗族瑶族傣族自治县委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 4, "name": "张亮", "gender": "男", "ethnicity": "汉族", "birth": "1982-11", "birthplace": "", "education": "云南省委党校在职研究生", "party_join": "中共党员", "work_start": "", "current_post": "金平县委常委、常务副县长", "current_org": "金平苗族瑶族傣族自治县人民政府", "source": "https://www.hhjp.gov.cn/info/52541/353891.htm"},
    {"id": 5, "name": "普康列", "gender": "男", "ethnicity": "彝族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县委常委、县纪委书记、县监委主任", "current_org": "中共金平苗族瑶族傣族自治县纪律检查委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 6, "name": "许建国", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县委常委", "current_org": "中共金平苗族瑶族傣族自治县委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 7, "name": "董春进", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县委常委", "current_org": "中共金平苗族瑶族傣族自治县委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 8, "name": "高志平", "gender": "男", "ethnicity": "白族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县委常委", "current_org": "中共金平苗族瑶族傣族自治县委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 9, "name": "王俊", "gender": "男", "ethnicity": "彝族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县委常委", "current_org": "中共金平苗族瑶族傣族自治县委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 10, "name": "李岸青", "gender": "男", "ethnicity": "傣族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县委常委", "current_org": "中共金平苗族瑶族傣族自治县委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 11, "name": "张云桃", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县委常委", "current_org": "中共金平苗族瑶族傣族自治县委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 12, "name": "吴新华", "gender": "男", "ethnicity": "汉族", "birth": "1984-01", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县委常委、副县长（挂职）", "current_org": "金平苗族瑶族傣族自治县人民政府", "source": "https://www.hhjp.gov.cn/info/52521/20651.htm"},
    {"id": 13, "name": "刘轩", "gender": "男", "ethnicity": "汉族", "birth": "1978-02", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县委常委、副县长（挂职）", "current_org": "金平苗族瑶族傣族自治县人民政府", "source": "https://www.hhjp.gov.cn/info/52521/20651.htm"},
    {"id": 14, "name": "潘立虎", "gender": "男", "ethnicity": "汉族", "birth": "1982-01", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县委常委、副县长（挂职）", "current_org": "金平苗族瑶族傣族自治县人民政府", "source": "https://www.hhjp.gov.cn/info/52521/20651.htm"},
    {"id": 15, "name": "熊伟", "gender": "男", "ethnicity": "苗族", "birth": "1979-04", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县人民政府副县长", "current_org": "金平苗族瑶族傣族自治县人民政府", "source": "https://www.hhjp.gov.cn/info/52521/20651.htm"},
    {"id": 16, "name": "吴进", "gender": "男", "ethnicity": "彝族", "birth": "1984-07", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县人民政府副县长", "current_org": "金平苗族瑶族傣族自治县人民政府", "source": "https://www.hhjp.gov.cn/info/52521/20651.htm"},
    {"id": 17, "name": "普寿华", "gender": "男", "ethnicity": "哈尼族", "birth": "1980-09", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县人民政府副县长、县公安局局长", "current_org": "金平苗族瑶族傣族自治县人民政府", "source": "https://www.hhjp.gov.cn/info/52521/20651.htm"},
    {"id": 18, "name": "李保富", "gender": "男", "ethnicity": "彝族", "birth": "1984-04", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县人民政府副县长", "current_org": "金平苗族瑶族傣族自治县人民政府", "source": "https://www.hhjp.gov.cn/info/52521/20651.htm"},
    {"id": 19, "name": "白春文", "gender": "男", "ethnicity": "", "birth": "1984-03", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县人民政府副县长", "current_org": "金平苗族瑶族傣族自治县人民政府", "source": "https://www.hhjp.gov.cn/info/52521/20651.htm"},
    {"id": 20, "name": "姜冬", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县纪委副书记、县监委副主任", "current_org": "中共金平苗族瑶族傣族自治县纪律检查委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 21, "name": "杨红", "gender": "男", "ethnicity": "彝族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县纪委副书记、县监委副主任", "current_org": "中共金平苗族瑶族傣族自治县纪律检查委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 22, "name": "桂宝雨", "gender": "男", "ethnicity": "回族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县纪委副书记、县监委副主任", "current_org": "中共金平苗族瑶族傣族自治县纪律检查委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 23, "name": "王正纪", "gender": "男", "ethnicity": "彝族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县纪委常委", "current_org": "中共金平苗族瑶族傣族自治县纪律检查委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 24, "name": "朱兴林", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县纪委常委", "current_org": "中共金平苗族瑶族傣族自治县纪律检查委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 25, "name": "杨奇涵", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县纪委常委", "current_org": "中共金平苗族瑶族傣族自治县纪律检查委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 26, "name": "唐红增", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县纪委常委", "current_org": "中共金平苗族瑶族傣族自治县纪律检查委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
    {"id": 27, "name": "简玉凤", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "金平县纪委常委", "current_org": "中共金平苗族瑶族傣族自治县纪律检查委员会", "source": "https://www.hhjp.gov.cn/info/2211/397931.htm"},
]

organizations = [
    {"id": 1, "name": "中共金平苗族瑶族傣族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共红河哈尼族彝族自治州委员会", "location": "云南红河金平"},
    {"id": 2, "name": "金平苗族瑶族傣族自治县人民政府", "type": "政府", "level": "县处级", "parent": "红河哈尼族彝族自治州人民政府", "location": "云南红河金平"},
    {"id": 3, "name": "中共金平苗族瑶族傣族自治县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共红河哈尼族彝族自治州纪律检查委员会", "location": "云南红河金平"},
    {"id": 4, "name": "金平苗族瑶族傣族自治县监察委员会", "type": "监察", "level": "县处级", "parent": "", "location": "云南红河金平"},
    {"id": 5, "name": "金平苗族瑶族傣族自治县公安局", "type": "政府", "level": "乡科级", "parent": "金平县人民政府", "location": "云南红河金平"},
]

positions = [
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共金平苗族瑶族傣族自治县委书记", "start": "2026-06", "end": "", "rank": "县处级正职", "note": "第十四届县委一次全会当选"},
    {"id": 2, "person_id": 2, "org_id": 1, "title": "中共金平苗族瑶族傣族自治县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "金平苗族瑶族傣族自治县人民政府县长", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 4, "person_id": 3, "org_id": 1, "title": "中共金平苗族瑶族傣族自治县委副书记", "start": "2026-06", "end": "", "rank": "县处级副职", "note": "第十四届县委一次全会当选"},
    {"id": 5, "person_id": 4, "org_id": 1, "title": "金平县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 6, "person_id": 4, "org_id": 2, "title": "金平县委常委、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 7, "person_id": 5, "org_id": 1, "title": "金平县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 8, "person_id": 5, "org_id": 3, "title": "金平县委常委、县纪委书记、县监委主任", "start": "2026-06", "end": "", "rank": "县处级副职", "note": "第十四届纪委全会当选"},
    {"id": 9, "person_id": 6, "org_id": 1, "title": "金平县委常委", "start": "2026-06", "end": "", "rank": "县处级副职", "note": "第十四届县委全会当选"},
    {"id": 10, "person_id": 7, "org_id": 1, "title": "金平县委常委", "start": "2026-06", "end": "", "rank": "县处级副职", "note": "第十四届县委全会当选"},
    {"id": 11, "person_id": 8, "org_id": 1, "title": "金平县委常委", "start": "2026-06", "end": "", "rank": "县处级副职", "note": "第十四届县委全会当选"},
    {"id": 12, "person_id": 9, "org_id": 1, "title": "金平县委常委", "start": "2026-06", "end": "", "rank": "县处级副职", "note": "第十四届县委全会当选"},
    {"id": 13, "person_id": 10, "org_id": 1, "title": "金平县委常委", "start": "2026-06", "end": "", "rank": "县处级副职", "note": "第十四届县委全会当选"},
    {"id": 14, "person_id": 11, "org_id": 1, "title": "金平县委常委", "start": "2026-06", "end": "", "rank": "县处级副职", "note": "第十四届县委全会当选"},
    {"id": 15, "person_id": 12, "org_id": 2, "title": "金平县委常委、副县长（挂职）", "start": "", "end": "", "rank": "县处级副职", "note": "挂职"},
    {"id": 16, "person_id": 13, "org_id": 2, "title": "金平县委常委、副县长（挂职）", "start": "", "end": "", "rank": "县处级副职", "note": "挂职"},
    {"id": 17, "person_id": 14, "org_id": 2, "title": "金平县委常委、副县长（挂职）", "start": "", "end": "", "rank": "县处级副职", "note": "挂职"},
    {"id": 18, "person_id": 15, "org_id": 2, "title": "金平县人民政府副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 19, "person_id": 16, "org_id": 2, "title": "金平县人民政府副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 20, "person_id": 17, "org_id": 2, "title": "金平县人民政府副县长、县公安局局长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 21, "person_id": 18, "org_id": 2, "title": "金平县人民政府副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 22, "person_id": 19, "org_id": 2, "title": "金平县人民政府副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 23, "person_id": 20, "org_id": 3, "title": "金平县纪委副书记、县监委副主任", "start": "2026-06", "end": "", "rank": "乡科级正职", "note": "第十四届纪委全会当选"},
    {"id": 24, "person_id": 21, "org_id": 3, "title": "金平县纪委副书记、县监委副主任", "start": "2026-06", "end": "", "rank": "乡科级正职", "note": "第十四届纪委全会当选"},
    {"id": 25, "person_id": 22, "org_id": 3, "title": "金平县纪委副书记、县监委副主任", "start": "2026-06", "end": "", "rank": "乡科级正职", "note": "第十四届纪委全会当选"},
    {"id": 26, "person_id": 23, "org_id": 3, "title": "金平县纪委常委", "start": "2026-06", "end": "", "rank": "乡科级副职", "note": "第十四届纪委全会当选"},
    {"id": 27, "person_id": 24, "org_id": 3, "title": "金平县纪委常委", "start": "2026-06", "end": "", "rank": "乡科级副职", "note": "第十四届纪委全会当选"},
    {"id": 28, "person_id": 25, "org_id": 3, "title": "金平县纪委常委", "start": "2026-06", "end": "", "rank": "乡科级副职", "note": "第十四届纪委全会当选"},
    {"id": 29, "person_id": 26, "org_id": 3, "title": "金平县纪委常委", "start": "2026-06", "end": "", "rank": "乡科级副职", "note": "第十四届纪委全会当选"},
    {"id": 30, "person_id": 27, "org_id": 3, "title": "金平县纪委常委", "start": "2026-06", "end": "", "rank": "乡科级副职", "note": "第十四届纪委全会当选"},
]

relationships = [
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "张猛（县委书记）与田红梅（县长）构成金平县党政正职搭档", "overlap_org": "中共金平苗族瑶族傣族自治县委员会", "overlap_period": "2026-06至今"},
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "同僚", "context": "张猛（书记）与苏庆劼（专职副书记）为县委同僚", "overlap_org": "中共金平苗族瑶族傣族自治县委员会", "overlap_period": "2026-06至今"},
    {"id": 3, "person_a_id": 1, "person_b_id": 4, "type": "同僚", "context": "同为第十四届县委常委", "overlap_org": "中共金平苗族瑶族傣族自治县委员会", "overlap_period": "2026-06至今"},
    {"id": 4, "person_a_id": 1, "person_b_id": 5, "type": "同僚", "context": "同为第十四届县委常委", "overlap_org": "中共金平苗族瑶族傣族自治县委员会", "overlap_period": "2026-06至今"},
    {"id": 5, "person_a_id": 1, "person_b_id": 6, "type": "同僚", "context": "同为第十四届县委常委", "overlap_org": "中共金平苗族瑶族傣族自治县委员会", "overlap_period": "2026-06至今"},
    {"id": 6, "person_a_id": 1, "person_b_id": 7, "type": "同僚", "context": "同为第十四届县委常委", "overlap_org": "中共金平苗族瑶族傣族自治县委员会", "overlap_period": "2026-06至今"},
    {"id": 7, "person_a_id": 1, "person_b_id": 8, "type": "同僚", "context": "同为第十四届县委常委", "overlap_org": "中共金平苗族瑶族傣族自治县委员会", "overlap_period": "2026-06至今"},
    {"id": 8, "person_a_id": 1, "person_b_id": 9, "type": "同僚", "context": "同为第十四届县委常委", "overlap_org": "中共金平苗族瑶族傣族自治县委员会", "overlap_period": "2026-06至今"},
    {"id": 9, "person_a_id": 1, "person_b_id": 10, "type": "同僚", "context": "同为第十四届县委常委；李岸青陪同张猛下乡调研", "overlap_org": "中共金平苗族瑶族傣族自治县委员会", "overlap_period": "2026-06至今"},
    {"id": 10, "person_a_id": 1, "person_b_id": 11, "type": "同僚", "context": "同为第十四届县委常委", "overlap_org": "中共金平苗族瑶族傣族自治县委员会", "overlap_period": "2026-06至今"},
    {"id": 11, "person_a_id": 2, "person_b_id": 4, "type": "上下级", "context": "田红梅（县长）与张亮（常务副县长）为正副职", "overlap_org": "金平苗族瑶族傣族自治县人民政府", "overlap_period": ""},
    {"id": 12, "person_a_id": 2, "person_b_id": 12, "type": "上下级", "context": "田红梅与挂职副县长吴新华", "overlap_org": "金平苗族瑶族傣族自治县人民政府", "overlap_period": ""},
    {"id": 13, "person_a_id": 2, "person_b_id": 13, "type": "上下级", "context": "田红梅与挂职副县长刘轩", "overlap_org": "金平苗族瑶族傣族自治县人民政府", "overlap_period": ""},
    {"id": 14, "person_a_id": 2, "person_b_id": 14, "type": "上下级", "context": "田红梅与挂职副县长潘立虎", "overlap_org": "金平苗族瑶族傣族自治县人民政府", "overlap_period": ""},
    {"id": 15, "person_a_id": 2, "person_b_id": 15, "type": "上下级", "context": "田红梅与熊伟（副县长）", "overlap_org": "金平苗族瑶族傣族自治县人民政府", "overlap_period": ""},
    {"id": 16, "person_a_id": 2, "person_b_id": 16, "type": "上下级", "context": "田红梅与吴进（副县长）", "overlap_org": "金平苗族瑶族傣族自治县人民政府", "overlap_period": ""},
    {"id": 17, "person_a_id": 2, "person_b_id": 17, "type": "上下级", "context": "田红梅与普寿华（副县长、公安局长）", "overlap_org": "金平苗族瑶族傣族自治县人民政府", "overlap_period": ""},
    {"id": 18, "person_a_id": 2, "person_b_id": 18, "type": "上下级", "context": "田红梅与李保富（副县长）", "overlap_org": "金平苗族瑶族傣族自治县人民政府", "overlap_period": ""},
    {"id": 19, "person_a_id": 2, "person_b_id": 19, "type": "上下级", "context": "田红梅与白春文（副县长）", "overlap_org": "金平苗族瑶族傣族自治县人民政府", "overlap_period": ""},
    {"id": 20, "person_a_id": 5, "person_b_id": 20, "type": "上下级", "context": "普康列（纪委书记）与姜冬（纪委副书记）", "overlap_org": "中共金平苗族瑶族傣族自治县纪律检查委员会", "overlap_period": "2026-06至今"},
    {"id": 21, "person_a_id": 5, "person_b_id": 21, "type": "上下级", "context": "普康列与杨红（纪委副书记）", "overlap_org": "中共金平苗族瑶族傣族自治县纪律检查委员会", "overlap_period": "2026-06至今"},
    {"id": 22, "person_a_id": 5, "person_b_id": 22, "type": "上下级", "context": "普康列与桂宝雨（纪委副书记）", "overlap_org": "中共金平苗族瑶族傣族自治县纪律检查委员会", "overlap_period": "2026-06至今"},
]

# ── BUILD SQLite DATABASE ──────────────────────
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.executescript("""
CREATE TABLE persons (id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT, ethnicity TEXT, birth TEXT, birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT, current_post TEXT, current_org TEXT, source TEXT);
CREATE TABLE organizations (id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT, level TEXT, parent TEXT, location TEXT);
CREATE TABLE positions (id INTEGER PRIMARY KEY, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL, title TEXT NOT NULL, start TEXT, end TEXT, rank TEXT, note TEXT, FOREIGN KEY (person_id) REFERENCES persons(id), FOREIGN KEY (org_id) REFERENCES organizations(id));
CREATE TABLE relationships (id INTEGER PRIMARY KEY, person_a_id INTEGER NOT NULL, person_b_id INTEGER NOT NULL, type TEXT NOT NULL, context TEXT, overlap_org TEXT, overlap_period TEXT, FOREIGN KEY (person_a_id) REFERENCES persons(id), FOREIGN KEY (person_b_id) REFERENCES persons(id));
""")
for p in persons:
    cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in organizations:
    cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    cur.execute("INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)", (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
for r in relationships:
    cur.execute("INSERT INTO relationships VALUES (?,?,?,?,?,?,?)", (r["id"],r["person_a_id"],r["person_b_id"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
conn.commit()
cur.execute("SELECT COUNT(*) FROM persons"); pc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations"); oc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions"); psc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships"); rc = cur.fetchone()[0]
conn.close()
print(f"SQLite: {DB_PATH}  ({pc} persons, {oc} orgs, {psc} positions, {rc} relationships)")

# ── GEXF ───────────────────────────────────────
today = datetime.now().strftime("%Y-%m-%d")
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
         f'  <meta lastmodifieddate="{today}">',
         '    <creator>china-gov-network</creator>',
         f'    <description>金平苗族瑶族傣族自治县领导班子工作关系网络</description>',
         '  </meta>',
         '  <graph mode="static" defaultedgetype="undirected">',
         '    <attributes class="node">',
         '      <attribute id="type" title="Type" type="string"/>',
         '      <attribute id="category" title="Category" type="string"/>',
         '      <attribute id="birth" title="Birth" type="string"/>',
         '      <attribute id="birthplace" title="Birthplace" type="string"/>',
         '      <attribute id="current_post" title="Current Post" type="string"/>',
         '      <attribute id="source" title="Source" type="string"/>',
         '    </attributes>',
         '    <attributes class="edge">',
         '      <attribute id="type" title="Type" type="string"/>',
         '      <attribute id="context" title="Context" type="string"/>',
         '      <attribute id="period" title="Period" type="string"/>',
         '    </attributes>',
         '    <nodes>']
for p in persons:
    pid = p["id"]
    if pid == 1: cr, cg, cb, sz="255","50","50","20.0"
    elif pid == 2: cr, cg, cb, sz="50","100","255","20.0"
    elif pid == 3: cr, cg, cb, sz="50","100","255","16.0"
    elif pid == 5: cr, cg, cb, sz="255","165","0","16.0"
    else: cr, cg, cb, sz="100","100","100","12.0"
    lines.append(f'<node id="p{pid}" label="{p["name"]}">')
    lines.append(f'<attvalues><attvalue for="type" value="person"/><attvalue for="category" value="person"/><attvalue for="birth" value="{p["birth"]}"/><attvalue for="birthplace" value="{p["birthplace"]}"/><attvalue for="current_post" value="{p["current_post"]}"/><attvalue for="source" value="{p["source"]}"/></attvalues>')
    lines.append(f'<viz:color r="{cr}" g="{cg}" b="{cb}"/><viz:size value="{sz}"/></node>')
for o in organizations:
    lines.append(f'<node id="o{1000+o["id"]}" label="{o["name"]}"><attvalues><attvalue for="type" value="org"/><attvalue for="category" value="{o["type"]}"/></attvalues><viz:color r="40" g="60" b="80"/><viz:size value="8.0"/></node>')
lines.append('</nodes><edges>')
eid = 1
for pos in positions:
    lines.append(f'<edge id="e{eid}" source="p{pos["person_id"]}" target="o{1000+pos["org_id"]}" label="worked_at"><attvalues><attvalue for="type" value="worked_at"/><attvalue for="context" value="{pos["title"]}"/><attvalue for="period" value="{(pos["start"] or "?")} → {(pos["end"] or "今")}"/></attvalues></edge>')
    eid += 1
for r in relationships:
    lines.append(f'<edge id="e{eid}" source="person{r["person_a_id"]}" target="person{r["person_b_id"]}" label="{r["type"]}"><attvalues><attvalue for="type" value="{r["type"]}"/><attvalue for="context" value="{r["context"]}"/><attvalue for="period" value="{r["overlap_period"]}"/></attvalues></edge>')
    eid += 1
lines.append('</edges></graph></gexf>')
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"GEXF: {GEXF_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)+len(relationships)} edges)")
print("Done!")