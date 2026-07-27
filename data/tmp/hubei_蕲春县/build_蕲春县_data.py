#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 蕲春县 (Qichun County) leadership network.

蕲春县,隶属于湖北省黄冈市.
"""

import os
import sqlite3  # noqa: F401  # used by runner internally
import sys
from pathlib import Path

# Add repo root to path
_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "蕲春县"
DB_PATH = DATABASE_DIR / "蕲春县_network.db"
GEXF_PATH = GRAPH_DIR / "蕲春县_network.gexf"

# ── PERSONS ───────────────────────────────────────────────────────────
# Sources: qichun.gov.cn official news articles (accessed 2026-07-24)

persons = [
    # ── 1. Current Party Secretary ──
    {
        "id": 1,
        "name": "陈丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共蕲春县委书记",
        "current_org": "中共蕲春县委员会",
        "source": "https://www.qichun.gov.cn/zwxw/qcyw/12109478.html",
    },
    # ── 2. Current Executive Deputy County Mayor (acting head of government) ──
    {
        "id": 2,
        "name": "何朝阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县委常委、常务副县长",
        "current_org": "蕲春县人民政府",
        "source": "https://www.qichun.gov.cn/zwgk/public/6636852/1736952.html",
    },
    # ── 3. Former Party Secretary ──
    {
        "id": 3,
        "name": "胡安元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（原中共蕲春县委书记，已离任）",
        "current_org": "",
        "source": "https://www.qichun.gov.cn/zwgk/public/6636852/1725643.html",
    },
    # ── 4. Deputy Party Secretary ──
    {
        "id": 4,
        "name": "毛红志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县委副书记",
        "current_org": "中共蕲春县委员会",
        "source": "https://www.qichun.gov.cn/zwgk/public/6636852/1711218.html",
    },
    # ── 5. Standing Committee / County Leaders ──
    {
        "id": 5,
        "name": "张明波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县领导",
        "current_org": "中共蕲春县委员会",
        "source": "https://www.qichun.gov.cn/zwxw/qcyw/12109682.html",
    },
    {
        "id": 6,
        "name": "李链稳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县领导",
        "current_org": "中共蕲春县委员会",
        "source": "https://www.qichun.gov.cn/zwxw/qcyw/12109682.html",
    },
    {
        "id": 7,
        "name": "朱朝辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县领导",
        "current_org": "中共蕲春县委员会",
        "source": "https://www.qichun.gov.cn/zwxw/qcyw/12109682.html",
    },
    {
        "id": 8,
        "name": "王超辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县副县长",
        "current_org": "蕲春县人民政府",
        "source": "https://www.qichun.gov.cn/zwgk/public/6636852/1725643.html",
    },
    {
        "id": 9,
        "name": "张攀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县副县长",
        "current_org": "蕲春县人民政府",
        "source": "https://www.qichun.gov.cn/zwgk/public/6636852/1725643.html",
    },
    {
        "id": 10,
        "name": "张立新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县副县长",
        "current_org": "蕲春县人民政府",
        "source": "https://www.qichun.gov.cn/zwgk/public/6636852/1725643.html",
    },
    {
        "id": 11,
        "name": "方敏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县副县长、县红十字会会长",
        "current_org": "蕲春县人民政府",
        "source": "https://www.qichun.gov.cn/zwxw/qcyw/12110402.html",
    },
    {
        "id": 12,
        "name": "王开伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县领导",
        "current_org": "中共蕲春县委员会",
        "source": "https://www.qichun.gov.cn/zwxw/qcyw/12110558.html",
    },
    {
        "id": 13,
        "name": "童文军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县领导",
        "current_org": "中共蕲春县委员会",
        "source": "https://www.qichun.gov.cn/zwxw/qcyw/12110558.html",
    },
    {
        "id": 14,
        "name": "杨振武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县领导",
        "current_org": "中共蕲春县委员会",
        "source": "https://www.qichun.gov.cn/zwgk/public/6636852/1711218.html",
    },
    {
        "id": 15,
        "name": "陈泽明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县领导",
        "current_org": "中共蕲春县委员会",
        "source": "https://www.qichun.gov.cn/zwgk/public/6636852/1711218.html",
    },
    {
        "id": 16,
        "name": "杨海燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县领导",
        "current_org": "中共蕲春县委员会",
        "source": "https://www.qichun.gov.cn/zwgk/public/6636852/1728864.html",
    },
    {
        "id": 17,
        "name": "范成意",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县领导",
        "current_org": "中共蕲春县委员会",
        "source": "https://www.qichun.gov.cn/zwgk/public/6636852/1728864.html",
    },
    {
        "id": 18,
        "name": "欧阳畅贤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蕲春县政府领导",
        "current_org": "蕲春县人民政府",
        "source": "https://www.qichun.gov.cn/zwgk/public/6636852/1713667.html",
    },
]

# ── ORGANIZATIONS ─────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共蕲春县委员会",
        "type": "党委",
        "level": "县处级",
        "location": "湖北省黄冈市蕲春县",
    },
    {
        "id": 2,
        "name": "蕲春县人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "湖北省黄冈市蕲春县",
    },
    {
        "id": 3,
        "name": "蕲春县人大常委会",
        "type": "人大",
        "level": "县处级",
        "location": "湖北省黄冈市蕲春县",
    },
    {
        "id": 4,
        "name": "蕲春县政协",
        "type": "政协",
        "level": "县处级",
        "location": "湖北省黄冈市蕲春县",
    },
    {
        "id": 5,
        "name": "中共蕲春县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "location": "湖北省黄冈市蕲春县",
    },
]

# ── POSITIONS ─────────────────────────────────────────────────────────

positions = [
    # 陈丹 career
    {
        "person_id": 1,
        "org_id": 2,
        "title": "蕲春县委副书记、县长",
        "start": "未知",
        "end": "2026-07",
        "rank": "县处级正职",
        "note": "2026年5月13日以县委副书记、县长身份出席秸秆禁烧会议。2026年6月2日以县长身份委托常务副县长主持会议。",
    },
    {
        "person_id": 1,
        "org_id": 1,
        "title": "蕲春县委书记",
        "start": "2026-07",
        "end": "至今",
        "rank": "县处级正职",
        "note": "2026年7月15日首次以县委书记身份主持县委常委会。2026年7月17日、7月23日新闻均称县委书记。",
    },
    # 何朝阳
    {
        "person_id": 2,
        "org_id": 1,
        "title": "蕲春县委常委",
        "start": "未知",
        "end": "至今",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "蕲春县常务副县长",
        "start": "未知",
        "end": "至今",
        "rank": "县处级副职",
        "note": "2026年6月2日受县长陈丹委托主持县政府常务会议。",
    },
    # 胡安元 (former party secretary)
    {
        "person_id": 3,
        "org_id": 1,
        "title": "蕲春县委书记",
        "start": "未知",
        "end": "2026-07",
        "rank": "县处级正职",
        "note": "2026年5月13日以县委书记身份主持秸秆禁烧会议。2026年7月前离任去向待查。",
    },
    # 毛红志
    {
        "person_id": 4,
        "org_id": 1,
        "title": "蕲春县委副书记",
        "start": "未知",
        "end": "至今",
        "rank": "县处级副职",
        "note": "2026年4月2日安排部署美丽城乡建设工作。",
    },
    # 张明波 / 李链稳 / 朱朝辉 — appeared in 陈丹接访 news
    {
        "person_id": 5,
        "org_id": 1,
        "title": "县领导",
        "start": "未知",
        "end": "至今",
        "rank": "县处级",
        "note": "2026年7月17日参加县委书记陈丹信访接访活动。",
    },
    {
        "person_id": 6,
        "org_id": 1,
        "title": "县领导",
        "start": "未知",
        "end": "至今",
        "rank": "县处级",
        "note": "2026年7月17日参加县委书记陈丹信访接访活动。",
    },
    {
        "person_id": 7,
        "org_id": 1,
        "title": "县领导",
        "start": "未知",
        "end": "至今",
        "rank": "县处级",
        "note": "2026年7月17日参加县委书记陈丹信访接访活动。",
    },
    # Deputy county mayors
    {
        "person_id": 8,
        "org_id": 2,
        "title": "蕲春县副县长",
        "start": "未知",
        "end": "至今",
        "rank": "县处级副职",
        "note": "2026年5月13日参加秸秆禁烧会议。2026年4月2日参加美丽城乡建设工作会。",
    },
    {
        "person_id": 9,
        "org_id": 2,
        "title": "蕲春县副县长",
        "start": "未知",
        "end": "至今",
        "rank": "县处级副职",
        "note": "2026年5月13日参加秸秆禁烧会议。2026年5月19日参加安全饮水和城市内涝防范工作会。",
    },
    {
        "person_id": 10,
        "org_id": 2,
        "title": "蕲春县副县长",
        "start": "未知",
        "end": "至今",
        "rank": "县处级副职",
        "note": "2026年5月13日参加秸秆禁烧会议。",
    },
    {
        "person_id": 11,
        "org_id": 2,
        "title": "蕲春县副县长、县红十字会会长",
        "start": "未知",
        "end": "至今",
        "rank": "县处级副职",
        "note": "2026年7月22日陪同市红十字会调研。",
    },
    # 王开伟
    {
        "person_id": 12,
        "org_id": 1,
        "title": "县领导",
        "start": "未知",
        "end": "至今",
        "rank": "县处级",
        "note": "2026年7月23日陪同省政协调研。",
    },
    # 童文军
    {
        "person_id": 13,
        "org_id": 1,
        "title": "县领导",
        "start": "未知",
        "end": "至今",
        "rank": "县处级",
        "note": "2026年7月23日陪同省政协调研。",
    },
    # 杨振武
    {
        "person_id": 14,
        "org_id": 1,
        "title": "县领导",
        "start": "未知",
        "end": "至今",
        "rank": "县处级",
        "note": "2026年4月2日参加美丽城乡建设工作会。",
    },
    # 陈泽明
    {
        "person_id": 15,
        "org_id": 1,
        "title": "县领导",
        "start": "未知",
        "end": "至今",
        "rank": "县处级",
        "note": "2026年4月2日参加美丽城乡建设工作会。",
    },
    # 杨海燕
    {
        "person_id": 16,
        "org_id": 1,
        "title": "县领导",
        "start": "未知",
        "end": "至今",
        "rank": "县处级",
        "note": "2026年5月19日参加安全饮水及内涝防范工作会。",
    },
    # 范成意
    {
        "person_id": 17,
        "org_id": 1,
        "title": "县领导",
        "start": "未知",
        "end": "至今",
        "rank": "县处级",
        "note": "2026年5月19日参加安全饮水及内涝防范工作会。",
    },
    # 欧阳畅贤
    {
        "person_id": 18,
        "org_id": 2,
        "title": "县政府领导",
        "start": "未知",
        "end": "至今",
        "rank": "县处级",
        "note": "2026年4月13日参加县政府党组（扩大）会议。",
    },
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────

relationships = [
    # 陈丹 ←→ 胡安元: predecessor/successor
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "胡安元为前任县委书记，陈丹接任。两人在2026年5月13日全县夏季秸秆禁烧推进会上曾同场（胡安元主持会议，陈丹作工作部署）。",
        "overlap_org": "中共蕲春县委员会",
        "overlap_period": "~2021至2026-07",
    },
    # 陈丹 ←→ 何朝阳: superior/subordinate
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "陈丹任县长期间，何朝阳为常务副县长，常受委托主持县政府常务会议。",
        "overlap_org": "蕲春县人民政府",
        "overlap_period": "陈丹任县长期间",
    },
    # 陈丹 ←→ 毛红志: deputy
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "陈丹任县长期间毛红志任县委副书记，同场出席美丽城乡建设工作会。",
        "overlap_org": "中共蕲春县委员会/蕲春县人民政府",
        "overlap_period": "2026年",
    },
    # 陈丹 ←→ 王超辉: overlap
    {
        "person_a": 1,
        "person_b": 8,
        "type": "overlap",
        "context": "陈丹任县长期间王超辉任副县长，多次同场参加会议。",
        "overlap_org": "蕲春县人民政府",
        "overlap_period": "2026年",
    },
    # 陈丹 ←→ 张攀: overlap
    {
        "person_a": 1,
        "person_b": 9,
        "type": "overlap",
        "context": "多次同场参加会议（秸秆禁烧、安全饮水等）。",
        "overlap_org": "蕲春县人民政府",
        "overlap_period": "2026年",
    },
    # 张明波 / 李链稳 / 朱朝辉 — 陪陈丹接访
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "张明波陪同县委书记陈丹接待来访群众。",
        "overlap_org": "中共蕲春县委员会",
        "overlap_period": "2026-07",
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "overlap",
        "context": "李链稳陪同县委书记陈丹接待来访群众。",
        "overlap_org": "中共蕲春县委员会",
        "overlap_period": "2026-07",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "overlap",
        "context": "朱朝辉陪同县委书记陈丹接待来访群众。",
        "overlap_org": "中共蕲春县委员会",
        "overlap_period": "2026-07",
    },
    # 王超辉 / 张攀 / 张立新: colleagues
    {
        "person_a": 8,
        "person_b": 9,
        "type": "overlap",
        "context": "同为副县长，多次同场参会。",
        "overlap_org": "蕲春县人民政府",
        "overlap_period": "2026年",
    },
    {
        "person_a": 8,
        "person_b": 10,
        "type": "overlap",
        "context": "同为副县长，同场参加秸秆禁烧会议。",
        "overlap_org": "蕲春县人民政府",
        "overlap_period": "2026-05",
    },
    {
        "person_a": 9,
        "person_b": 10,
        "type": "overlap",
        "context": "同为副县长，同场参加秸秆禁烧会议。",
        "overlap_org": "蕲春县人民政府",
        "overlap_period": "2026-05",
    },
    # 何朝阳 ←→ 欧阳畅贤
    {
        "person_a": 2,
        "person_b": 18,
        "type": "overlap",
        "context": "何朝阳、欧阳畅贤均为县政府领导，同场参加县政府党组（扩大）会议。",
        "overlap_org": "蕲春县人民政府",
        "overlap_period": "2026-04",
    },
    # 王开伟 / 童文军
    {
        "person_a": 12,
        "person_b": 13,
        "type": "overlap",
        "context": "同场陪同省政协调研。",
        "overlap_org": "中共蕲春县委员会",
        "overlap_period": "2026-07",
    },
    # 杨海燕 / 范成意
    {
        "person_a": 16,
        "person_b": 17,
        "type": "overlap",
        "context": "同场参加安全饮水及城市内涝防范工作会。",
        "overlap_org": "中共蕲春县委员会",
        "overlap_period": "2026-05",
    },
]

# ── BUILD ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"Done. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
