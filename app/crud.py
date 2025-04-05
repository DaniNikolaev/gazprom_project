from datetime import datetime
from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas


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


def calculate_median(values: List[float]) -> Optional[float]:
    """Вычисление медианы списка значений"""
    if not values:
        return None
    sorted_values = sorted(values)
    n = len(sorted_values)
    if n % 2 == 0:
        mid1 = sorted_values[n // 2 - 1]
        mid2 = sorted_values[n // 2]
        median = (mid1 + mid2) / 2
    else:
        median = sorted_values[n // 2]
    return median


def get_device_analysis(
        db: Session,
        device_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
) -> schemas.AnalysisResult:
    """Аналитика данных устройства"""
    data = get_device_data(db, device_id, start_time, end_time)
    if not data:
        raise HTTPException(status_code=404, detail="No data found for this device and time range")

    x_values = [item.x for item in data]
    y_values = [item.y for item in data]
    z_values = [item.z for item in data]
    total_count = len(data)

    analysis_result = schemas.AnalysisResult(
        min_x=min(x_values) if x_values else None,
        max_x=max(x_values) if x_values else None,
        avg_x=sum(x_values) / len(x_values) if x_values else None,
        sum_x=sum(x_values) if x_values else None,
        median_x=calculate_median(x_values),

        min_y=min(y_values) if y_values else None,
        max_y=max(y_values) if y_values else None,
        avg_y=sum(y_values) / len(y_values) if y_values else None,
        sum_y=sum(y_values) if y_values else None,
        median_y=calculate_median(y_values),

        min_z=min(z_values) if z_values else None,
        max_z=max(z_values) if z_values else None,
        avg_z=sum(z_values) / len(z_values) if z_values else None,
        sum_z=sum(z_values) if z_values else None,
        median_z=calculate_median(z_values),

        total_count=total_count
    )
    return analysis_result


def get_all_data_analysis(
        db: Session,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
) -> schemas.AnalysisResult:
    """Аналитика по всем устройствам"""

    query = db.query(models.Data)

    if start_time:
        query = query.filter(models.Data.time >= start_time)
    if end_time:
        query = query.filter(models.Data.time <= end_time)

    data = query.all()

    if not data:
        raise HTTPException(status_code=404, detail="No data found")

    x_values = [item.x for item in data]
    y_values = [item.y for item in data]
    z_values = [item.z for item in data]
    total_count = len(data)

    analysis_result = schemas.AnalysisResult(
        min_x=min(x_values) if x_values else None,
        max_x=max(x_values) if x_values else None,
        avg_x=sum(x_values) / len(x_values) if x_values else None,
        sum_x=sum(x_values) if x_values else None,
        median_x=calculate_median(x_values),

        min_y=min(y_values) if y_values else None,
        max_y=max(y_values) if y_values else None,
        avg_y=sum(y_values) / len(y_values) if y_values else None,
        sum_y=sum(y_values) if y_values else None,
        median_y=calculate_median(y_values),

        min_z=min(z_values) if z_values else None,
        max_z=max(z_values) if z_values else None,
        avg_z=sum(z_values) / len(z_values) if z_values else None,
        sum_z=sum(z_values) if z_values else None,
        median_z=calculate_median(z_values),

        total_count=total_count
    )
    return analysis_result
