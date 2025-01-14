# Create an expense tracker that allows users to track their expenses. The service should have the following features:
# User Authentication, User Signup (/register), User Login (/login), JWT Token Generation & Validation, User Session Management, Expense Management:
# Add a New Expense, Remove an Expense, Update an Expense, List Past Expenses, Filter by(Last week, Last month, Last 3 months,Custom date range)

import os 
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError 
import jwt
import cjson as json
import json

app = FastAPI()

# Database Setup
DATABASE_URL = "sqlite:///./expense_tracker.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    amount = Column(Float)
    date = Column(Date)

# Create Database
Base.metadata.create_all(bind=engine)

# Pydantic Schema
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    date: str

class ExpenseUpdate(BaseModel):
    title: str = None
    amount: float = None
    date: str = None
    
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create a new user
@app.post("/register/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# User Login
@app.post("/login/")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    return {"message": "Login Successful"}

# JWT Token Generation
SECRET_KEY = "your secret key"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Add a new expense
@app.post("/expenses/")
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = Expense(title=expense.title, amount=expense.amount, date=expense.date)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

# Update an expense
@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    if expense.title:
        db_expense.title = expense.title
    if expense.amount:
        db_expense.amount = expense.amount
    if expense.date:
        db_expense.date = expense.date
    db.commit()
    db.refresh(db_expense)
    return db_expense

# Remove an expense
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(db_expense)
    db.commit()
    return

# List past expenses
@app.get("/expenses/")
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()

# Filter by Last week
@app.get("/expenses/last_week/")
def get_last_week_expenses(db: Session = Depends(get_db)):
    last_week = datetime.now() - timedelta(days=7)
    return db.query(Expense).filter(Expense.date >= last_week).all()

# Filter by Last month
@app.get("/expenses/last_month/")
def get_last_month_expenses(db: Session = Depends(get_db)):
    last_month = datetime.now() - timedelta(days=30)
    return db.query(Expense).filter(Expense.date >= last_month).all()

# Filter by Last 3 months
@app.get("/expenses/last_3_months/")
def get_last_3_months_expenses(db: Session = Depends(get_db)):
    last_3_months = datetime.now() - timedelta(days=90)
    return db.query(Expense).filter(Expense.date >= last_3_months).all()

# Filter by Custom date range
@app.get("/expenses/custom_date_range/")
def get_custom_date_range_expenses(start_date: str, end_date: str, db: Session = Depends(get_db)):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    return db.query(Expense).filter(Expense.date >= start_date, Expense.date <= end_date).all()

