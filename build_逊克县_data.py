#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 逊克县 leadership network.

逊克县隶属黑龙江省黑河市。位于黑龙江省东北部，边境线长135公里，
下辖9个乡镇、78个行政村，常住人口8.2万人（七人普）。

Current leadership as of 2026-08 (sources: www.xunke.gov.cn):
- 县委书记: 冯术学
- 县长: 南极

All biographical data sourced from official government leadership pages on www.xunke.gov.cn.
"""

import sqlite3
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "逊克县"
DB_PATH = DATABASE_DIR / "逊克县_network.db"
GEXF_PATH = GRAPH_DIR / "逊克县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共逊克县委员会", "type": "党委", "level": "县处级", "parent": "中共黑河市委", "location": "黑龙江省黑河市逊克县"},
    {"id": 2, "name": "逊克县人民政府", "type": "政府", "level": "县处级", "parent": "黑河市人民政府", "location": "黑龙江省黑河市逊克县"},
    {"id": 3, "name": "逊克县人大常委会", "type": "人大", "level": "县处级", "parent": "黑河市人大常委会", "location": "黑龙江省黑河市逊克县"},
    {"id": 4, "name": "中国人民政治协商会议逊克县委员会", "type": "政协", "level": "县处级", "parent": "政协黑河市委员会", "location": "黑龙江省黑河市逊克县"},
    {"id": 5, "name": "中共逊克县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共黑河市纪委", "location": "黑龙江省黑河市逊克县"},
    {"id": 6, "name": "逊克县公安局", "type": "政府", "level": "县处级", "parent": "逊克县人民政府", "location": "黑龙江省黑河市逊克县"},
    {"id": 7, "name": "黑龙江逊克经济开发区", "type": "开发区", "level": "县处级", "parent": "逊克县人民政府", "location": "黑龙江省黑河市逊克县"},
]

# ── PERSONS ─────────────────────────────────────────────────────────

persons = [
    # ═══ 县委领导 ═══
    # 1 — 冯术学 — 县委书记
    {"id": 1, "name": "冯术学", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共逊克县委书记", "current_org": "中共逊克县委员会",
     "source": "http://www.xunke.gov.cn/xkx/c100746/202607/c11_357193.shtml"},
    # 2 — 南极 — 县长
    {"id": 2, "name": "南极", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年3月", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "逊克县委副书记、政府县长", "current_org": "逊克县人民政府",
     "source": "http://www.xunke.gov.cn/xkx/c100852/szfld.shtml"},
    # 3 — 尹刚 — 常务副县长
    {"id": 3, "name": "尹刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年4月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "逊克县委常委、政府副县长", "current_org": "逊克县人民政府",
     "source": "http://www.xunke.gov.cn/xkx/yg002/szfld.shtml"},
    # 4 — 刘建军 — 副县长
    {"id": 4, "name": "刘建军", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年12月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "逊克县委常委、政府副县长", "current_org": "逊克县人民政府",
     "source": "http://www.xunke.gov.cn/xkx/ljj/szfld.shtml"},
    # 5 — 史晓倩 — 挂职副县长
    {"id": 5, "name": "史晓倩", "gender": "女", "ethnicity": "汉族",
     "birth": "1990年4月", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "逊克县委常委、政府副县长（挂职）", "current_org": "逊克县人民政府",
     "source": "http://www.xunke.gov.cn/xkx/c100874/szfld.shtml"},
    # 6 — 车福海 — 副县长
    {"id": 6, "name": "车福海", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年8月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "逊克县政府副县长", "current_org": "逊克县人民政府",
     "source": "http://www.xunke.gov.cn/xkx/c103144/szfld.shtml"},
    # 7 — 矫志鹏 — 副县长、公安局长
    {"id": 7, "name": "矫志鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年10月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "逊克县政府副县长、县公安局局长", "current_org": "逊克县人民政府",
     "source": "http://www.xunke.gov.cn/xkx/jzp/szfld.shtml"},
    # 8 — 宋振海 — 副县长
    {"id": 8, "name": "宋振海", "gender": "男", "ethnicity": "汉族",
     "birth": "1984年10月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "逊克县政府副县长", "current_org": "逊克县人民政府",
     "source": "http://www.xunke.gov.cn/xkx/szh2026/szfld.shtml"},
    # 9 — 孙东昭 — 副县长
    {"id": 9, "name": "孙东昭", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年9月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "逊克县政府副县长", "current_org": "逊克县人民政府",
     "source": "http://www.xunke.gov.cn/xkx/myz/szfld.shtml"},
    # 10 — 郭丽娟 — 副县长
    {"id": 10, "name": "郭丽娟", "gender": "女", "ethnicity": "汉族",
     "birth": "1979年9月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "逊克县政府副县长", "current_org": "逊克县人民政府",
     "source": "http://www.xunke.gov.cn/xkx/glj/szfld.shtml"},
    # 11 — 徐延民 — 人大主任
    {"id": 11, "name": "徐延民", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "逊克县人大常委会主任", "current_org": "逊克县人大常委会",
     "source": "http://www.xunke.gov.cn/xkx/c100746/202607/c11_356264.shtml"},
    # 12 — 姜明星 — 人大副主任
    {"id": 12, "name": "姜明星", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "逊克县人大常委会副主任", "current_org": "逊克县人大常委会",
     "source": "http://www.xunke.gov.cn/xkx/c100746/202607/c11_356264.shtml"},
    # 13 — 刘建升 — 人大副主任
    {"id": 13, "name": "刘建升", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "逊克县人大常委会副主任", "current_org": "逊克县人大常委会",
     "source": "http://www.xunke.gov.cn/xkx/c100746/202607/c11_356264.shtml"},
]

# ── POSITIONS ──────────────────────────────────────────────────────

positions = [
    # 冯术学 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共逊克县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县委全面工作"},

    # 南极 — 县长
    {"person_id": 2, "org_id": 1, "title": "逊克县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "逊克县政府县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县政府全面工作"},

    # 尹刚 — 常务副县长
    {"person_id": 3, "org_id": 1, "title": "逊克县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "逊克县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责县政府常务工作"},

    # 刘建军 — 县委常委、副县长
    {"person_id": 4, "org_id": 1, "title": "逊克县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "逊克县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责发改商务、统计、交通运输"},

    # 史晓倩 — 县委常委、挂职副县长
    {"person_id": 5, "org_id": 1, "title": "逊克县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "挂职"},
    {"person_id": 5, "org_id": 2, "title": "逊克县政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "", "note": "省科技厅援边挂职"},

    # 车福海
    {"person_id": 6, "org_id": 2, "title": "逊克县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责市场监管、营商环境、金融保险"},

    # 矫志鹏
    {"person_id": 7, "org_id": 2, "title": "逊克县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "逊克县公安局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责公共安全、司法"},

    # 宋振海
    {"person_id": 8, "org_id": 2, "title": "逊克县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责工业经济、生态环境、招商引资"},

    # 孙东昭
    {"person_id": 9, "org_id": 2, "title": "逊克县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责农业农村、水务、供销社"},

    # 郭丽娟
    {"person_id": 10, "org_id": 2, "title": "逊克县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责教育体育、卫生健康、文化旅游、医疗保障"},

    # 徐延民
    {"person_id": 11, "org_id": 3, "title": "逊克县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},

    # 姜明星
    {"person_id": 12, "org_id": 3, "title": "逊克县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 刘建升
    {"person_id": 13, "org_id": 3, "title": "逊克县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────

relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "逊克县党政正职搭档: 县委书记与县长", "overlap_org": "中共逊克县委员会/逊克县人民政府", "overlap_period": "current"},
    # 县委副书记搭档（县长兼任副书记）
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与县委常委、常务副县长", "overlap_org": "中共逊克县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与县委常委、副县长刘建军", "overlap_org": "中共逊克县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记与挂职县委常委史晓倩", "overlap_org": "中共逊克县委员会", "overlap_period": "current"},
    # 县长与副县长
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与常务副县长", "overlap_org": "逊克县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长与副县长刘建军", "overlap_org": "逊克县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县长与副县长车福海", "overlap_org": "逊克县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县长与副县长矫志鹏（公安局长）", "overlap_org": "逊克县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县长与副县长宋振海", "overlap_org": "逊克县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县长与副县长孙东昭", "overlap_org": "逊克县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "县长与副县长郭丽娟", "overlap_org": "逊克县人民政府", "overlap_period": "current"},
    # 县委常委班子
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共逊克县委员会", "overlap_period": "current"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共逊克县委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共逊克县委员会", "overlap_period": "current"},
    # 县人大
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "县人大正副主任", "overlap_org": "逊克县人大常委会", "overlap_period": "current"},
    {"person_a": 11, "person_b": 13, "type": "overlap", "context": "县人大正副主任", "overlap_org": "逊克县人大常委会", "overlap_period": "current"},
    # 县委与人大
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委书记与人大主任", "overlap_org": "逊克县", "overlap_period": "current"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "县长与人大主任", "overlap_org": "逊克县", "overlap_period": "current"},
    # 政法系统
    {"person_a": 7, "person_b": 3, "type": "overlap", "context": "公安局长与常务副县长", "overlap_org": "逊克县人民政府", "overlap_period": "current"},
]


if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Build complete.")