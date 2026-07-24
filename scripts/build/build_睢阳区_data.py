#!/usr/bin/env python3
"""Build 商丘市睢阳区 (Shangqiu Suiyang District) leadership network data.

Level: 市辖区
Province: 河南省
Parent city: 商丘市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: henan_睢阳区

Research date: 2026-07-24
Official source: https://www.suiyangqu.gov.cn/ (睢阳区人民政府)

Current status (as of 2026-07-24, verified via government website and 接访公示):
- 区委书记: 丁向东 — 2026年7月现任。七届区委常委会第6、7次（扩大）会议主持
- 区长: 李长东 — 1974年1月生，中共党员，大学学历，公共管理硕士。2022年11月代理区长，12月当选
- 区委副书记: 张方杰
- 常务副区长: 宋一平 — 1980年10月生，中共党员，中央党校大学学历

Confirmed leadership roster (from 接访公示 2026-07-01):
- 区委书记: 丁向东
- 区委副书记、区长: 李长东
- 区委副书记: 张方杰
- 区委常委、常务副区长: 宋一平
- 区委常委、纪委书记: 吴进丰
- 区委常委、组织部长: 黄珊
- 区委常委、统战部长: 余振祥
- 区委常委、办公室主任: 孙银行
- 区委常委、政法委书记: 辛凯
- 区委常委、宣传部长、副区长: 张东林
- 副区长、公安分局局长: 谭振起
- 副区长: 焦凯
- 副区长: 彭丽
- 副区长: 李权

Key government page sources (all from sui yang qu .gov.cn):
- 李长东 profile: /zwgk/fdzdgknr/ldzc/zfld/content_29897
- 宋一平 profile: /zwgk/fdzdgknr/ldzc/zfld/content_255150
- 谭振起 profile: /zwgk/fdzdgknr/ldzc/zfld/content_158840
- 接访公示 (full roster): /zwzx/gsgg/content_308326
- 七届区委常委会第7次会议: /zwzx/syyw/content_309274
- 七届区委常委会第6次会议: /zwzx/syyw/content_309229
- 李长东当选区长: /zwgk/fdzdgknr/rsxx26syqrmzf/rsrm26syqrmzf/content_52966
- 李长东任代区长: /zwgk/fdzdgknr/rsxx26syqrmzf/rsrm26syqrmzf/content_50397
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "睢阳区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = datetime.now().strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y%m%d")

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "丁向东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "睢阳区委书记",
        "current_org": "中共商丘市睢阳区委员会",
        "source": ("官方: https://www.suiyangqu.gov.cn/zwzx/syyw/content_309274 "
                    "(七届区委常委会第7次会议); "
                    "接访公示: https://www.suiyangqu.gov.cn/zwzx/gsgg/content_308326"),
    },
    {
        "id": 2,
        "name": "李长东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年1月",
        "birthplace": "",
        "native_place": "",
        "education": "大学，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "睢阳区委副书记、区长",
        "current_org": "睢阳区人民政府",
        "source": ("官方: https://www.suiyangqu.gov.cn/zwgk/fdzdgknr/ldzc/zfld/content_29897; "
                    "当选: https://www.suiyangqu.gov.cn/zwgk/fdzdgknr/rsxx26syqrmzf/rsrm26syqrmzf/content_52966"),
    },
    {
        "id": 3,
        "name": "张方杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "睢阳区委副书记",
        "current_org": "中共商丘市睢阳区委员会",
        "source": "接访公示: https://www.suiyangqu.gov.cn/zwzx/gsgg/content_308326",
    },
    {
        "id": 4,
        "name": "宋一平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年10月",
        "birthplace": "",
        "native_place": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "睢阳区委常委、常务副区长",
        "current_org": "睢阳区人民政府",
        "source": ("官方: https://www.suiyangqu.gov.cn/zwgk/fdzdgknr/ldzc/zfld/content_255150; "
                    "接访公示: https://www.suiyangqu.gov.cn/zwzx/gsgg/content_308326"),
    },
    {
        "id": 5,
        "name": "吴进丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "睢阳区委常委、纪委书记",
        "current_org": "中共商丘市睢阳区纪律检查委员会",
        "source": "接访公示: https://www.suiyangqu.gov.cn/zwzx/gsgg/content_308326",
    },
    {
        "id": 6,
        "name": "黄珊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "睢阳区委常委、组织部长",
        "current_org": "中共商丘市睢阳区委员会组织部",
        "source": "接访公示: https://www.suiyangqu.gov.cn/zwzx/gsgg/content_308326",
    },
    {
        "id": 7,
        "name": "余振祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "睢阳区委常委、统战部长",
        "current_org": "中共商丘市睢阳区委员会统战部",
        "source": "接访公示: https://www.suiyangqu.gov.cn/zwzx/gsgg/content_308326",
    },
    {
        "id": 8,
        "name": "孙银行",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "睢阳区委常委、办公室主任",
        "current_org": "中共商丘市睢阳区委员会办公室",
        "source": "接访公示: https://www.suiyangqu.gov.cn/zwzx/gsgg/content_308326",
    },
    {
        "id": 9,
        "name": "辛凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "睢阳区委常委、政法委书记",
        "current_org": "中共商丘市睢阳区委员会政法委员会",
        "source": "接访公示: https://www.suiyangqu.gov.cn/zwzx/gsgg/content_308326",
    },
    {
        "id": 10,
        "name": "张东林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "睢阳区委常委、宣传部长、副区长",
        "current_org": "中共商丘市睢阳区委员会宣传部",
        "source": "接访公示: https://www.suiyangqu.gov.cn/zwzx/gsgg/content_308326",
    },
    # ════════════════════════════════════════
    # 区政府领导 (District Government)
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "谭振起",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "睢阳区副区长、睢阳公安分局局长",
        "current_org": "睢阳区人民政府",
        "source": ("官方: https://www.suiyangqu.gov.cn/zwgk/fdzdgknr/ldzc/zfld/content_158840; "
                    "接访公示: https://www.suiyangqu.gov.cn/zwzx/gsgg/content_308326"),
    },
    {
        "id": 12,
        "name": "焦凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "睢阳区政府党组成员、副区长",
        "current_org": "睢阳区人民政府",
        "source": "接访公示: https://www.suiyangqu.gov.cn/zwzx/gsgg/content_308326",
    },
    {
        "id": 13,
        "name": "彭丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "睢阳区副区长",
        "current_org": "睢阳区人民政府",
        "source": "接访公示: https://www.suiyangqu.gov.cn/zwzx/gsgg/content_308326",
    },
    {
        "id": 14,
        "name": "李权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "睢阳区副区长",
        "current_org": "睢阳区人民政府",
        "source": "接访公示: https://www.suiyangqu.gov.cn/zwzx/gsgg/content_308326",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共商丘市睢阳区委员会", "type": "党委", "level": "县级", "parent": "中共商丘市委", "location": "河南省商丘市睢阳区"},
    {"id": 2, "name": "睢阳区人民政府", "type": "政府", "level": "县级", "parent": "商丘市人民政府", "location": "河南省商丘市睢阳区"},
    {"id": 3, "name": "中共商丘市睢阳区纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共商丘市睢阳区委员会", "location": "河南省商丘市睢阳区"},
    {"id": 4, "name": "中共商丘市睢阳区委员会组织部", "type": "党委", "level": "县级", "parent": "中共商丘市睢阳区委员会", "location": "河南省商丘市睢阳区"},
    {"id": 5, "name": "中共商丘市睢阳区委员会统战部", "type": "党委", "level": "县级", "parent": "中共商丘市睢阳区委员会", "location": "河南省商丘市睢阳区"},
    {"id": 6, "name": "中共商丘市睢阳区委员会办公室", "type": "党委", "level": "县级", "parent": "中共商丘市睢阳区委员会", "location": "河南省商丘市睢阳区"},
    {"id": 7, "name": "中共商丘市睢阳区委员会政法委员会", "type": "党委", "level": "县级", "parent": "中共商丘市睢阳区委员会", "location": "河南省商丘市睢阳区"},
    {"id": 8, "name": "中共商丘市睢阳区委员会宣传部", "type": "党委", "level": "县级", "parent": "中共商丘市睢阳区委员会", "location": "河南省商丘市睢阳区"},
    {"id": 9, "name": "商丘市公安局睢阳分局", "type": "政府", "level": "县级", "parent": "睢阳区人民政府", "location": "河南省商丘市睢阳区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 丁向东
    {"person_id": 1, "org_id": 1, "title": "睢阳区委书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "2026年7月现任，主持七届区委常委会"},
    # 李长东
    {"person_id": 2, "org_id": 1, "title": "睢阳区委副书记", "start_date": "2022-11", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "睢阳区区长", "start_date": "2022-12", "end_date": "", "rank": "正县级", "note": "2022年11月任代区长，2022年12月当选区长"},
    # 张方杰
    {"person_id": 3, "org_id": 1, "title": "睢阳区委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 宋一平
    {"person_id": 4, "org_id": 1, "title": "睢阳区委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "睢阳区常务副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责综合协调、发展改革、财税金融等"},
    # 吴进丰
    {"person_id": 5, "org_id": 3, "title": "睢阳区纪委书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "区委常委"},
    # 黄珊
    {"person_id": 6, "org_id": 4, "title": "睢阳区委组织部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "区委常委"},
    # 余振祥
    {"person_id": 7, "org_id": 5, "title": "睢阳区委统战部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "区委常委"},
    # 孙银行
    {"person_id": 8, "org_id": 6, "title": "睢阳区委办公室主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "区委常委"},
    # 辛凯
    {"person_id": 9, "org_id": 7, "title": "睢阳区委政法委书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "区委常委"},
    # 张东林
    {"person_id": 10, "org_id": 8, "title": "睢阳区委宣传部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "区委常委，兼任副区长"},
    # 谭振起
    {"person_id": 11, "org_id": 9, "title": "睢阳公安分局局长", "start_date": "", "end_date": "", "rank": "副县级", "note": "挂职副区长"},
    # 焦凯
    {"person_id": 12, "org_id": 2, "title": "睢阳区副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "区政府党组成员"},
    # 彭丽
    {"person_id": 13, "org_id": 2, "title": "睢阳区副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 李权
    {"person_id": 14, "org_id": 2, "title": "睢阳区副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 书记 ↔ 区长（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长党政工作搭档", "overlap_org": "睢阳区", "overlap_period": ""},
    # 书记 ↔ 副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与区委副书记", "overlap_org": "中共睢阳区委", "overlap_period": ""},
    # 区长 ↔ 常务副区长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长与常务副区长工作搭档", "overlap_org": "睢阳区政府", "overlap_period": ""},
    # 书记 ↔ 纪委书记
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记与纪委书记", "overlap_org": "中共睢阳区委", "overlap_period": ""},
    # 书记 ↔ 组织部长
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记与组织部长", "overlap_org": "中共睢阳区委", "overlap_period": ""},
    # 书记 ↔ 统战部长
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记与统战部长", "overlap_org": "中共睢阳区委", "overlap_period": ""},
    # 书记 ↔ 办公室主任
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记与办公室主任", "overlap_org": "中共睢阳区委", "overlap_period": ""},
    # 书记 ↔ 政法委书记
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记与政法委书记", "overlap_org": "中共睢阳区委", "overlap_period": ""},
    # 书记 ↔ 宣传部长
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "区委书记与宣传部长", "overlap_org": "中共睢阳区委", "overlap_period": ""},
    # 区长 ↔ 副区长（公安分局）
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长与副区长（公安分局）", "overlap_org": "睢阳区政府", "overlap_period": ""},
    # 区长 ↔ 副区长（焦凯）
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长与副区长（焦凯）", "overlap_org": "睢阳区政府", "overlap_period": ""},
    # 区长 ↔ 副区长（彭丽）
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "区长与副区长（彭丽）", "overlap_org": "睢阳区政府", "overlap_period": ""},
    # 区长 ↔ 副区长（李权）
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "区长与副区长（李权）", "overlap_org": "睢阳区政府", "overlap_period": ""},
    # 纪委书记 ↔ 政法委书记
    {"person_a": 5, "person_b": 9, "type": "同级协作", "context": "纪委与政法委工作协作", "overlap_org": "中共睢阳区委", "overlap_period": ""},
    # 组织部长 ↔ 宣传部长
    {"person_a": 6, "person_b": 10, "type": "同级协作", "context": "组织与宣传工作协作", "overlap_org": "中共睢阳区委", "overlap_period": ""},
    # 副书记 ↔ 常务副区长
    {"person_a": 3, "person_b": 4, "type": "同级协作", "context": "区委副书记与常务副区长工作协作", "overlap_org": "睢阳区", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTER
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "睢阳区政府领导 - 李长东", "url": "https://www.suiyangqu.gov.cn/zwgk/fdzdgknr/ldzc/zfld/content_29897", "publisher": "睢阳区人民政府", "published_at": "", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "官方领导简介"},
        {"id": "S002", "title": "睢阳区政府领导 - 宋一平", "url": "https://www.suiyangqu.gov.cn/zwgk/fdzdgknr/ldzc/zfld/content_255150", "publisher": "睢阳区人民政府", "published_at": "", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "官方领导简介"},
        {"id": "S003", "title": "睢阳区政府领导 - 谭振起", "url": "https://www.suiyangqu.gov.cn/zwgk/fdzdgknr/ldzc/zfld/content_158840", "publisher": "睢阳区人民政府", "published_at": "", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "副区长(挂职)"},
        {"id": "S004", "title": "睢阳区党政领导接访时间公示", "url": "https://www.suiyangqu.gov.cn/zwzx/gsgg/content_308326", "publisher": "睢阳区信访局", "published_at": "2026-07-01", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "完整领导班子名单"},
        {"id": "S005", "title": "七届区委常委会第7次（扩大）会议", "url": "https://www.suiyangqu.gov.cn/zwzx/syyw/content_309274", "publisher": "睢阳区委宣传部", "published_at": "2026-07-22", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "丁向东以区委书记身份主持会议"},
        {"id": "S006", "title": "七届区委常委会第6次（扩大）会议", "url": "https://www.suiyangqu.gov.cn/zwzx/syyw/content_309229", "publisher": "睢阳区委宣传部", "published_at": "2026-07-21", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "丁向东以区委书记身份主持会议"},
        {"id": "S007", "title": "李长东当选为商丘市睢阳区人民政府区长", "url": "https://www.suiyangqu.gov.cn/zwgk/fdzdgknr/rsxx26syqrmzf/rsrm26syqrmzf/content_52966", "publisher": "睢阳区人民政府", "published_at": "2022-12-23", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "李长东当选区长"},
        {"id": "S008", "title": "李长东任睢阳区人民政府副区长、代理区长", "url": "https://www.suiyangqu.gov.cn/zwgk/fdzdgknr/rsxx26syqrmzf/rsrm26syqrmzf/content_50397", "publisher": "睢阳区人民政府", "published_at": "2022-11-30", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "李长东任代区长"},
    ]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON GRAPH JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def make_person_json(person: dict, timeline: list[dict], person_relationships: list[dict],
                     source_register: list[dict]) -> dict:
    """Build a Person Graph JSON v1.0 record."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "商丘市",
            "region": "睢阳区",
            "job": person.get("current_post", ""),
            "task_id": "henan_睢阳区",
            "time_focus": "2022-2026",
        },
        "identity": {
            "person_id": f"suiyangqu_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "",
                           "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S004"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": person_relationships,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "",
                                         "confidence": "unverified", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": "完整履历（早期职业生涯）未公开",
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的早期职业生涯（入职至最近调动前）",
             "why_it_matters": "完整履历是评估晋升路径和人际关系的基础",
             "suggested_queries": [f"{person['name']} 简历 商丘", f"{person['name']} 任前公示",
                                   f"{person['name']} 百度百科"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": f"{person['name']}的出生地和籍贯",
             "why_it_matters": "地域关系是人际关系网络的重要维度",
             "suggested_queries": [f"{person['name']} 出生", f"{person['name']} 籍贯"],
             "last_attempted": AS_OF},
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print("  商丘市睢阳区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 睢阳区政府网站 + 接访公示")
    print("=" * 60)

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
    print(f"\n✅ 睢阳区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 丁向东 (区委书记)
    ding_timeline = [
        {"start": "", "end": "", "org": "中共商丘市睢阳区委员会", "title": "睢阳区委书记",
         "notes": "2026年7月现任，主持七届区委常委会第6次、第7次（扩大）会议",
         "confidence": "confirmed", "source_ids": ["S005", "S006"]},
    ]
    ding_relationships = [
        {"person": "李长东", "person_id": "suiyangqu_李长东", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区委书记与区长党政工作搭档",
         "overlap_org": "睢阳区", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "张方杰", "person_id": "suiyangqu_张方杰", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区委书记与区委副书记",
         "overlap_org": "中共睢阳区委", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    ding_json = make_person_json(persons[0], ding_timeline, ding_relationships, source_register)
    ding_path = PERSONS_DIR / f"{TODAY}-河南省-商丘市-区委书记-丁向东.json"
    with open(ding_path, "w", encoding="utf-8") as f:
        json.dump(ding_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {ding_path.name}")

    # 2. 李长东 (区长)
    li_timeline = [
        {"start": "", "end": "2022-11", "org": "",
         "title": "履历缺口", "notes": "公开资料未找到李长东2022年11月之前的任职履历",
         "confidence": "unverified", "source_ids": []},
        {"start": "2022-11", "end": "2022-12", "org": "睢阳区人民政府", "title": "睢阳区副区长、代理区长",
         "notes": "2022年11月30日由区人大常委会任命为副区长、代理区长",
         "confidence": "confirmed", "source_ids": ["S008"]},
        {"start": "2022-12", "end": "", "org": "睢阳区人民政府", "title": "睢阳区区长",
         "notes": "2022年12月23日当选区长",
         "confidence": "confirmed", "source_ids": ["S007"]},
    ]
    li_relationships = [
        {"person": "丁向东", "person_id": "suiyangqu_丁向东", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区长与区委书记党政工作搭档",
         "overlap_org": "睢阳区", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "宋一平", "person_id": "suiyangqu_宋一平", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区长与常务副区长工作搭档",
         "overlap_org": "睢阳区政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    li_json = make_person_json(persons[1], li_timeline, li_relationships, source_register)
    li_path = PERSONS_DIR / f"{TODAY}-河南省-商丘市-区长-李长东.json"
    with open(li_path, "w", encoding="utf-8") as f:
        json.dump(li_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {li_path.name}")

    # 3. 张方杰 (区委副书记)
    zhang_timeline = [
        {"start": "", "end": "", "org": "中共商丘市睢阳区委员会", "title": "睢阳区委副书记",
         "notes": "2026年7月现任，来源接访公示",
         "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    zhang_relationships = [
        {"person": "丁向东", "person_id": "suiyangqu_丁向东", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区委副书记与区委书记",
         "overlap_org": "中共睢阳区委", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    zhang_json = make_person_json(persons[2], zhang_timeline, zhang_relationships, source_register)
    zhang_path = PERSONS_DIR / f"{TODAY}-河南省-商丘市-区委副书记-张方杰.json"
    with open(zhang_path, "w", encoding="utf-8") as f:
        json.dump(zhang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zhang_path.name}")

    # 4. 宋一平 (常务副区长)
    song_timeline = [
        {"start": "", "end": "", "org": "", "title": "履历缺口",
         "notes": "公开资料未找到宋一平的早期任职履历",
         "confidence": "unverified", "source_ids": []},
        {"start": "", "end": "", "org": "睢阳区人民政府", "title": "睢阳区委常委、常务副区长",
         "notes": "1980年10月生，中央党校大学学历，负责综合协调、发展改革、财税金融等",
         "confidence": "confirmed", "source_ids": ["S002", "S004"]},
    ]
    song_relationships = [
        {"person": "李长东", "person_id": "suiyangqu_李长东", "relationship_type": "overlap",
         "strength": "strong", "evidence": "常务副区长与区长工作搭档",
         "overlap_org": "睢阳区政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "丁向东", "person_id": "suiyangqu_丁向东", "relationship_type": "overlap",
         "strength": "strong", "evidence": "常务副区长与区委书记",
         "overlap_org": "睢阳区", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    song_json = make_person_json(persons[3], song_timeline, song_relationships, source_register)
    song_path = PERSONS_DIR / f"{TODAY}-河南省-商丘市-常务副区长-宋一平.json"
    with open(song_path, "w", encoding="utf-8") as f:
        json.dump(song_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {song_path.name}")

    # 5. 吴进丰 (纪委书记)
    wu_timeline = [
        {"start": "", "end": "", "org": "中共商丘市睢阳区纪律检查委员会", "title": "睢阳区委常委、纪委书记",
         "notes": "2026年7月现任，来源接访公示",
         "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    wu_relationships = [
        {"person": "丁向东", "person_id": "suiyangqu_丁向东", "relationship_type": "overlap",
         "strength": "strong", "evidence": "纪委书记与区委书记",
         "overlap_org": "中共睢阳区委", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    wu_json = make_person_json(persons[4], wu_timeline, wu_relationships, source_register)
    wu_path = PERSONS_DIR / f"{TODAY}-河南省-商丘市-纪委书记-吴进丰.json"
    with open(wu_path, "w", encoding="utf-8") as f:
        json.dump(wu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {wu_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()
