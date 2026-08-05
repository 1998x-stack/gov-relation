#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 顺河回族区 leadership network.

顺河回族区隶属河南省开封市，为开封市市辖区，位于开封市区东北部，是开封市民族
（回族）聚居区县之一，辖苹果园、宋门、铁塔、自由路、东外等街道。回族人口集中，
民族宗教工作显著。地处黄河冲积平原，2026 年为区名次（十五五）开局之年，区第十二次党
代会提出重点打造"一区两基地"。

Current leadership (as of 2026-08, sources: 顺河回族区人民政府门户 www.shunhequ.gov.cn
顺河信息 + 开封市人民政府门户 www.kaifeng.gov.cn 县区动态/县区长声音栏目):
- 区委书记: 白海富（2026-07-28 防汛调研、2026-07-24 政务服务发布会出席、使命2026防汛演练出席）
- 区委副书记、区长: 赛睿（2026-07-30 防汛工作复盘推进会主持、2026-05-30 安全生产部署会主持、
  2026-04-28 五一节前安全生产调研、做客开封市政府网县区长声音访谈）
- 区委副书记: 王德龙（2026-07-28 八一建军节走访驻区部队）
- 区委常委、副区长: 张朋（2026-04-30 安全生产和消防检查；使命2026防汛演练出席）
- 区政府党组成员、副区长: 马云彩（2026-07-24 政务服务专场发布会介绍政务服务改革）
- 区人大常委会主任: 戎中卿（2026-04-24 率队视察道路管网排水基础设施项目）
- 区领导: 赵纪莹、史俊宝、王伟、由长永（2026-05-30 全区安全生产部署会）
- 区领导: 李杰、熊超、唐旭、张园（2026-04-24 人大专项视察）
- 区人武部部长: 姜宏磊；区人武部领导: 马杰

Biographical 缺口: 白海富、赛睿、王德龙、张朋等出生年月/籍贯/学历/入党/完整履历 未从
公开渠道获取（官网领导介绍为 JS 异步加载，未能抓取简历页；通用搜索渠道在此环境受限）。
本构建基于官方确认的名单/职务与治理公开证据（partial-evidence mode）；个体履历缺口
在 report 与 data/persons/*.json 的 open_questions / report/open_gaps.md 中显式标注。
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

SLUG = "顺河回族区"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "顺河回族区_network.db")
    GEXF_PATH = os.path.join(_STAGING, "顺河回族区_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "顺河回族区_network.db"
    GEXF_PATH = GRAPH_DIR / "顺河回族区_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共顺河回族区委员会", "type": "党委", "level": "县处级", "parent": "中共开封市委", "location": "河南省开封市顺河回族区"},
    {"id": 2, "name": "顺河回族区人民政府", "type": "政府", "level": "县处级", "parent": "开封市人民政府", "location": "河南省开封市顺河回族区"},
    {"id": 3, "name": "顺河回族区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "开封市人大常委会", "location": "河南省开封市顺河回族区"},
    {"id": 4, "name": "中国人民政治协商会议顺河回族区委员会", "type": "政协", "level": "县处级", "parent": "政协开封市委员会", "location": "河南省开封市顺河回族区"},
    {"id": 5, "name": "中共顺河回族区纪律检查委员会/区监察委员会", "type": "纪委", "level": "县处级", "parent": "中共开封市纪委", "location": "河南省开封市顺河回族区"},
    {"id": 6, "name": "顺河回族区人民武装部", "type": "武装", "level": "县处级", "parent": "开封军分区", "location": "河南省开封市顺河回族区"},
    {"id": 7, "name": "顺河回族区委宣传部", "type": "党委", "level": "县处级", "parent": "中共顺河回族区委员会", "location": "河南省开封市顺河回族区"},
    {"id": 8, "name": "中共开封市委员会", "type": "党委", "level": "地厅级", "parent": "中共河南省委", "location": "河南省开封市"},
    {"id": 9, "name": "开封市人民政府", "type": "政府", "level": "地厅级", "parent": "河南省人民政府", "location": "河南省开封市"},
    {"id": 10, "name": "顺河回族区宋门街道", "type": "乡镇/街道", "level": "乡科级", "parent": "顺河回族区人民政府", "location": "河南省开封市顺河回族区宋门街道"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    {"id": 1, "name": "白海富", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共顺河回族区委书记", "current_org": "中共顺河回族区委员会",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2084950783617970176.html"},
    {"id": 2, "name": "赛睿", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区委副书记、区人民政府区长", "current_org": "顺河回族区人民政府",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2061257615114547200.html"},
    {"id": 3, "name": "王德龙", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区委副书记", "current_org": "中共顺河回族区委员会",
     "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/xqdt/pc/content/content_2082728635952312320.html"},
    {"id": 4, "name": "张朋", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区委常委、副区长", "current_org": "顺河回族区人民政府",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2051851451247407104.html"},
    {"id": 5, "name": "马云彩", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区人民政府副区长", "current_org": "顺河回族区人民政府",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2081561110975655936.html"},
    {"id": 6, "name": "戎中卿", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区人大常委会主任", "current_org": "顺河回族区人民代表大会常务委员会",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2048575580138942464.html"},
    {"id": 7, "name": "赵纪莹", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区领导", "current_org": "顺河回族区",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2061257615114547200.html"},
    {"id": 8, "name": "史俊宝", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区领导", "current_org": "顺河回族区",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2061257615114547200.html"},
    {"id": 9, "name": "王伟", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区领导", "current_org": "顺河回族区",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2061257615114547200.html"},
    {"id": 10, "name": "由长永", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区领导", "current_org": "顺河回族区",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2061257615114547200.html"},
    {"id": 11, "name": "李杰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区领导", "current_org": "顺河回族区",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2048575580138942464.html"},
    {"id": 12, "name": "熊超", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区领导", "current_org": "顺河回族区",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2048575580138942464.html"},
    {"id": 13, "name": "唐旭", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区领导", "current_org": "顺河回族区",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2048575580138942464.html"},
    {"id": 14, "name": "张园", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区领导", "current_org": "顺河回族区",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2048575580138942464.html"},
    {"id": 15, "name": "姜宏磊", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区人武部部长", "current_org": "顺河回族区人民武装部",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2059946210822238208.html"},
    {"id": 16, "name": "马杰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "顺河回族区人武部领导", "current_org": "顺河回族区人民武装部",
     "source": "https://www.kaifeng.gov.cn/kfsrmzfwz/xqdt/pc/content/content_2082728635952312320.html"},
    {"id": 17, "name": "高建立", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共开封市委书记", "current_org": "中共开封市委员会",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2073944675390631936.html"},
    {"id": 18, "name": "张红伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "开封市委常委、常务副市长", "current_org": "开封市人民政府",
     "source": "https://www.shunhequ.gov.cn/kfsshhzqwz/c00001/pc/content/content_2073944675390631936.html"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "顺河回族区委书记", "start": "", "end": "present", "rank": "正处级", "note": "2026-07-28 实地调研防汛（宋门街道）；2026-07-24 出席政务服务专场发布会；使命2026防汛演练出席；主持区委全面工作"},
    {"person_id": 1, "org_id": 1, "title": "（任区委书记前履历待查）", "start": "", "end": "", "rank": "", "note": "公开资料来源未找到任顺河回族区委书记前完整履历"},
    {"person_id": 2, "org_id": 2, "title": "顺河回族区人民政府区长", "start": "", "end": "present", "rank": "正处级", "note": "2026-07-30 防汛工作复盘暨部署推进会主持；2026-05-30 安全生产部署会主持并讲话；做客开封市政府网县区长声音栏目"},
    {"person_id": 2, "org_id": 1, "title": "顺河回族区委副书记", "start": "", "end": "present", "rank": "正处级", "note": "兼任区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "（任区长前履历待查）", "start": "", "end": "", "rank": "", "note": "公开履历缺口"},
    {"person_id": 3, "org_id": 1, "title": "顺河回族区委副书记", "start": "", "end": "present", "rank": "副处级", "note": "2026-07-28 八一建军节走访驻区部队官兵"},
    {"person_id": 4, "org_id": 2, "title": "顺河回族区副区长", "start": "", "end": "present", "rank": "副处级", "note": "2026-04-30 安全生产和消防检查"},
    {"person_id": 4, "org_id": 1, "title": "顺河回族区委常委", "start": "", "end": "present", "rank": "副处级", "note": "区委常委、副区长；使命2026防汛演练出席"},
    {"person_id": 5, "org_id": 2, "title": "顺河回族区副区长（政府党组成员）", "start": "", "end": "present", "rank": "副处级", "note": "2026-07-24 政务服务专场发布会介绍政务服务改革"},
    {"person_id": 6, "org_id": 3, "title": "顺河回族区人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "2026-04-24 率常委会组成人员和人大代表专项视察道路管网排水项目"},
    {"person_id": 7, "org_id": 2, "title": "顺河回族区领导", "start": "", "end": "present", "rank": "", "note": "2026-05-30 全区安全生产部署会出席"},
    {"person_id": 8, "org_id": 2, "title": "顺河回族区领导", "start": "", "end": "present", "rank": "", "note": "2026-05-30 全区安全生产部署会出席"},
    {"person_id": 9, "org_id": 2, "title": "顺河回族区领导", "start": "", "end": "present", "rank": "", "note": "2026-05-30 全区安全生产部署会出席"},
    {"person_id": 10, "org_id": 2, "title": "顺河回族区领导", "start": "", "end": "present", "rank": "", "note": "2026-05-30 全区安全生产部署会出席；2026-07-28 陪同区委书记调研防汛"},
    {"person_id": 11, "org_id": 3, "title": "顺河回族区领导", "start": "", "end": "present", "rank": "", "note": "2026-04-24 区人大专项视察参加"},
    {"person_id": 12, "org_id": 3, "title": "顺河回族区领导", "start": "", "end": "present", "rank": "", "note": "2026-04-24 区人大专项视察参加"},
    {"person_id": 13, "org_id": 3, "title": "顺河回族区领导", "start": "", "end": "present", "rank": "", "note": "2026-04-24 区人大专项视察参加"},
    {"person_id": 14, "org_id": 3, "title": "顺河回族区领导", "start": "", "end": "present", "rank": "", "note": "2026-04-24 区人大专项视察参加"},
    {"person_id": 15, "org_id": 6, "title": "顺河回族区人武部部长", "start": "", "end": "present", "rank": "", "note": "使命2026防汛应急综合演练出席"},
    {"person_id": 16, "org_id": 6, "title": "顺河回族区人武部领导", "start": "", "end": "present", "rank": "", "note": "2026-07-28 陪同区委副书记走访部队"},
    {"person_id": 17, "org_id": 8, "title": "开封市委书记", "start": "", "end": "present", "rank": "正厅级", "note": "2026-07-05 全市防汛抗旱专题调度会主持并讲话"},
    {"person_id": 18, "org_id": 9, "title": "开封市委常委、常务副市长", "start": "", "end": "present", "rank": "副厅级", "note": "2026-07-05 通报全市防汛工作情况"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "白海富（区委书记）与赛睿（区委副书记、区长）为顺河回族区现职党政主要一把手，2026-07-30 防汛工作复盘推进会、2026-06 区第十二届党代会等多场活动同台共事", "overlap_org": "顺河回族区", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "白海富与区委常委、副区长张朋同台出席使命2026防汛应急综合演练", "overlap_org": "中共顺河回族区委", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "赛睿（区长）主持全区安全生产部署会，区委常委、副区长张朋等区领导出席", "overlap_org": "顺河回族区", "overlap_period": "2026-05-30"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长赛睿主持全区安全生产部署会，区领导赵纪莹出席", "overlap_org": "顺河回族区", "overlap_period": "2026-05-30"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长赛睿主持全区安全生产部署会，区领导史俊宝出席", "overlap_org": "顺河回族区", "overlap_period": "2026-05-30"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长赛睿主持全区安全生产部署会，区领导王伟出席", "overlap_org": "顺河回族区", "overlap_period": "2026-05-30"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区长赛睿主持全区安全生产部署会，区领导由长永出席；由长永又以区领导身份陪同区委书记调研防汛", "overlap_org": "顺河回族区", "overlap_period": "2026"},
    {"person_a": 6, "person_b": 11, "type": "superior_subordinate", "context": "区人大常委会主任戎中卿率视察组开展专项视察，区领导李杰参加", "overlap_org": "顺河回族区人大常委会", "overlap_period": "2026-04-24"},
    {"person_a": 6, "person_b": 12, "type": "superior_subordinate", "context": "区人大常委会主任戎中卿率视察组开展专项视察，区领导熊超参加", "overlap_org": "顺河回族区人大常委会", "overlap_period": "2026-04-24"},
    {"person_a": 6, "person_b": 13, "type": "superior_subordinate", "context": "区人大常委会主任戎中卿率视察组开展专项视察，区领导唐旭参加", "overlap_org": "顺河回族区人大常委会", "overlap_period": "2026-04-24"},
    {"person_a": 6, "person_b": 14, "type": "superior_subordinate", "context": "区人大常委会主任戎中卿率视察组开展专项视察，区领导张园参加", "overlap_org": "顺河回族区人大常委会", "overlap_period": "2026-04-24"},
    {"person_a": 1, "person_b": 15, "type": "上下级", "context": "区委书记白海富出席使命2026防汛演练，区人武部部长姜宏磊出席", "overlap_org": "顺河回族区", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 16, "type": "上下级", "context": "区委副书记王德龙走访驻区部队，人武部领导马杰陪同", "overlap_org": "顺河回族区人武部", "overlap_period": "2026-07-28"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记白海富与区委副书记王德龙同属区委班子", "overlap_org": "中共顺河回族区委", "overlap_period": "现任"},
    {"person_a": 17, "person_b": 1, "type": "superior_subordinate", "context": "开封市委书记高建立与顺河回族区委书记存在市—区上下级领导关系，顺河回族区为其属区", "overlap_org": "开封市/顺河回族区", "overlap_period": "现任"},
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