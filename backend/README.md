# Baynext API

A FastAPI-based backend service for managing Marketing Mix Modeling (MMM) datasets, jobs, and pipelines. This API provides endpoints for dataset management, pipeline execution, and analytics for marketing attribution modeling.

## 🚀 Features

- **Dataset Management**: Upload, validate, and manage marketing datasets
- **Pipeline Orchestration**: Create and execute MMM analysis pipelines
- **Job Monitoring**: Track the status and progress of analytical jobs
- **User Authentication**: Secure API access with JWT tokens
- **Database Integration**: PostgreSQL with SQLModel ORM
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.115+
- **Database**: PostgreSQL with SQLModel
- **Authentication**: JWT with python-jose
- **File Storage**: Vercel Blob integration
- **Analytics Engine**: Google Meridian
- **Testing**: pytest with async support
- **Linting**: Ruff
- **Dependency Management**: uv

## 📋 Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- PostgreSQL database
- Environment variables configured (see `.env` setup below)

## 🏃‍♂️ Quick Start

### 1. Install Dependencies

```bash
# Install all dependencies
make install

# Or directly with uv
uv sync
```

### 2. Environment Setup

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/baynext_dev

# Authentication
ML_API_SECRET_API_KEY=your-secret-api-key-here
AUTH_SECRET=your-auth-secret-here

# Blob Storage
BLOB_READ_WRITE_TOKEN=your-vercel-blob-token
```

### 3. Database Setup

```bash
# Run database migrations
uv run alembic upgrade head

# Seed with sample data for development
make seed
```

### 4. Start Development Server

```bash
# Start the development server
make run

# Or directly with uv
uv run fastapi dev app/main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/v1/health

## 📜 Available Commands

Use `make help` to see all available commands:

### Development Server
```bash
make run          # Start development server
make run-prod     # Start production server
```

### Database Operations
```bash
make seed         # Seed database with sample data
make seed-fresh   # Clear and seed with fresh data
make clear        # Clear all seed data
make reset        # Reset database (clear + seed)
```

### Testing & Quality
```bash
make test         # Run tests
make test-cov     # Run tests with coverage report
make lint         # Run linting checks
make lint-fix     # Run linting and fix issues
```

### Dependency Management
```bash
make install      # Install/sync dependencies
```

## 🗄️ Database Seeding

The project includes a comprehensive seeding system for local development:

### Sample Data

The seeding system creates:

- **4 Sample Users**:
  - John Doe (john.doe@example.com)
  - Jane Smith (jane.smith@example.com)
  - Mike Johnson (mike.johnson@example.com)
  - Sarah Wilson (sarah.wilson@example.com)

- **3 Sample Projects**:
  - E-commerce MMM Campaign
  - Brand Awareness Study
  - Holiday Campaign 2024

- **3 Sample Datasets**:
  - Q3 Media Performance Data
  - Historical Sales Data
  - Brand Tracking Survey

### CLI Usage

#### Using Make (Recommended)
```bash
make seed         # Seed with sample data
make seed-fresh   # Clear existing data and seed fresh
make clear        # Clear all seed data
make reset        # Full reset (clear + seed)
```

#### Using uv directly
```bash
uv run python scripts/cli.py seed          # Basic seeding
uv run python scripts/cli.py seed --clear  # Clear then seed
uv run python scripts/cli.py clear         # Clear data only
uv run python scripts/cli.py reset         # Full reset
```

#### Using the convenience script
```bash
./scripts/db seed          # Basic seeding
./scripts/db seed --clear  # Clear then seed
./scripts/db clear         # Clear data only
./scripts/db reset         # Full reset
```

### CLI Features

- 🎨 **Rich output** with colors and emojis
- ✅ **Confirmation prompts** for destructive operations
- 📝 **Detailed logging** with timestamps
- 🔒 **Safe operations** - won't create duplicates
- 🚨 **Error handling** with proper exit codes

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
make test

# Run with coverage report
make test-cov

# Run specific test file
uv run pytest tests/test_security.py

# Run specific test
uv run pytest tests/test_security.py::test_check_token_valid
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/v1/           # API endpoints
│   ├── core/             # Core functionality (db, security, settings)
│   ├── schemas/          # SQLModel schemas/models
│   ├── services/         # Business logic services
│   ├── tasks/            # Background tasks
│   ├── utils/            # Utility functions
│   └── validations/      # Data validation schemas
├── scripts/
│   ├── cli.py           # Database management CLI
│   ├── db               # Convenience script wrapper
│   └── seed.py          # Seeding functions
├── tests/               # Test suite
├── Makefile             # Development commands
├── pyproject.toml       # Dependencies and config
└── README.md           # This file
```

## 🔧 API Endpoints

### Health Check
- `GET /v1/health` - Service health status

### Authentication
- `GET /v1/me` - Get current user info

### Projects & Datasets
- `GET /v1/projects/{project_id}/datasets` - List project datasets
- `GET /v1/projects/{project_id}/datasets/{dataset_id}` - Get dataset details

### Jobs & Pipelines
- `GET /v1/projects/{project_id}/jobs` - List project jobs
- `GET /v1/projects/{project_id}/pipelines` - List project pipelines

## 🔐 Authentication

The API uses Bearer token authentication. Include your token in the Authorization header:

```bash
curl -H "Authorization: Bearer your-token-here" http://localhost:8000/v1/me
```

## 🌍 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `ML_API_SECRET_API_KEY` | Secret key for API authentication | Yes |
| `AUTH_SECRET` | Secret for JWT token signing | Yes |
| `BLOB_READ_WRITE_TOKEN` | Vercel Blob storage token | Yes |

## 🚀 Deployment

### Production Build
```bash
make run-prod
```

### Docker (if using)
```bash
docker build -t baynext-api .
docker run -p 8000:8000 baynext-api
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `make test`
5. Run linting: `make lint-fix`
6. Commit your changes: `git commit -am 'Add feature'`
7. Push to the branch: `git push origin feature-name`
8. Submit a pull request

## 📝 Development Workflow

1. **Start with fresh data**:
   ```bash
   make seed-fresh
   ```

2. **Make changes to your code**

3. **Run tests**:
   ```bash
   make test
   ```

4. **Check code quality**:
   ```bash
   make lint-fix
   ```

5. **Test the API**:
   ```bash
   make run
   # Visit http://localhost:8000/docs
   ```

## 🆘 Troubleshooting

### Database Connection Issues
- Check your `DATABASE_URL` in `.env`
- Ensure PostgreSQL is running
- Verify database credentials

### Import Errors
- Run `make install` to sync dependencies
- Check Python version (requires 3.12+)

### Seeding Issues
- Check database connectivity
- Ensure migrations are up to date: `uv run alembic upgrade head`
- Clear existing data: `make clear`

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Typer Documentation](https://typer.tiangolo.com/)

---

**Happy coding! 🎉**
