from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DeviceBase(BaseModel):
    """Базовая схема устройства"""

    class Config:
        from_attributes = True


class DataBase(BaseModel):
    """Базовая схема данных"""

    class Config:
        from_attributes = True


class DeviceCreate(DeviceBase):
    """Схема для создания устройства"""


class DataCreate(DataBase):
    """Схема для создания записи данных"""
    x: float
    y: float
    z: float
    id_device: int
    time: Optional[datetime] = None


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


class AnalysisResult(BaseModel):
    """Схема результата анализа"""
    min_x: Optional[float] = 0.0
    max_x: Optional[float] = 0.0
    avg_x: Optional[float] = 0.0
    sum_x: Optional[float] = 0.0
    median_x: Optional[float] = 0.0

    min_y: Optional[float] = 0.0
    max_y: Optional[float] = 0.0
    avg_y: Optional[float] = 0.0
    sum_y: Optional[float] = 0.0
    median_y: Optional[float] = 0.0

    min_z: Optional[float] = 0.0
    max_z: Optional[float] = 0.0
    avg_z: Optional[float] = 0.0
    sum_z: Optional[float] = 0.0
    median_z: Optional[float] = 0.0

    total_count: Optional[int] = None
