from fastapi import FastAPI, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, BeforeValidator
from typing_extensions import Annotated
import logging
import os

from netfixgpt.providers.rag import RAGProvider
from netfixgpt.prompts.recommendation import RecommendationPrompt

app = FastAPI()


# Configure CORS
origins = [
    "http://localhost:3000",  # frontend URL
    "http://localhost:8080",  # frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # This allows all methods, such as GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # This allows all headers
)

MAX_PROMPT_SIZE = 250 #Avoid jailbreak prompts

def validate_prompt_details(v, handler):

    if len(v) < MAX_PROMPT_SIZE:
        return v
    
    else:
        raise HTTPException(
            status_code = 400,
            detail = "Invalid prompt - please try again with a prompt smaller than 250 characters"
        )

PromptDetails = Annotated[str, BeforeValidator(validate_prompt_details)]

class Prompt(BaseModel):
    details: PromptDetails

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "details": "Movies similar to The Bhoot Police"
                },
                {
                    "details": "Doctor G"
                },
            ]
        }
    }

@app.post("/generate", tags=["Generate"])
async def generate(
    req: Request,
    prompt_obj: Prompt
):
    """Generates movie recommendations.

    Params:

        prompt_obj: Prompt object containing movie recommendation details.

    """
    try:
        logging.info(f"Prompt: {prompt_obj.details}")

        prompt = RecommendationPrompt(details = prompt_obj.details)
        logging.info(f"Prompt: {str(prompt)}")

        provider = RAGProvider(api_key = os.environ["OPENAI_API_KEY"])
        response = provider.query(prompt = prompt)
        payload = jsonable_encoder({"answer": str(response)})

        logging.info(f"Response from ChatGPT: {payload}")
        response = JSONResponse(content=payload)

        return response
    
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")