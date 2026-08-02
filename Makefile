# ==============================================================================
# AgentFlow — Makefile
# All commands run from the project root (one level above docker/)
# ==============================================================================

COMPOSE_FILE   := docker/docker-compose.yml
COMPOSE        := docker compose -f $(COMPOSE_FILE)
IMAGE_TAG      ?= latest
DOCKER_REGISTRY ?= ghcr.io/agentflow

.PHONY: help build up down logs restart rebuild clean clean-all \
        shell-backend shell-frontend ps test lint

# ---------------------------------------------------------------------------
# Default target
# ---------------------------------------------------------------------------
help:
	@echo ""
	@echo "  AgentFlow — Available Makefile targets"
	@echo "  ─────────────────────────────────────────────────"
	@echo "  make build      Build all Docker images (no cache)"
	@echo "  make up         Start all services in detached mode"
	@echo "  make down       Stop and remove containers"
	@echo "  make logs       Tail logs from all containers"
	@echo "  make restart    Restart all services"
	@echo "  make rebuild    Clean + build + up (full reset)"
	@echo "  make clean      Remove stopped containers, dangling images,"
	@echo "                  build cache, unused networks and volumes"
	@echo "  make clean-all  Prune EVERYTHING (use with caution)"
	@echo "  make ps         List running containers"
	@echo "  make test       Run pytest suite locally"
	@echo "  make lint       Run ruff linter"
	@echo ""

# ---------------------------------------------------------------------------
# Part 1 — Build images
# ---------------------------------------------------------------------------
build:
	@echo "==> Building all Docker images..."
	$(COMPOSE) build --no-cache --pull

# ---------------------------------------------------------------------------
# Part 2 — Start services
# ---------------------------------------------------------------------------
up:
	@echo "==> Starting all services..."
	$(COMPOSE) up -d
	@echo "==> Services are up."
	@echo "    Nginx  : http://localhost"
	@echo "    Swagger: http://localhost/docs"

# ---------------------------------------------------------------------------
# Part 3 — Stop services
# ---------------------------------------------------------------------------
down:
	@echo "==> Stopping all services..."
	$(COMPOSE) down --remove-orphans

# ---------------------------------------------------------------------------
# Part 4 — Tail logs
# ---------------------------------------------------------------------------
logs:
	$(COMPOSE) logs -f --tail=100

# ---------------------------------------------------------------------------
# Part 5 — Restart
# ---------------------------------------------------------------------------
restart: down up

# ---------------------------------------------------------------------------
# Part 6 — Full rebuild (clean state)
# ---------------------------------------------------------------------------
rebuild: clean build up

# ---------------------------------------------------------------------------
# Part 7 — Clean dangling/stale Docker resources
# ---------------------------------------------------------------------------
clean:
	@echo "==> Removing stopped containers..."
	-docker container prune -f
	@echo "==> Removing dangling images..."
	-docker image prune -f
	@echo "==> Removing build cache..."
	-docker builder prune -f
	@echo "==> Removing unused networks..."
	-docker network prune -f
	@echo "==> Clean complete."

# WARNING: removes ALL unused volumes (including persistent data).
# Only use on a fresh deployment or CI runners.
clean-all:
	@echo "==> WARNING: Pruning ALL unused Docker resources including volumes..."
	docker system prune -af --volumes
	@echo "==> Full prune complete."

# ---------------------------------------------------------------------------
# Utility targets
# ---------------------------------------------------------------------------
ps:
	$(COMPOSE) ps

shell-backend:
	$(COMPOSE) exec backend /bin/sh

shell-frontend:
	$(COMPOSE) exec frontend /bin/sh

test:
	PYTHONPATH=. .venv/bin/pytest -v --tb=short

lint:
	.venv/bin/ruff check app/ frontend/ tests/
