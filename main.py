from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import bcrypt

app = FastAPI()

# CORS Middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database (fake_db) to store users
fake_db = []

# Pydantic models for registration and login
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Helper functions for password hashing
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@app.get('/')
async def hello():
    return {"message": "First Blank page"}

# Register Endpoint
@app.post("/register/", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    """
    Register a new user with:
    - Unique username
    - Hashed password
    - Email
    """
    # If user already exists
    if any(u['username'] == user.username for u in fake_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # If email already exists
    if any(u['email'] == user.email for u in fake_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with hashed password
    new_user = {
        "username": user.username,
        "password": hash_password(user.password),
        "email": user.email
    }
    
    fake_db.append(new_user)
    print(fake_db)  # Log to console to see the list of users
    
    return {
        "status": status.HTTP_201_CREATED,
        "message": "User registered successfully",
        "user": {
            "username": user.username,
            "email": user.email
        }
    }

# Login Endpoint
@app.post("/login/")
async def login(user: UserLogin):
    """
    Authenticate user with:
    - Valid username
    - Correct password
    """
    # Find user in fake DB
    db_user = next((u for u in fake_db if u['username'] == user.username), None)
    
    # Case 1: User doesn't exist
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Case 2: Password doesn't match
    if not verify_password(user.password, db_user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    print(fake_db)  # Log the user data to console

    # Case 3: Successful login
    return {
        "status": status.HTTP_200_OK,
        "message": "Login successful",
        "user": {
            "username": db_user['username'],
            "email": db_user['email']
        }
    }
