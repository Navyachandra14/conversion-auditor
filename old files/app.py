"""
app.py - The Pure Copy Engine
Focuses 100% on Forensic Copy Auditing. No UX. No Fluff.
"""

import streamlit as st
from utils import scrape_website, extract_hero_components, validate_url
from brain_copy import ForensicCopyAuditor

# --- CONFIG ---
st.set_page_config(page_title="Forensic Copy Engine", page_icon="📝", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    .metric-container { background-color: #f8f9fa; border: 1px solid #ddd; padding: 20px; border-radius: 10px; text-align: center; }
    .audit-card { background-color: white; border: 1px solid #eee; padding: 20px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #6c757d; }
    .audit-card.bad { border-left-color: #dc3545; }
    .rewrite-box { background-color: #d4edda; color: #155724; padding: 15px; border-radius: 5px; font-weight: bold; border: 1px solid #c3e6cb; }
    .violation-tag { background-color: #f8d7da; color: #721c24; padding: 2px 8px; border-radius: 12px; font-size: 0.85em; margin-right: 5px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("📝 Copy Engine")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    st.markdown("---")
    
    input_method = st.radio("Input Source", ["URL", "Paste Text"])
    
    if input_method == "URL":
        target_url = st.text_input("Enter URL", placeholder="https://example.com")
        manual_text = None
    else:
        target_url = None
        manual_text = st.text_area("Paste Hero Text", height=300)

    st.markdown("---")
    run_btn = st.button("🚀 Run Forensic Audit", type="primary")

# --- MAIN LOGIC ---
if run_btn:
    if not api_key:
        st.error("⚠️ API Key required.")
        st.stop()

    # 1. SCRAPING
    with st.spinner("🔍 Extracting Text..."):
        if manual_text:
            text_data = manual_text
            components = extract_hero_components(text_data)
        elif target_url:
            if not validate_url(target_url):
                st.error("Invalid URL.")
                st.stop()
            scrape_result = scrape_website(target_url)
            if not scrape_result['success']:
                st.error(scrape_result['error'])
                st.stop()
            text_data = scrape_result['content']
            components = extract_hero_components(scrape_result['content'])
        else:
            st.error("Input required.")
            st.stop()

    # 2. AUDITING
    try:
        auditor = ForensicCopyAuditor(api_key)
        with st.spinner("🧠 Analyzing Sales Psychology..."):
            result = auditor.audit(text_data[:3000], components)
            
        # --- DISPLAY RESULTS ---
        c1, c2 = st.columns([1, 3])
        with c1:
            score = result.get('friction_score', 0)
            st.markdown(f"""
            <div class="metric-container">
                <h1 style="color: {'#dc3545' if score > 50 else '#28a745'}; margin:0;">{score}/100</h1>
                <p style="margin:0; color: #666;">Friction Score</p>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"### 🚨 Primary Crime: {result.get('primary_crime', 'Unknown')}")
            st.info(f"**Verdict:** {result.get('logic_reasoning', 'N/A')}")

        st.divider()

        # COMPONENTS
        for title, key in [("1. The Headline", "headline_audit"), ("2. The Subhead", "subhead_audit"), ("3. The CTA", "cta_audit")]:
            data = result.get(key, {})
            st.markdown(f"### {title}")
            st.markdown(f"""
            <div class="audit-card bad">
                <small style="color:#666; text-transform:uppercase; font-weight:bold;">Current Text</small>
                <div style="font-size:1.1em; margin-bottom:10px;">"{data.get('current_text', 'N/A')}"</div>
                <div>{' '.join([f'<span class="violation-tag">{v}</span>' for v in data.get('violations', [])])}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"<div class='rewrite-box'>✅ Rewrite: {data.get('a_list_rewrite', 'N/A')}</div>", unsafe_allow_html=True)
            st.markdown("---")

    except Exception as e:
        st.error(f"System Failure: {str(e)}")

else:
    st.info("👈 Enter API Key and URL to start.")