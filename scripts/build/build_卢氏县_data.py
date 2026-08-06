#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 卢氏县 (Lushi County), 三门峡市, 河南省.

Investigation date: 2026-08-06
Task ID: henan_卢氏县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - Official website: www.lushixian.gov.cn (卢氏县人民政府 — 领导之窗, 今日要闻, 政府工作报告)
  - 求闻百科/维基: 胡志权（1971年7月生，河南柘城人，2023.05起任卢氏县委书记）
  - 大河网/三门峡网/河南一百度: 刘万增（1978年生，河南郏县人，2021.10当选卢氏县长）
  - 卢氏县纪委监委网站 (smxlz.gov.cn): 丁娜娜（2026.06 现任纪委书记/监委主任候选人）
  - 党员三中全会精神/县委全会报道: 县委常委会名单

Confidence notes:
  - 胡志权（县委书记）: confirmed via 2023.05 河南省委组织部任前公示 + 2026 官方要闻。
  - 刘万增（县长）: confirmed via 2021.10 大河网 + 2025/2026 政府工作报告及要闻。
  - 四套班子、常委会名单: 经官方要闻（县委十三届五次全会、县政府常务会、县人代会/政协会）确认。
  - 县委常委分工存在任期调整（纪委书记李庆锋→丁娜娜2026；组织部长王昱、统战部长吕宏伟）；
    人大主任 王磊（2026.01 起），前任 狄罡。相关变迁写入 notes/open_questions。
  - Partial-evidence artifact: 核心主官身份与履历来源较充分；个别常委（郭勇）具体分工与部分履历待补。
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "卢氏县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "胡志权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-07",
        "birthplace": "河南柘城",
        "education": "大学；河南师范大学政教系（文学学士）",
        "party_join": "1993-01",
        "work_start": "1993-07",
        "current_post": "县委书记",
        "current_org": "中共卢氏县委员会",
        "source": "河南省委组织部2023.05任前公示：胡志权任中共卢氏县委书记；卢氏县政府网站2026年要闻确认其在任"
    },
    {
        "id": 2,
        "name": "刘万增",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978",
        "birthplace": "河南郏县",
        "education": "兰州大学（2002.08毕业，在校入党）",
        "party_join": "2000-01",
        "work_start": "2002-08",
        "current_post": "县长",
        "current_org": "卢氏县人民政府",
        "source": "维基百科/刘万增（1978年生，河南郏县人）+ 2021.10 大河网当选县长报道 + 2025/2026 政府工作报告"
    },
    # ═══════ 县委/四套班子 ═══════
    {
        "id": 3,
        "name": "王磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县人大常委会主任",
        "current_org": "卢氏县人大常委会",
        "source": "卢氏县政府网要闻（2026-01 三门峡人大网：县委副书记、县人大常委会主任王磊）"
    },
    {
        "id": 4,
        "name": "王昱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共卢氏县委员会",
        "source": "卢氏县政府网：县委十三届五次全会及两会报道（常委、组织部部长王昱）"
    },
    {
        "id": 5,
        "name": "孙丽松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共卢氏县委员会",
        "source": "卢氏县政府网要闻（县委副书记、县委办主任王磊，县委常委、政法委书记孙丽松陪同调研）"
    },
    {
        "id": 6,
        "name": "王星",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "卢氏县人民政府",
        "source": "卢氏县政府网领导之窗：王星，女，汉族，中共党员，县委常委、常务副县长、党组副书记"
    },
    {
        "id": 7,
        "name": "吕宏伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共卢氏县委员会",
        "source": "卢氏县政府网要闻（2026-02：县委常委、统战部部长吕宏伟领学）"
    },
    {
        "id": 8,
        "name": "卫军强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "中共卢氏县委员会",
        "source": "卢氏县政府网县委十三届五次全会报道（常委卫军强；曾任副县长）"
    },
    {
        "id": 9,
        "name": "郭勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共卢氏县委员会",
        "source": "卢氏县政府网县委十三届五次全会报道（主席台就座常委郭勇）"
    },
    {
        "id": 10,
        "name": "丁娜娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记、县监委主任候选人",
        "current_org": "卢氏县纪律检查委员会",
        "source": "卢氏县纪委监委网站（2026-06-04）：丁娜娜，现任卢氏县委常委、县纪委书记、提名为县监察委员会主任候选人"
    },
    {
        "id": 11,
        "name": "李庆锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县纪委书记、县监委主任",
        "current_org": "卢氏县纪律检查委员会",
        "source": "卢氏县纪委监委网站领导机构（此前任纪委书记/监委主任；2026.02 仍以县领导身份出席市人代会议）"
    },
    {
        "id": 12,
        "name": "潘宇明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "卢氏县人民政府",
        "source": "卢氏县政府网领导之窗：潘宇明，男，汉族，人民政府副县长（自然资源/住建/城市管理/商务/生态环境等）"
    },
    {
        "id": 13,
        "name": "张杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "卢氏县人民政府",
        "source": "卢氏县政府网要闻（县领导张杰陪同调研；县政府办工作分工建档联系张杰）"
    },
    {
        "id": 14,
        "name": "辛海珍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "卢氏县人民政府",
        "source": "卢氏县十五届人大一次会议（2022.04）选举辛海珍为副县长；县政府办分工联系人"
    },
    {
        "id": 15,
        "name": "贺鹏飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "卢氏县人民政府",
        "source": "卢氏县政府办工作分工（张越同志联系贺鹏飞工作）"
    },
    {
        "id": 16,
        "name": "许金星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "卢氏县人民政府",
        "source": "卢氏县政府网要闻（县政府常务会，县领导许金星出席；县政府办分工）"
    },
    {
        "id": 17,
        "name": "王俊杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "卢氏县人民政府",
        "source": "卢氏县政府办工作分工（李小伟同志联系张杰、王俊杰等）"
    },
    {
        "id": 18,
        "name": "李春刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "卢氏县人民政府",
        "source": "卢氏县政府网要闻（县委常委会（扩大）会议，副县长李春刚交流发言；县政府办分工联系）"
    },
    {
        "id": 19,
        "name": "吴文峡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "卢氏县政协",
        "source": "三门峡市政协网及卢氏县政府网：县政协党组书记、主席吴文峡"
    },
    {
        "id": 20,
        "name": "李敏霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "卢氏县人大常委会",
        "source": "卢氏县十五届人大一次会议（2022.04）/两会报道（人大副主任李敏霞）"
    },
    {
        "id": 21,
        "name": "吴德方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "卢氏县人大常委会",
        "source": "卢氏县十五届人大一次会议（2022.04）选举吴德方为副主任"
    },
    {
        "id": 22,
        "name": "王燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "卢氏县人大常委会",
        "source": "卢氏县十五届人大一次会议（2022.04）选举王燕为副主任"
    },
    {
        "id": 23,
        "name": "王亚萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人民法院院长",
        "current_org": "卢氏县人民法院",
        "source": "卢氏县十五届人大一次会议（2022.04）选举王亚萍为县人民法院院长"
    },
    {
        "id": 24,
        "name": "刘京锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人民检察院检察长",
        "current_org": "卢氏县人民检察院",
        "source": "卢氏县十五届人大一次会议（2022.04）选举刘京锋为县人民检察院检察长；县委常委会报道列席"
    },
    # ═══════ 前任期 ═══════
    {
        "id": 25,
        "name": "王清华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "三门峡市委常委、宣传部部长（前任卢氏县委书记）",
        "current_org": "三门峡市委",
        "source": "维基百科：王清华（1968年生）2021.08起任卢氏县委书记；2025.02 要闻披露其已任三门峡市委常委、宣传部部长"
    },
    {
        "id": 26,
        "name": "张晓燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任卢氏县县长（卸任）",
        "current_org": "卢氏县人民政府",
        "source": "维基百科/刘万增：2021.07 万增接替张晓燕任卢氏县长"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共卢氏县委员会", "type": "党委", "level": "县处级", "parent": "中共三门峡市委", "location": "卢氏县"},
    {"id": 2, "name": "卢氏县人民政府", "type": "政府", "level": "县处级", "parent": "三门峡市人民政府", "location": "卢氏县"},
    {"id": 3, "name": "卢氏县人大常委会", "type": "人大", "level": "县处级", "parent": "三门峡市人大常委会", "location": "卢氏县"},
    {"id": 4, "name": "卢氏县政协", "type": "政协", "level": "县处级", "parent": "三门峡市政协", "location": "卢氏县"},
    {"id": 5, "name": "卢氏县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "三门峡市纪委监委", "location": "卢氏县"},
    {"id": 6, "name": "卢氏县人民法院", "type": "司法", "level": "县处级", "parent": "三门峡市中级人民法院", "location": "卢氏县"},
    {"id": 7, "name": "卢氏县人民检察院", "type": "司法", "level": "县处级", "parent": "三门峡市人民检察院", "location": "卢氏县"},
    {"id": 8, "name": "三门峡市委", "type": "党委", "level": "地厅级", "parent": "河南省委", "location": "三门峡市"},
    {"id": 9, "name": "三门峡市人民政府", "type": "政府", "level": "地厅级", "parent": "河南省政府", "location": "三门峡市"},
    {"id": 10, "name": "渑池县人民政府", "type": "政府", "level": "县处级", "parent": "三门峡市人民政府", "location": "渑池县"},
    {"id": 11, "name": "三门峡市陕州区人民政府", "type": "政府", "level": "县处级", "parent": "三门峡市人民政府", "location": "陕州区"},
    {"id": 12, "name": "三门峡市城乡一体化示范区（高新技术产业开发区）", "type": "发展区", "level": "县处级", "parent": "三门峡市人民政府", "location": "三门峡市"},
    {"id": 13, "name": "河南省委办公厅", "type": "党委", "level": "省部级", "parent": "河南省委", "location": "郑州市"},
    {"id": 14, "name": "三门峡市委办公室", "type": "党委", "level": "地厅级", "parent": "三门峡市委", "location": "三门峡市"},
    {"id": 15, "name": "中国共产党三门峡市湖滨区委员会", "type": "党委", "level": "县处级", "parent": "三门峡市委", "location": "湖滨区"},
    {"id": 16, "name": "中国共产党义马市委员会", "type": "党委", "level": "县处级", "parent": "三门峡市委", "location": "义马市"},
    {"id": 17, "name": "三门峡市城市管理局", "type": "政府", "level": "县处级", "parent": "三门峡市人民政府", "location": "三门峡市"},
    {"id": 18, "name": "渑池县委", "type": "党委", "level": "县处级", "parent": "三门峡市委", "location": "渑池县"},
]

# ── Positions (person → org with title) ────────────────────────────────────
# id: (person, org, title, start, end, rank, note)
positions = [
    # 胡志权
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2023-05", "end_date": "present", "rank": "县处级正职", "note": "2023.05 河南省委、三门峡市委决定，接替王清华"},
    {"person_id": 1, "org_id": 5, "title": "县人武部党委第一书记", "start_date": "", "end_date": "present", "rank": "县处级", "note": "兼任"},
    {"person_id": 1, "org_id": 12, "title": "三门峡示范区（高新区）党工委书记", "start_date": "2021", "end_date": "2023-05", "rank": "县处级正职", "note": "拟任县委书记前的职务"},
    {"person_id": 1, "org_id": 11, "title": "陕州区区长", "start_date": "2017-12", "end_date": "2021", "rank": "县处级正职", "note": "2017.12代区长，2018.01当选；主持区政府全面工作"},
    {"person_id": 1, "org_id": 14, "title": "三门峡市委副秘书长、市委政研室主任", "start_date": "2014-08", "end_date": "2017-12", "rank": "县处级", "note": "正县（2016.02 兼市委政策研究室主任）"},
    {"person_id": 1, "org_id": 10, "title": "渑池县副县长", "start_date": "2013-08", "end_date": "2014-08", "rank": "县处级副职", "note": "2013.09任渑池县委常委、副县长"},
    {"person_id": 1, "org_id": 13, "title": "省委办公厅督查检查室副主任", "start_date": "2008-12", "end_date": "2013-08", "rank": "乡科级", "note": "督查室副处长"},
    {"person_id": 1, "org_id": 13, "title": "省委办公厅督促检查室主任/副主任科员", "start_date": "2002-06", "end_date": "2008-12", "rank": "乡科级", "note": "督促检查室主任科员"},
    {"person_id": 1, "org_id": 13, "title": "省信访局联络处科员", "start_date": "1997-09", "end_date": "2003-12", "rank": "乡科级", "note": "干部→科员→副主任科员（通过省委信访系统）"},
    # 刘万增
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2021-10-23", "end_date": "present", "rank": "县处级正职", "note": "2021.07.12任代县长，2021.10.23当选"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2021-08-11", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "副县长（首次在卢氏）", "start_date": "2012-02", "end_date": "2014-08", "rank": "县处级副职", "note": "早年任卢氏副县长"},
    {"person_id": 2, "org_id": 17, "title": "三门峡市城市管理局局长", "start_date": "", "end_date": "2021-07", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 16, "title": "义马市委常委、常务副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "义马市委常委、市政府党组副书记、常务副市长"},
    {"person_id": 2, "org_id": 15, "title": "湖滨区委常委、组织部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 14, "title": "三门峡市委办公室工作人员", "start_date": "2002-08", "end_date": "", "rank": "乡科级", "note": "历任市委办公室常委办/办公室主任等"},
    # 王磊
    {"person_id": 3, "org_id": 3, "title": "县人大常委会主任", "start_date": "2026-01", "end_date": "present", "rank": "县处级正职", "note": "2026年初起任；此前为县委副书记、县委办主任"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "仍兼任县委副书记"},
    # 王昱
    {"person_id": 4, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 孙丽松
    {"person_id": 5, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 王星
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "常务副县长、党组副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责县政府常务工作"},
    # 吕宏伟
    {"person_id": 7, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副县长（前）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "曾任副县长"},
    # 卫军强
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 郭勇
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体分工待查"},
    # 丁娜娜
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 5, "title": "纪委书记、监委主任候选人", "start_date": "2026-06-04", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 李庆锋
    {"person_id": 11, "org_id": 5, "title": "县纪委书记、监委主任", "start_date": "", "end_date": "2026", "rank": "县处级副职", "note": "2026年前后卸任"},
    # 副县长们
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管自然资源、住建、城管、商务、生态环境等"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "2022-04", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 四套班子
    {"person_id": 19, "org_id": 4, "title": "县政协主席、党组书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "县人大常委会副主任", "start_date": "2022-04", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 21, "org_id": 3, "title": "县人大常委会副主任", "start_date": "2022-04", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 22, "org_id": 3, "title": "县人大常委会副主任", "start_date": "2022-04", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 23, "org_id": 6, "title": "县人民法院院长", "start_date": "2022-04", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 24, "org_id": 7, "title": "县人民检察院检察长", "start_date": "2022-04", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 前任期
    {"person_id": 25, "org_id": 8, "title": "三门峡市委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": ""},
    {"person_id": 25, "org_id": 1, "title": "县委书记（前任）", "start_date": "2021-08", "end_date": "2023-05", "rank": "县处级正职", "note": "胡志权的前任"},
    {"person_id": 26, "org_id": 2, "title": "县长（前任）", "start_date": "", "end_date": "2021-07", "rank": "县处级正职", "note": "刘万增的前任"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "胡志权任县委书记，刘万增任县长，为卢氏县党政正职搭档", "overlap_org": "卢氏县", "overlap_period": "2023-05 至今"},
    # 书记交接
    {"person_a": 25, "person_b": 1, "type": "predecessor_successor", "context": "王清华卸任卢氏县委书记，胡志权2023.05接任", "overlap_org": "中共卢氏县委员会", "overlap_period": "2023-05"},
    # 县长交接
    {"person_a": 26, "person_b": 2, "type": "predecessor_successor", "context": "张晓燕卸任卢氏县长，刘万增2021.07代任、10月当选", "overlap_org": "卢氏县人民政府", "overlap_period": "2021"},
    # 刘万增—常务副县长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "刘万增任县长，王星任常务副县长协助县长工作", "overlap_org": "卢氏县人民政府", "overlap_period": "当前"},
    # 书记—组织部长（人事权）
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "胡志权任县委书记，王昱任县委常委、组织部长——干部人事系统", "overlap_org": "中共卢氏县委员会", "overlap_period": "当前"},
    # 书记—政法委书记
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "胡志权任县委书记，孙丽松任政法委书记", "overlap_org": "中共卢氏县委员会", "overlap_period": "当前"},
    # 书记—纪委书记
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "胡志权任县委书记，丁娜娜任县纪委书记", "overlap_org": "中共卢氏县委员会", "overlap_period": "2026"},
    # 纪委交接
    {"person_a": 11, "person_b": 10, "type": "predecessor_successor", "context": "李庆锋卸任纪委书记，丁娜娜2026接任（监委主任候选人）", "overlap_org": "卢氏县纪律检查委员会", "overlap_period": "2026"},
    # 人大主任交接
    {"person_a": 3, "person_b": 19, "type": "overlap", "context": "王磊任县人大常委会主任、兼任县委副书记，吴文峡任县政协主席", "overlap_org": "卢氏县四套班子", "overlap_period": "当前"},
    # 胡志权—三门峡系统渊源（曾任渑池副县长、陕州区区长、示范区书记）
    {"person_a": 1, "person_b": 2, "type": "same_system", "context": "刘万增长期在三门峡市委/湖滨/义马/城市管理局任职，胡志权2013年后也在三门峡体系（渑池、陕州区、示范区）任职", "overlap_org": "三门峡市", "overlap_period": "2013-2023"},
    # 主要副县长与党政主官同班子
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "王星任常务副县长，潘宇明任副县长，同属县政府班子", "overlap_org": "卢氏县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "刘万增任县长，张杰任副县长", "overlap_org": "卢氏县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "刘万增任县长，辛海珍任副县长", "overlap_org": "卢氏县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 18, "type": "overlap", "context": "刘万增任县长，李春刚任副县长", "overlap_org": "卢氏县人民政府", "overlap_period": "当前"},
]


# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "胡志权",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "三门峡市",
                "region": "卢氏县",
                "job": "县委书记",
                "task_id": "henan_卢氏县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_lushi_huzhiquan",
                "name": "胡志权",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1971-07",
                "birthplace": "河南柘城",
                "native_place": "河南柘城",
                "education": [
                    {
                        "period": "1989.09-1993.07",
                        "institution": "河南师范大学政教系",
                        "major": "思想政治教育",
                        "degree": "文学学士",
                        "study_type": "full_time",
                        "source_ids": ["S003"]
                    }
                ],
                "party_join": "1993-01",
                "work_start": "1993-07",
                "dedupe_keys": {
                    "name_birth": "胡志权_1971",
                    "name_birthplace": "胡志权_河南柘城",
                    "official_profile_url": "https://www.lushixian.gov.cn/"
                }
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共卢氏县委员会",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"]
            },
            "career_timeline": [
                {"start": "2023-05", "end": "present", "org": "中共卢氏县委员会", "title": "县委书记", "level": "县处级正职", "location": "卢氏县", "system": "party", "rank": "正处", "is_key_promotion": True, "notes": "2023.05 河南省委、市委决定接替王清华", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "2021", "end": "2023-05", "org": "三门峡市城乡一体化示范区", "title": "党工委书记", "level": "县处级正职", "location": "三门峡市", "system": "other", "rank": "正职", "is_key_promotion": False, "notes": "拟任卢氏书记前在任", "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2017-12", "end": "2021", "org": "三门峡市陕州区人民政府", "title": "区长", "level": "县处级正职", "location": "陕州区", "system": "government", "rank": "正职", "is_key_promotion": True, "notes": "2018.01 当选区长", "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2014-08", "end": "2017-12", "org": "三门峡市委", "title": "市委副秘书长（兼市政策研究室主任）", "level": "县处级", "location": "三门峡市", "system": "party", "rank": "正县", "is_key_promotion": False, "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2013-08", "end": "2014-08", "org": "渑池县", "title": "县委常委、副县长", "level": "县处级副职", "location": "渑池县", "system": "government", "rank": "副职", "is_key_promotion": False, "notes": "由省委办公厅下派", "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2008-12", "end": "2013-08", "org": "河南省委办公厅", "title": "督促检查室副主任", "level": "乡级", "location": "郑州市", "system": "party", "rank": "副处", "is_key_promotion": False, "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2002-06", "end": "2008-12", "org": "河南省委办公厅", "title": "督促检查室主任科员/副主任科员", "level": "乡级", "location": "郑州市", "system": "party", "rank": "科级", "is_key_promotion": False, "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "1996-09", "end": "2002-06", "org": "河南省信访局", "title": "联络处干部/科员", "level": "乡级", "location": "郑州市", "system": "other", "rank": "科级", "is_key_promotion": False, "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "1993-07", "end": "1996-09", "org": "新乡市和平实业公司", "title": "工作人员", "level": "", "location": "新乡市", "system": "other", "rank": "", "is_key_promotion": False, "confidence": "confirmed", "source_ids": ["S003"]}
            ],
            "organizations": [
                {"name": "中共卢氏县委员会", "role": "县委书记", "period": "2023-05至今", "source_ids": ["S001", "S002"]},
                {"name": "三门峡市城乡一体化示范区", "role": "党工委书记", "period": "2021-2023", "source_ids": ["S003"]},
                {"name": "三门峡市陕州区人民政府", "role": "区长", "period": "2017-2021", "source_ids": ["S003"]},
                {"name": "三门峡市委", "role": "市委副秘书长、政策研究室主任", "period": "2014-2017", "source_ids": ["S003"]},
                {"name": "渑池县", "role": "县委常委、副县长", "period": "2013-2014", "source_ids": ["S003"]},
                {"name": "河南省委办公厅", "role": "督促检查室副主任等", "period": "2002-2013", "source_ids": ["S003"]}
            ],
            "relationships": [
                {"person": "刘万增", "person_id": "henan_lushi_liuwanzeng", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "胡志权任县委书记，刘万增任县长，党政正职搭档", "overlap_org": "卢氏县", "overlap_period": "2023-05至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"person": "王清华", "person_id": "henan_lushi_wangqinghua", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "胡志权接替王清华任卢氏县委书记", "overlap_org": "中共卢氏县委员会", "overlap_period": "2023-05", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S002"]},
                {"person": "王昱", "person_id": "henan_lushi_wangyu", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "王昱任县委常委、组织部长，干部人事归县委书记", "overlap_org": "中共卢氏县委员会", "overlap_period": "当前", "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S004"]}
            ],
            "governance_record": [
                {"period": "2026", "domain": "economic_development", "achievement_or_event": "推进成品油税收征管、食用菌产业数字化、网络货运平台等改革（2026.02 与省非煤办座谈）", "role_in_event": "主导推动", "measurable_outcome": "", "location": "卢氏县", "confidence": "confirmed", "source_ids": ["S006"]},
                {"period": "2026", "domain": "rural_revitalization", "achievement_or_event": "深入乡镇调研红色资源、项目建设、产业发展、乡村振兴", "role_in_event": "带队调研", "measurable_outcome": "", "location": "卢氏县木桐乡等", "confidence": "confirmed", "source_ids": ["S006"]},
                {"period": "2025", "domain": "education", "achievement_or_event": "在第四届国家工业遗产大会上作《以工业文化教育实践破题构建县域经济高质量发展新格局》主旨演讲", "role_in_event": "主旨演讲", "measurable_outcome": "", "location": "卢氏县", "confidence": "confirmed", "source_ids": ["S007"]}
            ],
            "professional_profile": {
                "primary_specializations": ["县域经济", "工业文化/产业转型", "省委办公厅督查出身"],
                "secondary_specializations": ["食用菌产业", "数字化治税"],
                "career_pattern": "provincial_department",
                "systems_experience": ["party", "government", "other"],
                "geographic_pattern": ["河南省委系统", "三门峡市", "卢氏县"],
                "promotion_velocity": {"summary": "1993-2013年在省委系统晋升，2013年下派三门峡任渑池副县长，后逐步任市委副秘书长、区长、示范区书记、县委书记", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "grassroots_oriented", "evidence": "多次深入乡镇（木桐乡、徐家湾乡、双龙湾镇）调研红色资源、产业、乡村振兴", "confidence": "plausible", "source_ids": ["S006"]},
                    {"trait": "reform_oriented", "evidence": "推动科技治税、食用菌数字化等改革创新", "confidence": "plausible", "source_ids": ["S006"]}
                ],
                "speech_themes": ["现代化卢氏建设", "产业转型升级", "乡村振兴"],
                "management_signals": ["强调挂图作战、压实责任", "重视红色资源开发"],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}],
            "source_register": [
                {"id": "S001", "title": "河南省委组织部拟任职公示（胡志权拟任县委书记）", "url": "https://m.henan100.com/news/2023/1149852.shtml", "publisher": "河南一百度", "published_at": "2023", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "确认拟任前职务为示范区党工委书记及出生年月"},
                {"id": "S002", "title": "卢氏县全县领导干部会议·宣布省委、市委决定胡志权任书记", "url": "https://app.dahecube.com/nweb/news/20230517/...", "publisher": "大河报", "published_at": "2023-05-17", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "胡志权接替王清华任卢氏县委书记"},
                {"id": "S003", "title": "胡志权履历（求闻百科/百科）", "url": "https://www.qiuwenbaike.cn/wiki/%E8%83%A1%E5%BF%97%E6%9D%83", "publisher": "求闻百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "给出 1989-2018 完整履历"},
                {"id": "S004", "title": "卢氏县委十三届五次全会报道", "url": "https://www.lushixian.gov.cn/1710/616544928/1170805.html", "publisher": "卢氏县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认县委常委会名单（胡志权、刘万增、王磊、王昱、孙丽松、王星、李庆锋、卫军强、郭勇、吕宏伟）"},
                {"id": "S006", "title": "胡志权赴省非煤办座谈（科技治税/食用菌）", "url": "https://www.lushixian.gov.cn/1710/617008896/1904374.html", "publisher": "卢氏县人民政府", "published_at": "2026-02-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "治理选段"},
                {"id": "S007", "title": "卢氏县委书记胡志权第四届国家工业遗产大会主旨演讲", "url": "https://www.hnjjbs.com/article/2025-11/176317661036968.html", "publisher": "河南经济报", "published_at": "2025-11-15", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "工业文化教育实践基地建设"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "complete",
                "relationship_confidence": "high",
                "biggest_gap": "胡志权2021-2023示范区党工委书记期间及卸任卢氏县长(2022)前的人事细节；部分任职精确日期待核"
            },
            "open_questions": [
                {"priority": "medium", "question": "胡志权2018-2021年间任陕州区区长、何时转任示范区党工委书记？", "why_it_matters": "精确交接时间", "suggested_queries": ["胡志权 陕州区长 示范区 党工委 时间"], "last_attempted": AS_OF},
                {"priority": "low", "question": "胡志权在担任县委书记前示范区任内的具体成绩与人事网络？", "why_it_matters": "扩充其跨领域网络", "suggested_queries": ["胡志权 示范区 高新区 2022"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "id": 2,
        "name": "刘万增",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "三门峡市",
                "region": "卢氏县",
                "job": "县长",
                "task_id": "henan_卢氏县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_lushi_liuwanzeng",
                "name": "刘万增",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1978",
                "birthplace": "河南郏县",
                "native_place": "河南郏县",
                "education": [{"period": "1998-2002", "institution": "兰州大学", "major": "", "degree": "大学", "study_type": "full_time", "source_ids": ["S011"]}],
                "party_join": "2000-01",
                "work_start": "2002-08",
                "dedupe_keys": {
                    "name_birth": "刘万增_1978",
                    "name_birthplace": "刘万增_河南郏县",
                    "official_profile_url": "https://www.lushixian.gov.cn/"
                }
            },
            "current_status": {
                "current_post": "县长",
                "current_org": "卢氏县人民政府",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S010", "S011"]
            },
            "career_timeline": [
                {"start": "2021-10-23", "end": "present", "org": "卢氏县人民政府", "title": "县长", "level": "县处级正职", "location": "卢氏县", "system": "government", "rank": "正职", "is_key_promotion": True, "notes": "2021.07.12代县长,10.23当选", "confidence": "confirmed", "source_ids": ["S010", "S011"]},
                {"start": "2021-08-11", "end": "present", "org": "中共卢氏县委员会", "title": "县委副书记", "level": "县处级副职", "location": "卢氏县", "system": "party", "rank": "副职", "is_key_promotion": False, "confidence": "confirmed", "source_ids": ["S011"]},
                {"start": "", "end": "2021-07", "org": "三门峡市城市管理局", "title": "局长", "level": "县处级正职", "location": "三门峡市", "system": "government", "rank": "正职", "is_key_promotion": False, "confidence": "confirmed", "source_ids": ["S011"]},
                {"start": "", "end": "", "org": "义马市委/政府", "title": "市委常委、常务副市长", "level": "县处级副职", "location": "义马市", "system": "party", "rank": "副职", "is_key_promotion": False, "notes": "市政府党组副书记兼常务副市长", "confidence": "confirmed", "source_ids": ["S011"]},
                {"start": "", "end": "", "org": "三门峡市湖滨区委", "title": "区委常委、组织部长", "level": "县处级副职", "location": "湖滨区", "system": "party", "rank": "副职", "is_key_promotion": False, "confidence": "confirmed", "source_ids": ["S011"]},
                {"start": "2012-02", "end": "2014-08", "org": "卢氏县人民政府", "title": "副县长", "level": "县处级副职", "location": "卢氏县", "system": "government", "rank": "副职", "is_key_promotion": False, "confidence": "confirmed", "source_ids": ["S011"]},
                {"start": "2002-08", "end": "", "org": "三门峡市委办公室", "title": "工作人员", "level": "", "location": "三门峡市", "system": "party", "rank": "", "is_key_promotion": False, "confidence": "confirmed", "source_ids": ["S011"]}
            ],
            "organizations": [
                {"name": "卢氏县人民政府", "role": "县长", "period": "2021-至今", "source_ids": ["S010", "S011"]},
                {"name": "中共卢氏县委员会", "role": "县委副书记", "period": "2021-至今", "source_ids": ["S011"]},
                {"name": "三门峡市城市管理局", "role": "局长", "period": "", "source_ids": ["S011"]},
                {"name": "义市市委/政府", "role": "市委常委、常务副市长", "period": "", "source_ids": ["S011"]},
                {"name": "三门峡市湖滨区委", "role": "区委常委、组织部长", "period": "", "source_ids": ["S011"]},
                {"name": "三门峡市委办公室", "role": "工作人员", "period": "2002-08起", "source_ids": ["S011"]}
            ],
            "relationships": [
                {"person": "胡志权", "person_id": "henan_lushi_huzhiquan", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "刘万增任县长，胡志权任县委书记，党政正职搭档", "overlap_org": "卢氏县", "overlap_period": "2023-至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001", "S010"]},
                {"person": "王星", "person_id": "henan_lushi_wangxing", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "王星任常委会、常务副县长协助县长", "overlap_org": "卢氏县人民政府", "overlap_period": "当前", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S008"]},
                {"person": "张晓燕", "person_id": "henan_lushi_zhangxiaoyan", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "刘万增接替张晓燕任卢氏县长", "overlap_org": "卢氏县人民政府", "overlap_period": "2021-07", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S011"]}
            ],
            "governance_record": [
                {"period": "2024", "domain": "economic_development", "achievement_or_event": "作2025年政府工作报告：GDP 149.5亿增5.3%全市第一，规上工业增10.7%全市第一", "role_in_event": "代表县政府报告", "measurable_outcome": "GDP增速全市第一", "location": "卢氏县", "confidence": "confirmed", "source_ids": ["S013"]}
            ],
            "professional_profile": {
                "primary_specializations": ["综合经济", "政府全面工作", "政法审计"],
                "secondary_specializations": [],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["government", "party", "organization"],
                "geographic_pattern": ["河南郏县", "兰州大学", "三门峡市", "卢氏县"],
                "promotion_velocity": {"summary": "2002-2021近20年在三门峡体系（市委办、湖滨、义马、城市管理局）历练，2021.07接任卢氏县长", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"label": "pragmatic", "evidence": "政府工作报告重点部署产业发展、项目建设、服务企业、招商引资", "confidence": "plausible", "source_ids": ["S012"]}
                ],
                "speech_themes": ["拼经济、稳中向好", "壮大产业、招商引资", "保障民生实事"],
                "management_signals": [],
                "caveat": "Work style inferred from public records."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}],
            "source_register": [
                {"id": "S010", "title": "刘万增当选卢氏县县长（大河网）", "url": "https://news.dahe.cn/2021/10-24/915798.html", "publisher": "大河网", "published_at": "2021-10-24", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "2021.10.23当选县长"},
                {"id": "S011", "title": "刘万增（维基百科）", "url": "https://zh.wikipedia.org/zh-hans/%E5%88%98%E4%B8%87%E5%A2%9E", "publisher": "维基百科", "published_at": "2021-08-12", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "完整履历（兰州大学、市委办、湖滨、义(马、城管局、卢氏副县长）"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "complete",
                "relationship_confidence": "high",
                "biggest_gap": "刘万增2014年卸任卢氏副县长至任城市管理局局长/2021任县长间的精确时间与中间任职待核"
            },
            "open_questions": [
                {"priority": "medium", "question": "刘万增2014-2021历年任职时间线与岗位？", "why_it_matters": "还原跨县调动链条", "suggested_queries": ["刘万增 龙门 城管局局长 时间", "刘万增 简历 卢氏 县长"], "last_attempted": AS_OF}
            ]
        }
    },
]


# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

    # Write DB + GEXF to staging
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

    # Write person JSON files
    for pf in person_files_data:
        fname = f"{TODAY}-河南省-三门峡市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  ✅ Person JSON: {path}")

    print(f"\n📦 Staged DB: {DB_PATH}")
    print(f"📦 Staged GEXF: {GEXF_PATH}")
    print(f"\n✅ Done — {SLUG} data staged (validate then promote via process_tmp.py).")


if __name__ == "__main__":
    main()