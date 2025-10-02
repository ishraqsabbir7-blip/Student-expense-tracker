# config.py

class Config:
    # MySQL database connection URI
    # Format: 'mysql+pymysql://username:password@host/database_name'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:rafsan@127.0.0.1/student_expenses'
    
    # Disable SQLAlchemy event system to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False


