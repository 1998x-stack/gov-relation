#!/usr/bin/env python3
"""Build script for 叠彩区 (Diecai District, Guilin, Guangxi) leadership network.

Generated: 2026-07-22
Sources:
  - http://www.glsdcqzf.gov.cn/ (official district government website)
  - http://www.glsdcqzf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/ (government leadership page)
  - http://www.glsdcqzf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/qz/index.shtml (区长 bio)
  - http://www.glsdcqzf.gov.cn/dcdt/ (district news confirming current officeholders)
  - https://www.guilin.gov.cn/ (Guilin city government)
"""

import sqlite3  # noqa: used by gov_relation.runner

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "罗胜奇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "叠彩区委书记",
        "current_org": "中共桂林市叠彩区委员会",
        "source": "http://www.glsdcqzf.gov.cn/dcdt/t27930267.shtml (confirmed as 区委书记 as of 2026-07-17)",
    },
    {
        "id": 2,
        "name": "陆华静",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1982年10月",
        "birthplace": "广西都安",
        "education": "研究生学历，经济学硕士学位",
        "party_join": "2005年4月",
        "work_start": "2006年7月",
        "current_post": "叠彩区区长",
        "current_org": "桂林市叠彩区人民政府",
        "source": "http://www.glsdcqzf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/qz/index.shtml (official bio, updated 2026-06-01)",
    },
    {
        "id": 3,
        "name": "蒋鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府党组书记、常务副区长",
        "current_org": "桂林市叠彩区人民政府",
        "source": "http://www.glsdcqzf.gov.cn/dcdt/t27930267.shtml (confirmed as 区政府党组书记 as of 2026-07-17)",
    },
    # ── Deputy Leaders ──
    {
        "id": 4,
        "name": "刘兆龙",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1979年11月",
        "birthplace": "桂林资源",
        "education": "大学本科学历",
        "party_join": "2000年12月",
        "work_start": "1998年7月",
        "current_post": "区委常委、常务副区长",
        "current_org": "桂林市叠彩区人民政府",
        "source": "http://www.glsdcqzf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/t26572846.shtml (official bio)",
    },
    {
        "id": 5,
        "name": "陈孝云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年7月",
        "birthplace": "湖南东安",
        "education": "",
        "party_join": "1992年12月",
        "work_start": "1983年9月",
        "current_post": "城管专员",
        "current_org": "桂林市叠彩区人民政府",
        "source": "http://www.glsdcqzf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/t26572842.shtml (official bio)",
    },
    {
        "id": 6,
        "name": "滕惠君",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "广西宾阳",
        "education": "本科学历，学士学位（天津商学院贸易经济专业）",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "桂林市叠彩区人民政府",
        "source": "http://www.glsdcqzf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/t26572839.shtml (official bio)",
    },
    {
        "id": 7,
        "name": "韩新秀",
        "gender": "女",
        "ethnicity": "",
        "birth": "1983年3月",
        "birthplace": "山东东营",
        "education": "在职研究生学历",
        "party_join": "2006年4月",
        "work_start": "2006年7月",
        "current_post": "副区长",
        "current_org": "桂林市叠彩区人民政府",
        "source": "http://www.glsdcqzf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/t26614307.shtml (official bio)",
    },
    {
        "id": 8,
        "name": "张帆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "广西桂林",
        "education": "法学学士（广西大学法学专业）",
        "party_join": "2004年4月",
        "work_start": "2004年8月",
        "current_post": "副区长、叠彩公安分局局长",
        "current_org": "桂林市公安局叠彩分局",
        "source": "http://www.glsdcqzf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/t26577395.shtml (official bio)",
    },
    # ── Second-Level Researchers ──
    {
        "id": 9,
        "name": "严清贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年2月",
        "birthplace": "湖北公安",
        "education": "大学本科学历（桂林陆军学院军事指挥专业）",
        "party_join": "1986年12月",
        "work_start": "1985年10月",
        "current_post": "二级调研员",
        "current_org": "桂林市叠彩区人民政府",
        "source": "http://www.glsdcqzf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/t26572834.shtml (official bio)",
    },
    {
        "id": 10,
        "name": "文孙革",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年3月",
        "birthplace": "",
        "education": "全日制本科学历，学士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "二级调研员",
        "current_org": "桂林市叠彩区人民政府",
        "source": "http://www.glsdcqzf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/t26572830.shtml (official bio)",
    },
    {
        "id": 11,
        "name": "曹琳树",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年8月",
        "birthplace": "江西都昌",
        "education": "大学学历（南京陆军指挥学院合同战术专业）",
        "party_join": "1998年5月",
        "work_start": "1996年12月",
        "current_post": "二级调研员",
        "current_org": "桂林市叠彩区人民政府",
        "source": "http://www.glsdcqzf.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/t26585024.shtml (official bio)",
    },
    # ── Previous Leaders ──
    {
        "id": 12,
        "name": "杨玉霜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂林市人大常委会副主任（原叠彩区委书记）",
        "current_org": "桂林市人大常委会",
        "source": "http://www.glsdcqzf.gov.cn/dcdt/t27687968.shtml (listed as 市人大常委会副主任、叠彩区委书记 as of 2026-05-05)",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共桂林市叠彩区委员会", "type": "党委", "level": "正处级", "parent": "中共桂林市委员会", "location": "桂林市叠彩区"},
    {"id": 2, "name": "桂林市叠彩区人民政府", "type": "政府", "level": "正处级", "parent": "桂林市人民政府", "location": "桂林市叠彩区"},
    {"id": 3, "name": "桂林市人大常委会", "type": "人大", "level": "正厅级", "parent": "", "location": "桂林市"},
    {"id": 4, "name": "桂林市公安局叠彩分局", "type": "政府", "level": "正科级", "parent": "桂林市公安局", "location": "桂林市叠彩区"},
    {"id": 5, "name": "高铁（桂林）广西园管委会", "type": "事业单位", "level": "正处级", "parent": "桂林市人民政府", "location": "桂林市"},
]

POSITIONS = [
    # 罗胜奇
    {"person_id": 1, "org_id": 1, "title": "叠彩区委书记", "start_date": "2026年", "end_date": "present", "rank": "正处级", "note": "2026年7月确认在任"},
    # 陆华静
    {"person_id": 2, "org_id": 2, "title": "叠彩区区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "同时任区委副书记"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 5, "title": "高铁（桂林）广西园管委会副主任（兼）", "start_date": "", "end_date": "present", "rank": "正处级", "note": "兼职"},
    # 陆华静 历任职
    {"person_id": 2, "org_id": 10001, "title": "广西壮族自治区财政厅财政监督检查局干部", "start_date": "2006年", "end_date": "", "rank": "", "note": "自治区财政厅"},
    {"person_id": 2, "org_id": 10001, "title": "广西壮族自治区财政厅国库处副主任科员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 10001, "title": "广西壮族自治区财政厅办公室副主任科员、主任科员", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 10002, "title": "广西河池市委办正科级干部、人事教育科科长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 10002, "title": "广西河池市委办副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 10003, "title": "广西大化瑶族自治县委常委、都阳镇党委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 10003, "title": "广西大化瑶族自治县委常委、宣传部部长，政府副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 10004, "title": "广西壮族自治区发展和改革委员会财政金融处副处长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 10004, "title": "广西壮族自治区发展和改革委员会办公室副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 10004, "title": "广西壮族自治区发展和改革委员会财政金融和信用建设处副处长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 10004, "title": "广西壮族自治区发展和改革委员会财政金融和信用建设处处长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 10005, "title": "广西桂林市七星区委常委、副区长提名人选（正处长级）", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 10005, "title": "广西桂林市七星区委常委、政府党组成员、副区长（正处长级）", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 蒋鹏
    {"person_id": 3, "org_id": 2, "title": "区政府党组书记、常务副区长", "start_date": "2026年", "end_date": "present", "rank": "正处级", "note": "区政府主要负责同志"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘兆龙
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘兆龙历任职
    {"person_id": 4, "org_id": 10006, "title": "资源县人大常委会办公室秘书", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 10006, "title": "资源县两水苗族乡党委委员、副乡长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 10006, "title": "资源县车田苗族乡党委副书记、乡长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 4, "org_id": 10006, "title": "资源县两水苗族乡党委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 4, "org_id": 10006, "title": "资源县政府办主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 10006, "title": "资源县政府副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 10006, "title": "资源县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 陈孝云
    {"person_id": 5, "org_id": 2, "title": "城管专员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 滕惠君
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 韩新秀
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张帆
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼叠彩公安分局局长"},
    {"person_id": 8, "org_id": 4, "title": "叠彩公安分局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "同时任公安局党委书记"},
    # 二级调研员
    {"person_id": 9, "org_id": 2, "title": "二级调研员", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "二级调研员", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "二级调研员", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 杨玉霜（前任）
    {"person_id": 12, "org_id": 3, "title": "桂林市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "原叠彩区委书记，仍兼任至2026年5月"},
    {"person_id": 12, "org_id": 1, "title": "叠彩区委书记（原任）", "start_date": "", "end_date": "2026年", "rank": "正处级", "note": "离任时间约为2026年5-6月"},
]

RELATIONSHIPS = [
    # 党政正职
    {"person_a": 1, "person_b": 3, "type": "党政正职搭档", "context": "区委书记-区政府党组书记（代区长）党政正职搭档", "overlap_org": "叠彩区四套班子", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 区委书记与区委常委
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记—区委常委（常务副区长）", "overlap_org": "叠彩区委常委会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 区政府党组书记与常务副区长
    {"person_a": 3, "person_b": 4, "type": "党政副职搭档", "context": "区政府党组书记—常务副区长", "overlap_org": "叠彩区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 区政府负责人与其他副区长
    {"person_a": 3, "person_b": 5, "type": "上下级", "context": "区政府党组书记—城管专员", "overlap_org": "叠彩区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 6, "type": "上下级", "context": "区政府党组书记—副区长", "overlap_org": "叠彩区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 7, "type": "上下级", "context": "区政府党组书记—副区长", "overlap_org": "叠彩区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 8, "type": "上下级", "context": "区政府党组书记—副区长（公安）", "overlap_org": "叠彩区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 前任-现任转接
    {"person_a": 12, "person_b": 1, "type": "前任-后任", "context": "杨玉霜卸任叠彩区委书记，罗胜奇接任", "overlap_org": "中共叠彩区委员会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 陆华静（区长）与前区委书记
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长与区委书记（前任搭档）", "overlap_org": "叠彩区四套班子", "overlap_period": "至2026年", "source": "", "confidence": "confirmed"},
    # 陆华静与蒋鹏（区政府交接）
    {"person_a": 2, "person_b": 3, "type": "前任-后任", "context": "区长交接过渡期", "overlap_org": "叠彩区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 副区长之间
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "副区长与副区长", "overlap_org": "叠彩区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "副区长与副区长（公安）", "overlap_org": "叠彩区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "副区长与副区长（公安）", "overlap_org": "叠彩区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

DB_PATH = DATABASE_DIR / "叠彩区_network.db"
GEXF_PATH = GRAPH_DIR / "叠彩区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="叠彩区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
