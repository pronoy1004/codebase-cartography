# Build from the repo root, not this directory:
#   docker build -f agents/codebase-cartographer/Dockerfile -t codebase-cartographer .
# The image needs skills/, which lives above this file.
#
# The service still clones a caller-supplied repository, which is enough reason to keep
# it contained even though the agent itself has no shell tool: git and the tool functions
# in tools.py only ever touch the checkout, but a container with no host mounts and
# limited egress is cheap insurance against a bug in that boundary.
FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends git ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 10001 agent
WORKDIR /app

RUN pip install --no-cache-dir "uvicorn>=0.30" \
      "agent-runtime @ git+https://github.com/pronoy1004/agent-runtime"

# The skills whose instructions get read into the system prompt.
COPY skills/ ./skills/
COPY agents/codebase-cartographer/*.py ./agents/codebase-cartographer/

USER agent
WORKDIR /app/agents/codebase-cartographer
EXPOSE 8000

# AGENT_API_KEY and GEMINI_API_KEY are required at run time.
# ALLOWED_REPO_ROOTS is left unset on purpose: in a container there is no host path
# worth exposing, so local-path requests are refused and only git URLs work.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
