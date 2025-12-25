
# 📄 Threat Monitoring & Alert Management – README

## 📌 Project Overview

This project is a simplified **Threat Alert Monitoring API**, built with:

* Django + Django REST Framework
* JWT Authentication
* PostgreSQL
* Docker support

It provides APIs to:

1. **Ingest security events**
2. **Automatically generate alerts** for high-severity events
3. **Allow analysts to review alerts**
4. **Allow administrators to manage alert lifecycle**

The goal is to simulate patterns you see in real SIEM / SOC tools, while demonstrating:

* good API design
* correct HTTP behavior
* security awareness
* performance-conscious modeling
* clean separation of concerns

---

## 🏗️ Architecture Overview

* Events are ingested through `/events/`
* If severity is `High` or `Critical` → an Alert is automatically created
* Analysts may read alerts
* Admins may update alert states
* Permissions enforced using Django Groups

Key concepts:

| Concept | Description                                                  |
| ------- | ------------------------------------------------------------ |
| Event   | Raw security signal coming from systems                      |
| Alert   | Derived object created only when severity warrants attention |
| Admin   | Can ingest events + update alerts                            |
| Analyst | Read-only access to alerts                                   |

---

## ⚙️ Setup Instructions (Local)

### 1️⃣ Clone repository

```bash
git clone https://github.com/<your-repo>.git
cd project
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure database

Ensure PostgreSQL is running.

Create database + user:

```sql
CREATE DATABASE DB_NAME;
CREATE USER DB_USER WITH PASSWORD 'DB_PASS';
GRANT ALL PRIVILEGES ON DATABASE DB_NAME TO DB_USER;
```

Ensure `settings.py` contains:

```python
DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "DB_NAME",
    "USER": "DB_USER",
    "PASSWORD": "DB_PASS",
    "HOST": "localhost",
    "PORT": "5432"
  }
}
```

---

### 5️⃣ Run migrations

```bash
python manage.py migrate
```

---

### 6️⃣ Create admin user

```bash
python manage.py createsuperuser
```

Then login:

```
http://127.0.0.1:8000/admin/
```

Create two groups:

```
Admin
Analyst
```

Assign users appropriately.

---

### 7️⃣ Run server

```bash
python manage.py runserver
```

---

## 🐳 Running with Docker (Optional)

Create `.env`

```
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=dev-key

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

Run:

```bash
docker compose up --build
```

Application runs at:

```
http://localhost:8000
```

---

## 🔐 Authentication

This project uses **JWT authentication (SimpleJWT)**.

### Obtain token

```
POST /api/auth/token/
```

Body:

```json
{
  "username": "<user>",
  "password": "<password>"
}
```

Use the token:

```
Authorization: Bearer <ACCESS_TOKEN>
```

---

## 📡 API Endpoints

### Events

| Method | Endpoint            | Access | Description                            |
| ------ | ------------------- | ------ | -------------------------------------- |
| GET    | `/api/events/`      | Admin  | List events (paginated)                |
| POST   | `/api/events/`      | Admin  | Create event — may auto-generate alert |
| GET    | `/api/events/{id}/` | Admin  | Retrieve event                         |

**Business rule**

> If an Event has severity `High` or `Critical`, an Alert is automatically created.

---

### Alerts

| Method | Endpoint            | Access          | Description                          |
| ------ | ------------------- | --------------- | ------------------------------------ |
| GET    | `/api/alerts/`      | Admin + Analyst | List alerts (paginated + filterable) |
| GET    | `/api/alerts/{id}/` | Admin + Analyst | View alert details                   |
| PATCH  | `/api/alerts/{id}/` | Admin only      | Update alert status                  |

Supported filters:

```
/api/alerts/?status=Open
/api/alerts/?event__severity=High
```

---

## ✔️ Functional Enhancements Implemented

### Pagination

Enabled globally using DRF `PageNumberPagination`.

### Throttling / Rate Limiting

Prevents abuse using Scoped/User throttles.

### Input Validation

Custom serializer validation ensures:

* Critical events must include meaningful description
* Alerts cannot reopen once resolved
* Required fields enforced with explanatory errors

### Error Handling

Custom global exception handler ensures consistent responses while preserving correct HTTP codes.

---

## 🌩️ Deployment Options

### Option 1 — Railway / Render

1. Push repo to GitHub
2. Create service → deploy via Docker
3. Add Postgres add-on
4. Set environment variables
5. Deploy

Both services autodetect `Dockerfile`.

---

### Option 2 — Azure VM (Ubuntu + Docker)

1. Create Ubuntu VM
2. SSH into server
3. Install Docker + Docker Compose
4. Clone repo
5. Create `.env`
6. Run:

```bash
docker compose up --build -d
```

Access:

```
http://SERVER_PUBLIC_IP:8000
```

---

## 🧠 Assumptions Made

1. Alerts exist **only** for important events
2. Role management via Django Groups is acceptable
3. API clients are technical (no UI provided)
4. No need for websocket notifications
5. In-container Postgres acceptable for test/demo — production would use managed DB

---

## 🧭 Future Improvements (if continued)

* More optimized and scalable APIs
* Pagination enhanced more to avoid the extra DB Query
* Implementation of Redis and more modular structure
* Asynchronous alert creation via Celery
* APIs for Web dashboard

---
