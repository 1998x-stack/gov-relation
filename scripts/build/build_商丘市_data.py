#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 商丘市 (Shangqiu City), 河南省.

Investigation date: 2026-08-06
Task ID: henan_商丘市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.shangqiu.gov.cn — 商丘市人民政府官方网站 (homepage confirmed 市长=孙起鹏, 副市长 roster, July-Aug 2026)
  - 澎湃新闻 / 新京报 / 河南日报 / 中国经济网 — 李湘豫任商丘市委书记（附简历）, 孙起鹏当选商丘市长
  - 360百科 / 百度百科 / 维基百科 — 李湘豫、孙起鹏、李若鹏、郭力铭、潘峰等人物条目
  - 河南省委组织部任前公示（河南日报 2025-11-10、2026-01-18、2026-04-13）
  - 河南省直机关党建网 / 河南老干部工作网 — 2026年商丘市委班子会议报道
  - 商丘市纪委监委官网 (lhlzw.gov.cn) — 邱建军任市纪委书记（2026-06-25）

Confidence notes:
  - 核心二人（李湘豫、孙起鹏）：身份与现任职务已确认（多重权威来源）
  - 部分常委出生年月/出生地来自百科，质量中；有任前公示者较可靠
  - 精确到月份的完整履历走向存在缺口，已标为 plausible / 缺口
  - 官方网站深层页面 403，采用新闻摘要 / 百科 / 任前公示补充
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "商丘市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
# When run from data/tmp/<task_id>/, STAGING is that directory.
# When run from repo root (e.g. as build_商丘市_data.py), STAGING is data/tmp/henan_商丘市/.
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "henan_商丘市"
if _CURRENT_DIR.name == "henan_商丘市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 core (书记/市长), 3-9 市委常委/市领导, 10-19 deputy govt, 20-29 人大/政协, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "李湘豫",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1970-07",
        "birthplace": "湖南省怀化市芷江侗族自治县",
        "education": "河南大学中文系中文专业；区域经济学博士",
        "party_join": "中共党员(1994-04)",
        "work_start": "1991-12",
        "current_post": "市委书记",
        "current_org": "中共商丘市委员会",
        "source": "https://m.thepaper.cn/newsDetail_forward_26816770",
        "confidence": "confirmed",
        "notes": "2024-03任商丘市委书记；2024-04-17任商丘军分区党委第一书记；此前任开封市长、河南省民宗委主任、援疆（哈密市委副书记）、信阳市委常委等"
    },
    {
        "id": 2,
        "name": "孙起鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-09",
        "birthplace": "河南省南阳市方城县",
        "education": "河南省委党校研究生",
        "party_join": "中共党员(1996-12)",
        "work_start": "1991-12",
        "current_post": "市长",
        "current_org": "商丘市人民政府",
        "source": "https://zh.wikipedia.org/zh-hans/%E5%AD%99%E8%B5%B7%E9%B9%8F",
        "confidence": "confirmed",
        "notes": "2025-11-27在商丘市六届人大四次会议上当选市长；此前任濮阳市委副书记、政法委书记，历次任焦作市副市长、西峡县委书记、县长"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市委领导 / 市委常委
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "李若鹏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974-12",
        "birthplace": "河南省平顶山市",
        "education": "北京大学政府管理学院博士（管理学）",
        "party_join": "中共党员(2000-06)",
        "work_start": "1996-09",
        "current_post": "市委副书记",
        "current_org": "中共商丘市委员会",
        "source": "https://baike.so.com/doc/5407057-5645015.html",
        "confidence": "confirmed",
        "notes": "2026年4月拟任省辖市委副书记，2026-05前后由市委常委、常务副市长升任；历任安阳市委常委、汤阴/滑县县委书记、共青团河南省委副书记、河南省商务厅副厅长"
    },
    {
        "id": 4,
        "name": "翁铁军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市委秘书长、宣传部部长",
        "current_org": "中共商丘市委员会",
        "source": "http://www.hnjgdj.gov.cn/2026/03-12/449546.html",
        "confidence": "confirmed",
        "notes": "兼市委直属机关工委书记；2026-03-04主持市直机关党建述职评议会"
    },
    {
        "id": 5,
        "name": "邱建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委代主任",
        "current_org": "中共商丘市纪律检查委员会",
        "source": "http://www.lhlzw.gov.cn/sitesources/sqlzw/page_pc/xxgk/ldjg/zggcdsqsjljcwyh/sj/articlef4241534a9b44a77a73d93dc203023f0.html",
        "confidence": "confirmed",
        "notes": "2026-06-25商丘市纪委监委确认任市纪委书记、市监委代主任（接任郭力铭）"
    },
    {
        "id": 6,
        "name": "毕启民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共商丘市委员会",
        "source": "http://www.hnjgdj.gov.cn/2026/03-12/449546.html",
        "confidence": "confirmed",
        "notes": "2026-03-04出席市直机关党建述职评议会；2026-02-10出席市厅级老同志情况通报会"
    },
    {
        "id": 7,
        "name": "潘峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-01",
        "birthplace": "河南省洛阳市伊川县",
        "education": "在职研究生，工商管理硕士",
        "party_join": "中共党员(1989-12)",
        "work_start": "1985-12",
        "current_post": "市委常委、政法委书记，市政府副市长",
        "current_org": "中共商丘市委员会",
        "source": "https://baike.baidu.com/item/%E6%BD%98%E5%B3%B0/19942812",
        "confidence": "confirmed",
        "notes": "曾任商丘市副市长、市委常委；分管城乡规划建设、公安政法等工作"
    },
    {
        "id": 8,
        "name": "朱洲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、商丘军分区政委",
        "current_org": "商丘军分区",
        "source": "https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E5%95%86%E4%B8%98%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A/58740447",
        "confidence": "plausible",
        "notes": "市委常委、军分区党委书记、大校政委"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市政府副市长 / 秘书长
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "袁道强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-07",
        "birthplace": "",
        "education": "在职研究生，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "商丘市人民政府",
        "source": "https://www.163.com/dy/article/ITV18VRG05563WHO.html",
        "confidence": "confirmed",
        "notes": "负责工业经济、金融等；2026-06-23出席常态化帮扶会议"
    },
    {
        "id": 10,
        "name": "黄继恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-09",
        "birthplace": "河南省开封市杞县",
        "education": "中央党校研究生",
        "party_join": "中共党员(1986-06)",
        "work_start": "1986-07",
        "current_post": "副市长、市公安局局长、党委书记",
        "current_org": "商丘市人民政府",
        "source": "https://www.163.com/dy/article/ITV18VRE05563WHO.html",
        "confidence": "confirmed",
        "notes": "市委政法委员会第一副书记；负责公安、司法、信访"
    },
    {
        "id": 11,
        "name": "高大立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-08",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "商丘市人民政府",
        "source": "https://www.163.com/dy/article/ITV18VRE05563WHO.html",
        "confidence": "confirmed",
        "notes": "负责农业农村、乡村振兴、水利；2026-06-23出席常态化帮扶会议"
    },
    {
        "id": 12,
        "name": "王爱林",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975-03",
        "birthplace": "",
        "education": "大学，工学学士",
        "party_join": "九三学社社员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "商丘市人民政府",
        "source": "https://www.163.com/dy/article/ITV18NR25563WHO.html",
        "confidence": "confirmed",
        "notes": "九三学社省委土地资源委员会主任；负责教育、文化、卫生健康"
    },
    {
        "id": 13,
        "name": "白超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "商丘市人民政府",
        "source": "https://city.dahe.cn/2023/01-20/1173250.html",
        "confidence": "plausible",
        "notes": "负责生态环境、工业经济、交通、能源、信息化建设、民营经济"
    },
    {
        "id": 14,
        "name": "李翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "商丘市人民政府",
        "source": "https://news.dahe.cn/2025/12-06/2028903.html",
        "confidence": "confirmed",
        "notes": "2025-12商丘市人大决定任命为副市长；2026-02政协六届四次会议在任"
    },
    {
        "id": 15,
        "name": "王洪民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-01",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "商丘市人民政府",
        "source": "https://www.163.com/dy/article/ITV18RU05563WHO.html",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 16,
        "name": "范建勋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "河南郑州",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "商丘市人民政府",
        "source": "https://baike.baidu.com/item/%E8%8C%83%E5%BB%BA%E5%8B%8B/19405524",
        "confidence": "plausible",
        "notes": "2024-04-18任副市长；此前郑州市工业和信息化局长、郑州市政协副主席"
    },
    {
        "id": 17,
        "name": "李进发",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "商丘市人民政府",
        "source": "https://city.dahe.cn/2023/01-20/1173250.html",
        "confidence": "plausible",
        "notes": "协助市长处理日常工作，主持市政府办公室工作"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大、政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 18,
        "name": "王少青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-02",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "商丘市人民代表大会常务委员会",
        "source": "https://www.sqrb.com.cn/content/2026-02/03/content_269156.html",
        "confidence": "confirmed",
        "notes": "2026-02商丘市六届人大五次会议当选市人大常委会主任；此前拟提名为省辖市人大常委会主任候选人"
    },
    {
        "id": 19,
        "name": "楚耀华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议商丘市委员会",
        "source": "https://www.hnzx.gov.cn/2026/03-25/4363302.html",
        "confidence": "confirmed",
        "notes": "2026-02政协六届四次会议闭幕；主持政协工作"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任领导（跨区域交接）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "摆向阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "",
        "education": "在职研究生，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "商丘市人民政府",
        "source": "https://news.qq.com/rain/a/20251127A06AW700",
        "confidence": "confirmed",
        "notes": "前任商丘市委副书记、市长；2025-11调任河南省民族宗教事务委员会党组书记、兼任省委统战部副部长"
    },
    {
        "id": 31,
        "name": "李国胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-01",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共商丘市委员会",
        "source": "https://news.qq.com/rain/a/20240324A01HQ00",
        "confidence": "confirmed",
        "notes": "曾任黄淮学院党委书记；2021-2024任商丘市委书记；2024-03不再担任，去向待查"
    },
    {
        "id": 32,
        "name": "王玉娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-01",
        "birthplace": "",
        "education": "大学，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委副书记",
        "current_org": "中共商丘市委员会",
        "source": "https://dzb.henandaily.cn/html5/2025-10/20/content_11_1762313.htm",
        "confidence": "confirmed",
        "notes": "前任市委副书记、统战部长；2025-11调任河南省委网信办主任"
    },
    {
        "id": 33,
        "name": "郭力铭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-06",
        "birthplace": "河南省新乡市延津县",
        "education": "大学，法学学士",
        "party_join": "中共党员",
        "work_start": "1988-01",
        "current_post": "前任市纪委书记",
        "current_org": "中共商丘市纪律检查委员会",
        "source": "https://baike.so.com/doc/9663600-10009650.html",
        "confidence": "confirmed",
        "notes": "原商丘市委常委、市纪委书记、市监委主任；2026-01拟提名为省辖市人大常委会主任候选人（继任邱建军）"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共商丘市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委员会", "location": "商丘市"},
    {"id": 2, "name": "商丘市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "商丘市"},
    {"id": 3, "name": "商丘市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "河南省人大常委会", "location": "商丘市"},
    {"id": 4, "name": "中国人民政治协商会议商丘市委员会", "type": "政协", "level": "地级市", "parent": "政协河南省委员会", "location": "商丘市"},
    {"id": 5, "name": "中共商丘市纪律检查委员会（商丘市监察委员会）", "type": "纪委", "level": "地级市", "parent": "河南省纪委监委", "location": "商丘市"},
    {"id": 6, "name": "商丘军分区", "type": "军队", "level": "军分区", "parent": "河南省军区", "location": "商丘市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 李湘豫 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2024-03", "end_date": "", "rank": "正厅级", "note": "兼任商丘军分区党委第一书记"},
    # 孙起鹏 — current Mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2025-11", "end_date": "", "rank": "正厅级", "note": "2025-11-27当选"},
    # 李若鹏 — Deputy Party Secretary (ex-常务副市长)
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "2026-05", "end_date": "", "rank": "副厅级", "note": "此前任市委常委、副市长"},
    {"person_id": 3, "org_id": 2, "title": "副市长（常务）", "start_date": "2024-04", "end_date": "2026-05", "rank": "副厅级", "note": "后升任市委副书记"},
    # 翁铁军
    {"person_id": 4, "org_id": 1, "title": "市委常委、市委秘书长、宣传部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼市委直属机关工委书记"},
    # 邱建军
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "市纪委书记、市监委代主任", "start_date": "2026-06", "end_date": "", "rank": "副厅级", "note": ""},
    # 毕启民
    {"person_id": 6, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 潘峰
    {"person_id": 7, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "负责城乡规划、公安政法"},
    # 朱洲
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "军分区政委（大校）", "start_date": "", "end_date": "", "rank": "副师级", "note": ""},
    # 袁道强
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 黄继恒
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼市公安局局长"},
    # 高大立
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 王爱林
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "九三学社社员"},
    # 白超
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 李翔
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "2025-12", "end_date": "", "rank": "副厅级", "note": ""},
    # 王洪民
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 范建勋
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "2024-04", "end_date": "", "rank": "副厅级", "note": ""},
    # 李进发
    {"person_id": 17, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 王少青
    {"person_id": 18, "org_id": 3, "title": "市人大常委会主任", "start_date": "2026-02", "end_date": "", "rank": "正厅级", "note": ""},
    # 楚耀华
    {"person_id": 19, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 前任领导 (30+)
    {"person_id": 30, "org_id": 2, "title": "市长", "start_date": "2023", "end_date": "2025-11", "rank": "正厅级", "note": "前任市长，已调任省民宗委"},
    {"person_id": 31, "org_id": 1, "title": "市委书记", "start_date": "2021", "end_date": "2024-03", "rank": "正厅级", "note": "前任市委书记"},
    {"person_id": 32, "org_id": 1, "title": "市委副书记、统战部部长", "start_date": "2023", "end_date": "2025-11", "rank": "副厅级", "note": "前任副书记，已调任省委网信办"},
    {"person_id": 33, "org_id": 5, "title": "市纪委书记、市监委主任", "start_date": "2023-01", "end_date": "2026", "rank": "副厅级", "note": "前任市纪委书记"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 李湘豫 ↔ 孙起鹏（市委书记—市长）
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共商丘市委员会", "overlap_period": "2025-11至今"},
    # 李湘豫 ↔ 李若鹏（书记—副书记）
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共商丘市委员会", "overlap_period": "2026"},
    # 李湘豫 ↔ 各常委（书记—常委）
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—秘书长/宣传部长", "overlap_org": "中共商丘市委员会", "overlap_period": "2024-至今"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共商丘市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—组织部长", "overlap_org": "中共商丘市委员会", "overlap_period": "2024-至今"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—政法书记", "overlap_org": "中共商丘市委员会", "overlap_period": "2024-至今"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—军分区政委", "overlap_org": "商丘军分区", "overlap_period": "2024-至今"},
    # 孙贵鹏 ↔ 市长—副市长/秘书长
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—常务副市长（李若鹏）", "overlap_org": "商丘市人民政府", "overlap_period": "2025-11—2026-05"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "市长—副市长", "overlap_org": "商丘市人民政府", "overlap_period": "2025-11-至今"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—副市长（公安局长）", "overlap_org": "商丘市人民政府", "overlap_period": "2025-11-至今"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "市长—副市长", "overlap_org": "商丘市人民政府", "overlap_period": "2025-11-至今"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "市长—副市长", "overlap_org": "商丘市人民政府", "overlap_period": "2025-11-至今"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "市长—副市长", "overlap_org": "商丘市人民政府", "overlap_period": "2025-11-至今"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "市长—副市长", "overlap_org": "商丘市人民政府", "overlap_period": "2025-12-至今"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "市长—副市长", "overlap_org": "商丘市人民政府", "overlap_period": "2025-11-至今"},
    {"person_a": 2, "person_b": 16, "type": "共事", "context": "市长—副市长", "overlap_org": "商丘市人民政府", "overlap_period": "2025-11-至今"},
    {"person_a": 2, "person_b": 17, "type": "共事", "context": "市长—秘书长", "overlap_org": "商丘市人民政府", "overlap_period": "2025-11-至今"},
    # 常委内部同僚
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共商丘市委员会", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共商丘市委员会", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共商丘市委员会", "overlap_period": "2026"},
    {"person_a": 7, "person_b": 4, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共商丘市委员会", "overlap_period": "2026"},
    # 前任交接
    {"person_a": 31, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记", "overlap_org": "中共商丘市委员会", "overlap_period": "2024-03"},
    {"person_a": 30, "person_b": 2, "type": "交接", "context": "前任市长—现任市长", "overlap_org": "商丘市人民政府", "overlap_period": "2025-11"},
    {"person_a": 32, "person_b": 3, "type": "交接", "context": "前任副书记—现任副书记", "overlap_org": "中共商丘市委员会", "overlap_period": "2025-11—2026-05"},
    {"person_a": 33, "person_b": 5, "type": "交接", "context": "前任纪委书记—现任纪委书记", "overlap_org": "中共商丘市纪律检查委员会", "overlap_period": "2026"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person.get("birth"):
        questions.append("出生年月未确认")
    if not person.get("birthplace"):
        questions.append("籍贯未确认")
    if not person.get("ethnicity"):
        questions.append("民族未确认")
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    if not person.get("notes", ""):
        questions.append("完整任职履历未确认")
    return questions


def _render_relationship(p: dict, rel: dict, persons: list[dict], pid: int) -> dict:
    """Return a relationship dict for the person JSON registry."""
    other_id = rel["person_b"] if rel["person_a"] == pid else rel["person_a"]
    other = next((x for x in persons if x["id"] == other_id), None)
    other_name = other["name"] if other else f"person_{other_id}"
    return {
        "person": other_name,
        "person_id": f"shangqiu_{other_name}",
        "relationship_type": "overlap",
        "strength": "strong" if rel["type"] == "共事" else "medium",
        "evidence": rel.get("context", ""),
        "overlap_org": rel.get("overlap_org", ""),
        "overlap_period": rel.get("overlap_period", ""),
        "direction": "undirected",
        "confidence": "confirmed",
        "source_ids": ["S001"],
    }


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"shangqiu_{name}"

    person_positions = [p for p in positions if p["person_id"] == pid]
    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Enrich with known external career segments from research (plausible, media)
    known_rows = {
        "李湘豫": [
            ("1991", "", "河南大学中文系毕业，留校工作", "", "1991-12参加工作"),
            ("1991", "2008", "河南省新乡市，跨县级干部（副县长→常委副县长→县长）", "获嘉县、长垣县", "早期履历"),
            ("2008", "2011", "河南省民族事务委员会（省宗教局）党组成员、副主任（副局长）", "", "2008年，早期在省民宗系统"),
            ("2011", "2016", "信阳市委常委（组织部部长、副市长）", "信阳", "2011年调任信阳"),
            ("2016", "2020", "第九批河南省援疆工作前方指挥部党委书记、总指挥，哈密市委副书记", "哈密", "2016年援疆"),
            ("2020-01", "2020-12", "河南省民族宗教事务委员会党组书记、主任（兼省委统战部副部长）", "", "2020年回省民宗委"),
            ("2020-12", "2024-01", "开封市委副书记、市长", "开封", "2020-12代市长，2021-02当选市长"),
            ("2024-03", "至今", "中共商丘市委书记", "商丘", "2024-03任书记，2024-04兼军分区党委第一书记"),
        ],
        "孙起鹏": [
            ("1991-12", "2014-04", "南阳市基层工作（约30年：县级、市直）", "南阳", "早年长期在南阳工作"),
            ("2014-04", "2016-02", "南阳市西峡县县长", "西峡", "2014-04任县长"),
            ("2016-02", "2018-09", "南阳市西峡县委书记", "西峡", "2016-02任书记"),
            ("2018-09", "2021-10", "焦作市人民政府副市长", "焦作", "2018-09任副市长"),
            ("2021-10", "2022-10", "濮阳市委常委、政法委书记", "濮阳", "2021-10任政法委书记"),
            ("2022-10", "2023-10", "濮阳市委常委、组织部部长", "濮阳", "2022-10任组织部长"),
            ("2023-10", "2025-11", "濮阳市委副书记、政法委书记", "濮阳", "2023-10任副书记，兼政法委书记"),
            ("2025-11", "至今", "商丘市委副书记、市长", "商丘", "2025-11-27当选"),
        ],
        "李若鹏": [
            ("1998", "2004", "北京大学政府管理学院硕博连读（管理博士）", "北京", "其间任北京大学研究生会主席、全国学联执行主席"),
            ("2004", "2007", "安阳县副县长", "安阳", "县长"),
            ("2007", "2009", "安阳市外事侨务办主任、党组书记", "安阳", ""),
            ("2009", "2011", "汤县委书记", "汤阴", "2011-08任安阳市委常委"),
            ("2011-09", "2013-05", "安阳市委常委、滑县县委书记", "滑县", ""),
            ("2013-05", "2016-09", "共青团河南省委副书记、党组副书记（主持工作）", "郑州", ""),
            ("2016-09", "2024-04", "河南省商务厅党组成员、副厅长", "郑州", ""),
            ("2024-04", "2026-05", "商丘市委常委、副市长", "商丘", "2024-04任副市长"),
            ("2026-05", "至今", "商丘市委副书记", "商丘", "2026-05前后升任"),
        ],
        "潘峰": [
            ("1985-12", "2019", "基层任职（河南伊川人）", "洛阳", ""),
            ("2020", "至今", "商丘市副市长、市委常委（分管城建）", "商丘", ""),
        ],
        "郭力铭": [
            ("1988-01", "2022", "纪检系统任职（河南延津人）", "新乡/河南", ""),
            ("2022-12", "2026", "商丘市委常委、市纪委书记、市监委主任", "商丘", "2023-01正式任职"),
        ],
    }
    if name in known_rows:
        for seg in known_rows[name]:
            career_timeline.append({
                "start": seg[0] or "unknown",
                "end": "present" if seg[1] in ("至今", "present") else (seg[1] or "unknown"),
                "org": seg[2],
                "title": seg[2],
                "level": "",
                "rank": "",
                "notes": seg[3] or "",
                "confidence": "plausible",
                "source_ids": ["S002"],
            })
    else:
        if len(career_timeline) <= 1 and not person.get("birth"):
            career_timeline.append({
                "start": "unknown", "end": "unknown",
                "org": "履历缺口", "title": "",
                "notes": "公开资料不足，完整履历待查。",
                "confidence": "unverified", "source_ids": [],
            })

    # Relationships
    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = [_render_relationship(person, r, persons, pid) for r in person_rels]

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "商丘市人民政府官方网站 / 大河网 / 澎湃新闻",
            "url": source_url,
            "publisher": "商丘市人民政府 / 媒体",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年商丘市政府官网首页领导信息及媒体任前 / 任命报道",
        }
    ]
    if name in known_rows:
        sources.append({
            "id": "S002",
            "title": "媒体 / 百科履历",
            "url": source_url,
            "publisher": "澎湃新闻 / 新京报 / 知乎百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "medium",
            "notes": "李湘豫、孙起鹏、李若鹏等公开履历（多源交叉）",
        })

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "商丘市",
            "region": "商丘市",
            "job": person.get("current_post", ""),
            "task_id": "henan_商丘市",
            "time_focus": "2026年8月",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": name,
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions; not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "good" if name in known_rows else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "普通市委常委出生/籍贯未核实；完整履历时间精确度中等地",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月/籍贯（部分常委未核实）",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整逐段任职履历（起止时间精确到月）",
                "why_it_matters": "关系网络分析需要精确时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-河南省-商丘市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════

def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print("  Writing person JSONs...")
    core_ids = {1, 2, 3, 30, 31, 32, 33}  # Core leaders + predecessors + key deputies
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return None


if __name__ == "__main__":
    main()