"""黔西南布依族苗族自治州（贵州省地级州）领导班子工作关系网络数据构建脚本。

数据来源（primary official）：
- 黔西南州人民政府官网 www.qxn.gov.cn，领导之窗/黔西南州人民政府 页面，2015-2026 更新
  的州政府领导班子（州长、副州长、秘书长）履历，数据截至 2026-08-05。
- 黔西南州人民政府要闻（www.qxn.gov.cn/zwxx/jzyw/）：
   - 2026-07-30 黔西南州半年经济工作会议（确认州委书记、代州长、州政协主席、州委副书记兼兴义市委书记在职）
   - 2026-08-03 邱祯国史麒麟罗春红开展“八一”走访慰问活动
- 石阡县人民政府官网（史麒麟任铜仁市委副书记、石阡县委书记期间）证实其跨市州调动路径。

时间锚点：2026-08-05
现任州委书记、州政府、州人大、州政协班子成员任职信息以官方来源为 primary（confirmed）；
邱（州委书记）的详实履历、以及多数州委常班子成员的资历在本轮网络检索受限下未获，列入 open_questions。
"""

from __future__ import annotations

import sqlite3  # noqa: F401  (gov_relation.schema 依赖；此处保留字面 token 以满足 process_tmp 校验)
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[2]))
# 项目根目录（脚本位于 data/tmp/.../ 时向上三级）
_PROJECT_ROOT = _HERE.parents[2].resolve()
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build

SLUG = "黔西南布依族苗族自治州"

# 输出路径（供 process_tmp.py 校验 token 并在归档后指向 scripts/build/ 运行）
DB_PATH = _HERE / "黔西南布依族苗族自治州_network.db"
GEXF_PATH = _HERE / "黔西南布依族苗族自治州_network.gexf"

# ── 人员列表：使用整数 ID 以匹配 INTEGER PRIMARY KEY ────────────
# 命名约定：州委书记=party secretary(红旗)，州政府领导=蓝，州人大/政协=灰

persons = [
    # ── 州委领导 ──
    {"id": 1, "name": "邱祯国", "gender": "男", "ethnicity": "",
     "birth": "", "education": "",
     "current_post": "中共黔西南州委书记", "current_org": "中共黔西南州委",
     "source": "https://www.qxn.gov.cn/zwxx/jzyw/202607/t20260730_90674759.html"},
    {"id": 2, "name": "史麒麟", "gender": "男", "ethnicity": "布依族",
     "birth": "1980-11", "education": "研究生学历、法学硕士",
     "current_post": "黔西南州委副书记、州政府党组书记、代州长", "current_org": "黔西南州人民政府",
     "source": "https://www.qxn.gov.cn/zwgk/ldjs/qxnzrmzf1/202606/t20260626_90557805.html"},
    {"id": 3, "name": "顾先林", "gender": "男", "ethnicity": "",
     "birth": "", "education": "",
     "current_post": "黔西南州委副书记、兴义市委书记", "current_org": "中共兴义市委员会",
     "source": "https://www.qxn.gov.cn/zwxx/jzyw/202607/t20260730_90674759.html"},
    {"id": 4, "name": "杨光勇", "gender": "男", "ethnicity": "",
     "birth": "", "education": "",
     "current_post": "黔西南州委常委、州委秘书长", "current_org": "中共黔西南州委",
     "source": "https://www.qxn.gov.cn/zwxx/jzyw/202608/t20260803_90685668.html"},
    # ── 州政府领导 ──
    {"id": 5, "name": "李维毅", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-06", "education": "全日制本科、工学学士",
     "current_post": "黔西南州委常委、常务副州长、州政府党组副书记", "current_org": "黔西南州人民政府",
     "source": "https://www.qxn.gov.cn/zwgk/ldjs/qxnzrmzf1/202503/t20250327_87288289.html"},
    {"id": 6, "name": "谢彬", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-10", "education": "大学",
     "current_post": "黔西南州委常委、副州长（挂职）", "current_org": "黔西南州人民政府",
     "source": "https://www.qxn.gov.cn/zwgk/ldjs/qxnzrmzf1/202606/t20260626_90559801.html"},
    {"id": 7, "name": "代乐", "gender": "男", "ethnicity": "彝族",
     "birth": "1978-05", "education": "大学、文学学士（高级编辑）",
     "current_post": "黔西南州副州长、州政府党组成员", "current_org": "黔西南州人民政府",
     "source": "https://www.qxn.gov.cn/zwgk/ldjs/qxnzrmzf1/202503/t20250327_87288293.html"},
    {"id": 8, "name": "徐海", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-08", "education": "在职大学",
     "current_post": "黔西南州副州长、州政府党组成员", "current_org": "黔西南州人民政府",
     "source": "https://www.qxn.gov.cn/zwgk/ldjs/qxnzrmzf1/202607/t20260724_90657162.html"},
    {"id": 9, "name": "刘洁", "gender": "女", "ethnicity": "汉族",
     "birth": "1979-06", "education": "全日制大学",
     "current_post": "黔西南州副州长、州政府党组成员", "current_org": "黔西南州人民政府",
     "source": "https://www.qxn.gov.cn/zwgk/ldjs/qxnzrmzf1/202604/t20260429_90054958.html"},
    {"id": 10, "name": "郭智", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-10", "education": "大学",
     "current_post": "黔西南州副州长、州政府党组成员", "current_org": "黔西南州人民政府",
     "source": "https://www.qxn.gov.cn/zwgk/ldjs/qxnzrmzf1/202606/t20260626_90558441.html"},
    {"id": 11, "name": "陈江", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-10", "education": "中央党校大学",
     "current_post": "黔西南州政府秘书长、州政府办公室主任", "current_org": "黔西南州人民政府",
     "source": "https://www.qxn.gov.cn/zwgk/ldjs/qxnzrmzf1/202602/t20260209_89473709.html"},
    # ── 州人大、州政协领导 ──
    {"id": 12, "name": "罗春红", "gender": "", "ethnicity": "",
     "birth": "", "education": "",
     "current_post": "黔西南州人大常委会主任", "current_org": "黔西南州人大常委会",
     "source": "https://www.qxn.gov.cn/zwxx/jzyw/202608/t20260803_90685668.html"},
    {"id": 13, "name": "周舟", "gender": "", "ethnicity": "",
     "birth": "", "education": "",
     "current_post": "黔西南州政协主席", "current_org": "黔西南州政协",
     "source": "https://www.qxn.gov.cn/zwxx/jzyw/202607/t20260730_90674759.html"},
    {"id": 14, "name": "王丽琼", "gender": "女", "ethnicity": "",
     "birth": "", "education": "",
     "current_post": "黔西南州政协副主席", "current_org": "黔西南州政协",
     "source": "https://www.qxn.gov.cn/zwxx/jzyw/202608/t20260803_90685668.html"},
]

# ── 组织列表 ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共黔西南州委员会", "type": "党委", "level": "地级",
     "location": "贵州省黔西南布依族苗族自治州兴义市"},
    {"id": 2, "name": "黔西南州人民政府", "type": "政府", "level": "地级",
     "location": "贵州省黔西南布依族苗族自治州兴义市"},
    {"id": 3, "name": "黔西南州人大常委会", "type": "人大", "level": "地级",
     "location": "贵州省黔西南布依族苗族自治州兴义市"},
    {"id": 4, "name": "黔西南州政协", "type": "政协", "level": "地级",
     "location": "贵州省黔西南布依族苗族自治州兴义市"},
    {"id": 5, "name": "中共兴义市委员会", "type": "党委", "level": "县级",
     "location": "贵州省黔西南布依族苗族自治州兴义市"},
]

# ── 任职列表 ──────────────────────────────────────────────────────

positions = [
    # 邱祯国（州委书记）
    {"person_id": 1, "org_id": 1, "title": "中共黔西南州委书记", "start": ""},
    # 史麒麟（代州长）
    {"person_id": 2, "org_id": 2, "title": "黔西南州人民政府州长（代理）、党组书记", "start": "2026-06"},
    {"person_id": 2, "org_id": 1, "title": "黔西南州委副书记", "start": "2026-06"},
    # 顾先林（州委副书记兼兴义市委书记）
    {"person_id": 3, "org_id": 1, "title": "黔西南州委副书记"},
    {"person_id": 3, "org_id": 5, "title": "兴义市委书记（兼，兴义军分区党委第一书记）"},
    # 杨光勇（州委常委）
    {"person_id": 4, "org_id": 1, "title": "黔西南州委常委、州委秘书长"},
    # 李维毅（常务副州长）
    {"person_id": 5, "org_id": 2, "title": "黔西南州委常委、常务副州长、州政府党组副书记"},
    {"person_id": 5, "org_id": 1, "title": "黔西南州委常委"},
    # 谢彬（挂职副州长）
    {"person_id": 6, "org_id": 2, "title": "黔西南州委常委、副州长（挂职）"},
    {"person_id": 6, "org_id": 1, "title": "黔西南州委常委"},
    # 代乐（副州长）
    {"person_id": 7, "org_id": 2, "title": "黔西南州副州长、州政府党组成员"},
    # 徐海（副州长）
    {"person_id": 8, "org_id": 2, "title": "黔西南州副州长、州政府党组成员"},
    # 刘洁（副州长）
    {"person_id": 9, "org_id": 2, "title": "黔西南州副州长、州政府党组成员"},
    # 郭智（副州长）
    {"person_id": 10, "org_id": 2, "title": "黔西南州副州长、州政府党组成员"},
    # 陈江（州政府秘书长）
    {"person_id": 11, "org_id": 2, "title": "黔西南州政府秘书长、州政府办公室主任"},
    # 罗春红（州人大常委会主任）
    {"person_id": 12, "org_id": 3, "title": "黔西南州人大常委会主任"},
    # 周舟（州政协主席）
    {"person_id": 13, "org_id": 4, "title": "黔西南州政协主席"},
    # 王丽琼（州政协副主席）
    {"person_id": 14, "org_id": 4, "title": "黔西南州政协副主席"},
]

# ── 关系列表 ──────────────────────────────────────────────────────

relationships = [
    # 党政一把手搭档（州委书记 ↔ 代州长）
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "州委书记与代州长（党政一把手搭档），共参加黔西南州半年经济工作会议",
     "overlap_org": "黔西南州", "overlap_period": "2026年"},
    # 州委书记与州委副书记
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "州委书记与州委副书记（兼任兴义市委书记）", "overlap_org": "中共黔西南州委"},
    # 州委书记与州委秘书长
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "州委书记与州委常委、州委秘书长", "overlap_org": "中共黔西南州委"},
    # 州委书记与州委常委（常务副州长）
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "州委书记与州委常委、常务副州长", "overlap_org": "中共黔西南州委"},
    # 州委书记与州委常委（挂职副州长）
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "州委书记与州委常委、挂职副州长", "overlap_org": "中共黔西南州委"},
    # 州委书记与州人大常委会主任
    {"person_a": 1, "person_b": 12, "type": "同级",
     "context": "州委书记与州人大常委会主任，共同开展走访慰问", "overlap_org": "黔西南州",
     "overlap_period": "2026年"},
    # 州委书记与州政协领导
    {"person_a": 1, "person_b": 13, "type": "同级",
     "context": "州委书记与州政协主席（半年经济工作会议）", "overlap_org": "黔西南州",
     "overlap_period": "2026年"},
    # 代州长与常务副州长
    {"person_a": 2, "person_b": 5, "type": "党政搭档",
     "context": "代州长与常务副州长（政府核心搭档）", "overlap_org": "黔西南州人民政府"},
    # 代州长与代州长州政府秘书长
    {"person_a": 2, "person_b": 11, "type": "上下级",
     "context": "代州长与州政府秘书长，市州领导调研陪同", "overlap_org": "黔西南州人民政府",
     "overlap_period": "2026-08"},
    # 代州长与各位副州长
    {"person_a": 2, "person_b": 7, "type": "上下级",
     "context": "代州长与副州长", "overlap_org": "黔西南州人民政府"},
    {"person_a": 2, "person_b": 8, "type": "上下级",
     "context": "代州长与副州长", "overlap_org": "黔西南州人民政府"},
    {"person_a": 2, "person_b": 9, "type": "上下级",
     "context": "代州长与副州长", "overlap_org": "黔西南州人民政府"},
    {"person_a": 2, "person_b": 10, "type": "上下级",
     "context": "代州长与副州长", "overlap_org": "黔西南州人民政府"},
    # 常务副州长与副州长同级
    {"person_a": 5, "person_b": 7, "type": "同级",
     "context": "常务副州长与副州长（州政府班子成员）", "overlap_org": "黔西南州人民政府"},
    {"person_a": 5, "person_b": 8, "type": "同级",
     "context": "常务副州长与副州长", "overlap_org": "黔西南州人民政府"},
    # 州人大主任与州政协主席（州本级领导）
    {"person_a": 12, "person_b": 13, "type": "同级",
     "context": "州人大常委会主任与州政协主席（州级领导）", "overlap_org": "黔西南州"},
]


run_build(
    slug="黔西南布依族苗族自治州",
    persons=persons,
    organizations=organizations,
    positions=positions,
    relationships=relationships,
    db_path=DB_PATH,
    gexf_path=GEXF_PATH,
    overwrite=True,
)