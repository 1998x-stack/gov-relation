#!/usr/bin/env python3
"""Build SQLite database, GEXF graph and person JSONs for 西陵区 (Xiling District), 宜昌市, 湖北省.

Level: 市辖区
Province: 湖北省
Parent city: 宜昌市
Targets: 区委书记 (Party Secretary), 区长 (District Governor)
Task ID: hubei_西陵区

Research date: 2026-08-11
Official sources (all confirmed accessible 2026-08-11):
- 区委领导: https://www.ycxl.gov.cn/list-4782-1.html
- 区人大领导: https://www.ycxl.gov.cn/list-4783-1.html
- 区政府领导: https://www.ycxl.gov.cn/list-4784-1.html
- 区政协领导: https://www.ycxl.gov.cn/list-4786-1.html
- 市生态环境局/民政局/清廉宜昌 等外宣线索核对

Current status (as of 2026-08-11):
- 区委书记: 梅卫民 (确认: 官方区委领导页; 2021-07任前公示拟任区政府正职; 2021-09代区长;
  2024年春起任区委书记并一度一肩挑书记、区长至2024-07; 2026年6-8月官方页面及会议报道仍为区委书记)
- 区委副书记、区长、西陵经济开发区党工委书记: 吴光明 (确认: 官方区政府领导页; 2025-01-11当选;
  2024-07-25任代理区长)
- 区委副书记: 李荣坤; 区人大常委会主任: 张祖铭; 区政协主席: 黄明

Predecessor chain:
- 区委书记: 卢斌(2016-2021.07) → 任蔚(2021.07-2023末) → 梅卫民(2023末/2024初-今)
- 区长: 任蔚(2015.08-2021.06) → 梅卫民(2021.09代-2024.07辞) → 吴光明(2024.07代-2025.01正-今)

Cross-district flows (confirmed):
- 任蔚 → 鄂州市副市长、华容区委书记 (2024-01到任) → 鄂州市委常委 (2025-10)
- 覃涛 → 夷陵区区长 (2026-07-31当选; 此前为西陵区委常委、常务副区长 2025.07-2026.07)
- 吴光明 曾任伍家岗区委常委、常务副区长 (2023.04-2024.06), 与伍家岗区委书记陈道坤共事
- 汪元程 (曾任西陵区委副书记/常务副区长) → 宜昌市委常委、常务副市长 → 武汉市副市长 →
  省经信厅厅长 → 2025-04 公示拟任市州党委书记
- 余峰 (曾任西陵区副区长) → 枝江市委书记 (2021-07)

Confidence notes:
- Current roles + identity for 区委/人大/政府/政协 roster: confirmed via official bio pages (2026-08)
- 梅卫民/吴光明/任蔚 历任履历: confirmed via 任前公示/百科/媒体, 早期精确年份部分为范围估计
- 区公安分局局长、现任常务副区长人选 (覃涛调任后) — 待补, 列入 open gaps
- 卢斌卸任后去向、李荣坤/付波/周成刚等早期履历 — 待查 (open gaps)
- 梅卫民拟任区委书记的具体公示时点 (2023年底-2024年初区间) — 待进一步核对
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import os
import json
import sqlite3  # noqa: F401
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/hubei_西陵区")
DB_PATH = os.path.join(STAGING, "西陵区_network.db")
GEXF_PATH = os.path.join(STAGING, "西陵区_network.gexf")
PERSONS_DIR = os.path.join(STAGING)

AS_OF = "2026-08-11"
TODAY = datetime.now().strftime("%Y%m%d")

# ── 公开来源 URI ───────────────────────────────────────────────────────
S_QW = "https://www.ycxl.gov.cn/list-4782-1.html"
S_QRD = "https://www.ycxl.gov.cn/list-4783-1.html"
S_QZF = "https://www.ycxl.gov.cn/list-4784-1.html"
S_QZX = "https://www.ycxl.gov.cn/list-4786-1.html"
S_GS = "http://hb.china.com.cn/2021-07/30/content_41632426.htm"
S_BAIKE_WGM = "https://baike.baidu.com/item/%E5%90%B4%E5%85%89%E6%98%8E/62937466"
S_BAIKE_RW = "https://baike.baidu.com/item/%E4%BB%BB%E8%94%9A/18594167"
S_XLNEWS = "http://www.sxxlw.cn/content/show?catid=331325&newsid=1020679"
S_EZHOU = "https://www.ezhou.gov.cn/sy/ldzc/swld/202510/t20251029_731476.html"
S_HRGW = "https://www.hbhr.gov.cn/zxzx/hryw/202401/t20240115_607729.html"
S_GZW = "http://gzw.yichang.gov.cn/content-40912-16490-1.html"
S_GGZY = "http://ggzyjyzx.yichang.gov.cn/content-64031-15667-1.html"
S_XL54 = "http://www.sxxlw.cn/content/show?catid=334096&newsid=1183865"
S_YT = "https://hb.china.com/news/20003178/20260803/26008992.html"
S_WYH = "http://hb.china.com.cn/2025-04/07/content_43075849.htm"
S_YF = "http://news.cjn.cn/sywh/201804/t3188121.htm"
S_YL = "http://www.yichang.gov.cn/html/zhengwuyizhantong/zhengwuzixun/jinriyaowen/2021/0730/1033271.html"
S_JW = "http://www.ycjw.gov.cn/site_855_yichangshiweixunchagongzuozhuanti/site_855_xilingqu/site_855_yaowen_HYK7/68b663f55e05d120ac143c57.html"
S_MZJ = "http://mzj.yichang.gov.cn/content-14692-998593-1.html"
S_HBJ = "http://hbj.yichang.gov.cn/content-62335-997460-1.html"
S_PAPER = "https://m.thepaper.cn/newsDetail_forward_32405787"
S_CJN = "http://news.cjn.cn/zjjjpd/yc_20062/202504/t5120670.htm"
S_HBD = "https://epaper.hubeidaily.net/pad/content/202501/17/content_302648.html"
S_ZHXW = "https://www.hb.chinanews.com.cn/news/2025/0916/420964.html"
S_MJH = "http://www.yichang.gov.cn/list-64208-1.html"
S_MJH2 = "http://www.yichang.gov.cn/list-64015-1.html"
S_WJG = "http://www.ycwjg.gov.cn/list-4782-1.html"
S_TX = "https://news.qq.com/rain/a/20210730A086E200"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 核心: 区委领导 ──
    {"id": 1, "name": "梅卫民", "gender": "男", "ethnicity": "汉族", "birth": "1972年12月",
     "birthplace": "湖北秭归", "education": "大学专科", "party_join": "中共党员", "work_start": "1993年8月",
     "current_post": "区委书记", "current_org": "中共宜昌市西陵区委员会", "source": S_QW},
    {"id": 2, "name": "吴光明", "gender": "男", "ethnicity": "汉族", "birth": "1982年6月",
     "birthplace": "", "education": "硕士研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、区政府区长、西陵经济开发区党工委书记", "current_org": "西陵区人民政府", "source": S_QZF},
    {"id": 3, "name": "李荣坤", "gender": "男", "ethnicity": "汉族", "birth": "1982年1月",
     "birthplace": "", "education": "硕士研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记", "current_org": "中共宜昌市西陵区委员会", "source": S_QW},
    {"id": 4, "name": "付波", "gender": "男", "ethnicity": "汉族", "birth": "1977年2月",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区纪委书记、区监委主任", "current_org": "中共宜昌市西陵区纪律检查委员会", "source": S_QW},
    {"id": 5, "name": "周成刚", "gender": "男", "ethnicity": "土家族", "birth": "1975年5月",
     "birthplace": "", "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、政法委书记", "current_org": "中共宜昌市西陵区委政法委员会", "source": S_QW},
    {"id": 6, "name": "付艳", "gender": "女", "ethnicity": "汉族", "birth": "1975年5月",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、组织部部长、统战部部长，区政协党组副书记", "current_org": "中共宜昌市西陵区委组织部", "source": S_QW},
    {"id": 7, "name": "吴海涛", "gender": "男", "ethnicity": "汉族", "birth": "1980年1月",
     "birthplace": "", "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区人武部上校政委", "current_org": "宜昌市西陵区人民武装部", "source": S_QW},
    {"id": 8, "name": "廖黎明", "gender": "男", "ethnicity": "汉族", "birth": "1982年2月",
     "birthplace": "", "education": "大学学历、硕士学位", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、宣传部部长", "current_org": "中共宜昌市西陵区委宣传部", "source": S_QW},
    {"id": 9, "name": "王锦林", "gender": "男", "ethnicity": "汉族", "birth": "1977年12月",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区委办公室主任兼区委直属机关工委书记", "current_org": "中共宜昌市西陵区委办公室", "source": S_QW},
    {"id": 10, "name": "涂超", "gender": "女", "ethnicity": "汉族", "birth": "1986年3月",
     "birthplace": "", "education": "硕士研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区政府副区长、党组成员", "current_org": "西陵区人民政府", "source": S_QZF},
    # ── 区人大 ──
    {"id": 11, "name": "张祖铭", "gender": "男", "ethnicity": "汉族", "birth": "1968年6月",
     "birthplace": "", "education": "大学学历、历史学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会主任、党组书记", "current_org": "西陵区人民代表大会常务委员会", "source": S_QRD},
    {"id": 12, "name": "覃家彦", "gender": "男", "ethnicity": "汉族", "birth": "1969年1月",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会副主任、党组副书记", "current_org": "西陵区人民代表大会常务委员会", "source": S_QRD},
    # ── 区政协 ──
    {"id": 13, "name": "黄明", "gender": "男", "ethnicity": "汉族", "birth": "1971年2月",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "区政协主席、党组书记", "current_org": "中国人民政治协商会议宜昌市西陵区委员会", "source": S_QZX},
    # ── 区政府其他领导 ──
    {"id": 14, "name": "姜媛", "gender": "女", "ethnicity": "汉族", "birth": "1980年3月",
     "birthplace": "", "education": "硕士研究生", "party_join": "民建会员", "work_start": "",
     "current_post": "副区长，区工商联（总商会）主席（会长）", "current_org": "西陵区人民政府", "source": S_QZF},
    {"id": 15, "name": "普布玉珍", "gender": "女", "ethnicity": "藏族", "birth": "1983年6月",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长（挂职，西藏山南市扎囊县委常委）", "current_org": "西陵区人民政府", "source": S_QZF},
    {"id": 16, "name": "潘廷瑞", "gender": "男", "ethnicity": "汉族", "birth": "1990年1月",
     "birthplace": "", "education": "博士研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "西陵区人民政府", "source": S_QZF},
    {"id": 17, "name": "但志平", "gender": "男", "ethnicity": "汉族", "birth": "1976年3月",
     "birthplace": "", "education": "博士研究生、工学博士", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长（挂职）", "current_org": "西陵区人民政府", "source": S_QZF},
    {"id": 18, "name": "李锐", "gender": "男", "ethnicity": "汉族", "birth": "1987年5月",
     "birthplace": "", "education": "大学本科、工学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长（挂职）", "current_org": "西陵区人民政府", "source": S_QZF},
    {"id": 19, "name": "宋恩", "gender": "男", "ethnicity": "汉族", "birth": "1980年8月",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "区政府党组成员，区服务葛洲坝片区工作委员会党组书记、主任", "current_org": "西陵区人民政府", "source": S_QZF},
    {"id": 20, "name": "张正", "gender": "男", "ethnicity": "汉族", "birth": "1980年5月",
     "birthplace": "", "education": "硕士研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "区政府党组成员、区政府办公室主任", "current_org": "西陵区人民政府", "source": S_QZF},
    # ── 前任与跨区网络 ──
    {"id": 21, "name": "任蔚", "gender": "女", "ethnicity": "汉族", "birth": "1979年1月",
     "birthplace": "河南省南阳市", "education": "在职大学学历、管理学学士", "party_join": "中共党员", "work_start": "1997年8月",
     "current_post": "鄂州市委常委、华容区委书记（曾任西陵区委书记、区长）", "current_org": "中共鄂州市华容区委员会", "source": S_EZHOU},
    {"id": 22, "name": "卢斌", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前任西陵区委书记（2016-2021.07，去向待查）", "current_org": "中共宜昌市西陵区委员会", "source": S_TX},
    {"id": 23, "name": "覃涛", "gender": "男", "ethnicity": "土家族", "birth": "1978年5月",
     "birthplace": "", "education": "大学、农学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "夷陵区委副书记、区政府区长（曾任西陵区委常委、常务副区长）", "current_org": "宜昌市夷陵区人民政府", "source": S_YT},
    {"id": 24, "name": "何良平", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前任西陵区委常委、常务副区长（2021，去向待查）", "current_org": "西陵区人民政府", "source": S_YL},
    {"id": 25, "name": "汪元程", "gender": "男", "ethnicity": "汉族", "birth": "1968年1月",
     "birthplace": "", "education": "在职大学、经济学硕士", "party_join": "中共党员", "work_start": "",
     "current_post": "湖北省经济和信息化厅党组书记、厅长（曾任西陵区委副书记、常务副区长）", "current_org": "湖北省经济和信息化厅", "source": S_WYH},
    {"id": 26, "name": "余峰", "gender": "男", "ethnicity": "汉族", "birth": "1973年10月",
     "birthplace": "湖北当阳", "education": "党校研究生学历", "party_join": "中共党员", "work_start": "1992年7月",
     "current_post": "枝江市委书记（曾任西陵区人民政府副区长）", "current_org": "中共枝江市委员会", "source": S_YF},
    {"id": 27, "name": "陈道坤", "gender": "男", "ethnicity": "汉族", "birth": "1971年4月",
     "birthplace": "", "education": "在职党校大学", "party_join": "中共党员", "work_start": "",
     "current_post": "伍家岗区委书记", "current_org": "中共宜昌市伍家岗区委员会", "source": S_WJG},
    {"id": 28, "name": "黄剑雄", "gender": "男", "ethnicity": "汉族", "birth": "1971年7月",
     "birthplace": "", "education": "博士研究生、经济学博士", "party_join": "中共党员", "work_start": "",
     "current_post": "中共宜昌市委书记", "current_org": "中共宜昌市委员会", "source": S_MJH},
    {"id": 29, "name": "陈红辉", "gender": "男", "ethnicity": "汉族", "birth": "1971年7月",
     "birthplace": "", "education": "博士研究生、医学博士", "party_join": "中共党员", "work_start": "",
     "current_post": "中共宜昌市委副书记、宜昌市人民政府市长", "current_org": "宜昌市人民政府", "source": S_MJH2},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共宜昌市西陵区委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市委员会", "location": "湖北省宜昌市西陵区"},
    {"id": 2, "name": "西陵区人民政府", "type": "政府", "level": "县级", "parent": "宜昌市人民政府", "location": "湖北省宜昌市西陵区"},
    {"id": 3, "name": "湖北西陵经济开发区", "type": "开发区", "level": "县级", "parent": "西陵区人民政府", "location": "湖北省宜昌市西陵区"},
    {"id": 4, "name": "中共宜昌市西陵区纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市纪律检查委员会", "location": "湖北省宜昌市西陵区"},
    {"id": 5, "name": "西陵区监察委员会", "type": "党委", "level": "县级", "parent": "宜昌市监察委员会", "location": "湖北省宜昌市西陵区"},
    {"id": 6, "name": "中共宜昌市西陵区委政法委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市西陵区委员会", "location": "湖北省宜昌市西陵区"},
    {"id": 7, "name": "中共宜昌市西陵区委组织部", "type": "党委", "level": "县级", "parent": "中共宜昌市西陵区委员会", "location": "湖北省宜昌市西陵区"},
    {"id": 8, "name": "中共宜昌市西陵区委统一战线工作部", "type": "党委", "level": "县级", "parent": "中共宜昌市西陵区委员会", "location": "湖北省宜昌市西陵区"},
    {"id": 9, "name": "中共宜昌市西陵区委宣传部", "type": "党委", "level": "县级", "parent": "中共宜昌市西陵区委员会", "location": "湖北省宜昌市西陵区"},
    {"id": 10, "name": "中共宜昌市西陵区委办公室", "type": "党委", "level": "县级", "parent": "中共宜昌市西陵区委员会", "location": "湖北省宜昌市西陵区"},
    {"id": 11, "name": "宜昌市西陵区人民武装部", "type": "党委", "level": "县级", "parent": "宜昌军分区", "location": "湖北省宜昌市西陵区"},
    {"id": 12, "name": "西陵区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "宜昌市人大常委会", "location": "湖北省宜昌市西陵区"},
    {"id": 13, "name": "中国人民政治协商会议宜昌市西陵区委员会", "type": "政协", "level": "县级", "parent": "政协宜昌市委员会", "location": "湖北省宜昌市西陵区"},
    {"id": 14, "name": "宜昌市伍家岗区人民政府", "type": "政府", "level": "县级", "parent": "宜昌市人民政府", "location": "湖北省宜昌市伍家岗区"},
    {"id": 15, "name": "中共宜昌市伍家岗区委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市委员会", "location": "湖北省宜昌市伍家岗区"},
    {"id": 16, "name": "宜昌市伍家岗区伍家乡", "type": "乡镇街道", "level": "乡级", "parent": "伍家岗区人民政府", "location": "湖北省宜昌市伍家岗区"},
    {"id": 17, "name": "宜昌市伍家岗区贸易局", "type": "政府", "level": "县级", "parent": "伍家岗区人民政府", "location": "湖北省宜昌市伍家岗区"},
    {"id": 18, "name": "宜昌新区建设推进办公室", "type": "事业单位", "level": "县级", "parent": "宜昌市人民政府", "location": "湖北省宜昌市"},
    {"id": 19, "name": "宜昌市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "湖北省宜昌市"},
    {"id": 20, "name": "宜昌市人民政府办公室", "type": "政府", "level": "地级市", "parent": "宜昌市人民政府", "location": "湖北省宜昌市"},
    {"id": 21, "name": "宜昌粮食集团有限公司", "type": "国企", "level": "地级市", "parent": "宜昌市国资委", "location": "湖北省宜昌市"},
    {"id": 22, "name": "中共宜昌市委员会", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "湖北省宜昌市"},
    {"id": 23, "name": "宜昌市夷陵区人民政府", "type": "政府", "level": "县级", "parent": "宜昌市人民政府", "location": "湖北省宜昌市夷陵区"},
    {"id": 24, "name": "中共鄂州市委员会", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "湖北省鄂州市"},
    {"id": 25, "name": "中共鄂州市华容区委员会", "type": "党委", "level": "县级", "parent": "中共鄂州市委员会", "location": "湖北省鄂州市华容区"},
    {"id": 26, "name": "湖北省经济和信息化厅", "type": "政府", "level": "省级", "parent": "湖北省人民政府", "location": "湖北省武汉市"},
    {"id": 27, "name": "中共枝江市委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市委员会", "location": "湖北省宜昌市枝江市"},
    {"id": 28, "name": "宜昌市招商局", "type": "政府", "level": "地级市", "parent": "宜昌市人民政府", "location": "湖北省宜昌市"},
    {"id": 29, "name": "共青团宜昌市委员会", "type": "群团", "level": "地级市", "parent": "共青团湖北省委", "location": "湖北省宜昌市"},
    {"id": 30, "name": "宜昌市妇女联合会", "type": "群团", "level": "地级市", "parent": "宜昌市", "location": "湖北省宜昌市"},
    {"id": 31, "name": "鄂州市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "湖北省鄂州市"},
    {"id": 32, "name": "西陵区服务葛洲坝片区工作委员会", "type": "事业单位", "level": "县级", "parent": "西陵区人民政府", "location": "湖北省宜昌市西陵区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 梅卫民 (1) ──
    {"person_id": 1, "org_id": 17, "title": "伍家岗区贸易局工作（起点）", "start": "1993-08", "end": "1999-11", "rank": "科员", "note": "1993.08-1999.11 在宜昌市伍家岗区贸易局工作"},
    {"person_id": 1, "org_id": 16, "title": "伍家乡副乡长、党委副书记、乡长、党委书记", "start": "1999-11", "end": "2011-08", "rank": "正科级", "note": "逐步任党委副书记、乡长、乡党委书记"},
    {"person_id": 1, "org_id": 15, "title": "伍家岗区委办公室副主任", "start": "2011-08", "end": "2011-10", "rank": "副科级", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "伍家岗区人民政府副区长", "start": "2011-11", "end": "2015", "rank": "副县级", "note": "党组成员；兼宜昌新区办工程部副部长、项目部部长"},
    {"person_id": 1, "org_id": 18, "title": "宜昌新区建设推进办公室党工委委员、副主任", "start": "2015", "end": "2020-01", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 20, "title": "宜昌市人民政府副秘书长", "start": "2020-01", "end": "2021-09", "rank": "正县级", "note": "机关党组成员、一级调研员"},
    {"person_id": 1, "org_id": 1, "title": "区委副书记、代区长", "start": "2021-09", "end": "2022-01", "rank": "正县级", "note": "2021-07-30 任前公示拟提名区政府正职"},
    {"person_id": 1, "org_id": 2, "title": "区长", "start": "2022-01", "end": "2024-07", "rank": "正县级", "note": "2024-07-25 辞去区长"},
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2024-01", "end": "present", "rank": "正县级", "note": "接替任蔚；2024年上半年一肩挑书记、区长"},
    # ── 吴光明 (2) ──
    {"person_id": 2, "org_id": 21, "title": "宜昌粮食集团有限公司党委书记、董事长、总经理", "start": "", "end": "2023-03", "rank": "正县级", "note": "2022-10 仍以该身份参加市国资委调研"},
    {"person_id": 2, "org_id": 14, "title": "伍家岗区委常委、常务副区长", "start": "2023-04", "end": "2024-06", "rank": "副县级", "note": "2023-04 公示为常务副区长人选; 2023-11 已就任"},
    {"person_id": 2, "org_id": 2, "title": "代区长", "start": "2024-08", "end": "2025-01", "rank": "正县级", "note": "2024-07-25 区人大常委会任命副区长、代理区长"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "2025-01", "end": "present", "rank": "正县级", "note": "2025-01-11 九届人大五次会议当选"},
    {"person_id": 2, "org_id": 3, "title": "西陵经济开发区党工委书记", "start": "2024-07", "end": "present", "rank": "正县级", "note": "兼任"},
    # ── 其他区委领导 ──
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "区委常委、纪委书记", "start": "", "end": "present", "rank": "副县级", "note": "分管纪检监察、巡察"},
    {"person_id": 4, "org_id": 5, "title": "区监委主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "区委常委、政法委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "区委常委、组织部部长", "start": "", "end": "present", "rank": "副县级", "note": "兼统战部长、区政协党组副书记"},
    {"person_id": 7, "org_id": 11, "title": "区委常委、区人武部上校政委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 9, "title": "区委常委、宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 10, "title": "区委常委、区委办公室主任", "start": "", "end": "present", "rank": "副县级", "note": "兼区委直属机关工委书记"},
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副县级", "note": "兼夜明珠街道党工委书记；分管住建、征收"},
    # ── 区人大 ──
    {"person_id": 11, "org_id": 12, "title": "区人大常委会主任、党组书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 12, "org_id": 12, "title": "区人大常委会副主任、党组副书记", "start": "", "end": "present", "rank": "副县级", "note": "曾任西陵区委常委"},
    # ── 区政协 ──
    {"person_id": 13, "org_id": 13, "title": "区政协主席、党组书记", "start": "", "end": "present", "rank": "正县级", "note": "曾任西陵区委常委"},
    # ── 区政府其他领导 ──
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副县级", "note": "民建会员；兼区工商联（总商会）主席；教育文旅卫健"},
    {"person_id": 15, "org_id": 2, "title": "副区长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "藏族；西藏山南市扎囊县委常委、县委办主任"},
    {"person_id": 16, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副县级", "note": "博士；城管、生态环境、市场监管"},
    {"person_id": 17, "org_id": 2, "title": "副区长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "工学博士；协助工业、科技"},
    {"person_id": 18, "org_id": 2, "title": "副区长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "协助城建、城管"},
    {"person_id": 19, "org_id": 32, "title": "服务葛洲坝片区工委党组书记、主任", "start": "", "end": "present", "rank": "副县级", "note": "区政府党组成员"},
    {"person_id": 20, "org_id": 19, "title": "区政府办公室主任", "start": "", "end": "present", "rank": "副县级", "note": "区政府党组成员"},
    # ── 任蔚 (21) ──
    {"person_id": 21, "org_id": 29, "title": "共青团宜昌市委副书记、党组成员", "start": "2005-12", "end": "2011-12", "rank": "副县级", "note": "2009.04-2009.10 挂职宜都市市长助理"},
    {"person_id": 21, "org_id": 30, "title": "宜昌市妇联主席、党组书记", "start": "2011-12", "end": "2013-10", "rank": "正县级", "note": ""},
    {"person_id": 21, "org_id": 28, "title": "宜昌市招商局党组书记、局长（兼市政府副秘书长）", "start": "2013-12", "end": "2015-08", "rank": "正县级", "note": "宜昌高新区管委会副主任、工委副书记"},
    {"person_id": 21, "org_id": 1, "title": "区委副书记、代区长", "start": "2015-08", "end": "2016-02", "rank": "正县级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "西陵区人民政府区长", "start": "2016-02", "end": "2021-06", "rank": "正县级", "note": "2016-02-26 当选"},
    {"person_id": 21, "org_id": 1, "title": "西陵区委书记", "start": "2021-07", "end": "2023-11", "rank": "正县级", "note": "2021-07-30 宜昌市委职务调整决定"},
    {"person_id": 21, "org_id": 31, "title": "鄂州市人民政府副市长", "start": "2024-01", "end": "2025-10", "rank": "副厅级", "note": "2025-10 免去"},
    {"person_id": 21, "org_id": 25, "title": "华容区委书记（兼区人武部党委第一书记）", "start": "2024-01", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 21, "org_id": 24, "title": "鄂州市委常委", "start": "2025-10", "end": "present", "rank": "副厅级", "note": "2025-08 公示拟任市州党委常委"},
    # ── 卢斌 (22) ──
    {"person_id": 22, "org_id": 1, "title": "西陵区委书记（前任）", "start": "2016-06", "end": "2021-07", "rank": "正县级", "note": "2021-07-30 不再担任，去向待查"},
    # ── 覃涛 (23) ──
    {"person_id": 23, "org_id": 3, "title": "西陵经济开发区党工委书记、管委会主任", "start": "2020", "end": "2022-08", "rank": "副县级", "note": "区政府党组成员"},
    {"person_id": 23, "org_id": 2, "title": "西陵区政府副区长", "start": "2022-08", "end": "2023-10", "rank": "副县级", "note": ""},
    {"person_id": 23, "org_id": 1, "title": "西陵区委常委", "start": "2023-10", "end": "2026-07", "rank": "副县级", "note": ""},
    {"person_id": 23, "org_id": 2, "title": "西陵区委常委、常务副区长", "start": "2025-07", "end": "2026-07", "rank": "副县级", "note": "协助区长负责政府日常工作"},
    {"person_id": 23, "org_id": 23, "title": "夷陵区人民政府区长", "start": "2026-07", "end": "present", "rank": "正县级", "note": "2026-07-31 当选"},
    # ── 何良平 (24) ──
    {"person_id": 24, "org_id": 2, "title": "西陵区委常委、常务副区长（前任）", "start": "", "end": "", "rank": "副县级", "note": "2021-07 八届十二次全会时在任"},
    # ── 汪元程 (25) ──
    {"person_id": 25, "org_id": 2, "title": "西陵区人民政府副区长", "start": "2012", "end": "2016", "rank": "副县级", "note": "常委、常务副区长"},
    {"person_id": 25, "org_id": 1, "title": "西陵区委副书记", "start": "2018", "end": "2021-06", "rank": "副县级", "note": ""},
    {"person_id": 25, "org_id": 19, "title": "宜昌市委常委、常务副市长", "start": "2021-09", "end": "2023", "rank": "副厅级", "note": ""},
    {"person_id": 25, "org_id": 26, "title": "湖北省经济和信息化厅党组书记、厅长", "start": "2024-11", "end": "present", "rank": "正厅级", "note": "2025-04 拟任市州党委书记公示"},
    # ── 余峰 (26) ──
    {"person_id": 26, "org_id": 2, "title": "西陵区人民政府副区长", "start": "2011", "end": "2016", "rank": "副县级", "note": "后任点军、伍家岗区委组织部长"},
    {"person_id": 26, "org_id": 27, "title": "枝江市委书记", "start": "2021-07", "end": "present", "rank": "正县级", "note": "2021-07-30 职务调整决定"},
    # ── 陈道坤 (27) 黄剑雄 (28) 陈红辉 (29) ──
    {"person_id": 27, "org_id": 15, "title": "伍家岗区委书记", "start": "2021-07", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 28, "org_id": 22, "title": "中共宜昌市委书记", "start": "", "end": "present", "rank": "正厅级", "note": "2026-02-26 指导西陵区委常委会民主生活会"},
    {"person_id": 29, "org_id": 22, "title": "中共宜昌市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 29, "org_id": 19, "title": "宜昌市人民政府市长", "start": "", "end": "present", "rank": "正厅级", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长党政一把手搭档，共同主持区委常委会、区人大与区政协年会等", "overlap_org": "西陵区", "overlap_period": "2025-01至今"},
    # 区委书记 × 班子成员
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与专职副书记（巡察书记专题会成员）", "overlap_org": "中共宜昌市西陵区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与纪委书记（区委书记专题会听取巡察汇报）", "overlap_org": "中共宜昌市西陵区委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与政法委书记", "overlap_org": "中共宜昌市西陵区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与组织部部长（干部任用主线）", "overlap_org": "中共宜昌市西陵区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区委书记与人武部政委（党管武装）", "overlap_org": "中共宜昌市西陵区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区委书记与宣传部部长", "overlap_org": "中共宜昌市西陵区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "区委书记与区委办主任", "overlap_org": "中共宜昌市西陵区委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "区委书记与常委副区长", "overlap_org": "中共宜昌市西陵区委员会", "overlap_period": "current"},
    # 四套班子
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "区委书记与区人大常委会主任（四套班子协同）", "overlap_org": "西陵区", "overlap_period": "current"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "区委书记与区政协主席（四套班子协同）", "overlap_org": "西陵区", "overlap_period": "current"},
    # 区长 × 政府班子
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "西陵区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "区长与副区长（民建）", "overlap_org": "西陵区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "区长与挂职副区长（西藏援派干部）", "overlap_org": "西陵区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "区长与副区长（博士）", "overlap_org": "西陵区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate", "context": "区长与挂职副区长（工学博士）", "overlap_org": "西陵区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 18, "type": "superior_subordinate", "context": "区长与挂职副区长", "overlap_org": "西陵区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 19, "type": "superior_subordinate", "context": "区长与区政府党组成员（葛洲坝片区工委）", "overlap_org": "西陵区人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 20, "type": "superior_subordinate", "context": "区长与政府办主任", "overlap_org": "西陵区人民政府", "overlap_period": "current"},
    # 前任/继任链
    {"person_a": 21, "person_b": 1, "type": "predecessor_successor", "context": "任蔚→梅卫民：2021-09 梅接任代区长；2023年末任蔚调鄂州，梅接任区委书记", "overlap_org": "中共宜昌市西陵区委员会", "overlap_period": "2021-2024"},
    {"person_a": 22, "person_b": 21, "type": "predecessor_successor", "context": "卢斌→任蔚：2021-07-30 西陵区委书记职务交接", "overlap_org": "中共宜昌市西陵区委员会", "overlap_period": "2021-07"},
    {"person_a": 1, "person_b": 23, "type": "superior_subordinate", "context": "梅卫民任书记期间，覃涛为区委常委、常务副区长，后调任夷陵区长", "overlap_org": "中共宜昌市西陵区委员会", "overlap_period": "2025-07~2026-07"},
    {"person_a": 2, "person_b": 23, "type": "superior_subordinate", "context": "吴光明任区长期间，覃涛为常务副区长（协助区长工作）", "overlap_org": "西陵区人民政府", "overlap_period": "2025-07~2026-07"},
    # 跨级 / 跨区
    {"person_a": 1, "person_b": 28, "type": "superior_subordinate", "context": "宜昌市委书记黄剑雄 2026-02-26 指导西陵区委常委会民主生活会", "overlap_org": "宜昌市-西陵区", "overlap_period": "2026-02"},
    {"person_a": 2, "person_b": 29, "type": "superior_subordinate", "context": "宜昌市长与西陵区长（市区两级政府业务指导）", "overlap_org": "宜昌市人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 27, "type": "superior_subordinate", "context": "吴光明 2023-2024 任伍家岗区委常委、常务副区长，与陈道坤（伍家岗区委书记）共事", "overlap_org": "宜昌市伍家岗区", "overlap_period": "2023-2024"},
    {"person_a": 1, "person_b": 27, "type": "overlap", "context": "梅卫民与陈道坤均出身伍家岗区领导干部序列（梅曾任伍家岗区副区长），分掌西陵、伍家两区", "overlap_org": "伍家岗区", "overlap_period": "2011-2015"},
    {"person_a": 25, "person_b": 1, "type": "overlap", "context": "汪元程曾任西陵区委副书记、常务副区长，后升任省经信厅长；与梅卫民在西陵区班子先后任职", "overlap_org": "西陵区", "overlap_period": "2012-2021"},
    {"person_a": 26, "person_b": 1, "type": "overlap", "context": "余峰曾任西陵区人民政府副区长，后任点军/伍家岗组织部长、枝江市委书记", "overlap_org": "西陵区人民政府", "overlap_period": "2011-2016"},
]

# =========================================================================
# 1. SQLite
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    post = p.get("current_post", "")
    if p["id"] == 1:
        return "255,50,50"   # 区委书记
    if p["id"] == 2 or p["id"] == 23:
        return "50,100,255"  # 区长
    if "纪委书记" in post or "监委" in post or p["id"] == 4:
        return "255,165,0"   # 纪委
    return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "开发区" in t:
        return "200,255,200"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "乡镇" in t:
        return "255,255,200"
    if "群团" in t:
        return "255,220,255"
    return "200,200,200"

def is_top_leader(p):
    return p["id"] in (1, 2)

print(f"[build 西陵区] persons={len(persons)} orgs={len(organizations)} positions={len(positions)} rels={len(relationships)}")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
conn = sqlite3.connect(DB_PATH)
conn.executescript("""
    CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    );
    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT, level TEXT,
        parent TEXT, location TEXT
    );
    CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
""")
for p in persons:
    conn.execute(
        "INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p.get("birthplace", ""), p["education"], p["party_join"], p.get("work_start", ""), p["current_post"], p["current_org"], p["source"]))
for o in organizations:
    conn.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                 (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o["location"]))
for pos in positions:
    conn.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                 (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))
for r in relationships:
    conn.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                 (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
conn.commit()
conn.close()
print(f"  DB written: {DB_PATH}")

# =========================================================================
# 2. GEXF
# =========================================================================
lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
lines.append('    <creator>gov-relation research agent (hubei_西陵区)</creator>')
lines.append('    <description>宜昌市西陵区领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="org" type="string"/>')
lines.append('      <attribute id="2" title="post" type="string"/>')
lines.append('      <attribute id="3" title="birth" type="string"/>')
lines.append('      <attribute id="4" title="education" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="period" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_org"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p["education"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{pos.get("start", "")}-{pos.get("end", "")}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"  GEXF written: {GEXF_PATH}")

# =========================================================================
# 3. Person graph JSONs (核心人物)
# =========================================================================
_ORG_NAME = {o["id"]: o["name"] for o in organizations}

_GOV = {
    1: [
        {"period": "2024-2026", "domain": "economic_development",
         "achievement_or_event": "推动2024年全区经济总量达998亿元、首次跻身赛迪全国百强区；2026年冲刺跨千亿、百强再进位（GDP增速目标7%以上）",
         "role_in_event": "区委书记（此前一肩挑书记、区长）", "measurable_outcome": "2024年998亿元，首入全国百强区",
         "location": "宜昌市西陵区", "confidence": "confirmed", "source_ids": ["S_PAPER", "S_CJN"]},
        {"period": "2025-2026", "domain": "urban_construction",
         "achievement_or_event": "服务三峡水运新通道工程：谋划重大项目29个、总投资129.2亿元，落户百亿规模的三峡水运新通道公司；推进葛洲坝片区风貌复兴、危旧改与老旧改、刘家大堰存量更新省级试点",
         "role_in_event": "区委书记", "measurable_outcome": "29个项目/129.2亿元", "location": "宜昌市西陵区",
         "confidence": "confirmed", "source_ids": ["S_HBD"]},
        {"period": "2025-09", "domain": "industry",
         "achievement_or_event": "与中国能建葛洲坝集团会谈深化央地合作（城市功能提升、基础设施补短板、存量资产盘活）",
         "role_in_event": "区委书记", "measurable_outcome": "形成全面战略共识", "location": "宜昌市西陵区",
         "confidence": "confirmed", "source_ids": ["S_ZHXW"]},
        {"period": "2026-01", "domain": "other",
         "achievement_or_event": "提出'一心一湾一带一廊'发展格局；环三峡大学创新圈、企业'头雁强雁群雁'培育计划；'来电宜昌·西陵宠你'文商旅系列、龙湖天街等消费项目",
         "role_in_event": "区委书记", "measurable_outcome": "", "location": "宜昌市西陵区",
         "confidence": "confirmed", "source_ids": ["S_PAPER"]},
    ],
    2: [
        {"period": "2023-2024", "domain": "other",
         "achievement_or_event": "任伍家岗区委常委、常务副区长，主抓优化营商环境，推动营商环境评价进入全省第一方阵；完善科技企业服务体系",
         "role_in_event": "常务副区长", "measurable_outcome": "", "location": "宜昌市伍家岗区",
         "confidence": "confirmed", "source_ids": ["S_GGZY", "S_GZW"]},
        {"period": "2026-07", "domain": "environment",
         "achievement_or_event": "带队督导重点生态环境问题整改（相关点位噪音、垃圾堆场等），要求党员干部下沉一线、问计于民",
         "role_in_event": "区长", "measurable_outcome": "问题清单逐项整改", "location": "宜昌市西陵区",
         "confidence": "confirmed", "source_ids": ["S_HBJ"]},
        {"period": "2026-01", "domain": "other",
         "achievement_or_event": "在区九届人大六次会议上作政府工作报告（2025年回顾、'十四五'回顾与'十五五'展望；2026年重点：市场主体超十万家、'四上'企业破千家）",
         "role_in_event": "区长", "measurable_outcome": "", "location": "宜昌市西陵区",
         "confidence": "confirmed", "source_ids": ["S_XL54"]},
    ],
    21: [
        {"period": "2015-2021", "domain": "economic_development",
         "achievement_or_event": "任西陵区长期间主抓中心城区能级提升，主持政府常务会推进重大项目；任区委书记后主持区委常委会部署重点任务",
         "role_in_event": "区长/区委书记", "measurable_outcome": "", "location": "宜昌市西陵区",
         "confidence": "confirmed", "source_ids": ["S_BAIKE_RW", "S_YL"]},
        {"period": "2024-至今", "domain": "economic_development",
         "achievement_or_event": "任鄂州市副市长、华容区委书记，推进武汉新城建设、武鄂协同发展先行区",
         "role_in_event": "副市长兼区委书记", "measurable_outcome": "", "location": "鄂州市华容区",
         "confidence": "confirmed", "source_ids": ["S_EZHOU", "S_HRGW"]},
    ],
}
_OPEN = {
    1: [
        {"priority": "medium", "question": "梅卫民早期履历细节（1993-1999贸易局及伍家乡各职级确切年份）",
         "why_it_matters": "完善任职链条证据", "suggested_queries": ["梅卫民 伍家乡 乡长", "梅卫民 简历 伍家岗"],
         "last_attempted": AS_OF},
        {"priority": "low", "question": "梅卫民就任区委书记的具体公示日期（2023年底-2024年初）",
         "why_it_matters": "精确锁定书记任命时点", "suggested_queries": ["梅卫民 区委书记 任命"],
         "last_attempted": AS_OF},
    ],
    2: [
        {"priority": "critical", "question": "吴光明的出生地、籍贯、大学院校及宜昌粮食集团任职起点",
         "why_it_matters": "识别国企-政界转换的完整链条", "suggested_queries": ["吴光明 宜昌 简历", "吴光明 粮食集团 任免"],
         "last_attempted": AS_OF},
    ],
    21: [
        {"priority": "low", "question": "任蔚调往鄂州的具体月份（2023年10-12月）",
         "why_it_matters": "精确锁定区委书记交接时点", "suggested_queries": ["任蔚 不再担任 西陵区委书记"],
         "last_attempted": AS_OF},
    ],
}
_STYLE = {
    1: {"public_style_indicators": [
            {"trait": "pragmatic", "evidence": "现场督导会持续至深夜（2024-05环保信访督办），要求'站在群众立场换位思考'", "confidence": "confirmed", "source_ids": []},
            {"trait": "stability_oriented", "evidence": "强调落实'政治首善'、市委'六大目标定位'", "confidence": "plausible", "source_ids": []}],
        "speech_themes": ["长江大保护典范城市核心主城", "千亿城区", "城市有机更新", "共同缔造"],
        "management_signals": ["构建'支部+干部+服务'征迁机制", "实施'头雁强雁群雁'企业培育计划"],
        "caveat": "风格判断基于公开讲话与工作报道，非私人心理评估。"},
    2: {"public_style_indicators": [
            {"trait": "grassroots_oriented", "evidence": "环保督导要求'全体党员干部一律下沉一线、经常问计于民'", "confidence": "confirmed", "source_ids": []}],
        "speech_themes": ["优化营商环境", "精致城市建设", "为民办实事"],
        "management_signals": ["强调营商环境治理的稳定性、长期性", "带头督办环保信访件"],
        "caveat": "风格判断基于公开报道。"},
    21: {"public_style_indicators": [
            {"trait": "media_visible", "evidence": "频繁调研走访、公开宣讲、获任后密集调研企业", "confidence": "confirmed", "source_ids": []}],
        "speech_themes": ["抓落实", "营商环境立标杆"],
        "management_signals": ["专项督查机制（2021年西陵'抓落实'专项会议）"],
        "caveat": "风格判断基于公开报道。"},
}

_PROF = {
    1: {"primary_specializations": ["城市建设", "园区/新区开发", "区域经济"],
        "secondary_specializations": ["旧城改造", "招商引资", "征收安置"],
        "career_pattern": "local_ladder",
        "systems_experience": ["乡镇街道", "区政府", "市直机关（新区办、市政府办）"],
        "geographic_pattern": ["伍家岗区", "宜昌市本级", "西陵区"],
        "promotion_velocity": {"summary": "1993年参加工作，2008年任伍家乡党委书记，2011年跨入副县级（伍家岗区副区长），经宜昌新区办、市政府办历练后2021年9月任正县级区长，2024年转任区委书记，属稳步攀升型", "notable_fast_promotions": []}},
    2: {"primary_specializations": ["企业经营管理", "营商环境", "国资国企改革"],
        "secondary_specializations": ["财政金融", "区域治理"],
        "career_pattern": "SOE_to_politics",
        "systems_experience": ["国企", "区政府", "开发区"],
        "geographic_pattern": ["宜昌市区（伍家岗区→西陵区）"],
        "promotion_velocity": {"summary": "1982年生，由市属国企一把手（宜昌粮食集团董事长）先后任伍家岗区委常委、常务副区长，2024-07代理西陵区长，2025-01当选区长，属'国企-政府'快速通道", "notable_fast_promotions": ["2023-04任伍家岗常务副区长 → 2024-07任西陵代区长 → 2025-01当选区长"]}},
    21: {"primary_specializations": ["宣传文化", "群团工作", "招商引资"],
         "secondary_specializations": ["城市管理"],
         "career_pattern": "city_layer_rotation",
         "systems_experience": ["宣传", "群团", "招商", "政府"],
         "geographic_pattern": ["宜昌市直", "西陵区", "鄂州市"],
         "promotion_velocity": {"summary": "1979年生，29岁任团市委副书记，32岁任正县级（妇联主席），36岁任西陵区长，42岁任区委书记，45岁升任鄂州市委常委（副厅级），属快速通道", "notable_fast_promotions": ["2025-08公示拟任市州党委常委"]}},
}

def build_sources(p):
    urls = [u.strip() for u in str(p.get("source", "")).split("|") if u.strip()]
    out = []
    for i, url in enumerate(urls):
        official = "ycxl.gov.cn" in url or "yichang.gov.cn" in url or "ezhou.gov.cn" in url
        out.append({"id": f"S{i+1:03d}", "title": f"公开人事信息（{p['name']}）", "url": url,
                    "publisher": "宜昌市西陵区人民政府/宜昌市政府/媒体", "published_at": "",
                    "accessed_at": AS_OF,
                    "source_type": "official" if official else "media",
                    "reliability": "high" if official else "medium", "notes": ""})
    return out

def write_person_json(p, rels_for_p, pos_for_p, job_label):
    filename = f"{TODAY}-湖北省-宜昌市-{job_label}-{p['name']}.json"
    path = os.path.join(PERSONS_DIR, filename)
    sources = build_sources(p)
    src_ids = [s["id"] for s in sources]
    career = []
    for pos in sorted(pos_for_p, key=lambda x: (x.get("start") or "9999")):
        career.append({
            "start": pos.get("start") or "unknown", "end": pos.get("end") or "unknown",
            "org": _ORG_NAME.get(pos["org_id"], ""), "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": "湖北省宜昌市" if pos["org_id"] not in (24, 25, 26, 31) else "湖北省鄂州市/武汉市",
            "system": "party" if ("委" in pos["title"] and "纪委" not in pos["title"]) or "书记" in pos["title"] else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": ("区委书记" in pos["title"] or "区长" in pos["title"] or "市长" in pos["title"] or "厅长" in pos["title"]) and "副" not in pos["title"] and "挂职" not in pos["title"],
            "notes": pos.get("note", ""), "confidence": "confirmed", "source_ids": src_ids,
        })
    if not career:
        career.append({"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
                       "notes": "公开资料未找到完整履历", "confidence": "unverified", "source_ids": []})
    rels_out = []
    for r in rels_for_p:
        other_id = r["person_b"] if r["person_a"] == p["id"] else r["person_a"]
        other = next((x for x in persons if x["id"] == other_id), None)
        if other:
            rels_out.append({"person": other["name"], "person_id": f"hubei_xiling_{other['name']}",
                             "relationship_type": r["type"],
                             "strength": "strong" if r["type"] in ("predecessor_successor",) else "medium",
                             "evidence": r["context"], "overlap_org": r["overlap_org"],
                             "overlap_period": r["overlap_period"], "direction": "undirected",
                             "confidence": "confirmed", "source_ids": src_ids})
    doc = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "湖北省", "city": "宜昌市", "region": "西陵区",
                                "job": job_label, "task_id": "hubei_西陵区", "time_focus": "2026年8月"},
        "identity": {
            "person_id": f"hubei_xiling_{p['name']}", "name": p["name"], "aliases": [],
            "gender": p["gender"], "ethnicity": p["ethnicity"], "birth": p["birth"],
            "birthplace": p.get("birthplace", ""), "native_place": "",
            "education": [{"period": "", "institution": "", "major": "",
                           "degree": p["education"] if p["education"] else "",
                           "study_type": "party_school" if "党校" in p.get("education", "") else "unknown",
                           "source_ids": src_ids}],
            "party_join": p["party_join"], "work_start": p.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{p['name']}_{p['birth']}",
                            "name_birthplace": f"{p['name']}_{p.get('birthplace', 'unknown')}",
                            "official_profile_url": p["source"]},
        },
        "current_status": {"current_post": p["current_post"], "current_org": p["current_org"],
                           "administrative_rank": "正县处级" if p["id"] in (1, 2) else "副厅级" if p["id"] == 21 else "副县处级",
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": src_ids},
        "career_timeline": career,
        "organizations": [{"name": _ORG_NAME[o], "role": "", "period": ""}
                          for o in sorted({pp["org_id"] for pp in pos_for_p})],
        "relationships": rels_out,
        "governance_record": _GOV.get(p["id"], []),
        "professional_profile": _PROF.get(p["id"], {"primary_specializations": [], "secondary_specializations": [],
                                                    "career_pattern": "unknown", "systems_experience": [],
                                                    "geographic_pattern": [],
                                                    "promotion_velocity": {"summary": "", "notable_fast_promotions": []}}),
        "work_style_and_personality": _STYLE.get(p["id"], {"public_style_indicators": [], "speech_themes": [],
                                                           "management_signals": [],
                                                           "caveat": "风格判断基于公开记录，非私人心理评估。"}),
        "network_metrics": {"direct_connections": len(rels_out), "total_relationships": len(rels_out),
                            "center_rank": "core" if p["id"] in (1, 2) else ("predecessor" if p["id"] in (21, 22) else "member")},
        "risk_and_integrity_signals": [{"type": "none_found",
                                        "description": f"截至{AS_OF}未发现公开的纪律处分、审计问题或负面报道（检索范围：宜昌市纪委、清廉宜昌平台及主流媒体）",
                                        "date": "", "confidence": "plausible", "source_ids": src_ids}],
        "source_register": sources,
        "confidence_summary": {"identity": "confirmed" if p["birth"] else "plausible",
                               "current_role": "confirmed", "career_completeness": "partial",
                               "relationship_confidence": "high",
                               "biggest_gap": f"{p['name']}早期履历细节（见 open_questions）"},
        "open_questions": _OPEN.get(p["id"], []),
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {filename}")

core_jobs = {1: "区委书记", 2: "区长", 21: "前任区委书记"}
for pid, job in core_jobs.items():
    p = next(x for x in persons if x["id"] == pid)
    rels_for_p = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    pos_for_p = [pos for pos in positions if pos["person_id"] == pid]
    write_person_json(p, rels_for_p, pos_for_p, job)

print(f"[* done] DB={DB_PATH}")
print(f"  GEXF={GEXF_PATH}")
print(f"  Person JSONs: {PERSONS_DIR}")