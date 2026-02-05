"""
app.py — Final Locked Production Version
"""

import os
import time
import logging
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# -----------------------
# ENV LOAD
# -----------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MASTER_KEY = os.getenv("MASTER_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY missing")

if not MASTER_KEY:
    raise RuntimeError("MASTER_KEY missing")

# -----------------------
# LOGGING
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
# INIT BRAINS
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# MASTER KEY GUARD
# -----------------------
def require_master_key(x_master_key: str = Header(None)):
    if x_master_key != MASTER_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

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
# REQUEST LOGGER
# -----------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 3)

    logging.info(
        f"{request.method} {request.url.path} "
        f"{response.status_code} {duration}s"
    )
    return response

# -----------------------
# ERROR HANDLER
# -----------------------
@app.exception_handler(Exception)
async def global_error_handler(request: Request, exc: Exception):
    logging.error(f"{request.url.path} → {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# -----------------------
# HEALTH (NO LOCK)
# -----------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------
# SIZE GUARD
# -----------------------
def validate_size(text: str, max_chars=5000):
    if len(text) > max_chars:
        raise HTTPException(status_code=413, detail="Input too large")

# -----------------------
# LEADGEN (LOCKED)
# -----------------------
@app.post("/leadgen")
def leadgen(
    req: LeadGenRequest,
    x_master_key: str = Header(None),
):
    require_master_key(x_master_key)
    validate_size(req.input_copy)
    return {"result": leadgen_brain.generate(req.input_copy, req.goal)}

# -----------------------
# SECTION REWRITE (LOCKED)
# -----------------------
@app.post("/section-rewrite")
def section_rewrite(
    req: SectionRequest,
    x_master_key: str = Header(None),
):
    require_master_key(x_master_key)
    validate_size(req.section_copy)
    return {"result": section_brain.audit_and_rewrite(req.section_copy)}

# -----------------------
# OUTREACH (LOCKED)
# -----------------------
@app.post("/outreach")
def outreach(
    req: OutreachRequest,
    x_master_key: str = Header(None),
):
    require_master_key(x_master_key)
    validate_size(req.context_input)
    return {
        "result": outreach_brain.generate_outreach(
            req.context_input, req.channel
        )
    }

# -----------------------
# DEEP DIVE (LOCKED)
# -----------------------
@app.post("/deep-dive")
def deep_dive(
    req: DeepDiveRequest,
    x_master_key: str = Header(None),
):
    require_master_key(x_master_key)
    validate_size(req.full_copy, 12000)
    return {"result": deep_brain.deep_audit(req.full_copy)}