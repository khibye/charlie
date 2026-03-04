import json
from typing import Any

DEFAULT_ANALYSIS_PROMPT = (
    "Extract and structure analytical insights from the provided data in relation to the user context. "
    "Identify thematic patterns, indirect signals, emerging trends, anomalies, and notable entities. "
    "Be conservative and evidence-based. Do not invent facts. "
    "When uncertain, reflect that uncertainty explicitly. "
    "Prioritize signal over verbosity and avoid narrative storytelling."
)

DEFAULT_ARTICLE_PROMPT = (
    "Write a concise, high-level analytical article based on the structured insights provided. "
    "Focus on thematic patterns, indirect signals, trends, and strategic implications. "
    "Include insights and well-reasoned conclusions. "
    "Mention important names, places, files, and dates when they materially support the analysis. "
    "Do not invent information beyond the provided insights."
)

DEFAULT_ANALYSIS_SYSTEM_PROMPT = (
    "You are an expert analyst. Your job is to extract themes, indirect signals, and patterns "
    "from batches of heterogeneous data. Be conservative: do not invent facts. "
    "When unsure, state uncertainty."
)

DEFAULT_ARTICLE_SYSTEM_PROMPT = (
    "You are a senior strategic analyst and writer. Your role is to synthesize structured analytical insights "
    "into a coherent, high-level article. Focus on patterns, implications, and well-supported conclusions. "
    "Do not invent facts beyond the provided insights. If signals are weak or conflicting, explicitly state the uncertainty. "
    "Prioritize clarity, synthesis, and strategic meaning over listing details."
)


def get_summarize_batch_user_prompt(user_context: str, indexed_docs: list[dict[str, Any]]) -> str:
    return (
        "USER CONTEXT (IMPORTANT):\n"
        f"{user_context}\n\n"
        "TASK PROMPT:\n"
        f"{DEFAULT_ANALYSIS_PROMPT}\n\n"
        "DATA (JSON, indexed):\n"
        f"{json.dumps(indexed_docs, ensure_ascii=False)}\n\n"
        "Return MUST ONLY valid JSON (avoid markdown, avoid trailing commas -- at all costs!"
        "The result should be and MUST be ONLY a valid JSON object) with this EXACT (MUST be the same) schema (avoid any additional data):\n"
        "{\n"
        '  "themes": [ {"name": str, "summary": str, "confidence": 0..1} ],\n'
        '  "indirect_signals": [ {"signal": str, "why_it_matters": str, "confidence": 0..1} ],\n'
        '  "notable_entities": {"people": [str], "companies": [str], "places": [str], "files": [str]},\n'
        '  "notable_dates": [ {"date": str, "why": str} ],\n'
        '  "anomalies": [ {"description": str, "confidence": 0..1} ],\n'
        '  "open_questions": [str],\n'
        '  "evidence": [ {"idx": int, "notes": str} ]\n'
        "}\n\n"
        "Rules:\n"
        "- Use evidence.idx values that refer to the provided DATA indices.\n"
        "- Keep evidence.notes short.\n"
        "- Do not include any keys outside the schema.\n"
    )


def get_synthesize_article_user_prompt(user_context: str, summaries_json: str) -> str:
    return (
        "USER CONTEXT (IMPORTANT):\n"
        f"{user_context}\n\n"
        "STRUCTURED INSIGHTS (JSON):\n"
        f"{summaries_json}\n\n"
        "TASK:\n"
        f"{DEFAULT_ARTICLE_PROMPT}\n\n"
        "Writing rules:\n"
        "- Produce a single article as plain text (no JSON).\n"
        "- Be conservative: do not invent facts not supported by the insights.\n"
        "- If evidence is weak or conflicting, say so explicitly.\n"
        "- Prefer synthesis over listing; avoid item-by-item mapping.\n"
        "- Mention important names/places/files/dates only when materially relevant.\n"
    )
