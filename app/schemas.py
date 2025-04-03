from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# Базовые схемы
class DeviceBase(BaseModel):
    """Базовая схема устройства"""

    class Config:
        from_attributes = True  # Позволяет работать с ORM (ранее orm_mode=True)


class DataBase(BaseModel):
    """Базовая схема данных"""

    class Config:
        from_attributes = True


# Схемы для создания (Create)
class DeviceCreate(DeviceBase):
    """Схема для создания устройства"""
    pass  # Можно добавить дополнительные поля при необходимости


class DataCreate(DataBase):
    """Схема для создания записи данных"""
    x: float
    y: float
    z: float
    id_device: int
    time: Optional[datetime] = None  # Если не указано, будет использовано текущее время


# Схемы для ответов (Response)
class DeviceResponse(DeviceBase):
    """Схема ответа с информацией об устройстве"""
    id: int
    addition_time: datetime


class DataResponse(DataBase):
    """Схема ответа с информацией о данных"""
    id: int
    x: float
    y: float
    z: float
    time: datetime
    id_device: int


# Схемы для аналитики
class AnalysisResult(BaseModel):
    """Схема результата анализа"""
    min_x: Optional[float] = None
    max_x: Optional[float] = None
    avg_x: Optional[float] = None
    sum_x: float
    median_x: Optional[float] = None

    min_y: Optional[float] = None
    max_y: Optional[float] = None
    avg_y: Optional[float] = None
    sum_y: float
    median_y: Optional[float] = None

    min_z: Optional[float] = None
    max_z: Optional[float] = None
    avg_z: Optional[float] = None
    sum_z: float
    median_z: Optional[float] = None

    total_count: Optional[int] = None



