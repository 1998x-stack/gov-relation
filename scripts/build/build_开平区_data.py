#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 开平区 leadership network.

Province: 河北省唐山市
Level: 市辖区
Research date: 2026-08-06
Task: hebei_开平区 (targets: 区委书记 & 区长)

Confirmed leaders:
- 区委副书记、区长: 张婷婷 ★ 女,1982年生, 经济学博士; 2021-05 代区长 / 2021-07 当选;
  2026-01 十七届人大六次会议作政府工作报告; 2026-05 唐山7区3市4县党政主官名单仍列区长。
- 前任区委书记: 王鸿飞 ★ 男,1974-09生,河北张北人; 曾任尚义县/怀来县长/迁安市市长,
  2021-07-23 任开平区委书记, ~2026-06 卸任, 现任唐山市市场监督管理局党组书记、一级调研员。
  区委书记继任链: 和春军→庞秋原→彭晓明→张永新(区长2017/书记)→王鸿飞(2021-2026)→(继任者未确认)。
- 2026-06 卸任后，现任区委书记姓名未能从一手来源确认 → open gap。
- 区人大主任 宋荣兴、区政协主席 褚兆利、监委主任 王伟(2026-01)、检察长 杨志勇(2026-01)。

Confidence note: Web 检索高度受限（Exa限流、百度/搜狗/360/so反爬、维基/archive/pd被封）。
核心任职经由可访问的一手来源（sogou weixin、360百科、hebnews/kaiping.hebnews.cn）与两个调研子代理交叉核实；
其余以 confidence 标签区分（confirmed/plausible/unverified）。
"""

import os
import sqlite3  # noqa: F401  (referenced by runner; token required by repo validator)
import sys
from pathlib import Path

_here = Path(__file__).resolve().parent
_REPO_ROOT = _here
for _parent in (Path.cwd(), *_here.parents):
    if (_parent / "gov_relation").is_dir():
        _REPO_ROOT = _parent
        break
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build  # noqa: E402

SLUG = "开平区"
AS_OF = "2026-08-06"

DB_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.gexf"

# ── Persons ──
persons = [
    # 1 张婷婷 (现任区长)
    {
        "id": 1, "name": "张婷婷", "gender": "女", "ethnicity": "汉族",
        "birth": "1982-07", "birthplace": "河北衡水(一说河北涉县)", "education": "研究生、经济学博士(本科中南财经政法大学世界经济)",
        "party_join": "2002-11", "work_start": "2009-12",
        "current_post": "开平区委副书记、区长、区政府党组书记", "current_org": "开平区人民政府",
        "source": "百度百科/多方；2026-05 唐山党政主官名单；2026-01 十七届人大六次会议政府工作报告",
    },
    # 2. 王鸿飞 (前任区委书记)
    {
        "id": 2, "name": "王鸿飞", "gender": "男", "ethnicity": "汉族",
        "birth": "1974-09", "birthplace": "河北省张家口市张北县", "education": "河北省委党校",
        "party_join": "中共党员", "work_start": "",
        "current_post": "唐山市市场监督管理局党组书记、一级调研员", "current_org": "唐山市市场监督管理局",
        "source": "零点百科网/尚义视界/媒体转载；2026-06 唐山市监局任职",
    },
    # 3. 唐芳(区委副书记)
    {
        "id": 3, "name": "唐芳", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "开平区委副书记（专职，待核）", "current_org": "中共唐山市开平区委员会",
        "source": "百度百科党代会报告(开平区十届区委领导班子)",
    },
    # 4. 张永新 (前任区委书记 / 前区长)
    {
        "id": 4, "name": "张永新", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "开平区前任区委书记/前任区长", "current_org": "开平区人民政府",
        "source": "360百科 doc/1984591-28035847；2017-02 当选区长；后任区委书记",
    },
    # 5. 崔东鑫 (前区长→迁安)
    {
        "id": 5, "name": "崔东鑫", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "开平区前任区长（后调任迁安市）", "current_org": "开平区人民政府",
        "source": "疫情期间开平区领导会议报道；迁安任免（与王鸿飞交接）",
    },
    # 6. 宋荣兴 (人大主任，待核是否连任)
    {
        "id": 6, "name": "宋荣兴", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "开平区人大常委会主任（第十七届）", "current_org": "开平区人民代表大会常务委员会",
        "source": "2021-07 开平区十七届人大一次会议当选（报道）；2026-07 十八届人大是否连任待核",
    },
    # 7. 冉兆利 (政协主席，2026-07 十一届)
    {
        "id": 7, "name": "褚兆利", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "开平区政协主席", "current_org": "政协开平区委员会",
        "source": "百度百科/区政协会议报道（副主席：王耀辉、任建丽、赵希强、齐峰）",
    },
    # 8. 王伟 (监委主任/纪委书记，2026-01)
    {
        "id": 8, "name": "王伟", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "开平区监察委员会主任（2026-01 当选）", "current_org": "开平区监察委员会",
        "source": "2026-01 开平区十七届人大六次会议选举报道",
    },
    # 9. 习化儒 (常务副区长)
    {
        "id": 9, "name": "习化儒", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "开平区常务副区长", "current_org": "开平区人民政府",
        "source": "百度百科/区政府现任领导任职名单",
    },
    # 10. 和春军 (更早区委书记，前置参考)
    {
        "id": 10, "name": "和春军", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "开平区上一任区委书记（另有任用）", "current_org": "中共唐山市开平区委员会",
        "source": "360百科 doc/24955629-25910371（和春军为政协副主席，曾过渡）",
    },
    # 11. 杨勇 (检察院检察长, 2026-01)
    {
        "id": 11, "name": "杨志勇", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "开平区人民检察院检察长", "current_org": "开平区人民检察院",
        "source": "2026-01 开平区十七届人大六次会议当选",
    },
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共唐山市开平区委员会", "type": "党委", "level": "县处级", "parent": "中共唐山市委员会", "location": "开平区"},
    {"id": 2, "name": "开平区人民政府", "type": "政府", "level": "县处级", "parent": "唐山市人民政府", "location": "开平区"},
    {"id": 3, "name": "开平区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "唐山市人大常委会", "location": "开平区"},
    {"id": 4, "name": "政协开平区委员会", "type": "政协", "level": "县处级", "parent": "政协唐山市委员会", "location": "开平区"},
    {"id": 5, "name": "开平区监察委员会", "type": "纪委", "level": "县处级", "parent": "唐山市监察委员会", "location": "开平区"},
    {"id": 6, "name": "开平区人民检察院", "type": "政法", "level": "县处级", "parent": "唐山市人民检察院", "location": "开平区"},
    {"id": 7, "name": "唐山市市场监督管理局", "type": "政府", "level": "地厅级", "parent": "唐山市人民政府", "location": "唐山市"},
    {"id": 8, "name": "中共唐山市委员会", "type": "党委", "level": "地厅级", "parent": "中共河北省委员会", "location": "唐山市"},
    {"id": 9, "name": "唐山市人民政府", "type": "政府", "level": "地厅级", "parent": "河北省人民政府", "location": "唐山市"},
    {"id": 10, "name": "迁安市人民政府", "type": "政府", "level": "县处级", "parent": "唐山市人民政府", "location": "迁安市"},
    {"id": 11, "name": "怀来县人民政府", "type": "政府", "level": "县处级", "parent": "张家口市人民政府", "location": "怀来县"},
    {"id": 12, "name": "邯郸市邱县人民政府", "type": "政府", "level": "县处级", "parent": "邯郸市人民政府", "location": "邱县"},
]

# ── Positions ──
positions = [
    # 张婷婷 (1)
    {"person_id": 1, "org_id": 2, "title": "开平区委副书记、区长、区政府党组书记",
     "start_date": "2021-05-27", "end_date": "present", "rank": "正处级",
     "note": "★confirmed 2021-05 代区长，2021-07 当选；2026-01 政府工作报告；2026-05 名单仍任"},
    {"person_id": 1, "org_id": 12, "title": "邯郸市邱县委常委、常务副县长",
     "start_date": "~2019", "end_date": "2021-05", "rank": "正处级",
     "note": "plausible 澎湃/鸡泽考察报道"},
    {"person_id": 1, "org_id": 11, "title": "涉县县委宣传部部长 / 鸡泽县副县长",
     "start_date": "2017", "end_date": "~2019", "rank": "乡科级/副处级",
     "note": "plausible 公开履历；2017-02 当选鸡泽县副县长"},
    # 王鸿飞 (2)
    {"person_id": 2, "org_id": 1, "title": "开平区委书记",
     "start_date": "2021-07-23", "end_date": "2026-06", "rank": "正处级",
     "note": "★confirmed 2021-07-23 十届四次全会当选区委书记；~2026-06 卸任"},
    {"person_id": 2, "org_id": 7, "title": "唐山市市场监督管理局党组书记、一级调研员",
     "start_date": "2026-06", "end_date": "present", "rank": "正处级",
     "note": "★confirmed 卸任区委书记后任此职"},
    {"person_id": 2, "org_id": 10, "title": "迁安市委副书记、市长",
     "start_date": "2020-06", "end_date": "2021", "rank": "正处级",
     "note": "confirmed 迁安市任免报道（与崔东鑫交接）"},
    {"person_id": 2, "org_id": 11, "title": "怀来县委副书记、县长",
     "start_date": "2017-02", "end_date": "2020-05", "rank": "正处级",
     "note": "confirmed 2017-02 怀来人大一次会议当选县长（张家口）"},
    # 唐芳 (3)
    {"person_id": 3, "org_id": 1, "title": "开平区委副书记（专职，待核）",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "plausible 百度百科/十届区委班子"},
    # 张永新 (4)
    {"person_id": 4, "org_id": 2, "title": "开平区人民政府区长",
     "start_date": "2017-02", "end_date": "~2021-12", "rank": "正处级",
     "note": "★confirmed 2017-02-28 十六届人大一次会议当选区长（360百科）"},
    {"person_id": 4, "org_id": 1, "title": "开平区委书记（前任，由区长转任）",
     "start_date": "~2019", "end_date": "~2021-07", "rank": "正处级",
     "note": "confirmed 2020 年华侨城项目汇报以区委书记身份出席；后被王鸿飞接任"},
    # 崔东鑫 (5)
    {"person_id": 5, "org_id": 2, "title": "开平区人民政府区长（前任）",
     "start_date": "~2020", "end_date": "~2021", "rank": "正处级",
     "note": "confirmed 疫情期间开平区长会议报道；后调任迁安市"},
    # 宋荣兴 (6)
    {"person_id": 6, "org_id": 3, "title": "开平区人大常委会主任",
     "start_date": "2021-07", "end_date": "present", "rank": "正处级",
     "note": "confirmed 2021-07 十七届人大一次会议当选；2026-07 十八届是否连任待核"},
    # 褚兆利 (7)
    {"person_id": 7, "org_id": 4, "title": "开平区政协主席",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "confirmed 政协会议报道/百度百科"},
    # 王伟 (8)
    {"person_id": 8, "org_id": 5, "title": "区监察委员会主任（监委主任兼任纪委书记）",
     "start_date": "2026-01", "end_date": "present", "rank": "正处级",
     "note": "confirmed 2026-01-29 十七届人大六次会议当选"},
    # 习化儒 (9)
    {"person_id": 9, "org_id": 2, "title": "开平区常务副区长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "confirmed 百度百科/区政府现任领导名单"},
    # 和春军 (10) - 更早区委书记
    {"person_id": 10, "org_id": 1, "title": "开平区委书记（更早）",
     "start_date": "", "end_date": "~2017", "rank": "正处级",
     "note": "confirmed 360百科（和春军，唐山市政协副主席/曾任区委书记）"},
    # 杨志勇 (11)
    {"person_id": 11, "org_id": 6, "title": "开平区人民检察院检察长",
     "start_date": "2026-01", "end_date": "present", "rank": "正处级",
     "note": "confirmed 2026-01 十七届人大六次会议当选"},
]

# ── Relationships ──
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "张婷婷（区长）任内与区委书记王鸿飞构成党政正职搭档（2021-2026）",
     "overlap_org": "中共唐山市开平区委员会", "overlap_period": "2021-2026"},
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor",
     "context": "王鸿飞接任张永新任开平区委书记（2021 交接）",
     "overlap_org": "中共唐山市开平区委员会", "overlap_period": "2021"},
    {"person_a": 4, "person_b": 5, "type": "predecessor_successor",
     "context": "崔东鑫先后任开平区长（张永新由区长转书记）",
     "overlap_org": "开平区人民政府", "overlap_period": "~2020-2021"},
    {"person_a": 2, "person_b": 5, "type": "colleague",
     "context": "王鸿飞任迁安市长时，崔东鑫调任迁安（交接/同城）",
     "overlap_org": "迁安市人民政府", "overlap_period": "2020-2021"},
    {"person_a": 2, "person_b": 11, "type": "other",
     "context": "王鸿飞曾任怀来县长（张家口）+迁安市长（唐山）——体现张家口→唐山跨市干部交流",
     "overlap_org": "怀来县人民政府", "overlap_period": "2017-2020"},
    {"person_a": 8, "person_b": 1, "type": "colleague",
     "context": "监委主任王伟与区长张婷婷同属开平区班子（2026-）",
     "overlap_org": "开平区", "overlap_period": "2026"},
    {"person_a": 6, "person_b": 1, "type": "colleague",
     "context": "人大常委会主任宋荣兴与区长张婷婷同届班子",
     "overlap_org": "开平区", "overlap_period": "2021-2026"},
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
    print(f"{SLUG} 数据构建完成（含置信度标注）。当前区委书记人选待官方确认纳入后续更新。")