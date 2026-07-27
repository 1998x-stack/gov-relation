#!/usr/bin/env python3
"""Build 武汉市江汉区 (Wuhan Jianghan District) leadership network data.

Level: 市辖区
Province: 湖北省
Parent city: 武汉市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: hubei_江汉区

Research date: 2026-07-24
Official source: https://www.jianghan.gov.cn/ (武汉市江汉区人民政府)
Staging build: data/tmp/hubei_江汉区/ → promoted by process_tmp.py

Current status (as of 2026-07-24, verified via jianghan.gov.cn news):
- 区委书记: 叶文静 — 2026年7月6日主持区委理论学习中心组集体学习；
  7月1日"两优一先"表彰大会讲话；6月30日带领区领导参观龙王庙抗洪精神主题公园
- 区委副书记、区长: 郭小平 — 2026年7月6日参加区委理论学习中心组学习；
  7月1日主持"两优一先"表彰大会
- 区委副书记、区委组织部部长、区委统战部部长: 姜辉 — 三项兼职
- 区委常委、区纪委书记、区监委主任: 毕盛
- 区委常委、副区长: 曹建
- 区领导: 王瑞

Confirmed leadership sources (all from jianghan.gov.cn):
- 区委理论学习中心组学习 (2026-07-06): /xwzx/jhyw/202607/t20260716_2821885.shtml
- 两优一先表彰大会 (2026-07-02): /xwzx/jhyw/202607/t20260716_2821855.shtml
- 弘扬抗洪精神活动 (2026-07-03): /xwzx/jhyw/202607/t20260716_2821849.shtml
- 警示教育会 (2026-06-01): /xwzx/jhyw/202606/t20260612_2776555.shtml
- 正确政绩观推进会 (2026-06-12): /xwzx/jhyw/202606/t20260612_2776552.shtml
- 叶文静赴常青街道调研 (2026-05-18): /tpxw/202605/t20260522_2767445.shtml
- 海峡两岸金融恳谈会 (2026-07-13): /xwzx/jhyw/202607/t20260716_2821833.shtml
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

SLUG = "江汉区"

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
        "name": "叶文静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江汉区委书记",
        "current_org": "中共武汉市江汉区委员会",
        "source": ("江汉区政府官网新闻确认: "
                    "https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821885.shtml; "
                    "https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821855.shtml; "
                    "https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821849.shtml"),
    },
    {
        "id": 2,
        "name": "郭小平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江汉区委副书记、区长",
        "current_org": "江汉区人民政府",
        "source": ("江汉区政府官网新闻确认: "
                    "https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821885.shtml; "
                    "https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821855.shtml"),
    },
    {
        "id": 3,
        "name": "姜辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区委组织部部长、区委统战部部长",
        "current_org": "中共武汉市江汉区委员会",
        "source": ("江汉区政府官网: "
                    "https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821885.shtml; "
                    "https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821833.shtml"),
    },
    {
        "id": 4,
        "name": "毕盛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共武汉市江汉区纪律检查委员会",
        "source": ("江汉区纪委监委官网: https://www.jianghan.gov.cn/qt/qjw/index.shtml; "
                    "https://www.jianghan.gov.cn/xwzx/jhyw/202606/t20260612_2776552.shtml"),
    },
    {
        "id": 5,
        "name": "曹建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "江汉区人民政府",
        "source": ("江汉区政府官网: "
                    "https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821833.shtml"),
    },
    {
        "id": 6,
        "name": "王瑞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导（职务待确认）",
        "current_org": "江汉区",
        "source": ("江汉区政府官网: "
                    "https://www.jianghan.gov.cn/tpxw/202605/t20260522_2767445.shtml"),
    },
    # ════════════════════════════════════════
    # 区人大 & 区政协
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "何裕生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "江汉区人大常委会",
        "source": ("江汉区政府官网: "
                    "https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821885.shtml; "
                    "https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821855.shtml"),
    },
    {
        "id": 8,
        "name": "叶劲松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协江汉区委员会",
        "source": ("江汉区政府官网: "
                    "https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821885.shtml; "
                    "https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821855.shtml"),
    },
    # ════════════════════════════════════════
    # 区纪委监委班子成员
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "王涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区纪委副书记、区监委副主任",
        "current_org": "中共武汉市江汉区纪律检查委员会",
        "source": ("江汉区纪委监委官网: https://www.jianghan.gov.cn/qt/qjw/index.shtml"),
    },
    {
        "id": 10,
        "name": "程臻",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区纪委常委",
        "current_org": "中共武汉市江汉区纪律检查委员会",
        "source": ("江汉区纪委监委官网: https://www.jianghan.gov.cn/qt/qjw/index.shtml"),
    },
    {
        "id": 11,
        "name": "贺春丽",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区纪委常委、区监委委员",
        "current_org": "中共武汉市江汉区纪律检查委员会",
        "source": ("江汉区纪委监委官网: https://www.jianghan.gov.cn/qt/qjw/index.shtml"),
    },
    {
        "id": 12,
        "name": "万鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区纪委常委",
        "current_org": "中共武汉市江汉区纪律检查委员会",
        "source": ("江汉区纪委监委官网: https://www.jianghan.gov.cn/qt/qjw/index.shtml"),
    },
    {
        "id": 13,
        "name": "周敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区监委委员",
        "current_org": "中共武汉市江汉区纪律检查委员会",
        "source": ("江汉区纪委监委官网: https://www.jianghan.gov.cn/qt/qjw/index.shtml"),
    },
    {
        "id": 14,
        "name": "彭少辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区监委委员",
        "current_org": "中共武汉市江汉区纪律检查委员会",
        "source": ("江汉区纪委监委官网: https://www.jianghan.gov.cn/qt/qjw/index.shtml"),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共武汉市江汉区委员会", "type": "党委", "level": "市辖区", "parent": "中共武汉市委员会", "location": "湖北省武汉市江汉区"},
    {"id": 2, "name": "江汉区人民政府", "type": "政府", "level": "市辖区", "parent": "武汉市人民政府", "location": "湖北省武汉市江汉区"},
    {"id": 3, "name": "中共武汉市江汉区纪律检查委员会", "type": "纪委", "level": "市辖区", "parent": "中共武汉市纪律检查委员会", "location": "湖北省武汉市江汉区"},
    {"id": 4, "name": "江汉区人大常委会", "type": "人大", "level": "市辖区", "parent": "武汉市人大常委会", "location": "湖北省武汉市江汉区"},
    {"id": 5, "name": "政协江汉区委员会", "type": "政协", "level": "市辖区", "parent": "政协武汉市委员会", "location": "湖北省武汉市江汉区"},
    {"id": 6, "name": "江汉区监察委员会", "type": "纪委", "level": "市辖区", "parent": "武汉市监察委员会", "location": "湖北省武汉市江汉区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 叶文静 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "江汉区委书记", "start": "", "end": "至今", "rank": "正处级", "note": "2026年7月6日主持区委理论学习中心组学习；7月1日'两优一先'表彰大会讲话；6月30日带队参观龙王庙"},
    # 郭小平 — 区长
    {"person_id": 2, "org_id": 2, "title": "江汉区区长", "start": "", "end": "至今", "rank": "正处级", "note": "区委副书记；2026年7月6日参加中心组学习；7月1日主持表彰大会"},
    {"person_id": 2, "org_id": 1, "title": "江汉区委副书记", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 姜辉 — 区委副书记/组织部长/统战部长
    {"person_id": 3, "org_id": 1, "title": "江汉区委副书记", "start": "", "end": "至今", "rank": "副处级", "note": "兼组织部部长、统战部部长"},
    # 毕盛 — 纪委书记
    {"person_id": 4, "org_id": 3, "title": "江汉区纪委书记", "start": "", "end": "至今", "rank": "副处级", "note": "兼区监委主任"},
    {"person_id": 4, "org_id": 1, "title": "江汉区委常委", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "江汉区监委主任", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 曹建 — 常委/副区长
    {"person_id": 5, "org_id": 1, "title": "江汉区委常委", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "江汉区副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 王瑞
    {"person_id": 6, "org_id": 1, "title": "江汉区区领导", "start": "", "end": "至今", "rank": "", "note": "职务待确认；2026年5月参加社区调研"},
    # 何裕生 — 人大主任
    {"person_id": 7, "org_id": 4, "title": "江汉区人大常委会主任", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 叶劲松 — 政协主席
    {"person_id": 8, "org_id": 5, "title": "江汉区政协主席", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 纪委监委班子
    {"person_id": 9, "org_id": 3, "title": "江汉区纪委副书记", "start": "", "end": "至今", "rank": "副处级", "note": "兼区监委副主任"},
    {"person_id": 10, "org_id": 3, "title": "江汉区纪委常委", "start": "", "end": "至今", "rank": "正科级", "note": ""},
    {"person_id": 11, "org_id": 3, "title": "江汉区纪委常委", "start": "", "end": "至今", "rank": "正科级", "note": "兼区监委委员"},
    {"person_id": 12, "org_id": 3, "title": "江汉区纪委常委", "start": "", "end": "至今", "rank": "正科级", "note": ""},
    {"person_id": 13, "org_id": 6, "title": "江汉区监委委员", "start": "", "end": "至今", "rank": "正科级", "note": ""},
    {"person_id": 14, "org_id": 6, "title": "江汉区监委委员", "start": "", "end": "至今", "rank": "正科级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长党政工作搭档关系", "overlap_org": "江汉区", "overlap_period": ""},
    # 副书记与书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与副书记工作搭档", "overlap_org": "中共江汉区委", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "区长与副书记工作搭档", "overlap_org": "江汉区", "overlap_period": ""},
    # 纪委书记与书记
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与纪委书记", "overlap_org": "中共江汉区委", "overlap_period": ""},
    # 常委副区长
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委书记与常委副区长", "overlap_org": "中共江汉区委", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "区长与副区长", "overlap_org": "江汉区政府", "overlap_period": ""},
    # 人大/政协
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "区委书记与人大主任", "overlap_org": "江汉区", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "区委书记与政协主席", "overlap_org": "江汉区", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "区长与人大主任", "overlap_org": "江汉区", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "区长与政协主席", "overlap_org": "江汉区", "overlap_period": ""},
    # 纪委监委班子
    {"person_a": 4, "person_b": 9, "type": "superior_subordinate", "context": "纪委书记与纪委副书记", "overlap_org": "江汉区纪委监委", "overlap_period": ""},
    {"person_a": 4, "person_b": 10, "type": "superior_subordinate", "context": "纪委书记与纪委常委", "overlap_org": "江汉区纪委监委", "overlap_period": ""},
    {"person_a": 4, "person_b": 11, "type": "superior_subordinate", "context": "纪委书记与纪委常委", "overlap_org": "江汉区纪委监委", "overlap_period": ""},
    {"person_a": 4, "person_b": 12, "type": "superior_subordinate", "context": "纪委书记与纪委常委", "overlap_org": "江汉区纪委监委", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    """Build source register from official sources."""
    return [
        {"id":"S001","title":"区委理论学习中心组集体（扩大）学习","url":"https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821885.shtml","publisher":"江汉区人民政府","published_at":"2026-07-06","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"叶文静主持，郭小平、何裕生、叶劲松、姜辉参加"},
        {"id":"S002","title":"江汉区'两优一先'表彰大会","url":"https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821855.shtml","publisher":"江汉区人民政府","published_at":"2026-07-02","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"叶文静讲话，郭小平主持，何裕生、叶劲松、姜辉出席"},
        {"id":"S003","title":"区领导集体参观龙王庙·抗洪精神主题公园","url":"https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821849.shtml","publisher":"江汉区人民政府","published_at":"2026-07-03","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"叶文静领誓，郭小平、何裕生、叶劲松全体区领导参加"},
        {"id":"S004","title":"海峡两岸金融服务外贸发展恳谈会","url":"https://www.jianghan.gov.cn/xwzx/jhyw/202607/t20260716_2821833.shtml","publisher":"江汉区人民政府","published_at":"2026-07-13","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"姜辉致辞，曹建主持"},
        {"id":"S005","title":"全区领导干部警示教育会","url":"https://www.jianghan.gov.cn/xwzx/jhyw/202606/t20260612_2776555.shtml","publisher":"江汉区人民政府","published_at":"2026-06-01","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"叶文静主持，毕盛通报典型案件"},
        {"id":"S006","title":"树立和践行正确政绩观学习教育工作推进会","url":"https://www.jianghan.gov.cn/xwzx/jhyw/202606/t20260612_2776552.shtml","publisher":"江汉区人民政府","published_at":"2026-06-12","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"叶文静讲话，郭小平出席，姜辉主持，毕盛通报"},
        {"id":"S007","title":"叶文静赴常青街道调研社区工作","url":"https://www.jianghan.gov.cn/tpxw/202605/t20260522_2767445.shtml","publisher":"江汉区人民政府","published_at":"2026-05-18","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"区委书记叶文静，毕盛、王瑞参加调研"},
        {"id":"S008","title":"江汉区纪委监委领导机构","url":"https://www.jianghan.gov.cn/qt/qjw/index.shtml","publisher":"江汉区纪委监委","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"毕盛为书记，王涛为副书记，程臻、贺春丽、万鹏为常委；周敏、彭少辉为监委委员"},
    ]

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def make_person_json(p, timeline, relationships_list, source_register):
    """Generate a person graph JSON object."""
    rank = "县处级正职" if ("书记" in p.get("current_post","") and "副" not in p.get("current_post","") and "纪委" not in p.get("current_post","")) or ("区长" in p.get("current_post","") and "副" not in p.get("current_post","") and "人大" not in p.get("current_post","") and "政协" not in p.get("current_post","")) or "主任" in p.get("current_post","") and ("人大" in p.get("current_post","") or "政协" in p.get("current_post","")) else "县处级副职"
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "武汉市",
            "region": "江汉区",
            "job": p.get("current_post",""),
            "task_id": "hubei_江汉区",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"jianghanqu_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender",""),
            "ethnicity": p.get("ethnicity",""),
            "birth": p.get("birth",""),
            "birthplace": p.get("birthplace",""),
            "native_place": p.get("native_place",""),
            "education": [{"period":"","institution":"","major":"","degree":p.get("education",""),"study_type":"unknown","source_ids":[]}] if p.get("education") else [],
            "party_join": p.get("party_join","").replace("中共党员（","").replace("中共党员","").replace("）",""),
            "work_start": p.get("work_start",""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source","")
            }
        },
        "current_status": {
            "current_post": p.get("current_post",""),
            "current_org": p.get("current_org",""),
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": []
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary":"","notable_fast_promotions":[]}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type":"none_found","description":"在公开信息中未发现该人物负面信号","date":"","confidence":"confirmed","source_ids":[]}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin" if not p.get("birth") else "partial",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息有待补充" if not p.get("birth") else f"{p['name']}早期职业生涯需确认"
        },
        "open_questions": [
            {"priority":"critical" if not p.get("birth") else "medium",
             "question": f"{p['name']}的完整职业生涯履历",
             "why_it_matters": "无法追溯其任职路径和系统经历",
             "suggested_queries": [f"{p['name']} 简历 江汉区",f"{p['name']} 任前公示"],
             "last_attempted": AS_OF}
        ]
    }
    return result

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print("  武汉市江汉区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 江汉区政府网站")
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
    print(f"\n✅ 江汉区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 叶文静 (区委书记)
    ye_timeline = [
        {"start":"","end":"","org":"中共武汉市江汉区委员会","title":"江汉区委书记","notes":"2026年7月确认；主持理论学习中心组、'两优一先'表彰大会","confidence":"confirmed","source_ids":["S001","S002","S003"]},
    ]
    ye_relationships = [
        {"person":"郭小平","person_id":"jianghanqu_郭小平","relationship_type":"overlap","strength":"strong","evidence":"区委书记与区长党政工作搭档","overlap_org":"江汉区","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S001","S002"]},
        {"person":"姜辉","person_id":"jianghanqu_姜辉","relationship_type":"overlap","strength":"strong","evidence":"区委书记与副书记工作搭档","overlap_org":"中共江汉区委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S001"]},
        {"person":"毕盛","person_id":"jianghanqu_毕盛","relationship_type":"overlap","strength":"strong","evidence":"区委书记与纪委书记","overlap_org":"中共江汉区委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S005","S006"]},
        {"person":"曹建","person_id":"jianghanqu_曹建","relationship_type":"overlap","strength":"medium","evidence":"区委书记与常委副区长","overlap_org":"中共江汉区委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S004"]},
        {"person":"何裕生","person_id":"jianghanqu_何裕生","relationship_type":"overlap","strength":"medium","evidence":"区委书记与人大主任","overlap_org":"江汉区","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S001","S002"]},
        {"person":"叶劲松","person_id":"jianghanqu_叶劲松","relationship_type":"overlap","strength":"medium","evidence":"区委书记与政协主席","overlap_org":"江汉区","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S001","S002"]},
    ]
    ye_json = make_person_json(persons[0], ye_timeline, ye_relationships, source_register)
    ye_path = PERSONS_DIR / f"{TODAY}-湖北省-武汉市-区委书记-叶文静.json"
    with open(ye_path, "w", encoding="utf-8") as f:
        json.dump(ye_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {ye_path.name}")

    # 2. 郭小平 (区长)
    guo_timeline = [
        {"start":"","end":"","org":"江汉区人民政府","title":"江汉区区长","notes":"2026年7月确认；区委副书记","confidence":"confirmed","source_ids":["S001","S002"]},
        {"start":"","end":"","org":"中共武汉市江汉区委员会","title":"江汉区委副书记","notes":"","confidence":"confirmed","source_ids":["S001"]},
    ]
    guo_relationships = [
        {"person":"叶文静","person_id":"jianghanqu_叶文静","relationship_type":"overlap","strength":"strong","evidence":"区长与区委书记党政工作搭档","overlap_org":"江汉区","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S001","S002"]},
        {"person":"姜辉","person_id":"jianghanqu_姜辉","relationship_type":"overlap","strength":"medium","evidence":"区长与副书记","overlap_org":"江汉区","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S001","S006"]},
        {"person":"曹建","person_id":"jianghanqu_曹建","relationship_type":"overlap","strength":"medium","evidence":"区长与副区长","overlap_org":"江汉区政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S004"]},
    ]
    guo_json = make_person_json(persons[1], guo_timeline, guo_relationships, source_register)
    guo_path = PERSONS_DIR / f"{TODAY}-湖北省-武汉市-区长-郭小平.json"
    with open(guo_path, "w", encoding="utf-8") as f:
        json.dump(guo_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {guo_path.name}")

    # 3. 姜辉 (区委副书记/组织部长/统战部长)
    jiang_timeline = [
        {"start":"","end":"","org":"中共武汉市江汉区委员会","title":"江汉区委副书记","notes":"兼组织部部长、统战部部长","confidence":"confirmed","source_ids":["S001","S004"]},
    ]
    jiang_relationships = [
        {"person":"叶文静","person_id":"jianghanqu_叶文静","relationship_type":"overlap","strength":"strong","evidence":"副书记与区委书记","overlap_org":"中共江汉区委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S001"]},
        {"person":"郭小平","person_id":"jianghanqu_郭小平","relationship_type":"overlap","strength":"medium","evidence":"副书记与区长","overlap_org":"江汉区","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S001","S006"]},
    ]
    jiang_json = make_person_json(persons[2], jiang_timeline, jiang_relationships, source_register)
    jiang_path = PERSONS_DIR / f"{TODAY}-湖北省-武汉市-区委副书记-姜辉.json"
    with open(jiang_path, "w", encoding="utf-8") as f:
        json.dump(jiang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {jiang_path.name}")


if __name__ == "__main__":
    build()
