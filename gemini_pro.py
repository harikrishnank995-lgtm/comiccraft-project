from app.config import GEMINI_API_KEY, GEMINI_MODEL, DEMO_MODE

def generate_story(outline: list[dict], character_name: str, tone: str) -> list[dict]:
    """Expand the outline into short narration and dialogue for every panel."""
    if not GEMINI_API_KEY:
        if DEMO_MODE:
            return [
                {
                    **panel,
                    "caption": ["A new day begins.", "Something glimmers nearby.", "The air grows tense.", "Courage takes the lead.", "A story worth remembering."][i],
                    "narration": [
                        f"{character_name} takes a careful first step into the unknown.",
                        f"“What could this be?” {character_name} wonders, leaning closer.",
                        f"“I can do this,” {character_name} says, taking a steady breath.",
                        f"With a clever plan, {character_name} turns the problem into an opportunity.",
                        f"By sunset, {character_name} knows that kindness and courage make the best heroes."
                    ][i],
                    "dialogue": [
                        "“Adventure, here I come!”",
                        "“This must be the clue!”",
                        "“I won't give up now!”",
                        "“Let's try a different way.”",
                        "“The best treasure is what we learned.”"
                    ][i],
                }
                for i, panel in enumerate(outline)
            ]
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")
    try:
        from google import genai
        import json, re
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = f"""
Expand this comic outline into narration and dialogue for exactly five panels.
Return ONLY a JSON array. Each object must include panel_number, title,
scene_description, image_prompt, caption, narration, dialogue.
Keep narration concise (2-3 sentences), dialogue short, tone: {tone}.
Main character: {character_name}. Family-friendly. Preserve the outline's events.
Outline JSON: {json.dumps(outline, ensure_ascii=False)}
"""
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        raw = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", (response.text or "").strip(), flags=re.I)
        data = json.loads(raw)
        if not isinstance(data, list) or len(data) != 5:
            raise ValueError("Gemini did not return exactly five story panels.")
        return [{**outline[i], **data[i], "panel_number": i + 1} for i in range(5)]
    except Exception as exc:
        if DEMO_MODE:
            # Keep the app usable in demo mode if a remote response is malformed or unavailable.
            from app.services.gemini_flash import _demo_outline
            fallback = _demo_outline("adventure", character_name, "a magical world", tone, "comic book")
            return [
                {**outline[i], "caption": "A new moment in the adventure.",
                 "narration": fallback[i]["scene_description"],
                 "dialogue": f"“Let's keep going!” — {character_name}"}
                for i in range(5)
            ]
        raise RuntimeError(f"Gemini story generation failed: {exc}") from exc
