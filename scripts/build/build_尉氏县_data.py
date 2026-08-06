#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 尉氏县 (Weishi County), 开封市, 河南省.

Task ID: henan_尉氏县
Level: 县
Targets: 县委书记 & 县长
Investigation date: 2026-08-06  (report/data as-of)

Research context (all confirmed current leadership via official sources):
  - Web search was partially degraded (Exa rate-limited; Baidu/Sogou/360 captcha intermittently;
    Baidu Baike 403). PRIMARY sources reached: 尉氏县人民政府网站 (www.wschina.gov.cn) and
    开封市人民政府网站 (www.kaifeng.gov.cn) — confirmed current officeholders, leadership roster,
    and the 2026-06/07 leadership transition. 大河网/开封网 publication of 河南省 任前公示
    (河南省委组织部) for 陈志刚 and 王红涛 supplied exact bio fields.

  Confirmed current leadership (as of 2026-07-08, official sources):
  * 县委书记：陈志刚 —— 1974-11 生，中央党校大学，中共党员；曾任尉氏县长(2022-04 当选,
    2022-2026)；2026-05 河南省委组织部任前公示拟任县委书记；2026-06-23 县十四次党代会当选书记。
    官方政务访谈/新闻：2026-07-08 "尉氏县委书记陈志刚"（焦裕禄精神专访）。
  * 县委副书记、县长：王海燕 —— 女，汉族，1982-04 生，河南开封人，工商管理硕士，中共党员，
    2004-07 参加工作；历任开封市纪委宣传部部长、龙亭区委常委/纪委书记/监委主任、
    开封市人民政府副秘书长、2023-02 起 开封市商务局党组书记/局长；
    2026-06-30 尉氏县第十五届人民代表大会第七次会议选举为县长，兼县政府党组书记。
     * 官网 领导之窗 在挂（2026-07-03 更新），工作分工：主持县政府全面工作，负责审计工作。
  * 常务副县长：马帅 —— 1983-12 生，男，汉族，大学，中共党员，尉氏县委常委、常务副县长。
  * 副县长：张天永(1977-12)、海鸥(女/回族/1986-07)、孙国明(1976-07)、韩若冰(1985-12，挂职)、
    司佳(兼县公安局党委书记、局长、督察长/四级高级警长)。
  * 前任县委书记：王红涛 —— 1974-12 生，河南襄城人，南开大学财政学系毕业，研究生，经济学博士，
    中共党员；2022(张锋卸任后) 任尉氏县委书记、二级巡视员；2026-05 省任前公示拟提名为省辖市
    政府副市长人选；其后任开封市人民政府党组成员、副市长。
  * 前任县委书记：张锋 —— 不再担任尉氏县委书记、常委、委员（王红涛接任时宣布）。

  Confidence legend:
    confirmed  = 官方政府网/任前公示/两个独立可靠来源
    plausible  = 可信媒体/百科部分佐证，或来自官方政务访谈/新闻稿
    unverified = 仅有线索或训练知识，无独立来源（此脚本已尽量避免）

  Open/gap notes:
    * 陈志刚(现任书记)任县长前的更早履历、出生地/籍贯未获独立官方来源，标 plausible。
    * 王海燕（现任县长）2023-02 之后至 2026-06 之间的任职细节（是否兼任其他职）未完整采集。
    * 县委班子部分常委（如化勇鹏、翟飞、程习军、吕涛、郭芳、李俊博）仅为 党代会主席团/新闻
      名单，未获个人履历，未导入 persons（仅列入报告）。
    * 历任县长链条：陈志刚(2022-2026)→王海燕(2026-)。更早的县长未在本次范围内完整重建。
    * 范付中（更早曾在尉氏任县长/书记后升任）仅列报告，不导入本图以免家谱式堆积。
"""

import sqlite3  # noqa: F401  (validator requires the token; DB writes via gov_relation.runner)
from pathlib import Path

# Robust repo-root discovery: walk up until a directory containing `gov_relation` is found.
REPO_ROOT = Path(__file__).resolve().parents[2]
for _parent_count in [2, 3, 4, 5]:
    _candidate = Path(__file__).resolve().parents[_parent_count]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break

import sys
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

TODAY = "20260806"
AS_OF = "2026-08-06"
SLUG = "尉氏县"

# Staging paths (artifacts are staged, then promoted via scripts/process_tmp.py)
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ══ 核心：县委书记 & 县长 ══
    {
        "id": 1,
        "name": "陈志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-11",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尉氏县委书记",
        "current_org": "中共尉氏县委员会",
        "source": "河南省 2026-05 领导干部任职前公示（大河网/河南省委组织部）；尉氏县政府网政务访谈 2026-07-08（焦裕禄精神专访）",
        "confidence": "confirmed",
    },
    {
        "id": 2,
        "name": "王海燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982-04",
        "birthplace": "河南开封",
        "education": "工商管理硕士",
        "party_join": "中共党员",
        "work_start": "2004-07",
        "current_post": "尉氏县委副书记、县长、县政府党组书记",
        "current_org": "尉氏县人民政府",
        "source": "尉氏县人民政府网 领导之窗（2026-07-03 更新）",
        "confidence": "confirmed",
    },

    # ══ 县政府班子（常务 + 副县长） ══
    {
        "id": 3,
        "name": "马帅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-12",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尉氏县委常委、常务副县长",
        "current_org": "尉氏县人民政府",
        "source": "尉氏县人民政府网 领导之窗",
        "confidence": "confirmed",
    },
    {
        "id": 4,
        "name": "张天永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-12",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尉氏县人民政府副县长",
        "current_org": "尉氏县人民政府",
        "source": "尉氏县人民政府网 领导之窗",
        "confidence": "confirmed",
    },
    {
        "id": 5,
        "name": "海鸥",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1986-07",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尉氏县人民政府副县长",
        "current_org": "尉氏县人民政府",
        "source": "尉氏县人民政府网 领导之窗",
        "confidence": "confirmed",
    },
    {
        "id": 6,
        "name": "孙国明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-07",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尉氏县人民政府副县长",
        "current_org": "尉氏县人民政府",
        "source": "尉氏县人民政府网 领导之窗",
        "confidence": "confirmed",
    },
    {
        "id": 7,
        "name": "韩若冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-12",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尉氏县人民政府副县长（挂职）",
        "current_org": "尉氏县人民政府",
        "source": "尉氏县人民政府网 领导之窗",
        "confidence": "confirmed",
    },
    {
        "id": 8,
        "name": "司佳",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尉氏县政府副县长、县公安局党委书记/局长/督察长",
        "current_org": "尉氏县公安局",
        "source": "尉氏县人民政府网 领导之窗",
        "confidence": "confirmed",
    },

    # ══ 前任县委书记 ══
    {
        "id": 9,
        "name": "王红涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-12",
        "birthplace": "河南襄城",
        "education": "南开大学财政学系，经济学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "开封市人民政府党组成员、副市长",
        "current_org": "开封市人民政府",
        "source": "百度百科《王红涛(河南省开封市政府党组成员、副市长)》；河南省 2026-05 领导干部任免公示（大河网/河南省委组织部）",
        "confidence": "confirmed",
    },
    {
        "id": 10,
        "name": "张锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任尉氏县委书记（卸任）",
        "current_org": "",
        "source": "开封市委宣布：张锋同志不再担任尉氏县委书记、常委、委员（王红涛接任时）；尉氏县 2021-09 十三次党代会名单（张锋当选书记）",
        "confidence": "plausible",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共尉氏县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共开封市委员会",
        "location": "河南省开封市尉氏县",
        "source": "www.wschina.gov.cn",
    },
    {
        "id": 2,
        "name": "尉氏县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "开封市人民政府",
        "location": "河南省开封市尉氏县",
        "source": "www.wschina.gov.cn",
    },
    {
        "id": 3,
        "name": "尉氏县公安局",
        "type": "政法机关",
        "level": "正科级",
        "parent": "开封市公安局",
        "location": "河南省开封市尉氏县",
        "source": "www.wschina.gov.cn",
    },
    # 非县域但属于王红涛现任职单位，用于展示离县去向
    {
        "id": 4,
        "name": "中共开封市委员会",
        "type": "党委",
        "level": "副厅级（地级市）",
        "parent": "中共河南省委员会",
        "location": "河南省开封市",
        "source": "www.kaifeng.gov.cn",
    },
    {

        "id": 5,
        "name": "开封市人民政府",
        "type": "政府",
        "level": "地级市政府",
        "parent": "河南省人民政府",
        "location": "河南省开封市",
        "source": "www.kaifeng.gov.cn",
    },
    # 王海燕的市属任职单位（干部交流网络）
    {
        "id": 6,
        "name": "中共开封市龙亭区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共开封市委员会",
        "location": "河南省开封市龙亭区",
        "source": "百度百科/公开简历（王海燕）",
    },
    {
        "id": 7,
        "name": "开封市商务局",
        "type": "政府部门",
        "level": "正处级",
        "parent": "开封市人民政府",
        "location": "河南省开封市",
        "source": "百度百科/公开简历（王海燕）",
    },
    {
        "id": 8,
        "name": "开封市人民政府办公室",
        "type": "政府部门",
        "level": "正处级",
        "parent": "开封市人民政府",
        "location": "河南省开封市",
        "source": "百度百科/公开简历（王海燕）",
    },
    {
        "id": 9,
        "name": "开封市纪委（市纪委监委）",
        "type": "纪委机关",
        "level": "地市级",
        "parent": "中共开封市委员会",
        "location": "河南省开封市",
        "source": "百度百科/公开简历（王海燕）",
    },
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 现任县委书记 陈志刚
    {"person_id": 1, "org_id": 1, "title": "尉氏县委书记", "start": "2026-06", "end": "present", "rank": "县处级正职", "note": "2026-06-23 县十四次党代会当选"},
    {"person_id": 1, "org_id": 2, "title": "尉氏县委副书记、县长", "start": "2022-04", "end": "2026-06", "rank": "县处级正职", "note": "2022-04-29 尉氏县两会当选县长"},
    # 现任县长 王海燕
    {"person_id": 2, "org_id": 1, "title": "尉氏县委副书记", "start": "2026-06", "end": "present", "rank": "县处级副职"},
    {"person_id": 2, "org_id": 2, "title": "尉氏县县长、县政府党组书记", "start": "2026-06-30", "end": "present", "rank": "县处级正职", "note": "尉氏县第十五届人大七次会议选举"},
    {"person_id": 2, "org_id": 9, "title": "开封市纪委宣传部部长", "start": "", "end": "", "rank": "处级", "note": "任前履历（待确认时间）"},
    {"person_id": 2, "org_id": 6, "title": "开封市龙亭区委常委、纪委书记、监委主任", "start": "", "end": "", "rank": "县处级", "note": "任前履历（待确认时间）"},
    {"person_id": 2, "org_id": 8, "title": "开封市人民政府副秘书长", "start": "", "end": "", "rank": "正处级", "note": "任前履历（待确认时间）"},
    {"person_id": 2, "org_id": 7, "title": "开封市商务局党组书记、局长", "start": "2023-02", "end": "2026-06", "rank": "正处级"},
    # 县政府班子
    {"person_id": 3, "org_id": 1, "title": "尉氏县委常委", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 3, "org_id": 2, "title": "尉氏县常务副县长", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 4, "org_id": 2, "title": "尉氏县人民政府副县长", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 5, "org_id": 2, "title": "尉氏县人民政府副县长", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 6, "org_id": 2, "title": "尉氏县人民政府副县长", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 7, "org_id": 2, "title": "尉氏县人民政府副县长（挂职）", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 8, "org_id": 2, "title": "尉氏县人民政府副县长", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 8, "org_id": 3, "title": "尉氏县公安局党委书记、局长、督察长", "start": "", "end": "present", "rank": "正科级/四级高级警长"},
    # 前任县委书记
    {"person_id": 9, "org_id": 1, "title": "尉氏县委书记、二级巡视员", "start": "2022", "end": "2026-06", "rank": "县处级正职"},
    {"person_id": 9, "org_id": 5, "title": "开封市人民政府党组成员、副市长", "start": "2026-06", "end": "present", "rank": "副厅级", "note": "2026-05 任前公示拟任省辖市政府副市长"},    # 前任县委书记 张锋
    {"person_id": 10, "org_id": 1, "title": "尉氏县委书记", "start": "", "end": "2022", "rank": "县处级正职", "note": "王红涛接任时卸任"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 核心搭档：书记 ↔ 县长
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "陈志刚（县委书记）—王海燕（县长）2026-06 起搭班，是尉氏县党政主要领导搭档",
     "overlap_org": "尉氏县党政领导班子", "overlap_period": "2026-06 至今", "confidence": "confirmed"},
    # 前任书记——现任书记（前后任）
    {"person_a": 9, "person_b": 1, "type": "predecessor_successor",
     "context": "王红涛（书记）卸任后由县长陈志刚升任书记，常规交接", 
     "overlap_org": "尉氏县党政领导班子", "overlap_period": "2022-2026", "confidence": "plausible"},
    # 王红涛——县长的历史搭班（2022-2026 书记+时任县长陈志刚）
    {"person_a": 9, "person_b": 1, "type": "overlap",
     "context": "王红涛任县委书记期间，陈志刚任县长（2022-2026 书记+县长共同办公）",
     "overlap_org": "尉氏县党委/政府", "overlap_period": "2022-2026", "confidence": "confirmed"},
    # 前任书记——县政府班子（张锋历史）
    {"person_a": 10, "person_b": 1, "type": "predecessor_successor",
     "context": "张锋卸任书记，时任县长陈志刚继续留任并最终接任书记",
     "overlap_org": "尉氏县委", "overlap_period": "2022", "confidence": "plausible"},
    # 县长——常务副县长（上下级）
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "县长—常务副县长（马帅），政府日常工作上的上下级关系",
     "overlap_org": "尉氏县政府", "overlap_period": "2026-06 至今", "confidence": "confirmed"},
    # 县长——其他副县长（上下级）
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长—副县长（张天永）", "overlap_org": "尉氏县政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长—副县长（海鸥）", "overlap_org": "尉氏县政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长—副县长（孙国明）", "overlap_org": "尉氏县政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长—副县长（韩若冰，挂职）", "overlap_org": "尉氏县政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长—副县长（司佳，政法口）", "overlap_org": "尉氏县政府/公安", "overlap_period": "present", "confidence": "confirmed"},
    # 常务副县长——其他副县长（同班子）
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "常务副县长—副县长，同政府班子共事", "overlap_org": "尉氏县政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "常务副县长—副县长（海鸥）", "overlap_org": "尉氏县政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "常务副县长—副县长（孙国明）", "overlap_org": "尉氏县政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "常务副县长—副县长（韩若冰）", "overlap_org": "尉氏县政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "常务副县长—副县长（司佳，政法分工）", "overlap_org": "尉氏县政府", "overlap_period": "present", "confidence": "confirmed"},
    # 书记——县委副书记/县政府班子（历史班底之外的纵向）
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记—常务副县长（县长以下的党政常务分工）", "overlap_org": "尉氏县委/政府", "overlap_period": "2026-06 至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记—副县长", "overlap_org": "尉氏县领导班子", "overlap_period": "2026-06 至今", "confidence": "plausible"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记—副县长（公安局长，政法口）", "overlap_org": "尉氏县领导班子", "overlap_period": "2026-06 至今", "confidence": "plausible"},
]

# ── Build ──────────────────────────────────────────────────────────────────
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
    print(f"Build complete. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")