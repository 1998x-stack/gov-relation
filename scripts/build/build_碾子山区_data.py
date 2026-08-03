#!/usr/bin/env python3
"""
碾子山区（黑龙江省齐齐哈尔市）领导班子工作关系网络 — 2026-08-03
Build script for Nianzishan District, Qiqihar City, Heilongjiang Province.

Data sources:
- 碾子山区人民政府官网 https://www.nzs.gov.cn/ — 领导之窗页面
- 各领导个人简历页面 (2023-2026)
- 百度百科等

TASK: heilongjiang_碾子山区
"""

import sqlite3
from datetime import datetime
import os

TODAY = "2026-08-03"
AS_OF = TODAY
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(BASE_DIR, "..", "..", ".."))
STAGING = BASE_DIR
DB_PATH = os.path.join(STAGING, "碾子山区_network.db")
GEXF_PATH = os.path.join(STAGING, "碾子山区_network.gexf")

# ── HELPERS ──

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(role):
    if role is None:
        role = ""
    if "区委书记" in role and "纪委" not in role:
        return "220,30,30"
    if "区长" in role and "副" not in role:
        return "40,100,220"
    if "副区长" in role or "党组成员" in role:
        return "40,140,220"
    if "纪委书记" in role:
        return "180,130,50"
    if "人大" in role:
        return "220,160,40"
    if "政协" in role:
        return "200,150,40"
    if "副书记" in role:
        return "180,60,180"
    if "部长" in role or "政法委" in role or "常委" in role:
        return "120,120,120"
    if "公安局" in role:
        return "60,80,180"
    return "160,160,160"


def person_size(role):
    if role is None:
        role = ""
    if "区委书记" in role:
        return "20.0"
    if "区长" in role and "副" not in role:
        return "18.0"
    if "副书记" in role:
        return "16.0"
    if "常委" in role:
        return "14.0"
    if "人大" in role or "政协" in role:
        return "14.0"
    return "12.0"


def org_color(org_type):
    if org_type is None:
        org_type = ""
    if "党委" in org_type:
        return "200,60,60"
    if "政府" in org_type or "公安" in org_type:
        return "60,100,200"
    if "人大" in org_type:
        return "200,150,40"
    if "政协" in org_type:
        return "180,130,40"
    if "纪委" in org_type:
        return "160,120,40"
    if "党委部门" in org_type:
        return "200,80,80"
    return "120,120,120"


# =========================================================================
# DATA
# =========================================================================

PERSONS = [
    # Top leaders
    ["nzsq_ma_tianshuai", "马天帅", "男", "汉族", "1974年5月", "待查",
     "研究生", "中共党员", "待查",
     "区委书记、一级调研员",
     "中共齐齐哈尔市碾子山区委员会",
     "https://www.nzs.gov.cn/nzsq/c103717/202309/c02_376211.shtml"],

    ["nzsq_sun_kun", "孙坤", "女", "满族", "1986年3月", "待查",
     "大学", "中共党员", "待查",
     "区委副书记、区政府区长",
     "齐齐哈尔市碾子山区人民政府",
     "https://www.nzs.gov.cn/nzsq/c103722/202411/c02_513014.shtml"],

    # Deputy secretaries
    ["nzsq_shi_qiwen", "石奇文", "男", "汉族", "1975年3月", "待查",
     "大学", "中共党员", "待查",
     "区委副书记、二级调研员",
     "中共齐齐哈尔市碾子山区委员会",
     "https://www.nzs.gov.cn/nzsq/c103718/202309/c02_307280.shtml"],

    ["nzsq_zheng_heshan", "郑禾山", "男", "满族", "1988年6月", "待查",
     "研究生", "中共党员", "待查",
     "区委副书记（挂职）",
     "中共齐齐哈尔市碾子山区委员会",
     "https://www.nzs.gov.cn/nzsq/c103718/202509/c02_578754.shtml"],

    # Standing committee
    ["nzsq_zhang_lijun", "张利军", "男", "汉族", "1980年10月", "待查",
     "大学", "中共党员", "待查",
     "区委常委、区政府副区长、三级调研员",
     "中共齐齐哈尔市碾子山区委员会",
     "https://www.nzs.gov.cn/nzsq/c103719/202309/c02_307281.shtml"],

    ["nzsq_pan_junwei", "潘军伟", "男", "汉族", "1970年8月", "待查",
     "大学", "中共党员", "待查",
     "区委常委、政法委书记、三级调研员",
     "中共齐齐哈尔市碾子山区委政法委员会",
     "https://www.nzs.gov.cn/nzsq/c103719/202309/c02_307283.shtml"],

    ["nzsq_han_zhicheng", "韩志成", "男", "汉族", "1976年7月", "待查",
     "大学", "中共党员", "待查",
     "区委常委、纪委书记、监委主任、四级高级监察官",
     "中共齐齐哈尔市碾子山区纪律检查委员会",
     "https://www.nzs.gov.cn/nzsq/c103719/202602/c02_610954.shtml"],

    ["nzsq_ren_xingguo", "任兴国", "男", "汉族", "1976年8月", "待查",
     "大学", "中共党员", "待查",
     "区委常委、宣传部部长",
     "中共齐齐哈尔市碾子山区委员会宣传部",
     "https://www.nzs.gov.cn/nzsq/c103719/202309/c02_307284.shtml"],

    ["nzsq_wang_yunfeng", "王云峰", "男", "汉族", "1982年7月", "待查",
     "大学", "中共党员", "待查",
     "区委常委、组织部部长",
     "中共齐齐哈尔市碾子山区委员会组织部",
     "https://www.nzs.gov.cn/nzsq/c103719/202309/c02_307309.shtml"],

    ["nzsq_liu_qingzhi", "刘清志", "男", "汉族", "1980年3月", "待查",
     "大学", "中共党员", "待查",
     "区委委员、常委",
     "中共齐齐哈尔市碾子山区委员会",
     "https://www.nzs.gov.cn/nzsq/c103719/202402/c02_454327.shtml"],

    # Vice-mayors
    ["nzsq_jiang_heng", "姜恒", "男", "汉族", "1981年9月", "待查",
     "研究生", "中共党员", "待查",
     "区政府副区长",
     "齐齐哈尔市碾子山区人民政府",
     "https://www.nzs.gov.cn/nzsq/c103723/202309/c02_307317.shtml"],

    ["nzsq_liu_dianjun", "刘殿军", "男", "汉族", "1971年5月", "待查",
     "大专", "中共党员", "待查",
     "区政府副区长",
     "齐齐哈尔市碾子山区人民政府",
     "https://www.nzs.gov.cn/nzsq/c103723/202309/c02_307318.shtml"],

    ["nzsq_song_li", "宋丽", "女", "汉族", "1972年2月", "待查",
     "大学", "中共党员", "待查",
     "区政府副区长",
     "齐齐哈尔市碾子山区人民政府",
     "https://www.nzs.gov.cn/nzsq/c103723/202309/c02_307319.shtml"],

    ["nzsq_liu_xianmin", "刘宪民", "男", "汉族", "1969年5月", "待查",
     "大学", "中共党员", "待查",
     "区政府党组成员、三级调研员",
     "齐齐哈尔市碾子山区人民政府",
     "https://www.nzs.gov.cn/nzsq/c103723/202309/c02_307320.shtml"],

    ["nzsq_li_dongdong", "李冬冬", "男", "汉族", "1976年11月", "待查",
     "大学", "中共党员", "待查",
     "区政府副区长、公安局局长、四级高级警长",
     "齐齐哈尔市碾子山区人民政府",
     "https://www.nzs.gov.cn/nzsq/c103723/202309/c02_307321.shtml"],

    # NPC
    ["nzsq_liu_guoqing", "刘国庆", "男", "汉族", "1969年10月", "待查",
     "大专", "中共党员", "待查",
     "区人大常委会主任",
     "齐齐哈尔市碾子山区人民代表大会常务委员会",
     "https://www.nzs.gov.cn/nzsq/c103720/202309/c02_307310.shtml"],

    ["nzsq_yin_yanzhen", "殷艳珍", "女", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "区人大常委会副主任",
     "齐齐哈尔市碾子山区人民代表大会常务委员会",
     "https://www.nzs.gov.cn/nzsq/c102350/xzf.shtml"],

    ["nzsq_wang_liguo", "王立国", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "区人大常委会副主任",
     "齐齐哈尔市碾子山区人民代表大会常务委员会",
     "https://www.nzs.gov.cn/nzsq/c102350/xzf.shtml"],

    ["nzsq_ma_baokui", "马宝奎", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "区人大常委会副主任",
     "齐齐哈尔市碾子山区人民代表大会常务委员会",
     "https://www.nzs.gov.cn/nzsq/c102350/xzf.shtml"],

    # CPPCC
    ["nzsq_qi_guangyan", "亓光焱", "女", "汉族", "1970年11月", "待查",
     "大学", "中共党员", "待查",
     "区政协主席",
     "中国人民政治协商会议齐齐哈尔市碾子山区委员会",
     "https://www.nzs.gov.cn/nzsq/c103725/202309/c02_307322.shtml"],

    ["nzsq_huang_jinbao", "黄金宝", "男", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "区政协副主席",
     "中国人民政治协商会议齐齐哈尔市碾子山区委员会",
     "https://www.nzs.gov.cn/nzsq/c102350/xzf.shtml"],

    ["nzsq_yang_xin", "杨欣", "女", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "区政协副主席",
     "中国人民政治协商会议齐齐哈尔市碾子山区委员会",
     "https://www.nzs.gov.cn/nzsq/c102350/xzf.shtml"],
]


ORGANIZATIONS = [
    ["nzsq_party_committee", "中共齐齐哈尔市碾子山区委员会", "党委", "县处级",
     "中共齐齐哈尔市委", "黑龙江省齐齐哈尔市碾子山区"],
    ["nzsq_discipline", "中共齐齐哈尔市碾子山区纪律检查委员会", "纪委", "县处级",
     "中共齐齐哈尔市纪委", "黑龙江省齐齐哈尔市碾子山区"],
    ["nzsq_org_dept", "中共齐齐哈尔市碾子山区委组织部", "党委部门", "正科级",
     "中共齐齐哈尔市碾子山区委员会", "黑龙江省齐齐哈尔市碾子山区"],
    ["nzsq_propaganda_dept", "中共齐齐哈尔市碾子山区委宣传部", "党委部门", "正科级",
     "中共齐齐哈尔市碾子山区委员会", "黑龙江省齐齐哈尔市碾子山区"],
    ["nzsq_politics_law", "中共齐齐哈尔市碾子山区委政法委员会", "党委部门", "正科级",
     "中共齐齐哈尔市碾子山区委员会", "黑龙江省齐齐哈尔市碾子山区"],
    ["nzsq_gov", "齐齐哈尔市碾子山区人民政府", "政府", "县处级",
     "齐齐哈尔市人民政府", "黑龙江省齐齐哈尔市碾子山区"],
    ["nzsq_public_security", "齐齐哈尔市碾子山区公安局", "政府", "正科级",
     "齐齐哈尔市碾子山区人民政府", "黑龙江省齐齐哈尔市碾子山区"],
    ["nzsq_npc", "齐齐哈尔市碾子山区人民代表大会常务委员会", "人大", "县处级",
     "齐齐哈尔市人民代表大会常务委员会", "黑龙江省齐齐哈尔市碾子山区"],
    ["nzsq_cppcc", "中国人民政治协商会议齐齐哈尔市碾子山区委员会", "政协", "县处级",
     "中国人民政治协商会议齐齐哈尔市委员会", "黑龙江省齐齐哈尔市碾子山区"],
    ["qqhr_party_committee", "中共齐齐哈尔市委员会", "党委", "地厅级",
     "中共黑龙江省委", "黑龙江省齐齐哈尔市"],
    ["qqhr_gov", "齐齐哈尔市人民政府", "政府", "地厅级",
     "黑龙江省人民政府", "黑龙江省齐齐哈尔市"],
]


POSITIONS = [
    # 马天帅
    ["nzsq_ma_tianshuai", "nzsq_party_committee",
     "区委书记、一级调研员", "2024.06", "present", "县处级",
     "confirmed from nzs.gov.cn"],
    # 孙坤
    ["nzsq_sun_kun", "nzsq_gov",
     "区长", "2024.11", "present", "县处级",
     "confirmed from nzs.gov.cn"],
    ["nzsq_sun_kun", "nzsq_party_committee",
     "区委副书记", "2024.11", "present", "县处级", ""],
    # 石奇文
    ["nzsq_shi_qiwen", "nzsq_party_committee",
     "区委副书记、二级调研员", "2021.09", "present", "县处级", ""],
    # 郑禾山
    ["nzsq_zheng_heshan", "nzsq_party_committee",
     "区委副书记（挂职）", "2025.03", "present", "县处级", ""],
    # 张利军
    ["nzsq_zhang_lijun", "nzsq_party_committee",
     "区委常委", "2021.07", "present", "副县处级", ""],
    ["nzsq_zhang_lijun", "nzsq_gov",
     "区政府副区长、三级调研员", "2021.07", "present", "副县处级", ""],
    # 潘军伟
    ["nzsq_pan_junwei", "nzsq_party_committee",
     "区委常委", "2021.09", "present", "副县处级", ""],
    ["nzsq_pan_junwei", "nzsq_politics_law",
     "区委政法委书记、三级调研员", "2021.09", "present", "副县处级", ""],
    # 韩志成
    ["nzsq_han_zhicheng", "nzsq_party_committee",
     "区委常委", "2025.12", "present", "副县处级", ""],
    ["nzsq_han_zhicheng", "nzsq_discipline",
     "区纪委书记、监委主任、四级高级监察官", "2025.12", "present", "副县处级", ""],
    # 任兴国
    ["nzsq_ren_xingguo", "nzsq_party_committee",
     "区委常委", "2021.09", "present", "副县处级", ""],
    ["nzsq_ren_xingguo", "nzsq_propaganda_dept",
     "宣传部部长", "2021.09", "present", "副县处级", ""],
    # 王云峰
    ["nzsq_wang_yunfeng", "nzsq_party_committee",
     "区委常委", "2023.06", "present", "副县处级", ""],
    ["nzsq_wang_yunfeng", "nzsq_org_dept",
     "组织部部长", "2023.06", "present", "副县处级", ""],
    # 刘清志
    ["nzsq_liu_qingzhi", "nzsq_party_committee",
     "区委委员、常委", "2023.12", "present", "副县处级", ""],
    # 姜恒
    ["nzsq_jiang_heng", "nzsq_gov",
     "区政府副区长", "2021.09", "present", "副县处级", ""],
    # 刘殿军
    ["nzsq_liu_dianjun", "nzsq_gov",
     "区政府副区长", "2021.09", "present", "副县处级", ""],
    # 宋丽
    ["nzsq_song_li", "nzsq_gov",
     "区政府副区长", "2021.09", "present", "副县处级", ""],
    # 刘宪民
    ["nzsq_liu_xianmin", "nzsq_gov",
     "区政府党组成员、三级调研员", "2021.09", "present", "副县处级", ""],
    # 李冬冬
    ["nzsq_li_dongdong", "nzsq_gov",
     "区政府副区长", "2022.05", "present", "副县处级", ""],
    ["nzsq_li_dongdong", "nzsq_public_security",
     "区公安局局长、四级高级警长", "2022.05", "present", "正科级", ""],
    # 刘国庆
    ["nzsq_liu_guoqing", "nzsq_npc",
     "区人大常委会主任", "2021.11", "present", "县处级", ""],
    # NPC deputies
    ["nzsq_yin_yanzhen", "nzsq_npc",
     "区人大常委会副主任", "待查", "present", "副县处级", ""],
    ["nzsq_wang_liguo", "nzsq_npc",
     "区人大常委会副主任", "待查", "present", "副县处级", ""],
    ["nzsq_ma_baokui", "nzsq_npc",
     "区人大常委会副主任", "待查", "present", "副县处级", ""],
    # 亓光焱
    ["nzsq_qi_guangyan", "nzsq_cppcc",
     "区政协主席", "2021.11", "present", "县处级", ""],
    # CPPCC deputies
    ["nzsq_huang_jinbao", "nzsq_cppcc",
     "区政协副主席", "待查", "present", "副县处级", ""],
    ["nzsq_yang_xin", "nzsq_cppcc",
     "区政协副主席", "待查", "present", "副县处级", ""],
]


RELATIONSHIPS = [
    # 党政搭档
    ["nzsq_ma_tianshuai", "nzsq_sun_kun",
     "党政搭档", "区委书记与区长党政正职搭档",
     "碾子山区党政领导班子", "2024.11-至今"],

    # 书记与副书记
    ["nzsq_ma_tianshuai", "nzsq_shi_qiwen",
     "上下级", "区委书记与专职副书记",
     "中共碾子山区委", "2021.09-至今"],
    ["nzsq_ma_tianshuai", "nzsq_zheng_heshan",
     "上下级", "区委书记与挂职副书记",
     "中共碾子山区委", "2025.03-至今"],

    # 区长与副区长
    ["nzsq_sun_kun", "nzsq_zhang_lijun",
     "上下级", "区长与常务副区长",
     "碾子山区政府", "2024.11-至今"],
    ["nzsq_sun_kun", "nzsq_jiang_heng",
     "上下级", "区长与副区长", "碾子山区政府", "2024.11-至今"],
    ["nzsq_sun_kun", "nzsq_liu_dianjun",
     "上下级", "区长与副区长", "碾子山区政府", "2024.11-至今"],
    ["nzsq_sun_kun", "nzsq_song_li",
     "上下级", "区长与副区长", "碾子山区政府", "2024.11-至今"],
    ["nzsq_sun_kun", "nzsq_li_dongdong",
     "上下级", "区长与副区长兼公安局长", "碾子山区政府", "2024.11-至今"],

    # 常委同僚
    ["nzsq_shi_qiwen", "nzsq_pan_junwei",
     "同僚", "同为区委常委", "中共碾子山区委", "2021.09-至今"],
    ["nzsq_shi_qiwen", "nzsq_ren_xingguo",
     "同僚", "同为区委常委", "中共碾子山区委", "2021.09-至今"],
    ["nzsq_shi_qiwen", "nzsq_wang_yunfeng",
     "同僚", "同为区委常委", "中共碾子山区委", "2023.06-至今"],
    ["nzsq_pan_junwei", "nzsq_ren_xingguo",
     "同僚", "同为区委常委", "中共碾子山区委", "2021.09-至今"],
    ["nzsq_pan_junwei", "nzsq_wang_yunfeng",
     "同僚", "同为区委常委", "中共碾子山区委", "2023.06-至今"],
    ["nzsq_ren_xingguo", "nzsq_wang_yunfeng",
     "同僚", "同为区委常委", "中共碾子山区委", "2023.06-至今"],
    ["nzsq_han_zhicheng", "nzsq_pan_junwei",
     "同僚", "同为区委常委", "中共碾子山区委", "2025.12-至今"],
    ["nzsq_han_zhicheng", "nzsq_ren_xingguo",
     "同僚", "同为区委常委", "中共碾子山区委", "2025.12-至今"],
    ["nzsq_liu_qingzhi", "nzsq_shi_qiwen",
     "同僚", "同为区委常委", "中共碾子山区委", "2023.12-至今"],
    ["nzsq_liu_qingzhi", "nzsq_wang_yunfeng",
     "同僚", "同为区委常委", "中共碾子山区委", "2023.12-至今"],

    # 副区长同僚
    ["nzsq_zhang_lijun", "nzsq_jiang_heng",
     "同僚", "同为区政府领导", "碾子山区政府", "2021.09-至今"],
    ["nzsq_zhang_lijun", "nzsq_liu_dianjun",
     "同僚", "同为区政府领导", "碾子山区政府", "2021.09-至今"],
    ["nzsq_zhang_lijun", "nzsq_song_li",
     "同僚", "同为区政府领导", "碾子山区政府", "2021.09-至今"],
    ["nzsq_jiang_heng", "nzsq_liu_dianjun",
     "同僚", "同为副区长", "碾子山区政府", "2021.09-至今"],
    ["nzsq_jiang_heng", "nzsq_song_li",
     "同僚", "同为副区长", "碾子山区政府", "2021.09-至今"],
    ["nzsq_liu_dianjun", "nzsq_song_li",
     "同僚", "同为副区长", "碾子山区政府", "2021.09-至今"],

    # 人大政协
    ["nzsq_liu_guoqing", "nzsq_qi_guangyan",
     "党政搭档", "人大主任与政协主席", "碾子山区", "2021.11-至今"],
]


# ── BUILD DATABASE ──

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in PERSONS:
        c.execute("""
            INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    for o in ORGANIZATIONS:
        c.execute("""
            INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)

    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, pos)

    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ── BUILD GEXF ──

def generate_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3"')
    lines.append('      xmlns:viz="http://gexf.net/1.3/viz"')
    lines.append('      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
    lines.append('      xsi:schemaLocation="http://gexf.net/1.3 http://gexf.net/1.3/gexf.xsd"')
    lines.append('      version="1.3">')
    lines.append('  <meta>')
    lines.append('    <creator>China-Gov-Network Investigation</creator>')
    lines.append('    <description>黑龙江省齐齐哈尔市碾子山区领导班子工作关系网络</description>')
    lines.append(f'    <date>{TODAY}</date>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="type" title="Node Type" type="string"/>')
    lines.append('      <attribute id="role" title="Role" type="string"/>')
    lines.append('      <attribute id="org_type" title="Org Type" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="type" title="Edge Type" type="string"/>')
    lines.append('      <attribute id="start" title="Start Date" type="string"/>')
    lines.append('      <attribute id="end" title="End Date" type="string"/>')
    lines.append('      <attribute id="strength" title="Strength" type="string"/>')
    lines.append('      <attribute id="context" title="Context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        label = p[1]
        role = p[9] or ""
        birth = p[4] or ""
        c = person_color(role)
        sz = person_size(role)
        rgb = c.split(",")
        lines.append(f'      <node id="{pid}" label="{esc(label)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="person"/>')
        lines.append(f'          <attvalue for="role" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="birth" value="{esc(birth)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in ORGANIZATIONS:
        oid = o[0]
        label = o[1]
        c = org_color(o[2])
        rgb = c.split(",")
        lines.append(f'      <node id="{oid}" label="{esc(label)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="org"/>')
        lines.append(f'          <attvalue for="org_type" value="{esc(o[2])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}" a="1.0"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="square"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in POSITIONS:
        eid += 1
        pid, oid, title, start, end_, rank, note = pos
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" type="directed" label="{esc(title)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="start" value="{esc(start or "")}"/>')
        lines.append(f'          <attvalue for="end" value="{esc(end_ or "")}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="80" g="80" b="80" a="0.5"/>')
        lines.append('        <viz:thickness value="1.0"/>')
        lines.append('      </edge>')

    for r in RELATIONSHIPS:
        eid += 1
        a, b, _typ, context, _org, period = r
        lines.append(f'          <edge id="e{eid}" source="{a}" target="{b}" type="undirected" label="{esc(context)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="relationship"/>')
        lines.append('          <attvalue for="strength" value="strong"/>')
        lines.append(f'          <attvalue for="context" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="start" value="{esc(period.split("-")[0].strip() if "-" in period else "")}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="184" g="149" b="62" a="0.8"/>')
        lines.append('        <viz:thickness value="2.5"/>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


# ── STATS ──

def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  黑龙江省齐齐哈尔市碾子山区领导班子工作关系网络")
    print("  等级: 市辖区（县处级）")
    print(f"  生成日期: {TODAY}")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\nSummary:")
    print_stats()
    print("\nDone.")