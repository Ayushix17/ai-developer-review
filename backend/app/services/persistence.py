from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.finding import Finding


def create_analysis(
    db: Session,
    source_type: str,
    language: str,
    input_code: str,
    context: str | None,
    summary: str,
    tokens_used: int,
    latency_ms: int,
    cost_usd: float,
    findings: list[dict],
    github_repo_full_name: str | None = None,
    github_pr_number: int | None = None,
    github_commit_sha: str | None = None,
    github_comment_url: str | None = None,
) -> Analysis:
    analysis = Analysis(
        source_type=source_type,
        github_repo_full_name=github_repo_full_name,
        github_pr_number=github_pr_number,
        github_commit_sha=github_commit_sha,
        github_comment_url=github_comment_url,
        language=language,
        input_code=input_code,
        context=context,
        summary=summary,
        tokens_used=tokens_used,
        latency_ms=latency_ms,
        cost_usd=cost_usd,
    )
    db.add(analysis)
    db.flush()

    for item in findings:
        db.add(
            Finding(
                analysis_id=analysis.id,
                severity=item["severity"],
                title=item["title"],
                description=item["description"],
                line_number=item.get("line_number"),
                suggestion=item.get("suggestion"),
                category=item["category"],
            )
        )

    db.commit()
    db.refresh(analysis)
    return analysis
