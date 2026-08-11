#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 定州市 leadership network.

Province: 河北省 (保定市代管/省直管县级市, 副厅级)
Level: 县级市
Research date: 2026-08-11
Task: hebei_定州市 (targets 市委书记 & 市长)

Data-integrity note:
  Research was completed via Exa web-search indexed highlights of the official
  定州市人民政府 website (dzs.gov.cn), 定州新闻网/定州日报 (dingzhoudaily.com),
  河北新闻网/长城网, 澎湃新闻, 人民网 河北频道, 百度/360百科 and 河北省纪委监委
  website. Baidu Baike direct fetch returned 403 and r.jina.ai transport failed,
  so encyclopedia data is cited via its own cached mirrors (114390.com,
  baike.so.com, qiuwenbaike.cn) and media reproductions. All claims carry
  confidence labels; unresolved biographical fields are flagged in
  `open_questions`/report gaps instead of being invented.

Key confirmed facts:
  - Current 市委书记: 张才芳 (1971-02, 河北武安人, 2024-06 起任市委书记; 前
    定州市长 2021-07当选). 2024-06-23 定州市委常委会新闻已以"市委书记"身份
    报道; 2026-05 多篇 市委常委会/全会新闻仍在任。
  - Current 市长: 邓艳学 (1976-08, 省委党校在职研究生; 2024-10 市委副书记、
    代市长, 2025-01-22 市九届人大六次会议当选市长; 2026-05 政府常务会议仍在任)。
  - Predecessor 市委书记: 张涛 (河北涿州人, 2019.01 定州市长, 2021.01 书记,
    2024-06 调任张家口市委常委、常务副市长, 2025-11 当选张家口市市长)。
  - 2020-11-05 前任书记王东群(2016.10-2020.11)主动投案, 2021-11 省委九届
    十四次全会追认给予留党察看一年处分; 其任内与市长陈业鹏长期不和, 陈
    2018-07 被免职(澎湃 2018-07 报道); 政协副主席、党组副书记刘立军 2020-11-01
    主动投案(王东群投案前4天)。
  - 现任 市委常委/领导: 人大主任周胜会, 政协主席张宝生(定州人), 市委副书记
    吕仲华(plausible)/刘力威(曾任副市长2017-2023, 百度百科载现任市委副书记),
    纪委书记孙振林, 组织部长葛亮, 常务副市长陈凯, 市委办主任李辉, 宣传部长
    张充, 人武部长张仲振, 副市长徐型伟/胡晓红/蔡红宇/邢伟涛/刘伟。

Uncertainties kept explicit: 邓艳宇 2018 年前履历未查到; 张才芳 1992-2009 早期
履历缺; 陈业鹏 2018-07 免职后去向未查到; 王静群处分后最终职级未公开;
吕仲华/张二文/王传琼等确切分工部分未决 — all listed in open_questions and gaps.
"""

import os
import sys
from pathlib import Path

def _find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(6):
        if (cur / "gov_relation").is_dir():
            return cur
        nxt = cur.parent
        if nxt == cur:
            break
        cur = nxt
    raise RuntimeError(f"could not locate repo root from {start}")

_REPO_ROOT = _find_repo_root(Path(__file__).parent)
for _p in (_REPO_ROOT, os.path.join(_REPO_ROOT, "scripts")):
    if _p not in sys.path:
        sys.path.insert(0, str(_p))

import sqlite3  # noqa: E402

from gov_relation.runner import run_build  # noqa: E402

SLUG = "定州市"
DB_PATH = Path(__file__).parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).parent / f"{SLUG}_network.gexf"
AS_OF = "2026-08-11"

# ────────────────────────────────────────────────────────────────────────────
# Persons — 定州市领导班子 + 关键前任 (核心书记/市长履历 confirmed, 其余 partial)
# ────────────────────────────────────────────────────────────────────────────
persons = [
    # ── 现任市委书记 (core target 1) ──
    {
        "id": 1,
        "name": "张才芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-02",
        "birthplace": "河北省武安市",
        "education": "河北省委党校研究生学历，教育学学士",
        "party_join": "1997-01",
        "work_start": "1992-06",
        "current_post": "定州市委书记（副厅级）",
        "current_org": "中共定州市委员会",
        "source": "360百科/114名人大全/定州新闻网·澎湃 (2024-06 任书记, 2021-05 任定州代市长)",
    },
    # ── 现任市委副书记、市长 (core 2) ──
    {
        "id": 2,
        "name": "邓艳学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-08",
        "birthplace": "",
        "education": "省委党校在职研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、市长（副厅级）",
        "current_org": "定州市人民政府",
        "source": "定州市人民政府领导之窗 (2024-10-18 维护); 定州新闻网 2025-01-22 当选市长",
    },
    # ── 现任班子 ──
    {
        "id": 3,
        "name": "周胜会",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "定州市人大常委会",
        "source": "定州新闻网/长城网 2021-07 市九届人大一次会议当选; 2025-01 仍为主席",
    },
    {
        "id": 4,
        "name": "张宝生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-10",
        "birthplace": "河北定州",
        "education": "中央党校函授学院政法专业，大学学历",
        "party_join": "1993-08",
        "work_start": "1990-08",
        "current_post": "市政协主席",
        "current_org": "政协定州市委员会",
        "source": "天天百科 张宝生(定州市政协主席); 长城网 2021-07 当选政协主席",
    },
    {
        "id": 5,
        "name": "吕仲华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记（plausible）",
        "current_org": "中共定州市委员会",
        "source": "2021-07/2024-02/2025-01 多次两会主席台并列顺序在市长之后推断",
    },
    {
        "id": 6,
        "name": "孙振林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、纪委书记、市监委主任",
        "current_org": "定州市纪委监委",
        "source": "定州市人民政府网 2024-12-13 八届市委第七轮巡察动员部署会（市委巡察工作领导小组常务副组长）",
    },
    {
        "id": 7,
        "name": "张二文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委（具体分工待核）",
        "current_org": "中共定州市委员会",
        "source": "2021-07/2024-02/2025-01 多次两会主席台名单; 2024-06 招商活动随行",
    },
    {
        "id": 8,
        "name": "张仲田",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市人武部部长",
        "current_org": "定州市人民武装部",
        "source": "定州新闻网 2022-08-03 民兵训练基地启用(主持人); 2024-08-01 人武部党委第一书记任职大会(表态发言)",
    },
    {
        "id": 9,
        "name": "刘力威",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1980-07",
        "birthplace": "河北安国",
        "education": "河北科技师范学院机械设计制造及其自动化专业，大学学历",
        "party_join": "2000-12",
        "work_start": "2003-08",
        "current_post": "市委副书记（百度百科；曾任副市长）",
        "current_org": "中共定州市委员会",
        "source": "百度百科 刘力威(定州市委副书记); 2017-02 当选定州市副市长; 河北科技师范学院校友简介(2003届省委选调生)",
    },
    {
        "id": 10,
        "name": "葛亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共定州市委员会",
        "source": "定州市人民政府网 2024-12-13 巡察动员部署(巡察工作领导小组副组长、宣读授权)",
    },
    {
        "id": 11,
        "name": "陈凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市政府常务副市长",
        "current_org": "定州市人民政府",
        "source": "定州市人民政府网 2025-03-06 市级总河长和市级河长名单（唐河、小清河市级河长）",
    },
    {
        "id": 12,
        "name": "李辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市委办公室主任",
        "current_org": "中共定州市委员会",
        "source": "定州日报 2024-07-23 署名文章(市委常委、办公室主任); 河北大学新闻传播学院 调研报道(市委秘书长)",
    },
    {
        "id": 13,
        "name": "张充",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共定州市委员会",
        "source": "河北大学新闻传播学院 调研报道(市委常委、宣传部长张充); 两会主席台名单",
    },
    {
        "id": 14,
        "name": "徐型伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "定州市人民政府",
        "source": "定州市人民政府网 2025-03-06 市级河长名单（磁河·木刀沟市级河长）",
    },
    {
        "id": 15,
        "name": "胡晓红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "定州市人民政府",
        "source": "定州市人民政府网 2025-03-06 市级河长名单（护城河市级河长）",
    },
    {
        "id": 16,
        "name": "蔡红宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "定州市人民政府",
        "source": "定州市人民政府网 2025-03-06 市级河长名单（孟良河、南水北调中线干线市级河长）",
    },
    {
        "id": 17,
        "name": "邢伟涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "定州市人民政府",
        "source": "定州市人民政府网 2025-03-06 市级河长名单（沙河灌渠总干渠市级河长）",
    },
    {
        "id": 18,
        "name": "刘伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "定州市人民政府",
        "source": "定州市人民政府网 2025-03-06 市级河长名单（沙河市级河长）",
    },
    # ── 前任一书记/市长 (履历关键节点 confirmed) ──
    {
        "id": 19,
        "name": "张涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-03",
        "birthplace": "河北省涿州市",
        "education": "河北农业大学植物保护专业（1994-07 毕业），在职研究生、管理学博士",
        "party_join": "1992-12",
        "work_start": "1994-07",
        "current_post": "张家口市委副书记、市长（兼经开区管委会主任）",
        "current_org": "张家口市人民政府",
        "source": "百度百科 张涛(张家口市长); 求闻百科; 长城网 2019-01 当选定州市长; 维基百科",
    },
    {
        "id": 20,
        "name": "王东群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-03",
        "birthplace": "河北省滦州市",
        "education": "大学学历（唐山教育学院英语专业；中国政法大学法学 函授）",
        "party_join": "1993-09",
        "work_start": "1980-08",
        "current_post": "已处分（定州市委原书记；2021-11 留党察看一年）",
        "current_org": "",
        "source": "河北省纪委监委 2020-11-05 通报+简历; 中央纪委网站; 新京报; 澎湃 2021-11 处分追认",
    },
    {
        "id": 21,
        "name": "陈业鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-06",
        "birthplace": "河北省阜平县",
        "education": "省委党校在职研究生班法学专业，研究生学历",
        "party_join": "1988-12",
        "work_start": "1984-09",
        "current_post": "已免职（原定州市长；2018-07 职务被调整）",
        "current_org": "",
        "source": "澎湃新闻 2017-02 当选定州市长(附简历); 澎湃/上游新闻 2018-07 因与王东群不和免职",
    },
    {
        "id": 22,
        "name": "刘立军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已投案（原市政协副主席、党组副书记；2020-11-01 主动投案）",
        "current_org": "",
        "source": "上游新闻 2021-11-22（王东群投案前4天刘立军主动投案）",
    },
    {
        "id": 23,
        "name": "李军辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已卸任（原定州市长 2014-2016）",
        "current_org": "",
        "source": "保定定州历任市长列表(2014.01-2016.12); 政务生涯细节未公开",
    },
    {
        "id": 24,
        "name": "赵志栋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已卸任（原定州市委书记 2012-2016）",
        "current_org": "",
        "source": "保定定州历任市委书记列表(2012.05-2016.10); 履历细节未公开",
    },
]

# ────────────────────────────────────────────────────────────────────────────
# Organizations
# ────────────────────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共定州市委员会", "type": "党委", "level": "副厅级", "parent": "河北省委", "location": "河北省定州市"},
    {"id": 2, "name": "定州市人民政府", "type": "政府", "level": "副厅级", "parent": "河北省政府", "location": "河北省定州市"},
    {"id": 3, "name": "定州市人大常委会", "type": "人大", "level": "副厅级", "parent": "中共定州市委", "location": "河北省定州市"},
    {"id": 4, "name": "政协定州市委员会", "type": "政协", "level": "副厅级", "parent": "中共定州市委", "location": "河北省定州市"},
    {"id": 5, "name": "定州市纪委监委", "type": "纪委", "level": "副厅级", "parent": "中共定州市委", "location": "河北省定州市"},
    {"id": 6, "name": "定州市人民武装部", "type": "人武部", "level": "团级", "parent": "保定军分区", "location": "河北省定州市"},
    {"id": 7, "name": "定州经济开发区（高新区）", "type": "开发区", "level": "", "parent": "定州市人民政府", "location": "河北省定州市"},
    {"id": 8, "name": "河北省科学技术厅", "type": "省直机关", "level": "厅级", "parent": "河北省人民政府", "location": "河北省石家庄市"},
    {"id": 9, "name": "张家口市人民政府", "type": "政府", "level": "厅级", "parent": "河北省人民政府", "location": "河北省张家口市"},
    {"id": 10, "name": "保定市人民政府", "type": "政府", "level": "厅级", "parent": "河北省人民政府", "location": "河北省保定市"},
    {"id": 11, "name": "中共邯郸市邯山区委", "type": "党委", "level": "县处级", "parent": "邯郸市委", "location": "河北省邯郸市"},
    {"id": 12, "name": "邯郸市邯山区人民政府", "type": "政府", "level": "县处级", "parent": "中共邯山区委", "location": "河北省邯郸市"},
    {"id": 13, "name": "中共磁县县委", "type": "党委", "level": "县处级", "parent": "邯郸市委", "location": "河北省邯郸市磁县"},
    {"id": 14, "name": "磁县经济开发区（漳河经济开发区）", "type": "开发区", "level": "", "parent": "中共磁县县委", "location": "河北省邯郸市磁县"},
    {"id": 15, "name": "中共顺平县委员会", "type": "党委", "level": "县处级", "parent": "保定市委", "location": "河北省保定市顺平县"},
    {"id": 16, "name": "顺平县人民政府", "type": "政府", "level": "县处级", "parent": "中共顺平县委", "location": "河北省保定市顺平县"},
    {"id": 17, "name": "中共唐县委员会", "type": "党委", "level": "县处级", "parent": "保定市委", "location": "河北省保定市唐县"},
    {"id": 18, "name": "乐亭县人民政府", "type": "政府", "level": "县处级", "parent": "中共乐亭县委", "location": "河北省唐山市乐亭县"},
    {"id": 19, "name": "唐山市（市直机关/园区）", "type": "政府", "level": "厅级", "parent": "河北省人民政府", "location": "河北省唐山市"},
    {"id": 20, "name": "中共邯郸县委", "type": "党委", "level": "县处级", "parent": "邯郸市委", "location": "河北省邯郸市"},
    {"id": 21, "name": "邯郸工业园区/邯山经济开发区", "type": "开发区", "level": "", "parent": "邯郸市政府", "location": "河北省邯郸市"},
]

# ────────────────────────────────────────────────────────────────────────────
# Positions — all titled rows with dates; confidence in note
# ────────────────────────────────────────────────────────────────────────────
positions = [
    # 张才芳 (1)
    {"person_id": 1, "org_id": 1, "title": "定州市委书记", "start_date": "2024-06", "end_date": "present", "rank": "副厅级",
     "note": "2024-06 起接替张涛任市委书记; 2024-06-23 首次以书记身份主持市委常委会 (confirmed)"},
    {"person_id": 1, "org_id": 2, "title": "定州市委副书记、市长", "start_date": "2021-05", "end_date": "2024-06", "rank": "副厅级",
     "note": "2021-05-19 领导干部大会宣布任市委副书记、代市长; 2021-07 当选市长 (confirmed)"},
    {"person_id": 1, "org_id": 13, "title": "磁县县委书记", "start_date": "2019-09", "end_date": "2021-05", "rank": "县处级正职",
     "note": "兼任漳河经济开发区党工委书记、磁县经济开发区党工委书记; 2019-09-07 干部大会宣布 (confirmed)"},
    {"person_id": 1, "org_id": 12, "title": "邯山区委副书记、区长", "start_date": "2017-02", "end_date": "2019-09", "rank": "县处级正职",
     "note": "2016-12 区委副书记、区长候选人; 2017-02 当选 (confirmed)"},
    {"person_id": 1, "org_id": 12, "title": "邯山区常务副区长", "start_date": "2014", "end_date": "2016-12", "rank": "县处级副职",
     "note": "兼任邯郸工业园区管委会主任、邯山经济开发区管委会主任; 年份按自述'历任'推定 (plausible)"},
    {"person_id": 1, "org_id": 20, "title": "邯郸县委常委、政府副县长", "start_date": "2009", "end_date": "2014", "rank": "县处级副职",
     "note": "公开资料仅记'历任邯郸县委常委、政府副县长'，具体起止待查 (plausible)"},
    {"person_id": 1, "org_id": 21, "title": "邯郸工业园区管委会主任、邯山经济开发区管委会主任（兼）", "start_date": "", "end_date": "2016-12", "rank": "",
     "note": "兼任职务，随邯山区职务变动 (plausible)"},
    # 邓艳学 (2)
    {"person_id": 2, "org_id": 2, "title": "定州市委副书记、市长", "start_date": "2025-01", "end_date": "present", "rank": "副厅级",
     "note": "2024-10 任市委副书记、代市长(领导之窗 2024-10-18); 2025-01-22 市九届人大六次会议当选市长 (confirmed)"},
    {"person_id": 2, "org_id": 17, "title": "唐县县委书记", "start_date": "2021-05", "end_date": "2024-10", "rank": "县处级正职",
     "note": "2021-05-18 唐县领导干部大会宣布任县委书记; 2023-08 巡视整改通报仍为书记 (confirmed)"},
    {"person_id": 2, "org_id": 15, "title": "顺平县委副书记、县长", "start_date": "2018-09", "end_date": "2021-05", "rank": "县处级正职",
     "note": "2018-09 中国网报道为顺平县委副书记、代县长; 2020-09 报道为县长; 2021-05-20 顺平县人大常委会接受辞职 (confirmed)"},
    {"person_id": 2, "org_id": 15, "title": "顺平县委副书记", "start_date": "2017", "end_date": "2018-09", "rank": "县处级副职",
     "note": "2018 年前在顺平县任职，具体到任时间未公开 (plausible)"},
    # 周胜会 (3)
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start_date": "2021-07", "end_date": "present", "rank": "",
     "note": "2021-07 市九届人大一次会议选举; 2025-01 六次会议仍为主任 (confirmed)"},
    # 张宝生 (4)
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start_date": "2021-07", "end_date": "present", "rank": "",
     "note": "2021-07 当选新一届政协主席 (confirmed)"},
    {"person_id": 4, "org_id": 2, "title": "定州市政府副市长", "start_date": "2017-02", "end_date": "2021-05", "rank": "",
     "note": "2017-02-23 八届人大一次会议当选副市长; 2021-05-20 八届人大常委会第36次会议辞去副市长 (confirmed)"},
    # 吕仲华 (5)
    {"person_id": 5, "org_id": 1, "title": "市委副书记（专职）", "start_date": "2021-07", "end_date": "present", "rank": "",
     "note": "2021-07 起历年两会/全会主席台名单在市长之后列第二; 确切分工未单独见报 (plausible)"},
    # 孙振林 (6)
    {"person_id": 6, "org_id": 5, "title": "市委常委、纪委书记、市监委主任", "start_date": "2021-07", "end_date": "present", "rank": "",
     "note": "2021-07-22 四大班子联席会即以常委身份出席; 2024-12-13 作为巡察工作领导小组常务副组长传达精神 (confirmed)"},
    # 张二文 (7)
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "2021-07", "end_date": "present", "rank": "",
     "note": "2021-07-22 起历年名单常委; 具体分工待核 (confirmed 为常委)"},
    # 张仲田 (8)
    {"person_id": 8, "org_id": 6, "title": "市委常委、人武部部长", "start_date": "2022-08", "end_date": "present", "rank": "",
     "note": "2022-08-03 民兵训练基地启用仪式主持; 2024-08-01 人武部第一书记任职大会表态发言 (confirmed)"},
    # 刘力威 (9)
    {"person_id": 9, "org_id": 1, "title": "市委副书记", "start_date": "2023-03", "end_date": "present", "rank": "",
     "note": "百度百科 刘力威 条目'现任定州市委副书记' (plausible)"},
    {"person_id": 9, "org_id": 2, "title": "定州市政府副市长", "start_date": "2017-02", "end_date": "2023-03", "rank": "",
     "note": "2017-02-23 当选; 2021-07 起为两会名单(市委序列); 2022-08 民兵基地介绍人 (confirmed)"},
    {"person_id": 9, "org_id": 2, "title": "定州市号头庄乡党委书记/乡长等基层岗位", "start_date": "2011", "end_date": "2017-02", "rank": "",
     "note": "2011.12-2015.03 号头庄乡乡长; 2015.03-2017.01 号头庄乡党委书记; 2003 省委选调生 (confirmed via 2017-02 选举新闻简历)"},
    # 葛亮 (10)
    {"person_id": 10, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "2024-12", "end_date": "present", "rank": "",
     "note": "2024-12-13 巡察动员会宣读授权任职和任务分工决定 (confirmed); 2021-07 起为市委常委"},
    # 陈凯 (11)
    {"person_id": 11, "org_id": 2, "title": "市委常委、市政府常务副市长", "start_date": "2025-01", "end_date": "present", "rank": "",
     "note": "2025-03-06 市级河长名单列为市委常委、常务副市长 (confirmed); 2024-08 起以常委身份出席会议"},
    # 李辉 (12)
    {"person_id": 12, "org_id": 1, "title": "市委常委、市委办公室主任", "start_date": "2024-07", "end_date": "present", "rank": "",
     "note": "2024-07-23 定州日报署名文章落款'市委常委、办公室主任' (confirmed)"},
    # 张充 (13)
    {"person_id": 13, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "2024-06", "end_date": "present", "rank": "",
     "note": "河北大学新闻传播学院调研报道'市委常委、宣传部长张充'参加 (confirmed)"},
    # 市政府领导班子 (14-18)
    {"person_id": 14, "org_id": 2, "title": "市政府副市长", "start_date": "2024-08", "end_date": "present", "rank": "",
     "note": "2024-08-01 人武部会议出席; 2025-03-06 河长名单 (confirmed)"},
    {"person_id": 15, "org_id": 2, "title": "市政府副市长", "start_date": "2025-01", "end_date": "present", "rank": "",
     "note": "2025-03-06 市级河长名单; 2024-08-26 述法评议会议点评 (confirmed)"},
    {"person_id": 16, "org_id": 2, "title": "市政府副市长", "start_date": "2025-01", "end_date": "present", "rank": "",
     "note": "2025-03-06 市级河长名单 (confirmed)"},
    {"person_id": 17, "org_id": 2, "title": "市政府副市长", "start_date": "2025-01", "end_date": "present", "rank": "",
     "note": "2025-03-06 市级河长名单 (confirmed)"},
    {"person_id": 18, "org_id": 2, "title": "市政府副市长", "start_date": "2025-01", "end_date": "present", "rank": "",
     "note": "2025-03-06 市级河长名单 (confirmed)"},
    # 张涛 (19)
    {"person_id": 19, "org_id": 9, "title": "张家口市委副书记、市长（兼经开区管委会主任）", "start_date": "2025-11", "end_date": "present", "rank": "厅级",
     "note": "2025-11-10 代市长; 2025-11-14 市十五届人大八次会议补选 (confirmed)"},
    {"person_id": 19, "org_id": 9, "title": "张家口市委常委、常务副市长", "start_date": "2024-06", "end_date": "2025-10", "rank": "厅级副职",
     "note": "2024-06 由定州转任 (confirmed)"},
    {"person_id": 19, "org_id": 1, "title": "定州市委书记", "start_date": "2021-01", "end_date": "2024-06", "rank": "副厅级",
     "note": "2021-01 任市委书记(兼任市长至2021-05); 2024-03 机构改革动员仍为书记 (confirmed)"},
    {"person_id": 19, "org_id": 2, "title": "定州市长", "start_date": "2019-01", "end_date": "2021-01", "rank": "副厅级",
     "note": "2019-01-29 市八届人大四次会议当选 (confirmed)"},
    {"person_id": 19, "org_id": 2, "title": "定州市代市长", "start_date": "2018-07", "end_date": "2019-01", "rank": "副厅级",
     "note": "2018-07 省委决定任代市长 (confirmed)"},
    {"person_id": 19, "org_id": 8, "title": "河北省科技厅副厅长、党组成员", "start_date": "2017-09", "end_date": "2018-07", "rank": "厅级副职",
     "note": "其间 2018-03-07 中央党校中青年干部培训班 (confirmed)"},
    {"person_id": 19, "org_id": 8, "title": "河北省科技厅副巡视员", "start_date": "2013-11", "end_date": "2017-09", "rank": "",
     "note": "其间 2015-07-2016-08 挂职中关村管委会副主任 (confirmed)"},
    # 王东群 (20)
    {"person_id": 20, "org_id": 1, "title": "定州市委书记", "start_date": "2016-10", "end_date": "2020-11", "rank": "副厅级",
     "note": "2020-11-05 主动投案; 2021-11 省委追认留党察看一年 (confirmed)"},
    {"person_id": 20, "org_id": 3, "title": "市人大常委会主任（兼）", "start_date": "2017-02", "end_date": "2019-01", "rank": "",
     "note": "兼任市人大常委会主任 (confirmed)"},
    {"person_id": 20, "org_id": 18, "title": "乐亭县委书记", "start_date": "2013-11", "end_date": "2016-10", "rank": "县处级正职",
     "note": "2011.01 乐亭县委副书记、代县长; 2011.02-2013.11 县长 (confirmed)"},
    {"person_id": 20, "org_id": 19, "title": "唐山市直机关及园区任职", "start_date": "1980-08", "end_date": "2011-01", "rank": "",
     "note": "含 滦县教师/县开放办/外经局、驻京办、海港开发区管委会副主任(2000-2005)、曹妃甸工业区工程建设局长(2005-2007)、路南区委常委副区长(2007-2009)、市政府副秘书长(2009-2010) (confirmed)"},
    # 陈业鹏 (21)
    {"person_id": 21, "org_id": 2, "title": "定州市长", "start_date": "2017-02", "end_date": "2018-07", "rank": "副厅级",
     "note": "2017-02-23 市八届人大一次会议当选; 2018-07 职务被调整(与王东群长期矛盾) (confirmed)"},
    {"person_id": 21, "org_id": 2, "title": "定州市代市长", "start_date": "2016-12", "end_date": "2017-02", "rank": "副厅级",
     "note": "2016-12 任市委副书记、市政府党组书记、代市长 (confirmed)"},
    {"person_id": 21, "org_id": 4, "title": "定州市政协主席", "start_date": "2015-02", "end_date": "2016-12", "rank": "",
     "note": "2015.02 定州市政协主席(兼市委常委、常务副市长) (confirmed)"},
    {"person_id": 21, "org_id": 2, "title": "定州市委常委、常务副市长", "start_date": "2013-06", "end_date": "2016-12", "rank": "",
     "note": "2013-06 由保定市政府副秘书长任定州市委常委、常务副市长 (confirmed)"},
    {"person_id": 21, "org_id": 10, "title": "保定市政府副秘书长", "start_date": "2011-03", "end_date": "2013-06", "rank": "",
     "note": "兼市食品安全委员会办公室主任 (confirmed)"},
    {"person_id": 21, "org_id": 19, "title": "涞源县副县长/县委常委", "start_date": "2000-10", "end_date": "2011-03", "rank": "",
     "note": "2000.10 涞源县任职至 2011.03 保定市政府; 期间 2003-2005 省委党校在职研究生班（法学） (confirmed)"},
    # 刘立军 (22)
    {"person_id": 22, "org_id": 4, "title": "市政协副主席、党组副书记", "start_date": "2017", "end_date": "2020-11", "rank": "",
     "note": "2020-11-01 主动投案 (confirmed)"},
    # 李军辉 (23)
    {"person_id": 23, "org_id": 2, "title": "定州市长", "start_date": "2014-01", "end_date": "2016-12", "rank": "",
     "note": "2014-2016 任市长(列表来源); 履历细节未公开 (plausible)"},
    # 赵志栋 (24)
    {"person_id": 24, "org_id": 1, "title": "定州市委书记", "start_date": "2012-05", "end_date": "2016-10", "rank": "",
     "note": "2012-2016 任市委书记(列表来源); 履历细节未公开 (plausible)"},
]

# ────────────────────────────────────────────────────────────────────────────
# Relationships — 关系边 (同一机构/同时期/前后任/冲突)
# ────────────────────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "张才芳(书记)与邓艳学(市长)党政双核搭档",
     "overlap_org": "定州市", "overlap_period": "2024-10-至今"},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "邓艳学 2024-10 接任张才芳留下的市长职务（张任书记）",
     "overlap_org": "定州市人民政府", "overlap_period": "2024-10"},
    {"person_a": 1, "person_b": 19, "type": "predecessor_successor",
     "context": "张才芳 2024-06 接替张涛任市委书记；此前 2021-2024 市长-书记共事",
     "overlap_org": "中共定州市委", "overlap_period": "2021-05-2024-06"},
    {"person_a": 19, "person_b": 20, "type": "superior_subordinate",
     "context": "王东群任书记、张涛任市长期间班子共事(2018-2020)",
     "overlap_org": "定州市", "overlap_period": "2018-07-2020-11"},
    {"person_a": 20, "person_b": 21, "type": "conflict",
     "context": "书记王东群与市长陈业鹏长期不和，2018-07 陈被免职，王向省委作深刻检讨（澎湃 2018-07 报道）",
     "overlap_org": "定州市", "overlap_period": "2017-02-2018-07"},
    {"person_a": 21, "person_b": 19, "type": "predecessor_successor",
     "context": "陈业鹏 2018-07 免职后，张涛任代市长并于 2019-01 当选",
     "overlap_org": "定州市人民政府", "overlap_period": "2018-07"},
    {"person_a": 23, "person_b": 21, "type": "predecessor_successor",
     "context": "陈业鹏 2016-12 接任李军辉的市长职务",
     "overlap_org": "定州市人民政府", "overlap_period": "2016-12"},
    {"person_a": 24, "person_b": 20, "type": "predecessor_successor",
     "context": "王东群 2016-10 接替赵志栋任市委书记",
     "overlap_org": "中共定州市委", "overlap_period": "2016-10"},
    {"person_a": 20, "person_b": 22, "type": "colleague",
     "context": "王东群任书记期间刘立军任市政协副主席；2020-11 两人先后主动投案接受审查（助纪检风潮）",
     "overlap_org": "定州市", "overlap_period": "2017-2020"},
    {"person_a": 19, "person_b": 3, "type": "colleague",
     "context": "张涛任书记期间与人大主任周胜会班子共事",
     "overlap_org": "定州市", "overlap_period": "2021-01-2024-06"},
    {"person_a": 19, "person_b": 4, "type": "colleague",
     "context": "张涛任市长/书记期间与政协主席张宝生共事",
     "overlap_org": "定州市", "overlap_period": "2018-07-2024-06"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "书记张才芳与纪委书记孙振林（市委巡察工作领导小组组长-常务副组长）",
     "overlap_org": "中共定州市委", "overlap_period": "2024-06-至今"},
    {"person_a": 1, "person_b": 3, "type": "colleague",
     "context": "张才芳任市长/书记期间与人大主任周胜会班子共事",
     "overlap_org": "定州市", "overlap_period": "2021-05-至今"},
    {"person_a": 1, "person_b": 4, "type": "colleague",
     "context": "张才芳任市长/书记与政协主席张宝生共事",
     "overlap_org": "定州市", "overlap_period": "2021-05-至今"},
    {"person_a": 1, "person_b": 8, "type": "colleague",
     "context": "书记与人武部部长张仲田（2024-08 市人武部党委第一书记任职大会）",
     "overlap_org": "中共定州市委", "overlap_period": "2024-06-至今"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "市长邓艳学与常务副市长陈凯搭档",
     "overlap_org": "定州市人民政府", "overlap_period": "2024-10-至今"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "张才芳任市长期间陈凯为班子成员（2024-08 起常委）",
     "overlap_org": "定州市人民政府", "overlap_period": "2024-01-至今"},
    {"person_a": 2, "person_b": 10, "type": "colleague",
     "context": "市长与组织部部长葛亮班子共事",
     "overlap_org": "中共定州市委", "overlap_period": "2024-10-至今"},
    {"person_a": 2, "person_b": 4, "type": "colleague",
     "context": "市长邓艳学与政协主席张宝生班子共事",
     "overlap_org": "定州市", "overlap_period": "2024-10-至今"},
    {"person_a": 2, "person_b": 3, "type": "colleague",
     "context": "市长邓艳学与人大主任周胜会班子共事",
     "overlap_org": "定州市", "overlap_period": "2024-10-至今"},
    {"person_a": 3, "person_b": 4, "type": "colleague",
     "context": "人大-政协两班子 2021-07 同届选举产生",
     "overlap_org": "定州市", "overlap_period": "2021-07-至今"},
]





def esc(s) -> str:
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _add_worked_at_edges(gexf_path: Path, positions: list[dict], next_edge_id: int) -> None:
    """Raw-string surgery: append person -> organization 'worked_at' edges to the
    GEXF written by the shared builder (which only emits person<->person edges).
    String insertion keeps the unprefixed serialization intact."""
    text = gexf_path.read_text(encoding="utf-8")
    marker = "</edges>"
    idx = text.rfind(marker)
    if idx < 0:
        raise RuntimeError("</edges> not found in gexf output")
    chunks = []
    eid = next_edge_id
    for pos in positions:
        source = str(pos["person_id"])
        target = str(pos["org_id"] + 100000)
        title = pos.get("title", "")
        period = str(pos.get("start_date", "")) + " ~ " + str(pos.get("end_date") or "")
        attvalues = "".join(
            f'<attvalue for="{i}" value="{esc(v)}"/>'
            for i, v in (
                ("0", "worked_at"),
                ("1", title),
                ("2", period),
                ("3", "person->org membership"),
            )
        )
        chunks.append(
            f'<edge id="{eid}" source="{source}" target="{target}" type="directed">'
            f"<attvalues>{attvalues}</attvalues></edge>"
        )
        eid += 1
    text = text[:idx] + "".join(chunks) + text[idx:]
    gexf_path.write_text(text, encoding="utf-8")
    return eid - next_edge_id

def main() -> None:
    print(f"Building {SLUG} network...")
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
    conn = sqlite3.connect(str(DB_PATH))
    counts = {
        table: conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        for table in ("persons", "organizations", "positions", "relationships")
    }
    conn.close()
    worked = _add_worked_at_edges(GEXF_PATH, positions, next_edge_id=len(relationships))
    print(
        "Done. Wrote "
        f"{DB_PATH.relative_to(Path.cwd())} and {GEXF_PATH.relative_to(Path.cwd())} "
        f"[{counts}] + {worked} worked_at edges"
    )


if __name__ == "__main__":
    main()