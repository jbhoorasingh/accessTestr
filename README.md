# AccessTestr

This project uses Django to build a simple web application that checks if a URI is accessible and if a web page loads correctly.

## Getting started (development environment)
1. Clone repository `git clone https://github.com/jbhoorasingh/accessTestr.git`
2. Create .env files - `.app.env` and `.db.env`
3. Run docker compose up `docker-compose up`

### .db.env
``` 
POSTGRES_USER=postgres
POSTGRES_PASSWORD=ThisIsDbPassword123MustBeTheSame
POSTGRES_DB=access_testr
```

### .app.env
``` 
DB_HOST=db
DB_NAME=access_testr
DB_USER=postgres
DB_PASSWORD=ThisIsDbPassword123MustBeTheSame
DB_PORT=5432
CELERY_BROKER_URL="redis://redis:6379/0"
CELERY_RESULT_BACKEND="redis://redis:6379/0"
```

