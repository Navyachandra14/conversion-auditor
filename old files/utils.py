"""
utils.py - The Eyes (Refined for Smart Headline Detection)
Aggressively removes Nav bars and ignores Page Titles to find the Real Hook.
"""

import requests
from bs4 import BeautifulSoup
import re
import json

def validate_url(url):
    if not url: return False
    if not url.startswith(('http://', 'https://')): url = 'https://' + url
    return True

def scrape_website(url):
    """
    Robust scraper. Removes Navigation & Garbage.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        response = requests.get(url, headers=headers, timeout=15, verify=True)
        if response.encoding == 'ISO-8859-1':
            response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. CLEAN GARBAGE
        for element in soup(['script', 'style', 'noscript', 'svg', 'iframe', 'form', 'footer']):
            element.decompose()

        # 2. DESTROY NAVIGATION
        for nav in soup.find_all('nav'): nav.decompose()
        for header in soup.find_all('header'):
            for ul in header.find_all('ul'): ul.decompose()
        for element in soup.find_all(class_=re.compile(r'menu|nav|navigation|top-bar', re.I)):
            element.decompose()

        # 3. TEXT EXTRACTION
        text = soup.get_text(separator='\n')
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        clean_text = text.strip()

        if len(clean_text) < 50:
             return {'success': False, 'content': "", 'error': "Website blocked scraping. Please Paste Text manually."}

        return {
            'success': True,
            'content': clean_text[:4000], 
            'error': None
        }

    except Exception as e:
        return {'success': False, 'content': "", 'error': str(e)}

def extract_hero_components(text):
    """
    Smart Parsing: Skips Brand Names/Page Titles to find the Real Hook.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    if not lines:
        return {'headline': '', 'subhead': '', 'cta': ''}

    headline = lines[0]
    subhead = ""
    cta = ""
    
    # --- LOGIC UPGRADE: Skip "Brand Name" lines ---
    # If the first line has " - " or "|" it's usually a Page Title, not a Headline.
    # If it's the Brand Name (e.g. "SocialCura"), skip it.
    idx = 0
    if len(lines) > 0:
        first_line = lines[0]
        if " - " in first_line or " | " in first_line or len(first_line) < 20:
            # Likely a logo or title tag. Move to next line.
            if len(lines) > 1:
                headline = lines[1]
                idx = 1
            else:
                headline = lines[0]

    # Subhead is the next line
    if len(lines) > idx + 1:
        subhead = lines[idx + 1]

    # Intelligent CTA Hunt
    cta_triggers = ['get', 'start', 'try', 'join', 'book', 'sign', 'buy', 'demo', 'learn', 'talk', 'contact']
    
    # Scan lines looking for button-like text
    for line in lines[idx:idx+10]: 
        # Buttons are usually short (< 40 chars) and contain action verbs
        if len(line) < 40 and any(trigger in line.lower() for trigger in cta_triggers):
            cta = line
            break
            
    # Fallback if no button found
    if not cta and len(lines) > idx + 2:
        cta = lines[idx + 2]

    return {
        'headline': headline,
        'subhead': subhead,
        'cta': cta
    }

def parse_json_safely(response_text):
    if not response_text: return None
    try:
        cleaned = response_text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None