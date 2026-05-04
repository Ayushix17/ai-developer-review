import json

from openai import OpenAI

from app.config import get_settings


def review_code_with_llm(code: str, language: str, context: str | None) -> dict:
    settings = get_settings()
    if not settings.openai_api_key:
        return {"findings": [], "tokens_used": 0, "cost_usd": 0.0}

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = f"""
Review the following {language} code.
Return JSON with a top-level key `findings`.
Each finding must include: severity, title, description, line_number, suggestion, category.
Only include concrete issues. Use category `llm`.
Context:
{context or "None"}

Code:
{code}
""".strip()

    response = client.responses.create(
        model=settings.openai_model,
        input=[
            {
                "role": "system",
                "content": "You are a precise code reviewer. Return valid JSON only.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    text = response.output_text.strip()
    parsed = json.loads(text) if text else {"findings": []}
    findings = parsed.get("findings", [])
    for finding in findings:
        finding["category"] = "llm"

    usage = getattr(response, "usage", None)
    tokens_used = getattr(usage, "total_tokens", 0) if usage else 0
    cost_usd = round(tokens_used * 0.000001, 6)
    return {"findings": findings, "tokens_used": tokens_used, "cost_usd": cost_usd}
