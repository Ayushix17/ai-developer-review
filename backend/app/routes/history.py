from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.models.analysis import Analysis
from app.schemas.analyze import AnalysisDetail, AnalysisListItem, FindingResponse

router = APIRouter()


@router.get("/analyses", response_model=list[AnalysisListItem])
def list_analyses(db: Session = Depends(get_db)) -> list[AnalysisListItem]:
    rows = db.query(Analysis).order_by(Analysis.created_at.desc()).all()
    return [
        AnalysisListItem(
            id=row.id,
            language=row.language,
            source_type=row.source_type,
            summary=row.summary,
            cost_usd=row.cost_usd,
            latency_ms=row.latency_ms,
            created_at=row.created_at,
        )
        for row in rows
    ]


@router.get("/analyses/{analysis_id}", response_model=AnalysisDetail)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)) -> AnalysisDetail:
    row = (
        db.query(Analysis)
        .options(selectinload(Analysis.findings))
        .filter(Analysis.id == analysis_id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return AnalysisDetail(
        analysis_id=row.id,
        language=row.language,
        source_type=row.source_type,
        input_code=row.input_code,
        context=row.context,
        created_at=row.created_at,
        summary=row.summary,
        findings=[
            FindingResponse(
                severity=finding.severity,
                title=finding.title,
                description=finding.description,
                line_number=finding.line_number,
                suggestion=finding.suggestion,
                category=finding.category,
            )
            for finding in row.findings
        ],
        tokens_used=row.tokens_used,
        latency_ms=row.latency_ms,
        cost_usd=row.cost_usd,
    )
