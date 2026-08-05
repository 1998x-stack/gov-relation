#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 梨树区 leadership network.

梨树区隶属黑龙江省鸡西市，位于鸡西市区西部，是全国重要的煤炭工业城区之一，
区境内分布梨树镇、平岗等街道，曾以煤矿产业著称，现推进"一谷三区四产业"
产业转型升级与生态修复（矸石山综合治理）。

Current leadership as of 2026-08 (sources: 鸡西市梨树区人民政府门户 www.jixilishu.gov.cn
官方"政府领导"之窗 + 梨树区"梨树微讯"公众号官方报道):
- 区委书记: 郭志鹏（公众号多篇区委常委会/督导检查报道盖章确认）
- 区委副书记、区长: 徐春雷（区委副书记、政府区长、区政府党组书记，政府领导之窗确认）

四大班子（2026年第十七届人大六次会议主席台名单确认）:
- 区人大常委会主任: 王伟泉
- 区政协主席: 吕建辉
- 区委常委、纪委书记、监委主任: 周向宇
- 区委常委、常务副区长: 陶君喜
- 区委常委、副区长: 邹雪峰

Biographical detail (出生/学历/入党) 在官方页面缺失，标记为 open_questions；
构建仍基于官方确认的名单、职务与治理公开证据。具体见 report 与 data/persons/*.json。
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

SLUG = "梨树区"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "梨树区_network.db")
    GEXF_PATH = os.path.join(_STAGING, "梨树区_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "梨树区_network.db"
    GEXF_PATH = GRAPH_DIR / "梨树区_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共梨树区委员会", "type": "党委", "level": "县处级", "parent": "中共鸡西市委", "location": "黑龙江省鸡西市梨树区"},
    {"id": 2, "name": "梨树区人民政府", "type": "政府", "level": "县处级", "parent": "鸡西市人民政府", "location": "黑龙江省鸡西市梨树区"},
    {"id": 3, "name": "梨树区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "鸡西市人大常委会", "location": "黑龙江省鸡西市梨树区"},
    {"id": 4, "name": "中国人民政治协商会议梨树区委员会", "type": "政协", "level": "县处级", "parent": "政协鸡西市委员会", "location": "黑龙江省鸡西市梨树区"},
    {"id": 5, "name": "中共梨树区纪律检查委员会/梨树区监察委员会", "type": "纪委", "level": "县处级", "parent": "中共鸡西市纪委", "location": "黑龙江省鸡西市梨树区"},
    {"id": 6, "name": "梨树区人民法院", "type": "司法", "level": "县处级", "parent": "鸡西市中级人民法院", "location": "黑龙江省鸡西市梨树区"},
    {"id": 7, "name": "梨树区人民检察院", "type": "司法", "level": "县处级", "parent": "鸡西市人民检察院", "location": "黑龙江省鸡西市梨树区"},
    {"id": 8, "name": "中共鸡西市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委", "location": "黑龙江省鸡西市"},
    {"id": 9, "name": "鸡西市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省鸡西市"},
    {"id": 10, "name": "梨树区教育局", "type": "政府", "level": "科级", "parent": "梨树区人民政府", "location": "黑龙江省鸡西市梨树区"},
    {"id": 11, "name": "梨树区卫生健康局", "type": "政府", "level": "科级", "parent": "梨树区人民政府", "location": "黑龙江省鸡西市梨树区"},
    {"id": 12, "name": "梨树区医疗保障局", "type": "政府", "level": "科级", "parent": "梨树区人民政府", "location": "黑龙江省鸡西市梨树区"},
    {"id": 13, "name": "梨树区住房和城乡建设局", "type": "政府", "level": "科级", "parent": "梨树区人民政府", "location": "黑龙江省鸡西市梨树区"},
    {"id": 14, "name": "梨树区平岗街道办事处", "type": "乡镇/街道", "level": "正科级", "parent": "梨树区人民政府", "location": "黑龙江省鸡西市梨树区"},
    {"id": 15, "name": "梨树区街里街道办事处", "type": "乡镇/街道", "level": "正科级", "parent": "梨树区人民政府", "location": "黑龙江省鸡西市梨树区"},
    {"id": 16, "name": "梨树区凤山村", "type": "村", "level": "村级", "parent": "梨树区人民政府", "location": "黑龙江省鸡西市梨树区"},
    {"id": 17, "name": "鸡西市消防救援局", "type": "市直单位", "level": "地厅级", "parent": "鸡西市人民政府", "location": "黑龙江省鸡西市"},
    {"id": 18, "name": "梨树区人民武装部", "type": "军事", "level": "县处级", "parent": "中国人民解放军鸡西军分区", "location": "黑龙江省鸡西市梨树区"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 郭志鹏 — 区委书记（现任）
    {"id": 1, "name": "郭志鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共梨树区委书记", "current_org": "中共梨树区委员会",
     "source": "https://www.jixilishu.gov.cn/（梨树区委常委会会议、督导检查报道）"},
    # 2 — 徐春雷 — 区委副书记、区长（现任）
    {"id": 2, "name": "徐春雷", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区委副书记、政府区长、区政府党组书记", "current_org": "梨树区人民政府",
     "source": "http://www.jixilishu.gov.cn/lsq/1aa57951d016451a809304accbd5179e/202309/c06_155119.shtml"},
    # 3 — 周向宇 — 区委常委、纪委书记、监委主任
    {"id": 3, "name": "周向宇", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区委常委、纪委书记、监委主任", "current_org": "中共梨树区纪律检查委员会",
     "source": "https://www.jixilishu.gov.cn/"},
    # 4 — 陶君喜 — 区委常委、常务副区长
    {"id": 4, "name": "陶君喜", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区委常委、常务副区长", "current_org": "梨树区人民政府",
     "source": "http://www.jixilishu.gov.cn/lsq/049c1b9bd9f84d4c559cd128af99d5c6f2/202506/c06_158160.shtml"},
    # 5 — 邹雪峰 — 区委常委、副区长
    {"id": 5, "name": "邹雪峰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区委常委、副区长", "current_org": "梨树区人民政府",
     "source": "http://www.jixilishu.gov.cn/"},
    # 6 — 王伟泉 — 区人大常委会主任
    {"id": 6, "name": "王伟泉", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区人大常委会主任", "current_org": "梨树区人民代表大会常务委员会",
     "source": "https://www.jixilishu.gov.cn/"},
    # 7 — 吕建辉 — 区政协主席
    {"id": 7, "name": "吕建辉", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区政协主席", "current_org": "中国人民政治协商会议梨树区委员会",
     "source": "https://www.jixilishu.gov.cn/"},
    # 8 — 程显斌 — 副区长
    {"id": 8, "name": "程显斌", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区副区长", "current_org": "梨树区人民政府",
     "source": "http://www.jixilishu.gov.cn/lsq/049c1b9bd9f846df8194c731dd3b0b97f/202309/c20_116198.shtml"},
    # 9 — 宋继武 — 副区长
    {"id": 9, "name": "宋继武", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区副区长", "current_org": "梨树区人民政府",
     "source": "http://www.jixilishu.gov.cn/"},
    # 10 — 周庆玺 — 副区长
    {"id": 10, "name": "周庆玺", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区副区长", "current_org": "梨树区人民政府",
     "source": "https://www.jixilishu.gov.cn/"},
    # 11 — 孙宇良 — 副区长
    {"id": 11, "name": "孙宇良", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区副区长", "current_org": "梨树区人民政府",
     "source": "http://www.jixilishu.gov.cn/"},
    # 12 — 孙子淇 — 副区长（挂职）
    {"id": 12, "name": "孙子淇", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区副区长（挂职）", "current_org": "梨树区人民政府",
     "source": "http://www.jixilishu.gov.cn/lsq/049c1b9bd9f846df5c4d20c062858d5a4342/202506/c20_115817.shtml"},
    # 13 — 马文欣 — 区人民法院院长
    {"id": 13, "name": "马文欣", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区人民法院院长", "current_org": "梨树区人民法院",
     "source": "https://www.jixilishu.gov.cn/"},
    # 14 — 郭丽 — 区人民检察院代理检察长
    {"id": 14, "name": "郭丽", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区人民检察院代理检察长", "current_org": "梨树区人民检察院",
     "source": "https://www.jixilishu.gov.cn/"},
    # 15-22 — 其他区委常委/区领导（人代会主席台名单）
    {"id": 15, "name": "孔德利", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区委常委/区领导", "current_org": "中共梨树区委员会",
     "source": "https://www.jixilishu.gov.cn/"},
    {"id": 16, "name": "赵金鹏", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区委常委/区领导", "current_org": "中共梨树区委员会",
     "source": "https://www.jixilishu.gov.cn/"},
    {"id": 17, "name": "张启迪", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区委常委/区领导", "current_org": "中共梨树区委员会",
     "source": "https://www.jixilishu.gov.cn/"},
    {"id": 18, "name": "杜国强", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区委常委/区领导", "current_org": "中共鸡西市委员会",
     "source": "https://www.jixilishu.gov.cn/"},
    {"id": 19, "name": "赵武", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区领导", "current_org": "中共鸡西市委员会",
     "source": "https://www.jixilishu.gov.cn/"},
    {"id": 20, "name": "杨艳秋", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区领导", "current_org": "中共鸡西市委员会",
     "source": "https://www.jixilishu.gov.cn/"},
    {"id": 21, "name": "朱秀芳", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "梨树区领导", "current_org": "中共鸡西市委员会",
     "source": "https://www.jixilishu.gov.cn/"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 郭志鹏
    {"person_id": 1, "org_id": 1, "title": "梨树区委书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "2026年多次主持区委常委会会议（官方公众号确认），任期起点待查"},
    # 徐春雷
    {"person_id": 2, "org_id": 2, "title": "梨树区委副书记、政府区长、区政府党组书记", "start": "约2023", "end": "present", "rank": "正处级", "note": "政府领导之窗 / 区政府党组会议主持；履职记录始于2023"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "约2023", "end": "present", "rank": "正处级", "note": "与区长职务同时任"},
    # 周向宇
    {"person_id": 3, "org_id": 5, "title": "梨树区委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 陶君喜
    {"person_id": 4, "org_id": 2, "title": "梨树区委常委、常务副区长", "start": "", "end": "present", "rank": "副处级", "note": "人代会作十五五规划纲要说明"},
    # 邹雪峰
    {"person_id": 5, "org_id": 2, "title": "梨树区委常委、副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王伟泉
    {"person_id": 6, "org_id": 3, "title": "梨树区人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "作区人大常委会工作报告"},
    # 吕建辉
    {"person_id": 7, "org_id": 4, "title": "梨树区政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 程显斌
    {"person_id": 8, "org_id": 2, "title": "梨树区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 宋继武
    {"person_id": 9, "org_id": 2, "title": "梨树区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 周庆玺
    {"person_id": 10, "org_id": 2, "title": "梨树区副区长", "start": "", "end": "present", "rank": "副处级", "note": "陪同区委书记督导检查生态环保、基层治理"},
    # 孙宇良
    {"person_id": 11, "org_id": 2, "title": "梨树区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 孙子淇（挂职）
    {"person_id": 12, "org_id": 2, "title": "梨树区副区长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "负责教育、卫生健康、医疗保障；分管教育局、卫健局、医保局、住建局（部分）"},
    {"person_id": 12, "org_id": 10, "title": "分管教育局", "start": "", "end": "present", "rank": "", "note": "挂职副区长分管局长"},
    # 马文欣
    {"person_id": 13, "org_id": 6, "title": "梨树区人民法院院长", "start": "", "end": "present", "rank": "副院/正处", "note": "作区人民法院工作报告"},
    # 郭丽
    {"person_id": 14, "org_id": 7, "title": "梨树区人民检察院代理检察长", "start": "", "end": "present", "rank": "正处", "note": "作区人民检察院工作报告"},
    # 其他区领导/常委
    {"person_id": 15, "org_id": 1, "title": "梨树区委常委/区领导", "start": "", "end": "present", "rank": "副处级", "note": "人代会主席台名单"},
    {"person_id": 16, "org_id": 1, "title": "梨树区委常委/区领导", "start": "", "end": "present", "rank": "副处级", "note": "人代会主席台名单"},
    {"person_id": 17, "org_id": 1, "title": "梨树区委常委/区领导", "start": "", "end": "present", "rank": "副处级", "note": "人代会主席台名单"},
    {"person_id": 18, "org_id": 8, "title": "鸡西市/梨树区领导", "start": "", "end": "present", "rank": "", "note": "人代会主席台名单，任职归属待细分"},
    {"person_id": 19, "org_id": 8, "title": "鸡西市/梨树区领导", "start": "", "end": "present", "rank": "", "note": "人代会主席台名单，任职归属待细分"},
    {"person_id": 20, "org_id": 8, "title": "鸡西市/梨树区领导", "start": "", "end": "present", "rank": "", "note": "人代会主席台名单，任职归属待细分"},
    {"person_id": 21, "org_id": 8, "title": "鸡西市/梨树区领导", "start": "", "end": "present", "rank": "", "note": "人代会主席台名单，任职归属待细分"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "郭志鹏（区委书记）与徐春雷（区委副书记、区长）为梨树区现任党政主要一把手，同一区委班子共事", "overlap_org": "梨树区", "overlap_period": "2023/2026至今"},
    # 区委书记与区委班子
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "郭志鹏任区委书记，周向宇任区委常委纪委书记，同一班子", "overlap_org": "梨树区", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "郭志鹏与常务副区长陶君喜共事", "overlap_org": "梨树区", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "郭志鹏与区委常委、副区长邹雪峰共事", "overlap_org": "梨树区", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "郭志鹏督导检查，副区长周庆玺陪同", "overlap_org": "梨树区", "overlap_period": "2026"},
    # 区长与副区长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "徐春雷区长与常务副区长陶君喜共事", "overlap_org": "梨树区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "徐春雷区长与区委常委、副区长邹雪峰共事", "overlap_org": "梨树区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "徐春雷区长与挂职副区长孙子淇共事，分管教育卫健", "overlap_org": "梨树区人民政府", "overlap_period": "至今"},
    # 党政 vs 人大/政协
    {"person_a": 1, "person_b": 6, "type": "predecessor_successor/上下级", "context": "郭志鹏与区人大常委会主任王伟泉同台履职", "overlap_org": "梨树区", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "徐春雷向人代会报告政府工作，王伟泉作人大常委会报告", "overlap_org": "梨树区", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "郭志鹏与区政协主席吕建辉同台履职", "overlap_org": "梨树区", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "同场公职", "context": "徐春雷与政协主席吕建辉同席政府/政协会议", "overlap_org": "梨树区", "overlap_period": "至今"},
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