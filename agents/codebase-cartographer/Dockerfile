# Build from the repo root, not this directory:
#   docker build -f agents/codebase-cartographer/Dockerfile -t codebase-cartographer .
# The image needs skills/ and .claude-plugin/, which live above this file.
#
# The container is not a convenience here. This agent clones a caller-supplied repository
# and runs a model with Bash inside it, which is remote code execution by design. Run it
# in the container, as the non-root user below, with no host mounts and egress limited to
# the git host. See the README before deploying.
FROM python:3.12-slim

# git for the clone; node for the Claude Code CLI the Agent SDK drives.
RUN apt-get update \
 && apt-get install -y --no-install-recommends git nodejs npm ca-certificates \
 && npm install -g @anthropic-ai/claude-code \
 && apt-get purge -y npm && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 10001 agent
WORKDIR /app

RUN pip install --no-cache-dir "uvicorn>=0.30" \
      "agent-runtime @ git+https://github.com/pronoy1004/agent-runtime"

# The plugin: the skills the agent drives.
COPY .claude-plugin/ ./.claude-plugin/
COPY skills/ ./skills/
COPY agents/codebase-cartographer/*.py ./agents/codebase-cartographer/

USER agent
WORKDIR /app/agents/codebase-cartographer
EXPOSE 8000

# AGENT_API_KEY and ANTHROPIC_API_KEY are required at run time.
# ALLOWED_REPO_ROOTS is left unset on purpose: in a container there is no host path
# worth exposing, so local-path requests are refused and only git URLs work.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
