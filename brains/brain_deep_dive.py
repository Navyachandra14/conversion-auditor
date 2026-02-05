"""
brain_deep_dive.py

Deep Conversion Audit Brain
Strategic conversion diagnosis for full pages or long sections.
Focus: revenue leaks, messaging gaps, trust issues, priority fixes.
"""

from openai import OpenAI


class DeepDiveBrain:

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenAI API key required")
        self.client = OpenAI(api_key=api_key)

    def deep_audit(self, full_copy: str) -> str:

        if not full_copy or len(full_copy.strip()) < 120:
            raise ValueError("Deep audit requires longer copy input.")

        prompt = f"""
ROLE:
You are a senior conversion strategist auditing a landing page.

PRIMARY OBJECTIVE:
Diagnose why visitors hesitate, lose confidence, or fail to act.

IMPORTANT RULES:
- Work ONLY with the provided copy
- Do NOT assume design, UI, or layout
- Do NOT rewrite the page
- Focus on diagnosis, not solutions
- Avoid generic CRO advice
- Be clear, specific, and practical

FOCUS ON IDENTIFYING:
- Where clarity breaks down
- Where trust is weakened
- Where the offer feels vague or risky
- Where motivation to act is missing

COPY TO AUDIT:
---
{full_copy}
---

OUTPUT FORMAT (STRICT):

PRIMARY CONVERSION RISKS:
(List the 3–5 most important reasons conversions may be lost)

MESSAGING GAPS:
(What a serious buyer still does not understand)

TRUST / PROOF WEAKNESSES:
(Why a buyer might hesitate to believe or commit)

OFFER CLARITY ISSUES:
(Where the offer feels unclear, risky, or incomplete)

PRIORITY FIX ORDER:
(What should be fixed first, second, third — based on impact)
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": "You are a calm, senior conversion strategist who diagnoses revenue problems clearly."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4
        )

        return response.choices[0].message.content.strip()
