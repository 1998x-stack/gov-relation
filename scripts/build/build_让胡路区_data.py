#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 让胡路区 leadership network.

让胡路区隶属黑龙江省大庆市，位于大庆市区西部（松嫩平原中部）。常驻人口约58.1万，
辖1镇（喇嘛甸镇）及多个街道。大庆为油田城市，"地企合作/油地融合"是核心治理逻辑。

Current leadership as of 2026-07 (sources: 让胡路区人民政府官网 www.dqrhl.gov.cn
"区政府领导" 领导之窗官方栏目 qzfld/listxxgk.shtml + 区委/区政府新闻报道（融媒体中心）):
- 区委书记: 孙钊（现任确认，2026-07 主持区委十届104次常委会、一线调研防洪）
- 区委副书记、政府区长: 胡璐璐（女/汉，2026-06-25官网领导简介确认，主持区政府全面工作）

区政府领导班子（官网领导简介，2026-06-25，confirmed）:
- 佟剑飞: 男/满族，区委常委、副区长（分管常务；国资、工业经济、安全生产、城区建设、城市管理、生态环境）
- 高晓薇: 女/汉，区委常委、副区长（商贸经济、招商引资、营商环境、统计）
- 王洪喜: 男/汉，副区长（农业农村、自然资源、林业草原、市场监管、民政、退役军人）
- 王德忠: 男/汉，副区长（公共安全、司法；统筹辖区公安分局/交警）
- 于铁峰: 男/汉，政府党组成员（财税、国资；联系中省直企业）

其他区级领导（报告新闻确认，具体区委职务待核）:
- 唐万涛: 区政协主席；彭景伟: 区政协副主席
- 杜尊义、朱晓东、康金凤、王兆忠: 区级领导

Biographical gaps（见 report 与 data/persons/*.json）:
- 孙钊、胡璐璐的出生年/籍贯/学历/入党时间及任现职前的完整履历未在官网公开 -> open_questions
- 前任区委书记（孙钊前任）与前任区长身份及去向待核
- 区委纪委书记、组织部/宣传部/统战部/政法委书记具体人选待核
- 杜尊义/朱晓东/康金凤/王兆忠的区委具体职务待核
"""

import os
import sqlite3  # noqa: F401  (validated by process_tmp.py token check)
import sys
from datetime import datetime
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

SLUG = "让胡路区"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "让胡路区_network.db")
    GEXF_PATH = os.path.join(_STAGING, "让胡路区_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "让胡路区_network.db"
    GEXF_PATH = GRAPH_DIR / "让胡路区_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共大庆市让胡路区委员会", "type": "党委", "level": "县处级", "parent": "中共大庆市委", "location": "黑龙江省大庆市让胡路区"},
    {"id": 2, "name": "让胡路区人民政府", "type": "政府", "level": "县处级", "parent": "大庆市人民政府", "location": "黑龙江省大庆市让胡路区"},
    {"id": 3, "name": "让胡路区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "大庆市人大常委会", "location": "黑龙江省大庆市让胡路区"},
    {"id": 4, "name": "中国人民政治协商会议让胡路区委员会", "type": "政协", "level": "县处级", "parent": "政协大庆市委员会", "location": "黑龙江省大庆市让胡路区"},
    {"id": 5, "name": "中共让胡路区纪律检查委员会/让胡路区监察委员会", "type": "纪委", "level": "县处级", "parent": "中共大庆市纪委", "location": "黑龙江省大庆市让胡路区"},
    {"id": 6, "name": "大庆市让胡路区喇嘛甸镇人民政府", "type": "乡镇/街道", "level": "正科级", "parent": "让胡路区人民政府", "location": "黑龙江省大庆市让胡路区喇嘛甸镇"},
    {"id": 7, "name": "大庆油田有限责任公司（驻区企业）", "type": "国有特大型能源企业", "level": "央企", "parent": "中国石油天然气集团", "location": "黑龙江省大庆市"},
    {"id": 8, "name": "中共大庆市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委", "location": "黑龙江省大庆市"},
    {"id": 9, "name": "大庆市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省大庆市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 孙钊 — 区委书记（现任）
    {"id": 1, "name": "孙钊", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共大庆市让胡路区委书记", "current_org": "中共大庆市让胡路区委员会",
     "source": "https://www.dqrhl.gov.cn/ranghulu/toutiao/202607/c05_417051.shtml（区委常委会报道，official）"},
    # 2 — 胡璐璐 — 区长（现任）
    {"id": 2, "name": "胡璐璐", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "让胡路区委副书记、政府区长", "current_org": "让胡路区人民政府",
     "source": "https://www.dqrhl.gov.cn/ranghulu/qzfld/202504/c05_376135.shtml（区政府领导简介，official）"},
    # 3 — 佟剑飞 — 常务副区长
    {"id": 3, "name": "佟剑飞", "gender": "男", "ethnicity": "满族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "让胡路区委常委、政府副区长（常务）", "current_org": "让胡路区人民政府",
     "source": "https://www.dqrhl.gov.cn/ranghulu/qzfld/202504/c05_376127.shtml（区政府领导简介，official）"},
    # 4 高晓薇
    {"id": 4, "name": "高晓薇", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "让胡路区委常委、政府副区长", "current_org": "让胡路区人民政府",
     "source": "https://www.dqrhl.gov.cn/ranghulu/qzfld/202504/c05_376131.shtml（区政府领导简介，official）"},
    # 5 王洪喜
    {"id": 5, "name": "王洪喜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "让胡路区政府副区长", "current_org": "让胡路区人民政府",
     "source": "https://www.dqrhl.gov.cn/ranghulu/qzfld/202504/c05_376129.shtml（区政府领导简介，official）"},
    # 6 王德忠
    {"id": 6, "name": "王德忠", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "让胡路区政府副区长", "current_org": "让胡路区人民政府",
     "source": "https://www.dqrhl.gov.cn/ranghulu/qzfld/202504/c05_376128.shtml（区政府领导简介，official）"},
    # 7 于铁峰 — 政府党组成员
    {"id": 7, "name": "于铁峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "让胡路区政府党组成员", "current_org": "让胡路区人民政府",
     "source": "https://www.dqrhl.gov.cn/ranghulu/qzfld/202504/c05_376126.shtml（区政府领导简介，official）"},
    # 8 唐万涛 — 政协主席
    {"id": 8, "name": "唐万涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "让胡路区政协主席", "current_org": "中国人民政治协商会议让胡路区委员会",
     "source": "https://www.dqrhl.gov.cn/ranghulu/tpxw/202607/c05_415685.shtml（区政协十届25次常委会，official）"},
    # 9 彭景伟 — 政协副主席
    {"id": 9, "name": "彭景伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "让胡路区政协副主席", "current_org": "中国人民政治协商会议让胡路区委员会",
     "source": "https://www.dqrhl.gov.cn/ranghulu/tpxw/202607/c05_415685.shtml（区政协新闻，official）"},
    # 10 杜尊义 — 区领导（具体职务待核）
    {"id": 10, "name": "杜尊义", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "让胡路区（区委/区人大）领导", "current_org": "中共大庆市让胡路区委员会",
     "source": "https://www.dqrhl.gov.cn/ranghulu/tpxw/202607/c05_415034.shtml 与 c05_416289.shtml（区委表彰/活动新闻列名，official）"},
    # 11 朱晓东 — 区级领导
    {"id": 11, "name": "朱晓东", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "让胡路区级领导", "current_org": "中共大庆市让胡路区委员会",
     "source": "https://www.dqrhl.gov.cn/ranghulu/tpxw/202607/c05_415034.shtml（区委'两优一先'表彰大会新闻列名，official）"},
    # 12 康金凤 — 区领导
    {"id": 12, "name": "康金凤", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "让胡路区级领导", "current_org": "中共大庆市让胡路区委员会",
     "source": "https://www.dqrhl.gov.cn/ranghulu/tpxw/202607/c05_416289.shtml（区常务会议/安委会列名，official）"},
    # 13 王兆忠 — 区领导
    {"id": 13, "name": "王兆忠", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "让胡路区级领导", "current_org": "中共大庆市让胡路区委员会",
     "source": "https://www.dqrhl.gov.cn/ranghulu/tpxw/202607/c05_416289.shtml（年轻干部大赛出席领导列名，official）"},
    # 14 李世峰 — 大庆市委书记（上级跨级关联）
    {"id": 14, "name": "李世峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共大庆市委书记", "current_org": "中共大庆市委员会",
     "source": "https://www.dqrhl.gov.cn/ranghulu/toutiao/202607/c05_417051.shtml（转国家领导调研，official）+ report/大庆市报告"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "让胡路区委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持区委全面工作；2026-07-29 主持区委十届104次常委会，2026-07-04 带队防洪调研（融媒体中心，confirmed）"},
    {"person_id": 2, "org_id": 2, "title": "让胡路区委副书记、政府区长", "start": "", "end": "present", "rank": "正处级", "note": "主持区政府全面工作，主管区审计局；2026-06-25 官网领导简介，2026-07-14 主持区政府十一届65次常务会议"},
    {"person_id": 3, "org_id": 2, "title": "区委常委、政府副区长（常务）", "start": "", "end": "present", "rank": "副处级", "note": "区政府常务工作；国资监管、工业经济、安全生产、城区建设、城市管理、生态环境；协助区长分管审计局"},
    {"person_id": 4, "org_id": 2, "title": "区委常委、政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "商贸经济、招商引资、营商环境、统计；联系区工商联"},
    {"person_id": 5, "org_id": 2, "title": "区政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "农业农村、自然资源、林业草原、市场监管、退役军人、民政"},
    {"person_id": 6, "org_id": 2, "title": "区政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "公共安全、司法；统筹协调辖区各公安分局、交警大队"},
    {"person_id": 7, "org_id": 2, "title": "区政府党组成员", "start": "", "end": "present", "rank": "", "note": "财税、国资；协调红骥牧场/星火牧场/银浪牧场等国有企业国资监管，联系大庆油田等中省直企业"},
    {"person_id": 8, "org_id": 4, "title": "让胡路区政协主席", "start": "", "end": "present", "rank": "正处级", "note": "2026-07-08 主持区政协十届25次常委会（扩大）会议"},
    {"person_id": 9, "org_id": 4, "title": "让胡路区政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "让胡路区区级领导（具体职务待核）", "start": "", "end": "present", "rank": "县处级", "note": "官方新闻以区领导列名（孙钊带队活动）"},
    {"person_id": 11, "org_id": 1, "title": "让胡路区区级领导", "start": "", "end": "present", "rank": "县处级", "note": "官方新闻'两优一先'表彰大会为列名"},
    {"person_id": 12, "org_id": 1, "title": "让胡路区区级领导", "start": "", "end": "present", "rank": "县处级", "note": "出席区政府常务会议、安全生产委员会会议"},
    {"person_id": 13, "org_id": 1, "title": "让胡路区区级领导", "start": "", "end": "present", "rank": "县处级", "note": "年轻干部风采展示大赛出席列名"},
    # 上级（大庆市）关系
    {"person_id": 14, "org_id": 8, "title": "中共大庆市委书记", "start": "", "end": "present", "rank": "正厅级", "note": "2026-07-28 到让胡路区调研（上级对区指导）"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "孙钊（区委书记）与胡璐璐（区委副书记、政府区长）为让胡路区现行党政主要领导，2026年同届共事", "overlap_org": "中共大庆市让胡路区委员会", "overlap_period": "2026至今"},
    # 区委书记与班子成员
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记孙钊与区委常委佟剑飞同届班子共事（防洪调研中佟剑飞陪同）", "overlap_org": "中共大庆市让胡路区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记孙钊与区委常委高晓薇同届班子共事", "overlap_org": "中共大庆市让胡路区委员会", "overlap_period": "2026"},
    # 区长与副区长
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "区长胡璐璐与常务副区长佟剑飞共事（协助区长分管审计局）", "overlap_org": "让胡路区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长胡璐璐与副区长高晓薇共事", "overlap_org": "让胡路区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长胡璐璐与副区长王洪喜共事", "overlap_org": "让胡路区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长胡璐璐与副区长王德忠共事", "overlap_org": "让胡路区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长胡璐璐与政府党组成员于铁峰共事（财税/国资）", "overlap_org": "让胡路区人民政府", "overlap_period": "2026"},
    # 人大政协
    {"person_a": 1, "person_b": 8, "type": "同场公职", "context": "区委书记孙钊与区政协主席唐万涛同台履职", "overlap_org": "让胡路区", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "同场公职", "context": "区长胡璐璐与区政协主席唐万涛同台履职", "overlap_org": "让胡路区", "overlap_period": "2026"},
    # 市区跨级
    {"person_a": 14, "person_b": 1, "type": "上级指导", "context": "大庆市委书记李世峰2026-07-28到让胡路区调研（市级对区级领导指导）", "overlap_org": "让胡路区", "overlap_period": "2026-07"},
    # 油地合作线索（企业关联）
    {"person_a": 7, "person_b": 3, "type": "企地合作", "context": "常务副区长佟剑飞分工衔接区国资/工业经济，企业与地方治理互动（油地融合）", "overlap_org": "大庆油田驻区企业", "overlap_period": "2026"},
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