#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 城固县 (Chenggu County), 汉中市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_城固县
Level: 县
Targets: 县委书记 & 县长

Research sources (primary official, accessed 2026-08-07):
  - 城固县人民政府官网 www.chenggu.gov.cn (http): 领导之窗 profiles, 城固要闻,
    全县公开接访安排公告 (7/20-7/24, 7/27-7/31), 县十九届人大常委会第三十二次会议 (2026-08-04).
  - 汉中市人民政府 www.hanzhong.gov.cn: 张烨(市委书记) 会见新闻 2026-08-07.
  - 陕西省委组织部干部任前公示 (2026-07-14: 王钧平 拟进一步使用; 2026-07-20: 李鹏程 拟任党政正职) +
    中国共产党新闻网/陕西网 转载.
  - 城固县纪委监委 (chenggu.qinfeng.gov.cn) 述责述廉会 2026-01-30: 黄锐(纪委书记/监委主任).
  - 城固县人大网站: 人大常委会任免.

Confidence notes:
  - 现任县委书记 王钧平 —— confirmed. 男,汉族,1974-10,省委党校研究生,中共党员. 历任 汉中市委政法委政治部主任→镇巴县纪委书记→汉中市人大副秘书长/办公室主任→汉中市应急管理局局长→汉中市滨江新区书记→城固县委副书记、县长(2025.03-2026.07)→县委书记(2026.08). 兼汉中航空技术开发区管委会主任.
    官方简历页 2026-07-30 更新为书记; 接访公告 2026-07-29 仍列 "县委副书记、县长" → 近期升任书记.
  - 现任代县长 李鹏程 —— 通过 2026-08-04 县人大常委会第三十二次会议 决定任命为副县长并代理县长; 县政府党组书记.
    男, 汉族, 1985-10, 大学, 农学学士, 中共党员; 原 南郑区委常委、副区长、党组副书记 (2026-07-20 任前公示).
  - 县委班子 (接访公告 2026-07): 常务副县长 杨奇涛, 常委副县长 陈超, 陈新林,
    副县长 王艳云(民盟), 宋本明, 尹建忠, 王淳(党组成员,省工信厅挂职), 李秀虎(副县长·公安局长);
    政法委书记 王雪冰; 组织部长 胡传明.
  - 人大: 主任 肖万鹏; 副主任 靳侠、孙刚、张天元、张春. 法院院长 余家武; 检察长 俞健;
    监委代主任 王伟 (2026-08-04 决定). 纪委书记 黄锐 (2025).
  - 前任县委书记 王健梅 (女, 1979-06, 工程硕士) —— 2025-01 至 2026-07 任书记(此前2022 县长), 去向待查.
  - 前任县长 时序链: 王健梅(县长~2022-2025初) → 王钧平(县长 2025初-2026.07) → 李鹏程(2026.08起·代县长).
  - 汉中市 context: 市委书记 张烨; 市委组织部部长 周耀宜; 市纪委书记 钟伟.

This is a partial-evidence artifact. Core current roles are confirmed from official primary sources;
some historical career segments (尤其 王钧平 2025 年前、王健梅去职后) are preserved as unknown/plausible
rather than fabricated.
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent

def _find_repo_root(start: Path) -> Path:
    for p in [start] + list(start.parents):
        if (p / "gov_relation").is_dir() and (p / "data").is_dir():
            return p
    return start

BASE = _find_repo_root(STAGING_DIR)
SLUG = "城固县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# Canonical output paths (self-contained reproducible build).
DB_PATH = BASE / "data" / "database" / f"{SLUG}_network.db"
GEXF_PATH = BASE / "data" / "graph" / f"{SLUG}_network.gexf"

ORG_OFFSET = 100000


# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core targets (县委书记 & 县长) ═══════
    {
        "id": 1,
        "name": "王钧平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-10",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共城固县委员会",
        "source": "任前公示 2026-07-14 (陕西省委组织部); 城固县政府官网 领导之窗 (更新2026-07-30); 接访公告 2026-07-29; 县委常委会 2026-08-02. 履历前后跨镇巴/汉中市/应急局/滨江新区等."
    },
    {
        "id": 2,
        "name": "李鹏程",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-10",
        "birthplace": "",
        "education": "大学(农学学士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、代县长",
        "current_org": "城固县人民政府",
        "source": "任前公示 2026-07-20 (陕西省委组织部项目政职); 县十九届人大常委会第三十二次会议 2026-08-04 决定任命副县长、决定代理县长; 城固县政府新闻 2026-08-04/05 (李鹏程调研重点/航空项目). 原南郑区委常委、副区长、党组副书记."
    },
    # ═══════ 县委常委会 (接访公告 2026-07-20~31, 2026-08) ═══════
    {
        "id": 3,
        "name": "杨奇涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "城固县人民政府",
        "source": "领导之窗 2026 (研究生学历, 党员, 党组副书记); 县人大常委会 2026-08-04 列席."
    },
    {
        "id": 4,
        "name": "陈超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "城固县人民政府",
        "source": "领导之窗 (研究生学历, 党员); 接访公告 2026-07-28 (分管住建/生态/城管/文旅/城投/棚改)."
    },
    {
        "id": 5,
        "name": "陈新林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "城固县人民政府",
        "source": "领导之窗 (研究生学历, 党员); 接访公告 2026-07-21 (分管苏陕协作、科技)."
    },
    {
        "id": 6,
        "name": "王艳云",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "民盟盟员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "城固县人民政府",
        "source": "领导之窗: 女, 汉族, 大学学历, 民盟盟员; 分管卫生/民政/医保."
    },
    {
        "id": 7,
        "name": "宋本明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "城固县人民政府",
        "source": "领导之窗 (大学学历, 党员); 接访公告 2026-07-27 (分管农业/水利/林业/交通)."
    },
    {
        "id": 8,
        "name": "尹建忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "城固县人民政府",
        "source": "领导之窗 (大学学历, 党员, 更新2026-05-12)."
    },
    {
        "id": 9,
        "name": "李秀虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、公安局长",
        "current_org": "城固县人民政府",
        "source": "领导之窗 (男,汉族,大学学历,党员; 现任副县长/党组成员/公安局长); 接访公告 2026-07-22."
    },
    {
        "id": 10,
        "name": "王淳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员",
        "current_org": "城固县人民政府",
        "source": "领导之窗 (大学学历,党员; 省工信厅定点帮扶挂职, 分管供销社)."
    },
    {
        "id": 11,
        "name": "王雪冰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共城固县委员会",
        "source": "接访公告 2026-07-23 (分管公安局/法院/检察院/司法)."
    },
    {
        "id": 12,
        "name": "胡传明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部长",
        "current_org": "中共城固县委员会",
        "source": "接访公告 2026-07-31 (分管编办/老干局/党史研究室/考核办/公务员局). 亦见城固县委组织部相关活动."
    },
    # ═══════ 县人大 / 法检 / 监委 ═══════
    {
        "id": 13,
        "name": "肖万朋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "城固县人民代表大会常务委员会",
        "source": "县十九届人大常委会第三十二次会议 2026-08-04 主持."
    },
    {
        "id": 14,
        "name": "靳侠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "城固县人民代表大会常务委员会",
        "source": "接访公告 2026-07-20; 人大常委会 2026-08-04."
    },
    {
        "id": 15,
        "name": "孙刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "城固县人民代表大会常务委员会",
        "source": "人大常委会第三十二次会议 2026-08-04."
    },
    {
        "id": 16,
        "name": "张天元",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "城固县人民代表大会常务委员会",
        "source": "接访公告 2026-07-24; 人大常委会 2026-08-04."
    },
    {
        "id": 17,
        "name": "张春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "城固县人民代表大会常务委员会",
        "source": "接访公告 2026-07-29; 人大常委会 2026-08-04."
    },
    {
        "id": 18,
        "name": "余家武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人民法院院长",
        "current_org": "城固县人民法院",
        "source": "县人大常委会第三十二次会议 2026-08-04 列席."
    },
    {
        "id": 19,
        "name": "俞健",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人民检察院检察长",
        "current_org": "城固县人民检察院",
        "source": "县人大常委会第三十二次会议 2026-08-04 列席."
    },
    {
        "id": 20,
        "name": "王伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县监委代主任",
        "current_org": "中共城固县纪律检查委员会",
        "source": "县人大常委会第三十二次会议 2026-08-04 决定任命副主任并决定代理主任."
    },
    {
        "id": 21,
        "name": "黄锐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县纪委书记、监委主任",
        "current_org": "中共城固县纪律检查委员会",
        "source": "城固县纪委监委述责述廉会 2026-01-30 (chenggu.qinfeng.gov.cn)."
    },
    # ═══════ 前任 & 上级网络 ═══════
    {
        "id": 22,
        "name": "王健梅 (前任县委书记)",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979-06",
        "birthplace": "",
        "education": "研究生(工程硕士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记 (去向待查)",
        "current_org": "中共城固县委员会",
        "source": "2025-01 官方披露任城固县委书记(兼县长/航开区主任); 2024-12 陕西省委组织部拟进一步使用公示. 2026-07 后卸任，去向未公开确认."
    },
    {
        "id": 23,
        "name": "汉中市委书记 张烨 (context)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉中市委书记 (context)",
        "current_org": "中共汉中市委",
        "source": "汉中市政府网 2026-08-07 会见新闻."
    },
]


# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {
        "id": ORG_OFFSET + 1,
        "name": "中共城固县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共汉中市委",
        "location": "陕西省汉中市城固县"
    },
    {
        "id": ORG_OFFSET + 2,
        "name": "城固县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "汉中市人民政府",
        "location": "陕西省汉中市城固县"
    },
    {
        "id": ORG_OFFSET + 3,
        "name": "中共城固县纪律检查委员会",
        "type": "纪律检查",
        "level": "县级",
        "parent": "中共汉中市纪律检查委员会",
        "location": "陕西省汉中市城固县"
    },
    {
        "id": ORG_OFFSET + 4,
        "name": "城固县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "陕西省人民代表大会常务委员会",
        "location": "陕西省汉中市城固县"
    },
    {
        "id": ORG_OFFSET + 5,
        "name": "城固县人民法院",
        "type": "政府",
        "level": "县级",
        "parent": "汉中市中级人民法院",
        "location": "陕西省汉中市城固县"
    },
    {
        "id": ORG_OFFSET + 6,
        "name": "城固县人民检察院",
        "type": "政府",
        "level": "县级",
        "parent": "汉中市人民检察院",
        "location": "陕西省汉中市城固县"
    },
    {
        "id": ORG_OFFSET + 7,
        "name": "城固县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "城固县人民政府",
        "location": "陕西省汉中市城固县"
    },
    {
        "id": ORG_OFFSET + 8,
        "name": "汉中航空技术开发区",
        "type": "开发区",
        "level": "地级",
        "parent": "汉中市人民政府",
        "location": "陕西省汉中市城固县"
    },
    {
        "id": ORG_OFFSET + 9,
        "name": "汉中市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "陕西省人民政府",
        "location": "陕西省汉中市"
    },
    {
        "id": ORG_OFFSET + 10,
        "name": "中共汉中市委",
        "type": "党委",
        "level": "地级市",
        "parent": "中共陕西省委",
        "location": "陕西省汉中市"
    },
]


# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 王钧平 (书记)
    {"person_id": 1, "org_id": ORG_OFFSET + 1, "title": "县委书记", "start": "2026-08", "end": "present", "rank": "正处级", "note": "2026-07-24 任前公示拟进一步使用; 2026-08 正式任书记; 兼汉中航空技术开发区管委会主任"},
    {"person_id": 1, "org_id": ORG_OFFSET + 8, "title": "汉中航空技术开发区管委会主任(兼)", "start": "2025", "end": "present", "rank": "正处级", "note": "兼"}, 
    {"person_id": 1, "org_id": ORG_OFFSET + 2, "title": "县委副书记、县长 (前任)", "start": "2025-03", "end": "2026-07", "rank": "正处级", "note": "接访公告 2026-07-29 仍列县长"},
    # 李鹏程 (代县长)
    {"person_id": 2, "org_id": ORG_OFFSET + 2, "title": "副县长、代县长", "start": "2026-08-04", "end": "present", "rank": "正处级", "note": "县人大常委会第三十二次会议决定任命副县长并代理县长; 县政府党组书记"},
    {"person_id": 2, "org_id": ORG_OFFSET + 1, "title": "县委副书记", "start": "2026-08", "end": "present", "rank": "正处级", "note": ""},
    # 政府班子
    {"person_id": 3, "org_id": ORG_OFFSET + 2, "title": "县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "党组副书记"},
    {"person_id": 4, "org_id": ORG_OFFSET + 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副处级", "note": "分管住建/生态/城管/文旅/城投/棚改"},
    {"person_id": 5, "org_id": ORG_OFFSET + 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副处级", "note": "分管苏陕协作/科技"},
    {"person_id": 6, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "民盟"},
    {"person_id": 7, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "农业/水利/林业/交通"},
    {"person_id": 8, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": ORG_OFFSET + 2, "title": "副县长、公安局长", "start": "", "end": "present", "rank": "副处级", "note": "公安/司法/信访/退役军人"},
    {"person_id": 9, "org_id": ORG_OFFSET + 7, "title": "县公安局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": ORG_OFFSET + 2, "title": "县政府党组成员", "start": "", "end": "present", "rank": "副处级", "note": "省工信厅定点帮扶挂职"},
    # 县委
    {"person_id": 11, "org_id": ORG_OFFSET + 1, "title": "县委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": "分管公安/法检/司法"},
    {"person_id": 12, "org_id": ORG_OFFSET + 1, "title": "县委常委、组织部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 人大 / 法检 / 监委
    {"person_id": 13, "org_id": ORG_OFFSET + 4, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": ORG_OFFSET + 4, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": ORG_OFFSET + 4, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": ORG_OFFSET + 4, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": ORG_OFFSET + 4, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": ORG_OFFSET + 5, "title": "县人民法院院长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": ORG_OFFSET + 6, "title": "县人民检察院检察长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": ORG_OFFSET + 3, "title": "县监委代主任", "start": "2026-08-04", "end": "present", "rank": "副处级", "note": "决定代理"},
    {"person_id": 21, "org_id": ORG_OFFSET + 3, "title": "县纪委书记、监委主任", "start": "", "end": "2026-08", "rank": "副处级", "note": "2026-08 王伟代其位(待确认)"},
    # 前任 / 上级
    {"person_id": 22, "org_id": ORG_OFFSET + 1, "title": "县委书记 (前任)", "start": "2025-01", "end": "2026-07", "rank": "正处级", "note": "去向待查"},
    {"person_id": 22, "org_id": ORG_OFFSET + 2, "title": "县长 (更前任)", "start": "2021-08", "end": "2025-03", "rank": "正处级", "note": ""},
    {"person_id": 23, "org_id": ORG_OFFSET + 10, "title": "汉中市委书记", "start": "", "end": "present", "rank": "正厅级", "note": "上级网络 context"},
]


# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档 (书记—代县长)
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记王钧平 与 代县长李鹏程 现党政搭档 (2026-08 换届后)",
        "overlap_org": "城固县",
        "overlap_period": "2026-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 书记—县长 传承 (王钧平 由县长升书记, 李鹏程接任县长)
    {
        "person_a": 1, "person_b": 2,
        "type": "predecessor_successor",
        "context": "王钧平由城固县长升任书记(2026-08); 李鹏 程接任代县长 — 班子交接",
        "overlap_org": "城固县人民政府",
        "overlap_period": "2026",
        "strength": "strong",
        "confidence": "plausible"
    },
    # 前任书记 王健梅 → 王钧平 (书记接班)
    {
        "person_a": 22, "person_b": 1,
        "type": "predecessor_successor",
        "context": "王健梅卸任城固县委书记(2026-07)后王钧平接任(2026-08)",
        "overlap_org": "中共城固县委员会",
        "overlap_period": "2026",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 王健梅 与 王钧平 (县长先后任)
    {
        "person_a": 22, "person_b": 1,
        "type": "predecessor_successor",
        "context": "王健梅曾任城固县长, 后王钧平接任县长并升书记",
        "overlap_org": "城固县人民政府",
        "overlap_period": "2025",
        "strength": "medium",
        "confidence": "plausible"
    },
    # 书记与常务副县长
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记王钧平 与 常务副县长杨奇涛",
        "overlap_org": "城固县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 代县长 与 常务副县长
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "代县长李鹏程 与 常务副县长杨奇涛 共事(政府班子)",
        "overlap_org": "城固县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 县与政法委/组织部
    {
        "person_a": 1, "person_b": 11,
        "type": "superior_subordinate",
        "context": "书记 与 政法委书记王雪冰",
        "overlap_org": "中共城固县委员会",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 12,
        "type": "superior_subordinate",
        "context": "书记 与 组织部长胡传明",
        "overlap_org": "中共城固县委员会",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 李鹏程 与 南郑 (跨县网络线索)
    {
        "person_a": 2, "person_b": 23,
        "type": "overlap",
        "context": "李鹏程由南郑区调入城固任代县长; 隶属汉中市委领导",
        "overlap_org": "汉中市",
        "overlap_period": "2026",
        "strength": "weak",
        "confidence": "plausible"
    },
    # 公安线
    {
        "person_a": 9, "person_b": 1,
        "type": "superior_subordinate",
        "context": "公安局长李秀虎 隶属县委县政府领导",
        "overlap_org": "城固县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 法检两长 / 监委 — 党委纪律链
    {
        "person_a": 18, "person_b": 11,
        "type": "overlap",
        "context": "法院院长余家武 与 政法委书记 (政法口)",
        "overlap_org": "城固县",
        "overlap_period": "2026-",
        "strength": "weak",
        "confidence": "plausible"
    },
    {
        "person_a": 19, "person_b": 11,
        "type": "overlap",
        "context": "检察长俞健 与 政法委书记 (政法口)",
        "overlap_org": "城固县",
        "overlap_period": "2026-",
        "strength": "weak",
        "confidence": "plausible"
    },
    {
        "person_a": 21, "person_b": 1,
        "type": "superior_subordinate",
        "context": "纪委书记/监委主任 黄锐 隶属县委领导",
        "overlap_org": "中共城固县委员会",
        "overlap_period": "2025-2026",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 人大主任
    {
        "person_a": 13, "person_b": 1,
        "type": "superior_subordinate",
        "context": "县人大主任肖万朋 与 县委书记 搭档",
        "overlap_org": "城固县",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
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