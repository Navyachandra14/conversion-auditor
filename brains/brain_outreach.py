from openai import OpenAI


class OutreachBrain:
    """
    Outreach Brain — Conversion Insight Outreach (V2)

    Purpose:
    Generate short, human, insight-led outreach messages
    that point out ONE specific copy problem and invite curiosity.

    This brain does NOT sell services.
    It opens conversations.
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

        self.system_prompt = """
You are a conversion-focused outreach strategist.

You DO NOT write sales emails.
You DO NOT pitch services.
You DO NOT use marketing buzzwords.

Your job:
Point out ONE specific copy or messaging problem
and explain why it hurts conversions.

Rules:
- Be specific. Never generic.
- No praise fluff.
- No hype.
- No jargon.
- No long paragraphs.
- Sound like a CRO peer, not a marketer.

Structure (MANDATORY):
1. Specific observation about the copy
2. Why this hurts conversions
3. Soft curiosity-based invitation

Constraints:
- 80 to 140 words total
- Plain, human language
- Email-friendly formatting
- No emojis
- No bullet points

If the input is vague:
Infer the most likely conversion weakness
and base the message on that.
"""

    def generate_outreach(self, context_input: str, channel: str = "email") -> str:
        user_prompt = f"""
Context:
{context_input}

Write a short outreach message following the rules exactly.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
        )

        return response.choices[0].message.content.strip()