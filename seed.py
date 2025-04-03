import asyncio
from datetime import datetime, timedelta
from app.database import SessionLocal, engine
from app import models, schemas
from app.crud import create_device, create_data
import random


def seed_data():
    db = SessionLocal()

    try:
        # Создаем устройства
        devices = []
        for i in range(1, 4):
            device = models.Device(addition_time=datetime.now() - timedelta(days=i))
            db.add(device)
            devices.append(device)

        db.commit()  # Фиксируем устройства, чтобы получить их ID

        # Создаем данные для устройств
        for device in devices:
            for day in range(5):  # По 5 записей на каждое устройство
                db.add(models.Data(
                    x=random.uniform(-10, 10),
                    y=random.uniform(-5, 5),
                    z=random.uniform(0, 100),
                    time=datetime.now() - timedelta(days=day),
                    id_device=device.id
                ))

        db.commit()
        print("✅ Тестовые данные успешно добавлены")
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()