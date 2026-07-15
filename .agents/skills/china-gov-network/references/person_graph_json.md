# Person Graph JSON Reference

Use this reference when creating `data/persons/YYYYMMDD-{province}-{city}-{job}-{name}.json`.
This file is a deep, evidence-backed person profile, not only a resume. It should support
future graph merging, narrative analysis, and targeted follow-up research.

## Filename

```text
data/persons/YYYYMMDD-{province}-{city}-{job}-{name}.json
```

Rules:

- Use Chinese names in the filename when the source material is Chinese.
- Keep `{job}` short: `县委书记`, `区长`, `市长`, `省委书记`, etc.
- If city is not applicable for a province-level figure, use province name for `{city}` or `省本级`.
- If the same person has multiple roles, make the filename reflect the role under investigation.

## Top-Level Schema

```json
{
  "schema_version": "1.0",
  "generated_at": "YYYY-MM-DD",
  "investigation_scope": {
    "province": "",
    "city": "",
    "region": "",
    "job": "",
    "task_id": "",
    "time_focus": ""
  },
  "identity": {},
  "current_status": {},
  "career_timeline": [],
  "organizations": [],
  "relationships": [],
  "governance_record": [],
  "professional_profile": {},
  "work_style_and_personality": {},
  "network_metrics": {},
  "risk_and_integrity_signals": [],
  "source_register": [],
  "confidence_summary": {},
  "open_questions": []
}
```

## Required Detail

### identity

Capture stable identity fields for deduplication:

```json
{
  "person_id": "province_city_name_birthyear_optional",
  "name": "",
  "aliases": [],
  "gender": "",
  "ethnicity": "",
  "birth": "",
  "birthplace": "",
  "native_place": "",
  "education": [
    {
      "period": "",
      "institution": "",
      "major": "",
      "degree": "",
      "study_type": "full_time|part_time|party_school|unknown",
      "source_ids": []
    }
  ],
  "party_join": "",
  "work_start": "",
  "dedupe_keys": {
    "name_birth": "",
    "name_birthplace": "",
    "official_profile_url": ""
  }
}
```

### current_status

Record the current role and evidence freshness:

```json
{
  "current_post": "",
  "current_org": "",
  "administrative_rank": "",
  "as_of": "YYYY-MM-DD",
  "is_current_confirmed": true,
  "source_ids": []
}
```

### career_timeline

Use a table-like list. Every position should have dates and source IDs when possible.

```json
{
  "start": "YYYY-MM or YYYY",
  "end": "YYYY-MM or present or unknown",
  "org": "",
  "title": "",
  "level": "",
  "location": "",
  "system": "party|government|discipline|organization|propaganda|development_zone|state_owned_enterprise|education|other",
  "rank": "",
  "is_key_promotion": false,
  "notes": "",
  "confidence": "confirmed|plausible|unverified",
  "source_ids": []
}
```

Flag gaps explicitly:

```json
{
  "start": "unknown",
  "end": "unknown",
  "org": "履历缺口",
  "title": "",
  "notes": "公开资料未找到 2001-2008 年履历",
  "confidence": "unverified",
  "source_ids": []
}
```

### relationships

Model evidence, not gossip. Relationship records can be converted to graph edges.

```json
{
  "person": "",
  "person_id": "",
  "relationship_type": "overlap|predecessor_successor|superior_subordinate|same_native_place|same_school|same_system|promotion_chain|reported_association|family|other",
  "strength": "strong|medium|weak",
  "evidence": "",
  "overlap_org": "",
  "overlap_period": "",
  "direction": "undirected|person_to_other|other_to_person",
  "confidence": "confirmed|plausible|unverified",
  "source_ids": []
}
```

Strength guidance:

- `strong`: same organization and overlapping time in clearly related roles; direct predecessor/successor; explicit source says they worked together.
- `medium`: same system/area with likely interaction but limited direct overlap evidence.
- `weak`: same school/native place/general network lead without operational evidence.

### governance_record

Capture public achievements and policy domains, with evidence:

```json
{
  "period": "",
  "domain": "economic_development|urban_construction|poverty_alleviation|rural_revitalization|discipline|public_security|industry|education|health|environment|other",
  "achievement_or_event": "",
  "role_in_event": "",
  "measurable_outcome": "",
  "location": "",
  "confidence": "confirmed|plausible|unverified",
  "source_ids": []
}
```

### professional_profile

Summarize expertise and career pattern:

```json
{
  "primary_specializations": [],
  "secondary_specializations": [],
  "career_pattern": "local_ladder|cross_county_rotation|provincial_department|technical_specialist|discipline_track|organization_track|unknown",
  "systems_experience": [],
  "geographic_pattern": [],
  "promotion_velocity": {
    "summary": "",
    "notable_fast_promotions": []
  }
}
```

### work_style_and_personality

Only infer from public evidence and mark confidence. Do not invent psychological claims.

```json
{
  "public_style_indicators": [
    {
      "trait": "pragmatic|technocratic|discipline_oriented|grassroots_oriented|media_visible|low_profile|reform_oriented|stability_oriented|unknown",
      "evidence": "",
      "confidence": "confirmed|plausible|unverified",
      "source_ids": []
    }
  ],
  "speech_themes": [],
  "management_signals": [],
  "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
}
```

### risk_and_integrity_signals

Record only source-backed signals:

```json
{
  "type": "disciplinary_action|inspection_feedback|controversy|audit_issue|negative_media|none_found",
  "description": "",
  "date": "",
  "confidence": "confirmed|plausible|unverified",
  "source_ids": []
}
```

If no risk signal is found, write a `none_found` record with search scope and date.

### source_register

Use stable source IDs so timeline and relationships can cite compactly:

```json
{
  "id": "S001",
  "title": "",
  "url": "",
  "publisher": "",
  "published_at": "",
  "accessed_at": "YYYY-MM-DD",
  "source_type": "official|appointment_notice|media|encyclopedia|database|inferred",
  "reliability": "high|medium|low",
  "notes": ""
}
```

### confidence_summary

```json
{
  "identity": "confirmed|plausible|unverified",
  "current_role": "confirmed|plausible|unverified",
  "career_completeness": "complete|partial|thin",
  "relationship_confidence": "high|medium|low",
  "biggest_gap": ""
}
```

### open_questions

```json
{
  "priority": "critical|high|medium|low",
  "question": "",
  "why_it_matters": "",
  "suggested_queries": [],
  "last_attempted": "YYYY-MM-DD"
}
```

## Validation

Run:

```bash
python3 -m json.tool data/persons/YYYYMMDD-{province}-{city}-{job}-{name}.json
```

Use UTF-8 JSON and `ensure_ascii=False` if generated by Python. Avoid comments and trailing commas.

