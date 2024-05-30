from fastapi import FastAPI
from core.config.environments import OPENAI_API_KEY
from core.config.router import router
import openai
from fastapi.middleware.cors import CORSMiddleware

# Seetings to API KEY OPENAI
openai.api_key = OPENAI_API_KEY

# Create FastAPI app instance
app = FastAPI()
app.include_router(router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=["*"],
)