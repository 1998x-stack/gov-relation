#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 金城江区 leadership network.

金城江区隶属广西壮族自治区河池市，是河池市市级党政机关驻地（市辖区），位于广西西北部、
云贵高原南麓、红水河中游，是滇黔桂联接华南区域的咽喉要冲，素有"桂西北门户"之称，面积
约2340平方公里，人口约35万，辖多个街道、乡镇。

Current (or recently current) leadership as of 2026-07/08 (sources: 河池市委组织部任前公示、
金城江发布/金城江融媒、广西县域经济网、新华网/河池纪检监察网、人民网广西、中国科学院大学等):
- 区委书记: 吴华勇（2026年起，主持区委会议；与贵港市覃塘区原区长吴华勇是否同一人存疑，
  详见 report 与 open_gaps.md）
- 区委副书记、区长: 徐宇列（原广西国资委规划发展与科技创新处处长，2025-09-18 代理区长，
	2026-07 区第六次党代会后为区委副书记、区长）

Biographical data sourced from official government pages, appointment notices (任前公示), and
mainstream media. Confidence marked per person and per claim (见 report 与 open_gaps.md)。
"""

import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]  # scripts/build -> repo root
# When run from staging (data/tmp/<task_id>/), parents[1] is not the repo root.
# Walk upward to locate the directory containing the gov_relation package.
for _parent in (Path(__file__).resolve().parents):
    if (_parent / "gov_relation" / "runner.py").exists():
        REPO_ROOT = _parent
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "金城江区"

# 构建入库（暂存）时通过 STAGING_DIR 覆盖；默认写入规范化目录
_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "金城江区_network.db")
    GEXF_PATH = os.path.join(_STAGING, "金城江区_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "金城江区_network.db"
    GEXF_PATH = GRAPH_DIR / "金城江区_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共河池市金城江区委员会", "type": "党委", "level": "市辖区", "parent": "中共河池市委", "location": "广西壮族自治区河池市金城江区"},
    {"id": 2, "name": "金城江区人民政府", "type": "政府", "level": "市辖区", "parent": "河池市人民政府", "location": "广西壮族自治区河池市金城江区"},
    {"id": 3, "name": "金城江区人民代表大会常务委员会", "type": "人大", "level": "市辖区", "parent": "河池市人大常委会", "location": "广西壮族自治区河池市金城江区"},
    {"id": 4, "name": "中国人民政治协商会议金城江区委员会", "type": "政协", "level": "市辖区", "parent": "政协河池市委员会", "location": "广西壮族自治区河池市金城江区"},
    {"id": 5, "name": "中共金城江区纪律检查委员会/金城江区监察委员会", "type": "纪委", "level": "市辖区", "parent": "中共河池市纪委", "location": "广西壮族自治区河池市金城江区"},
    {"id": 6, "name": "广西壮族自治区人民政府国有资产监督管理委员会", "type": "政府", "level": "正厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区南宁市"},
    {"id": 7, "name": "河池市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区河池市"},
    {"id": 8, "name": "中共贵港市覃塘区委员会", "type": "党委", "level": "市辖区", "parent": "中共贵港市委", "location": "广西壮族自治区贵港市覃塘区"},
    {"id": 9, "name": "贵港市覃塘区人民政府", "type": "政府", "level": "市辖区", "parent": "贵港市人民政府", "location": "广西壮族自治区贵港市覃塘区"},
    {"id": 10, "name": "中国科学院大学", "type": "事业单位", "level": "", "parent": "中国科学院", "location": "北京市"},
    {"id": 11, "name": "河池市大化瑶族自治县人民政府", "type": "政府", "level": "县处级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市大化县"},
    {"id": 12, "name": "靖西市人民政府", "type": "政府", "level": "县级市", "parent": "百色市人民政府", "location": "广西壮族自治区百色市靖西市"},
    {"id": 13, "name": "中共百色市靖西市委员会", "type": "党委", "level": "县级市", "parent": "中共百色市委", "location": "广西壮族自治区百色市靖西市"},
    {"id": 14, "name": "中国科学院上海应用物理研究所", "type": "事业单位", "level": "", "parent": "中国科学院", "location": "上海市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # ═══ 党委正职 ═══
    # 1 — 吴华勇 — 区委书记
    {"id": 1, "name": "吴华勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1983年2月（据贵港覃塘吴华勇）；疑同名，存疑", "birthplace": "广东省汕头市（据贵港覃塘吴华勇）；存疑",
     "education": "清华大学环境学院工学博士（据贵港覃塘吴华勇）；存疑",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共河池市金城江区委员会书记", "current_org": "中共河池市金城江区委员会",
     "source": "https://site.xxrb.com.cn/html/special/2026/0720/33116.html"},
    # ═══ 区政府 ═══
    # 2 — 徐宇列 — 区长
    {"id": 2, "name": "徐宇列", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "中国科学院大学无机化学专业理学博士（2015届）；中国科学院上海应用物理研究所硕士",
     "party_join": "中共党员", "work_start": "2015年7月（广西定向选调）",
     "current_post": "金城江区委副书记、区人民政府区长", "current_org": "金城江区人民政府",
     "source": "http://m.gxcounty.com/show-30-184066-0.html"},
    # ═══ 区委班子 ═══
    # 3 — 韦林浩 — 常委、政法委书记
    {"id": 3, "name": "韦林浩", "gender": "男", "ethnicity": "壮族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "金城江区委常委、政法委书记", "current_org": "中共河池市金城江区委员会",
     "source": "https://c.m.163.com/news/a/KVNUKC2E05568W0A.html"},
    # 4 唐增科 — 常委、区委办主任
    {"id": 4, "name": "唐增科", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "金城江区委常委、区委办公室主任", "current_org": "中共河池市金城江区委员会",
     "source": "https://www.163.com/dy/article/L2HJ1KEB05568W0A.html"},
    # ═══ 区人大/政协 ═══
    # 5 容祖浪 — 区人大常委会主任
    {"id": 5, "name": "容祖浪", "gender": "男", "ethnicity": "壮族",
     "birth": "1973年9月", "birthplace": "广西壮族自治区河池市",
     "education": "广西区委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "金城江区人大常委会主任", "current_org": "金城江区人民代表大会常务委员会",
     "source": "http://www.gxhc.gov.cn/"},
    # 6 蒙仕林 — 区政协主席
    {"id": 6, "name": "蒙仕林", "gender": "男", "ethnicity": "瑶族",
     "birth": "1972年12月", "birthplace": "广西壮族自治区河池市大化县",
     "education": "在职大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "金城江区政协主席", "current_org": "中国人民政治协商会议金城江区委员会",
     "source": "https://www.163.com/dy/article/L05FEASL05568W0A.html"},
    # ═══ 前任 ═══
    # 7 — 潘广军 — 前任区委书记
    {"id": 7, "name": "潘广军", "gender": "男", "ethnicity": "仫佬族",
     "birth": "1973年9月", "birthplace": "广西壮族自治区河池市罗城县",
     "education": "广西区委党校行政管理专业，在职研究生学历",
     "party_join": "1995年7月加入中国共产党", "work_start": "1991年7月参加工作",
     "current_post": "（曾任中共金城江区委员会书记，2021.07-约2025）", "current_org": "中共河池市金城江区委员会",
     "source": "http://www.gqxie.com/lyxw/14697.jhtml"},
    # 8 — 韦琪 — 前任区长（落马）
    {"id": 8, "name": "韦琪", "gender": "男", "ethnicity": "壮族",
     "birth": "1975年9月", "birthplace": "广西壮族自治区河池市南丹县",
     "education": "在职研究生学历，经济学学士",
     "party_join": "2001年4月加入中国共产党", "work_start": "",
     "current_post": "（2026年6月被纪律审查调查）", "current_org": "金城江区人民政府",
     "source": "https://www.gxjjw.gov.cn/staticpages/20260611/gxjjw6a2a77e7-204536.shtml"},
    # 9 — 覃生贤 — 前任区委书记（落马）
    {"id": 9, "name": "覃生贤", "gender": "男", "ethnicity": "壮族",
     "birth": "1969年5月", "birthplace": "广西壮族自治区河池市大化县",
     "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（2022年8月一审宣判，获刑十二年六个月）", "current_org": "中共河池市金城江区委员会",
     "source": "https://www.chinanews.com.cn/gn/2022/08-01/9816978.shtml"},
    # 10 — 刘永雄 — 前区委副书记 → 靖西市长（跨市交流）
    {"id": 10, "name": "刘永雄", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "广西壮族自治区",
     "education": "",
     "party_join": "中共党员", "work_start": "1999年7月参加工作（广西河池化工）",
     "current_post": "靖西市委副书记、市人民政府市长", "current_org": "靖西市人民政府",
     "source": "https://www.gxhc.gov.cn/"},
    # 11 韦晖 — 区委副书记（原，拟调任市直）
    {"id": 11, "name": "韦晖", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年8月", "birthplace": "广西壮族自治区河池市宜州区",
     "education": "研究生学历（农学硕士）",
     "party_join": "中共党员（2008年6月入党）", "work_start": "",
     "current_post": "金城江区委副书记、常务副区长（2026-02公示拟任市直正处级单位正职）", "current_org": "金城江区人民政府",
     "source": "http://gxcounty.com/zhengwu/rsrm/187546.html"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 吴华勇 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共河池市金城江区委员会书记", "start_date": "2026", "end_date": "present", "rank": "正处级", "note": "主持区委全面工作"},
    # 徐宇列 — 区长（兼区委副书记）
    {"person_id": 2, "org_id": 1, "title": "金城江区委副书记", "start_date": "2025-09", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "金城江区委副书记、区人民政府区长", "start_date": "2025-09-18", "end_date": "present", "rank": "正处级", "note": "代理区长，2026-06后正式确认"},
    {"person_id": 2, "org_id": 6, "title": "广西自治区国资委规划发展与科技创新处处长", "start_date": "2021-07", "end_date": "2025-09", "rank": "正处级", "note": "曾任处办公室副主任等"},
    {"person_id": 2, "org_id": 11, "title": "大化县人民政府副县长（挂职）", "start_date": "2019", "end_date": "", "rank": "", "note": "选调生基层挂职"},
    {"person_id": 2, "org_id": 14, "title": "中国科学院上海应用物理所硕士", "start_date": "", "end_date": "", "rank": "", "note": "理学硕士"},
    {"person_id": 2, "org_id": 10, "title": "中国科学院大学无机化学博士（2015届）", "start_date": "", "end_date": "2015-07", "rank": "", "note": "理学博士"},
    # 韦林浩 — 常委、政法委书记
    {"person_id": 3, "org_id": 1, "title": "金城江区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 唐增科 — 常委、办主任
    {"person_id": 4, "org_id": 1, "title": "金城江区委常委、区委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 容祖浪 — 区人大主任
    {"person_id": 5, "org_id": 3, "title": "金城江区人大常委会主任", "start_date": "2022", "end_date": "present", "rank": "正处级", "note": ""},
    # 蒙仕林 — 区政协主席
    {"person_id": 6, "org_id": 4, "title": "金城江区政协主席", "start_date": "2022", "end_date": "present", "rank": "正处级", "note": ""},
    # 潘广军 — 前任区委书记
    {"person_id": 7, "org_id": 1, "title": "中共金城江区委员会书记", "start_date": "2021-07", "end_date": "2025", "rank": "正处级", "note": ""},
    # 韦琪 — 前任区长
    {"person_id": 8, "org_id": 2, "title": "金城江区人民政府区长", "start_date": "2021", "end_date": "2025", "rank": "正处级", "note": "2026年6月被查"},
    # 覃生贤 — 前任区委书记
    {"person_id": 9, "org_id": 1, "title": "中共金城江区委员会书记", "start_date": "2012", "end_date": "2021", "rank": "正处级", "note": "2022年判刑"},
    # 刘永雄 — 跨市交流
    {"person_id": 10, "org_id": 1, "title": "金城江区委副书记", "start_date": "2021", "end_date": "2023-09", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 13, "title": "靖西市委副书记、代理市长", "start_date": "2023-09", "end_date": "2023-10", "rank": "正处级", "note": ""},
    {"person_id": 10, "org_id": 12, "title": "靖西市委副书记、市人民政府市长", "start_date": "2023-10", "end_date": "present", "rank": "正处级", "note": ""},
    # 韦晖 — 原副书记/常务副区长
    {"person_id": 11, "org_id": 1, "title": "金城江区委副书记", "start_date": "", "end_date": "2026", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "金城江区人民政府常务副区长", "start_date": "", "end_date": "2026", "rank": "副处级", "note": "2026-02公示拟任市直正处级单位正职"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "金城江区党政正职搭档：区委书记吴华勇与区长徐宇列", "overlap_org": "中共金城江区委员会/金城江区人民政府", "overlap_period": "2025-至今"},
    # 区委班子
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与区委常委、政法委书记韦林波", "overlap_org": "中共金城江区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与区委办主任唐增科", "overlap_org": "中共金城江区委员会", "overlap_period": "current"},
    # 区长与班子
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "区长徐宇列与政法委书记韦林波", "overlap_org": "金城江区", "overlap_period": "current"},
    # 区人大/政协
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委书记与区人大常委会主任容祖浪", "overlap_org": "金城江区", "overlap_period": "current"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区委书记与区政协主席蒙仕林", "overlap_org": "金城江区", "overlap_period": "current"},
    # 前任/继任
    {"person_a": 1, "person_b": 7, "type": "predecessor_successor", "context": "吴华勇接任潘广军任区委书记", "overlap_org": "中共金城江区委员会", "overlap_period": "2026"},
    {"person_a": 7, "person_b": 9, "type": "predecessor_successor", "context": "潘广军接任覃生贤任区委书记", "overlap_org": "中共金城江区委员会", "overlap_period": "2021"},
    {"person_a": 2, "person_b": 8, "type": "predecessor_successor", "context": "徐宇列接任韦琪任区长", "overlap_org": "金城江区人民政府", "overlap_period": "2025"},
    # 前任书记与前任区长
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "潘广军任书记、韦琪任区长期间党政共治", "overlap_org": "金城江区", "overlap_period": "2021-2025"},
    # 跨市交流
    {"person_a": 10, "person_b": 1, "type": "overlap", "context": "刘永雄任区委副书记，吴华勇任区委书记", "overlap_org": "中共金城江区委员会", "overlap_period": "2021-2023"},
    {"person_a": 10, "person_b": 2, "type": "overlap", "context": "刘永雄任区委副书记期间，后跨市调任靖西市长", "overlap_org": "金城江区", "overlap_period": "2021-2023"},
    # 纪检监督关系（前任区长落马）
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "覃生贤、韦琪两任落马干部先后被查处（监督信号）", "overlap_org": "广西纪检监察系统", "overlap_period": "2022-2026"},
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