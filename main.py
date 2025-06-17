from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_USER = os.getenv("API_USER")
API_SECRET = os.getenv("API_SECRET")

app = FastAPI()

class ImageURL(BaseModel):
    url: str

# Helper function to interpret AI score
def interpret_ai_score(score: float, threshold: float = 0.5) -> str:
    return "yes" if score >= threshold else "no"

@app.post("/check-url")
async def check_image_url(image: ImageURL):
    params = {
        'url': image.url,
        'models': 'genai',
        'api_user': API_USER,
        'api_secret': API_SECRET
    }
    try:
        r = requests.get('https://api.sightengine.com/1.0/check.json', params=params)
        result = r.json()

        if result.get("status") == "success" and "type" in result:
            ai_score = result["type"].get("ai_generated", 0)
            ai_result = interpret_ai_score(ai_score)
            return {
                "ai_generated": ai_result,
                "confidence_score": ai_score,
                "image_url": result.get("media", {}).get("uri", None)
            }

        return JSONResponse(content={"error": "API response failed", "details": result}, status_code=400)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/check-upload")
async def check_image_upload(file: UploadFile = File(...)):
    params = {
        'models': 'genai',
        'api_user': API_USER,
        'api_secret': API_SECRET
    }
    try:
        files = {'media': (file.filename, file.file, file.content_type)}
        r = requests.post('https://api.sightengine.com/1.0/check.json', data=params, files=files)
        result = r.json()

        if result.get("status") == "success" and "type" in result:
            ai_score = result["type"].get("ai_generated", 0)
            ai_result = interpret_ai_score(ai_score)
            return {
                "ai_generated": ai_result,
                "confidence_score": ai_score,
                "image_url": result.get("media", {}).get("uri", None)
            }

        return JSONResponse(content={"error": "API response failed", "details": result}, status_code=400)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)