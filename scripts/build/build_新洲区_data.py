#!/usr/bin/env python3
"""Build script for 武汉市新洲区 (Xinzhou District, Wuhan, Hubei) cadre leadership network.

Task: hubei_新洲区 — targets 区委书记 & 区长 (市辖区).
As-of date: 2026-08-06.

Primary source (one-to-one, official):
- 新洲区人民政府门户 https://www.whxinzhou.gov.cn/ — 政务要闻 2026-07/08:
  - "全区上半年经济形势分析会举行" (2026-08-03) → 区委书记朱功伟主持会议，区委副书记、区长李先勇总结，区人大常委会主任易金莲、区政协主席高潮出席
  - 多篇"区委书记朱功伟专题调研/调研督导/走访" (2026-07-24/26/28/31)
  - "区领导走访慰问驻区部队官兵和退役军人" (2026-08-01) → 区长李先勇一行
  - "8月份新洲区领导干部接待群众来访日程安排表" (2026-07-30) → 确认全部区委常委/区政府/区人大/区政协/法检班子名单

CONFIDENCE NOTES
- 朱功伟 = 现任新洲区委书记 (confirmed: 多篇官方政务要闻明确"区委书记朱功伟")
- 李先勇 = 现任新洲区委副书记、区长 (confirmed: 官方"区长李先勇总结上半年经济工作/一行走访")
- 区委常委/区政府/人大/政协/法检班子 = confirmed by 官方接访日程 (2026-08)
- 完整履历(出生地/籍贯/出生年月/毕业院校/入党参工时间/前任职) = OPEN GAP (外部搜索不可用)
- 前区委书记、前任区长去向 = OPEN GAP (未核实)
"""

import sqlite3
import sys
from pathlib import Path

# Locate repo root (holds gov_relation/) robustly across staging/scripts/build/root locations.
_root = Path(__file__).resolve()
while not (_root / "gov_relation").is_dir() and _root != _root.parent:
    _root = _root.parent
sys.path.insert(0, str(_root))

from gov_relation.runner import run_build

AS_OF = "2026-08-06"
SLUG = "新洲区"

TMP = Path(__file__).resolve().parent
DB_PATH = TMP / "新洲区_network.db"
GEXF_PATH = TMP / "新洲区_network.gexf"

OFFICIAL = "https://www.whxinzhou.gov.cn/"

persons = [
    # ── 现任核心领导 ──
    {
        "id": 1,
        "name": "朱功伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新洲区委书记",
        "current_org": "中共武汉市新洲区委员会",
        "source": OFFICIAL,
    },
    {
        "id": 2,
        "name": "李先勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新洲区委副书记、区长",
        "current_org": "新洲区人民政府",
        "source": OFFICIAL,
    },
    # ── 区委常委 ──
    {
        "id": 3,
        "name": "杨红喜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "新洲区人民政府",
        "source": OFFICIAL,
    },
    {
        "id": 4,
        "name": "黄海军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共武汉市新洲区委员会组织部",
        "source": OFFICIAL,
    },
    {
        "id": 5,
        "name": "罗新坤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共武汉市新洲区委统战部",
        "source": OFFICIAL,
    },
    {
        "id": 6,
        "name": "邓辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、宣传部部长、区总工会主席",
        "current_org": "中共武汉市新洲区委宣传部",
        "source": OFFICIAL,
    },
    {
        "id": 7,
        "name": "汪刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区委办公室主任",
        "current_org": "中共武汉市新洲区委办公室",
        "source": OFFICIAL,
    },
    {
        "id": 8,
        "name": "杨泽敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "新洲区人民政府",
        "source": OFFICIAL,
    },
    {
        "id": 9,
        "name": "张惊波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区人武部政委",
        "current_org": "新洲区人民武装部",
        "source": OFFICIAL,
    },
    # ── 区政府副区长 (非常委) ──
    {
        "id": 10,
        "name": "丁力",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新洲区人民政府副区长",
        "current_org": "新洲区人民政府",
        "source": OFFICIAL,
    },
    {
        "id": 11,
        "name": "肖新锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新洲区人民政府副区长",
        "current_org": "新洲区人民政府",
        "source": OFFICIAL,
    },
    {
        "id": 12,
        "name": "夏昌作",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长、区委政法委副书记、区公安分局局长",
        "current_org": "新洲区人民政府/新洲区公安分局",
        "source": OFFICIAL,
    },
    # ── 人大/政协 ──
    {
        "id": 13,
        "name": "易金莲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "新洲区人民代表大会常务委员会",
        "source": OFFICIAL,
    },
    {
        "id": 14,
        "name": "吕秀平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "新洲区人民代表大会常务委员会",
        "source": OFFICIAL,
    },
    {
        "id": 15,
        "name": "万鹰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "新洲区人民代表大会常务委员会",
        "source": OFFICIAL,
    },
    {
        "id": 16,
        "name": "张水泉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "新洲区人民代表大会常务委员会",
        "source": OFFICIAL,
    },
    {
        "id": 17,
        "name": "陶建权",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "新洲区人民代表大会常务委员会",
        "source": OFFICIAL,
    },
    {
        "id": 18,
        "name": "陶磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "新洲区人民代表大会常务委员会",
        "source": OFFICIAL,
    },
    {
        "id": 19,
        "name": "高潮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议武汉市新洲区委员会",
        "source": OFFICIAL,
    },
    {
        "id": 20,
        "name": "陶宏伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "新洲区政协",
        "source": OFFICIAL,
    },
    {
        "id": 21,
        "name": "陈红英",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "新洲区政协",
        "source": OFFICIAL,
    },
    {
        "id": 22,
        "name": "王志芳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "新洲区政协",
        "source": OFFICIAL,
    },
    {
        "id": 23,
        "name": "张爱平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "新洲区政协",
        "source": OFFICIAL,
    },
    # ── 法检 ──
    {
        "id": 24,
        "name": "曾琳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区法院院长",
        "current_org": "新洲区人民法院",
        "source": OFFICIAL,
    },
    {
        "id": 25,
        "name": "张琦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区检察院代理检察长",
        "current_org": "新洲区人民检察院",
        "source": OFFICIAL,
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共武汉市新洲区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中国共产党武汉市委员会",
        "location": "武汉市新洲区",
    },
    {
        "id": 2,
        "name": "新洲区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "武汉市人民政府",
        "location": "武汉市新洲区",
    },
    {
        "id": 3,
        "name": "新洲区人民代表大会常务委员会",
        "type": "人大",
        "level": "市辖区",
        "parent": "武汉市新洲区委员会",
        "location": "武汉市新洲区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议武汉市新洲区委员会",
        "type": "群团",
        "level": "市辖区",
        "parent": "武汉市新洲区委员会",
        "location": "武汉市新洲区",
    },
    {
        "id": 5,
        "name": "新洲区人民法院",
        "type": "other",
        "level": "市辖区",
        "parent": "武汉市中级人民法院",
        "location": "武汉市新洲区",
    },
    {
        "id": 6,
        "name": "新洲区人民检察院",
        "type": "other",
        "level": "市辖区",
        "parent": "武汉市人民检察院",
        "location": "武汉市新洲区",
    },
    {
        "id": 7,
        "name": "中共武汉市新洲区委员会组织部",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共武汉市新洲区委员会",
        "location": "武汉市新洲区",
    },
    {
        "id": 8,
        "name": "中共武汉市新洲区委宣传部",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共武汉市新洲区委员会",
        "location": "武汉市新洲区",
    },
    {
        "id": 9,
        "name": "中共武汉市新洲区委统战部",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共武汉市新洲区委员会",
        "location": "武汉市新洲区",
    },
    {
        "id": 10,
        "name": "中共武汉市新洲区委办公室",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共武汉市新洲区委员会",
        "location": "武汉市新洲区",
    },
    {
        "id": 11,
        "name": "新洲区人民武装部",
        "type": "其他",
        "level": "市辖区",
        "parent": "中共武汉市新洲区委员会",
        "location": "武汉市新洲区",
    },
    {
        "id": 12,
        "name": "新洲区公安分局",
        "type": "政府",
        "level": "市辖区",
        "parent": "新洲区人民政府",
        "location": "武汉市新洲区",
    },
]

positions = [
    # 现任核心
    {"person_id": 1, "org_id": 1, "title": "新洲区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "现任区委书记（official 2026-07/08）"},
    {"person_id": 2, "org_id": 2, "title": "新洲区区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "现任区委副书记、区长（official 2026-08）"},
    {"person_id": 2, "org_id": 1, "title": "新洲区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "区委副书记"},
    # 区委常委
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    {"person_id": 4, "org_id": 7, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    {"person_id": 5, "org_id": 9, "title": "统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    {"person_id": 6, "org_id": 8, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委、区总工会主席"},
    {"person_id": 7, "org_id": 10, "title": "区委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委，分管农业农村现代化、乡村振兴"},
    {"person_id": 9, "org_id": 11, "title": "区人武部政委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    # 政府副职
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管财政/金融/市场监管"},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "自然资源和城乡建设、开发区"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "公安/司法/信访"},
    {"person_id": 12, "org_id": 12, "title": "区公安分局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委政法委副书记"},
    # 人大
    {"person_id": 13, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 政协
    {"person_id": 19, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 法检
    {"person_id": 24, "org_id": 5, "title": "区法院院长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 6, "title": "区检察院代理检察长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

relationships = [
    # 现任党政一把手搭档 (强关系)
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "朱功伟（区委书记）与李先勇（区委副书记、区长）组成现任新洲区党政一把手搭档，2026-07/08 共同主持全区工作",
     "overlap_org": "中共新洲区委员会/新洲区人民政府", "overlap_period": "2026至今", "confidence": "confirmed"},
    # 区委书记 vs 各副职 (领导班子上级下级)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记朱功伟领导班子，杨红喜为常务副区长（区委常委）", "overlap_org": "中共新洲区委员会", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记领导组织部长", "overlap_org": "中共新洲区委员会", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "区委书记领导宣传部长", "overlap_org": "中共新洲区委员会", "overlap_period": "2026", "confidence": "confirmed"},
    # 区长 vs 副区长（政府内部上下级）
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "区长领导常务副区长（区政府党组内部）", "overlap_org": "新洲区人民政府", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长领导副区长杨泽敏（分管农业农村）", "overlap_org": "新洲区人民政府", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "区长领导副区长丁力", "overlap_org": "新洲区人民政府", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "区长领导副区长肖新锋", "overlap_org": "新洲区人民政府", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "区长领导副区长/公安局长夏昌作", "overlap_org": "新洲区人民政府", "overlap_period": "2026", "confidence": "confirmed"},
    # 区委与人大/政协关系
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate",
     "context": "区委书记与区人大常委会主任工作关系（党代会/人大班子）", "overlap_org": "中共新洲区委员会", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 19, "type": "superior_subordinate",
     "context": "区委书记与区政协主席工作关系", "overlap_org": "中共新洲区委员会", "overlap_period": "2026", "confidence": "confirmed"},
]

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
    conn = sqlite3.connect(str(DB_PATH))
    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("persons", "organizations", "positions", "relationships")}
    conn.close()
    print(f"Built {DB_PATH} and {GEXF_PATH}")
    print(f"persons={len(persons)} orgs={len(organizations)} positions={len(positions)} relationships={len(relationships)}")
    print("DB counts:", counts)