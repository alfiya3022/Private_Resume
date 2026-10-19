
from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


def timestamp_column():
    """Match the existing PostgreSQL TIMESTAMP WITH TIME ZONE columns."""
    return mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


# ---------------------------------------------------------------------------
# Candidate skills
# Existing table: candidate_skills
# Legacy columns: profile_id, name, category, proficiency
# ---------------------------------------------------------------------------

class Skill(Base):
    """Normalized skill catalog; requires a database migration."""
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    category: Mapped[str | None] = mapped_column(String(80))
    created_at: Mapped[datetime] = timestamp_column()


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"

    id: Mapped[int] = mapped_column(primary_key=True)

    candidate_profile_id: Mapped[int] = mapped_column(
        "profile_id",
        ForeignKey("candidate_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category: Mapped[str | None] = mapped_column(String(100))
    proficiency_level: Mapped[str | None] = mapped_column(
        "proficiency",
        String(50),
    )


# ---------------------------------------------------------------------------
# Projects
# Existing columns include profile_id, title, bullets, technologies and url.
# ---------------------------------------------------------------------------

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)

    candidate_profile_id: Mapped[int] = mapped_column(
        "profile_id",
        ForeignKey("candidate_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column("title", String(255), nullable=False)
    role: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)

    achievements: Mapped[list[Any]] = mapped_column(
        "bullets",
        JSON,
        nullable=False,
    )
    technologies: Mapped[list[Any]] = mapped_column(JSON, nullable=False)

    project_url: Mapped[str | None] = mapped_column("url", String(255))
    start_date: Mapped[str | None] = mapped_column(String(50))
    end_date: Mapped[str | None] = mapped_column(String(50))


class ProjectSkillEvidence(Base):
    """Normalized project-to-skill evidence; requires a database migration."""
    __tablename__ = "project_skill_evidence"
    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "skill_id",
            name="uq_project_skill_evidence",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    evidence_text: Mapped[str | None] = mapped_column(Text)
    evidence_type: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = timestamp_column()


# ---------------------------------------------------------------------------
# Experience
# ---------------------------------------------------------------------------

class Experience(Base):
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(primary_key=True)

    candidate_profile_id: Mapped[int] = mapped_column(
        "profile_id",
        ForeignKey("candidate_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    company_name: Mapped[str] = mapped_column(
        "company",
        String(255),
        nullable=False,
    )
    job_title: Mapped[str] = mapped_column(
        "title",
        String(255),
        nullable=False,
    )

    location: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)

    achievements: Mapped[list[Any]] = mapped_column(
        "bullets",
        JSON,
        nullable=False,
    )

    start_date: Mapped[str | None] = mapped_column(String(50))
    end_date: Mapped[str | None] = mapped_column(String(50))

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
        default=False,
    )


# ---------------------------------------------------------------------------
# Education
# Actual table name is "educations", not "education".
# ---------------------------------------------------------------------------

class Education(Base):
    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(primary_key=True)

    candidate_profile_id: Mapped[int] = mapped_column(
        "profile_id",
        ForeignKey("candidate_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    institution: Mapped[str] = mapped_column(String(255), nullable=False)
    qualification: Mapped[str] = mapped_column(
        "degree",
        String(255),
        nullable=False,
    )
    field_of_study: Mapped[str | None] = mapped_column(String(255))
    grade: Mapped[str | None] = mapped_column(String(50))
    start_date: Mapped[str | None] = mapped_column(String(50))
    end_date: Mapped[str | None] = mapped_column(String(50))


# ---------------------------------------------------------------------------
# Certifications
# ---------------------------------------------------------------------------

class Certification(Base):
    __tablename__ = "certifications"

    id: Mapped[int] = mapped_column(primary_key=True)

    candidate_profile_id: Mapped[int] = mapped_column(
        "profile_id",
        ForeignKey("candidate_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    issuing_organization: Mapped[str] = mapped_column(
        "issuer",
        String(255),
        nullable=False,
    )
    issue_date: Mapped[str | None] = mapped_column(String(50))
    credential_url: Mapped[str | None] = mapped_column(String(255))


# ---------------------------------------------------------------------------
# Master resumes
# ---------------------------------------------------------------------------

class MasterResume(Base):
    __tablename__ = "master_resumes"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    original_filename: Mapped[str] = mapped_column(
        "filename",
        String(255),
        nullable=False,
    )
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    extracted_text: Mapped[str] = mapped_column(
        "raw_text",
        Text,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
        default=True,
    )
    created_at: Mapped[datetime] = timestamp_column()


# ---------------------------------------------------------------------------
# Jobs
# ---------------------------------------------------------------------------

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    company_name: Mapped[str] = mapped_column(
        "company",
        String(255),
        nullable=False,
    )
    job_title: Mapped[str] = mapped_column(
        "title",
        String(255),
        nullable=False,
    )
    location: Mapped[str | None] = mapped_column(String(255))
    job_url: Mapped[str | None] = mapped_column(String(500))
    salary_text: Mapped[str | None] = mapped_column(
        "salary",
        String(100),
    )

    original_description: Mapped[str] = mapped_column(
        "raw_jd_text",
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        server_default=text("'active'"),
        default="active",
    )

    created_at: Mapped[datetime] = timestamp_column()
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


# ---------------------------------------------------------------------------
# Job requirements
# Existing database uses JSON, not JSONB.
# ---------------------------------------------------------------------------

class JobRequirement(Base):
    __tablename__ = "job_requirements"

    id: Mapped[int] = mapped_column(primary_key=True)

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    required_skills: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    preferred_skills: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    languages: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    frameworks: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    databases: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    tools: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    cloud: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    responsibilities: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    qualifications: Mapped[list[Any]] = mapped_column(JSON, nullable=False)

    experience_years: Mapped[str | None] = mapped_column(String(100))
    soft_skills: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    raw_analysis: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = timestamp_column()
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


# ---------------------------------------------------------------------------
# Match analysis
# ---------------------------------------------------------------------------

class MatchAnalysis(Base):
    __tablename__ = "match_analyses"

    id: Mapped[int] = mapped_column(primary_key=True)

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    estimated_match: Mapped[int] = mapped_column(
        "estimated_match_score",
        Integer,
        nullable=False,
    )

    matched_skills: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    weak_skills: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    missing_skills: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    unsupported_claims: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    evidence_map: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = timestamp_column()
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


# ---------------------------------------------------------------------------
# Normalized match results
# New table; requires a database migration.
# ---------------------------------------------------------------------------

class MatchResult(Base):
    __tablename__ = "match_results"
    __table_args__ = (
        UniqueConstraint(
            "match_analysis_id",
            "job_requirement_id",
            name="uq_match_results_analysis_requirement",
        ),
        CheckConstraint(
            "match_status IN ('matched', 'weak', 'missing', 'unsupported')",
            name="valid_match_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    match_analysis_id: Mapped[int] = mapped_column(
        ForeignKey("match_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_requirement_id: Mapped[int] = mapped_column(
        ForeignKey("job_requirements.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    match_status: Mapped[str] = mapped_column(String(20), nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text)
    evidence_refs: Mapped[list[Any] | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = timestamp_column()


# ---------------------------------------------------------------------------
# Tailored resumes
# ---------------------------------------------------------------------------

class TailoredResume(Base):
    __tablename__ = "tailored_resumes"

    id: Mapped[int] = mapped_column(primary_key=True)

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    version_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("1"),
        default=1,
    )
    parent_version_id: Mapped[int | None] = mapped_column(
        ForeignKey("tailored_resumes.id", ondelete="SET NULL"),
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'draft'"),
        default="draft",
    )
    target_role: Mapped[str | None] = mapped_column(String(150))
    content_snapshot: Mapped[dict[str, Any]] = mapped_column(
        "content",
        JSON,
        nullable=False,
    )

    created_at: Mapped[datetime] = timestamp_column()
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


# ---------------------------------------------------------------------------
# Resume artifacts
# ---------------------------------------------------------------------------

class ResumeArtifact(Base):
    __tablename__ = "resume_artifacts"

    id: Mapped[int] = mapped_column(primary_key=True)

    tailored_resume_id: Mapped[int] = mapped_column(
        ForeignKey("tailored_resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    artifact_type: Mapped[str] = mapped_column(String(20), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int | None] = mapped_column(Integer)
    compilation_log: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = timestamp_column()


# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------

class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        Index("ix_applications_status", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tailored_resume_id: Mapped[int | None] = mapped_column(
        ForeignKey("tailored_resumes.id", ondelete="SET NULL"),
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        server_default=text("'applied'"),
        default="applied",
    )
    applied_at: Mapped[datetime] = mapped_column(
        "applied_date",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    notes: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = timestamp_column()
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


# ---------------------------------------------------------------------------
# Resume validations
# ---------------------------------------------------------------------------

class ResumeValidation(Base):
    __tablename__ = "resume_validations"

    id: Mapped[int] = mapped_column(primary_key=True)

    tailored_resume_id: Mapped[int] = mapped_column(
        ForeignKey("tailored_resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    overall_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'PASS'"),
        default="PASS",
    )
    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("100"),
        default=100,
    )
    checks: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = timestamp_column()
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
