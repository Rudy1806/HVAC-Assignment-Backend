# HVAC Assignment Backend

Backend API for the HVAC Management System.

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd HVAC-Assignment-Backend
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file and add the required database and application settings.

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts and enter:

- Username
- Email
- Password

### 7. Start Development Server

```bash
python manage.py runserver
```

The backend will be available at:

```text
http://127.0.0.1:8000/
```

### 8. Access Django Admin

```text
http://127.0.0.1:8000/admin/
```

Login using the superuser credentials created in Step 6.

## API Documentation

Refer to the project source code and API routes for available endpoints.

## Notes

- Ensure PostgreSQL is running before starting the application.
- Run migrations whenever database schema changes are made.
- Create a superuser to access the admin panel.
