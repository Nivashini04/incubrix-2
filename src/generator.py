
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"

PLATFORMS = ["LinkedIn", "Instagram", "YouTube Shorts"]


def generate_assets(source_text, platforms=None):

    if not source_text.strip():
        raise ValueError("Please provide source content.")

    if platforms is None:
        platforms = PLATFORMS

    prompt = f"""
You are a professional content strategist.

Extract exactly 10 distinct content ideas from the source.
Create one useful hook, caption, hashtags and CTA for each.

Rules:
- Use only information supported by the source.
- Do not invent statistics or product features.
- Make the ideas genuinely different.
- Return valid JSON only.

Format:
{{
 "assets": [
  {{
   "hook": "Hook",
   "caption": "Core caption",
   "hashtags": ["Content", "Marketing"],
   "call_to_action": "CTA",
   "source_idea": "Main source idea"
  }}
 ]
}}

SOURCE:
{source_text[:5000]}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "options": {
                "temperature": 0.5,
                "num_predict": 1200,
                "num_ctx": 2048
            }
        },
        timeout=600
    )

    response.raise_for_status()

    data = json.loads(response.json()["response"])
    base_assets = data.get("assets", [])[:10]

    if not base_assets:
        raise ValueError("The AI did not return any content ideas.")

    all_assets = []

    for index, item in enumerate(base_assets, start=1):

        hook = item.get("hook", "")
        caption = item.get("caption", "")
        idea = item.get("source_idea", "")
        hashtags = item.get("hashtags", [])
        cta = item.get("call_to_action", "")

        for platform in platforms:

            if platform == "LinkedIn":
                adapted_hook = hook
                adapted_caption = (
                    f"{hook}\n\n{caption}\n\n"
                    "A practical takeaway for professionals "
                    "and content creators."
                )
                adapted_cta = cta

            elif platform == "Instagram":
                adapted_hook = f"✨ {hook}"
                adapted_caption = (
                    f"{hook} 👇\n\n{caption}\n\n"
                    "Save this post for later!"
                )
                adapted_cta = "Save and share this with another creator!"

            else:
                adapted_hook = f"SHORTS HOOK: {hook}"
                adapted_caption = (
                    f"HOOK: {hook}\n\n"
                    f"MAIN MESSAGE: {caption}\n\n"
                    "ENDING: Share your thoughts below!"
                )
                adapted_cta = "Follow for more content tips!"

            all_assets.append({
                "platform": platform,
                "hook": adapted_hook,
                "caption": adapted_caption,
                "hashtags": hashtags,
                "call_to_action": adapted_cta,
                "source_idea": idea,
                "content_type": (
                    "Professional Post" if platform == "LinkedIn"
                    else "Social Post" if platform == "Instagram"
                    else "Short Video Script"
                ),
                "generation_method": "AI-assisted platform adaptation",
                "source_asset": index
            })

    return all_assets
