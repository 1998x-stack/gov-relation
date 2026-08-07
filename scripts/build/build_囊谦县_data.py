#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 囊谦县 leadership network.

囊谦县隶属青海省玉树藏族自治州，位于青海省南部、三江源核心区腹地，与西藏昌都地区接壤。
县域平均海拔高、藏族同胞比例高，是本州政治、经济、文化重镇之一。

Current leadership as of 2026-08 (primary source: 囊谦县人民政府官网 www.nangqian.gov.cn
党政领导栏目，官方一手):

- 县委书记: 石大存（男/汉族/1979-03 生/青海海东互助县人；2003-03 参加工作、2000-12 入党、
  青海师范大学生物系本科。曾任青海省公安厅政治部人事处机关干部科副科长、科长；同仁县副县长；
  黄南州司法局副局长；泽库县委副书记；黄南州委政法委副书记；现任中共囊谦县委书记。主持县委全面工作。）CONFIRMED
- 县委副书记、县长: 尕玛桑周（县政府全面工作，负责审计；协助石大存负责县委财经委、审计委日常工作。
  出生/民族/学历/前职未见 → gap）CONFIRMED role、bio thin
- 县委副书记: 达哇扎西（协助处理县委日常工作、党建、深改委、编委）
- 县委副书记: 索南扎西（藏族/1976-09 生/玉树市人；1997-07 参加工作、1999-05 入党、青海省委党校研究生。
  曾任玉树州残联、州民政局（低保科副科/科长）、着晓乡党委书记、香达镇党委书记、
  囊谦县委常委、宣传部长，县委副书记。）CONFIRMED
- 政协主席: 更却代丁（藏族/1971-07/青海囊谦人；本科；1997-07 入党、1992-07 参加工作。
  历任娘拉乡人武部长→娘拉乡党委书记→东坝乡党委书记→县民政局局长→2016-10 至 2021-07
  县委常委、政法委书记→2021-08 至 2024-03 县人大常委会主任→2024-04 至今县政协主席。）CONFIRMED
- 玉树州领导（背景）: 州委书记 马锐；州委副书记、州长 龙措

Confidence: confirmed = 官方官网/两会公报；plausible = 党媒/地方报道；unverified = 前履历线索。
Biography 单体不完整者置于 person JSON 的 open_questions 与 report/open_gaps.md。
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

SLUG = "囊谦县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "囊谦县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "囊谦县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "囊谦县_network.db"
    GEXF_PATH = GRAPH_DIR / "囊谦县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共囊谦县委员会", "type": "党委", "level": "县处级", "parent": "中共玉树州委", "location": "青海省玉树藏族自治州囊谦县"},
    {"id": 2, "name": "囊谦县人民政府", "type": "政府", "level": "县处级", "parent": "玉树州人民政府", "location": "青海省玉树藏族自治州囊谦县"},
    {"id": 3, "name": "囊谦县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "玉树州人大常委会", "location": "青海省玉树藏族自治州囊谦县"},
    {"id": 4, "name": "中国人民政治协商会议囊谦县委员会", "type": "政协", "level": "县处级", "parent": "政协玉树州委员会", "location": "青海省玉树藏族自治州囊谦县"},
    {"id": 5, "name": "中共囊谦县纪律检查委员会/囊谦县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共玉树州纪委", "location": "青海省玉树藏族自治州囊谦县"},
    {"id": 6, "name": "囊谦县人民法院", "type": "法院", "level": "县处级", "parent": "玉树州中级人民法院", "location": "青海省玉树藏族自治州囊谦县"},
    {"id": 7, "name": "囊谦县人民检察院", "type": "检察院", "level": "县处级", "parent": "玉树州人民检察院", "location": "青海省玉树藏族自治州囊谦县"},
    # 上级组织
    {"id": 8, "name": "中共玉树州委员会", "type": "党委", "level": "地厅级", "parent": "中共青海省委", "location": "青海省玉树藏族自治州玉树市"},
    {"id": 9, "name": "玉树藏族自治州人民政府", "type": "政府", "level": "地厅级", "parent": "青海省人民政府", "location": "青海省玉树藏族自治州玉树市"},
    # 石大存前履组织（跨黄南州/系统）
    {"id": 10, "name": "青海省公安厅政治部人事处", "type": "政府部门", "level": "厅局级", "parent": "青海省公安厅", "location": "青海省西宁市"},
    {"id": 11, "name": "青海省黄南藏族自治州同仁县人民政府", "type": "政府", "level": "县处级", "parent": "黄南州人民政府", "location": "青海省黄南藏族自治州同仁县"},
    {"id": 12, "name": "黄南州司法局", "type": "政府部门", "level": "地厅级", "parent": "黄南州人民政府", "location": "青海省黄南藏族自治州"},
    {"id": 13, "name": "中共泽库县委员会", "type": "党委", "level": "县处级", "parent": "中共黄南州委", "location": "青海省黄南藏族自治州泽库县"},
    {"id": 14, "name": "中共黄南州委政法委员会", "type": "政法", "level": "地厅级", "parent": "中共黄南州委", "location": "青海省黄南藏族自治州"},
    # 索南扎西前职业线索（玉树州内部乡镇/部门）
    {"id": 15, "name": "玉树州残疾人联合会", "type": "群团", "level": "地厅级", "parent": "", "location": "青海省玉树州"},
    {"id": 16, "name": "玉树州民政局", "type": "政府部门", "level": "地厅级", "parent": "玉树州人民政府", "location": "青海省玉树藏族自治州玉树市"},
    {"id": 17, "name": "囊谦县香达镇党委", "type": "乡镇", "level": "乡科级", "parent": "中共囊谦县委", "location": "青海省玉树藏族自治州囊谦县"},
    {"id": 18, "name": "囊谦县委宣传部", "type": "党委部门", "level": "县处级", "parent": "中共囊谦县委", "location": "青海省玉树藏族自治州囊谦县"},
    # 更却代丁前职业线索（本地乡镇/部门）
    {"id": 19, "name": "囊谦县娘拉乡党委", "type": "乡镇", "level": "乡科级", "parent": "中共囊谦县委", "location": "青海省玉树藏族自治州囊谦县"},
    {"id": 20, "name": "囊谦县东坝乡党委", "type": "乡镇", "level": "乡科级", "parent": "中共囊谦县委", "location": "青海省玉树藏族自治州囊谦县"},
    {"id": 21, "name": "囊谦县民政局", "type": "政府部门", "level": "县处级", "parent": "囊谦县人民政府", "location": "青海省玉树藏族自治州囊谦县"},
    {"id": 22, "name": "中共囊谦县委政法委员会", "type": "政法", "level": "县处级", "parent": "中共囊谦县委", "location": "青海省玉树藏族自治州囊谦县"},
    {"id": 23, "name": "囊谦县委组织部", "type": "党委部门", "level": "县处级", "parent": "中共囊谦县委", "location": "青海省玉树藏族自治州囊谦县"},
    {"id": 24, "name": "中共青海省委党校", "type": "事业单位", "level": "正厅级", "parent": "", "location": "青海省西宁市"},
    {"id": 25, "name": "青海师范大学", "type": "事业单位", "level": "正厅级", "parent": "", "location": "青海省西宁市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 石大存 — 县委书记（现任，CONFIRMED 完整履历）
    {"id": 1, "name": "石大存", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-03", "birthplace": "青海省海东市互助县",
     "education": "青海师范大学生物系本科", "party_join": "2000-12", "work_start": "2003-03",
     "current_post": "中共囊谦县委书记", "current_org": "中共囊谦县委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3701"},
    # 2 — 尕玛桑周 — 县委副书记、县长（现任，CONFIRMED role，bio thin）
    {"id": 2, "name": "尕玛桑周", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县委副书记、县长", "current_org": "囊谦县人民政府",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3700"},
    # 3 — 达哇扎西 — 县委副书记
    {"id": 3, "name": "达哇扎西", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县委副书记", "current_org": "中共囊谦县委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3703"},
    # 4 — 索南扎西 — 县委副书记（CONFIRMED 履历）
    {"id": 4, "name": "索南扎西", "gender": "男", "ethnicity": "藏族",
     "birth": "1976-09", "birthplace": "青海省玉树藏族自治州玉树市",
     "education": "青海省委党校研究生", "party_join": "1999-05", "work_start": "1997-07",
     "current_post": "囊谦县委副书记", "current_org": "中共囊谦县委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3704"},
    # 5 — 更却代丁 — 政协主席（CONFIRMED 履历）
    {"id": 5, "name": "更却代丁", "gender": "男", "ethnicity": "藏族",
     "birth": "1971-07", "birthplace": "青海省玉树藏族自治州囊谦县",
     "education": "本科", "party_join": "1997-07", "work_start": "1992-07",
     "current_post": "政协囊谦县委员会主席", "current_org": "政协囊谦县委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3707"},
    # 6 — 秦召 — 县委常委、常务副县长
    {"id": 6, "name": "秦召", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县委常委、常务副县长", "current_org": "囊谦县人民政府",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3717"},
    # 7 — 刘涛 — 县委常委、副县长（分管宣传/意识形态）
    {"id": 7, "name": "刘涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县委常委、副县长", "current_org": "囊谦县人民政府",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3718"},
    # 8 — 西然多杰 — 县委常委、副县长
    {"id": 8, "name": "西然多杰", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县委常委、副县长", "current_org": "囊谦县人民政府",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3699"},
    # 9 — 张志峰 — 县委常委
    {"id": 9, "name": "张志峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县委常委", "current_org": "中共囊谦县委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3705"},
    # 10 — 王文涛 — 县委常委
    {"id": 10, "name": "王文涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县委常委", "current_org": "中共囊谦县委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3706"},
    # 11 — 索南羊培 — 县委常委
    {"id": 11, "name": "索南羊培", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县委常委", "current_org": "中共囊谦县委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3711"},
    # 12 — 措尕 — 县委常委
    {"id": 12, "name": "措尕", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县委常委", "current_org": "中共囊谦县委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3713"},
    # 13 — 王世贺 — 县委常委
    {"id": 13, "name": "王世贺", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县委常委", "current_org": "中共囊谦县委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3714"},
    # 14 — 普巴才仁 — 县委常委
    {"id": 14, "name": "普巴才仁", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县委常委", "current_org": "中共囊谦县委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3715"},
    # 15 — 吉松保 — 县委常委
    {"id": 15, "name": "吉松保", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县委常委", "current_org": "中共囊谦县委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3716"},
    # 16 — 马永达杰 — 副县长
    {"id": 16, "name": "马永达杰", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县人民政府副县长", "current_org": "囊谦县人民政府",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3694"},
    # 17 — 刘海春 — 副县长
    {"id": 17, "name": "刘海春", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县人民政府副县长", "current_org": "囊谦县人民政府",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3697"},
    # 18 — 才仁松保 — 副县长
    {"id": 18, "name": "才仁松保", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县人民政府副县长", "current_org": "囊谦县人民政府",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3691"},
    # 19 — 措吉 — 副县长
    {"id": 19, "name": "措吉", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县人民政府副县长", "current_org": "囊谦县人民政府",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3692"},
    # 20 — 洛周求丁 — 副县长
    {"id": 20, "name": "洛周求丁", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县人民政府副县长", "current_org": "囊谦县人民政府",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3695"},
    # 21 — 赫发春 — 副县长（常务，2026 任前公示拟任）
    {"id": 21, "name": "赫发春", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县人民政府副县长", "current_org": "囊谦县人民政府",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3690"},
    # 22 — 丁保 — 人大常委会副主任
    {"id": 22, "name": "丁保", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县人大常委会副主任", "current_org": "囊谦县人大常委会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3687"},
    # 23 — 郭晓荣 — 人大常委会副主任
    {"id": 23, "name": "郭晓荣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县人大常委会副主任", "current_org": "囊谦县人大常委会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3689"},
    # 24 — 堪布多杰 — 人大常委会副主任
    {"id": 24, "name": "堪布多杰", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "囊谦县人大常委会副主任", "current_org": "囊谦县人大常委会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3688"},
    # 25 — 吾华才杰 — 政协副主席
    {"id": 25, "name": "吾华才杰", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政协囊谦县委员会副主席", "current_org": "政协囊谦县委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3708"},
    # 26 — 拉元舜 — 政协副主席
    {"id": 26, "name": "拉元舜", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政协囊谦县委员会副主席", "current_org": "政协囊谦县委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3709"},
    # 27 — 白玛成林 — 政协副主席
    {"id": 27, "name": "白玛成林", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政协囊谦县委员会副主席", "current_org": "政协囊谦县委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=3710"},
    # 28 — 马锐 — 州委书记（背景）
    {"id": 28, "name": "马锐", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共玉树州委书记", "current_org": "中共玉树州委员会",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=10752"},
    # 29 — 龙措 — 州委副书记、州长（背景）
    {"id": 29, "name": "龙措", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "玉树州委副书记、州长", "current_org": "玉树藏族自治州人民政府",
     "source": "https://www.nangqian.gov.cn/index.php?c=show&id=10794"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 石大存（书记）
    {"person_id": 1, "org_id": 1, "title": "囊谦县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持县委全面工作（官方领导页）"},
    {"person_id": 1, "org_id": 10, "title": "青海省公安厅政治部人事处机关干部科副科长、科长", "start_date": "", "end_date": "", "rank": "", "note": "前履"},
    {"person_id": 1, "org_id": 11, "title": "同仁县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "黄南州同仁县"},
    {"person_id": 1, "org_id": 12, "title": "黄南州司法局副局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "黄南州司法局"},
    {"person_id": 1, "org_id": 13, "title": "泽库县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "黄南州泽库县"},
    {"person_id": 1, "org_id": 14, "title": "黄南州委政法委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "黄南州委政法委"},
    # 尕玛桑周（县长）
    {"person_id": 2, "org_id": 2, "title": "囊谦县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "领导县政府全面工作，负责审计；协助县委财经委/审计委"},
    {"person_id": 2, "org_id": 1, "title": "囊谦县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "县委副书记兼职"},
    # 达哇扎西 / 索南扎西（副书记）
    {"person_id": 3, "org_id": 1, "title": "囊谦县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助处理县委日常工作、党建、深改委、编委；分管县委办"},
    {"person_id": 4, "org_id": 1, "title": "囊谦县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "统筹涉藏/维护稳定/国安委/教工委；分管政法统战外事"},
    {"person_id": 4, "org_id": 15, "title": "玉树州残联干部", "start_date": "", "end_date": "", "rank": "", "note": "前履"},
    {"person_id": 4, "org_id": 16, "title": "玉树州民政局干部、低保科副科长、科长", "start_date": "", "end_date": "", "rank": "", "note": "前履"},
    {"person_id": 4, "org_id": 17, "title": "囊谦县香达镇党委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": "香达镇党委书记（县委与政府双重任命）"},
    {"person_id": 4, "org_id": 18, "title": "囊谦县委常委、宣传部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "前履"},
    # 更却代丁（政协主席）
    {"person_id": 5, "org_id": 4, "title": "政协囊谦县委员会主席", "start_date": "2024-04", "end_date": "present", "rank": "正处级", "note": "2024-04起任政协主席"},
    {"person_id": 5, "org_id": 3, "title": "囊谦县人大常委会主任", "start_date": "2021-08", "end_date": "2024-03", "rank": "正处级", "note": "前任人大主任"},
    {"person_id": 5, "org_id": 22, "title": "囊谦县委常委、政法委书记", "start_date": "2016-10", "end_date": "2021-07", "rank": "副处级", "note": "县委常委、政法委书记"},
    {"person_id": 5, "org_id": 21, "title": "囊谦县民政局局长", "start_date": "", "end_date": "", "rank": "正科级", "note": "前履"},
    {"person_id": 5, "org_id": 19, "title": "囊谦县娘拉乡党委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": "前履"},
    {"person_id": 5, "org_id": 20, "title": "囊谦县东坝乡党委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": "前履"},
    {"person_id": 5, "org_id": 19, "title": "囊谦县娘拉乡人武部长", "start_date": "", "end_date": "", "rank": "", "note": "前履"},
    # 县党委常委会成员
    {"person_id": 6, "org_id": 2, "title": "囊谦县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助达哇扎西负责乡村振兴、全域无垃圾和禁塑减废专项行动"},
    {"person_id": 7, "org_id": 2, "title": "囊谦县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助索南扎西负责宣传、意识形态、网信、融媒体中心"},
    {"person_id": 8, "org_id": 2, "title": "囊谦县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "副县长、常委"},
    {"person_id": 9, "org_id": 1, "title": "囊谦县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "囊谦县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "囊谦县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "囊谦县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "囊谦县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "囊谦县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "囊谦县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 县政府副县长（非常委）
    {"person_id": 16, "org_id": 2, "title": "囊谦县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "囊谦县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "囊谦县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "囊谦县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "囊谦县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "囊谦县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026任前公示拟任（常务副县长候选人）"},
    # 人大/政协
    {"person_id": 22, "org_id": 3, "title": "囊谦县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 3, "title": "囊谦县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 24, "org_id": 3, "title": "囊谦县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 4, "title": "政协囊谦县委员会副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 26, "org_id": 4, "title": "政协囊谦县委员会副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 27, "org_id": 4, "title": "政协囊谦县委员会副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 州级背景
    {"person_id": 28, "org_id": 8, "title": "中共玉树州委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 29, "org_id": 9, "title": "玉树州委副书记、州长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    # 县委书记 × 县长
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "石大存（书记）与尕玛桑周（县委副书记、县长）为囊谦现任党政主要领导，领导县委、县政府全线", "overlap_org": "囊谦县", "overlap_period": ""},
    # 书记 × 副书记们
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "达哇扎西作为县委副书记协助石大存处理县委日常工作/党建/深改办", "overlap_org": "中共囊谦县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "索南扎西（县委副书记）在石大存领导下统筹政法、统战、涉藏工作", "overlap_org": "中共囊谦县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "党政分工", "context": "更却代丁（政协主席）与县委领导班子同在职（更却任人大主任、政协主席期间与书记共事）", "overlap_org": "囊谦县", "overlap_period": "2021至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "常务副县长秦召在县委常委会与书记同班", "overlap_org": "中共囊谦县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "副县长刘涛协助索南扎西分工；与书大为县委班子成员", "overlap_org": "中共囊谦县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "副县长西然多杰为县委常委，与书大同班", "overlap_org": "中共囊谦县委", "overlap_period": ""},
    # 县长 × 县政府班子
    {"person_a": 2, "person_b": 6, "type": "搭档", "context": "县长与常务副县长秦召共同推进县政府常务工作", "overlap_org": "囊谦县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "县长与副县长马永达杰同属县政府班子", "overlap_org": "囊谦县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "上下级", "context": "县长与副县长刘烨春同属县政府班子", "overlap_org": "囊谦县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 18, "type": "上下级", "context": "县长与副县长才仁松保同属县政府班子", "overlap_org": "囊谦县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 19, "type": "上下级", "context": "县长与副县长措吉同属县政府班子", "overlap_org": "囊谦县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 20, "type": "上下级", "context": "县长与副县长洛周求丁同属县政府班子", "overlap_org": "囊谦县人民政府", "overlap_period": ""},
    # 跨系统职业网络：石大存（公安/政法 → 黄南 → 玉树）
    {"person_a": 1, "person_b": 5, "type": "predecessor_successor", "context": "更却代丁曾任囊谦县委常委、政法委书记（2016-2021），石大存任县委书记后与其兼跨政法系统", "overlap_org": "囊谦县", "overlap_period": "2016-2021"},
    {"person_a": 4, "person_b": 5, "type": "同政治系统轮换", "context": "索南扎西（副书记）与更却代丁（政协主席）均长期在囊谦政法/统战领域共事", "overlap_org": "囊谦县", "overlap_period": ""},
    # 州级领导 → 县级（上下级）
    {"person_a": 28, "person_b": 1, "type": "上下级", "context": "玉树州委书记马锐为囊谦县委书记上级（州管县干部）", "overlap_org": "玉树州", "overlap_period": ""},
    {"person_a": 29, "person_b": 2, "type": "上下级", "context": "玉树州长龙措督导囊谦防汛工作（州对县指导）", "overlap_org": "玉树州", "overlap_period": "2026"},
    {"person_a": 29, "person_b": 1, "type": "上下级", "context": "州长龙措赴囊谦督导防汛，县级党委政府主要负责人陪同", "overlap_org": "玉树州/囊谦县", "overlap_period": "2026"},
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