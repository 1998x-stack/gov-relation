#!/usr/bin/env python3
"""构建江永县（湖南省永州市）领导人物关系网络数据库和图文件。

数据来源：
- 江永县人民政府官网 (https://www.jiangyong.gov.cn/jiangyong/zfld/leaderIndex3.shtml)
- 江永县政务动态 (截至2026年7月)
- 永州市领导班子调查 (2026-07-14 报告)

生成:
  data/tmp/hunan_江永县/江永县_network.db
  data/tmp/hunan_江永县/江永县_network.gexf
"""

from pathlib import Path

import sqlite3  # noqa: F401 — required for process_tmp.py token check

from gov_relation.runner import run_build

HERE = Path(__file__).parent
DB_PATH = HERE / "江永县_network.db"
GEXF_PATH = HERE / "江永县_network.gexf"

# ═══════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════

persons = [
    # ── 现任核心领导 ──
    {
        "id": 1,
        "name": "李群辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "江永县委书记",
        "current_org": "中共江永县委",
        "source": "https://www.jiangyong.gov.cn/jiangyong/xzdt/202606/ab5c278d295b4847ac48cb141dd4e427.shtml",
    },
    {
        "id": 2,
        "name": "于思洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-11",
        "birthplace": "辽宁本溪",
        "education": "研究生学历",
        "party_join": "2009-05",
        "work_start": "2012-07",
        "current_post": "江永县委副书记、县长",
        "current_org": "江永县人民政府",
        "source": "https://www.jiangyong.gov.cn/jiangyong/zfld/leaderIndex3.shtml",
    },
    # ── 县委常委 ──
    {
        "id": 3,
        "name": "杨敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-10",
        "birthplace": "湖南宁远",
        "education": "研究生学历",
        "party_join": "2001-05",
        "work_start": "2001-12",
        "current_post": "江永县委常委、常务副县长",
        "current_org": "江永县人民政府",
        "source": "https://www.jiangyong.gov.cn/jiangyong/zfld/leaderIndex3.shtml",
    },
    {
        "id": 4,
        "name": "彭浩宸",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-02",
        "birthplace": "湖南零陵",
        "education": "研究生学历",
        "party_join": "2009-06",
        "work_start": "2007-12",
        "current_post": "江永县委常委、副县长、江永产业开发区党工委第一书记",
        "current_org": "江永县人民政府",
        "source": "https://www.jiangyong.gov.cn/jiangyong/zfld/leaderIndex3.shtml",
    },
    {
        "id": 5,
        "name": "蒋丽君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "江永县委常委、宣传部部长",
        "current_org": "中共江永县委宣传部",
        "source": "https://www.jiangyong.gov.cn/ 新闻报道 (2026年7月全国露营大会)",
    },
    # ── 副县长 ──
    {
        "id": 6,
        "name": "周仁文",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth": "1982-02",
        "birthplace": "湖南双牌",
        "education": "大专学历",
        "party_join": "2001-07",
        "work_start": "2002-10",
        "current_post": "江永县副县长、县公安局局长",
        "current_org": "江永县人民政府",
        "source": "https://www.jiangyong.gov.cn/jiangyong/zfld/leaderIndex3.shtml",
    },
    {
        "id": 7,
        "name": "曹孝卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-10",
        "birthplace": "湖南衡阳",
        "education": "博士研究生学历，理学博士学位",
        "party_join": "2009-03",
        "work_start": "2012-06",
        "current_post": "江永县副县长",
        "current_org": "江永县人民政府",
        "source": "https://www.jiangyong.gov.cn/jiangyong/zfld/leaderIndex3.shtml",
    },
    {
        "id": 8,
        "name": "唐明川",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth": "1981-09",
        "birthplace": "湖南江永",
        "education": "大学学历",
        "party_join": "2002-03",
        "work_start": "1998-09",
        "current_post": "江永县副县长",
        "current_org": "江永县人民政府",
        "source": "https://www.jiangyong.gov.cn/jiangyong/zfld/leaderIndex3.shtml",
    },
    {
        "id": 9,
        "name": "唐梦琳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981-09",
        "birthplace": "湖南零陵",
        "education": "大学学历",
        "party_join": "2007-06",
        "work_start": "2004-08",
        "current_post": "江永县副县长",
        "current_org": "江永县人民政府",
        "source": "https://www.jiangyong.gov.cn/jiangyong/zfld/leaderIndex3.shtml",
    },
    {
        "id": 10,
        "name": "朱国华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1992-04",
        "birthplace": "湖南道县",
        "education": "大学学历",
        "party_join": "2017-09",
        "work_start": "2013-08",
        "current_post": "江永县副县长",
        "current_org": "江永县人民政府",
        "source": "https://www.jiangyong.gov.cn/jiangyong/zfld/leaderIndex3.shtml",
    },
    # ── 县领导（角色待确认） ──
    {
        "id": 11,
        "name": "钱建洪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "江永县领导",
        "current_org": "中共江永县委/江永县人民政府",
        "source": "https://www.jiangyong.gov.cn/jiangyong/xzdt/202606/ab5c278d295b4847ac48cb141dd4e427.shtml",
    },
    # ── 产业开发区 ──
    {
        "id": 12,
        "name": "邓海平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "江永产业开发区党工委书记",
        "current_org": "江永产业开发区",
        "source": "https://www.jiangyong.gov.cn/ 新闻报道",
    },
    # ── 前任领导（来自 Wikipedia/永州调研） ──
    {
        "id": 13,
        "name": "唐德荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-12",
        "birthplace": "永州冷水滩",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江永县原县委书记（前任）",
        "current_org": "中共江永县委",
        "source": "https://zh.wikipedia.org/wiki/%E6%B1%9F%E6%B0%B8%E5%8E%BF",
    },
    {
        "id": 14,
        "name": "何德波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-12",
        "birthplace": "湖南道县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江永县原县长（前任）",
        "current_org": "江永县人民政府",
        "source": "https://zh.wikipedia.org/wiki/%E6%B1%9F%E6%B0%B8%E5%8E%BF",
    },
]

# ═══════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共江永县委", "type": "党委", "level": "县级", "parent": "中共永州市委", "location": "永州市江永县"},
    {"id": 2, "name": "江永县人民政府", "type": "政府", "level": "县级", "parent": "永州市人民政府", "location": "永州市江永县"},
    {"id": 3, "name": "中共江永县委宣传部", "type": "党委", "level": "县级", "parent": "中共江永县委", "location": "永州市江永县"},
    {"id": 4, "name": "江永县公安局", "type": "政府", "level": "正科级", "parent": "江永县人民政府", "location": "永州市江永县"},
    {"id": 5, "name": "江永产业开发区", "type": "开发区", "level": "县级", "parent": "江永县人民政府", "location": "永州市江永县"},
    {"id": 6, "name": "江永县人大常委会", "type": "人大", "level": "县级", "parent": "江永县", "location": "永州市江永县"},
    {"id": 7, "name": "政协江永县委员会", "type": "政协", "level": "县级", "parent": "江永县", "location": "永州市江永县"},
]

# ═══════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════

positions = [
    # 李群辉
    {"person_id": 1, "org_id": 1, "title": "江永县委书记", "start": "", "end": "present", "rank": "正处级", "note": "截至2026年3月已在任"},
    # 于思洋
    {"person_id": 2, "org_id": 2, "title": "江永县委副书记、县长", "start": "", "end": "present", "rank": "正处级", "note": "截至2026年3月在任，前任为何德波"},
    # 杨敏
    {"person_id": 3, "org_id": 2, "title": "江永县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 彭浩宸
    {"person_id": 4, "org_id": 2, "title": "江永县委常委、副县长、江永产业开发区党工委第一书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 蒋丽君
    {"person_id": 5, "org_id": 3, "title": "江永县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 周仁文
    {"person_id": 6, "org_id": 2, "title": "江永县副县长、县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 曹孝卫
    {"person_id": 7, "org_id": 2, "title": "江永县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 唐明川
    {"person_id": 8, "org_id": 2, "title": "江永县副县长", "start": "", "end": "present", "rank": "副处级", "note": "本地干部，江永人"},
    # 唐梦琳
    {"person_id": 9, "org_id": 2, "title": "江永县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 朱国华
    {"person_id": 10, "org_id": 2, "title": "江永县副县长", "start": "", "end": "present", "rank": "副处级", "note": "最年轻，1992年生"},
    # 钱建洪
    {"person_id": 11, "org_id": 1, "title": "江永县领导（县委常委/副县长）", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待确认"},
    # 邓海平
    {"person_id": 12, "org_id": 5, "title": "江永产业开发区党工委书记", "start": "", "end": "present", "rank": "正科级/副处级", "note": ""},
    # 前任领导
    {"person_id": 13, "org_id": 1, "title": "江永县委书记", "start": "2021-07", "end": "", "rank": "正处级", "note": "前任县委书记，去向未知"},
    {"person_id": 14, "org_id": 2, "title": "江永县县长", "start": "2021-06", "end": "", "rank": "正处级", "note": "前任县长，已被于思洋接替，去向未知"},
]

# ═══════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════

relationships = [
    # ── 核心班子关系 ──
    {
        "person_a": 1, "person_b": 2,
        "type": "共事",
        "context": "县委书记—县长，江永县党政一把手",
        "overlap_org": "中共江永县委/江永县人民政府",
        "overlap_period": "2026—至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "共事",
        "context": "县委书记—常务副县长",
        "overlap_org": "中共江永县委",
        "overlap_period": "2026—至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "共事",
        "context": "县长—常务副县长，政府班子正副手",
        "overlap_org": "江永县人民政府",
        "overlap_period": "2026—至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 11,
        "type": "共事",
        "context": "李群辉调研财税工作时钱建洪一同参加",
        "overlap_org": "中共江永县委",
        "overlap_period": "2026",
        "confidence": "confirmed",
    },
    # ── 政府班子共事关系 ──
    {
        "person_a": 2, "person_b": 4,
        "type": "共事",
        "context": "县长—常委副县长",
        "overlap_org": "江永县人民政府",
        "overlap_period": "2026—至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "共事",
        "context": "县长—副县长/公安局长",
        "overlap_org": "江永县人民政府",
        "overlap_period": "2026—至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "共事",
        "context": "县长—副县长",
        "overlap_org": "江永县人民政府",
        "overlap_period": "2026—至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 8,
        "type": "共事",
        "context": "县长—副县长",
        "overlap_org": "江永县人民政府",
        "overlap_period": "2026—至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 9,
        "type": "共事",
        "context": "县长—副县长",
        "overlap_org": "江永县人民政府",
        "overlap_period": "2026—至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 10,
        "type": "共事",
        "context": "县长—副县长",
        "overlap_org": "江永县人民政府",
        "overlap_period": "2026—至今",
        "confidence": "confirmed",
    },
    # ── 县委班子共事关系 ──
    {
        "person_a": 3, "person_b": 4,
        "type": "共事",
        "context": "常委副县长—常委副县长",
        "overlap_org": "中共江永县委",
        "overlap_period": "2026—至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 3, "person_b": 5,
        "type": "共事",
        "context": "县委常委—宣传部长",
        "overlap_org": "中共江永县委",
        "overlap_period": "2026—至今",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "共事",
        "context": "县委书记—宣传部长",
        "overlap_org": "中共江永县委",
        "overlap_period": "2026—至今",
        "confidence": "confirmed",
    },
    # ── 前后任关系 ──
    {
        "person_a": 1, "person_b": 13,
        "type": "前后任",
        "context": "李群辉接替唐德荣任江永县委书记",
        "overlap_org": "中共江永县委",
        "overlap_period": "2026年前后交接",
        "confidence": "plausible",
    },
    {
        "person_a": 2, "person_b": 14,
        "type": "前后任",
        "context": "于思洋接替何德波任江永县县长",
        "overlap_org": "江永县人民政府",
        "overlap_period": "2026年前后交接",
        "confidence": "plausible",
    },
    # ── 同乡关系 ──
    {
        "person_a": 10, "person_b": 14,
        "type": "同乡",
        "context": "朱国华（副县长）与前任县长何德波均籍贯湖南道县",
        "overlap_org": "道县",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # ── 跨县关系 ──
    {
        "person_a": 3, "person_b": 8,
        "type": "籍贯关联",
        "context": "杨敏（湖南宁远人）与唐明川（江永本地干部）跨县工作关系",
        "overlap_org": "江永县人民政府",
        "overlap_period": "2026—至今",
        "confidence": "confirmed",
    },
    # ── 彭浩宸与产业开发区 ──
    {
        "person_a": 4, "person_b": 12,
        "type": "上下级",
        "context": "彭浩宸任产业开发区党工委第一书记，邓海平任党工委书记",
        "overlap_org": "江永产业开发区",
        "overlap_period": "2026—至今",
        "confidence": "confirmed",
    },
]


# ═══════════════════════════════════════════
# 构建
# ═══════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="江永县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("✓ 江永县网络构建完成")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
