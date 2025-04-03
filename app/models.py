from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base  # Предполагается, что Base - это declarative_base()


class Device(Base):
    """Модель устройства"""
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, index=True)
    addition_time = Column(DateTime, default=datetime.utcnow)

    # Связь один-ко-многим с данными
    data_records = relationship("Data", back_populates="device")

    def __repr__(self):
        return f"<Device(id={self.id}, addition_time={self.addition_time})>"


class Data(Base):
    """Модель данных устройства"""
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    time = Column(DateTime, default=datetime.utcnow)
    id_device = Column(Integer, ForeignKey('devices.id'))

    # Связь многие-к-одному с устройством
    device = relationship("Device", back_populates="data_records")

    def __repr__(self):
        return f"<Data(id={self.id}, x={self.x}, y={self.y}, z={self.z}, time={self.time})>"


# Pydantic модели для запросов и ответов API
from pydantic import BaseModel


class DeviceBase(BaseModel):
    """Базовая модель устройства"""

    class Config:
        from_attributes = True


class DeviceCreate(DeviceBase):
    """Модель для создания устройства"""
    pass  # Можно добавить дополнительные поля при необходимости


class DeviceResponse(DeviceBase):
    """Модель ответа с информацией об устройстве"""
    id: int
    addition_time: datetime


class DataBase(BaseModel):
    """Базовая модель данных"""

    class Config:
        from_attributes = True


class DataCreate(DataBase):
    """Модель для создания записи данных"""
    x: float
    y: float
    z: float
    id_device: int
    time: Optional[datetime] = None


class DataResponse(DataBase):
    """Модель ответа с информацией о данных"""
    id: int
    x: float
    y: float
    z: float
    time: datetime
    id_device: int


class AnalysisResult(BaseModel):
    """Модель результата анализа"""
    min: float
    max: float
    count: int
    sum: float
    median: float