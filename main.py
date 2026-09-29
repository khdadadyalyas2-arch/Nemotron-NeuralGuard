https://api.studio.nebius.ai/v1/chat/completionsimport os
import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Nemotron-NeuralGuard", version="1.0.0")

NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY", "nebius-default-key")
MODEL = "nvidia/Llama-3.1-Nemotron-70B-Instruct"

class AuditRequest(BaseModel):
    payload: str

@app.get("/")
def root():
    return {"status": "active", "model": MODEL, "engine": "Nebius Token Factory"}

@app.post("/audit")
async def audit(req: AuditRequest):
    headers = {"Authorization": f"Bearer {NEBIUS_API_KEY}", "Content-Type": "application/json"}
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are Nemotron-NeuralGuard, an autonomous on-chain auditor for smart contracts and payloads. Evaluate security risks, reentrancy vulnerabilities, and malicious opcodes with extreme precision."},
            {"role": "user", "content": f"Audit Target:\n{req.payload}"}
        ],
        "temperature": 0.2
    }
    try:
        async with httpx.AsyncClient(timeout=45.0) as client:
            res = await client.post("https://api.studio.nebius.ai/v1/chat/completions", headers=headers, json=body)
        return {"report": res.json()["choices"][0]["message"]["content"], "auditor": MODEL}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
