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
You are a senior conversion strategist who audits high-revenue landing pages.

PRIMARY OBJECTIVE:
Identify where conversions are being lost and what is missing that would increase buyer confidence and action.

IMPORTANT RULES:
- Work ONLY with provided copy
- Do NOT assume design, UI, or layout
- Do NOT rewrite full sections unless absolutely necessary
- Focus on diagnosis, not rewriting
- Be concise but insightful
- No generic CRO advice
- No marketing framework lectures

FOCUS AREAS:
1. Revenue leaks
2. Messaging gaps
3. Trust and proof weaknesses
4. Offer clarity problems
5. Buyer hesitation triggers
6. Missing persuasion elements

COPY TO AUDIT:
---
{full_copy}
---

OUTPUT FORMAT:

PRIMARY CONVERSION RISKS:
(Top 3–5 issues causing lost conversions)

MESSAGING GAPS:
(What buyers still don’t understand or don’t see)

TRUST / PROOF WEAKNESSES:
(Why visitors might hesitate to believe or act)

OFFER CLARITY ISSUES:
(Where offer may confuse or slow decisions)

PRIORITY FIX ORDER:
(What to fix first → highest conversion impact)
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
