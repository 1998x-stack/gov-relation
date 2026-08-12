#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 盖州市 (营口市，辽宁省).

Investigation date: 2026-08-12
Task ID: liaoning_盖州市
Level: 县级市
Parent city: 营口市
Targets: 市委书记 & 市长

Research status: PRIMARY SOURCE ACCESS (official city portal gaizhou.gov.cn + 营口市委组织部公示)
  - 盖州市人民政府门户 (www.gaizhou.gov.cn) 一手信源充分：领导之窗（市长/副市长简历）、
    中国共产党盖州市第八次代表大会（2026-07-22/24 换届报道）、八届一次全会（2026-07-24 选举，
    2026-07-27 发布）、2026 三级河长公示（2026-06-18，载明市委/政府班子分工）、历次市委常委会、
    政府工作报告（2025）；营口市委组织部任前公示（2021-2026 多号）与辽宁省管干部任前公示（2025年第5号）。
  - 现任市委书记 李典阁、市委副书记/市长 袁世君、专职副书记 张鑫煜 已通过官方一手信源确认；
    李典阁系 辽宁省管干部任前公示(2025年第5号) 后由 辽阳县委副书记、县长 跨市调任（2026-05 起
    以书记身份履职，2026-07-24 在市第八次党代会换届后当选八届市委书记）。其更早履历：曾任辽阳县
    纪委书记、监委主任（2019-11 前已在任）→ 2022-04 辽阳县副县长/代县长 → 县长 → 辽阳县委书记（2025-06/07）→ 盖州书记。
  - 徐海龙（2021-07 由市长转任市委书记，此前在大石桥市长期任职后调任盖州）在 2026-02 仍为书记，
    2026-05-24 市委常委会已由李典阁主持——徐海龙于 2026 年上半年卸任，具体去向待核（最大开放缺口）。
  - 前前任书记链：王庆珂（~2013前）→ 班耀康（2013-07~2017-10）→ 吴峰（2017-10~2021-07，现营口市政协党组成员、秘书长）→ 徐海龙。
  - 市长链：赵国栋（~2013-2015）→ 朱文铎（2016-01~2017-03，后被查双开）→ 徐海龙（2017~2021-07）→ 袁世君（2021-07~）。
  - Exa 检索可用；百度百科/360百科/镜像为次级来源并已降级标注。部分常委（曲松楠、姜爽等）出生/学历未公开，按证据分级。

Confirmed current officeholders (as of 2026-08-12):
   - 市委书记: 李典阁（八代会/八届一次全会/多次常委会、调研报道；2026-07-24 当选八届书记）
   - 市委副书记、市长: 袁世君（市政府党组书记、市长；官网简历 1978-05，研究生/工程硕士；
     2021-07 由省委/营口市委提名市长候选人并当选；2026-07-24 连任八届市委副书记）
   - 市委副书记（专职）: 张鑫煜（2026-03-02 高质量发展推进会主持；2026-07-24 当选副书记；
     2025-07 由营口市公安局政治部主任/二级高级警长拟任县区委副书记）
   - 市委常委（八届，分工均获官方河长表/全会/纪委交叉确认）: 李维（常务副市长/政府党组副书记，满族，
     1983-04 在职研究生/硕士，原北海经开区党工委书记、管委会主任）、王一震（政法委书记，1975-04 原公安局长）、
     李悦（组织部长，1982-06 原营口市委巡察办副主任）、葛鑫（纪委书记/监委主任）、曲松楠（宣传部长，
     兼市委教育工委书记）、姜爽（人武部长）、李静波（统战部长，女 1974-08 原西市区副区长）、梁迅峥（副市长 1986-09 大学）
   - 市政府副市长: 李维（常务）、梁迅峥、邵凤江（公安局长，1970-07 大学本科）、蒋存祺（1987-10 研究生/硕士）、
     邹艳丽（女，1980-09 研究生）；市政府党组成员: 李瀚霖
   - 市人大常委会主任: 董伟（1973-12，2025-12-31 补选；原营口市人大人事选举委主任委员）
   - 市政协主席: 吕永祥（1967-05，2025-12-29 政协八届五次会议任主席；原盖州市人大副主任→市委副书记）

Predecessor timeline (多源拼合，营口市委组织部公示+官网)：
   - 市委书记: 班耀康（2013-07~2017-10）→ 吴峰（2017-10-10~2021-07-10，现任营口市政协党组成员、秘书长）→
     徐海龙（2021-07-10 由市长转任书记，2026 上半年卸任，去向待核）→ 李典阁（2026-05 履职，2026-07-24 当选）
   - 市长: 赵国栋（~2013-2015）→ 朱文铎（2016-01~2017-03）→ 徐海龙（2017-12~2021-07）→ 袁世君（2021-07~）
   - 2021-07-10 干部大会（营口市委常委、组织部部长孙雨宣布）：张杨任市委副书记（不再任宣传部长）、
     王锐任市委常委/副市长、李默任市委常委、李扬提名副市长
   - 政府班子演变：2024-05 衣冠鹏（党组副书记/常务）/李默/刘雪峰/乔焱/王一震/张继成/陈洪波 → 2024-11 邵凤江入班子 →
     2025-10 常务副市长衣冠鹏/副市长李默 → 2026 衣冠鹏调任大石桥市长、李维升任常务副市长、梁迅峥/蒋存祺/邹艳丽在班子

Cross-region / context:
   - 盖州市系营口市代管的县级市，营口市委书记姚华明、市长李军（参照营口市库）
   - 李典阁由辽阳市辽阳县县长跨市调任（省管干部任前公示2025年第5号）——辽阳→营口跨市交流
   - 营口市域内密集双向流动：徐海龙（大石桥→盖州）、王克大（大石桥公安→盖州副市长，2019 公示）、
     衣冠鹏（盖州常务副市长→大石桥市长，2025-12）、张杨（盖州副书记→站前区委书记）、曹德强（盖州组织部长→
     副书记→营口社工部长→西市区委书记，2026 省公示）、王锐（盖州常委/副市长→营口市工信局长，2026-03 人大任命）、
     吴峰（鲅鱼圈经开区→仙人岛园区→盖州书记→营口市政协秘书长）、朱文铎（老边→盖州市长→营口交通局长）
   - 盖州为"中国苹果之乡"农业大市，拥有北海、仙人岛两个省级经开区，营口LNG接收站等重大项目，
    2025 年地区生产总值约 200 亿元、财政收入增长较快；获"东北县域经济发展潜力十强"首位

Confidence policy: 当前角色（书记/市长/常委分工/副市长）confirmed（官方一手，河长公示+换届报道+常委会）；
  身份（出生/学历）对市长、常务副市长及多数副市长为 confirmed（官网简历），对部分常委为 plausible（任前公示）；
  前任（徐海龙去向为 UNKNOWN、吴峰=confirmed 营口市政协秘书长）；李典阁早期（辽阳纪委书记段）confirmed。
"""

from __future__ import annotations

import json
import sqlite3  # noqa: F401  (DB I/O handled by gov_relation.runner)
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

from gov_relation.runner import run_build

# ── Metadata ─────────────────────────────────────────────────────────────
SLUG = "盖州市"
AS_OF = "2026-08-12"

_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"
PERSONS_STAGING_DIR = _CURRENT_DIR

# ── Persons ──────────────────────────────────────────────────────────────
# 主要一手来源: 盖州市政府门户（http://www.gaizhou.gov.cn/）领导之窗/新闻中心/河长公示
persons = [
    # ── 市委（核心） ──
    {"id": 1, "name": "李典阁", "gender": "男", "ethnicity": "汉族", "birth": "1975-02", "birthplace": "",
     "education": "大学学历、硕士学位", "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记", "current_org": "中国共产党盖州市委员会",
     "source": "https://www.ln.gov.cn/web/ywdt/jrln/wzxx2018/2025060919443373914/index.shtml (辽宁省管干部任前公示2025年第5号) + https://www.bjsupervision.gov.cn/qfy/bmlf/201911/t20191101_66619.html (2019-11 辽阳县纪委书记/监委主任) + http://www.ljying.com/... 盖州 2026 报道"},
    {"id": 2, "name": "袁世君", "gender": "男", "ethnicity": "汉族", "birth": "1978-05", "birthplace": "",
     "education": "研究生学历、工程硕士学位", "party_join": "中共党员", "work_start": "",
     "current_post": "市委副书记、市长", "current_org": "盖州市人民政府",
     "source": "http://www.gaizhou.gov.cn/ldzc/012001/012001001/leader.html (盖州市政府领导之窗/市长简历) + 2021-07-10 干部大会 (提名市长候选人)"},
    {"id": 3, "name": "张鑫煜", "gender": "男", "ethnicity": "汉族", "birth": "1975-02", "birthplace": "",
     "education": "在职大学学历、学士学位", "party_join": "中共党员", "work_start": "",
     "current_post": "市委副书记（专职）", "current_org": "中国共产党盖州市委员会",
     "source": "https://www.yingkou.gov.cn/govxxgk/ykszf/2025-07-14/ (营口市委组织部公告：市公安局党委委员、政治部主任、二级高级警长拟任县（市）区委副书记) + http://gaizhou.gov.cn/003/003003/20260302/0f25be7c-135d-484b-a6bf-28af200d578b.html (2026-02-28 高质量发展推进会主持) + 八届一次全会 (2026-07-24 当选副书记)"},
    {"id": 4, "name": "李维", "gender": "男", "ethnicity": "满族", "birth": "1983-04", "birthplace": "",
     "education": "在职研究生学历、硕士学位", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、市政府党组副书记、常务副市长", "current_org": "盖州市人民政府",
     "source": "http://www.gaizhou.gov.cn/ldzc/012003/012003006/leader.html (政府领导·李维) + 2026-06-18 三级河长公示 (市委常委会、常务副总河长) + 百度百科 (原北海经开区党工委副书记、管委会主任；含发改、能源局任职)"},
    {"id": 5, "name": "王一震", "gender": "男", "ethnicity": "汉族", "birth": "1975-04", "birthplace": "营口市(生)",
     "education": "大学学历、学士学位", "party_join": "中共党员", "work_start": "1998-08",
     "current_post": "市委常委、政法委书记", "current_org": "中国共产党盖州市委员会",
     "source": "营口市委组织部2024年17号公告 (2024-04-22：副市长/公安局长拟任县（市）区委常委) + 2026-06-18 三级河长公示 (政法委书记) + 2024-11 分工调整文件 (原市公安局局长)"},
    {"id": 6, "name": "李悦", "gender": "男", "ethnicity": "汉族", "birth": "1982-06", "birthplace": "",
     "education": "大学学历、学士学位", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、组织部部长", "current_org": "中国共产党盖州市委员会",
     "source": "营口市委组织部公告(2023-12-27, ykd 202312月)：市委巡察工作领导小组办公室副主任、四级高级监察官拟任县（市）区委常委 + 2026-06-18 三级河长公示 (组织部长) + 八届一次全会 (常委)"},
    {"id": 7, "name": "葛鑫", "gender": "男", "ethnicity": "满族", "birth": "1980-03", "birthplace": "",
     "education": "省委党校大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、市纪委书记、市监委主任", "current_org": "中国共产党盖州市纪律检查委员会/盖州市监察委员会",
     "source": "营口市纪检监察网/百家 (原营口市纪委监委第一纪检监察室主任、四级高级监察官；2023-08 任前公示拟任县（市）区委常委、纪委书记) + 2026-01-26 市纪委七届六次全会主持 (盖州市委常委、纪委书记、监委主任)"},
    {"id": 8, "name": "曲松楠", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、宣传部部长（兼市委教育工委书记）", "current_org": "中国共产党盖州市委员会",
     "source": "2026-06-18 三级河长公示 (市委常委会宣传部长) + 2025-05-20 市委教育工委 (兼) + 2024-06 文联交流 (男性称谓)"},
    {"id": 9, "name": "姜爽", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "军队干部（履历未公开）", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、人武部部长", "current_org": "中国共产党盖州市委员会（人武部）",
     "source": "2026-01-28 市人武部党委（扩大）会议 (市委常委、人武部党委副书记、部长姜爽讲话) + 2026-06-18 三级河长公示"},
    {"id": 10, "name": "李静波", "gender": "女", "ethnicity": "汉族", "birth": "1974-08", "birthplace": "",
     "education": "大学学历、学士学位(工学学士)", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、统战部部长", "current_org": "中国共产党盖州市委员会",
     "source": "营口市委组织部2026年第6号任前公示 (西市区副区长拟任县（市）区委常委；2024-08 公示：西市区得胜街道党工委书记→拟提名副区长) + 2026-06-18 三级河长公示 (市委常委统战部长) + 八届一次全会 (常委)"},
    {"id": 11, "name": "梁迅峥", "gender": "男", "ethnicity": "待确认", "birth": "1986-09", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、副市长", "current_org": "盖州市人民政府",
     "source": "http://gaizhou.gov.cn/ldzc/012003/012003007/leader.html (政府领导·梁迅峥) + 八届一次全会 (常委)"},
    {"id": 12, "name": "邵凤江", "gender": "男", "ethnicity": "汉族", "birth": "1970-07", "birthplace": "",
     "education": "大学本科学历", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长、市公安局局长", "current_org": "盖州市公安局",
     "source": "http://gaizhou.gov.cn/ldzc/012003/012003001/leader.html (政府领导·邵凤江)"},
    {"id": 13, "name": "蒋存祺", "gender": "男", "ethnicity": "汉族", "birth": "1987-10", "birthplace": "",
     "education": "研究生学历、硕士学位", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "盖州市人民政府",
     "source": "http://gaizhou.gov.cn/ldzc/012003/012003008/leader.html (政府领导·蒋存祺) + 2025-10 河长公示 (曾任青石岭镇党委书记)"},
    {"id": 14, "name": "邹艳丽", "gender": "女", "ethnicity": "待确认", "birth": "1980-09", "birthplace": "",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "盖州市人民政府",
     "source": "http://gaizhou.gov.cn/ldzc/012003/012003003/leader.html (政府领导·邹艳丽) + 2025-10 河长公示 (曾任二台乡党委书记)"},
    {"id": 15, "name": "李瀚霖", "gender": "待确认", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "市政府党组成员", "current_org": "盖州市人民政府",
     "source": "2026-06-18 三级河长公示 (市政府党组成员/河长) + 2026-06-08 安全生产防汛会议 (市及经开区领导)"},
    {"id": 16, "name": "董伟", "gender": "男", "ethnicity": "汉族", "birth": "1973-12", "birthplace": "",
     "education": "大学学历、学士学位", "party_join": "中共党员", "work_start": "",
     "current_post": "市人大常委会党组书记、主任", "current_org": "盖州市人民代表大会常务委员会",
     "source": "https://www.yingkou.gov.cn/govxxgk/ykszf/2025-07-14/ (营口市人大常委会人事选举委员会主任委员拟任盖州人大主任) + 2025-12-31 市八届人大五次会议补选为主任 (gaizhou.gov.cn) + 2026-05-24 市委常委会扩大会议出席"},
    {"id": 17, "name": "吕永祥", "gender": "男", "ethnicity": "汉族", "birth": "1967-05", "birthplace": "",
     "education": "在职大专学历", "party_join": "中共党员", "work_start": "",
     "current_post": "市政协党组书记、主席", "current_org": "中国人民政治协商会议盖州市委员会",
     "source": "营口市委组织部2024年17号公告 (2024-04-22 盖州市人大党组副书记、副主任拟任县（市）区委副书记) + 2025-06-13 公示拟提名政协主席候选人 + 2025-12-29 政协八届五次会议任主席 + 2026 出席记录"},
    # ── 前任/交流 ──
    {"id": 18, "name": "徐海龙", "gender": "男", "ethnicity": "汉族", "birth": "1976-06", "birthplace": "",
     "education": "在职大学学历", "party_join": "1998-08", "work_start": "1996-11",
     "current_post": "（前任）市委书记", "current_org": "中国共产党盖州市委员会",
     "source": "百度百科 (1976-06生，大石桥乡镇/园区→盖州) + 2021-07-10 干部大会 (任市委书记/不再任市长) + 2026-03-02 高质量发展推进会仍在任；2026 上半年卸任，去向待核"},
    {"id": 19, "name": "吴峰", "gender": "男", "ethnicity": "满族", "birth": "1966-01", "birthplace": "",
     "education": "全日制大学学历", "party_join": "1997-06", "work_start": "1990-11",
     "current_post": "（前任）市委书记，现任营口市政协党组成员、秘书长", "current_org": "中国人民政治协商会议营口市委员会",
     "source": "2017-09 任前公示 (仙人岛能源化工区党工委副书记、管委会常务副主任拟任盖州市委书记) + 营口市政协 (2022-12 起为市政协委员；党组成员、秘书长) + 2021-07-10 干部大会 (免去盖州市委书记)"},
    {"id": 20, "name": "衣冠鹏", "gender": "男", "ethnicity": "汉族", "birth": "1978-09", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "（交流）大石桥市委副书记、市政府党组书记、市长", "current_org": "大石桥市人民政府",
     "source": "http://www.dsq.gov.cn/010/011001/011001001/leader.html (大石桥市长简历) + 盖州2024/2025分工文件与河长公示 (原盖州市委常委、常务副市长)；2025-12 大石桥市委常委会任代市长"},
    {"id": 21, "name": "张杨", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "（交流）营口市站前区委书记", "current_org": "中国共产党营口市站前区委员会",
     "source": "参照 data/provinces/liaoning/persons/20260806-辽宁省-营口市-区委书记-张杨.json + 2021-07-10 干部大会 (任盖州市委副书记，不再任宣传部长)"},
    {"id": 22, "name": "孙雨", "gender": "待确认", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "（营口市领导）", "current_org": "中共营口市委",
     "source": "2021-07-10 干部大会 (当时任营口市委常委、组织部部长，宣布任免)"},
    # ── 更早前任（2013-2017）与跨区交流 ──
    {"id": 23, "name": "班耀康", "gender": "男", "ethnicity": "待确认", "birth": "1957-01", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "（前任）市委书记", "current_org": "中国共产党盖州市委员会",
     "source": "2013-06 任前公示 (营口北海新区党工委副书记/管委会主任、盖州市委副书记(兼)拟任盖州市委书记) + 2015 北海新区新闻 (兼党工委书记)"},
    {"id": 24, "name": "王庆珂", "gender": "男", "ethnicity": "待确认", "birth": "1957-09", "birthplace": "",
     "education": "中央党校大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "（前前任）市委书记", "current_org": "中国共产党盖州市委员会",
     "source": "2013-06 任前公示 (盖州市委书记、北海新区/仙人岛党工委书记拟任盘锦市委常委)"},
    {"id": 25, "name": "朱文铎", "gender": "男", "ethnicity": "汉族", "birth": "1961-10", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "（前任）市长（已被查）", "current_org": "盖州市人民政府",
     "source": "营口市纪委监委通报 (2024-09 开除党籍公职；老边区委常委/常务副区长→盖州市委副书记/市长2016-2017→营口市交通局长) + twwiki 百科"},
    {"id": 26, "name": "赵国栋", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "（前任）市长、北海新区党工委书记", "current_org": "盖州市人民政府",
     "source": "2013-2015 盖州政府工作报告/北海新区新闻 (代市长2013→市长2014-2015)"},
    {"id": 27, "name": "曹德强", "gender": "男", "ethnicity": "待确认", "birth": "1972-02", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "（交流）营口市西市区委书记", "current_org": "中国共产党营口市西市区委员会",
     "source": "营口市委组织部2022第28号/2024第17号公示 (盖州组织部长→副书记) + 2026年省公示 (拟任县（市、区）委书记；营口市委社会工作部部长→西市区委书记)"},
    {"id": 28, "name": "王锐", "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "（交流）营口市工业和信息化局局长", "current_org": "营口市工业和信息化局",
     "source": "2021-07-10 干部大会 (任盖州市委委员、常委，提名为副市长人选) + 营口市人大(2026-03 任命为市工信局局长)"},
    {"id": 29, "name": "关盛鑫", "gender": "女", "ethnicity": "待确认", "birth": "1970-11", "birthplace": "",
     "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "（前任）市委常委、统战部部长", "current_org": "中国共产党盖州市委员会",
     "source": "营口市委组织部2022第28号公示 (盖州市政协党组副书记、副主席拟任县（市）区委常委) + 2025-10 河长公示 (市委统战部长) + 2026年第6号公示 (拟提名县（市）区政协主席候选人)"},
]

organizations = [
    {"id": 1, "name": "中国共产党盖州市委员会", "type": "党委", "level": "县处级(县级市)", "parent": "中共营口市委", "location": "辽宁省营口市盖州市"},
    {"id": 2, "name": "盖州市人民政府", "type": "政府", "level": "县处级", "parent": "营口市人民政府", "location": "辽宁省营口市盖州市"},
    {"id": 3, "name": "盖州市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "盖州市", "location": "辽宁省营口市盖州市"},
    {"id": 4, "name": "中国人民政治协商会议盖州市委员会", "type": "政协", "level": "县处级", "parent": "盖州市", "location": "辽宁省营口市盖州市"},
    {"id": 5, "name": "中国共产党盖州市纪律检查委员会/盖州市监察委员会", "type": "纪委", "level": "县处级", "parent": "中共营口市纪委", "location": "辽宁省营口市盖州市"},
    {"id": 6, "name": "盖州市公安局", "type": "政府", "level": "县处级", "parent": "盖州市人民政府", "location": "辽宁省营口市盖州市"},
    {"id": 7, "name": "盖州市人武部", "type": "党委", "level": "县处级", "parent": "营口军分区", "location": "辽宁省营口市盖州市"},
    {"id": 8, "name": "中国共产党营口市委员会", "type": "党委", "level": "地厅级", "parent": "中共辽宁省委", "location": "辽宁省营口市"},
    {"id": 9, "name": "营口市人民政府", "type": "政府", "level": "地厅级", "parent": "辽宁省人民政府", "location": "辽宁省营口市"},
    {"id": 10, "name": "中国共产党辽阳县委员会", "type": "党委", "level": "县处级", "parent": "中共辽阳市委", "location": "辽宁省辽阳市辽阳县"},
    {"id": 11, "name": "大石桥市人民政府", "type": "政府", "level": "县处级", "parent": "营口市人民政府", "location": "辽宁省营口市大石桥市"},
    {"id": 12, "name": "中国共产党营口市站前区委员会", "type": "党委", "level": "县处级", "parent": "中共营口市委", "location": "辽宁省营口市站前区"},
    {"id": 13, "name": "营口盖州市北海经济开发区管委会", "type": "开发区", "level": "县处级", "parent": "营口市人民政府", "location": "辽宁省营口市盖州市"},
    {"id": 14, "name": "营口盖州市仙人岛经济开发区管委会", "type": "开发区", "level": "县处级", "parent": "营口市人民政府", "location": "辽宁省营口市盖州市"},
    {"id": 15, "name": "中国人民政治协商会议营口市委员会", "type": "政协", "level": "地厅级", "parent": "政协辽宁省委员会", "location": "辽宁省营口市"},
    {"id": 16, "name": "中国共产党营口市西市区委员会", "type": "党委", "level": "县处级", "parent": "中共营口市委", "location": "辽宁省营口市西市区"},
    {"id": 17, "name": "营口市工业和信息化局", "type": "政府", "level": "地厅级部门", "parent": "营口市人民政府", "location": "辽宁省营口市"},
    {"id": 18, "name": "中国共产党辽阳县纪律检查委员会/辽阳县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共辽阳市纪委", "location": "辽宁省辽阳市辽阳县"},
    {"id": 19, "name": "营口（鲅鱼圈）经济技术开发区管委会", "type": "开发区", "level": "国家级", "parent": "营口市人民政府", "location": "辽宁省营口市鲅鱼圈区"},
    {"id": 20, "name": "营口市交通运输局", "type": "政府", "level": "地厅级部门", "parent": "营口市人民政府", "location": "辽宁省营口市"},
    {"id": 21, "name": "老边区人民政府", "type": "政府", "level": "县处级", "parent": "营口市人民政府", "location": "辽宁省营口市老边区"},
    {"id": 22, "name": "西市区人民政府", "type": "政府", "level": "县处级", "parent": "营口市人民政府", "location": "辽宁省营口市西市区"},
]

positions = [
    # 李典阁(1) 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2026-05(约)", "end_date": "present", "rank": "县处级正职(副厅级常规)",
     "note": "辽宁省管干部任前公示(2025年第5号)后由辽阳县委副书记、县长调任；2026-05-24 首次以书记身份主持市委常委会；2026-07-22/24 主持市第八次党代会；2026-07-24 八届一次全会当选八届市委书记"},
    {"person_id": 1, "org_id": 10, "title": "县委书记", "start_date": "~2025-06/07", "end_date": "~2026-02/05", "rank": "县处级正职",
     "note": "2025-06-10 任前公示拟任县（市、区）委书记；2025-07-17 辽阳县十七届人大五次会议党员大会以县委书记身份出席；2025-08-18 调研；2025-12-03 赴浪莎考察"},
    {"person_id": 1, "org_id": 10, "title": "县委副书记、县长", "start_date": "~2022-04", "end_date": "~2025-06", "rank": "县处级正职",
     "note": "2022-04 起任辽阳县副县长、代理县长；2022-12-21 十七届人大二次会议作政府工作报告（代县长）；2023 起以县长身份见报；2024-12-18 十七届人大四次会议作报告"},
    {"person_id": 1, "org_id": 18, "title": "县纪委书记、监委主任", "start_date": "≤2019-11", "end_date": "2022-04", "rank": "县处级副职",
     "note": "2019-11-01 中央纪委国家监委网站：辽阳县纪委书记、监委主任李典阁（15乡镇立案93件）；约2021年以辽阳县纪委书记接受采访（贯彻辽阳市12次党代会精神）"},
    # 袁世君(2) 市长
    {"person_id": 2, "org_id": 2, "title": "市政府党组书记、市长", "start_date": "2021-07(提名)", "end_date": "present", "rank": "县处级正职",
     "note": "主持市政府全面工作，负责审计方面工作，分管审计局（官网简历）；2025-12-29 盖州市八届人大五次会议上作2025年政府工作报告；2026-07-24 连任八届市委副书记"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2021-07", "end_date": "present", "rank": "县处级正职", "note": "市长兼任；2021-07-10 干部大会提名市长候选人；2021-12-08 八届人大一次会议选举为市长"},
    {"person_id": 2, "org_id": 22, "title": "（前职待核）", "start_date": "unknown", "end_date": "2021-07", "rank": "",
     "note": "2021 年前履历未公开（1978-05生、研究生/工程硕士）；仅确认最晚 2018-04 起任大石桥市副市长，约2019-2020 调任盖州市委副书记；任市长前任职待核（详见 person JSON open_questions）"},
    # 张鑫煜(3) 专职副书记
    {"person_id": 3, "org_id": 1, "title": "市委副书记（专职）", "start_date": "2025-07(约)", "end_date": "present", "rank": "县处级",
     "note": "2025-07-14 营口市委组织部公示：市公安局党委委员、政治部主任、二级高级警长拟任县（市）区委副书记；2026-02-28 高质量发展推进会主持；2026-07-24 八届一次全会当选副书记；2026-03 兼市关工委主任"},
    {"person_id": 3, "org_id": 8, "title": "营口市公安局党委委员、政治部主任（原职）", "start_date": "未知", "end_date": "~2025-07", "rank": "副县级",
     "note": "二级高级警长；任前公示所载原职"},
    # 李维(4) 常务副市长
    {"person_id": 4, "org_id": 2, "title": "市委常委、市政府党组副书记、常务副市长", "start_date": "~2026", "end_date": "present", "rank": "县处级副职",
     "note": "负责政府常务工作（官网简历）；2026-06-18 三级河长公示副总河长；2026-06-01 陪同李典阁检查矿山安全"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "~2026", "end_date": "present", "rank": "县处级", "note": "八届一次全会常委"},
    {"person_id": 4, "org_id": 13, "title": "北海经开区党工委书记、管委会主任（原职）", "start_date": "~2023-2025", "end_date": "~2026", "rank": "县处级",
     "note": "百度百科：原任营口北海经开区党工委副书记、管委会主任（2023-08 拟任市属园区正职）；后转入盖州市政府任常务副市长（时序仍有冲突待核）"},
    # 王一震(5) 政法委书记
    {"person_id": 5, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "~2024-2025", "end_date": "present", "rank": "县处级",
     "note": "2024-11-28 分工调整不再任公安局长（曾为副市长/公安局长）；2024-04-22 任前公示拟任县（市）区委常委；2026-06-18 河长公示政法委书记；1998-08 参加工作，公安系统出身（明慧网线索，待官方复核）"},
    # 李悦(6) 组织部长
    {"person_id": 6, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "≤2023-12", "end_date": "present", "rank": "县处级",
     "note": "2023-12-27 营口市委组织部公示：市委巡察工作领导小组办公室副主任、四级高级监察官拟任县（市）区委常委；2025-04-09 巡察工作会议以组织部长宣布授权；2026-06-18 河长公示；八届一次全会常委"},
    # 葛鑫(7) 纪委书记
    {"person_id": 7, "org_id": 5, "title": "市委常委、市纪委书记、市监委主任", "start_date": "~2023-08", "end_date": "present", "rank": "县处级",
     "note": "原营口市纪委监委第一纪检监察室主任、四级高级监察官；2023-08 任前公示拟任县（市）区委常委、纪委书记；2026-01-26 市纪委七届六次全会主持；八届一次全会常委"},
    # 曲松楠(8) 宣传部长
    {"person_id": 8, "org_id": 1, "title": "市委常委、宣传部部长（兼市委教育工委书记）", "start_date": "~2023", "end_date": "present", "rank": "县处级",
     "note": "2026-06-18 河长公示宣传部部长；2025-05-20 以市委教育工委书记出席；2024-06 与作家交流（男性）；八届一次全会常委"},
    # 姜爽(9) 人武部长
    {"person_id": 9, "org_id": 7, "title": "市委常委、人武部部长", "start_date": "<=2026", "end_date": "present", "rank": "县处级",
     "note": "2026-01-28 市人武部党委（扩大）会议以人武部党委副书记、部长讲话；八届一次全会常委；军队干部履历未公开"},
    # 李静波(10) 统战部长
    {"person_id": 10, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "~2026", "end_date": "present", "rank": "县处级",
     "note": "2026年第6号任前公示：西市区副区长拟任县（市）区委常委；2026-06-18 河长公示统战部长；八届一次全会常委"},
    {"person_id": 10, "org_id": 22, "title": "营口市西市区副区长（原职）", "start_date": "~2024-08", "end_date": "~2026", "rank": "县处级副职",
     "note": "2024-08 任前公示：西市区得胜街道党工委书记拟提名副区长"},
    # 梁迅峥(11) 副市长/常委
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "<=2026", "end_date": "present", "rank": "县处级副职",
     "note": "负责工业信息化、交通、生态环境（官网简历）；2026-06-18 河长公示副市长"},
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start_date": "2026-07", "end_date": "present", "rank": "县处级", "note": "八届一次全会常委"},
    # 邵凤江(12) 公安局长/副市长
    {"person_id": 12, "org_id": 6, "title": "市公安局局长", "start_date": "~2024-2025", "end_date": "present", "rank": "县处级",
     "note": "2024-11-28 分工调整后负责公安等（接替王一震）；官网简历"},
    {"person_id": 12, "org_id": 2, "title": "副市长、市政府党组成员", "start_date": "~2024-2025", "end_date": "present", "rank": "县处级副职", "note": "官网简历"},
    # 蒋存祺(13) 副市长
    {"person_id": 13, "org_id": 2, "title": "副市长、市政府党组成员", "start_date": "~2025-2026", "end_date": "present", "rank": "县处级副职",
     "note": "负责农业农村、水利（官网简历）；2025-10 河长公示曾为青石岭镇党委书记——乡镇主官提拔入市府"},
    # 邹艳丽(14) 副市长
    {"person_id": 14, "org_id": 2, "title": "副市长、市政府党组成员", "start_date": "~2026", "end_date": "present", "rank": "县处级副职",
     "note": "负责教育、卫健（官网简历）；2025-10 河长公示曾为二台乡党委书记——乡镇主官提拔"},
    # 李瀚霖(15) 政府党组成员
    {"person_id": 15, "org_id": 2, "title": "市政府党组成员", "start_date": "<=2026", "end_date": "present", "rank": "县处级",
     "note": "2026-06-18 河长公示政府党组成员/河长；2026-06-08 安全生产防汛会议出席"},
    # 董伟(16) 人大主任
    {"person_id": 16, "org_id": 3, "title": "市人大常委会党组书记、主任", "start_date": "2025-12-31", "end_date": "present", "rank": "县处级正职",
     "note": "2025-07-14 公示：营口市人大常委会人事选举委员会主任委员拟任盖州人大主任；2025-08-19 任盖州市人大党组书记、主任候选人；2025-12-31 市八届人大五次会议补选为主任"},
    # 吕永祥(17) 政协主席
    {"person_id": 17, "org_id": 4, "title": "市政协党组书记、主席", "start_date": "2025-12-29", "end_date": "present", "rank": "县处级正职",
     "note": "2025-06-13 公示拟提名政协主席候选人；2025-12-29 政协八届五次会议任党组书记/主席候选人并作常委会报告；2026 以市政协主席出席"},
    {"person_id": 17, "org_id": 1, "title": "市委副书记", "start_date": "2024-04", "end_date": "~2025-06", "rank": "县处级",
     "note": "2024-04-22 公示：盖州市人大常委会党组副书记、副主任 拟任县（市）区委副书记；2024-12 以市委副书记参加政协党员委员大会；兼市委国安办主任"},
    # 徐海龙(18) 前任书记
    {"person_id": 18, "org_id": 1, "title": "市委书记", "start_date": "2021-07", "end_date": "~2026", "rank": "县处级正职",
     "note": "2021-07-10 干部大会由市长转任书记；2026-01/02 纪委全会、民主生活会、高质量发展推进会仍为书记；2026 上半年卸任调离（去向待核）"},
    {"person_id": 18, "org_id": 2, "title": "市长", "start_date": "~2017-12", "end_date": "2021-07", "rank": "县处级正职",
     "note": "2017年底市七届人大一次会议选举为市长；2018/2019/2021 政府工作报告署市长；2021-07-10 不再担任市长"},
    {"person_id": 18, "org_id": 12, "title": "（前职）盖州市委常委/常务副市长/市委副书记、代市长", "start_date": "~2016", "end_date": "~2017", "rank": "县处级",
     "note": "百度百科：大石桥市（乡镇/园区/常委）→ 2016 年调盖州，任常委/副市长人选→常务副市长→副书记、代市长；2021-07 称在盖州工作5年"},
    # 吴峰(19) 前任书记/现营口市政协秘书长
    {"person_id": 19, "org_id": 1, "title": "市委书记", "start_date": "2017-10", "end_date": "2021-07", "rank": "县处级正职",
     "note": "2017-09 省委公示：仙人岛能源化工区党工委副书记、管委会常务副主任拟任盖州市委书记；2017-10-10 到任；2021-07-10 免职"},
    {"person_id": 19, "org_id": 15, "title": "市政协党组成员、秘书长（现任）", "start_date": "~2021-2022", "end_date": "present", "rank": "地厅级部门",
     "note": "2022-12-13 营口市政协调补委员；现任营口市政协党组成员、秘书长、办公室主任"},
    # 衣冠鹏(20) 大石桥市长（交流）
    {"person_id": 20, "org_id": 11, "title": "大石桥市委副书记、市政府党组书记、市长", "start_date": "2025-12(代)", "end_date": "present", "rank": "县处级正职",
     "note": "2025-12-11 大石桥市委常委会公开以市委副书记/市政府党组书记/副市长/代市长身份；2026-04 起以市长见报；参照大石桥市调查"},
    {"person_id": 20, "org_id": 2, "title": "盖州市委常委、常务副市长/市政府党组副书记、副市长", "start_date": "~2021-2024", "end_date": "~2025-12", "rank": "县处级副职",
     "note": "2024 分工文件为市政府党组副书记、副市长；2025-10 河长公示为市委常委、常务副市长——盖州→大石桥市跨县(市)交流"},
    # 张杨(21) 站前区委书记（交流）
    {"person_id": 21, "org_id": 12, "title": "营口市站前区委书记", "start_date": "~2022-2026", "end_date": "present", "rank": "县处级正职",
     "note": "参照 2026-08-06 站前区调查"},
    {"person_id": 21, "org_id": 1, "title": "盖州市委副书记", "start_date": "2021-07", "end_date": "~2022", "rank": "县处级",
     "note": "2021-07-10 干部大会任市委副书记（不再任宣传部长）；随后交流至站前区任区委书记"},
    # 孙雨(22) 营口市领导
    {"person_id": 22, "org_id": 8, "title": "营口市委常委、组织部部长", "start_date": "<=2021", "end_date": "unknown", "rank": "地厅级副职",
     "note": "2021-07-10 出席盖州干部大会宣布省委/营口市委任免"},
    # 班耀康(23) 前任书记
    {"person_id": 23, "org_id": 1, "title": "市委书记", "start_date": "2013-07", "end_date": "2017-10", "rank": "县处级正职",
     "note": "2013-06 任前公示：营口北海新区党工委副书记/管委会主任、盖州市委副书记(兼)拟任盖州市委书记；兼北海新区党工委书记；1957-01生、2017 卸任时 60 岁，疑到龄转岗/退休"},
    # 王庆珂(24) 前前任书记
    {"person_id": 24, "org_id": 1, "title": "市委书记", "start_date": "~2011-2013", "end_date": "~2013-07", "rank": "县处级正职（副市级）",
     "note": "2013-06 任前公示：盖州市委书记兼北海新区/仙人岛党工委书记拟任盘锦市委常委；1957-09生"},
    # 朱文铎(25) 前任市长（已被查）
    {"person_id": 25, "org_id": 2, "title": "市长", "start_date": "2016-01", "end_date": "2017-03", "rank": "县处级正职",
     "note": "2016-01 盖州市代市长→市长；2017-03 调任营口市交通（运输）局党组书记、局长；2024-09 被查双开（营口市纪委监委通报）"},
    {"person_id": 25, "org_id": 21, "title": "老边区委常委、常务副区长（原职）", "start_date": "未知", "end_date": "~2015", "rank": "县处级副职", "note": "纪委通报所载此前职务"},
    # 赵国栋(26) 前任市长
    {"person_id": 26, "org_id": 2, "title": "市长", "start_date": "2013(代)/2014", "end_date": "~2015", "rank": "县处级正职",
     "note": "2013 代市长→2014 市长；兼北海新区党工委书记；2015 年在任；去向后待核"},
    # 曹德强(27) 交流
    {"person_id": 27, "org_id": 16, "title": "营口市西市区委书记（现任）", "start_date": "~2026", "end_date": "present", "rank": "县处级正职",
     "note": "2026-01-09 省公示：营口市委社会工作部部长拟任县（市、区）委书记；沿海产业基地官网2026-04 载为西市区委书记"},
    {"person_id": 27, "org_id": 1, "title": "盖州市委副书记", "start_date": "~2022", "end_date": "~2024", "rank": "县处级",
     "note": "营口市委组织部2022第28号公示：盖州市委常委、组织部部长拟任县（市）区委副书记 → 后就任盖州市委副书记；2024-04 公示拟任市直部门正职→营口市委社会工作部部长"},
    # 王锐(28) 交流
    {"person_id": 28, "org_id": 17, "title": "营口市工业和信息化局局长（现任）", "start_date": "2026-03", "end_date": "present", "rank": "地厅级部门",
     "note": "2026-03 营口市人大任命为市工业和信息化局局长"},
    {"person_id": 28, "org_id": 1, "title": "盖州市委委员、常委，副市长（原职）", "start_date": "2021-07", "end_date": "~2026", "rank": "县处级",
     "note": "2021-07-10 干部大会任盖州市委委员、常委，提名为副市长人选（党政交叉任职）"},
    # 关盛鑫(29) 前任统战部长
    {"person_id": 29, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "~2021-2022", "end_date": "~2026", "rank": "县处级",
     "note": "2022 第28号公示：盖州市政协党组副书记、副主席拟任县（市）区委常委→任统战部长；2025-10 河长公示仍为统战部长；2026 第6号公示拟提名县（市）区政协主席候选人（去向：转任厅/退休待核）"},
]

relationships = [
    # 核心党政搭档
    {"person_a": 1, "person_b": 2, "type": "co_leadership", "context": "市委书记（李典阁）与市长（袁世君，兼市委副书记）——党政一把手搭班",
     "overlap_org": "盖州市", "overlap_period": "2026-", "confidence": "confirmed"},
    # 市委班子核心
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记与专职副书记（八届班子；2026-07-24 同届当选）",
     "overlap_org": "盖州市委", "overlap_period": "2026-07-", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "书记与常务副市长（八届常委；2026-06-01 矿山安全督导同行）",
     "overlap_org": "盖州市委", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "书记与组织部部长（党建、选人用人、换届）",
     "overlap_org": "盖州市委组织部", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "书记与纪委书记（全面从严治党、党风廉政建设）",
     "overlap_org": "盖州市纪委监委", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "书记与宣传部长（意识形态）",
     "overlap_org": "盖州市委", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "co_leadership", "context": "书记与常委/副市长（八届班子）",
     "overlap_org": "盖州市委", "overlap_period": "2026-07-", "confidence": "confirmed"},
    # 政府班子
    {"person_a": 2, "person_b": 4, "type": "co_leadership", "context": "市长与常务副市长（政府班子）",
     "overlap_org": "盖州市人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长与公安局长/副市长（公安、社会稳定）",
     "overlap_org": "盖州市人民政府", "overlap_period": "~2025-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "co_leadership", "context": "市长与副市长（政府班子）",
     "overlap_org": "盖州市人民政府", "overlap_period": "~2025-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "co_leadership", "context": "市长与副市长（政府班子）",
     "overlap_org": "盖州市人民政府", "overlap_period": "~2026-", "confidence": "confirmed"},
    # 四大班子
    {"person_a": 1, "person_b": 16, "type": "co_leadership", "context": "书记与市人大常委会主任（常委会扩大会议同台）",
     "overlap_org": "盖州市", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 17, "type": "co_leadership", "context": "书记与市政协主席（常委会扩大会议同台）",
     "overlap_org": "盖州市", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "co_leadership", "context": "市长与市人大主任", "overlap_org": "盖州市", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 17, "type": "co_leadership", "context": "市长与市政协主席", "overlap_org": "盖州市", "overlap_period": "2026-", "confidence": "confirmed"},
    # 前任/继任链条
    {"person_a": 18, "person_b": 1, "type": "predecessor_successor", "context": "徐海龙卸任盖州市委书记 → 李典阁接任（2026 上半年）",
     "overlap_org": "盖州市委", "overlap_period": "2021-2026", "confidence": "confirmed"},
    {"person_a": 19, "person_b": 18, "type": "predecessor_successor", "context": "吴峰卸任盖州市委书记 → 徐海龙由市长接任（2021-07-10）",
     "overlap_org": "盖州市委", "overlap_period": "2021-07", "confidence": "confirmed"},
    {"person_a": 18, "person_b": 2, "type": "predecessor_successor", "context": "徐海龙由市长转任书记，袁世君接任市长（2021-07-10）",
     "overlap_org": "盖州市人民政府", "overlap_period": "2021-07", "confidence": "confirmed"},
    # 跨县（市）交流
    {"person_a": 1, "person_b": 20, "type": "同系统", "context": "李典阁（辽阳县县长→盖州书记）与衣冠鹏（盖州常务副市长→大石桥市长）——营口/辽阳体系内干部流动",
     "overlap_org": "盖州市", "overlap_period": "2025-2026", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 20, "type": "predecessor_successor", "context": "衣冠鹏曾任盖州市委常委、常务副市长（袁世君政府班子成员），后调任大石桥市长",
     "overlap_org": "盖州市人民政府", "overlap_period": "~2021-2026", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 21, "type": "co_leadership", "context": "张杨曾任盖州市委副书记（2021-2022 与市长同班子），后交流至站前区委书记",
     "overlap_org": "盖州市委", "overlap_period": "2021-2022", "confidence": "confirmed"},
    {"person_a": 18, "person_b": 22, "type": "superior_subordinate", "context": "孙雨（营口市委常委/组织部长）2021-07 宣布徐海龙任免（上级组织部门）",
     "overlap_org": "中共营口市委", "overlap_period": "2021-07", "confidence": "confirmed"},
    # 乡镇提拔入市府
    {"person_a": 13, "person_b": 14, "type": "同系统", "context": "蒋存祺（青石岭镇党委书记）与邹艳丽（二台乡党委书记）先后由乡镇主官提拔入市政府",
     "overlap_org": "盖州市人民政府", "overlap_period": "2025-2026", "confidence": "confirmed"},
    # 更早代际交接（2013-2021）
    {"person_a": 24, "person_b": 23, "type": "predecessor_successor", "context": "王庆珂卸任盖州市委书记（2013-06 公示拟任盘锦市委常委）→ 班耀康接任（2013-07）",
     "overlap_org": "盖州市委", "overlap_period": "2013", "confidence": "confirmed"},
    {"person_a": 23, "person_b": 19, "type": "predecessor_successor", "context": "班耀康卸任（2017-10，60岁疑到龄）→ 吴峰接任盖州市委书记",
     "overlap_org": "盖州市委", "overlap_period": "2017-10", "confidence": "confirmed"},
    {"person_a": 26, "person_b": 25, "type": "predecessor_successor", "context": "赵国栋（市长约2013-2015）→ 朱文铎（2016-01 代市长/市长）",
     "overlap_org": "盖州市人民政府", "overlap_period": "2015-2016", "confidence": "confirmed"},
    {"person_a": 25, "person_b": 18, "type": "predecessor_successor", "context": "朱文铎调任营口市交通局长（2017-03，后被查双开）→ 徐海龙接任市长（2017-12 选举）",
     "overlap_org": "盖州市人民政府", "overlap_period": "2017", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 27, "type": "同系统", "context": "曹德强曾任盖州市委常委/组织部长→副书记（2022-2024），后经营口市委社会工作部部长任西市区委书记（2026 省公示）——盖州干部外溢",
     "overlap_org": "盖州市委", "overlap_period": "2022-2024", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 28, "type": "co_leadership", "context": "王锐曾任盖州市委常委/副市长（2021-07 起，与市长同班子），2026-03 调任营口市工信局局长",
     "overlap_org": "盖州市人民政府", "overlap_period": "2021-2026", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 29, "type": "co_leadership", "context": "关盛鑫曾任盖州市委常委、统战部长（政协调动/班子内会议），2026 拟提名县（市）区政协主席候选人",
     "overlap_org": "盖州市委", "overlap_period": "~2022-2026", "confidence": "confirmed"},
    {"person_a": 19, "person_b": 25, "type": "同系统", "context": "吴峰（2017-10 任盖州书记）、朱文铎（2016 任盖州市长）先后由园区/区县调入盖州领导层——营口园区/县区干部汇聚盖州",
     "overlap_org": "盖州市", "overlap_period": "2016-2017", "confidence": "confirmed"},
]


# ── Person JSONs ────────────────────────────────────────────────────────
def write_person_jsons():
    """Write per-person graph JSON for core leaders (市委书记 & 市长)."""

    li = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "营口市", "region": "盖州市",
                                "job": "市委书记", "task_id": "liaoning_盖州市", "time_focus": "2025-2026"},
        "identity": {
            "person_id": "yingkou_gaizhou_lidiange",
            "name": "李典阁",
            "aliases": [],
            "gender": "男", "ethnicity": "汉族", "birth": "1975-02", "birthplace": "", "native_place": "",
            "education": [
                {"period": "", "institution": "待查（大学学历、硕士学位）", "major": "", "degree": "硕士（最终）", "study_type": "unknown", "source_ids": ["S001"]}
            ],
            "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "李典阁_1975-02", "name_birthplace": "李典阁_unknown",
                            "official_profile_url": "https://www.ln.gov.cn/web/ywdt/jrln/wzxx2018/2025060919443373914/index.shtml"},
        },
        "current_status": {"current_post": "市委书记", "current_org": "中国共产党盖州市委员会",
                           "administrative_rank": "县处级正职(副厅级常规)", "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S002", "S003", "S004"]},
        "career_timeline": [
            {"start": "2026-05(约)", "end": "present", "org": "中共盖州市委员会", "title": "市委书记",
             "level": "县处级", "location": "盖州市", "system": "party", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "2026-05-24 首次以书记身份主持市委常委会；2026-07-22/24 主持市第八次党代会；2026-07-24 八届一次全会当选八届市委书记",
             "confidence": "confirmed", "source_ids": ["S002", "S003", "S004"]},
            {"start": "~2025-06/07", "end": "~2026-02/05", "org": "中共辽阳县委", "title": "县委书记",
             "level": "县处级", "location": "辽阳市辽阳县", "system": "party", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "2025-06-10 辽宁省管干部任前公示（2025年第5号）拟任县（市、区）委书记；2025-07-17 辽阳县十七届人大五次会议党员大会以县委书记身份出席；2025-08-18 调研重点项目；2025-12-03 赴浪莎集团考察",
             "confidence": "confirmed", "source_ids": ["S001", "S009"]},
            {"start": "2022-04(约)", "end": "~2025-06", "org": "辽阳县人民政府", "title": "县长（代理县长→县长；兼县委副书记）",
             "level": "县处级", "location": "辽阳市辽阳县", "system": "government", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "2022-04 起任辽阳县副县长、代理县长（辽阳县第十七届人大常委会第二次会议任命）；2022-12-21 十七届人大二次会议作政府工作报告（代县长）；2023 起以县长身份见报；2024-12-18 十七届人大四次会议作政府工作报告",
             "confidence": "confirmed", "source_ids": ["S001", "S006"]},
            {"start": "≤2019-11", "end": "2022-04", "org": "辽阳县纪委监委", "title": "县委常委、纪委书记、监委主任",
             "level": "县处级副职", "location": "辽阳市辽阳县", "system": "discipline", "rank": "县处级副职", "is_key_promotion": False,
             "notes": "2019-11-01 中央纪委国家监委网站刊文：辽阳县纪委书记、监委主任李典阁（全县15个乡镇立案93件）；约2021年以辽阳县纪委书记接受采访谈贯彻辽阳市第十二次党代会和纪委十二届一次全会精神",
             "confidence": "confirmed", "source_ids": ["S007", "S008"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任辽阳县纪委书记之前的更早履历（出生地、院校专业、入党时间、参加工作年份、此前职务）公开资料未检索到；确有同名'李典阁'（1975-10生、辽阳市公安局政治部干部科）词条为不同人，勿混淆",
             "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"name": "中国共产党盖州市委员会", "role": "市委书记"}],
        "relationships": [
            {"person": "袁世君", "person_id": "yingkou_gaizhou_yuanshijun", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任搭班：市委书记+市长（兼市委副书记）", "overlap_org": "盖州市",
             "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"person": "张鑫煜", "person_id": "yingkou_gaizhou_zhangxinyu", "relationship_type": "superior_subordinate",
             "strength": "strong", "evidence": "八届市委副书记（专职）", "overlap_org": "盖州市委",
             "overlap_period": "2026-07-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
            {"person": "徐海龙", "person_id": "yingkou_gaizhou_xuhailong", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "前任盖州市委书记（2021-2026），李典阁2026年接任", "overlap_org": "盖州市委",
             "overlap_period": "2026", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S005"]},
            {"person": "衣冠鹏", "person_id": "yingkou_dashiqiao_yiguanpeng", "relationship_type": "same_system",
             "strength": "medium", "evidence": "衣冠鹏原盖州常务副市长调任大石桥市长——营口内县级市干部流动；李典阁自辽阳调盖州（跨市交流）",
             "overlap_org": "盖州市", "overlap_period": "2025-2026", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
        ],
        "governance_record": [
            {"period": "2026-07", "domain": "party_building", "achievement_or_event": "主持市第八次党代会与八届一次全会，部署未来五年任务与全面从严治党、政治建设",
             "role_in_event": "市委书记", "measurable_outcome": "", "location": "盖州市",
             "confidence": "confirmed", "source_ids": ["S003", "S004"]},
            {"period": "2026-05", "domain": "public_security", "achievement_or_event": "主持市委常委会研究安全生产、矿山整治、生态环保督察整改、信访维稳",
             "role_in_event": "市委书记", "measurable_outcome": "", "location": "盖州市",
             "confidence": "confirmed", "source_ids": ["S002"]},
            {"period": "2026-06", "domain": "rural_revitalization", "achievement_or_event": "督导人居环境整治（巴岭村、垃圾填埋场）；调研企业运行与产业发展（耐火材料、蛋鸡养殖）；检查矿山安全（双台/徐屯）",
             "role_in_event": "市委书记", "measurable_outcome": "", "location": "盖州市",
             "confidence": "confirmed", "source_ids": ["S011"]},
        ],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "cross_county_rotation", "systems_experience": ["discipline", "government", "party"],
            "geographic_pattern": ["辽阳市辽阳县", "营口市盖州市"],
            "promotion_velocity": {"summary": "县纪委书记→县长→县委书记（跨市提拔），任前公示2025年第5号", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "grassroots_oriented", "evidence": "到任后密集下乡调研（人居环境、矿山、企业），强调问题整改'后半篇文章'", "confidence": "plausible", "source_ids": ["S011"]},
                {"trait": "pragmatic", "evidence": "强调项目牵引、实绩实效、招大引强（政府工作报告与会议讲话）", "confidence": "plausible", "source_ids": ["S002", "S010"]},
            ],
            "speech_themes": ["高质量发展", "振兴发展", "全面从严治党", "政治建设", "民生实事"],
            "management_signals": ["强调'问题导向、目标导向'", "实施'硬封堵+智监管'"],
            "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026-08-12 未发现违纪或负面舆情记录", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "辽宁省管干部任前公示（2025年第5号）", "url": "https://www.ln.gov.cn/web/ywdt/jrln/wzxx2018/2025060919443373914/index.shtml",
             "publisher": "中共辽宁省委组织部", "published_at": "2025-06", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high",
             "notes": "李典阁：男，汉族，1975年2月生，大学学历、硕士学位，中共党员，现任辽阳县委副书记、县长，拟任县（市、区）委书记"},
            {"id": "S002", "title": "市委常委会召开会议(2026-05-24)", "url": "http://www.gaizhou.gov.cn/003/003003/20260525/3412175c-c36c-4847-b8d1-178fab41d15e.html",
             "publisher": "盖州市融媒体中心", "published_at": "2026-05-25", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "李典阁首次以市委书记身份主持市委常委会"},
            {"id": "S003", "title": "中国共产党盖州市第八次代表大会胜利闭幕", "url": "http://www.gaizhou.gov.cn/003/003004/20260724/b3aa846a-16ca-4387-aac0-4d5713b4be11.html",
             "publisher": "盖事辰州/盖州市政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "李典阁主持第八次党代会并作总结讲话"},
            {"id": "S004", "title": "中国共产党盖州市第八届委员会举行第一次全体会议", "url": "http://www.gaizhou.gov.cn/003/003004/20260727/229a50f4-bc8c-407c-891c-96d13cf368ff.html",
             "publisher": "盖事辰州", "published_at": "2026-07-27", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "选举李典阁为八届市委书记；常委名单"},
            {"id": "S005", "title": "盖州市高质量发展推进会议(2026-02-28)", "url": "http://www.gaizhou.gov.cn/003/003004/20260302/0f25be7c-135d-484b-a6bf-28af200d578b.html",
             "publisher": "盖州市融媒体中心", "published_at": "2026-03-02", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "徐海龙以市委书记讲话（其为前任，李典阁接任）"},
            {"id": "S006", "title": "大石桥市领导之窗/盖州2024-2025分工文件", "url": "data/provinces/liaoning/persons/20260806-辽宁省-营口市-市长-衣冠鹏.json",
             "publisher": "大石桥市/盖州市政府", "published_at": "2026-08-06", "accessed_at": AS_OF, "source_type": "database", "reliability": "high",
             "notes": "衣冠鹏现为大石桥市长（原盖州常务副市长）——营口内县级市干部流动佐证"},
            {"id": "S007", "title": "辽阳县纪委书记、监委主任（中央纪委国家监委网站）", "url": "https://www.bjsupervision.gov.cn/qfy/bmlf/201911/t20191101_66619.html",
             "publisher": "中央纪委国家监委网站/北京市纪委监委官网", "published_at": "2019-11-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "李典阁以辽阳县纪委书记、监委主任身份：全县15个乡镇立案93件"},
            {"id": "S008", "title": "辽阳县纪委书记李典阁访谈（壹读转载）", "url": "https://read01.com/QRPJDA.html",
             "publisher": "壹读/辽阳县", "published_at": "~2021", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium",
             "notes": "以辽阳县纪委书记身份谈贯彻辽阳市第十二次党代会及纪委十二届一次全会精神（时期与职务吻合）"},
            {"id": "S009", "title": "辽阳县第十七届人大五次会议（县委书记出席）", "url": "https://news.qq.com/rain/a/20250717A09BZC00",
             "publisher": "腾讯新闻转载县务报道", "published_at": "2025-07-17", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium",
             "notes": "李典阁以辽阳县委书记身份出席——到任窗口 2025-06-10 公示 ~ 2025-07-17"},
            {"id": "S010", "title": "盖州市委十五五规划建议", "url": "http://gaizhou.gov.cn/003/003003/20260108/def872c4-371b-49e6-80ae-7c3399496d77.html",
             "publisher": "盖州市委", "published_at": "2026-01-08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "十五五发展思路（农业强市、港产城融合、海洋经济）"},
            {"id": "S011", "title": "李典阁调研报道（人居环境/企业/矿山）", "url": "http://gaizhou.gov.cn/009/009001/20260616/92656c33-d8ec-4516-aa6a-47e840d9db58.html",
             "publisher": "盖州市融媒体中心", "published_at": "2026-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "书记调研风格与治理重点（人居环境、企业、矿山安全）"},
        ],
        "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "partial",
                               "relationship_confidence": "medium", "biggest_gap": "任辽阳县前的早期履历与具体出生地/院校"},
        "open_questions": [
            {"priority": "critical", "question": "李典阁出生年月口径（任前公示1975-02；个别来源1975-10/11）与籍贯、院校专业、入党/参加工作年份", "why_it_matters": "身份信息矛盾需校准",
             "suggested_queries": ["李典阁 辽阳 简历 1975", "李典阁 任前公示 完整"], "last_attempted": AS_OF},
            {"priority": "high", "question": "任辽阳县前的更早履历（乡镇/县委/市直）", "why_it_matters": "晋升路径与人际网络",
             "suggested_queries": ["李典阁 辽阳 县长 前 任职"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "何时正式到盖州任职（有2026-05-24任职记录，具体任免大会日期待核）", "why_it_matters": "精确到任时间",
             "suggested_queries": ["盖州 任免 李典阁 2026"], "last_attempted": AS_OF},
        ],
    }

    yuan = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "营口市", "region": "盖州市",
                                "job": "市长", "task_id": "liaoning_盖州市", "time_focus": "2021-2026"},
        "identity": {
            "person_id": "yingkou_gaizhou_yuanshijun",
            "name": "袁世君",
            "aliases": [],
            "gender": "男", "ethnicity": "汉族", "birth": "1978-05", "birthplace": "", "native_place": "",
            "education": [
                {"period": "", "institution": "待查（研究生学历、工程硕士学位）", "major": "", "degree": "工程硕士（最终）", "study_type": "unknown", "source_ids": ["S001"]}
            ],
            "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "袁世君_1978-05", "name_birthplace": "袁世君_unknown",
                            "official_profile_url": "http://www.gaizhou.gov.cn/ldzc/012001/012001001/leader.html"},
        },
        "current_status": {"current_post": "市委副书记、市政府党组书记、市长", "current_org": "盖州市人民政府",
                           "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S001", "S002", "S003"]},
        "career_timeline": [
            {"start": "2021-07(提名)", "end": "present", "org": "盖州市人民政府", "title": "市政府党组书记、市长",
             "level": "县处级", "location": "盖州市", "system": "government", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "2021-07-10 干部大会提名市长候选人后当选；主持市政府全面工作（官网简历）；2025-12-29 八届人大五次会议作政府工作报告；2026-07-24 连任八届市委副书记",
             "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
            {"start": "2021-07", "end": "present", "org": "中共盖州市委员会", "title": "市委副书记",
             "level": "县处级", "location": "盖州市", "system": "party", "rank": "县处级正职", "is_key_promotion": False,
             "notes": "市长党内职务；八届一次全会确认连任", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"start": "~2019-2020", "end": "2021-07", "org": "中共盖州市委员会", "title": "市委副书记（专职）",
             "level": "县处级", "location": "盖州市", "system": "party", "rank": "县处级", "is_key_promotion": True,
             "notes": "2020-06-12 央广网/北国网：中共盖州市委副书记袁世君为盖州特色农产品直播代言——最晚2020-06 已在任；2018-10 仍在任大石桥市副市长，调任盖州副书记区间约 2019-2020",
             "confidence": "plausible", "source_ids": ["S007", "S008"]},
            {"start": "~2017-12(最晚2018-04)", "end": "~2019-2020", "org": "大石桥市人民政府", "title": "副市长",
             "level": "县处级副职", "location": "营口市大石桥市", "system": "government", "rank": "县处级副职", "is_key_promotion": False,
             "notes": "2018 年多场大石桥官方新闻以副市长身份出席（环保/安全生产/镁产业/招商调度）；非常务副市长",
             "confidence": "confirmed", "source_ids": ["S009"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任大石桥副市长之前的更早履历（出生地、院校、入党时间、参加工作年份）公开资料未检索到",
             "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"name": "盖州市人民政府", "role": "市长"}],
        "relationships": [
            {"person": "李典阁", "person_id": "yingkou_gaizhou_lidiange", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任搭班：市长与市委书记", "overlap_org": "盖州市",
             "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"person": "徐海龙", "person_id": "yingkou_gaizhou_xuhailong", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "徐海龙由市长转书记，袁世君2021-07接任市长", "overlap_org": "盖州市人民政府",
             "overlap_period": "2021-07", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S004"]},
            {"person": "衣冠鹏", "person_id": "yingkou_dashiqiao_yiguanpeng", "relationship_type": "superior_subordinate",
             "strength": "medium", "evidence": "衣冠鹏曾任其政府班子常务副市长，后调任大石桥市长", "overlap_org": "盖州市人民政府",
             "overlap_period": "~2021-2026", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
            {"person": "张杨", "person_id": "yingkou_zhanqian_zhangyang", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "张杨2021-2022任盖州市委副书记（与市长同班子）", "overlap_org": "盖州市委",
             "overlap_period": "2021-2022", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        ],
        "governance_record": [
            {"period": "2025", "domain": "economic_development", "achievement_or_event": "2025年政府工作报告：地区生产总值约200亿元、财政预算收入预增141.6%、签约项目152个总投资409.5亿元、招商到位96.5亿元",
             "role_in_event": "市长（作报告）", "measurable_outcome": "GDP突破200亿", "location": "盖州市",
             "confidence": "confirmed", "source_ids": ["S006"]},
            {"period": "2025", "domain": "rural_revitalization", "achievement_or_event": "高标农田33.9万亩、'盖州葡萄''盖州西瓜'等5项国家地理标志；农业一产产值稳居营口首位",
             "role_in_event": "市长", "measurable_outcome": "", "location": "盖州市",
             "confidence": "confirmed", "source_ids": ["S006"]},
            {"period": "2025", "domain": "environment", "achievement_or_event": "中央环保督察22项、省级8项整改全部完成；大清河入选全国美丽河湖优秀案例；矿山修复6500亩",
             "role_in_event": "市长", "measurable_outcome": "", "location": "盖州市",
             "confidence": "confirmed", "source_ids": ["S006"]},
            {"period": "2025", "domain": "public_security", "achievement_or_event": "渔业安全'木改钢'35艘、拆解'三无'渔船442艘；194个废弃矿洞全部封堵",
             "role_in_event": "市长", "measurable_outcome": "", "location": "盖州市",
             "confidence": "confirmed", "source_ids": ["S006"]},
        ],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "local_ladder", "systems_experience": ["government", "party"],
            "geographic_pattern": [], "promotion_velocity": {"summary": "2021年任市长（时年43岁），现为县处级正职", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "pragmatic", "evidence": "政府工作报告强调'起步冲刺''项目为王'、招商、营商环境'最佳口碑县级市'目标", "confidence": "plausible", "source_ids": ["S006"]},
                {"trait": "stability_oriented", "evidence": "强调安全生产、社会稳定、债务风险化解", "confidence": "plausible", "source_ids": ["S006"]},
            ],
            "speech_themes": ["高质量发展", "项目建设", "乡村振兴", "营商环境", "民生保障"],
            "management_signals": ["'一表三图'项目调度", "零基预算改革", "'免申即享'服务"],
            "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026-08-12 未发现违纪或负面舆情记录", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "袁世君-盖州市人民政府(领导之窗)", "url": "http://www.gaizhou.gov.cn/ldzc/012001/012001001/leader.html",
             "publisher": "盖州市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "市长简历：男，汉族，1978年5月生，研究生学历、工程硕士学位，中共党员，现任市政府党组书记、市长"},
            {"id": "S002", "title": "八届一次全会", "url": "http://www.gaizhou.gov.cn/003/003004/20260727/229a50f4-bc8c-407c-891c-96d13cf368ff.html",
             "publisher": "盖事辰州", "published_at": "2026-07-27", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "袁世君连任八届市委副书记"},
            {"id": "S003", "title": "市委常委会(2026-05-24)", "url": "http://www.gaizhou.gov.cn/003/003003/20260525/3412175c-c36c-4847-b8d1-178fab41d15e.html",
             "publisher": "盖州市融媒体中心", "published_at": "2026-05-25", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "袁世君以市委副书记、市长作传达部署"},
            {"id": "S004", "title": "我市召开干部大会(2021-07-10)", "url": "http://www.gaizhou.gov.cn/003/003003/20210712/a2b2ee2f-17b8-4c58-8eec-d53ca4469416.html",
             "publisher": "盖州市政府办公室", "published_at": "2021-07-12", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "提名袁世君为市长候选人；徐海龙任书记；张杨副书记"},
            {"id": "S005", "title": "盖政办发〔2024〕1号市政府领导分工", "url": "http://www.gaizhou.gov.cn/govxxgk/gzs/2024-07-05/fefce566-d03a-46c9-90ef-6f67498b8c55.html",
             "publisher": "盖州市政府办公室", "published_at": "2024-07-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "袁世君主持全面工作；衣冠鹏党组副书记/副市长等"},
            {"id": "S006", "title": "盖州市2025年政府工作报告", "url": "http://www.gaizhou.gov.cn/govxxgk/gzs/2026-02-25/a098478a-8653-4c19-a888-6ebdcddca321.html",
             "publisher": "盖州市人民政府", "published_at": "2026-02-25", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
             "notes": "2025-12-29 八届人大五次会议上由市长袁世君所作"},
            {"id": "S007", "title": "盖州农产品直播（市委副书记袁世君）", "url": "http://tech.cnr.cn/techph/20200614/t20200614_525128066.shtml",
             "publisher": "央广网/北国网", "published_at": "2020-06-13", "accessed_at": AS_OF, "source_type": "media", "reliability": "high",
             "notes": "2020-06-12 中共盖州市委副书记袁世君组团为该市农产品直播代言——最晚 2020-06 已任盖州副书记"},
            {"id": "S008", "title": "中国日报网/国际在线 盖州农产直播及发展会", "url": "https://ex.chinadaily.com.cn/exchange/partners/82/rss/channel/cn/columns/j3u3t6/stories/WS5ee44106a31027ab2a8cff14.html",
             "publisher": "中国日报网", "published_at": "2020-06", "accessed_at": AS_OF, "source_type": "media", "reliability": "high",
             "notes": "佐证盖州市委副书记身份；大手笔网 2020-07-31 亦载市委副书记袁世君发言"},
            {"id": "S009", "title": "大石桥新闻网/营口之窗 2018 报道", "url": "http://www.ykwin.com/zx/news/20180418_191809.html",
             "publisher": "营口之窗/大石桥官方新闻镜像", "published_at": "2018-04", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium",
             "notes": "2018-04/05/08/10 多次以'大石桥市副市长袁世君'身份见报（环保、安全生产、镁产业调度）"},
        ],
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial",
                               "relationship_confidence": "medium", "biggest_gap": "大石桥副市长之前的更早履历与具体院校/入党参加工作年份"},
        "open_questions": [
            {"priority": "critical", "question": "大石桥市副市长任期起止与大石桥之前的工作履历（院校专业）", "why_it_matters": "晋升轨迹与人际网络",
             "suggested_queries": ["袁世君 大石桥 副市长 简历", "袁世君 拟任 盖州市委副书记 公示"], "last_attempted": AS_OF},
            {"priority": "high", "question": "出生地/籍贯与入党、参加工作年份", "why_it_matters": "身份细节",
             "suggested_queries": ["袁世君 市长 1978"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "盖州市委副书记到盖州的精确日期（区间2019-2020）", "why_it_matters": "班子延续",
             "suggested_queries": ["营口市委组织部 公示 盖州 2019", "盖州 干部大会 袁世君"], "last_attempted": AS_OF},
        ],
    }

    person_dir = PERSONS_STAGING_DIR
    today = AS_OF.replace("-", "")
    for fname, data in [
        (f"{today}-辽宁省-营口市-市委书记-李典阁.json", li),
        (f"{today}-辽宁省-营口市-市长-袁世君.json", yuan),
    ]:
        path = person_dir / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path}")


def main():
    print(f"Building {SLUG} network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    write_person_jsons()

    print(f"\nDone! Staged output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    for f in sorted(PERSONS_STAGING_DIR.glob("*.json")):
        if "盖州" in f.name:
            print(f"  JSON: {f}")


if __name__ == "__main__":
    main()
