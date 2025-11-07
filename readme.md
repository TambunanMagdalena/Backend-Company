Company - Backend API
Backend REST API untuk sistem informasi sebuah company yang dibangun dengan python Flask, SQL Server, dan Redis. Menyediakan endpoints untuk manajemen data cities dan mendukung frontend Vue.js modern.

🛠 Tech Stack

- Framework: Flask 2.3.2
- Database: SQL Server dengan SQLAlchemy ORM
- Caching: Redis untuk optimalisasi performa
- Migrations: Flask-Migrate dengan Alembic
- CORS: Flask-CORS untuk frontend integration
- Environment: python-dotenv

📋 Prerequisites

- Python 3.9+
- SQL Server (localhost atau cloud)
- Redis Server
- Git
- Postman

🚀 Installation & Setup

1. Clone Repository
   git clone <repository-url>
   cd moonlay-boilerplate-python

2. Setup Virtual Environment

# Windows

python -m venv venv
.\venv\Scripts\activate

# macOS/Linux

python -m venv venv
source venv/bin/activate

3. Install Dependencies
   pip install -r requirements.txt

4. Environment Configuration

Buat file .env di root directory:

# Flask Configuration

FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
PORT=5000

# Database Configuration (SQL Server)

DB_HOST=localhost
DB_PORT=1433
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database_name

# Redis Configuration

REDIS_URL=redis://localhost:6379/0

# Alternative: Direct Database URL

DATABASE_URL=mssql+pyodbc://username:password@host:port/database?driver=ODBC+Driver+17+for+SQL+Server

5. Database Setup

# Initialize migrations (jika pertama kali)

flask db init

# Create migration script

flask db migrate -m "Initial migration"

# Apply migrations

flask db upgrade

🏃‍♂️ Running the Application
Development Mode
flask run
Production Mode
python run.py

📚 API Endpoints
![alt text](image.png)

Database Models
City Model
{
"id": Integer (Primary Key),
"name": String(100),
"country": String(100)
}

Redis Caching
Response Format
{
"status": "success",
"message": "Request successful",
"data": [...],
"page": 1,
"page_size": 10,
"pages": 5,
"total": 50
}

author: Magdalena Pebrianty Tambunan
