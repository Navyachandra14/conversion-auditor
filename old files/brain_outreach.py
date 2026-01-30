"""
brain_outreach.py - The Cold Outreach Sniper (On-Demand Version)
Top 1% Business Development Rep - Generates platform-specific hooks on demand.
"""

from openai import OpenAI
import json
from typing import Dict, Optional

class OutreachSniper:
    """
    The Outreach Brain - Generates single, high-impact messages for specific platforms.
    """
    
    def __init__(self, api_key: str):
        """Initialize with OpenAI API key"""
        if not api_key:
            raise ValueError("OpenAI API key required")
        self.client = OpenAI(api_key=api_key)
    
    def generate_hook(self, platform: str, copy_audit: Dict) -> Dict:
        """
        Generate a single, high-converting message for a specific platform.
        
        Args:
            platform: "email", "linkedin", or "facebook"
            copy_audit: The results from brain_copy.py
            
        Returns:
            JSON with 'subject' (for email) and 'body'
        """
        
        # 1. Extract Intelligence from the Copy Audit
        # We need the "Crime" (Problem) and the "Rewrite" (Solution)
        primary_crime = copy_audit.get('primary_crime', 'Conversion Friction')
        friction_score = copy_audit.get('friction_score', 0)
        
        # Try to get the headline rewrite, fallback to a generic fix if missing
        headline_rewrite = copy_audit.get('headline_audit', {}).get('a_list_rewrite', 'Clearer Value Proposition')
        
        # 2. Define Platform-Specific Personas and Context
        if platform.lower() == "email":
            context_instruction = """
            **PLATFORM: COLD EMAIL**
            - STRUCTURE: Subject Line + Body.
            - TONE: Professional but "Internal" (like a colleague sent it).
            - CONSTRAINT: Subject line must be lowercase and boring (e.g. "question about [company]").
            - LENGTH: Under 120 words.
            """
        elif platform.lower() == "linkedin":
            context_instruction = """
            **PLATFORM: LINKEDIN DM**
            - STRUCTURE: Body only (No Subject).
            - TONE: Casual, "Text Message" style.
            - CONSTRAINT: Use lowercase. No formal salutations ("Dear Sir").
            - LENGTH: Under 60 words.
            """
        elif platform.lower() == "facebook":
            context_instruction = """
            **PLATFORM: FACEBOOK/SOCIAL DM**
            - STRUCTURE: Body only.
            - TONE: Very casual, direct, peer-to-peer.
            - CONSTRAINT: Get straight to the point. No fluff.
            - LENGTH: Under 50 words.
            """
        else:
            # Fallback
            context_instruction = "**PLATFORM: GENERAL MESSAGE** - Keep it brief and professional."

        # 3. The Prompt
        prompt = f"""You are a Top 1% Business Development Sniper. You do not write "marketing campaigns." You write **one-to-one messages** that get replies.

You are writing a cold outreach message to a Founder based on a forensic audit of their website.

**THE INTELLIGENCE:**
- Their Primary Mistake: {primary_crime}
- Friction Score: {friction_score}/100 (High friction = bad)
- The Fix (Your Rewrite): "{headline_rewrite}"

{context_instruction}

**YOUR STRATEGY (The "Value-First" Approach):**
1. **The Hook:** Call out the specific mistake ({primary_crime}) immediately.
2. **The Cost:** Briefly imply why this mistake loses them money.
3. **The Gift:** Give them the "Fix" (The Rewrite) for free right now.
4. **The Ask:** Soft ask ("Worth fixing?", "Mind if I send the full audit?").
5. **ANTI-SPAM RULE:** NEVER use "Hope you are well", "I wanted to reach out", or "Transform your business".

**OUTPUT FORMAT:**
Respond ONLY with valid JSON.
{{
  "subject": "...",  (Only for Email, otherwise leave empty string "")
  "body": "..."
}}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview", # Use smart model for nuance
                messages=[
                    {"role": "system", "content": "You are a cold outreach expert. Respond ONLY in JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {
                "subject": "Error",
                "body": f"Could not generate message: {str(e)}"
            }