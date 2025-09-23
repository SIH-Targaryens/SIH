from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

try:
    import google.generativeai as genai
except ImportError:
    genai = None

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    history: list = []

class PredictRequest(BaseModel):
    exam: str
    percentile: float
    category: str = "general"
    state: str = "all_india"

class IssueRequest(BaseModel):
    issue: str
    user_context: dict = {}

def get_gemini_model():
    api_key = os.getenv("AIzaSyDtagAC7zSCMvimq9DWXkuYMuF3P_NyECY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Gemini API key not configured.")
    if not genai:
        raise HTTPException(status_code=500, detail="google-generativeai SDK not installed.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-pro")

@router.post("/chat")
async def ai_chat(req: ChatRequest):
    model = get_gemini_model()
    prompt = f"You are a helpful AI career counselor. Answer the user's question for Indian students: {req.query}"
    try:
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

@router.post("/predict")
async def predict_rank(req: PredictRequest):
    """
    Predicts rank or college possibilities based on percentile for an exam.
    Replace dummy logic with ML model or Gemini prompt if needed.
    """
    if req.exam.lower() == "jee main":
        approx_rank = int((100 - req.percentile) * 1000)  
        message = (
            f"With a percentile of {req.percentile} in {req.exam}, "
            f"your approximate rank is {approx_rank}. "
            "This is a rough estimate; use official tools for counselling."
        )
        return {"predicted_rank": approx_rank, "message": message}
    prompt = (
        f"A student scored {req.percentile} percentile in {req.exam} "
        f"({req.category}, {req.state}). Predict their approximate rank or best possible college. "
        "Give concise advice and probable outcomes."
    )
    model = get_gemini_model()
    try:
        response = model.generate_content(prompt)
        return {"message": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

@router.post("/issue")
async def solve_issue(req: IssueRequest):
    """
    Accepts user's issue (career confusion, college choice, stress...) and responds supportively.
    """
    model = get_gemini_model()
    prompt = (
        "You are a career support assistant and counselor. "
        "A student has the following issue or query:\n"
        f"{req.issue}\n"
        "Given their context (if any):\n"
        f"{req.user_context}\n"
        "Give actionable and empathetic advice. Suggest resources or next steps if possible."
    )
    try:
        response = model.generate_content(prompt)
        return {"advice": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")
