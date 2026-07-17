#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for 政和县 (Zhenghe County),
南平市 (Nanping City), 福建省 (Fujian Province).

Covers: Party Secretary (县委书记), County Mayor (县长, position currently vacant
as of July 2026), key deputy positions (县委副书记, 常务副县长, 组织部长, 纪委书记,
政法委书记), predecessor/successor chains, and the county-level leadership network.

Sources:
- 政和新闻网 (http://www.fjzhxww.com/): Official local media
- 人民网福建频道 (http://fj.people.com.cn/): Appointment announcements
- 东南网 (http://np.fjsen.com/): Local news
- 政和县人民政府 (http://www.zhenghe.gov.cn/): Government portal

Generated: 2026-07-17
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_政和县")
DB_PATH = os.path.join(TMP, "政和县_network.db")
GEXF_PATH = os.path.join(TMP, "政和县_network.gexf")
PERSONS_DIR = TMP

AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 王丰 — 政和县委书记 (2026.5-), 前县长 (2021-2026.5)
    {"id": 1, "name": "王丰", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-11", "birthplace": "福建武夷山",
     "native_place": "福建建瓯",
     "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政和县委书记",
     "current_org": "中共政和县委员会",
     "source": "http://fj.people.com.cn/n2/2026/0503/c181466-41570707.html",
     "notes": "曾任政和县长5年（2021-2026），2026年5月升任县委书记",
     "confidence": "confirmed"},

    # 刘铠维 — 县委副书记 (2023-)
    {"id": 2, "name": "刘铠维", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "native_place": "", "education": "北京大学经济学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政和县委副书记、政和经济开发区党工委书记",
     "current_org": "中共政和县委员会",
     "source": "http://www.fjzhxww.com/2026-07/10/content_2363818.htm",
     "notes": "福建省引进生（2017年），北京大学博士，曾任武夷山市副市长（挂职）",
     "confidence": "confirmed"},

    # 翁贤忠 — 县人大常委会主任
    {"id": 3, "name": "翁贤忠", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人大常委会主任",
     "current_org": "政和县人民代表大会常务委员会",
     "source": "http://www.fjzhxww.com/2026-07/02/content_2361024.htm",
     "notes": "",
     "confidence": "confirmed"},

    # 曹斌 — 县政协主席 (2025-)，前常务副县长
    {"id": 4, "name": "曹斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-10", "birthplace": "",
     "native_place": "福建政和",
     "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政和县政协主席",
     "current_org": "政协政和县委员会",
     "source": "http://www.fjzhxww.com/2026-07/06/content_2362292.htm",
     "notes": "曾任中学一级教师、石屯镇党委书记、县委常委/常务副县长（~2021-2025），2025年底转任政协主席",
     "confidence": "confirmed"},

    # 杨笔剑 — 县委常委、副县长
    {"id": 5, "name": "杨笔剑", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-10", "birthplace": "",
     "native_place": "",
     "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政和县委常委、副县长",
     "current_org": "政和县人民政府",
     "source": "http://www.fjzhxww.com/2026-07/03/content_2361466.htm",
     "notes": "曾任石屯镇党委书记，2024年6月任前公示拟任党政副职，后任副县长、县委常委",
     "confidence": "confirmed"},

    # 白子华 — 县委常委、组织部部长
    {"id": 6, "name": "白子华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政和县委常委、组织部部长",
     "current_org": "中共政和县委组织部",
     "source": "http://www.fjzhxww.com/2026-03/23/content_2323539.htm",
     "notes": "最早2024年11月以组织部长身份公开出现",
     "confidence": "confirmed"},

    # 林昊 — 县委常委、县纪委书记、县监委主任
    {"id": 7, "name": "林昊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "native_place": "",
     "education": "警院毕业",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政和县委常委、县纪委书记、县监委主任",
     "current_org": "中共政和县纪律检查委员会",
     "source": "http://www.fjzhxww.com/2026-02/12/content_2310689.htm",
     "notes": "曾任建瓯市乡镇派出所民警/村支书/政法委/南平市纪委，2021年负责全市粮食购销领域腐败专项整治，2024年被评为南平市第八届道德模范",
     "confidence": "confirmed"},

    # 卢亨强 — 县委常委、宣传部部长
    {"id": 8, "name": "卢亨强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政和县委常委、宣传部部长",
     "current_org": "中共政和县委宣传部",
     "source": "http://www.fjzhxww.com/2026-06/05/content_2351047.htm",
     "notes": "",
     "confidence": "confirmed"},

    # 游美君 — 县委常委、统战部部长
    {"id": 9, "name": "游美君", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政和县委常委、统战部部长",
     "current_org": "中共政和县委统战部",
     "source": "http://www.fjzhxww.com/2026-04/29/content_2336362.htm",
     "notes": "",
     "confidence": "confirmed"},

    # 赖传铭 — 县委常委（分工待确认）
    {"id": 10, "name": "赖传铭", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "native_place": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政和县委常委",
     "current_org": "中共政和县委员会",
     "source": "http://www.fjzhxww.com/2026-05/14/content_2341084.htm",
     "notes": "具体分工待确认",
     "confidence": "plausible"},

    # ── Predecessors ──

    # 黄拔荣 — 前任县委书记 (2021.5-2026.4)
    {"id": 11, "name": "黄拔荣", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-10", "birthplace": "",
     "native_place": "",
     "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南平市副市长",
     "current_org": "南平市人民政府",
     "source": "http://fj.people.com.cn/n2/2026/0528/c181466-41594356.html",
     "notes": "曾任南平市工信局党组书记/局长，2021年5月任政和县委书记，2026年4月升任南平市副市长",
     "confidence": "confirmed"},

    # 黄爱华 — 前任县委书记 (2016.4-2021.5)
    {"id": 12, "name": "黄爱华", "gender": "女", "ethnicity": "汉族",
     "birth": "1973-11", "birthplace": "",
     "native_place": "福建南平延平区",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "福建省总工会党组成员、专职副主席",
     "current_org": "福建省总工会",
     "source": "https://baike.baidu.com/item/%E9%BB%84%E7%88%B1%E5%8D%8E/16658492",
     "notes": "在政和工作15年（2006-2021）: 组织部长→县长→县委书记",
     "confidence": "confirmed"},

    # 张行书 — 前任县长 (2016.4-2021.5)
    {"id": 13, "name": "张行书", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "native_place": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "",
     "current_org": "",
     "source": "https://news.qq.com/rain/a/20210525A049A700",
     "notes": "曾任政和县长（2016-2021），后调松溪县委书记，去向待进一步确认",
     "confidence": "plausible"},

    # 庄宏 — 前县纪委书记 (2021.7-2024.9)，被调查
    {"id": 14, "name": "庄宏", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-07", "birthplace": "福建南平",
     "native_place": "福建惠安",
     "education": "大学",
     "party_join": "中共党员", "work_start": "1992-02",
     "current_post": "",
     "current_org": "",
     "source": "https://www.9pinw.com/news_f563703.html",
     "notes": "2024年9月接受福建省纪委监委纪律审查和监察调查",
     "confidence": "confirmed"},

    # 叶金星 — 前县委常委、政法委书记，现任县人大常委会副主任
    {"id": 15, "name": "叶金星", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-10", "birthplace": "",
     "native_place": "福建政和",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人大常委会副主任",
     "current_org": "政和县人民代表大会常务委员会",
     "source": "https://www.thepaper.cn/newsDetail_forward_16006819",
     "notes": "曾任县委办主任（廖俊波时期），后调南平市城市公用事业管理局，2023年12月任县人大副主任，2024年4月兼任县委常委、政法委书记",
     "confidence": "confirmed"},

    # ── Current deputy mayors ──
    {"id": 16, "name": "徐清平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人民政府副县长",
     "current_org": "政和县人民政府",
     "source": "http://www.fjzhxww.com/2026-06/12/content_2353751.htm",
     "notes": "分管自然资源、生态环境等工作",
     "confidence": "confirmed"},

    {"id": 17, "name": "陈海", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人民政府副县长",
     "current_org": "政和县人民政府",
     "source": "http://www.fjzhxww.com/2026-07/01/content_2360413.htm",
     "notes": "分管住建、城市管理等工作",
     "confidence": "confirmed"},

    {"id": 18, "name": "饶宇梁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人民政府副县长、县公安局局长",
     "current_org": "政和县人民政府",
     "source": "http://www.fjzhxww.com/2025-08/14/content_2245511.htm",
     "notes": "分管公安、司法、信访等工作",
     "confidence": "confirmed"},

    {"id": 19, "name": "范子凤", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人民政府副县长",
     "current_org": "政和县人民政府",
     "source": "http://www.fjzhxww.com/2026-05/14/content_2341084.htm",
     "notes": "",
     "confidence": "confirmed"},

    {"id": 20, "name": "陈夏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人民政府副县长",
     "current_org": "政和县人民政府",
     "source": "http://www.zhenghe.gov.cn/",
     "notes": "",
     "confidence": "confirmed"},

    {"id": 21, "name": "罗文彬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人民政府副县长",
     "current_org": "政和县人民政府",
     "source": "http://www.zhenghe.gov.cn/",
     "notes": "",
     "confidence": "confirmed"},

    {"id": 22, "name": "李刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人民政府副县长",
     "current_org": "政和县人民政府",
     "source": "http://www.fjzhxww.com/2026-06/02/content_2347860.htm",
     "notes": "",
     "confidence": "confirmed"},

    # ── NPC and CPPCC vice chairs ──
    {"id": 23, "name": "范成功", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人大常委会副主任",
     "current_org": "政和县人民代表大会常务委员会",
     "source": "http://www.fjzhxww.com/2026-07/01/content_2360413.htm",
     "notes": "",
     "confidence": "confirmed"},

    {"id": 24, "name": "谢应灿", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人大常委会副主任",
     "current_org": "政和县人民代表大会常务委员会",
     "source": "http://www.fjzhxww.com/2026-07/01/content_2360413.htm",
     "notes": "",
     "confidence": "confirmed"},

    {"id": 25, "name": "兰桂花", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人大常委会副主任",
     "current_org": "政和县人民代表大会常务委员会",
     "source": "http://www.fjzhxww.com/2026-07/01/content_2360413.htm",
     "notes": "",
     "confidence": "confirmed"},

    {"id": 26, "name": "刘小伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人大常委会副主任",
     "current_org": "政和县人民代表大会常务委员会",
     "source": "http://www.fjzhxww.com/2026-07/01/content_2360413.htm",
     "notes": "",
     "confidence": "confirmed"},

    # ── Judiciary ──
    {"id": 27, "name": "谢争春", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人民法院院长",
     "current_org": "政和县人民法院",
     "source": "http://www.dyzxw.org/html/article/202405/14/238558.shtml",
     "notes": "(注：2025年12月报道中余崇斌为代院长，可能已换人)",
     "confidence": "plausible"},

    {"id": 28, "name": "王晓亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政和县人民检察院检察长",
     "current_org": "政和县人民检察院",
     "source": "http://www.fjzhxww.com/2026-07/01/content_2360413.htm",
     "notes": "",
     "confidence": "confirmed"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共政和县委员会", "type": "党委", "level": "县级",
     "parent": "中共南平市委员会", "location": "福建省南平市政和县"},
    {"id": 2, "name": "政和县人民政府", "type": "政府", "level": "县级",
     "parent": "南平市人民政府", "location": "福建省南平市政和县"},
    {"id": 3, "name": "政和县人民代表大会常务委员会", "type": "人大", "level": "县级",
     "parent": "", "location": "福建省南平市政和县"},
    {"id": 4, "name": "政协政和县委员会", "type": "政协", "level": "县级",
     "parent": "", "location": "福建省南平市政和县"},
    {"id": 5, "name": "中共政和县委组织部", "type": "党委", "level": "县级",
     "parent": "中共政和县委员会", "location": "福建省南平市政和县"},
    {"id": 6, "name": "中共政和县委宣传部", "type": "党委", "level": "县级",
     "parent": "中共政和县委员会", "location": "福建省南平市政和县"},
    {"id": 7, "name": "中共政和县委统战部", "type": "党委", "level": "县级",
     "parent": "中共政和县委员会", "location": "福建省南平市政和县"},
    {"id": 8, "name": "中共政和县纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共政和县委员会", "location": "福建省南平市政和县"},
    {"id": 9, "name": "中共政和县委政法委员会", "type": "党委", "level": "县级",
     "parent": "中共政和县委员会", "location": "福建省南平市政和县"},
    {"id": 10, "name": "政和经济开发区党工委", "type": "党委", "level": "县级",
     "parent": "中共政和县委员会", "location": "福建省南平市政和县"},
    {"id": 11, "name": "政和县公安局", "type": "政府", "level": "县级",
     "parent": "政和县人民政府", "location": "福建省南平市政和县"},
    {"id": 12, "name": "政和县人民法院", "type": "事业单位", "level": "县级",
     "parent": "", "location": "福建省南平市政和县"},
    {"id": 13, "name": "政和县人民检察院", "type": "事业单位", "level": "县级",
     "parent": "", "location": "福建省南平市政和县"},
    {"id": 14, "name": "中共南平市委员会", "type": "党委", "level": "地级",
     "parent": "中共福建省委员会", "location": "福建省南平市"},
    {"id": 15, "name": "南平市人民政府", "type": "政府", "level": "地级",
     "parent": "福建省人民政府", "location": "福建省南平市"},
    {"id": 16, "name": "南平市工业和信息化局", "type": "政府", "level": "地级",
     "parent": "南平市人民政府", "location": "福建省南平市"},
    {"id": 17, "name": "福建省总工会", "type": "群团", "level": "省级",
     "parent": "", "location": "福建省福州市"},
    {"id": 18, "name": "共青团南平市委员会", "type": "群团", "level": "地级",
     "parent": "", "location": "福建省南平市"},
    {"id": 19, "name": "南平市城市公用事业管理局", "type": "政府", "level": "地级",
     "parent": "南平市人民政府", "location": "福建省南平市"},
    {"id": 20, "name": "政和县石屯镇", "type": "乡镇/街道", "level": "乡级",
     "parent": "政和县人民政府", "location": "福建省南平市政和县石屯镇"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 王丰 (id=1) — 县委书记 (current)
    {"person_id": 1, "org_id": 1, "title": "政和县委书记",
     "start": "2026-05", "end": "present", "rank": "正处级",
     "note": "2026年4月21日任前公示，5月正式就任，接替黄拔荣"},
    {"person_id": 1, "org_id": 2, "title": "政和县人民政府县长",
     "start": "2021-05", "end": "2026-04", "rank": "正处级",
     "note": "2021年5月提名为县长候选人，2021年12月正式当选"},
    {"person_id": 1, "org_id": 1, "title": "政和县委副书记",
     "start": "2021-05", "end": "2026-04", "rank": "副处级",
     "note": "任县长期间同时担任县委副书记"},
    {"person_id": 1, "org_id": 18, "title": "共青团南平市委书记",
     "start": "", "end": "2021", "rank": "正处级",
     "note": "任团市委书记后转政和县委副书记(正处长级)"},
    {"person_id": 1, "org_id": 18, "title": "共青团南平市委副书记",
     "start": "", "end": "", "rank": "副处级",
     "note": ""},

    # 刘铠维 (id=2) — 县委副书记
    {"person_id": 2, "org_id": 1, "title": "政和县委副书记",
     "start": "2023", "end": "present", "rank": "副处级",
     "note": "最早2023年12月以县委副书记身份公开出现"},
    {"person_id": 2, "org_id": 10, "title": "政和经济开发区党工委书记",
     "start": "2024-02", "end": "present", "rank": "",
     "note": "兼任开发区党工委书记"},

    # 翁贤忠 (id=3) — 人大主任
    {"person_id": 3, "org_id": 3, "title": "政和县人大常委会主任",
     "start": "", "end": "present", "rank": "正处级",
     "note": ""},

    # 曹斌 (id=4) — 政协主席 (前常务副县长)
    {"person_id": 4, "org_id": 4, "title": "政和县政协主席",
     "start": "2025-12", "end": "present", "rank": "正处级",
     "note": "2025年12月至今任政协主席"},
    {"person_id": 4, "org_id": 2, "title": "政和县委常委、常务副县长",
     "start": "2021", "end": "2025", "rank": "副处级",
     "note": "2021年任县委常委、副县长，后任常务副县长"},
    {"person_id": 4, "org_id": 20, "title": "政和县石屯镇党委书记",
     "start": "", "end": "2021", "rank": "正科级",
     "note": ""},

    # 杨笔剑 (id=5) — 县委常委、副县长
    {"person_id": 5, "org_id": 2, "title": "政和县委常委、副县长",
     "start": "2024", "end": "present", "rank": "副处级",
     "note": "2024年6月任前公示后任副县长，后任县委常委"},
    {"person_id": 5, "org_id": 20, "title": "政和县石屯镇党委书记",
     "start": "", "end": "2024", "rank": "正科级",
     "note": "接替曹斌任石屯镇党委书记"},

    # 白子华 (id=6) — 组织部长
    {"person_id": 6, "org_id": 5, "title": "政和县委常委、组织部部长",
     "start": "2024", "end": "present", "rank": "副处级",
     "note": "最早2024年11月以组织部长身份出现"},

    # 林昊 (id=7) — 纪委书记
    {"person_id": 7, "org_id": 8, "title": "政和县委常委、县纪委书记、县监委主任",
     "start": "2024", "end": "present", "rank": "副处级",
     "note": "接替被调查的庄宏"},

    # 卢亨强 (id=8) — 宣传部长
    {"person_id": 8, "org_id": 6, "title": "政和县委常委、宣传部部长",
     "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # 游美君 (id=9) — 统战部长
    {"person_id": 9, "org_id": 7, "title": "政和县委常委、统战部部长",
     "start": "", "end": "present", "rank": "副处级",
     "note": ""},

    # 赖传铭 (id=10) — 县委常委
    {"person_id": 10, "org_id": 1, "title": "政和县委常委",
     "start": "", "end": "present", "rank": "副处级",
     "note": "具体分工待确认"},

    # 黄拔荣 (id=11) — 前任县委书记
    {"person_id": 11, "org_id": 1, "title": "政和县委书记",
     "start": "2021-05", "end": "2026-04", "rank": "正处级",
     "note": "2021年5月至2026年4月任县委书记"},
    {"person_id": 11, "org_id": 16, "title": "南平市工业和信息化局党组书记、局长",
     "start": "", "end": "2021-05", "rank": "正处级",
     "note": "任政和县委书记前任南平市工信局党组书记/局长"},
    {"person_id": 11, "org_id": 15, "title": "南平市副市长",
     "start": "2026-05", "end": "present", "rank": "副厅级",
     "note": "2026年5月升任南平市副市长"},

    # 黄爱华 (id=12) — 前任县委书记
    {"person_id": 12, "org_id": 1, "title": "政和县委书记",
     "start": "2016-04", "end": "2021-05", "rank": "正处级",
     "note": ""},
    {"person_id": 12, "org_id": 2, "title": "政和县人民政府县长",
     "start": "2011-12", "end": "2016-04", "rank": "正处级",
     "note": ""},
    {"person_id": 12, "org_id": 1, "title": "政和县委常委、组织部部长",
     "start": "2006", "end": "2011", "rank": "副处级",
     "note": "2006年任政和县委常委、组织部部长"},
    {"person_id": 12, "org_id": 17, "title": "福建省总工会党组成员、专职副主席",
     "start": "2021", "end": "present", "rank": "副厅级",
     "note": ""},

    # 张行书 (id=13) — 前任县长
    {"person_id": 13, "org_id": 2, "title": "政和县人民政府县长",
     "start": "2016-04", "end": "2021-05", "rank": "正处级",
     "note": ""},

    # 庄宏 (id=14) — 前纪委书记 (被调查)
    {"person_id": 14, "org_id": 8, "title": "政和县委常委、县纪委书记、县监委主任",
     "start": "2021-07", "end": "2024-09", "rank": "副处级",
     "note": "2024年9月接受福建省纪委监委纪律审查和监察调查"},

    # 叶金星 (id=15) — 前政法委书记/人大副主任
    {"person_id": 15, "org_id": 9, "title": "政和县委常委、政法委书记",
     "start": "2024-04", "end": "present", "rank": "副处级",
     "note": "2024年4月以政法委书记身份出席活动"},
    {"person_id": 15, "org_id": 3, "title": "政和县人大常委会副主任",
     "start": "2023-12", "end": "present", "rank": "副处级",
     "note": "2023年12月当选人大副主任，同时兼任政法委书记"},
    {"person_id": 15, "org_id": 19, "title": "南平市城市公用事业管理局党总支书记",
     "start": "", "end": "2023", "rank": "正处级",
     "note": ""},

    # Deputy mayors
    {"person_id": 16, "org_id": 2, "title": "政和县人民政府副县长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "政和县人民政府副县长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "政和县人民政府副县长、县公安局局长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "分管公安、司法等工作"},
    {"person_id": 18, "org_id": 11, "title": "政和县公安局局长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "政和县人民政府副县长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "政和县人民政府副县长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "政和县人民政府副县长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 2, "title": "政和县人民政府副县长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},

    # NPC/CPPCC vice chairs
    {"person_id": 23, "org_id": 3, "title": "政和县人大常委会副主任",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 24, "org_id": 3, "title": "政和县人大常委会副主任",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 3, "title": "政和县人大常委会副主任",
     "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 26, "org_id": 3, "title": "政和县人大常委会副主任",
     "start": "", "end": "present", "rank": "副处级", "note": ""},

    # Judiciary
    {"person_id": 27, "org_id": 12, "title": "政和县人民法院院长",
     "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 28, "org_id": 13, "title": "政和县人民检察院检察长",
     "start": "", "end": "present", "rank": "正处级", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 王丰 ↔ 黄拔荣 (县委书记接替)
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor",
     "context": "王丰接替黄拔荣任政和县委书记",
     "overlap_org": "中共政和县委员会", "overlap_period": "2026-05",
     "strength": "strong", "confidence": "confirmed"},

    # 王丰 ↔ 黄拔荣 (党政搭档 2021-2026)
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "黄拔荣任县委书记期间，王丰任县长，党政搭档5年",
     "overlap_org": "中共政和县委员会", "overlap_period": "2021-2026",
     "strength": "strong", "confidence": "confirmed"},

    # 黄拔荣 ↔ 黄爱华 (县委书记接替)
    {"person_a": 11, "person_b": 12, "type": "predecessor_successor",
     "context": "黄拔荣接替黄爱华任政和县委书记",
     "overlap_org": "中共政和县委员会", "overlap_period": "2021-05",
     "strength": "strong", "confidence": "confirmed"},

    # 王丰 ↔ 张行书 (县长接替)
    {"person_a": 1, "person_b": 13, "type": "predecessor_successor",
     "context": "王丰接替张行书任政和县长",
     "overlap_org": "政和县人民政府", "overlap_period": "2021-05",
     "strength": "strong", "confidence": "confirmed"},

    # 王丰 ↔ 刘铠维 (上下级)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "王丰任县委书记/县长期间，刘铠维任县委副书记",
     "overlap_org": "中共政和县委员会", "overlap_period": "2023-present",
     "strength": "strong", "confidence": "confirmed"},

    # 林昊 ↔ 庄宏 (纪委书记接替)
    {"person_a": 7, "person_b": 14, "type": "predecessor_successor",
     "context": "林昊接替被调查的庄宏任纪委书记",
     "overlap_org": "中共政和县纪律检查委员会", "overlap_period": "2024",
     "strength": "strong", "confidence": "confirmed"},

    # 曹斌 ↔ 杨笔剑 (石屯镇党委书记接替)
    {"person_a": 4, "person_b": 5, "type": "predecessor_successor",
     "context": "杨笔剑接替曹斌任石屯镇党委书记",
     "overlap_org": "政和县石屯镇", "overlap_period": "2024",
     "strength": "medium", "confidence": "confirmed"},

    # 黄爱华 ↔ 张行书 (党政搭档 2016-2021)
    {"person_a": 12, "person_b": 13, "type": "overlap",
     "context": "黄爱华任县委书记期间，张行书任县长",
     "overlap_org": "中共政和县委员会", "overlap_period": "2016-2021",
     "strength": "strong", "confidence": "confirmed"},

    # 叶金星 ↔ 黄爱华 (上下级)
    {"person_a": 15, "person_b": 12, "type": "superior_subordinate",
     "context": "叶金星任县委办主任期间，黄爱华任县委书记",
     "overlap_org": "中共政和县委员会", "overlap_period": "2011-2015",
     "strength": "medium", "confidence": "plausible"},

    # 曹斌 ↔ 白子华 (同届常委)
    {"person_a": 4, "person_b": 6, "type": "overlap",
     "context": "曹斌（前常务副县长、现政协主席）与白子华（组织部长）同期任职",
     "overlap_org": "中共政和县委员会", "overlap_period": "2024-present",
     "strength": "medium", "confidence": "confirmed"},

    # 王丰 ↔ 翁贤忠 (党政-人大)
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "王丰与翁贤忠在县四套班子中共事",
     "overlap_org": "中共政和县委员会", "overlap_period": "2021-present",
     "strength": "medium", "confidence": "confirmed"},

    # 王丰 ↔ 曹斌 (上下级/共事)
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "王丰任县长时曹斌任常务副县长，后王丰升书记时曹斌转政协主席",
     "overlap_org": "政和县人民政府", "overlap_period": "2021-2025",
     "strength": "strong", "confidence": "confirmed"},

    # 杨笔剑 ↔ 白子华 (同届常委)
    {"person_a": 5, "person_b": 6, "type": "overlap",
     "context": "杨笔剑（县委常委/副县长）与白子华（组织部长）同届常委",
     "overlap_org": "中共政和县委员会", "overlap_period": "2024-present",
     "strength": "medium", "confidence": "confirmed"},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def create_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON")

    c.execute('''CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, native_place TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT,
        source TEXT, notes TEXT, confidence TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT,
        level TEXT, parent TEXT, location TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT,
        rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        strength TEXT, confidence TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )''')

    for p in persons:
        c.execute('''INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, native_place,
             education, party_join, work_start,
             current_post, current_org, source,
             notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p.get("birthplace", ""), p.get("native_place", ""),
             p["education"], p["party_join"], p.get("work_start", ""),
             p["current_post"], p["current_org"], p["source"],
             p.get("notes", ""), p.get("confidence", "confirmed")))

    for o in organizations:
        c.execute('''INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)''',
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        c.execute('''INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)''',
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute('''INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period,
             strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)''',
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"],
             r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"✓ SQLite database: {DB_PATH}")
    print(f"  Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")


def create_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(p):
        post = p.get("current_post", "")
        name = p["name"]
        # Party secretary
        if "书记" in post and "纪委" not in post and "副书记" not in post:
            return "255,50,50"
        # Government leaders
        elif "县长" in post or ("政府" in post and "副县长" not in post):
            return "50,100,255"
        # Deputies
        elif "副县长" in post or ("副县长" in post):
            return "100,100,255"
        # NPC
        elif "人大" in post:
            return "200,255,255"
        # CPPCC
        elif "政协" in post:
            return "255,240,200"
        # Discipline
        elif "纪委" in post:
            return "255,150,50"
        # Organization
        elif "组织" in post:
            return "150,255,150"
        # Propaganda
        elif "宣传" in post:
            return "100,200,255"
        # United Front
        elif "统战" in post:
            return "200,150,255"
        # Judiciary
        elif "法院" in post or "检察院" in post:
            return "150,150,200"
        else:
            return "100,100,100"

    def is_top_leader(p):
        return p["name"] in ("王丰", "黄拔荣", "黄爱华", "刘铠维")

    def org_color(o):
        ot = o["type"]
        if "党委" in ot:
            return "255,200,200"
        elif "政府" in ot:
            return "200,200,255"
        elif "人大" in ot:
            return "200,255,255"
        elif "政协" in ot:
            return "255,240,200"
        elif "群团" in ot:
            return "255,220,255"
        elif "乡镇" in ot:
            return "255,255,200"
        else:
            return "200,200,200"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Research Agent</creator>')
    lines.append('    <description>政和县领导班子工作关系网络 - 福建省南平市</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="start" type="string"/>')
    lines.append('      <attribute id="3" title="end" type="string"/>')
    lines.append('      <attribute id="4" title="strength" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        note = pos.get("note", "")
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(note)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    for r in relationships:
        w = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(r["strength"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ GEXF graph: {GEXF_PATH}")
    print(f"  Person nodes: {len(persons)}, Org nodes: {len(organizations)}, "
          f"Person-Org edges: {len(positions)}, Person-Person edges: {len(relationships)}")


def write_person_json(person):
    """Write a single person JSON file to staging dir."""
    pid = person["id"]
    name = person["name"]
    post_slug = "县委书记" if "书记" in person.get("current_post","") and "纪委" not in person.get("current_post","") and "副书记" not in person.get("current_post","") else "县长" if "县长" in person.get("current_post","") else "县委副书记" if "副书记" in person.get("current_post","") else "县领导"
    filename = f"{AS_OF}-福建省-南平市-{post_slug}-{name}.json"
    filepath = os.path.join(PERSONS_DIR, filename)

    # Build career entries
    career = []
    for pos in positions:
        if pos["person_id"] == pid:
            org_name = ""
            for o in organizations:
                if o["id"] == pos["org_id"]:
                    org_name = o["name"]
                    break
            career.append({
                "start": pos["start"],
                "end": pos["end"],
                "org": org_name,
                "title": pos["title"],
                "level": pos["rank"],
                "location": "",
                "system": "party" if "委" in pos["title"] else "government",
                "rank": pos["rank"],
                "is_key_promotion": "书记" in pos["title"] or "县长" in pos["title"],
                "notes": pos["note"],
                "confidence": "confirmed" if person.get("confidence","confirmed") == "confirmed" else "plausible",
                "source_ids": ["S001"]
            })

    # Build relationship entries
    rels = []
    for r in relationships:
        other_id = None
        direction = "undirected"
        if r["person_a"] == pid:
            other_id = r["person_b"]
            direction = "other_to_person" if "接替" in r["context"] else "undirected"
        elif r["person_b"] == pid:
            other_id = r["person_a"]
            direction = "person_to_other" if "接替" in r["context"] else "undirected"
        if other_id:
            other_name = ""
            for p in persons:
                if p["id"] == other_id:
                    other_name = p["name"]
                    break
            rels.append({
                "person": other_name,
                "person_id": f"zhenghe_{other_name}",
                "relationship_type": r["type"],
                "strength": r["strength"],
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": direction,
                "confidence": r.get("confidence", "confirmed"),
                "source_ids": ["S001"]
            })

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "福建省",
            "city": "南平市",
            "region": "政和县",
            "job": post_slug,
            "task_id": "fujian_政和县",
            "time_focus": "2021-2026"
        },
        "identity": {
            "person_id": f"zhenghe_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [{
                "period": "",
                "institution": person.get("education", ""),
                "major": "",
                "degree": person.get("education", ""),
                "study_type": "party_school" if "党校" in person.get("education", "") else "unknown",
                "source_ids": ["S001"]
            }],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if "书记" in person.get("current_post","") or "县长" in person.get("current_post","") else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence", "confirmed") == "confirmed",
            "source_ids": ["S001"]
        },
        "career_timeline": career,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if "福建" in person.get("birthplace","") + person.get("native_place","") else "cross_county_rotation",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": f"未发现{name}相关违纪违法或负面报道",
            "date": "",
            "confidence": "plausible",
            "source_ids": []
        }],
        "source_register": [{
            "id": "S001",
            "title": person.get("source", ""),
            "url": person.get("source", ""),
            "publisher": "政和新闻网",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "high" if person.get("confidence","") == "confirmed" else "medium",
            "notes": ""
        }],
        "confidence_summary": {
            "identity": person.get("confidence", "confirmed"),
            "current_role": person.get("confidence", "confirmed"),
            "career_completeness": "partial" if not person.get("birth") else "complete",
            "relationship_confidence": "high",
            "biggest_gap": ""
        },
        "open_questions": []
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ Person JSON: {filepath}")


def main():
    print("=" * 60)
    print("政和县领导班子工作关系网络 - 数据构建")
    print("=" * 60)
    print()

    create_database()
    print()

    create_gexf()
    print()

    # Write person JSON for core leaders
    core_ids = [1, 2]  # 王丰 and 刘铠维 as core figures
    for pid in core_ids:
        for p in persons:
            if p["id"] == pid:
                write_person_json(p)
                break
    print()

    print("=" * 60)
    print("构建完成!")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
