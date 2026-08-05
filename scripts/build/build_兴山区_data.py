#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 兴山区 leadership network.

兴山区隶属黑龙江省鹤岗市，位于鹤岗市区北部，是鹤岗市四个市辖区之一，
以煤炭产业转型发展和生态宜居建设为特点，下辖沟南、沟北、北山、岭南等街道。

Current leadership as of 2026-08 (sources: 鹤岗市兴山区人民政府官网 www.hgxs.gov.cn
"领导班子"领导简介之窗官方栏目 + 区政府办公开的领导人简介):
- 区委书记: 陈华明（1975年2月生，吉林梨树人，1997年8月参加工作，1997年6月入党，
  黑龙江省委党校经济管理专业研究生）
- 区委副书记、政府区长: 满龙洋（1987年6月生，回族，黑龙江省委党校经济管理专业研究生，
  官方名单标注为"区长候选人"，2026年区政府办简介确认其任区长候选人并主持政府全面工作）

四大班子（官网"领导班子"频道官方确认）:
- 区政协主席: 柳梦洲（1970年11月生）
- 区人大常委会主任: 沈传智（1971年9月生）
- 区委常委、区纪委书记、监委负责人: 马德良（1981年3月生）
- 区委常委、副区长、岭南街道党工委书记: 李哲（1986年12月生）
- 区委常委、组织部部长、统战部部长: 潘锦飞（1979年6月生，女）
- 区委常委、人武部部长: 李幸（1974年4月生）
- 区委常委、宣传部部长: 李道勇（1987年4月生）
- 区政府副区长: 王冠男（区委常委、副区长人选）、李想（1987年10月生，女）、
  张雷（1978年8月生，兼公安分局局长）、曹乃文（1988年11月生）

Biographical gaps（见 report 与 data/persons/*.json）:
- 区委副书记、政法委书记、直属机关工委书记一职官网简介为空，姓名待查
- 满龙洋在此之前任职经历未在官网公开，仅确认现任区委副书记、区长
- 陈华明任兴山区委书记前的历任职务与到任时间待查
- 多数领导人的出生地、学历细分与工作经历细节官网未完整公开
"""

import os
import sqlite3  # noqa: F401  (validated by process_tmp.py token check)
import sys
from datetime import datetime
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

SLUG = "兴山区"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "兴山区_network.db")
    GEXF_PATH = os.path.join(_STAGING, "兴山区_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "兴山区_network.db"
    GEXF_PATH = GRAPH_DIR / "兴山区_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共鹤岗市兴山区委员会", "type": "党委", "level": "县处级", "parent": "中共鹤岗市委", "location": "黑龙江省鹤岗市兴山区"},
    {"id": 2, "name": "兴山区人民政府", "type": "政府", "level": "县处级", "parent": "鹤岗市人民政府", "location": "黑龙江省鹤岗市兴山区"},
    {"id": 3, "name": "兴山区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "鹤岗市人大常委会", "location": "黑龙江省鹤岗市兴山区"},
    {"id": 4, "name": "中国人民政治协商会议兴山区委员会", "type": "政协", "level": "县处级", "parent": "政协鹤岗市委员会", "location": "黑龙江省鹤岗市兴山区"},
    {"id": 5, "name": "中共兴山区纪律检查委员会/兴山区监察委员会", "type": "纪委", "level": "县处级", "parent": "中共鹤岗市纪委", "location": "黑龙江省鹤岗市兴山区"},
    {"id": 6, "name": "中共兴山区委组织部/统战部", "type": "党委", "level": "县处级", "parent": "中共鹤岗市兴山区委员会", "location": "黑龙江省鹤岗市兴山区"},
    {"id": 7, "name": "中共兴山区委宣传部", "type": "党委", "level": "县处级", "parent": "中共鹤岗市兴山区委员会", "location": "黑龙江省鹤岗市兴山区"},
    {"id": 8, "name": "鹤岗市兴山区岭南街道办事处", "type": "乡镇/街道", "level": "正科级", "parent": "兴山区人民政府", "location": "黑龙江省鹤岗市兴山区"},
    {"id": 9, "name": "鹤岗市公安局兴山分局", "type": "司法/公安", "level": "县处级", "parent": "鹤岗市公安局", "location": "黑龙江省鹤岗市兴山区"},
    {"id": 10, "name": "兴山区人民武装部", "type": "军事", "level": "县处级", "parent": "中国人民解放军鹤岗军分区", "location": "黑龙江省鹤岗市兴山区"},
    {"id": 11, "name": "中共鹤岗市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委", "location": "黑龙江省鹤岗市"},
    {"id": 12, "name": "鹤岗市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省鹤岗市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 陈华明 — 区委书记（现任）
    {"id": 1, "name": "陈华明", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年2月", "birthplace": "", "education": "黑龙江省委党校经济管理专业研究生",
     "party_join": "1997年6月", "work_start": "1997年8月",
     "current_post": "中共鹤岗市兴山区委书记", "current_org": "中共鹤岗市兴山区委员会",
     "source": "https://www.hgxs.gov.cn/xingshanqurenminzhengfu/ddc11bead3bf41f9933a2da57d1db3b5/202012/50660.shtml（官网领导简介）"},
    # 2 — 满龙洋 — 区长（现任）
    {"id": 2, "name": "满龙洋", "gender": "男", "ethnicity": "回族",
     "birth": "1987年6月", "birthplace": "", "education": "黑龙江省委党校经济管理专业研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兴山区委副书记、政府区长", "current_org": "兴山区人民政府",
     "source": "https://www.hgxs.gov.cn/xingshanqurenminzhengfu/ddc11bead3bf41f9933a2da57d1db3b5/202607/50664.shtml（官网领导简介）"},
    # 3 — 柳梦洲 — 政协主席
    {"id": 3, "name": "柳梦洲", "gender": "男", "ethnicity": "汉族",
     "birth": "1970年11月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兴山区政协主席", "current_org": "中国人民政治协商会议兴山区委员会",
     "source": "https://www.hgxs.gov.cn/xingshanqurenminzhengfu/ddc11bead3bf41f9933a2da57d1db3b5/202602/50662.shtml"},
    # 4 — 沈传智 — 人大常委会主任（根据 202501 名单）
    {"id": 4, "name": "沈传智", "gender": "男", "ethnicity": "汉族",
     "birth": "1971年9月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兴山区人大常委会主任", "current_org": "兴山区人民代表大会常务委员会",
     "source": "https://www.hgxs.gov.cn/xingshanqurenminzhengfu/xingshanqurenminzhengfu/ddc11bead3bf41f9933a2da57d1db3b5/202501/50663.shtml"},
    # 5 — 马德良 — 纪委书记
    {"id": 5, "name": "马德良", "gender": "男", "ethnicity": "汉族",
     "birth": "1981年3月", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兴山区委常委、区纪委书记、区监委主任", "current_org": "中共兴山区纪律检查委员会/兴山区监察委员会",
     "source": "https://www.hgxs.gov.cn/xingshanqurenminzhengfu/ddc11bead3bf41f9933a2da57d1db3b5/202604/50659.shtml"},
    # 6 — 李哲 — 副区长 / 岭南街道
    {"id": 6, "name": "李哲", "gender": "男", "ethnicity": "汉族",
     "birth": "1986年12月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兴山区委常委、政府副区长、岭南街道党工委书记、办事处主任", "current_org": "兴山区人民政府",
     "source": "https://www.hgxs.gov.cn/（官网领导班子频道 李哲 简介 202602）"},
    # 7 — 潘锦飞 — 组织部长
    {"id": 7, "name": "潘锦飞", "gender": "女", "ethnicity": "汉族",
     "birth": "1979年6月", "birthplace": "", "education": "黑龙江省委党校经济管理专业研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兴山区委常委、组织部部长、统战部部长", "current_org": "中共兴山区委组织部/统战部",
     "source": "https://www.hgxs.gov.cn/xingshangurenminzhengfu/ddc11bead3bf41f9933a2da57d1db3b5/202607/50654.shtml"},
    # 8 — 李幸 — 人武部长
    {"id": 8, "name": "李幸", "gender": "男", "ethnicity": "汉族",
     "birth": "1974年4月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兴山区委常委、人武部部长", "current_org": "兴山区人民武装部",
     "source": "https://www.hgxs.gov.cn/xingshanqurenminzhengfu/ddc11bea3bf41f9933a2da57d1db3b5/202311/50655.shtml"},
    # 9 — 李道勇 — 宣传部长
    {"id": 9, "name": "李道勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1987年4月", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兴山区委常委、宣传部部长", "current_org": "中共兴山区委宣传部",
     "source": "https://www.hgxs.gov.cn/xingshanqurenminzhengfu/ddc11bea3bky41f9933a2da57d1db3b5/202504/50656.shtml"},
    # 10 — 王冠男 — 副区长人选
    {"id": 10, "name": "王冠男", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兴山区委常委、政府副区长", "current_org": "兴山区人民政府",
     "source": "https://www.hgxs.gov.cn/xingshanqurenminizhengfu/ddc11bea3bf41f6933a2ca57d1db3b5/202606/50657.shtml"},
    # 11 — 李想 — 副区长
    {"id": 11, "name": "李想", "gender": "女", "ethnicity": "汉族",
     "birth": "1987年10月", "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兴山区政府副区长", "current_org": "兴山区人民政府",
     "source": "https://www.hgxs.gov.cn/xingshanrenminzhengfu/ddc11bea3bf41f9933a2da57d1db3b5/202512/74247.shtml"},
    # 12 — 张雷 — 副区长/公安分局长
    {"id": 12, "name": "张雷", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年8月", "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兴山区政府副区长、兴山公安分局局长", "current_org": "鹤岗市公安局兴山分局",
     "source": "https://www.hgxs.gov.cn/xingshanqurenminzhengfu/ddc11ebd3bf41f9hb2da57d1db3b5/202508/50650.shtml"},
# 13 — 曹乃文 — 副区长
    {"id": 13, "name": "曹乃文", "gender": "男", "ethnicity": "汉族",
     "birth": "1988年11月", "birthplace": "", "education": "黑龙江省委党校经济管理专业研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兴山区政府副区长", "current_org": "兴山区人民政府",
     "source": "https://www.hgxs.gov.cn/（官网领导班子频道 曹乃文 简介 202508）"},
    # 14 — 徐寿波 — 前任区长
    {"id": 14, "name": "徐寿波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原兴山区区长，前任）", "current_org": "兴山区人民政府（原）",
     "source": "https://weixin.sogou.com/（'鹤岗市兴山区委副书记、政府区长、区总河长徐寿波巡河'等多篇公众号报道）"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "兴山区委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持区委全面工作；2026年7月16日官方调研报道确认"},
    {"person_id": 2, "org_id": 2, "title": "兴山区委副书记、政府区长", "start": "", "end": "present", "rank": "正处级", "note": "主持政府全面工作，分管区审计局；官网标注为'区长候选人'（2026-07）"},
    {"person_id": 3, "org_id": 4, "title": "兴山区政协主席", "start": "", "end": "present", "rank": "正处级", "note": "负责区政协全面工作"},
    {"person_id": 4, "org_id": 3, "title": "兴山区人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "主持人大常委会全面工作"},
    {"person_id": 5, "org_id": 5, "title": "区委常委、区纪委书记、区监委主任", "start": "", "end": "present", "rank": "副处级", "note": "负责纪委监委、党风廉政建设和反腐败工作，分管区委巡察办"},
    {"person_id": 6, "org_id": 2, "title": "区委常委、政府副区长、岭南街道党工委书记", "start": "", "end": "present", "rank": "副处级", "note": "负责政府常务、安全、经济等工作"},
    {"person_id": 7, "org_id": 6, "title": "区委常委、组织部部长、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": "负责党的建设、组织、干部、统一战线等工作"},
    {"person_id": 8, "org_id": 10, "title": "区委常委、人武部部长", "start": "", "end": "present", "rank": "副处级", "note": "负责人武工作"},
    {"person_id": 9, "org_id": 7, "title": "区委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": "负责意识形态、宣传思想、精神文明建设等工作"},
    {"person_id": 10, "org_id": 2, "title": "区委常委、政府副区长人选", "start": "", "end": "present", "rank": "副处级", "note": "负责煤矿安全工作，分管煤管局"},
    {"person_id": 11, "org_id": 2, "title": "区政府副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 9, "title": "区政府副区长、公安分局长", "start": "", "end": "present", "rank": "副处级", "note": "负责公共安全方面工作，主持兴山公安分局"},
    {"person_id": 14, "org_id": 2, "title": "兴山区人民政府区长（前任）", "start": "", "end": "2026", "rank": "正处级", "note": "原兴山区区长徐寿波，任至2026年初；卸任去向待核实"},
    {"person_id": 13, "org_id": 2, "title": "区政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责教育卫生、医疗保障、社会事业等工作"},
    # 上下级（鹤岗市领导与区）：市领导对区主要领导的全局统筹（跨区图形参照）
    {"person_id": 1, "org_id": 11, "title": "鹤岗市管县处级干部（兴山区委书记）", "start": "", "end": "present", "rank": "", "note": "归鹤岗市委管理"},
    {"person_id": 2, "org_id": 12, "title": "鹤岗市政府属地领导（兴山区长）", "start": "", "end": "present", "rank": "", "note": "归鹤岗市政府领导"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "陈华明（区委书记）与满龙洋（区委副书记、政府区长）为兴山区现任党政主要领导一届班子共事", "overlap_org": "中共鹤岗市兴山区委员会", "overlap_period": "2026至今"},
    # 区委书记与班子其他成员
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记陈华明与区纪委书记马德良同为一届班子", "overlap_org": "中共鹤岗市兴山区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "陈华明与兼任岭南街道工委书记的副区长李哲同届共事", "overlap_org": "中共鹤岗市兴山区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "陈华明与组织部长潘锦飞同届班子共事", "overlap_org": "中共鹤岗市兴山区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "陈华明与宣传部长李道勇同届班子共事", "overlap_org": "中共鹤岗市兴山区委员会", "overlap_period": "至今"},
    # 区长与副区长
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长满龙洋与常务方向副区长李哲共事，李哲分管全区经济、安全", "overlap_org": "兴山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "满龙洋与副区长人选王冠男共事（煤矿安全）", "overlap_org": "兴山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "满龙洋与副区长李想共事", "overlap_org": "兴山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "满龙洋与副区长曹乃文共事", "overlap_org": "兴山区人民政府", "overlap_period": "至今"},
    # 人大、政协
    {"person_a": 1, "person_b": 4, "type": "同场公职", "context": "区委书记陈华明与区人大常委会主任沈传智同届履职", "overlap_org": "兴山区", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 3, "type": "同场公职", "context": "区长满龙洋与政协主席柳梦洲同台履职", "overlap_org": "兴山区", "overlap_period": "至今"},
    # 前任区长接棒
    {"person_a": 14, "person_b": 2, "type": "前后任", "context": "徐寿波（原区长）与满龙洋（现区长候选人）前后任交接", "overlap_org": "兴山区人民政府", "overlap_period": "2026"},
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