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

Your task is to audit and rewrite the following COPY SECTION to improve conversions.

IMPORTANT RULES:
- Work ONLY with the provided text
- Do NOT assume layout, design, visuals, or page structure
- Do NOT invent audience, industry, or use cases not stated
- Avoid generic marketing language and buzzwords
- Be specific, concrete, and buyer-focused
- Rewrite is MANDATORY

If the section is short, keep analysis concise.
If the section is longer, stay focused on clarity and persuasion.

SECTION COPY:
---
{section_copy}
---

Your output MUST follow this format exactly:

WHAT’S HURTING CONVERSIONS:
- List specific issues in the copy (no vague advice)

WHY THIS MATTERS:
- Briefly explain how these issues reduce clarity, trust, or action

REWRITTEN SECTION (HIGH-CONVERSION):
- Provide a complete rewritten version of this section
- Make it clearer, more persuasive, and more action-oriented

WHAT’S MISSING / CAN BE IMPROVED:
- Suggest only elements relevant to THIS section (proof, clarity, CTA strength, specificity)
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
