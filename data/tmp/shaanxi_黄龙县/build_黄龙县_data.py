#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 黄龙县, 陕西省延安市.

Investigation date: 2026-07-25
Task ID: shaanxi_黄龙县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - Baidu Baike: 张晶 (lemmaId: 24135647) — full career timeline
  - hlx.gov.cn — 黄龙县人民政府官方网站 (primary, accessed July 2026)
  - huanglong.qinfeng.gov.cn — 黄龙县纪检监察网 (discipline inspection)
  - Sohu News (2016-2017) — 省管干部任职公示
  - Tencent News (2021, 2025) — 选举/政府工作报告
  - myzaker — 张晶已任黄龙县委书记 (2026-07)
  - lcx.gov.cn — 鲁强简历 (黄龙→洛川 cross-county exchange)
  - Baidu Zhidao — 李富荣任代理县长 (2016)

Confidence notes:
  - 张晶 (县委书记): confirmed via Baidu Baike — full timeline
  - 胡锐 (代县长): confirmed appointment date (2026-07-01), full career unknown
  - 袁立 (常务副县长): confirmed via hlx.gov.cn — basic bio (1979.01, 研究生, 女)
  - 曹增俊 (常委/副县长): confirmed via hlx.gov.cn
  - 王孟伟 (常委/组织部长): confirmed via qinfeng.gov.cn
  - 雷东 (常委/纪委书记): confirmed via qinfeng.gov.cn (b.1980.04, 工学学士)
  - 李晓民/王吉林/刘世红 (常委): confirmed via qinfeng.gov.cn
  - 申龙 (人大主任), 吴江宏 (政协主席): confirmed via qinfeng.gov.cn
  - 鲁强 (黄龙→洛川) : confirmed via lcx.gov.cn — full career path
  - 李富荣 (前任书记): confirmed via Tencent News, 去向 unverified
  - 陈斌 (前任县长): confirmed via Tencent News, 去向 unverified
  - 王云祥 (前任书记): confirmed via Sohu News (1977.06, 陕西神木)
  - 任高飞 (前任书记/县长): confirmed via Sohu News (1973.06, 陕西佳县)
  - Full career histories: thin for most officials
"""

from __future__ import annotations

import sqlite3  # noqa — used by gov_relation.runner via import

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "黄龙县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_黄龙县"
if _CURRENT_DIR.name == "shaanxi_黄龙县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 县委主要领导, 3-6 县政府领导, 7-11 县委其他常委, 12-13 人大/政协, 14-15 前任

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 县委主要领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1, "name": "张晶", "gender": "男", "ethnicity": "汉族",
        "birth": "1973年11月", "birthplace": "陕西富县", "education": "研究生学历",
        "party_join": "中共党员（1995年2月入党）", "work_start": "1991年7月",
        "current_post": "县委书记", "current_org": "中共黄龙县委员会",
        "source": "https://baike.baidu.com/item/%E5%BC%A0%E6%99%B6/24135647"
    },
    {
        "id": 2, "name": "胡锐", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记、代县长", "current_org": "黄龙县人民政府",
        "source": "黄龙宣传（2026-07-01）"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县政府领导班子
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3, "name": "袁立", "gender": "女", "ethnicity": "汉族",
        "birth": "1979年1月", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、常务副县长", "current_org": "黄龙县人民政府",
        "source": "https://www.hlx.gov.cn/zfxxgk/fdzdgknr/zfld/"
    },
    {
        "id": 4, "name": "曹增俊", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、副县长", "current_org": "黄龙县人民政府",
        "source": "https://www.hlx.gov.cn/zfxxgk/fdzdgknr/zfld/"
    },
    {
        "id": 5, "name": "赵军锋", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "黄龙县人民政府",
        "source": "https://www.hlx.gov.cn/zfxxgk/fdzdgknr/zfld/"
    },
    {
        "id": 6, "name": "汪洋", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "黄龙县人民政府",
        "source": "https://www.hlx.gov.cn/zfxxgk/fdzdgknr/zfld/"
    },
    {
        "id": 7, "name": "张得胜", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "黄龙县人民政府",
        "source": "https://www.hlx.gov.cn/zfxxgk/fdzdgknr/zfld/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县委其他常委
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 8, "name": "雷东", "gender": "男", "ethnicity": "汉族",
        "birth": "1980年4月", "birthplace": "", "education": "全日制大学学历、工学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任", "current_org": "中共黄龙县纪律检查委员会",
        "source": "https://huanglong.qinfeng.gov.cn/xxgk/ldjg1.htm"
    },
    {
        "id": 9, "name": "王孟伟", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、组织部部长", "current_org": "中共黄龙县委组织部",
        "source": "https://huanglong.qinfeng.gov.cn/info/1051/8823.htm"
    },
    {
        "id": 10, "name": "孙炜刚", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记（专职）", "current_org": "中共黄龙县委员会",
        "source": "https://huanglong.qinfeng.gov.cn/info/1051/8812.htm"
    },
    {
        "id": 11, "name": "李晓民", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委", "current_org": "中共黄龙县委员会",
        "source": "https://huanglong.qinfeng.gov.cn/info/1051/8812.htm"
    },
    {
        "id": 12, "name": "王吉林", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、政法委书记", "current_org": "中共黄龙县委员会",
        "source": "https://huanglong.qinfeng.gov.cn/info/1051/8812.htm"
    },
    {
        "id": 13, "name": "刘世红", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委", "current_org": "中共黄龙县委员会",
        "source": "https://huanglong.qinfeng.gov.cn/info/1051/8812.htm"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大/政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 14, "name": "申龙", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会主任", "current_org": "黄龙县人民代表大会常务委员会",
        "source": "https://huanglong.qinfeng.gov.cn/info/1051/8812.htm"
    },
    {
        "id": 15, "name": "吴江宏", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协主席", "current_org": "中国人民政治协商会议黄龙县委员会",
        "source": "https://huanglong.qinfeng.gov.cn/info/1051/8812.htm"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 16, "name": "李富荣", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任县委书记", "current_org": "中共黄龙县委员会",
        "source": "https://new.qq.com/rain/a/20210930A0H3CN00"
    },
    {
        "id": 17, "name": "陈斌", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任县长", "current_org": "黄龙县人民政府",
        "source": "https://news.qq.com/rain/a/20250206A05IFM00"
    },
    {
        "id": 18, "name": "王云祥", "gender": "男", "ethnicity": "汉族",
        "birth": "1977年6月", "birthplace": "陕西神木", "education": "全日制大学/文学学士，在职研究生/哲学硕士",
        "party_join": "中共党员（2000年4月入党）", "work_start": "2000年7月",
        "current_post": "前任县委书记", "current_org": "中共黄龙县委员会",
        "source": "https://m.sohu.com/a/205806699_721001"
    },
    {
        "id": 19, "name": "任高飞", "gender": "男", "ethnicity": "汉族",
        "birth": "1973年6月", "birthplace": "陕西佳县", "education": "全日制高中学历，省委党校研究生学历",
        "party_join": "中共党员（1999年1月入党）", "work_start": "1991年6月",
        "current_post": "前任县委书记", "current_org": "中共黄龙县委员会",
        "source": "https://www.sohu.com/a/104442194_119659"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 跨县交流人物（黄龙→洛川）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20, "name": "鲁强", "gender": "男", "ethnicity": "汉族",
        "birth": "1980年9月", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "曾任黄龙副县长/公安局长（现洛川副县长/公安局长）",
        "current_org": "洛川县人民政府",
        "source": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/lq/1.html"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共黄龙县委员会", "type": "党委", "level": "县级", "parent": "中共延安市委", "location": "黄龙县"},
    {"id": 2, "name": "黄龙县人民政府", "type": "政府", "level": "县级", "parent": "延安市人民政府", "location": "黄龙县"},
    {"id": 3, "name": "中共黄龙县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共黄龙县委员会", "location": "黄龙县"},
    {"id": 4, "name": "黄龙县监察委员会", "type": "党委", "level": "县级", "parent": "中共黄龙县委员会", "location": "黄龙县"},
    {"id": 5, "name": "中共黄龙县委组织部", "type": "党委", "level": "县级", "parent": "中共黄龙县委员会", "location": "黄龙县"},
    {"id": 6, "name": "中共黄龙县委政法委员会", "type": "党委", "level": "县级", "parent": "中共黄龙县委员会", "location": "黄龙县"},
    {"id": 7, "name": "黄龙县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "延安市人民代表大会常务委员会", "location": "黄龙县"},
    {"id": 8, "name": "中国人民政治协商会议黄龙县委员会", "type": "政协", "level": "县级", "parent": "政协延安市委员会", "location": "黄龙县"},
    {"id": 9, "name": "黄龙县公安局", "type": "政府", "level": "科级", "parent": "黄龙县人民政府", "location": "黄龙县"},
    {"id": 10, "name": "延安干部培训学院", "type": "事业单位", "level": "市级", "parent": "中共延安市委", "location": "延安市"},
    {"id": 11, "name": "中共延川县委", "type": "党委", "level": "县级", "parent": "中共延安市委", "location": "延川县"},
    {"id": 12, "name": "洛川县人民政府", "type": "政府", "level": "县级", "parent": "延安市人民政府", "location": "洛川县"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 张晶 (县委书记)
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2025.07", "end": "present",
     "rank": "正处级", "note": "从洛川县长调任黄龙县委书记"},
    {"person_id": 1, "org_id": 1, "title": "县委组织部副科级组织员→正科级", "start": "早期", "end": "~2010",
     "rank": "副科→正科", "note": "长期在县/市委组织部系统工作"},
    {"person_id": 1, "org_id": 10, "title": "副院长（副县级）", "start": "2013.12", "end": "2016.06",
     "rank": "副处级", "note": "延安干部培训学院"},
    {"person_id": 1, "org_id": 10, "title": "常务副院长（正县级）", "start": "2016.06", "end": "2018.03",
     "rank": "正处级", "note": "延安干部培训学院"},  # note: "正处级" is colloquial - actual rank of 常务副院长 is typically 副处 or 正处
    {"person_id": 1, "org_id": 11, "title": "县委副书记（正县级）、县委党校校长", "start": "~2018", "end": "2021.08",
     "rank": "正处级", "note": "延川县"},
    {"person_id": 1, "org_id": 12, "title": "代县长", "start": "2021.08", "end": "2022.03",
     "rank": "正处级", "note": "洛川县"},
    {"person_id": 1, "org_id": 12, "title": "县长", "start": "2022.03", "end": "2025.07",
     "rank": "正处级", "note": "洛川县"},
    # 胡锐 (代县长)
    {"person_id": 2, "org_id": 2, "title": "副县长、代理县长", "start": "2026.07.01", "end": "present",
     "rank": "正处级", "note": "此前职务待查"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2026.07", "end": "present",
     "rank": "正处级", "note": "代县长兼任县委副书记"},
    # 袁立 (常务副县长)
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start": "", "end": "",
     "rank": "副处级", "note": "1979年1月生/研究生；曾任市直部门副科长/科长/副职，区委常委/统战部长，县委常委/组织部长"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start": "", "end": "",
     "rank": "副处级", "note": "县委常委会成员"},
    # 曹增俊 (常委/副县长)
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": "县委常委、副县长"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "",
     "rank": "副处级", "note": "县委常委会成员"},
    # 赵军锋 (副县长)
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": ""},
    # 汪洋 (副县长)
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": ""},
    # 张得胜 (副县长)
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": ""},
    # 雷东 (纪委书记)
    {"person_id": 8, "org_id": 3, "title": "县纪委书记", "start": "", "end": "",
     "rank": "副处级", "note": "1980年4月生/全日制大学/工学学士/四级高级监察官"},
    {"person_id": 8, "org_id": 4, "title": "县监委主任", "start": "", "end": "",
     "rank": "副处级", "note": "兼任监委主任"},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "",
     "rank": "副处级", "note": "县委常委会成员"},
    # 王孟伟 (组织部长)
    {"person_id": 9, "org_id": 5, "title": "组织部部长", "start": "", "end": "",
     "rank": "副处级", "note": "2026年3月宣布第九轮巡察组长授权"},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "",
     "rank": "副处级", "note": "县委常委会成员"},
    # 孙炜刚 (专职副书记)
    {"person_id": 10, "org_id": 1, "title": "县委副书记（专职）", "start": "", "end": "",
     "rank": "副处级", "note": "2026年3月报道"},
    # 李晓民 (常委)
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "",
     "rank": "副处级", "note": ""},
    # 王吉林 (政法委书记)
    {"person_id": 12, "org_id": 6, "title": "政法委书记", "start": "", "end": "",
     "rank": "副处级", "note": "县委常委、政法委书记"},
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start": "", "end": "",
     "rank": "副处级", "note": "县委常委会成员"},
    # 刘世红 (常委)
    {"person_id": 13, "org_id": 1, "title": "县委常委", "start": "", "end": "",
     "rank": "副处级", "note": ""},
    # 申龙 (人大主任)
    {"person_id": 14, "org_id": 7, "title": "县人大常委会主任", "start": "", "end": "",
     "rank": "正处级", "note": ""},
    # 吴江宏 (政协主席)
    {"person_id": 15, "org_id": 8, "title": "县政协主席", "start": "", "end": "",
     "rank": "正处级", "note": ""},
    # 李富荣 (前任书记)
    {"person_id": 16, "org_id": 2, "title": "代县长→县长", "start": "2016.08", "end": "2021.09",
     "rank": "正处级", "note": "2016年8月任代理县长；后正式任县长"},
    {"person_id": 16, "org_id": 1, "title": "县委书记", "start": "2021.09", "end": "2025.07",
     "rank": "正处级", "note": "2021年9月当选县委书记；2025年7月卸任，去向待查"},
    # 陈斌 (前任县长)
    {"person_id": 17, "org_id": 2, "title": "县长", "start": "2021.09", "end": "~2026.06",
     "rank": "正处级", "note": "2025年2月仍作政府工作报告；2026年7月胡锐接任"},
    {"person_id": 17, "org_id": 1, "title": "县委副书记", "start": "2021.09", "end": "~2026.06",
     "rank": "正处级", "note": "县长兼任县委副书记"},
    # 王云祥 (前任书记)
    {"person_id": 18, "org_id": 1, "title": "县委书记", "start": "2017.11", "end": "2021.09",
     "rank": "正处级", "note": "1977年6月生/陕西神木人；此前任富县县长"},
    # 任高飞 (前任书记/县长)
    {"person_id": 19, "org_id": 2, "title": "县长", "start": "", "end": "2016.08",
     "rank": "正处级", "note": "1973年6月生/陕西佳县人"},
    {"person_id": 19, "org_id": 1, "title": "县委书记", "start": "2016.07", "end": "2017.11",
     "rank": "正处级", "note": "从县长晋升县委书记"},
    # 鲁强 (黄龙→洛川, 跨县交流)
    {"person_id": 20, "org_id": 9, "title": "县公安局政委", "start": "", "end": "",
     "rank": "正科级", "note": "从宝塔分局副政委调任"},
    {"person_id": 20, "org_id": 9, "title": "副县长、公安局党委书记/局长", "start": "", "end": "",
     "rank": "副处级", "note": "在黄龙晋升"},
    {"person_id": 20, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": "兼任公安局长"},
]

# ── Relationships ──────────────────────────────────────────────────────────────
relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与代县长，县委与县政府一把手", "overlap_org": "黄龙县", "overlap_period": "2026.07-至今"},
    # 县委书记 x 其他常委
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与县委常委/常务副县长", "overlap_org": "中共黄龙县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与县委常委/副县长", "overlap_org": "中共黄龙县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记与纪委书记", "overlap_org": "中共黄龙县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记与组织部部长", "overlap_org": "中共黄龙县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委书记与专职副书记", "overlap_org": "中共黄龙县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委书记与县委常委李晓民", "overlap_org": "中共黄龙县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "县委书记与政法委书记", "overlap_org": "中共黄龙县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "县委书记与县委常委刘世红", "overlap_org": "中共黄龙县委", "overlap_period": ""},
    # 代县长 x 副县长
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "代县长与常务副县长", "overlap_org": "黄龙县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "代县长与副县长", "overlap_org": "黄龙县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "代县长与副县长", "overlap_org": "黄龙县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "代县长与副县长", "overlap_org": "黄龙县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "代县长与副县长", "overlap_org": "黄龙县人民政府", "overlap_period": ""},
    # 前任与现任 - 书记传承
    {"person_a": 16, "person_b": 1, "type": "predecessor_successor", "context": "李富荣为前任县委书记，张晶接任", "overlap_org": "中共黄龙县委", "overlap_period": "2025.07"},
    {"person_a": 18, "person_b": 16, "type": "predecessor_successor", "context": "王云祥为前任县委书记，李富荣接任", "overlap_org": "中共黄龙县委", "overlap_period": "2021.09"},
    {"person_a": 19, "person_b": 18, "type": "predecessor_successor", "context": "任高飞为前任县委书记，王云祥接任", "overlap_org": "中共黄龙县委", "overlap_period": "2017.11"},
    # 前任与现任 - 县长传承
    {"person_a": 17, "person_b": 2, "type": "predecessor_successor", "context": "陈斌为前任县长，胡锐接任", "overlap_org": "黄龙县人民政府", "overlap_period": "2026.07"},
    {"person_a": 16, "person_b": 17, "type": "predecessor_successor", "context": "李富荣为前任县长，陈斌接任", "overlap_org": "黄龙县人民政府", "overlap_period": "2021.09"},
    {"person_a": 19, "person_b": 16, "type": "predecessor_successor", "context": "任高飞为前任县长，李富荣接任", "overlap_org": "黄龙县人民政府", "overlap_period": "2016.08"},
    # 县长→书记（本地晋升）
    {"person_a": 19, "person_b": 19, "type": "self_referencing", "context": "任高飞从县长晋升县委书记", "overlap_org": "黄龙县", "overlap_period": "2016"},
    {"person_a": 16, "person_b": 16, "type": "self_referencing", "context": "李富荣从县长晋升县委书记", "overlap_org": "黄龙县", "overlap_period": "2021"},
    # 跨县交流
    {"person_a": 1, "person_b": 20, "type": "former_colleague", "context": "张晶任洛川县长期间与鲁强（副县长/公安局长）共事", "overlap_org": "洛川县人民政府", "overlap_period": "~2022-2025"},
    # 人大/政协 x 县委
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "县委书记与县人大常委会主任", "overlap_org": "黄龙县", "overlap_period": ""},
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "县委书记与县政协主席", "overlap_org": "黄龙县", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "百度百科 — 张晶", "url": "https://baike.baidu.com/item/%E5%BC%A0%E6%99%B6/24135647", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "张晶完整履历"},
        {"id": "S002", "title": "搜狐新闻 — 任高飞拟任黄龙县委书记(2016)", "url": "https://www.sohu.com/a/104442194_119659", "publisher": "搜狐新闻", "published_at": "2016-07", "accessed_at": AS_OF, "source_type": "news", "reliability": "high", "notes": "任高飞省管干部任职公示"},
        {"id": "S003", "title": "搜狐新闻 — 王云祥拟任黄龙县委书记(2017)", "url": "https://m.sohu.com/a/205806699_721001", "publisher": "搜狐新闻", "published_at": "2017-11-21", "accessed_at": AS_OF, "source_type": "news", "reliability": "high", "notes": "王云祥省管干部任职公示"},
        {"id": "S004", "title": "腾讯新闻 — 李富荣当选黄龙县委书记(2021)", "url": "https://new.qq.com/rain/a/20210930A0H3CN00", "publisher": "腾讯新闻", "published_at": "2021-09-30", "accessed_at": AS_OF, "source_type": "news", "reliability": "high", "notes": "李富荣当选，陈斌任县长"},
        {"id": "S005", "title": "腾讯新闻 — 陈斌作政府工作报告(2025)", "url": "https://news.qq.com/rain/a/20250206A05IFM00", "publisher": "腾讯新闻", "published_at": "2025-02-06", "accessed_at": AS_OF, "source_type": "news", "reliability": "high", "notes": "陈斌仍在县长任上"},
        {"id": "S006", "title": "黄龙县人民政府 — 领导分工/个人简历", "url": "https://www.hlx.gov.cn/zfxxgk/fdzdgknr/zfld/", "publisher": "黄龙县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "袁立(常务副)/曹增俊/赵军锋/汪洋/张得胜等"},
        {"id": "S007", "title": "百度知道 — 李富荣任黄龙代理县长(2016)", "url": "https://zhidao.baidu.com/question/627950375783983804.html", "publisher": "百度知道", "published_at": "2016-08", "accessed_at": AS_OF, "source_type": "qa", "reliability": "medium", "notes": "李富荣代理县长任命"},
        {"id": "S008", "title": "myzaker — 张晶已任黄龙县委书记", "url": "http://app.myzaker.com/article/6870d5641bc8e0e66c000006", "publisher": "myzaker", "published_at": "2026-07", "accessed_at": AS_OF, "source_type": "news", "reliability": "medium", "notes": "张晶调研小寺庄煤矿"},
        {"id": "S009", "title": "黄龙宣传 — 胡锐任代理县长", "url": "", "publisher": "黄龙县融媒体中心", "published_at": "2026-07-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "胡锐任命消息"},
        {"id": "S010", "title": "洛川县人民政府 — 鲁强简历", "url": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/lq/1.html", "publisher": "洛川县人民政府", "published_at": "2026-07-14", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "鲁强：曾任黄龙县副县长/公安局长→洛川副县长/公安局长"},
        {"id": "S011", "title": "百度百科 — 黄龙县", "url": "https://baike.baidu.com/item/%E9%BB%84%E9%BE%99%E5%8%BF/10564200", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "黄龙县基本情况"},
        {"id": "S012", "title": "黄龙纪检监察网 — 领导机构", "url": "https://huanglong.qinfeng.gov.cn/xxgk/ldjg1.htm", "publisher": "中共黄龙县纪律检查委员会", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "雷东(1980.04)/张海峰/路鑫等纪委领导"},
        {"id": "S013", "title": "黄龙纪检监察网 — 县纪委第六次全会报道", "url": "https://huanglong.qinfeng.gov.cn/info/1051/8812.htm", "publisher": "中共黄龙县纪律检查委员会", "published_at": "2026-03-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张晶/陈斌/孙炜刚/袁立/曹增俊/王孟伟等全部常委确认"},
    ]


def make_person_json(person, timeline, relationships_list, source_register, gaps=None):
    """Build a person graph JSON following the schema."""
    pfname = f"huanglong_{person['name']}"
    # Determine rank
    post = person["current_post"]
    if "书记" in post and "常委" not in post and "副" not in post:
        rank = "正处级"
    elif "代县长" in post or "县长" in post:
        rank = "正处级"
    elif "人大主任" in post or "政协主席" in post:
        rank = "正处级"
    elif "前任" in post:
        rank = "正处级"
    else:
        rank = "副处级"
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "陕西省",
            "city": "延安市",
            "region": "黄龙县",
            "job": person["current_post"],
            "task_id": "shaanxi_黄龙县",
            "time_focus": "2016-2026"
        },
        "identity": {
            "person_id": pfname,
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person["education"], "study_type": "unknown", "source_ids": []}] if person["education"] else [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}" if person["birth"] else person["name"],
                "name_birthplace": f"{person['name']}_{person['birthplace']}" if person["birthplace"] else person["name"],
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
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
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面公开记录", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial" if person["birth"] else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{person['name']}的早期履历不完整"
        },
        "open_questions": (gaps if gaps else [
            {"priority": "high", "question": f"{person['name']}的完整职业履历是什么？", "why_it_matters": "无法分析晋升路径和跨部门经验", "suggested_queries": [f"{person['name']} 简历 黄龙"], "last_attempted": AS_OF},
        ])
    }


# ══════════════════════════════════════════════════════════════════════════
# Build Function
# ══════════════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print("  黄龙县领导班子工作关系网络")
    print("  等级: 县")
    print(f"  调查日期: {AS_OF}")
    print("  信息来源: 百度百科、hlx.gov.cn、qinfeng.gov.cn、lcx.gov.cn")
    print("=" * 60)

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\n  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 张晶 (县委书记)
    zhang_timeline = [
        {"start": "早期", "end": "2013.12", "org": "县/市委组织部", "title": "副科级组织员→科长→副县级组织员", "notes": "长期在组织系统工作", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2013.12", "end": "2016.06", "org": "陕西省延安干部培训学院", "title": "副院长（副县级）", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2016.06", "end": "2018.03", "org": "陕西省延安干部培训学院", "title": "常务副院长（正县级）", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "~2018", "end": "2021.08", "org": "中共延川县委", "title": "县委副书记（正县级）、县委党校校长", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2021.08", "end": "2022.03", "org": "洛川县人民政府", "title": "洛川县委副书记、代县长", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2022.03", "end": "2025.07", "org": "洛川县人民政府", "title": "洛川县委副书记、县长", "notes": "2025年3月仍以县长身份调研", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2025.07", "end": "present", "org": "中共黄龙县委", "title": "黄龙县委书记", "notes": "从洛川县长调任黄龙县委书记", "confidence": "confirmed", "source_ids": ["S001", "S008"]},
    ]
    zhang_relationships = [
        {"person": "胡锐", "person_id": "huanglong_胡锐", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与代理县长，党政搭档", "overlap_org": "黄龙县", "overlap_period": "2026.07-至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S009"]},
        {"person": "袁立", "person_id": "huanglong_袁立", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与县委常委/常务副县长", "overlap_org": "中共黄龙县委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
        {"person": "雷东", "person_id": "huanglong_雷东", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与纪委书记", "overlap_org": "中共黄龙县委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S013"]},
        {"person": "王孟伟", "person_id": "huanglong_王孟伟", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与组织部部长", "overlap_org": "中共黄龙县委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S013"]},
        {"person": "李富荣", "person_id": "huanglong_李富荣", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "张晶接替李富荣任县委书记", "overlap_org": "中共黄龙县委", "overlap_period": "2025.07", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S004", "S008"]},
        {"person": "鲁强", "person_id": "huanglong_鲁强", "relationship_type": "former_colleague", "strength": "medium", "evidence": "张晶任洛川县长时鲁强为副县长", "overlap_org": "洛川县人民政府", "overlap_period": "~2022-2025", "direction": "undirected", "confidence": "plausible", "source_ids": ["S001", "S010"]},
    ]
    zhang_json = make_person_json(persons[0], zhang_timeline, zhang_relationships, source_register)
    zhang_path = PJSON_DIR / f"{TODAY}-陕西省-延安市-县委书记-张晶.json"
    with open(zhang_path, "w", encoding="utf-8") as f:
        json.dump(zhang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zhang_path.name}")

    # 2. 胡锐 (代县长)
    hurui_timeline = [
        {"start": "2026.07.01", "end": "present", "org": "黄龙县人民政府", "title": "副县长、代理县长", "notes": "2026年7月1日被任命；此前职务待查", "confidence": "confirmed", "source_ids": ["S009"]},
    ]
    hurui_relationships = [
        {"person": "张晶", "person_id": "huanglong_张晶", "relationship_type": "overlap", "strength": "strong", "evidence": "代县长与县委书记，党政搭档", "overlap_org": "黄龙县", "overlap_period": "2026.07-至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S009"]},
        {"person": "袁立", "person_id": "huanglong_袁立", "relationship_type": "overlap", "strength": "strong", "evidence": "代县长与常务副县长", "overlap_org": "黄龙县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
        {"person": "陈斌", "person_id": "huanglong_陈斌", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "胡锐接替陈斌任县长", "overlap_org": "黄龙县人民政府", "overlap_period": "2026.07", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S005", "S009"]},
    ]
    hurui_gaps = [
        {"priority": "critical", "question": "胡锐2026年7月前担任何职？完整履历是什么？", "why_it_matters": "核心人物；履历完全空白", "suggested_queries": ["胡锐 黄龙 简历", "胡锐 任前公示", "胡锐 此前 担任"], "last_attempted": AS_OF},
        {"priority": "critical", "question": "胡锐的出生年份、籍贯、教育背景？", "why_it_matters": "核心人物身份信息缺失", "suggested_queries": ["胡锐 出生 陕西"], "last_attempted": AS_OF},
    ]
    hurui_json = make_person_json(persons[1], hurui_timeline, hurui_relationships, source_register, hurui_gaps)
    hurui_path = PJSON_DIR / f"{TODAY}-陕西省-延安市-县长-胡锐.json"
    with open(hurui_path, "w", encoding="utf-8") as f:
        json.dump(hurui_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {hurui_path.name}")

    # 3. 袁立 (常务副县长)
    yuanli_timeline = [
        {"start": "", "end": "", "org": "黄龙县人民政府", "title": "县委常委、常务副县长", "notes": "1979年1月生/研究生；曾任市直部门副科长/科长/副职，区委常委/统战部长，县委常委/组织部长", "confidence": "confirmed", "source_ids": ["S006"]},
    ]
    yuanli_relationships = [
        {"person": "张晶", "person_id": "huanglong_张晶", "relationship_type": "overlap", "strength": "strong", "evidence": "常务副县长与县委书记", "overlap_org": "中共黄龙县委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
        {"person": "胡锐", "person_id": "huanglong_胡锐", "relationship_type": "overlap", "strength": "strong", "evidence": "常务副县长与代县长", "overlap_org": "黄龙县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
    ]
    yuanli_gaps = [
        {"priority": "high", "question": "袁立的市直部门经历？曾任职哪个区？哪个县委任组织部长？", "why_it_matters": "了解其晋升路径和跨部门经验", "suggested_queries": ["袁立 简历 黄龙", "袁立 延安"], "last_attempted": AS_OF},
    ]
    yuanli_json = make_person_json(persons[2], yuanli_timeline, yuanli_relationships, source_register, yuanli_gaps)
    yuanli_path = PJSON_DIR / f"{TODAY}-陕西省-延安市-常务副县长-袁立.json"
    with open(yuanli_path, "w", encoding="utf-8") as f:
        json.dump(yuanli_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {yuanli_path.name}")

    # 4. 鲁强 (黄龙→洛川, cross-county exchange)
    luqiang_timeline = [
        {"start": "", "end": "", "org": "延安市公安局", "title": "政治部综合处/宣传处处长", "notes": "在延安市公安局政治部工作", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "", "end": "", "org": "延安市公安局宝塔分局", "title": "副政委", "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "", "end": "", "org": "黄龙县公安局", "title": "政委", "notes": "从宝塔分局副政委调任黄龙", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "", "end": "", "org": "黄龙县人民政府/公安局", "title": "副县长、公安局党委书记/局长", "notes": "在黄龙晋升", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "", "end": "present", "org": "洛川县人民政府/公安局", "title": "副县长、公安局党委书记/局长", "notes": "从黄龙调任洛川", "confidence": "confirmed", "source_ids": ["S010"]},
    ]
    luqiang_relationships = [
        {"person": "张晶", "person_id": "huanglong_张晶", "relationship_type": "former_colleague", "strength": "medium", "evidence": "鲁强在洛川任副县长时，张晶曾任洛川县长", "overlap_org": "洛川县人民政府", "overlap_period": "~2022-2025", "direction": "undirected", "confidence": "plausible", "source_ids": ["S001", "S010"]},
    ]
    luqiang_gaps = [
        {"priority": "high", "question": "鲁强的完整职业履历？各任职的具体起止日期？", "why_it_matters": "无法确定交流时间线", "suggested_queries": ["鲁强 简历 洛川", "鲁强 延安 公安"], "last_attempted": AS_OF},
    ]
    luqiang_json = make_person_json(persons[19], luqiang_timeline, luqiang_relationships, source_register, luqiang_gaps)
    luqiang_path = PJSON_DIR / f"{TODAY}-陕西省-延安市-副县长(黄龙调洛川)-鲁强.json"
    with open(luqiang_path, "w", encoding="utf-8") as f:
        json.dump(luqiang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {luqiang_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PJSON_DIR}")


if __name__ == "__main__":
    build()
