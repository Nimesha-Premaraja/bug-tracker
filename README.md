# Bug Tracker

This Bug Tracking System is built with Python Flask and PostgreSQL, designed to streamline issue management in Software Development Life Cycle (SDLC). It features a role-based access control system that defines specific workflows for Admins, Developers, and Testers to ensure secure and organized collaboration. Users can efficiently track bugs through their entire lifecycle with integrated tools for file attachments, priority settings, and detailed commenting. Additionally, the system provides visual insights into project health via an interactive dashboard that monitors bug status distribution and recent team activity.

## Tech Stack

### Infrastructure and Platform
- **Containerization**: Docker
- **Orchestration**: Docker Compose, Kubernetes, Helm
- **Web Server**: Gunicorn

### Backend
- **Framework**: Flask 3.0.3
- **Database ORM**: Flask-SQLAlchemy
- **Database**: PostgreSQL
- **Authentication**: Flask-Login, Werkzeug
- **Forms**: WTForms
- **Validation**: email-validator

### Frontend
- **Markup**: HTML5 with Jinja2 templates
- **Styling**: CSS3 (Responsive design)
- **JavaScript**: Vanilla JS with Fetch API
- **Charts**: Chart.js 4.4.0

## Features

<details>
<summary><b>Click to extract features</b></summary>

### Authentication
- Login / Logout
- Forgot Password with reset token
- Change Password
- Session-based authentication

### User Roles & Permissions
- **Admin**: Full access to all bugs, user management
- **Developer**: Can create, edit, assign bugs and update status
- **Tester**: Can create bugs and view (read-only)

### Bug Management
- Create, Read, Update, Delete bugs
- Assign bugs to team members
- Change bug status (Open → In Progress → Closed)
- Set priority (Low, Medium, High, Critical)
- Add comments to bugs
- Track reporter and assignee

### Search & Filters
- Full-text search by title and description
- Filter by status
- Filter by assignee
- Filter by priority
- Sort by creation date
- Pagination (20 bugs per page)

### File Uploads
- Upload screenshots (PNG, JPG, GIF)
- Upload logs (TXT, LOG)
- Upload documents (PDF, DOCX)
- Max file size: 25MB per file
- Download and delete attachments

### Dashboard
- Open bugs count
- Closed bugs count
- In-progress bugs count
- Bugs by status chart (pie/doughnut)
- Bugs by priority chart (bar)
- Recent bugs activity feed

</details>

### Prerequisites
---

- Docker
- Docker Compose
- Helm
- Docker Desktop with at least 4GB memory available for the local ELK stack

### Installation & Setup

<details>
<summary><b>Local Development (Docker Compose)</b></summary>

1. Clone the repository and navigate to the bug-tracker directory:
```bash
cd apps/bug-tracker
```

2. Copy the environment file:
```bash
cp .env.example .env
```

3. Build and start the application:
```bash
docker-compose up -d --build 
```

4. Access the application:
- Frontend: http://localhost:5000
- Backend API: http://localhost:5000/api
- Database: localhost:5432
- Elasticsearch: http://localhost:9200
- Kibana: http://localhost:5601

5. Stop the application:
```bash
docker-compose down
```

6. Stop the application and remove local data volumes:
```bash
docker-compose down -v
```

</details>

<details>
<summary><b>Local Observability (ELK Stack)</b></summary>

The Docker Compose setup includes a local-only ELK stack for development log search:

- Elasticsearch stores logs at http://localhost:9200
- Kibana provides the UI at http://localhost:5601
- Filebeat collects Docker stdout/stderr logs from the `bugtracker-web` container only

The local Elasticsearch and Kibana services run with Elastic security disabled and are intended only for local development. Do not expose these ports publicly.

Application logs are emitted as JSON to stdout. Gunicorn access logs are emitted to stdout and error logs to stderr. Filebeat harvests the web container logs from Docker, enriches them with container metadata, and writes them to daily indices named `bug-tracker-logs-*`.

Start or rebuild the full local stack:

```bash
docker-compose up -d --build
```

Check service status:

```bash
docker-compose ps
```

Validate Elasticsearch health:

```bash
curl http://localhost:9200/_cluster/health?pretty
```

Open Kibana, then create a data view with this index pattern:

```text
bug-tracker-logs-*
```

Use `@timestamp` as the time field. In Discover, useful fields include `message`, `log.level`, `log.logger`, `event.dataset`, `http.request.method`, `http.response.status_code`, `url.original`, `container.name`, and `service.name`.

Generate access and application log events:

```bash
curl http://localhost:5000/
curl http://localhost:5000/health
```

Inspect indexed events directly:

```bash
curl "http://localhost:9200/bug-tracker-logs-*/_search?pretty&size=5"
```

Check Filebeat logs if events are missing:

```bash
docker-compose logs filebeat
```

User-uploaded attachments under `app/uploads`, including uploaded `.log` files, are not harvested by Filebeat.

</details>

---

### Default Credentials

Login with these credentials:

| Email | Password | Role |
|-------|----------|------|
| admin@example.com | password123 | Admin |
| dev@example.com | password123 | Developer |
| tester@example.com | password123 | Tester |

---

<details>
<summary><b>Configuration Details</b></summary>

## Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- role (admin/developer/tester)
- is_active
- reset_token (for password reset)
- reset_token_expiry
- created_at, updated_at

### Bugs Table
- id (Primary Key)
- title
- description
- status (open/in_progress/closed)
- priority (low/medium/high/critical)
- reporter_id (FK -> Users)
- assignee_id (FK -> Users)
- created_at, updated_at, closed_at

### Comments Table
- id (Primary Key)
- bug_id (FK -> Bugs)
- user_id (FK -> Users)
- body
- created_at

### Attachments Table
- id (Primary Key)
- bug_id (FK -> Bugs)
- filename
- stored_filename (unique storage name)
- file_type
- file_size
- uploaded_by (FK -> Users)
- created_at

## API Endpoints

### Authentication
- `POST /auth/login` - Login
- `GET /auth/logout` - Logout
- `GET /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset password with token
- `GET/POST /auth/change-password` - Change password

### Bugs
- `GET /bugs/` - List bugs (with filters and pagination)
- `GET /bugs/<id>` - Get bug detail
- `GET /bugs/create` - Create bug form
- `POST /bugs/create` - Create bug
- `GET /bugs/<id>/edit` - Edit bug form
- `POST /bugs/<id>/edit` - Update bug
- `POST /bugs/<id>/delete` - Delete bug
- `POST /bugs/<id>/assign` - Assign bug
- `POST /bugs/<id>/status` - Change status
- `POST /bugs/<id>/comment` - Add comment
- `POST /bugs/<id>/upload` - Upload attachment
- `POST /bugs/attachment/<id>/delete` - Delete attachment

### Dashboard
- `GET /dashboard/` - Dashboard page
- `GET /dashboard/stats` - Dashboard statistics (JSON)

### Users (Admin Only)
- `GET /users/` - List users
- `GET /users/create` - Create user form
- `POST /users/create` - Create user
- `GET /users/<id>/edit` - Edit user form
- `POST /users/<id>/edit` - Update user
- `POST /users/<id>/delete` - Delete user

## Environment Variables

```
FLASK_ENV=development                          # development, production, testing
FLASK_APP=wsgi.py
SECRET_KEY=your-secret-key-here                # Change in production!
DATABASE_URL=postgresql://user:pass@host:port/db
UPLOAD_FOLDER=app/uploads
LOG_LEVEL=INFO                                 # Python/Gunicorn log level
GUNICORN_WORKERS=1                             # Local Compose worker count
```

### Security Features

- CSRF protection with Flask-WTF
- SQL injection prevention via SQLAlchemy ORM
- XSS prevention with template escaping
- Password hashing with Werkzeug (PBKDF2)
- Password reset tokens with expiration
- File upload validation (type, size)
- Role-based access control
- Session cookie security flags
- Non-root Docker user
- Environment-based secrets

</details>

<details>
<summary><b>Troubleshooting</b></summary>

### Database Connection Error
```
Ensure PostgreSQL is running and credentials in .env are correct:
DATABASE_URL=postgresql://buguser:bugpass@db:5432/bugtracker
```

### Port Already in Use
```bash
# Change ports in docker-compose.yml
# Or kill existing processes:
lsof -i :5000  # Find process on port 5000
kill -9 <PID>  # Kill the process
```

### Permissions Error with Uploads
```
Ensure app/uploads directory exists with proper permissions:
mkdir -p app/uploads
chmod 755 app/uploads
```

### File Upload Limits

- Allowed file types: png, jpg, jpeg, gif, txt, log, pdf, docx
- Max file size: 25MB
- Max attachments per bug: Unlimited (limited by 25MB per file)

### Testing

To test the application:

1. Use default credentials to login
2. Create bugs from the dashboard
3. Assign bugs to team members
4. Test file uploads
5. Test search and filters
6. Test role permissions

### Code Validation

Run static validation commands:

```bash
ruff check .
python3 -I -m compileall -q app config.py wsgi.py gunicorn.conf.py
docker-compose config
```

### Deployment

For production deployment:

1. Update `.env` with production values
2. Set `FLASK_ENV=production`
3. Generate a strong `SECRET_KEY`
4. Use HTTPS by setting `SESSION_COOKIE_SECURE=True`
5. Configure proper database backups
6. Set up proper logging
7. Use environment secrets management

Example production deployment with nginx:

```yaml
# In docker-compose.yml, add nginx service
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
  depends_on:
    - web
```

</details>

---

```
Support: For issues and questions, please open an issue in the repository.
Author: Nimesha Premaraja
```
