
from sqlalchemy import UniqueConstraint

from app.models import Base, CandidateProfile
from app.models.domain import ResumeValidation


def test_models_register_existing_tables():
    expected_tables = {
        "users",
        "candidate_profiles",
        "candidate_skills",
        "projects",
        "experiences",
        "educations",
        "certifications",
        "master_resumes",
        "jobs",
        "job_requirements",
        "match_analyses",
        "tailored_resumes",
        "resume_artifacts",
        "resume_validations",
        "applications",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())


def test_candidate_profile_uses_existing_table_name():
    assert CandidateProfile.__tablename__ == "candidate_profiles"


def test_candidate_profile_has_required_user_reference():
    table = CandidateProfile.__table__

    assert "user_id" in table.c
    assert table.c.user_id.nullable is False


def test_candidate_profile_user_reference_is_unique():
    table = CandidateProfile.__table__

    has_unique_constraint = any(
        isinstance(constraint, UniqueConstraint)
        and [column.name for column in constraint.columns] == ["user_id"]
        for constraint in table.constraints
    )

    has_unique_index = any(
        index.unique
        and [column.name for column in index.columns] == ["user_id"]
        for index in table.indexes
    )

    assert has_unique_constraint or has_unique_index


def test_candidate_profile_user_foreign_key_cascades_on_delete():
    foreign_keys = CandidateProfile.__table__.c.user_id.foreign_keys

    assert any(
        foreign_key.target_fullname == "users.id"
        and foreign_key.ondelete == "CASCADE"
        for foreign_key in foreign_keys
    )


def test_candidate_profile_contains_expected_profile_fields():
    expected_columns = {
        "id",
        "user_id",
        "headline",
        "summary",
        "phone",
        "location",
        "linkedin_url",
        "github_url",
        "portfolio_url",
        "created_at",
        "updated_at",
    }

    assert expected_columns.issubset(
        CandidateProfile.__table__.columns.keys()
    )


def test_resume_validation_maps_to_existing_table():
    assert ResumeValidation.__tablename__ == "resume_validations"
    assert "tailored_resume_id" in ResumeValidation.__table__.c
    assert "user_id" in ResumeValidation.__table__.c
