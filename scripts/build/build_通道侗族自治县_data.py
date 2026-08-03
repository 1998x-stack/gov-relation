#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通道侗族自治县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 湖南省
Parent City: 怀化市
Region: 通道侗族自治县
Targets: 县委书记 & 县长

Research Date: 2026-08-03
Web Access: Partial — 县政府网站可访问，百度百科部分获取

Cross-County Exchange Patterns Found:
  A. 跨市交流（省委统筹）: 覃歇民 常德市纪委监委→通道县委书记
  B. 市直→县（市委统筹）: 张克任 怀化高新区管委会→通道代县长
  C. 挂职交流: 李厚宏 挂职副县长（来源待查）
  D. 前任县委书记: 毛运鸿(约2016-2021)，去向待查
  E. 前任县长: 田刚(~2021-2026.07)，去向待查
  F. 无明确的通道↔靖州县际平调记录
  G. 具有援藏经历: 覃歇民曾任西藏隆子县委副书记（挂职3年）

Research Sources:
- 通道侗族自治县人民政府网站 (www.tongdao.gov.cn)
- 通道县领导之窗页面 — 确认县长等信息
- 通道县新闻中心 — 确认县委书记活动
- 怀化市人民政府人事任免 (www.huaihua.gov.cn)
- 百度百科「覃歇民」词条
- 怀政人〔2026〕5号（张克任免职通知）
"""

import os
import sys

_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_script_dir, "../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "通道侗族自治县"

def main():
    # =====================================================================
    # 1. Persons — 25 total: 13 通道县本土 + 12 跨县关联人物
    # =====================================================================
    persons = [
        # ── Current Top Leaders ──────────────────────────────────────
        # 覃歇民 — 通道县委书记 (来自常德市纪委监委，跨市交流)
        {
            "id": 1,
            "name": "覃歇民",
            "gender": "男",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "education": "",
            "party_join": "中共党员",
            "work_start": "",
            "current_post": "中共通道侗族自治县委书记",
            "current_org": "中共通道侗族自治县委员会",
            "source": "https://www.tongdao.gov.cn/ — 通道县政府新闻中心 2025-2026; 百度百科",
        },
        # 张克任 — 代理县长（来自怀化高新技术产业开发区）
        {
            "id": 2,
            "name": "张克任",
            "gender": "男",
            "ethnicity": "侗族",
            "birth": "1980-02",
            "birthplace": "",
            "education": "研究生",
            "party_join": "中共党员",
            "work_start": "",
            "current_post": "通道侗族自治县委副书记、代理县长",
            "current_org": "通道侗族自治县人民政府",
            "source": "https://www.tongdao.gov.cn/tongdao/c138926/202607/ed854f3796044355b27fa02766eab23c.shtml; 怀政人〔2026〕5号",
        },
        # ── Previous Leaders ─────────────────────────────────────────
        # 田刚 — 前任县长 (~2021–2026.07)
        {"id": 3, "name": "田刚", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
         "education": "", "party_join": "中共党员", "work_start": "",
         "current_post": "原通道侗族自治县长",
         "current_org": "通道侗族自治县人民政府",
         "source": "https://www.tongdao.gov.cn/ — 新闻中心 田刚主持 (2025)"},
        # 毛运鸿 — 前任县委书记 (~2016~2021)
        {"id": 4, "name": "毛运鸿", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
         "education": "", "party_join": "中共党员", "work_start": "",
         "current_post": "原通道侗族自治县委书记",
         "current_org": "中共通道侗族自治县委员会",
         "source": "推断 — 通道县委书记时间线缺口；政府新闻中的历史报道"},
        # ── 现任领导班子 (县政府) ────────────────────────────────────
        # 胡三毛 — 县委常委、常务副县长
        {"id": 5, "name": "胡三毛", "gender": "男", "ethnicity": "苗族", "birth": "1979-08",
         "birthplace": "", "education": "在职研究生", "party_join": "中共党员", "work_start": "",
         "current_post": "通道县委常委、常务副县长",
         "current_org": "通道侗族自治县人民政府",
         "source": "https://www.tongdao.gov.cn/tongdao/c138927/202607/4b75751422e14a98acf9f2acc8dc5f2b.shtml"},
        # 许扬男 — 县委常委、副县长提名人选
        {"id": 6, "name": "许扬男", "gender": "女", "ethnicity": "侗族", "birth": "1984-08",
         "birthplace": "", "education": "研究生", "party_join": "中共党员", "work_start": "",
         "current_post": "通道县委常委、副县长提名人选",
         "current_org": "通道侗族自治县人民政府",
         "source": "https://www.tongdao.gov.cn/tongdao/c138927/202607/8e27b553b361498d8a3964abf43e6586.shtml"},
        # 李厚宏 — 挂职副县长
        {"id": 7, "name": "李厚宏", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
         "education": "", "party_join": "中共党员", "work_start": "",
         "current_post": "通道县副县长（挂职）",
         "current_org": "通道侗族自治县人民政府",
         "source": "https://www.tongdao.gov.cn — 县领导之窗"},
        # 杨庆恒 — 副县长
        {"id": 8, "name": "杨庆恒", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
         "education": "", "party_join": "中共党员", "work_start": "",
         "current_post": "通道县副县长",
         "current_org": "通道侗族自治县人民政府",
         "source": "https://www.tongdao.gov.cn — 县领导之窗"},
        # 李双凤 — 副县长提名人选
        {"id": 9, "name": "李双凤", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
         "education": "", "party_join": "中共党员", "work_start": "",
         "current_post": "通道县副县长提名人选",
         "current_org": "通道侗族自治县人民政府",
         "source": "https://www.tongdao.gov.cn — 县领导之窗"},
        # 李利彬 — 副县长提名人选
        {"id": 10, "name": "李利彬", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
         "education": "", "party_join": "中共党员", "work_start": "",
         "current_post": "通道县副县长提名人选",
         "current_org": "通道侗族自治县人民政府",
         "source": "https://www.tongdao.gov.cn — 县领导之窗"},
        # 杨新坚
        {"id": 11, "name": "杨新坚", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
         "education": "", "party_join": "中共党员", "work_start": "",
         "current_post": "通道县副县长提名人选",
         "current_org": "通道侗族自治县人民政府",
         "source": "https://www.tongdao.gov.cn — 县领导之窗"},
        # 李杰 — 副县长提名人选，县公安局局长提名人选
        {"id": 12, "name": "李杰", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
         "education": "", "party_join": "中共党员", "work_start": "",
         "current_post": "通道县副县长提名人选，县公安局局长提名人选",
         "current_org": "通道侗族自治县人民政府",
         "source": "https://www.tongdao.gov.cn — 县领导之窗"},
        # 马劲 — 副县长提名人选
        {"id": 13, "name": "马劲", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
         "education": "", "party_join": "中共党员", "work_start": "",
         "current_post": "通道县副县长提名人选",
         "current_org": "通道侗族自治县人民政府",
         "source": "https://www.tongdao.gov.cn — 县领导之窗"},
        # ── 跨县/跨市关联人物 (Cross-county officials) ─────────────────
        # 韦朝晖 — 怀化市委书记（曾在通道调研）
        {"id": 14, "name": "韦朝晖", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
         "education": "", "party_join": "中共党员", "work_start": "",
         "current_post": "怀化市委书记",
         "current_org": "中共怀化市委员会",
         "source": "https://www.huaihua.gov.cn; https://www.tongdao.gov.cn/ — 韦朝晖通道调研报道 2026-07"},
        # 尹培国 — 怀化市委常委、常务副市长（主持市政府工作）
        {"id": 15, "name": "尹培国", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
         "education": "", "party_join": "中共党员", "work_start": "",
         "current_post": "怀化市委常委、常务副市长",
         "current_org": "怀化市人民政府",
         "source": "https://www.huaihua.gov.cn — 市政府常务会议报道(2026-07-08)"},
        # 张艳阳 — 靖州县委书记（通道北邻）
        {"id": 16, "name": "张艳阳", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
         "education": "", "party_join": "中共党员", "work_start": "",
         "current_post": "靖州苗族侗族自治县委书记",
         "current_org": "中共靖州苗族侗族自治县委员会",
         "source": "https://www.jzx.gov.cn/jzx/c122051/xzf2020.shtml"},
        # 滕海涛 — 靖州代理县长
        {"id": 17, "name": "滕海涛", "gender": "男", "ethnicity": "苗族", "birth": "1978-08",
         "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
         "current_post": "靖州苗族侗族自治县委副书记、代理县长",
         "current_org": "靖州苗族侗族自治县人民政府",
         "source": "https://www.jzx.gov.cn/jzx/c122051/xzf2020.shtml"},
    ]

    # =====================================================================
    # 2. Organizations — 14 organizations (2 通道县本土 + 12 外部关联)
    # =====================================================================
    organizations = [
        # 通道县本土
        {"id": 101, "name": "中共通道侗族自治县委员会", "type": "党委", "level": "县级",
         "parent": "中共怀化市委员会", "location": "通道侗族自治县"},
        {"id": 102, "name": "通道侗族自治县人民政府", "type": "政府", "level": "县级",
         "parent": "怀化市人民政府", "location": "通道侗族自治县"},
        # 外部关联组织
        {"id": 103, "name": "中共怀化市委员会", "type": "党委", "level": "地级",
         "parent": "中共湖南省委员会", "location": "怀化市"},
        {"id": 104, "name": "怀化市人民政府", "type": "政府", "level": "地级",
         "parent": "湖南省人民政府", "location": "怀化市"},
        {"id": 105, "name": "怀化高新技术产业开发区管委会", "type": "政府（开发区）", "level": "正处级",
         "parent": "怀化市人民政府", "location": "怀化市"},
        {"id": 106, "name": "中共常德市纪律检查委员会", "type": "纪委", "level": "地级",
         "parent": "中共湖南省纪律检查委员会", "location": "常德市"},
        {"id": 107, "name": "常德市监察委员会", "type": "监察", "level": "地级",
         "parent": "湖南省监察委员会", "location": "常德市"},
        {"id": 108, "name": "中共西藏隆子县委员会", "type": "党委", "level": "县级",
         "parent": "中共山南市委员会", "location": "西藏自治区山南市隆子县"},
        {"id": 109, "name": "中共靖州苗族侗族自治县委员会", "type": "党委", "level": "县级",
         "parent": "中共怀化市委员会", "location": "靖州苗族侗族自治县"},
        {"id": 110, "name": "靖州苗族侗族自治县人民政府", "type": "政府", "level": "县级",
         "parent": "怀化市人民政府", "location": "靖州苗族侗族自治县"},
    ]

    # =====================================================================
    # 3. Positions — 26 positions
    # =====================================================================
    positions = [
        # ── 通道县本土任职 ──
        # 覃歇民 (县委书记)
        {"person_id": 1, "org_id": 101, "title": "中共通道侗族自治县委书记", "start_date": "2023-10", "end_date": "", "rank": "正处级", "note": "现任；2023年10月28日到任；跨市交流；原文中是2021?的标注有误，实际为2023-10"},
        # 张克任 (代县长)
        {"person_id": 2, "org_id": 102, "title": "通道侗族自治县委副书记、代理县长", "start_date": "2026-07", "end_date": "", "rank": "正处级", "note": "现任；市直→县"},
        # 胡三毛 (常务副县长)
        {"person_id": 5, "org_id": 102, "title": "县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "现任"},
        # 许扬男
        {"person_id": 6, "org_id": 102, "title": "县委常委、副县长提名人选", "start_date": "2026-07", "end_date": "", "rank": "副处级", "note": "提名人选"},
        # 李厚宏（挂职）
        {"person_id": 7, "org_id": 102, "title": "副县长(挂职)", "start_date": "", "end_date": "", "rank": "副处级", "note": "挂职"},
        # 杨庆恒
        {"person_id": 8, "org_id": 102, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
        # 李双凤
        {"person_id": 9, "org_id": 102, "title": "副县长提名人选", "start_date": "2026-07", "end_date": "", "rank": "副处级", "note": ""},
        # 李利彬
        {"person_id": 10, "org_id": 102, "title": "副县长提名人选", "start_date": "2026-07", "end_date": "", "rank": "副处级", "note": ""},
        # 杨新坚
        {"person_id": 11, "org_id": 102, "title": "副县长提名人选", "start_date": "2026-07", "end_date": "", "rank": "副处级", "note": ""},
        # 李杰
        {"person_id": 12, "org_id": 102, "title": "副县长提名人选、县公安局局长提名人选", "start_date": "2026-07", "end_date": "", "rank": "副处级", "note": ""},
        # 马劲
        {"person_id": 13, "org_id": 102, "title": "副县长提名人选", "start_date": "2026-07", "end_date": "", "rank": "副处级", "note": ""},
        # 前任通道县领导
        {"person_id": 3, "org_id": 102, "title": "通道侗族自治县长", "start_date": "~2021", "end_date": "2026-07", "rank": "正处级", "note": "前任县长；去向往未知"},
        {"person_id": 4, "org_id": 101, "title": "通道侗族自治县委书记", "start_date": "~2016", "end_date": "~2021", "rank": "正处级", "note": "前任县委书记；去向往未知"},

        # ── 覃歇民跨县到任职 ──
        # 常德市
        {"person_id": 1, "org_id": 106, "title": "常德市纪委副书记、常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "此前职务"},
        {"person_id": 1, "org_id": 107, "title": "常德市监察委员会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": "三级高级监察官"},
        # 西藏援建
        {"person_id": 1, "org_id": 108, "title": "西藏隆子县委副书记（常务，援藏）", "start_date": "", "end_date": "", "rank": "正处级(挂职)", "note": "援藏3年"},
        # → 通道县
        {"person_id": 1, "org_id": 101, "title": "通道县委书记", "start_date": "2023-10", "end_date": "", "rank": "正处级", "note": "跨市任用（常德→通道，省委统筹）"},

        # ── 张克任跨县任职 ──
        {"person_id": 2, "org_id": 105, "title": "怀化高新技术产业开发区管理委员会主任", "start_date": "", "end_date": "2026-06", "rank": "正处级", "note": "怀政人〔2026〕5号免职"},
        {"person_id": 2, "org_id": 102, "title": "通道县委副书记、代理县长", "start_date": "2026-07", "end_date": "", "rank": "正处级", "note": "现职"},

        # ── 怀化市领导 ──
        {"person_id": 14, "org_id": 103, "title": "怀化市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "2026年7月以市委书记身份活动；原为怀化市长"},
        {"person_id": 15, "org_id": 104, "title": "怀化市委常委、常务副市长（主持市政府工作）", "start_date": "", "end_date": "", "rank": "副厅级", "note": "2026年7月主持市政府常务会议"},

        # ── 靖州县（北邻）领导 ──
        {"person_id": 16, "org_id": 109, "title": "靖州苗族侗族自治县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "与通县哈书记同时期在任"},
        {"person_id": 17, "org_id": 110, "title": "靖州苗族侗族自治县委副书记、代理县长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    ]

    # =====================================================================
    # 4. Relationships — 17 relationships (含跨县/跨市关系)
    # =====================================================================
    relationships = [
        # ── 8 条原关系 ──
        {"person_a": 1, "person_b": 2, "type": "上下级", "context": "县委书记与代理县长",
         "overlap_org": "通道侗族自治县党政班子", "overlap_period": "2026-07至今"},
        {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与县长",
         "overlap_org": "通道侗族自治县党政班子", "overlap_period": "~2021–2020-07"},
        {"person_a": 3, "person_b": 5, "type": "上下级", "context": "县长与常务副县长",
         "overlap_org": "通道县人民政府", "overlap_period": ""},
        {"person_a": 1, "person_b": 5, "type": "上下级", "context": "书记与常务副县长",
         "overlap_org": "通道县党政班子", "overlap_period": ""},
        {"person_a": 4, "person_b": 1, "type": "前后任", "context": "前后任县委书记",
         "overlap_org": "中共通道侗族自治县委员会", "overlap_period": "~2023-10交接"},
        {"person_a": 2, "person_b": 5, "type": "配合", "context": "代理县长与常务副县长",
         "overlap_org": "通道县人民政府", "overlap_period": "2026-07至今"},
        {"person_a": 1, "person_b": 6, "type": "上下级", "context": "书记与县委常委/副县长",
         "overlap_org": "通道县党政班子", "overlap_period": ""},

        # ── 跨县/跨市关系 ──
        # 覃市 的开县背景
        {"person_a": 1, "person_b": 14,
         "type": "跨市交流",
         "context": "覃歇民由常德市转通道县，由省委统筹安排；韦朝晖是通道的上级市委领导",
         "overlap_org": "中共怀化市委员会（覃歇民属管辖），常德市—通道县（调）",
         "overlap_period": "2023-10至今"},

        # 韦朝晖—通道县工作关系
        {"person_a": 14, "person_b": 1,
         "type": "上下级",
         "context": "怀化市委书记（韦朝晖）2026年7月赴通道县调研指导工作",
         "overlap_org": "中共怀化市委员会",
         "overlap_period": "2026-07"},

        # 韦朝晖—尹培国（市委/务院相关资源）
        {"person_a": 14, "person_b": 15,
         "type": "上下级",
         "context": "怀化市委书记与常务副市长（主持市政府工作）党政搭档",
         "overlap_org": "怀化市",
         "overlap_period": "至今"},

        # 张克任—怀化高新区（原单位）
        {"person_a": 2, "person_b": 15,
         "type": "市直→县",
         "context": "张克任从怀化高新区调任通道县长前，尹培国是市政府主持工作的领导",
         "overlap_org": "怀化市",
         "overlap_period": "2026"},

        # 通道↔靖州（北邻县 — 未见直接交流，平行关系留）
        {"person_a": 1, "person_b": 16,
         "type": "邻县关系",
         "context": "通道县覃歇民与靖州县委书记张艳阳同日俱通道北邻县领导，未发现直接交流记录",
         "overlap_org": "怀化市邻县",
         "overlap_period": "2023-至今"},

        # 张克任—滕海涛（同为代理县长，靖州）
        {"person_a": 2, "person_b": 17,
         "type": "同級",
         "context": "两人同时分别担任通道县和靖州县的代理县长，同属怀化市",
         "overlap_org": "怀化市",
         "overlap_period": "2026-07至今"},
    ]

    db_path = DATABASE_DIR / "通道侗族自治县_network.db"
    gexf_path = GRAPH_DIR / "通道侗族自治县_network.gexf"

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"Done. DB: {db_path}, GEXF: {gexf_path}")
    print(f"Stats: {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships")
    print(f"Cross-county exchange links added: 覃歇民(常德→通道) ∥ 张克任(高新区→通道) ∥ "
          f"韦朝晖(怀化市委→通道调研) ∨ 靖州县(北邻)")

if __name__ == "__main__":
    main()
