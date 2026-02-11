# Sales Manager

A Django web application for managing sales orders, customers, and products. Built with Django 6.0, PostgreSQL, and deployed using Docker with Traefik as a reverse proxy.

## Features

- User authentication (login, logout, registration)
- Order management with full CRUD operations
- Inline order items with dynamic row addition
- Auto-calculated order totals
- Admin panel for managing customers, products, and orders
- PostgreSQL database
- Dockerized multi-service architecture (Django, PostgreSQL, Traefik)
- HTTPS with Let's Encrypt via Traefik
- Production-ready with Gunicorn

## Technologies

- **Backend:** Django 6.0, Python 3.13
- **Database:** PostgreSQL 16
- **Web Server:** Gunicorn
- **Reverse Proxy / SSL:** Traefik v3.6 with Let's Encrypt
- **Containerization:** Docker, Docker Compose
- **Static Files:** WhiteNoise

## Database Schema

```
Customer
├── full_name (CharField)
├── phone_number (CharField)
└── is_vip (BooleanField)

Product
├── name (CharField)
└── sku_code (CharField)

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
- Product → OrderItem: one-to-many

## Local Setup

### Prerequisites

- Python 3.13+
- PostgreSQL 16
- Docker & Docker Compose (for containerized setup)

### Development (without Docker)

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/DSCC_CW1_00016221.git
   cd DSCC_CW1_00016221
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
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

3. Run migrations:
   ```bash
   docker compose exec web python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

The application will be available at `http://localhost:8000`.

## Deployment

### Server Requirements

- Docker and Docker Compose installed
- Domain pointing to server IP
- Ports 80 and 443 open

### Steps

1. SSH into the server and clone the repository.

2. Create `.env` and `.env.postgres` with production credentials.

3. Start the services:
   ```bash
   docker compose up -d --build
   ```

4. Run migrations and collect static files:
   ```bash
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py collectstatic --noinput
   ```

5. Create a superuser:
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

Traefik handles SSL certificates automatically via Let's Encrypt. The application is accessible at `https://16221.wiut911.uz`.

## Environment Variables

### `.env` (Django application)

| Variable      | Description                       | Example                              |
|---------------|-----------------------------------|--------------------------------------|
| `DB_ENGINE`   | Django database backend           | `django.db.backends.postgresql`      |
| `DB_USER`     | Database username                 | `sales_user`                         |
| `DB_PASSWORD` | Database password                 | `your_secure_password`               |
| `DB_HOST`     | Database host                     | `postgresql`                         |
| `DB_PORT`     | Database port                     | `5432`                               |
| `DB_NAME`     | Database name                     | `sales_db`                           |

### `.env.postgres` (PostgreSQL container)

| Variable            | Description         | Example                |
|---------------------|---------------------|------------------------|
| `POSTGRES_USER`     | PostgreSQL username  | `sales_user`           |
| `POSTGRES_PASSWORD` | PostgreSQL password  | `your_secure_password` |
| `POSTGRES_DB`       | PostgreSQL database  | `sales_db`             |

## Project Structure

```
DSCC_CW1_00016221/
├── config/                  # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── sales/                   # Main application
│   ├── admin.py             # Admin panel configuration
│   ├── forms.py             # Order and registration forms
│   ├── models.py            # Database models
│   ├── urls.py              # App URL routing
│   ├── views.py             # View functions
│   ├── static/sales/        # CSS
│   └── templates/sales/     # App templates
├── templates/               # Global templates (base, auth)
├── staticfiles/             # Collected static files
├── Dockerfile               # Multi-stage Docker build
├── docker-compose.yaml      # Service orchestration
├── traefik.yaml             # Traefik reverse proxy config
├── requirements.txt         # Python dependencies
└── manage.py
```

## Screenshots

<!-- Add screenshots of the running application here -->
