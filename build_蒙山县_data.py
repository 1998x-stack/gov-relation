#!/usr/bin/env python3
"""Build script for 蒙山县 (Mengshan County, Wuzhou, Guangxi) leadership network.

Generated: 2026-07-23
Level: 县
Province: 广西壮族自治区
Parent City: 梧州市
Targets: 县委书记 & 县长

Research Notes:
  Current County Party Secretary: 陈坚 (promoted from county mayor in 2025)
  Current Acting County Mayor: 邱振宇 (appointed 2025-09)
  Previous County Party Secretary: 张银岳 (served ~2021-2025, now 梧州市自然资源局党组书记)

  Confirmed facts:
  - 陈坚: b.1973-11, 广西岑溪人, 广西区委党校研究生. Long career in Wuzhou municipal
    government (副秘书长, 安监局, 投促局, 退役军人事务局) before becoming 蒙山县县长 in 2021.
    Promoted to 县委书记 in 2025 per 2025-07 pre-appointment公示 and 2025-09巡视 feedback
    confirming his title.
  - 邱振宇: b.1982-10, 湖南浏阳人, 大学/管理学学士. Career in Wuzhou Party committee
    office (市委办第一秘书科科长, 市委分管日常工作的副秘书长) then 市自然资源局局长.
    Appointed acting county mayor 2025-09.
  - 张银岳: Served as 蒙山县县委书记 ~2021-2025. 2025-12 appointed 梧州市自然资源局局长.
    As of 2026-07 a noted as 梧州市自然资源局党组书记, 二级巡视员.

  County Government leadership (as of pre-2026):
  - 副县长: 黎威君, 韩格, 莫智懿, 甘家科(免公安局局长2026-01), 谭永辉, 梁洁铭, 梁文光/梁管文, 苏杨华
  - 王琦毅 appointed 副县长/公安局局长 2026-01-19 replacing 甘家科
  - 县委常委/政法委书记: 莫黎 (confirmed via 检察院2026-01 article)

  GAPS:
  - Most 县委常委 specific titles (纪委书记, 组织部长, 宣传部长, 统战部长) unknown
  - 黎威君, 韩格, 莫智懿, 谭永辉, 梁洁铭, 梁文光, 苏杨华 full biographies unknown
  - 县人大常委会主任, 政协主席 unknown
  - 邱振宇 early career details (2007-2015 timeline gaps)
  - Predecessor of 陈坚 as 县委书记 (张银岳) confirmed but exact handoff date unclear

Sources:
  - https://baike.baidu.com/item/%E9%99%88%E5%9D%9A/59373172 (陈坚 biography)
  - https://www.gxjjw.gov.cn (广西纪检监察网 — 巡视反馈 2025-09-05, 巡视动员 2025-04-18)
  - http://gxcounty.com （广西县域经济网 — 梧州市领导干部任职前公示 2025-07）
  - http://m.gxcounty.com/show-30-184053-0.html (邱振宇任代县长)
  - http://www.gxcounty.com/zhengwu/rsrm/184812.html (2026-01县人大常委会任免)
  - http://www.zgcounty.com/news/39478.html (蒙山县领导信息)
  - https://baike.baidu.com/item/%E8%92%99%E5%B1%B1%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C (蒙山县人民政府)
  - http://www.gxwzrd.gov.cn (梧州人大网 — 张银岳当选县委书记 2021)
  - http://www.gxcounty.com/zhengwu/rsrm/184662.html (2025-12梧州市人大常委会任免 — 张银岳任市自然资源局局长)
  - http://www.gxmsjcy.gov.cn (蒙山县检察院 — 2026-01-23 确认莫黎为县委常委/政法委书记)
  - http://www.esilk.net （金蚕网 — 梁洁铭副县长到访中国丝绸协会）
"""

import sqlite3  # noqa: used by gov_relation.runner

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
        "name": "陈坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年11月",
        "birthplace": "广西岑溪",
        "education": "广西区委党校研究生",
        "party_join": "1995年5月",
        "work_start": "1993年7月",
        "current_post": "蒙山县委书记",
        "current_org": "中共蒙山县委员会",
        "source": "https://baike.baidu.com/item/%E9%99%88%E5%9D%9A/59373172; http://gxcounty.com/zhengwu/rsrm/183755.html; https://www.gxjjw.gov.cn (2025-09-05巡视反馈确认陈坚为县委书记)",
    },
    {
        "id": 2,
        "name": "邱振宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "湖南浏阳",
        "education": "大学/管理学学士",
        "party_join": "",
        "work_start": "2007年7月",
        "current_post": "蒙山县委副书记、代县长",
        "current_org": "蒙山县人民政府",
        "source": "http://m.gxcounty.com/show-30-184053-0.html; http://gxcounty.com/zhengwu/rsrm/183755.html",
    },
    {
        "id": 3,
        "name": "张银岳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "梧州市自然资源局党组书记、二级巡视员（前蒙山县委书记）",
        "current_org": "梧州市自然资源局",
        "source": "https://baike.baidu.com/item/%E5%BC%A0%E9%93%B6%E5%B2%B3/17933767; http://gxcounty.com/zhengwu/rsrm/184662.html; https://dnr.gxzf.gov.cn (2026-07参加调研确认职务)",
    },
    # ── County Government Leaders ──
    {
        "id": 4,
        "name": "黎威君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蒙山县副县长",
        "current_org": "蒙山县人民政府",
        "source": "http://www.zgcounty.com/news/39478.html",
    },
    {
        "id": 5,
        "name": "韩格",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蒙山县副县长",
        "current_org": "蒙山县人民政府",
        "source": "http://www.zgcounty.com/news/39478.html",
    },
    {
        "id": 6,
        "name": "莫智懿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蒙山县副县长",
        "current_org": "蒙山县人民政府",
        "source": "https://baike.baidu.com/item/%E8%92%99%E5%B1%B1%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
    },
    {
        "id": 7,
        "name": "甘家科（已免）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原蒙山县副县长、公安局局长（2026-01免）",
        "current_org": "蒙山县人民政府",
        "source": "http://www.gxcounty.com/zhengwu/rsrm/184812.html; http://www.zgcounty.com/news/39478.html",
    },
    {
        "id": 8,
        "name": "谭永辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蒙山县副县长",
        "current_org": "蒙山县人民政府",
        "source": "https://baike.baidu.com/item/%E8%92%99%E5%B1%B1%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
    },
    {
        "id": 9,
        "name": "梁洁铭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蒙山县副县长",
        "current_org": "蒙山县人民政府",
        "source": "http://www.zgcounty.com/news/39478.html; http://www.esilk.net (茧丝绸产业调研)",
    },
    {
        "id": 10,
        "name": "梁文光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蒙山县副县长",
        "current_org": "蒙山县人民政府",
        "source": "https://baike.baidu.com/item/%E8%92%99%E5%B1%B1%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
    },
    {
        "id": 11,
        "name": "苏杨华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蒙山县副县长",
        "current_org": "蒙山县人民政府",
        "source": "https://baike.baidu.com/item/%E8%92%99%E5%B1%B1%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
    },
    {
        "id": 12,
        "name": "王琦毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蒙山县副县长、公安局局长",
        "current_org": "蒙山县公安局",
        "source": "http://www.gxcounty.com/zhengwu/rsrm/184812.html (2026-01-19任命)",
    },
    {
        "id": 13,
        "name": "莫黎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "蒙山县委常委、政法委书记",
        "current_org": "中共蒙山县委员会政法委员会",
        "source": "http://www.gxmsjcy.gov.cn (2026-01-23蒙山县检察院总结大会确认)",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共蒙山县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共梧州市委员会",
        "location": "蒙山县",
    },
    {
        "id": 2,
        "name": "蒙山县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "梧州市人民政府",
        "location": "蒙山县",
    },
    {
        "id": 3,
        "name": "蒙山县公安局",
        "type": "政府",
        "level": "县",
        "parent": "蒙山县人民政府",
        "location": "蒙山县",
    },
    {
        "id": 4,
        "name": "中共蒙山县委员会政法委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共蒙山县委员会",
        "location": "蒙山县",
    },
    {
        "id": 5,
        "name": "梧州市自然资源局",
        "type": "政府",
        "level": "市",
        "parent": "梧州市人民政府",
        "location": "梧州市",
    },
    {
        "id": 6,
        "name": "中共梧州市委员会",
        "type": "党委",
        "level": "市",
        "parent": "中共广西壮族自治区委员会",
        "location": "梧州市",
    },
    {
        "id": 7,
        "name": "梧州市人民政府",
        "type": "政府",
        "level": "市",
        "parent": "广西壮族自治区人民政府",
        "location": "梧州市",
    },
]

POSITIONS = [
    # 陈坚
    {"person_id": 1, "org_id": 1, "title": "蒙山县委书记", "start_date": "2025-07", "end_date": "present", "rank": "正处级", "note": "2025年7月任前公示拟任县（市、区）党委书记"},
    {"person_id": 1, "org_id": 2, "title": "蒙山县县长", "start_date": "2021-09", "end_date": "2025-07", "rank": "正处级", "note": "2021-09-09确认为县长；2025年7月公示后转任县委书记"},
    {"person_id": 1, "org_id": 6, "title": "中共梧州市委委员", "start_date": "", "end_date": "", "rank": "", "note": "第十四届梧州市委委员"},
    # 陈坚早期 — 岑溪梨木镇
    {"person_id": 1, "org_id": 0, "title": "岑溪市梨木镇党委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": "陈坚早期职务"},
    {"person_id": 1, "org_id": 7, "title": "梧州市人民政府副秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": "市政府办公室副主任、党组成员，兼应急办主任、调处办主任"},
    {"person_id": 1, "org_id": 7, "title": "梧州市安全生产监督管理局局长", "start_date": "2016-09", "end_date": "2019-03", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "梧州市投资促进局局长", "start_date": "2019-03", "end_date": "2020-04", "rank": "正处级", "note": "兼粤桂合作特别试验区党工委委员"},
    {"person_id": 1, "org_id": 7, "title": "梧州市退役军人事务局局长", "start_date": "2020-04", "end_date": "2021-09", "rank": "正处级", "note": "调任蒙山县前职务"},
    # 邱振宇
    {"person_id": 2, "org_id": 2, "title": "蒙山县委副书记、代县长", "start_date": "2025-09", "end_date": "present", "rank": "正处级", "note": "2025-07公示，2025-09县人大常委会任命为代县长"},
    {"person_id": 2, "org_id": 5, "title": "梧州市自然资源局局长", "start_date": "", "end_date": "2025-12", "rank": "正处级", "note": "2025-12-30梧州市人大常委会免去局长职务"},
    {"person_id": 2, "org_id": 6, "title": "梧州市委分管日常工作的副秘书长", "start_date": "", "end_date": "2025-09", "rank": "正处级", "note": "市委办公室副主任"},
    {"person_id": 2, "org_id": 6, "title": "梧州市委办公室第一秘书科科长", "start_date": "", "end_date": "", "rank": "正科级", "note": "早期职务"},
    # 张银岳
    {"person_id": 3, "org_id": 5, "title": "梧州市自然资源局党组书记、二级巡视员", "start_date": "2025-12", "end_date": "present", "rank": "副厅级（二级巡视员）", "note": "2025-12-30任命为市自然资源局局长"},
    {"person_id": 3, "org_id": 1, "title": "蒙山县委书记", "start_date": "2021-07", "end_date": "2025-07", "rank": "正处级", "note": "2021年7月蒙山县第十五次党代会当选"},
    {"person_id": 3, "org_id": 2, "title": "蒙山县县长", "start_date": "2020-07", "end_date": "2021-07", "rank": "正处级", "note": "2020-06县长候选人，2021-06蒙山县委主要负责人"},
    # 县政府班子
    {"person_id": 4, "org_id": 2, "title": "蒙山县副县长", "start_date": "2023-02-22", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "蒙山县副县长", "start_date": "2023-02-22", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "蒙山县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "蒙山县副县长", "start_date": "2023-02-22", "end_date": "2026-01-19", "rank": "副处级", "note": "兼任公安局局长；2026-01-19免去副县长和公安局局长职务"},
    {"person_id": 8, "org_id": 2, "title": "蒙山县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "蒙山县副县长", "start_date": "2023-02-22", "end_date": "present", "rank": "副处级", "note": "分管茧丝绸产业"},
    {"person_id": 10, "org_id": 2, "title": "蒙山县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "蒙山县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 3, "title": "蒙山县副县长、公安局局长", "start_date": "2026-01-19", "end_date": "present", "rank": "副处级", "note": "接替甘家科"},
    {"person_id": 13, "org_id": 4, "title": "蒙山县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

RELATIONSHIPS = [
    # 陈坚—邱振宇：前后任县长关系/主要领导共事
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "陈坚原为县长，2025年晋升为县委书记；邱振宇接任代县长", "overlap_org": "蒙山县人民政府", "overlap_period": "2025-09至今"},
    # 陈坚—张银岳：前后任县委书记
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "张银岳原为县委书记，调任市自然资源局后陈坚接任", "overlap_org": "中共蒙山县委员会", "overlap_period": "2025"},
    # 张银岳—陈坚：曾为书记—县长搭档
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "张银岳任县委书记时陈坚任县长，党政一把手共事约4年", "overlap_org": "中共蒙山县委员会 / 蒙山县人民政府", "overlap_period": "2021-2025"},
    # 邱振宇—张银岳：曾在梧州市级层面有交集
    {"person_a": 2, "person_b": 3, "type": "same_system", "context": "邱振宇任市自然资源局局长时张银岳接任该局局长", "overlap_org": "梧州市自然资源局", "overlap_period": "2025-12"},
]

# fmt: on

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

DB_PATH = DATABASE_DIR / "蒙山县_network.db"
GEXF_PATH = GRAPH_DIR / "蒙山县_network.gexf"


def main() -> None:
    run_build(
        slug="蒙山县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )


if __name__ == "__main__":
    main()
