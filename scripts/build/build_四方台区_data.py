#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 四方台区 leadership network.

四方台区隶属黑龙江省双鸭山市，位于市区东南部，是双鸭山市四个市辖区之一，
东部与尖山区相连。主要产业包括煤炭、农业（太保镇等）。区委、区政府负责
全区党建、经济发展、社会建设等。

Current leadership as of 2026-08 (sources: 双鸭山市四方台区人民政府官网
www.syssft.gov.cn 官方"领导视窗" + 各领导简介页):
- 区委书记: 于立国（2022.04 至今，官方简历确认）
- 区委副书记、区长: 刘鹏（2021.12 至今，官方简历确认）
- 区委副书记、政法委书记: 王丹（2023.12 至今）
- 区委常委、副区长: 徐文韬、孟凡智
- 区委常委、纪委书记、监委主任: 佟伟新
- 区人大常委会主任: 刘长国（2026.03 至今）
- 区政协主席: 李景林（2018.08 至今）
- 区政府副区长: 曲志峰（兼公安分局局长）

关系网络要点（均来自官方简历，confirmed）：
- 党政主轴: 于立国(书记) – 刘鹏(区长)
- 纪委体系交接: 王丹(区纪委书记 2021-2023) → 佟伟新(区纪委书记 2024 至今)
- 市委组织部体系: 于立国、王丹、徐文韬、刘长国曾任职双鸭山市委组织部/市纪委监委
- 区县干部交流: 曲志峰(市公安局)、孟凡智(宝清县)、徐文韬(友谊/市政府办)
"""

import os
import sqlite3  # noqa: F401
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

SLUG = "四方台区"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "四方台区_network.db")
    GEXF_PATH = os.path.join(_STAGING, "四方台区_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "四方台区_network.db"
    GEXF_PATH = GRAPH_DIR / "四方台区_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共四方台区委员会", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市四方台区"},
    {"id": 2, "name": "四方台区人民政府", "type": "政府", "level": "县处级", "parent": "双鸭山市人民政府", "location": "黑龙江省双鸭山市四方台区"},
    {"id": 3, "name": "四方台区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "双鸭山市人大常委会", "location": "黑龙江省双鸭山市四方台区"},
    {"id": 4, "name": "中国人民政治协商会议四方台区委员会", "type": "政协", "level": "县处级", "parent": "双鸭山市政协", "location": "黑龙江省双鸭山市四方台区"},
    {"id": 5, "name": "中共四方台区纪律检查委员会/四方台区监察委员会", "type": "纪委", "level": "副县处级", "parent": "中共双鸭山市纪委", "location": "黑龙江省双鸭山市四方台区"},
    {"id": 6, "name": "四方台区太保镇", "type": "乡镇", "level": "正科级", "parent": "四方台区人民政府", "location": "黑龙江省双鸭山市四方台区太保镇"},
    {"id": 7, "name": "双鸭山市公安局四方台公安分局", "type": "政府", "level": "副县处级", "parent": "双鸭山市公安局", "location": "黑龙江省双鸭山市四方台区"},
    {"id": 8, "name": "双鸭山市委组织部", "type": "党委部门", "level": "正处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市"},
    {"id": 9, "name": "中共宝山区委", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市宝山区"},
    {"id": 10, "name": "中共饶河县委", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市饶河县"},
    {"id": 11, "name": "双鸭山市乡村振兴局", "type": "政府", "level": "正处级", "parent": "双鸭山市人民政府", "location": "黑龙江省双鸭山市"},
    {"id": 12, "name": "双鸭山市扶贫开发办公室", "type": "政府", "level": "正处级", "parent": "双鸭山市人民政府", "location": "黑龙江省双鸭山市"},
    {"id": 13, "name": "黑龙江省人民政府办公厅", "type": "政府", "level": "省厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省哈尔滨市"},
    {"id": 14, "name": "黑龙江省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "黑龙江省哈尔滨市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 于立国 — 区委书记（现任）
    {"id": 1, "name": "于立国", "gender": "男", "ethnicity": "汉族", "birth": "1972年7月", "birthplace": "待查",
     "education": "佳木斯师范专科学校（体育教育）；省教育学院（教育管理）；黑龙江大学（法学函授）",
     "party_join": "1995年5月入党", "work_start": "1995年7月",
     "current_post": "四方台区委书记、一级调研员", "current_org": "中共四方台区委员会",
     "source": "http://www.syssft.gov.cn/sft/283/202604/c07_246948.shtml"},
    # 2 — 刘鹏 — 区委副书记、区长（现任）
    {"id": 2, "name": "刘鹏", "gender": "男", "ethnicity": "汉族", "birth": "1980年8月", "birthplace": "待查",
     "education": "哈尔滨工业大学市政工程系给水排水工程（本科）",
     "party_join": "2005年7月入党", "work_start": "2003年9月",
     "current_post": "四方台区委副书记、区长、区政府党组书记", "current_org": "四方台区人民政府",
     "source": "http://www.syssft.gov.cn/sft/285/202604/c07_246928.shtml"},
    # 3 — 王丹 — 区委副书记、政法委书记（现任）
    {"id": 3, "name": "王丹", "gender": "女", "ethnicity": "汉族", "birth": "1978年9月", "birthplace": "待查",
     "education": "黑龙江大学法律专业（在职本科）",
     "party_join": "1999年4月入党", "work_start": "1999年8月",
     "current_post": "区委副书记、政法委书记、二级调研员", "current_org": "中共四方台区委员会",
     "source": "http://www.syssft.gov.cn/sft/283/202604/c07_246946.shtml"},
    # 4 — 徐文韬 — 区委常委、副区长（现任）
    {"id": 4, "name": "徐文韬", "gender": "男", "ethnicity": "汉族", "birth": "1986年9月", "birthplace": "待查",
     "education": "国家开放大学行政管理",
     "party_join": "2005年6月入党", "work_start": "2008年7月",
     "current_post": "区委常委、副区长、三级调研员", "current_org": "四方台区人民政府",
     "source": "http://www.syssft.gov.cn/sft/283/202604/c07_246944.shtml"},
    # 5 — 孟凡智 — 区委常委、副区长（现任）
    {"id": 5, "name": "孟凡智", "gender": "男", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查",
     "education": "东北农业大学工商管理（大专）",
     "party_join": "中共党员", "work_start": "2004年7月",
     "current_post": "区委常委、副区长", "current_org": "四方台区人民政府",
     "source": "http://www.syssft.gov.cn/sft/283/202604/c07_246943.shtml"},
    # 6 — 佟伟新 — 区委常委、纪委书记（现任）
    {"id": 6, "name": "佟伟新", "gender": "男", "ethnicity": "汉族", "birth": "1975年2月", "birthplace": "待查",
     "education": "辽宁警官高等专科学校；省委党校研究生",
     "party_join": "2007年3月入党", "work_start": "1997年7月",
     "current_post": "区委常委、纪委书记、监委主任", "current_org": "中共四方台区纪律检查委员会",
     "source": "http://www.syssft.gov.cn/sft/284/202604/c06_246941.shtml"},
    # 7 — 刘长国 — 区人大常委会主任（现任）
    {"id": 7, "name": "刘长国", "gender": "男", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查",
     "education": "黑龙江大学法律（自考本科）",
     "party_join": "中共党员", "work_start": "2005年7月",
     "current_post": "区人大常委会党组书记、主任", "current_org": "四方台区人民代表大会常务委员会",
     "source": "http://www.syssft.gov.cn/sft/284/202604/c07_246918.shtml"},
    # 8 — 李景林 — 区政协主席（现任）
    {"id": 8, "name": "李景林", "gender": "男", "ethnicity": "汉族", "birth": "1970年5月", "birthplace": "待查",
     "education": "大专",
     "party_join": "1996年4月入党", "work_start": "1991年7月",
     "current_post": "四方台区政协主席", "current_org": "中国人民政治协商会议四方台区委员会",
     "source": "http://www.syssft.gov.cn/sft/286/202604/c07_247005.shtml"},
    # 9 — 曲志峰 — 副区长、公安分局局长（现任）
    {"id": 9, "name": "曲志峰", "gender": "男", "ethnicity": "汉族", "birth": "1978年4月", "birthplace": "待查",
     "education": "国家开放大学法学（函授本科）",
     "party_join": "2005年6月入党", "work_start": "2000年7月",
     "current_post": "区政府党组成员、副区长、公安分局局长", "current_org": "四方台区人民政府",
     "source": "http://www.syssft.gov.cn/sft/285/202604/c00_246924.shtml"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 于立国
    {"person_id": 1, "org_id": 1, "title": "四方台区委书记、一级调研员", "start": "2022.04", "end": "present", "rank": "正处级", "note": "官方简历确认，2022.04至今"},
    {"person_id": 1, "org_id": 10, "title": "饶河县委常委、纪委书记", "start": "2015.12", "end": "2017.11", "rank": "副处级", "note": "此前曾任"},
    {"person_id": 1, "org_id": 9, "title": "宝山区委常委、纪委书记", "start": "2008.10", "end": "2015.12", "rank": "副处级", "note": "此前曾任"},
    {"person_id": 1, "org_id": 11, "title": "双鸭山市乡村振兴局局长、党组书记", "start": "2021.07", "end": "2022.04", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "双鸭山市扶贫开发办公室主任、党组书记", "start": "2017.11", "end": "2021.07", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "双鸭山市委组织部干部（2001-2008）", "start": "2001.03", "end": "2008.10", "rank": "", "note": "科员→综合信息科科长→干部监督科科长"},
    # 刘鹏
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长、区政府党组书记", "start": "2021.12", "end": "present", "rank": "正处级", "note": "2021.12至今"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "2020.08", "end": "present", "rank": "副处级", "note": "2020.08起任区委副书记"},
    {"person_id": 2, "org_id": 6, "title": "太保镇党委书记", "start": "2020.10", "end": "2021.09", "rank": "正科级", "note": "兼任"},
    {"person_id": 2, "org_id": 13, "title": "省政府办公厅干部", "start": "2013.09", "end": "2017.08", "rank": "", "note": "政务公开/企业投诉管理办"},
    # 王丹
    {"person_id": 3, "org_id": 1, "title": "区委副书记、政法委书记", "start": "2023.12", "end": "present", "rank": "副县处级", "note": "2023.12至今"},
    {"person_id": 3, "org_id": 5, "title": "区委常委、纪委书记、监委主任", "start": "2021.10", "end": "2023.11", "rank": "副县处级", "note": "2021-2023任区纪委书记，后佟伟新继任"},
    {"person_id": 3, "org_id": 8, "title": "市委组织部/市委巡察办干部", "start": "2005.07", "end": "2021.10", "rank": "", "note": "人才科→考评办科长→市委巡察办副主任"},
    # 徐文韬
    {"person_id": 4, "org_id": 2, "title": "区委常委、副区长", "start": "2025.04", "end": "present", "rank": "副处级", "note": "2025至今"},
    {"person_id": 4, "org_id": 8, "title": "双鸭山市委组织部研究室主任", "start": "2016.12", "end": "2021.07", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "友谊县东建乡党委书记", "start": "2020.05", "end": "2021.07", "rank": "正科级", "note": ""},
    # 孟凡智
    {"person_id": 5, "org_id": 2, "title": "区委常委、副区长", "start": "2026.01", "end": "present", "rank": "副处级", "note": "2026.01至今"},
    {"person_id": 5, "org_id": 9, "title": "宝清县委常委、统战部部长", "start": "2021.12", "end": "2025.12", "rank": "副处级", "note": "来自宝清县"},
    # 佟伟新
    {"person_id": 6, "org_id": 5, "title": "区委常委、纪委书记、监委主任", "start": "2024.01", "end": "present", "rank": "副县处级", "note": "2024.01至今"},
    {"person_id": 6, "org_id": 8, "title": "双鸭山市纪委监委监督检查室主任", "start": "2019.09", "end": "2023.11", "rank": "", "note": ""},
    # 刘长国
    {"person_id": 7, "org_id": 3, "title": "区人大常委会党组书记、主任", "start": "2026.03", "end": "present", "rank": "正处级", "note": "2026.03至今"},
    {"person_id": 7, "org_id": 1, "title": "区委常委、组织部部长、统战部部长", "start": "2021.11", "end": "2026.02", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 8, "title": "双鸭山市委组织部/市纪委监委组织部", "start": "2005", "end": "2021.11", "rank": "", "note": "干部二科/人才科科长、市纪委监委组织部部长"},
    # 李景林
    {"person_id": 8, "org_id": 4, "title": "四方台区政协主席", "start": "2018.08", "end": "present", "rank": "正处级", "note": "2018.08至今"},
    {"person_id": 8, "org_id": 8, "title": "尖山区纪委书记/市纪委常委", "start": "2006.10", "end": "2018.06", "rank": "副处级", "note": ""},
    # 曲志峰
    {"person_id": 9, "org_id": 2, "title": "副区长（兼公安分局局长）", "start": "2025.08", "end": "present", "rank": "副处级", "note": "2025.08至今"},
    {"person_id": 9, "org_id": 7, "title": "双鸭山市公安局四方分局局长", "start": "2025.08", "end": "present", "rank": "", "note": ""},
    {"person_id": 9, "org_id": 8, "title": "双鸭山市公安局办公室主任", "start": "2023.06", "end": "2025.08", "rank": "", "note": ""},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "于立国（区委书记）与刘鹏（区委副书记、区长）为现任党政一把手，同一区委班子共事", "overlap_org": "四方台区", "overlap_period": "2022.04至今"},
    # 区委领导班子内部
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "于立国任区委书记，王丹任区委副书记、政法委书记，上下级共事", "overlap_org": "四方台区委", "overlap_period": "2023.12至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "于立国（区委书记）与佟伟新（区纪委书记）同区党委书记下共事", "overlap_org": "四方台区委", "overlap_period": "2024至今"},
    # 纪委交接
    {"person_a": 3, "person_b": 6, "type": "前任继任", "context": "王丹先任区纪委书记（2021-2023），佟伟新后任区纪委书记（2024至今），岗位交接", "overlap_org": "四方台区纪委", "overlap_period": "2023-2024"},
    # 区委副书记平级
    {"person_a": 2, "person_b": 3, "type": "平级", "context": "刘鹏（副书记/区长）与王丹（副书记/政法委书记）同为四方台区委副书记", "overlap_org": "四方台区委", "overlap_period": "2023.12至今"},
    # 区政府内部
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "刘鹏区长与副区长徐文韬共事", "overlap_org": "四方台区人民政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "刘鹏区长与副区长孟凡智共事", "overlap_org": "四方台区人民政府", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "刘鹏区长与副区长曲志峰共事", "overlap_org": "四方台区人民政府", "overlap_period": "2025至今"},
    # 人大/政协关联
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "四方台区委书记于立国与区人大常委会主任刘长国同台履职", "overlap_org": "四方台区", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "刘鹏区长向人代会作政府工作报告", "overlap_org": "四方台区", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 8, "type": "同场公职", "context": "区委书记于立国与政协主席李景林同台履职", "overlap_org": "四方台区", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 8, "type": "同场公职", "context": "区长刘鹏与政协主席李景林同席会议", "overlap_org": "四方台区", "overlap_period": "至今"},
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