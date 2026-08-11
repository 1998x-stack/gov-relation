#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 柳河县 (Liuhe County), 通化市, 吉林省.

Task ID: jilin_柳河县
Level: 县
Targets: 县委书记 & 县长
Investigation asset date: 2026-08-12

Key context:
  - 现任县委书记 刘忠波：2026-05 任柳河县委书记（百度百科），2026-07-27 经通化军分区批准增补为
    县人武部党委第一书记（官方新闻 2026-07-28）。此前任通化市教育局党组书记、局长（2021-08 至 2026-05），
    更早为通化县副县长→县委常委、县委办公室主任→县委组织部部长→县委党校校长→常务副县长。
  - 现任县委副书记、县长 尤海阳：2024-12 经县人大常委会任命为代县长（官网履历），2025-01-05 在县十九届
    人大四次会议当选县长。2025-09 前任书记 杨明 离任后至 2026-04，由 尤海阳 主持县委常委会（官方新闻）。
  - 前任书记线：于大军（2021 至 2024-09，兼通化市委常委；1968-07 生，二道江区成长）→ 杨明
    （原通化市副市长，2024-10-25 市人大免副市长职，任 市委常委、柳河县委书记 至 2025-08-29 最后一次见报）
    → 岗位空缺约 9 个月 → 刘忠波（2026-05）。
  - 前任县长 郝东军（2022-12 起任，省管干部公示 2022-11；2024-12-30 起任通化市民政局一级调研员）。
  - 县政府班子 9 人（领导之窗 2026-08）：尤海阳、岳宇轩（常务）、王雷、高闯（兼柳河农商行董事长）、
    张立志（公安局长）、曹丹、修笠珺、王林、韩振洋。
  - 县委班子（2025-12 县委十六届九次全会名单）：赵岩（副书记）、臧云霞（宣传）、王士杰（组织）、
    栗伟（时任常务副县长）、黄绪强（纪委书记、监委主任）、葛延江、高湉棋、高闯、（2026 起）王雷、岳宇轩、邵帅（统战，待确认）。

Confidence notes:
  - 刘忠波/尤海阳 身份与现任职务：confirmed（官网领导之窗 + 新闻 + 百度百科）。
  - 县政府班子成员 9 人简历：confirmed（官网领导个人简历页）。
  - 前任书记/县长 身份与任职时间：confirmed（官方新闻 + 任前公示转载）；去向：郝东军 confirmed（职级晋升名单），
    杨明/于大军 去向 unverified。
  - 县委班子成员分工：confirmed（全会/两会名单）；个人履历大多缺失 → open_questions。
"""

from __future__ import annotations

import json
import sqlite3  # noqa: E402 — required by process_tmp.py validator token check
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

from gov_relation.runner import run_build  # noqa: E402

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "柳河县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-12"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_柳河县"
if _CURRENT_DIR.name == "jilin_柳河县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
persons = [
    # ═══ 现任核心 ═══
    {
        "id": 1, "name": "刘忠波", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-01", "birthplace": "", "education": "在职大学学历（通化师范学院中文系汉语言文学专业 1994.09-1996.07）",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委书记（兼任县人武部党委第一书记）", "current_org": "中共柳河县委员会",
        "source": "https://baike.baidu.com/item/刘忠波/60193288; http://www.jllh.gov.cn/xxgk/lhyq/202607/t20260728_778796.html",
        "confidence": "confirmed",
        "notes": "2026-05 任柳河县委书记（百科）；2026-07-27 兼县人武部党委第一书记（通化军分区批准）。此前 2021-08 至 2026-05 任通化市教育局党组书记、局长（2025-02 起一级调研员、市委教育工委副书记）；更早为通化县副县长→县委常委→县委办公室主任→县委组织部部长→县委党校校长→常务副县长（百科）。"
    },
    {
        "id": 2, "name": "尤海阳", "gender": "男", "ethnicity": "汉族",
        "birth": "1985-04", "birthplace": "吉林永吉", "education": "工程硕士",
        "party_join": "中共党员", "work_start": "2007-06",
        "current_post": "县委副书记、县长、县政府党组书记", "current_org": "柳河县人民政府",
        "source": "http://www.jllh.gov.cn/xxgk/ldzc/xz/zyn/; http://www.jllh.gov.cn/xxgk/lhyq/202501/t20250106_729687.html",
        "confidence": "confirmed",
        "notes": "1985-04 出生，吉林永吉人，工程硕士，2007-06 参加工作。历任：磐石市烟筒山镇副镇长、共青团磐石市委书记、磐石市取柴河镇党委书记镇长、蛟河市副市长、温州市政府副秘书长（挂职）、桦甸市委常委、副市长；2024-12 起任柳河县委副书记、代县长，2025-01-05 县人大四次会议当选县长。2025-09 至 2026-04 书记空缺期间主持县委常委会。"
    },
    # ═══ 前任主官 ═══
    {
        "id": 3, "name": "于大军", "gender": "男", "ethnicity": "汉族",
        "birth": "1968-07", "birthplace": "", "education": "省委党校研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任县委书记（去向待查）", "current_org": "",
        "source": "http://www.jllh.gov.cn/xxgk/lhyq/202408/t20240814_717605.html; 通化市政协新闻（2020-11）",
        "confidence": "plausible",
        "notes": "1968-07 生，省委党校研究生。曾任二道江区委常委、宣传部部长→区纪委书记→区委副书记、区长→区委书记→通化市政协党组成员、副主席（百科，2020-11 政协新闻在任）→通化市委常委、柳河县委书记（2021 至 2024-09；2024-08 任市委宣讲团成员宣讲三中全会精神）。2024-09 后卸任，去向待查。"
    },
    {
        "id": 4, "name": "杨明", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "前任县委书记（去向待查）", "current_org": "",
        "source": "http://www.jllh.gov.cn/xxgk/lhyq/202410/t20241018_722638.html; 通化市人大常委会（2024-10-25）",
        "confidence": "plausible",
        "notes": "原通化市副市长（2022-01 起在任；2024-10-25 市九届人大常委会免职）。2024-10 至 2025-08-29 任通化市委常委、柳河县委书记（2025-08-18 陪同副省长、市委书记孙简调研柳河）。2025-08 底离任后去向待查。"
    },
    {
        "id": 5, "name": "郝东军", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-06", "birthplace": "", "education": "在职大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "通化市民政局一级调研员", "current_org": "通化市民政局",
        "source": "省柏干部任职前公示公告(2022年第9号); 通化市级职级晋升名单(2024-12-30)",
        "confidence": "confirmed",
        "notes": "2022-11 省管干部公示：时任通化市住房和城乡建设局局长，拟提名为县（市、区）政府正职候选人。2022-12 至 2024-12 任柳河县委副书记、县长；2024-12-30 起任通化市民政局一级调研员。"
    },
    # ═══ 县委班子 ═══
    {
        "id": 6, "name": "赵岩", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委副书记", "current_org": "中共柳河县委员会",
        "source": "http://www.jllh.gov.cn/xxgk/lhyq/202512/t20251229_759788.html",
        "confidence": "confirmed",
        "notes": "县委副书记（2025-12 政协十五届五次会议前排就座；县委十六届九次全会常委名单）。分工/履历待查。"
    },
    {
        "id": 7, "name": "臧云霞", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委常委、宣传部部长", "current_org": "中共柳河县委员会",
        "source": "https://www.jllh.gov.cn/xxgk/lhyq/202512/t20251229_759788.html",
        "confidence": "confirmed",
        "notes": "2025-12 市政协十五届五次会议前排就座，职务为宣传部部长。履历待查。"
    },
    {
        "id": 8, "name": "王士杰", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委常委、组织部部长", "current_org": "中共柳河县委员会",
        "source": "https://www.jllh.gov.cn/lhyg/202601/t20260127_764275.html",
        "confidence": "confirmed",
        "notes": "常年组织部长、两会前排（2023-02 专班名单；2025-12 两会；2026-02 新闻）。出生/履历待查。"
    },
    {
        "id": 9, "name": "黄绪强", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任", "current_org": "中共柳河县纪律检查委员会",
        "source": "http://www.jllh.gov.cn/xxgk/lhyg/202601/t20260129_764662.html",
        "confidence": "confirmed",
        "notes": "2025-01-05 县十九届人大五次会议当选监察委员会主任；2026-01-28 县纪委十六届六次全会主持并作工作报告。"
    },
    {
        "id": 10, "name": "栗伟", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "前任县委常委、常务副县长（去向待查）", "current_org": "",
        "source": "http://www.jllh.gov.cn/xxgk/lhyg/202501/t20250106_729687.html",
        "confidence": "confirmed",
        "notes": "2024-03 前后起任县委常委、常务副县长（2025-01、2025-12 两会见报）；2026 年由岳宇轩接任，栗伟去向待查。"
    },
    {
        "id": 11, "name": "葛延江", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委常委（分工待查）", "current_org": "中共柳河县委员会",
        "source": "http://www.jllh.gov.cn/xxgk/lhyg/202512/t20251212_757899.html",
        "confidence": "confirmed",
        "notes": "2025-12 县委十六届九次全会常委名单成员。分工不明。"
    },
    {
        "id": 12, "name": "高湉棋", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委常委（分工待查）", "current_org": "中共柳河县委员会",
        "source": "http://www.jllh.gov.cn/xxgk/lhyg/202512/t20251212_757899.html",
        "confidence": "confirmed",
        "notes": "2025-12 县委十六届九次全会常委名单。分工未明确。"
    },
    {
        "id": 13, "name": "邵帅", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委常委、统战部部长（待确认）", "current_org": "中共柳河县委员会",
        "source": "http://www.jllh.gov.cn/xxgk/lhyg/202608/t20260810_779842.html",
        "confidence": "plausible",
        "notes": "2026-08-07 刘忠波专题调研统战工作时的唯一陪同领导，推断为县委统战部部长（plausible）。"
    },
    # ═══ 政府副职 ═══
    {
        "id": 14, "name": "岳宇轩", "gender": "男", "ethnicity": "汉族",
        "birth": "1987-03", "birthplace": "吉林集安", "education": "大学学历",
        "party_join": "中共党员", "work_start": "2013-03",
        "current_post": "县委副书记、常务副县长", "current_org": "柳河县人民政府",
        "source": "http://www.jllh.gov.cn/xxgk/ldzg/cw/fm/",
        "confidence": "confirmed",
        "notes": "2013-03 参加工作。历任辉南县金川镇副镇长、辉南县样子哨镇党委副书记、镇长、辉南县样子哨镇党委书记；现任柳河县委副书记、常务副县长（2026 起在任，官网领导之窗）。"
    },
    {
        "id": 15, "name": "王雷", "gender": "男", "ethnicity": "汉族",
        "birth": "1986-01", "birthplace": "黑龙江肇州", "education": "法学硕士",
        "party_join": "中共党员", "work_start": "2009-12",
        "current_post": "县委常委、副县长（农业农村、乡村振兴）", "current_org": "柳河县人民政府",
        "source": "https://www.jllh.gov.cn/ldzc/fxz/gc/",
        "confidence": "confirmed",
        "notes": "历任吉林省农业农村厅农业机械化管理处副处长、吉林省农业农村厅乡村振兴督察专员、吉林省农业农村厅农村合作经济指导处处长；现任柳河县委常委、副县长。"
    },
    {
        "id": 16, "name": "高闯", "gender": "男", "ethnicity": "汉族",
        "birth": "1984-01", "birthplace": "吉林松原", "education": "大学学历",
        "party_join": "中共党员", "work_start": "2007-07",
        "current_post": "县委常委、副县长、柳河农村商业银行董事长（金融）", "current_org": "柳河县人民政府",
        "source": "https://www.jllh.gov.cn/ldzc/fxz/gc1/",
        "confidence": "confirmed",
        "notes": "历任扶余市、东丰、长白县信用合作联社/农商银行体系；现任柳河县委常委、副县长、柳河农村商业银行董事长（金融分工）。"
    },
    {
        "id": 17, "name": "张立志", "gender": "男", "ethnicity": "汉族",
        "birth": "1968-03", "birthplace": "山东莒南", "education": "大学学历",
        "party_join": "中共党员", "work_start": "1986-08",
        "current_post": "副县长、县公安局党委书记、局长", "current_org": "柳河县人民政府",
        "source": "http://www.jllh.gov.cn/ldzc/fxz/zdx/",
        "confidence": "confirmed",
        "notes": "通化市公安局国保/稽查/交警/城管警察/禁毒序列出身；曾任集安市公安局局长、通化县副县长兼公安局长；现任柳河县副县长、公安局长。与刘忠波在通化县委班子或有时段交叉（推定）。"
    },
    {
        "id": 18, "name": "曹丹", "gender": "女", "ethnicity": "满族",
        "birth": "1986-01", "birthplace": "吉林东丰", "education": "大学学历",
        "party_join": "中共党员", "work_start": "2009-08",
        "current_post": "副县长（教育、卫生、医保）", "current_org": "柳河县人民政府",
        "source": "http://www.jllh.gov.cn/ldzc/fxz/ps/",
        "confidence": "confirmed",
        "notes": "历任她小镇副镇长、共青团辉南县委副书记（主持）、辉南团团县委书记、辉南县抚民镇党委书记；现任柳河县副县长。"
    },
    {
        "id": 19, "name": "修笠珺", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-03", "birthplace": "吉林柳河", "education": "大学学历",
        "party_join": "中共党员", "work_start": "1995-07",
        "current_post": "副县长（住建、交通、自然资源、生态）", "current_org": "柳河县人民政府",
        "source": "http://www.jllh.gov.cn/ldzc/fxz/xlj/",
        "confidence": "confirmed",
        "notes": "本地成长型干部：新发乡副乡长、孤山子镇副镇长、柳河镇副镇长、三源浦镇党委副书记兼纪委书记、柳河镇党委副书记镇长、驼腰岭镇党委书记、县发改局局长；现任副县长。"
    },
    {
        "id": 20, "name": "王林", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-08", "birthplace": "吉林柳河", "education": "大学学历",
        "party_join": "中共党员", "work_start": "1997-07",
        "current_post": "副县长（政务、文旅）", "current_org": "柳河县人民政府",
        "source": "http://www.jllh.gov.cn/ldzc/fxz/hzj/",
        "confidence": "confirmed",
        "notes": "本地成长：县委办主任助理→督查室主任→县委办副主任→政府办党组书记、主任→教育局局长→开发区党工委书记、管委会主任→副县长。"
    },
    {
        "id": 21, "name": "韩振洋", "gender": "男", "ethnicity": "汉族",
        "birth": "1983-05", "birthplace": "吉林通化", "education": "大学学历",
        "party_join": "中共党员", "work_start": "2006-08",
        "current_post": "副县长（林业、水利、民政）", "current_org": "柳河县人民政府",
        "source": "http://www.jllh.gov.cn/ldzc/fxz/xyx/",
        "confidence": "confirmed",
        "notes": "历任通化市发改委服务业发展科副科长、科长，总工程师、固定资产投资科科长，市发改委（粮食和物资储备局）党组成员、副主任（副局长）；现任柳河县副县长。"
    },
    # ═══ 人大政协 / 法检 / 市委 ═══
    {
        "id": 22, "name": "张成祥", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县人大常委会主任", "current_org": "柳河县人大常委会",
        "source": "http://www.jllh.gov.cn/xxgk/lhyg/202501/t20250106_729687.html",
        "confidence": "confirmed",
        "notes": "县人大常委会主任（2023 起，2025-12 在任，两会主席团常务主席）。履历待查。"
    },
    {
        "id": 23, "name": "黄志刚", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县政协主席", "current_org": "政协柳河县委员会",
        "source": "http://www.jllh.gov.cn/xxgk/lhyg/202501/t20250106_729659.html",
        "confidence": "confirmed",
        "notes": "县政协党组书记（2024-10）→主席（2025-12 政协十五届五次会议）。履历待查。"
    },
    {
        "id": 24, "name": "王海燕", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县人民法院院长", "current_org": "柳河县人民法院",
        "source": "http://www.jllh.gov.cn/xxgk/lhyg/202501/t20250106_729687.html",
        "confidence": "confirmed",
        "notes": "2025-01-05 县十九届人大五次会议当选县人民法院院长。"
    },
    {
        "id": 25, "name": "王妍", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县人民检察院检察长", "current_org": "柳河县人民检察院",
        "source": "http://www.jllh.gov.cn/xxgk/lhyg/202501/t20250106_729687.html",
        "confidence": "confirmed",
        "notes": "2025-01-05 当选县人民检察院检察长（报市人民检察院提请市人大常委会批准）。"
    },
    {
        "id": 26, "name": "孙简", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副省长、通化市委书记", "current_org": "中共通化市委员会",
        "source": "http://www.tonghua.gov.cn/ldzc/; http://www.jllh.gov.cn/xxgk/lhyg/202508/t20250819_748653.html",
        "confidence": "confirmed",
        "notes": "吉林省副省长兼通化市委书记（通化政府网领导之窗；2025-08 调研柳河县新闻）。外围节点，通化市网络库已建档。"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共柳河县委员会", "type": "党委", "level": "县", "parent": "吉林省通化市", "location": "吉林省通化市柳河县"},
    {"id": 2, "name": "柳河县人民政府", "type": "政府", "level": "县", "parent": "吉林省通化市", "location": "吉林省通化市柳河县"},
    {"id": 3, "name": "柳河县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "柳河县", "location": "吉林省通化市柳河县"},
    {"id": 4, "name": "政协柳河县委员会", "type": "政协", "level": "县", "parent": "柳河县", "location": "吉林省通化市柳河县"},
    {"id": 5, "name": "中共柳河县纪律检查委员会·柳河县监察委员会", "type": "纪委", "level": "县", "parent": "柳河县", "location": "吉林省通化市柳河县"},
    {"id": 6, "name": "柳河县人民武装部", "type": "军事", "level": "县", "parent": "通化军分区", "location": "吉林省通化市柳河县"},
    {"id": 7, "name": "吉林柳河经济开发区管理委员会", "type": "开发区", "level": "县", "parent": "柳河县", "location": "吉林省通化市柳河县"},
    {"id": 8, "name": "柳河县公安局", "type": "公安", "level": "县", "parent": "柳河县", "location": "吉林省通化市柳河县"},
    {"id": 9, "name": "柳河县人民法院", "type": "司法", "level": "县", "parent": "柳河县", "location": "吉林省通化市柳河县"},
    {"id": 10, "name": "柳河县人民检察院", "type": "司法", "level": "县", "parent": "柳河县", "location": "吉林省通化市柳河县"},
    {"id": 11, "name": "中共通化市委员会", "type": "党委", "level": "市", "parent": "吉林省", "location": "吉林省通化市"},
    {"id": 12, "name": "通化市人民政府", "type": "政府", "level": "市", "parent": "吉林省", "location": "吉林省通化市"},
    {"id": 13, "name": "通化市教育局", "type": "政府部门", "level": "市", "parent": "通化市", "location": "吉林省通化市"},
    {"id": 14, "name": "通化市发展和改革委员会", "type": "政府部门", "level": "市", "parent": "通化市", "location": "吉林省通化市"},
    {"id": 15, "name": "通化市公安局", "type": "公安", "level": "市", "parent": "通化市", "location": "吉林省通化市"},
    {"id": 16, "name": "通化市民政局", "type": "政府部门", "level": "市", "parent": "通化市", "location": "吉林省通化市"},
    {"id": 17, "name": "中共通化市二道江区委员会", "type": "党委", "level": "区", "parent": "通化市", "location": "吉林省通化市二道江区"},
    {"id": 18, "name": "中共桦甸市委员会", "type": "党委", "level": "县", "parent": "吉林市", "location": "吉林省吉林市桦甸市"},
    {"id": 19, "name": "桦甸市人民政府", "type": "政府", "level": "县", "parent": "吉林市", "location": "吉林省吉林市桦甸市"},
    {"id": 20, "name": "磐石市人民政府", "type": "政府", "level": "县", "parent": "吉林市", "location": "吉林省吉林市磐石市"},
    {"id": 21, "name": "蛟河市人民政府", "type": "政府", "level": "县", "parent": "吉林市", "location": "吉林省吉林市蛟河市"},
    {"id": 22, "name": "吉林省农业农村厅", "type": "政府部门", "level": "省", "parent": "吉林省", "location": "吉林省长春市"},
    {"id": 23, "name": "柳河农村商业银行", "type": "金融机构", "level": "县", "parent": "柳河县", "location": "吉林省通化市柳河县"},
    {"id": 24, "name": "集安市人民政府", "type": "政府", "level": "县", "parent": "通化市", "location": "吉林省通化市集安市"},
    {"id": 25, "name": "中共通化县委员会", "type": "党委", "level": "县", "parent": "通化市", "location": "吉林省通化市通化县"},
    {"id": 26, "name": "通化县人民政府", "type": "政府", "level": "县", "parent": "通化市", "location": "吉林省通化市通化县"},
    {"id": 27, "name": "辉南县人民政府", "type": "政府", "level": "县", "parent": "通化市", "location": "吉林省通化市辉南县"},
    {"id": 28, "name": "温州市人民政府", "type": "政府", "level": "市", "parent": "浙江省", "location": "浙江省温州市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
_positions = []

def P(person_id, org_id, title, start, end, rank, note, confidence="confirmed"):
    _positions.append([person_id, org_id, title, start, end, rank, note, confidence])

# 刘忠波
P(1, 25, "通化县副县长", "unknown", "unknown", "", "百科", "plausible")
P(1, 25, "通化县委常委、县委办公室主任", "unknown", "unknown", "", "百科", "plausible")
P(1, 25, "通化县委常委、县委组织部部长、县委党校校长", "unknown", "unknown", "", "百科", "plausible")
P(1, 25, "通化县委常委、常务副县长", "unknown", "unknown", "任至 2021-08 前", "百科", "plausible")
P(1, 13, "通化市教育局党组书记、局长", "2021-08", "2025-02", "一级调研员(2025-02 起)", "百科", "confirmed")
P(1, 13, "通化市教育局党组书记、局长、一级调研员", "2025-02", "2026-05", "市委教育工委副书记", "百科", "confirmed")
P(1, 1, "柳河县委书记", "2026-05", "present", "", "官方+百科", "confirmed")
P(1, 6, "柳河县人武部党委第一书记", "2026-07-27", "present", "通化军分区批准", "官方", "confirmed")
# 尤海阳
P(2, 20, "磐石市烟筒山镇副镇长", "unknown", "unknown", "", "官网", "confirmed")
P(2, 20, "共青团磐石市委书记", "unknown", "unknown", "", "官网", "confirmed")
P(2, 20, "磐石市取柴河镇党委书记、镇长", "unknown", "unknown", "", "官网", "confirmed")
P(2, 21, "蛟河市副市长", "unknown", "unknown", "", "官网", "confirmed")
P(2, 28, "温州市政府副秘书长（挂职）", "unknown", "unknown", "", "官网", "confirmed")
P(2, 18, "桦甸市委常委、副市长", "unknown", "unknown", "", "官网", "confirmed")
P(2, 2, "柳河县委副书记、代县长", "2024-12", "2025-01-05", "县人大常委会任命", "官网+两会", "confirmed")
P(2, 2, "柳河县委副书记、县长、县政府党组书记", "2025-01-05", "present", "人大代表选举", "官网+两会", "confirmed")
# 于大军
P(3, 17, "二道江区委常委、宣传部部长", "unknown", "unknown", "", "百科", "plausible")
P(3, 17, "二道江区委常委、区纪委书记", "unknown", "unknown", "", "百科", "plausible")
P(3, 17, "二道江区委副书记、区长", "unknown", "unknown", "", "百科", "plausible")
P(3, 17, "二道江区委书记", "unknown", "unknown", "2020 前", "百科", "plausible")
P(3, 4, "通化市政协党组成员、副主席", "unknown", "unknown", "2020-11 在任", "政协新闻", "plausible")
P(3, 1, "通化市委常委、柳河县委书记", "2021", "2024-09", "", "官方+百科", "confirmed")
# 杨明
P(4, 12, "通化市副市长", "2022-01", "2024-10", "2024-10-25 免职", "市人大决定", "confirmed")
P(4, 1, "通化市委常委、柳河县委书记", "2024-10", "2025-08", "", "官方新闻", "confirmed")
# 郝东军
P(5, 13, "通化市住房和城乡建设局局长", "unknown", "2022-11", "", "公示", "confirmed")
P(5, 2, "柳河县委副书记、县长", "2022-12", "2024-12", "", "官方+公示", "confirmed")
P(5, 16, "通化市民政局一级调研员", "2024-12-30", "present", "", "职级晋升名单", "confirmed")
# 县委班子
P(6, 1, "柳河县委副书记", "2025", "present", "", "官方", "confirmed")
P(7, 1, "柳河县委常委、宣传部部长", "2025", "present", "", "官方", "confirmed")
P(8, 1, "柳河县委常委、县委组织部部长", "2023-02", "present", "", "官方", "confirmed")
P(9, 5, "柳河县纪委书记、县监委主任", "2025-01-05", "present", "", "官方", "confirmed")
P(10, 2, "柳河县常务副县长", "2024-03", "2025-12", "2026 前后由岳宇轩接任", "官方", "confirmed")
P(11, 1, "柳河县委常委（分工待查）", "2025", "present", "", "官方", "confirmed")
P(12, 1, "柳河县委常委（分工待查）", "2025", "present", "", "官方", "confirmed")
P(13, 1, "柳河县委常委、统战部部长（待确认）", "2026", "present", "", "官方新闻", "plausible")
# 政府副职
P(14, 27, "辉南县金川镇副镇长", "unknown", "unknown", "", "官网", "confirmed")
P(14, 27, "辉南县样子哨镇党委副书记、镇长", "unknown", "unknown", "", "官网", "confirmed")
P(14, 27, "辉南县样子哨镇党委书记", "unknown", "unknown", "", "官网", "confirmed")
P(14, 2, "柳河县委常委、常务副县长", "2026", "present", "", "官网", "confirmed")
P(15, 22, "吉林省农业农村厅农业机械化管理处副处长", "unknown", "unknown", "", "官网", "confirmed")
P(15, 22, "吉林省农业农村厅乡村振兴督察专员", "unknown", "unknown", "", "官网", "confirmed")
P(15, 22, "吉林省农业农村厅农村合作经济指导处处长", "unknown", "unknown", "", "官网", "confirmed")
P(15, 2, "柳河县委常委、副县长", "2025", "present", "", "官网", "confirmed")
P(16, 23, "柳河农村商业银行董事长（兼）", "2025", "present", "", "官网", "confirmed")
P(16, 2, "柳河县委常委、副县长", "2025", "present", "", "官网+全会", "confirmed")
P(17, 15, "通化市公安局（国保/有组织犯罪/交警/禁毒序列）", "unknown", "unknown", "", "官网", "confirmed")
P(17, 24, "集安市副市长、市公安局局长", "unknown", "unknown", "", "官网", "confirmed")
P(17, 26, "通化县副县长、县公安局局长", "unknown", "unknown", "", "官网", "confirmed")
P(17, 8, "柳河县副县长、县公安局党委书记、局长", "unknown", "present", "", "官网", "confirmed")
P(18, 27, "辉南县庆阳镇副镇长/团县委（书记）", "unknown", "unknown", "", "官网", "confirmed")
P(18, 2, "柳河县人民政府副县长", "unknown", "present", "", "官网", "confirmed")
P(19, 2, "柳河县（乡镇序列：新发乡/孤山子/柳河镇/三源浦/驼腰岭）", "unknown", "unknown", "", "官网", "confirmed")
P(19, 2, "柳河县发展和改革局党组书记、局长", "unknown", "unknown", "", "官网", "confirmed")
P(19, 2, "柳河县人民政府副县长（住建/交通/自然资源/生态）", "unknown", "present", "", "官网", "confirmed")
P(20, 2, "柳河县委办公室（主任助理/督查室/副主任）", "unknown", "unknown", "", "官网", "confirmed")
P(20, 2, "柳河县人民政府办公室（党组书记/主任）", "unknown", "unknown", "", "官网", "confirmed")
P(20, 2, "柳河县教育局党组书记、局长", "unknown", "unknown", "", "官网", "confirmed")
P(20, 7, "吉林柳河经济开发区党工委书记、管委会主任", "unknown", "unknown", "", "官网", "confirmed")
P(20, 2, "柳河县人民政府副县长（政务、市场、文旅）", "unknown", "present", "", "官网", "confirmed")
P(21, 14, "通化市发改委（服务业/固投序列）", "unknown", "unknown", "", "官网", "confirmed")
P(21, 2, "柳河县人民政府副县长（林业、水利、民政）", "unknown", "present", "", "官网", "confirmed")
# 人大政协 / 法检
P(22, 3, "柳河县人大常委会主任", "2023", "present", "", "官方", "confirmed")
P(23, 4, "柳河县政协党组书记、主席", "2024-10", "present", "", "官方", "confirmed")
P(24, 9, "柳河县人民法院院长", "2025-01-05", "present", "", "官方", "confirmed")
P(25, 10, "柳河县人民检察院检察长", "2025-01-05", "present", "", "官方", "confirmed")
# 孙简
P(26, 11, "吉林省副省长、通化市委书记", "2023", "present", "", "官方", "confirmed")

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "县委书记×县长（2026-05 起共事）", "overlap_org": "中共柳河县委员会", "overlap_period": "2026-05—present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "班子", "context": "书记与纪委书记", "overlap_org": "中共柳河县委员会", "overlap_period": "2026-05—present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "班子", "context": "书记与组织部长", "overlap_org": "中共柳河县委员会", "overlap_period": "2026-05—present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 22, "type": "班子", "context": "书记与人大主任", "overlap_org": "柳河县", "overlap_period": "2026—present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 23, "type": "班子", "context": "书记与政协主席", "overlap_org": "柳河县", "overlap_period": "2026—present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "班子", "context": "书记与常委（葛延江）", "overlap_org": "中共柳河县委员会", "overlap_period": "2026-05—present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "班子", "context": "书记与常委（高湉棋）", "overlap_org": "中共柳河县委员会", "overlap_period": "2026-05—present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "班子", "context": "两位副书记搭档", "overlap_org": "中共柳河县委员会", "overlap_period": "2025—present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "班子", "context": "县长与常务副县长（栗伟）", "overlap_org": "柳河县人民政府", "overlap_period": "2024-12—2025-12", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "班子", "context": "县长与常务副县长（岳宇轩）", "overlap_org": "柳河县人民政府", "overlap_period": "2026—present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "班子", "context": "县长与常委副县长", "overlap_org": "柳河县人民政府", "overlap_period": "2025—present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "班子", "context": "县长与常委副县长（金融）", "overlap_org": "柳河县人民政府", "overlap_period": "2025—present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 17, "type": "班子", "context": "县长与副县长/公安局长", "overlap_org": "柳河县人民政府", "overlap_period": "2024—present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "班子", "context": "书记空缺期由尤海阳主持县委常委会，与纪委书记共事", "overlap_org": "柳河县", "overlap_period": "2025-09—2026-04", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "班子", "context": "县长与组织部长（述职评议等）", "overlap_org": "柳河县", "overlap_period": "2024-12—present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 22, "type": "班子", "context": "县长与人大主任", "overlap_org": "柳河县", "overlap_period": "2024-12—present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 23, "type": "班子", "context": "县长与政协主席", "overlap_org": "柳河县", "overlap_period": "2024-12—present", "confidence": "confirmed"},
    # 前任继任链
    {"person_a": 3, "person_b": 4, "type": "前任继任", "context": "于大军→杨明交棒", "overlap_org": "中共柳河县委员会", "overlap_period": "2024-10", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 1, "type": "前任继任", "context": "杨明 2025-08 底卸任，空缺约 9 个月后刘忠波接任", "overlap_org": "中共柳河县委员会", "overlap_period": "2024-10—2026-05", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 2, "type": "前任继任", "context": "郝东军→尤海阳（2024-12 代→2025-01 当选）", "overlap_org": "柳河县人民政府", "overlap_period": "2024-12", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 5, "type": "上下级", "context": "于大军（书记）与郝东军（县长）搭档", "overlap_org": "柳河县", "overlap_period": "2022-12—2024-09", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 2, "type": "上下级", "context": "杨明（书记）与尤海阳（县长）搭档", "overlap_org": "柳河县", "overlap_period": "2024-10—2025-08", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 22, "type": "班子", "context": "书记与人大主任", "overlap_org": "柳河县", "overlap_period": "2021—2024-09", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 23, "type": "班子", "context": "书记与政协主席", "overlap_org": "柳河县", "overlap_period": "2022—2024-09", "confidence": "confirmed"},
    # 跨县域 / 系统交集
    {"person_a": 1, "person_b": 17, "type": "共事（推定）", "context": "通化县委班子交叉（刘忠波常务副县长、张立志公安局长，时段推定）", "overlap_org": "通化县", "overlap_period": "2018—2021（推定）", "confidence": "plausible"},
    {"person_a": 14, "person_b": 18, "type": "同县成长", "context": "岳宇轩/曹丹 均自辉南县成长", "overlap_org": "辉南县", "overlap_period": "2013—2023（推定重叠）", "confidence": "plausible"},
    {"person_a": 16, "person_b": 15, "type": "班子", "context": "同为县委常委、副县长", "overlap_org": "柳河县人民政府", "overlap_period": "2025—present", "confidence": "confirmed"},
    {"person_a": 16, "person_b": 14, "type": "班子", "context": "政府班子成员", "overlap_org": "柳河县人民政府", "overlap_period": "2026—present", "confidence": "confirmed"},
    # 市级领导
    {"person_a": 26, "person_b": 1, "type": "上下级", "context": "通化市委书记（副省长兼）与柳河县委书记", "overlap_org": "中共通化市委员会", "overlap_period": "2026—present", "confidence": "confirmed"},
    {"person_a": 26, "person_b": 2, "type": "上下级", "context": "通化市委书记与柳河县长", "overlap_org": "中共通化市委员会", "overlap_period": "2024-12—present", "confidence": "confirmed"},
    {"person_a": 26, "person_b": 4, "type": "上下级", "context": "2025-08 孙简调研柳河县，杨明陪同", "overlap_org": "通化市", "overlap_period": "2025", "confidence": "confirmed"},
]

# ── Person JSON deep records ──────────────────────────────────────────────────
JSON_JOB = {1: "县委书记", 2: "县长", 3: "前任县委书记", 4: "前任县委书记", 5: "前任县长"}

SOURCES = [
    {"id": "S001", "title": "柳河县人民政府 领导之窗（县长及副县长简历）", "url": "http://www.jllh.gov.cn/xxgk/ldzg/", "publisher": "柳河县人民政府", "published_at": "2026-08-11(访问)", "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high", "notes": "县长与县政府各副县长简历"},
    {"id": "S002", "title": "县人武部党委第一书记任职仪式", "url": "http://www.jllh.gov.cn/xxgk/lhyg/202607/t20260728_778796.html", "publisher": "柳河县融媒体中心", "published_at": "2026-07-28", "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high", "notes": "刘忠波增补人武部第一书记"},
    {"id": "S003", "title": "县委常委会召开2026年第11次会议", "url": "http://www.jllh.gov.cn/xxgk/lhyg/202608/t20260806_779663.html", "publisher": "柳河县融媒体中心", "published_at": "2026-08-06", "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high", "notes": ""},
    {"id": "S004", "title": "柳河要情（lhyg）新闻列页 2024-07 至 2026-08", "url": "http://www.jllh.gov.cn/xxgk/lhyg/", "publisher": "柳河县融媒体中心", "published_at": "2026-08-11", "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high", "notes": "370+ 篇县领导活动新闻（含班子名单）"},
    {"id": "S005", "title": "柳河县第十九届人民代表大会第四次会议闭幕（尤海阳当选县长）", "url": "http://www.jllh.gov.cn/xxgk/lhyg/202501/t20250106_729687.html", "publisher": "柳河县融媒体中心", "published_at": "2025-01-05", "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high", "notes": ""},
    {"id": "S006", "title": "柳河县第十九届人民代表大会第五次会议闭幕", "url": "http://www.jllh.gov.cn/xxgk/lhyg/202512/t20251229_759800.html", "publisher": "柳河县融媒体中心", "published_at": "2025-12-27", "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high", "notes": "人大班子名单（张成祥/王春雷等）"},
    {"id": "S007", "title": "中共柳河县委十六届九次全体会议", "url": "http://www.jllh.gov.cn/xxgk/lhyg/202512/t20251212_757899.html", "publisher": "柳河县融媒体中心", "published_at": "2025-12-11", "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high", "notes": "县委常委会名单（赵岩/臧云烨/王杰/栗伟/黄绪强/葛延江/高闯/高湉棋）"},
    {"id": "S008", "title": "县委常委会召开2026年第1次会议（尤海阳主持）", "url": "http://www.jllh.gov.cn/xxgk/lhyg/202601/t20260127_764275.html", "publisher": "柳河县融媒体中心", "published_at": "2026-01-26", "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high", "notes": "书记空缺期由尤海阳主持县委常委会"},
    {"id": "S009", "title": "中国共产党柳河县第十六届纪律检查委员会第六次全体会议", "url": "http://www.jllh.gov.cn/xxgk/lhyg/202601/t20260129_764662.html", "publisher": "柳河县融媒体中心", "published_at": "2026-01-28", "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high", "notes": "黄绪强主持并作报告"},
    {"id": "S010", "title": "刘忠波调研我县统战工作", "url": "http://www.jllh.gov.cn/xxgk/lhyg/202608/t20260810_779842.html", "publisher": "柳河县融媒体中心", "published_at": "2026-08-07", "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high", "notes": "邵帅陪同（统战部长推断来源）"},
    {"id": "S011", "title": "刘忠波（吉林省通化市柳河县委书记）百度百科", "url": "https://baike.baidu.com/item/刘忠波/60193288", "publisher": "百度百科", "published_at": "2026-08(访问)", "accessed_at": "2026-08-12", "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
    {"id": "S012", "title": "省管干部任职前公示公告（2022年第9号）：郝东军", "url": "微信公众号（吉林省组织）转载", "publisher": "吉林省委组织部", "published_at": "2022-11-04", "accessed_at": "2026-08-12", "source_type": "appointment_notice", "reliability": "high", "notes": "郝东军：1971-06 生、在职大学、原通化市住建局局长"},
    {"id": "S013", "title": "吉林省一地发布最新人事动态（通化市人大常委会决定 2024-10-25）", "url": "澎湃新闻/北方法制报", "publisher": "澎湃新闻", "published_at": "2024-10-29", "accessed_at": "2026-08-12", "source_type": "media", "reliability": "medium", "notes": "因工作变动免去王雁飞、杨明副市长等职务"},
    {"id": "S014", "title": "通化市政协新闻（于大军 2020-11）", "url": "微信公众号转载", "publisher": "通化媒体", "published_at": "2020-11-04", "accessed_at": "2026-08-12", "source_type": "media", "reliability": "medium", "notes": "市政协副主席于大军视察东昌区"},
    {"id": "S015", "title": "通化市职级晋升名单（2024-12-30）", "url": "微信公众号转载", "publisher": "通化市组织部门", "published_at": "2024-12-30", "accessed_at": "2026-08-12", "source_type": "appointment_notice", "reliability": "medium", "notes": "郝东军任市民政局一级调研员"},
    {"id": "S016", "title": "柳河县与温岭对口合作工作领导小组名单（2023-02）", "url": "http://xxgk.jllh.gov.cn/", "publisher": "柳河县政府信息公开", "published_at": "2023-02-01", "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high", "notes": "王杰任副组长（组织部长）"},
    {"id": "S017", "title": "通化市领导之窗（孙简）", "url": "http://www.tonghua.gov.cn/ldzg/", "publisher": "通化市人民政府", "published_at": "2026-08(访问)", "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high", "notes": "副省长、市委书记"},
]

OPEN_QUESTIONS = {
    1: [
        {"priority": "high", "question": "刘忠波任通化县副县长/主任/组织部长/常务副县长的任期年份段", "why_it_matters": "2010 年代通化县班子的精确时间线", "suggested_queries": ["刘忠波 通化县 常务副县长 2019"], "last_attempted": "2026-08-12"},
        {"priority": "medium", "question": "刘忠波出生地/籍贯", "why_it_matters": "身份画像补全", "suggested_queries": ["刘忠波 籍贯"], "last_attempted": "2026-08-12"},
    ],
    2: [
        {"priority": "high", "question": "尤海阳任柳河代县长的县人大常委会决定日期（2024-12 内具体日）", "why_it_matters": "交接链精确到日", "suggested_queries": ["尤海阳 柳河 代县长 人大常委会"], "last_attempted": "2026-08-12"},
        {"priority": "medium", "question": "尤海阳在磐石/蛟河/桦甸各职务的起止时间", "why_it_matters": "吉林市系成长路径时长", "suggested_queries": ["尤海阳 桦甸市副市长 2023"], "last_attempted": "2026-08-12"},
    ],
    3: [
        {"priority": "critical", "question": "于大军 2024 年 9 月卸任柳河县委书记后的去向（现职）", "why_it_matters": "前任书记去向是干部流向关键节点", "suggested_queries": ["于大军 通化 2025 任命"], "last_attempted": "2026-08-12"},
        {"priority": "high", "question": "于大军任柳河县委书记的精确起始时间（2021 年内月份）", "why_it_matters": "锁定 2021-2024 班子任期", "suggested_queries": ["于大军 柳河县委书记 干部大会"], "last_attempted": "2026-08-12"},
    ],
    4: [
        {"priority": "critical", "question": "杨明 2025 年 8 月底卸任柳河县委书记后的去向（现职）", "why_it_matters": "市级班子去向与通化市干部流向", "suggested_queries": ["杨明 通化市委 2025 任命"], "last_attempted": "2026-08-12"},
        {"priority": "high", "question": "杨明出生年月/教育背景/早期履历（任副市长前）", "why_it_matters": "其 2024 年调整的驱动因素", "suggested_queries": ["杨明 通化市副市长 简历"], "last_attempted": "2026-08-12"},
    ],
    5: [
        {"priority": "medium", "question": "郝东军任柳河县长前在通化市住建局的任职起始", "why_it_matters": "专业型干部画像", "suggested_queries": ["郝东军 通化市住建局"], "last_attempted": "2026-08-12"},
    ],
    10: [
        {"priority": "high", "question": "栗伟 2025 年底后去向（原常务副县长）", "why_it_matters": "县政府常务岗位交接链", "suggested_queries": ["栗伟 柳河县 调任"], "last_attempted": "2026-08-12"},
        {"priority": "medium", "question": "栗伟出生信息与早期履历", "why_it_matters": "班子成员画像补全", "suggested_queries": ["栗伟 柳河 简历"], "last_attempted": "2026-08-12"},
    ],
    11: [{"priority": "medium", "question": "葛延江分工（政法/统战/其他）与履历", "why_it_matters": "常委会分工图谱缺一键", "suggested_queries": ["葛延江 柳河县 常委"], "last_attempted": "2026-08-12"}],
    12: [{"priority": "medium", "question": "高湉棋分工与履历", "why_it_matters": "常委会分工", "suggested_queries": ["高湉棋 柳河"], "last_attempted": "2026-08-12"}],
    13: [{"priority": "medium", "question": "确认邵帅是否为统战部长（当前 plausible）", "why_it_matters": "统战职责归属", "suggested_queries": ["邵帅 柳河县 统战部"], "last_attempted": "2026-08-12"}],
    6: [{"priority": "low", "question": "赵岩副书记履历", "why_it_matters": "班子画像", "suggested_queries": ["赵岩 柳河县委副书记"], "last_attempted": "2026-08-12"}],
}

TIMELINES = {
    1: [
        {"start": "1994-09", "end": "1996-07", "org": "通化师范学院中文系", "title": "汉语言文学专业学习（在职）", "confidence": "confirmed", "source_ids": ["S011"]},
        {"start": "unknown", "end": "unknown", "org": "通化县", "title": "副县长→县委常委、县委办主任→组织部长、党校校长→常务副县长", "confidence": "plausible", "source_ids": ["S011"]},
        {"start": "2021-08", "end": "2025-02", "org": "通化市教育局", "title": "党组书记、局长", "confidence": "confirmed", "source_ids": ["S011"]},
        {"start": "2025-02", "end": "2026-05", "org": "通化市教育局", "title": "局长、一级调研员（兼任市委教育工委副书记）", "confidence": "confirmed", "source_ids": ["S011"]},
        {"start": "2026-05", "end": "present", "org": "柳河县", "title": "柳河县委书记", "confidence": "confirmed", "source_ids": ["S011"]},
        {"start": "2026-07-27", "end": "present", "org": "柳河县人武部", "title": "人武部党委第一书记（兼任）", "confidence": "confirmed", "source_ids": ["S002"]},
    ],
    2: [
        {"start": "unknown", "end": "unknown", "org": "磐石市", "title": "烟筒山镇副镇长→团市委书记→取柴河镇党委书记、镇长", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "蛟河市", "title": "副市长", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "温州市", "title": "市政府副秘书长（挂职）", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "桦甸市", "title": "市委常委、副市长", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2024-12", "end": "2025-01-05", "org": "柳河县政府", "title": "代县长", "confidence": "confirmed", "source_ids": ["S005"]},
        {"start": "2025-01-05", "end": "present", "org": "柳河县政府", "title": "县委副书记、县长、县政府党组书记", "confidence": "confirmed", "source_ids": ["S005"]},
        {"start": "2025-09", "end": "2026-04", "org": "中共柳河县委员会", "title": "书记空缺期主持县委常委会", "confidence": "confirmed", "source_ids": ["S008"]},
    ],
    3: [
        {"start": "unknown", "end": "unknown", "org": "二道江区", "title": "区委常委、宣传部部长→区纪委书记", "confidence": "plausible", "source_ids": ["S014"]},
        {"start": "unknown", "end": "unknown", "org": "二道江区", "title": "区委副书记、区长→区委书记", "confidence": "plausible", "source_ids": ["S014"]},
        {"start": "unknown", "end": "unknown", "org": "通化市政协", "title": "党组成员、副主席（2020-11 在任）", "confidence": "plausible", "source_ids": ["S014"]},
        {"start": "2021", "end": "2024-09", "org": "柳河县", "title": "通化市委常委、柳河县委书记", "confidence": "confirmed", "source_ids": ["S004"]},
    ],
    4: [
        {"start": "2022-01", "end": "2024-10", "org": "通化市政府", "title": "副市长", "confidence": "confirmed", "source_ids": ["S013"]},
        {"start": "2024-10", "end": "2025-08", "org": "柳河县", "title": "通化市委常委、柳河县委书记", "confidence": "confirmed", "source_ids": ["S004"]},
    ],
    5: [
        {"start": "unknown", "end": "2022-11", "org": "通化市住建局", "title": "党组书记、局长", "confidence": "confirmed", "source_ids": ["S012"]},
        {"start": "2022-12", "end": "2024-12", "org": "柳河县政府", "title": "县委副书记、县长", "confidence": "confirmed", "source_ids": ["S012", "S004"]},
        {"start": "2024-12-30", "end": "present", "org": "通化市民政局", "title": "一级调研员", "confidence": "confirmed", "source_ids": ["S015"]},
    ],
}

PROFILES = {
    1: {"career_pattern": "provincial_city_ladder", "systems_experience": ["party", "government", "education", "organization"], "geographic": ["通化县", "通化市", "柳河县"], "primary_specializations": ["教育管理", "组织人事", "县域治理"]},
    2: {"career_pattern": "cross_county_rotation", "systems_experience": ["youth_league", "government", "township", "挂职"], "geographic": ["磐石", "蛟河", "桦甸", "温州", "柳河"], "primary_specializations": ["经济治理", "基层治理", "民生保障"]},
    3: {"career_pattern": "district_ladder", "systems_experience": ["party", "propaganda", "discipline", "government", "政协"], "geographic": ["二道江区", "柳河县"], "primary_specializations": ["基层组织", "纪律检查", "区域规划"]},
    4: {"career_pattern": "cross_county_rotation", "systems_experience": ["government", "party"], "geographic": ["通化市", "柳河县"], "primary_specializations": ["综合行政"]},
    5: {"career_pattern": "municipal_department_to_county", "systems_experience": ["construction", "government"], "geographic": ["通化市", "柳河县"], "primary_specializations": ["住建", "城建规划"]},
}

STYLE = {
    1: [
        {"trait": "grassroots_oriented", "evidence": "2026-06 至 08 高频赴乡镇/街道调研：安全生产、产业、防汛、教育、文旅（官方新闻逐周可见）", "confidence": "confirmed", "source_ids": ["S004"]},
        {"trait": "discipline_oriented", "evidence": "反复强调政绩观、安全底线、防汛 24 小时值守、纠治形式主义", "confidence": "plausible", "source_ids": ["S003"]},
    ],
    2: [
        {"trait": "stability_oriented", "evidence": "书记空缺约 9 个月主持全县工作，保持班子稳定与工作连续", "confidence": "confirmed", "source_ids": ["S008"]},
        {"trait": "pragmatic", "evidence": "多次督查安全生产、医保基金监管与社会救助规范（2026-07 调研新闻）", "confidence": "plausible", "source_ids": ["S004"]},
    ],
}

RISKS = {
    1: [{"type": "none_found", "description": "2026-08-12 搜索范围内未见纪检调查/负面报道", "date": "2026-08-12", "confidence": "unverified", "source_ids": []}],
    2: [{"type": "none_found", "description": "2026-08-12 搜索范围内未见纪检调查/负面报道", "date": "2026-08-12", "confidence": "unverified", "source_ids": []}],
    3: [{"type": "inspection_feedback", "description": "2024-02 省委巡视组向柳河县反馈巡视情况，于大军主持反馈会议并作表态发言（例行巡视）", "date": "2024-02", "confidence": "confirmed", "source_ids": ["S014"]}],
}

GOV_RECORDS = {
    1: [
        {"period": "2026-06 至 08", "domain": "economic_development", "achievement_or_event": "任内密集督导安全生产、防汛体系、乡村特色产业（林蛙、参旅融合、漂流项目等）", "role_in_event": "县委书记", "confidence": "plausible", "source_ids": ["S004"]},
    ],
    2: [
        {"period": "2025", "domain": "economic_development", "achievement_or_event": "主持县政府全面工作，推进'四个百亿级'产业集群与'十五五'规划编制", "role_in_event": "县长", "confidence": "plausible", "source_ids": ["S004"]},
    ],
}


def _p(pid: int) -> dict:
    for p in persons:
        if p["id"] == pid:
            return p
    raise KeyError(f"person id {pid} not found")


def write_person_json(pid: int) -> None:
    p = _p(pid)
    name = p["name"]
    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省", "city": "通化市", "region": "柳河县",
            "job": JSON_JOB.get(pid, p["current_post"]), "task_id": "jilin_柳河县", "time_focus": "2021-2026",
        },
        "identity": {
            "person_id": f"liuhe_county_{name}",
            "name": name,
            "aliases": [], "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""),
            "education": [{"institution": p.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": p.get("party_join", ""), "work_start": p.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{name}_{p.get('birth', '')}", "official_profile_url": p.get("source", "")},
        },
        "current_status": {
            "current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级" if pid in {1, 2} else "待查",
            "as_of": AS_OF, "is_current_confirmed": p.get("confidence") == "confirmed", "source_ids": [],
        },
        "career_timeline": TIMELINES.get(pid, []),
        "organizations": [{"name": p.get("current_org", ""), "role": "current"}],
        "relationships": [
            {
                "person": _p(r["person_b"])["name"] if r["person_a"] == pid else _p(r["person_a"])["name"],
                "person_id": "",
                "relationship_type": r["type"],
                "evidence": r["context"],
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": r.get("confidence", "plausible"),
                "source_ids": [x["id"] for x in SOURCES],
            }
            for r in relationships if r["person_a"] == pid or r["person_b"] == pid
        ],
        "governance_record": GOV_RECORDS.get(pid, []),
        "professional_profile": PROFILES.get(pid, {"career_pattern": "unknown", "systems_experience": [], "geographic": [], "primary_specializations": []}),
        "work_style_and_personality": {
            "public_style_indicators": STYLE.get(pid, []),
            "speech_themes": [], "management_signals": [],
            "caveat": "工作风格根据公开活动与报道推断，并非私人心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": RISKS.get(pid, []),
        "source_register": SOURCES,
        "confidence_summary": {
            "identity": p.get("confidence", "plausible"),
            "current_role": p.get("confidence", "plausible"),
            "career_completeness": "partial" if pid in {1, 2} else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": (OPEN_QUESTIONS.get(pid, [{}])[0].get("question", "")),
        },
        "open_questions": OPEN_QUESTIONS.get(pid, []),
    }
    fname = f"{TODAY}-吉林省-通化市-{JSON_JOB.get(pid, p['current_post'])}-{name}.json"
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
        positions=[dict(zip(["person_id", "org_id", "title", "start", "end", "rank", "note", "confidence"], row)) for row in _positions],
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print("  Writing person JSONs...")
    for pid in sorted(JSON_JOB):
        write_person_json(pid)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())