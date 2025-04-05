import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import schemas
from .database import get_db
from .crud import (
    create_device,
    get_device,
    get_devices,
    create_data_record,
    get_all_data,
    get_data_by_id,
    get_device_data,
    get_device_analysis,
    get_all_data_analysis
)


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app = FastAPI(title="Device Monitoring API", version="1.0")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "API сервиса мониторинга устройств",
            "endpoints": {
                "/devices": "Список всех устройств",
                "/devices/{id}": "Детальное описание устройства",
                "/data": "Список всех записей с данным",
                "/data/{id}": "Детальное описание записи",
                "/analysis": "Аналитика по всем устройствам",
                "/analysis/{id}": "Аналитика по устройству"
            }
        }
    )


@app.get("/devices", response_class=HTMLResponse, include_in_schema=False)
async def list_devices_html(
        request: Request,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    devices = get_devices(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "devices/list.html",
        {
            "request": request,
            "title": "Список устройств",
            "devices": devices
        }
    )


@app.get("/devices/{device_id}", response_class=HTMLResponse, include_in_schema=False)
async def get_device_html(
        request: Request,
        device_id: int,
        db: Session = Depends(get_db)
):
    device = get_device(db, device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return templates.TemplateResponse(
        "devices/detail.html",
        {
            "request": request,
            "title": f"Устройство: #{device_id}",
            "device": device
        }
    )


@app.get("/data", response_class=HTMLResponse, include_in_schema=False)
async def list_data_html(
        request: Request,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    data = get_all_data(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "data/list.html",
        {
            "request": request,
            "title": "Список всех записей с данными",
            "data": data
        }
    )


# HTML эндпоинт
@app.get("/data/{data_id}", response_class=HTMLResponse, include_in_schema=False)
async def get_data_html(
        request: Request,
        data_id: int,
        db: Session = Depends(get_db)
):
    """Получить запись данных (HTML версия)"""
    data = get_data_by_id(db, data_id=data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data record not found")

    return templates.TemplateResponse(
        "data/detail.html",
        {
            "request": request,
            "title": f"Запись с ID: #{data_id}",
            "data": data
        }
    )


@app.get("/devices/{device_id}/data", response_class=HTMLResponse, include_in_schema=False)
async def get_device_data_html(
        request: Request,
        device_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    data = get_device_data(
        db,
        device_id=device_id,
        start_time=start_time,
        end_time=end_time,
        skip=skip,
        limit=limit
    )

    device = get_device(db, device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return templates.TemplateResponse(
        "data/list.html",
        {
            "request": request,
            "title": f"Данные по устройству: #{device_id}",
            "data": data,
            "device": device
        }
    )


@app.get("/analysis", response_class=HTMLResponse)
async def get_global_analysis_html(
        request: Request,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        db: Session = Depends(get_db)
):
    """
    Получение агрегированной аналитики по всем данным (HTML страница)
    """
    analysis = get_all_data_analysis(db, start_time, end_time)
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="No data available for analysis"
        )

    return templates.TemplateResponse(
        "analysis/global.html",
        {
            "request": request,
            "analysis": analysis,
            "title": "Аналитика по всем записям",
            "start_time": start_time,
            "end_time": end_time
        }
    )


@app.get("/analysis/{device_id}", response_class=HTMLResponse, include_in_schema=False)
async def get_device_analysis_html(
        request: Request,
        device_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        db: Session = Depends(get_db)
):
    analysis = get_device_analysis(
        db,
        device_id=device_id,
        start_time=start_time,
        end_time=end_time
    )

    device = get_device(db, device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return templates.TemplateResponse(
        "analysis/result.html",
        {
            "request": request,
            "title": f"Аналитика по устройству #{device_id}",
            "device": device,
            "analysis": analysis
        }
    )


@app.post("/api/devices", response_model=schemas.DeviceResponse)
async def create_device_api(db: Session = Depends(get_db)):
    """Create a new device"""
    return create_device(db)


@app.get("/api/devices", response_model=List[schemas.DeviceResponse])
async def list_devices_api(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """List all devices"""
    return get_devices(db, skip=skip, limit=limit)


@app.get("/api/devices/{device_id}", response_model=schemas.DeviceResponse)
async def get_device_api(
        device_id: int,
        db: Session = Depends(get_db)
):
    """Get device by ID"""
    device = get_device(db, device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@app.post("/api/data", response_model=schemas.DataResponse)
async def create_data_api(
        data: schemas.DataCreate,
        db: Session = Depends(get_db)
):
    """Create new data record"""
    return create_data_record(db, data=data)


@app.get("/api/data", response_model=List[schemas.DataResponse])
async def list_data_api(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """List all data records"""
    return get_all_data(db, skip=skip, limit=limit)


@app.get("/api/data/{data_id}", response_model=schemas.DataResponse)
async def get_data_api(
    data_id: int,
    db: Session = Depends(get_db)
):
    """Получить конкретную запись данных по ID"""
    data = get_data_by_id(db, data_id=data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data record not found")
    return data


@app.get("/api/devices/{device_id}/data", response_model=List[schemas.DataResponse])
async def get_device_data_api(
        device_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """Get device data with time filter"""
    return get_device_data(
        db,
        device_id=device_id,
        start_time=start_time,
        end_time=end_time,
        skip=skip,
        limit=limit
    )


@app.get("/api/analysis", response_model=schemas.AnalysisResult)
async def get_global_analysis(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Получение агрегированной аналитики по всем данным
    Поддерживает фильтрацию по временному диапазону
    """
    return get_all_data_analysis(
        db,
        start_time=start_time,
        end_time=end_time
    )


@app.get("/api/analysis/{device_id}", response_model=schemas.AnalysisResult)
async def get_device_analysis_api(
        device_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        db: Session = Depends(get_db)
):
    """Get device analytics"""
    return get_device_analysis(
        db,
        device_id=device_id,
        start_time=start_time,
        end_time=end_time
    )
