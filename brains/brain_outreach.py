from openai import OpenAI


class OutreachBrain:

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenAI API key required")
        self.client = OpenAI(api_key=api_key)

    def generate_outreach(self, context_input: str, channel: str = "email") -> str:

        if not context_input or len(context_input.strip()) < 10:
            raise ValueError("Context input too short.")

        prompt = f"""
ROLE:
You are an elite B2B outreach copywriter who writes short, human, observation-driven outreach messages.

PRIMARY OBJECTIVE:
Write an outreach message that proves you reviewed their copy by referencing ONE specific copy pattern from the context.

MANDATORY LANGUAGE STRUCTURE:
You MUST use one of these linguistic patterns:
- talks about X but not Y
- explains A but does not show B
- mentions feature but not outcome
- describes process but not result
- says what you do but not what customer gets

BANNED WORDS AND PHRASES:
Do NOT use:
broad
vague
open-ended
unclear
improve messaging
could be stronger
needs improvement
optimize
enhance
elevate

CONTEXT USAGE RULE:
You MUST reference a real idea from the provided context.
Do NOT invent problems.
Do NOT generalize.

TONE RULES:
- Human
- Natural
- Helpful
- Calm confidence
- No marketing lecture
- No audit explanation
- No selling pressure

LENGTH RULES:
Email body must be 60–120 words maximum.
No long paragraphs.

CHANNEL:
{channel}

CONTEXT:
{context_input}

OUTPUT CONTRACT:

IF EMAIL:
Subject: (max 8 words, natural)
Body:
- Short intro
- One specific observation using required pattern
- Soft offer or curiosity CTA
- Close naturally

IF LINKEDIN OR DM:
Message:
- One specific observation
- One curiosity question
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": "You produce precise outreach messages that feel personally observed and credible."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5
        )

        return response.choices[0].message.content.strip()
