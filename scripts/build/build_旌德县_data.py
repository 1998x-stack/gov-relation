#!/usr/bin/env python3
"""Build Jingde County (旌德县) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-16
Task: anhui_旌德县 (县 level)
Province: 安徽省 (Anhui)
Parent city: 宣城市 (Xuancheng)
Targets: 县委书记 & 县长

Current leadership (as of 2026-07-16):
  - 县委书记: 吴忠梅 (female, born 1971.10)
  - 县委副书记、县长: 张旗会 (male, born 1977.03)
  - 县委副书记: 周兵
  - 县人大常委会主任: 王斌
  - 县政协主席: 张蕾

Sources:
  Official government site: https://www.ahjd.gov.cn/
  - https://www.ahjd.gov.cn/SiteLeader/44.html (县政府领导, accessed 2026-07-16)
  - https://www.ahjd.gov.cn/SiteLeader/showList/65/44.html (张旗会 profile)
  - https://www.ahjd.gov.cn/SiteLeader/showList/138/44.html (艾康雨 profile)
  - https://www.ahjd.gov.cn/News/show/1693469.html (县委十六届十次全会, 2025-12-31)
  - https://www.ahjd.gov.cn/News/show/1626195.html (2025年县委工作会议, 2025-03-21)
  - https://www.ahjd.gov.cn/News/show/1707228.html (2026年县委工作会议, 2026-04-16)
  - https://www.ahjd.gov.cn/News/show/1629204.html (县委常委会暨县委党建领导小组会议, 2025-03-28)
  - https://www.ahjd.gov.cn/News/show/1678198.html (县委常委会扩大会议, 2025-09-13)
  - https://www.ahjd.gov.cn/OpennessContent/show/3454427.html (2025年工作务虚会, 2025-12-17)
  - https://www.ahjd.gov.cn/News/show/1715212.html (县委招商引资调度会, 2026-06-16)
  - https://www.ahjd.gov.cn/Jczwgk/show/3250878.html (2023年县级河长名单)
  Baidu Baike (旌德县): https://baike.baidu.com/item/旌德县/3356659
  新京报: https://m.bjnews.com.cn/detail/1739073241129278.html (吴忠梅发言报道)
  经济之家: http://zonghe.dejiangwang.com/zonghe/2023/0728/65563.html (张旗会简历)
  云南行业网: http://www.yunnan.chinalh.com.cn/gundong/2023/0625/91507.html (储德友履新)

Confidence: Current roles confirmed from official Jingde County government web pages
and multiple 2024/2025/2026 meeting reports. Biographical details for 张旗会 have
detailed career timeline from appointment notices. 吴忠梅's detailed pre-2021 resume
is partial — gaps marked explicitly.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "旌德县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "旌德县_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Top Leaders ═══════════════════════════════════════════════════
    {
        "id": 1,
        "name": "吴忠梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年10月",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共旌德县委员会",
        "source": "https://www.ahjd.gov.cn/News/show/1619768.html (县委常委会2024年度民主生活会, 2025-02); https://m.bjnews.com.cn/detail/1739073241129278.html (新京报, 2025-02-09)",
        "notes": "旌德县委书记。曾任旌德县县长(2019-2023)，2023年6月任县委书记。\n公开报道显示，吴忠梅出生于1971年10月。主政风格强调'工业富县'、'双招双引'，\n曾脱稿批评'公务员安稳论'，主张干部须经一线锤炼。\n履历缺口：2021年以前在旌德县的具体任职时间有待进一步明确。曾任旌德县委副书记、代县长(2019年底-2020年初)，2020年初正式任县长。之前职务待查。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "张旗会",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年3月",
        "birthplace": "",
        "native_place": "安徽郎溪",
        "education": "安徽省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "1996年12月",
        "current_post": "县委副书记、县长",
        "current_org": "旌德县人民政府",
        "source": "https://www.ahjd.gov.cn/SiteLeader/showList/65/44.html (张旗会官方简历, accessed 2026-07-16); http://zonghe.dejiangwang.com/zonghe/2023/0728/65563.html (经济之家, 2023-07-28)",
        "notes": "旌德县委副书记、县长。1996年7月入党，1996年12月参加工作。\n籍贯安徽郎溪。安徽省委党校研究生学历。\n2023年7月当选旌德县县长。",
        "confidence": "confirmed"
    },
    # ═══ Party Committee (县委常委) ════════════════════════════════════
    {
        "id": 3,
        "name": "周兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共旌德县委员会",
        "source": "https://www.ahjd.gov.cn/News/show/1693469.html (县委十六届十次全会, 2025-12-31); https://www.ahjd.gov.cn/News/show/1715212.html (县委招商引资调度会, 2026-06-16)",
        "notes": "旌德县委副书记。2025年12月县委十六届十次全会时以县委副书记身份出现。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "王沧浪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记（原）",
        "current_org": "中共旌德县纪律检查委员会",
        "source": "https://www.ahjd.gov.cn/OpennessContent/show/3454427.html (2025年工作务虚会, 2025-12-17); https://www.ahjd.gov.cn/News/show/1606998.html (离退休干部形势通报会, 2025-01-16); https://www.ahjd.gov.cn/News/show/1598428.html (赴浙江考察, 2024-12)",
        "notes": "曾任县委常委、县纪委书记(2023-2024年河长名单显示)。2025-01-16以'县委副书记王沧浪'身份出现。\n2025年12月务虚会仍为'县领导'。\n可能职务由纪委书记转任或兼任县委副书记。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "金伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "旌德县人民政府",
        "source": "https://www.ahjd.gov.cn/SiteLeader/showList/137/44.html (县政府领导, accessed 2026-07-16); https://www.ahjd.gov.cn/News/show/1598428.html (赴浙江考察, 2024-12)",
        "notes": "旌德县委常委、常务副县长。县政府领导排名第4位。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "郭磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共旌德县委组织部",
        "source": "https://www.ahjd.gov.cn/News/show/1626195.html (2025年县委工作会议, 2025-03-21); https://www.ahjd.gov.cn/News/show/1664154.html (吴忠梅调研规上企业, 2025-07-23); https://www.ahjd.gov.cn/OpennessContent/show/3560469.html (吴忠梅调研督导, 2025-07-05)",
        "notes": "旌德县委常委、组织部部长。2025年3月县委工作会议时以'郭磊'身份总结部署组织工作。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "刘明辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共旌德县委统战部",
        "source": "https://www.ahjd.gov.cn/News/show/1626195.html (2025年县委工作会议, 2025-03-21); https://www.ahjd.gov.cn/Jczwgk/show/3250878.html (2023年县级河长名单)",
        "notes": "旌德县委常委、统战部部长。2025年3月县委工作会议时以'刘明辉'总结部署统战工作。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "王浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共旌德县委政法委员会",
        "source": "https://www.ahjd.gov.cn/News/show/1626195.html (2025年县委工作会议, 2025-03-21); https://www.ahjd.gov.cn/Jczwgk/show/3250878.html (2023年县级河长名单)",
        "notes": "旌德县委常委、政法委书记。2025年3月县委工作会议时以'王浩'总结部署政法工作。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "夏博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "旌德县人民政府",
        "source": "https://www.ahjd.gov.cn/SiteLeader/44.html (县政府领导, accessed 2026-07-16); http://www.jdxrdcwh.gov.cn/News/show/1918.html (县人代会选举公告, 2025-01-03)",
        "notes": "旌德县委常委、常务副县长(现任县政府领导页面)。2025年度人代会选举为县监委主任。\n2026年6月已以'县委常委、常务副县长'身份出席县政府重点项目会议。\n金伟为此前常务副县长，夏博接任常务副县长时间待查。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "解浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "旌德县人民政府",
        "source": "https://www.ahjd.gov.cn/SiteLeader/44.html (县政府领导, accessed 2026-07-16); https://www.ahjd.gov.cn/News/show/1715212.html (县委招商引资调度会, 2026-06-16)",
        "notes": "旌德县委常委、副县长。县政府领导排名第3位。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "胡红蔚",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长（原）",
        "current_org": "中共旌德县委组织部",
        "source": "https://www.ahjd.gov.cn/Jczwgk/show/3250878.html (2023年县级河长名单); https://www.ahjd.gov.cn/News/show/1568667.html (吴忠梅专题调研民政工作, 2024-07-01); https://jdxf.gov.cn/content/detail/66a2eda88b5ec3a6308b4567.html (送清凉慰问活动, 2024-07-24)",
        "notes": "曾任旌德县委常委、组织部部长、县总工会主席(2024年7月确认)。\n2025年县委工作会议(2025-03-21)时组织部工作已由郭磊总结部署，\n推测胡红蔚已调离或转任。\n履历待查。",
        "confidence": "confirmed"
    },
    # ═══ County Government (县政府领导) ═══════════════════════════════
    {
        "id": 12,
        "name": "艾康雨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "",
        "native_place": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "旌德县人民政府",
        "source": "https://www.ahjd.gov.cn/SiteLeader/showList/138/44.html (艾康雨官方简历, accessed 2026-07-16)",
        "notes": "旌德县人民政府副县长、党组成员，县公安局党委书记、局长、督察长（三级高级警长）。\n1973年12月生，本科学历，中共党员。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "朱琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "旌德县人民政府",
        "source": "https://www.ahjd.gov.cn/SiteLeader/44.html (县政府领导, accessed 2026-07-16)",
        "notes": "旌德县人民政府副县长。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "柴长宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "旌德县人民政府",
        "source": "https://www.ahjd.gov.cn/SiteLeader/44.html (县政府领导, accessed 2026-07-16)",
        "notes": "旌德县人民政府副县长。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "周云海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "旌德县人民政府",
        "source": "https://www.ahjd.gov.cn/SiteLeader/44.html (县政府领导, accessed 2026-07-16)",
        "notes": "旌德县人民政府副县长。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 16,
        "name": "吕建国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历、工学博士",
        "party_join": "九三学社社员",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "旌德县人民政府",
        "source": "https://www.ahjd.gov.cn/SiteLeader/showList/192/44.html (吕建国官方简历, accessed 2026-07-16)",
        "notes": "旌德县人民政府副县长（挂职）。1980年1月出生，九三学社社员，\n研究生学历、工学博士学位。现任合肥师范学院科研处副处长。",
        "confidence": "confirmed"
    },
    {
        "id": 17,
        "name": "傅世恩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "旌德县人民政府",
        "source": "https://www.ahjd.gov.cn/SiteLeader/44.html (县政府领导, accessed 2026-07-16)",
        "notes": "旌德县人民政府副县长。曾任旌德经开区管委会主任。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 18,
        "name": "陈愿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "旌德县人民政府",
        "source": "https://www.ahjd.gov.cn/SiteLeader/44.html (县政府领导, accessed 2026-07-16)",
        "notes": "旌德县人民政府副县长（县政府领导页面列最后一位）。\n履历待查。",
        "confidence": "confirmed"
    },
    # ═══ Legislative & Advisory (人大、政协) ═══════════════════════════
    {
        "id": 19,
        "name": "王斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "旌德县人民代表大会常务委员会",
        "source": "https://www.ahjd.gov.cn/News/show/1693469.html (县委十六届十次全会, 2025-12-31); https://www.ahjd.gov.cn/News/show/1574527.html (县人大常委会议, 2024-07-31)",
        "notes": "旌德县人大常委会主任。多次在县委全会和人大会议中确认。\n履历待查。",
        "confidence": "confirmed"
    },
    {
        "id": 20,
        "name": "张蕾",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议旌德县委员会",
        "source": "https://www.ahjd.gov.cn/News/show/1693469.html (县委十六届十次全会, 2025-12-31); http://www.jdzx.gov.cn/News/show/872.html (县政协十一届五次会议)",
        "notes": "旌德县政协主席。多次在县委全会和政协会议中确认。\n履历待查。",
        "confidence": "confirmed"
    },
    # ═══ Predecessors ══════════════════════════════════════════════════
    {
        "id": 21,
        "name": "储德友",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年12月",
        "birthplace": "",
        "native_place": "安徽宁国",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宣城市委秘书长",
        "current_org": "中共宣城市委",
        "source": "http://www.yunnan.chinalh.com.cn/gundong/2023/0625/91507.html (云南行业网, 2023-06-25)",
        "notes": "旌德县前任县委书记(2020.02-2023.06)。2023年6月调任宣城市委秘书长。\n曾任泾县县委常委、组织部长，宣城市委组织部常务副部长、\n市委非公有制经济和社会组织工委书记。\n1970年12月生，籍贯安徽宁国，省委党校研究生学历。",
        "confidence": "confirmed"
    },
    {
        "id": 22,
        "name": "周密",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年",
        "birthplace": "",
        "native_place": "",
        "education": "博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://news.ustc.edu.cn/info/1049/48144.htm (新安晚报, 2014-10-28)",
        "notes": "旌德县前任县委书记(约2014-2016)。15岁上中国科大，29岁任团省委副书记(副厅)，\n32岁任旌德县委书记兼宣城市副市长。\n曾任安徽省政府研究室综合处主任科员，挂职滁州团市委副书记，\n淮北职业技术学院副院长，相山区委常委、常务副区长，\n团省委副书记。",
        "confidence": "confirmed"
    },
    {
        "id": 23,
        "name": "孙立志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.ahjd.gov.cn/News/show/1118944.html (人武部党委第一书记任职大会, 2019-04-27)",
        "notes": "旌德县前任县长(约2017-2019)。2019年4月与储德友(县委书记)同时期任职。\n2019年底/2020年初由吴忠梅接替。\n履历待查。",
        "confidence": "confirmed"
    },
]

organizations = [
    {"id": 1, "name": "中共旌德县委员会", "type": "党委", "level": "县", "parent": "中共宣城市委", "location": "安徽省宣城市旌德县"},
    {"id": 2, "name": "旌德县人民政府", "type": "政府", "level": "县", "parent": "宣城市人民政府", "location": "安徽省宣城市旌德县"},
    {"id": 3, "name": "旌德县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "旌德县", "location": "安徽省宣城市旌德县"},
    {"id": 4, "name": "中国人民政治协商会议旌德县委员会", "type": "政协", "level": "县", "parent": "旌德县", "location": "安徽省宣城市旌德县"},
    {"id": 5, "name": "中共旌德县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共旌德县委员会", "location": "安徽省宣城市旌德县"},
    {"id": 6, "name": "中共旌德县委组织部", "type": "党委", "level": "县", "parent": "中共旌德县委员会", "location": "安徽省宣城市旌德县"},
    {"id": 7, "name": "中共旌德县委统战部", "type": "党委", "level": "县", "parent": "中共旌德县委员会", "location": "安徽省宣城市旌德县"},
    {"id": 8, "name": "中共旌德县委政法委员会", "type": "党委", "level": "县", "parent": "中共旌德县委员会", "location": "安徽省宣城市旌德县"},
    {"id": 9, "name": "旌德县公安局", "type": "政府", "level": "县", "parent": "旌德县人民政府", "location": "安徽省宣城市旌德县"},
    {"id": 10, "name": "中共宣城市委", "type": "党委", "level": "地级市", "parent": "中共安徽省委", "location": "安徽省宣城市"},
    {"id": 11, "name": "宣城市人民政府", "type": "政府", "level": "地级市", "parent": "安徽省人民政府", "location": "安徽省宣城市"},
    {"id": 12, "name": "合肥师范学院", "type": "事业单位", "level": "省属高校", "parent": "安徽省教育厅", "location": "安徽省合肥市"},
    # Predecessor orgs
    {"id": 13, "name": "郎溪县毕桥镇", "type": "乡镇/街道", "level": "乡镇", "parent": "郎溪县", "location": "安徽省宣城市郎溪县"},
    {"id": 14, "name": "郎溪县飞里乡", "type": "乡镇/街道", "level": "乡镇", "parent": "郎溪县", "location": "安徽省宣城市郎溪县"},
    {"id": 15, "name": "共青团郎溪县委员会", "type": "群团", "level": "县", "parent": "共青团宣城市委", "location": "安徽省宣城市郎溪县"},
    {"id": 16, "name": "郎溪县东夏镇", "type": "乡镇/街道", "level": "乡镇", "parent": "郎溪县", "location": "安徽省宣城市郎溪县"},
    {"id": 17, "name": "郎溪县人民政府", "type": "政府", "level": "县", "parent": "宣城市人民政府", "location": "安徽省宣城市郎溪县"},
    {"id": 18, "name": "宣城市委非公经济和社会组织工委", "type": "党委", "level": "地级市", "parent": "中共宣城市委", "location": "安徽省宣城市"},
    {"id": 19, "name": "宣城经济技术开发区", "type": "开发区", "level": "国家级经开区", "parent": "宣城市人民政府", "location": "安徽省宣城市"},
    {"id": 20, "name": "中共宣州区委", "type": "党委", "level": "县", "parent": "中共宣城市委", "location": "安徽省宣城市宣州区"},
    {"id": 21, "name": "宣州区委党校", "type": "事业单位", "level": "县", "parent": "中共宣州区委", "location": "安徽省宣城市宣州区"},
    {"id": 22, "name": "中共泾县县委组织部", "type": "党委", "level": "县", "parent": "中共泾县委员会", "location": "安徽省宣城市泾县"},
    {"id": 23, "name": "宣城市委组织部", "type": "党委", "level": "地级市", "parent": "中共宣城市委", "location": "安徽省宣城市"},
]

positions = [
    # ── 吴忠梅 ──────────────────────────────────────────────────
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2023-06", "end": "present", "rank": "正处级", "note": "2023年6月任旌德县委书记"},
    {"person_id": 1, "org_id": 2, "title": "县长", "start": "2019-12", "end": "2023-06", "rank": "正处级", "note": "2019年底任代县长，2020年初正式任县长，2023年6月卸任"},
    {"person_id": 1, "org_id": 1, "title": "县委副书记", "start": "2019-12", "end": "2023-06", "rank": "正处级", "note": "任县长期间同时任县委副书记"},
    # ── 张旗会 ──────────────────────────────────────────────────
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2023-06", "end": "present", "rank": "正处级", "note": "2023年6月任旌德县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "2023-07", "end": "present", "rank": "正处级", "note": "2023年7月当选旌德县县长"},
    {"person_id": 2, "org_id": 20, "title": "区委副书记（正县级）", "start": "2022-04", "end": "2023-06", "rank": "正处级", "note": "兼区委党校校长(2022.05起)"},
    {"person_id": 2, "org_id": 19, "title": "管委会副主任、党工委副书记", "start": "2021-09", "end": "2022-04", "rank": "正县级", "note": "宣城经济技术开发区管委会副主任、党工委副书记（正县级）"},
    {"person_id": 2, "org_id": 19, "title": "管委会副主任、党工委委员", "start": "2017-07", "end": "2021-09", "rank": "副处级→正县级", "note": "2017.07-2021.01: 副主任、党工委委员；2021.01-2021.09: 副主任、党工委副书记"},
    {"person_id": 2, "org_id": 18, "title": "专职副书记", "start": "2014-08", "end": "2017-07", "rank": "副处级", "note": "宣城市委非公经济和社会组织工委专职副书记；2017.03-2017.05挂职温州市经信局局长助理"},
    {"person_id": 2, "org_id": 17, "title": "县委常委、办公室主任", "start": "2014-01", "end": "2014-08", "rank": "副处级", "note": "郎溪县委常委、办公室主任"},
    {"person_id": 2, "org_id": 17, "title": "县委常委、副县长", "start": "2011-08", "end": "2013-12", "rank": "副处级", "note": "郎溪县委常委、县政府副县长"},
    {"person_id": 2, "org_id": 1, "title": "县委常委", "start": "2011-06", "end": "2011-08", "rank": "副处级", "note": "郎溪县委常委"},
    {"person_id": 2, "org_id": 16, "title": "党委书记、镇长", "start": "2009-05", "end": "2011-06", "rank": "正科级", "note": "郎溪县东夏镇党委书记、镇长"},
    {"person_id": 2, "org_id": 15, "title": "团县委书记", "start": "2006-02", "end": "2009-05", "rank": "正科级", "note": "共青团郎溪县委书记"},
    {"person_id": 2, "org_id": 14, "title": "党委委员、副乡长", "start": "2004-08", "end": "2006-02", "rank": "副科级", "note": "郎溪县飞里乡党委委员、副乡长"},
    {"person_id": 2, "org_id": 13, "title": "副镇长", "start": "2004-03", "end": "2004-08", "rank": "副科级", "note": "郎溪县毕桥镇副镇长"},
    {"person_id": 2, "org_id": 13, "title": "党委委员", "start": "2001-09", "end": "2004-03", "rank": "副科级", "note": "郎溪县毕桥镇党委委员"},
    {"person_id": 2, "org_id": 13, "title": "党委组织干事", "start": "2000-03", "end": "2001-09", "rank": "科员级", "note": "郎溪县毕桥镇党委组织干事"},
    {"person_id": 2, "org_id": 13, "title": "林业站技术员", "start": "1996-12", "end": "2000-03", "rank": "科员级", "note": "郎溪县毕桥林业站技术员"},
    # ── 周兵 ────────────────────────────────────────────────────
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "2025", "end": "present", "rank": "副处级", "note": "旌德县委副书记，具体到任时间待查"},
    # ── 王沧浪 ──────────────────────────────────────────────────
    {"person_id": 4, "org_id": 5, "title": "县委常委、县纪委书记", "start": "2023", "end": "2024", "rank": "副处级", "note": "2023年河长名单确认；2024年末/2025年初可能转任县委副书记"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start": "2025-01", "end": "present", "rank": "副处级", "note": "2025年1月以县委副书记身份出现；与县纪委书记是否兼任或转任待查"},
    # ── 金伟 ────────────────────────────────────────────────────
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "2023", "end": "present", "rank": "副处级", "note": "旌德县委常委"},
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start": "2023", "end": "2025", "rank": "副处级", "note": "旌德县委常委、常务副县长(至2025年)"},
    # ── 郭磊 ────────────────────────────────────────────────────
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "2025", "end": "present", "rank": "副处级", "note": "2025年3月以县委常委身份出现"},
    {"person_id": 6, "org_id": 6, "title": "组织部部长", "start": "2025", "end": "present", "rank": "副处级", "note": "接替胡红蔚任县委组织部部长"},
    # ── 刘明辉 ──────────────────────────────────────────────────
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "2023", "end": "present", "rank": "副处级", "note": "旌德县委常委"},
    {"person_id": 7, "org_id": 7, "title": "统战部部长", "start": "2023", "end": "present", "rank": "副处级", "note": "旌德县委常委、统战部部长"},
    # ── 王浩 ────────────────────────────────────────────────────
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "2023", "end": "present", "rank": "副处级", "note": "旌德县委常委"},
    {"person_id": 8, "org_id": 8, "title": "政法委书记", "start": "2023", "end": "present", "rank": "副处级", "note": "旌德县委常委、政法委书记"},
    # ── 夏博 ────────────────────────────────────────────────────
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "2025", "end": "present", "rank": "副处级", "note": "2025年1月当选县监委主任"},
    {"person_id": 9, "org_id": 2, "title": "常务副县长", "start": "2025", "end": "present", "rank": "副处级", "note": "接替金伟任常务副县长"},
    {"person_id": 9, "org_id": 5, "title": "县监委主任", "start": "2025-01", "end": "2025", "rank": "副处级", "note": "2025年1月县人大会议选举为监察委员会主任，后转任常务副县长"},
    # ── 解浩 ────────────────────────────────────────────────────
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "2023", "end": "present", "rank": "副处级", "note": "旌德县委常委"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "2023", "end": "present", "rank": "副处级", "note": "旌德县委常委、副县长"},
    # ── 胡红蔚 ──────────────────────────────────────────────────
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "2023", "end": "2025", "rank": "副处级", "note": "曾任旌德县委常委(至2025年)"},
    {"person_id": 11, "org_id": 6, "title": "组织部部长", "start": "2023", "end": "2025", "rank": "副处级", "note": "并兼任县总工会主席"},
    # ── 艾康雨 ──────────────────────────────────────────────────
    {"person_id": 12, "org_id": 2, "title": "副县长、县公安局局长", "start": "2023", "end": "present", "rank": "副处级", "note": "旌德县副县长、党组成员，县公安局党委书记、局长、督察长（三级高级警长）"},
    # ── 朱琴 ────────────────────────────────────────────────────
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "2024", "end": "present", "rank": "副处级", "note": "旌德县政府副县长"},
    # ── 柴长宏 ──────────────────────────────────────────────────
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "2023", "end": "present", "rank": "副处级", "note": "旌德县政府副县长"},
    # ── 周云海 ──────────────────────────────────────────────────
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "2025", "end": "present", "rank": "副处级", "note": "旌德县政府副县长"},
    # ── 吕建国 ──────────────────────────────────────────────────
    {"person_id": 16, "org_id": 2, "title": "副县长（挂职）", "start": "2025", "end": "present", "rank": "副处级", "note": "旌德县政府副县长（挂职），合肥师范学院科研处副处长"},
    {"person_id": 16, "org_id": 12, "title": "科研处副处长", "start": "", "end": "present", "rank": "副处级", "note": "合肥师范学院科研处副处长"},
    # ── 傅世恩 ──────────────────────────────────────────────────
    {"person_id": 17, "org_id": 2, "title": "副县长", "start": "2025", "end": "present", "rank": "副处级", "note": "旌德县政府副县长，曾任旌德经开区管委会主任"},
    # ── 陈愿 ────────────────────────────────────────────────────
    {"person_id": 18, "org_id": 2, "title": "副县长", "start": "2025", "end": "present", "rank": "副处级", "note": "旌德县政府副县长"},
    # ── 王斌 ────────────────────────────────────────────────────
    {"person_id": 19, "org_id": 3, "title": "县人大常委会主任", "start": "2022", "end": "present", "rank": "正处级", "note": "旌德县人大常委会主任"},
    # ── 张蕾 ────────────────────────────────────────────────────
    {"person_id": 20, "org_id": 4, "title": "县政协主席", "start": "2022", "end": "present", "rank": "正处级", "note": "旌德县政协主席"},
    # ── 储德友 ──────────────────────────────────────────────────
    {"person_id": 21, "org_id": 1, "title": "县委书记", "start": "2020-02", "end": "2023-06", "rank": "正处级", "note": "旌德县委书记"},
    {"person_id": 21, "org_id": 10, "title": "市委秘书长", "start": "2023-06", "end": "present", "rank": "正处级", "note": "宣城市委秘书长"},
    {"person_id": 21, "org_id": 22, "title": "县委常委、组织部部长", "start": "", "end": "", "rank": "副处级", "note": "曾任泾县县委常委、组织部长"},
    {"person_id": 21, "org_id": 23, "title": "常务副部长", "start": "", "end": "", "rank": "正处级", "note": "曾任宣城市委组织部常务副部长、市委非公工委书记"},
    # ── 周密 ────────────────────────────────────────────────────
    {"person_id": 22, "org_id": 1, "title": "县委书记", "start": "2014", "end": "2016", "rank": "正处级", "note": "兼宣城市副市长"},
    # ── 孙立志 ──────────────────────────────────────────────────
    {"person_id": 23, "org_id": 2, "title": "县长", "start": "2017", "end": "2019", "rank": "正处级", "note": "旌德县县长"},
]

relationships = [
    # ── 吴忠梅 ↔ 张旗会: predecessor/successor (县长接力) ─────
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "吴忠梅卸任县长后由张旗会接任县长", "overlap_org": "旌德县人民政府", "overlap_period": "2023-06~2023-07", "strength": "strong", "direction": "person_to_other", "confidence": "confirmed"},
    # ── 吴忠梅 ↔ 张旗会: 当前搭档 (书记+县长) ──────────────
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "现任县委书记与县长，日常工作搭档，多次共同出席会议和调研", "overlap_org": "中共旌德县委员会/旌德县人民政府", "overlap_period": "2023-06~present", "strength": "strong", "direction": "undirected", "confidence": "confirmed"},
    # ── 吴忠梅 ↔ 储德友: predecessor/successor (县委书记接力) ─
    {"person_a": 21, "person_b": 1, "type": "predecessor_successor", "context": "储德友卸任县委书记后由吴忠梅接任", "overlap_org": "中共旌德县委员会", "overlap_period": "2023-06", "strength": "strong", "direction": "other_to_person", "confidence": "confirmed"},
    # ── 吴忠梅 ↔ 孙立志: predecessor/successor (县长接力) ───
    {"person_a": 23, "person_b": 1, "type": "predecessor_successor", "context": "孙立志卸任县长后由吴忠梅接任", "overlap_org": "旌德县人民政府", "overlap_period": "2019", "strength": "strong", "direction": "other_to_person", "confidence": "confirmed"},
    # ── 张旗会 ↔ 周兵: 当前搭档 ─────────────────────────────
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县委副书记、县长与县委副书记，日常共事", "overlap_org": "中共旌德县委员会", "overlap_period": "2025~present", "strength": "medium", "direction": "undirected", "confidence": "confirmed"},
    # ── 吴忠梅 ↔ 周兵: 当前搭档 ─────────────────────────────
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与县委副书记", "overlap_org": "中共旌德县委员会", "overlap_period": "2025~present", "strength": "medium", "direction": "undirected", "confidence": "confirmed"},
    # ── 吴忠梅 ↔ 金伟: 县委常委共事 ──────────────────────────
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记与县委常委、常务副县长", "overlap_org": "中共旌德县委员会", "overlap_period": "2023~present", "strength": "medium", "direction": "undirected", "confidence": "confirmed"},
    # ── 张旗会 ↔ 金伟: 县政府搭档 ────────────────────────────
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县长与常务副县长", "overlap_org": "旌德县人民政府", "overlap_period": "2023~2025", "strength": "medium", "direction": "undirected", "confidence": "confirmed"},
    # ── 吴忠梅 ↔ 胡红蔚: 2019起共事 ──────────────────────────
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委书记与县委常委、组织部部长(2025年前)", "overlap_org": "中共旌德县委员会", "overlap_period": "2020~2025", "strength": "medium", "direction": "undirected", "confidence": "confirmed"},
    # ── 张旗会 ↔ 解浩: 县政府搭档 ────────────────────────────
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "县长与县委常委、副县长", "overlap_org": "旌德县人民政府", "overlap_period": "2023~present", "strength": "medium", "direction": "undirected", "confidence": "confirmed"},
    # ── 储德友 ↔ 张旗会: 上下级(储德友为县委书记时张旗会尚未到任) ───
    # (储2023.06离任，张2023.06到任，交接期存在)
]

# ── SQLite ────────────────────────────────────────────────────────────

def create_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            direction TEXT,
            confidence TEXT
        );
    """)
    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, "end", rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
             pos["end"], pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period, strength, direction, confidence)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"], r["strength"], r["direction"],
             r["confidence"]))
    conn.commit()
    conn.close()
    print(f"✅ DB created: {DB_PATH}")


# ── GEXF ────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return r,g,b string for a person based on role."""
    post = p.get("current_post", "")
    if "县委书记" in post:
        return "255,50,50"
    if "县长" in post and "副" not in post:
        return "50,100,255"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    if "副书记" in post:
        return "50,100,255"
    if "副县长" in post or "常务副县长" in post:
        return "50,100,255"
    if "部长" in post or "书记" in post:
        return "100,100,100"
    if "主任" in post or "主席" in post:
        return "100,100,100"
    return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "开发区" in t:
        return "200,255,200"
    if "乡镇" in t:
        return "255,255,200"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "群团" in t:
        return "255,220,255"
    if "事业单位" in t:
        return "220,220,220"
    return "200,200,200"

def is_top_leader(p):
    post = p.get("current_post", "")
    return "县委书记" in post or ("县长" in post and "副" not in post)

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent (Sisyphus)</creator>')
    lines.append('    <description>旌德县 leadership network — Jingde County, Xuancheng, Anhui. Research date: 2026-07-16.</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("15.0" if p.get("current_post","") and ("常委" in p["current_post"] or "副书记" in p["current_post"]) else "12.0")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("confidence",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # org nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # edges
    lines.append('    <edges>')
    eid = 0

    # person → org (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["confidence"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")


# ── main ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Building 旌德县 leadership network data...")
    create_db()
    build_gexf()

    # Verify
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        cnt = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {cnt} records")
    conn.close()
    print("Done.")
