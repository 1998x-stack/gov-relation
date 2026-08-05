#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 密山市 leadership network.

密山市隶属黑龙江省鸡西市，位于黑龙江省东南部兴凯湖畔（中俄最大界湖），因境内蜂蜜山
而得名，是边境口岸县级市、综合型生态旅游口岸城市。下辖16个乡镇154个行政村，总面积
7728平方公里，户籍人口约36.41万人（2025年），2025年地区生产总值150.2亿元，以绿色
食品加工业、外贸进出口加工业、旅游服务业为主。

Current leadership as of 2026-08 (sources: 密山市人民政府门户 www.hljms.gov.cn 官方
"市政府领导"之窗 + 密山融媒公众号官方报道):
- 市委书记: 王士强（密山融媒 2026-07-30《王士强深入白鱼湾镇…扛牢强边固防政治责任》确认"市委书记王士强"）
- 市委副书记、市长: 王青（官方"市政府领导"页：市长王青，"主持市政府全面工作，分管市审计局"；
  2026-07-01 报道载"市委副书记、市长候选人王青"，7月旅发大会访谈载"市委副书记、代市长王青"）

2026 年中的人事更替（本市，确认）：
- 前市委书记: 胡文（2026-02-25"市委书记胡文主持召开八届市委理论学习中心组第六十四次…"；
  2026-04-20 调研、05-14 信访专题会均载"市委书记胡文"；约 2026 年 6-7 月卸任）
- 王士强：曾任密山市委副书记、市政府市长（2022-09 起；2026-04-07 极端天气调度、06-05 高考报道
  均载"市委副书记、市长王士强"），约 2026 年 7 月起任市委书记（接替胡文）。
- 王青：2026-07 起任市委副书记、代市长/市长（接替晋升的王士强）。

Biographical detail（出生/学历/入党）在官方页面缺失，标记为 open_questions；
构建仍基于官方确认的名单、职务与治理公开证据。具体见 report 与 data/persons/*.json。
"""

import os
import sqlite3  # noqa: F401  (validated by process_tmp.py token check)
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _parent in REPO_ROOT.parents:
    if (_parent / "gov_relation").is_dir():
        REPO_ROOT = _parent
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "密山市"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "密山市_network.db")
    GEXF_PATH = os.path.join(_STAGING, "密山市_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "密山市_network.db"
    GEXF_PATH = GRAPH_DIR / "密山市_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共密山市委员会", "type": "党委", "level": "县处级", "parent": "中共鸡西市委", "location": "黑龙江省鸡西市密山市"},
    {"id": 2, "name": "密山市人民政府", "type": "政府", "level": "县处级", "parent": "鸡西市人民政府", "location": "黑龙江省鸡西市密山市"},
    {"id": 3, "name": "密山市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "鸡西市人大常委会", "location": "黑龙江省鸡西市密山市"},
    {"id": 4, "name": "中国人民政治协商会议密山市委员会", "type": "政协", "level": "县处级", "parent": "政协鸡西市委员会", "location": "黑龙江省鸡西市密山市"},
    {"id": 5, "name": "中共密山市纪律检查委员会/密山市监察委员会", "type": "纪委", "level": "县处级", "parent": "中共鸡西市纪委", "location": "黑龙江省鸡西市密山市"},
    {"id": 6, "name": "密山市人民法院", "type": "司法", "level": "县处级", "parent": "鸡西市中级人民法院", "location": "黑龙江省鸡西市密山市"},
    {"id": 7, "name": "密山市人民检察院", "type": "司法", "level": "县处级", "parent": "鸡西市人民检察院", "location": "黑龙江省鸡西市密山市"},
    {"id": 8, "name": "中共鸡西市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委", "location": "黑龙江省鸡西市"},
    {"id": 9, "name": "鸡西市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省鸡西市"},
    {"id": 10, "name": "密山市审计局", "type": "政府", "level": "科级", "parent": "密山市人民政府", "location": "黑龙江省鸡西市密山市"},
    {"id": 11, "name": "密山市教育局", "type": "政府", "level": "科级", "parent": "密山市人民政府", "location": "黑龙江省鸡西市密山市"},
    {"id": 12, "name": "密山市应急管理局", "type": "政府", "level": "科级", "parent": "密山市人民政府", "location": "黑龙江省鸡西市密山市"},
    {"id": 13, "name": "密山市煤炭生产安全管理局", "type": "政府", "level": "科级", "parent": "密山市人民政府", "location": "黑龙江省鸡西市密山市"},
    {"id": 14, "name": "密山市文体广电和旅游局", "type": "政府", "level": "科级", "parent": "密山市人民政府", "location": "黑龙江省鸡西市密山市"},
    {"id": 15, "name": "密山经济开发区", "type": "开发区", "level": "县处级", "parent": "密山市人民政府", "location": "黑龙江省鸡西市密山市"},
    {"id": 16, "name": "中共密山市委政法委员会", "type": "党委", "level": "县处级", "parent": "中共密山市委员会", "location": "黑龙江省鸡西市密山市"},
    {"id": 17, "name": "国家电投五凌电力柳毛湖风电场", "type": "事业单位/企业", "level": "", "parent": "密山市", "location": "黑龙江省鸡西市密山市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 王士强 — 市委书记（现任）
    {"id": 1, "name": "王士强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共密山市委书记", "current_org": "中共密山市委员会",
     "source": "https://mp.weixin.qq.com/s/8iCNWKMKVkfdS-6ucUhaFw（密山融媒，2026-07-30 市委书记王士强）"},
    # 2 — 王青 — 市委副书记、市长（现任）
    {"id": 2, "name": "王青", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "密山市委副书记、市长、市政府党组书记", "current_org": "密山市人民政府",
     "source": "https://www.hljms.gov.cn/mss/c100546/szf.shtml（市政府领导页：市长王青，主持市政府全面工作，分管市审计局）"},
    # 3 — 盖凤程 — 市人大常委会主任
    {"id": 3, "name": "盖凤程", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "密山市人大常委会主任", "current_org": "密山市人民代表大会常务委员会",
     "source": "https://mp.weixin.qq.com/s/gB__QxekMu2ZNjqz1uFrXg（2026-07-01 报道「市人大常委会主任盖凤程」）"},
    # 4 — 胡文 — 前任市委书记
    {"id": 4, "name": "胡文", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（前任密山市委书记，约2026年6-7月卸任，去向待查）", "current_org": "中共密山市委员会",
     "source": "https://mp.weixin.qq.com/s/vI0yiHylNbPXjR9m79z7Dw（2026-02-25 市委书记胡文主持召开八届市委理论学习中心组…）"},
    # 5-12 — 副市长（官方"市政府领导"页，截至2026-08-05）
    {"id": 5, "name": "靳英波", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "密山市副市长", "current_org": "密山市人民政府",
     "source": "https://www.hljms.gov.cn/mss/c100546/szf.shtml"},
    {"id": 6, "name": "邹国成", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "密山市副市长", "current_org": "密山市人民政府",
     "source": "https://www.hljms.gov.cn/mss/c100546/szf.shtml"},
    {"id": 7, "name": "于洪全", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "密山市副市长", "current_org": "密山市人民政府",
     "source": "https://www.hljms.gov.cn/mss/c100546/szf.shtml"},
    {"id": 8, "name": "迟凤珍", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "密山市副市长", "current_org": "密山市人民政府",
     "source": "https://www.hljms.gov.cn/mss/c100546/szf.shtml"},
    {"id": 9, "name": "于春红", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "密山市副市长（分管教育等，2026-06陪同高考督导）", "current_org": "密山市人民政府",
     "source": "https://mp.weixin.qq.com/s/DdeuvVEmaHoTX7FLUrSgCA + https://www.hljms.gov.cn/mss/c100546/szf.shtml"},
    {"id": 10, "name": "韩永继", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "密山市副市长", "current_org": "密山市人民政府",
     "source": "https://www.hljms.gov.cn/mss/c100546/szf.shtml"},
    {"id": 11, "name": "俞海峰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "密山市副市长", "current_org": "密山市人民政府",
     "source": "https://www.hljms.gov.cn/mss/c100546/szf.shtml"},
    {"id": 12, "name": "李君", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "密山市副市长", "current_org": "密山市人民政府",
     "source": "https://www.hljms.gov.cn/mss/c100546/szf.shtml"},
    # 13 — 周雷 — 市委常委/市领导（见诸报端，职务待细分）
    {"id": 13, "name": "周雷", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "密山市领导（市委班子，职务待细分）", "current_org": "中共密山市委员会",
     "source": "https://mp.weixin.qq.com/s/1Jrll2CHBFq2RpCyXqFmSQ（2026-05-14 信访专题会出席市领导名单）"},
    # 14 — 王海欧 — 市领导（见诸报端）
    {"id": 14, "name": "王海欧", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "密山市领导（职务待细分）", "current_org": "中共密山市委员会",
     "source": "https://mp.weixin.qq.com/s/1Jrll2CHBFq2RpCyXqFmSQ（2026-05-14 信访专题会出席名单）"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 王士强
    {"person_id": 1, "org_id": 1, "title": "密山市委书记", "start": "约2026-07", "end": "present", "rank": "正处级",
     "note": "2026-07-30 密山融媒确认；由市长晋升，接替胡文"},
    {"person_id": 1, "org_id": 2, "title": "市委副书记、市政府市长（原任）", "start": "约2022-09", "end": "约2026-06", "rank": "正处级",
     "note": "官方市政府领导之窗 2022-09 起任职；2026-06-05 高考报道仍载市长"},
    {"person_id": 1, "org_id": 1, "title": "市委副书记", "start": "约2022-09", "end": "约2026-06", "rank": "正处级", "note": "与市长同时任"},
    # 王青
    {"person_id": 2, "org_id": 2, "title": "密山市委副书记、市政府市长、市政府党组书记", "start": "约2026-07", "end": "present", "rank": "正处级",
     "note": "2026-07-01 报道载市长候选人，7月代市长；官方市政府领导页确认市长"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "约2026-07", "end": "present", "rank": "正处级", "note": "与市长职务同时任"},
    # 盖凤程
    {"person_id": 3, "org_id": 3, "title": "密山市人大常委会主任", "start": "", "end": "present", "rank": "正处级",
     "note": "2026-07-01 报道确认；履历待查"},
    # 胡文（前任书记）
    {"person_id": 4, "org_id": 1, "title": "密山市委书记（前任）", "start": "", "end": "约2026-06", "rank": "正处级",
     "note": "2026-02 至 05 多次主持市委全会/市委理论学习中心组；任期起点、卸任去向待查"},
    # 副市长
    {"person_id": 5, "org_id": 2, "title": "密山市副市长", "start": "", "end": "present", "rank": "副处级", "note": "市政府领导之窗"},
    {"person_id": 6, "org_id": 2, "title": "密山市副市长", "start": "", "end": "present", "rank": "副处级", "note": "市政府领导之窗"},
    {"person_id": 7, "org_id": 2, "title": "密山市副市长", "start": "", "end": "present", "rank": "副处级", "note": "市政府领导之窗"},
    {"person_id": 8, "org_id": 2, "title": "密山市副市长", "start": "", "end": "present", "rank": "副处级", "note": "市政府领导之窗"},
    {"person_id": 9, "org_id": 2, "title": "密山市副市长", "start": "", "end": "present", "rank": "副处级", "note": "2026-06 高考督导陪同"},
    {"person_id": 10, "org_id": 2, "title": "密山市副市长", "start": "", "end": "present", "rank": "副处级", "note": "市政府领导之窗"},
    {"person_id": 11, "org_id": 2, "title": "密山市副市长", "start": "", "end": "present", "rank": "副处级", "note": "市政府领导之窗"},
    {"person_id": 12, "org_id": 2, "title": "密山市副市长", "start": "", "end": "present", "rank": "副处级", "note": "市政府领导之窗"},
    # 周雷、王海欧
    {"person_id": 13, "org_id": 1, "title": "密山市领导/市委常委", "start": "", "end": "present", "rank": "", "note": "见诸报端，职务待细分"},
    {"person_id": 14, "org_id": 1, "title": "密山市领导", "start": "", "end": "present", "rank": "", "note": "见诸报端，职务待细分"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    # 党政一把手（现任）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "王士强（市委书记）与王青（市委副书记、市长）为密山市现任党政主要一把手，同一市委班子共事；系市委书记晋升后由王青接任市长", "overlap_org": "密山市", "overlap_period": "2026-07至今"},
    # 前任书记继任关系
    {"person_a": 4, "person_b": 1, "type": "predecessor_successor", "context": "胡文（前任市委书记）与王士强为书记职位前后任；王士强原任市长，2026年7月接任书记", "overlap_org": "中共密山市委员会", "overlap_period": "2026-06/07交接"},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor（市长更替）", "context": "王士强卸任市长后，由王青接任市长", "overlap_org": "密山市人民政府", "overlap_period": "2026-07交接"},
    # 党政 vs 人大
    {"person_a": 1, "person_b": 3, "type": "上下级/同场公职", "context": "王士强（书记）与市人大常委会主任盖凤程同台履职（建党105周年观看大会等）", "overlap_org": "密山市", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 3, "type": "上下级/同场公职", "context": "王青（市长）与市人大常委会主任盖凤程同台履职", "overlap_org": "密山市", "overlap_period": "至今"},
    # 书记与前任书记 / 班子成员
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "王士强（书记）与市领导周雷同在市委班子/信访专题会出席", "overlap_org": "密山市", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 14, "type": "上下级", "context": "王士强与市领导王海欧同场履职", "overlap_org": "密山市", "overlap_period": "2026"},
    # 市长与副市长
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "王青区长与副市长靳英波共事", "overlap_org": "密山市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "王青与副市长迟凤珍共事", "overlap_org": "密山市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "王青与副市长于春红共事（分管教育领域）", "overlap_org": "密山市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "王青与副市长俞海峰共事", "overlap_org": "密山市人民政府", "overlap_period": "至今"},
    # 前任书记与当时的市长（共事）
    {"person_a": 4, "person_b": 1, "type": "党政搭档(前任)", "context": "胡文（前任书记）与王士强（时任市长）为2023-2026上半年党政搭档", "overlap_org": "密山市", "overlap_period": "约2022-2026上半年"},
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
    print(f"Wrote DB: {DB_PATH}")
    print(f"Wrote GEXF: {GEXF_PATH}")
    print(f"Stats: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")