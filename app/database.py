from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Формат подключения к SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"  # Файл БД будет создан в той же директории

# Создаем движок SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Нужно только для SQLite
)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def get_db():
    """
    Генератор сессий БД для dependency injection в FastAPI.
    Использование:
    db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Функция для инициализации БД (создание таблиц).
    Можно вызывать при старте приложения.
    """
    Base.metadata.create_all(bind=engine)