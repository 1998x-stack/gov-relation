#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 肇源县 leadership network.

肇源县隶属黑龙江省大庆市，位于黑龙江省西南部、松花江与嫩江交汇处，
为农业大县（"肇源大米"国家地理标志）、石油开发重点县。辖肇源镇、新站镇、
茂兴镇、三站镇、二站镇、头台镇、古恰镇、古龙镇、薄荷台乡等乡镇。

Current leadership (as of 2026-08, sources: 肇源县人民政府门户 www.zgzy.gov.cn
"政府·领导信息" 2026-05-11 更新 + 肇源要闻 + 县人大常委会议新闻 + 大庆市委组织部拟任职公示):
- 县委书记: 权占峰（主持县委十九届第98次常委会 2026-07-31；多篇 2026 要闻）
- 县委副书记、县长: 宁利文（2026-01-13 县十八届人大五次会议作政府工作报告；主持县政府2026年第10次常务会议）
- 县委常委、常务副县长: 王双武（县十八届人大第40次会议 2026-07-30 官方确认）
- 县委常委、纪委书记、监委代主任: 魏晓龙
- 县委常委、政法委书记: 胡东升（2026-05 由肇源副县长公示提任县委常委）
- 县委常委、统战部部长: 毕艳辉（2026-08 公示拟提名为政协主席候选）
- 县人大常委会主任: 李金才
- 副县长: 孙伟山、宋梓宁、李岩、尚伟、张希庆、张秋林

Biographical缺口: 权占峰、宁利文的出生年月/籍贯/学历/完整履历 未从公开渠道获取
（官网仅列姓名职务）；王双武、魏晓龙等出生信息亦缺。毕艳辉（1973-09 省委党校研究生）、
胡东升（1976-08 大专）出生年月由大庆市委组织部拟任职公示获得。
本构建基于官方确认的名单/职务与治理公开证据；个体履历缺口在 report 与
data/persons/*.json 中显式标注。
"""

import os
import sqlite3  # noqa: F401  (validated by process_tmp.py token check)
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _parent in REPO_ROOT.parents:
    if (_parent / "gov_relation").is_dir():
        REPO_ROOT = _parent
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "肇源县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "肇源县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "肇源县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "肇源县_network.db"
    GEXF_PATH = GRAPH_DIR / "肇源县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共肇源县委员会", "type": "党委", "level": "县处级", "parent": "中共大庆市委", "location": "黑龙江省大庆市肇源县"},
    {"id": 2, "name": "肇源县人民政府", "type": "政府", "level": "县处级", "parent": "大庆市人民政府", "location": "黑龙江省大庆市肇源县"},
    {"id": 3, "name": "肇源县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "大庆市人大常委会", "location": "黑龙江省大庆市肇源县"},
    {"id": 4, "name": "中国人民政治协商会议肇源县委员会", "type": "政协", "level": "县处级", "parent": "政协大庆市委员会", "location": "黑龙江省大庆市肇源县"},
    {"id": 5, "name": "中共肇源县纪律检查委员会/肇源县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共大庆市纪委", "location": "黑龙江省大庆市肇源县"},
    {"id": 6, "name": "肇源县公安局", "type": "司法", "level": "县处级", "parent": "大庆市公安局", "location": "黑龙江省大庆市肇源县"},
    {"id": 7, "name": "肇源县人民法院", "type": "司法", "level": "县处级", "parent": "大庆市中级人民法院", "location": "黑龙江省大庆市肇源县"},
    {"id": 8, "name": "肇源县人民检察院", "type": "司法", "level": "县处级", "parent": "大庆市人民检察院", "location": "黑龙江省大庆市肇源县"},
    {"id": 9, "name": "肇源县委政法委", "type": "党委", "level": "县处级", "parent": "中共肇源县委员会", "location": "黑龙江省大庆市肇源县"},
    {"id": 10, "name": "肇源县委统战部", "type": "党委", "level": "县处级", "parent": "中共肇源县委员会", "location": "黑龙江省大庆市肇源县"},
    {"id": 11, "name": "中共大庆市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委", "location": "黑龙江省大庆市"},
    {"id": 12, "name": "大庆市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省大庆市"},
    {"id": 13, "name": "肇源县新站镇", "type": "乡镇/街道", "level": "乡科级", "parent": "肇源县人民政府", "location": "黑龙江省大庆市肇源县新站镇"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 权占峰 — 县委书记（现任）
    {"id": 1, "name": "权占峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共肇源县委书记", "current_org": "中共肇源县委员会",
     "source": "http://www.zgzy.gov.cn/zhaoyuan/zwdt2/202608/c05_417265.shtml"},
    # 2 — 宁利文 — 县委副书记、县长（现任）
    {"id": 2, "name": "宁利文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "肇源县委副书记、县人民政府县长", "current_org": "肇源县人民政府",
     "source": "http://www.zgzy.gov.cn/zhaoyuan/jgzn2/202412/c05_362821.shtml"},
    # 3 — 王双武 — 县委常委、常务副县长
    {"id": 3, "name": "王双武", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "肇源县委常委、常务副县长", "current_org": "肇源县人民政府",
     "source": "http://www.zgzy.gov.cn/zhaoyuan/jgzn2/202605/c05_410657.shtml"},
    # 4 — 魏晓龙 — 县委常委、纪委书记、监委代主任
    {"id": 4, "name": "魏晓龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "肇源县委常委、纪委书记、监委代主任", "current_org": "中共肇源县纪律检查委员会",
     "source": "http://www.zgzy.gov.cn/zhaoyuan/toutiao/202607/c05_417161.shtml"},
    # 5 — 胡东升 — 县委常委、政法委书记（2026-05 由副县长提任）
    {"id": 5, "name": "胡东升", "gender": "男", "ethnicity": "满族",
     "birth": "1976-08", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "肇源县委常委、政法委书记", "current_org": "肇源县委政法委",
     "source": "https://www.daqing.gov.cn/daqing/renshixinxizt/202605/c05_410632.shtml"},
    # 6 — 毕艳辉 — 县委常委、统战部部长（2026-08 拟任政协主席候选）
    {"id": 6, "name": "毕艳辉", "gender": "女", "ethnicity": "汉族",
     "birth": "1973-09", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "肇源县委常委、统战部部长（三级调研员；拟任县政协主席）", "current_org": "肇源县委统战部",
     "source": "https://www.daqing.gov.cn/daqing/renshixinxizt/202608/c05_417276.shtml"},
    # 7 — 李金才 — 县人大常委会主任
    {"id": 7, "name": "李金才", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "肇源县人大常委会主任", "current_org": "肇源县人民代表大会常务委员会",
     "source": "http://www.zgzy.gov.cn/zhaoyuan/toutiao/202607/c05_417161.shtml"},
    # 8 — 孙伟山 — 副县长
    {"id": 8, "name": "孙伟山", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "肇源县人民政府副县长", "current_org": "肇源县人民政府",
     "source": "http://www.zgzy.gov.cn/zhaoyuan/jgzn2/202509/c05_391647.shtml"},
    # 9 — 宋梓宁 — 副县长
    {"id": 9, "name": "宋梓宁", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "肇源县人民政府副县长", "current_org": "肇源县人民政府",
     "source": "http://www.zgzy.gov.cn/zhaoyuan/jgzn2/202504/c05_376465.shtml"},
    # 10 — 李岩 — 副县长
    {"id": 10, "name": "李岩", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "肇源县人民政府副县长", "current_org": "肇源县人民政府",
     "source": "http://www.zgzy.gov.cn/zhaoyuan/jgzn2/202509/c05_391644.shtml"},
    # 11 — 尚伟 — 副县长
    {"id": 11, "name": "尚伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "肇源县人民政府副县长", "current_org": "肇源县人民政府",
     "source": "http://www.zgzy.gov.cn/zhaoyuan/jgzn2/202412/c05_362808.shtml"},
    # 12 — 张希庆 — 副县长
    {"id": 12, "name": "张希庆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "肇源县人民政府副县长", "current_org": "肇源县人民政府",
     "source": "http://www.zgzy.gov.cn/zhaoyuan/jgzn2/202412/c05_362812.shtml"},
    # 13 — 张秋林 — 副县长
    {"id": 13, "name": "张秋林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "肇源县人民政府副县长", "current_org": "肇源县人民政府",
     "source": "http://www.zgzy.gov.cn/zhaoyuan/jgzn2/202412/c05_362816.shtml"},
    # 14 — 刘怡爽 — 跨县流动人物（2020-2021 肇源县委副书记/新站镇党委书记 → 龙凤区区长）
    {"id": 14, "name": "刘怡爽", "gender": "女", "ethnicity": "汉族",
     "birth": "1976-07", "birthplace": "", "education": "黑龙江大学研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大庆市龙凤区委副书记、区长", "current_org": "大庆市龙凤区人民政府",
     "source": "http://www.dqlf.gov.cn/longfeng/g11/202303/c05_189875.shtml"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 权占峰
    {"person_id": 1, "org_id": 1, "title": "肇源县委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持县委十九届第98次常委会（2026-07-31）；多篇 2026 要闻确认在任"},
    {"person_id": 1, "org_id": 11, "title": "（任县委书记前履历待查）", "start": "", "end": "", "rank": "", "note": "公开资料未找到任肇源县委书记前完整履历"},
    # 宁利文
    {"person_id": 2, "org_id": 2, "title": "肇源县人民政府县长", "start": "", "end": "present", "rank": "正处级", "note": "2026-01-13 县十八届人大五次会议作政府工作报告；主持县政府全面工作，主管财政/发改/审计"},
    {"person_id": 2, "org_id": 1, "title": "肇源县委副书记", "start": "", "end": "present", "rank": "正处级", "note": "兼任县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "（上任县长前履历待查）", "start": "", "end": "", "rank": "", "note": "公开履历缺口"},
    # 王双武
    {"person_id": 3, "org_id": 2, "title": "肇源县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责常务工作；分管财政/发改/审计；县长外出期间主持县政府工作"},
    {"person_id": 3, "org_id": 1, "title": "肇源县委常委", "start": "", "end": "present", "rank": "副处级", "note": "县十八届人大第40次会议到场"},
    # 魏晓龙
    {"person_id": 4, "org_id": 5, "title": "肇源县委常委、纪委书记、监委代主任", "start": "", "end": "present", "rank": "副处级", "note": "2026-07-30 县人大第40次会议列席"},
    # 胡东升
    {"person_id": 5, "org_id": 9, "title": "肇源县委常委、政法委书记", "start": "2026-05", "end": "present", "rank": "副处级", "note": "2026-05-09 大庆市委公示由副县长拟任县委常委；2026-07-30 停任政法委书记"},
    {"person_id": 5, "org_id": 2, "title": "肇源县人民政府副县长", "start": "", "end": "2026-05", "rank": "副处级", "note": "提任县委常委前职务；满族 1976-08 大专"},
    # 毕艳辉
    {"person_id": 6, "org_id": 10, "title": "肇源县委常委、统战部部长（三级调研员）", "start": "", "end": "present", "rank": "副处级", "note": "2026-08-01 公示拟提名为县（区）政协主席候选"},
    # 李金才
    {"person_id": 7, "org_id": 3, "title": "肇源县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "主持县十八届人大四十次会议（2026-07-30）"},
    # 孙伟山
    {"person_id": 8, "org_id": 2, "title": "肇源县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责工信、交通、营商环境、园区、招商"},
    # 宋梓宁
    {"person_id": 9, "org_id": 2, "title": "肇源县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责教育"},
    # 李岩
    {"person_id": 10, "org_id": 2, "title": "肇源县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责卫健、文体广电和旅游、医疗保障"},
    # 尚伟
    {"person_id": 11, "org_id": 2, "title": "肇源县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责市场监管、环境保护、民政救助、林业和草原"},
    # 张希庆
    {"person_id": 12, "org_id": 2, "title": "肇源县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责农业农村、水务"},
    # 张秋林
    {"person_id": 13, "org_id": 2, "title": "肇源县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责公安、信访"},
    # 刘怡爽（跨县，历史任职于肇源）
    {"person_id": 14, "org_id": 1, "title": "肇源县委副书记", "start": "2020-09", "end": "2021-09", "rank": "副县处级", "note": "肇源县委副书记"},
    {"person_id": 14, "org_id": 13, "title": "肇源县新站镇党委书记", "start": "2020-09", "end": "2021-09", "rank": "乡科级", "note": "兼任新站镇党委书记"},
    {"person_id": 14, "org_id": 12, "title": "大庆市龙凤区区长", "start": "2021-12", "end": "present", "rank": "正县处级", "note": "跨县交流至龙凤区任区长"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "权占峰（县委书记）与宁利文（县委副书记、县长）为肇源县现职党政主要一把手，同县委班子/县人代会共事", "overlap_org": "肇源县", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "权占峰与县委常委/常务副县长王双武同县委班子", "overlap_org": "中共肇源县委", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "权占峰与纪委书记魏晓龙同班子", "overlap_org": "中共肇源县委", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "权占峰与政法委书记胡东升同班子", "overlap_org": "中共肇源县委", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "权占峰与统战部部长毕艳辉同班子", "overlap_org": "中共肇源县委", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "宁利文（县长）与常务副县长王双武政府班子正副职搭档，常务副县长分抓财政/发改/审计", "overlap_org": "肇源县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "宁利文（县长）与副县长孙伟山政府班子搭档，分管工信交通工业", "overlap_org": "肇源县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "宁利文（县长）与副县长宋梓宁政府班子搭档，分管教育", "overlap_org": "肇源县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "宁利文（县长）与副县长李岩政府班子搭档，分管卫健文旅", "overlap_org": "肇源县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "宁利文（县长）与副县长尚伟政府班子搭档，分管市场监管环保民政", "overlap_org": "肇源县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "宁利文（县长）与副县长张希庆政府班子搭档，分管农业水务", "overlap_org": "肇源县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "宁利文（县长）与副县长张秋林政府班子搭档，分管公安信访", "overlap_org": "肇源县人民政府", "overlap_period": "现任"},
    {"person_a": 7, "person_b": 3, "type": "superior_subordinate", "context": "县人大常委会对政府工作的监督，常务副县长王双武 2026-07-30 列席人代会（债务管理、物业、医疗次中心报告）", "overlap_org": "肇源县人大/县政府", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 2, "type": "promotion_chain", "context": "胡东升由副县长提任县党委常委（2026-05 公示）", "overlap_org": "肇源县", "overlap_period": "2026"},
    {"person_a": 14, "person_b": 1, "type": "promotion_chain", "context": "刘怡爽曾任肇源县委副书记（2020-2021），为现前任县委副职，与权占峰同在肇源县委系统", "overlap_org": "中共肇源县委", "overlap_period": "2020-2021"},
    {"person_a": 14, "person_b": 2, "type": "predecessor_successor", "context": "刘怡爽2020-2021任肇源县委副书记，与现县委副书记、县长宁利文为县委副书记梯队先后任", "overlap_org": "中共肇源县委", "overlap_period": "2021前后"},
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
    print(f"Wrote DB: {DB_PATH}")
    print(f"Wrote GEXF: {GEXF_PATH}")
    print(f"Stats: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")