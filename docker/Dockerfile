# Build container using python slim base
FROM python:3.12-slim

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Setup working directory
WORKDIR /workspace

# Copy dependencies definitions
COPY pyproject.toml uv.lock ./

# Install project dependencies
RUN uv sync --frozen --no-cache

# Copy application files
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI backend app
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]