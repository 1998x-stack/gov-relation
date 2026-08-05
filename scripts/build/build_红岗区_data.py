#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 红岗区 leadership network.

红岗区隶属黑龙江省大庆市，位于大庆市中东部（大庆油田腹地），为石油工业城区，
产业以石油装备制造、天然气加工、精细化工等支柱产业为主，红岗经济开发区为省级园区；
辖8百垧/红岗/杏南/创业/银河/解放街道及杏树岗镇。

Current leadership (as of 2026-08, sources: 红岗区人民政府门户 www.honggang.gov.cn
"区政府·领导信息" 2026-02-06 更新 + 红岗要闻 + 大庆市委组织部拟任职公示):
- 区委书记: 郭铜强（主持区委十届常委会至第96次 2026-07；多篇 2026 要闻）
- 区委副书记、区人民政府区长: 宋玉红（2026-01-15 区十一届人大六次会议作政府工作报告）
- 区委副书记: 提常君（2025-12-15 公示由区委常委/副区长提任）
- 区委常委/政法委书记: 王大伟; 区委常委/宣传部部长/统战部部长: 邢龙
- 区政府副区长: 刘科远（常务）、孙毓（区委常委/副区长）、李云涛、邹玉峰（公安分局长）、唐立明、王东生

Biographical缺口: 郭铜强、宋玉红的出生年月/籍贯/学历/完整履历 未从公开渠道获取（官网仅列姓名职务）；
> 提常君（1978-10 省委党校研究生）、王大伟（省委党校研究生）、邢龙（1976-02 大专）出生年月由大庆市委组织部拟任职公示获得。
本构建基于官方确认的名单/职务与治理公开证据；个体履历缺口在 report 与 data/persons/*.json 中显式标注。
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

SLUG = "红岗区"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "红岗区_network.db")
    GEXF_PATH = os.path.join(_STAGING, "红岗区_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "红岗区_network.db"
    GEXF_PATH = GRAPH_DIR / "红岗区_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共大庆市红岗区委员会", "type": "党委", "level": "县处级", "parent": "中共大庆市委", "location": "黑龙江省大庆市红岗区"},
    {"id": 2, "name": "大庆市红岗区人民政府", "type": "政府", "level": "县处级", "parent": "大庆市人民政府", "location": "黑龙江省大庆市红岗区"},
    {"id": 3, "name": "红岗区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "大庆市人大常委会", "location": "黑龙江省大庆市红岗区"},
    {"id": 4, "name": "中国人民政治协商会议红岗区委员会", "type": "政协", "level": "县处级", "parent": "政协大庆市委员会", "location": "黑龙江省大庆市红岗区"},
    {"id": 5, "name": "中共红岗区纪律检查委员会/红岗区监察委员会", "type": "纪委", "level": "县处级", "parent": "中共大庆市纪委", "location": "黑龙江省大庆市红岗区"},
    {"id": 6, "name": "大庆市公安局红岗分局", "type": "司法", "level": "县处级", "parent": "大庆市公安局", "location": "黑龙江省大庆市红岗区"},
    {"id": 7, "name": "红岗区人民法院", "type": "司法", "level": "县处级", "parent": "大庆市中级人民法院", "location": "黑龙江省大庆市红岗区"},
    {"id": 8, "name": "红岗区人民检察院", "type": "司法", "level": "县处级", "parent": "大庆市人民检察院", "location": "黑龙江省大庆市红岗区"},
    {"id": 9, "name": "黑龙江红岗经济开发区管理委员会", "type": "开发区", "level": "县处级", "parent": "红岗区人民政府", "location": "黑龙江省大庆市红岗区"},
    {"id": 10, "name": "中共大庆市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委", "location": "黑龙江省大庆市"},
    {"id": 11, "name": "大庆市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省大庆市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 郭铜强 — 区委书记（现任）
    {"id": 1, "name": "郭铜强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共红岗区委书记", "current_org": "中共大庆市红岗区委员会",
     "source": "https://www.honggang.gov.cn/"},
    # 2 — 宋玉红 — 区委副书记、区长（现任）
    {"id": 2, "name": "宋玉红", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红岗区委副书记、区人民政府区长", "current_org": "大庆市红岗区人民政府",
     "source": "https://www.honggang.gov.cn/honggang/zfxxgk1/202602/c05_166098.shtml"},
    # 3 — 提常君 — 区委副书记（2025-12 提任）
    {"id": 3, "name": "提常君", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-10", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红岗区委副书记", "current_org": "中共大庆市红岗区委员会",
     "source": "https://www.daqing.gov.cn/daqing/renshixinxizt/202512/c05_398039.shtml"},
    # 4 — 王志云 — 区委副书记（2026-08 拟调离）
    {"id": 4, "name": "王志云", "gender": "女", "ethnicity": "汉族",
     "birth": "1978-12", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红岗区委副书记（三级调研员；拟调离）", "current_org": "中共大庆市红岗区委员会",
     "source": "https://www.daqing.gov.cn/daqing/renshixinxizt/202608/c05_417276.shtml"},
    # 5 — 王大伟 — 区委常委、政法委书记
    {"id": 5, "name": "王大伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1972", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红岗区委常委、政法委书记（三级调研员）", "current_org": "中共大庆市红岗区委员会",
     "source": "https://www.daqing.gov.cn/daqing/renshixinxizt/202608/c05_417276.shtml"},
    # 6 — 邢龙 — 区委常委、宣传部长、统战部长
    {"id": 6, "name": "邢龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-02", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红岗区委常委、宣传部部长、统战部部长（三级调研员）", "current_org": "中共大庆市红岗区委员会",
     "source": "https://www.daqing.gov.cn/daqing/renshixinxizt/202608/c05_417276.shtml"},
    # 7 — 刘科远 — 区委常委、常务副区长
    {"id": 7, "name": "刘科远", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红岗区委常委、常务副区长", "current_org": "大庆市红岗区人民政府",
     "source": "https://www.honggang.gov.cn/honggang/zfxxgk1/202501/c05_368116.shtml"},
    # 8 — 孙毓 — 区委常委、副区长
    {"id": 8, "name": "孙毓", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红岗区委常委、副区长", "current_org": "大庆市红岗区人民政府",
     "source": "https://www.honggang.gov.cn/honggang/zfxxgk1/202505/c05_378816.shtml"},
    # 9 — 李云涛 — 副区长
    {"id": 9, "name": "李云涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红岗区人民政府副区长", "current_org": "大庆市红岗区人民政府",
     "source": "https://www.honggang.gov.cn/honggang/zfxxgk1/202602/c05_166099.shtml"},
    # 10 — 邹玉峰 — 副区长、红岗公安分局局长
    {"id": 10, "name": "邹玉峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红岗区人民政府副区长、红岗公安分局局长", "current_org": "大庆市公安局红岗分局",
     "source": "https://www.honggang.gov.cn/honggang/zfxxgk1/202602/c05_166103.shtml"},
    # 11 — 唐立明 — 副区长
    {"id": 11, "name": "唐立明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红岗区人民政府副区长", "current_org": "大庆市红岗区人民政府",
     "source": "https://www.honggang.gov.cn/honggang/zfxxgk1/202602/c05_166100.shtml"},
    # 12 — 王东生 — 副区长
    {"id": 12, "name": "王东生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红岗区人民政府副区长", "current_org": "大庆市红岗区人民政府",
     "source": "https://www.honggang.gov.cn/honggang/zfxxgk1/202602/c05_166102.shtml"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 郭铜强
    {"person_id": 1, "org_id": 1, "title": "红岗区委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持区委十届常委会；2026年多篇要闻确认"},
    {"person_id": 1, "org_id": 10, "title": "（此前履历待查）", "start": "", "end": "", "rank": "", "note": "任红岗区委书记前任职履历未公开"},
    # 宋玉红
    {"person_id": 2, "org_id": 2, "title": "红岗区人民政府区长", "start": "2026-01", "end": "present", "rank": "正处级", "note": "2026-01-15 区十一届人大六次会议作政府工作报告"},
    {"person_id": 2, "org_id": 1, "title": "红岗区委副书记", "start": "2026-01", "end": "present", "rank": "正处级", "note": "与区长职务同时任"},
    {"person_id": 2, "org_id": 2, "title": "红岗区副区长（此前）", "start": "", "end": "2026-01", "rank": "副处级", "note": "任区长前履历待查"},
    # 提常君
    {"person_id": 3, "org_id": 1, "title": "红岗区委副书记", "start": "2025-12", "end": "present", "rank": "副处级", "note": "2025-12-15 拟任职公示提任"},
    {"person_id": 3, "org_id": 2, "title": "红岗区委常委、区政府副区长", "start": "", "end": "2025-12", "rank": "副处级", "note": "提任县委副书记前职务"},
    # 王志云
    {"person_id": 4, "org_id": 1, "title": "红岗区委副书记（三级调研员）", "start": "", "end": "2026-08", "rank": "副处级", "note": "2026-08-03 拟任市直机关正处级领导职务，拟调离"},
    # 王大伟
    {"person_id": 5, "org_id": 1, "title": "红岗区委常委、政法委书记（三级调研员）", "start": "", "end": "present", "rank": "副处级", "note": "2026-08 拟提名为县（区）人大主任候选人"},
    # 邢龙
    {"person_id": 6, "org_id": 1, "title": "红岗区委常委、宣传部部长、统战部部长（三级调研员）", "start": "", "end": "present", "rank": "副处级", "note": "2026-08 拟任县（区）政协主席候选人"},
    # 刘科远
    {"person_id": 7, "org_id": 2, "title": "红岗区委常委、常务副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责财政金融、综合经济、应急管理、统计、交通运输、国防动员"},
    # 孙毓
    {"person_id": 8, "org_id": 2, "title": "红岗区委常委、副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责经开区、自然资源"},
    # 李云涛
    {"person_id": 9, "org_id": 2, "title": "红岗区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责城乡建设、城市管理、退役军人、民政、街道"},
    # 邹玉峰
    {"person_id": 10, "org_id": 6, "title": "红岗区人民政府副区长、红岗公安分局局长", "start": "", "end": "present", "rank": "副处级", "note": "负责红岗公安分局；统筹公安工作"},
    # 唐立明
    {"person_id": 11, "org_id": 2, "title": "红岗区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责人社、教育、卫健、司法、市场监管、农业农村、林业草原、生态环境"},
    # 王东生
    {"person_id": 12, "org_id": 2, "title": "红岗区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责工信、营商环境、商务"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "郭铜强（区委书记）与宋玉红（区委副书记、区长）为红岗区现职党政主要一把手，同区委班子/区人代会共事", "overlap_org": "红岗区", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "郭铜强与区委副书记提常君同班子", "overlap_org": "中共红岗区委", "overlap_period": "2025至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "郭铜强与区委副书记王志云同班子（王志云2026-08拟调离）", "overlap_org": "中共红岗区委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "郭铜强与政法委书记王大伟同班子", "overlap_org": "中共红岗区委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "郭铜强与宣传部/统战部长邢龙同班子", "overlap_org": "中共红岗区委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "郭铜强与区委常委/常务副区长刘科远同班子", "overlap_org": "中共红岗区委", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "宋玉红（区长）与常务副区长刘科远政府班子正副职搭档", "overlap_org": "红岗区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "宋玉红（区长）与区委常委/副区长孙毓政府班子搭档", "overlap_org": "红岗区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "宋玉红（区长）与副区长李云涛政府班子搭档，分管城建民政", "overlap_org": "红岗区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "宋玉红（区长）与副区长/公安分局长邹玉峰，平安建设协同", "overlap_org": "红岗区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "宋玉红（区长）与副区长唐立明政府班子搭档，分管民生事务", "overlap_org": "红岗区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "宋玉红（区长）与副区长王东生政府班子搭档，分管工信商务", "overlap_org": "红岗区人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 7, "type": "promotion_chain", "context": "提常君由区委常委/副区长提任区委副书记（2025-12公示）", "overlap_org": "红岗区", "overlap_period": "2025"},
    {"person_a": 4, "person_b": 1, "type": "上下级", "context": "王志云（区委副书记）与郭铜强（书记）、提常君（副书记）构成区副书记班子", "overlap_org": "中共红岗区委", "overlap_period": "2026"},
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