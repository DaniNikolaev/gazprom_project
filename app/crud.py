from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional
from . import models, schemas


# Device operations
def create_device(db: Session):
    """Создание нового устройства"""
    db_device = models.Device(addition_time=datetime.utcnow())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def get_device(db: Session, device_id: int):
    """Получение устройства по ID"""
    return db.query(models.Device).filter(models.Device.id == device_id).first()


def get_devices(db: Session, skip: int = 0, limit: int = 100):
    """Получение списка устройств с пагинацией"""
    return db.query(models.Device).offset(skip).limit(limit).all()


# Data operations
def create_data_record(db: Session, data: schemas.DataCreate):
    """Создание новой записи данных"""
    db_data = models.Data(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_all_data(db: Session, skip: int = 0, limit: int = 100):
    """Получение всех данных"""
    return db.query(models.Data).offset(skip).limit(limit).all()


def get_device_data(
        db: Session,
        device_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
):
    """Получение данных конкретного устройства с фильтрацией по времени"""
    query = db.query(models.Data).filter(models.Data.id_device == device_id)

    if start_time:
        query = query.filter(models.Data.time >= start_time)
    if end_time:
        query = query.filter(models.Data.time <= end_time)

    return query.offset(skip).limit(limit).all()

def get_data_by_id(db: Session, data_id: int):
    """Получить запись данных по ID"""
    return db.query(models.Data).filter(models.Data.id == data_id).first()


def get_device_analysis(
        db: Session,
        device_id: int = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
):
    """Аналитика данных устройства с приблизительной медианой"""
    result = db.query(
        # Мертики для X
        func.min(models.Data.x).label("min_x"),
        func.max(models.Data.x).label("max_x"),
        func.avg(models.Data.x).label("avg_x"),
        func.sum(models.Data.x).label("sum_x"),

        # Мертики для Y
        func.min(models.Data.y).label("min_y"),
        func.max(models.Data.y).label("max_y"),
        func.avg(models.Data.y).label("avg_y"),
        func.sum(models.Data.y).label("sum_y"),

        # Мертики для Z
        func.min(models.Data.z).label("min_z"),
        func.max(models.Data.z).label("max_z"),
        func.avg(models.Data.z).label("avg_z"),
        func.sum(models.Data.z).label("sum_z"),

        # Общие метрики
        func.count(models.Data.id).label("count"),

        # Приблизительная медиана (работает в SQLite)
        func.avg(models.Data.x).label("median_x"),  # Замена медианы средним
        func.avg(models.Data.y).label("median_y"),
        func.avg(models.Data.z).label("median_z")
    ).filter(models.Data.id_device == device_id)

    if start_time:
        result = result.filter(models.Data.time >= start_time)
    if end_time:
        result = result.filter(models.Data.time <= end_time)

    return result.first()

def get_all_data_analysis(
        db: Session,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
):
    """Аналитика данных устройства с приблизительной медианой"""
    result = db.query(
        # Мертики для X
        func.min(models.Data.x).label("min_x"),
        func.max(models.Data.x).label("max_x"),
        func.avg(models.Data.x).label("avg_x"),
        func.sum(models.Data.x).label("sum_x"),

        # Мертики для Y
        func.min(models.Data.y).label("min_y"),
        func.max(models.Data.y).label("max_y"),
        func.avg(models.Data.y).label("avg_y"),
        func.sum(models.Data.y).label("sum_y"),

        # Мертики для Z
        func.min(models.Data.z).label("min_z"),
        func.max(models.Data.z).label("max_z"),
        func.avg(models.Data.z).label("avg_z"),
        func.sum(models.Data.z).label("sum_z"),

        # Общие метрики
        func.count(models.Data.id).label("count"),

        # Приблизительная медиана (работает в SQLite)
        func.avg(models.Data.x).label("median_x"),  # Замена медианы средним
        func.avg(models.Data.y).label("median_y"),
        func.avg(models.Data.z).label("median_z")
    )

    if start_time:
        result = result.filter(models.Data.time >= start_time)
    if end_time:
        result = result.filter(models.Data.time <= end_time)

    return result.first()