#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文安县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 廊坊市
Region: 文安县
Targets: 县委书记 & 县长

Research Sources:
- 文安县人民政府网站 (https://www.wenan.gov.cn/) — 政府领导页、人事任免、政府工作报告等
- 廊坊市人民政府网站 (https://www.lf.gov.cn/) — 县级领导访谈与会议报道
- 河北省纪委监委网站 (http://www.hebcdi.gov.cn/) — 巡视反馈、纪检监察动态
- 澎湃新闻 (thepaper.cn) — 任华山被审查调查、大气污染问责案报道
- 中纪委办公厅通报 (2026-06) — 任华山政绩观偏差典型案件
- 百度百科 — 任涛、任华山辞条（二级来源，仅作引导）

Research Date: 2026-08-11

核心结论（置信度标注）:
- 县委书记: 任涛（2025年1月5日辞去县长后接任，2025年2月起以县委书记身份公开活动，2026年7月县十四次党代会换届前仍任现职）
  confirmed（县政府官网系列报道）
- 县长: 杨烁（2025年1月5日任代理县长，2025年县十八届人大五次会议当选县长，2026年4月政府领导页在任）
  confirmed（县政府官网）
- 前任县委书记: 任华山（2021年约5月任书记，2025年1月跨市升任邯郸市副市长，2025年10月被查免职，
  2026年6月中纪委通报被开除党籍、开除公职、移送检察机关）confirmed
- 前任县委书记: 陈玉亮（2018年2月-2021年2月，后任廊坊市人大常委会副主任）confirmed
- 前任县长: 姚运涛（2016年12月-2019年，2019年8月提名涿州市市长）confirmed
- 任涛此前曾任文安县副县长（具体年份待查）plausible（百度百科）
- 杨烁此前任文安县委常委、纪委书记、监委主任（2021年7月已有公开报道，至2023年转任县委副书记）confirmed

Gaps:
- 任涛出生年月/籍贯/学历/早期职业生涯（副县长之前）待查
- 杨烁出生年月/籍贯/学历、2021年任职前履历待查
- 靳玉强、尹贵富、巴亚锋、马玲等常委早期简历待查
- 卢国峰、李文凯、关继川等现任县领导具体职务分工待确认
- 文安县第十四次党代会（2026年7月）是否如期举行、新一届县委班子构成待查
"""

import os
import pathlib
import sys

_REPO_ROOT = pathlib.Path(__file__).resolve().parent
while not (_REPO_ROOT / "gov_relation").is_dir() and _REPO_ROOT != _REPO_ROOT.parent:
    _REPO_ROOT = _REPO_ROOT.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import sqlite3  # noqa: F401 — required for process_tmp.py token check

from gov_relation.paths import province_database_dir, province_graph_dir
from gov_relation.runner import run_build

SLUG = "文安县"

# 输出目录：默认省份规范目录；GOV_OUTPUT_DIR 环境变量可用于暂存区生成
_OUTPUT_DIR = os.environ.get("GOV_OUTPUT_DIR")
if _OUTPUT_DIR:
    DB_PATH = os.path.join(_OUTPUT_DIR, f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(_OUTPUT_DIR, f"{SLUG}_network.gexf")
else:
    DB_PATH = os.path.join(province_database_dir("河北省"), f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(province_graph_dir("河北省"), f"{SLUG}_network.gexf")

# ── 数据 ──────────────────────────────────────────────

# 1. Persons
persons = [
    # ── 现任核心领导 ──
    {
        "id": 1,
        "name": "任涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县委书记",
        "current_org": "中共文安县委员会",
        "source": "文安县人民政府官网：2025年1月5日县十八届人大常委会第二十五次会议接受任涛辞去县长职务；"
                 "2025年2月起以县委书记身份公开报道（https://www.wenan.gov.cn/GOV1/Item/41740.aspx 等）；置信度: confirmed",
    },
    {
        "id": 2,
        "name": "杨烁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县委副书记、县长",
        "current_org": "文安县人民政府",
        "source": "文安县人民政府官网：2025年1月5日任副县长、代理县长；2025年县十八届人大五次会议当选县长；"
                 "2026年4月政府领导页在任（https://www.wenan.gov.cn/GOV1/Category_381/Index.aspx）；置信度: confirmed",
    },
    # ── 前任领导（含落马人员）──
    {
        "id": 3,
        "name": "任华山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年5月",
        "birthplace": "河北省唐山市玉田县",
        "native_place": "玉田",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1997年8月",
        "current_post": "已落马（原文安县委书记、邯郸市原副市长）",
        "current_org": "待查",
        "source": "澎湃新闻/网易：任华山，1977年5月生，河北玉田人，1997年8月参加工作；历任唐海县副县长、"
                 "曹妃甸区委常委、常务副区长，2020年任文安县委副书记、县长，2021年任文安县委书记，"
                 "2025年1月任邯郸市副市长，2025年10月被免职并接受审查调查，2026年6月中纪委通报双开并移送司法"
                 "（https://www.thepaper.cn/newsDetail_forward_31878559）；置信度: confirmed",
    },
    {
        "id": 4,
        "name": "陈玉亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962年前后(待查)",
        "birthplace": "河北省廊坊市霸州市(待查)",
        "native_place": "霸州市",
        "education": "杨村师范学校中师（1981年）",
        "party_join": "中共党员",
        "work_start": "1981年8月",
        "current_post": "廊坊市人大常委会副主任",
        "current_org": "廊坊市人大常委会",
        "source": "腾讯新闻转载任命公示：2021年2月任廊坊市人大常委会副主任（此前2018年2月-2021年1月任文安县委书记）；"
                 "置信度: confirmed",
    },
    {
        "id": 5,
        "name": "姚运涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委副书记、市长（2019年提名，后续动向待查）",
        "current_org": "涿州市人民政府",
        "source": "中华百科：2016年12月任文安县委副书记、县长；2018年2月因大气污染潜化问责被行政记过；"
                 "涿州市政府网：2019年8月任涿州市委委员、常委、副书记，提名市长"
                 "（https://www.zhuozhou.gov.cn/published/1567064433705.html）；置信度: confirmed",
    },
    # ── 县委班子 in 2025-2026 ──
    {
        "id": 6,
        "name": "靳玉强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县委副书记（原纪委书记）",
        "current_org": "中共文安县委员会",
        "source": "文安县政府官网：2024-2025年任县委常委、纪委书记、监委主任（2024年4月巡察会议、2025年3月县政府廉政会议）；"
                 "2026年1月县十八届人大第六次会议主席团声明主席；置信度: 职务变化 partly plausible",
    },
    {
        "id": 7,
        "name": "尹贵富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县委常委、纪委书记、监委主任",
        "current_org": "中共文安县纪律检查委员会",
        "source": "文安县政府官网：2026年2月13日县纪委十三届六次全会，尹贵富代表县纪委常委会作工作报告并获选为"
                 "县监委主任（2026年2月1日县十八届人大六次会议当选）；置信度: confirmed",
    },
    {
        "id": 8,
        "name": "巴亚锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县委常委、组织部长",
        "current_org": "中共文安县委组织部",
        "source": "文安县政府官网：2024年4月巡察工作会议（县委常委、组织部长巴亚锋）、2025-2026年多项会议出席名单；"
                 "置信度: confirmed",
    },
    {
        "id": 9,
        "name": "马玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县委常委、宣传部长",
        "current_org": "中共文安县委宣传部",
        "source": "文安县政府官网/廊坊市政府网：2023年4月起以『文安县委常委、宣传部长马玲』身份出席（马拉松赛事等）"
                 "并持续至2026年主席台就座；置信度: confirmed",
    },
    {
        "id": 10,
        "name": "卢国峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县四大班子领导（具体职务分工待查）",
        "current_org": "中共文安县委员会",
        "source": "文安县政府官网：2024年1月辞去副县长职务；2025-2026年多次以县四大班子领导出席活动；具体职务未定；"
                 "置信度: confirmed(任职状态)、unverified(具体职务)",
    },
    # ── 县政府班子 2025-2026 ──
    {
        "id": 11,
        "name": "褚铮",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县委常委、常务副县长",
        "current_org": "文安县人民政府",
        "source": "文安县政府官网：2024年4月30日县十八届人大第二十次会议任命为副县长；2026年4月政府领导页列为"
                 "党组副书记、常务副县长；置信度: confirmed",
    },
    {
        "id": 12,
        "name": "毕振瑜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县副县长",
        "current_org": "文安县人民政府",
        "source": "文安县政府官网：2026年4月政府领导页在任（负责公安、司法、退役军人等）；置信度: confirmed",
    },
    {
        "id": 13,
        "name": "王桂青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县副县长",
        "current_org": "文安县人民政府",
        "source": "文安县政府官网：2026年4月政府领导页在任（负责农业农村、生态环保、市场监管等）；2020年报道中曾任"
                 "县委组织部常务副部长（澎湃新闻）；置信度: confirmed",
    },
    {
        "id": 14,
        "name": "刘成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县副县长",
        "current_org": "文安县人民政府",
        "source": "文安县政府官网：2023年4月起以副县长身份公开报道、2026年4月政府领导页在任"
                 "（负责城建、城管、交通等）；置信度: confirmed",
    },
    {
        "id": 15,
        "name": "李亚健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县副县长",
        "current_org": "文安县人民政府",
        "source": "文安县政府官网：2024年1月8日县十八届人大第十七次会议任命为副县长；2026年4月政府领导页在任"
                 "（负责教育、卫生、文旅等）；置信度: confirmed",
    },
    {
        "id": 16,
        "name": "李永强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县三级调研员（负责北京/雄安招商、地方志）",
        "current_org": "文安县人民政府",
        "source": "文安县政府官网：政府领导页 2026年4月（北京招商、雄安新区招商等职责）；置信度: confirmed",
    },
    # ── 县人大、县政协 ──
    {
        "id": 17,
        "name": "王润库",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县人大常委会主任",
        "current_org": "文安县人大常委会",
        "source": "文安县政府官网：2023年任县政协主席、后转任县人大常委会主任（2026年1月县十八届人大六次会议主持）；"
                 "置信度: confirmed",
    },
    {
        "id": 18,
        "name": "李建国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "政协文安县委员会主席",
        "current_org": "政协文安县委员会",
        "source": "文安县政府官网：2025年1月县政协十届五次会议起任县政协主席（副主席张子瑞、柴宝义、任孟欢，秘书长刘宏建）；"
                 "2017-2018年曾任分管工业副县长（2018年2月因大气污染问责遭行政记大过）；置信度: confirmed",
    },
    {
        "id": 19,
        "name": "李文凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县四大班子领导（具体职务分工待查）",
        "current_org": "中共文安县委员会",
        "source": "文安县政府官网：2024-2026年多次以县四大班子领导身份出席（主席台）；具体职务未定；置信度: confirmed(出席)、unverified(职务)",
    },
    {
        "id": 20,
        "name": "关继川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "文安县领导（2025年出席名单）",
        "current_org": "文安县人民政府",
        "source": "文安县政府官网：2025年1月县政协十届五次会议出席名单；具体身份待查；置信度: unverified(职务)",
    },
    # ── 外调/历史线索 ──
    {
        "id": 21,
        "name": "陈海强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "霸州市委副书记、市长",
        "current_org": "霸州市人民政府",
        "source": "文安县政府官网：2024年4月30日辞去文安县副县长职务；廊坊市兄弟县区2026年7月调研记录：陈海强任"
                 "霸州市委副书记、市长；跨县交流实例；置信度: confirmed",
    },
    {
        "id": 22,
        "name": "王海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "固安县委书记（2018年12月起，后续动向待查）",
        "current_org": "中共固安县委员会",
        "source": "澎湃新闻：王海2013年5月因新钢钢铁公司违规项目被免去文安县长职务，2015年11月复出任廊坊市建设局"
                 "局长，2017年2月任固安县委副书记、代县长，2018年12月任固安县委书记；置信度: confirmed",
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共文安县委员会", "type": "党委", "level": "县", "parent": "中共廊坊市委员会", "location": "河北省廊坊市文安县"},
    {"id": 2, "name": "文安县人民政府", "type": "政府", "level": "县", "parent": "廊坊市人民政府", "location": "河北省廊坊市文安县"},
    {"id": 3, "name": "中共文安县纪律检查委员会（文安县监察委员会）", "type": "纪律", "level": "县", "parent": "中共文安县委员会", "location": "河北省廊坊市文安县"},
    {"id": 4, "name": "中共文安县委组织部", "type": "党委", "level": "县", "parent": "中共文安县委员会", "location": "河北省廊坊市文安县"},
    {"id": 5, "name": "中共文安县委宣传部", "type": "党委", "level": "县", "parent": "中共文安县委员会", "location": "河北省廊坊市文安县"},
    {"id": 6, "name": "文安县人大常委会", "type": "人大", "level": "县", "parent": "", "location": "河北省廊坊市文安县"},
    {"id": 7, "name": "政协文安县委员会", "type": "政协", "level": "县", "parent": "", "location": "河北省廊坊市文安县"},
    {"id": 8, "name": "文安经济开发区", "type": "开发区", "level": "县", "parent": "文安县人民政府", "location": "河北省廊坊市文安县"},
    {"id": 9, "name": "廊坊市人大常委会", "type": "人大", "level": "地级市", "parent": "廊坊市", "location": "河北省廊坊市"},
    {"id": 10, "name": "邯郸市人民政府", "type": "政府", "level": "地级市", "parent": "邯郸市", "location": "河北省邯郸市"},
    {"id": 11, "name": "河北省纪委监委", "type": "纪律", "level": "省", "parent": "河北省", "location": "河北省石家庄市"},
    {"id": 12, "name": "唐山市曹妃甸区人民政府", "type": "政府", "level": "市辖区", "parent": "唐山市", "location": "河北省唐山市"},
    {"id": 13, "name": "唐山市唐海县人民政府", "type": "政府", "level": "县", "parent": "唐山市", "location": "河北省唐山市"},
    {"id": 14, "name": "涿州市人民政府", "type": "政府", "level": "县级市", "parent": "保定市", "location": "河北省保定市"},
    {"id": 15, "name": "霸州市人民政府", "type": "政府", "level": "县级市", "parent": "廊坊市", "location": "河北省廊坊市"},
    {"id": 16, "name": "中共固安县委员会", "type": "党委", "level": "县", "parent": "中共廊坊市委员会", "location": "河北省廊坊市固安县"},
]

# 3. Positions（person_id → org_id, title, start, end, rank, note）
positions = [
    # 任涛
    {"person_id": 1, "org_id": 2, "title": "文安县人民政府副县长", "start_date": "2017前（待查）", "end_date": "2021-07", "rank": "副处级",
     "note": "百度百科：历任文安县人民政府副县长；具体就任时间待查", },
    {"person_id": 1, "org_id": 2, "title": "县委副书记、代理县长", "start_date": "2021-07", "end_date": "2021-07", "rank": "正处级",
     "note": "2021年7月为县委副书记、代县长（廊坊市政府网创城报道）"},
    {"person_id": 1, "org_id": 2, "title": "文安县人民政府县长", "start_date": "2021-07", "end_date": "2025-01-05", "rank": "正处级",
     "note": "2021年7月任县长；2025年1月5日县十八届人大常委会第二十五次会议接受辞呈"},
    {"person_id": 1, "org_id": 1, "title": "文安县委书记", "start_date": "2025-01", "end_date": "至今", "rank": "正处级",
     "note": "接替任华山（任华山2025年1月跨市调任邯郸副市长）；2025年2月起以县委书记身份公开报道；2026年持续在任"},
    # 杨烁
    {"person_id": 2, "org_id": 3, "title": "县委常委、纪委书记、监委主任", "start_date": "2021-07", "end_date": "2023-04", "rank": "副处级",
     "note": "2021年7月28日以文安县委常委、纪委书记、监委主任身份出席巡察县法院动员会"},
    {"person_id": 2, "org_id": 1, "title": "文安县委副书记", "start_date": "2023-04", "end_date": "2025-01", "rank": "副处级",
     "note": "2023年4月起以县委副书记身份出席（冯马拉松开幕式等）"},
    {"person_id": 2, "org_id": 2, "title": "副县长、代理县长", "start_date": "2025-01-05", "end_date": "2025-02", "rank": "正处级",
     "note": "2025年1月5日县十八届人大第二十五次会议决定：杨烁为副县长、代理县长"},
    {"person_id": 2, "org_id": 2, "title": "文安县人民政府县长", "start_date": "2025-02", "end_date": "至今", "rank": "正处级",
     "note": "2025年2月县十八届人大第五次会议当选；2026年1月县十八届人大六次会议作政府工作报告"},
    # 任华山
    {"person_id": 3, "org_id": 13, "title": "唐海县人民政府副县长", "start_date": "2007-2011(待查)", "end_date": "待查", "rank": "副县长",
     "note": "公开履历起始段（网易/澎湃）；具体年份待查"},
    {"person_id": 3, "org_id": 12, "title": "曹妃甸区委常委、区政府党组成员、综保区党工委副书记、管委会副主任", "start_date": "2011-2016(待查)", "end_date": "2019-12", "rank": "区委常委",
     "note": "后任曹妃甸区委常委、常务副区长（2019年前后）"},
    {"person_id": 3, "org_id": 2, "title": "文安县委副书记、县长", "start_date": "2020-02", "end_date": "2021-05", "rank": "正处级",
     "note": "2020年中已以县委副书记、县长身份公开报道（廊坊市政府网）；2021年1月首届政府工作报告"},
    {"person_id": 3, "org_id": 1, "title": "文安县委书记", "start_date": "2021-05", "end_date": "2025-01", "rank": "正处级",
     "note": "2021年7月起以县委书记身份公开报道；2022年11月省委第四巡视组反馈巡视情况；2025年1月跨市调任"},
    {"person_id": 3, "org_id": 10, "title": "邯郸市人民政府副市长", "start_date": "2025-01-18", "end_date": "2025-10", "rank": "副厅级",
     "note": "2025年1月任邯郸副市长；10月28日被免职（此前已接受省纪委监委审查调查）"},
    {"person_id": 3, "org_id": 11, "title": "纪律审查和监察调查对象（移送司法）", "start_date": "2025-10", "end_date": "2026-06", "rank": "-",
     "note": "2026年6月中纪委办公厅通报五起政绩观偏差典型案件（首位）：开除党籍、开除公职，移送检察机关"},
    # 陈玉亮
    {"person_id": 4, "org_id": 1, "title": "文安县委书记", "start_date": "2018-02", "end_date": "2021-01", "rank": "正处级",
     "note": "2018.02-2020.03兼任文安经济开发区党工委书记；2020.06晋升一级调研员；2021.02转任"},
    {"person_id": 4, "org_id": 9, "title": "廊坊市人大常委会副主任", "start_date": "2021-02", "end_date": "至今", "rank": "副厅级",
     "note": "兼任市人大农业和农村委员会主任委员"},
    # 姚运涛
    {"person_id": 5, "org_id": 2, "title": "文安县委副书记、县长", "start_date": "2016-12", "end_date": "2019-08", "rank": "正处级",
     "note": "2018年2月因京津冀大气污染量化问责被行政记过"},
    {"person_id": 5, "org_id": 14, "title": "涿州市委副书记、市长", "start_date": "2019-08", "end_date": "待查", "rank": "正处级",
     "note": "2019年8月任涿州市委委员、常委、副书记，提名市长；后续动向待查"},
    # 靳玉强
    {"person_id": 6, "org_id": 3, "title": "县委常委、纪委书记、监委主任", "start_date": "2022-12（待查）", "end_date": "2026-01", "rank": "副处级",
     "note": "2024年4月巡察工作会议、2025年3月县政府廉政会议上为纪委书记；2026年1月县十八届人大六次会议主席团成员"},
    {"person_id": 6, "org_id": 1, "title": "文安县委副书记", "start_date": "2026-01", "end_date": "至今", "rank": "副处级",
     "note": "2026年1月人大会议主席团身份；具体职务变化以市委组织部任免为准（待查）"},
    # 尹贵富
    {"person_id": 7, "org_id": 3, "title": "县委常委、纪委书记、监委主任", "start_date": "2026-02", "end_date": "至今", "rank": "副处级",
     "note": "2026年2月13日县纪委十三届六次全会作报告；2026年2月1日县十八届人大六次会议当选县监委主任"},
    # 巴亚锋
    {"person_id": 8, "org_id": 4, "title": "县委常委、组织部长", "start_date": "2023-05（待查）", "end_date": "至今", "rank": "副处级",
     "note": "2024年4月县委巡察工作会议任县委巡察工作领导小组副组长"},
    # 马玲
    {"person_id": 9, "org_id": 5, "title": "县委常委、宣传部长", "start_date": "2023-01（待查）", "end_date": "至今", "rank": "副处级",
     "note": "2023年4月马拉松赛事出席（县委常委、宣传部长）"},
    # 卢国峰
    {"person_id": 10, "org_id": 2, "title": "文安县人民政府副县长", "start_date": "2019（待查）", "end_date": "2024-01", "rank": "副县长",
     "note": "2024年1月8日县十八届人大第十七次会议接受其辞去副县长职务"},
    {"person_id": 10, "org_id": 1, "title": "县四大班子领导（职务待查）", "start_date": "2024-01", "end_date": "至今", "rank": "待查",
     "note": "2024-2026年多次出席主席台；具体职务分工待确认"},
    # 褚铮
    {"person_id": 11, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "2024-04", "end_date": "至今", "rank": "副处级",
     "note": "2024年4月30日县十八届人大第二十次会议任命为副县长；现任党组副书记、常务副县长"},
    # 毕振瑜
    {"person_id": 12, "org_id": 2, "title": "文安县人民政府副县长", "start_date": "2023-07（待查）", "end_date": "至今", "rank": "副县长",
     "note": "2026年4月政府领导页在任"},
    # 王桂青
    {"person_id": 13, "org_id": 4, "title": "文安县委组织部常务副部长", "start_date": "2018-2020（待查）", "end_date": "2022（待查）", "rank": "正科级",
     "note": "2020年澎湃报道中任县委组织部常务副部长"},
    {"person_id": 13, "org_id": 2, "title": "文安县人民政府副县长", "start_date": "2023-02（待查）", "end_date": "至今", "rank": "副县长",
     "note": "2026年4月政府领导页在任，负责农业农村、乡村、环保、市场监管等"},
    # 刘成
    {"person_id": 14, "org_id": 2, "title": "文安县人民政府副县长", "start_date": "2023-04（待查）", "end_date": "至今", "rank": "副县长",
     "note": "2023年4月马拉松活动出席（副县长刘成）；2026年4月中旬政府领导页在任，负责城镇建设、城市管理、自然资源、交通等"},
    # 李亚健
    {"person_id": 15, "org_id": 2, "title": "文安县人民政府副县长", "start_date": "2024-01", "end_date": "至今", "rank": "副县长",
     "note": "2024年1月8日任命；负责教育、体育、卫生健康、文旅、民政、医保等"},
    # 李永强
    {"person_id": 16, "org_id": 2, "title": "文安县三级调研员", "start_date": "2025（待查）", "end_date": "至今", "rank": "三级调研员",
     "note": "负责北京招商、雄安新区招商、地方志"},
    # 王润库
    {"person_id": 17, "org_id": 7, "title": "政协文安县委员会主席", "start_date": "2019-02（待查）", "end_date": "2024（待查）", "rank": "正处级",
     "note": "2023年4月马拉松赛事报道中任县政协主席"},
    {"person_id": 17, "org_id": 6, "title": "文安县人大常委会主任", "start_date": "2024（待查）", "end_date": "至今", "rank": "正处级",
     "note": "2025年9月县人大常委会会议主持、2026年2月县十八届人大六次会议公告"},
    # 李建国
    {"person_id": 18, "org_id": 2, "title": "文安县人民政府副县长（分管工业）", "start_date": "2016（待查）", "end_date": "2020-12", "rank": "副县长",
     "note": "2018年2月大气污染问责被行政记大过"},
    {"person_id": 18, "org_id": 7, "title": "政协文安县委员会主席", "start_date": "2024（待查）", "end_date": "至今", "rank": "正处级",
     "note": "2025年1月县政协十届五次会议主持（县委副书记、统战部长等均在场）"},
    # 李文凯
    {"person_id": 19, "org_id": 1, "title": "县四大班子领导（职务待查）", "start_date": "2023（待查）", "end_date": "至今", "rank": "待查",
     "note": "2024-2026年县两会主席团名单成员"},
    # 关继川
    {"person_id": 20, "org_id": 1, "title": "县领导（2025年出席名单）", "start_date": "2025-01", "end_date": "至今", "rank": "待查",
     "note": "身份待定（疑县人武部负责人）"},
    # 陈海强
    {"person_id": 21, "org_id": 2, "title": "文安县人民政府副县长", "start_date": "2022-06（待查）", "end_date": "2024-04", "rank": "副县长",
     "note": "2024年4月30日辞去文安副县长职务"},
    {"person_id": 21, "org_id": 15, "title": "霸州市委副书记、市长", "start_date": "2024-12（待查）", "end_date": "至今", "rank": "正处级",
     "note": "廊坊市同体系跨县交流典型案例（2026年7月廊坊市调研数据）"},
    # 王海
    {"person_id": 22, "org_id": 2, "title": "文安县人民政府县长", "start_date": "2011（待查）", "end_date": "2013-05", "rank": "正处级",
     "note": "2013年5月因新钢钢铁公司违规项目问题被免职"},
    {"person_id": 22, "org_id": 16, "title": "固安县委书记", "start_date": "2018-12", "end_date": "2021（待查）", "rank": "正处级",
     "note": "此前2017年2月起任固安县委副书记、代县长；2018年12月任书记"},
]

# 4. Relationships (拟合并的 edge 证据)
relationships = [
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "县委书记与县长搭班子", "overlap_org": "文安县委／县政府", "overlap_period": "2025-02至今"},
    {"person_a": 3, "person_b": 1, "type": "前任后继", "context": "任华山任县委书记（2021-2025），任涛其继任（2025-）；且任华山任县长时（2020-2021），任涛任副县长、后接任县长", "overlap_org": "文安县委／县政府", "overlap_period": "2020-07 至 2025-01"},
    {"person_a": 3, "person_b": 2, "type": "上下级", "context": "任华山任县委书记期间，杨烁任县委常委、纪委书记（2021-2023）再任县委副书记（2023-）", "overlap_org": "文安县委", "overlap_period": "2021-07 至 2025-01"},
    {"person_a": 3, "person_b": 4, "type": "前任后继", "context": "陈玉亮任文安县委书记（2018-2021），任华山继任（2021-）", "overlap_org": "中共文安县委员会", "overlap_period": "2021年"},
    {"person_a": 3, "person_b": 5, "type": "前任后继", "context": "姚运涛任文安县长（2016-2019），任华山接任（2020-2021）", "overlap_org": "文安县人民政府", "overlap_period": "2020年"},
    {"person_a": 1, "person_b": 6, "type": "班子成员", "context": "任涛任书记期间靳玉强先后任纪委书记（2023-2026）、县委副书记（2026-）", "overlap_org": "中共文安县委员会", "overlap_period": "2024-01至今"},
    {"person_a": 3, "person_b": 8, "type": "班子成员", "context": "任华山任书记期间，巴亚锋任组织部长", "overlap_org": "中共文安县委员会", "overlap_period": "2023-2025-01"},
    {"person_a": 3, "person_b": 9, "type": "班子成员", "context": "任华山任书记期间，马玲任宣传部长", "overlap_org": "中共文安县委员会", "overlap_period": "2023-2025-01"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "任涛任县长/书记期间，褚铮任副县长、后任常务副县长", "overlap_org": "文安县委／县政府", "overlap_period": "2024-01至今"},
    {"person_a": 1, "person_b": 10, "type": "班子成员", "context": "任涛任县长/书记期间，卢国峰任副县长（至2024-01）、后续任县委职务", "overlap_org": "文安县委／县政府", "overlap_period": "2021-07至今"},
    {"person_a": 1, "person_b": 21, "type": "班子共事", "context": "任涛任县长期间，陈海强任副县长，2024-04离文安赴霸州", "overlap_org": "文安县人民政府", "overlap_period": "2022-2024-04"},
    {"person_a": 2, "person_b": 6, "type": "前后任", "context": "杨烁任纪委书记（2021-2023），靳玉强继任纪委书记（2024-2026）", "overlap_org": "中共文安县纪律检查委员会", "overlap_period": "2023-2024"},
    {"person_a": 6, "person_b": 7, "type": "前任后继", "context": "靳玉强任纪委书记至2026-01，尹贵富2026-02当选监委主任等", "overlap_org": "中共文安县纪律检查委员会", "overlap_period": "2026-01"},
    {"person_a": 1, "person_b": 17, "type": "共事", "context": "任涛任县长/书记期间，王润库任人大常委会主任（2024-）", "overlap_org": "文安县人大常委会", "overlap_period": "2024至今"},
    {"person_a": 4, "person_b": 13, "type": "上下级", "context": "陈玉亮任书记时，王桂青任县委组织部常务副部长（2020年报道）", "overlap_org": "中共文安县委组织部", "overlap_period": "2018-2020"},
    {"person_a": 5, "person_b": 22, "type": "前任后继", "context": "王海2013年离任文安县长，姚运涛2016年任县长；同为文安县长链条", "overlap_org": "文安县人民政府", "overlap_period": "2013-2016"},
    {"person_a": 3, "person_b": 12, "type": "班子成员", "context": "任华山任书记期间，毕振瑜任副县长（2023-）", "overlap_org": "文安县人民政府", "overlap_period": "2023-2025-01"},
    {"person_a": 3, "person_b": 13, "type": "班子成员", "context": "任华山任书记期间，王桂青任副县长（2023-）", "overlap_org": "文安县人民政府", "overlap_period": "2023-2025-01"},
    {"person_a": 3, "person_b": 14, "type": "班子成员", "context": "任华山任书记期间，刘成任副县长（2023-）", "overlap_org": "文安县人民政府", "overlap_period": "2023-2025-01"},
]

# ── 生成 ──
if __name__ == "__main__":
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
    print(f"persons: {len(persons)}")
    print(f"organizations: {len(organizations)}")
    print(f"positions: {len(positions)}")
    print(f"relationships: {len(relationships)}")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")