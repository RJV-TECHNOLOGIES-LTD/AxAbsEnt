# api/errors.py

"""
AxAbsEnt API Error Handling System
Provides consistent error representation across the API with proper status codes,
error codes, and detailed messages for debugging and client integration.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union
import logging
from uuid import uuid4

# Setup logger
logger = logging.getLogger("axabsent.errors")

# Error response model
class ErrorResponse(BaseModel):
    detail: str
    status_code: int = Field(..., ge=100, le=599)
    error_code: str
    error_id: str
    path: str
    timestamp: str
    context: Optional[Dict[str, Any]] = None
    validation_errors: Optional[List[Dict[str, Any]]] = None

# Error types with codes
class ErrorCode:
    # Client errors (4xx)
    INVALID_REQUEST = "INVALID_REQUEST"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN" 
    IMMUTABLE_ENTITY = "IMMUTABLE_ENTITY"
    INVALID_PARAMETERS = "INVALID_PARAMETERS"
    ENTITY_NOT_FOUND = "ENTITY_NOT_FOUND"
    
    # Server errors (5xx)
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SIMULATION_FAILURE = "SIMULATION_FAILURE"
    DATABASE_ERROR = "DATABASE_ERROR"
    COMPUTATION_ERROR = "COMPUTATION_ERROR"
    MODEL_ERROR = "MODEL_ERROR"
    
    # Domain-specific errors
    ONTOLOGY_VIOLATION = "ONTOLOGY_VIOLATION"
    FORCE_EXTRACTION_ERROR = "FORCE_EXTRACTION_ERROR"
    ABSOLUTE_ENTITY_ERROR = "ABSOLUTE_ENTITY_ERROR"

# Base exception class
class AxAbsEntError(Exception):
    def __init__(
        self, 
        detail: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = ErrorCode.INTERNAL_ERROR,
        context: Optional[Dict[str, Any]] = None
    ):
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code
        self.context = context or {}
        super().__init__(self.detail)

# Specific exception classes
class ResourceNotFoundError(AxAbsEntError):
    def __init__(self, detail: str, resource_type: str, resource_id: str = None):
        context = {"resource_type": resource_type}
        if resource_id:
            context["resource_id"] = resource_id
            
        super().__init__(
            detail=detail,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ErrorCode.RESOURCE_NOT_FOUND,
            context=context
        )

class ValidationError(AxAbsEntError):
    def __init__(self, detail: str, errors: List[Dict[str, Any]] = None):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code=ErrorCode.INVALID_PARAMETERS,
            context={"validation_errors": errors or []}
        )

class SimulationError(AxAbsEntError):
    def __init__(self, detail: str, simulation_type: str, parameters: Dict[str, Any] = None):
        context = {"simulation_type": simulation_type}
        if parameters:
            context["parameters"] = parameters
            
        super().__init__(
            detail=detail,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=ErrorCode.SIMULATION_FAILURE,
            context=context
        )

class OntologyViolationError(AxAbsEntError):
    def __init__(self, detail: str, entity_id: str = None):
        context = {}
        if entity_id:
            context["entity_id"] = entity_id
            
        super().__init__(
            detail=detail,
            status_code=status.HTTP_409_CONFLICT,
            error_code=ErrorCode.ONTOLOGY_VIOLATION,
            context=context
        )

# Setup exception handlers for FastAPI
def setup_error_handlers(app: FastAPI):
    """Register all error handlers with the FastAPI application"""
    
    @app.exception_handler(AxAbsEntError)
    async def handle_axabsent_error(request: Request, exc: AxAbsEntError):
        """Handle all custom AxAbsEnt exceptions"""
        error_id = str(uuid4())
        
        # Log the error
        logger.error(
            f"Error {error_id}: {exc.error_code} - {exc.detail}",
            extra={
                "error_id": error_id,
                "status_code": exc.status_code,
                "path": request.url.path,
                "context": exc.context
            }
        )
        
        # Create response
        error_response = ErrorResponse(
            detail=exc.detail,
            status_code=exc.status_code,
            error_code=exc.error_code,
            error_id=error_id,
            path=request.url.path,
            timestamp=datetime.datetime.utcnow().isoformat(),
            context=exc.context
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.dict()
        )
    
    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors"""
        error_id = str(uuid4())
        
        # Log the error
        logger.warning(
            f"Validation error {error_id} at {request.url.path}",
            extra={
                "error_id": error_id,
                "errors": exc.errors()
            }
        )
        
        # Create response
        error_response = ErrorResponse(
            detail="Request validation failed",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code=ErrorCode.INVALID_PARAMETERS,
            error_id=error_id,
            path=request.url.path,
            timestamp=datetime.datetime.utcnow().isoformat(),
            validation_errors=exc.errors()
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response.dict()
        )
    
    @app.exception_handler(Exception)
    async def handle_unhandled_exception(request: Request, exc: Exception):
        """Catch-all handler for unhandled exceptions"""
        error_id = str(uuid4())
        
        # Log the error with traceback
        logger.exception(
            f"Unhandled exception {error_id} at {request.url.path}: {str(exc)}",
            exc_info=exc
        )
        
        # Create response (with limited details for security)
        error_response = ErrorResponse(
            detail="An unexpected error occurred",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=ErrorCode.INTERNAL_ERROR,
            error_id=error_id,
            path=request.url.path,
            timestamp=datetime.datetime.utcnow().isoformat()
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.dict()
        )
