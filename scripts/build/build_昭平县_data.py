#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 昭平县 leadership network.

昭平县隶属广西壮族自治区贺州市，位于广西东部、桂江中游，县域面积3224平方公里，
人口约45万，辖9镇3乡。为国家乡村振兴重点帮扶县、国家生态文明建设示范县，
"山清水秀生态美、镇古茶香人长寿"，森林覆盖率约82%。

Current leadership as of 2025-2026 (sources: 贺州市委组织部任前公示、广西县域经济网、
贺州市文化和旅游局领导介绍页、昭平在线 news 等):
- 县委书记: 邹红英（2024.02 起）
- 县委副书记、县长: 周强

Biographical data sourced from official government pages, appointment notices (任前公示),
and mainstream media. Confidence marked per person (见 report 与 open_gaps.md)。
"""

import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]  # scripts/build -> repo root
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "昭平县"

# 构建入库（暂存）时通过 STAGING_DIR 覆盖；默认写入规范化目录
_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "昭平县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "昭平县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "昭平县_network.db"
    GEXF_PATH = GRAPH_DIR / "昭平县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共昭平县委员会", "type": "党委", "level": "县处级", "parent": "中共贺州市委", "location": "广西壮族自治区贺州市昭平县"},
    {"id": 2, "name": "昭平县人民政府", "type": "政府", "level": "县处级", "parent": "贺州市人民政府", "location": "广西壮族自治区贺州市昭平县"},
    {"id": 3, "name": "昭平县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "贺州市人大常委会", "location": "广西壮族自治区贺州市昭平县"},
    {"id": 4, "name": "中国人民政治协商会议昭平县委员会", "type": "政协", "level": "县处级", "parent": "政协贺州市委员会", "location": "广西壮族自治区贺州市昭平县"},
    {"id": 5, "name": "中共昭平县纪律检查委员会/昭平县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共贺州市纪委", "location": "广西壮族自治区贺州市昭平县"},
    {"id": 6, "name": "贺州市文化和旅游局", "type": "政府", "level": "地厅级", "parent": "贺州市人民政府", "location": "广西壮族自治区贺州市"},
    {"id": 7, "name": "中共贺州市八步区委员会", "type": "党委", "level": "县处级", "parent": "中共贺州市委", "location": "广西壮族自治区贺州市八步区"},
    {"id": 8, "name": "共青团兴安县委员会", "type": "群团", "level": "县处级", "parent": "共青团广西区委", "location": "广西壮族自治区桂林市兴安县"},
    {"id": 9, "name": "贺州市档案局(馆)", "type": "政府", "level": "县处级", "parent": "贺州市人民政府", "location": "广西壮族自治区贺州市"},
    {"id": 10, "name": "贺州市旅游发展委员会", "type": "政府", "level": "地厅级", "parent": "贺州市人民政府", "location": "广西壮族自治区贺州市"},
    {"id": 11, "name": "贺州市政协", "type": "政协", "level": "地厅级", "parent": "广西壮族自治区政协", "location": "广西壮族自治区贺州市"},
    {"id": 12, "name": "贺州市政府办公室", "type": "政府", "level": "地厅级", "parent": "贺州市人民政府", "location": "广西壮族自治区贺州市"},
    {"id": 13, "name": "贺州交通投资集团有限公司", "type": "国企", "level": "县处级", "parent": "贺州市人民政府", "location": "广西壮族自治区贺州市"},
    {"id": 14, "name": "中共肇庆市鼎湖区委员会", "type": "党委", "level": "县处级", "parent": "中共肇庆市委", "location": "广东省肇庆市鼎湖区"},
    {"id": 15, "name": "广东省梅州市旅游局", "type": "政府", "level": "地厅级", "parent": "梅州市人民政府", "location": "广东省梅州市"},
    {"id": 16, "name": "贺州市平桂区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "贺州市人大常委会", "location": "广西壮族自治区贺州市平桂区"},
    {"id": 17, "name": "贺州市供销合作社联社", "type": "事业单位", "level": "县处级", "parent": "贺州市人民政府", "location": "广西壮族自治区贺州市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # ═══ 党委正职 ═══
    # 1 — 邹红英 — 县委书记
    {"id": 1, "name": "邹红英", "gender": "女", "ethnicity": "瑶族",
     "birth": "1978年3月", "birthplace": "广西壮族自治区桂林市资源县",
     "education": "在职研究生学历（桂林理工大学思想政治教育专业），政工师",
     "party_join": "1999年8月加入中国共产党", "work_start": "1996年11月参加工作",
     "current_post": "中共昭平县委书记（一级调研员）", "current_org": "中共昭平县委员会",
     "source": "http://m.gxcounty.com/show-30-181316-0.html"},
    # 2 — 周强 — 县长
    {"id": 2, "name": "周强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "昭平县委副书记、县人民政府县长", "current_org": "昭平县人民政府",
     "source": "https://baike.baidu.com/item/%E5%91%A8%E5%BC%BA/65525841"},
    # ═══ 县委/县政府班子 ═══
    # 3 — 马攀 — 县委副书记
    {"id": 3, "name": "马攀", "gender": "男", "ethnicity": "汉族",
     "birth": "1983年12月", "birthplace": "安徽省淮南市",
     "education": "中国农业大学农学与生物技术学院种子科学专业研究生学历，农学博士",
     "party_join": "2007年12月加入中国共产党", "work_start": "2013年7月参加工作",
     "current_post": "昭平县委副书记", "current_org": "中共昭平县委员会",
     "source": "https://www.newton.com.tw/wiki/%E9%A6%AC%E6%94%80/8080330"},
    # 4 — 刘启哲 — 县委常委、常务副县长
    {"id": 4, "name": "刘启哲", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "昭平县委常委、县政府党组副书记、副县长（常务）", "current_org": "昭平县人民政府",
     "source": "https://www.newton.com.tw/wiki/%E5%8A%89%E5%95%9F%E5%93%B2/61946786"},
    # 5 — 尹洁 — 县委常委、挂职副县长
    {"id": 5, "name": "尹洁", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "内蒙古工业大学工商管理专业毕业（管理学硕士）",
     "party_join": "中共党员", "work_start": "",
     "current_post": "昭平县委常委、县政府党组成员、副县长（挂职）", "current_org": "昭平县人民政府",
     "source": "https://www.newton.com.tw/wiki/%E5%B0%B8%E6%B4%81"},
    # 6 — 唐少云 — 副县长
    {"id": 6, "name": "唐少云", "gender": "男", "ethnicity": "汉族",
     "birth": "1990年（九零后）", "birthplace": "",
     "education": "华中科技大学毕业",
     "party_join": "中共党员", "work_start": "2012年选调生",
     "current_post": "昭平县人民政府副县长", "current_org": "昭平县人民政府",
     "source": "https://www.jfdaily.com/wx/detail.do?id=832145"},
    # 7 — 钟光柱 — 县纪委书记/监委主任（2023-2025）
    {"id": 7, "name": "钟光柱", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年9月", "birthplace": "广西壮族自治区贺州市钟山县",
     "education": "北京林业大学会计学专业（函授）",
     "party_join": "2003年6月加入中国共产党", "work_start": "1999年7月参加工作",
     "current_post": "贺州市平桂区人大常委会副主任（提名，2025.12起）", "current_org": "贺州市平桂区人民代表大会常务委员会",
     "source": "http://m.gxcounty.com/show-30-184488-0.html"},
    # 8 — 吴伟红 — 县人大常委会主任
    {"id": 8, "name": "吴伟红", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "昭平县人大常委会主任", "current_org": "昭平县人民代表大会常务委员会",
     "source": "http://www.zpol.cn/zx/zpxw/content_233167"},
    # 9 — 张贤才 — 县政协主席
    {"id": 9, "name": "张贤才", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "昭平县政协主席", "current_org": "中国人民政治协商会议昭平县委员会",
     "source": "http://www.zpol.cn/zx/zpxw/content_233167"},
    # ═══ 前任 ═══
    # 10 — 刘飞国 — 前任县委书记
    {"id": 10, "name": "刘飞国", "gender": "男", "ethnicity": "汉族",
     "birth": "1974年1月", "birthplace": "广西壮族自治区玉林市容县",
     "education": "中央党校在职大学学历；广西区党校在职研究生班经济管理专业",
     "party_join": "1996年8月加入中国共产党", "work_start": "1991年7月参加工作",
     "current_post": "贺州市政协党组成员、秘书长（2024.02起）", "current_org": "贺州市政协",
     "source": "http://m.gxcounty.com/show-30-181326-0.html"},
    # 11 — 邓忠耀 — 前任县长（落马）
    {"id": 11, "name": "邓忠耀", "gender": "男", "ethnicity": "瑶族",
     "birth": "1976年11月", "birthplace": "广西壮族自治区贺州市富川瑶族自治县",
     "education": "广西区委党校研究生学历",
     "party_join": "1998年1月加入中国共产党", "work_start": "",
     "current_post": "（2025年4月辞职后被查）", "current_org": "贺州市供销合作社联社",
     "source": "https://www.thepaper.cn/newsDetail_forward_30638808"},
    # 12 — 邓少华 — 前任县长
    {"id": 12, "name": "邓少华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任昭平县人民政府县长，2015-2021）", "current_org": "昭平县人民政府",
     "source": "https://baike.so.com/doc/1813079-24412348.html"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 邹红英 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共昭平县委书记", "start_date": "2024-02", "end_date": "present", "rank": "正处级", "note": "主持县委全面工作，一级调研员"},
    # 周强 — 县长（兼县委副书记）
    {"person_id": 2, "org_id": 1, "title": "昭平县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "昭平县人民政府县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持县政府全面工作"},
    # 马攀 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "昭平县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "昭平县政府副县长", "start_date": "2016-05", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 14, "title": "广东肇庆市鼎湖区委常委、副区长（挂职）", "start_date": "2018-02", "end_date": "", "rank": "", "note": "粤桂协作挂职交流"},
    # 刘启哲 — 常务副县长
    {"person_id": 4, "org_id": 1, "title": "昭平县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "昭平县政府党组副书记、副县长（常务）", "start_date": "2023-12", "end_date": "present", "rank": "副处级", "note": "县政府常务工作"},
    # 尹洁 — 挂职副县长
    {"person_id": 5, "org_id": 1, "title": "昭平县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "昭平县人民政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "", "note": "央企定点帮扶挂职、任期二年"},
    # 唐少云 — 副县长
    {"person_id": 6, "org_id": 2, "title": "昭平县人民政府副县长", "start_date": "2023-12", "end_date": "present", "rank": "副处级", "note": "曾任走马镇党委书记"},
    # 钟光柱 — 纪委书记（已调离）
    {"person_id": 7, "org_id": 5, "title": "昭平县委常委、县纪委书记、县监委主任", "start_date": "2023-09", "end_date": "2025-09", "rank": "副处级", "note": "四级高级监察官"},
    {"person_id": 7, "org_id": 16, "title": "贺州市平桂区人大常委会副主任", "start_date": "2025-12", "end_date": "present", "rank": "副处级", "note": ""},
    # 吴伟红 — 人大主任
    {"person_id": 8, "org_id": 3, "title": "昭平县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 张贤才 — 政协主席
    {"person_id": 9, "org_id": 4, "title": "昭平县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 刘飞国
    {"person_id": 10, "org_id": 1, "title": "中共昭平县委书记（一级调研员）", "start_date": "2018-09", "end_date": "2024-02", "rank": "正处级", "note": ""},
    {"person_id": 10, "org_id": 12, "title": "贺州市政府党组成员、秘书长、办公室党组书记、主任", "start_date": "2016-06", "end_date": "2018-09", "rank": "正处级", "note": ""},
    {"person_id": 10, "org_id": 11, "title": "贺州市政协党组成员、秘书长", "start_date": "2024-02", "end_date": "present", "rank": "正处级", "note": ""},
    # 邓忠耀
    {"person_id": 11, "org_id": 2, "title": "昭平县人民政府县长", "start_date": "2021-09", "end_date": "2025-04", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 13, "title": "贺州交通投资集团有限公司党委书记、董事长", "start_date": "", "end_date": "2021-09", "rank": "", "note": ""},
    {"person_id": 11, "org_id": 12, "title": "贺州市人民政府副秘书长（正处长级）", "start_date": "", "end_date": "", "rank": "", "note": "办公室副主任、应急管理办主任"},
    {"person_id": 11, "org_id": 17, "title": "贺州市供销合作社联社一级调研员", "start_date": "2025-04", "end_date": "", "rank": "正处级", "note": "辞职后调任，随即被查"},
    # 邓少华
    {"person_id": 12, "org_id": 2, "title": "昭平县人民政府县长", "start_date": "2015", "end_date": "2021", "rank": "正处级", "note": "2016年9月当选"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "昭平县党政正职搭档：县委书记与县长", "overlap_org": "中共昭平县委员会/昭平县人民政府", "overlap_period": "2024-至今"},
    # 县委班子
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与县委副书记马攀同届共事", "overlap_org": "中共昭平县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与县委常委、常务副县长刘启哲", "overlap_org": "中共昭平县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记与挂职县委常委尹洁", "overlap_org": "中共昭平县委员会", "overlap_period": "current"},
    # 县长与班子
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与县委副书记马攀", "overlap_org": "中共昭平县委员会", "overlap_period": "current"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长与常务副县长刘启哲", "overlap_org": "昭平县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县长与副县长唐少云", "overlap_org": "昭平县人民政府", "overlap_period": "current"},
    # 前前任县长落马 / 书记交接
    {"person_a": 11, "person_b": 2, "type": "predecessor_successor", "context": "邓忠耀卸任后由周强接任县长", "overlap_org": "昭平县人民政府", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "邹红英接任刘飞国任县委书记", "overlap_org": "中共昭平县委员会", "overlap_period": "2024"},
    # 前任书记与前任县长曾共事
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "刘飞国任书记期间邓忠耀任县长，党政共治", "overlap_org": "中共昭平县委员会/昭平县人民政府", "overlap_period": "2021-2022"},
    {"person_a": 12, "person_b": 11, "type": "predecessor_successor", "context": "邓少华卸任后由邓忠耀继任县长", "overlap_org": "昭平县人民政府", "overlap_period": "2021"},
    # 人大/政协与县委
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记与县人大常委会主任", "overlap_org": "昭平县", "overlap_period": "current"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记与县政协主席", "overlap_org": "昭平县", "overlap_period": "current"},
    # 纪检与落马县长
    {"person_a": 7, "person_b": 11, "type": "overlap", "context": "钟光柱任纪委书记期间邓忠耀被查（监督关系）", "overlap_org": "昭平县纪委监委/昭平县人民政府", "overlap_period": "2023-2025"},
    # 跨区域挂职/东融交流
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "马攀挂职肇庆鼎湖、尹洁央企挂职，跨省/央企干部交流", "overlap_org": "粤桂协作挂职通道", "overlap_period": "current"},
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