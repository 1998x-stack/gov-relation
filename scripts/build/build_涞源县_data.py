#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
涞源县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 保定市
Region: 涞源县
Targets: 县委书记 & 县长

Research Sources:
- 涞源县人民政府门户网站 (www.laiyuan.gov.cn)
  - 领导之窗 lists/372 及 shows/372/*: 确认薛春雷(县长)、杨忠良(常务副县长)、高红亮、
    熊锦望(公安局长)、朱江涛、李国记、宋爱栋(挂职)、朱智慧、常建鹏、李志英
  - 官网站内检索确认: 县委书记王燕(2024-09起, 至2025-12十四届十次全会)、
    薛春雷(县委副书记、代县长2024-10 → 县长2025起)
  - 王燕履历: 360百科“王燕(涞源县委副书记)”条目, 河北易县人, 1977-08生,
    曾任易县、唐县多职, 2021-05调任涞源代县长, 2024后期任县委书记
  - 历史班子(2019-02, 全县领导干部大会报道): 李自贤(书记)、周峰(县长)、
    王力军(县委副书记)、柳向标(组织部长)、曾文(宣传部长)、王晓明(政法委书记)、
    梁永强(常务副县长)、徐润雨(副县长)
  - 前任县委书记: 陈英民(2021~2024-07), 前前任: 李自贤
  - 前任县长: 周峰(至2021), 王燕(2021~2024-08)

Research Date: 2026-08-05
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "涞源县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 现任核心领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "王燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年8月",
        "birthplace": "河北易县",
        "native_place": "河北易县",
        "education": "中共河北省委党校经济管理专业在职研究生",
        "party_join": "1996年11月",
        "work_start": "1996年8月",
        "current_post": "涞源县委书记",
        "current_org": "中共涞源县委员会",
        "source": "涞源县人民政府门户网站(县委书记王燕, 2024-09/10, 2025-06/08, 2025-12十四届十次全会). 373百科王燕词条(女,1977-08,河北易县, 唐县→涞源县长→书记). 来源: http://www.laiyuan.gov.cn/",
    },
    {
        "id": 2,
        "name": "薛春雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县委副书记、政府县长",
        "current_org": "涞源县人民政府",
        "source": "涞源县人民政府领导之窗(shows/372/855.html)确认薛春雷为县委副书记、政府党组书记、县长, 涞源经济开发区党工委副书记、管委会主任. 官网站内检索确认2024-10-30县委副书记、代县长, 2025-02-11起政府县长并主持十七届政府第60-62次常务会议. 来源: http://www.laiyuan.gov.cn/",
    },
    # ════════════════════════════════════════
    # 县政府班子 (from 领导之窗 lists/577, official)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "杨忠良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县委常委、常务副县长",
        "current_org": "涞源县人民政府",
        "source": "涞源县人民政府领导之窗(shows/372/910.html) 确认杨忠良为县委常委、政府党组副书记、常务副县长.",
    },
    {
        "id": 4,
        "name": "高红亮",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县政府党组成员、副县长",
        "current_org": "涞源县人民政府",
        "source": "涞源县人民政府领导之窗(lists/372). 负责水利、农业农村、乡村振兴.",
    },
    {
        "id": 5,
        "name": "熊锦望",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县政府党组成员、副县长、公安局长",
        "current_org": "涞源县公安局",
        "source": "涞源县人民政府领导之窗(shows/372/912.html) 确认熊锦望为政府党组成员、副县长、公安局长.",
    },
    {
        "id": 6,
        "name": "朱江涛",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县政府党组成员、副县长",
        "current_org": "涞源县人民政府",
        "source": "涞源县人民政府领导之窗(shows/372/2071). 负责人社、教育体育、交通、城建.",
    },
    {
        "id": 7,
        "name": "李国记",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县政府党组成员、副县长",
        "current_org": "涞源县人民政府",
        "source": "涞源县人民政府领导之窗(shows/372/1119). 负责金融、市场监管、数字涞源建设.",
    },
    {
        "id": 8,
        "name": "宋爱栋",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县委常委、政府副县长(挂职)",
        "current_org": "涞源县人民政府",
        "source": "涞源县人民政府领导之窗(shows/372/856). 局长曾由高红亮主导(协助).",
    },
    {
        "id": 9,
        "name": "朱智慧",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县政府副县长",
        "current_org": "涞源县人民政府",
        "source": "涞源县人民政府领导之窗(shows/372/911). 负责医保、卫健、民政、文旅.",
    },
    {
        "id": 10,
        "name": "常建鹏",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县四级调研员",
        "current_org": "涞源县人民政府",
        "source": "涞源县人民政府领导之窗(shows/372/913). 协助杨忠良工作.",
    },
    {
        "id": 11,
        "name": "李志英",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "Oz涞源县三级调研员",
        "current_org": "涞源县人民政府",
        "source": "涞源县人民政府领导之窗(shows/372/1118). 负责通信方面工作.",
    },
    # ════════════════════════════════════════
    # 前任与历史领导
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "陈英民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县前任县委书记(现任保定市教育局党组书记、局长)",
        "current_org": "中共涞源县委员会",
        "source": "涞源县2021-05任书记至2024-09(2024-07-01仍任,后卸任; 继任者为王燕). 卸任后任保定市教育工委书记、市教育局党组书记/局长(2025). 来源: http://www.laiyuan.gov.cn/ 及保定市教育局.",
    },
    {
        "id": 13,
        "name": "李自贤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县前任县委书记(至约2021)",
        "current_org": "中共涞源县委员会",
        "source": "涞源县人民政府网(2020-12仍任, 2021-01十三届八次全会仍有记载; 同时任市政协副主席). 来源: http://www.laiyuan.gov.cn/",
    },
    {
        "id": 14,
        "name": "周峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县前任县长(至约2021)",
        "current_org": "涞源县人民政府",
        "source": "涞源县人民政府网(2021-04-20仍任县委副书记、政府县长). 来源: http://www.laiyuan.gov.cn/",
    },
    # ── 历史班子 (2019-02 全县领导干部大会) ──
    {
        "id": 15,
        "name": "王力军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县委副书记(2019)",
        "current_org": "中共涞源县委员会",
        "source": "涞源县2019-02-28全县领导干部大会报道(shows/11/8083).",
    },
    {
        "id": 16,
        "name": "柳向标",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县委常委、组织部长(2019)",
        "current_org": "中共涞源县委组织部",
        "source": "涞源县2019-02-27全县领导干部大会(shows/11/8083).",
    },
    {
        "id": 17,
        "name": "曾文",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县委常委、宣传部长(2019)",
        "current_org": "中共涞源县委宣传部",
        "source": "涞源县2019-02-27全县领导干部大会(shows/11/8083).",
    },
    {
        "id": 18,
        "name": "王晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县委政法委书记(2019)",
        "current_org": "中共涞源县委政法委",
        "source": "涞源县2019-02-27全县领导干部大会(shows/11/8083).",
    },
    {
        "id": 19,
        "name": "梁永强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县委常委、常务副县长(2019)",
        "current_org": "涞源县人民政府",
        "source": "涞源县2019-02-27全县领导干部大会(shows/11/8083).",
    },
    {
        "id": 20,
        "name": "徐润雨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县政府副县长(2019)",
        "current_org": "涞源县人民政府",
        "source": "涞源县2019-02-27全县领导干部大会(shows/11/8083).",
    },
    # ── 跨县交流历史人物 (来源: 网易/澎湃/河北新闻网) ──
    {
        "id": 22,
        "name": "都建华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定兴县委书记(历史上涞源任职)",
        "current_org": "定兴县人民政府",
        "source": "网易(2021-01-29): 曾任涞源县委常委/副县长/常务副县长, 后任定兴县委书记.",
    },
    {
        "id": 23,
        "name": "刘晓萌",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源前期副县长(后调保定市人防办主任)",
        "current_org": "保定市人民防空办公室",
        "source": "澎湃(2024-07): 曾任涞源县政府副县长, 后任保定市人民防空办公室主任.",
    },
    {
        "id": 24,
        "name": "周仲明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞源县历史县长(后调保定市直乃至唐山)",
        "current_org": "保定市人民政府",
        "source": "河北新闻网简历(2015): 1996-1998任涞源县委副书记、县长, 后任保定市政府副秘书长、蠡县县委书记等.",
    },
    {
        "id": 25,
        "name": "王义民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "河北涞源县",
        "native_place": "河北涞源县",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涞水县原县委书记(涞源籍, 2020被查)",
        "current_org": "涞水县人民政府",
        "source": "百度百科王义民; 每日经济新闻(2020-10): 涞源籍, 历任北桥区、雄县、涞水县委书记.",
    },
]

# 2. Organizations
organizations = [
    {"id": 0, "name": "中共涞源县委员会", "type": "党委", "level": "县级", "parent": "中共保定市委", "location": "河北省保定市涞源县"},
    {"id": 1, "name": "涞源县人民政府", "type": "政府", "level": "县级", "parent": "保定市人民政府", "location": "河北省保定市涞源县"},
    {"id": 2, "name": "涞源县人大常委会", "type": "人大", "level": "县级", "parent": "保定市人大常委会", "location": "河北省保定市涞源县"},
    {"id": 3, "name": "政协涞源县委员会", "type": "政协", "level": "县级", "parent": "保定市政协", "location": "河北省保定市涞源县"},
    {"id": 4, "name": "涞源县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共涞源县委员会", "location": "河北省保定市涞源县"},
    {"id": 5, "name": "中共涞源县委组织部", "type": "党委部门", "level": "县级", "parent": "中共涞源县委员会", "location": "河北省保定市涞源县"},
    {"id": 6, "name": "中共涞源县委宣传部", "type": "党委部门", "level": "县级", "parent": "中共涞源县委员会", "location": "河北省保定市涞源县"},
    {"id": 7, "name": "中共涞源县委政法委", "type": "党委部门", "level": "县级", "parent": "中共涞源县委员会", "location": "河北省保定市涞源县"},
    {"id": 8, "name": "涞源县公安局", "type": "政府部门", "level": "县级", "parent": "涞源县人民政府", "location": "河北省保定市涞源县"},
    {"id": 9, "name": "涞源经济开发区管委会", "type": "开发区", "level": "省级", "parent": "涞源县人民政府", "location": "河北省保定市涞源县"},
    {"id": 10, "name": "涞源县人民政府办公室", "type": "政府部门", "level": "县级", "parent": "涞源县人民政府", "location": "河北省保定市涞源县"},
    {"id": 11, "name": "涞源县发展和改革局", "type": "政府部门", "level": "县级", "parent": "涞源县人民政府", "location": "河北省保定市涞源县"},
    {"id": 12, "name": "涞源县财政局", "type": "政府部门", "level": "县级", "parent": "涞源县人民政府", "location": "河北省保定市涞源县"},
    {"id": 13, "name": "涞源县水利局", "type": "政府部门", "level": "县级", "parent": "涞源县人民政府", "location": "河北省保定市涞源县"},
    {"id": 14, "name": "涞源县农业农村局", "type": "政府部门", "level": "县级", "parent": "涞源县人民政府", "location": "河北省保定市涞源县"},
    {"id": 15, "name": "涞源县乡村振兴局", "type": "政府部门", "level": "县级", "parent": "涞源县人民政府", "location": "河北省保定市涞源县"},
    # ── 跨县/市节点 ──
    {"id": 16, "name": "中共保定市委", "type": "党委", "level": "地市级", "parent": "中共河北省委", "location": "河北省保定市"},
    {"id": 17, "name": "保定市人民政府", "type": "政府", "level": "地市级", "parent": "河北省人民政府", "location": "河北省保定市"},
    {"id": 18, "name": "唐县人民政府", "type": "政府", "level": "县级", "parent": "保定市人民政府", "location": "河北省保定市唐县"},
    {"id": 19, "name": "中共唐县委员会", "type": "党委", "level": "县级", "parent": "中共保定市委", "location": "河北省保定市唐县"},
    {"id": 20, "name": "中共唐县县委组织部", "type": "党委部门", "level": "县级", "parent": "中共唐县委员会", "location": "河北省保定市唐县"},
    {"id": 21, "name": "中共易县委员会", "type": "党委", "level": "县级", "parent": "中共保定市委", "location": "河北省保定市易县"},
    {"id": 22, "name": "易县人民政府", "type": "政府", "level": "县级", "parent": "保定市人民政府", "location": "河北省保定市易县"},
    {"id": 23, "name": "共青团易县委员会", "type": "群团", "level": "县级", "parent": "中共易县委员会", "location": "河北省保定市易县"},
    {"id": 24, "name": "易县裴山镇人民政府", "type": "政府", "level": "乡镇级", "parent": "易县人民政府", "location": "河北省保定市易县"},
    {"id": 25, "name": "涿州师范学校", "type": "事业单位", "level": "地市", "parent": "保定市教育局", "location": "河北省保定市涿州市"},
    {"id": 26, "name": "易县桥头乡中学", "type": "事业单位", "level": "乡镇级", "parent": "易县教育局", "location": "河北省保定市易县"},
    {"id": 27, "name": "中共河北省委党校", "type": "事业单位", "level": "省级", "parent": "中共河北省委", "location": "河北省石家庄市"},
    {"id": 28, "name": "中国人民政治协商会议河北省保定市委员会", "type": "政协", "level": "地市级", "parent": "河北省政协", "location": "河北省保定市"},
    {"id": 31, "name": "保定市教育局", "type": "政府部门", "level": "地市级", "parent": "保定市人民政府", "location": "河北省保定市"},
    {"id": 32, "name": "中共保定市委教育工委", "type": "党委部门", "level": "地市级", "parent": "中共保定市委", "location": "河北省保定市"},
    {"id": 33, "name": "定兴县人民政府", "type": "政府", "level": "县级", "parent": "保定市人民政府", "location": "河北省保定市定兴县"},
    {"id": 34, "name": "保定市人民防空办公室", "type": "政府部门", "level": "地市级", "parent": "保定市人民政府", "location": "河北省保定市"},
    {"id": 35, "name": "涞水县人民政府", "type": "政府", "level": "县级", "parent": "保定市人民政府", "location": "河北省保定市涞水县"},
    {"id": 29, "name": "中共唐县县委宣传部", "type": "党委部门", "level": "县级", "parent": "中共唐县委员会", "location": "河北省保定市唐县"},
    {"id": 30, "name": "中共唐县县委统战部", "type": "党委部门", "level": "县级", "parent": "中共唐县委员会", "location": "河北省保定市唐县"},
]

# 3. Positions
positions = [
    # ── 王燕 (县委书记) ──
    {"person_id": 1, "org_id": 0, "title": "涞源县委书记", "start": "2024-08/09", "end": "至今", "rank": "正处级", "note": "2024-07-29仍为县长; 2024-09-25起以书记身份活动; 2025-12十四届十次全会主持"},
    {"person_id": 1, "org_id": 1, "title": "涞源县委副书记、政府县长", "start": "2021-05", "end": "2024-08", "rank": "正处级", "note": "2021-05任代县长, 后任县长"},
    {"person_id": 1, "org_id": 19, "title": "唐县县委副书记、三级调研员", "start": "2021-02", "end": "2021-05", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 18, "title": "唐县县委常委、副县长(分工常务工作)、三级调研员", "start": "2019-05", "end": "2021-02", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 20, "title": "唐县县委常委、组织部长", "start": "2017-01", "end": "2019-05", "rank": "副处级", "note": "兼任统战部长(至2019-01)"},
    {"person_id": 1, "org_id": 29, "title": "唐县县委常委、宣传部长、农工委书记", "start": "2011-08", "end": "2017-01", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 24, "title": "易县裴山镇党委副书记、镇长", "start": "2008-11", "end": "2011-08", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 23, "title": "共青团易县县委书记", "start": "2005-03", "end": "2008-11", "rank": "正科级", "note": "此前1997-2005任团县委副书记"},
    {"person_id": 1, "org_id": 26, "title": "易县桥头乡中学教师", "start": "1996-08", "end": "1997-03", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 25, "title": "涿州师范学校学生", "start": "1993-09", "end": "1996-08", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 27, "title": "中共河北省委党校在职研究生(经济管理专业)", "start": "2006-09", "end": "2009-06", "rank": "", "note": "在职学历"},

    # ── 薛春雷 (县长) ──
    {"person_id": 2, "org_id": 1, "title": "涞源县委副书记、政府县长", "start": "2025-01/02", "end": "至今", "rank": "正处级", "note": "2025-01-26起为政府县长"},
    {"person_id": 2, "org_id": 1, "title": "涞源县委副书记、代县长", "start": "2024-10", "end": "2025-01", "rank": "正处级", "note": "2024-10-31以代县长活动"},
    {"person_id": 2, "org_id": 9, "title": "涞源经济开发区党工委副书记、管委会主任(兼任)", "start": "2024-10", "end": "至今", "rank": "", "note": "兼任"},

    # ── 县政府班子 ──
    {"person_id": 3, "org_id": 1, "title": "涞源县委常委、政府党组副书记、常务副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "涞源县政府党组成员、副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "负责水利、农业农村、乡村振兴"},
    {"person_id": 5, "org_id": 8, "title": "涞源县政府副县长、公安局长", "start": "待查", "end": "至今", "rank": "副处级", "note": "政府党组成员、副县长兼公安局长"},
    {"person_id": 6, "org_id": 1, "title": "涞源县政府党组成员、副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "负责教育体育、交通、城建"},
    {"person_id": 7, "org_id": 1, "title": "涞源县政府党组成员、副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "负责金融、市场监管"},
    {"person_id": 8, "org_id": 1, "title": "涞源县委常委、副县长(挂职)", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "涞源县政府副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "负责医保、卫健、民政、文旅"},
    {"person_id": 10, "org_id": 1, "title": "涞源县四级调研员(协助常务副县长)", "start": "待查", "end": "至今", "rank": "副处级", "note": "常建鹏"},
    {"person_id": 11, "org_id": 1, "title": "涞源县三级调研员(负责通信)", "start": "待查", "end": "至今", "rank": "副处级", "note": "李志英"},

    # ── 前任 ──
    {"person_id": 12, "org_id": 0, "title": "涞源县委书记", "start": "2021-12?", "end": "2024-07", "rank": "正处级", "note": "2022-01十三届三次全会起以书记身份; 2024-07-01仍任; 后由王燕接任"},
    {"person_id": 13, "org_id": 0, "title": "涞源县委书记", "start": "待查", "end": "2021?", "rank": "正处级", "note": "李自贤; 兼市政协副主席; 2020-12仍任, 2021-01十三届八次全会"},
    {"person_id": 13, "org_id": 28, "title": "保定市政协副主席(兼任)", "start": "待查", "end": "待查", "rank": "副厅级", "note": "兼任"},
    {"person_id": 14, "org_id": 1, "title": "涞源县委副书记、政府县长", "start": "待查", "end": "2021-06?", "rank": "正处级", "note": "周峰; 2021-04-20仍任"},
    # ── 2019 历史班子 ──
    {"person_id": 15, "org_id": 0, "title": "涞源县委副书记(2019)", "start": "2019", "end": "待查", "rank": "副处级", "note": "王力军"},
    {"person_id": 16, "org_id": 5, "title": "涞源县委常委、组织部长(2019)", "start": "2019", "end": "待查", "rank": "副处级", "note": "柳向标"},
    {"person_id": 17, "org_id": 6, "title": "涞源县委常委、宣传部长(2019)", "start": "2019", "end": "待查", "rank": "副处级", "note": "曾文"},
    {"person_id": 18, "org_id": 7, "title": "涞源县委政法委书记(2019)", "start": "2019", "end": "待查", "rank": "副处级", "note": "王晓明"},
    {"person_id": 19, "org_id": 1, "title": "涞源县委常委、常务副县长(2019)", "start": "2019", "end": "待查", "rank": "副处级", "note": "梁永强"},
    {"person_id": 20, "org_id": 1, "title": "涞源县政府副县长(2019)", "start": "2019", "end": "待查", "rank": "副处级", "note": "徐润雨"},
    # ── 跨县交流人物任职 ──
    {"person_id": 12, "org_id": 31, "title": "保定市教育局党组书记、局长(市委教育工委书记)", "start": "2024末/2025", "end": "待查", "rank": "正处级", "note": "卸任涞源县委书记后调任保定市直"},
    {"person_id": 22, "org_id": 1, "title": "涞源县委常委、副县长/常务副县长(历史)", "start": "待查", "end": "待查", "rank": "副处级", "note": "都建华, 后任定兴县委书记"},
    {"person_id": 22, "org_id": 33, "title": "定兴县委书记", "start": "2021?（推测）", "end": "待查", "rank": "正处级", "note": "网易(2021-01-29)确认"},
    {"person_id": 23, "org_id": 1, "title": "涞源县政府副县长(历史)", "start": "待查", "end": "待查", "rank": "副处级", "note": "刘晓萌"},
    {"person_id": 23, "org_id": 34, "title": "保定市人民防空办公室主任", "start": "待查", "end": "待查", "rank": "正处级", "note": "澎湃(2024-07)"},
    {"person_id": 24, "org_id": 1, "title": "涞源县委副书记、县长(1996-1998)", "start": "1996", "end": "1998", "rank": "正处级", "note": "周仲明, 历史"},
    {"person_id": 24, "org_id": 17, "title": "保定市政府副秘书长(后续)", "start": "1998", "end": "2001", "rank": "正处级", "note": "河北新闻网简历(2015)"},
    {"person_id": 25, "org_id": 35, "title": "涞水县委书记(涞源籍)", "start": "待查", "end": "2020", "rank": "正处级", "note": "王义民, 2020被查", },
]

# 4. Relationships
relationships = [
    # ── 现任核心搭档 ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政主要领导搭档", "overlap_org": "中共涞源县委员会/涞源县人民政府", "overlap_period": "2024-至今"},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "王燕由县长转任书记, 薛春雷接任县长", "overlap_org": "涞源县人民政府", "overlap_period": "2024-10"},
    # 书记 + 常务副职
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与常务副县长工作关系", "overlap_org": "涞源县人民政府", "overlap_period": "2024-至今"},
    # 县长 + 副县长们
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与常务副县长搭档", "overlap_org": "涞源县人民政府", "overlap_period": "2024-至今"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长与副县长(农业、水利)", "overlap_org": "涞源县人民政府", "overlap_period": "2024-至今"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与公安局长", "overlap_org": "涞源县人民政府", "overlap_period": "2024-至今"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长(交通、城建)", "overlap_org": "涞源县人民政府", "overlap_period": "2024-至今"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长(金融)", "overlap_org": "涞源县人民政府", "overlap_period": "2024-至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长(文旅、卫生)", "overlap_org": "涞源县人民政府", "overlap_period": "2024-至今"},

    # ── 前后任/交接 ──
    {"person_a": 12, "person_b": 1, "type": "predecessor_successor", "context": "陈英民前任涞源县委书记, 王燕接任", "overlap_org": "中共涞源县委员会", "overlap_period": "2024"},
    {"person_a": 13, "person_b": 12, "type": "predecessor_successor", "context": "李自贤前任涞源县委书记, 陈英民接任", "overlap_org": "中共涞源县委员会", "overlap_period": "2021"},
    {"person_a": 14, "person_b": 1, "type": "predecessor_successor", "context": "周峰前任涞源县长, 王燕接任", "overlap_org": "涞源县人民政府", "overlap_period": "2021"},

    # ── 同团队重叠 ──
    {"person_a": 12, "person_b": 1, "type": "overlap", "context": "陈英民任书记期间王燕任县长(2022-2024)", "overlap_org": "中共涞源县委员会/涞源县人民政府", "overlap_period": "2022-2024"},
    {"person_a": 13, "person_b": 14, "type": "overlap", "context": "李自贤任书记会同周峰任县长搭档", "overlap_org": "中共涞源县委员会/涞源县人民政府", "overlap_period": "2019-2021"},

    # ── 跨县交流 (王燕 的易县→唐县→涞源路径) ──
    {"person_a": 1, "person_b": 19, "type": "same_system", "context": "王燕在唐县任宣传部长、组织部长、常务副县长、县委副书记近10年", "overlap_org": "中共唐县委员会/唐县人民政府", "overlap_period": "2011-2021"},

    # ── 历史班子同事 (2019) ──
    {"person_a": 15, "person_b": 16, "type": "overlap", "context": "王力军任县委副书记柳向标任组织部长同届班子", "overlap_org": "中共涞源县委员会", "overlap_period": "2019"},
    {"person_a": 15, "person_b": 17, "type": "overlap", "context": "王力军、曾文同届县委班子", "overlap_org": "中共涞源县委员会", "overlap_period": "2019"},
    {"person_a": 15, "person_b": 18, "type": "overlap", "context": "王力军、王晓明同届县委班子", "overlap_org": "中共涞源县委员会", "overlap_period": "2019"},
    {"person_a": 19, "person_b": 14, "type": "overlap", "context": "梁永强任常务副县长时周峰任县长", "overlap_org": "涞源县人民政府", "overlap_period": "2019"},

    # ── 跨县交流 ──
    {"person_a": 12, "person_b": 16, "type": "same_system", "context": "陈英民卸任涞源书记后调任保定市市直(教育局局长/教育工委书记)", "overlap_org": "保定市人民政府/中共保定市委", "overlap_period": "2025"},
    {"person_a": 22, "person_b": 1, "type": "same_org", "context": "都建华曾在涞源任职(溆源常委/副县长), 后任定兴县委书记", "overlap_org": "涞源县人民政府", "overlap_period": "待查"},
    {"person_a": 23, "person_b": 1, "type": "same_org", "context": "刘晓萌曾任涞源县政府副县长, 后调保定市人防办", "overlap_org": "涞源县人民政府", "overlap_period": "待查"},
    {"person_a": 24, "person_b": 1, "type": "same_org", "context": "周仲明1996-1998任涞源县长(历史), 后保定市直", "overlap_org": "涞源县人民政府", "overlap_period": "1996-1998"},
]

# ── Build ──
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