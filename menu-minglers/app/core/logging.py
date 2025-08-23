"""Logging utilities for the application."""

import logging
import sys
import traceback
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

from fastapi import Request
from fastapi.responses import JSONResponse

from app.config import settings


class StructuredLogger:
    """Structured logger for detailed error tracking."""
    
    def __init__(self, name: str = "menu_minglers"):
        """Initialize the structured logger.
        
        Args:
            name: Logger name
        """
        self.logger = logging.getLogger(name)
        
        # Set log level from settings
        log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        
        # Clear existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Create formatters
        self.detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.json_formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": %(message)s}'
        )
        
        # Console handler (if enabled)
        if settings.enable_console_logging:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(self.detailed_formatter)
            self.logger.addHandler(console_handler)
        
        # File handler for detailed logs
        try:
            file_handler = logging.FileHandler(settings.log_file_path)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(self.detailed_formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            # Fallback to console if file logging fails
            print(f"Warning: Could not create file handler for {settings.log_file_path}: {e}")
        
        # Error file handler
        try:
            error_handler = logging.FileHandler(settings.error_log_file_path)
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(self.detailed_formatter)
            self.logger.addHandler(error_handler)
        except Exception as e:
            # Fallback to console if error file logging fails
            print(f"Warning: Could not create error file handler for {settings.error_log_file_path}: {e}")
    
    def _format_error_context(
        self,
        error: Exception,
        request: Optional[Request] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Format error context with stack trace and request details.
        
        Args:
            error: The exception that occurred
            request: FastAPI request object (optional)
            additional_context: Additional context data (optional)
            
        Returns:
            Formatted error context dictionary
        """
        error_id = str(uuid4())
        
        # Get full stack trace
        exc_type, exc_value, exc_traceback = sys.exc_info()
        stack_trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
        
        context = {
            "error_id": error_id,
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "stack_trace": stack_trace,
            "additional_context": additional_context or {}
        }
        
        # Add request context if available
        if request:
            context["request"] = {
                "method": request.method,
                "url": str(request.url),
                "headers": dict(request.headers),
                "client": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
            }
            
            # Try to get request body (be careful with sensitive data)
            try:
                if hasattr(request, '_body'):
                    context["request"]["body_size"] = len(request._body)
            except Exception:
                pass
        
        return context
    
    def log_error(
        self,
        error: Exception,
        request: Optional[Request] = None,
        additional_context: Optional[Dict[str, Any]] = None,
        level: str = "ERROR"
    ) -> str:
        """Log an error with full context and stack trace.
        
        Args:
            error: The exception that occurred
            request: FastAPI request object (optional)
            additional_context: Additional context data (optional)
            level: Log level (ERROR, CRITICAL, etc.)
            
        Returns:
            Error ID for tracking
        """
        context = self._format_error_context(error, request, additional_context)
        error_id = context["error_id"]
        
        # Log the structured error
        log_message = f"Error ID: {error_id} - {type(error).__name__}: {str(error)}"
        
        if level.upper() == "CRITICAL":
            self.logger.critical(log_message, extra={"error_context": context})
        else:
            self.logger.error(log_message, extra={"error_context": context})
        
        # Also log the full context as a separate message for easier parsing
        self.logger.error(f"Error Context for {error_id}: {context}")
        
        return error_id
    
    def log_warning(
        self,
        message: str,
        request: Optional[Request] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Log a warning with context.
        
        Args:
            message: Warning message
            request: FastAPI request object (optional)
            additional_context: Additional context data (optional)
            
        Returns:
            Warning ID for tracking
        """
        warning_id = str(uuid4())
        context = {
            "warning_id": warning_id,
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "additional_context": additional_context or {}
        }
        
        if request:
            context["request"] = {
                "method": request.method,
                "url": str(request.url),
                "client": request.client.host if request.client else None,
            }
        
        self.logger.warning(f"Warning ID: {warning_id} - {message}", extra={"warning_context": context})
        return warning_id
    
    def log_info(
        self,
        message: str,
        request: Optional[Request] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ):
        """Log an info message with context.
        
        Args:
            message: Info message
            request: FastAPI request object (optional)
            additional_context: Additional context data (optional)
        """
        context = additional_context or {}
        if request:
            context["request"] = {
                "method": request.method,
                "url": str(request.url),
            }
        
        self.logger.info(f"{message}", extra={"info_context": context})
    
    def log_debug(
        self,
        message: str,
        request: Optional[Request] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ):
        """Log a debug message with context.
        
        Args:
            message: Debug message
            request: FastAPI request object (optional)
            additional_context: Additional context data (optional)
        """
        context = additional_context or {}
        if request:
            context["request"] = {
                "method": request.method,
                "url": str(request.url),
            }
        
        self.logger.debug(f"{message}", extra={"debug_context": context})


# Global logger instance
logger = StructuredLogger()


def log_exception_handler(
    request: Request,
    exc: Exception,
    additional_context: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """Global exception handler that logs errors with full context.
    
    Args:
        request: FastAPI request object
        exc: The exception that occurred
        additional_context: Additional context data (optional)
        
    Returns:
        JSONResponse with error details
    """
    error_id = logger.log_error(exc, request, additional_context)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "error_id": error_id,
            "detail": str(exc) if logger.logger.level <= logging.DEBUG else "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )
