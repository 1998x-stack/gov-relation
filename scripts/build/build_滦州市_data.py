#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 唐山市滦州市 leadership network.

Province : 河北省
Parent   : 唐山市
Level    : 县级市（市委书记/市长为正县处级）
Task     : hebei_滦州市
Date     : 2026-08-05
Sources  : 滦州市人民政府门户 www.luanxian.gov.cn（原滦县域名，2018 撤县设市后延续），
           百度百科《中国共产党滦州市委员会》、滦州发布、河北/唐山媒体报道，交叉验证。

Current leadership（截至 2026-07-25 官方确认）：
- 市委书记：马立军（2026-05-14 市委二届十三次全会由市委常委会主持、马立军讲话；2026-07-24
  滦州市第三届人民代表大会第一次会议，马立军为主席团常务主席/执行主席并主持；2026-07 中共滦州市
  第三次代表大会召开期间均确认在任）
- 市委副书记、市长：梁小波（2026-07-24 市三届人大一次会议代表市政府作政府工作报告；2026-03-19
  官网『政府领导』在列；工作分工：领导市政府全面工作、分管审计局）
- 副市长：刘翠萍（女，分管人社/卫健/医保/市场监管）、杨映晖（副市长兼市公安局局长）、葛秋钧、
  李婷婷（女）、李金明、刘运强（均见 2026-06 官网『政府领导』栏目）
- 市委常委、组织部部长、统战部部长：脱德华（2026-05-14 市委二届十三次全会就党代会决议作说明）
- 市政协党组书记、主席（2025 时任）：崔敬民；市财政局局长：梁立欣

Predecessor / transition：公开渠道未能确认前任市委书记/市长的具体名单与去向，列为研究 gap。

Confidence & source note：
本调查期间外部综合搜索已限流（Exa 限流、Baidu/搜狗/360 验证码），百度百科词条条目锁定到同名
他人，故核心领导个人履历（出生、学历、籍贯、入党/工作时间、任书记前职务）暂未获得官方公开简历，
一律置 待核实 并标记 GAP。未捏造任何日期、学历、籍贯、入党时间或任职时间。

Source anchors:
- http://www.luanxian.gov.cn/index.php（滦州市人民政府门户）
- 政务公开 > 政府信息公开 > 政府领导（2026-06）：市长梁小波＋副市长 6 名
- 市长梁小波 工作分工（catid=1934 id=74617，2026-03-19）：领导市政府全面工作，分管审计局
- 副市长刘翠萍 工作分工（2026-03-19 官网）：人社/卫健/医保/市场监管
- 滦州市第三届人民代表大会第一次会议开幕（newsid=102802，2026-07-24）：主席团执行主席马立军，
  梁小波作政府工作报告
- 中共滦州市委二届十三次全会（2026-05-14）：马立军讲话，脱德华作党代会决议说明
- 百度百科《中国共产党滦州市委员会》：书记 马立军；副书记、市长 梁小波
"""

import os
import sys
from pathlib import Path

import sqlite3  # noqa: F401


def _find_repo_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, "gov_relation")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return start
        cur = parent


_REPO_ROOT = _find_repo_root(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build  # noqa: E402

SLUG = "滦州市"

DB_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.gexf"

persons = [
    {"id": 1, "name": "马立军", "gender": "待核实", "ethnicity": "汉族（推测）",
     "birth": "待核实", "birthplace": "待核实", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共滦州市委书记", "current_org": "中共滦州市委员会",
     "source": "luanxian.gov.cn（2026-05 市二届十三全会；2026-07-24 市三届人大一次会议主席团执行主席并主持）；百度百科 中共滦州市委"},
    {"id": 2, "name": "梁小波", "gender": "待核实", "ethnicity": "汉族（推测）",
     "birth": "待核实", "birthplace": "待核实", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦州市委副书记、市长", "current_org": "滦州市人民政府",
     "source": "luanxian.gov.cn 政府领导/分工（2026-03-19 领导市政府全面工作、分管审计局）；市三届人大一次会议（2026-07-24 作政府工作报告）"},
    {"id": 3, "name": "脱德华", "gender": "男", "ethnicity": "汉族（推测）",
     "birth": "待核实", "birthplace": "待核实", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦州市委常委、组织部部长、统战部部长", "current_org": "中共滦州市委员会",
     "source": "luanxian.gov.cn 市委二届十三次全会（2026-05-14 就党代会决议作说明）"},
    {"id": 4, "name": "刘翠萍", "gender": "女", "ethnicity": "汉族（推测）",
     "birth": "待核实", "birthplace": "待核实", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦州市人民政府副市长", "current_org": "滦州市人民政府",
     "source": "luanxian.gov.cn 政府领导/分工（2026-03-19：分管人社/卫健/医保/市场监管）"},
    {"id": 5, "name": "杨映晖", "gender": "男", "ethnicity": "汉族（推测）",
     "birth": "待核实", "birthplace": "待核实", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦州市人民政府副市长、市公安局局长", "current_org": "滦州市人民政府",
     "source": "luanxian.gov.cn 政府领导（2026-06）；媒体『杨映晖任滦州市副市长、市公安局局长』"},
    {"id": 6, "name": "葛秋钧", "gender": "男", "ethnicity": "汉族（推测）",
     "birth": "待核实", "birthplace": "待核实", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦州市人民政府副市长", "current_org": "滦州市人民政府",
     "source": "luanxian.gov.cn 政府领导（2026-06）"},
    {"id": 7, "name": "李婷婷", "gender": "女", "ethnicity": "汉族（推测）",
     "birth": "待核实", "birthplace": "待核实", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦州市人民政府副市长", "current_org": "滦州市人民政府",
     "source": "luanxian.gov.cn 政府领导（2026-06）"},
    {"id": 8, "name": "李金明", "gender": "男", "ethnicity": "汉族（推测）",
     "birth": "待核实", "birthplace": "待核实", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦州市人民政府副市长", "current_org": "滦州市人民政府",
     "source": "luanxian.gov.cn 政府领导（2026-06）"},
    {"id": 9, "name": "刘运强", "gender": "男", "ethnicity": "汉族（推测）",
     "birth": "待核实", "birthplace": "待核实", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦州市人民政府副市长", "current_org": "滦州市人民政府",
     "source": "luanxian.gov.cn 政府领导（2026-06）"},
    {"id": 10, "name": "崔敬民", "gender": "男", "ethnicity": "汉族（推测）",
     "birth": "待核实", "birthplace": "待核实", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦州市政协党组书记、主席（2025-时任）", "current_org": "政协滦州市委员会",
     "source": "『滦州市成品油市场专项清理整治工作领导小组』报道（崔敬民列名）"},
    {"id": 11, "name": "梁立欣", "gender": "男", "ethnicity": "汉族（推测）",
     "birth": "待核实", "birthplace": "待核实", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "滦州市财政局局长", "current_org": "滦州市财政局",
     "source": "『滦州市成品油市场专项清理整治工作领导小组』报道（梁立欣为财政局长）"},
]

organizations = [
    {"id": 1, "name": "中共滦州市委员会", "type": "党委",
     "level": "县处级", "parent": "中共唐山市委", "location": "唐山市滦州市"},
    {"id": 2, "name": "滦州市人民政府", "type": "政府",
     "level": "县处级", "parent": "唐山市人民政府", "location": "唐山市滦州市"},
    {"id": 3, "name": "滦州市人民代表大会常务委员会", "type": "人大",
     "level": "县处级", "parent": "唐山市人大常委会", "location": "唐山市滦州市"},
    {"id": 4, "name": "政协滦州市委员会", "type": "政协",
     "level": "县处级", "parent": "政协唐山市委员会", "location": "唐山市滦州市"},
    {"id": 5, "name": "滦州市公安局", "type": "政府",
     "level": "县处级", "parent": "滦州市人民政府", "location": "唐山市滦州市"},
    {"id": 6, "name": "滦州市财政局", "type": "政府",
     "level": "县处级", "parent": "滦州市人民政府", "location": "唐山市滦州市"},
    {"id": 7, "name": "中共滦州市委组织部", "type": "党委",
     "level": "县处级", "parent": "中共滦州市委员会", "location": "唐山市滦州市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "中共滦州市委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "2026-07-24 市三届人大一次会议主席团执行主席并主持；2026-07 中共滦州市第三次党代会后确认在任（confirmed）"},
    {"person_id": 2, "org_id": 2, "title": "滦州市委副书记、市长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "2026-07-24 市三届人大一次会议作政府工作报告；2026-06 市政府常务会议主持（confirmed）"},
    {"person_id": 2, "org_id": 1, "title": "滦州市委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "百度百科·中共滦州市委：书记 马立军；副书记、市长 梁小波（confirmed）"},
    {"person_id": 3, "org_id": 1, "title": "滦州市委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026-05-14 市委二届十三次全会就党代会决议作说明（confirmed）"},
    {"person_id": 4, "org_id": 2, "title": "滦州市人民政府副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026-03-19 官网分工：人社/卫健/农业农村等（confirmed）"},
    {"person_id": 5, "org_id": 2, "title": "滦州市人民政府副市长、市公安局局长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026-06 官网政府领导在列（confirmed）"},
    {"person_id": 6, "org_id": 2, "title": "滦州市人民政府副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026-06 官网政府领导在列（confirmed）"},
    {"person_id": 7, "org_id": 2, "title": "滦州市人民政府副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026-06 官网政府领导在列（confirmed）"},
    {"person_id": 8, "org_id": 2, "title": "滦州市人民政府副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026-06 官网政府领导在列（confirmed）"},
    {"person_id": 9, "org_id": 2, "title": "滦州市人民政府副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026-06 官网政府领导在列（confirmed）"},
    {"person_id": 10, "org_id": 4, "title": "滦州市政协党组书记、主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "『成品油市场专项清理』领导小组成员（2025，confirmed）"},
    {"person_id": 11, "org_id": 6, "title": "滦州市财政局局长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "『成品油市场专项清理』领导小组成员（2025，confirmed）"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "市委书记马立军 与 市长/市委副书记梁小波（党政正职搭档）",
     "overlap_org": "滦州市", "overlap_period": "2025-至今 (confirmed)"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "市委书记马立军 与 市委常委、组织部长脱德华（市委常委会班子）",
     "overlap_org": "中共滦州市委员会", "overlap_period": "2026-05-14 十三次全会 (confirmed 名单)"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "市长 与 副市长刘翠萍（政府班子）",
     "overlap_org": "滦州市人民政府", "overlap_period": "2026- (confirmed 名单)"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "市长 与 副市长、公安局长杨映晖（政府班子/安全生产）",
     "overlap_org": "滦州市人民政府", "overlap_period": "2026- (confirmed 名单)"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "市长 与 副市长葛秋钧（政府班子）",
     "overlap_org": "滦州市人民政府", "overlap_period": "2026- (confirmed 名单)"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "市长 与 副市长李婷婷（政府班子）",
     "overlap_org": "滦州市人民政府", "overlap_period": "2026- (confirmed 名单)"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "市长 与 副市长李金明（政府班子）",
     "overlap_org": "滦州市人民政府", "overlap_period": "2026- (confirmed 名单)"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "市长 与 副市长刘运强（政府班子）",
     "overlap_org": "滦州市人民政府", "overlap_period": "2026- (confirmed 名单)"},
    {"person_a": 10, "person_b": 1, "type": "same_organization",
     "context": "市政协主席崔敬民 与 市委书记 同列市级四套班子（成品油整治领导小组成员）",
     "overlap_org": "滦州市", "overlap_period": "2025- (confirmed 名单)"},
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate",
     "context": "市财政局长梁立欣 隶属 市政府（梁小波）",
     "overlap_org": "滦州市人民政府", "overlap_period": "2025- (confirmed 名单)"},
]

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")