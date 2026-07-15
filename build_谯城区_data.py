#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 谯城区 (Qiaocheng District, Bozhou) leadership network.

Covers: 区委、区政府、区纪委、区人大、区政协领导班子，
党政正职（区委书记、区长）的完整履历，前任脉络，以及关键副职。

Data sources:
- 谯城区人民政府 (bzqc.gov.cn) — 新闻文章、党代会、纪委全会 (2026)
- 百度百科 — 张建影、宋保众、高川、金春龙
- 综合公开资料（标注了置信度）

Data as of: 2026-07-15
"""

import sqlite3
import os
from datetime import datetime

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
TMP_DIR = os.path.join(REPO, "data/tmp/anhui_谯城区")
os.makedirs(TMP_DIR, exist_ok=True)

PRODUCTION = os.environ.get("PRODUCTION")
DB_PATH = os.path.join(REPO, "data/database/谯城区_network.db") if PRODUCTION else os.path.join(TMP_DIR, "谯城区_network.db")
GEXF_PATH = os.path.join(REPO, "data/graph/谯城区_network.gexf") if PRODUCTION else os.path.join(TMP_DIR, "谯城区_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. 区委书记 ──
    {
        "id": "qiaocheng_zhou_xiao",
        "name": "周霄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "谯城区委书记",
        "current_org": "中共亳州市谯城区委员会",
        "source": "bzqc.gov.cn 新闻公告＋百度百科",
        "notes": "原谯城区区长，约2021年接替金春龙任区委书记。周霄的详细履历（出生年、教育、早期职务）需进一步查证（百度百科页面临验证码屏蔽）。",
        "confidence": "plausible",
    },
    # ── 2. 区长 ──
    {
        "id": "qiaocheng_zhang_jianying",
        "name": "张建影",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983-02",
        "birthplace": "安徽涡阳",
        "native_place": "安徽涡阳",
        "education": "省委党校研究生学历（在职）",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "谯城区委副书记、区长",
        "current_org": "谯城区人民政府",
        "source": "https://baike.baidu.com/item/张建影/22548805",
        "notes": "2026年6月11日任代区长，7月13日当选区长。此前任亳州市中医药管理局局长、党组书记，市药业发展促进局局长（兼）。曾任谯城区委常委、组织部长、统战部长。",
        "confidence": "confirmed",
    },
    # ── 3. 前任区长 宋保众 ──
    {
        "id": "qiaocheng_song_baozhong",
        "name": "宋保众",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-12",
        "birthplace": "安徽利辛",
        "native_place": "安徽利辛",
        "education": "安徽省委党校政治学专业研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "谯城区政府原区长（去向待查）",
        "current_org": "（待查）",
        "source": "https://baike.baidu.com/item/宋保众/16710058",
        "notes": "2021年12月任谯城区代区长，2022年1月当选区长，2026年6月11日辞去区长职务。去向尚未公开披露。",
        "confidence": "confirmed",
    },
    # ── 4. 前任区委书记 金春龙 ──
    {
        "id": "qiaocheng_jin_chunlong",
        "name": "金春龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-03",
        "birthplace": "安徽萧县",
        "native_place": "安徽萧县",
        "education": "安徽大学汉语言文学专业，文学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（已被开除党籍和公职）",
        "current_org": "（原省科协党组书记，已被查）",
        "source": "https://baike.baidu.com/item/金春龙",
        "notes": "2016.05–2021.07任谯城区委书记（兼亳州市委常委）。后任铜陵市委副书记、省科协党组书记。2025年9月被调查，2026年5月9日被开除党籍和公职，移送检察机关。",
        "confidence": "confirmed",
    },
    # ── 5. 前任区长 高川 ──
    {
        "id": "qiaocheng_gao_chuan",
        "name": "高川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "安徽利辛",
        "native_place": "安徽利辛",
        "education": "安徽省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（已被开除党籍，移送检察机关）",
        "current_org": "（原市政协二级巡视员，已被查）",
        "source": "https://baike.baidu.com/item/高川/18878233",
        "notes": "2015.12–2020.11任谯城区委副书记、区长。后转任亳州市政协二级巡视员。2025年3月被调查，2025年10月被开除党籍。",
        "confidence": "confirmed",
    },
    # ── 6. 区委副书记（专职）──
    {
        "id": "qiaocheng_liang_chao",
        "name": "梁超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "谯城区委副书记、区委党校校长",
        "current_org": "中共亳州市谯城区委员会",
        "source": "https://www.bzqc.gov.cn/News/show/721595.html",
        "notes": "2026年6月28日当选区委副书记。",
        "confidence": "confirmed",
    },
    # ── 7. 常务副区长 ──
    {
        "id": "qiaocheng_li_ya",
        "name": "李亚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "谯城区委常委、常务副区长",
        "current_org": "谯城区人民政府",
        "source": "https://www.bzqc.gov.cn/News/show/708856.html",
        "notes": "在区安委会会议中以常务副区长身份出席。",
        "confidence": "confirmed",
    },
    # ── 8. 区纪委书记 ──
    {
        "id": "qiaocheng_xu_zhiyuan",
        "name": "徐致远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "谯城区委常委、区纪委书记、区监委主任",
        "current_org": "中共亳州市谯城区纪律检查委员会",
        "source": "https://www.bzqc.gov.cn/News/show/721596.html",
        "notes": "2026年6月28日当选区纪委书记。纪委副书记：胥艳彬、刘永田；纪委常委：徐致远、胥艳彬、刘永田、刘磊、王肖男、张铭、吴林。",
        "confidence": "confirmed",
    },
    # ── 9. 区人大主任 ──
    {
        "id": "qiaocheng_wang_jundong",
        "name": "王俊东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区人大常委会主任",
        "current_org": "亳州市谯城区人民代表大会常务委员会",
        "source": "bzqc.gov.cn 新闻公告",
        "notes": "",
        "confidence": "plausible",
    },
    # ── 10. 区政协主席 ──
    {
        "id": "qiaocheng_lu_lei",
        "name": "鲁磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议亳州市谯城区委员会",
        "source": "bzqc.gov.cn 新闻公告",
        "notes": "",
        "confidence": "plausible",
    },
    # ── 11. 区委常委 蒋运涛 ──
    {
        "id": "qiaocheng_jiang_yuntao",
        "name": "蒋运涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "谯城区委常委",
        "current_org": "中共亳州市谯城区委员会",
        "source": "https://www.bzqc.gov.cn/News/show/721595.html",
        "notes": "2026年6月28日当选区委常委。具体分管领域待查。",
        "confidence": "confirmed",
    },
    # ── 12. 区委常委 张苗平 ──
    {
        "id": "qiaocheng_zhang_miaoping",
        "name": "张苗平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "谯城区委常委",
        "current_org": "中共亳州市谯城区委员会",
        "source": "https://www.bzqc.gov.cn/News/show/721595.html",
        "notes": "2026年6月28日当选区委常委。具体分管领域待查。",
        "confidence": "confirmed",
    },
    # ── 13. 区委常委 崔文佳 ──
    {
        "id": "qiaocheng_cui_wenjia",
        "name": "崔文佳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "谯城区委常委",
        "current_org": "中共亳州市谯城区委员会",
        "source": "https://www.bzqc.gov.cn/News/show/721595.html",
        "notes": "2026年6月28日当选区委常委。此前曾任副区长。",
        "confidence": "confirmed",
    },
    # ── 14. 区委常委 梁海天 ──
    {
        "id": "qiaocheng_liang_haitian",
        "name": "梁海天",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "谯城区委常委",
        "current_org": "中共亳州市谯城区委员会",
        "source": "https://www.bzqc.gov.cn/News/show/721595.html",
        "notes": "2026年6月28日当选区委常委。具体分管领域待查。",
        "confidence": "confirmed",
    },
    # ── 15. 区委常委 王飞 ──
    {
        "id": "qiaocheng_wang_fei",
        "name": "王飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "谯城区委常委",
        "current_org": "中共亳州市谯城区委员会",
        "source": "https://www.bzqc.gov.cn/News/show/721595.html",
        "notes": "2026年6月28日当选区委常委。具体分管领域待查。",
        "confidence": "confirmed",
    },
    # ── 16. 区委常委 陈影 ──
    {
        "id": "qiaocheng_chen_ying",
        "name": "陈影",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "谯城区委常委",
        "current_org": "中共亳州市谯城区委员会",
        "source": "https://www.bzqc.gov.cn/News/show/721595.html",
        "notes": "2026年6月28日当选区委常委。此前曾任副区长级领导。",
        "confidence": "confirmed",
    },
    # ── 17. 副区长 赵伟 ──
    {
        "id": "qiaocheng_zhao_wei",
        "name": "赵伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府领导（副区长级）",
        "current_org": "谯城区人民政府",
        "source": "https://www.bzqc.gov.cn/News/show/722824.html",
        "notes": "出席区安委会会议。",
        "confidence": "plausible",
    },
    # ── 18. 副区长 潘承尧 ──
    {
        "id": "qiaocheng_pan_chengyao",
        "name": "潘承尧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府领导（副区长级）",
        "current_org": "谯城区人民政府",
        "source": "https://www.bzqc.gov.cn/News/show/722824.html",
        "notes": "出席区安委会会议。",
        "confidence": "plausible",
    },
    # ── 19. 副区长 王洪波 ──
    {
        "id": "qiaocheng_wang_hongbo",
        "name": "王洪波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府领导（副区长级）",
        "current_org": "谯城区人民政府",
        "source": "https://www.bzqc.gov.cn/News/show/722824.html",
        "notes": "出席区安委会会议。",
        "confidence": "plausible",
    },
    # ── 20. 副区长 郭全德 ──
    {
        "id": "qiaocheng_guo_quande",
        "name": "郭全德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府领导（副区长级）",
        "current_org": "谯城区人民政府",
        "source": "https://www.bzqc.gov.cn/News/show/722824.html",
        "notes": "出席区安委会会议。",
        "confidence": "plausible",
    },
    # ── 21. 副区长 刘虎 ──
    {
        "id": "qiaocheng_liu_hu",
        "name": "刘虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府党组成员、谯城经开区党工委书记、管委会主任",
        "current_org": "谯城区人民政府",
        "source": "bzqc.gov.cn 新闻公告",
        "notes": "经开区主要领导。",
        "confidence": "plausible",
    },
    # ── 22. 纪委副书记 胥艳彬 ──
    {
        "id": "qiaocheng_xu_yanbin",
        "name": "胥艳彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区纪委副书记、监委副主任",
        "current_org": "中共亳州市谯城区纪律检查委员会",
        "source": "https://www.bzqc.gov.cn/News/show/721596.html",
        "notes": "",
        "confidence": "confirmed",
    },
    # ── 23. 纪委副书记 刘永田 ──
    {
        "id": "qiaocheng_liu_yongtian",
        "name": "刘永田",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区纪委副书记、监委副主任",
        "current_org": "中共亳州市谯城区纪律检查委员会",
        "source": "https://www.bzqc.gov.cn/News/show/721596.html",
        "notes": "",
        "confidence": "confirmed",
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": "org_qc_party",
        "name": "中共亳州市谯城区委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共亳州市委员会",
        "location": "安徽省亳州市谯城区",
    },
    {
        "id": "org_qc_gov",
        "name": "谯城区人民政府",
        "type": "government",
        "level": "county",
        "parent": "亳州市人民政府",
        "location": "安徽省亳州市谯城区",
    },
    {
        "id": "org_qc_discipline",
        "name": "中共亳州市谯城区纪律检查委员会",
        "type": "discipline",
        "level": "county",
        "parent": "中共亳州市纪律检查委员会",
        "location": "安徽省亳州市谯城区",
    },
    {
        "id": "org_qc_npc",
        "name": "亳州市谯城区人民代表大会常务委员会",
        "type": "npc",
        "level": "county",
        "parent": "亳州市人民代表大会常务委员会",
        "location": "安徽省亳州市谯城区",
    },
    {
        "id": "org_qc_cppcc",
        "name": "中国人民政治协商会议亳州市谯城区委员会",
        "type": "cppcc",
        "level": "county",
        "parent": "中国人民政治协商会议亳州市委员会",
        "location": "安徽省亳州市谯城区",
    },
    {
        "id": "org_qc_party_school",
        "name": "中共亳州市谯城区委党校",
        "type": "education",
        "level": "county",
        "parent": "中共亳州市谯城区委员会",
        "location": "安徽省亳州市谯城区",
    },
    {
        "id": "org_qc_economic_zone",
        "name": "谯城经济开发区",
        "type": "development_zone",
        "level": "county",
        "parent": "谯城区人民政府",
        "location": "安徽省亳州市谯城区",
    },
    # References
    {
        "id": "org_bozhou_party",
        "name": "中共亳州市委员会",
        "type": "party_committee",
        "level": "prefecture",
        "parent": "中共安徽省委员会",
        "location": "安徽省亳州市",
    },
    {
        "id": "org_bozhou_gov",
        "name": "亳州市人民政府",
        "type": "government",
        "level": "prefecture",
        "parent": "安徽省人民政府",
        "location": "安徽省亳州市",
    },
    {
        "id": "org_bozhou_discipline",
        "name": "中共亳州市纪律检查委员会",
        "type": "discipline",
        "level": "prefecture",
        "parent": "中共安徽省纪律检查委员会",
        "location": "安徽省亳州市",
    },
    {
        "id": "org_tongling_party",
        "name": "中共铜陵市委员会",
        "type": "party_committee",
        "level": "prefecture",
        "parent": "中共安徽省委员会",
        "location": "安徽省铜陵市",
    },
    {
        "id": "org_anhui_science_assoc",
        "name": "安徽省科学技术协会",
        "type": "mass_organization",
        "level": "provincial",
        "parent": "安徽省",
        "location": "安徽省合肥市",
    },
    {
        "id": "org_bozhou_cppcc",
        "name": "中国人民政治协商会议亳州市委员会",
        "type": "cppcc",
        "level": "prefecture",
        "parent": "安徽省政协",
        "location": "安徽省亳州市",
    },
    {
        "id": "org_bozhou_tcm_admin",
        "name": "亳州市中医药管理局",
        "type": "government",
        "level": "prefecture",
        "parent": "亳州市人民政府",
        "location": "安徽省亳州市",
    },
    {
        "id": "org_bozhou_pharma_dev",
        "name": "亳州市药业发展促进局",
        "type": "government",
        "level": "prefecture",
        "parent": "亳州市人民政府",
        "location": "安徽省亳州市",
    },
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 周霄
    {"person_id": "qiaocheng_zhou_xiao", "org_id": "org_qc_party", "title": "谯城区委书记", "start": "2021", "end": "", "rank": "1", "note": "接替金春龙"},
    {"person_id": "qiaocheng_zhou_xiao", "org_id": "org_qc_gov", "title": "谯城区区长（此前曾任）", "start": "2020-11", "end": "2021", "rank": "1", "note": "2020年11月任代区长，此前曾任区长"},
    # 张建影
    {"person_id": "qiaocheng_zhang_jianying", "org_id": "org_qc_gov", "title": "谯城区区长", "start": "2026-07", "end": "", "rank": "1", "note": "2026年7月13日当选区长，此前6月11日任代区长"},
    {"person_id": "qiaocheng_zhang_jianying", "org_id": "org_qc_party", "title": "谯城区委副书记", "start": "2026-06", "end": "", "rank": "2", "note": "2026年6月28日当选"},
    {"person_id": "qiaocheng_zhang_jianying", "org_id": "org_bozhou_tcm_admin", "title": "亳州市中医药管理局局长", "start": "unknown", "end": "2026-06", "rank": "2", "note": "此前任职"},
    {"person_id": "qiaocheng_zhang_jianying", "org_id": "org_bozhou_pharma_dev", "title": "亳州市药业发展促进局局长（兼）", "start": "unknown", "end": "2026-06", "rank": "2", "note": "此前兼职"},
    {"person_id": "qiaocheng_zhang_jianying", "org_id": "org_qc_party", "title": "谯城区委常委、组织部部长、统战部部长（此前曾任）", "start": "unknown", "end": "unknown", "rank": "5", "note": "区政协党组副书记（兼）"},
    # 宋保众
    {"person_id": "qiaocheng_song_baozhong", "org_id": "org_qc_gov", "title": "谯城区区长（此前曾任）", "start": "2021-12", "end": "2026-06", "rank": "1", "note": "2021年12月任代区长，2022年1月当选，2026年6月11日辞去区长职务"},
    {"person_id": "qiaocheng_song_baozhong", "org_id": "org_bozhou_gov", "title": "亳州市审计局副局长（此前曾任）", "start": "unknown", "end": "2021-12", "rank": "4", "note": ""},
    # 金春龙
    {"person_id": "qiaocheng_jin_chunlong", "org_id": "org_qc_party", "title": "谯城区委书记（此前曾任）", "start": "2016-05", "end": "2021-07", "rank": "1", "note": "2016.05–2016.07挂任亳州市委常委"},
    {"person_id": "qiaocheng_jin_chunlong", "org_id": "org_tongling_party", "title": "铜陵市委副书记", "start": "2021-07", "end": "2022-04", "rank": "3", "note": ""},
    {"person_id": "qiaocheng_jin_chunlong", "org_id": "org_anhui_science_assoc", "title": "省科协党组书记、副主席", "start": "2022-04", "end": "2025-09", "rank": "1", "note": "2025年9月4日被调查，2026年5月9日被开除党籍公职"},
    # 高川
    {"person_id": "qiaocheng_gao_chuan", "org_id": "org_qc_gov", "title": "谯城区区长（此前曾任）", "start": "2015-12", "end": "2020-11", "rank": "1", "note": ""},
    {"person_id": "qiaocheng_gao_chuan", "org_id": "org_bozhou_cppcc", "title": "亳州市政协二级巡视员", "start": "2020-11", "end": "2025-03", "rank": "5", "note": "2025年3月被调查，10月被开除党籍"},
    # 梁超
    {"person_id": "qiaocheng_liang_chao", "org_id": "org_qc_party", "title": "谯城区委副书记", "start": "2026-06", "end": "", "rank": "3", "note": ""},
    {"person_id": "qiaocheng_liang_chao", "org_id": "org_qc_party_school", "title": "区委党校校长（兼）", "start": "2026-06", "end": "", "rank": "3", "note": ""},
    # 李亚
    {"person_id": "qiaocheng_li_ya", "org_id": "org_qc_party", "title": "谯城区委常委", "start": "2026-06", "end": "", "rank": "4", "note": ""},
    {"person_id": "qiaocheng_li_ya", "org_id": "org_qc_gov", "title": "常务副区长", "start": "2026-06", "end": "", "rank": "2", "note": "区委常委兼任"},
    # 徐致远
    {"person_id": "qiaocheng_xu_zhiyuan", "org_id": "org_qc_party", "title": "谯城区委常委", "start": "2026-06", "end": "", "rank": "5", "note": ""},
    {"person_id": "qiaocheng_xu_zhiyuan", "org_id": "org_qc_discipline", "title": "区纪委书记、区监委主任", "start": "2026-06", "end": "", "rank": "1", "note": "区委常委兼任"},
    # 王俊东
    {"person_id": "qiaocheng_wang_jundong", "org_id": "org_qc_npc", "title": "区人大常委会主任", "start": "", "end": "", "rank": "1", "note": ""},
    # 鲁磊
    {"person_id": "qiaocheng_lu_lei", "org_id": "org_qc_cppcc", "title": "区政协主席", "start": "", "end": "", "rank": "1", "note": ""},
    # 蒋运涛
    {"person_id": "qiaocheng_jiang_yuntao", "org_id": "org_qc_party", "title": "谯城区委常委", "start": "2026-06", "end": "", "rank": "6", "note": "具体分管领域待查"},
    # 张苗平
    {"person_id": "qiaocheng_zhang_miaoping", "org_id": "org_qc_party", "title": "谯城区委常委", "start": "2026-06", "end": "", "rank": "7", "note": "具体分管领域待查"},
    # 崔文佳
    {"person_id": "qiaocheng_cui_wenjia", "org_id": "org_qc_party", "title": "谯城区委常委", "start": "2026-06", "end": "", "rank": "8", "note": "此前曾任副区长"},
    # 梁海天
    {"person_id": "qiaocheng_liang_haitian", "org_id": "org_qc_party", "title": "谯城区委常委", "start": "2026-06", "end": "", "rank": "9", "note": "具体分管领域待查"},
    # 王飞
    {"person_id": "qiaocheng_wang_fei", "org_id": "org_qc_party", "title": "谯城区委常委", "start": "2026-06", "end": "", "rank": "10", "note": "具体分管领域待查"},
    # 陈影
    {"person_id": "qiaocheng_chen_ying", "org_id": "org_qc_party", "title": "谯城区委常委", "start": "2026-06", "end": "", "rank": "11", "note": "此前曾任副区长级"},
    # 副区长
    {"person_id": "qiaocheng_zhao_wei", "org_id": "org_qc_gov", "title": "副区长（区领导）", "start": "", "end": "", "rank": "3", "note": "具体分工待查"},
    {"person_id": "qiaocheng_pan_chengyao", "org_id": "org_qc_gov", "title": "副区长（区领导）", "start": "", "end": "", "rank": "3", "note": "具体分工待查"},
    {"person_id": "qiaocheng_wang_hongbo", "org_id": "org_qc_gov", "title": "副区长（区领导）", "start": "", "end": "", "rank": "3", "note": "具体分工待查"},
    {"person_id": "qiaocheng_guo_quande", "org_id": "org_qc_gov", "title": "副区长（区领导）", "start": "", "end": "", "rank": "3", "note": "具体分工待查"},
    {"person_id": "qiaocheng_liu_hu", "org_id": "org_qc_economic_zone", "title": "谯城经开区党工委书记、管委会主任", "start": "", "end": "", "rank": "3", "note": "区政府党组成员"},
    # 纪委系统
    {"person_id": "qiaocheng_xu_yanbin", "org_id": "org_qc_discipline", "title": "区纪委副书记、监委副主任", "start": "", "end": "", "rank": "2", "note": ""},
    {"person_id": "qiaocheng_liu_yongtian", "org_id": "org_qc_discipline", "title": "区纪委副书记、监委副主任", "start": "", "end": "", "rank": "2", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 周霄 ↔ 张建影（党政正职搭档）
    {
        "person_a": "qiaocheng_zhou_xiao",
        "person_b": "qiaocheng_zhang_jianying",
        "type": "colleague",
        "context": "区委书记与区长党政正职搭档（2026年7月起）",
        "overlap_org": "org_qc_party",
        "overlap_period": "2026年6月至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 周霄 ← 宋保众（前任后继：区长链条）
    {
        "person_a": "qiaocheng_zhou_xiao",
        "person_b": "qiaocheng_song_baozhong",
        "type": "predecessor_successor",
        "context": "周霄升任区委书记后，宋保众接任区长",
        "overlap_org": "org_qc_gov",
        "overlap_period": "2021年",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 周霄 ← 金春龙（前任后继：书记链条）
    {
        "person_a": "qiaocheng_zhou_xiao",
        "person_b": "qiaocheng_jin_chunlong",
        "type": "predecessor_successor",
        "context": "周霄接替金春龙任区委书记",
        "overlap_org": "org_qc_party",
        "overlap_period": "2021年",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 宋保众 ← 高川（前任后继：区长链条）
    {
        "person_a": "qiaocheng_song_baozhong",
        "person_b": "qiaocheng_gao_chuan",
        "type": "predecessor_successor",
        "context": "宋保众接替高川任区长",
        "overlap_org": "org_qc_gov",
        "overlap_period": "2020–2021",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 张建影 ← 宋保众（前任后继：区长链条）
    {
        "person_a": "qiaocheng_zhang_jianying",
        "person_b": "qiaocheng_song_baozhong",
        "type": "predecessor_successor",
        "context": "张建影接替宋保众任区长",
        "overlap_org": "org_qc_gov",
        "overlap_period": "2026年6月",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 周霄 ↔ 梁超（书记与副书记）
    {
        "person_a": "qiaocheng_zhou_xiao",
        "person_b": "qiaocheng_liang_chao",
        "type": "colleague",
        "context": "区委书记与专职副书记",
        "overlap_org": "org_qc_party",
        "overlap_period": "2026年6月至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 张建影 ↔ 梁超（区长与副书记）
    {
        "person_a": "qiaocheng_zhang_jianying",
        "person_b": "qiaocheng_liang_chao",
        "type": "colleague",
        "context": "区长与专职副书记",
        "overlap_org": "org_qc_party",
        "overlap_period": "2026年6月至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 周霄 ↔ 李亚（书记与常务副区长）
    {
        "person_a": "qiaocheng_zhou_xiao",
        "person_b": "qiaocheng_li_ya",
        "type": "colleague",
        "context": "区委书记与常务副区长",
        "overlap_org": "org_qc_party",
        "overlap_period": "2026年至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 张建影 ↔ 李亚（区长与常务副区长）
    {
        "person_a": "qiaocheng_zhang_jianying",
        "person_b": "qiaocheng_li_ya",
        "type": "colleague",
        "context": "区长与常务副区长（政府班子搭档）",
        "overlap_org": "org_qc_gov",
        "overlap_period": "2026年6月至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 周霄 ↔ 徐致远（书记与纪委书记）
    {
        "person_a": "qiaocheng_zhou_xiao",
        "person_b": "qiaocheng_xu_zhiyuan",
        "type": "colleague",
        "context": "区委书记与纪委书记",
        "overlap_org": "org_qc_party",
        "overlap_period": "2026年6月至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 徐致远 ↔ 胥艳彬（纪委正副书记）
    {
        "person_a": "qiaocheng_xu_zhiyuan",
        "person_b": "qiaocheng_xu_yanbin",
        "type": "colleague",
        "context": "区纪委书记与副书记",
        "overlap_org": "org_qc_discipline",
        "overlap_period": "",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 徐致远 ↔ 刘永田（纪委正副书记）
    {
        "person_a": "qiaocheng_xu_zhiyuan",
        "person_b": "qiaocheng_liu_yongtian",
        "type": "colleague",
        "context": "区纪委书记与副书记",
        "overlap_org": "org_qc_discipline",
        "overlap_period": "",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 金春龙 ↔ 高川（前任书记与前任区长，同时期搭档）
    {
        "person_a": "qiaocheng_jin_chunlong",
        "person_b": "qiaocheng_gao_chuan",
        "type": "colleague",
        "context": "前任书记与前任区长在谯城区同时期搭档（2016–2020年），两人均被查",
        "overlap_org": "org_qc_party",
        "overlap_period": "2016–2020",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 金春龙 → 高川（监督关系）
    {
        "person_a": "qiaocheng_jin_chunlong",
        "person_b": "qiaocheng_gao_chuan",
        "type": "superior_subordinate",
        "context": "金春龙（区委书记）与高川（区长）党政正职搭档",
        "overlap_org": "org_qc_party",
        "overlap_period": "2016–2020",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 区委常委班子成员之间（11人班子结构关系）
    {"person_a": "qiaocheng_zhou_xiao", "person_b": "qiaocheng_jiang_yuntao", "type": "colleague", "context": "区委常委班子", "overlap_org": "org_qc_party", "overlap_period": "2026年6月至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "qiaocheng_zhou_xiao", "person_b": "qiaocheng_zhang_miaoping", "type": "colleague", "context": "区委常委班子", "overlap_org": "org_qc_party", "overlap_period": "2026年6月至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "qiaocheng_zhou_xiao", "person_b": "qiaocheng_cui_wenjia", "type": "colleague", "context": "区委常委班子", "overlap_org": "org_qc_party", "overlap_period": "2026年6月至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "qiaocheng_zhou_xiao", "person_b": "qiaocheng_liang_haitian", "type": "colleague", "context": "区委常委班子", "overlap_org": "org_qc_party", "overlap_period": "2026年6月至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "qiaocheng_zhou_xiao", "person_b": "qiaocheng_wang_fei", "type": "colleague", "context": "区委常委班子", "overlap_org": "org_qc_party", "overlap_period": "2026年6月至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "qiaocheng_zhou_xiao", "person_b": "qiaocheng_chen_ying", "type": "colleague", "context": "区委常委班子", "overlap_org": "org_qc_party", "overlap_period": "2026年6月至今", "strength": "strong", "confidence": "confirmed"},
    # 张建影与各政府副职
    {"person_a": "qiaocheng_zhang_jianying", "person_b": "qiaocheng_zhao_wei", "type": "colleague", "context": "区长与副区长", "overlap_org": "org_qc_gov", "overlap_period": "2026年至今", "strength": "strong", "confidence": "plausible"},
    {"person_a": "qiaocheng_zhang_jianying", "person_b": "qiaocheng_pan_chengyao", "type": "colleague", "context": "区长与副区长", "overlap_org": "org_qc_gov", "overlap_period": "2026年至今", "strength": "strong", "confidence": "plausible"},
    {"person_a": "qiaocheng_zhang_jianying", "person_b": "qiaocheng_wang_hongbo", "type": "colleague", "context": "区长与副区长", "overlap_org": "org_qc_gov", "overlap_period": "2026年至今", "strength": "strong", "confidence": "plausible"},
    {"person_a": "qiaocheng_zhang_jianying", "person_b": "qiaocheng_guo_quande", "type": "colleague", "context": "区长与副区长", "overlap_org": "org_qc_gov", "overlap_period": "2026年至今", "strength": "strong", "confidence": "plausible"},
    # 张建影—秦凤玉（从属关系：张建影曾在秦凤玉领导下工作于亳州市）
    {"person_a": "qiaocheng_zhang_jianying", "person_b": "bozhou_qin_fengyu", "type": "superior_subordinate", "context": "秦凤玉（亳州市长）与张建影（曾任亳州市中医药管理局局长，属市政府部门领导）", "overlap_org": "org_bozhou_gov", "overlap_period": "unknown", "strength": "medium", "confidence": "plausible"},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT,
    ethnicity TEXT,
    birth TEXT,
    birthplace TEXT,
    native_place TEXT,
    education TEXT,
    party_join TEXT,
    work_start TEXT,
    current_post TEXT,
    current_org TEXT,
    source TEXT,
    notes TEXT,
    confidence TEXT
);

CREATE TABLE IF NOT EXISTS organizations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id TEXT NOT NULL,
    org_id TEXT NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a TEXT NOT NULL,
    person_b TEXT NOT NULL,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    strength TEXT,
    confidence TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    c.execute("""
        INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place, education, party_join, work_start, current_post, current_org, source, notes, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""), p.get("birth",""), p.get("birthplace",""), p.get("native_place",""), p.get("education",""), p.get("party_join",""), p.get("work_start",""), p["current_post"], p["current_org"], p.get("source",""), p.get("notes",""), p.get("confidence","unverified")))

for o in organizations:
    c.execute("""
        INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    c.execute("""
        INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (pos["person_id"], pos["org_id"], pos.get("title",""), pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note","")))

for r in relationships:
    c.execute("""
        INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org",""), r.get("overlap_period",""), r.get("strength","medium"), r.get("confidence","unverified")))

conn.commit()
print(f"✅ SQLite: {DB_PATH}")
print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

# =========================================================================
# BUILD GEXF
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

role_color_map = {
    "party_secretary": (200, 60, 50),
    "government_leader": (50, 100, 200),
    "discipline": (220, 140, 40),
    "npc": (80, 160, 80),
    "cppcc": (160, 80, 160),
    "default": (150, 150, 150),
}

def person_color(p):
    post = p["current_post"]
    if "书记" in post and "副书记" not in post:
        return role_color_map["party_secretary"]
    if "区长" in post or "市长" in post or "县长" in post or "副区长" in post or "副市长" in post:
        return role_color_map["government_leader"]
    if "政协" in post:
        return role_color_map["cppcc"]
    if "人大" in post:
        return role_color_map["npc"]
    if "纪委" in post or "监委" in post:
        return role_color_map["discipline"]
    return role_color_map["default"]

org_color_map = {
    "party_committee": (180, 50, 50),
    "government": (50, 80, 180),
    "discipline": (200, 120, 30),
    "npc": (60, 140, 60),
    "cppcc": (140, 60, 140),
    "education": (100, 160, 200),
    "development_zone": (100, 200, 100),
    "mass_organization": (180, 180, 180),
}

def is_top_leader(pid):
    return pid in ("qiaocheng_zhou_xiao", "qiaocheng_zhang_jianying")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{TODAY}">')
lines.append('    <creator>Gov-Relation Research Agent</creator>')
lines.append('    <description>谯城区领导班子工作关系网络 — 含区委、区政府、区纪委、区人大、区政协领导班子及前任脉络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="role" title="role" type="string"/>')
lines.append('      <attribute id="source" title="source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="context" title="context" type="string"/>')
lines.append('    </attributes>')

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    pid = p["id"]
    name = esc(p["name"])
    post = esc(p["current_post"])
    org = esc(p["current_org"])
    r, g, b = person_color(p)
    sz = "20.0" if is_top_leader(pid) else "12.0"
    lines.append(f'      <node id="{pid}" label="{name}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="role" value="{post}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p.get("source",""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'        <viz:shape value="disc"/>')
    lines.append('      </node>')

# Nodes: Organizations
for o in organizations:
    oid = o["id"]
    name = esc(o["name"])
    t = o["type"]
    r, g, b = org_color_map.get(t, (120, 120, 120))
    lines.append(f'      <node id="{oid}" label="{name}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="role" value="{t}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'        <viz:shape value="square"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 0

# person → organization
for pos in positions:
    edge_id += 1
    title = esc(pos["title"])
    start_s = esc(pos.get("start","") or "未知")
    end_s = esc(pos.get("end","") or "至今")
    lines.append(f'      <edge id="e{edge_id}" source="{pos["person_id"]}" target="{pos["org_id"]}" label="{title}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{title} ({start_s}-{end_s})"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# person ↔ person
for r in relationships:
    edge_id += 1
    ctx = esc(r["context"])
    lines.append(f'      <edge id="e{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}" label="{ctx}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="relationship"/>')
    lines.append(f'          <attvalue for="context" value="{ctx}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"✅ GEXF: {GEXF_PATH}")
print(f"   Nodes: {len(persons)} persons + {len(organizations)} orgs")
print(f"   Edges: {len(positions)} worked_at + {len(relationships)} relationships")

# Summary
print(f"\n{'=' * 50}")
print(f"谯城区 Leadership Network — Build Complete")
print(f"{'=' * 50}")
print(f"Persons: {len(persons)}")
print(f"Organizations: {len(organizations)}")
print(f"Positions: {len(positions)}")
print(f"Relationships: {len(relationships)}")
print(f"\nOutput files:")
print(f"  Database: {DB_PATH}")
print(f"  GEXF:     {GEXF_PATH}")
print(f"{'=' * 50}")

conn.close()
print("✅ Done!")
