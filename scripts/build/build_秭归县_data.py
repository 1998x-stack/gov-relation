#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 秭归县 (Zigui County) leadership network.

Sources:
- 秭归县人民政府官网 (www.hbzg.gov.cn) — 领导之窗 pages (primary, confirmed)
  - 县委领导: http://www.hbzg.gov.cn/list-2702-1.html
  - 县政府领导: http://www.hbzg.gov.cn/list-2704-1.html
  - 县人大领导: http://www.hbzg.gov.cn/list-2703-1.html
  - 县政协领导: http://www.hbzg.gov.cn/list-2705-1.html
- 宜昌市人民政府官网 (www.yichang.gov.cn) — 市级领导 for cross-county network
"""

import sqlite3
import sys
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE
while not (ROOT / "gov_relation").is_dir() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
BASE = str(ROOT)
DB_PATH = os.path.join(BASE, "data", "database", "秭归县_network.db")
GEXF_PATH = os.path.join(BASE, "data", "graph", "秭归县_network.gexf")
sys.path.insert(0, BASE)

from gov_relation.runner import run_build

AS_OF = "2026-08-07"

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── 1. CORE TARGETS ──
    {"id": 1, "name": "顾鹏飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1983年5月", "birthplace": "", "education": "博士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县委书记", "current_org": "中共秭归县委员会",
     "source": "http://www.hbzg.gov.cn/list-2702-1.html"},
    {"id": 2, "name": "李芹", "gender": "女", "ethnicity": "汉族",
     "birth": "1978年11月", "birthplace": "", "education": "大专学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县委副书记、县长", "current_org": "秭归县人民政府",
     "source": "http://www.hbzg.gov.cn/list-2704-1.html"},
    # ── 1b. PREDECESSOR / CAREER CONTEXT ──
    {"id": 24, "name": "杨勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "湖北省宜昌市夷陵区", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潜江市人民政府代市长（曾任秭归县委书记、县长）", "current_org": "潜江市人民政府",
     "source": "秭归县委县政府前任领导，媒体/百科报道"},
    # ── 2. 县委常委 (县委副书记 + standing committee) ──
    {"id": 3, "name": "李波", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年2月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县委副书记", "current_org": "中共秭归县委员会",
     "source": "http://www.hbzg.gov.cn/list-2702-1.html"},
    {"id": 4, "name": "杨卫海", "gender": "男", "ethnicity": "汉族",
     "birth": "1974年7月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县委常委、政法委书记", "current_org": "中共秭归县委政法委员会",
     "source": "http://www.hbzg.gov.cn/list-2702-1.html"},
    {"id": 5, "name": "余志红", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年4月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县委常委、常务副县长", "current_org": "秭归县人民政府",
     "source": "http://www.hbzg.gov.cn/list-2702-1.html"},
    {"id": 6, "name": "刘斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1983年12月", "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县委常委、县人武部政委", "current_org": "秭归县人民武装部",
     "source": "http://www.hbzg.gov.cn/list-2702-1.html"},
    {"id": 7, "name": "钟明政", "gender": "男", "ethnicity": "汉族",
     "birth": "1981年12月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县委常委、纪委书记、监委主任", "current_org": "中共秭归县纪律检查委员会",
     "source": "http://www.hbzg.gov.cn/list-2702-1.html"},
    {"id": 8, "name": "张妮娜", "gender": "女", "ethnicity": "汉族",
     "birth": "1979年2月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县委常委、宣传部长", "current_org": "中共秭归县委宣传部",
     "source": "http://www.hbzg.gov.cn/list-2702-1.html"},
    {"id": 9, "name": "朱荣庭", "gender": "男", "ethnicity": "汉族",
     "birth": "1983年4月", "birthplace": "", "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县委常委、副县长、湖北秭归经济开发区党工委书记",
     "current_org": "秭归县人民政府",
     "source": "http://www.hbzg.gov.cn/list-2702-1.html"},
    {"id": 10, "name": "宋兴建", "gender": "男", "ethnicity": "汉族",
     "birth": "1971年8月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县委常委、县委办公室主任", "current_org": "中共秭归县委办公室",
     "source": "http://www.hbzg.gov.cn/list-2702-1.html"},
    {"id": 11, "name": "黄战", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年10月", "birthplace": "", "education": "大学文学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县委常委、组织部长、统战部长、党校校长",
     "current_org": "中共秭归县委组织部",
     "source": "http://www.hbzg.gov.cn/list-2702-1.html"},
    # ── 3. 县政府 副县长 ──
    {"id": 12, "name": "向波", "gender": "男", "ethnicity": "汉族",
     "birth": "1973年3月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县人民政府党组成员、副县长", "current_org": "秭归县人民政府",
     "source": "http://www.hbzg.gov.cn/list-2704-1.html"},
    {"id": 13, "name": "徐斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年10月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县人民政府副县长（挂职）", "current_org": "秭归县人民政府",
     "source": "http://www.hbzg.gov.cn/list-2704-1.html"},
    {"id": 14, "name": "程泽锋", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年4月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县人民政府党组成员、副县长", "current_org": "秭归县人民政府",
     "source": "http://www.hbzg.gov.cn/list-2704-1.html"},
    {"id": 15, "name": "洪伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1973年6月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县人民政府副县长、公安局党委书记、局长",
     "current_org": "秭归县公安局",
     "source": "http://www.hbzg.gov.cn/list-2704-1.html"},
    {"id": 16, "name": "张浩", "gender": "男", "ethnicity": "汉族",
     "birth": "1985年8月", "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县人民政府党组成员、副县长", "current_org": "秭归县人民政府",
     "source": "http://www.hbzg.gov.cn/list-2704-1.html"},
    {"id": 17, "name": "宋思谕", "gender": "女", "ethnicity": "汉族",
     "birth": "1985年9月", "birthplace": "", "education": "博士研究生",
     "party_join": "", "work_start": "",
     "current_post": "秭归县人民政府副县长", "current_org": "秭归县人民政府",
     "source": "http://www.hbzg.gov.cn/list-2704-1.html"},
    {"id": 18, "name": "赵洪武", "gender": "男", "ethnicity": "汉族",
     "birth": "1986年5月", "birthplace": "", "education": "大学经济学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县人民政府副县长（挂职）", "current_org": "秭归县人民政府",
     "source": "http://www.hbzg.gov.cn/list-2704-1.html"},
    {"id": 19, "name": "张文强", "gender": "男", "ethnicity": "汉族",
     "birth": "1988年1月", "birthplace": "", "education": "研究生历史学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县人民政府副县长（挂职）", "current_org": "秭归县人民政府",
     "source": "http://www.hbzg.gov.cn/list-2704-1.html"},
    # ── 4. 县人大 ──
    {"id": 20, "name": "谭健康", "gender": "男", "ethnicity": "汉族",
     "birth": "1968年12月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县人大常委会主任", "current_org": "秭归县人民代表大会常务委员会",
     "source": "http://www.hbzg.gov.cn/list-2703-1.html"},
    {"id": 21, "name": "罗朝政", "gender": "男", "ethnicity": "汉族",
     "birth": "1973年7月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县人大常委会副主任", "current_org": "秭归县人民代表大会常务委员会",
     "source": "http://www.hbzg.gov.cn/list-2703-1.html"},
    # ── 5. 县政协 ──
    {"id": 22, "name": "王雄", "gender": "男", "ethnicity": "汉族",
     "birth": "1968年6月", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "秭归县政协主席", "current_org": "中国人民政治协商会议秭归县委员会",
     "source": "http://www.hbzg.gov.cn/list-2705-1.html"},
    {"id": 23, "name": "杨婧", "gender": "女", "ethnicity": "汉族",
     "birth": "1985年1月", "birthplace": "", "education": "研究生学历",
     "party_join": "民革党员", "work_start": "",
     "current_post": "秭归县政协副主席", "current_org": "中国人民政治协商会议秭归县委员会",
     "source": "http://www.hbzg.gov.cn/list-2705-1.html"},
]

organizations = [
    {"id": 1, "name": "中共秭归县委员会", "type": "党委", "level": "县处级",
     "parent": "中共宜昌市委员会", "location": "湖北省宜昌市秭归县"},
    {"id": 2, "name": "秭归县人民政府", "type": "政府", "level": "县处级",
     "parent": "宜昌市人民政府", "location": "湖北省宜昌市秭归县"},
    {"id": 3, "name": "中共秭归县委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共宜昌市委政法委员会", "location": "湖北省宜昌市秭归县"},
    {"id": 4, "name": "秭归县公安局", "type": "政府", "level": "县处级",
     "parent": "宜昌市公安局", "location": "湖北省宜昌市秭归县"},
    {"id": 5, "name": "秭归县人民武装部", "type": "政府", "level": "县处级",
     "parent": "宜昌军分区", "location": "湖北省宜昌市秭归县"},
    {"id": 6, "name": "中共秭归县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共宜昌市纪律检查委员会", "location": "湖北省宜昌市秭归县"},
    {"id": 7, "name": "中共秭归县委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共宜昌市委宣传部", "location": "湖北省宜昌市秭归县"},
    {"id": 8, "name": "中共秭归县委办公室", "type": "党委", "level": "县处级",
     "parent": "中共宜昌市委办公室", "location": "湖北省宜昌市秭归县"},
    {"id": 9, "name": "中共秭归县委组织部", "type": "党委", "level": "县处级",
     "parent": "中共宜昌市委组织部", "location": "湖北省宜昌市秭归县"},
    {"id": 10, "name": "湖北秭归经济开发区", "type": "开发区", "level": "县处级",
     "parent": "湖北省人民政府", "location": "湖北省宜昌市秭归县"},
    {"id": 11, "name": "秭归县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "宜昌市人民代表大会常务委员会", "location": "湖北省宜昌市秭归县"},
    {"id": 12, "name": "中国人民政治协商会议秭归县委员会", "type": "政协", "level": "县处级",
     "parent": "政协宜昌市委员会", "location": "湖北省宜昌市秭归县"},
    {"id": 13, "name": "潜江市人民政府", "type": "政府", "level": "省直管县级市",
     "parent": "湖北省人民政府", "location": "湖北省潜江市"},
]

positions = [
    # 顾鹏飞
    {"person_id": 1, "org_id": 1, "title": "秭归县委书记", "start_date": "2023.10", "end_date": "", "rank": "县处级正职", "note": "现任，自县长升任"},
    # 李芹
    {"person_id": 2, "org_id": 1, "title": "秭归县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "秭归县县长、县政府党组书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    # 李波
    {"person_id": 3, "org_id": 1, "title": "秭归县委副书记（专职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 杨卫海
    {"person_id": 4, "org_id": 1, "title": "秭归县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 4, "org_id": 3, "title": "县委政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 余志红
    {"person_id": 5, "org_id": 1, "title": "秭归县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 5, "org_id": 2, "title": "常务副县长、党组副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 刘斌
    {"person_id": 6, "org_id": 1, "title": "秭归县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 6, "org_id": 5, "title": "县人武部政委", "start_date": "", "end_date": "", "rank": "正团级", "note": "现任"},
    # 钟明政
    {"person_id": 7, "org_id": 1, "title": "秭归县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 7, "org_id": 6, "title": "县纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 张妮娜
    {"person_id": 8, "org_id": 1, "title": "秭归县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 8, "org_id": 7, "title": "县委宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 朱荣庭
    {"person_id": 9, "org_id": 1, "title": "秭归县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 9, "org_id": 10, "title": "湖北秭归经济开发区党工委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 宋兴建
    {"person_id": 10, "org_id": 1, "title": "秭归县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 10, "org_id": 8, "title": "县委办公室主任、县直机关工委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 黄战
    {"person_id": 11, "org_id": 1, "title": "秭归县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 11, "org_id": 9, "title": "县委组织部部长、统战部部长、党校校长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 向波
    {"person_id": 12, "org_id": 2, "title": "秭归县副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 徐斌
    {"person_id": 13, "org_id": 2, "title": "秭归县副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "挂职"},
    # 程泽锋
    {"person_id": 14, "org_id": 2, "title": "秭归县副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 洪伟
    {"person_id": 15, "org_id": 2, "title": "秭归县副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 15, "org_id": 4, "title": "县公安局党委书记、局长", "start_date": "", "end_date": "", "rank": "副处长级", "note": "现任"},
    # 张浩
    {"person_id": 16, "org_id": 2, "title": "秭归县副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 宋思谕
    {"person_id": 17, "org_id": 2, "title": "秭归县副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 赵洪武
    {"person_id": 18, "org_id": 2, "title": "秭归县副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "挂职"},
    # 张文强
    {"person_id": 19, "org_id": 2, "title": "秭归县副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "挂职"},
    # 谭健康
    {"person_id": 20, "org_id": 11, "title": "秭归县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    # 罗朝政
    {"person_id": 21, "org_id": 11, "title": "秭归县人大常委会副主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 王雄
    {"person_id": 22, "org_id": 12, "title": "秭归县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    # 杨婧
    {"person_id": 23, "org_id": 12, "title": "秭归县政协副主席", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任，民革"},
    # 杨勇 (前任书记/县长)
    {"person_id": 24, "org_id": 1, "title": "秭归县委书记（前任）", "start_date": "2021", "end_date": "2023", "rank": "县处级正职", "note": "后调任潜江"},
    {"person_id": 24, "org_id": 2, "title": "秭归县长（历任）", "start_date": "2016", "end_date": "2021", "rank": "县处级正职", "note": "历任县长"},
    {"person_id": 24, "org_id": 2, "title": "秭归常务副县长", "start_date": "2014", "end_date": "2016", "rank": "县处级副职", "note": "此前在夷陵/点军履职"},
    {"person_id": 24, "org_id": 13, "title": "潜江市代市长（现任）", "start_date": "2023", "end_date": "", "rank": "省直管县级市正职", "note": "调任去向"},
    # 顾鹏飞 早期路径
    {"person_id": 1, "org_id": 2, "title": "秭归县长（历任）", "start_date": "2021.8", "end_date": "2023.10", "rank": "县处级正职", "note": "此前任点军区"},
]

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "顾鹏飞（县委书记）与李芹（县长）党政一把手搭档",
     "overlap_org": "中共秭归县委员会", "overlap_period": "现任"},
    # 县委副书记班子
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "顾鹏飞与专职县委副书记李波工作配合",
     "overlap_org": "中共秭归县委员会", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 3, "type": "同僚",
     "context": "李芹与李波均为县委副书记",
     "overlap_org": "中共秭归县委员会", "overlap_period": "现任"},
    # 书记 - 常委
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "顾鹏飞与政法委书记杨卫海（县委班子）",
     "overlap_org": "中共秭归县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 7, "type": "上下级",
     "context": "顾鹏飞与纪委书记钟明政（县委班子）",
     "overlap_org": "中共秭归县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 11, "type": "上下级",
     "context": "顾鹏飞与组织部长黄战（县委班子）",
     "overlap_org": "中共秭归县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 8, "type": "上下级",
     "context": "顾鹏飞与宣传部长张妮娜（县委班子）",
     "overlap_org": "中共秭归县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 10, "type": "上下级",
     "context": "顾鹏飞与县委办主任宋兴建（直接工作关系）",
     "overlap_org": "中共秭归县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "顾鹏飞与人武部政委刘斌（党管武装）",
     "overlap_org": "中共秭归县委员会", "overlap_period": "现任"},
    # 县长 - 常务副县长 / 副县长班子
    {"person_a": 2, "person_b": 5, "type": "上下级",
     "context": "李芹与常务副县长余志红（政府班子）",
     "overlap_org": "秭归县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 9, "type": "上下级",
     "context": "李芹与副县长朱荣庭（政府班子）",
     "overlap_org": "秭归县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 12, "type": "上下级",
     "context": "李芹与副县长向波（政府班子）",
     "overlap_org": "秭归县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 14, "type": "上下级",
     "context": "李芹与副县长程泽锋（政府班子）",
     "overlap_org": "秭归县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 15, "type": "上下级",
     "context": "李芹与副县长、公安局长洪伟（政府班子）",
     "overlap_org": "秭归县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 16, "type": "上下级",
     "context": "李芹与副县长张浩（政府班子）",
     "overlap_org": "秭归县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 17, "type": "上下级",
     "context": "李芹与副县长宋思谕（政府班子）",
     "overlap_org": "秭归县人民政府", "overlap_period": "现任"},
    # 常委内部关系
    {"person_a": 4, "person_b": 7, "type": "同僚",
     "context": "杨卫海与钟明政均为县委常委",
     "overlap_org": "中共秭归县委员会", "overlap_period": "现任"},
    {"person_a": 11, "person_b": 8, "type": "同僚",
     "context": "黄战（组织）与张桃娜（宣传）均为县委常委",
     "overlap_org": "中共秭归县委员会", "overlap_period": "现任"},
    # 四套班子
    {"person_a": 1, "person_b": 20, "type": "同僚",
     "context": "顾鹏飞与人大主任谭健康四套班子共事",
     "overlap_org": "秭归县人民政府", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 22, "type": "同僚",
     "context": "顾鹏飞与政协主席王雄四套班子共事",
     "overlap_org": "秭归县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 20, "type": "同僚",
     "context": "李芹与人大主任谭健康四套班子共事",
     "overlap_org": "秭归县人民政府", "overlap_period": "现任"},
{"person_a": 2, "person_b": 22, "type": "同僚",
     "context": "李芹与政协主席王雄四套班子共事",
     "overlap_org": "秭归县人民政府", "overlap_period": "现任"},
    # 前任/继任链条
    {"person_a": 24, "person_b": 1, "type": "交接",
     "context": "杨勇→顾鹏飞，秭归县委书记职务交接（2023.10）",
     "overlap_org": "中共秭归县委员会", "overlap_period": "2023"},
    {"person_a": 1, "person_b": 2, "type": "交接",
     "context": "顾鹏飞→李芹，秭归县长职务交接（2023-2024）",
     "overlap_org": "秭归县人民政府", "overlap_period": "2023-2024"},
    {"person_a": 24, "person_b": 2, "type": "交接",
     "context": "杨勇→李芹，历届秭归县长更替",
     "overlap_org": "秭归县人民政府", "overlap_period": "2016-2024"},
]

# ═══════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════

run_build(
    slug="秭归县领导班子关系图",
    persons=persons,
    organizations=organizations,
    positions=positions,
    relationships=relationships,
    db_path=DB_PATH,
    gexf_path=GEXF_PATH,
    overwrite=True,
)

print("\nBuild complete (canonical data dirs).")
print(f"  DB:  {DB_PATH}")
print(f"  GEXF:{GEXF_PATH}")
print(f"Total: {len(persons)} persons, {len(organizations)} orgs, "
      f"{len(positions)} positions, {len(relationships)} relationships")
print(f"As-of: {AS_OF}  (source: www.hbzg.gov.cn 领导之窗)")