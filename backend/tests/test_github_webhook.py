import sys

from fastapi.testclient import TestClient


def _make_client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path.as_posix()}")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GITHUB_WEBHOOK_SECRET", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    for name in list(sys.modules):
        if name == "app" or name.startswith("app."):
            sys.modules.pop(name)

    from app.main import app

    return TestClient(app)


def test_github_webhook_processes_pull_request(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)

    from app.services.github import PullRequestFile

    monkeypatch.setattr(
        "app.services.github.fetch_pull_request_files",
        lambda repo_full_name, pr_number, token=None: [
            PullRequestFile(
                filename="main.py",
                raw_url="https://example.com/main.py",
                patch="@@ -1 +1 @@",
                status="modified",
            )
        ],
    )
    monkeypatch.setattr(
        "app.services.github.fetch_raw_file_contents",
        lambda raw_url, token=None: "import os\nprint('debug')",
    )
    monkeypatch.setattr(
        "app.services.github.review_code_with_llm",
        lambda code, language, context: {
            "findings": [
                {
                    "severity": "warn",
                    "title": "LLM finding",
                    "description": "Synthetic finding",
                    "line_number": 2,
                    "suggestion": "Use logging instead.",
                    "category": "llm",
                }
            ],
            "tokens_used": 12,
            "cost_usd": 0.000012,
        },
    )
    monkeypatch.setattr(
        "app.services.github.post_pull_request_comment",
        lambda repo_full_name, pr_number, body, token=None: "https://github.com/example/comment/1",
    )

    response = client.post(
        "/webhook/github",
        headers={"X-GitHub-Event": "pull_request"},
        json={
            "action": "opened",
            "number": 7,
            "repository": {"full_name": "owner/repo"},
            "pull_request": {
                "number": 7,
                "title": "Add feature",
                "body": "PR body",
                "head": {"sha": "abc123"},
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "processed"
    assert body["analysis_id"] > 0
    assert body["github_comment_url"] == "https://github.com/example/comment/1"


def test_github_webhook_ignores_non_pr_events(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)

    response = client.post(
        "/webhook/github",
        headers={"X-GitHub-Event": "issues"},
        json={"action": "opened"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ignored"
