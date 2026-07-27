#!/usr/bin/env python3
"""青浦区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区(直辖市)
调查日期: 2026-07-25
信息来源:
  - 上海市青浦区人民政府网站 (www.shqp.gov.cn) 领导之窗
  - 各领导详细简历页面
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Find project root: walk up looking for gov_relation/
PROJECT_ROOT = HERE
for _ in range(10):
    if (PROJECT_ROOT / "gov_relation").is_dir():
        break
    PROJECT_ROOT = PROJECT_ROOT.parent
else:
    PROJECT_ROOT = HERE.parents[2]  # fallback

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "青浦区"
TODAY = "2026-07-25"

STAGING = HERE
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# Canonical destinations (always relative to project root)
CANONICAL_DB = PROJECT_ROOT / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = PROJECT_ROOT / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = PROJECT_ROOT / "scripts" / "build" / f"build_{SLUG}_data.py"
CANONICAL_ROOT_BUILD = PROJECT_ROOT / f"build_{SLUG}_data.py"

# ── Persons ──────────────────────────────────────────────────────────────────
# ID ranges: 1xxx = party committee, 2xxx = government, 3xxx = congress,
#            4xxx = cppcc, 5xxx = judiciary

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 区委领导班子
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 王平 — 区委书记
    {
        "id": 1001,
        "name": "王平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "",
        "education": "中央党校研究生，法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区委书记",
        "current_org": "中共上海市青浦区委员会",
        "source": "https://www.shqp.gov.cn/shqp/qwld/20250527/1282241.html",
    },
    # 2. 金晓明 — 区委副书记、区长
    {
        "id": 1002,
        "name": "金晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "",
        "education": "大学，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区委副书记、区长",
        "current_org": "上海市青浦区人民政府",
        "source": "https://www.shqp.gov.cn/shqp/qwld/20241017/1214527.html",
    },
    # 3. 刘琪 — 区委副书记、党校校长
    {
        "id": 1003,
        "name": "刘琪",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "",
        "education": "大学，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区委副书记，区委党校校长、校务委员会主任",
        "current_org": "中共上海市青浦区委员会",
        "source": "https://www.shqp.gov.cn/shqp/qwld/20241010/1212868.html",
    },
    # 4. 张得志 — 区委常委、统战部部长
    {
        "id": 1004,
        "name": "张得志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年4月",
        "birthplace": "",
        "education": "研究生、经济学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区委常委、区委统战部部长，区政协党组副书记，区社会主义学院院长",
        "current_org": "中共上海市青浦区委统战部",
        "source": "https://www.shqp.gov.cn/shqp/qwld/20230529/1119632.html",
    },
    # 5. 苗光辉 — 区委常委、人武部政委
    {
        "id": 1005,
        "name": "苗光辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年3月",
        "birthplace": "",
        "education": "大学，经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区委常委、人武部政治委员、党委书记",
        "current_org": "上海市青浦区人民武装部",
        "source": "https://www.shqp.gov.cn/shqp/qwld/20190820/504119.html",
    },
    # 6. 顾骏 — 区委常委、政法委书记
    {
        "id": 1006,
        "name": "顾骏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年10月",
        "birthplace": "",
        "education": "大学，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区委常委、区委政法委书记",
        "current_org": "中共上海市青浦区委政法委员会",
        "source": "https://www.shqp.gov.cn/shqp/qwld/20211020/894719.html",
    },
    # 7. 陈建国 — 区委常委、宣传部部长
    {
        "id": 1007,
        "name": "陈建国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年3月",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区委常委、区委宣传部部长",
        "current_org": "中共上海市青浦区委宣传部",
        "source": "https://www.shqp.gov.cn/shqp/qwld/20211020/894720.html",
    },
    # 8. 李方明 — 区委常委、组织部部长
    {
        "id": 1008,
        "name": "李方明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年7月",
        "birthplace": "",
        "education": "大学，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区委常委、区委组织部部长",
        "current_org": "中共上海市青浦区委组织部",
        "source": "https://www.shqp.gov.cn/shqp/qwld/20211020/894721.html",
    },
    # 9. 叶靖 — 区委常委、副区长
    {
        "id": 1009,
        "name": "叶靖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "",
        "education": "大学，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区委常委、区人民政府副区长、党组成员",
        "current_org": "上海市青浦区人民政府",
        "source": "https://www.shqp.gov.cn/shqp/qwld/20260226/1352513.html",
    },
    # 10. 沈雪峰 — 区委常委、纪委书记
    {
        "id": 1010,
        "name": "沈雪峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年1月",
        "birthplace": "",
        "education": "大学，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区委常委、区纪委书记，区监察委副主任、代理主任",
        "current_org": "中共上海市青浦区纪律检查委员会",
        "source": "https://www.shqp.gov.cn/shqp/qwld/20260413/1368936.html",
    },
    # 11. 李峰 — 区委常委、副区长
    {
        "id": 1011,
        "name": "李峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年6月",
        "birthplace": "",
        "education": "大学，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区委常委、区人民政府副区长、党组成员",
        "current_org": "上海市青浦区人民政府",
        "source": "https://www.shqp.gov.cn/shqp/qwld/20250516/1280688.html",
    },
    # 12. 田锋 — 区委常委、人武部部长
    {
        "id": 1012,
        "name": "田锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年4月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区委常委，区人民武装部大校部长、部党委副书记",
        "current_org": "上海市青浦区人民武装部",
        "source": "https://www.shqp.gov.cn/shqp/qwld/20260413/1368937.html",
    },

    # ═══════════════════════════════════════════════════════════════════════
    # 区政府领导班子（非常委副区长）
    # ═══════════════════════════════════════════════════════════════════════
    # 13. 倪向军 — 副区长
    {
        "id": 2001,
        "name": "倪向军",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1967年6月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "青浦区人民政府副区长，区行政学院院长",
        "current_org": "上海市青浦区人民政府",
        "source": "https://www.shqp.gov.cn/shqp/ldzc/index.html",
    },
    # 14. 张彦 — 副区长
    {
        "id": 2002,
        "name": "张彦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年6月",
        "birthplace": "",
        "education": "研究生，工学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区人民政府副区长、党组成员",
        "current_org": "上海市青浦区人民政府",
        "source": "https://www.shqp.gov.cn/shqp/ldzc/index.html",
    },
    # 15. 朱众伟 — 副区长
    {
        "id": 2003,
        "name": "朱众伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "",
        "education": "大学，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区人民政府副区长、党组成员",
        "current_org": "上海市青浦区人民政府",
        "source": "https://www.shqp.gov.cn/shqp/ldzc/index.html",
    },
    # 16. 陈锡琦 — 副区长
    {
        "id": 2004,
        "name": "陈锡琦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年8月",
        "birthplace": "",
        "education": "研究生，理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区人民政府副区长、党组成员",
        "current_org": "上海市青浦区人民政府",
        "source": "https://www.shqp.gov.cn/shqp/ldzc/index.html",
    },

    # ═══════════════════════════════════════════════════════════════════════
    # 区人大领导班子
    # ═══════════════════════════════════════════════════════════════════════
    # 17. 程巍 — 人大常委会主任
    {
        "id": 3001,
        "name": "程巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年3月",
        "birthplace": "",
        "education": "在职研究生，管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区人大常委会主任、党组书记",
        "current_org": "上海市青浦区人大常委会",
        "source": "https://www.shqp.gov.cn/shqp/qrdld/20260227/1352621.html",
    },
    # 18. 陶夏芳 — 人大副主任
    {
        "id": 3002,
        "name": "陶夏芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1964年2月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "青浦区人大常委会副主任、一级巡视员",
        "current_org": "上海市青浦区人大常委会",
        "source": "https://www.shqp.gov.cn/shqp/qrdld/20180622/148421.html",
    },
    # 19. 吴瑞弟 — 人大副主任
    {
        "id": 3003,
        "name": "吴瑞弟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年1月",
        "birthplace": "",
        "education": "大学，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区人大常委会副主任、党组成员",
        "current_org": "上海市青浦区人大常委会",
        "source": "https://www.shqp.gov.cn/shqp/qrdld/20211027/894860.html",
    },
    # 20. 高健 — 人大副主任
    {
        "id": 3004,
        "name": "高健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年3月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区人大常委会副主任、党组成员，区总工会主席",
        "current_org": "上海市青浦区人大常委会",
        "source": "https://www.shqp.gov.cn/shqp/qrdld/index.html",
    },
    # 21. 王海青 — 人大副主任
    {
        "id": 3005,
        "name": "王海青",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1965年1月",
        "birthplace": "",
        "education": "大学，文学学士",
        "party_join": "民盟",
        "work_start": "",
        "current_post": "青浦区人大常委会副主任（不驻会）、民盟青浦区主委、区科协一级调研员",
        "current_org": "上海市青浦区人大常委会",
        "source": "https://www.shqp.gov.cn/shqp/qrdld/index.html",
    },

    # ═══════════════════════════════════════════════════════════════════════
    # 区政协领导班子
    # ═══════════════════════════════════════════════════════════════════════
    # 22. 曹卫东 — 政协主席
    {
        "id": 4001,
        "name": "曹卫东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年10月",
        "birthplace": "",
        "education": "大学，法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区政协主席、党组书记",
        "current_org": "政协上海市青浦区委员会",
        "source": "https://www.shqp.gov.cn/shqp/qzld/index.html",
    },
    # 23. 徐孝芳 — 政协副主席
    {
        "id": 4002,
        "name": "徐孝芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1968年12月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区政协副主席、党组成员",
        "current_org": "政协上海市青浦区委员会",
        "source": "https://www.shqp.gov.cn/shqp/qzld/index.html",
    },
    # 24. 饶斐文 — 政协副主席
    {
        "id": 4003,
        "name": "饶斐文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "农工党",
        "work_start": "",
        "current_post": "青浦区政协副主席（不驻会）、农工党青浦区委主委、区卫健委一级调研员",
        "current_org": "政协上海市青浦区委员会",
        "source": "https://www.shqp.gov.cn/shqp/qzld/index.html",
    },
    # 25. 顾桂芳 — 政协副主席
    {
        "id": 4004,
        "name": "顾桂芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1968年9月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "民进",
        "work_start": "",
        "current_post": "青浦区政协副主席（不驻会）、区体育局局长、民进青浦区总支主委",
        "current_org": "政协上海市青浦区委员会",
        "source": "https://www.shqp.gov.cn/shqp/qzld/index.html",
    },
    # 26. 高峰 — 政协副主席
    {
        "id": 4005,
        "name": "高峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年10月",
        "birthplace": "",
        "education": "大学，理学学士",
        "party_join": "民建",
        "work_start": "",
        "current_post": "青浦区政协副主席（不驻会）、区残疾人联合会理事长、民建青浦区委主委",
        "current_org": "政协上海市青浦区委员会",
        "source": "https://www.shqp.gov.cn/shqp/qzld/index.html",
    },

    # ═══════════════════════════════════════════════════════════════════════
    # 区法院、检察院
    # ═══════════════════════════════════════════════════════════════════════
    # 27. 方正杰 — 法院院长
    {
        "id": 5001,
        "name": "方正杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年4月",
        "birthplace": "",
        "education": "大学，法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区人民法院院长、党组书记、二级高级法官",
        "current_org": "上海市青浦区人民法院",
        "source": "https://www.shqp.gov.cn/shqp/ldzc/index.html",
    },
    # 28. 秦明华 — 检察院检察长
    {
        "id": 5002,
        "name": "秦明华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年7月",
        "birthplace": "",
        "education": "大学，法律硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青浦区人民检察院检察长、党组书记、二级高级检察官",
        "current_org": "上海市青浦区人民检察院",
        "source": "https://www.shqp.gov.cn/shqp/ldzc/index.html",
    },

    # ═══════════════════════════════════════════════════════════════════════
    # 前任领导
    # ═══════════════════════════════════════════════════════════════════════
    # 29. 徐建 — 前任区委书记
    {
        "id": 6001,
        "name": "徐建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "综合媒体报道",
    },
    # 30. 杨小菁 — 前任区长
    {
        "id": 6002,
        "name": "杨小菁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "综合媒体报道",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共上海市青浦区委员会", "type": "党委", "level": "市辖区"},
    {"id": 2, "name": "上海市青浦区人民政府", "type": "政府", "level": "市辖区"},
    {"id": 3, "name": "上海市青浦区人大常委会", "type": "人大", "level": "市辖区"},
    {"id": 4, "name": "政协上海市青浦区委员会", "type": "政协", "level": "市辖区"},
    {"id": 5, "name": "上海市青浦区人民法院", "type": "其他", "level": "市辖区"},
    {"id": 6, "name": "上海市青浦区人民检察院", "type": "其他", "level": "市辖区"},
    {"id": 7, "name": "中共上海市青浦区委统战部", "type": "党委", "level": "市辖区"},
    {"id": 8, "name": "上海市青浦区人民武装部", "type": "其他", "level": "市辖区"},
    {"id": 9, "name": "中共上海市青浦区委政法委员会", "type": "党委", "level": "市辖区"},
    {"id": 10, "name": "中共上海市青浦区委宣传部", "type": "党委", "level": "市辖区"},
    {"id": 11, "name": "中共上海市青浦区委组织部", "type": "党委", "level": "市辖区"},
    {"id": 12, "name": "中共上海市青浦区纪律检查委员会", "type": "党委", "level": "市辖区"},
    {"id": 13, "name": "上海市青浦区总工会", "type": "群团", "level": "市辖区"},
    {"id": 14, "name": "上海市青浦区科学技术协会", "type": "群团", "level": "市辖区"},
    {"id": 15, "name": "上海市青浦区卫生健康委员会", "type": "政府", "level": "市辖区"},
    {"id": 16, "name": "上海市青浦区体育局", "type": "政府", "level": "市辖区"},
    {"id": 17, "name": "上海市青浦区残疾人联合会", "type": "群团", "level": "市辖区"},
    {"id": 18, "name": "中共上海市青浦区委党校", "type": "事业单位", "level": "市辖区"},
    {"id": 19, "name": "上海市青浦区社会主义学院", "type": "事业单位", "level": "市辖区"},
    # 前任关联组织
    {"id": 20, "name": "中共上海市杨浦区委员会", "type": "党委", "level": "市辖区"},
    {"id": 21, "name": "上海市教育委员会", "type": "政府", "level": "省级"},
    {"id": 22, "name": "上海市人大常委会", "type": "人大", "level": "省级"},
    {"id": 23, "name": "上海市人民政府办公厅", "type": "政府", "level": "省级"},
    {"id": 24, "name": "绍兴市越城区人民政府", "type": "政府", "level": "县处级"},
    {"id": 25, "name": "中共绍兴市越城区委员会", "type": "党委", "level": "县处级"},
    {"id": 26, "name": "绍兴滨海新区管理委员会", "type": "政府", "level": "县处级"},
    {"id": 27, "name": "中共浙江省委办公厅", "type": "党委", "level": "省级"},
    {"id": 28, "name": "浙江省委全面深化改革委员会办公室", "type": "党委", "level": "省级"},
    {"id": 29, "name": "中共上海市虹口区委员会", "type": "党委", "level": "市辖区"},
    {"id": 30, "name": "上海市嘉定区人民政府", "type": "政府", "level": "市辖区"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 王平 — 区委书记
    {"person_id": 1001, "org_id": 1, "title": "青浦区委书记", "start": "2025-05", "end": "present", "rank": "正局级", "note": "区委全面工作"},
    {"person_id": 1001, "org_id": 23, "title": "上海市政府副秘书长、市政府办公厅主任", "start": "", "end": "2025-05", "rank": "正局级", "note": ""},
    {"person_id": 1001, "org_id": 21, "title": "上海市教卫工作党委副书记、市教委主任", "start": "", "end": "", "rank": "正局级", "note": ""},
    {"person_id": 1001, "org_id": 22, "title": "上海市人大常委会副秘书长、办公厅主任", "start": "", "end": "", "rank": "正局级", "note": ""},
    {"person_id": 1001, "org_id": 21, "title": "上海市教委副主任", "start": "", "end": "", "rank": "副局级", "note": ""},
    {"person_id": 1001, "org_id": 20, "title": "杨浦区委办公室主任", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 1001, "org_id": 20, "title": "杨浦区教育局局长、党委书记", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 1001, "org_id": 20, "title": "杨浦区委宣传部副部长（正处级）", "start": "", "end": "", "rank": "正处级", "note": ""},

    # 金晓明 — 区长
    {"person_id": 1002, "org_id": 2, "title": "青浦区委副书记、区长", "start": "2024-10", "end": "present", "rank": "正局级", "note": "区政府全面工作"},
    {"person_id": 1002, "org_id": 2, "title": "青浦区人民政府代理区长", "start": "2024", "end": "2024-10", "rank": "正局级", "note": ""},
    {"person_id": 1002, "org_id": 28, "title": "浙江省委全面深化改革委员会办公室常务副主任（正厅级）", "start": "", "end": "", "rank": "正厅级", "note": ""},
    {"person_id": 1002, "org_id": 27, "title": "浙江省委办公厅副主任", "start": "", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 1002, "org_id": 26, "title": "绍兴滨海新区党工委副书记、管委会主任", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 1002, "org_id": 25, "title": "绍兴市越城区委书记", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 1002, "org_id": 2, "title": "绍兴市越城区区长", "start": "", "end": "", "rank": "正处级", "note": "跨省：从浙江至上海"},
    {"person_id": 1002, "org_id": 24, "title": "绍兴市越城区委副书记", "start": "", "end": "", "rank": "副处级", "note": ""},

    # 刘琪 — 区委副书记
    {"person_id": 1003, "org_id": 1, "title": "青浦区委副书记、区委党校校长", "start": "", "end": "present", "rank": "正局级", "note": ""},

    # 张得志 — 统战部长
    {"person_id": 1004, "org_id": 7, "title": "青浦区委常委、统战部部长，区政协党组副书记", "start": "", "end": "present", "rank": "副局级", "note": ""},

    # 苗光辉 — 人武部政委
    {"person_id": 1005, "org_id": 8, "title": "青浦区委常委、人武部政治委员", "start": "", "end": "present", "rank": "副局级", "note": ""},

    # 顾骏 — 政法委书记
    {"person_id": 1006, "org_id": 9, "title": "青浦区委常委、政法委书记", "start": "", "end": "present", "rank": "副局级", "note": ""},

    # 陈建国 — 宣传部长
    {"person_id": 1007, "org_id": 10, "title": "青浦区委常委、宣传部部长", "start": "", "end": "present", "rank": "副局级", "note": ""},

    # 李方明 — 组织部长
    {"person_id": 1008, "org_id": 11, "title": "青浦区委常委、组织部部长", "start": "", "end": "present", "rank": "副局级", "note": ""},

    # 叶靖 — 常委副区长
    {"person_id": 1009, "org_id": 2, "title": "青浦区委常委、副区长", "start": "", "end": "present", "rank": "副局级", "note": ""},
    {"person_id": 1009, "org_id": 12, "title": "青浦区纪委书记、区监委主任", "start": "", "end": "2026-02", "rank": "副局级", "note": "转任副区长"},
    {"person_id": 1009, "org_id": 20, "title": "杨浦区教育工作党委书记", "start": "", "end": "", "rank": "正处级", "note": ""},

    # 沈雪峰 — 纪委书记
    {"person_id": 1010, "org_id": 12, "title": "青浦区委常委、区纪委书记", "start": "2026-04", "end": "present", "rank": "副局级", "note": "区监察委副主任、代理主任"},

    # 李峰 — 常委副区长
    {"person_id": 1011, "org_id": 2, "title": "青浦区委常委、副区长", "start": "", "end": "present", "rank": "副局级", "note": ""},
    {"person_id": 1011, "org_id": 30, "title": "嘉定区副区长", "start": "", "end": "", "rank": "副局级", "note": ""},
    {"person_id": 1011, "org_id": 30, "title": "嘉定区委办公室主任", "start": "", "end": "", "rank": "正处级", "note": ""},

    # 田锋 — 人武部长
    {"person_id": 1012, "org_id": 8, "title": "青浦区委常委、人武部大校部长", "start": "2026-04", "end": "present", "rank": "副局级", "note": ""},

    # 倪向军 — 副区长
    {"person_id": 2001, "org_id": 2, "title": "青浦区副区长、区行政学院院长", "start": "", "end": "present", "rank": "副局级", "note": "无党派"},

    # 张彦 — 副区长
    {"person_id": 2002, "org_id": 2, "title": "青浦区副区长", "start": "", "end": "present", "rank": "副局级", "note": ""},

    # 朱众伟 — 副区长
    {"person_id": 2003, "org_id": 2, "title": "青浦区副区长", "start": "", "end": "present", "rank": "副局级", "note": ""},

    # 陈锡琦 — 副区长
    {"person_id": 2004, "org_id": 2, "title": "青浦区副区长", "start": "", "end": "present", "rank": "副局级", "note": ""},

    # 程巍 — 人大主任
    {"person_id": 3001, "org_id": 3, "title": "青浦区人大常委会主任", "start": "2026-02", "end": "present", "rank": "正局级", "note": ""},

    # 陶夏芳 — 人大副主任
    {"person_id": 3002, "org_id": 3, "title": "青浦区人大常委会副主任", "start": "", "end": "present", "rank": "副局级", "note": "一级巡视员"},

    # 吴瑞弟 — 人大副主任
    {"person_id": 3003, "org_id": 3, "title": "青浦区人大常委会副主任", "start": "", "end": "present", "rank": "副局级", "note": ""},

    # 高健 — 人大副主任
    {"person_id": 3004, "org_id": 3, "title": "青浦区人大常委会副主任、区总工会主席", "start": "", "end": "present", "rank": "副局级", "note": ""},

    # 王海青 — 人大副主任
    {"person_id": 3005, "org_id": 3, "title": "青浦区人大常委会副主任（不驻会）", "start": "", "end": "present", "rank": "副局级", "note": "民盟"},

    # 曹卫东 — 政协主席
    {"person_id": 4001, "org_id": 4, "title": "青浦区政协主席", "start": "", "end": "present", "rank": "正局级", "note": ""},

    # 徐孝芳 — 政协副主席
    {"person_id": 4002, "org_id": 4, "title": "青浦区政协副主席", "start": "", "end": "present", "rank": "副局级", "note": ""},

    # 饶斐文 — 政协副主席
    {"person_id": 4003, "org_id": 4, "title": "青浦区政协副主席（不驻会）", "start": "", "end": "present", "rank": "副局级", "note": "农工党"},

    # 顾桂芳 — 政协副主席
    {"person_id": 4004, "org_id": 4, "title": "青浦区政协副主席（不驻会）", "start": "", "end": "present", "rank": "副局级", "note": "民进"},

    # 高峰 — 政协副主席
    {"person_id": 4005, "org_id": 4, "title": "青浦区政协副主席（不驻会）", "start": "", "end": "present", "rank": "副局级", "note": "民建"},

    # 方正杰 — 法院院长
    {"person_id": 5001, "org_id": 5, "title": "青浦区人民法院院长", "start": "", "end": "present", "rank": "副局级", "note": "二级高级法官"},

    # 秦明华 — 检察院检察长
    {"person_id": 5002, "org_id": 6, "title": "青浦区人民检察院检察长", "start": "", "end": "present", "rank": "副局级", "note": "二级高级检察官"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 班子成员关系 — 同一届区委常委会
    {"person_a": 1001, "person_b": 1002, "type": "overlap", "strength": "strong",
     "context": "区委书记与区长搭档，2025年5月起共事", "overlap_org": "中共上海市青浦区委员会", "overlap_period": "2025-至今"},
    {"person_a": 1001, "person_b": 1003, "type": "overlap", "strength": "strong",
     "context": "区委书记与区委副书记在同一常委会", "overlap_org": "中共上海市青浦区委员会", "overlap_period": "至今"},
    {"person_a": 1002, "person_b": 1003, "type": "overlap", "strength": "strong",
     "context": "区长与区委副书记在同一常委会", "overlap_org": "中共上海市青浦区委员会", "overlap_period": "至今"},
    {"person_a": 1001, "person_b": 1009, "type": "overlap", "strength": "strong",
     "context": "区委书记与常委副区长在区委常委会共事", "overlap_org": "中共上海市青浦区委员会", "overlap_period": "至今"},
    {"person_a": 1001, "person_b": 1011, "type": "overlap", "strength": "strong",
     "context": "区委书记与常委副区长在区委常委会共事", "overlap_org": "中共上海市青浦区委员会", "overlap_period": "至今"},

    # 王平与叶靖 — 杨浦区同源
    {"person_a": 1001, "person_b": 1009, "type": "same_system", "strength": "medium",
     "context": "王平曾任杨浦区委办公室主任、教育局局长等职；叶靖曾任杨浦区教育工作党委书记、平凉路街道党工委书记。二人在杨浦区可能有工作交集", "overlap_org": "中共上海市杨浦区委员会", "overlap_period": ""},

    # 李峰 — 嘉定区调任
    {"person_a": 1011, "person_b": 1001, "type": "same_system", "strength": "medium",
     "context": "李峰从嘉定区调任青浦，为跨区交流干部", "overlap_org": "", "overlap_period": ""},

    # 前任关系
    {"person_a": 6001, "person_b": 1001, "type": "predecessor_successor", "strength": "strong",
     "context": "徐建为前任青浦区委书记，王平于2025年5月接任", "overlap_org": "中共上海市青浦区委员会", "overlap_period": "2025"},
    {"person_a": 6002, "person_b": 1002, "type": "predecessor_successor", "strength": "strong",
     "context": "杨小菁为前任青浦区长，金晓明于2024年10月接任", "overlap_org": "上海市青浦区人民政府", "overlap_period": "2024"},

    # 金晓明跨省交流
    {"person_a": 1002, "person_b": 1001, "type": "promotion_chain", "strength": "medium",
     "context": "金晓明从浙江省委（正厅级）跨省交流至上海青浦任区长，为跨省干部交流案例", "overlap_org": "", "overlap_period": ""},
]

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"=== 青浦区领导班子工作关系网络 ===")
    print(f"调查日期: {TODAY}")
    print(f"人员: {len(persons)}")
    print(f"机构: {len(organizations)}")
    print(f"任职: {len(positions)}")
    print(f"关系: {len(relationships)}")
    print()

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\n数据库: {DB_PATH}")
    print(f"图谱:   {GEXF_PATH}")

    # Copy to canonical locations if running from staging
    import shutil
    if STAGING != HERE.parents[2]:
        for src, dst in [
            (DB_PATH, CANONICAL_DB),
            (GEXF_PATH, CANONICAL_GEXF),
            (HERE / f"build_{SLUG}_data.py", CANONICAL_BUILD),
            (HERE / f"build_{SLUG}_data.py", CANONICAL_ROOT_BUILD),
        ]:
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                print(f"已复制: {src} -> {dst}")
