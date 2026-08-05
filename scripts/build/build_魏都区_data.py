#!/usr/bin/env python3
"""Build 许昌市魏都区 leadership network data (henan_魏都区, 2026-08-05)."""
from __future__ import annotations
import json, os, sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
import sqlite3  # noqa

SLUG = "魏都区"
DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR
AS_OF = datetime.now().strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y%m%d")
OFFICIAL_LDZC = "http://www.weidu.gov.cn/zwgk/003004/secondPageLeaders.html"

persons = [{"id": 1, "name": "何长成", "gender": "男", "ethnicity": "汉族(推断)", "birth": "", "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "魏都区委书记", "current_org": "中共许昌市魏都区委员会", "src": "官方区十六次党代会作报告/主持区委常委会"}, {"id": 2, "name": "李淼", "gender": "男", "ethnicity": "汉族", "birth": "1985-07", "birthplace": "", "native_place": "", "education": "研究生,管理学博士", "party_join": "中共党员", "work_start": "", "current_post": "魏都区委副书记、区长", "current_org": "魏都区人民政府", "src": "http://www.weidu.gov.cn/zwgk/003004/secondPageLeaders.html (区委副书记,区政府区长、党组书记)"}, {"id": 3, "name": "屈红雨", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区委副书记(推测)", "current_org": "中共魏都区委员会", "source_id": "S02"}, {"id": 4, "name": "申健民", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区人大常委会主任", "current_org": "魏都区人大常委会", "src": "官方八一走访慰问"}, {"id": 5, "name": "杜晓辉", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区政协主席", "current_org": "政协魏都区委员会", "src": "官方八一走访慰问"}, {"id": 6, "name": "孙卫东", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区委领导(待确认)", "current_org": "中共魏都区委员会", "src": "区十六次党代会执行主席"}, {"id": 7, "name": "金俊山", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区委领导(待确认)", "current_org": "中共魏都区委员会", "src": "区十六次党代会执行主席"}, {"id": 8, "name": "楚知真", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区委领导(待确认)", "current_org": "中共魏都区委员会", "src": "区十六次党代会执行主席"}, {"id": 9, "name": "王应选", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区委领导(待确认)", "current_org": "中共魏都区委员会", "src": "区十六次党代会执行主席"}, {"id": 10, "name": "张鹏帅", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区委领导(待确认)", "current_org": "中共魏都区委员会", "src": "区十六次党代会执行主席"}, {"id": 11, "name": "汪甲奇", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区委领导(待确认)", "current_org": "中共魏都区委员会", "src": "区十六次党代会执行主席+八一活动"}, {"id": 12, "name": "宋佳", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区委领导(待确认)", "current_org": "中共魏都区委员会", "src": "区十六次党代会执行主席+八一活动"}, {"id": 13, "name": "尹飞", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区领导(待确认)", "current_org": "魏都区", "src": "低效用地盘活例会:何长成、李淼、万英豪、张二峰、尹飞"}, {"id": 14, "name": "龚文兵", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区领导(待确认)", "current_org": "魏都区", "src": "官方八一活动区领导"}, {"id": 15, "name": "张二峰", "gender": "男", "ethnicity": "汉族", "birth": "1975-03", "birthplace": "", "native_place": "", "education": "大学", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、常务副区长", "current_org": "魏都区人民政府", "src": "http://www.weidu.gov.cn/zwgk/003004/secondPageLeaders.html"}, {"id": 16, "name": "万英豪", "gender": "男", "ethnicity": "汉族", "birth": "1986-12", "birthplace": "", "native_place": "", "education": "研究生,经济学硕士", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、副区长", "current_org": "魏都区人民政府", "src": "http://www.weidu.gov.cn/zwgk/003004/secondPageLeaders.html"}, {"id": 17, "name": "王伟芳", "gender": "女", "ethnicity": "汉族", "birth": "1974-10", "birthplace": "", "native_place": "", "education": "大学,法学学士", "party_join": "民建会员", "work_start": "", "current_post": "副区长", "current_org": "魏都区人民政府", "src": "http://www.weidu.gov.cn/zwgk/003004/secondPageLeaders.html"}, {"id": 18, "name": "张小龙", "gender": "男", "ethnicity": "汉族", "birth": "1985-06", "birthplace": "", "native_place": "", "education": "本科,工学学士", "party_join": "中共党员", "work_start": "", "current_post": "副区长", "current_org": "魏都区人民政府", "src": "http://www.weidu.gov.cn/zwgk/003004/secondPageLeaders.html"}, {"id": 19, "name": "陈林", "gender": "男", "ethnicity": "汉族", "birth": "1980-08", "birthplace": "", "native_place": "", "education": "研究生", "party_join": "中共党员", "work_start": "", "current_post": "副区长", "current_org": "魏都区人民政府", "src": "http://www.weidu.gov.cn/zwgk/003004/secondPageLeaders.html"}, {"id": 20, "name": "俎照虎", "gender": "男", "ethnicity": "汉族", "birth": "1975-11", "birthplace": "", "native_place": "", "education": "大专", "party_join": "中共党员", "work_start": "", "current_post": "副区长", "current_org": "魏都区人民政府", "src": "http://www.weidu.gov.cn/zwgk/003004/secondPageLeaders.html"}, {"id": 21, "name": "常畅", "gender": "男", "ethnicity": "汉族", "birth": "1983-03", "birthplace": "", "native_place": "", "education": "本科", "party_join": "中共党员", "work_start": "", "current_post": "副区长", "current_org": "魏都区人民政府", "src": "http://www.weidu.gov.cn/zwgk/003004/secondPageLeaders.html"}, {"id": 22, "name": "蔡晨凛", "gender": "男", "ethnicity": "汉族", "birth": "1977-05", "birthplace": "", "native_place": "", "education": "大学,工程硕士", "party_join": "中共党员", "work_start": "", "current_post": "公安局长(兼副区长)", "current_org": "许昌市公安局魏都分局", "src": "http://www.weidu.gov.cn/zwgk/003004/secondPageLeaders.html"}]

organizations = [{"id": 1, "name": "中共许昌市魏都区委员会", "type": "党委", "level": "市辖区", "parent": "中共许昌市委员会", "location": "河南省许昌市魏都区"}, {"id": 2, "name": "魏都区人民政府", "type": "政府", "level": "市辖区", "parent": "许昌市人民政府", "location": "河南省许昌市魏都区"}, {"id": 3, "name": "魏都区人大常委会", "type": "人大", "level": "市辖区", "parent": "许昌市人大常委会", "location": "河南省许昌市魏都区"}, {"id": 4, "name": "政协魏都区委员会", "type": "政协", "level": "市辖区", "parent": "政协许昌市委员会", "location": "河南省许昌市魏都区"}, {"id": 5, "name": "中共许昌市魏都区纪律检查委员会", "type": "纪委", "level": "市辖区", "parent": "中共许昌市纪律检查委员会", "location": "河南省许昌市魏都区"}, {"id": 6, "name": "许昌市公安局魏都分局", "type": "政府", "level": "区直部门", "parent": "许昌市公安局", "location": "河南省许昌市魏都区"}]

positions = [{"person_id": 1, "org_id": 1, "title": "魏都区委书记", "start": "", "end": "至今", "rank": "县处级正职", "note": "主持区十六次党代会/区委常委会"}, {"person_id": 2, "org_id": 1, "title": "魏都区委副书记", "start": "", "end": "至今", "rank": "县处级副职", "note": ""}, {"person_id": 2, "org_id": 2, "title": "魏都区区长", "start": "", "end": "至今", "rank": "区级正职", "note": "区政府党组书记;主持全面工作,负责审计"}, {"person_id": 3, "org_id": 1, "title": "魏都区委副书记", "start": "", "end": "至今", "rank": "县处级副职", "note": "具体分工待确认"}, {"person_id": 4, "org_id": 3, "title": "区人大常委会主任", "start": "", "end": "至今", "rank": "区级正职", "note": ""}, {"person_id": 5, "org_id": 4, "title": "区政协主席", "start": "", "end": "至今", "rank": "区级正职", "note": ""}, {"person_id": 6, "org_id": 1, "title": "区委领导", "start": "", "end": "至今", "rank": "县处级副职", "note": "待确认"}, {"person_id": 7, "org_id": 1, "title": "区委领导", "start": "", "end": "至今", "rank": "县处级副职", "note": "待确认"}, {"person_id": 8, "org_id": 1, "title": "区委领导", "start": "", "end": "至今", "rank": "县处级副职", "note": "待确认"}, {"person_id": 9, "org_id": 1, "title": "区委领导", "start": "", "end": "至今", "rank": "县处级副职", "note": "待确认"}, {"person_id": 10, "org_id": 1, "title": "区委领导", "start": "", "end": "至今", "rank": "县处级副职", "note": "待确认"}, {"person_id": 11, "org_id": 1, "title": "区委领导", "start": "", "end": "至今", "rank": "县处级副职", "note": "待确认"}, {"person_id": 12, "org_id": 1, "title": "区委领导", "start": "", "end": "至今", "rank": "县处级副职", "note": "待确认"}, {"person_id": 13, "org_id": 1, "title": "区领导", "start": "", "end": "至今", "rank": "县处级副职", "note": "待确认"}, {"person_id": 14, "org_id": 1, "title": "区领导", "start": "", "end": "至今", "rank": "县处级副职", "note": "待确认"}, {"person_id": 15, "org_id": 1, "title": "魏都区委常委", "start": "", "end": "至今", "rank": "县处级副职", "note": ""}, {"person_id": 15, "org_id": 2, "title": "常务副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": "区政府党组副书记"}, {"person_id": 16, "org_id": 1, "title": "魏都区委常委", "start": "", "end": "至今", "rank": "县处级副职", "note": ""}, {"person_id": 16, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": ""}, {"person_id": 17, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": ""}, {"person_id": 18, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": ""}, {"person_id": 19, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": ""}, {"person_id": 20, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": ""}, {"person_id": 21, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": ""}, {"person_id": 22, "org_id": 6, "title": "许昌市公安局魏都分局局长", "start": "", "end": "至今", "rank": "乡科级正职", "note": "魏都分局党委书记"}, {"person_id": 22, "org_id": 2, "title": "区人民政府党组成员", "start": "", "end": "至今", "rank": "县处级副职", "note": ""}]

relationships = [{"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长党政搭档,共同出席专项会议、八一慰问", "overlap_org": "魏都区", "overlap_period": "2026年"}, {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与区委副书记,区十六次党代会", "overlap_org": "中共魏都区委", "overlap_period": "2026年"}, {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与人大常委会主任", "overlap_org": "魏都区", "overlap_period": "2026年"}, {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委书记与区政协主席", "overlap_org": "魏都区", "overlap_period": "2026年"}, {"person_a": 1, "person_b": 15, "type": "overlap", "context": "区委书记与常务副区长,低效用地例会", "overlap_org": "魏都区", "overlap_period": "2026年"}, {"person_a": 1, "person_b": 16, "type": "overlap", "context": "区委书记与区委常委/副区长", "overlap_org": "中共魏都区/区政府", "overlap_period": "2026年"}, {"person_a": 1, "person_b": 20, "type": "overlap", "context": "区委书记与副区长,防汛调研", "overlap_org": "魏都区", "overlap_period": "2026年"}, {"person_a": 1, "person_b": 18, "type": "overlap", "context": "区委书记与副区长,曹魏专班", "overlap_org": "魏都区", "overlap_period": "2026年"}, {"person_a": 1, "person_b": 11, "type": "overlap", "context": "区委书记与区委领导,十六次党代会+八一", "overlap_org": "中共魏都区委", "overlap_period": "2026年"}, {"person_a": 1, "person_b": 12, "type": "overlap", "context": "区委书记与区委领导宋佳", "overlap_org": "中共魏都区委", "overlap_period": "2026年"}, {"person_a": 2, "person_b": 15, "type": "overlap", "context": "区长与常务副区长", "overlap_org": "魏都区政府", "overlap_period": "2026年"}, {"person_a": 2, "person_b": 16, "type": "overlap", "context": "区长与区委常委/副区长", "overlap_org": "魏都区政府", "overlap_period": "2026年"}, {"person_a": 2, "person_b": 18, "type": "overlap", "context": "区长与副区长,曹魏专班", "overlap_org": "魏都区", "overlap_period": "2026年"}, {"person_a": 2, "person_b": 14, "type": "overlap", "context": "区长与区领导,八一活动", "overlap_org": "魏都区", "overlap_period": "2026年"}, {"person_a": 15, "person_b": 16, "type": "overlap", "context": "区政府党组班子", "overlap_org": "魏都区政府", "overlap_period": "2026年"}]

SOURCE_REGISTER = [{"id": "S01", "title": "魏都区政府领导页面", "url": "http://www.weidu.gov.cn/zwgk/003004/secondPageLeaders.html", "publisher": "魏都区人民政府", "published_at": "2026-08-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "李区、张二峰、万英豪、王伟芳、张小龙、陈林、俎照虎、常畅、蔡晨凛及分工简历"}, {"id": "S02", "title": "区十六届党代会开幕", "url": "http://www.weidu.gov.cn/zwxx/002001/20260624/cf68059b-593a-471b-9e52-ee11009dd9fd.html", "publisher": "魏都区人民政府", "published_at": "2026-06-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "何长成(书记)作报告;屈红云主持;执行主席名单"}, {"id": "S03", "title": "区委常委会会议", "url": "http://www.weidu.gov.cn/zwxx/002001/20260731/d35c58a4-95a3-427f-a900-92c8522efa1b.html", "publisher": "魏都区人民政府", "published_at": "2026-07-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "何长成主持"}, {"id": "S04", "title": "区领导八一走访慰问", "url": "http://www.weidu.gov.cn/zwxx/002001/20260803/6be20448-8c67-42e9-a9b9-b4b2f43b3f5d.html", "publisher": "魏都区人民政府", "published_at": "2026-07-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "何长成、李淼、申健民、杜晓辉走访;汪甲奇、宋佳、龚文兵、王伟芳出席"}, {"id": "S05", "title": "低效工业用地盘活工作例会", "url": "http://www.weidu.gov.cn/zwxx/002001/20260731/2f0d9b0c-6aac-4e23-a9a6-a77fc0d6237b.html", "publisher": "魏都区人民政府", "published_at": "2026-07-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "何长成、李淼、万英豪、张二峰、尹飞参加会议"}, {"id": "S06", "title": "曹魏·187专班周例会", "url": "http://www.weidu.gov.cn/zwxx/002001/20260731/34d3ee6b-7566-4e01-b3cd-4a3ef6ca8b28.html", "publisher": "魏都区人民政府", "published_at": "2026-07-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "何长成、李淼、张小龙参加会议"}, {"id": "S07", "title": "区领导调研积水点改造及防汛备汛", "url": "http://www.weidu.gov.cn/zwxx/002001/20260707/ba1f783c-a3bb-4ddb-ba7b-2a9ebcb4195f.html", "publisher": "魏都区人民政府", "published_at": "2026-07-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区委书记何长成带队,区领导俎照虎参加"}, {"id": "S08", "title": "宁伟伟履历(襄城县)", "url": "scripts/build/build_襄城县_data.py", "publisher": "本仓库研究数据", "published_at": "", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "宁伟伟 2016.06-2019.03 任魏都区委常委、办公室主任,后任襄城县委书记"}]

def make_person_json(p, timeline, rel_list, is_key):
    cp = p.get("current_post","")
    has_bio = bool(p.get("birth") or p.get("birthplace"))
    has_conf = bool(timeline and any(t.get("confidence")=="confirmed" for t in timeline))
    zheng = (("书记" in cp and "副" not in cp and "纪委" not in cp)
             or ("区长" in cp and "副" not in cp and "人大" not in cp)
             or "人大常委会主任" in cp or "政协主席" in cp)
    return {
        "schema_version":"1.0","generated_at":AS_OF,
        "investigation_scope":{"province":"河南省","city":"许昌市","region":"魏都区","job":cp,"task_id":"henan_魏都区","time_focus":"2026年8月"},
        "identity":{"person_id":f"weiduqu_{p['name']}","name":p["name"],"aliases":[],
            "gender":p.get("gender",""),"ethnicity":p.get("ethnicity",""),
            "birth":p.get("birth",""),"birthplace":p.get("birthplace",""),"native_place":p.get("native_place",""),
            "education":([{"period":"","institution":"","major":"","degree":p.get("education",""),"study_type":"unknown","source_ids":[]}] if p.get("education") else []),
            "party_join":p.get("party_join","").replace("中共党员","").replace("（","").replace("）",""),
            "work_start":p.get("work_start",""),
            "dedupe_keys":{"name_birth":f"{p['name']}_{p.get('birth','')}","name_birthplace":f"{p['name']}_{p.get('birthplace','')}","official_profile_url":p.get("source","")}},"current_status":{"current_post":cp,"current_org":p.get("current_org",""),"administrative_rank":("区级正职" if zheng else "区级副职"),"as_of":AS_OF,"is_current_confirmed":True,"source_ids":[]},
        "career_timeline":timeline or [],
        "organizations":[],
        "relationships":rel_list or [],
        "governance_record":[],
        "professional_profile":{"primary_specializations":[],"secondary_specializations":[],"career_pattern":"unknown","systems_experience":[],"geographic_pattern":[],"promotion_velocity":{"summary":"","notable_fast_promotions":[]}},
        "work_style_and_personality":{"public_style_indicators":[],"speech_themes":[],"management_signals":[],"caveat":"Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics":{},
        "risk_and_integrity_signals":[{"type":"none_found","description":"在公开信息中未发现该人物负面信号","date":"","confidence":"confirmed","source_ids":[]}],
        "source_register":SOURCE_REGISTER,
        "confidence_summary":{"identity":("confirmed" if has_bio else "plausible"),"current_role":"confirmed","career_completeness":("partial" if has_conf else "thin"),"relationship_confidence":"medium","biggest_gap":((f"{p['name']}的完整履历和出生信息有待补充") if not has_bio else f"{p['name']}早期职业生涯需确认")},
        "open_questions":[{"priority":("critical" if is_key else ("high" if has_conf else "medium")),"question":f"{p['name']}的完整职业生涯履历和出生信息","why_it_matters":"无法追溯其任职路径和系统经历","suggested_queries":[f"{p['name']} 简历 魏都区",f"{p['name']} 百度百科"],"last_attempted":AS_OF}],
    }

def build():
    print("="*60)
    print("  许昌市魏都区领导班子工作关系网络 | 市辖区 | 2026-08-05")
    print("="*60)
    run_build(slug=SLUG, persons=persons, organizations=organizations, positions=positions, relationships=relationships, db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print(f"DB: {DB_PATH}\nGEXF: {GEXF_PATH}" )
    # Person JSONs
    reg = [dict(r) for r in SOURCE_REGISTER]
    # 何长成 (区委书记)
    he_tl = [{"start":"","end":"","org":"中共许昌市魏都区委员会","title":"魏都区委书记","notes":"主持区十六次党代会(2026-06-23)、区委常委会;公开履历有限,出生信息待查","confidence":"confirmed","source_ids":["S02","S03","S07"]},{"start":"unknown","end":"unknown","org":"中共许昌市魏都区委员会","title":"此前任区委领导","notes":"代表区十五届委员会作报告,具体路径待核","confidence":"unverified","source_ids":["S02"]}]
    he_rel = [
        {"person":"李淼","person_id":"weiduqu_李淼","relationship_type":"overlap","strength":"strong","evidence":"区委书记与区长党政搭档","overlap_org":"魏都区","overlap_period":"2026年","direction":"undirected","confidence":"confirmed","source_ids":["S04","S05"]},
        {"person":"屈红雨","person_id":"weiduqu_屈红雨","relationship_type":"overlap","strength":"strong","evidence":"区委书记与区委副书记","overlap_org":"中共魏都区委","overlap_period":"2026年","direction":"undirected","confidence":"confirmed","source_ids":["S02"]},
        {"person":"申健民","person_id":"weiduqu_申健民","relationship_type":"overlap","strength":"medium","evidence":"共同八一慰问","overlap_org":"魏都区","overlap_period":"2026年","direction":"undirected","confidence":"confirmed","source_ids":["S04"]},
        {"person":"杜晓辉","person_id":"weiduqu_杜晓辉","relationship_type":"overlap","strength":"medium","evidence":"共同八一慰问","overlap_org":"魏都区","overlap_period":"2026年","direction":"undirected","confidence":"confirmed","source_ids":["S04"]},
        {"person":"张二峰","person_id":"weiduqu_张二峰","relationship_type":"overlap","strength":"strong","evidence":"低效用地例会","overlap_org":"魏都区","overlap_period":"2026年","direction":"undirected","confidence":"confirmed","source_ids":["S05"]},
    ]
    # 李淼 (区长)
    li_tl = [
        {"start":"","end":"","org":"中共魏都区委员会","title":"区委副书记","notes":"区政府党组书记","confidence":"confirmed","source_ids":["S01","S04"]},
        {"start":"","end":"","org":"魏都区人民政府","title":"魏都区区长","notes":"主持区政府全面工作;负责审计","confidence":"confirmed","source_ids":["S01","S05"]},
    ]
    li_rel = [
        {"person":"何长成","person_id":"weiduqu_何长成","relationship_type":"overlap","strength":"strong","evidence":"区长与区委书记党政搭档","overlap_org":"魏都区","overlap_period":"2026年","direction":"undirected","confidence":"confirmed","source_ids":["S04","S05"]},
        {"person":"张二峰","person_id":"weiduqu_张二峰","relationship_type":"overlap","strength":"strong","evidence":"区长与常务副区长","overlap_org":"魏都区政府","overlap_period":"2026年","direction":"undirected","confidence":"confirmed","source_ids":["S05"]},
    ]
    # 屈红雨 (区委副书记)
    qh_tl = [{"start":"","end":"","org":"中共魏都区委员会","title":"魏都区委副书记","notes":"主持区十六次党代会大会;分工待确认","confidence":"plausible","source_ids":["S02"]}]
    qh_rel = [{"person":"何长成","person_id":"weiduqu_何长成","relationship_type":"overlap","strength":"strong","evidence":"区委副书记与区委书记","overlap_org":"中共魏都区委","overlap_period":"2026年","direction":"undirected","confidence":"confirmed","source_ids":["S02"]}]

    jobs = [
        (persons[0], "区委书记-何长成", he_tl, he_rel, True),
        (persons[1], "区长-李淼", li_tl, li_rel, True),
        (persons[2], "区委副书记-屈红雨", qh_tl, qh_rel, False),
    ]
    for p, label, tl, rel, key in jobs:
        obj = make_person_json(p, tl, rel, key)
        role = {"何长成":"区委书记", "李淼":"区长", "屈红雨":"区委副书记"}[p['name']]
        out = PERSONS_DIR / f"{TODAY}-河南省-许昌市-{role}-{p['name']}.json"
        with open(out,"w",encoding="utf-8") as f: json.dump(obj, f, ensure_ascii=False, indent=2)
        print("  Person JSON:", out.name)

if __name__ == "__main__":
    build()

