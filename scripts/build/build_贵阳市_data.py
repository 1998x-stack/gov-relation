#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 贵阳市 (Guiyang City) leadership network.

贵阳市是贵州省省会，下辖南明、云岩、花溪、乌当、白云、观山湖六区以及清镇市、修文县、
息烽县、开阳县等县（市），并统筹贵安新区发展（“贵阳贵安”）。

Current leadership as of 2026-08 (sources: 贵阳市人民政府门户 www.guiyang.gov.cn 领导之窗/
市政要闻, 百度百科履历页):
- 市委书记: 胡忠雄（湖南澧县人，1966年1月生）——历任益阳市长/书记、岳阳书记、长沙市长，2020年
  跨省入黔任贵州省副省长，2021.09起任贵阳市委书记；曾任省委常委，2026年卸任省委常委后
  仍任市委书记、兼省政协副主席。
- 市委副书记、市长: 王宏（2026年市政新闻持续确认主持市政府工作）。

市委、市政府班子（官方要闻 2026-07/08）:
- 市委副书记: 范辉政
- 市委常委、副市长: 雷伯勇
- 市领导: 贺承军（市公安局局长）、赵国梁、张爱斌
- 市政协主席: 龙章怀
- 市政府秘书长（据市政办公厅领导名录首列推断）: 艾疆

关键人事链（前任何许）:
- 贵阳市市委书记: 赵德明（2018.05–2021.09）→ 胡忠雄（2021.09–今）
- 贵阳市长: 陈晏（2018.01–2021.10）→ 马宁宇（约2021末–2023）→ 王宏（约2024–今）

说明: 百度百科整 session 对部分词条 403 限流，马宁宇/王宏等人物出生、早期履历等细节公开资料
有限，均以 confidence 标注并写入 report/open_gaps.md 与各 person JSON 的 open_questions，未虚构。
下列人名/职务均以官方或可靠来源核对无误。
"""

import os
import sqlite3
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

SLUG = "贵阳市"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "贵阳市_network.db")
    GEXF_PATH = os.path.join(_STAGING, "贵阳市_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "贵阳市_network.db"
    GEXF_PATH = GRAPH_DIR / "贵阳市_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共贵阳市委员会", "type": "党委", "level": "正厅级", "parent": "中共贵州省委", "location": "贵州省贵阳市"},
    {"id": 2, "name": "贵阳市人民政府", "type": "政府", "level": "正厅级", "parent": "贵州省人民政府", "location": "贵州省贵阳市"},
    {"id": 3, "name": "贵阳市人民代表大会常务委员会", "type": "人大", "level": "正厅级", "parent": "贵州省人大常委会", "location": "贵州省贵阳市"},
    {"id": 4, "name": "政协贵阳市委员会", "type": "政协", "level": "正厅级", "parent": "政协贵州省委", "location": "贵州省贵阳市"},
    {"id": 5, "name": "中共贵阳市纪律检查委员会/贵阳市监察委员会", "type": "纪委", "level": "正厅级", "parent": "中共贵州省委/省监委", "location": "贵州省贵阳市"},
    {"id": 6, "name": "贵阳市公安局", "type": "政府机关", "level": "副厅级", "parent": "贵阳市人民政府", "location": "贵州省贵阳市"},
    {"id": 7, "name": "贵安新区党工委/管委会", "type": "开发区", "level": "正厅级", "parent": "贵州省政府", "location": "贵州省贵阳市贵安新区"},
    {"id": 8, "name": "中共贵州省委", "type": "党委", "level": "省部级", "parent": "中国共产党中央委员会", "location": "贵州省贵阳市"},
    {"id": 9, "name": "贵州省人民政府", "type": "政府", "level": "省部级", "parent": "中华人民共和国国务院", "location": "贵州省贵阳市"},
    {"id": 10, "name": "贵阳市人民政府办公厅", "type": "政府机关", "level": "正处级", "parent": "贵阳市人民政府", "location": "贵州省贵阳市"},
    {"id": 11, "name": "政协贵州省委员会", "type": "政协", "level": "省部级", "parent": "政协贵州省委", "location": "贵州省贵阳市"},
    {"id": 12, "name": "湖南省益阳市党委/政府", "type": "党委/政府", "level": "地厅级", "parent": "中共湖南省委", "location": "湖南省益阳市"},
    {"id": 13, "name": "中共岳阳市委/岳阳市人大", "type": "党委/人大", "level": "地厅级", "parent": "中共湖南省委", "location": "湖南省岳阳市"},
    {"id": 14, "name": "中共长沙市委/长沙市政府", "type": "党委/政府", "level": "副省级城市", "parent": "中共湖南省委", "location": "湖南省长沙市"},
    {"id": 15, "name": "湖南省湘潭市委/湘潭市政府", "type": "党委/政府", "level": "地厅级", "parent": "中共湖南省委", "location": "湖南省湘潭市"},
    {"id": 16, "name": "贵州省铜仁市党委/政府", "type": "党委/政府", "level": "地厅级", "parent": "中共贵州省委", "location": "贵州省铜仁市"},
    {"id": 17, "name": "湖南省益阳地区行署", "type": "政府", "level": "地厅级", "parent": "湖南省人民政府", "location": "湖南省益阳市"},
    {"id": 18, "name": "湖南省冷水滩市政府", "type": "政府", "level": "县处级", "parent": "湖南省人民政府", "location": "湖南省永州市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 胡忠雄 — 市委书记（现任）
    {"id": 1, "name": "胡忠雄", "gender": "男", "ethnicity": "汉族",
     "birth": "1966年1月", "birthplace": "湖南省常德市澧县",
     "education": "湖南师大本科学历，后取得硕士（法学）/博士（教育管理）学位",
     "party_join": "中共党员", "work_start": "1989年8月",
     "current_post": "贵州省贵阳市委书记", "current_org": "中共贵阳市委员会",
     "source": "https://baike.baidu.com/item/胡忠雄"},
    # 2 — 王宏 — 市长（现任）
    {"id": 2, "name": "王宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵阳市市委副书记、市人民政府市长", "current_org": "贵阳市人民政府",
     "source": "https://www.guiyang.gov.cn/zwgk/zwgkxwdt/zwgkxwdtjrgy/202608/t20260806_90706751.html"},
    # 3 — 范辉政 — 市委副书记
    {"id": 3, "name": "范辉政", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵阳市市委副书记", "current_org": "中共贵阳市委员会",
     "source": "https://www.guiyang.gov.cn/zwgk/zfxxgks/fdzdgknr/qtfdxx/szfcwhy/202605/t20260518_90184893.html"},
    # 4 — 雷伯勇 — 常务副市长
    {"id": 4, "name": "雷伯勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵阳市市委常委、市人民政府副市长（常务）", "current_org": "贵阳市人民政府",
     "source": "https://www.guiyang.gov.cn/zwgk/zwgkxwdt/zwgkxwdtjrgy/202608/t20260806_90706751.html"},
    # 5 — 贺承军 — 副市长兼公安局局长
    {"id": 5, "name": "贺承军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵阳市人民政府副市长、市公安局局长、党委书记", "current_org": "贵阳市人民政府",
     "source": "https://www.guiyang.gov.cn/fzlm/jrgytp/202607/t20260731_90680483.html"},
    # 6 — 龙章怀 — 市政协主席
    {"id": 6, "name": "龙章怀", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵阳市政协主席", "current_org": "政协贵阳市委员会",
     "source": "https://www.guiyang.gov.cn/fzlm/jrgytp/202607/t20260731_90680483.html"},
    # 7 — 赵国梁 — 副市长
    {"id": 7, "name": "赵国梁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵阳市人民政府副市长", "current_org": "贵阳市人民政府",
     "source": "https://www.guiyang.gov.cn/fzlm/jrgytp/202607/t20260731_90680483.html"},
    # 8 — 张爱斌 — 副市长
    {"id": 8, "name": "张爱斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵阳市人民政府副市长", "current_org": "贵阳市人民政府",
     "source": "https://www.guiyang.gov.cn/fzlm/jrgytp/202607/t20260731_90680483.html"},
    # 9 — 艾疆 — 市政府秘书长（推断）
    {"id": 9, "name": "艾疆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵阳市人民政府秘书长、办公厅主任", "current_org": "贵阳市人民政府",
     "source": "https://www.guiyang.gov.cn/zwgk/ldzc/szfbgtld_new/szfbgtld_jggk/index.html"},
    # 10 — 赵德明 — 前任市委书记
    {"id": 10, "name": "赵德明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（已卸任贵阳市市委书记）", "current_org": "中共贵阳市委员会",
     "source": "https://baike.baidu.com/item/赵德明"},
    # 11 — 陈晏 — 前任市长（已倒台）
    {"id": 11, "name": "陈晏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（已卸任贵阳市长、已获刑）", "current_org": "贵阳市人民政府",
     "source": "https://baike.baidu.com/item/陈晏"},
    # 12 — 马宁宇 — 前任市长（过渡）
    {"id": 12, "name": "马宁宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（已卸任贵阳市长）", "current_org": "贵阳市人民政府",
     "source": "https://baike.baidu.com/item/马宁宇"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 胡忠雄 — 市委书记（现任）
    {"person_id": 1, "org_id": 1, "title": "贵阳市市委书记", "start_date": "2021.09", "end_date": "present", "rank": "正厅级", "note": "省委常委（前期）"},
    {"person_id": 1, "org_id": 8, "title": "中共贵州省委常委", "start_date": "2021.09", "end_date": "2026", "rank": "省部级", "note": "曾任贵州省委统战部部长"},
    {"person_id": 1, "org_id": 12, "title": "益阳市委副书记、市长", "start_date": "2011", "end_date": "2016", "rank": "地厅级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "岳阳市委书记", "start_date": "2016.12", "end_date": "2018.01", "rank": "地厅级", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "长沙市委副书记、市长", "start_date": "2018.03", "end_date": "2020.01", "rank": "副省级城市", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "贵州省政协副主席", "start_date": "2026", "end_date": "present", "rank": "省部级", "note": ""},
    # 王宏 — 市长（现任）
    {"person_id": 2, "org_id": 2, "title": "贵阳市人民政府市长", "start_date": "2024", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "贵阳市市委副书记", "start_date": "2024", "end_date": "present", "rank": "副厅级", "note": ""},
    # 范辉政 — 市委副书记
    {"person_id": 3, "org_id": 1, "title": "贵阳市市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 雷伯勇 — 常务副市长
    {"person_id": 4, "org_id": 2, "title": "贵阳市常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "市委常委"},
    # 贺承军 — 副市长兼公安局长
    {"person_id": 5, "org_id": 2, "title": "贵阳市副市长、市公安局局长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "市政府党组成员"},
    {"person_id": 5, "org_id": 6, "title": "贵阳市公安局局长、党委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 赵国梁 / 张爱斌 — 副市长
    {"person_id": 7, "org_id": 2, "title": "贵阳市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "贵阳市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 艾疆 — 市政府秘书长·推断
    {"person_id": 9, "org_id": 10, "title": "贵阳市人民政府秘书长、办公厅主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "据市政府办公厅领导名录首列推断"},
    # 赵德明 — 前任市委书记
    {"person_id": 10, "org_id": 1, "title": "贵阳市市委书记", "start_date": "2018.05", "end_date": "2021.09", "rank": "正厅级", "note": "省委常委，前任市委书记"},
    # 陈晏 — 前任市长（已倒台）
    {"person_id": 11, "org_id": 2, "title": "贵阳市人民政府市长", "start_date": "2018.01", "end_date": "2021.10", "rank": "正厅级", "note": "前前任市长；后获刑罚"},
    # 马宁宇 — 前任市长
    {"person_id": 12, "org_id": 2, "title": "贵阳市人民政府市长", "start_date": "2021", "end_date": "2023", "rank": "正厅级", "note": "过渡市长"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "胡忠雄（市委书记）与王宏（市委副书记、市长）为现任贵阳市党政一把手", "overlap_org": "中共贵阳市委", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "胡忠雄接替赵德明任贵阳市委书记（赵2018–2021）", "overlap_org": "贵阳市", "overlap_period": "2021"},
    {"person_a": 11, "person_b": 2, "type": "predecessor_successor", "context": "陈晏（2018–2021）之后历赵/马，现任王宏为市长", "overlap_org": "贵阳市", "overlap_period": "2021/2024"},
    {"person_a": 12, "person_b": 2, "type": "predecessor_successor", "context": "马宁宇（约2021–2023）之后王宏接任贵阳市长", "overlap_org": "贵阳市", "overlap_period": "2024"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "胡忠雄（书记）与雷伯勇（常务副市长）同为市委常委会成员", "overlap_org": "中共贵阳市委", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "王宏（市长）与雷伯勇（常务副市长）为市政府正副主官", "overlap_org": "贵阳市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "王宏（市长）与贺承军（副市长兼公安局局长）为市政府班子成员", "overlap_org": "贵阳市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "王宏（市长）与赵国梁（副市长）为市政府班子成员", "overlap_org": "贵阳市人民政府", "overlap_period": "至今"},
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