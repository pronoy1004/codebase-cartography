"""ASGI entry point. Run: uvicorn main:app --port 8002"""

from agent import SPEC
from agent_runtime import create_app

app = create_app(SPEC)
