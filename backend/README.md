# HRMS Lite Backend

FastAPI backend with PostgreSQL for the HRMS Lite application.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+

### Installation

```bash
pip install -r requirements.txt
```

### Environment Configuration

```bash
cp .env.example .env
```

Update `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/hrms_lite
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
DEBUG=True
```

### Run Server

```bash
uvicorn app.main:app --reload
```

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Project Structure

```
backend/
├── app/
│   ├── models/              # SQLAlchemy models
│   │   ├── employee.py      # Employee model
│   │   └── attendance.py    # Attendance model
│   ├── routes/              # API endpoints
│   │   ├── employee.py      # Employee routes
│   │   └── attendance.py    # Attendance routes
│   ├── services/            # Business logic
│   │   ├── employee_service.py
│   │   └── attendance_service.py
│   ├── config.py            # Configuration
│   ├── database.py          # PostgreSQL connection
│   └── main.py              # FastAPI application
├── requirements.txt         # Dependencies
├── runtime.txt              # Python version
├── build.sh                 # Render build script
└── .env.example
```

## 🗄️ Database

### Local PostgreSQL

```bash
# Create database
createdb hrms_lite

# Or via SQL
psql -U postgres
CREATE DATABASE hrms_lite;
```

### Tables Auto-Created
- `employees` - Employee records
- `attendance` - Attendance records

Schema is created automatically on first run.

## 📡 API Endpoints

### Employees
- `POST /api/v1/employees` - Create employee
- `GET /api/v1/employees` - Get all employees
- `GET /api/v1/employees/{id}` - Get employee
- `DELETE /api/v1/employees/{id}` - Delete employee

### Attendance
- `POST /api/v1/attendance` - Mark attendance
- `GET /api/v1/attendance` - Get all records
- `GET /api/v1/attendance?date=YYYY-MM-DD` - Filter by date
- `GET /api/v1/attendance/employee/{id}` - Employee attendance

### Health
- `GET /` - Health check

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection | `postgresql://...` |
| `CORS_ORIGINS` | Allowed origins | `http://localhost:5173` |
| `DEBUG` | Debug mode | `False` |

## ✅ Features

- ✅ **RESTful API** with FastAPI
- ✅ **Async SQLAlchemy** ORM
- ✅ **PostgreSQL** database
- ✅ **Pydantic** validation
- ✅ **Auto-generated docs** (Swagger/ReDoc)
- ✅ **CORS** configuration
- ✅ **Error handling** with proper status codes
- ✅ **Cascade deletes** for relationships
- ✅ **Comprehensive logging**

## 🚢 Deployment (Render)

### 1. Create PostgreSQL Database
- Go to Render Dashboard
- Create PostgreSQL instance
- Copy **Internal Database URL**

### 2. Create Web Service
- Connect GitHub repository
- **Root directory**: `backend`
- **Build command**: `./build.sh`
- **Start command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Environment Variables
```
DATABASE_URL=<internal-database-url>
CORS_ORIGINS=https://your-frontend.vercel.app
DEBUG=False
```

### 4. Deploy
Auto-deploys on git push

## 📚 API Documentation

Interactive API docs available at `/docs`:
- Try out endpoints
- View request/response schemas
- See example payloads

## 🔒 Security

- **Input validation**: Pydantic models
- **SQL injection prevention**: SQLAlchemy ORM
- **CORS restrictions**: Configurable origins
- **Environment variables**: Secure configuration
- **Error messages**: User-friendly (no stack traces)

## 🆘 Troubleshooting

### Database Connection Failed
- Check `DATABASE_URL` format
- Ensure PostgreSQL is running
- Verify credentials

### CORS Errors
- Add frontend URL to `CORS_ORIGINS`
- Use comma-separated list
- Include protocol (http/https)

### Tables Not Created
- Check database connection
- Tables auto-create on startup
- View logs for errors

## 📝 Development

### Hot Reload
```bash
uvicorn app.main:app --reload
```

### View Logs
Check console output for:
- Startup messages
- Request logs
- Error traces

### Database Inspection
```bash
psql -U user -d hrms_lite
\dt  # List tables
SELECT * FROM employees;
```

## 📄 License

Showcase project for FastAPI + PostgreSQL backend development.

---

**Built with** ❤️ **using FastAPI, SQLAlchemy, and PostgreSQL**
