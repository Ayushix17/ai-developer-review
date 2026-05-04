from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import requests

from app.db import get_db
from app.schemas.analyze import GitHubWebhookResult
from app.services.github import analyze_pull_request, verify_github_signature

router = APIRouter()


@router.post("/webhook/github", response_model=GitHubWebhookResult)
async def github_webhook(request: Request, db: Session = Depends(get_db)) -> GitHubWebhookResult:
    body = await request.body()
    try:
        verify_github_signature(body, request.headers.get("X-Hub-Signature-256"))
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc))

    payload = await request.json()
    if request.headers.get("X-GitHub-Event") != "pull_request":
        return GitHubWebhookResult(status="ignored", message="Event is not pull_request")

    action = payload.get("action")
    if action not in {"opened", "reopened", "synchronize", "edited", "ready_for_review"}:
        return GitHubWebhookResult(status="ignored", message=f"Action `{action}` is not reviewable")

    repository = payload.get("repository") or {}
    pull_request = payload.get("pull_request") or {}
    repo_full_name = repository.get("full_name")
    pr_number = payload.get("number") or pull_request.get("number")
    pr_title = pull_request.get("title") or ""
    pr_body = pull_request.get("body")
    head_sha = ((pull_request.get("head") or {}).get("sha"))

    if not repo_full_name or not pr_number:
        raise HTTPException(status_code=400, detail="Missing repository or pull request number")

    try:
        result = analyze_pull_request(
            db=db,
            repo_full_name=repo_full_name,
            pr_number=int(pr_number),
            pr_title=pr_title,
            pr_body=pr_body,
            head_sha=head_sha,
        )
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"GitHub request failed: {exc}")

    return GitHubWebhookResult(
        status="processed",
        message="Pull request analyzed",
        analysis_id=result["analysis_id"],
        github_comment_url=result["github_comment_url"],
    )
