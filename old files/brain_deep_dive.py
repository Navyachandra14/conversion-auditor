"""
brain_deep_dive.py - The Revenue Intelligence Report Generator (OpenAI Version)
$50,000/month High-Ticket Management Consultant
"""

from openai import OpenAI
import os
from typing import Dict

class DeepDiveAnalyst:
    """
    The Deep Dive Brain - Generates comprehensive revenue intelligence reports
    """
    
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenAI API key required")
        self.client = OpenAI(api_key=api_key)
    
    def generate_report(self, page_content: str, copy_audit: Dict, ux_audit: Dict) -> str:
        """
        Generate comprehensive Markdown revenue intelligence report.
        Synthesizes the Copy and UX audits into a strategic roadmap.
        """
        
        # Extract key metrics to feed the consultant brain
        copy_score = copy_audit.get('friction_score', 0)
        ux_score = ux_audit.get('ux_score', 0)
        headline_rewrite = copy_audit.get('headline_audit', {}).get('a_list_rewrite', 'N/A')
        
        prompt = f"""You are a High-Ticket Conversion Consultant (McKinsey/Bain level).
You charge $50,000 for a "Revenue Intelligence Audit."

**THE CLIENT'S SITUATION:**
- Copy Friction Score: {copy_score}/100 (High friction = Bad)
- Cognitive Load Score: {ux_score}/100 (High score = Good scannability)
- Identified Headline Issue: {copy_audit.get('headline_audit', {}).get('crime', 'Unknown')}

**PAGE CONTENT SAMPLE:**
{page_content[:4000]}

**YOUR TASK:**
Write a **Revenue Recovery Roadmap** in Markdown format.
Do NOT write generic advice ("Add more testimonials"). 
Write forensic analysis ("Your testimonials lack specificity, causing a 20% drop in trust").

**REPORT STRUCTURE (Strictly Follow This):**

# 📑 REVENUE INTELLIGENCE REPORT

## 1. EXECUTIVE DIAGNOSIS
- Summarize the single biggest revenue leak.
- Estimate the "Lost Revenue Opportunity" (use hypothetical but realistic math).

## 2. THE TRUST GAP ANALYSIS
- **Forensic Evidence:** Audit the text for specific numbers, names, and data points.
- **The Verdict:** Is this brand "Vague" (High Risk) or "Specific" (Low Risk)?
- **Missing Elements:** explicitly list missing trust signals (e.g., "No 'As Seen On' logos," "Testimonials lack full names").

## 3. OBJECTION HANDLING MATRIX
- Identify the top 3 unaddressed objections a skeptical buyer would have.
- Script the exact "Objection Killer" copy block for each.

## 4. THE COMPETITIVE "ONLY" FACTOR
- Does the copy articulate a Unique Mechanism?
- If not, write a "We are the only..." statement for them.

## 5. 90-DAY RECOVERY PLAN (Prioritized)
- **Phase 1 (24 Hours):** The "Quick Wins" (e.g., Swap the Headline).
- **Phase 2 (7 Days):** The "Trust Injection" (Gathering proof).
- **Phase 3 (30 Days):** The "Offer Restructure" (Risk Reversal).

---
**Tone:** Expensive, Direct, authoritative. No fluff.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview", # Use smart model for long reports
                messages=[
                    {"role": "system", "content": "You are a high-ticket management consultant. Output professional Markdown."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"# ❌ Report Generation Failed\n\nError details: {str(e)}"