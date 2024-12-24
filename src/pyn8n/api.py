"""pyn8n REST API."""
from enum import Enum

import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field

from dslmodel.agent_model import AgentModel
from pyn8n.n8n_decorator import router as n8n_router
from fastapi.middleware.cors import CORSMiddleware


import coloredlogs
from fastapi import FastAPI, Request

import pyn8n.n8n_nodes  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle FastAPI startup and shutdown events."""
    # Startup events:
    # - Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    # - Add coloredlogs' colored StreamHandler to the root logger.
    coloredlogs.install()

    # print(n8n_router.routes)
    # for route in app.routes:
    #     print(f"Route path: {route.path}, methods: {route.methods}")
    yield
    # Shutdown events.


app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include the n8n router
app.include_router(n8n_router, prefix="/actions")


@app.get("/compute")
async def compute(n: int = 42) -> int:
    """Compute the result of a CPU-bound function."""

    def fibonacci(n: int) -> int:
        return n if n <= 1 else fibonacci(n - 1) + fibonacci(n - 2)

    result = await asyncio.to_thread(fibonacci, n)
    return result


class VoicePayload(BaseModel):
    text: str

class Intent(str, Enum):
    NAVIGATE = "navigate"
    QUERY = "query"
    ACTION = "action"
    UNKNOWN = "unknown"

class VoiceResponse(AgentModel):
    thoughts: str = Field(..., title="The thoughts to generate the response.")
    intent: Intent = Field(..., title="The intent of the voice command.")
    answer: str = Field(..., title="The response to the voice prompt. DO NOT REPEAT THE PROMPT.")
    route: str = Field(..., title="The route to navigate to.")


@app.post("/voice")
async def voice_endpoint(payload: VoicePayload):
    """Echo the text from the payload"""
    print(f"Received payload: {payload}")
    prompt = f"""Routes to navigate to [
      "/agent",
      "/agents",
      "/analytics",
      "/api-keys",
      "/blockchain",
      "/blog",
      "/crew",
      "/crews",
      "/dashboard/agents",
      "/dashboard/inbox",
      "/dashboard",
      "/dashboard/settings",
      "/dashboard/settings/members",
      "/dashboard/settings/notifications",
      "/dashboard/settings",
      "/dashboard/users",
      "/docs",
      "/enterprise",
      "/index",
      "/integrations",
      "/login",
      "/marketplace",
      "/pricing",
      "/signup",
      "/tasks",
      "/ui-studio"
    ]
    {payload.text}
    """
    resp = await VoiceResponse.from_prompt(prompt, model="groq:llama3-groq-8b-8192-tool-use-preview")
    print(f"Response: {resp}")
    return resp
