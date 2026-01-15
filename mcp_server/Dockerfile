# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
WORKDIR /app
COPY . ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Run the web service on container startup.
# We use uvicorn to serve the FastMCP app
# Cloud Run expects the container to listen on $PORT (default 8080)
CMD exec fastmcp run mcp_server/server.py --host 0.0.0.0 --port ${PORT:-8080}
