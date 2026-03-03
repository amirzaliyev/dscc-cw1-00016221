# Sales Manager

A Django web application for managing sales orders, customers, and products. Built with Django 6.0, PostgreSQL, Nginx, and deployed using Docker on an Eskiz cloud server with HTTPS.

## Features

- User authentication (login, logout, registration)
- Order management with full CRUD operations
- Inline order items with dynamic row addition
- Auto-calculated order totals
- Customer management with VIP flag
- Product catalogue with tag support
- Admin panel for managing all models
- PostgreSQL database with persistent storage
- Dockerized multi-service architecture (Django, PostgreSQL, Nginx, Certbot)
- HTTPS with Let's Encrypt via Certbot
- Production-ready with Gunicorn

## Technologies

- **Backend:** Django 6.0, Python 3.13
- **Database:** PostgreSQL 16
- **Web Server:** Gunicorn
- **Reverse Proxy / SSL:** Nginx + Certbot (Let's Encrypt)
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions

## Database Schema

```
Customer
├── full_name (CharField)
├── phone_number (CharField)
└── is_vip (BooleanField)

Tag
└── name (CharField)

Product
├── name (CharField)
├── sku_code (CharField)
└── tags (ManyToManyField → Tag)

Order
├── total_amount (DecimalField, auto-calculated)
├── created_at (DateTimeField)
└── customer (FK → Customer)

OrderItem
├── product (FK → Product)
├── order (FK → Order)
├── quantity (IntegerField)
└── price (DecimalField)
```

**Relationships:**
- Customer → Order: one-to-many
- Order → OrderItem: one-to-many
- Product → OrderItem: many-to-one
- Product ↔ Tag: many-to-many

## Screenshots

<!-- Add screenshots of the running application here -->

## Local Setup

### Prerequisites

- Python 3.13+
- PostgreSQL 16
- Docker & Docker Compose (for containerized setup)

### Development (without Docker)

1. Clone the repository:
   ```bash
   git clone https://github.com/amirzaliyev/DSCC_CW1_00016221.git
   cd DSCC_CW1_00016221
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```

3. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   Fill in the database credentials (see [Environment Variables](#environment-variables)).

4. Create a `.env.postgres` file from the example:
   ```bash
   cp .env.postgres.example .env.postgres
   ```

5. Run migrations:
   ```bash
   cd backend
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Development (with Docker)

1. Create `.env` and `.env.postgres` files from the examples and fill in credentials.

2. Build and start the services:
   ```bash
   docker compose up --build
   ```

The application will be available at `http://localhost:8000`.

## Deployment

### Server Requirements

- Docker and Docker Compose installed
- Domain pointing to server IP
- Ports 22, 80, and 443 open (UFW)

### Steps

1. SSH into the server and clone the repository:
   ```bash
   git clone https://github.com/amirzaliyev/DSCC_CW1_00016221.git ~/projects/dscc-cw1-00016221
   cd ~/projects/dscc-cw1-00016221
   ```

2. Create `.env` and `.env.postgres` with production credentials:
   ```bash
   cp .env.example .env
   cp .env.postgres.example .env.postgres
   # Edit both files with production values
   ```

3. Start PostgreSQL and the web service first:
   ```bash
   docker compose up -d postgresql web
   ```

4. Obtain the SSL certificate (Nginx must not be running yet):
   ```bash
   # Use a temporary HTTP-only Nginx config, then run certbot:
   docker compose up -d nginx
   docker compose run --rm certbot
   ```

5. Restart Nginx to load the certificate:
   ```bash
   docker compose restart nginx
   ```

6. Create a superuser:
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

The application is accessible at `https://16221.wiut911.uz`.

## Environment Variables

### `.env` (Django application)

| Variable               | Description                       | Example                              |
|------------------------|-----------------------------------|--------------------------------------|
| `SECRET_KEY`           | Django secret key                 | `your-secret-key`                    |
| `DEBUG`                | Debug mode (False in production)  | `false`                              |
| `ALLOWED_HOSTS`        | Comma-separated allowed hosts     | `16221.wiut911.uz,localhost`         |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins for CSRF          | `https://16221.wiut911.uz`           |
| `DB_ENGINE`            | Django database backend           | `django.db.backends.postgresql`      |
| `DB_USER`              | Database username                 | `sales_user`                         |
| `DB_PASSWORD`          | Database password                 | `your_secure_password`               |
| `DB_HOST`              | Database host (container name)    | `postgresql`                         |
| `DB_PORT`              | Database port                     | `5432`                               |
| `DB_NAME`              | Database name                     | `sales_db`                           |

### `.env.postgres` (PostgreSQL container)

| Variable            | Description         | Example                |
|---------------------|---------------------|------------------------|
| `POSTGRES_USER`     | PostgreSQL username  | `sales_user`           |
| `POSTGRES_PASSWORD` | PostgreSQL password  | `your_secure_password` |
| `POSTGRES_DB`       | PostgreSQL database  | `sales_db`             |

## Project Structure

```
dscc-cw1-00016221/
├── backend/                 # Django project root
│   ├── config/              # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── sales/               # Main application
│   │   ├── admin.py         # Admin panel configuration
│   │   ├── forms.py         # Order and registration forms
│   │   ├── models.py        # Database models
│   │   ├── urls.py          # App URL routing
│   │   ├── views.py         # View functions
│   │   ├── static/sales/    # CSS
│   │   └── templates/sales/ # App templates
│   ├── templates/           # Global templates (base, auth)
│   ├── static_files/        # Collected static files
│   ├── Dockerfile           # Multi-stage Docker build
│   ├── manage.py
│   └── requirements.txt
├── nginx/
│   └── nginx.conf           # Nginx reverse proxy config
├── docker-compose.yaml      # Service orchestration
├── .env.example             # Environment variable template
├── .env.postgres.example    # PostgreSQL env template
└── .github/
    └── workflows/
        └── deploy.yaml      # CI/CD pipeline
```
