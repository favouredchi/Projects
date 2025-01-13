# Create an expense tracker that allows users to track their expenses. The service should have the following features:
# Sign up a new user, generate and validate a JWT authentication and user session, list and filter past expenses(past week, last month. last 3 months, custom start and end date) 
# add new expenses, remove existing expenses, update existing expenses, update expenses.

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi import APIRouter

app = FastAPI()

# Database Setup
DATABASE_URL = "sqlite:///./expense.db"
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
    user_id = Column(Integer)
    amount = Column(Float)
    description = Column(String)
    date = Column(DateTime, default=datetime.now)

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
    amount: float
    description: str

class ExpenseUpdate(BaseModel):
    amount: float
    description: str

class ExpenseFilter(BaseModel):
    start_date: datetime
    end_date: datetime

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username)
    if user is None:
        raise credentials_exception
    return user

# Dependency
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Dependency
def get_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Dependency
def get_expense(db: Session, expense_id: int):
    return db.query(Expense).filter(Expense.id == expense_id).first()

# Dependency
def get_expenses(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= start_date, Expense.date <= end_date).all()

# Dependency
def get_expenses_all(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).all()

# Dependency
def get_expenses_week(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=7)).all()

# Dependency
def get_expenses_month(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=30)).all()

# Dependency
def get_expenses_three_months(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=90)).all()

# Dependency
def get_expenses_custom(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= start_date, Expense.date <= end_date).all()

# Dependency
def get_expenses_total(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).count()

# Dependency
def get_expenses_total_amount(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).sum(Expense.amount)

# Dependency
def get_expenses_total_week(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=7)).count()

# Dependency
def get_expenses_total_amount_week(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=7)).sum(Expense.amount)

# Dependency
def get_expenses_total_month(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=30)).count()    

# Dependency
def get_expenses_total_amount_month(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=30)).sum(Expense.amount)

# Dependency
def get_expenses_total_three_months(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=90)).count()

# Dependency
def get_expenses_total_amount_three_months(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=90)).sum(Expense.amount)

# Dependency
def get_expenses_total_custom(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= start_date, Expense.date <= end_date).count()

# Dependency
def get_expenses_total_amount_custom(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= start_date, Expense.date <= end_date).sum(Expense.amount)

# Dependency
def get_expenses_total_week(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=7)).count()

# Dependency
def get_expenses_total_amount_week(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=7)).sum(Expense.amount)

# Dependency
def get_expenses_total_month(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=30)).count()

# Dependency
def get_expenses_total_amount_month(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=30)).sum(Expense.amount)

# Dependency
def get_expenses_total_three_months(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=90)).count()

# Dependency
def get_expenses_total_amount_three_months(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=90)).sum(Expense.amount)

# Dependency
def get_expenses_total_custom(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= start_date, Expense.date <= end_date).count()

# Dependency
def get_expenses_total_amount_custom(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= start_date, Expense.date <= end_date).sum(Expense.amount)

# Dependency
def get_expenses_total(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).count()

# Dependency
def get_expenses_total_amount(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).sum(Expense.amount)

# Dependency
def get_expenses_total_week(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=7)).count()

# Dependency
def get_expenses_total_amount_week(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=7)).sum(Expense.amount)

# Dependency
def get_expenses_total_month(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=30)).count()

# Dependency
def get_expenses_total_amount_month(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=30)).sum(Expense.amount)

# Dependency
def get_expenses_total_three_months(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=90)).count()

# Dependency
def get_expenses_total_amount_three_months(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= datetime.now() - timedelta(days=90)).sum(Expense.amount)

# Dependency
def get_expenses_total_custom(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= start_date, Expense.date <= end_date).count()

# Dependency
def get_expenses_total_amount_custom(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return db.query(Expense).filter(Expense.user_id == user_id, Expense.date >= start_date, Expense.date <= end_date).sum(Expense.amount)

# Dependency
def get_expenses_total(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).count()

# Dependency
def get_expenses_total_amount(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).sum(Expense.amount)

# Dependency
def add_expense(db: Session, user_id: int, expense: ExpenseCreate):
    db_expense = Expense(user_id=user_id, amount=expense.amount, description=expense.description)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# Dependency
def update_expense(db: Session, expense_id: int, expense: ExpenseUpdate):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    db_expense.amount = expense.amount
    db_expense.description = expense.description
    db.commit()
    db.refresh(db_expense)
    return db_expense

# Dependency
def delete_expense(db: Session, expense_id: int):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    db.delete(db_expense)
    db.commit()
    return

# Dependency
def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Dependency
def hash_password(password: str):
    return pwd_context.hash(password)

# Dependency
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Dependency
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

# Dependency
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username)
    if user is None:
        raise credentials_exception
    return user


