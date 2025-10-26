# Drama Llama AI Service

> AI-powered learning platform with personalized roadmaps, learning materials, quizzes, and graduation projects.

A FastAPI-based microservice that provides intelligent career guidance, personalized learning roadmap generation, and adaptive educational content creation using GROQ's LLM API.

---

## 📑 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
  - [Docker Deployment](#docker-deployment)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Database](#-database)
- [AI Service Architecture](#-ai-service-architecture)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🚀 Features

### Core Capabilities

- **🤖 AI-Powered Chat**: Conversational interface for career guidance and learning advice
- **🗺️ Personalized Roadmap Generation**: Creates structured learning paths based on user goals and experience level
- **📚 Learning Material Creation**: Generates comprehensive study materials with examples, projects, and resources
- **📝 Quiz Generation**: Creates adaptive quizzes for knowledge assessment
- **🎓 Graduation Projects**: Generates and evaluates capstone projects with AI-powered feedback
- **💼 CV Analysis**: Extracts and analyzes information from PDF resumes
- **🔄 Session Management**: Maintains conversation context across interactions
- **⚡ Streaming Responses**: Server-Sent Events (SSE) for real-time AI responses

### AI Features

- Context-aware conversation management
- Tool-based execution system (roadmap creation, material generation, quiz creation)
- Multi-phase learning workflow (Roadmap → Materials → Quizzes → Graduation Project)
- Structured output using JSON schemas
- Auto-reloading prompt system for rapid development

---

## 🏗️ Architecture

The service follows a modular architecture:

```
┌─────────────┐
│   FastAPI   │  ← REST API Layer
└──────┬──────┘
       │
┌──────┴──────────────────────┐
│   Routes Layer              │  ← Endpoint handlers
│  (ai_actions, sessions,     │
│   graduation_project)       │
└──────┬──────────────────────┘
       │
┌──────┴──────────────────────┐
│   AI Service Layer          │  ← Business logic
│  (AIService, GroqClient)    │
└──────┬──────────────────────┘
       │
┌──────┴──────────────────────┐
│   Database Layer (CRUD)     │  ← Data access
│  (PostgreSQL + SQLAlchemy)  │
└─────────────────────────────┘
```

### Key Components

1. **Routes**: HTTP endpoint handlers for different features
2. **AI Service**: Orchestrates AI interactions and tool execution
3. **GROQ Client**: Manages communication with GROQ's LLM API
4. **Database Layer**: PostgreSQL with SQLAlchemy ORM
5. **Prompt System**: YAML-based prompt templates with hot-reloading
6. **Authentication**: API key-based security

---

## 🛠️ Tech Stack

### Backend Framework

- **FastAPI 0.104+**: Modern, high-performance web framework
- **Uvicorn**: ASGI server with WebSocket support
- **Pydantic v2**: Data validation and settings management

### AI/ML

- **GROQ API**: LLM inference (Llama-4 Maverick 17B)
- **OpenAI SDK**: Client library for API interactions
- **Structured Outputs**: JSON schema-based response formatting

### Database

- **PostgreSQL 16**: Primary database
- **SQLAlchemy 2.0**: ORM and query builder
- **Alembic**: Database migrations

### Document Processing

- **PyPDF**: PDF text extraction
- **PyMuPDF (fitz)**: Advanced PDF parsing
- **ftfy**: Text encoding fixes

### Infrastructure

- **Docker & Docker Compose**: Containerization
- **Redis 5.0+**: Caching layer (optional)

### Development Tools

- **pytest**: Testing framework
- **python-dotenv**: Environment management
- **PyYAML**: Prompt template parsing

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **PostgreSQL 16+** (or Docker)
- **GROQ API Key** ([Get one here](https://console.groq.com))
- **Git**

### Local Development

#### 1. Clone the Repository

```bash
git clone https://github.com/astudentinearth/drama-llama.git
cd drama-llama/ai
```

#### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# Required
GROQ_API_KEY=your-groq-api-key-here
API_KEY_SECRET=your-secret-key-here

# Database (adjust for your setup)
AI_DATABASE_URL=postgresql://username:password@localhost:5432/dramallama_ai

# Optional - GROQ Configuration
GROQ_MODEL=meta-llama/llama-4-maverick-17b-128e-instruct
GROQ_MAX_TOKENS=4096
GROQ_TEMPERATURE=0.1
GROQ_TIMEOUT=60

# API Settings
API_HOST=0.0.0.0
API_PORT=8001
API_RELOAD=True
LOG_LEVEL=INFO
```

#### 5. Set Up Database

```bash
# Create PostgreSQL database
createdb dramallama_ai

# Or use psql
psql -U postgres
CREATE DATABASE dramallama_ai;
\q
```

#### 6. Initialize Database Tables

The application automatically creates tables on first run. You can also trigger manually:

```bash
# Start the server
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Hit the health endpoint to initialize
curl http://localhost:8001/health
```

#### 7. Verify Installation

```bash
# Check health endpoint
curl http://localhost:8001/health

# Expected response:
# {"status":"ok","database":"connected","error":null}
```

#### 8. Access API Documentation

Open your browser:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

---

### Docker Deployment

For production or isolated development, use Docker:

#### 1. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

#### 2. Build and Run

```bash
# Start all services (AI service + PostgreSQL)
docker-compose up -d

# View logs
docker-compose logs -f ai_service

# Stop services
docker-compose down
```

#### 3. Verify

```bash
curl http://localhost:8001/health
```

For detailed Docker instructions, see [README.docker.md](./README.docker.md).

---

## 📂 Project Structure

```
ai/
├── config.py                      # Application configuration
├── main.py                        # FastAPI application entry point
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container definition
├── docker-compose.yml            # Multi-container orchestration
│
├── db_config/                    # Database layer
│   ├── __init__.py
│   ├── database.py              # SQLAlchemy engine & session
│   └── crud.py                  # Database operations
│
├── models/                       # Data models
│   ├── __init__.py
│   ├── db_models.py            # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic request/response models
│   └── Prompt.py               # Prompt handling logic
│
├── routes/                       # API endpoints
│   ├── __init__.py
│   ├── ai_actions.py           # Main AI chat & tools
│   ├── sessions.py             # Session management
│   └── graduation_project.py   # Graduation project features
│
├── utils/                        # Utility modules
│   ├── __init__.py
│   ├── auth.py                 # API key authentication
│   ├── groq_client.py          # GROQ API client
│   ├── pdf_parse.py            # PDF processing
│   ├── prompt_loader.py        # YAML prompt loader
│   ├── yaml_parser.py          # YAML parsing utilities
│   │
│   └── ai/                      # AI service components
│       ├── __init__.py
│       ├── service.py          # Core AI orchestration
│       └── tool_specs.py       # Tool definitions & schemas
│
├── prompts/                      # YAML prompt templates
│   ├── master.prompt.yaml       # Main conversation orchestration
│   ├── createroadmapskeleton.prompt.yaml
│   ├── createlearningmaterial.prompt.yaml
│   ├── createquizforgoal.prompt.yaml
│   ├── editroadmapskeleton.prompt.yaml
│   ├── evaluategraduationprojectanswer.prompt.yaml
│   ├── extractcvinformation.prompt.yaml
│   └── creategraduationproject.prompt.yaml
│
└── scripts/                      # Utility scripts
    └── check_ollama.py          # Ollama health check (legacy)
```

### Key Files Explained

- **`main.py`**: Application entry point, router registration, health checks
- **`config.py`**: Centralized settings using Pydantic BaseSettings
- **`utils/ai/service.py`**: Core AI logic - tool planning and execution
- **`utils/groq_client.py`**: GROQ API wrapper with structured outputs
- **`routes/ai_actions.py`**: Primary endpoints for chat and AI interactions
- **`db_config/crud.py`**: All database operations (sessions, roadmaps, materials, etc.)
- **`prompts/*.yaml`**: Editable prompt templates (hot-reloaded in dev mode)

---

## ⚙️ Configuration

### Environment Variables

| Variable              | Default                                         | Description                  |
| --------------------- | ----------------------------------------------- | ---------------------------- |
| **GROQ API**          |                                                 |                              |
| `GROQ_API_KEY`        | _(required)_                                    | Your GROQ API key            |
| `GROQ_MODEL`          | `meta-llama/llama-4-maverick-17b-128e-instruct` | Model identifier             |
| `GROQ_MAX_TOKENS`     | `4096`                                          | Maximum response tokens      |
| `GROQ_TEMPERATURE`    | `0.1`                                           | Sampling temperature (0-1)   |
| `GROQ_TIMEOUT`        | `60`                                            | Request timeout (seconds)    |
| **API Settings**      |                                                 |                              |
| `API_HOST`            | `0.0.0.0`                                       | Server bind address          |
| `API_PORT`            | `8001`                                          | Server port                  |
| `API_RELOAD`          | `True`                                          | Auto-reload on code changes  |
| `API_KEY_SECRET`      | `dev-secret-key`                                | API authentication secret    |
| `CORS_ORIGINS`        | `http://localhost:5173`                         | Allowed CORS origins         |
| **Database**          |                                                 |                              |
| `AI_DATABASE_URL`     | `postgresql://...`                              | PostgreSQL connection string |
| `POSTGRES_PASSWORD`   | `postgres_password`                             | DB password (Docker only)    |
| **Logging**           |                                                 |                              |
| `LOG_LEVEL`           | `INFO`                                          | Logging verbosity            |
| `DEBUG`               | `true`                                          | Enable prompt hot-reloading  |
| **Legacy (Optional)** |                                                 |                              |
| `OLLAMA_HOST`         | `http://localhost:11434`                        | Ollama server (if used)      |
| `OLLAMA_MODEL`        | `llama3.2:1b`                                   | Ollama model                 |

### Supported GROQ Models

Only certain models support JSON schema structured outputs:

- ✅ `meta-llama/llama-4-maverick-17b-128e-instruct` (recommended)
- ✅ `llama-3.1-70b-versatile`
- ✅ `llama-3.1-8b-instant`
- ✅ `gemma2-9b-it`

---

## 📡 API Documentation

### Authentication

All endpoints (except `/health`) require API key authentication:

```bash
curl -H "X-API-Key: your-secret-key-here" http://localhost:8001/ai/sessions
```

### Core Endpoints

#### Health Check

```http
GET /health
```

Returns service and database status.

#### Create Session

```http
POST /sessions
Authorization: X-API-Key: {your-key}
Content-Type: application/json

{
  "user_id": "user123",
  "session_name": "React Learning Journey",
  "description": "Learning React from scratch"
}
```

#### Chat with AI (Streaming)

```http
POST /ai/sessions/{session_id}/chat
Authorization: X-API-Key: {your-key}
Content-Type: application/json

{
  "message": "I want to learn React, I'm a beginner"
}
```

Returns Server-Sent Events (SSE) stream:

```
event: master_prompt
data: {"message":"Great! Let me create a roadmap...","tool_calls":[...]}

event: createRoadmapSkeleton
data: {"title":"React Development Roadmap",...}

event: done
data: {"status":"complete"}
```

#### Execute Tool

```http
POST /ai/sessions/{session_id}/tools/{tool_name}
Authorization: X-API-Key: {your-key}
Content-Type: application/json

{
  "tool_arguments": {
    "goal_id": 1
  }
}
```

### Available Tools

| Tool Name                  | Description                 | Phase      | Arguments                                              |
| -------------------------- | --------------------------- | ---------- | ------------------------------------------------------ |
| `createRoadmapSkeleton`    | Generate learning roadmap   | Roadmap    | `learning_goal`, `experience_level`, `time_commitment` |
| `editRoadmapSkeleton`      | Modify existing roadmap     | Roadmap    | `roadmap_id`, `changes`                                |
| `createLearningMaterial`   | Generate study materials    | Learning   | `goal_id`                                              |
| `createQuizForGoal`        | Generate quiz               | Quiz       | `goal_id`                                              |
| `createGraduationProject`  | Generate capstone project   | Graduation | `roadmap_id`                                           |
| `evaluateGraduationAnswer` | Evaluate project submission | Graduation | `project_id`, `answer`                                 |
| `extractCVInformation`     | Parse resume PDF            | Anytime    | `pdf_base64`                                           |

### Interactive API Docs

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

---

## 🗄️ Database

### Schema Overview

**Core Tables:**

- `sessions`: User conversation sessions
- `messages`: Chat message history
- `roadmaps`: Learning roadmap definitions
- `goals`: Individual learning goals within roadmaps
- `learning_materials`: Generated study content
- `quizzes`: Quiz definitions
- `quiz_questions`: Individual quiz questions
- `quiz_attempts`: User quiz submissions
- `graduation_projects`: Capstone project definitions
- `graduation_submissions`: User project submissions

### ER Diagram (Simplified)

```
sessions (1) ─────< (M) messages
   │
   └─── (1:1) roadmaps
           │
           ├─── (1:M) goals
           │       │
           │       ├─── (1:M) learning_materials
           │       └─── (1:M) quizzes
           │
           └─── (1:1) graduation_projects
                   │
                   └─── (1:M) graduation_submissions
```

### Database Operations

**Initialize tables:**

```bash
curl http://localhost:8001/health
```

**Reset database (DANGER):**

```bash
curl http://localhost:8001/drop_db
```

**Direct database access:**

```bash
# Local
psql -U username -d dramallama_ai

# Docker
docker-compose exec postgres psql -U postgres -d dramallama_ai
```

### Migrations

Currently using auto-migration via SQLAlchemy. For production, consider Alembic:

```bash
# Initialize Alembic (future)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

---

## 🤖 AI Service Architecture

### Workflow Overview

The AI service uses a **tool-based execution model**:

1. **User sends message** → Saved to database
2. **AI Service analyzes context** → Determines phase and available tools
3. **AI returns response** → May include tool call instructions
4. **Tools execute automatically** → Results streamed back
5. **Results saved to database** → Session context updated

### Phase System

The AI operates in different phases based on session state:

| Phase          | Available Tools                                       | Trigger           |
| -------------- | ----------------------------------------------------- | ----------------- |
| **Roadmap**    | `createRoadmapSkeleton`, `editRoadmapSkeleton`        | No roadmap exists |
| **Learning**   | `createLearningMaterial`, `createQuizForGoal`         | Roadmap exists    |
| **Graduation** | `createGraduationProject`, `evaluateGraduationAnswer` | Learning complete |

### Prompt System

Prompts are defined in YAML files (`prompts/*.yaml`):

```yaml
model: "meta-llama/llama-4-maverick-17b-128e-instruct"
modelProvider: "groq"
modelProperties:
  temperature: 0.1

messages:
  - role: "system"
    content: |
      You are a Career Development AI Assistant...
      {{content}}  # Context injection point
```

**Hot-reloading**: When `DEBUG=true`, prompts reload on every request.

### Structured Outputs

All tool responses use JSON schemas defined in `utils/ai/tool_specs.py`:

```python
def get_response_schema(tool_name: str) -> Dict[str, Any]:
    """Get Pydantic schema for tool response validation."""
    schemas = {
        "createRoadmapSkeleton": RoadmapSkeletonResponse.model_json_schema(),
        "createLearningMaterial": LearningMaterialResponse.model_json_schema(),
        # ...
    }
    return schemas.get(tool_name)
```

This ensures type-safe, predictable AI outputs.

---

## 🔧 Development

### Running Locally

```bash
# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Or use the configured settings
python -c "from config import settings; import uvicorn; uvicorn.run('main:app', host=settings.api_host, port=settings.api_port, reload=settings.api_reload)"
```

### Development Mode Features

- **Auto-reload**: Code changes trigger server restart
- **Prompt hot-reloading**: YAML prompts reload without restart
- **Verbose logging**: Set `LOG_LEVEL=DEBUG` for detailed logs
- **SQL echo**: Set `SQL_ECHO=true` to log all queries

### Code Style

Follow PEP 8 and use type hints:

```python
from typing import List, Optional
from sqlalchemy.orm import Session

def get_session(db: Session, session_id: int) -> Optional[SessionModel]:
    """Retrieve session by ID."""
    return db.query(SessionModel).filter(SessionModel.id == session_id).first()
```

### Adding New Tools

1. **Define Pydantic response schema** (`models/schemas.py`):

```python
class MyToolResponse(BaseModel):
    result: str
    data: Dict[str, Any]
```

2. **Create prompt template** (`prompts/mytool.prompt.yaml`):

```yaml
model: "meta-llama/llama-4-maverick-17b-128e-instruct"
modelProvider: "groq"
messages:
  - role: "system"
    content: "Execute my tool..."
```

3. **Add tool specification** (`utils/ai/tool_specs.py`):

```python
def get_tool_definitions():
    return [
        # ...existing tools...
        {
            "type": "function",
            "function": {
                "name": "myTool",
                "description": "Does something amazing",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input": {"type": "string"}
                    },
                    "required": ["input"]
                }
            }
        }
    ]
```

4. **Implement executor** (`utils/ai/service.py`):

```python
def execute_my_tool(self, args: Dict[str, Any], db: Session) -> MyToolResponse:
    # Implementation
    return MyToolResponse(result="success", data={})
```

5. **Add route handler** (`routes/ai_actions.py`):

```python
elif tool_name == "myTool":
    result = ai_service.execute_my_tool(request.tool_arguments, db)
```

---

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies (included in requirements.txt)
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run specific test file
pytest tests/test_ai_service.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=. --cov-report=html
```

### Test Structure (TODO)

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_ai_service.py       # AI service tests
├── test_routes.py           # API endpoint tests
├── test_database.py         # CRUD operation tests
└── test_prompts.py          # Prompt loading tests
```

### Writing Tests

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

---

## 🚢 Deployment

### Production Checklist

- [ ] Set strong `API_KEY_SECRET`
- [ ] Use production-grade PostgreSQL
- [ ] Set `API_RELOAD=False`
- [ ] Configure proper `CORS_ORIGINS`
- [ ] Set `LOG_LEVEL=WARNING` or `ERROR`
- [ ] Disable `DEBUG` mode
- [ ] Set up database backups
- [ ] Configure SSL/TLS certificates
- [ ] Set up monitoring (logs, metrics)
- [ ] Use environment secrets management

### Docker Production

```bash
# Build production image
docker build -t dramallama-ai:latest .

# Run with production settings
docker run -d \
  --name dramallama-ai \
  -p 8001:8001 \
  --env-file .env.production \
  dramallama-ai:latest
```

### Environment-Specific Configs

```bash
.env.development    # Local development
.env.staging        # Staging environment
.env.production     # Production environment
```

### Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # SSE support
        proxy_buffering off;
        proxy_cache off;
        proxy_set_header Connection '';
        proxy_http_version 1.1;
        chunked_transfer_encoding off;
    }
}
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Database Connection Failed

**Error**: `could not connect to server: Connection refused`

**Solutions**:

- Verify PostgreSQL is running: `pg_isready`
- Check `AI_DATABASE_URL` in `.env`
- Ensure database exists: `psql -l | grep dramallama_ai`
- Check firewall settings

#### 2. GROQ API Errors

**Error**: `401 Unauthorized` or `Invalid API key`

**Solutions**:

- Verify `GROQ_API_KEY` is set correctly
- Check API key is active at https://console.groq.com
- Ensure no extra spaces in the key

#### 3. Tool Execution Fails

**Error**: `Tool 'xyz' returned invalid response`

**Solutions**:

- Check prompt template syntax in `prompts/`
- Verify JSON schema matches response model
- Review logs: `LOG_LEVEL=DEBUG`
- Test with simpler prompts first

#### 4. Port Already in Use

**Error**: `Address already in use`

**Solutions**:

```bash
# Find process using port 8001
lsof -i :8001

# Kill process
kill -9 <PID>

# Or use different port
API_PORT=8002 uvicorn main:app --port 8002
```

#### 5. Import Errors

**Error**: `ModuleNotFoundError: No module named 'xyz'`

**Solutions**:

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify virtual environment is activated
which python
```

### Debug Mode

Enable detailed logging:

```bash
DEBUG=true
LOG_LEVEL=DEBUG
SQL_ECHO=true
```

Then check logs for detailed stack traces.

### Health Diagnostics

```bash
# Check service health
curl http://localhost:8001/health

# Check database directly
docker-compose exec postgres psql -U postgres -d dramallama_ai -c "SELECT COUNT(*) FROM sessions;"

# View recent logs
docker-compose logs --tail=100 ai_service
```

---

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes and test**
4. **Commit**: `git commit -m "Add amazing feature"`
5. **Push**: `git push origin feature/amazing-feature`
6. **Open Pull Request**

### Code Guidelines

- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for public APIs
- Add tests for new features
- Update documentation as needed

### Commit Message Format

```
type(scope): brief description

Detailed explanation if needed

Fixes #123
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

## 📄 License

This project is part of the Drama Llama platform. See the main repository for license information.

---

## 📞 Support

- **Repository**: https://github.com/astudentinearth/drama-llama
- **Issues**: https://github.com/astudentinearth/drama-llama/issues
- **Documentation**: http://localhost:8001/docs (when running)

---

## 🙏 Acknowledgments

- **GROQ**: For providing high-performance LLM inference
- **FastAPI**: For the excellent web framework
- **SQLAlchemy**: For robust ORM capabilities
- **The Drama Llama Team**: For building an innovative learning platform

---

## 📊 Metrics & Monitoring

### Key Metrics to Track

- API response times
- GROQ API latency
- Database query performance
- Tool execution success rates
- Session creation/completion rates
- Error rates by endpoint

### Recommended Tools

- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Sentry**: Error tracking
- **PostgreSQL logs**: Query analysis

---

## 🔒 Security

### Best Practices

1. **Never commit `.env` files**
2. **Rotate API keys regularly**
3. **Use HTTPS in production**
4. **Implement rate limiting**
5. **Validate all user inputs**
6. **Keep dependencies updated**: `pip install --upgrade -r requirements.txt`
7. **Use database connection pooling** (already configured)

### Reporting Security Issues

Please report security vulnerabilities privately to the maintainers.

---

**Happy Coding! 🚀**
