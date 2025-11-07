from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis
import os

db = SQLAlchemy()
migrate = Migrate()
redis_client = None

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Konfigurasi database dari environment variables
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        # Build dari komponen terpisah
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_name = os.getenv('DB_NAME')
        
        database_url = f"mssql+pyodbc://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['FLASK_ENV'] = os.getenv('FLASK_ENV')
    
    # 🔥 FIX CORS - Allow all origins for development
    CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"], supports_credentials=True)

    # Initialize Redis
    setup_redis(app)
    
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app.routes import bp
        app.register_blueprint(bp)

    return app

def setup_redis(app):
    """Setup Redis connection"""
    global redis_client
    
    try:
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        redis_client = redis.Redis.from_url(
            redis_url,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_keepalive=True
        )
        
        # Test connection
        redis_client.ping()
        print("✅ Redis connected successfully!")
        
    except redis.ConnectionError as e:
        print(f"❌ Redis connection failed: {e}")
        redis_client = None
    except Exception as e:
        print(f"❌ Redis error: {e}")
        redis_client = None

def get_redis():
    """Get Redis client instance"""
    return redis_client