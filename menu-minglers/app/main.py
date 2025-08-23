"""FastAPI application entry point."""

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.config import settings
from app.core.logging import log_exception_handler, logger

load_dotenv()

# ---- ultra-ugly hackathon patch: make llama_index.core.Document.text writable ----
try:
    from llama_index.core import Document  # llama-index-core >= 0.10
except Exception:
    from llama_index import Document  # some older versions expose it here

# Only patch if it's a read-only property
if isinstance(getattr(Document, "text", None), property) and Document.text.fset is None:
    _getter = Document.text.fget

    def _set_text(self, value):
        """
        Make .text 'settable' by recreating the underlying pydantic model
        and copying fields back in-place. This avoids pydantic's __setattr__ guard.
        """
        try:
            # pydantic v2 BaseModel has model_copy(update=...)
            new_model = self.model_copy(update={"text": value})
            # Replace fields in-place so existing references keep working
            for k, v in new_model.__dict__.items():
                object.__setattr__(self, k, v)
        except Exception:
            # Absolute last-ditch fallback: force-set a private attr
            # (may be ignored by LlamaIndex versions, but keeps us running)
            object.__setattr__(self, "_text", value)

    Document.text = property(_getter, _set_text)
# ---- end hack ----

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A FastAPI application for menu management",
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    debug=settings.debug,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler to catch all unhandled exceptions."""
    return log_exception_handler(request, exc)


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Menu Minglers API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": f"{settings.api_v1_prefix}/health"
    }
