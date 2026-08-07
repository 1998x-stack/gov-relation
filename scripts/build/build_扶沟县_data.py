#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 扶沟县 (Fugou County), 周口市, 河南省.

Investigation date: 2026-08-07
Task ID: henan_扶沟县
Level: 县
Targets: 县委书记 & 县长

Research sources (all official primary, accessed 2026-08-07):
  - 扶沟县人民政府官网 www.fugou.gov.cn (http), 领导之窗 leader bio pages.
  - 扶沟县委常委会 news (2026-07-22), 八一慰问 (2026-07-31): 县委书记 李祥生.
  - 扶沟县十六届人大常委会第29次会议 (2026-07-29): 县长 李涛, 人大主任 肖炜,
    王刘明 获任副县长, 法检两长.
  - 扶沟县信访局《关于扶沟县领导干部接访工作的公告》(2026-08-03): 完整 县委/县政府班子名单.
  - 扶沟县第十五次党员代表大会 (2026-06): 县委常委会选举, 李祥生 继任书记.
  - 扶政〔2025〕1号 县政府班子分工通知 (2025-05-30): 前任班子快照 (李祥生=县长, 李涛=常务副县长).
  - 周口市人民政府 www.zhoukou.gov.cn: 市委书记 黄玉国, 市长 詹鹏 (context).
  - 大河网人事/任前公示 https://news.dahe.cn/rsrm/: 周口市内"县长→书记"提拔模式旁证.

Confidence notes:
  - 现任县委书记 李祥生 (李 X) —— confirmed via multiple official news; 曾2025-05任县长后升书记.
  - 现任县长 李涛 —— confirmed via 政府常务会 + 人大常委会 + 接访表; 男,回族,本科学历,中共党员;
    2025-05 时任常务副县长, 后升县长.
  - 县常委会 (接访表 2026-08-03): 尚守永(副书记/政法委), 夏逢源(常委/县委办主任),
    申洪(常委/副县长), 王刘明(常委/常务副县长), 黄宇飞(常委/组织部长), 宋晓霞(常委/宣传部长),
    郭辉(常委/统战部长), 孟涛(常委/纪委书记/监委主任).
  - 政府班子成员 bio (领导之窗): 王刘明(1984-10 男汉本科党员), 徐彩云(1972-08 女汉研究生党员 副县长/公安局长),
    张伟(1981-07 男汉研究生党员 副县长), 郭辉(1974-06 男汉本科党员).
  - 人大: 主任 肖炜; 副主任 魏军占、郑峰、万群玲、杨建华. 法院院长 吴骥原; 检察长 韩中华.
  - 前任县委书记: 待查 (李 x 由县长升书记; 前书记需周重申委组织部任前公示). GAP.
  - 前任县长: 2025-05 前为李祥生? No — 2025-05 县长即李祥生. 再前任(李涛之前) 未查.
    实际上 2025-05 分工表县长=李祥生, 常务=李涛. 换届后 李祥生任书记, 李涛任县长.
  - 周德者(2022-2025 常委宣传部长/副县长, 分管农业) 2026-08 已不在接访表 → 去向待查.
  - Cross-county (周口市, 玄体系): 张建党(淮阳区委书记→周口市市委常委/常务副市长),
    田庆者(西华县委书记→沈丘县委书记), 马昭才(西华县长→县委书记, 2026-02-27 河南省委组织部任前公示).
  - 大量人物完整履历 (出生/学历/籍贯/入党) 未知 → 置 confidence=unverified, 写入 open_questions.

This is a partial-evidence artifact. Core current roles are confirmed from official primary
sources (扶沟县政府官网 + 县人大常委会/县委调研); historical career details for most officials
are preserved as unknown/plausible rather than fabricated.
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent

def _find_repo_root(start: Path) -> Path:
    """Locate the repository root by walking up to the ancestor containing gov_relation/ and data/."""
    for p in [start] + list(start.parents):
        if (p / "gov_relation").is_dir() and (p / "data").is_dir():
            return p
    return start

BASE = _find_repo_root(STAGING_DIR)
SLUG = "扶沟县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# Output paths: write directly into canonical database/graph dirs.
DB_PATH = BASE / "data" / "database" / f"{SLUG}_network.db"
GEXF_PATH = BASE / "data" / "graph" / f"{SLUG}_network.gexf"

# Canonical paths
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"

# ── Helper: ID offset for orgs ─────────────────────────────────────────────
ORG_OFFSET = 100000


# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership (targets) ═══════
    {
        "id": 1,
        "name": "李祥生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共扶沟县委员会",
        "source": "Official news 2026-07-22 县委常委会 (http://www.fugou.gov.cn/...bbdcbfddf8a74ff0b1a3d0bddcca4a5a.html); 2026-07-31 八一慰问 (https://r.jina.ai/http://http://www.fugou.gov.cn/...a8e6088541dd48208c296857bdf2acfa.html); 第十五次党代会 2026-06; 接访表 8/10, 8/24. 2025-05 曾任县长 (扶政〔2025〕1号)."
    },
    {
        "id": 2,
        "name": "李涛",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "扶沟县人民政府",
        "source": "Official bio 领导之窗 (2025-12-05): 男,回族,本科学历,中共党员,现任扶沟县委常委、政府县长、党组书记. 人大常委会第29次 (2026-07-29), 政府第75次常务会. 2025-05 曾任常务副县长."
    },
    # ═══════ 县委常委会 (from 接访公告 2026-08-03) ═══════
    {
        "id": 3,
        "name": "尚守永",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、政法委书记",
        "current_org": "中共扶沟县委员会",
        "source": "接访公告 2026-08-03 (8/11); 八一慰问同行 (2026-07-31)."
    },
    {
        "id": 4,
        "name": "夏逢源",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共扶沟县委员会",
        "source": "接访公告 2026-08-03 (8/4, 8/21); 八一慰问同行."
    },
    {
        "id": 5,
        "name": "申洪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "扶沟县人民政府",
        "source": "接访公告 2026-08-03 (8/5, 8/25); 2025-05 曾任县政府党组成员、包屯镇党委书记 (扶政〔2025〕1号)."
    },
    {
        "id": 6,
        "name": "王刘明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-10",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "扶沟县人民政府",
        "source": "Official bio 领导之窗 (2022-06-09); 人大常委会第29次 (2026-07-29) 任命副县长; 接访公告 2026-08-03."
    },
    {
        "id": 7,
        "name": "黄宇飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部长",
        "current_org": "中共扶沟县委员会",
        "source": "接访公告 2026-08-03 (8/14)."
    },
    {
        "id": 8,
        "name": "宋晓霞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部长",
        "current_org": "中共扶沟县委员会",
        "source": "全县宣传思想文化工作会议; 接访公告 2026-08-03 (8/7, 8/26)."
    },
    {
        "id": 9,
        "name": "郭辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-06",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部长",
        "current_org": "中共扶沟县委员会",
        "source": "Official bio 领导之窗 (2023-12-21) 副县长; 接访公告 2026-08-03 (8/19) 统战部长. 2025 副县长→2026 统战部长 (转移待确认)."
    },
    {
        "id": 10,
        "name": "孟涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共扶沟县纪律检查委员会",
        "source": "党代会预备会 (换届纪律部署); 接访公告 2026-08-03 (8/20)."
    },
    # ═══════ 县政府 (副县长) ═══════
    {
        "id": 11,
        "name": "徐彩云",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972-08",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "扶沟县人民政府",
        "source": "Official bio 领导之窗 (2022-06-09): 女,汉族,1972-08,研究生学历; 接访公告 2026-08-03 (8/13)."
    },
    {
        "id": 12,
        "name": "张伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-07",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "扶沟县人民政府",
        "source": "Official bio 领导之窗 (2022-06-09): 男,汉族,1981-07,研究生学历; 接访公告 2026-08-03 (8/18)."
    },
    {
        "id": 13,
        "name": "周德志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-12",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委常委、宣传部长、副县长",
        "current_org": "扶沟县人民政府",
        "source": "Official bio 领导之窗 (2022-06-09): 男,汉族,1973-12,研究生学历,曾任县委常委/宣传部长/副县长, 分管农业农村. 2026-08已不在接访表 → 去向待查."
    },
    # ═══════ 人大 / 法检 ═══════
    {
        "id": 14,
        "name": "肖炜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "扶沟县人民代表大会常务委员会",
        "source": "县十六届人大常委会第29次会议 (2026-07-29)."
    },
    {
        "id": 15,
        "name": "吴冀原",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人民法院院长",
        "current_org": "扶沟县人民法院",
        "source": "人大常委会第29次会议 (2026-07-29); 接访公告 2026-08-03 (8/6)."
    },
    {
        "id": 16,
        "name": "韩中华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人民检察院检察长",
        "current_org": "扶沟县人民检察院",
        "source": "人大常委会第29次会议 (2026-07-29)."
    },
    # ═══════ 前任 & 跨区网络 ═══════
    {
        "id": 17,
        "name": "周口市市长 詹鹏 (context)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "周口市市长 (context)",
        "current_org": "周口市人民政府",
        "source": "周口市政府官网 (zhoukou.gov.cn) 政务动态; 限于县级任务, 仅作上级网络 context."
    },
]


# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {
        "id": ORG_OFFSET + 1,
        "name": "中共扶沟县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共周口市委",
        "location": "河南省周口市扶沟县"
    },
    {
        "id": ORG_OFFSET + 2,
        "name": "扶沟县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "周口市人民政府",
        "location": "河南省周口市扶沟县"
    },
    {
        "id": ORG_OFFSET + 3,
        "name": "中共扶沟县纪律检查委员会",
        "type": "纪律检查",
        "level": "县级",
        "parent": "中共周口市纪律检查委员会",
        "location": "河南省周口市扶沟县"
    },
    {
        "id": ORG_OFFSET + 4,
        "name": "扶沟县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "河南省人民代表大会常务委员会",
        "location": "河南省周口市扶沟县"
    },
    {
        "id": ORG_OFFSET + 5,
        "name": "扶沟县人民法院",
        "type": "政府",
        "level": "县级",
        "parent": "周口市中级人民法院",
        "location": "河南省周口市扶沟县"
    },
    {
        "id": ORG_OFFSET + 6,
        "name": "扶沟县人民检察院",
        "type": "政府",
        "level": "县级",
        "parent": "周口市人民检察院",
        "location": "河南省周口市扶沟县"
    },
    {
        "id": ORG_OFFSET + 7,
        "name": "扶沟县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "扶沟县人民政府",
        "location": "河南省周口市扶沟县"
    },
    {
        "id": ORG_OFFSET + 8,
        "name": "周口市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "河南省人民政府",
        "location": "河南省周口市"
    },
]


# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 李祥生 (書記)
    {"person_id": 1, "org_id": ORG_OFFSET + 1, "title": "县委书记", "start": "2025-06", "end": "present", "rank": "正县处级", "note": "自2025-06(党内升任)任书记; 经多次官方新闻确认至2026-08"},
    {"person_id": 1, "org_id": ORG_OFFSET + 2, "title": "县长 (前任)", "start": "", "end": "2025-05", "rank": "正县处级", "note": "扶政〔2025〕1号 2025-05-30 仍任县长"},
    # 李涛 (县长)
    {"person_id": 2, "org_id": ORG_OFFSET + 2, "title": "县长", "start": "2026", "end": "present", "rank": "正县处级", "note": "2026 任县长, 主持人常委会; 人大常委会第29次会议列席"},
    {"person_id": 2, "org_id": ORG_OFFSET + 1, "title": "县委副书记", "start": "2026", "end": "present", "rank": "正县处级", "note": ""},
    {"person_id": 2, "org_id": ORG_OFFSET + 2, "title": "常务副县长 (前任)", "start": "", "end": "2025", "rank": "副县处级", "note": "扶政〔2025〕1号 2025-05 任常务副县长"},
    # 县委常委会
    {"person_id": 3, "org_id": ORG_OFFSET + 1, "title": "县委副书记、政法委书记", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 4, "org_id": ORG_OFFSET + 1, "title": "县委常委、县委办公室主任", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 5, "org_id": ORG_OFFSET + 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 6, "org_id": ORG_OFFSET + 2, "title": "县委常委、常务副县长", "start": "2026-07", "end": "present", "rank": "副县处级", "note": "2026-07-29 获任副县长(常务)"},
    {"person_id": 6, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 7, "org_id": ORG_OFFSET + 1, "title": "县委常委、组织部长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 8, "org_id": ORG_OFFSET + 1, "title": "县委常委、宣传部长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 9, "org_id": ORG_OFFSET + 1, "title": "县委常委、统战部长", "start": "", "end": "present", "rank": "副县处级", "note": "接访表列统战部长; 2025-2026 由副县长转移"},
    {"person_id": 10, "org_id": ORG_OFFSET + 3, "title": "县委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    # 县政府
    {"person_id": 11, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副县处级", "note": "负责公安、司法、交通、信访"},
    {"person_id": 11, "org_id": ORG_OFFSET + 7, "title": "县公安局局长", "start": "", "end": "present", "rank": "副县处级", "note": "公安局长一体"},
    {"person_id": 12, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副县处级", "note": "负责规划、城建、自然资源"},
    # 周德志 (转任/前任)
    {"person_id": 13, "org_id": ORG_OFFSET + 1, "title": "县委常委 (前任)", "start": "", "end": "2025-05", "rank": "副县处级", "note": "曾任宣传部长; 2026-08 已不在班子名单"},
    {"person_id": 13, "org_id": ORG_OFFSET + 2, "title": "副县长 (前任)", "start": "", "end": "2025", "rank": "副县处级", "note": "分管农业农村"},
    # 人大 / 法检
    {"person_id": 14, "org_id": ORG_OFFSET + 4, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正县处级", "note": ""},
    {"person_id": 15, "org_id": ORG_OFFSET + 5, "title": "县人民法院院长", "start": "", "end": "present", "rank": "正县处级", "note": ""},
    {"person_id": 16, "org_id": ORG_OFFSET + 6, "title": "县人民检察院检察长", "start": "", "end": "present", "rank": "正县处级", "note": ""},
    # 周口市 (context)
    {"person_id": 17, "org_id": ORG_OFFSET + 8, "title": "市长", "start": "", "end": "present", "rank": "正厅级", "note": "上级市领导 (context)"},
]


# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档 (书记—县长)
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记李祥生 与 县长李涛 现党政搭档 (2025-06 换届后)",
        "overlap_org": "扶沟县",
        "overlap_period": "2025-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 书记与县委副书记/政法
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记 与 县委副书记、政法委书记尚守永",
        "overlap_org": "中共扶沟县委员会",
        "overlap_period": "2025-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 县长与常委副县长
    {
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "县长李涛 与 常务副县长王刘明 共事",
        "overlap_org": "扶沟县人民政府",
        "overlap_period": "2026-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 县政府班子
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "县长与县委常委、副县长申洪 共事",
        "overlap_org": "扶沟县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 11,
        "type": "overlap",
        "context": "县长与副县长、公安局长徐彩云 共事",
        "overlap_org": "扶沟县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 12,
        "type": "overlap",
        "context": "县长与副县长张伟 共事",
        "overlap_org": "扶沟县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 书记与人大主任
    {
        "person_a": 1, "person_b": 14,
        "type": "superior_subordinate",
        "context": "县委书记与县人大主任肖炜搭档",
        "overlap_org": "扶沟县",
        "overlap_period": "2025-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 老班子 (李祥生 县长 → 李涛 常务) 传承
    {
        "person_a": 1, "person_b": 2,
        "type": "predecessor_successor",
        "context": "2025-05 前: 李祥生任县长, 李涛任常务副县长; 换届后李祥生任书记, 李涛升任县长 (班子交接)",
        "overlap_org": "扶沟县人民政府",
        "overlap_period": "2025",
        "strength": "strong",
        "confidence": "plausible"
    },
    # 常务副县长王刘明 与 县长李涛 交接
    {
        "person_a": 6, "person_b": 2,
        "type": "predecessor_successor",
        "context": "李涛任县长后, 王刘明接任常务副县长 (2026-07-29 获任副县长)",
        "overlap_org": "扶沟县人民政府",
        "overlap_period": "2026",
        "strength": "medium",
        "confidence": "plausible"
    },
    # 前任宣传部长周德志 与 现宣传部长宋晓霞 (前后任)
    {
        "person_a": 13, "person_b": 8,
        "type": "predecessor_successor",
        "context": "周德志曾任宣传部长/副县长, 现离任; 宋晓霞任现任宣传部长",
        "overlap_org": "中共扶沟县委员会",
        "overlap_period": "2026",
        "strength": "medium",
        "confidence": "plausible"
    },
    # 公安线
    {
        "person_a": 11, "person_b": 1,
        "type": "superior_subordinate",
        "context": "徐彩云 (副县长/公安局长) 隶属县委县政府领导",
        "overlap_org": "扶沟县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 法检两长
    {
        "person_a": 15, "person_b": 1,
        "type": "overlap",
        "context": "县法院院长吴冀原 与县委领导 (政法口)",
        "overlap_org": "扶沟县",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "plausible"
    },
    {
        "person_a": 16, "person_b": 1,
        "type": "overlap",
        "context": "县检察院检察长韩中华 与县委领导 (政法口)",
        "overlap_org": "扶沟县",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "plausible"
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# Database + GEXF build
# ═══════════════════════════════════════════════════════════════════════════

def build():
    """Build SQLite database and GEXF graph."""
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

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


def verify():
    """Verify output files exist and have correct structure."""
    import sqlite3
    errors = []

    if not DB_PATH.exists():
        errors.append(f"Database not found: {DB_PATH}")
    else:
        conn = sqlite3.connect(str(DB_PATH))
        tables = [row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )]
        expected = ["persons", "organizations", "positions", "relationships"]
        for t in expected:
            if t not in tables:
                errors.append(f"Missing table: {t}")
        for t in expected:
            c = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            print(f"  {t}: {c}")
        conn.close()

    if not GEXF_PATH.exists():
        errors.append(f"GEXF not found: {GEXF_PATH}")
    else:
        content = GEXF_PATH.read_text("utf-8")
        if '<gexf' not in content:
            errors.append("GEXF missing <gexf> tag")
        if '<nodes>' not in content:
            errors.append("GEXF missing <nodes>")
        if '<edges>' not in content:
            errors.append("GEXF missing <edges>")
        if '</gexf>' not in content:
            errors.append("GEXF missing closing </gexf>")

    if errors:
        for e in errors:
            print(f"  ERROR: {e}")
        return False
    print("  Verification: PASSED")
    return True


if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    build()
    print("\nVerifying...")
    if verify():
        print("\nDone. Files created:")
        print(f"  DB:   {DB_PATH}")
        print(f"  GEXF: {GEXF_PATH}")
    else:
        print("\nFAILED: verification errors")
        sys.exit(1)