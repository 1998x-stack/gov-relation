#!/usr/bin/env python3
"""枣强县领导班子工作关系网络 - 数据构建脚本

Generated: 2026-07-24
Task: hebei_枣强县
Sources:
  - https://www.baike.com/wiki/刘新营 (快懂百科/抖音百科)
  - http://www.zaoqiang.gov.cn (枣强县人民政府官网)
  - 人民网 http://he.people.com.cn/n2/2021/0519/c192235-34734654.html
  - 海峡网 https://www.toutiao.com/article/7330533645154910760/
"""

from gov_relation.runner import run_build

# Person IDs: 1=刘新营, 2=赵飞, 3=葛茂松, 4=李景龙, 5=刘泽军, 6=武骏, 7=郑丹
# Org IDs: 1-12 (will be shifted by 100000 in GEXF builder)

persons = [
    {
        "id": 1, "name": "刘新营", "gender": "男", "ethnicity": "汉族",
        "birth": "1966年12月", "birthplace": "河北省阜城县",
        "education": "河北师范大学政治教育专业（大学）/ 河北省委党校在职研究生",
        "party_join": "1990年10月", "work_start": "1988年8月",
        "current_post": "衡水市人大常委会副主任、枣强县委书记",
        "current_org": "中共枣强县委",
        "source": "https://www.baike.com/wiki/刘新营",
    },
    {
        "id": 2, "name": "赵飞", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣强县人民政府县长", "current_org": "枣强县人民政府",
        "source": "枣强县人民政府官网",
    },
    {
        "id": 3, "name": "葛茂松", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣强县委常委、常务副县长", "current_org": "枣强县人民政府",
        "source": "枣强县人民政府官网",
    },
    {
        "id": 4, "name": "李景龙", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣强县委常委、纪委书记、监委主任",
        "current_org": "中共枣强县纪律检查委员会",
        "source": "枣强县人民政府官网",
    },
    {
        "id": 5, "name": "刘泽军", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣强县委常委、组织部长", "current_org": "中共枣强县委组织部",
        "source": "枣强县人民政府官网",
    },
    {
        "id": 6, "name": "武骏", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣强县委常委、政法委书记",
        "current_org": "中共枣强县委政法委",
        "source": "枣强县人民政府官网",
    },
    {
        "id": 7, "name": "郑丹", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣强县委常委、宣传部长", "current_org": "中共枣强县委宣传部",
        "source": "枣强县人民政府官网",
    },
]

organizations = [
    {"id": 1, "name": "中共枣强县委", "type": "党委", "level": "县处级", "location": "河北省衡水市枣强县"},
    {"id": 2, "name": "枣强县人民政府", "type": "政府", "level": "县处级", "location": "河北省衡水市枣强县"},
    {"id": 3, "name": "中共枣强县纪律检查委员会", "type": "党委", "level": "县处级", "location": "河北省衡水市枣强县"},
    {"id": 4, "name": "中共枣强县委组织部", "type": "党委", "level": "县处级", "location": "河北省衡水市枣强县"},
    {"id": 5, "name": "中共枣强县委政法委", "type": "党委", "level": "县处级", "location": "河北省衡水市枣强县"},
    {"id": 6, "name": "中共枣强县委宣传部", "type": "党委", "level": "县处级", "location": "河北省衡水市枣强县"},
    {"id": 7, "name": "衡水市人大常委会", "type": "人大", "level": "地厅级", "location": "河北省衡水市"},
    {"id": 8, "name": "衡水地委（市委）办公室", "type": "党委", "level": "地厅级", "location": "河北省衡水市"},
    {"id": 9, "name": "故城县委", "type": "党委", "level": "县处级", "location": "河北省衡水市故城县"},
    {"id": 10, "name": "衡水地区粮食局", "type": "政府", "level": "地厅级", "location": "河北省衡水市"},
    {"id": 11, "name": "衡水地区粮食学校", "type": "事业单位", "level": "", "location": "河北省衡水市"},
    {"id": 12, "name": "河北师范大学", "type": "事业单位", "level": "", "location": "河北省石家庄市"},
]

positions = [
    # 刘新营 (id=1)
    {"person_id": 1, "org_id": 7, "title": "衡水市人大常委会副主任", "start_date": "2024-01", "end_date": "present", "rank": "副厅级", "note": "2024年1月30日当选"},
    {"person_id": 1, "org_id": 1, "title": "枣强县委书记", "start_date": "2021-05", "end_date": "present", "rank": "县处级正职", "note": "2021年5月18日任县委书记"},
    {"person_id": 1, "org_id": 2, "title": "枣强县委副书记、县长", "start_date": "2017-02", "end_date": "2021-05", "rank": "县处级正职", "note": "2017年2月正式任县长"},
    {"person_id": 1, "org_id": 2, "title": "枣强县委副书记、代县长", "start_date": "2016-12", "end_date": "2017-02", "rank": "县处级正职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "枣强县委副书记", "start_date": "2015-06", "end_date": "2016-12", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "故城县委常委、组织部长", "start_date": "2011-08", "end_date": "2015-06", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "衡水市委副秘书长", "start_date": "2008-10", "end_date": "2011-08", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "衡水市委办公室副主任", "start_date": "2007-06", "end_date": "2008-10", "rank": "县处级副职", "note": "2008年10月正式任职"},
    {"person_id": 1, "org_id": 8, "title": "衡水市委办公室秘书一科科长", "start_date": "2002-09", "end_date": "2007-06", "rank": "乡科级正职", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "衡水市委办公室综合二科主任科员", "start_date": "2000-12", "end_date": "2002-09", "rank": "乡科级正职", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "衡水市委办公室综合二科副科长", "start_date": "1997-06", "end_date": "2000-12", "rank": "乡科级副职", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "衡水市委（地委）办公室综合科科员", "start_date": "1995-09", "end_date": "1997-06", "rank": "科员", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "衡水地区粮食局农村购销科科员", "start_date": "1992-02", "end_date": "1995-09", "rank": "科员", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "衡水地区粮食学校教师", "start_date": "1988-08", "end_date": "1992-02", "rank": "教师", "note": ""},
    # 赵飞 (id=2)
    {"person_id": 2, "org_id": 2, "title": "枣强县人民政府县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "现任枣强县县长"},
    # 葛茂松 (id=3)
    {"person_id": 3, "org_id": 2, "title": "枣强县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 李景龙 (id=4)
    {"person_id": 4, "org_id": 3, "title": "枣强县委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 刘泽军 (id=5)
    {"person_id": 5, "org_id": 4, "title": "枣强县委常委、组织部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 武骏 (id=6)
    {"person_id": 6, "org_id": 5, "title": "枣强县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 郑丹 (id=7)
    {"person_id": 7, "org_id": 6, "title": "枣强县委常委、宣传部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭班子", "overlap_org": "枣强县", "overlap_period": "2021-至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与常务副县长搭班子", "overlap_org": "枣强县", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与常务副县长搭班子", "overlap_org": "枣强县人民政府", "overlap_period": ""},
]

if __name__ == "__main__":
    import sys
    from pathlib import Path
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    db_path = out_dir / "枣强县_network.db"
    gexf_path = out_dir / "枣强县_network.gexf"
    run_build(slug="枣强县", persons=persons, organizations=organizations,
              positions=positions, relationships=relationships,
              db_path=db_path, gexf_path=gexf_path, overwrite=True)
    print(f"Output: {out_dir}")
