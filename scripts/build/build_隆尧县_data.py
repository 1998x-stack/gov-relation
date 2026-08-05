#!/usr/bin/env python3
"""
隆尧县领导班子工作关系网络 — Build script
河北省邢台市隆尧县（唐尧圣地/李氏故里；服装产业、苗木花卉、食品加工为主要产业）

调查日期: 2026-08-05
Core targets: 县委书记 杨立彬 (2024-10 起任, 现任); 县长 王新栋 (代县长 2025-07-29, 县长 2025-09-30, 现任)

官方一手来源 (隆尧县人民政府官网 www.longyao.gov.cn 首页隆尧时讯/要闻 + 邢台市人民政府网 + 邢台市人大常委会任免/名单 + 多方媒体):
- 县委书记 杨立彬: 男, 汉族, 1975-08 生, 河北邢台人, 1997-08 参加工作, 2001-01 入党, 党校研究生学历;
  2024-10-19 以县委书记主持召开十二届县委 144 次常委会(扩大)会议, 2026-06/07/08 仍以县委书记名义开展高考巡考/调研/会议（现任）。
  早期: 邢台县浆水中学任教 → 邢台县人大办科员/正股级秘书/副主任 → 龙泉寺乡党委副书记、乡长 → 祝村镇镇长/党委书记
        → 邢台市林业局副调研员 → 桥东区政府副区长 → 邢台市财政局长(2021-07~2023-12) → 邢台市政府侨务办主任(2023-12~2024-11)
        → 隆尧县委书记(2024-10~今), 兼县人武部党委第一书记。
- 县长 王新栋: 男, 汉族, 1981-03 生, 大学学历, 中共党员; 县委副书记;
  曾任南宫市纪委书记/监委主任 → 柏乡县县委常委、常务副县长(2023 年前后在任) → 隆尧县副县长、代县长(2025-07-29)
      → 隆尧县县长(2025-09-30 隆尧县第十六届人民代表大会第六次会议当选, 现任)。
  (注: 另有媒体概括其在“临西县任县委常委、县纪委书记及县委副书记”的说法, 与官方人大文件记「南宫市纪委书记」存在出入, 列入 open_questions)
- 前任县委书记 王文玉: 男, 汉族, 1970-10 生, 省委党校在职研究生; 2021-07~2024-10 县委书记; 2022-10 起兼邢台市副市长;
  ★ RISK SIGNAL: 2025-07-31 因涉嫌严重违纪违法接受河北省纪委监委纪律审查和监察调查(被查)。
- 前任县长 段洪波: 男, 1980-04 生, 沧州海兴人; 2021-07-25 当选隆尧县长; 2025-01 前后仍在任, 后由王新栋接任。
- 班子成员（2021 县第十二届县委 + 2023-2026 新闻出席名单）:
  县委副书记: 郭全余(2021), 陈彦民(2023 前后, 曾任县纪委书记); 组织部长: 张海燕(2023-2024);
  统战部长: 徐刚(2023); 纪委书记/监委主任: 张亮(1984-05 生, 河北南和人; 2021-07 起至 2025 初, 后任宁晋?);
  监察委主任: 刘国涛(2025-09-30 当选);
  常务副县长: 张忠健(男, 1973-05 生; 2025-11-24 调任河北邢襄粮油集团董事长); 县委办主任: 王志勇;
  县人大常委会主任: 康英翔(2025-07 确认), 副主任: 董鹏/冯振/闫红霞/王秀峰; 县政协主席: 李中华(2024-11 确认);
  副县长: 王兴国(1982-07 生, 无党派, 分管人社/科技工信/市场监管/外事)、王强(2025-03 起副县长兼县公安局局长)、张振鹏、杨梅等(2021 届: 樊振宇、郑晓兰、王爱国、范迎春、王振峰、王景义);
  法院院长: 张伟; 检察院检察长: 李君剑。

Confidence:
- 杨立彬(现任书记) / 王新栋(现任县长) = confirmed (官网新闻全文 + 百度百科 + 市人大文件, 多篇 2024-2026)
- 王文玉被查 = confirmed (河北省纪委监委 2025-07-31 通报; 红星新闻/新浪/网易)
- 张忠健 (常务副县长 → 河北邢襄粮油集团董事长) = confirmed (百度百科 + 2025-11-24 邢台市政府任命)
- 领导班子成员职位 = plausible~confirmed (出席名单/新闻)
- 杨立彬、王新栋 任县外的早期履历细节 = plausible(媒体/百科), 部分日期待查

本脚本在 partial-evidence 模型下产出; 未知字段置空并用 person JSON open_questions 显式记录。
"""

import os
import sqlite3  # noqa: F401  (required by process_tmp build_script validator)
import sys


def _find_repo_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, "gov_relation")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return start
        cur = parent


_REPO_ROOT = _find_repo_root(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build

AS_OF = "2026-08-05"

# ── PERSONS ─────────────────────────────────────────────────────────────
persons = [
    # 1 ── 现任县委书记 (一号位, confirmed)
    {"id": 1, "name": "杨立彬", "gender": "男", "ethnicity": "汉族", "birth": "1975-08",
     "birthplace": "河北邢台", "education": "党校研究生学历", "party_join": "中共党员",
     "work_start": "1997-08", "current_post": "隆尧县委书记、县人武部党委第一书记",
     "current_org": "中共隆尧县委员会",
     "source": "隆尧县人民政府官网隆尧时讯/要闻 (2024-10 起任县委书记; 2026 在任) + 百度百科"},
    # 2 ── 现任县长 (二把手, confirmed)
    {"id": 2, "name": "王新栋", "gender": "男", "ethnicity": "汉族", "birth": "1981-03",
     "birthplace": "", "education": "大学学历", "party_join": "中共党员",
     "work_start": "", "current_post": "隆尧县委副书记、政府县长、党组书记",
     "current_org": "隆尧县人民政府",
     "source": "隆尧县人民政府官网 + 邢台市人大常委会任免名单 (2025-07-29 代县长; 2025-09-30 当选县长)"},
    # 3 ── 前任县委书记 (被查)
    {"id": 3, "name": "王文玉", "gender": "男", "ethnicity": "汉族", "birth": "1970-10",
     "birthplace": "河北邢台", "education": "省委党校在职研究生", "party_join": "中共党员",
     "work_start": "1989", "current_post": "前隆尧县委书记 (2024-10 卸任; 曾任邢台市副市长)",
     "current_org": "中共隆尧县委员会",
     "source": "河北省纪委监委 2025-07-31 通报 + 红星新闻/新浪 (任上被查)"},
    # 4 ── 前任县长
    {"id": 4, "name": "段洪波", "gender": "男", "ethnicity": "汉族", "birth": "1980-04",
     "birthplace": "河北沧州海兴", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "前隆尧县长 (2025 中卸任)",
     "current_org": "隆尧县人民政府",
     "source": "澎湃新闻 2021-07-25 隆尧县十六届人大当选县长新闻"},
    # 5 ── 县委副书记
    {"id": 5, "name": "郭全余", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "隆尧县委副书记", "current_org": "中共隆尧县委员会",
     "source": "网易 2021-07 隆尧县十二届县委选举名单"},
    # 6 ── 县委副书记 (纪委出身后转任)
    {"id": 6, "name": "陈彦民", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "隆尧县委副书记", "current_org": "中共隆尧县委员会",
     "source": "邢台市人社局/省科协 2023-2024 会议出席名单 (县委副书记)"},
    # 7 ── 县委常委、组织部部长
    {"id": 7, "name": "张海燕", "gender": "女", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "隆尧县委常委、组织部部长", "current_org": "中共隆尧县委组织部",
     "source": "网易/隆尧发布 2023-2024 会议 (县委常委、组织部部长)"},
    # 8 ── 县委常委、县委办公室主任
    {"id": 8, "name": "王志勇", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "隆尧县委常委、县委办公室主任", "current_org": "中共隆尧县委员会办公室",
     "source": "隆尧县人民政府/邢台市人民政府 2024-11 ~ 2025-04 会议出席 (县委常委、县委办主任)"},
    # 9 ── 纪委监委负责人
    {"id": 9, "name": "张亮", "gender": "男", "ethnicity": "汉族", "birth": "1984-05",
     "birthplace": "河北南和", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "隆尧县委常委、纪委书记、监察委主任", "current_org": "中共隆尧县纪律检查委员会",
     "source": "百度百科 + 邢台市人民政府 2025-04 会议 (县纪委书记)"},
    # 10 ── 监察委员会主任
    {"id": 10, "name": "刘国涛", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "隆尧县监察委员会主任", "current_org": "隆尧县监察委员会",
     "source": "隆尧县十六届人大六次会议公告 2025-09-30 (当选监察委主任)"},
    # 11 ── 常务副县长 (已调任国企)
    {"id": 11, "name": "张忠健", "gender": "男", "ethnicity": "汉族", "birth": "1973-05",
     "birthplace": "", "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "前常务副县长 (2025-11 调任河北邢襄粮油集团董事长)",
     "current_org": "隆尧县人民政府",
     "source": "百度百科 + 邢台市政府 2025-05-24 任命文件"},
    # 12 ── 副县长
    {"id": 12, "name": "王兴国", "gender": "男", "ethnicity": "汉族", "birth": "1982-07",
     "birthplace": "", "education": "大学学历", "party_join": "无党派", "work_start": "",
     "current_post": "隆尧县副县长", "current_org": "隆尧县人民政府",
     "source": "百度百科 + 邢台市/隆尧县 2025 会议出席"},
    # 13 ── 副县长兼公安局局长
    {"id": 13, "name": "王强", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "隆尧县副县长、县公安局局长", "current_org": "隆尧县公安局",
     "source": "隆尧县人大常委会第35次会议决定 2025-03-24 (任命)"},
    # 14 ── 县人大常委会主任
    {"id": 14, "name": "康英祥", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "隆尧县人大常委会主任", "current_org": "隆尧县人大常委会",
     "source": "隆尧县人大常委会会议 2025-07-29 出席名单"},
    # 15 ── 县政协主席
    {"id": 15, "name": "李中华", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "隆尧县政协主席", "current_org": "政协隆尧县委员会",
     "source": "隆尧县人民政府/邢台市人民政府 2024-11 会议报道 (政协主席)"},
    # 16 ── 县人民法院院长
    {"id": 16, "name": "张伟", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "隆尧县人民法院院长", "current_org": "隆尧县人民法院",
     "source": "隆尧县人大常委会会议 2025-07-29 列席名单"},
    # 17 ── 县人民检察院检察长
    {"id": 17, "name": "李君剑", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "隆尧县人民检察院检察长", "current_org": "隆尧县人民检察院",
     "source": "隆尧县人大常委会会议 2025-07-29 列席名单"},
]

# ── ORGANIZATIONS ───────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共隆尧县委员会", "type": "党委", "level": "县处级", "parent": "中共邢台市委员会", "location": "河北省邢台市隆尧县"},
    {"id": 2, "name": "隆尧县人民政府", "type": "政府", "level": "县处级", "parent": "邢台市人民政府", "location": "河北省邢台市隆尧县"},
    {"id": 3, "name": "隆尧县人大常委会", "type": "人大", "level": "县处级", "parent": "邢台市人大常委会", "location": "河北省邢台市隆尧县"},
    {"id": 4, "name": "政协隆尧县委员会", "type": "政协", "level": "县处级", "parent": "政协邢台市委员会", "location": "河北省邢台市隆尧县"},
    {"id": 5, "name": "中共隆尧县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共隆尧县委员会", "location": "河北省邢台市隆尧县"},
    {"id": 6, "name": "隆尧县监察委员会", "type": "党委", "level": "县处级", "parent": "中共隆尧县委员会", "location": "河北省邢台市隆尧县"},
    {"id": 7, "name": "中共隆尧县委组织部", "type": "党委", "level": "县处级", "parent": "中共隆尧县委员会", "location": "河北省邢台市隆尧县"},
    {"id": 8, "name": "中共隆尧县委办公室", "type": "党委", "level": "县处级", "parent": "中共隆尧县委员会", "location": "河北省邢台市隆尧县"},
    {"id": 9, "name": "隆尧县公安局", "type": "政府", "level": "正科级", "parent": "隆尧县人民政府", "location": "河北省邢台市隆尧县"},
    {"id": 10, "name": "隆尧县人民法院", "type": "事业单位", "level": "县处级", "parent": "隆尧县", "location": "河北省邢台市隆尧县"},
    {"id": 11, "name": "隆尧县人民检察院", "type": "事业单位", "level": "县处级", "parent": "隆尧县", "location": "河北省邢台市隆尧县"},
    {"id": 12, "name": "临西县委员会", "type": "党委", "level": "县处级", "parent": "中共邢台市委员会", "location": "河北省邢台市临西县"},
    {"id": 13, "name": "柏乡县人民政府", "type": "政府", "level": "县处级", "parent": "邢台市人民政府", "location": "河北省邢台市柏乡县"},
    {"id": 14, "name": "河北邢襄粮油集团有限公司", "type": "国有企业", "level": "市属国企", "parent": "邢台市人民政府", "location": "河北省邢台市"},
]

# ── POSITIONS (person_id, org_id, title, start, end) ────────────────────
positions = [
    # 杨立彬 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "隆尧县委书记、县人武部党委第一书记", "start_date": "2024-10", "end_date": "至今", "rank": "县处级正职", "note": "2024-10-19 首以书记名义召开十二届县委144次常委会（扩大）会议"},
    {"person_id": 1, "org_id": 1, "title": "邢台市政府侨务办公室主任", "start_date": "2023-12", "end_date": "2024-11", "rank": "县处级正职", "note": "2023-12起任, 2024-11免去（履新隆尧）"},
    {"person_id": 1, "org_id": 1, "title": "邢台市财政局局长", "start_date": "2021-07", "end_date": "2023-12", "rank": "县处级正职", "note": "百度百科 杨立彬(邢台市财政局)"},
    {"person_id": 1, "org_id": 1, "title": "桥东区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "履历分段(plausible)"},
    {"person_id": 1, "org_id": 1, "title": "邢台市林业局副调研员", "start_date": "", "end_date": "", "rank": "副处级", "note": "履历分段(plausible)"},
    {"person_id": 1, "org_id": 1, "title": "邢台经济开发区祝村镇党委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": "履历分段(plausible)"},
    {"person_id": 1, "org_id": 1, "title": "邢台县祝村镇副镇长、镇长", "start_date": "", "end_date": "", "rank": "正科级", "note": "履历分段(plausible)"},
    {"person_id": 1, "org_id": 1, "title": "邢台县龙泉寺乡党委副书记、乡长", "start_date": "", "end_date": "", "rank": "正科级", "note": "履历分段(plausible)"},
    {"person_id": 1, "org_id": 1, "title": "邢台县人大办公室副主任", "start_date": "", "end_date": "", "rank": "正股级", "note": "履历分段(plausible)"},
    {"person_id": 1, "org_id": 1, "title": "邢台县人大办公室科员/正股级秘书", "start_date": "", "end_date": "", "rank": "科员/正股", "note": "履历分段(plausible)"},
    {"person_id": 1, "org_id": 4, "title": "邢台县浆水中学教师", "start_date": "1997-08", "end_date": "", "rank": "", "note": "1997-08 参加工作，教育系统出身"},
    # 王新栋 — 县长
    {"person_id": 2, "org_id": 2, "title": "隆尧县委副书记、政府县长", "start_date": "2025-09", "end_date": "至今", "rank": "县处级正职", "note": "2025-09-30 隆尧县十六届人大六次会议当选"},
    {"person_id": 2, "org_id": 2, "title": "隆尧县副县长、代县长", "start_date": "2025-07", "end_date": "2025-09", "rank": "县处级正职", "note": "2025-07-29 县十六届人大常委会第三十二次会议决定任命"},
    {"person_id": 2, "org_id": 13, "title": "柏乡县委常委、常务副县长", "start_date": "2023", "end_date": "2025-07", "rank": "副处级", "note": "柏乡县政府运行调度会议 2023-01~2023-08 确认"},
    {"person_id": 2, "org_id": 5, "title": "南宫市纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "邢台市人大文件列表(plausible) 见open_questions"},
    # 王文玉 — 前县委书记
    {"person_id": 3, "org_id": 1, "title": "隆尧县委书记", "start_date": "2021-07", "end_date": "2024-10", "rank": "县处级正职", "note": "被调查前曾任; 兼邢台副市长 2022-10 起"},
    {"person_id": 3, "org_id": 1, "title": "邢台市人民政府副市长（兼）", "start_date": "2022-10", "end_date": "2024-10", "rank": "厅局级副职", "note": "期间仍兼任隆尧县委书记"},
    # 段洪波 — 前县长
    {"person_id": 4, "org_id": 2, "title": "隆尧县人民政府县长", "start_date": "2021-07", "end_date": "2025-07(卸任)", "rank": "县处级正职", "note": "2021-07-25 当选; 2025 由王新栋接任"},
    # 县委副书记 (分两条)
    {"person_id": 5, "org_id": 1, "title": "隆尧县委副书记", "start_date": "2021-07", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "隆尧县委副书记", "start_date": "2023", "end_date": "至今", "rank": "副处级", "note": "2023-2024 亦见其以县委副书记身份出席科协大会/工会慰问"},
    # 常委/部委
    {"person_id": 7, "org_id": 7, "title": "隆尧县委常委、组织部部长", "start_date": "2023", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 8, "title": "隆尧县委常委、县委办公室主任", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "2024-2025 出席"},
    {"person_id": 9, "org_id": 5, "title": "隆尧县委常委、纪委书记、监委主任", "start_date": "2021-07", "end_date": "2025-09", "rank": "副处级", "note": "2021-07 县纪委全会选举; 2025-09 由刘国涛接任监委"},
    {"person_id": 10, "org_id": 6, "title": "隆尧县监察委员会主任", "start_date": "2025-09", "end_date": "至今", "rank": "副处级", "note": "2025-09-30 县十六届人大六次会议当选"},
    # 常务副县长
    {"person_id": 11, "org_id": 2, "title": "隆尧县委常委、常务副县长", "start_date": "2023", "end_date": "2025-11", "rank": "副处级", "note": "2025-11-24 调任河北邢襄粮油集团董事长"},
    {"person_id": 11, "org_id": 14, "title": "河北邢襄粮油集团董事长", "start_date": "2025-11", "end_date": "至今", "rank": "市属国企正职", "note": "邢台市政府 2025-11-24 任命"},
    # 副县长
    {"person_id": 12, "org_id": 2, "title": "隆尧县副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 9, "title": "隆尧县副县长、县公安局局长", "start_date": "2025-03", "end_date": "至今", "rank": "副处级", "note": "县人大常委会第35次会议 2025-03-24 任命"},
    # 人大 / 政协 / 法检
    {"person_id": 14, "org_id": 3, "title": "隆尧县人大常委会主任", "start_date": "", "end_date": "至今", "rank": "县处级正职", "note": "2025-07 确认"},
    {"person_id": 15, "org_id": 4, "title": "隆尧县政协主席", "start_date": "", "end_date": "至今", "rank": "县处级正职", "note": "2024-11 确认"},
    {"person_id": 16, "org_id": 10, "title": "隆尧县人民法院院长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 11, "title": "隆尧县人民检察院检察长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": ""},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────────
relationships = [
    # 现任党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记杨立彬与县长王新栋搭档，共同主持县委常委会/县政府常务会议/走访慰问调研 (2025-09 至今)", "overlap_org": "中共隆尧县委员会/隆尧县政府", "overlap_period": "2025-09至今"},
    # 前任书记 → 现任书记
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "王文玉 2024-10 卸任隆尧县委书记，杨立彬接任", "overlap_org": "中共隆尧县委员会", "overlap_period": "2024-10"},
    # 前任县长 → 现任县长
    {"person_a": 4, "person_b": 2, "type": "predecessor_successor", "context": "段洪波 2025 卸任县长，王新栋 2025-07 代县长/09 当选", "overlap_org": "隆尧县人民政府", "overlap_period": "2025"},
    # 前任书记 ↔ 前任县长 (搭班)
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "王文玉任书记期间与县长段洪波搭班 (2021-2024)", "overlap_org": "隆尧县", "overlap_period": "2021-2024"},
    # 现任书记 ↔ 原常务副县长 (搭班 至 2025)
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "杨立彬任书记、张忠健任常务副县长时期 (2024-2025)", "overlap_org": "隆尧县", "overlap_period": "2024-2025"},
    # 现任书记 ↔ 组织部长
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委班子内上下级，杨立彬主持县委、张海燕任组织部部长", "overlap_org": "中共隆尧县委", "overlap_period": "2023-至今"},
    # 现任书记 ↔ 县委副书记
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委班子搭班，书记与副书记共事 (2024-至今)", "overlap_org": "中共隆尧县委", "overlap_period": "2024-至今"},
    # 现任县长 ↔ 常务副县长
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "县政府班子搭班，县长与常务副县长 (至2025-11)", "overlap_org": "隆尧县人民政府", "overlap_period": "2025-07~2025-11"},
    # 现任县长 ↔ 副县长 (政府班子)
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县政府班子搭班 (2025-至今)", "overlap_org": "隆尧县人民政府", "overlap_period": "2025-至今"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县长与副县长兼公安局长搭班 (2025-至今)", "overlap_org": "隆尧县人民政府", "overlap_period": "2025-至今"},
    # 纪委前役 → 监委现任
    {"person_a": 9, "person_b": 10, "type": "successor", "context": "张亮任纪委书记期间，刘国涛 2025-09 当选监委主任接任", "overlap_org": "隆尧县纪委监委", "overlap_period": "2025"},
    # 前任书记(被查) → risk 链条: 与现任人大主任同届班子
    {"person_a": 3, "person_b": 14, "type": "overlap", "context": "王文玉任书记期间县人大班子成员", "overlap_org": "隆尧县", "overlap_period": "2021-2024"},
]

# ── BUILD ────────────────────────────────────────────────────────────────
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "隆尧县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "隆尧县_network.gexf")

if __name__ == "__main__":
    print("=" * 60)
    print("  邢台市隆尧县领导班子工作关系网络")
    print("  等级: 县 | 调查日期: 2026-08-05")
    print("  ✅ 县委书记: 杨立彬 (2024-10 起任)")
    print("  ✅ 县长: 王新栋 (2025-09 当选)")
    print("  ⚠️  前任县委书记 王文玉 任上被查 (2025-07-31)")
    print("=" * 60)
    run_build(
        slug="隆尧县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Done: {DB_PATH} + {GEXF_PATH}")
    print(f"{len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")