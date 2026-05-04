from datetime import datetime

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    code: str = Field(min_length=1)
    language: str = Field(default="python")
    source_type: str = Field(default="pasted_code")
    context: str | None = None


class FindingResponse(BaseModel):
    severity: str
    title: str
    description: str
    line_number: int | None = None
    suggestion: str | None = None
    category: str


class AnalyzeResponse(BaseModel):
    analysis_id: int
    summary: str
    findings: list[FindingResponse]
    tokens_used: int
    latency_ms: int
    cost_usd: float


class AnalysisListItem(BaseModel):
    id: int
    language: str
    source_type: str
    summary: str
    cost_usd: float
    latency_ms: int
    created_at: datetime


class AnalysisDetail(AnalyzeResponse):
    language: str
    source_type: str
    input_code: str
    context: str | None = None
    created_at: datetime


class GitHubWebhookResult(BaseModel):
    status: str
    message: str
    analysis_id: int | None = None
    github_comment_url: str | None = None
