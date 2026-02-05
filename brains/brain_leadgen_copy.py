"""
brain_leadgen_copy.py

Lead Generation Micro Copy Brain
Ultra-focused on sharp, uncomfortable, high-conversion micro copy.
No fluff. No generic hooks.
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
        Generates sharp, conversion-focused micro copy.

        input_copy: short text (5–80 words ideally)
        goal: lead_capture | click | reply | book_call
        """

        if not input_copy or len(input_copy.strip()) < 3:
            raise ValueError("Input copy too short.")

        prompt = f"""
You are a ruthless conversion-focused copy auditor.

Your job is to generate MICRO COPY that forces attention
by calling out a clear problem, risk, or missed opportunity.

This is NOT marketing copy.
This is NOT polite.
This is NOT generic.

If the output feels safe, it has failed.

STRICT RULES:
- No buzzwords
- No hype language
- No vague promises
- No "unlock", "discover", "what’s working", "double your leads"
- No inspirational tone
- No generic curiosity

Each line MUST:
- Call out a specific weakness, gap, or risk
- Imply urgency or consequence
- Make the reader feel slightly uncomfortable
- Trigger a “wait… what?” reaction

You are allowed to be direct.
You are allowed to be blunt.
You are NOT allowed to be fluffy.

DO NOT invent industries or audiences unless stated.
DO NOT explain strategy.
DO NOT justify yourself.

INPUT COPY:
---
{input_copy}
---

OUTPUT FORMAT (STRICT):

REWRITTEN MICRO COPY:
(Provide 2–3 sharp lines only)

WHY THIS WORKS (MAX 1–2 LINES):
Explain briefly why this forces attention.
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": "You write elite, uncomfortable conversion micro-copy. Be sharp."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5
        )

        return response.choices[0].message.content.strip()