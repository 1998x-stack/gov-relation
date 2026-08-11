#!/usr/bin/env python3
"""Shandong Province (山东省) leadership network build script.

This script creates a SQLite database and GEXF graph for the Shandong
provincial leadership network. It covers the current Party Secretary (省委书记),
Governor (省长), and the 12th Provincial Party Standing Committee.

Data sources
------------
- Wikipedia (English/Chinese)
- Official government announcements
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

# Add project root for gov_relation imports
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent.parent.resolve()
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Metadata ──────────────────────────────────────────────────────────────
SLUG = "山东省"
DATE_TAG = datetime.now().strftime("%Y%m%d")
TIMESTAMP = datetime.now().strftime("%Y-%m-%d")

# ── Persons (id starts at 1) ─────────────────────────────────────────────

PERSONS = [
    # ── Top Leader: Party Secretary ──
    {
        "id": 1,
        "name": "林武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962-02",
        "birthplace": "福建省闽侯县",
        "education": "江西冶金学院（现江西理工大学）",
        "party_join": "1987",
        "work_start": "1982",
        "current_post": "山东省委书记",
        "current_org": "中国共产党山东省委员会",
        "source": "https://en.wikipedia.org/wiki/Lin_Wu",
    },
    # ── Top Leader: Governor ──
    {
        "id": 2,
        "name": "周乃翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1961-12",
        "birthplace": "江苏省宜兴市",
        "education": "南京工业大学",
        "party_join": "1987-12",
        "work_start": "1982",
        "current_post": "山东省省长",
        "current_org": "山东省人民政府",
        "source": "https://en.wikipedia.org/wiki/Zhou_Naixiang",
    },
    # ── Predecessor: Former Party Secretary (now Central Politburo) ──
    {
        "id": 3,
        "name": "李干杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964-11-11",
        "birthplace": "湖南省望城县",
        "education": "清华大学工程物理系",
        "party_join": "1984",
        "work_start": "1989",
        "current_post": "中央统战部部长",
        "current_org": "中共中央统一战线工作部",
        "source": "https://en.wikipedia.org/wiki/Li_Ganjie",
    },
    # ── Predecessor: Previous Party Secretary ──
    {
        "id": 4,
        "name": "刘家义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1956",
        "birthplace": "重庆市开县",
        "education": "西南财经大学",
        "party_join": "1976",
        "work_start": "1975",
        "current_post": "（离任）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Liu_Jiayi",
    },
    # ── Standing Committee Members (12th Provincial Committee, as of 2022) ──
    {
        "id": 5,
        "name": "徐海荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山东省委常委、宣传部部长",
        "current_org": "中国共产党山东省委员会",
        "source": "https://en.wikipedia.org/wiki/Shandong_Provincial_Committee_of_the_Chinese_Communist_Party",
    },
    {
        "id": 6,
        "name": "白玉刚",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山东省委常委、组织部部长",
        "current_org": "中国共产党山东省委员会",
        "source": "https://en.wikipedia.org/wiki/Shandong_Provincial_Committee_of_the_Chinese_Communist_Party",
    },
    {
        "id": 7,
        "name": "王宇燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山东省委常委、统战部部长",
        "current_org": "中国共产党山东省委员会",
        "source": "https://en.wikipedia.org/wiki/Shandong_Provincial_Committee_of_the_Chinese_Communist_Party",
    },
    {
        "id": 8,
        "name": "刘强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山东省委常委、济南市委书记",
        "current_org": "中国共产党济南市委员会",
        "source": "https://en.wikipedia.org/wiki/Shandong_Provincial_Committee_of_the_Chinese_Communist_Party",
    },
    {
        "id": 9,
        "name": "曾赞荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山东省委常委、常务副省长",
        "current_org": "山东省人民政府",
        "source": "https://en.wikipedia.org/wiki/Shandong_Provincial_Committee_of_the_Chinese_Communist_Party",
    },
    {
        "id": 10,
        "name": "张海波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山东省委常委、秘书长",
        "current_org": "中国共产党山东省委员会",
        "source": "https://en.wikipedia.org/wiki/Shandong_Provincial_Committee_of_the_Chinese_Communist_Party",
    },
    {
        "id": 11,
        "name": "傅明先",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山东省委常委（前任）",
        "current_org": "中国共产党山东省委员会",
        "source": "https://en.wikipedia.org/wiki/Shandong_Provincial_Committee_of_the_Chinese_Communist_Party",
    },
    {
        "id": 12,
        "name": "夏红民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山东省委常委、省纪委书记",
        "current_org": "中共山东省纪律检查委员会",
        "source": "https://en.wikipedia.org/wiki/Shandong_Provincial_Committee_of_the_Chinese_Communist_Party",
    },
    {
        "id": 13,
        "name": "江山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山东省委常委（2022-12增补）",
        "current_org": "中国共产党山东省委员会",
        "source": "https://en.wikipedia.org/wiki/Shandong_Provincial_Committee_of_the_Chinese_Communist_Party",
    },
    {
        "id": 14,
        "name": "范波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山东省委常委（2024-04增补）",
        "current_org": "中国共产党山东省委员会",
        "source": "https://en.wikipedia.org/wiki/Shandong_Provincial_Committee_of_the_Chinese_Communist_Party",
    },
    # ── Predecessor governors ──
    {
        "id": 15,
        "name": "龚正",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1960-03",
        "birthplace": "江苏省苏州市",
        "education": "北京对外贸易学院",
        "party_join": "1986-03",
        "work_start": "1982-08",
        "current_post": "上海市市长",
        "current_org": "上海市人民政府",
        "source": "https://en.wikipedia.org/wiki/Gong_Zheng",
    },
    # ── Past Standing Committee: Lu Zhiyuan (former deputy secretary) ──
    {
        "id": 16,
        "name": "陆治原",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（离任山东）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Shandong_Provincial_Committee_of_the_Chinese_Communist_Party",
    },
]

# ── Organizations (id starts at 1) ────────────────────────────────────────

ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党山东省委员会", "type": "党委", "level": "省级", "parent": "", "location": "山东省济南市"},
    {"id": 2, "name": "山东省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "山东省济南市"},
    {"id": 3, "name": "中共山东省纪律检查委员会", "type": "党委", "level": "省级", "parent": "中国共产党山东省委员会", "location": "山东省济南市"},
    {"id": 4, "name": "中共山东省委组织部", "type": "党委", "level": "省级部门", "parent": "中国共产党山东省委员会", "location": "山东省济南市"},
    {"id": 5, "name": "中共山东省委宣传部", "type": "党委", "level": "省级部门", "parent": "中国共产党山东省委员会", "location": "山东省济南市"},
    {"id": 6, "name": "中共山东省委统战部", "type": "党委", "level": "省级部门", "parent": "中国共产党山东省委员会", "location": "山东省济南市"},
    {"id": 7, "name": "中共山东省委政法委", "type": "党委", "level": "省级部门", "parent": "中国共产党山东省委员会", "location": "山东省济南市"},
    {"id": 8, "name": "山东省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "山东省济南市"},
    {"id": 9, "name": "中国人民政治协商会议山东省委员会", "type": "政协", "level": "省级", "parent": "", "location": "山东省济南市"},
    {"id": 10, "name": "中共济南市委员会", "type": "党委", "level": "副省级", "parent": "中国共产党山东省委员会", "location": "山东省济南市"},
    {"id": 11, "name": "中共中央统一战线工作部", "type": "党委", "level": "中央级", "parent": "", "location": "北京市"},
    {"id": 12, "name": "湖南省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "湖南省长沙市"},
    {"id": 13, "name": "山西省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "山西省太原市"},
    {"id": 14, "name": "吉林省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "吉林省长春市"},
    {"id": 15, "name": "上海市人民政府", "type": "政府", "level": "省级", "parent": "", "location": "上海市"},
    {"id": 16, "name": "中国建筑集团有限公司", "type": "事业单位", "level": "中央级", "parent": "", "location": "北京市"},
    {"id": 17, "name": "生态环境部", "type": "事业单位", "level": "中央级", "parent": "", "location": "北京市"},
    {"id": 18, "name": "中央组织部", "type": "党委", "level": "中央级", "parent": "", "location": "北京市"},
]

# ── Positions ────────────────────────────────────────────────────────────

POSITIONS = [
    # Lin Wu - Party Secretary
    {"person_id": 1, "org_id": 1, "title": "山东省委书记", "start_date": "2022-12", "end_date": "present", "rank": "正省级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "山西省委书记", "start_date": "2021-06", "end_date": "2022-12", "rank": "正省级", "note": "前任职务"},
    {"person_id": 1, "org_id": 13, "title": "山西省省长", "start_date": "2019-12", "end_date": "2021-06", "rank": "正省级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "山西省常务副省长", "start_date": "2018", "end_date": "2019-12", "rank": "副省级", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "吉林省常务副省长", "start_date": "2017", "end_date": "2018", "rank": "副省级", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "吉林省委常委、组织部部长", "start_date": "2016", "end_date": "2017", "rank": "副省级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "湖南省委组织部常务副部长", "start_date": "2011", "end_date": "2016", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "湖南省娄底市委书记", "start_date": "2008", "end_date": "2011", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "湖南省娄底市代市长", "start_date": "2005", "end_date": "2008", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "湖南省经济委员会主任", "start_date": "2004", "end_date": "2005", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "湖南省经济贸易委员会主任", "start_date": "2003", "end_date": "2004", "rank": "正厅级", "note": ""},

    # Zhou Naixiang - Governor
    {"person_id": 2, "org_id": 2, "title": "山东省省长", "start_date": "2021-09", "end_date": "present", "rank": "正省级", "note": ""},
    {"person_id": 2, "org_id": 16, "title": "中国建筑集团董事长", "start_date": "2019-09", "end_date": "2021-09", "rank": "副省级", "note": "央企领导"},
    {"person_id": 2, "org_id": 10, "title": "苏州市委书记", "start_date": "2016-01", "end_date": "2019-09", "rank": "副省级", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "苏州市代市长、市长", "start_date": "2012-02", "end_date": "2016-01", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "江苏省住房和城乡建设厅副厅长", "start_date": "2010-10", "end_date": "2012-02", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "江苏省旅游局局长", "start_date": "2008", "end_date": "2010-10", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "江苏省泰州市副市长、市委常委", "start_date": "2003-07", "end_date": "2008", "rank": "副厅级", "note": ""},

    # Li Ganjie - Former Party Secretary / Governor
    {"person_id": 3, "org_id": 11, "title": "中央统战部部长", "start_date": "2025-04", "end_date": "present", "rank": "副国级", "note": "二十届中央政治局委员"},
    {"person_id": 3, "org_id": 18, "title": "中央组织部部长", "start_date": "2023-04", "end_date": "2025-04", "rank": "副国级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "山东省委书记", "start_date": "2021-09", "end_date": "2022-12", "rank": "正省级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "山东省省长", "start_date": "2020-04", "end_date": "2021-09", "rank": "正省级", "note": ""},
    {"person_id": 3, "org_id": 17, "title": "生态环境部部长", "start_date": "2018-03", "end_date": "2020-04", "rank": "正部级", "note": ""},
    {"person_id": 3, "org_id": 17, "title": "环境保护部部长", "start_date": "2017-06", "end_date": "2018-03", "rank": "正部级", "note": ""},

    # Liu Jiayi - Former Party Secretary
    {"person_id": 4, "org_id": 1, "title": "山东省委书记", "start_date": "2017-04", "end_date": "2021-09", "rank": "正省级", "note": ""},
    {"person_id": 4, "org_id": 17, "title": "审计署审计长", "start_date": "2008", "end_date": "2017", "rank": "正部级", "note": ""},

    # Standing committee members
    {"person_id": 5, "org_id": 1, "title": "山东省委常委、宣传部部长", "start_date": "2022-06", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "山东省委常委、组织部部长", "start_date": "2022-06", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "山东省委常委、统战部部长", "start_date": "2022-06", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 8, "org_id": 10, "title": "山东省委常委、济南市委书记", "start_date": "2022-06", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "山东省委常委、常务副省长", "start_date": "2022-06", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "山东省委常委、秘书长", "start_date": "2022-06", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "山东省委常委（前任）", "start_date": "2022-06", "end_date": "2022-09", "rank": "副省级", "note": "调离"},
    {"person_id": 12, "org_id": 3, "title": "山东省委常委、省纪委书记", "start_date": "2022-06", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "山东省委常委", "start_date": "2022-12", "end_date": "present", "rank": "副省级", "note": "2022年12月增补"},
    {"person_id": 14, "org_id": 1, "title": "山东省委常委", "start_date": "2024-04", "end_date": "present", "rank": "副省级", "note": "2024年4月增补"},

    # Gong Zheng - Former Governor
    {"person_id": 15, "org_id": 15, "title": "上海市市长", "start_date": "2020", "end_date": "present", "rank": "正省级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "山东省省长", "start_date": "2017-04", "end_date": "2020", "rank": "正省级", "note": ""},

    # Lu Zhiyuan - Former Deputy Secretary
    {"person_id": 16, "org_id": 1, "title": "山东省委副书记", "start_date": "2021-09", "end_date": "2023-10", "rank": "副省级", "note": ""},
]

# ── Relationships (person <-> person) ─────────────────────────────────────

RELATIONSHIPS = [
    # Lin Wu <-> Zhou Naixiang (current top duo)
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "省委书记—省长工作搭档（2022至今）", "overlap_org": "山东省", "overlap_period": "2022-12至今"},
    # Lin Wu <-> Li Ganjie (predecessor-successor)
    {"person_a": 1, "person_b": 3, "type": "前任后任", "context": "李干杰离任山东省委书记后由林武接任", "overlap_org": "中国共产党山东省委员会", "overlap_period": "2022-12"},
    # Zhou Naixiang <-> Li Ganjie (former duo + predecessor)
    {"person_a": 2, "person_b": 3, "type": "前任后任", "context": "周乃翔接替李干杰任山东省省长", "overlap_org": "山东省人民政府", "overlap_period": "2021-09"},
    # Zhou Naixiang <-> Li Ganjie (former colleagues in Shandong)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "李干杰任省委书记期间周乃翔任省长", "overlap_org": "中共山东省委/山东省政府", "overlap_period": "2021-09至2022-12"},
    # Li Ganjie <-> Liu Jiayi (predecessor-successor)
    {"person_a": 3, "person_b": 4, "type": "前任后任", "context": "刘家义离任山东省委书记后由李干杰接任", "overlap_org": "中国共产党山东省委员会", "overlap_period": "2021-09"},
    # Lin Wu <-> Liu Jiayi (predecessor-successor via Li Ganjie)
    {"person_a": 1, "person_b": 4, "type": "间接继任", "context": "刘家义后经李干杰再由林武接任山东省委书记", "overlap_org": "中国共产党山东省委员会", "overlap_period": "2017-2022"},
    # Zhou Naixiang <-> Gong Zheng (predecessor-successor)
    {"person_a": 2, "person_b": 15, "type": "前任后任", "context": "龚正离任山东省省长后由周乃翔接任", "overlap_org": "山东省人民政府", "overlap_period": "2021-09"},
    # Lin Wu <-> Lu Zhiyuan (former standing committee colleagues)
    {"person_a": 1, "person_b": 16, "type": "共事", "context": "陆治原任山东省委副书记期间林武任省委书记", "overlap_org": "中共山东省委", "overlap_period": "2022-12至2023-10"},
    # Zhou Naixiang <-> Lu Zhiyuan (former standing committee colleagues)
    {"person_a": 2, "person_b": 16, "type": "共事", "context": "陆治原任省委副书记期间周乃翔任省长", "overlap_org": "中共山东省委", "overlap_period": "2021-09至2023-10"},
    # Lin Wu <-> Xia Hongmin (standing committee)
    {"person_a": 1, "person_b": 12, "type": "共事", "context": "省纪委书记与省委书记同一届常委会", "overlap_org": "中共山东省委", "overlap_period": "2022至今"},
    # Lin Wu <-> Liu Qiang (standing committee)
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "济南市委书记与省委书记同一届常委会", "overlap_org": "中共山东省委", "overlap_period": "2022至今"},
    # Lin Wu <-> Zeng Zanrong (standing committee)
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "常务副省长与省委书记同一届常委会", "overlap_org": "中共山东省委", "overlap_period": "2022至今"},
    # Zhou Naixiang <-> Zeng Zanrong (government colleagues)
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "省长与常务副省长在省政府共事", "overlap_org": "山东省人民政府", "overlap_period": "2022至今"},
    # Zhou Naixiang <-> Liu Qiang (provincial + city level)
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "省长与济南市委书记同一届省委常委会", "overlap_org": "中共山东省委", "overlap_period": "2022至今"},
    # Zhou Naixiang <-> Xia Hongmin
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "省长与省纪委书记同一届省委常委会", "overlap_org": "中共山东省委", "overlap_period": "2022至今"},
    # Li Ganjie <-> Zhou Naixiang (former colleagues in Shandong government)
    {"person_a": 3, "person_b": 15, "type": "共事", "context": "李干杰任山东省长前龚正任山东省长", "overlap_org": "山东省人民政府", "overlap_period": "2017-2020"},
    # Lin Wu <-> Zhang Haibo (standing committee)
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "省委秘书长与省委书记同一届常委会", "overlap_org": "中共山东省委", "overlap_period": "2022至今"},
    # Lin Wu <-> Bai Yugang (standing committee)
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "组织部长与省委书记同一届常委会", "overlap_org": "中共山东省委", "overlap_period": "2022至今"},
    # All current standing committee members as a collective
    {"person_a": 5, "person_b": 6, "type": "共事", "context": "宣传部部长与组织部部长同属省委常委", "overlap_org": "中共山东省委", "overlap_period": "2022至今"},
    {"person_a": 5, "person_b": 7, "type": "共事", "context": "宣传部部长与统战部部长同属省委常委", "overlap_org": "中共山东省委", "overlap_period": "2022至今"},
    {"person_a": 6, "person_b": 7, "type": "共事", "context": "组织部部长与统战部部长同属省委常委", "overlap_org": "中共山东省委", "overlap_period": "2022至今"},
    {"person_a": 9, "person_b": 10, "type": "共事", "context": "常务副省长与省委秘书长同属省委常委", "overlap_org": "中共山东省委", "overlap_period": "2022至今"},
]


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    staging = _HERE
    db_path = staging / "山东省_network.db"
    gexf_path = staging / "山东省_network.gexf"

    print(f"Building Shandong province network...")
    print(f"  Database: {db_path}")
    print(f"  GEXF:     {gexf_path}")
    print()

    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    # Print summary
    print()
    print("Summary:")
    print(f"  Persons:        {len(PERSONS)}")
    print(f"  Organizations:  {len(ORGANIZATIONS)}")
    print(f"  Positions:      {len(POSITIONS)}")
    print(f"  Relationships:  {len(RELATIONSHIPS)}")
    print()

    # Verify files exist
    for p in [db_path, gexf_path]:
        if p.exists():
            print(f"  ✅ {p.name} ({p.stat().st_size / 1024:.1f} KB)")
        else:
            print(f"  ❌ {p.name} NOT FOUND")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
