import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from exceptions.custom import AgentFlowException

logger = logging.getLogger("agentflow.exceptions")


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AgentFlowException)
    async def agentflow_exception_handler(request: Request, exc: AgentFlowException):
        logger.error(f"AgentFlowException: {exc.message} | Details: {exc.details}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "message": exc.message, "details": exc.details},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(
            f"Unhandled Exception on {request.url.path}: {exc!s}",
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "An unexpected error occurred on the server.",
                "details": {"error_type": exc.__class__.__name__, "message": str(exc)},
            },
        )
