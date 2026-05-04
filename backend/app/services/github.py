from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

from app.config import get_settings
from app.services.llm import review_code_with_llm
from app.services.persistence import create_analysis
from app.services.static_analysis import run_static_analysis


SUPPORTED_LANGUAGES_BY_EXTENSION = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".go": "go",
    ".rb": "ruby",
    ".php": "php",
    ".cs": "csharp",
    ".c": "c",
    ".cpp": "cpp",
    ".rs": "rust",
}


@dataclass(slots=True)
class PullRequestFile:
    filename: str
    raw_url: str | None
    patch: str | None
    status: str


def verify_github_signature(payload: bytes, signature: str | None) -> None:
    settings = get_settings()
    secret = settings.github_webhook_secret
    if not secret:
        return

    if not signature:
        raise ValueError("Missing X-Hub-Signature-256 header")

    expected = "sha256=" + hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise ValueError("Invalid GitHub webhook signature")


def github_api_headers(token: str | None = None) -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ai-developer-review",
    }
    auth_token = token or get_settings().github_token
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    return headers


def infer_language(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    return SUPPORTED_LANGUAGES_BY_EXTENSION.get(suffix, "text")


def fetch_pull_request_files(
    repo_full_name: str,
    pr_number: int,
    token: str | None = None,
) -> list[PullRequestFile]:
    owner, repo = repo_full_name.split("/", 1)
    page = 1
    collected: list[PullRequestFile] = []

    while True:
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files",
            headers=github_api_headers(token),
            params={"per_page": 100, "page": page},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        if not data:
            break

        for item in data:
            collected.append(
                PullRequestFile(
                    filename=item["filename"],
                    raw_url=item.get("raw_url"),
                    patch=item.get("patch"),
                    status=item.get("status", "modified"),
                )
            )

        if len(data) < 100:
            break
        page += 1

    return collected


def fetch_raw_file_contents(raw_url: str, token: str | None = None) -> str:
    response = requests.get(raw_url, headers=github_api_headers(token), timeout=30)
    response.raise_for_status()
    return response.text


def post_pull_request_comment(
    repo_full_name: str,
    pr_number: int,
    body: str,
    token: str | None = None,
) -> str | None:
    owner, repo = repo_full_name.split("/", 1)
    response = requests.post(
        f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments",
        headers=github_api_headers(token),
        json={"body": body},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("html_url")


def build_summary_comment(
    repo_full_name: str,
    pr_number: int,
    pr_title: str,
    summary: str,
    findings: list[dict[str, Any]],
) -> str:
    lines = [
        f"AI review for `{repo_full_name}#{pr_number}`",
        "",
        f"PR title: {pr_title}",
        "",
        summary,
    ]

    if findings:
        lines.append("")
        lines.append("Top findings:")
        for finding in findings[:10]:
            file_name = finding.get("file_path") or finding.get("file_name") or "unknown file"
            line_number = finding.get("line_number")
            location = f"{file_name}:{line_number}" if line_number else file_name
            lines.append(f"- `{finding['severity']}` {finding['title']} ({location})")
            description = finding.get("description")
            if description:
                lines.append(f"  - {description}")
            suggestion = finding.get("suggestion")
            if suggestion:
                lines.append(f"  - Suggestion: {suggestion}")
    else:
        lines.append("")
        lines.append("No issues were found.")

    return "\n".join(lines)


def analyze_pull_request(
    db,
    repo_full_name: str,
    pr_number: int,
    pr_title: str,
    pr_body: str | None,
    head_sha: str | None,
    token: str | None = None,
) -> dict[str, Any]:
    files = fetch_pull_request_files(repo_full_name, pr_number, token=token)
    reviewed_chunks: list[str] = []
    findings: list[dict[str, Any]] = []
    total_tokens = 0
    total_cost = 0.0

    for file_info in files:
        if file_info.status == "removed":
            continue
        if not file_info.raw_url:
            continue

        language = infer_language(file_info.filename)
        if language == "text":
            continue

        content = fetch_raw_file_contents(file_info.raw_url, token=token)
        reviewed_chunks.append(f"### {file_info.filename}\n\n{content}")

        static_findings = run_static_analysis(content, language)
        for item in static_findings:
            item["file_path"] = file_info.filename
            item["file_name"] = file_info.filename
        findings.extend(static_findings)

        llm_result = review_code_with_llm(content, language, pr_body)
        for item in llm_result["findings"]:
            item["file_path"] = file_info.filename
            item["file_name"] = file_info.filename
        findings.extend(llm_result["findings"])
        total_tokens += llm_result["tokens_used"]
        total_cost += llm_result["cost_usd"]

    if not reviewed_chunks:
        reviewed_chunks.append("No supported files were available for review.")

    summary = (
        f"Found {len(findings)} issue(s) across {len(reviewed_chunks)} file(s): "
        f"{len([f for f in findings if f.get('category') == 'static'])} static, "
        f"{len([f for f in findings if f.get('category') == 'llm'])} AI."
    )
    context = "\n".join(
        [
            f"Repository: {repo_full_name}",
            f"PR: #{pr_number}",
            f"Title: {pr_title}",
            f"Commit: {head_sha or 'unknown'}",
            "",
            pr_body or "",
        ]
    ).strip()
    input_code = "\n\n".join(reviewed_chunks)

    analysis = create_analysis(
        db=db,
        source_type="github_pr",
        github_repo_full_name=repo_full_name,
        github_pr_number=pr_number,
        github_commit_sha=head_sha,
        github_comment_url=None,
        language="multi",
        input_code=input_code,
        context=context,
        summary=summary,
        tokens_used=total_tokens,
        latency_ms=0,
        cost_usd=total_cost,
        findings=findings,
    )

    comment_body = build_summary_comment(repo_full_name, pr_number, pr_title, summary, findings)
    comment_url = None
    try:
        comment_url = post_pull_request_comment(repo_full_name, pr_number, comment_body, token=token)
    except requests.RequestException:
        comment_url = None

    if comment_url:
        analysis.github_comment_url = comment_url
        db.commit()

    return {
        "analysis_id": analysis.id,
        "summary": summary,
        "findings": findings,
        "tokens_used": total_tokens,
        "cost_usd": total_cost,
        "github_comment_url": comment_url,
    }
