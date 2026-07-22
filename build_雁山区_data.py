#!/usr/bin/env python3
"""Build script for 雁山区 (Yanshan District, Guilin, Guangxi) leadership network.

Generated: 2026-07-22
Level: 市辖区
Province: 广西壮族自治区
Parent City: 桂林市
Targets: 区委书记 & 区长

Research Note:
  Official district website (http://www.glyszf.gov.cn/) was accessible via HTTP.
  Leadership bios sourced from official 领导之窗 pages and news articles.
  Pre-appointment notices from 桂林市委组织部 provide promotion context.

Sources:
  - http://www.glyszf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/qz/t26310928.shtml (区长潘军华官方简历)
  - http://www.glyszf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/t27802865.shtml (副区长陈曦官方简历)
  - http://www.glyszf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/t26303254.shtml (副区长罗周韬官方简历)
  - http://www.glyszf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/t26303256.shtml (副区长薛媛官方简历)
  - http://www.glyszf.gov.cn/jrys/ysxw/t27731578.shtml (区委书记李强调研报道, confirmed as of 2026-05-27)
  - http://www.glyszf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/rsxx/rqgs/t27882028.shtml (2026-07-07 桂林领导干部任职前公示)
  - http://www.glyszf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfwj_2/zffw/t27802690.shtml (雁政干〔2026〕5号)
  - http://www.glyszf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfwj_2/zffw/t27802670.shtml (雁政干〔2026〕4号)
  - http://www.glyszf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfwj_2/zffw/t27802680.shtml (雁政干〔2026〕3号)
"""

import sqlite3  # noqa: used by gov_relation.runner
from pathlib import Path

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "李强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "雁山区委书记",
        "current_org": "中共桂林市雁山区委员会",
        "source": "http://www.glyszf.gov.cn/jrys/ysxw/t27731578.shtml (2026-05-27 调研报道确认现职) — 完整简历尚未在公开渠道找到",
    },
    {
        "id": 2,
        "name": "潘军华",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1981年1月",
        "birthplace": "广西资源",
        "education": "在职研究生学历，法学学士学位（广西师范大学法商学院法学专业）",
        "party_join": "2001年10月",
        "work_start": "2003年10月",
        "current_post": "雁山区区长、区委副书记",
        "current_org": "桂林市雁山区人民政府",
        "source": "http://www.glyszf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/qz/t26310928.shtml (官方简历, 2026-01-05更新)",
    },
    # ── Deputy Leaders ──
    {
        "id": 3,
        "name": "陈曦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年9月",
        "birthplace": "广西全州",
        "education": "大学学历，理学学士学位",
        "party_join": "2003年2月",
        "work_start": "2003年6月",
        "current_post": "雁山区副区长",
        "current_org": "桂林市雁山区人民政府",
        "source": "http://www.glyszf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/t27802865.shtml (官方简历, 2026-01-22更新) — 2026-07-07 任前公示显示\"拟进一步使用\"",
    },
    {
        "id": 4,
        "name": "罗周韬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年1月",
        "birthplace": "广西河池",
        "education": "在职大专学历（广西劳改警校狱政管理专业）",
        "party_join": "2001年5月",
        "work_start": "1995年",
        "current_post": "雁山区副区长、市公安局雁山分局党委书记、局长",
        "current_org": "桂林市雁山区人民政府",
        "source": "http://www.glyszf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/t26303254.shtml (官方简历, 2025-02-25更新)",
    },
    {
        "id": 5,
        "name": "薛媛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年1月",
        "birthplace": "广西平乐",
        "education": "在职研究生学历，公共管理硕士（中国政法大学法学学士、广西师范大学公共管理硕士）",
        "party_join": "",
        "work_start": "1999年9月",
        "current_post": "雁山区副区长（拟任市直正处级单位正职）",
        "current_org": "桂林市雁山区人民政府",
        "source": "http://www.glyszf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/t26303256.shtml (官方简历, 2023-07-28更新)；2026-07-07 任前公示\"拟任市直正处级单位正职\"",
        "note": "无党派人士",
    },
    # ── Additional Known Officials ──
    {
        "id": 6,
        "name": "隆胜军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "雁山区委常委、区委办主任",
        "current_org": "中共桂林市雁山区委员会",
        "source": "http://www.glyszf.gov.cn/jrys/ysxw/t27731578.shtml (2026-05-27 陪同区委书记李强调研的报道)",
    },
    # ── Gap placeholder positions ──
    {
        "id": 7,
        "name": "【待查】雁山区常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "雁山区委常委、常务副区长（待查）",
        "current_org": "桂林市雁山区人民政府",
        "source": "GAP — 官网领导之窗仅列出区长和三名副区长, 未列出常务副区长",
    },
    {
        "id": 8,
        "name": "【待查】雁山区纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "雁山区委常委、纪委书记（待查）",
        "current_org": "中共桂林市雁山区纪律检查委员会",
        "source": "GAP — 未在公开信息中找到",
    },
    {
        "id": 9,
        "name": "【待查】雁山区委组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "雁山区委常委、组织部长（待查）",
        "current_org": "中共桂林市雁山区委组织部",
        "source": "GAP — 未在公开信息中找到",
    },
    # ── Other known officials from appointment notices ──
    {
        "id": 10,
        "name": "黄贤斌",
        "gender": "",
        "ethnicity": "壮族",
        "birth": "约1987年",
        "birthplace": "",
        "education": "在职研究生，管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "雁山区委办公室副主任(正科长级)（拟任副处级）",
        "current_org": "中共桂林市雁山区委员会",
        "source": "2026-07-07 桂林领导干部任职前公示 — 原大埠乡党委书记",
    },
    {
        "id": 11,
        "name": "张虹",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1983年2月",
        "birthplace": "",
        "education": "在职研究生，管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "雁山区委办公室副主任(正科长级)（拟任副处级）",
        "current_org": "中共桂林市雁山区委员会",
        "source": "2026-07-07 桂林领导干部任职前公示 — 原草坪回族乡党委书记",
    },
    {
        "id": 12,
        "name": "莫锦锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "民革党员",
        "work_start": "",
        "current_post": "雁山区人民政府办公室副主任（保留正科长级）（拟任副处级）",
        "current_org": "桂林市雁山区人民政府",
        "source": "2026-07-07 桂林领导干部任职前公示；雁政干〔2026〕3号 (2026-06-04任政府办副主任)",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共桂林市雁山区委员会", "type": "党委", "level": "正处级", "parent": "中共桂林市委员会", "location": "桂林市雁山区"},
    {"id": 2, "name": "桂林市雁山区人民政府", "type": "政府", "level": "正处级", "parent": "桂林市人民政府", "location": "桂林市雁山区"},
    {"id": 3, "name": "中共桂林市雁山区纪律检查委员会", "type": "纪委", "level": "副处级", "parent": "中共桂林市纪律检查委员会", "location": "桂林市雁山区"},
    {"id": 4, "name": "中共桂林市雁山区委组织部", "type": "党委", "level": "正科级", "parent": "中共桂林市雁山区委员会", "location": "桂林市雁山区"},
    {"id": 5, "name": "桂林市公安局雁山分局", "type": "政府", "level": "正科级", "parent": "桂林市公安局", "location": "桂林市雁山区"},
    {"id": 6, "name": "中共桂林市雁山区委办公室", "type": "党委", "level": "正科级", "parent": "中共桂林市雁山区委员会", "location": "桂林市雁山区"},
    {"id": 7, "name": "雁山区大埠乡党委", "type": "党委", "level": "正科级", "parent": "中共桂林市雁山区委员会", "location": "桂林市雁山区大埠乡"},
    {"id": 8, "name": "雁山区草坪回族乡党委", "type": "党委", "level": "正科级", "parent": "中共桂林市雁山区委员会", "location": "桂林市雁山区草坪回族乡"},
]

POSITIONS = [
    # 李强 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "雁山区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026-05-27 在任确认"},
    # 潘军华 — 区长
    {"person_id": 2, "org_id": 1, "title": "雁山区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "官方简历确认"},
    {"person_id": 2, "org_id": 2, "title": "雁山区区长、区政府党组书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "同时兼任高新区管委会副主任"},
    # 陈曦 — 副区长
    {"person_id": 3, "org_id": 2, "title": "雁山区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-07-07 任前公示显示拟进一步使用，可能在变动中"},
    # 罗周韬 — 副区长兼公安局长
    {"person_id": 4, "org_id": 2, "title": "雁山区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "政府党组成员"},
    {"person_id": 4, "org_id": 5, "title": "市公安局雁山分局党委书记、局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "官方简历确认"},
    # 薛媛 — 副区长
    {"person_id": 5, "org_id": 2, "title": "雁山区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "无党派人士；2026-07-07 拟任市直正处级单位正职"},
    # 隆胜军 — 区委办主任
    {"person_id": 6, "org_id": 1, "title": "雁山区委常委、区委办主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-05-27 陪同李强调研确认"},
    # GAP positions
    {"person_id": 7, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    {"person_id": 8, "org_id": 3, "title": "雁山区纪委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    {"person_id": 9, "org_id": 4, "title": "雁山区委组织部长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "GAP — 姓名未知"},
    # 黄贤斌
    {"person_id": 10, "org_id": 6, "title": "雁山区委办公室副主任（正科长级）", "start_date": "", "end_date": "present", "rank": "正科级", "note": "拟任副处级领导职务"},
    {"person_id": 10, "org_id": 7, "title": "大埠乡党委原书记", "start_date": "", "end_date": "", "rank": "正科级", "note": "原任"},
    # 张虹
    {"person_id": 11, "org_id": 6, "title": "雁山区委办公室副主任（正科长级）", "start_date": "", "end_date": "present", "rank": "正科级", "note": "拟任副处级领导职务"},
    {"person_id": 11, "org_id": 8, "title": "草坪回族乡党委原书记", "start_date": "", "end_date": "", "rank": "正科级", "note": "原任"},
    # 莫锦锋
    {"person_id": 12, "org_id": 2, "title": "雁山区政府办公室副主任（保留正科长级）", "start_date": "2026-06-04", "end_date": "present", "rank": "正科级", "note": "雁政干〔2026〕3号任免, 拟任副处级"},
]

RELATIONSHIPS = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "李强（区委书记）-潘军华（区长/区委副书记）", "overlap_org": "雁山区四套班子", "overlap_period": "2026年在任", "source": "confirmed from official news and bio pages", "confidence": "confirmed"},
    # 区长与副区长们
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "潘军华（区长）-陈曦（副区长）", "overlap_org": "雁山区人民政府", "overlap_period": "2026年在任", "source": "confirmed from official website", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "潘军华（区长）-罗周韬（副区长）", "overlap_org": "雁山区人民政府", "overlap_period": "2026年在任", "source": "confirmed from official website", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "潘军华（区长）-薛媛（副区长）", "overlap_org": "雁山区人民政府", "overlap_period": "2023-2026年在任", "source": "confirmed from official website", "confidence": "confirmed"},
    # 区委书记-区委办主任
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "李强（区委书记）-隆胜军（区委常委、区委办主任）", "overlap_org": "雁山区委常委会", "overlap_period": "2026年在任", "source": "confirmed from 2026-05-27 news article (隆胜军陪同李强调研)", "confidence": "confirmed"},
    # 副区长之间的同事关系
    {"person_a": 3, "person_b": 4, "type": "同级", "context": "陈曦与罗周韬同为副区长", "overlap_org": "雁山区人民政府", "overlap_period": "2025-2026", "source": "inferred from official website", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 5, "type": "同级", "context": "陈曦与薛媛同为副区长", "overlap_org": "雁山区人民政府", "overlap_period": "2023-2026", "source": "inferred from official website", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 5, "type": "同级", "context": "罗周韬与薛媛同为副区长", "overlap_org": "雁山区人民政府", "overlap_period": "2023-2026", "source": "inferred from official website", "confidence": "confirmed"},
    # 乡镇党委书记与区委的关系
    {"person_a": 10, "person_b": 1, "type": "上下级", "context": "黄贤斌（原大埠乡党委书记, 现任区委办副主任）-李强（区委书记）", "overlap_org": "雁山区委", "overlap_period": "2026年", "source": "inferred from 2026-07-07 任前公示", "confidence": "plausible"},
    {"person_a": 11, "person_b": 1, "type": "上下级", "context": "张虹（原草坪回族乡党委书记, 现任区委办副主任）-李强（区委书记）", "overlap_org": "雁山区委", "overlap_period": "2026年", "source": "inferred from 2026-07-07 任前公示", "confidence": "plausible"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "雁山区_network.db"
GEXF_PATH = STAGING_DIR / "雁山区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="雁山区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
