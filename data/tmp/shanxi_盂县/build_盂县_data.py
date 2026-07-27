# -*- coding: utf-8 -*-
"""Build script: 盂县 (Yuxian County, Yangquan, Shanxi) leadership network.
   Investigation date: 2026-07-26

Current 县委书记: 王拥国 (appointed 2025-11-03, previously 县长)
Current 县长: 程秀宏 (appointed 2025-11, formerly 阳泉市住建局局长)
Predecessor 县委书记: 梁海昌 (last active 2025-07-15, whereabouts unknown)
"""

import sys, os
_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, _REPO_ROOT)
os.chdir(_REPO_ROOT)

from gov_relation.runner import run_build

slug = "盂县"

# ═══════════════════════════════════════════════════════════
# SOURCE REGISTER
# ═══════════════════════════════════════════════════════════
SOURCES = {
    "S001": {"title": "盂县人民政府门户网站", "url": "https://www.sxyx.gov.cn/", "publisher": "盂县人民政府", "published_at": "", "accessed_at": "2026-07-26", "source_type": "official", "reliability": "high"},
    "S002": {"title": "盂县人民政府领导信息页", "url": "https://www.sxyx.gov.cn/yxxxgk/yxrmzf/fdzdgknr/ldxx/202408/t20240805_1932967.html", "publisher": "盂县人民政府", "published_at": "2024-08-05", "accessed_at": "2026-07-26", "source_type": "official", "reliability": "high"},
    "S003": {"title": "县委常委会（扩大）会议 — 王拥国主持", "url": "https://www.sxyx.gov.cn/xwzx/xwdt/202607/t20260708_2218019.shtml", "publisher": "盂县人民政府", "published_at": "2026-07-08", "accessed_at": "2026-07-26", "source_type": "official", "reliability": "high"},
    "S004": {"title": "县长副县长分工通知 (2026年5月)", "url": "https://www.sxyx.gov.cn/zwgk/zfxxgkml/xzfbwj/202606/t20260626_2214590.shtml", "publisher": "盂县人民政府办公室", "published_at": "2026-06-26", "accessed_at": "2026-07-26", "source_type": "official", "reliability": "high"},
    "S005": {"title": "提质跃升座谈会 领导名单", "url": "https://www.sxyx.gov.cn/xwzx/xwdt/202607/t20260717_2220946.shtml", "publisher": "盂县人民政府", "published_at": "2026-07-17", "accessed_at": "2026-07-26", "source_type": "official", "reliability": "high"},
    "S006": {"title": "李冲(宣传部长)授课报道", "url": "https://www.sxyx.gov.cn/xwzx/xwdt/202607/t20260710_2218726.shtml", "publisher": "盂县人民政府", "published_at": "2026-07-10", "accessed_at": "2026-07-26", "source_type": "official", "reliability": "high"},
    "S007": {"title": "吕世伟(组织部长)调研报道", "url": "https://www.sxyx.gov.cn/xwzx/xwdt/202606/t20260609_2206677.shtml", "publisher": "盂县人民政府", "published_at": "2026-06-09", "accessed_at": "2026-07-26", "source_type": "official", "reliability": "high"},
    "S008": {"title": "程秀宏督导防汛报道", "url": "https://www.sxyx.gov.cn/xwzx/xwdt/202607/t20260714_2219547.shtml", "publisher": "盂县人民政府", "published_at": "2026-07-14", "accessed_at": "2026-07-26", "source_type": "official", "reliability": "high"},
    "S009": {"title": "梁海昌最后亮相 — 县委常委扩大会议", "url": "https://www.sxyx.gov.cn/xwzx/xwdt/202507/t202507_} ", "publisher": "盂县人民政府", "published_at": "2025-07-15", "accessed_at": "2026-07-26", "source_type": "official", "reliability": "high"},
    "S010": {"title": "王拥国县长办公会报道", "url": "https://www.sxyx.gov.cn/xwzx/xwdt/202411/t20241121_2188609.shtml", "publisher": "盂县人民政府", "published_at": "2024-11-21", "accessed_at": "2026-07-26", "source_type": "official", "reliability": "high"},
    "S011": {"title": "全县领导干部大会 王拥国任书记", "url": "https://www.sxyx.gov.cn/xwzx/xwdt/202511/t20251105_2210001.shtml", "publisher": "盂县人民政府", "published_at": "2025-11-05", "accessed_at": "2026-07-26", "source_type": "official", "reliability": "high"},
}

persons = [
    # ═══ 核心领导 ═══
    {"id": 1, "name": "王拥国", "gender": "男", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查", "education": "待查",
     "current_post": "县委书记", "current_org": "中共盂县委员会",
     "source": "S003"},
    {"id": 2, "name": "程秀宏", "gender": "男", "ethnicity": "汉族", "birth": "1975", "birthplace": "待查", "education": "大学本科",
     "current_post": "县委副书记、县长、县经开区党工委书记", "current_org": "盂县人民政府",
     "source": "S002"},
    {"id": 18, "name": "梁海昌", "gender": "男", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查", "education": "待查",
     "current_post": "前县委书记（2025年7月后不再出现）", "current_org": "（去向待查）",
     "source": "S009"},

    # ═══ 县委常委 ═══
    {"id": 3, "name": "王珂", "gender": "男", "ethnicity": "汉族", "birth": "1985", "birthplace": "待查", "education": "研究生，文学硕士",
     "current_post": "县委常委、副县长", "current_org": "盂县人民政府",
     "source": "S002"},
    {"id": 4, "name": "韩秀山", "gender": "男", "ethnicity": "汉族", "birth": "1977", "birthplace": "待查", "education": "大学本科",
     "current_post": "县委常委、副县长", "current_org": "盂县人民政府",
     "source": "S002"},
    {"id": 5, "name": "艾尼亚尔·艾尼瓦尔", "gender": "男", "ethnicity": "维吾尔族", "birth": "1987", "birthplace": "新疆伊犁", "education": "管理学学士",
     "current_post": "县委常委、副县长（挂职）", "current_org": "盂县人民政府",
     "source": "S002"},
    {"id": 12, "name": "李冲", "gender": "女", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查", "education": "待查",
     "current_post": "县委常委、宣传部部长", "current_org": "中共盂县县委宣传部",
     "source": "S006"},
    {"id": 13, "name": "吕世伟", "gender": "男", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查", "education": "待查",
     "current_post": "县委常委、组织部部长", "current_org": "中共盂县委员会",
     "source": "S007"},
    {"id": 14, "name": "郭华", "gender": "男", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查", "education": "待查",
     "current_post": "县委常委、常务副县长", "current_org": "盂县人民政府",
     "source": "S004"},
    {"id": 15, "name": "连斌", "gender": "男", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查", "education": "待查",
     "current_post": "县委常委、纪委书记（推测）", "current_org": "中共盂县纪委",
     "source": "S003"},
    {"id": 16, "name": "王云飞", "gender": "男", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查", "education": "待查",
     "current_post": "县委领导", "current_org": "中共盂县委员会",
     "source": "S005"},
    {"id": 17, "name": "李春", "gender": "男", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查", "education": "待查",
     "current_post": "县委领导", "current_org": "中共盂县委员会",
     "source": "S005"},
    {"id": 19, "name": "张军", "gender": "男", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查", "education": "待查",
     "current_post": "县委领导", "current_org": "中共盂县委员会",
     "source": "S005"},

    # ═══ 县政府班子 ═══
    {"id": 6, "name": "李东亮", "gender": "男", "ethnicity": "汉族", "birth": "1971", "birthplace": "待查", "education": "大学本科",
     "current_post": "副县长", "current_org": "盂县人民政府",
     "source": "S002"},
    {"id": 7, "name": "王雪梅", "gender": "女", "ethnicity": "汉族", "birth": "1979", "birthplace": "待查", "education": "大学本科，法学学士",
     "current_post": "副县长", "current_org": "盂县人民政府",
     "source": "S002"},
    {"id": 8, "name": "雷渊", "gender": "男", "ethnicity": "汉族", "birth": "1977", "birthplace": "待查", "education": "大学本科",
     "current_post": "副县长、县公安局党委书记、局长", "current_org": "盂县公安局",
     "source": "S002"},
    {"id": 9, "name": "冯燕斌", "gender": "男", "ethnicity": "汉族", "birth": "1975", "birthplace": "待查", "education": "大学本科",
     "current_post": "副县长", "current_org": "盂县人民政府",
     "source": "S002"},
    {"id": 10, "name": "蒯平宇", "gender": "男", "ethnicity": "汉族", "birth": "1983", "birthplace": "待查", "education": "工学博士",
     "current_post": "副县长（挂职）", "current_org": "盂县人民政府",
     "source": "S002"},
    {"id": 11, "name": "王贵珠", "gender": "男", "ethnicity": "汉族", "birth": "1983", "birthplace": "待查", "education": "待查",
     "current_post": "副县长", "current_org": "盂县人民政府",
     "source": "S002"},
]

organizations = [
    {"id": 1, "name": "中共盂县委员会", "type": "党委", "level": "县", "parent": "中共阳泉市委", "location": "山西省阳泉市盂县"},
    {"id": 2, "name": "盂县人民政府", "type": "政府", "level": "县", "parent": "阳泉市人民政府", "location": "山西省阳泉市盂县"},
    {"id": 3, "name": "盂县公安局", "type": "政府", "level": "县（部门）", "parent": "盂县人民政府", "location": "山西省阳泉市盂县"},
    {"id": 4, "name": "盂县经济技术开发区", "type": "开发区", "level": "省级", "parent": "盂县人民政府", "location": "山西省阳泉市盂县"},
    {"id": 5, "name": "阳泉市平定县纪委", "type": "党委", "level": "县", "parent": "中共平定县委员会", "location": "山西省阳泉市平定县"},
    {"id": 6, "name": "平定县张庄镇", "type": "政府", "level": "乡镇", "parent": "平定县人民政府", "location": "山西省阳泉市平定县"},
    {"id": 7, "name": "平定县巨城镇", "type": "政府", "level": "乡镇", "parent": "平定县人民政府", "location": "山西省阳泉市平定县"},
    {"id": 8, "name": "平定经济技术开发区", "type": "开发区", "level": "省级", "parent": "平定县人民政府", "location": "山西省阳泉市平定县"},
    {"id": 9, "name": "平定县娘子关镇", "type": "政府", "level": "乡镇", "parent": "平定县人民政府", "location": "山西省阳泉市平定县"},
    {"id": 10, "name": "阳泉市郊区区委/政府", "type": "政府", "level": "县（区）", "parent": "阳泉市人民政府", "location": "山西省阳泉市郊区"},
    {"id": 11, "name": "阳泉市住房和城乡建设局", "type": "政府", "level": "市级", "parent": "阳泉市人民政府", "location": "山西省阳泉市"},
    {"id": 12, "name": "山西出版传媒集团", "type": "企业", "level": "省级", "parent": "山西省国资委", "location": "山西省太原市"},
    {"id": 13, "name": "平定县公安局", "type": "政府", "level": "县（部门）", "parent": "平定县人民政府", "location": "山西省阳泉市平定县"},
    {"id": 14, "name": "阳泉市公安局", "type": "政府", "level": "市级", "parent": "阳泉市人民政府", "location": "山西省阳泉市"},
    {"id": 15, "name": "盂县秀水镇", "type": "政府", "level": "乡镇", "parent": "盂县人民政府", "location": "山西省阳泉市盂县"},
    {"id": 16, "name": "盂县苌池镇", "type": "政府", "level": "乡镇", "parent": "盂县人民政府", "location": "山西省阳泉市盂县"},
    {"id": 17, "name": "盂县仙人乡", "type": "政府", "level": "乡镇", "parent": "盂县人民政府", "location": "山西省阳泉市盂县"},
    {"id": 18, "name": "盂县孙家庄镇", "type": "政府", "level": "乡镇", "parent": "盂县人民政府", "location": "山西省阳泉市盂县"},
    {"id": 19, "name": "盂县东梁乡", "type": "政府", "level": "乡镇", "parent": "盂县人民政府", "location": "山西省阳泉市盂县"},
    {"id": 20, "name": "盂县牛村镇", "type": "政府", "level": "乡镇", "parent": "盂县人民政府", "location": "山西省阳泉市盂县"},
    {"id": 21, "name": "阳泉市郊区西南舁乡", "type": "政府", "level": "乡镇", "parent": "郊区政府", "location": "山西省阳泉市郊区"},
    {"id": 22, "name": "阳泉市郊区李家庄乡", "type": "政府", "level": "乡镇", "parent": "郊区政府", "location": "山西省阳泉市郊区"},
    {"id": 23, "name": "阳泉市郊区河底镇", "type": "政府", "level": "乡镇", "parent": "郊区政府", "location": "山西省阳泉市郊区"},
    {"id": 24, "name": "华阳集团", "type": "企业", "level": "省级", "parent": "山西省国资委", "location": "山西省阳泉市"},
    {"id": 25, "name": "盂县梁家寨乡", "type": "政府", "level": "乡镇", "parent": "盂县人民政府", "location": "山西省阳泉市盂县"},
    {"id": 26, "name": "中共盂县县委宣传部", "type": "党委", "level": "县（部门）", "parent": "中共盂县委员会", "location": "山西省阳泉市盂县"},
    {"id": 27, "name": "阳泉市郊区西南昇乡", "type": "政府", "level": "乡镇", "parent": "郊区政府", "location": "山西省阳泉市郊区"},
    {"id": 28, "name": "中共盂县纪委", "type": "党委", "level": "县", "parent": "中共盂县委员会", "location": "山西省阳泉市盂县"},
    {"id": 29, "name": "中共盂县县委组织部", "type": "党委", "level": "县（部门）", "parent": "中共盂县委员会", "location": "山西省阳泉市盂县"},
]

positions = [
    # 程秀宏 (id=2) — 完整履历
    {"person_id": 2, "org_id": 5, "title": "平定县纪委副书记", "start": "unknown", "end": "unknown", "rank": "副科", "note": "起点岗位"},
    {"person_id": 2, "org_id": 6, "title": "张庄镇党委副书记、镇长", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "巨城镇党委书记", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "张庄镇党委书记（再次）", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "平定经开区管委会副主任", "start": "unknown", "end": "unknown", "rank": "副处", "note": "兼娘子关镇党委书记"},
    {"person_id": 2, "org_id": 9, "title": "娘子关旅游景区管委会主任", "start": "unknown", "end": "unknown", "rank": "副处", "note": "兼娘子关镇党委书记"},
    {"person_id": 2, "org_id": 10, "title": "区委常委、副区长", "start": "unknown", "end": "unknown", "rank": "副处", "note": "阳泉市郊区"},
    {"person_id": 2, "org_id": 11, "title": "党组书记、局长", "start": "unknown", "end": "2025-11", "rank": "正处", "note": "阳泉市住建局"},
    {"person_id": 2, "org_id": 2, "title": "县长、县政府党组书记", "start": "2025-11", "end": "present", "rank": "正处", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2025-11", "end": "present", "rank": "正处", "note": "兼职"},
    {"person_id": 2, "org_id": 4, "title": "县经开区党工委书记", "start": "2025-11", "end": "present", "rank": "正处", "note": "兼职"},

    # 王拥国 (id=1)
    {"person_id": 1, "org_id": 2, "title": "县长（原任）", "start": "unknown", "end": "2025-11", "rank": "正处", "note": "2024年7月起公开活动可见为县长"},
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2025-11", "end": "present", "rank": "正处", "note": "2025-11-03 全省领导干部大会宣布"},
    {"person_id": 1, "org_id": 1, "title": "县委副书记（原任）", "start": "unknown", "end": "2025-11", "rank": "正处", "note": "原任县长时兼任"},

    # 梁海昌 (id=18) — 前县委书记
    {"person_id": 18, "org_id": 1, "title": "县委书记（原任）", "start": "2021?", "end": "2025-07", "rank": "正处", "note": "2025年7月15日最后一次公开活动"},

    # 王珂 (id=3)
    {"person_id": 3, "org_id": 12, "title": "山西出版传媒集团团委副书记/经营部副主任/发行部主任", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长→副县长", "start": "2024?", "end": "present", "rank": "副处", "note": "2026年5月起分工为民生/退役领域"},

    # 郭华 (id=14) — 常务副县长
    {"person_id": 14, "org_id": 2, "title": "县委常委、常务副县长", "start": "2026-05?", "end": "present", "rank": "副处", "note": "接替王珂常务分工"},

    # 李冲 (id=12)
    {"person_id": 12, "org_id": 26, "title": "县委常委、宣传部部长", "start": "unknown", "end": "present", "rank": "副处", "note": ""},

    # 吕世伟 (id=13)
    {"person_id": 13, "org_id": 29, "title": "县委常委、组织部部长", "start": "unknown", "end": "present", "rank": "副处", "note": ""},

    # 连斌 (id=15)
    {"person_id": 15, "org_id": 28, "title": "县委常委、纪委书记（推测中）", "start": "unknown", "end": "present", "rank": "副处", "note": "尚未在公开报道中明确职务"},

    # 韩秀山 (id=4)
    {"person_id": 4, "org_id": 1, "title": "县委台湾工作办公室主任", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 4, "org_id": 16, "title": "苌池镇党委副书记、镇长", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "县政府办公室主任", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 4, "org_id": 15, "title": "秀水镇党委书记", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "县委常委、副县长", "start": "unknown", "end": "present", "rank": "副处", "note": "分管工业/能源/环保"},

    # 李东亮 (id=6)
    {"person_id": 6, "org_id": 17, "title": "仙人乡政法书记/委员", "start": "unknown", "end": "unknown", "rank": "副科", "note": ""},
    {"person_id": 6, "org_id": 17, "title": "仙人乡党委副书记、乡长", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 6, "org_id": 18, "title": "孙家庄镇党委副书记、镇长", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 6, "org_id": 19, "title": "东梁乡党委书记", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 6, "org_id": 20, "title": "牛村镇党委书记", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处", "note": "分管民政/交通/市场监管"},

    # 王雪梅 (id=7)
    {"person_id": 7, "org_id": 25, "title": "梁家寨乡乡长", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "行政审批服务管理局副局长", "start": "unknown", "end": "unknown", "rank": "正科", "note": "九三学社"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处", "note": "分管教育/文旅/卫健"},

    # 雷渊 (id=8)
    {"person_id": 8, "org_id": 13, "title": "平定县公安局经侦大队长/副局长", "start": "unknown", "end": "unknown", "rank": "副科", "note": ""},
    {"person_id": 8, "org_id": 14, "title": "阳泉市公安局监所管理支队支队长", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 8, "org_id": 3, "title": "副县长、县公安局党委书记、局长", "start": "unknown", "end": "present", "rank": "副处", "note": ""},

    # 冯燕斌 (id=9)
    {"person_id": 9, "org_id": 21, "title": "西南舁乡人大主席", "start": "unknown", "end": "unknown", "rank": "正科", "note": "郊区"},
    {"person_id": 9, "org_id": 22, "title": "李家庄乡人大主席", "start": "unknown", "end": "unknown", "rank": "正科", "note": "郊区"},
    {"person_id": 9, "org_id": 10, "title": "区委组织部副部长（郊区）", "start": "unknown", "end": "unknown", "rank": "正科", "note": ""},
    {"person_id": 9, "org_id": 22, "title": "李家庄乡党委副书记、镇长", "start": "unknown", "end": "unknown", "rank": "正科", "note": "郊区"},
    {"person_id": 9, "org_id": 23, "title": "河底镇党委书记", "start": "unknown", "end": "unknown", "rank": "正科", "note": "郊区"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处", "note": "分管住建/自然资源/生态环境"},

    # 王贵珠 (id=11)
    {"person_id": 11, "org_id": 22, "title": "李家庄乡党委副书记、乡长", "start": "unknown", "end": "unknown", "rank": "正科", "note": "郊区"},
    {"person_id": 11, "org_id": 23, "title": "河底镇党委副书记、镇长", "start": "unknown", "end": "unknown", "rank": "正科", "note": "郊区"},
    {"person_id": 11, "org_id": 27, "title": "西南昇乡党委书记", "start": "unknown", "end": "unknown", "rank": "正科", "note": "郊区"},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处", "note": "分管农业农村/乡村振兴"},

    # 艾尼亚尔·艾尼瓦尔 (id=5)
    {"person_id": 5, "org_id": 2, "title": "县委常委、副县长（挂职）", "start": "unknown", "end": "present", "rank": "副处", "note": "新疆伊犁昭苏县委常委、统战部长挂职"},
]

relationships = [
    # 现任书记-县长搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记-县长党政搭档", "overlap_org": "盂县", "overlap_period": "2025-11至今"},
    # 前书记-现书记交接
    {"person_a": 1, "person_b": 18, "type": "predecessor_successor", "context": "王拥国接替梁海昌任县委书记", "overlap_org": "中共盂县委员会", "overlap_period": "2025-07/11交接"},
    # 书记-宣传部长
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "书记-宣传部长", "overlap_org": "中共盂县委员会", "overlap_period": "现任"},
    # 书记-组织部长
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "书记-组织部长", "overlap_org": "中共盂县委员会", "overlap_period": "现任"},
    # 县长-常务副县长
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长-常务副县长", "overlap_org": "盂县人民政府", "overlap_period": "现任"},
    # 县长-公安局长: 同县出身
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县长与公安局长均从平定县调至盂县", "overlap_org": "平定县", "overlap_period": "来盂县前"},
    # 程秀宏-冯燕斌: 跨县调入
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县长与副县长均从外县调入", "overlap_org": "盂县人民政府", "overlap_period": "现任"},
    # 程秀宏-王贵珠: 跨县调入
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "县长与副县长均从外县调入", "overlap_org": "盂县人民政府", "overlap_period": "现任"},
    # 冯燕斌-王贵珠: 同区出身
    {"person_a": 9, "person_b": 11, "type": "overlap", "context": "均从阳泉市郊区调至盂县", "overlap_org": "阳泉市郊区", "overlap_period": "来盂县前"},
    # 韩秀山-李东亮: 盂县本地干部
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "均为盂县本地逐级晋升干部", "overlap_org": "盂县", "overlap_period": "长期"},
    # 王珂-郭华: 常务副县长交接
    {"person_a": 3, "person_b": 14, "type": "predecessor_successor", "context": "王珂此前为常务副县长，2026年5月后郭华接替常务分工", "overlap_org": "盂县人民政府", "overlap_period": "2026交接"},
    # 王珂-山西出版传媒集团
    {"person_a": 3, "person_b": 15, "type": "overlap", "context": "连斌（纪委推测）与王珂（出版集团出身）均为省级单位下派", "overlap_org": "省直系统", "overlap_period": ""},
]

run_build(
    slug=slug,
    persons=persons,
    organizations=organizations,
    positions=positions,
    relationships=relationships,
    db_path="/workspace/data/xieming/other-codes/gov-relation/data/tmp/shanxi_盂县/盂县_network.db",
    gexf_path="/workspace/data/xieming/other-codes/gov-relation/data/tmp/shanxi_盂县/盂县_network.gexf",
    overwrite=True,
)
print("\n=== Build complete! ===")
print(f"Persons: {len(persons)}")
print(f"Organizations: {len(organizations)}")
print(f"Positions: {len(positions)}")
print(f"Relationships: {len(relationships)}")
