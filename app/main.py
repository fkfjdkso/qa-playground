import random
import asyncio
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import engine, get_db
from app.model import Base, Location as DBLocation

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


class LocationRequest(BaseModel):
    zip: str
    city: str
    country: str
    bugs: dict


@app.get("/")
async def read_index():
    return FileResponse("app/static/index.html")


@app.post("/api/save_location")
async def save_location(data: LocationRequest, db: Session = Depends(get_db)):

    if not data.zip.strip() or not data.country.strip() or not data.city.strip():
        raise HTTPException(status_code=400, detail="Empty fields")

    if data.bugs.get("slow_db"):
        delay = random.randint(5, 40)
        print(f"sleeping for {delay}s ---")
        await asyncio.sleep(delay)

    final_city = data.city

    if data.bugs.get("data_loss"):
        final_city = final_city[:3] if final_city else ""
        print(f"truncating city to {final_city} ---")

    if not data.bugs.get("integrity"):
        exists = db.query(DBLocation).filter(DBLocation.zip == data.zip).first()
        if exists:
            raise HTTPException(status_code=400, detail="Index already exists in DB")

    try:
        new_entry = DBLocation(zip=data.zip, city=final_city, country=data.country)
        db.add(new_entry)
        db.commit()
        return {"status": "success", "message": f"Saved {data.zip}"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=409, detail="Unique Constraint Violation")


# роут для очистки
@app.delete("/api/danger/clear_db")
async def clear_db(db: Session = Depends(get_db)):
    try:
        db.query(DBLocation).delete()
        db.commit()
        return {"message": "Database cleared successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to clear DB")
