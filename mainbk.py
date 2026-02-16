from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

import model
from database import engine, SessionLocal
from schemas import DestinationCreate

# Create tables
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Travel API Running"}


@app.get("/destinations")
def get_destinations(db: Session = Depends(get_db)):
    return db.query(model.Destination).all()


@app.post("/destinations")
def create_destinations(
    destination: DestinationCreate,
    db: Session = Depends(get_db)
):
    new_destination = model.Destination(
        name=destination.name,
        city=destination.city,
        category=destination.category,
        rating=destination.rating
    )

    db.add(new_destination)
    db.commit()
    db.refresh(new_destination)

    return new_destination

@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    new_user = model.User(username=username, password=password)

    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")

    return {"message": "Registered successfully"}


@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(
        model.User.username == username
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.password != password:
        raise HTTPException(status_code=401, detail="Password mismatch")

    return {"message": "Logged in successfully"}

favorites = {}


@app.post("/favorites/{destination_id}")
def add_favorite(destination_id: int, username: str):
    if username not in favorites:
        favorites[username] = []

    favorites[username].append(destination_id)

    return {"message": "Added to favorites"}


@app.get("/favorites/{username}")
def get_favorites(username: str):
    if username not in favorites:
        return []

    return favorites[username]

@app.get("/destinations/search")
def search_for_destinations(q: str,db: Session = Depends(get_db)):
    results = db.query(model.Destination).filter( or_(
        model.Destination.name.ilike(f"%{q}%"),
        model.Destination.category.ilike(f"%{q}%"),
        model.Destination.city.ilike(f"%{q}%")
    )
    ).all()
    return results

