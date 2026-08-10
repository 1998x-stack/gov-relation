\set ON_ERROR_STOP on

DO $$
DECLARE
    expected_schemas text[] := ARRAY['meta', 'ingest', 'registry', 'evidence', 'assertion', 'review', 'publishing'];
    schema_name text;
BEGIN
    FOREACH schema_name IN ARRAY expected_schemas LOOP
        IF NOT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = schema_name) THEN
            RAISE EXCEPTION 'missing schema: %', schema_name;
        END IF;
    END LOOP;
END;
$$;

DO $$
DECLARE
    expected_tables text[] := ARRAY[
        'meta.schema_migrations', 'meta.audit_events',
        'ingest.datasets', 'ingest.runs', 'ingest.raw_records', 'ingest.entity_provenance',
        'registry.jurisdictions', 'registry.organizations', 'registry.persons',
        'registry.person_identity_keys', 'registry.person_aliases',
        'evidence.sources', 'evidence.source_assets', 'evidence.rights_decisions', 'evidence.evidence_links',
        'assertion.assertions', 'assertion.position_assertions',
        'assertion.relationship_assertions', 'assertion.attribute_assertions',
        'review.resolution_candidates', 'review.merge_decisions', 'review.decisions', 'review.quality_issues',
        'publishing.releases', 'publishing.release_items', 'publishing.release_metrics'
    ];
    table_name text;
BEGIN
    FOREACH table_name IN ARRAY expected_tables LOOP
        IF to_regclass(table_name) IS NULL THEN
            RAISE EXCEPTION 'missing table: %', table_name;
        END IF;
    END LOOP;
END;
$$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM meta.schema_migrations
        WHERE version = '0001' AND checksum ~ '^[0-9a-f]{64}$'
    ) THEN
        RAISE EXCEPTION 'migration 0001 is not registered with a valid checksum';
    END IF;

    IF EXISTS (SELECT 1 FROM pg_constraint WHERE NOT convalidated) THEN
        RAISE EXCEPTION 'database contains unvalidated constraints';
    END IF;

    IF (SELECT count(*) FROM pg_trigger
        WHERE NOT tgisinternal AND tgname IN (
            'position_assertion_type_guard', 'relationship_assertion_type_guard',
            'attribute_assertion_type_guard', 'current_position_observed_guard',
            'assertion_base_update_guard', 'release_item_gate'
        )) <> 6 THEN
        RAISE EXCEPTION 'expected six domain invariant triggers';
    END IF;
END;
$$;

BEGIN;

DO $$
DECLARE
    jurisdiction uuid;
    organization uuid;
    first_person uuid;
    second_person uuid;
    current_assertion uuid;
    wrong_type_assertion uuid;
    relation_assertion uuid;
    release uuid;
    source uuid;
    asset uuid;
    rights uuid;
    rejected boolean;
BEGIN
    INSERT INTO registry.jurisdictions(name, normalized_name, level)
    VALUES ('测试省', '测试省', 'province') RETURNING jurisdiction_id INTO jurisdiction;

    INSERT INTO registry.organizations(jurisdiction_id, canonical_name, normalized_name)
    VALUES (jurisdiction, '测试省人民政府', '测试省人民政府') RETURNING organization_id INTO organization;

    INSERT INTO registry.persons(canonical_name, normalized_name, identity_status)
    VALUES ('甲', '甲', 'verified') RETURNING person_id INTO first_person;
    INSERT INTO registry.persons(canonical_name, normalized_name, identity_status)
    VALUES ('乙', '乙', 'verified') RETURNING person_id INTO second_person;

    INSERT INTO assertion.assertions(assertion_type, confidence, review_status, created_by)
    VALUES ('position', 'confirmed', 'reviewed', 'verification') RETURNING assertion_id INTO current_assertion;

    rejected := false;
    BEGIN
        INSERT INTO assertion.position_assertions(
            assertion_id, person_id, organization_id, title, is_current
        ) VALUES (current_assertion, first_person, organization, '省长', true);
    EXCEPTION WHEN check_violation THEN
        rejected := true;
    END;
    IF NOT rejected THEN
        RAISE EXCEPTION 'current position without observed_at was accepted';
    END IF;

    UPDATE assertion.assertions SET observed_at = clock_timestamp()
    WHERE assertion_id = current_assertion;
    INSERT INTO assertion.position_assertions(
        assertion_id, person_id, organization_id, title, is_current
    ) VALUES (current_assertion, first_person, organization, '省长', true);

    INSERT INTO assertion.assertions(assertion_type, confidence, created_by)
    VALUES ('attribute', 'confirmed', 'verification') RETURNING assertion_id INTO wrong_type_assertion;
    rejected := false;
    BEGIN
        INSERT INTO assertion.position_assertions(
            assertion_id, person_id, organization_id, title
        ) VALUES (wrong_type_assertion, first_person, organization, '错误类型');
    EXCEPTION WHEN check_violation THEN
        rejected := true;
    END;
    IF NOT rejected THEN
        RAISE EXCEPTION 'assertion subtype mismatch was accepted';
    END IF;

    INSERT INTO assertion.assertions(assertion_type, confidence, review_status, created_by)
    VALUES ('relationship', 'confirmed', 'reviewed', 'verification') RETURNING assertion_id INTO relation_assertion;
    INSERT INTO assertion.relationship_assertions(
        assertion_id, person_from_id, person_to_id, relationship_type, direction,
        strength, evidence_summary, overlap_organization_id, overlap_from
    ) VALUES (
        relation_assertion, first_person, second_person, 'overlap', 'undirected',
        'strong', '同机构同期任职', organization, DATE '2020-01-01'
    );

    INSERT INTO publishing.releases(
        release_key, corpus_version, schema_version, code_version, cutoff_at,
        manifest_sha256, created_by
    ) VALUES (
        'verification', 'test', '0001', 'test', clock_timestamp(), repeat('a', 64), 'verification'
    ) RETURNING release_id INTO release;

    rejected := false;
    BEGIN
        INSERT INTO publishing.release_items(
            release_id, assertion_id, rights_decision_id, visibility, entitlement_class
        ) VALUES (release, relation_assertion, gen_random_uuid(), 'api', 'test');
    EXCEPTION WHEN foreign_key_violation OR check_violation THEN
        rejected := true;
    END;
    IF NOT rejected THEN
        RAISE EXCEPTION 'release item without evidence/rights was accepted';
    END IF;

    INSERT INTO evidence.sources(publisher, canonical_domain, source_type, reliability)
    VALUES ('测试政府', 'example.gov', 'official', 'high') RETURNING source_id INTO source;
    INSERT INTO evidence.source_assets(
        source_id, canonical_url, captured_at, content_sha256, storage_key
    ) VALUES (
        source, 'https://example.gov/test', clock_timestamp(), repeat('b', 64), 'test/source'
    ) RETURNING source_asset_id INTO asset;
    INSERT INTO evidence.evidence_links(assertion_id, source_asset_id)
    VALUES (relation_assertion, asset);
    INSERT INTO evidence.rights_decisions(
        source_id, decision, permitted_uses, legal_memo_ref, reviewer_id, effective_from
    ) VALUES (
        source, 'cleared', ARRAY['commercial_distribution'], 'TEST-ONLY', 'verification', clock_timestamp()
    ) RETURNING rights_decision_id INTO rights;
    INSERT INTO publishing.release_items(
        release_id, assertion_id, rights_decision_id, visibility, entitlement_class
    ) VALUES (release, relation_assertion, rights, 'api', 'test');
END;
$$;

ROLLBACK;

SELECT 'postgres schema 0001 verification passed' AS result;
