
"""Add skill catalog and evidence tables for E01."""

from alembic import op
import sqlalchemy as sa


revision = "e01_add_skill_evidence_tables"
down_revision = "009_create_application_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("category", sa.String(80), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.create_table(
        "match_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "match_analysis_id",
            sa.Integer(),
            sa.ForeignKey("match_analyses.id"),
            nullable=False,
        ),
        sa.Column(
            "job_requirement_id",
            sa.Integer(),
            sa.ForeignKey("job_requirements.id"),
            nullable=False,
        ),
        sa.Column("match_status", sa.String(20), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("evidence_refs", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint(
            "match_analysis_id",
            "job_requirement_id",
            name="uq_match_results_analysis_requirement",
        ),
        sa.CheckConstraint(
            "match_status IN ('matched', 'weak', 'missing', 'unsupported')",
            name="ck_match_results_match_status",
        ),
    )
    op.create_index(
        "ix_match_results_match_analysis_id",
        "match_results",
        ["match_analysis_id"],
    )
    op.create_index(
        "ix_match_results_job_requirement_id",
        "match_results",
        ["job_requirement_id"],
    )

    op.create_table(
        "project_skill_evidence",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id"),
            nullable=False,
        ),
        sa.Column(
            "skill_id",
            sa.Integer(),
            sa.ForeignKey("skills.id"),
            nullable=False,
        ),
        sa.Column("evidence_text", sa.Text(), nullable=True),
        sa.Column("evidence_type", sa.String(50), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint(
            "project_id",
            "skill_id",
            name="uq_project_skill_evidence_project_skill",
        ),
    )
    op.create_index(
        "ix_project_skill_evidence_project_id",
        "project_skill_evidence",
        ["project_id"],
    )
    op.create_index(
        "ix_project_skill_evidence_skill_id",
        "project_skill_evidence",
        ["skill_id"],
    )


def downgrade() -> None:
    op.drop_table("project_skill_evidence")
    op.drop_table("match_results")
    op.drop_table("skills")
