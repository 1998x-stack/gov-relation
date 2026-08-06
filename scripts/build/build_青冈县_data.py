#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 黑龙江省绥化市青冈县 leadership network.

青冈县隶属黑龙江省绥化市，县政府驻地青冈镇（县级行政区）。

**Current leadership as of 2026-08 (官方 www.qgnet.gov.cn 青冈县人民政府门户):**
- 县委书记：孙国文（确认；官方青冈要闻 2026-07-31 "孙国文走访慰问驻青部队"明确"县委书记孙国文"）
- 县委副书记、县长：马庆宝（确认；官方青冈要闻 2026-08-06 "县防汛抗旱指挥部总指挥长马庆宝"、
  重大会议 2026-07-22 "县委副书记、县长马庆宝主持召开县政府2026年第12次常务会议"）
- 县委常委、县政府副县长：王洪伟（2026-08-05 防汛调研陪同）
- 副县长：王秀鹏、孙中辉
- 县人武部政委：王昊（县委常委）；县人武部部长：李永
- 县人大常委会副主任：郑秀艳；县政协副主席：商淑红

资料来源（一手官方）：青冈县人民政府门户 www.qgnet.gov.cn 青冈要闻/重大会议；
关联市领导：绥化市政府门户 www.suihua.gov.cn（市委书记 韩雪松、市长 陈立军 2026 新闻）。
受技术检索环境影响（搜索引擎全被 anti-bot 拦截），孙国文/马庆宝的出生、籍贯、学历等
履历型信息及前任信息未能逐项核实，已列入 report/ 与 person JSON 的 open_questions 说明。
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

SLUG = "青冈县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "青冈县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "青冈县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "青冈县_network.db"
    GEXF_PATH = GRAPH_DIR / "青冈县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共青冈县委员会", "type": "党委", "level": "县处级", "parent": "中共绥化市委", "location": "黑龙江省绥化市青冈县"},
    {"id": 2, "name": "青冈县人民政府", "type": "政府", "level": "县处级", "parent": "绥化市人民政府", "location": "黑龙江省绥化市青冈县"},
    {"id": 3, "name": "青冈县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "绥化市人大常委会", "location": "黑龙江省绥化市青冈县"},
    {"id": 4, "name": "中国人民政治协商会议青冈县委员会", "type": "政协", "level": "县处级", "parent": "政协绥化市委员会", "location": "黑龙江省绥化市青冈县"},
    {"id": 5, "name": "中共青冈县纪律检查委员会/青冈县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共绥化市纪委", "location": "黑龙江省绥化市青冈县"},
    {"id": 6, "name": "青冈县人民武装部", "type": "其他", "level": "县处级", "parent": "绥化军分区", "location": "黑龙江省绥化市青冈县"},
    {"id": 7, "name": "中共绥化市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委", "location": "黑龙江省绥化市北林区"},
    {"id": 8, "name": "绥化市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省绥化市北林区"},
    {"id": 9, "name": "中共黑龙江省委员会", "type": "党委", "level": "省部级", "parent": "", "location": "黑龙江省哈尔滨市"},
    {"id": 10, "name": "黑龙江省人民政府", "type": "政府", "level": "省部级", "parent": "", "location": "黑龙江省哈尔滨市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
# 1-2 为调研核心目标（县委书记、县长），其余为 2026 公开领导班子成员。
persons = [
    # 1 — 孙国文 — 青冈县委书记（现任，官方确认）
    {"id": 1, "name": "孙国文", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "中共青冈县委书记", "current_org": "中共青冈县委员会",
     "source": "http://www.qgnet.gov.cn/qg/qgyw/202607/c12_238688.shtml"},
    # 2 — 马庆宝 — 县委副书记、县长（现任，官方确认）
    {"id": 2, "name": "马庆宝", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "青冈县委副书记、青冈县人民政府县长", "current_org": "青冈县人民政府",
     "source": "http://www.qgnet.gov.cn/qg/qgyw/202608/c12_239190.shtml"},
    # 3 — 王洪伟 — 县委常委、副县长
    {"id": 3, "name": "王洪伟", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "青冈县委常委、县人民政府副县长", "current_org": "青冈县人民政府",
     "source": "http://www.qgnet.gov.cn/qg/qgyw/202608/c12_239190.shtml"},
    # 4 — 王秀鹏 — 副县长
    {"id": 4, "name": "王秀鹏", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "青冈县人民政府副县长", "current_org": "青冈县人民政府",
     "source": "http://www.qgnet.gov.cn/qg/zyhy/202607/c12_238204.shtml"},
    # 5 — 孙中辉 — 副县长
    {"id": 5, "name": "孙中辉", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "青冈县人民政府副县长", "current_org": "青冈县人民政府",
     "source": "http://www.qgnet.gov.cn/qg/zyhy/202607/c12_238204.shtml"},
    # 6 — 王昊 — 县委常委、县人武部政委
    {"id": 6, "name": "王昊", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "青冈县委常委、县人武部政委", "current_org": "青冈县人民武装部",
     "source": "http://www.qgnet.gov.cn/qg/qgyw/202607/c12_238688.shtml"},
    # 7 — 李永 — 县人武部部长
    {"id": 7, "name": "李永", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "青冈县人武部部长", "current_org": "青冈县人民武装部",
     "source": "http://www.qgnet.gov.cn/qg/qgyw/202607/c12_238688.shtml"},
    # 8 — 郑秀艳 — 县人大常委会副主任
    {"id": 8, "name": "郑秀艳", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "青冈县人大常委会副主任", "current_org": "青冈县人民代表大会常务委员会",
     "source": "http://www.qgnet.gov.cn/qg/qgyw/202607/c12_238688.shtml"},
    # 9 — 商淑红 — 县政协副主席
    {"id": 9, "name": "商淑红", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "政协青冈县委员会副主席", "current_org": "政协青冈县委员会",
     "source": "http://www.qgnet.gov.cn/qg/zyhy/202607/c12_238204.shtml"},
    # 10 — 韩雪松 — 绥化市委书记（市级关联）
    {"id": 10, "name": "韩雪松", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "中共绥化市委书记", "current_org": "中共绥化市委员会",
     "source": "https://www.suihua.gov.cn/sh/bdyw/202607/c12_238427.shtml"},
    # 11 — 陈立军 — 绥化市市长（市级关联）
    {"id": 11, "name": "陈立军", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "绥化市委副书记、绥化市人民政府市长", "current_org": "绥化市人民政府",
     "source": "https://www.suihua.gov.cn/sh/bdyw/202607/c12_237876.shtml"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 现任核心党政领导
    {"person_id": 1, "org_id": 1, "title": "中共青冈县委书记", "start": "unknown", "end": "present", "rank": "正县处级", "note": "2026-07 在职（官方，前任待查）；接任前职务待核"},
    {"person_id": 2, "org_id": 1, "title": "中共青冈县委副书记", "start": "", "end": "present", "rank": "副县处级", "note": "2026 在职（官方）"},
    {"person_id": 2, "org_id": 2, "title": "青冈县人民政府县长", "start": "unknown", "end": "present", "rank": "正县处级", "note": "2026-07/08 在职；县防汛抗旱指挥部总指挥长；任县长前职务与到任时间待核"},
    # 县政府班子
    {"person_id": 3, "org_id": 1, "title": "中共青冈县委委员、常委", "start": "", "end": "present", "rank": "副县处级", "note": "2026-08 在职"},
    {"person_id": 3, "org_id": 2, "title": "青冈县人民政府副县长", "start": "", "end": "present", "rank": "副县处级", "note": "2026-08 防汛调研陪同县长"},
    {"person_id": 4, "org_id": 2, "title": "青冈县人民政府副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "青冈县人民政府副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    # 人武部
    {"person_id": 6, "org_id": 6, "title": "青冈县人武部政治委员（县委常委）", "start": "", "end": "present", "rank": "副县处级", "note": "2026-07 随县委书记慰问官兵"},
    {"person_id": 7, "org_id": 6, "title": "青冈县人武部部长", "start": "", "end": "present", "rank": "副县处级", "note": "2026-07 随县委书记慰问官兵"},
    # 人大 / 政协
    {"person_id": 8, "org_id": 3, "title": "青冈县人大常委会副主任", "start": "", "end": "present", "rank": "副县处级", "note": "2026-07 随县委书记慰问官兵"},
    {"person_id": 9, "org_id": 4, "title": "政协青冈县委员会副主席", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    # 关联市领导
    {"person_id": 10, "org_id": 7, "title": "中共绥化市委书记", "start": "", "end": "present", "rank": "正地厅级", "note": "2026 多次到青冈县调研"},
    {"person_id": 11, "org_id": 7, "title": "中共绥化市委副书记", "start": "", "end": "present", "rank": "副地厅级", "note": "2026 多次到青冈县调研"},
    {"person_id": 11, "org_id": 8, "title": "绥化市人民政府市长", "start": "", "end": "present", "rank": "正地厅级", "note": "2026-05/06/07 多次到青冈县督导"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    # 核心党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "孙国文（县委书记）与马庆宝（县委副书记、县长）为青冈县现任党政主要领导搭档",
     "overlap_org": "青冈县", "overlap_period": "2026至今"},
    # 书记-常委副职
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "孙国文（县委书记）与王洪伟（县委常委、副县长）同在县委常委会组成班子",
     "overlap_org": "中共青冈县委员会", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "孙国文（县委书记）与王昊（县委常委、县人武部政委）同出席八一走访慰问活动",
     "overlap_org": "青冈县", "overlap_period": "2026-07"},
    # 县长与副职
    {"person_a": 2, "person_b": 3, "type": "上下级",
     "context": "马庆宝（县委副书记、县长）与王洪伟（县委常委、副县长）防汛调研共事",
     "overlap_org": "青冈县人民政府", "overlap_period": "2026-08"},
    {"person_a": 2, "person_b": 4, "type": "上下级",
     "context": "马庆宝（县长）与王秀鹏（副县长）同在县政府班子",
     "overlap_org": "青冈县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "上下级",
     "context": "马庆宝（县长）与孙中辉（副县长）同在县政府班子",
     "overlap_org": "青冈县人民政府", "overlap_period": "2026"},
    # 书记-市级
    {"person_a": 1, "person_b": 10, "type": "上下级",
     "context": "绥化市委书记韩雪松到青冈县调研时听取县委书记孙国文工作汇报（上下级）",
     "overlap_org": "绥化市/青冈县", "overlap_period": "2026-05/07"},
    # 县长-市级
    {"person_a": 2, "person_b": 11, "type": "上下级",
     "context": "绥化市市长陈立军多次到青冈县调研督导（县长马庆宝汇报）",
     "overlap_org": "绥化市/青冈县", "overlap_period": "2026-05/06/07"},
    # 人武部内部
    {"person_a": 6, "person_b": 7, "type": "同事",
     "context": "王昊（县人武部政委）与李永（县人武部部长）为人武部军政搭档",
     "overlap_org": "青冈县人民武装部", "overlap_period": "2026"},
    # 人大/政协与县政府
    {"person_a": 8, "person_b": 9, "type": "同事",
     "context": "郑秀艳（人大副主任）与商淑红（政协副主席）同出席县内活动（机构交叉笔误待核）",
     "overlap_org": "青冈县", "overlap_period": "2026"},
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
    )
    import os as _os
    print(f"Built 青冈县 network: db={_os.path.abspath(DB_PATH)} gexf={_os.path.abspath(GEXF_PATH)}")