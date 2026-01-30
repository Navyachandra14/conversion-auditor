"""
brain_leadgen_copy.py

Lead Generation Micro Copy Brain
Ultra-focused on short, high-conversion micro copy.
No long analysis. No strategy essays. No fluff.
"""

from openai import OpenAI
from typing import Optional


class LeadGenCopyBrain:

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenAI API key required")
        self.client = OpenAI(api_key=api_key)

    def generate(self, input_copy: str, goal: Optional[str] = "lead_capture") -> str:
        """
        Generates high-conversion micro copy for lead generation and outreach triggers.

        input_copy: short text (5–80 words ideally)
        goal: lead_capture | click | reply | book_call
        """

        if not input_copy or len(input_copy.strip()) < 3:
            raise ValueError("Input copy too short.")

        prompt = f"""
You are a top 1% direct-response copywriter specializing in micro-copy and lead generation hooks.

Your job is to REWRITE the provided copy into a higher-converting version.

STRICT RULES:
- Output must be SHORT
- No essays
- No long explanations
- No teaching tone
- No generic marketing buzzwords
- No fluff
- No UI assumptions
- Do not invent audience or industry unless clearly stated

Focus on:
- Curiosity
- Specific outcomes
- Pain awareness
- Action trigger
- Reply / click motivation

GOAL:
{goal}

INPUT COPY:
---
{input_copy}
---

OUTPUT FORMAT (STRICT):

REWRITTEN MICRO COPY:
(Provide 1–3 strong variations max)

WHY THIS WORKS (MAX 2 LINES):
(Explain briefly in plain language)
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": "You write elite conversion micro-copy. You are concise and precise."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.6
        )

        return response.choices[0].message.content.strip()
