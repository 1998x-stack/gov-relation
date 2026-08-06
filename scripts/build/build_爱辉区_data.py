#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 爱辉区 leadership network.

爱辉区隶属黑龙江省黑河市，是黑河市唯一的市辖区、市行政中心所在地。
北邻俄罗斯，是全国边境县区之一。下辖4街道、3镇、5乡、3民族乡，
第七次人口普查常住人口22.38万人。

Current leadership as of 2026-08 (source: www.aihui.gov.cn 爱辉区人民政府官网):
- 区委书记: 宋秋田
- 区长: 赵中南
- 常务副区长(区委常委): 祝军
- 区委常委、副区长: 李蕙、袁星野；副区长: 崔永均、李祥龙、韩易晓、赵久、周海洋、冯冠琳
"""

import sqlite3
import sys
from pathlib import Path

# Resolve the repo root that owns the gov_relation package, independent of script location
_REPO_ROOT = Path(__file__).resolve().parents[2]
if not (_REPO_ROOT / "gov_relation").is_dir():
    _p = Path(__file__).resolve().parent
    while _p != _p.parent and not (_p / "gov_relation").is_dir():
        _p = _p.parent
    _REPO_ROOT = _p
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "爱辉区"
DB_PATH = DATABASE_DIR / "爱辉区_network.db"
GEXF_PATH = GRAPH_DIR / "爱辉区_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共黑河市爱辉区委员会", "type": "党委", "level": "县处级", "parent": "中共黑河市委", "location": "黑龙江省黑河市爱辉区"},
    {"id": 2, "name": "爱辉区人民政府", "type": "政府", "level": "县处级", "parent": "黑河市人民政府", "location": "黑龙江省黑河市爱辉区"},
    {"id": 3, "name": "爱辉区人大常委会", "type": "人大", "level": "县处级", "parent": "黑河市人大常委会", "location": "黑龙江省黑河市爱辉区"},
    {"id": 4, "name": "中国人民政治协商会议爱辉区委员会", "type": "政协", "level": "县处级", "parent": "政协黑河市委员会", "location": "黑龙江省黑河市爱辉区"},
    {"id": 5, "name": "中共爱辉区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共黑河市纪委", "location": "黑龙江省黑河市爱辉区"},
    {"id": 6, "name": "黑河市公安局爱辉分局", "type": "政府", "level": "县处级", "parent": "爱辉区人民政府", "location": "黑龙江省黑河市爱辉区"},
    {"id": 7, "name": "逊克县人民政府", "type": "政府", "level": "县处级", "parent": "黑河市人民政府", "location": "黑龙江省黑河市逊克县"},
    {"id": 8, "name": "中共逊克县委员会", "type": "党委", "level": "县处级", "parent": "中共黑河市委", "location": "黑龙江省黑河市逊克县"},
    {"id": 9, "name": "黑河市农业农村局", "type": "政府", "level": "县处级", "parent": "黑河市人民政府", "location": "黑龙江省黑河市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────

persons = [
    # ═══ 区委主要领导 ═══
    # 1 — 宋秋田 — 区委书记
    {"id": 1, "name": "宋秋田", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年2月", "birthplace": "黑龙江省望奎县", "education": "研究生学历(省委党校)",
     "party_join": "中共党员", "work_start": "2000年9月",
     "current_post": "爱辉区委书记", "current_org": "中共黑河市爱辉区委员会",
     "source": "http://www.aihui.gov.cn/ahq/c101037/202607/c11_357332.shtml"},
    # 2 — 赵中南 — 区长
    {"id": 2, "name": "赵中南", "gender": "男", "ethnicity": "锡伯族",
     "birth": "1984年11月", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "爱辉区委副书记、政府区长", "current_org": "爱辉区人民政府",
     "source": "http://www.aihui.gov.cn/ahq/c100852/qld.shtml"},
    # 3 — 祝军 — 常务副区长(区委常委)
    {"id": 3, "name": "祝军", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年10月", "birthplace": "", "education": "大学本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "爱辉区委常委、常务副区长", "current_org": "爱辉区人民政府",
     "source": "http://www.aihui.gov.cn/ahq/c100753/202409/c11_303688.shtml"},
    # 4 — 李蕙 — 区委常委、副区长
    {"id": 4, "name": "李蕙", "gender": "女", "ethnicity": "汉族",
     "birth": "1984年4月", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "爱辉区委常委、副区长", "current_org": "爱辉区人民政府",
     "source": "http://www.aihui.gov.cn/ahq/c100753/202505/c11_328585.shtml"},
    # 5 — 袁星野 — 区委常委、副区长
    {"id": 5, "name": "袁星野", "gender": "男", "ethnicity": "汉族",
     "birth": "1990年8月", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "爱辉区委常委、副区长", "current_org": "爱辉区人民政府",
     "source": "http://www.aihui.gov.cn/ahq/c100753/202508/c11_337478.shtml"},
    # 6 — 崔永均 — 副区长
    {"id": 6, "name": "崔永均", "gender": "男", "ethnicity": "汉族",
     "birth": "1973年5月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "爱辉区政府副区长", "current_org": "爱辉区人民政府",
     "source": "http://www.aihui.gov.cn/ahq/c100753/202308/c11_259236.shtml"},
    # 7 — 李祥龙 — 副区长
    {"id": 7, "name": "李祥龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年12月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "爱辉区政府副区长", "current_org": "爱辉区人民政府",
     "source": "http://www.aihui.gov.cn/ahq/c100753/202603/c11_349661.shtml"},
    # 8 — 韩易晓 — 副区长 (名录确认, 履历待查)
    {"id": 8, "name": "韩易晓", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "爱辉区政府副区长", "current_org": "爱辉区人民政府",
     "source": "http://www.aihui.gov.cn/ahq/c100751/szf.shtml"},
    # 9 — 赵久 — 副区长 (名录确认, 履历待查)
    {"id": 9, "name": "赵久", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "爱辉区政府副区长", "current_org": "爱辉区人民政府",
     "source": "http://www.aihui.gov.cn/ahq/c100751/szf.shtml"},
    # 10 — 周海洋 — 副区长 (名录确认, 履历待查)
    {"id": 10, "name": "周海洋", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "爱辉区政府副区长", "current_org": "爱辉区人民政府",
     "source": "http://www.aihui.gov.cn/ahq/c100751/szf.shtml"},
    # 11 — 冯冠琳 — 副区长 (名录确认, 履历待查)
    {"id": 11, "name": "冯冠琳", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "爱辉区政府副区长", "current_org": "爱辉区人民政府",
     "source": "http://www.aihui.gov.cn/ahq/c100751/szf.shtml"},
    # 12 — 宋秋田 (逊克县履历补充) — 逊克县副县长任上
    # 用 id 1 补任职, 不再另建 person。
]

# ── POSITIONS ──────────────────────────────────────────────────────

positions = [
    # 宋秋田 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "爱辉区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持区委全面工作"},
    # 宋秋田 早年逊克县履历
    {"person_id": 1, "org_id": 8, "title": "逊克县政府副县长", "start_date": "2018", "end_date": "", "rank": "县处级副职", "note": "2018年起任逊克县副县长, 后调爱辉"},

    # 赵中南 — 区长
    {"person_id": 2, "org_id": 1, "title": "爱辉区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "爱辉区政府区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持区政府全面工作, 主管胜山国家级自然保护区服务中心、区审计局"},
    # 赵中南 早年履历
    {"person_id": 2, "org_id": 9, "title": "黑河市农业农村局副局长", "start_date": "", "end_date": "2022-12", "rank": "县处级副职", "note": "2022-12-08免职"},
    {"person_id": 2, "org_id": 7, "title": "逊克县政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分管农业农村、水务、供销社"},

    # 祝军 — 常务副区长
    {"person_id": 3, "org_id": 1, "title": "爱辉区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "爱辉区政府常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责财政金融、人社、安全生产、信访稳定、医疗保障"},

    # 李蕙 — 区委常委、副区长
    {"person_id": 4, "org_id": 1, "title": "爱辉区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "爱辉区政府副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责综合经济、工业、对外经济合作、园区建设"},

    # 袁星野 — 区委常委、副区长
    {"person_id": 5, "org_id": 1, "title": "爱辉区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "爱辉区政府副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责商务、科技、外事"},

    # 崔永均 — 副区长
    {"person_id": 6, "org_id": 2, "title": "爱辉区政府副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责公共安全、司法法制、公安/司法局"},
    {"person_id": 6, "org_id": 6, "title": "黑河市公安局爱辉分局分管领导", "start_date": "", "end_date": "present", "rank": "", "note": "分管市公安局爱辉分局"},

    # 李祥龙 — 副区长
    {"person_id": 7, "org_id": 2, "title": "爱辉区政府副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责农业农村、水务、乡村振兴、供销社"},

    # 名录确认的副区长
    {"person_id": 8, "org_id": 2, "title": "爱辉区政府副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "韩易晓"},
    {"person_id": 9, "org_id": 2, "title": "爱辉区政府副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "赵久"},
    {"person_id": 10, "org_id": 2, "title": "爱辉区政府副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "周海洋"},
    {"person_id": 11, "org_id": 2, "title": "爱辉区政府副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "冯冠琳"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────

relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "爱辉区党政正职搭档: 区委书记与区长", "overlap_org": "中共爱辉区委员会/爱辉区人民政府", "overlap_period": "current"},
    # 逊克县时期工作交集 — 宋秋田(2018起副县长) 与 赵中南(副县长/农业) 曾在逊克县政府班子同期
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "两人此前均在逊克县政府任副县长", "overlap_org": "逊克县人民政府", "overlap_period": "约2018前后"},
    # 区委书记与区委常委班子
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与区委常委、常务副区长", "overlap_org": "中共爱辉区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与区委常委、副区长李蕙", "overlap_org": "中共爱辉区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委书记与区委常委、副区长袁星野", "overlap_org": "中共爱辉区委员会", "overlap_period": "current"},
    # 区长与副区长
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "区长与常务副区长祝军", "overlap_org": "爱辉区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "区长与副区长李蕙", "overlap_org": "爱辉区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "区长与副区长袁星野", "overlap_org": "爱辉区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "区长与副区长崔永均", "overlap_org": "爱辉区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "区长与副区长李祥龙", "overlap_org": "爱辉区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "区长与副区长韩易晓", "overlap_org": "爱辉区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "区长与副区长赵久", "overlap_org": "爱辉区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "区长与副区长周海洋", "overlap_org": "爱辉区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "区长与副区长冯冠琳", "overlap_org": "爱辉区人民政府", "overlap_period": "current"},
    # 区委常委班子内部
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "区委常委班子成员", "overlap_org": "中共爱辉区委员会", "overlap_period": "current"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "区委常委班子成员", "overlap_org": "中共爱辉区委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "区委常委班子成员", "overlap_org": "中共爱辉区委员会", "overlap_period": "current"},
    # 政法委线口 (副区长崔永均分管公安/司法)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区委书记与分管政法副区长", "overlap_org": "中共爱辉区委员会", "overlap_period": "current"},
    # 先进的关系: 区长与分管政法副区长
    {"person_a": 6, "person_b": 3, "type": "overlap", "context": "政法线口与常务副区长", "overlap_org": "爱辉区人民政府", "overlap_period": "current"},
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