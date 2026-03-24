# Vassouras Pernambucanas

A Django-based backend application for managing a product showcase (vitrine). This project provides a REST API and an administrative interface to manage categories and products.

## 🚀 Stack

- **Language:** Python 3.x
- **Framework:** Django 6.0.3
- **API Framework:** Django REST Framework (DRF)
- **Admin Interface:** Django Unfold
- **Database:** PostgreSQL (via `dj_database_url`)
- **Storage:** Cloudinary (Media files)
- **Static Files:** WhiteNoise
- **WSGI Server:** Gunicorn

## 📋 Requirements

- Python 3.x
- PostgreSQL database
- Cloudinary account (for media storage)

## 🛠️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd vassouras-pernambucanas
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory (or set them in your environment):
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/vassouras_db
   SECRET_KEY=your-django-secret-key
   CLOUD_NAME=your-cloudinary-name
   CLOUD_API_KEY=your-cloudinary-api-key
   CLOUD_API_SECRET=your-cloudinary-api-secret
   # For production (Render)
   RENDER=true
   RENDER_EXTERNAL_HOSTNAME=your-app.onrender.com
   ```

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser (for Admin access):**
   ```bash
   python manage.py createsuperuser
   ```

## 🏃 Running the Application

### Development Server
```bash
python manage.py runserver
```
The application will be available at `http://127.0.0.1:8000/`.

### Production
The project includes a `build.sh` script for deployment:
```bash
./build.sh
```
This script installs requirements, collects static files, and runs migrations.

## 📜 Scripts

- `python manage.py runserver`: Starts the development server.
- `python manage.py migrate`: Applies database migrations.
- `python manage.py collectstatic`: Collects static files for production.
- `python manage.py createsuperuser`: Creates an administrative user.
- `./build.sh`: Deployment build script.

## 📡 API Endpoints

The API is accessible under the `/api/` prefix:

- **Categories:** `GET /api/categorias/`
- **Products:** `GET /api/produtos/`
- **Admin Interface:** `/admin/`
- **API Auth:** `/api-auth/`

## 🧪 Tests

To run tests, use:
```bash
python manage.py test vitrine
```

## 📁 Project Structure

```text
├── core/               # Project configuration (settings, urls, wsgi/asgi)
├── vitrine/            # Main application (models, views, serializers, urls)
│   ├── migrations/     # Database migrations
│   ├── tests.py        # Application tests
│   └── ...
├── media/              # Local media storage (development only)
├── static/             # Static files
├── manage.py           # Django management script
├── build.sh            # Deployment build script
└── requirements.txt    # Project dependencies
```

## 🔑 Environment Variables (TODO)

- [ ] Define if `DEBUG` should be explicitly set via env var (currently based on `RENDER` env).
- [ ] Add `ALLOWED_HOSTS` configuration for non-Render environments.

## 📄 License

TODO: Add license information.
