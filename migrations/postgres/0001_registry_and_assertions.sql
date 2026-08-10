\set ON_ERROR_STOP on

BEGIN;

CREATE SCHEMA IF NOT EXISTS meta;
CREATE SCHEMA IF NOT EXISTS ingest;
CREATE SCHEMA IF NOT EXISTS registry;
CREATE SCHEMA IF NOT EXISTS evidence;
CREATE SCHEMA IF NOT EXISTS assertion;
CREATE SCHEMA IF NOT EXISTS review;
CREATE SCHEMA IF NOT EXISTS publishing;

CREATE TABLE IF NOT EXISTS meta.schema_migrations (
    version text PRIMARY KEY,
    name text NOT NULL,
    checksum char(64) NOT NULL CHECK (checksum ~ '^[0-9a-f]{64}$'),
    applied_at timestamptz NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE IF NOT EXISTS meta.audit_events (
    event_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id text NOT NULL,
    action text NOT NULL,
    target_type text NOT NULL,
    target_id text NOT NULL,
    request_id text,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    occurred_at timestamptz NOT NULL DEFAULT clock_timestamp()
);

CREATE INDEX IF NOT EXISTS audit_events_target_idx
    ON meta.audit_events (target_type, target_id, occurred_at DESC);

CREATE TABLE IF NOT EXISTS registry.jurisdictions (
    jurisdiction_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_id uuid REFERENCES registry.jurisdictions(jurisdiction_id),
    name text NOT NULL CHECK (btrim(name) <> ''),
    normalized_name text NOT NULL CHECK (btrim(normalized_name) <> ''),
    administrative_code text,
    level text NOT NULL CHECK (level IN ('country', 'province', 'prefecture', 'county', 'township', 'other', 'unknown')),
    valid_from date,
    valid_to date,
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from),
    UNIQUE NULLS NOT DISTINCT (parent_id, normalized_name, level)
);

CREATE TABLE IF NOT EXISTS registry.organizations (
    organization_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    jurisdiction_id uuid REFERENCES registry.jurisdictions(jurisdiction_id),
    parent_organization_id uuid REFERENCES registry.organizations(organization_id),
    canonical_name text NOT NULL CHECK (btrim(canonical_name) <> ''),
    normalized_name text NOT NULL CHECK (btrim(normalized_name) <> ''),
    organization_type text NOT NULL DEFAULT 'unknown',
    administrative_level text NOT NULL DEFAULT '',
    valid_from date,
    valid_to date,
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from)
);

CREATE INDEX IF NOT EXISTS organizations_name_idx
    ON registry.organizations (normalized_name);
CREATE INDEX IF NOT EXISTS organizations_jurisdiction_idx
    ON registry.organizations (jurisdiction_id);

CREATE TABLE IF NOT EXISTS registry.persons (
    person_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    canonical_name text NOT NULL CHECK (btrim(canonical_name) <> ''),
    normalized_name text NOT NULL CHECK (btrim(normalized_name) <> ''),
    identity_status text NOT NULL DEFAULT 'unresolved'
        CHECK (identity_status IN ('verified', 'probable', 'unresolved', 'merged', 'suppressed')),
    merged_into_person_id uuid REFERENCES registry.persons(person_id),
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    updated_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    CHECK (
        (identity_status = 'merged' AND merged_into_person_id IS NOT NULL)
        OR (identity_status <> 'merged' AND merged_into_person_id IS NULL)
    )
);

CREATE INDEX IF NOT EXISTS persons_name_idx ON registry.persons (normalized_name);

CREATE TABLE IF NOT EXISTS registry.person_identity_keys (
    identity_key_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    person_id uuid NOT NULL REFERENCES registry.persons(person_id),
    key_type text NOT NULL CHECK (key_type IN ('name_birth', 'name_birthplace', 'official_profile', 'external_id', 'source_scoped')),
    key_value text NOT NULL CHECK (btrim(key_value) <> ''),
    scope_key text NOT NULL DEFAULT 'global',
    verification_status text NOT NULL DEFAULT 'unverified'
        CHECK (verification_status IN ('verified', 'probable', 'unverified', 'rejected')),
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    UNIQUE (person_id, key_type, key_value, scope_key)
);

CREATE INDEX IF NOT EXISTS person_identity_lookup_idx
    ON registry.person_identity_keys (key_type, key_value, scope_key);

CREATE UNIQUE INDEX IF NOT EXISTS person_verified_identity_unique_idx
    ON registry.person_identity_keys (key_type, key_value, scope_key)
    WHERE verification_status = 'verified';

CREATE TABLE IF NOT EXISTS registry.person_aliases (
    person_alias_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    person_id uuid NOT NULL REFERENCES registry.persons(person_id),
    alias text NOT NULL CHECK (btrim(alias) <> ''),
    normalized_alias text NOT NULL CHECK (btrim(normalized_alias) <> ''),
    alias_type text NOT NULL DEFAULT 'other',
    valid_from date,
    valid_to date,
    UNIQUE (person_id, normalized_alias, alias_type),
    CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from)
);

CREATE TABLE IF NOT EXISTS ingest.datasets (
    dataset_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_key text NOT NULL UNIQUE,
    dataset_kind text NOT NULL CHECK (dataset_kind IN ('legacy_sqlite', 'person_profile', 'research_package', 'manual')),
    source_path text NOT NULL,
    content_sha256 char(64) NOT NULL CHECK (content_sha256 ~ '^[0-9a-f]{64}$'),
    jurisdiction_id uuid REFERENCES registry.jurisdictions(jurisdiction_id),
    created_at timestamptz NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE IF NOT EXISTS ingest.runs (
    run_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    idempotency_key text NOT NULL UNIQUE,
    mode text NOT NULL,
    code_version text NOT NULL,
    schema_version text NOT NULL,
    status text NOT NULL CHECK (status IN ('running', 'succeeded', 'failed', 'partial')),
    started_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    finished_at timestamptz,
    input_count bigint NOT NULL DEFAULT 0 CHECK (input_count >= 0),
    imported_count bigint NOT NULL DEFAULT 0 CHECK (imported_count >= 0),
    rejected_count bigint NOT NULL DEFAULT 0 CHECK (rejected_count >= 0),
    result jsonb NOT NULL DEFAULT '{}'::jsonb,
    CHECK (finished_at IS NULL OR finished_at >= started_at)
);

CREATE TABLE IF NOT EXISTS ingest.raw_records (
    raw_record_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id uuid NOT NULL REFERENCES ingest.datasets(dataset_id),
    source_table text NOT NULL,
    source_pk text NOT NULL,
    payload jsonb NOT NULL,
    payload_sha256 char(64) NOT NULL CHECK (payload_sha256 ~ '^[0-9a-f]{64}$'),
    imported_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    UNIQUE (dataset_id, source_table, source_pk)
);

CREATE TABLE IF NOT EXISTS ingest.entity_provenance (
    provenance_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id uuid NOT NULL REFERENCES ingest.datasets(dataset_id),
    raw_record_id uuid REFERENCES ingest.raw_records(raw_record_id),
    entity_type text NOT NULL,
    entity_id uuid NOT NULL,
    source_field text NOT NULL DEFAULT '',
    transformation text NOT NULL,
    transformer_version text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    UNIQUE NULLS NOT DISTINCT (dataset_id, raw_record_id, entity_type, entity_id, source_field)
);

CREATE TABLE IF NOT EXISTS evidence.sources (
    source_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    publisher text NOT NULL DEFAULT '',
    canonical_domain text NOT NULL DEFAULT '',
    source_type text NOT NULL CHECK (source_type IN ('official', 'appointment_notice', 'media', 'encyclopedia', 'database', 'inferred', 'other')),
    reliability text NOT NULL CHECK (reliability IN ('high', 'medium', 'low')),
    created_at timestamptz NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE IF NOT EXISTS evidence.source_assets (
    source_asset_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id uuid NOT NULL REFERENCES evidence.sources(source_id),
    canonical_url text NOT NULL DEFAULT '',
    captured_at timestamptz NOT NULL,
    published_at timestamptz,
    http_status integer,
    media_type text NOT NULL DEFAULT '',
    content_sha256 char(64) NOT NULL CHECK (content_sha256 ~ '^[0-9a-f]{64}$'),
    storage_key text NOT NULL,
    parser_version text NOT NULL DEFAULT '',
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE (source_id, canonical_url, content_sha256)
);

CREATE INDEX IF NOT EXISTS source_assets_url_idx ON evidence.source_assets (canonical_url);

CREATE TABLE IF NOT EXISTS evidence.rights_decisions (
    rights_decision_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id uuid NOT NULL REFERENCES evidence.sources(source_id),
    decision text NOT NULL CHECK (decision IN ('cleared', 'restricted', 'unknown')),
    permitted_uses text[] NOT NULL DEFAULT ARRAY[]::text[],
    permitted_fields text[] NOT NULL DEFAULT ARRAY[]::text[],
    restrictions jsonb NOT NULL DEFAULT '{}'::jsonb,
    legal_memo_ref text NOT NULL DEFAULT '',
    reviewer_id text NOT NULL,
    effective_from timestamptz NOT NULL,
    effective_to timestamptz,
    decided_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    CHECK (effective_to IS NULL OR effective_to > effective_from),
    CHECK (
        decision <> 'cleared'
        OR (cardinality(permitted_uses) > 0 AND btrim(legal_memo_ref) <> '')
    )
);

CREATE INDEX IF NOT EXISTS rights_decisions_effective_idx
    ON evidence.rights_decisions (source_id, effective_from DESC);

CREATE TABLE IF NOT EXISTS assertion.assertions (
    assertion_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    assertion_type text NOT NULL CHECK (assertion_type IN ('position', 'relationship', 'attribute')),
    confidence text NOT NULL CHECK (confidence IN ('confirmed', 'plausible', 'unverified')),
    review_status text NOT NULL DEFAULT 'draft'
        CHECK (review_status IN ('draft', 'reviewed', 'rejected', 'superseded', 'withdrawn')),
    valid_from date,
    valid_to date,
    date_precision text NOT NULL DEFAULT 'unknown'
        CHECK (date_precision IN ('day', 'month', 'year', 'range', 'unknown')),
    original_date_text text NOT NULL DEFAULT '',
    observed_at timestamptz,
    system_from timestamptz NOT NULL DEFAULT clock_timestamp(),
    system_to timestamptz,
    supersedes_assertion_id uuid REFERENCES assertion.assertions(assertion_id),
    created_by text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from),
    CHECK (system_to IS NULL OR system_to > system_from),
    CHECK (supersedes_assertion_id IS NULL OR supersedes_assertion_id <> assertion_id)
);

CREATE INDEX IF NOT EXISTS assertions_status_idx
    ON assertion.assertions (review_status, assertion_type, confidence);
CREATE INDEX IF NOT EXISTS assertions_valid_time_idx
    ON assertion.assertions (valid_from, valid_to);

CREATE TABLE IF NOT EXISTS assertion.position_assertions (
    assertion_id uuid PRIMARY KEY REFERENCES assertion.assertions(assertion_id) ON DELETE CASCADE,
    person_id uuid NOT NULL REFERENCES registry.persons(person_id),
    organization_id uuid REFERENCES registry.organizations(organization_id),
    organization_text text NOT NULL DEFAULT '',
    title text NOT NULL CHECK (btrim(title) <> ''),
    rank text NOT NULL DEFAULT '',
    category text NOT NULL DEFAULT '',
    is_current boolean NOT NULL DEFAULT false,
    notes text NOT NULL DEFAULT '',
    CHECK (organization_id IS NOT NULL OR btrim(organization_text) <> '')
);

CREATE INDEX IF NOT EXISTS position_assertions_person_idx
    ON assertion.position_assertions (person_id);
CREATE INDEX IF NOT EXISTS position_assertions_org_idx
    ON assertion.position_assertions (organization_id);

CREATE TABLE IF NOT EXISTS assertion.relationship_assertions (
    assertion_id uuid PRIMARY KEY REFERENCES assertion.assertions(assertion_id) ON DELETE CASCADE,
    person_from_id uuid NOT NULL REFERENCES registry.persons(person_id),
    person_to_id uuid NOT NULL REFERENCES registry.persons(person_id),
    relationship_type text NOT NULL CHECK (btrim(relationship_type) <> ''),
    direction text NOT NULL CHECK (direction IN ('undirected', 'from_to', 'to_from')),
    strength text NOT NULL CHECK (strength IN ('strong', 'medium', 'weak', 'unknown')),
    context text NOT NULL DEFAULT '',
    evidence_summary text NOT NULL DEFAULT '',
    overlap_organization_id uuid REFERENCES registry.organizations(organization_id),
    overlap_from date,
    overlap_to date,
    CHECK (person_from_id <> person_to_id),
    CHECK (overlap_to IS NULL OR overlap_from IS NULL OR overlap_to >= overlap_from),
    CHECK (
        strength <> 'strong'
        OR btrim(evidence_summary) <> ''
        OR (overlap_organization_id IS NOT NULL AND overlap_from IS NOT NULL)
    )
);

CREATE INDEX IF NOT EXISTS relationship_assertions_from_idx
    ON assertion.relationship_assertions (person_from_id);
CREATE INDEX IF NOT EXISTS relationship_assertions_to_idx
    ON assertion.relationship_assertions (person_to_id);

CREATE TABLE IF NOT EXISTS assertion.attribute_assertions (
    assertion_id uuid PRIMARY KEY REFERENCES assertion.assertions(assertion_id) ON DELETE CASCADE,
    subject_type text NOT NULL CHECK (subject_type IN ('person', 'organization', 'jurisdiction')),
    subject_id uuid NOT NULL,
    predicate text NOT NULL CHECK (btrim(predicate) <> ''),
    value jsonb NOT NULL
);

CREATE TABLE IF NOT EXISTS evidence.evidence_links (
    evidence_link_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    assertion_id uuid NOT NULL REFERENCES assertion.assertions(assertion_id) ON DELETE CASCADE,
    source_asset_id uuid NOT NULL REFERENCES evidence.source_assets(source_asset_id),
    evidence_role text NOT NULL DEFAULT 'supports'
        CHECK (evidence_role IN ('supports', 'contradicts', 'context')),
    locator text NOT NULL DEFAULT '',
    excerpt_hash char(64),
    notes text NOT NULL DEFAULT '',
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    CHECK (excerpt_hash IS NULL OR excerpt_hash ~ '^[0-9a-f]{64}$'),
    UNIQUE (assertion_id, source_asset_id, evidence_role, locator)
);

CREATE TABLE IF NOT EXISTS review.resolution_candidates (
    candidate_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type text NOT NULL CHECK (entity_type IN ('person', 'organization')),
    left_entity_id uuid NOT NULL,
    right_entity_id uuid NOT NULL,
    score numeric(5,4) NOT NULL CHECK (score >= 0 AND score <= 1),
    resolver_version text NOT NULL,
    reasons jsonb NOT NULL,
    status text NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'merged', 'rejected', 'expired')),
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    CHECK (left_entity_id <> right_entity_id),
    UNIQUE (entity_type, left_entity_id, right_entity_id, resolver_version)
);

CREATE TABLE IF NOT EXISTS review.merge_decisions (
    merge_decision_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id uuid NOT NULL REFERENCES review.resolution_candidates(candidate_id),
    decision text NOT NULL CHECK (decision IN ('merge', 'reject')),
    survivor_entity_id uuid,
    reviewer_id text NOT NULL,
    rationale text NOT NULL CHECK (btrim(rationale) <> ''),
    decided_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    CHECK ((decision = 'merge' AND survivor_entity_id IS NOT NULL) OR decision = 'reject')
);

CREATE TABLE IF NOT EXISTS review.decisions (
    review_decision_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    target_type text NOT NULL,
    target_id uuid NOT NULL,
    action text NOT NULL CHECK (action IN ('approve', 'reject', 'supersede', 'withdraw', 'suppress', 'restore')),
    reviewer_id text NOT NULL,
    rationale text NOT NULL CHECK (btrim(rationale) <> ''),
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    decided_at timestamptz NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE IF NOT EXISTS review.quality_issues (
    issue_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    issue_code text NOT NULL,
    severity text NOT NULL CHECK (severity IN ('error', 'warning', 'info')),
    target_type text NOT NULL DEFAULT '',
    target_id uuid,
    owner_id text,
    status text NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'resolved', 'ignored')),
    message text NOT NULL,
    details jsonb NOT NULL DEFAULT '{}'::jsonb,
    due_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    resolved_at timestamptz,
    CHECK ((status = 'resolved' AND resolved_at IS NOT NULL) OR status <> 'resolved')
);

CREATE INDEX IF NOT EXISTS quality_issues_queue_idx
    ON review.quality_issues (status, severity, issue_code, due_at);

CREATE TABLE IF NOT EXISTS publishing.releases (
    release_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    release_key text NOT NULL UNIQUE,
    status text NOT NULL DEFAULT 'building'
        CHECK (status IN ('building', 'ready', 'active', 'superseded', 'withdrawn')),
    corpus_version text NOT NULL,
    schema_version text NOT NULL,
    code_version text NOT NULL,
    cutoff_at timestamptz NOT NULL,
    manifest_sha256 char(64) NOT NULL CHECK (manifest_sha256 ~ '^[0-9a-f]{64}$'),
    signature text NOT NULL DEFAULT '',
    created_by text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    activated_at timestamptz
);

CREATE TABLE IF NOT EXISTS publishing.release_items (
    release_id uuid NOT NULL REFERENCES publishing.releases(release_id) ON DELETE CASCADE,
    assertion_id uuid NOT NULL REFERENCES assertion.assertions(assertion_id),
    rights_decision_id uuid NOT NULL REFERENCES evidence.rights_decisions(rights_decision_id),
    visibility text NOT NULL CHECK (visibility IN ('explorer', 'analyst', 'api', 'enterprise')),
    entitlement_class text NOT NULL,
    added_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    PRIMARY KEY (release_id, assertion_id, entitlement_class)
);

CREATE TABLE IF NOT EXISTS publishing.release_metrics (
    release_metric_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    release_id uuid NOT NULL REFERENCES publishing.releases(release_id) ON DELETE CASCADE,
    jurisdiction_id uuid REFERENCES registry.jurisdictions(jurisdiction_id),
    metric_name text NOT NULL,
    metric_value numeric NOT NULL,
    dimensions jsonb NOT NULL DEFAULT '{}'::jsonb,
    measured_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    UNIQUE NULLS NOT DISTINCT (release_id, jurisdiction_id, metric_name, dimensions)
);

CREATE OR REPLACE FUNCTION assertion.enforce_assertion_subtype()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    actual_type text;
BEGIN
    SELECT assertion_type INTO actual_type
    FROM assertion.assertions
    WHERE assertion_id = NEW.assertion_id;

    IF actual_type IS DISTINCT FROM TG_ARGV[0] THEN
        RAISE EXCEPTION 'assertion % has type %, expected %', NEW.assertion_id, actual_type, TG_ARGV[0]
            USING ERRCODE = 'check_violation';
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS position_assertion_type_guard ON assertion.position_assertions;
CREATE TRIGGER position_assertion_type_guard
BEFORE INSERT OR UPDATE ON assertion.position_assertions
FOR EACH ROW EXECUTE FUNCTION assertion.enforce_assertion_subtype('position');

DROP TRIGGER IF EXISTS relationship_assertion_type_guard ON assertion.relationship_assertions;
CREATE TRIGGER relationship_assertion_type_guard
BEFORE INSERT OR UPDATE ON assertion.relationship_assertions
FOR EACH ROW EXECUTE FUNCTION assertion.enforce_assertion_subtype('relationship');

DROP TRIGGER IF EXISTS attribute_assertion_type_guard ON assertion.attribute_assertions;
CREATE TRIGGER attribute_assertion_type_guard
BEFORE INSERT OR UPDATE ON assertion.attribute_assertions
FOR EACH ROW EXECUTE FUNCTION assertion.enforce_assertion_subtype('attribute');

CREATE OR REPLACE FUNCTION assertion.enforce_current_position_observed()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    observation timestamptz;
BEGIN
    IF NEW.is_current THEN
        SELECT observed_at INTO observation
        FROM assertion.assertions
        WHERE assertion_id = NEW.assertion_id;
        IF observation IS NULL THEN
            RAISE EXCEPTION 'current position assertion % requires observed_at', NEW.assertion_id
                USING ERRCODE = 'check_violation';
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS current_position_observed_guard ON assertion.position_assertions;
CREATE TRIGGER current_position_observed_guard
BEFORE INSERT OR UPDATE ON assertion.position_assertions
FOR EACH ROW EXECUTE FUNCTION assertion.enforce_current_position_observed();

CREATE OR REPLACE FUNCTION assertion.enforce_assertion_base_update()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.assertion_type <> OLD.assertion_type AND (
        EXISTS (SELECT 1 FROM assertion.position_assertions WHERE assertion_id = NEW.assertion_id)
        OR EXISTS (SELECT 1 FROM assertion.relationship_assertions WHERE assertion_id = NEW.assertion_id)
        OR EXISTS (SELECT 1 FROM assertion.attribute_assertions WHERE assertion_id = NEW.assertion_id)
    ) THEN
        RAISE EXCEPTION 'cannot change subtype of assertion % after detail creation', NEW.assertion_id
            USING ERRCODE = 'check_violation';
    END IF;

    IF NEW.observed_at IS NULL AND EXISTS (
        SELECT 1 FROM assertion.position_assertions
        WHERE assertion_id = NEW.assertion_id AND is_current
    ) THEN
        RAISE EXCEPTION 'current position assertion % requires observed_at', NEW.assertion_id
            USING ERRCODE = 'check_violation';
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS assertion_base_update_guard ON assertion.assertions;
CREATE TRIGGER assertion_base_update_guard
BEFORE UPDATE OF assertion_type, observed_at ON assertion.assertions
FOR EACH ROW EXECUTE FUNCTION assertion.enforce_assertion_base_update();

CREATE OR REPLACE FUNCTION publishing.enforce_release_item()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    assertion_state text;
    rights_state text;
    rights_uses text[];
    rights_source uuid;
BEGIN
    SELECT review_status INTO assertion_state
    FROM assertion.assertions
    WHERE assertion_id = NEW.assertion_id;
    IF assertion_state IS DISTINCT FROM 'reviewed' THEN
        RAISE EXCEPTION 'release assertion % must be reviewed', NEW.assertion_id
            USING ERRCODE = 'check_violation';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM evidence.evidence_links
        WHERE assertion_id = NEW.assertion_id AND evidence_role = 'supports'
    ) THEN
        RAISE EXCEPTION 'release assertion % requires supporting evidence', NEW.assertion_id
            USING ERRCODE = 'check_violation';
    END IF;

    SELECT decision, permitted_uses, source_id
    INTO rights_state, rights_uses, rights_source
    FROM evidence.rights_decisions
    WHERE rights_decision_id = NEW.rights_decision_id
      AND effective_from <= clock_timestamp()
      AND (effective_to IS NULL OR effective_to > clock_timestamp());

    IF rights_state IS DISTINCT FROM 'cleared'
       OR NOT ('commercial_distribution' = ANY(COALESCE(rights_uses, ARRAY[]::text[]))) THEN
        RAISE EXCEPTION 'release item lacks effective commercial rights'
            USING ERRCODE = 'check_violation';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM evidence.evidence_links link
        JOIN evidence.source_assets asset USING (source_asset_id)
        WHERE link.assertion_id = NEW.assertion_id
          AND link.evidence_role = 'supports'
          AND asset.source_id = rights_source
    ) THEN
        RAISE EXCEPTION 'rights decision source does not support assertion %', NEW.assertion_id
            USING ERRCODE = 'check_violation';
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS release_item_gate ON publishing.release_items;
CREATE TRIGGER release_item_gate
BEFORE INSERT OR UPDATE ON publishing.release_items
FOR EACH ROW EXECUTE FUNCTION publishing.enforce_release_item();

INSERT INTO meta.schema_migrations(version, name, checksum)
VALUES ('0001', 'registry_and_assertions', :'migration_checksum')
ON CONFLICT (version) DO NOTHING;

COMMIT;
