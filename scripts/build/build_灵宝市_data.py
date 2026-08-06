#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 灵宝市 leadership network.

灵宝市 — 河南省三门峡市下辖县级市（1993年5月撤县设市）
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path

# Write outputs next to this script (staging dir during build, scripts/build after promotion)
SCRIPT_DIR = Path(__file__).parent
DB_PATH = os.path.join(str(SCRIPT_DIR), "灵宝市_network.db")
GEXF_PATH = os.path.join(str(SCRIPT_DIR), "灵宝市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── 1. 宋速快 — 市委书记 (current) ──
    {"id": 1, "name": "宋速快", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-03", "birthplace": "河南滑县", "education": "研究生（农学硕士）",
     "party_join": "中共党员", "work_start": "2008-07",
     "current_post": "中共灵宝市委书记", "current_org": "中共灵宝市委员会",
     "source": "https://www.bjnews.com.cn/detail/1760419472129667.html"},
    # ── 2. 刘小旺 — 市长 (current) ──
    {"id": 2, "name": "刘小旺", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市委副书记、市长", "current_org": "灵宝市人民政府",
     "source": "https://www.lingbao.gov.cn/16030/616583808/1263202.html"},
    # ── 3. 张志刚 — 前任市委书记 (2022-2025) ──
    {"id": 3, "name": "张志刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-01", "birthplace": "河南灵宝", "education": "在职研究生",
     "party_join": "1997-11", "work_start": "1998-07",
     "current_post": "三门峡市委常委、副市长", "current_org": "三门峡市人民政府",
     "source": "https://www.smx.gov.cn/4099/2025/10/2142577.html"},
    # ── 4. 孙淑芳 — 更早前市委书记 (2018-2021) ──
    {"id": 4, "name": "孙淑芳", "gender": "女", "ethnicity": "汉族",
     "birth": "1967", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "三门峡市人民政府副市长", "current_org": "三门峡市人民政府",
     "source": "https://baike.baidu.com/item/孙淑芳/17653554"},
    # ── 5. 杜元华 — 市委常委、常务副市长 ──
    {"id": 5, "name": "杜元华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市委常委、常务副市长", "current_org": "灵宝市人民政府",
     "source": "https://www.lingbao.gov.cn/16030/616709088/1522822.html"},
    # ── 6. 杜继英 — 市委常委、宣传部部长、副市长 ──
    {"id": 6, "name": "杜继英", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市委常委、宣传部部长、副市长", "current_org": "灵宝市人民政府",
     "source": "https://www.lingbao.gov.cn/16030/616583808/1263214.html"},
    # ── 7. 田红方 — 市委常委、组织部部长 ──
    {"id": 7, "name": "田红方", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市委常委、组织部部长", "current_org": "中共灵宝市委员会",
     "source": "https://www.lingbao.gov.cn/16018/617037408/1919677.html"},
    # ── 8. 陈少华 — 市委常委、纪委书记、监委主任 ──
    {"id": 8, "name": "陈少华", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市委常委、纪委书记、监委主任", "current_org": "中共灵宝市纪律检查委员会",
     "source": "http://www.smxlz.gov.cn/sitesources/smxlz/page_pc/xsqjw/lbs/xxgk/zzjg/articlec3fda8b08e8c48b2a1c06704e64ade6e.html"},
    # ── 9. 郭仙朋 — 市人大常委会主任 ──
    {"id": 9, "name": "郭仙朋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市人大常委会主任", "current_org": "灵宝市人大常委会",
     "source": "https://www.lingbao.gov.cn/16364/616676256/1508089.html"},
    # ── 10. 师生林 — 市政协主席 ──
    {"id": 10, "name": "师生林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "政协灵宝市委员会主席", "current_org": "政协灵宝市委员会",
     "source": "https://www.lingbao.gov.cn/16018/617037408/1919677.html"},
    # ── 11. 李栓斌 — 市委常委、办公室主任 ──
    {"id": 11, "name": "李栓斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市委常委、市委办公室主任", "current_org": "中共灵宝市委员会",
     "source": "https://www.lingbao.gov.cn/16018/617186016/2059357.html"},
    # ── 12. 段永锋 — 副市长 ──
    {"id": 12, "name": "段永锋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市副市长", "current_org": "灵宝市人民政府",
     "source": "https://www.lingbao.gov.cn/16030/0000/zhengfuxinxi-1.html"},
    # ── 13. 李学斌 — 副市长 ──
    {"id": 13, "name": "李学斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市副市长", "current_org": "灵宝市人民政府",
     "source": "https://www.lingbao.gov.cn/16030/0000/zhengfuxinxi-1.html"},
    # ── 14. 韩保平 — 副市长 ──
    {"id": 14, "name": "韩保平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市副市长", "current_org": "灵宝市人民政府",
     "source": "https://www.lingbao.gov.cn/16030/0000/zhengfuxinxi-1.html"},
    # ── 15. 杨娟 — 副市长 ──
    {"id": 15, "name": "杨娟", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市副市长", "current_org": "灵宝市人民政府",
     "source": "https://www.lingbao.gov.cn/16030/0000/zhengfuxinxi-1.html"},
    # ── 16. 贾学党 — 市委常委 ──
    {"id": 16, "name": "贾学党", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市委常委", "current_org": "中共灵宝市委员会",
     "source": "https://www.lingbao.gov.cn/16018/617037408/1919677.html"},
    # ── 17. 董成梁 — 市委常委 ──
    {"id": 17, "name": "董成梁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市委常委", "current_org": "中共灵宝市委员会",
     "source": "https://www.lingbao.gov.cn/16018/617037408/1919677.html"},
    # ── 18. 李广庆 — 市委常委、统战部部长 ──
    {"id": 18, "name": "李广庆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市委常委、统战部部长", "current_org": "中共灵宝市委员会",
     "source": "https://www.hnzx.gov.cn/2021/03-21/4273106.html"},
    # ── 19. 王泉钧 — 市委常委、统战部部长（后）──
    {"id": 19, "name": "王泉钧", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市委常委、统战部部长", "current_org": "中共灵宝市委员会",
     "source": "https://www.lingbao.gov.cn/16019/616359168/1267401.html"},
    # ── 20. 冯铎 — 市委领导 ──
    {"id": 20, "name": "冯铎", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵宝市领导", "current_org": "中共灵宝市委员会",
     "source": "https://www.lingbao.gov.cn/16018/617037408/1919677.html"},
    # ── 21. 周详 — 渑池县长（曾任灵宝市委副书记、宣传部部长）──
    {"id": 21, "name": "周详", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "渑池县委副书记、县长", "current_org": "渑池县人民政府",
     "source": "https://www.lingbao.gov.cn/16364/616676256/1508089.html"},
]

organizations = [
    {"id": 1, "name": "中共灵宝市委员会", "type": "党委", "level": "县级", "parent": "中共三门峡市委员会", "location": "河南省三门峡市灵宝市"},
    {"id": 2, "name": "灵宝市人民政府", "type": "政府", "level": "县级", "parent": "三门峡市人民政府", "location": "河南省三门峡市灵宝市"},
    {"id": 3, "name": "中共灵宝市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共三门峡市纪律检查委员会", "location": "河南省三门峡市灵宝市"},
    {"id": 4, "name": "灵宝市人大常委会", "type": "人大", "level": "县级", "parent": "三门峡市人大常委会", "location": "河南省三门峡市灵宝市"},
    {"id": 5, "name": "政协灵宝市委员会", "type": "政协", "level": "县级", "parent": "政协三门峡市委员会", "location": "河南省三门峡市灵宝市"},
    {"id": 6, "name": "三门峡市人民政府", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省三门峡市"},
    {"id": 7, "name": "中共三门峡市委员会", "type": "党委", "level": "地级", "parent": "中共河南省委", "location": "河南省三门峡市"},
    {"id": 8, "name": "三门峡市纪委监委", "type": "纪委", "level": "地级", "parent": "中共三门峡市纪律检查委员会", "location": "河南省三门峡市"},
    {"id": 9, "name": "渑池县人民政府", "type": "政府", "level": "县级", "parent": "三门峡市人民政府", "location": "河南省三门峡市渑池县"},
    {"id": 10, "name": "中共渑池县委员会", "type": "党委", "level": "县级", "parent": "中共三门峡市委员会", "location": "河南省三门峡市渑池县"},
    {"id": 11, "name": "河南省荥阳市高村乡", "type": "乡级", "level": "乡科级", "parent": "荥阳市", "location": "河南省郑州市荥阳市"},
    {"id": 12, "name": "三门峡市农业农村局", "type": "政府", "level": "地级", "parent": "三门峡市人民政府", "location": "河南省三门峡市"},
    {"id": 13, "name": "三门峡市农业科学研究院", "type": "事业单位", "level": "地级", "parent": "三门峡市农业农村局", "location": "河南省三门峡市"},
    {"id": 14, "name": "渑池县委员会（县委）", "type": "党委", "level": "县级", "parent": "中共三门峡市委员会", "location": "河南省三门峡市渑池县"},
]

positions = [
    # ── 宋速快 career ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共灵宝市委书记", "start": "2025-10", "end": "现任", "rank": "正县级", "note": "2025年10月13日河南省委决定任灵宝市委书记"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "灵宝市人民政府市长", "start": "2022-04", "end": "2025-10", "rank": "正县级", "note": "2022年3月代市长，4月当选市长，2025年10月辞去市长职务"},
    {"id": 3, "person_id": 1, "org_id": 1, "title": "灵宝市委副书记、统战部部长", "start": "2021-07", "end": "2022-03", "rank": "副县级", "note": "市政协党组副书记、市委党校校长"},
    {"id": 4, "person_id": 1, "org_id": 13, "title": "三门峡市农科院院长、党组书记", "start": "2019-02", "end": "2021-01", "rank": "地级", "note": "市农业农村局党组成员"},
    {"id": 5, "person_id": 1, "org_id": 9, "title": "渑池县副县长", "start": "2017-02", "end": "2019-02", "rank": "副县级", "note": ""},
    {"id": 6, "person_id": 1, "org_id": 12, "title": "三门峡市农业农村局副局长、农机办主任", "start": "2013-08", "end": "2017-02", "rank": "副处级", "note": "曾任荥阳高村乡副乡长、荥阳农委副书记/主任等职"},
    # ── 刘小旺 career ──
    {"id": 7, "person_id": 2, "org_id": 2, "title": "灵宝市委副书记、市长", "start": "2025-11", "end": "现任", "rank": "正县级", "note": "2025年11月代市长，12月19日十五届人大六次会议当选"},
    {"id": 8, "person_id": 2, "org_id": 8, "title": "三门峡市纪委监委委员", "start": "2021", "end": "2025", "rank": "副县级", "note": "曾任三门峡市监察委员会委员（纪检监察系统）"},
    # ── 张志刚 career ──
    {"id": 9, "person_id": 3, "org_id": 1, "title": "中共灵宝市委书记", "start": "2022-03", "end": "2025-10", "rank": "正县级", "note": "2021.02任灵宝市委副书记、市长，2022.03任书记"},
    {"id": 10, "person_id": 3, "org_id": 6, "title": "三门峡市委常委、副市长", "start": "2025-10", "end": "现任", "rank": "副厅级", "note": "负责农业农村、乡村振兴、烟草等"},
    # ── 孙淑芳 career ──
    {"id": 11, "person_id": 4, "org_id": 1, "title": "中共灵宝市委书记", "start": "2018-02", "end": "2021-12", "rank": "正县级", "note": "接替李宏伟，后由张志刚接任"},
    {"id": 12, "person_id": 4, "org_id": 6, "title": "三门峡市人民政府副市长", "start": "2022", "end": "现任", "rank": "副厅级", "note": "由灵宝市委书记升任"},
    # ── 现任班子 ──
    {"id": 13, "person_id": 5, "org_id": 2, "title": "灵宝市委常委、常务副市长", "start": "2024", "end": "现任", "rank": "副县级", "note": ""},
    {"id": 14, "person_id": 6, "org_id": 2, "title": "灵宝市委常委、宣传部部长、副市长", "start": "2024", "end": "现任", "rank": "副县级", "note": ""},
    {"id": 15, "person_id": 7, "org_id": 1, "title": "灵宝市委常委、组织部部长", "start": "2025", "end": "现任", "rank": "副县级", "note": ""},
    {"id": 16, "person_id": 8, "org_id": 3, "title": "灵宝市委常委、纪委书记、监委主任", "start": "2022", "end": "现任", "rank": "副县级", "note": "女"},
    {"id": 17, "person_id": 9, "org_id": 4, "title": "灵宝市人大常委会主任", "start": "2022", "end": "现任", "rank": "正县级", "note": "曾任市政协主席、市委常委、政法委书记"},
    {"id": 18, "person_id": 10, "org_id": 5, "title": "政协灵宝市委员会主席", "start": "2022", "end": "现任", "rank": "正县级", "note": ""},
    {"id": 19, "person_id": 11, "org_id": 1, "title": "灵宝市委常委、市委办公室主任", "start": "2024", "end": "现任", "rank": "副县级", "note": ""},
    {"id": 20, "person_id": 12, "org_id": 2, "title": "灵宝市副市长", "start": "2025", "end": "现任", "rank": "副县级", "note": ""},
    {"id": 21, "person_id": 13, "org_id": 2, "title": "灵宝市副市长", "start": "2025", "end": "现任", "rank": "副县级", "note": ""},
    {"id": 22, "person_id": 14, "org_id": 2, "title": "灵宝市副市长", "start": "2024", "end": "现任", "rank": "副县级", "note": ""},
    {"id": 23, "person_id": 15, "org_id": 2, "title": "灵宝市副市长", "start": "2024", "end": "现任", "rank": "副县级", "note": ""},
    {"id": 24, "person_id": 16, "org_id": 1, "title": "灵宝市委常委", "start": "2025", "end": "现任", "rank": "副县级", "note": ""},
    {"id": 25, "person_id": 17, "org_id": 1, "title": "灵宝市委常委", "start": "2025", "end": "现任", "rank": "副县级", "note": ""},
    {"id": 26, "person_id": 18, "org_id": 1, "title": "灵宝市委常委、统战部部长", "start": "2021", "end": "2023", "rank": "副县级", "note": ""},
    {"id": 27, "person_id": 19, "org_id": 1, "title": "灵宝市委常委、统战部部长", "start": "2023", "end": "现任", "rank": "副县级", "note": ""},
    # ── 跨县网络 ──
    {"id": 28, "person_id": 21, "org_id": 1, "title": "灵宝市委副书记、宣传部部长、寺河乡党委书记", "start": "", "end": "", "rank": "副县级", "note": "曾任灵宝市委副书记等，后调任渑池县长"},
    {"id": 29, "person_id": 21, "org_id": 9, "title": "渑池县委副书记、县长", "start": "2022", "end": "现任", "rank": "正县级", "note": ""},
]

relationships = [
    # ── 前后任 ──
    {"id": 1, "person_a_id": 3, "person_b_id": 1, "type": "交接", "context": "张志刚→宋速快 灵宝市委书记交接（2025年10月）", "overlap_org": "中共灵宝市委员会", "overlap_period": "2025-10"},
    {"id": 2, "person_a_id": 4, "person_b_id": 3, "type": "交接", "context": "孙淑芳→张志刚 灵宝市委书记交接（2021-2022）", "overlap_org": "中共灵宝市委员会", "overlap_period": "2021-2022"},
    # ── 党政搭档 ──
    {"id": 3, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "宋速快任书记、刘小旺任市长，党政正职搭档", "overlap_org": "灵宝市", "overlap_period": "2025-11-"},
    {"id": 4, "person_a_id": 1, "person_b_id": 2, "type": "接任", "context": "宋速快辞去市长，刘小旺接任市长", "overlap_org": "灵宝市人民政府", "overlap_period": "2025-11"},
    # ── 党务班子工作交集 ──
    {"id": 5, "person_a_id": 1, "person_b_id": 7, "type": "同僚", "context": "宋速快与田红方均为灵宝市委常委会班子成员", "overlap_org": "中共灵宝市委员会", "overlap_period": "2025-"},
    {"id": 6, "person_a_id": 8, "person_b_id": 1, "type": "上下级/同委会", "context": "陈少华（纪委书记、监委主任）与宋速快同在灵宝市委", "overlap_org": "中共灵宝市委员会", "overlap_period": "2022-"},
    {"id": 7, "person_a_id": 5, "person_b_id": 2, "type": "上下级", "context": "杜元华（常务副市长）协助市长刘小旺分管审计、政府运行", "overlap_org": "灵宝市人民政府", "overlap_period": "2024-"},
    {"id": 8, "person_a_id": 9, "person_b_id": 1, "type": "上下级", "context": "郭仙朋（市人大主任）对市委书记宋速快所辖政府工作实施监督", "overlap_org": "灵宝市", "overlap_period": "2025-"},
    # ── 跨地区干部交流 ──
    {"id": 9, "person_a_id": 1, "person_b_id": 21, "type": "跨县交流", "context": "周详曾任灵宝市委副书记，后调任渑池县长；宋速快亦曾任职渑池县", "overlap_org": "渑池县/灵宝", "overlap_period": ""},
    {"id": 10, "person_a_id": 3, "person_b_id": 1, "type": "跨县调动", "context": "宋速快、张志刚均先后经历渑池县与灵宝市的任职，属三门峡市域干部交流圈", "overlap_org": "三门峡市", "overlap_period": ""},
]

# ── BUILD SQLite DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
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
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>灵宝市领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Node colors: person by role, org by type ──
def person_color(pid):
    if pid == 1:      # 市委书记
        return "#E03C31", 20.0
    if pid == 2:      # 市长
        return "#2980B9", 20.0
    if pid in (5, 6, 12, 13, 14, 15):  # 政府/副市长
        return "#2980B9", 14.0
    if pid == 8:      # 纪委
        return "#E67E22", 14.0
    if pid in (3, 4): # 前任
        return "#95A5A6", 14.0
    if pid == 21:     # 跨县关联
        return "#95A5A6", 12.0
    return "#7F8C8D", 12.0   # 其他常委/班子

org_colors = {
    "党委": (231, 76, 60),
    "政府": (52, 152, 219),
    "纪委": (241, 196, 15),
    "人大": (155, 89, 182),
    "政协": (46, 204, 113),
}

lines.append('    <nodes>')
for p in persons:
    clr, size = person_color(p["id"])
    r, g, b = int(clr[1:3], 16), int(clr[3:5], 16), int(clr[5:7], 16)
    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append('      </node>')

for o in organizations:
    oid = 1000 + o["id"]
    c = org_colors.get(o["type"], (127, 140, 141))
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(pos["start"] or "?")} → {esc(pos["end"] or "今")}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    edge_id += 1

for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r["overlap_period"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")