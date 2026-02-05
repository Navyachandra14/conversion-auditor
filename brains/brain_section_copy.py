"""
brain_section_copy.py

Section Copy Auditor & Rewriter (Hybrid Mode)
Focused on improving a specific section of copy for conversions.
No UI assumptions. No outreach. Rewrite is mandatory.
"""

from openai import OpenAI


class SectionCopyBrain:

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenAI API key required")
        self.client = OpenAI(api_key=api_key)

    def audit_and_rewrite(self, section_copy: str) -> str:
        if not section_copy or len(section_copy.strip()) < 20:
            raise ValueError("Section copy too short to audit meaningfully.")

        prompt = f"""
You are a top 1% conversion copywriter and ruthless editor.

Your task is to audit and rewrite the following COPY SECTION
to make inaction feel costly and action feel obvious.

IMPORTANT RULES:
- Work ONLY with the provided text
- Do NOT assume layout, visuals, or page structure
- Do NOT invent audience, industry, or use cases
- Do NOT use generic marketing language
- Avoid buzzwords and vague promises
- Rewrite is MANDATORY

Your mindset:
- If the copy is vague, expose the vagueness
- If the benefit is implied, make it explicit
- If the CTA is weak, sharpen it
- If the value is unclear, force clarity

SECTION COPY:
---
{section_copy}
---

OUTPUT FORMAT (STRICT):

WHAT’S HURTING CONVERSIONS:
- List concrete, specific problems in the copy
- No generic advice

WHY THIS MATTERS:
- Explain how these issues reduce clarity, trust, or action

REWRITTEN SECTION (HIGH-CONVERSION):
- Provide a complete rewritten version
- Make outcomes explicit
- Make the value obvious
- Make the next step clear

WHAT’S MISSING / CAN BE IMPROVED:
- Suggest only additions relevant to THIS section
- Prioritize proof, specificity, and CTA strength
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": "You rewrite copy to increase conversions. You are clear, direct, and practical."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4
        )

        return response.choices[0].message.content.strip()
