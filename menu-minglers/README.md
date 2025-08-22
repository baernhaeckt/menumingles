# Menu Minglers

A FastAPI application for menu management with a clean, maintainable architecture.

## Features

- FastAPI framework for high-performance API development
- Poetry for dependency management
- Uvicorn as ASGI server
- Health check endpoint
- Clean architecture with separated concerns (endpoints, managers, services, models)
- Docker support for containerized deployment
- Development tools: Black, isort, flake8, mypy

## Project Structure

```
app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration settings
├── api/
│   └── v1/
│       ├── endpoints/
│       │   └── health.py
│       └── router.py
├── core/
│   └── exceptions.py
├── models/
│   └── health.py
├── services/
│   └── health_service.py
└── managers/
    └── health_manager.py
```

## Setup

### Prerequisites

- Python 3.12+
- Poetry

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd menu-minglers
```

2. Install dependencies:

```bash
poetry install
```

3. Activate the virtual environment:

```bash
poetry shell
```

### Development

Run the application in development mode:

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Code Quality

Format code:

```bash
poetry run black .
poetry run isort .
```

Lint code:

```bash
poetry run flake8 .
poetry run mypy .
```

Run tests:

```bash
poetry run pytest
```

## Docker

Build the Docker image:

```bash
docker build -t menu-minglers .
```

Run the container:

```bash
docker run -p 8000:8000 menu-minglers
```

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Environment Variables

- `APP_ENV` - Application environment (development, production)
- `DEBUG` - Debug mode (true/false)
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)

## Contributing

1. Follow the existing code style (Black + isort)
2. Add tests for new features
3. Ensure all tests pass before submitting
4. Update documentation as needed
