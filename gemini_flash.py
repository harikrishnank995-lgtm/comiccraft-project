import json
import re
from typing import Any
from app.config import GEMINI_API_KEY, GEMINI_MODEL, DEMO_MODE

def _demo_outline(prompt: str, character_name: str, setting: str, tone: str, art_style: str) -> list[dict[str, Any]]:
    titles = ["The Beginning", "A Strange Discovery", "The Challenge", "A Brave Choice", "A New Legend"]
    beats = [
        f"{character_name} arrives in {setting}, ready for an unexpected adventure.",
        f"{character_name} discovers a mysterious clue that changes everything.",
        f"A surprising obstacle tests {character_name}'s courage and cleverness.",
        f"{character_name} makes a thoughtful choice and faces the challenge.",
        f"The adventure ends with a hopeful discovery and a lesson learned.",
    ]
    return [
        {
            "panel_number": i + 1,
            "title": titles[i],
            "scene_description": beats[i],
            "image_prompt": (
                f"{art_style} illustration, {setting}, featuring {character_name}; "
                f"{beats[i]} Tone: {tone}. Consistent character design, expressive composition, "
                "clear storytelling, no text, no lettering, family-friendly."
            ),
        }
        for i in range(5)
    ]

def generate_outline(prompt: str, character_name: str, setting: str, tone: str, art_style: str) -> list[dict[str, Any]]:
    """Generate a validated five-panel outline. Falls back to a deterministic demo outline when configured."""
    if not GEMINI_API_KEY:
        if DEMO_MODE:
            return _demo_outline(prompt, character_name, setting, tone, art_style)
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        instruction = f"""
Create exactly five connected comic panels from this user idea.
Return ONLY valid JSON: an array of five objects with keys:
panel_number (integer), title (short string), scene_description (1-2 sentences),
image_prompt (detailed visual prompt, no lettering in image).
Keep the same character appearance across all panels. Keep it family-friendly.
Story idea: {prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}
"""
        response = client.models.generate_content(model=GEMINI_MODEL, contents=instruction)
        raw = response.text or ""
        raw = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", raw.strip(), flags=re.I)
        data = json.loads(raw)
        if not isinstance(data, list) or len(data) != 5:
            raise ValueError("Gemini did not return exactly five panels.")
        result = []
        for index, item in enumerate(data):
            result.append({
                "panel_number": index + 1,
                "title": str(item.get("title", f"Panel {index+1}"))[:100],
                "scene_description": str(item.get("scene_description", ""))[:1200],
                "image_prompt": str(item.get("image_prompt", ""))[:1500],
            })
        return result
    except Exception as exc:
        if DEMO_MODE:
            return _demo_outline(prompt, character_name, setting, tone, art_style)
        raise RuntimeError(f"Gemini outline generation failed: {exc}") from exc
