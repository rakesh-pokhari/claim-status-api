from fastapi import FastAPI, HTTPException
from src.services.claim_service import get_claim
from src.services.summary_service import summarize_claim

app = FastAPI()

@app.get("/claims/{claim_id}")
def fetch_claim(claim_id: str):
    claim = get_claim(claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim


@app.post("/claims/{claim_id}/summarize")
def summarize(claim_id: str):
    result = summarize_claim(claim_id)
    if not result:
        raise HTTPException(status_code=404, detail="Claim not found")
    return result
