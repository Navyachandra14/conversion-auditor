"""
brain_copy.py - The Forensic Copy Auditor (Ruthless Edition)
A-List Direct Response Copywriter (Eugene Schwartz/Gary Halbert level)
"""

from openai import OpenAI
import os
import json
from typing import Dict, Optional
from utils import parse_json_safely, extract_hero_components

class ForensicCopyAuditor:
    
    def __init__(self, api_key: str):
        if not api_key: raise ValueError("OpenAI API key required")
        self.client = OpenAI(api_key=api_key)
    
    def audit(self, hero_text: str, extracted_components: Optional[Dict] = None) -> Dict:
        if not extracted_components:
            extracted_components = extract_hero_components(hero_text)
        
        prompt = f"""You are a Direct Response Copywriting Auditor (Eugene Schwartz level).
You do not write "marketing copy." You write **SALES ARGUMENTS**.

**MANDATE:**
Audit the Hero Section below. Detect "Conversion Crimes." Rewrite them.

**3 LOGIC GATES:**
1. **We-Centric:** Flag "We", "Our", "I". (Crime: Seller-focused).
2. **Passive:** Flag "is designed to", "helps to". (Crime: Weak verbs).
3. **Jargon:** Flag "Synergy", "Solution", "Transform". (Crime: Noise).

**⛔ BANNED WORDS (DO NOT USE IN REWRITES):**
- "Boost", "Elevate", "Unlock", "Unleash", "Master", "Impact", "Empower", "Streamline"
Use concrete numbers, dollars, hours, or specific outcomes instead.

**HERO SECTION:**
Headline: {extracted_components.get('headline', 'N/A')}
Subhead: {extracted_components.get('subhead', 'N/A')}
CTA: {extracted_components.get('cta', 'N/A')}

**OUTPUT JSON:**
{{
  "friction_score": 85,
  "primary_crime": "Jargon Gate",
  "logic_reasoning": "...",
  "headline_audit": {{ "current_text": "...", "violations": ["..."], "a_list_rewrite": "..." }},
  "subhead_audit": {{ "current_text": "...", "violations": ["..."], "a_list_rewrite": "..." }},
  "cta_audit": {{ "current_text": "...", "violations": ["..."], "a_list_rewrite": "..." }}
}}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview", 
                messages=[
                    {"role": "system", "content": "You are a ruthless direct response copywriter. Respond ONLY in valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            result = parse_json_safely(response.choices[0].message.content)
            return result if result else self._fallback(extracted_components, "JSON Parse Fail")
            
        except Exception as e:
            return self._fallback(extracted_components, str(e))
    
    def _fallback(self, components, error):
        return {
            "friction_score": 50,
            "primary_crime": "Analysis Error",
            "logic_reasoning": f"Error: {error}",
            "headline_audit": {"current_text": components.get('headline', ''), "violations": [], "a_list_rewrite": "Error"},
            "subhead_audit": {"current_text": components.get('subhead', ''), "violations": [], "a_list_rewrite": "Error"},
            "cta_audit": {"current_text": components.get('cta', ''), "violations": [], "a_list_rewrite": "Error"}
        }