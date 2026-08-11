"""凉山彝族自治州（四川省地级州）领导班子工作关系网络数据构建脚本。

数据来源：
- 凉山州人民政府官网 (lsz.gov.cn)，州政府领导页面数据截至 2026-07-28
- 凉山新闻网 (ls666.com) 领导人简历
"""

import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[2]))
os.chdir(sys.path[0])

STAGING = _HERE

from gov_relation.runner import run_build

SLUG = "凉山彝族自治州"

# ── 人员列表：使用整数 ID 以匹配 INTEGER PRIMARY KEY ────────────

persons = [
    # ── 州委领导 ──
    {"id": 1, "name": "虞平", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-09", "education": "党校研究生、在职研究生",
     "current_post": "中共凉山州委书记", "current_org": "中共凉山州委",
     "source": "https://www.lsz.gov.cn/"},
    {"id": 2, "name": "马辉", "gender": "男",
     "birth": "", "education": "",
     "current_post": "凉山州委副书记（专职）/ 州委常委", "current_org": "中共凉山州委",
     "source": "https://www.lsz.gov.cn/"},
    {"id": 3, "name": "尹江涛", "gender": "男",
     "birth": "", "education": "",
     "current_post": "凉山州委常委", "current_org": "中共凉山州委",
     "source": "https://www.lsz.gov.cn/"},
    # ── 州政府领导 ──
    {"id": 4, "name": "张文旺", "gender": "男", "ethnicity": "彝族",
     "birth": "1972-09", "education": "大学，经济学学士",
     "current_post": "凉山州委副书记、州长、州政府党组书记", "current_org": "凉山州人民政府",
     "source": "https://www.lsz.gov.cn/zfld/"},
    {"id": 5, "name": "王岳", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-10", "education": "大学",
     "current_post": "凉山州委常委、常务副州长、党组副书记", "current_org": "凉山州人民政府",
     "source": "https://www.lsz.gov.cn/zfld/ldxx/fzz/zzfwy/"},
    {"id": 6, "name": "徐振华", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1972-10", "education": "在职研究生",
     "current_post": "凉山州委常委、副州长（挂职）", "current_org": "凉山州人民政府",
     "source": "https://www.lsz.gov.cn/zfld/ldxx/fzz/xzf/"},
    {"id": 7, "name": "周仕伦", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-03", "education": "省委党校研究生",
     "current_post": "凉山州副州长", "current_org": "凉山州人民政府",
     "source": "https://www.lsz.gov.cn/zfld/ldxx/fzz/fzzzsl/"},
    {"id": 8, "name": "苏正清", "gender": "男", "ethnicity": "彝族",
     "birth": "1969-12", "education": "省委党校研究生",
     "current_post": "凉山州副州长、党组成员", "current_org": "凉山州人民政府",
     "source": "https://www.lsz.gov.cn/zfld/ldxx/fzz/fzzszq/"},
    {"id": 9, "name": "刘行勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-10", "education": "大学、在职硕士",
     "current_post": "凉山州副州长、州公安局局长", "current_org": "凉山州人民政府",
     "source": "https://www.lsz.gov.cn/zfld/ldxx/fzz/lxy/"},
    {"id": 10, "name": "李佳林", "gender": "男", "ethnicity": "汉族",
     "birth": "1987", "education": "工学博士",
     "current_post": "凉山州副州长、党组成员", "current_org": "凉山州人民政府",
     "source": "https://www.lsz.gov.cn/zfld/ldxx/fzz/ljl/"},
    {"id": 11, "name": "高晶晶", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-04", "education": "在职研究生",
     "current_post": "凉山州副州长", "current_org": "凉山州人民政府",
     "source": "https://www.lsz.gov.cn/zfld/ldxx/fzz/zfldgjj/"},
    {"id": 12, "name": "陈翔", "gender": "男", "ethnicity": "彝族",
     "birth": "1975-06", "education": "省委党校研究生",
     "current_post": "凉山州副州长、党组成员，美姑县委书记", "current_org": "凉山州人民政府",
     "source": "https://www.lsz.gov.cn/zfld/ldxx/fzz/fzzcx/"},
    {"id": 13, "name": "刘长佐", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-01", "education": "在职研究生",
     "current_post": "凉山州政府秘书长、党组成员、办公室党组书记", "current_org": "凉山州人民政府",
     "source": "https://www.lsz.gov.cn/zfld/ldxx/msz/smzq/"},
    # ── 人大、政协领导 ──
    {"id": 14, "name": "龙伟", "gender": "男",
     "current_post": "凉山州人大常委会主任、党组书记", "current_org": "凉山州人大常委会",
     "source": "https://www.lsz.gov.cn/"},
    {"id": 15, "name": "陈刚", "gender": "男",
     "current_post": "凉山州政协主席", "current_org": "凉山州政协",
     "source": "https://www.lsz.gov.cn/"},
]

# ── 组织列表 ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共凉山州委", "type": "党委", "level": "地级",
     "location": "四川省凉山彝族自治州西昌市"},
    {"id": 2, "name": "凉山州人民政府", "type": "政府", "level": "地级",
     "location": "四川省凉山彝族自治州西昌市"},
    {"id": 3, "name": "凉山州人大常委会", "type": "人大", "level": "地级",
     "location": "四川省凉山彝族自治州西昌市"},
    {"id": 4, "name": "凉山州政协", "type": "政协", "level": "地级",
     "location": "四川省凉山彝族自治州西昌市"},
    {"id": 5, "name": "凉山州公安局", "type": "政府", "level": "地级",
     "location": "四川省凉山彝族自治州西昌市"},
    {"id": 6, "name": "中共美姑县委", "type": "党委", "level": "县级",
     "location": "四川省凉山彝族自治州美姑县"},
    {"id": 7, "name": "中央纪委国家监委驻中粮集团有限公司纪检监察组",
     "type": "党委", "level": "副部级", "location": "北京市"},
]

# ── 任职列表 ──────────────────────────────────────────────────────

positions = [
    # 虞平
    {"person_id": 1, "org_id": 1, "title": "中共凉山州委书记", "start": "2023-02"},
    # 马辉
    {"person_id": 2, "org_id": 1, "title": "凉山州委副书记（专职）/州委常委"},
    # 尹江涛
    {"person_id": 3, "org_id": 1, "title": "凉山州委常委"},
    # 张文旺
    {"person_id": 4, "org_id": 2, "title": "凉山州人民政府州长、党组书记"},
    {"person_id": 4, "org_id": 1, "title": "凉山州委副书记"},
    # 王岳
    {"person_id": 5, "org_id": 2, "title": "常务副州长、党组副书记"},
    {"person_id": 5, "org_id": 1, "title": "凉山州委常委"},
    # 徐振华
    {"person_id": 6, "org_id": 2, "title": "副州长（挂职）"},
    {"person_id": 6, "org_id": 1, "title": "凉山州委常委"},
    {"person_id": 6, "org_id": 7, "title": "中央纪委国家监委驻中粮集团纪检监察组副组长"},
    # 周仕伦
    {"person_id": 7, "org_id": 2, "title": "副州长"},
    # 苏正清
    {"person_id": 8, "org_id": 2, "title": "副州长、党组成员"},
    # 刘行勇
    {"person_id": 9, "org_id": 2, "title": "副州长"},
    {"person_id": 9, "org_id": 5, "title": "州公安局局长"},
    # 李佳林
    {"person_id": 10, "org_id": 2, "title": "副州长、党组成员"},
    # 高晶晶
    {"person_id": 11, "org_id": 2, "title": "副州长"},
    # 陈翔
    {"person_id": 12, "org_id": 2, "title": "副州长、党组成员"},
    {"person_id": 12, "org_id": 6, "title": "美姑县委书记（兼）"},
    # 刘长佐
    {"person_id": 13, "org_id": 2, "title": "州政府秘书长、党组成员、办公室党组书记"},
    # 龙伟
    {"person_id": 14, "org_id": 3, "title": "州人大常委会主任、党组书记"},
    # 陈刚
    {"person_id": 15, "org_id": 4, "title": "州政协主席"},
]

# ── 关系列表 ──────────────────────────────────────────────────────

relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 4, "type": "党政搭档",
     "context": "州委书记与州长（党政一把手搭档）",
     "overlap_org": "中共凉山州委"},
    # 书记与副书记
    {"person_a": 1, "person_b": 2, "type": "上下级",
     "context": "书记与专职副书记", "overlap_org": "中共凉山州委"},
    # 书记与常委副州长
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "书记与州委常委、常务副州长", "overlap_org": "中共凉山州委"},
    # 书记与挂职副州长
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "书记与挂职副州长（州委常委）", "overlap_org": "中共凉山州委"},
    # 州长与常务副州长
    {"person_a": 4, "person_b": 5, "type": "党政搭档",
     "context": "州长与常务副州长（政府核心搭档）",
     "overlap_org": "凉山州人民政府"},
    # 州长与各位副州长
    {"person_a": 4, "person_b": 7, "type": "上下级",
     "context": "州长与副州长", "overlap_org": "凉山州人民政府"},
    {"person_a": 4, "person_b": 8, "type": "上下级",
     "context": "州长与副州长", "overlap_org": "凉山州人民政府"},
    {"person_a": 4, "person_b": 9, "type": "上下级",
     "context": "州长与副州长兼公安局长", "overlap_org": "凉山州人民政府"},
    {"person_a": 4, "person_b": 10, "type": "上下级",
     "context": "州长与副州长", "overlap_org": "凉山州人民政府"},
    {"person_a": 4, "person_b": 11, "type": "上下级",
     "context": "州长与副州长", "overlap_org": "凉山州人民政府"},
    {"person_a": 4, "person_b": 12, "type": "上下级",
     "context": "州长与副州长", "overlap_org": "凉山州人民政府"},
    # 书记与人大、政协
    {"person_a": 1, "person_b": 14, "type": "同级",
     "context": "州委书记与人大常委会主任（州级领导）",
     "overlap_org": "凉山州"},
    {"person_a": 1, "person_b": 15, "type": "同级",
     "context": "州委书记与政协主席", "overlap_org": "凉山州"},
    # 副州长同级关系
    {"person_a": 5, "person_b": 9, "type": "工作关系",
     "context": "常务副州长与公安局长", "overlap_org": "凉山州人民政府"},
    {"person_a": 8, "person_b": 12, "type": "同级",
     "context": "彝族干部，同为副州长", "overlap_org": "凉山州人民政府"},
    # 书记与其他州委常委
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "书记与州委常委", "overlap_org": "中共凉山州委"},
]


run_build(
    slug="凉山彝族自治州",
    persons=persons,
    organizations=organizations,
    positions=positions,
    relationships=relationships,
    db_path=STAGING / "凉山彝族自治州_network.db",
    gexf_path=STAGING / "凉山彝族自治州_network.gexf",
    overwrite=True,
)