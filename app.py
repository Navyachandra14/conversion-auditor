"""
app.py — Production Hardened Version
"""

from fastapi.middleware.cors import CORSMiddleware
import os
import time
import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from dotenv import load_dotenv

# -----------------------
# ENV LOAD
# -----------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY missing")

# -----------------------
# LOGGING SETUP
# -----------------------
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/api.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# -----------------------
# IMPORT BRAINS
# -----------------------
from brains.brain_leadgen_copy import LeadGenCopyBrain
from brains.brain_section_copy import SectionCopyBrain
from brains.brain_outreach import OutreachBrain
from brains.brain_deep_dive import DeepDiveBrain

# -----------------------
# INIT BRAINS (ONCE)
# -----------------------
leadgen_brain = LeadGenCopyBrain(OPENAI_API_KEY)
section_brain = SectionCopyBrain(OPENAI_API_KEY)
outreach_brain = OutreachBrain(OPENAI_API_KEY)
deep_brain = DeepDiveBrain(OPENAI_API_KEY)

# -----------------------
# FASTAPI INIT
# -----------------------
app = FastAPI(
    title="Conversion Intelligence API",
    version="1.0.0",
)
# CORS (Allow Browser UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------
# REQUEST MODELS
# -----------------------
class LeadGenRequest(BaseModel):
    input_copy: str
    goal: str = "lead_capture"

class SectionRequest(BaseModel):
    section_copy: str

class OutreachRequest(BaseModel):
    context_input: str
    channel: str = "email"

class DeepDiveRequest(BaseModel):
    full_copy: str

# -----------------------
# GLOBAL REQUEST LOGGER
# -----------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = round(time.time() - start_time, 3)

    logging.info(
        f"{request.method} {request.url.path} "
        f"Status={response.status_code} "
        f"Duration={duration}s"
    )

    return response

# -----------------------
# GLOBAL ERROR HANDLER
# -----------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"ERROR {request.url.path} → {str(exc)}")
    return HTTPException(
        status_code=500,
        detail="Internal server error. Logged."
    )

# -----------------------
# HEALTH
# -----------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------
# INPUT SIZE GUARD
# -----------------------
def validate_size(text: str, max_chars=5000):
    if len(text) > max_chars:
        raise HTTPException(
            status_code=413,
            detail="Input too large"
        )

# -----------------------
# LEADGEN
# -----------------------
@app.post("/leadgen")
def leadgen(req: LeadGenRequest):
    try:
        validate_size(req.input_copy)
        result = leadgen_brain.generate(req.input_copy, req.goal)
        return {"result": result}
    except Exception as e:
        logging.error(f"Leadgen error → {str(e)}")
        raise HTTPException(status_code=500, detail="Leadgen failed")

# -----------------------
# SECTION
# -----------------------
@app.post("/section-rewrite")
def section_rewrite(req: SectionRequest):
    try:
        validate_size(req.section_copy)
        result = section_brain.audit_and_rewrite(req.section_copy)
        return {"result": result}
    except Exception as e:
        logging.error(f"Section error → {str(e)}")
        raise HTTPException(status_code=500, detail="Section rewrite failed")

# -----------------------
# OUTREACH
# -----------------------
@app.post("/outreach")
def outreach(req: OutreachRequest):
    try:
        validate_size(req.context_input)
        result = outreach_brain.generate_outreach(req.context_input, req.channel)
        return {"result": result}
    except Exception as e:
        logging.error(f"Outreach error → {str(e)}")
        raise HTTPException(status_code=500, detail="Outreach failed")

# -----------------------
# DEEP DIVE
# -----------------------
@app.post("/deep-dive")
def deep_dive(req: DeepDiveRequest):
    try:
        validate_size(req.full_copy, 12000)
        result = deep_brain.deep_audit(req.full_copy)
        return {"result": result}
    except Exception as e:
        logging.error(f"Deep dive error → {str(e)}")
        raise HTTPException(status_code=500, detail="Deep audit failed")
