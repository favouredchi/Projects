# Create a URL Shortner that Generates a short URL for a given long URL, Saves mappings in an SQLite database, Supports seamless redirection when a short URL is accessed
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from random import choices
import string 
import sqlite3
from starlette.responses import RedirectResponse

app = FastAPI

# Database setup
conn = sqlite3.connect("urls.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENTS,
    short TEXT UNIQUE,
    long TEXT UNIQUE,
)
                                             )               )
""")
conn.commit()

#URL Model
class URLRequest(BaseModel):
    long_url:str

# Function to generate a short URL
def generate_short_url():
    return ''.join(choices(string.ascii_leters + string.digits, k=6))

@app.post("/shorten/")
def shorten_url(request: URLRequest):
    shorten_url = generate_short_url()
    cursor.execute("INSERT INTO urls (short, long) VALUES (?, ?)", (shorten_url, request.long_url))
    conn.commit()
    return {"short_url": f:http://localhost:8000/{shorten_url}"}


@app.get("/{short_url}")
def redirect_to_long_url(short_url: str):