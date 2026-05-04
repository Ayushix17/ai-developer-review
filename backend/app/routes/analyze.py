from time import perf_counter

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse, FindingResponse
from app.services.llm import review_code_with_llm
from app.services.persistence import create_analysis
from app.services.static_analysis import run_static_analysis

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_code(payload: AnalyzeRequest, db: Session = Depends(get_db)) -> AnalyzeResponse:
    start = perf_counter()
    static_findings = run_static_analysis(payload.code, payload.language)
    llm_result = review_code_with_llm(payload.code, payload.language, payload.context)
    latency_ms = int((perf_counter() - start) * 1000)

    findings = static_findings + llm_result["findings"]
    summary = f"Found {len(findings)} issue(s): {len(static_findings)} static, {len(llm_result['findings'])} AI."
    analysis = create_analysis(
        db=db,
        source_type=payload.source_type,
        language=payload.language,
        input_code=payload.code,
        context=payload.context,
        summary=summary,
        tokens_used=llm_result["tokens_used"],
        latency_ms=latency_ms,
        cost_usd=llm_result["cost_usd"],
        findings=findings,
    )

    return AnalyzeResponse(
        analysis_id=analysis.id,
        summary=analysis.summary,
        findings=[FindingResponse(**finding) for finding in findings],
        tokens_used=analysis.tokens_used,
        latency_ms=analysis.latency_ms,
        cost_usd=analysis.cost_usd,
    )
