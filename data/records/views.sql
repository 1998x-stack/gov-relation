CREATE VIEW gold_commercial_claims AS
SELECT DISTINCT c.* FROM claims c
JOIN evidence_links e ON e.subject_type='claim' AND e.subject_id=c.claim_id
JOIN gold_commercial_sources s ON s.source_id=e.source_id
;
CREATE VIEW gold_commercial_persons AS
SELECT DISTINCT p.* FROM persons p
JOIN evidence_links e ON e.subject_type='person' AND e.subject_id=p.person_id
JOIN gold_commercial_sources s ON s.source_id=e.source_id
;
CREATE VIEW gold_commercial_positions AS
SELECT DISTINCT p.* FROM positions p
JOIN evidence_links e ON e.subject_type='position' AND e.subject_id=p.position_id
JOIN gold_commercial_sources s ON s.source_id=e.source_id
;
CREATE VIEW gold_commercial_relationships AS
SELECT DISTINCT r.* FROM relationships r
JOIN evidence_links e ON e.subject_type='relationship' AND e.subject_id=r.relationship_id
JOIN gold_commercial_sources s ON s.source_id=e.source_id
;
CREATE VIEW gold_commercial_sources AS
SELECT s.* FROM sources s
JOIN source_rights_decisions d ON d.source_id=s.source_id
WHERE d.decision='cleared'
  AND instr(d.permitted_uses_json, '"commercial_distribution"') > 0
  AND datetime(d.effective_from) <= CURRENT_TIMESTAMP
  AND (d.effective_to IS NULL OR datetime(d.effective_to) >= CURRENT_TIMESTAMP)
  AND d.rowid = (
      SELECT d2.rowid FROM source_rights_decisions d2
      WHERE d2.source_id=s.source_id
        AND datetime(d2.effective_from) <= CURRENT_TIMESTAMP
        AND (d2.effective_to IS NULL OR datetime(d2.effective_to) >= CURRENT_TIMESTAMP)
      ORDER BY datetime(d2.effective_from) DESC, d2.rowid DESC
      LIMIT 1
  )
;
CREATE VIEW gold_current_positions AS
SELECT p.person_id, p.canonical_name, ps.title, o.canonical_name AS organization_name,
       ps.rank, ps.start_text, ps.end_text, ps.confidence
FROM positions ps
JOIN persons p ON p.person_id = ps.person_id
LEFT JOIN organizations o ON o.organization_id = ps.organization_id
WHERE ps.is_current = 1
;
CREATE VIEW gold_relationship_edges AS
SELECT r.relationship_id, a.canonical_name AS person_from, b.canonical_name AS person_to,
       r.relationship_type, r.direction, r.strength, r.confidence,
       r.context, r.overlap_period_text
FROM relationships r
JOIN persons a ON a.person_id = r.person_from_id
JOIN persons b ON b.person_id = r.person_to_id
;
